#!/usr/bin/env python3
"""check_skill_deploy_sync.py -- do skills cited in an ADR Verification block
actually exist at their deployed path?

Root cause this gate closes: docs/adr/2026-08-09-check-brief-canon-ruling.md
names ~/.claude/skills/brief-authoring/scripts/check_brief.py as canonical,
and every citing ADR's own Verification block runs it -- but the deployed
bundle can silently fall behind the in-repo source (sync_skills.py's own
docstring: the one-way contract "cannot be fully enforced from this script --
the sync layer can still clobber"). Concretely: docs/adr/2026-08-27-ssot-
data-lineage-remediation-program.md Sec.0 Step 1 found the cited script had
NEVER existed at all, on either side of the sync boundary, so
`sync_skills.py --check` (which only diffs files that exist repo-side)
structurally could not see the defect. This gate makes that whole class of
drift visible instead of letting the Verification block fail silently or not
get run at all.

Scope: greps docs/adr/**/*.md for `~/.claude/skills/<name>/scripts/<file>.py`
citations, resolves each against $HOME (or HOME_SKILLS_DEPLOY_TARGET_OVERRIDE
for tests), and checks existence. Does not check content/hash equivalence --
that is sync_skills.py --check's job; this gate only asks "does the cited
path exist at all", the same floor check_falsifier_reachability.py applies to
falsifier commands.

SKIP vs PASS (2026-08-28 review fix -- Critical): this gate resolves a
deploy ROOT (~/.claude/skills/ or the override) before it can check anything
under it. GitHub Actions runners -- and any fresh clone -- have no such
directory at all; there is no deploy step in .github/workflows/, by design
(deploying skills to a CI runner's $HOME would be theater, not verification).
On such a machine the prior version of this script still walked the citation
list, found every target missing under a nonexistent root, and exited 1 --
hard-failing the sole required CI check (`skills (3.12)`, which runs every
`tier: always` gate unconditionally via `gate_manifest.py --tier check`) on
EVERY future PR, forever, for a property of the local machine, not the
commit. Mirrors check_falsifier_reachability.py's own honesty convention
(distinguishing "no docs/adr -- skipped" from "OK" from "WARN"): when the
resolved deploy root does not exist AT ALL, this script now prints a SKIP
message and exits 0 -- explicitly NOT a pass, just nothing to check here.
When the root DOES exist and a cited script is genuinely missing under it,
the real check is unchanged: exit 1, drift listed.
"""
import os
import re
import sys
from pathlib import Path

CITATION_RE = re.compile(r"~/\.claude/skills/([\w-]+)/scripts/([\w.]+\.py)")


def find_cited_skill_scripts(adr_dir: Path) -> set[tuple[str, str]]:
    cited = set()
    for path in adr_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for skill, script in CITATION_RE.findall(text):
            cited.add((skill, script))
    return cited


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    adr_dir = Path(
        os.environ.get("ADR_DIR_OVERRIDE")
        or (repo_root / "docs" / "adr")
    )
    home_skills = Path(
        os.environ.get("HOME_SKILLS_DEPLOY_TARGET_OVERRIDE")
        or (Path.home() / ".claude" / "skills")
    )

    cited = find_cited_skill_scripts(adr_dir)
    if not cited:
        print("No ~/.claude/skills/*/scripts/*.py citations found in docs/adr/ -- nothing to check.")
        return 0

    if not home_skills.is_dir():
        print(
            f"SKIP: no deploy target at {home_skills} -- this machine has no "
            "~/.claude/skills/ bundle at all (CI runner / fresh clone; there is "
            "no skills-deploy step in .github/workflows/, by design). NOT "
            "CHECKED, not a pass -- this gate cannot compare against a bundle "
            "that does not exist. Run `python scripts/sync_skills.py` on a "
            "machine that has a deployed bundle to exercise the real check."
        )
        return 0

    missing = []
    for skill, script in sorted(cited):
        target = home_skills / skill / "scripts" / script
        if not target.exists():
            missing.append((skill, script, target))

    if missing:
        print(f"DRIFT: {len(missing)} ADR-cited skill script(s) missing from deployed bundle:")
        for skill, script, target in missing:
            print(f"  {skill}/scripts/{script} -- expected at {target}")
        print("Run: python scripts/sync_skills.py")
        return 1

    print(f"OK: {len(cited)} ADR-cited skill script(s) present in deployed bundle.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
