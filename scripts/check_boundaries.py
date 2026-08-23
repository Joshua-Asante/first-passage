#!/usr/bin/env python3
"""check_boundaries.py — AST import-boundary scanner for the 4-layer monorepo.

Enforces the ADR 2026-06-05 dependency contract (`docs/adr/2026-06-05-monorepo-
layer-boundaries.md`); `REPO_MAP.md` is the human-readable source of truth.

Interpreter target (gate floor)
-------------------------------
This scanner AST-parses every non-exempt ``*.py`` under the running interpreter.
**Gate floor is Python 3.11** — matches ``pyproject.toml`` ``requires-python``,
CI's ``tests.yml`` matrix floor, and ``.venv-research`` (databento). Syntax that
only parses under 3.12+ (e.g. PEP 701 nested same-quote f-strings) is a
**parse failure under the gate floor**, not an illegal import edge. A verdict
that flips with whichever ``python`` is on PATH is not a gate; keep first-party
sources 3.11-parseable.

Contract (legal edges):
    governance -> core
    lab        -> core, governance
    ops        -> core, governance
    same-layer -> same-layer
  Illegal:  core -> {governance,lab,ops} ;  governance -> {lab,ops} ;
            lab <-> ops  (the load-bearing isolation invariant).

Layer of a source file is by path prefix. The application layers (core/, lab/,
ops/) are physically relocated; governance is root-resident (docs/, .claude/,
.github/, scripts/, root files) because moving it breaks tooling (REPO_MAP §2).
`tests/` is contract-EXEMPT (a single suite imports core+lab+ops at once,
ADR §8 Q-c). `scripts/` is root-resident but mixed-layer — classified per
REPO_MAP §2.1 (the dict below). `.claude/worktrees/<name>/` is also EXEMPT: a
git worktree checked out there is a full, independent repo copy with its own
core/lab/ops/tests — without this exemption its nested `tests/*.py` sits under
a `.claude/` (governance) prefix instead of a bare `tests/` prefix, so the scan
misclassified legitimate ops-importing test files as illegal governance->ops
edges (2026-07-06 housekeeping audit finding). Virtualenv roots (`.venv/`,
`venv/`, `env/` — mirroring .gitignore) are EXEMPT for the same class of reason:
site-packages is third-party code, not a contract party — scanning it AST-parses
thousands of vendored files on every pre-commit run, and any vendored module
with a bare `import cli` / `import analysis` (names in the first-party index)
would be misread as an illegal governance->ops/lab edge (2026-07-10 finding,
databento research-venv integration).

Resolution catches plain `import X`, `from X import Y`, aliased, and lazy/
in-function forms (ast.walk visits every node — the in-function import is exactly
what a line-grep missed at parity_check.py). Relative imports (`from . import`)
are same-layer by construction -> always legal.

Exit codes: 0 = no illegal edges, no name collisions, no unparseable sources;
1 = failure(s). Parse failures are reported separately from illegal edges.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

# Floor shared with pyproject requires-python / CI matrix / .venv-research.
MIN_PYTHON = (3, 11)

REPO_ROOT = Path(__file__).resolve().parent.parent

EXEMPT_PREFIXES = ("tests/", "archive/", ".claude/worktrees/", ".worktrees/",
                   ".venv/", ".venv-research/", "venv/", "env/",
                   "third_party/")  # venv roots + study clones (NeMo pin)
APP_LAYER_PREFIX = {"core/": "core", "lab/": "lab", "ops/": "ops"}
GOVERNANCE_PREFIXES = ("docs/", ".claude/", ".github/")

# scripts/ is root-resident, mixed-layer (REPO_MAP §2.1).
SCRIPTS_LAYER = {
    # governance — discipline / gates
    # (check_brief_evidence_coverage retired 2026-06-08 — ADR 2026-05-16-fixture-test-requirement Amendment)
    "check_brief": "governance",
    "archive_lab_analysis": "governance",
    "check_boundaries": "governance", "check_data_manifests": "governance",
    "check_pine_manifest": "governance", "check_skill_refs": "governance",
    "check_path_liveness": "governance", "pine_check": "governance",
    # parse_bar_export imports core/bar_export_loader only (governance->core legal)
    "parse_bar_export": "governance",
    "check_skills_no_constants": "governance",
    "verify_lock_anchors": "governance", "sync_pine_to_worktree": "governance",
    "sync_skills": "governance",
    # lab — research
    "mc_user_guardian": "lab",
    "beta_cohesion_read": "lab",
    "event_study_read": "lab",
    "pine_lint": "lab",
    "cost_geometry_pregate": "lab",
    "parse_econ_export": "lab",
    "diff_econ_calendar": "lab",
    # ops — live-ops tooling (run_ecr / preprocess_pine_ecr_logs retired 2026-07-11)
    "lock_event_hook": "ops",
}

LEGAL_EDGES = {
    ("governance", "core"),
    ("lab", "core"), ("lab", "governance"),
    ("ops", "core"), ("ops", "governance"),
    ("core", "core"), ("governance", "governance"),
    ("lab", "lab"), ("ops", "ops"),
}


def layer_of_file(rel: str) -> str | None:
    """Layer for a repo-relative posix path; None == exempt."""
    if rel.startswith(EXEMPT_PREFIXES):
        return None
    for pre, lyr in APP_LAYER_PREFIX.items():
        if rel.startswith(pre):
            return lyr
    if rel.startswith("scripts/"):
        return SCRIPTS_LAYER.get(Path(rel).stem, "governance")
    if rel.startswith(GOVERNANCE_PREFIXES):
        return "governance"
    return "governance"  # other root-resident .py (none after the move)


def _dir_has_py(d: Path) -> bool:
    return any(d.rglob("*.py"))


def build_index() -> tuple[dict[str, str], list[tuple[str, str, str]]]:
    """Map first-party top-level module/package name -> layer. Returns
    (index, collisions). A name in >1 layer is a hard error (Option B flattens
    the layer roots onto sys.path, so a collision mis-resolves silently)."""
    index: dict[str, str] = {}
    collisions: list[tuple[str, str, str]] = []

    def add(name: str, layer: str) -> None:
        if name.startswith("_"):
            return
        if name in index and index[name] != layer:
            collisions.append((name, index[name], layer))
        index.setdefault(name, layer)

    for layer in ("core", "lab", "ops"):
        root = REPO_ROOT / layer
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir()):
            if child.is_file() and child.suffix == ".py":
                add(child.stem, layer)
            elif child.is_dir() and child.name != "__pycache__" and _dir_has_py(child):
                add(child.name, layer)  # importable package / namespace dir
    return index, collisions


def _first_party_targets(tree: ast.AST, index: dict[str, str]) -> list[tuple[int, str, str]]:
    """Yield (lineno, module_name, target_layer) for each first-party import.
    Relative imports are skipped (same-layer by construction)."""
    out: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                head = alias.name.split(".", 1)[0]
                if head in index:
                    out.append((node.lineno, head, index[head]))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # relative -> same layer -> legal
            head = (node.module or "").split(".", 1)[0]
            if head in index:
                out.append((node.lineno, head, index[head]))
    return out


def main() -> int:
    py_ver = sys.version_info[:2]
    if py_ver < MIN_PYTHON:
        print(
            f"check_boundaries: REFUSED — running under Python {py_ver[0]}.{py_ver[1]}, "
            f"gate floor is {MIN_PYTHON[0]}.{MIN_PYTHON[1]} "
            f"(pyproject requires-python / CI / .venv-research). "
            f"Re-run with that interpreter or newer.",
            file=sys.stderr,
        )
        return 1

    index, collisions = build_index()
    edge_violations: list[str] = []
    parse_errors: list[str] = []
    py_label = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    for name, a, b in collisions:
        edge_violations.append(
            f"NAME COLLISION: module '{name}' in both {a}/ and {b}/ "
            f"(Option B flattens layer roots; rename or consolidate)")

    for path in sorted(REPO_ROOT.rglob("*.py")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(EXEMPT_PREFIXES) or "__pycache__" in rel:
            continue
        src_layer = layer_of_file(rel)
        if src_layer is None:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=rel)
        except SyntaxError as exc:
            # Not an illegal edge — AST could not run. Distinct so a 3.11
            # SyntaxError is never misread as an ADR H1 boundary finding.
            parse_errors.append(
                f"{rel}:{exc.lineno}: UNPARSEABLE under Python {py_label} — {exc.msg}")
            continue
        for lineno, mod, tgt_layer in _first_party_targets(tree, index):
            if (src_layer, tgt_layer) not in LEGAL_EDGES:
                edge_violations.append(
                    f"{rel}:{lineno}: ILLEGAL {src_layer}->{tgt_layer} "
                    f"import '{mod}' (legal {src_layer} targets: "
                    f"{sorted(t for s, t in LEGAL_EDGES if s == src_layer)})")

    failed = bool(edge_violations or parse_errors)
    if failed:
        parts = []
        if edge_violations:
            parts.append(f"{len(edge_violations)} illegal edge(s)/collision(s)")
        if parse_errors:
            parts.append(f"{len(parse_errors)} unparseable source(s)")
        print(f"check_boundaries: {'; '.join(parts)}")
        for v in edge_violations:
            print(f"  {v}")
        for v in parse_errors:
            print(f"  {v}")
        if edge_violations:
            print("\nA real illegal edge is a finding (ADR H1 falsifier), NOT a contract "
                  "to relax. Absorb a shared dep into core/, or reclassify a misfiled file.")
        if parse_errors:
            print("\nUNPARSEABLE is not an illegal edge. Fix the syntax for the gate "
                  f"floor (Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+), or move non-scanned "
                  "bytes out of the tree. Do not relax LEGAL_EDGES for a parse failure.")
        return 1
    print(f"check_boundaries: OK — {len(index)} first-party modules, "
          f"no illegal edges, no name collisions "
          f"(parsed under Python {py_label}; floor {MIN_PYTHON[0]}.{MIN_PYTHON[1]}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
