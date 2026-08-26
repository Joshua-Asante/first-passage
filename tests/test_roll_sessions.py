"""Tests for scripts/roll_sessions.py — the session-log roll-off tool.

Design: docs/spec/2026-06-27-session-log-rolloff-design.md
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

# scripts/ is not a package; load the module by path (stdlib-only module).
# Register in sys.modules before exec so dataclass introspection (Py3.14) resolves.
_REPO = Path(__file__).resolve().parents[1]
_PATH = _REPO / "scripts" / "roll_sessions.py"
_spec = importlib.util.spec_from_file_location("roll_sessions", _PATH)
rs = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = rs
_spec.loader.exec_module(rs)


# ── fixtures / helpers ────────────────────────────────────────────────────────

# Header includes the fenced template line `## YYYY-MM-DD — <focus title>`, which
# must NOT be parsed as an entry (literal YYYY, not digits).
HEADER = (
    "# Session Log\n"
    "\n"
    "Newest first. One entry per session.\n"
    "\n"
    "**Entry template:**\n"
    "```markdown\n"
    "## YYYY-MM-DD — <focus title>\n"
    "**Focus:** what the session set out to do.\n"
    "```\n"
    "\n"
    "---\n"
    "\n"
)


def _entry(date_str: str, title: str) -> str:
    return (
        f"## {date_str} — {title}\n"
        f"**Focus:** focus for {title}.\n"
        f"**Shipped:** shipped for {title}.\n"
    )


def _doc(entries: list[tuple[str, str]]) -> str:
    """entries: newest-first list of (YYYY-MM-DD, title)."""
    blocks = [_entry(d, t) for d, t in entries]
    return HEADER + "\n\n---\n\n".join(blocks) + "\n"


def _write(root: Path, text: str) -> Path:
    p = root / "docs" / "SESSIONS.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _read(root: Path) -> str:
    return (root / "docs" / "SESSIONS.md").read_text(encoding="utf-8")


def _git(root: Path, *args: str, when: str | None = None) -> None:
    env = dict(os.environ)
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    subprocess.run(["git", *args], cwd=root, check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _repo_with_history(root: Path, commits: list[tuple[str, list[tuple[str, str]]]]) -> None:
    """Build a real git repo whose commits add entries at controlled AUTHOR times.

    Real history rather than a monkeypatch: the whole mechanism under test is
    "git already knows which entry was authored later", so a fake would assert
    the design back to itself instead of testing it.
    """
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    for when, entries in commits:
        _write(root, _doc(entries))
        _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", f"entries @ {when}", when=when)


def _titles(text: str) -> list[str]:
    """Entry titles in file order. Goes through parse() rather than scanning for
    '## ', so the fenced `## YYYY-MM-DD` template in the header is excluded."""
    return [e.title for e in rs.parse(text)[1]]


needs_git = pytest.mark.skipif(
    shutil.which("git") is None, reason="git not on PATH")


def _archive(root: Path, quarter: str) -> Path:
    # Delegate to the tool's own path builder so the archive destination
    # (docs/ltm/notes/archive/sessions/, post-LTM-reorg) stays single-sourced.
    return rs.archive_file(root, quarter)


# ── parse / quarter ───────────────────────────────────────────────────────────

def test_parse_splits_header_and_entries_excluding_template():
    doc = _doc([("2026-06-03", "Title C"), ("2026-06-02", "Title B"), ("2026-06-01", "Title A")])
    header, entries = rs.parse(doc)
    assert "Entry template" in header
    assert "## YYYY-MM-DD" in header  # template stays in the header, not an entry
    assert len(entries) == 3
    assert entries[0].date == dt.date(2026, 6, 3)
    assert entries[0].title == "Title C"
    assert entries[2].date == dt.date(2026, 6, 1)


def test_quarter_of_boundaries():
    assert rs.quarter_of(dt.date(2026, 1, 1)) == "2026-Q1"
    assert rs.quarter_of(dt.date(2026, 4, 1)) == "2026-Q2"
    assert rs.quarter_of(dt.date(2026, 7, 1)) == "2026-Q3"
    assert rs.quarter_of(dt.date(2026, 12, 31)) == "2026-Q4"


def test_normalize_entry_removes_only_structural_divider():
    chunk = "## 2026-06-01 — Exact\nbody keeps trailing spaces  \n\n---\n\n"

    assert rs._normalize_entry(chunk) == (
        "## 2026-06-01 — Exact\nbody keeps trailing spaces  "
    )


def test_strip_trailing_debris_removes_doubled_separator_any_interleaving():
    # union-merge debris: extra blank lines / bare "---" lines in any order.
    text = "## 2026-06-01 — Exact\nbody line\n\n---\n\n---\n\n\n"
    assert rs._strip_trailing_debris(text) == "## 2026-06-01 — Exact\nbody line"


def test_strip_trailing_debris_noop_on_clean_entry():
    text = "## 2026-06-01 — Exact\nbody line"
    assert rs._strip_trailing_debris(text) == text


def test_normalize_removes_doubled_separators_without_reorder(tmp_path):
    # Two entries glued together with a doubled "---" (as left by a union
    # merge), same failure shape as the live docs/SESSIONS.md incidents.
    doc = (
        HEADER
        + _entry("2026-06-05", "E5")
        + "\n\n---\n\n---\n\n"
        + _entry("2026-06-04", "E4")
        + "\n"
    )
    _write(tmp_path, doc)
    changed = rs.normalize(tmp_path)
    assert changed is True
    out = _read(tmp_path)
    assert "---\n\n---" not in out
    _, entries = rs.parse(out)
    assert [e.title for e in entries] == ["E5", "E4"]


def test_normalize_is_idempotent(tmp_path):
    _write(tmp_path, _doc([("2026-06-05", "E5"), ("2026-06-04", "E4")]))
    rs.normalize(tmp_path)
    first = _read(tmp_path)
    changed_again = rs.normalize(tmp_path)
    assert changed_again is False
    assert _read(tmp_path) == first


def test_normalize_dry_run_reports_without_writing(tmp_path):
    doc = (
        HEADER
        + _entry("2026-06-05", "E5")
        + "\n\n---\n\n---\n\n"
        + _entry("2026-06-04", "E4")
        + "\n"
    )
    _write(tmp_path, doc)
    changed = rs.normalize(tmp_path, dry_run=True)
    assert changed is True
    assert _read(tmp_path) == doc  # untouched on disk


def test_normalize_reorder_stable_sorts_same_date_entries_keep_order(tmp_path):
    # An older-dated entry landed above a newer one (merge-order artifact);
    # --reorder should bring 06-05 above 06-04 while the two same-day 06-05
    # entries keep their on-disk relative order (date alone can't recover
    # same-day chronology).
    doc = _doc([
        ("2026-06-04", "Older"),
        ("2026-06-05", "Newer-A"),
        ("2026-06-05", "Newer-B"),
    ])
    _write(tmp_path, doc)
    rs.normalize(tmp_path, reorder=True)
    _, entries = rs.parse(_read(tmp_path))
    assert [e.title for e in entries] == ["Newer-A", "Newer-B", "Older"]


def test_archive_link_rewrite_rebases_only_relative_markdown_links():
    text = (
        "[brief](briefs/Q.md) [lab](../lab/analysis/x.md) "
        "[anchor](#section) [web](https://example.com/x)"
    )

    assert rs.rewrite_links_for_archive(text) == (
        "[brief](../../../../briefs/Q.md) "
        "[lab](../../../../../lab/analysis/x.md) "
        "[anchor](#section) [web](https://example.com/x)"
    )


# ── roll behavior ─────────────────────────────────────────────────────────────

def test_roll_keeps_newest_and_rolls_rest(tmp_path):
    _write(tmp_path, _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-02", "E2"), ("2026-06-01", "E1"),
    ]))
    res = rs.roll(tmp_path, keep_n=3)
    assert res["kept"] == 3 and res["rolled"] == 2
    _, kept = rs.parse(rs.split_index(_read(tmp_path))[0])
    assert [e.title for e in kept] == ["E5", "E4", "E3"]
    arch = _archive(tmp_path, "2026-Q2")
    assert arch.exists()
    _, arch_entries = rs.parse(arch.read_text(encoding="utf-8"))
    assert [e.title for e in arch_entries] == ["E2", "E1"]


def test_roll_refuses_to_duplicate_an_archived_heading(tmp_path):
    """2026-08-26 finding: naively rolling a live entry whose label already
    exists in the archive (different title, same YYYY-MM-DDx) creates a
    genuine duplicate heading INSIDE the archive file -- append_entries()
    only dedups by exact heading line, not by label. roll() must keep such
    an entry live past the cap rather than corrupt the archive."""
    _archive(tmp_path, "2026-Q2").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q2").write_text(
        "## 2026-06-01a — Already-archived entry\n**Focus:** f.\n", encoding="utf-8")
    _write(tmp_path, _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-01a", "Colliding live entry"),
    ]))
    res = rs.roll(tmp_path, keep_n=3)
    assert res["retained_collisions"] == ["2026-06-01a"]
    assert res["kept"] == 4  # 3 under the cap + the retained collision
    assert res["rolled"] == 0
    _, kept = rs.parse(rs.split_index(_read(tmp_path))[0])
    assert "Colliding live entry" in [e.title for e in kept]
    _, arch_entries = rs.parse(_archive(tmp_path, "2026-Q2").read_text(encoding="utf-8"))
    matching = [e for e in arch_entries if lettered_label_of_(e) == "2026-06-01a"]
    assert len(matching) == 1, "archive must not gain a second 2026-06-01a heading"


def lettered_label_of_(e) -> str:
    return rs.lettered_label_of(e.text.splitlines()[0])


def test_roll_preserves_every_entry_apart_from_link_rewrite(tmp_path):
    (tmp_path / "docs" / "briefs").mkdir(parents=True)
    (tmp_path / "docs" / "briefs" / "Q.md").write_text("brief", encoding="utf-8")
    (tmp_path / "lab").mkdir()
    (tmp_path / "lab" / "x.md").write_text("lab", encoding="utf-8")
    original = _doc([
        ("2026-06-03", "Kept"),
        ("2026-06-02", "Linked"),
        ("2026-06-01", "Oldest"),
    ]).replace(
        "**Shipped:** shipped for Linked.",
        "**Shipped:** [brief](briefs/Q.md) and [lab](../lab/x.md).",
    ).replace(
        "**Shipped:** shipped for Oldest.",
        "**Shipped:** final line keeps spaces.  ",
    )
    _write(tmp_path, original)
    _, before = rs.parse(original)

    rs.roll(tmp_path, keep_n=1)

    _, kept = rs.parse(rs.split_index(_read(tmp_path))[0])
    _, archived = rs.parse(_archive(tmp_path, "2026-Q2").read_text(encoding="utf-8"))
    after = {entry.title: entry.text for entry in kept + archived}
    expected = {
        entry.title: (
            entry.text
            if entry.title == "Kept"
            else rs.rewrite_links_for_archive(entry.text)
        )
        for entry in before
    }
    assert after == expected
    archive_parent = _archive(tmp_path, "2026-Q2").parent
    assert (archive_parent / "../../../../briefs/Q.md").resolve().is_file()
    assert (archive_parent / "../../../../../lab/x.md").resolve().is_file()


def test_roll_routes_by_quarter(tmp_path):
    _write(tmp_path, _doc([
        ("2026-05-01", "Q2b"), ("2026-04-15", "Q2a"),
        ("2026-03-10", "Q1b"), ("2026-02-01", "Q1a"),
    ]))
    rs.roll(tmp_path, keep_n=1)
    _, q2 = rs.parse(_archive(tmp_path, "2026-Q2").read_text(encoding="utf-8"))
    _, q1 = rs.parse(_archive(tmp_path, "2026-Q1").read_text(encoding="utf-8"))
    assert [e.title for e in q2] == ["Q2a"]            # Q2b kept (newest)
    assert [e.title for e in q1] == ["Q1b", "Q1a"]     # newest-first within file


def test_roll_noop_at_or_under_keep(tmp_path):
    original = _doc([("2026-06-03", "C"), ("2026-06-02", "B"), ("2026-06-01", "A")])
    _write(tmp_path, original)
    res = rs.roll(tmp_path, keep_n=3)
    assert res["rolled"] == 0
    assert _read(tmp_path) == original  # byte-identical, no index added
    assert not _archive(tmp_path, "2026-Q2").parent.exists()


def test_roll_idempotent(tmp_path):
    _write(tmp_path, _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-02", "E2"), ("2026-06-01", "E1"),
    ]))
    rs.roll(tmp_path, keep_n=3)
    sessions_1 = _read(tmp_path)
    arch_1 = _archive(tmp_path, "2026-Q2").read_text(encoding="utf-8")
    rs.roll(tmp_path, keep_n=3)
    assert _read(tmp_path) == sessions_1
    assert _archive(tmp_path, "2026-Q2").read_text(encoding="utf-8") == arch_1


def test_roll_migrates_legacy_archive_links_once(tmp_path):
    _write(tmp_path, _doc([("2026-07-01", "Current")]))
    archive = _archive(tmp_path, "2026-Q2")
    archive.parent.mkdir(parents=True)
    archive.write_text(
        "# Session archive — 2026-Q2\n\n"
        "Rolled from `docs/SESSIONS.md` (newest first).\n\n---\n\n"
        "## 2026-06-01 — Legacy\n"
        "**Shipped:** [brief](briefs/Q.md).\n",
        encoding="utf-8",
    )

    rs.roll(tmp_path, keep_n=1)
    migrated = archive.read_text(encoding="utf-8")
    assert rs.ARCHIVE_LINK_NOTE in migrated
    assert "[brief](../../../../briefs/Q.md)" in migrated

    first = migrated
    rs.roll(tmp_path, keep_n=1)
    assert archive.read_text(encoding="utf-8") == first


def test_regenerate_archives_from_source_restores_exact_entries(tmp_path):
    source = _doc([
        ("2026-07-03", "Current"),
        ("2026-07-02", "Q3 Rolled"),
        ("2026-06-02", "Linked"),
        ("2026-06-01", "Trailing"),
    ]).replace(
        "**Shipped:** shipped for Linked.",
        "**Shipped:** [brief](briefs/Q.md).",
    ).replace(
        "**Shipped:** shipped for Trailing.",
        "**Shipped:** keep these spaces.  ",
    ).replace(
        "**Shipped:** shipped for Q3 Rolled.\n\n\n---",
        "**Shipped:** shipped for Q3 Rolled.\n\n---",
    )
    _write(tmp_path, _doc([("2026-07-03", "Current")]))

    rs.regenerate_archives_from_source(tmp_path, source, keep_n=1)

    _, source_entries = rs.parse(source)
    archive_entries = []
    for quarter in ("2026-Q3", "2026-Q2"):
        archive_entries.extend(
            rs.parse(_archive(tmp_path, quarter).read_text(encoding="utf-8"))[1]
        )
    assert {entry.title: entry.text for entry in archive_entries} == {
        entry.title: rs.rewrite_links_for_archive(entry.text)
        for entry in source_entries[1:]
    }


def test_index_regenerated_from_archives(tmp_path):
    _write(tmp_path, _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-02", "Rolled Two"), ("2026-06-01", "Rolled One"),
    ]))
    rs.roll(tmp_path, keep_n=3)
    doc = _read(tmp_path)
    assert rs.INDEX_START in doc and rs.INDEX_END in doc
    idx = doc[doc.index(rs.INDEX_START):doc.index(rs.INDEX_END)]
    assert "2026-06-02" in idx and "Rolled Two" in idx
    assert "2026-06-01" in idx and "Rolled One" in idx
    assert "notes/archive/sessions/SESSIONS-2026-Q2.md" in idx
    # newest archived entry listed before the older one
    assert idx.index("Rolled Two") < idx.index("Rolled One")


def test_dry_run_writes_nothing(tmp_path):
    original = _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-02", "E2"), ("2026-06-01", "E1"),
    ])
    _write(tmp_path, original)
    res = rs.roll(tmp_path, keep_n=3, dry_run=True)
    assert res["rolled"] == 2
    assert _read(tmp_path) == original
    assert not _archive(tmp_path, "2026-Q2").exists()


def test_header_preserved_byte_for_byte(tmp_path):
    _write(tmp_path, _doc([
        ("2026-06-05", "E5"), ("2026-06-04", "E4"), ("2026-06-03", "E3"),
        ("2026-06-02", "E2"), ("2026-06-01", "E1"),
    ]))
    rs.roll(tmp_path, keep_n=3)
    after = _read(tmp_path)
    assert after.startswith(HEADER)  # header region unchanged


# ── same-date ordering (the merge=union trap) ─────────────────────────────────

SAME_DAY = "2026-07-31"
EARLY, LATE = f"{SAME_DAY}T09:00:00+00:00", f"{SAME_DAY}T15:00:00+00:00"


def _two_same_day(root: Path) -> None:
    """History: 'first' authored at 09:00, then 'second' added at 15:00 on top."""
    _repo_with_history(root, [
        (EARLY, [(SAME_DAY, "first")]),
        (LATE, [(SAME_DAY, "second"), (SAME_DAY, "first")]),
    ])


@needs_git
def test_check_order_flags_a_union_scrambled_same_day_pair(tmp_path):
    _two_same_day(tmp_path)
    _write(tmp_path, _doc([(SAME_DAY, "first"), (SAME_DAY, "second")]))  # scrambled
    problems = rs.check_order(tmp_path, window=5)
    assert len(problems) == 1
    assert "'first' sits above 'second'" in problems[0]


def test_check_order_flags_two_entries_sharing_one_date_letter_label(tmp_path):
    """The 2026-08-09g collision: two sessions independently pick the same letter.

    Union merge keeps both sides, `_dedup_by_heading` keys on the FULL heading
    line so differing titles are not deduped, and the order pass never inspects
    the letter — so a duplicate label reaches `main` through a merge git calls
    clean. No git history needed: this is a pure content property.
    """
    _write(tmp_path, _doc([("2026-08-09g", "sync"), ("2026-08-09g", "gsub")]))
    problems = rs.check_order(tmp_path, window=5)
    assert any("2026-08-09g" in p for p in problems), problems


def test_check_order_allows_distinct_letters_on_one_day(tmp_path):
    """Guard against a gate that fires on any same-day pair.

    Same-day entries are normal and expected; only a repeated *label* is the
    defect. Without this, the check above would pass just as well against a
    rule that banned same-day entries outright.
    """
    _write(tmp_path, _doc([("2026-08-09h", "later"), ("2026-08-09g", "earlier")]))
    assert rs.check_order(tmp_path, window=5) == []


# ── duplicate-label grandfathering (2026-08-16h vs append-only deadlock) ──────
#
# check_order's duplicate scan and check_append_only used to be jointly
# unsatisfiable for any duplicate that had already landed on main: order
# demands a rename, append-only forbids editing an already-committed
# heading. duplicate_labels()'s own docstring always meant to catch a *new*
# collision at merge time ("the only thing standing between a duplicate
# label and main") — the fix scopes it to that: a collision entirely inside
# history append-only already freezes is left as-is (and surfaced via
# grandfathered_duplicate_notes, never silently), while a genuinely new
# collision still fails exactly as before.


def test_duplicate_labels_grandfathers_a_collision_entirely_in_history():
    """No file needed; duplicate_labels is a pure function of entries + grandfathered."""
    entries = [
        rs.Entry(dt.date(2026, 8, 16), "S3", "## 2026-08-16h — S3\n**Focus:** f.\n"),
        rs.Entry(dt.date(2026, 8, 16), "DL-1", "## 2026-08-16h — DL-1\n**Focus:** f.\n"),
    ]
    grandfathered = {e.text.splitlines()[0] for e in entries}
    assert rs.duplicate_labels(entries, grandfathered=grandfathered) == []


def test_duplicate_labels_still_flags_a_new_collision_against_history():
    """A NEW heading colliding with an old, grandfathered label must still fail —
    grandfathering is not a blanket exemption for the label, only for the
    specific headings already frozen by append-only."""
    old = rs.Entry(dt.date(2026, 8, 16), "S3", "## 2026-08-16h — S3\n**Focus:** f.\n")
    new = rs.Entry(dt.date(2026, 8, 17), "New work", "## 2026-08-16h — New work\n**Focus:** f.\n")
    problems = rs.duplicate_labels([new, old], grandfathered={old.text.splitlines()[0]})
    assert problems, "gate went VACUOUS: a genuinely new collision was suppressed"
    assert "2026-08-16h" in problems[0]


def test_duplicate_labels_default_grandfathered_none_flags_everything():
    """No grandfather set (the historical call shape) behaves exactly as before."""
    entries = [
        rs.Entry(dt.date(2026, 8, 9), "sync", "## 2026-08-09g — sync\n**Focus:** f.\n"),
        rs.Entry(dt.date(2026, 8, 9), "gsub", "## 2026-08-09g — gsub\n**Focus:** f.\n"),
    ]
    assert rs.duplicate_labels(entries) != []


# ── archive-scan (2026-08-26 finding: docs/ltm/ is search-index-excluded, so
# duplicate_labels()/check_order() never saw an already-archived label and 7
# real live-vs-archive collisions landed undetected) ──────────────────────────

def test_archived_headings_reads_every_quarterly_archive_file(tmp_path):
    _archive(tmp_path, "2026-Q2").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q2").write_text(
        "## 2026-06-01a — Old A\n**Focus:** f.\n", encoding="utf-8")
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-07-01b — Old B\n**Focus:** f.\n", encoding="utf-8")
    headings = rs.archived_headings(tmp_path)
    assert "## 2026-06-01a — Old A" in headings
    assert "## 2026-07-01b — Old B" in headings


def test_archived_headings_empty_when_no_archive_dir(tmp_path):
    assert rs.archived_headings(tmp_path) == set()


def test_archived_labels_extracts_lettered_tokens(tmp_path):
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-24g — Old G\n**Focus:** f.\n"
        "## 2026-08-24\n**Focus:** bare, no letter — excluded.\n",
        encoding="utf-8")
    assert rs.archived_labels(tmp_path) == {"2026-08-24g"}


def test_archive_collisions_flags_live_entry_matching_archived_label(tmp_path):
    """The exact 2026-08-26 failure shape: a live heading reuses a letter an
    archived heading already claimed for the same date."""
    entries = [rs.Entry(dt.date(2026, 8, 24), "New work",
                         "## 2026-08-24g — New work\n**Focus:** f.\n")]
    problems = rs.archive_collisions(entries, {"2026-08-24g"})
    assert problems, "gate went VACUOUS: a live/archive collision was not caught"
    assert "2026-08-24g" in problems[0]


def test_archive_collisions_clean_when_no_overlap(tmp_path):
    entries = [rs.Entry(dt.date(2026, 8, 24), "New work",
                         "## 2026-08-24z — New work\n**Focus:** f.\n")]
    assert rs.archive_collisions(entries, {"2026-08-24g"}) == []


def test_archive_collisions_noop_with_no_archived_labels():
    entries = [rs.Entry(dt.date(2026, 8, 24), "New work",
                         "## 2026-08-24g — New work\n**Focus:** f.\n")]
    assert rs.archive_collisions(entries, set()) == []


def test_archived_letters_for_date_scoped_to_the_requested_day(tmp_path):
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-24g — Same day\n**Focus:** f.\n"
        "## 2026-08-25a — Different day\n**Focus:** f.\n",
        encoding="utf-8")
    assert rs.archived_letters_for_date(tmp_path, dt.date(2026, 8, 24)) == {"g"}
    assert rs.archived_letters_for_date(tmp_path, dt.date(2026, 8, 26)) == set()


def test_archive_internal_duplicate_labels_flags_two_distinct_headings(tmp_path):
    """The exact 2026-08-26 finding: the same label used by two DIFFERENT
    headings within the archive itself (title differs, label collides) --
    distinct from a live-vs-archive collision, and from an exact-duplicate
    heading that ``archived_headings()``'s set would already collapse."""
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-23m — First entry\n**Focus:** f.\n"
        "## 2026-08-23m — Unrelated second entry\n**Focus:** f.\n",
        encoding="utf-8")
    notes = rs.archive_internal_duplicate_labels(tmp_path)
    assert len(notes) == 1, notes
    assert "2026-08-23m" in notes[0]
    assert "First entry" in notes[0] and "Unrelated second entry" in notes[0]


