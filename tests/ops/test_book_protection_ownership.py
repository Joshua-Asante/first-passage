"""Protection ownership through real occurrence, listener, broker and journal paths."""
from dataclasses import replace
import pytest
from c1_signal_daemon.book_protocol import Bracket, BracketAmend, OrderIntent, Side
from c1_rail.book_account_owner import BrokerResult
from book_protection_fixtures import ProtectionScenario


@pytest.fixture
def scenario(tmp_path):
    return ProtectionScenario(tmp_path)


@pytest.mark.parametrize('foreign', [False, True])
def test_invalid_final_target_prevents_every_child_send(scenario, foreign):
    scenario.enter(('orb',), leg='orb_mnq_v7')
    target = 'unknown'
    if foreign:
        scenario.enter(('mym',))
        target = 'mym'
    before = len(scenario.broker.commands)
    result = scenario.dispatch(BracketAmend('orb_mnq_v7', Bracket(stop=98), ('orb', target)),
                               scenario.occurrence('mixed'))
    assert result.refusal_reason == 'invalid_protection_target'
    assert len(scenario.broker.commands) == before
    assert scenario.owner.authority == 'INTERVENTION'
    assert scenario.owner.incidents
    assert scenario.protection('orb').observed is None
    assert scenario.protection('orb').pending_operation is None


def test_bare_attach_waits_for_actual_application(scenario):
    quantity = scenario.enter()
    result = scenario.prepare(BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base',)), scenario.occurrence('attach'))
    assert result.transport_state == 'accepted'
    assert scenario.protection('base').observed is None
    assert scenario.protection('base').pending_operation is not None
    command, = scenario.protection_commands
    assert command.protection_change.target.primitive == 'attach'
    assert command.protection_change.target.quantity == quantity == 3
    scenario.confirm(result)
    assert scenario.protection('base').observed == Bracket(stop=98)
    assert scenario.protection('base').pending_operation is None


def test_same_receiver_levels_complete_noop_without_send(scenario):
    scenario.enter(bracket=Bracket(stop=98.1))
    before = len(scenario.broker.commands)
    result = scenario.prepare(BracketAmend('dj30_mym_p250', Bracket(stop=98.9), ('base',)),
                              scenario.occurrence('same-tick'), command_count=0)
    assert result.refusal_reason == 'unchanged_protection'
    assert len(scenario.broker.commands) == before
    assert scenario.protection('base').observed == Bracket(stop=98)
    assert scenario.protection('base').pending_operation is None


def test_fixed_stop_amendment_preserves_active_trail_anchor(scenario):
    bracket = Bracket(stop=90, trail_activation_ticks=2, trail_offset_ticks=4)
    scenario.enter(bracket=bracket)
    scenario.broker.mark_price('dj30_mym_p250', 103, at=scenario.advance())
    scenario.observe()
    assert scenario.protection('base').trail_anchor == 103
    result = scenario.prepare(BracketAmend('dj30_mym_p250', replace(bracket, stop=91), ('base',)), scenario.occurrence('raise-stop'))
    command, = scenario.protection_commands
    assert command.protection_change.changed_components == ('stop',)
    scenario.confirm(result)
    observed = scenario.protection('base')
    assert observed.observed == replace(bracket, stop=91)
    assert observed.trail_active and observed.trail_anchor == 103


def test_fifo_consumed_owner_cannot_resurrect_while_live_original_owner_amends(scenario):
    bracket = Bracket(stop=90, trail_activation_ticks=2, trail_offset_ticks=4)
    scenario.enter(('old', 'new'), quantities=(1, 2), bracket=bracket)
    scenario.broker.mark_price('dj30_mym_p250', 103, at=scenario.advance())
    scenario.observe()
    event = scenario.broker.execute_protection('protection:new', quantity=2, price=99,
                                               terminal=True, at=scenario.advance())
    feedback = scenario.owner.observe_protection_execution(event, now=scenario.now)
    assert tuple((e.fill.entry_fill_id, e.fill.qty) for e in feedback) == (('old', 1), ('new', 1))
    assert scenario.owner.exposure('dj30_mym_p250') == (1, 0)
    assert scenario.protection('new').consumed
    assert scenario.protection('old').quantity == 1
    assert scenario.protection('old').trail_anchor == 103
    before = len(scenario.broker.commands)
    refused = scenario.dispatch(BracketAmend('dj30_mym_p250', bracket, ('new',)), scenario.occurrence('resurrection'))
    assert refused.refusal_reason == 'consumed_protection'
    assert len(scenario.broker.commands) == before
    result = scenario.prepare(BracketAmend('dj30_mym_p250', replace(bracket, stop=91), ('old',)), scenario.occurrence('surviving-owner'))
    assert result.transport_state == 'accepted'
    scenario.confirm(result)
    assert scenario.protection('old').observed.stop == 91
    assert scenario.protection('old').trail_anchor == 103
    assert scenario.owner.observe_protection_execution(event, now=scenario.now) == ()
    assert scenario.owner.exposure('dj30_mym_p250') == (1, 0)


def test_rejected_amendment_intact_old_evidence_allows_new_occurrence_only(scenario):
    scenario.enter(bracket=Bracket(stop=98))
    action = BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base',))
    occurrence = scenario.occurrence('first-change')
    rejected = scenario.prepare(action, occurrence, outcome='rejected')
    assert rejected.transport_state == 'rejected'
    scenario.observe()
    assert scenario.owner.authority == 'NORMAL'
    assert scenario.protection('base').observed == Bracket(stop=98)
    assert scenario.protection('base').pending_operation is None
    before = len(scenario.protection_commands)
    assert scenario.dispatch(action, occurrence).operation_id == rejected.operation_id
    assert len(scenario.protection_commands) == before
    retry = scenario.prepare(action, scenario.occurrence('new-change'))
    assert retry.operation_id != rejected.operation_id
    assert retry.transport_state == 'accepted'
    scenario.confirm(retry)
    assert scenario.protection('base').observed == Bracket(stop=99)


def test_redelivery_cannot_expand_retained_unscoped_targets(scenario):
    scenario.enter(('original',))
    occurrence = scenario.occurrence('unscoped')
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98))
    original = scenario.prepare(action, occurrence)
    scenario.confirm(original)
    scenario.enter(('later',), kind='add')
    before = len(scenario.protection_commands)
    replay = scenario.dispatch(action, occurrence)
    assert replay.operation_id == original.operation_id
    assert len(scenario.protection_commands) == before == 1
    assert scenario.protection_commands[0].protection_change.target.entry_fill_id == 'original'
    assert scenario.protection('later').observed is None


