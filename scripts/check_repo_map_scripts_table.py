#!/usr/bin/env python3
"""Emit / check the REPO_MAP.md §2.1 scripts table.

Row set: ``git ls-files 'scripts/*.py'``.
Layer: ``scripts/repo_map_layers.yml`` ``scripts_layer`` (fallback governance) —
the same single definition ``check_boundaries.py`` loads, read through its
loader so this table can never disagree with the scanner.
Gate wiring: ``scripts/gates.yml`` (id, tier, load-bearing flags). A gate whose cmd
names no script (a module run) is credited to the tracked scripts its
``when.staged_regex`` selects.

This is a documentation generator. It does **not** change gate composition
(``gates.yml`` remains the sole owner). ``--check`` is wired into ``gates.yml``
as the path-conditional ``repo-map-scripts-table`` gate; on failure regenerate
with ``--write``.

Sibling of ``check_repo_map_layers.py`` (the layer-map schema gate); this
script owns the human-readable §2.1 table so the section cannot drift into
hand-maintained prose again. The two common defaults (layer fallback; no gate)
are marked once in a legend, not repeated in every row's Notes.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOUNDARIES = REPO / "scripts" / "check_boundaries.py"
LAYERS_YML = REPO / "scripts" / "repo_map_layers.yml"
GATES_YML = REPO / "scripts" / "gates.yml"
REPO_MAP = REPO / "REPO_MAP.md"
GATE_MANIFEST = REPO / "scripts" / "gate_manifest.py"

BEGIN = "<!-- BEGIN generated: scripts-table -->"
END = "<!-- END generated: scripts-table -->"

# Flags that change fail-closed vs warn/report. Ordinary invocation flags
# (--check, --all, --catalog-only) stay out of Notes.
_LOAD_BEARING_FLAGS: tuple[tuple[str, str], ...] = (
    ("--exit-zero", "WARN, --exit-zero"),
    ("--stats", "--stats (report-only)"),
    ("--check-tree-skew", "--check-tree-skew (report-only)"),
)

_SPECIAL_NOTES = {
    "gate_manifest.py": "gate runner (reads gates.yml); not itself a gated id",
}

_SECTION_HEADING = "### §2.1 — `scripts/` per-file layer (root-resident; recorded for the scanner)"

_INTRO = """\
Generated from `scripts_layer` in
[`repo_map_layers.yml`](scripts/repo_map_layers.yml) (loaded by
`check_boundaries.py` as `SCRIPTS_LAYER`; unlisted files fall back to
**governance** via `layer_of_file()`) and [`gates.yml`](scripts/gates.yml).
Neither the scanner nor [`check_repo_map_layers.py`](scripts/check_repo_map_layers.py)
reads this table. Regenerate with
`python scripts/check_repo_map_scripts_table.py --write`; `--check` exits 1 on drift.
"""

FALLBACK_MARK = "†"
NO_GATE = "—"
# Direct invocation or module-run trigger only: unlisted scripts may run inside
# another gate's script, as hooks or in CI.
LEGEND = (
    f"{FALLBACK_MARK} = layer fallback (not in `scripts_layer`); "
    f"Gate {NO_GATE} = no `gates.yml` command runs the file and no module-run gate "
    "triggers on it (it may still run inside another gate's script)."
)


def _load_scripts_layer(layers_yml: Path) -> dict[str, str]:
    """``scripts_layer`` from the layer-map file, via the scanner's own loader."""
    spec = importlib.util.spec_from_file_location("check_boundaries", BOUNDARIES)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {BOUNDARIES}")
    cb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cb)
    return dict(cb.load_layer_maps(layers_yml)["scripts_layer"])


def _load_gate_manifest():
    spec = importlib.util.spec_from_file_location("gate_manifest", GATE_MANIFEST)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {GATE_MANIFEST}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def list_scripts(repo: Path) -> list[str]:
    out = subprocess.check_output(
        ["git", "ls-files", "scripts/*.py"],
        cwd=repo,
        text=True,
    )
    return sorted(ln.strip() for ln in out.splitlines() if ln.strip())


# A cmd token carrying any of these is a pattern (unittest's test_*.py), not a path.
_GLOB_CHARS = ("*", "?", "[")


def _script_from_cmd(cmd: list[str]) -> str | None:
    for part in cmd:
        if any(ch in part for ch in _GLOB_CHARS):
            continue
        if part.startswith("scripts/") and part.endswith(".py"):
            return part
        if part.endswith(".py") and "/" not in part and not part.startswith("-"):
            return f"scripts/{part}"
    return None


def gates_by_script(gates: list[dict], scripts: list[str]) -> dict[str, list[dict]]:
    """Direct invocation wins; a module-run gate (no script in cmd) is credited to
    every tracked script its ``when.staged_regex`` selects."""
    by: dict[str, list[dict]] = {}
    for gate in gates:
        rel = _script_from_cmd(list(gate.get("cmd") or []))
        if rel is not None:
            by.setdefault(rel, []).append(gate)
            continue
        pattern = (gate.get("when") or {}).get("staged_regex")
        if not pattern:
            continue
        rx = re.compile(pattern)
        for path in scripts:
            if rx.match(path):
                by.setdefault(path, []).append(gate)
    return by


