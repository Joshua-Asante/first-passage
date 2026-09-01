"""Correctness checks for the L5 pilot pipeline, run before any large-scale
simulation. The single most load-bearing property: the identity rotation
(every group draws k=0) must exactly reproduce the real, observed
bias_volume -- this is the property DESIGN.md S4.3/S4.4 explicitly require
and prior Codex review rounds flagged as broken when comparator/threshold
mismatches existed.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2] / "volregime_byyear_l4_2026-08-31"),
)

import byyear_l4  # noqa: E402
import l5_folds  # noqa: E402
import l5_null  # noqa: E402
import l5_prepare  # noqa: E402


def build_identity_rotation(day_groups: pd.DataFrame) -> dict:
    donor_of = {}
    excluded_days = set()
    for (_regime, _mask), group in day_groups.groupby(["regime", "slot_mask"], sort=False):
        days = group["trading_day"].tolist()
        if len(days) < 2:
            excluded_days.update(days)
            continue
        for day in days:
            donor_of[day] = day  # k=0
    return {"donor_of": donor_of, "excluded_days": excluded_days}


def run_checks(symbol: str) -> None:
    print(f"\n=== {symbol} ===")
    t0 = time.time()
    frame, meta = l5_prepare.prepare_l5(symbol)
    print(f"prepare_l5: {time.time()-t0:.2f}s  n_scored={meta['n_scored']}")

    ref_frame, ref_meta = byyear_l4.prepare(symbol)
    scored = frame.loc[frame["scored"]].reset_index(drop=False).rename(
        columns={"index": "full_idx"}
    )
    ref_by_time = ref_frame.set_index("time_utc")
    overlap = scored["time_utc"].isin(ref_by_time.index)
    print(f"rows overlapping byyear_l4's own scored set: {overlap.sum()}/{len(scored)}")
    joined = scored.loc[overlap].set_index("time_utc").join(ref_by_time, rsuffix="_ref")
    assert (joined["bias_volume"].astype(int) == joined["bias_volume_ref"]).all(), "bias_volume mismatch on overlap"
    assert (joined["bias_range"].astype(int) == joined["bias_range_ref"]).all(), "bias_range mismatch on overlap"
    assert (joined["outcome"].astype(int) == joined["outcome_ref"]).all(), "outcome mismatch on overlap"
    print("bias_volume/bias_range/outcome exact match on overlapping rows: OK")

    folds, setup_end = l5_folds.build_folds(scored)
    print(f"folds: n={len(folds)} setup_end={setup_end.date()}")

    t0 = time.time()
    fitted, residual = l5_null.fit_residual_regression(scored)
    print(f"fit_residual_regression: {time.time()-t0:.2f}s  resid std={residual.std():.4f}")

    day_regime = l5_null.classify_day_regime(meta["day_true_range"])
    day_groups = l5_null.build_day_groups(scored, day_regime)
    print(
        f"day_groups: n_days={len(day_groups)} "
        f"n_singleton_masks={sum(day_groups.groupby(['regime','slot_mask']).size() < 2)}"
    )

    t0 = time.time()
    plan = l5_null.build_threshold_plan(frame["slot"].to_numpy(), l5_null.WINDOW[symbol])
    identity = build_identity_rotation(day_groups)
    scored_row_idx = scored["full_idx"].to_numpy()
    pseudo_volume_full, pseudo_bias_volume, excluded_mask = l5_null.reconstruct_pseudo_volume(
        frame, fitted, residual, scored_row_idx, day_groups, identity, plan, symbol
    )
    print(f"reconstruct_pseudo_volume (identity): {time.time()-t0:.2f}s")

    real_bias_volume = scored["bias_volume"].to_numpy()
    non_excluded = ~excluded_mask
    match = np.array_equal(
        pseudo_bias_volume[non_excluded].astype(int), real_bias_volume[non_excluded].astype(int)
    )
    n_excluded = excluded_mask.sum()
    print(
        f"identity rotation reproduces real bias_volume: {match} "
        f"(excluded rows: {n_excluded}/{len(scored)})"
    )
    if not match:
        mism = np.flatnonzero(
            pseudo_bias_volume[non_excluded].astype(int) != real_bias_volume[non_excluded].astype(int)
        )
        print(f"  MISMATCH count: {len(mism)} / {non_excluded.sum()}, first few idx: {mism[:10]}")
    assert match, "IDENTITY ROTATION DOES NOT REPRODUCE REAL DATA -- load-bearing failure"

    # time a NON-identity (real random) rotation for cost estimation
    rng = np.random.default_rng(20260831)
    t0 = time.time()
    rotation = l5_null.draw_rotation(day_groups, rng)
    pseudo_volume_full2, pseudo_bias_volume2, excluded_mask2 = l5_null.reconstruct_pseudo_volume(
        frame, fitted, residual, scored_row_idx, day_groups, rotation, plan, symbol
    )
    dt_replicate = time.time() - t0
    frac_flipped = (
        pseudo_bias_volume2[non_excluded].astype(int) != real_bias_volume[non_excluded].astype(int)
    ).mean()
    print(
        f"one random-rotation replicate: {dt_replicate:.3f}s "
        f"(fraction of bias_volume flipped vs real: {frac_flipped:.3f})"
    )
    return dt_replicate


if __name__ == "__main__":
    times = []
    for symbol in ("MNQ", "MYM"):
        times.append(run_checks(symbol))
    print(f"\nmean per-replicate reconstruction time: {np.mean(times):.3f}s")
