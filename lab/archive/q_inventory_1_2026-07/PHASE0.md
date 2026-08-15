# Q-INVENTORY-1 Phase 0 — dedup + bank re-read

**Date:** 2026-07-17
**Parent brief:** [`docs/briefs/Q-INVENTORY-1-zero-survivor-replenishment-disposition.md`](lab/archive/../../docs/briefs/Q-INVENTORY-1-zero-survivor-replenishment-disposition.md) §7 Phase 0
**Pre-registration:** [`Q-INVENTORY-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-INVENTORY-1-verdict-preregistration.md) (FROZEN this session, before Phase 1)

## K-banks (re-read from `discovery_manifests/*.json`, not the §0 snapshot)

| Family | Bank | Manifests |
|---|---|---|
| GC/MGC | **3,177** (permanent kill, Req-3) | `disccamp0_gc_2010_18` (closed) |
| ES | **2** | `h_od_1_es_overnight_drift` (closed, K=1) + `harv2026_001_es_monthend` (closed, K=1) |
| NQ/MNQ | **1 closed + 1 open** | `d5_nq_intraday_mom` (closed, K=1) + `orb_mnq_intraday_breakout` (**open**, K=1) — conservative sniff basis: any new NQ-family seed enters at bank **2** |
| 6J / 6E / CL / YM / all others | **0** | — |

Sniff consequence: new-seed K_eff at K_intrinsic=1 → ES 3 (floor 0.98, marginal PASS) · NQ 3 (0.98) · YM/6J/6E/CL 1 (0.65).

## Dead-class wall (emit — the burst must not re-stage)

From `docs/rejected_candidates.md` + closed manifests + `docs/methodology/rejected_signals.md` + harvest kill ledger (checked 2026-07-17):

1. Month-end / turn-of-month, any instrument, any citation (D3 ES power 0.24–0.30; D7 6J power 0.30; Q-HARV-1 §R DECLINED; A4 diagnostic residue).
2. Monthly-frequency TSMOM 12m/1m at Default-#1 OOS N≈86 (H-TSMOM-1; H-TSMOM-6J power 0.26–0.34; break-even N≈192).
3. Intraday last-30m / rest-of-day momentum on index micros (D5 — cost-law 11.06bp hurdle vs ≈2.97bp cohort; Tier-C, no size carve-out).
4. Overnight drift / session drift siblings (H-OD-1 — mechanism CONFIRMED, cost-law killed 5.05bp vs 1.5bp; MNQ expression separately UNSCREENABLE).
5. Any GC/MGC-required design (bank 3,177 → floor 2.05; only permanent kill class).
6. Registry rejects: XAGUSD Guardian-family · custodian month-end EURUSD · USOIL spike-fader · EURUSD fixing-reversal · EURGBP Aegis port · gold KER/TSMOM regime-gate · GEX gate · T10Y3M gate · Friday gate · micro-Treasury intraday MR · SPX dispersion · 5th-leg free-data domain (SNAG-CLOSED).
7. Carry timing (Koijen 6J/6E/CL expressions) — **not re-stageable as admissible rows** while Req-2 timing-δ stays unpublished-per-instrument; pre-declared probe-fork limb only.
8. `rejected_signals.md`: starvation signal (methodology-layer; no market class implicated).

## Burst discipline check (before Phase 1)

- `discovery_manifests/` count at burst open: **5** (delta must be 0 at close).
- No `register_search open` inside the burst window; zero pulls, zero K.
- Q1–Q6 families inherited by reference (freeze `b304f2c` lineage); not edited.
