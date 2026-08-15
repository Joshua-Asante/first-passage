"""c1 rail listener — Option C: ties the sizing host to a live CrossTrade order.

docs/spec/c1_nt8_sizing_host_impl.md §2.4 addendum (both unknowns resolved
2026-07-18): TradingView's alert points directly at a listener running this
module's `handle_signal`, which runs the incoming B1 payload through
C1SizingHostReference (the SAME sizing law, unchanged) and — unless halted,
floored, or in DRY_RUN — builds and sends a CrossTrade order via
ops/c1_rail/crosstrade_payload.py, targeting the linked Tradovate account directly
(no NT8 hop required).

Monitoring ADR 2026-07-22 M1: when an EventLedger is supplied, every risk-add
path persists a pre-send decision event before transport; transport outcomes
are named honestly (accepted ≠ execution verified); transport_unknown blocks
further risk-add and never auto-retries. Exit/flat remain best-effort.

This module only contains the pure decision-routing function
(`handle_signal`) plus the leg_id -> instrument-symbol mapping the sizing
host's own leg map deliberately doesn't carry (that's an order-ticket
concern, not a sizing-law concern). The actual HTTP-server socket wiring
that TradingView's webhook hits lives in ops/c1_rail/c1_rail_http_server.py — a thin
adapter around this function, intentionally not exercised by these tests —
same split as ops/c1_rail/c1_sizing_host_reference.py's tested algorithm vs. its
untested NT8/ATI host process.

INSTRUMENT_SYMBOLS is provisional (TV's own continuous-contract notation,
matching tests/rail_crosstrade/fixtures.py's convention) — verify against
CrossTrade's actual accepted order-ticket symbol format at the B6 dry-fire;
do not assume it is correct for a live order without that check.

Fail-safe (unchanged from the frozen spec, just retargeted at this
transport): halt or a floored (qty 0) decision NEVER reaches the sender.
DRY_RUN computes and returns the would-be payload for audit review but
never calls the sender either. dry_run defaults True if the config key is
absent — the same "never fail open to live" rule as the sizing host's own
state-read fail-safe.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from c1_rail_telemetry import (
    EventLedger,
    LoggingNotifier,
    OperatorNotifier,
    TelemetryError,
    TelemetryUnhealthy,
    TransportOutcome,
    body_sha256,
    decision_fields,
    make_transport_payload,
    new_event_id,
)
from c1_sizing_host_reference import C1SizingHostReference, SizingDecision
from crosstrade_payload import build_crosstrade_payload, send_to_crosstrade

INSTRUMENT_SYMBOLS: dict[str, str] = {
    "dj30_mym": "MYM1!",
    "nas100_mnq": "MNQ1!",
}


@dataclass(frozen=True)
class RailAction:
    """Audit record for one processed signal, transport layer."""
    decision: SizingDecision
    sent: bool
    dry_run: bool
    payload_text: str | None = None
    http_status: int | None = None
    event_id: str | None = None
    order_id: str | None = None
    transport_state: str | None = None  # not_attempted|accepted|failed|unknown


def _leg_action(signal_type: str) -> tuple[str, str]:
    """Map the B1 signal_type to the CrossTrade payload's (leg, action)."""
    if signal_type in ("exit", "flat"):
        return "exit", "close"
    return signal_type, "buy"  # entry / add are always long (c1 is long-only)


def _order_id(payload: dict, signal_type: str) -> str:
    leg_id = str(payload["leg_id"])
    return f"{leg_id}-{signal_type}-{payload['bar_time']}"


