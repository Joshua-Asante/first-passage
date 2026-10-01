"""Account-fence classification on the synthetic seam (§59 Ruling 7(b); H4 checkpoint F).

States: (i) known working on fresh, qualifying order-level evidence; (ii) stale;
(iii) unknown dispatch; (iv) terminal. Evidence is stale when its age at
evaluation is one bar period or more (operator-confirmed inclusive boundary).

Every acquisition here is a labelled synthetic test input. None of it is, or
stands in for, the real order-level evidence producer (T09), route
integration, or the rev9 halt for ordinary unknowns; those remain owed.
"""
from dataclasses import replace
from datetime import timedelta

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult
from c1_rail.book_policy import leg
from c1_rail.book_protection import ProtectionRead
from c1_signal_daemon.book_protocol import BAR_PERIOD, Bracket, BracketAmend, FillTiming, OrderIntent, Side
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh
from test_book_account_owner import NOW, SESSION, binding, intent


MICROSECOND = timedelta(microseconds=1)
STRIKER = 'MYM1!'
ORB = 'MNQ1!'


class Route(BootstrapBroker):
    """Synthetic route: accepted unless a different outcome is queued first."""

    def send(self, command):
        if not self._results:
            self.queue(BrokerResult('accepted'))
        return super().send(command)


class Account:
    def __init__(self, tmp_path, **overrides):
        bound = binding()
        bound.update(valid_until=NOW + timedelta(hours=2), max_evidence_age=timedelta(hours=2))
        bound.update(overrides)
        self.broker = Route([])
        self.owner = BookAccountOwner.boot(tmp_path / 'owner.sqlite', 'synthetic-account',
                                           binding=bound, synthetic_broker=self.broker)
        activate_fresh(self.owner)
        self.now = NOW

    def at(self, when):
        self.now = when
        self.broker.advance(when)
        return when

    def tick(self):
        return self.at(self.now + timedelta(milliseconds=100))

    def send(self, action, *, outcome='accepted'):
        if outcome != 'accepted':
            self.broker.queue(BrokerResult(outcome))
        return self.owner.dispatch(action, occurrence=self.owner.make_occurrence('direct', action.order_id),
                                   now=self.now)

    def evidence(self, symbol, rows, *, at=None, read=None, complete=True, position_only=False,
                 observed=None):
        from c1_rail.book_account_owner import SyntheticOrderEvidence
        at = self.now if at is None else at
        if read is None:
            read = self.owner.prepare_synthetic_order_read(symbol, now=at - timedelta(seconds=1))
        return self.owner.observe_synthetic_order_evidence(
            SyntheticOrderEvidence(read.read_id, symbol, at, complete, position_only, tuple(rows)),
            now=at if observed is None else observed)

    def classify(self, identity, at):
        return self.owner.request_classification(now=at)[identity]

    def fenced(self, at):
        with self.owner._transaction() as db:
            return self.owner._ordinary_unknown_orders_db(db, now=at)


def working(result, action, remaining, **changes):
    from c1_rail.book_account_owner import SyntheticWorkingOrder
    row = SyntheticWorkingOrder(result.operation_id, result.attempt_id, action.leg_id,
                                leg(action.leg_id).order_symbol, action.kind, remaining)
    return replace(row, **changes)


def other_leg(order_id, at):
    return replace(intent(order_id), leg_id='orb_mnq_v7', qty=1, bar_time=at)


def resting_entry(acct):
    """A Striker entry sent at NOW and accepted; 3 contracts rest unfilled."""
    action = intent()
    result = acct.send(action)
    assert result.transport_state == 'accepted' and result.quantity == 3
    return action, result


def evidenced_every_bar(acct, action, result, until):
    """Fresh qualifying order-level acquisitions on every bar up to ``until``."""
    at = NOW + timedelta(minutes=10)
    while at <= until:
        assert acct.evidence(STRIKER, [working(result, action, 3)], at=acct.at(at)) == 'qualified'
        at += timedelta(minutes=10)


# --- Loosening-amend fixture: an ORB lot with a confirmed protective stop at 98.

