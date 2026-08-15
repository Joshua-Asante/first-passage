"""CC-handoff §2.6 follow-on — regime-robustness (half-panel) check on the 5th leg.

The 2026-06-07 HOLD ADR's binding finding: static de-risk (allocation k or
dd_protection) clears the FULL decompounded 2020-26 panel but FAILS the
regime-robustness gate — H1 (2020-2023 chop/crisis) busts 8.9-13.5%. Sizing
cannot fix the hard regime because all four legs are long-biased risk assets
that co-draw in risk-off.

The 5th-leg thesis is mechanistically different: a NEGATIVELY stress-correlated
leg offsets the co-drawdown rather than scaling it. This script applies the same
deterministic half-panel split (bday midpoint 2023-03-20, per the 2026-06-07
gate) to the 4-leg baseline AND a chosen synthetic 5th-leg profile, to test
whether the 5th leg's benefit is REGIME-ROBUST (clears H1) — the bar the de-risk
candidates could not clear.

Reuses the production MC + part-2 synthetic generator verbatim. Profile is read
from argv or defaults to the strongest helpful cell (ρ=-0.6 / solid PF / Thu-Fri).
"""
from __future__ import annotations

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
from analyze_part1 import run_mc, ACCOUNT, ALLOC, FIXED_1R, LABEL  # noqa: E402
import analyze_part2 as P2  # noqa: E402  (reuse make_synth + panel + worst_days)

panel = P2.panel
LEGS = list(panel.columns)
SPLIT = pd.Timestamp("2023-03-20")  # deterministic midpoint, per 2026-06-07 regime_gate


def _mc_on(idx_mask, synth=None, risk5=None):
    sub = panel.loc[idx_mask]
    trades = {leg: pd.DataFrame({"exit_date": sub.index, "pnl": sub[leg].to_numpy()}) for leg in LEGS}
    allocs = dict(ALLOC); fixed = dict(FIXED_1R)
    if synth is not None:
        ss = synth.loc[idx_mask]
        trades["synth5"] = pd.DataFrame({"exit_date": sub.index, "pnl": ss.to_numpy()})
        allocs["synth5"] = risk5; fixed["synth5"] = risk5 * ACCOUNT
    return run_mc(trades, allocs, fixed)


def _gate(r):
    return "CLEAR" if (r["bust_rate"] < 0.01 and r["p99_dd"] < 0.05) else "FAIL"


def _line(name, r):
    return (f"  {name:<26} pass {r['pass_rate']:>7.2%}  bust {r['bust_rate']:>6.2%}  "
            f"p99 {r['p99_dd']:>6.2%}  med {str(r['median_days_to_pass']):>4}d   -> {_gate(r)}")


def main():
    # profile: rho, pf_tier, active-day set, risk5
    rho = float(sys.argv[1]) if len(sys.argv) > 1 else -0.6
    pf_tier = sys.argv[2] if len(sys.argv) > 2 else "solid(PF~1.5)"
    active = sys.argv[3] if len(sys.argv) > 3 else "ThuFri"
    risk5 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0050
    active_wd = {3, 4} if active.lower().startswith("thu") else {0, 1}

    synth, diag = P2.make_synth(active_wd, pf_tier, rho, risk5, seed=4242)

    h1 = panel.index < SPLIT
    h2 = panel.index >= SPLIT
    print("=" * 92)
    print(f"§2.6 REGIME-ROBUSTNESS (half-panel split @ {SPLIT.date()}) — does the 5th leg clear the")
    print(f"     hard H1 regime that static de-risk could NOT (2026-06-07 ADR)?")
    print(f"5th-leg profile: ρ_stress {rho:+.1f} (real {diag['realized_rho']:+.2f}) / {pf_tier} "
          f"(real PF {diag['realized_pf']:.2f}) / {active} / risk {risk5:.2%}  n={diag['n_trades']}")
    print("=" * 92)
    print(f"H1 = {panel.index[h1].min().date()} -> {panel.index[h1].max().date()}  "
          f"({h1.sum()} bdays) | H2 = {panel.index[h2].min().date()} -> {panel.index[h2].max().date()}  ({h2.sum()} bdays)")
    print("Gate (each partition): bust < 1% AND p99 DD < 5%.\n")

    print("FULL PANEL 2020-26:")
    print(_line("4-leg baseline", _mc_on(np.ones(len(panel), bool))))
    print(_line("+ synth 5th leg", _mc_on(np.ones(len(panel), bool), synth, risk5)))
    print("\nH1 (2020-2023 chop/crisis — the hard regime):")
    b_h1 = _mc_on(h1); print(_line("4-leg baseline", b_h1))
    s_h1 = _mc_on(h1, synth, risk5); print(_line("+ synth 5th leg", s_h1))
    print("\nH2 (2023-2026 benign trend):")
    print(_line("4-leg baseline", _mc_on(h2)))
    print(_line("+ synth 5th leg", _mc_on(h2, synth, risk5)))
    print()
    print("VERDICT (regime-robustness of the 5th-leg lever):")
    if _gate(s_h1) == "CLEAR" and _gate(b_h1) == "FAIL":
        print("  The 5th leg CLEARS the hard H1 regime that the 4-leg baseline fails -> the")
        print("  negatively-stress-correlated leg is a REGIME-ROBUST lever where static de-risk was not.")
    elif _gate(s_h1) == "CLEAR":
        print("  Both clear H1 (baseline already clears at this split) — inspect bust/p99 deltas above.")
    else:
        print("  The 5th leg does NOT clear H1 at this profile/risk -> the synthetic offset is")
        print("  insufficient for the hard regime; the ENB-lift helps the average but not the tail.")
        print("  (Either a stronger ρ_stress / lower risk, or this confirms regime-adaptive sizing")
        print("   remains the only structural fix per the 2026-06-07 ADR.)")


if __name__ == "__main__":
    main()
