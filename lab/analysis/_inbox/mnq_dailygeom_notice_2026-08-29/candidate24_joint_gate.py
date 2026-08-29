"""D-S-A pre-Q gate, candidates 2 (overnight-range) and 4 (gap-magnitude) run
JOINTLY -- Simplify step: does gap magnitude add lift beyond overnight range's
own conditioning, and vice versa?

Both candidates independently cleared the frozen corrected-null-battery spec's
D5 stage-1 $0 falsifier against matched DAY-HISTORY conditioning (bias' =
yesterday's own RTH range). Candidate 4's own §3-C flagged the open question
this script answers: are the two candidates redundant (gap is a noisier proxy
for the same overnight-vol-regime information overnight range already
supplies) or independently informative?

Design (the D-S-A gate's Simplify action -- lowest-dimension representation
that preserves the anomaly under test): swap the conditioning variable from
day-history to EACH candidate's own bias, and test the other candidate's
incremental lift within strata of it. Symmetric by construction -- neither
candidate is privileged as the "base" case a priori (that would be a forbidden
D-test: assuming which one is real before looking).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw, rth_ohlc, overnight_ohlc, range_series  # noqa: E402
from candidate2_overnight_rth_transfer import rolling_pct_strict_prior, rolling_pct_through_yesterday, WINDOW, Q_BIAS  # noqa: E402


def build_joint_frame():
    df = load_raw()
    rth = rth_ohlc(df)
    on = overnight_ohlc(df)
    common = rth.index.intersection(on.index)
    rth = rth.loc[common].sort_index()
    on = on.loc[common].sort_index()
    n = len(common)

    rth_range = range_series(rth).to_numpy()
    on_range = range_series(on).to_numpy()
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    gap = np.full(n, np.nan)
    gap[1:] = np.abs(rth_open[1:] - rth_close[:-1])

    bias_on = (on_range >= rolling_pct_strict_prior(on_range, WINDOW, Q_BIAS)).astype(float)
    bias_on[np.isnan(rolling_pct_strict_prior(on_range, WINDOW, Q_BIAS))] = np.nan

    bias_gap = (gap >= rolling_pct_strict_prior(gap, WINDOW, Q_BIAS)).astype(float)
    bias_gap[np.isnan(rolling_pct_strict_prior(gap, WINDOW, Q_BIAS))] = np.nan
    bias_gap[np.isnan(gap)] = np.nan

    bias_dayhist_raw = (rth_range >= rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS)).astype(float)
    bias_dayhist_raw[np.isnan(rolling_pct_strict_prior(rth_range, WINDOW, Q_BIAS))] = np.nan
    bias_dayhist = np.full(n, np.nan)
    bias_dayhist[1:] = bias_dayhist_raw[:-1]

    ref = rolling_pct_through_yesterday(rth_range, WINDOW, 0.50)
    y = (rth_range > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    scored = (~np.isnan(bias_on)) & (~np.isnan(bias_gap)) & (~np.isnan(bias_dayhist)) & (~np.isnan(y))
    frame = dict(
        trading_day=[str(d.date()) for d in common[scored]],
        bias_overnight=bias_on[scored].astype(int),
        bias_gap=bias_gap[scored].astype(int),
        bias_dayhist=bias_dayhist[scored].astype(int),
        y=y[scored].astype(int),
        on_range=on_range[scored], gap=gap[scored], rth_range=rth_range[scored],
    )
    return frame


def rate(y, mask):
    return (float(y[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)


def block_bootstrap_p(y, mask_a, mask_b, block=20, draws=4000, seed=44):
    """One-sided bootstrap p that rate(mask_a) - rate(mask_b) <= 0, resampling
    contiguous day-blocks jointly across y/mask_a/mask_b to preserve pairing."""
    rng = np.random.default_rng(seed)
    N = len(y)
    nblocks = int(np.ceil(N / block))
    diffs = []
    for _ in range(draws):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        yy, ma, mb = y[idx], mask_a[idx], mask_b[idx]
        if ma.any() and mb.any():
            diffs.append(float(yy[ma].mean() - yy[mb].mean()))
    diffs = np.array(diffs)
    p_le0 = (1 + int((diffs <= 0).sum())) / (len(diffs) + 1)
    return diffs, p_le0


def main():
    f = build_joint_frame()
    y = f["y"]
    bo, bg, bd = f["bias_overnight"], f["bias_gap"], f["bias_dayhist"]
    n = len(y)
    print(f"joint-scored days: {n}")

    print(f"\nSpearman(overnight_range, gap): {spearmanr(f['on_range'], f['gap']).statistic:.4f}")
    print(f"Spearman(overnight_range, rth_range): {spearmanr(f['on_range'], f['rth_range']).statistic:.4f}")
    print(f"Spearman(gap, rth_range): {spearmanr(f['gap'], f['rth_range']).statistic:.4f}")
    print(f"co-occurrence: P(bias_gap=1|bias_overnight=1)={bg[bo==1].mean():.4f}  "
          f"P(bias_gap=1|bias_overnight=0)={bg[bo==0].mean():.4f}  (marginal P(bias_gap=1)={bg.mean():.4f})")

    print("\n--- Does GAP add lift within OVERNIGHT-range strata? ---")
    gap_lifts = {}
    for s in (0, 1):
        m = bo == s
        hi, lo = rate(y, m & (bg == 1)), rate(y, m & (bg == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        gap_lifts[s] = lift
        print(f"overnight-stratum={s}: P(y=1|gap=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|gap=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bg == 1), m & (bg == 0), seed=100+s)
            print(f"  bootstrap p(lift<=0) = {p:.5f}")

    print("\n--- Does OVERNIGHT add lift within GAP strata? ---")
    on_lifts = {}
    for s in (0, 1):
        m = bg == s
        hi, lo = rate(y, m & (bo == 1)), rate(y, m & (bo == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        on_lifts[s] = lift
        print(f"gap-stratum={s}: P(y=1|overnight=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|overnight=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bo == 1), m & (bo == 0), seed=200+s)
            print(f"  bootstrap p(lift<=0) = {p:.5f}")

    print("\n--- Full 2x2 cell breakdown (overnight x gap) ---")
    cells = {}
    for a in (0, 1):
        for b in (0, 1):
            m = (bo == a) & (bg == b)
            r = rate(y, m)
            cells[f"on={a},gap={b}"] = r
            print(f"on={a}, gap={b}: P(y=1)={r[0]:.4f} (n={r[1]})")

    # Robustness: does either survive with day-history ALSO held fixed (three-way)?
    print("\n--- Three-way check: does GAP add lift within (overnight, dayhist) cells? ---")
    three_way = {}
    for a in (0, 1):
        for d in (0, 1):
            m = (bo == a) & (bd == d)
            hi, lo = rate(y, m & (bg == 1)), rate(y, m & (bg == 0))
            lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
            three_way[f"on={a},dayhist={d}"] = dict(hi=hi, lo=lo, lift=lift)
            print(f"on={a}, dayhist={d}: P(y=1|gap=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|gap=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")

    out = dict(n=n, spearman_on_gap=float(spearmanr(f["on_range"], f["gap"]).statistic),
               spearman_on_rth=float(spearmanr(f["on_range"], f["rth_range"]).statistic),
               spearman_gap_rth=float(spearmanr(f["gap"], f["rth_range"]).statistic),
               gap_lifts_within_overnight_strata=gap_lifts,
               overnight_lifts_within_gap_strata=on_lifts,
               cells_2x2=cells, three_way_gap_check=three_way)
    (HERE / "candidate24_joint_results.json").write_text(json.dumps(out, indent=1, default=str))

    # Accelerate: cache the merged per-day frame so a future stage-2 design
    # (joint-surrogation null) doesn't need to re-derive sessions from raw bars.
    import csv
    with open(HERE / "candidate24_joint_frame.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["trading_day", "bias_overnight", "bias_gap", "bias_dayhist", "y", "on_range", "gap", "rth_range"])
        for i in range(n):
            w.writerow([f["trading_day"][i], bo[i], bg[i], bd[i], y[i], f["on_range"][i], f["gap"][i], f["rth_range"][i]])
    print(f"\nwrote candidate24_joint_results.json + candidate24_joint_frame.csv (n={n} rows)")


if __name__ == "__main__":
    main()