def test_archive_internal_duplicate_labels_clean_on_exact_duplicate_heading(tmp_path):
    """An exact byte-identical duplicate heading (same title too) collapses
    to one entry in the underlying set -- nothing to flag."""
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-23m — Same entry\n**Focus:** f.\n"
        "## 2026-08-23m — Same entry\n**Focus:** g.\n",
        encoding="utf-8")
    assert rs.archive_internal_duplicate_labels(tmp_path) == []


def test_archive_internal_duplicate_labels_clean_with_no_collisions(tmp_path):
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-23m — Entry\n**Focus:** f.\n"
        "## 2026-08-23n — Different entry\n**Focus:** f.\n",
        encoding="utf-8")
    assert rs.archive_internal_duplicate_labels(tmp_path) == []


def test_check_order_cli_notes_an_archive_internal_duplicate(tmp_path, capsys):
    _write(tmp_path, _doc([("2026-08-24", "Live entry, unrelated")]))
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-23m — First archived entry\n**Focus:** f.\n"
        "## 2026-08-23m — Second archived entry\n**Focus:** f.\n",
        encoding="utf-8")
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "NOTE:" in out and "2026-08-23m" in out and "archive-internal" in out


def test_check_order_cli_notes_but_passes_an_archive_collision(tmp_path, capsys):
    """WARN-tier, not blocking, same posture as a grandfathered live-vs-live
    duplicate: fixing a live/archive collision may need a same-day letter the
    a-z scheme cannot supply (2026-08-26 finding), so this gate surfaces it
    visibly rather than either hiding it or force-failing every commit until
    a label-scheme decision is made."""
    _write(tmp_path, _doc([("2026-08-24", "Live entry reusing an archived letter")]))
    # _doc's single same-day entry is bare (claims 'a'-equivalent has no letter
    # suffix); give it an explicit letter matching the archived one instead.
    doc = _read(tmp_path).replace(
        "## 2026-08-24 — Live entry reusing an archived letter",
        "## 2026-08-24g — Live entry reusing an archived letter",
    )
    _write(tmp_path, doc)
    _archive(tmp_path, "2026-Q3").parent.mkdir(parents=True, exist_ok=True)
    _archive(tmp_path, "2026-Q3").write_text(
        "## 2026-08-24g — Already-archived entry\n**Focus:** f.\n", encoding="utf-8")
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "NOTE:" in out and "2026-08-24g" in out and "archive" in out


