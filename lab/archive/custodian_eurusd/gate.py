#!/usr/bin/env python3
"""Custodian-EURUSD v0.1 — month-end equity-hedging-flow mechanism falsifier.

Tests the concept's OWN pre-registered falsifier (brief
CC-HANDOFF-custodian-eurusd-v0.1-mechanism-probe, §4). Mechanism probe ONLY — no
strategy/Pine is built, no primitive library is extended (brief §5).

The Melvin-Prins equity-hedging channel claims: when US equities outperform
Eurozone equities over the concluding month, benchmark-tracking managers become
under-hedged in USD and must SELL USD / BUY EUR into the last London 4 p.m.
WM/Reuters fix of the period -> EURUSD UP. So the prior-period relative (US-EZ)
equity return ``x`` should POSITIVELY predict the last-trading-day pre-fix EURUSD
return ``y``.

PRE-REGISTERED PRIMARY (brief §0.5, RATIFIED by Joshua 2026-06-09, frozen pre-data):
  y (primary): close[16:00 London] / open[12:00 London] - 1   on the last trading
               day of the month (London afternoon into the WM/R fix). 16:00
               Europe/London, DST-aware.
  x (primary): concluding month M local-currency relative return THROUGH T-1
               (penultimate trading day):
                  [SPX(T-1)/SPX(prev-month-end) - 1]
                - [ESTX50(T-1)/ESTX50(prev-month-end) - 1]
               window ending STRICTLY BEFORE the day-T y window (no look-ahead).
               "prior calendar-month" = concluding-month-through-T-1 (confirmed).

H-CUSTODIAN (§4): OLS y ~ const + x with HC3-robust SE yields beta > 0,
two-sided p < 0.05, n >= 90 months.
  RESOLVED      iff beta > 0 AND p < 0.05 AND n >= 90.
  FALSIFIED     iff p >= 0.05 OR beta <= 0  (a significant NEGATIVE beta is
                FALSIFIED, not a pass — the load-bearing sign-discipline point).
  AMBIGUOUS-HOLD iff right sign but 0.05 <= p < 0.10, OR n < 90 from data gaps.

ROBUSTNESS (reported, NOT a pass route — brief §5 #1):
  y-window {15:00->16:00, 08:00->16:00};  x {FX-adjusted ESTX50-in-USD, single-leg US-only}.

STAGE 2 (ADVISORY ONLY — brief §2.4, must NOT move the kill verdict): single
monthly sign-following trade into the fix, net of swept round-trip spread
{0,1,2,3,5} bps + a once-per-period overnight-hold swap. Informs codification
go/no-go, never the FALSIFIED criterion.

Causal-lag (load-bearing, brief §5 #3): x is built from index closes up to and
including T-1; y is the day-T 12:00->16:00 London window. x's last observation
(T-1 close) is strictly before y's first bar (day-T 12:00 London), so there is no
same-day/look-ahead leakage. Enforced in build_monthly_frame + asserted +
spot-checked in the DST/lag table.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import statsmodels.api as sm
    _HAVE_SM = True
except Exception:  # pragma: no cover
    _HAVE_SM = False

from scipy import stats as _sps

# ---- pre-registered constants ----
SAMPLE_START = pd.Timestamp("2016-01-01")
N_FLOOR = 90
P_RESOLVE = 0.05
P_AMBIG = 0.10
SPREAD_SWEEP_BPS = [0, 1, 2, 3, 5]
# Once-per-period overnight-hold swap on EURUSD. FXIFY swap table
# (docs/external/fxify_swap_rates_2026-05-25.md) covers XAUUSD/USDJPY/DJ30/NAS100,
# NOT EURUSD majors, so no in-repo EURUSD swap rate exists. The hold is a single
# overnight (enter into the 16:00 fix, exit next session), so one swap event. A
# representative EURUSD long-swap drag of ~0.5 bps/night is applied as a flat,
# DIRECTION-INDEPENDENT cost on the |position| (advisory only). Reported
# explicitly so the assumption is auditable; it cannot manufacture or destroy the
# Stage-1 regression result (Stage 2 is advisory, brief §2.4).
SWAP_BPS_PER_NIGHT = 0.5

# London wall-clock windows (m15 bars stamped at bar-OPEN). The fix CLOSE at
# HH:00 = close of the HH-15min bar (the bar whose 15-min span ends at HH:00),
# exactly as noct used close[05:15] for the 05:30 exit. So a "12:00 open ->
# 16:00 fix close" window is (open_bar='12:00', close_bar='15:45'); the close-bar
# tag is the target close time minus one m15 bar.
Y_PRIMARY = ("12:00", "15:45")        # open[12:00] -> close[15:45 bar] = 16:00 London fix print
Y_ROBUST = {"15to16": ("15:00", "15:45"), "08to16": ("08:00", "15:45")}


# ---------------------------------------------------------------------------
# Bar loading -> London wall-clock map + daily closes
# ---------------------------------------------------------------------------
def load_bars_london(path: Path) -> pd.DataFrame:
    """Load an m15 OHLCV CSV; add a DST-aware Europe/London wall-clock + date."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    ts_utc = pd.to_datetime(df["time"], utc=True, format="ISO8601")
    ldn = ts_utc.dt.tz_convert("Europe/London")
    out = pd.DataFrame({
        "utc": ts_utc.dt.tz_localize(None).values,
        "ldn": ldn.dt.tz_localize(None).values,
        "open": df["open"].astype(float).values,
        "high": df["high"].astype(float).values,
        "low": df["low"].astype(float).values,
        "close": df["close"].astype(float).values,
    })
    out["ldn_date"] = out["ldn"].dt.normalize()
    out["ldn_hm"] = pd.Series(out["ldn"]).dt.strftime("%H:%M")
    return out


