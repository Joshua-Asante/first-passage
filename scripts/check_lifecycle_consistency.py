#!/usr/bin/env python3
"""check_lifecycle_consistency.py — strategy-lifecycle-tier restatement gate.

The lifecycle multiplier state (`AUTHORIZED · MECHANISM @ 1.00×`) is
independently restated as bare prose in 25+ files repo-wide, almost none of
them citing docs/methodology/strategy_lifecycle.md (the canonical owner) or
core/lifecycle.py (the code-level ground truth) — found during the 2026-08-26
memory-architecture audit. That is the widest, least-tethered fact-duplication
pattern found in the repo: if the tier ever actually changes (a real
demotion), nothing forces any of these 25+ mentions to update, and nothing
would notice if only some of them did.

This gate does NOT try to consolidate the prose (most of the 25+ sites are
closed ADRs / audit notes / archived session entries — historical record, not
living state; rewriting their body text would be exactly the "retelling"
CLAUDE.md's own §Retention warns against). It checks the one thing that IS
mechanically knowable: whether a (TIER, MULTIPLIER) pair a LIVE (non-
historical) file states is actually consistent with core/lifecycle.py's tier
ladder and, when the ladder is currently uniform across every strategy (no
lifecycle_state.json -> every leg AUTHORIZED @ 1.00x, the live reality as of
this writing), with that single current tier.

Two HARD checks:
  L1 — LADDER: every (tier, multiplier) pair found in a live file must be a
       real pairing in core.lifecycle.TIER_MULTIPLIER (catches an internally
       inconsistent restatement, e.g. "AUTHORIZED @ 0.50x" -- always a bug,
       regardless of which strategy or whether the ladder is currently
       uniform).
  L2 — CURRENT (only enforced when load_lifecycle_state() is empty, i.e. the
       ladder is genuinely uniform right now): every tier found in a live
       file must equal DEFAULT_TIER. Deliberately NOT enforced once a real
       per-strategy state file exists, since free-form prose can't be
       reliably attributed to one specific strategy leg -- a stronger,
       leg-attributed check would need each mention to name its strategy
       unambiguously, which most of the 25+ sites don't do. L2 stays
       reachable at all only because today's ground truth happens to be
       uniform; re-derive it, don't assume it, if that ever stops being true.

Historical-record paths are exempt from both checks (path-prefix, matching
the live/historical boundary this repo's other gates already draw the same
way): docs/adr/, docs/briefs/closures/, docs/notes/audits/, docs/ltm/,
docs/superpowers/. A file under one of these is a point-in-time record of a
decision, not a place that should track a FUTURE tier change.

Exit codes: 0 = no HARD findings; 1 = one or more L1/L2.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "core"))

from lifecycle import DEFAULT_TIER, TIER_MULTIPLIER, load_lifecycle_state  # noqa: E402

# Path prefixes that are historical record, not living state -- exempt from
# both checks. Matches the live/historical boundary check_adr_graph.py (A3/A4
# cold-stub handling) and the Great-Prune-era gates already draw.
_HISTORICAL_PREFIXES = (
    "docs/adr/",
    "docs/briefs/closures/",
    "docs/notes/audits/",
    "docs/ltm/",
    "docs/superpowers/",
)

# Tier word, then up to 60 chars of connective prose (durability tag, dashes,
# "no live venue" asides -- observed margin across all current restatements
# is ~12 chars), then "@ N.NN×". Deliberately does not require a leading
# strategy name: most sites don't reliably name one, and L1/L2 don't need it
# (see module docstring).
_TIER_ALT = "|".join(re.escape(t) for t in TIER_MULTIPLIER)
_PAIR_RE = re.compile(
    rf"\b({_TIER_ALT})\b[^\n@]{{0,60}}@\s*(\d\.\d\d)\s*[x×]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    severity: str   # "HARD"
    code: str       # "L1" | "L2"
    path: str
    lineno: int
    message: str


def is_historical(rel_path: str) -> bool:
    return any(rel_path.startswith(p) for p in _HISTORICAL_PREFIXES)


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if is_historical(rel):
            continue
        yield path, rel


def check_file(path: Path, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    uniform_state = not load_lifecycle_state()
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _PAIR_RE.finditer(line):
            tier = m.group(1).upper()
            mult = float(m.group(2))
            expected = TIER_MULTIPLIER.get(tier)
            if expected is None or abs(expected - mult) > 1e-9:
                findings.append(Finding(
                    "HARD", "L1", rel, lineno,
                    f"states {tier!r} @ {mult:.2f}x, but core.lifecycle.TIER_MULTIPLIER"
                    f" pairs {tier!r} with {expected!r} -- internally inconsistent"
                    if expected is not None else
                    f"states unknown tier {tier!r} (not in TIER_MULTIPLIER: "
                    f"{sorted(TIER_MULTIPLIER)})"
                ))
            elif uniform_state and tier != DEFAULT_TIER:
                findings.append(Finding(
                    "HARD", "L2", rel, lineno,
                    f"states tier {tier!r}, but no lifecycle_state.json exists so "
                    f"every strategy is currently {DEFAULT_TIER!r} (code default) -- "
                    f"stale relative to the current uniform state"
                ))
    return findings


def collect_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path, rel in iter_markdown_files(root):
        findings.extend(check_file(path, rel))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)

    findings = collect_findings(args.repo_root)
    for f in findings:
        print(f"HARD: {f.path}:{f.lineno}: {f.code} {f.message}")

    if findings:
        print(
            f"\ncheck_lifecycle_consistency: {len(findings)} finding(s). "
            "core/lifecycle.py (+ lifecycle_state.json when present) is the "
            "authority; repair the drifting doc, do not relax the gate."
        )
        return 1
    print("check_lifecycle_consistency: OK — no lifecycle-tier restatement drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
