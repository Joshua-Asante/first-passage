"""Tests for the INQHIORI Sentinel Tier-1 scanners.

C1 (headroom-retraction skew) and C2 (slate precondition gaps) are the live
findings the probe surfaced this session; they are the regression fixtures here.
"""
import shutil
import subprocess
from datetime import date, timedelta
from pathlib import Path

import pytest

from sentinel.report import render_run
from sentinel.scan import (
    Finding,
    ROUTING,
    SLATE_DATE,
    _corresponds,
    _git_lines,
    _is_prereg_artifact,
    _is_result_artifact,
    _pair_violations,
    obligation_scan,
    precondition_scan,
    preregistration_scan,
    sessions_scan,
    skew_scan,
)


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# --- Finding shape -------------------------------------------------------- #

def test_finding_shape():
    f = Finding(id="X", category="skew", routing="Action", summary="s", source="CLAUDE.md:1", next_step="n")
    assert f.routing in ROUTING
    assert f.category == "skew"


# --- skew_scan (C1) ------------------------------------------------------- #

def test_skew_detects_headroom_retraction(tmp_path):
    _write(tmp_path, "CLAUDE.md", "anchor: 99.83% pass; p99 DD 0.63pp headroom; tighter than prior.\n")
    _write(tmp_path, "docs/mc_anchor_history.md",
           "Q-SWAP-2 ... provisionally retracted ... under fixed-1R modeling (0.45pp).\n")
    findings = skew_scan(tmp_path)
    assert len(findings) == 1
    assert findings[0].id == "SKEW-headroom-fixed1r"
    assert findings[0].category == "skew"
    assert findings[0].routing == "Action"
    assert findings[0].source.startswith("CLAUDE.md:")


def test_skew_clean_when_caveat_present(tmp_path):
    _write(tmp_path, "CLAUDE.md",
           "anchor: 99.83% pass; p99 DD 0.63pp headroom (under fixed-1R per M-SWAP-1: 0.45pp).\n")
    _write(tmp_path, "docs/mc_anchor_history.md",
           "Q-SWAP-2 ... provisionally retracted ... under fixed-1R modeling.\n")
    assert skew_scan(tmp_path) == []


def test_skew_clean_when_no_retraction_in_history(tmp_path):
    _write(tmp_path, "CLAUDE.md", "anchor: p99 DD 0.63pp headroom.\n")
    _write(tmp_path, "docs/mc_anchor_history.md", "no retraction here.\n")
    assert skew_scan(tmp_path) == []


# --- obligation_scan (C2 part 1) ------------------------------------------ #

def test_obligation_surfaces_near_date(tmp_path):
    _write(tmp_path, "CLAUDE.md",
           "Forward revert trigger: run regime-check quarterly (next dates: 2026-08-08, 2026-11-08).\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert any("2026-08-08" in f.summary for f in findings)
    assert all(f.category == "obligation" for f in findings)
    assert all(f.routing in ("Action", "Forward") for f in findings)


def test_obligation_ignores_far_date(tmp_path):
    _write(tmp_path, "CLAUDE.md", "review trigger next: 2026-11-08.\n")
    assert obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []


def test_obligation_requires_keyword(tmp_path):
    _write(tmp_path, "CLAUDE.md", "The lock landed on 2026-08-08 after testing.\n")
    assert obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []


# --- precondition_scan (C2 part 2) ---------------------------------------- #

def test_precondition_flags_unverified_calendar(tmp_path):
    _write(tmp_path, "ops/instruments/USDCAD.md",
           "## Regime calendar (2020–2026)\n\n"
           "| Year | Tag |\n|---|---|\n"
           "| 2025 | [M] |\n| 2026 | [L] |\n"
           f"Maintenance: one verification pass on [M]/[L] cells is due before the "
           f"{SLATE_DATE.isoformat()} slate.\n")
    findings = precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=46), horizon_days=60)
    assert "PRECOND-regime-calendar-unverified" in {f.id for f in findings}
    assert all(f.category == "precondition" for f in findings)


def test_precondition_flags_empty_trip_log(tmp_path):
    _write(tmp_path, "docs/notes/audits/rule-2-trip-log.md",
           "| Date | Loop class | ... |\n|---|---|---|\n| 2026-06-16 | OUTER | baseline |\n")
    findings = precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=46), horizon_days=60)
    assert "PRECOND-rule2-triplog-starved" in {f.id for f in findings}


