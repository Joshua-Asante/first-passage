#!/usr/bin/env python3
"""sync_skills.py — skill drift diagnostics and explicit revision publication.

ONE-WAY CONTRACT (ADR docs/adr/2026-06-04-methodology-skills-under-vc.md §2.2):
the repo is the single source of truth. Skills flow repo -> deployed ONLY.
This script never copies deployed -> repo.

Publication is an explicit release: both --revision and --target are required.
The invocation is the caller's attestation that the named revision was reviewed.
Git metadata proves revision identity only; this tool never prints
"review verified". --force is accepted only to emit a migration error and
never bypasses the release checks.

--check remains read-only from any checkout. It never creates a target,
snapshot, cache, or log under the target and never implies permission to
publish. Diagnostic default-target resolution stays on resolve_targets().

Exit codes:
  0 — publication succeeded / no substantive diagnostic drift
  1 — diagnostic drift, or preparation/install/rollback error
  2 — invalid/missing source or CLI input
  3 — source-policy refusal
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import sys
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_SKILLS = REPO_ROOT / ".claude" / "skills"

DEFAULT_DEPLOY_TARGET = Path(
    os.path.expandvars(
        r"%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin"
        r"\72fdf38f-9be5-43cc-9803-8e04bfac2290"
        r"\4a461c5e-0034-4ec3-8928-8324158d1365\skills"
    )
)

HOME_SKILLS_DEPLOY_TARGET = Path.home() / ".claude" / "skills"

STOCK_SKILLS_EXEMPT = frozenset({
    "consolidate-memory",
    "docx",
    "pdf",
    "pptx",
    "schedule",
    "session-start-hook",
    "setup-cowork",
    "skill-creator",
    "xlsx",
})

GENERATED_DIR_NAMES = frozenset({
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
})
GENERATED_FILE_NAMES = frozenset({".DS_Store"})
GENERATED_SUFFIXES = frozenset({".pyc", ".pyo"})
TEXT_COMPARE_SUFFIXES = frozenset({
    ".md", ".mdc", ".py", ".js", ".json", ".yaml", ".yml", ".txt",
})
RULE0_SKILL = "rule-0"
RULE0_OWNER = "docs/pursuits/d3-rule-0-user-skill.md"
MAIN_BRANCH = "main"

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_POLICY = 3

_REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def is_under_worktrees(path: Path) -> bool:
    """True if *path* sits inside a `.claude/worktrees/` tree (worktree session)."""
    parts = [s.lower() for s in Path(path).parts]
    return any(
        parts[i] == ".claude" and parts[i + 1] == "worktrees"
        for i in range(len(parts) - 1)
    )


def resolve_target(explicit: str | None) -> Path:
    """Resolve the *primary* deploy target (AppData / env / --target).

    Kept as a single-Path helper so import_skill_from_cache.py (and any other
    caller that needs one root) stays stable. Prefer resolve_targets() for
    deploy/--check so the home bundle is included under default resolution.
    """
    if explicit:
        return Path(explicit)
    env = os.environ.get("SKILLS_DEPLOY_TARGET")
    if env:
        return Path(env)
    return DEFAULT_DEPLOY_TARGET


def resolve_targets(explicit: str | None) -> list[Path]:
    """All destinations for diagnostic --check.

    Explicit --target is the sole destination (test isolation + one-off ops).
    Otherwise the primary slot (env or DEFAULT_DEPLOY_TARGET) is paired with
    HOME_SKILLS_DEPLOY_TARGET when that path is distinct.
    """
    if explicit:
        return [Path(explicit)]
    primary = resolve_target(None)
    targets = [primary]
    home = HOME_SKILLS_DEPLOY_TARGET
    try:
        if home.resolve() != primary.resolve():
            targets.append(home)
    except OSError:
        targets.append(home)
    return targets


def _is_generated_rel(rel: str) -> bool:
    parts = Path(rel.replace("\\", "/")).parts
    if any(part in GENERATED_DIR_NAMES or part in GENERATED_FILE_NAMES for part in parts):
        return True
    name = parts[-1] if parts else ""
    return Path(name).suffix.lower() in GENERATED_SUFFIXES


def _iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    if not root.exists():
        return files
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name not in GENERATED_DIR_NAMES]
        current = Path(dirpath)
        if _path_is_reparse(current):
            continue
        for name in filenames:
            if name in GENERATED_FILE_NAMES or Path(name).suffix.lower() in GENERATED_SUFFIXES:
                continue
            path = current / name
            if path.is_file() and not _path_is_reparse(path):
                files.append(path)
    return files


def _normalized_text_bytes(data: bytes, suffix: str) -> bytes:
    if suffix.lower() not in TEXT_COMPARE_SUFFIXES:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _files_differ(left: Path, right: Path) -> bool:
    left_bytes = left.read_bytes()
    right_bytes = right.read_bytes()
    return _normalized_text_bytes(left_bytes, left.suffix) != _normalized_text_bytes(
        right_bytes, right.suffix
    )


def diff_skill(repo_skill: Path, deployed_skill: Path) -> list[str]:
    """Return relative paths that diverge (missing or differing) for one skill."""
    diverging: list[str] = []
    for f in _iter_files(repo_skill):
        rel = f.relative_to(repo_skill).as_posix()
        target_f = deployed_skill / f.relative_to(repo_skill)
        if not target_f.exists():
            diverging.append(f"{repo_skill.name}/{rel}  (missing in deployed)")
        elif _entry_kind(target_f) != "file":
            diverging.append(
                f"{repo_skill.name}/{rel}  (deployed entry is not a regular file)"
            )
        elif _files_differ(f, target_f):
            diverging.append(f"{repo_skill.name}/{rel}  (content differs)")
    if deployed_skill.is_dir():
        for f in _iter_files(deployed_skill):
            rel = f.relative_to(deployed_skill)
            if not (repo_skill / rel).exists():
                diverging.append(
                    f"{repo_skill.name}/{rel.as_posix()}  (extra in deployed)")
    return diverging


def find_extra_deployed_skills(repo_skills: Path, target: Path) -> list[str]:
    """Whole deployed directories with no repo counterpart at all."""
    if not target.is_dir():
        return []
    repo_names = {p.name for p in repo_skills.iterdir() if p.is_dir()}
    extras: list[str] = []
    for d in sorted(p for p in target.iterdir() if p.is_dir()):
        if d.name in repo_names or d.name in STOCK_SKILLS_EXEMPT:
            continue
        if d.name.startswith(".skill-release-"):
            continue
        if d.name == RULE0_SKILL:
            extras.append(
                f"{d.name}  (intentionally separately owned; "
                f"see {RULE0_OWNER})"
            )
            continue
        extras.append(
            f"{d.name}  (extra top-level skill in deployed, no repo copy — import or delete)"
        )
    return extras


def check_drift(repo_skills: Path, target: Path) -> list[str]:
    """Compare every in-repo skill against the deploy target. Returns drift list."""
    drift: list[str] = []
    for skill_dir in sorted(p for p in repo_skills.iterdir() if p.is_dir()):
        if skill_dir.name.startswith("."):
            continue
        drift.extend(diff_skill(skill_dir, target / skill_dir.name))
    drift.extend(find_extra_deployed_skills(repo_skills, target))
    return drift


def copy_skills(repo_skills: Path, target: Path) -> int:
    """Copy every in-repo skill into the target (repo -> deployed). Returns count.

    Test/helper fixture only. Publication uses revision-tracked bytes via
    _stage_release_payload, never this working-tree copy.
    """
    target.mkdir(parents=True, exist_ok=True)
    n = 0
    for skill_dir in sorted(p for p in repo_skills.iterdir() if p.is_dir()):
        dst = target / skill_dir.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill_dir, dst)
        n += 1
    return n


def _run_git(cwd: Path, *args: str, binary: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=not binary,
        check=False,
    )


def _git_ok(proc: subprocess.CompletedProcess) -> bool:
    return proc.returncode == 0


def _same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve())) == os.path.normcase(str(right.resolve()))


def _abs_git_path(cwd: Path, spec: str) -> Path | None:
    proc = _run_git(cwd, "rev-parse", spec)
    if not _git_ok(proc):
        return None
    raw = (proc.stdout or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = cwd / path
    return path.resolve()


def _path_is_reparse(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(path, "is_junction", None)
        if callable(is_junction) and is_junction():
            return True
        st = os.lstat(path)
        attrs = getattr(st, "st_file_attributes", 0)
        if attrs & _REPARSE_ATTRIBUTE:
            return True
    except OSError:
        return False
    if os.name == "nt":
        try:
            import ctypes
            GetFileAttributesW = ctypes.windll.kernel32.GetFileAttributesW
            GetFileAttributesW.argtypes = [ctypes.c_wchar_p]
            GetFileAttributesW.restype = ctypes.c_uint32
            attrs = GetFileAttributesW(str(path))
            if attrs != 0xFFFFFFFF and attrs & _REPARSE_ATTRIBUTE:
                return True
        except (AttributeError, OSError, ValueError):
            return False
    return False


def _any_reparse_in_tree(root: Path) -> bool:
    if not root.exists() and not root.is_symlink():
        return False
    if _path_is_reparse(root):
        return True
    if not root.is_dir():
        return False
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        if _path_is_reparse(current):
            return True
        for name in list(dirnames) + list(filenames):
            if _path_is_reparse(current / name):
                return True
    return False


def _path_has_reparse_ancestor(path: Path) -> bool:
    """True if *path* or an unresolved ancestor is a symlink/junction/reparse."""
    current = Path(path)
    while True:
        try:
            if current.exists() or current.is_symlink():
                if _path_is_reparse(current):
                    return True
        except OSError:
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _entry_kind(path: Path) -> str:
    if _path_is_reparse(path):
        return "reparse"
    if path.is_dir():
        return "dir"
    if path.is_file():
        return "file"
    return "other"


def _tree_inventory(path: Path) -> dict[str, dict]:
    """Nested kinds, reparse presence, and file hashes. Does not follow links."""
    if not path.exists() and not path.is_symlink():
        return {}
    out: dict[str, dict] = {}
    if _path_is_reparse(path):
        return {".": {"kind": "reparse"}}
    for dirpath, dirnames, filenames in os.walk(path, followlinks=False):
        current = Path(dirpath)
        if current != path and _path_is_reparse(current):
            dirnames[:] = []
            continue
        keep_dirs: list[str] = []
        for name in dirnames:
            child = current / name
            rel = child.relative_to(path).as_posix()
            kind = _entry_kind(child)
            out[rel] = {"kind": kind}
            if kind != "reparse":
                keep_dirs.append(name)
        dirnames[:] = keep_dirs
        for name in filenames:
            child = current / name
            rel = child.relative_to(path).as_posix()
            kind = _entry_kind(child)
            rec: dict = {"kind": kind}
            if kind == "file":
                rec["hash"] = hashlib.sha256(child.read_bytes()).hexdigest()
            out[rel] = rec
    return out


def _target_snapshot(target: Path) -> dict:
    if not target.exists() and not target.is_symlink():
        return {"exists": False}
    snap: dict = {"exists": True, "kind": _entry_kind(target)}
    if snap["kind"] == "file":
        snap["hash"] = hashlib.sha256(target.read_bytes()).hexdigest()
        return snap
    if snap["kind"] != "dir":
        return snap
    children: dict[str, dict] = {}
    for child in sorted(target.iterdir()):
        if child.name.startswith(".skill-release-"):
            continue
        kind = _entry_kind(child)
        rec: dict = {"kind": kind}
        if kind == "file":
            rec["hash"] = hashlib.sha256(child.read_bytes()).hexdigest()
        elif kind == "dir":
            rec["tree"] = _tree_inventory(child)
        children[child.name] = rec
    snap["children"] = children
    return snap


def _classify_checkout(repo_skills: Path) -> tuple[str, Path | None, str]:
    """Return (kind, toplevel, detail). kind is primary_main or a refusal token."""
    try:
        top_proc = _run_git(repo_skills, "rev-parse", "--show-toplevel")
    except FileNotFoundError:
        return "unavailable_git", None, "git is not available"
    if not _git_ok(top_proc):
        return "no_git", None, "not a git checkout"
    toplevel = Path((top_proc.stdout or "").strip())
    if not str(toplevel):
        return "unknown_git", None, "git toplevel is empty"
    toplevel = toplevel.resolve()

    super_proc = _run_git(repo_skills, "rev-parse", "--show-superproject-working-tree")
    if _git_ok(super_proc) and (super_proc.stdout or "").strip():
        return "submodule", toplevel, "source is a git submodule"

    git_dir = _abs_git_path(repo_skills, "--absolute-git-dir")
    common_dir = _abs_git_path(repo_skills, "--git-common-dir")
    if git_dir is None or common_dir is None:
        return "unknown_git", toplevel, "git directory metadata is unavailable"

    if not _same_path(git_dir, common_dir):
        return "linked_worktree", toplevel, "source is a linked worktree"

    expected_git = (toplevel / ".git").resolve()
    if not _same_path(git_dir, expected_git) or not expected_git.is_dir():
        return "separate_git_dir", toplevel, "source uses a separate git directory"

    head_proc = _run_git(repo_skills, "rev-parse", "--abbrev-ref", "HEAD")
    if not _git_ok(head_proc):
        return "unknown_git", toplevel, "HEAD cannot be resolved"
    branch = (head_proc.stdout or "").strip()
    if branch in {"", "HEAD"}:
        return "detached", toplevel, "source HEAD is detached"
    if branch != MAIN_BRANCH:
        return "non_main", toplevel, f"source branch is {branch!r}, not {MAIN_BRANCH!r}"
    return "primary_main", toplevel, ""


def _resolve_revision(repo_skills: Path, commitish: str) -> str | None:
    proc = _run_git(repo_skills, "rev-parse", "--verify", f"{commitish}^{{commit}}")
    if not _git_ok(proc):
        return None
    sha = (proc.stdout or "").strip()
    return sha or None


def _head_sha(repo_skills: Path) -> str | None:
    proc = _run_git(repo_skills, "rev-parse", "HEAD")
    if not _git_ok(proc):
        return None
    sha = (proc.stdout or "").strip()
    return sha or None


def _skills_rel(toplevel: Path, repo_skills: Path) -> str:
    return repo_skills.resolve().relative_to(toplevel).as_posix()


def _payload_problems(repo_skills: Path, toplevel: Path, revision: str) -> list[str]:
    """Compare releasable disk membership to the named revision.

    Ignores index hints (assume-unchanged / skip-worktree) and gitignore.
    Generated caches are excluded. Working-tree comparison uses Git's
    configured clean conversion (`hash-object --path`) so a clean CRLF
    checkout can match an LF blob. Publication still stages exact blob bytes.
    """
    rel = _skills_rel(toplevel, repo_skills)
    listed = _run_git(toplevel, "ls-tree", "-r", "--name-only", revision, "--", rel)
    if not _git_ok(listed):
        return ["unable to list revision skill payload"]
    prefix = rel.rstrip("/") + "/"
    tracked: set[str] = set()
    for raw in (listed.stdout or "").splitlines():
        path = raw.strip().replace("\\", "/")
        if not path or _is_generated_rel(path):
            continue
        tracked.add(path)

    disk: set[str] = set()
    if repo_skills.is_dir():
        for dirpath, dirnames, filenames in os.walk(repo_skills, followlinks=False):
            dirnames[:] = [name for name in dirnames if name not in GENERATED_DIR_NAMES]
            current = Path(dirpath)
            if _path_is_reparse(current):
                return [f"reparse point inside skill payload: {current}"]
            for name in filenames:
                if name in GENERATED_FILE_NAMES or Path(name).suffix.lower() in GENERATED_SUFFIXES:
                    continue
                path = current / name
                if _path_is_reparse(path):
                    return [f"reparse point inside skill payload: {path}"]
                disk.add(path.relative_to(toplevel).as_posix())

    problems: list[str] = []
    for extra in sorted(disk - tracked):
        problems.append(f"untracked or ignored releasable file: {extra}")
    for missing in sorted(tracked - disk):
        problems.append(f"missing tracked payload: {missing}")
    for path in sorted(tracked & disk):
        blob = _run_git(toplevel, "rev-parse", f"{revision}:{path}")
        hashed = _run_git(toplevel, "hash-object", "--path", path, "--", path)
        if not _git_ok(blob) or not _git_ok(hashed):
            problems.append(f"unreadable payload: {path}")
            continue
        if (blob.stdout or "").strip() != (hashed.stdout or "").strip():
            problems.append(f"working-tree payload differs from revision: {path}")
    return problems


def _paths_overlap(left: Path, right: Path) -> bool:
    try:
        left_r = left.resolve()
        right_r = right.resolve()
    except OSError:
        return True
    if _same_path(left_r, right_r):
        return True
    left_parts = os.path.normcase(str(left_r))
    right_parts = os.path.normcase(str(right_r))
    sep = os.sep
    return (
        right_parts.startswith(left_parts + sep)
        or left_parts.startswith(right_parts + sep)
    )


def _is_git_dir(path: Path) -> bool:
    try:
        return (path / "HEAD").exists() and (
            (path / "objects").is_dir()
            or (path / "refs").is_dir()
            or (path / "commondir").is_file()
        )
    except OSError:
        return False


def _gitfile_gitdir(gitfile: Path) -> Path | None:
    try:
        text = gitfile.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not text.lower().startswith("gitdir:"):
        return None
    raw = text.split(":", 1)[1].strip()
    path = Path(raw)
    if not path.is_absolute():
        path = gitfile.parent / path
    try:
        return path.resolve()
    except OSError:
        return None


def _inside_any_git_metadata(target: Path) -> bool:
    """Refuse any path inside Git metadata, including unrelated repositories."""
    chain: list[Path] = [target, *target.parents]
    try:
        resolved = target.resolve()
        chain.extend([resolved, *resolved.parents])
    except OSError:
        return True

    seen: set[str] = set()
    for cand in chain:
        key = os.path.normcase(str(cand))
        if key in seen:
            continue
        seen.add(key)
        if cand.name == ".git" or _is_git_dir(cand):
            return True
        if any(part == ".git" for part in cand.parts):
            return True
        gitfile = cand / ".git"
        if gitfile.is_file():
            gitdir = _gitfile_gitdir(gitfile)
            if gitdir is None:
                return True
            try:
                resolved_target = target.resolve()
            except OSError:
                return True
            if _same_path(resolved_target, gitdir) or gitdir in resolved_target.parents:
                return True

    start = target if target.exists() else target.parent
    if start.exists():
        try:
            git_dir = _abs_git_path(start, "--absolute-git-dir")
        except FileNotFoundError:
            return True
        if git_dir is not None:
            try:
                resolved_target = target.resolve()
                git_dir_r = git_dir.resolve()
            except OSError:
                return True
            if _same_path(resolved_target, git_dir_r) or git_dir_r in resolved_target.parents:
                return True
    return False


def _require_safe_io_path(path: Path) -> None:
    if _path_has_reparse_ancestor(path) or _path_is_reparse(path):
        raise OSError(f"symlink/junction/reparse in path: {path}")
    if _inside_any_git_metadata(path):
        raise OSError(f"path is inside git metadata: {path}")


def _require_safe_tree(path: Path) -> None:
    _require_safe_io_path(path)
    if path.exists() and path.is_dir() and _any_reparse_in_tree(path):
        raise OSError(f"symlink/junction/reparse in tree: {path}")


def _safe_replace(src: Path, dest: Path) -> None:
    _require_safe_tree(src)
    _require_safe_io_path(dest)
    if dest.exists() or dest.is_symlink():
        _require_safe_tree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    os.replace(src, dest)


def _safe_rmtree(path: Path, ignore_errors: bool = False) -> None:
    try:
        _require_safe_tree(path)
    except OSError:
        if ignore_errors:
            return
        raise
    shutil.rmtree(path, ignore_errors=ignore_errors)


def _stage_release_payload(
    repo_skills: Path,
    revision: str,
    staging_root: Path,
) -> Path:
    toplevel_proc = _run_git(repo_skills, "rev-parse", "--show-toplevel")
    if not _git_ok(toplevel_proc):
        raise OSError("unable to resolve git toplevel for staging")
    toplevel = Path((toplevel_proc.stdout or "").strip()).resolve()
    rel = _skills_rel(toplevel, repo_skills)
    listed = _run_git(toplevel, "ls-tree", "-r", "--name-only", revision, "--", rel)
    if not _git_ok(listed):
        raise OSError("unable to list revision skill payload")
    staging_root.mkdir(parents=True, exist_ok=True)
    wrote_any = False
    for raw in (listed.stdout or "").splitlines():
        path = raw.strip()
        if not path or _is_generated_rel(path):
            continue
        blob = _run_git(toplevel, "show", f"{revision}:{path}", binary=True)
        if blob.returncode != 0:
            raise OSError(f"unable to read {path} from {revision}")
        rel_skill = Path(path).as_posix()
        prefix = rel.rstrip("/") + "/"
        if not rel_skill.startswith(prefix):
            continue
        dest = staging_root / rel_skill[len(prefix):]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob.stdout)
        wrote_any = True
    if not wrote_any:
        raise OSError("revision contains no releasable skill payload")
    for skill_dir in sorted(p for p in staging_root.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").is_file():
            raise OSError(f"staged skill {skill_dir.name} is missing SKILL.md")
    return staging_root


def _revision_payload_manifest(repo_skills: Path, revision: str) -> dict[str, bytes]:
    toplevel_proc = _run_git(repo_skills, "rev-parse", "--show-toplevel")
    if not _git_ok(toplevel_proc):
        raise OSError("unable to resolve git toplevel for manifest")
    toplevel = Path((toplevel_proc.stdout or "").strip()).resolve()
    rel = _skills_rel(toplevel, repo_skills)
    listed = _run_git(toplevel, "ls-tree", "-r", "--name-only", revision, "--", rel)
    if not _git_ok(listed):
        raise OSError("unable to list revision skill payload")
    prefix = rel.rstrip("/") + "/"
    manifest: dict[str, bytes] = {}
    for raw in (listed.stdout or "").splitlines():
        path = raw.strip().replace("\\", "/")
        if not path or _is_generated_rel(path) or not path.startswith(prefix):
            continue
        blob = _run_git(toplevel, "show", f"{revision}:{path}", binary=True)
        if blob.returncode != 0:
            raise OSError(f"unable to read {path} from {revision}")
        manifest[path[len(prefix):]] = blob.stdout
    if not manifest:
        raise OSError("revision contains no releasable skill payload")
    return manifest


def _staged_payload_problems(
    staging_root: Path, expected: dict[str, bytes]
) -> list[str]:
    """Inventory every staged entry, including generated names and reparses."""
    problems: list[str] = []
    found: dict[str, bytes] = {}
    expected_dirs = {
        parent.as_posix()
        for rel in expected
        for parent in Path(rel).parents
        if parent != Path(".")
    }
    if not staging_root.exists():
        return ["staged payload is missing"]
    for dirpath, dirnames, filenames in os.walk(staging_root, followlinks=False):
        current = Path(dirpath)
        if current != staging_root and _path_is_reparse(current):
            problems.append(
                "reparse in staged payload: "
                + current.relative_to(staging_root).as_posix()
            )
            dirnames[:] = []
            continue
        keep_dirs: list[str] = []
        for name in dirnames:
            child = current / name
            rel = child.relative_to(staging_root).as_posix()
            if rel not in expected_dirs:
                problems.append(f"unexpected staged directory: {rel}")
            if _path_is_reparse(child):
                problems.append(
                    "reparse in staged payload: "
                    + child.relative_to(staging_root).as_posix()
                )
                continue
            keep_dirs.append(name)
        dirnames[:] = keep_dirs
        for name in filenames:
            path = current / name
            rel = path.relative_to(staging_root).as_posix()
            if _path_is_reparse(path):
                problems.append(f"reparse in staged payload: {rel}")
                continue
            if path.is_file():
                found[rel] = path.read_bytes()
    for extra in sorted(set(found) - set(expected)):
        problems.append(f"unexpected staged file: {extra}")
    for missing in sorted(set(expected) - set(found)):
        problems.append(f"missing staged file: {missing}")
    for rel in sorted(set(expected) & set(found)):
        if found[rel] != expected[rel]:
            problems.append(f"staged bytes differ: {rel}")
    return problems


def _expected_for_skill(expected: dict[str, bytes], skill_name: str) -> dict[str, bytes]:
    """Slice *expected* paths down to one skill directory (relative keys)."""
    prefix = skill_name + "/"
    return {
        rel[len(prefix):]: data
        for rel, data in expected.items()
        if rel.startswith(prefix)
    }


def _skill_matches_expected(
    dest: Path, skill_name: str, expected: dict[str, bytes]
) -> bool:
    """True when *dest* exactly matches this skill's release bytes."""
    return not _staged_payload_problems(dest, _expected_for_skill(expected, skill_name))


