"""Guard: listener import closure ⊆ Dockerfile COPY set.

A module that the listener (transitively) imports but that is absent from every
`COPY` line yields a GREEN `fly deploy` build and a dead container at CMD —
`ModuleNotFoundError` cannot fail a COPY of a path that was never named.
That class bit once: `core/historical_challenge.py` (substrate Phase 4,
2026-07-30) was imported unguarded by `core/dd_protection.py` and missing from
`deploy/c1_rail/Dockerfile` until 2026-07-31. See the Dockerfile comment and
`.dockerignore` CAVEAT.

Direction is one-way on purpose. Operator CLIs (`c1_rail_arm.py`,
`c1_rail_slippage.py`) and the M1 acceptance JSON are COPYed but are not part
of the listener's import graph; extras in the image are fine. Missing closure
members are not.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = REPO_ROOT / "deploy" / "c1_rail" / "Dockerfile"
LISTENER = REPO_ROOT / "ops" / "c1_rail" / "c1_rail_listener.py"

# Roots whose transitive repo-local imports must be packaged. The listener is
# the decision core; the HTTP server is the CMD entrypoint (it imports the
# listener, but also pulls a few modules directly). Checking both closes the
# boot path the green-build / dead-container failure mode actually hits.
_ENTRYPOINTS = (
    REPO_ROOT / "ops" / "c1_rail" / "c1_rail_listener.py",
    REPO_ROOT / "ops" / "c1_rail" / "c1_rail_http_server.py",
)


def _dockerfile_copied_py_paths(dockerfile: Path) -> set[str]:
    """Parse COPY sources that are ops/ or core/ `.py` files.

    Joins `\\`-continued lines the way Dockerfiles are written in this repo,
    then takes every source token before the destination.
    """
    logical_lines: list[str] = []
    buf = ""
    for raw in dockerfile.read_text(encoding="utf-8").splitlines():
        stripped = raw.rstrip()
        if stripped.endswith("\\"):
            buf += stripped[:-1] + " "
            continue
        buf += stripped
        logical_lines.append(buf.strip())
        buf = ""

    copied: set[str] = set()
    for line in logical_lines:
        if not line.startswith("COPY "):
            continue
        tokens = line.split()[1:]
        if len(tokens) < 2:
            continue
        for src in tokens[:-1]:
            if src.endswith(".py") and (
                src.startswith("ops/") or src.startswith("core/")
            ):
                copied.add(src)
    return copied


def _repo_import_names(path: Path) -> set[str]:
    """Dotted module names referenced by import statements in `path`."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
    return names


def _resolve_repo_module(mod: str) -> Path | None:
    """Map a dotted import to an on-disk ops/ or core/ module, else None.

    Mirrors the image's sys.path bootstrap (`/app/ops/c1_rail`, `/app/core`):
    rail modules resolve under ops/c1_rail/; other flat ops modules under ops/;
    `lib.*` lives under `core/lib/`. Stdlib / third-party names resolve to
    nothing and are ignored.
    """
    rel = Path(*mod.split("."))
    candidates = (
        REPO_ROOT / "ops" / "c1_rail" / rel.with_suffix(".py"),
        REPO_ROOT / "ops" / rel.with_suffix(".py"),
        REPO_ROOT / "core" / rel.with_suffix(".py"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _import_closure(entrypoints: tuple[Path, ...]) -> set[Path]:
    """BFS over repo-local imports starting at `entrypoints`."""
    seen: set[Path] = set()
    queue = [p.resolve() for p in entrypoints]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        if not path.is_file():
            continue
        seen.add(path)
        for mod in _repo_import_names(path):
            resolved = _resolve_repo_module(mod)
            if resolved is not None:
                queue.append(resolved.resolve())
    return seen


def _repo_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def test_dockerfile_copy_set_is_nonempty():
    copied = _dockerfile_copied_py_paths(DOCKERFILE)
    assert copied, "Dockerfile PARSE produced an empty COPY set — parser broken?"
    assert "ops/c1_rail/c1_rail_listener.py" in copied
    assert "core/historical_challenge.py" in copied, (
        "regression pin: the 2026-07-31 bite must stay in the COPY set")


def test_listener_import_closure_is_covered_by_dockerfile_copy():
    """Every module the boot path imports must appear in a COPY line."""
    copied = _dockerfile_copied_py_paths(DOCKERFILE)
    closure = _import_closure(_ENTRYPOINTS)
    assert LISTENER.resolve() in closure

    missing = sorted(
        _repo_rel(path) for path in closure if _repo_rel(path) not in copied
    )
    assert missing == [], (
        "modules in the c1 rail import closure but absent from every Dockerfile "
        f"COPY line (green build, dead container): {missing}"
    )


def test_closure_includes_historical_challenge_regression_pin():
    """The exact module that bit on 2026-07-31 must be in the traced closure.

    If the AST walker ever stops seeing `dd_protection → historical_challenge`,
    this test fails loudly instead of silently weakening the COPY coverage
    check above (which would then pass vacuously on a thinner closure).
    """
    closure_rels = {_repo_rel(p) for p in _import_closure(_ENTRYPOINTS)}
    assert "core/historical_challenge.py" in closure_rels
    assert "core/lib/file_lock.py" in closure_rels
    assert "ops/c1_rail/c1_rail_telemetry.py" in closure_rels
