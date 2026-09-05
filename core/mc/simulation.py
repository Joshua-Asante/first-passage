"""Deterministic path and seeded bootstrap simulation for portfolio MC."""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral, Real
from typing import Tuple

import numpy as np

try:
    from ..historical_challenge import (
        DAILY_LOSS_PCT_SIGNED,
        HISTORICAL_CHALLENGE_BASIS,
        HISTORICAL_CHALLENGE_FIRM_KWARGS,
        INACTIVITY_LIMIT,
        MIN_TRADING_DAYS,
        PROFIT_TARGET_ABS,
        STARTING_EQUITY,
        STATIC_DD_PCT_SIGNED,
    )
except ImportError:
    from historical_challenge import (
        DAILY_LOSS_PCT_SIGNED,
        HISTORICAL_CHALLENGE_BASIS,
        HISTORICAL_CHALLENGE_FIRM_KWARGS,
        INACTIVITY_LIMIT,
        MIN_TRADING_DAYS,
        PROFIT_TARGET_ABS,
        STARTING_EQUITY,
        STATIC_DD_PCT_SIGNED,
    )

# Re-export historical challenge fixture (ADR 2026-07-22 Phase 4).
# Defaults below stay byte-identical to the retired FIRM_RULES["FXIFY"] pin;
# living prop runs must pass firm kwargs explicitly via preflight.firm_kwargs.
PROFIT_TARGET = PROFIT_TARGET_ABS
DAILY_LOSS_PCT = DAILY_LOSS_PCT_SIGNED
STATIC_DD_PCT = STATIC_DD_PCT_SIGNED
HORIZON_CAP = 1500
DEFAULT_STRATS = ("guardian", "striker", "aegis", "striker_nas100")

# Keyword-only params of simulate_path that are NOT firm semantics and therefore do
# not belong in the fixture above. Same rationale as `horizon` (excluded by being
# positional): these describe the PATH, not the firm's rules, so a firm config could
# never supply them and the totality check must not demand a fixture entry.
#
# `intraday_low` — per-day minimum equity excursion, supplied alongside `path` by a
# caller that has intraday resolution. Absent => the legacy end-of-day barrier test,
# which is what the historical anchor was calibrated under.
_NON_FIRM_KEYWORDS: frozenset[str] = frozenset({"initial_state", "intraday_low"})


