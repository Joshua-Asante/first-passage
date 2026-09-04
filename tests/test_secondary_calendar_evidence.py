"""Synthetic secondary-calendar evidence tests for Tradeify Phase 1."""

from __future__ import annotations

import json
from datetime import date
from hashlib import sha256
from pathlib import Path

import pytest

from research_utils import secondary_calendar_evidence
from research_utils.secondary_calendar_evidence import load_secondary_early_close_calendar
from research_utils.trade_reconciliation import analyze_venue, load_early_close_calendar
from test_trade_reconciliation import _spec, _trade, _trades, fee_schedule
from test_tradeify_phase1_runner import _five_source_fixture, run_phase1, synthetic_pin_manifest


def _source_calendar() -> dict[str, object]:
    return {
        "schema": "cme_holiday_calendar/v1",
        "generated": "2026-09-03",
        "coverage_start": "2026-01-01",
        "coverage_end": "2026-12-31",
        "provenance": "SECONDARY",
        "provenance_note": "Synthetic secondary evidence only.",
        "day_basis": {"basis": "CME_TRADE_DATE", "note": "Synthetic trade-date note."},
        "product_groups": {"equity_index": "MNQ/MYM", "metals": "MGC", "fx": "6J"},
        "derived": {
            "venue_flat_dates": {
                "rule": "Union of EARLY_CLOSE dates.", "count": 2,
                "dates": ["2026-01-05", "2026-04-03"],
            },
            "full_closure_dates": {
                "rule": "Trade-date inventory only.", "count": 1, "dates": ["2026-12-25"],
            },
            "sub_deadline_close_dates": {
                "rule": "Not modeled as a closure.", "count": 1,
                "dates": [{"date": "2026-04-03", "holiday": "Good Friday", "closes_et": {"equity_index": "09:15", "fx": "11:15"}}],
            },
        },
        "entries": [
            {
                "date": "2026-01-05", "holiday": "Synthetic equity holiday",
                "equity_index_status": "EARLY_CLOSE", "equity_index_close_et": "13:00",
                "metals_status": "NORMAL", "metals_close_et": "",
                "fx_status": "NORMAL", "fx_close_et": "",
                "confidence": "HIGH", "note": "6J stays normal, but the account deadline applies.",
            },
            {
                "date": "2026-04-03", "holiday": "Good Friday",
                "equity_index_status": "EARLY_CLOSE", "equity_index_close_et": "09:15",
                "metals_status": "FULL_CLOSURE", "metals_close_et": "",
                "fx_status": "EARLY_CLOSE", "fx_close_et": "11:15",
                "confidence": "MEDIUM", "note": "Pre-12:59 closes are a limitation.",
            },
            {
                "date": "2026-12-25", "holiday": "Christmas",
                "equity_index_status": "FULL_CLOSURE", "equity_index_close_et": "",
                "metals_status": "FULL_CLOSURE", "metals_close_et": "",
                "fx_status": "FULL_CLOSURE", "fx_close_et": "",
                "confidence": "LOW", "note": "Inventory only; never a wall-date deadline.",
            },
        ],
        "source_urls": [
            "https://example.test/secondary-calendar",
            "file:///home/user/first-passage/ops/instruments/6J.md",
        ],
        "unresolved": [{"date": "2026-01-05", "issue": "Synthetic unresolved evidence."}],
        "source_revisions": {
            "pinned_at": "2026-09-03",
            "pins": {"example/calendar": "a" * 40},
            "note": "Tips were resolved after research and do not prove captured read bytes.",
        },
    }