def arming_expiry_reason(config: Mapping[str, Any], *,
                         now: datetime | None = None) -> str | None:
    """Return a halt reason if the armed window is expired/invalid, else None.

    Arming carries a wall-clock deadline (`armed_until`, absolute ISO-8601 with
    an explicit UTC offset) so a forgotten disarm cannot leave the rail live
    indefinitely — the 2026-07-27 failure class, where an unrelated restart
    re-read `dry_run:false` off the volume and rebooted armed.

    `now` is injectable ONLY so a caller that already fixed an instant can
    evaluate against that same instant instead of re-reading the clock — see
    c1_rail_arm.plan_arm, which must judge the config it just built as of the
    moment it built it. The boot gate and the per-request risk-add gate never
    pass it: on those paths the real clock is the whole point, and the default
    keeps them byte-identical to the pre-injection behaviour.

    ABSOLUTE, deliberately — never a duration-from-boot. A relative window
    would be re-granted in full on every restart, which is precisely the bug
    this exists to close.

    FAIL-SAFE on every path: absent, wrong-typed, unparseable, or
    timezone-naive values all read as EXPIRED. A naive timestamp is rejected
    rather than assumed-UTC because guessing an operator's intended zone is
    exactly the ambiguity that would grant an unintended extra window.

    Callers apply this to risk-add (entry/add) ONLY. Exit/flat must keep
    relaying when the window lapses — otherwise an expiry mid-position would
    strand an open position with no way to close it, inverting the rail's
    standing asymmetry that a fault blocks risk-add and never risk-reduction.
    """
    raw = config.get("armed_until")
    if raw is None:
        return ("arming expired: armed_until absent while dry_run=false "
                "(fail-safe — set an absolute UTC deadline when arming)")
    if not isinstance(raw, str):
        return (f"arming expired: armed_until must be an ISO-8601 string, got "
                f"{type(raw).__name__}")
    try:
        deadline = datetime.fromisoformat(raw)
    except ValueError:
        return (f"arming expired: armed_until unparseable ({raw!r}); want "
                f"ISO-8601 with offset, e.g. 2026-07-28T17:15:00+00:00")
    if deadline.tzinfo is None:
        return (f"arming expired: armed_until has no timezone ({raw!r}); want "
                f"an explicit offset, e.g. 2026-07-28T17:15:00+00:00")
    now = now or datetime.now(timezone.utc)
    if now >= deadline:
        return (f"arming expired at {deadline.isoformat()} "
                f"(now {now.isoformat()}) — re-arm to send risk-add")
    return None


