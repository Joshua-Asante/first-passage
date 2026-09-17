"""Shared brief parsing and numbered checks; wrappers own coverage and reporting."""
from __future__ import annotations

import re
from typing import Callable, NamedTuple


REPO_PATH_PREFIXES = (
    "docs/", "config/", "ops/", "core/", "lab/", "data/", "tests/", "scripts/",
    ".claude/", "archive/", "analysis/", "strategies/", "reports/",
)


REPO_PATH_EXTS = (
    ".py", ".md", ".toml", ".pine", ".json", ".yml", ".yaml",
    ".sh", ".bat", ".csv",
)


_SECTION_RE = re.compile(
    r"^\s{0,3}#{1,4}\s+"
    r"(?:§\s*|section\s+|sec\.\s*)?"
    r"(?P<num>\d+(?:\.\d+)?)"
    r"\b",
    re.IGNORECASE | re.MULTILINE,
)


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


_COMMIT_ANCHOR_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


_DATE_ANCHOR_RE = re.compile(r"last[- ]modified|\b20\d{2}-\d{2}-\d{2}\b", re.IGNORECASE)


_BARE_PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9_./\-]+")


_LIGHT_TIER_RE = re.compile(r"^\*\*Tier:\*\*\s*light\b", re.IGNORECASE | re.MULTILINE)


_CONCISE_ADR_RE = re.compile(r"^\*\*Format:\*\*\s*concise\b", re.IGNORECASE | re.MULTILINE)


GENERAL_REQUIRED = ("0", "1", "4", "5", "6", "10")


def _header_block(text: str) -> str:
    """Everything before the first `## ` heading — see is_light_tier()."""
    return re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]


def is_light_tier(text: str) -> bool:
    """True if the header block self-declares `**Tier:** light` (ADR
    2026-08-08-adr-ceremony-tiering.md). Header-scoped so a document *about*
    the tiering convention that quotes the phrase in prose is not misread."""
    return bool(_LIGHT_TIER_RE.search(_header_block(text)))


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


class Violation(NamedTuple):
    severity: str   # "HARD" or "WARN"
    section: str
    message: str

    def __str__(self) -> str:
        return f"{self.severity}: {self.section} | {self.message}"



class NumberedChecks(NamedTuple):
    is_empty: Callable[[str], bool]

    def _check_required_sections(self, sections: dict[str, str], required: tuple[str, ...]) -> list[Violation]:
        out: list[Violation] = []
        for num in required:
            if num not in sections:
                out.append(Violation("HARD", f"§{num}", "required section missing"))
            elif self.is_empty(sections[num]):
                out.append(Violation("WARN", f"§{num}",
                                      "section present but empty / placeholder (ceremonial)"))
        return out


    def _check_section0_paths(self, sections: dict[str, str]) -> list[Violation]:
        body = sections.get("0")
        if body is None or self.is_empty(body):
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


    def _check_falsifiable_hypothesis(self, sections: dict[str, str]) -> list[Violation]:
        """§4 needs a hypothesis AND a falsifier — OR one of the canonical
        alternative framings (Revert trigger / if-then / reject-accept-if), per
        .claude/skills/brief-authoring/SKILL.md#checker-ownership."""
        body = sections.get("4")
        if body is None or self.is_empty(body):
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


    def _check_forbidden_moves(self, sections: dict[str, str]) -> list[Violation]:
        body = sections.get("5")
        if body is None or self.is_empty(body):
            return []
        if not _LIST_ITEM_RE.search(body):
            return [Violation("HARD", "§5",
                              "no forbidden moves listed (expected a bullet/numbered list)")]
        return []


    def _check_fenced_section(self, sections: dict[str, str], key: str) -> list[Violation]:
        """A runnable audit-hook section must contain a fenced code block."""
        body = sections.get(key)
        if body is None or self.is_empty(body):
            return []
        if not _FENCE_RE.search(body):
            return [Violation("HARD", f"§{key}",
                              "no runnable audit hook (expected a fenced ``` code block)")]
        return []


    def _check_gate_verdicts(self, sections: dict[str, str]) -> list[Violation]:
        body = sections.get("6")
        if body is None or self.is_empty(body):
            return []
        if not _VERDICT_RE.search(body):
            return [Violation("WARN", "§6",
                              "no binary verdict keyword "
                              "(RESOLVED / FALSIFIED / AMBIGUOUS) — gate may be vague")]
        return []


    def _check_handoff_extras(self, sections: dict[str, str]) -> list[Violation]:
        out: list[Violation] = []
        body6 = sections.get("6")
        if body6 is not None and not self.is_empty(body6):
            present = [t for t in _HANDOFF_STATUS_TOKENS if t in body6]
            if len(present) < len(_HANDOFF_STATUS_TOKENS):
                missing = [t for t in _HANDOFF_STATUS_TOKENS if t not in present]
                out.append(Violation("HARD", "§6",
                                    "CC-handoff status taxonomy incomplete; missing "
                                    + ", ".join(missing)))
        return out
