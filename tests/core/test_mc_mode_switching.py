"""Mode-switching kernel path in simulate_path / run_seed (frozen 2026-10-05 §0.5).

Synthetic inputs only. The card's load-bearing property is stated once and tested
everywhere: **with the new keywords absent every existing output is byte-identical**.
With them present, a day reads its protected-regime twin exactly when the settled
drawdown from the end-of-day peak is at or below ``-mode_trigger`` — the same
predicate ``ops/c1_rail/book_policy.py::is_protected`` expresses (pinned separately
in tests/test_mode_switching_book_parity.py).

Nothing here touches DD_TRIGGER, DD_SCALE, NO_PROTECTION_TRIGGER, firm_rules or
book_policy: the mode-switching branch is only ever reached with an explicit
``protected_path``/``mode_trigger`` pair, and that pairing is itself validated.
"""
from __future__ import annotations

import numpy as np
import pytest

from core.mc.simulation import HISTORICAL_CHALLENGE_FIRM_KWARGS, run_seed, simulate_path
from discovery.prop_survivor_scoring import ScoringThresholds, run_tier_remc

START = 100_000.0
MODE_TRIGGER = 0.01
# One protection mechanism only: dd_trigger >= 1.0 disables continuous dd_scale
# de-risking (mirrors NO_PROTECTION_TRIGGER usage in the scoring harness).
NO_SCALING_TRIGGER = 10.0
UNIT_SCALE = 1.0

# Every barrier, the daily-loss gate, the pass target and the inactivity barrier are
# unreachable, so the only observable is the equity path itself (outcome / max_dd).
INERT = dict(
    starting_equity=START,
    daily_loss_pct=None,
    dd_type="static",
    static_dd_pct=-0.99,
    profit_target=START * 10.0,
    min_trading_days=0,
    inactivity_limit=10_000,
    consistency_frac=None,
)

# A reachable static floor ($97,000) for the tests that need a bust to be observable.
BARRIER = dict(INERT, static_dd_pct=-0.03)

# Tradeify Select 100K geometry: an unreachable lock reduces `trailing_locking` to a
# pure fixed-$3,000 end-of-day trail off peak (same idiom as test_mc_intraday_barrier).
TRAILING = dict(
    INERT,
    dd_type="trailing_locking",
    static_dd_pct=None,
    trailing_dd_pct=-0.03,
    dd_lock_offset_usd=1_000_000.0,
)

# Daily-loss gate ON at -2% ($2,000) for the selected-channel daily-loss test.
DAILY_LOSS = dict(INERT, daily_loss_pct=-0.02)


def _path(daily_pnls) -> np.ndarray:
    return np.array([[float(p)] for p in daily_pnls], dtype=float)


def _zeros(n: int) -> np.ndarray:
    return _path([0.0] * n)


# ── §0.5 item 1 / card §4 preamble: absent keywords are byte-identical ──────


def test_simulate_path_explicit_none_matches_the_legacy_call():
    """Omitting the keywords and passing None explicitly must agree exactly."""
    path = _path([-2_000.0, -1_000.0, -400.0, 300.0, 1_500.0, -2_500.0])
    legacy = simulate_path(path, 0.015, 0.40, 6, **INERT)
    explicit = simulate_path(
        path,
        0.015,
        0.40,
        6,
        protected_path=None,
        protected_intraday_low=None,
        mode_trigger=None,
        **INERT,
    )
    assert legacy == explicit


def test_run_seed_explicit_none_matches_the_legacy_call():
    blocks = np.array(
        [[[v] for v in (-1_500.0, 400.0, -900.0, 250.0, -2_100.0)] for _ in range(4)]
    )
    legacy = run_seed(
        42, 20, blocks, 0.015, 0.40, horizon=25, strats=("candidate",),
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS),
    )
    explicit = run_seed(
        42, 20, blocks, 0.015, 0.40, horizon=25, strats=("candidate",),
        firm_kwargs=dict(HISTORICAL_CHALLENGE_FIRM_KWARGS),
        protected_blocks=None,
        protected_intraday_blocks=None,
        mode_trigger=None,
    )
    assert legacy == explicit