def handle_signal(
    payload: dict,
    host: C1SizingHostReference,
    current_equity: float,
    *,
    config: dict,
    sender=None,
    ledger: EventLedger | None = None,
    notifier: OperatorNotifier | None = None,
    event_id: str | None = None,
) -> RailAction:
    """Route one B1 signal through sizing + optional CrossTrade send.

    When ``ledger`` is provided:
      - entry/add require a durable pre-send decision append before send; a
        write failure halts the risk-add (never auto-retries).
      - exit/flat still attempt transport if decision allows; telemetry write
        failure raises CRITICAL via notifier but does not block the send.
      - transport_unknown blocks subsequent risk-add on the ledger.
    """
    notifier = notifier or LoggingNotifier()
    eid = event_id or new_event_id()
    dry_run = config.get("dry_run", True)  # absent -> safe default, never live
    is_risk_add = str(payload.get("signal_type", "")) in ("entry", "add")

    if ledger is not None and is_risk_add and ledger.risk_add_blocked:
        reason = ledger.block_reason or "risk-add blocked by monitoring spine"
        decision = SizingDecision(
            leg_id=str(payload.get("leg_id", "<absent>")),
            signal_type=str(payload.get("signal_type", "<absent>")),
            qty_out=0, submit=False, halt=True, halt_reason=reason,
        )
        return RailAction(decision=decision, sent=False, dry_run=dry_run,
                          event_id=eid, transport_state="not_attempted")

    # Armed-window expiry (same policy-block shape as risk_add_blocked above).
    # Gated on `not dry_run` so a disarmed rail is byte-identical to before,
    # and on is_risk_add so exit/flat always keep their path to the sender.
    if not dry_run and is_risk_add:
        expiry_reason = arming_expiry_reason(config)
        if expiry_reason is not None:
            decision = SizingDecision(
                leg_id=str(payload.get("leg_id", "<absent>")),
                signal_type=str(payload.get("signal_type", "<absent>")),
                qty_out=0, submit=False, halt=True, halt_reason=expiry_reason,
            )
            return RailAction(decision=decision, sent=False, dry_run=dry_run,
                              event_id=eid, transport_state="not_attempted")

    decision = host.process_signal(payload, current_equity=current_equity)
    order_id = None
    if "leg_id" in payload and "bar_time" in payload and not decision.halt:
        try:
            order_id = _order_id(payload, decision.signal_type)
        except (KeyError, TypeError):
            order_id = None

    def _persist_decision(*, pre_send: bool) -> None:
        if ledger is None:
            return
        payload_body: dict[str, Any] = {
            **decision_fields(decision),
            "pre_send": pre_send,
            "current_equity": current_equity,
            "dry_run": dry_run,
        }
        ledger.append("decision", payload_body, event_id=eid, order_id=order_id)

    def _persist_transport(outcome: TransportOutcome,
                           payload_text: str | None) -> None:
        if ledger is None:
            return
        try:
            ledger.append(
                "transport_result",
                make_transport_payload(
                    outcome, dry_run=dry_run,
                    payload_sha256=(body_sha256(payload_text)
                                    if payload_text else None),
                ),
                event_id=eid, order_id=order_id,
            )
        except TelemetryError as exc:
            notifier.notify(
                "CRITICAL",
                f"post-send telemetry persistence failed: {exc}",
                event_id=eid,
                details={"order_id": order_id},
            )

    if decision.halt:
        try:
            _persist_decision(pre_send=True)
            _persist_transport(
                TransportOutcome(state="not_attempted"), None)
        except TelemetryError:
            pass
        return RailAction(decision=decision, sent=False, dry_run=dry_run,
                          event_id=eid, order_id=order_id,
                          transport_state="not_attempted")

    is_close = decision.signal_type in ("exit", "flat")
    if not is_close and not decision.submit:
        try:
            _persist_decision(pre_send=True)
            _persist_transport(
                TransportOutcome(state="not_attempted"), None)
        except TelemetryError:
            pass
        return RailAction(decision=decision, sent=False, dry_run=dry_run,
                          event_id=eid, order_id=order_id,
                          transport_state="not_attempted")

    leg_id = str(payload["leg_id"])
    symbol = INSTRUMENT_SYMBOLS.get(leg_id)
    if symbol is None:
        raise ValueError(f"no instrument symbol mapped for leg_id {leg_id!r}")

    leg, action = _leg_action(decision.signal_type)
    order_id = _order_id(payload, decision.signal_type)

    payload_text = build_crosstrade_payload(
        leg=leg, action=action, symbol=symbol, qty=decision.qty_out,
        order_id=order_id, account=config["account"],
        secret_key=config["secret_key"], destination=config.get("destination"),
    )

    # Pre-send decision persistence — mandatory for armed risk-add.
    if ledger is not None:
        try:
            _persist_decision(pre_send=True)
        except (TelemetryError, TelemetryUnhealthy) as exc:
            if is_close:
                notifier.notify(
                    "CRITICAL",
                    f"exit/flat decision telemetry write failed (still "
                    f"relaying): {exc}",
                    event_id=eid, details={"order_id": order_id},
                )
            else:
                return RailAction(
                    decision=SizingDecision(
                        leg_id=decision.leg_id,
                        signal_type=decision.signal_type,
                        qty_out=0, submit=False, halt=True,
                        halt_reason=f"telemetry pre-send persist failed: {exc}",
                        leg_key=decision.leg_key,
                    ),
                    sent=False, dry_run=dry_run, event_id=eid,
                    order_id=order_id, transport_state="not_attempted",
                )

    if dry_run:
        _persist_transport(TransportOutcome(state="not_attempted"),
                           payload_text)
        return RailAction(decision=decision, sent=False, dry_run=True,
                          payload_text=payload_text, event_id=eid,
                          order_id=order_id, transport_state="not_attempted")

    result = send_to_crosstrade(
        payload_text, webhook_id=config["webhook_id"],
        webhook_secret=config["webhook_secret"], sender=sender,
    )
    outcome = TransportOutcome(
        state=result.state, http_status=result.http_status, error=result.error)
    _persist_transport(outcome, payload_text)

    if outcome.state == "unknown":
        if ledger is not None:
            ledger.block_risk_add(
                f"transport_unknown for event_id={eid}; reconcile before retry")
        notifier.notify(
            "CRITICAL",
            "transport_unknown after send — no auto-retry; reconcile before "
            "any operator retry",
            event_id=eid,
            details={"order_id": order_id, "error": outcome.error},
        )
        return RailAction(
            decision=decision, sent=False, dry_run=False,
            payload_text=payload_text, http_status=outcome.http_status,
            event_id=eid, order_id=order_id, transport_state="unknown",
        )

    if outcome.state == "failed":
        return RailAction(
            decision=decision, sent=False, dry_run=False,
            payload_text=payload_text, http_status=outcome.http_status,
            event_id=eid, order_id=order_id, transport_state="failed",
        )

    # accepted — HTTP response received; NOT execution verified.
    return RailAction(
        decision=decision, sent=True, dry_run=False,
        payload_text=payload_text, http_status=outcome.http_status,
        event_id=eid, order_id=order_id, transport_state="accepted",
    )
