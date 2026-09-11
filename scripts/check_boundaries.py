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
what a line-grep missed at parity_check.py). Relative imports are resolved from
the source package; legal same-layer imports remain allowed. Dynamic imports
and filesystem reads are outside this AST import check.

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
                   "third_party/")  # venv-class: untracked vendor / study trees
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
    "audit_notice_grade_k_correction": "lab",
    "event_study_read": "lab",
    "pine_lint": "lab",
    "cost_geometry_pregate": "lab",
    "check_cost_model_closed_world": "lab",
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


# Import roots used by pyproject.toml, scripts/layer_bootstrap.py and the rail
# entry points. Mirror in repo_map_layers.yml and REPO_MAP section 2.2.
FLAT_IMPORT_ROOTS = ("core", "lab", "ops", "ops/c1_rail", "ops/c1_signal_daemon", "scripts")


def build_index() -> tuple[dict[str, tuple[str, ...]], list[tuple[str, tuple[str, ...]]]]:
    """Resolve importable names to repository paths, including namespace packages.

    Never recursively flatten arbitrary directories: only documented import roots
    create bare names. Retain every candidate so cross-layer ambiguity fails closed.
    """
    candidates: dict[str, set[str]] = {}
    for path in sorted(REPO_ROOT.rglob("*.py")):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if layer_of_file(rel) is None or "__pycache__" in path.parts:
            continue
        for root in ("", *FLAT_IMPORT_ROOTS):
            prefix = root + "/" if root else ""
            if not rel.startswith(prefix):
                continue
            parts = rel[len(prefix):].split("/")
            parts[-1] = parts[-1][:-3]
            if parts[-1] == "__init__":
                parts.pop()
            if not parts or not all(part.isidentifier() for part in parts):
                continue
            name = ".".join(parts)
            candidates.setdefault(name, set()).add(rel)
            # Namespace directories are importable even without __init__.py.
            for count in range(1, len(parts)):
                parent = ".".join(parts[:count])
                directory = prefix + "/".join(parts[:count]) + "/"
                candidates.setdefault(parent, set()).add(directory)
    index = {}
    for name, paths in candidates.items():
        # Package initializers take precedence over the synthetic directory entry.
        index[name] = tuple(sorted(path for path in paths
                                   if not (path.endswith("/") and path + "__init__.py" in paths)))
    collisions = [(name, paths) for name, paths in sorted(index.items())
                  if len({layer_of_file(path) for path in paths}) > 1]
    return index, collisions


def _first_party_targets(tree: ast.AST, index: dict[str, tuple[str, ...]],
                         source: str = "") -> list[tuple[int, str, str | None]]:
    """Return (line, import name, resolved path); None marks unresolved first-party.

    Unknown absolute roots are external. A known first-party root with a missing
    module is an error, distinct from external imports. For from-imports, resolve
    an imported submodule before treating its name as an attribute of the base.
    """
    out: list[tuple[int, str, str | None]] = []
    first_party = {name.split(".")[0] for name in index} | {"core", "lab", "ops", "scripts"}

    def emit(line: int, name: str, force: bool = False) -> None:
        if name in index:
            out.extend((line, name, path) for path in index[name])
        elif force or name.split(".")[0] in first_party:
            out.append((line, name, None))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                emit(node.lineno, alias.name)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parents = source.split("/")[:-1]
                if node.level > len(parents):
                    emit(node.lineno, "." * node.level + base, True)
                    continue
                base = ".".join(parents[:len(parents) - node.level + 1] + ([base] if base else []))
            resolved_child = False
            needs_base = False
            for alias in node.names:
                child = base + "." + alias.name
                if child in index:
                    emit(node.lineno, child)
                    resolved_child = True
                else:
                    needs_base = True
            if needs_base or not resolved_child:
                emit(node.lineno, base, bool(node.level))
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

    for name, paths in collisions:
        edge_violations.append(
            f"NAME COLLISION: module '{name}' candidates {list(paths)} "
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
        for lineno, mod, target in _first_party_targets(tree, index, rel):
            if target is None:
                kind = "INVALID RELATIVE" if mod.startswith(".") else "UNRESOLVED first-party"
                edge_violations.append(f"{rel}:{lineno}: {kind} import '{mod}'")
                continue
            tgt_layer = layer_of_file(target)
            if (src_layer, tgt_layer) not in LEGAL_EDGES:
                edge_violations.append(
                    f"{rel}:{lineno}: ILLEGAL {src_layer}->{tgt_layer} "
                    f"import '{mod}' -> {target} (legal {src_layer} targets: "
                    f"{sorted(t for s, t in LEGAL_EDGES if s == src_layer)})")

    failed = bool(edge_violations or parse_errors)
    if failed:
        parts = []
        if edge_violations:
            parts.append(f"{len(edge_violations)} import failure(s)/collision(s)")
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
