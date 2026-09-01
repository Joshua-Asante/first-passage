"""DESIGN.md S4.2-S4.4: joint residualization, day-level circular shift, and
per-replicate causal reconstruction.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

WINDOW = {"MNQ": 60, "MYM": 20}
VOLUME_CMP = {"MNQ": "ge", "MYM": "gt"}  # byyear_l4.py's own per-instrument comparator


@dataclass
class SlotThresholdPlan:
    """Precomputed sort/grouping structure for tod_threshold, reused across
    every replicate -- only the *values* array changes per replicate, never
    the slot assignment, so the O(n log n) sort is paid once, not per call."""

    order: np.ndarray
    starts: np.ndarray
    ends: np.ndarray
    window: int


def build_threshold_plan(slots: np.ndarray, window: int) -> SlotThresholdPlan:
    order = np.argsort(slots, kind="stable")
    slots_sorted = slots[order]
    n = len(slots)
    boundaries = np.flatnonzero(np.diff(slots_sorted)) + 1
    starts = np.concatenate(([0], boundaries))
    ends = np.concatenate((boundaries, [n]))
    return SlotThresholdPlan(order=order, starts=starts, ends=ends, window=window)


def apply_threshold_plan(values: np.ndarray, plan: SlotThresholdPlan) -> np.ndarray:
    """Numerically identical to l5_prepare.tod_threshold_vectorized, but reuses
    a precomputed sort/grouping plan instead of recomputing it."""
    n = len(values)
    out_sorted = np.full(n, np.nan)
    values_sorted = values[plan.order]
    for start, end in zip(plan.starts, plan.ends):
        seg_len = end - start
        if seg_len <= plan.window:
            continue
        seg = values_sorted[start:end]
        s = pd.Series(seg)
        rolling = s.rolling(window=plan.window, min_periods=plan.window).median()
        shifted = rolling.shift(1).to_numpy()
        valid = shifted > 0
        seg_out = np.full(seg_len, np.nan)
        seg_out[valid] = shifted[valid]
        out_sorted[start:end] = seg_out
    out = np.full(n, np.nan)
    out[plan.order] = out_sorted
    return out


def fit_residual_regression(
    scored: pd.DataFrame, extra_cols: list[str] | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """DESIGN.md S4.2 (and S4.5 for Comparison 2, via extra_cols=['prior_day_regime']).

    Fits log(volume) ~ tod_sin + tod_cos + range_z + bias_range + range_lag_1..4
    + day_of_week(one-hot) + rth [+ prior_day_regime] by OLS on the *scored*
    rows only (each is a valid training-eligible bar), via closed-form least
    squares (no iterative solver needed -- exact, fast, deterministic).

    Returns (fitted_log_volume, raw_residual) aligned to `scored`'s own row
    order. range_z is the trigger bar's own continuous range, standardized by
    scored's own mean/SD (S3.3) -- for this regression fit, using the *whole
    scoreable panel's* own mean/SD is appropriate (the regression itself is a
    global-per-replicate nuisance object, per S4.2/S4.3's own note), distinct
    from baseline_1's own per-fold standardization used later in scoring.
    """
    n = len(scored)
    range_z = (scored["bar_range"] - scored["bar_range"].mean()) / scored["bar_range"].std()
    dow = pd.get_dummies(scored["day_of_week"], prefix="dow", drop_first=True).astype(float)
    cols = {
        "intercept": np.ones(n),
        "tod_sin": scored["tod_sin"].to_numpy(),
        "tod_cos": scored["tod_cos"].to_numpy(),
        "range_z": range_z.to_numpy(),
        "bias_range": scored["bias_range"].to_numpy(),
        "range_lag_1": scored["range_lag_1"].to_numpy(),
        "range_lag_2": scored["range_lag_2"].to_numpy(),
        "range_lag_3": scored["range_lag_3"].to_numpy(),
        "range_lag_4": scored["range_lag_4"].to_numpy(),
        "rth": scored["rth"].to_numpy(),
    }
    for c in dow.columns:
        cols[str(c)] = dow[c].to_numpy()
    if extra_cols:
        for c in extra_cols:
            cols[c] = scored[c].to_numpy()
    X = np.column_stack(list(cols.values())).astype(float)
    y = np.log(scored["volume"].to_numpy(float))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    residual = y - fitted
    return fitted, residual


def classify_day_regime(
    day_true_range: pd.Series, window_days: int = 60
) -> pd.Series:
    """DESIGN.md S4.3 step 1: P80 conditioning threshold, causal, computed once
    from real (never-permuted) day-level True Range, shared across every
    replicate. day_true_range must be indexed by trading_day, sorted ascending.
    Mirrors byyear_l4.tod_threshold's own guard/window discipline at the day
    granularity: trailing `window_days` prior days' own True Range, P80
    quantile, strictly causal (excludes the day itself). Comparator is
    inclusive (`>=`), matching `daily-range-state-persistence`'s own canonical
    definition (`bias_d = 1{TR_d >= P80(TR_{d-60..d-1})}`,
    lab/analysis/_inbox/rangestate_gc_2026-08/run_s1a.py:176-177) -- futures
    ranges are tick-discrete, so exact ties at the percentile are not rare,
    and strict `>` would misclassify a tied day into the low regime (Codex PR
    #243 review).
    """
    trailing = day_true_range.rolling(window=window_days, min_periods=window_days).quantile(0.80)
    threshold = trailing.shift(1)
    regime = (day_true_range >= threshold).astype("float")
    regime[threshold.isna()] = np.nan
    return regime


def build_day_groups(
    scored: pd.DataFrame, day_regime: pd.Series
) -> pd.DataFrame:
    """One row per scoreable trading day: regime bucket, slot mask (as a
    sorted tuple, hashable for grouping), and the day's own positional row
    indices into `scored` (sorted by slot).

    `row_idx` is guaranteed to be 0-based POSITIONS into `scored`'s own row
    order, regardless of what pandas index `scored` carries on entry: a
    caller that passes `frame.loc[frame["scored"]]` directly (without first
    resetting its index) would otherwise get sparse full-frame index LABELS
    here instead of positions, silently misaligning every downstream
    `raw_residual[donor_positions]`-style lookup, since fitted_log_volume/
    raw_residual are plain numpy arrays aligned to `scored`'s row order, not
    its index labels (Codex PR #243 review).
    """
    scored = scored.reset_index(drop=True)
    rows = []
    for day, day_frame in scored.groupby("trading_day", sort=True):
        regime = day_regime.get(day, np.nan)
        if pd.isna(regime):
            continue
        day_frame = day_frame.sort_values("slot")
        slot_mask = tuple(day_frame["slot"].to_numpy().tolist())
        rows.append(
            {
                "trading_day": day,
                "regime": int(regime),
                "slot_mask": slot_mask,
                "row_idx": day_frame.index.to_numpy(),
            }
        )
    return pd.DataFrame(rows)


def precompute_rotation_groups(day_groups: pd.DataFrame) -> tuple[list[list], set]:
    """Precompute the (regime, slot_mask) grouping once. `day_groups` never
    changes across replicates, so re-running pandas' own .groupby() on every
    one of B=4000 replicate draws is repeated, avoidable overhead. Returns
    (eligible_groups, excluded_days): eligible_groups is a list of day-lists,
    each with >=2 members (DESIGN.md S4.3 step 3); excluded_days is the fixed
    set of singleton-group days, both replicate-invariant."""
    eligible_groups: list[list] = []
    excluded_days: set = set()
    for (_regime, _mask), group in day_groups.groupby(["regime", "slot_mask"], sort=False):
        days = group["trading_day"].tolist()
        if len(days) < 2:
            excluded_days.update(days)
        else:
            eligible_groups.append(days)
    return eligible_groups, excluded_days


def draw_rotation(
    eligible_groups: list[list],
    excluded_days: set,
    rng: np.random.Generator,
    seen: set | None = None,
    max_attempts: int = 200,
) -> dict:
    """DESIGN.md S4.3 steps 3-5. `eligible_groups`/`excluded_days` come from
    `precompute_rotation_groups` (called once, outside the B-replicate loop).
    Within each eligible group, draws one circular shift k (identity
    included); `excluded_days` days are excluded entirely (from scoring, not
    just the rotation pool -- handled by the caller).

    DESIGN.md S4.3 step 5: "Draw ONE joint rotation assignment -- one k per
    group -- for the WHOLE PANEL, once per replicate j ... Where B=4000
    exceeds the number of distinct enumerable joint combinations for a given
    instrument's own day count, sample without replacement until exhausted,
    then resample with replacement, disclosed as such -- not silently
    padded." When `seen` is a set the caller persists across the whole
    B-replicate loop, this draws without replacement against every
    previously returned joint assignment (identified by the per-group k
    tuple) until `max_attempts` consecutive collisions, at which point the
    joint combination space is treated as exhausted and a repeat is allowed
    -- disclosed via the returned "exhausted" flag (the caller should log/
    count this, never silently ignore it). Pass seen=None for callers that
    don't need the without-replacement guarantee (e.g. a single ad hoc draw,
    this module's own identity-rotation smoke test).

    Returns {"donor_of": {...}, "excluded_days": set, "exhausted": bool}.
    """
    attempts = max_attempts if seen is not None else 1
    donor_of: dict = {}
    fingerprint: tuple = ()
    for _ in range(attempts):
        donor_of = {}
        ks = []
        for days in eligible_groups:
            n = len(days)
            k = int(rng.integers(0, n))  # identity (k=0) included
            ks.append(k)
            for i, day in enumerate(days):
                donor_of[day] = days[(i - k) % n]
        fingerprint = tuple(ks)
        if seen is None or fingerprint not in seen:
            if seen is not None:
                seen.add(fingerprint)
            return {"donor_of": donor_of, "excluded_days": excluded_days, "exhausted": False}
    # max_attempts consecutive collisions: the joint combination space is
    # exhausted (or small enough that avoiding a repeat is no longer cheap);
    # allow this repeat, disclosed via "exhausted" rather than silently
    # padding the replicate count with an undisclosed duplicate.
    seen.add(fingerprint)
    return {"donor_of": donor_of, "excluded_days": excluded_days, "exhausted": True}


def reconstruct_pseudo_volume(
    full_frame: pd.DataFrame,
    fitted_log_volume: np.ndarray,
    raw_residual: np.ndarray,
    scored_row_idx: np.ndarray,
    day_groups: pd.DataFrame,
    rotation: dict,
    plan: SlotThresholdPlan,
    symbol: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """DESIGN.md S4.4 steps 2-3. full_frame is the *entire* l5_prepare panel
    (not just scored rows); scored_row_idx are full_frame's own positional
    indices for the scored subset that fitted_log_volume/raw_residual align to.

    Returns (pseudo_volume_full, pseudo_bias_volume_scored, excluded_row_mask)
    where pseudo_volume_full is aligned to full_frame (pre-scoreable region and
    excluded-day rows = real volume, retained as trailing history so a small
    number of excluded days cannot invalidate other days' rolling-median
    thresholds; non-excluded scoreable rows = reconstructed per this
    replicate's own rotation) and pseudo_bias_volume_scored aligns to
    scored_row_idx. excluded_row_mask marks rows the caller must drop from the
    actual L5 statistic (no valid null-world reconstruction existed for them).
    """
    n_full = len(full_frame)
    pseudo_volume_full = full_frame["volume"].to_numpy(float).copy()

    # day_groups["row_idx"] holds positions WITHIN the scored subset (the
    # frame `fit_residual_regression` was fit on, in its own row order) --
    # NOT full_frame positions. fitted_log_volume/raw_residual are aligned to
    # that same scored-subset ordering, so day_groups's own row_idx values
    # index directly into them. `scored_row_idx` is only used at the very end
    # to map scored-subset positions back into full_frame positions.
    residual_by_row = np.full(len(scored_row_idx), np.nan)
    # .iterrows() builds a fresh Series per row and dominates this function's
    # cost (profiled: ~55% of wall time over day_groups' ~1500 rows, more than
    # the rolling-median threshold computation itself) since this runs once
    # per replicate, B=4000 times per outer panel. Plain-Python zip over
    # pre-extracted arrays does the same job without the per-row Series
    # construction.
    group_days = day_groups["trading_day"].to_numpy()
    group_row_idx = day_groups["row_idx"].to_numpy()
    donor_by_day = dict(zip(group_days, group_row_idx))
    donor_of = rotation["donor_of"]
    excluded_days = rotation["excluded_days"]
    # Default every scored row to excluded; only rows belonging to a day that
    # is actually visited below (i.e. present in day_groups with a valid
    # donor) get cleared. This also catches trading days that never made it
    # into day_groups at all -- classify_day_regime's own window_days warm-up
    # period leaves early days with regime=NaN, so build_day_groups skips them
    # entirely (S4.3 step 1). Those days have no regime bucket to stratify
    # into and thus no valid null-world reconstruction either, exactly like a
    # <2-day (regime, slot_mask) group -- defaulting to excluded here (rather
    # than defaulting to included and only marking the <2-day case) is what
    # catches them; the old default-included version silently fell through to
    # a NaN residual for these rows instead of excluding them.
    excluded_row_mask = np.ones(len(scored_row_idx), dtype=bool)
    self_donor_mask = np.zeros(len(scored_row_idx), dtype=bool)

    for day, own_positions in zip(group_days, group_row_idx):
        if day in excluded_days:
            continue
        donor_day = donor_of[day]
        donor_positions = donor_by_day[donor_day]
        # own_positions and donor_positions share an identical slot mask by
        # construction (S4.3 step 3), so positional (slot-sorted) alignment
        # is exact.
        residual_by_row[own_positions] = raw_residual[donor_positions]
        excluded_row_mask[own_positions] = False
        if donor_day == day:
            self_donor_mask[own_positions] = True

    pseudo_log_volume_scored = fitted_log_volume + residual_by_row
    pseudo_volume_scored = np.exp(pseudo_log_volume_scored)
    # Self-donor rows (every row under identity; any row whose drawn k happens
    # to map it to itself under a real rotation) are mathematically exactly
    # the real value -- raw_residual[i] = log(volume[i]) - fitted[i], so
    # exp(fitted[i] + raw_residual[i]) recovers volume[i] only up to the
    # exp(log(x)) round-trip's float error. Substituting the real value
    # directly removes that noise, which otherwise flips bias_volume at the
    # rare row whose real volume sits exactly on its own trailing-median
    # threshold (a genuine tie, not a reconstruction defect).
    if self_donor_mask.any():
        real_volume_scored = full_frame["volume"].to_numpy(float)[scored_row_idx]
        pseudo_volume_scored = np.where(
            self_donor_mask, real_volume_scored, pseudo_volume_scored
        )
    # excluded-group scored rows have no valid null-world reconstruction (no
    # donor), but they are excluded from *scoring* (S4.3 step 3), not deleted
    # from the panel: only the non-excluded positions get overwritten here, so
    # excluded rows retain their real volume (already present from the initial
    # copy) as trailing history for the rolling-median threshold below. Writing
    # NaN there instead would poison every OTHER (non-excluded) same-slot
    # occurrence whose own trailing window happens to span one of these rows --
    # pandas' rolling(window, min_periods=window).median() invalidates the
    # entire window when any single value inside it is NaN, so a handful of
    # excluded days can otherwise corrupt thousands of downstream thresholds
    # for bars that have nothing to do with them.
    non_excluded_scored = ~excluded_row_mask
    non_excluded_full_idx = scored_row_idx[non_excluded_scored]
    pseudo_volume_full[non_excluded_full_idx] = pseudo_volume_scored[non_excluded_scored]

    pseudo_threshold_full = apply_threshold_plan(pseudo_volume_full, plan)
    cmp = np.greater_equal if VOLUME_CMP[symbol] == "ge" else np.greater
    pseudo_bias_volume_full = np.where(
        np.isnan(pseudo_threshold_full) | np.isnan(pseudo_volume_full),
        np.nan,
        cmp(pseudo_volume_full, pseudo_threshold_full).astype(float),
    )
    pseudo_bias_volume_scored = pseudo_bias_volume_full[scored_row_idx]
    # excluded_row_mask still marks these rows for the caller to drop from the
    # actual L5 statistic (fold-local scoring / pooled Brier) -- their
    # pseudo_bias_volume_scored value is well-defined (real volume vs. a now-
    # correctly-computed threshold) but is not a null-world reconstruction and
    # must not be scored.
    return pseudo_volume_full, pseudo_bias_volume_scored, excluded_row_mask