def test_scoped_explicit_close_reduces_selected_lot_and_snapshot_tombstones_owner(scenario):
    scenario.enter(('old', 'new'), quantities=(1, 2), bracket=Bracket(stop=98))
    action = OrderIntent('close-new', 'dj30_mym_p250', 'exit', Side.SELL, 2,
                         scope_fill_ids=('new',), bar_time=scenario.now)
    scenario.broker.queue(BrokerResult('accepted'))
    result = scenario.dispatch(action, scenario.occurrence('close-new'))
    assert result.transport_state == 'accepted'
    assert scenario.owner.exposure('dj30_mym_p250')[0] == 3
    scenario.broker.mark_price('dj30_mym_p250', 101, at=scenario.advance())
    scenario.broker.apply(result.operation_id, outcome='applied', at=scenario.advance())
    fact, = scenario.broker.result_facts(result.operation_id)
    assert (fact.quantity, fact.entry_execution_id) == (2, 'new')
    scenario.owner.observe(fact, now=scenario.now)
    assert scenario.owner.exposure('dj30_mym_p250') == (1, 0)
    assert not scenario.protection('new').consumed
    scenario.observe()
    assert scenario.protection('new').consumed
    assert scenario.protection('old').quantity == 1
    assert scenario.protection('old').observed == Bracket(stop=98)
    assert scenario.owner.authority == 'NORMAL'


def test_nonterminal_protective_execution_retains_remaining_order_and_replays_once(scenario):
    scenario.enter(bracket=Bracket(stop=98))
    event = scenario.broker.execute_protection('protection:base', quantity=1, price=98,
                                               terminal=False, at=scenario.advance())
    feedback = scenario.owner.observe_protection_execution(event, now=scenario.now)
    assert len(feedback) == 1 and feedback[0].fill.qty == 1
    assert scenario.owner.exposure('dj30_mym_p250') == (2, 0)
    assert not scenario.protection('base').consumed
    assert scenario.protection('base').quantity == 2
    assert scenario.owner.observe_protection_execution(event, now=scenario.now) == ()
    assert scenario.owner.exposure('dj30_mym_p250') == (2, 0)
    terminal = scenario.broker.execute_protection('protection:base', quantity=2, price=98,
                                                  terminal=True, at=scenario.advance())
    assert len(scenario.owner.observe_protection_execution(terminal, now=scenario.now)) == 1
    assert scenario.owner.exposure('dj30_mym_p250') == (0, 0)
    assert scenario.protection('base').consumed


