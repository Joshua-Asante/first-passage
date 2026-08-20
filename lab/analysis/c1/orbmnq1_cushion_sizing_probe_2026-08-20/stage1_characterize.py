#!/usr/bin/env python3
"""Stage 1: characterize what changes in ORB-MNQ-1 / MNQ price action around the
2021-09-28 regime break found by the prior (independent) verifier.

Reuses (does not re-derive) resolve_panel/make_inst/orb_days_with_excursion and the
underlying orb_lib session_panel/orb_backtest from
run_evalseq_orb_intraday.py (already-verified harness, same session). Pure read +
compute on the already-cached MNQ.v.0 panel. $0/K=0. Writes only to scratch.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SCRATCH = Path(__file__).resolve().parent
if str(SCRATCH) not in sys.path:
    sys.path.insert(0, str(SCRATCH))

import run_evalseq_orb_intraday as R  # noqa: E402

CUTOFF = pd.Timestamp("2021-09-28")


def main():
    inst = R.make_inst()
    panel_pkl = R.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data] {panel_pkl}  rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    piv, meta = R.ol.session_panel(df, inst)
    bt = R.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = R.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    R.assert_mirror_matches_engine(recon, bt)
    print(f"[ctrl] recon mirrors orb_lib.orb_backtest bit-for-bit, n={len(recon)}")

    # ---- (a) realized vol of MNQ itself: session high-low range + 14d True Range/ATR,
    # over ALL session days (not just ORB-triggering days) ----
    h, l, c = piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    sess_high = h[tods].max(axis=1, skipna=True)
    sess_low = l[tods].min(axis=1, skipna=True)
    sess_range = (sess_high - sess_low).dropna()
    sess_range.index = pd.to_datetime(sess_range.index)

    prev_close = meta["rth_close"].shift(1)
    rth_close = meta["rth_close"]
    tr = pd.concat([
        (sess_high - sess_low),
        (sess_high - prev_close).abs(),
        (sess_low - prev_close).abs(),
    ], axis=1).max(axis=1).dropna()
    tr.index = pd.to_datetime(tr.index)
    atr14 = tr.rolling(14, min_periods=14).mean()

    # ---- (b) ORB's own opening-range size, over ALL session days (or_hi-or_lo,
    # independent of whether a breakout later triggered) ----
    or_tods = tods[:2]
    or_hi_all = h[or_tods].max(axis=1, skipna=True)
    or_lo_all = l[or_tods].min(axis=1, skipna=True)
    or_rng_all = (or_hi_all - or_lo_all).dropna()
    or_rng_all = or_rng_all[or_rng_all > 0]
    or_rng_all.index = pd.to_datetime(or_rng_all.index)

    all_days = pd.to_datetime(pd.Index(c.index))

    def split(s: pd.Series):
        pre = s[s.index < CUTOFF]
        post = s[s.index >= CUTOFF]
        return pre, post

    def summ(s: pd.Series):
        return dict(n=int(len(s)), mean=float(s.mean()), median=float(s.median()),
                    std=float(s.std()))

    report = {"cutoff": str(CUTOFF.date())}

    sr_pre, sr_post = split(sess_range)
    report["session_hl_range_pt"] = dict(pre=summ(sr_pre), post=summ(sr_post))

    tr_pre, tr_post = split(atr14.dropna())
    report["atr14_pt"] = dict(pre=summ(tr_pre), post=summ(tr_post))

    orall_pre, orall_post = split(or_rng_all)
    report["or_size_all_session_days_pt"] = dict(pre=summ(orall_pre), post=summ(orall_post))

    recon_idx = recon.set_index("date")
    or_trig_pre = recon_idx.loc[recon_idx.index < CUTOFF, "range_pt"]
    or_trig_post = recon_idx.loc[recon_idx.index >= CUTOFF, "range_pt"]
    report["or_size_trigger_days_pt"] = dict(pre=summ(or_trig_pre), post=summ(or_trig_post))

    days_pre = all_days[all_days < CUTOFF]
    days_post = all_days[all_days >= CUTOFF]
    n_trig_pre = int((recon["date"] < CUTOFF).sum())
    n_trig_post = int((recon["date"] >= CUTOFF).sum())
    report["trigger_frequency"] = dict(
        pre=dict(n_session_days=int(len(days_pre)), n_triggers=n_trig_pre,
                  freq=n_trig_pre / len(days_pre) if len(days_pre) else float("nan")),
        post=dict(n_session_days=int(len(days_post)), n_triggers=n_trig_post,
                   freq=n_trig_post / len(days_post) if len(days_post) else float("nan")),
    )

    R_pre = recon.loc[recon["date"] < CUTOFF, "R"]
    R_post = recon.loc[recon["date"] >= CUTOFF, "R"]
    report["win_rate"] = dict(pre=float((R_pre > 0).mean()), post=float((R_post > 0).mean()))
    report["mean_R"] = dict(pre=float(R_pre.mean()), post=float(R_post.mean()))
    report["stopped_frac"] = dict(
        pre=float(recon.loc[recon["date"] < CUTOFF, "stopped"].mean()),
        post=float(recon.loc[recon["date"] >= CUTOFF, "stopped"].mean()),
    )
    long_frac_pre = float((recon.loc[recon["date"] < CUTOFF, "side"] == "long").mean())
    long_frac_post = float((recon.loc[recon["date"] >= CUTOFF, "side"] == "long").mean())
    report["long_side_frac"] = dict(pre=long_frac_pre, post=long_frac_post)

    print("\n" + "=" * 100)
    print(f"STAGE 1 -- pre/post {CUTOFF.date()} characterization")
    print("=" * 100)

    def pct_chg(pre, post):
        return (post - pre) / pre * 100.0 if pre else float("nan")

    rows = [
        ("session H-L range (pt), all days", sr_pre.mean(), sr_post.mean()),
        ("ATR-14 (pt), all days", tr_pre.mean(), tr_post.mean()),
        ("OR size (pt), all session days", orall_pre.mean(), orall_post.mean()),
        ("OR size (pt), ORB-trigger days only", or_trig_pre.mean(), or_trig_post.mean()),
        ("trigger freq (trades/session)", n_trig_pre / len(days_pre), n_trig_post / len(days_post)),
        ("win rate", float((R_pre > 0).mean()), float((R_post > 0).mean())),
        ("mean R", float(R_pre.mean()), float(R_post.mean())),
        ("stopped frac", float(recon.loc[recon['date'] < CUTOFF, 'stopped'].mean()),
         float(recon.loc[recon['date'] >= CUTOFF, 'stopped'].mean())),
        ("long-side frac", long_frac_pre, long_frac_post),
    ]
    for name, pre_v, post_v in rows:
        print(f"  {name:38s}  pre={pre_v:10.4f}  post={post_v:10.4f}  chg={pct_chg(pre_v, post_v):+7.1f}%")

    out = SCRATCH / "stage1_characterization.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")

    # also persist the raw daily series for Stage 2 reuse (no recompute of panel loading)
    sess_range.to_pickle(SCRATCH / "stage1_sess_range.pkl")
    tr.to_pickle(SCRATCH / "stage1_true_range.pkl")
    recon.to_pickle(SCRATCH / "stage1_recon.pkl")
    print(f"[write] stage1_sess_range.pkl / stage1_true_range.pkl / stage1_recon.pkl (Stage 2 reuse)")


if __name__ == "__main__":
    main()
