"""Service-specific image recipes with shared COPY parsing and graph traversal."""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ImageTestProfile:
    dockerfile: Path
    entrypoints: tuple[Path, ...]
    copy_prefixes: tuple[str, ...]
    imported_names: Callable[[Path], set[str]]
    resolve_module: Callable[[str], Path | None]
    resolve_paths: bool = False


def copied_python_paths(profile: ImageTestProfile) -> set[str]:
    """Parse COPY sources that are ops/ or core/ `.py` files.

    Joins `\\`-continued lines the way Dockerfiles are written in this repo,
    then takes every source token before the destination.
    """
    logical_lines: list[str] = []
    buf = ""
    for raw in profile.dockerfile.read_text(encoding="utf-8").splitlines():
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
                src.startswith(profile.copy_prefixes)
            ):
                copied.add(src)
    return copied


def import_closure(profile: ImageTestProfile) -> set[Path]:
    seen: set[Path] = set()
    stack = list(profile.entrypoints)
    while stack:
        path = stack.pop()
        if profile.resolve_paths:
            path = path.resolve()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        for name in profile.imported_names(path):
            resolved = profile.resolve_module(name)
            if resolved is not None:
                stack.append(resolved)
    return seen
