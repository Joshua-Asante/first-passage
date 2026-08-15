# Envelope reconcile — Track C / Q-HARV-0 Wave 0

**Date:** 2026-07-11  
**Source envelope:** `ops/prop_envelope_default.md` (PROVISIONAL v0.1)  
**Repo scan:** `core/firm_rules.py` + futures-prop / conversion / remc docs under `docs/` and `lab/analysis/`  
**Posture note:** The closed CFD challenge venue and the futures-prop NO-GO mean every `FIRM_RULES` entry is a **historical fixture** (provenance / re-open material), not a live deploy target. Contradictions below are fixture-vs-envelope mismatches useful for envelope ratification and deployable-expression design — they do **not** imply a live firm is misconfigured.

Firm-specific names are omitted from this artifact (envelope §2.4). Config families are labeled by rule geometry only.

---

## Contradiction list

| # | Envelope rule | Repo fact | Severity | Notes |
|---|---|---|---|---|
| C1 | **E1** — build target flat by **16:00 ET** (strict end of observed ~15:59–16:59 ET band) | Futures-prop MC / force-flat harnesses truncate at **17:00 ET** (≈15:59 CT primary print; 15m-bar fill via last ≤16:45 bar). One Select-style comment pins rail force-flat at **16:59 ET**. A MYM prototype edition used a **16:30 ET** bar. | **High** (clock-print drift) | Intent (no overnight / no weekend) aligns; the **deadline print does not**. Envelope 16:00 ET is stricter than the 17:00 ET modeling convention. Envelope §5 already flags this as an open ratification item. |
| C2 | **E1** — no overnight / weekend holds | Historical CFD fixture (`ACTIVE_FIRM`): `weekend_holds: True` | **Medium** (fixture class mismatch) | Expected: CFD challenge semantics ≠ futures-prop envelope. Retained only as MC-anchor fixture. Do not read as envelope-aligned. |
| C3 | **E3** — trailing DD measured **intraday on unrealized equity** (strict) | Select Flex–class configs: `dd_type="trailing_locking"` — floor ratchets on **EOD balance only** (never intraday, never down), then locks. Explicitly the **looser** EOD variant the envelope text contrasts against. | **High** (barrier geometry) | Envelope default is the strict build target; this family is a §4 overlay unlock (EOD trail), not a default match. Designing only to EOD-trail understates excursion risk if a deployment fork lands on an intraday-trail firm. |
| C4 | **E3** — intraday unrealized trail | Option-1–class configs claim **real-time** trailing; engine `bust_trailing` path historically modeled as **EOD %-of-peak** in remc docs | **Medium** (model vs primary-source claim) | Config *intent* matches E3; simulation semantic may be looser than the strict envelope unless fixed-dollar / intraday path is confirmed at deploy. Historical fixture under NO-GO. |
| C5 | **E4** — daily loss limit **present by default** | All futures-prop tiers: `daily_loss_pct: None`. Only the historical CFD fixture sets a numeric daily loss (5%). | **Low** (expected overlay divergence) | Envelope §1 already states not all firms impose a daily LL. Fixtures correctly encode absence. Residual: candidates built *only* to “no daily LL” overlays are not default-envelope-complete. |

**Contradiction count: 5** (C1–C5). Of these, **2 are High** (C1 clock print, C3 EOD-vs-intraday trail).

---

## Non-contradictions (aligned or N/A)

| Rule | Verdict | Evidence |
|---|---|---|
| **E1** force-flat *intent* (futures-prop fixtures) | **Aligned** | All futures-prop tiers: `weekend_holds: False`; remc / hold-compat work assumes daily flat, no overnight/weekend carry. |
| **E2** 40% consistency | **Aligned** | Envelope 40% matches Select Flex–class comments (`min_trading_days: 3` forced by 40% eval) and remc `consistency_frac=0.40` arms; Option-1 Master payout formula pinned at best-day ≤40% of cumulative profit (payout-gated, not bust-gated). Not a `FIRM_RULES` key — modeled in harnesses only. |
| **E3** Option-1 real-time trail *intent* | **Aligned** (with C4 caveat) | `dd_type="trailing"` + comments: real-time trailing, no daily LL — matches envelope’s strict *type*, level remains tier-parameter. |
| **E5** micro sizing & caps | **Aligned** | Futures-prop tiers carry `micro_contract_cap` (and where present `cost_per_side_usd`); integer-micro / RESERVE discipline is the standing futures path. |
| **E6** attended automation | **Aligned / dormant** | Envelope assumes attended automation on TV→CrossTrade→NT8. Repo posture: that rail is the named target and is **not built** under futures-prop NO-GO — dormant, not contradictory. No design claim of unattended 24h operation in the envelope path. |
| **E7** news = overlay-only | **Aligned** | Envelope correctly keeps news out of the default. Futures-prop configs have no news-restriction field. Historical CFD fixture sets `news_trading: True` (permitted), which is an overlay fact, not a default constraint. |
| Live prop book | **N/A** | Zero prop accounts; CFD venue closed; futures-prop NO-GO. Envelope is a *research build target* for a possible future fork, not a live compliance matrix. |

---

## Summary for Wave 0

- **Top issues:** (1) E3 default = intraday unrealized trail, but a major configured family is EOD-locking — treat as overlay, never as default. (2) E1 default print 16:00 ET vs repo’s 17:00 ET / ~16:59 ET operational prints — ratify one build-target clock before deployable-expression cost hurdles. (3) E4 “present by default” is stricter than all futures-prop fixtures (`None`) — keep as conservative design tax, not a fixture bug.
- **Safe to treat as shared:** E2 @ 40%, E5 micros, E6 attended (dormant rail), E7 overlay-only, E1 no-overnight *intent* on futures-prop fixtures.
- **Do not** use `ACTIVE_FIRM` / CFD challenge semantics as envelope ground truth.
