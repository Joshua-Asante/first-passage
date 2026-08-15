# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
# Q-FEED-1 closed RESOLVED-BY-RETIREMENT by that ADR. The duka_panel_path /
# load_duka_bars accessors below target core/data/bar_data/*_duka.csv, which
# docs/adr/2026-07-22-challenge-era-substrate-retirement.md disposition B
# DELETED in Phase 5 (2026-07-30). Byte-independent parsing/join helpers remain
# under synthetic test (tests/test_feed_divergence_parsing.py); the byte-reading
# paths do not run.
"""Shared utilities for Q-FEED-1 feed-divergence analysis."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[3]
ANALYSIS_DIR = Path(__file__).resolve().parent
PREREG_PATH = _REPO_ROOT / "docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md"
TV_EXPORT_DIR = _REPO_ROOT / "core/data/tv_exports/pepperstone/bar_export"
BAR_DATA_DIR = _REPO_ROOT / "core/data/bar_data"
RESULTS_PATH = ANALYSIS_DIR / "RESULTS.md"
CONVENTION_PATH = ANALYSIS_DIR / "FROZEN_CONVENTION.txt"

WINDOW_START = pd.Timestamp("2026-03-01T00:00:00Z")
WINDOW_END = pd.Timestamp("2026-06-01T00:00:00Z")
CALIBRATION_END = pd.Timestamp("2026-03-08T00:00:00Z")  # week 1 of frozen window
BAR_MINUTES = 15

FX_SYMBOLS = ("USDJPY", "GBPUSD")
IDX_SYMBOL = "US30"
DUKA_IDX_SYMBOL = "USA30IDXUSD"

# TV BAR EXPORT v0.1 (deployed): Signal = epoch_ms|open|high|low|close|volume
SIGNAL_PIPE_RE = re.compile(
    r"^(?P<epoch>\d+)\|(?P<o>[-\d.]+)\|(?P<h>[-\d.]+)\|(?P<l>[-\d.]+)\|(?P<c>[-\d.]+)\|(?P<v>\d+)$"
)
# Legacy/alternate comment-keyed format (lab pine stub)
COMMENT_RE = re.compile(
    r"^BAR\|o=(?P<o>[-\d.]+)\|h=(?P<h>[-\d.]+)\|l=(?P<l>[-\d.]+)\|c=(?P<c>[-\d.]+)\|v=(?P<v>\d+)$"
)

PRICE_COL = {
    "USDJPY": "Price JPY",
    "GBPUSD": "Price USD",
    "US30": "Price USD",
    "US30USD": "Price USD",
}

# Candidate TV timestamp shifts (minutes) applied to epoch_ms before flooring to M15 UTC open.
# BAR EXPORT v0.1 Signal epoch_ms is bar-open UTC — shift=0 is the null hypothesis.
# tv_close_as_open (-15) removed: it misaligns by one bar when epoch_ms is authoritative
# (defect Q-FEED-1-D1, 2026-06-12). Chart-TZ probes retained for EDT/UTC discovery only.
CONVENTION_CANDIDATES: tuple[tuple[str, int], ...] = (
    ("tv_open_utc", 0),
    ("tv_shift_minus_4h", -240),
    ("tv_shift_minus_5h", -300),
    ("tv_shift_plus_4h", 240),
    ("tv_shift_plus_5h", 300),
)

# Week-1 calibration tie-break: if match count within this many of the leader, prefer
# lower FX p95(|Δclose|)/ATR14 (price-agreement; still week-1-only, not full-window shopping).
CALIBRATION_MATCH_TIE_BARS = 5

US30_CLOSE_MIN = 15_000.0
US30_CLOSE_MAX = 55_000.0


@dataclass(frozen=True)
class FrozenThresholds:
    fx_p95_accept: float
    fx_p95_reject: float
    fx_cov_accept: float
    fx_cov_reject: float
    idx_residual_p95_accept: float
    idx_residual_p95_reject: float


def load_thresholds(path: Path | None = None) -> FrozenThresholds:
    """Parse frozen thresholds from the pre-registration markdown table."""
    text = (path or PREREG_PATH).read_text(encoding="utf-8")
    rows: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 4 or parts[0] in ("Metric", "---"):
            continue
        # Metric names may contain escaped pipes (e.g. p95(\|Δclose\|)); take fixed tail columns.
        accept, reject = parts[-3], parts[-2]
        metric = "|".join(parts[:-3])
        rows[metric] = (accept, reject)

    def _row(prefix: str) -> tuple[str, str]:
        for key, vals in rows.items():
            if key.startswith(prefix):
                return vals
        raise KeyError(f"pre-registration row not found for prefix {prefix!r}")

    def _pct(s: str) -> float:
        return float(s.replace("%", "").strip()) / 100.0

    fx_accept, fx_reject = _row("FX p95")
    cov_accept, cov_reject = _row("FX matched-bar coverage")
    idx_accept, idx_reject = _row("IDX residual p95")
    return FrozenThresholds(
        fx_p95_accept=float(fx_accept.replace("<", "").strip()),
        fx_p95_reject=float(fx_reject.replace("≥", "").strip()),
        fx_cov_accept=_pct(cov_accept.replace("≥", "")),
        fx_cov_reject=_pct(cov_reject.replace("<", "")),
        idx_residual_p95_accept=float(idx_accept.replace("<", "").strip()),
        idx_residual_p95_reject=float(idx_reject.replace("≥", "").strip()),
    )


def decode_bar_signal(signal: str) -> dict[str, float]:
    """Decode BAR EXPORT v0.1 Signal field (pipe or comment-keyed)."""
    text = str(signal).strip()
    m = SIGNAL_PIPE_RE.match(text)
    if m:
        return {
            "epoch_ms": float(m.group("epoch")),
            "o": float(m.group("o")),
            "h": float(m.group("h")),
            "l": float(m.group("l")),
            "c": float(m.group("c")),
            "v": float(m.group("v")),
        }
    m = COMMENT_RE.match(text)
    if m:
        return {k: float(m.group(k)) for k in ("o", "h", "l", "c", "v")}
    raise ValueError(f"BAR EXPORT signal decode fail: {text!r}")


def decode_bar_comment(comment: str) -> dict[str, float]:
    """Alias for decode_bar_signal (tests / legacy name)."""
    return decode_bar_signal(comment)


def price_tolerance(symbol: str, price: float) -> float:
    if symbol in ("US30", "US30USD"):
        return max(0.5, price * 1e-4)
    if "JPY" in symbol:
        return max(0.001, price * 1e-4)
    return max(1e-5, price * 1e-4)


def _trade_id_column(df: pd.DataFrame) -> str:
    for col in ("Trade #", "Trade number"):
        if col in df.columns:
            return col
    raise ValueError("TV export missing Trade # / Trade number column")


def parse_tv_bar_export(path: Path, *, symbol: str) -> pd.DataFrame:
    """Decode BAR EXPORT v0.1 List-of-Trades CSV into OHLCV bars."""
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    if "Date and time" not in raw.columns:
        raise ValueError(f"TV export missing Date and time column: {path}")

    price_col = PRICE_COL.get(symbol)
    if price_col is None or price_col not in raw.columns:
        raise ValueError(f"TV export missing price column for {symbol}: {path}")

    trade_col = _trade_id_column(raw)
    entries = raw[raw["Type"].astype(str).str.startswith("Entry")].copy()
    entries = entries.sort_values(trade_col).reset_index(drop=True)

    rows: list[dict] = []
    skipped = 0
    for i in range(len(entries)):
        signal = entries.iloc[i].get("Signal", entries.iloc[i].get("Comment", ""))
        try:
            enc = decode_bar_signal(signal)
        except ValueError:
            skipped += 1
            continue
        entry_px = float(entries.iloc[i][price_col])
        tol = price_tolerance(symbol, enc["c"])
        # process_orders_on_close: fill price == bar close
        if abs(entry_px - enc["c"]) > tol:
            raise ValueError(
                f"Cross-check fail {path} trade {entries.iloc[i][trade_col]}: "
                f"entry px {entry_px} vs encoded close {enc['c']}"
            )
        if "epoch_ms" in enc:
            ts = pd.to_datetime(int(enc["epoch_ms"]), unit="ms", utc=True)
        else:
            ts = pd.to_datetime(entries.iloc[i]["Date and time"], utc=True)
        rows.append({
            "tv_time": ts,
            "open": enc["o"],
            "high": enc["h"],
            "low": enc["l"],
            "close": enc["c"],
            "volume": enc["v"],
        })

    if skipped:
        print(f"=== parse_tv_bar_export: skipped {skipped} entry rows without pipe signal ===")
    if not rows:
        raise ValueError(f"No decodable bars in {path}")

    return pd.DataFrame(rows).sort_values("tv_time").reset_index(drop=True)


def load_duka_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df.sort_values("time").reset_index(drop=True)


def floor_m15_utc(ts: pd.Series) -> pd.Series:
    return ts.dt.floor(f"{BAR_MINUTES}min")


def apply_convention(tv: pd.DataFrame, shift_minutes: int) -> pd.DataFrame:
    out = tv.copy()
    out["bar_open"] = floor_m15_utc(out["tv_time"] + pd.Timedelta(minutes=shift_minutes))
    return out


def is_weekend_boundary(ts: pd.Timestamp) -> bool:
    """Fri 21:00 UTC through Sun 22:00 UTC (exclusive of Sun 22:00)."""
    wd, hour = ts.weekday(), ts.hour
    if wd == 4 and hour >= 21:
        return True
    if wd == 5:
        return True
    if wd == 6 and hour < 22:
        return True
    return False


def eligible_mask(times: pd.Series) -> pd.Series:
    return ~times.map(lambda t: is_weekend_boundary(t))


def compute_atr14(df: pd.DataFrame, *, time_col: str = "time") -> pd.Series:
    """Wilder ATR(14) on the Dukascopy OHLC series."""
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()


def match_bars(
    duka: pd.DataFrame,
    tv: pd.DataFrame,
    *,
    shift_minutes: int,
    start: pd.Timestamp = WINDOW_START,
    end: pd.Timestamp = WINDOW_END,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (matched, duka_only, tv_only) within [start, end), ex weekend boundary."""
    d = duka.copy()
    d["bar_open"] = floor_m15_utc(d["time"])
    t = apply_convention(tv, shift_minutes)

    d = d[(d["bar_open"] >= start) & (d["bar_open"] < end)]
    t = t[(t["bar_open"] >= start) & (t["bar_open"] < end)]
    d = d[eligible_mask(d["bar_open"])].copy()
    t = t[eligible_mask(t["bar_open"])].copy()

    merged = d.merge(t, on="bar_open", how="inner", suffixes=("_duka", "_tv"))
    d_only = d[~d["bar_open"].isin(merged["bar_open"])].copy()
    t_only = t[~t["bar_open"].isin(merged["bar_open"])].copy()
    return merged, d_only, t_only


