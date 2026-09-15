"""TB-C1 forward session calendar: verified rows in, BookSession or typed refusal out."""
import json
import sys
from dataclasses import replace
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from book_session_calendar import (
    CalendarError, SessionDecision, load_closure_overlay, load_ratifications,
    load_ratified_calendar, load_session_calendar,
)
from book_sizing_context import BookSession, SettledClose, size_book_request
from test_tradeify_sizing_integration import POLICY, inputs

REPO = Path(__file__).resolve().parents[2]
CALENDAR = REPO / "ops" / "calendars" / "book_session_calendar_2026-09.json"
OVERLAY = REPO / "ops" / "calendars" / "book_closure_overlay.json"
EVIDENCE = REPO / "ops" / "calendars" / "evidence" / "2026-09-15-forward-session-source-captures.json"
D19 = REPO / "ops" / "calendars" / "cme_holiday_calendar_2022_2026.json"
RATIFIED = REPO / "ops" / "calendars" / "RATIFIED.json"
ET = ZoneInfo("America/New_York")

# Pinned identities for the first attended-release file. A changed byte here is a
# replacement freeze and a new operator decision, never a silent edit.
CALENDAR_SHA256 = "650e8aab4166f74a988675a3f3dfa2dbd21c1c1b342777ac37d65aacea9d6f2f"
OVERLAY_SHA256 = "483f2324b85548e60429b823454641a0ee6e34c8ef2a9cadc7dcc6555f7def5b"
EVIDENCE_SHA256 = "56951e1527af20966dea64130bf8d0a1dccb9bc011bd6e0501282faa549fcba5"
D19_SHA256 = "2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9"


def et(y, m, d, hh, mm=0):
    return datetime(y, m, d, hh, mm, tzinfo=ET)


def load():
    return load_session_calendar(CALENDAR, overlay_path=OVERLAY, repo_root=REPO)


LABOR_DAY = dict(halts_local={"6J": "17:00", "MGC": "14:30", "MYM": "13:00", "MNQ": "13:00"},
                 source_ids=("cme-ui-labor-2026", "cme-globex-2026-holiday-schedule"))


def calendar_fixture(tmp_path, *, first, last, denials=(), generated="2026-09-15T00:00:00Z"):
    """Author a synthetic calendar through the real authoring tool into a tmp repo layout."""
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import author_book_session_calendar as author
    finally:
        sys.path.pop(0)
    repo = tmp_path / "repo"
    evidence_dir = repo / "ops" / "calendars" / "evidence"
    evidence_dir.mkdir(parents=True)
    evidence_path = evidence_dir / EVIDENCE.name
    evidence_path.write_bytes(EVIDENCE.read_bytes())
    overlay_path = repo / "ops" / "calendars" / "book_closure_overlay.json"
    overlay_path.write_bytes(OVERLAY.read_bytes())
    payload = author.build_calendar(first, last, dict(denials), evidence_path, generated, "synthetic/forward")
    payload["sources"]["evidence_file"] = "ops/calendars/evidence/" + EVIDENCE.name
    path = repo / "ops" / "calendars" / "synthetic.json"
    path.write_bytes(json.dumps(payload, indent=2).encode("utf-8") + b"\n")
    return path, overlay_path, repo, payload


def rewrite(path, payload):
    path.write_bytes(json.dumps(payload, indent=2).encode("utf-8") + b"\n")


# ---------------------------------------------------------------- checked-in artifacts


def test_checked_in_calendar_overlay_and_evidence_are_byte_pinned():
    """The ratification target is the exact bytes; any drift must be a visible new decision."""
    assert sha256(CALENDAR.read_bytes()).hexdigest() == CALENDAR_SHA256
    assert sha256(OVERLAY.read_bytes()).hexdigest() == OVERLAY_SHA256
    assert sha256(EVIDENCE.read_bytes()).hexdigest() == EVIDENCE_SHA256
    assert sha256(D19.read_bytes()).hexdigest() == D19_SHA256
    cal = load()
    assert cal.calendar_digest == CALENDAR_SHA256
    assert cal.overlay_digest == OVERLAY_SHA256


