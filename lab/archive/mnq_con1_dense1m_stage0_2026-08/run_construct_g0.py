"""Q-MNQDTL-CON-1 Stage-0 runner - cheap falsifier always; path PnL GO-gated.

Usage:
  python run_construct_g0.py                 # cheap falsifier + freeze template
  python run_construct_g0.py --explore-go    # requires EXPLORE_GO.md; then scores
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ICT = _HERE.parents[1] / "ict_mnq_2026-08"
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ICT))

import build_w_export as B  # noqa: E402
import construct_lib as C  # noqa: E402

CACHE = Path.home() / ".databento_cache"
MNQ_DBN = CACHE / C.MNQ_DBN_DEFAULT
ES_DBN = CACHE / C.ES_DBN_DEFAULT


def run_cheap() -> dict:
    r = C.cheap_falsifier(
        prior_art_effect_pt=None, entry_named=True, sign_relative_contrarian=True
    )
    return {
        "verdict": r.verdict,
        "detail": r.detail,
        "em1_pred_pt": r.em1_pred_pt,
        "nedge_pred_pt": r.nedge_pred_pt,
        "em1_wr_bar": r.em1_wr_bar,
        "nedge_wr_bar": r.nedge_wr_bar,
        "prior_art_effect_pt": r.prior_art_effect_pt,
        "falsified_by_arithmetic": r.falsified_by_arithmetic,
        "tnec_template": C.g0_freeze_verdict_template(),
        "explore_scored": False,
        "panels": {
            "mnq_dbn": C.MNQ_DBN_DEFAULT,
            "es_dbn": C.ES_DBN_DEFAULT,
            "cost_usd": 0.0,
        },
    }


def _load_ohlc(path: Path) -> pd.DataFrame:
    import databento as db

    if not path.is_file():
        raise FileNotFoundError(f"missing panel: {path}")
    df = db.DBNStore.from_file(path).to_df()[["open", "high", "low", "close"]]
    return df.sort_index()


def _sessionize_joined(mnq: pd.DataFrame, es: pd.DataFrame) -> pd.DataFrame:
    """Inner-join on UTC bar open; keep RTH 09:30–15:59 ET; tag session date."""
    both = mnq.join(es, how="inner", lsuffix="_mnq", rsuffix="_es")
    ts = both.index
    if ts.tz is None:
        ts = ts.tz_localize("UTC")
    et = ts.tz_convert("America/New_York")
    minute = et.hour * 60 + et.minute
    keep = (minute >= C.RTH_OPEN_MIN) & (minute < C.RTH_CLOSE_MIN)
    et_k = et[keep]
    sub = both.loc[keep]
    return pd.DataFrame(
        {
            "session": pd.DatetimeIndex(et_k).normalize().date,
            "open": sub["open_mnq"].to_numpy(dtype=float),
            "high": sub["high_mnq"].to_numpy(dtype=float),
            "low": sub["low_mnq"].to_numpy(dtype=float),
            "close_mnq": sub["close_mnq"].to_numpy(dtype=float),
            "close_es": sub["close_es"].to_numpy(dtype=float),
        }
    )


def _parse_go_window(token_path: Path) -> tuple[date | None, date | None]:
    """Optional `start:` / `end:` YYYY-MM-DD lines in EXPLORE_GO.md; else full panel."""
    text = token_path.read_text(encoding="utf-8")
    start = end = None
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith("start:"):
            start = date.fromisoformat(s.split(":", 1)[1].strip())
        elif s.lower().startswith("end:"):
            end = date.fromisoformat(s.split(":", 1)[1].strip())
    return start, end


def run_explore(token_path: Path) -> dict:
    print("EXPLORE: loading MNQ + ES 1m continuous ($0 cache reuse)...")
    mnq = _load_ohlc(MNQ_DBN)
    es = _load_ohlc(ES_DBN)
    df = _sessionize_joined(mnq, es)
    start, end = _parse_go_window(token_path)
    if start is not None:
        df = df[df["session"] >= start]
    if end is not None:
        df = df[df["session"] <= end]

    sessions = sorted(df["session"].unique())
    # Pre-compute per-session abs(d) for theta (all non-roll sessions in frame)
    abs_d_by_session: list[np.ndarray] = []
    sess_meta: list[dict] = []
    for sess in sessions:
        grp = df[df["session"] == sess]
        if len(grp) < 60:
            abs_d_by_session.append(np.array([]))
            sess_meta.append({"session": sess, "skip": "short", "roll": False})
            continue
        roll = bool(B.in_roll_window(sess))
        d = C.divergence_series_vec(
            grp["close_es"].to_numpy(), grp["close_mnq"].to_numpy()
        )
        abs_d_by_session.append(np.abs(d[np.isfinite(d)]))
        sess_meta.append(
            {
                "session": sess,
                "skip": "roll" if roll else None,
                "roll": roll,
                "grp": grp,
                "d": d,
            }
        )

    long_trades: list[dict] = []
    short_trades: list[dict] = []
    long_packs: list[dict] = []
    short_packs: list[dict] = []
    # daily R series over scored (non-roll, theta-ready) sessions
    long_daily: list[float] = []
    short_daily: list[float] = []
    n_eligible_sessions = 0
    n_signal_sessions = 0

    for i, meta in enumerate(sess_meta):
        if meta.get("skip"):
            continue
        theta = C.session_theta(abs_d_by_session, i)
        if not np.isfinite(theta) or theta <= 0.0:
            continue
        n_eligible_sessions += 1
        grp = meta["grp"]
        d = meta["d"]
        o = grp["open"].to_numpy()
        h = grp["high"].to_numpy()
        l = grp["low"].to_numpy()
        c = grp["close_mnq"].to_numpy()
        trades = C.simulate_session_trades(o, h, l, c, d, theta)
        if trades:
            n_signal_sessions += 1
        sess = meta["session"]
        long_r_sum = 0.0
        short_r_sum = 0.0
        long_clocks: list[int] = []
        short_clocks: list[int] = []
        for tr in trades:
            row = {
                "session": sess,
                "entry_i": tr["entry_i"],
                "side": tr["side"],
                "pts": tr["pts"],
                "kind": tr["kind"],
                "R": tr["R"],
            }
            if tr["side"] > 0:
                long_trades.append(row)
                long_clocks.append(tr["entry_i"])
                long_r_sum += tr["R"]
            else:
                short_trades.append(row)
                short_clocks.append(tr["entry_i"])
                short_r_sum += tr["R"]
        long_daily.append(long_r_sum)
        short_daily.append(short_r_sum)
        # Placebo packs: path-R on signal-eligible clocks (|d|>=θ), same side.
        # Entry positions are remapped into this eligible pool for shuffling.
        eligible = np.flatnonzero(
            np.isfinite(d) & (np.abs(d) >= theta)
        ).astype(int)
        if len(eligible) == 0:
            eligible = np.arange(len(o), dtype=int)

        def _pack(side: int, entry_clocks: list[int]) -> dict | None:
            if not entry_clocks:
                return None
            # Map each entry clock to its index inside `eligible` (exact match).
            el_list = eligible.tolist()
            pos = []
            for t in entry_clocks:
                try:
                    pos.append(el_list.index(int(t)))
                except ValueError:
                    pos.append(0)
            return {
                "entry_clocks": np.asarray(pos, dtype=int),
                "path_r_all_clocks": C.path_r_at_clocks(
                    o, h, l, c, side, eligible
                ),
            }

        lp = _pack(+1, long_clocks)
        if lp is not None:
            long_packs.append(lp)
        sp = _pack(-1, short_clocks)
        if sp is not None:
            short_packs.append(sp)

    print(
        f"  joined RTH bars={len(df):,} sessions={len(sessions):,} "
        f"eligible(theta)={n_eligible_sessions:,} signal_sessions={n_signal_sessions:,}"
    )
    print("  scoring long arm...")
    long_score = C.score_arm_full(long_trades, long_packs, long_daily)
    print("  scoring short arm...")
    short_score = C.score_arm_full(short_trades, short_packs, short_daily)
    overall = C.overall_explore_verdict(long_score["verdict"], short_score["verdict"])

    # TNEC: N-SHAPE from explore; others remain U until their GO
    n_shape = "P" if overall == "SHAPE-CLEAR" else ("F" if overall == "FALSIFIED" else "U")
    tnec = C.format_tnec_verdict({"N-SHAPE": n_shape})

    trades_per_eligible = (
        (len(long_trades) + len(short_trades)) / n_eligible_sessions
        if n_eligible_sessions
        else float("nan")
    )
    coverage = (
        n_signal_sessions / n_eligible_sessions if n_eligible_sessions else float("nan")
    )

    out = {
        "status": overall,
        "tnec": tnec,
        "cost_usd": 0.0,
        "k_intrinsic": C.K_INTRINSIC,
        "window": {
            "start": start.isoformat() if start else "panel_start",
            "end": end.isoformat() if end else "panel_end",
            "n_sessions_raw": len(sessions),
            "n_eligible_sessions": n_eligible_sessions,
            "n_signal_sessions": n_signal_sessions,
        },
        "panels": {"mnq_dbn": C.MNQ_DBN_DEFAULT, "es_dbn": C.ES_DBN_DEFAULT},
        "geometry": {
            "G": C.GATE_G,
            "RT": C.RT_PT,
            "lookback_min": C.LOOKBACK_MIN,
            "theta_sessions": C.THETA_SESSIONS,
            "exit": "session_flat",
        },
        "long": long_score,
        "short": short_score,
        "disclose": {
            "trades_per_eligible_session": trades_per_eligible,
            "frac_eligible_with_trade": coverage,
            "em": "Y Y Y Y Y Y",  # stop+R exist; EM3 one-pos; arms separate — shape class
        },
        "scored_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return out


def _write_results(out: dict) -> None:
    (_HERE / "RESULTS.json").write_text(
        json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8"
    )
    lines = [
        "# Q-MNQDTL-CON-1 — EXPLORATION RESULTS (G0)",
        "",
        f"**Status:** `{out['status']}`",
        f"**TNEC:** `{out['tnec']}`",
        f"**Cost:** ${out['cost_usd']:.4f} · K_intrinsic={out['k_intrinsic']}",
        f"**Window:** {out['window']['start']} → {out['window']['end']} "
        f"(eligible sessions {out['window']['n_eligible_sessions']})",
        "",
        "## Long",
        f"- n={out['long']['n']} mean_R={out['long']['mean_R']:.4f} "
        f"CI={out['long']['ci95']} WR={out['long']['wr']:.3f}",
        f"- placebo_p={out['long']['placebo_p']} halves={out['long']['halves']}",
        f"- annSR={out['long']['ann_sr']:.3f} DSR={out['long']['dsr']:.3f} "
        f"verdict=`{out['long']['verdict']}`",
        "",
        "## Short",
        f"- n={out['short']['n']} mean_R={out['short']['mean_R']:.4f} "
        f"CI={out['short']['ci95']} WR={out['short']['wr']:.3f}",
        f"- placebo_p={out['short']['placebo_p']} halves={out['short']['halves']}",
        f"- annSR={out['short']['ann_sr']:.3f} DSR={out['short']['dsr']:.3f} "
        f"verdict=`{out['short']['verdict']}`",
        "",
        "## Disclose",
        f"- trades/eligible session: {out['disclose']['trades_per_eligible_session']:.3f}",
        f"- frac eligible with ≥1 trade: {out['disclose']['frac_eligible_with_trade']:.3f}",
        f"- EM six-char (class): {out['disclose']['em']}",
        "",
        "Cap not claimed. Confirm / N-SURV / deploy unpaid.",
        "",
    ]
    (_HERE / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {_HERE / 'RESULTS.json'}")
    print(f"wrote {_HERE / 'RESULTS.md'}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--explore-go",
        action="store_true",
        help="Attempt EXPLORATION path PnL (requires EXPLORE_GO.md token)",
    )
    args = ap.parse_args(argv[1:])

    print("Q-MNQDTL-CON-1 Stage-0 - ES/NQ divergence construct")
    print("PREREG: lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md")
    print(
        f"FROZEN G={C.GATE_G} session-flat RT={C.RT_PT} lookback={C.LOOKBACK_MIN} "
        f"theta_sessions={C.THETA_SESSIONS} K={C.K_INTRINSIC}\n"
    )

    cheap = run_cheap()
    print("CHEAP FALSIFIER")
    print(f"  verdict: {cheap['verdict']}")
    print(f"  detail:  {cheap['detail']}")
    print(f"  EM1 pred >= {cheap['em1_pred_pt']:.2f} pt  WR bar {cheap['em1_wr_bar']:.4f}")
    print(
        f"  N-EDGE pred >= {cheap['nedge_pred_pt']:.2f} pt  "
        f"WR bar {cheap['nedge_wr_bar']:.4f}"
    )
    print(f"  TNEC template: {cheap['tnec_template']}")
    print(f"  panels (cache reuse $0): MNQ={C.MNQ_DBN_DEFAULT}")
    print(f"                           ES ={C.ES_DBN_DEFAULT}")

    if not args.explore_go:
        print("\nEXPLORE: blocked (no --explore-go). Con-3: Stage-0 GO unpaid.")
        print("  Drop EXPLORE_GO.md + pass --explore-go after operator GO to score.")
        return 0 if cheap["verdict"] == "CHEAP_FALSIFIER_OK" else 1

    if not C.explore_go_present(_HERE):
        print("\nEXPLORE: BLOCKED - missing EXPLORE_GO.md (operator token).")
        print("  Refusing real-panel path PnL. No RESULTS written.")
        return 2

    if cheap["verdict"] != "CHEAP_FALSIFIER_OK":
        print("\nEXPLORE: BLOCKED - cheap falsifier not OK.")
        return 1

    token = _HERE / "EXPLORE_GO.md"
    out = run_explore(token)
    _write_results(out)
    print(f"\nEXPLORE VERDICT: {out['status']}")
    print(f"  TNEC: {out['tnec']}")
    print(f"  long={out['long']['verdict']}  short={out['short']['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
