"""Tests for scripts/archive_lab_analysis.py — disposition parser (Task 1).

Design: docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# scripts/ is not a package; load the module by path (stdlib-only module).
_REPO = Path(__file__).resolve().parents[1]
_PATH = _REPO / "scripts" / "archive_lab_analysis.py"
_spec = importlib.util.spec_from_file_location("archive_lab_analysis", _PATH)
ala = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = ala
_spec.loader.exec_module(ala)


def test_parse_inline_disposition_closed():
    text = "**Date:** 2026-06-30 · **Disposition:** CLOSED — no viable candidate · **Scope:** lab\n"
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "CLOSED"
    assert "CLOSED" in d.raw_token.upper()


def test_parse_bold_verdict_falsified():
    text = "**Verdict: FALSIFIED.** USDJPY trend-persistence does not separate.\n"
    d = ala.parse_disposition(text)
    assert d.status == "FALSIFIED"


def test_parse_reject_maps_falsified():
    text = "**Verdict: REJECT — edge-failure (+ venue/cost-constraint).**\n"
    d = ala.parse_disposition(text)
    assert d.status == "FALSIFIED"


def test_uppercase_stop_null_maps_null_not_falsified():
    """Terminal NULL closure (Q-TNEC-ENV-1 shape) is its own archiveable verdict.

    Historically ``\\bNULL\\b`` (re.I) collapsed into FALSIFIED, so CATALOG derived
    ``archive owed (FALSIFIED)`` for a genuine STOP / NULL. Case-sensitive uppercase
    NULL only — prose ``null`` must not take this branch.
    """
    text = (
        "**Status:** CLOSED — H_B = 0, STOP / NULL per PREREG F7 "
        "· closure: docs/briefs/closures/Q-TNEC-ENV-1-closure.md\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "NULL"
    assert ala.is_archiveable(d.status) is True


def test_lowercase_prose_null_does_not_map_null_verdict():
    """MNQFLOW-1 trap: lowercase prose ``the null`` must not become the NULL token.

    ACTIVE/HOLD dominance short-circuits before ``_TOKEN_STATUS``, so the load-bearing
    shape is a terminal CLOSED whose narrative names ``the null`` — the historic
    case-insensitive ``\\bNULL\\b`` stole that into FALSIFIED before CLOSED could win.
    """
    text = (
        "**Disposition:** CLOSED — pre-registered the null as most probable\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "CLOSED"
    assert d.status != "NULL"


def test_falsified_line_still_maps_falsified():
    text = (
        "**Status:** FALSIFIED — V2 fired as pre-registered most likely: "
        "the observable book carries no edge\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "FALSIFIED"


def test_parse_hold_not_archiveable():
    text = "**Disposition:** AMBIGUOUS / operational HOLD — build NOT triggered\n"
    d = ala.parse_disposition(text)
    assert d.status == "HOLD"
    assert ala.is_archiveable(d.status) is False


def test_hold_dominates_ambiguous_in_the_verdict_clause():
    """The live shape from xauusd_cgb_2026-06-15, verbatim.

    `AMBIGUOUS` alone is terminal (Q-GEOFIT-1), but `AMBIGUOUS ... HOLD` is the
    repo's non-terminal verdict. Priority-order search let AMBIGUOUS win and
    stamped a held study 'archive owed (CLOSED)' — `--slug` would have moved it.
    """
    text = "## Disposition: AMBIGUOUS (brief §6) / operational HOLD — build NOT triggered\n"
    d = ala.parse_disposition(text)
    assert d.status == "HOLD"
    assert ala.is_archiveable(d.status) is False


def test_hold_named_only_in_narrative_does_not_reopen_a_closed_study():
    """The live shape from q_kbudget_1_2026-07, verbatim in the load-bearing part.

    Its verdict is RESOLVED; the one-liner merely recounts passing through
    AMBIGUOUS-HOLD. A blanket 'HOLD wins' rule would re-open every study whose
    history mentions a hold, so dominance is scoped to the verdict clause.
    ``RESOLVED`` is not a CATALOG status token (stay-hot Active rows would
    flip to archiveable CLOSED). This fixture still maps CLOSED via the
    narrative ``AMBIGUOUS`` token — the historical path must not steal HOLD.
    """
    text = ("**Verdict: `RESOLVED`** (frozen pre-reg §D: ≥1 axis PASSES both "
            "clauses) — flipped 2026-07-15 after operator ratification. "
            "Historical path: AMBIGUOUS-HOLD 2026-07-14 → D5 ratified.\n")
    d = ala.parse_disposition(text)
    assert d.status == "CLOSED"
    assert ala.is_archiveable(d.status) is True


def test_bare_resolved_is_not_a_catalog_status_token():
    """RESOLVED alone does not parse — house style leads with ACTIVE/HOLD."""
    assert ala.parse_disposition(
        "**Verdict:** `RESOLVED` (H-MONSURF-1 accepted)\n"
    ) is None


def test_lowercase_resolved_does_not_map_closed():
    """Same NULL/CLOSED collision class — prose 'resolved' is not the token."""
    text = "**Status:** ACTIVE — the question resolved on the honest clock\n"
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "ACTIVE"


def test_exploratory_and_measured_map_active():
    d = ala.parse_disposition("**Status:** EXPLORATORY — not pre-registered\n")
    assert d is not None
    assert d.status == "ACTIVE"
    assert ala.is_archiveable(d.status) is False
    d = ala.parse_disposition(
        "**Status:** MEASURED — WITH NAMED RESIDUAL (2026-08-23)\n"
    )
    assert d is not None
    assert d.status == "ACTIVE"


def test_exploratory_clause_dominates_closed_in_narrative():
    text = "**Status:** EXPLORATORY — later CLOSED as a historical note\n"
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "ACTIVE"


def test_active_clause_dominates_resolved_in_narrative():
    """House style: ACTIVE — … `RESOLVED` … must stay Active, not archiveable."""
    text = (
        "**Verdict:** ACTIVE — `Q-MONSURF-1` idle-clock — `RESOLVED` 2026-08-23\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "ACTIVE"
    assert ala.is_archiveable(d.status) is False


def test_dominance_is_uppercase_only_so_prose_cannot_hijack_a_closure():
    """Status tokens are caps throughout the corpus; lowercase is prose.

    The lowercase words must sit INSIDE the verdict clause to test this at all —
    anything after the dash is already excluded by scoping, so a post-dash
    example would pass even with a case-insensitive rule and prove nothing.
    """
    d = ala.parse_disposition("**Disposition:** CLOSED (the gates hold) — narrative\n")
    assert d.status == "CLOSED"
    d = ala.parse_disposition("**Status:** RETIRED (no longer active) — narrative\n")
    assert d.status == "RETIRED"
    # …and the word-boundary cases that appear in real cards stay inert.
    for prose in ("holdout", "holding", "HOLDS"):
        got = ala.parse_disposition(f"**Disposition:** FALSIFIED ({prose} MISS)\n")
        assert got.status == "FALSIFIED", prose


def test_heading_alone_does_not_parse():
    text = "## Verdict — NO ROBUST STANDALONE EDGE\n\nBody prose.\n"
    assert ala.parse_disposition(text) is None


def test_blockquote_verdict_without_field_needs_stamp():
    text = "> **VERDICT: NOT-CONFIRMED — offline null.**\n"
    # blockquote bold VERDICT without Disposition:/Status:/Verdict: field shape
    # Spec: do not auto-qualify; implementer may accept **VERDICT: if field-shaped
    # after stripping > — if accepted, status FALSIFIED/CLOSED; prefer refuse (None)
    # Locked choice for v1: return None (stamp-first for orb-style)
    assert ala.parse_disposition(text) is None


def test_decisive_hint_from_stamp():
    text = "**Disposition:** CLOSED — decisive: RESULTS_gap_followup3.md — gap null\n"
    d = ala.parse_disposition(text)
    assert d.decisive_hint == "RESULTS_gap_followup3.md"


def test_only_first_40_lines_scanned():
    lines = ["noise\n"] * 45 + ["**Disposition:** CLOSED — late\n"]
    assert ala.parse_disposition("".join(lines)) is None


def test_verdict_wins_over_earlier_status_active():
    """ADR 2026-08-22: separate Verdict line beats a preceding Status: ACTIVE."""
    text = (
        "**Status:** ACTIVE — still listed in the Active table\n"
        "**Verdict:** FALSIFIED — terminal on the honest clock\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "FALSIFIED"


def test_verdict_null_wins_over_status_active():
    text = (
        "**Status:** ACTIVE — house-style mask\n"
        "**Verdict:** NULL — leftover stay-hot body\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "NULL"
    assert ala.is_archiveable(d.status) is True


def test_hold_in_verdict_clause_still_dominates_status_active():
    text = (
        "**Status:** ACTIVE — scanning\n"
        "**Verdict:** AMBIGUOUS-HOLD — do not archive\n"
    )
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "HOLD"
    assert ala.is_archiveable(d.status) is False


def test_inline_status_active_null_without_verdict_line_stays_active():
    """House style without a separate Verdict line is unchanged — ACTIVE dominates."""
    text = "**Status:** ACTIVE — NULL: leftover one-liner\n"
    d = ala.parse_disposition(text)
    assert d is not None
    assert d.status == "ACTIVE"


def test_parse_theme_from_bold_field():
    text = "**Theme:** c1\n**Status:** ACTIVE — measuring\n"
    assert ala.parse_theme(text) == "c1"


def test_parse_theme_unknown_maps_inbox():
    text = "**Theme:** widgets\n**Status:** ACTIVE\n"
    assert ala.parse_theme(text) == "_inbox"


def test_parse_theme_missing_maps_inbox():
    assert ala.parse_theme("# Study\n**Status:** ACTIVE\n") == "_inbox"


def test_parse_theme_empty_value_maps_inbox():
    # **Theme:** with no token must not IndexError on .split()[0].
    assert ala.parse_theme("**Theme:**\n**Status:** ACTIVE\n") == "_inbox"
    assert ala.parse_theme("**Theme:**   \n**Status:** ACTIVE\n") == "_inbox"


def test_themes_closed_set_includes_striker_and_c1():
    assert "c1" in ala.THEMES and "striker" in ala.THEMES
    assert ala.THEME_ORDER.index("c1") < ala.THEME_ORDER.index("striker")


# ── Task 2: catalog scan + regenerate ─────────────────────────────────────────


def test_choose_source_card_prefers_results(tmp_path: Path):
    d = tmp_path / "study"
    d.mkdir()
    (d / "README.md").write_text("# x\n", encoding="utf-8")
    (d / "RESULTS.md").write_text("**Disposition:** CLOSED — done\n", encoding="utf-8")
    assert ala.choose_source_card(d).name == "RESULTS.md"


def test_scan_lab_nested_hot_and_flat_stub(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis"
    archive = tmp_path / "lab" / "archive"

    hot = analysis / "c1" / "band_study"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — band floor\n", encoding="utf-8"
    )
    (analysis / "c1" / "README.md").write_text("# c1\n", encoding="utf-8")

    stub = analysis / "old"
    stub.mkdir(parents=True)
    (stub / "CARD.md").write_text(
        "# old\n\n**Disposition:** CLOSED — done\n**Archived:** 2026-08-01\n",
        encoding="utf-8",
    )
    (archive / "old").mkdir(parents=True)
    (archive / "old" / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — done\n", encoding="utf-8"
    )

    tracked = {
        "old": frozenset({"lab/analysis/old/CARD.md"}),
        "band_study": frozenset({"lab/analysis/c1/band_study/RESULTS.md"}),
    }
    rows = {r.slug: r for r in ala.scan_lab(tmp_path, tracked_override=tracked)}
    assert rows["band_study"].theme == "c1"
    assert rows["band_study"].body == "lab/analysis/c1/band_study/"
    assert rows["band_study"].status == "ACTIVE"
    assert rows["old"].body == "lab/archive/old/"
    assert rows["old"].theme == "—"


def test_resolve_hot_dir_returns_nested_path(tmp_path: Path):
    hot = tmp_path / "lab" / "analysis" / "c1" / "band_study"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — nested\n", encoding="utf-8"
    )
    assert ala.resolve_hot_dir(tmp_path, "band_study") == hot


def test_resolve_hot_dir_returns_none_for_flat_full_dir(tmp_path: Path):
    """Flat pre-Wave-2 full dirs must not resolve (_inbox ∈ THEMES trap)."""
    flat = tmp_path / "lab" / "analysis" / "flat_study"
    flat.mkdir(parents=True)
    (flat / "RESULTS.md").write_text(
        "**Status:** ACTIVE — still flat\n", encoding="utf-8"
    )
    # Sanity: iter_hot_bodies still sees the flat body as (_inbox, …).
    bodies = ala.iter_hot_bodies(tmp_path)
    assert ("_inbox", "flat_study", flat) in bodies
    assert ala.resolve_hot_dir(tmp_path, "flat_study") is None


def test_resolve_scan_theme_stamp_real_wins_over_dir():
    assert ala._resolve_scan_theme("c1", "striker") == "c1"


def test_resolve_scan_theme_inbox_stamp_falls_back_to_dir():
    assert ala._resolve_scan_theme("_inbox", "orb") == "orb"


def test_resolve_scan_theme_both_real_disagree_prefers_stamp():
    assert ala._resolve_scan_theme("harvest", "legacy") == "harvest"


def test_regenerate_catalog_partitions_active_and_archived(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis"
    archive = tmp_path / "lab" / "archive"

    hot = analysis / "hot"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text("# Hot study\nNo stamp yet.\n", encoding="utf-8")

    holdme = analysis / "holdme"
    holdme.mkdir(parents=True)
    (holdme / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting for data\n", encoding="utf-8"
    )

    old_stub = analysis / "old"
    old_stub.mkdir(parents=True)
    (old_stub / "CARD.md").write_text(
        "# old\n\n**Disposition:** CLOSED — done\n**Archived:** 2026-07-01\n",
        encoding="utf-8",
    )
    old_body = archive / "old"
    old_body.mkdir(parents=True)
    (old_body / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — done\n", encoding="utf-8"
    )

    tracked = {
        "old": frozenset({"lab/analysis/old/CARD.md"}),
        "hot": frozenset({"lab/analysis/hot/RESULTS.md"}),
        "holdme": frozenset({"lab/analysis/holdme/RESULTS.md"}),
    }

    text = ala.render_catalog(ala.scan_lab(tmp_path, tracked_override=tracked))
    assert "## Hot bodies" in text and "## Archived" in text
    assert "## In flight" in text
    assert "holdme" in text and "HOLD" in text
    assert "old" in text and "lab/archive/old" in text
    assert "hot" in text and "ACTIVE" in text


def test_render_catalog_groups_active_by_theme(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis"
    (analysis / "c1" / "a").mkdir(parents=True)
    (analysis / "c1" / "a" / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — alpha\n", encoding="utf-8"
    )
    (analysis / "orb" / "b").mkdir(parents=True)
    (analysis / "orb" / "b" / "RESULTS.md").write_text(
        "**Theme:** orb\n**Status:** HOLD — waiting\n", encoding="utf-8"
    )
    tracked = {
        "a": frozenset({"lab/analysis/c1/a/RESULTS.md"}),
        "b": frozenset({"lab/analysis/orb/b/RESULTS.md"}),
    }
    text = ala.render_catalog(ala.scan_lab(tmp_path, tracked_override=tracked))
    assert "### c1" in text and "### orb" in text
    assert "### striker" not in text  # omit empty
    assert "| slug | theme | status | hot | one-liner | body | heavy |" in text
    assert "lab/analysis/c1/a/" in text


def test_in_flight_excludes_hold_and_spent_includes_named(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis"
    live = analysis / "c1" / "live_camp"
    live.mkdir(parents=True)
    (live / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — still open\n", encoding="utf-8"
    )
    held = analysis / "c1" / "held_camp"
    held.mkdir(parents=True)
    (held / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** HOLD — operator hold\n", encoding="utf-8"
    )
    spent = analysis / "c1" / "spent_camp"
    spent.mkdir(parents=True)
    (spent / "RESULTS.md").write_text(
        "**Theme:** c1\n**Verdict:** FALSIFIED — no config survives\n",
        encoding="utf-8",
    )
    escape = analysis / "orb" / "escape_camp"
    escape.mkdir(parents=True)
    (escape / "RESULTS.md").write_text(
        "**Theme:** orb\n**In-flight:** yes\n**Status:** ACTIVE — cultivation\n",
        encoding="utf-8",
    )
    (tmp_path / "STATE.md").write_text(
        "## OPERATOR QUEUE — strictly ordered\n\n"
        "| # | Item | Owner artifact | Blocks |\n"
        "|---|---|---|---|\n"
        "| 1 | find | [`P50`](lab/analysis/c1/live_camp/RESULTS.md) · "
        "[`held`](lab/analysis/c1/held_camp/RESULTS.md) · "
        "[`spent`](lab/analysis/c1/spent_camp/RESULTS.md) | — |\n",
        encoding="utf-8",
    )
    briefs = tmp_path / "docs" / "briefs"
    briefs.mkdir(parents=True)
    (briefs / "INDEX.md").write_text(
        "## Open\n\n"
        "| Q | Status | Home |\n"
        "|---|---|---|\n"
        "| **Q-X** | OPEN | [`live`](lab/analysis/c1/live_camp/RESULTS.md) |\n",
        encoding="utf-8",
    )
    tracked = {
        "live_camp": frozenset({"lab/analysis/c1/live_camp/RESULTS.md"}),
        "held_camp": frozenset({"lab/analysis/c1/held_camp/RESULTS.md"}),
        "spent_camp": frozenset({"lab/analysis/c1/spent_camp/RESULTS.md"}),
        "escape_camp": frozenset({"lab/analysis/orb/escape_camp/RESULTS.md"}),
    }
    rows = ala.scan_lab(tmp_path, tracked_override=tracked)
    slugs = ala.derive_in_flight_slugs(tmp_path, rows)
    assert slugs == frozenset({"live_camp", "escape_camp"})
    assert "held_camp" not in slugs
    assert "spent_camp" not in slugs
    text = ala.render_catalog(rows, in_flight_slugs=slugs)
    inflight = text.split("## Hot bodies")[0]
    assert "## In flight" in inflight
    assert "live_camp" in inflight and "escape_camp" in inflight
    assert "held_camp" not in inflight
    assert "spent_camp" not in inflight
    assert "| slug | theme | status | one-liner | body |" in inflight


def test_regenerate_preserves_gitignored_heavy(tmp_path: Path):
    study = tmp_path / "lab" / "analysis" / "heavy_study"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Status:** ACTIVE — measuring\n", encoding="utf-8"
    )
    scanned = ala.scan_lab(tmp_path)
    committed = [
        ala.CatalogRow(
            slug=r.slug,
            theme=r.theme,
            status=r.status,
            one_liner=r.one_liner,
            card=r.card,
            body=r.body,
            heavy="inputs gitignored",
            closed=r.closed,
        )
        for r in scanned
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    ala.regenerate_catalog(tmp_path)
    text = (tmp_path / "lab" / "CATALOG.md").read_text(encoding="utf-8")
    assert "inputs gitignored" in text


def test_compare_tolerates_in_flight_one_liner(tmp_path: Path):
    study = tmp_path / "lab" / "analysis" / "c1" / "live_camp"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — " + ("x" * 200) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "STATE.md").write_text(
        "## OPERATOR QUEUE — strictly ordered\n\n"
        "[`live`](lab/analysis/c1/live_camp/RESULTS.md)\n",
        encoding="utf-8",
    )
    rows = ala.scan_lab(tmp_path)
    slugs = ala.derive_in_flight_slugs(tmp_path, rows)
    expected = ala.render_catalog(rows, in_flight_slugs=slugs)
    # Committed In flight + Hot bodies keep the untruncated one-liner.
    long = "ACTIVE — " + ("x" * 200)
    disk = expected.replace(rows[0].one_liner, long)
    issues, _warnings = ala._compare_catalog(disk, expected)
    assert issues == []


# ── Task 3: archive move + stub + sibling link rewrite ───────────────────────


def test_rewrite_sibling_link_to_hot_target(tmp_path: Path):
    regime = tmp_path / "lab" / "analysis" / "regime_signal_research_2026-06-25"
    regime.mkdir(parents=True)
    src = "[x](../regime_signal_research_2026-06-25/CLOSURE.md)"
    out = ala.rewrite_sibling_links(src, "chop_native_leg_2026-06-30", tmp_path)
    assert "lab/analysis/regime_signal_research_2026-06-25/CLOSURE.md" in out


def test_rewrite_sibling_link_to_nested_hot_target(tmp_path: Path):
    nested = (
        tmp_path / "lab" / "analysis" / "c1" / "regime_signal_research_2026-06-25"
    )
    nested.mkdir(parents=True)
    src = "[x](../regime_signal_research_2026-06-25/CLOSURE.md)"
    out = ala.rewrite_sibling_links(src, "chop_native_leg_2026-06-30", tmp_path)
    assert (
        "lab/analysis/c1/regime_signal_research_2026-06-25/CLOSURE.md" in out
    )


def test_rewrite_sibling_link_to_archive_target(tmp_path: Path):
    old = tmp_path / "lab" / "archive" / "old_study"
    old.mkdir(parents=True)
    src = "[x](../old_study/RESULTS.md)"
    out = ala.rewrite_sibling_links(src, "chop_native_leg_2026-06-30", tmp_path)
    assert "lab/archive/old_study/RESULTS.md" in out


def test_rewrite_skips_non_sibling_links(tmp_path: Path):
    src = "[x](lab/analysis/other/RESULTS.md) and [y](./local.md)"
    out = ala.rewrite_sibling_links(src, "study", tmp_path)
    assert out == src


def test_rewrite_skips_multi_hop_relative_links(tmp_path: Path):
    """A ../../ (or deeper) link is not a sibling-slug reference - stripping
    exactly one hop leaves a leftover ".." that must not be treated as a
    slug name (it trivially resolves as a directory and corrupts the path).
    """
    (tmp_path / "lab" / "archive").mkdir(parents=True)
    src = (
        "[two-hop](../../docs/briefs/closures/X-closure.md) "
        "[three-hop](../../../docs/rejected_candidates.md)"
    )
    out = ala.rewrite_sibling_links(src, "study", tmp_path)
    assert out == src
    assert "lab/archive/.." not in out


def test_build_stub_matches_spec_template():
    disp = ala.Disposition(
        raw_token="CLOSED",
        status="CLOSED",
        one_liner="no viable candidate",
        decisive_hint=None,
    )
    stub = ala.build_stub("study_slug", disp, "RESULTS.md", "2026-07-11")
    assert stub.startswith("# study_slug\n\n")
    assert "**Disposition:** CLOSED — no viable candidate" in stub
    assert "**Archived:** 2026-07-11" in stub
    assert "**Body:** [`lab/archive/study_slug/`](../../archive/study_slug/)" in stub
    assert "**Source card:** [`RESULTS.md`](../../archive/study_slug/RESULTS.md)" in stub
    assert "lab/CATALOG.md" in stub


def test_build_stub_strips_redundant_status_prefix():
    disp = ala.Disposition(
        raw_token="CLOSED",
        status="CLOSED",
        one_liner="CLOSED — no viable candidate",
        decisive_hint=None,
    )
    stub = ala.build_stub("study_slug", disp, "RESULTS.md", "2026-07-11")
    assert "**Disposition:** CLOSED — no viable candidate" in stub
    assert "CLOSED — CLOSED" not in stub


def test_build_stub_status_only_one_liner():
    disp = ala.Disposition(
        raw_token="FALSIFIED",
        status="FALSIFIED",
        one_liner="FALSIFIED",
        decisive_hint=None,
    )
    stub = ala.build_stub("noct_spx", disp, "verdict.md", "2026-07-11")
    assert "**Disposition:** FALSIFIED\n" in stub
    assert "FALSIFIED — FALSIFIED" not in stub


def test_archive_writes_stub_and_moves_tracked(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — archival test study\n", encoding="utf-8"
    )
    (analysis / "NOTES.md").write_text("# notes\n", encoding="utf-8")

    tracked = {
        "study": frozenset(
            {"lab/analysis/study/RESULTS.md", "lab/analysis/study/NOTES.md"}
        ),
    }

    ala.archive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        tracked_override=tracked,
    )
    assert (tmp_path / "lab/archive/study/RESULTS.md").is_file()
    assert (tmp_path / "lab/analysis/study/CARD.md").is_file()
    assert not (tmp_path / "lab/analysis/study/RESULTS.md").exists()
    catalog = (tmp_path / "lab/CATALOG.md").read_text(encoding="utf-8")
    assert "## Archived" in catalog and "study" in catalog


def test_archive_slug_from_nested_hot(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "c1" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Theme:** c1\n**Disposition:** CLOSED — done\n",
        encoding="utf-8",
    )
    tracked = {
        "study": frozenset({"lab/analysis/c1/study/RESULTS.md"}),
    }
    ala.archive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        tracked_override=tracked,
    )
    assert (tmp_path / "lab/archive/study/RESULTS.md").is_file()
    assert (tmp_path / "lab/analysis/study/CARD.md").is_file()
    assert not (tmp_path / "lab/analysis/c1/study/RESULTS.md").exists()
    catalog = (tmp_path / "lab/CATALOG.md").read_text(encoding="utf-8")
    assert "## Archived" in catalog and "study" in catalog


def test_archive_rewrites_sibling_links_in_moved_body(tmp_path: Path):
    other = tmp_path / "lab" / "analysis" / "other"
    other.mkdir(parents=True)
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — done\n"
        "See [peer](../other/NOTES.md).\n",
        encoding="utf-8",
    )

    ala.archive_slug(tmp_path, "study", dry_run=False, use_git=False)
    body = (tmp_path / "lab/archive/study/RESULTS.md").read_text(encoding="utf-8")
    assert "lab/analysis/other/NOTES.md" in body
    assert "../other/" not in body


def test_archive_refuses_without_disposition(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text("# just noise\nNo stamp.\n", encoding="utf-8")

    with pytest.raises(ala.ArchiveError, match="archiveable"):
        ala.archive_slug(tmp_path, "study", dry_run=False, use_git=False)


def test_archive_refuses_hold_disposition(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "holdme"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting for data\n", encoding="utf-8"
    )

    with pytest.raises(ala.ArchiveError, match="archiveable"):
        ala.archive_slug(tmp_path, "holdme", dry_run=False, use_git=False)


def test_archive_refuses_hot_sys_path_dependent(tmp_path: Path):
    target = tmp_path / "lab" / "analysis" / "lib_slug"
    target.mkdir(parents=True)
    (target / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — library study\n", encoding="utf-8"
    )
    (target / "shared.py").write_text("VALUE = 1\n", encoding="utf-8")

    consumer = tmp_path / "lab" / "analysis" / "consumer"
    consumer.mkdir(parents=True)
    (consumer / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — consumer\n", encoding="utf-8"
    )
    (consumer / "run.py").write_text(
        'import sys\nsys.path.insert(0, "lab/analysis/lib_slug")\n',
        encoding="utf-8",
    )

    with pytest.raises(ala.ArchiveError, match="sys.path"):
        ala.archive_slug(tmp_path, "lib_slug", dry_run=False, use_git=False)


def test_archive_dry_run_writes_nothing(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — dry run\n", encoding="utf-8"
    )

    report = ala.archive_slug(tmp_path, "study", dry_run=True, use_git=False)
    assert report.dry_run is True
    assert (tmp_path / "lab/analysis/study/RESULTS.md").is_file()
    assert not (tmp_path / "lab/archive/study").exists()
    assert not (tmp_path / "lab/CATALOG.md").exists()


# ── Task 4: unarchive, --check, dependency report ─────────────────────────────


def test_unarchive_round_trip(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — round trip\n", encoding="utf-8"
    )
    tracked = {
        "study": frozenset({"lab/analysis/study/RESULTS.md"}),
    }

    ala.archive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        tracked_override=tracked,
    )
    assert (tmp_path / "lab/archive/study/RESULTS.md").is_file()
    assert (tmp_path / "lab/analysis/study/CARD.md").is_file()

    ala.unarchive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        tracked_override={"study": frozenset({"lab/analysis/study/CARD.md"})},
    )
    assert (tmp_path / "lab/analysis/study/RESULTS.md").is_file()
    assert not (tmp_path / "lab/analysis/study/CARD.md").exists()
    assert not (tmp_path / "lab/archive/study").exists()
    catalog = (tmp_path / "lab/CATALOG.md").read_text(encoding="utf-8")
    assert "## Hot bodies" in catalog and "study" in catalog
    assert "lab/archive/study" not in catalog


def test_unarchive_to_theme_when_layout_active(tmp_path: Path):
    """When any theme dir exists, unarchive with theme= restores nested hot."""
    keep = tmp_path / "lab" / "analysis" / "c1" / "keep_alive"
    keep.mkdir(parents=True)
    (keep / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — stay hot\n", encoding="utf-8"
    )

    nested = tmp_path / "lab" / "analysis" / "c1" / "study"
    nested.mkdir(parents=True)
    (nested / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — nested round trip\n", encoding="utf-8"
    )
    tracked = {
        "study": frozenset({"lab/analysis/c1/study/RESULTS.md"}),
        "keep_alive": frozenset({"lab/analysis/c1/keep_alive/RESULTS.md"}),
    }
    ala.archive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        tracked_override=tracked,
    )
    assert (tmp_path / "lab/analysis/study/CARD.md").is_file()

    ala.unarchive_slug(
        tmp_path,
        "study",
        dry_run=False,
        use_git=False,
        theme="c1",
        tracked_override={"study": frozenset({"lab/analysis/study/CARD.md"})},
    )
    restored = tmp_path / "lab" / "analysis" / "c1" / "study" / "RESULTS.md"
    assert restored.is_file()
    assert "**Theme:** c1" in restored.read_text(encoding="utf-8")
    assert not (tmp_path / "lab" / "analysis" / "study" / "CARD.md").exists()
    assert not (tmp_path / "lab" / "archive" / "study").exists()


def test_check_detects_archive_without_stub(tmp_path: Path):
    archive = tmp_path / "lab" / "archive" / "orphan"
    archive.mkdir(parents=True)
    (archive / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — orphan body\n", encoding="utf-8"
    )

    issues = ala.check_lab(tmp_path)
    assert any("orphan" in i and "stub" in i.lower() for i in issues)


def test_check_detects_full_dir_with_archiveable_disposition(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "closed_hot"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — should be archived\n", encoding="utf-8"
    )

    issues = ala.check_lab(tmp_path)
    assert any("closed_hot" in i and "archiveable" in i.lower() for i in issues)


def test_check_detects_stub_not_exactly_card(tmp_path: Path):
    stub = tmp_path / "lab" / "analysis" / "bad_stub"
    stub.mkdir(parents=True)
    (stub / "CARD.md").write_text("# bad\n", encoding="utf-8")
    (stub / "EXTRA.md").write_text("# extra\n", encoding="utf-8")
    archive = tmp_path / "lab" / "archive" / "bad_stub"
    archive.mkdir(parents=True)
    (archive / "RESULTS.md").write_text("# body\n", encoding="utf-8")

    tracked = {
        "bad_stub": frozenset(
            {"lab/analysis/bad_stub/CARD.md", "lab/analysis/bad_stub/EXTRA.md"}
        ),
    }
    issues = ala.check_lab(tmp_path, tracked_override=tracked)
    assert any("bad_stub" in i and "CARD.md" in i for i in issues)


def test_dependency_report_lists_outbound_sibling(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    other = tmp_path / "lab" / "analysis" / "other"
    other.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — done\n"
        "See [peer](../other/NOTES.md).\n",
        encoding="utf-8",
    )

    report = ala.dependency_report(tmp_path, "study")
    assert "Outbound sibling links" in report
    assert "../other/" in report or "other" in report


def test_dependency_report_lists_inbound_citation(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "target"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — inbound test\n", encoding="utf-8"
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "hit.md").write_text(
        "See lab/analysis/target/RESULTS.md for details.\n", encoding="utf-8"
    )

    report = ala.dependency_report(tmp_path, "target")
    assert "Inbound citations" in report
    assert "docs/hit.md" in report
    assert "lab/analysis/target" in report


def test_dependency_report_lists_python_coupling(tmp_path: Path):
    target = tmp_path / "lab" / "analysis" / "lib_slug"
    target.mkdir(parents=True)
    (target / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — library\n", encoding="utf-8"
    )
    consumer = tmp_path / "lab" / "analysis" / "consumer"
    consumer.mkdir(parents=True)
    (consumer / "run.py").write_text(
        'import sys\nsys.path.insert(0, "lab/analysis/lib_slug")\n',
        encoding="utf-8",
    )

    report = ala.dependency_report(tmp_path, "lib_slug")
    assert "Python path coupling" in report
    assert "consumer" in report


def test_dependency_report_lists_untracked_leftovers(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — leftovers\n", encoding="utf-8"
    )
    (analysis / "cache.pkl").write_bytes(b"\x00")

    tracked = {"study": frozenset({"lab/analysis/study/RESULTS.md"})}
    report = ala.dependency_report(
        tmp_path, "study", tracked_override=tracked
    )
    assert "Untracked leftovers" in report
    assert "cache.pkl" in report


def test_refuse_archive_if_hot_sys_path_dependent(tmp_path: Path):
    target = tmp_path / "lab" / "analysis" / "target_slug"
    target.mkdir(parents=True)
    (target / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — library study\n", encoding="utf-8"
    )

    consumer = tmp_path / "lab" / "analysis" / "consumer"
    consumer.mkdir(parents=True)
    (consumer / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — consumer\n", encoding="utf-8"
    )
    (consumer / "run.py").write_text(
        'import sys\nsys.path.insert(0, ".../lab/analysis/target_slug")\n',
        encoding="utf-8",
    )

    with pytest.raises(ala.ArchiveError, match="sys.path"):
        ala.archive_slug(tmp_path, "target_slug", dry_run=False, use_git=False)


def test_archive_dry_run_includes_dependency_report(tmp_path: Path, capsys):
    analysis = tmp_path / "lab" / "analysis" / "study"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — dry run report\n", encoding="utf-8"
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "hit.md").write_text("lab/analysis/study\n", encoding="utf-8")

    ala.archive_slug(tmp_path, "study", dry_run=True, use_git=False)
    captured = capsys.readouterr()
    assert "Inbound citations" in captured.out
    assert "docs/hit.md" in captured.out


def test_check_cli_exits_nonzero(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis" / "drift"
    analysis.mkdir(parents=True)
    (analysis / "RESULTS.md").write_text(
        "**Disposition:** FALSIFIED — drift case\n", encoding="utf-8"
    )

    rc = ala.main(["--root", str(tmp_path), "--check"])
    assert rc == 1


def test_check_detects_stale_catalog_active_body_under_archive(tmp_path: Path):
    """Active/HOLD row in CATALOG with body under lab/archive/ is drift."""
    holdme = tmp_path / "lab" / "analysis" / "holdme"
    holdme.mkdir(parents=True)
    (holdme / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting for data\n", encoding="utf-8"
    )

    stale = ala.render_catalog(
        [
            ala.CatalogRow(
                slug="holdme",
                theme="_inbox",
                status="HOLD",
                one_liner="waiting for data",
                card="lab/analysis/holdme/RESULTS.md",
                body="lab/archive/holdme/",
                heavy="—",
                closed="—",
            )
        ]
    )
    ala.write_catalog(tmp_path, stale)

    issues = ala.check_lab(tmp_path)
    assert any("CATALOG.md stale vs scan" in i for i in issues)


def test_check_detects_stale_catalog_archived_row_missing_on_disk(tmp_path: Path):
    """Archived catalog row with no stub or archive body on disk is drift."""
    stale = ala.render_catalog(
        [
            ala.CatalogRow(
                slug="ghost",
                theme="—",
                status="CLOSED",
                one_liner="gone study",
                card="lab/analysis/ghost/CARD.md",
                body="lab/archive/ghost/",
                heavy="—",
                closed="2026-07-01",
            )
        ]
    )
    ala.write_catalog(tmp_path, stale)

    issues = ala.check_lab(tmp_path)
    assert any("CATALOG.md stale vs scan" in i for i in issues)


def test_check_ok_when_catalog_matches_scan(tmp_path: Path):
    holdme = tmp_path / "lab" / "analysis" / "holdme"
    holdme.mkdir(parents=True)
    (holdme / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting for data\n", encoding="utf-8"
    )

    ala.regenerate_catalog(tmp_path)

    issues = ala.check_lab(tmp_path)
    assert "CATALOG.md stale vs scan" not in issues


def test_check_catalog_only_ignores_unstubbed_close(tmp_path: Path):
    """Always-on gate: stale catalog fails; unstubbed FALSIFIED does not."""
    closed = tmp_path / "lab" / "analysis" / "done_study"
    closed.mkdir(parents=True)
    (closed / "RESULTS.md").write_text(
        "**Verdict:** FALSIFIED — terminal\n", encoding="utf-8"
    )
    ala.regenerate_catalog(tmp_path)

    full = ala.check_lab(tmp_path)
    assert any("unstubbed close" in i for i in full)

    catalog_only = ala.check_lab(tmp_path, catalog_only=True)
    assert catalog_only == []

    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 0


def test_full_dir_archiveable_keeps_disposition_and_hot_yes(tmp_path: Path):
    """Unstubbed FALSIFIED stays Active with honest disposition; C2 joins to hot."""
    closed = tmp_path / "lab" / "analysis" / "done_study"
    closed.mkdir(parents=True)
    (closed / "RESULTS.md").write_text(
        "**Verdict:** FALSIFIED — terminal edge\n", encoding="utf-8"
    )
    rows = ala.scan_lab(tmp_path)
    assert len(rows) == 1
    assert rows[0].status == "FALSIFIED"
    assert rows[0].hot == "yes"
    text = ala.render_catalog(rows)
    active = text.split("## Archived")[0]
    assert "## Hot bodies" in active and "done_study" in active
    assert "| FALSIFIED | yes |" in active


def test_check_catalog_only_fails_when_stale(tmp_path: Path):
    holdme = tmp_path / "lab" / "analysis" / "holdme"
    holdme.mkdir(parents=True)
    (holdme / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting\n", encoding="utf-8"
    )
    (tmp_path / "lab" / "CATALOG.md").write_text(
        "# Lab analysis catalog\n\n## Active\n\n| slug |\n|---|\n| ghost |\n",
        encoding="utf-8",
    )

    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 1


def test_catalog_only_requires_check_flag(tmp_path: Path):
    rc = ala.main(["--root", str(tmp_path), "--catalog-only"])
    assert rc == 1


# ── heavy-column worktree tolerance ───────────────────────────────────────────
# Design: docs/superpowers/specs/
#   2026-07-24-lab-catalog-check-heavy-column-worktree-tolerance-design.md


@pytest.mark.parametrize("annotation", ["inputs gitignored", "pkl gitignored"])
def test_catalog_only_tolerates_absent_gitignored_heavy(
    tmp_path: Path, annotation: str, capsys
):
    """Bare worktree / clone: the committed catalog annotates `heavy` for a study
    whose gitignored inputs/ + *.pkl were never checked out, so a fresh scan sees
    '—'. The always-on catalog-only gate must NOT hard-fail on that heavy-column
    downgrade (mirrors the sibling manifest gates' public-clone soft-degrade); it
    warns instead."""
    study = tmp_path / "lab" / "analysis" / "heavy_study"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Disposition:** HOLD — waiting for data\n", encoding="utf-8"
    )
    # No inputs/ dir and no *.pkl on disk → a fresh scan yields heavy '—'.
    scanned = ala.scan_lab(tmp_path)
    assert [r.heavy for r in scanned] == ["—"]

    # Committed catalog was generated on the primary tree, where the heavy
    # artifacts exist → the column carries the annotation.
    committed = [
        ala.CatalogRow(
            slug=r.slug,
            theme=r.theme,
            status=r.status,
            one_liner=r.one_liner,
            card=r.card,
            body=r.body,
            heavy=annotation,
            closed=r.closed,
        )
        for r in scanned
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))

    assert ala.check_lab(tmp_path, catalog_only=True) == []
    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 0
    # No silent cap: the un-verifiable heavy row is surfaced as a warning.
    assert "heavy_study" in capsys.readouterr().err


def test_catalog_only_still_fails_on_real_drift_with_heavy_absent(tmp_path: Path):
    """The heavy-column tolerance must not mask a genuine slug/status drift that
    coexists with a tolerable heavy downgrade."""
    a = tmp_path / "lab" / "analysis" / "study_a"
    a.mkdir(parents=True)
    (a / "RESULTS.md").write_text(
        "**Disposition:** HOLD — real study\n", encoding="utf-8"
    )
    scanned = ala.scan_lab(tmp_path)  # study_a HOLD, heavy '—'

    committed = [
        # tolerable heavy downgrade on the real study …
        ala.CatalogRow(
            slug="study_a",
            theme=scanned[0].theme,
            status=scanned[0].status,
            one_liner=scanned[0].one_liner,
            card=scanned[0].card,
            body=scanned[0].body,
            heavy="pkl gitignored",
            closed=scanned[0].closed,
        ),
        # … plus a phantom slug not on disk (real drift → must still fail).
        ala.CatalogRow(
            slug="ghost",
            theme="_inbox",
            status="ACTIVE",
            one_liner="—",
            card="—",
            body="lab/analysis/ghost/",
            heavy="—",
            closed="—",
        ),
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))

    assert ala.check_lab(tmp_path, catalog_only=True) == ["CATALOG.md stale vs scan"]


def test_catalog_only_fails_when_heavy_present_but_uncommitted(tmp_path: Path):
    """Inverse direction: heavy artifacts ARE present on disk but the committed
    catalog does not annotate them → real staleness, must hard-fail (the
    tolerance is one-directional: committed-annotation→scanned-'—' only)."""
    study = tmp_path / "lab" / "analysis" / "s"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Disposition:** HOLD — x\n", encoding="utf-8"
    )
    (study / "inputs").mkdir()
    (study / "inputs" / "d.csv").write_text("a,b\n", encoding="utf-8")
    scanned = ala.scan_lab(tmp_path)
    assert scanned[0].heavy == "inputs gitignored"

    committed = [
        ala.CatalogRow(
            slug="s",
            theme=scanned[0].theme,
            status=scanned[0].status,
            one_liner=scanned[0].one_liner,
            card=scanned[0].card,
            body=scanned[0].body,
            heavy="—",
            closed=scanned[0].closed,
        )
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))

    assert ala.check_lab(tmp_path, catalog_only=True) == ["CATALOG.md stale vs scan"]




def test_clean_one_liner_strips_hand_status_parenthetical():
    assert ala._clean_one_liner(
        "ACTIVE (one headline RETRACTED 2026-08-02) — faithful sweep",
        "ACTIVE",
    ) == "faithful sweep"
    assert ala._clean_one_liner(
        "ACTIVE (K columns superseded 2026-08-04)",
        "ACTIVE",
    ) == "ACTIVE (K columns superseded 2026-08-04)"
    # Dated archive prefixes must not be stripped (no space before em-dash after ).
    assert ala._clean_one_liner(
        "FALSIFIED (2026-06-17)** — directional signal is",
        "FALSIFIED",
    ) == "FALSIFIED (2026-06-17)** — directional signal is"


def test_catalog_tolerates_hand_status_parenthetical(tmp_path: Path):
    """M11/M45: hand-annotated CATALOG Status must stay green vs bare scan token."""
    study = tmp_path / "lab" / "analysis" / "flagged"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Status:** ACTIVE (one headline RETRACTED) — body one-liner\n",
        encoding="utf-8",
    )
    scanned = ala.scan_lab(tmp_path)
    assert scanned[0].status == "ACTIVE"
    assert scanned[0].one_liner == "body one-liner"
    committed = [
        ala.CatalogRow(
            slug=scanned[0].slug,
            theme=scanned[0].theme,
            status="ACTIVE (one headline RETRACTED)",
            one_liner=scanned[0].one_liner,
            card=scanned[0].card,
            body=scanned[0].body,
            heavy=scanned[0].heavy,
            closed=scanned[0].closed,
        )
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    assert ala.check_lab(tmp_path, catalog_only=True) == []



def test_catalog_only_tolerates_unverifiable_one_liner(tmp_path: Path, capsys):
    """Mid-campaign hot body with no RESULTS*/README source card: scan emits
    one-liner empty, but the committed catalog may retain hand-authored prose.
    Catalog-only freshness must WARN, not hard-fail (same class as heavy-column
    soft-degrade; third live firing: msl_c3_m2k_2026-08 at 9bcf3cb)."""
    study = tmp_path / "lab" / "analysis" / "mid_campaign"
    study.mkdir(parents=True)
    # STAGE-only body — choose_source_card returns None → one_liner empty.
    (study / "STAGE1.md").write_text(
        "**Status:** STAGE-1 PASS — not a catalog source card\n", encoding="utf-8"
    )
    scanned = ala.scan_lab(tmp_path)
    assert scanned[0].one_liner == "—"
    assert scanned[0].status == "ACTIVE"

    committed = [
        ala.CatalogRow(
            slug=r.slug,
            theme=r.theme,
            status=r.status,
            one_liner="hand-authored mid-campaign prose retained in CATALOG",
            card=r.card,
            body=r.body,
            heavy=r.heavy,
            closed=r.closed,
        )
        for r in scanned
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))

    assert ala.check_lab(tmp_path, catalog_only=True) == []
    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 0
    err = capsys.readouterr().err
    assert "mid_campaign" in err
    assert "one-liner" in err


def test_catalog_only_tolerates_120_char_truncation(tmp_path: Path):
    """Hand-authored CATALOG one-liner longer than parse_disposition's 120-cap.

    Scan emits the truncated form; disk keeps the full Status prose. Must not
    hard-fail — same direction as the empty-scan soft-degrade, but silent
    because the cap is mechanical.
    """
    study = tmp_path / "lab" / "analysis" / "long_line"
    study.mkdir(parents=True)
    full = (
        "W1 pattern extended to all 7 Bulenox/BluSky trailing tiers "
        "with a long residual clause that exceeds the one-liner cap "
        "and then some extra measured residual so the 120-char cut fires"
    )
    assert len(full) > 120
    (study / "RESULTS.md").write_text(
        f"**Theme:** c1\n**Status:** ACTIVE — {full}\n",
        encoding="utf-8",
    )
    scanned = ala.scan_lab(tmp_path)
    assert scanned[0].one_liner.endswith("...")
    assert len(scanned[0].one_liner) <= 120
    assert ala._scan_one_liner_is_truncation(scanned[0].one_liner, full)

    committed = [
        ala.CatalogRow(
            slug=r.slug,
            theme=r.theme,
            status=r.status,
            one_liner=full,
            card=r.card,
            body=r.body,
            heavy=r.heavy,
            closed=r.closed,
        )
        for r in scanned
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    assert ala.check_lab(tmp_path, catalog_only=True) == []
    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 0


def test_catalog_only_tolerates_hand_authored_summary_vs_truncation(tmp_path: Path):
    """A concise catalog summary must win over parse_disposition's 120-cap.

    Scan still emits the truncated Status fragment; disk keeps a complete
    hand-authored one-liner that is *not* a prefix-extension of that fragment.
    Must not hard-fail — same class as keeping the untruncated Status prose.
    """
    study = tmp_path / "lab" / "analysis" / "long_line"
    study.mkdir(parents=True)
    full = (
        "W1 pattern extended to all 7 Bulenox/BluSky trailing tiers "
        "with a long residual clause that exceeds the one-liner cap "
        "and then some extra measured residual so the 120-char cut fires"
    )
    summary = "W1 extends to all 7 trailing tiers; residual stays unpublished"
    assert len(full) > 120
    assert not summary.endswith("...")
    assert not full.startswith(summary)
    (study / "RESULTS.md").write_text(
        f"**Theme:** c1\n**Status:** ACTIVE — {full}\n",
        encoding="utf-8",
    )
    scanned = ala.scan_lab(tmp_path)
    assert scanned[0].one_liner.endswith("...")
    assert len(scanned[0].one_liner) <= 120
    assert ala._scan_one_liner_is_truncation(scanned[0].one_liner, summary)

    committed = [
        ala.CatalogRow(
            slug=r.slug,
            theme=r.theme,
            status=r.status,
            one_liner=summary,
            card=r.card,
            body=r.body,
            heavy=r.heavy,
            closed=r.closed,
        )
        for r in scanned
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    assert ala.check_lab(tmp_path, catalog_only=True) == []
    rc = ala.main(["--root", str(tmp_path), "--check", "--catalog-only"])
    assert rc == 0


def test_catalog_only_still_fails_on_nonempty_one_liner_drift(tmp_path: Path):
    """Soft-degrade must not mask real one-liner drift when both sides are prose."""
    study = tmp_path / "lab" / "analysis" / "live_study"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Disposition:** ACTIVE — real one-liner from source card\n",
        encoding="utf-8",
    )
    scanned = ala.scan_lab(tmp_path)
    assert not ala._is_empty_one_liner(scanned[0].one_liner)

    committed = [
        ala.CatalogRow(
            slug=scanned[0].slug,
            theme=scanned[0].theme,
            status=scanned[0].status,
            one_liner="WRONG prose",
            card=scanned[0].card,
            body=scanned[0].body,
            heavy=scanned[0].heavy,
            closed=scanned[0].closed,
        )
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    assert ala.check_lab(tmp_path, catalog_only=True) == ["CATALOG.md stale vs scan"]


def test_catalog_hand_status_still_fails_on_one_liner_drift(tmp_path: Path):
    study = tmp_path / "lab" / "analysis" / "flagged"
    study.mkdir(parents=True)
    (study / "RESULTS.md").write_text(
        "**Status:** ACTIVE (note) — real one-liner\n",
        encoding="utf-8",
    )
    scanned = ala.scan_lab(tmp_path)
    committed = [
        ala.CatalogRow(
            slug=scanned[0].slug,
            theme=scanned[0].theme,
            status="ACTIVE (note)",
            one_liner="WRONG",
            card=scanned[0].card,
            body=scanned[0].body,
            heavy=scanned[0].heavy,
            closed=scanned[0].closed,
        )
    ]
    ala.write_catalog(tmp_path, ala.render_catalog(committed))
    assert ala.check_lab(tmp_path, catalog_only=True) == ["CATALOG.md stale vs scan"]


def test_catalog_duplicate_slug_active_and_archived_hard_fails(tmp_path: Path):
    """Planted Active+Archived phantom must hard-fail — not silently overwrite.

    2026-08-13: ``msl_c1_mym_2026-08`` / ``msl_c2_mgc_2026-08`` were archived
    (``b2e3eec``), then PR #798 re-added phantom Active rows. ``--check
    --catalog-only`` false-passed because ``_partition_catalog`` keyed only by
    slug and the Archived row overwrote the Active one — slug sets matched the
    scan and the phantom drift was discarded. Co-Active ``keep_alive`` keeps
    Active-section structure identical so the blind spot is the only path.
    Rows are now keyed by ``(section, slug)`` so the phantom Active key is a
    set delta vs an Archived-only scan.
    """
    keep = tmp_path / "lab" / "analysis" / "c1" / "keep_alive"
    keep.mkdir(parents=True)
    (keep / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — still hot\n", encoding="utf-8"
    )
    stub = tmp_path / "lab" / "analysis" / "dup_slug"
    stub.mkdir(parents=True)
    (stub / "CARD.md").write_text(
        "# dup_slug\n\n**Disposition:** CLOSED — archived\n"
        "**Archived:** 2026-08-13\n",
        encoding="utf-8",
    )
    body = tmp_path / "lab" / "archive" / "dup_slug"
    body.mkdir(parents=True)
    (body / "RESULTS.md").write_text(
        "**Disposition:** CLOSED — archived\n", encoding="utf-8"
    )
    tracked = {
        "keep_alive": frozenset({"lab/analysis/c1/keep_alive/RESULTS.md"}),
        "dup_slug": frozenset({"lab/analysis/dup_slug/CARD.md"}),
    }
    scanned = ala.scan_lab(tmp_path, tracked_override=tracked)
    by_slug = {r.slug: r for r in scanned}
    assert set(by_slug) == {"keep_alive", "dup_slug"}
    assert by_slug["dup_slug"].body.startswith("lab/archive/")

    phantom = ala.CatalogRow(
        slug="dup_slug",
        theme="c1",
        status="ACTIVE",
        one_liner="phantom Active re-added by stale merge",
        card="—",
        body="lab/analysis/c1/dup_slug/",
        heavy="—",
        closed="—",
    )
    planted = ala.render_catalog([*scanned, phantom])
    assert planted.count("| dup_slug |") == 2
    ala.write_catalog(tmp_path, planted)

    # Pure comparator: expected is scan-faithful (Archived only for dup_slug);
    # disk has phantom Active + Archived — (section, slug) set must diverge.
    expected = ala.render_catalog(scanned)
    disk_keys = set(ala._partition_catalog(planted)[1])
    exp_keys = set(ala._partition_catalog(expected)[1])
    assert ("active", "dup_slug") in disk_keys
    assert ("active", "dup_slug") not in exp_keys
    issues, _warnings = ala._compare_catalog(planted, expected)
    assert issues == ["CATALOG.md stale vs scan"], (
        "phantom Active beside Archived must not yield a false freshness pass"
    )

    assert ala.check_lab(
        tmp_path, tracked_override=tracked, catalog_only=True
    ) == ["CATALOG.md stale vs scan"]
    rc = ala.main(
        [
            "--root",
            str(tmp_path),
            "--check",
            "--catalog-only",
        ]
    )
    assert rc == 1


# ── Task 5: --check honesty rules + inventory CLI ─────────────────────────────


def test_inventory_classifies_archiveable_hold_active(tmp_path: Path):
    analysis = tmp_path / "lab" / "analysis"
    closed = analysis / "c1" / "done_study"
    closed.mkdir(parents=True)
    (closed / "RESULTS.md").write_text(
        "**Theme:** c1\n**Disposition:** CLOSED — terminal\n", encoding="utf-8"
    )
    held = analysis / "orb" / "wait_study"
    held.mkdir(parents=True)
    (held / "RESULTS.md").write_text(
        "**Theme:** orb\n**Disposition:** HOLD — waiting\n", encoding="utf-8"
    )
    live = analysis / "striker" / "live_study"
    live.mkdir(parents=True)
    (live / "RESULTS.md").write_text(
        "**Theme:** striker\n**Status:** ACTIVE — measuring\n", encoding="utf-8"
    )

    rows = {r.slug: r for r in ala.inventory_lab(tmp_path)}
    assert rows["done_study"].cls == "archiveable"
    assert rows["done_study"].status == "CLOSED"
    assert rows["done_study"].theme == "c1"
    assert rows["wait_study"].cls == "hold"
    assert rows["live_study"].cls == "active"
    assert "measuring" in rows["live_study"].one_liner


def test_check_theme_mismatch_issue_string(tmp_path: Path):
    hot = tmp_path / "lab" / "analysis" / "c1" / "misplaced"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text(
        "**Theme:** orb\n**Status:** ACTIVE — wrong theme dir\n",
        encoding="utf-8",
    )
    ala.regenerate_catalog(tmp_path)

    issues = ala.check_lab(tmp_path)
    assert "theme mismatch: misplaced dir=c1 stamp=orb" in issues


def test_check_flat_full_dir_remnant_warns_when_theme_dirs_exist(
    tmp_path: Path, capsys
):
    nested = tmp_path / "lab" / "analysis" / "c1" / "nested"
    nested.mkdir(parents=True)
    (nested / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — nested\n", encoding="utf-8"
    )
    flat = tmp_path / "lab" / "analysis" / "still_flat"
    flat.mkdir(parents=True)
    (flat / "RESULTS.md").write_text(
        "**Status:** ACTIVE — remnant\n", encoding="utf-8"
    )
    ala.regenerate_catalog(tmp_path)

    issues = ala.check_lab(tmp_path)
    err = capsys.readouterr().err
    assert "WARN flat full dir remnant: still_flat" in err
    assert not any("flat full dir remnant" in i for i in issues)


def test_warn_new_slug_same_theme_collision_emits_stderr(tmp_path: Path, capsys):
    """Untracked hot body under a theme that already has an Active CATALOG row.

    ADR 2026-08-13 §2 leg 3: report-only WARN (never an issue / exit-code bit).
    """
    catalog = ala.render_catalog(
        [
            ala.CatalogRow(
                slug="orb_existing",
                theme="orb",
                status="ACTIVE",
                one_liner="prior orb work",
                card="lab/analysis/orb/orb_existing/RESULTS.md",
                body="lab/analysis/orb/orb_existing/",
                heavy="—",
                closed="—",
            )
        ]
    )
    ala.write_catalog(tmp_path, catalog)

    newbie = tmp_path / "lab" / "analysis" / "orb" / "orb_new_candidate"
    newbie.mkdir(parents=True)
    (newbie / "RESULTS.md").write_text(
        "**Theme:** orb\n**Status:** ACTIVE — not yet catalogued\n",
        encoding="utf-8",
    )

    # Empty override → every slug reports as untracked (git ls-files bypass).
    ala.warn_new_slug_same_theme_collisions(tmp_path, tracked_override={})
    err = capsys.readouterr().err
    assert "WARN new-slug same-theme collision:" in err
    assert "lab/analysis/orb/orb_new_candidate/" in err
    assert "theme 'orb'" in err
    assert "orb_existing: prior orb work" in err


def test_warn_new_slug_same_theme_collision_silent_without_overlap(
    tmp_path: Path, capsys
):
    """Untracked hot body under a theme with no Active CATALOG peers → no WARN."""
    catalog = ala.render_catalog(
        [
            ala.CatalogRow(
                slug="c1_existing",
                theme="c1",
                status="ACTIVE",
                one_liner="prior c1 work",
                card="lab/analysis/c1/c1_existing/RESULTS.md",
                body="lab/analysis/c1/c1_existing/",
                heavy="—",
                closed="—",
            )
        ]
    )
    ala.write_catalog(tmp_path, catalog)

    newbie = tmp_path / "lab" / "analysis" / "orb" / "orb_solo"
    newbie.mkdir(parents=True)
    (newbie / "RESULTS.md").write_text(
        "**Theme:** orb\n**Status:** ACTIVE — different theme from catalog\n",
        encoding="utf-8",
    )

    ala.warn_new_slug_same_theme_collisions(tmp_path, tracked_override={})
    err = capsys.readouterr().err
    assert "WARN new-slug same-theme collision:" not in err
    assert "orb_solo" not in err


def test_empty_one_liner_gated_by_require_one_liners(tmp_path: Path):
    hot = tmp_path / "lab" / "analysis" / "c1" / "blank"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text(
        "**Theme:** c1\n# blank study\nNo status stamp yet.\n",
        encoding="utf-8",
    )
    ala.regenerate_catalog(tmp_path)

    # Wave 3: full check hard-fails empty Active/HOLD one-liners by default.
    assert "empty one-liner: blank" in ala.check_lab(tmp_path)
    assert not any(
        "empty one-liner" in i
        for i in ala.check_lab(tmp_path, require_one_liners=False)
    )



def test_inventory_cli_prints_tsv(tmp_path: Path, capsys):
    hot = tmp_path / "lab" / "analysis" / "c1" / "live_study"
    hot.mkdir(parents=True)
    (hot / "RESULTS.md").write_text(
        "**Theme:** c1\n**Status:** ACTIVE — measuring\n", encoding="utf-8"
    )

    rc = ala.main(["--root", str(tmp_path), "--inventory"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "live_study\tactive\tc1\tACTIVE\t" in out
    assert "measuring" in out


def test_truncate_one_liner_does_not_slice_campaign_id():
    raw = (
        "H_B = 0, STOP / NULL per PREREG F7 · closure: "
        "docs/briefs/closures/Q-TNEC-ENV-1-closure.md"
    )
    out = ala._truncate_one_liner(raw, limit=80)
    assert "Q-TNEC-ENV-1" in out
    assert "Q-TNEC-ENV..." not in out


def test_git_mv_falls_back_on_cross_device_link(tmp_path: Path, monkeypatch):
    """Overlay / bind-mount workspaces raise EXDEV on ``git mv``; copy+rm must land."""
    src = tmp_path / "from_dir"
    dst = tmp_path / "to_dir"
    src.mkdir()
    (src / "card.md").write_text("x\n", encoding="utf-8")

    def fake_run(cmd, cwd=None, capture_output=False, text=False, check=False):
        if cmd[:2] == ["git", "mv"]:
            return ala.subprocess.CompletedProcess(
                cmd, 128, stdout="", stderr="fatal: Invalid cross-device link\n"
            )
        if cmd[:3] == ["git", "rm", "-r"]:
            return ala.subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        if cmd[:3] == ["git", "add", "-A"]:
            return ala.subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"unexpected cmd {cmd}")

    monkeypatch.setattr(ala.subprocess, "run", fake_run)
    ala._git_mv(tmp_path, src, dst)
    assert (dst / "card.md").read_text(encoding="utf-8") == "x\n"
    assert not src.exists()
