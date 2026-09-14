"""SYNTHETIC transport fixtures; actual SQLite and collector behavior under test."""
import copy
import io
import json
import sqlite3
import urllib.error

import pytest

from ops.crosstrade_observer.collector import collect
from ops.crosstrade_observer.journal import Journal
from ops.crosstrade_observer.transport import ReadClient, ReadError


def fill(**changes):
    row = dict(executionId='tv:demo:1', fillId=1, orderId=2, accountId=3,
               accountName='SYNTHETIC', environment='demo', instrument='MYM 09-26',
               root='MYM', action='Buy', qty=1, price=42000.0, commission=0.35,
               fees=1.02, timestamp='2026-09-14T14:00:00Z', tradeDate='2026-09-14')
    return {**row, **changes}


class FixtureClient:
    def __init__(self, pages=None, overrides=None):
        self.pages = pages or [dict(success=True, data=[fill()], count=1, nextCursor=None)]
        self.overrides = overrides or {}
        self.paths = []

    def get(self, path):
        self.paths.append(path)
        if path in self.overrides:
            value = self.overrides[path]
            if isinstance(value, Exception):
                raise value
            return copy.deepcopy(value)
        if path.startswith('/v1/api/tv/fills/history?'):
            return 200, copy.deepcopy(self.pages.pop(0))
        if path == '/v1/api/tv/accounts/snapshot':
            return 200, dict(success=True, asOf='2026-09-14T14:00:00Z',
                             asOfEpoch=1789394400000, source='tradovate',
                             accounts=[dict(name='SYNTHETIC', accountId='3',
                                            environment='demo', broker='tradovate',
                                            netLiq=100000, openPnl=0, realizedPnl=0,
                                            weekRealizedPnl=0, positions=[],
                                            workingOrders=[], error=None)],
                             counts=dict(accounts=1, positions=0, workingOrders=0))
        assert path in ('/v1/api/tv/accounts/SYNTHETIC/positions',
                        '/v1/api/tv/accounts/SYNTHETIC/orders',
                        '/v1/api/tv/accounts/SYNTHETIC/fills')
        return 200, dict(success=True, data=[])


def test_collection_survives_restart(tmp_path):
    path = tmp_path / 'observations.db'
    with Journal(path, 'SYNTHETIC') as journal:
        result = collect(FixtureClient(), journal, 'SYNTHETIC')
    with Journal(path, 'SYNTHETIC') as journal:
        assert journal.report(result['run_id']) == result
    assert result['state'] == 'collected'
    assert result['observations'] == 5
    assert result['fill_versions'] == 1
    assert result['qualification'] == dict(E1='unproven', E2='unproven', E3='unproven')
    assert result['history_stored_rows_exhausted'] is True
    assert 'SYNTHETIC' not in json.dumps(result)


def test_pages_fee_revisions_conflicts_and_cache_reuse(tmp_path):
    with Journal(tmp_path / 'observations.db', 'SYNTHETIC') as journal:
        first = collect(FixtureClient(), journal, 'SYNTHETIC')
        second = collect(FixtureClient(pages=[dict(success=True, data=[fill(fees=2.0)],
                                                   count=1, nextCursor=None)]), journal, 'SYNTHETIC')
        third = collect(FixtureClient(pages=[dict(success=True, data=[fill(qty=2)],
                                                  count=1, nextCursor=None)]), journal, 'SYNTHETIC')
        assert first['fill_versions'] == 1
        assert second['fill_versions'] == 1
        assert 'fee_revision' in second['flags']
        assert 'cached_snapshot' in second['flags']
        assert 'economic_conflict' in third['flags']
        assert third['state'] == 'limited'
    with sqlite3.connect(tmp_path / 'observations.db') as db:
        assert db.execute('SELECT COUNT(*) FROM fill_versions').fetchone()[0] == 3
        assert db.execute('SELECT COUNT(*) FROM observations').fetchone()[0] == 15


def test_two_pages_opaque_cursor_and_dedup(tmp_path):
    pages = [dict(success=True, data=[fill()], count=1, nextCursor='opaque+/='),
             dict(success=True, data=[fill(), fill(executionId='tv:demo:4', fillId=4)],
                  count=2, nextCursor=None)]
    client = FixtureClient(pages=pages)
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        result = collect(client, journal, 'SYNTHETIC', limit=2)
    assert result['fill_versions'] == 2
    assert 'duplicate_execution' in result['flags']
    assert 'cursor=opaque%2B%2F%3D' in client.paths[-1]
    assert result['history_stored_rows_exhausted'] is True


