"""Post-fix confirmation: the CANONICAL path now returns the corrected geometry
NATIVELY -- no monkey-patch, no override, just firm_rules.py as shipped.

Context. `remc_eval_lock_fix.py` (2026-07-22) measured the defect by MUTATING
`firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"]` at runtime, scoring a
BASELINE arm (100.0, as published) against a CORRECTED arm (1_000_000.0,
unreachable). That proved the DELTA. It deliberately left the source constant
at 100 (RESULTS.md section 6: "the constant is not hand-edited... needs its
own ADR + re-pin pass").

Every consumer since has carried the correction as a per-script monkey-patch
(c1_band_rescore_2026-07-24, c1_cadence_inactivity_2026-08-02, this
directory's own two scripts). That is real technical debt: a fresh, naive
invocation of `prop_survivor_scoring`'s documented CLI, or a direct
`firm_kwargs()` call, inherits the WRONG default with no signal that a patch
is expected. The source fix removes that trap.

This script proves the fix landed correctly by running `score_candidate`
IDENTICALLY to `remc_eval_lock_fix.py`'s two arms, but reading
`dd_lock_offset_usd` straight off `firm_rules.FIRM_RULES` -- once before the
fix (must reproduce the old BASELINE numbers) and once after (must reproduce
the old CORRECTED numbers), with NO in-script override either time. The only
thing that changes between the two calls is the state of the committed file.

Usage:
    python remc_native_postfix_check_2026-08-04.py --pre    # run BEFORE the fix lands
    python remc_native_postfix_check_2026-08-04.py --post   # run AFTER the fix lands
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]

_HARNESS = _ROOT / "lab" / "analysis" / "c1" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", _HARNESS,
           _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import firm_rules  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    load_scoring_thresholds, score_candidate,
)

# Parse OUR OWN args before wiping sys.argv for H's benefit below -- H (run_class_s_
# c1_scoring) has its own module-level argparse and chokes on unrecognized flags, so
# every sibling script in this family resets sys.argv before importing it. Doing that
# BEFORE this script's own parse_args() call (as the first draft did) silently wipes
# --pre/--post before they're read. Parse first, wipe second.
_ap = argparse.ArgumentParser()
_grp = _ap.add_mutually_exclusive_group(required=True)
_grp.add_argument("--pre", action="store_true", help="run before the fix lands")
_grp.add_argument("--post", action="store_true", help="run after the fix lands")
_ARGS = _ap.parse_args()
_PHASE = "post" if _ARGS.post else "pre"

sys.argv = [sys.argv[0]]
import run_class_s_c1_scoring as H  # noqa: E402

import numpy as np  # noqa: E402

TIERS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")

# From remc_eval_lock_fix.py / remc_g8_discharge_check.py, 2026-07-22, re-confirmed
# this session against the frozen 07-11 panel bytes (see the companion re-run log).
EXPECTED = {
    "pre": {   # source AS-SHIPPED (dd_lock_offset_usd=100) -> must equal the OLD "baseline" numbers
        "Tradeify_Select_100K": {"run2_bust": 0.0265},
        "MFFU_Rapid_100K": {"run2_bust": 0.0264},
    },
    "post": {  # source FIXED (dd_lock_offset_usd=1_000_000.0) -> must equal the OLD "corrected" numbers
        "Tradeify_Select_100K": {"run2_bust": 0.0474},
        "MFFU_Rapid_100K": {"run2_bust": 0.0425},
    },
}
TOLERANCE = 5e-4  # matches remc_eval_lock_fix.py's own MATCH/MISMATCH threshold


def main() -> int:
    phase = _PHASE

    thr = load_scoring_thresholds(H.GATE_PREREG)
    panel, meta, trades = H.build_scaled_panel(
        H.C1_STRATS, H.C1_ALLOCS, expect_1r=dict(H.EXPECTED_1R)
    )
    daily_100k = H.book_daily_at_100k(panel)
    tr = np.concatenate([s.to_numpy(dtype=float) for s in trades.values()])

    print(f"[phase] {phase}  (no override applied in this script; "
          f"reading firm_rules.py as committed)")
    for tier in TIERS:
        live_offset = firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"]
        print(f"[source] {tier}.dd_lock_offset_usd = {live_offset}")

    out = {"phase": phase}
    all_match = True
    for tier in TIERS:
        tier_offset = firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"]
        rep = score_candidate(
            strategy_label=f"c1 native-postfix-check {phase} {tier}",
            candidate_daily_pnl=daily_100k,
            full_res_trades=list(tr),
            envelope_verdict="YES",
            thresholds=thr,
            gross_edge_usd=float(tr[tr > 0].sum()),
            tiers=(tier,),
        ).to_dict()
        t = rep["tiers"][tier]
        run2 = t.get("run2") or {}
        bust = run2.get("headline_bust")
        expected = EXPECTED[phase][tier]["run2_bust"]
        match = bust is not None and abs(bust - expected) < TOLERANCE
        all_match &= match
        out[tier] = {"dd_lock_offset_usd": tier_offset, "run2_bust": bust,
                     "expected": expected, "match": match}
        print(f"  {tier}: run2 bust {bust*100:.2f}% vs expected "
              f"{expected*100:.2f}% ({phase}-fix) -> {'MATCH' if match else 'MISMATCH'}")

    dest = Path(__file__).with_name(f"remc_native_postfix_{phase}_report.json")
    dest.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"\n[written] {dest}")
    print(f"\n[verdict] {'ALL MATCH' if all_match else 'MISMATCH — see above'} "
          f"-- the canonical path {'already returns' if all_match else 'does NOT yet return'} "
          f"the {phase}-fix numbers with zero override.")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
