#!/usr/bin/env python3
"""
DD-protection geometry — dd_protection as a CONCEPT, not a constant.
====================================================================
Registry of per-(portfolio, firm-tier) protection *instances* of the one
invariant mechanism (operator directive 2026-07-12; ratified recommendation
docs/briefs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md §3;
decision record docs/adr/2026-07-13-dd-protection-concept-not-constant.md).

The INVARIANT (never varies across firms/portfolios): when the portfolio's
remaining room to its LIVE bust floor is depleted past a fraction of the
firm's DD budget, multiply that day's sizing down; clear automatically on
recovery to reference; the factor MULTIPLIES BASE_RISK (compounds with the
lifecycle authorization haircut — it never edits any locked parameter); ULP
rounding before the threshold compare; single tier. Any instance change
requires re-MC + regime-robustness gate + a freeze record.

The VARIABLES (per instance): exactly three —
    trigger         absolute DD distance that fires the de-risk
    scale           sizing multiplier while fired
    reference_mode  which floor DD is measured against ("static" — fixed
                    dd-from-peak proxy; "trailing" — ratcheting %-of-peak
                    floor; "locking" — ratchet-then-freeze fixed-$ floor)

Registry rows are admitted only via pre-registration → re-MC → both-halves
regime gate → admitting ADR (concept ADR §4). The historical FXIFY-C2 seed
row and its import-time one-way pin were retired 2026-07-22 under
docs/adr/2026-07-22-challenge-era-substrate-retirement.md Phase 1 — the
venue-agnostic type + dd_type→reference_mode mapping remain. Locked
DD_TRIGGER/DD_SCALE live in dd_protection.py (ast.Constant RHS; validate_params
+ verify_lock_anchors require that shape). Nothing on the MC anchor import
path (portfolio_mc -> mc.modes/mc.simulation -> dd_protection / firm_rules)
imports this module.

theta* = 0.30 (FXIFY-C2's shipped trigger/budget ratio, 1.5%/5%) remains
PROVENANCE-ONLY historical context — explicitly not a validated transferable
invariant (FXIFY-C2's own Q-DDP-1 regime-robustness gate FAILED; see
dd_protection.py header). Every new instance must clear its OWN re-MC +
regime gate; it never rides FXIFY's.

Deliberately NOT here (deferred until a real pre-registered prop candidate +
the engine pre-flight exist — ratified trim, recommendation §3.4): seed-policy
heuristics, the reference_mode-gated simulate_path branch, harness swaps.
Adding a new instance row is a code edit carrying its admitting ADR — there is
no runtime registration API, so every instance is git-auditable.

This module reads dd_type ONLY from firm configs — never daily_loss_pct — so
it is immune to the `daily_loss_pct: None` import-time division hazard.
"""

from dataclasses import dataclass

REFERENCE_MODES = frozenset({"static", "trailing", "locking"})

# firm_rules dd_type -> reference_mode. Keys are the only dd_type values the
# engine implements (core/mc/simulation.py branch chain); an unknown dd_type
# is a hard error, never a silent static fallback (a prop instance de-risking
# off a static peak would misplace the trigger against a ratcheting floor).
_REFERENCE_MODE_BY_DD_TYPE = {
    "static": "static",
    "trailing": "trailing",
    "trailing_locking": "locking",
}


@dataclass(frozen=True)
class ProtectionPolicy:
    """One frozen protection instance: (reference_mode, trigger, scale) + provenance."""

    reference_mode: str
    trigger: float
    scale: float
    provenance: str

    def __post_init__(self):
        if self.reference_mode not in REFERENCE_MODES:
            raise ValueError(
                f"reference_mode must be one of {sorted(REFERENCE_MODES)}, "
                f"got {self.reference_mode!r}"
            )
        if not (0.0 < self.trigger < 1.0):
            raise ValueError(f"trigger must be a fraction in (0, 1), got {self.trigger}")
        if not (0.0 <= self.scale <= 1.0):
            raise ValueError(f"scale must be in [0, 1], got {self.scale}")


# The instance registry. Keyed by instance id ("<portfolio>@<firm-tier>").
# Empty after Phase-1 FXIFY-C2 seed retirement (ADR 2026-07-22). Each new row
# lands ONLY with: a dated re-MC at that (portfolio, firm-tier), a passed
# regime-robustness gate, and an admitting ADR named in `provenance` — see the
# concept ADR §4. Never invent a silent default instance.
POLICY_REGISTRY: dict[str, ProtectionPolicy] = {}


def protection_policy(instance_key: str) -> ProtectionPolicy:
    """Resolve a registered protection instance. Side-effect-free.

    Raises KeyError with the registered keys listed — an unregistered
    (portfolio, firm-tier) has NO protection instance and must not invent a
    default (transplanting a foreign DD geometry is exactly what the concept
    ADR forbids).
    """
    try:
        return POLICY_REGISTRY[instance_key]
    except KeyError:
        raise KeyError(
            f"No protection instance registered for {instance_key!r}. "
            f"Registered: {sorted(POLICY_REGISTRY)}. New instances require a "
            f"dated re-MC + regime gate + admitting ADR (concept ADR §4) — "
            f"never invent a default instance."
        ) from None


def reference_mode_for_dd_type(dd_type: str) -> str:
    """Map a firm_rules dd_type to the de-risk reference geometry.

    Reads dd_type ONLY (never daily_loss_pct — None-hazard immune). Unknown
    dd_type raises: the engine has no branch for it, so no reference geometry
    can be correct.
    """
    try:
        return _REFERENCE_MODE_BY_DD_TYPE[dd_type]
    except KeyError:
        raise KeyError(
            f"Unknown dd_type {dd_type!r}; engine-implemented types: "
            f"{sorted(_REFERENCE_MODE_BY_DD_TYPE)}"
        ) from None
