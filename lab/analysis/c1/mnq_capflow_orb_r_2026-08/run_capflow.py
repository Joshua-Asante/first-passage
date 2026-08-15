#!/usr/bin/env python3
"""Q-CAPFLOW-1 Cap-spend — THE SINGLE RUN.

Joins parent N14 triggers to unmodified orb_backtest R (FM-1 break scoped here),
computes OR-window signed aggressor A from TBBO (OFCHAN day reuse + optional gap
pull via pull_or_windows.py), scores Pearson ρ(A,R) under CAPA-shaped W0–W5.

Protocol: tests green → estimate → reuse/pull → this script once.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import databento as db
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "mnq_orb_flow_substrate_2026-08-05"
# parents[1] = lab/analysis (theme nest); parents[2] wrongly pointed at lab/orb/
ORB_LIB_DIR = HERE.parents[1] / "orb" / "orb_universe_2026-06-22"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ORB_LIB_DIR))
import capflow_lib as cl  # noqa: E402
import orb_lib as ol  # noqa: E402

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

CACHE_OFCHAN = (
    Path.home()
    / ".databento_cache"
    / "q_ofchan_1_exploration_tbbo"
    / "GLBX-20260807-EHX5KUSF7K"
)
CACHE_GAP = Path.home() / ".databento_cache" / "q_capflow_1_or_tbbo_gap"
GAP_BLOB = CACHE_GAP / "gap_20250806_20260206.tbbo.dbn"
CACHE_1M = Path.home() / ".databento_cache" / "ohlcv-1m_continuous_13b1f5f7c85e3bce.dbn"
EVENTS = PARENT / "events.parquet"
WIN_START = "2025-08-06"
WIN_END = "2026-08-04"
OFCHAN_START = date(2026, 2, 6)
_GAP_DAY_CACHE: dict[date, tuple] = {}

MNQ = ol.Instrument(
    name="MNQ_native",
    path=Path("(built-in-memory)"),
    loader="none",
    feed="databento",
    tick=0.25,
    spread_pt=0.25,
    rt_cost_pt=1.11,
    open_tod=ol.OPEN_TOD_US,
    close_tod=ol.CLOSE_TOD_US,
    tz="America/New_York",
    note="native MNQ.v.0 1m->15m; CapFLOW R join",
)


def load_1m() -> pd.DataFrame:
    raw = db.DBNStore.from_file(CACHE_1M).to_df()
    raw.index = raw.index.tz_convert(ET)
    return raw[["open", "high", "low", "close", "volume"]].sort_index()


def to_15m(raw: pd.DataFrame) -> pd.DataFrame:
    o = raw["open"].resample("15min", label="left", closed="left").first()
    h = raw["high"].resample("15min", label="left", closed="left").max()
    lo = raw["low"].resample("15min", label="left", closed="left").min()
    cl = raw["close"].resample("15min", label="left", closed="left").last()
    v = raw["volume"].resample("15min", label="left", closed="left").sum()
    bars = pd.DataFrame({"open": o, "high": h, "low": lo, "close": cl, "volume": v})
    bars = bars.dropna(subset=["open", "high", "low", "close"])
    epoch_ms = bars.index.tz_convert("UTC").view("int64") // 1_000_000
    df = pd.DataFrame(
        {
            "epoch": np.asarray(epoch_ms, dtype="int64"),
            "open": bars["open"].to_numpy(),
            "high": bars["high"].to_numpy(),
            "low": bars["low"].to_numpy(),
            "close": bars["close"].to_numpy(),
            "volume": bars["volume"].to_numpy().astype("int64"),
        }
    )
    return ol._finalize(df)


def trade_days(piv, inst: ol.Instrument, *, or_bars: int = 2) -> list:
    h, l, c = piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    or_tods, rest_tods = tods[:or_bars], tods[or_bars:]
    days = []
    for day in c.index:
        or_hi = h.loc[day, or_tods].max()
        or_lo = l.loc[day, or_tods].min()
        if not np.isfinite(or_hi) or not np.isfinite(or_lo):
            continue
        if (or_hi - or_lo) <= 0:
            continue
        for t in rest_tods:
            bh, bl = h.loc[day, t], l.loc[day, t]
            if not np.isfinite(bh):
                continue
            if bh >= or_hi or bl <= or_lo:
                days.append(day)
                break
    return days


def join_r_by_trigger_id() -> dict[int, float]:
    """Unmodified orb_backtest R keyed by trigger_id (= engine trade index)."""
    raw = load_1m()
    raw = raw.loc[
        (raw.index >= pd.Timestamp(WIN_START, tz=ET))
        & (raw.index < pd.Timestamp(WIN_END, tz=ET) + pd.Timedelta(days=1))
    ]
    df15 = to_15m(raw)
    piv, meta = ol.session_panel(df15, MNQ)
    bt = ol.orb_backtest(piv, meta, MNQ, or_bars=2)
    days = trade_days(piv, MNQ)
    assert len(days) == len(bt["R"]), (
        f"day-mapping count {len(days)} != engine n {len(bt['R'])}"
    )
    return {int(i): float(bt["R"][i]) for i in range(len(bt["R"]))}


def _session_date_from_name(path: Path) -> date | None:
    stem = path.name.split(".")[0]
    ymd = stem.split("-")[-1]
    if len(ymd) != 8 or not ymd.isdigit():
        return None
    return date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))


def resolve_day_file(d: date) -> Path | None:
    # Prefer OFCHAN zst day files, then gap day parquet/dbn, then gap blob.
    name_zst = f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.dbn.zst"
    p = CACHE_OFCHAN / name_zst
    if p.exists():
        return p
    pq = CACHE_GAP / f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.parquet"
    if pq.exists():
        return pq
    name2 = f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.dbn"
    for root in (CACHE_OFCHAN, CACHE_GAP):
        p = root / name2
        if p.exists():
            return p
    if d < OFCHAN_START and GAP_BLOB.exists():
        return GAP_BLOB
    return None


def load_day_trade_arrays(
    path: Path,
    session_day: date | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (ts_ns, size, side) for action=T prints (RTH pad 09:28–16:02 ET).

    When path is the continuous GAP_BLOB, pass session_day to filter that calendar day.
    """
    global _GAP_DAY_CACHE
    if path.resolve() == GAP_BLOB.resolve() and session_day is not None:
        if session_day in _GAP_DAY_CACHE:
            return _GAP_DAY_CACHE[session_day]

    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = db.DBNStore.from_file(path).to_df()
    if "ts_event" not in df.columns:
        raise SystemExit(f"{path}: missing ts_event")
    if "action" in df.columns:
        df = df.loc[df["action"].astype(str) == "T"].copy()
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert(ET)
    if path.resolve() == GAP_BLOB.resolve() and session_day is not None:
        mask_day = et.dt.date == session_day
        df = df.loc[mask_day].copy()
        ts = ts.loc[mask_day]
        et = et.loc[mask_day]
    mask = (et.dt.time >= time(9, 28)) & (et.dt.time <= time(16, 2))
    df = df.loc[mask].copy()
    ts = ts.loc[mask]
    if len(df) == 0:
        empty = (
            np.array([], dtype=np.int64),
            np.array([], dtype=float),
            np.array([], dtype=object),
        )
        if path.resolve() == GAP_BLOB.resolve() and session_day is not None:
            _GAP_DAY_CACHE[session_day] = empty
        return empty
    order = np.argsort(ts.to_numpy())
    ts = ts.iloc[order]
    df = df.iloc[order]
    ts_ns = ts.to_numpy(dtype="datetime64[ns]").astype("int64")
    size = df["size"].to_numpy(dtype=float)
    side = df["side"].astype(str).to_numpy()
    ok = np.isfinite(size) & (size > 0)
    out = (ts_ns[ok], size[ok], side[ok])
    if path.resolve() == GAP_BLOB.resolve() and session_day is not None:
        _GAP_DAY_CACHE[session_day] = out
    return out


