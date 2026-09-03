**Theme:** c1
**Verdict:** CLOSED — Class-S #1 haircut re-MC superseded; §4 discharge withdrawn
**Status:** ACTIVE — lifecycle-haircut regime re-MC for Class-S candidate #1
# Class-S candidate #1 — lifecycle-haircut regime re-MC: RESULTS

> ## ⛔ SUPERSEDED 2026-07-22 — every bust figure below is computed on a DEFECTIVE input,
> ## and the §4 discharge asserted below was WITHDRAWN
>
> **(1) Defective input.** The `Tradeify_Select_*` eval rows carried `dd_lock_offset_usd: 100`,
> giving the simulated **evaluation** a drawdown-locking cushion Tradeify does not apply in eval.
> All figures below are **optimistic**. Corrected values at the deployed WATCH-1 0.50× rung:
> full-panel 0.08% → **0.11%**, H1 0.14% → **0.22%**, bootstrap-95th 0.77% → **1.20%**; at 1.00×,
> H1 4.37% → **6.78%**. Both verdicts survive correction (0.50× PASS, 1.00× FAIL).
> Corrected sources: [`CORRECTED_FULLPANEL.md`](CORRECTED_FULLPANEL.md) (same directory) and
> [`../eval_shape_diagnostics_2026-07-28/RESULTS.md`](../eval_shape_diagnostics_2026-07-28/RESULTS.md)
> (L130).
>
> **(2) §4 is NOT discharged.** L71–72 ("The mechanical Part A **DISCHARGED** (four-firms §4
> falsifier) is unchanged") and L92 ("program §4 was already discharged by candidate #1") are
> stale. That discharge was **WITHDRAWN 2026-07-22** —
> [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
> (`Accepted`): corrected eval geometry flips both `trailing_locking` tiers Part A FAIL,
> `discharges_falsifier = False`, and §4 is live with hard date **2026-11-08**. The 2026-07-24
> 50K-band re-score found two Part A clearers (`Tradeify_Select_50K` 1.06% / `MFFU_Rapid_50K`
> 0.96%), which defeats the 11-08 "no clearer on any tier" demotion clause **without**
> discharging §4; `Tradeify_Select_100K` @ 1.00× corrected scores **4.74% — FAIL** against the
> 3.0% ceiling. ⚠ **2026-09-03:** that ceiling was raised to **5.0%** on 2026-08-26
> ([`prereg v2`](../../../../docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md)
> §3), against which 4.74% would read PASS. **Do not re-read it that way** — the withdrawal ADR's
> §5 bars moving the ceiling to re-admit this candidate, and 4.74% is an EOD-clock lower bound with
> **no *gate-grade* 1.00× honest-clock successor**. ⚠ A 1.00× honest-clock figure does exist, in this
> campaign's own sibling file — [`RESULTS_INTRADAY_W1.md`](RESULTS_INTRADAY_W1.md) §Non-vacuity:
> **real bust 32.33%** / pass 57.17% vs EOD 2.50% / 71.00%. It is a reduced-N guard run (horizon 400,
> 200 sims/seed, book level, MFFU not resolved separately), so it cannot settle the collision — but
> it is the only 1.00× honest-clock evidence there is, it is **strongly adverse** (failing at 3.0%
> and 5.0% alike), and it must not be omitted from any account of whether 4.74% may be re-read.
> See that ADR's
> [Addendum 2026-09-03](../../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-09-03--the-50-ceiling-does-not-re-admit-candidate-1-proposed).
>
> **(3)** Both Striker legs were withdrawn from the c1 eval deployment 2026-08-04. The re-MC
> result itself (regime-robustness at the 0.50× haircut) is unaffected.
>
> Body below is frozen and unedited.


**Status:** `RESOLVED-DEPLOYABLE` — c1 is regime-robust at a reversible **WATCH-1 (0.50×)** book-level lifecycle haircut.
**Run completed:** 2026-07-17 (0.50× arm wall 11,499s ≈ 3.2h, n=100 / 10k×3 sims, 8 cores).
**Pre-registration (FROZEN, operator-signed §9):** [`docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md)
**Parent candidate:** [`2026-07-15-existing-strategy-book-candidate-1-prereg.md`](../../../docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md)
**Gate of record:** [`2026-07-13-prop-survivor-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)

## Verdict (§6)

**RESOLVED-DEPLOYABLE at the least-haircut passing rung — WATCH-1 (0.50×).** The 0.50× arm clears
the frozen floor (bust ≤ 3.0% **and** pass ≥ 50%) on **all four partitions × both discharge tiers**.
The **0.25× arm was not run** — moot under the least-haircut decision rule once 0.50× passes.

## The numbers

Both discharge tiers return identical partition results (same $100K book daily series; both are
`trailing_locking` with a 3.0% DD) — reported once:

| Partition | 1.00× (baseline / control) | **0.50× (WATCH-1)** | Floor |
|---|---|---|---|
| Full-panel bust | 2.65% / 2.64% | **0.08%** | ≤3.0% ✓ |
| **H1 (2020-23 chop) bust** | **4.37% / 4.36% — FAIL** | **0.14%** | ≤3.0% ✓ |
| H2 (2023-26 trend) bust | 1.70% | 0.02% | ≤3.0% ✓ |
| **Bootstrap-95th bust** | **10.37% / 10.33% — FAIL** | **0.77%** | ≤3.0% ✓ |
| Bootstrap pass-5th | ~89% | 95.76% | ≥50% ✓ |
| **Gate** | **FAIL (regime-fragile)** | **PASS** | |

The two binding cells that failed at 1.00× collapse under the half-size haircut — **H1 4.37% → 0.14%**
(~31×) and **bootstrap-95th 10.37% → 0.77%** (~13×), far more than linearly. A trailing-DD bust is a
barrier-crossing event; halving position volatility sharply cuts the odds of crossing a fixed 3%
barrier under positive drift. Crucially, **pass-rate stays high** (bootstrap pass-5th 95.76% ≫ the
50% floor), so the decompound-precedent "impractical" failure mode does **not** bite here.

## Reproduction control (§6 precondition — satisfied)

The 1.00× control validated the harness by **exact reproduction** of the frozen 2026-07-15
`REGIME_GATE.md` baseline (recorded in `run_full.log`, from the first, teardown-killed full run):
full-panel **2.65% / 2.64%**, H1 **4.37% / 4.36%**, H2 **1.70%** — matching the baseline to the basis
point. The gate is fully seeded (`thr` seeds + `BOOT_SEED=20260715`), so the bootstrap-95th (baseline
10.37%) is deterministic; its re-run was skipped as redundant, and the exact match on the three
non-bootstrap partitions confirms harness fidelity. The 0.50× arm ran on the **identical** harness
(same frozen 2026-07-15 primitives), differing only by the ×0.5 multiplier on `daily_100k`.

## Discipline honored (per pre-reg §5)

- Only the ratified `core/lifecycle.py` ladder rungs tested; 0.50× is the **least-haircut** passing
  rung (WATCH-1). No fractional "just-clear" search.
- Frozen **3.0% / 50%** floor inherited unchanged; no separate "regime floor."
- Haircut applied **book-level** (×0.5 on `daily_100k`); **no** locked-parameter edit, **no** re-weight
  of the 0.70/0.37 composition, **no** `lifecycle_state.json` write on the CFD legs. Primary injection
  confirmed faithful in run Phase-0 (`core/mc/simulation.py` consistency clause is ratio-based →
  scale-invariant under a uniform daily haircut).
- `median_days_to_pass` not surfaced by `summarize_outcomes` → `pass_rate` reported as the
  practicality proxy (documented §8 Phase-0 deviation; non-gating; pass stays 95%+).

## What this means, and what stays gated

- **Finding:** c1 (2-leg **MYM+MNQ**, Striker-only, native futures) is **regime-robust when deployed at
  WATCH-1 (0.50×)** — the reversible, down-only lifecycle haircut rescues it from the standing
  regime-fragile caveat. This **contradicts** the decompound-HOLD-based prior (which predicted no
  static de-risk would be regime-robust without making the challenge impractical); the 2-leg futures
  book behaves differently from the 4-leg CFD book.
- **Cost of the haircut:** at 0.50× the book runs at half its risk_pct → roughly half the per-period
  return, so median-days-to-pass roughly doubles. The pass **rate** stays 95%+ within the 1500-day
  horizon, so this is a practicality caveat, not a blocker.
- **Still gated (unchanged):** rail build, account registration, and go-live remain separate operator
  GO/NO-GO. This is a **deployability finding + a lifecycle-intake basis** (CANDIDATE, deployable at
  WATCH-1), nothing more. The mechanical Part A **DISCHARGED** (four-firms §4 falsifier) is unchanged
  and was never at issue in this re-MC.

## Artifacts

- Machine report: `haircut_remc_report.json` (committed). Run log: `run_050.log`; 1.00× control
  evidence: `run_full.log`; per-arm intermediate: `arm_0.50x.json` (logs + intermediates gitignored).
- Run environment: worktree frozen code + main-clone `.venv-research` (py3.11.9, numpy/pandas/joblib) +
  sha256-pinned CME panels (`15d8b` / `beabf`); 0.50× arm n=100 / 10k×3, joblib across 8 cores.

## Ratification (2026-07-17)

Operator ratified (chat: "ratify c1 as CANDIDATE deployable at WATCH-1") — recorded at
[`../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md`](../class_s_candidate1_scoring_2026-07-15/G8_INTAKE.md)
("Ratified disposition" section, supersedes the prior 1.00×-with-standing-caveat intake). Lifecycle
intake: **CANDIDATE, deployable at WATCH-1 (0.50×)**, book-level. Go-live path (rail / account)
stays a separate operator decision.

**Correction:** candidate #2 (S1, 3-leg + Aegis→6J, ae744) — flagged below as "remains available"
before this ratification session checked current repo state — was scored separately 2026-07-16
and closed **`FALSIFIED — all-four-fail`** (Tradeify/MFFU 5.69% bust); it does not affect this
ratification (program §4 was already discharged by candidate #1).

## Next (operator)

1. ~~Ratify the deployability finding~~ — **DONE 2026-07-17** (see above).
2. Optional: run the 0.25× arm for margin/color (not required — 0.50× is the least-haircut answer).
3. Go-live path (rail / account) stays a separate operator decision. Candidate #2 is dead (see
   correction above); a fresh existing-strategy candidate would need its own pre-registration.
