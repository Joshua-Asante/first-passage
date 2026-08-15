"""Q-TXG-1 striker×MNQ Block-4/5 scoring."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "lab"))
sys.path.insert(0, str(REPO / "core"))

from reconcile import compute_metrics, load_csv  # noqa: E402

CELL = Path(__file__).resolve().parent
PANEL = CELL / "inputs" / (
    "Striker_DJ30_MNQ_Q-TXG-1_PROTOTYPE_CME_MINI_MNQ1!_2026-08-12_68340.csv"
)
PANEL_SHA = "7bf08a2341284a5ec378d5cbf67e92399a597176c7dfc638da1421be06864025"
REQUIRED_NET_R = 0.03
MNQ_POINT_VALUE = 2.00
COMMISSION_PER_SIDE = 0.91
INITIAL_CAPITAL = 100_000.0
BAR_PATH = Path(r"C:/Users/joshu/multi_firm_operations/core/data/bar_data/MNQ_M15.csv")
BAR_SHA = "6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def static_equity_recompute(df: pd.DataFrame) -> dict:
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    entries = df[df["Type"].astype(str).str.startswith("Entry")].copy()
    entry_by_trade = entries.set_index("Trade #")
    deltas = []
    tv_sum = 0.0
    recom_sum = 0.0
    for _, ex in exits.iterrows():
        tid = ex["Trade #"]
        if tid not in entry_by_trade.index:
            continue
        en = entry_by_trade.loc[tid]
        if isinstance(en, pd.DataFrame):
            en = en.iloc[0]
        qty = float(ex["Size (qty)"])
        gross = qty * (float(ex["Price USD"]) - float(en["Price USD"])) * MNQ_POINT_VALUE
        net_recompute = gross - (2.0 * COMMISSION_PER_SIDE * qty)
        tv_net = float(ex["Net P&L USD"])
        deltas.append(abs(net_recompute - tv_net))
        tv_sum += tv_net
        recom_sum += net_recompute
    return {
        "n_legs": len(deltas),
        "tv_net_sum": tv_sum,
        "recompute_net_sum": recom_sum,
        "max_abs_delta": max(deltas) if deltas else 0.0,
        "mean_abs_delta": float(np.mean(deltas)) if deltas else 0.0,
        "ok_within_1usd": bool(all(d < 1.0 for d in deltas)),
    }


def build_daily(df: pd.DataFrame) -> pd.DataFrame:
    exits = df[df["Type"].astype(str).str.startswith("Exit")].copy()
    exits["date"] = pd.to_datetime(exits["Date and time"]).dt.normalize()
    daily = (
        exits.groupby("date", as_index=False)["Net P&L USD"]
        .sum()
        .rename(columns={"Net P&L USD": "pnl_usd"})
    )
    return daily.sort_values("date").reset_index(drop=True)


def load_bars(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path)
    out = pd.DataFrame({
        "ts": pd.to_datetime(raw["time"], utc=True),
        "low": pd.to_numeric(raw["low"], errors="coerce"),
    }).dropna()
    et = out["ts"].dt.tz_convert("America/New_York")
    out["date"] = et.dt.normalize().dt.tz_localize(None)
    out["ts_et"] = et.dt.tz_localize(None)
    return out


def attach_bar_intraday_lows(daily: pd.DataFrame, bars: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    entries = trades[trades["Type"].astype(str).str.startswith("Entry")].copy()
    exits = trades[trades["Type"].astype(str).str.startswith("Exit")].copy()
    entries["ts"] = pd.to_datetime(entries["Date and time"])
    exits["ts"] = pd.to_datetime(exits["Date and time"])
    entry_map = {tid: row for tid, row in entries.set_index("Trade #").iterrows()}
    exit_map = {tid: row for tid, row in exits.set_index("Trade #").iterrows()}

    legs = []
    for tid, en in entry_map.items():
        if tid not in exit_map:
            continue
        ex = exit_map[tid]
        legs.append((
            pd.Timestamp(en["ts"]),
            pd.Timestamp(ex["ts"]),
            float(en["Price USD"]),
            float(en["Size (qty)"]),
        ))

    bars_by_date = {d: g for d, g in bars.groupby("date", sort=False)}
    exits_by_date = {
        d: g for d, g in exits.assign(date=exits["ts"].dt.normalize()).groupby("date", sort=False)
    }

    prior = 0.0
    lows = []
    covered = 0
    for _, row in daily.iterrows():
        day = pd.Timestamp(row["date"])
        day_open_eq = INITIAL_CAPITAL + prior
        prior += float(row["pnl_usd"])
        day_bars = bars_by_date.get(day)
        if day_bars is None or day_bars.empty:
            lows.append(np.nan)
            continue
        covered += 1
        day_legs = [L for L in legs if L[0] < day + pd.Timedelta(days=1) and L[1] >= day]
        day_ex = exits_by_date.get(day)
        min_exc = 0.0
        if day_legs:
            t0 = max(day, min(L[0] for L in day_legs))
            t1 = min(day + pd.Timedelta(days=1), max(L[1] for L in day_legs) + pd.Timedelta(minutes=15))
            sub = day_bars[(day_bars["ts_et"] >= t0) & (day_bars["ts_et"] <= t1)]
        else:
            sub = day_bars.iloc[0:0]
        ts_arr = sub["ts_et"].to_numpy()
        low_arr = sub["low"].to_numpy()
        for ts_et, low in zip(ts_arr, low_arr):
            mtm = 0.0
            for entry_ts, exit_ts, entry_px, qty in day_legs:
                if entry_ts <= ts_et <= exit_ts:
                    mtm += qty * (float(low) - entry_px) * MNQ_POINT_VALUE
            realized = 0.0
            if day_ex is not None:
                realized = float(day_ex.loc[day_ex["ts"] <= ts_et, "Net P&L USD"].sum())
            min_exc = min(min_exc, realized + mtm)
        lows.append(float(min_exc))

    out = daily.copy()
    out["intraday_low"] = lows
    out.attrs["bar_days_covered"] = covered
    return out


def midpoint_boundary(daily: pd.DataFrame) -> str:
    dates = list(daily["date"])
    return pd.Timestamp(dates[len(dates) // 2]).date().isoformat()


def main() -> int:
    assert PANEL.is_file(), PANEL
    sha = _sha(PANEL)
    assert sha == PANEL_SHA, (sha, PANEL_SHA)
    assert BAR_PATH.is_file(), BAR_PATH
    assert _sha(BAR_PATH) == BAR_SHA, _sha(BAR_PATH)

    df = load_csv(PANEL)
    m = compute_metrics(df, "striker_dj30", account=INITIAL_CAPITAL)
    recompute = static_equity_recompute(df)
    mean_r = (m.net / m.n / m.r_dollars) if m.n and m.r_dollars else float("nan")
    cost_gate = {
        "net_usd": m.net,
        "n": m.n,
        "pf": m.pf,
        "wr_pct": m.wr_pct,
        "max_dd_pct": m.max_dd_pct,
        "r_basis": m.r_basis,
        "r_n_cohort": m.r_n_cohort,
        "r_dollars": m.r_dollars,
        "mean_net_r": mean_r,
        "required_net_r": REQUIRED_NET_R,
        "dead_cost_net_le_0": m.net <= 0.0,
        "beats_required_net_r": mean_r > REQUIRED_NET_R,
        "verdict": (
            "DEAD(cost)"
            if m.net <= 0.0
            else ("PASS_COST" if mean_r > REQUIRED_NET_R else "DEAD(cost)_below_required_net_r")
        ),
    }
    out = {
        "panel": PANEL.as_posix(),
        "panel_sha256": sha,
        "static_equity_recompute": recompute,
        "cost_gate": cost_gate,
    }
    (CELL / "PANEL_SCORE.json").write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"recompute": recompute, "cost_gate": cost_gate}, indent=2))
    if str(cost_gate["verdict"]).startswith("DEAD"):
        print("STOP: cost gate failed")
        return 0

    print(f"loading bars {BAR_PATH} ...")
    bars = load_bars(BAR_PATH)
    daily = build_daily(df)
    print(f"daily_n={len(daily)} bar_rows={len(bars)} bar_end={bars['date'].max().date()}")
    daily_i = attach_bar_intraday_lows(daily, bars, df)
    missing = int(daily_i["intraday_low"].isna().sum())
    print(f"missing_bar_days={missing} covered={daily_i.attrs.get('bar_days_covered')}")
    daily_i = daily_i.dropna(subset=["intraday_low"]).reset_index(drop=True)
    daily_i["intraday_low"] = daily_i["intraday_low"].clip(upper=0.0)
    boundary = midpoint_boundary(daily_i)
    daily_i.to_csv(CELL / "daily_pnl_nsurv.csv", index=False)

    from research_utils.nsurv_channel import score_nsurv

    print(f"scoring N-SURV half_boundary={boundary} n={len(daily_i)} ...")
    report = score_nsurv(daily_i, half_boundary_date=boundary)
    block = report.to_dict()
    block["half_boundary_rule"] = "midpoint-by-day-count (disclosed; not date-frozen in cell PREREG)"
    block["bars_path"] = BAR_PATH.as_posix()
    block["bars_sha256"] = BAR_SHA
    block["missing_bar_days_dropped"] = missing
    block["format_block"] = report.format_block()
    out["nsurv"] = block
    (CELL / "PANEL_SCORE.json").write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    (CELL / "NSURV_BLOCK.txt").write_text(report.format_block() + "\n", encoding="utf-8")
    print(report.format_block())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