def daily_close_series(bars: pd.DataFrame) -> pd.Series:
    """Per London-date close = close of the last bar on that date (index = date)."""
    g = bars.sort_values("ldn").groupby("ldn_date")
    s = g["close"].last()
    s.index = pd.DatetimeIndex(s.index)
    return s.sort_index()


def window_return(bars_by_date: dict, date: pd.Timestamp, open_hm: str, close_hm: str):
    """(close[close_hm] - open[open_hm]) / open[open_hm] for `date`'s London bars."""
    day = bars_by_date.get(pd.Timestamp(date))
    if day is None:
        return np.nan
    o = day["open"].get(open_hm)
    c = day["close"].get(close_hm)
    if o is None or c is None or not (o > 0):
        return np.nan
    return c / o - 1.0


def _bars_by_date(bars: pd.DataFrame) -> dict:
    """date -> {'open': {hm: open}, 'close': {hm: close}} for fast window lookup."""
    out: dict = {}
    for d, sub in bars.groupby("ldn_date"):
        out[pd.Timestamp(d)] = {
            "open": dict(zip(sub["ldn_hm"], sub["open"])),
            "close": dict(zip(sub["ldn_hm"], sub["close"])),
        }
    return out


# ---------------------------------------------------------------------------
# Monthly trading calendar (T = last trading day, T-1 = penultimate)
# ---------------------------------------------------------------------------
def month_last_two_trading_days(trading_dates: pd.DatetimeIndex):
    """For each calendar month present, return (T, T-1) trading dates.

    Uses the REAL trading calendar derived from EURUSD bar dates (the instrument
    whose y is measured), not a synthetic business-day grid.
    """
    df = pd.DataFrame({"d": trading_dates})
    df["ym"] = df["d"].dt.to_period("M")
    rows = []
    for ym, sub in df.groupby("ym"):
        ds = sub["d"].sort_values().to_list()
        if len(ds) >= 2:
            rows.append((ym, ds[-1], ds[-2]))   # T, T-1
        elif len(ds) == 1:
            rows.append((ym, ds[-1], None))
    return rows


