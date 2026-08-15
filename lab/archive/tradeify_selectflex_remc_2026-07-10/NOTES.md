# Tradeify Select Flex re-MC — analysis & §4 verdict (2026-07-10)

Operationalizes CC-HANDOFF-tradeify-target-firm.md (+ §1 ADDENDUM). Reproducible
raw table: [`RESULTS_tradeify_remc_2026-07-10.md`](RESULTS_tradeify_remc_2026-07-10.md);
driver: [`run_tradeify_remc.py`](run_tradeify_remc.py).

## Headline

**§4 hypothesis FALSIFIED at the pre-registered gates (bust < 1% AND p99 DD < 5%).**
No Tradeify Select Flex tier clears *both* gates, in either the 2-strat canonical
book or the 3-strat (+Aegis/6J provisional) book. The binding constraint was **NOT
barrier geometry alone** — it is the locked strategies' **edge survival on the
force-flat CME-micro venue** (the P2 edge-transfer gate already closed FALSIFIED,
2026-07-06). Switching the firm improves the *box*; the *book underneath* still
busts ~7% (2-strat 100K/150K) to ~13% (3-strat).

Per the handoff §5(3) and §4, this is reported as-is — **nothing was tuned to make
a gate pass.**

## What the lock geometry actually buys (it IS a real improvement — just 2nd-order)

Comparison is on IDENTICAL fixed-$ trailing arithmetic; the ONLY difference is the
lock (Tradeify offset=$100 vs matched-Bulenox offset=unreachable). At **100K/150K**
the two firms' DD ($3,000/$4,500) and target (6%) are identical, so those tiers
isolate PURELY the lock:

| Tier (2-strat) | Bulenox-matched (no lock) | Tradeify (lock) | Effect of lock |
|---|---|---|---|
| 100K | bust 9.11% / p99 3.51% | bust **7.04%** / p99 3.90% | bust −2.1pp |
| 150K | bust 9.11% / p99 3.51% | bust **7.01%** / p99 3.90% | bust −2.1pp |

The lock also holds **p99 DD < 5% at every 2-strat tier** (4.29–4.31% at 25K/50K,
3.90% at 100K/150K) and reduces p99 vs Bulenox at the small tiers (25K: 4.29% vs
5.13%) by capping how far the trailing floor can rise. So the geometry fix works
exactly as designed — it just cannot overcome a book that busts ~7–9% on the venue.

**25K/50K anomaly:** Tradeify busts *more* than Bulenox there (3.09% vs 0.45% at
25K) because Tradeify's *Select* DD is TIGHTER than Bulenox's ($1,000/$2,000 vs
$1,500/$2,500). The tighter box outweighs the lock. Clean lock-isolation exists
only at 100K/150K.

## Harness validation (high confidence)