def test_checked_in_calendar_covers_the_approved_horizon_and_only_ordinary_sessions():
    """September 3-30 2026, twenty account days, Labor Day and its adjacent session denied."""
    cal = load()
    assert cal.rows[0].session_id == "tradeify-account-day:2026-09-03"
    assert cal.rows[-1].session_id == "tradeify-account-day:2026-09-30"
    assert len(cal.rows) == 20
    assert cal.coverage_start == et(2026, 9, 2, 18)
    assert cal.coverage_end == et(2026, 9, 30, 17)
    denied = {r.session_id.split(":")[1]: r.denial_reason for r in cal.rows if r.permission == "DENIED"}
    assert denied == {"2026-09-07": "HOLIDAY", "2026-09-08": "UNCERTAIN_ADJACENT"}
    assert all(r.session_id.split(":")[1] > "2026-09-02" for r in cal.rows), "must not restate frozen D19 rows"
    assert not any(r.overlay_blocked for r in cal.rows)


def test_checked_in_calendar_reproduces_from_the_authoring_tool():
    """The committed bytes are exactly what the tool emits for the recorded inputs."""
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import author_book_session_calendar as author
    finally:
        sys.path.pop(0)
    denials = {
        date(2026, 9, 7): author.Denial("HOLIDAY", "CME Globex 2026 Labor Day holiday schedule (dates 6-8 September); Tradeify holiday-shortened flat deadline 12:59 ET; product matching halts observed on the wall date (cme-ui-labor-2026); preceding open not separately established", **LABOR_DAY),
        date(2026, 9, 8): author.Denial("UNCERTAIN_ADJACENT", "Inside the CME 2026 Labor Day schedule dates 6-8 September. The 17:00 CT reopen on 2026-09-07 is observed, but the full 2026-09-08 regular session is not separately qualified; denied under the first-release adjacent-session rule"),
    }
    payload = author.build_calendar(date(2026, 9, 3), date(2026, 9, 30), denials, EVIDENCE,
                                    "2026-09-15T10:40:00Z", "tradeify-select-100k/forward/2026-09")
    payload["sources"]["evidence_file"] = "ops/calendars/evidence/" + EVIDENCE.name
    regenerated = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    assert sha256(regenerated).hexdigest() == CALENDAR_SHA256


def test_overlay_dates_are_typed_and_agree_with_d19_sub_deadline_closes():
    """Overlay rows override D19 explicitly and never fall inside the forward window."""
    dates, digest = load_closure_overlay(OVERLAY)
    assert digest == OVERLAY_SHA256
    assert dates == {date(2023, 4, 7), date(2025, 1, 9), date(2026, 4, 3)}
    d19 = json.loads(D19.read_bytes())
    sub = {date.fromisoformat(r["date"]) for r in d19["derived"]["sub_deadline_close_dates"]["dates"]}
    assert dates == sub
    raw = json.loads(OVERLAY.read_bytes())
    assert all(row["overrides_d19"] is True for row in raw["dates"])
    assert raw["d19_source"]["sha256"] == D19_SHA256
    cal = load()
    assert not any(cal.coverage_start <= datetime(d.year, d.month, d.day, tzinfo=timezone.utc) < cal.coverage_end
                   for d in dates)


# ---------------------------------------------------------------- section 5 schedule rule


def test_ordinary_session_derives_the_ratified_regular_times():
    """V=16:45 ET (venue) gives 15:45 cutoff, 15:55 flatten start, 16:00 own-flat."""
    row = load().schedule_for("tradeify-account-day:2026-09-15")
    assert row.opens_at == et(2026, 9, 14, 18)
    assert row.closes_at == et(2026, 9, 15, 17)
    assert row.v == et(2026, 9, 15, 16, 45)
    assert row.risk_add_cutoff == et(2026, 9, 15, 15, 45)
    assert row.flatten_start == et(2026, 9, 15, 15, 55)
    assert row.own_flat_deadline == et(2026, 9, 15, 16)


