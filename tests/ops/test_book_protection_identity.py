"""Composite protective evidence rejects identity conflicts before mutation."""
from dataclasses import replace

import pytest

from book_protection_fixtures import ProtectionScenario
from c1_rail.book_account_owner import BookAccountOwner, BrokerFact
from c1_signal_daemon.book_protocol import Bracket
from test_book_account_owner import binding


@pytest.mark.parametrize('collision', ['embedded', 'feedback', 'capacity', 'old_snapshot'])
def test_execution_identity_conflict_is_durable_without_partial_reduction(tmp_path, collision):
    case = ProtectionScenario(tmp_path)
    fill_id = 'execution:0' if collision == 'feedback' else 'base'
    case.enter((fill_id,), bracket=Bracket(stop=98))
    if collision == 'capacity':
        terminal = replace(BrokerFact.terminal('entry-1', 'filled', 3, case.advance()),
                           fact_id='protection-fill:execution')
        case.owner.observe(terminal, now=case.now)
    prior = case.observe()
    event = case.broker.execute_protection('protection:' + fill_id, quantity=1,
                                          price=98, terminal=False, at=case.advance())
    event = replace(event, fact_id='execution')
    if collision == 'embedded':
        event = replace(event, snapshot=replace(event.snapshot, fact_id=event.fact_id))
    elif collision == 'old_snapshot':
        event = replace(event, snapshot=replace(event.snapshot, fact_id=prior.fact_id))
    before = case.owner.all_feedback
    assert case.owner.observe_protection_execution(event, now=case.now) == ()
    assert case.owner.authority == 'INTERVENTION'
    assert case.owner.incidents
    assert case.owner.exposure('dj30_mym_p250') == (3, 0)
    assert case.owner.all_feedback == before
    restarted = BookAccountOwner.boot(case.owner.path, case.owner.account,
                                     binding=binding(), synthetic_broker=case.broker)
    assert restarted.authority == 'INTERVENTION'
    assert restarted.incidents
    assert restarted.exposure('dj30_mym_p250') == (3, 0)
    assert restarted.all_feedback == before


def test_distinct_execution_ids_apply_once_with_replay(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    event = case.broker.execute_protection('protection:base', quantity=1,
                                          price=98, terminal=False, at=case.advance())
    assert len(case.owner.observe_protection_execution(event, now=case.now)) == 1
    before = case.owner.all_feedback
    assert case.owner.observe_protection_execution(event, now=case.now) == ()
    assert case.owner.all_feedback == before
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    assert case.owner.authority == 'NORMAL'
