"""Provisional CME-micro granularity floors for the prop pair (NAS100/DJ30).

Floor = the account balance below which the base position rounds to 0 contracts:
    base_contracts(balance) = floor( (balance * risk_pct) / (sl_pts * $per_pt) )
    floor_balance           = (sl_pts * $per_pt) / risk_pct     # base first hits 1

$per_pt is the VERIFIED micro value (MNQ $2 / MYM $0.50), NEVER the loaded
standard-E-mini file's pointvalue (spec §2.2 / plan Global Constraints).
ATR is computed on the roll-seam-masked panel (A4). All outputs PROVISIONAL
until the ATR length / SL multiple / risk% are Pine-verified at Phase B B0.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import roll_mask as rm  # noqa: E402

_BAR_DIR = Path(__file__).resolve().parents[4] / "core" / "data" / "bar_data"


def _atr_points(bars: pd.DataFrame, *, symbol: str, atr_len: int) -> float:
    """Median ATR (in price points) over the roll-seam-masked panel (RMA/Wilder)."""
    b = rm.flag_roll_seams(bars, symbol=symbol).copy()
    b = b[~b["roll_seam"]].reset_index(drop=True)
    prev_close = b["close"].shift(1)
    tr = pd.concat([
        b["high"] - b["low"],
        (b["high"] - prev_close).abs(),
        (b["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1.0 / atr_len, adjust=False, min_periods=atr_len).mean()
    return float(atr.median())


def derive_floor(symbol: str, *, atr_len: int, sl_mult: float, risk_pct: float,
                 dollars_per_pt: float, balance_grid: list[float]) -> dict:
    bars = pd.read_csv(_BAR_DIR / f"{symbol}_M15.csv")
    atr_pts = _atr_points(bars, symbol=symbol, atr_len=atr_len)
    sl_pts = sl_mult * atr_pts
    risk_frac = risk_pct / 100.0
    floor_balance = (sl_pts * dollars_per_pt) / risk_frac

    def base_contracts(bal: float) -> int:
        return math.floor((bal * risk_frac) / (sl_pts * dollars_per_pt))

    per_tier = []
    for bal in balance_grid:
        n = base_contracts(bal)
        ideal = (bal * risk_frac) / (sl_pts * dollars_per_pt)
        rounding_loss = (1.0 - n / ideal) if ideal > 0 else 1.0
        per_tier.append({"balance": bal, "base_contracts": n,
                         "ideal_contracts": round(ideal, 3),
                         "rounding_loss_pct": round(100 * rounding_loss, 1)})

    return {"symbol": symbol, "atr_points_median": round(atr_pts, 2),
            "sl_points": round(sl_pts, 2), "dollars_per_pt": dollars_per_pt,
            "risk_pct": risk_pct, "floor_balance": round(floor_balance, 0),
            "per_tier": per_tier}


BULENOX_TIERS = [25_000, 50_000, 100_000, 150_000, 250_000]

# PROVISIONAL locked values (LOCK.md mirror — re-verify vs Pine at B0).
CONFIGS = {
    "NQ": dict(atr_len=11, sl_mult=1.20, risk_pct=0.37, dollars_per_pt=2.00),   # -> MNQ
    "YM": dict(atr_len=11, sl_mult=1.20, risk_pct=0.70, dollars_per_pt=0.50),   # -> MYM
}


def main() -> None:
    for sym, cfg in CONFIGS.items():
        r = derive_floor(sym, balance_grid=BULENOX_TIERS, **cfg)
        print(f"\n{sym} -> micro (${cfg['dollars_per_pt']}/pt) PROVISIONAL")
        print(f"  ATR(pts) median {r['atr_points_median']}  SL(pts) {r['sl_points']}"
              f"  floor_balance ${r['floor_balance']:,.0f}")
        for t in r["per_tier"]:
            print(f"    ${t['balance']:>7,.0f}: base {t['base_contracts']} "
                  f"(ideal {t['ideal_contracts']}, rounding loss {t['rounding_loss_pct']}%)")


if __name__ == "__main__":
    main()
