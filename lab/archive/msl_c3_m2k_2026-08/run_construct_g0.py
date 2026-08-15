"""MSL-C3-K2 Stage G0 runner — freeze recall always; path PnL GO-gated.

Usage:
  python run_construct_g0.py                 # freeze template + admission recall
  python run_construct_g0.py --explore-go    # requires EXPLORE_GO.md + M2K_M15 (W4 first)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parents[3]
sys.path.insert(0, str(_HERE))

import construct_lib as C  # noqa: E402

PANEL_DEFAULT = _REPO / C.M2K_PANEL_REL
SHA256SUMS = _REPO / "core" / "data" / "bar_data" / "SHA256SUMS"

# IS = sessions with date < 2025-09-01; CONFIRM never read
EXPLORE_END = __import__("datetime").date(2025, 8, 31)


def _expected_m2k_sha() -> str | None:
    if not SHA256SUMS.is_file():
        return C.M2K_SHA256
    text = SHA256SUMS.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace("*", " ").split()
        if len(parts) >= 2 and parts[-1].endswith("M2K_M15.csv"):
            return parts[0]
    return C.M2K_SHA256


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_panel_ok(panel: Path) -> None:
    if not panel.is_file():
        raise SystemExit(
            f"REFUSE: panel missing {panel} — run fresh W4 dry-run before pull "
            f"(STAGE0 §3 / PREREG_G0 §6)"
        )
    want = _expected_m2k_sha()
    if want is None:
        raise SystemExit(
            "REFUSE: no M2K_M15 sha pin in SHA256SUMS — complete W4 + manifest pin first"
        )
    got = _file_sha256(panel)
    if got != want:
        raise SystemExit(
            f"REFUSE: M2K_M15 sha mismatch\n  got  {got}\n  want {want}"
        )


def load_bars(panel: Path):
    import pandas as pd  # explore path only

    df = pd.read_csv(panel)
    if "time" not in df.columns:
        raise SystemExit("REFUSE: panel missing 'time' column")
    ts = pd.to_datetime(df["time"], utc=True)
    et = ts.dt.tz_convert("America/New_York")
    minute = et.dt.hour * 60 + et.dt.minute
    # Globex RTH-day key: bars from 18:00 ET onward attach to the next calendar
    # date so overnight [18:00 prior → 09:29] and RTH share one session (Axis B).
    cal = pd.DatetimeIndex(et).normalize()
    session_ts = cal + pd.to_timedelta((minute >= C.OVERNIGHT_OPEN_MIN).astype(int), unit="D")
    session = pd.DatetimeIndex(session_ts).date
    out = pd.DataFrame(
        {
            "session": session,
            "minute": minute.to_numpy(dtype=int),
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    return out[out["session"] <= EXPLORE_END].copy()


def run_cheap() -> dict:
    r = C.cheap_falsifier_freeze_ok()
    return {
        "verdict": r.verdict,
        "detail": r.detail,
        "rt_usd": r.rt_usd,
        "four_x_rt_usd": r.four_x_rt_usd,
        "k_intrinsic": C.K_INTRINSIC,
        "dsr_floor": C.DSR_FLOOR,
        "axes": list(C.AXES),
        "tnec_template": C.g0_freeze_verdict_template(),
        "explore_scored": False,
        "panel": str(PANEL_DEFAULT),
        "panel_present": PANEL_DEFAULT.is_file(),
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


def _collect(trades_by_sess: list[list[dict]], sess_meta: list, side: int):
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


def _gate_axis(long_c, short_c, delete, flip, aux) -> str:
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
        return "FALSIFIED"
    if _live_pass(long_c, aux["long"], long_del, long_flip_ok) or _live_pass(
        short_c, aux["short"], short_del, short_flip_ok
    ):
        return "SHAPE-CLEAR"
    return "AMBIGUOUS-HOLD"


def run_explore(panel: Path) -> dict:
    if not C.explore_go_present(_HERE):
        raise SystemExit("REFUSE: EXPLORE_GO.md missing — operator explore GO unpaid")
    assert_panel_ok(panel)
    df = load_bars(panel)
    sessions = sorted(df["session"].unique())
    by_sess = {s: g for s, g in df.groupby("session", sort=False)}

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

    def score_axis(axis_id: str) -> dict:
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
            if axis_id == C.AXIS_A:
                if np.isfinite(phi) and np.isfinite(plo):
                    constrained_by_sess.append(
                        C.simulate_axis_a_constrained(o, h, lo_, c, m, phi, plo)
                    )
                    flip_by_sess.append(C.simulate_axis_a_flip(o, h, lo_, c, m, phi, plo))
                else:
                    constrained_by_sess.append([])
                    flip_by_sess.append([])
                delete_by_sess.append(C.simulate_axis_a_delete_sham(o, h, lo_, c, m))
            else:
                constrained_by_sess.append(C.simulate_axis_b_constrained(o, h, lo_, c, m))
                flip_by_sess.append(C.simulate_axis_b_flip(o, h, lo_, c, m))
                if np.isfinite(phi) and np.isfinite(plo):
                    delete_by_sess.append(
                        C.simulate_axis_b_delete_sham(o, h, lo_, c, m, phi, plo)
                    )
                else:
                    delete_by_sess.append([])
            sess_meta.append(s)

        long_c, half_l, ann_l, pla_l, _ = _collect(constrained_by_sess, sess_meta, +1)
        short_c, half_s, ann_s, pla_s, _ = _collect(constrained_by_sess, sess_meta, -1)
        long_d, _, _, _, _ = _collect(delete_by_sess, sess_meta, +1)
        short_d, _, _, _, _ = _collect(delete_by_sess, sess_meta, -1)
        long_f, _, _, _, _ = _collect(flip_by_sess, sess_meta, +1)
        short_f, _, _, _, _ = _collect(flip_by_sess, sess_meta, -1)

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
        gate = _gate_axis(long_c, short_c, delete, flip, aux)
        pooled = C.pooled_mean_r(
            long_c["mean_R"], short_c["mean_R"], long_c["n"], short_c["n"]
        )
        coverage = sum(
            1
            for trades in constrained_by_sess
            if any(t["side"] in (+1, -1) for t in trades)
        )
        return {
            "axis": axis_id,
            "gate": gate,
            "long": long_c,
            "short": short_c,
            "delete": delete,
            "flip": flip,
            "aux": aux,
            "pooled_mean_R": pooled,
            "coverage_sessions_with_trade": coverage,
            "scored_sessions": len(sess_meta),
        }

    axis_a = score_axis(C.AXIS_A)
    axis_b = score_axis(C.AXIS_B)
    promoted = C.promote_axis(
        axis_a["gate"], axis_b["gate"], axis_a["pooled_mean_R"], axis_b["pooled_mean_R"]
    )
    if axis_a["gate"] == "FALSIFIED" and axis_b["gate"] == "FALSIFIED":
        overall = "FALSIFIED"
    elif promoted is None:
        overall = "FALSIFIED"
    elif axis_a["gate"] == "SHAPE-CLEAR" or axis_b["gate"] == "SHAPE-CLEAR":
        overall = "SHAPE-CLEAR"
    else:
        overall = "AMBIGUOUS-HOLD"

    tnec = C.format_tnec_verdict(
        {"N-SHAPE": "U"},
        bust="U",
        p_pass="U",
        mu_disclosed=(
            f"A:{axis_a['pooled_mean_R']:.4f}/B:{axis_b['pooled_mean_R']:.4f}"
            if np.isfinite(axis_a["pooled_mean_R"])
            else "U"
        ),
    )
    return {
        "gate": overall,
        "promoted_axis": promoted,
        "tnec": tnec,
        "k_intrinsic": C.K_INTRINSIC,
        "dsr_floor": C.DSR_FLOOR,
        "axes": {C.AXIS_A: axis_a, C.AXIS_B: axis_b},
        "disclosures": {
            "explore_end": str(EXPLORE_END),
            "confirm_reserved": "2025-09-01→2026-08-13",
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
        "# MSL-C3-K2 — EXPLORATION RESULTS (G0 dual-axis)",
        "",
        f"**Status:** `{out['gate']}`",
        f"**Date:** {out.get('scored_at', '')[:10]} · **Cost:** $0.00 · **K:** disclosure "
        f"(`K_intrinsic=2`, floor 0.850).",
        f"**Promoted axis:** `{out.get('promoted_axis')}`",
        f"**Explore GO:** [`EXPLORE_GO.md`](EXPLORE_GO.md)",
        f"**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md)",
        f"**Machine record:** [`RESULTS.json`](RESULTS.json)",
        "",
        "## Per-axis headline (IS only; CONFIRM unread)",
        "",
    ]
    for axis_id, block in out["axes"].items():
        lines += [
            f"### `{axis_id}` — gate `{block['gate']}`",
            "",
            "| Arm | n | mean net R | WR | session-block 95% CI |",
            "|---|---|---|---|---|",
        ]
        for name in ("long", "short"):
            a = block[name]
            ci = a.get("ci") or [None, None]
            lines.append(
                f"| {name.title()} | {a['n']} | {a['mean_R']:.4f} | "
                f"{a.get('wr', float('nan')):.3f} | [{ci[0]}, {ci[1]}] |"
            )
        lines.append("")
    lines += [
        f"**Overall gate:** `{out['gate']}` · **TNEC:** `{out['tnec']}`",
        "",
        "## What this run does NOT license",
        "",
        "Reading CONFIRM · Cap claim · Pine/TV/B5 · θ retune · K=1 drop · arming.",
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
        print(
            "Explore: BLOCKED (pass --explore-go after EXPLORE_GO.md + W4 + M2K_M15 pin)"
        )
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
