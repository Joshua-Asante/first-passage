"""Guard: daemon import closure ⊆ Dockerfile COPY set (mirror listener guard)."""
from __future__ import annotations

import ast
from pathlib import Path
from image_manifest_support import ImageTestProfile, copied_python_paths, import_closure

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = REPO_ROOT / "deploy" / "c1_signal_daemon" / "Dockerfile"
_ENTRYPOINTS = (
    REPO_ROOT / "ops" / "c1_signal_daemon" / "daemon.py",
    REPO_ROOT / "ops" / "c1_signal_daemon" / "evaluate_loop.py",
    REPO_ROOT / "ops" / "c1_signal_daemon" / "book_evaluate_loop.py",
    REPO_ROOT / "ops" / "c1_signal_daemon" / "m1_stage1_control.py",
)


def _repo_import_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.level:
                package = path.parent.relative_to(REPO_ROOT / "ops").parts
                keep = len(package) - node.level + 1
                if keep >= 0:
                    names.add(".".join((*package[:keep], *node.module.split("."))))
            else:
                names.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
    return names


def _resolve_c1_signal_module(mod: str) -> Path | None:
    if mod.startswith("c1_rail"):
        rel = Path(*mod.split("."))
        candidate = REPO_ROOT / "ops" / rel.with_suffix(".py")
        return candidate if candidate.is_file() else None
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


def _profile(dockerfile=DOCKERFILE, entrypoints=_ENTRYPOINTS):
    return ImageTestProfile(dockerfile, entrypoints, ("ops/",),
                            _repo_import_names, _resolve_c1_signal_module, resolve_paths=False)


def _dockerfile_copied_py_paths(dockerfile: Path) -> set[str]:
    return copied_python_paths(_profile(dockerfile=dockerfile))


def _closure(entry: Path) -> set[Path]:
    return import_closure(_profile(entrypoints=(entry,)))


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


def test_daemon_build_context_allows_packaged_files():
    allowed = {line[1:] for line in (REPO_ROOT / ".dockerignore").read_text().splitlines()
               if line.startswith("!")}
    assert _dockerfile_copied_py_paths(DOCKERFILE) <= allowed


def test_relative_package_closure_detects_missing_copy(tmp_path, monkeypatch):
    monkeypatch.setattr(__import__(__name__), "REPO_ROOT", tmp_path)
    package = tmp_path / "ops/c1_signal_daemon"
    (package / "nested").mkdir(parents=True)
    entry = package / "entry.py"
    entry.write_text("from .nested import value\n", encoding="utf-8")
    init = package / "nested/__init__.py"
    init.write_text("from ..leaf import value\n", encoding="utf-8")
    leaf = package / "leaf.py"
    leaf.write_text("value = 1\n", encoding="utf-8")
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("COPY ops/c1_signal_daemon/entry.py /app/\n", encoding="utf-8")
    closure = _closure(entry)
    assert closure == {entry, init, leaf}
    assert {p.relative_to(tmp_path).as_posix() for p in closure} - _dockerfile_copied_py_paths(dockerfile) == {
        "ops/c1_signal_daemon/nested/__init__.py", "ops/c1_signal_daemon/leaf.py"}


def test_copy_profile_preserves_service_prefixes(tmp_path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("COPY core/a.py ops/b.py /app/\n", encoding="utf-8")
    assert _dockerfile_copied_py_paths(dockerfile) == {"ops/b.py"}
    from dataclasses import replace
    assert copied_python_paths(replace(_profile(dockerfile=dockerfile),
                                       copy_prefixes=("core/", "ops/"))) == {"core/a.py", "ops/b.py"}
