"""Actual bounded scheduling; peer UID/capture acceptance requires Linux tests."""
from concurrent.futures import ThreadPoolExecutor
from threading import Event
import pytest

from c1_rail.qualification.execution import service


def test_incomplete_peer_cannot_serialize_other_connections():
    dispatcher=getattr(service,'BoundedConnections',None)
    assert dispatcher is not None, 'service needs bounded concurrent peer handling'
    entered,release=Event(),Event()
    def handle(connection):
        if connection=='slow':
            entered.set()
            assert release.wait(5)
        return connection
    with dispatcher(handle,limit=2) as connections:
        slow=connections.submit('slow')
        try:
            assert entered.wait(2)
            assert connections.submit('authorized').result(timeout=2)=='authorized'
        finally:
            release.set()
        assert slow.result(timeout=2)=='slow'


def test_request_admission_is_bounded_until_a_handler_completes():
    dispatcher=getattr(service,'BoundedConnections',None)
    assert dispatcher is not None, 'service needs bounded concurrent peer handling'
    entered,release,attempted,third_entered=Event(),Event(),Event(),Event()
    def handle(connection):
        if connection==1:
            entered.set(); assert release.wait(5)
        else: third_entered.set()
        return connection
    with dispatcher(handle,limit=1) as connections,ThreadPoolExecutor(max_workers=1) as callers:
        first=connections.submit(1)
        assert entered.wait(2)
        def submit():
            attempted.set()
            return connections.submit(2)
        second=callers.submit(submit)
        try:
            assert attempted.wait(2)
            with pytest.raises(TimeoutError): second.result(timeout=.2)
            assert not third_entered.is_set()
        finally: release.set()
        assert first.result(timeout=2)==1 and second.result(timeout=2).result(timeout=2)==2
