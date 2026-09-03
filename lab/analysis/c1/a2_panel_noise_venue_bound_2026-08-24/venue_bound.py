"""Closed-form venue bound for a prop eval with a trailing rope, and its validation
against the A2 shape-feasibility map's own 945 committed cells.

Derivation (see RESULTS.md section 2). For a construct with per-trade edge mu and
per-trade dispersion sigma (both in R), traded at r dollars of risk per trade, against
an eval with a trailing rope of D dollars and a profit target of T dollars:

    P(max drawdown from running peak >= D)  ~=  exp(-2*mu*D / (sigma^2 * r))
    trades needed to reach the target        =  T / (mu * r)

Setting the first equal to the frozen bust ceiling b and eliminating r gives a
*size-invariant* floor on the number of trades, and hence on calendar time:

    n_min      = (T/D) * (ln(1/b)/2) * (sigma/mu)^2
    T_min(yrs) = (T/D) * (ln(1/b)/2) / annSR^2        [annSR = (mu/sigma)*sqrt(trades/yr)]

Position size cancels. That is the formal content of "no risk size is simultaneously
safe and useful" (orb_universe_2026-06-22/RESULTS.md, NAS100 ORB-30 sizing sweep).

Read-only. Imports nothing from core/ or ops/; consumes the committed A2 JSONL.
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
A2_JSONL = REPO_ROOT / "lab/analysis/c1/shape_feasibility_map_2026-08/region_data_with_growth.jsonl"

# ⚠ v1's frozen ceiling (prereg 2026-07-13), pinned to reproduce THIS campaign's
# published bound. The LIVE ceiling is 0.05 (prereg v2, 2026-08-26). This constant
# is quantitatively load-bearing -- it enters as math.log(1.0 / BUST_CEILING), so
# at 0.05 the bound term falls 3.507 -> 2.996 and every min_years / required-panel
# figure below shrinks by ~15%. Do not "update" it in place: re-deriving the bound
# at the live ceiling is a separate result needing its own GO.
BUST_CEILING = 0.03          # frozen, prop-survivor-scoring prereg 2026-07-13 (v1, CLOSED)
TRADING_DAYS_PER_YEAR = 252

# (rope $, target $) per tier -- core/firm_rules.py
TIERS = {
    "Tradeify_Select_25K":  (1_000.0, 1_500.0),
    "Tradeify_Select_50K":  (2_000.0, 3_000.0),
    "Tradeify_Select_100K": (3_000.0, 6_000.0),
    "Tradeify_Select_150K": (4_500.0, 9_000.0),
    "Tradeify_Growth_100K": (3_500.0, 6_000.0),
    "MFFU_Rapid_50K":       (2_000.0, 3_000.0),
    "MFFU_Rapid_100K":      (3_000.0, 6_000.0),
}


def bound_constant(rope: float, target: float, ceiling: float = BUST_CEILING) -> float:
    """The tier's own constant C, such that T_min(years) = C / annSR^2."""
    return (target / rope) * (math.log(1.0 / ceiling) / 2.0)


def min_years(annsr: float, tier: str, ceiling: float = BUST_CEILING) -> float:
    rope, target = TIERS[tier]
    return bound_constant(rope, target, ceiling) / (annsr ** 2)


def required_annsr(years: float, tier: str, ceiling: float = BUST_CEILING) -> float:
    rope, target = TIERS[tier]
    return math.sqrt(bound_constant(rope, target, ceiling) / years)


# --- the A2 map's own synthetic DGP, in closed form (shape_generator.py section 2) ---
def dgp_moments(win_rate: float, shape: str) -> tuple[float, float]:
    if shape == "symmetric":
        mw, vw, ml, vl = 1.0, (1.3 - 0.7) ** 2 / 12, -1.0, (1.3 - 0.7) ** 2 / 12
    elif shape == "mild_right_skew":
        mw, vw, ml, vl = 1.5, 0.5 ** 2, -1.0, (1.3 - 0.7) ** 2 / 12
    elif shape == "bounded_clustered":
        mw, vw, ml, vl = 1.0, (1.1 - 0.9) ** 2 / 12, -1.0, 0.0
    else:
        raise ValueError(shape)
    m = win_rate * mw + (1 - win_rate) * ml
    e2 = win_rate * (mw * mw + vw) + (1 - win_rate) * (ml * ml + vl)
    return m, math.sqrt(e2 - m * m)


def validate() -> None:
    rows = [json.loads(line) for line in A2_JSONL.open(encoding="utf-8")]
    print("Validation of  T_min = C / annSR^2  against the A2 map's committed cells.")
    print("The bound is CONDITIONAL on bust <= 3%: cells sized above the ceiling reach the")
    print("target faster precisely because they are over-risked, and are not in scope.\n")
    for tier in ("Tradeify_Select_100K", "Tradeify_Growth_100K"):
        const = bound_constant(*TIERS[tier])
        honour, violations, tight = 0, [], []
        for r in rows:
            if r["firm"] != tier or r["median_days_to_pass"] is None or r["bust"] > BUST_CEILING:
                continue
            m, s = dgp_moments(r["win_rate"], r["shape"])
            if m <= 0:
                continue
            annsr = (m / s) * math.sqrt(r["cadence"] * 52)
            t_min_days = const / annsr ** 2 * TRADING_DAYS_PER_YEAR
            ratio = r["median_days_to_pass"] / t_min_days
            if ratio < 0.98:
                violations.append((r["cell_id"], round(t_min_days), r["median_days_to_pass"], r["bust"]))
            else:
                honour += 1
            if 0.02 < r["bust"] <= BUST_CEILING:
                tight.append(ratio)
        print(f"{tier}   (C = {const:.3f})")
        print(f"   bust-compliant cells honouring the bound : {honour}")
        print(f"   violations                               : {len(violations)}")
        for v in violations:
            print(f"      {v[0]}  T_min {v[1]}d  actual {v[2]:.0f}d  bust {v[3]:.4f}")
        if tight:
            print(f"   cells with bust in (2%, 3%] -- where the bound should BIND:")
            print(f"      actual/T_min  min {min(tight):.2f}  median {statistics.median(tight):.2f}  max {max(tight):.2f}")
        print()


