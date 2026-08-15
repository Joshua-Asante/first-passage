#!/usr/bin/env python3
"""Q-R2FLOW-1 Stage-G (G2) — score C1 on EXPLORATION TBBO only (OFCHAN cache reuse).

PREREG_G0.md §6 step 2. CONFIRM window is never opened.
Operator explore GO: cache reuse only — no new Databento pull.
Must pass test_flow_lib.py before this reads cache bytes.

Usage:
  .venv-research/Scripts/python.exe lab/archive/mnq_r2flow_routeb_2026-08/run_flow_g2.py
  .venv-research/Scripts/python.exe …/run_flow_g2.py --from-checkpoint   # reuse day scan
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import databento as db
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import flow_lib as fl  # noqa: E402

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

CACHE = (
    Path.home()
    / ".databento_cache"
    / "q_ofchan_1_exploration_tbbo"
    / "GLBX-20260807-EHX5KUSF7K"
)
EXPLORATION_START = date(2026, 2, 6)
EXPLORATION_END_EXCL = date(2026, 8, 6)
BATCH_ID = "GLBX-20260807-EHX5KUSF7K"
CHECKPOINT = HERE / "_g2_day_checkpoint.npz"  # local only; never commit


def _session_date_from_name(path: Path) -> date | None:
    # glbx-mdp3-YYYYMMDD.tbbo.dbn.zst
    stem = path.name.split(".")[0]
    ymd = stem.split("-")[-1]
    if len(ymd) != 8 or not ymd.isdigit():
        return None
    return date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))


def load_day_trade_arrays(
    path: Path,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (ts_ns, size, side, bid_px, ask_px) for trade-tagged TBBO in RTH pad.

    Pad 09:28–16:02 ET so 15:59+60s mid exists. Minute walk further restricts to RTH.
    """
    df = db.DBNStore.from_file(path).to_df()
    if "ts_event" not in df.columns:
        raise SystemExit(f"{path}: missing ts_event")
    if "action" in df.columns:
        df = df.loc[df["action"].astype(str) == "T"].copy()
    ts = pd.to_datetime(df["ts_event"], utc=True)
    et = ts.dt.tz_convert(ET)
    t0 = time(9, 28)
    t1 = time(16, 2)
    mask = (et.dt.time >= t0) & (et.dt.time <= t1)
    df = df.loc[mask].copy()
    ts = ts.loc[mask]
    if len(df) == 0:
        return (
            np.array([], dtype=np.int64),
            np.array([], dtype=float),
            np.array([], dtype=object),
            np.array([], dtype=float),
            np.array([], dtype=float),
        )
    order = np.argsort(ts.to_numpy())
    ts = ts.iloc[order]
    df = df.iloc[order]
    ts_ns = ts.to_numpy(dtype="datetime64[ns]").astype("int64")
    size = df["size"].to_numpy(dtype=float)
    side = df["side"].astype(str).to_numpy()
    bid_px = df["bid_px_00"].to_numpy(dtype=float)
    ask_px = df["ask_px_00"].to_numpy(dtype=float)
    ok = np.isfinite(bid_px) & np.isfinite(ask_px) & (bid_px > 0) & (ask_px > 0)
    ok &= np.isfinite(size) & (size > 0)
    return ts_ns[ok], size[ok], side[ok], bid_px[ok], ask_px[ok]


def rth_quote_span_ok(ts_ns: np.ndarray, session_day: date) -> bool:
    """True if quotes cover full RTH open through last+horizon (early-close detector)."""
    if len(ts_ns) == 0:
        return False
    open_ns = int(
        datetime.combine(session_day, fl.RTH_OPEN, tzinfo=ET)
        .astimezone(UTC)
        .timestamp()
        * 1e9
    )
    need_end = datetime.combine(session_day, time(16, 0), tzinfo=ET).astimezone(UTC)
    need_end_ns = int(need_end.timestamp() * 1e9)
    return int(ts_ns[0]) <= open_ns + 60_000_000_000 and int(ts_ns[-1]) >= need_end_ns


