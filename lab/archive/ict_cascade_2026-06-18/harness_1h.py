"""Q-ICT-CASCADE-1 / LAYER 1H (Premium/Discount) -- offline verdict harness.

Encodes PREREG-1H.md (lab/analysis/ict_cascade_2026-06-18/PREREG-1H.md) EXACTLY.
The PREREG is the lock; every FROZEN threshold below cites the PREREG section /
the gitignored Pine line it serves. No criterion is re-openable here.

WHAT THIS LAYER ASKS (PREREG-1H, TEST_PLAN H-1H + H-CASCADE)
  Does the 1H premium/discount split carry directional follow-through > coin flip
  (premium -> down, discount -> up), de-overlapped, placebo-beating, multiplicity-
  penalized -- AND does that 1H zone TRANSFER to the live 1M PD gate (range-LAG +
  price-BASIS axes)? A 1H PASS licenses the 1M PD gate ONLY if the transfer pre-gate
  clears (>=90% sign-agreement AND <=3pp rate gap on BOTH axes); else it licenses
  NOTHING (PREREG-1H "Cascade-licensing rule"; TEST_PLAN 1H-E1).

FROZEN config (PREREG-1H "frozen configuration" table; DRAFT = ict_1h_premium_discount_DRAFT.pine
bytes 7556 / LastWriteUTC 2026-06-18T17:53:06Z; 1M = ict_1m_execution.pine):
  anchor          = lookback-extremes (gate-relevant)         DRAFT L22 ; 1M L94-95
  lookN           = 60  (must equal 1M pdLookN=60)            DRAFT L27 ; 1M L62
  eqBand          = 0.05 (must equal 1M eqBand=0.05)          DRAFT L29 ; 1M L63
  fwdK            = 12  (measurement window; de-overlap unit) DRAFT L31
  zone polarity   = +1 premium->down ; -1 discount->up ; 0 EQ stand-down  lib pd L195-202
  premHit         = (zone[fwdK]==+1) AND (close < close[fwdK])  DRAFT L81-86
  discHit         = (zone[fwdK]==-1) AND (close > close[fwdK])  DRAFT L81-86

VERDICT INSTRUMENT (PREREG-1H "Resampling unit"): the DE-OVERLAPPED OFFLINE estimate.
  primary    = stride-by-fwdK=12 (one scored row / 12 bars / zone)
  cross-check= moving-block bootstrap, block = fwdK = 12 bars
  A rate's CI must clear 0.5 by >= 2pp under BOTH estimators.
  The on-chart premRate/discRate table (DRAFT L126-131) is FORBIDDEN as the verdict
  (autocorrelated by the script's own admission L15-16; PREREG-1H Forbidden #1).

n-FLOOR (PREREG-1H GENUINE CHOICE 1): effective independent windows per zone =
  floor(N_scored / fwdK). Floor = 30 per zone. Below 30 -> INSUFFICIENT-N for that
  zone; both zones below -> layer INSUFFICIENT-N (re-spec export window).

PLACEBO (PREREG-1H "Placebo 1H-E5"; GENUINE CHOICE 5): random-EQ AND sign-shuffle,
  BOTH reported; verdict uses the CLOSER/HIGHER null (conservative). Real de-overlapped
  rate must EXCEED it.

ANCHOR SWEEP + PENALTY (PREREG-1H "Anchor sweep 1H-E4"; GENUINE CHOICES 2-4):
  lookN in {40,60,80} x eqBand in {0,0.05,0.10} = 9 gate-relevant cells (anchor =
  lookback-extremes, the only gate-relevant level; swing-pair is REPORT-ONLY,
  Forbidden #6). Recompute zone from 1H OHLC via _ict_offline.pd_zone over
  highest/lowest. Penalty = deflated-Sharpe OR Bonferroni max-stat (GENUINE CHOICE 4,
  operator picks one before run 1; DSR is the default). Winner must clear 0.5 by >=2pp
  AFTER penalty. n-per-cell reported (eqBand is an n-throttle, 1H-E6).

TRANSFER PRE-GATE (PREREG-1H "Transfer pre-gate"; thresholds FROZEN >=90% AND <=3pp):
  (a) range-LAG axis (ON-CHART): native [0]-fresh `zone` vs [1]-lagged `zoneGate`
      (DRAFT L65-72). sign-agreement + rate gap.
  (b) price-BASIS axis (OFFLINE): 1-min `close` vs 1H `close` against the same
      [1]-lagged hourly range (1M L94-95,100). Recompute the 1M gate zone from the
      paired 1M export; sign-agreement + rate gap vs the 1H zone.
  REJECT (and license NOTHING) if agreement < 90% OR gap > 3pp on EITHER axis.

BIAS-CONDITIONED VARIANT (PREREG-1H "1H-E3"; GENUINE CHOICE 7): also report each rate
  split by sign of the WEEKLY structBias joined by timestamp (the 1M trades
  structBias AND PD, never PD alone; 1M L91-92,106-107). Drives AMBIGUOUS-HOLD.

HALVES-STATIONARITY SUPERSET (PREREG-1H GENUINE CHOICE 8, flagged/operator-ratifiable):
  a rate that clears overall but flips its >0.5 margin sign across the two chronological
  halves routes to AMBIGUOUS-HOLD (one-regime), not RESOLVED.

CONVENTIONS (PREREG-1H + repo): look-ahead-free; ET=America/New_York (DST-aware);
  TV BAR_EXPORT epoch is UTC -> convert UTC->ET for sessions/DOW. ASCII only. The
  real-export entrypoints SKIP cleanly when the export is absent (operator has not run
  TV yet) and print exactly which export(s) are needed.

Run the unit tests (synthetic, no vendor data):
  python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_1h.py -q
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ict_offline as M  # noqa: E402  (shared detectors + stats; do not re-port)

# -----------------------------------------------------------------------------
# FROZEN constants (PREREG-1H -- do not edit during the verdict window)
# -----------------------------------------------------------------------------
FWDK = 12                       # DRAFT L31 (measurement horizon; de-overlap unit + block)
LOOKN_LOCK = 60                 # DRAFT L27 ; must equal 1M pdLookN (1M L62)
EQBAND_LOCK = 0.05              # DRAFT L29 ; must equal 1M eqBand (1M L63)
MARGIN_PP = 0.02               # PREREG-1H >=2pp clearance of 0.5 (set by H-CASCADE/sec 6)
N_FLOOR = 30                   # PREREG-1H GENUINE CHOICE 1 (effective windows / zone)
TRANSFER_AGREE_MIN = 0.90      # PREREG-1H transfer pre-gate (>=90%)
TRANSFER_GAP_MAX_PP = 0.03     # PREREG-1H transfer pre-gate (<=3pp)
LOOKN_GRID = (40, 60, 80)      # GENUINE CHOICE 2 (60 forced; +/-20 neighbors)
EQBAND_GRID = (0.0, 0.05, 0.10)  # GENUINE CHOICE 3 (0.05 forced; 0 + 0.10 bracket)
N_CELLS = len(LOOKN_GRID) * len(EQBAND_GRID)   # 9 (PREREG-1H, declared before run 1)
GAMMA = 0.5772156649           # Euler-Mascheroni (DSR E[max] approx, dsr.py)

# de-overlap stride/block + bootstrap config
STRIDE = FWDK                  # primary de-overlap (PREREG-1H resampling unit #1)
BLOCK = FWDK                   # block-bootstrap block length (GENUINE CHOICE 6)
B_BOOT = 5000                  # bootstrap resamples (CI instrument)
B_PLACEBO = 2000               # placebo resamples (sign-shuffle / random-EQ)
SEED = 20260618                # pinned (reproducibility)


# =============================================================================
# DATA STRUCTURES
# =============================================================================
@dataclass
class HourExport:
    """Parsed 1H indicator export (PREREG-1H CONSUMES col set).

    cols: time, open, high, low, close, zone, eq, premHit, discHit, zoneGate, zoneAgree.
    epoch_ms is UTC (TV BAR_EXPORT); et_* are derived (DST-aware).
    """
    epoch_ms: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    zone: np.ndarray          # native [0]-fresh zone (DRAFT L44-57)
    eq: np.ndarray
    prem_hit: np.ndarray      # exported premHit (audited vs recompute)
    disc_hit: np.ndarray      # exported discHit
    zone_gate: np.ndarray     # [1]-lagged gate-basis zone (DRAFT L65-72)
    zone_agree: np.ndarray    # on-chart agree flag (smoke; not the verdict)
    et_hour: np.ndarray = field(default_factory=lambda: np.array([]))
    et_date: np.ndarray = field(default_factory=lambda: np.array([]))
    n: int = 0


@dataclass
class MinuteExport:
    """Parsed paired 1M export (PREREG-1H price-BASIS axis CONSUMES col set).

    cols: time, netBias, zone, inKZ, close. `zone` here is the 1M gate zone computed
    from the [1]-lagged hourly range vs the 1-MIN close (1M L94-95,100) -- the
    price-BASIS the transfer must license.
    """
    epoch_ms: np.ndarray
    net_bias: np.ndarray
    zone: np.ndarray
    in_kz: np.ndarray
    close: np.ndarray
    n: int = 0


# =============================================================================
# LOADERS (export parsing; skip-clean handled in main())
# =============================================================================
def _to_epoch_ms(time_col):
    """Coerce a `time` column to UTC epoch-ms int64. Accepts int/float epochs (ms or
    s) or ISO strings. TV BAR_EXPORT epoch is UTC (PREREG-1H convention)."""
    s = pd.Series(time_col)
    if pd.api.types.is_numeric_dtype(s):
        vals = s.to_numpy(dtype="float64")
        # heuristic: ~1e12 -> ms, ~1e9 -> s. Use 1e11 as the split.
        if np.nanmedian(vals) < 1e11:
            vals = vals * 1000.0
        return vals.astype("int64")
    t = pd.to_datetime(s, utc=True)
    # tz-aware -> UTC ms epoch. Drop the tz (already UTC) to a naive datetime64, then
    # cast via numpy datetime64[ms] so the result is resolution-independent (pandas may
    # store us/ns); .astype int64 on [ms] == epoch ms. (tz_localize(None) on a UTC
    # series yields the UTC wall-clock, which is the epoch we want.)
    return t.dt.tz_localize(None).to_numpy().astype("datetime64[ms]").astype("int64")


def load_hour_export(path) -> HourExport:
    """Load the 1H indicator export. Required cols per PREREG-1H CONSUMES."""
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    need = ["time", "open", "high", "low", "close", "zone", "eq",
            "premhit", "dischit", "zonegate", "zoneagree"]
    missing = [c for c in need if c not in cols]
    if missing:
        raise ValueError(f"1H export missing columns {missing}; have {list(df.columns)}")
    epoch = _to_epoch_ms(df[cols["time"]])
    hh, _mm, _dow, date = M.et_fields(epoch)
    return HourExport(
        epoch_ms=epoch,
        o=df[cols["open"]].to_numpy(float),
        h=df[cols["high"]].to_numpy(float),
        l=df[cols["low"]].to_numpy(float),
        c=df[cols["close"]].to_numpy(float),
        zone=df[cols["zone"]].to_numpy(float),
        eq=df[cols["eq"]].to_numpy(float),
        prem_hit=df[cols["premhit"]].to_numpy(float),
        disc_hit=df[cols["dischit"]].to_numpy(float),
        zone_gate=df[cols["zonegate"]].to_numpy(float),
        zone_agree=df[cols["zoneagree"]].to_numpy(float),
        et_hour=hh, et_date=date, n=len(df),
    )


def load_minute_export(path) -> MinuteExport:
    """Load the paired 1M export (price-BASIS axis). Required cols per PREREG-1H."""
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    need = ["time", "netbias", "zone", "inkz", "close"]
    missing = [c for c in need if c not in cols]
    if missing:
        raise ValueError(f"1M export missing columns {missing}; have {list(df.columns)}")
    epoch = _to_epoch_ms(df[cols["time"]])
    return MinuteExport(
        epoch_ms=epoch,
        net_bias=df[cols["netbias"]].to_numpy(float),
        zone=df[cols["zone"]].to_numpy(float),
        in_kz=df[cols["inkz"]].to_numpy(float),
        close=df[cols["close"]].to_numpy(float),
        n=len(df),
    )


# =============================================================================
# HIT RECOMPUTATION (look-ahead audit, PREREG-1H / TEST_PLAN 1H sec 7.B item 6)
# =============================================================================
def recompute_hits(zone, close, fwd_k=FWDK):
    """Recompute premHit/discHit faithfully from raw zone/close, indexed at the
    DECISION bar (Pine DRAFT L81-86; PREREG-1H L52).

    Pine records the hit at the RESOLUTION bar t using HISTORICAL offsets
    (`zone[fwdK]`/`close[fwdK]` = fwdK bars BACK):
        premHit_t = (zone[t-fwd_k]==+1) AND (close[t] < close[t-fwd_k])   # premium resolved DOWN
        discHit_t = (zone[t-fwd_k]==-1) AND (close[t] > close[t-fwd_k])   # discount resolved UP
    Re-indexed to the DECISION bar d = t-fwd_k, the identical EVENT is:
        prem[d] = (zone[d]==+1) AND (close[d+fwd_k] < close[d])           # premium -> DOWN
        disc[d] = (zone[d]==-1) AND (close[d+fwd_k] > close[d])           # discount -> UP
    The decision-bar form is consistent with _zone_hit_vectors / bias_conditioned /
    placebo_random_eq, which all select the scored zone on the SAME bar d (zone[d]==
    target), and it yields the IDENTICAL de-overlapped rate as Pine's resolution-bar
    form. (audit_exported_hits validates the EXPORTED columns against Pine's
    resolution-bar form via _pine_resolution_hits.)

    Look-ahead-free as a MEASUREMENT: the hit at decision bar d is only KNOWN fwd_k
    bars later; only bars with d+fwd_k < n are scorable. Returns (prem_hit, disc_hit,
    scorable) of length n; the non-scorable tail (last fwd_k bars) is 0/False.

    DEFECT FIX 2026-06-19 (lesson M-ICT-1H-OFFSET): the prior version used a FORWARD
    array index zone[i+fwd_k] (the FUTURE zone) with close[i] < close[i+fwd_k] (price
    UP), inverting the time arrow into "price rose INTO a premium zone" -- the
    COMPLEMENT of the claim. It matched the exported Pine premHit only ~36%; this
    decision-bar form scores the premium->down EVENT exactly.
    """
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    n = len(zone)
    prem = np.zeros(n, bool)
    disc = np.zeros(n, bool)
    scorable = np.zeros(n, bool)
    for i in range(n - fwd_k):
        j = i + fwd_k
        scorable[i] = True
        if zone[i] == 1 and close[j] < close[i]:     # premium NOW -> price LOWER fwd_k bars later (DOWN)
            prem[i] = True
        if zone[i] == -1 and close[j] > close[i]:    # discount NOW -> price HIGHER fwd_k bars later (UP)
            disc[i] = True
    return prem, disc, scorable


def _pine_resolution_hits(zone, close, fwd_k=FWDK):
    """Pine's per-bar premHit/discHit AS EXPORTED, at the RESOLUTION bar t with the
    HISTORICAL offsets the Pine source uses (DRAFT L81-86):
        premHit_t = (zone[t-fwd_k]==+1) AND (close[t] < close[t-fwd_k])
        discHit_t = (zone[t-fwd_k]==-1) AND (close[t] > close[t-fwd_k])
    This reproduces what TV writes to the export columns. It is used ONLY by
    audit_exported_hits to validate the exported columns -- NOT as the verdict basis
    (the verdict uses the decision-bar recompute_hits, which scores the identical
    EVENT). Returns (prem, disc, scorable) of length n; scorable is False for the
    warmup HEAD (t < fwd_k) and for EQ bars (zone[t-fwd_k]==0)."""
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    n = len(zone)
    prem = np.zeros(n, bool)
    disc = np.zeros(n, bool)
    scorable = np.zeros(n, bool)
    for t in range(fwd_k, n):
        zt = zone[t - fwd_k]
        if zt == 1:
            scorable[t] = True
            if close[t] < close[t - fwd_k]:
                prem[t] = True
        elif zt == -1:
            scorable[t] = True
            if close[t] > close[t - fwd_k]:
                disc[t] = True
    return prem, disc, scorable


def audit_exported_hits(ex: HourExport, fwd_k=FWDK, tol_frac=0.0):
    """PREREG-1H / TEST_PLAN item 6: validate the EXPORTED premHit/discHit columns
    against a faithful reproduction of Pine's resolution-bar formula (DRAFT L81-86,
    via _pine_resolution_hits). Returns ok=True when the exported columns match (a
    clean, faithful export); a mismatch flags a Pine<->offline discrepancy or an
    export polarity drift. tol_frac is the max allowed disagreement fraction
    (default 0 -> exact).

    NOTE (M-ICT-1H-OFFSET fix): the verdict does NOT depend on the exported columns --
    it scores the decision-bar recompute_hits, which measures the identical
    premium->down EVENT. This audit is purely an export-faithfulness check, so it
    compares against Pine's RESOLUTION-bar form (matching how TV emits the columns),
    NOT recompute_hits' decision-bar indexing. The prior version compared the exported
    columns against the (then-inverted) recompute_hits and, on a real export, fired
    ok=False at ~49% mismatch -- which it then mis-handled by discarding the CORRECT
    exported columns in favor of the buggy recompute."""
    prem, disc, scorable = _pine_resolution_hits(ex.zone, ex.c, fwd_k)
    idx = np.where(scorable)[0]
    if len(idx) == 0:
        return {"ok": False, "reason": "no scorable rows", "prem_mismatch": np.nan,
                "disc_mismatch": np.nan}
    pm = float(np.mean(prem[idx] != (ex.prem_hit[idx] > 0)))
    dm = float(np.mean(disc[idx] != (ex.disc_hit[idx] > 0)))
    ok = (pm <= tol_frac) and (dm <= tol_frac)
    return {"ok": ok, "prem_mismatch": pm, "disc_mismatch": dm,
            "reason": "" if ok else "exported hit columns disagree with Pine reproduction"}


# =============================================================================
# ZONE RECOMPUTATION from 1H OHLC (anchor sweep cells; PREREG-1H 1H-E4)
# =============================================================================
def zone_series(high, low, close, look_n, eq_band):
    """Native [0]-fresh zone over an INCLUSIVE lookback-extremes range (DRAFT L44-57).

    range = highest(high, look_n) / lowest(low, look_n) INCLUSIVE of the current bar
    (DRAFT uses ta.highest/lowest(high/low, lookN) against the current 1H close).
    Returns int array (NaN warmup -> 0=EQ stand-down). Uses _ict_offline.pd_zone +
    highest/lowest (do not re-implement).
    """
    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)
    n = len(close)
    rh = M.highest(high, look_n)
    rl = M.lowest(low, look_n)
    z = np.zeros(n, int)
    for i in range(n):
        if np.isnan(rh[i]) or np.isnan(rl[i]):
            z[i] = 0
            continue
        zi, _ = M.pd_zone(rh[i], rl[i], close[i], eq_band)
        z[i] = zi
    return z


def gate_zone_series(high, low, close, look_n, eq_band):
    """[1]-lagged gate-basis zone (DRAFT L65-66): range from highest(high,lookN)[1] /
    lowest(low,lookN)[1] (exclude current bar) vs the current close. This is the
    range-LAG axis of the transfer pre-gate. Returns int array (NaN warmup -> 0)."""
    high = np.asarray(high, float)
    low = np.asarray(low, float)
    close = np.asarray(close, float)
    n = len(close)
    rh = M.highest(high, look_n)
    rl = M.lowest(low, look_n)
    # [1]-lag: shift the rolling extremes forward by one bar (exclude current).
    rh_lag = np.concatenate([[np.nan], rh[:-1]])
    rl_lag = np.concatenate([[np.nan], rl[:-1]])
    z = np.zeros(n, int)
    for i in range(n):
        if np.isnan(rh_lag[i]) or np.isnan(rl_lag[i]):
            z[i] = 0
            continue
        zi, _ = M.pd_zone(rh_lag[i], rl_lag[i], close[i], eq_band)
        z[i] = zi
    return z


# =============================================================================
# RATE + DE-OVERLAP ESTIMATORS (PREREG-1H resampling unit)
# =============================================================================
def _zone_hit_vectors(zone, prem_hit, disc_hit, scorable):
    """Per-zone 0/1 hit vectors over SCORABLE rows only.
    premium rows: zone==+1 ; discount rows: zone==-1.
    Returns (prem_vec, disc_vec, prem_idx, disc_idx) where *_idx are the bar indices
    (for stride de-overlap)."""
    zone = np.asarray(zone, float)
    ph = np.asarray(prem_hit, float)
    dh = np.asarray(disc_hit, float)
    sc = np.asarray(scorable, bool)
    prem_idx = np.where(sc & (zone == 1))[0]
    disc_idx = np.where(sc & (zone == -1))[0]
    return (ph[prem_idx].astype(float), dh[disc_idx].astype(float),
            prem_idx, disc_idx)


def stride_rate_ci(hit_vec, bar_idx, stride=STRIDE, alpha=0.05):
    """Stride-by-fwdK de-overlap (PREREG-1H primary). Keep one scored row every
    `stride` bars (in bar-index space) so forward windows do not overlap, then CI
    the de-overlapped hit vector.

    Returns dict: n_eff, rate, ci_lo, ci_hi, clears (CI clears 0.5 by >=MARGIN_PP).
    The CI here is a normal-approx on the n_eff INDEPENDENT windows -- after stride
    de-overlap the windows are non-overlapping, so an iid CI is valid (this is NOT the
    forbidden iid-on-overlapping move 1H-E2; it is iid on de-overlapped rows).
    """
    hit_vec = np.asarray(hit_vec, float)
    bar_idx = np.asarray(bar_idx)
    if len(hit_vec) == 0:
        return {"n_eff": 0, "rate": np.nan, "ci_lo": np.nan, "ci_hi": np.nan,
                "clears": False}
    # greedy stride in bar-index space: take the first scorable row, then the next
    # whose bar index is >= last_taken + stride.
    keep = []
    last = -10**9
    for k in range(len(bar_idx)):
        if bar_idx[k] >= last + stride:
            keep.append(k)
            last = bar_idx[k]
    sub = hit_vec[keep]
    n_eff = len(sub)
    rate = float(sub.mean())
    if n_eff < 2:
        return {"n_eff": n_eff, "rate": rate, "ci_lo": np.nan, "ci_hi": np.nan,
                "clears": False}
    se = np.sqrt(max(rate * (1.0 - rate), 1e-12) / n_eff)
    from scipy.stats import norm
    z = norm.ppf(1.0 - alpha / 2.0)
    lo = rate - z * se
    hi = rate + z * se
    clears = lo > 0.5 + MARGIN_PP
    return {"n_eff": n_eff, "rate": rate, "ci_lo": float(lo), "ci_hi": float(hi),
            "clears": bool(clears)}


def block_rate_ci(hit_vec, block_len=BLOCK, B=B_BOOT, seed=SEED, alpha=0.05):
    """Moving-block bootstrap cross-check (PREREG-1H resampling unit #2; block=fwdK=12).
    Uses _ict_offline.moving_block_bootstrap_ci (do not reinvent). The point estimate
    is read on ALL scored rows in the zone; the CI resamples by the block unit.

    Returns dict: n_scored, rate, ci_lo, ci_hi, clears (CI clears 0.5 by >=MARGIN_PP).
    """
    hit_vec = np.asarray(hit_vec, float)
    if len(hit_vec) == 0:
        return {"n_scored": 0, "rate": np.nan, "ci_lo": np.nan, "ci_hi": np.nan,
                "clears": False}
    rate = float(hit_vec.mean())
    lo, hi = M.moving_block_bootstrap_ci(hit_vec, block_len, B, seed, alpha)
    clears = (not np.isnan(lo)) and (lo > 0.5 + MARGIN_PP)
    return {"n_scored": len(hit_vec), "rate": rate, "ci_lo": float(lo),
            "ci_hi": float(hi), "clears": bool(clears)}


def effective_n(zone, scorable, target_zone, fwd_k=FWDK):
    """PREREG-1H n-floor basis: effective independent windows = floor(N_scored / fwdK)
    per zone. target_zone is +1 (premium) or -1 (discount)."""
    zone = np.asarray(zone, float)
    sc = np.asarray(scorable, bool)
    n_scored = int(np.sum(sc & (zone == target_zone)))
    return n_scored // fwd_k


# =============================================================================
# PLACEBO (regression-to-the-range, PREREG-1H 1H-E5)
# =============================================================================
def placebo_random_eq(zone, prem_hit, disc_hit, scorable, which, seed=SEED, B=B_PLACEBO):
    """random-EQ null (PREREG-1H 1H-E5): shuffle the premium/discount label assignment
    at the MATCHED base frequency, recompute the rate. `which` in {'prem','disc'}.

    The regression-to-the-range floor: with labels randomized but the same base
    frequency and the same forward outcomes, what rate does the mechanism alone give?
    Returns the mean placebo de-overlapped rate over B shuffles (point estimate on the
    full scorable set, matching the on-chart rate basis but with shuffled labels).
    """
    zone = np.asarray(zone, float)
    sc = np.asarray(scorable, bool)
    idx = np.where(sc)[0]
    if len(idx) == 0:
        return np.nan
    rng = np.random.default_rng(seed)
    if which == "prem":
        hit = np.asarray(prem_hit, float)[idx]
        target = 1
    else:
        hit = np.asarray(disc_hit, float)[idx]
        target = -1
    n_target = int(np.sum(zone[idx] == target))
    n = len(idx)
    if n_target == 0:
        return np.nan
    rates = np.empty(B)
    for b in range(B):
        pick = rng.choice(n, size=n_target, replace=False)
        rates[b] = hit[pick].mean()
    return float(rates.mean())


def placebo_sign_shuffle(zone, close, scorable, which, fwd_k=FWDK, block=BLOCK,
                         seed=SEED, B=B_PLACEBO):
    """sign-shuffle null (PREREG-1H 1H-E5): block-permute the `zone` sign labels
    against the realized forward returns (block = fwdK), recompute the rate. `which`
    in {'prem','disc'}.

    Block-permute zone in chunks of `block` bars (preserves the local autocorrelation
    of the label stream), then recompute the hit on the SAME realized forward returns.
    Returns the mean placebo rate over B block-permutations.
    """
    zone = np.asarray(zone, float)
    close = np.asarray(close, float)
    sc = np.asarray(scorable, bool)
    n = len(zone)
    idx = np.where(sc)[0]
    if len(idx) == 0:
        return np.nan
    # realized forward direction for each scorable bar (decision-bar d=i, outcome at
    # i+fwd_k; consistent with recompute_hits' decision-bar form -- M-ICT-1H-OFFSET fix)
    fwd_down = np.zeros(n, bool)
    fwd_up = np.zeros(n, bool)
    for i in idx:
        j = i + fwd_k
        if j < n:
            fwd_down[i] = close[j] < close[i]    # price resolved DOWN over the next fwd_k bars
            fwd_up[i] = close[j] > close[i]       # price resolved UP
    rng = np.random.default_rng(seed + 1)
    # block structure over the full series
    n_blocks = int(np.ceil(n / block))
    rates = np.empty(B)
    for b in range(B):
        order = rng.permutation(n_blocks)
        zperm = np.empty(n)
        pos = 0
        for blk in order:
            s = blk * block
            e = min(s + block, n)
            chunk = zone[s:e]
            zperm[pos:pos + len(chunk)] = chunk
            pos += len(chunk)
        zperm = zperm[:n]
        if which == "prem":
            sel = sc & (zperm == 1)
            hit = (fwd_down & sel)
        else:
            sel = sc & (zperm == -1)
            hit = (fwd_up & sel)
        denom = int(np.sum(sel))
        rates[b] = (np.sum(hit) / denom) if denom > 0 else np.nan
    return float(np.nanmean(rates))


def placebo_floor(zone, close, prem_hit, disc_hit, scorable, which):
    """PREREG-1H GENUINE CHOICE 5: report BOTH nulls; the verdict uses the
    CLOSER/HIGHER one (the conservative floor the real rate must beat)."""
    req = placebo_random_eq(zone, prem_hit, disc_hit, scorable, which)
    sss = placebo_sign_shuffle(zone, close, scorable, which)
    vals = [v for v in (req, sss) if not (v is None or np.isnan(v))]
    floor = max(vals) if vals else np.nan
    return {"random_eq": req, "sign_shuffle": sss, "floor": floor}


# =============================================================================
# ANCHOR SWEEP + MULTIPLICITY PENALTY (PREREG-1H 1H-E4)
# =============================================================================
def _cell_rate(ex: HourExport, look_n, eq_band, which):
    """Recompute zone for one (lookN, eqBand) cell from the 1H OHLC, recompute hits,
    and return the de-overlapped (stride) rate + effective-N for the requested zone.
    `which` in {'prem','disc'}."""
    z = zone_series(ex.h, ex.l, ex.c, look_n, eq_band)
    prem, disc, sc = recompute_hits(z, ex.c, FWDK)
    pv, dv, pidx, didx = _zone_hit_vectors(z, prem, disc, sc)
    if which == "prem":
        st = stride_rate_ci(pv, pidx)
        n_eff = effective_n(z, sc, 1)
    else:
        st = stride_rate_ci(dv, didx)
        n_eff = effective_n(z, sc, -1)
    return {"look_n": look_n, "eq_band": eq_band, "which": which,
            "rate": st["rate"], "n_eff": n_eff, "stride": st}


def anchor_sweep(ex: HourExport, which):
    """9-cell grid (lookN x eqBand) for one zone. Returns list of cell dicts +
    n-per-cell. The swing-pair anchor is REPORT-ONLY (Forbidden #6) and is NOT
    swept here -- only lookback-extremes (the gate-relevant level)."""
    cells = []
    for look_n in LOOKN_GRID:
        for eq_band in EQBAND_GRID:
            cells.append(_cell_rate(ex, look_n, eq_band, which))
    return cells


def deflated_max_stat_penalty(cells, n_cells=N_CELLS):
    """Penalty over the grid (PREREG-1H 1H-E4; GENUINE CHOICE 4 = DSR default).

    Treats each cell's de-overlapped rate as a per-cell statistic in [0,1]. The
    deflated max-stat threshold is the expected MAX of n_cells independent draws under
    the null (rate ~ 0.5). We use the Bailey-Lopez de Prado E[max] form (dsr.py):
        E[max] ~ E + sqrt(Var) * ((1-g)*Phi^-1(1-1/N) + g*Phi^-1(1-1/(N*e)))
    with null mean E=0.5 and per-cell SE estimated from the cell's effective-N
    (Var = mean rate variance / n_eff across cells). The winning cell PASSES the
    penalty iff its (rate - MARGIN_PP) lower edge still exceeds this deflated
    threshold AND its CI clears 0.5 by >= MARGIN_PP (the per-cell stride gate).

    Bonferroni fallback (GENUINE CHOICE 4 alternative) is also reported: per-cell
    alpha' = 0.05 / n_cells; winner must clear under the tighter per-cell CI. The
    operator picks DSR or Bonferroni before run 1; both are emitted so the choice is
    transparent.
    """
    from scipy.stats import norm
    valid = [c for c in cells if c["n_eff"] >= 2 and not np.isnan(c["rate"])]
    if not valid:
        return {"winner": None, "pass_dsr": False, "pass_bonf": False,
                "e_max": np.nan, "reason": "no valid cells"}
    winner = max(valid, key=lambda c: c["rate"])
    rates = np.array([c["rate"] for c in valid])
    # per-cell SE under null p=0.5 using each cell's effective-N (the de-overlap unit)
    n_eff_arr = np.array([max(c["n_eff"], 1) for c in valid], float)
    var_cell = np.mean(0.25 / n_eff_arr)        # mean null rate-variance across cells
    N = n_cells
    e_max = 0.5 + np.sqrt(var_cell) * (
        (1 - GAMMA) * norm.ppf(1 - 1.0 / N) + GAMMA * norm.ppf(1 - 1.0 / (N * np.e)))
    # DSR-style: winner's stride CI lower bound must clear BOTH 0.5+margin AND e_max
    w_lo = winner["stride"]["ci_lo"]
    pass_dsr = (not np.isnan(w_lo)) and (w_lo > 0.5 + MARGIN_PP) and (w_lo > e_max)
    # Bonferroni: re-CI the winner at alpha' = 0.05/N (tighter), must clear 0.5+margin
    alpha_b = 0.05 / N
    z_b = norm.ppf(1.0 - alpha_b / 2.0)
    w_rate = winner["rate"]
    w_neff = max(winner["n_eff"], 1)
    se_b = np.sqrt(max(w_rate * (1 - w_rate), 1e-12) / w_neff)
    lo_b = w_rate - z_b * se_b
    pass_bonf = lo_b > 0.5 + MARGIN_PP
    return {"winner": winner, "pass_dsr": bool(pass_dsr), "pass_bonf": bool(pass_bonf),
            "e_max": float(e_max), "bonf_lo": float(lo_b), "winner_ci_lo": float(w_lo)}


# =============================================================================
# TRANSFER PRE-GATE (PREREG-1H, both axes; thresholds FROZEN >=90% AND <=3pp)
# =============================================================================
def _sign_agreement(za, zb, restrict_nonzero=False, mask=None):
    """Agreement rate between two zone arrays. Returns (agree_rate, n).

    Default (restrict_nonzero=False) is RAW equality over every row in `mask`
    (or every row if `mask` is None): zone==zoneGate INCLUDING 0==0 (EQ==EQ) counts
    as AGREE, and a 0-vs-nonzero row is a DISAGREE that STAYS in the denominator.
    This matches the DRAFT Pine `zoneAgree`/`agreeRate` semantic exactly (DRAFT L72
    `zoneAgree = ... zone == zoneGate`; L75-78 counts over ALL confirmed valid &
    gateValid bars). The range-LAG transfer axis (PREREG-1H L83) is tied to that
    Pine agreeRate, so it MUST use this raw-equality path -- dropping EQ rows would
    let the offline estimate read ~100% where Pine reads <90% and falsely license
    the 1M PD gate (FINDING 1H-CRITICAL).

    restrict_nonzero=True keeps only rows where BOTH zones are non-zero (dropping
    every EQ row from numerator AND denominator). This is NOT the Pine agreeRate
    basis and is NOT the range-LAG verdict instrument; it is retained only for
    diagnostic both-nonzero comparisons, never for the transfer pre-gate.

    `mask` (optional bool array) restricts the rows considered to the valid &
    gateValid bars (Pine L75 guard: only `valid and gateValid` confirmed bars enter
    the agreement count). Combined with restrict_nonzero it is intersected.
    """
    za = np.asarray(za, float)
    zb = np.asarray(zb, float)
    n = min(len(za), len(zb))
    za, zb = za[:n], zb[:n]
    if mask is None:
        sel = np.ones(n, bool)
    else:
        sel = np.asarray(mask, bool)[:n].copy()
    if restrict_nonzero:
        sel = sel & (za != 0) & (zb != 0)
    denom = int(np.sum(sel))
    if denom == 0:
        return (np.nan, 0)
    agree = float(np.mean(za[sel] == zb[sel]))
    return (agree, denom)


def _valid_gate_valid_mask(ex: HourExport, look_n=LOOKN_LOCK):
    """Reconstruct Pine's `valid and gateValid` confirmed-bar mask (DRAFT L51, L67)
    from the 1H OHLC at the locked lookN. Only these bars enter the Pine agreeRate
    count (DRAFT L75), so the offline range-LAG agreement must be measured over the
    same mask -- otherwise warmup `0==0` rows would be counted as agree (Pine never
    counts them) and the agreement would not match agreeRate.

      valid     : native range defined AND rHigh > rLow (DRAFT L51)
      gateValid : [1]-lagged range defined AND rHighGate > rLowGate (DRAFT L67)
    Returns a bool array of length ex.n.
    """
    high = np.asarray(ex.h, float)
    low = np.asarray(ex.l, float)
    rh = M.highest(high, look_n)
    rl = M.lowest(low, look_n)
    rh_lag = np.concatenate([[np.nan], rh[:-1]])
    rl_lag = np.concatenate([[np.nan], rl[:-1]])
    valid = (~np.isnan(rh)) & (~np.isnan(rl)) & (rh > rl)
    gate_valid = (~np.isnan(rh_lag)) & (~np.isnan(rl_lag)) & (rh_lag > rl_lag)
    return valid & gate_valid


def transfer_range_lag_axis(ex: HourExport):
    """(a) range-LAG axis (PREREG-1H ON-CHART): native [0]-fresh `zone` vs [1]-lagged
    `zoneGate` (DRAFT L65-72). Metric = sign-agreement + rate gap |premRate/discRate
    (native) - rate(zoneGate basis)|. PASS iff agreement >=90% AND gap <=3pp.

    AGREEMENT (FINDING 1H-CRITICAL): PREREG-1H L83 ties this metric to the Pine
    agreeRate (DRAFT L78), which counts agreement over ALL confirmed valid &
    gateValid bars with zone==zoneGate INCLUDING 0==0 (EQ==EQ) as agree and a
    0-vs-nonzero row as a DISAGREE that stays in the denominator. So we use raw
    equality (restrict_nonzero=False) masked to the valid & gateValid bars; we do
    NOT drop EQ rows (the both-nonzero path would inflate agreement to ~100% where
    Pine reads <90% and wrongly license the 1M PD gate).

    The rate gap uses the de-overlapped (stride) premRate (premium zone) as the
    representative rate, recomputed on the native zone vs the gate zone, taking the
    LARGER of the premium/discount gaps (conservative)."""
    vg_mask = _valid_gate_valid_mask(ex)
    agree, n_agree = _sign_agreement(ex.zone, ex.zone_gate, restrict_nonzero=False,
                                     mask=vg_mask)
    # native rates
    p_n, d_n, sc_n = recompute_hits(ex.zone, ex.c, FWDK)
    pv_n, dv_n, pidx_n, didx_n = _zone_hit_vectors(ex.zone, p_n, d_n, sc_n)
    prem_native = stride_rate_ci(pv_n, pidx_n)["rate"]
    disc_native = stride_rate_ci(dv_n, didx_n)["rate"]
    # gate-basis rates (hits recomputed on the [1]-lagged gate zone)
    p_g, d_g, sc_g = recompute_hits(ex.zone_gate, ex.c, FWDK)
    pv_g, dv_g, pidx_g, didx_g = _zone_hit_vectors(ex.zone_gate, p_g, d_g, sc_g)
    prem_gate = stride_rate_ci(pv_g, pidx_g)["rate"]
    disc_gate = stride_rate_ci(dv_g, didx_g)["rate"]
    gaps = [abs(a - b) for a, b in ((prem_native, prem_gate), (disc_native, disc_gate))
            if not (np.isnan(a) or np.isnan(b))]
    gap = max(gaps) if gaps else np.nan
    clears = (not np.isnan(agree)) and agree >= TRANSFER_AGREE_MIN and \
             (not np.isnan(gap)) and gap <= TRANSFER_GAP_MAX_PP
    return {"axis": "range_lag", "agree": agree, "n_agree": n_agree, "gap": gap,
            "prem_native": prem_native, "prem_gate": prem_gate,
            "disc_native": disc_native, "disc_gate": disc_gate, "clears": bool(clears)}


def _join_hour_to_minute(ex: HourExport, mn: MinuteExport):
    """Map each 1H bar to the 1M gate zone in force at the START of that hour. The 1M
    gate zone is recomputed per-minute from the [1]-lagged hourly range vs the 1-min
    close (1M L94-95,100) and is carried in `mn.zone`. We take the 1M zone at the
    minute whose epoch == the 1H bar's epoch (hour open). Returns (hour_zone,
    minute_zone, valid_mask) aligned arrays over matched timestamps.

    valid_mask[k] marks the k-th joined bar as a valid & gateValid 1H confirmed bar
    (per _valid_gate_valid_mask, DRAFT L51/L67) AND the joined 1M zone defined
    (non-warmup). Only these enter the EQ-inclusive price-BASIS agreement -- mirroring
    the range-LAG axis's valid&gateValid masking; without it, warmup 0==0 rows would
    count as agreement (PR #198 follow-up #1, ALIGN)."""
    vg_mask = _valid_gate_valid_mask(ex)
    m_map = {int(t): z for t, z in zip(mn.epoch_ms, mn.zone)}
    hz, mz, vm = [], [], []
    for i, (t, z) in enumerate(zip(ex.epoch_ms, ex.zone)):
        key = int(t)
        if key in m_map:
            mzv = m_map[key]
            hz.append(z)
            mz.append(mzv)
            vm.append(bool(vg_mask[i]) and not bool(np.isnan(mzv)))
    return np.array(hz, float), np.array(mz, float), np.array(vm, bool)


def transfer_price_basis_axis(ex: HourExport, mn: MinuteExport):
    """(b) price-BASIS axis (PREREG-1H OFFLINE-only): 1-min `close` vs 1H `close`
    against the same [1]-lagged hourly range (1M L94-95,100). Sign-agreement + rate
    gap of the 1M gate zone vs the 1H zone, joined by timestamp. PASS iff agreement
    >=90% AND gap <=3pp.

    The 1M gate zone is the price-BASIS the live gate actually reads; if it disagrees
    with the 1H zone the cheap 1H proxy licenses nothing about the 1M gate (1H-E1)."""
    hz, mz, vm = _join_hour_to_minute(ex, mn)
    if len(hz) == 0:
        return {"axis": "price_basis", "agree": np.nan, "n_agree": 0, "gap": np.nan,
                "clears": False, "reason": "no timestamp overlap 1H<->1M"}
    # price-BASIS axis (ALIGNED 2026-06-18, PR #198 follow-up #1 / PREREG-1H amendment):
    # EQ-inclusive raw equality over valid & gateValid joined bars, MATCHING the
    # range-LAG axis. The old restrict_nonzero=True dropped EQ-vs-nonzero rows -- which
    # are GENUINE transfer failures (1H directional, the 1M-basis the live gate reads in
    # EQ stand-down) -- and so inflated agreement toward a false 1M-gate license (the
    # same shape as FINDING 1H-CRITICAL, minus the Pine agreeRate anchor). The valid
    # mask excludes warmup 0==0 rows so EQ-inclusion does not inflate the other way.
    agree, n_agree = _sign_agreement(hz, mz, restrict_nonzero=False, mask=vm)
    # rate gap: 1H native premRate vs the rate computed on the 1M-basis zone joined to
    # the same forward 1H returns. We re-derive hits on the joined minute-zone using
    # the 1H close path (the 1H follow-through window is the measurement horizon).
    p_h, d_h, sc_h = recompute_hits(ex.zone, ex.c, FWDK)
    pv_h, dv_h, pidx_h, didx_h = _zone_hit_vectors(ex.zone, p_h, d_h, sc_h)
    prem_h = stride_rate_ci(pv_h, pidx_h)["rate"]
    disc_h = stride_rate_ci(dv_h, didx_h)["rate"]
    # build a full-length minute-zone aligned to the 1H bars (0 where no join)
    m_map = {int(t): z for t, z in zip(mn.epoch_ms, mn.zone)}
    mzone_full = np.array([m_map.get(int(t), 0.0) for t in ex.epoch_ms], float)
    p_m, d_m, sc_m = recompute_hits(mzone_full, ex.c, FWDK)
    pv_m, dv_m, pidx_m, didx_m = _zone_hit_vectors(mzone_full, p_m, d_m, sc_m)
    prem_m = stride_rate_ci(pv_m, pidx_m)["rate"]
    disc_m = stride_rate_ci(dv_m, didx_m)["rate"]
    gaps = [abs(a - b) for a, b in ((prem_h, prem_m), (disc_h, disc_m))
            if not (np.isnan(a) or np.isnan(b))]
    gap = max(gaps) if gaps else np.nan
    clears = (not np.isnan(agree)) and agree >= TRANSFER_AGREE_MIN and \
             (not np.isnan(gap)) and gap <= TRANSFER_GAP_MAX_PP
    return {"axis": "price_basis", "agree": agree, "n_agree": n_agree, "gap": gap,
            "prem_1h": prem_h, "prem_1m": prem_m, "disc_1h": disc_h, "disc_1m": disc_m,
            "clears": bool(clears)}


def transfer_pregate(ex: HourExport, mn: MinuteExport | None):
    """Both axes (PREREG-1H). Pre-condition: lookN==1M pdLookN AND eqBand==1M eqBand
    (held by frozen-config; we assert the 1H locks here). REJECT if EITHER axis fails.

    If the paired 1M export is absent, the price-BASIS axis is UNAVAILABLE and the
    transfer CANNOT clear (it requires both axes) -> licenses nothing; the harness
    reports which export is missing."""
    a = transfer_range_lag_axis(ex)
    if mn is None:
        return {"range_lag": a, "price_basis": None, "clears": False,
                "reason": "1M export absent -> price-BASIS axis not computable; "
                          "transfer requires BOTH axes"}
    b = transfer_price_basis_axis(ex, mn)
    clears = bool(a["clears"]) and bool(b["clears"])
    return {"range_lag": a, "price_basis": b, "clears": clears,
            "reason": "" if clears else "transfer REJECT: <90% agreement or >3pp gap "
                                        "on at least one axis"}


# =============================================================================
# BIAS-CONDITIONED VARIANT (PREREG-1H 1H-E3; GENUINE CHOICE 7)
# =============================================================================
def _week_key_et(epoch_ms):
    """ET ISO-week key (year, week) for each UTC epoch-ms bar (DST-aware via ET).
    Used to join the WEEKLY structBias to each 1H bar."""
    t = pd.to_datetime(np.asarray(epoch_ms), unit="ms", utc=True).tz_convert(M.ET)
    iso = t.isocalendar()
    return list(zip(iso.year.to_numpy(), iso.week.to_numpy()))


def bias_conditioned_rates(ex: HourExport, weekly_bias):
    """Split each rate by the sign of the WEEKLY structBias joined by timestamp
    (PREREG-1H 1H-E3). `weekly_bias` is a dict {(iso_year, iso_week): +1/-1} OR a
    (epoch_ms_array, bias_array) tuple of weekly anchors that we bucket into ET weeks.

    Returns nested dict: {'prem': {+1: rate, -1: rate}, 'disc': {+1:..,-1:..}} on the
    de-overlapped (stride) basis. The 1M trades structBias AND PD (never PD alone), so
    the gate-relevant conditional is premHit|bias and discHit|bias."""
    if isinstance(weekly_bias, tuple):
        wb_epoch, wb_val = weekly_bias
        wk_map = {}
        for k, v in zip(_week_key_et(wb_epoch), np.asarray(wb_val, float)):
            wk_map[k] = int(np.sign(v)) if v != 0 else 0
    else:
        wk_map = dict(weekly_bias)
    bar_weeks = _week_key_et(ex.epoch_ms)
    bias_per_bar = np.array([wk_map.get(w, 0) for w in bar_weeks], float)
    prem, disc, sc = recompute_hits(ex.zone, ex.c, FWDK)
    out = {"prem": {}, "disc": {}}
    for sign in (1, -1):
        bmask = bias_per_bar == sign
        # premium zone under this bias
        pmask = sc & (ex.zone == 1) & bmask
        pidx = np.where(pmask)[0]
        pv = prem[pidx].astype(float)
        out["prem"][sign] = stride_rate_ci(pv, pidx)["rate"] if len(pv) else np.nan
        dmask = sc & (ex.zone == -1) & bmask
        didx = np.where(dmask)[0]
        dv = disc[didx].astype(float)
        out["disc"][sign] = stride_rate_ci(dv, didx)["rate"] if len(dv) else np.nan
    return out


# =============================================================================
# HALVES STATIONARITY (PREREG-1H GENUINE CHOICE 8 superset)
# =============================================================================
def halves_margin_flip(hit_vec, bar_idx):
    """PREREG-1H GENUINE CHOICE 8: does the rate's >0.5 margin flip sign across the
    two chronological halves (one half <= 0.5)? Returns dict with each half rate and
    a `flips` flag. Split is by the median bar index (chronological)."""
    hit_vec = np.asarray(hit_vec, float)
    bar_idx = np.asarray(bar_idx)
    if len(hit_vec) < 4:
        return {"h1": np.nan, "h2": np.nan, "flips": False, "n1": 0, "n2": 0}
    order = np.argsort(bar_idx)
    hv = hit_vec[order]
    mid = len(hv) // 2
    h1 = float(hv[:mid].mean())
    h2 = float(hv[mid:].mean())
    flips = (h1 <= 0.5) or (h2 <= 0.5)
    return {"h1": h1, "h2": h2, "flips": bool(flips), "n1": mid, "n2": len(hv) - mid}


# =============================================================================
# VERDICT (PREREG-1H sec 6 verdict gate)
# =============================================================================
def verdict_1h(ex: HourExport, mn: MinuteExport | None = None, weekly_bias=None,
               apply_halves_superset=True):
    """Run the full PREREG-1H sec 6 verdict + cascade-licensing decision.

    Returns a dict with every sub-result and the final `verdict` in
    {RESOLVED, FALSIFIED, AMBIGUOUS-HOLD, INSUFFICIENT-N} plus `licenses_1m_gate`.

    sec 6 RESOLVED requires ALL of:
      - a rate's de-overlapped CI clears 0.5 by >=2pp under BOTH stride AND block
      - the real rate BEATS the placebo floor (1H-E5)
      - the winning anchor cell clears 0.5 by >=2pp AFTER the 9-cell penalty (1H-E4)
      - the transfer pre-gate clears (both axes; 1H-E1)
      - effective-N >= 30 in the scored zone
    FALSIFIED: BOTH prem AND disc de-overlapped CIs straddle 0.5 after penalty.
    AMBIGUOUS-HOLD: clears unconditional gate but fails bias-conditioned (1H-E3) OR
      (superset) the margin flips across halves.
    INSUFFICIENT-N: effective-N < 30 per zone after stride de-overlap (both zones).
    """
    out = {}
    # 0) look-ahead audit -- discard exported hit columns if they disagree
    audit = audit_exported_hits(ex)
    out["hit_audit"] = audit
    # use the RECOMPUTED hits as the verdict basis (look-ahead-free, polarity-checked)
    prem, disc, sc = recompute_hits(ex.zone, ex.c, FWDK)
    pv, dv, pidx, didx = _zone_hit_vectors(ex.zone, prem, disc, sc)

    # 1) effective-N / n-floor
    neff_prem = effective_n(ex.zone, sc, 1)
    neff_disc = effective_n(ex.zone, sc, -1)
    out["n_eff"] = {"prem": neff_prem, "disc": neff_disc, "floor": N_FLOOR}
    prem_ok_n = neff_prem >= N_FLOOR
    disc_ok_n = neff_disc >= N_FLOOR
    if not prem_ok_n and not disc_ok_n:
        out["verdict"] = "INSUFFICIENT-N"
        out["licenses_1m_gate"] = False
        out["reason"] = (f"effective-N < {N_FLOOR} in BOTH zones after stride "
                         f"de-overlap (prem={neff_prem}, disc={neff_disc}); "
                         f"re-spec export window (longer/multi-regime)")
        return out

    # 2) de-overlap CI (stride + block) per zone
    out["prem"] = {"stride": stride_rate_ci(pv, pidx), "block": block_rate_ci(pv)}
    out["disc"] = {"stride": stride_rate_ci(dv, didx), "block": block_rate_ci(dv)}

    def both_clear(z):
        return bool(z["stride"]["clears"]) and bool(z["block"]["clears"])

    prem_both = prem_ok_n and both_clear(out["prem"])
    disc_both = disc_ok_n and both_clear(out["disc"])

    # 3) placebo floor (real must beat) -- only meaningful for the candidate zone(s)
    out["placebo"] = {"prem": placebo_floor(ex.zone, ex.c, prem, disc, sc, "prem"),
                      "disc": placebo_floor(ex.zone, ex.c, prem, disc, sc, "disc")}
    prem_beats = prem_both and (out["prem"]["stride"]["rate"] >
                                out["placebo"]["prem"]["floor"])
    disc_beats = disc_both and (out["disc"]["stride"]["rate"] >
                                out["placebo"]["disc"]["floor"])

    # 4) anchor sweep + penalty (per candidate zone)
    out["sweep"] = {}
    out["penalty"] = {}
    for which, cand in (("prem", prem_beats), ("disc", disc_beats)):
        cells = anchor_sweep(ex, which)
        out["sweep"][which] = cells
        out["penalty"][which] = deflated_max_stat_penalty(cells)
    prem_penalty = out["penalty"]["prem"]["pass_dsr"]
    disc_penalty = out["penalty"]["disc"]["pass_dsr"]

    # 5) transfer pre-gate (both axes; licenses-nothing on REJECT)
    out["transfer"] = transfer_pregate(ex, mn)
    transfer_ok = bool(out["transfer"]["clears"])

    # candidate-zone unconditional PASS (all sec 6 RESOLVED conditions except transfer)
    prem_uncond = prem_beats and prem_penalty
    disc_uncond = disc_beats and disc_penalty
    any_uncond = prem_uncond or disc_uncond

    # FALSIFIED: both prem AND disc straddle 0.5 (stride CI does not clear) after penalty
    prem_straddle = not (out["prem"]["stride"]["clears"] and prem_penalty)
    disc_straddle = not (out["disc"]["stride"]["clears"] and disc_penalty)
    if prem_straddle and disc_straddle:
        out["verdict"] = "FALSIFIED"
        out["licenses_1m_gate"] = False
        out["reason"] = ("both premium-down AND discount-up de-overlapped rate CIs "
                         "straddle 0.5 after the 9-cell penalty -- the split is decorative")
        return out

    # bias-conditioned variant (1H-E3) -- gate-relevant conditional
    bias_fail = False
    if weekly_bias is not None:
        out["bias_conditioned"] = bias_conditioned_rates(ex, weekly_bias)
        # gate-relevant: premHit under bias=+1 should still clear, discHit under
        # bias=-1 should still clear (trend-continuation under the traded bias). If the
        # unconditional clears but the matched bias-conditioned rate <= 0.5, fail.
        bc = out["bias_conditioned"]
        if prem_uncond and not (bc["prem"].get(1, np.nan) > 0.5):
            bias_fail = True
        if disc_uncond and not (bc["disc"].get(-1, np.nan) > 0.5):
            bias_fail = True
    else:
        out["bias_conditioned"] = None
        # PREREG-1H requires the bias-conditioned variant for RESOLVED; without the
        # weekly bias series it cannot be evaluated -> cannot RESOLVE (AMBIGUOUS-HOLD).
        bias_fail = any_uncond  # only matters if something cleared unconditionally

    # halves superset (GENUINE CHOICE 8) -- only if operator-ratified
    halves_flip = False
    if apply_halves_superset:
        out["halves"] = {"prem": halves_margin_flip(pv, pidx),
                         "disc": halves_margin_flip(dv, didx)}
        if prem_uncond and out["halves"]["prem"]["flips"]:
            halves_flip = True
        if disc_uncond and out["halves"]["disc"]["flips"]:
            halves_flip = True
    else:
        out["halves"] = None

    # ---- final disposition ----
    if any_uncond and transfer_ok and not bias_fail and not halves_flip:
        out["verdict"] = "RESOLVED"
        out["licenses_1m_gate"] = True
        out["reason"] = ("a rate clears 0.5 by >=2pp under BOTH estimators, beats the "
                         "placebo, survives the 9-cell penalty, AND the transfer "
                         "pre-gate clears on both axes")
        return out

    if any_uncond and (bias_fail or halves_flip):
        out["verdict"] = "AMBIGUOUS-HOLD"
        out["licenses_1m_gate"] = False
        reasons = []
        if bias_fail:
            reasons.append("fails the bias-conditioned (gate-relevant) variant 1H-E3"
                           if weekly_bias is not None else
                           "weekly structBias series not supplied -> bias-conditioned "
                           "variant uncomputable (required for RESOLVED)")
        if halves_flip:
            reasons.append("the >0.5 margin flips sign across chronological halves "
                           "(one-regime; GENUINE CHOICE 8 superset)")
        out["reason"] = "; ".join(reasons) + " -> HOLD, no 1M PD-gate licensing"
        return out

    if any_uncond and not transfer_ok:
        # unconditional gate clears but transfer REJECTs -> RESOLVED-but-licenses-nothing.
        # PREREG-1H: a 1H PASS on the [0]-fresh/1H-close basis while the gate basis
        # disagrees licenses NOTHING; route to the full 1M end-to-end run.
        out["verdict"] = "RESOLVED"
        out["licenses_1m_gate"] = False
        out["reason"] = ("unconditional + placebo + penalty + bias/halves all clear, "
                         "but the TRANSFER pre-gate REJECTS (cascade-licensing rule): "
                         "this 1H PASS licenses NOTHING about the 1M PD gate -- the only "
                         "valid evidence becomes the full 1M end-to-end run")
        return out

    # nothing cleared unconditionally but not both fully straddle (e.g. one zone n-ok
    # but rate just under threshold) -> AMBIGUOUS-HOLD (not a clean falsification)
    out["verdict"] = "AMBIGUOUS-HOLD"
    out["licenses_1m_gate"] = False
    out["reason"] = ("no zone clears the full unconditional gate (CI/placebo/penalty) "
                     "and not both zones cleanly straddle -> hold; name the re-test "
                     "object/window")
    return out


# =============================================================================
# REPORTING
# =============================================================================
def _fmt_rate(x):
    return "  nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.4f}"


def print_report(res):
    print("=" * 72)
    print("Q-ICT-CASCADE-1 / LAYER 1H -- PREREG-1H verdict")
    print("=" * 72)
    a = res.get("hit_audit", {})
    print(f"[0] hit-column look-ahead audit: ok={a.get('ok')} "
          f"prem_mismatch={_fmt_rate(a.get('prem_mismatch'))} "
          f"disc_mismatch={_fmt_rate(a.get('disc_mismatch'))}")
    ne = res.get("n_eff", {})
    print(f"[1] effective-N (floor {ne.get('floor')}): "
          f"prem={ne.get('prem')} disc={ne.get('disc')}")
    if res["verdict"] == "INSUFFICIENT-N":
        print(f"\nVERDICT: {res['verdict']}\n  {res['reason']}")
        return
    for z in ("prem", "disc"):
        st = res[z]["stride"]
        bl = res[z]["block"]
        pl = res["placebo"][z]
        pen = res["penalty"][z]
        print(f"[2/3/4] {z}: stride rate={_fmt_rate(st['rate'])} "
              f"CI=[{_fmt_rate(st['ci_lo'])},{_fmt_rate(st['ci_hi'])}] "
              f"clears={st['clears']} (n_eff={st['n_eff']})")
        print(f"         block  rate={_fmt_rate(bl['rate'])} "
              f"CI=[{_fmt_rate(bl['ci_lo'])},{_fmt_rate(bl['ci_hi'])}] "
              f"clears={bl['clears']}")
        print(f"         placebo floor={_fmt_rate(pl['floor'])} "
              f"(random_eq={_fmt_rate(pl['random_eq'])} "
              f"sign_shuffle={_fmt_rate(pl['sign_shuffle'])})")
        w = pen.get("winner")
        if w:
            print(f"         penalty: winner lookN={w['look_n']} eqBand={w['eq_band']} "
                  f"rate={_fmt_rate(w['rate'])} n_eff={w['n_eff']} "
                  f"e_max={_fmt_rate(pen.get('e_max'))} "
                  f"pass_dsr={pen.get('pass_dsr')} pass_bonf={pen.get('pass_bonf')}")
    tr = res["transfer"]
    rl = tr["range_lag"]
    print(f"[5] transfer range-LAG: agree={_fmt_rate(rl['agree'])} "
          f"(n={rl['n_agree']}) gap={_fmt_rate(rl['gap'])} clears={rl['clears']}")
    pb = tr["price_basis"]
    if pb is None:
        print(f"    transfer price-BASIS: UNAVAILABLE ({tr.get('reason')})")
    else:
        print(f"    transfer price-BASIS: agree={_fmt_rate(pb['agree'])} "
              f"(n={pb['n_agree']}) gap={_fmt_rate(pb['gap'])} clears={pb['clears']}")
    print(f"    transfer pre-gate clears (BOTH axes): {tr['clears']}")
    bc = res.get("bias_conditioned")
    if bc:
        print(f"[E3] bias-conditioned: prem|+1={_fmt_rate(bc['prem'].get(1))} "
              f"prem|-1={_fmt_rate(bc['prem'].get(-1))} "
              f"disc|+1={_fmt_rate(bc['disc'].get(1))} "
              f"disc|-1={_fmt_rate(bc['disc'].get(-1))}")
    hv = res.get("halves")
    if hv:
        print(f"[E8] halves: prem h1={_fmt_rate(hv['prem']['h1'])} "
              f"h2={_fmt_rate(hv['prem']['h2'])} flips={hv['prem']['flips']} | "
              f"disc h1={_fmt_rate(hv['disc']['h1'])} "
              f"h2={_fmt_rate(hv['disc']['h2'])} flips={hv['disc']['flips']}")
    print("-" * 72)
    print(f"VERDICT: {res['verdict']}")
    print(f"LICENSES 1M PD GATE: {res['licenses_1m_gate']}")
    print(f"  {res['reason']}")
    print("=" * 72)


# =============================================================================
# MAIN -- skip cleanly when the real export(s) are absent
# =============================================================================
DEFAULT_HOUR_CSV = "ict_1h_premium_discount_export.csv"
DEFAULT_MIN_CSV = "ict_1m_execution_export.csv"
DEFAULT_BIAS_CSV = "ict_weekly_structbias_export.csv"


def main(hour_csv=None, min_csv=None, bias_csv=None):
    here = Path(__file__).resolve().parent
    hour_csv = Path(hour_csv) if hour_csv else here / DEFAULT_HOUR_CSV
    min_csv = Path(min_csv) if min_csv else here / DEFAULT_MIN_CSV
    bias_csv = Path(bias_csv) if bias_csv else here / DEFAULT_BIAS_CSV

    if not hour_csv.exists():
        print("[SKIP] 1H export not found -- the operator has not run TV yet.")
        print(f"       expected 1H export at: {hour_csv}")
        print("       REQUIRED EXPORTS (PREREG-1H CONSUMES):")
        print("       1) 1H indicator export (ict_1h_premium_discount_DRAFT.pine):")
        print("          cols = time, open, high, low, close, zone, eq, premHit,")
        print("                 discHit, zoneGate, zoneAgree")
        print("       2) paired 1M export (ict_1m_execution.pine) for the price-BASIS")
        print("          transfer axis: cols = time, netBias, zone, inKZ, close")
        print("       3) (optional) weekly structBias export for the bias-conditioned")
        print("          variant (1H-E3): cols = time, structBias")
        print("       Re-run: python lab/analysis/ict_cascade_2026-06-18/harness_1h.py")
        return None

    ex = load_hour_export(hour_csv)
    mn = load_minute_export(min_csv) if min_csv.exists() else None
    if mn is None:
        print(f"[WARN] 1M export not found at {min_csv} -- the price-BASIS transfer "
              "axis cannot be computed; the transfer pre-gate will REJECT (it requires "
              "BOTH axes) and the 1H verdict licenses NOTHING about the 1M gate.")

    weekly_bias = None
    if bias_csv.exists():
        bdf = pd.read_csv(bias_csv)
        bcols = {c.lower(): c for c in bdf.columns}
        if "time" in bcols and "structbias" in bcols:
            wb_epoch = _to_epoch_ms(bdf[bcols["time"]])
            wb_val = bdf[bcols["structbias"]].to_numpy(float)
            weekly_bias = (wb_epoch, wb_val)
    else:
        print(f"[WARN] weekly structBias export not found at {bias_csv} -- the "
              "bias-conditioned variant (1H-E3) cannot be evaluated; a unconditional "
              "PASS routes to AMBIGUOUS-HOLD (bias-conditioned is required for RESOLVED).")

    res = verdict_1h(ex, mn, weekly_bias)
    print_report(res)
    return res


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Q-ICT-CASCADE-1 Layer 1H harness (PREREG-1H)")
    ap.add_argument("--hour-csv", default=None)
    ap.add_argument("--min-csv", default=None)
    ap.add_argument("--bias-csv", default=None)
    args = ap.parse_args()
    main(args.hour_csv, args.min_csv, args.bias_csv)
