"""P1-CF / P2-CF -- six-lead pursuit plan cheap falsifiers, 2026-08-17.

Design frozen in docs/briefs/programs/2026-08-17-six-lead-pursuit-plan.md Sec4
("P1-CF / P2-CF design freeze") before this script was written -- segmentation,
roll-handling, session boundary, and stop-sizing were fixed a priori.

P1-CF (L3=L6, overnight-reversal): fade the overnight gap
  (session_close[D-1] -> session_open[D]), enter at D's reopen bar close,
  exit at D's session close (16:00 ET) or hard-stop, whichever first.

P2-CF (L1, index-flow reversal): fade the FULL prior session's move
  (session_open[D-1] -> session_close[D-1]) -- the "venue-expressible slice",
  not raw close-to-close autocorrelation -- entered/exited identically to P1.

Session boundary: trade_date bucketing at 18:00 ET (CME Globex reopen after
the daily maintenance halt) -> 16:00 ET (E1 flat default, confirmed in
ops/prop_envelope_default.md). Holiday-short (12:59 ET) handling NOT applied
here -- flagged in the design freeze as unchecked against a current CME
calendar; this run uses the uniform 16:00 ET cutoff and reports the
(small, expected) exposure this leaves.

Roll handling: TV `1!` volume-lead continuous panels carry no contract-month
field, so roll days are detected as overnight-return outliers (|z| > 5 on the
instrument's own overnight-return distribution) rather than a calendar rule --
documented in the design freeze as a data-driven proxy, not the frozen
ROLL-EXCLUDE-2026-07-31 ruling (which governs MCL/M2K/MYM only).

Cost: commission $0.91/side (the third-leg-map figure reused across
M6A/MGC/MCL ledgers) + 1 tick total slippage, RT cost per contract:
  MGC: 2*0.91 + 1*$1.00   = $2.82
  6J:  2*0.91 + 1*$6.25   = $8.07
Pass bar: gross mean $/trade >= 4x RT cost (COST-MULT-4X, the standing
Req-5 convention used throughout this repo).
"""
from __future__ import annotations

import math
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[4] / "core" / "data" / "bar_data"
OUT_DIR = Path(__file__).resolve().parent

ET = ZoneInfo("America/New_York")

INSTRUMENTS = {
    "MGC": {
        "file": "MGC_M15.csv",
        "commission_per_side": 0.91,
        "mintick": 0.1,
        "pointvalue": 10.0,  # $/price-point, from MGC_M15.meta.json
    },
    "6J": {
        "file": "6J_M15.csv",
        "commission_per_side": 0.91,
        "mintick": 5e-07,
        "pointvalue": 12_500_000.0,  # from 6J_M15.meta.json
    },
}


def tick_value(sym: str) -> float:
    spec = INSTRUMENTS[sym]
    return spec["mintick"] * spec["pointvalue"]


def point_value(sym: str) -> float:
    return INSTRUMENTS[sym]["pointvalue"]

STOP_ATR_MULT = 1.5
ATR_LOOKBACK_SESSIONS = 20
ROLL_OUTLIER_Z = 5.0


def load_panel(sym: str) -> pd.DataFrame:
    path = DATA_DIR / INSTRUMENTS[sym]["file"]
    df = pd.read_csv(path)
    df["time_utc"] = pd.to_datetime(df["time"], utc=True)
    df["time_et"] = df["time_utc"].dt.tz_convert(ET)
    # Trade-date bucketing: bars from 18:00 ET onward belong to the NEXT
    # calendar date's session (the reopen after the daily maintenance halt).
    shifted = df["time_et"] + pd.Timedelta(hours=6)
    df["trade_date"] = shifted.dt.date
    return df.sort_values("time_utc").reset_index(drop=True)


