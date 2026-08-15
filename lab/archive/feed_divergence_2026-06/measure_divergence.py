#!/usr/bin/env python3
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
# Q-FEED-1 closed RESOLVED-BY-RETIREMENT. Reads core/data/bar_data/*_duka.csv,
# DELETED by docs/adr/2026-07-22-challenge-era-substrate-retirement.md Phase 5 (B).
# BLOCKED 2026-07-30 — do not invoke; bytes absent.
"""Matched-bar divergence measurement (Q-FEED-1 Phase 3, step 2)."""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import pandas as pd

_LIB_PATH = Path(__file__).resolve().parent / "_lib.py"
_spec = importlib.util.spec_from_file_location("feed_div_lib", _LIB_PATH)
_feed_div_lib = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = _feed_div_lib
_spec.loader.exec_module(_feed_div_lib)

CONVENTION_PATH = _feed_div_lib.CONVENTION_PATH
FX_SYMBOLS = _feed_div_lib.FX_SYMBOLS
IDX_SYMBOL = _feed_div_lib.IDX_SYMBOL
RESULTS_PATH = _feed_div_lib.RESULTS_PATH
WINDOW_END = _feed_div_lib.WINDOW_END
WINDOW_START = _feed_div_lib.WINDOW_START
compute_atr14 = _feed_div_lib.compute_atr14
coverage_ratio = _feed_div_lib.coverage_ratio
duka_panel_path = _feed_div_lib.duka_panel_path
eligible_mask = _feed_div_lib.eligible_mask
idx_residual_p95 = _feed_div_lib.idx_residual_p95
load_duka_bars = _feed_div_lib.load_duka_bars
match_bars = _feed_div_lib.match_bars
parse_tv_bar_export = _feed_div_lib.parse_tv_bar_export
p95_abs_delta_close_norm = _feed_div_lib.p95_abs_delta_close_norm
tv_panel_path = _feed_div_lib.tv_panel_path


def _load_shift_minutes(explicit: int | None) -> tuple[str, int]:
    if explicit is not None:
        return ("cli_override", explicit)
    if not CONVENTION_PATH.exists():
        raise FileNotFoundError(
            f"missing {CONVENTION_PATH} — run calibrate_convention.py --write first"
        )
    line = CONVENTION_PATH.read_text(encoding="utf-8").strip()
    m = re.search(r"shift_minutes=(-?\d+)", line)
    name_m = re.search(r"name=([^\s]+)", line)
    if not m:
        raise ValueError(f"cannot parse shift from: {line!r}")
    return (name_m.group(1) if name_m else "frozen", int(m.group(1)))


def _duka_eligible(duka: pd.DataFrame) -> pd.DataFrame:
    d = duka.copy()
    d["bar_open"] = d["time"].dt.floor("15min")
    mask = (d["bar_open"] >= WINDOW_START) & (d["bar_open"] < WINDOW_END)
    mask &= eligible_mask(d["bar_open"])
    return d[mask]


def measure_symbol(sym: str, shift_minutes: int) -> dict:
    duka = load_duka_bars(duka_panel_path(sym))
    tv = parse_tv_bar_export(tv_panel_path(sym), symbol=sym)
    duka = duka.copy()
    duka["bar_open"] = duka["time"].dt.floor("15min")
    atr = compute_atr14(duka)
    atr.index = duka["bar_open"]

    matched, d_only, t_only = match_bars(duka, tv, shift_minutes=shift_minutes)
    d_elig = _duka_eligible(duka)

    return {
        "symbol": sym,
        "matched": len(matched),
        "duka_eligible": len(d_elig),
        "duka_only": len(d_only),
        "tv_only": len(t_only),
        "coverage": coverage_ratio(matched, d_elig),
        "p95_dclose_atr": p95_abs_delta_close_norm(matched, atr),
        "idx_residual_p95": idx_residual_p95(matched, atr) if sym == IDX_SYMBOL else None,
    }


def _fmt_table(rows: list[dict], convention_line: str) -> str:
    lines = [
        "# Q-FEED-1 feed divergence — RESULTS",
        "",
        convention_line,
        "",
        f"Window: {WINDOW_START} → {WINDOW_END}",
        "",
        "## Decomposition table",
        "",
        "| symbol | class | matched | duka_eligible | coverage | p95(|Δclose|)/ATR14 | idx_residual_p95 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        cls = "IDX" if r["symbol"] == IDX_SYMBOL else "FX"
        resid = "" if r["idx_residual_p95"] is None else f"{r['idx_residual_p95']:.4f}"
        lines.append(
            f"| {r['symbol']} | {cls} | {r['matched']} | {r['duka_eligible']} | "
            f"{r['coverage']*100:.2f}% | {r['p95_dclose_atr']:.4f} | {resid} |"
        )
    lines.extend([
        "",
        "## Unmatched census (summary)",
        "",
    ])
    for r in rows:
        lines.append(
            f"- **{r['symbol']}**: duka_only={r['duka_only']}, tv_only={r['tv_only']}"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Measure Dukascopy↔TV bar divergence.")
    ap.add_argument("--shift-minutes", type=int, default=None,
                    help="Override frozen convention shift (testing only)")
    ap.add_argument("--out", default=str(RESULTS_PATH))
    a = ap.parse_args(argv)

    name, shift = _load_shift_minutes(a.shift_minutes)
    convention_line = (
        CONVENTION_PATH.read_text(encoding="utf-8").strip()
        if CONVENTION_PATH.exists() and a.shift_minutes is None
        else f"FROZEN-CONVENTION: name={name} shift_minutes={shift}"
    )

    rows = []
    for sym in (*FX_SYMBOLS, IDX_SYMBOL):
        duka_p = duka_panel_path(sym)
        tv_p = tv_panel_path(sym)
        if not duka_p.exists() or not tv_p.exists():
            print(f"=== skip {sym}: missing {duka_p} or {tv_p} ===", file=sys.stderr)
            continue
        rows.append(measure_symbol(sym, shift))

    if not rows:
        print("=== no symbol pairs to measure ===", file=sys.stderr)
        return 2

    out = Path(a.out)
    out.write_text(_fmt_table(rows, convention_line), encoding="utf-8")
    print(f"=== wrote {out} (convention shift={shift}min) ===")
    for r in rows:
        print(f"  {r['symbol']}: coverage={r['coverage']*100:.2f}% "
              f"p95/ATR={r['p95_dclose_atr']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
