"""SYNTHETIC broker observations; persistent owner engineering, no qualification."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import sqlite3

import pytest

from book_halt import BookHaltStore, HaltStoreError
from book_recovery import RecoveryOwner, RecoveryDemand, RecoveryEvidence


class SyntheticRoute:
    """SYNTHETIC external causal producer and synchronous recording transport."""
    def __init__(self, outcome='accepted'):
        self.sequence = 10
        self.calls = []
        self.outcome = outcome

    def boundary(self):
        self.sequence += 1
        return {'domain': 'synthetic-domain', 'sequence': self.sequence,
                'timestamp': f'2026-09-14T12:00:{self.sequence:02d}+00:00'}

    def send(self, command):
        self.calls.append(command)
        return {'state': self.outcome, 'filled_quantity': 1 if self.outcome == 'partial' else 0}


def evidence(symbol='MYMZ6', product='MYM'):
    return RecoveryEvidence(
        account='account', route='SYNTHETIC', version='fixture-v1',
        domain='synthetic-domain', acquisition_id='capture-' + symbol,
        timestamp='2026-09-14T12:00:01+00:00', sequence=1,
        orders=({'order_id': 'order-' + symbol, 'request_id': 'original-' + symbol,
                 'authority_digest': 'a' * 64, 'symbol': symbol, 'side': 'buy',
                 'kind': 'risk_add', 'quantity': 3, 'remaining': 1},),
        allocations=({'execution_id': 'fill-' + symbol, 'lot_id': 'lot-' + symbol,
                      'order_id': 'order-' + symbol, 'quantity': 2, 'sequence': 1},),
        protection=({'owner_id': 'owner-' + symbol, 'origin_execution_id': 'fill-' + symbol,
                     'quantity': 2, 'components': ({'order_ref': 'stop-' + symbol,
                        'kind': 'stop', 'side': 'sell', 'quantity': 2,
                        'linkage': 'oco-' + symbol, 'parameters': {'price': '10', 'anchor': '11'}},)},),
        observed_symbols=(symbol,),
        bindings=({'product': product, 'symbol': symbol, 'evidence_digest': 'b' * 64},),
    )


def demand(symbol='MYMZ6', product='MYM', operation_id='close-1'):
    return RecoveryDemand(operation_id=operation_id, incident_id='fault', kind='CLOSE',
                          symbol=symbol, scope_ids=('product:' + product,),
                          order_ids=('order-' + symbol,))


def owner_at(tmp_path, route=None, products=('MYM',)):
    owner = RecoveryOwner.boot(tmp_path / 'book.db', 'account', controlled_products=products)
    owner.report_fault('fault', 'execution')
    return owner if route is None else RecoveryOwner.synthetic(owner, route)


def test_graph_duplicate_and_changed_identity(tmp_path):
    owner = owner_at(tmp_path)
    first = owner.prepare(demand(), evidence=evidence())
    assert owner.prepare(demand(), evidence=evidence()) == first
    with pytest.raises(HaltStoreError):
        owner.prepare(replace(demand(), kind='CANCEL'), evidence=evidence())
    snapshot = owner.snapshot()
    assert len(snapshot['operations']) == 1
    assert snapshot['operations'][0]['orders'][0]['request_id'] == 'original-MYMZ6'
    assert snapshot['operations'][0]['protection'][0]['owner_id'] == 'owner-MYMZ6'
    assert snapshot['operations'][0]['allocations'][0]['execution_id'] == 'fill-MYMZ6'


def test_production_dispatch_is_unavailable_and_pure_status(tmp_path):
    owner = owner_at(tmp_path)
    owner.prepare(demand(), evidence=evidence())
    assert owner.dispatch('close-1')['status'] == 'blocked'
    before = owner.snapshot()
    assert before['attempts'] == []
    assert owner.snapshot() == before
    assert any(o['reason'] == 'capability' for o in before['obligations'])


@pytest.mark.parametrize('outcome', ['accepted', 'partial', 'rejected', 'unknown'])
def test_attempt_original_identity_never_retried_or_completed(tmp_path, outcome):
    route = SyntheticRoute(outcome)
    owner = owner_at(tmp_path, route)
    owner.prepare(demand(), evidence=evidence())
    owner.dispatch('close-1')
    owner.dispatch('close-1')
    assert len(route.calls) == 1
    state = owner.snapshot()
    assert state['attempts'][0]['state'] == 'UNKNOWN'
    assert state['attempts'][0]['observation']['state'] == outcome
    assert state['operations'][0]['status'] == 'unresolved'
    restarted = RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM',))
    restarted.dispatch('close-1')
    assert restarted.snapshot()['attempts'] == state['attempts']
    assert len(route.calls) == 1


def test_durable_boundary_visible_to_transport(tmp_path):
    route = SyntheticRoute()
    owner = owner_at(tmp_path, route)
    owner.prepare(demand(), evidence=evidence())
    original_send = route.send
    def send(command):
        with sqlite3.connect(owner.path) as db:
            assert db.execute('SELECT count(*) FROM recovery_attempts').fetchone()[0] == 1
        return original_send(command)
    route.send = send
    owner.dispatch('close-1')
    assert route.calls[0]['request_id'] == owner.snapshot()['attempts'][0]['request_id']


def test_same_symbol_concurrent_work_serializes_and_retains_all(tmp_path):
    route = SyntheticRoute()
    owner = owner_at(tmp_path, route)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda i: owner.prepare(demand(operation_id=f'op-{i}'), evidence=evidence()), range(4)))
        list(pool.map(lambda i: owner.dispatch(f'op-{i}'), range(4)))
    assert len(route.calls) == 1
    assert len(owner.snapshot()['operations']) == 4


def test_two_symbol_batch_is_atomic_and_partial_retains_sibling(tmp_path):
    route = SyntheticRoute('partial')
    owner = owner_at(tmp_path, route, products=('MYM', 'MNQ'))
    a, b = evidence(), evidence('MNQZ6', 'MNQ')
    both = replace(a, orders=a.orders + b.orders, allocations=a.allocations + b.allocations,
                   protection=a.protection + b.protection, observed_symbols=('MYMZ6', 'MNQZ6'),
                   bindings=a.bindings + b.bindings)
    with pytest.raises(HaltStoreError):
        owner.prepare_recovery((demand(),), evidence=both)
    owner.prepare_recovery((demand(), demand('MNQZ6', 'MNQ', 'close-2')), evidence=both)
    owner.dispatch('close-1')
    assert len(owner.snapshot()['operations']) == 2
    assert owner.snapshot()['operations'][1]['status'] == 'prepared'


def test_unknown_order_has_no_cancel_authority(tmp_path):
    route = SyntheticRoute()
    owner = owner_at(tmp_path, route)
    e = evidence()
    e = replace(e, orders=({**e.orders[0], 'authority_digest': None},))
    owner.prepare(replace(demand(), kind='CANCEL'), evidence=e)
    assert owner.dispatch('close-1')['status'] == 'blocked'
    assert route.calls == []
    assert any(x['reason'] == 'unknown_order' for x in owner.snapshot()['obligations'])


def test_bounded_close_refuses_without_overclose(tmp_path):
    route = SyntheticRoute()
    owner = owner_at(tmp_path, route)
    owner.prepare(replace(demand(), quantity=1), evidence=evidence())
    assert owner.dispatch('close-1')['status'] == 'blocked'
    assert not route.calls


@pytest.mark.parametrize('table', ['operation_orders', 'operation_protection',
                                  'operation_allocations', 'recovery_effects', 'operation_scopes'])
def test_missing_graph_child_refuses_restart(tmp_path, table):
    owner = owner_at(tmp_path)
    owner.prepare(demand(), evidence=evidence())
    with sqlite3.connect(owner.path) as db:
        db.execute(f'DELETE FROM {table}')
    with pytest.raises(HaltStoreError):
        owner.snapshot()
    with pytest.raises(HaltStoreError):
        RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM',))


def test_plain_halt_boot_fences_recovery_owner(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute())
    owner.prepare(demand(), evidence=evidence())
    BookHaltStore.boot(owner.path, 'account', controlled_symbols=('MYM',))
    with pytest.raises(HaltStoreError):
        owner.dispatch('close-1')


def test_batch_with_uncovered_observed_location_refuses(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute())
    e = replace(evidence(), observed_symbols=('MYMZ6', 'UNKNOWNZ6'))
    with pytest.raises(HaltStoreError):
        owner.prepare_recovery((demand(),), evidence=e)
    assert owner.snapshot()['operations'] == []


def test_malformed_schema_losing_check_constraint_refuses(tmp_path):
    owner = owner_at(tmp_path)
    with sqlite3.connect(owner.path) as db:
        db.execute('ALTER TABLE recovery_meta RENAME TO old_meta')
        db.execute('CREATE TABLE recovery_meta (event_count INTEGER NOT NULL)')
        db.execute('INSERT INTO recovery_meta SELECT * FROM old_meta')
        db.execute('DROP TABLE old_meta')
    with pytest.raises(HaltStoreError):
        owner.snapshot()


def test_unpublished_recovery_identity_in_graph_refuses_even_with_rehashed_body(tmp_path):
    import json
    from book_recovery_schema import canonical, digest
    owner = owner_at(tmp_path)
    owner.prepare(demand(), evidence=evidence())
    with sqlite3.connect(owner.path) as db:
        body = json.loads(db.execute('SELECT body FROM recovery_operations').fetchone()[0])
        body['generation'] = 999
        db.execute('UPDATE recovery_operations SET body=?, digest=?', (canonical(body), digest(body)))
        db.execute("UPDATE recovery_events SET digest=? WHERE kind='prepared'", (digest(body),))
    with pytest.raises(HaltStoreError):
        owner.snapshot()


def test_synthetic_dispatch_boundary_cannot_go_backwards_across_symbols(tmp_path):
    route = SyntheticRoute()
    owner = owner_at(tmp_path, route, products=('MYM', 'MNQ'))
    owner.prepare(demand(), evidence=evidence())
    owner.dispatch('close-1')  # boundary 12
    route.sequence = 10
    with pytest.raises(HaltStoreError):
        owner.prepare(demand('MNQZ6', 'MNQ', 'close-2'), evidence=evidence('MNQZ6', 'MNQ'))


def test_product_scope_cannot_be_attached_to_unrelated_symbol(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute(), products=('MYM', 'MNQ'))
    with pytest.raises(HaltStoreError):
        owner.prepare(demand(product='MNQ'), evidence=evidence())


@pytest.mark.parametrize('change', ['empty', 'parameters', 'side'])
def test_incomplete_owned_protection_is_not_sendable(tmp_path, change):
    owner = owner_at(tmp_path, SyntheticRoute())
    e = evidence()
    protection = dict(e.protection[0])
    component = dict(protection['components'][0])
    if change == 'parameters':
        component['parameters'] = {'garbage': '10'}
    if change == 'side':
        component['side'] = 'buy'
    protection['components'] = () if change == 'empty' else (component,)
    with pytest.raises(HaltStoreError):
        owner.prepare(demand(), evidence=replace(e, protection=(protection,)))


def test_unknown_orders_outside_selected_demand_retain_individual_request_owners(tmp_path):
    owner = owner_at(tmp_path, SyntheticRoute())
    a, b = evidence(), evidence('EXTZ6', 'EXT')
    unknown = {**b.orders[0], 'authority_digest': None}
    other = {**unknown, 'order_id': 'external-2', 'request_id': 'external-request-2'}
    combined = replace(a, orders=a.orders + (unknown, other),
                       observed_symbols=('MYMZ6', 'EXTZ6'), bindings=a.bindings+b.bindings)
    owner.prepare(demand(), evidence=combined)
    before = owner.snapshot()
    orders = [o for o in before['obligations'] if o['reason'] == 'unknown_order']
    requests = [o for o in before['obligations'] if o['reason'] == 'unknown_request']
    assert {o['facts']['order_id'] for o in orders} == {'order-EXTZ6', 'external-2'}
    assert {o['facts']['request_id'] for o in requests} == {'original-EXTZ6', 'external-request-2'}
    restarted = RecoveryOwner.boot(owner.path, 'account', controlled_products=('MYM',))
    assert restarted.snapshot()['obligations'] == before['obligations']