def test_grandfathered_duplicate_notes_reports_only_fully_grandfathered_collisions():
    old = rs.Entry(dt.date(2026, 8, 16), "S3", "## 2026-08-16h — S3\n**Focus:** f.\n")
    old2 = rs.Entry(dt.date(2026, 8, 16), "DL-1", "## 2026-08-16h — DL-1\n**Focus:** f.\n")
    new = rs.Entry(dt.date(2026, 8, 17), "New", "## 2026-08-17a — New\n**Focus:** f.\n")
    grandfathered = {old.text.splitlines()[0], old2.text.splitlines()[0]}
    notes = rs.grandfathered_duplicate_notes([new, old, old2], grandfathered)
    assert len(notes) == 1
    assert "2026-08-16h" in notes[0]
    assert "append-only" in notes[0]
    # A non-duplicate label (the new entry) never generates a note.
    assert "2026-08-17a" not in notes[0]


@needs_git
def test_check_order_reconciles_with_append_only_on_a_committed_duplicate(tmp_path):
    """The real deadlock, reproduced: a duplicate label already on HEAD must pass
    check_order AND check_append_only simultaneously when left untouched, and
    check_order must still catch a fresh collision layered on top."""
    _repo_with_history(tmp_path, [
        ("2026-08-16T21:45:00-04:00", [
            ("2026-08-16h", "DL-1 train scoring executed"),
            ("2026-08-16h", "S3 WHO-drought relief"),
        ]),
    ])
    # Untouched working tree: both gates must pass together.
    assert rs.check_order(tmp_path, window=5) == []
    assert rs.check_append_only(tmp_path) == []

    # Layering a brand-new entry that reuses the SAME stale label is still a
    # real, newly introduced collision and must still fail.
    _write(tmp_path, _doc([
        ("2026-08-16h", "third entry, new collision"),
        ("2026-08-16h", "DL-1 train scoring executed"),
        ("2026-08-16h", "S3 WHO-drought relief"),
    ]))
    problems = rs.check_order(tmp_path, window=5)
    assert any("2026-08-16h" in p for p in problems), problems


