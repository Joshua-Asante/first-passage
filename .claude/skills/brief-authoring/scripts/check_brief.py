#!/usr/bin/env python3
"""check_brief.py — CANONICAL brief well-formedness validator (skill-side).

Authored under docs/adr/2026-08-09-check-brief-canon-ruling.md ("check_brief
canon: skill-side governs; repo-side declines what it cannot check"). That
ADR's own §0 Reads line claimed this file already existed, untracked, with a
passing --self-test; `docs/adr/2026-08-27-ssot-data-lineage-remediation-
program.md` §0 Step 1 re-verified that claim against git history and found
`git log --oneline --all -- ".claude/skills/brief-authoring/scripts/
check_brief.py"` returns ZERO commits, ever — the cited commit anchor
(`47cc3eb`) touches only the repo-side script plus an unrelated SKILL.md
doc-reference cleanup. This file is therefore authored fresh against the
2026-08-09 ADR's ratified §Decision text (the operative content) and the
current canonical templates under `.claude/skills/brief-authoring/references/`
(the closest thing to reconstructible ground truth for each type's section
contract) — NOT reconstructed from the unverifiable Reads-line claim about a
prior script's internals.

Relationship to the repo-side subset (`scripts/check_brief.py`, tracked,
proven, NOT modified by this file):

  ADR 2026-08-09 §Decision (quoted): "The skill-side check_brief.py is
  canonical for brief discipline; repo-side scripts/check_brief.py is its
  mechanical subset ... Repo-side now declines types whose section contract
  it does not model (lock, notice, lesson, audit, and light-tier records ->
  RESULT: NOT CHECKED) instead of applying the generic contract to them, and
  its §4 check accepts every canonical framing (Revert trigger, if/then,
  reject/accept-if), not only a literal H:+falsifi* pair."

  This file is the canonical half of that split. Unlike repo-side, it does
  NOT decline lock / notice / lesson / audit / light-tier records — it applies
  each type's OWN section contract (numbered §N for inquire/adr/cc_handoff/
  notice/audit; named markdown headings for lesson/light-tier; a best-effort
  content check for the retired `lock` type, which has no surviving template
  to derive a full contract from — see check_lock()'s docstring). It also
  carries the same broadened §4 acceptance repo-side already has (Revert
  trigger / if-then / reject-accept-if, not only H:+falsifi*).

Per-type section contracts (derived from the current 7 canonical templates
under references/, read in full before writing this):
  inquire / adr / cc_handoff — numbered §N sections (unchanged from repo-side
      general contract): §0 Rule-0 path+anchor, §4 falsifiable hypothesis
      (broadened framing), §5 forbidden-moves list, §6 gate verdict (soft
      WARN), §10 runnable fenced hook. cc_handoff additionally requires §0.5
      and the four-state status taxonomy in §6.
  notice — numbered §N (references/notice_log.md: §0,1,2,3,4,10; §5
      conditional on a HOLD routing decision). §0 is explicitly "one line,
      not a verified-commit list" (notice_log.md:14) so the repo-path+anchor
      check does NOT apply here — only presence/non-emptiness. §4 is a
      GRADUATE / DROP / HOLD routing decision, not a falsifiable hypothesis.
  audit — numbered §N (references/audit_note.md: §0,1,2,3,4,5,6,7,10,11). §0
      DOES cite concrete artifacts with commit hashes / page IDs
      (audit_note.md:16-19), so the standard repo-path+anchor check applies.
      §4 is root-cause analysis, not a falsifiable hypothesis, so no
      falsifier/forbidden-moves/gate-verdict checks apply.
  lesson — NOT numbered sections at all (references/lesson_capture.md is
      keyed on named headings: "Pattern", "Anchor incidents", "Repair /
      discipline rule", "Audit hooks" required; "Promotion record" /
      "Retirement" required only when the header `**Status:**` field says
      Standing rule / Retired respectively — SKILL.md trap #9's dollar-anchor
      quality check stays judgment-only, per SKILL.md's own text).
  light-tier ADR — named headings Decision / Grounds / Reads / Gate /
      Boundary (docs/adr/2026-08-08-adr-ceremony-tiering.md; SKILL.md:124,230).
      Gate and Boundary may legitimately read literally "none" — that is NOT
      ceremonial for this type, unlike the general is_light_tier() light-tier
      short-circuit repo-side uses to skip these types outright. A soft WARN
      fires if the body exceeds the ~300-word guideline (SKILL.md's own
      language is a shape guideline, not named as a HARD gate, and a false
      MALFORMED trains authors to ignore the checker — the exact defect this
      ADR fixed for repo-side).
  lock — the `lock` authoring type was deleted 2026-08-08 (SKILL.md:71: "Do
      not author new lock-decision briefs") and no reference template
      survives in this repo's history to derive a full section contract from
      (confirmed: `references/lock_decision.md` does not exist in-repo, only
      as a deploy-target-only "extra" per the 2026-08-27 ADR §0 Step 2 sync
      diff). This is a real "beyond references/*.md" gap for this ONE
      back-compat-only type — handled with a deliberately narrow, honestly-
      documented content check (see check_lock()) rather than either a false
      NOT CHECKED decline (which the ADR forbids) or an invented multi-section
      contract this session cannot verify against a real template.
  closure — delegates to check_closure_disposition.py, same as repo-side;
      not part of the ADR's decision text but kept for CLI parity so this
      script is a strict superset of repo-side's coverage, never a regression.

Exit codes (same convention as repo-side):
  0 — well-formed (WARN-level issues may still have printed), or a
      self-test/list-checks invocation that completed
  1 — one or more HARD violations, or a failing --self-test
  2 — usage / file-not-found error
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

SKILL_ROOT = Path(__file__).resolve().parent.parent  # .../brief-authoring/
REFERENCES_DIR = SKILL_ROOT / "references"

# Repo top-level dirs / extensions that mark a token as a concrete repo path.
REPO_PATH_PREFIXES = (
    "docs/", "config/", "ops/", "core/", "lab/", "data/", "tests/", "scripts/",
    ".claude/", "archive/", "analysis/", "strategies/", "reports/",
)
REPO_PATH_EXTS = (
    ".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
    ".sh", ".bat", ".csv",
)

# Numbered section heading, e.g. "## §0 — Rule 0" or "## 4. Falsifier".
_SECTION_RE = re.compile(
    r"^\s{0,3}#{1,4}\s+"
    r"(?:§\s*|section\s+|sec\.\s*)?"
    r"(?P<num>\d+(?:\.\d+)?)"
    r"\b",
    re.IGNORECASE | re.MULTILINE,
)
# Any markdown heading (numbered or named) — used for header-keyed types.
_NAMED_HEADING_RE = re.compile(r"^\s{0,3}#{1,4}\s+(?P<title>[^\n]+)$", re.MULTILINE)

_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S", re.MULTILINE)

_HYPOTHESIS_RE = re.compile(r"\bH\s*:|\bhypothesis\b|^\s*\*?\*?H\b", re.IGNORECASE | re.MULTILINE)
_FALSIFIER_RE = re.compile(r"\bfalsifi", re.IGNORECASE)
_REVERT_TRIGGER_RE = re.compile(r"\brevert\s+trigger\b", re.IGNORECASE)
_IF_THEN_RE = re.compile(r"\bif\b[^.\n]{0,200}?\bthen\b", re.IGNORECASE | re.DOTALL)
_REJECT_ACCEPT_RE = re.compile(r"\b(reject|accept)\b[^.\n]{0,40}\bif\b", re.IGNORECASE)

_VERDICT_RE = re.compile(r"\bRESOLVED\b|\bFALSIFIED\b|\bAMBIGUOUS\b")
_HANDOFF_STATUS_TOKENS = ("DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED")

# §4 routing decision keywords (notice_log.md §4 "Routing decision").
_NOTICE_ROUTING_RE = re.compile(r"\b(GRADUATE|DROP|HOLD)\b", re.IGNORECASE)

# Markdown pipe-table (header row + a `---`-style separator row) — used by the
# best-effort `lock` content check (see check_lock()).
_TABLE_RE = re.compile(r"^[ \t]*\|.+\|[ \t]*\n[ \t]*\|[\s:|-]+\|[ \t]*$", re.MULTILINE)

# Required §N sections per numbered-section type.
GENERAL_REQUIRED = ("0", "1", "4", "5", "6", "10")
NOTICE_REQUIRED = ("0", "1", "2", "3", "4", "10")
AUDIT_REQUIRED = ("0", "1", "2", "3", "4", "5", "6", "7", "10", "11")

# Required named headings for the two header-keyed types.
LESSON_NAMED_REQUIRED = ("pattern", "anchor incidents", "repair", "audit hooks")
LIGHT_NAMED_REQUIRED = ("decision", "grounds", "reads")
LIGHT_NAMED_ALLOW_NONE = ("gate", "boundary")  # present required; "none" is legitimate content
LIGHT_WORD_LIMIT = 300

# The complete skill-side type vocabulary (7 live types + the closure delegate
# + the retired-but-still-accepted `lock` back-compat alias).
ACCEPTED_TYPES = (
    "inquire", "adr", "cc_handoff", "notice", "lesson", "audit", "lock", "closure",
)
_CLOSURE_DELEGATE_TYPE = "closure"

_LIGHT_TIER_RE = re.compile(r"^\*\*Tier:\*\*\s*light\b", re.IGNORECASE | re.MULTILINE)


def _header_block(text: str) -> str:
    """Everything before the first `## ` heading — see is_light_tier()."""
    return re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]


def is_light_tier(text: str) -> bool:
    """True if the header block self-declares `**Tier:** light` (ADR
    2026-08-08-adr-ceremony-tiering.md). Header-scoped so a document *about*
    the tiering convention that quotes the phrase in prose is not misread."""
    return bool(_LIGHT_TIER_RE.search(_header_block(text)))


def _header_field(text: str, name: str) -> str | None:
    """Value of a `**<name>:**` header field (first match, header block only),
    or None if absent. Used for the lesson type's Status-conditional checks."""
    m = re.search(
        rf"^\*\*{re.escape(name)}:\*\*\s*(.+)$",
        _header_block(text),
        re.IGNORECASE | re.MULTILINE,
    )
    return m.group(1).strip() if m else None