# ---------------------------------------------------------------------------
# Build the per-month analysis frame (x, y) with the causal lag enforced
# ---------------------------------------------------------------------------
def build_monthly_frame(eur_bars, spx_close, estx_close,
                        y_window=Y_PRIMARY) -> pd.DataFrame:
    """Return a tidy per-month frame with x (primary), y (primary + robustness),
    and the columns needed for the lag spot-check.

    eur_bars: EURUSD m15 bars (London wall-clock) — the y instrument + trading cal.
    spx_close / estx_close: per-London-date daily close Series (the x legs).
    """
    eur_by_date = _bars_by_date(eur_bars)
    trading_dates = pd.DatetimeIndex(sorted(eur_bars["ldn_date"].unique()))
    trading_dates = trading_dates[trading_dates >= SAMPLE_START]
    months = month_last_two_trading_days(trading_dates)

    def asof_close(series: pd.Series, date) -> float:
        """Most recent close on or before `date` (handles index-vs-EUR-cal drift)."""
        if date is None:
            return np.nan
        idx = series.index
        pos = idx.searchsorted(pd.Timestamp(date), side="right") - 1
        if pos < 0:
            return np.nan
        return float(series.iloc[pos])

    # Map each month -> prior month's T (its month-end), for the x baseline.
    month_T = {ym: T for (ym, T, _Tm1) in months}

    rows = []
    prev_ym = None
    for (ym, T, Tm1) in months:
        prev_period = ym - 1
        prev_T = month_T.get(prev_period)   # prior month's last trading day
        if T is None or Tm1 is None or prev_T is None:
            prev_ym = ym
            continue

        # ---- x legs (local currency), through T-1, baselined at prev month-end ----
        spx_prev = asof_close(spx_close, prev_T)
        spx_tm1 = asof_close(spx_close, Tm1)
        estx_prev = asof_close(estx_close, prev_T)
        estx_tm1 = asof_close(estx_close, Tm1)

        if not all(np.isfinite([spx_prev, spx_tm1, estx_prev, estx_tm1])) \
                or spx_prev <= 0 or estx_prev <= 0:
            prev_ym = ym
            continue

        r_us = spx_tm1 / spx_prev - 1.0
        r_ez = estx_tm1 / estx_prev - 1.0
        x_primary = r_us - r_ez                # relative, local currency
        x_us_only = r_us                       # single-leg robustness

        # ---- y windows on day T (London) ----
        y_prim = window_return(eur_by_date, T, *y_window)
        y_15to16 = window_return(eur_by_date, T, *Y_ROBUST["15to16"])
        y_08to16 = window_return(eur_by_date, T, *Y_ROBUST["08to16"])

        # ---- causal-lag witnesses (for assertion + spot-check) ----
        # x's last observation is the T-1 close (end of day Tm1). y's first bar is
        # the day-T 12:00 London open. Strictly Tm1 < T => no overlap.
        rows.append({
            "ym": str(ym), "T": pd.Timestamp(T), "Tm1": pd.Timestamp(Tm1),
            "prev_T": pd.Timestamp(prev_T),
            "spx_prev": spx_prev, "spx_tm1": spx_tm1,
            "estx_prev": estx_prev, "estx_tm1": estx_tm1,
            "r_us": r_us, "r_ez": r_ez,
            "x": x_primary, "x_us_only": x_us_only,
            "y": y_prim, "y_15to16": y_15to16, "y_08to16": y_08to16,
        })
        prev_ym = ym

    frame = pd.DataFrame(rows)
    # Look-ahead guard: every x observation (T-1) strictly precedes its y day (T).
    if len(frame):
        assert bool((frame["Tm1"] < frame["T"]).all()), \
            "LOOK-AHEAD: an x window (T-1) is not strictly before its y day (T)."
    return frame


def add_fx_adjusted_x(frame: pd.DataFrame, eurusd_close: pd.Series) -> pd.DataFrame:
    """Robustness x: ESTX50 leg converted to USD (multiply EUR level by EURUSD) so
    both legs are in USD. Reported only — NOT a pass route (brief §5 #1)."""
    def asof(series, date):
        idx = series.index
        pos = idx.searchsorted(pd.Timestamp(date), side="right") - 1
        return float(series.iloc[pos]) if pos >= 0 else np.nan
    out = frame.copy()
    fx_prev = out["prev_T"].map(lambda d: asof(eurusd_close, d))
    fx_tm1 = out["Tm1"].map(lambda d: asof(eurusd_close, d))
    estx_prev_usd = out["estx_prev"] * fx_prev
    estx_tm1_usd = out["estx_tm1"] * fx_tm1
    r_ez_usd = estx_tm1_usd / estx_prev_usd - 1.0
    out["x_fxadj"] = out["r_us"] - r_ez_usd
    return out


