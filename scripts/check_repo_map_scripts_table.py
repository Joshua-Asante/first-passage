#!/usr/bin/env python3
"""Emit / check the REPO_MAP.md §2.1 scripts table.

Row set: ``git ls-files 'scripts/*.py'``.
Layer: ``check_boundaries.py`` ``SCRIPTS_LAYER`` (fallback governance).
Gate wiring: ``scripts/gates.yml`` (id, tier, load-bearing flags).

This is a documentation generator. It does **not** change gate composition
(``gates.yml`` remains the sole owner). ``--check`` is available locally and
is not wired into ``gates.yml``.

Sibling of ``check_repo_map_layers.py`` (P5 map-compare). That gate stays a
dict↔YAML compare; this script owns the human-readable §2.1 table so the
section cannot drift into hand-maintained prose again.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOUNDARIES = REPO / "scripts" / "check_boundaries.py"
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
`scripts/` stays at root but its files are classified. Layer comes from
`check_boundaries.py`'s `SCRIPTS_LAYER`; anything not in that dict falls back
to **governance** via `layer_of_file()`. The scanner does **not** load this
table. The P5 gate ([`check_repo_map_layers.py`](scripts/check_repo_map_layers.py))
compares `SCRIPTS_LAYER` to [`repo_map_layers.yml`](scripts/repo_map_layers.yml),
not this table. Gate composition is owned by [`gates.yml`](scripts/gates.yml)
and is not changed by regenerating this section.

Regenerate: `python scripts/check_repo_map_scripts_table.py --write`.
`--check` exits 1 on drift; it is **not** wired into `gates.yml`.
"""


def _load_scripts_layer(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        name = node.targets[0]
        if isinstance(name, ast.Name) and name.id == "SCRIPTS_LAYER":
            value = ast.literal_eval(node.value)
            if not isinstance(value, dict):
                raise ValueError("SCRIPTS_LAYER is not a dict")
            return {str(k): str(v) for k, v in value.items()}
    raise ValueError(f"{path} has no SCRIPTS_LAYER assignment")


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


def _script_from_cmd(cmd: list[str]) -> str | None:
    for part in cmd:
        if part.startswith("scripts/") and part.endswith(".py"):
            return part
        if part.endswith(".py") and "/" not in part and not part.startswith("-"):
            return f"scripts/{part}"
    return None


def gates_by_script(gates: list[dict]) -> dict[str, list[dict]]:
    by: dict[str, list[dict]] = {}
    for gate in gates:
        rel = _script_from_cmd(list(gate.get("cmd") or []))
        if rel is None:
            continue
        by.setdefault(rel, []).append(gate)
    return by


def _notes_for(rel: str, wired: list[dict], *, in_layer_dict: bool) -> str:
    bits: list[str] = []
    name = Path(rel).name
    if name in _SPECIAL_NOTES:
        bits.append(_SPECIAL_NOTES[name])
    elif not wired:
        bits.append("manual/local only, not in gates.yml")
    seen: set[str] = set()
    for gate in wired:
        for part in gate.get("cmd") or []:
            for flag, label in _LOAD_BEARING_FLAGS:
                if part == flag and flag not in seen:
                    bits.append(label)
                    seen.add(flag)
    if not in_layer_dict:
        bits.append("layer fallback (not in SCRIPTS_LAYER)")
    return "; ".join(bits)


def _gate_cell(wired: list[dict]) -> str:
    if not wired:
        return "—"
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
        in_dict = stem in scripts_layer
        layer = scripts_layer.get(stem, "governance")
        wired = by_script.get(rel, [])
        notes = _notes_for(rel, wired, in_layer_dict=in_dict) or "—"
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
            render_table(rows),
            END,
        ]
    )


def render_section(rows: list[tuple[str, str, str, str]]) -> str:
    return _INTRO + "\n" + render_generated_block(rows) + "\n"


def collect(
    *,
    repo: Path,
    boundaries: Path,
    gates_yml: Path,
) -> list[tuple[str, str, str, str]]:
    scripts_layer = _load_scripts_layer(boundaries)
    gm = _load_gate_manifest()
    data = gm.load_manifest(gates_yml)
    by_script = gates_by_script(list(data.get("gates") or []))
    scripts = list_scripts(repo)
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
    parser.add_argument("--boundaries", type=Path, default=None)
    parser.add_argument("--gates", type=Path, default=None)
    parser.add_argument("--repo-map", type=Path, default=None)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    boundaries = args.boundaries or (root / "scripts" / "check_boundaries.py")
    gates_yml = args.gates or (root / "scripts" / "gates.yml")
    repo_map = args.repo_map or (root / "REPO_MAP.md")

    try:
        rows = collect(repo=root, boundaries=boundaries, gates_yml=gates_yml)
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
                "SCRIPTS_LAYER + gates.yml + git ls-files. "
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
