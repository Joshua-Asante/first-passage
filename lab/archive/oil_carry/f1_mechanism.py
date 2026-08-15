"""F1 mechanism falsifier for CONCEPT-USOIL-CARRY-001 (Helios).

Question: does conditioning on WTI futures-curve backwardation SEPARATE forward
returns from contango, or is Helios a disguised long-oil trend trade?

Pre-registered design (grounded in the verified Databento CL panel):

* Curve-state signal  : backwardation == close(CL.c.0) > close(CL.c.1) at day D.
* LAG (no look-ahead) : the signal at day D's close conditions the forward
                        return whose holding window STARTS the next bar (D+1).
                        Implemented as state.shift(1) relative to the return
                        indexed at its start bar. Strictly leak-free: entry is
                        the bar AFTER the curve is observed (stricter than the
                        brief's literal "[T, T+h] on state(T)", which would
                        enter at the same close the settle is read from).
* Forward return      : r_h[t] = close_c0[t+h] / close_c0[t] - 1.
* Roll filter         : drop any window whose front contract (iid_c0) is not
                        constant over [t, t+h] — a cross-contract ratio is not a
                        tradable return (verified hazard: 2020-04 May->June roll).
* Negative-price filter: drop any window touching close_c0 <= 0 (verified
                        hazard: 2020-04-20 settled negative; a % return through
                        zero is undefined). Counts reported, never silent.
* R unit              : R == pooled standard deviation of the h-day forward
                        return across BOTH states. With entry/exit logic stripped
                        for F1 there is no stop-distance R, so the principled
                        analog is a volatility unit; gap/R is then a standardized
                        effect size. Raw % gap is also reported.

PASS (primary horizon = 5d): two-sample Welch p <= 0.05 AND
(mean_backwardation - mean_contango) >= 0.15 R AND the label-permutation null
corroborates (p <= 0.05). Otherwise FAIL -> Helios is a disguised trend trade.

SWAP NOTE: the brief asked for returns "net of a modeled long-swap accrual".
No USOIL swap rate exists in-repo (docs/external/fxify_swap_rates_2026-05-25.md
has only XAUUSD/USDJPY/DJ30/NAS100). The Alchemy "+174.5 pts/lot" credit cited
in the handoff is a backwardation-PERIOD figure; modeling swap as a function of
curve state would inject the very signal under test (circular). F1 therefore
tests GROSS price-return separation (the falsifiable core: does curve state move
the directional/roll return). A state-INDEPENDENT flat swap shifts both cohorts
equally and cannot manufacture separation, so it is omitted from the verdict and
flagged for the deferred build.
"""
from __future__ import annotations

import argparse

import numpy as np
from scipy import stats

from analysis.oil_carry.curve_loader import load_curve_panel, regime_report
from research_utils.permutation import label_permutation_test

HORIZONS = (1, 5, 10)
PRIMARY_H = 5
P_THRESH = 0.05
R_GAP_THRESH = 0.15


def build_forward_returns(df, h: int):
    """Return (r, s, dropped) where r/s are aligned forward-return / lagged-state
    arrays and dropped is a {reason: count} dict. Leak-free one-bar lag."""
    c0 = df["close_c0"].to_numpy(dtype=float)
    iid = df["iid_c0"].to_numpy()
    state = df["state"].to_numpy(dtype=int)
    n = len(df)

    r_list, s_list = [], []
    dropped = {"roll": 0, "nonpos": 0}
    # t = forward-window start bar; needs a prior bar (t-1) for the lagged signal
    # and t+h within range.
    for t in range(1, n - h):
        entry, exit_ = c0[t], c0[t + h]
        if entry <= 0 or exit_ <= 0:
            dropped["nonpos"] += 1
            continue
        if np.unique(iid[t : t + h + 1]).size != 1:
            dropped["roll"] += 1
            continue
        r_list.append(exit_ / entry - 1.0)
        s_list.append(state[t - 1])  # lagged: signal from the prior bar's close
    return np.asarray(r_list), np.asarray(s_list), dropped