def test_check_order_cli_flags_a_duplicate_with_no_history_to_consult(tmp_path, capsys):
    """No git history here (plain tmp_path) -> nothing can be grandfathered ->
    still fails, exactly the pre-existing content-only behaviour this augments,
    never weakens, when history is unavailable."""
    _write(tmp_path, _doc([("2026-08-16h", "DL-1"), ("2026-08-16h", "S3")]))
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "duplicate session label" in out


@needs_git
def test_check_order_cli_notes_but_passes_a_grandfathered_duplicate(tmp_path, capsys):
    """Visible-restraint: a suppressed pre-existing duplicate must still be seen
    in the CLI output, not vanish into a silently clean-looking pass."""
    _repo_with_history(tmp_path, [
        ("2026-08-16T21:45:00-04:00", [
            ("2026-08-16h", "DL-1 train scoring executed"),
            ("2026-08-16h", "S3 WHO-drought relief"),
        ]),
    ])
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "NOTE:" in out and "2026-08-16h" in out and "pre-existing duplicate" in out


def test_check_order_allows_several_bare_dated_entries_on_one_day(tmp_path):
    """Bare same-day entries are a supported shape, not a collision.

    This file orders same-day entries by author time and `reorder` exists to
    sort exactly that case, so requiring a letter would break the mechanism.
    Only a repeated *letter* claims a duplicate identity. Pinned because the
    first cut of the label check banned this and three existing tests caught it.
    """
    _write(tmp_path, _doc([("2026-08-09", "second"), ("2026-08-09", "first")]))
    assert rs.duplicate_labels(rs.parse(_read(tmp_path))[1]) == []


