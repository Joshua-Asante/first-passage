"""Structural tests for docs/methodology/LESSONS_INDEX.jsonl.

These do NOT re-verify lesson content against source prose (that was a
one-time transcription, not something a fast test can check) -- they pin
the structural invariants a stale or hand-edited-out-of-sync file would
violate: well-formed JSONL, unique IDs (the exact M-25/M-19 collision class
this index exists to prevent), no fabricated content on stub entries, and
that every full entry's full_ref anchor actually resolves in the cited file.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "docs" / "methodology" / "LESSONS_INDEX.jsonl"


def _load_entries() -> list[dict]:
    lines = INDEX_PATH.read_text(encoding="utf-8").splitlines()
    return [json.loads(ln) for ln in lines if ln.strip()]


def test_index_file_exists_and_nonempty():
    assert INDEX_PATH.is_file()
    assert INDEX_PATH.read_text(encoding="utf-8").strip()


def test_every_line_is_valid_json():
    for i, ln in enumerate(INDEX_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        if not ln.strip():
            continue
        try:
            json.loads(ln)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"line {i} is not valid JSON: {exc}") from exc


def test_ids_are_unique():
    entries = _load_entries()
    ids = [e["id"] for e in entries]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate lesson IDs (the M-25/M-19-shaped collision this index exists to prevent): {dupes}"


def test_required_fields_present_on_every_entry():
    required = {
        "id", "class", "status", "status_note", "title", "one_line_lesson",
        "cost_if_repeated", "trigger_globs", "trigger_keywords", "full_ref",
        "siblings", "content_verified", "last_verified_date",
    }
    for e in _load_entries():
        missing = required - set(e)
        assert not missing, f"{e.get('id')}: missing fields {missing}"


def test_full_entries_carry_real_content():
    for e in _load_entries():
        if e["content_verified"]:
            assert e["title"], f"{e['id']}: content_verified=True but title is empty"
            assert e["one_line_lesson"], f"{e['id']}: content_verified=True but one_line_lesson is empty"
            assert e["cost_if_repeated"], f"{e['id']}: content_verified=True but cost_if_repeated is empty"


def test_stub_entries_carry_no_fabricated_content():
    """The whole point of the stub/full split: a stub entry must not smuggle in
    invented lesson content under the appearance of a verified one."""
    for e in _load_entries():
        if not e["content_verified"]:
            assert e["title"] is None, f"{e['id']}: stub entry must not have a title"
            assert e["one_line_lesson"] is None, f"{e['id']}: stub entry must not have one_line_lesson"
            assert e["cost_if_repeated"] is None, f"{e['id']}: stub entry must not have cost_if_repeated"
            assert e.get("citing_files"), f"{e['id']}: stub entry must cite where it was actually found"


def test_siblings_and_memory_twins_reference_real_ids():
    entries = _load_entries()
    known_ids = {e["id"] for e in entries}
    for e in entries:
        for sib in e.get("siblings") or []:
            assert sib in known_ids, f"{e['id']}: sibling {sib!r} is not a known lesson ID"
        twin = e.get("memory_twin")
        if twin:
            assert twin in known_ids, f"{e['id']}: memory_twin {twin!r} is not a known lesson ID"


_ANCHOR_RE = re.compile(r"^(?P<path>[^#]+)#(?P<anchor>.+)$")


def _slugify(heading: str) -> str:
    """Approximate GitHub's markdown-heading-anchor slugification.

    GitHub strips punctuation (an em-dash disappears, not collapses to one
    hyphen) then replaces each remaining space with its own hyphen -- so
    "E1 — Trust" (dash flanked by two spaces) becomes "e1--trust" (double
    hyphen), not "e1-trust". Consecutive spaces are NOT collapsed first.
    """
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s", "-", s)
    return s


def test_full_entry_refs_resolve_to_a_real_heading_in_the_cited_file():
    for e in _load_entries():
        if not e["content_verified"]:
            continue
        ref = e["full_ref"]
        m = _ANCHOR_RE.match(ref)
        if not m:
            continue  # no anchor to check (shouldn't happen for full entries, but don't hard-fail on it)
        path = REPO_ROOT / m.group("path")
        assert path.is_file(), f"{e['id']}: full_ref path does not exist: {m.group('path')}"
        text = path.read_text(encoding="utf-8", errors="replace")
        headings = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
        slugs = {_slugify(h) for h in headings}
        assert m.group("anchor") in slugs, (
            f"{e['id']}: anchor {m.group('anchor')!r} does not match any heading slug in "
            f"{m.group('path')} (closest headings: {sorted(headings)[:5]})"
        )


def test_at_least_the_expected_full_entry_count():
    """Loose floor, not an exact pin -- guards against an accidental wholesale
    truncation of the generator's FULL list, not against adding more entries."""
    full = [e for e in _load_entries() if e["content_verified"]]
    assert len(full) >= 30, f"expected >=30 full entries, found {len(full)}"
