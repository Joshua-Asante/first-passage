"""Bounded observation acquisition; no execution credit, retry or resume authority."""
from datetime import datetime
import math
import urllib.parse

from .journal import utc_now
from .transport import ReadError


def _date(value, *, require_zone=True):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed if parsed.tzinfo is not None or not require_zone else None
    except (ValueError, TypeError, AttributeError):
        return None


def _markers(body):
    flags = set()
    if isinstance(body, dict):
        if body.get('partial') is True or body.get('unavailable'):
            flags.add('partial_response')
        if body.get('error'):
            flags.add('provider_error')
        for value in body.values():
            flags.update(_markers(value))
    elif isinstance(body, list):
        for value in body:
            flags.update(_markers(value))
    return flags


def _valid_fill(row):
    strings = ('executionId', 'accountName', 'environment', 'instrument', 'root', 'tradeDate')
    integers = ('fillId', 'orderId', 'accountId', 'qty')
    return (isinstance(row, dict)
            and all(isinstance(row.get(k), str) and row[k] for k in strings)
            and all(type(row.get(k)) is int and row[k] > 0 for k in integers)
            and row.get('action') in ('Buy', 'Sell')
            and _date(row.get('timestamp')) is not None
            and all(type(row.get(k)) in (int, float) and math.isfinite(row[k])
                    for k in ('price', 'commission', 'fees')))


def collect(client, journal, account, *, limit=500, max_pages=10):
    """Collect once. Completed acquisition is still unqualified broker evidence."""
    if account != journal.account:
        raise ValueError('journal account mismatch')
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError('invalid page limit')
    if type(max_pages) is not int or not 1 <= max_pages <= 100:
        raise ValueError('invalid page budget')
    run_id = journal.start()
    quoted = urllib.parse.quote(account, safe='')
    base = '/v1/api/tv/accounts/' + quoted
    requests = [('snapshot', '/v1/api/tv/accounts/snapshot'),
                ('positions', base + '/positions'), ('orders', base + '/orders'),
                ('fills', base + '/fills')]
    cursor = None
    cursors = set()
    execution_ids = set()
    exhausted = False
    account_id = None
    for index in range(4 + max_pages):
        if index < 4:
            kind, path = requests[index]
        else:
            kind = 'history'
            query = dict(account=account, limit=limit)
            if cursor:
                query['cursor'] = cursor
            path = '/v1/api/tv/fills/history?' + urllib.parse.urlencode(query)
        started = utc_now()
        try:
            status, body = client.get(path)
            flags = _markers(body)
            valid = status == 200 and isinstance(body, dict) and body.get('success') is True
            if status != 200:
                flags.add('http_error')
            elif not valid:
                flags.add('malformed_envelope')
        except ReadError as exc:
            allowed = {'timeout', 'transport_error', 'invalid_json', 'response_too_large', 'redirect_refused'}
            code = str(exc) if str(exc) in allowed else 'read_error'
            status, body, flags, valid = None, {'read_error': code}, {code}, False
        fills = []
        if valid and kind == 'snapshot':
            accounts = body.get('accounts')
            valid = isinstance(accounts, list)
            snapshot_time = _date(body.get('asOf'), require_zone=False)
            if snapshot_time is None:
                flags.add('snapshot_time_unavailable')
            elif snapshot_time.tzinfo is None:
                flags.add('snapshot_timezone_unavailable')
            if valid:
                targets = [r for r in accounts if isinstance(r, dict)
                           and str(r.get('name', '')).casefold() == account.casefold()]
                if len(targets) != 1:
                    flags.add('account_mismatch')
                elif not all(isinstance(targets[0].get(k), list) for k in ('positions', 'workingOrders')):
                    valid = False
                else:
                    account_id = str(targets[0]['accountId']) if targets[0].get('accountId') is not None else None
                    if account_id is None:
                        flags.add('account_binding_unavailable')
                previous = journal.previous_snapshot()
                old_time = _date(previous.get('asOf')) if isinstance(previous, dict) else None
                if snapshot_time and isinstance(previous, dict) and previous.get('asOf') == body.get('asOf'):
                    flags.add('cached_snapshot')
                elif old_time and snapshot_time and snapshot_time.tzinfo is not None and snapshot_time < old_time:
                    flags.add('regressed_snapshot')
            if not valid:
                flags.add('malformed_envelope')
        elif valid:
            if not isinstance(body.get('data'), list):
                valid = False
                flags.add('malformed_envelope')
            elif kind != 'history':
                for row in body['data']:
                    if not isinstance(row, dict):
                        flags.add('malformed_envelope')
                    elif account_id is None or row.get('accountId') is None:
                        flags.add('account_binding_unavailable')
                    elif str(row['accountId']) != account_id:
                        flags.add('account_mismatch')
        if valid and kind == 'history':
            valid = ('nextCursor' in body and (body['nextCursor'] is None or
                     isinstance(body['nextCursor'], str) and bool(body['nextCursor']))
                     and type(body.get('count')) is int and body['count'] == len(body['data']))
            if not valid:
                flags.add('malformed_history')
            else:
                for row in body['data']:
                    if not _valid_fill(row):
                        flags.add('malformed_fill')
                        valid = False
                    elif (row['accountName'].casefold() != account.casefold()
                          or account_id is not None and str(row['accountId']) != account_id):
                        flags.add('account_mismatch')
                        valid = False
                    elif account_id is None:
                        flags.add('account_binding_unavailable')
                        valid = False
                    else:
                        if row['executionId'] in execution_ids:
                            flags.add('duplicate_execution')
                        execution_ids.add(row['executionId'])
                        fills.append(row)
                cursor = body['nextCursor']
                if valid:
                    if cursor is None:
                        exhausted = True
                    elif cursor in cursors:
                        valid = False
                        flags.add('cursor_loop')
                    else:
                        cursors.add(cursor)
                        if index == 3 + max_pages:
                            flags.add('page_budget_exhausted')
        journal.record(run_id, kind, started, status, body, flags, fills)
        if kind == 'history' and (not valid or exhausted):
            break
    return journal.finish(run_id, exhausted)
