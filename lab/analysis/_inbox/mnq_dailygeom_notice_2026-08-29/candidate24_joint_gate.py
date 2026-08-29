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

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw, rth_ohlc, overnight_ohlc, range_series  # noqa: E402
from candidate2_overnight_rth_transfer import rolling_pct_strict_prior, rolling_pct_through_yesterday, WINDOW, Q_BIAS  # noqa: E402

CACHED_FRAME = HERE / "candidate24_joint_frame.csv"


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


def load_cached_frame():
    """Reload the committed per-day frame so a follow-up (null-calibrated p,
    stage-2 design) does not need vendor bars. Same columns `build_joint_frame`
    writes. Returns None if the cache is absent."""
    if not CACHED_FRAME.exists():
        return None
    with CACHED_FRAME.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return None

    def col(name, typ=float):
        return np.array([typ(r[name]) for r in rows])

    return dict(
        trading_day=[r["trading_day"] for r in rows],
        bias_overnight=col("bias_overnight", int),
        bias_gap=col("bias_gap", int),
        bias_dayhist=col("bias_dayhist", int),
        y=col("y", int),
        on_range=col("on_range"),
        gap=col("gap"),
        rth_range=col("rth_range"),
    )


def rate(y, mask):
    return (float(y[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)


def block_bootstrap_p(y, mask_a, mask_b, block=20, draws=4000, seed=44):
    """Percentile-bootstrap tail probability that rate(mask_a) - rate(mask_b) <= 0,
    resampling contiguous day-blocks WITH REPLACEMENT jointly across y/mask_a/mask_b
    to preserve pairing.

    NOT a null-calibrated p-value (flagged on review, PR #205 / this retrofit):
    this resamples the OBSERVED data, so the bootstrap distribution stays
    centered on the observed lift. `p_le0` measures "how much of this bootstrap
    distribution's mass sits at or below 0" -- a percentile-CI-style tail
    probability -- not "how often would a lift this large arise under a true
    zero-lift null". Kept for continuity (disclose, don't erase). Report
    `circular_shift_null_p` below as the significance figure."""
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


def circular_shift_null_p(y, fixed_mask, other_label, draws=4000, seed=44):
    """Null-calibrated one-sided p-value: does `other_label` carry information
    about y within `fixed_mask`, beyond what a decorrelated version of the same
    two series would produce by chance?

    Circularly shifts `other_label`'s FULL series (not just the `fixed_mask`
    subset) by a random offset each draw, so `other_label`'s own autocorrelation
    /persistence structure is exactly preserved (a rotation, not an i.i.d.
    reshuffle) while its pairing with (y, fixed_mask) is destroyed -- the same
    circular-shift/surrogate logic this codebase already uses for block-shuffle
    and IAAFT nulls elsewhere (see MYM `iaaft_battery.py`), applied here to a
    cross-series lift statistic instead of an autocorrelation statistic. Reports
    the fraction of null draws whose within-stratum lift is >= the observed lift
    (one-sided, Type-I-controlled under H0: no association).

    Copied from the reviewed MYM sibling
    `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c24_joint_gate.py`
    (PR #205, commit f9db9ec).
    """
    rng = np.random.default_rng(seed)
    N = len(y)
    hi0 = fixed_mask & (other_label == 1)
    lo0 = fixed_mask & (other_label == 0)
    if not (hi0.any() and lo0.any()):
        return np.array([]), float("nan"), float("nan")
    observed = float(y[hi0].mean() - y[lo0].mean())
    draws_out = []
    for _ in range(draws):
        shift = rng.integers(1, N)
        shifted = np.roll(other_label, shift)
        hi = fixed_mask & (shifted == 1)
        lo = fixed_mask & (shifted == 0)
        if hi.any() and lo.any():
            draws_out.append(float(y[hi].mean() - y[lo].mean()))
    draws_out = np.array(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def main():
    f = load_cached_frame()
    if f is not None:
        print(f"loaded {CACHED_FRAME.name} (cached per-day frame; no vendor bars)")
    else:
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
    gap_boot_p = {}
    gap_null_p = {}
    for s in (0, 1):
        m = bo == s
        hi, lo = rate(y, m & (bg == 1)), rate(y, m & (bg == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        gap_lifts[s] = lift
        print(f"overnight-stratum={s}: P(y=1|gap=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|gap=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bg == 1), m & (bg == 0), seed=100 + s)
            gap_boot_p[s] = p
            print(f"  bootstrap p(lift<=0) [NOT null-calibrated -- see docstring] = {p:.5f}")
            _, p_null, _obs = circular_shift_null_p(y, m, bg, seed=300 + s)
            gap_null_p[s] = p_null
            print(f"  circular-shift null p(null_lift>=observed) [null-calibrated]  = {p_null:.5f}")

    print("\n--- Does OVERNIGHT add lift within GAP strata? ---")
    on_lifts = {}
    on_boot_p = {}
    on_null_p = {}
    for s in (0, 1):
        m = bg == s
        hi, lo = rate(y, m & (bo == 1)), rate(y, m & (bo == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        on_lifts[s] = lift
        print(f"gap-stratum={s}: P(y=1|overnight=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|overnight=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bo == 1), m & (bo == 0), seed=200 + s)
            on_boot_p[s] = p
            print(f"  bootstrap p(lift<=0) [NOT null-calibrated -- see docstring] = {p:.5f}")
            _, p_null, _obs = circular_shift_null_p(y, m, bo, seed=400 + s)
            on_null_p[s] = p_null
            print(f"  circular-shift null p(null_lift>=observed) [null-calibrated]  = {p_null:.5f}")

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
               cells_2x2=cells, three_way_gap_check=three_way,
               gap_lift_bootstrap_p=gap_boot_p,
               overnight_lift_bootstrap_p=on_boot_p,
               gap_lift_null_calibrated_p=gap_null_p,
               overnight_lift_null_calibrated_p=on_null_p)
    (HERE / "candidate24_joint_results.json").write_text(json.dumps(out, indent=1, default=str))

    # Accelerate: cache the merged per-day frame so a future stage-2 design
    # (joint-surrogation null) doesn't need to re-derive sessions from raw bars.
    # Skip rewrite when we loaded the committed cache (byte-identity preserve).
    if not CACHED_FRAME.exists():
        with open(CACHED_FRAME, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["trading_day", "bias_overnight", "bias_gap", "bias_dayhist", "y", "on_range", "gap", "rth_range"])
            for i in range(n):
                w.writerow([f["trading_day"][i], bo[i], bg[i], bd[i], y[i], f["on_range"][i], f["gap"][i], f["rth_range"][i]])
        print(f"\nwrote candidate24_joint_results.json + {CACHED_FRAME.name} (n={n} rows)")
    else:
        print(f"\nwrote candidate24_joint_results.json (n={n}; frame cache left untouched)")


if __name__ == "__main__":
    main()
