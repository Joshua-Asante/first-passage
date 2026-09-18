"""Peer credential parser units; real socket credentials require Linux tests."""
import importlib
import struct
import pytest


@pytest.mark.parametrize('uid',[0,1002,65534])
def test_wrong_server_identity_rejected(uid):
    client=importlib.import_module('c1_rail.qualification.execution.client')
    with pytest.raises(ValueError,match='server identity'):
        client.verify_server_credentials(struct.pack('3i',42,uid,uid),expected_uid=1001)


def test_expected_server_identity_passes():
    client=importlib.import_module('c1_rail.qualification.execution.client')
    assert client.verify_server_credentials(struct.pack('3i',42,1001,1001),expected_uid=1001) is None
