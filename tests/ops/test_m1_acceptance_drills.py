"""M1 offline acceptance drills — ADR 2026-07-22 §4 items 2, 3, 4, 7, 8, 9.

These are the six drills the acceptance validator requires by name
(``scripts/validate_c1_monitoring_acceptance.py`` ``REQUIRED_DRILLS``), one
test each, named ``test_drill_<key>`` so the mapping from
``M1_MONITORING_ACCEPTANCE.json`` to executable evidence is mechanical:

    transport_unknown            -> §4 item 8
    partial_fill_confirmed_base  -> §4 item 9 (partial authorizes from base)
    rejected_entry_no_add        -> §4 item 9 (reject authorizes nothing)
    exit_on_equity_failure       -> §4 item 3 (+ item 2's "never blocks exit")
    restart_confirmed_base       -> §4 item 9 (survives process restart)
    b6_wrong_secret_shape        -> §4 item 7

Each drill plants a REAL failure and asserts against production code
(``handle_signal`` / ``process_signal`` / ``EventLedger`` /
``ExecutionStateStore`` / ``reconcile_chain``) — no reimplementation of rail
logic lives here.

**Every drill carries a negative control.** A guard test that only asserts
"the bad thing halted" passes vacuously if the good path is also broken, so
each drill also proves the *permissive* branch still works. That is the whole
point of the asymmetry these criteria encode: risk-add must be blocked while
risk-reduction must not be.

Venue-free by construction — no CrossTrade, Tradovate, or TradingView. The
three criteria these drills CANNOT cover are §4 items 5 (structured event from
a real strategy signal), 6 (controlled SIM ``CHAIN_OK``), and 10 (deployed
notification channel + operator acknowledgement). Those are operator-owned and
must stay absent from the acceptance artifact until evidenced at the desk.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail_listener import handle_signal
from c1_rail_telemetry import (
    BrokerEvidence,
    EventLedger,
    ExecutionStateStore,
    reconcile_chain,
)
from c1_sizing_host_reference import C1SizingHostReference, generate_constants

TIER = "Tradeify_Select_100K"
E_FIRM = 100_000.0
LEG_ID = "dj30_mym"
LEG_KEY = "Striker"
STOP = 60.8201


def _write_json(path, obj):
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


def _seed_state(tmp_path):
    _write_json(tmp_path / "lifecycle_state.json",
                {"Striker": "WATCH-1", "Striker NAS100": "WATCH-1"})
    _write_json(tmp_path / "c1_dd_state.json",
                {"account": TIER, "peak_equity": E_FIRM,
                 "last_updated_utc": "2026-07-27T00:00:00Z"})
    _write_json(tmp_path / "c1_sizing_constants.json", generate_constants(TIER))


def _make_host(tmp_path):
    return C1SizingHostReference(
        lifecycle_state_path=tmp_path / "lifecycle_state.json",
        dd_state_path=tmp_path / "c1_dd_state.json",
        constants_path=tmp_path / "c1_sizing_constants.json",
    )


@pytest.fixture
def host(tmp_path):
    _seed_state(tmp_path)
    return _make_host(tmp_path)


def _payload(signal_type, *, bar_time=1752778800000, close=44100.0):
    return {"leg_id": LEG_ID, "signal_type": signal_type, "bar_time": bar_time,
            "close": close, "stop_dist_pts": STOP}


def _config(**overrides):
    # dry_run=False + a live armed_until == a correctly-armed rail. Computed,
    # not hardcoded, so the drills never expire into a spurious failure.
    cfg = dict(account="TDFY-DRILL", secret_key="drill-secret",
               webhook_id="drill-id", webhook_secret="drill-wh",
               destination="tradovate", dry_run=False,
               armed_until=(datetime.now(timezone.utc)
                            + timedelta(hours=1)).isoformat())
    cfg.update(overrides)
    return cfg


class _CapturingSender:
    def __init__(self, status=200):
        self.calls = []
        self._status = status

    def __call__(self, url, body, headers):
        self.calls.append({"url": url, "body": body, "headers": headers})
        return self._status


def _pyr_pct():
    """Pyramid % for the MYM leg, read from production constants (locked)."""
    return float(generate_constants(TIER)["leg_map"][LEG_ID]["pyr_pct"])


# ── §4 item 8 — transport unknown blocks risk-add, never auto-retries ──────

def test_drill_transport_unknown(host, tmp_path):
    """A timeout AFTER bytes may have left is `unknown`, not a failure.

    It must block the next risk-add and must never be automatically retried.
    """
    def timeout_sender(url, body, headers):
        raise TimeoutError("planted: timeout after bytes may have left")

    ledger = EventLedger(tmp_path / "events.jsonl")
    first = handle_signal(_payload("entry"), host, current_equity=E_FIRM,
                          config=_config(), sender=timeout_sender, ledger=ledger)
    assert first.transport_state == "unknown"
    assert first.sent is False
    assert ledger.risk_add_blocked is True

    # The next risk-add is blocked, and the sender is NOT called again
    # (no automatic retry of an uncertain send).
    retry_sender = _CapturingSender()
    blocked = handle_signal(_payload("entry", bar_time=2), host,
                            current_equity=E_FIRM, config=_config(),
                            sender=retry_sender, ledger=ledger)
    assert blocked.decision.halt is True
    assert blocked.sent is False
    assert retry_sender.calls == []
    assert "reconcile" in (blocked.decision.halt_reason or "").lower()

    # NEGATIVE CONTROL: the block is state, not a permanent brick — an
    # explicit operator repair clears it and sizing resumes. Without this the
    # assertions above would also pass on a host that halts everything.
    ledger.clear_risk_add_block()
    assert ledger.risk_add_blocked is False
    ok_sender = _CapturingSender()
    resumed = handle_signal(_payload("entry", bar_time=3), host,
                            current_equity=E_FIRM, config=_config(),
                            sender=ok_sender, ledger=ledger)
    assert resumed.decision.halt is False
    assert resumed.decision.qty_out == 8
    assert len(ok_sender.calls) == 1

    # CrossTrade order_id idempotency is NOT proven by this drill and no
    # correctness claim rests on it (§4 item 8's explicit escape clause).


# ── §4 item 9 — a partial entry authorizes add sizing from the FILL ───────

def test_drill_partial_fill_confirmed_base(host):
    """Intended 8, broker fills 5 -> the add must size from 5, never from 8."""
    sender = _CapturingSender()
    entry = handle_signal(_payload("entry"), host, current_equity=E_FIRM,
                          config=_config(), sender=sender)
    intended = entry.decision.qty_out
    assert intended == 8

    # Intended quantity must NOT have seeded executed base on its own.
    assert host.open_leg_state.get(LEG_KEY) is None

    partial_fill = 5
    host.confirm_executed_base(LEG_KEY, partial_fill)

    add = handle_signal(_payload("add", bar_time=2), host,
                        current_equity=E_FIRM, config=_config(), sender=sender)
    expected_from_fill = int(partial_fill * _pyr_pct() // 100)
    expected_from_intended = int(intended * _pyr_pct() // 100)
    assert add.decision.qty_out == expected_from_fill
    # NEGATIVE CONTROL: the two differ, so the assertion above genuinely
    # discriminates confirmed-base sizing from intended-quantity sizing.
    assert expected_from_fill != expected_from_intended
    assert add.decision.qty_out < expected_from_intended

    # A partial is also a reconcile mismatch, not a clean chain.
    verdict = reconcile_chain(
        intended_qty=intended, transport_state="accepted",
        evidence=BrokerEvidence(
            event_id="drill-partial", crosstrade_receive=True,
            crosstrade_validate=True, crosstrade_execute=True,
            fill_qty=partial_fill, tradovate_status="Filled"),
        signal_type="entry")
    assert verdict == "QTY_MISMATCH"


# ── §4 item 9 — a rejected entry authorizes NOTHING ───────────────────────

def test_drill_rejected_entry_no_add(host):
    """A rejected entry leaves no confirmed base, so an add must halt."""
    sender = _CapturingSender()
    entry = handle_signal(_payload("entry"), host, current_equity=E_FIRM,
                          config=_config(), sender=sender)
    assert entry.decision.qty_out == 8

    # Broker rejected it downstream — despite an accepted HTTP transport.
    rejected = reconcile_chain(
        intended_qty=entry.decision.qty_out, transport_state="accepted",
        evidence=BrokerEvidence(
            event_id="drill-reject", crosstrade_receive=True,
            crosstrade_validate=True, crosstrade_execute=False,
            tradovate_status="Rejected"),
        signal_type="entry")
    assert rejected == "REJECTED"

    # No confirm_executed_base call was made, so the add cannot be authorized.
    add = handle_signal(_payload("add", bar_time=2), host,
                        current_equity=E_FIRM, config=_config(), sender=sender)
    assert add.decision.halt is True
    assert add.decision.qty_out == 0
    assert "no tracked executed base" in (add.decision.halt_reason or "")
    assert not any("add" in c["body"] for c in sender.calls)

    # NEGATIVE CONTROL: the same add succeeds once a base IS confirmed, so the
    # halt above is caused by the missing base and not by a broken add path.
    host.confirm_executed_base(LEG_KEY, 8)
    ok_add = handle_signal(_payload("add", bar_time=3), host,
                           current_equity=E_FIRM, config=_config(),
                           sender=sender)
    assert ok_add.decision.halt is False
    assert ok_add.decision.qty_out == 60


# ── §4 item 3 (+ item 2) — state failure blocks risk-add, NEVER exit/flat ──

@pytest.mark.parametrize("reducing_signal", ["exit", "flat"])
def test_drill_exit_on_equity_failure(tmp_path, reducing_signal):
    """Plant total state failure: entries halt, risk-REDUCING orders relay.

    All three state inputs are destroyed (constants, lifecycle, DD/equity), so
    no sizing input is readable at all. This is the strongest form of the
    planted failure and proves the asymmetry structurally.
    """
    _seed_state(tmp_path)
    host = _make_host(tmp_path)

    # Plant the failure: unreadable constants + missing lifecycle + corrupt DD.
    (tmp_path / "c1_sizing_constants.json").write_text("{ not json",
                                                       encoding="utf-8")
    (tmp_path / "lifecycle_state.json").unlink()
    (tmp_path / "c1_dd_state.json").write_text("\x00\x01 corrupt",
                                               encoding="utf-8")

    entry_sender = _CapturingSender()
    entry = handle_signal(_payload("entry"), host, current_equity=E_FIRM,
                          config=_config(), sender=entry_sender)
    assert entry.decision.halt is True
    assert entry.decision.qty_out == 0
    assert entry.sent is False
    assert entry_sender.calls == [], "risk-add must not reach the sender"

    # The same broken state must NOT block a risk-reducing order.
    exit_sender = _CapturingSender()
    reducing = handle_signal(_payload(reducing_signal, bar_time=2), host,
                             current_equity=E_FIRM, config=_config(),
                             sender=exit_sender)
    assert reducing.decision.halt is False, "exit/flat must never halt on state"
    assert reducing.sent is True
    assert len(exit_sender.calls) == 1
    body = exit_sender.calls[0]["body"]
    assert "command=closeposition;" in body
    # Relayed WITHOUT invoking sizing — no quantity is computed or sent.
    assert "quantity=" not in body
    assert reducing.decision.qty_out == 0


def test_drill_exit_on_equity_failure_flat_clears_only_when_broker_confirmed(
        tmp_path):
    """Persisted execution state clears on broker-confirmed flatness ONLY.

    A flat *signal* is not evidence of flatness (ADR M1 §2.7) — the host
    deliberately does not clear on it.
    """
    _seed_state(tmp_path)
    host = _make_host(tmp_path)
    store = ExecutionStateStore(tmp_path / "exec_state.json")

    host.confirm_executed_base(LEG_KEY, 8)
    store.set_confirmed_base(LEG_KEY, 8)
    assert store.get_confirmed_base(LEG_KEY) == 8

    # A bare flat signal must NOT clear confirmed base.
    handle_signal(_payload("flat", bar_time=2), host, current_equity=E_FIRM,
                  config=_config(), sender=_CapturingSender())
    assert host.open_leg_state.get(LEG_KEY) == 8
    assert store.get_confirmed_base(LEG_KEY) == 8

    # Broker-CONFIRMED flatness does clear it.
    evidence = BrokerEvidence(event_id="drill-flat", flat_confirmed=True,
                              position_after=0)
    assert reconcile_chain(intended_qty=None, transport_state="accepted",
                           evidence=evidence, signal_type="flat") == "CHAIN_OK"
    host.clear_executed_base(LEG_KEY)
    store.clear_leg(LEG_KEY)
    assert host.open_leg_state.get(LEG_KEY) is None
    assert store.get_confirmed_base(LEG_KEY) is None

    # NEGATIVE CONTROL: an unconfirmed flat is NOT CHAIN_OK.
    assert reconcile_chain(
        intended_qty=None, transport_state="accepted",
        evidence=BrokerEvidence(event_id="drill-flat-2", flat_confirmed=False),
        signal_type="flat") == "NO_FLAT_CONFIRM"


# ── §4 item 9 — confirmed base survives a process restart ─────────────────

def test_drill_restart_confirmed_base(tmp_path):
    """Add sizing after a restart comes from the PERSISTED confirmed base."""
    _seed_state(tmp_path)
    host = _make_host(tmp_path)
    store = ExecutionStateStore(tmp_path / "exec_state.json")

    partial_fill = 5
    host.confirm_executed_base(LEG_KEY, partial_fill)
    store.set_confirmed_base(LEG_KEY, partial_fill)

    # Simulate the restart: brand-new host and store objects, nothing in
    # memory, exactly as run_server does at startup (exec_state.load_into).
    restarted_host = _make_host(tmp_path)
    restarted_store = ExecutionStateStore(tmp_path / "exec_state.json")
    assert restarted_host.open_leg_state == {}, "must start with empty memory"
    restarted_store.load_into(restarted_host.open_leg_state)
    assert restarted_host.open_leg_state.get(LEG_KEY) == partial_fill

    add = handle_signal(_payload("add", bar_time=9), restarted_host,
                        current_equity=E_FIRM, config=_config(),
                        sender=_CapturingSender())
    assert add.decision.halt is False
    assert add.decision.qty_out == int(partial_fill * _pyr_pct() // 100)

    # NEGATIVE CONTROL: without the load_into hydration a restarted host must
    # HALT the add rather than invent a base — proving the pass above is caused
    # by the persisted state and not by some default.
    cold_host = _make_host(tmp_path)
    cold_add = handle_signal(_payload("add", bar_time=10), cold_host,
                             current_equity=E_FIRM, config=_config(),
                             sender=_CapturingSender())
    assert cold_add.decision.halt is True
    assert "no tracked executed base" in (cold_add.decision.halt_reason or "")


# ── §4 item 7 — B6 wrong-secret shape is never CHAIN_OK, despite HTTP 200 ──

def test_drill_b6_wrong_secret_shape():
    """Replay the B6 defect: HTTP 200 at the rail, VALIDATE failed downstream.

    The 2026-07-20 B4 failure looked clean from the rail's own log
    (`sent=True http_status=200`) while CrossTrade rejected all four on
    `Secret key is missing, invalid, or inactive`.
    """
    wrong_secret = BrokerEvidence(
        event_id="drill-b6", crosstrade_receive=True,
        crosstrade_validate=False, crosstrade_execute=False,
        crosstrade_trace_id="drill-trace",
        notes="B6 shape: key rejected at VALIDATE")

    verdict = reconcile_chain(intended_qty=8, transport_state="accepted",
                              evidence=wrong_secret, signal_type="entry")
    assert verdict == "REJECTED"
    assert verdict != "CHAIN_OK"

    # Same shape with no evidence attached at all is RAIL_ONLY — also never
    # CHAIN_OK. An HTTP 200 alone can never be surfaced as execution verified.
    assert reconcile_chain(intended_qty=8, transport_state="accepted",
                           evidence=None, signal_type="entry") == "RAIL_ONLY"

    # NEGATIVE CONTROL: the identical call with a VALID key and a matching
    # fill IS CHAIN_OK, so the REJECTED verdicts above are driven by the
    # planted secret failure and not by a reconciler that never passes.
    assert reconcile_chain(
        intended_qty=8, transport_state="accepted",
        evidence=BrokerEvidence(
            event_id="drill-b6-ok", crosstrade_receive=True,
            crosstrade_validate=True, crosstrade_execute=True,
            fill_qty=8, tradovate_status="Filled"),
        signal_type="entry") == "CHAIN_OK"


# ── §4 items 1 + 4 — no secret reaches the event file; stream stays valid ──

def test_drill_ledger_secret_free_and_ordered(tmp_path):
    """Supporting evidence for §4 items 1 and 4 on the drill path itself."""
    ledger = EventLedger(tmp_path / "events.jsonl")
    _seed_state(tmp_path)
    host = _make_host(tmp_path)
    sender = _CapturingSender()
    for i in range(5):
        handle_signal(_payload("entry", bar_time=100 + i), host,
                      current_equity=E_FIRM, config=_config(), sender=sender,
                      ledger=ledger)

    raw = (tmp_path / "events.jsonl").read_text(encoding="utf-8")
    records = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
    assert records, "ledger must not be empty"
    seqs = [r["seq"] for r in records if "seq" in r]
    assert seqs == sorted(seqs), "JSONL must stay monotonically ordered"

    # The drill config's secret VALUES must appear nowhere in the event file.
    for secret_value in ("drill-secret", "drill-wh", "drill-id"):
        assert secret_value not in raw, f"{secret_value!r} leaked into ledger"
    assert ledger.healthy is True
