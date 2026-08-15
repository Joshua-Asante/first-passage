"""Weekly activity-decision status line (STATE row 0 / idle-clock follow-up).

Fixtures fake the compliance-note append-only record — never against live data.
"""
from datetime import date
from pathlib import Path

from sentinel.activity_week import (
    COMPLIANCE_REL,
    business_days_remaining,
    decision_status,
    format_activity_decision_line,
    mon_fri_week,
    week_label,
)
from sentinel.report import render_run


def _write_compliance(root: Path, body: str) -> None:
    p = root / COMPLIANCE_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def test_mon_fri_week_and_business_days():
    asof = date(2026, 8, 12)  # Wednesday
    monday, friday = mon_fri_week(asof)
    assert monday == date(2026, 8, 10)
    assert friday == date(2026, 8, 14)
    assert business_days_remaining(asof, friday) == 3
    assert business_days_remaining(date(2026, 8, 14), friday) == 1
    assert business_days_remaining(date(2026, 8, 15), friday) == 0  # Saturday


def test_not_recorded_when_compliance_silent(tmp_path):
    _write_compliance(
        tmp_path,
        "# §2a\n\n**Next bucket: 2026-08-10 → 08-14**, opening Monday.\n",
    )
    asof = date(2026, 8, 12)
    line = format_activity_decision_line(tmp_path, asof)
    assert "weekly activity decision [2026-08-10→08-14]: NOT RECORDED" in line
    assert "(3 business days left)" in line
    assert "operator call, see STATE row 0" in line
    # Load-bearing wording: status, not a trade instruction / standing licence.
    assert "trade" not in line.lower()
    assert "licence" not in line.lower() and "license" not in line.lower()
    assert "remind" not in line.lower()


def test_not_recorded_when_compliance_missing(tmp_path):
    asof = date(2026, 8, 12)
    line = format_activity_decision_line(tmp_path, asof)
    assert "NOT RECORDED" in line


def test_recorded_via_coverage_limb(tmp_path):
    _write_compliance(
        tmp_path,
        "#### Follow-up\n\n"
        "| Date | Limb | Who / how | Result |\n"
        "|---|---|---|---|\n"
        "| 2026-08-12 (Wed) | **Coverage — 08-10→08-14 bucket** "
        "| **Operator-placed trade at the venue** | ✅ **COVERED** — the week discharged |\n",
    )
    asof = date(2026, 8, 12)
    monday, friday = mon_fri_week(asof)
    assert decision_status(
        (tmp_path / COMPLIANCE_REL).read_text(encoding="utf-8"), monday, friday
    ) == "RECORDED"
    line = format_activity_decision_line(tmp_path, asof)
    assert f"weekly activity decision [{week_label(monday, friday)}]: RECORDED" in line
    assert "(3 business days left)" in line
    assert "operator call, see STATE row 0" in line


def test_recorded_via_covered_heading(tmp_path):
    _write_compliance(
        tmp_path,
        "#### Follow-up entry — 2026-08-12: week 08-10→08-14 **COVERED**; next opens later\n",
    )
    assert "RECORDED" in format_activity_decision_line(tmp_path, date(2026, 8, 12))


def test_other_week_coverage_does_not_count(tmp_path):
    _write_compliance(
        tmp_path,
        "| 2026-08-07 (Fri) | **Coverage — 08-03→08-07 bucket** "
        "| Operator-placed | ✅ **COVERED** |\n"
        "**Next bucket: 2026-08-10 → 08-14**\n",
    )
    assert "NOT RECORDED" in format_activity_decision_line(tmp_path, date(2026, 8, 12))


def test_render_run_includes_status_line():
    line = (
        "weekly activity decision [2026-08-10→08-14]: NOT RECORDED "
        "(3 business days left) — operator call, see STATE row 0"
    )
    out = render_run(date(2026, 8, 12), findings=[], status_lines=[line])
    assert line in out
    assert out.index("## Run 2026-08-12") < out.index(line)
