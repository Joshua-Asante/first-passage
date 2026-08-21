"""Split docs/rejected_candidates.md into individually-taggable entries.

The file is organized into several `##` sections. Most contain individual
per-candidate closure records (in a shared prose-field shape); two are
DOMAIN-LEVEL rollups (a whole research theme closed or bar-raised,
spanning many instruments as one record) rather than per-candidate
entries, and are excluded by name -- see the Rule-0 note in Task 6 of the
implementation plan for the verified current section list and why a
denylist (not an allowlist) is used. This module does no classification --
only splitting and locating -- see mechanism_prior_ingest.py and Task 7 of
the implementation plan for the LLM tagging step that consumes this output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SECTION_HEADING_RE = re.compile(r"^## (.+)$", re.MULTILINE)
ENTRY_HEADING_RE = re.compile(r"^### (.+)$", re.MULTILINE)

# Domain-level rollups and meta/process sections are NOT per-candidate
# entries. Denylist, not allowlist, so a future new per-candidate section
# (e.g. "Harness-fed rejections" once populated) is picked up automatically.
EXCLUDED_SECTIONS = {
    "Domain-level SNAG closures",
    "Domain-level tail-exhaustion raised bars",
    "Audit hooks",
}


@dataclass(frozen=True)
class RawEntry:
    title: str
    body: str
    source_ref: str  # e.g. "entry-1" -- stable, order-based identifier


def split_entries(markdown_text: str) -> list[RawEntry]:
    """Return one RawEntry per `### ` heading, across every `##` section
    except EXCLUDED_SECTIONS.

    Text before the first `## ` section (front-matter, registry preamble)
    is never treated as an entry. source_ref numbering is continuous
    across included sections only -- an excluded section never consumes
    a number, so there are no gaps.
    """
    sections = [(m.start(), m.group(1).strip()) for m in SECTION_HEADING_RE.finditer(markdown_text)]
    sections.append((len(markdown_text), None))  # sentinel end boundary

    entries: list[RawEntry] = []
    counter = 0
    for (start, name), (end, _) in zip(sections, sections[1:]):
        if name in EXCLUDED_SECTIONS:
            continue
        section_text = markdown_text[start:end]
        headings = list(ENTRY_HEADING_RE.finditer(section_text))
        for i, match in enumerate(headings):
            counter += 1
            title = match.group(1).strip()
            body_start = match.end()
            body_end = headings[i + 1].start() if i + 1 < len(headings) else len(section_text)
            body = section_text[body_start:body_end].strip()
            entries.append(RawEntry(title=title, body=body, source_ref=f"entry-{counter}"))
    return entries


def load_entries(path: Path) -> list[RawEntry]:
    return split_entries(path.read_text(encoding="utf-8"))
