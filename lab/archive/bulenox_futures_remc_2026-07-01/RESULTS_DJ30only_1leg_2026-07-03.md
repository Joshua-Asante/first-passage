# DJ30-only (1-leg) Bulenox viability re-MC — VERIFIED result

**Date:** 2026-07-03 · **Driver:** [`dj30_only_remc.py`](dj30_only_remc.py) · **Verdict:** **NEEDS-REWORK** (bust-safe but not a viability win; two cheap tiers design-void; needs a true integer re-run for lock-grade)

Question (operator-chosen, 2026-07-03): after Q-P2-MEASURE-1 killed NAS100 on edge-transfer and Q-P2-MEASURE-1.b showed DJ30's edge transfers — does a **DJ30-only** MYM book survive Bulenox's fixed-$ trailing DD, given DJ30 is cap-bound to ~half its locked risk? C5 modeled the *2-leg* book (no tier cleared the pre-registered gates; 150K 91.26%/8.74%).

## Screen numbers (5000 sims × 3 seeds, C2-off, token-mitigated inactivity; full-history 2020-2026 panel)

| Tier | arm | eff risk | pass | bust | p99 DD | med days | integer base | status |
|---|---|---|---|---|---|---|---|---|
| 25K | CAPPED | 0.43% | 99.27% | 0.00% | 2.51% | 465 | **0 contracts** | **VOID** |
| 50K | CAPPED | 0.54% | 99.65% | 0.02% | 3.10% | 372 | **0 contracts** | **VOID** |
| 100K | CAPPED | 0.50% | 98.82% | 0.83% | 2.82% | 397 | 1 contract | CONTINGENT (coarse) |
| **150K** | CAPPED | 0.43% | 99.10% | 0.29% | 2.54% | 460 | 2 contracts | CONTINGENT (best) |
| 250K | CAPPED | 0.44% | 97.23% | 2.41% | 2.15% | 447 | 3 contracts | bust-gate FAIL |

FULL-arm (%-equity 0.70%, upper bound on bust): 25K 99.85/0.05 · 50K 99.72/0.19 · 100K+150K 96.69/3.29 · 250K 89.31/10.69. Bust is 100% trailing-DD (Bulenox has no daily-loss/static mode — verified).

## VERIFIED via a 6-lens adversarial workflow (wf_f114358d-e64, ~1.5M tokens)

4 of 6 lenses returned; 2 (cap-granularity, inactivity) errored on API stalls but the synthesis judge independently covered their scope. Findings, re-classified by the synthesis:

- **Numbers reproduce (Lens 6 CLEAN).** Independent from-scratch recompute of 150K CAPPED = 99.12% pass / 0.32% bust / 2.57% p99DD / 457 med — within <0.03pp of the driver. SE at n=15K/~99% ≈ 0.08pp. The reported cells are what the specified inputs produce.
- **Wiring clean (Lens 1 MINOR).** 1-strat panel, firm_kwargs→Bulenox rules, C2-off=dd_scale=1.0, PRE_SHOCK_1R pin (fell_back=False), single tier-rescale — all correct. **One real infidelity:** `_simulate_path` models Bulenox's **fixed-$** trailing cushion as **percent-of-peak**, biasing bust optimistically low by 0.07–0.36% of balance as equity rises toward target. Sub-gate-flip magnitude, and it is the same convention C4/C5 used — but it is a genuine model gap for a fixed-$ trailing venue.
- **Force-flat sound (Lens 4).** 10/273 exits truncated (3.7%), net −11.5% — matches C4's ~3.7%/−9.6%. Panel not corrupted.

### Corrections that change the headline

