#!/usr/bin/env python3
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
# Q-FEED-1 closed RESOLVED-BY-RETIREMENT. Reads core/data/bar_data/*_duka.csv,
# DELETED by docs/adr/2026-07-22-challenge-era-substrate-retirement.md Phase 5 (B).
# BLOCKED 2026-07-30 — do not invoke; bytes absent.
"""Week-1 timestamp convention calibration (Q-FEED-1 Phase 3, step 1)."""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

_LIB_PATH = Path(__file__).resolve().parent / "_lib.py"
_spec = importlib.util.spec_from_file_location("feed_div_lib", _LIB_PATH)
_feed_div_lib = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = _feed_div_lib
_spec.loader.exec_module(_feed_div_lib)

CALIBRATION_END = _feed_div_lib.CALIBRATION_END
CALIBRATION_MATCH_TIE_BARS = _feed_div_lib.CALIBRATION_MATCH_TIE_BARS
CONVENTION_CANDIDATES = _feed_div_lib.CONVENTION_CANDIDATES
CONVENTION_PATH = _feed_div_lib.CONVENTION_PATH
FX_SYMBOLS = _feed_div_lib.FX_SYMBOLS
IDX_SYMBOL = _feed_div_lib.IDX_SYMBOL
WINDOW_START = _feed_div_lib.WINDOW_START
compute_atr14 = _feed_div_lib.compute_atr14
duka_panel_path = _feed_div_lib.duka_panel_path
load_duka_bars = _feed_div_lib.load_duka_bars
match_bars = _feed_div_lib.match_bars
parse_tv_bar_export = _feed_div_lib.parse_tv_bar_export
p95_abs_delta_close_norm = _feed_div_lib.p95_abs_delta_close_norm
tv_panel_path = _feed_div_lib.tv_panel_path


def _week1_fx_p95(shift_minutes: int) -> float:
    """Mean week-1 FX p95(|Δclose|)/ATR14 across symbols (inf if no data)."""
    scores: list[float] = []
    for sym in FX_SYMBOLS:
        duka_path = duka_panel_path(sym)
        tv_path = tv_panel_path(sym)
        if not duka_path.exists() or not tv_path.exists():
            continue
        duka = load_duka_bars(duka_path)
        tv = parse_tv_bar_export(tv_path, symbol=sym)
        matched, _, _ = match_bars(
            duka, tv, shift_minutes=shift_minutes,
            start=WINDOW_START, end=CALIBRATION_END,
        )
        if matched.empty:
            continue
        d = duka.copy()
        d["bar_open"] = d["time"].dt.floor("15min")
        atr = compute_atr14(d)
        atr.index = d["bar_open"]
        p95 = p95_abs_delta_close_norm(matched, atr)
        if p95 == p95:  # finite
            scores.append(p95)
    return sum(scores) / len(scores) if scores else float("inf")


def _score_convention(shift_minutes: int) -> tuple[int, float, dict[str, int]]:
    per_symbol: dict[str, int] = {}
    total = 0
    for sym in (*FX_SYMBOLS, IDX_SYMBOL):
        duka_path = duka_panel_path(sym)
        tv_path = tv_panel_path(sym)
        if not duka_path.exists() or not tv_path.exists():
            per_symbol[sym] = 0
            continue
        duka = load_duka_bars(duka_path)
        tv = parse_tv_bar_export(tv_path, symbol=sym)
        matched, _, _ = match_bars(
            duka, tv, shift_minutes=shift_minutes,
            start=WINDOW_START, end=CALIBRATION_END,
        )
        per_symbol[sym] = len(matched)
        total += len(matched)
    fx_p95 = _week1_fx_p95(shift_minutes)
    return total, fx_p95, per_symbol


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Calibrate TV timestamp convention on week 1 only.")
    ap.add_argument("--write", action="store_true", help="Write winning convention to FROZEN_CONVENTION.txt")
    a = ap.parse_args(argv)

    rows: list[tuple[str, int, int, float, dict[str, int]]] = []
    print("=== week-1 convention calibration (max match count; FX p95 tie-break) ===")
    for name, shift in CONVENTION_CANDIDATES:
        total, fx_p95, per_sym = _score_convention(shift)
        rows.append((name, shift, total, fx_p95, per_sym))
        print(f"  {name:20s} shift={shift:+4d}min  matches={total:4d}  "
              f"fx_p95={fx_p95:.4f}  {per_sym}")

    max_matches = max(r[2] for r in rows)
    tied = [r for r in rows if r[2] >= max_matches - CALIBRATION_MATCH_TIE_BARS]
    best_name, best_shift, best_total, best_p95, _ = min(tied, key=lambda r: (r[3], -r[2]))

    if best_total < 0:
        print("=== no panels found — run Phase 1 + Phase 2 first ===", file=sys.stderr)
        return 2

    tie_note = ""
    if len(tied) > 1:
        tie_note = f" tie_break=fx_p95 among {len(tied)} within {CALIBRATION_MATCH_TIE_BARS} matches of leader"
    line = (
        f"FROZEN-CONVENTION: name={best_name} shift_minutes={best_shift} "
        f"week1_matches={best_total} week1_fx_p95={best_p95:.4f}{tie_note}"
    )
    print(f"\n=== winner: {line} ===")

    if a.write:
        CONVENTION_PATH.write_text(line + "\n", encoding="utf-8")
        print(f"=== wrote {CONVENTION_PATH} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