def test_holiday_row_keeps_deadlines_for_safe_flattening_even_though_denied():
    """V=12:59 gives 12:29, 12:39 and 12:44 exactly as the spec example; denial keeps the row."""
    row = load().schedule_for("tradeify-account-day:2026-09-07")
    assert row.permission == "DENIED"
    assert row.v == et(2026, 9, 7, 12, 59)
    assert row.risk_add_cutoff == et(2026, 9, 7, 12, 29)
    assert row.flatten_start == et(2026, 9, 7, 12, 39)
    assert row.own_flat_deadline == et(2026, 9, 7, 12, 44)
    assert row.prior_session_id == "tradeify-account-day:2026-09-04"


# ---------------------------------------------------------------- session_for decisions


@pytest.mark.parametrize("now,refusal", [
    (et(2026, 9, 2, 17, 59), "coverage_not_started"),
    (et(2026, 9, 30, 17), "coverage_expired"),
    (et(2026, 9, 12, 12), "no_session_at_now"),            # Saturday
    (et(2026, 9, 7, 9), "session_denied:HOLIDAY"),
    (et(2026, 9, 8, 9), "session_denied:UNCERTAIN_ADJACENT"),
    (et(2026, 9, 15, 15, 45), "after_risk_add_cutoff"),
    (et(2026, 9, 15, 16, 30), "after_risk_add_cutoff"),
    (et(2026, 9, 14, 17, 30), "no_session_at_now"),        # maintenance break
])
def test_refusals_are_values_not_fallbacks(now, refusal):
    """Nothing outside a permitted qualified row admits new risk; no weekday fallback."""
    decision = load().session_for(now)
    assert isinstance(decision, SessionDecision)
    assert decision.session is None
    assert decision.refusal == refusal
    assert decision.calendar_digest == CALENDAR_SHA256


def test_permitted_session_binds_identity_window_and_digest():
    """A permitted row yields the consumer's BookSession with the file digest."""
    decision = load().session_for(et(2026, 9, 15, 9, 30))
    assert decision.refusal is None
    assert decision.session == BookSession(
        "tradeify-account-day:2026-09-15", "tradeify-account-day:2026-09-14",
        et(2026, 9, 14, 18), et(2026, 9, 15, 15, 45), et(2026, 9, 15, 17), CALENDAR_SHA256)
    assert decision.session.opens_at.tzinfo is timezone.utc   # UTC instants; ET mapping verified at load


def test_pinned_digest_mismatch_refuses_before_any_row_is_read():
    """A ratified digest that does not match the file bytes cannot produce a session."""
    cal = load()
    assert cal.session_for(et(2026, 9, 15, 9), expected_digest="e" * 64).refusal == "calendar_digest_mismatch"
    assert cal.session_for(et(2026, 9, 15, 9), expected_digest=CALENDAR_SHA256).permitted


def test_naive_now_and_review_due_warning():
    """A naive clock is refused; passing review_due warns but does not silently extend coverage."""
    cal = load()
    assert cal.session_for(datetime(2026, 9, 15, 13)).refusal == "invalid_now"
    late = cal.session_for(et(2026, 9, 25, 9))
    assert late.permitted and "calendar_review_due" in late.warnings
    assert "calendar_review_due" not in cal.session_for(et(2026, 9, 15, 9)).warnings


