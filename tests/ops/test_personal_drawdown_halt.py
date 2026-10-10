"""Personal-account 15% running-peak halt-and-flatten (ADR 2026-10-09 Decision 4, item 7).

Equity values are test fixtures (peak 100), not account figures.
"""
import json
import math

import pytest

import firm_rules
from personal_drawdown_halt import HaltStateError, PersonalDrawdownHalt as Halt

ACCOUNT, PORTFOLIO = "personal-test", "portfolio-test"


@pytest.fixture
def path(tmp_path):
    return tmp_path / "halt.json"


def _new(path, equity=100.0):
    return Halt.initialize(path, account=ACCOUNT, portfolio_id=PORTFOLIO, starting_equity=equity)


def _load(path):
    return Halt(path, account=ACCOUNT, portfolio_id=PORTFOLIO)


def _go(go_id="go-1", **over):
    return {"go_id": go_id, "operator": "Joshua", "account": ACCOUNT,
            "portfolio_id": PORTFOLIO, "rebase_peak": False, **over}


def _flat(_account):
    return 0


def test_threshold_is_the_tier_value():
    assert firm_rules.FIRM_RULES["Personal_Tradovate"]["max_dd_pct"] == 15.0


def test_running_permits_entries_and_ratchets_peak(path):
    h = _new(path)
    assert h.observe(110.0)["peak"] == 110.0
    assert h.observe(95.0)["state"] == "RUNNING"  # 13.6% below 110
    assert h.entry_permitted() and not h.flatten_required()


def test_intraday_trough_latches_through_recovery(path):
    h = _new(path)
    h.observe(84.9)  # intraday low, 15.1%
    assert h.observe(101.0)["state"] == "HALTED"  # close recovers above peak
    assert not h.entry_permitted() and h.flatten_required()
    assert _load(path).snapshot()["peak"] == 100.0


def test_gap_through_threshold_halts_on_one_observation(path):
    h = _new(path)
    assert h.observe(70.0)["state"] == "HALTED"


@pytest.mark.parametrize("equity,halted", [(85.0, True), (85.00001, True), (85.0001, False)])
def test_threshold_compare_rounds_to_six_places(path, equity, halted):
    assert (_new(path).observe(equity)["state"] == "HALTED") is halted


@pytest.mark.parametrize("bad", [math.nan, math.inf, 0.0, -1.0, True, "100", None])
def test_invalid_equity_halts(path, bad):
    h = _new(path)
    assert h.observe(bad)["state"] == "HALTED"
    assert h.snapshot()["incidents"][-1]["reason"] == "equity_invalid"


def test_restart_while_halted_stays_halted_and_demands_flatten(path):
    _new(path).observe(80.0)
    h = _load(path)
    assert not h.entry_permitted() and h.flatten_required()


def test_flatten_failure_keeps_demanding_flatten(path):
    h = _new(path)
    h.observe(80.0)

    def boom(_account):
        raise ConnectionError("broker down")

    for executor in (boom, lambda _a: 2, lambda _a: True, lambda _a: None):
        assert h.flatten(executor) is False
        assert h.snapshot()["flatten"] == "FAILED" and h.flatten_required()
        assert not h.entry_permitted()
    assert not h.resume(_go(rebase_peak=True), current_equity=80.0)
    assert h.flatten(_flat) is True and h.snapshot()["flatten"] == "CONFIRMED"
    assert not h.entry_permitted()  # flat is not resumed
    assert _load(path).snapshot()["flatten"] == "CONFIRMED"


def test_flatten_is_not_called_while_running(path):
    called = []
    assert _new(path).flatten(lambda a: called.append(a) or 0) is True
    assert called == []


