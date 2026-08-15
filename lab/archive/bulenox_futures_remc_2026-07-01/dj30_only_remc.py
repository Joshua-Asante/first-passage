"""DJ30-only (1-leg) Bulenox trailing-DD re-MC — viability of a single-leg MYM
book after Q-P2-MEASURE-1 killed NAS100 on edge-transfer (2026-07-03).

*** VERIFIED-CAVEATS (adversarial workflow wf_f114358d-e64, 2026-07-03) —
    this is a VIABILITY SCREEN, NOT lock-grade. See RESULTS_DJ30only_1leg_2026-07-03.md.
    1. 25K & 50K CAPPED rows are DESIGN-VOID: RESERVE base = floor(cap/8.5) rounds
       DJ30 base to 0 contracts at those tiers (caps 3/8 -> base 0). The CAPPED
       mean-ratio scalar cannot see this step-discontinuity; those rows are meaningless.
    2. The CAPPED arm's mean-ratio scalar is NOT a faithful model of per-trade
       integer sizing at coarse tiers (100K base=1, 150K base=2). The FULL/CAPPED
       bracket claim is untested where base rounds toward 0. A true integer re-run
       (base=floor(cap/8.5) per trade, suppress base=0) is required for lock-grade.
    3. bust<1% and p99DD<5% clear at 100K/150K and ARE regime-robust (0.07-0.47%
       bust across 2020-22 chop / 2022-26 windows) — verified. BUT the low bust is
       bought by a book that STALLS: 150K median pass ~457 days; in 2020-22 chop
       only 36.7% pass, 62.8% hit the horizon cap. "Clears the gates" is misleading.
    4. Do NOT claim "NAS100 was the bust driver": a matched-panel 2-leg book busts
       only 0.65%, split ~50/50 DJ30/NAS100.
    5. Panel uses the 2026-07-03 export, which does not reconcile to the canonical
       218-trade 567e1 baseline (fixed-1R pin absorbs it; audit-trail defect).
    6. _simulate_path models the fixed-$ Bulenox trailing cushion as percent-of-peak
       (optimistic by 0.07-0.36% of balance; sub-gate-flip but wrong for this venue). ***

Q-P2-MEASURE-1 (K2 tolerant re-score) excluded NAS100 from the futures book and
Q-P2-MEASURE-1.b showed DJ30's edge transfers. C4/C5 modeled the *2-leg*
DJ30+NAS100 book; this asks the now-relevant question: does DJ30 *alone*, at its
cap-bound sizing, survive Bulenox's fixed-$ trailing DD per tier?

Reuses the C4 orchestrator's exact machinery (force_flat + build_daily_panel +
run_seed + PRE_SHOCK_1R) with a 1-strat panel. Two arms per tier:
  - FULL   : %-equity at the locked 0.70% (no cap) — UPPER bound on bust
             (cap-bound reality is lower risk -> lower bust, slower pass).
  - CAPPED : panel x the C5 per-tier DJ30 cap factor (RESULTS_C5 "DJ30 mean
             ratio" column) — first-order model of the realistic cap-bound
             book (integer/RESERVE granularity not modeled per-trade; the two
             arms BRACKET the true integer-sized result).

C2-off (dd_scale=1.0 — the TV->TradersPost rail cannot run a portfolio-equity
overlay, same gate arm as C5). Inactivity token-trade-mitigated (a DJ30-only
book trades Tue/Fri only and idles far more than the 2-leg book -> the >=1-trade-
per-5-trading-days token micro-trade is an even harder requirement here; modeled
as non-binding).

Data: 2026-07-03 full-history DJ30 Pepperstone export (Downloads; slightly later
vintage than C4/C5's 2026-05-24 canonical panel — same locked v4.5 strategy) +
US30_M15 bars (main checkout). Vintage difference noted in RESULTS.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from joblib import Parallel, delayed  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from portfolio_mc import (  # noqa: E402
    ALLOCATIONS, BASELINE_BALANCE, PRE_SHOCK_1R, SEEDS,
    build_daily_panel, build_week_blocks, load_trades, run_seed,
)
from force_flat_transform import bars_utc_to_et, force_flat_csv  # noqa: E402

# Viability screen: 5000 sims/seed x 3 seeds = 15K/tier-arm is ample precision
# for a pass/bust screen (SE on a 90% rate at n=15K is ~0.24pp). The locked
# anchor's 10K is for lock-grade; this is a go/no-go viability cut.
SIMS_PER_SEED = 5_000

DL = Path(os.environ.get("P2_EXPORT_DIR", str(Path.home() / "Downloads")))
RAW_DJ30 = DL / "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-07-03_70416.csv"
# US30 bars: this worktree's core/data is bare (gitignored); main checkout has them.
US30_BARS = Path("C:/Users/joshu/multi_firm_operations/core/data/bar_data/US30_M15.csv")

TIERS = ("Bulenox_25K", "Bulenox_50K", "Bulenox_100K", "Bulenox_150K", "Bulenox_250K")
# RESULTS_C5_integer_2026-07-03.md, "DJ30 mean ratio (base cap)" column — the
# effective-risk multiplier the Bulenox contract cap imposes on DJ30 per tier.
C5_DJ30_CAP_FACTOR = {
    "Bulenox_25K": 0.61, "Bulenox_50K": 0.77, "Bulenox_100K": 0.72,
    "Bulenox_150K": 0.62, "Bulenox_250K": 0.63,
}


def build_dj30_panel() -> pd.DataFrame:
    """Force-flat DJ30 -> 1-strat $200K-normalized daily panel (striker only)."""
    for p in (RAW_DJ30, US30_BARS):
        if not p.exists():
            raise FileNotFoundError(f"missing input: {p}")
    raw = pd.read_csv(RAW_DJ30, encoding="utf-8-sig")
    bars = bars_utc_to_et(pd.read_csv(US30_BARS))
    ff = force_flat_csv(raw, bars)
    ff_path = _HERE / "inputs" / "dj30_forceflat_1leg.csv"
    ff_path.parent.mkdir(exist_ok=True)
    ff.to_csv(ff_path, index=False)
    trades = {"striker": load_trades(ff_path, strategy="striker")}
    panel, scale_info = build_daily_panel(
        trades, {"striker": ALLOCATIONS["striker"]},
        fixed_1r_reference={"striker": PRE_SHOCK_1R["striker"]},
    )
    print(f"scale_info: {scale_info}")
    return panel


def run_tier(panel: pd.DataFrame, tier: str, risk_mult: float) -> dict:
    firm = FIRM_RULES[tier]
    bal = float(firm["starting_balance"])
    # rescale $200K-normalized panel to tier balance, then apply the risk mult
    tier_panel = panel * (bal / BASELINE_BALANCE) * risk_mult
    blocks = build_week_blocks(tier_panel)
    firm_kwargs = {
        "starting_equity": bal,
        "dd_type": firm["dd_type"],
        "trailing_dd_pct": -firm["max_dd_pct"] / 100,
        "daily_loss_pct": None,          # Bulenox has no daily loss limit
        "profit_target": bal * (1 + firm["profit_target_pct"] / 100),
        "min_trading_days": firm["min_trading_days"],
        "inactivity_limit": 10_000,      # token-trade-mitigated (non-binding)
    }
    seeds = [run_seed(s, SIMS_PER_SEED, blocks, 0.015, 1.0,  # dd_scale=1.0 = C2-off
                      strats=("striker",), firm_kwargs=firm_kwargs) for s in SEEDS]
    per = SIMS_PER_SEED
    keys = ("pass", "bust_daily", "bust_static", "bust_trailing",
            "bust_inactivity", "horizon_cap")
    rates = {k: float(np.mean([r["outcomes"][k] / per for r in seeds])) for k in keys}
    dds = [d for r in seeds for d in r["max_dds"]]
    days = [d for r in seeds for d in r["days_to_pass"]]
    return {
        "tier": tier, "bal": bal, "risk_mult": risk_mult,
        "pass": rates["pass"],
        "bust": rates["bust_daily"] + rates["bust_static"] + rates["bust_trailing"],
        "p99_dd": float(np.percentile(dds, 99)) if dds else float("nan"),
        "med_days": int(np.median(days)) if days else -1,
        "n_blocks": len(blocks),
    }


def main():
    panel = build_dj30_panel()
    print(f"panel: {len(panel)} bdays, DJ30-only", flush=True)
    jobs = [(tier, arm, mult)
            for tier in TIERS
            for arm, mult in (("FULL", 1.0), ("CAPPED", C5_DJ30_CAP_FACTOR[tier]))]
    # Parallelize the 10 (tier, arm) combos across cores; each runs 3 seeds serially.
    results = Parallel(n_jobs=-1, verbose=5)(
        delayed(run_tier)(panel, tier, mult) for (tier, arm, mult) in jobs
    )
    print(f"\n{'tier':<14}{'arm':<8}{'risk':<7}{'pass':>8}{'bust':>8}{'p99DD':>8}{'medD':>7}", flush=True)
    print("-" * 60, flush=True)
    for (tier, arm, mult), r in zip(jobs, results):
        eff = ALLOCATIONS["striker"] * mult
        print(f"{tier:<14}{arm:<8}{eff*100:>5.2f}%{r['pass']:>8.2%}"
              f"{r['bust']:>8.2%}{r['p99_dd']:>8.2%}{r['med_days']:>7}", flush=True)
    print("\nNote: bust is 100% trailing-DD (Bulenox has no daily-loss/static mode).", flush=True)
    print("FULL = %-equity 0.70% (upper bound on bust); CAPPED = x C5 per-tier cap", flush=True)
    print("factor (realistic cap-bound). True integer-sized result is bracketed by these.", flush=True)


if __name__ == "__main__":
    main()
