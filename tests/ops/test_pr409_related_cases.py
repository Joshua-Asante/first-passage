"""Related boundary cases for PR409's latest execution and input findings."""
from collections import UserDict
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from fractions import Fraction
import sqlite3

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerFact, BrokerResult
from c1_signal_daemon.book_protocol import Cancel, Side
from c1_signal_daemon.book_runtime import FourLegRuntime
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from test_book_account_owner import NOW, binding, intent, owner
from test_four_leg_runtime import Adapter, LEGS, bars, inert_adapters


@pytest.mark.parametrize('kind,scoped', [('exit', False), ('flat', False), ('exit', True)])
@pytest.mark.parametrize('outcome', ['accepted', 'unknown', 'rejected'])
def test_close_refuses_live_entry_remainder_until_terminal(tmp_path, kind, scoped, outcome):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult(outcome)])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('early', 'base', 'dj30_mym_p250', 'entry', 1, 100, NOW), now=NOW)
    account.dispatch(Cancel('dj30_mym_p250', 'base'),
                     occurrence=account.make_occurrence('direct', 'cancel'), now=NOW)
    close = replace(intent('close'), kind=kind, side=Side.SELL, qty=None,
                    scope_fill_ids=('early',) if scoped else None)
    occurrence = account.make_occurrence('direct', 'close')
    result = account.dispatch(close, occurrence=occurrence, now=NOW)
    assert result.refusal_reason == 'entry_remainder_pending'
    assert [c.kind for c in broker.commands] == ['entry', 'cancel']
    with sqlite3.connect(account.path) as db:
        assert db.execute('SELECT count(*) FROM close_reservations').fetchone()[0] == 0
    assert account.exposure('dj30_mym_p250') == (1, 2)
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.fill('late', 'base', close.leg_id, 'entry', 1, 100, at), now=at)
    account.observe(BrokerFact.terminal('base', 'cancelled', 2, at), now=at)
    # Refusal is immutable for its occurrence; a new evaluation may close.
    assert account.dispatch(close, occurrence=occurrence, now=at) == result
    broker.queue(BrokerResult('accepted'))
    admitted = account.dispatch(close, occurrence=account.make_occurrence('direct', 'retry'), now=at)
    assert admitted.transport_state == 'accepted'
    assert admitted.quantity == (1 if scoped else 2)


def test_runtime_cancel_and_exit_batch_reports_refusal_and_recovers(tmp_path):
    from test_four_leg_runtime import owner as runtime_owner, binding as runtime_binding
    account = runtime_owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')], protected=True)
    broker = account.synthetic_broker
    actions = [Cancel('dj30_mym_p250', 'base'), replace(intent('exit'), kind='exit', side=Side.SELL, qty=None)]
    class BatchAdapter(Adapter):
        def on_bar(self, bar):
            super().on_bar(bar)
            return [intent()] if len(self.bars) == 1 else [actions[0], replace(actions[1], bar_time=bar.ts)]
    def adapters():
        values = inert_adapters()
        values['dj30_mym_p250'] = BatchAdapter('dj30_mym_p250')
        return values
    registry = adapters()
    runtime = FourLegRuntime(account, registry)
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    runtime.observe_fact(BrokerFact.fill('early', 'base', 'dj30_mym_p250', 'entry', 1, 100, NOW), now=NOW)
    later = NOW + timedelta(minutes=15)
    for leg_id in LEGS:
        results = runtime.on_completed_bar(leg_id, replace(bars()[leg_id], ts=later), now=later)
    assert results[-1].refusal_reason == 'entry_remainder_pending'
    assert [c.kind for c in broker.commands] == ['entry', 'cancel']
    assert ('reject', 'exit', None) in registry['dj30_mym_p250'].events
    restarted = BookAccountOwner.boot(account.path, account.account, binding=runtime_binding(protected=True), synthetic_broker=broker)
    recovered = FourLegRuntime.recover(restarted, adapters())
    assert recovered.adapters['dj30_mym_p250'].events == registry['dj30_mym_p250'].events
    assert restarted.exposure('dj30_mym_p250') == (1, 2)
    assert len(broker.commands) == 2


