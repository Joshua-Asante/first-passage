"""Unit tests for scripts/check_status_consistency.py — cross-surface status gate.

CATALOG is the status authority; the ledger DEAD-lists + rejected_candidates.md
are the asserting surfaces, joined on the lab/(analysis|archive)/<slug>/ path.
Tests pin the parser, the reliable finding classes (C2 self-consistency, C3
stale-tier link) + the advisory NOTE, the backtick/prose robustness of the link
regex, the joinability limit, and CLI exit codes — all on synthetic tmp fixtures.

(A "C1" status-contradiction check was designed but dropped: rejection contexts
link the apparatus/parent study, which may legitimately be Active, so the slug
join was false-positive-only. The tier check C3 + CATALOG self-consistency C2 are
the mechanically-reliable core. See the design doc.)
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_CSC_PATH = REPO_ROOT / "scripts" / "check_status_consistency.py"
_spec = importlib.util.spec_from_file_location("check_status_consistency", _CSC_PATH)
csc = importlib.util.module_from_spec(_spec)
# Register before exec so the module's @dataclass fields (str | None, under
# `from __future__ import annotations`) resolve — dataclasses looks the owning
# module up in sys.modules to classify string annotations. The standard
# spec_from_file_location idiom (Python docs) includes this step.
sys.modules[_spec.name] = csc
_spec.loader.exec_module(csc)


_ALA_PATH = REPO_ROOT / "scripts" / "archive_lab_analysis.py"
_ala_spec = importlib.util.spec_from_file_location("archive_lab_analysis", _ALA_PATH)
ala = importlib.util.module_from_spec(_ala_spec)
sys.modules[_ala_spec.name] = ala
_ala_spec.loader.exec_module(ala)



CATALOG_MINI = """# Lab analysis catalog

## Active

| slug | status | one-liner | card | body | heavy | closed |
|---|---|---|---|---|---|---|
| orb_universe_2026-06-22 | ACTIVE | — | lab/analysis/orb_universe_2026-06-22/RESULTS.md | lab/analysis/orb_universe_2026-06-22/ | — | — |
| q_kbudget_1_2026-07 | HOLD | held | lab/analysis/q_kbudget_1_2026-07/RESULTS.md | lab/analysis/q_kbudget_1_2026-07/ | — | — |

## Archived

| slug | status | one-liner | card | body | heavy | closed |
|---|---|---|---|---|---|---|
| usoil_rdm | FALSIFIED | edge-failure | lab/analysis/usoil_rdm/CARD.md | lab/archive/usoil_rdm/ | — | 2026-07-12 |
"""

CATALOG_THEMED = """# Lab analysis catalog

## Active

### c1

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| band_study | c1 | ACTIVE | floors | lab/analysis/c1/band_study/ | — |

## Archived

