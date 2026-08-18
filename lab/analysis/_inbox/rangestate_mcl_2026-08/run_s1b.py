"""H-RANGESTATE-CL-1 (S1b) -- daily range-state persistence, CL train era.

Frozen design: PREREG_S1B.md (same directory), committed and pull-recorded before this ran.
Replication of S1a (GC) on a second, unrelated commodity -- every function below is
byte-identical to the adversarially-verified, corrected run_s1a.py (CI_BLOCK=60 circular,
etc.). Only the panel path and output filename are re-parameterized for CL/MCL.

Object: TR_d = Wilder's True Range (daily OHLC). bias_d = 1{TR_d >= P80(TR_{d-60..d-1})}
(strictly prior 60 valid obs, no self-inclusion). y_{d+1} = 1{TR_{d+1} > P50(TR_{d-59..d})}
(prior-through-today 60 valid obs, no lookahead into d+1). Verdict cell = conditional hit rate
P(y_{d+1}=1 | bias_d=1). Roll days (instrument_id transition) excluded from TR entirely.
Weekend phantom bars (UTC-day bucketing) dropped before any TR computation.

Panel: CL.v.0 continuous, ohlcv-1d, 2010-06-06..2019-01-01 (train era; MCL micro-era reserved).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PARQUET = HERE / "cl_1d.parquet"

ROLL_WINDOW = 60          # trailing valid-TR observations
QUANTILE_BIAS = 0.80      # top-quintile threshold
QUANTILE_REF = 0.50       # median reference for the outcome
CI_BLOCK, CI_DRAWS, CI_SEED = 60, 4000, 42
PL_BLOCK, PL_PERMS, PL_SEED = 60, 2000, 7
N_FLOOR_POP, N_FLOOR_COND = 400, 100


def load_clean() -> pd.DataFrame:
    """Load the pulled panel, apply the frozen Step-0 fix (drop weekend phantom bars),
    sort by time, and return with a clean DatetimeIndex."""
    df = pd.read_parquet(PARQUET)
    df = df.sort_index()
    df = df[df.index.dayofweek < 5]  # drop Sat(5)/Sun(6) -- frozen Step-0 remedy
    df = df[~df.index.duplicated(keep="last")]
    return df


def compute_tr_with_roll_exclusion(df: pd.DataFrame) -> pd.Series:
    """Wilder's TR on the weekend-filtered daily panel, with roll-day exclusion.

    A day is a roll day if its instrument_id differs from the immediately PRECEDING
    row in this (weekend-filtered, time-sorted) frame -- i.e. adjacency is measured on
    the actual trading-day sequence, not on raw UTC calendar distance, so a Friday->
    Monday gap is never mistaken for a roll. TR is undefined (NaN, not imputed) on any
    roll day, since |H_d - C_{d-1}| / |L_d - C_{d-1}| would compare across two
    different underlying contracts' price levels.
    """
    iid = df["instrument_id"].to_numpy()
    is_roll = np.empty(len(df), dtype=bool)
    is_roll[0] = False           # first row: no prior day to compare -- also excluded below (no C_{d-1})
    is_roll[1:] = iid[1:] != iid[:-1]

    h = df["high"].to_numpy()
    l = df["low"].to_numpy()
    c = df["close"].to_numpy()
    prev_c = np.empty(len(df))
    prev_c[0] = np.nan
    prev_c[1:] = c[:-1]

    tr = np.maximum.reduce([h - l, np.abs(h - prev_c), np.abs(l - prev_c)])
    tr[0] = np.nan               # no prior close
    tr[is_roll] = np.nan         # roll day: cross-contract comparison invalid

    return pd.Series(tr, index=df.index, name="TR")


def rolling_percentile_strict_prior(tr_valid: np.ndarray, window: int, q: float) -> np.ndarray:
    """thresh[i] = the q-th percentile of tr_valid[i-window : i] (STRICTLY prior `window`
    obs, excludes index i itself). NaN until `window` prior obs exist (i >= window)."""
    n = len(tr_valid)
    out = np.full(n, np.nan)
    for i in range(window, n):
        out[i] = np.percentile(tr_valid[i - window:i], q * 100)
    return out


def rolling_percentile_through_today(tr_valid: np.ndarray, window: int, q: float) -> np.ndarray:
    """ref[i] = the q-th percentile of tr_valid[i-window+1 : i+1] (the `window` obs
    ENDING AT AND INCLUDING index i). NaN until `window` obs exist (i >= window-1)."""
    n = len(tr_valid)
    out = np.full(n, np.nan)
    for i in range(window - 1, n):
        out[i] = np.percentile(tr_valid[i - window + 1:i + 1], q * 100)
    return out


def block_shuffle_conditional_p95(bias: np.ndarray, y: np.ndarray, obs: float,
                                  block: int, nperm: int, seed: int):
    """Permute the ORDER of contiguous `block`-length chunks of the BIAS sequence
    (outcome sequence fixed) -- preserves the marginal bias distribution and its
    within-block clustering exactly; recomputes the CONDITIONAL hit rate
    P(y=1 | bias_shuffled=1) on whichever positions land bias=1 after reshuffling."""
    rng = np.random.default_rng(seed)
    n = len(bias)
    starts = list(range(0, n, block))
    chunks = [bias[s:s + block] for s in starts]
    rates = np.empty(nperm)
    ge = 0
    for i in range(nperm):
        order = rng.permutation(len(chunks))
        bp = np.concatenate([chunks[j] for j in order])[:n]
        m = bp == 1
        rates[i] = float(y[m].mean()) if m.any() else np.nan
        if not np.isnan(rates[i]) and rates[i] >= obs:
            ge += 1
    rates = rates[~np.isnan(rates)]
    return dict(mean=float(rates.mean()), p95=float(np.percentile(rates, 95)),
                p=(ge + 1) / (nperm + 1), n_valid_perms=int(len(rates)))


def block_bootstrap_ci_conditional(bias: np.ndarray, y: np.ndarray, block: int,
                                   n: int, seed: int, q=(2.5, 97.5)):
    """CIRCULAR block-bootstrap CI on the conditional hit rate (Politis-Romano):
    resample BLOCKS of the joint (bias, y) sequence with WRAPAROUND indexing
    (block start ranges over the full [0, N), not truncated to [0, N-block]), so
    pairing is preserved within each block and no boundary region is systematically
    under-sampled. Recomputes P(y=1 | bias=1) on each resample."""
    rng = np.random.default_rng(seed)
    N = len(bias)
    eff_block = block if N >= block + 1 else max(1, N // 2)
    nblocks = int(np.ceil(N / eff_block))
    pool = np.arange(0, N)  # circular: every position is a valid block start
    stats = []
    for _ in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(eff_block)[None, :]) % N  # wraparound
        idx = idx.ravel()[:N]
        bb, yy = bias[idx], y[idx]
        m = bb == 1
        if m.any():
            stats.append(float(yy[m].mean()))
    stats = np.asarray(stats)
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi)


def main():
    df = load_clean()
    print(f"panel rows after weekend-filter: {len(df)}  span {df.index.min()} -> {df.index.max()}")

    tr_full = compute_tr_with_roll_exclusion(df)
    n_roll_excluded = int(tr_full.isna().sum()) - 1  # -1 for the unavoidable first-row NaN
    print(f"TR: {tr_full.notna().sum()} valid / {len(tr_full)} total "
          f"({n_roll_excluded} roll-excluded + 1 first-row)")

    roll_dates = [str(d.date()) for d in tr_full.index[tr_full.isna()][1:]]  # [1:] drops row 0

    all_gaps = df.index.to_series().diff().dt.days
    gap_days = df.index[(all_gaps >= 4).fillna(False)]
    gap_report = [{"date": str(d.date()), "gap_calendar_days": int(all_gaps.loc[d])}
                  for d in gap_days]

    valid = tr_full.dropna()
    idx = valid.index
    tr = valid.to_numpy()
    n = len(tr)

    bias_thresh = rolling_percentile_strict_prior(tr, ROLL_WINDOW, QUANTILE_BIAS)
    bias = (tr >= bias_thresh).astype(float)
    bias[np.isnan(bias_thresh)] = np.nan

    ref_median = rolling_percentile_through_today(tr, ROLL_WINDOW, QUANTILE_REF)
    y_of_tomorrow = np.full(n, np.nan)   # y_{d+1} aligned to index d's row (predicting d+1)
    y_of_tomorrow[:-1] = (tr[1:] > ref_median[:-1]).astype(float)
    y_of_tomorrow[np.isnan(ref_median)] = np.nan

    scored = (~np.isnan(bias)) & (~np.isnan(y_of_tomorrow))
    bias_s = bias[scored].astype(int)
    y_s = y_of_tomorrow[scored].astype(int)
    days_s = idx[scored]
    n_scored = len(y_s)
    print(f"scored days (population): {n_scored}")

    p_up_unconditional = float(y_s.mean())
    f_bias1 = float(bias_s.mean())
    print(f"P(y=1) unconditional = {p_up_unconditional:.4f}   bias=1 share = {f_bias1:.4f}")

    cond_mask = bias_s == 1
    n_cond = int(cond_mask.sum())
    obs = float(y_s[cond_mask].mean()) if n_cond else float("nan")
    print(f"conditional n = {n_cond}   gateHit = P(y=1|bias=1) = {obs:.4f}")

    lo, hi = block_bootstrap_ci_conditional(bias_s, y_s, CI_BLOCK, CI_DRAWS, CI_SEED)
    h = n_cond // 2
    cond_days_order = np.where(cond_mask)[0]
    y_cond_ordered = y_s[cond_days_order]
    halves = (float(y_cond_ordered[:h].mean()), float(y_cond_ordered[h:].mean())) if n_cond >= 2 else (np.nan, np.nan)

    pl = block_shuffle_conditional_p95(bias_s, y_s, obs, PL_BLOCK, PL_PERMS, PL_SEED)

    limbs = dict(
        n_floor=bool(n_scored >= N_FLOOR_POP and n_cond >= N_FLOOR_COND),
        ci_lb=bool(lo > 0.50),
        halves=bool(halves[0] > 0.50 and halves[1] > 0.50),
        placebo=bool(obs > pl["p95"]),
    )
    verdict = ("SIGNAL" if all(limbs.values()) else
               ("AMBIGUOUS" if not limbs["n_floor"] else "NULL"))

    years = pd.Series([d.year for d in days_s[cond_mask]])
    by_year = {int(yy): float(y_cond_ordered[(years == yy).to_numpy()].mean())
               for yy in sorted(years.unique())}

    out = dict(
        n_scored_population=n_scored, n_conditional=n_cond,
        p_up_unconditional=p_up_unconditional, f_bias1=f_bias1,
        gateHit=obs, ci=(lo, hi), halves=halves, placebo=pl,
        limbs=limbs, VERDICT=verdict, by_year_conditional=by_year,
        n_roll_excluded=n_roll_excluded,
        roll_dates=roll_dates,
        gap_days_ge4_calendar=gap_report,
        panel_rows_post_weekend_filter=len(df),
        span=(str(df.index.min()), str(df.index.max())),
    )
    (HERE / "s1b_results.json").write_text(json.dumps(out, indent=1, default=str))

    print(f"\nCI=[{lo:.4f},{hi:.4f}]  halves={tuple(round(x,4) for x in halves)}")
    print(f"placebo mean={pl['mean']:.4f} p95={pl['p95']:.4f} p={pl['p']:.4f} (valid perms={pl['n_valid_perms']})")
    print(f"by_year_conditional={ {k: round(v,4) for k,v in by_year.items()} }")
    print(f"limbs={limbs}")
    print(f"\nVERDICT: {verdict}")


if __name__ == "__main__":
    main()
