#!/usr/bin/env python3
"""Stage 2: trailing (causal) MNQ realized-vol regime classifier -> re-run the SAME
cushion-proportional-sizing Tradeify survivor-scoring gate check on each regime
bucket, k=1. Reuses day_loop_intraday / build_paths_orb / run_policy_orb /
pol_cushion / pol_const / build_k_panel / blocks_from_panel from
run_evalseq_orb_intraday.py UNCHANGED (imported, not retyped). $0/K=0, writes only
to scratch.

Regime variable: rolling 63-trading-day (~1 calendar quarter) mean of MNQ's own
daily True Range (session high-low, gapped against prior session close), SHIFTED
by 1 day so each day's regime value uses only the 63 session days strictly BEFORE
it (t-63..t-1) -- never the day itself, never anything after it. This is the same
True Range series Stage 1 characterized (stage1_true_range.pkl), just smoothed and
made strictly trailing/causal here (Stage 1's own ATR-14 in the characterization
table already includes day t via a plain non-shifted rolling window -- fine for a
DESCRIPTIVE table, but that would be look-ahead if used as a regime label, hence
the extra .shift(1) here).

Window choice (stated before looking at which window "wins"): 63 trading days is
the standard quarterly cadence for macro-driven vol regimes (Fed-meeting spacing,
earnings seasons) -- long enough to filter week-to-week chop (a 14-20d window
produces 46-64 flip/flop segments over the panel, i.e. noise, not "regime"), short
enough that the resulting classification is NOT simply a smoothed re-derivation of
the calendar split (a 126d+ window collapses to 8 segments and >=97% same-side
purity vs the 2021-09-28 cutoff -- at that point the "test" is circular). At 63d
the panel splits into 20 contiguous regime segments, giwing a genuinely independent
bucketing to test against the calendar break, not a foregone conclusion either way.

Bucketing note: per-day REGIME VALUE is strictly trailing/causal (as required).
The THRESHOLD used to bucket days into HIGH-vol vs LOW-vol (median of the trailing
series over the full sample) is a post-hoc, full-sample statistic -- exactly like
run_evalseq_orb_intraday's own mid=len(dates)//2 half-split point, which is also
chosen after seeing the whole panel. This is fine for a DESCRIPTIVE/measurement
split (what this task is) and is flagged here as NOT a live-tradeable rule as-is.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

SCRATCH = Path(__file__).resolve().parent
if str(SCRATCH) not in sys.path:
    sys.path.insert(0, str(SCRATCH))

import run_evalseq_orb_intraday as R  # noqa: E402

CUTOFF = pd.Timestamp("2021-09-28")
WINDOW = 63
K = 1


def contiguous_runs(mask: pd.Series):
    """Yield (start_pos, end_pos) [end exclusive] positional slices of `mask`'s
    index where mask is True and contiguous (adjacent ROWS of the underlying
    business-day-indexed panel -- i.e. real adjacent calendar business days,
    since the panel index itself is pd.bdate_range)."""
    vals = mask.to_numpy()
    n = len(vals)
    i = 0
    while i < n:
        if not vals[i]:
            i += 1
            continue
        j = i
        while j < n and vals[j]:
            j += 1
        yield i, j
        i = j


def build_regime_blocks(panel_full: pd.DataFrame, label: pd.Series, want: bool):
    """Concatenate blocks_from_panel(...) over every contiguous run of the panel
    where label==want, skipping runs too short to form even one Monday-anchored
    5-day block (blocks_from_panel raises ValueError on those -- caught & skipped,
    same silent boundary-day exclusion the existing harness already applies to a
    panel's own trailing partial week)."""
    label = label.reindex(panel_full.index)
    mask = (label == want)
    pnl_parts, low_parts = [], []
    n_days_used = 0
    n_runs_used = 0
    n_runs_skipped = 0
    for i0, i1 in contiguous_runs(mask):
        sub = panel_full.iloc[i0:i1]
        try:
            bp, bl = R.blocks_from_panel(sub)
        except ValueError:
            n_runs_skipped += 1
            continue
        pnl_parts.append(bp)
        low_parts.append(bl)
        n_days_used += (i1 - i0)
        n_runs_used += 1
    if not pnl_parts:
        raise ValueError(f"no usable blocks for label={want}")
    bpnl = np.concatenate(pnl_parts, axis=0)
    blow = np.concatenate(low_parts, axis=0)
    return bpnl, blow, dict(n_days_in_label=int(mask.sum()), n_days_in_blocks=n_days_used,
                             n_runs_used=n_runs_used, n_runs_skipped=n_runs_skipped,
                             n_blocks=len(bpnl))


def main():
    t0 = time.time()
    report: dict = {"window": WINDOW, "k": K, "cutoff": str(CUTOFF.date())}

    thr = R.load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}")

    recon = pd.read_pickle(SCRATCH / "stage1_recon.pkl")
    tr = pd.read_pickle(SCRATCH / "stage1_true_range.pkl")  # session-day True Range, from Stage 1
    print(f"[data ] recon n={len(recon)}  tr n={len(tr)} session days")

    R.assert_engine_ready(R.TIER)
    fkw_base = R.firm_kwargs(R.TIER, inactivity_off=True, consistency=R.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == R.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=R.LOCK_UNREACHABLE)
    else:
        fkw = dict(fkw_base)
    assert fkw["profit_target"] == R.TARGET
    assert fkw["starting_equity"] == R.START
    assert fkw["trailing_dd_pct"] == -R.DD / R.START

    # ---- build the causal regime label ----
    roll = tr.rolling(WINDOW, min_periods=WINDOW).mean().shift(1)  # trailing t-63..t-1, never day t
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    roll_full = roll.reindex(full_idx).ffill()  # NYSE-holiday gap fill only; no new info added
    valid = roll_full.notna()
    median_thr = float(roll_full[valid].median())
    label = pd.Series(np.where(roll_full > median_thr, "HIGH", np.where(valid, "LOW", "WARMUP")),
                       index=full_idx)
    n_high, n_low, n_warmup = (label == "HIGH").sum(), (label == "LOW").sum(), (label == "WARMUP").sum()
    print(f"\n[regime] window={WINDOW}d trailing mean True Range, median threshold={median_thr:.2f}pt")
    print(f"[regime] n_days: HIGH={n_high}  LOW={n_low}  WARMUP(insufficient trailing history)={n_warmup}  "
          f"total={len(full_idx)}")
    report["median_threshold_pt"] = median_thr
    report["n_days"] = dict(HIGH=int(n_high), LOW=int(n_low), WARMUP=int(n_warmup))

    # ---- date-correlation check: does the vol regime track the calendar split? ----
    idx_high = full_idx[label == "HIGH"]
    idx_low = full_idx[label == "LOW"]
    frac_high_post = float((idx_high >= CUTOFF).mean())
    frac_low_post = float((idx_low >= CUTOFF).mean())
    frac_post_that_is_high = float((label.loc[full_idx >= CUTOFF] == "HIGH").mean())
    frac_pre_that_is_high = float((label.loc[full_idx < CUTOFF] == "HIGH").mean())
    print(f"\n[date-corr] frac of HIGH-regime days that fall on/after {CUTOFF.date()}: {frac_high_post:.1%}")
    print(f"[date-corr] frac of LOW-regime  days that fall on/after {CUTOFF.date()}: {frac_low_post:.1%}")
    print(f"[date-corr] frac of post-{CUTOFF.date()} days labeled HIGH: {frac_post_that_is_high:.1%}")
    print(f"[date-corr] frac of pre-{CUTOFF.date()}  days labeled HIGH: {frac_pre_that_is_high:.1%}")
    report["date_correlation"] = dict(
        frac_high_days_post_cutoff=frac_high_post, frac_low_days_post_cutoff=frac_low_post,
        frac_post_cutoff_days_that_are_high=frac_post_that_is_high,
        frac_pre_cutoff_days_that_are_high=frac_pre_that_is_high,
    )

    # segment structure
    n_seg_high = sum(1 for _ in contiguous_runs(label.reindex(full_idx) == "HIGH"))
    n_seg_low = sum(1 for _ in contiguous_runs(label.reindex(full_idx) == "LOW"))
    print(f"[segments] HIGH: {n_seg_high} contiguous runs   LOW: {n_seg_low} contiguous runs")
    report["n_segments"] = dict(HIGH=n_seg_high, LOW=n_seg_low)

    # ---- build k=1 panel, then regime-bucketed blocks (reused blocks_from_panel per run) ----
    panel_full = R.build_k_panel(recon, K)

    gate_report = {}
    for regime_name in ("HIGH", "LOW"):
        bpnl, blow, meta = build_regime_blocks(panel_full, label, regime_name)
        print(f"\n--- regime={regime_name}  n_blocks={meta['n_blocks']}  "
              f"days_in_label={meta['n_days_in_label']}  days_used_in_blocks={meta['n_days_in_blocks']}  "
              f"runs_used={meta['n_runs_used']}  runs_skipped(too short)={meta['n_runs_skipped']} ---")

        flat = R.run_policy_orb(bpnl, blow, R.pol_const(1.0), use_intraday=True,
                                 horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        cush = R.run_policy_orb(bpnl, blow, R.pol_cushion, use_intraday=True,
                                 horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)

        def gate(bust_pct, pass_pct):
            return (bust_pct <= thr.eval_bust_ceiling * 100.0) and (pass_pct >= thr.pass_floor * 100.0)

        flat_pass = gate(flat["bust_pct"], flat["pass_pct"])
        cush_pass = gate(cush["bust_pct"], cush["pass_pct"])
        print(f"  flat(k=1)    : bust={flat['bust_pct']:.2f}%  pass={flat['pass_pct']:.2f}%  "
              f"gate={'PASS' if flat_pass else 'FAIL'}")
        print(f"  cushion(k=1) : bust={cush['bust_pct']:.2f}%  pass={cush['pass_pct']:.2f}%  "
              f"gate={'PASS' if cush_pass else 'FAIL'}   (elapsed {time.time()-t0:.0f}s)")

        gate_report[regime_name] = dict(
            meta=meta,
            flat=dict(bust_pct=flat["bust_pct"], pass_pct=flat["pass_pct"], gate_pass=flat_pass),
            cushion=dict(bust_pct=cush["bust_pct"], pass_pct=cush["pass_pct"], gate_pass=cush_pass),
        )

    report["gate"] = gate_report
    report["gate_thresholds"] = dict(eval_bust_ceiling_pct=thr.eval_bust_ceiling * 100.0,
                                      pass_floor_pct=thr.pass_floor * 100.0)

    out = SCRATCH / "stage2_regime_gate_results.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
