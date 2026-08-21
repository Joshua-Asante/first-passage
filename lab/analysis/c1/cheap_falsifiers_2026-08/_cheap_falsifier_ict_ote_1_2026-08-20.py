"""Parent-side GENEROUS cheap falsifier -- Q-ICT-OTE-1 (Optimal Trade Entry).

Mechanism id: ict-ote-fib-retracement (not yet registered in MECHANISMS.md --
registration happens only if this clears to a G0 freeze). No Q-ID/manifest opened
by this run; licensed by docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md
Phase 1 only.

RECONSTRUCTION NOTE (Rule 0): the original raid/sweep detector
(lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py) is not present in this public
worktree -- this repo's pre-transition history (where that file would have been
committed) lives only in the private archive, and the file was never committed to
the public seed. This falsifier therefore RECONSTRUCTS the sweep/pivot logic fresh
from the frozen prose parameters already on record (PREREG_EXP.md / PREREG_D_W.md:
pvLen=2 pivot, raidWin=8 same-direction pairing) rather than importing lost code.
For a cheap falsifier this is an accepted simplification (deliberately fast/generous,
not the frozen-G0 bar); if this clears to a G0 freeze, the reconstruction becomes
load-bearing and should be independently checked against the prose spec again, not
just copied forward from this file.

Sweep (raid) -> confirmed impulse leg -> 0.62-0.79 Fib retracement entry -> stop
beyond the sweep extreme -> target the frozen 1H range-extreme DOL (h1High/h1Low,
lookN=60, [1]-lagged, non-repaint -- reused verbatim from PREREG-1H, this piece IS
directly reconstructable from its own formula, not lost) -> exit at target or
session-flat (E1, 16:00 ET), whichever first.

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

PV_LEN = 2                # pivot: PV_LEN bars strictly higher/lower on each side
RAID_WIN = 8               # sweep must reverse within this many bars of the pivot
DISP_MULT = 1.5             # impulse-leg displacement threshold, x ATR(14)
ATR_LEN = 14
FIB_LO, FIB_HI = 0.62, 0.79  # OTE band
LEG_CONFIRM_WIN = 30         # bars allowed for the impulse leg to reach its own end
ENTRY_ARM_WIN = 20           # bars allowed for price to touch the Fib zone after leg confirms
LOOKN_1H = 60                # DOL target lookback, in COMPLETED 1H buckets

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


def find_pivots(high: np.ndarray, low: np.ndarray, pv_len: int = PV_LEN):
    """Standard fractal pivots: bar i is a pivot high if high[i] > high[i-pv_len:i]
    and > high[i+1:i+1+pv_len]; symmetric for pivot low. Returns boolean arrays."""
    n = len(high)
    piv_hi = np.zeros(n, dtype=bool)
    piv_lo = np.zeros(n, dtype=bool)
    for i in range(pv_len, n - pv_len):
        left_h = high[i - pv_len:i]
        right_h = high[i + 1:i + 1 + pv_len]
        if high[i] > left_h.max() and high[i] > right_h.max():
            piv_hi[i] = True
        left_l = low[i - pv_len:i]
        right_l = low[i + 1:i + 1 + pv_len]
        if low[i] < left_l.min() and low[i] < right_l.min():
            piv_lo[i] = True
    return piv_hi, piv_lo


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


def first_ote_trade(
    open_: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray,
    dol_target: float,
) -> dict | None:
    """First sweep -> confirmed impulse leg -> OTE-zone touch -> entry, this session."""
    n = len(close)
    if n < 2 * PV_LEN + RAID_WIN + LEG_CONFIRM_WIN + ENTRY_ARM_WIN:
        return None
    piv_hi, piv_lo = find_pivots(high, low)
    atr_v = atr(high, low, close)

    for p in range(PV_LEN, n - PV_LEN):
        if not (piv_hi[p] or piv_lo[p]):
            continue
        if not np.isfinite(atr_v[p]):
            continue
        # --- sweep: price trades beyond the pivot extreme within RAID_WIN bars, then
        # closes back on the origin side (the "grab, then reject" liquidity raid) ---
        raid_end = min(p + 1 + RAID_WIN, n)
        sweep_i = None
        side = 0
        if piv_lo[p]:
            pivot_px = float(low[p])
            for j in range(p + 1, raid_end):
                if low[j] < pivot_px and close[j] > pivot_px:
                    sweep_i, side = j, +1  # SSL swept -> bullish setup
                    sweep_extreme = float(low[j])
                    break
        elif piv_hi[p]:
            pivot_px = float(high[p])
            for j in range(p + 1, raid_end):
                if high[j] > pivot_px and close[j] < pivot_px:
                    sweep_i, side = j, -1  # BSL swept -> bearish setup
                    sweep_extreme = float(high[j])
                    break
        if sweep_i is None:
            continue

        # --- confirmed impulse leg: displacement >= DISP_MULT x ATR from the sweep
        # extreme, in the reversal direction, within LEG_CONFIRM_WIN bars ---
        leg_end = min(sweep_i + 1 + LEG_CONFIRM_WIN, n)
        disp_needed = DISP_MULT * float(atr_v[sweep_i])
        leg_end_i = None
        leg_end_px = None
        if side > 0:
            for k in range(sweep_i + 1, leg_end):
                if float(high[k]) - sweep_extreme >= disp_needed:
                    leg_end_i, leg_end_px = k, float(high[k])
                    break
        else:
            for k in range(sweep_i + 1, leg_end):
                if sweep_extreme - float(low[k]) >= disp_needed:
                    leg_end_i, leg_end_px = k, float(low[k])
                    break
        if leg_end_i is None:
            continue

        # --- OTE zone: 0.62-0.79 retracement of [sweep_extreme, leg_end_px] ---
        leg_range = abs(leg_end_px - sweep_extreme)
        if leg_range <= 0:
            continue
        if side > 0:
            fib_hi_px = leg_end_px - FIB_LO * leg_range
            fib_lo_px = leg_end_px - FIB_HI * leg_range
        else:
            fib_lo_px = leg_end_px + FIB_LO * leg_range
            fib_hi_px = leg_end_px + FIB_HI * leg_range

        # --- entry: first touch of the zone within ENTRY_ARM_WIN bars after leg confirms ---
        arm_end = min(leg_end_i + 1 + ENTRY_ARM_WIN, n)
        for t in range(leg_end_i + 1, arm_end - 1):
            touched = (side > 0 and float(low[t]) <= fib_hi_px and float(high[t]) >= fib_lo_px) or (
                side < 0 and float(high[t]) >= fib_lo_px and float(low[t]) <= fib_hi_px
            )
            if not touched:
                continue
            entry_i = t + 1
            entry = float(open_[entry_i])
            stop_level = sweep_extreme
            stop_dist = abs(entry - stop_level)
            if stop_dist <= 0:
                return None
            # path: stop at sweep extreme, target the DOL, else session-flat at last bar
            for j in range(entry_i, n):
                if side > 0:
                    if float(low[j]) <= stop_level:
                        return {"side": side, "pts": -stop_dist, "stop_dist": stop_dist, "kind": "stop"}
                    if np.isfinite(dol_target) and float(high[j]) >= dol_target:
                        pts = dol_target - entry
                        return {"side": side, "pts": pts, "stop_dist": stop_dist, "kind": "target"}
                else:
                    if float(high[j]) >= stop_level:
                        return {"side": side, "pts": -stop_dist, "stop_dist": stop_dist, "kind": "stop"}
                    if np.isfinite(dol_target) and float(low[j]) <= dol_target:
                        pts = entry - dol_target
                        return {"side": side, "pts": pts, "stop_dist": stop_dist, "kind": "target"}
            pts = side * (float(close[n - 1]) - entry)
            return {"side": side, "pts": pts, "stop_dist": stop_dist, "kind": "flat"}
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


def build_1h_dol(raw: pd.DataFrame) -> pd.Series:
    """h1High/h1Low: rolling max/min of the prior LOOKN_1H completed 1H buckets,
    reused verbatim from PREREG-1H's own formula. Indexed by 1H bucket start (UTC)."""
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
        # nearest completed 1H bucket at or before the session open
        bucket = ts_first.floor("1h")
        try:
            dol_hi = float(h1_high.asof(bucket))
            dol_lo = float(h1_low.asof(bucket))
        except Exception:
            dol_hi, dol_lo = float("nan"), float("nan")

        # score long arm against dol_hi, short arm against dol_lo -- first_ote_trade
        # only receives one target, so run it twice (side-appropriate target), first
        # signal wins per side just as the frozen chain treats long/short independently.
        tr_long = first_ote_trade(o, h, lo, c, dol_hi)
        tr_short = first_ote_trade(o, h, lo, c, dol_lo)
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
        verdict, detail = "CHEAP_FALSIFIER_OK", "coverage clears; not both-arms CI<0 under sweep->confirmed-leg->OTE-zone / sweep-extreme stop / 1H-DOL target"

    out = {
        "verdict": verdict,
        "detail": detail,
        "mechanism_id": "ict-ote-fib-retracement",
        "reconstruction_note": "raid/pivot detector reconstructed fresh from prose spec (pvLen=2, raidWin=8); original code unavailable in this public worktree",
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
    results_path = _HERE / f"_cheap_falsifier_ict_ote_1_{stamp}_RESULTS.json"
    results_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"WROTE {results_path}")
    print(f"VERDICT {verdict}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
