"""Parent-side GENEROUS cheap falsifier — displacement fade on MNQSEL-2 panel.

No Q-ID. $0. Failure is conclusive (both arms CI entirely < 0 at powered n).
Pass licenses G0 authoring for Q-TNEC-CON-2; does NOT score EXPLORATION.
"""
from __future__ import annotations

import datetime as _dt
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_CON1 = _HERE / "mnq_con1_dense1m_stage0_2026-08"
sys.path.insert(0, str(_CON1))

import construct_lib as C  # noqa: E402

PANEL = _HERE / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"

# Roll exclusion — same rule as MNQSEL-2 / ICT helper (ict body pruned; inlined).
ROLL_MONTHS = (3, 6, 9, 12)
ROLL_BUFFER_DAYS = 4


def _third_friday(year: int, month: int) -> _dt.date:
    d = _dt.date(year, month, 1)
    # first Friday on/after the 1st, then +14 → 3rd Friday
    offset = (4 - d.weekday()) % 7
    first_fri = d + _dt.timedelta(days=offset)
    return first_fri + _dt.timedelta(days=14)


def in_roll_window(day: _dt.date, buffer_days: int = ROLL_BUFFER_DAYS) -> bool:
    for yr in (day.year - 1, day.year, day.year + 1):
        for mo in ROLL_MONTHS:
            if abs((day - _third_friday(yr, mo)).days) <= buffer_days:
                return True
    return False

# ---- GENEROUS a-priori constants (cheap falsifier only; G0 may re-freeze) ----
THETA_RANGE_MULT = 1.0  # prior bar range >= 1.0 × trailing median range
BODY_FRAC = 0.50  # |c-o| / range >= 0.50
MEDIAN_SESSIONS = 20
N_MIN_ARM = 100  # powered enough that both-negative is conclusive
N_BOOT = 2000  # lighter than explore; CI for kill decision only
BOOT_SEED = 20260809


def sessionize_rth(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    keep = (minute >= C.RTH_OPEN_MIN) & (minute < C.RTH_CLOSE_MIN)
    et_k = et[keep]
    out = pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": df.loc[keep, "open"].to_numpy(dtype=float),
            "high": df.loc[keep, "high"].to_numpy(dtype=float),
            "low": df.loc[keep, "low"].to_numpy(dtype=float),
            "close": df.loc[keep, "close"].to_numpy(dtype=float),
        }
    )
    return out


def session_median_range(ranges_by_session: list[np.ndarray], sid: int) -> float:
    if sid < MEDIAN_SESSIONS:
        return float("nan")
    chunks = ranges_by_session[sid - MEDIAN_SESSIONS : sid]
    parts = [c[c > 0] for c in chunks if len(c)]
    if not parts:
        return float("nan")
    return float(np.median(np.concatenate(parts)))


def displacement_side(o: float, c: float, h: float, l: float, med_rng: float) -> int:
    """Return fade side at NEXT open after this completed bar: +1 long / -1 short / 0.

    Displacement: range >= THETA_RANGE_MULT * med_rng and body/range >= BODY_FRAC.
    Fade AGAINST bar direction (close>open → short).
    """
    if not (np.isfinite(med_rng) and med_rng > 0):
        return 0
    rng = h - l
    if rng <= 0 or rng < THETA_RANGE_MULT * med_rng:
        return 0
    body = abs(c - o)
    if body / rng < BODY_FRAC:
        return 0
    # against the bar
    if c > o:
        return -1
    if c < o:
        return +1
    return 0


def simulate_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    med_rng: float,
) -> list[dict]:
    trades: list[dict] = []
    pos_end = -1
    n = len(open_)
    # signal from completed bar t-1 → enter at open of t
    for t in range(1, n):
        if t <= pos_end:
            continue
        side = displacement_side(
            float(open_[t - 1]),
            float(close[t - 1]),
            float(high[t - 1]),
            float(low[t - 1]),
            med_rng,
        )
        if side == 0:
            continue
        pts, kind = C.path_pts_session_flat(
            float(open_[t]), side, high, low, close, t, stop_pt=C.GATE_G
        )
        # exit bar
        stop_level = float(open_[t]) - side * C.GATE_G
        exit_i = n - 1
        for j in range(t, n):
            if side > 0 and low[j] <= stop_level:
                exit_i = j
                break
            if side < 0 and high[j] >= stop_level:
                exit_i = j
                break
        trades.append(
            {
                "side": side,
                "pts": pts,
                "kind": kind,
                "R": C.r_from_pts(pts),
                "exit_i": exit_i,
            }
        )
        pos_end = exit_i
    return trades


