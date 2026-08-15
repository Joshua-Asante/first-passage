"""Q-TNEC-CON-4 Stage-0 runner — cheap record always; path PnL GO-gated.

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
EXPLORE_END = pd.Timestamp("2025-08-31").date()


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
        "tnec_template": C.g0_freeze_verdict_template(),
        "explore_scored": False,
        "panel": str(PANEL_DEFAULT),
        "cost_usd": 0.0,
        "long_mean_r_parent": r.long_mean_r,
        "short_mean_r_parent": r.short_mean_r,
    }


def run_explore(panel: Path) -> dict:
    if not C.explore_go_present(_HERE):
        raise SystemExit("REFUSE: EXPLORE_GO.md missing — operator explore GO unpaid")
    if not panel.is_file():
        raise SystemExit(f"REFUSE: panel missing {panel}")
    raw = pd.read_parquet(panel)
    df = sessionize_rth(raw)
    df = df[df["session"] <= EXPLORE_END]
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}
    ordered = []
    prior_hl = {}
    for s in sessions:
        if in_roll_window(s):
            continue
        grp = by_sess[s]
        if len(grp) < 60:
            continue
        ordered.append(s)
        prior_hl[s] = (float(grp["high"].max()), float(grp["low"].min()))

    long_rs: list[float] = []
    short_rs: list[float] = []
    long_blocks: list[np.ndarray] = []
    short_blocks: list[np.ndarray] = []
    sess_records: list[dict] = []
    stop_dists: list[float] = []
    gross_pts: list[float] = []
    scored_sessions = 0

    for i, s in enumerate(ordered):
        if i == 0:
            continue
        pdh, pdl = prior_hl[ordered[i - 1]]
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo_ = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        scored_sessions += 1
        trades = C.first_pdh_pdl_trade(o, h, lo_, c, pdh, pdl)
        lr = np.asarray([t["R"] for t in trades if t["side"] > 0], dtype=float)
        sr = np.asarray([t["R"] for t in trades if t["side"] < 0], dtype=float)
        for tr in trades:
            stop_dists.append(float(tr["stop_dist"]))
            gross_pts.append(float(tr["pts"]))
        sess_records.append(
            {
                "session": s,
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

    rng = np.random.default_rng(C.RANDOM_SEED)

    def _placebo_p(obs_rs: list[float]) -> float:
        arr = np.asarray(obs_rs, dtype=float)
        if len(arr) == 0:
            return float("nan")
        obs = float(arr.mean())
        means = np.empty(C.PLACEBO_REPS)
        for rep in range(C.PLACEBO_REPS):
            signs = rng.choice(np.array([-1.0, 1.0]), size=len(arr))
            means[rep] = float((arr * signs).mean())
        return float(np.mean(means >= obs))

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

    def _annsr(key):
        daily = np.asarray([r[key] for r in sess_records], dtype=float)
        if len(daily) < 2 or daily.std(ddof=1) == 0:
            return float("nan")
        return float(daily.mean() / daily.std(ddof=1) * np.sqrt(252.0))

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
    aux = {
        "long": {
            "placebo_p": _placebo_p(long_rs),
            "annsr": _annsr("sum_R_long"),
            "halves": halves["long"],
            "halves_agree": _halves_agree(halves["long"]),
        },
        "short": {
            "placebo_p": _placebo_p(short_rs),
            "annsr": _annsr("sum_R_short"),
            "halves": halves["short"],
            "halves_agree": _halves_agree(halves["short"]),
        },
    }

    def arm_pass(a):
        return a["n"] >= 30 and a["ci"][0] is not None and a["ci"][0] > 0 and a["mean_R"] > 0

    def arm_fail(a):
        return a["n"] >= 100 and a["ci"][1] is not None and a["ci"][1] < 0

    def _live_pass(a, x):
        return (
            arm_pass(a)
            and np.isfinite(x["placebo_p"])
            and x["placebo_p"] < 0.05
            and np.isfinite(x["annsr"])
            and x["annsr"] >= C.DSR_FLOOR
            and x["halves_agree"]
        )

    if arm_fail(long) and arm_fail(short):
        gate, n_shape = "FALSIFIED", "F"
    elif _live_pass(long, aux["long"]) or _live_pass(short, aux["short"]):
        gate, n_shape = "SHAPE-CLEAR-CANDIDATE", "U"
    else:
        gate, n_shape = "AMBIGUOUS-HOLD", "U"

    mean_stop = float(np.mean(stop_dists)) if stop_dists else float("nan")
    mean_gross = float(np.mean(gross_pts)) if gross_pts else float("nan")
    return {
        "gate": gate,
        "tnec": C.format_tnec_verdict(
            {"N-EDGE": "U", "N-SHAPE": n_shape},
            bust="U",
            p_pass="U",
            mu_disclosed=f"L{long['mean_R']:.4f}/S{short['mean_R']:.4f}",
        ),
        "long": long,
        "short": short,
        "aux": aux,
        "disclosures": {
            "explore_end": str(EXPLORE_END),
            "scored_sessions": scored_sessions,
            "coverage_sessions_with_trade": sum(
                1 for r in sess_records if r["n_long"] or r["n_short"]
            ),
            "mean_stop_dist_pt": mean_stop,
            "mean_gross_pts": mean_gross,
            "gross_vs_4x_rt": (mean_gross / (4.0 * C.RT_PT)) if np.isfinite(mean_gross) else None,
            "em_six_char": "P U U P P P",
            "placebo_note": "sign-randomized observed R; declared at explore GO",
        },
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
    (_HERE / "RESULTS.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
