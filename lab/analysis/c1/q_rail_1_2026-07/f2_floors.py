"""Q-RAIL-1 F2 — WATCH-1 integer-sizing floors on MYM/MNQ CME panels.

Recomputes provisional floors at locked ATR(11)×1.20 and at 0.50× effective
risk (WATCH-1), and checks RESERVE-cap add survival at $100K / 80-micro cap.

Panels: core/data/bar_data/{MYM,MNQ}_M15.csv (SHA256SUMS).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "lab/analysis/legacy/futures_conversion_2026-07-01"))
import roll_mask as rm  # noqa: E402

BAR = ROOT / "core/data/bar_data"
OUT = Path(__file__).resolve().parent / "f2_floors.json"

ATR_LEN = 11
SL_MULT = 1.20
ACCOUNT = 100_000.0
CAP = 80


def atr_frame(bars: pd.DataFrame, symbol: str) -> pd.DataFrame:
    b = rm.flag_roll_seams(bars, symbol=symbol).copy()
    b = b[~b["roll_seam"]].reset_index(drop=True)
    t = pd.to_datetime(b["time"], utc=True)
    prev = b["close"].shift(1)
    tr = pd.concat(
        [b["high"] - b["low"], (b["high"] - prev).abs(), (b["low"] - prev).abs()],
        axis=1,
    ).max(axis=1)
    atr = tr.ewm(alpha=1.0 / ATR_LEN, adjust=False, min_periods=ATR_LEN).mean()
    return b.assign(time=t, atr=atr).dropna(subset=["atr"])


def window_stats(
    s: pd.DataFrame,
    *,
    dollars: float,
    risk_full: float,
    pyr_pct: float,
) -> dict:
    atr = float(s["atr"].median())
    sl = SL_MULT * atr
    risk_w1 = risk_full * 0.5
    floor_1x = (sl * dollars) / (risk_full / 100.0)
    floor_w1 = (sl * dollars) / (risk_w1 / 100.0)
    ideal_base = (ACCOUNT * (risk_w1 / 100.0)) / (sl * dollars)
    base = math.floor(ideal_base)
    reserve_base_max = math.floor(CAP / (1.0 + pyr_pct / 100.0))
    base_capped = min(base, reserve_base_max)
    add_qty = math.floor(base_capped * (pyr_pct / 100.0))
    total = base_capped + add_qty
    return {
        "atr_median_pts": round(atr, 4),
        "sl_pts": round(sl, 4),
        "floor_1x_usd": round(floor_1x),
        "floor_watch1_usd": round(floor_w1),
        "ideal_base_at_100k_w1": round(ideal_base, 3),
        "base_qty": base,
        "reserve_base_max": reserve_base_max,
        "base_capped": base_capped,
        "add_qty": add_qty,
        "total_qty": total,
        "base_ge_1": base >= 1,
        "add_survives": add_qty >= 1,
        "under_cap": total <= CAP,
        "headroom_100k_minus_floor_w1": round(ACCOUNT - floor_w1),
    }


def leg(symbol: str, dollars: float, risk_full: float, pyr_pct: float) -> dict:
    bars = pd.read_csv(BAR / f"{symbol}_M15.csv")
    s = atr_frame(bars, symbol)
    tmax = s["time"].max()
    recent = s[s["time"] >= (tmax - pd.Timedelta(days=90))]
    return {
        "symbol": symbol,
        "dollars_per_pt": dollars,
        "risk_full_pct": risk_full,
        "risk_watch1_pct": risk_full * 0.5,
        "pyramid_pct": pyr_pct,
        "panel_n_bars_masked": int(len(s)),
        "panel_end_utc": str(tmax),
        "full_median": window_stats(s, dollars=dollars, risk_full=risk_full, pyr_pct=pyr_pct),
        "recent_90d": window_stats(
            recent, dollars=dollars, risk_full=risk_full, pyr_pct=pyr_pct
        ),
    }


def main() -> None:
    report = {
        "brief": "Q-RAIL-1",
        "scored": "F2",
        "method": "roll-seam-masked RMA ATR(11)×1.20; floor=(sl*$/pt)/risk%; WATCH-1=0.50× risk",
        "account_usd": ACCOUNT,
        "micro_cap": CAP,
        "legs": [
            leg("MYM", 0.50, 0.70, 750.0),
            leg("MNQ", 2.00, 0.37, 1000.0),
        ],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