The `Bulenox shipped (%-of-peak)` cross-reference reproduces the recorded canonical
Bulenox C4 **pass/bust** numbers (PR #274, RESULTS_C4_forceflat_2026-07-03.md) EXACTLY
at all four tiers — 25K 99.60%/0.40%, 50K 98.87%/1.13%, 100K 91.46%/8.54%, 150K
91.46%/8.54%. C4's `run_bulenox_remc` uses the SAME `567e1` DJ30 trades export this
run uses (only its BAR_EXPORT bar file differed), so this is a direct
reproducibility check, not a vintage-invariance claim. **p99 DD does NOT reproduce**
(this run 3.55% vs C4's 2.97% at 100K; 5.13% vs 5.09% at 25K): C4 ran 2026-07-03,
before the 2026-07-06 bust-day max_dd inclusion fix (commit `83e589f`,
`docs/adr/2026-07-06-bust-day-maxdd-inclusion.md`) that records the breach day's DD
on bust paths — this run includes it, so its p99 is legitimately higher. Pass/bust
are the gate-relevant quantities and match exactly; the harness is faithful. (The
matched-Bulenox fixed-$ arm 100K = 90.89%/9.11% also reproduced on an independent
§7-review re-run, and sits correctly between the %-of-peak 8.54% and the
Tradeify-lock 7.04%.)

## Fidelity — the integer-micro arm (RUN 2026-07-10, [`RESULTS_tradeify_integer_2026-07-10.md`](RESULTS_tradeify_integer_2026-07-10.md), driver [`run_tradeify_integer_remc.py`](run_tradeify_integer_remc.py))

The %-equity table above is Run 1 (optimistic: full locked %-risk). The integer-micro
arm sizes each trade in whole micro contracts under Tradeify's own caps (20/40/80/120),
RESERVE cap policy, and a round-turn cost — the C5 model. It does **not** simply "fail
harder" as first hypothesized; it changes the picture, and running it was load-bearing:

* **Contract caps de-risk the book to ~0.45–0.52× locked risk** (DJ30 base capped at
  `floor(cap/(1+pyr))` = 2/4/9/14 contracts for 25/50/100/150K; NAS similar). Smaller
  positions → **LOWER** bust than %-equity (100K integer 4.59% vs %-equity 7.04%), but
  median days-to-pass roughly DOUBLES (100–152d vs 67–71d), and at 25K the NAS leg is
  **design-void** (71/163 base trades round to 0 contracts under the micro-20 cap). So
  the earlier "integer fails harder on bust" note was wrong on direction — corrected here.
* **The pass/fail verdict is entirely commission-sensitive.** With NO cost, all four
  Tradeify tiers PASS both gates (bust 0.06/0.09/0.80/0.92%, p99 <5%). With the $2.22/
  contract round-turn PROXY, all four FAIL (bust 1.05/1.11/4.59/5.02%). Tradeify's actual
  commission is **NEEDS_CONTEXT** (not in §1), so the integer arm BRACKETS the answer
  rather than resolving it — the true bust sits between "comfortably passing" (no-cost)
  and "failing" (proxy-cost), pivoting on a number we do not have.
* Lock still helps at matched-DD 100K/150K (with-cost Tradeify 4.59/5.02% vs
  matched-Bulenox no-lock 6.26/6.82%) — same ~1.7pp direction as %-equity.
* **Harness validated:** the Bulenox %-of-peak integer cross-ref reproduces recorded
  C5 pass/bust near-exactly (25K 99.50/0.50, 50K 97.19/2.81, 100K 87.58/12.42, 150K
  91.24/8.76 vs recorded 91.26/8.74; p99 differs only via the 2026-07-06 bust-day-maxdd fix).
* Commission is a **PROXY** ($2.22 RT = Bulenox CME-micro all-in) — Tradeify's real
  per-side rate must be confirmed before any read at 25K/50K, where the margin over the
  1% gate is only 0.05–0.11pp and entirely cost-driven.

**Net across both arms:** neither the barrier geometry NOR the fidelity switch delivers
a robust, commission-independent pass. The %-equity arm falsifies clearly (full-risk
book busts 3–7%). The integer arm shows a capped book CAN approach/clear the gate — but
only by trading at ~0.5× risk over ~5 months with a void NAS leg at small tiers, and
only if Tradeify's commissions are low enough (unverified). The binding constraints
remain the strategy edge on the venue and now, specifically, the eval-economics gate +
the real commission — an operator EV decision, not a geometry fix.

## Commission RESOLVED (2026-07-10) — research follow-up to the §5-flagged proxy

The $2.22/contract proxy above was a Bulenox borrow (NEEDS_CONTEXT at the time). Tradeify's
real commission is now **verified from two primary Tradeify sources**, fetched directly
(WebFetch was 403'd by both help-center pages — Intercom blocks bots — so this was
retrieved via the in-app browser instead):

* [Trading Commission Fees](https://help.tradeify.co/en/articles/10468315-trading-commission-fees)
  (Tradeify Help Center, last updated **2026-04-28**): **Micro E-Mini Dow (MYM) = $1.82**,
  **Micro E-Mini NASDAQ (MNQ) = $1.82**, both **per contract, round-trip**. Page states
  explicitly: *"Total Round Trip Cost includes Exchange fees, NFA fees, Clearing fees, and
  Commissions"* — i.e. **all-in**, no execution slippage included, free-membership tier.
* [Tradeify Pricing Reference](https://help.tradeify.co/en/articles/14369021-tradeify-pricing-reference)
  (updated ~2026-06-26): independently corroborates **MNQ = $1.82**, **MES = $1.82**
  round-trip, and states *"All brokers (Tradovate, Rithmic, WealthCharts) are the same
  price — no platform surcharges"* — confirms $1.82 applies on the Rithmic rail this
  operation's TV→CrossTrade→NT8→Rithmic lane uses.

A third-party aggregator surfaced in search (~$0.62–0.67/side ≈ $1.24–1.34 RT) was **not**
corroborated by either Tradeify-owned page and is treated as unreliable — the two primary
sources agree with each other and are used instead ([[lesson_verify_source_not_label]]).

**Verified cost is LOWER than the $2.22 proxy** ($1.82 vs $2.22, −18%). The integer arm
was re-parameterized on `rt_cost` (was a with/without-costs boolean) to run three points:
$0 (bound), **$1.82 (verified, primary)**, $2.82 ($1.82 + 2-tick round-turn slippage,
conservative live-exec sensitivity) — code lands in `run_tradeify_integer_remc.py`.

**The $1.82 re-run was started but STOPPED before completion at the operator's explicit
instruction ("no need to run the re MC, we will end it here") — there is no
`RESULTS_tradeify_integer_RESOLVED_2026-07-10.md`, and no number at the verified $1.82
cost exists.** The two bracket points that DID complete earlier (from
[`RESULTS_tradeify_integer_2026-07-10.md`](RESULTS_tradeify_integer_2026-07-10.md), run
against the superseded $2.22 proxy) still stand as the only real data:

| Cost | 25K | 50K | 100K | 150K |
|---|---|---|---|---|
| $0 (no-cost bound) | 0.06% / 2.68% — PASS | 0.09% / 2.78% — PASS | 0.80% / 2.99% — PASS | 0.92% / 3.01% — PASS |
| $2.22 (superseded proxy) | 1.05% / 3.96% — FAIL | 1.11% / 3.98% — FAIL | 4.59% / 3.50% — FAIL | 5.02% / 3.56% — FAIL |

$1.82 sits 82% of the way from $0 to the $2.22 proxy (only $0.40 below it), not partway
toward the no-cost bound — so a same-direction, same-order-of-magnitude result to the
$2.22 row is the reasonable expectation, NOT something close to passing. But this is
qualitative judgment, not a measurement: cost enters the panel linearly per-trade while
bust probability is a nonlinear (threshold/barrier) function of cumulative drag, so
naive interpolation between these two points is not a substitute for the actual run.
**Status: commission is RESOLVED (verified $1.82); the integer-arm verdict AT that cost
is explicitly UNRESOLVED — left open by operator decision, not by data.**

**Bonus corroboration for Caveat 1 (cheap-retry eval economics):** the Pricing Reference
page confirms Select reset fees are $60/$95/$169/$239 for 25/50/100/150K — far below a
full re-purchase ($109–$369). This directly supports treating `bust<1%` as an
FXIFY-inherited one-shot gate that is likely too strict for Tradeify's actual retry economics.

## Caveats (carry into any operator decision)

1. **Gate provenance is a live Forward question.** `bust < 1%` is FXIFY *one-shot
   purchase* economics. Tradeify Flex is a *cheap-retry* eval (small monthly fee,
   re-purchasable). The appropriate accept/reject gate for cheap-retry economics is a
   NEW operator-owned EV decision, NOT the inherited FXIFY 1% (RESULTS_C5:19 flagged
   the same for Bulenox). This re-MC deliberately reports against the pre-registered
   FXIFY gate and does NOT move it post-hoc (that would be p-hacking). Under a laxer,
   EV-justified bust gate the 2-strat 25K/50K (~3% bust, p99 <5%) could be
   acceptable — but that is the operator's call, on stated economics, made before
   reading these numbers, not after.
2. **Aegis/6J 3-strat is PROVISIONAL and makes it WORSE.** The v0.3 6J leg is a
   non-canonical prototype (trail-MC not locked; BEPAD closed-falsified). Adding it
   raises bust everywhere (2-strat 100K 7.04% → 3-strat 100K 13.37%) — its 2022-H1
   chop tail is a net drag. The 3-strat verdict inherits provisional status on this
   leg. Aegis 1R pinned to the 6J panel's own full-stop mean ($1,385.74), allocation
   held at the locked Aegis 1.50% (both provisional choices for a non-locked lane).
3. **Vendor data was copied into the worktree** (gitignored, not committed) from the
   main checkout to enable the run: DJ30 567e1 + NAS100 11605 + US30_M15 bars + the
   Aegis 6J panel (sha256 `c3b341…` verified against the panel-of-record).
4. **dd-protection OFF (C2-off)** — the TV→CrossTrade→NT8→Rithmic rail cannot run a
   portfolio-equity overlay; matches the Bulenox C4/C5 canonical arm.
5. Panel windows: 2-strat 2022-01-04→2026-04-17 (1119 bdays); 3-strat extends to
   2026-07-01 (1172 bdays) via the Aegis 6J panel's later last-trade.

## Bottom line for the firm-selection thesis

"Shop the barrier, hold the edge fixed" is a sound principle, and Tradeify's EOD-lock
IS a strictly better barrier than Bulenox's never-locking trail (lower bust at
matched DD, lower p99 DD, no daily-loss limit, own-account group-trading permitted).
But on the currently-mappable force-flat futures book the **edge is the binding
constraint, not the box** — consistent with the futures pivot already being DEMOTED.
The firm decision and the edge-transfer question are separable: Tradeify is the
better firm *if/when* a book that clears the operator's (re-derived) eval gate
exists. Today, no tier clears the FXIFY-inherited gate. Returns to the parent for
the gate-economics decision and as AMBIGUOUS-leaning-negative on "geometry fixes the
first-passage failure."
