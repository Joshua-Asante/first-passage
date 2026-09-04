# Strategy catalog

Open this file first for strategy dispositions under `core/strategies/`.
Hot stubs are `*_CARD.md` beside each family; cold bodies live under
`core/strategies/_archive/<family>/`.

Disposition ≠ lifecycle authorization — see
[`docs/methodology/strategy_lifecycle.md`](../../docs/methodology/strategy_lifecycle.md)
and ADR 2026-08-04 (Tradeify de-scope).

| Disposition | Meaning |
|---|---|
| `VENUE_LESS_CFD` | Locked CFD edition; no live venue |
| `VENUE_WITHDRAWN` | Futures edition withdrawn from Tradeify; F3-retainable |
| `PARKED_PROTOTYPE` | Research prototype; not locked live |
| `FALSIFIED_PARKED` | Candidate/falsified research; not live |

## Locked parameter record (CFD-era book)

Human-readable mirror of the locked book, moved here from `CLAUDE.md` §Strategy Reference on
2026-09-04 (root-doc charter: root docs carry pointers, owners carry records —
[`docs/operational_rules.md`](../../docs/operational_rules.md) §7).

**No live venue.** These four strategies are a historical record of the locked CFD book and its
withdrawn futures editions, not a live book. Live sizing authority is
`dd_protection.BASE_RISK` / `firm_rules._BASE_RISK` (both derived from
[`historical_challenge.py`](../historical_challenge.py)`.HISTORICAL_CHALLENGE_BASE_RISK`) — never
this table. The two Striker futures editions (MYM/MNQ) *were* the c1 book until 2026-08-04; that
code path is deliberately untouched (`ops/c1_rail/c1_sizing_host_reference.py` still consumes
`BASE_RISK["Striker"]` / `["Striker NAS100"]` via `LEG_MAP`).

| Strategy | Instrument / TF | Risk/trade | Version | DXTrade contractValue |
|---|---|---|---|---|
| Striker DJ30 | DJ30 15m | **0.70%** (pyramid 750%) | v4.5 LOCKED | **10** (critical — default 1 ⇒ ~7% risk) |
| Striker NAS100 | NAS100 15m | **0.37%** (pyramid 1000%) | v1 LOCKED | 10 |

Guardian Gold / Aegis USDJPY are **historical CFD book**, not living `BASE_RISK` — frozen risk% in
`historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK`; Pine + LOCK bodies under `_archive/`
([Phase C](../../docs/adr/2026-08-23-strategy-coldstore-phase-c.md)).

Risk% and pyramid are mirrored here from `firm_rules.py` / Pine as the human-readable record; every
other strategy parameter (SL/TP/ATR/session/BE/trail) lives in **Pine only** and is never duplicated
in markdown. The `contractValue=10` requirement is owned by
[`docs/operational_rules.md`](../../docs/operational_rules.md) Rule 3 (dormant — DXTrade is retired).
Lock lineage: [allocation refresh 2](../../docs/adr/2026-05-23-allocation-refresh-2.md).

## Registry

| Slug | Family | Disposition | One-liner | Card | Body |
|---|---|---|---|---|---|
| guardian_gold_v5.5 | guardian | VENUE_LESS_CFD | Locked XAUUSD 15m CFD edition (+ indicator); no live venue | core/strategies/guardian/guardian_gold_v5.5_CARD.md | core/strategies/_archive/guardian/ |
| aegis_usdjpy_v4.3 | aegis | VENUE_LESS_CFD | Locked USDJPY 15m CFD edition (+ indicator); no live venue | core/strategies/aegis/aegis_usdjpy_v4.3_CARD.md | core/strategies/_archive/aegis/ |
| striker_dj30_v4.5 | striker | VENUE_LESS_CFD | Locked DJ30 15m CFD edition (+ indicator); no live venue | core/strategies/striker/striker_dj30_v4.5_CARD.md | core/strategies/_archive/striker/ |
| striker_nas100_v1 | nas | VENUE_LESS_CFD | Locked NAS100 15m CFD edition (+ indicator); no live venue | core/strategies/nas/striker_nas100_v1_CARD.md | core/strategies/_archive/nas/ |
| striker_dj30_v4.5_mym | striker | VENUE_WITHDRAWN | MYM futures venue edition (+ FUTURES_LOCK); Tradeify withdrawn, F3-retainable | core/strategies/striker/striker_dj30_v4.5_mym_CARD.md | core/strategies/_archive/striker/ |
| striker_nas100_v1_mnq | nas | VENUE_WITHDRAWN | MNQ futures venue edition (+ FUTURES_LOCK); Tradeify withdrawn, F3-retainable | core/strategies/nas/striker_nas100_v1_mnq_CARD.md | core/strategies/_archive/nas/ |
| striker_nas100_v1_mym_qtxg1 | nas | PARKED_PROTOTYPE | Q-TXG-1 sibling-swap: NAS100 v1 → MYM research port (not F1 redeploy) | core/strategies/nas/striker_nas100_v1_mym_qtxg1_CARD.md | core/strategies/_archive/nas/ |
| striker_dj30_v4.5_mnq_qtxg1 | striker | FALSIFIED_PARKED | Q-TXG-1 sibling-swap: DJ30 v4.5 → MNQ research port (not F1 redeploy); Block 4 scored this cell `DEAD(N-SURV)` 2026-08-12, lane closed `FALSIFIED-at-walls` same day (see card) | core/strategies/striker/striker_dj30_v4.5_mnq_qtxg1_CARD.md | core/strategies/_archive/striker/ |
| aegis_jpy_futures_v0_3 | aegis | PARKED_PROTOTYPE | Aegis 6J futures prototypes (base + bepad); research only | core/strategies/aegis/aegis_jpy_futures_v0_3_CARD.md | core/strategies/_archive/aegis/ |
| orb_mnq | orb | FALSIFIED_PARKED | ORB-MNQ-1 v0.1/v0.2 (+ CANDIDATE docs); payability target falsified | core/strategies/orb/orb_mnq_CARD.md | core/strategies/_archive/orb/ |
| candidates | candidates | PARKED_PROTOTYPE | Phase A cold-store body FALSIFIED_PARKED; MSL-S4 `expiry-oi-strike-convergence` (MGC) live, G0 FROZEN, not yet hash-pinned (see card) ⚠ Correction 2026-08-23: `PARKED` 2026-08-21 (AMBIGUOUS-HOLD), hash-pinned 2026-08-23 — see card | core/strategies/candidates/candidates_CARD.md | core/strategies/_archive/candidates/ |