def _process_one_day(path_str: str) -> dict:
    """Worker: score one TBBO day file. Top-level for Windows spawn pickling."""
    path = Path(path_str)
    d = _session_date_from_name(path)
    if d is None:
        return {"kind": "skip", "skip": {"file": path.name, "reason": "bad_name"}}
    if d < EXPLORATION_START or d >= EXPLORATION_END_EXCL:
        return {
            "kind": "skip",
            "skip": {
                "file": path.name,
                "reason": "outside_exploration",
                "date": str(d),
            },
        }
    if not fl.is_rth_session(d):
        return {
            "kind": "skip",
            "skip": {
                "file": path.name,
                "reason": "excluded_calendar",
                "date": str(d),
            },
        }

    ts_ns, size, side, bid_px, ask_px = load_day_trade_arrays(path)
    if not rth_quote_span_ok(ts_ns, d):
        return {
            "kind": "skip",
            "skip": {
                "file": path.name,
                "reason": "incomplete_rth_span",
                "date": str(d),
                "n_rows": int(len(ts_ns)),
            },
        }

    a, r, n_ret, n_elig = fl.sample_pairs_for_day(ts_ns, size, side, bid_px, ask_px, d)
    if n_elig == 0:
        return {
            "kind": "skip",
            "skip": {"file": path.name, "reason": "zero_eligible", "date": str(d)},
        }
    if n_ret == 0:
        return {
            "kind": "elig_only",
            "date_ord": d.toordinal(),
            "n_elig": int(n_elig),
            "skip": {"file": path.name, "reason": "zero_retained", "date": str(d)},
        }
    return {
        "kind": "ok",
        "date_ord": d.toordinal(),
        "a": a.astype(np.float64),
        "r": r.astype(np.float64),
        "n_ret": int(n_ret),
        "n_elig": int(n_elig),
        "file": path.name,
    }


def scan_days(workers: int) -> tuple[
    list[tuple[np.ndarray, np.ndarray]],
    list[date],
    int,
    int,
    list[dict],
    int,
]:
    if not CACHE.is_dir():
        raise SystemExit(f"ABORT: EXPLORATION cache missing: {CACHE}")
    files = sorted(CACHE.glob("*.tbbo.dbn.zst"))
    if len(files) != 155:
        print(f"WARN: expected 155 day files, found {len(files)}")

    paths = [str(p) for p in files]
    print(f"day scan parallel workers={workers} files={len(paths)}", flush=True)

    results: list[dict] = []
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(_process_one_day, p): p for p in paths}
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 10 == 0 or done == len(paths):
                print(f"[{done}/{len(paths)}] days finished", flush=True)

    sessions: list[tuple[np.ndarray, np.ndarray]] = []
    session_dates: list[date] = []
    n_retained_total = 0
    n_eligible_total = 0
    skipped: list[dict] = []

    ok_rows = [r for r in results if r["kind"] == "ok"]
    ok_rows.sort(key=lambda r: int(r["date_ord"]))
    for r in ok_rows:
        sessions.append((r["a"], r["r"]))
        session_dates.append(date.fromordinal(int(r["date_ord"])))
        n_retained_total += int(r["n_ret"])
        n_eligible_total += int(r["n_elig"])

    for r in results:
        if r["kind"] == "skip":
            skipped.append(r["skip"])
        elif r["kind"] == "elig_only":
            skipped.append(r["skip"])
            n_eligible_total += int(r["n_elig"])

    print(
        f"day scan done: sessions={len(sessions)} retained={n_retained_total} "
        f"elig={n_eligible_total} skipped={len(skipped)}",
        flush=True,
    )
    return sessions, session_dates, n_retained_total, n_eligible_total, skipped, len(files)


