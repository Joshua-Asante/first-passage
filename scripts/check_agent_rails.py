#!/usr/bin/env python3
"""Assert docs/agent_rails/rails.yml still matches production bytes.

Labeled mirror of existing rails — not a second owner and not a NeMo runtime.
Fail-closed: missing path, missing must_contain, missing NeMo stage, no hard
execution rail, or a pin that claims a runtime adoption all exit 1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover — pyproject lists pyyaml
    yaml = None  # type: ignore

REPO = Path(__file__).resolve().parent.parent
DEFAULT_INVENTORY = REPO / "docs" / "agent_rails" / "rails.yml"
REQUIRED_STAGES = ("input", "dialog", "retrieval", "execution", "output")
ALLOWED_HARDNESS = frozenset({"hard", "soft"})
PIN_RUNTIME_REQUIRED = "not-adopted"


def load_inventory(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read rails.yml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


def _anchor_errors(repo: Path, rail_id: str, anchors: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(anchors, list) or not anchors:
        return [f"{rail_id}: anchors must be a non-empty list"]
    for i, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            errors.append(f"{rail_id} anchor[{i}]: expected mapping")
            continue
        rel = anchor.get("path")
        needle = anchor.get("must_contain")
        if not isinstance(rel, str) or not rel:
            errors.append(f"{rail_id} anchor[{i}]: missing path")
            continue
        if not isinstance(needle, str) or not needle:
            errors.append(f"{rail_id} anchor[{i}]: missing must_contain")
            continue
        target = repo / rel
        if not target.is_file():
            errors.append(f"{rail_id}: missing path {rel}")
            continue
        text = target.read_text(encoding="utf-8")
        if needle not in text:
            errors.append(f"{rail_id}: {rel} missing {needle!r}")
    return errors


def check_inventory(repo: Path, inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    pin = inventory.get("nemo_pin")
    if not isinstance(pin, dict):
        errors.append("nemo_pin: missing mapping")
    else:
        commit = pin.get("commit")
        if not (isinstance(commit, str) and len(commit) == 40 and
                all(c in "0123456789abcdef" for c in commit)):
            errors.append("nemo_pin.commit: expected 40-char lowercase hex")
        if pin.get("runtime") != PIN_RUNTIME_REQUIRED:
            errors.append(
                f"nemo_pin.runtime: expected {PIN_RUNTIME_REQUIRED!r}, "
                f"got {pin.get('runtime')!r}"
            )
        if pin.get("tag") != "v0.23.0":
            errors.append("nemo_pin.tag: expected 'v0.23.0' (update checker with pin)")

    stages = inventory.get("stages")
    if not isinstance(stages, dict) or not stages:
        return errors + ["stages: missing mapping"]

    missing_stages = [name for name in REQUIRED_STAGES if name not in stages]
    if missing_stages:
        errors.append("stages: missing " + ", ".join(missing_stages))

    hard_execution = 0
    for stage_name, rails in stages.items():
        if not isinstance(rails, list) or not rails:
            errors.append(f"stages.{stage_name}: expected non-empty list")
            continue
        for rail in rails:
            if not isinstance(rail, dict):
                errors.append(f"stages.{stage_name}: rail is not a mapping")
                continue
            rail_id = str(rail.get("id") or f"{stage_name}?<missing-id>")
            hardness = rail.get("hardness")
            if hardness not in ALLOWED_HARDNESS:
                errors.append(f"{rail_id}: hardness must be hard|soft")
            owner = rail.get("owner")
            if not isinstance(owner, str) or not owner:
                errors.append(f"{rail_id}: missing owner")
            elif not (repo / owner).exists():
                errors.append(f"{rail_id}: missing owner {owner}")
            errors.extend(_anchor_errors(repo, rail_id, rail.get("anchors")))
            if stage_name == "execution" and hardness == "hard":
                hard_execution += 1

    if hard_execution < 1:
        errors.append("execution: at least one hardness=hard rail is required")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", type=Path, default=DEFAULT_INVENTORY,
        help="rails.yml path (default: docs/agent_rails/rails.yml)",
    )
    parser.add_argument(
        "--repo", type=Path, default=REPO, help="repository root",
    )
    args = parser.parse_args(argv)
    try:
        inventory = load_inventory(args.inventory)
        errors = check_inventory(args.repo, inventory)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"agent-rails: FAIL — {exc}", file=sys.stderr)
        return 1
    if errors:
        print("agent-rails: FAIL", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    print("agent-rails: CLEAN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