@needs_git
def test_reorder_fixes_what_a_date_only_sort_cannot(tmp_path):
    """The regression this whole change exists for.

    Both entries share a date, so the previous date-only sort was a no-op on
    them — it is the case union always produces, and it was never covered.
    """
    _two_same_day(tmp_path)
    scrambled = _doc([(SAME_DAY, "first"), (SAME_DAY, "second")])
    _write(tmp_path, scrambled)

    # What the old behaviour did: stable date sort leaves it exactly as-is.
    _, entries = rs.parse(scrambled)
    date_only = sorted(entries, key=lambda e: e.date, reverse=True)
    assert [e.title for e in date_only] == ["first", "second"], "date sort is a no-op here"

    assert rs.normalize(tmp_path, reorder=True, window=5) is True
    assert _titles(_read(tmp_path)) == ["second", "first"]
    assert rs.check_order(tmp_path, window=5) == []


@needs_git
def test_reorder_is_a_pure_move_and_never_edits_a_body(tmp_path):
    _two_same_day(tmp_path)
    _write(tmp_path, _doc([(SAME_DAY, "first"), (SAME_DAY, "second")]))
    # Compare canonical bodies: normalize also strips trailing separator debris,
    # which is its other job, and conflating the two would hide a real rewrite.
    canon = lambda doc: {e.title: rs._strip_trailing_debris(e.text)
                         for e in rs.parse(doc)[1]}
    before = canon(_read(tmp_path))
    rs.normalize(tmp_path, reorder=True, window=5)
    after = canon(_read(tmp_path))
    assert before == after, "reorder must move whole entries, not rewrite them"
    assert _titles(_read(tmp_path)) == ["second", "first"], "and it did reorder"


@needs_git
def test_reorder_leaves_settled_entries_below_the_window_alone(tmp_path):
    """Repair scope == detection scope. A full sort would move hand-placed
    historical entries; measured on the real file, that was 9 of them —
    including one whose heading reads '2026-07-29 (later)'.

    The two below-window entries must be authored at DIFFERENT times and sit
    in the order a full sort would flip, or this asserts nothing: entries from
    one commit share a key and a full sort leaves them put regardless.
    """
    old_day = "2026-07-20"
    t_a, t_b = f"{old_day}T09:00:00+00:00", f"{old_day}T17:00:00+00:00"
    old = [(old_day, "older-a"), (old_day, "older-b")]
    rev = [(old_day, "older-b"), (old_day, "older-a")]
    _repo_with_history(tmp_path, [
        (t_a, [(old_day, "older-a")]),
        (t_b, rev),                                   # older-b authored LATER
        (EARLY, [(SAME_DAY, "first")] + rev),
        (LATE, [(SAME_DAY, "second"), (SAME_DAY, "first")] + rev),
    ])
    # On disk older-a sits above older-b — "wrong" by author time, so a
    # whole-file sort would flip it. It is below the window, so it must not.
    _write(tmp_path, _doc([(SAME_DAY, "first"), (SAME_DAY, "second")] + old))
    rs.normalize(tmp_path, reorder=True, window=2)
    titles = _titles(_read(tmp_path))
    assert titles[:2] == ["second", "first"], "window repaired"
    assert titles[2:] == ["older-a", "older-b"], "below-window order untouched"