def test_fully_filled_entry_without_terminal_has_no_live_remainder(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    close = replace(intent('close'), kind='exit', side=Side.SELL, qty=None)
    result = account.dispatch(close, occurrence=account.make_occurrence('direct', 'close'), now=NOW)
    assert result.transport_state == 'accepted' and result.quantity == 3


@pytest.mark.parametrize('filled_add', [0, 1])
def test_close_waits_for_same_leg_add_even_before_cancel_is_requested(tmp_path, filled_add):
    account, broker = owner(tmp_path, [BrokerResult('accepted'), BrokerResult('accepted')])
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('base-fill', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    account.observe(BrokerFact.terminal('base', 'filled', 3, NOW), now=NOW)
    added = account.dispatch(intent('add', kind='add'), occurrence=account.make_occurrence('direct', 'add'), now=NOW)
    assert added.transport_state == 'accepted'
    if filled_add:
        account.observe(BrokerFact.fill('add-fill', 'add', 'dj30_mym_p250', 'add', 1, 100, NOW), now=NOW)
    close = replace(intent('close'), kind='exit', side=Side.SELL, qty=None, scope_fill_ids=('base-fill',))
    assert account.dispatch(close, occurrence=account.make_occurrence('direct', 'close'), now=NOW).refusal_reason == 'entry_remainder_pending'
    assert len(broker.commands) == 2
    at = NOW + timedelta(seconds=1)
    account.observe(BrokerFact.terminal('add', 'cancelled', filled_add, at), now=at)
    broker.queue(BrokerResult('accepted'))
    result = account.dispatch(close, occurrence=account.make_occurrence('direct', 'retry'), now=at)
    assert result.transport_state == 'accepted' and result.quantity == 3


def test_other_leg_live_order_does_not_block_safe_close(tmp_path):
    account, broker = owner(tmp_path, [BrokerResult('accepted')]*3)
    account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    account.observe(BrokerFact.fill('full', 'base', 'dj30_mym_p250', 'entry', 3, 100, NOW), now=NOW)
    other = replace(intent('orb'), leg_id='orb_mnq_v7', qty=1)
    account.dispatch(other, occurrence=account.make_occurrence('direct', 'other'), now=NOW)
    close = replace(intent('close'), kind='flat', side=Side.SELL, qty=None)
    result = account.dispatch(close, occurrence=account.make_occurrence('direct', 'close'), now=NOW)
    assert result.transport_state == 'accepted' and result.quantity == 3
    assert account.exposure('orb_mnq_v7') == (0, 1)


@pytest.mark.parametrize('field', ['risk_dollars', 'cap_allocations', 'lifecycle_tiers'])
@pytest.mark.parametrize('value', [None, [], 'bad', 7, True, 'leg-list'])
def test_nonmapping_runtime_bindings_rejected_before_database_creation(tmp_path, field, value):
    bound = binding()
    bound[field] = list(bound['lifecycle_tiers']) if value == 'leg-list' else value
    path = tmp_path / 'owner.sqlite'
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=bound, synthetic_broker=BootstrapBroker())
    assert not path.exists()


@pytest.mark.parametrize('field,value', [
    ('risk_dollars', []), ('risk_dollars', None), ('risk_dollars', True),
    ('risk_dollars', '100'), ('risk_dollars', float('nan')), ('risk_dollars', -1),
    ('cap_allocations', []), ('cap_allocations', True), ('cap_allocations', 81),
    ('cap_allocations', -1), ('lifecycle_tiers', []), ('lifecycle_tiers', 'invalid'),
])
def test_malformed_mapping_values_rejected_before_retention(tmp_path, field, value):
    bound = binding()
    bound[field]['dj30_mym_p250'] = value
    path = tmp_path / 'owner.sqlite'
    with pytest.raises(AccountOwnerError):
        BookAccountOwner.boot(path, 'synthetic-account', binding=bound, synthetic_broker=BootstrapBroker())
    assert not path.exists()


@pytest.mark.parametrize('risk', [100, Decimal('100'), Fraction(100)])
@pytest.mark.parametrize('mapping_type', [dict, UserDict])
def test_binding_maps_are_snapshotted_before_caller_mutation(tmp_path, risk, mapping_type):
    bound = binding()
    bound['risk_dollars']['dj30_mym_p250'] = risk
    bound = {key: mapping_type(value) if isinstance(value, dict) else value for key, value in bound.items()}
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account',
                                    binding=bound, synthetic_broker=BootstrapBroker([BrokerResult('accepted')]))
    digest = account.status()['runtime_binding_digest']
    bound['risk_dollars']['dj30_mym_p250'] = []
    bound['cap_allocations']['dj30_mym_p250'] = 0
    bound['lifecycle_tiers']['dj30_mym_p250'] = 'RETIRED'
    activate_fresh(account)
    result = account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'entry'), now=NOW)
    assert result.transport_state == 'accepted' and result.quantity == 3
    assert account.status()['runtime_binding_digest'] == digest