def save_checkpoint(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    session_dates: list[date],
    n_retained: int,
    n_eligible: int,
    skipped: list[dict],
    n_day_files: int,
) -> None:
    payload = {
        "n_sessions": len(sessions),
        "n_retained": n_retained,
        "n_eligible": n_eligible,
        "n_day_files": n_day_files,
        "session_dates": np.array([d.toordinal() for d in session_dates], dtype=np.int64),
        "skipped_json": np.array(json.dumps(skipped)),
    }
    for i, (a, r) in enumerate(sessions):
        payload[f"a_{i}"] = a
        payload[f"r_{i}"] = r
    np.savez_compressed(CHECKPOINT, **payload)
    print(f"checkpoint written: {CHECKPOINT}", flush=True)


def load_checkpoint() -> tuple[
    list[tuple[np.ndarray, np.ndarray]],
    list[date],
    int,
    int,
    list[dict],
    int,
]:
    if not CHECKPOINT.is_file():
        raise SystemExit(f"ABORT: checkpoint missing: {CHECKPOINT}")
    z = np.load(CHECKPOINT, allow_pickle=False)
    n_s = int(z["n_sessions"])
    sessions = [(z[f"a_{i}"], z[f"r_{i}"]) for i in range(n_s)]
    session_dates = [date.fromordinal(int(x)) for x in z["session_dates"]]
    skipped = json.loads(str(z["skipped_json"]))
    return (
        sessions,
        session_dates,
        int(z["n_retained"]),
        int(z["n_eligible"]),
        skipped,
        int(z["n_day_files"]),
    )


