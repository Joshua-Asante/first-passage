# Q-COMPOSE-1 — CLOSURE: `FALSIFIED` (breadth does not rescue the book's regime-fragility)

> ⚠ **2026-07-22:** this closure's "four-firms ADR §4 falsifier: remains discharged by c1"
> line was **WITHDRAWN** — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). Closure left as written (Trap #12); this Q's own verdict is unaffected.

**Closed:** 2026-07-17
**Parent Pre-Q:** [`Q-COMPOSE-1-orb-classs-book-regime-breadth.md`](../Q-COMPOSE-1-orb-classs-book-regime-breadth.md) (now `CLOSED — FALSIFIED`)
**Pre-reg (FROZEN 2026-07-16, operator-signed §9):** [`Q-COMPOSE-1-verdict-preregistration.md`](../pre-registration/Q-COMPOSE-1-verdict-preregistration.md)
**Run artifacts:** [`lab/archive/q_compose_1_2026-07/`](../../../lab/archive/q_compose_1_2026-07/) — `PHASE0.md` (architecture confirm), `run_compose_regime_remc.py`, `RESULTS.md`, `compose_remc_report.json`
**Engine:** frozen — 10,000 sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, bootstrap n=100/126 bd/seed 20260715; floor bust ≤ 3.0% ∧ P(pass) ≥ 50% (+ bootstrap 95th ≤ 3.0%). No criterion moved after data (Trap #12 clean); single frozen ORB weight (no sweep).

## Verdict (§6 asserted against actual numbers)

**`FALSIFIED`** — the §6 row-2 trigger fired on **every tier via BOTH limbs** (only one was
required): H1 headline bust 54.17–67.63% and bootstrap-95th bust 46.80–59.58% against the
3.0% ceiling, at ORB @ 0.37% / 1.00× lifecycle. Zero tiers cleared all four partitions;
the RESOLVED and AMBIGUOUS limbs were never approached.

## Anchor numbers (frozen 10k × 3; composed vs the 2-leg baseline it had to beat)

| Tier (dd_type) | Partition | 2-leg baseline | Composed 3-leg | Floor |
|---|---|---|---|---|
| Tradeify_Select_100K (trailing_locking) | full | 2.65% PASS | **38.75%** | ≤3.0% |
| | H1 2020-23 | 4.37% FAIL | **54.73%** | ≤3.0% |
| | H2 2023-26 | 1.70% PASS | **25.84%** | ≤3.0% |
| | boot bust-95th | 10.37% FAIL | **47.14%** | ≤3.0% |
| MFFU_Rapid_100K (trailing_locking) | full / H1 / H2 / boot95 | 2.64% / 4.36% / ~1.70% / 10.33% | **38.54% / 54.17% / 25.79% / 46.80%** | ≤3.0% |
| Bulenox_100K (trailing) | full / H1 / H2 / boot95 | (3.51% full, Part-A FAIL) | **44.75% / 60.93% / 31.38% / 52.82%** | ≤3.0% |
| BluSky_Premium_100K (trailing) | full / H1 / H2 / boot95 | (4.44% full, Part-A FAIL) | **51.91% / 67.63% / 37.28% / 59.58%** | ≤3.0% |

Composition made **every** partition dramatically worse — including full-panel and H2,
which the 2-leg book passes. This is not a marginal miss: 15–23× over the ceiling on the
pre-committed limbs.

## Honest prior vs what happened

The §4 disclosed prior was FALSIFIED (decompound-HOLD precedent; ORB dead-2020
regime-common-mode), with RESOLVED live via joint-tail diversification. FALSIFIED
happened — but by a **different and stronger mechanism than the prior imagined**: the
regime-common-mode contest never got to matter, because simple variance dominance decided
it first. At 0.37%, ORB's daily $ std at the $100K basis ($438) exceeds the **entire**
2-leg book's ($273); the composed series runs ~$539/day against an unchanged $3,000
trailing barrier, collapsing bust geometry on ALL partitions including the trend half.
The §7 prior-look disclosure had named exactly this ("0.37% is *not* risk-conservative…
the bootstrap-95th limb is the direct test of whether that dominance helps or hurts") —
measured answer: it devastates.

**The breadth decomposition is the finding:** dependence N_eff 1.9948 → 2.9502
(near-perfect correlation breadth, +0.955 of a possible +1.0) while risk N_eff stayed
flat at 1.96 → 1.96. Correlation breadth without risk-weight balance does nothing for a
dollar-denominated trailing-DD tail — the tail is owned by the dominant-variance leg.

## Dispositions

- **Q-COMPOSE-1 CLOSED.** The breadth lever is now measured on the same defect the sizing
  lever was measured on: **sizing PASSES** (haircut re-MC: WATCH-1 0.50× clears all four
  partitions × both discharge tiers), **breadth FAILS**. Extends the decompound-HOLD "no
  static counterbalance" finding to a breadth-adding leg (its first non-sizing extension).
- **c1 disposition:** the §6 "accept-with-caveat + tripwires" fallback is already
  satisfied-and-superseded by the **2026-07-17 G8 ratification — lifecycle CANDIDATE
  deployable @ WATCH-1 (0.50×)** — which stands independently of this fork and is now the
  **sole** deployable path for the c1 book. Nothing re-opens.
- **Combined (composed × haircut) arm: NOT licensed.** §5 permits it only "if both singles
  fail"; the haircut single passed. No further compose test is owed or authorized.
- **ORB-MNQ-1 standing unchanged:** remains a standalone lifecycle CANDIDATE @ 1.00× with
  its ADMISSION.md caveats. This closure kills its role as a **c1 book leg at the tested
  weight/geometry** — it does not demote the candidate. A failed composed candidate closes;
  it does not iterate weight (§5).
- **Four-firms ADR §4 falsifier:** remains discharged by c1 (banked); this adds a negative
  composition data point, re-opens nothing. Feeds the **2026-08-08** packet.
- **K-accounting:** pre-registered single-arm portfolio re-MC (no search, no sweep) — no
  discovery manifest consumed; no K banked.

- **Registry:** rejected_candidates.md — ### Q-COMPOSE-1 ORB-MNQ-1 breadth-leg composition × MYM+MNQ Class-S c1 book — FALSIFIED (regime-breadth re-MC)

## Lesson candidates

1. **Dependence N_eff is not a bust-geometry input; risk N_eff is.** A leg that lifts
   PR(corr) to near-max while leaving PR(cov) flat predicts *harm* to a trailing-DD floor
   when it is variance-dominant — check PR(cov) before composing, it was known pre-run
   (Stage-8: risk N_eff 1.96 at 0.37%, falling at higher weights). Sibling of
   `lesson_market_neutral_not_regime_neutral` and the candidate-#2 "third leg is not free"
   prior; sharpens both from correlation-space into risk-space.
2. **The cheap falsifier ran before the expensive one and was decisive:** the daily-std
   comparison ($438 ORB vs $273 whole-book, computed in seconds at Phase-0 smoke) already
   implied the verdict the 1.5 h frozen-engine run then confirmed. The frozen engine was
   still owed (pre-registered), but the magnitude ordering was knowable at panel-build
   time — a future compose pre-reg should surface the injected-leg vs book daily-$-std
   ratio in its §7 disclosure, not just weekly vol.

## Audit hook (append-only)

Was any criterion moved after data arrived? **No.** Floor, partitions, tiers, engine,
weight, and verdict table all match the FROZEN 2026-07-16 pre-reg byte-for-byte; the run
executed the §8 protocol in order (Phase-0 report → Phase-1 → this §6 assertion).
