#!/usr/bin/env python3
"""check_md_relative_links.py — file-relative markdown link liveness (warn-only).

Sibling of `check_path_liveness.py` (MANIFEST parent dirs) and
`check_root_doc_liveness.py` (root orientation docs resolved against repo root).

Nested markdown under `docs/`, `ops/`, and `lab/` must resolve link targets
**relative to the containing file**, not as if every file lived at repo root.
The 2026-08-03 lab theme-nest move and root-shaped `](docs/adr/...)` hrefs
inside `docs/SESSIONS.md` are the motivating failure modes: root-doc liveness
cannot see them because those files are not in its five-doc scope, and a
repo-root resolve would falsely pass a `docs/adr/...` href written from
`docs/SESSIONS.md` (that path is `docs/docs/adr/...` file-relative).

Default mode is WARN-only (exit 0 even when dead links remain) so the corpus
debt can be measured before hardening. Pass `--strict` to exit 1 on misses.

Pure stdlib. Skips URLs, mailto/tel, pure `#anchor`s, gitignored targets, and
lines that deliberately cite evicted blobs (`git show` / `pre-prune-`).

Exit codes:
  0 — default (warn-only), or `--strict` with zero dead links
  1 — `--strict` and one or more dead links
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_GLOBS = (
    "*.md",
    "docs/**/*.md",
    "ops/**/*.md",
    "lab/**/*.md",
)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HISTORICAL_LINE_RE = re.compile(r"git\s+show|pre-prune-", re.IGNORECASE)
KNOWN_EXTS = (
    ".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
    ".sh", ".bat", ".csv", ".txt", ".html",
)


def _looks_like_path(path_part: str) -> bool:
    """Skip notation/anchors mistaken for paths (e.g. [r0](r0))."""
    if "/" in path_part or path_part.startswith("."):
        return True
    lower = path_part.lower()
    return any(lower.endswith(ext) for ext in KNOWN_EXTS)


_SKIP_PARTS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".claude",
    ".worktrees",
}


_GITIGNORE_CACHE: dict[tuple[str, str], bool] = {}


def _is_gitignored(target: str, repo_root: Path) -> bool:
    """True if `target` is gitignored (legit absence on clone/CI)."""
    key = (str(repo_root), target)
    cached = _GITIGNORE_CACHE.get(key)
    if cached is not None:
        return cached
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", target],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        hit = result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        hit = False
    _GITIGNORE_CACHE[key] = hit
    return hit


def _iter_markdown(repo_root: Path, globs: tuple[str, ...]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for pattern in globs:
        for path in sorted(repo_root.glob(pattern)):
            if not path.is_file():
                continue
            try:
                rel = path.relative_to(repo_root)
            except ValueError:
                continue
            if any(part in _SKIP_PARTS for part in rel.parts):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            out.append(path)
    return out


def check_file(doc_path: Path, repo_root: Path) -> list[str]:
    """Return dead-link messages for one markdown file (file-relative resolve)."""
    if not doc_path.exists():
        return [f"{doc_path.as_posix()}: file itself does not exist"]
    misses: list[str] = []
    text = doc_path.read_text(encoding="utf-8", errors="replace")
    rel_doc = doc_path.relative_to(repo_root).as_posix()
    for m in LINK_RE.finditer(text):
        target = m.group(1).strip()
        if " " in target:
            target = target.split(" ", 1)[0]
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        if path_part.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if not _looks_like_path(path_part):
            continue
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.end())
        line = text[line_start : line_end if line_end != -1 else len(text)]
        if HISTORICAL_LINE_RE.search(line):
            continue
        candidate = doc_path.parent / path_part
        try:
            candidate_resolved = candidate.resolve()
        except OSError:
            candidate_resolved = candidate
        if candidate_resolved.exists():
            continue
        ignore_probe = path_part
        if path_part.startswith(("./", "../")):
            try:
                ignore_probe = candidate_resolved.relative_to(
                    repo_root.resolve()
                ).as_posix()
            except ValueError:
                ignore_probe = path_part
        if _is_gitignored(ignore_probe, repo_root):
            continue
        if _is_gitignored(path_part, repo_root):
            continue
        lineno = text.count("\n", 0, m.start()) + 1
        misses.append(f"{rel_doc}:{lineno}: dead link -> {target}")
    return misses


def scan(
    repo_root: Path,
    globs: tuple[str, ...] = DEFAULT_GLOBS,
) -> tuple[list[str], int, int]:
    """Return (misses, files_scanned, links_checked)."""
    files = _iter_markdown(repo_root, globs)
    misses: list[str] = []
    links_checked = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if " " in target:
                target = target.split(" ", 1)[0]
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            if path_part.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            if not _looks_like_path(path_part):
                continue
            links_checked += 1
        misses.extend(check_file(path, repo_root))
    return misses, len(files), links_checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="repo root to scan",
    )
    parser.add_argument(
        "--glob",
        action="append",
        dest="globs",
        default=None,
        help="glob under repo root (repeatable; default: docs/ops/lab + root *.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when any dead link is found (default: warn-only, exit 0)",
    )
    args = parser.parse_args()
    globs = tuple(args.globs) if args.globs else DEFAULT_GLOBS
    misses, n_files, n_links = scan(args.repo_root, globs)

    for msg in misses:
        print(f"WARN: {msg}")

    print(
        f"\ncheck_md_relative_links: scanned {n_files} markdown file(s), "
        f"checked {n_links} non-URL link target(s), "
        f"{len(misses)} unresolved (file-relative)."
    )
    if misses and not args.strict:
        print(
            "Mode: WARN-only (exit 0). Re-run with --strict to hard-fail once "
            "the corpus is cleaned."
        )
        return 0
    if misses and args.strict:
        print("Mode: --strict; treating unresolved links as HARD failures.")
        return 1
    print("check_md_relative_links: OK — all scanned relative links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