def test_denied_days_stay_in_the_prior_session_chain_and_consumer_agrees():
    """Sept 9's prior close is Sept 8 (denied), not the last day the book traded."""
    cal = load()
    decision = cal.session_for(et(2026, 9, 9, 9))
    assert decision.session.prior_session_id == "tradeify-account-day:2026-09-08"
    request, context, binding = inputs()
    now = et(2026, 9, 9, 9)
    settled_ok = SettledClose("tradeify-account-day:2026-09-08", et(2026, 9, 8, 17), 99000, 100000, "d" * 64)
    settled_skip = replace(settled_ok, session_id="tradeify-account-day:2026-09-04")
    good_binding = replace(binding, session=decision.session, settlement=settled_ok)
    good_context = replace(context, session_id=decision.session.session_id,
                           calendar_digest=CALENDAR_SHA256, settled=settled_ok,
                           as_of=now, valid_until=now + timedelta(seconds=30))
    assert not size_book_request(request, context=good_context, binding=good_binding, policy=POLICY, now=now).halt
    bad_binding = replace(good_binding, settlement=settled_skip)
    bad_context = replace(good_context, settled=settled_skip)
    assert size_book_request(request, context=bad_context, binding=bad_binding, policy=POLICY, now=now).halt


def test_refusal_leaves_flatten_deadlines_reachable():
    """Halting new risk never hides the current row's flatten obligations."""
    cal = load()
    now = et(2026, 9, 8, 10)
    decision = cal.session_for(now)
    assert decision.refusal == "session_denied:UNCERTAIN_ADJACENT"
    assert decision.schedule is not None and decision.schedule.own_flat_deadline == et(2026, 9, 8, 16)
    assert cal.row_containing(now).session_id == "tradeify-account-day:2026-09-08"
    assert cal.next_row_after(et(2026, 9, 4, 17)).session_id == "tradeify-account-day:2026-09-07"


# ---------------------------------------------------------------- DST and boundary mapping


def test_dst_transition_changes_the_utc_mapping_and_still_loads(tmp_path):
    """Spring-forward week: the same 18:00 ET open is 23:00Z before and 22:00Z after March 8."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 3, 5), last=date(2026, 3, 11))
    cal = load_session_calendar(path, overlay_path=overlay, repo_root=repo)
    before = cal.schedule_for("tradeify-account-day:2026-03-06")
    after = cal.schedule_for("tradeify-account-day:2026-03-09")
    assert before.opens_at == datetime(2026, 3, 5, 23, tzinfo=timezone.utc)
    assert after.opens_at == datetime(2026, 3, 8, 22, tzinfo=timezone.utc)
    assert before.risk_add_cutoff == datetime(2026, 3, 6, 20, 45, tzinfo=timezone.utc)
    assert after.risk_add_cutoff == datetime(2026, 3, 9, 19, 45, tzinfo=timezone.utc)


@pytest.mark.parametrize("local,utc", [
    ("2026-03-08T02:30:00-05:00", "2026-03-08T07:30:00Z"),   # nonexistent (gap)
    ("2026-11-01T01:30:00-04:00", "2026-11-01T05:30:00Z"),   # ambiguous (fold)
])
def test_gap_and_fold_local_times_are_refused(tmp_path, local, utc):
    """A wall time the zone cannot map unambiguously is a defect, not a guess."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 3, 5), last=date(2026, 3, 11))
    payload["sessions"][0]["opens_local"] = local
    payload["sessions"][0]["opens_utc"] = utc
    rewrite(path, payload)
    with pytest.raises(CalendarError, match="ambiguous|nonexistent"):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)


