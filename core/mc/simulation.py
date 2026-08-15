"""Deterministic path and seeded bootstrap simulation for portfolio MC."""

from __future__ import annotations

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
_NON_FIRM_KEYWORDS: frozenset[str] = frozenset({"intraday_low"})


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
    equity = peak = float(starting_equity)
    trade_days = 0
    consecutive_idle = 0
    max_dd = 0.0
    max_day_profit = 0.0

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
        if dd_type == "trailing":
            if (
                trailing_dd_pct is not None
                and round((equity_test - peak) / peak, 6) <= trailing_dd_pct
            ):
                return (
                    "bust_trailing",
                    day + 1,
                    max_dd,
                    int(np.argmin(strategy_pnls)),
                )
        elif dd_type == "trailing_locking":
            if trailing_dd_pct is not None and dd_lock_offset_usd is not None:
                max_dd_usd = -trailing_dd_pct * starting_equity
                floor = min(
                    peak - max_dd_usd, starting_equity + dd_lock_offset_usd
                )
                if round((equity_test - floor) / starting_equity, 6) <= 0.0:
                    return (
                        "bust_trailing",
                        day + 1,
                        max_dd,
                        int(np.argmin(strategy_pnls)),
                    )
        elif (
            round((equity_test - starting_equity) / starting_equity, 6)
            <= static_dd_pct
        ):
            return "bust_static", day + 1, max_dd, int(np.argmin(strategy_pnls))

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

        if round(equity, 2) >= profit_target and trade_days >= min_trading_days:
            if consistency_frac is None:
                return "pass", day + 1, max_dd, None
            total_profit = equity - starting_equity
            if (
                total_profit <= 0.0
                or round(max_day_profit - consistency_frac * total_profit, 2) <= 0.0
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
            path, dd_trigger, dd_scale, horizon, **sim_kwargs
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