| slug | status | one-liner | card | body | heavy | closed |
|---|---|---|---|---|---|---|
| old | CLOSED | done | lab/analysis/old/CARD.md | lab/archive/old/ | — | 2026-08-01 |
"""


# ── parse_catalog ───────────────────────────────────────────────

def test_parse_catalog_indexes_slug_table_and_tier():
    cat = csc.parse_catalog(CATALOG_MINI)
    assert set(cat) == {"orb_universe_2026-06-22", "q_kbudget_1_2026-07", "usoil_rdm"}
    assert cat["orb_universe_2026-06-22"].table == "active"
    assert cat["orb_universe_2026-06-22"].body_tier == "live"
    assert cat["q_kbudget_1_2026-07"].status == "HOLD"
    # Archived row: body is lab/archive/ even though card is a lab/analysis/ stub.
    assert cat["usoil_rdm"].table == "archived"
    assert cat["usoil_rdm"].body_tier == "archived"
    assert cat["usoil_rdm"].status == "FALSIFIED"


def test_parse_catalog_themed_active_columns():
    cat = csc.parse_catalog(CATALOG_THEMED)
    assert cat["band_study"].status == "ACTIVE"
    assert cat["band_study"].table == "active"
    assert cat["band_study"].body_tier == "live"
    assert cat["old"].body_tier == "archived"


def test_parse_catalog_hot_bodies_heading_is_active():
    text = CATALOG_THEMED_HOT.replace("## Active", "## Hot bodies")
    text = (
        "# Lab analysis catalog\n\n## In flight\n\n"
        "| slug | theme | status | one-liner | body |\n"
        "|---|---|---|---|---|\n"
        "| stay_hot | c1 | FALSIFIED | leftover | lab/analysis/c1/stay_hot/ |\n\n"
        + text.split("# Lab analysis catalog\n\n", 1)[-1]
    )
    cat = csc.parse_catalog(text)
    assert cat["stay_hot"].table == "active"
    assert cat["stay_hot"].status == "FALSIFIED"
    assert cat["stay_hot"].hot == "yes"


def test_slug_link_nested_hot_extracts_study_slug_not_theme():
    links = csc._links_in_line(
        "see [x](lab/analysis/c1/band_study/RESULTS.md)"
    )
    assert links[0][1] == "band_study"


# ── C2: CATALOG self-consistency ────────────────────────────────

def test_c2_active_row_with_archive_body_is_flagged():
    bad = CATALOG_MINI.replace(
        "| orb_universe_2026-06-22 | ACTIVE | — | lab/analysis/orb_universe_2026-06-22/RESULTS.md | lab/analysis/orb_universe_2026-06-22/ | — | — |",
        "| orb_universe_2026-06-22 | ACTIVE | — | lab/analysis/orb_universe_2026-06-22/RESULTS.md | lab/archive/orb_universe_2026-06-22/ | — | — |",
    )
    findings = csc.check_catalog_internal(csc.parse_catalog(bad))
    assert any(f.code == "C2" and "orb_universe_2026-06-22" in f.message for f in findings)


def test_c2_terminal_disposition_in_active_without_hot_is_not_flagged():
    """Legacy rows omit `hot`; disposition class is no longer a C2 join key."""
    bad = CATALOG_MINI.replace(
        "| q_kbudget_1_2026-07 | HOLD |", "| q_kbudget_1_2026-07 | FALSIFIED |",
    )
    findings = csc.check_catalog_internal(csc.parse_catalog(bad))
    assert not any(f.code == "C2" and "q_kbudget_1_2026-07" in f.message for f in findings)


CATALOG_THEMED_HOT = """# Lab analysis catalog

## Active

### c1

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| stay_hot | c1 | FALSIFIED | yes | leftover | lab/analysis/c1/stay_hot/ | — |

## Archived

| slug | status | one-liner | card | body | heavy | closed |
|---|---|---|---|---|---|---|
| old | CLOSED | done | lab/analysis/old/CARD.md | lab/archive/old/ | — | 2026-08-01 |
"""


def test_c2_terminal_disposition_in_active_with_hot_yes_is_clean():
    assert csc.check_catalog_internal(csc.parse_catalog(CATALOG_THEMED_HOT)) == []


def test_c2_hot_no_in_active_table_is_flagged():
    bad = CATALOG_THEMED_HOT.replace("| stay_hot | c1 | FALSIFIED | yes |", "| stay_hot | c1 | FALSIFIED | no |")
    findings = csc.check_catalog_internal(csc.parse_catalog(bad))
    assert any(f.code == "C2" and "stay_hot" in f.message and "hot=" in f.message for f in findings)


def test_c2_hot_yes_in_archived_table_is_flagged():
    archived_hot = """# Lab analysis catalog

## Archived

| slug | theme | status | hot | one-liner | body | heavy |
|---|---|---|---|---|---|---|
| old | — | CLOSED | yes | done | lab/archive/old/ | — |
"""
    findings = csc.check_catalog_internal(csc.parse_catalog(archived_hot))
    assert any(f.code == "C2" and "old" in f.message for f in findings)


def test_c2_clean_catalog_has_no_findings():
    assert csc.check_catalog_internal(csc.parse_catalog(CATALOG_MINI)) == []


def test_c2_unknown_status_word_not_flagged():
    # A status word outside LIVE/TERMINAL (e.g. WATCH) is not a C2 join key;
    # with a live-tier body in the Active table there is no tier/`hot` mismatch either.
    cat = CATALOG_MINI.replace("| q_kbudget_1_2026-07 | HOLD |", "| q_kbudget_1_2026-07 | WATCH |")
    findings = csc.check_catalog_internal(csc.parse_catalog(cat))
    assert not any(f.code == "C2" and "q_kbudget_1_2026-07" in f.message for f in findings)


# ── scanners ────────────────────────────────────────────────────

LEDGER_MINI = """# INSTRUMENT LEDGER — TESTSYM