def secondary_fixture(tmp_path):
    repo_root = tmp_path / "repo"
    source_path = repo_root / "ops" / "calendars" / "cme_holiday_calendar_2022_2026.json"
    source_path.parent.mkdir(parents=True)
    source_bytes = json.dumps(_source_calendar()).encode("utf-8")
    source_path.write_bytes(source_bytes)
    wrapper = {
        "schema": "tradeify_secondary_early_close/v1",
        "source_url": "https://example.test/tradeify-secondary-wrapper",
        "page_date": "2026-09-03",
        "observed_date": "2026-09-03",
        "coverage_start": "2026-01-01",
        "coverage_end": "2026-12-31",
        "coverage_status": "NEEDS_CONTEXT",
        "coverage_note": "Synthetic secondary evidence cannot complete the campaign.",
        "source_calendar": {
            "repo_path": "ops/calendars/cme_holiday_calendar_2022_2026.json",
            "sha256": sha256(source_bytes).hexdigest(),
        },
        "rows": [
            {"date": "2026-01-05", "deadline_local": "12:59 America/New_York"},
            {"date": "2026-04-03", "deadline_local": "12:59 America/New_York"},
        ],
    }
    wrapper_path = tmp_path / "secondary_wrapper.json"
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")
    return wrapper_path, wrapper, source_path, repo_root


def d19_acceptance():
    return {
        "decision": "D19",
        "disposition": "ACCEPTED_SECONDARY",
        "ruling_date": "2026-09-03",
        "ruling_ref": "Operator ruling 2026-09-03; campaign-state §6 D19: secondary CME calendar provenance accepted.",
    }


def test_complete_secondary_requires_the_exact_d19_acceptance(tmp_path):
    """Calling incomplete secondary provenance complete without D19 would overstate the evidence."""
    wrapper_path, wrapper, _, repo_root = secondary_fixture(tmp_path)
    wrapper["coverage_status"] = "COMPLETE"
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")

    with pytest.raises(ValueError, match="D19"):
        load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)

    wrapper["provenance_acceptance"] = d19_acceptance()
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")
    calendar = load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)

    assert calendar.coverage_status == "COMPLETE"
    assert calendar.evidence_kind == "SECONDARY"
    assert calendar.evidence_metadata["provenance_acceptance"] == d19_acceptance()


@pytest.mark.parametrize("mutation", ["missing_key", "extra_key", "decision", "disposition", "ruling_date", "ruling_ref"])
def test_complete_secondary_rejects_malformed_d19_acceptance(tmp_path, mutation):
    """Only the operator's exact D19 acceptance may lift a secondary wrapper to COMPLETE."""
    wrapper_path, wrapper, _, repo_root = secondary_fixture(tmp_path)
    acceptance = d19_acceptance()
    if mutation == "missing_key":
        acceptance.pop("ruling_ref")
    elif mutation == "extra_key":
        acceptance["extra"] = True
    else:
        acceptance[mutation] = "wrong" if mutation != "ruling_date" else "2026-09-04"
    wrapper.update(coverage_status="COMPLETE", provenance_acceptance=acceptance)
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")

    with pytest.raises(ValueError, match="D19"):
        load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)


def test_d19_complete_rejects_a_covered_year_without_a_venue_flat_date(tmp_path):
    """D19 accepts provenance, never a fabricated empty year of calendar evidence."""
    wrapper_path, wrapper, source_path, repo_root = secondary_fixture(tmp_path)
    source = _source_calendar()
    source["coverage_start"] = "2025-01-01"
    source["coverage_end"] = "2026-12-31"
    source["entries"] = [entry for entry in source["entries"] if entry["date"] != "2026-01-05"]
    source["derived"]["venue_flat_dates"] = {
        "rule": "Union of EARLY_CLOSE dates.", "count": 1, "dates": ["2026-04-03"],
    }
    raw = json.dumps(source).encode("utf-8")
    source_path.write_bytes(raw)
    wrapper.update(
        coverage_start="2025-01-01", coverage_end="2026-12-31", coverage_status="COMPLETE",
        provenance_acceptance=d19_acceptance(),
        source_calendar={"repo_path": "ops/calendars/cme_holiday_calendar_2022_2026.json", "sha256": sha256(raw).hexdigest()},
        rows=[{"date": "2026-04-03", "deadline_local": "12:59 America/New_York"}],
    )
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")

    with pytest.raises(ValueError, match="each covered year"):
        load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)


