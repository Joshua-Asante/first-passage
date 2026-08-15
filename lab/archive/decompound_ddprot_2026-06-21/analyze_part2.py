"""CC-handoff §2.6 — parametric synthetic 5th-leg target-spec sweep (2026-06-21).

NOT an instrument pick. Injects a *clearly-synthetic* parametric leg defined by
(standalone PF tier, risk%, ρ_stress = correlation to the 4-leg portfolio
RESTRICTED to the §2.5 worst windows, active-day set) and re-runs the LOCKED
production MC for each cell. Output: the pass-rate / p99-DD response surface and
the minimum 5th-leg profile that materially helps, then maps the copper-short
candidate onto it.

Reuses the production MC (run_mc -> build_daily_panel / build_week_blocks /
_run_seeds / _simulate_path) verbatim. Controlled-Δ design: appending a 5th
column leaves n_blocks and the per-seed block indices UNCHANGED (fixed SEEDS),
so every cell samples the identical resampled week sequences — the only
difference is the 5th leg's P&L. Δpass / Δp99 are therefore clean.

NO fabricated instrument CSV. The 5th leg is labelled synthetic throughout.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from analyze_part1 import (  # noqa: E402  (reuse the exact part-1 primitives)
    dd_protection_walk, run_mc, ACCOUNT, ALLOC, FIXED_1R, LABEL,
)

OUT = _HERE
ACCT = ACCOUNT

# ── load the persisted 4-leg static dollar panel + worst windows ───────────
panel = pd.read_pickle(OUT / "panel_static.pkl")
LEGS = list(panel.columns)
P = panel.sum(axis=1)                      # portfolio combined daily $ P&L
cov = json.load(open(OUT / "covariance_enb.json"))

# worst-window day SET = union of [peak..trough] business days over the K=10 windows
worst_days = set()
for w in cov["worst_windows"]:
    rng = pd.bdate_range(w["peak"], w["trough"])
    worst_days.update(rng)
print(f"Worst-window day set: {len(worst_days)} bdays across {len(cov['worst_windows'])} windows.")

# ── synthetic-leg generator ────────────────────────────────────────────────
# PF tier -> (win-rate, win multiple in R) s.t. PF = WR*Rmult/(1-WR).
PF_TIERS = {
    "marginal(PF~1.1)": (0.40, 1.65),   # 0.40*1.65/0.60 = 1.10
    "solid(PF~1.5)":    (0.45, 1.833),  # 0.45*1.833/0.55 = 1.50
    "strong(PF~2.0)":   (0.50, 2.00),   # 0.50*2.00/0.50  = 2.00
}
ACTIVE_DAYS = {
    "Mon/Tue (crowded)": {0, 1},
    "Thu/Fri (fill)":    {3, 4},
}
SIGNAL_FREQ = 0.45          # P(signal | active weekday) -> ~0.9 trades/wk ~ 300 trades/6.4yr (NAS-like)
RHO_GRID = [+0.3, 0.0, -0.3, -0.6]
RISK5_DEFAULT = 0.0050      # modest 0.50% added weight (between NAS 0.37% and DJ30 0.70%)


def make_synth(active_wd, pf_tier, rho_target, risk5, seed):
    """Synthetic 5th-leg daily $ P&L (Series on panel.index, 0 off-days).

    Trades on `active_wd` weekdays with prob SIGNAL_FREQ. Standalone edge set by
    PF tier (WR, R-multiple). ρ_stress imposed by aligning a |rho_target| share
    of worst-window trade-day outcomes to -sign(P) (rho<0 = green when the
    portfolio bleeds) or +sign(P) (rho>0). 1R = risk5 * $200K.
    """
    rng = np.random.default_rng(seed)
    wr, rmult = PF_TIERS[pf_tier]
    oneR = risk5 * ACCT
    y = np.zeros(len(panel.index))
    Parr = P.to_numpy()
    for i, d in enumerate(panel.index):
        if d.weekday() not in active_wd:
            continue
        if rng.random() >= SIGNAL_FREQ:
            continue
        in_stress = d in worst_days
        if in_stress and rho_target != 0.0 and rng.random() < abs(rho_target):
            Pd = Parr[i]
            win = (Pd < 0) if rho_target < 0 else (Pd > 0)
        else:
            win = rng.random() < wr
        y[i] = rmult * oneR if win else -oneR
    s = pd.Series(y, index=panel.index)
    # realized diagnostics
    traded = s[s != 0]
    rp = float(traded[traded > 0].sum() / abs(traded[traded < 0].sum())) if (traded < 0).any() else float("inf")
    # realized ρ over worst-window trade days
    mask = np.array([d in worst_days for d in panel.index]) & (s.to_numpy() != 0)
    if mask.sum() > 3:
        rr = float(np.corrcoef(s.to_numpy()[mask], Parr[mask])[0, 1])
    else:
        rr = float("nan")
    return s, {"n_trades": int((s != 0).sum()), "realized_pf": rp, "realized_rho": rr,
               "net": float(s.sum())}


def mc_5leg(synth: pd.Series, risk5: float):
    """Run the production MC on the 4 static legs + the synthetic 5th, fixed-1R."""
    trades = {leg: pd.DataFrame({"exit_date": panel.index, "pnl": panel[leg].to_numpy()})
              for leg in LEGS}
    trades["synth5"] = pd.DataFrame({"exit_date": panel.index, "pnl": synth.to_numpy()})
    allocs = dict(ALLOC); allocs["synth5"] = risk5
    fixed = dict(FIXED_1R); fixed["synth5"] = risk5 * ACCT
    return run_mc(trades, allocs, fixed)


def run_cell(active_name, active_wd, pf_tier, rho, risk5, seed):
    """One sweep cell (top-level so joblib/loky can pickle it). Deterministic given
    seed + fixed MC SEEDS -> identical to the serial path."""
    synth, diag = make_synth(active_wd, pf_tier, rho, risk5, seed)
    r = mc_5leg(synth, risk5)
    return {"active": active_name, "pf_tier": pf_tier, "rho_target": rho,
            "rho_real": diag["realized_rho"], "pf_real": diag["realized_pf"],
            "n_trades": diag["n_trades"], "pass": r["pass_rate"],
            "bust": r["bust_rate"], "p99": r["p99_dd"], "median": r["median_days_to_pass"]}


def main():
    # 4-leg baseline (reconstruct from panel -> must reproduce part-1 §2.4)
    base_trades = {leg: pd.DataFrame({"exit_date": panel.index, "pnl": panel[leg].to_numpy()})
                   for leg in LEGS}
    base = run_mc(base_trades, ALLOC, FIXED_1R)
    b_pass, b_bust, b_p99, b_med = base["pass_rate"], base["bust_rate"], base["p99_dd"], base["median_days_to_pass"]
    print("=" * 100)
    print("§2.6  4-LEG BASELINE (decompounded static 2020-26, locked C2) — controlled-Δ reference")
    print(f"      pass {b_pass:.2%} | bust {b_bust:.2%} | p99 DD {b_p99:.2%} | median {b_med}d "
          f"  [gates: bust<1% {'OK' if b_bust<0.01 else 'BREACH'}, p99<5% {'OK' if b_p99<0.05 else 'BREACH'}]")
    print("=" * 100)
    print(f"Synthetic leg: risk {RISK5_DEFAULT:.2%} (ADDED -> total risk {2.91+RISK5_DEFAULT*100:.2f}%), "
          f"signal freq {SIGNAL_FREQ:.0%} of active weekdays.")
    print(f"ρ_stress target = correlation to the 4-leg portfolio over the {len(worst_days)} worst-window days.\n")

    # build the 24-cell arg list (seed=1000+cell preserves serial reproducibility)
    args = []
    cell = 0
    for active_name, active_wd in ACTIVE_DAYS.items():
        for pf_tier in PF_TIERS:
            for rho in RHO_GRID:
                cell += 1
                args.append((active_name, active_wd, pf_tier, rho, RISK5_DEFAULT, 1000 + cell))
    from joblib import Parallel, delayed
    raw = Parallel(n_jobs=7, backend="loky")(delayed(run_cell)(*a) for a in args)

    print(f"{'active':<20}{'PF tier':<18}{'ρ tgt':>6}{'ρ real':>8}{'PF real':>8}{'N':>5}"
          f"{'pass':>8}{'bust':>8}{'p99':>8}{'med':>5}{'Δpass':>8}{'Δbust':>8}{'Δp99':>8}  gatesOK")
    rows = []
    for c in raw:
        c["dpass"] = c["pass"] - b_pass
        c["dbust"] = c["bust"] - b_bust
        c["dp99"] = c["p99"] - b_p99
        c["gates_restored"] = (c["bust"] < 0.01) and (c["p99"] < 0.05)
        print(f"{c['active']:<20}{c['pf_tier']:<18}{c['rho_target']:>+6.1f}{c['rho_real']:>8.2f}"
              f"{c['pf_real']:>8.2f}{c['n_trades']:>5}"
              f"{c['pass']:>8.2%}{c['bust']:>8.2%}{c['p99']:>8.2%}"
              f"{c['median']:>5}{c['dpass']:>+8.2%}{c['dbust']:>+8.2%}{c['dp99']:>+8.2%}"
              f"  {'YES' if c['gates_restored'] else 'no'}")
        rows.append(c)
    print()

    # ── response-surface read + minimum profile ────────────────────────────
    df = pd.DataFrame(rows)
    print("RESPONSE SURFACE — Δp99 DD (pp) by ρ_stress × PF tier  (avg over both active-day sets):")
    piv = df.pivot_table(index="pf_tier", columns="rho_target", values="dp99", aggfunc="mean") * 100
    print(piv.round(2).to_string())
    print("\nRESPONSE SURFACE — Δpass (pp) by ρ_stress × PF tier:")
    piv2 = df.pivot_table(index="pf_tier", columns="rho_target", values="dpass", aggfunc="mean") * 100
    print(piv2.round(2).to_string())
    print()

    gate_cells = df[df["gates_restored"]].sort_values(["dp99", "dbust"])
    print(f"Cells that RESTORE BOTH gates (bust<1% AND p99<5%): {len(gate_cells)} / {len(df)}")
    if len(gate_cells):
        for _, c in gate_cells.iterrows():
            print(f"  {c['active']:<20}{c['pf_tier']:<18} ρtgt {c['rho_target']:+.1f} (real {c['rho_real']:+.2f})"
                  f"  -> pass {c['pass']:.2%} bust {c['bust']:.2%} p99 {c['p99']:.2%}  Δp99 {c['dp99']*100:+.2f}pp")
        mp = gate_cells.iloc[0]
        print(f"\nMINIMUM gate-restoring profile (weakest that clears): {mp['active']}, {mp['pf_tier']}, "
              f"ρ_stress {mp['rho_target']:+.1f}.")
    else:
        print("  NONE — no single synthetic profile at this risk weight restores both gates.")
    p99_only = df[df["dp99"] < 0].sort_values("dp99")
    print(f"\nCells that cap p99 below the 4-leg value ({b_p99:.2%}): {len(p99_only)} / {len(df)} "
          f"(condition (ii) of §4).")
    print()

    # ── risk-weight sensitivity at the strongest helpful profile ───────────
    print("RISK-WEIGHT SENSITIVITY at ρ_stress=-0.6 / solid PF~1.5 / Thu-Fri fill:")
    for risk5 in (0.0025, 0.0050, 0.0075):
        synth, diag = make_synth({3, 4}, "solid(PF~1.5)", -0.6, risk5, seed=777)
        r = mc_5leg(synth, risk5)
        print(f"  risk {risk5:.2%} (total {2.91+risk5*100:.2f}%): pass {r['pass_rate']:.2%} "
              f"bust {r['bust_rate']:.2%} p99 {r['p99_dd']:.2%} median {r['median_days_to_pass']}d  "
              f"(Δp99 {(r['p99_dd']-b_p99)*100:+.2f}pp, gates {'OK' if r['bust_rate']<0.01 and r['p99_dd']<0.05 else 'breach'})")
    print()

    json.dump({"baseline": {"pass": b_pass, "bust": b_bust, "p99": b_p99, "median": b_med},
               "cells": rows}, open(OUT / "fifth_leg_surface.json", "w"), indent=2)
    print("Saved fifth_leg_surface.json")
    print()
    print("=" * 100)
    print("COPPER-SHORT MAPPING (memory's #1 candidate) — where a global-growth-proxy short sits:")
    print("  * ρ_stress: the 4-leg worst windows (2020 COVID, 2021-22 rate-shock, 2022 bear) are")
    print("    RISK-OFF / growth-scare episodes. Copper (Dr. Copper) falls in those -> a copper")
    print("    SHORT prints GREEN exactly there -> ρ_stress NEGATIVE, plausibly -0.3..-0.6.")
    print("  * active days: copper trades the full week -> can be scheduled to FILL the Thu/Fri gap")
    print("    (the portfolio's thinnest coverage; Striker DJ30 Fri is the only current Fri leg).")
    print("  * required edge: read the minimum gate-restoring PF off the surface at ρ≈-0.4, Thu/Fri.")
    print("    That is the bar a real copper-short backtest must clear AFTER costs before it earns")
    print("    a validation loop. Instrument selection stays a separate INQHIORI loop (forbidden #6).")


if __name__ == "__main__":
    main()
