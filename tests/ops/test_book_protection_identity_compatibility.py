"""Identities may overlap across journals when ingress does not write both."""
from dataclasses import replace

from book_protection_fixtures import ProtectionScenario
from c1_rail.book_account_owner import BrokerFact, BrokerResult
from test_book_close_reconciliation import close


def test_close_terminal_can_share_capacity_key_without_claiming_it(tmp_path):
    case = ProtectionScenario(tmp_path)
    case.enter()
    case.broker.queue(BrokerResult('accepted'))
    result = case.dispatch(close('ordinary', quantity=1), case.occurrence('ordinary'))
    assert result.transport_state == 'accepted'
    # Entry 'base' owns capacity key 'fill:base'. A close terminal writes only
    # broker facts/feedback, so its distinct fact identity can use that string.
    fact = replace(BrokerFact.terminal('ordinary', 'cancelled', 0, case.advance()),
                   fact_id='fill:base')
    events = case.owner.observe(fact, now=case.now)
    assert len(events) == 1
    assert events[0].event == 'cancel'
    assert case.owner.authority == 'NORMAL'
    assert case.owner.exposure('dj30_mym_p250') == (3, 0)
    before = case.owner.all_feedback
    assert case.owner.observe(fact, now=case.now) == ()
    assert case.owner.all_feedback == before
    assert case.owner.authority == 'NORMAL'
