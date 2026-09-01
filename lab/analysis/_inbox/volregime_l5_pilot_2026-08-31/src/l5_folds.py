"""DESIGN.md S3.4: setup period, 6-month test blocks, purge/embargo.

Operates on the *scored* subset of an l5_prepare frame (frame.loc[frame.scored]).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

EMBARGO_TRADING_DAYS = 4
TEST_BLOCK_MONTHS = 6
SETUP_MONTHS = 12


@dataclass
class Fold:
    train_idx: np.ndarray  # positional indices into the scored frame
    test_idx: np.ndarray
    test_start: pd.Timestamp
    test_end: pd.Timestamp  # exclusive


def _add_months(ts: pd.Timestamp, months: int) -> pd.Timestamp:
    return ts + pd.DateOffset(months=months)


def build_folds(scored: pd.DataFrame) -> tuple[list[Fold], pd.Timestamp]:
    """scored must be sorted by time_utc ascending, reset_index(drop=True).

    Returns (folds, setup_end) where setup_end is the timestamp fold 1's own
    test block begins at (S3.4's own 12-month setup period boundary).
    """
    scored = scored.reset_index(drop=True)
    t0 = scored["time_utc"].iloc[0]
    setup_end = _add_months(t0, SETUP_MONTHS)

    times = scored["time_utc"]
    trading_days = scored["trading_day"]
    max_lag_bars = 4  # S3.3's own 4 range lags -- the longest feature-side lookback in bars
    unique_days = pd.Index(pd.unique(trading_days)).sort_values()

    folds: list[Fold] = []
    block_start = setup_end
    panel_end = times.iloc[-1]
    while True:
        block_end = _add_months(block_start, TEST_BLOCK_MONTHS)
        if block_end > panel_end + pd.Timedelta(minutes=15):
            break  # partial trailing block -- dropped entirely, per S3.4
        test_mask = (times >= block_start) & (times < block_end)
        test_idx = np.flatnonzero(test_mask.to_numpy())
        if test_idx.size == 0:
            block_start = block_end
            continue

        train_mask = times < block_start
        train_idx_all = np.flatnonzero(train_mask.to_numpy())

        # feature-side purge: drop training rows whose trailing window (range
        # lags, up to 4 bars back) overlaps the test block -- i.e. any
        # training row within max_lag_bars bars of the test block start.
        # Since train_idx_all is exactly "everything before block_start" and
        # test starts at block_start, the trailing-window-of-length-4 rows
        # immediately preceding block_start are the ones whose OWN feature
        # window (their own 4-bar lookback) could reach into a *previous*
        # fold's test block, not this one -- the feature-side purge here is
        # about not computing a training row's features FROM this test
        # block's bars, which cannot happen for any row with time < block_start
        # in a strictly-causal lag construction. No additional drop needed
        # beyond the label-side purge below (S3.4's own information-interval
        # note (b): a trailing predictor does not itself require purging
        # merely for being near the boundary).

        # label-side purge: the row whose label (next bar) falls at/after
        # block_start -- i.e. the single training row immediately preceding
        # the test block.
        label_purge_idx = train_idx_all[-1:] if train_idx_all.size else np.array([], dtype=int)

        # embargo purge: training rows (from a *later* fold's own train set)
        # that fall on a trading day within EMBARGO_TRADING_DAYS after this
        # block's own end -- applied when CONSTRUCTING this fold's own state
        # is not needed (embargo affects the NEXT fold's training set, not
        # this one); implemented here by excluding this block's own embargo
        # days from all FUTURE folds' train sets via a running exclusion set.
        train_idx = np.setdiff1d(train_idx_all, label_purge_idx, assume_unique=False)

        folds.append(
            Fold(
                train_idx=train_idx,
                test_idx=test_idx,
                test_start=block_start,
                test_end=block_end,
            )
        )
        block_start = block_end

    # Apply embargo across folds: for fold k, drop training rows whose own
    # trading_day falls within the first EMBARGO_TRADING_DAYS trading days
    # STRICTLY AFTER any EARLIER fold's own last test trading day.
    #
    # Anchoring on the last test ROW's own trading_day (not `test_end`, a UTC
    # block boundary) matters here: `trading_day` is ET-session-anchored (the
    # 18:00 ET overnight cutover bumps late bars to the next session), while
    # `test_end` inherits the *panel's own start timestamp's* UTC time-of-day
    # component (via repeated pd.DateOffset(months=...) arithmetic) -- on
    # these panels that's 23:00 UTC, which falls inside the ET trading day
    # that starts at 18:00 ET the evening before. Normalizing that UTC
    # boundary to UTC midnight (as an earlier version of this code did) does
    # not land on the ET trading-day boundary the embargo actually needs:
    # it could admit a trading day that still contains test-block bars,
    # consuming part of the 4-day embargo on a day that isn't embargo
    # territory at all (Codex PR #243 review).
    last_test_days = [trading_days.iloc[f.test_idx[-1]] for f in folds]
    for i, f in enumerate(folds):
        embargo_exclude = np.zeros(f.train_idx.shape[0], dtype=bool)
        for last_day in last_test_days[:i]:
            post_days = unique_days[unique_days > last_day]
            embargo_window_days = set(post_days[:EMBARGO_TRADING_DAYS].tolist())
            if embargo_window_days:
                td = trading_days.iloc[f.train_idx].to_numpy()
                embargo_exclude |= np.isin(td, list(embargo_window_days))
        if embargo_exclude.any():
            f.train_idx = f.train_idx[~embargo_exclude]

    return folds, setup_end
