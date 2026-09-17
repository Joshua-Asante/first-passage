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
import re
import shutil
import subprocess
import sys
from pathlib import Path
from image_manifest_support import ImageTestProfile, copied_python_paths, import_closure

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
    REPO_ROOT / "ops" / "c1_rail" / "m1_stage1_control.py",
    REPO_ROOT / "ops" / "c1_rail" / "c1_rail_arm.py",
    REPO_ROOT / "ops" / "c1_rail" / "c1_rail_slippage.py",
)


def test_packaged_book_boundary_imports_without_checkout(tmp_path):
    """Exercise the lazy host import using only Python files in the image recipe."""
    for rel in _dockerfile_copied_py_paths(DOCKERFILE):
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO_ROOT / rel, target)
    script = """
import sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path[:0] = [str(root / 'ops'), str(root / 'core'), str(root / 'ops' / 'c1_rail')]
from c1_sizing_host_reference import C1SizingHostReference
host = C1SizingHostReference(root / 'absent', root / 'absent', root / 'absent')
result = host.process_book_signal(None, policy=None, context=None, binding=None, now=None)
assert result.halt and result.qty_out == 0 and result.submit is False
from c1_rail_slippage import TICK_SIZE_PTS
assert TICK_SIZE_PTS == {"dj30_mym": 1.0, "nas100_mnq": 0.25}
"""
    result = subprocess.run([sys.executable, "-I", "-c", script, str(tmp_path)],
                            cwd=tmp_path, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr


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
        REPO_ROOT / rel.with_suffix(".py"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _profile(dockerfile=DOCKERFILE, entrypoints=_ENTRYPOINTS):
    return ImageTestProfile(dockerfile, entrypoints, ("ops/", "core/"),
                            _repo_import_names, _resolve_repo_module, resolve_paths=True)


def _dockerfile_copied_py_paths(dockerfile: Path) -> set[str]:
    return copied_python_paths(_profile(dockerfile=dockerfile))


def _import_closure(entrypoints: tuple[Path, ...]) -> set[Path]:
    return import_closure(_profile(entrypoints=entrypoints))


def _repo_rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def test_dockerfile_copy_set_is_nonempty():
    copied = _dockerfile_copied_py_paths(DOCKERFILE)
    assert copied, "Dockerfile PARSE produced an empty COPY set — parser broken?"
    assert "ops/c1_rail/c1_rail_listener.py" in copied
    assert "core/historical_challenge.py" in copied, (
        "regression pin: the 2026-07-31 bite must stay in the COPY set")


def test_ci_exact_inventory_includes_packaged_python_modules():
    script = (REPO_ROOT / "scripts/c1_image_validation.sh").read_text(encoding="utf-8")
    inventory = re.search(r"(?ms)^LISTENER_FILES=\(\n(.*?)^\)", script)
    assert inventory is not None
    declared = set(re.findall(r"/app/([^\s\"']+\.py)", inventory.group(1)))
    assert _dockerfile_copied_py_paths(DOCKERFILE) <= declared


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


def test_packaged_files_are_allowed_in_build_context():
    # Default-excluded context must explicitly include each packaged module.
    allowed = {line[1:] for line in (REPO_ROOT / ".dockerignore").read_text().splitlines()
               if line.startswith("!")}
    assert _dockerfile_copied_py_paths(DOCKERFILE) <= allowed