## Durable findings

| # | Finding | Evidence |
|---|---|---|
| F1 | orb is live | [RESULTS](../../lab/analysis/orb_universe_2026-06-22/RESULTS.md) |

## Dead / parked (do not revive)

- **usoil fader:** FALSIFIED → [RESULTS](../../lab/archive/usoil_rdm/RESULTS.md).
- **Q-NAS-4 sign-gate:** memory-only [[project_q_nas_4_closure]] — no lab slug.
- **evicted thing:** retrieve via `git show pre-prune-2026-06-05:lab/analysis/gone/x.md`.

## Feed notes

- see [stub](../../lab/analysis/usoil_rdm/CARD.md) for the archived body.
"""


def test_scan_ledger_flags_dead_section_only():
    a = csc.scan_ledger(LEDGER_MINI, "ops/instruments/TESTSYM.md")
    by_slug = {x.slug: x for x in a}
    # Durable-findings link: present but NOT asserting rejection.
    assert by_slug["orb_universe_2026-06-22"].asserts_rejection is False
    # Dead-section link: asserts rejection.
    assert "usoil_rdm" in by_slug
    dead = [x for x in a if x.slug == "usoil_rdm" and x.link_tier == "archive"]
    assert dead and dead[0].asserts_rejection is True


def test_scan_ledger_skips_memory_and_historical_lines():
    a = csc.scan_ledger(LEDGER_MINI, "ops/instruments/TESTSYM.md")
    slugs = {x.slug for x in a}
    assert "gone" not in slugs          # git show pre-prune- line skipped
    # The memory-only Q-NAS-4 line carries no lab/(analysis|archive)/ link at all.
    assert all("q_nas" not in s for s in slugs)


# Mirrors the 2026-08-14 rejected_candidates.md:306 shape: a retrieve-via
# git-show clause and a separate live lab/analysis/ citation on the SAME line.
# Whole-line HISTORICAL_LINE_RE skip hid the live href from C3.
_MIXED_EVICTION_AND_LIVE = (
    "retired ops/regime_gate/README.md "
    "(retrieve via git show <pre-2026-07-11-commit>:ops/regime_gate/README.md); "
    "graduated from [RESULTS](../lab/analysis/movedstudy/RESULTS.md)."
)


def test_scan_still_sees_live_link_beside_eviction_clause(tmp_path):
    """Eviction-idiom skip is clause-scoped: a live lab/analysis/ link on the
    same line as a git-show retrieval must still be scanned, and C3-flagged
    when that target has moved to archive."""
    (tmp_path / "lab" / "archive" / "movedstudy").mkdir(parents=True)
    (tmp_path / "lab" / "archive" / "movedstudy" / "RESULTS.md").write_text(
        "body", encoding="utf-8")
    rejected = csc.scan_rejected(
        _MIXED_EVICTION_AND_LIVE + "\n", "docs/rejected_candidates.md")
    ledger = csc.scan_ledger(
        "## Dead / parked\n\n- " + _MIXED_EVICTION_AND_LIVE + "\n",
        "ops/instruments/TESTSYM.md")
    for assertions in (rejected, ledger):
        slugs = {x.slug for x in assertions}
        assert "movedstudy" in slugs
        assert "gone" not in slugs
        assert "regime_gate" not in slugs
        live = [x for x in assertions if x.slug == "movedstudy"]
        assert live and live[0].link_tier == "analysis"
        findings = csc.check_c3(assertions, tmp_path)
        assert any(f.code == "C3" and "movedstudy" in f.message for f in findings)


def test_scan_ledger_clears_dead_section_at_next_header():
    # The "## Feed notes" header (same level as "## Dead / parked") clears the
    # dead flag: its lab/analysis/usoil_rdm/CARD.md link must NOT assert rejection.
    a = csc.scan_ledger(LEDGER_MINI, "ops/instruments/TESTSYM.md")
    feed = [x for x in a if x.slug == "usoil_rdm" and x.link_tier == "analysis"]
    assert feed and all(x.asserts_rejection is False for x in feed)


def test_scan_rejected_all_links_assert_rejection():
    text = "### Foo\n**Artifact:** [x](lab/archive/usoil_rdm/CARD.md) and [y](../lab/analysis/oil_carry/CARD.md)\n"
    a = csc.scan_rejected(text, "docs/rejected_candidates.md")
    assert {x.slug for x in a} == {"usoil_rdm", "oil_carry"}
    assert all(x.asserts_rejection for x in a)


def test_slug_link_regex_excludes_backtick_prose():
    # Generic inline-code prose like "the `lab/analysis/` lane" must NOT yield a
    # slug (there is none), and a backtick-wrapped path must yield the clean slug
    # (no trailing backtick). This is the regression for the first-run parse bug.
    a = csc.scan_rejected(
        "routed to the `lab/analysis/` lane; see `lab/archive/usoil_rdm`.\n",
        "docs/rejected_candidates.md")
    assert {x.slug for x in a} == {"usoil_rdm"}
    assert a[0].link_tier == "archive"


# ── C3: stale analysis->archive tier link + flat-to-theme-nest ──

def test_c3_stale_analysis_link_with_archive_body(tmp_path):
    # slug moved to lab/archive/; a link still points at lab/analysis/<slug>/RESULTS.md
    (tmp_path / "lab" / "archive" / "movedstudy").mkdir(parents=True)
    (tmp_path / "lab" / "archive" / "movedstudy" / "RESULTS.md").write_text("body", encoding="utf-8")
    assertions = [csc.Assertion(
        "ops/instruments/TESTSYM.md", 12, "movedstudy",
        "analysis", "lab/analysis/movedstudy/RESULTS.md", True)]
    findings = csc.check_c3(assertions, tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "C3"
    assert "lab/archive/movedstudy/RESULTS.md" in findings[0].message  # repoint suggestion


def test_c3_resolving_stub_link_is_clean(tmp_path):
    # link to the surviving lab/analysis/<slug>/CARD.md stub resolves -> no C3
    (tmp_path / "lab" / "analysis" / "stubbed").mkdir(parents=True)
    (tmp_path / "lab" / "analysis" / "stubbed" / "CARD.md").write_text("stub", encoding="utf-8")
    assertions = [csc.Assertion(
        "ops/instruments/TESTSYM.md", 20, "stubbed",
        "analysis", "lab/analysis/stubbed/CARD.md", False)]
    assert csc.check_c3(assertions, tmp_path) == []


def test_c3_archive_tier_links_never_flagged(tmp_path):
    assertions = [csc.Assertion(
        "docs/rejected_candidates.md", 5, "whatever",
        "archive", "lab/archive/whatever/CARD.md", True)]
    assert csc.check_c3(assertions, tmp_path) == []


def test_c3_stale_flat_link_with_theme_nest(tmp_path):
    """NAS100.md shape: lab/analysis/<slug>/... moved to lab/analysis/<theme>/<slug>/."""
    nested = (
        tmp_path / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
    )
    nested.mkdir(parents=True)
    (nested / "RESULTS_gap_followup3.md").write_text("body", encoding="utf-8")
    assertions = [csc.Assertion(
        "ops/instruments/NAS100.md", 85, "orb_universe_2026-06-22",
        "analysis",
        "lab/analysis/orb_universe_2026-06-22/RESULTS_gap_followup3.md",
        False)]
    findings = csc.check_c3(assertions, tmp_path)
    assert len(findings) == 1
    assert findings[0].code == "C3"
    assert "lab/analysis/orb/orb_universe_2026-06-22/RESULTS_gap_followup3.md" in findings[0].message


def test_c3_stale_flat_link_orb_mnq_theme_nest(tmp_path):
    """NQ.md shape: lab/analysis/orb_mnq_2026-07/... now under lab/analysis/orb/."""
    nested = tmp_path / "lab" / "analysis" / "orb" / "orb_mnq_2026-07"
    nested.mkdir(parents=True)
    (nested / "RESULTS.md").write_text("body", encoding="utf-8")
    assertions = [csc.Assertion(
        "ops/instruments/NQ.md", 49, "orb_mnq_2026-07",
        "analysis", "lab/analysis/orb_mnq_2026-07/RESULTS.md", False)]
    findings = csc.check_c3(assertions, tmp_path)
    assert len(findings) == 1
    assert "lab/analysis/orb/orb_mnq_2026-07/RESULTS.md" in findings[0].message


def test_c3_unresolved_without_nest_or_archive_is_clean(tmp_path):
    assertions = [csc.Assertion(
        "ops/instruments/TESTSYM.md", 3, "ghost",
        "analysis", "lab/analysis/ghost/RESULTS.md", False)]
    assert csc.check_c3(assertions, tmp_path) == []


# ── NOTE: uncatalogued rejected slug (advisory) ─────────────────

def test_note_uncatalogued_slug():
    cat = csc.parse_catalog(CATALOG_MINI)
    assertions = [csc.Assertion(
        "docs/rejected_candidates.md", 5, "ghost_study_2099",
        "archive", "lab/archive/ghost_study_2099/CARD.md", True)]
    notes = csc.check_notes(cat, assertions)
    assert len(notes) == 1 and notes[0].severity == "NOTE" and "ghost_study_2099" in notes[0].message


# ── orchestration + CLI ─────────────────────────────────────────

def _write_mini_repo(root: Path, catalog_text: str, ledger_text: str, rejected_text: str) -> None:
    (root / "lab").mkdir(parents=True, exist_ok=True)
    (root / "lab" / "CATALOG.md").write_text(catalog_text, encoding="utf-8")
    (root / "ops" / "instruments").mkdir(parents=True, exist_ok=True)
    (root / "ops" / "instruments" / "TESTSYM.md").write_text(ledger_text, encoding="utf-8")
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "rejected_candidates.md").write_text(rejected_text, encoding="utf-8")


def _stale_link_repo(root: Path) -> None:
    # An archived study whose RESULTS.md moved to lab/archive/, but a ledger still
    # links the lab/analysis/ path -> C3.
    (root / "lab" / "archive" / "usoil_rdm").mkdir(parents=True, exist_ok=True)
    (root / "lab" / "archive" / "usoil_rdm" / "RESULTS.md").write_text("body", encoding="utf-8")
    ledger = ("# L\n\n## Dead / parked\n\n"
              "- usoil: [r](../../lab/analysis/usoil_rdm/RESULTS.md)\n")
    _write_mini_repo(root, CATALOG_MINI, ledger, "# Rejected\n")


def test_collect_findings_c3_end_to_end(tmp_path):
    _stale_link_repo(tmp_path)
    findings = csc.collect_findings(
        tmp_path, tmp_path / "lab" / "CATALOG.md",
        tmp_path / "ops" / "instruments", tmp_path / "docs" / "rejected_candidates.md")
    c3 = [f for f in findings if f.code == "C3"]
    assert len(c3) == 1
    assert "lab/archive/usoil_rdm/RESULTS.md" in c3[0].message


def test_cli_exit_nonzero_on_stale_tier_link(tmp_path):
    _stale_link_repo(tmp_path)
    r = subprocess.run(
        [sys.executable, str(_CSC_PATH), "--repo-root", str(tmp_path)],
        capture_output=True, text=True)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "C3" in r.stdout


def test_cli_exit_zero_when_consistent(tmp_path):
    # Dead-lists usoil via its ARCHIVE-tier link -> no C3, C2 clean -> exit 0.
    ledger = ("# L\n\n## Dead / parked\n\n"
              "- usoil: [r](../../lab/archive/usoil_rdm/RESULTS.md)\n")
    _write_mini_repo(tmp_path, CATALOG_MINI, ledger, "# Rejected\n")
    r = subprocess.run(
        [sys.executable, str(_CSC_PATH), "--repo-root", str(tmp_path)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_theme_order_matches_archive_lab_analysis():
    # scripts/ aren't packages — pin equality rather than a cross-import.
    # Must stay aligned with scripts/archive_lab_analysis.THEME_ORDER.
    assert csc._THEME_ORDER == ala.THEME_ORDER