def session_block_ci(session_trade_rs: list[np.ndarray], n_boot: int = N_BOOT) -> tuple[float, float]:
    """Session-block bootstrap CI for the trade-weighted grand mean.

    Resample sessions with replacement, concatenate their trades, take mean.
    (Equal-weighting session *means* can flip sign vs trade-weighted mean_R —
    that bug falsely cleared an all-negative displacement fade.)
    """
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
    ranges_by_session: list[np.ndarray] = []
    sess_meta: list[object] = []
    for s in sessions:
        if in_roll_window(s):
            continue
        grp = df[df["session"] == s]
        if len(grp) < 60:
            continue
        rng = (grp["high"].to_numpy() - grp["low"].to_numpy()).astype(float)
        ranges_by_session.append(rng)
        sess_meta.append(s)

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    n_disp_clocks = 0
    n_eligible = 0

    # Pre-split once (avoid O(sessions²) full-frame filters)
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    for sid, s in enumerate(sess_meta):
        med = session_median_range(ranges_by_session, sid)
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        l = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        for t in range(1, len(o)):
            if displacement_side(o[t - 1], c[t - 1], h[t - 1], l[t - 1], med) != 0:
                n_disp_clocks += 1
        if not np.isfinite(med):
            continue
        n_eligible += 1
        trades = simulate_session(o, h, l, c, med)
        lr = np.asarray([t["R"] for t in trades if t["side"] > 0], dtype=float)
        sr = np.asarray([t["R"] for t in trades if t["side"] < 0], dtype=float)
        if len(lr):
            long_rs.extend(lr.tolist())
            long_blocks.append(lr)
        if len(sr):
            short_rs.extend(sr.tolist())
            short_blocks.append(sr)

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
        stop_r = C.r_from_pts(-C.GATE_G)
        return {
            "n": int(len(arr)),
            "mean_R": float(arr.mean()),
            "wr": float((arr > 0).mean()),
            "ci_lo": ci_lo,
            "ci_hi": ci_hi,
            "stop_rate": float(np.mean(np.isclose(arr, stop_r, atol=1e-9))),
            "n_sessions": int(len(blocks)),
        }

    long = arm_summary(long_rs, long_blocks)
    short = arm_summary(short_rs, short_blocks)
    elapsed = time.perf_counter() - t0

    # Kill rule (GENEROUS): FALSIFIED only if BOTH arms powered AND CI entirely < 0
    def arm_killed(a: dict) -> bool:
        return (
            a["n"] >= N_MIN_ARM
            and np.isfinite(a["ci_hi"])
            and a["ci_hi"] < 0.0
        )

    killed = arm_killed(long) and arm_killed(short)
    # Underpowered both → do not kill (inconclusive; licenses cautious G0 or VOID)
    underpowered = long["n"] < N_MIN_ARM and short["n"] < N_MIN_ARM

    if killed:
        verdict = "FALSIFIED"
        detail = (
            f"both arms session-block CI entirely < 0 at n>={N_MIN_ARM} "
            "— mechanism dead at $0"
        )
    elif underpowered:
        verdict = "VOID-UNDERPOWERED"
        detail = "displacement clocks too sparse under generous θ — do not spend Q-ID"
    else:
        verdict = "CHEAP_FALSIFIER_OK"
        detail = (
            "not both-arms CI<0; licenses G0 freeze for Q-TNEC-CON-2 "
            "(not EXPLORATION / not SHAPE-CLEAR)"
        )

    print("=== Q-TNEC-CON-2 candidate cheap falsifier: displacement fade ===")
    print(f"panel: {PANEL}")
    print(f"geometry: G={C.GATE_G} session-flat RT={C.RT_PT} EM3")
    print(
        f"thresholds (GENEROUS): range>={THETA_RANGE_MULT}×med20 body>={BODY_FRAC} "
        f"fade-against-bar"
    )
    print(f"eligible_sessions_with_theta: {n_eligible}")
    print(f"displacement_clocks: {n_disp_clocks}")
    print(f"long:  {long}")
    print(f"short: {short}")
    print(f"elapsed_s: {elapsed:.2f}")
    print(f"VERDICT: {verdict}")
    print(f"detail: {detail}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
