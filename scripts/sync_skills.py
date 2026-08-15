#!/usr/bin/env python3
"""sync_skills.py — one-way deploy of in-repo skills to the deployed bundle(s).

ONE-WAY CONTRACT (ADR docs/adr/2026-06-04-methodology-skills-under-vc.md §2.2):
the repo is the single source of truth. Skills flow repo -> deployed ONLY.
This script never copies deployed -> repo. Edits happen in-repo, pass the gate
(`check_skill_refs.py`, `check_skills_no_constants.py`), then deploy via this script.

CAVEAT (load-bearing — per project memory): the AppData default deploy target is
a cloud-synced location (AppData/.../skills-plugin/...). Raw on-disk writes there
can be overwritten by cloud sync, so the one-way contract cannot be fully
*enforced* from this script — it is a convention this tool implements but the
sync layer can still clobber. Treat `--check` drift as advisory when the target
is the cloud-synced path.

Deploy target resolution (default mode / --check with no --target):
  Primary slot:
    1. --target <path>           (explicit — sole destination; skips the home add-on)
    2. $SKILLS_DEPLOY_TARGET      (env override for the primary slot)
    3. DEFAULT_DEPLOY_TARGET      (built-in cloud-synced AppData skills dir)
  Additional default slot (when --target is not set):
    HOME_SKILLS_DEPLOY_TARGET = ~/.claude/skills/
    — the bundle Claude Code sessions actually load. Measured 2026-08-08 as a
      third, unsynced copy; now a first-class default destination so
      `make sync-skills` / the PostToolUse hook cannot leave it stale while
      AppData is green. Deduped if it coincides with the primary.

Modes:
  (default)   copy in-repo .claude/skills/<skill> -> each resolved target/<skill>
  --check     compare only; exit non-zero on any repo-vs-deployed divergence
              across all resolved targets, printing each diverging file. No writes.
  --force     allow deploying from a `.claude/worktrees/` checkout (normally
              refused — worktree branch state must not clobber the live bundle)

--check ALSO flags whole deployed directories that have no repo counterpart at
all ("extras") — this is distinct from diff_skill's per-file "extra in
deployed", which only fires for a skill that already shares a name with a repo
dir. An extra deployed-only directory means one of three things: (a) a stock
skill bundled with Claude Code/Cowork itself (not a project skill — expected
to live only in the deployed bundle) — add it to STOCK_SKILLS_EXEMPT below and
it stops being flagged; (b) a project skill authored directly in the bundle
that never went through the repo (import it — see import_skill_from_cache.py,
the exact defect class ADR docs/adr/2026-06-04-methodology-skills-under-vc.md
closed); or (c) a stale directory to delete. Deliberately NOT auto-exempted:
resolving (b)/(c) requires a human decision, so an unrecognized extra keeps
`--check` red until triaged.

Exit codes:
  0 — copy succeeded / no drift
  1 — drift detected (--check) OR copy error
  2 — repo source dir missing
  3 — refused: source is inside .claude/worktrees/ (re-run with --force)
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_SKILLS = REPO_ROOT / ".claude" / "skills"

# Built-in default deploy target (cloud-synced; see CAVEAT in module docstring).
DEFAULT_DEPLOY_TARGET = Path(
    os.path.expandvars(
        r"%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin"
        r"\72fdf38f-9be5-43cc-9803-8e04bfac2290"
        r"\4a461c5e-0034-4ec3-8928-8324158d1365\skills"
    )
)

# Second default destination — the user-level bundle Claude Code loads.
# Path.home() so Windows (C:\\Users\\…\\.claude\\skills) and POSIX share one form.
HOME_SKILLS_DEPLOY_TARGET = Path.home() / ".claude" / "skills"

# Deployed-only top-level directories confirmed to be stock skills bundled with
# Claude Code/Cowork itself (not authored in this repo, not project skills) —
# `--check` does not flag these as "extra in deployed". Triaged 2026-07-06
# (skills-sync extras check): `notion-mcp-api-patterns` was NOT added here —
# it is a Joshua-authored project skill that only ever lived in the bundle
# (see docs/adr/2026-06-04-methodology-skills-under-vc.md §1), so it stays
# flagged until imported via import_skill_from_cache.py, not exempted.
STOCK_SKILLS_EXEMPT = frozenset({
    "consolidate-memory",
    "docx",
    "pdf",
    "pptx",
    "schedule",
    "setup-cowork",
    "skill-creator",
    "xlsx",
})


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
    """All destinations for deploy / --check.

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
        # Unresolvable primary (e.g. literal %APPDATA% on non-Windows) — still
        # include home so the loadable bundle is covered.
        targets.append(home)
    return targets