def _amount(name: str, value: Real, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite real number")
    amount = float(value)
    if not np.isfinite(amount):
        raise ValueError(f"{name} must be finite")
    if positive and amount <= 0.0:
        raise ValueError(f"{name} must be positive")
    return amount


def _nonnegative_count(name: str, value: Integral) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be a nonnegative integer")
    count = int(value)
    if count < 0:
        raise ValueError(f"{name} must be nonnegative")
    return count


@dataclass(frozen=True)
class EvaluationState:
    """Settled evaluation state at the boundary before a modeled session.

    The caller is responsible for establishing that the snapshot has no pending
    orders, current-session trading, deposits, withdrawals, or account adjustments.
    These five values check internal consistency; they cannot certify provenance.
    """

    original_basis: float
    current_equity: float
    historical_eod_peak: float
    prior_trade_days: int
    prior_max_day_profit: float

    def __post_init__(self) -> None:
        basis = _amount("original_basis", self.original_basis, positive=True)
        equity = _amount("current_equity", self.current_equity, positive=True)
        peak = _amount("historical_eod_peak", self.historical_eod_peak, positive=True)
        trade_days = _nonnegative_count("prior_trade_days", self.prior_trade_days)
        best_day = _amount("prior_max_day_profit", self.prior_max_day_profit)
        if best_day < 0.0:
            raise ValueError("prior_max_day_profit must be nonnegative")
        if peak < basis or peak < equity:
            raise ValueError(
                "historical_eod_peak must be at least original_basis and current_equity"
            )
        if trade_days == 0 and not (
            equity == basis and peak == basis and best_day == 0.0
        ):
            raise ValueError(
                "zero prior_trade_days require pristine equity, peak, and best-day profit"
            )
        peak_gain = peak - basis
        if peak_gain > 0.0:
            if best_day <= 0.0:
                raise ValueError(
                    "a positive historical peak gain requires a positive best day"
                )
            if round(peak_gain, 2) > round(trade_days * best_day, 2):
                raise ValueError(
                    "historical peak gain cannot exceed prior_trade_days times "
                    "prior_max_day_profit"
                )

        object.__setattr__(self, "original_basis", basis)
        object.__setattr__(self, "current_equity", equity)
        object.__setattr__(self, "historical_eod_peak", peak)
        object.__setattr__(self, "prior_trade_days", trade_days)
        object.__setattr__(self, "prior_max_day_profit", best_day)


def _validate_fraction(
    name: str,
    value: Real,
    *,
    allow_zero: bool = False,
) -> float:
    fraction = _amount(name, value)
    lower_ok = fraction >= 0.0 if allow_zero else fraction > 0.0
    if not lower_ok or fraction > 1.0:
        bound = (
            "between zero and one"
            if allow_zero
            else "greater than zero and at most one"
        )
        raise ValueError(f"{name} must be {bound}")
    return fraction


def _validate_initial_state_configuration(
    initial_state: EvaluationState,
    *,
    dd_trigger: float,
    dd_scale: float,
    horizon: int,
    starting_equity: float,
    daily_loss_pct: float | None,
    dd_type: str,
    static_dd_pct: float | None,
    trailing_dd_pct: float | None,
    dd_lock_offset_usd: float | None,
    profit_target: float,
    min_trading_days: int,
    inactivity_limit: int,
    consistency_frac: float | None,
) -> None:
    if type(initial_state) is not EvaluationState:
        raise TypeError("initial_state must be exactly an EvaluationState")

    basis = _amount("starting_equity", starting_equity, positive=True)
    if initial_state.original_basis != basis:
        raise ValueError(
            "initial_state original_basis must match starting_equity; "
            "build firm kwargs from the original basis"
        )

    horizon_count = _nonnegative_count("horizon", horizon)
    inactivity_count = _nonnegative_count("inactivity_limit", inactivity_limit)
    if inactivity_count <= horizon_count:
        raise ValueError(
            "initial_state supports inactivity-OFF only: inactivity_limit must exceed horizon"
        )
    _nonnegative_count("min_trading_days", min_trading_days)

    _validate_fraction("dd_trigger", dd_trigger, allow_zero=True)
    _validate_fraction("dd_scale", dd_scale, allow_zero=True)
    target = _amount("profit_target", profit_target, positive=True)
    if target <= basis:
        raise ValueError("profit_target must exceed the original starting_equity")
    if daily_loss_pct is not None:
        daily_limit = _amount("daily_loss_pct", daily_loss_pct)
        if not -1.0 < daily_limit < 0.0:
            raise ValueError("daily_loss_pct must be greater than -1 and less than zero")
    if consistency_frac is not None:
        _validate_fraction("consistency_frac", consistency_frac)

    if dd_type == "static":
        barrier = _amount("static_dd_pct", static_dd_pct)  # type: ignore[arg-type]
        if not -1.0 < barrier < 0.0:
            raise ValueError("static_dd_pct must be greater than -1 and less than zero")
    elif dd_type in ("trailing", "trailing_locking"):
        barrier = _amount("trailing_dd_pct", trailing_dd_pct)  # type: ignore[arg-type]
        if not -1.0 < barrier < 0.0:
            raise ValueError("trailing_dd_pct must be greater than -1 and less than zero")
        if dd_type == "trailing_locking":
            lock_offset = _amount(
                "dd_lock_offset_usd", dd_lock_offset_usd  # type: ignore[arg-type]
            )
            if lock_offset < 0.0:
                raise ValueError("dd_lock_offset_usd must be nonnegative")
    else:
        raise ValueError(
            "dd_type must be 'static', 'trailing', or 'trailing_locking' for initial_state"
        )


def _drawdown_outcome(
    equity_test: float,
    peak: float,
    *,
    starting_equity: float,
    dd_type: str,
    static_dd_pct: float,
    trailing_dd_pct: float | None,
    dd_lock_offset_usd: float | None,
) -> str | None:
    if dd_type == "trailing":
        if (
            trailing_dd_pct is not None
            and round((equity_test - peak) / peak, 6) <= trailing_dd_pct
        ):
            return "bust_trailing"
    elif dd_type == "trailing_locking":
        if trailing_dd_pct is not None and dd_lock_offset_usd is not None:
            max_dd_usd = -trailing_dd_pct * starting_equity
            floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)
            if round((equity_test - floor) / starting_equity, 6) <= 0.0:
                return "bust_trailing"
    elif round((equity_test - starting_equity) / starting_equity, 6) <= static_dd_pct:
        return "bust_static"
    return None


