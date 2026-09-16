"""Explicit direct-harness provenance for legacy owner regression scenarios."""
from datetime import timedelta
from c1_rail.book_account_owner import BookAccountOwner, BrokerResult
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from test_book_account_owner import NOW, binding, intent


def bare_protection_owner(tmp_path):
    route = SyntheticProtectionBroker(account='synthetic-account', account_epoch='unbound', at=NOW)
    account = BookAccountOwner.boot(tmp_path / 'owner.sqlite', 'synthetic-account', binding=binding(), synthetic_broker=route)
    route.account_epoch = account.make_occurrence('direct', 'fixture-bind').account_epoch
    account.activate_synthetic(now=NOW)
    route.queue(BrokerResult('accepted'))
    result = account.dispatch(intent(), occurrence=account.make_occurrence('direct', 'fixture-entry'), now=NOW)
    fact = route.execute_entry(result.operation_id, fill_id='base-fill', quantity=result.quantity, price=100, at=NOW)
    account.observe(fact, now=NOW)
    return account, route


def prepare_protection(account, route, action, event_id, *, now=NOW):
    event = account.make_occurrence('direct', event_id)
    prepared = account.dispatch(action, occurrence=event, now=now)
    assert prepared.refusal_reason == 'awaiting_evidence'
    later = now + timedelta(seconds=1)
    route.advance(later)
    return account.dispatch(action, occurrence=event, now=later)