@needs_git
def test_a_brand_new_uncommitted_entry_sorts_newest(tmp_path):
    _two_same_day(tmp_path)
    _write(tmp_path, _doc([(SAME_DAY, "second"), (SAME_DAY, "first"), (SAME_DAY, "draft")]))
    rs.normalize(tmp_path, reorder=True, window=5)
    assert _titles(_read(tmp_path))[0] == "draft"


def test_order_check_degrades_to_pass_without_git_history(tmp_path):
    """Shallow clone / CI: report nothing rather than block or guess.

    Same posture as the Pine manifest gate on a clone with no .pine present.
    """
    _write(tmp_path, _doc([(SAME_DAY, "first"), (SAME_DAY, "second")]))
    assert rs.order_keys(tmp_path, rs.parse(_read(tmp_path))[1]) is None
    assert rs.check_order(tmp_path, window=5) == []
    # …and reorder falls back to the date-only sort instead of scrambling.
    rs.normalize(tmp_path, reorder=True, window=5)
    assert _titles(_read(tmp_path)) == ["first", "second"]


# ── 2026-08-08 stranding regressions (letter suffix + merge + gate) ───────────


def _rich_entry(date_str: str, title: str, *, live_ops: str = "c1 warm/disarmed") -> str:
    """Entry with Live-ops — the field reorder previously dropped."""
    return (
        f"## {date_str} — {title}\n"
        f"**Focus:** focus for {title}.\n"
        f"**Shipped:** shipped for {title}.\n"
        f"**Decisions/defects:** none.\n"
        f"**Open / next:** next for {title}.\n"
        f"**Live-ops state:** {live_ops}.\n"
    )


def test_parse_accepts_same_day_letter_suffixes():
    """Same-day sessions use ## YYYY-MM-DDb / c headings; they are real entries."""
    doc = (
        HEADER
        + _rich_entry("2026-08-08c", "Charlie")
        + "\n\n---\n\n"
        + _rich_entry("2026-08-08b", "Bravo")
        + "\n\n---\n\n"
        + _rich_entry("2026-08-08", "Plain")
        + "\n"
    )
    header, entries = rs.parse(doc)
    assert "2026-08-08c" not in header
    assert [e.text.splitlines()[0] for e in entries] == [
        "## 2026-08-08c — Charlie",
        "## 2026-08-08b — Bravo",
        "## 2026-08-08 — Plain",
    ]
    assert [e.date for e in entries] == [dt.date(2026, 8, 8)] * 3
    assert [e.title for e in entries] == ["Charlie", "Bravo", "Plain"]
    assert all("**Live-ops state:**" in e.text for e in entries)


@needs_git
def test_reorder_merge_same_day_suffixes_does_not_sink_unresolved(tmp_path):
    """Regression: union-merge + --normalize --reorder stranded same-day entries.

    Simulates the 2026-08-08 incident shape: plain / ``b`` / ``c`` same-day
    headings plus an older row; author-time resolution fails (merge-shaped).
    Reorder must not sink 08-08 under 08-05, and must keep each body
    (incl. Live-ops) byte-identical.
    """
    day, older = "2026-08-08", "2026-08-05"
    # Commit history as if two sides landed (plain @10:00, b @13:12), then a
    # working-tree-only ``c`` — without relying on git's union merge option.
    _repo_with_history(tmp_path, [
        (f"{older}T09:00:00-04:00", [(older, "Settled")]),
        (f"{day}T10:00:00-04:00", [(day, "Plain-ADR"), (older, "Settled")]),
        (f"{day}T13:12:50-04:00", [
            (f"{day}b", "Bravo-R2"), (day, "Plain-ADR"), (older, "Settled"),
        ]),
    ])
    # Patch _entry-based history with rich bodies for the scramble step.
    scrambled = (
        HEADER
        + _rich_entry(older, "Settled") + "\n\n---\n\n"
        + _rich_entry(day, "Plain-ADR") + "\n\n---\n\n"
        + _rich_entry(f"{day}b", "Bravo-R2") + "\n\n---\n\n"
        + _rich_entry(f"{day}c", "Charlie-new") + "\n"
    )
    _write(tmp_path, scrambled)
    before_bodies = {
        e.text.splitlines()[0]: rs._strip_trailing_debris(e.text)
        for e in rs.parse(scrambled)[1]
    }
    assert len(before_bodies) == 4

    real_intro = rs.intro_times
    rs.intro_times = lambda root, wanted: {}  # merge-shaped: nothing resolvable
    try:
        rs.normalize(tmp_path, reorder=True, window=12)
        out = _read(tmp_path)
        _, after = rs.parse(out)
        titles = [e.title for e in after]
        for a, b in zip(after, after[1:]):
            assert a.date >= b.date, (a.title, b.title)
        settled_i = titles.index("Settled")
        assert titles.index("Plain-ADR") < settled_i
        assert titles.index("Bravo-R2") < settled_i
        assert titles.index("Charlie-new") < settled_i
        after_bodies = {
            e.text.splitlines()[0]: rs._strip_trailing_debris(e.text)
            for e in after
        }
        for h, body in before_bodies.items():
            assert after_bodies[h] == body
            assert "**Live-ops state:**" in after_bodies[h]
        assert out.count("\n\n---\n\n") >= 3
    finally:
        rs.intro_times = real_intro


@needs_git
def test_check_order_flags_date_inversion_beyond_top_window(tmp_path):
    """Top-12-only check green-lit the 2026-08-08 stranding; full-file must catch it."""
    day, older = "2026-08-08", "2026-08-05"
    decoys = [(older, f"D{i}") for i in range(13)]
    # Single commit → identical author times inside the window (no author-time noise).
    _repo_with_history(tmp_path, [(f"{older}T12:00:00-04:00", decoys)])
    _write(tmp_path, _doc(decoys + [(day, "Stranded-ADR")]))
    assert rs.check_order(tmp_path, window=12)  # must not be blind below the window
    blob = " ".join(rs.check_order(tmp_path, window=12))
    assert "Stranded-ADR" in blob or "2026-08-08" in blob or "date" in blob.lower()


def test_duplicate_label_remediation_does_not_send_you_to_reorder(tmp_path, capsys):
    """`--reorder` is a pure move; it cannot renumber a label.

    Printing it as *the* fix for a collision sends the reader to a command that
    silently no-ops on their actual problem — the failure mode this whole gate
    exists to end. The label case must name renumbering instead.
    """
    _write(tmp_path, _doc([("2026-08-09g", "sync"), ("2026-08-09g", "gsub")]))
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "renumber" in out.lower()
    assert "--reorder" not in out
    assert "roll_sessions.py --next-label <date>" in out


