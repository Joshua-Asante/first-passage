"""Equivalent link primitives only; scanners own scope, resolution and severity."""
import re
import subprocess
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HISTORICAL_LINE_RE = re.compile(r"git\s+show|pre-prune-", re.IGNORECASE)
REPO_EXTENSIONS = (".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
                   ".sh", ".bat", ".csv")
DOCUMENT_EXTENSIONS = REPO_EXTENSIONS + (".txt", ".html")


def looks_like_path(path: str) -> bool:
    return "/" in path or path.startswith(".") or path.lower().endswith(DOCUMENT_EXTENSIONS)


def markdown_links(text: str, *, require_path_shape=False, skip_history=True):
    """Yield match, title-stripped target, anchor-stripped path in source order."""
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip().split(" ", 1)[0]
        path = target.split("#", 1)[0]
        if not path or path.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        if require_path_shape and not looks_like_path(path):
            continue
        end = text.find("\n", match.end())
        line = text[text.rfind("\n", 0, match.start()) + 1:end if end != -1 else len(text)]
        if skip_history and HISTORICAL_LINE_RE.search(line):
            continue
        yield match, target, path


def link_target(doc: Path, repo: Path, target: str, resolution: str) -> Path:
    if resolution == "repo":
        return repo / target
    if resolution != "document":
        raise ValueError(f"unknown link resolution: {resolution}")
    candidate = doc.parent / target
    try:
        return candidate.resolve()
    except OSError:
        return candidate


def is_gitignored(target: str, repo_root: Path) -> bool:
    try:
        return subprocess.run(["git", "check-ignore", "--quiet", target], cwd=repo_root,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
