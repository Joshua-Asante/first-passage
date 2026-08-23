"""Call-4 beta-cohesion diagnostic — pairwise lead-lag on historical panels.

Report-only. Informs the soft-flag interim review. Does not implement the
2-of-4 / 3-of-4 WATCH counts (those live in ``core.lifecycle.beta_death_assessment``)
and does not write authorization state.

Lag convention: positive ``lag`` means series B lags series A (A leads).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Mapping

import numpy as np

COHESION_CORR_FLOOR = 0.50
DEFAULT_MAX_LAG = 8


@dataclass(frozen=True)
class LeadLagPair:
    a: str
    b: str
    lag: int
    corr: float


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    if x.size < 8 or y.size < 8:
        return float("nan")
    if float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def lagged_correlation(x: np.ndarray, y: np.ndarray, max_lag: int = DEFAULT_MAX_LAG) -> tuple[int, float]:
    """Return (lag, corr) maximizing |corr|. Positive lag => y lags x."""
    x = np.asarray(x, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    if x.size != y.size:
        raise ValueError(f"series length mismatch: {x.size} vs {y.size}")
    if max_lag < 0:
        raise ValueError("max_lag must be >= 0")
    best_lag = 0
    best_corr = _pearson(x, y)
    best_abs = abs(best_corr) if np.isfinite(best_corr) else -1.0
    for lag in range(-max_lag, max_lag + 1):
        if lag == 0:
            continue
        if lag > 0:
            corr = _pearson(x[:-lag], y[lag:])
        else:
            corr = _pearson(x[-lag:], y[:lag])
        score = abs(corr) if np.isfinite(corr) else -1.0
        if score > best_abs:
            best_abs = score
            best_corr = corr
            best_lag = lag
    return best_lag, best_corr


def pairwise_lead_lag(
    series: Mapping[str, np.ndarray],
    max_lag: int = DEFAULT_MAX_LAG,
) -> dict[tuple[str, str], LeadLagPair]:
    names = list(series)
    out: dict[tuple[str, str], LeadLagPair] = {}
    for a, b in combinations(names, 2):
        lag, corr = lagged_correlation(series[a], series[b], max_lag=max_lag)
        out[(a, b)] = LeadLagPair(a=a, b=b, lag=lag, corr=corr)
    return out


def cohesion_flag(
    pairs: Mapping[tuple[str, str], LeadLagPair],
    floor: float = COHESION_CORR_FLOOR,
) -> bool:
    return any(np.isfinite(p.corr) and abs(p.corr) >= floor for p in pairs.values())


def load_close_series(name: str, path: str | Path) -> tuple[np.ndarray | None, str]:
    """Load a close series. Missing vendor CSV → (None, reason). Never raises on absence."""
    p = Path(path)
    if not p.exists():
        return None, f"missing vendor CSV: {p}"
    try:
        import pandas as pd
    except ImportError:  # pragma: no cover
        return None, "pandas unavailable"

    df = pd.read_csv(p)
    cols = {c.lower(): c for c in df.columns}
    if "close" in cols:
        close = pd.to_numeric(df[cols["close"]], errors="coerce").to_numpy(dtype=float)
        close = close[np.isfinite(close)]
        if close.size < 16:
            return None, f"{name}: too few close prints"
        return close, ""
    if "signal" in cols:
        try:
            from bar_export_loader import parse_bar_export
        except ImportError:  # pragma: no cover
            return None, f"{name}: bar_export_loader unavailable"
        symbol = _symbol_from_stem(p.stem) or name
        bars = parse_bar_export(p, symbol=symbol)
        close = bars["close"].to_numpy(dtype=float)
        close = close[np.isfinite(close)]
        if close.size < 16:
            return None, f"{name}: too few decoded bars"
        return close, ""
    return None, f"{name}: no close/Signal column"


def _symbol_from_stem(stem: str) -> str | None:
    parts = stem.split("_")
    for part in parts:
        if part.endswith("1!") or part.endswith("1"):
            return part
    return None


def returns_from_close(close: np.ndarray) -> np.ndarray:
    close = np.asarray(close, dtype=float).ravel()
    close = close[np.isfinite(close) & (close > 0)]
    if close.size < 17:
        return np.asarray([], dtype=float)
    return np.diff(np.log(close))


def build_report(
    loaded: Mapping[str, np.ndarray],
    skipped: list[dict[str, str]],
    *,
    max_lag: int = DEFAULT_MAX_LAG,
    floor: float = COHESION_CORR_FLOOR,
) -> dict:
    rets = {k: returns_from_close(v) for k, v in loaded.items()}
    rets = {k: v for k, v in rets.items() if v.size >= 16}
    n = min((v.size for v in rets.values()), default=0)
    aligned = {k: v[-n:] for k, v in rets.items()} if n else {}
    pairs = pairwise_lead_lag(aligned, max_lag=max_lag) if len(aligned) >= 2 else {}
    return {
        "diagnostic": "beta_cohesion",
        "max_lag": max_lag,
        "corr_floor": floor,
        "series": sorted(aligned),
        "skipped": skipped,
        "pairs": [asdict(p) for p in pairs.values()],
        "cohesion_flag": cohesion_flag(pairs, floor=floor) if pairs else False,
        "soft_flag_owner": "core.lifecycle.beta_death_assessment",
        "wrote_lifecycle_state": False,
    }
