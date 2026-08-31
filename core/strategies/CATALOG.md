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
| striker_dj30_v4.5_mnq_qtxg1 | striker | PARKED_PROTOTYPE | Q-TXG-1 sibling-swap: DJ30 v4.5 → MNQ research port (not F1 redeploy) | core/strategies/striker/striker_dj30_v4.5_mnq_qtxg1_CARD.md | core/strategies/_archive/striker/ |
| aegis_jpy_futures_v0_3 | aegis | PARKED_PROTOTYPE | Aegis 6J futures prototypes (base + bepad); research only | core/strategies/aegis/aegis_jpy_futures_v0_3_CARD.md | core/strategies/_archive/aegis/ |
| orb_mnq | orb | FALSIFIED_PARKED | ORB-MNQ-1 v0.1/v0.2 (+ CANDIDATE docs); payability target falsified | core/strategies/orb/orb_mnq_CARD.md | core/strategies/_archive/orb/ |
| candidates | candidates | PARKED_PROTOTYPE | Phase A cold-store body FALSIFIED_PARKED; MSL-S4 `expiry-oi-strike-convergence` (MGC) live, G0 FROZEN, not yet hash-pinned (see card) ⚠ Correction 2026-08-23: `PARKED` 2026-08-21 (AMBIGUOUS-HOLD), hash-pinned 2026-08-23 — see card | core/strategies/candidates/candidates_CARD.md | core/strategies/_archive/candidates/ |