def protected_orb_lot(acct):
    action = replace(intent('orb-entry'), leg_id='orb_mnq_v7', qty=1, bracket=Bracket(stop=98))
    assert acct.send(action).transport_state == 'accepted'
    at = acct.tick()
    acct.owner.observe(acct.broker.execute_entry('orb-entry', fill_id='orb-fill', quantity=1,
                                                 price=100, at=at), now=at)
    acct.owner.observe(BrokerFact.terminal('orb-entry', 'filled', 1, at), now=at)
    prepared = acct.now
    acct.tick()
    snapshot = acct.broker.read_protection(ProtectionRead(
        acct.owner.make_occurrence('direct', 'protection-read'), ('orb_mnq_v7',), prepared))
    acct.owner.observe_protection(snapshot, now=acct.now)
    assert acct.owner.authority == 'NORMAL', acct.owner.incidents


def loosen(acct, at):
    """Loosen the ORB stop 98 -> 97; the admission decision is taken exactly at ``at``."""
    action = BracketAmend('orb_mnq_v7', Bracket(stop=97), ('orb-fill',))
    occurrence = acct.owner.make_occurrence('direct', 'loosen:' + at.isoformat())
    acct.at(at - timedelta(milliseconds=100))
    first = acct.owner.dispatch(action, occurrence=occurrence, now=acct.now)
    assert first.refusal_reason == 'awaiting_evidence', first
    acct.at(at)
    return acct.owner.dispatch(action, occurrence=occurrence, now=at)


# --- Takeover fixture. Protected Aegis on WATCH-1 needs 10 micro. Striker holds
# 20 filled + 50 add micro and ORB 1, so only ORB is displaced: Striker is a
# non-displaced leg whose add request can be in any fence state.

def takeover_account(tmp_path):
    tiers = {**binding()['lifecycle_tiers'], 'aegis_6j': 'WATCH-1'}
    acct = Account(tmp_path, lifecycle_tiers=tiers, risk_dollars={'dj30_mym_p250': 600})
    base = intent('s-base', qty=20)
    assert acct.send(base).quantity == 20
    at = acct.tick()
    acct.owner.observe(acct.broker.execute_entry('s-base', fill_id='s-fill', quantity=20,
                                                 price=100, at=at), now=at)
    acct.owner.observe(BrokerFact.terminal('s-base', 'filled', 20, at), now=at)
    return acct


def striker_add(acct):
    action = replace(intent('s-add', kind='add', qty=50), bar_time=acct.now)
    result = acct.send(action)
    assert result.transport_state == 'accepted' and result.quantity == 50, result
    return action, result


def displaced_orb_entry(acct):
    action = replace(intent('orb-1'), leg_id='orb_mnq_v7', qty=1, bar_time=acct.now)
    result = acct.send(action)
    assert result.transport_state == 'accepted', result
    acct.broker.apply('orb-1', outcome='applied', at=acct.tick())
    return action, result


def aegis_takeover(acct):
    root = OrderIntent('aegis-root', 'aegis_6j', 'entry', Side.SELL, 8, timing=FillTiming.THIS_CLOSE,
                       stop_dist_pts=1, bar_time=acct.now)
    result = acct.owner.dispatch(root, occurrence=acct.owner.make_occurrence('direct', 'root'), now=acct.now)
    assert result.refusal_reason == 'takeover_pending', result
    with acct.owner._transaction() as db:
        assert acct.owner._takeover_plan_db(db, 'aegis-root')['displaced'] == ['orb_mnq_v7']


def poll_takeover(acct):
    read = acct.owner.prepare_takeover_inventory(now=acct.now)
    acct.tick()
    acct.owner.observe_takeover_inventory(acct.broker.read_inventory(read), now=acct.now)
    return acct.owner.advance_takeover(now=acct.now)


def cancel_displaced(acct):
    cancel = next(c for c in acct.broker.commands if c.kind == 'cancel')
    acct.broker.apply_cancel(cancel.operation_id, at=acct.tick())


def resume_root(acct):
    results = acct.owner.resume_takeover(now=acct.now)
    return next(r for r in results if r.operation_id == 'aegis-root')


