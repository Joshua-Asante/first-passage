"""Q-TNEC-CON-2 Stage-0 runner — cheap record always; path PnL GO-gated.

Usage:
  python run_construct_g0.py                 # freeze template + admission recall
  python run_construct_g0.py --explore-go    # requires EXPLORE_GO.md; then scores
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import construct_lib as C  # noqa: E402

PANEL_DEFAULT = (
    _HERE.parent / "mnq_selection_ceiling_allbars_2026-08" / "_mnq_1m.parquet"
)

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


def sessionize_rth(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    keep = (minute >= C.RTH_OPEN_MIN) & (minute < C.RTH_CLOSE_MIN)
    et_k = et[keep]
    return pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": df.loc[keep, "open"].to_numpy(dtype=float),
            "high": df.loc[keep, "high"].to_numpy(dtype=float),
            "low": df.loc[keep, "low"].to_numpy(dtype=float),
            "close": df.loc[keep, "close"].to_numpy(dtype=float),
        }
    )


def session_block_ci(blocks: list[np.ndarray], n_boot: int = 10_000, seed: int = C.RANDOM_SEED):
    kept = [a for a in blocks if len(a)]
    if len(kept) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    idx = np.arange(len(kept))
    boots = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        pick = rng.choice(idx, size=len(kept), replace=True)
        boots[i] = float(np.concatenate([kept[j] for j in pick]).mean())
    return float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def run_cheap() -> dict:
    r = C.cheap_falsifier_freeze_ok()
    return {
        "verdict": r.verdict,
        "detail": r.detail,
        "em1_pred_pt": r.em1_pred_pt,
        "nedge_pred_pt": r.nedge_pred_pt,
        "tnec_template": C.g0_freeze_verdict_template(),
        "explore_scored": False,
        "panel": str(PANEL_DEFAULT),
        "cost_usd": 0.0,
    }


# EXPLORATION/CONFIRM split — declared in EXPLORE_GO.md at operator GO, before any score.
# CONFIRM (sessions > EXPLORE_END) is dropped before scoring and never read.
EXPLORE_END = pd.Timestamp("2025-08-31").date()


def _mae_mfe_pts(entry, side, high, low, start, exit_bar):
    seg_hi = float(np.max(high[start : exit_bar + 1]))
    seg_lo = float(np.min(low[start : exit_bar + 1]))
    if side > 0:
        return entry - seg_lo, seg_hi - entry
    return seg_hi - entry, entry - seg_lo


def _precompute_all_entries(open_, high, low, close):
    """Path R for every (bar, side) — the random-entry placebo's sampling pool."""
    n = len(open_)
    out = {1: np.full(n, np.nan), -1: np.full(n, np.nan)}
    for side in (1, -1):
        for t in range(C.K_NARROW + 1, n):
            pts, _ = C.path_pts_session_flat(float(open_[t]), side, high, low, close, t)
            out[side][t] = C.r_from_pts(pts)
    return out