@pytest.mark.parametrize('outcome', ['rejected', 'unknown'])
def test_first_attachment_failure_fences_immediately_and_retains_exposure(scenario, outcome):
    scenario.enter()
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98), ('base',))
    occurrence = scenario.occurrence('attach-failure')
    result = scenario.prepare(action, occurrence, outcome=outcome)
    assert result.transport_state == outcome
    assert scenario.owner.authority == 'INTERVENTION'
    assert scenario.owner.incidents
    assert scenario.owner.exposure('dj30_mym_p250') == (3, 0)
    assert scenario.protection('base').observed is None
    assert scenario.protection('base').pending_operation is not None
    before = len(scenario.broker.commands)
    scenario.dispatch(action, occurrence)
    scenario.dispatch(action, scenario.occurrence('different-attach'))
    assert len(scenario.broker.commands) == before


def test_removed_protection_cannot_reappear_under_removal_operation(scenario):
    scenario.enter(bracket=Bracket(stop=98))
    original = scenario.observe().orders[0]
    removal = scenario.prepare(BracketAmend('dj30_mym_p250', Bracket(), ('base',)), scenario.occurrence('remove'))
    scenario.confirm(removal)
    assert scenario.protection('base').observed is None
    snapshot = scenario.observe()
    phantom = replace(original, operation_id=scenario.protection_commands[-1].operation_id,
                      revision=original.revision + 1)
    fault = replace(snapshot, fact_id='phantom-after-removal', sequence=snapshot.sequence + 1,
                    orders=(phantom,))
    scenario.owner.observe_protection(fault, now=scenario.now)
    assert scenario.owner.authority == 'INTERVENTION'
    assert scenario.protection('base').observed is None


def test_multi_owner_attach_retains_first_applied_effect_when_later_child_rejected(scenario):
    scenario.enter(('first', 'second'), quantities=(1, 2))
    action = BracketAmend('dj30_mym_p250', Bracket(stop=98))
    occurrence = scenario.occurrence('two-attaches')
    assert scenario.dispatch(action, occurrence).refusal_reason == 'awaiting_evidence'
    scenario.advance()
    scenario.broker.queue(BrokerResult('accepted'))
    scenario.broker.queue(BrokerResult('rejected'))
    result = scenario.dispatch(action, occurrence)
    assert result.transport_state == 'rejected'
    first, second = scenario.protection_commands
    assert scenario.owner.authority == 'INTERVENTION'
    scenario.broker.apply(first.operation_id, outcome='applied', at=scenario.advance())
    scenario.observe()
    assert scenario.protection('first').observed == Bracket(stop=98)
    assert scenario.protection('first').pending_operation is None
    assert scenario.protection('second').observed is None
    assert scenario.protection('second').pending_operation == second.operation_id
    assert scenario.owner.authority == 'INTERVENTION'


def test_transport_exception_after_receipt_is_unknown_and_late_evidence_cannot_resume(scenario, monkeypatch):
    scenario.enter(bracket=Bracket(stop=98))
    action = BracketAmend('dj30_mym_p250', Bracket(stop=99), ('base',))
    occurrence = scenario.occurrence('broken-transport')
    assert scenario.dispatch(action, occurrence).refusal_reason == 'awaiting_evidence'
    scenario.advance()
    scenario.broker.queue(BrokerResult('accepted'))
    original_send = scenario.broker.send

    def receipt_then_disconnect(command):
        original_send(command)
        raise OSError('synthetic transport disconnected after receipt')

    monkeypatch.setattr(scenario.broker, 'send', receipt_then_disconnect)
    result = scenario.dispatch(action, occurrence)
    assert result.transport_state == 'unknown'
    assert scenario.owner.authority == 'INTERVENTION'
    command, = scenario.protection_commands
    assert scenario.protection('base').observed == Bracket(stop=98)
    scenario.broker.apply(command.operation_id, outcome='applied', at=scenario.advance())
    scenario.observe()
    assert scenario.protection('base').observed == Bracket(stop=99)
    assert scenario.owner.authority == 'INTERVENTION'
    before = len(scenario.broker.commands)
    scenario.dispatch(action, occurrence)
    assert len(scenario.broker.commands) == before