def _installed_payload_problems(
    target: Path, skill_names: list[str], expected: dict[str, bytes]
) -> list[str]:
    """Compare installed skill trees against the release manifest."""
    problems: list[str] = []
    for name in skill_names:
        dest = target / name
        skill_expected = _expected_for_skill(expected, name)
        if not skill_expected:
            continue
        if not dest.exists() and not dest.is_symlink():
            problems.append(f"{name}/  (missing after install)")
            continue
        for item in _staged_payload_problems(dest, skill_expected):
            problems.append(f"{name}: {item}")
    return problems


def _run_release_validators(toplevel: Path) -> tuple[int, str]:
    """Run skill validators against *toplevel* before publication."""
    script_dir = Path(__file__).resolve().parent
    validators = [
        (script_dir / "check_skill_refs.py", ["--all", "--repo-root", str(toplevel)]),
        (
            script_dir / "check_skills_no_constants.py",
            ["--repo-root", str(toplevel)],
        ),
    ]
    missing = [path.name for path, _argv in validators if not path.exists()]
    if missing:
        return (
            EXIT_USAGE,
            "ERROR: missing release validator(s): " + ", ".join(missing),
        )
    failures: list[str] = []
    for script, argv in validators:
        try:
            result = subprocess.run(
                [sys.executable, str(script), *argv],
                cwd=str(toplevel),
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as exc:
            return EXIT_ERROR, f"ERROR: could not run {script.name}: {exc}"
        label = " ".join([script.name, *argv]).strip()
        if result.returncode != 0:
            detail = ((result.stdout or "") + (result.stderr or "")).strip()
            detail = detail or f"exit {result.returncode}"
            failures.append(f"{label} failed:\n{detail}")
    if failures:
        return (
            EXIT_POLICY,
            "REFUSED: release validators failed\n  " + "\n  ".join(failures),
        )
    return EXIT_OK, ""


def _backup_existing_skill(src: Path, dest: Path) -> None:
    _safe_replace(src, dest)


def _install_skill(staged: Path, dest: Path) -> None:
    _require_safe_tree(staged)
    _require_safe_io_path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        raise OSError(f"destination already exists: {dest}")
    os.replace(staged, dest)


def _restore_skill(
    backup: Path,
    dest: Path,
    *,
    installed_expected: dict[str, bytes] | None = None,
) -> None:
    """Restore *backup* over *dest*.

    When *installed_expected* is provided, refuse to delete *dest* unless it still
    matches those installed bytes — preserving concurrent target updates.
    """
    _require_safe_tree(backup)
    _require_safe_io_path(dest)
    if dest.exists() or dest.is_symlink():
        if installed_expected is not None:
            problems = _staged_payload_problems(dest, installed_expected)
            if problems:
                raise OSError(
                    f"destination changed since install; refusing to overwrite: {dest}"
                )
        _safe_rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    os.replace(backup, dest)


def _remove_created_skill(
    dest: Path,
    *,
    installed_expected: dict[str, bytes] | None = None,
) -> None:
    if dest.exists() or dest.is_symlink():
        if installed_expected is not None:
            problems = _staged_payload_problems(dest, installed_expected)
            if problems:
                raise OSError(
                    f"destination changed since install; refusing to remove: {dest}"
                )
        _safe_rmtree(dest)


def _validate_source_for_publish(
    repo_skills: Path, revision: str
) -> tuple[int, str, Path | None, str | None]:
    try:
        kind, toplevel, detail = _classify_checkout(repo_skills)
    except FileNotFoundError:
        return EXIT_USAGE, "ERROR: git is not available", None, None
    if kind == "unavailable_git":
        return EXIT_USAGE, f"ERROR: {detail}", None, None
    if kind == "no_git":
        return EXIT_USAGE, f"ERROR: {detail}: {repo_skills}", None, None
    if kind != "primary_main":
        return EXIT_POLICY, f"REFUSED: {detail}", toplevel, None
    try:
        sha = _resolve_revision(repo_skills, revision)
    except FileNotFoundError:
        return EXIT_USAGE, "ERROR: git is not available", toplevel, None
    if sha is None:
        return EXIT_USAGE, f"ERROR: cannot resolve revision {revision!r}", toplevel, None
    try:
        head = _head_sha(repo_skills)
    except FileNotFoundError:
        return EXIT_USAGE, "ERROR: git is not available", toplevel, None
    if head is None:
        return EXIT_USAGE, "ERROR: cannot resolve HEAD", toplevel, None
    if head != sha:
        return (
            EXIT_POLICY,
            f"REFUSED: HEAD {head} is not the requested release revision {sha}",
            toplevel,
            sha,
        )
    try:
        problems = _payload_problems(repo_skills, toplevel, sha)
    except FileNotFoundError:
        return EXIT_USAGE, "ERROR: git is not available", toplevel, sha
    if problems:
        return (
            EXIT_POLICY,
            "REFUSED: release skill tree is dirty "
            f"(modified/deleted/untracked payload):\n  " + "\n  ".join(problems),
            toplevel,
            sha,
        )
    return EXIT_OK, "", toplevel, sha


def _validate_target_for_publish(
    repo_skills: Path,
    toplevel: Path,
    target: Path,
) -> tuple[int, str]:
    if (
        _path_has_reparse_ancestor(repo_skills)
        or _path_is_reparse(repo_skills)
        or _any_reparse_in_tree(repo_skills)
    ):
        return EXIT_POLICY, "REFUSED: source path contains a symlink/junction/reparse point"
    if (
        _path_has_reparse_ancestor(target)
        or _path_is_reparse(target)
        or _any_reparse_in_tree(target)
    ):
        return EXIT_POLICY, "REFUSED: target path contains a symlink/junction/reparse point"
    if _paths_overlap(toplevel, target) or _paths_overlap(repo_skills, target):
        return EXIT_POLICY, "REFUSED: target overlaps the source checkout"
    if _inside_any_git_metadata(target):
        return EXIT_POLICY, "REFUSED: target is inside git metadata"
    return EXIT_OK, ""


def _publish(repo_skills: Path, revision: str, target: Path) -> int:
    rc, msg, toplevel, sha = _validate_source_for_publish(repo_skills, revision)
    if rc != EXIT_OK or toplevel is None or sha is None:
        print(msg, file=sys.stderr)
        return rc
    rc, msg = _run_release_validators(toplevel)
    if rc != EXIT_OK:
        print(msg, file=sys.stderr)
        return rc
    rc, msg = _validate_target_for_publish(repo_skills, toplevel, target)
    if rc != EXIT_OK:
        print(msg, file=sys.stderr)
        return rc

    created_target = not target.exists() and not target.is_symlink()
    token = uuid.uuid4().hex
    staging_root = target.parent / f".skill-release-stage-{token}"
    backup_root = target.parent / f".skill-release-backup-{token}"
    installed: list[tuple[str, bool]] = []
    preserve_recovery = False
    expected: dict[str, bytes] = {}
    skill_names: list[str] = []

    try:
        preflight = _target_snapshot(target)
        _require_safe_io_path(staging_root)
        _require_safe_io_path(backup_root)
        _stage_release_payload(repo_skills, sha, staging_root)
        expected = _revision_payload_manifest(repo_skills, sha)
        staged_problems = _staged_payload_problems(staging_root, expected)
        if staged_problems:
            print(
                "REFUSED: staged payload does not match the named revision\n  "
                + "\n  ".join(staged_problems),
                file=sys.stderr,
            )
            return EXIT_POLICY
        rc, msg, _, sha_again = _validate_source_for_publish(repo_skills, sha)
        if rc != EXIT_OK or sha_again != sha:
            print(
                "REFUSED: source identity or payload changed during preparation",
                file=sys.stderr,
            )
            if msg:
                print(msg, file=sys.stderr)
            return rc if rc != EXIT_OK else EXIT_POLICY
        rc, msg = _run_release_validators(toplevel)
        if rc != EXIT_OK:
            print(msg, file=sys.stderr)
            return rc
        if _target_snapshot(target) != preflight:
            print(
                "ERROR: target changed during staging; leaving existing skills in place",
                file=sys.stderr,
            )
            return EXIT_ERROR
        rc, msg = _validate_target_for_publish(repo_skills, toplevel, target)
        if rc != EXIT_OK:
            print(msg, file=sys.stderr)
            return rc
        skill_names = sorted(
            {Path(rel).parts[0] for rel in expected if len(Path(rel).parts) > 1}
        )
        backup_root.mkdir(parents=True, exist_ok=True)
        backed_up: list[str] = []
        for name in skill_names:
            dest = target / name
            if dest.exists():
                _backup_existing_skill(dest, backup_root / name)
                backed_up.append(name)
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
        try:
            for name in skill_names:
                dest = target / name
                had_predecessor = name in backed_up
                _install_skill(staging_root / name, dest)
                installed.append((name, had_predecessor))
        except OSError as exc:
            print(f"ERROR: install failed: {exc}", file=sys.stderr)
            rollback_ok = True
            already = {name for name, _had in installed}
            restore_order = list(reversed(installed))
            for name in reversed(backed_up):
                if name not in already:
                    restore_order.append((name, True))
            for name, had_predecessor in restore_order:
                dest = target / name
                skill_expected = _expected_for_skill(expected, name)
                try:
                    if had_predecessor:
                        _restore_skill(
                            backup_root / name,
                            dest,
                            installed_expected=skill_expected,
                        )
                    else:
                        _remove_created_skill(
                            dest, installed_expected=skill_expected
                        )
                except OSError as restore_exc:
                    rollback_ok = False
                    preserve_recovery = True
                    print(
                        f"ERROR: rollback failed for {dest}: {restore_exc}",
                        file=sys.stderr,
                    )
            leftover_new = [
                name for name, had in installed if not had and (target / name).exists()
            ]
            if rollback_ok and leftover_new:
                try:
                    for name in leftover_new:
                        _remove_created_skill(
                            target / name,
                            installed_expected=_expected_for_skill(expected, name),
                        )
                except OSError as leftover_exc:
                    rollback_ok = False
                    preserve_recovery = True
                    print(
                        f"ERROR: refused unsafe leftover cleanup: {leftover_exc}",
                        file=sys.stderr,
                    )
            if rollback_ok:
                if created_target and target.exists():
                    remaining = [
                        p for p in target.iterdir()
                        if not p.name.startswith(".skill-release-")
                    ]
                    if not remaining:
                        try:
                            _safe_rmtree(target)
                        except OSError as cleanup_exc:
                            rollback_ok = False
                            preserve_recovery = True
                            print(
                                f"ERROR: refused unsafe target cleanup: {cleanup_exc}",
                                file=sys.stderr,
                            )
                if rollback_ok:
                    print(
                        f"ERROR: release rolled back. backup={backup_root} staging={staging_root}",
                        file=sys.stderr,
                    )
                    return EXIT_ERROR
            print(
                "ERROR: rollback failed; target was modified and the release "
                "did not complete. Manual recovery is required.\n"
                f"  target={target}\n"
                f"  staging={staging_root}\n"
                f"  backup={backup_root}",
                file=sys.stderr,
            )
            return EXIT_ERROR

        installed_problems = _installed_payload_problems(
            target, skill_names, expected
        )
        if installed_problems:
            preserve_recovery = True
            print(
                "ERROR: installed skills do not match the reviewed revision; "
                "release incomplete. Manual recovery is required.\n  "
                + "\n  ".join(installed_problems)
                + f"\n  target={target}\n  staging={staging_root}\n  backup={backup_root}",
                file=sys.stderr,
            )
            return EXIT_ERROR
    except OSError as exc:
        print(f"ERROR: preparation/backup failed: {exc}", file=sys.stderr)
        restore_failed = False
        if backup_root.exists():
            for child in backup_root.iterdir():
                dest = target / child.name
                if not dest.exists() and child.exists():
                    try:
                        _safe_replace(child, dest)
                    except OSError as restore_exc:
                        restore_failed = True
                        preserve_recovery = True
                        print(
                            f"ERROR: could not restore {child} after backup failure: "
                            f"{restore_exc}",
                            file=sys.stderr,
                        )
        if restore_failed or (
            backup_root.exists() and any(backup_root.iterdir())
        ):
            preserve_recovery = True
        print(
            "ERROR: backup-failure recovery incomplete; recovery material preserved.\n"
            f"  target={target}\n"
            f"  staging={staging_root}\n"
            f"  backup={backup_root}",
            file=sys.stderr,
        )
        return EXIT_ERROR
    else:
        print(
            f"Released {len(installed)} skill(s) revision={sha} -> {target} "
            f"(explicit release; backup {backup_root})"
        )
        return EXIT_OK
    finally:
        # Successful releases and clean rollbacks drop the stage directory.
        # Incomplete recovery keeps it beside the retained backup.
        if staging_root.exists() and not preserve_recovery:
            _safe_rmtree(staging_root, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="report repo-vs-deployed drift; no writes")
    parser.add_argument("--target", default=None,
                        help="sole destination (required for publication)")
    parser.add_argument("--revision", default=None,
                        help="commit-ish to publish (required for publication)")
    parser.add_argument("--repo-skills", type=Path, default=REPO_SKILLS,
                        help="in-repo skills dir (default: .claude/skills)")
    parser.add_argument("--force", action="store_true",
                        help="legacy flag; never bypasses release checks")
    args = parser.parse_args(argv)

    repo_skills_raw = Path(args.repo_skills)
    if _path_has_reparse_ancestor(repo_skills_raw) or _path_is_reparse(repo_skills_raw):
        print(
            "REFUSED: source path contains a symlink/junction/reparse point",
            file=sys.stderr,
        )
        return EXIT_POLICY
    if not repo_skills_raw.is_dir():
        print(f"ERROR: repo skills dir missing: {repo_skills_raw}", file=sys.stderr)
        return EXIT_USAGE
    repo_skills = repo_skills_raw.resolve()

    if args.check:
        targets = [t.resolve() for t in resolve_targets(args.target)]
        any_drift = False
        for target in targets:
            if not target.exists():
                print(f"DRIFT: deploy target does not exist: {target}")
                any_drift = True
                continue
            drift = check_drift(repo_skills, target)
            if drift:
                print(
                    f"DRIFT ({len(drift)} file(s)) repo={repo_skills} "
                    f"target={target}:"
                )
                for d in drift:
                    print(f"  {d}")
                any_drift = True
            else:
                print(f"OK: deployed bundle matches repo ({target}).")
        return EXIT_ERROR if any_drift else EXIT_OK

    if args.force:
        print(
            "ERROR: --force does not bypass release checks. Publication "
            "requires an explicit reviewed --revision and --target.",
            file=sys.stderr,
        )

    if not args.revision or not args.target:
        missing = []
        if not args.revision:
            missing.append("--revision")
        if not args.target:
            missing.append("--target")
        print(
            "ERROR: publication requires "
            + " and ".join(missing)
            + ". No AppData or home destination is selected implicitly.",
            file=sys.stderr,
        )
        return EXIT_USAGE

    target_raw = Path(args.target)
    if _path_has_reparse_ancestor(target_raw) or _path_is_reparse(target_raw):
        print(
            "REFUSED: target path contains a symlink/junction/reparse point",
            file=sys.stderr,
        )
        return EXIT_POLICY
    if _inside_any_git_metadata(target_raw):
        print("REFUSED: target is inside git metadata", file=sys.stderr)
        return EXIT_POLICY
    return _publish(repo_skills, args.revision, target_raw)


if __name__ == "__main__":
    sys.exit(main())