# ---------------------------------------------------------------------------
# Regression (HC3-robust OLS), with a manual HC3 fallback
# ---------------------------------------------------------------------------
def hc3_ols(y: np.ndarray, x: np.ndarray) -> dict:
    """OLS y ~ const + x with HC3 heteroskedasticity-robust SE on the slope.

    Uses statsmodels when available; otherwise a hand-rolled HC3 (sandwich with
    leverage-corrected residuals h_ii) so the gate runs on a public clone too.
    """
    mask = np.isfinite(y) & np.isfinite(x)
    y = y[mask].astype(float)
    x = x[mask].astype(float)
    n = len(y)
    out = {"n": int(n)}
    if n < 3:
        out.update({"beta": float("nan"), "t": float("nan"), "p": float("nan"),
                    "r2": float("nan"), "engine": "none", "alpha": float("nan")})
        return out

    if _HAVE_SM:
        X = sm.add_constant(x)
        res = sm.OLS(y, X).fit(cov_type="HC3")
        out.update({
            "alpha": float(res.params[0]), "beta": float(res.params[1]),
            "t": float(res.tvalues[1]), "p": float(res.pvalues[1]),
            "r2": float(res.rsquared), "engine": "statsmodels-HC3",
        })
        return out

    # Manual HC3 fallback ------------------------------------------------------
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta_hat = XtX_inv @ X.T @ y
    resid = y - X @ beta_hat
    H = X @ XtX_inv @ X.T
    h = np.clip(np.diag(H), 0, 0.999999)
    omega = (resid / (1.0 - h)) ** 2          # HC3 weighting
    bread = XtX_inv @ (X.T * omega) @ X @ XtX_inv
    se_beta = math.sqrt(bread[1, 1])
    t = beta_hat[1] / se_beta if se_beta > 0 else float("nan")
    df = n - 2
    p = float(2 * _sps.t.sf(abs(t), df)) if np.isfinite(t) else float("nan")
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    out.update({"alpha": float(beta_hat[0]), "beta": float(beta_hat[1]),
                "t": float(t), "p": p, "r2": r2, "engine": "manual-HC3"})
    return out


def verdict_from(reg: dict) -> str:
    """Apply the §4 / §6 KILL criterion to a primary regression result."""
    beta, p, n = reg["beta"], reg["p"], reg["n"]
    if not np.isfinite(beta) or not np.isfinite(p):
        return "AMBIGUOUS-HOLD"
    if beta > 0 and p < P_RESOLVE and n >= N_FLOOR:
        return "RESOLVED"
    if beta > 0 and P_RESOLVE <= p < P_AMBIG:
        return "AMBIGUOUS-HOLD"
    if n < N_FLOOR and beta > 0:
        return "AMBIGUOUS-HOLD"
    return "FALSIFIED"


# ---------------------------------------------------------------------------
# Stage 2 — tradeability sanity (ADVISORY ONLY; does NOT move the verdict)
# ---------------------------------------------------------------------------
def stage2_sign_following(frame: pd.DataFrame, y_col="y") -> dict:
    """Single monthly sign-following trade into the fix: long EUR if x>0 else short.

    Net return per month = sign(x) * y  -  round_trip_spread  -  one-night swap.
    Reports net mean, annualized Sharpe (~12 trades/yr), breakeven spread.
    ADVISORY (brief §2.4): informs codification go/no-go, NOT the kill verdict.
    """
    sub = frame[["x", y_col]].dropna()
    x = sub["x"].to_numpy()
    y = sub[y_col].to_numpy()
    sgn = np.sign(x)
    gross = sgn * y
    n = len(gross)
    months_per_year = 12.0
    by_spread = {}
    for bps in SPREAD_SWEEP_BPS:
        cost = bps / 1e4 + SWAP_BPS_PER_NIGHT / 1e4    # round-trip spread + 1 swap
        net = gross - cost
        mean = float(np.mean(net)) if n else float("nan")
        sd = float(np.std(net, ddof=1)) if n > 1 else float("nan")
        sharpe_ann = (mean / sd) * math.sqrt(months_per_year) if sd and sd > 0 else float("nan")
        by_spread[bps] = {"mean": mean, "sd": sd, "sharpe_ann": sharpe_ann, "n": n}
    gross_mean_bps = float(np.mean(gross) * 1e4) if n else float("nan")
    breakeven_bps = gross_mean_bps - SWAP_BPS_PER_NIGHT   # spread at which net->0
    return {"n": n, "gross_mean_bps": gross_mean_bps,
            "breakeven_roundtrip_bps": breakeven_bps,
            "swap_bps_per_night": SWAP_BPS_PER_NIGHT, "by_spread": by_spread}


