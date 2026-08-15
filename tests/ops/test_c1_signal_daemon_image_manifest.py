"""Guard: daemon import closure ⊆ Dockerfile COPY set (mirror listener guard)."""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = REPO_ROOT / "deploy" / "c1_signal_daemon" / "Dockerfile"
_ENTRYPOINTS = (
    REPO_ROOT / "ops" / "c1_signal_daemon" / "daemon.py",
    REPO_ROOT / "ops" / "c1_signal_daemon" / "evaluate_loop.py",
)


def _dockerfile_copied_py_paths(dockerfile: Path) -> set[str]:
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
            if src.endswith(".py") and src.startswith("ops/"):
                copied.add(src)
    return copied


def _repo_import_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
    return names


def _resolve_c1_signal_module(mod: str) -> Path | None:
    if not mod.startswith("c1_signal_daemon"):
        return None
    parts = mod.split(".")
    # c1_signal_daemon.foo -> ops/c1_signal_daemon/foo.py
    if len(parts) == 1:
        return REPO_ROOT / "ops" / "c1_signal_daemon" / "__init__.py"
    rel = Path(*parts[1:])
    py = REPO_ROOT / "ops" / "c1_signal_daemon" / f"{rel}.py"
    pkg = REPO_ROOT / "ops" / "c1_signal_daemon" / rel / "__init__.py"
    if py.is_file():
        return py
    if pkg.is_file():
        return pkg
    return None


def _closure(entry: Path) -> set[Path]:
    seen: set[Path] = set()
    stack = [entry]
    while stack:
        path = stack.pop()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        for mod in _repo_import_names(path):
            resolved = _resolve_c1_signal_module(mod)
            if resolved is not None and resolved not in seen:
                stack.append(resolved)
    return seen


def test_daemon_dockerfile_covers_import_closure():
    assert DOCKERFILE.is_file(), f"missing {DOCKERFILE}"
    copied = _dockerfile_copied_py_paths(DOCKERFILE)
    needed: set[str] = set()
    for entry in _ENTRYPOINTS:
        for path in _closure(entry):
            rel = path.relative_to(REPO_ROOT).as_posix()
            needed.add(rel)
    missing = sorted(needed - copied)
    assert missing == [], (
        "daemon Dockerfile missing COPY for import closure members "
        f"(green-build / dead-CMD class): {missing}"
    )
