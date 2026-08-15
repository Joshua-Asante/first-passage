#!/usr/bin/env python3
"""One-command reproducer for the Custodian-EURUSD mechanism probe.

  1. fetch the three Dukascopy m15 panels if absent (fetch_panel.py):
       EURUSD_M15.csv (1e5), USA500IDXUSD_M15.csv (1e3), EUSIDXEUR_M15.csv (1e3)
  2. run the pre-registered falsifier regression (gate.py) -> gate_result.json

Run from the repo root:
    python lab/analysis/custodian_eurusd/run_gate.py

The EuroStoxx-50 symbol EUSIDXEUR / point_factor 1e3 was discovered + verified
empirically in Phase 0 (see fetch_panel.py docstring + README.md).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_BARDIR = _ROOT / "core" / "data" / "bar_data"

PANELS = [
    ("EURUSD", "EURUSD_M15.csv", "100000"),
    ("USA500IDXUSD", "USA500IDXUSD_M15.csv", "1000"),
    ("EUSIDXEUR", "EUSIDXEUR_M15.csv", "1000"),
]


def main() -> int:
    for symbol, fname, factor in PANELS:
        path = _BARDIR / fname
        if not path.exists() or path.stat().st_size < 1024:
            print(f"=== {fname} missing/empty -> fetching {symbol} ===")
            rc = subprocess.call([
                sys.executable, str(_HERE / "fetch_panel.py"),
                "--symbol", symbol, "--point-factor", factor,
                "--out", str(path), "--start", "2016-01-01", "--end", "2026-06-09",
            ])
            if rc != 0:
                print(f"fetch of {symbol} returned non-zero — check coverage in the summary.")
    rc = subprocess.call([
        sys.executable, str(_HERE / "gate.py"),
        "--eur", str(_BARDIR / "EURUSD_M15.csv"),
        "--spx", str(_BARDIR / "USA500IDXUSD_M15.csv"),
        "--estx", str(_BARDIR / "EUSIDXEUR_M15.csv"),
        "--out", str(_HERE),
    ])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