def _has_passed(
    equity: float,
    trade_days: int,
    max_day_profit: float,
    *,
    starting_equity: float,
    profit_target: float,
    min_trading_days: int,
    consistency_frac: float | None,
) -> bool:
    if round(equity, 2) < profit_target or trade_days < min_trading_days:
        return False
    if consistency_frac is None:
        return True
    total_profit = equity - starting_equity
    return total_profit <= 0.0 or round(
        max_day_profit - consistency_frac * total_profit, 2
    ) <= 0.0


def simulate_path(
    path: np.ndarray,
    dd_trigger: float,
    dd_scale: float,
    horizon: int,
    *,
    starting_equity: float = STARTING_EQUITY,
    daily_loss_pct: float | None = DAILY_LOSS_PCT,
    dd_type: str = "static",
    static_dd_pct: float = STATIC_DD_PCT,
    trailing_dd_pct: float | None = None,
    dd_lock_offset_usd: float | None = None,
    profit_target: float = PROFIT_TARGET,
    min_trading_days: int = MIN_TRADING_DAYS,
    inactivity_limit: int = INACTIVITY_LIMIT,
    consistency_frac: float | None = None,
    intraday_low: np.ndarray | None = None,
    initial_state: EvaluationState | None = None,
) -> Tuple[str, int, float, int | None]:
    """Run one deterministic challenge simulation over a strategy-P&L path.

    `intraday_low` (OPTIONAL, default None -> byte-identical legacy behaviour)
    ------------------------------------------------------------------------
    Per-day minimum equity EXCURSION in dollars, measured from that day's OPENING
    equity, so entries are <= 0.0 and UNSCALED (this function applies `dd_scale`
    to them exactly as it does to `path`).

    Why it exists: Tradeify's own rule page (help.tradeify.co art. 10495897, read
    2026-07-30) states the drawdown LIMIT updates end-of-day but the BREACH is
    "ENFORCED in real-time ... your account fails immediately - even if you might
    have recovered by end of day". This loop carries one P&L scalar per business day
    and previously tested the barrier only against the CLOSE, so it could not see a
    path that touched the floor intraday and recovered. Every bust figure produced
    without this argument is therefore a LOWER BOUND, not an estimate.

    Two-clock geometry, faithfully: the FLOOR still ratchets on end-of-day equity
    (`peak` is unchanged); only the equity TESTED against it gains the intraday
    minimum. That is exactly what the venue describes.

    Deliberately NOT changed, to avoid moving separately-published numbers:
      * `max_dd` stays END-OF-DAY denominated (it feeds the published p99-DD series).
      * the daily-loss check stays on the day's realized `pnl`.
    Both are documented limitations, not oversights; widening either is its own
    re-MC + amending ADR.

    Passing None reproduces the historical anchor byte-for-byte - the barrier
    comparison then reads `equity_new` itself, not a recomputed equal value.
    """
    if intraday_low is not None:
        intraday_low = np.asarray(intraday_low, dtype=float)
        if intraday_low.shape[0] < horizon:
            raise ValueError(
                f"intraday_low must cover the horizon: got {intraday_low.shape[0]} "
                f"day(s), need {horizon}"
            )
        if np.any(intraday_low > 0.0):
            raise ValueError(
                "intraday_low entries are excursions BELOW the day's opening equity "
                "and must be <= 0.0; got a positive value"
            )
    if initial_state is None:
        equity = peak = float(starting_equity)
        trade_days = 0
        max_dd = 0.0
        max_day_profit = 0.0
    else:
        _validate_initial_state_configuration(
            initial_state,
            dd_trigger=dd_trigger,
            dd_scale=dd_scale,
            horizon=horizon,
            starting_equity=starting_equity,
            daily_loss_pct=daily_loss_pct,
            dd_type=dd_type,
            static_dd_pct=static_dd_pct,
            trailing_dd_pct=trailing_dd_pct,
            dd_lock_offset_usd=dd_lock_offset_usd,
            profit_target=profit_target,
            min_trading_days=min_trading_days,
            inactivity_limit=inactivity_limit,
            consistency_frac=consistency_frac,
        )
        equity = initial_state.current_equity
        peak = initial_state.historical_eod_peak
        trade_days = initial_state.prior_trade_days
        max_dd = (peak - equity) / peak
        max_day_profit = initial_state.prior_max_day_profit

        initial_bust = _drawdown_outcome(
            equity,
            peak,
            starting_equity=starting_equity,
            dd_type=dd_type,
            static_dd_pct=static_dd_pct,
            trailing_dd_pct=trailing_dd_pct,
            dd_lock_offset_usd=dd_lock_offset_usd,
        )
        if initial_bust is not None:
            raise ValueError(
                f"initial_state is already at or beyond its drawdown floor ({initial_bust})"
            )
        if _has_passed(
            equity,
            trade_days,
            max_day_profit,
            starting_equity=starting_equity,
            profit_target=profit_target,
            min_trading_days=min_trading_days,
            consistency_frac=consistency_frac,
        ):
            return "pass", 0, max_dd, None

    consecutive_idle = 0

    for day in range(horizon):
        dd_from_peak = (equity - peak) / peak if peak > 0 else 0.0
        scale = dd_scale if round(dd_from_peak, 6) <= -dd_trigger else 1.0
        strategy_pnls = path[day] * scale
        pnl = float(strategy_pnls.sum())
        equity_new = equity + pnl

        dd_new = (peak - equity_new) / peak if peak > 0 else 0.0
        if dd_new > max_dd:
            max_dd = dd_new

        # The equity the BARRIER sees. When no intraday series is supplied this is
        # `equity_new` itself (identity, not an equal recomputation), so the legacy
        # arithmetic below is untouched.
        if intraday_low is None:
            equity_test = equity_new
        else:
            equity_test = min(equity_new, equity + float(intraday_low[day]) * scale)

        if (
            daily_loss_pct is not None
            and round(pnl / starting_equity, 6) <= daily_loss_pct
        ):
            return "bust_daily", day + 1, max_dd, int(np.argmin(strategy_pnls))
        drawdown_outcome = _drawdown_outcome(
            equity_test,
            peak,
            starting_equity=starting_equity,
            dd_type=dd_type,
            static_dd_pct=static_dd_pct,
            trailing_dd_pct=trailing_dd_pct,
            dd_lock_offset_usd=dd_lock_offset_usd,
        )
        if drawdown_outcome is not None:
            return drawdown_outcome, day + 1, max_dd, int(np.argmin(strategy_pnls))

        had_activity = bool(np.any(strategy_pnls != 0.0))
        is_idle = not had_activity
        if is_idle:
            consecutive_idle += 1
        else:
            consecutive_idle = 0
        if consecutive_idle >= inactivity_limit:
            return "bust_inactivity", day + 1, max_dd, None

        equity = equity_new
        if equity > peak:
            peak = equity
        if had_activity:
            trade_days += 1
        if pnl > max_day_profit:
            max_day_profit = pnl

        if _has_passed(
            equity,
            trade_days,
            max_day_profit,
            starting_equity=starting_equity,
            profit_target=profit_target,
            min_trading_days=min_trading_days,
            consistency_frac=consistency_frac,
        ):
            return "pass", day + 1, max_dd, None

    return "horizon_cap", horizon, max_dd, None


