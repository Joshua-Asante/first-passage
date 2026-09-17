#!/usr/bin/env python3
"""Schema gate for scripts/repo_map_layers.yml — the single layer-map definition.

Gate id ``repo-map-layers`` (path-conditional, scripts/gates.yml). The scanner
(scripts/check_boundaries.py) loads the same file at import, so there is no
second copy to drift; this gate turns a bad edit into a readable verdict instead
of a scanner traceback: required sections and types, prefixes end with ``/``,
layers are known, an app prefix names its own directory, every
``scripts_layer`` stem is a tracked ``scripts/<stem>.py`` (a stale override is
dead configuration), and every prefix / flat root is a directory.

History: created 2026-08-23 (pain-point packet P5) as a dict<->YAML drift
compare while the scanner kept hard-coded copies; single-source since
2026-09-17 (docs/adr/2026-06-05-monorepo-layer-boundaries.md §2.3 amendment).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
LAYERS_YML = REPO / "scripts" / "repo_map_layers.yml"
LAYERS = ("core", "governance", "lab", "ops")
SECTIONS = {
    "app_layer_prefix": dict,
    "governance_prefixes": list,
    "scripts_layer": dict,
    "flat_import_roots": list,
}


def schema_problems(data: object) -> list[str]:
    """Shape and value rules that need only the parsed file."""
    if not isinstance(data, dict):
        return ["top level is not a mapping"]
    out: list[str] = []
    for name, kind in SECTIONS.items():
        value = data.get(name)
        if not isinstance(value, kind) or not value:
            out.append(f"{name}: missing or not a non-empty {kind.__name__}")
            continue
        atoms = [*value.keys(), *value.values()] if kind is dict else list(value)
        if not all(isinstance(x, str) and x for x in atoms):
            out.append(f"{name}: every key and value must be a non-empty plain string")
    out.extend(f"unknown section '{name}'" for name in set(data) - set(SECTIONS))
    if out:
        return out
    app = data["app_layer_prefix"]
    for prefix, layer in app.items():
        if layer not in LAYERS or layer == "governance":
            out.append(f"app_layer_prefix: '{prefix}' maps to unknown application layer '{layer}'")
        elif prefix != f"{layer}/":
            out.append(f"app_layer_prefix: '{prefix}' must be '{layer}/' (the dir is the layer)")
    for prefix in data["governance_prefixes"]:
        if not prefix.endswith("/"):
            out.append(f"governance_prefixes: '{prefix}' must end with '/'")
        if prefix in app:
            out.append(f"governance_prefixes: '{prefix}' is already an application prefix")
    for stem, layer in data["scripts_layer"].items():
        if layer not in LAYERS:
            out.append(f"scripts_layer: '{stem}' maps to unknown layer '{layer}'")
        if not stem.isidentifier():
            out.append(f"scripts_layer: '{stem}' is not a module stem (no path, no .py)")
    for root in data["flat_import_roots"]:
        if root.startswith("/") or root.endswith("/"):
            out.append(f"flat_import_roots: '{root}' must be a relative dir without a trailing '/'")
    for name in ("governance_prefixes", "flat_import_roots"):
        seen: set[str] = set()
        for item in data[name]:
            if item in seen:
                out.append(f"{name}: duplicate entry '{item}'")
            seen.add(item)
    return out


def repository_problems(data: dict, repo_root: Path) -> list[str]:
    """Rules that need the tree: overrides name tracked scripts; roots and prefixes are dirs."""
    out: list[str] = []
    for stem in data["scripts_layer"]:
        if stem.isidentifier() and not (repo_root / "scripts" / f"{stem}.py").is_file():
            out.append(f"scripts_layer: no scripts/{stem}.py for override '{stem}'")
    for name in ("app_layer_prefix", "governance_prefixes", "flat_import_roots"):
        for entry in data[name]:
            if not (repo_root / entry).is_dir():
                out.append(f"{name}: '{entry}' is not a directory under {repo_root}")
    return out


def main(argv: list[str] | None = None) -> int:
    """Exit 1 with every violation listed; 0 with a one-line summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yml", type=Path, default=LAYERS_YML)
    parser.add_argument("--repo-root", type=Path, default=REPO,
                        help="tree for the existence checks (tests point tmp copies at it)")
    args = parser.parse_args(argv)
    try:
        with args.yml.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        print(f"repo-map-layers: FAIL — cannot load {args.yml}: {exc}", file=sys.stderr)
        return 1
    problems = schema_problems(data)
    if not problems:
        problems = repository_problems(data, args.repo_root.resolve())
    if problems:
        print(f"repo-map-layers: FAIL — {args.yml} breaks the layer-map schema", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print("repo-map-layers: OK — "
          f"{len(data['app_layer_prefix'])} app prefixes, "
          f"{len(data['governance_prefixes'])} governance prefixes, "
          f"{len(data['scripts_layer'])} script overrides, "
          f"{len(data['flat_import_roots'])} flat roots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