def _process_day(args: tuple) -> dict:
    """Worker: score all triggers for one session date."""
    date_str, path_str, trig_rows = args
    d = date.fromisoformat(date_str)
    path = Path(path_str) if path_str else None
    if path is None or not path.exists():
        return {
            "date": date_str,
            "pairs": [
                {"trigger_id": int(r["trigger_id"]), "A": None, "R": r["R"], "reason": "no_day_file"}
                for r in trig_rows
            ],
        }
    ts_ns, size, side = load_day_trade_arrays(path, session_day=d)
    t0 = cl.or_start_ns(d)
    out = []
    for r in trig_rows:
        t1 = int(pd.Timestamp(r["ts_et"]).tz_convert("UTC").timestamp() * 1e9)
        a = cl.signed_aggressor_sum(ts_ns, size, side, t0, t1)
        out.append(
            {
                "trigger_id": int(r["trigger_id"]),
                "A": a,
                "R": r["R"],
                "reason": None if a is not None else "no_ba_prints",
            }
        )
    return {"date": date_str, "pairs": out}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument(
        "--allow-partial",
        action="store_true",
        help="Score with available day files even if coverage will VOID (diagnostics).",
    )
    args = ap.parse_args()

    if not EVENTS.exists():
        raise SystemExit(
            f"ABORT: parent events missing at {EVENTS} — rebuild via parent build_events.py "
            f"or copy local events.parquet into the parent dir"
        )
    if not CACHE_1M.exists():
        raise SystemExit(f"ABORT: 1m panel missing at {CACHE_1M}")

    ev = pd.read_parquet(EVENTS)
    trig = ev[ev["kind"] == "trigger"].copy()
    trig["ts_et"] = pd.to_datetime(trig["ts_et"])
    if trig["ts_et"].dt.tz is None:
        trig["ts_et"] = trig["ts_et"].dt.tz_localize(ET)
    else:
        trig["ts_et"] = trig["ts_et"].dt.tz_convert(ET)
    n_trig = int(len(trig))

    print(f"[join] rebuilding orb_backtest R for {n_trig} triggers …")
    r_map = join_r_by_trigger_id()
    missing_r = [int(i) for i in trig["trigger_id"] if int(i) not in r_map]
    if missing_r:
        raise SystemExit(f"ABORT: R join missing trigger_ids {missing_r[:5]}…")
    trig["R"] = trig["trigger_id"].map(lambda i: r_map[int(i)])

    # Group by session date
    by_day: dict[str, list[dict]] = {}
    gap_days: list[str] = []
    ofchan_days: list[str] = []
    for _, row in trig.iterrows():
        d = pd.Timestamp(row["date"]).date()
        ds = d.isoformat()
        path = resolve_day_file(d)
        by_day.setdefault(ds, []).append(
            {
                "trigger_id": int(row["trigger_id"]),
                "ts_et": row["ts_et"].isoformat(),
                "R": float(row["R"]),
            }
        )
        if path is None:
            if ds not in gap_days:
                gap_days.append(ds)
        else:
            try:
                if ds not in ofchan_days and CACHE_OFCHAN in path.parents:
                    ofchan_days.append(ds)
            except Exception:
                pass

    n_gap = len(gap_days)
    print(f"[cache] trigger days={len(by_day)}  gap_days_missing={n_gap}  "
          f"ofchan_reuse_days~={len(by_day) - n_gap}")
    if n_gap and not args.allow_partial:
        est_path = HERE / "ESTIMATE_gap.json"
        hint = (
            f"ABORT: {n_gap} trigger session days lack TBBO day files. "
            f"Prefer OFCHAN reuse; estimate/pull gaps via pull_or_windows.py "
            f"(budget ≤ $50). Missing sample: {gap_days[:5]}"
        )
        if est_path.exists():
            hint += f"\nSee {est_path}"
        raise SystemExit(hint)

    work = []
    for ds, rows in sorted(by_day.items()):
        d = date.fromisoformat(ds)
        p = resolve_day_file(d)
        work.append((ds, str(p) if p else "", rows))

    results_pairs: list[dict] = []
    if args.workers <= 1:
        for item in work:
            results_pairs.extend(_process_day(item)["pairs"])
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futs = [pool.submit(_process_day, item) for item in work]
            for fut in as_completed(futs):
                results_pairs.extend(fut.result()["pairs"])

    # Align coverage to all parent triggers
    by_tid = {int(p["trigger_id"]): p for p in results_pairs}
    pairs_for_assemble = []
    covered = 0
    for _, row in trig.iterrows():
        tid = int(row["trigger_id"])
        p = by_tid.get(tid, {})
        a = p.get("A")
        r = float(row["R"])
        d = pd.Timestamp(row["date"]).date()
        if a is not None and np.isfinite(a):
            covered += 1
            pairs_for_assemble.append((float(a), r, d))
        else:
            pairs_for_assemble.append((None, r, d))

    coverage = covered / n_trig if n_trig else 0.0
    sessions, dates, dropped = cl.assemble_trigger_sessions(pairs_for_assemble)

    if covered < cl.N_MIN:
        out = dict(
            verdict="VOID-POWER",
            n_triggers=n_trig,
            coverage_covered=covered,
            coverage=float(coverage),
            cap_spent=False,
            gap_days_missing=n_gap,
            c11_non_claims=True,
        )
        (HERE / "RESULTS.json").write_text(json.dumps(out, indent=2))
        _write_results_md(out)
        print(f"VERDICT: VOID-POWER  covered={covered} < {cl.N_MIN}")
        return 0
    if coverage < cl.COV_MIN:
        out = dict(
            verdict="VOID-COVERAGE",
            n_triggers=n_trig,
            coverage_covered=covered,
            coverage=float(coverage),
            cap_spent=False,
            gap_days_missing=n_gap,
            c11_non_claims=True,
        )
        (HERE / "RESULTS.json").write_text(json.dumps(out, indent=2))
        _write_results_md(out)
        print(f"VERDICT: VOID-COVERAGE  coverage={coverage:.4f} < {cl.COV_MIN}")
        return 0

    a_all = np.concatenate([s[0] for s in sessions])
    r_all = np.concatenate([s[1] for s in sessions])
    obs = cl.pearson_rho(a_all, r_all)
    disc = cl.mean_split_delta(a_all, r_all)
    ci = cl.session_block_bootstrap_rho(sessions)
    placebo = cl.within_session_r_shuffle_placebo(sessions)
    p95 = float(np.percentile(np.abs(placebo), 95))
    p_emp = float((np.abs(placebo) >= abs(obs)).mean())
    h1, h2 = cl.halves_rho(sessions, dates)
    verdict = cl.verdict_capflow(ci, obs, placebo, coverage, covered, h1, h2)
    spent = cl.cap_spent(verdict)

    out = dict(
        verdict=verdict,
        cap_spent=spent,
        n_triggers=n_trig,
        n_sessions_used=int(len(sessions)),
        coverage=float(coverage),
        coverage_covered=int(covered),
        dropped_uncovered=int(dropped),
        rho=float(obs),
        mean_split_delta_disclosure=float(disc) if np.isfinite(disc) else None,
        ci95=[float(ci[0]), float(ci[1])],
        placebo_abs_p95=p95,
        placebo_p_emp=p_emp,
        mag_floor=cl.MAG_FLOOR,
        by_half=dict(h1_rho=float(h1), h2_rho=float(h2)),
        gap_days_missing=n_gap,
        ofchan_reuse=True,
        seed=cl.SEED,
        n_boot=cl.N_BOOT,
        n_placebo=cl.N_PLACEBO,
        k_intrinsic=1 if spent else 0,
        feature="or_window_net_signed_aggressor_size",
        target="orb_backtest_R",
        c11_non_claims=True,
        non_claims=[
            "not_an_ORB_entry_filter",
            "not_Tradeify_unpark",
            "not_resting_L1_retune",
            "not_Pine_or_rail",
        ],
    )
    (HERE / "RESULTS.json").write_text(json.dumps(out, indent=2))
    _write_results_md(out)
    print("=" * 78)
    print(f"Q-CAPFLOW-1 Cap-spend — VERDICT: {verdict}   cap_spent={spent}")
    print("=" * 78)
    print(f"triggers            : {n_trig}")
    print(f"coverage            : {coverage:.4f}  ({covered}/{n_trig})")
    print(f"sessions used       : {len(sessions)}")
    print(f"rho                 : {obs:+.6f}   CI95 [{ci[0]:+.6f}, {ci[1]:+.6f}]")
    print(f"disclosure Δ        : {disc:+.6f}" if np.isfinite(disc) else "disclosure Δ        : nan")
    print(f"placebo |.| p95     : {p95:.6f}    p_emp = {p_emp:.4f}")
    print(f"by-half             : H1 {h1:+.6f}  H2 {h2:+.6f}")
    print(f"C11 non-claims      : confirmed (no ORB gate / unpark)")
    print(f"[write] {HERE / 'RESULTS.json'}")
    return 0