def _iter_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file()]


def diff_skill(repo_skill: Path, deployed_skill: Path) -> list[str]:
    """Return relative paths that diverge (missing or differing) for one skill."""
    diverging: list[str] = []
    for f in _iter_files(repo_skill):
        rel = f.relative_to(repo_skill).as_posix()
        target_f = deployed_skill / f.relative_to(repo_skill)
        if not target_f.exists():
            diverging.append(f"{repo_skill.name}/{rel}  (missing in deployed)")
        elif not filecmp.cmp(f, target_f, shallow=False):
            diverging.append(f"{repo_skill.name}/{rel}  (content differs)")
    # Files present in deployed but not in repo are also divergence.
    if deployed_skill.is_dir():
        for f in _iter_files(deployed_skill):
            rel = f.relative_to(deployed_skill)
            if not (repo_skill / rel).exists():
                diverging.append(
                    f"{repo_skill.name}/{rel.as_posix()}  (extra in deployed)")
    return diverging


def find_extra_deployed_skills(repo_skills: Path, target: Path) -> list[str]:
    """Whole deployed directories with no repo counterpart at all.

    Distinct from diff_skill's per-file "extra in deployed", which only
    considers skills that already share a name with a repo dir. Stock skills
    in STOCK_SKILLS_EXEMPT are not flagged; everything else is either an
    unimported project skill or a stale directory — a human call, so it stays
    flagged rather than being silently exempted.
    """
    if not target.is_dir():
        return []
    repo_names = {p.name for p in repo_skills.iterdir() if p.is_dir()}
    extras: list[str] = []
    for d in sorted(p for p in target.iterdir() if p.is_dir()):
        if d.name in repo_names or d.name in STOCK_SKILLS_EXEMPT:
            continue
        extras.append(
            f"{d.name}  (extra top-level skill in deployed, no repo copy — import or delete)"
        )
    return extras


def check_drift(repo_skills: Path, target: Path) -> list[str]:
    """Compare every in-repo skill against the deploy target. Returns drift list."""
    drift: list[str] = []
    for skill_dir in sorted(p for p in repo_skills.iterdir() if p.is_dir()):
        drift.extend(diff_skill(skill_dir, target / skill_dir.name))
    drift.extend(find_extra_deployed_skills(repo_skills, target))
    return drift


def copy_skills(repo_skills: Path, target: Path) -> int:
    """Copy every in-repo skill into the target (repo -> deployed). Returns count."""
    target.mkdir(parents=True, exist_ok=True)
    n = 0
    for skill_dir in sorted(p for p in repo_skills.iterdir() if p.is_dir()):
        dst = target / skill_dir.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill_dir, dst)
        n += 1
    return n


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="report repo-vs-deployed drift; no writes")
    parser.add_argument("--target", default=None,
                        help="sole deploy target (overrides defaults; skips home add-on)")
    parser.add_argument("--repo-skills", type=Path, default=REPO_SKILLS,
                        help="in-repo skills dir (default: .claude/skills)")
    parser.add_argument("--force", action="store_true",
                        help="deploy even when the source is a .claude/worktrees checkout")
    args = parser.parse_args(argv)

    repo_skills = args.repo_skills.resolve()
    if not repo_skills.is_dir():
        print(f"ERROR: repo skills dir missing: {repo_skills}", file=sys.stderr)
        return 2

    targets = [t.resolve() for t in resolve_targets(args.target)]

    if args.check:
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
        return 1 if any_drift else 0

    # Default: one-way copy repo -> each deployed target. Refuse when the
    # source is a worktree checkout — uncommitted branch state must not
    # clobber the shared live bundle (--check above stays allowed: read-only).
    if is_under_worktrees(repo_skills) and not args.force:
        print(
            f"REFUSED: source {repo_skills} is inside .claude/worktrees/ — "
            "deploying worktree branch state would clobber the live bundle. "
            "Deploy from the main checkout, or re-run with --force.",
            file=sys.stderr,
        )
        return 3
    for target in targets:
        try:
            n = copy_skills(repo_skills, target)
        except OSError as e:
            print(f"ERROR copying skills to {target}: {e}", file=sys.stderr)
            return 1
        print(
            f"Deployed {n} skill(s) repo -> {target} "
            "(one-way; repo is source of truth)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