# ---------------------------------------------------------------------------
# DST spot-check (mandatory, mirrors noct)
# ---------------------------------------------------------------------------
def dst_spotcheck(eur_bars: pd.DataFrame) -> list[dict]:
    """Show the 16:00 London fix bar's UTC for a BST month, a GMT month, and a
    UK/US DST-mismatch week — confirming the fix is London-clock, DST-aware
    (15:00 UTC under BST, 16:00 UTC under GMT), not fixed-UTC (brief §0.5-4)."""
    by = eur_bars.set_index(["ldn_date", "ldn_hm"])  # for utc lookup of the 16:00 print
    # The 16:00 fix = close of the 15:45 London bar; show that bar's UTC stamp.
    utc_of = {}
    for (d, hm), row in by.iterrows():
        utc_of[(pd.Timestamp(d), hm)] = row["utc"]
    probes = [
        ("2022-06-30", "BST summer (UK on DST)"),
        ("2022-12-30", "GMT winter (UK off DST)"),
        ("2022-03-17", "US-EU mismatch (US EDT, UK still GMT)"),
        ("2023-03-17", "US-EU mismatch (US EDT, UK still GMT)"),
        ("2022-10-28", "US-EU mismatch (UK back to GMT, US still EDT)"),
    ]
    checks = []
    for ds, label in probes:
        d = pd.Timestamp(ds).normalize()
        # nearest available date <= ds with a 15:45 bar (month-end may be a weekend)
        cand = [k for k in utc_of if k[1] == "15:45" and k[0] <= d]
        if not cand:
            checks.append({"date": ds, "label": label, "note": "no 15:45 London bar near date"})
            continue
        kd = max(cand, key=lambda k: k[0])
        raw_utc = utc_of[kd]
        utc_ts = pd.Timestamp(raw_utc).tz_localize("UTC")
        ldn = utc_ts.tz_convert("Europe/London")
        checks.append({
            "probe_date": ds, "resolved_bar_date": str(kd[0].date()), "label": label,
            "fix_bar_open_ldn": ldn.strftime("%H:%M %Z"),
            "fix_close_approx_ldn": "16:00",
            "fix_bar_open_utc": utc_ts.strftime("%H:%M UTC"),
        })
    return checks


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def run(eur_path: Path, spx_path: Path, estx_path: Path, out_dir: Path) -> dict:
    eur_bars = load_bars_london(eur_path)
    spx_bars = load_bars_london(spx_path)
    estx_bars = load_bars_london(estx_path)

    spx_close = daily_close_series(spx_bars)
    estx_close = daily_close_series(estx_bars)
    eur_close = daily_close_series(eur_bars)

    frame = build_monthly_frame(eur_bars, spx_close, estx_close, y_window=Y_PRIMARY)
    frame = add_fx_adjusted_x(frame, eur_close)

    # ---- Stage 1: pre-registered PRIMARY regression (KILL criterion) ----
    reg_primary = hc3_ols(frame["y"].to_numpy(), frame["x"].to_numpy())
    verdict = verdict_from(reg_primary)

    # ---- Robustness (reported, NOT a pass route) ----
    robustness = {
        "y_15to16": hc3_ols(frame["y_15to16"].to_numpy(), frame["x"].to_numpy()),
        "y_08to16": hc3_ols(frame["y_08to16"].to_numpy(), frame["x"].to_numpy()),
        "x_fxadj": hc3_ols(frame["y"].to_numpy(), frame["x_fxadj"].to_numpy()),
        "x_us_only": hc3_ols(frame["y"].to_numpy(), frame["x_us_only"].to_numpy()),
    }

    # ---- Stage 2: advisory tradeability ----
    stage2 = stage2_sign_following(frame, y_col="y")

    dst = dst_spotcheck(eur_bars)

    usable = frame.dropna(subset=["x", "y"])
    result = {
        "data": {
            "eur_bars": int(len(eur_bars)), "spx_bars": int(len(spx_bars)),
            "estx_bars": int(len(estx_bars)),
            "eur_first": str(eur_bars["utc"].min()), "eur_last": str(eur_bars["utc"].max()),
            "estx_symbol": "EUSIDXEUR", "estx_point_factor": 1000.0,
            "months_total": int(len(frame)), "months_usable": int(len(usable)),
            "month_first": str(usable["ym"].min()) if len(usable) else None,
            "month_last": str(usable["ym"].max()) if len(usable) else None,
            "sample_start": str(SAMPLE_START.date()),
        },
        "primary": {"spec": {"y": "close[16:00 London]/open[12:00 London]-1 on last trading day",
                             "x": "[SPX(T-1)/SPX(prevME)-1] - [ESTX50(T-1)/ESTX50(prevME)-1] (local, through T-1)"},
                    "regression": reg_primary, "verdict": verdict,
                    "gate": {"n_floor": N_FLOOR, "p_resolve": P_RESOLVE, "p_ambig": P_AMBIG}},
        "robustness_NOT_a_pass_route": robustness,
        "stage2_ADVISORY": stage2,
        "dst_spotcheck": dst,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "gate_result.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    # also persist the per-month frame for audit
    frame.to_csv(out_dir / "monthly_frame.csv", index=False)
    return result


def _pct(x):
    return f"{x*100:.4f}%" if np.isfinite(x) else "nan"


def print_summary(r: dict):
    d = r["data"]
    p = r["primary"]["regression"]
    print("=" * 80)
    print("Custodian-EURUSD v0.1 — month-end equity-hedging-flow mechanism falsifier")
    print("=" * 80)
    print(f"EURUSD bars {d['eur_bars']}  SPX bars {d['spx_bars']}  "
          f"EUSIDXEUR bars {d['estx_bars']}")
    print(f"EURUSD span {d['eur_first']} -> {d['eur_last']}")
    print(f"months: total {d['months_total']}  usable(x&y) {d['months_usable']}  "
          f"[{d['month_first']} -> {d['month_last']}]")
    print()
    print("--- DST spot-check (16:00 London WM/R fix bar) ---")
    for c in r["dst_spotcheck"]:
        if "fix_bar_open_utc" in c:
            print(f"  {c['probe_date']} ({c['resolved_bar_date']}) {c['label']:<40} "
                  f"15:45 London bar = {c['fix_bar_open_utc']} -> fix close 16:00 London")
        else:
            print(f"  {c['probe_date']} {c['label']:<40} {c['note']}")
    print()
    print("--- STAGE 1: PRIMARY regression y ~ const + x  (KILL criterion) ---")
    print(f"  engine={p['engine']}  n={p['n']}")
    print(f"  beta = {p['beta']:+.5f}   t = {p['t']:+.3f}   p = {p['p']:.4f}   "
          f"R^2 = {p['r2']:.4f}   alpha = {p.get('alpha', float('nan')):+.6f}")
    print(f"  gate: beta>0 [{ 'Y' if p['beta']>0 else 'N'}]  "
          f"p<0.05 [{ 'Y' if p['p']<P_RESOLVE else 'N'}]  "
          f"n>=90 [{ 'Y' if p['n']>=N_FLOOR else 'N'}]")
    print(f"  >>> PROBE VERDICT: {r['primary']['verdict']} <<<")
    print()
    print("--- ROBUSTNESS (reported, NOT a pass route) ---")
    for k, rr in r["robustness_NOT_a_pass_route"].items():
        print(f"  {k:<10} beta={rr['beta']:+.5f}  t={rr['t']:+.3f}  p={rr['p']:.4f}  n={rr['n']}")
    print()
    print("--- STAGE 2 (ADVISORY ONLY — does NOT move the verdict) ---")
    s2 = r["stage2_ADVISORY"]
    print(f"  gross mean = {s2['gross_mean_bps']:+.3f} bps/month  "
          f"breakeven round-trip spread = {s2['breakeven_roundtrip_bps']:+.3f} bps "
          f"(after {s2['swap_bps_per_night']} bp swap)")
    print(f"  {'spread':>6} {'net mean(bps)':>14} {'Sharpe_ann':>11} {'n':>4}")
    for bps in SPREAD_SWEEP_BPS:
        e = s2["by_spread"][bps] if bps in s2["by_spread"] else s2["by_spread"][str(bps)]
        print(f"  {bps:>6} {e['mean']*1e4:>14.3f} {e['sharpe_ann']:>11.3f} {e['n']:>4}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Custodian-EURUSD mechanism falsifier")
    ap.add_argument("--eur", default="core/data/bar_data/EURUSD_M15.csv")
    ap.add_argument("--spx", default="core/data/bar_data/USA500IDXUSD_M15.csv")
    ap.add_argument("--estx", default="core/data/bar_data/EUSIDXEUR_M15.csv")
    ap.add_argument("--out", default="lab/analysis/custodian_eurusd")
    a = ap.parse_args(argv)
    r = run(Path(a.eur), Path(a.spx), Path(a.estx), Path(a.out))
    print_summary(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
