#!/usr/bin/env python3
"""M1 §4 item 5 capture helper — non-zero admitted-leg dry_run strategy entry.

Operator-owned evidence: a REAL TV strategy signal with expected (non-zero)
sizing. This script never invents that evidence. It:

  1. Reads a host ledger dump (c1_rail_events.jsonl).
  2. Finds / evaluates an admitted-leg entry triad for item-5 fitness
     (`ITEM5_LEGS = dj30_mym, nas100_mnq` — widened 2026-08-02 on operator
     direction; see L42-50).
  3. Decodes bar_time for the §2b mid-bar re-measurement.
  4. Optionally writes dry_run_strategy_signal_event_id into the acceptance
     artifact — and only flips status=RESOLVED when the operator also
     supplies --operator + --confirm-resolved.

Refuse paths (exit 2): qty 0 / floored, leg not in `ITEM5_LEGS`, non-entry,
incomplete triad, armed/live send, missing parsed fields, ledger arithmetic mismatch.

Usage (PowerShell — dump then analyze):

  powershell -File scripts/m1_item5_dump.ps1
  python scripts/m1_item5_capture.py $env:TEMP\\m1_item5\\c1_rail_events.jsonl --latest

Desk cards: docs/notes/rail_build/B7_STAGE1_DESK_CARD_*.md — read the **LATEST by date**; every earlier card is stamped SPENT in its own header. ⚠ As of 2026-08-04 the entire B7 Stage-1 queue is **MOOTED** by the venue de-scope — do not run any card, and do not arm, without a fresh operator GO under fork F2/F3.
ADR: docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md §4 item 5
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

LEG_MYM = "dj30_mym"
LEG_MNQ = "nas100_mnq"
# Item 5 is LEG-AGNOSTIC by its own text ("from a REAL TV strategy entry, not a
# canned payload" -- no leg named), and a real MNQ entry DID write the full triad
# on 2026-07-28. It failed on qty_out=0, NOT on being MNQ. This script previously
# hard-required dj30_mym, which locked M1 to MYM in tooling where the acceptance
# artifact does not. Widened 2026-08-02 on operator direction ("I do not want to
# lock M1 to Striker MYM specifically"). EVERY substantive guard is unchanged --
# b1_json, signal_type=entry, dry_run, not-floored and qty_out > 0 all still bind,
# and they are what actually rejected the 07-28 event.
ITEM5_LEGS = (LEG_MYM, LEG_MNQ)
ET = timezone(timedelta(hours=-4))  # US Eastern, fixed offset (no DST table)

# Desk-card §1: qty 8 at stop <= 87.50; qty 7 strictly above (floor(700/stop)).
MYM_ENTRY_QTY_CLIFF_PTS = 87.50

AUDIT_REJECT_RE = re.compile(r"non-JSON|non-object")


@dataclass
class Triad:
    event_id: str
    request: dict[str, Any]
    decision: dict[str, Any]
    transport: dict[str, Any]


@dataclass
class Verdict:
    ok: bool
    event_id: str | None
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    triad: Triad | None = None
    bar_open_utc: str | None = None
    bar_open_et: str | None = None
    bar_close_et: str | None = None
    parsed_close: float | None = None
    stop_dist_pts: float | None = None
    qty_out: int | None = None
    expected_band_qty: int | None = None
    close_delta: float | None = None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load JSONL; skip blank lines and non-JSON noise (fly ssh Windows trailer)."""
    rows: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    return rows


def index_triads(events: list[dict[str, Any]]) -> dict[str, Triad]:
    by_id: dict[str, dict[str, dict[str, Any]]] = {}
    for ev in events:
        eid = ev.get("event_id")
        kind = ev.get("kind")
        if not isinstance(eid, str) or not isinstance(kind, str):
            continue
        by_id.setdefault(eid, {})[kind] = ev
    out: dict[str, Triad] = {}
    for eid, kinds in by_id.items():
        req, dec, tr = (
            kinds.get("request_received"),
            kinds.get("decision"),
            kinds.get("transport_result"),
        )
        if req and dec and tr:
            out[eid] = Triad(event_id=eid, request=req, decision=dec, transport=tr)
    return out