class Violation(NamedTuple):
    severity: str   # "HARD" or "WARN"
    section: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity}: {self.section} | {self.message}"


# ── Numbered-section parsing (shared by inquire/adr/cc_handoff/notice/audit) ──

def _mask_fences(text: str) -> str:
    """Blank fenced code-block *content* (length/newlines preserved) so a
    `# 1. ...` comment inside a fence is never mistaken for a heading."""
    def _blank(m: re.Match) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    return _FENCE_RE.sub(_blank, text)


def split_sections(text: str) -> dict[str, str]:
    """{section_number: body_text} for every `§N`-style heading, in doc order.
    First occurrence of a repeated number wins. Heading positions are found on
    a fence-masked copy; bodies are sliced from the ORIGINAL text so §10's
    fence-detection still sees real fences."""
    matches = list(_SECTION_RE.finditer(_mask_fences(text)))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        num = m.group("num")
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        nl = body.find("\n")
        body = body[nl + 1:] if nl != -1 else ""
        if num not in sections:
            sections[num] = body
    return sections


def split_named_sections(text: str) -> list[tuple[str, str]]:
    """[(heading_title, body), ...] for EVERY markdown heading (numbered or
    named), in doc order — used for lesson/light-tier's header-keyed contract
    where sections are identified by title substring, not a §N scheme."""
    matches = list(_NAMED_HEADING_RE.finditer(_mask_fences(text)))
    out: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        title = m.group("title").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((title, text[start:end]))
    return out