1. **25K & 50K are DESIGN-VOID.** RESERVE policy = base ≤ ⌊cap/8.5⌋; tier caps 3/8/14/17/29 → base = **0/0/1/2/3**. At 25K/50K DJ30 base rounds to **zero contracts** — no book. The CAPPED mean-ratio scalar (a continuous multiplier) is structurally blind to this step-discontinuity. C5 independently flagged 25K void for the 2-leg book. The 25K/50K CAPPED rows are meaningless.
2. **"NAS100 was the bust driver" — NOT ESTABLISHED (drop it).** A matched-panel, matched-sizing 2-leg book busts only **0.65%**, with bust split ~50/50 DJ30/NAS100. The C5 8.74%→sub-1% improvement is dominated by integer-vs-mean-ratio **sizing** and C5's shared-account cap modeling — not by removing NAS100.
3. **The mean-ratio CAPPED scalar is not faithful at coarse tiers.** 100K/150K run a 1–2-contract base; the "FULL/CAPPED brackets the true integer result" claim is untested and likely **false** where base rounds toward 0 (a scalar cannot bracket a step-discontinuity). Only a per-trade integer re-run settles 100K/150K.
4. **A retracted refutation:** LENS 5 claimed a 13.8× "vintage confound" (0.29%→3.99% bust). The synthesis **could not reproduce it** under controlled window slicing (bust 0.07%–0.47% across all regimes) — Lens 5 fed a different export without re-pinning 1R, reintroducing exactly the magnitude the fixed-1R pin divides out. The bust gate **is** regime-robust; the 3.99% is withdrawn.

### The single most decision-relevant fact

**The low bust is "not failing while rarely finishing," not "passing."** At 150K the median time-to-pass is **~457 days**, and in the 2020–2022 chop regime **only 36.7% of paths ever pass — 62.8% hit the 1500-day horizon cap.** A one-legged book trading Tue/Fri only, at ~half locked risk (cap-bound), needing 15+ months median to clear +6% and stalling in chop, is a **capital-efficiency problem, not a viability win.** And per C5 Finding #1, applying the FXIFY-calibrated bust<1% gate to a cheap-retry Bulenox eval is a **new operator-owned EV decision**, not an inherited pass/fail.

### Also standing

- **All tiers TOKEN-TRADE DEPENDENT.** `inactivity_limit=10000` fully disables Bulenox's ≥1-trade-per-5-trading-days rule; unmitigated, C5 measured ~96% of paths die to inactivity (worse for 1-leg). The numbers are conditional on a mandatory automated 1-micro token trade in TradersPost.
- **Provenance weakness (Lens 4).** The panel is built from the 2026-07-03 export (N=273, net $250K), which does **not** reconcile to the canonical 2026-05-24 567e1 baseline (N=218, net $440K) even on the same window (+22% trades / −43% net / 38→11 full-stops — unexplained). The fixed-1R pin (own-1R $4,128 vs pinned $4,229, −2.6%) absorbs the magnitude so no number moves, but it is an audit-trail defect for lock-grade use.

## Bottom line

A DJ30-only MYM book **does not blow up** — `bust <1%` (regime-robust) and `p99 DD <5%` genuinely clear at **150K** (and marginally 100K) at cap-bound sizing. But it is **not the rescue the raw table suggested**: the two cheapest tiers are design-void (base=0), the viable tiers run at coarse 1–2-contract granularity the scalar model can't vouch for, the "NAS100-driver" story is false, and the low bust is bought by a book that **stalls in chop** (457-day median, 62.8% horizon-cap). Minimum viable tier is **150K**, and even there it is a slow, capital-heavy, token-trade-dependent instrument.

## Must re-run before lock-grade

1. **True integer-contract DJ30-only re-run** (base = ⌊cap/8.5⌋ per trade; suppress base=0 legs) — formally voids 25K/50K, tests whether 100K/150K's bust survives real 1–2-contract granularity. Replaces the mean-ratio scalar the CAPPED arm currently uses.
2. **Reconcile the 2026-07-03 export to the canonical 218-trade 567e1 baseline** (or re-run on 567e1), and **fix the fixed-$ vs percent trailing-DD model** in `firm_rules`/`_simulate_path` for a fixed-$ venue.
3. **Report the token-trade dependency + 457-day median / 62.8%-chop-horizon-cap in the headline**, not the caveats.
