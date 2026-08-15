"""MSL-C1 Stage G0 runner — freeze recall always; path PnL GO-gated.

Usage:
  python run_construct_g0.py                 # freeze template + admission recall
  python run_construct_g0.py --explore-go    # requires EXPLORE_GO.md + MYM_M15 sha match
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[3]
sys.path.insert(0, str(_HERE))

import construct_lib as C  # noqa: E402

PANEL_DEFAULT = _REPO / C.MYM_PANEL_REL
SHA256SUMS = _REPO / "core" / "data" / "bar_data" / "SHA256SUMS"

# IS = sessions with date < 2025-09-01; CONFIRM never read
EXPLORE_END = pd.Timestamp("2025-08-31").date()


def _expected_mym_sha() -> str:
    text = SHA256SUMS.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace("*", " ").split()
        if len(parts) >= 2 and parts[-1].endswith("MYM_M15.csv"):
            return parts[0]
    return C.MYM_SHA256


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_panel_ok(panel: Path) -> None:
    if not panel.is_file():
        raise SystemExit(f"REFUSE: panel missing {panel}")
    got = _file_sha256(panel)
    want = _expected_mym_sha()
    if got != want:
        raise SystemExit(
            f"REFUSE: MYM_M15 sha mismatch\n  got  {got}\n  want {want}"
        )


def load_bars(panel: Path) -> pd.DataFrame:
    df = pd.read_csv(panel)
    if "time" not in df.columns:
        raise SystemExit("REFUSE: panel missing 'time' column")
    ts = pd.to_datetime(df["time"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    out = pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et).normalize().date,
            "minute": et.dt.hour * 60 + et.dt.minute,
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    # Drop CONFIRM entirely before any score path
    return out[out["session"] <= EXPLORE_END].copy()


def run_cheap() -> dict:
    r = C.cheap_falsifier_freeze_ok()
    return {
        "verdict": r.verdict,
        "detail": r.detail,
        "rt_usd": r.rt_usd,
        "four_x_rt_usd": r.four_x_rt_usd,
        "tnec_template": C.g0_freeze_verdict_template(),
        "explore_scored": False,
        "panel": str(PANEL_DEFAULT),
        "explore_go_present": C.explore_go_present(_HERE),
        "cost_usd": 0.0,
        "k_spent": 0,
    }


def _placebo_p(obs_rs: list[float], seed: int = C.RANDOM_SEED) -> float:
    if len(obs_rs) < 2:
        return float("nan")
    arr = np.asarray(obs_rs, dtype=float)
    obs = float(arr.mean())
    rng = np.random.default_rng(seed)
    null = np.empty(C.PLACEBO_REPS, dtype=float)
    for i in range(C.PLACEBO_REPS):
        signs = rng.choice(np.array([-1.0, 1.0]), size=len(arr))
        null[i] = float((arr * signs).mean())
    return float(np.mean(np.abs(null) >= abs(obs)))


def _annsr_daily(daily_r: np.ndarray) -> float:
    if len(daily_r) < 2:
        return float("nan")
    mu = float(daily_r.mean())
    sd = float(daily_r.std(ddof=1))
    if sd <= 0 or not np.isfinite(sd):
        return float("nan")
    return mu / sd * np.sqrt(252.0)


def _halves_agree(h: dict) -> bool:
    o, n = h.get("older"), h.get("newer")
    if not (np.isfinite(o) and np.isfinite(n)):
        return False
    return (o > 0 and n > 0) or (o < 0 and n < 0)


def run_explore(panel: Path) -> dict:
    if not C.explore_go_present(_HERE):
        raise SystemExit("REFUSE: EXPLORE_GO.md missing — operator explore GO unpaid")
    assert_panel_ok(panel)
    df = load_bars(panel)
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

    # Prior Globex-day RTH H/L = PDH/PDL (chronological)
    prior_pdh_pdl: dict = {}
    prev_hi, prev_lo = float("nan"), float("nan")
    for s in sessions:
        prior_pdh_pdl[s] = (prev_hi, prev_lo)
        grp = by_sess[s]
        hi, lo = C.rth_hl(
            grp["high"].to_numpy(dtype=float),
            grp["low"].to_numpy(dtype=float),
            grp["minute"].to_numpy(dtype=int),
        )
        if np.isfinite(hi) and np.isfinite(lo):
            prev_hi, prev_lo = hi, lo

    constrained_by_sess: list[list[dict]] = []
    delete_by_sess: list[list[dict]] = []
    flip_by_sess: list[list[dict]] = []
    sess_meta: list = []

    for s in sessions:
        grp = by_sess[s]
        o = grp["open"].to_numpy(dtype=float)
        h = grp["high"].to_numpy(dtype=float)
        lo_ = grp["low"].to_numpy(dtype=float)
        c = grp["close"].to_numpy(dtype=float)
        m = grp["minute"].to_numpy(dtype=int)
        phi, plo = prior_pdh_pdl[s]
        if np.isfinite(phi) and np.isfinite(plo):
            constrained_by_sess.append(C.simulate_constrained(o, h, lo_, c, m, phi, plo))
            flip_by_sess.append(C.simulate_flip_join(o, h, lo_, c, m, phi, plo))
        else:
            constrained_by_sess.append([])
            flip_by_sess.append([])
        delete_by_sess.append(C.simulate_delete_sham(o, h, lo_, c, m))
        sess_meta.append(s)

    def collect(trades_by_sess: list[list[dict]], side: int):
        rs: list[float] = []
        blocks: list[np.ndarray] = []
        dates_for_halves: list = []
        rs_by_sess: list[np.ndarray] = []
        stops: list[float] = []
        daily: list[float] = []
        for s, trades in zip(sess_meta, trades_by_sess):
            arm = [t for t in trades if int(t["side"]) == side]
            day_r = 0.0
            arr = (
                np.asarray([t["R"] for t in arm], dtype=float)
                if arm
                else np.asarray([], dtype=float)
            )
            if len(arr):
                rs.extend(arr.tolist())
                blocks.append(arr)
                stops.extend(float(t["stop_dist"]) for t in arm)
                day_r = float(arr.sum())
            dates_for_halves.append(s)
            rs_by_sess.append(arr)
            daily.append(day_r)
        scored = C.score_arm_rs(rs)
        lo, hi = C.session_block_ci(blocks)
        scored["ci"] = [lo if np.isfinite(lo) else None, hi if np.isfinite(hi) else None]
        scored["mean_stop_dist"] = float(np.mean(stops)) if stops else float("nan")
        halves = C.halves_means(dates_for_halves, rs_by_sess)
        annsr = _annsr_daily(np.asarray(daily, dtype=float))
        placebo = _placebo_p(rs)
        return scored, halves, annsr, placebo, rs

    long_c, half_l, ann_l, pla_l, rs_l = collect(constrained_by_sess, +1)
    short_c, half_s, ann_s, pla_s, rs_s = collect(constrained_by_sess, -1)
    long_d, _, _, _, _ = collect(delete_by_sess, +1)
    short_d, _, _, _, _ = collect(delete_by_sess, -1)
    long_f, _, _, _, _ = collect(flip_by_sess, +1)
    short_f, _, _, _, _ = collect(flip_by_sess, -1)

    delete = {
        "long": {
            "constrained_mean": long_c["mean_R"],
            "sham_mean": long_d["mean_R"],
            "pass": C.delete_pass(long_c["mean_R"], long_d["mean_R"]),
        },
        "short": {
            "constrained_mean": short_c["mean_R"],
            "sham_mean": short_d["mean_R"],
            "pass": C.delete_pass(short_c["mean_R"], short_d["mean_R"]),
        },
    }
    flip = {
        "long_fade_vs_short_flip": {
            "fade_mean": long_c["mean_R"],
            "flip_mean": short_f["mean_R"],
            "pass": C.flip_pass(long_c["mean_R"], short_f["mean_R"]),
        },
        "short_fade_vs_long_flip": {
            "fade_mean": short_c["mean_R"],
            "flip_mean": long_f["mean_R"],
            "pass": C.flip_pass(short_c["mean_R"], long_f["mean_R"]),
        },
    }

    def arm_pass(a):
        return (
            a["n"] >= 30
            and a["ci"][0] is not None
            and a["ci"][0] > 0
            and np.isfinite(a["mean_R"])
            and a["mean_R"] > 0
        )

    def arm_fail(a):
        return a["n"] >= 100 and a["ci"][1] is not None and a["ci"][1] < 0

    aux = {
        "long": {
            "placebo_p": pla_l,
            "annsr": ann_l,
            "halves": half_l,
            "halves_agree": _halves_agree(half_l),
        },
        "short": {
            "placebo_p": pla_s,
            "annsr": ann_s,
            "halves": half_s,
            "halves_agree": _halves_agree(half_s),
        },
    }

    def _live_pass(a, x, del_ok, flip_ok):
        return (
            arm_pass(a)
            and del_ok
            and flip_ok
            and np.isfinite(x["placebo_p"])
            and x["placebo_p"] < 0.05
            and np.isfinite(x["annsr"])
            and x["annsr"] >= C.DSR_FLOOR
            and x["halves_agree"]
        )

    long_del = delete["long"]["pass"]
    short_del = delete["short"]["pass"]
    long_flip_ok = flip["long_fade_vs_short_flip"]["pass"]
    short_flip_ok = flip["short_fade_vs_long_flip"]["pass"]

    if arm_fail(long_c) and arm_fail(short_c):
        gate = "FALSIFIED"
    elif _live_pass(long_c, aux["long"], long_del, long_flip_ok) or _live_pass(
        short_c, aux["short"], short_del, short_flip_ok
    ):
        gate = "SHAPE-CLEAR"
    else:
        gate = "AMBIGUOUS-HOLD"

    def cost_law(a):
        sd = a.get("mean_stop_dist", float("nan"))
        if not np.isfinite(sd) or sd <= 0:
            return None
        one_r = sd * C.POINT_VALUE
        return {
            "mean_stop_dist_pts": sd,
            "one_r_usd": one_r,
            "four_x_rt_usd": C.FOUR_X_RT_USD,
            "gross_vs_4x": one_r / C.FOUR_X_RT_USD,
        }

    scored_sessions = len(sess_meta)
    coverage = sum(
        1
        for trades in constrained_by_sess
        if any(t["side"] in (+1, -1) for t in trades)
    )
    tnec = C.format_tnec_verdict(
        {"N-SHAPE": "U"},
        bust="U",
        p_pass="U",
        mu_disclosed=f"L{long_c['mean_R']:.4f}/S{short_c['mean_R']:.4f}",
    )
    return {
        "gate": gate,
        "tnec": tnec,
        "long": long_c,
        "short": short_c,
        "delete": delete,
        "flip": flip,
        "aux": aux,
        "cost_law": {"long": cost_law(long_c), "short": cost_law(short_c)},
        "disclosures": {
            "explore_end": str(EXPLORE_END),
            "confirm_reserved": "2025-09-01→2026-08-13",
            "scored_sessions": scored_sessions,
            "coverage_sessions_with_trade": coverage,
            "panel_sha256": _file_sha256(panel),
            "em_six_char": "U U U U U U",
        },
        "explore_scored": True,
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "panel": str(panel),
        "cost_usd": 0.0,
        "k_spent": 0,
    }


def _write_results_md(out: dict) -> None:
    lines = [
        "# MSL-C1 — EXPLORATION RESULTS (G0)",
        "",
        f"**Status:** `{out['gate']}`",
        f"**Date:** {out.get('scored_at', '')[:10]} · **Cost:** $0.00 · **K:** disclosure only "
        f"(`K_intrinsic=1`).",
        f"**Explore GO:** [`EXPLORE_GO.md`](EXPLORE_GO.md) (promoted from DRAFT; delete/flip + "
        f"placebo declared pre-score).",
        f"**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md)",
        f"**Machine record:** [`RESULTS.json`](RESULTS.json)",
        "",
        "## Headline (EXPLORATION = sessions ≤ 2025-08-31; CONFIRM reserved unread)",
        "",
        "| Arm | n | mean net R | WR | session-block 95% CI |",
        "|---|---|---|---|---|",
    ]
    for name in ("long", "short"):
        a = out[name]
        ci = a.get("ci") or [None, None]
        lines.append(
            f"| {name.title()} | {a['n']} | {a['mean_R']:.4f} | {a.get('wr', float('nan')):.3f} | "
            f"[{ci[0]}, {ci[1]}] |"
        )
    lines += [
        "",
        f"**Gate:** `{out['gate']}` · **TNEC:** `{out['tnec']}`",
        "",
        "## Delete / flip",
        "",
        "```json",
        json.dumps({"delete": out["delete"], "flip": out["flip"]}, indent=2),
        "```",
        "",
        "## What this run does NOT license",
        "",
        "Reading CONFIRM · Cap claim · Pine/TV/B5 · θ retune · instrument hop · arming.",
        "",
    ]
    (_HERE / "RESULTS_g2.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--explore-go", action="store_true")
    p.add_argument("--panel", type=Path, default=PANEL_DEFAULT)
    args = p.parse_args()
    cheap = run_cheap()
    print(json.dumps(cheap, indent=2))
    print(f"TNEC freeze template: {cheap['tnec_template']}")
    if not args.explore_go:
        print("Explore: BLOCKED (pass --explore-go after EXPLORE_GO.md + MYM_M15 restore)")
        return 0
    out = run_explore(args.panel)
    print(json.dumps(out, indent=2, default=str))
    (_HERE / "RESULTS.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    _write_results_md(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
