"""D-S-A pre-Q gate, MYM candidates 2 (overnight-range) and 4 (gap-magnitude) run
JOINTLY -- Simplify step: does gap magnitude add lift beyond overnight range's own
conditioning, and vice versa?

Direct port of the MNQ sibling campaign's `candidate24_joint_gate.py`
(lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate24_joint_gate.py) --
same design, same seeds, same output shape -- so the two runs are directly
comparable rather than superficially similar. On MNQ this script found gap
magnitude is a nested, sign-unstable sub-question of overnight range (positive
lift only when overnight range is itself calm; near-zero/negative when overnight
range is already hot) and that finding is what let MNQ's Q-RANGEXFER-1 combine
both predictors under one id instead of two. MYM's own two predictors
(overnight-range-day-session-transfer, overnight-gap-magnitude-range-conditioning)
have never been tested against each other this way -- this script is that test,
not a re-run of anything already scored under either MYM id.

Design (the D-S-A gate's Simplify action -- lowest-dimension representation that
preserves the anomaly under test): swap the conditioning variable from day-history
to EACH candidate's own bias, and test the other candidate's incremental lift
within strata of it. Symmetric by construction -- neither candidate is privileged
as the "base" case a priori (that would be a forbidden D-test: assuming which one
is real before looking).

Reuses MYM's own load_sessions.py / iaaft_battery.py helpers and the exact
bias/bias_dayhist/y definitions already verified correct in
c2_c4_stratified_rerun.py -- this script only adds the joint (2-predictor)
cross-tabulation on top of those same per-session series.

Run from lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/ (same directory as
c2_c4_stratified_rerun.py, so the load_sessions/iaaft_battery imports resolve).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from load_sessions import load_bars, session_ohlc, rth_ohlc, overnight_ohlc, PANEL
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
CACHED_FRAME = HERE / "c24_joint_frame.csv"
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50


def load_cached_frame():
    """Reload the committed per-day frame so a follow-up (null-calibrated p,
    stage-2 design) does not need vendor bars. Same columns `build_joint_frame`
    writes. Returns None if the cache is absent. Ported verbatim from the MNQ
    sibling script's own `load_cached_frame` (Codex review, PR #207/#210)."""
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