def decode_bar_time(bar_time: Any) -> tuple[datetime, datetime]:
    """Pine time is bar-open epoch ms UTC -> (utc, et)."""
    if isinstance(bar_time, str) and bar_time.endswith("Z"):
        utc = datetime.fromisoformat(bar_time.replace("Z", "+00:00"))
    else:
        ms = int(bar_time)
        utc = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
    return utc, utc.astimezone(ET)


def expected_mym_entry_qty(stop_dist_pts: float) -> int | None:
    if 30.0 <= stop_dist_pts <= MYM_ENTRY_QTY_CLIFF_PTS:
        return 8
    if MYM_ENTRY_QTY_CLIFF_PTS < stop_dist_pts <= 100.0:
        return 7
    return None


def _reproduce_qty(decision: dict[str, Any]) -> tuple[int | None, list[str]]:
    """Recompute qty_out from the decision's own arithmetic fields."""
    errs: list[str] = []
    try:
        risk = float(decision["risk_dollars"])
        per = float(decision["per_contract"])
        reserve = int(decision["reserve_cap"])
        raw = int(decision["qty_base_raw"])
        out = int(decision["qty_out"])
    except (KeyError, TypeError, ValueError) as exc:
        return None, [f"decision missing arithmetic fields: {exc}"]

    if per <= 0:
        return None, ["per_contract must be > 0"]
    expect_raw = math.floor(risk / per)
    if raw != expect_raw:
        errs.append(
            f"qty_base_raw {raw} != floor(risk_dollars/per_contract)={expect_raw}"
        )
    expect_out = min(expect_raw, reserve)
    if out != expect_out:
        errs.append(
            f"qty_out {out} != min(qty_base_raw, reserve_cap)={expect_out}"
        )
    return expect_out, errs