def test_new_keywords_are_path_keywords_not_firm_semantics():
    """§0.5 item 1: all three names belong in _NON_FIRM_KEYWORDS."""
    from core.mc.simulation import _NON_FIRM_KEYWORDS

    assert {"protected_path", "protected_intraday_low", "mode_trigger"} <= set(
        _NON_FIRM_KEYWORDS
    )
    assert not (
        {"protected_path", "protected_intraday_low", "mode_trigger"}
        & set(HISTORICAL_CHALLENGE_FIRM_KWARGS)
    )


# ── card §4 (b): a path that never draws down ignores the protected channel ──


def test_never_drawdown_path_equals_the_normal_only_run():
    normal = _path([100.0, 250.0, -50.0, 400.0, 1_000.0, 60.0, -10.0, 900.0])
    # Wildly different protected twin: it must never be read, because equity never
    # sits at or below -1% from the running peak.
    protected = _path([-70_000.0] * 8)
    plain = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 8, **INERT)
    switched = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        8,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **INERT,
    )
    assert plain == switched
    assert plain[0] == "horizon_cap"


# ── card §4 (c): a path at or below -1% from day 2 switches from day 2 ───────


def test_path_at_one_percent_from_day_2_uses_protected_from_day_2():
    normal = _path([-2_000.0, -1_000.0, -1_000.0, -1_000.0])
    # Day 1 must read the NORMAL channel (a -70,000 protected twin would put equity
    # at 30,000 and max_dd at 0.70); days 2+ must read the protected twin (0 P&L).
    protected = _path([-70_000.0, 0.0, 0.0, 0.0])
    plain = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 4, **INERT)
    switched = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        4,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **INERT,
    )
    assert plain[0] == switched[0] == "horizon_cap"
    # Normal only: 100,000 -> 98,000 -> 97,000 -> 96,000 -> 95,000.
    assert plain[2] == pytest.approx(0.05)
    # Mode-switching: day 1 normal (-2,000 = 2% from peak), then flat at 98,000.
    assert switched[2] == pytest.approx(0.02)


def test_mode_is_recomputed_daily_with_no_latch():
    """Recovering above the peak returns the day to the normal channel."""
    normal = _path([-2_000.0, -50.0, -60.0, -50.0])
    # Day 3 is protected, so the RECOVERY itself must come from the protected twin;
    # it lifts equity to a new peak, and day 4 must then read the normal channel.
    protected = _path([-70_000.0, 0.0, 5_000.0, -70_000.0])
    plain = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 4, **BARRIER)
    switched = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        4,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **BARRIER,
    )
    # Normal only: 100,000 -> 98,000 -> 97,950 -> 97,890 -> 97,840.
    assert plain[0] == "horizon_cap"
    assert plain[2] == pytest.approx((START - 97_840.0) / START)
    # Mode-switching: -> 98,000 -> 98,000 (protected) -> 103,000 (new peak) -> 102,950.
    assert switched[0] == "horizon_cap"
    assert switched[2] == pytest.approx(0.02)
    # A latched mode would read the protected twin on day 4 and bust at $33,000.


# ── card §4 (d): equality at exactly -1.000000% (after rounding) is protected ─


def test_exactly_one_percent_boundary_is_protected():
    assert round((START - 1_000.0 - START) / START, 6) == -MODE_TRIGGER
    normal = _path([-1_000.0, -1_000.0, -1_000.0])
    protected = _path([-70_000.0, 0.0, 0.0])
    plain = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 3, **INERT)
    switched = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        3,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **INERT,
    )
    # Protected from day 2 -> equity pinned at 99,000 (max_dd exactly 1%).
    assert switched[2] == pytest.approx(0.01)
    # Control: the normal-only run keeps falling to 97,000.
    assert plain[2] == pytest.approx(0.03)


def test_just_above_one_percent_stays_normal():
    """$999 down = 0.00999 from peak, which rounds below the trigger."""
    assert round((START - 999.0 - START) / START, 6) > -MODE_TRIGGER
    normal = _path([-999.0, -1_000.0])
    protected = _path([-70_000.0, 0.0])
    plain = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 2, **INERT)
    switched = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **INERT,
    )
    assert plain == switched
    assert switched[0] == "horizon_cap"
    # Day 2 read the NORMAL channel (99,001 -> 98,001 = -1.9999%). Had the trigger
    # fired one ULP early, equity would have stayed at 99,001 (-0.9999%).
    assert switched[2] == pytest.approx(0.01999)


