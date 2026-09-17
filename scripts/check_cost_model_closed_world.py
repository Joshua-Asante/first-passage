#!/usr/bin/env python3
"""check_cost_model_closed_world.py — SSOT Phase 3 partition gate.

Hard-fails when geometry lacks commission classification, a priced symbol lacks
geometry, or an explicit commission binding names an invalid category.

Does not join ops/instruments ledgers. Does not add commission dollars.
Classified lab so the discovery.cost_model import is a legal lab→lab edge.
"""
from __future__ import annotations

import sys

from layer_bootstrap import add_layer_roots

add_layer_roots("lab", "core")

from discovery.cost_model import closed_world_findings  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    del argv  # no flags in v1
    findings = closed_world_findings()
    if not findings:
        print("check_cost_model_closed_world: OK")
        return 0
    print("check_cost_model_closed_world: FAIL", file=sys.stderr)
    for finding in findings:
        print(f"  {finding}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
