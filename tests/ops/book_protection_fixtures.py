"""Real owner/listener/producer scenarios; no SQL mutation or recovery activation."""
from dataclasses import replace
from datetime import timedelta
from c1_rail.book_account_owner import BrokerResult
from c1_rail.book_protection import ProtectionRead
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from c1_rail.c1_rail_listener import handle_book_action, handle_book_protection
from c1_signal_daemon.book_protocol import BracketAmend
from test_book_account_owner import owner, intent, NOW


class ProtectionScenario:
    def __init__(self, tmp_path):
        self.owner, _ = owner(tmp_path, [])
        self.now = NOW
        occurrence = self.occurrence('bootstrap')
        self.broker = SyntheticProtectionBroker(account=occurrence.account,
            account_epoch=occurrence.account_epoch, at=self.now)
        self.owner.synthetic_broker = self.broker
        self._number = 0

    def occurrence(self, event):
        return self.owner.make_occurrence('direct', event)

    def advance(self):
        self.now += timedelta(milliseconds=100)
        self.broker.advance(self.now)
        return self.now

    def dispatch(self, action, occurrence):
        return handle_book_action(action, self.owner, occurrence=occurrence, now=self.now)

    def enter(self, ids=('base',), *, quantities=None, bracket=None, leg='dj30_mym_p250', kind='entry'):
        self._number += 1
        action = replace(intent('entry-' + str(self._number)), leg_id=leg, bracket=bracket,
                         kind=kind, qty=1 if leg == 'orb_mnq_v7' else 12 if kind == 'add' else 5)
        self.broker.queue(BrokerResult('accepted'))
        result = self.dispatch(action, self.occurrence(action.order_id))
        assert result.transport_state == 'accepted', result
        quantities = quantities or (result.quantity,)
        assert sum(quantities) == result.quantity
        assert len(ids) == len(quantities)
        for fid, qty in zip(ids, quantities):
            fact = self.broker.execute_entry(action.order_id, fill_id=fid, quantity=qty,
                                             price=100, at=self.advance())
            self.owner.observe(fact, now=self.now)
        self.observe()
        return result.quantity

    def observe(self, legs=('dj30_mym_p250', 'orb_mnq_v7')):
        prepared = self.now
        self.advance()
        snapshot = self.broker.read_protection(ProtectionRead(self.occurrence('read'), legs, prepared))
        assert snapshot is not None
        handle_book_protection(snapshot, self.owner, now=self.now)
        return snapshot

    def prepare(self, action, occurrence, *, outcome='accepted', command_count=1):
        result = self.dispatch(action, occurrence)
        assert result.refusal_reason == 'awaiting_evidence', result
        self.advance()
        for _ in range(command_count):
            self.broker.queue(BrokerResult(outcome))
        return self.dispatch(action, occurrence)

    def confirm(self, result, *, outcome='applied'):
        commands = [c for c in self.broker.commands if c.operation_id.startswith(result.operation_id + ':')]
        assert commands, result
        for command in commands:
            self.broker.apply(command.operation_id, outcome=outcome, at=self.advance())
        self.observe()

    def establish(self, fid, bracket, *, leg='dj30_mym_p250'):
        result = self.prepare(BracketAmend(leg, bracket, (fid,)), self.occurrence('establish:' + fid))
        assert result.transport_state == 'accepted', result
        self.confirm(result)
        assert self.protection(fid).observed is not None
        return result

    def protection(self, fid):
        return next(row for row in self.owner.protection_owners if row.entry_fill_id == fid)

    @property
    def protection_commands(self):
        return tuple(command for command in self.broker.commands if command.protection_change is not None)