def test_check_order_printer_encoding_safe_on_cp1252(tmp_path, monkeypatch):
    """Failure path used to UnicodeEncodeError on Windows cp1252 consoles (→)."""
    _write(tmp_path, _doc([
        ("2026-08-05", "Older"),
        ("2026-08-08", "Accept \u2192 build"),
    ]))
    monkeypatch.setattr(rs, "check_order", lambda root, window=12: [
        "'Accept \u2192 build' sits above 'Older', but was authored earlier"
    ])

    class _Cp1252:
        encoding = "cp1252"

        def write(self, s):
            if isinstance(s, str):
                s.encode(self.encoding)
            return len(s) if isinstance(s, str) else 0

        def flush(self):
            pass

    monkeypatch.setattr(sys, "stdout", _Cp1252())
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    assert rc == 1


# ── --next-label same-day allocator ───────────────────────────────────────────


def test_next_label_no_entries_prints_a_first(tmp_path, capsys):
    """a-first convention (2026-08-10): empty day → first suffix is ``a``."""
    _write(tmp_path, _doc([("2026-08-01", "other-day")]))
    rc = rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "a"


def test_next_label_bare_plus_b_through_d_prints_e(tmp_path, capsys):
    """Bare claims the ``a`` slot (08-08 shape); bare + b..d → ``e``."""
    _write(tmp_path, _doc([
        ("2026-08-11d", "D"),
        ("2026-08-11c", "C"),
        ("2026-08-11b", "B"),
        ("2026-08-11", "Bare"),
    ]))
    rc = rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "e"


def test_next_label_gap_fills_first_free(tmp_path, capsys):
    """Gaps are filled: a,c claimed → ``b`` (checker-acceptable; only dupes fail)."""
    _write(tmp_path, _doc([("2026-08-11c", "C"), ("2026-08-11a", "A")]))
    rc = rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "b"


def test_next_label_non_date_exits_2(tmp_path, capsys):
    _write(tmp_path, _doc([("2026-08-11a", "A")]))
    rc = rs.main(["--next-label", "not-a-date", "--root", str(tmp_path)])
    assert rc == 2
    err = capsys.readouterr().out.lower()
    assert "yyyy-mm-dd" in err
    assert "not-a-date" in err


def test_next_label_is_read_only(tmp_path, capsys):
    original = _doc([("2026-08-11a", "A")])
    _write(tmp_path, original)
    assert rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "b"
    assert _read(tmp_path) == original  # SESSIONS.md untouched (claim is outside repo)


# ── separator structure (union-merge splice) ───────────────────────────────────


def _doc_missing_separator_between(
    entries: list[tuple[str, str]], *, glue: str = "\n",
) -> str:
    """Like _doc but join entries with ``glue`` instead of ENTRY_SEPARATOR.

    ``glue="\\n"`` reproduces the 2026-08-11y/x/w splice: a heading lands
    directly under the prior entry's Live-ops line with no ``---`` rule.
    """
    blocks = [_entry(d, t) for d, t in entries]
    return HEADER + glue.join(blocks) + "\n"


def test_separator_problems_flags_missing_rule_between_entries():
    doc = _doc_missing_separator_between([
        ("2026-08-11y", "Y"),
        ("2026-08-11x", "X"),
        ("2026-08-11w", "W"),
    ])
    problems = rs.separator_problems(doc)
    assert len(problems) == 2, problems
    assert all("missing --- separator" in p for p in problems)
    assert any("'X'" in p for p in problems)
    assert any("'W'" in p for p in problems)


def test_check_order_flags_missing_separators(tmp_path):
    """The gate that already runs at pre-commit must catch the splice shape.

    Before this check, ``--check-order`` returned [] on the live 2026-08-11
    file while ``--normalize`` would have rewritten the separators — so the
    failure mode was silent at every wired gate.
    """
    _write(tmp_path, _doc_missing_separator_between([
        ("2026-08-11y", "Y"),
        ("2026-08-11x", "X"),
    ]))
    problems = rs.check_order(tmp_path, window=5)
    assert any("missing --- separator" in p for p in problems), problems


def test_structure_ok_on_clean_doc(tmp_path):
    """Clean docs must not fail the new separator limb (no false positives)."""
    _write(tmp_path, _doc([("2026-08-11b", "B"), ("2026-08-11a", "A")]))
    assert rs.structure_problems(_read(tmp_path)) == []
    # Distinct letters + proper --- rules → gate silent even without git history.
    assert rs.separator_problems(_read(tmp_path)) == []
    assert rs.duplicate_labels(rs.parse(_read(tmp_path))[1]) == []


