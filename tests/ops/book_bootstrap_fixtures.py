"""Stateful empty providers for fresh-only offline account fixtures."""
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from datetime import datetime, timezone

NOW = datetime(2026, 9, 15, 14, tzinfo=timezone.utc)


class BootstrapBroker(SyntheticProtectionBroker):
    def __init__(self, results=()):
        super().__init__(results, account='synthetic-account', account_epoch='unbound', at=NOW)


def activate_fresh(account, *, now=NOW):
    route = account.synthetic_broker
    if route.account_epoch == 'unbound':
        route.account_epoch = account.make_occurrence('direct', 'fixture-bind').account_epoch
    route.advance(now)
    return account.activate_synthetic(now=now)
