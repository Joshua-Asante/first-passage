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


def request(socket_path:Path,operation:str,fields:dict)->bytes:
    from .runtime import load_instance,installed_code_root
    from .files import read_regular
    from .profile import parse_profile
    if sys.platform!='linux': raise ValueError('Linux peer credentials required')
    config=load_instance(installed_code_root()/'qualification-installation/supervisor.json')
    if str(socket_path)!=config['socket_path']: raise ValueError('protected socket path differs')
    release=parse_canonical_json(read_regular(Path(config['installation_root']),'release.json',limit=16*1024*1024),label='release')
    profile=parse_profile(encoded(release['profile']))
    raw=encoded(dict(operation=operation,**fields))
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
