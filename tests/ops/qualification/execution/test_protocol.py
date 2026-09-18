"""Untrusted request bytes cannot add authority or alternative execution inputs."""
import importlib
import struct

import pytest


def protocol():
    return importlib.import_module('c1_rail.qualification.execution.protocol')


@pytest.mark.parametrize('raw', [
    b'{"operation":"STATUS","attempt_id":"a","attempt_id":"b"}',
    b'{"attempt_id":"a", "operation":"STATUS"}',
    b'{"attempt_id":"a","operation":"STATUS","path":"/tmp/journal"}',
    b'{"attempt_id":"a","operation":"COMPLETE_CHECKPOINT"}',
    b'{"attempt_id":"a","operation":"SIGN"}',
    b'{"attempt_id":"a","operation":"SUBMIT_N1","bundle_sha256":"bad"}',
    b'{"attempt_id":true,"operation":"STATUS"}',
])
def test_request_rejects_noncanonical_unknown_or_substituted_inputs(raw):
    with pytest.raises(ValueError):
        protocol().parse_request(raw)


def test_request_accepts_only_closed_identity_submission():
    raw = b'{"attempt_id":"a","bundle_sha256":"' + b'a' * 64 + b'","operation":"SUBMIT_N1"}'
    assert protocol().parse_request(raw) == {
        'attempt_id': 'a', 'bundle_sha256': 'a' * 64, 'operation': 'SUBMIT_N1'}


@pytest.mark.parametrize('suffix', [b'\0', struct.pack('!I', 2) + b'{}'])
def test_extra_stdout_or_second_frame_is_never_a_success(suffix):
    with pytest.raises(ValueError, match='frame'):
        protocol().decode_frame(struct.pack('!I', 2) + b'{}' + suffix, limit=10)


@pytest.mark.parametrize('raw', [b'', b'\0\0', struct.pack('!I', 9) + b'{}', struct.pack('!I', 99)])
def test_truncation_and_oversize_fail_closed(raw):
    with pytest.raises(ValueError, match='frame'):
        protocol().decode_frame(raw, limit=10)


def test_one_bounded_frame_roundtrips_exact_bytes():
    assert protocol().decode_frame(protocol().encode_frame(b'{}', limit=2), limit=2) == b'{}'


def test_snapshot_and_artifact_requests_have_closed_shapes():
    from c1_rail.qualification.contract import canonical_json_bytes as encoded
    assert protocol().parse_request(encoded(dict(operation='SNAPSHOT',attempt_id='a')))['operation']=='SNAPSHOT'
    row=dict(operation='STORE_ARTIFACT',attempt_id='a',role='n1_result',bytes_b64='e30=')
    assert protocol().parse_request(encoded(row))==row
    for changes in (dict(path='/tmp/key'),dict(role='private-result'),dict(bytes_b64='not base64')):
        with pytest.raises(ValueError): protocol().parse_request(encoded(dict(row,**changes)))


def test_deep_untrusted_json_is_rejected_without_recursion_escape():
    raw=b'['*1500+b'0'+b']'*1500
    with pytest.raises(ValueError):
        protocol().decode_frame(struct.pack('!I',len(raw))+raw,limit=4096)
