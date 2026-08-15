#!/usr/bin/env python3
"""Assert Q-FEED-1 §6 gate verdicts from RESULTS.md metrics (Phase 4)."""
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

FX_SYMBOLS = _feed_div_lib.FX_SYMBOLS
IDX_SYMBOL = _feed_div_lib.IDX_SYMBOL
RESULTS_PATH = _feed_div_lib.RESULTS_PATH
classify_verdict_band = _feed_div_lib.classify_verdict_band
load_thresholds = _feed_div_lib.load_thresholds


def _parse_results_table(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| symbol"):
            continue
        if line.startswith("|---"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 7:
            continue
        sym, cls, matched, elig, cov, p95, resid = parts[:7]
        if sym == "symbol":
            continue
        rows.append({
            "symbol": sym,
            "class": cls,
            "coverage": float(cov.replace("%", "")) / 100.0,
            "p95_dclose_atr": float(p95),
            "idx_residual_p95": float(resid) if resid else None,
        })
    return rows


def _overall_verdict(fx_bands: list[str], idx_band: str | None) -> str:
    if any(b == "AMBIGUOUS" for b in fx_bands) or idx_band == "AMBIGUOUS":
        return "AMBIGUOUS-HOLD"
    if any(b == "REJECT" for b in fx_bands):
        return "FALSIFIED (FX)"
    fx_ok = all(b == "ACCEPT" for b in fx_bands)
    if not fx_ok:
        return "AMBIGUOUS-HOLD"
    if idx_band == "REJECT":
        return "RESOLVED-UNSTABLE (IDX)"
    if idx_band == "ACCEPT":
        return "RESOLVED-STABLE-BASIS (IDX)"
    return "AMBIGUOUS-HOLD"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run Q-FEED-1 gate assertion.")
    ap.add_argument("--results", default=str(RESULTS_PATH))
    a = ap.parse_args(argv)

    results_path = Path(a.results)
    if not results_path.exists():
        print(f"=== missing {results_path} — run measure_divergence.py first ===", file=sys.stderr)
        return 2

    thr = load_thresholds()
    rows = _parse_results_table(results_path)
    if not rows:
        print("=== no rows parsed from RESULTS.md ===", file=sys.stderr)
        return 2

    print("=== Q-FEED-1 gate assertion (thresholds from pre-registration) ===")
    fx_bands: list[str] = []
    idx_band: str | None = None

    for r in rows:
        p95_band = classify_verdict_band(
            r["p95_dclose_atr"], thr.fx_p95_accept, thr.fx_p95_reject, higher_is_worse=True,
        )
        cov_band = classify_verdict_band(
            r["coverage"], thr.fx_cov_accept, thr.fx_cov_reject, higher_is_worse=False,
        )
        if r["class"] == "FX":
            sym_band = "REJECT" if "REJECT" in (p95_band, cov_band) else (
                "ACCEPT" if p95_band == "ACCEPT" and cov_band == "ACCEPT" else "AMBIGUOUS"
            )
            fx_bands.append(sym_band)
            print(f"  FX {r['symbol']}: p95/ATR={r['p95_dclose_atr']:.4f} ({p95_band}) "
                  f"coverage={r['coverage']*100:.2f}% ({cov_band}) -> {sym_band}")
        elif r["symbol"] == IDX_SYMBOL and r["idx_residual_p95"] is not None:
            idx_band = classify_verdict_band(
                r["idx_residual_p95"],
                thr.idx_residual_p95_accept,
                thr.idx_residual_p95_reject,
                higher_is_worse=True,
            )
            print(f"  IDX {r['symbol']}: residual_p95/ATR={r['idx_residual_p95']:.4f} ({idx_band})")

    verdict = _overall_verdict(fx_bands, idx_band)
    print(f"\n=== OVERALL VERDICT: {verdict} ===")
    if verdict == "FALSIFIED (FX)":
        print("=== route to code-defect-debugging before accepting feed finding ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