@pytest.mark.parametrize('pages,max_pages,flag', [
    ([dict(success=True, data=[], count=0, nextCursor='same')]*2, 5, 'cursor_loop'),
    ([dict(success=True, data=[], count=0, nextCursor='more')], 1, 'page_budget_exhausted'),
    ([dict(success=True, data=[], count=0)], 5, 'malformed_history'),
    ([dict(success=True, data=[fill(accountName='OTHER')], count=1, nextCursor=None)],
     5, 'account_mismatch'),
    ([dict(success=True, data=[fill(accountId=999)], count=1, nextCursor=None)],
     5, 'account_mismatch'),
    ([dict(success=True, data=[fill(qty=True)], count=1, nextCursor=None)],
     5, 'malformed_fill'),
])
def test_history_limits_are_persisted(tmp_path, pages, max_pages, flag):
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        result = collect(FixtureClient(pages=pages), journal, 'SYNTHETIC', max_pages=max_pages)
        assert flag in result['flags']
        assert result['state'] == 'limited'
        assert journal.report(result['run_id']) == result


@pytest.mark.parametrize('response,flag', [
    ((400, dict(success=False, error='private error')), 'http_error'),
    ((200, dict(success=True, data=[], partial=True, unavailable=['commands'])), 'partial_response'),
    ((200, dict(success=True, data=None)), 'malformed_envelope'),
    (ReadError('timeout'), 'timeout'),
])
def test_failed_read_does_not_become_empty_success(tmp_path, response, flag):
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        result = collect(FixtureClient(overrides={
            '/v1/api/tv/accounts/SYNTHETIC/orders': response}), journal, 'SYNTHETIC')
    assert flag in result['flags']
    assert result['state'] == 'limited'
    assert result['observations'] == 5
    assert 'private error' not in json.dumps(result)


def test_interrupted_run_and_wrong_account(tmp_path):
    path = tmp_path / 'db'
    with Journal(path, 'SYNTHETIC') as journal:
        run_id = journal.start()
    with Journal(path, 'SYNTHETIC') as journal:
        assert journal.report(run_id)['state'] == 'running'
        result = collect(FixtureClient(), journal, 'SYNTHETIC')
        assert result['prior_unfinished_runs'] == 1
        with pytest.raises(ValueError):
            collect(FixtureClient(), journal, 'OTHER')
    with pytest.raises(ValueError):
        Journal(path, 'OTHER')


def test_existing_unrelated_database_is_not_modified(tmp_path):
    path = tmp_path / 'db'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE existing (value TEXT)')
    with pytest.raises(ValueError):
        Journal(path, 'SYNTHETIC')
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() == [('existing',)]


class Reply(io.BytesIO):
    status = 200


def test_transport_only_allows_documented_get_and_redacts_secret():
    class Opener:
        def open(self, request, timeout):
            assert request.get_method() == 'GET'
            assert request.full_url == 'https://app.crosstrade.io/v1/api/tv/accounts/snapshot'
            assert request.get_header('Authorization') == 'Bearer private-token'
            assert timeout == 15
            return Reply(b'{"success":true,"echo":"private-token"}')
    client = ReadClient('private-token')
    client.opener = Opener()
    status, body = client.get('/v1/api/tv/accounts/snapshot')
    assert status == 200 and body['echo'] == '[REDACTED]'
    for path in ('https://evil.example', '//evil.example', '/v1/api/tv/accounts/X/orders/place',
                 '/v1/api/tv/accounts/../orders', '/v1/api/tv/fills/history?token=secret'):
        with pytest.raises(ValueError):
            client.get(path)


def test_redirect_handler_refuses_following_credentials():
    client = ReadClient('private-token')
    handlers = [h for h in client.opener.handlers
                if isinstance(h, __import__('urllib.request', fromlist=['HTTPRedirectHandler']).HTTPRedirectHandler)]
    assert len(handlers) == 1
    req = __import__('urllib.request', fromlist=['Request']).Request('https://app.crosstrade.io')
    assert handlers[0].redirect_request(req, None, 302, 'Found', {}, 'https://evil.example') is None


@pytest.mark.parametrize('raw,code', [(b'not json', 'invalid_json'),
                                    (b'{"x":NaN}', 'invalid_json'),
                                    (b'{"x":1e400}', 'invalid_json'),
                                    (b'{"x":1,"x":2}', 'invalid_json'),
                                    (b'x'*2_000_001, 'response_too_large')],
                         ids=['invalid', 'nonfinite', 'overflow', 'duplicate-key', 'oversized'])
