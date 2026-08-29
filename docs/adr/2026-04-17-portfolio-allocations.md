# ADR: Portfolio allocations — G 0.30 / S 1.00 / A 1.50

⚠ **The title's G 0.30 / S 1.00 / A 1.50 figures are SUPERSEDED — see Addendum 2026-08-29.** Live
Striker allocation is **0.70%** (single DJ30 leg; NAS100 is a separate 0.37% line), and Aegis is
**not live** at all (historical CFD book, no `_BASE_RISK` entry). Source of truth:
`core/firm_rules.py` / `core/historical_challenge.py`.

**Date:** 2026-04-17
**Status:** Accepted - allocations superseded by later refreshes; see Addendum 2026-08-29 for current figures.
**Decision date:** 2026-04-17
**Supersedes:** none
**Superseded-by:** none
**Retain-until:** none
**Superseded-in-part-by:** `2026-04-23-guardian-risk-relock-0.34.md` - Guardian allocation only (0.30% to 0.34%).
**Scope:** `firm_rules.py`, portfolio risk allocation

## Context

Prior portfolio allocations (G 0.30% / S 0.70% / A 0.75%) produced a 4yr net in the $200K+ range with acceptable MC pass rate, but risk budget was under-utilized. Striker and Aegis both had spare room under the FXIFY 5% daily DD cap that their per-strategy recovery factors justified filling.

Allocations needed to optimize net P&L across the 150-day challenge horizon subject to:
- FXIFY rules: 5% profit target, 5% daily loss, 5% static DD
- Portfolio-level bust rate constraint (target <5%)
- No strategy allocated above its own recovery-factor-implied ceiling

## Decision

Allocations finalized at Guardian 0.30% / Striker 1.00% / Aegis 1.50% per trade.

Allocation method: per-strategy recovery factor optimization. Each strategy's risk allocation is proportional to its recovery factor relative to the portfolio-level bust constraint.

## Alternatives considered

- **Prior allocations (0.30 / 0.70 / 0.75).** Validated but suboptimal. Under-uses risk budget on Striker and Aegis.
- **Equal-risk (0.75 / 0.75 / 0.75).** Rejected — ignores per-strategy recovery factor differences. Guardian's RF 22.04 vs Striker's 18.43 vs Aegis (highest μ/σ 1.63) argue for differential allocation, not flat.
- **Aggressive (G 0.50 / S 1.20 / A 2.00).** Rejected — MC bust rate exceeded 5% threshold. Aegis at 2.0% becomes the dominant bust driver past the tolerable range.

## Consequences

Positive:
- 4yr scaled net P&L lifts materially vs prior allocations.
- Recovery factor ordering (Guardian > Striker > Aegis when normalized) respected.
- Under single-tier DD 1.0%/0.40×, MC produces bust 1.55% / pass 93.00% / p99 DD ~4.9%.

Negative:
- Aegis at 1.50% is the dominant bust driver (~47% of bust attribution). This is an artifact of correct sizing toward highest-μ/σ strategy, not a miscalibration, but it means tail events in USDJPY mean-reversion drive portfolio outcomes more than either of the other two strategies.

Risks:
- BOJ April 28, 2026 meeting is a binary vol event that could shift USDJPY regime away from Aegis's edge window. If regime shift is confirmed post-meeting, allocation may need downward adjustment. Monitor, do not preemptively cut.
- ~~Guardian funded ramp (0.30 → 0.40 at $210K, 0.50 at $220K, 0.55 at $225K) changes the allocation profile as challenge clears. Each ramp step requires portfolio MC rerun before activation.~~ (Superseded same day, 2026-04-17, by the unified-allocation decision: challenge phase = funded phase, no re-sizing at pass. See `firm_rules.py` `RISK_TIERS` and `CLAUDE.md` Multiplier System.)

## Cross-references

- Notion: [dd_protection retune to 1.5%/0.40× — 2026-04-17](https://www.notion.so/346dc0b53c118124811bee0d77c1b1e1) (captures allocation rationale)
- Code: `firm_rules.py`
- Related: ADR 2026-04-17-dd-trigger-calibration, ADR 2026-04-17-equity-tier-deletion

## Addendum 2026-08-29 — discharge (DECAYED_UNDOCUMENTED, adr-decay-audit precursor run)

The 2026-08-23 `adr-decay-audit` precursor run (`docs/adr/2026-08-23-adr-decay-audit-skill-ratification.md`
§1) flagged this ADR's Status line as `DECAYED_UNDOCUMENTED` — current reality has moved on with no
discharge recorded. This addendum is that discharge; the Context/Decision/Consequences above stay
byte-unedited as the historical record (Rule 14).

**Current state, verified against production (`core/firm_rules.py`, `core/historical_challenge.py`):**

- `_LIVE_BASE_RISK_SLUGS = ("striker", "striker_nas100")` — only the two Striker legs are live.
  Guardian and Aegis carry no entry in the live `_BASE_RISK` dict at all.
- Live Striker (DJ30) allocation is **0.70%**, not the 1.00% this ADR names — moved via the
  2026-05-14 allocation refresh this ADR's own §Cross-references already points at, then again via
  a later refresh (see `CLAUDE.md` Strategy Reference table for the current figure and lock version).
- Striker NAS100 (added 2026-05-07, after this ADR) is a separate **0.37%** line, not part of this
  ADR's original scope at all.
- Aegis (1.50% here) is **not live** — historical CFD book only
  (`core/historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK["aegis"] = 0.0150`, frozen record, no
  live venue). See CLAUDE.md §Strategy Reference and Phase C
  (`docs/adr/2026-08-23-strategy-coldstore-phase-c.md`).
- Guardian (0.30% here) is likewise historical-only, since re-locked to 0.34% the same day by
  `2026-04-23-guardian-risk-relock-0.34.md` (already correctly linked above as
  Superseded-in-part-by) and now cold-stored under the same Phase C.

`docs/adr/INDEX.md`'s mirror of this Status line is corrected in the same commit as this addendum
(it is a living pointer document, corrected in place per Rule 14, not a frozen artifact).
