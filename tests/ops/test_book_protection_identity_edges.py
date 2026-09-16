"""Protective generated feedback shares durable identities with ordinary facts."""
from dataclasses import replace

from book_protection_fixtures import ProtectionScenario
from c1_rail.book_account_owner import BookAccountOwner, BrokerResult
from c1_signal_daemon.book_protocol import Bracket
from test_book_account_owner import binding
from test_book_close_reconciliation import close


def test_pending_close_feedback_identity_conflict_is_durable(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('ordinary', quantity=1), case.occurrence('ordinary'))
    for fact in case.broker.execute_close('ordinary', execution_id='execution:0',
            quantity=1, price=100, terminal=True, at=case.advance()):
        fact = replace(fact, fact_id='execution:0') if fact.kind == 'fill' else fact
        assert case.owner.observe(fact, now=case.now) == ()
    event = case.broker.execute_protection('protection:base', quantity=1,
        price=98, terminal=False, at=case.advance())
    event = replace(event, fact_id='execution')
    before = case.owner.all_feedback
    assert case.owner.observe_protection_execution(event, now=case.now) == ()
    assert case.owner.authority == 'INTERVENTION'
    assert case.owner.incidents
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    assert case.owner.all_feedback == before
    restarted = BookAccountOwner.boot(case.owner.path, case.owner.account,
        binding=binding(), synthetic_broker=case.broker)
    assert restarted.authority == 'INTERVENTION'
    assert restarted.incidents
    assert restarted.exposure('dj30_mym_p250') == (2, 0)
    assert restarted.all_feedback == before


def test_ordinary_close_cannot_claim_protective_feedback_identity(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter(bracket=Bracket(stop=98))
    event = case.broker.execute_protection('protection:base', quantity=1,
        price=98, terminal=False, at=case.advance())
    event = replace(event, fact_id='execution')
    assert len(case.owner.observe_protection_execution(event, now=case.now)) == 1
    case.broker.queue(BrokerResult('accepted'))
    case.dispatch(close('ordinary', quantity=1), case.occurrence('ordinary'))
    facts = case.broker.execute_close('ordinary', execution_id='execution:0',
        quantity=1, price=100, terminal=True, at=case.advance())
    before = case.owner.all_feedback
    assert case.owner.observe(replace(facts[0], fact_id='execution:0'), now=case.now) == ()
    assert case.owner.authority == 'INTERVENTION'
    assert case.owner.incidents
    assert case.owner.exposure('dj30_mym_p250') == (2, 0)
    assert case.owner.all_feedback == before
    restarted = BookAccountOwner.boot(case.owner.path, case.owner.account,
        binding=binding(), synthetic_broker=case.broker)
    assert restarted.authority == 'INTERVENTION'
    assert restarted.incidents
    assert restarted.exposure('dj30_mym_p250') == (2, 0)
    assert restarted.all_feedback == before