def run_seed(
    seed: int,
    n_sims: int,
    blocks: np.ndarray,
    dd_trigger: float,
    dd_scale: float,
    horizon: int = HORIZON_CAP,
    strats: Tuple[str, ...] = DEFAULT_STRATS,
    *,
    firm_kwargs: dict | None = None,
    intraday_blocks: np.ndarray | None = None,
    initial_state: EvaluationState | None = None,
) -> dict:
    """Run deterministic block-bootstrap simulations for one RNG seed.

    ``intraday_blocks`` (OPTIONAL) — week-blocks of per-day equity excursions
    paired to ``blocks`` by index. Drawn with the **same** block indices as the
    P&L path (never re-sampled independently). Shape ``(n_weeks, 5, 1)`` or
    ``(n_weeks, 5)``; assembled into a 1-D ``intraday_low`` for ``simulate_path``.
    ``None`` preserves legacy close-only behaviour byte-for-byte.
    """
    rng = np.random.default_rng(seed)
    n_blocks = len(blocks)
    blocks_per_sim = (horizon + 4) // 5
    effective_firm_kwargs = firm_kwargs or {}
    if "intraday_low" in effective_firm_kwargs:
        raise ValueError(
            "intraday_low belongs on the path (intraday_blocks=...), not in firm_kwargs"
        )
    if "initial_state" in effective_firm_kwargs:
        raise ValueError(
            "initial_state is a path starting point, not a firm rule; pass it separately"
        )
    if initial_state is not None:
        _validate_initial_state_configuration(
            initial_state,
            dd_trigger=dd_trigger,
            dd_scale=dd_scale,
            horizon=horizon,
            starting_equity=effective_firm_kwargs.get("starting_equity", STARTING_EQUITY),
            daily_loss_pct=effective_firm_kwargs.get("daily_loss_pct", DAILY_LOSS_PCT),
            dd_type=effective_firm_kwargs.get("dd_type", "static"),
            static_dd_pct=effective_firm_kwargs.get("static_dd_pct", STATIC_DD_PCT),
            trailing_dd_pct=effective_firm_kwargs.get("trailing_dd_pct"),
            dd_lock_offset_usd=effective_firm_kwargs.get("dd_lock_offset_usd"),
            profit_target=effective_firm_kwargs.get("profit_target", PROFIT_TARGET),
            min_trading_days=effective_firm_kwargs.get(
                "min_trading_days", MIN_TRADING_DAYS
            ),
            inactivity_limit=effective_firm_kwargs.get(
                "inactivity_limit", INACTIVITY_LIMIT
            ),
            consistency_frac=effective_firm_kwargs.get("consistency_frac"),
        )
    if intraday_blocks is not None:
        intraday_blocks = np.asarray(intraday_blocks)
        if len(intraday_blocks) != n_blocks:
            raise ValueError(
                f"intraday_blocks length {len(intraday_blocks)} != blocks length {n_blocks}"
            )

    outcomes = {
        "pass": 0,
        "bust_daily": 0,
        "bust_static": 0,
        "bust_trailing": 0,
        "bust_inactivity": 0,
        "horizon_cap": 0,
    }
    days_to_pass: list[int] = []
    max_dds: list[float] = []
    bust_attribution = {strategy: 0 for strategy in strats}

    for _ in range(n_sims):
        indices = rng.integers(0, n_blocks, blocks_per_sim)
        path = np.concatenate([blocks[index] for index in indices])[:horizon]
        sim_kwargs = dict(effective_firm_kwargs)
        if intraday_blocks is not None:
            low_blocks = [intraday_blocks[index] for index in indices]
            low = np.concatenate(
                [np.asarray(b, dtype=float).reshape(-1) for b in low_blocks]
            )[:horizon]
            sim_kwargs["intraday_low"] = low
        outcome, day, max_dd, culprit = simulate_path(
            path,
            dd_trigger,
            dd_scale,
            horizon,
            initial_state=initial_state,
            **sim_kwargs,
        )
        outcomes[outcome] += 1
        max_dds.append(max_dd)
        if outcome == "pass":
            days_to_pass.append(day)
        elif (
            outcome in ("bust_daily", "bust_static", "bust_trailing")
            and culprit is not None
        ):
            bust_attribution[strats[culprit]] += 1

    return {
        "outcomes": outcomes,
        "days_to_pass": days_to_pass,
        "max_dds": max_dds,
        "bust_attribution": bust_attribution,
    }