def _find_named(sections: list[tuple[str, str]], keyword: str) -> str | None:
    """Body of the first heading whose title contains `keyword` (case-
    insensitive substring). None if no heading matches."""
    kw = keyword.lower()
    for title, body in sections:
        if kw in title.lower():
            return body
    return None


def _is_empty_body(body: str) -> bool:
    """A section body is 'empty' if only whitespace, markdown rules, or a
    TBD/N-A/none/todo placeholder remain — the ceremonial-section trap."""
    stripped = body.strip()
    if not stripped:
        return True
    lines = [ln.strip() for ln in stripped.splitlines()]
    content = [ln for ln in lines if ln and not set(ln) <= set("-—=*_ ")]
    if not content:
        return True
    joined = " ".join(content).lower()
    placeholder_only = re.sub(r"[^a-z]", "", joined)
    return placeholder_only in ("tbd", "na", "none", "tba", "todo")


def _is_blank(body: str) -> bool:
    """True only for genuinely blank content — no placeholder-word matching.
    Used for light-tier Gate/Boundary, where a literal 'none' IS legitimate
    content (SKILL.md: 'Boundary and Gate may be `none`'), unlike everywhere
    else in this checker where 'none' reads as a ceremonial placeholder."""
    return not body.strip()


# ── §0 repo-path + anchor (shared: inquire/adr/cc_handoff/audit) ──────────

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


