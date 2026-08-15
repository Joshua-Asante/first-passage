"""Build monthly HARV-0 panel from Databento ohlcv-1d continuous bars.

Frozen operationalization (brief §4) — do not retune:
  T-k = k-th-to-last trading day of calendar month (CME session days)
  Window = close(T-3) → close(T-1) log return
  R_spread = cum ES − cum ZN from last-month T-1 close through this-month T-4 close
  Qualifying: |R_spread| ≥ 100bp (log-space threshold = ln(1.01))
  Signal: R_spread ≥ +thr → short (−1); R_spread ≤ −thr → long (+1)
  C = ln(close/open)_T-2 + ln(close/open)_T-1
  G = window − C
  Placebo = close(T-13) → close(T-11)
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PARENTS = DATA / "parents_ohlcv_1d.parquet"
MICROS = DATA / "micros_ohlcv_1d.parquet"

# Frozen §4: 100bp. Log-return threshold = ln(1 + 0.01); do not retune.
R_SPREAD_BP = 100.0
R_SPREAD_THRESHOLD_LOG = math.log(1.0 + R_SPREAD_BP / 10_000.0)

# Study window (brief §4 H1): months through 2026-06 inclusive.
PANEL_END_YEAR = 2026
PANEL_END_MONTH = 6

# Placebo needs T-13; primary window needs T-4..T-1.
MIN_DAYS_FOR_PLACEBO = 13


def _to_et_index(df: pd.DataFrame) -> pd.DataFrame:
    """Index Databento ts_event → America/New_York settlement calendar date."""
    out = df.copy()
    if "ts_event" in out.columns:
        ts = pd.to_datetime(out["ts_event"], utc=True)
    else:
        ts = pd.to_datetime(out.index, utc=True)
    et = ts.dt.tz_convert("America/New_York")
    out["session_date"] = et.dt.normalize().dt.tz_localize(None)
    # Globex ohlcv-1d is typically stamped at session open (evening prior).
    # If hour >= 17 ET on calendar D, settlement day is D+1; else same calendar day.
    hour = et.dt.hour
    settle = et.dt.tz_localize(None).dt.normalize()
    settle = settle + pd.to_timedelta((hour >= 17).astype(int), unit="D")
    out["settle_date"] = settle.dt.normalize()
    return out


def load_symbol_frame(path: Path, symbol: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    sym_col = "symbol" if "symbol" in df.columns else None
    if sym_col and df[sym_col].nunique() > 1:
        exact = df[sym_col].astype(str) == symbol
        if exact.any():
            df = df.loc[exact].copy()
        else:
            mask = df[sym_col].astype(str).str.startswith(symbol.split(".")[0])
            df = df.loc[mask].copy()
    df = _to_et_index(df)
    # Databento GLBX ohlcv-1d buckets by UTC calendar day, so the Sunday-evening
    # Globex reopen (Sun 18:00 ET) lands in its own thin bar whose settle_date is a
    # SUNDAY. That is not a CME equity-index trade date — the real Monday trade date
    # is carried by the Monday bar. Left in, these phantom Sunday days shift the
    # month-end T-k offset counting (e.g. March-2024 T-1 becomes Sun 03-31 instead of
    # the true last trade date Thu 03-28). Drop weekend settle_dates so trading days
    # match the CME calendar the frozen §4 definition refers to. (Weekday filter, not
    # a parameter change; the synthetic self-tests use bdate_range so never hit this.)
    wd = pd.to_datetime(df["settle_date"]).dt.dayofweek
    df = df.loc[wd <= 4]
    df = df.sort_values("settle_date")
    df = df.drop_duplicates("settle_date", keep="last")
    df = df.set_index("settle_date")
    for col in ("open", "high", "low", "close"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[["open", "high", "low", "close"]].dropna(subset=["close"])


def trading_days_in_month(index: pd.DatetimeIndex, year: int, month: int) -> pd.DatetimeIndex:
    mask = (index.year == year) & (index.month == month)
    return index[mask]


def prev_calendar_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def t_offsets(days: pd.DatetimeIndex) -> dict[int, pd.Timestamp]:
    """T-k = k-th-to-last trading day. days must be sorted ascending."""
    n = len(days)
    return {k: days[n - k] for k in range(1, n + 1)}


def log_ret(a: float, b: float) -> float:
    return float(np.log(b / a))


def signal_from_r_spread(r_spread: float) -> int:
    """Frozen §4 signal; qualifying ≡ signal != 0 (|R_spread| ≥ 100bp)."""
    if r_spread >= R_SPREAD_THRESHOLD_LOG:
        return -1  # short-window prediction
    if r_spread <= -R_SPREAD_THRESHOLD_LOG:
        return +1  # long-window prediction
    return 0


def build_monthly_panel(
    es: pd.DataFrame,
    zn: pd.DataFrame,
    ym: pd.DataFrame | None = None,
    gc: pd.DataFrame | None = None,
    *,
    end_year: int = PANEL_END_YEAR,
    end_month: int = PANEL_END_MONTH,
) -> pd.DataFrame:
    """One row per calendar month with frozen fields."""
    idx = es.index.intersection(zn.index)
    es, zn = es.loc[idx], zn.loc[idx]
    months = sorted({(d.year, d.month) for d in idx})
    rows = []

    for y, m in months:
        if (y, m) > (end_year, end_month):
            continue
        days = trading_days_in_month(idx, y, m)
        if len(days) < MIN_DAYS_FOR_PLACEBO:
            continue

        prev_y, prev_m = prev_calendar_month(y, m)
        prev_days = trading_days_in_month(idx, prev_y, prev_m)
        if len(prev_days) < 1:
            continue

        t = t_offsets(days)
        t_prev1 = prev_days[-1]
        needed = [t_prev1, t[4], t[3], t[2], t[1], t[13], t[11]]
        if any(d not in es.index or d not in zn.index for d in needed):
            continue

        r_spread = log_ret(es.loc[t_prev1, "close"], es.loc[t[4], "close"]) - log_ret(
            zn.loc[t_prev1, "close"], zn.loc[t[4], "close"]
        )
        window = log_ret(es.loc[t[3], "close"], es.loc[t[1], "close"])
        c_capt = log_ret(es.loc[t[2], "open"], es.loc[t[2], "close"]) + log_ret(
            es.loc[t[1], "open"], es.loc[t[1], "close"]
        )
        gap = window - c_capt
        placebo = log_ret(es.loc[t[13], "close"], es.loc[t[11], "close"])

        # Next-month reversal: T-1 → T+3 (3rd trading day of next calendar month).
        reversal = np.nan
        next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
        next_days = trading_days_in_month(idx, next_y, next_m)
        if len(next_days) >= 3 and t[1] in es.index and next_days[2] in es.index:
            reversal = log_ret(es.loc[t[1], "close"], es.loc[next_days[2], "close"])

        signal = signal_from_r_spread(r_spread)
        signed = signal * window if signal != 0 else np.nan
        signed_c = signal * c_capt if signal != 0 else np.nan

        row = {
            "year": y,
            "month": m,
            "month_id": f"{y:04d}-{m:02d}",
            "n_trading_days": len(days),
            "T_1": t[1],
            "T_2": t[2],
            "T_3": t[3],
            "T_4": t[4],
            "R_spread": r_spread,
            "R_spread_bp": r_spread * 10_000.0,
            "window": window,
            "C": c_capt,
            "G": gap,
            "placebo": placebo,
            "reversal_T1_to_next_T3": reversal,
            "signal": signal,
            "signed_window": signed,
            "signed_C": signed_c,
            "qualifying": signal != 0,
            "quarter_end": m in (3, 6, 9, 12),
            "micro_era": pd.Timestamp(t[1]) >= pd.Timestamp("2019-05-06"),
        }

        if ym is not None and all(d in ym.index for d in (t[3], t[1])):
            row["ym_window"] = log_ret(ym.loc[t[3], "close"], ym.loc[t[1], "close"])
            row["signed_ym_window"] = signal * row["ym_window"] if signal else np.nan

        # Identical rule on GC: same ES−ZN condition/signal; GC window (brief §4 P-instrument).
        if gc is not None and all(d in gc.index for d in (t[3], t[1])):
            row["gc_window"] = log_ret(gc.loc[t[3], "close"], gc.loc[t[1], "close"])
            row["signed_gc_window"] = signal * row["gc_window"] if signal else np.nan

        rows.append(row)

    return pd.DataFrame(rows)


def inspect_parquet(path: Path) -> None:
    df = pd.read_parquet(path)
    print(f"=== {path.name} ===")
    print("columns:", list(df.columns))
    print("rows:", len(df))
    if "symbol" in df.columns:
        print("symbols:", df["symbol"].value_counts().head(20).to_dict())
    print(df.head(3))


if __name__ == "__main__":
    for p in (PARENTS, MICROS, DATA / "ES_c0_definition.parquet"):
        if p.exists():
            inspect_parquet(p)
        else:
            print(f"MISSING {p}")