def test_overlay_date_inside_coverage_blocks_the_session(tmp_path):
    """A typed overlay date is a whole-session block even if the row says PERMITTED."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 18))
    raw = json.loads(overlay.read_bytes())
    raw["dates"].append({"date": "2026-09-16", "label": "synthetic", "overrides_d19": True, "reason": "test"})
    overlay.write_bytes(json.dumps(raw).encode("utf-8"))
    cal = load_session_calendar(path, overlay_path=overlay, repo_root=repo)
    assert cal.session_for(et(2026, 9, 16, 9)).refusal == "overlay_closure"
    assert cal.session_for(et(2026, 9, 17, 9)).permitted


# ---------------------------------------------------------------- mutation matrix


def _mutate(payload, mutation):
    rows = payload["sessions"]
    if mutation == "cutoff_tampered":
        rows[3]["risk_add_cutoff_utc"] = "2026-09-17T19:46:00Z"
    elif mutation == "own_flat_extended":
        rows[3]["own_flat_deadline_utc"] = "2026-09-17T20:15:00Z"
    elif mutation == "weekend_session":
        rows[3]["session_id"] = "tradeify-account-day:2026-09-19"
        rows[3]["account_date"] = "2026-09-19"
    elif mutation == "chain_broken":
        rows[3]["prior_session_id"] = "tradeify-account-day:2026-09-15"
    elif mutation == "chain_self":
        rows[3]["prior_session_id"] = rows[3]["session_id"]
    elif mutation == "denied_without_reason":
        rows[3]["permission"] = "DENIED"
    elif mutation == "denied_untyped_reason":
        rows[3]["permission"] = "DENIED"
        rows[3]["denial_reason"] = "SEEMS_FINE"
        rows[3]["denial_note"] = "x"
    elif mutation == "permitted_with_unqualified_product":
        rows[3]["products"]["6J"]["qualified"] = False
    elif mutation == "unknown_source_id":
        rows[3]["products"]["6J"]["source_ids"] = ["not-captured"]
    elif mutation == "evidence_digest_mismatch":
        payload["sources"]["evidence_sha256"] = "0" * 64
    elif mutation == "extra_top_key":
        payload["fallback"] = "weekday"
    elif mutation == "missing_row_key":
        del rows[3]["flatten_start_utc"]
    elif mutation == "wrong_schema":
        payload["schema"] = "book_session_calendar/v0"
    elif mutation == "coverage_end_extended":
        payload["coverage"]["coverage_end_utc"] = "2026-10-01T21:00:00Z"
    elif mutation == "review_due_after_coverage":
        payload["coverage"]["review_due_utc"] = "2026-12-01T00:00:00Z"
    elif mutation == "schedule_constants_changed":
        payload["schedule_rule"]["cutoff_before_own_flat_minutes"] = 10
    elif mutation == "products_set_wrong":
        del payload["products"]["MGC"]
    elif mutation == "local_utc_disagree":
        rows[3]["opens_utc"] = "2026-09-16T23:00:00Z"
    elif mutation == "session_overlap":
        rows[3]["opens_local"] = "2026-09-16T16:00:00-04:00"
        rows[3]["opens_utc"] = "2026-09-16T20:00:00Z"
    elif mutation == "wrong_venue_deadline":
        rows[3]["venue_flat_deadline_local"] = "2026-09-17T16:59:00-04:00"
    elif mutation == "matching_outside_day":
        rows[3]["products"]["MNQ"]["matching_close_utc"] = "2026-09-17T21:30:00Z"
    elif mutation == "gap_beyond_weekend":
        del rows[1]
        del rows[1]
    elif mutation == "skipped_weekday":
        rows[3]["prior_session_id"] = rows[1]["session_id"]     # chain around the deleted Wednesday
        del rows[2]
    elif mutation == "first_row_skips_a_day":
        rows[0]["prior_session_id"] = "tradeify-account-day:2026-09-10"   # Monday 09-14's prior must be Friday 09-11
    elif mutation == "row_omits_venue_sources":
        rows[3]["source_ids"] = ["cme-spec-6J"]
    elif mutation == "sub_minute_close":
        rows[3]["closes_local"] = rows[3]["closes_local"].replace("17:00:00", "17:00:59")
        rows[3]["closes_utc"] = rows[3]["closes_utc"].replace("21:00:00Z", "21:00:59Z")
    elif mutation == "product_cites_other_product_source":
        rows[3]["products"]["MGC"]["source_ids"] = ["cme-spec-6J", "cme-globex-2026-holiday-schedule"]
    elif mutation == "predecessor_flag_wrong":
        rows[0]["predecessor_in_file"] = True
    elif mutation == "policy_permits_more":
        payload["first_release_policy"]["deny"] = ["HOLIDAY"]
    elif mutation == "timezone_changed":
        payload["venue"]["timezone"] = "UTC"
    else:
        raise AssertionError(mutation)


@pytest.mark.parametrize("mutation", [
    "cutoff_tampered", "own_flat_extended", "weekend_session", "chain_broken", "chain_self",
    "denied_without_reason", "denied_untyped_reason", "permitted_with_unqualified_product",
    "unknown_source_id", "evidence_digest_mismatch", "extra_top_key", "missing_row_key",
    "wrong_schema", "coverage_end_extended", "review_due_after_coverage",
    "schedule_constants_changed", "products_set_wrong", "local_utc_disagree", "session_overlap",
    "wrong_venue_deadline", "matching_outside_day", "gap_beyond_weekend", "predecessor_flag_wrong",
    "policy_permits_more", "timezone_changed", "skipped_weekday", "product_cites_other_product_source",
    "first_row_skips_a_day", "row_omits_venue_sources", "sub_minute_close",
])
def test_defective_calendar_files_are_refused_whole(tmp_path, mutation):
    """Any inconsistency with the schedule rule, chain, sources or coverage refuses the file."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 23))
    _mutate(payload, mutation)
    rewrite(path, payload)
    with pytest.raises(CalendarError):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)


