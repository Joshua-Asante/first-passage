"""Q-TNEC-CON-4 CONFIRM runner -- window-only sibling of run_construct_g0.py's
run_explore(). Authorized by docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md
(U1 exception). Does NOT modify run_construct_g0.py or construct_lib.py -- both stay
byte-identical to their EXPLORE-scoring state; this file only changes the session-date
window and the GO-gate artifact it checks for.

Usage:
  python run_confirm_g0.py --confirm-go    # requires CONFIRM_GO.md; then scores
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
import run_construct_g0 as E  # noqa: E402  (reuse sessionize_rth / in_roll_window / session_block_ci verbatim)

CONFIRM_START = pd.Timestamp("2025-09-01").date()
CONFIRM_END = pd.Timestamp("2026-08-05").date()


def confirm_go_present() -> bool:
    return (_HERE / "CONFIRM_GO.md").is_file()


def run_confirm(panel: Path) -> dict:
    if not confirm_go_present():
        raise SystemExit("REFUSE: CONFIRM_GO.md missing -- operator/ADR confirm GO not on disk")
    if not panel.is_file():
        raise SystemExit(f"REFUSE: panel missing {panel}")
    raw = pd.read_parquet(panel)
    df = E.sessionize_rth(raw)
    # Full panel, not window-clipped here -- the prior-session PDH/PDL lookback for the
    # first CONFIRM session must see the last EXPLORE-era session. Window selection
    # happens per-session below, at scoring time, not at the session-list stage.
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}
    ordered = []
    prior_hl = {}
    for s in sessions:
        if E.in_roll_window(s):
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
        if not (CONFIRM_START <= s <= CONFIRM_END):
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
        # NOTE: run_construct_g0.py's run_explore() has the identical `if recs else
        # np.array([])` guard, which does not cover the case where recs is non-empty
        # but every record's `key` array is itself empty (e.g. zero long trades in an
        # entire half) -- np.concatenate([]) then raises ValueError. Never hit at
        # EXPLORE's ~245-session scale; hit immediately on this file's small synthetic
        # test fixture (test_run_confirm_g0.py). Fixed here only -- the frozen EXPLORE
        # runner is not touched, since EXPLORE already scored successfully.
        parts = [r[key] for r in recs if len(r[key])]
        allr = np.concatenate(parts) if parts else np.array([])
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
        lo, hi = E.session_block_ci(blocks)
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
            "confirm_start": str(CONFIRM_START),
            "confirm_end": str(CONFIRM_END),
            "scored_sessions": scored_sessions,
            "coverage_sessions_with_trade": sum(
                1 for r in sess_records if r["n_long"] or r["n_short"]
            ),
            "mean_stop_dist_pt": mean_stop,
            "mean_gross_pts": mean_gross,
            "gross_vs_4x_rt": (mean_gross / (4.0 * C.RT_PT)) if np.isfinite(mean_gross) else None,
            "placebo_note": "sign-randomized observed R; declared at CONFIRM_GO (unchanged from EXPLORE)",
        },
        "confirm_scored": True,
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "panel": str(panel),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--confirm-go", action="store_true")
    p.add_argument("--panel", type=Path, default=E.PANEL_DEFAULT)
    args = p.parse_args()
    if not args.confirm_go:
        print("Confirm: BLOCKED (pass --confirm-go after CONFIRM_GO.md)")
        return 0
    out = run_confirm(args.panel)
    print(json.dumps(out, indent=2, default=str))
    (_HERE / "RESULTS_CONFIRM.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
