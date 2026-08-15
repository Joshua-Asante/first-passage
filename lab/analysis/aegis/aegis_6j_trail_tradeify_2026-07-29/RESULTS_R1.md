# RESULTS — R1 (per-contract daily-$ std) for Aegis→6J

**Date:** 2026-07-29 · **Script:** [`r1_sigma.py`](r1_sigma.py) · **Log:** [`run_r1.log`](run_r1.log)
**Screen:** third-leg spec [§2.3 / §7.2 R1](../../../docs/spec/2026-07-27-third-leg-target-spec.md) —
per-contract daily-$ std ≤ ~$125 at the $100K basis. **Never measured for 6J** until now.

**Headline: R1 PASSES. It does not block Aegis-6J — and the prediction that it would was wrong.**

---

## §1 — The estimator failed one of its two calibration anchors, so no absolute value is reported

The spec derives ORB's figure as `438 / 2.31` — a leg's daily-$ std at deployable weight divided by
its contract count. Reproducing that shape from panels requires the Stage-8 weight normalization.
Two published anchors were used as controls **before** reading the 6J number:

| Anchor | Published | This estimator | Verdict |
|---|---|---|---|
| Composed book (MYM+MNQ) daily-$ std | **$273** | $882 all-days / $1,890 trade-days | **DOES NOT REPRODUCE** |
| ORB-MNQ per-contract | **$190** (→ FAIL, 1.5×) | **$270.94** (→ FAIL, 2.2×) | verdict ✓, magnitude +43% |

**Anchor 1's failure is diagnosed, not shrugged at: TV equity compounding.** The book's trade-day
std grows **$1,381 (H1) → $2,282 (H2), 1.65×**, because dollar P&L scales with compounded equity —
so a raw-panel std is *not* "the $100K basis". This is the repo's known TV-compounding artifact.
**Consequence: no absolute R1 number is reported for 6J.** Reporting one would be the
borrowed-metric-without-its-cohort failure.

**What survives is a clean relative comparison.** Both instruments that matter are
**compounding-free**: the ORB panel is **qty = 1 exactly** (min 1, max 1), and 6J is cap-bound at 12
on 76% of trades, its halves flat at $1,237 → $1,108. So ORB↔6J on one estimator is valid even
though the absolute basis is not reconstructable.

## §2 — Measurement

Per-contract daily series = (day's net P&L ÷ day's contracts), zeros on flat days. The all-days vs
trade-days convention is **load-bearing for 6J and immaterial for ORB** (which trades 99.1% of
days), so both are carried.

| | traded | per-contract daily-$ std (all-days) | (trade-days) |
|---|---:|---:|---:|
| ORB-MNQ v0.2 (spec's negative control) | 99.1% | **$270.94** | $273.03 |
| **6J (Aegis v0.3, panel of record)** | **11.1%** | **$37.40** | **$109.75** |
| 6J ÷ ORB | | **0.138×** | **0.402×** |

**Verdict by relative calibration.** The spec places ORB at **1.5× the ceiling**, so the ceiling in
this estimator's units is $270.94 / 1.5 = **$180.63**:

| 6J convention | value | vs ceiling | verdict |
|---|---:|---:|---|
| all-days | $37.40 | **0.21×** | **PASS** |
| trade-days | $109.75 | **0.61×** | **PASS** |

**PASSES under both conventions** — the result is convention-robust, which is what makes it usable
despite the unreconstructable absolute basis. Contracts fitting the same budget ORB needed 0.66 of:
**4.8 (all-days) / 1.6 (trade-days)**. **There is no granularity lockout for 6J.**

## §3 — The prediction this refutes

The pre-run expectation (stated to the operator on 2026-07-29) was that 6J would fail R1 on
granularity, reasoning from notional: ¥12.5M ≈ $85K per contract, so "almost certainly multiples of
the ceiling". **That was wrong, and wrong for an instructive reason.** R1 is a property of the
*strategy's realized daily P&L per contract*, not of the instrument's notional. Two things dominate:

1. **Frequency** — Aegis-6J is flat **89%** of sessions. A leg that does not hold contributes no
   variance on those days, and portfolio daily variance is an unconditional quantity.
2. **Stop distance** — Aegis's 1R is **$1,385.74 at avg qty 11.35 ≈ $122/contract**, so one 6J
   contract under Aegis's rules carries roughly the risk of a couple of index micros. The contract
   is large; the *position's risk* is not.

Notional is a poor proxy for variance contribution. ORB — a 1-contract MNQ strategy trading 99% of
days — carries **7.2×** the per-contract daily variance of a full-size 6J leg.

## §4 — Why passing R1 does not rescue the candidate

**The σ-screen assumes approximate Gaussianity, and this leg violates it badly — for exactly the
reason it passes.** Being flat 89% of days produces:

- **excess kurtosis +43.8** on the all-days per-contract series;
- **worst single day −$196.35/contract = 5.3σ** of that series.

A standard deviation is a poor summary of a distribution that is a point mass at zero plus
occasional ~1R hits. R1 measures the *average* variance contribution; **bust is a path-and-tail
property**, and the direct measurement of it ([`RESULTS.md`](RESULTS.md), ledger **J4b**) returns
**3.88% vs a 3.0% ceiling — FAIL** at the best achievable sizing.

**R1 PASSES and the direct survival measurement FAILS. When they disagree, the direct measurement
governs** — §2.3 says so in its own words: a pre-screen that decides what is worth running, never a
substitute for the run. This is a worked example of that clause firing, and the first one in the
repo where the pre-screen is the *permissive* side.

## §5 — Disposition

**R1 is removed from the blocker list for Aegis-6J.** It was the cheap test named as likely-fatal;
it is neither fatal nor decisive. Remaining same-account blockers:

1. **Bust — measured FAIL** (J4b: 3.88% vs 3.0%, best cell). This is now the *only* measured blocker.
2. **S2** — the screen's text excludes non-micro contracts. Its **rationale is now weak for 6J
   specifically**: E5 grounds S2 in sizing granularity (refuted above — 1.6–4.8 contracts fit),
   firm scaling plans, and databento Rule-4 **proxy** discipline (inapplicable — this panel is
   natively measured on 6J, not proxied from a parent). Moving S2 is a **§6.1 event and an operator
   call**, not an edit; recorded here, not acted on.

**Caveats.** No absolute R1 value is established (§1) — only a relative verdict against the spec's
own negative control. The ORB anchor reproduces in verdict but not magnitude (+43%), which is itself
a flag on the spec's two-point extrapolation. Neither weakness affects the direction: 6J is 0.138×
ORB, and ORB fails by 1.5–2.2×.

No `core/`, allocation, `dd_protection`, Pine, rung, or rail byte touched. Nothing armed. K unchanged.
