#!/usr/bin/env python3
"""check_brief.py — brief well-formedness validator.

ADR `docs/adr/2026-06-04-methodology-skills-under-vc.md` §2.5 calls for landing
this script: every brief's "Verification block" (and the two 2026-06-04 ADRs)
invokes `python scripts/check_brief.py <brief.md>`, but the script did not exist
in-repo. This is that script.

The checks are NOT invented — they are the *mechanical* subset of the
"six load-bearing discipline checks" and the CC-handoff "patterns 7–10" that
`.claude/skills/brief-authoring/SKILL.md` prescribes. Provenance per check is
recorded in the `Check` table below and in each check function's docstring.

What this validates (mechanical only — judgment checks stay with the human):

  §0  Rule-0 reads      present AND cite at least one concrete repo path.
                        (SKILL.md "The six ... checks" #1; Known-trap #3.)
  §1  Context           present (SKILL.md trap #8: orphan briefs that don't
                        connect to standing doctrine).
  §4  Falsifiable H     present AND contains an "H:" / hypothesis statement AND
                        a falsifier/falsification clause.
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
  The authoritative brief-discipline checker is skill-side —
  `~/.claude/skills/brief-authoring/scripts/check_brief.py` — with 7 types
  ({inquire, adr, lock, cc_handoff, notice, lesson, audit}), `--self-test`, and
  `--list-checks`. THIS repo-side script is its *mechanical subset*: landed by
  ADR `2026-06-04-methodology-skills-under-vc.md` §2.5 so every brief's
  verification block resolves an in-repo path and CI / a public clone can run
  *something* without the skill present. When the two disagree, the skill-side
  result governs.

  Type-name reconciliation (so a doc-copied `--type <skill-name>` never
  hard-errors here): the skill-side vocabulary is accepted and mapped to the
  closest repo-side internal type —
      cc_handoff → handoff       inquire → brief        lock → brief
      notice → generic           lesson → generic       audit → generic
  Requesting any skill-only name prints a one-line note that only the mechanical
  subset ran (see `SKILL_ONLY_TYPES`).

  Known divergences (the two checkers can disagree in BOTH directions — a green
  run here is NOT the full discipline gate, and a red run here is not necessarily
  malformed by the canon; the skill-side result governs):
    - Repo-side is WEAKER on several checks: it does not replicate the skill-side
      §3 question-form heuristic, the cc_handoff §7 two-pass / consolidated-read
      checks, the §6 BLOCKED sub-case taxonomy, or §10 command-recognition (here
      §10 needs only a fenced block, not a recognizable shell/python command).
    - Repo-side is STRICTER / more literal on §4: it requires an explicit
      hypothesis token ("H:" / "hypothesis") AND a "falsifi*" token in the §4
      body, whereas the skill-side ADR check also accepts the canonical
      "Revert trigger" / if-then / reject-accept-if framing without those words.
      So a canonical-template ADR using only "Revert trigger" wording passes
      skill-side but fails here until §4 also states the hypothesis explicitly.
  For the authoritative gate, run the skill-side checker.

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

REPO_ROOT = Path(__file__).resolve().parent.parent

# Repo top-level dirs that mark a token as a concrete repo path in §0.
REPO_PATH_PREFIXES = (
    "docs/", "config/", "ops/", "core/", "lab/", "data/", "tests/", "scripts/",
    ".claude/", "archive/", "analysis/", "strategies/", "reports/",
)
# File extensions that also mark a token as a concrete repo path.
REPO_PATH_EXTS = (
    ".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
    ".sh", ".bat", ".csv",
)

# Section heading: matches both "## §0 — Rule 0" and a bare "## 0. ..." /
# "## Section 0" style. The canonical brief uses "§N"; we accept the loose forms
# so a brief authored slightly off-template still parses.
_SECTION_RE = re.compile(
    r"^\s{0,3}#{1,4}\s+"            # markdown heading marker
    r"(?:§\s*|section\s+|sec\.\s*)?" # optional "§" / "Section" prefix
    r"(?P<num>\d+(?:\.\d+)?)"       # the number, e.g. 0, 4, 0.5, 2.6
    r"\b",
    re.IGNORECASE | re.MULTILINE,
)

# Fenced code block (```...```), used to detect runnable §10 audit hooks.
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
# Inline-code span, used to pick repo-path tokens out of §0 prose.
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
# Markdown link target.
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# A markdown list item (bullet or ordered).
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S", re.MULTILINE)

# §4 hypothesis / falsifier wording.
_HYPOTHESIS_RE = re.compile(r"\bH\s*:|\bhypothesis\b|^\s*\*?\*?H\b", re.IGNORECASE | re.MULTILINE)
_FALSIFIER_RE = re.compile(r"\bfalsifi", re.IGNORECASE)  # falsifier / falsified / falsification

# §4 ALTERNATIVE canonical framings (added 2026-08-09, ADR
# `2026-08-09-rejection-register-topology-and-bar-wiring.md` sibling fix).
# The canonical ADR template states its §4 as "**Revert trigger:** …" and the
# canonical lock/cc_handoff templates use if/then or reject-accept-if wording —
# none of which contains a literal "H:" or "falsifi*" token. The old paired-token
# requirement therefore HARD-failed the skill's own templates (6 of 7 measured
# 2026-08-09), which is a checker defect, not a template defect. §4 is satisfied
# by the paired tokens OR by any of these framings.
_REVERT_TRIGGER_RE = re.compile(r"\brevert\s+trigger\b", re.IGNORECASE)
_IF_THEN_RE = re.compile(r"\bif\b[^.\n]{0,200}?\bthen\b", re.IGNORECASE | re.DOTALL)
_REJECT_ACCEPT_RE = re.compile(r"\b(reject|accept)\b[^.\n]{0,40}\bif\b", re.IGNORECASE)

# §6 binary-verdict wording (soft nudge only).
_VERDICT_RE = re.compile(r"\bRESOLVED\b|\bFALSIFIED\b|\bAMBIGUOUS\b")

# CC-handoff status-return taxonomy (SKILL.md pattern #8).
_HANDOFF_STATUS_TOKENS = ("DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED")

# Required section numbers per brief type.
_GENERAL_REQUIRED = ("0", "1", "4", "5", "6", "10")
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

# LIGHT-tier decision records (ADR `2026-08-08-adr-ceremony-tiering.md`) declare
# `**Tier:** light` in the header block and deliberately carry NO numbered
# sections — the ratified shape is Decision / Grounds / Reads / Gate / Boundary,
# body capped at 300 words. Applying the full §0–§10 ADR contract to one reports
# 6 HARD violations on a correctly-formed record. Same defect class as
# _UNMODELED_CONTRACT_TYPES, found 2026-08-09 while authoring the first light ADR.
_LIGHT_TIER_RE = re.compile(r"^\*\*Tier:\*\*\s*light\b", re.IGNORECASE | re.MULTILINE)


def _header_block(text: str) -> str:
    """Return the markdown header (everything before the first `## ` heading).

    Shared by light-tier detection and type inference so a later prose mention
    of a header field cannot flip either classification."""
    return re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]


def is_light_tier(text: str) -> bool:
    """True if this artifact declares itself a light-tier decision record.

    Only the header region counts — the boundary is the first `## ` heading, so
    a later prose mention of `**Tier:** light` (e.g. an ADR *about* the tiering
    convention quoting it) is not miscounted as a self-declaration."""
    return bool(_LIGHT_TIER_RE.search(_header_block(text)))


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


class Violation(NamedTuple):
    """One well-formedness finding. Mirrors validate_params.py's Violation."""
    severity: str   # "HARD" or "WARN"
    section: str     # e.g. "§4" or "§10"
    message: str

    def __str__(self) -> str:
        return f"{self.severity}: {self.section} | {self.message}"