def test_transport_bounds_and_strict_json(raw, code):
    class Opener:
        def open(self, *_args, **_kwargs):
            return Reply(raw)
    client = ReadClient('private-token')
    client.opener = Opener()
    with pytest.raises(ReadError, match=code):
        client.get('/v1/api/tv/accounts/snapshot')


def test_run_crash_retains_committed_observations(tmp_path):
    class Interrupted(FixtureClient):
        def get(self, path):
            if path.endswith('/positions'):
                raise KeyboardInterrupt
            return super().get(path)
    path = tmp_path / 'db'
    with Journal(path, 'SYNTHETIC') as journal:
        with pytest.raises(KeyboardInterrupt):
            collect(Interrupted(), journal, 'SYNTHETIC')
    with Journal(path, 'SYNTHETIC') as journal:
        run_id = journal.db.execute('SELECT id FROM runs').fetchone()[0]
        assert journal.report(run_id)['state'] == 'running'
        assert journal.report(run_id)['observations'] == 1


def test_observation_and_fill_revision_commit_atomically(tmp_path):
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        journal.db.execute('''CREATE TRIGGER simulate_disk_error BEFORE INSERT ON fill_versions
            BEGIN SELECT RAISE(ABORT, 'disk failure'); END''')
        with pytest.raises(sqlite3.IntegrityError):
            collect(FixtureClient(), journal, 'SYNTHETIC')
        assert journal.db.execute('SELECT COUNT(*) FROM observations').fetchone()[0] == 4
        assert journal.db.execute('SELECT state FROM runs').fetchone()[0] == 'running'


@pytest.mark.parametrize('data,flag', [(['not an order'], 'malformed_envelope'),
                                     ([dict(accountId=999)], 'account_mismatch')])
def test_scoped_response_rows_validate_account(tmp_path, data, flag):
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        result = collect(FixtureClient(overrides={
            '/v1/api/tv/accounts/SYNTHETIC/orders': (200, dict(success=True, data=data))}),
            journal, 'SYNTHETIC')
    assert flag in result['flags']
    assert result['state'] == 'limited'


def test_cli_success_and_failure_do_not_print_secrets(tmp_path, monkeypatch, capsys):
    from ops.crosstrade_observer import __main__ as cli
    config = tmp_path / 'config.json'
    config.write_text(json.dumps(dict(account='SYNTHETIC', destination='tradovate',
                                     secret_key='private-token')), encoding='utf-8')
    monkeypatch.setattr(cli, 'ReadClient', lambda _secret: FixtureClient())
    code = cli.main(['--config', str(config), '--journal', str(tmp_path / 'db')])
    text = capsys.readouterr().out
    assert code == 0 and json.loads(text)['state'] == 'collected'
    assert 'private-token' not in text and 'SYNTHETIC' not in text
    config.write_text('not json private-token', encoding='utf-8')
    assert cli.main(['--config', str(config), '--journal', str(tmp_path / 'other')]) == 1
    assert 'private-token' not in capsys.readouterr().err


def test_cli_limited_run_is_nonzero(tmp_path, monkeypatch, capsys):
    from ops.crosstrade_observer import __main__ as cli
    config = tmp_path / 'config.json'
    config.write_text(json.dumps(dict(account='SYNTHETIC', destination='tradovate',
                                     secret_key='private-token')), encoding='utf-8')
    monkeypatch.setattr(cli, 'ReadClient', lambda _secret: FixtureClient(overrides={
        '/v1/api/tv/accounts/SYNTHETIC/orders': (403, dict(success=False))}))
    assert cli.main(['--config', str(config), '--journal', str(tmp_path / 'db')]) == 2
    assert json.loads(capsys.readouterr().out)['state'] == 'limited'


def test_snapshot_without_timezone_preserves_binding_but_reports_limitation(tmp_path):
    class NaiveSnapshot(FixtureClient):
        def get(self, path):
            status, body = super().get(path)
            if path.endswith('/snapshot'):
                body['asOf'] = '2026-09-14T23:20:06.476011'
            return status, body
    with Journal(tmp_path / 'db', 'SYNTHETIC') as journal:
        result = collect(NaiveSnapshot(), journal, 'SYNTHETIC')
    assert 'snapshot_timezone_unavailable' in result['flags']
    assert result['fill_versions'] == 1
    assert result['state'] == 'limited'
    assert result['qualification']['E1'] == 'unproven'