_COMMIT_ANCHOR_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
_DATE_ANCHOR_RE = re.compile(r"last[- ]modified|\b20\d{2}-\d{2}-\d{2}\b", re.IGNORECASE)
_BARE_PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_./\-]+")


def _section0_cites_repo_path(body: str) -> bool:
    for m in _MD_LINK_RE.finditer(body):
        target = m.group(1).split(" ", 1)[0].split("#", 1)[0]
        if _looks_like_repo_path(target):
            return True
    for m in _INLINE_CODE_RE.finditer(body):
        tok = m.group(1).strip()
        for word in tok.split():
            word = word.split("#", 1)[0]
            if _looks_like_repo_path(word):
                return True
    for word in _BARE_PATH_TOKEN_RE.findall(body):
        if _looks_like_repo_path(word.split("#", 1)[0]):
            return True
    return False


def _section0_has_anchor(body: str) -> bool:
    return bool(_COMMIT_ANCHOR_RE.search(body) or _DATE_ANCHOR_RE.search(body))


def _check_section0_paths(sections: dict[str, str]) -> list[Violation]:
    body = sections.get("0")
    if body is None or _is_empty_body(body):
        return []
    if not _section0_cites_repo_path(body):
        return [Violation("HARD", "§0",
                          "Rule-0 reads cite no concrete repo path "
                          "(need e.g. `dd_protection.py` or `docs/adr/...`)")]
    if not _section0_has_anchor(body):
        return [Violation("HARD", "§0",
                          "Rule-0 path citation has no anchor "
                          "(commit hash or date / last-modified)")]
    return []


# ── Shared numbered-section content checks ────────────────────────────────

def _check_required_sections(sections: dict[str, str], required: tuple[str, ...]) -> list[Violation]:
    out: list[Violation] = []
    for num in required:
        if num not in sections:
            out.append(Violation("HARD", f"§{num}", "required section missing"))
        elif _is_empty_body(sections[num]):
            out.append(Violation("WARN", f"§{num}",
                                  "section present but empty / placeholder (ceremonial)"))
    return out


def _check_falsifiable_hypothesis(sections: dict[str, str]) -> list[Violation]:
    """§4 needs a hypothesis AND a falsifier — OR one of the canonical
    alternative framings (Revert trigger / if-then / reject-accept-if), per
    ADR 2026-08-09's explicit broadening of this check."""
    body = sections.get("4")
    if body is None or _is_empty_body(body):
        return []
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
    body = sections.get("5")
    if body is None or _is_empty_body(body):
        return []
    if not _LIST_ITEM_RE.search(body):
        return [Violation("HARD", "§5",
                          "no forbidden moves listed (expected a bullet/numbered list)")]
    return []


def _check_fenced_section(sections: dict[str, str], key: str) -> list[Violation]:
    """A runnable audit-hook section must contain a fenced code block."""
    body = sections.get(key)
    if body is None or _is_empty_body(body):
        return []
    if not _FENCE_RE.search(body):
        return [Violation("HARD", f"§{key}",
                          "no runnable audit hook (expected a fenced ``` code block)")]
    return []


def _check_gate_verdicts(sections: dict[str, str]) -> list[Violation]:
    body = sections.get("6")
    if body is None or _is_empty_body(body):
        return []
    if not _VERDICT_RE.search(body):
        return [Violation("WARN", "§6",
                          "no binary verdict keyword "
                          "(RESOLVED / FALSIFIED / AMBIGUOUS) — gate may be vague")]
    return []


def _check_handoff_extras(sections: dict[str, str]) -> list[Violation]:
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