def _validate_historical_fixture() -> None:
    """HISTORICAL_CHALLENGE_FIRM_KWARGS must exactly mirror simulate_path's
    firm keyword defaults -- total, with identical values.

    Guards the two drift modes that would otherwise be silent:
      (a) a keyword-only param added to simulate_path but not to the fixture,
          so callers passing the fixture silently inherit a def-time default;
      (b) a value drifting between the two, so "explicit" callers and default
          callers stop agreeing.

    Both are invisible today (the defaults ARE the fixture) and become
    undetectable in Phase 4 when those defaults are removed. Runs at import,
    matching this repo's existing MVD self-check convention.
    """
    import inspect

    params = inspect.signature(simulate_path).parameters
    firm_keys = {
        name
        for name, p in params.items()
        if p.kind is inspect.Parameter.KEYWORD_ONLY
        and name not in _NON_FIRM_KEYWORDS
    }
    fixture_keys = set(HISTORICAL_CHALLENGE_FIRM_KWARGS)

    missing = firm_keys - fixture_keys
    extra = fixture_keys - firm_keys
    if missing or extra:
        raise AssertionError(
            "HISTORICAL_CHALLENGE_FIRM_KWARGS is not total over simulate_path's "
            f"firm keyword surface: missing={sorted(missing)} extra={sorted(extra)}"
        )

    for key in sorted(firm_keys):
        expected = params[key].default
        actual = HISTORICAL_CHALLENGE_FIRM_KWARGS[key]
        if actual != expected or type(actual) is not type(expected):
            raise AssertionError(
                f"HISTORICAL_CHALLENGE_FIRM_KWARGS[{key!r}]={actual!r} "
                f"({type(actual).__name__}) != simulate_path default "
                f"{expected!r} ({type(expected).__name__})"
            )


_validate_historical_fixture()
