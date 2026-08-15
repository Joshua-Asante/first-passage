"""Repo-root resolver for lab packages and nested analysis harnesses."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return the monorepo root from any module under ``lab/<package>/``."""
    # lab/research_utils/repo_root.py → parents[0]=research_utils, [1]=lab, [2]=repo
    return Path(__file__).resolve().parents[2]


def repo_root_from(start: Path) -> Path:
    """Walk up from *start* until siblings ``lab/`` and ``core/`` are found.

    Use this from nested hot harnesses at ``lab/analysis/<theme>/<slug>/`` where
    a fixed ``parents[N]`` index is nest-depth-sensitive. Prefer over hard-coded
    ``HERE.parents[2]`` / ``Path(__file__).resolve().parents[3]`` (pre-nest).
    """
    p = start.resolve()
    if p.is_file():
        p = p.parent
    for candidate in (p, *p.parents):
        if (candidate / "lab").is_dir() and (candidate / "core").is_dir():
            return candidate
    raise FileNotFoundError(f"repo root not found above {start}")
