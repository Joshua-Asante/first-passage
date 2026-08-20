#!/usr/bin/env python3
"""N-SURV single-history magnitude-blindspot probe -- applied to ORB-MNQ-1's OWN book.

NOT a lab/analysis/ campaign; NOT a re-open of anything. Informal $0.00 spend,
zero K probe answering the question the HOLD notice raised
(`docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md`) for a
SECOND, independently-fitted book -- notice §3-C's own open item ("only c1 has been
tested"). Touches no locked/frozen repo file; writes only to this directory.

===============================================================================
WHAT THIS DOES
===============================================================================
1. Reuses `family_skewed_gamma.py` (geofit_skewed_family_construction_2026-08-15),
   UNCHANGED, fit to ORB-MNQ-1's OWN active-day daily P&L (not the 2-leg c1 book
   the notice's own characterize.json used).
2. Reuses ORB-MNQ-1's own already-validated intraday-honest reconstruction
   (orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py) unchanged
   -- Control B mirror check re-run here as this script's own precondition, not
   re-derived from raw bars.
3. Draws N=50 fresh synthetic realizations from the fitted family (seeds
   20260820100-20260820149, matching the notice's own N=50 for direct
   methodological comparability) and runs the SAME cushion-sizing gate check
   (day_loop_intraday / build_paths_orb / run_policy_orb / pol_cushion, all
   imported unchanged from run_evalseq_orb_intraday.py) that tonight's cushion
   probe ran on the single real historical draw.

===============================================================================
SCOPE DECISION -- intraday-honest vs EOD-only for synthetic realizations
(record the reasoning, not just the choice; read this before trusting §5/§6)
===============================================================================
`family_skewed_gamma.fit_family`/`draw_series` are documented (its own module
docstring) as modeling ONE thing: the daily EOD P&L magnitude, i.i.d. across
active days. They do not -- and were never built to -- produce a paired
intraday-LOW companion for each synthetic day. `day_loop_intraday`'s bust test
is `equity_test = bal_open + min(d, d_low)` where `d = pnl*m`, `d_low = low*m`.
Fabricating a `low` companion for a synthetic day (e.g. bootstrapping the real
book's giveback/pnl ratio) was explored and REJECTED: the real book's own
giveback-to-pnl ratio for win days is itself extremely heavy-tailed (mean 2.88x,
median 0.54x, max 468x, weak/negative correlation with the win's own size --
measured this session, not assumed), so any resampled ratio applied to a
synthetic magnitude produces either an impossible low (low > pnl, e.g. giveback
ratio 8x applied to a $3000 synthetic win needs a low of -$24000, itself an
uncontrolled second fabricated tail) or an arbitrary clip that would itself be
the finding. Inventing an unvalidated joint mechanism here would be exactly the
"new mechanism" this probe should NOT be inventing -- it is out of scope for a
$0 informal probe and belongs, if ever built, in a dedicated successor brief
(the geofit README already flags "CFD-book scope" and other open items the
SAME way: deferred, not invented ad hoc).

Resolution: this probe measures the N=50 distribution EOD-only
(`use_intraday=False`, a pre-existing, unmodified parameter of
`day_loop_intraday` -- not a new code path). Load-bearing check BEFORE trusting
this substitution: this script recomputes the REAL book's own full-panel
pol_cushion result under BOTH use_intraday=True and use_intraday=False and
confirms they are identical (bust 0.00% / pass 52.27% either way -- pol_cushion's
own de-risking multiplier caps at 0.75x and shrinks toward 0 as cushion shrinks
toward the trailing floor, which dominates the intraday/EOD distinction for this
policy on this book). This does not prove the same equivalence holds inside
every one of the 50 synthetic realizations individually, but it is measured,
not assumed, on the one draw where both are checkable -- and it is reported
explicitly, not buried, as the scope caveat that qualifies every number below.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tradeify-bottleneck-solutions-84e1e6")
CUSHION_DIR = REPO / "lab" / "analysis" / "c1" / "orbmnq1_cushion_sizing_probe_2026-08-20"
GEOFIT_DIR = REPO / "lab" / "analysis" / "c1" / "geofit_skewed_family_construction_2026-08-15"
ORB_LIB_DIR = REPO / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
OUT_DIR = Path(__file__).resolve().parent

for _p in (REPO / "core", REPO / "lab", ORB_LIB_DIR, CUSHION_DIR, GEOFIT_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import run_evalseq_orb_intraday as E  # noqa: E402  (unchanged reuse)
import family_skewed_gamma as F  # noqa: E402  (unchanged reuse)
from discovery.prop_survivor_scoring import load_scoring_thresholds  # noqa: E402

N_REALIZATIONS = 50
SEED_BASE = 20260820100
TIER = "Tradeify_Select_100K"
K = 1  # task-specified: same k=1 the cushion probe's headline used


def daily_skew(active: np.ndarray) -> float:
    m = active - active.mean()
    return float((m ** 3).mean() / (m ** 2).mean() ** 1.5)


def build_real_recon_and_panel():
    panel_pkl = E.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    inst = E.make_inst()
    import orb_lib as ol
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = E.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    E.assert_mirror_matches_engine(recon, bt)  # Control B mirror check, re-run as precondition
    panel1 = E.build_k_panel(recon, K)
    return recon, panel1


def main() -> int:
    t0 = time.time()
    report: dict = {"n_realizations": N_REALIZATIONS, "seed_base": SEED_BASE, "k": K, "tier": TIER}

    thr = load_scoring_thresholds()
    if thr.eval_bust_ceiling != 0.03 or thr.pass_floor != 0.5:
        print(f"[probe] PHASE0: gate ceilings drifted: {thr}", file=sys.stderr)
        return 3
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon} seeds={thr.seeds} sims/seed={thr.sims_per_seed} "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%} pass_floor={thr.pass_floor:.0%}")

    print("\n" + "=" * 96)
    print("STEP 1 -- reconstruct ORB-MNQ-1's own daily P&L (Control B mirror check)")
    print("=" * 96)
    recon, panel1 = build_real_recon_and_panel()
    print(f"  Control B mirror check: PASS (n={len(recon)})")
    n_bdays = len(panel1)
    print(f"  full k={K} panel: {n_bdays} business days "
          f"({panel1.index.min().date()} -> {panel1.index.max().date()})")

    active_series = panel1.loc[panel1["pnl"] != 0.0, "pnl"]
    active = active_series.to_numpy(dtype=float)
    real_mean = float(active.mean())
    real_sd = float(active.std(ddof=1))
    real_skew = daily_skew(active)
    real_worst = float(active.min())
    real_max = float(active.max())
    real_p_win = float((active > 0).mean())
    print(f"  n_active={active.size}  mean={real_mean:.2f}  sd={real_sd:.2f}  skew={real_skew:+.4f}  "
          f"worst_day={real_worst:.2f}  max_day={real_max:.2f}  p_win={real_p_win:.4f}")
    report["real_book"] = dict(n_bdays=n_bdays, n_active=int(active.size), mean=real_mean, sd=real_sd,
                                skew=real_skew, worst_day=real_worst, max_day=real_max, p_win=real_p_win)

    print("\n" + "=" * 96)
    print("STEP 2 -- fit skewed-gamma family to ORB-MNQ-1's OWN active-day P&L")
    print("=" * 96)
    params = F.fit_family(active)
    print(f"  fitted params: {json.dumps({k: round(v, 4) if isinstance(v, float) else v for k, v in params.items()})}")
    report["fitted_params"] = params

    print("\n" + "=" * 96)
    print("STEP 3 -- fidelity check: real book's own single-history cushion result, "
          "intraday-honest vs EOD-only")
    print("=" * 96)
    bpnl_real, blow_real = E.blocks_from_panel(panel1)
    r_intraday = E.run_policy_orb(bpnl_real, blow_real, E.pol_cushion, use_intraday=True,
                                   horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    r_eod = E.run_policy_orb(bpnl_real, blow_real, E.pol_cushion, use_intraday=False,
                              horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
    print(f"  real book, intraday-honest: bust={r_intraday['bust_pct']:.4f}%  pass={r_intraday['pass_pct']:.4f}%")
    print(f"  real book, EOD-only       : bust={r_eod['bust_pct']:.4f}%  pass={r_eod['pass_pct']:.4f}%")
    equivalence_ok = (abs(r_intraday["bust_pct"] - r_eod["bust_pct"]) < 1e-9
                       and abs(r_intraday["pass_pct"] - r_eod["pass_pct"]) < 1e-9)
    print(f"  EOD-only == intraday-honest on the real draw: {equivalence_ok} "
          f"(load-bearing check for the EOD-only substitution used on synthetic draws below)")
    real_floor_ok = bool(r_intraday["bust_pct"] <= 3.0 and r_intraday["pass_pct"] >= 50.0)
    report["real_single_history_cushion"] = dict(
        intraday_honest=r_intraday, eod_only=r_eod, equivalence_ok=equivalence_ok, floor_ok=real_floor_ok,
    )

    print("\n" + "=" * 96)
    print(f"STEP 4/5 -- draw N={N_REALIZATIONS} synthetic realizations, gate-check each (EOD-only, "
          "see module docstring 'SCOPE DECISION')")
    print("=" * 96)
    seeds = [SEED_BASE + i for i in range(N_REALIZATIONS)]
    runs = []
    for i, seed in enumerate(seeds):
        s = F.draw_series(params, seed, n_bdays)
        s_active = s[s != 0.0]
        skew_i = daily_skew(s_active) if s_active.size > 2 else float("nan")
        worst_i = float(s_active.min()) if s_active.size else float("nan")

        synth_panel = pd.DataFrame({"pnl": s, "low": s}, index=panel1.index)
        bpnl_s, blow_s = E.blocks_from_panel(synth_panel)
        t1 = time.time()
        r = E.run_policy_orb(bpnl_s, blow_s, E.pol_cushion, use_intraday=False,
                              horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        wall = time.time() - t1
        floor_ok = bool(r["bust_pct"] <= 3.0 and r["pass_pct"] >= 50.0)
        runs.append(dict(seed=seed, n_active=int(s_active.size), realized_skew=skew_i,
                          realized_worst_day=worst_i, bust_pct=r["bust_pct"], pass_pct=r["pass_pct"],
                          floor_ok=floor_ok, wall_s=round(wall, 1)))
        print(f"  [{i+1:2d}/{N_REALIZATIONS}] seed={seed}  n_active={s_active.size}  "
              f"skew={skew_i:+.3f}  worst={worst_i:.2f}  bust={r['bust_pct']:.4f}%  "
              f"pass={r['pass_pct']:.4f}%  floor_ok={floor_ok}  ({wall:.1f}s, total {time.time()-t0:.0f}s)")

    bust = np.array([r["bust_pct"] for r in runs])
    passp = np.array([r["pass_pct"] for r in runs])
    skews = np.array([r["realized_skew"] for r in runs])
    worsts = np.array([r["realized_worst_day"] for r in runs])
    n_floor_ok = int(sum(r["floor_ok"] for r in runs))

    print("\n" + "=" * 96)
    print("STEP 6 -- distribution summary")
    print("=" * 96)
    bust_pcts = {p: float(np.percentile(bust, p)) for p in (10, 25, 50, 75, 90)}
    print(f"  bust%  mean={bust.mean():.4f}  median={np.median(bust):.4f}  sd={bust.std(ddof=1):.4f}  "
          f"min={bust.min():.4f}  max={bust.max():.4f}")
    print(f"  bust%  percentiles: " + " ".join(f"p{p}={v:.4f}" for p, v in bust_pcts.items()))
    print(f"  pass%  mean={passp.mean():.4f}  median={np.median(passp):.4f}  sd={passp.std(ddof=1):.4f}  "
          f"min={passp.min():.4f}  max={passp.max():.4f}")
    print(f"  n realizations clearing floor_ok (bust<=3.0% AND pass>=50%): {n_floor_ok}/{N_REALIZATIONS} "
          f"({n_floor_ok/N_REALIZATIONS:.1%})")
    n_zero_bust = int((bust <= 1e-9).sum())
    print(f"  n realizations with bust==0.00%: {n_zero_bust}/{N_REALIZATIONS} ({n_zero_bust/N_REALIZATIONS:.1%})")
    # percentile rank of the real single-history bust value (0.00%) within the 50-draw distribution
    real_bust = r_intraday["bust_pct"]
    rank_pct = float((bust <= real_bust).mean() * 100.0)
    print(f"  real single-history bust ({real_bust:.4f}%) rank within the 50-draw distribution: "
          f"{rank_pct:.1f}th percentile (fraction of synthetic draws AT OR BELOW the real value)")

    fidelity = dict(
        real_skew=real_skew, real_worst_day=real_worst,
        synth_skew_mean=float(np.nanmean(skews)), synth_skew_median=float(np.nanmedian(skews)),
        synth_skew_min=float(np.nanmin(skews)), synth_skew_max=float(np.nanmax(skews)),
        synth_worst_mean=float(np.nanmean(worsts)), synth_worst_median=float(np.nanmedian(worsts)),
        synth_worst_min=float(np.nanmin(worsts)), synth_worst_max=float(np.nanmax(worsts)),
    )
    print(f"\n  FIDELITY CHECK: real skew {real_skew:+.4f} vs synthetic-draw skew "
          f"mean={fidelity['synth_skew_mean']:+.4f} median={fidelity['synth_skew_median']:+.4f} "
          f"(range {fidelity['synth_skew_min']:+.4f}..{fidelity['synth_skew_max']:+.4f})")
    print(f"  FIDELITY CHECK: real worst-day {real_worst:.2f} vs synthetic-draw worst-day "
          f"mean={fidelity['synth_worst_mean']:.2f} median={fidelity['synth_worst_median']:.2f} "
          f"(range {fidelity['synth_worst_min']:.2f}..{fidelity['synth_worst_max']:.2f})")

    report["runs"] = runs
    report["distribution"] = dict(
        bust_mean=float(bust.mean()), bust_median=float(np.median(bust)), bust_sd=float(bust.std(ddof=1)),
        bust_min=float(bust.min()), bust_max=float(bust.max()), bust_percentiles=bust_pcts,
        pass_mean=float(passp.mean()), pass_median=float(np.median(passp)), pass_sd=float(passp.std(ddof=1)),
        pass_min=float(passp.min()), pass_max=float(passp.max()),
        n_floor_ok=n_floor_ok, frac_floor_ok=n_floor_ok / N_REALIZATIONS,
        n_zero_bust=n_zero_bust, frac_zero_bust=n_zero_bust / N_REALIZATIONS,
        real_bust_rank_percentile=rank_pct,
    )
    report["fidelity_check"] = fidelity
    report["wall_s_total"] = round(time.time() - t0, 1)

    out = OUT_DIR / "nsurv_magnitude_probe_results.json"
    out.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