def evaluate_triad(
    triad: Triad,
    *,
    confirmed_close: float | None = None,
    require_dry_run: bool = True,
) -> Verdict:
    v = Verdict(ok=False, event_id=triad.event_id, triad=triad)
    req, dec, tr = triad.request, triad.decision, triad.transport
    parsed = req.get("parsed") or {}

    if req.get("body_category") != "b1_json":
        v.reasons.append(
            f"body_category={req.get('body_category')!r} (need b1_json)"
        )
    _leg = parsed.get("leg_id") or dec.get("leg_id")
    if _leg not in ITEM5_LEGS:
        v.reasons.append(
            f"leg_id={_leg!r} (need one of {', '.join(ITEM5_LEGS)})"
        )
    if parsed.get("signal_type") != "entry" and dec.get("signal_type") != "entry":
        v.reasons.append(
            f"signal_type={parsed.get('signal_type') or dec.get('signal_type')!r} "
            "(need entry)"
        )

    close = parsed.get("close")
    stop = parsed.get("stop_dist_pts")
    if close is None or stop is None:
        v.reasons.append("parsed.close / parsed.stop_dist_pts missing")
    else:
        try:
            v.parsed_close = float(close)
            v.stop_dist_pts = float(stop)
        except (TypeError, ValueError):
            v.reasons.append("parsed.close / stop_dist_pts not numeric")

    bar_time = parsed.get("bar_time")
    if bar_time is None:
        v.reasons.append("parsed.bar_time missing")
    else:
        try:
            utc, et = decode_bar_time(bar_time)
            v.bar_open_utc = utc.isoformat()
            v.bar_open_et = et.isoformat()
            # Pine time = bar open; confirmed C is available after open+15m.
            v.bar_close_et = (et + timedelta(minutes=15)).isoformat()
        except (TypeError, ValueError, OSError) as exc:
            v.reasons.append(f"bar_time decode failed: {exc}")

    if dec.get("halt") is not False:
        v.reasons.append(f"halt={dec.get('halt')!r} (need false)")
    try:
        qty = int(dec["qty_out"])
        v.qty_out = qty
    except (KeyError, TypeError, ValueError):
        v.reasons.append("decision.qty_out missing/non-int")
        qty = None

    if qty is not None and qty <= 0:
        v.reasons.append(
            f"qty_out={qty} — floored/zero is deliberately NOT item-5 evidence "
            "(07-28 MNQ class; desk card)"
        )
    if dec.get("floored") is True and (qty is None or qty <= 0):
        v.reasons.append("floored=true with non-positive qty")

    if require_dry_run:
        if dec.get("dry_run") is not True:
            v.reasons.append(f"decision.dry_run={dec.get('dry_run')!r} (need true)")
        if tr.get("dry_run") is not True:
            v.reasons.append(f"transport.dry_run={tr.get('dry_run')!r} (need true)")
        if tr.get("transport_state") != "not_attempted":
            v.reasons.append(
                f"transport_state={tr.get('transport_state')!r} "
                "(dry_run expect not_attempted)"
            )

    if tr.get("execution_verified") is True:
        v.reasons.append(
            "execution_verified=true — refuse (item 5 is dry_run evidence)"
        )

    if qty is not None and qty > 0:
        expect_out, arith_errs = _reproduce_qty(dec)
        v.reasons.extend(arith_errs)
        if v.stop_dist_pts is not None:
            if _leg == LEG_MYM:
                band = expected_mym_entry_qty(v.stop_dist_pts)
                v.expected_band_qty = band
                if band is None:
                    v.warnings.append(
                        f"stop_dist_pts={v.stop_dist_pts} outside desk-card bands "
                        f"(30-100 pts @ peak DD); check DD_SCALE / lifecycle"
                    )
                elif expect_out is not None and expect_out != band:
                    v.warnings.append(
                        f"ledger qty {expect_out} != desk-card band qty {band} "
                        f"at stop {v.stop_dist_pts} — STOP if unexplained"
                    )
                elif qty != band and band is not None:
                    v.warnings.append(
                        f"qty_out {qty} != desk-card band {band} at stop "
                        f"{v.stop_dist_pts}"
                    )
            elif _leg == LEG_MNQ:
                v.warnings.append(
                    "MNQ item-5 sizing: reserve_cap=1 at the rail host — "
                    "MYM desk-card band check not applicable (non-alarm)"
                )

    if confirmed_close is not None and v.parsed_close is not None:
        v.close_delta = confirmed_close - v.parsed_close
        if v.close_delta == 0:
            v.warnings.append(
                "section 2b: confirmed C == parsed.close — benign (fired at/after close)"
            )
        else:
            v.warnings.append(
                f"section 2b: confirmed C - parsed.close = {v.close_delta:+.4g} — "
                "signal-identity divergence; escalate per desk card (does not "
                "block item-5 record)"
            )

    v.ok = len(v.reasons) == 0
    return v


def find_candidates(triads: dict[str, Triad]) -> list[Verdict]:
    """All admitted-leg entry triads, scored; passing ones first, then by seq."""
    scored: list[Verdict] = []
    for triad in triads.values():
        leg = (triad.request.get("parsed") or {}).get("leg_id") or triad.decision.get(
            "leg_id"
        )
        sig = (triad.request.get("parsed") or {}).get(
            "signal_type"
        ) or triad.decision.get("signal_type")
        if leg not in ITEM5_LEGS or sig != "entry":
            continue
        scored.append(evaluate_triad(triad))
    scored.sort(key=lambda v: (not v.ok, -(v.triad.decision.get("seq") or 0)))
    return scored


