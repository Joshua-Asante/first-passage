#!/usr/bin/env python3
"""B7 Stage 2b — per-fill add-slippage capture (READ-ONLY).

Joins ``request_received.parsed.close`` with ``BrokerEvidence.fill_price`` by
``event_id``, cohort-splits by ``signal_type``, and compares **add** fills
against the exact panel baselines owned by RUNBOOK §B7 Stage 2b:

  MYM (dj30_mym)  add → close + 1.00 pt  (1 tick)
  MNQ (nas100_mnq) add → close + 0.50 pt  (2 ticks)

Live test per add fill: ``fill_price − parsed.close`` vs those offsets.
Excess above the panel basis is slippage the panel never charged. Actionable
threshold (pre-declared): persistent MYM add excess ≥ 1 tick (−3.0% of MYM
panel net per extra tick). MNQ is near-immune (−0.12%/tick).

This module does NOT:
  - append to the ledger (unlike ``c1_rail_telemetry`` reconcile CLI)
  - place / modify / cancel any order
  - change execution policy (``order_type=market`` stays)
  - buy or propose the declined $19.91 ``mbp-10`` escalation

Owner: docs/notes/rail_build/RUNBOOK.md §B7 Stage 2b ·
       docs/notes/2026-07-24-execution-quality-investigation.md P1.

Usage (in-container, after operator-attested evidence is on disk)::

    python ops/c1_rail/c1_rail_slippage.py \\
        --events /data/c1_rail_events.jsonl \\
        --evidence /data/c1_broker_evidence.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

# Standalone-run bootstrap (same pattern as ops/c1_rail/c1_rail_telemetry.py).
# parents[2] = repo root (this file lives under ops/c1_rail/).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RAIL_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "core"), str(_RAIL_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from c1_rail_telemetry import (  # noqa: E402
    BrokerEvidence,
    EventLedger,
    TelemetryError,
    find_records_for_event,
    load_evidence_overlay,
)

# ── Panel baselines (RUNBOOK §B7 Stage 2b — exact, 100%, zero exceptions) ──

# Index-point offset of panel *add* fills from the signal-bar close.
# Positive = fill above close (long add adverse under TV slippage=1 mintick).
PANEL_ADD_OFFSET_PTS: Mapping[str, float] = {
    "dj30_mym": 1.00,   # 1 MYM tick
    "nas100_mnq": 0.50,  # 2 MNQ ticks
}

# One mintick in index points — used to express excess in ticks.
TICK_SIZE_PTS: Mapping[str, float] = {
    "dj30_mym": 1.00,
    "nas100_mnq": 0.25,
}

# Pre-declared actionable threshold: persistent MYM add excess ≥ 1 tick.
MYM_ADD_EXCESS_TICK_THRESHOLD = 1.0

# Cohorts Stage 2b cares about. Aggregate across these is worthless — the edge
# lives in the adds (63.6% MYM / 87.7% MNQ of panel net).
SIGNAL_COHORTS = frozenset({"entry", "add", "exit", "flat"})


@dataclass(frozen=True)
class FillSlippageRow:
    """One joined fill ready for Stage 2b recording / comparison."""

    event_id: str
    leg_id: str | None
    signal_type: str | None
    close: float | None
    fill_price: float | None
    fill_qty: int | None
    fill_ts: str | None
    tradovate_order_id: str | None
    order_id: str | None
    delta_pts: float | None
    panel_basis_pts: float | None
    excess_pts: float | None
    excess_ticks: float | None
    incomplete_reason: str | None = None

    @property
    def is_complete(self) -> bool:
        return self.incomplete_reason is None

    @property
    def is_add(self) -> bool:
        return self.signal_type == "add"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def panel_add_basis(leg_id: str | None) -> float | None:
    """Return the panel add-fill offset for ``leg_id``, or None if unknown."""
    if leg_id is None:
        return None
    return PANEL_ADD_OFFSET_PTS.get(leg_id)


def tick_size(leg_id: str | None) -> float | None:
    if leg_id is None:
        return None
    return TICK_SIZE_PTS.get(leg_id)


def _first_of_kind(records: Sequence[Mapping[str, Any]], kind: str) -> dict | None:
    for r in records:
        if r.get("kind") == kind:
            return dict(r)
    return None


def _last_of_kind(records: Sequence[Mapping[str, Any]], kind: str) -> dict | None:
    found = None
    for r in records:
        if r.get("kind") == kind:
            found = dict(r)
    return found


def _evidence_for_event(
    event_id: str,
    *,
    ledger_records: Sequence[Mapping[str, Any]],
    overlay: Sequence[BrokerEvidence] | None,
) -> BrokerEvidence | None:
    """Prefer the latest overlay row; fall back to ledger ``broker_evidence``."""
    if overlay:
        matches = [e for e in overlay if e.event_id == event_id]
        if matches:
            return matches[-1]
    ev_rec = _last_of_kind(ledger_records, "broker_evidence")
    if ev_rec is None:
        return None
    return BrokerEvidence.from_dict(ev_rec)


def compute_fill_slippage(
    *,
    event_id: str,
    records: Sequence[Mapping[str, Any]],
    evidence: BrokerEvidence | None,
) -> FillSlippageRow:
    """Join one event's request/decision + evidence into a Stage 2b row.

    Pure. Never touches disk. Incomplete rows carry ``incomplete_reason`` and
    leave comparison fields as None — they are still returned so the operator
    can see what is missing.
    """
    request = _first_of_kind(records, "request_received")
    decision = _first_of_kind(records, "decision")

    parsed = (request or {}).get("parsed") if request else None
    if not isinstance(parsed, Mapping):
        parsed = {}

    leg_id = parsed.get("leg_id")
    if leg_id is None and decision is not None:
        leg_id = decision.get("leg_id")
    signal_type = parsed.get("signal_type")
    if signal_type is None and decision is not None:
        signal_type = decision.get("signal_type")

    close = parsed.get("close")
    if close is not None:
        try:
            close = float(close)
        except (TypeError, ValueError):
            close = None

    order_id = None
    if request is not None:
        order_id = request.get("order_id")
    if order_id is None and decision is not None:
        order_id = decision.get("order_id")
    if order_id is None and evidence is not None:
        order_id = evidence.order_id

    fill_price = evidence.fill_price if evidence else None
    fill_qty = evidence.fill_qty if evidence else None
    fill_ts = evidence.attested_utc if evidence else None
    tradovate_order_id = evidence.tradovate_order_id if evidence else None

    incomplete: str | None = None
    if evidence is None:
        incomplete = "no_broker_evidence"
    elif fill_price is None:
        incomplete = "missing_fill_price"
    elif close is None:
        incomplete = "missing_parsed_close"
    elif signal_type not in SIGNAL_COHORTS:
        incomplete = f"unknown_signal_type:{signal_type!r}"

    delta: float | None = None
    basis: float | None = None
    excess: float | None = None
    excess_ticks: float | None = None

    if incomplete is None:
        assert fill_price is not None and close is not None
        delta = fill_price - close
        # Panel basis applies to the ADD cohort only — that is the Stage 2b
        # pass/fail. Entry/exit rows still carry delta for free recording
        # (execution-quality P1/P2) but leave excess None so they cannot be
        # mistaken for the add gate.
        if signal_type == "add":
            basis = panel_add_basis(leg_id if isinstance(leg_id, str) else None)
            if basis is None:
                incomplete = f"unknown_leg_id:{leg_id!r}"
            else:
                excess = delta - basis
                tick = tick_size(leg_id if isinstance(leg_id, str) else None)
                if tick is not None and tick > 0:
                    excess_ticks = excess / tick

    return FillSlippageRow(
        event_id=event_id,
        leg_id=leg_id if isinstance(leg_id, str) else None,
        signal_type=signal_type if isinstance(signal_type, str) else None,
        close=close,
        fill_price=fill_price,
        fill_qty=fill_qty if isinstance(fill_qty, int) else None,
        fill_ts=fill_ts,
        tradovate_order_id=tradovate_order_id,
        order_id=order_id if isinstance(order_id, str) else None,
        delta_pts=delta,
        panel_basis_pts=basis,
        excess_pts=excess,
        excess_ticks=excess_ticks,
        incomplete_reason=incomplete,
    )


def _event_ids_with_evidence(
    ledger: EventLedger,
    overlay: Sequence[BrokerEvidence] | None,
) -> list[str]:
    """Event ids that have fill-bearing evidence (overlay ∪ ledger)."""
    ids: list[str] = []
    seen: set[str] = set()
    if overlay:
        for e in overlay:
            if e.event_id not in seen and e.fill_price is not None:
                seen.add(e.event_id)
                ids.append(e.event_id)
    for rec in ledger.iter_records():
        if rec.get("kind") != "broker_evidence":
            continue
        eid = rec.get("event_id")
        if not isinstance(eid, str) or eid in seen:
            continue
        if rec.get("fill_price") is None:
            continue
        seen.add(eid)
        ids.append(eid)
    return ids


def collect_fill_slippage(
    ledger: EventLedger,
    *,
    overlay: Sequence[BrokerEvidence] | None = None,
    event_ids: Sequence[str] | None = None,
) -> list[FillSlippageRow]:
    """Build Stage 2b rows for every evidenced fill (or an explicit id list).

    Read-only: never appends. When ``event_ids`` is omitted, scans for events
    that carry a ``fill_price`` in the overlay or ledger.
    """
    targets = list(event_ids) if event_ids is not None else _event_ids_with_evidence(
        ledger, overlay
    )
    rows: list[FillSlippageRow] = []
    for eid in targets:
        records = find_records_for_event(ledger, eid)
        if not records and event_ids is not None:
            # Explicit id with no rail record — still surface incompleteness.
            evidence = None
            if overlay:
                matches = [e for e in overlay if e.event_id == eid]
                evidence = matches[-1] if matches else None
            rows.append(
                FillSlippageRow(
                    event_id=eid,
                    leg_id=None,
                    signal_type=None,
                    close=None,
                    fill_price=evidence.fill_price if evidence else None,
                    fill_qty=evidence.fill_qty if evidence else None,
                    fill_ts=evidence.attested_utc if evidence else None,
                    tradovate_order_id=(
                        evidence.tradovate_order_id if evidence else None
                    ),
                    order_id=evidence.order_id if evidence else None,
                    delta_pts=None,
                    panel_basis_pts=None,
                    excess_pts=None,
                    excess_ticks=None,
                    incomplete_reason="no_rail_records",
                )
            )
            continue
        evidence = _evidence_for_event(eid, ledger_records=records, overlay=overlay)
        rows.append(
            compute_fill_slippage(
                event_id=eid, records=records, evidence=evidence
            )
        )
    return rows


def summarize_by_cohort(
    rows: Iterable[FillSlippageRow],
) -> dict[str, Any]:
    """Cohort-split summary. Aggregate-only views are deliberately absent."""
    by_key: dict[tuple[str, str], list[FillSlippageRow]] = {}
    incomplete: list[FillSlippageRow] = []
    for row in rows:
        if not row.is_complete:
            incomplete.append(row)
            continue
        leg = row.leg_id or "<unknown>"
        sig = row.signal_type or "<unknown>"
        by_key.setdefault((leg, sig), []).append(row)

    cohorts: list[dict[str, Any]] = []
    for (leg, sig), group in sorted(by_key.items()):
        deltas = [r.delta_pts for r in group if r.delta_pts is not None]
        excesses = [r.excess_pts for r in group if r.excess_pts is not None]
        cell: dict[str, Any] = {
            "leg_id": leg,
            "signal_type": sig,
            "n": len(group),
            "delta_pts_median": _median(deltas),
            "delta_pts_mean": (sum(deltas) / len(deltas)) if deltas else None,
        }
        if sig == "add":
            basis = panel_add_basis(leg)
            cell["panel_basis_pts"] = basis
            cell["excess_pts_median"] = _median(excesses)
            cell["excess_pts_mean"] = (
                (sum(excesses) / len(excesses)) if excesses else None
            )
            tick_excesses = [
                r.excess_ticks for r in group if r.excess_ticks is not None
            ]
            cell["excess_ticks_median"] = _median(tick_excesses)
            if leg == "dj30_mym" and excesses:
                # Informational flag only — n=1 is not evidence (RUNBOOK).
                cell["mym_add_excess_ge_1_tick"] = any(
                    (r.excess_ticks or 0.0) >= MYM_ADD_EXCESS_TICK_THRESHOLD
                    for r in group
                )
        cohorts.append(cell)

    return {
        "n_rows": sum(c["n"] for c in cohorts) + len(incomplete),
        "n_complete": sum(c["n"] for c in cohorts),
        "n_incomplete": len(incomplete),
        "cohorts": cohorts,
        "incomplete": [r.to_dict() for r in incomplete],
    }


def _median(values: Sequence[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def format_report(rows: Sequence[FillSlippageRow], summary: Mapping[str, Any]) -> str:
    """Human-readable desk report — cohort-split, never aggregate-only."""
    lines: list[str] = []
    lines.append("=== c1 Stage 2b fill-slippage (READ-ONLY) ===")
    lines.append(
        f"rows={summary['n_rows']} complete={summary['n_complete']} "
        f"incomplete={summary['n_incomplete']}"
    )
    lines.append("")
    lines.append(
        "per-fill: event_id · leg_id · signal_type · close · fill_price · "
        "fill_qty · fill_ts · tradovate_order_id · delta_pts · excess_pts"
    )
    for row in rows:
        if row.is_complete:
            lines.append(
                f"  {row.event_id}  {row.leg_id}  {row.signal_type}  "
                f"close={row.close}  fill={row.fill_price}  qty={row.fill_qty}  "
                f"ts={row.fill_ts}  tv={row.tradovate_order_id}  "
                f"delta={row.delta_pts:+.4f}"
                + (
                    f"  excess={row.excess_pts:+.4f}"
                    if row.excess_pts is not None
                    else ""
                )
            )
        else:
            lines.append(
                f"  {row.event_id}  INCOMPLETE ({row.incomplete_reason})  "
                f"leg={row.leg_id}  signal={row.signal_type}  "
                f"close={row.close}  fill={row.fill_price}"
            )
    lines.append("")
    lines.append("cohort summary (split mandatory — no aggregate):")
    for cell in summary["cohorts"]:
        line = (
            f"  {cell['leg_id']}/{cell['signal_type']}: n={cell['n']}  "
            f"delta_med={cell['delta_pts_median']}"
        )
        if cell["signal_type"] == "add":
            line += (
                f"  basis={cell.get('panel_basis_pts')}  "
                f"excess_med={cell.get('excess_pts_median')}  "
                f"excess_ticks_med={cell.get('excess_ticks_median')}"
            )
            if "mym_add_excess_ge_1_tick" in cell:
                line += f"  flag_ge_1tick={cell['mym_add_excess_ge_1_tick']}"
        lines.append(line)
    lines.append("")
    lines.append(
        "Standing constraints: keep order_type=market; do not buy mbp-10 on "
        "n=1; MYM add excess ≥1 tick is the actionable signal (persistent)."
    )
    return "\n".join(lines)


def _cli(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "c1 Stage 2b per-fill add-slippage capture. READ-ONLY — never "
            "appends to the ledger, never places or cancels an order."
        )
    )
    ap.add_argument("--events", type=Path, required=True,
                    help="path to c1_rail_events.jsonl")
    ap.add_argument(
        "--evidence", type=Path, default=None,
        help="optional operator-attested BrokerEvidence JSONL overlay",
    )
    ap.add_argument(
        "--event-id", action="append", default=None,
        help="restrict to one or more event_ids (repeatable); default=all "
             "evidenced fills",
    )
    ap.add_argument(
        "--json", action="store_true",
        help="emit machine-readable JSON (rows + cohort summary)",
    )
    args = ap.parse_args(argv)

    if not args.events.exists():
        raise SystemExit(f"events ledger not found: {args.events}")

    try:
        ledger = EventLedger(args.events)
    except TelemetryError as exc:
        raise SystemExit(f"ledger error: {exc}") from exc

    overlay = load_evidence_overlay(args.evidence) if args.evidence else None
    rows = collect_fill_slippage(
        ledger, overlay=overlay, event_ids=args.event_id
    )
    summary = summarize_by_cohort(rows)

    if args.json:
        print(json.dumps(
            {"rows": [r.to_dict() for r in rows], "summary": summary},
            indent=2, sort_keys=True,
        ))
    else:
        print(format_report(rows, summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