def run_horizon(df, h: int) -> dict:
    r, s, dropped = build_forward_returns(df, h)
    back = r[s == 1]
    cont = r[s == 0]
    pooled_sd = float(np.std(r, ddof=1))
    gap = float(back.mean() - cont.mean())
    gap_R = gap / pooled_sd if pooled_sd > 0 else float("nan")

    t_stat, t_p = stats.ttest_ind(back, cont, equal_var=False)
    u_stat, u_p = stats.mannwhitneyu(back, cont, alternative="two-sided")

    # Label-permutation null (reuse oanda_stage1 helper): blocked subset first.
    pop = np.concatenate([back, cont])
    _, _, perm_p = label_permutation_test(pop, len(back), n_perm=2000, seed=42)

    passed = (t_p <= P_THRESH) and (gap_R >= R_GAP_THRESH) and (perm_p <= P_THRESH)
    return {
        "h": h, "n_back": len(back), "n_cont": len(cont), "dropped": dropped,
        "mean_back": float(back.mean()), "mean_cont": float(cont.mean()),
        "gap_pct": gap * 100, "pooled_sd_pct": pooled_sd * 100, "gap_R": gap_R,
        "t_p": float(t_p), "u_p": float(u_p), "perm_p": float(perm_p),
        "passed": bool(passed),
    }


def print_horizon(res: dict) -> None:
    h = res["h"]
    tag = " (PRIMARY)" if h == PRIMARY_H else ""
    print(f"--- horizon {h}d{tag} ---")
    print(f"  N: backwardation {res['n_back']}  /  contango {res['n_cont']}"
          f"   (dropped: roll {res['dropped']['roll']}, nonpos {res['dropped']['nonpos']})")
    print(f"  mean fwd return  : backw {res['mean_back']*100:+.3f}%   contango {res['mean_cont']*100:+.3f}%")
    print(f"  gap (back-cont)  : {res['gap_pct']:+.3f}%   pooled SD {res['pooled_sd_pct']:.3f}%   => {res['gap_R']:+.3f} R")
    print(f"  Welch t p        : {res['t_p']:.4f}      Mann-Whitney p: {res['u_p']:.4f}      permutation p: {res['perm_p']:.4f}")
    crit = (f"p<={P_THRESH} [{ 'Y' if res['t_p']<=P_THRESH else 'N'}]  "
            f"gap>={R_GAP_THRESH}R [{ 'Y' if res['gap_R']>=R_GAP_THRESH else 'N'}]  "
            f"perm<={P_THRESH} [{ 'Y' if res['perm_p']<=P_THRESH else 'N'}]")
    print(f"  verdict          : {'PASS' if res['passed'] else 'FAIL'}   ({crit})")
    print()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Helios F1 mechanism falsifier")
    ap.add_argument("--horizon", type=int, default=None, help="run a single horizon")
    ap.add_argument("--report-regime-counts", action="store_true")
    ap.add_argument("--rebuild", action="store_true", help="force refetch the panel")
    args = ap.parse_args(argv)

    df = load_curve_panel(rebuild=args.rebuild)

    if args.report_regime_counts:
        print(regime_report(df))
        print()

    print("=" * 72)
    print("F1 mechanism falsifier — CONCEPT-USOIL-CARRY-001 (Helios, WTI carry)")
    print(f"Source: Databento GLBX.MDP3 CL.c.0/CL.c.1  |  panel {df['date'].min().date()} -> {df['date'].max().date()}")
    print("=" * 72)
    print()

    horizons = (args.horizon,) if args.horizon else HORIZONS
    results = {h: run_horizon(df, h) for h in horizons}
    for h in horizons:
        print_horizon(results[h])

    if PRIMARY_H in results:
        pr = results[PRIMARY_H]
        verdict = "PASS" if pr["passed"] else "FAIL"
        print("=" * 72)
        print(f"F1 VERDICT (primary {PRIMARY_H}d): {verdict}")
        if verdict == "FAIL":
            print("  -> Term-structure conditioning does not separate forward returns at the")
            print("     pre-registered bar. Helios is a disguised long-oil trend trade. REJECT.")
        else:
            print("  -> Curve state separates forward returns. Mechanism survives F1; recommend")
            print("     the deferred codify->sweep->validate handoff (gated also on F3 live-swap).")
        print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
