"""Bounded Unix client with protected server identity; no authority imports."""
import socket
import struct
import sys
from pathlib import Path
from ..contract import canonical_json_bytes as encoded,parse_canonical_json
from .protocol import decode_base64,encode_frame,fields as closed_fields,parse_request
from .transport import receive


def verify_server_credentials(raw,*,expected_uid):
    if type(expected_uid) is not int or expected_uid<=0 or type(raw) is not bytes or len(raw)!=struct.calcsize('3i'):
        raise ValueError('protected server identity required')
    pid,uid,_=struct.unpack('3i',raw)
    if pid<=0 or uid!=expected_uid:
        raise ValueError('protected server identity differs')


def _configuration(socket_path):
    from .runtime import load_instance,installed_code_root
    from .files import read_regular
    from .profile import parse_profile
    if sys.platform!='linux': raise ValueError('Linux peer credentials required')
    config=load_instance(installed_code_root()/'qualification-installation/supervisor.json')
    if str(socket_path)!=config['socket_path']: raise ValueError('protected socket path differs')
    release=parse_canonical_json(read_regular(Path(config['installation_root']),'release.json',limit=16*1024*1024),label='release')
    profile=parse_profile(encoded(release['profile']))
    return config, profile


def request(socket_path:Path,operation:str,fields:dict)->bytes:
    config, profile = _configuration(socket_path)
    raw=encoded(dict(operation=operation,**fields))
    if 'schema' in fields:
        from .campaign_protocol import parse_campaign_request
        parse_campaign_request(raw)
    else:
        parse_request(raw)
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as connection:
        connection.settimeout(profile.capture_seconds)
        connection.connect(str(socket_path))
        verify_server_credentials(connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,struct.calcsize('3i')),
                                  expected_uid=config['service_uid'])
        connection.sendall(encode_frame(raw,limit=profile.rpc_byte_limit))
        connection.shutdown(socket.SHUT_WR)
        response=parse_canonical_json(receive(connection,limit=profile.rpc_byte_limit),label='service response')
    if response.get('ok') is not True:
        closed_fields(response,{'ok','error'})
        raise ValueError(response['error'])
    closed_fields(response,{'ok','data_b64'})
    return decode_base64(response['data_b64'])



def fetch_campaign_plan(socket_path: Path, *, attempt_id: str) -> bytes:
    """Read historical plan bytes only after validating every chunk and whole hash."""
    from ..checkpoint_plan import _CAMPAIGN_MAX_BYTES
    from .campaign_protocol import CAMPAIGN_REQUEST_SCHEMA, PLAN_CHUNK_LIMIT
    from .protocol import identity, digest, sha256
    identity(attempt_id)
    _, profile = _configuration(socket_path)
    base = dict(schema=CAMPAIGN_REQUEST_SCHEMA, attempt_id=attempt_id)
    status = parse_canonical_json(request(socket_path, 'STATUS', base), label='campaign status')
    receipt = status.get('receipt') if type(status) is dict else None
    if type(receipt) is not dict or receipt.get('attempt_id') != attempt_id or receipt.get('profile_sha256') != profile.sha256:
        raise ValueError('campaign receipt identity differs')
    total = receipt.get('plan_byte_length')
    expected = digest(receipt.get('plan_sha256'))
    if type(total) is not int or not 0 < total <= min(_CAMPAIGN_MAX_BYTES, profile.input_byte_limit):
        raise ValueError('campaign plan total exceeds bound')
    result = bytearray()
    while len(result) < total:
        offset = len(result)
        length = min(PLAN_CHUNK_LIMIT, total - offset)
        chunk = closed_fields(parse_canonical_json(request(socket_path, 'FETCH_PLAN_CHUNK',
            dict(base, object_sha256=expected, offset=offset, length=length)), label='plan chunk'),
            {'schema', 'attempt_id', 'object_sha256', 'offset', 'total_byte_length', 'byte_length', 'bytes_b64'})
        if (chunk['schema'] != 'qualification_campaign_plan_chunk/v1'
                or chunk['attempt_id'] != attempt_id or chunk['object_sha256'] != expected
                or type(chunk['offset']) is not int or chunk['offset'] != offset
                or type(chunk['total_byte_length']) is not int or chunk['total_byte_length'] != total
                or type(chunk['byte_length']) is not int or chunk['byte_length'] != length):
            raise ValueError('campaign chunk metadata differs')
        # Bound even a malicious encoded string before allocating its decoding.
        if type(chunk['bytes_b64']) is not str or len(chunk['bytes_b64']) != 4 * ((length + 2) // 3):
            raise ValueError('campaign chunk encoding length differs')
        part = decode_base64(chunk['bytes_b64'])
        if len(part) != length:
            raise ValueError('campaign chunk payload length differs')
        result.extend(part)
    raw = bytes(result)
    if sha256(raw) != expected:
        raise ValueError('campaign plan digest differs')
    return raw