def preflight_audit(
    events: list[dict[str, Any]], audit_text: str
) -> tuple[bool, list[str]]:
    """§0.1 — any audit reject after the latest b1_json arrival?"""
    last_b1_ts: str | None = None
    for ev in events:
        if (
            ev.get("kind") == "request_received"
            and ev.get("body_category") == "b1_json"
        ):
            ts = ev.get("ts_utc")
            if isinstance(ts, str) and (last_b1_ts is None or ts > last_b1_ts):
                last_b1_ts = ts

    msgs: list[str] = []
    if last_b1_ts is None:
        msgs.append("no b1_json in events dump — section 0.4 same-session proof still owed")
        return False, msgs

    msgs.append(f"latest b1_json ts_utc={last_b1_ts}")
    hits_after: list[str] = []
    for line in audit_text.splitlines():
        if not AUDIT_REJECT_RE.search(line):
            continue
        m = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
        if not m:
            continue
        audit_ts = m.group(1).replace(" ", "T")
        b1_cmp = last_b1_ts[:19]
        if audit_ts > b1_cmp:
            hits_after.append(line.strip())

    if hits_after:
        msgs.append(f"BLOCKING: {len(hits_after)} reject(s) after latest b1_json:")
        msgs.extend(f"  {h}" for h in hits_after[-10:])
        return False, msgs

    msgs.append("section 0.1 CLEAN — no non-JSON/non-object after latest b1_json")
    return True, msgs


def write_acceptance(
    path: Path,
    *,
    event_id: str,
    operator: str | None,
    confirm_resolved: bool,
    verdict: Verdict,
) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    notes: list[str] = []

    existing = data.get("dry_run_strategy_signal_event_id")
    if existing and existing != event_id:
        raise SystemExit(
            f"acceptance already has dry_run_strategy_signal_event_id={existing!r}; "
            f"refusing to overwrite with {event_id!r}"
        )

    data["dry_run_strategy_signal_event_id"] = event_id
    notes.append(f"set dry_run_strategy_signal_event_id={event_id}")

    note_line = (
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')} — M1 §4 item 5 "
        f"RECORDED via m1_item5_capture.py: event_id={event_id}, "
        f"qty_out={verdict.qty_out}, stop_dist_pts={verdict.stop_dist_pts}, "
        f"parsed.close={verdict.parsed_close}, "
        f"bar_open_et={verdict.bar_open_et}. "
        f"dry_run=true throughout. "
        + (
            f"section 2b close_delta={verdict.close_delta}."
            if verdict.close_delta is not None
            else "section 2b confirmed-close not supplied at write time."
        )
    )
    data.setdefault("notes", [])
    if note_line not in data["notes"]:
        data["notes"].insert(3, note_line)

    if confirm_resolved:
        if not operator:
            raise SystemExit("--confirm-resolved requires --operator")
        _t = verdict.triad
        _leg = (
            ((_t.request.get("parsed") or {}).get("leg_id") or _t.decision.get("leg_id"))
            if _t
            else None
        )
        if _leg not in ITEM5_LEGS:
            raise SystemExit(
                f"refusing sign-off: leg_id={_leg!r} not in {ITEM5_LEGS}"
            )
        data["operator_signoff"] = {
            "operator": operator,
            "signed_utc": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "note": (
                f"M1 §4 item 5 non-zero {_leg} dry_run strategy entry + prior "
                "items 6/10/drills."
            ),
        }
        data["status"] = "RESOLVED"
        notes.append(f"status=RESOLVED; operator_signoff.operator={operator}")
    else:
        notes.append("status unchanged (pass --confirm-resolved to flip RESOLVED)")

    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return notes