def coverage_ratio(matched: pd.DataFrame, duka_eligible: pd.DataFrame) -> float:
    if len(duka_eligible) == 0:
        return 0.0
    return len(matched) / len(duka_eligible)


def p95_abs_delta_close_norm(matched: pd.DataFrame, atr: pd.Series) -> float:
    if matched.empty:
        return float("nan")
    atr_at = atr.reindex(matched["bar_open"]).values
    delta = (matched["close_duka"] - matched["close_tv"]).abs().values
    valid = np.isfinite(atr_at) & (atr_at > 0)
    if not valid.any():
        return float("nan")
    return float(np.nanpercentile(delta[valid] / atr_at[valid], 95))


def rolling_day_median_basis(matched: pd.DataFrame) -> pd.Series:
    """Rolling 1-trading-day median of (duka_close - tv_close) on matched bars."""
    m = matched.sort_values("bar_open").copy()
    m["basis"] = m["close_duka"] - m["close_tv"]
    m["trade_date"] = m["bar_open"].dt.date
    day_median = m.groupby("trade_date", sort=True)["basis"].transform("median")
    return day_median


def idx_residual_p95(matched: pd.DataFrame, atr: pd.Series) -> float:
    if matched.empty:
        return float("nan")
    basis = rolling_day_median_basis(matched)
    residual = (matched["close_duka"] - matched["close_tv"] - basis).abs()
    atr_at = atr.reindex(matched["bar_open"]).values
    valid = np.isfinite(atr_at) & (atr_at > 0)
    if not valid.any():
        return float("nan")
    return float(np.nanpercentile((residual.values[valid] / atr_at[valid]), 95))


def classify_verdict_band(value: float, accept: float, reject: float, *, higher_is_worse: bool) -> str:
    if not np.isfinite(value):
        return "AMBIGUOUS"
    if higher_is_worse:
        if value < accept:
            return "ACCEPT"
        if value >= reject:
            return "REJECT"
        return "AMBIGUOUS"
    # coverage: higher is better
    if value >= accept:
        return "ACCEPT"
    if value < reject:
        return "REJECT"
    return "AMBIGUOUS"


def duka_panel_path(symbol: str) -> Path:
    if symbol == IDX_SYMBOL:
        return BAR_DATA_DIR / "USA30IDXUSD_M15_duka.csv"
    return BAR_DATA_DIR / f"{symbol}_M15_duka.csv"


def tv_panel_path(symbol: str) -> Path:
    return TV_EXPORT_DIR / f"{symbol}_M15_pep.csv"