def test_checked_in_d19_wrapper_binds_the_lf_blob_and_all_venue_flat_dates():
    """The accepted wrapper must bind the tracked LF bytes, never a Windows checkout hash or closure union."""
    repo_root = Path(__file__).parents[1]
    campaign = repo_root / "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09"
    source_path = repo_root / "ops/calendars/cme_holiday_calendar_2022_2026.json"
    source = json.loads(source_path.read_bytes())

    calendar = load_secondary_early_close_calendar(
        campaign / "cme_early_close_calendar.json", repo_root=repo_root,
    )

    venue_flat = source["derived"]["venue_flat_dates"]["dates"]
    assert calendar.coverage_status == "COMPLETE"
    assert calendar.source_calendar_sha256 == "2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9"
    assert calendar.source_calendar_sha256 == sha256(source_path.read_bytes()).hexdigest()
    assert sorted(day.isoformat() for day in calendar.early_close_dates) == venue_flat
    assert len(venue_flat) == 49
    assert not set(venue_flat) & set(source["derived"]["full_closure_dates"]["dates"])
    assert calendar.evidence_metadata["provenance_acceptance"] == d19_acceptance()


def test_secondary_union_is_account_level_and_preserves_caveats(tmp_path, fee_schedule):
    """Dropping a NORMAL-6J date would miss a blanket account-level deadline."""
    wrapper_path, _, _, repo_root = secondary_fixture(tmp_path)

    calendar = load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)

    assert calendar.coverage_status == "NEEDS_CONTEXT"
    assert calendar.early_close_dates == {date(2026, 1, 5), date(2026, 4, 3)}
    assert calendar.evidence_kind == "SECONDARY"
    assert calendar.evidence_metadata["source_calendar"]["repo_path"] == "ops/calendars/cme_holiday_calendar_2022_2026.json"
    assert calendar.evidence_metadata["day_basis"]["basis"] == "CME_TRADE_DATE"
    assert calendar.evidence_metadata["source_urls"][1].startswith("file://")
    venue = analyze_venue(_trades(_trade(1, "2026-01-05 13:00", "1.00", "1.82")), _spec(instrument="6J"), fee_schedule, early_close_calendar=calendar)
    assert venue.holiday_short_deadline_status == "NEEDS_CONTEXT"
    assert any(issue.code == "FORCE_FLAT_VIOLATION" for issue in venue.issues)


@pytest.mark.parametrize("mutation", [
    "complete", "hash", "missing_source", "row_omitted", "row_extra", "row_duplicate",
    "derived_mismatch", "entry_extra", "source_extra", "wrapper_extra", "wrong_path", "traversal", "bad_utf8",
])
def test_secondary_schema_rejects_unverified_or_noncanonical_evidence(tmp_path, mutation):
    """A relaxed secondary schema could silently overstate deadline coverage."""
    wrapper_path, wrapper, source_path, repo_root = secondary_fixture(tmp_path)
    source = _source_calendar()
    if mutation == "complete":
        wrapper["coverage_status"] = "COMPLETE"
    elif mutation == "hash":
        wrapper["source_calendar"]["sha256"] = "0" * 64
    elif mutation == "missing_source":
        source_path.unlink()
    elif mutation == "row_omitted":
        wrapper["rows"].pop()
    elif mutation == "row_extra":
        wrapper["rows"].append({"date": "2026-12-25", "deadline_local": "12:59 America/New_York"})
    elif mutation == "row_duplicate":
        wrapper["rows"].append(dict(wrapper["rows"][0]))
    elif mutation == "derived_mismatch":
        source["derived"]["venue_flat_dates"]["dates"] = ["2026-01-05"]
        source["derived"]["venue_flat_dates"]["count"] = 1
        raw = json.dumps(source).encode("utf-8")
        source_path.write_bytes(raw)
        wrapper["source_calendar"]["sha256"] = sha256(raw).hexdigest()
    elif mutation == "entry_extra":
        source["entries"][0]["extra"] = True
        raw = json.dumps(source).encode("utf-8")
        source_path.write_bytes(raw)
        wrapper["source_calendar"]["sha256"] = sha256(raw).hexdigest()
    elif mutation == "source_extra":
        source["extra"] = True
        raw = json.dumps(source).encode("utf-8")
        source_path.write_bytes(raw)
        wrapper["source_calendar"]["sha256"] = sha256(raw).hexdigest()
    elif mutation == "wrapper_extra":
        wrapper["extra"] = True
    elif mutation == "wrong_path":
        wrapper["source_calendar"]["repo_path"] = "ops/calendars/other_calendar.json"
    elif mutation == "traversal":
        wrapper["source_calendar"]["repo_path"] = "../outside.json"
    elif mutation == "bad_utf8":
        source_path.write_bytes(b"\xff")
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")

    with pytest.raises(ValueError):
        load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)