def test_precondition_clean_when_met(tmp_path):
    _write(tmp_path, "ops/instruments/USDCAD.md",
           "## Regime calendar (2020–2026)\n\n"
           "| Year | Tag |\n|---|---|\n"
           "| 2025 | [H] |\n| 2026 | [H] |\n")
    _write(tmp_path, "docs/notes/audits/rule-2-trip-log.md",
           "|---|\n| 2026-06-16 | OUTER | a |\n| 2026-06-20 | INNER | b |\n")
    assert precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=46), horizon_days=60) == []


def test_precondition_clean_when_slate_verification_discharged(tmp_path):
    """A [M] cell the slate's own verification pass deliberately left in place is not
    an outstanding precondition. Anchor: USDCAD.md's 2026-07-02 R6 discharge holds
    2026 YTD at [M] pending year-end, which the cell-only check mis-flagged weekly."""
    _write(tmp_path, "ops/instruments/USDCAD.md",
           "## Regime calendar (2020–2026)\n\n"
           "| Year | Tag |\n|---|---|\n"
           "| 2025 | [H] |\n| 2026 YTD | [M] |\n\n"
           f"**{SLATE_DATE.isoformat()} verification — DISCHARGED 2026-07-02** (programme-audit R6): "
           "2025 [M]→[H]; 2026 YTD [L]→[M] (partial year — full-year label at year-end).\n")
    findings = precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=12), horizon_days=60)
    assert "PRECOND-regime-calendar-unverified" not in {f.id for f in findings}


def test_precondition_flags_when_discharge_names_another_slate(tmp_path):
    """Negative control: a discharge must name THIS slate to suppress. A stale
    discharge for a prior/other slate leaves the pass outstanding."""
    other_slate = SLATE_DATE - timedelta(days=92)  # the just-superseded slate
    _write(tmp_path, "ops/instruments/USDCAD.md",
           "## Regime calendar (2020–2026)\n\n"
           "| Year | Tag |\n|---|---|\n"
           "| 2026 YTD | [M] |\n\n"
           f"**{other_slate.isoformat()} verification — DISCHARGED 2026-07-02** (a different slate).\n")
    findings = precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=12), horizon_days=60)
    assert "PRECOND-regime-calendar-unverified" in {f.id for f in findings}


def test_precondition_dormant_far_from_slate(tmp_path):
    _write(tmp_path, "ops/instruments/USDCAD.md",
           "## Regime calendar (2020–2026)\n\n"
           "| Year | Tag |\n|---|---|\n"
           f"| 2026 | [L] |\nverification due before {SLATE_DATE.isoformat()}.\n")
    assert precondition_scan(tmp_path, asof=SLATE_DATE - timedelta(days=180), horizon_days=60) == []


def test_slate_date_is_pinned():
    assert SLATE_DATE == date(2026, 11, 8)


# --- obligation_scan: docs/adr/* trigger-schedule aggregation (X2/X3) ----- #
# Gate-stack audit 2026-08-03 (docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md):
# the design spec named docs/adr/* as an obligation_scan surface; the
# implementation plan silently narrowed it away. Naive per-line scanning of
# 100 ADR files reproduces the "ADR-date noise" the original curation avoided,
# so this scan is restricted to the template's own **Trigger check schedule:**
# / **Check schedule:** field and aggregates by DATE, not by file.