@pytest.mark.parametrize("mutation", [
    "row_missing_flag", "row_flag_false", "row_extra_key", "duplicate_date", "wrong_basis", "empty",
])
def test_defective_overlay_files_are_refused(tmp_path, mutation):
    """Overlay rows must be typed, flagged and unique; otherwise the whole file is refused."""
    raw = json.loads(OVERLAY.read_bytes())
    if mutation == "row_missing_flag":
        del raw["dates"][0]["overrides_d19"]
    elif mutation == "row_flag_false":
        raw["dates"][0]["overrides_d19"] = False
    elif mutation == "row_extra_key":
        raw["dates"][0]["exchange_closed"] = True
    elif mutation == "duplicate_date":
        raw["dates"].append(dict(raw["dates"][0]))
    elif mutation == "wrong_basis":
        raw["day_basis"] = "CME_TRADE_DATE"
    elif mutation == "empty":
        raw["dates"] = []
    path = tmp_path / "overlay.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(CalendarError):
        load_closure_overlay(path)


def test_evidence_file_cannot_escape_the_repository(tmp_path):
    """A sources.evidence_file pointing outside repo_root is refused, not read."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 18))
    outside = tmp_path / "outside.json"
    outside.write_bytes(EVIDENCE.read_bytes())
    payload["sources"]["evidence_file"] = "../outside.json"
    rewrite(path, payload)
    with pytest.raises(CalendarError, match="escapes"):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)


# ---------------------------------------------------------------- operator ratification


def test_checked_in_ratification_binds_exactly_the_checked_in_bytes():
    """The operator's 2026-09-15 ratification names the current calendar and overlay digests."""
    rows = load_ratifications(RATIFIED)
    assert set(rows) == {CALENDAR_SHA256}
    row = rows[CALENDAR_SHA256]
    assert row["closure_overlay_sha256"] == OVERLAY_SHA256
    assert row["ratified_by"] == "operator" and row["instruction"] == "ratify calendar 650e8aab"
    cal = load_ratified_calendar(CALENDAR, overlay_path=OVERLAY, ratified_path=RATIFIED, repo_root=REPO)
    assert cal.calendar_digest == CALENDAR_SHA256
    assert cal.session_for(et(2026, 9, 15, 9, 30), expected_digest=CALENDAR_SHA256).permitted