def test_missing_separator_remediation_names_normalize_not_reorder(tmp_path, capsys):
    _write(tmp_path, _doc_missing_separator_between([
        ("2026-08-11b", "B"),
        ("2026-08-11a", "A"),
    ]))
    rc = rs.main(["--check-order", "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "--normalize" in out
    # Pure separator fault: do not send the reader to --reorder.
    assert "--reorder" not in out


def test_normalize_repairs_missing_separators_without_touching_bodies(tmp_path):
    doc = _doc_missing_separator_between([
        ("2026-08-11y", "Y"),
        ("2026-08-11x", "X"),
    ])
    _write(tmp_path, doc)
    before = {e.title: rs._strip_trailing_debris(e.text) for e in rs.parse(doc)[1]}
    assert rs.normalize(tmp_path, reorder=False) is True
    out = _read(tmp_path)
    assert rs.structure_problems(out) == []
    after = {e.title: rs._strip_trailing_debris(e.text) for e in rs.parse(out)[1]}
    assert before == after
    assert rs.ENTRY_SEPARATOR in out


# ── same-clone --next-label claim markers ─────────────────────────────────────


def test_next_label_second_invocation_skips_claimed_letter(tmp_path, capsys, monkeypatch):
    """Same-clone concurrency: second --next-label must not re-issue the first.

    Cross-clone / cloud sessions still collide (markers live in the process
    temp dir, not the repo); this only cheapens the within-clone failure mode.
    """
    # Isolate claim dir from other tests sharing the same tmp root pattern.
    claim_root = tmp_path / "claims"
    monkeypatch.setattr(rs, "claim_dir_for", lambda root: claim_root / "c")
    _write(tmp_path, _doc([("2026-08-11a", "A")]))
    assert rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "b"
    assert rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "c"
    assert "claim marker" in captured.err.lower() or "reserve" in captured.err.lower()


def test_next_label_no_claim_ignores_markers(tmp_path, capsys, monkeypatch):
    claim_root = tmp_path / "claims"
    monkeypatch.setattr(rs, "claim_dir_for", lambda root: claim_root / "c")
    _write(tmp_path, _doc([("2026-08-11a", "A")]))
    assert rs.main(["--next-label", "2026-08-11", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "b"
    # --no-claim sees only the file → still "b", and does not reserve further.
    assert rs.main([
        "--next-label", "2026-08-11", "--no-claim", "--root", str(tmp_path),
    ]) == 0
    assert capsys.readouterr().out.strip() == "b"


def test_read_claimed_letters_ignores_expired(tmp_path):
    day = dt.date(2026, 8, 11)
    cdir = tmp_path / "c"
    path = rs.write_label_claim(cdir, day, "u")
    stale = time.time() - (rs._CLAIM_TTL_SEC + 60)
    os.utime(path, (stale, stale))
    assert rs.read_claimed_letters(cdir, day) == set()
    assert rs.read_claimed_letters(
        cdir, day, now=stale + 10, ttl_sec=rs._CLAIM_TTL_SEC,
    ) == {"u"}


# ── append-only (packet 1: freeze prior entry bodies) ─────────────────────────
# Union merge keeps both sides' added lines. The 2026-08-13z/13y nesting was a
# prior Open/next line absorbing a new heading. Append-only keys by heading:
# new headings may appear; a heading that existed on the base must keep its body.


def test_append_only_allows_a_new_top_entry():
    base = _doc([("2026-08-13w", "older")])
    ours = _doc([("2026-08-13z", "new work"), ("2026-08-13w", "older")])
    assert rs.append_only_problems(base, ours) == []


def test_append_only_rejects_mutating_a_prior_open_next():
    """Habit 2: carry Open/next into the NEW entry; do not edit the old one."""
    base = _doc([("2026-08-13w", "older")])
    mutated = base.replace("shipped for older", "shipped for older — stealth edit")
    problems = rs.append_only_problems(base, mutated)
    assert problems, "gate went VACUOUS: prior-body edit passed"
    assert any("older" in p for p in problems)


def test_append_only_rejects_dropping_a_prior_heading():
    base = _doc([("2026-08-13z", "new"), ("2026-08-13w", "older")])
    ours = _doc([("2026-08-13z", "new")])
    problems = rs.append_only_problems(base, ours)
    assert any("older" in p or "removed" in p.lower() for p in problems), problems


def test_append_only_allows_heading_rolled_to_archive_with_rebased_body():
    """keep-20 roll: live heading may leave iff archive holds the frozen rebased body."""
    base = _doc([("2026-08-13z", "kept"), ("2026-08-13w", "rolled")])
    ours = _doc([("2026-08-13z", "kept")])
    _, base_entries = rs.parse(base)
    rolled = next(e for e in base_entries if e.title == "rolled")
    archived = rs.Entry(
        rolled.date,
        rolled.title,
        rs.rewrite_links_for_archive(rolled.text),
    )
    archived_by = {rs.heading_line(archived): archived}
    assert rs.append_only_problems(base, ours, archived_by_heading=archived_by) == []


def test_append_only_rejects_heading_dropped_without_archive_copy():
    base = _doc([("2026-08-13z", "kept"), ("2026-08-13w", "rolled")])
    ours = _doc([("2026-08-13z", "kept")])
    problems = rs.append_only_problems(base, ours, archived_by_heading={})
    assert any("removed" in p.lower() or "rolled" in p for p in problems), problems


def test_append_only_rejects_archive_copy_with_drifted_body():
    base = _doc([("2026-08-13z", "kept"), ("2026-08-13w", "rolled")])
    ours = _doc([("2026-08-13z", "kept")])
    _, base_entries = rs.parse(base)
    rolled = next(e for e in base_entries if e.title == "rolled")
    drifted = rs.Entry(
        rolled.date,
        rolled.title,
        rs.rewrite_links_for_archive(rolled.text).replace(
            "shipped for rolled", "shipped for rolled — archive drift"
        ),
    )
    archived_by = {rs.heading_line(drifted): drifted}
    problems = rs.append_only_problems(base, ours, archived_by_heading=archived_by)
    assert problems, "gate went VACUOUS: drifted archive body passed"
    assert any("rolled" in p or "archive" in p.lower() for p in problems)


def test_append_only_tolerates_trailing_separator_debris_on_a_frozen_entry():
    """--normalize-class trailing --- / blank runs are not a body edit."""
    base = _doc([("2026-08-13w", "older")])
    _, entries = rs.parse(base)
    debris = entries[0].text + "\n\n---\n\n"
    ours = HEADER + debris + "\n"
    assert rs.append_only_problems(base, ours) == []


def test_append_only_allows_editing_a_heading_absent_from_the_base():
    """PR-URL pin: the branch's own new top entry is not frozen vs origin/main."""
    base = _doc([("2026-08-13w", "older")])
    first = _doc([("2026-08-13z", "new work"), ("2026-08-13w", "older")])
    pinned = first.replace("shipped for new work", "shipped for new work — PR #805")
    assert rs.append_only_problems(base, first) == []
    assert rs.append_only_problems(base, pinned) == []


def test_append_only_tolerates_archive_repo_repoint_on_a_frozen_entry():
    """first-passage → first-passage-archive on PR/commit hrefs is not a body edit."""
    gh = "https://github.com/Joshua-Asante/"
    old_pr = gh + "first-passage/" + "pull/831"
    new_pr = gh + "first-passage-archive/pull/831"
    old_sha = gh + "first-passage/" + "commit/12126c58"
    new_sha = gh + "first-passage-archive/commit/12126c58"
    base = HEADER + (
        "## 2026-08-13w — older\n"
        f"**Focus:** focus for older.\n"
        f"**Shipped:** [PR #831]({old_pr}) [`12126c58`]({old_sha}).\n"
    )
    ours = base.replace(old_pr, new_pr).replace(old_sha, new_sha)
    assert rs.append_only_problems(base, ours) == []
    mutated = ours.replace("focus for older", "focus for older — stealth")
    problems = rs.append_only_problems(base, mutated)
    assert problems, "gate went VACUOUS: body edit beside the repoint passed"
    retargeted = ours.replace(new_pr, new_pr.replace("831", "999"))
    problems = rs.append_only_problems(base, retargeted)
    assert problems, "gate went VACUOUS: PR-number change passed as a repoint"


@needs_git
def test_check_append_only_cli_vs_explicit_base(tmp_path):
    _repo_with_history(tmp_path, [
        ("2026-08-13T12:00:00+00:00", [("2026-08-13w", "older")]),
    ])
    _write(tmp_path, _doc([("2026-08-13z", "new"), ("2026-08-13w", "older")]))
    rc = rs.main([
        "--check-append-only", "--root", str(tmp_path),
        "--append-only-base", "HEAD",
    ])
    assert rc == 0

    _write(
        tmp_path,
        _doc([("2026-08-13w", "older")]).replace(
            "shipped for older", "shipped for older — mutated"
        ),
    )
    rc = rs.main([
        "--check-append-only", "--root", str(tmp_path),
        "--append-only-base", "HEAD",
    ])
    assert rc == 1