def build_joint_frame():
    """Unchanged from c2_c4_stratified_rerun.py's build_frame() -- same data,
    same series, same session filter."""
    bars = load_bars()
    full = session_ohlc(bars)
    full = full[full["n_bars"] >= 20]
    rth = rth_ohlc(bars)
    on = overnight_ohlc(bars)
    idx = full.index
    rth = rth.reindex(idx)
    on = on.reindex(idx)

    rth_range = (rth["high"] - rth["low"]).to_numpy()
    on_range = (on["high"] - on["low"]).to_numpy()
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    gap = np.full(len(idx), np.nan)
    gap[1:] = rth_open[1:] - rth_close[:-1]
    abs_gap = np.abs(gap)

    n = len(idx)

    bias_on = (on_range >= B.rolling_pctl_strict_prior(on_range, WINDOW, Q_BIAS)).astype(float)
    bias_on[np.isnan(B.rolling_pctl_strict_prior(on_range, WINDOW, Q_BIAS))] = np.nan

    bias_gap = (abs_gap >= B.rolling_pctl_strict_prior(abs_gap, WINDOW, Q_BIAS)).astype(float)
    bias_gap[np.isnan(B.rolling_pctl_strict_prior(abs_gap, WINDOW, Q_BIAS))] = np.nan
    bias_gap[np.isnan(abs_gap)] = np.nan

    bias_dayhist_raw = (rth_range >= B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_BIAS)).astype(float)
    bias_dayhist_raw[np.isnan(B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_BIAS))] = np.nan
    bias_dayhist = np.full(n, np.nan)
    bias_dayhist[1:] = bias_dayhist_raw[:-1]  # yesterday's state, aligned to today's row

    ref = B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_REF)
    y = (rth_range > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    scored = (~np.isnan(bias_on)) & (~np.isnan(bias_gap)) & (~np.isnan(bias_dayhist)) & (~np.isnan(y))
    frame = dict(
        trading_day=[str(d) for d in np.asarray(idx)[scored]],
        bias_overnight=bias_on[scored].astype(int),
        bias_gap=bias_gap[scored].astype(int),
        bias_dayhist=bias_dayhist[scored].astype(int),
        y=y[scored].astype(int),
        on_range=on_range[scored], gap=abs_gap[scored], rth_range=rth_range[scored],
    )
    return frame


def rate(y, mask):
    return (float(y[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)


def block_bootstrap_p(y, mask_a, mask_b, block=20, draws=4000, seed=44):
    """Percentile-bootstrap tail probability that rate(mask_a) - rate(mask_b) <= 0,
    resampling contiguous day-blocks WITH REPLACEMENT jointly across y/mask_a/mask_b
    to preserve pairing. Same scheme, same default block/draws as MNQ's sibling
    script.

    NOT a null-calibrated p-value (flagged on review, PR #205): this resamples the
    OBSERVED data, so the bootstrap distribution stays centered on the observed
    lift. `p_le0` measures "how much of this bootstrap distribution's mass sits at
    or below 0" -- a percentile-CI-style tail probability -- not "how often would a
    lift this large arise under a true zero-lift null" (the Type-I-controlled
    quantity a hypothesis test needs). Kept for continuity with the rest of this
    2026-08-29 batch's scripts (c2_c4_stratified_rerun.py, c3_stratified_rerun.py,
    and MNQ's own candidate2/candidate24 scripts all use this exact convention) and
    because it is still an honest, useful CI-style summary -- but report
    `circular_shift_null_p` below as the significance figure, not this one."""
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


_MAX_ENUMERATE_N = 2500


def _stratum_circular_lifts(y_s, other_s):
    n = len(other_s)
    lifts = np.full(n, np.nan)
    for k in range(n):
        rolled = np.roll(other_s, k)
        hi = rolled == 1
        n_hi = int(hi.sum())
        if 0 < n_hi < n:
            lifts[k] = float(y_s[hi].mean() - y_s[~hi].mean())
    return lifts


def circular_shift_null_p(y, fixed_mask, other_label, draws=4000, seed=44):
    """Null-calibrated one-sided p-value under a *within-stratum* circular-shift
    null: does `other_label` carry information about y within `fixed_mask`,
    beyond what a decorrelated version of the same two series would produce by
    chance?

    Corrected 2026-08-30 (Codex review, PR #210) to match the MNQ sibling
    script's own Codex-reviewed (PR #207) construction, which this function
    previously diverged from in two ways that made the two instruments'
    null-calibrated p-values not directly comparable:

    1. Rotate `other_label` ONLY inside `fixed_mask` (`o_s = other_label[fixed]`,
       then roll `o_s`), not the full series before masking. Rotating the full
       series first and masking afterward can import label values from OUTSIDE
       the fixed stratum into the rotated in-stratum groups -- exactly the
       cross-stratum leakage the "within-stratum" name is supposed to rule out.
    2. Enumerate every distinct rotation k in {0, ..., n-1} -- INCLUDING the
       identity rotation (k=0) -- when n is small enough to do so exhaustively,
       rather than drawing `draws` random shifts from {1, ..., N-1} (which both
       excludes identity and re-uses uniform sampling where exhaustive
       enumeration is cheap and exact).

    This is the test `block_bootstrap_p` above is NOT: that one resamples the
    observed data and is centered on the observed effect (a CI-style tail
    probability); this one resamples under an explicit zero-association null.
    """
    fixed = np.asarray(fixed_mask, dtype=bool)
    other = np.asarray(other_label)
    y_s = np.asarray(y)[fixed]
    o_s = other[fixed]
    n = len(o_s)
    hi0 = o_s == 1
    lo0 = o_s == 0
    if n < 2 or not (hi0.any() and lo0.any()):
        return np.array([]), float("nan"), float("nan")
    observed = float(y_s[hi0].mean() - y_s[lo0].mean())

    if n <= _MAX_ENUMERATE_N:
        lifts = _stratum_circular_lifts(y_s, o_s)
        valid = lifts[np.isfinite(lifts)]
        if valid.size == 0:
            return np.array([]), float("nan"), observed
        p_ge_obs = float((valid >= observed).sum()) / float(valid.size)
        return valid, p_ge_obs, observed

    rng = np.random.default_rng(seed)
    draws_out = []
    for _ in range(draws):
        rolled = np.roll(o_s, int(rng.integers(0, n)))
        hi = rolled == 1
        lo = rolled == 0
        if hi.any() and lo.any():
            draws_out.append(float(y_s[hi].mean() - y_s[lo].mean()))
    draws_out = np.asarray(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def main():
    from_bars = PANEL.exists()
    if from_bars:
        f = build_joint_frame()
        print(f"built frame from {PANEL.name} (vendor bars present)")
    else:
        f = load_cached_frame()
        if f is None:
            raise FileNotFoundError(
                f"neither {PANEL} nor {CACHED_FRAME} present; cannot run joint gate"
            )
        print(f"vendor bars absent ({PANEL}); loaded {CACHED_FRAME.name}")
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
    gap_null_p = {}
    for s in (0, 1):
        m = bo == s
        hi, lo = rate(y, m & (bg == 1)), rate(y, m & (bg == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        gap_lifts[s] = lift
        print(f"overnight-stratum={s}: P(y=1|gap=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|gap=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bg == 1), m & (bg == 0), seed=100 + s)
            print(f"  bootstrap p(lift<=0) [NOT null-calibrated -- see docstring] = {p:.5f}")
            _, p_null, obs = circular_shift_null_p(y, m, bg, seed=300 + s)
            gap_null_p[s] = p_null
            print(f"  circular-shift null p(null_lift>=observed) [null-calibrated]  = {p_null:.5f}")

    print("\n--- Does OVERNIGHT add lift within GAP strata? ---")
    on_lifts = {}
    on_null_p = {}
    for s in (0, 1):
        m = bg == s
        hi, lo = rate(y, m & (bo == 1)), rate(y, m & (bo == 0))
        lift = hi[0] - lo[0] if (hi[1] and lo[1]) else None
        on_lifts[s] = lift
        print(f"gap-stratum={s}: P(y=1|overnight=1)={hi[0]:.4f}(n={hi[1]})  P(y=1|overnight=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if hi[1] and lo[1]:
            _, p = block_bootstrap_p(y, m & (bo == 1), m & (bo == 0), seed=200 + s)
            print(f"  bootstrap p(lift<=0) [NOT null-calibrated -- see docstring] = {p:.5f}")
            _, p_null, obs = circular_shift_null_p(y, m, bo, seed=400 + s)
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

    # Robustness: does gap survive with day-history ALSO held fixed (three-way)?
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
               gap_lift_null_calibrated_p=gap_null_p,
               overnight_lift_null_calibrated_p=on_null_p,
               null_construction="within_stratum_circular_shift",
               null_includes_identity=True,
               frame_source=("vendor bars " + PANEL.name) if from_bars else CACHED_FRAME.name)
    (HERE / "c24_joint_results.json").write_text(json.dumps(out, indent=1, default=str))

    # Accelerate: cache the merged per-day frame so a future stage-2 design
    # (joint-surrogation null) doesn't need to re-derive sessions from raw bars.
    # Refresh the committed cache only when we rebuilt from vendor bars; when
    # bars are absent, keep the cache byte-identical (matches the MNQ sibling
    # script's own convention).
    if from_bars:
        with open(CACHED_FRAME, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["trading_day", "bias_overnight", "bias_gap", "bias_dayhist", "y", "on_range", "gap", "rth_range"])
            for i in range(n):
                w.writerow([f["trading_day"][i], bo[i], bg[i], bd[i], y[i], f["on_range"][i], f["gap"][i], f["rth_range"][i]])
        print(f"\nwrote c24_joint_results.json + refreshed {CACHED_FRAME.name} (n={n} rows)")
    else:
        print(f"\nwrote c24_joint_results.json (n={n}; frame cache left untouched)")


if __name__ == "__main__":
    main()