def test_unratified_calendar_bytes_cannot_produce_a_session(tmp_path):
    """A valid but unratified file is refused whole; ratification is by exact digest."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 18))
    with pytest.raises(CalendarError, match="calendar_not_ratified"):
        load_ratified_calendar(path, overlay_path=overlay, ratified_path=RATIFIED, repo_root=repo)


def test_ratification_with_wrong_overlay_or_coverage_is_refused(tmp_path):
    """Ratifying the calendar digest alone does not accept a different overlay or horizon."""
    raw = json.loads(RATIFIED.read_bytes())
    wrong_overlay = json.loads(json.dumps(raw))
    wrong_overlay["ratifications"][0]["closure_overlay_sha256"] = "e" * 64
    p1 = tmp_path / "r1.json"
    p1.write_bytes(json.dumps(wrong_overlay).encode("utf-8"))
    with pytest.raises(CalendarError, match="overlay_not_ratified"):
        load_ratified_calendar(CALENDAR, overlay_path=OVERLAY, ratified_path=p1, repo_root=REPO)
    wrong_cov = json.loads(json.dumps(raw))
    wrong_cov["ratifications"][0]["coverage_end_utc"] = "2026-10-30T21:00:00Z"
    p2 = tmp_path / "r2.json"
    p2.write_bytes(json.dumps(wrong_cov).encode("utf-8"))
    with pytest.raises(CalendarError, match="ratification_coverage_mismatch"):
        load_ratified_calendar(CALENDAR, overlay_path=OVERLAY, ratified_path=p2, repo_root=REPO)


@pytest.mark.parametrize("mutation", [
    "not_operator", "bad_digest", "duplicate_digest", "ratified_after_expiry", "extra_key", "wrong_schema",
])
def test_defective_ratification_files_are_refused(tmp_path, mutation):
    """Ratification rows must be complete, operator-issued and unique per digest."""
    raw = json.loads(RATIFIED.read_bytes())
    row = raw["ratifications"][0]
    if mutation == "not_operator":
        row["ratified_by"] = "agent"
    elif mutation == "bad_digest":
        row["calendar_sha256"] = "650E8AAB"
    elif mutation == "duplicate_digest":
        raw["ratifications"].append(dict(row))
    elif mutation == "ratified_after_expiry":
        row["ratified_utc"] = "2026-10-01T00:00:00Z"
    elif mutation == "extra_key":
        row["waives"] = "activation"
    elif mutation == "wrong_schema":
        raw["schema"] = "calendar_ratification/v0"
    path = tmp_path / "ratified.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(CalendarError):
        load_ratifications(path)


def test_holiday_denial_needs_its_own_halts_and_sources(tmp_path):
    """The authoring tool never reuses another holiday's halts; a HOLIDAY denial without evidence refuses."""
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import author_book_session_calendar as author
    finally:
        sys.path.pop(0)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    with pytest.raises(ValueError, match="own per-product halts"):
        calendar_fixture(tmp_path / "a", first=date(2026, 11, 23), last=date(2026, 11, 27),
                         denials={date(2026, 11, 26): author.Denial("HOLIDAY", "Thanksgiving")})
    with pytest.raises(ValueError, match="captured sources"):
        calendar_fixture(tmp_path / "b", first=date(2026, 11, 23), last=date(2026, 11, 27),
                         denials={date(2026, 11, 26): author.Denial("HOLIDAY", "Thanksgiving",
                                                                    halts_local=LABOR_DAY["halts_local"],
                                                                    source_ids=("cme-ui-thanksgiving-2026",))})


