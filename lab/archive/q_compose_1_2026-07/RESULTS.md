# Q-COMPOSE-1 — composed-book (2-leg Class-S c1 + ORB-MNQ-1 @0.37%) regime-breadth re-MC — RESULTS

**Status:** `FALSIFIED` (§6 row 2 — both limbs, every tier)
**Date run:** 2026-07-17 (frozen engine; wall 5,428 s)
**Pre-reg:** [`Q-COMPOSE-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md) (FROZEN 2026-07-16, operator-signed §9)
**Phase-0 record:** [`PHASE0.md`](PHASE0.md) (anchors re-verified; injection shape ratified = book-daily construction per the §2 disjunction; smoke + 2-leg falsifier control clean)
**Driver:** [`run_compose_regime_remc.py`](run_compose_regime_remc.py) · machine report `compose_remc_report.json` (committed)
**Closure:** [`docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`](lab/archive/../../docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md)

## Frozen configuration (§2, executed exactly)

3-leg book {MYM-Striker @0.70%, MNQ-Striker @0.37% (byte-pinned, un-haircut), ORB-MNQ-1
@0.37% (SINGLE frozen weight, 1.00× lifecycle)}; panel 2020-01-06 → 2026-06-30 (1692
bdays, frozen index — H1/H2 midpoint identical to the c1 rider); engine 10,000 sims ×
seeds 42/123/2026, horizon 1500, inactivity off, dd_protection OFF, Run-2 consistency-on
where present; bootstrap n=100, block 126 bd, seed 20260715; floor per (partition × tier):
bust ≤ 3.0% ∧ P(pass) ≥ 50%, bootstrap additionally bust-95th ≤ 3.0%. ORB daily series
engine-faithful (R-multiset assert vs `orb_lib.orb_backtest`); DBN cache sha256
`4fc074ab4bf5aca1…` recorded in the report.

## Per-cell table (headline bust / pass; frozen 10k × 3 engine)

| Tier | dd_type | Full | H1 (2020-23 chop) | H2 (2023-26) | boot bust-95th | boot pass-5th | all-four clear |
|---|---|---|---|---|---|---|---|
| Bulenox_100K | trailing | **44.75%** / 55.3% | **60.93%** / 39.1% | **31.38%** | **52.82%** | 47.2% | no |
| Tradeify_Select_100K | trailing_locking | **38.75%** / 61.3% | **54.73%** / 45.3% | **25.84%** | **47.14%** | 52.9% | no |
| MFFU_Rapid_100K | trailing_locking | **38.54%** / 61.5% | **54.17%** / 45.8% | **25.79%** | **46.80%** | 53.2% | no |
| BluSky_Premium_100K | trailing | **51.91%** / 48.1% | **67.63%** / 32.4% | **37.28%** | **59.58%** | 40.4% | no |

**2-leg baseline (REGIME_GATE.md @163b0b5) vs composed, discharge tiers:** Tradeify full
2.65% → **38.75%**, H1 4.37% → **54.73%**, H2 1.70% → **25.84%**, boot-95th 10.37% →
**47.14%**; MFFU full 2.64% → **38.54%**, H1 4.36% → **54.17%**, boot-95th 10.33% →
**46.80%**. Every partition — including full-panel and H2, which the 2-leg book PASSES —
is dramatically worse under composition.

## §6 gate assertion

- `RESOLVED` trigger (all four partitions clear on ≥2 tiers incl. ≥1 trailing_locking): **0 clearers** — not met.
- `FALSIFIED` trigger (H1 bust > 3.0% **OR** boot-95th > 3.0% on **every** tier): met on **every tier via BOTH limbs** (H1 54–68%, boot-95th 47–60% vs the 3.0% ceiling — 15–23× over).
- `AMBIGUOUS-HOLD` limbs: not reached.

**Verdict: `FALSIFIED`.** Breadth at the frozen weight does not rescue — it destroys —
the book's bust geometry.

## §2-required 3-leg breadth declaration (weekly Mon-anchored, n=339)

| | 2-leg | 3-leg | Δ |
|---|---|---|---|
| dependence N_eff (PR corr) | 1.9948 | 2.9502 | **+0.9554** |
| risk N_eff (PR cov) | 1.9593 | 1.9628 | **+0.0034** |

Byte-reproduces Stage-8 (`RESULTS_stage8_neff.md` @9620138). The decomposition IS the
mechanism finding: near-perfect **correlation** breadth (2.95/3.0) with **zero risk**
breadth — ORB at 0.37% carries $438/day std at the $100K basis vs $273/day for the entire
2-leg book (composed $539/day, ~2×) against an unchanged $3,000 trailing barrier. A
dollar-denominated trailing-DD tail is owned by the dominant-variance leg; PR(corr) rising
while PR(cov) stays flat predicted harm, not help.

## Deviations / integrity notes (all recorded pre-run in PHASE0.md)

- `median_days_to_pass` not surfaced by `summarize_outcomes` — pass_rate is the
  practicality proxy (non-gating; same as the haircut sibling).
- Full-n reproduction control skipped (not mandated); harness fidelity shown by the 2-leg
  smoke control (2.83%/2.83% vs frozen 2.65%/2.64%) + the haircut sibling's 2026-07-17
  1.00× control on this machine/venv.
- No weight, partition, tier, or engine setting other than the §2 table was examined
  (§5 honored; single frozen ORB weight).
