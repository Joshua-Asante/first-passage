"""A9-PREP: mocked tests for the provider-neutral BarSource contract (no network, no provider)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

from c1_rail.book_policy import LEG_BY_ID
from c1_signal_daemon.bar_source_contract import (
    LEG_FEEDS, AuthRejected, ContractBarSource, DeliveredBar, Lease, SymbolBinding,
    TransportError, TransportPolicy, bar_open_utc, in_product_frame)
from c1_signal_daemon.book_runtime import LEG_ORDER
from c1_signal_daemon.evaluate_loop import EvaluateLoop
from c1_signal_daemon.strategy_protocol import Signal

UTC = timezone.utc
NY = ZoneInfo("America/New_York")
T0 = datetime(2026, 10, 6, 14, 0, tzinfo=UTC)  # Tuesday 10:00 EDT
DONE = T0 + timedelta(minutes=15, seconds=5)   # T0 bar completed, inside M5
SESSION = SimpleNamespace(opens_at=datetime(2026, 10, 5, 22, tzinfo=UTC),
                          closes_at=datetime(2026, 10, 6, 21, tzinfo=UTC))
CODE = "PROVIDER:MNQ-DEC26"  # placeholder provider-native code


class Clock:
    def __init__(self, now):
        self.now = now

    def __call__(self):
        return self.now

    def advance(self, **delta):
        self.now += timedelta(**delta)


class FakeTransport:
    """Scripted BarTransport: queued outcomes per method, success by default."""

    def __init__(self, clock):
        self.clock, self.lease_s, self.calls = clock, 3600, []
        self.script = {"authenticate": [], "renew": [], "connect": [], "receive": []}

    def _run(self, name, default):
        self.calls.append(name)
        outcome = self.script[name].pop(0) if self.script[name] else default
        if isinstance(outcome, Exception):
            raise outcome
        return outcome() if callable(outcome) else outcome

    def _lease(self):
        return Lease(self.clock.now + timedelta(seconds=self.lease_s))

    def authenticate(self):
        return self._run("authenticate", self._lease)

    def renew(self, lease):
        return self._run("renew", self._lease)

    def connect(self, lease):
        return self._run("connect", None)

    def receive(self):
        return self._run("receive", [])

    def close(self):
        self.calls.append("close")


def delivered(stamp, *, close=100.0, volume=5.0, symbol=CODE, **flags):
    return DeliveredBar(symbol, stamp, 100.0, 101.0, 99.0, close, volume, **flags)


def make(clock, *, stamp="open", valid_until=None, window=lambda ts: SESSION,
         policy=None):
    transport = FakeTransport(clock)
    binding = SymbolBinding("orb_mnq_v7", "CME", CODE, "MNQZ6",
                            valid_until or datetime(2026, 12, 18, tzinfo=UTC), stamp)
    source = ContractBarSource(transport, binding=binding,
                               policy=policy or TransportPolicy(1.0, 8.0, 60.0),
                               session_window=window, clock=clock)
    return source, transport


# -- completed-bar delivery ------------------------------------------------------

def test_completed_bar_forwarded_once_keyed_at_bar_open_utc():
    clock = Clock(DONE)
    source, transport = make(clock, stamp="close")
    local_close = (T0 + timedelta(minutes=15)).astimezone(ZoneInfo("America/Chicago"))
    transport.script["receive"] = [[delivered(local_close)], [delivered(local_close)]]
    bar = source.poll()
    assert bar.ts == T0 and bar.ts.tzinfo is UTC and bar.volume == 5.0
    assert source.poll() is None
    assert source.counts["duplicate"] == 1 and source.connected and source.healthy()


def test_forming_bar_never_forwarded_and_final_bar_still_admitted():
    clock = Clock(T0 + timedelta(minutes=14))
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0, close=99.5)]]
    assert source.poll() is None
    clock.now = DONE
    transport.script["receive"] = [[delivered(T0, final=False)], [delivered(T0)]]
    assert source.poll() is None
    assert source.poll().close == 100.0
    assert source.counts["incomplete"] == 2


def test_bar_after_m5_deadline_not_forwarded():
    clock = Clock(T0 + timedelta(minutes=15, seconds=31))
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0)]]
    assert source.poll() is None and source.counts["late"] == 1


def test_revision_of_delivered_bar_never_forwarded_and_counted():
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0)], [delivered(T0, close=100.5)]]
    assert source.poll().close == 100.0
    assert source.poll() is None and source.counts["revision"] == 1


def test_out_of_order_bar_not_forwarded():
    clock = Clock(DONE + timedelta(minutes=15))
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0 + timedelta(minutes=15))], [delivered(T0)]]
    assert source.poll().ts == T0 + timedelta(minutes=15)
    assert source.poll() is None and source.counts["out_of_order"] == 1


@pytest.mark.parametrize("flags", [{"volume": 0.0}, {"trade_evidence": False}])
def test_empty_or_synthetic_bar_is_absent_not_forwarded(flags):
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0, **flags)]]
    assert source.poll() is None and source.counts["no_trade_evidence"] == 1


def test_other_contract_code_never_substituted():
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0, symbol="PROVIDER:MNQ-MAR27")]]
    assert source.poll() is None and source.counts["foreign_symbol"] == 1


# -- session and timezone semantics --------------------------------------------

def test_naive_dst_ambiguous_and_off_grid_stamps_refused():
    for stamp in (T0.replace(tzinfo=None),                   # naive
                  datetime(2026, 11, 1, 1, 30, tzinfo=NY),   # fall-back fold
                  datetime(2026, 3, 8, 2, 30, tzinfo=NY),    # spring-forward gap
                  T0 + timedelta(minutes=7)):                # off grid
        with pytest.raises(ValueError):
            bar_open_utc(stamp, "open")
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0.replace(tzinfo=None))]]
    assert source.poll() is None and source.counts["invalid_time"] == 1


@pytest.mark.parametrize("utc, expected", [
    ((2026, 10, 6, 20, 45), True),    # 16:45 EDT
    ((2026, 10, 6, 21, 0), False),    # 17:00 EDT: daily break
    ((2026, 10, 6, 21, 45), False),   # 17:45 EDT
    ((2026, 10, 6, 22, 0), True),     # 18:00 EDT: reopen
    ((2026, 12, 8, 21, 45), True),    # 16:45 EST: same UTC slot trades in winter
    ((2026, 12, 8, 22, 0), False),    # 17:00 EST
    ((2026, 12, 8, 23, 0), True),     # 18:00 EST
    ((2026, 10, 9, 20, 45), True),    # Friday 16:45 EDT
    ((2026, 10, 9, 21, 0), False),    # Friday 17:00 EDT: weekend
    ((2026, 10, 10, 15, 0), False),   # Saturday
    ((2026, 10, 11, 21, 45), False),  # Sunday 17:45 EDT
    ((2026, 10, 11, 22, 0), True),    # Sunday 18:00 EDT open
])
def test_product_frame_follows_new_york_dst(utc, expected):
    assert in_product_frame(datetime(*utc, tzinfo=UTC)) is expected


def test_nothing_in_break_after_product_halt_or_outside_coverage():
    halt = datetime(2026, 10, 6, 17, 0, tzinfo=UTC)  # 13:00 EDT early close
    early = SimpleNamespace(opens_at=SESSION.opens_at, closes_at=halt)
    clock = Clock(halt + timedelta(seconds=5))
    source, transport = make(clock, window=lambda ts: early)
    transport.script["receive"] = [[delivered(halt - timedelta(minutes=15))]]
    assert source.poll().ts == halt - timedelta(minutes=15)
    clock.advance(minutes=15)
    transport.script["receive"] = [[delivered(halt)]]
    assert source.poll() is None
    brk = datetime(2026, 10, 6, 21, 0, tzinfo=UTC)  # 17:00 EDT, window allows it
    open_window = SimpleNamespace(opens_at=brk - timedelta(days=1), closes_at=brk + timedelta(days=1))
    for window, ts in ((lambda ts: open_window, brk), (lambda ts: None, T0)):
        clock = Clock(ts + timedelta(minutes=15, seconds=5))
        source, transport = make(clock, window=window)
        transport.script["receive"] = [[delivered(ts)]]
        assert source.poll() is None and source.counts["outside_session"] == 1


# -- authentication, renewal, reconnect ------------------------------------------

def test_rejected_credential_latches_refusal_without_retry():
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["authenticate"] = [AuthRejected("401")]
    transport.script["receive"] = [[delivered(T0)]]
    assert source.poll() is None
    clock.advance(hours=6)
    assert source.poll() is None
    assert (source.state, source.refusal) == ("REFUSED", "auth_rejected")
    assert transport.calls.count("authenticate") == 1 and "receive" not in transport.calls
    assert not source.connected and not source.healthy()


def test_stream_auth_rejection_latches_refusal():
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [AuthRejected("session revoked"), [delivered(T0)]]
    assert source.poll() is None and source.poll() is None
    assert source.refusal == "auth_rejected" and transport.calls.count("receive") == 1


def test_transient_auth_failure_retries_with_capped_backoff():
    clock = Clock(T0)
    source, transport = make(clock, policy=TransportPolicy(1.0, 4.0, 60.0))
    transport.script["authenticate"] = [TransportError("503")] * 4
    for offset in (0, 0.5, 1, 3, 7, 10.9, 11):
        clock.now = T0 + timedelta(seconds=offset)
        source.poll()
    assert transport.calls.count("authenticate") == 5 and source.connected
    retries = [d["retry_at"] for _, kind, d in source.events if kind == "connect_failed"]
    assert [(b - a).total_seconds() for a, b in zip([T0] + retries, retries)] == [1, 2, 4, 4]


def test_token_renewed_before_expiry_without_reconnect():
    clock = Clock(T0)
    source, transport = make(clock)
    transport.lease_s = 120  # renewal margin 60 s
    source.poll()
    clock.advance(seconds=61)
    source.poll()
    assert transport.calls.count("renew") == 1 and transport.calls.count("authenticate") == 1
    assert "close" not in transport.calls and source.connected and source.counts["renewed"] == 1


def test_failed_renewal_disconnects_then_reauthenticates():
    clock = Clock(T0)
    source, transport = make(clock)
    transport.lease_s = 120
    source.poll()
    clock.advance(seconds=61)
    transport.script["renew"] = [AuthRejected("refresh token revoked")]
    assert source.poll() is None
    assert source.state == "DISCONNECTED" and "close" in transport.calls and not source.healthy()
    clock.advance(seconds=1)
    source.poll()
    assert transport.calls.count("authenticate") == 2 and source.connected


def test_rejected_reauthentication_after_renewal_failure_refuses():
    clock = Clock(T0)
    source, transport = make(clock)
    transport.lease_s = 120
    source.poll()
    clock.advance(seconds=61)
    transport.script["renew"] = [TransportError("timeout")]
    transport.script["authenticate"] = [AuthRejected("401")]
    source.poll()
    clock.advance(seconds=1)
    assert source.poll() is None and source.refusal == "auth_rejected"


def test_disconnect_unhealthy_and_reconnect_forwards_only_bars_within_m5():
    clock = Clock(DONE)
    source, transport = make(clock)
    transport.script["receive"] = [[delivered(T0)], TransportError("reset")]
    assert source.poll().ts == T0
    clock.advance(seconds=5)
    assert source.poll() is None
    assert not source.connected and not source.healthy()
    clock.now = T0 + timedelta(minutes=45, seconds=5)  # T0+15 missed its deadline
    transport.script["receive"] = [[delivered(T0 + timedelta(minutes=30)),
                                    delivered(T0 + timedelta(minutes=15))]]
    assert source.poll().ts == T0 + timedelta(minutes=30)
    assert source.counts["late"] == 1 and transport.calls.count("authenticate") == 2


# -- staleness and fail-closed -------------------------------------------------

def test_staleness_uses_s2b_formula():
    clock = Clock(DONE)
    source, transport = make(clock)
    assert source.poll() is None and source.connected and not source.healthy()  # no bar yet
    transport.script["receive"] = [[delivered(T0)]]
    source.poll()
    assert source.healthy(T0 + timedelta(seconds=2 * 900 + 30))
    assert not source.healthy(T0 + timedelta(seconds=2 * 900 + 31))


class _AlwaysSignal:
    def on_bar(self, bar):
        return Signal(leg_id="nas100_mnq", signal_type="entry", close=bar.close,
                      stop_dist_pts=10.0, bar_time="t-fresh")


class _Client:
    def __init__(self):
        self.posts = []

    def post_b1(self, payload):
        self.posts.append(payload)
        return 200, "ok"


def test_expired_binding_refuses_and_evaluate_loop_emits_nothing():
    clock = Clock(DONE)
    source, transport = make(clock, valid_until=DONE + timedelta(minutes=15))
    client = _Client()
    loop = EvaluateLoop(source=source, client=client, strategy=_AlwaysSignal(), emit_enabled=True)
    transport.script["receive"] = [[delivered(T0)]]
    assert loop.step(clock.now)["action"] == "posted"
    clock.advance(minutes=15)
    transport.script["receive"] = [[delivered(T0 + timedelta(minutes=15))]]
    assert loop.step(clock.now) == {"action": "suppress", "reason": "feed_unhealthy"}
    assert source.refusal == "binding_expired" and len(client.posts) == 1
    assert transport.calls.count("receive") == 1 and source.poll() is None


# -- configuration -----------------------------------------------------------

@pytest.mark.parametrize("args", [
    ("mnq", "CME", CODE, "MNQZ6", T0, "open"),
    ("orb_mnq_v7", "CBOT", CODE, "MNQZ6", T0, "open"),
    ("orb_mnq_v7", "CME", CODE, "MYMZ6", T0, "open"),
    ("orb_mnq_v7", "CME", CODE, "MNQ1!", T0, "open"),
    ("orb_mnq_v7", "CME", " ", "MNQZ6", T0, "open"),
    ("orb_mnq_v7", "CME", CODE, "MNQZ6", T0.replace(tzinfo=None), "open"),
    ("orb_mnq_v7", "CME", CODE, "MNQZ6", T0, "mid"),
])
def test_binding_refuses_invalid_mapping(args):
    with pytest.raises(ValueError):
        SymbolBinding(*args)


@pytest.mark.parametrize("args", [(0, 1, 60), (2, 1, 60), (1, 31, 60), (1, 30, 0)])
def test_policy_refuses_bounds_outside_contract(args):
    with pytest.raises(ValueError):
        TransportPolicy(*args)


def test_backoff_stays_capped_after_long_outage():
    assert TransportPolicy(1.0, 30.0, 60.0).delay(5000) == timedelta(seconds=30)


def test_leg_feeds_cover_the_book_in_priority_order():
    assert tuple(LEG_FEEDS) == LEG_ORDER
    assert all(LEG_FEEDS[leg][0] == LEG_BY_ID[leg].symbol for leg in LEG_ORDER)
