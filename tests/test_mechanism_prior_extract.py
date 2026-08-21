from pathlib import Path

from lab.research_utils.mechanism_prior_extract import load_entries, split_entries

SAMPLE = """# Rejected portfolio candidates

Some preamble text that is not an entry.

## Entries

### First entry title -- FALSIFIED

**Rejection scope:** blah blah.
**Closure date:** 2026-08-13

<!-- concept-intake-entry instrument="MNQ" -->

### Second entry title -- STAGE-1 FAIL

**Rejection scope:** other blah.

## Domain-level SNAG closures

### A domain rollup that must be excluded

**Scope:** spans many instruments -- not a per-candidate entry.

## Queryable index (concept-intake gate, added 2026-06-05)

### Third entry title -- from the index section

**Rejection scope:** index-section blah.

## Audit hooks

### Not a candidate either

Mechanical check text, also excluded.
"""


def test_split_entries_ignores_preamble_before_first_section():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "First entry title -- FALSIFIED" in titles
    assert all("not an entry" not in e.body for e in entries)


def test_split_entries_captures_title_and_body():
    entries = split_entries(SAMPLE)
    first = entries[0]
    assert first.title == "First entry title -- FALSIFIED"
    assert "Rejection scope" in first.body
    assert "concept-intake-entry" in first.body


def test_split_entries_excludes_domain_level_and_audit_sections():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "A domain rollup that must be excluded" not in titles
    assert "Not a candidate either" not in titles


def test_split_entries_includes_queryable_index_section():
    entries = split_entries(SAMPLE)
    titles = [e.title for e in entries]
    assert "Third entry title -- from the index section" in titles


def test_split_entries_assigns_stable_source_refs_across_included_sections_only():
    entries = split_entries(SAMPLE)
    # 3 included entries total (Entries x2 + Queryable index x1); excluded
    # sections never consume a source_ref, so numbering has no gaps.
    assert [e.source_ref for e in entries] == ["entry-1", "entry-2", "entry-3"]


def test_split_entries_last_entry_in_a_section_runs_to_next_section_boundary():
    entries = split_entries(SAMPLE)
    first = entries[0]
    assert "Second entry title" not in first.body


def test_split_entries_empty_text_returns_empty_list():
    assert split_entries("# Rejected portfolio candidates\n\nNo entries here.") == []


def test_load_entries_reads_real_file(tmp_path):
    p = tmp_path / "rejected.md"
    p.write_text(SAMPLE, encoding="utf-8")
    entries = load_entries(p)
    assert len(entries) == 3