def score_and_write(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    session_dates: list[date],
    n_retained_total: int,
    n_eligible_total: int,
    skipped: list[dict],
    n_day_files: int,
    placebo_workers: int = 6,
) -> int:
    coverage = (
        float(n_retained_total) / float(n_eligible_total) if n_eligible_total else 0.0
    )
    if sessions:
        a_all = np.concatenate([s[0] for s in sessions])
        r_all = np.concatenate([s[1] for s in sessions])
        rho = fl.pearson_rho(a_all, r_all)
    else:
        a_all = np.array([])
        r_all = np.array([])
        rho = float("nan")

    print(
        f"computing bootstrap CI (10k) via suff-stats — "
        f"n_sessions={len(sessions)} n_pairs={n_retained_total}…",
        flush=True,
    )
    ci = fl.session_block_bootstrap_rho(sessions, n=fl.N_BOOT, seed=fl.SEED)
    print(f"rho={rho} ci95={ci}", flush=True)

    lo, hi = ci
    ci_fails = (not (np.isfinite(lo) and np.isfinite(hi) and np.isfinite(rho))) or (
        lo <= 0.0 <= hi
    )
    if ci_fails:
        print("CI limb fails — skipping placebo (PREREG precedence)", flush=True)
        placebo = np.array([0.0])
        placebo_skipped = True
    else:
        print(
            f"computing placebo (1k) parallel threads={placebo_workers} "
            f"(SeedSequence.spawn)…",
            flush=True,
        )
        placebo = fl.within_session_r_shuffle_placebo_parallel(
            sessions, n=fl.N_PLACEBO, seed=fl.SEED, workers=placebo_workers
        )
        placebo_skipped = False
    h1, h2 = fl.halves_rho(sessions, session_dates)
    placebo_p95 = (
        float(np.percentile(np.abs(placebo), 95)) if len(placebo) else float("nan")
    )

    verdict = fl.verdict_g2(ci, rho, placebo, coverage, n_retained_total, h1, h2)
    candidates = fl.candidate_list(verdict)

    if len(r_all):
        sigma_r = float(np.std(r_all))
        census = {
            "n_retained": int(n_retained_total),
            "A_abs_p05": float(np.percentile(np.abs(a_all), 5)),
            "A_abs_p50": float(np.percentile(np.abs(a_all), 50)),
            "A_abs_p95": float(np.percentile(np.abs(a_all), 95)),
            "A_mean": float(np.mean(a_all)),
            "r_mean": float(np.mean(r_all)),
            "r_std": sigma_r,
            "r_abs_p50": float(np.percentile(np.abs(r_all), 50)),
            "r_abs_p95": float(np.percentile(np.abs(r_all), 95)),
        }
    else:
        census = {"n_retained": 0}

    payload = {
        "cell": "C1",
        "campaign": "Q-R2FLOW-1",
        "stage": "G2",
        "feature": "clock_minute_net_signed_aggressor_size",
        "window": {
            "role": "EXPLORATION",
            "start": str(EXPLORATION_START),
            "end_exclusive": str(EXPLORATION_END_EXCL),
        },
        "confirm_untouched": True,
        "confirm_reserved": "2025-09-01→2026-02-06",
        "explore_go": "operator_cache_reuse_2026-08-08",
        "new_databento_pull": False,
        "batch_id": BATCH_ID,
        "cache": str(CACHE),
        "n_day_files": n_day_files,
        "n_sessions_scored": len(sessions),
        "n_retained": int(n_retained_total),
        "n_eligible": int(n_eligible_total),
        "coverage": coverage,
        "rho": rho,
        "ci95": list(ci),
        "placebo_abs_p95": placebo_p95,
        "rho_h1": h1,
        "rho_h2": h2,
        "verdict": verdict,
        "candidates": candidates,
        "seed": fl.SEED,
        "n_boot": fl.N_BOOT,
        "n_placebo": fl.N_PLACEBO,
        "mag_floor": fl.MAG_FLOOR,
        "bootstrap_impl": "session_sufficient_statistics_equiv_concat",
        "day_scan": "ProcessPoolExecutor_parallel",
        "placebo_skipped_ci_precedence": placebo_skipped,
        "placebo_impl": "SeedSequence_spawn_threadpool"
        if not placebo_skipped
        else "skipped_ci_precedence",
        "placebo_workers": int(placebo_workers) if not placebo_skipped else 0,
        "excluded_session_dates": sorted(str(x) for x in fl.EXCLUDED_SESSION_DATES),
        "skipped": skipped,
        "census": census,
        "run_utc": datetime.now(tz=UTC).isoformat(),
        "fm5": "G2 promotion is candidate-only — not edge, admission, or harvest PASS",
        "cap_seat_claimed": False,
    }

    out_json = HERE / "RESULTS_g2.json"
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                k: payload[k]
                for k in (
                    "verdict",
                    "candidates",
                    "rho",
                    "ci95",
                    "coverage",
                    "n_retained",
                    "n_eligible",
                    "placebo_abs_p95",
                    "rho_h1",
                    "rho_h2",
                )
            },
            indent=2,
        )
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--from-checkpoint",
        action="store_true",
        help="Skip day scan; load _g2_day_checkpoint.npz and score only",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=max(1, min(6, (os.cpu_count() or 4) - 1)),
        help="Parallel day-scan workers (default: min(6, cpu-1))",
    )
    args = ap.parse_args()

    if args.from_checkpoint:
        sessions, session_dates, n_ret, n_elig, skipped, n_files = load_checkpoint()
        print(
            f"loaded checkpoint: sessions={len(sessions)} retained={n_ret} elig={n_elig}",
            flush=True,
        )
    else:
        sessions, session_dates, n_ret, n_elig, skipped, n_files = scan_days(
            workers=max(1, int(args.workers))
        )
        save_checkpoint(sessions, session_dates, n_ret, n_elig, skipped, n_files)

    return score_and_write(
        sessions,
        session_dates,
        n_ret,
        n_elig,
        skipped,
        n_files,
        placebo_workers=max(1, int(args.workers)),
    )


if __name__ == "__main__":
    raise SystemExit(main())
