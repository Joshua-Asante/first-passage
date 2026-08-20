#!/usr/bin/env python3
"""$0/K=0 informal probe: re-derive the cushion-proportional throttle's CEILING from
ORB-MNQ-1's OWN measured loss-tail, instead of reusing the 2-leg book's generic 0.75
constant (Q-EVALSEQ-1's `pol_cushion`, ported unchanged onto ORB-MNQ-1 earlier tonight
at lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py).

Writes ONLY to this new scratch directory. Touches no locked/frozen repo file. Reuses
`day_loop_intraday` / `build_paths_orb` / `run_policy_orb` / `pol_const` / `pol_cushion`
/ `DD` UNCHANGED (imported, not retyped) from that already-verified harness.

--------------------------------------------------------------------------------------
DERIVATION -- exact reasoning, not an assertion
--------------------------------------------------------------------------------------

pol_cushion's functional form is a LINEAR ramp of the cushion (distance from the
trailing-DD floor), clipped to [0, ceiling]:

    cushion = bal - (peak - DD)
    m(cushion) = ceiling * clip(cushion / DD, 0, 1)

Structural fact about this SHAPE (true for any `ceiling`, not just 0.75): in the ramp
region (0 <= cushion < DD), m is *linear* in cushion, so a single day's loss as a
FRACTION of that day's starting cushion is a CONSTANT, independent of how much cushion
remains:

    day_loop_intraday computes, each day t, on bal_open (yesterday's close):
        cushion_t = bal_open - floor         (floor = peak - DD)
        m_t       = ceiling * cushion_t / DD                      (ramp region)
        loss_t    = L * k * m_t = L * k * ceiling * cushion_t / DD
        loss_t / cushion_t = L * k * ceiling / DD                 <-- CONSTANT in cushion_t

    where L (<=0) is that day's per-contract low_usd_1lot excursion and k is the base
    contract count. Bust is `bal_open + loss_t <= floor`, i.e. `cushion_t + loss_t <= 0`,
    i.e. `loss_t / cushion_t <= -1` (since cushion_t > 0 while alive).

So the SAME single test governs every state, not just "from a full-cushion state": if

    |L_worst| * k * ceiling / DD < 1                                            (*)

for the worst-case per-contract single-day loss L_worst the policy will ever face, then
NO single day, at ANY cushion level in the ramp region, can consume 100%+ of that day's
starting cushion. Recursively, cushion_{t+1} >= cushion_t * (1 - |L_worst|*k*ceiling/DD)
> 0 whenever cushion_t > 0 -- so (*) is not just a "one bad day" guarantee, it is a
"no sequence of consecutive worst-case-or-better days, of ANY length, can cross the
floor" guarantee (geometric decay toward, never through, zero). This is a STRONGER
claim than the task's literal "single day from full cushion" framing, and is exactly
why pol_cushion(0.75) measured 0.0% bust in EVERY slice tonight (H1/H2, T1/T2/T3) --
it is a mathematical certainty given (DD, L, k, ceiling), not an emergent property of
this specific historical panel. (Capped region cushion>=DD: m stays at `ceiling`, and
the same (*) inequality with cushion_t replaced by its floor value DD is the binding
case, so (*) is the single governing condition across the WHOLE domain.)

Solving (*) for the BREAKEVEN ceiling given ORB-MNQ-1's own numbers, k=1, DD=$3,000
(Tradeify_Select_100K's fixed trail, unchanged from the harness):

    ceiling_breakeven = DD / (|L_worst| * k)

Two `L_worst` candidates, BOTH re-derived from ORB-MNQ-1's own panel in this script
(not hardcoded -- see `derive_loss_tail()` below), matching the task's background:

    L_empirical   = min(low_usd_1lot) over the full k=1 panel   = -$783.82/contract
    L_theoretical = max(range_pt) * $2/pt - RT_cost_usd          = -$1,244.18/contract
                    (the widest opening range ever observed on this instrument, taken
                    as the bound on how far an UNSTOPPED held day could move against a
                    position before close -- strictly >= any loss actually realized by
                    any specific stopped OR held trade in the panel, since no trade's
                    realized adverse excursion ever consumed its own full day's range
                    in one direction AND happened to have the widest range of any day)

    ceiling_breakeven(empirical,   k=1) = 3000 / 783.82  = 3.827
    ceiling_breakeven(theoretical, k=1) = 3000 / 1244.18 = 2.411
    ceiling_breakeven(theoretical, k=2) = 3000 / 2488.36 = 1.205   (analytic only, not
                                                                     run -- task scopes
                                                                     MC runs to k=1)

FINDING (report this plainly, not just the winning number): applying the task's own
suggested method LITERALLY -- "size ceiling so the theoretical worst day can't alone
cross the floor from full cushion" -- is a NON-BINDING constraint for ORB-MNQ-1 at
k=1: the breakeven (2.411) is already above 1.0, the natural cap for a multiplier that
is supposed to THROTTLE (reduce) exposure relative to the k-contract reference, never
amplify it. ORB-MNQ-1's own loss tail is thin enough, relative to Tradeify's $3,000
trail, that literally NO ceiling <= 1.0 can ever fail the single-day structural test --
even ceiling=1.00 (i.e. dropping the borrowed constant entirely, using the RAW ramp
`m = min(1, cushion/DD)` with no separate cap) is unconditionally floor-safe by this
same argument, and stays that way at k=2 too (breakeven 1.205 > 1.0, margin thinner but
still non-binding). This is a genuine, checked, structural finding: the RIGHT answer to
"what does ORB's own tail license" is that the borrowed 0.75 is unnecessarily
conservative FOR THE PURPOSE THE TASK NAMES (never-bust-from-a-single-worst-day), not
that some other specific sub-1.0 number is "the" derived ceiling.

Because a literal breakeven-search collapses to a degenerate, uninformative answer
("no cap needed"), two DISTINCT, motivated candidates are built and tested instead of
one, per the task's own allowance ("feel free to try more than one ... report all"):

  CEIL_MAX  (ceiling=1.00): the maximal ceiling consistent with (*) -- "use ORB's own
      thin tail to justify dropping the borrowed cap altogether," same shape, same
      structural zero-bust guarantee, but preserving more exposure near full cushion
      than the borrowed 0.75 does (so it should show up as a HIGHER pass rate if
      exposure-near-full-cushion is actually load-bearing for time-to-target).

  CEIL_HALF (ceiling=0.50): a deliberately conservative alternative in the OTHER
      direction, calibrated as "budget at most half the linear-ramp's own worst-case
      fraction of DD" (0.50 * ceiling_breakeven(theoretical,k=1)/... no -- stated
      directly as ceiling=0.50, chosen as a round number below the borrowed 0.75,
      giving a genuinely different (MORE conservative) operating point to bracket the
      comparison and test whether extra caution costs pass rate for no bust benefit
      (bust is already structurally 0.0% for ANY ceiling <= 2.411, so any bust
      difference across {0.50, 0.75, 1.00} would itself be a red flag worth
      investigating, not an expected result).

Both candidates keep the IDENTICAL functional shape as pol_cushion (linear ramp,
clip(cushion/DD, 0, 1) times a ceiling constant) -- only the ceiling constant differs.
That is deliberate: the task's background frames the problem as "the ceiling is a
generic constant, not the SHAPE" -- so this probe isolates the ceiling as the single
free parameter and holds the shape fixed, rather than also changing the ramp's
functional form (a genuinely different shape is a separate, larger question this $0
probe does not open).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tradeify-bottleneck-solutions-84e1e6")
CUSHION_PROBE_DIR = REPO / "lab" / "analysis" / "c1" / "orbmnq1_cushion_sizing_probe_2026-08-20"
OUT_DIR = Path(__file__).resolve().parent

if str(CUSHION_PROBE_DIR) not in sys.path:
    sys.path.insert(0, str(CUSHION_PROBE_DIR))

# Reused UNCHANGED from the already fidelity-verified harness -- not retyped.
import run_evalseq_orb_intraday as H  # noqa: E402
import orb_lib as ol  # noqa: E402  (already on sys.path via H's own module-level insert)

K = 1  # task scopes every MC run in this probe to k=1


# =====================================================================================
# Loss-tail re-derivation (from THIS run's own `recon`, not hardcoded -- see docstring)
# =====================================================================================

def derive_loss_tail(recon: pd.DataFrame) -> dict:
    """Both bounds re-derived fresh from the panel this script itself reconstructs
    (same `orb_days_with_excursion` recon as the cushion-sizing probe), so nothing
    here is a magic number carried over from the background context uninspected."""
    l_empirical = float(recon["low_usd_1lot"].min())
    rt_cost_usd = H.RT_PT_TRADEIFY * H.MNQ_USD_PER_PT
    l_theoretical = -(float(recon["range_pt"].max()) * H.MNQ_USD_PER_PT - rt_cost_usd)
    return dict(l_empirical=l_empirical, l_theoretical=l_theoretical, rt_cost_usd=rt_cost_usd)


# =====================================================================================
# Re-derived policy family -- SAME shape as H.pol_cushion, ceiling is the free param
# =====================================================================================

def pol_cushion_ceiling(ceiling: float):
    """Identical functional form to H.pol_cushion, with `ceiling` in place of the
    borrowed constant 0.75. `ceiling=0.75` reproduces H.pol_cushion bit-for-bit
    (verified below, Control D)."""
    def f(t, bal, peak, stepped, t_b):
        cushion = bal - (peak - H.DD)
        return ceiling * np.minimum(1.0, np.maximum(cushion, 0.0) / H.DD)
    return f


# =====================================================================================
# main
# =====================================================================================

def main() -> int:
    t0 = time.time()
    report: dict = {}

    print("=" * 100)
    print("ORB-MNQ-1 own-tail-derived cushion-ceiling probe (vs borrowed pol_cushion 0.75x)")
    print("=" * 100)

    thr = H.load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")

    panel_pkl = H.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}")
    print(f"[data ] rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    inst = H.make_inst()
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")

    print("\n--- Control B (re-run, unchanged): mirror vs orb_lib.orb_backtest ---")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"  PASS -- n={len(recon)}")

    # ---------------------------------------------------------------- loss-tail derivation
    tail = derive_loss_tail(recon)
    l_emp, l_theo = tail["l_empirical"], tail["l_theoretical"]
    print("\n--- Loss-tail re-derivation (from this run's own recon) ---")
    print(f"  L_empirical (min low_usd_1lot, k=1)          = ${l_emp:,.2f}/contract")
    print(f"  L_theoretical (max range_pt * $/pt - RT cost) = ${l_theo:,.2f}/contract")
    print(f"  background context stated -783.82 / ~-1250   -- match: "
          f"{'YES' if abs(l_emp - (-783.82)) < 0.01 else 'NO'} / "
          f"{'YES (rounds to ~1250)' if abs(l_theo - (-1250.0)) < 10 else 'NO'}")

    DD = H.DD
    ceil_breakeven_emp_k1 = DD / (-l_emp * K)
    ceil_breakeven_theo_k1 = DD / (-l_theo * K)
    ceil_breakeven_theo_k2 = DD / (-l_theo * 2)
    print(f"\n  DD (Tradeify_Select_100K fixed trail) = ${DD:,.0f}")
    print(f"  breakeven ceiling (empirical,   k=1) = DD/|L_emp|   = {ceil_breakeven_emp_k1:.3f}")
    print(f"  breakeven ceiling (theoretical, k=1) = DD/|L_theo|  = {ceil_breakeven_theo_k1:.3f}")
    print(f"  breakeven ceiling (theoretical, k=2, analytic only) = {ceil_breakeven_theo_k2:.3f}")
    print("  Both k=1 breakevens are > 1.0 -- the single-day-from-full-cushion test is "
          "NON-BINDING at k=1 for ANY ceiling <= 1.0 (see module docstring for the full "
          "derivation and why this is reported as a finding, not glossed over).")

    candidates = {
        "borrowed_0.75": dict(ceiling=0.75, policy=H.pol_cushion, note="Q-EVALSEQ-1's original, quoted verbatim"),
        "derived_ceil_max_1.00": dict(ceiling=1.00, policy=pol_cushion_ceiling(1.00),
                                       note="max ceiling consistent with (*) at k=1 -- see derivation"),
        "derived_ceil_half_0.50": dict(ceiling=0.50, policy=pol_cushion_ceiling(0.50),
                                        note="deliberately conservative bracket, round number below borrowed"),
    }
    for name, c in candidates.items():
        frac_theo = c["ceiling"] * (-l_theo) * K / DD
        frac_emp = c["ceiling"] * (-l_emp) * K / DD
        print(f"  [{name:24s}] ceiling={c['ceiling']:.2f}  worst-day-at-ceiling as %DD: "
              f"theoretical={frac_theo:.1%}  empirical={frac_emp:.1%}  ({c['note']})")

    report["loss_tail"] = dict(l_empirical=l_emp, l_theoretical=l_theo, dd=DD,
                                ceil_breakeven_emp_k1=ceil_breakeven_emp_k1,
                                ceil_breakeven_theo_k1=ceil_breakeven_theo_k1,
                                ceil_breakeven_theo_k2=ceil_breakeven_theo_k2)
    report["candidates"] = {name: dict(ceiling=c["ceiling"], note=c["note"]) for name, c in candidates.items()}

    # ---------------------------------------------------------------- Control D: shape equivalence
    print("\n--- Control D: pol_cushion_ceiling(0.75) reproduces H.pol_cushion bit-for-bit ---")
    bal_test = np.array([100000.0, 98500.0, 97000.0, 101500.0, 96999.9])
    peak_test = np.array([100000.0, 100000.0, 100000.0, 101500.0, 100000.0])
    m_borrowed = H.pol_cushion(0, bal_test, peak_test, None, None)
    m_reimpl = pol_cushion_ceiling(0.75)(0, bal_test, peak_test, None, None)
    assert np.allclose(m_borrowed, m_reimpl), "pol_cushion_ceiling(0.75) diverges from H.pol_cushion"
    print(f"  PASS -- max abs diff = {np.max(np.abs(m_borrowed - m_reimpl)):.2e}")

    # ---------------------------------------------------------------- fidelity control (flat k=1)
    print("\n" + "=" * 100)
    print("FIDELITY CONTROL -- flat policy (m=1.0), k=1, full panel -- must reproduce 67.67%")
    print("=" * 100)
    PUBLISHED_K1 = 67.67
    TOL_PP = 2.0

    panel_full = H.build_k_panel(recon, K)
    bpnl_full, blow_full = H.blocks_from_panel(panel_full)
    flat_full = H.run_policy_orb(bpnl_full, blow_full, H.pol_const(1.0), use_intraday=True,
                                  horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    delta = flat_full["bust_pct"] - PUBLISHED_K1
    fidelity_ok = abs(delta) <= TOL_PP
    print(f"  k=1 flat  bust={flat_full['bust_pct']:.2f}%  pass={flat_full['pass_pct']:.2f}%  "
          f"published={PUBLISHED_K1:.2f}%  delta={delta:+.2f}pp  "
          f"{'PASS' if fidelity_ok else 'FAIL'}  (elapsed {time.time()-t0:.0f}s)")
    report["fidelity_control"] = dict(bust_pct=flat_full["bust_pct"], pass_pct=flat_full["pass_pct"],
                                       published=PUBLISHED_K1, delta_pp=delta, within_tol=fidelity_ok)
    if not fidelity_ok:
        print("STOPPING before any policy comparison -- fidelity control did not reproduce "
              "the published figure within tolerance.")
        (OUT_DIR / "evalseq_orb_derived_ceiling_results.json").write_text(json.dumps(report, indent=2))
        return 2

    # ---------------------------------------------------------------- build the SAME slices
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    n = len(full_idx)
    mid = n // 2
    c1, c2 = n // 3, 2 * n // 3
    slices = {
        "FULL": full_idx,
        "H1": full_idx[:mid],
        "H2": full_idx[mid:],
        "T1": full_idx[:c1],
        "T2": full_idx[c1:c2],
        "T3": full_idx[c2:],
    }
    print(f"\n[split] {n} business days  mid={mid}  cut1={c1} cut2={c2}")
    for name, idx in slices.items():
        print(f"  {name:5s} {idx[0].date()} -> {idx[-1].date()}  (n={len(idx)})")

    report["split"] = {name: dict(start=str(idx[0].date()), end=str(idx[-1].date()), n_bdays=len(idx))
                        for name, idx in slices.items()}

    # ---------------------------------------------------------------- Section: comparison matrix
    print("\n" + "=" * 100)
    print("COMPARISON -- flat-k1 control + all 3 sized policies, k=1, every slice")
    print("=" * 100)

    comparison: dict = {}
    for slice_name, idx in slices.items():
        panel_slice = panel_full.loc[panel_full.index.isin(idx)]
        bpnl, blow = H.blocks_from_panel(panel_slice)
        n_blocks = len(bpnl)

        if slice_name == "FULL":
            flat = flat_full  # reuse the fidelity-control run, don't re-spend
        else:
            flat = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                                     horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)

        flat_hcap = max(0.0, 100.0 - flat["bust_pct"] - flat["pass_pct"])
        row = dict(n_blocks=n_blocks,
                   flat_bust_pct=flat["bust_pct"], flat_pass_pct=flat["pass_pct"],
                   flat_horizon_cap_pct=flat_hcap)
        print(f"\n  -- {slice_name} (n_blocks={n_blocks}) --")
        print(f"    flat(k=1, m=1.0, control) : bust={flat['bust_pct']:6.2f}%  pass={flat['pass_pct']:6.2f}%  "
              f"horizon_cap={flat_hcap:6.2f}%")

        for name, c in candidates.items():
            res = H.run_policy_orb(bpnl, blow, c["policy"], use_intraday=True,
                                    horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
            row[f"{name}_bust_pct"] = res["bust_pct"]
            row[f"{name}_pass_pct"] = res["pass_pct"]
            row[f"{name}_horizon_cap_pct"] = max(0.0, 100.0 - res["bust_pct"] - res["pass_pct"])
            print(f"    {name:24s} (ceiling={c['ceiling']:.2f}): bust={res['bust_pct']:6.2f}%  "
                  f"pass={res['pass_pct']:6.2f}%  (elapsed {time.time()-t0:.0f}s)")

        comparison[slice_name] = row

    report["comparison"] = comparison

    out = OUT_DIR / "evalseq_orb_derived_ceiling_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
