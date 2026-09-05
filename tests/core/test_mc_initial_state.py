"""Used-account session-boundary state for the Monte Carlo kernel.

All examples are synthetic and use small hand-checkable paths.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import numpy as np
import pytest

from core.mc.simulation import EvaluationState, run_seed, simulate_path


START = 100_000.0


def _path(*daily_pnls: float) -> np.ndarray:
    return np.array([[pnl] for pnl in daily_pnls], dtype=float)


def _rules(**overrides: object) -> dict[str, object]:
    rules: dict[str, object] = {
        "starting_equity": START,
        "daily_loss_pct": None,
        "dd_type": "trailing_locking",
        "static_dd_pct": -0.03,
        "trailing_dd_pct": -0.03,
        "dd_lock_offset_usd": 1_000_000.0,
        "profit_target": 110_000.0,
        "min_trading_days": 0,
        "inactivity_limit": 100,
        "consistency_frac": None,
    }
    rules.update(overrides)
    return rules


def _state(
    *,
    equity: float = START,
    peak: float = START,
    days: int = 0,
    best: float = 0.0,
) -> EvaluationState:
    return EvaluationState(START, equity, peak, days, best)


def test_evaluation_state_is_required_frozen_and_normalized() -> None:
    with pytest.raises(TypeError):
        EvaluationState()  # type: ignore[call-arg]

    state = EvaluationState(100_000, 100_000, 100_000, 0, 0)
    assert state == EvaluationState(100_000.0, 100_000.0, 100_000.0, 0, 0.0)
    with pytest.raises(FrozenInstanceError):
        state.current_equity = 99_000.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("original_basis", True),
        ("current_equity", "100000"),
        ("historical_eod_peak", float("nan")),
        ("prior_max_day_profit", float("inf")),
        ("original_basis", 0.0),
        ("current_equity", -1.0),
        ("historical_eod_peak", 0.0),
        ("prior_max_day_profit", -0.01),
    ],
)
def test_evaluation_state_rejects_invalid_amounts(field: str, value: object) -> None:
    values: dict[str, object] = {
        "original_basis": START,
        "current_equity": START,
        "historical_eod_peak": START,
        "prior_trade_days": 0,
        "prior_max_day_profit": 0.0,
    }
    values[field] = value
    with pytest.raises((TypeError, ValueError)):
        EvaluationState(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize("days", [True, -1, 1.5, float("nan")])
def test_evaluation_state_rejects_invalid_trade_days(days: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        EvaluationState(START, START, START, days, 0.0)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "values",
    [
        (START, START + 1.0, START, 1, 1.0),
        (START, START, START - 1.0, 1, 0.0),
        (START, START - 1.0, START, 0, 0.0),
        (START, START, START, 0, 0.01),
        (START, START, START + 1.0, 1, 0.0),
        (START, START, START + 100.01, 2, 50.0),
    ],
)
def test_evaluation_state_rejects_internally_inconsistent_history(values: tuple) -> None:
    with pytest.raises(ValueError):
        EvaluationState(*values)


def test_prior_peak_gain_consistency_is_compared_at_cents_precision() -> None:
    state = EvaluationState(START, START, START + 100.004, 2, 50.0)
    assert state.historical_eod_peak == pytest.approx(100_100.004)


def test_absent_none_and_pristine_state_agree_before_any_terminal_condition() -> None:
    path = _path(100.0, -50.0)
    rules = _rules(profit_target=200_000.0)
    absent = simulate_path(path, 0.015, 0.40, 2, **rules)
    explicit_none = simulate_path(path, 0.015, 0.40, 2, initial_state=None, **rules)
    pristine = simulate_path(path, 0.015, 0.40, 2, initial_state=_state(), **rules)
    assert absent == explicit_none == pristine


def test_used_account_reaches_original_target_sooner_and_basis_mismatch_is_rejected() -> None:
    used = _state(equity=108_000.0, peak=108_000.0, days=2, best=5_000.0)
    rules = _rules()
    assert simulate_path(_path(2_000.0), 0.015, 0.40, 1, initial_state=used, **rules) == (
        "pass",
        1,
        0.0,
        None,
    )
    assert simulate_path(_path(2_000.0), 0.015, 0.40, 1, **rules)[0] == "horizon_cap"

    rebased = dict(rules, starting_equity=108_000.0, profit_target=118_000.0)
    with pytest.raises(ValueError, match="basis"):
        simulate_path(_path(2_000.0), 0.015, 0.40, 1, initial_state=used, **rebased)


def test_historical_peak_controls_floor_and_intraday_touch_fails() -> None:
    low_peak = _state(equity=99_000.0, peak=START, days=1, best=0.0)
    high_peak = _state(equity=99_000.0, peak=101_500.0, days=1, best=1_500.0)
    path = _path(100.0)
    # The high-peak snapshot is already beyond the 1.5% protection trigger, so
    # -$1,250 is scaled to -$500 and touches its $98,500 floor. The low-peak
    # snapshot remains full-size and stays above its lower $97,000 floor.
    excursion = np.array([-1_250.0])

    survives = simulate_path(
        path, 0.015, 0.40, 1, initial_state=low_peak, intraday_low=excursion, **_rules()
    )
    touches = simulate_path(
        path, 0.015, 0.40, 1, initial_state=high_peak, intraday_low=excursion, **_rules()
    )
    assert survives[0] == "horizon_cap"
    assert touches[:2] == ("bust_trailing", 1)


def test_historical_peak_activates_existing_dd_protection_haircut() -> None:
    protected = _state(equity=START, peak=102_000.0, days=1, best=2_000.0)
    pristine = _state()
    rules = _rules(profit_target=100_500.0)
    assert simulate_path(
        _path(1_000.0), 0.015, 0.40, 1, initial_state=protected, **rules
    )[0] == "horizon_cap"
    assert simulate_path(
        _path(1_000.0), 0.015, 0.40, 1, initial_state=pristine, **rules
    )[:2] == ("pass", 1)


def test_prior_best_day_delays_consistency_clearance() -> None:
    clears_soon = _state(equity=108_000.0, peak=108_000.0, days=2, best=4_000.0)
    clears_later = _state(equity=108_000.0, peak=108_000.0, days=2, best=7_000.0)
    rules = _rules(consistency_frac=0.40)
    path = _path(2_000.0, 5_000.0, 5_000.0)
    assert simulate_path(path, 0.015, 0.40, 3, initial_state=clears_soon, **rules)[:2] == (
        "pass",
        1,
    )
    assert simulate_path(path, 0.015, 0.40, 3, initial_state=clears_later, **rules)[:2] == (
        "pass",
        3,
    )


def test_prior_trade_days_qualify_but_are_not_added_to_elapsed_days() -> None:
    used = _state(equity=109_000.0, peak=109_000.0, days=4, best=3_000.0)
    rules = _rules(min_trading_days=5)
    assert simulate_path(_path(1_000.0), 0.015, 0.40, 1, initial_state=used, **rules)[:2] == (
        "pass",
        1,
    )


def test_already_passing_state_returns_day_zero_with_snapshot_drawdown() -> None:
    state = _state(equity=110_000.0, peak=112_000.0, days=5, best=4_000.0)
    got = simulate_path(
        _path(999.0),
        0.015,
        0.40,
        1,
        initial_state=state,
        **_rules(min_trading_days=5),
    )
    assert got == ("pass", 0, pytest.approx(2_000.0 / 112_000.0), None)


@pytest.mark.parametrize(
    "rules",
    [
        _rules(dd_type="static", static_dd_pct=-0.03),
        _rules(dd_type="trailing", trailing_dd_pct=-0.03),
        _rules(
            dd_type="trailing_locking",
            trailing_dd_pct=-0.03,
            dd_lock_offset_usd=1_000_000.0,
        ),
    ],
    )
def test_initial_floor_touch_is_rejected_before_pass_status(rules: dict[str, object]) -> None:
    if rules["dd_type"] == "static":
        state = _state(equity=97_000.0, peak=110_000.0, days=5, best=10_000.0)
    elif rules["dd_type"] == "trailing":
        state = _state(equity=110_580.0, peak=114_000.0, days=5, best=10_000.0)
    else:
        state = _state(equity=110_000.0, peak=113_000.0, days=5, best=10_000.0)
    with pytest.raises(ValueError, match="drawdown floor"):
        simulate_path(_path(), 0.015, 0.40, 0, initial_state=state, **rules)


def test_explicit_state_requires_exact_type_and_inactivity_off() -> None:
    with pytest.raises(TypeError, match="EvaluationState"):
        simulate_path(_path(0.0), 0.015, 0.40, 1, initial_state={}, **_rules())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="inactivity"):
        simulate_path(
            _path(0.0),
            0.015,
            0.40,
            1,
            initial_state=_state(),
            **_rules(inactivity_limit=1),
        )


@pytest.mark.parametrize(
    "overrides",
    [
        {"horizon": True},
        {"horizon": -1},
        {"inactivity_limit": 1.5},
        {"min_trading_days": -1},
        {"profit_target": float("nan")},
        {"daily_loss_pct": 0.0},
        {"consistency_frac": 0.0},
        {"dd_type": "unknown"},
        {"dd_type": "static", "static_dd_pct": None},
        {"dd_type": "static", "static_dd_pct": 0.0},
        {"dd_type": "trailing", "trailing_dd_pct": None},
        {"dd_type": "trailing", "trailing_dd_pct": 0.0},
        {"dd_type": "trailing_locking", "dd_lock_offset_usd": None},
        {"dd_type": "trailing_locking", "dd_lock_offset_usd": -1.0},
        {"dd_trigger": float("inf")},
        {"dd_scale": -0.1},
    ],
)
def test_explicit_state_rejects_malformed_or_inert_rule_inputs(overrides: dict[str, object]) -> None:
    horizon = overrides.pop("horizon", 1)
    dd_trigger = overrides.pop("dd_trigger", 0.015)
    dd_scale = overrides.pop("dd_scale", 0.40)
    rules = _rules(**overrides)
    with pytest.raises((TypeError, ValueError)):
        simulate_path(
            _path(0.0),
            dd_trigger,  # type: ignore[arg-type]
            dd_scale,  # type: ignore[arg-type]
            horizon,  # type: ignore[arg-type]
            initial_state=_state(),
            **rules,
        )


def test_run_seed_restarts_each_path_from_the_same_state() -> None:
    blocks = np.full((1, 5, 1), 500.0)
    state = _state(equity=109_000.0, peak=109_000.0, days=2, best=4_500.0)
    got = run_seed(
        7,
        3,
        blocks,
        0.015,
        0.40,
        horizon=2,
        strats=("synthetic",),
        firm_kwargs=_rules(),
        initial_state=state,
    )
    assert got["outcomes"]["pass"] == 3
    assert got["days_to_pass"] == [2, 2, 2]


def test_run_seed_keeps_intraday_blocks_paired_with_used_state() -> None:
    blocks = np.full((1, 5, 1), 100.0)
    intraday = np.full((1, 5, 1), -1_250.0)
    state = _state(equity=99_000.0, peak=101_500.0, days=1, best=1_500.0)
    got = run_seed(
        11,
        2,
        blocks,
        0.015,
        0.40,
        horizon=1,
        strats=("synthetic",),
        firm_kwargs=_rules(),
        intraday_blocks=intraday,
        initial_state=state,
    )
    assert got["outcomes"]["bust_trailing"] == 2
    assert got["bust_attribution"] == {"synthetic": 2}


def test_run_seed_rejects_state_in_firm_kwargs() -> None:
    rules = _rules(initial_state=_state())
    with pytest.raises(ValueError, match="initial_state"):
        run_seed(1, 1, np.zeros((1, 5, 1)), 0.015, 0.40, horizon=1, firm_kwargs=rules)


def test_run_seed_validates_explicit_state_for_empty_batch() -> None:
    mismatched = EvaluationState(50_000.0, 50_000.0, 50_000.0, 0, 0.0)
    with pytest.raises(ValueError, match="basis"):
        run_seed(
            1,
            0,
            np.zeros((1, 5, 1)),
            0.015,
            0.40,
            horizon=1,
            firm_kwargs=_rules(),
            initial_state=mismatched,
        )


@pytest.mark.parametrize(
    ("rules", "state"),
    [
        (
            _rules(dd_type="static", static_dd_pct=-0.03),
            _state(equity=97_000.0, peak=110_000.0, days=5, best=10_000.0),
        ),
        (
            _rules(dd_type="trailing", trailing_dd_pct=-0.03),
            _state(equity=110_580.0, peak=114_000.0, days=5, best=10_000.0),
        ),
        (
            _rules(
                dd_type="trailing_locking",
                trailing_dd_pct=-0.03,
                dd_lock_offset_usd=1_000_000.0,
            ),
            _state(equity=110_000.0, peak=113_000.0, days=5, best=10_000.0),
        ),
    ],
)
def test_run_seed_empty_batch_rejects_initial_floor_touch(
    rules: dict[str, object], state: EvaluationState
) -> None:
    with pytest.raises(ValueError, match="drawdown floor"):
        run_seed(
            1,
            0,
            np.zeros((1, 5, 1)),
            0.015,
            0.40,
            horizon=0,
            firm_kwargs=rules,
            initial_state=state,
        )


@pytest.mark.parametrize(
    ("daily_pnl", "profit_target"),
    [
        (float("nan"), 110_000.0),
        (100.0, float("nan")),
    ],
)
def test_legacy_unordered_equity_target_comparison_does_not_pass(
    daily_pnl: float, profit_target: float
) -> None:
    got = simulate_path(
        _path(daily_pnl),
        0.015,
        0.40,
        1,
        **_rules(profit_target=profit_target),
    )
    assert got[:2] == ("horizon_cap", 1)


@pytest.mark.parametrize("with_intraday", [False, True])
@pytest.mark.parametrize("already_passing", [False, True])
def test_run_seed_horizon_zero_uses_explicit_state_without_a_sampled_path(
    already_passing: bool, with_intraday: bool
) -> None:
    blocks = np.zeros((1, 5, 1))
    intraday_blocks = np.zeros((1, 5, 1)) if with_intraday else None
    state = (
        _state(equity=110_000.0, peak=110_000.0, days=5, best=2_000.0)
        if already_passing
        else _state()
    )

    got = run_seed(
        19,
        2,
        blocks,
        0.015,
        0.40,
        horizon=0,
        strats=("synthetic",),
        firm_kwargs=_rules(min_trading_days=5),
        intraday_blocks=intraday_blocks,
        initial_state=state,
    )

    terminal = "pass" if already_passing else "horizon_cap"
    assert got["outcomes"][terminal] == 2
    assert sum(got["outcomes"].values()) == 2
    assert got["days_to_pass"] == ([0, 0] if already_passing else [])
    assert got["max_dds"] == [0.0, 0.0]


def test_run_seed_horizon_zero_without_state_preserves_legacy_error() -> None:
    with pytest.raises(ValueError):
        run_seed(
            19,
            1,
            np.zeros((1, 5, 1)),
            0.015,
            0.40,
            horizon=0,
            strats=("synthetic",),
            firm_kwargs=_rules(),
        )