def complete_takeover(acct):
    poll_takeover(acct)
    cancel_displaced(acct)
    _controls, done = poll_takeover(acct)
    assert done, acct.owner.incidents
    return resume_root(acct)


def aegis_sent(acct):
    return any(c.operation_id == 'aegis-root' for c in acct.broker.commands)


# --- Case 1: (b1) known working; retain reservation; no block because old.

def test_fresh_working_entry_does_not_block_other_leg_admission(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    evidenced_every_bar(acct, action, result, NOW + timedelta(minutes=20))
    at = acct.at(NOW + timedelta(minutes=25))
    assert acct.classify('base', at) == 'known_working'
    admitted = acct.send(other_leg('other', at))
    assert admitted.transport_state == 'accepted', admitted
    assert acct.owner.exposure('dj30_mym_p250') == (0, 3)


def test_fresh_working_entry_does_not_block_other_leg_loosening_amend(tmp_path):
    acct = Account(tmp_path)
    protected_orb_lot(acct)
    acct.at(NOW + timedelta(seconds=2))
    action = replace(intent(), bar_time=acct.now)
    result = acct.send(action)
    assert result.transport_state == 'accepted'
    evidenced_every_bar(acct, action, result, NOW + timedelta(minutes=20))
    at = NOW + timedelta(minutes=25)
    loosened = loosen(acct, at)
    assert acct.classify('base', at) == 'known_working'
    assert loosened.transport_state == 'accepted', loosened
    assert acct.broker.commands[-1].kind == 'bracketamend'


def test_fresh_working_entry_on_non_displaced_leg_does_not_block_takeover(tmp_path):
    acct = takeover_account(tmp_path)
    add, add_result = striker_add(acct)
    for minutes in (10, 20):
        assert acct.evidence(STRIKER, [working(add_result, add, 50)],
                             at=acct.at(NOW + timedelta(minutes=minutes))) == 'qualified'
    acct.at(NOW + timedelta(minutes=24))
    displaced_orb_entry(acct)
    aegis_takeover(acct)
    root = complete_takeover(acct)
    assert acct.classify('s-add', acct.now) == 'known_working'
    assert root.transport_state == 'accepted', root
    assert aegis_sent(acct)


def test_fresh_working_entry_retains_capacity_reservation(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    evidenced_every_bar(acct, action, result, NOW + timedelta(minutes=40))
    at = NOW + timedelta(minutes=45)
    assert acct.classify('base', at) == 'known_working'
    assert 'base' not in acct.fenced(at)
    assert acct.owner.exposure('dj30_mym_p250') == (0, 3)
    assert acct.owner.unresolved_attempts == (result.attempt_id,)


# --- Case 2: (b2) stale evidence blocks; (b1) fresh evidence reclassifies.

@pytest.mark.parametrize('consumer', ['admission', 'loosening', 'takeover'])
def test_stale_evidence_blocks_admission_loosening_and_takeover(tmp_path, consumer):
    if consumer == 'takeover':
        acct = takeover_account(tmp_path)
        add, add_result = striker_add(acct)
        last = acct.at(NOW + timedelta(minutes=5))
        assert acct.evidence(STRIKER, [working(add_result, add, 50)], at=last) == 'qualified'
        acct.at(NOW + timedelta(minutes=15))
        displaced_orb_entry(acct)
        aegis_takeover(acct)
        acct.at(last + BAR_PERIOD)
        assert acct.classify('s-add', acct.now) == 'stale'
        root = complete_takeover(acct)
        assert root.refusal_reason == 'unknown_order', root
        assert not aegis_sent(acct)
        return
    acct = Account(tmp_path)
    if consumer == 'loosening':
        protected_orb_lot(acct)
    acct.at(NOW + timedelta(seconds=2))
    action = replace(intent(), bar_time=acct.now)
    result = acct.send(action)
    last = acct.at(NOW + timedelta(minutes=10))
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=last) == 'qualified'
    at = last + BAR_PERIOD
    if consumer == 'admission':
        refused = acct.send(other_leg('other', acct.at(at)))
        assert refused.refusal_reason == 'unknown_order'
    else:
        refused = loosen(acct, at)
        assert refused.refusal_reason == 'risk_add_not_authorized'
    assert acct.classify('base', at) == 'stale'
    assert acct.fenced(at) == ('base',)


def test_fresh_working_evidence_after_staleness_reclassifies_known_working(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    first = acct.at(NOW + timedelta(minutes=5))
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=first) == 'qualified'
    stale = acct.at(first + BAR_PERIOD + timedelta(minutes=1))
    assert acct.classify('base', stale) == 'stale'
    assert acct.fenced(stale) == ('base',)
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=acct.tick()) == 'qualified'
    assert acct.classify('base', acct.now) == 'known_working'
    assert acct.fenced(acct.now) == ()


