"""Tier-demotion state writer — calls autonomous_demote; writes tier only."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

try:
    from lifecycle import (
        DEFAULT_TIER,
        STATE_FILE,
        STRATEGY_KEYS,
        TIER_MULTIPLIER,
        autonomous_demote,
        load_lifecycle_state,
    )
except ImportError:  # pragma: no cover
    from core.lifecycle import (
        DEFAULT_TIER,
        STATE_FILE,
        STRATEGY_KEYS,
        TIER_MULTIPLIER,
        autonomous_demote,
        load_lifecycle_state,
    )


@dataclass(frozen=True)
class DemotionResult:
    strategy: str
    tier_before: str
    tier_after: str
    demoted: bool
    state_file: str
    state_delta: dict[str, str]


def _current_tier(state: dict, strategy: str) -> str:
    return state.get(strategy, DEFAULT_TIER)


def write_lifecycle_state(state: dict[str, str], path: Path) -> None:
    """Write exactly ``{strategy: tier}`` and round-trip via load_lifecycle_state.

    Does **not** apply any multiplier — the haircut lives in dd_protection.
    """
    unknown = set(state) - set(STRATEGY_KEYS)
    if unknown:
        raise ValueError(f"Unknown lifecycle strategies: {sorted(unknown)}")
    # Schema: strategy -> tier string only.
    payload = {k: str(v) for k, v in sorted(state.items())}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_confirmed_demotion(
    strategy: str,
    *,
    state_file: Path | None = None,
) -> DemotionResult:
    """On a confirmed 2nd consecutive breach: step tier via autonomous_demote.

    WATCH-2 is the autonomous floor (never auto-RETIRE). Writes only the tier
    string into ``lifecycle_state.json``'s ``{strategy: tier}`` schema.
    """
    if strategy not in STRATEGY_KEYS:
        raise ValueError(f"Unknown strategy {strategy!r}; valid: {sorted(STRATEGY_KEYS)}")

    dest = Path(state_file) if state_file is not None else Path(STATE_FILE)

    # load_lifecycle_state always reads STATE_FILE; for a test seam we read the
    # same schema ourselves when dest differs, then still validate via a write
    # + temporary swap only when dest == STATE_FILE. Prefer: read dest directly
    # with the same validation rules.
    if dest == Path(STATE_FILE) and dest.exists():
        before_state = load_lifecycle_state()
    elif dest.exists():
        raw = json.loads(dest.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("Lifecycle state must be a JSON object")
        unknown = set(raw) - set(STRATEGY_KEYS)
        if unknown:
            raise ValueError(f"Unknown lifecycle strategies: {sorted(unknown)}")
        before_state = {str(k): str(v) for k, v in raw.items()}
    else:
        before_state = {}

    tier_before = _current_tier(before_state, strategy)
    tier_after = autonomous_demote(tier_before)
    demoted = tier_after != tier_before

    after_state = dict(before_state)
    after_state[strategy] = tier_after
    write_lifecycle_state(after_state, dest)

    # Round-trip validation through core.lifecycle when writing the live path.
    if dest == Path(STATE_FILE):
        reloaded = load_lifecycle_state()
        if reloaded.get(strategy) != tier_after:
            raise ValueError(
                f"round-trip failed: wrote {tier_after!r} for {strategy!r}, "
                f"load_lifecycle_state returned {reloaded.get(strategy)!r}"
            )
    else:
        # Alternate path (tests): validate schema shape matches what the loader
        # would accept.
        raw = json.loads(dest.read_text(encoding="utf-8"))
        if set(raw) - set(STRATEGY_KEYS):
            raise ValueError("written state has unknown keys")
        invalid = {k: t for k, t in raw.items() if t not in TIER_MULTIPLIER}
        if invalid:
            raise ValueError(f"Invalid lifecycle tiers: {invalid}")

    delta = {strategy: tier_after} if demoted else {}
    return DemotionResult(
        strategy=strategy,
        tier_before=tier_before,
        tier_after=tier_after,
        demoted=demoted,
        state_file=str(dest),
        state_delta=delta,
    )