def _check_notice_routing(sections: dict[str, str]) -> list[Violation]:
    body = sections.get("4")
    if body is None or _is_empty_body(body):
        return []
    if not _NOTICE_ROUTING_RE.search(body):
        return [Violation("HARD", "§4",
                          "no routing decision (expected GRADUATE / DROP / HOLD, "
                          "per notice_log.md §4)")]
    return []


# ── Per-type check functions ───────────────────────────────────────────────

def check_general(text: str, handoff_extra: bool = False) -> list[Violation]:
    """inquire / adr / cc_handoff — the numbered-section general contract."""
    sections = split_sections(text)
    required = GENERAL_REQUIRED + (("0.5",) if handoff_extra else ())
    out = _check_required_sections(sections, required)
    out += _check_section0_paths(sections)
    out += _check_falsifiable_hypothesis(sections)
    out += _check_forbidden_moves(sections)
    out += _check_fenced_section(sections, "10")
    out += _check_gate_verdicts(sections)
    if handoff_extra:
        out += _check_handoff_extras(sections)
    return out


def check_notice(text: str) -> list[Violation]:
    """notice — numbered §N, but §0 has no repo-path contract and §4 is a
    routing decision, not a falsifiable hypothesis (notice_log.md read in
    full: §0 is explicitly 'one line, not a verified-commit list')."""
    sections = split_sections(text)
    required = list(NOTICE_REQUIRED)
    body4 = sections.get("4", "")
    if re.search(r"\bHOLD\b", body4, re.IGNORECASE):
        required.append("5")  # "§5 — If HOLD: re-check trigger" becomes owed
    out = _check_required_sections(sections, tuple(required))
    out += _check_notice_routing(sections)
    out += _check_fenced_section(sections, "10")
    return out


def check_audit(text: str) -> list[Violation]:
    """audit — numbered §N; §0 DOES cite concrete artifacts with commit
    hashes/page IDs (audit_note.md §0 example content), so the standard
    repo-path+anchor check applies; §4 is root-cause analysis, not a
    hypothesis, so no falsifier/forbidden-moves/gate-verdict checks."""
    sections = split_sections(text)
    out = _check_required_sections(sections, AUDIT_REQUIRED)
    out += _check_section0_paths(sections)
    out += _check_fenced_section(sections, "10")
    return out


def check_lesson(text: str) -> list[Violation]:
    """lesson — NOT numbered sections; keyed on named headings
    (lesson_capture.md read in full). Promotion record / Retirement are only
    owed when the header Status field says so. Dollar-anchor QUALITY (trap #9)
    stays judgment-only per SKILL.md's own text — not mechanically enforced
    here beyond requiring the section exist."""
    named = split_named_sections(text)
    out: list[Violation] = []
    for key in LESSON_NAMED_REQUIRED:
        body = _find_named(named, key)
        if body is None:
            out.append(Violation("HARD", key.title(), "required section missing"))
        elif _is_empty_body(body):
            out.append(Violation("WARN", key.title(),
                                  "section present but empty / placeholder (ceremonial)"))
    audit_body = _find_named(named, "audit hooks")
    if audit_body is not None and not _is_empty_body(audit_body) and not _FENCE_RE.search(audit_body):
        out.append(Violation("HARD", "Audit Hooks",
                              "no runnable hook (expected a fenced ``` code block)"))
    status = _header_field(text, "Status")
    if status:
        if re.search(r"\bstanding rule\b", status, re.IGNORECASE):
            promo = _find_named(named, "promotion record")
            if promo is None or _is_empty_body(promo):
                out.append(Violation("HARD", "Promotion Record",
                                      "Status = Standing rule requires a populated "
                                      "Promotion record section"))
        if re.search(r"\bretired\b", status, re.IGNORECASE):
            retire = _find_named(named, "retirement")
            if retire is None or _is_empty_body(retire):
                out.append(Violation("HARD", "Retirement",
                                      "Status = Retired requires a populated "
                                      "Retirement section"))
    return out