def test_terminal_resolves_stale_request(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    assert acct.evidence(STRIKER, [working(result, action, 3)],
                         at=acct.at(NOW + timedelta(minutes=5))) == 'qualified'
    at = acct.at(NOW + timedelta(minutes=25))
    assert acct.fenced(at) == ('base',)
    acct.owner.observe(BrokerFact.terminal('base', 'cancelled', 0, at), now=at)
    assert acct.fenced(at) == ()
    assert acct.owner.exposure('dj30_mym_p250') == (0, 0)


# --- Case 3: (b2); the S1 cut is unchanged for an accepted, never-evidenced request.

def test_accepted_request_never_evidenced_blocks_from_one_bar(tmp_path):
    acct = Account(tmp_path)
    resting_entry(acct)
    assert acct.fenced(NOW + BAR_PERIOD - MICROSECOND) == ()
    assert acct.fenced(NOW + BAR_PERIOD) == ('base',)
    refused = acct.send(other_leg('other', acct.at(NOW + BAR_PERIOD)))
    assert refused.refusal_reason == 'unknown_order'


# --- Case 4: only qualifying acquisitions (evidence currency; E1-E3).

@pytest.mark.parametrize('evidence_case', [
    'position_only', 'incomplete', 'unfenced', 'read_before_dispatch',
    'as_of_equal_preparation', 'as_of_before_preparation', 'one_bar_old', 'observed_late',
])
def test_nonqualifying_evidence_never_makes_request_known_working(tmp_path, evidence_case):
    acct = Account(tmp_path)
    if evidence_case == 'read_before_dispatch':
        early = acct.owner.prepare_synthetic_order_read(STRIKER, now=NOW - timedelta(seconds=1))
    action, result = resting_entry(acct)
    row = working(result, action, 3)
    at = acct.at(NOW + timedelta(minutes=1))
    evaluate = at + timedelta(minutes=1)
    if evidence_case == 'position_only':
        assert acct.evidence(STRIKER, [row], at=at, position_only=True) != 'qualified'
    elif evidence_case == 'incomplete':
        assert acct.evidence(STRIKER, [row], at=at, complete=False) != 'qualified'
    elif evidence_case == 'unfenced':
        from c1_rail.book_account_owner import SyntheticOrderEvidence
        disposition = acct.owner.observe_synthetic_order_evidence(
            SyntheticOrderEvidence('never-issued', STRIKER, at, True, False, (row,)), now=at)
        assert disposition != 'qualified'
    elif evidence_case == 'read_before_dispatch':
        acct.evidence(STRIKER, [row], at=at, read=early)
    elif evidence_case == 'as_of_equal_preparation':
        read = acct.owner.prepare_synthetic_order_read(STRIKER, now=NOW - timedelta(seconds=1))
        acct.evidence(STRIKER, [row], at=NOW, read=read)
    elif evidence_case == 'as_of_before_preparation':
        read = acct.owner.prepare_synthetic_order_read(STRIKER, now=NOW - timedelta(seconds=2))
        acct.evidence(STRIKER, [row], at=NOW - timedelta(seconds=1), read=read)
    elif evidence_case == 'one_bar_old':
        assert acct.evidence(STRIKER, [row], at=at) == 'qualified'
        assert acct.classify('base', at + BAR_PERIOD - MICROSECOND) == 'known_working'
        evaluate = at + BAR_PERIOD
    elif evidence_case == 'observed_late':
        assert acct.evidence(STRIKER, [row], at=at, observed=at + timedelta(seconds=31)) != 'qualified'
    assert acct.classify('base', evaluate) != 'known_working'
    past_first_bar = max(evaluate, NOW + BAR_PERIOD)
    assert acct.classify('base', past_first_bar) == 'stale'
    assert acct.fenced(past_first_bar) == ('base',)


@pytest.mark.parametrize('mismatch', [
    'other_attempt', 'other_operation', 'other_leg', 'row_symbol', 'acquisition_symbol',
    'remainder_high', 'remainder_after_fill',
])
def test_mismatched_identity_symbol_or_remainder_is_not_known_working(tmp_path, mismatch):
    """Not (i). E2/E3 quarantine or attended resolution of these reads is not
    implemented by the account owner; it is still owed with the real producer."""
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    row = working(result, action, 3)
    symbol = STRIKER
    if mismatch == 'other_attempt':
        row = replace(row, attempt_id='other-attempt')
    elif mismatch == 'other_operation':
        row = replace(row, operation_id='other-order')
    elif mismatch == 'other_leg':
        row = replace(row, leg_id='orb_mnq_v7')
    elif mismatch == 'row_symbol':
        row = replace(row, order_symbol=ORB)
    elif mismatch == 'acquisition_symbol':
        symbol = ORB
    elif mismatch == 'remainder_high':
        row = replace(row, remaining=4)
    elif mismatch == 'remainder_after_fill':
        at = acct.at(NOW + timedelta(minutes=1))
        acct.owner.observe(acct.broker.execute_entry('base', fill_id='partial', quantity=1,
                                                     price=100, at=at), now=at)
    at = acct.at(NOW + timedelta(minutes=19))
    acct.evidence(symbol, [row], at=at)
    evaluate = NOW + timedelta(minutes=20)
    assert acct.classify('base', evaluate) == 'stale'
    assert acct.fenced(evaluate) == ('base',)


# --- Case 5: (b1) "working or partially filled".

def test_partial_fill_with_fresh_working_remainder_is_known_working(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    at = acct.at(NOW + timedelta(minutes=1))
    acct.owner.observe(acct.broker.execute_entry('base', fill_id='partial', quantity=1,
                                                 price=100, at=at), now=at)
    assert acct.owner.exposure('dj30_mym_p250') == (1, 2)
    assert acct.evidence(STRIKER, [working(result, action, 2)],
                         at=acct.at(NOW + timedelta(minutes=19))) == 'qualified'
    at = acct.at(NOW + timedelta(minutes=20))
    assert acct.classify('base', at) == 'known_working'
    assert acct.send(other_leg('other', at)).transport_state == 'accepted'


# --- Case 6: (b3) unknown dispatch blocks immediately; terminal-only resolution.

def test_unknown_dispatch_blocks_immediately(tmp_path):
    acct = Account(tmp_path)
    result = acct.send(intent(), outcome='unknown')
    assert result.transport_state == 'unknown'
    assert acct.fenced(NOW) == ('base',)
    refused = acct.send(other_leg('other', acct.at(NOW + timedelta(seconds=1))))
    # CC-3: the unknown halts into INTERVENTION at once, ahead of the ordinary unknown fence.
    assert refused.refusal_reason == 'intervention_fence'
    assert (acct.owner.permission, acct.owner.authority) == ('HALTED', 'INTERVENTION')


@pytest.mark.parametrize('input_case', [
    'other_order_working', 'position_only', 'equal_time_terminal', 'positive_lookup_same_order',
])
def test_unknown_dispatch_clears_only_on_accepted_postdating_terminal(tmp_path, input_case):
    acct = Account(tmp_path)
    action = intent()
    result = acct.send(action, outcome='unknown')
    if input_case == 'equal_time_terminal':
        acct.owner.observe(BrokerFact.terminal('base', 'cancelled', 0, NOW), now=NOW)
    else:
        at = acct.at(NOW + timedelta(minutes=1))
        if input_case == 'other_order_working':
            acct.evidence(STRIKER, [working(result, action, 3, operation_id='other-order')], at=at)
        elif input_case == 'position_only':
            acct.evidence(STRIKER, [], at=at, position_only=True)
        else:  # a positive working lookup of the same order stays held (UB-7)
            assert acct.evidence(STRIKER, [working(result, action, 3)], at=at) == 'qualified'
    at = acct.at(NOW + timedelta(minutes=2))
    assert acct.fenced(at) == ('base',)
    assert acct.send(other_leg('blocked', at)).refusal_reason == 'intervention_fence'
    if input_case == 'equal_time_terminal':
        return  # the reducer retains the equal-time terminal; the request stays unresolved
    acct.owner.observe(BrokerFact.terminal('base', 'cancelled', 0, at), now=at)
    assert acct.fenced(at) == ()
    # The accepted postdating terminal reconciles the request; it does not resume automation.
    resumed = acct.send(other_leg('after', at))
    assert resumed.refusal_reason == 'intervention_fence' and resumed.transport_state == 'not_attempted'
    assert len(acct.broker.commands) == 1
    assert (acct.owner.permission, acct.owner.authority) == ('HALTED', 'INTERVENTION')


# --- Case 7: (b4) a terminal resolves only the request it covers.

def test_terminal_resolves_only_the_request_it_covers(tmp_path):
    acct = Account(tmp_path)
    resting_entry(acct)
    acct.at(NOW + timedelta(seconds=1))
    assert acct.send(other_leg('orb-unknown', acct.now), outcome='unknown').transport_state == 'unknown'
    sent = len(acct.broker.commands)
    at = acct.at(NOW + timedelta(minutes=20))
    assert acct.fenced(at) == ('base', 'orb-unknown')
    acct.owner.observe(BrokerFact.terminal('base', 'cancelled', 0, at), now=at)
    assert acct.fenced(at) == ('orb-unknown',)
    # CC-3: the unknown orb request halted the account, so every later send meets the fence.
    assert acct.send(replace(intent('still-blocked'), bar_time=at)).refusal_reason == 'intervention_fence'
    acct.owner.observe(BrokerFact.terminal('orb-unknown', 'cancelled', 0, at), now=at)
    assert acct.fenced(at) == ()
    assert acct.send(other_leg('after', at)).refusal_reason == 'intervention_fence'
    assert len(acct.broker.commands) == sent
    assert (acct.owner.permission, acct.owner.authority) == ('HALTED', 'INTERVENTION')


# --- Case 8: takeover quiescence counts (ii), (iii) and displaced-leg orders only.

def test_takeover_not_blocked_by_non_displaced_order_within_first_bar(tmp_path):
    acct = takeover_account(tmp_path)
    striker_add(acct)
    acct.tick()
    displaced_orb_entry(acct)
    aegis_takeover(acct)
    root = complete_takeover(acct)
    assert root.transport_state == 'accepted', root
    assert aegis_sent(acct)
    assert acct.classify('s-add', acct.now) == 'accepted'


def test_takeover_blocked_by_non_displaced_stale_request(tmp_path):
    acct = takeover_account(tmp_path)
    add, add_result = striker_add(acct)
    last = acct.at(NOW + timedelta(minutes=5))
    assert acct.evidence(STRIKER, [working(add_result, add, 50)], at=last) == 'qualified'
    acct.at(NOW + timedelta(minutes=15))
    displaced_orb_entry(acct)
    aegis_takeover(acct)
    acct.at(last + BAR_PERIOD + timedelta(seconds=1))
    root = complete_takeover(acct)
    assert acct.classify('s-add', acct.now) == 'stale'
    assert root.refusal_reason == 'unknown_order', root
    assert not aegis_sent(acct)


def test_takeover_requires_displaced_order_terminal(tmp_path):
    acct = takeover_account(tmp_path)
    add, add_result = striker_add(acct)
    at = acct.tick()
    acct.owner.observe(acct.broker.execute_entry('s-add', fill_id='s-add-fill', quantity=50,
                                                 price=100, at=at), now=at)
    acct.owner.observe(BrokerFact.terminal('s-add', 'filled', 50, at), now=at)
    acct.tick()
    orb, orb_result = displaced_orb_entry(acct)
    aegis_takeover(acct)
    poll_takeover(acct)
    assert any(c.kind == 'cancel' and c.target_operation_id == 'orb-1' for c in acct.broker.commands)
    assert acct.evidence(ORB, [working(orb_result, orb, 1)], at=acct.tick()) == 'qualified'
    assert acct.classify('orb-1', acct.now) == 'known_working'
    _controls, done = poll_takeover(acct)
    assert not done
    assert acct.owner.resume_takeover(now=acct.now) == ()
    assert not aegis_sent(acct)
    cancel_displaced(acct)
    _controls, done = poll_takeover(acct)
    assert done
    assert resume_root(acct).transport_state == 'accepted'


# --- Case 9: (b5) and S9; classification never grants permission.

def test_pre_restart_evidence_never_makes_request_known_working_after_restart(tmp_path):
    from c1_rail.book_account_owner import SyntheticOrderEvidence
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    row = working(result, action, 3)
    before = acct.at(NOW + timedelta(minutes=10))
    assert acct.evidence(STRIKER, [row], at=before) == 'qualified'
    pending_read = acct.owner.prepare_synthetic_order_read(STRIKER, now=acct.tick())
    assert acct.classify('base', NOW + timedelta(minutes=20)) == 'known_working'
    restarted = BookAccountOwner.boot(acct.owner.path, acct.owner.account, binding=acct.owner.binding,
                                      synthetic_broker=acct.broker)
    assert restarted.permission == 'HALTED'
    at = acct.at(NOW + timedelta(minutes=20))
    for read_id, as_of in ((pending_read.read_id, at), (pending_read.read_id, before + timedelta(seconds=1))):
        disposition = restarted.observe_synthetic_order_evidence(
            SyntheticOrderEvidence(read_id, STRIKER, as_of, True, False, (row,)), now=at)
        assert disposition != 'qualified'
    assert restarted.request_classification(now=at)['base'] == 'stale'
    assert restarted.permission == 'HALTED'


def test_refreshed_evidence_never_restores_permission_after_incident_halt(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    assert acct.evidence(STRIKER, [working(result, action, 3)],
                         at=acct.at(NOW + timedelta(minutes=5))) == 'qualified'
    stale = acct.at(NOW + timedelta(minutes=21))
    assert acct.classify('base', stale) == 'stale'
    acct.owner.halt('incident-under-test', 'operator', now=stale)
    before = (acct.owner.permission, acct.owner.authority, acct.owner.incidents)
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=acct.tick()) == 'qualified'
    assert acct.classify('base', acct.now) == 'known_working'
    assert (acct.owner.permission, acct.owner.authority, acct.owner.incidents) == before
    assert before[:2] == ('HALTED', 'INTERVENTION')
    refused = acct.send(other_leg('after-halt', acct.now))
    assert refused.refusal_reason == 'intervention_fence'
    assert len([c for c in acct.broker.commands if c.kind == 'entry']) == 1


# --- Case 10: cutoff and own-flat deadline are unchanged consumers.

def test_cutoff_cancels_known_working_entry(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    evidenced = acct.at(SESSION.risk_add_cutoff - timedelta(minutes=5))
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=evidenced) == 'qualified'
    cutoff = acct.at(SESSION.risk_add_cutoff)
    assert acct.classify('base', cutoff) == 'known_working'
    acct.owner.advance_schedule(now=cutoff)
    cancel = acct.broker.commands[-1]
    assert cancel.kind == 'cancel' and cancel.target_operation_id == 'base'
    assert acct.owner.authority == 'SCHEDULED_EXIT'
    # The cancel is a later dispatch touching the order: older evidence no
    # longer makes it known working, and the request stays owned.
    assert acct.classify('base', cutoff) == 'stale'
    assert acct.owner.exposure('dj30_mym_p250') == (0, 3)


@pytest.mark.parametrize('state', ['known_working', 'stale', 'unknown'])
def test_deadline_breach_with_known_working_stale_or_unknown_request(tmp_path, state):
    acct = Account(tmp_path)
    action = intent()
    result = acct.send(action, outcome='unknown' if state == 'unknown' else 'accepted')
    acct.at(SESSION.risk_add_cutoff)
    acct.owner.advance_schedule(now=acct.now)
    deadline = SESSION.own_flat_deadline
    if state == 'unknown':
        # CC-3: the unknown entry halted the account at dispatch, so no automatic cutoff cancel
        # and no deadline incident follow; the request stays classified unknown.
        assert [c.kind for c in acct.broker.commands] == ['entry']
        acct.at(deadline)
        acct.owner.advance_schedule(now=deadline)
        assert acct.owner.authority == 'INTERVENTION'
        assert [i['incident_id'] for i in acct.owner.incidents] == ['ordinary-unknown:' + result.attempt_id]
        assert acct.classify('base', deadline) == 'unknown'
        return
    assert acct.broker.commands[-1].kind == 'cancel'
    if state == 'known_working':
        assert acct.evidence(STRIKER, [working(result, action, 3)],
                             at=acct.at(deadline - timedelta(minutes=1))) == 'qualified'
    acct.at(deadline)
    acct.owner.advance_schedule(now=deadline)
    assert acct.owner.authority == 'INTERVENTION'
    assert any(i['incident_id'] == 'own-flat-deadline:' + SESSION.session_id for i in acct.owner.incidents)
    assert acct.classify('base', deadline) == state


# --- Case 11: the operator-confirmed inclusive one-bar boundary.

def test_evidence_fresh_just_under_one_bar(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    evidenced = acct.at(NOW + timedelta(minutes=5))
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=evidenced) == 'qualified'
    at = acct.at(evidenced + BAR_PERIOD - MICROSECOND)
    assert acct.classify('base', at) == 'known_working'
    assert acct.fenced(at) == ()
    assert acct.send(other_leg('other', at)).transport_state == 'accepted'


def test_evidence_stale_at_exactly_one_bar(tmp_path):
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    evidenced = acct.at(NOW + timedelta(minutes=5))
    assert acct.evidence(STRIKER, [working(result, action, 3)], at=evidenced) == 'qualified'
    at = acct.at(evidenced + BAR_PERIOD)
    assert acct.classify('base', at) == 'stale'
    assert acct.fenced(at) == ('base',)
    assert acct.send(other_leg('other', at)).refusal_reason == 'unknown_order'


# --- Case 12: E1 ordering; replayed or reordered reads cannot restore (i).

def test_newer_position_only_read_then_older_full_read_cannot_restore_known_working(tmp_path):
    from c1_rail.book_account_owner import SyntheticOrderEvidence
    acct = Account(tmp_path)
    action, result = resting_entry(acct)
    row = working(result, action, 3)
    first = acct.at(NOW + timedelta(minutes=5))
    assert acct.evidence(STRIKER, [row], at=first) == 'qualified'
    older = acct.owner.prepare_synthetic_order_read(STRIKER, now=NOW + timedelta(minutes=11))
    newer = acct.owner.prepare_synthetic_order_read(STRIKER, now=NOW + timedelta(minutes=11, seconds=1))
    position_at = acct.at(NOW + timedelta(minutes=11, seconds=5))
    assert acct.evidence(STRIKER, [], at=position_at, read=newer, position_only=True) != 'qualified'
    full = SyntheticOrderEvidence(older.read_id, STRIKER, NOW + timedelta(minutes=11, seconds=3),
                                  True, False, (row,))
    assert acct.owner.observe_synthetic_order_evidence(full, now=acct.tick()) != 'qualified'
    assert acct.owner.observe_synthetic_order_evidence(full, now=acct.tick()) != 'qualified'
    evaluate = first + BAR_PERIOD
    assert acct.classify('base', evaluate) == 'stale'
    assert acct.fenced(evaluate) == ('base',)
