"""Durable rejection only; no broker evidence or permission to trade."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
import sqlite3

import pytest

from book_halt import BookHaltStore, HaltStoreError
from c1_rail_listener import handle_signal
from c1_rail_http_server import make_handler


def test_reboot_preserves_incidents_and_fences_old_owner(tmp_path):
    path = tmp_path / 'halt.sqlite'
    first = BookHaltStore.boot(path, 'account')
    first.halt('incident', 'feed')
    before = first.snapshot()
    second = BookHaltStore.boot(path, 'account')
    after = second.snapshot()
    assert after['permission'] == 'HALTED'
    assert after['generation'] > before['generation']
    assert after['boot_id'] != before['boot_id']
    assert 'incident' in {x['incident_id'] for x in after['incidents']}
    with pytest.raises(HaltStoreError):
        first.halt('stale', 'feed')
    assert 'unavailable' in first.rejection_reason()


def test_duplicate_is_read_only_but_conflict_refused(tmp_path):
    store = BookHaltStore.boot(tmp_path / 'halt.sqlite', 'account')
    first = store.halt('incident', 'feed')
    assert store.halt('incident', 'feed') == first
    with pytest.raises(HaltStoreError):
        store.halt('incident', 'operator')
    assert store.snapshot() == first


def test_concurrent_incidents_are_not_lost(tmp_path):
    store = BookHaltStore.boot(tmp_path / 'halt.sqlite', 'account')
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda i: store.halt(f'fault-{i}', 'feed'), range(12)))
    state = store.snapshot()
    assert len(state['incidents']) == 13
    assert state['generation'] == 13


def test_other_account_does_not_replace_state(tmp_path):
    path = tmp_path / 'halt.sqlite'
    store = BookHaltStore.boot(path, 'account')
    before = store.snapshot()
    with pytest.raises(HaltStoreError):
        BookHaltStore.boot(path, 'different')
    assert store.snapshot() == before


def test_corruption_is_not_reinitialized(tmp_path):
    path = tmp_path / 'halt.sqlite'
    path.write_bytes(b'corrupt')
    with pytest.raises(HaltStoreError):
        BookHaltStore.boot(path, 'account')
    assert path.read_bytes() == b'corrupt'


def test_running_injected_into_database_never_grants_permission(tmp_path):
    path = tmp_path / 'halt.sqlite'
    store = BookHaltStore.boot(path, 'account')
    with sqlite3.connect(path) as conn:
        conn.execute("UPDATE state SET permission='RUNNING'")
    assert 'unavailable' in store.rejection_reason()
    with pytest.raises(HaltStoreError):
        BookHaltStore.boot(path, 'account')


class NoSizing:
    def process_signal(self, *args, **kwargs):
        raise AssertionError('halted input must not reach sizing')


@pytest.mark.parametrize('kind', ['entry', 'add'])
@pytest.mark.parametrize('leg_id', ['aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7'])
def test_unconfigured_book_never_reaches_sizing_or_sender(kind, leg_id):
    result = handle_signal({'leg_id': leg_id, 'signal_type': kind}, NoSizing(), 0,
                           config={'dry_run': False}, sender=lambda *args: pytest.fail('send'))
    assert result.decision.halt and not result.sent
    assert 'book' in result.decision.halt_reason.lower()


def test_configured_legacy_entry_is_blocked_before_sizing(tmp_path):
    store = BookHaltStore.boot(tmp_path / 'halt.sqlite', 'account')
    result = handle_signal({'leg_id': 'dj30_mym', 'signal_type': 'entry'}, NoSizing(), 0,
                           config={'dry_run': False}, book_halt=store,
                           sender=lambda *args: pytest.fail('send'))
    assert result.decision.halt and not result.sent


def test_handler_boot_creates_store_and_rejects_corruption(tmp_path):
    path = tmp_path / 'halt.sqlite'
    cfg = {'account': 'account', 'book_halt_path': str(path)}
    make_handler(NoSizing(), cfg)
    with sqlite3.connect(path) as conn:
        assert conn.execute('SELECT permission FROM state').fetchone() == ('HALTED',)
        conn.execute("UPDATE state SET permission='RUNNING'")
    with pytest.raises(HaltStoreError):
        make_handler(NoSizing(), cfg)


@pytest.mark.parametrize('path', ['', None, False, 123])
def test_invalid_config_path_does_not_silently_disable_gate(path):
    with pytest.raises(HaltStoreError):
        make_handler(NoSizing(), {'account': 'account', 'book_halt_path': path})


def test_http_request_passes_boot_store_to_real_listener(tmp_path, monkeypatch):
    import c1_rail_http_server as http
    equity = tmp_path / 'equity.json'
    equity.write_text(json.dumps({'current_equity': 100000}))
    dd = tmp_path / 'dd.json'
    dd.write_text(json.dumps({'peak_equity': 100000}))
    cfg = {'account': 'account', 'book_halt_path': str(tmp_path / 'halt.sqlite'),
           'path_token': 'x' * 32, 'equity_source': 'file', 'equity_path': str(equity),
           'dd_state_path': str(dd), 'secret_key': 'test', 'webhook_id': 'test',
           'webhook_secret': 'test', 'dry_run': False}
    calls = []

    def route(*args, **kwargs):
        calls.append(kwargs['book_halt'].snapshot())
        return handle_signal(*args, **kwargs, sender=lambda *a: pytest.fail('send'))

    monkeypatch.setattr(http, 'handle_signal', route)
    handler = make_handler(NoSizing(), cfg)
    body = json.dumps({'leg_id': 'dj30_mym', 'signal_type': 'entry',
                       'bar_time': 1, 'close': 1, 'stop_dist_pts': 1}).encode()
    request = (f'POST /c1/{cfg["path_token"]} HTTP/1.0\r\nContent-Length: {len(body)}\r\n'
               'Content-Type: application/json\r\n\r\n').encode() + body

    class Connection:
        response = b''

        def makefile(self, *args):
            return BytesIO(request)

        def sendall(self, data):
            self.response += bytes(data)

    conn = Connection()
    handler(conn, ('127.0.0.1', 1), object())
    assert len(calls) == 1 and calls[0]['permission'] == 'HALTED'
    assert b'200' in conn.response.split(b'\r\n')[0]