def _notes_for(rel: str, wired: list[dict]) -> str:
    """Exceptional notes only; the no-gate and layer-fallback defaults are in LEGEND."""
    bits: list[str] = []
    name = Path(rel).name
    if name in _SPECIAL_NOTES:
        bits.append(_SPECIAL_NOTES[name])
    seen: set[str] = set()
    for gate in wired:
        for part in gate.get("cmd") or []:
            for flag, label in _LOAD_BEARING_FLAGS:
                if part == flag and flag not in seen:
                    bits.append(label)
                    seen.add(flag)
    return "; ".join(bits)


def _gate_cell(wired: list[dict]) -> str:
    if not wired:
        return NO_GATE
    parts = []
    for gate in wired:
        gid = gate.get("id") or "?"
        tier = gate.get("tier") or "?"
        parts.append(f"`{gid}` ({tier})")
    return "; ".join(parts)


def build_rows(
    scripts: list[str],
    scripts_layer: dict[str, str],
    by_script: dict[str, list[dict]],
) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for rel in scripts:
        stem = Path(rel).stem
        layer = scripts_layer.get(stem, "governance" + FALLBACK_MARK)
        wired = by_script.get(rel, [])
        notes = _notes_for(rel, wired) or "—"
        rows.append((rel, layer, _gate_cell(wired), notes))
    return rows


def render_table(rows: list[tuple[str, str, str, str]]) -> str:
    lines = [
        "| Script | Layer | Gate id (tier) | Notes |",
        "|---|---|---|---|",
    ]
    for script, layer, gate, notes in rows:
        lines.append(f"| `{script}` | {layer} | {gate} | {notes} |")
    return "\n".join(lines)


def render_generated_block(rows: list[tuple[str, str, str, str]]) -> str:
    n = len(rows)
    caption = (
        f"_{n} tracked `scripts/*.py` files "
        f"(`git ls-files 'scripts/*.py'`)._"
    )
    return "\n".join(
        [
            BEGIN,
            caption,
            "",
            LEGEND,
            "",
            render_table(rows),
            END,
        ]
    )


def render_section(rows: list[tuple[str, str, str, str]]) -> str:
    return _INTRO + "\n" + render_generated_block(rows) + "\n"


def collect(
    *,
    repo: Path,
    layers: Path,
    gates_yml: Path,
) -> list[tuple[str, str, str, str]]:
    scripts_layer = _load_scripts_layer(layers)
    gm = _load_gate_manifest()
    data = gm.load_manifest(gates_yml)
    scripts = list_scripts(repo)
    by_script = gates_by_script(list(data.get("gates") or []), scripts)
    return build_rows(scripts, scripts_layer, by_script)


def _replace_section(text: str, section_body: str) -> str:
    if _SECTION_HEADING not in text:
        raise ValueError(f"REPO_MAP.md is missing heading: {_SECTION_HEADING}")
    start = text.index(_SECTION_HEADING)
    after_heading = start + len(_SECTION_HEADING)
    rest = text[after_heading:]
    # Section ends at the horizontal rule before the next ### heading.
    end_rel = rest.find("\n### ")
    if end_rel < 0:
        raise ValueError("REPO_MAP.md §2.1 has no following ### heading")
    before_next = rest[:end_rel]
    rule_at = before_next.rfind("\n---")
    if rule_at < 0:
        raise ValueError("REPO_MAP.md §2.1 is not closed by a --- rule")
    section_end = after_heading + rule_at
    new_body = "\n\n" + section_body.rstrip() + "\n"
    return text[:after_heading] + new_body + text[section_end:]


def extract_generated_block(text: str) -> str | None:
    if BEGIN not in text or END not in text:
        return None
    start = text.index(BEGIN)
    end = text.index(END) + len(END)
    return text[start:end]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO)
    parser.add_argument("--layers", type=Path, default=None,
                        help="layer-map file (default scripts/repo_map_layers.yml)")
    parser.add_argument("--gates", type=Path, default=None)
    parser.add_argument("--repo-map", type=Path, default=None)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    layers = args.layers or (root / "scripts" / "repo_map_layers.yml")
    gates_yml = args.gates or (root / "scripts" / "gates.yml")
    repo_map = args.repo_map or (root / "REPO_MAP.md")

    try:
        rows = collect(repo=root, layers=layers, gates_yml=gates_yml)
        section = render_section(rows)
        block = render_generated_block(rows)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"repo-map-scripts-table: FAIL — {exc}", file=sys.stderr)
        return 1

    if args.write:
        text = repo_map.read_text(encoding="utf-8")
        try:
            updated = _replace_section(text, section)
        except ValueError as exc:
            print(f"repo-map-scripts-table: FAIL — {exc}", file=sys.stderr)
            return 1
        repo_map.write_text(updated, encoding="utf-8", newline="\n")
        print(f"repo-map-scripts-table: wrote {len(rows)} rows into {repo_map}")
        return 0

    if args.check:
        if not repo_map.is_file():
            print(f"repo-map-scripts-table: FAIL — missing {repo_map}", file=sys.stderr)
            return 1
        existing = extract_generated_block(repo_map.read_text(encoding="utf-8"))
        if existing is None:
            print(
                "repo-map-scripts-table: FAIL — generated markers missing in "
                f"{repo_map}. Run --write.",
                file=sys.stderr,
            )
            return 1
        if existing.replace("\r\n", "\n") != block:
            print(
                "repo-map-scripts-table: FAIL — §2.1 table drift vs "
                "repo_map_layers.yml scripts_layer + gates.yml + git ls-files. "
                "Run: python scripts/check_repo_map_scripts_table.py --write",
                file=sys.stderr,
            )
            return 1
        print(f"repo-map-scripts-table: OK — {len(rows)} rows match sources")
        return 0

    print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
