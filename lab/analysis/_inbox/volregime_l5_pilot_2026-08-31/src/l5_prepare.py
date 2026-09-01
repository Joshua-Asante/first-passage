"""L5 data preparation for Q-VOLREGIME-1 Packet C.

Extends `byyear_l4.py::prepare()`'s exact conventions (hash verification, ET
conversion, trading-day assignment, MYM truncation, tod_threshold, bias_volume,
bias_range, outcome) but retains the continuous values L4 discards -- L5 needs
continuous volume/range and the threshold series themselves to build the
DESIGN.md S4.2 regression and the S4.4 causal reconstruction, not just the
final binary flags.

Every numeric convention below is copied verbatim from byyear_l4.py, not
re-derived, to guarantee L5's own "real" bias_volume/bias_range/outcome match
L1-L4's exactly.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
DATA = REPO / "core" / "data" / "bar_data"
EXPECTED = {
    "MNQ": "6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a",
    "MYM": "24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58",
}
WINDOW = {"MNQ": 60, "MYM": 20}
RTH_START_MIN = 9 * 60 + 30  # 09:30 ET
RTH_END_MIN = 16 * 60  # 16:00 ET


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tod_threshold_vectorized(values: np.ndarray, slots: np.ndarray, window: int) -> np.ndarray:
    """Trailing same-slot median (strict prior), vectorized per slot.

    Numerically identical to byyear_l4.py::tod_threshold's own per-row Python
    loop (same window, same `med > 0` guard, same "insufficient history ->
    NaN" rule) but computed by grouping rows per slot and running a rolling
    median within each slot's own occurrence-ordered sub-series, rather than
    a single global Python for-loop. This function is called once per
    replicate during S4.4's causal reconstruction (thousands of times across
    a pilot run), so the per-row-loop reference implementation is too slow to
    reuse directly; this is the same computation, faster.
    """
    n = len(values)
    out = np.full(n, np.nan)
    order = np.argsort(slots, kind="stable")
    slots_sorted = slots[order]
    values_sorted = values[order]
    # boundaries of each contiguous same-slot run in slot-sorted order
    boundaries = np.flatnonzero(np.diff(slots_sorted)) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [n]))
    out_sorted = np.full(n, np.nan)
    for start, end in zip(starts, ends):
        seg = values_sorted[start:end]
        seg_len = end - start
        if seg_len <= window:
            continue
        med = _trailing_median(seg, window)
        out_sorted[start:end] = med
    out[order] = out_sorted
    return out


def _trailing_median(seg: np.ndarray, window: int) -> np.ndarray:
    """For seg[i], the median of seg[i-window:i] if i >= window else NaN,
    with the byyear_l4.py `med > 0` guard applied."""
    n = len(seg)
    result = np.full(n, np.nan)
    # pandas rolling median is the fast, correct primitive for this
    s = pd.Series(seg)
    rolling = s.rolling(window=window, min_periods=window).median()
    # rolling.iloc[i] covers seg[i-window+1 : i+1]; we need the median of
    # seg[i-window:i] (strictly prior, excludes seg[i] itself) -> shift by 1
    shifted = rolling.shift(1).to_numpy()
    valid = shifted > 0
    result[valid] = shifted[valid]
    return result


def prepare_l5(symbol: str) -> tuple[pd.DataFrame, dict]:
    """Return (frame, metadata). frame has one row per RAW bar (not just
    scored ones) plus a `scored` boolean column, so callers can build
    trailing history over the full pre-scoreable region too."""
    path = DATA / f"{symbol}_M15.csv"
    if not path.is_file():
        raise RuntimeError(f"{symbol} vendor panel absent: {path}")
    actual_hash = sha256(path)
    if actual_hash != EXPECTED[symbol]:
        raise RuntimeError(f"{symbol} hash mismatch: {actual_hash}")

    raw = pd.read_csv(path)
    raw["time"] = pd.to_datetime(raw["time"], utc=True)
    raw = raw.sort_values("time").drop_duplicates("time", keep="last").reset_index(drop=True)
    et = raw["time"].dt.tz_convert("America/New_York")
    slots = (et.dt.hour * 60 + et.dt.minute).to_numpy()
    trading_day = et.dt.normalize() + pd.to_timedelta((slots >= 18 * 60).astype(int), unit="D")

    if symbol == "MYM":  # frozen stage-1 exclusion of final truncated session
        keep = trading_day < trading_day.max()
        raw = raw.loc[keep].reset_index(drop=True)
        slots = slots[keep.to_numpy()]
        trading_day = trading_day.loc[keep].reset_index(drop=True)
        et = et.loc[keep].reset_index(drop=True)

    window = WINDOW[symbol]
    volume = raw["volume"].to_numpy(float)
    bar_range = (raw["high"] - raw["low"]).to_numpy(float)
    volume_threshold = tod_threshold_vectorized(volume, slots, window)
    range_threshold = tod_threshold_vectorized(bar_range, slots, window)

    volume_cmp = np.greater_equal if symbol == "MNQ" else np.greater
    bias_volume = np.where(
        np.isnan(volume_threshold), np.nan, volume_cmp(volume, volume_threshold).astype(float)
    )
    bias_range = np.where(
        np.isnan(range_threshold), np.nan, np.greater(bar_range, range_threshold).astype(float)
    )
    outcome = np.full(len(raw), np.nan)
    outcome[:-1] = np.where(
        ~np.isnan(range_threshold[1:]),
        np.greater(bar_range[1:], range_threshold[1:]).astype(float),
        np.nan,
    )

    scored = (~np.isnan(bias_volume)) & (~np.isnan(bias_range)) & (~np.isnan(outcome))

    day_of_week = et.dt.dayofweek.to_numpy()  # 0=Mon .. 6=Sun
    rth = ((slots >= RTH_START_MIN) & (slots < RTH_END_MIN)).astype(int)
    tod_angle = 2.0 * np.pi * (slots / (24.0 * 60.0))

    frame = pd.DataFrame(
        {
            "time_utc": raw["time"],
            "trading_day": trading_day,
            "slot": slots,
            "tod_sin": np.sin(tod_angle),
            "tod_cos": np.cos(tod_angle),
            "day_of_week": day_of_week,
            "rth": rth,
            "volume": volume,
            "bar_range": bar_range,
            "volume_threshold": volume_threshold,
            "range_threshold": range_threshold,
            "bias_volume": bias_volume,
            "bias_range": bias_range,
            "outcome": outcome,
            "scored": scored,
        }
    )
    # S3.3's four lagged binary range indicators -- bar-index lags (strictly
    # causal: lag_i at row t is bias_range at row t-i, computed only from
    # already-observed bars). A lag that reaches before row 0 is NaN, which
    # `scored` does not currently account for -- folded in below.
    for lag in (1, 2, 3, 4):
        frame[f"range_lag_{lag}"] = frame["bias_range"].shift(lag)
    lag_ok = frame[[f"range_lag_{lag}" for lag in (1, 2, 3, 4)]].notna().all(axis=1)
    frame["scored"] = frame["scored"] & lag_ok

    # Day-level True Range for S4.3 step 1 / S3.1 baseline_2's own P80
    # conditioning flag: the classic Wilder's True Range on daily OHLC (gap-
    # aware -- max of high-low, |high-prev_close|, |low-prev_close|), NOT
    # max(bar_range) across a day's own M15 bars, which drops the overnight
    # gap term entirely and is a different, smaller-magnitude statistic than
    # the `daily-range-state-persistence` construct this reuses (Codex PR
    # #243 review). daily_high/daily_low use ALL bars (RTH+overnight, per
    # that construct's own `daily_ohlc()` convention); daily_close is the
    # session's own last bar close -- pulled from `raw` (`frame` only carries
    # the derived `bar_range`, not high/low/close), which shares `frame`'s
    # exact row order/count (both built from the same, possibly MYM-
    # truncated, `raw`). No roll-day exclusion is performed here, matching
    # this exact panel's own sibling convention
    # (mnq_dailygeom_notice_2026-08-29/data_lib.py: "TV continuous front-
    # month '1!' splice ... no per-bar roll marker to key it on") -- real
    # data only, never permuted.
    daily_high = raw.groupby(trading_day)["high"].max().sort_index()
    daily_low = raw.groupby(trading_day)["low"].min().sort_index()
    daily_close = raw.groupby(trading_day)["close"].last().sort_index()
    prev_close = daily_close.shift(1)
    day_true_range = np.maximum.reduce(
        [
            (daily_high - daily_low).to_numpy(),
            (daily_high - prev_close).abs().to_numpy(),
            (daily_low - prev_close).abs().to_numpy(),
        ]
    )
    day_true_range = pd.Series(day_true_range, index=daily_high.index, name="day_true_range")
    day_true_range.iloc[0] = np.nan  # no prior close

    metadata = {
        "csv": path.relative_to(REPO).as_posix(),
        "sha256": actual_hash,
        "window_same_slot_prior_observations": window,
        "n_scored": int(frame["scored"].sum()),
        "span_utc": [str(raw["time"].min()), str(raw["time"].max())],
        "day_true_range": day_true_range,
    }
    return frame, metadata


if __name__ == "__main__":
    import time

    for symbol in ("MNQ", "MYM"):
        t0 = time.time()
        frame, meta = prepare_l5(symbol)
        dt = time.time() - t0
        print(f"{symbol}: n_scored={meta['n_scored']} prepare_time={dt:.2f}s")
        scored_frame = frame.loc[frame["scored"]]
        print(
            f"  bias_volume mean={scored_frame['bias_volume'].mean():.4f} "
            f"bias_range mean={scored_frame['bias_range'].mean():.4f} "
            f"outcome mean={scored_frame['outcome'].mean():.4f}"
        )