def test_empty_sparse_risk_map_keeps_non_striker_entry_valid(tmp_path):
    bound = binding()
    bound['risk_dollars'] = {}
    account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=bound,
                                    synthetic_broker=BootstrapBroker([BrokerResult('accepted')]))
    activate_fresh(account)
    result = account.dispatch(replace(intent('orb'), leg_id='orb_mnq_v7', qty=1),
                              occurrence=account.make_occurrence('direct', 'orb'), now=NOW)
    assert result.transport_state == 'accepted' and result.quantity == 1


@pytest.mark.parametrize('field', ['flatness_basis', 'valuation_basis'])
@pytest.mark.parametrize('value', [[], {}, None, 7, True])
def test_nested_equity_types_are_refused_by_pure_calculation(field, value):
    from test_account_close_calculation import initial_head, calculate, package, S14, NOW14, Refusal
    head = initial_head()
    proposed, sources = package(head, S14, NOW14, scope='record_only')
    if field == 'valuation_basis' and isinstance(value, (list, dict)):
        value = ['close_equity.png'] if isinstance(value, list) else {'file': 'close_equity.png'}
    proposed['equity'][field] = value
    reason = 'flatness_basis' if field == 'flatness_basis' else 'venue_equity_at_close'
    assert calculate(proposed, sources, head) == Refusal(reason)


@pytest.mark.parametrize('unified', [False, True])
@pytest.mark.parametrize('field,value,reason', [
    ('flatness_basis', [], 'flatness_basis'),
    ('flatness_basis', {}, 'flatness_basis'),
    ('valuation_basis', ['close_equity.png'], 'venue_equity_at_close'),
])
def test_signed_nested_equity_refusal_preserves_head_and_owner(tmp_path, unified, field, value, reason):
    from test_book_settlement import Operator, seated, package, S14, NOW14, challenge, submit, CALENDAR
    from test_book_owner_settlement_integration import binding as attached_binding, NOW as boot_time
    from test_book_settlement import seat, b7_seal
    from c1_rail.book_settlement import Refusal, canonical_bytes, sha256_hex
    from settlement_signing import signing_envelope
    operator = Operator()
    account = None
    if unified:
        bound = attached_binding()
        bound['policy_digest'] = 'b' * 64
        account = BookAccountOwner.boot(tmp_path/'owner.sqlite', 'synthetic-account', binding=bound)
        store = account.open_settlement(trusted_keys={operator.key_id: ['record_only']}, now=boot_time)
        head = seat(store, b7_seal())
    else:
        store, head = seated(tmp_path, operator)
    proposed, sources = package(head, S14, NOW14, scope='record_only')
    proposed['equity'][field] = value
    if unified:
        raw = account.issue_settlement_challenge(scope='record_only', target_session_id=None,
            proposed_session_id=S14, package_sha256=sha256_hex(canonical_bytes(proposed)), calendar=CALENDAR, now=NOW14)
        envelope = signing_envelope(raw, signed_at=NOW14)
        incidents = account.incidents
        result = account.submit_settlement(envelope=envelope, signature=operator.sign(envelope),
            key_id=operator.key_id, package=proposed, sources=sources, calendar=CALENDAR, now=NOW14)
        assert account.incidents == incidents
        assert account.permission == 'HALTED'
        assert not getattr(account, '_input_send_suppressed', False)
    else:
        envelope = challenge(store, proposed, target=None, now=NOW14, scope='record_only', permission='HALTED')
        result = submit(store, operator, envelope, proposed, sources, NOW14)
    assert result == Refusal(reason)
    retained_head = store.status()['head']
    assert isinstance(retained_head, dict)
    assert retained_head.get('session_id') == head.session_id