def test_obligation_adr_trigger_single_file(tmp_path):
    _write(tmp_path, "docs/adr/2026-07-01-example.md",
           "# ADR\n\n**Status:** Accepted\n\n"
           "**Trigger check schedule:** rides the standing quarterly programme audit "
           "— next **2026-08-08**, then 2026-11-08.\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    ids = {f.id for f in findings}
    assert "OBLIG-adr-triggers-2026-08-08" in ids
    hit = next(f for f in findings if f.id == "OBLIG-adr-triggers-2026-08-08")
    assert "1 ADR" in hit.summary
    assert "docs/adr/2026-07-01-example.md" in hit.summary


def test_obligation_adr_triggers_aggregate_across_files(tmp_path):
    """The core X2 fix: N ADRs naming the same trigger date collapse to ONE
    Finding, not N — this is what keeps docs/adr/* from being noisy."""
    for i in range(5):
        _write(tmp_path, f"docs/adr/2026-07-0{i+1}-example.md",
               "**Trigger check schedule:** rides the standing quarterly review "
               "(next 2026-08-08).\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    adr_findings = [f for f in findings if f.id == "OBLIG-adr-triggers-2026-08-08"]
    assert len(adr_findings) == 1
    assert "5 ADR" in adr_findings[0].summary


def test_obligation_adr_trigger_ignores_incidental_dates(tmp_path):
    """A date elsewhere in the ADR body (Decision date, Change history, an
    unrelated 'reviewed on' sentence) must NOT fire — only the trigger field
    itself. This is the precision guarantee the whole design rests on."""
    _write(tmp_path, "docs/adr/2026-07-01-example.md",
           "# ADR\n\n**Decision date:** 2026-08-08\n\n"
           "The operator reviewed this on 2026-08-08 before the audit gate.\n\n"
           "**Trigger check schedule:** event-driven; no calendar date.\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert not any(f.id.startswith("OBLIG-adr-triggers-") for f in findings)


def test_obligation_adr_trigger_excludes_index(tmp_path):
    _write(tmp_path, "docs/adr/INDEX.md",
           "**Trigger check schedule:** 2026-08-08 (should never fire — not a real ADR).\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert not any(f.id.startswith("OBLIG-adr-triggers-") for f in findings)


def test_obligation_adr_trigger_wrapped_continuation(tmp_path):
    """The field wraps onto a second line for long entries — must still parse."""
    _write(tmp_path, "docs/adr/2026-07-01-example.md",
           "**Trigger check schedule:** at the both-halves re-run's completion, and in any case\n"
           "**before** the first armed send, whichever comes first — no later than\n"
           "2026-08-08.\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert any(f.id == "OBLIG-adr-triggers-2026-08-08" for f in findings)


def test_obligation_adr_trigger_stops_at_next_field(tmp_path):
    """A date in the NEXT bold field (past the trigger schedule) must not leak in."""
    _write(tmp_path, "docs/adr/2026-07-01-example.md",
           "**Trigger check schedule:** event-driven; no calendar date.\n\n"
           "**Related:** some ADR dated 2026-08-08.\n")
    findings = obligation_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert not any(f.id.startswith("OBLIG-adr-triggers-") for f in findings)


# --- precondition_scan: STATE.md board-sync (X2/X3, generalizing SLATE_DATE) #

def test_board_sync_flags_gap(tmp_path):
    _write(tmp_path, "docs/adr/2026-07-01-a.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "docs/adr/2026-07-02-b.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "STATE.md", "### 2026-08-08\n\n- unrelated line, no ADR link\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    hit = next(f for f in findings if f.id == "PRECOND-board-sync-2026-08-08")
    assert "2 ADR" in hit.summary and "0 of them" in hit.summary


def test_board_sync_partial_gap_counts_correctly(tmp_path):
    _write(tmp_path, "docs/adr/2026-07-01-a.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "docs/adr/2026-07-02-b.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "STATE.md",
           "### 2026-08-08\n\n- [a ADR](docs/adr/2026-07-01-a.md)\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    hit = next(f for f in findings if f.id == "PRECOND-board-sync-2026-08-08")
    assert "1 of them" in hit.summary


def test_board_sync_clean_when_fully_referenced(tmp_path):
    _write(tmp_path, "docs/adr/2026-07-01-a.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "STATE.md",
           "### 2026-08-08\n\n- [a ADR](docs/adr/2026-07-01-a.md)\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert not any(f.id.startswith("PRECOND-board-sync-") for f in findings)


def test_board_sync_no_heading_at_all(tmp_path):
    _write(tmp_path, "docs/adr/2026-07-01-a.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    _write(tmp_path, "STATE.md", "### 2026-11-08\n\n- unrelated section\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    hit = next(f for f in findings if f.id == "PRECOND-board-sync-2026-08-08")
    assert "no ### 2026-08-08 heading" in hit.summary


def test_board_sync_silent_without_state_md(tmp_path):
    """Fails open: no STATE.md at all (e.g. a non-repo tmp_path) -> no finding,
    not a crash and not a false claim."""
    _write(tmp_path, "docs/adr/2026-07-01-a.md",
           "**Trigger check schedule:** next 2026-08-08.\n")
    findings = precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60)
    assert not any(f.id.startswith("PRECOND-board-sync-") for f in findings)


def test_board_sync_silent_without_adr_dir(tmp_path):
    """No docs/adr/ directory at all -> silent (covers the existing SLATE_DATE
    unit tests above, none of which create docs/adr/)."""
    _write(tmp_path, "STATE.md", "### 2026-08-08\n\n- nothing to check\n")
    assert precondition_scan(tmp_path, asof=date(2026, 6, 23), horizon_days=60) == []


# --- sessions_scan (roll-off window) -------------------------------------- #

_SESS_HEADER = (
    "# Session Log\n\n**Entry template:**\n```markdown\n"
    "## YYYY-MM-DD — <focus title>\n```\n\n---\n\n"
)


def _sessions_doc(n: int) -> str:
    entries = [f"## 2026-06-{i:02d} — entry {i}\n**Focus:** x.\n" for i in range(1, n + 1)]
    return _SESS_HEADER + "\n\n---\n\n".join(entries) + "\n"


def test_sessions_scan_fires_over_threshold(tmp_path):
    _write(tmp_path, "docs/SESSIONS.md", _sessions_doc(21))
    findings = sessions_scan(tmp_path, max_entries=20)
    assert len(findings) == 1
    assert findings[0].id == "SESSIONS-over-window"
    assert findings[0].category == "hygiene"
    assert findings[0].routing == "Forward"
    assert findings[0].source == "docs/SESSIONS.md"


def test_sessions_scan_silent_at_threshold(tmp_path):
    _write(tmp_path, "docs/SESSIONS.md", _sessions_doc(20))
    assert sessions_scan(tmp_path, max_entries=20) == []


def test_sessions_scan_failopen_when_missing(tmp_path):
    assert sessions_scan(tmp_path, max_entries=20) == []


def test_sessions_scan_ignores_template_line(tmp_path):
    _write(tmp_path, "docs/SESSIONS.md", _SESS_HEADER)  # template only, 0 real entries
    assert sessions_scan(tmp_path, max_entries=0) == []


# --- render_run ----------------------------------------------------------- #

def test_render_run_empty_is_no_findings():
    out = render_run(asof=date(2026, 6, 23), findings=[])
    assert "2026-06-23" in out
    assert "no findings" in out.lower()


def test_render_run_lists_findings_grouped():
    f = Finding(id="SKEW-x", category="skew", routing="Action", summary="s", source="CLAUDE.md:80", next_step="n")
    out = render_run(asof=date(2026, 6, 23), findings=[f])
    assert "SKEW-x" in out and "Action" in out and "CLAUDE.md:80" in out


def test_render_run_is_deterministic():
    f = Finding(id="OBLIG-2026-08-08", category="obligation", routing="Forward", summary="s", source="CLAUDE.md:82", next_step="n")
    assert render_run(date(2026, 6, 23), [f]) == render_run(date(2026, 6, 23), [f])


# --- preregistration_scan: classifiers -------------------------------------- #
# Real anchors: violation efeda82 (prereg+closure+RESULTS in one commit);
# gold standard 46f47d1 (freeze) -> 913829b (run); 3935d2c prereg is a proper
# ancestor (711d499), so artifact-pairing correctly does not fire.

def test_prereg_artifact_classification():
    assert _is_prereg_artifact("docs/briefs/pre-registration/Q-SWAP-2-verdict-preregistration.md")
    assert _is_prereg_artifact("docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md")
    assert _is_prereg_artifact("docs/briefs/pre-registration/PREREG-USDCAD-FADE-2026-06-26.md")
    assert _is_prereg_artifact("lab/analysis/regime_cond_2026-06-30/preregistration.md")
    assert _is_prereg_artifact("lab/analysis/x/COMPOSITE-FREEZE.md")
    assert not _is_prereg_artifact("lab/analysis/regime_cond_2026-06-30/FINDINGS.md")
    assert not _is_prereg_artifact("docs/briefs/Q-ORB-FRIDAY-1-closure-falsified.md")


def test_prereg_name_match_is_documents_only():
    """A prereg is a DOCUMENT. Code whose name happens to carry the token is scaffold.

    Anchor: the 2026-08-03 weekly run emitted PREREG-SAMECOMMIT-c050965 against
    `run_phase123_freeze_tstar.py` — a Q-DRIFTEX-1 runner, not a pre-registration.
    That run's real prereg (docs/briefs/pre-registration/2026-08-01-drift-
    exhaustion-mechanism-preregistration.md) was frozen in 26cad59, a proper
    ancestor of the results commit: the gold-standard shape, reported as a
    violation. Across all history, every genuine name-matched prereg outside
    the prereg directory is markdown (13/13); the only two non-markdown matches
    are this runner and lab/research_utils/prereg_paths.py — both false.
    """
    assert not _is_prereg_artifact("lab/analysis/driftex_2026-08/run_phase123_freeze_tstar.py")
    assert not _is_prereg_artifact("lab/research_utils/prereg_paths.py")
    # Non-document freeze OUTPUTS are scaffold too, not the freeze record itself.
    assert not _is_prereg_artifact("lab/analysis/driftex_2026-08/freeze_tstar.json")
    # The document forms all still classify.
    assert _is_prereg_artifact("lab/analysis/x/COMPOSITE-FREEZE.md")
    assert _is_prereg_artifact("docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md")


def test_result_artifact_classification():
    assert _is_result_artifact("docs/briefs/Q-ORB-FRIDAY-1-closure-falsified.md")
    assert _is_result_artifact("docs/briefs/Q-INCUMBENT-REGIME-1-closure-resolved.md")
    assert _is_result_artifact("lab/analysis/decompound_remc_2026-06-07/RESULTS_cleanvintage_2026-06-25.md")
    assert _is_result_artifact("lab/analysis/regime_cond_2026-06-30/FINDINGS.md")
    assert _is_result_artifact("lab/archive/decompound_remc_2026-06-07/RESULTS.md")
    # A prereg is never its own result, even under lab/analysis/.
    assert not _is_result_artifact("lab/analysis/regime_cond_2026-06-30/preregistration.md")
    # CARD.md stubs are not result artifacts.
    assert not _is_result_artifact("lab/analysis/x/CARD.md")
    # Scaffold / data outputs are not results.
    assert not _is_result_artifact("lab/analysis/regime_cond_2026-06-30/panel.py")
    assert not _is_result_artifact("lab/analysis/regime_cond_2026-06-30/conditional_results.json")


def test_corresponds_by_qid_and_directory():
    assert _corresponds(
        "docs/briefs/Q-INCUMBENT-REGIME-1-closure-resolved.md",
        "docs/briefs/pre-registration/Q-INCUMBENT-REGIME-1-verdict-preregistration.md",
    )
    assert _corresponds(
        "lab/analysis/regime_cond_2026-06-30/FINDINGS.md",
        "lab/analysis/regime_cond_2026-06-30/preregistration.md",
    )
    # Different question, different directory -> no correspondence.
    assert not _corresponds(
        "docs/briefs/Q-SWAP-2-closure-ambiguous.md",
        "docs/briefs/pre-registration/Q-ORB-FRIDAY-1-verdict-preregistration.md",
    )


def test_corresponds_by_body_qid_across_trees():
    """G1-family shape: no Q-ID in either basename, shared Q-ID only in bodies."""
    result = "lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md"
    prereg = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
    assert not _corresponds(result, prereg)
    assert _corresponds(
        result, prereg,
        result_text="Scored under Q-SURVIVOR-1 frozen thresholds.",
        prereg_text="This freeze is Q-SURVIVOR-1.",
    )


def test_corresponds_when_results_cite_prereg_path():
    """Cross-tree: lab RESULTS body names the prereg path (audit R3)."""
    result = "lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md"
    prereg = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
    assert _corresponds(
        result, prereg,
        result_text=(
            "Gate: docs/briefs/pre-registration/"
            "2026-07-13-prop-survivor-scoring-prereg.md"
        ),
    )
    assert not _corresponds(
        result, prereg,
        result_text="Unrelated campaign; no prereg citation.",
    )


# --- preregistration_scan: pure pairing core -------------------------------- #

def test_pair_violations_flags_closure_plus_prereg():
    changed = [
        ("A", "docs/briefs/Q-INCUMBENT-REGIME-1-closure-resolved.md"),
        ("A", "docs/briefs/pre-registration/Q-INCUMBENT-REGIME-1-verdict-preregistration.md"),
    ]
    pairs = _pair_violations(changed)
    assert len(pairs) == 1
    assert pairs[0][0].endswith("closure-resolved.md")


def test_pair_violations_ignores_prereg_plus_scaffold():
    # The 46f47d1 freeze shape: prereg + runner + data, NO results -> clean.
    changed = [
        ("A", "lab/analysis/regime_cond_2026-06-30/preregistration.md"),
        ("A", "lab/analysis/regime_cond_2026-06-30/panel.py"),
        ("A", "lab/analysis/regime_cond_2026-06-30/panel.csv"),
        ("A", "lab/analysis/regime_cond_2026-06-30/coverage.json"),
    ]
    assert _pair_violations(changed) == []


def test_pair_violations_ignores_freeze_named_runner_with_results():
    """The real c050965 shape: results + a runner whose NAME carries 'freeze'.

    Its pre-registration is a proper ancestor (26cad59), so this commit is the
    gold standard, not a violation. Must be clean.
    """
    changed = [
        ("A", "lab/analysis/driftex_2026-08/RESULTS.md"),
        ("A", "lab/analysis/driftex_2026-08/run_phase123_freeze_tstar.py"),
        ("A", "lab/analysis/driftex_2026-08/run_phase456_ladder_verdict.py"),
        ("A", "lab/analysis/driftex_2026-08/TSTAR_FROZEN.json"),
    ]
    assert _pair_violations(changed) == []


def test_pair_violations_still_flags_real_same_commit_prereg_doc():
    """Negative control for the fix above: a genuine prereg DOCUMENT added
    alongside its results in the same directory must still flag."""
    changed = [
        ("A", "lab/analysis/driftex_2026-08/RESULTS.md"),
        ("A", "lab/analysis/driftex_2026-08/preregistration.md"),
    ]
    pairs = _pair_violations(changed)
    assert len(pairs) == 1
    assert pairs[0][1].endswith("preregistration.md")


def test_pair_violations_ignores_results_only():
    # The 913829b run shape: results + code, prereg untouched -> clean.
    changed = [
        ("A", "lab/analysis/regime_cond_2026-06-30/FINDINGS.md"),
        ("A", "lab/analysis/regime_cond_2026-06-30/conditional.py"),
        ("A", "lab/analysis/regime_cond_2026-06-30/conditional_results.json"),
    ]
    assert _pair_violations(changed) == []


def test_pair_violations_ignores_unrelated_prereg_and_results():
    changed = [
        ("A", "docs/briefs/Q-SWAP-2-closure-ambiguous.md"),
        ("A", "docs/briefs/pre-registration/Q-ORB-FRIDAY-1-verdict-preregistration.md"),
    ]
    assert _pair_violations(changed) == []


def test_pair_violations_flags_crosstree_when_results_cite_prereg():
    """Path-only misses the G1 family; a RESULTS body that cites the prereg fires."""
    result = "lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md"
    prereg = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
    changed = [("A", result), ("A", prereg)]
    assert _pair_violations(changed) == []
    texts = {result: f"Frozen gate: {prereg}", prereg: "no Q-ID in this filename"}
    pairs = _pair_violations(changed, texts)
    assert len(pairs) == 1
    assert pairs[0][1] == prereg


def test_pair_violations_tags_added_prereg_status():
    """An ADDED prereg is the self-attested-freeze class; the pair carries its status
    so the caller can tell it apart from a run-commit edit of an already-frozen file."""
    changed = [
        ("A", "docs/briefs/Q-INCUMBENT-REGIME-1-closure-resolved.md"),
        ("A", "docs/briefs/pre-registration/Q-INCUMBENT-REGIME-1-verdict-preregistration.md"),
    ]
    pairs = _pair_violations(changed)
    assert len(pairs) == 1
    assert pairs[0][2] == "A"


def test_pair_violations_tags_modified_prereg_status():
    # Touching the frozen prereg in the run commit is a DIFFERENT claim from a
    # same-commit freeze: the freeze may well be a proper ancestor.
    changed = [
        ("A", "docs/briefs/Q-ORB-FRIDAY-1-closure-falsified.md"),
        ("M", "docs/briefs/pre-registration/Q-ORB-FRIDAY-1-verdict-preregistration.md"),
    ]
    pairs = _pair_violations(changed)
    assert len(pairs) == 1
    assert pairs[0][2] == "M"


def test_pair_violations_ignores_prereg_only():
    changed = [("A", "docs/briefs/pre-registration/Q-SWAP-2-verdict-preregistration.md")]
    assert _pair_violations(changed) == []


# --- preregistration_scan: git integration + fail-open ---------------------- #

def _git(repo: Path, *args: str, when: str | None = None) -> None:
    env = None
    if when is not None:
        import os
        env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True, env=env,
    )


def _commit(repo: Path, files: dict[str, str], msg: str, when: str) -> None:
    for rel, body in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", msg, when=when)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_preregistration_scan_git_flags_same_commit_not_gold_standard(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    # Base commit so the freeze/run commits below have a visible parent delta.
    _commit(repo, {"README.md": "base\n"}, "base", when="2026-06-28T09:00:00")
    # Freeze (prereg + scaffold) -> run (results only): the gold standard, clean.
    _commit(repo, {
        "lab/analysis/regime_cond/preregistration.md": "H0: composite is fresh.\n",
        "lab/analysis/regime_cond/panel.py": "print('panel')\n",
    }, "prereg(freeze): composite BEFORE returns", when="2026-06-28T10:00:00")
    _commit(repo, {
        "lab/analysis/regime_cond/FINDINGS.md": "FALSIFIED.\n",
        "lab/analysis/regime_cond/conditional.py": "print('run')\n",
    }, "run: FALSIFIED", when="2026-06-28T11:00:00")
    # Violation: closure + its prereg in one commit.
    _commit(repo, {
        "docs/briefs/Q-DEMO-1-closure-falsified.md": "closed.\n",
        "docs/briefs/pre-registration/Q-DEMO-1-verdict-preregistration.md": "frozen.\n",
    }, "Q-DEMO-1: FALSIFIED + prereg (same commit)", when="2026-06-29T10:00:00")

    findings = preregistration_scan(repo, asof=date(2026, 7, 2), lookback_days=14)
    assert len(findings) == 1
    f = findings[0]
    assert f.category == "prereg"
    assert f.routing == "Action"
    assert f.id.startswith("PREREG-SAMECOMMIT-")
    assert "Q-DEMO-1-closure-falsified.md" in f.source


def _seed_frozen_prereg(repo: Path, qid: str) -> str:
    """Freeze a prereg in its own commit (the gold standard), return its path."""
    rel = f"docs/briefs/pre-registration/{qid}-verdict-preregistration.md"
    _commit(repo, {rel: (
        "# Pre-registration\n"
        "**Status:** `FROZEN` — operator signed §9.\n"
        "**Gate:** reject H if D1 < 5%.\n"
    )}, f"brief({qid}): sign + FREEZE §9", when="2026-06-28T10:00:00")
    return rel


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_preregistration_scan_git_ignores_closure_status_stamp(tmp_path):
    """A run commit that stamps ONLY the prereg's `**Status:**` header is the repo's
    closure convention, not a freeze violation — the freeze is a proper ancestor and
    the body is retained unedited. Anchors: b0189db (Q-COSTGEO-1), 6812146 (Q-COSTGEO-3)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "base\n"}, "base", when="2026-06-28T09:00:00")
    rel = _seed_frozen_prereg(repo, "Q-STAMP-1")
    _commit(repo, {
        "docs/briefs/closures/Q-STAMP-1-closure-ambiguous.md": "AMBIGUOUS.\n",
        rel: (
            "# Pre-registration\n"
            "**Status:** `CLOSED — AMBIGUOUS` (2026-06-29). Body retained unedited below.\n"
            "**Gate:** reject H if D1 < 5%.\n"
        ),
    }, "closure(Q-STAMP-1): AMBIGUOUS", when="2026-06-29T10:00:00")

    assert preregistration_scan(repo, asof=date(2026, 7, 2), lookback_days=14) == []


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_preregistration_scan_git_flags_substantive_prereg_edit(tmp_path):
    """A run commit editing the frozen prereg BEYOND its status header is the real
    concern (the 3935d2c verdict-logic class) — flagged, but as its own claim."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "base\n"}, "base", when="2026-06-28T09:00:00")
    rel = _seed_frozen_prereg(repo, "Q-EDIT-1")
    _commit(repo, {
        "docs/briefs/closures/Q-EDIT-1-closure-falsified.md": "FALSIFIED.\n",
        rel: (
            "# Pre-registration\n"
            "**Status:** `CLOSED — FALSIFIED` (2026-06-29).\n"
            "**Gate:** reject H if D1 < 2%.\n"          # <- frozen threshold moved
        ),
    }, "closure(Q-EDIT-1): FALSIFIED", when="2026-06-29T10:00:00")

    findings = preregistration_scan(repo, asof=date(2026, 7, 2), lookback_days=14)
    assert len(findings) == 1
    f = findings[0]
    assert f.id.startswith("PREREG-RUNEDIT-")
    assert f.category == "prereg"
    # The message must NOT claim a self-attested freeze — the freeze IS an ancestor.
    assert "self-attested" not in f.summary


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_preregistration_scan_respects_lookback_window(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "base\n"}, "base", when="2026-04-01T10:00:00")
    # A genuine violation (has a parent, so it would be flagged if in-window)...
    _commit(repo, {
        "docs/briefs/Q-OLD-1-closure-falsified.md": "closed.\n",
        "docs/briefs/pre-registration/Q-OLD-1-verdict-preregistration.md": "frozen.\n",
    }, "Q-OLD-1: violation outside the window", when="2026-05-01T10:00:00")
    # ...but it is dated before the 14d window from asof -> excluded.
    assert preregistration_scan(repo, asof=date(2026, 7, 2), lookback_days=14) == []


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_preregistration_scan_skips_parentless_commit(tmp_path):
    # Regression guard for the shallow-clone graft boundary: a parentless commit
    # (here the root) has no visible delta, so it is skipped rather than flagged
    # on its whole tree — even though it introduces a corresponding prereg+closure.
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {
        "docs/briefs/Q-ROOT-1-closure-falsified.md": "closed.\n",
        "docs/briefs/pre-registration/Q-ROOT-1-verdict-preregistration.md": "frozen.\n",
    }, "Q-ROOT-1: violation but this is the root commit", when="2026-06-29T10:00:00")
    assert preregistration_scan(repo, asof=date(2026, 7, 2), lookback_days=14) == []


def test_preregistration_scan_failopen_non_git(tmp_path):
    # Not a git repo -> no findings, no crash.
    assert preregistration_scan(tmp_path, asof=date(2026, 7, 2), lookback_days=14) == []


# --- _git_lines: locale-independent decoding + fail-open contract ----------- #
#
# Regression fixtures for the 2026-08-08 audit-time crash. `text=True` without an
# explicit `encoding=` decodes with the LOCALE default (cp1252 on a stock Windows
# box). This repo's docs carry em-dashes, arrows and warning glyphs, so essentially
# every `git diff` here is non-decodable under cp1252. The failure mode is nasty:
# the decode raises in subprocess's reader THREAD, which subprocess swallows, so
# the parent sees returncode 0 with stdout silently None -- and `_git_lines` then
# crashed on `.splitlines()`, taking the whole sentinel run down instead of
# failing open as its docstring promises.

def test_git_lines_pins_utf8_and_never_relies_on_locale(monkeypatch):
    """The decode encoding must be EXPLICIT. This is the platform-independent
    regression: on a UTF-8 box the integration test below passes either way, so
    only pinning the kwarg catches a reintroduction everywhere."""
    seen: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        seen.update(kwargs)
        return subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert _git_lines(Path("."), "log") == ["ok"]
    assert seen.get("encoding") == "utf-8", (
        "git output must be decoded as UTF-8 explicitly, never via the locale default"
    )
    assert seen.get("errors"), (
        "an errors= policy is required so a non-UTF-8 blob degrades instead of raising"
    )


def test_git_lines_fails_open_when_stdout_is_none(monkeypatch):
    """Contract: '_git_lines returns None on any failure. Fail-open by design.'
    A reader-thread decode death yields returncode 0 with stdout None, which slips
    past the returncode check -- the guard must catch it rather than AttributeError."""
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout=None, stderr=None)

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert _git_lines(Path("."), "diff-tree", "-p", "HEAD") is None


@pytest.mark.skipif(shutil.which("git") is None, reason="git not available")
def test_git_lines_decodes_non_cp1252_diff_bytes(tmp_path):
    """End-to-end: a diff carrying characters absent from cp1252 must round-trip.
    Reproduces the real crash -- the byte that killed the 2026-08-08 run was 0x81,
    a UTF-8 continuation byte that cp1252 leaves undefined."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "base\n"}, "base", when="2026-08-08T09:00:00")
    # U+2014 em dash, U+2265 >=, U+26A0 warning, U+2192 arrow: all present across
    # this repo's ADRs and all undefined or lossy in cp1252.
    body = "Trigger — check ≥ 1 ⚠ route → audit\n"
    _commit(repo, {"docs/adr/demo.md": body}, "add adr with non-cp1252 glyphs",
            when="2026-08-08T10:00:00")

    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, encoding="utf-8", check=True,
    ).stdout.strip()

    lines = _git_lines(repo, "diff-tree", "-p", "--no-commit-id", "-r", head)
    assert lines is not None, "decode failure must not collapse the scan to None"
    added = "\n".join(ln for ln in lines if ln.startswith("+") and not ln.startswith("+++"))
    assert "—" in added and "≥" in added and "⚠" in added and "→" in added
