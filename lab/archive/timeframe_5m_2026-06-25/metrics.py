"""Per-strategy metrics on the FXIFY static-$200K basis (avoids TV compounding
artifact). PF/WR are count-based; Net/MaxDD/RF/1R use static_pnl."""
from __future__ import annotations
import numpy as np
import pandas as pd

import portfolio_mc as pmc          # core, via conftest sys.path

STATIC_EQUITY = 200_000.0

def static_pnl(exits: pd.DataFrame) -> pd.Series:
    return exits["net_pnl_pct"].astype(float) / 100.0 * STATIC_EQUITY

def _pf(pnl: pd.Series) -> float:
    gp = float(pnl[pnl > 0].sum())
    gl = float(-pnl[pnl < 0].sum())
    return gp / gl if gl > 0 else float("inf")

def _win_rate(pnl: pd.Series) -> float:
    return float((pnl > 0).sum() / len(pnl)) if len(pnl) else 0.0

def _max_dd(pnl: pd.Series) -> float:
    curve = pnl.cumsum()
    dd = curve.cummax() - curve
    return float(dd.max()) if len(dd) else 0.0

def compute_metrics(exits: pd.DataFrame, strategy: str) -> dict:
    pnl = static_pnl(exits)
    net = float(pnl.sum())
    mdd = _max_dd(pnl)
    r1, fell_back = pmc.implied_1r(pnl, strategy)
    return {
        "trades": int(len(exits)),
        "net_usd": net,
        "pf": _pf(pnl),
        "win_rate": _win_rate(pnl),
        "max_dd_usd": mdd,
        "rf": float(net / mdd) if mdd > 0 else float("inf"),
        "r1_usd": float(r1),
        "r1_fell_back": bool(fell_back),
    }
