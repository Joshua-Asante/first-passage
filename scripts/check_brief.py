#!/usr/bin/env python3
"""check_brief.py — brief well-formedness validator.

Current checker ownership: scripts/README.md#brief-checker-ownership.
Historical landing decision (§2.5):
https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-06-04-methodology-skills-under-vc.md

The checks are NOT invented — they are the *mechanical* subset of the
"six load-bearing discipline checks" and the CC-handoff "patterns 7–10" that
`.claude/skills/brief-authoring/SKILL.md` prescribes. Provenance per check is
recorded in the `Check` table below and in each check function's docstring.

What this validates (mechanical only — judgment checks stay with the human):

  §0  Rule-0 reads      present AND cite at least one concrete repo path.
                        (SKILL.md "The six ... checks" #1; Known-trap #3.)
  §1  Context           present (SKILL.md trap #8: orphan briefs that don't
                        connect to standing doctrine).
  §4  Falsifiable H     present with a supported hypothesis/falsifier,
                        Revert-trigger, if-then or reject/accept-if framing.
                        (SKILL.md check #2; trap #1 ceremonial-section guard.)
  §5  Forbidden moves   present AND lists at least one move (a list item).
                        (SKILL.md check #3; trap #4.)
  §6  Gate criteria     present (SKILL.md check #4; binary-verdict wording is a
                        WARN nudge, not a hard fail — see below).
  §10 Audit hooks       present AND contain a fenced code block (runnable hook).
                        (SKILL.md check #6; trap #6.)

  CC-handoff extras (only when --type handoff):
  §0.5 Clarifying-Qs    present (SKILL.md pattern #7).
  §6   Status taxonomy  mentions DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT /
                        BLOCKED (SKILL.md pattern #8).

Severity model (mirrors validate_params.py's HARD/WARN tiers):
  HARD (exit 1) — a required section is missing, or a required *content*
                  assertion fails (no falsifier in §4, no list in §5, no fenced
                  block in §10, no repo path in §0).
  WARN (exit 0) — a required section is present but EMPTY (the ceremonial-section
                  failure mode, SKILL.md trap #1), or a soft nudge fires
                  (e.g. §6 has no binary-verdict keyword).

Type → required-section sets (SKILL.md type × check matrix, 2026-08-23):
  adr / brief   — §0, §1, §4, §5, §6, §10   (inquire / full ADR)
  handoff       — §0, §1, §4, §5, §6, §10   plus §0.5 and the §6 status taxonomy
  generic       — same as adr/brief; used when --type is omitted and inference
                  finds no stronger signal. Header `**Loop:** Inquire-…` /
                  `**Type:** Inquire-…` wins over body §0.5 / spawn-taxonomy
                  sniffing (those sections are copied into CC-handoff-ready
                  Inquire briefs and are not a `--type handoff` signal).
  lock/notice/lesson/audit — NOT CHECKED (type-owned templates; this subset
                  does not model their section contracts).
  light ADR     — NOT CHECKED (`**Tier:** light`; Decision/Grounds/Reads/Gate/
                  Boundary). Header fields still go through check_adr_graph.py.
  closure       — not modeled here; `--type closure` delegates to
                  scripts/check_closure_disposition.py.

Relationship to the skill-side checker (CANONICAL):
  .claude/skills/brief-authoring/SKILL.md#checker-ownership owns the type contracts.
  Its scripts/check_brief.py is the canonical source; the ~/.claude/skills/ copy
  is deployed from that source. This repo-side checker is a mechanical subset.
  Unsupported types and concise/legacy light ADRs explicitly print NOT CHECKED;
  closure mode prints the delegated command, not a closure verdict. A subset
  result cannot replace the artifact's canonical validation and judgment checks.
  Both checkers accept the supported broadened §4 framings. The implementation
  below owns this subset's precise checks; checker unification is separate work.

Exit codes:
  0 — well-formed (WARN-level issues may still have printed)
  1 — one or more HARD violations
  2 — usage / file-not-found error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

import importlib.util

_engine_spec = importlib.util.spec_from_file_location("brief_checks", Path(__file__).resolve().parent.parent / ".claude/skills/brief-authoring/scripts/brief_checks.py")
_engine = importlib.util.module_from_spec(_engine_spec)
_engine_spec.loader.exec_module(_engine)
REPO_PATH_PREFIXES = _engine.REPO_PATH_PREFIXES
REPO_PATH_EXTS = _engine.REPO_PATH_EXTS
_SECTION_RE = _engine._SECTION_RE
_FENCE_RE = _engine._FENCE_RE
_INLINE_CODE_RE = _engine._INLINE_CODE_RE
_MD_LINK_RE = _engine._MD_LINK_RE
_LIST_ITEM_RE = _engine._LIST_ITEM_RE
_HYPOTHESIS_RE = _engine._HYPOTHESIS_RE
_FALSIFIER_RE = _engine._FALSIFIER_RE
_REVERT_TRIGGER_RE = _engine._REVERT_TRIGGER_RE
_IF_THEN_RE = _engine._IF_THEN_RE
_REJECT_ACCEPT_RE = _engine._REJECT_ACCEPT_RE
_VERDICT_RE = _engine._VERDICT_RE
_HANDOFF_STATUS_TOKENS = _engine._HANDOFF_STATUS_TOKENS
_COMMIT_ANCHOR_RE = _engine._COMMIT_ANCHOR_RE
_DATE_ANCHOR_RE = _engine._DATE_ANCHOR_RE
_BARE_PATH_TOKEN_RE = _engine._BARE_PATH_TOKEN_RE
_LIGHT_TIER_RE = _engine._LIGHT_TIER_RE
_CONCISE_ADR_RE = _engine._CONCISE_ADR_RE
_GENERAL_REQUIRED = _engine.GENERAL_REQUIRED
_header_block = _engine._header_block
is_light_tier = _engine.is_light_tier
_mask_fences = _engine._mask_fences
split_sections = _engine.split_sections
_looks_like_repo_path = _engine._looks_like_repo_path
_section0_cites_repo_path = _engine._section0_cites_repo_path
_section0_has_anchor = _engine._section0_has_anchor
Violation = _engine.Violation


REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SECTIONS = {
    "adr":     _GENERAL_REQUIRED,
    "brief":   _GENERAL_REQUIRED,
    "generic": _GENERAL_REQUIRED,
    "handoff": _GENERAL_REQUIRED + ("0.5",),
}

# Repo-side internal types this subset actually models.
_INTERNAL_TYPES = ("adr", "brief", "handoff", "generic")

# The skill-side checker's vocabulary, mapped to the closest internal type so a
# doc-copied `--type <skill-name>` resolves here instead of argparse-dying. The
# skill-side checker remains canonical (see module docstring); these are accepted
# for portability, not because this subset fully models them.
_TYPE_ALIASES = {
    "cc_handoff": "handoff",
    "inquire":    "brief",
    "lock":       "brief",
    "notice":     "generic",
    "lesson":     "generic",
    "audit":      "generic",
}
# Skill-only names: accepted, but only the mechanical subset runs — flagged.
SKILL_ONLY_TYPES = frozenset(_TYPE_ALIASES)

# Types whose SECTION CONTRACT this subset does not model (added 2026-08-09).
# In the skill-side canon an audit note's §4 is root-cause analysis, a notice
# log's §4 is a routing decision, and a lesson capture is keyed on named headers
# (Pattern / Anchor incidents / Repair) rather than numbered sections. Aliasing
# them to `generic` applied ANOTHER type's schema and reported well-formed
# artifacts as MALFORMED — measured 2026-08-09 against the skill's own canonical
# templates and against real repo artifacts. Applying a contract we do not own is
# worse than declining to check: a false MALFORMED trains authors to ignore the
# checker. For these, run only type-agnostic checks and say so.
# Measured 2026-08-09 against the skill's own canonical templates:
#   lock   — §4 is a trigger/threshold TABLE ("Binary triggers that supersede
#            this lock"); the skill-side checker accepts a table natively, this
#            one only pattern-matches prose.
#   notice — §0 is a "Source anchor", explicitly "one line, not a verified-commit
#            list", so even the §0-repo-path check is the wrong contract here.
#   lesson — keyed on named headers (Pattern / Anchor incidents / Repair), not
#            numbered sections at all; repo-side reported 6/6 sections missing.
#   audit  — §4 is root-cause analysis, not a falsifiable hypothesis.
# For these we assert NOTHING and say so, rather than reporting a false verdict
# in either direction. Types this subset genuinely models: adr, inquire/brief,
# cc_handoff/handoff, generic.
_UNMODELED_CONTRACT_TYPES = frozenset({"lock", "notice", "lesson", "audit"})


# Closure is accepted so a copied `--type closure` does not argparse-die;
# main() delegates to check_closure_disposition.py and does not run §0–§10.
_CLOSURE_DELEGATE_TYPE = "closure"

# Every value the CLI / callers may pass.
ACCEPTED_TYPES = _INTERNAL_TYPES + tuple(_TYPE_ALIASES) + (_CLOSURE_DELEGATE_TYPE,)


def _normalize_type(brief_type: str) -> str:
    """Map a skill-side type name to its repo-side internal equivalent.

    Internal types pass through unchanged; an unknown type falls back to
    'generic' (the same default infer_type uses on no signal)."""
    if brief_type in _INTERNAL_TYPES:
        return brief_type
    return _TYPE_ALIASES.get(brief_type, "generic")


def _is_empty_body(body: str) -> bool:
    """A section body (title line already stripped by split_sections) is 'empty'
    if it has no substantive content — only whitespace, markdown horizontal
    rules, or a 'TBD'/'N/A' placeholder. Catches SKILL.md trap #1 (ceremonial
    sections)."""
    stripped = body.strip()
    if not stripped:
        return True
    lines = [ln.strip() for ln in stripped.splitlines()]
    # Drop blank lines and markdown horizontal rules (---, ===, ***).
    content = [ln for ln in lines if ln and not set(ln) <= set("-—=*_ ")]
    if not content:
        return True
    joined = " ".join(content).lower()
    placeholder_only = re.sub(r"[^a-z]", "", joined)
    return placeholder_only in ("tbd", "na", "none", "tba", "todo")


_checks = _engine.NumberedChecks(_is_empty_body)
_check_required_sections = _checks._check_required_sections
_check_section0_paths = _checks._check_section0_paths
_check_falsifiable_hypothesis = _checks._check_falsifiable_hypothesis
_check_forbidden_moves = _checks._check_forbidden_moves
_check_fenced_section = _checks._check_fenced_section
_check_gate_verdicts = _checks._check_gate_verdicts
_check_handoff_extras = _checks._check_handoff_extras



# ── Individual checks ──────────────────────────────────────────

def _check_required_present(sections: dict[str, str], brief_type: str) -> list[Violation]:
    return _check_required_sections(sections, REQUIRED_SECTIONS[brief_type])


def _check_audit_hooks(sections: dict[str, str]) -> list[Violation]:
    return _check_fenced_section(sections, "10")


# ── Type inference ─────────────────────────────────────────────

# House header fields that declare the artifact's own type. Header-scoped so a
# later prose mention ("when spawned as a CC handoff") cannot flip inference.
# `Loop-of-Record` is a different field — the colon must follow `Loop` immediately.
_HEADER_FIELD_RE = re.compile(
    r"^\*\*(Loop|Brief type|Type):\*\*\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
# Inquire self-declaration at the START of the field value. "N/A — blocked
# before the Inquire-phase" must not match.
_INQUIRE_DECL_RE = re.compile(
    r"^\s*inquire(?:-style|-phase|-light)?\b",
    re.IGNORECASE,
)
# "…brief, CC-handoff-ready" is still an Inquire-style brief (spawnable), not
# a CC-handoff. Matches the GSUB-1 house line.
_HANDOFF_READY_BRIEF_RE = re.compile(
    r"\bbrief,\s*cc-handoff-ready\b",
    re.IGNORECASE,
)
# Genuine CC/Cursor handoff self-declaration. `(?!-ready)` keeps
# "CC-handoff-ready" (the Inquire-style qualifier) from counting.
_HANDOFF_DECL_RE = re.compile(
# `cursor` stays in this alternation after the 2026-09-15 Cursor retirement:
# two FROZEN historical briefs self-declare `**Brief type:** Cursor handoff`
# (docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md,
#  docs/briefs/handoffs/2026-07-24-cursor-handoff-agent-surface-posture-sync.md).
# Dropping it would silently reclassify those records. The regex reads history;
# it does not authorize a Cursor lane.
    r"\b(?:cc[/\s-]*cursor|cursor|cc)[\s-]+handoff\b(?!-ready)",
    re.IGNORECASE,
)


def _declared_type_from_header(text: str) -> str | None:
    """Return an internal type if the header self-declares one, else None.

    Inquire-style / Inquire-phase / Inquire-light (and the
    `brief, CC-handoff-ready` qualifier) win over a CC-handoff declaration on
    another header line, because CC-handoff-ready Inquire briefs are still
    Inquire briefs — they copy §0.5 / spawn-taxonomy language without being
    `--type handoff` artifacts.
    """
    head = _header_block(text)
    saw_handoff = False
    for m in _HEADER_FIELD_RE.finditer(head):
        value = m.group(2)
        if _INQUIRE_DECL_RE.match(value) or _HANDOFF_READY_BRIEF_RE.search(value):
            return "brief"
        if _HANDOFF_DECL_RE.search(value):
            saw_handoff = True
    if saw_handoff:
        return "handoff"
    return None


def infer_type(path: Path, text: str) -> str:
    """Best-effort brief-type inference when --type is omitted.

    Precedence (first match wins):
      1. Header self-declaration (`**Loop:**` / `**Brief type:**` / `**Type:**`).
         An Inquire-style / Inquire-phase line is authoritative even when the
         body also has §0.5 or the four-state spawn taxonomy (those sections
         are copied into CC-handoff-ready Inquire briefs; treating them as
         `--type handoff` is a FORM false-positive).
      2. Filename containing handoff / cc-handoff / spawn ⇒ handoff
      3. A §0.5 section or the four-state status taxonomy anywhere ⇒ handoff
      4. Filename / first heading mentioning ADR ⇒ adr
      5. generic (no stronger signal)
    """
    declared = _declared_type_from_header(text)
    if declared is not None:
        return declared
    name = path.name.lower()
    if "handoff" in name or "cc-handoff" in name or "spawn" in name:
        return "handoff"
    if "0.5" in split_sections(text) or all(t in text for t in _HANDOFF_STATUS_TOKENS):
        return "handoff"
    head = text[:400].lower()
    if name.startswith("adr") or "adr" in name or re.search(r"^#\s*adr\b", head):
        return "adr"
    return "generic"


# ── Top-level run ──────────────────────────────────────────────

def check_brief(text: str, brief_type: str) -> list[Violation]:
    """Run all mechanical checks for `brief_type`. Returns all violations.

    `brief_type` may be a repo-side internal type or a skill-side name (e.g.
    'cc_handoff'); skill-side names are normalized to the closest internal type
    so a doc-copied invocation behaves consistently."""
    requested = brief_type
    if requested == _CLOSURE_DELEGATE_TYPE:
        return []
    if requested == "adr" and _CONCISE_ADR_RE.search(_header_block(text)):
        return []  # canonical skill checker owns this named-section contract
    brief_type = _normalize_type(brief_type)
    sections = split_sections(text)
    violations: list[Violation] = []
    if is_light_tier(text):
        # Light-tier records have their own ratified shape; the numbered-section
        # contract does not apply. See _LIGHT_TIER_RE.
        return []
    if requested in _UNMODELED_CONTRACT_TYPES:
        # We do NOT own this type's section contract, so we assert nothing —
        # see _UNMODELED_CONTRACT_TYPES. main() reports NOT CHECKED, never
        # "well-formed", so an empty violation list is not read as a pass.
        return []
    violations.extend(_check_required_present(sections, brief_type))
    violations.extend(_check_section0_paths(sections))
    violations.extend(_check_falsifiable_hypothesis(sections))
    violations.extend(_check_forbidden_moves(sections))
    violations.extend(_check_audit_hooks(sections))
    violations.extend(_check_gate_verdicts(sections))
    if brief_type == "handoff":
        violations.extend(_check_handoff_extras(sections))
    return violations


def emit_report(path: Path, brief_type: str, violations: list[Violation]) -> int:
    """Print per-violation report + summary. Return exit code (0 or 1)."""
    hard = [v for v in violations if v.severity == "HARD"]
    warn = [v for v in violations if v.severity == "WARN"]
    print(f"check_brief: {path}  (type={brief_type})")
    for v in hard:
        print(f"  {v}")
    for v in warn:
        print(f"  {v}")
    print()
    print(f"Summary: {len(hard)} HARD violation(s), {len(warn)} WARN violation(s)")
    if hard:
        print("RESULT: MALFORMED")
        return 1
    print("RESULT: well-formed" + (" (with warnings)" if warn else ""))
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: parse args, validate one brief, return its exit code."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brief", type=Path, help="path to the brief markdown file")
    parser.add_argument("--type", choices=list(ACCEPTED_TYPES),
                        default=None, metavar="TYPE",
                        help="Modeled: adr, brief, handoff, generic, inquire, "
                             "cc_handoff. Unmodeled (NOT CHECKED): lock, notice, "
                             "lesson, audit, and any **Tier:** light record. "
                             "closure delegates to check_closure_disposition.py. "
                             "Default: infer from header Loop/Type, then "
                             "filename/content.")
    args = parser.parse_args(argv)

    if not args.brief.exists():
        print(f"brief not found: {args.brief}", file=sys.stderr)
        return 2
    if not args.brief.is_file():
        print(f"not a file: {args.brief}", file=sys.stderr)
        return 2

    text = args.brief.read_text(encoding="utf-8", errors="replace")
    requested = args.type or infer_type(args.brief, text)
    brief_type = _normalize_type(requested)
    if requested == _CLOSURE_DELEGATE_TYPE:
        print("note: closure records are gated by "
              "scripts/check_closure_disposition.py, not this subset.",
              file=sys.stderr)
        print(f"check_brief: {args.brief}  (type=closure)")
        print("RESULT: DELEGATED — run: "
              f"python scripts/check_closure_disposition.py {args.brief}")
        return 0
    if requested == "adr" and _CONCISE_ADR_RE.search(_header_block(text)):
        print(f"check_brief: {args.brief}  (type=adr, format=concise)")
        print("RESULT: NOT CHECKED — concise ADR; run the canonical skill-side "
              "checker for Decision/Grounds/Current owner validation")
        return 0
    if is_light_tier(text):
        print("note: light-tier decision record (ADR 2026-08-08-adr-ceremony-tiering) "
              "— the numbered-section contract does not apply; no checks were run.",
              file=sys.stderr)
        print(f"check_brief: {args.brief}  (type={brief_type}, tier=light)")
        print("RESULT: NOT CHECKED — light-tier record; shape is "
              "Decision/Grounds/Reads/Gate/Boundary, ≤300-word body")
        return 0
    if requested in _UNMODELED_CONTRACT_TYPES:
        print(f"note: '{requested}' has a per-type section contract this repo-side "
              f"subset does NOT model, so NO checks were run. This is not a pass "
              f"and not a failure. Fill the type template under "
              f".claude/skills/brief-authoring/references/.",
              file=sys.stderr)
        print(f"check_brief: {args.brief}  (type={requested})")
        print(f"RESULT: NOT CHECKED — '{requested}' contract not modeled "
              f"in this subset; fill the type template")
        return 0
    if requested in SKILL_ONLY_TYPES:
        print(f"note: '{requested}' is a skill-side brief type; this repo-side "
              f"script ran only its mechanical subset (internal type "
              f"'{brief_type}'). For the authoritative discipline gate, run the "
              f"skill-side checker "
              f"(~/.claude/skills/brief-authoring/scripts/check_brief.py).",
              file=sys.stderr)
    # Pass the REQUESTED type, not the normalized one: check_brief normalizes
    # internally, and it needs the original name to recognize a type whose
    # section contract this subset does not model (_UNMODELED_CONTRACT_TYPES).
    # Passing the normalized name here silently defeated that branch.
    violations = check_brief(text, requested)
    return emit_report(args.brief, brief_type, violations)


if __name__ == "__main__":
    sys.exit(main())