def _print_verdict(v: Verdict) -> None:
    status = "PASS" if v.ok else "FAIL"
    print(f"{status} event_id={v.event_id}")
    if v.qty_out is not None:
        print(
            f"  qty_out={v.qty_out}  stop_dist_pts={v.stop_dist_pts}  "
            f"parsed.close={v.parsed_close}"
        )
    if v.expected_band_qty is not None:
        print(f"  desk-card band qty={v.expected_band_qty}")
    if v.bar_open_et:
        print(
            f"  bar open ET={v.bar_open_et}  "
            f"(confirmed C readable after {v.bar_close_et})"
        )
    if v.close_delta is not None:
        print(f"  section 2b close_delta={v.close_delta:+.4g}")
    for r in v.reasons:
        print(f"  REASON: {r}")
    for w in v.warnings:
        print(f"  WARN: {w}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "events",
        type=Path,
        help="Local dump of /data/c1_rail_events.jsonl",
    )
    ap.add_argument("--event-id", help="Evaluate a specific event_id")
    ap.add_argument(
        "--latest",
        action="store_true",
        help="Evaluate the newest admitted-leg entry candidate (PASS preferred)",
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="List all admitted-leg entry triads with PASS/FAIL",
    )
    ap.add_argument(
        "--confirmed-close",
        type=float,
        help="Chart-confirmed Close of the signal bar (§2b)",
    )
    ap.add_argument(
        "--allow-live",
        action="store_true",
        help="Do not require dry_run=true (emergency only; default refuses)",
    )
    ap.add_argument(
        "--write-acceptance",
        type=Path,
        metavar="PATH",
        help="Write dry_run_strategy_signal_event_id into acceptance JSON",
    )
    ap.add_argument(
        "--operator",
        help="operator_signoff.operator (required with --confirm-resolved)",
    )
    ap.add_argument(
        "--confirm-resolved",
        action="store_true",
        help="Also set operator_signoff + status=RESOLVED",
    )
    ap.add_argument(
        "--audit-log",
        type=Path,
        help="Local dump of /data/c1_rail_audit.log (for --preflight)",
    )
    ap.add_argument(
        "--preflight",
        action="store_true",
        help="Run §0.1 audit check against events + --audit-log",
    )
    args = ap.parse_args(argv)

    events = load_jsonl(args.events)
    triads = index_triads(events)

    if args.preflight:
        if not args.audit_log:
            print("--preflight requires --audit-log", file=sys.stderr)
            return 2
        ok, msgs = preflight_audit(
            events, args.audit_log.read_text(encoding="utf-8", errors="replace")
        )
        for m in msgs:
            print(m)
        return 0 if ok else 2

    if args.list or (not args.event_id and not args.latest):
        cands = find_candidates(triads)
        if not cands:
            print("No admitted-leg entry triads in dump "
                  f"({', '.join(ITEM5_LEGS)}).")
            print(
                "NOTE: no source event can exist at this venue since the 2026-08-04 de-scope; "
                "item 5 is **undischargeable here, not merely pending**. See forks F2 and F3, "
                "both 2026-08-08."
            )
            return 1
        for v in cands:
            _print_verdict(v)
            print()
        passing = [v for v in cands if v.ok]
        print(f"{len(passing)}/{len(cands)} admitted-leg entry triad(s) PASS item-5 gates")
        if not args.event_id and not args.latest and not args.write_acceptance:
            return 0 if passing else 1

    target_id = args.event_id
    if args.latest and not target_id:
        cands = find_candidates(triads)
        if not cands:
            print("No admitted-leg entry triads.", file=sys.stderr)
            return 1
        passing = [v for v in cands if v.ok]
        target_id = (passing[0] if passing else cands[0]).event_id

    if not target_id:
        return 0

    triad = triads.get(target_id)
    if triad is None:
        print(f"event_id={target_id!r} has no complete triad", file=sys.stderr)
        return 2

    verdict = evaluate_triad(
        triad,
        confirmed_close=args.confirmed_close,
        require_dry_run=not args.allow_live,
    )
    _print_verdict(verdict)

    if not verdict.ok:
        print(
            "\nREFUSING write — fix reasons above. "
            "A qty-0/floored event must NOT populate "
            "dry_run_strategy_signal_event_id.",
            file=sys.stderr,
        )
        return 2

    if args.write_acceptance:
        notes = write_acceptance(
            args.write_acceptance,
            event_id=target_id,
            operator=args.operator,
            confirm_resolved=args.confirm_resolved,
            verdict=verdict,
        )
        for n in notes:
            print(f"WRITE: {n}")
        validator = REPO_ROOT / "scripts" / "validate_c1_monitoring_acceptance.py"
        if validator.is_file():
            cmd = [sys.executable, str(validator), str(args.write_acceptance)]
            if args.confirm_resolved:
                cmd.append("--require-resolved")
            proc = subprocess.run(cmd, check=False)
            if proc.returncode != 0:
                return proc.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
