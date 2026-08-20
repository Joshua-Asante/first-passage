# ADR 2026-08-20 — N-SURV magnitude-resampling gap becomes a mandatory disclosure line, not a gate change

**Status:** `Proposed` — drafted at operator direction (`Q-NSURV-2` RESOLVED, "go bigger" election), ratification owed
**Decision date:** 2026-08-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** methodology (research rules of evidence / reporting convention only). No `dd_protection`, allocation, Pine, rail, lifecycle, or gate-arithmetic change.

## Decision

Every future N-SURV-gated verdict (Pre-Q brief, closure, or `ops/instruments/*.md` finding that cites a single-history bust%/pass% as evidence for or against a survivor-scoring gate) must carry a one-line disclosure: *the single-history point estimate is one draw from a process whose magnitude-resampled spread has, on 2 of 2 candidates measured to date, been material on at least one axis (c1: bust-axis sd 7.07pp; ORB-MNQ-1: pass-axis sd 24.17pp) — cite the point estimate, but not as a stand-alone confidence claim.* This is a **reporting requirement only**. `run_partition_mc`, `blocks_from_daily_pnl`, and every existing N-SURV gate's PASS/FAIL arithmetic are **unchanged** — no closed verdict is re-scored, and no future verdict's gate criteria are altered by this ADR.

## Grounds

`Q-NSURV-1` (`RESOLVED` 2026-08-20) confirmed the single-history magnitude-blindspot is general across two independently-fitted candidates, with its own closure explicitly deferring design work to "a third candidate or a principled reason to act on 2." `Q-NSURV-2` (`RESOLVED` 2026-08-20) supplies that principled reason: a wrapper reproducing both candidates' headline point estimates bit-identically (within 2.0pp) — reusing already-committed fitted-family artifacts, touching no core simulation/bootstrap code — proves an additive, non-retroactive disclosure is buildable today at effectively zero blast radius. Mirrors the 2026-08-04/08-18 family-K-bank precedent exactly: a real estate-wide finding, operationalized as a mandatory disclosure rather than a gate change, because the evidence to calibrate a *gate* change (how large the true spread is for an arbitrary future candidate, not just the two measured) doesn't yet exist.

## Reads

`docs/briefs/closures/Q-NSURV-1-closure-resolved.md` @ `97f301f` (parent finding) · `docs/briefs/closures/Q-NSURV-2-closure-resolved.md` @ this session (reproduction proof) · `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` @ `6608339` (direct structural precedent) · `lab/analysis/c1/nsurv_layer_design_2026-08-20/wrapper_reproduction_results.json` (reproduction numbers).

## Gate

`Accepted` on operator ratification — no §4 falsifier apparatus (light tier): this is a reporting-format addition, not a load-bearing threshold or gate-arithmetic change, so there is nothing quantitative to falsify. If a third N-SURV candidate is ever measured and shows NO material magnitude-resampling spread on any axis, that would inform (not obligate) a future review of whether the disclosure is still warranted — named here as a watch condition, not a revert trigger.

## Boundary

Do not read this ADR as authorizing a change to `run_partition_mc`'s bust/pass computation, any existing N-SURV gate's PASS/FAIL threshold, or a re-score of any closed verdict. It adds exactly one disclosure requirement to future reporting; nothing broader. A future ADR proposing an actual gate-arithmetic change (e.g., gating on a resampled percentile instead of the single-history point estimate) is a separate, heavier decision this ADR does not make and does not pre-authorize.
