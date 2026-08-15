# RESULTS — HARV-2026-001 (Q-HARV-0)

**Disposition:** CLOSED — AMBIGUOUS — H1 corroborated but placebo magnitude un-passable; successor pre-Q parked 08-08

**Candidate:** HARV-2026-001
**Brief:** [`docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md`](lab/archive/../../docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md)
**Lab:** `lab/analysis/harv_0_month_end_rebalance_es_2026-07/`
**Status:** COMPLETE — Phase 2–5 run 2026-07-12 (`run_harv0.py` → `results.json`, `diagnostics.py` → `diagnostics.json`)
**Panel:** Pepperstone→n/a; Databento GLBX.MDP3 `ohlcv-1d` continuous `.c.0` (unadjusted). parents sha256 `f096b116…83e9f8e`, micros sha256 `db83cb82…86091b`. 192 months (2010-07→2026-06), 163 qualifying.

---

## Verdict (exactly one)

- [ ] RESOLVED
- [ ] FALSIFIED
- [x] **AMBIGUOUS**

**Reporting taxonomy:** `DONE_WITH_CONCERNS` — all gates evaluated; H1 corroborated at primary but the mid-month placebo magnitude clause fired, and diagnostics show era decay + micro-era non-significance (named below).

## Deployability annotation (§4; does not alter verdict)

`DEPLOYABLE-DEFAULT-ENVELOPE:` **YES** — capturable intraday C = **+21.10 bp** (same-signed as H1) ≥ 4× two-RT hurdle (13.68 bp). (Informational; AMBIGUOUS does not authorize deployment.)

## Primary H1 (pooled parent panel)

| Metric | Value |
|---|---|
| n months / n qualifying | 192 / 163 |
| trade rate | 84.9% (clause OK: within [40%, 90%]) |
| mean signed window (bp) | **+19.21** |
| σ (per-month) / CI95 | 126.4 bp / **[−0.19, +38.6] bp** (parametric CI grazes 0 — permutation is the gate, per §4 power disclosure) |
| permutation p (10k label shuffles) | **0.0129** (frozen full-shuffle null); **0.0042** under the alt fix-qualifying/permute-signs null → significant under both, frozen null is the more conservative |
| cost hurdle 1× / 4× (single-RT bp) | 1.71 / **6.84** (MES specs; mes_price 4373) |
| H1 pass (≥4× ∧ p≤0.05)? | **YES** (19.21 ≥ 6.84 ∧ 0.0129 ≤ 0.05) |

## Bundled predictions

| Gate | Pass? | Notes |
|---|---|---|
| P-placebo (T-13→T-11) | **NO** | p 0.9837 > 0.10 ✓ but \|est\| = **29.07 bp** ≥ 50% of H1 (9.6 bp) ✗ — mid-month effect is opposite-signed and *larger* than primary |
| P-instrument (GC) | YES | −10.5 bp, p 0.7006 (>0.10) — control clean |
| P-covariance (\|R_spread\| terciles) | YES | low 30.4 → high 38.5 bp (high>low); mid −12.4 bp (non-monotone middle) |
| P-micro-OOS (MES same-sign) | YES | +15.00 bp, same-signed, n=75 |

## Diagnostics (non-gating)

- Unconditional TOM window mean: **+7.98 bp** (H1 conditional +19.21 bp is 2.4× the unconditional drift)
- **Ex-quarter-end subset (roll-clean): +25.13 bp, p 0.0164, n=107** — effect is *stronger* where the roll phantom is absent ⇒ NOT a roll artifact
- Quarter-end-only: +7.88 bp, p 0.1855, n=56 (weak/noisy; 18/56 qualifications within one ~135bp roll-phantom of threshold)
- **Era 2010-2017: +26.35 bp, p 0.0151** vs **Era 2018-2026: +13.41 bp, p 0.1049 (not significant)** — front-loaded; possible decay
- Micro-era parent (2019-05→): +14.86 bp, **p 0.1335 (not significant)** — significance weakens exactly on the deployable era (native MES same-sign still holds)
- Next-month reversal (signal·T-1→next-T3): **−15.96 bp** — the faded winner recovers next month (transient-pressure/reversal consistent with the Etula/Parker mechanism)
- Step-0: OK (192 months, 0 dup, 0 NaN in R_spread/window/C/G/placebo, 64 quarter-end)

## Triggers / notes

**§6 trigger fired: P-placebo magnitude clause.** H1 clears the primary gate (effect, permutation, hurdle, GC control, covariance, micro same-sign, trade-rate) but the identical rule on the mid-month T-13→T-11 window shows a **−29 bp opposite-signed** effect that exceeds 50% of the primary magnitude. Under the frozen partition that is AMBIGUOUS, not RESOLVED (§5: no rescue). Compounding concerns: **era decay** (post-2018 p=0.10) and **micro-era-parent non-significance** (p=0.13).

**Post-closure diagnostic (2026-07-12, non-gating — verdict unchanged):** the placebo trigger is **selection arithmetic, not a market phenomenon**. T-13→T-11 lies *inside* the conditioning window (prev-T-1→T-4), so qualifying months mechanically carry anti-signal drift in every sub-window: signed conditioning-window ES drift = −363 bp over ~18.6 days (mean |R_spread| among qualifying = 412 bp) ⇒ pro-rata 2-day prediction −39 bp; observed T-16→T-14 / T-13→T-11 / T-10→T-8 / T-7→T-5 = **−38.2 / −29.1 / −28.3 / −29.8 bp** — uniform, matching the prediction, nothing special about the frozen window. With a ~30–39 bp mechanical floor vs a 9.6 bp allowance, **the clause was structurally un-passable at registration** (RESOLVED unreachable for any realistic calendar-effect size). The placebo p-clause itself passed (0.98 > 0.10). Successor requirement + lane lesson (gate-reachability simulation at registration) recorded in the closure note.

## Closure artifacts

- Closure note: [`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`](lab/archive/../../docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md)
- Monitor spec (RESOLVED only): [`MONITOR_SPEC.md`](MONITOR_SPEC.md) — N/A (AMBIGUOUS)
- Provenance pins: [`PROVENANCE.md`](PROVENANCE.md); Wave-1 record: [`NOTES.md`](NOTES.md)
- Machine output: `results.json`, `diagnostics.json`
- K ledger: `discovery_manifests/harv2026_001_es_monthend.json` (closed; primary p=0.0129 at K=1)