def test_late_product_open_delays_admission_until_every_market_is_open(tmp_path):
    """A product whose matching interval opens after the account open moves admission to that open."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 18))
    row = payload["sessions"][1]                                     # 2026-09-15
    row["products"]["6J"]["matching_open_utc"] = "2026-09-15T00:00:00Z"   # 20:00 ET Sept 14, after the 18:00 ET open
    rewrite(path, payload)
    cal = load_session_calendar(path, overlay_path=overlay, repo_root=repo)
    assert cal.session_for(et(2026, 9, 14, 19)).refusal == "before_product_open"
    decision = cal.session_for(et(2026, 9, 14, 20, 30))
    assert decision.permitted and decision.session.opens_at == datetime(2026, 9, 15, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------- evidence schema v1 / v2


def test_september_loads_under_evidence_v1_with_a_warning_on_every_decision():
    """The ratified September file predates product coverage; every decision says so."""
    cal = load()
    assert cal.evidence_warning == "evidence_schema_v1_no_product_coverage"
    for now in (et(2026, 9, 15, 9), et(2026, 9, 7, 9), et(2026, 9, 12, 12)):
        assert "evidence_schema_v1_no_product_coverage" in cal.session_for(now).warnings


def _v2_fixture(tmp_path, products_by_id=None):
    """A v2 evidence file: every capture declares the products it covers."""
    path, overlay, repo, payload = calendar_fixture(tmp_path, first=date(2026, 9, 14), last=date(2026, 9, 18))
    evidence_path = repo / "ops" / "calendars" / "evidence" / EVIDENCE.name
    ev = json.loads(evidence_path.read_bytes())
    ev["schema"] = "forward_session_source_captures/v2"
    defaults = {"cme-spec-6J": ["6J"], "cme-spec-MGC": ["MGC"], "cme-spec-MYM": ["MYM"], "cme-spec-MNQ": ["MNQ"]}
    for c in ev["captures"]:
        c["products"] = (products_by_id or {}).get(c["id"], defaults.get(c["id"], ["6J", "MGC", "MYM", "MNQ"]))
    data = json.dumps(ev, indent=2).encode("utf-8")
    evidence_path.write_bytes(data)
    payload["sources"]["evidence_sha256"] = sha256(data).hexdigest()
    rewrite(path, payload)
    return path, overlay, repo, payload


def test_evidence_v2_binds_every_product_row_to_a_covering_capture(tmp_path):
    """Under v2 a product row, permitted or denied, must cite a capture that covers that product."""
    path, overlay, repo, payload = _v2_fixture(tmp_path)
    cal = load_session_calendar(path, overlay_path=overlay, repo_root=repo)
    assert cal.evidence_warning is None and "evidence_schema_v1_no_product_coverage" not in cal.session_for(et(2026, 9, 15, 9)).warnings
    # The holiday-schedule capture covers all four products; make it cover none of MGC and cite only it.
    path, overlay, repo, payload = _v2_fixture(tmp_path / "b", {"cme-globex-2026-holiday-schedule": ["6J", "MYM", "MNQ"]})
    payload["sessions"][1]["products"]["MGC"]["source_ids"] = ["cme-globex-2026-holiday-schedule"]
    payload["sessions"][1]["products"]["MGC"]["qualified"] = False
    payload["sessions"][1]["permission"] = "DENIED"
    payload["sessions"][1]["denial_reason"] = "UNCERTAIN_ADJACENT"
    payload["sessions"][1]["denial_note"] = "synthetic"
    rewrite(path, payload)
    with pytest.raises(CalendarError, match="no cited capture covers product MGC"):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)


def test_evidence_v2_capture_without_products_is_refused(tmp_path):
    """A v2 capture must declare its products; an unknown evidence schema refuses outright."""
    path, overlay, repo, payload = _v2_fixture(tmp_path)
    evidence_path = repo / "ops" / "calendars" / "evidence" / EVIDENCE.name
    ev = json.loads(evidence_path.read_bytes())
    del ev["captures"][0]["products"]
    data = json.dumps(ev, indent=2).encode("utf-8")
    evidence_path.write_bytes(data)
    payload["sources"]["evidence_sha256"] = sha256(data).hexdigest()
    rewrite(path, payload)
    with pytest.raises(CalendarError, match="must declare the products"):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)
    ev["captures"][0]["products"] = ["6J"]
    ev["schema"] = "forward_session_source_captures/v9"
    data = json.dumps(ev, indent=2).encode("utf-8")
    evidence_path.write_bytes(data)
    payload["sources"]["evidence_sha256"] = sha256(data).hexdigest()
    rewrite(path, payload)
    with pytest.raises(CalendarError, match="unknown evidence schema"):
        load_session_calendar(path, overlay_path=overlay, repo_root=repo)

