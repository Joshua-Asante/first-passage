from datetime import date, datetime, timedelta, timezone
import hashlib
import pytest
from c1_signal_daemon.feed import Bar
from c1_rail.qualification.model import LEG_IDS, SessionSchedule
from c1_rail.qualification.panel import build_panel, load_bar_csv, PanelError


def fixture():
    t = datetime(2020, 1, 6, 15, tzinfo=timezone.utc)
    bars = tuple(Bar(t + timedelta(minutes=15*i), 100, 101, 99, 100) for i in range(2))
    panels = {leg: bars for leg in LEG_IDS}
    end = t.replace(hour=21)
    schedules = {date(2020,1,6): SessionSchedule(end-timedelta(minutes=15),end-timedelta(minutes=5),end)}
    return panels, schedules


def test_missing_active_flat_leg_excludes_whole_session():
    panels, schedules = fixture()
    panels[LEG_IDS[0]] = panels[LEG_IDS[0]][:1]
    result = build_panel(panels, schedules=schedules, expected_dates=tuple(schedules), active=lambda leg,t:True)
    assert result.sessions == ()
    assert len(result.exclusions) == 1
    assert result.exclusions[0].reason == 'missing_active_bar'


def test_missing_outside_window_allowed_but_no_imputation():
    panels, schedules = fixture()
    panels[LEG_IDS[0]] = panels[LEG_IDS[0]][:1]
    result = build_panel(panels, schedules=schedules, expected_dates=tuple(schedules), active=lambda leg,t:leg!=LEG_IDS[0] or t.minute==0)
    assert len(result.sessions) == 1
    assert len(result.sessions[0].bars[1].bars) == 3


def test_unknown_calendar_and_completely_absent_session_fail_closed():
    panels, schedules = fixture()
    with pytest.raises(PanelError, match='calendar'):
        build_panel(panels,schedules={},expected_dates=tuple(schedules),active=lambda l,t:True)
    panels = {leg: () for leg in LEG_IDS}
    report=build_panel(panels,schedules=schedules,expected_dates=tuple(schedules),active=lambda l,t:True)
    assert report.exclusions[0].reason == 'missing_entire_session'


def test_csv_digest_checked_before_parsing_and_duplicates_rejected(tmp_path):
    content=b'time,open,high,low,close,volume\n2020-01-06T15:00:00+00:00,100,101,99,100,1\n'
    path=tmp_path/'synthetic.csv';path.write_bytes(content)
    assert len(load_bar_csv(path,hashlib.sha256(content).hexdigest()))==1
    with pytest.raises(PanelError,match='digest'):
        load_bar_csv(path,'0'*64)
    duplicated=content+content.splitlines(keepends=True)[1];path.write_bytes(duplicated)
    with pytest.raises(PanelError,match='duplicate'):
        load_bar_csv(path,hashlib.sha256(duplicated).hexdigest())
