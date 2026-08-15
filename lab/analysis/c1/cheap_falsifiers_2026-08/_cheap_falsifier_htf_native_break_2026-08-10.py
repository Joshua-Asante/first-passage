"""Parent-side GENEROUS cheap falsifier — HTF-native 5m compression break.

Q-TNEC-CON-3 candidate. No Q-ID until CHEAP_FALSIFIER_OK.
Trade the 5m break itself (structural stop = opposite quiet extreme;
first signal per RTH session only). Distinct from CON-2 (1m/G=10) and
from HTF-bias→LTF filter (already FALSIFIED).

Kill:
  VOID-COVERAGE if too few sessions produce a break clock
  FALSIFIED if both arms powered and session-block CI entirely < 0
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CON2 = _HERE / "mnq_tnec_con2_compression_break_2026-08"
sys.path.insert(0, str(_CON2))

import construct_lib as C  # noqa: E402

PANEL = _HERE / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"

K_NARROW = 2
NARROW_MULT = 1.0
MEDIAN_SESSIONS = 20
HTF_MINUTES = 5
RT_PT = 1.41
N_MIN_ARM = 100
N_BOOT = 2000
BOOT_SEED = 20260810
BREAK_SESSION_FRAC_MIN = 0.20
COST_BAR_PT = 4.0 * RT_PT  # disclosure only

ROLL_MONTHS = (3, 6, 9, 12)
ROLL_BUFFER_DAYS = 4


def _third_friday(year: int, month: int) -> _dt.date:
    d = _dt.date(year, month, 1)
    offset = (4 - d.weekday()) % 7
    first_fri = d + _dt.timedelta(days=offset)
    return first_fri + _dt.timedelta(days=14)


def in_roll_window(day: _dt.date, buffer_days: int = ROLL_BUFFER_DAYS) -> bool:
    for yr in (day.year - 1, day.year, day.year + 1):
        for mo in ROLL_MONTHS:
            if abs((day - _third_friday(yr, mo)).days) <= buffer_days:
                return True
    return False


def sessionize_rth(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    keep = (minute >= C.RTH_OPEN_MIN) & (minute < C.RTH_CLOSE_MIN)
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


def session_median_range(ranges_by_session: list[np.ndarray], sid: int) -> float:
    if sid < MEDIAN_SESSIONS:
        return float("nan")
    chunks = ranges_by_session[sid - MEDIAN_SESSIONS : sid]
    parts = [c[c > 0] for c in chunks if len(c)]
    if not parts:
        return float("nan")
    return float(np.median(np.concatenate(parts)))


def resample_5m(grp: pd.DataFrame) -> pd.DataFrame:
    g = grp.set_index("ts_et").sort_index()
    ohlc = g.resample(f"{HTF_MINUTES}min", label="left", closed="left").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
    )
    return ohlc.dropna(subset=["open", "high", "low", "close"])


def settle_side_at_t(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
    med_rng: float,
) -> tuple[int, float, float]:
    """After HTF bar t closes: side (+1/-1/0), quiet_hi, quiet_lo.

    Compression = K_NARROW narrow bars ending at t-1; break bar = t.
    Require close beyond extreme AND on that side of midline.
    """
    if not (np.isfinite(med_rng) and med_rng > 0):
        return 0, float("nan"), float("nan")
    start = t - K_NARROW
    end_comp = t - 1
    if start < 0 or t >= len(close):
        return 0, float("nan"), float("nan")
    for i in range(start, end_comp + 1):
        rng = high[i] - low[i]
        if rng <= 0 or rng > NARROW_MULT * med_rng:
            return 0, float("nan"), float("nan")
    quiet_hi = float(np.max(high[start : end_comp + 1]))
    quiet_lo = float(np.min(low[start : end_comp + 1]))
    if quiet_hi <= quiet_lo:
        return 0, float("nan"), float("nan")
    mid = 0.5 * (quiet_hi + quiet_lo)
    c_brk = float(close[t])
    up = c_brk > quiet_hi and c_brk > mid
    dn = c_brk < quiet_lo and c_brk < mid
    if up and not dn:
        return +1, quiet_hi, quiet_lo
    if dn and not up:
        return -1, quiet_hi, quiet_lo
    return 0, float("nan"), float("nan")


def path_pts_structural(
    entry: float,
    side: int,
    stop_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str, float]:
    """Return (pts, kind, stop_dist). Same-bar stop wins; else session-flat."""
    stop_dist = abs(entry - stop_level)
    if stop_dist <= 0:
        return float("nan"), "invalid", float("nan")
    n = len(high)
    for j in range(start, n):
        if side > 0 and low[j] <= stop_level:
            return -stop_dist, "stop", stop_dist
        if side < 0 and high[j] >= stop_level:
            return -stop_dist, "stop", stop_dist
    pts = side * (float(close[n - 1]) - entry)
    return pts, "flat", stop_dist


def simulate_session_first_only(htf: pd.DataFrame, med_rng: float) -> list[dict]:
    """At most one trade: first settle → enter next 5m open."""
    if not np.isfinite(med_rng) or len(htf) < K_NARROW + 2:
        return []
    high = htf["high"].to_numpy(dtype=float)
    low = htf["low"].to_numpy(dtype=float)
    close = htf["close"].to_numpy(dtype=float)
    open_ = htf["open"].to_numpy(dtype=float)
    n = len(htf)
    for t in range(K_NARROW, n - 1):
        side, q_hi, q_lo = settle_side_at_t(high, low, close, t, med_rng)
        if side == 0:
            continue
        entry_i = t + 1
        entry = float(open_[entry_i])
        stop_level = q_lo if side > 0 else q_hi
        pts, kind, stop_dist = path_pts_structural(
            entry, side, stop_level, high, low, close, entry_i
        )
        if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
            return []
        r = (pts - RT_PT) / stop_dist
        return [
            {
                "side": side,
                "pts": pts,
                "kind": kind,
                "R": r,
                "stop_dist": stop_dist,
                "gross_pts": pts if kind == "flat" else pts,  # signed pts before RT
            }
        ]
    return []


def session_block_ci(
    session_trade_rs: list[np.ndarray], n_boot: int = N_BOOT
) -> tuple[float, float]:
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
    df = sessionize_rth(raw)
    sessions = sorted(df["session"].unique())
    ranges_5m: list[np.ndarray] = []
    sess_meta: list[object] = []
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < 60:
            continue
        htf = resample_5m(grp)
        if len(htf) < K_NARROW + 2:
            continue
        ranges_5m.append((htf["high"].to_numpy() - htf["low"].to_numpy()).astype(float))
        sess_meta.append(s)

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    gross_pts: list[float] = []
    stop_dists: list[float] = []
    n_eligible = 0
    n_break_sessions = 0

    for sid, s in enumerate(sess_meta):
        med = session_median_range(ranges_5m, sid)
        if not np.isfinite(med):
            continue
        n_eligible += 1
        htf = resample_5m(by_sess[s])
        # coverage: any settle clock (even if last bar — no entry)
        high = htf["high"].to_numpy(dtype=float)
        low = htf["low"].to_numpy(dtype=float)
        close = htf["close"].to_numpy(dtype=float)
        had_break = False
        for t in range(K_NARROW, len(htf)):
            side, _, _ = settle_side_at_t(high, low, close, t, med)
            if side != 0:
                had_break = True
                break
        if had_break:
            n_break_sessions += 1
        trades = simulate_session_first_only(htf, med)
        if not trades:
            continue
        tr = trades[0]
        gross_pts.append(float(tr["pts"]))
        stop_dists.append(float(tr["stop_dist"]))
        if tr["side"] > 0:
            long_rs.append(tr["R"])
            long_blocks.append(np.asarray([tr["R"]], dtype=float))
        else:
            short_rs.append(tr["R"])
            short_blocks.append(np.asarray([tr["R"]], dtype=float))

    def arm_summary(rs: list[float], blocks: list[np.ndarray]) -> dict:
        arr = np.asarray(rs, dtype=float)
        if len(arr) == 0:
            return {
                "n": 0,
                "mean_R": float("nan"),
                "wr": float("nan"),
                "ci_lo": float("nan"),
                "ci_hi": float("nan"),
                "stop_rate": float("nan"),
                "n_sessions": 0,
            }
        ci_lo, ci_hi = session_block_ci(blocks)
        return {
            "n": int(len(arr)),
            "mean_R": float(arr.mean()),
            "wr": float((arr > 0).mean()),
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
            "stop_rate": float(np.mean(np.asarray(rs) < 0)),  # approx; stops are negative R
            "n_sessions": int(len(blocks)),
        }

    long = arm_summary(long_rs, long_blocks)
    short = arm_summary(short_rs, short_blocks)
    break_frac = (n_break_sessions / n_eligible) if n_eligible else 0.0
    mean_gross = float(np.mean(np.abs(gross_pts))) if gross_pts else float("nan")
    mean_stop = float(np.mean(stop_dists)) if stop_dists else float("nan")
    # signed mean pts for disclosure
    mean_signed_pts = float(np.mean(gross_pts)) if gross_pts else float("nan")
    elapsed = time.perf_counter() - t0

    def arm_killed(a: dict) -> bool:
        return a["n"] >= N_MIN_ARM and np.isfinite(a["ci_hi"]) and a["ci_hi"] < 0.0

    killed = arm_killed(long) and arm_killed(short)
    underpowered = long["n"] < N_MIN_ARM and short["n"] < N_MIN_ARM
    void_cov = break_frac < BREAK_SESSION_FRAC_MIN

    if void_cov:
        verdict = "VOID-COVERAGE"
        detail = (
            f"break session frac {break_frac:.3f} < floor {BREAK_SESSION_FRAC_MIN} "
            "- do not spend Q-ID"
        )
    elif killed:
        verdict = "FALSIFIED"
        detail = (
            f"both arms session-block CI entirely < 0 at n>={N_MIN_ARM} "
            "- mechanism dead at $0"
        )
    elif underpowered:
        verdict = "VOID-UNDERPOWERED"
        detail = "first-per-session clocks too sparse under generous theta - no Q-ID"
    else:
        verdict = "CHEAP_FALSIFIER_OK"
        detail = (
            "coverage OK + not both-arms CI<0; licenses G0 freeze for "
            "Q-TNEC-CON-3 (not EXPLORATION / not SHAPE-CLEAR)"
        )

    out = {
        "family": "htf_native_5m_compression_break",
        "geometry": {
            "HTF_min": HTF_MINUTES,
            "stop": "opposite_quiet_extreme",
            "exit": "session_flat",
            "RT": RT_PT,
            "selectivity": "first_per_session",
            "EM3": True,
        },
        "thresholds": {
            "K_NARROW": K_NARROW,
            "NARROW_MULT": NARROW_MULT,
            "MEDIAN_SESSIONS": MEDIAN_SESSIONS,
            "BREAK_SESSION_FRAC_MIN": BREAK_SESSION_FRAC_MIN,
        },
        "eligible_sessions_with_theta": n_eligible,
        "break_sessions": n_break_sessions,
        "break_session_frac": break_frac,
        "n_trades": len(gross_pts),
        "mean_signed_pts": mean_signed_pts,
        "mean_abs_pts": mean_gross,
        "mean_stop_dist": mean_stop,
        "cost_bar_pt_4x": COST_BAR_PT,
        "gross_vs_4x_bar": (
            float(mean_gross / COST_BAR_PT) if np.isfinite(mean_gross) else None
        ),
        "long": long,
        "short": short,
        "elapsed_s": elapsed,
        "verdict": verdict,
        "detail": detail,
        "cost_usd": 0.0,
        "domain_bar": {
            "id": "index-intraday-ohlcv-directional-timing-2026-07-21",
            "route": "1_temporal_selectivity_ADR_2026-08-10",
            "mechanism": "htf-compression-breakout-5m",
        },
    }
    out_path = _HERE / "_cheap_falsifier_htf_native_break_2026-08-10_RESULTS.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("=== Q-TNEC-CON-3 candidate: HTF-native 5m compression break ===")
    print(f"panel: {PANEL}")
    print(
        f"geometry: 5m native · structural stop · first/session · "
        f"session-flat · RT={RT_PT}"
    )
    print(f"eligible_sessions_with_theta: {n_eligible}")
    print(f"break_sessions: {n_break_sessions} ({break_frac:.3f})")
    print(f"n_trades: {len(gross_pts)}")
    print(
        f"mean_signed_pts: {mean_signed_pts:.4f}  mean_abs_pts: {mean_gross:.4f}  "
        f"vs 4x bar {COST_BAR_PT}: "
        f"{(mean_gross / COST_BAR_PT) if np.isfinite(mean_gross) else float('nan'):.3f}x"
    )
    print(f"mean_stop_dist: {mean_stop:.4f}")
    print(f"long:  {long}")
    print(f"short: {short}")
    print(f"elapsed_s: {elapsed:.2f}")
    print(f"VERDICT: {verdict}")
    print(f"detail: {detail}")
    print(f"wrote: {out_path}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
