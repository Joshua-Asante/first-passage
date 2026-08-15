#!/usr/bin/env python3
"""check_skill_refs.py — path-reference linter for `.claude/skills/*/SKILL.md`.

Every repo-relative path a skill cites should resolve. This catches the most
common form of skill rot: a doc/code path referenced in a skill that has since
moved or been deleted. Installed in the pre-commit gate per ADR
`docs/adr/2026-06-04-methodology-skills-under-vc.md` §2.4 (cheapest-first
check #1).

Convention (deliberately conservative — under-flag rather than false-positive):

Fenced code blocks (```` ``` ````) are stripped before extraction — they hold
command examples and template bodies, not navigable references. A token is then
extracted from markdown links (`[text](target)`) and inline code spans
(`` `token` ``). It is treated as a *candidate repo path* only when ALL of the
following hold:

  - it contains `/`
  - it is not a URL (`http://`, `https://`, `mailto:`) and not a bare `#anchor`
  - it is not a bare directory (does not end in `/`) — a skill naming a target
    *directory* ("artifacts live in `docs/briefs/`") is not asserting a file
  - it contains no shell-argument whitespace and no template placeholder
    (`<...>`, `{...}`, `[...]`, bare `...`, `YYYY`, `MM`, `DD`, `NNN`, `*`,
    or a lone uppercase variable segment such as `Q-X-name`)
  - it EITHER starts with a known top-level repo dir  OR  ends in a known repo
    extension (`.py .md .toml .pine .json .yml .yaml .sh .bat .csv`).

A candidate is RESOLVED against both the repo root and the skill's own dir (so
`references/foo.md` resolves skill-relative, `docs/adr/x.md` resolves
repo-relative, `../../../docs/...` relative links resolve too). Trailing `:N`
line citations (`docs/adr/foo.md:52`) are stripped before resolve.

A candidate is HARD-FAILED only when it (a) starts with one of the
REPO-NAVIGATION dirs (`docs/`, `config/`, `data/`, `tests/`, `.claude/`,
`archive/`, `analysis/`, `strategies/`, `ops/`, `core/`, `lab/`, `scripts/`),
(b) is NOT under a gitignored vendor-data subtree (`data/tv_exports/`,
`data/bar_data/`, `data/external/`, and the monorepo `core/data/` equivalents —
absent on CI / fresh clones per the public-clone posture), (c) is NOT matched
by a repo-root `.gitignore` rule (e.g. `**/*.pine` — cited correctly, bytes
intentionally absent), (d) is NOT marked as a deliberate tombstone (inline
`` `path` (deleted) `` / `` `path` (retired) ``), and (e) resolves nowhere.
The (a)∧¬(b)∧¬(c)∧¬(d) refs are links *into the wider repo* and must stay live.

Three reference classes are intentionally NOT hard-failed (resolved-and-OK when
present, ignored when absent):
  - skill *bundled-asset* refs under `references/` — these are a skill's
    forward-looking contract for assets it ships or promises; a missing
    bundled template is the skill's own gap (e.g. brief-authoring's not-yet-
    authored `references/adr.md`, surfaced by ADR 2026-06-04 §0), not repo rot.
  - `.claude/*.local.md` install-destination refs — `.gitignore` (line ~51)
    already marks this exact glob "machine-local by convention; not shared
    via git", so a skill's "Install surfaces" table citing its own not-yet-
    installed local copy (e.g. blast-radius's
    `.claude/hookify.blast-radius.local.md`) is describing a per-clone
    install step, not a dead repo path — same rationale as the vendor-data
    exemption below, different gitignore rule (2026-08-05).
  - other extension-only tokens not under a repo-nav dir (e.g. a legacy
    `prop_firm_pipeline/dd_protection.py` mention) — too ambiguous to fail on.

Note: `scripts/` is dual-homed. A skill-local `scripts/foo.py` that resolves
under the skill directory passes; a missing `scripts/foo.py` is treated as a
repo-nav hit into the discipline-scripts tree and hard-fails (Algorithm
gate-estate repair 2026-07-24). Promise a not-yet-authored skill script via
`references/` or land the file before citing it.

`references/*.md` files under each skill are scanned with the same extraction
rules but WARN-only (first release) — hard-fail stays SKILL.md-only.

Inline code is checked, but a token containing a space (a command with args,
e.g. `scripts/reconcile.py --baseline`) is skipped — such tokens are not pure
paths and matching them produces false positives on tool-invocation examples.

Modes / exit codes:
  --all              check every skill under .claude/skills/      (default scope)
  --skill <name>     check a single skill
  0 — all cited paths resolve (WARN-only findings do not fail)
  1 — one or more unresolved refs (each printed with its skill)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_SUBDIR = (".claude", "skills")

# Dirs that represent navigation into the wider repo — links here must stay live.
REPO_NAV_DIRS = (
    "docs/", "config/", "data/",
    "tests/", ".claude/", "archive/", "analysis/", "strategies/",
    "ops/", "core/", "lab/", "scripts/",
)
# Gitignored vendor-data subtrees (public-clone posture, see CLAUDE.md): the CSVs
# under these are not tracked and are absent on CI / fresh clones, so a skill
# citing one as an example must not hard-fail — mirrors validate_params.py
# treating absent Pine as WARN-only. Include both pre-monorepo `data/` and
# post-move `core/data/` prefixes.
VENDOR_DATA_PREFIXES = (
    "data/tv_exports/", "data/bar_data/", "data/external/",
    "core/data/tv_exports/", "core/data/bar_data/", "core/data/external/",
)
# Per-clone Claude-local install destinations — `.gitignore` pattern
# `.claude/*.local.md` ("machine-local by convention; not shared via git").
# A skill's Install-surfaces table citing its own local-copy destination
# (not the `references/*.local.md` template it ships, which already resolves
# under SKILL_ASSET_DIRS) is a per-clone install step, not a dead repo path.
LOCAL_INSTALL_PREFIX = ".claude/"
LOCAL_INSTALL_SUFFIX = ".local.md"
# Skill bundled-asset prefixes — `references/` is never hard-failed when absent.
# `scripts/` is also recognised as a candidate prefix (skill-relative resolve
# still passes) but missing scripts/ hits hard-fail as repo-nav (see docstring).
SKILL_ASSET_DIRS = ("references/", "scripts/")
KNOWN_TOP_DIRS = REPO_NAV_DIRS + SKILL_ASSET_DIRS
KNOWN_EXTS = (
    ".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
    ".sh", ".bat", ".csv",
)

# Markdown link target: [text](target)
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# Inline code span: `token`
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
# Fenced code block: ```...```  (stripped before extraction)
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
# Template placeholder markers that mean "this is a pattern, not a real path".
#  <...> / {...} / [...] / bare ... / date tokens / NNN / glob *  AND a lone
#  uppercase variable segment used as a stand-in (e.g. the `X` in
#  `docs/briefs/Q-X-name.md`). Bracketed `[...]` tokens are templates
#  (e.g. `data/mc/[panel-name].csv`), not character-class globs.
_PLACEHOLDER_RE = re.compile(
    r"<[^>]*>|\{[^}]*\}|\[[^\]]+\]|\.\.\.|YYYY|MM\b|DD\b|NNN|\*"
    r"|(?<![A-Za-z])X(?![A-Za-z])"
)
# Glob metacharacters — a glob is an assertion (at least one match).
# `*` / `?` only: `[` is reserved for template placeholders above.
# Discarding globs as placeholders let skills cite trees that moved
# (e.g. core/strategies/*/LOCK.md → _archive/) while the gate stayed green.
_GLOB_RE = re.compile(r"[*?]")
# Brace tokens remain discarded by _PLACEHOLDER_RE; Path.glob does not
# expand braces — accept that gap explicitly (pre-expand or leave discarded).
# Trailing `:N` line citation (e.g. `docs/adr/foo.md:52`) — strip before resolve.
_LINE_SUFFIX_RE = re.compile(r":\d+$")
# Deliberate tombstone: `path` (deleted) / `path` (retired) adjacent to the span.
_TOMBSTONE_INLINE_RE_TMPL = r"`{token}`\s*\((?:deleted|retired)\)"
_TOMBSTONE_LINK_RE_TMPL = (
    r"\[[^\]]*\]\({token}(?:#[^)\s]*)?(?:\s+\"[^\"]*\")?\)\s*\((?:deleted|retired)\)"
)


def _strip_link_target(target: str) -> str:
    """A markdown link target may be `path#anchor` or `path "title"` — keep path."""
    target = target.strip()
    # Drop an optional title:  (path "Title")
    if " " in target:
        target = target.split(" ", 1)[0]
    # Drop a trailing #anchor
    if "#" in target:
        target = target.split("#", 1)[0]
    return _strip_line_suffix(target.strip())


def _strip_line_suffix(token: str) -> str:
    """Drop a trailing `:N` line citation (`docs/adr/foo.md:52` → `…/foo.md`)."""
    return _LINE_SUFFIX_RE.sub("", token)


def _is_url_or_anchor(token: str) -> bool:
    t = token.strip()
    if t.startswith("#"):
        return True
    lower = t.lower()
    return lower.startswith(("http://", "https://", "mailto:"))


def _is_template_placeholder(token: str) -> bool:
    """True for pattern tokens (`[…]`, `<…>`, `{…}`, bare `…`, date/NNN stands-in)."""
    return _PLACEHOLDER_RE.search(token) is not None


def _is_candidate_path(token: str) -> bool:
    if "/" not in token:
        return False
    if _is_url_or_anchor(token):
        return False
    if token.endswith("/"):
        # Bare directory reference — not a file assertion.
        return False
    # Template placeholders (incl. `[panel-name]`, `data/...`) before glob
    # treatment — bracket tokens are templates, not character-class globs.
    if _is_template_placeholder(token):
        # Exception: REPO_NAV globs that use only * / ? (no bracket templates)
        # still qualify — but _PLACEHOLDER_RE matches `*`, so re-check for a
        # pure glob assertion (claim-alignment S-22).
        if token.startswith(REPO_NAV_DIRS) and _GLOB_RE.search(token):
            # A token with both `*` and `[strategy]` is a template, not a glob.
            if re.search(r"\[[^\]]+\]", token) or "..." in token:
                return False
            if re.search(r"<[^>]*>|\{[^}]*\}", token):
                return False
            return True
        return False
    if token.startswith(KNOWN_TOP_DIRS):
        return True
    return token.endswith(KNOWN_EXTS)


def _vendor_parent_exists(repo_root: Path, token: str) -> bool:
    """Waive vendor-data tokens only when the parent directory exists.

    Live gitignored trees (e.g. core/data/tv_exports/cme/) stay waived;
    retired feed parents (e.g. core/data/tv_exports/pepperstone/) hard-fail.
    """
    for prefix in VENDOR_DATA_PREFIXES:
        if token.startswith(prefix):
            parent = (repo_root / token).parent
            return parent.is_dir()
    return False


@lru_cache(maxsize=4)
def _gitignore_patterns(repo_root_str: str) -> tuple[str, ...]:
    """Load non-comment `.gitignore` lines (repo-root file only; no nested)."""
    path = Path(repo_root_str) / ".gitignore"
    if not path.is_file():
        return ()
    out: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        out.append(raw)
    return tuple(out)


def _pattern_matches_path(pattern: str, path: str) -> bool:
    """Match one gitignore-style pattern against a repo-relative posix path."""
    if pattern.startswith("!"):
        # Negations handled by the caller (last-match wins); bare check here.
        pattern = pattern[1:]
    dir_only = pattern.endswith("/")
    pattern = pattern.rstrip("/")
    if pattern.startswith("/"):
        pattern = pattern[1:]
    p = PurePosixPath(path)
    # Basename-only patterns match in any directory.
    if "/" not in pattern:
        if p.match(pattern) or p.match(f"**/{pattern}"):
            return True
        if dir_only and any(part == pattern for part in p.parts[:-1]):
            return True
        return False
    if p.match(pattern):
        return True
    if dir_only:
        # Directory prefix: `foo/bar/` matches `foo/bar/baz.txt`.
        return path == pattern or path.startswith(pattern + "/")
    return False


def _is_gitignored_via_patterns(repo_root: Path, token: str) -> bool:
    """Fall back when `git check-ignore` is unavailable — read `.gitignore`."""
    ignored = False
    for pattern in _gitignore_patterns(str(repo_root.resolve())):
        negated = pattern.startswith("!")
        if _pattern_matches_path(pattern, token):
            ignored = not negated
    return ignored


def _is_gitignored(repo_root: Path, token: str) -> bool:
    """True when token matches a repo-root `.gitignore` rule.

    Prefers `git check-ignore` (honours git's grammar exactly). Falls back to
    reading `.gitignore` + pathlib matching when git is absent (unit fixtures).
    Intentionally absent files that are gitignored by design (e.g. `**/*.pine`)
    must not warn — the citation is correct; the bytes are private.
    """
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", token],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return True
        if result.returncode == 1:
            return False
        # 128 = not a git repo / other error → fall through to file parse.
    except (OSError, subprocess.SubprocessError):
        pass
    return _is_gitignored_via_patterns(repo_root, token)


def _glob_cites_no_path(repo_root: Path, token: str) -> bool:
    """True when token is a REPO_NAV glob with zero Path.glob matches."""
    if not (token.startswith(REPO_NAV_DIRS) and _GLOB_RE.search(token)):
        return False
    # Brace / bracket templates: still discarded upstream; if one reaches here,
    # do not pretend Path.glob expands them.
    if "{" in token or "}" in token or "[" in token:
        return False
    return not any(repo_root.glob(token))


def _hard_failable(repo_root: Path, token: str) -> bool:
    """True only for links into the wider repo (REPO_NAV_DIRS), excluding
    gitignored vendor-data whose **parent directory still exists**, and
    excluding skill-bundled `references/` promises."""
    if token.startswith(VENDOR_DATA_PREFIXES):
        return not _vendor_parent_exists(repo_root, token)
    # references/ stays a non-hard-fail bundled-asset contract even though
    # scripts/ is now dual-homed into REPO_NAV_DIRS.
    if token.startswith("references/"):
        return False
    if token.startswith(LOCAL_INSTALL_PREFIX) and token.endswith(LOCAL_INSTALL_SUFFIX):
        return False
    return token.startswith(REPO_NAV_DIRS)


def _is_tombstoned(text: str, token: str) -> bool:
    """True if any occurrence of token is marked (deleted)/(retired) adjacent."""
    escaped = re.escape(token)
    inline = re.compile(_TOMBSTONE_INLINE_RE_TMPL.format(token=escaped))
    link = re.compile(_TOMBSTONE_LINK_RE_TMPL.format(token=escaped))
    return inline.search(text) is not None or link.search(text) is not None


def _extract_candidates(text: str) -> list[str]:
    """Return candidate path tokens from markdown links + inline code spans.

    Fenced code blocks are stripped first (command examples / template bodies).
    """
    text = _FENCE_RE.sub("\n", text)
    candidates: list[str] = []

    for m in _MD_LINK_RE.finditer(text):
        target = _strip_link_target(m.group(1))
        if _is_candidate_path(target):
            candidates.append(target)

    for m in _INLINE_CODE_RE.finditer(text):
        token = m.group(1).strip()
        # Skip tool-invocation examples (command with args) — not a pure path.
        if " " in token:
            continue
        # An inline path may still carry a trailing #anchor.
        if "#" in token and not token.startswith("#"):
            token = token.split("#", 1)[0]
        token = _strip_line_suffix(token)
        if _is_candidate_path(token):
            candidates.append(token)

    return candidates


def _resolves(repo_root: Path, skill_dir: Path, token: str) -> bool:
    """True if token resolves under repo root OR the skill's own directory."""
    # Glob assertion: at least one match under repo root.
    if token.startswith(REPO_NAV_DIRS) and _GLOB_RE.search(token):
        if "{" in token or "}" in token or "[" in token:
            return False
        return any(repo_root.glob(token))
    # Repo-root resolution.
    p = (repo_root / token).resolve()
    try:
        if p.exists():
            return True
    except OSError:
        pass
    # Skill-relative resolution (handles `references/foo.md` and `../../x`).
    p2 = (skill_dir / token).resolve()
    try:
        if p2.exists():
            return True
    except OSError:
        pass
    return False


def check_skill(repo_root: Path, skill_name: str) -> list[tuple[str, str]]:
    """Return list of (skill_name, dead_ref) for one skill's SKILL.md."""
    skills_root = repo_root.joinpath(*SKILLS_SUBDIR)
    skill_dir = skills_root / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    dead: list[tuple[str, str]] = []
    seen: set[str] = set()
    for token in _extract_candidates(text):
        if token in seen:
            continue
        seen.add(token)
        if not _hard_failable(repo_root, token):
            # Bundled references/ / ambiguous extension-only ref: never hard-fail.
            continue
        if _glob_cites_no_path(repo_root, token):
            dead.append((skill_name, f"glob cites no existing path: {token}"))
            continue
        if _resolves(repo_root, skill_dir, token):
            continue
        if _is_tombstoned(text, token):
            continue
        if _is_gitignored(repo_root, token):
            continue
        dead.append((skill_name, token))
    return dead


def check_skill_references_warn(
    repo_root: Path, skill_name: str,
) -> list[tuple[str, str, str]]:
    """WARN-only scan of skill `references/*.md`.

    Returns list of (skill_name, rel_md_path, dead_ref). Never contributes to
    hard-fail exit codes — inventory for a later hard-fail flip.
    """
    skills_root = repo_root.joinpath(*SKILLS_SUBDIR)
    skill_dir = skills_root / skill_name
    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        return []
    warnings: list[tuple[str, str, str]] = []
    for md in sorted(refs_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        seen: set[str] = set()
        for token in _extract_candidates(text):
            if token in seen:
                continue
            seen.add(token)
            if not _hard_failable(repo_root, token):
                continue
            if _glob_cites_no_path(repo_root, token):
                rel = md.relative_to(skill_dir).as_posix()
                warnings.append(
                    (skill_name, rel, f"glob cites no existing path: {token}")
                )
                continue
            if _resolves(repo_root, skill_dir, token):
                continue
            if _is_tombstoned(text, token):
                continue
            if _is_gitignored(repo_root, token):
                continue
            rel = md.relative_to(skill_dir).as_posix()
            warnings.append((skill_name, rel, token))
    return warnings


def _all_skill_names(repo_root: Path) -> list[str]:
    skills_root = repo_root.joinpath(*SKILLS_SUBDIR)
    if not skills_root.is_dir():
        return []
    return sorted(
        d.name for d in skills_root.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )


def check_all(repo_root: Path) -> list[tuple[str, str]]:
    """Return list of (skill_name, dead_ref) across every skill."""
    dead: list[tuple[str, str]] = []
    for name in _all_skill_names(repo_root):
        dead.extend(check_skill(repo_root, name))
    return dead


def check_all_references_warn(
    repo_root: Path,
) -> list[tuple[str, str, str]]:
    warnings: list[tuple[str, str, str]] = []
    for name in _all_skill_names(repo_root):
        warnings.extend(check_skill_references_warn(repo_root, name))
    return warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true",
                       help="check every skill under .claude/skills/")
    group.add_argument("--skill", help="check a single skill by directory name")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT,
                        help="repo root for path resolution (default: this repo)")
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()

    if args.all:
        dead = check_all(repo_root)
        warns = check_all_references_warn(repo_root)
    else:
        dead = check_skill(repo_root, args.skill)
        warns = check_skill_references_warn(repo_root, args.skill)

    if warns:
        print("WARN: unresolved repo-path references in skill references/*.md "
              "(report-only; does not fail the gate):", file=sys.stderr)
        for skill_name, rel, ref in warns:
            print(f"  [{skill_name}/{rel}] {ref}", file=sys.stderr)
        print(f"\n{len(warns)} warn-only reference(s).", file=sys.stderr)

    if dead:
        print("Unresolved repo-path references in skills:")
        for skill_name, ref in dead:
            print(f"  [{skill_name}] {ref}")
        print(f"\n{len(dead)} unresolved reference(s).")
        return 1

    scope = "all skills" if args.all else f"skill {args.skill!r}"
    print(f"OK: every cited repo path resolves ({scope}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
