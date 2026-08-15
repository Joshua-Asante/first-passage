# Anchor-dependent (substrate-retirement disposition C): this one-off read
# portfolio_mc.PEPPERSTONE_PANELS, the four 2026-05-24 panels that
# docs/adr/2026-07-22-challenge-era-substrate-retirement.md retires in Phase 3.
# Kept, not deleted: tests/test_phase1_safety_gates.py and
# scripts/check_boundaries.py both reference it.
"""
One-off: run portfolio_mc with the user's Guardian CSV in the Guardian slot,
canonical Pepperstone Striker/Aegis/NAS in the other slots.

**RETIRED (substrate Phase 3, 2026-07-24):** the four Pepperstone executable-
anchor CSVs and PEPPERSTONE_PANELS are gone. Historical 99.83/0.17/4.37 metrics
live in docs/mc_anchor_history.md and
docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md.
Engine regression uses tests/core/test_mc_synthetic_engine.py.

Bypasses the MVD filename gate (user's CSVs aren't canonical exports); every
other step — load_trades, implied_1r, build_daily_panel, run_seed, aggregation
— uses the production functions unchanged.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PHASE3_RETIREMENT_MSG = (
    "mc_user_guardian.py is retired (substrate Phase 3, 2026-07-24): "
    "PEPPERSTONE_PANELS and the four 2026-05-24 anchor CSVs were deleted. "
    "See docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md "
    "and docs/mc_anchor_history.md for the historical 99.83/0.17/4.37 record."
)


def run(guardian_csv: Path, guardian_alloc: float, label: str):
    raise SystemExit(_PHASE3_RETIREMENT_MSG)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, type=Path)
    p.add_argument("--alloc", required=True, type=float)
    p.add_argument("--label", required=True)
    args = p.parse_args()
    raise SystemExit(_PHASE3_RETIREMENT_MSG)


if __name__ == "__main__":
    main()