def _write_results_md(out: dict) -> None:
    spent = out.get("cap_spent", False)
    lines = [
        "# Q-CAPFLOW-1 — CapFLOW RESULTS",
        "",
        f"**Verdict:** `{out.get('verdict')}` · **cap_spent:** `{spent}`",
        f"**Date:** 2026-08-08",
        "",
        "## Score",
        "",
        f"- n_triggers: {out.get('n_triggers')}",
        f"- coverage: {out.get('coverage')} ({out.get('coverage_covered')}/{out.get('n_triggers')})",
        f"- ρ: {out.get('rho')}",
        f"- CI95: {out.get('ci95')}",
        f"- placebo |·| p95: {out.get('placebo_abs_p95')}",
        f"- halves: {out.get('by_half')}",
        f"- disclosure mean-split Δ: {out.get('mean_split_delta_disclosure')}",
        f"- gap_days_missing: {out.get('gap_days_missing')}",
        "",
        "## C11 / F2 non-claims (confirmed)",
        "",
        "- Not an ORB entry filter / gate.",
        "- Not a Tradeify unpark license.",
        "- Not a resting-L1 / N14 retune.",
        "- Not Pine / rail / Striker redeploy.",
        "",
        "Positive CapFLOW (if any) is companion/conditioner research only under a later GO.",
        "",
    ]
    (HERE / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