# ── Section parsing ────────────────────────────────────────────

def _mask_fences(text: str) -> str:
    """Return `text` with fenced code-block *content* blanked out, length and
    newlines preserved. Headings are located on this masked copy so that a
    `# 1. ...` comment INSIDE a ```bash audit-hook fence is not mistaken for a
    section heading — the failure that truncated §10 before its closing fence."""
    def _blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    return _FENCE_RE.sub(_blank, text)


def split_sections(text: str) -> dict[str, str]:
    """Return {section_number: body_text} for every detected heading.

    A section's body is everything from its heading up to (but excluding) the
    next heading at the same-or-shallower depth — approximated here as the text
    up to the next *section heading* of any number. Good enough for presence and
    emptiness checks; we do not need a full markdown tree.

    Heading positions are found on a fence-masked copy (offsets preserved) so
    fenced code content never registers as a heading; bodies are then sliced
    from the ORIGINAL text so §10's runnable-hook check sees the real fences.
    """
    matches = list(_SECTION_RE.finditer(_mask_fences(text)))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        num = m.group("num")
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # Drop the remainder of the heading line (the section *title*, e.g.
        # "— Falsifiable hypothesis") so it never leaks into content checks —
        # otherwise a §4 titled "Falsifiable hypothesis" trivially satisfies the
        # falsifier regex on its own title.
        nl = body.find("\n")
        body = body[nl + 1:] if nl != -1 else ""
        # First occurrence wins (a number repeated, e.g. two "§2.x", keeps §2's
        # first body — but we only key on top-level required numbers anyway).
        if num not in sections:
            sections[num] = body
    return sections


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