def build_sessions(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for trade_date, g in df.groupby("trade_date", sort=True):
        g = g.sort_values("time_utc")
        close_mask = g["time_et"].dt.hour < 16
        close_eligible = g[close_mask]
        if close_eligible.empty:
            # No bar strictly before 16:00 ET local hour -- fall back to the
            # bar at exactly 16:00 if present, else skip (rare partial session).
            at_1600 = g[(g["time_et"].dt.hour == 16) & (g["time_et"].dt.minute == 0)]
            if at_1600.empty:
                continue
            close_row = at_1600.iloc[-1]
        else:
            close_row = close_eligible.iloc[-1]
        open_row = g.iloc[0]
        session_high = g["high"].max()
        session_low = g["low"].min()
        rows.append(
            {
                "trade_date": trade_date,
                "open_time": open_row["time_utc"],
                "open_price": open_row["open"],
                "close_time": close_row["time_utc"],
                "close_price": close_row["close"],
                "session_high": session_high,
                "session_low": session_low,
            }
        )
    sess = pd.DataFrame(rows).sort_values("trade_date").reset_index(drop=True)
    sess["prior_close_price"] = sess["close_price"].shift(1)
    sess["prior_open_price"] = sess["open_price"].shift(1)
    sess["overnight_ret"] = np.log(sess["open_price"] / sess["prior_close_price"])
    sess["prior_session_ret"] = np.log(sess["prior_close_price"] / sess["prior_open_price"])
    sess["true_range"] = sess["session_high"] - sess["session_low"]
    sess["atr20"] = sess["true_range"].rolling(ATR_LOOKBACK_SESSIONS, min_periods=5).mean().shift(1)
    return sess


def flag_roll_outliers(sess: pd.DataFrame) -> pd.Series:
    r = sess["overnight_ret"]
    mu, sigma = r.mean(), r.std()
    z = (r - mu) / sigma
    return z.abs() > ROLL_OUTLIER_Z


def run_construct(sym: str, sess: pd.DataFrame, df: pd.DataFrame, construct: str) -> dict:
    """construct: 'P1' fades overnight_ret, 'P2' fades prior_session_ret."""
    rt_cost = 2 * INSTRUMENTS[sym]["commission_per_side"] + 1 * tick_value(sym)
    pv = point_value(sym)

    roll_outlier = flag_roll_outliers(sess)
    trades = []
    n_excluded_roll = 0
    n_no_stop_data = 0

    signal_col = "overnight_ret" if construct == "P1" else "prior_session_ret"

    for i in range(1, len(sess)):
        row = sess.iloc[i]
        if pd.isna(row[signal_col]) or pd.isna(row["atr20"]):
            continue
        if roll_outlier.iloc[i]:
            n_excluded_roll += 1
            continue
        sig = row[signal_col]
        if sig == 0:
            continue
        direction = -1.0 if sig > 0 else 1.0  # fade

        # Entry at the reopen bar's own open: the fade signal (vs. the prior
        # session's close, or the prior session's own open-to-close move) is
        # fully determined the instant this session's first print appears.
        entry_price = row["open_price"]
        stop_dist = STOP_ATR_MULT * row["atr20"]
        if stop_dist <= 0 or pd.isna(stop_dist):
            n_no_stop_data += 1
            continue
        stop_price = entry_price - direction * stop_dist  # adverse side

        # Scan intraday bars for a stop breach between open and close (inclusive).
        day_bars = df[
            (df["trade_date"] == row["trade_date"])
            & (df["time_utc"] >= row["open_time"])
            & (df["time_utc"] <= row["close_time"])
        ]
        exit_price = row["close_price"]
        stopped = False
        for _, b in day_bars.iterrows():
            if direction > 0 and b["low"] <= stop_price:
                exit_price = stop_price
                stopped = True
                break
            if direction < 0 and b["high"] >= stop_price:
                exit_price = stop_price
                stopped = True
                break

        raw_ret = direction * (exit_price - entry_price)
        gross_usd = raw_ret * pv
        net_usd = gross_usd - rt_cost
        r_multiple = raw_ret / stop_dist if stop_dist else np.nan

        trades.append(
            {
                "trade_date": row["trade_date"],
                "direction": direction,
                "signal": sig,
                "stopped": stopped,
                "raw_ret_pts": raw_ret,
                "gross_usd": gross_usd,
                "net_usd": net_usd,
                "r_multiple": r_multiple,
            }
        )

    tdf = pd.DataFrame(trades)
    n = len(tdf)
    result = {
        "symbol": sym,
        "construct": construct,
        "n_trades": n,
        "n_excluded_roll_outlier": n_excluded_roll,
        "n_excluded_no_stop_data": n_no_stop_data,
        "n_sessions_total": len(sess),
    }
    if n == 0:
        result.update({"win_rate": None, "mean_gross_usd": None, "mean_net_usd": None,
                        "sum_net_usd": None, "t_stat_net": None, "vs_4x_hurdle": None})
        return result, tdf

    win_rate = (tdf["net_usd"] > 0).mean()
    mean_gross = tdf["gross_usd"].mean()
    mean_net = tdf["net_usd"].mean()
    sum_net = tdf["net_usd"].sum()
    se = tdf["net_usd"].std(ddof=1) / math.sqrt(n) if n > 1 else float("nan")
    t_stat = mean_net / se if se and not math.isnan(se) and se != 0 else float("nan")
    hurdle_4x = 4 * rt_cost
    result.update(
        {
            "rt_cost_usd": rt_cost,
            "hurdle_4x_usd": hurdle_4x,
            "win_rate": win_rate,
            "mean_gross_usd": mean_gross,
            "mean_net_usd": mean_net,
            "sum_net_usd": sum_net,
            "t_stat_net": t_stat,
            "vs_4x_hurdle": mean_gross / hurdle_4x if hurdle_4x else float("nan"),
        }
    )
    return result, tdf


def main() -> None:
    all_results = []
    for sym in INSTRUMENTS:
        df = load_panel(sym)
        sess = build_sessions(df)
        for construct in ("P1", "P2"):
            result, tdf = run_construct(sym, sess, df, construct)
            all_results.append(result)
            tdf.to_csv(OUT_DIR / f"trades_{construct}_{sym}.csv", index=False)
            print(f"=== {construct} x {sym} ===")
            for k, v in result.items():
                print(f"  {k}: {v}")
            print()

    pd.DataFrame(all_results).to_csv(OUT_DIR / "SUMMARY.csv", index=False)


if __name__ == "__main__":
    main()