# ── §0.5 item 2: every other rule reads the selected channel unchanged ──────


def test_daily_loss_gate_reads_the_selected_channel():
    normal = _path([-1_500.0, 0.0])           # day 2 normal: no daily loss
    protected = _path([-70_000.0, -3_000.0])  # day 2 protected: -3% on the day
    out = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **DAILY_LOSS,
    )
    assert out[0] == "bust_daily"
    assert out[1] == 2
    assert out[3] == 0  # culprit argmin over the selected day's strategy_pnls

    control = simulate_path(normal, NO_SCALING_TRIGGER, UNIT_SCALE, 2, **DAILY_LOSS)
    assert control[0] == "horizon_cap"


def test_barrier_reads_the_selected_channel():
    normal = _path([-1_500.0, 0.0])
    protected = _path([-70_000.0, -4_000.0])  # 98,500 - 4,000 < 97,000 floor
    out = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **BARRIER,
    )
    assert out[0] == "bust_static"
    assert out[1] == 2


def test_inactivity_and_trade_days_read_the_selected_channel():
    """A protected day with zero P&L counts as idle, exactly as a normal one would."""
    normal = _path([-1_500.0, 0.0, 0.0, 0.0])
    protected = _path([-70_000.0, -10.0, 0.0, 0.0])
    idle = dict(INERT, inactivity_limit=2)
    out = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        4,
        protected_path=protected,
        mode_trigger=MODE_TRIGGER,
        **idle,
    )
    # Days 2 (-10) and 3 (0) and 4 (0): three consecutive idle days -> bust on day 4.
    assert out[0] == "bust_inactivity"
    assert out[1] == 4


def test_protected_intraday_low_is_used_on_protected_days_only():
    """The barrier excursion also follows the selected channel."""
    normal = _path([-1_500.0, 0.0])
    protected = _path([-70_000.0, 0.0])
    common = dict(intraday_low=np.array([0.0, 0.0]))
    shallow = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        protected_path=protected,
        protected_intraday_low=np.array([0.0, -1_000.0]),
        mode_trigger=MODE_TRIGGER,
        **dict(TRAILING, **common),
    )
    assert shallow[0] != "bust_trailing"  # 98,500 - 1,000 = 97,500 > 97,000 floor

    deep = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        protected_path=protected,
        protected_intraday_low=np.array([0.0, -2_000.0]),
        mode_trigger=MODE_TRIGGER,
        **dict(TRAILING, **common),
    )
    assert deep[0] == "bust_trailing"
    assert deep[1] == 2

    # Control: the NORMAL excursion (0) would not bust, so the protected one was read.
    normal_only = simulate_path(
        normal,
        NO_SCALING_TRIGGER,
        UNIT_SCALE,
        2,
        intraday_low=np.array([0.0, 0.0]),
        **TRAILING,
    )
    assert normal_only[0] == "horizon_cap"


# ── §0.5 item 1: every misuse raises ────────────────────────────────────────