def check_light(text: str) -> list[Violation]:
    """light-tier ADR — named headings Decision/Grounds/Reads/Gate/Boundary
    (docs/adr/2026-08-08-adr-ceremony-tiering.md; SKILL.md:124,230). Gate and
    Boundary may legitimately read 'none' — see _is_blank(). Word-count is a
    soft WARN only: the ADR this file implements exists specifically because
    a false HARD MALFORMED on a correctly-formed artifact trains authors to
    ignore the checker."""
    named = split_named_sections(text)
    out: list[Violation] = []
    for key in LIGHT_NAMED_REQUIRED:
        body = _find_named(named, key)
        if body is None:
            out.append(Violation("HARD", key.title(), "required section missing"))
        elif _is_empty_body(body):
            out.append(Violation("WARN", key.title(),
                                  "section present but empty / placeholder (ceremonial)"))
    for key in LIGHT_NAMED_ALLOW_NONE:
        body = _find_named(named, key)
        if body is None:
            out.append(Violation("HARD", key.title(), "required section missing"))
        elif _is_blank(body):
            out.append(Violation("WARN", key.title(),
                                  "section present but blank (a literal 'none' is "
                                  "legitimate content for this section; truly empty is not)"))
    body_start = re.search(r"^## ", text, re.MULTILINE)
    body_text = text[body_start.start():] if body_start else text
    word_count = len(re.findall(r"\S+", body_text))
    if word_count > LIGHT_WORD_LIMIT:
        out.append(Violation("WARN", "body",
                              f"light-tier body is {word_count} words "
                              f"(guideline: <= {LIGHT_WORD_LIMIT})"))
    return out


def check_lock(text: str) -> list[Violation]:
    """lock — retired 2026-08-08 (SKILL.md:71), back-compat alias only. No
    reference template survives in-repo to derive a full contract from (the
    2026-08-27 ADR's own sync diff shows `lock_decision.md` as deploy-target-
    only, never repo-side). Repo-side's own docstring records the one fact we
    DO have about its shape: '§4 is a trigger/threshold TABLE (\"Binary
    triggers that supersede this lock\")'. This check is deliberately narrow
    and honestly scoped to that one fact plus the same broadened falsifier
    framings general briefs accept — NOT a full section contract, because
    inventing headings/required-sections beyond what a surviving artifact
    supports would be exactly the 'applying a contract we do not own' failure
    this ADR exists to stop."""
    has_table = bool(_TABLE_RE.search(text))
    has_framing = bool(
        _REVERT_TRIGGER_RE.search(text)
        or _IF_THEN_RE.search(text)
        or _REJECT_ACCEPT_RE.search(text)
        or (_HYPOTHESIS_RE.search(text) and _FALSIFIER_RE.search(text))
    )
    if not (has_table or has_framing):
        return [Violation(
            "HARD", "§4",
            "lock records need either a binary trigger/threshold TABLE "
            "('Binary triggers that supersede this lock') or a canonical "
            "falsifier framing (Revert trigger / if-then / reject-accept-if / "
            "H:+falsifier)",
        )]
    return []


# ── Type inference ──────────────────────────────────────────────────────