# ── Token extraction for §0 ────────────────────────────────────

def _looks_like_repo_path(token: str) -> bool:
    token = token.strip()
    if "/" not in token:
        return False
    low = token.lower()
    if low.startswith(("http://", "https://", "mailto:")):
        return False
    if token.startswith(REPO_PATH_PREFIXES):
        return True
    return token.endswith(REPO_PATH_EXTS)


# §0 anchor (ADR 2026-08-20-rule0-anchor-verification-and-triage-discipline.md
# Phase 1): commit hash, ISO date, or "last-modified". Presence only — not
# that the hash is current (a stale-but-real anchor is legitimate).
_COMMIT_ANCHOR_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
_DATE_ANCHOR_RE = re.compile(
    r"last[- ]modified|\b20\d{2}-\d{2}-\d{2}\b",
    re.IGNORECASE,
)
_BARE_PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_./\-]+")


def _section0_cites_repo_path(body: str) -> bool:
    """True if §0 names at least one concrete repo path (SKILL.md check #1)."""
    for m in _MD_LINK_RE.finditer(body):
        target = m.group(1).split(" ", 1)[0].split("#", 1)[0]
        if _looks_like_repo_path(target):
            return True
    for m in _INLINE_CODE_RE.finditer(body):
        tok = m.group(1).strip()
        # A command-with-args inline span may embed a path; check each word.
        for word in tok.split():
            word = word.split("#", 1)[0]
            if _looks_like_repo_path(word):
                return True
    for word in _BARE_PATH_TOKEN_RE.findall(body):
        if _looks_like_repo_path(word.split("#", 1)[0]):
            return True
    return False


def _section0_has_anchor(body: str) -> bool:
    """True if §0 carries a hash-shaped or date / last-modified anchor."""
    return bool(_COMMIT_ANCHOR_RE.search(body) or _DATE_ANCHOR_RE.search(body))


# ── Individual checks ──────────────────────────────────────────

def _check_required_present(sections: dict[str, str], brief_type: str) -> list[Violation]:
    """Required sections present; present-but-empty downgraded to WARN.

    Provenance: SKILL.md "The six load-bearing discipline checks" enumerate
    §0/§4/§5/§6/§10; trap #8 adds §1 (doctrine linkage). Empty-but-present is
    SKILL.md trap #1 (ceremonial sections)."""
    out: list[Violation] = []
    for num in REQUIRED_SECTIONS[brief_type]:
        if num not in sections:
            out.append(Violation("HARD", f"§{num}", "required section missing"))
        elif _is_empty_body(sections[num]):
            out.append(Violation("WARN", f"§{num}",
                                  "section present but empty / placeholder (ceremonial)"))
    return out