def test_protected_path_without_mode_trigger_raises():
    with pytest.raises(ValueError, match="mode_trigger"):
        simulate_path(
            _path([-100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 1,
            protected_path=_path([-100.0]), **INERT,
        )


def test_mode_trigger_without_protected_path_raises():
    with pytest.raises(ValueError, match="protected_path"):
        simulate_path(
            _path([-100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 1,
            mode_trigger=MODE_TRIGGER, **INERT,
        )


def test_protected_intraday_low_without_protected_path_raises():
    with pytest.raises(ValueError, match="requires protected_path"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            intraday_low=np.array([0.0, 0.0]),
            protected_intraday_low=np.array([0.0, -10.0]),
            **INERT,
        )


def test_protected_path_with_intraday_low_but_no_twin_raises():
    with pytest.raises(ValueError, match="protected_intraday_low is required"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            intraday_low=np.array([0.0, 0.0]),
            protected_path=_path([-100.0, -100.0]),
            mode_trigger=MODE_TRIGGER,
            **INERT,
        )


def test_protected_intraday_low_without_intraday_low_raises():
    with pytest.raises(ValueError, match="requires intraday_low"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            protected_path=_path([-100.0, -100.0]),
            protected_intraday_low=np.array([0.0, -10.0]),
            mode_trigger=MODE_TRIGGER,
            **INERT,
        )


def test_protected_path_with_continuous_scaling_raises():
    """One protection mechanism only: dd_trigger must be >= 1.0."""
    with pytest.raises(ValueError, match="one protection mechanism only"):
        simulate_path(
            _path([-100.0]), 0.015, 0.40, 1,
            protected_path=_path([-100.0]), mode_trigger=MODE_TRIGGER, **INERT,
        )
    # At exactly 1.0 the channel is admissible (continuous scaling is unreachable).
    ok = simulate_path(
        _path([-100.0]), 1.0, 0.40, 1,
        protected_path=_path([-100.0]), mode_trigger=MODE_TRIGGER, **INERT,
    )
    assert ok[0] == "horizon_cap"


def test_protected_path_shorter_than_the_horizon_raises():
    with pytest.raises(ValueError, match="protected_path must cover the horizon"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            protected_path=_path([-100.0]), mode_trigger=MODE_TRIGGER, **INERT,
        )


def test_protected_intraday_low_validation_mirrors_intraday_low():
    base = dict(
        protected_path=_path([-100.0, -100.0]),
        mode_trigger=MODE_TRIGGER,
        intraday_low=np.array([0.0, 0.0]),
    )
    with pytest.raises(ValueError, match="protected_intraday_low must cover the horizon"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            protected_intraday_low=np.array([0.0]), **base, **INERT,
        )
    with pytest.raises(ValueError, match="must be <= 0.0"):
        simulate_path(
            _path([-100.0, -100.0]), NO_SCALING_TRIGGER, UNIT_SCALE, 2,
            protected_intraday_low=np.array([0.0, 25.0]), **base, **INERT,
        )


# ── §0.5 item 3: run_seed draws the protected blocks with the same indices ──


def test_run_seed_uses_the_same_indices_for_the_protected_channel():
    n_blocks = 12
    horizon = 30
    blocks = np.full((n_blocks, 5, 1), -2_000.0)          # every normal day: -2,000
    marker = np.arange(1, n_blocks + 1, dtype=float).reshape(n_blocks, 1, 1)
    protected = np.repeat(-10.0 * marker, 5, axis=1)       # block i -> -(10 * (i + 1))
    result = run_seed(
        7, 3, blocks, NO_SCALING_TRIGGER, UNIT_SCALE, horizon=horizon,
        strats=("candidate",), firm_kwargs=dict(INERT),
        protected_blocks=protected, mode_trigger=MODE_TRIGGER,
    )
    assert result["outcomes"]["horizon_cap"] == 3

    # Replay the one-index-draw-per-sim contract: day 1 is normal (equity == peak),
    # every later day is protected because equity only falls further from peak.
    rng = np.random.default_rng(7)
    blocks_per_sim = (horizon + 4) // 5
    for sim in range(3):
        indices = rng.integers(0, n_blocks, blocks_per_sim)
        drawn = np.concatenate(
            [np.asarray(protected[i], dtype=float).reshape(-1) for i in indices]
        )[:horizon]
        equity = [START - 2_000.0]
        for pnl in drawn[1:]:
            equity.append(equity[-1] + float(pnl))
        expected_max_dd = (START - min(equity)) / START
        assert result["max_dds"][sim] == pytest.approx(expected_max_dd)


def test_run_seed_validates_protected_block_lengths():
    blocks = np.zeros((4, 5, 1))
    with pytest.raises(ValueError, match="protected_blocks length 3"):
        run_seed(
            1, 2, blocks, NO_SCALING_TRIGGER, UNIT_SCALE, horizon=10,
            strats=("candidate",), firm_kwargs=dict(INERT),
            protected_blocks=np.zeros((3, 5, 1)), mode_trigger=MODE_TRIGGER,
        )
    with pytest.raises(ValueError, match="protected_intraday_blocks length 5"):
        run_seed(
            1, 2, blocks, NO_SCALING_TRIGGER, UNIT_SCALE, horizon=10,
            strats=("candidate",), firm_kwargs=dict(INERT),
            protected_blocks=np.zeros((4, 5, 1)),
            intraday_blocks=np.zeros((4, 5, 1)),
            protected_intraday_blocks=np.zeros((5, 5, 1)),
            mode_trigger=MODE_TRIGGER,
        )


def test_run_seed_rejects_mode_keywords_in_firm_kwargs():
    blocks = np.zeros((4, 5, 1))
    with pytest.raises(ValueError, match="not in firm_kwargs"):
        run_seed(
            1, 2, blocks, NO_SCALING_TRIGGER, UNIT_SCALE, horizon=10,
            strats=("candidate",),
            firm_kwargs=dict(INERT, mode_trigger=MODE_TRIGGER),
            protected_blocks=blocks,
        )


# ── §0.5 item 4: run_tier_remc threads the keywords ─────────────────────────


def _thresholds(horizon: int) -> ScoringThresholds:
    """Synthetic, in-test thresholds: nothing is read from a pre-registration."""
    return ScoringThresholds(
        eval_bust_ceiling=1.0,
        funded_bust_ceiling=1.0,
        pass_floor=0.0,
        tier_keys=("Tradeify_Select_100K",),
        seeds=(42,),
        sims_per_seed=1,
        horizon=horizon,
        cost_law_multiple=1.0,
        source_path="synthetic-mode-switching-test",
    )


def _tier_blocks(daily: float, n_weeks: int = 5) -> np.ndarray:
    return np.array(
        [[[daily] for _ in range(5)] for _ in range(n_weeks)], dtype=float
    )


def test_run_tier_remc_threads_the_mode_switching_keywords():
    thr = _thresholds(20)
    firm = "Tradeify_Select_100K"
    blocks = _tier_blocks(-1_500.0)
    zeros = np.zeros_like(blocks)

    plain = run_tier_remc(firm, blocks, thr, n_sims=8)
    # A protected twin identical to the normal channel, with a zeros intraday pair,
    # must reproduce the plain (EOD, no-mode) figures exactly.
    identity = run_tier_remc(
        firm, blocks, thr, n_sims=8,
        intraday_blocks=zeros, protected_blocks=blocks,
        protected_intraday_blocks=zeros, mode_trigger=MODE_TRIGGER,
    )
    assert identity["headline_bust"] == pytest.approx(plain["headline_bust"])
    assert identity["pass_rate"] == pytest.approx(plain["pass_rate"])
    assert identity["summary"]["rates"] == plain["summary"]["rates"]

    # A flat protected twin de-risks every day from the first 1% drawdown: the
    # fixed-$3,000 trail is never reached, so the tier stops busting.
    switched = run_tier_remc(
        firm, blocks, thr, n_sims=8,
        intraday_blocks=zeros, protected_blocks=zeros,
        protected_intraday_blocks=zeros, mode_trigger=MODE_TRIGGER,
    )
    assert plain["headline_bust"] == pytest.approx(1.0)
    assert switched["headline_bust"] == pytest.approx(0.0)
    assert switched["pass_rate"] != plain["pass_rate"] or (
        switched["headline_bust"] != plain["headline_bust"]
    )


def test_run_tier_remc_without_the_keywords_is_byte_identical():
    thr = _thresholds(20)
    firm = "Tradeify_Select_100K"
    blocks = _tier_blocks(-1_500.0)
    plain = run_tier_remc(firm, blocks, thr, n_sims=8)
    explicit = run_tier_remc(
        firm, blocks, thr, n_sims=8,
        protected_blocks=None, protected_intraday_blocks=None, mode_trigger=None,
    )
    assert plain == explicit


def test_run_seed_rejects_orphan_mode_keywords():
    """run_seed fails closed: no silently ignored mode-switching keyword."""




    blocks = np.zeros((4, 5, 1))
    lows = np.zeros((4, 5, 1))
    with pytest.raises(ValueError, match="require protected_blocks"):
        run_seed(1, 2, blocks, 10.0, 0.4, horizon=10, strats=("a",), mode_trigger=0.01)
    with pytest.raises(ValueError, match="require protected_blocks"):
        run_seed(1, 2, blocks, 10.0, 0.4, horizon=10, strats=("a",),
                 intraday_blocks=lows, protected_intraday_blocks=lows)
    with pytest.raises(ValueError, match="requires intraday_blocks"):
        run_seed(1, 2, blocks, 10.0, 0.4, horizon=10, strats=("a",),
                 protected_blocks=blocks, protected_intraday_blocks=lows, mode_trigger=0.01)