def run_explore(panel: Path) -> dict:
    if not C.explore_go_present(_HERE):
        raise SystemExit("REFUSE: EXPLORE_GO.md missing — operator explore GO unpaid")
    if not panel.is_file():
        raise SystemExit(f"REFUSE: panel missing {panel}")
    raw = pd.read_parquet(panel)
    df = sessionize_rth(raw)
    df = df[df["session"] <= EXPLORE_END]  # CONFIRM reserved; never read past here
    sessions = sorted(df["session"].unique())
    ranges_by_session: list[np.ndarray] = []
    sess_meta: list = []
    for s in sessions:
        if in_roll_window(s):
            continue
        grp = df[df["session"] == s]
        if len(grp) < 60:
            continue
        ranges_by_session.append((grp["high"].to_numpy() - grp["low"].to_numpy()).astype(float))
        sess_meta.append(s)
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}
    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    # per-session records for placebo / halves / DSR / disclosures
    sess_records: list[dict] = []
    mae_l: list[float] = []
    mfe_l: list[float] = []
    mae_s: list[float] = []
    mfe_s: list[float] = []
    scored_sessions = 0
    for sid, s in enumerate(sess_meta):
        med = C.session_median_range(ranges_by_session, sid)
        if not np.isfinite(med):
            continue
        scored_sessions += 1
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo_ = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        trades = C.simulate_session_trades(o, h, lo_, c, med)
        for t in trades:
            a, f = _mae_mfe_pts(float(o[t["entry_i"]]), t["side"], h, lo_, t["entry_i"], t["exit_i"])
            (mae_l if t["side"] > 0 else mae_s).append(a)
            (mfe_l if t["side"] > 0 else mfe_s).append(f)
        lr = np.asarray([t["R"] for t in trades if t["side"] > 0], dtype=float)
        sr = np.asarray([t["R"] for t in trades if t["side"] < 0], dtype=float)
        sess_records.append(
            {
                "session": s,
                "ohlc": (o, h, lo_, c),
                "n_long": int(len(lr)),
                "n_short": int(len(sr)),
                "sum_R_long": float(lr.sum()) if len(lr) else 0.0,
                "sum_R_short": float(sr.sum()) if len(sr) else 0.0,
                "long_R": lr,
                "short_R": sr,
            }
        )
        if len(lr):
            long_rs.extend(lr.tolist())
            long_blocks.append(lr)
        if len(sr):
            short_rs.extend(sr.tolist())
            short_blocks.append(sr)

    # --- placebo (EXPLORE_GO.md operationalization): random-entry, same per-session
    # count + side mix, same geometry; PLACEBO_REPS reps, RANDOM_SEED; p_emp one-sided
    rng = np.random.default_rng(C.RANDOM_SEED)
    pools = []
    for rec in sess_records:
        if rec["n_long"] or rec["n_short"]:
            o, h, lo_, c = rec["ohlc"]
            pool = _precompute_all_entries(o, h, lo_, c)
            valid = {sd: np.flatnonzero(np.isfinite(pool[sd])) for sd in (1, -1)}
            pools.append((rec, pool, valid))
    def _placebo_means(side_key: str, side: int):
        obs_all = np.concatenate([r[0][side_key] for r in pools if len(r[0][side_key])]) if pools else np.array([])
        if len(obs_all) == 0:
            return float("nan"), float("nan")
        obs = float(obs_all.mean())
        n_tr = [len(r[0][side_key]) for r in pools]
        means = np.empty(C.PLACEBO_REPS)
        for rep in range(C.PLACEBO_REPS):
            acc = []
            for (rec, pool, valid), k in zip(pools, n_tr):
                if k and len(valid[side]):
                    pick = rng.choice(valid[side], size=k, replace=True)
                    acc.append(pool[side][pick])
            means[rep] = float(np.concatenate(acc).mean()) if acc else np.nan
        p_emp = float(np.mean(means >= obs))
        return obs, p_emp

    _, placebo_p_long = _placebo_means("long_R", 1)
    _, placebo_p_short = _placebo_means("short_R", -1)

    # --- halves (older/newer EXPLORATION session-date halves; §3)
    mid = len(sess_records) // 2
    def _half_mean(recs, key):
        allr = np.concatenate([r[key] for r in recs if len(r[key])]) if recs else np.array([])
        return float(allr.mean()) if len(allr) else float("nan")
    halves = {
        "long": [_half_mean(sess_records[:mid], "long_R"), _half_mean(sess_records[mid:], "long_R")],
        "short": [_half_mean(sess_records[:mid], "short_R"), _half_mean(sess_records[mid:], "short_R")],
    }
    def _halves_agree(pair):
        a, b = pair
        if not (np.isfinite(a) and np.isfinite(b)):
            return False
        return (a > 0) == (b > 0)

    # --- DSR limb (EXPLORE_GO.md reading): annSR of daily net-R stream, zero days included
    def _annsr(key):
        daily = np.asarray([r[key] for r in sess_records], dtype=float)
        if len(daily) < 2 or daily.std(ddof=1) == 0:
            return float("nan")
        return float(daily.mean() / daily.std(ddof=1) * np.sqrt(252.0))
    annsr = {"long": _annsr("sum_R_long"), "short": _annsr("sum_R_short")}

    def arm(rs, blocks):
        arr = np.asarray(rs, dtype=float)
        if len(arr) == 0:
            return {"n": 0, "mean_R": float("nan"), "wr": float("nan"), "ci": [None, None]}
        lo, hi = session_block_ci(blocks)
        return {
            "n": int(len(arr)),
            "mean_R": float(arr.mean()),
            "wr": float((arr > 0).mean()),
            "ci": [lo, hi],
            "n_sessions": len(blocks),
        }

    long = arm(long_rs, long_blocks)
    short = arm(short_rs, short_blocks)

    def arm_pass(a):
        return (
            a["n"] >= 30
            and a["ci"][0] is not None
            and a["ci"][0] > 0
            and a["mean_R"] > 0
        )

    def arm_fail(a):
        return (
            a["n"] >= 100
            and a["ci"][1] is not None
            and a["ci"][1] < 0
        )

    # EXPLORE_GO.md declared downgrades: an arm is only a live pass if the primary CI
    # passes AND placebo p_emp < 0.05 AND annSR >= DSR floor AND halves agree in sign.
    aux = {
        "long": {"placebo_p": placebo_p_long, "annsr": annsr["long"],
                 "halves": halves["long"], "halves_agree": _halves_agree(halves["long"])},
        "short": {"placebo_p": placebo_p_short, "annsr": annsr["short"],
                  "halves": halves["short"], "halves_agree": _halves_agree(halves["short"])},
    }
    def _live_pass(a, x):
        return (arm_pass(a) and x["placebo_p"] < 0.05
                and np.isfinite(x["annsr"]) and x["annsr"] >= C.DSR_FLOOR
                and x["halves_agree"])

    if arm_fail(long) and arm_fail(short):
        gate = "FALSIFIED"
        n_shape = "F"
    elif _live_pass(long, aux["long"]) or _live_pass(short, aux["short"]):
        gate = "SHAPE-CLEAR-CANDIDATE"
        n_shape = "U"  # confirm GO still owed; explore only
    elif arm_pass(long) or arm_pass(short):
        gate = "AMBIGUOUS-HOLD"  # primary passed; a declared aux limb failed (disclosed)
        n_shape = "U"
    else:
        gate = "AMBIGUOUS-HOLD"
        n_shape = "U"

    tnec = C.format_tnec_verdict(
        {"N-EDGE": "U", "N-SHAPE": n_shape},
        bust="U",
        p_pass="U",
        mu_disclosed=f"L{long['mean_R']:.4f}/S{short['mean_R']:.4f}",
    )
    disclosures = {
        "explore_end": str(EXPLORE_END),
        "scored_sessions": scored_sessions,
        "coverage_sessions_with_trade": sum(1 for r in sess_records if r["n_long"] or r["n_short"]),
        "trades_per_session": {
            "long": (long["n"] / scored_sessions) if scored_sessions else float("nan"),
            "short": (short["n"] / scored_sessions) if scored_sessions else float("nan"),
        },
        "mae_mfe_pts_mean": {
            "long": [float(np.mean(mae_l)) if mae_l else None, float(np.mean(mfe_l)) if mfe_l else None],
            "short": [float(np.mean(mae_s)) if mae_s else None, float(np.mean(mfe_s)) if mfe_s else None],
        },
        "em_six_char": "P U U P P P",
    }
    return {
        "gate": gate,
        "tnec": tnec,
        "long": long,
        "short": short,
        "aux": aux,
        "disclosures": disclosures,
        "explore_scored": True,
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "panel": str(panel),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--explore-go", action="store_true")
    p.add_argument("--panel", type=Path, default=PANEL_DEFAULT)
    args = p.parse_args()
    cheap = run_cheap()
    print(json.dumps(cheap, indent=2))
    print(f"TNEC freeze template: {cheap['tnec_template']}")
    if not args.explore_go:
        print("Explore: BLOCKED (pass --explore-go after EXPLORE_GO.md)")
        return 0
    out = run_explore(args.panel)
    print(json.dumps(out, indent=2))
    ( _HERE / "RESULTS.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
