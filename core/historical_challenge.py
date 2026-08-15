"""Frozen historical FXIFY $200K challenge fixture (substrate Phase 4).

Not a ``FIRM_RULES`` row and not a live firm selector. Living firm selection
is always an explicit ``FIRM_RULES`` key (Tradeify / MFFU / Bulenox / BluSky).

These literals preserve engine-regression byte-identity for the retired
FXIFY-shaped challenge semantics (static 5% / daily 5% / target 5% /
60 idle days / $200K basis) after ``FIRM_RULES["FXIFY"]`` and
``BASELINE_BALANCE`` were deleted. Opt in via
``HISTORICAL_CHALLENGE_FIRM_KWARGS`` / ``HISTORICAL_CHALLENGE_BASIS`` —
never via an import-time firm switch.

Provenance: ``docs/adr/2026-07-22-challenge-era-substrate-retirement.md``
§2-E / Phase 4; earlier pin lived at ``FIRM_RULES["FXIFY"]`` (Phase 1).
"""

from __future__ import annotations

# Account basis — retired continuous-lot $200K challenge size.
HISTORICAL_CHALLENGE_BALANCE: float = 200_000.0

# Rule percentages as published on the closed FXIFY challenge (unsigned %).
_PROFIT_TARGET_PCT: float = 5.0
_DAILY_LOSS_PCT: float = 5.0
_MAX_DD_PCT: float = 5.0
_MIN_TRADING_DAYS: int = 5
_INACTIVITY_MAX_IDLE_DAYS: int = 60

# Absolute / signed forms consumed by MC + dd_protection challenge CLI.
STARTING_EQUITY: float = HISTORICAL_CHALLENGE_BALANCE
PROFIT_TARGET_ABS: float = HISTORICAL_CHALLENGE_BALANCE * (
    1 + _PROFIT_TARGET_PCT / 100
)  # 210_000
PROFIT_TARGET_FRAC: float = _PROFIT_TARGET_PCT / 100  # 0.05 (dd_protection)
DAILY_LOSS_PCT_SIGNED: float = -_DAILY_LOSS_PCT / 100  # -0.05 (simulate_path)
DAILY_LOSS_LIMIT_FRAC: float = _DAILY_LOSS_PCT / 100  # 0.05 (dd_protection)
STATIC_DD_PCT_SIGNED: float = -_MAX_DD_PCT / 100  # -0.05
STATIC_DD_LIMIT_FRAC: float = _MAX_DD_PCT / 100  # 0.05
MIN_TRADING_DAYS: int = _MIN_TRADING_DAYS
INACTIVITY_LIMIT: int = _INACTIVITY_MAX_IDLE_DAYS

# TOTAL over simulate_path's firm keyword surface (see core/mc/simulation.py).
HISTORICAL_CHALLENGE_FIRM_KWARGS: dict = {
    "starting_equity": STARTING_EQUITY,
    "daily_loss_pct": DAILY_LOSS_PCT_SIGNED,
    "dd_type": "static",
    "static_dd_pct": STATIC_DD_PCT_SIGNED,
    "trailing_dd_pct": None,
    "dd_lock_offset_usd": None,
    "profit_target": PROFIT_TARGET_ABS,
    "min_trading_days": MIN_TRADING_DAYS,
    "inactivity_limit": INACTIVITY_LIMIT,
    "consistency_frac": None,
}

HISTORICAL_CHALLENGE_BASIS: float = STARTING_EQUITY
