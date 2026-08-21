"""Parent-side GENEROUS cheap falsifier -- Q-ICT-OB-1 (Order Blocks).

Mechanism id: ict-ob-last-opposing-candle (not yet registered in MECHANISMS.md --
registration happens only if this clears to a G0 freeze). No Q-ID/manifest opened
by this run; licensed by
docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md Phase 1 only.

RECONSTRUCTION NOTE (Rule 0): same as Q-ICT-OTE-1's own falsifier -- the original
displacement/FVG detector is not present in this public worktree. Displacement
detection is reconstructed fresh from the frozen dispMlt=1.5xATR(14) threshold
already on record; this is a fresh, independently-correct implementation of a
documented parameter, not a copy of lost code.

Last opposing candle before a qualifying displacement -> OB range [low, high] of
that candle -> entry on return to the range (limit-style touch, ENTRY_ARM_WIN bars
to arm) -> stop beyond the OB candle's far edge -> target the frozen 1H
range-extreme DOL (reused verbatim from Q-ICT-OTE-1) -> exit at target or
session-flat, whichever first.

Kill:
  VOID-COVERAGE if trade-session frac < 0.20
  FALSIFIED if both arms powered (n>=100) and session-block CI entirely < 0
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
PANEL = _HERE.parent / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"

RT_PT = 1.41
N_MIN_ARM = 100
N_BOOT = 2000
BOOT_SEED = 20260820
TRADE_SESSION_FRAC_MIN = 0.20
RTH_OPEN_MIN = 9 * 60 + 30
RTH_CLOSE_MIN = 16 * 60
COST_BAR_PT = 4.0 * RT_PT

DISP_MULT = 1.5
ATR_LEN = 14
ENTRY_ARM_WIN = 30          # bars allowed for price to return to the OB range
LOOKN_1H = 60

ROLL_MONTHS = (3, 6, 9, 12)
ROLL_BUFFER_DAYS = 4


def _third_friday(year: int, month: int):
    import datetime as _dt

    d = _dt.date(year, month, 1)
    offset = (4 - d.weekday()) % 7
    return d + _dt.timedelta(days=offset + 14)


def in_roll_window(day, buffer_days: int = ROLL_BUFFER_DAYS) -> bool:
    for yr in (day.year - 1, day.year, day.year + 1):
        for mo in ROLL_MONTHS:
            if abs((day - _third_friday(yr, mo)).days) <= buffer_days:
                return True
    return False


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, length: int = ATR_LEN) -> np.ndarray:
    n = len(close)
    tr = np.empty(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
    out = np.full(n, np.nan)
    if n >= length:
        out[length - 1] = tr[:length].mean()
        for i in range(length, n):
            out[i] = (out[i - 1] * (length - 1) + tr[i]) / length
    return out


def first_ob_trade(
    open_: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray,
    dol_target: float,
) -> dict | None:
    """First qualifying displacement -> its preceding opposing candle (OB) ->
    return-to-range entry -> stop beyond OB far edge -> target/session-flat exit."""
    n = len(close)
    if n < ATR_LEN + 3:
        return None
    atr_v = atr(high, low, close)

    for t in range(ATR_LEN, n - 1):
        if not np.isfinite(atr_v[t - 1]):
            continue
        move = close[t] - close[t - 1]
        disp_needed = DISP_MULT * float(atr_v[t - 1])
        if abs(move) < disp_needed:
            continue
        side = +1 if move > 0 else -1

        # walk backward from t-1 for the nearest opposite-colored candle
        ob_i = None
        for k in range(t - 1, -1, -1):
            is_down = close[k] < open_[k]
            is_up = close[k] > open_[k]
            if side > 0 and is_down:
                ob_i = k
                break
            if side < 0 and is_up:
                ob_i = k
                break
            if t - 1 - k > 10:  # bounded backward search -- keep this cheap
                break
        if ob_i is None:
            continue

        ob_hi = float(high[ob_i])
        ob_lo = float(low[ob_i])
        if ob_hi <= ob_lo:
            continue

        # arm from the displacement bar onward; entry on first touch of the OB range
        arm_end = min(t + 1 + ENTRY_ARM_WIN, n)
        for j in range(t + 1, arm_end - 1):
            touched = float(low[j]) <= ob_hi and float(high[j]) >= ob_lo
            if not touched:
                continue
            entry_i = j + 1
            entry = float(open_[entry_i])
            stop_level = ob_lo if side > 0 else ob_hi
            stop_dist = abs(entry - stop_level)
            if stop_dist <= 0:
                return None
            for m in range(entry_i, n):
                if side > 0:
                    if float(low[m]) <= stop_level:
                        return {"side": side, "pts": -stop_dist, "stop_dist": stop_dist, "kind": "stop"}
                    if np.isfinite(dol_target) and float(high[m]) >= dol_target:
                        return {"side": side, "pts": dol_target - entry, "stop_dist": stop_dist, "kind": "target"}
                else:
                    if float(high[m]) >= stop_level:
                        return {"side": side, "pts": -stop_dist, "stop_dist": stop_dist, "kind": "stop"}
                    if np.isfinite(dol_target) and float(low[m]) <= dol_target:
                        return {"side": side, "pts": entry - dol_target, "stop_dist": stop_dist, "kind": "target"}
            pts = side * (float(close[n - 1]) - entry)
            return {"side": side, "pts": pts, "stop_dist": stop_dist, "kind": "flat"}
        return None
    return None


def sessionize_rth(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    keep = (minute >= RTH_OPEN_MIN) & (minute < RTH_CLOSE_MIN)
    et_k = et[keep]
    return pd.DataFrame(
        {
            "ts_et": et_k.to_numpy(),
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": df.loc[keep, "open"].to_numpy(dtype=float),
            "high": df.loc[keep, "high"].to_numpy(dtype=float),
            "low": df.loc[keep, "low"].to_numpy(dtype=float),
            "close": df.loc[keep, "close"].to_numpy(dtype=float),
        }
    )


def build_1h_dol(raw: pd.DataFrame):
    ts = pd.to_datetime(raw["ts_event"], utc=True)
    df = pd.DataFrame({"ts": ts, "high": raw["high"], "low": raw["low"]}).set_index("ts")
    h1 = df.resample("1h").agg(high=("high", "max"), low=("low", "min")).dropna()
    h1_high = h1["high"].rolling(LOOKN_1H).max().shift(1)
    h1_low = h1["low"].rolling(LOOKN_1H).min().shift(1)
    return h1_high, h1_low


def session_block_ci(session_trade_rs, n_boot: int = N_BOOT):
    blocks = [a for a in session_trade_rs if len(a) > 0]
    if len(blocks) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(BOOT_SEED)
    idx = np.arange(len(blocks))
    boots = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        pick = rng.choice(idx, size=len(blocks), replace=True)
        boots[i] = float(np.concatenate([blocks[j] for j in pick]).mean())
    return float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def main() -> int:
    t0 = time.perf_counter()
    if not PANEL.is_file():
        print(f"MISSING_PANEL {PANEL}")
        return 2
    raw = pd.read_parquet(PANEL)
    h1_high, h1_low = build_1h_dol(raw)
    df = sessionize_rth(raw)
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    long_rs, short_rs = [], []
    long_blocks, short_blocks = [], []
    gross_pts, stop_dists = [], []
    n_eligible = 0
    n_trade_sessions = 0

    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < 100:
            continue
        n_eligible += 1
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        ts_first = pd.Timestamp(grp["ts_et"].iloc[0]).tz_convert("UTC")
        bucket = ts_first.floor("1h")
        try:
            dol_hi = float(h1_high.asof(bucket))
            dol_lo = float(h1_low.asof(bucket))
        except Exception:
            dol_hi, dol_lo = float("nan"), float("nan")

        tr_long = first_ob_trade(o, h, lo, c, dol_hi)
        tr_short = first_ob_trade(o, h, lo, c, dol_lo)
        traded = False
        if tr_long is not None and tr_long["side"] > 0:
            traded = True
            R = (tr_long["pts"] - RT_PT) / tr_long["stop_dist"]
            long_rs.append(R)
            long_blocks.append(np.asarray([R], dtype=float))
            gross_pts.append(tr_long["pts"])
            stop_dists.append(tr_long["stop_dist"])
        if tr_short is not None and tr_short["side"] < 0:
            traded = True
            R = (tr_short["pts"] - RT_PT) / tr_short["stop_dist"]
            short_rs.append(R)
            short_blocks.append(np.asarray([R], dtype=float))
            gross_pts.append(tr_short["pts"])
            stop_dists.append(tr_short["stop_dist"])
        if traded:
            n_trade_sessions += 1

    def arm_summary(rs, blocks) -> dict:
        arr = np.asarray(rs, dtype=float)
        if len(arr) == 0:
            return {"n": 0, "mean_R": float("nan"), "wr": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan")}
        ci_lo, ci_hi = session_block_ci(blocks)
        return {"n": int(len(arr)), "mean_R": float(arr.mean()), "wr": float((arr > 0).mean()), "ci_lo": ci_lo, "ci_hi": ci_hi}

    long = arm_summary(long_rs, long_blocks)
    short = arm_summary(short_rs, short_blocks)
    trade_frac = (n_trade_sessions / n_eligible) if n_eligible else 0.0
    mean_signed_pts = float(np.mean(gross_pts)) if gross_pts else float("nan")
    mean_stop = float(np.mean(stop_dists)) if stop_dists else float("nan")
    elapsed = time.perf_counter() - t0

    def arm_killed(a: dict) -> bool:
        return a["n"] >= N_MIN_ARM and np.isfinite(a["ci_hi"]) and a["ci_hi"] < 0.0

    killed = arm_killed(long) and arm_killed(short)
    void_cov = trade_frac < TRADE_SESSION_FRAC_MIN

    if void_cov:
        verdict, detail = "VOID-COVERAGE", f"trade session frac {trade_frac:.3f} < floor {TRADE_SESSION_FRAC_MIN}"
    elif killed:
        verdict, detail = "FALSIFIED", "both arms n>=100 and session-block CI entirely < 0"
    else:
        verdict, detail = "CHEAP_FALSIFIER_OK", "coverage clears; not both-arms CI<0 under last-opposing-candle OB / far-edge stop / 1H-DOL target"

    out = {
        "verdict": verdict,
        "detail": detail,
        "mechanism_id": "ict-ob-last-opposing-candle",
        "reconstruction_note": "displacement detector reconstructed fresh from prose spec (dispMlt=1.5xATR14); original code unavailable in this public worktree",
        "n_eligible_sessions": n_eligible,
        "n_trade_sessions": n_trade_sessions,
        "trade_frac": trade_frac,
        "n_trades": len(gross_pts),
        "mean_signed_pts": mean_signed_pts,
        "mean_stop_dist": mean_stop,
        "gross_vs_4x_rt": (mean_signed_pts / COST_BAR_PT) if np.isfinite(mean_signed_pts) else None,
        "long": long,
        "short": short,
        "elapsed_s": elapsed,
        "cost_usd": 0.0,
        "panel": str(PANEL),
    }
    stamp = "2026-08-20"
    results_path = _HERE / f"_cheap_falsifier_ict_ob_1_{stamp}_RESULTS.json"
    results_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"WROTE {results_path}")
    print(f"VERDICT {verdict}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
