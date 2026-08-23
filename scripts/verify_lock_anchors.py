#!/usr/bin/env python3
"""verify_lock_anchors.py — surface Closed / Forward / Error routing.

Slimmed 2026-08-03 (ADR docs/adr/2026-08-03-params-toml-gate-retirement.md):
the retired `params.toml` hub is no longer a source. This script asks only:

  Are live DD_TRIGGER / DD_SCALE readable in `dd_protection.py`, is historical
  Guardian risk in `HISTORICAL_CHALLENGE_BASE_RISK` inside the documented safe
  band, and are CFD slugs absent from living `firm_rules._BASE_RISK`?

Routing (per `docs/methodology/observation_routing.md`):

  Closed   — `dd_protection.py` + `firm_rules.py` + `historical_challenge.py`
             present; DD_TRIGGER / DD_SCALE parseable; historical Guardian
             inside [0.30%, 0.34%]; living `_BASE_RISK` has no guardian/aegis.
             Exit 0.

  Forward  — historical Guardian outside the documented [0.30%, 0.34%] safe
             band. Exit 2. Does NOT auto-run portfolio_mc.

  Error    — required files missing, required constants not parseable, or
             living `_BASE_RISK` still lists guardian/aegis. Exit 3.

  Action   — unused after params.toml retirement (kept in the Literal for
             observation_routing compatibility; never emitted).

Routing precedence:  Error > Forward > Closed.

Exit codes:
  0 — Closed
  1 — Action (unused)
  2 — Forward
  3 — Error

Usage:
  python scripts/verify_lock_anchors.py
  python scripts/verify_lock_anchors.py --quiet
  python scripts/verify_lock_anchors.py --json
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent

GUARDIAN_SAFE_BAND_PCT = (0.30, 0.34)
PCT_EPS = 1e-6

Routing = Literal["Closed", "Action", "Forward", "Error"]


@dataclass
class Sources:
    """File paths the verifier reads. Tests inject a tmp_path-rooted Sources."""
    dd_protection: Path = field(
        default_factory=lambda: REPO_ROOT / "core" / "dd_protection.py")
    firm_rules: Path = field(
        default_factory=lambda: REPO_ROOT / "core" / "firm_rules.py")
    historical_challenge: Path = field(
        default_factory=lambda: REPO_ROOT / "core" / "historical_challenge.py")

    def required(self) -> list[Path]:
        return [self.dd_protection, self.firm_rules, self.historical_challenge]


@dataclass
class Drift:
    field: str
    source_a: str
    value_a: float | str
    source_b: str
    value_b: float | str

    def __str__(self) -> str:
        return (f"  {self.field}: {self.source_a}={self.value_a} != "
                f"{self.source_b}={self.value_b}")


@dataclass
class Trigger:
    name: str
    detail: str

    def __str__(self) -> str:
        return f"  [{self.name}] {self.detail}"


@dataclass
class Decision:
    routing: Routing
    drifts: list[Drift] = field(default_factory=list)
    triggers: list[Trigger] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def exit_code(self) -> int:
        return {"Closed": 0, "Action": 1, "Forward": 2, "Error": 3}[self.routing]


def parse_dd_protection_constants(text: str) -> dict:
    """Pull DD_TRIGGER, DD_SCALE from dd_protection.py (AST Constant assigns)."""
    out: dict = {}
    tree = ast.parse(text)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id in ("DD_TRIGGER", "DD_SCALE") and isinstance(
                node.value, ast.Constant
            ):
                out[target.id] = float(node.value.value)
    return out


def _parse_str_float_dict(text: str, name: str) -> dict[str, float] | None:
    """Pull a module-level `{str: float}` assignment by name (AST Constant)."""
    tree = ast.parse(text)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name) or target.id != name:
                continue
            if not isinstance(node.value, ast.Dict):
                continue
            out: dict[str, float] = {}
            for k, v in zip(node.value.keys, node.value.values):
                if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                    out[str(k.value)] = float(v.value)
            return out
    return None


def parse_historical_guardian_risk(text: str) -> float | None:
    """Pull `HISTORICAL_CHALLENGE_BASE_RISK['guardian']`."""
    book = _parse_str_float_dict(text, "HISTORICAL_CHALLENGE_BASE_RISK")
    if book is None or "guardian" not in book:
        return None
    return book["guardian"]


def parse_living_base_risk_slugs(text: str) -> set[str] | None:
    """Pull living `_BASE_RISK` slug keys. None if the dict is not parseable.

    After Phase C the living dict is a comprehension over
    ``HISTORICAL_CHALLENGE_BASE_RISK``. A literal `_BASE_RISK = {...}` is the
    fixture shape; a comprehension is treated as “no CFD slugs in a literal”
    and the caller must not require a literal.
    """
    book = _parse_str_float_dict(text, "_BASE_RISK")
    if book is None:
        return None
    return set(book)


def check_guardian_safe_band(guardian_risk: float) -> Trigger | None:
    g_pct = guardian_risk * 100.0
    lo, hi = GUARDIAN_SAFE_BAND_PCT
    if not (lo - PCT_EPS <= g_pct <= hi + PCT_EPS):
        return Trigger(
            "guardian_safe_band",
            f"historical_challenge.py:HISTORICAL_CHALLENGE_BASE_RISK['guardian']"
            f"={g_pct:.4f}% is outside documented safe band "
            f"[{lo:.2f}%, {hi:.2f}%] (±{PCT_EPS:.0e}).",
        )
    return None


def decide(sources: Sources | None = None) -> Decision:
    sources = sources or Sources()

    missing = [p for p in sources.required() if not p.exists()]
    if missing:
        return Decision(
            routing="Error",
            errors=[f"Required file missing: {p}" for p in missing],
            notes=["Cannot run routing checks. Restore missing files and re-run."],
        )

    try:
        dd_consts = parse_dd_protection_constants(
            sources.dd_protection.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return Decision(
            routing="Error",
            errors=[f"dd_protection.py: parse failure — {exc}"],
        )

    try:
        guardian_risk = parse_historical_guardian_risk(
            sources.historical_challenge.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return Decision(
            routing="Error",
            errors=[f"historical_challenge.py: parse failure — {exc}"],
        )

    try:
        living_slugs = parse_living_base_risk_slugs(
            sources.firm_rules.read_text(encoding="utf-8")
        )
    except Exception as exc:
        return Decision(
            routing="Error",
            errors=[f"firm_rules.py: parse failure — {exc}"],
        )

    parse_errors: list[str] = []
    for key in ("DD_TRIGGER", "DD_SCALE"):
        if key not in dd_consts:
            parse_errors.append(
                f"dd_protection.py: required constant '{key}' not parseable"
            )
    if guardian_risk is None:
        parse_errors.append(
            "historical_challenge.py: required constant "
            "'HISTORICAL_CHALLENGE_BASE_RISK[\"guardian\"]' not parseable"
        )
    cfd_in_living = set()
    if living_slugs is not None:
        cfd_in_living = living_slugs & {"guardian", "aegis"}
        if cfd_in_living:
            parse_errors.append(
                "firm_rules.py: living _BASE_RISK still lists CFD slugs "
                f"{sorted(cfd_in_living)} (Phase C: historical book only)"
            )
    if parse_errors:
        return Decision(
            routing="Error",
            errors=parse_errors,
            notes=["Fix dd_protection.py so DD_TRIGGER / DD_SCALE are "
                   "ast.Constant assignments, historical_challenge.py so "
                   "HISTORICAL_CHALLENGE_BASE_RISK['guardian'] is an "
                   "ast.Constant dict entry, and firm_rules.py so living "
                   "_BASE_RISK has no guardian/aegis keys."],
        )

    triggers: list[Trigger] = []
    t = check_guardian_safe_band(guardian_risk)
    if t is not None:
        triggers.append(t)

    if triggers:
        return Decision(
            routing="Forward",
            triggers=triggers,
            notes=[
                "Re-MC trigger fired. Review production sizing constants and "
                "re-run portfolio_mc if MC inputs changed.",
                "This script does NOT auto-run portfolio_mc.",
            ],
        )
    return Decision(routing="Closed")


def emit_human(decision: Decision, quiet: bool) -> None:
    print(f"ROUTING: {decision.routing}")
    if quiet:
        return
    if decision.errors:
        print("\nErrors:")
        for e in decision.errors:
            print(f"  {e}")
    if decision.triggers:
        print("\nRe-MC triggers fired:")
        for t in decision.triggers:
            print(t)
    if decision.drifts:
        print("\nDrift detected:")
        for d in decision.drifts:
            print(d)
    if decision.notes:
        print()
        for line in decision.notes:
            print(line)


def emit_json(decision: Decision) -> None:
    print(json.dumps(asdict(decision), indent=2, default=str))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quiet", action="store_true",
                    help="Print only the ROUTING line.")
    ap.add_argument("--json", action="store_true",
                    help="Emit machine-readable JSON.")
    args = ap.parse_args()
    try:
        decision = decide()
    except Exception as exc:  # pragma: no cover
        print(f"verify_lock_anchors: error — {exc}", file=sys.stderr)
        return 3
    if args.json:
        emit_json(decision)
    else:
        emit_human(decision, quiet=args.quiet)
    return decision.exit_code()


if __name__ == "__main__":
    sys.exit(main())