def tier_table() -> None:
    print("Tier geometry, ranked by how hard the rope makes the eval:\n")
    print(f"{'tier':24s} {'rope $':>8} {'target $':>9} {'T/D':>6} {'C':>7} "
          f"{'annSR for 3mo':>14} {'6mo':>7} {'1yr':>7}")
    for tier, (rope, target) in sorted(TIERS.items(), key=lambda kv: kv[1][1] / kv[1][0]):
        c = bound_constant(rope, target)
        print(f"{tier:24s} {rope:>8,.0f} {target:>9,.0f} {target/rope:>6.3f} {c:>7.3f} "
              f"{required_annsr(0.25, tier):>14.2f} {required_annsr(0.5, tier):>7.2f} "
              f"{required_annsr(1.0, tier):>7.2f}")


# Measured annualised Sharpe for every construct in the corpus that publishes one.
# ORB / ICT (the first-pass ledger's scope) and the four live TNEC construct lanes.
CORPUS = [
    ("ORB-MNQ-1, 2021+ best cell (corpus max)", 1.280,
     "orb_mnq_2026-07/RESULTS_stage7.md -- 2021+ at 3 ticks added slip"),
    ("NAS100 ORB-30 CFD 2020-26 (t=2.94, n=1663)", 1.154, "orb_universe_2026-06-22/RESULTS.md"),
    ("ORB-MNQ-1, 2021+ @ Tradeify cost", 1.140, "orb_mnq_2026-07/RESULTS_stage7.md T1"),
    ("ORB-MNQ-1, best admissible close_tod (13:45)", 0.934, "sessconf_mnq_2026-08/RESULTS.md"),
    ("ORB-MNQ-1, full window @ Bulenox cost", 0.890, "orb_mnq_2026-07/RESULTS_stage6.md"),
    ("ORB-MNQ-1, full window @ Tradeify cost", 0.835,
     "orb_mnq_2026-07/RESULTS_stage7.md T1; reproduced exactly by sessconf_mnq_2026-08"),
    ("Q-TNEC-CON-3 HTF native break, long arm", 0.405,
     "mnq_tnec_con3_htf_native_break_2026-08/RESULTS.md -- best of the four live lanes"),
    ("Q-TNEC-CON-4 PDH/PDL break, short arm", 0.085, "mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md"),
    ("ICT raid->FVG chain, frozen DOL target", 0.0, "ict_mnq_2026-08/RESULTS_EXP.md (CI straddles 0)"),
    ("Q-TNEC-CON-4 PDH/PDL break, long arm", -0.128, "mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS.md"),
    ("Q-TNEC-CON-2 compression break, long arm", -0.404, "mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md"),
    ("Q-TNEC-CON-5 impulse/pullback/VWAP, long arm", -0.532,
     "mnq_tnec_con5_impulse_pullback_vwap_2026-08/RESULTS.md"),
]


def corpus_scorecard() -> None:
    print("\nEvery construct in the corpus that publishes an annualised Sharpe,")
    print("against what the tiers require:\n")
    print(f"{'construct':46s} {'annSR':>6} {'T_min Select100K':>17} {'Growth100K':>12} {'Select50K':>11}")
    for name, sr, _src in CORPUS:
        if sr <= 0:
            print(f"{name:46s} {sr:>6.2f} {'never':>17} {'never':>12} {'never':>11}")
            continue
        print(f"{name:46s} {sr:>6.3f} "
              f"{min_years(sr,'Tradeify_Select_100K'):>16.1f}y "
              f"{min_years(sr,'Tradeify_Growth_100K'):>11.1f}y "
              f"{min_years(sr,'Tradeify_Select_50K'):>10.1f}y")
    print("\nFor reference: the repo's own frozen Stage-6 admission gate is annSR >= 0.85")
    print(f"   -> T_min on Select_100K = {min_years(0.85,'Tradeify_Select_100K'):.1f} years.")
    print(f"   The frozen survivor-scoring horizon is 1500 business days = "
          f"{1500/TRADING_DAYS_PER_YEAR:.2f} years, so 'P(pass) >= 50%' is a statement")
    print("   about a six-year eval, not a near-term one.")
    print("\nBreadth: k independent legs of equal Sharpe give annSR*sqrt(k), so T_min divides by k.")
    for tier, months in (("Tradeify_Select_100K", 6), ("Tradeify_Select_50K", 6)):
        need = required_annsr(months / 12, tier)
        for label, sr in (("ORB-MNQ-1 2021+", 1.140), ("ORB-MNQ-1 full", 0.835)):
            print(f"   {tier:22s} {months}-month pass needs annSR {need:.2f}  ->  "
                  f"{(need/sr)**2:5.1f} independent legs at {label} quality ({sr:.3f})")


if __name__ == "__main__":
    tier_table(); print(); validate(); corpus_scorecard()