def _check_section0_paths(sections: dict[str, str]) -> list[Violation]:
    """§0 must cite a repo path *and* an adjacent-section anchor (ADR 2026-08-20)."""
    body = sections.get("0")
    if body is None or _is_empty_body(body):
        return []  # missing/empty already reported by the presence check
    if not _section0_cites_repo_path(body):
        return [Violation("HARD", "§0",
                          "Rule-0 reads cite no concrete repo path "
                          "(need e.g. `dd_protection.py` or `docs/adr/...`)")]
    if not _section0_has_anchor(body):
        return [Violation("HARD", "§0",
                          "Rule-0 path citation has no anchor "
                          "(commit hash or date / last-modified)")]
    return []


def _check_falsifiable_hypothesis(sections: dict[str, str]) -> list[Violation]:
    """§4 needs an H: statement AND a falsifier clause (SKILL.md check #2)."""
    body = sections.get("4")
    if body is None or _is_empty_body(body):
        return []  # presence check owns missing/empty
    # Canonical-template framings that carry a falsifier without the literal
    # token pair. Any one of these satisfies §4 on its own.
    if (_REVERT_TRIGGER_RE.search(body)
            or _IF_THEN_RE.search(body)
            or _REJECT_ACCEPT_RE.search(body)):
        return []
    out: list[Violation] = []
    if not _HYPOTHESIS_RE.search(body):
        out.append(Violation("HARD", "§4",
                            "no hypothesis statement (expected 'H:'/'hypothesis', "
                            "a 'Revert trigger', an if/then, or a reject/accept-if)"))
    if not _FALSIFIER_RE.search(body):
        out.append(Violation("HARD", "§4",
                            "no falsifier clause (expected 'Falsifier' / 'falsified', "
                            "a 'Revert trigger', an if/then, or a reject/accept-if)"))
    return out


def _check_forbidden_moves(sections: dict[str, str]) -> list[Violation]:
    """§5 must list at least one forbidden move (SKILL.md check #3, trap #4)."""
    body = sections.get("5")
    if body is None or _is_empty_body(body):
        return []
    if not _LIST_ITEM_RE.search(body):
        return [Violation("HARD", "§5",
                          "no forbidden moves listed (expected a bullet/numbered list)")]
    return []


def _check_audit_hooks(sections: dict[str, str]) -> list[Violation]:
    """§10 must contain a fenced code block — a runnable hook (SKILL.md check #6)."""
    body = sections.get("10")
    if body is None or _is_empty_body(body):
        return []
    if not _FENCE_RE.search(body):
        return [Violation("HARD", "§10",
                          "no runnable audit hook (expected a fenced ``` code block)")]
    return []


def _check_gate_verdicts(sections: dict[str, str]) -> list[Violation]:
    """§6 SHOULD use binary RESOLVED/FALSIFIED/AMBIGUOUS verdicts. Soft nudge:
    WARN only (SKILL.md check #4 names this discipline but the binary-vs-vague
    judgment is human; the keyword presence is the mechanical proxy)."""
    body = sections.get("6")
    if body is None or _is_empty_body(body):
        return []
    if not _VERDICT_RE.search(body):
        return [Violation("WARN", "§6",
                          "no binary verdict keyword "
                          "(RESOLVED / FALSIFIED / AMBIGUOUS) — gate may be vague")]
    return []


def _check_handoff_extras(sections: dict[str, str]) -> list[Violation]:
    """CC-handoff-only: §0.5 clarifying-Qs (pattern #7, presence owned elsewhere)
    and the §6 four-state status taxonomy (pattern #8)."""
    out: list[Violation] = []
    body6 = sections.get("6")
    if body6 is not None and not _is_empty_body(body6):
        present = [t for t in _HANDOFF_STATUS_TOKENS if t in body6]
        if len(present) < len(_HANDOFF_STATUS_TOKENS):
            missing = [t for t in _HANDOFF_STATUS_TOKENS if t not in present]
            out.append(Violation("HARD", "§6",
                                "CC-handoff status taxonomy incomplete; missing "
                                + ", ".join(missing)))
    return out


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
