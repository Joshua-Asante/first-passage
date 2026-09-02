"""Shared feature/day-frame builder for the ORB-MYM-1 v0.4 filter screen (2026-09-02).
Definitions frozen in PREREG_filters.md. Reuses load_sessions.py verbatim.

Reproduction: requires (1) a local, non-committed copy of the operator's
`ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-01_76b9e.csv` export (override with a
CLI arg or by editing CSV below) and (2) `core/data/bar_data/MYM_M15.csv`
present locally (gitignored vendor data; see core/data/bar_data/README.md).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[4]
HARVEST = REPO / "lab" / "analysis" / "_inbox" / "mym_mechanism_harvest_2026-08-29"
sys.path.insert(0, str(HARVEST))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_sessions import load_bars, session_ohlc, rth_ohlc, overnight_ohlc, wilder_tr  # noqa: E402
from _reconcile_lite import load_csv  # noqa: E402

CSV = sys.argv[1] if len(sys.argv) > 1 else str(
    Path.home() / "Downloads" / "ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-01_76b9e.csv"
)
W = 60
TODW = 20


def _pctl(x, w, q):
    return pd.Series(x).rolling(w, min_periods=w).quantile(q).shift(1).to_numpy()


def _med(x, w):
    return pd.Series(x).rolling(w, min_periods=w).median().shift(1).to_numpy()


def tod_ratio(values, slot, window):
    n = len(values); out = np.full(n, np.nan); by_slot = {}
    for t in range(n):
        s = int(slot[t]); hist = by_slot.get(s, [])
        if len(hist) >= window:
            med = float(np.median(hist[-window:]))
            if med > 0:
                out[t] = values[t] / med
        hist.append(float(values[t])); by_slot[s] = hist
    return out


def session_features() -> pd.DataFrame:
    bars = load_bars()
    bars = bars[bars["session"] < bars["session"].max()]
    full = session_ohlc(bars); full = full[full["n_bars"] >= 20]
    idx = full.index
    rth = rth_ohlc(bars).reindex(idx); on = overnight_ohlc(bars).reindex(idx)
    f = pd.DataFrame(index=idx)
    f["rth_range"] = (rth["high"] - rth["low"]).to_numpy()
    f["on_range"] = (on["high"] - on["low"]).to_numpy()
    f["rth_open"] = rth["open"].to_numpy(); f["rth_close"] = rth["close"].to_numpy()
    f["prev_rth_close"] = f["rth_close"].shift(1)
    f["prev_rth_high"] = rth["high"].shift(1).to_numpy(); f["prev_rth_low"] = rth["low"].shift(1).to_numpy()
    f["gap"] = f["rth_open"] - f["prev_rth_close"]; f["abs_gap"] = f["gap"].abs()
    f["on_ret"] = on["close"].to_numpy() - f["prev_rth_close"]
    f["prev_rth_ret"] = f["rth_close"].shift(1) - f["rth_open"].shift(1)
    pr = f["prev_rth_high"] - f["prev_rth_low"]
    f["prev_clv"] = (f["prev_rth_close"] - f["prev_rth_low"]) / pr.where(pr > 0)
    on_r = f["on_range"].to_numpy(); rr = f["rth_range"].to_numpy()
    f["on_p80"] = _pctl(on_r, W, 0.80)
    f["on_elev80"] = (f["on_range"] >= f["on_p80"]).astype(float).where(f["on_p80"].notna())
    rr_p80 = _pctl(rr, W, 0.80)
    prev_elev = pd.Series((rr >= rr_p80).astype(float)).where(pd.Series(rr_p80).notna())
    f["bprime"] = prev_elev.shift(1).to_numpy()
    f["gap_p80"] = _pctl(f["abs_gap"].to_numpy(), W, 0.80)
    f["gap_elev80"] = (f["abs_gap"] >= f["gap_p80"]).astype(float).where(f["gap_p80"].notna())
    tr = wilder_tr(full)
    f["atr20"] = tr.rolling(20, min_periods=20).mean().shift(1).to_numpy()
    b = bars.copy()
    b["vol_tod"] = tod_ratio(b["volume"].to_numpy(float), b["minute"].to_numpy(int), TODW)
    for name, minute in (("or0930", 570), ("b0915", 555)):
        sub = b[b["minute"] == minute].set_index("session"); sub.index = pd.to_datetime(sub.index)
        f[f"{name}_vol_tod"] = sub["vol_tod"].reindex(idx).to_numpy()
        f[f"{name}_high"] = sub["high"].reindex(idx).to_numpy()
        f[f"{name}_low"] = sub["low"].reindex(idx).to_numpy()
    # as-run OR 09:15-09:45 = union of the 09:15 and 09:30 bars (Pine: inOR window)
    f["orr"] = np.maximum(f["b0915_high"], f["or0930_high"]) - np.minimum(f["b0915_low"], f["or0930_low"])
    # min_periods=45: 3 sessions lack a 09:15/09:30 bar (ORR NaN) and would otherwise
    # poison every 60-session window after them (598 -> 524 scorable days; fixed
    # 2026-09-02, disclosed in PREREG_filters.md's addendum). Threshold unchanged.
    f["orr_med60"] = pd.Series(f["orr"].to_numpy()).rolling(W, min_periods=45).median().shift(1).to_numpy()
    f["orr_wide"] = (f["orr"] > f["orr_med60"]).astype(float).where(f["orr_med60"].notna())
    f["or_width_atr"] = f["orr"] / f["atr20"]
    f["dow"] = idx.dayofweek
    return f


def day_frame(csv_path: str = CSV) -> pd.DataFrame:
    df = load_csv(csv_path)
    ent = df[df["Type"].str.startswith("Entry")].copy(); ex = df[df["Type"].str.startswith("Exit")].copy()
    assert list(df["Size (qty)"].unique()) == [2]
    tag = ent.set_index("Trade #")["Signal"]
    ex["tag"] = ex["Trade #"].map(tag)
    ex["hot"] = (ex["tag"].str.contains("Hot") & ~ex["tag"].str.contains("NotHot")).astype(int)
    ex["day"] = pd.to_datetime(ex["dt"].dt.date); ent["day"] = pd.to_datetime(ent["dt"].dt.date)
    base = ent[ent["Signal"].str.startswith("ORB")].copy()
    days = ex.groupby("day").agg(pnl=("Net P&L USD", "sum"), hot=("hot", "max"),
                                 n_exits=("Net P&L USD", "size"), mae=("Adverse excursion USD", "min"))
    fb = base.sort_values("dt").groupby("day").first()
    days["base_time_min"] = (fb["dt"].dt.hour * 60 + fb["dt"].dt.minute).reindex(days.index)
    days["n_add"] = ent[ent["Signal"].str.startswith("Scale-in")].groupby("day").size().reindex(days.index).fillna(0)
    days["pnl_pc"] = days["pnl"] / 2.0; days["mae_pc"] = np.minimum(days["mae"] / 2.0, 0.0)
    m = days.join(session_features(), how="left")
    m["scorable"] = m["rth_range"].notna() & m["on_elev80"].notna() & m["orr_wide"].notna()
    return m


if __name__ == "__main__":
    m = day_frame()
    s = m[m.scorable]
    print(len(m), int(m.scorable.sum()), s.index.min().date(), s.index.max().date())
    print("hot==on_elev80:", bool((s.hot == s.on_elev80).all()))
    print("orr median (scorable):", float(s.orr.median()), " wide-share:", float(s.orr_wide.mean()))