_HEADER_FIELD_RE = re.compile(
    r"^\*\*(Loop|Brief type|Type):\*\*\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
_INQUIRE_DECL_RE = re.compile(r"^\s*inquire(?:-style|-phase|-light)?\b", re.IGNORECASE)
_HANDOFF_READY_BRIEF_RE = re.compile(r"\bbrief,\s*cc-handoff-ready\b", re.IGNORECASE)
_HANDOFF_DECL_RE = re.compile(
    r"\b(?:cc[/\s-]*cursor|cursor|cc)[\s-]+handoff\b(?!-ready)", re.IGNORECASE,
)


def _declared_type_from_header(text: str) -> str | None:
    head = _header_block(text)
    saw_handoff = False
    for m in _HEADER_FIELD_RE.finditer(head):
        value = m.group(2)
        if _INQUIRE_DECL_RE.match(value) or _HANDOFF_READY_BRIEF_RE.search(value):
            return "inquire"
        if _HANDOFF_DECL_RE.search(value):
            saw_handoff = True
    if saw_handoff:
        return "cc_handoff"
    return None


def infer_type(path: Path, text: str) -> str:
    """Best-effort type inference when --type is omitted.

    Precedence: header self-declaration > ID-field self-declaration
    (**Audit ID:** / **Notice ID:** / **Lesson ID:**, read straight off each
    template's own header) > filename/path hints > four-state taxonomy body
    sniff > 'adr' default (SKILL.md: 'When in doubt, default to ADR')."""
    declared = _declared_type_from_header(text)
    if declared is not None:
        return declared
    head = _header_block(text)
    if re.search(r"\*\*Audit ID:\*\*", head):
        return "audit"
    if re.search(r"\*\*Notice ID:\*\*", head):
        return "notice"
    if re.search(r"\*\*Lesson ID:\*\*", head):
        return "lesson"
    name = path.name.lower()
    path_str = str(path).lower()
    if "handoff" in name or "cc-handoff" in name or "spawn" in name:
        return "cc_handoff"
    if "0.5" in split_sections(text) or all(t in text for t in _HANDOFF_STATUS_TOKENS):
        return "cc_handoff"
    if "closure" in name or "closures" in path_str or re.search(r"CLOSURE:\s*`", text[:2000]):
        return "closure"
    if name.startswith("adr") or "adr" in name or re.search(r"^#\s*adr\b", text[:400].lower()):
        return "adr"
    return "adr"


# ── Top-level run ──────────────────────────────────────────────────────

def check_brief(text: str, brief_type: str) -> list[Violation]:
    """Dispatch to the requested type's OWN section contract. Light-tier
    detection wins regardless of requested type (a light ADR authored with
    --type adr still gets the light contract, matching the header it actually
    declares) — same precedence repo-side uses, but here light means REAL
    checks, not a skip."""
    if is_light_tier(text):
        return check_light(text)
    if brief_type == _CLOSURE_DELEGATE_TYPE:
        return []
    if brief_type == "lesson":
        return check_lesson(text)
    if brief_type == "lock":
        return check_lock(text)
    if brief_type == "notice":
        return check_notice(text)
    if brief_type == "audit":
        return check_audit(text)
    if brief_type == "cc_handoff":
        return check_general(text, handoff_extra=True)
    # inquire / adr / any unrecognized value: general contract (SKILL.md
    # "When in doubt, default to ADR" — the structure forces falsifier and
    # forbidden moves, which catch most ceremony).
    return check_general(text, handoff_extra=False)


def emit_report(path: Path, brief_type: str, violations: list[Violation]) -> int:
    hard = [v for v in violations if v.severity == "HARD"]
    warn = [v for v in violations if v.severity == "WARN"]
    print(f"check_brief (skill-side canonical): {path}  (type={brief_type})")
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


# ── --self-test ─────────────────────────────────────────────────────────

# (type, template filename) for every canonical template this script models.
# `closure` is included for CLI-parity coverage even though check_brief()
# trivially returns [] for it (delegated to check_closure_disposition.py).
SELF_TEST_TEMPLATES = (
    ("inquire", "inquire_brief.md"),
    ("adr", "adr.md"),
    ("cc_handoff", "cc_handoff.md"),
    ("notice", "notice_log.md"),
    ("lesson", "lesson_capture.md"),
    ("audit", "audit_note.md"),
    ("closure", "closure_record.md"),
)


def run_self_test() -> int:
    """Structural regression guard: run this checker against its own 7
    canonical templates and assert every section THE TEMPLATE ACTUALLY HAS is
    recognized as present, under the right type's contract.

    Deliberately NOT a "the raw template passes every HARD check" assertion —
    the templates are unfilled fill-in-the-blank documents (placeholders like
    `<hash>`, `NNN`, `YYYY-MM-DD`), so content-fidelity checks such as the §0
    anchor requirement (added 2026-08-20, after the 2026-08-09 canon ruling
    this file implements) are EXPECTED to fire on them — that is the checker
    correctly refusing to treat a placeholder as a real anchor, not a defect.
    A 'required section missing' violation is different in kind: it means
    this checker's section-detection or per-type required-section list
    disagrees with what the template itself actually contains, which IS a
    real regression. Only that category fails self-test; other HARD/WARN
    findings are printed as expected content-quality notes."""
    ok = True
    for brief_type, fname in SELF_TEST_TEMPLATES:
        path = REFERENCES_DIR / fname
        if not path.exists():
            print(f"SELF-TEST SKIP: {fname} not found at {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        violations = check_brief(text, brief_type)
        hard = [v for v in violations if v.severity == "HARD"]
        missing = [v for v in hard if "required section missing" in v.message]
        expected = [v for v in hard if v not in missing]
        status = "PASS" if not missing else "FAIL"
        if missing:
            ok = False
        print(f"SELF-TEST {status}: {fname} (type={brief_type}) "
              f"{len(missing)} missing-section HARD (regression), "
              f"{len(expected)} content-quality HARD (expected on a blank "
              f"template), {len(violations) - len(hard)} WARN")
        for v in missing:
            print(f"    REGRESSION: {v}")
        for v in expected:
            print(f"    expected (blank-template placeholder): {v}")
    print("SELF-TEST: " + ("ALL PASS (no section-detection regressions)" if ok else "FAILURES ABOVE"))
    return 0 if ok else 1


def print_list_checks() -> None:
    print("check_brief.py (skill-side canonical) — per-type section contracts:")
    print("  inquire / adr / cc_handoff : numbered §N; §0 path+anchor, §4 falsifiable")
    print("                               hypothesis (broadened framing), §5 forbidden")
    print("                               moves list, §6 gate verdict (WARN), §10 fenced")
    print("                               hook. cc_handoff adds §0.5 + status taxonomy.")
    print("  notice                     : numbered §N (0,1,2,3,4,10; 5 iff HOLD). §0 is")
    print("                               presence-only (no path+anchor). §4 is a")
    print("                               GRADUATE/DROP/HOLD routing decision.")
    print("  audit                      : numbered §N (0,1,2,3,4,5,6,7,10,11). §0 IS")
    print("                               path+anchor-checked. No falsifier/forbidden-")
    print("                               moves/gate-verdict checks (§4 is root cause).")
    print("  lesson                     : named headings (Pattern, Anchor incidents,")
    print("                               Repair, Audit hooks required; Promotion")
    print("                               record / Retirement iff Status says so).")
    print("  light-tier ADR             : named headings Decision/Grounds/Reads")
    print("                               (required) + Gate/Boundary (may read 'none').")
    print("                               Body >300 words is a soft WARN.")
    print("  lock (retired, back-compat): best-effort content check only — see")
    print("                               check_lock()'s docstring for why.")
    print("  closure                    : delegates to check_closure_disposition.py.")
    print("See docs/adr/2026-08-09-check-brief-canon-ruling.md for the skill-vs-repo split.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("brief", type=Path, nargs="?", help="path to the brief markdown file")
    parser.add_argument("--type", choices=list(ACCEPTED_TYPES), default=None, metavar="TYPE",
                        help="inquire|adr|cc_handoff|notice|lesson|audit|lock|closure. "
                             "Default: infer from header Loop/Type/ID fields, then "
                             "filename/content.")
    parser.add_argument("--self-test", action="store_true",
                        help="run against this skill's own 7 canonical templates")
    parser.add_argument("--list-checks", action="store_true",
                        help="print the per-type section-contract summary and exit")
    args = parser.parse_args(argv)

    if args.list_checks:
        print_list_checks()
        return 0
    if args.self_test:
        return run_self_test()

    if args.brief is None:
        parser.error("brief path is required unless --self-test or --list-checks is given")
        return 2  # pragma: no cover — parser.error() exits before this

    if not args.brief.exists():
        print(f"brief not found: {args.brief}", file=sys.stderr)
        return 2
    if not args.brief.is_file():
        print(f"not a file: {args.brief}", file=sys.stderr)
        return 2

    text = args.brief.read_text(encoding="utf-8", errors="replace")
    brief_type = args.type or infer_type(args.brief, text)

    if brief_type == _CLOSURE_DELEGATE_TYPE:
        print("note: closure records are gated by "
              "scripts/check_closure_disposition.py, not this checker.",
              file=sys.stderr)
        print(f"check_brief (skill-side canonical): {args.brief}  (type=closure)")
        print("RESULT: DELEGATED — run: "
              f"python scripts/check_closure_disposition.py {args.brief}")
        return 0

    if is_light_tier(text):
        print("note: light-tier decision record (ADR 2026-08-08-adr-ceremony-tiering) — "
              "Decision/Grounds/Reads/Gate/Boundary contract applied, not the numbered "
              "§0-§10 ADR contract.", file=sys.stderr)

    violations = check_brief(text, brief_type)
    return emit_report(args.brief, brief_type, violations)


if __name__ == "__main__":
    sys.exit(main())