def test_secondary_source_is_read_once_before_hash_and_parse(tmp_path, monkeypatch):
    """A second source read could hash one calendar and consume another."""
    wrapper_path, _, source_path, repo_root = secondary_fixture(tmp_path)
    original = source_path.read_bytes()
    real_read = type(source_path).read_bytes
    reads = 0

    def read_once_then_mutate(path):
        nonlocal reads
        if path == source_path:
            reads += 1
            if reads == 1:
                source_path.write_bytes(b"changed after the captured snapshot")
                return original
        return real_read(path)

    monkeypatch.setattr(type(source_path), "read_bytes", read_once_then_mutate)
    calendar = load_secondary_early_close_calendar(wrapper_path, repo_root=repo_root)
    assert calendar.source_calendar_sha256 == sha256(original).hexdigest()
    assert reads == 1


def test_runner_echoes_populated_secondary_without_lifting_context_cap(tmp_path, monkeypatch, synthetic_pin_manifest):
    """Calling populated secondary rows 'not inferred' would conceal their use."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    wrapper_path, _, _, repo_root = secondary_fixture(tmp_path)
    calendar_path = config.parent / "cme_early_close_calendar.json"
    calendar_path.write_bytes(wrapper_path.read_bytes())
    monkeypatch.setattr(secondary_calendar_evidence, "_REPO_ROOT", repo_root)

    loaded = load_early_close_calendar(calendar_path)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    rendered = result.report_bytes.decode("utf-8")

    assert loaded.evidence_kind == "SECONDARY"
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["cme_early_close_calendar"]["evidence_kind"] == "SECONDARY"
    assert manifest["cme_early_close_calendar"]["evidence_metadata"]["source_revisions"]["pins"] == {"example/calendar": "a" * 40}
    assert "populated SECONDARY" in rendered
    assert "no historical early-close date was inferred" not in rendered
    assert "full-closure inventory (1): 2026-12-25" in rendered
    assert "Sub-deadline inventory (1):" in rendered
    assert "2026-04-03 Good Friday — equity_index=09:15, fx=11:15" in rendered


def test_runner_keeps_secondary_caveats_visible_when_d19_allows_complete(tmp_path, monkeypatch, synthetic_pin_manifest):
    """A COMPLETE label must not hide that D19 accepts date membership rather than a primary calendar."""
    source_dir, config, _ = _five_source_fixture(tmp_path)
    wrapper_path, wrapper, _, repo_root = secondary_fixture(tmp_path)
    wrapper.update(coverage_status="COMPLETE", provenance_acceptance=d19_acceptance())
    wrapper_path.write_text(json.dumps(wrapper), encoding="utf-8")
    (config.parent / "cme_early_close_calendar.json").write_bytes(wrapper_path.read_bytes())
    monkeypatch.setattr(secondary_calendar_evidence, "_REPO_ROOT", repo_root)

    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    rendered = result.report_bytes.decode("utf-8")

    assert manifest["cme_early_close_calendar"]["coverage_status"] == "COMPLETE"
    assert manifest["cme_early_close_calendar"]["evidence_kind"] == "SECONDARY"
    assert manifest["cme_early_close_calendar"]["evidence_metadata"]["provenance_acceptance"] == d19_acceptance()
    assert "D19" in rendered
    assert "SECONDARY" in rendered
    assert "primary-CME upgrade" in rendered
