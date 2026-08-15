#!/usr/bin/env python3
"""check_skills_no_constants.py — methodology-skill no-constants guard.

Extracted from the retired validate_params hub (ADR
docs/adr/2026-08-03-params-toml-gate-retirement.md). ADR
docs/adr/2026-06-04-methodology-skills-under-vc.md §2.4 hook #2.

CARVE-OUT: scans ONLY the four *methodology* skills, where a restated
operational constant is pure drift. Operational-reference skills
(prop-firm-challenge, code-defect-debugging) and pinescript-v6 are EXEMPT.

On CI / public clones with no `.claude/skills/` methodology dirs, this is a
clean no-op.

Exit codes:
  0 — zero HARD violations
  1 — one or more HARD violations
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

GUARDED_SKILLS = ("inqhiori", "ooda-loop", "programme-audit", "brief-authoring")

# Tuned to avoid false positives on legitimate pointer prose (e.g. lines that
# cite an allocation ADR path without restating a live constant).
_SKILL_CONST_PATTERNS = (
    ("version-assignment", re.compile(r"version\s*=")),
    ("risk_pct", re.compile(r"risk_pct")),
    ("bare-0.40", re.compile(r"(?<!\d)0\.40(?!\d)")),
    ("dd_protection-tier", re.compile(r"dd_protection.*1\.[05]")),
    ("allocation-pct", re.compile(r"(?<!\d)\d\.\d{1,2}%")),
)


@dataclass(frozen=True)
class Violation:
    severity: str
    location: str
    expected: str
    found: str

    def __str__(self) -> str:
        return (
            f"{self.severity}: {self.location}: "
            f"expected {self.expected}; found {self.found}"
        )


def check_skills_no_constants(repo_root: Path) -> list[Violation]:
    """Flag operational constants restated in the four GUARDED methodology skills."""
    violations: list[Violation] = []
    skills_root = repo_root / ".claude" / "skills"
    if not skills_root.is_dir():
        return violations
    for skill in GUARDED_SKILLS:
        skill_md = skills_root / skill / "SKILL.md"
        if not skill_md.exists():
            continue
        rel = skill_md.relative_to(repo_root).as_posix()
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, pat in _SKILL_CONST_PATTERNS:
                m = pat.search(line)
                if m:
                    violations.append(Violation(
                        "HARD", f"{rel}:{lineno}",
                        f"no operational constant ({label})",
                        f"'{m.group(0)}' in: {line.strip()[:80]}",
                    ))
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root", type=Path, default=REPO_ROOT,
        help="repo root for .claude/skills lookup",
    )
    args = parser.parse_args()
    hard = [v for v in check_skills_no_constants(args.repo_root) if v.severity == "HARD"]
    for v in hard:
        print(v)
    if hard:
        print(f"\nSummary: {len(hard)} HARD violation(s)")
        return 1
    print("check_skills_no_constants: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
