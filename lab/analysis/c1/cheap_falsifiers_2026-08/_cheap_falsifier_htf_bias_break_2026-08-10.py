"""Parent-side GENEROUS cheap falsifier — HTF-5m bias + LTF-1m with-break.

Master-Pattern-shaped cell (Tradeify defaults). No Q-ID. $0.
Failure conclusive:
  - VOID-COVERAGE if too few sessions ever get a defined HTF bias, OR
  - FALSIFIED if both arms powered and session-block CI entirely < 0.

Licenses G0 freeze only on CHEAP_FALSIFIER_OK — not explore / not SHAPE-CLEAR.
Distinct from Q-TNEC-CON-2 (single-TF with-break; already AMBIGUOUS-HOLD).
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

# ---- GENEROUS a-priori constants (plan freeze packet) -----------------------
K_NARROW = 2
NARROW_MULT = 1.0
MEDIAN_SESSIONS = 20
HTF_MINUTES = 5
N_MIN_ARM = 100
N_BOOT = 2000
BOOT_SEED = 20260810
# Coverage floor: fraction of θ-warm sessions that ever hold a defined bias
BIAS_SESSION_FRAC_MIN = 0.20

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
    """Aggregate 1m RTH bars to 5m OHLC; index = bar open (ET)."""
    g = grp.set_index("ts_et").sort_index()
    ohlc = g.resample(f"{HTF_MINUTES}min", label="left", closed="left").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
    )
    return ohlc.dropna(subset=["open", "high", "low", "close"])


def htf_break_side(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
    med_rng: float,
) -> int:
    """Bias settle at HTF bar t (uses bars ≤ t only — after that bar closes).

    Compression: K_NARROW narrow bars ending at t-1; break bar = t.
    Midline = mid of quiet hi/lo. Require close beyond extreme AND on that
    side of midline (plan settle rule).
    """
    if not (np.isfinite(med_rng) and med_rng > 0):
        return 0
    start = t - K_NARROW
    end_comp = t - 1
    if start < 0 or t >= len(close):
        return 0
    for i in range(start, end_comp + 1):
        rng = high[i] - low[i]
        if rng <= 0 or rng > NARROW_MULT * med_rng:
            return 0
    quiet_hi = float(np.max(high[start : end_comp + 1]))
    quiet_lo = float(np.min(low[start : end_comp + 1]))
    if quiet_hi <= quiet_lo:
        return 0
    mid = 0.5 * (quiet_hi + quiet_lo)
    c_brk = float(close[t])
    up = c_brk > quiet_hi and c_brk > mid
    dn = c_brk < quiet_lo and c_brk < mid
    if up and not dn:
        return +1
    if dn and not up:
        return -1
    return 0


def build_htf_bias_series(
    htf: pd.DataFrame, med_rng: float
) -> tuple[np.ndarray, np.ndarray]:
    """Return (htf_close_ts, bias_after_close) — bias known at/after each HTF close."""
    high = htf["high"].to_numpy(dtype=float)
    low = htf["low"].to_numpy(dtype=float)
    close = htf["close"].to_numpy(dtype=float)
    # close timestamp = open + 5m (label=left); use int64 ns for searchsorted
    opens = pd.DatetimeIndex(htf.index)
    closes_ts = (opens + pd.Timedelta(minutes=HTF_MINUTES)).asi8
    bias = np.zeros(len(htf), dtype=int)
    cur = 0
    for t in range(K_NARROW, len(htf)):
        side = htf_break_side(high, low, close, t, med_rng)
        if side != 0:
            cur = side
        bias[t] = cur
    return closes_ts, bias


def bias_at_1m_open(ts_open, htf_close_ts: np.ndarray, htf_bias: np.ndarray) -> int:
    """Causal: only HTF bars whose close ≤ this 1m open contribute."""
    if len(htf_close_ts) == 0:
        return 0
    ts_ns = pd.Timestamp(ts_open).value
    i = int(np.searchsorted(htf_close_ts, ts_ns, side="right")) - 1
    if i < 0:
        return 0
    return int(htf_bias[i])


def ltf_break_side(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
    med_rng: float,
) -> int:
    """Same CON-2 with-break rule at 1m open t (bars ≤ t-1)."""
    return C.break_side_at_t(high, low, close, t, med_rng)


def simulate_session_directed(
    grp: pd.DataFrame,
    med_1m: float,
    med_5m: float,
) -> tuple[list[dict], bool]:
    """Return (trades, session_had_bias)."""
    if not (np.isfinite(med_1m) and np.isfinite(med_5m)):
        return [], False
    htf = resample_5m(grp)
    if len(htf) < K_NARROW + 1:
        return [], False
    htf_close_ts, htf_bias = build_htf_bias_series(htf, med_5m)
    had_bias = bool(np.any(htf_bias != 0))

    o = grp["open"].to_numpy(dtype=float)
    h = grp["high"].to_numpy(dtype=float)
    l = grp["low"].to_numpy(dtype=float)
    c = grp["close"].to_numpy(dtype=float)
    ts = grp["ts_et"].to_numpy()

    trades: list[dict] = []
    pos_end = -1
    n = len(o)
    for t in range(K_NARROW + 1, n):
        if t <= pos_end:
            continue
        bias = bias_at_1m_open(ts[t], htf_close_ts, htf_bias)
        if bias == 0:
            continue
        side = ltf_break_side(h, l, c, t, med_1m)
        if side == 0 or side != bias:
            continue
        pts, kind = C.path_pts_session_flat(
            float(o[t]), side, h, l, c, t, stop_pt=C.GATE_G
        )
        stop_level = float(o[t]) - side * C.GATE_G
        exit_i = n - 1
        for j in range(t, n):
            if side > 0 and l[j] <= stop_level:
                exit_i = j
                break
            if side < 0 and h[j] >= stop_level:
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
    return trades, had_bias


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
    ranges_1m: list[np.ndarray] = []
    ranges_5m: list[np.ndarray] = []
    sess_meta: list[object] = []
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < 60:
            continue
        ranges_1m.append((grp["high"].to_numpy() - grp["low"].to_numpy()).astype(float))
        htf = resample_5m(grp)
        if len(htf) < 5:
            continue
        ranges_5m.append((htf["high"].to_numpy() - htf["low"].to_numpy()).astype(float))
        sess_meta.append(s)

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    n_eligible = 0
    n_bias_sessions = 0
    n_entry_clocks = 0

    for sid, s in enumerate(sess_meta):
        med_1m = session_median_range(ranges_1m, sid)
        med_5m = session_median_range(ranges_5m, sid)
        if not (np.isfinite(med_1m) and np.isfinite(med_5m)):
            continue
        n_eligible += 1
        trades, had_bias = simulate_session_directed(by_sess[s], med_1m, med_5m)
        if had_bias:
            n_bias_sessions += 1
        n_entry_clocks += len(trades)
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
    bias_frac = (n_bias_sessions / n_eligible) if n_eligible else 0.0
    elapsed = time.perf_counter() - t0

    def arm_killed(a: dict) -> bool:
        return a["n"] >= N_MIN_ARM and np.isfinite(a["ci_hi"]) and a["ci_hi"] < 0.0

    killed = arm_killed(long) and arm_killed(short)
    underpowered = long["n"] < N_MIN_ARM and short["n"] < N_MIN_ARM
    void_cov = bias_frac < BIAS_SESSION_FRAC_MIN

    if void_cov:
        verdict = "VOID-COVERAGE"
        detail = (
            f"bias session frac {bias_frac:.3f} < floor {BIAS_SESSION_FRAC_MIN} "
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
        detail = "directed entry clocks too sparse under generous theta - no Q-ID"
    else:
        verdict = "CHEAP_FALSIFIER_OK"
        detail = (
            "bias coverage + not both-arms CI<0; licenses G0 freeze for "
            "Q-TNEC-CON-3 (not EXPLORATION / not SHAPE-CLEAR)"
        )

    out = {
        "family": "htf5m_bias_ltf1m_with_break",
        "geometry": {
            "G": C.GATE_G,
            "exit": "session_flat",
            "RT": C.RT_PT,
            "EM3": True,
            "HTF_min": HTF_MINUTES,
            "LTF_min": 1,
        },
        "thresholds": {
            "K_NARROW": K_NARROW,
            "NARROW_MULT": NARROW_MULT,
            "MEDIAN_SESSIONS": MEDIAN_SESSIONS,
            "BIAS_SESSION_FRAC_MIN": BIAS_SESSION_FRAC_MIN,
        },
        "eligible_sessions_with_theta": n_eligible,
        "bias_sessions": n_bias_sessions,
        "bias_session_frac": bias_frac,
        "entry_clocks": n_entry_clocks,
        "long": long,
        "short": short,
        "elapsed_s": elapsed,
        "verdict": verdict,
        "detail": detail,
        "cost_usd": 0.0,
    }
    out_path = _HERE / "_cheap_falsifier_htf_bias_break_2026-08-10_RESULTS.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("=== Q-TNEC-CON-3 candidate cheap falsifier: HTF-5m bias + LTF with-break ===")
    print(f"panel: {PANEL}")
    print(f"geometry: G={C.GATE_G} session-flat RT={C.RT_PT} HTF={HTF_MINUTES}m LTF=1m")
    print(
        f"thresholds: K_NARROW={K_NARROW} NARROW_MULT={NARROW_MULT} "
        f"bias_frac_min={BIAS_SESSION_FRAC_MIN}"
    )
    print(f"eligible_sessions_with_theta: {n_eligible}")
    print(f"bias_sessions: {n_bias_sessions} ({bias_frac:.3f})")
    print(f"entry_clocks: {n_entry_clocks}")
    print(f"long:  {long}")
    print(f"short: {short}")
    print(f"elapsed_s: {elapsed:.2f}")
    print(f"VERDICT: {verdict}")
    print(f"detail: {detail}")
    print(f"wrote: {out_path}")
    return 0 if verdict == "CHEAP_FALSIFIER_OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
