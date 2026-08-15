#!/usr/bin/env python3
"""One-command reproducer for the Sovereign (CONCEPT-USDCAD-RDM-001) F1 gate.

Fetches any missing inputs (all free/keyless; the six composite exports must be
present locally — vendor-licensed, see fetch_panel.py), then runs the gate.

Usage:
    python lab/analysis/usdcad_rdm/run_gate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import fetch_panel  # noqa: E402
import gate  # noqa: E402

if __name__ == "__main__":
    fetch_panel.main([])          # skips anything already on disk
    raise SystemExit(gate.main([]))