def test_resume_requires_valid_operator_go(path):
    h = _new(path)
    h.observe(80.0)
    h.flatten(_flat)
    for go in (None, {}, _go(account="other"), _go(portfolio_id="other"), _go(go_id=""),
               _go(operator=""), _go(rebase_peak="yes")):
        assert not h.resume(go, current_equity=80.0)
    # Carried peak: equity still 20% below it, so a carry-peak GO is refused.
    assert not h.resume(_go(), current_equity=80.0)
    assert h.resume(_go(rebase_peak=True), current_equity=80.0)
    snap = h.snapshot()
    assert snap["state"] == "RUNNING" and snap["peak"] == 80.0 and h.entry_permitted()
    assert snap["resumes"][-1]["go_id"] == "go-1"


def test_carry_peak_resume_and_go_id_single_use(path):
    h = _new(path)
    h.observe(84.0)
    h.flatten(_flat)
    assert h.resume(_go(), current_equity=90.0)  # 10% below the carried peak
    assert h.snapshot()["peak"] == 100.0
    h.observe(80.0)
    h.flatten(_flat)
    assert not h.resume(_go(rebase_peak=True), current_equity=80.0)  # go-1 reused
    assert h.resume(_go("go-2", rebase_peak=True), current_equity=80.0)


def test_resume_with_invalid_equity_refused(path):
    h = _new(path)
    h.observe(80.0)
    h.flatten(_flat)
    assert not h.resume(_go(rebase_peak=True), current_equity=math.nan)


def test_incident_history_is_never_cleared(path):
    h = _new(path)
    h.observe(80.0)
    h.flatten(_flat)
    h.resume(_go(rebase_peak=True), current_equity=80.0)
    h.observe(60.0)
    assert [i["reason"] for i in _load(path).snapshot()["incidents"]] == ["drawdown", "drawdown"]


def test_missing_state_blocks_entries(path):
    h = _load(path)
    assert not h.entry_permitted() and h.flatten_required()
    with pytest.raises(HaltStateError):
        h.observe(100.0)


@pytest.mark.parametrize("mutate", [
    lambda s: "{not json",
    lambda s: json.dumps({**s, "account": "other"}),
    lambda s: json.dumps({**s, "portfolio_id": "other"}),
    lambda s: json.dumps({**s, "threshold": "0.30"}),
    lambda s: json.dumps({**s, "schema": "v0"}),
    lambda s: json.dumps({**s, "state": "ARMED"}),
    lambda s: json.dumps({**s, "peak": -5}),
    lambda s: json.dumps({**s, "extra": 1}),
    lambda s: json.dumps({**s, "state": "RUNNING", "flatten": "FAILED"}),
    lambda s: json.dumps({**s, "resumes": [{"operator": "x"}]}),
])
def test_corrupt_or_foreign_state_blocks_entries(path, mutate):
    _new(path)
    path.write_text(mutate(json.loads(path.read_text(encoding="utf-8"))), encoding="utf-8")
    assert not _load(path).entry_permitted()


def test_tier_threshold_change_invalidates_state(path, monkeypatch):
    _new(path)
    monkeypatch.setitem(firm_rules.FIRM_RULES["Personal_Tradovate"], "max_dd_pct", 30.0)
    assert not _load(path).entry_permitted()


def test_initialize_never_overwrites_state(path):
    _new(path).observe(80.0)
    with pytest.raises(HaltStateError):
        _new(path)
    assert _load(path).snapshot()["state"] == "HALTED"


def test_initialize_refuses_invalid_start(path):
    for bad in (0.0, math.nan, True):
        with pytest.raises(HaltStateError):
            _new(path, bad)
    assert not path.exists()


def test_persist_failure_latches_halt_in_process(path, monkeypatch):
    h = _new(path)

    def fail(*_a, **_k):
        raise OSError("disk full")

    monkeypatch.setattr("personal_drawdown_halt._atomic_write", fail)
    with pytest.raises(HaltStateError):
        h.observe(80.0)
    assert not h.entry_permitted() and h.flatten_required()
    with pytest.raises(HaltStateError):
        h.observe(100.0)
