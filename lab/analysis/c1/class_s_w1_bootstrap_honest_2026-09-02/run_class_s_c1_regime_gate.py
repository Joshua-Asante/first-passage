"""Class-S candidate #1 regime-robustness rider (gate §7(7) / candidate §6).

Runs the methodology regime gate
(``docs/methodology/regime_robustness_gate.md``) on the C1 scaled MYM+MNQ book
**before trusting DISCHARGED into G8 intake**.

Floor = frozen Part A ceilings (bust ≤ 3.0%, P(pass) ≥ 50%), not FXIFY lock gates.
Geometry = Run-2 on the two discharge tiers (Tradeify_Select_100K, MFFU_Rapid_100K).

Semantics (candidate §6): a both-halves FAIL does **not** overturn mechanical Part A
DISCHARGED — it rides into G8 as a standing caveat.

Does NOT switch ``ACTIVE_FIRM``. Reuses panel construction from
``run_class_s_c1_scoring.py`` and MC primitives from
``lab/discovery/prop_survivor_scoring.py``.

Exit codes:
  0 — gate completed; REGIME_GATE.md written (PASS or FAIL)
  2 — NEEDS_CONTEXT (missing/mismatched panel bytes or 1R guard)
  3 — Phase-0 signature / ACTIVE_FIRM / pre-reg intactness failure
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_CORE = _ROOT / "core"
_LAB = _ROOT / "lab"
for _p in (_CORE, _LAB, str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from firm_rules import FIRM_RULES  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    blocks_from_daily_pnl,
    load_scoring_thresholds,
    run_tier_remc,
    score_part_a,
)

# Import sibling adapter helpers (panel + Phase-0) — same process, not a package.
from run_class_s_c1_scoring import (  # noqa: E402
    C1_ALLOCS,
    C1_STRATS,
    EXPECTED_1R,
    GATE_PREREG,
    PANEL_FILES,
    NeedsContext,
    Phase0Error,
    book_daily_at_100k,
    build_scaled_panel,
    phase0_verify,
    resolve_panel_path,
)

try:
    from joblib import Parallel, delayed

    _HAS_JOBLIB = True
except ImportError:  # pragma: no cover
    _HAS_JOBLIB = False

DISCHARGE_TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
BLOCK_SIZE_BDAYS = 126  # ~6 months contiguous blocks
N_PANELS_DEFAULT = 100
BOOT_SEED = 20260715
SMOKE_N_PANELS = 5
SMOKE_N_SIMS = 200


def _consistency_frac(firm_key: str) -> float | None:
    raw = FIRM_RULES[firm_key].get("consistency_rule_pct")
    if raw is None:
        return None
    return float(raw) / 100.0


def run_partition_mc(
    daily_100k: np.ndarray,
    firm_key: str,
    thr,
    *,
    n_sims: int | None = None,
) -> dict:
    """Run-2 (consistency-on where present) headline bust/pass on a daily series."""
    blocks = blocks_from_daily_pnl(daily_100k)
    cons = _consistency_frac(firm_key)
    # Run-2 gate: consistency-on when the firm has a consistency rule.
    run = run_tier_remc(
        firm_key, blocks, thr, n_sims=n_sims, consistency=cons
    )
    clears = score_part_a(run, thr)
    return {
        "firm_key": firm_key,
        "consistency": cons,
        "n_sims": run["n_sims"],
        "headline_bust": float(run["headline_bust"]),
        "pass_rate": float(run["pass_rate"]),
        "clears_part_a": bool(clears),
        "gated_on": "run2" if cons is not None else "run1_degenerate",
    }


def _floor_ok(result: dict, thr) -> bool:
    return (
        float(result["headline_bust"]) <= thr.eval_bust_ceiling
        and float(result["pass_rate"]) >= thr.pass_floor
    )


def half_panel_split(daily_100k: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """Split at business-day midpoint (Part B). Index positions, not calendar labels."""
    n = int(daily_100k.size)
    mid = n // 2
    return daily_100k[:mid].copy(), daily_100k[mid:].copy(), mid


def part_b_half_panel(
    daily_100k: np.ndarray,
    thr,
    *,
    n_sims: int | None = None,
    tiers: Sequence[str] = DISCHARGE_TIERS,
) -> dict:
    h1, h2, mid = half_panel_split(daily_100k)
    out: dict = {
        "mid_index": mid,
        "h1_n_bdays": int(h1.size),
        "h2_n_bdays": int(h2.size),
        "tiers": {},
    }
    for firm_key in tiers:
        print(f"[regime] Part B {firm_key} H1 ({h1.size} bd) ...", flush=True)
        r1 = run_partition_mc(h1, firm_key, thr, n_sims=n_sims)
        print(f"[regime] Part B {firm_key} H2 ({h2.size} bd) ...", flush=True)
        r2 = run_partition_mc(h2, firm_key, thr, n_sims=n_sims)
        ok1 = _floor_ok(r1, thr)
        ok2 = _floor_ok(r2, thr)
        out["tiers"][firm_key] = {
            "H1": {**r1, "floor_ok": ok1},
            "H2": {**r2, "floor_ok": ok2},
            "half_panel_ok": bool(ok1 and ok2),
        }
        print(
            f"[regime]   H1 bust={r1['headline_bust']:.2%} pass={r1['pass_rate']:.2%} "
            f"{'PASS' if ok1 else 'FAIL'} | "
            f"H2 bust={r2['headline_bust']:.2%} pass={r2['pass_rate']:.2%} "
            f"{'PASS' if ok2 else 'FAIL'}",
            flush=True,
        )
    return out


def _make_alt_panel(
    vals: np.ndarray,
    *,
    target_len: int,
    block_size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    n_avail = target_len - block_size + 1
    if n_avail < 1:
        raise ValueError(
            f"panel too short for block bootstrap: len={target_len} block={block_size}"
        )
    sampled: list[np.ndarray] = []
    tot = 0
    while tot < target_len:
        st = int(rng.integers(0, n_avail))
        blk = vals[st : st + block_size]
        sampled.append(blk)
        tot += len(blk)
    return np.concatenate(sampled)[:target_len]


def _boot_one(
    pid: int,
    vals: np.ndarray,
    target_len: int,
    block_size: int,
    boot_seed: int,
    firm_key: str,
    thr,
    n_sims: int | None,
) -> dict:
    # Independent RNG stream per panel id (reproducible under parallel).
    rng = np.random.default_rng(boot_seed + pid * 1_000_003)
    alt = _make_alt_panel(vals, target_len=target_len, block_size=block_size, rng=rng)
    return run_partition_mc(alt, firm_key, thr, n_sims=n_sims)


def part_a_bootstrap(
    daily_100k: np.ndarray,
    thr,
    *,
    n_panels: int = N_PANELS_DEFAULT,
    block_size: int = BLOCK_SIZE_BDAYS,
    boot_seed: int = BOOT_SEED,
    n_sims: int | None = None,
    tiers: Sequence[str] = DISCHARGE_TIERS,
    n_jobs: int = -1,
) -> dict:
    vals = np.asarray(daily_100k, dtype=float).reshape(-1)
    target_len = int(vals.size)
    out: dict = {
        "n_panels": int(n_panels),
        "block_size_bdays": int(block_size),
        "boot_seed": int(boot_seed),
        "tiers": {},
    }
    for firm_key in tiers:
        print(
            f"[regime] Part A bootstrap {firm_key} n={n_panels} "
            f"block={block_size}bd ...",
            flush=True,
        )
        t0 = time.time()
        if _HAS_JOBLIB and n_jobs != 1 and n_panels > 1:
            results = Parallel(n_jobs=n_jobs, prefer="processes")(
                delayed(_boot_one)(
                    pid,
                    vals,
                    target_len,
                    block_size,
                    boot_seed,
                    firm_key,
                    thr,
                    n_sims,
                )
                for pid in range(n_panels)
            )
        else:
            results = []
            for pid in range(n_panels):
                results.append(
                    _boot_one(
                        pid,
                        vals,
                        target_len,
                        block_size,
                        boot_seed,
                        firm_key,
                        thr,
                        n_sims,
                    )
                )
                if (pid + 1) % 20 == 0 or (pid + 1) == n_panels:
                    el = time.time() - t0
                    rem = el * n_panels / (pid + 1) - el
                    print(
                        f"[regime]   bootstrap {pid + 1}/{n_panels} "
                        f"({el:.0f}s, est rem {rem:.0f}s)",
                        flush=True,
                    )
        passes = np.array([r["pass_rate"] for r in results], dtype=float)
        busts = np.array([r["headline_bust"] for r in results], dtype=float)
        pass_5th = float(np.percentile(passes, 5))
        bust_95th = float(np.percentile(busts, 95))
        boot_ok = (
            pass_5th >= thr.pass_floor and bust_95th <= thr.eval_bust_ceiling
        )
        out["tiers"][firm_key] = {
            "pass_5th": pass_5th,
            "pass_mean": float(passes.mean()),
            "bust_95th": bust_95th,
            "bust_mean": float(busts.mean()),
            "bootstrap_ok": bool(boot_ok),
            "wall_s": float(time.time() - t0),
            "panels": [
                {
                    "headline_bust": r["headline_bust"],
                    "pass_rate": r["pass_rate"],
                    "clears_part_a": r["clears_part_a"],
                }
                for r in results
            ],
        }
        print(
            f"[regime]   pass 5th={pass_5th:.2%} mean={passes.mean():.2%} | "
            f"bust 95th={bust_95th:.2%} mean={busts.mean():.2%} -> "
            f"{'PASS' if boot_ok else 'FAIL'}",
            flush=True,
        )
    return out


def full_panel_reference(
    daily_100k: np.ndarray,
    thr,
    *,
    n_sims: int | None = None,
    tiers: Sequence[str] = DISCHARGE_TIERS,
) -> dict:
    out = {}
    for firm_key in tiers:
        print(f"[regime] full-panel reference {firm_key} ...", flush=True)
        r = run_partition_mc(daily_100k, firm_key, thr, n_sims=n_sims)
        out[firm_key] = {**r, "floor_ok": _floor_ok(r, thr)}
        print(
            f"[regime]   bust={r['headline_bust']:.2%} pass={r['pass_rate']:.2%} "
            f"{'PASS' if out[firm_key]['floor_ok'] else 'FAIL'}",
            flush=True,
        )
    return out


def compose_verdict(full: dict, half: dict, boot: dict, thr) -> dict:
    """Per-tier and overall GATE PASS iff bootstrap + H1 + H2 all clear floors."""
    tiers = {}
    all_ok = True
    for firm_key in DISCHARGE_TIERS:
        h = half["tiers"][firm_key]
        b = boot["tiers"][firm_key]
        f = full[firm_key]
        gate = bool(b["bootstrap_ok"] and h["half_panel_ok"])
        all_ok = all_ok and gate
        tiers[firm_key] = {
            "full_panel_ok": f["floor_ok"],
            "bootstrap_ok": b["bootstrap_ok"],
            "H1_ok": h["H1"]["floor_ok"],
            "H2_ok": h["H2"]["floor_ok"],
            "gate_pass": gate,
            "full": f,
            "half": h,
            "bootstrap_summary": {
                "pass_5th": b["pass_5th"],
                "bust_95th": b["bust_95th"],
                "pass_mean": b["pass_mean"],
                "bust_mean": b["bust_mean"],
            },
        }
    return {
        "floor_bust": thr.eval_bust_ceiling,
        "floor_pass": thr.pass_floor,
        "overall_gate_pass": bool(all_ok),
        "verdict": (
            "GATE PASS"
            if all_ok
            else "GATE FAIL (regime-fragile) — standing G8 caveat; "
            "does NOT overturn Part A DISCHARGED"
        ),
        "tiers": tiers,
    }


def write_regime_gate_md(path: Path, report: dict) -> None:
    status = report.get("status", "UNKNOWN")
    lines = [
        "# Class-S candidate #1 — regime-robustness rider (gate §7(7))",
        "",
        f"**Status:** `{status}`",
        f"**Date:** 2026-07-15",
        "",
        "## Citations",
        "",
        "- Candidate pre-reg: [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](../../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) (§6 rider)",
        "- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (§7(7))",
        "- Methodology: [`docs/methodology/regime_robustness_gate.md`](../../../docs/methodology/regime_robustness_gate.md)",
        "- G0–G8 RESULTS: [`RESULTS.md`](RESULTS.md) (`RESOLVED (DISCHARGED)`)",
        "- Driver: [`run_class_s_c1_regime_gate.py`](run_class_s_c1_regime_gate.py)",
        "",
        "## Locked posture",
        "",
        f"- Floor = Part A: bust ≤ {report.get('floor_bust_pct', '3.0')}%"
        f" + P(pass) ≥ {report.get('floor_pass_pct', '50')}%",
        "- Geometry = Run-2 on `Tradeify_Select_100K` + `MFFU_Rapid_100K`",
        "- FAIL does **not** overturn mechanical Part A DISCHARGED — standing G8 caveat only",
        f"- Live c1 tier `Tradeify_Select_100K` present in FIRM_RULES "
        f"(ACTIVE_FIRM deleted substrate Phase 4)",
        "",
    ]
    detail = report.get("detail")
    if detail:
        lines.extend(["## Detail", "", detail, ""])

    verdict = report.get("verdict")
    if verdict:
        lines.extend(
            [
                "## Verdict",
                "",
                f"**{verdict.get('verdict', status)}**",
                "",
                f"Overall gate pass: `{verdict.get('overall_gate_pass')}`",
                "",
            ]
        )
        for firm_key, t in verdict.get("tiers", {}).items():
            bs = t.get("bootstrap_summary", {})
            h = t.get("half", {})
            lines.extend(
                [
                    f"### {firm_key}",
                    "",
                    f"- Full-panel: bust={t['full']['headline_bust']:.2%} "
                    f"pass={t['full']['pass_rate']:.2%} "
                    f"→ {'PASS' if t['full_panel_ok'] else 'FAIL'}",
                    f"- Bootstrap: pass 5th={bs.get('pass_5th', float('nan')):.2%} "
                    f"bust 95th={bs.get('bust_95th', float('nan')):.2%} "
                    f"→ {'PASS' if t['bootstrap_ok'] else 'FAIL'}",
                    f"- H1: bust={h['H1']['headline_bust']:.2%} "
                    f"pass={h['H1']['pass_rate']:.2%} "
                    f"→ {'PASS' if t['H1_ok'] else 'FAIL'}",
                    f"- H2: bust={h['H2']['headline_bust']:.2%} "
                    f"pass={h['H2']['pass_rate']:.2%} "
                    f"→ {'PASS' if t['H2_ok'] else 'FAIL'}",
                    f"- **Tier gate:** `{'PASS' if t['gate_pass'] else 'FAIL'}`",
                    "",
                ]
            )

    lines.extend(
        [
            "## G8 intake note",
            "",
            report.get(
                "g8_note",
                "Deferred — gate not completed.",
            ),
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def g8_note_for(verdict: dict | None, *, status: str) -> str:
    if status.startswith("NEEDS_CONTEXT") or status.startswith("PHASE0"):
        return (
            "G8 intake blocked on panel bytes / Phase-0 — runner ready; "
            "re-run locally with pinned CME CSVs, then annotate with PASS "
            "or standing FAIL caveat."
        )
    if verdict is None:
        return "G8 intake pending regimen completion."
    if verdict.get("overall_gate_pass"):
        return (
            "DISCHARGED stands. Regime rider **PASS** on both discharge tiers — "
            "book ready for lifecycle CANDIDATE @ 1.00× intake annotation. "
            "Rail / account / go-live stay separately gated. No `core/lifecycle.py` "
            "write for the four locked CFD legs (prop CANDIDATE is book-level)."
        )
    return (
        "DISCHARGED stands (mechanical Part A unchanged). Regime rider "
        "**FAIL (regime-fragile)** — admit to G8 with **standing caveat** only; "
        "do not re-open Part A. Rail / account / go-live stay gated."
    )


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--smoke",
        action="store_true",
        help=f"wiring check: n_panels={SMOKE_N_PANELS}, n_sims={SMOKE_N_SIMS}",
    )
    ap.add_argument(
        "--half-only",
        action="store_true",
        help="run Part B half-panel only (skip bootstrap)",
    )
    ap.add_argument(
        "--n-panels",
        type=int,
        default=None,
        help=f"bootstrap panel count (default {N_PANELS_DEFAULT}; smoke={SMOKE_N_PANELS})",
    )
    ap.add_argument(
        "--n-sims",
        type=int,
        default=None,
        help="override sims/seed (default: frozen 10k)",
    )
    ap.add_argument(
        "--n-jobs",
        type=int,
        default=-1,
        help="joblib parallel workers for bootstrap (-1=all; 1=serial)",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=_HERE,
        help="directory for REGIME_GATE.md + JSON report",
    )
    args = ap.parse_args(list(argv) if argv is not None else None)
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    n_sims = SMOKE_N_SIMS if args.smoke and args.n_sims is None else args.n_sims
    n_panels = (
        SMOKE_N_PANELS
        if args.smoke and args.n_panels is None
        else (args.n_panels if args.n_panels is not None else N_PANELS_DEFAULT)
    )

    try:
        phase0_verify()
    except Phase0Error as e:
        report = {
            "status": "PHASE0_FAIL",
            "detail": str(e),
            "g8_note": g8_note_for(None, status="PHASE0_FAIL"),
        }
        write_regime_gate_md(out_dir / "REGIME_GATE.md", report)
        (out_dir / "regime_gate_report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(f"[regime] PHASE0_FAIL: {e}", file=sys.stderr)
        return 3

    thr = load_scoring_thresholds(GATE_PREREG)
    try:
        for leg in C1_STRATS:
            resolve_panel_path(leg)
        panel_c1, meta_c1, _trades = build_scaled_panel(
            C1_STRATS, C1_ALLOCS, expect_1r=dict(EXPECTED_1R)
        )
    except NeedsContext as e:
        report = {
            "status": "NEEDS_CONTEXT",
            "detail": (
                "Phase-0 inputs incomplete — regime gate not started "
                "(no improvisation; same class as G0–G8 adapter).\n\n"
                f"```\n{e}\n```\n\n"
                "Required files under `core/data/tv_exports/cme/` "
                "(gitignored; SHA256SUMS already lists the hashes):\n"
                + "\n".join(
                    f"- `{PANEL_FILES[leg][0]}` sha256=`{PANEL_FILES[leg][1]}`"
                    for leg in C1_STRATS
                )
            ),
            "floor_bust_pct": f"{thr.eval_bust_ceiling * 100:.1f}",
            "floor_pass_pct": f"{thr.pass_floor * 100:.0f}",
            "g8_note": g8_note_for(None, status="NEEDS_CONTEXT"),
        }
        write_regime_gate_md(out_dir / "REGIME_GATE.md", report)
        (out_dir / "regime_gate_report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(f"[regime] NEEDS_CONTEXT: {e}", file=sys.stderr)
        return 2

    daily_100k = book_daily_at_100k(panel_c1)
    print(
        f"[regime] panel {meta_c1.get('panel_span')} "
        f"n_bdays={meta_c1.get('n_bdays')} "
        f"smoke={args.smoke} n_sims={n_sims or thr.sims_per_seed} "
        f"n_panels={n_panels}",
        flush=True,
    )

    full = full_panel_reference(daily_100k, thr, n_sims=n_sims)
    half = part_b_half_panel(daily_100k, thr, n_sims=n_sims)

    if args.half_only:
        boot = {
            "n_panels": 0,
            "block_size_bdays": BLOCK_SIZE_BDAYS,
            "boot_seed": BOOT_SEED,
            "tiers": {
                fk: {
                    "pass_5th": float("nan"),
                    "pass_mean": float("nan"),
                    "bust_95th": float("nan"),
                    "bust_mean": float("nan"),
                    "bootstrap_ok": False,
                    "wall_s": 0.0,
                    "panels": [],
                    "skipped": True,
                }
                for fk in DISCHARGE_TIERS
            },
        }
        status = "HALF_ONLY (bootstrap deferred)"
    else:
        boot = part_a_bootstrap(
            daily_100k,
            thr,
            n_panels=n_panels,
            n_sims=n_sims,
            n_jobs=args.n_jobs,
        )
        status = "SMOKE" if args.smoke else "COMPLETE"

    verdict = compose_verdict(full, half, boot, thr)
    if args.half_only:
        # Override: without bootstrap, no overall PASS claim.
        verdict["overall_gate_pass"] = False
        verdict["verdict"] = (
            "HALF_ONLY — Part B recorded; bootstrap still owed before GATE PASS/FAIL claim"
        )

    g8 = g8_note_for(verdict if not args.half_only else None, status=status)
    report = {
        "status": status,
        "floor_bust": thr.eval_bust_ceiling,
        "floor_pass": thr.pass_floor,
        "floor_bust_pct": f"{thr.eval_bust_ceiling * 100:.1f}",
        "floor_pass_pct": f"{thr.pass_floor * 100:.0f}",
        "n_sims": n_sims or thr.sims_per_seed,
        "n_panels": n_panels if not args.half_only else 0,
        "smoke": bool(args.smoke),
        "half_only": bool(args.half_only),
        "panel_meta": meta_c1,
        "live_c1_tier": "Tradeify_Select_100K",
        "full_panel": full,
        "half_panel": half,
        "bootstrap": {
            k: {kk: vv for kk, vv in v.items() if kk != "panels"}
            for k, v in boot["tiers"].items()
        },
        "bootstrap_meta": {
            "n_panels": boot["n_panels"],
            "block_size_bdays": boot["block_size_bdays"],
            "boot_seed": boot["boot_seed"],
        },
        "verdict": verdict,
        "g8_note": g8,
        "detail": (
            f"Part A floors applied per partition (bust≤{thr.eval_bust_ceiling:.1%}, "
            f"pass≥{thr.pass_floor:.0%}). "
            f"Discharge tiers={list(DISCHARGE_TIERS)}. "
            f"DISCHARGED mechanical read stands regardless of rider outcome."
        ),
        "candidate_prereg": (
            "docs/briefs/pre-registration/"
            "2026-07-15-existing-strategy-book-candidate-1-prereg.md"
        ),
        "gate_prereg": (
            "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
        ),
    }
    # Keep full bootstrap panel vectors in a sidecar-friendly shape when not enormous.
    if not args.half_only and n_panels <= 20:
        report["bootstrap_panels"] = boot["tiers"]

    (out_dir / "regime_gate_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    write_regime_gate_md(out_dir / "REGIME_GATE.md", report)
    print(
        f"[regime] DONE status={status} "
        f"overall_gate_pass={verdict.get('overall_gate_pass')} "
        f"verdict={verdict.get('verdict')}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
