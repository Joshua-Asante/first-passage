#!/usr/bin/env python3
"""Re-run of the ACTUAL MNQTAPE-1 Stage-G EXPLORATION harness
(scratchpad/mnqtape1/mnqtape1_g2.py, this session's own real execution artifact,
RESULTS_g2.json: rho_observed=0.07513760779902512, p_emp=0.20539730134932535,
n_usable=126), UNCHANGED in every computational respect, with ONE addition: dump
the final per-session (date, lti_norm, r_pm) arrays actually used to reach that
verdict, so the real r_pm(s) series can be reused (not re-derived under a
different judgment call) for the MNQTAPE-1 synthetic-signal power check.

The original scratchpad artifact (mnqtape1/mnqtape1_g2.py, mnqtape1/RESULTS_g2.json)
is NOT modified -- this is a separate copy. Re-running is legitimate: $0 cost,
cache-reuse only (per PREREG §7 step 2 / §8 item 2's already-given EXPLORATION GO),
no new Databento pull, and this script is expected to reproduce the identical
rho_observed / p_emp / n_usable as a correctness check before the dumped r_pm
array is trusted for anything downstream.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import databento as db
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

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

RTH_OPEN_NS = (9 * 3600 + 30 * 60) * 1_000_000_000
SPLIT_NS = (12 * 3600) * 1_000_000_000
RTH_CLOSE_NS = (16 * 3600) * 1_000_000_000

SIZE_MIN = 10
SEED = 20260822
M_PERM = 2000


def _session_date_from_name(path: Path) -> date | None:
    stem = path.name.split(".")[0]
    ymd = stem.split("-")[-1]
    if len(ymd) != 8 or not ymd.isdigit():
        return None
    return date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))


def classify_aggressor(price: np.ndarray, bid: np.ndarray, ask: np.ndarray) -> tuple[np.ndarray, bool, int]:
    n = price.size
    signs = np.full(n, np.nan)
    is_buy = price >= ask
    is_sell = (~is_buy) & (price <= bid)
    is_amb = ~(is_buy | is_sell)
    signs[is_buy] = 1.0
    signs[is_sell] = -1.0
    n_amb = int(is_amb.sum())
    dropped_first = False
    if n_amb == 0:
        return signs, dropped_first, n_amb

    last_price = None
    last_sign = None
    for i in range(n):
        if is_amb[i]:
            if last_price is None:
                dropped_first = True
                continue
            p = price[i]
            if p > last_price:
                s = 1.0
            elif p < last_price:
                s = -1.0
            else:
                s = last_sign
            signs[i] = s
            last_price = p
            last_sign = s
        else:
            last_price = price[i]
            last_sign = signs[i]
    return signs, dropped_first, n_amb


def _process_one_day(path_str: str) -> dict:
    path = Path(path_str)
    d = _session_date_from_name(path)
    if d is None:
        return {"date": None, "skip": "bad_filename", "file": path.name}
    if d < EXPLORATION_START or d >= EXPLORATION_END_EXCL:
        return {"date": str(d), "skip": "outside_exploration_window", "file": path.name}

    df = db.DBNStore.from_file(path).to_df()
    if df.empty:
        return {"date": str(d), "skip": "empty_file", "instrument_id": None}

    if "action" in df.columns:
        df = df.loc[df["action"].astype(str) == "T"].copy()
    if df.empty:
        return {"date": str(d), "skip": "no_trades", "instrument_id": None}

    ts_utc = pd.to_datetime(df["ts_event"], utc=True)
    et = ts_utc.dt.tz_convert(ET)
    ns_of_day = (et - et.dt.normalize()).dt.total_seconds().to_numpy() * 1e9

    rth_mask = (ns_of_day >= RTH_OPEN_NS) & (ns_of_day <= RTH_CLOSE_NS)
    if not rth_mask.any():
        return {"date": str(d), "skip": "no_rth_trades", "instrument_id": None}

    df = df.loc[rth_mask].copy()
    ns_of_day = ns_of_day[rth_mask]
    sequence = df["sequence"].to_numpy()

    order = np.lexsort((sequence, ns_of_day))
    df = df.iloc[order]
    ns_of_day = ns_of_day[order]

    price = df["price"].to_numpy(dtype=float)
    size = df["size"].to_numpy(dtype=np.int64)
    bid = df["bid_px_00"].to_numpy(dtype=float)
    ask = df["ask_px_00"].to_numpy(dtype=float)
    instrument_ids = df["instrument_id"].to_numpy()
    uniq_ids = np.unique(instrument_ids)
    instrument_id = int(uniq_ids[0]) if uniq_ids.size == 1 else None
    contains_intraday_switch = uniq_ids.size > 1

    quote_ok = np.isfinite(bid) & np.isfinite(ask) & (bid > 0) & (ask > 0)
    n_bad_quote = int((~quote_ok).sum())
    if n_bad_quote:
        price = price[quote_ok]
        size = size[quote_ok]
        bid = bid[quote_ok]
        ask = ask[quote_ok]
        ns_of_day = ns_of_day[quote_ok]
    if price.size == 0:
        return {"date": str(d), "skip": "no_valid_quotes", "instrument_id": instrument_id}

    signs, dropped_first, n_amb = classify_aggressor(price, bid, ask)

    am_mask = (ns_of_day <= SPLIT_NS) & np.isfinite(signs) & (size >= SIZE_MIN)
    am_size_sum = float(size[am_mask].sum()) if am_mask.any() else 0.0
    if am_size_sum == 0.0:
        return {
            "date": str(d),
            "skip": "empty_am_large_trade_population",
            "instrument_id": instrument_id,
            "n_amb": n_amb,
        }
    lti_norm = float((signs[am_mask] * size[am_mask]).sum() / am_size_sum)

    idx_12 = int(np.searchsorted(ns_of_day, SPLIT_NS, side="right")) - 1
    idx_16 = len(ns_of_day) - 1
    if idx_12 < 0:
        return {
            "date": str(d),
            "skip": "no_trade_at_or_before_1200",
            "instrument_id": instrument_id,
            "n_amb": n_amb,
        }
    p_12 = float(price[idx_12])
    p_16 = float(price[idx_16])
    if not (np.isfinite(p_12) and np.isfinite(p_16) and p_12 > 0 and p_16 > 0):
        return {
            "date": str(d),
            "skip": "invalid_target_price",
            "instrument_id": instrument_id,
            "n_amb": n_amb,
        }
    r_pm = float(np.log(p_16 / p_12))

    return {
        "date": str(d),
        "skip": None,
        "instrument_id": instrument_id,
        "contains_intraday_switch": bool(contains_intraday_switch),
        "lti_norm": lti_norm,
        "r_pm": r_pm,
        "n_rth_trades": int(len(ns_of_day)),
        "n_am_large_trades": int(am_mask.sum()),
        "am_size_sum": am_size_sum,
        "n_amb": n_amb,
        "dropped_first": bool(dropped_first),
        "n_bad_quote": n_bad_quote,
        "file": path.name,
    }


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    rho, _ = spearmanr(x, y)
    return float(rho)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    if not CACHE.is_dir():
        raise SystemExit(f"ABORT: EXPLORATION cache missing: {CACHE}")
    files = sorted(CACHE.glob("*.tbbo.dbn.zst"))
    print(f"[cache] {len(files)} day files found at {CACHE}", flush=True)

    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = {pool.submit(_process_one_day, str(p)): p for p in files}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 20 == 0 or done == len(files):
                print(f"[{done}/{len(files)}] day files processed", flush=True)

    results.sort(key=lambda r: r["date"] or "")

    ok_rows = [r for r in results if r.get("skip") is None]
    skipped_rows = [r for r in results if r.get("skip") is not None]

    roll_excluded_dates: list[str] = []
    prev_iid = None
    kept_after_roll: list[dict] = []
    for r in ok_rows:
        iid = r["instrument_id"]
        is_roll_day = bool(r.get("contains_intraday_switch"))
        if prev_iid is not None and iid is not None and iid != prev_iid:
            is_roll_day = True
        if is_roll_day:
            roll_excluded_dates.append(r["date"])
        else:
            kept_after_roll.append(r)
        if iid is not None:
            prev_iid = iid

    n_usable = len(kept_after_roll)
    lti = np.array([r["lti_norm"] for r in kept_after_roll], dtype=float)
    rpm = np.array([r["r_pm"] for r in kept_after_roll], dtype=float)
    dates_usable = [r["date"] for r in kept_after_roll]

    rho_obs = spearman_rho(lti, rpm) if n_usable >= 2 else float("nan")

    rng = np.random.default_rng(SEED)
    rho_null = np.empty(M_PERM)
    for k in range(M_PERM):
        perm = rng.permutation(n_usable)
        rho_null[k] = spearman_rho(lti, rpm[perm])

    n_ge = int(np.sum(rho_null >= rho_obs))
    p_emp = (1 + n_ge) / (M_PERM + 1)

    gate_a = n_usable >= 60
    gate_b = (rho_obs > 0)
    gate_c = (p_emp < 0.20)
    promote = gate_a and gate_b and gate_c

    print(json.dumps(
        {
            "n_sessions_scored_pre_roll": len(ok_rows),
            "n_roll_excluded": len(roll_excluded_dates),
            "n_usable": n_usable,
            "rho_observed": rho_obs,
            "p_emp": p_emp,
            "gate_a_n_usable_ge_60": gate_a,
            "gate_b_sign_positive": gate_b,
            "gate_c_p_emp_lt_0_20": gate_c,
            "PROMOTE": promote,
            "roll_excluded_dates": roll_excluded_dates,
        },
        indent=2, default=str,
    ), flush=True)

    # --- reproduction check against the real scratchpad artifact ---
    # The original Stage-G artifact (mnqtape1/RESULTS_g2.json) is scratchpad-only by the
    # pre-reg's own convention (not repo-tracked -- see RESULTS.md Reproducibility note),
    # so this comparison is skipped gracefully -- not aborted -- when that file isn't
    # sitting alongside this script (e.g. after this script is copied into the repo).
    # When this script was actually run to produce r_pm_series.json, the comparison DID
    # run and DID pass bit-identically (checks below, all True) -- see
    # power_check_2026-08-23's own RESULTS.md §1 and rerun_log.txt for that record.
    orig_path = Path(__file__).resolve().parent / "mnqtape1" / "RESULTS_g2.json"
    if orig_path.is_file():
        orig = json.loads(orig_path.read_text())
        checks = {
            "n_usable_matches": n_usable == orig["n_usable"],
            "rho_observed_matches": abs(rho_obs - orig["rho_observed"]) < 1e-9,
            "p_emp_matches": abs(p_emp - orig["p_emp"]) < 1e-9,
            "roll_dates_match": roll_excluded_dates == orig["roll_excluded_dates"],
        }
        print("REPRODUCTION CHECK vs original artifact:", json.dumps(checks, indent=2), flush=True)
    else:
        checks = {"skipped_original_artifact_not_found": str(orig_path)}
        print(
            f"REPRODUCTION CHECK skipped -- original artifact not found at {orig_path} "
            "(expected outside the original scratchpad; see RESULTS.md for the recorded "
            "bit-identical result from when this check actually ran)",
            flush=True,
        )

    # --- the actual deliverable: the real, ordered r_pm(s) series ---
    dump = {
        "n_usable": n_usable,
        "dates": dates_usable,
        "lti_norm": lti.tolist(),
        "r_pm": rpm.tolist(),
        "reproduction_check": checks,
        "source": "re-run of scratchpad/mnqtape1/mnqtape1_g2.py (this session's real "
                  "MNQTAPE-1 Stage-G execution artifact), unmodified computation, "
                  "output extended to dump per-session arrays",
    }
    out_path = Path(__file__).resolve().parent / "r_pm_series.json"
    out_path.write_text(json.dumps(dump, indent=2), encoding="utf-8")
    print(f"wrote {out_path}", flush=True)

    if orig_path.is_file() and not all(checks.values()):
        raise SystemExit("ABORT: reproduction check FAILED -- do not trust r_pm_series.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
