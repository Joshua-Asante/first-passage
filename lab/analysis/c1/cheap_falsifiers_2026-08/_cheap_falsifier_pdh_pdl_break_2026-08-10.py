"""Parent-side GENEROUS cheap falsifier — PDH/PDL RTH with-break (CON-4 candidate).

Mechanism id: pdh-pdl-breakout-rth. No Q-ID until CHEAP_FALSIFIER_OK.
First close beyond prior-RTH high (long) or low (short) → enter next 1m open;
structural stop at opposite prior extreme; first signal/session; session-flat; RT 1.41.

Distinct from CON-2/3 compression family, ORB, MNQPROX (OF approach contrast),
and N9/C10 level-touch attraction (this is through-break, not fade).

Kill:
  VOID-COVERAGE if break-session frac < 0.20
  FALSIFIED if both arms powered (n>=100) and session-block CI entirely < 0
"""
from __future__ import annotations

import datetime as _dt
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
PANEL = _HERE / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"

RT_PT = 1.41
N_MIN_ARM = 100
N_BOOT = 2000
BOOT_SEED = 20260810
BREAK_SESSION_FRAC_MIN = 0.20
RTH_OPEN_MIN = 9 * 60 + 30
RTH_CLOSE_MIN = 16 * 60
COST_BAR_PT = 4.0 * RT_PT

ROLL_MONTHS = (3, 6, 9, 12)
ROLL_BUFFER_DAYS = 4


def _third_friday(year: int, month: int) -> _dt.date:
    d = _dt.date(year, month, 1)
    offset = (4 - d.weekday()) % 7
    return d + _dt.timedelta(days=offset + 14)


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


def path_pts_structural(
    entry: float,
    side: int,
    stop_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str, float]:
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


def first_pdh_pdl_trade(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    pdh: float,
    pdl: float,
) -> dict | None:
    """First close beyond PDH/PDL → enter next open; stop at opposite extreme."""
    if not (np.isfinite(pdh) and np.isfinite(pdl) and pdh > pdl):
        return None
    n = len(close)
    for t in range(n - 1):
        c = float(close[t])
        side = 0
        stop_level = float("nan")
        if c > pdh:
            side = +1
            stop_level = pdl
        elif c < pdl:
            side = -1
            stop_level = pdh
        else:
            continue
        entry_i = t + 1
        entry = float(open_[entry_i])
        pts, kind, stop_dist = path_pts_structural(
            entry, side, stop_level, high, low, close, entry_i
        )
        if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
            return None
        return {
            "side": side,
            "pts": pts,
            "kind": kind,
            "R": (pts - RT_PT) / stop_dist,
            "stop_dist": stop_dist,
        }
    return None


def session_had_break(close: np.ndarray, pdh: float, pdl: float) -> bool:
    if not (np.isfinite(pdh) and np.isfinite(pdl) and pdh > pdl):
        return False
    return bool(np.any(close > pdh) or np.any(close < pdl))


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
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    # Build prior-RTH H/L map (skip roll windows for both prior and current)
    prior_hl: dict = {}
    ordered: list = []
    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < 60:
            continue
        ordered.append(s)
        prior_hl[s] = (
            float(grp["high"].max()),
            float(grp["low"].min()),
        )

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    gross_pts: list[float] = []
    stop_dists: list[float] = []
    n_eligible = 0
    n_break_sessions = 0

    for i, s in enumerate(ordered):
        if i == 0:
            continue  # no prior session
        prev = ordered[i - 1]
        pdh, pdl = prior_hl[prev]
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        n_eligible += 1
        if session_had_break(c, pdh, pdl):
            n_break_sessions += 1
        tr = first_pdh_pdl_trade(o, h, lo, c, pdh, pdl)
        if tr is None:
            continue
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
            }
        ci_lo, ci_hi = session_block_ci(blocks)
        return {
            "n": int(len(arr)),
            "mean_R": float(arr.mean()),
            "wr": float((arr > 0).mean()),
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
        }

    long = arm_summary(long_rs, long_blocks)
    short = arm_summary(short_rs, short_blocks)
    break_frac = (n_break_sessions / n_eligible) if n_eligible else 0.0
    mean_signed_pts = float(np.mean(gross_pts)) if gross_pts else float("nan")
    mean_stop = float(np.mean(stop_dists)) if stop_dists else float("nan")
    elapsed = time.perf_counter() - t0

    def arm_killed(a: dict) -> bool:
        return a["n"] >= N_MIN_ARM and np.isfinite(a["ci_hi"]) and a["ci_hi"] < 0.0

    killed = arm_killed(long) and arm_killed(short)
    void_cov = break_frac < BREAK_SESSION_FRAC_MIN

    if void_cov:
        verdict = "VOID-COVERAGE"
        detail = (
            f"break session frac {break_frac:.3f} < floor {BREAK_SESSION_FRAC_MIN}"
        )
    elif killed:
        verdict = "FALSIFIED"
        detail = "both arms n>=100 and session-block CI entirely < 0"
    else:
        verdict = "CHEAP_FALSIFIER_OK"
        detail = (
            "coverage clears; not both-arms CI<0 under PDH/PDL with-break / "
            "structural opposite-extreme stop / first-per-session"
        )

    out = {
        "verdict": verdict,
        "detail": detail,
        "mechanism_id": "pdh-pdl-breakout-rth",
        "n_eligible_sessions": n_eligible,
        "n_break_sessions": n_break_sessions,
        "break_frac": break_frac,
        "n_trades": len(gross_pts),
        "mean_signed_pts": mean_signed_pts,
        "mean_stop_dist": mean_stop,
        "gross_vs_4x_rt": (
            (mean_signed_pts / COST_BAR_PT) if np.isfinite(mean_signed_pts) else None
        ),
        "long": long,
        "short": short,
        "elapsed_s": elapsed,
        "cost_usd": 0.0,
        "panel": str(PANEL),
    }
    stamp = "2026-08-10"
    results_path = _HERE / f"_cheap_falsifier_pdh_pdl_break_{stamp}_RESULTS.json"
    results_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print(f"WROTE {results_path}")
    print(f"VERDICT {verdict}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
