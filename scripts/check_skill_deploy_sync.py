#!/usr/bin/env python3
"""check_skill_deploy_sync.py -- do skills cited in an ADR Verification block
actually exist at their deployed path?

Current contract: scripts/README.md#skill-lifecycle. Historical root cause:
https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-09-check-brief-canon-ruling.md
names ~/.claude/skills/brief-authoring/scripts/check_brief.py as canonical,
and every citing ADR's own Verification block runs it -- but the deployed
bundle can silently fall behind the in-repo source (the historical sync
design could not prevent external rewrites). Concretely: docs/adr/2026-08-27-ssot-
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

Second route to the same false-fail (2026-09-15): managed remote sessions
(Claude Code on the web) DO have a ~/.claude/skills/ directory, but it is
harness-owned -- observed contents were only `session-start-hook/` and
`synced/<uuid>_<uuid>/...` (the plugin marketplace's own copy of skills
such as brief-authoring). Nothing under that root was published by
scripts/sync_skills.py, so `brief-authoring/scripts/check_brief.py` was
absent directly under it, the root-exists test above took the real-check
branch, and `gate_manifest.py --tier check` exited 1 on an unmodified
`main` checkout. The SKIP decision therefore keys on whether THIS REPO'S
deployed bundle is present -- at least one of this repo's skills has a
directory DIRECTLY under the root (see bundle_skill_dirs_present) -- not on
whether the root exists. The marker set is the ADR-cited skills PLUS every
skill directory the repo owns under .claude/skills/. Keying on the cited
skill alone had a hole (Codex review of PR #403): the ADR corpus cites only
brief-authoring, so a real bundle that lost brief-authoring/ itself -- the
exact external rewrite this gate exists to catch -- would have read as
harness-owned and SKIPped instead of reporting the deletion as drift. With
repo-owned names in the marker set, that bundle still shows two dozen other
repo skills, takes the real check, and lists brief-authoring as missing.
A root holding only foreign entries SKIPs (NOT CHECKED); a root that has
any repo skill's directory but lacks a cited script fails (exit 1, drift
listed); a partial bundle is drift, not a skip. The marker-file alternative (have
sync_skills.py stamp the target and SKIP when the stamp is absent) was
rejected: every bundle published before the marker existed -- including
the operator's live one -- would silently SKIP until republished, and
external cloud sync can rewrite the target without preserving a marker
(scripts/README.md#skill-lifecycle already records that limit).
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


def repo_skill_names(repo_root: Path) -> set[str]:
    """Names of every skill this repo owns: the directories under .claude/skills/.

    They join the marker set so that a deployed bundle is recognised by ANY of
    its skills, not only by the one the ADR corpus happens to cite -- otherwise
    the disappearance of that one cited skill would make the bundle look
    harness-owned and the gate would SKIP on the very defect it guards.
    """
    skills_dir = repo_root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return set()
    return {
        p.name for p in skills_dir.iterdir()
        if p.is_dir() and not p.name.startswith((".", "_"))
    }


def bundle_skill_dirs_present(home_skills: Path, marker_skills: set[str]) -> list[str]:
    """Marker skills (ADR-cited or repo-owned) with a directory DIRECTLY under the root.

    This is the SKIP / real-check decision (2026-09-15): an empty list means
    the root is not this repo's deployed bundle (harness-owned entries only,
    e.g. a managed remote container), so there is nothing to compare
    against. Nested copies (synced/<uuid>/<skill>/) deliberately do not
    count -- they are not a sync_skills.py release.
    """
    return sorted(skill for skill in marker_skills if (home_skills / skill).is_dir())


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
            "that does not exist. Re-run this existence checker "
            "(`python scripts/check_skill_deploy_sync.py`) on a machine "
            "where the deployed bundle already exists. Publication is not "
            "required to perform this check."
        )
        return 0

    cited_skills = sorted({skill for skill, _ in cited})
    owned = repo_skill_names(repo_root)
    markers = set(cited_skills) | owned
    if not bundle_skill_dirs_present(home_skills, markers):
        try:
            entries = sorted(p.name for p in home_skills.iterdir())
        except OSError:
            entries = []
        shown = ", ".join(entries[:8]) + (", ..." if len(entries) > 8 else "")
        print(
            f"SKIP: deploy target {home_skills} exists but holds none of this "
            f"repo's skill directories directly under it -- neither the ADR-cited "
            f"({', '.join(cited_skills)}) nor any of the {len(owned)} skills under "
            f".claude/skills/ (top-level entries: {shown or '<empty>'}). That root is "
            "not this repo's deployed bundle -- e.g. a managed remote "
            "container's harness-owned ~/.claude/skills/ (session-start-hook/, "
            "synced/<uuid>/... marketplace copies), which no sync_skills.py "
            "release ever populated. NOT CHECKED, not a pass -- this gate "
            "cannot compare against a bundle that was never published here. "
            "Re-run this existence checker "
            "(`python scripts/check_skill_deploy_sync.py`) on a machine where "
            "the deployed bundle already exists. Publication is not required "
            "to perform this check."
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
        print(
            "Missing cited scripts are not fixed by a no-argument "
            "publication. From a primary main checkout, after review of a "
            "named revision, publish explicitly: "
            "python scripts/sync_skills.py --revision <reviewed-sha> "
            "--target <explicit-destination>  "
            "(or: make sync-skills REVISION=<reviewed-sha> "
            "TARGET=<explicit-destination>). Policy: "
            "scripts/README.md#skill-lifecycle."
        )
        return 1

    print(f"OK: {len(cited)} ADR-cited skill script(s) present in deployed bundle.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
