#!/usr/bin/env python3
"""Fail if check_boundaries.py layer maps drift from scripts/repo_map_layers.yml.

P5 of the 2026-08-23 pain-point charter. Does **not** make check_boundaries
import REPO_MAP.md — the scanner keeps hard-coded dicts; this gate compares them
to the machine sibling YAML.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # stdlib-only fallback: minimal subset via safe_load not required
    yaml = None  # type: ignore

REPO = Path(__file__).resolve().parent.parent
BOUNDARIES = REPO / "scripts" / "check_boundaries.py"
LAYERS_YML = REPO / "scripts" / "repo_map_layers.yml"


def _load_boundaries_maps(path: Path) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: dict = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        name = node.targets[0]
        if not isinstance(name, ast.Name):
            continue
        if name.id not in (
            "APP_LAYER_PREFIX",
            "GOVERNANCE_PREFIXES",
            "SCRIPTS_LAYER",
        ):
            continue
        out[name.id] = ast.literal_eval(node.value)
    missing = {"APP_LAYER_PREFIX", "GOVERNANCE_PREFIXES", "SCRIPTS_LAYER"} - set(out)
    if missing:
        raise ValueError(f"check_boundaries.py missing assignments: {sorted(missing)}")
    return out


def _load_yml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = _parse_simple_yml(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


def _parse_simple_yml(text: str) -> dict:
    """Minimal YAML subset for this file only (no PyYAML required)."""
    app: dict[str, str] = {}
    gov: list[str] = []
    scripts: dict[str, str] = {}
    section: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and line.endswith(":"):
            section = line[:-1].strip()
            continue
        if section == "app_layer_prefix" and ":" in line:
            k, v = line.strip().split(":", 1)
            app[k.strip()] = v.strip()
        elif section == "governance_prefixes" and line.strip().startswith("- "):
            gov.append(line.strip()[2:].strip())
        elif section == "scripts_layer" and ":" in line:
            k, v = line.strip().split(":", 1)
            scripts[k.strip()] = v.strip()
    return {
        "app_layer_prefix": app,
        "governance_prefixes": gov,
        "scripts_layer": scripts,
    }


def compare(boundaries: dict, yml: dict) -> list[str]:
    problems: list[str] = []
    app_b = boundaries["APP_LAYER_PREFIX"]
    app_y = yml.get("app_layer_prefix") or {}
    if app_b != app_y:
        problems.append(
            f"APP_LAYER_PREFIX drift: boundaries={app_b!r} yml={app_y!r}"
        )
    gov_b = tuple(boundaries["GOVERNANCE_PREFIXES"])
    gov_y = tuple(yml.get("governance_prefixes") or ())
    if gov_b != gov_y:
        problems.append(
            f"GOVERNANCE_PREFIXES drift: boundaries={gov_b!r} yml={gov_y!r}"
        )
    scr_b = boundaries["SCRIPTS_LAYER"]
    scr_y = yml.get("scripts_layer") or {}
    if scr_b != scr_y:
        only_b = sorted(set(scr_b) - set(scr_y))
        only_y = sorted(set(scr_y) - set(scr_b))
        both = sorted(
            k for k in set(scr_b) & set(scr_y) if scr_b[k] != scr_y[k]
        )
        problems.append(
            "SCRIPTS_LAYER drift: "
            f"only_in_boundaries={only_b} only_in_yml={only_y} "
            f"value_mismatch={both}"
        )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundaries", type=Path, default=BOUNDARIES)
    parser.add_argument("--yml", type=Path, default=LAYERS_YML)
    args = parser.parse_args(argv)
    try:
        boundaries = _load_boundaries_maps(args.boundaries)
        yml = _load_yml(args.yml)
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"repo-map-layers: FAIL — {exc}", file=sys.stderr)
        return 1
    problems = compare(boundaries, yml)
    if problems:
        print("repo-map-layers: FAIL — maps drift", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("repo-map-layers: OK — check_boundaries maps match repo_map_layers.yml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
