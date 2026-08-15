#!/usr/bin/env python3
"""import_skill_from_cache.py — ONE-TIME seed of a skill from the deployed bundle.

Recovery path for exactly one failure shape: a skill whose ONLY copy lives in
the deployed (evictable, cloud-synced) bundle because it was authored there
directly and never went through the repo authoring path. ADR
`docs/adr/2026-06-04-methodology-skills-under-vc.md` §2.1 made
`.claude/skills/` canonical, but a skill created in the bundle *after* that
migration (e.g. `strategy-validation`, ~2026-06-11) has no repo copy at all —
so the de-facto canonical source is an evictable cache (data-loss exposure).
Worse, any non-byte-true repo copy is a clobber hazard: `sync_skills.py` (and
the `sync_skills_hook.py` PostToolUse auto-deploy) push repo -> bundle with
rmtree+copytree, so a lossy repo copy would overwrite the only true copy on
the next skill edit. The seed must therefore be byte-for-byte from the bundle,
which is what this script does.

This is NOT bidirectional sync (forbidden — ADR §5 move 3). Guardrails:
  * REFUSES when `.claude/skills/<skill>` already exists. Once a repo copy
    exists, every edit goes through the repo authoring path; there is no
    deployed -> repo overwrite, ever (deliberately no --force).
  * REFUSES when the source dir lacks a SKILL.md (not a real skill).
  * Copies one named skill byte-for-byte; never touches other skills.

After a successful import the repo is canonical for that skill. Gate + commit:

  python scripts/check_skill_refs.py --skill <name>
  python scripts/check_skills_no_constants.py
  python scripts/sync_skills.py --check
  git add .claude/skills/<name>  &&  git commit

Source resolution (mirrors sync_skills.py deploy-target resolution):
  1. --source <path>            (explicit, wins)
  2. $SKILLS_DEPLOY_TARGET       (env override)
  3. sync_skills.DEFAULT_DEPLOY_TARGET (the cloud-synced AppData bundle)

Exit codes:
  0 — imported
  1 — refused: repo copy already exists (use the repo authoring path)
  2 — source missing / not a skill dir
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_SKILLS = REPO_ROOT / ".claude" / "skills"

# Reuse sync_skills.py's target resolution so the two scripts can never drift
# on where the deployed bundle lives.
_SS_PATH = Path(__file__).resolve().parent / "sync_skills.py"
_spec = importlib.util.spec_from_file_location("sync_skills", _SS_PATH)
_sync_skills = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sync_skills)


def import_skill(source_skill: Path, dest_skill: Path) -> tuple[int, str]:
    """Copy one skill dir from the deployed bundle into the repo. No overwrite."""
    if dest_skill.exists():
        return 1, (
            f"REFUSED: repo copy already exists: {dest_skill}\n"
            "  Edits go through the repo authoring path (ADR 2026-06-04 §2.2);\n"
            "  there is no deployed -> repo overwrite. If the bundle diverged,\n"
            "  reconcile by hand and commit in-repo."
        )
    if not source_skill.is_dir():
        return 2, f"ERROR: source skill dir missing: {source_skill}"
    if not (source_skill / "SKILL.md").exists():
        return 2, f"ERROR: source has no SKILL.md (not a skill dir): {source_skill}"

    shutil.copytree(source_skill, dest_skill)

    files = sorted(p for p in dest_skill.rglob("*") if p.is_file())
    lines = [f"Imported {len(files)} file(s)  {source_skill} -> {dest_skill}"]
    for f in files:
        rel = f.relative_to(dest_skill).as_posix()
        n_lines = len(f.read_bytes().splitlines())
        lines.append(f"  {rel}  ({n_lines} lines, {f.stat().st_size} bytes)")
    return 0, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("skill", help="skill directory name to import (e.g. strategy-validation)")
    parser.add_argument("--source", default=None,
                        help="deployed bundle root (overrides $SKILLS_DEPLOY_TARGET / default)")
    parser.add_argument("--repo-skills", type=Path, default=REPO_SKILLS,
                        help="in-repo skills dir (default: .claude/skills)")
    args = parser.parse_args(argv)

    source_root = _sync_skills.resolve_target(args.source)
    rc, msg = import_skill(source_root / args.skill, args.repo_skills / args.skill)
    print(msg, file=sys.stderr if rc else sys.stdout)
    if rc == 0:
        print(
            "\nRepo is now canonical for this skill. Gate + commit:\n"
            f"  python scripts/check_skill_refs.py --skill {args.skill}\n"
            "  python scripts/check_skills_no_constants.py\n"
            "  python scripts/sync_skills.py --check\n"
            f"  git add .claude/skills/{args.skill}  &&  git commit"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
