#!/usr/bin/env python3
"""One-command reproducer for the NOCT-SPX-001 Stage 1+2 gate.

  1. fetch the Dukascopy USA500IDXUSD m15 panel if absent (fetch_panel.py)
  2. run the channel-isolating falsifier (gate.py) -> gate_result.json + summary

Run from the repo root:
    python lab/analysis/noct_spx/run_gate.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_BARS = _ROOT / "core" / "data" / "bar_data" / "USA500IDXUSD_M15.csv"


def main() -> int:
    if not _BARS.exists() or _BARS.stat().st_size < 1024:
        print(f"=== bars missing/empty -> fetching {_BARS.name} ===")
        rc = subprocess.call([sys.executable, str(_HERE / "fetch_panel.py"),
                              "--out", str(_BARS)])
        if rc != 0:
            print("fetch returned non-zero (some chunks may have failed) — continuing "
                  "to gate on whatever was written; check coverage in the summary.")
    rc = subprocess.call([sys.executable, str(_HERE / "gate.py"),
                          "--bars", str(_BARS), "--out", str(_HERE)])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
