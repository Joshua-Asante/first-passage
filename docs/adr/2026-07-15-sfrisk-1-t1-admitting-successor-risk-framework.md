# ADR — Admit T1 as the self-funded successor risk framework (Q-SFRISK-1 RESOLVED)

**Status:** Accepted (ratified 2026-07-15)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-15
**Authors:** Joshua (risk-tolerance numbers, "confirm T1") + Claude Code (recorder/adjudicator)
**Supersedes:** none — **admits** a new falsifiable claim set; does not edit or revive the retired challenge-era numbers (99.83/0.17/4.37 stay historical per the rescope ADR).
**Related:** [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) (§4 completion falsifier, discharged by this ADR — see its dated addendum); [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md) (parent Pre-Q, `H-SFRISK-1`); [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md) (T1's frozen numbers); [`docs/briefs/Q-SFRISK-1-closure-resolved.md`](../briefs/Q-SFRISK-1-closure-resolved.md) (the closure this ADR is promoted from); [`docs/adr/2026-06-07-decompound-remc-hold.md`](2026-06-07-decompound-remc-hold.md) (the instrument this framework runs on; its HOLD is unaffected — see §2); [`docs/adr/2026-07-06-bust-day-maxdd-inclusion.md`](2026-07-06-bust-day-maxdd-inclusion.md) (explains the F1 fidelity delta, §0).
**Layer:** portfolio / governance (a new risk-characterization claim; **zero** locked parameter, allocation, `dd_protection` constant, or MC-anchor touch)

---

## §0 — Rule 0 reads (production-source verification)

Read on-disk this session, off `origin/main` @ `432e14e`:

- [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](../briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md) — anchor `9b219ab` (2026-07-14). `Status: NUMERIC FROZEN`; T1 is the sole declared triple: F1 `p99 max-DD ≤ 10% per regime half`, F2 `DEFERRED` (no clause), F3 `ADOPT +5%/$200K base/reset-to-base (banded)`, F4 `median days-to-first-skim > 252 bd ⇒ IMPRACTICAL`. Operator-confirmed via "confirm T1," 2026-07-14.
- [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md) — §4 `H-SFRISK-1` (accept/reject/ambiguous-hold conditions, verbatim), §6 gate table (`RESOLVED` trigger: "≥1 declared triple clears both regime halves without crossing the impracticality bar" → "Promote to admitting ADR / go-live risk artifact" — this ADR is that promotion), §5 forbidden moves (transcribed from the rescope ADR; none forbid admission of a cleared triple).
- [`lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md`](../../lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md) — the Phase-1 numeric report (merged `936a9e0`). F1: H1 pass 86.16% / bust 13.84% / p99 **8.00%** / med 62; H2 pass 99.79% / bust 0.21% / p99 **4.53%** / med 20. F4 (n_paths=30000, seed=20260607): H1 median **51.0 bd** / censoring 0.3%; H2 median **16.0 bd** / censoring 0.0%; pooled median 26.0 bd / censoring 0.0%. Independently re-run locally this session against the identical frozen driver spec — every reported figure reproduced byte-identically, cross-validating both the instrument and the Phase-1 report's F4 panel-source correctness (built from the clean 2026-06-25 vintage, not the stitched 2026-06-07 vintage `days_to_first_skim.build_banded_portfolio_panel()` would default to).
- [`docs/adr/2026-07-06-bust-day-maxdd-inclusion.md`](2026-07-06-bust-day-maxdd-inclusion.md) — anchor `83e589f` (2026-07-06). Explains why F1's H1 p99 (8.00%) diverges from the 2026-06-25 informal reference (7.76%) while pass/bust/median stay byte-identical: the fix includes breach-day drawdown in bust-path `max_dd`, scaling with bust rate. Confirms 8.00% is the current, engine-correct figure — not a re-run defect.
- [`docs/adr/2026-06-07-decompound-remc-hold.md`](2026-06-07-decompound-remc-hold.md) (+ 2026-06-25 addendum) — the instrument this framework runs on. Its HOLD (locked allocations/dd_protection unchanged; both *historical challenge-era* gates breach on the decompounded full-history panel) is a separate, still-standing decision about **parameter** configuration. This ADR does not touch it — T1 is a different, self-funded-native claim set evaluated on the same instrument, not a relock of the challenge-era gates.
- [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) — anchor `99b7854` (2026-07-11). §4's completion falsifier (2026-11-08 hard date, "no successor risk-framework Pre-Q pre-registered" → D1 mandatory go-live blocker) — this ADR discharges it in full (see its dated addendum, landed alongside this ADR).
- CLAUDE.md — Live-execution posture section: "Aegis→M6J is the sole active lane (go-live is a separately gated decision)." This ADR supplies risk-characterization input to that separate gate; it is not the gate itself (§5 forbidden moves).

---

## §1 — Context

The 2026-07-11 rescope ADR retired the challenge-era P(pass)/bust/p99-DD claims as *live* self-funded claims (the FXIFY venue that made them live claims no longer exists) but left a completion falsifier: without a successor risk-framework Pre-Q pre-registered, run, and adjudicated by 2026-11-08, D1 escalates to a mandatory blocker on any Aegis→M6J go-live decision. Q-SFRISK-1 was pre-registered 2026-07-14 (architecture), numerically frozen the same day (T1, operator-confirmed "confirm T1"), and run 2026-07-15 (Phase 1, merged `936a9e0`, independently cross-validated this session). Every declared clause of the sole declared triple clears on both regime halves without approaching the impracticality bar — [`docs/briefs/Q-SFRISK-1-closure-resolved.md`](../briefs/Q-SFRISK-1-closure-resolved.md) formally asserts `RESOLVED` per the frozen §6 table.

**Decision driver (one sentence):** the frozen gate cleared on real data under a pre-registered, non-negotiable spec — admitting T1 as the operative self-funded risk framework is the mechanical next step the parent brief's own §6/§9 already commit to, not a fresh judgment call.

---

## §2 — Decision

**T1 is admitted as the self-funded successor risk framework, replacing the retired challenge-era P(pass) claim as the risk-characterization input for any future Aegis→M6J go-live decision.** Concretely:

1. **The claim (what T1 says):** On the clean-vintage decompound instrument (2020–2026, locked book, dd_protection C2), under the withdrawal model **ADOPTED** as-is (+5% skim / $200K base / reset-to-base), evaluated separately on both the 2020–2023 chop half and the 2023–2026 trend half:
   - The 99th-percentile peak-relative max-DD does **not** exceed **10%** on either half (observed: H1 8.00%, H2 4.53%).
   - The lane is **not operationally impractical** by the median-days-to-first-skim measure — observed medians (H1 51 bd, H2 16 bd) sit far inside the 252-bd ceiling on both halves.
2. **What this claim is a successor to:** the retired challenge-era 99.83%/0.17%/4.37% P(pass)/bust/p99-DD headline, which answered a different question (probability of passing a $200K FXIFY challenge) that no longer has a live referent. T1 answers the self-funded question directly — capital-ruin risk and cashflow-return cadence — on both the regime that already broke both old challenge gates (H1) and the regime that didn't (H2).
3. **What this claim is NOT:** a go-live authorization, a relock of any locked parameter, or a revival of the historical anchor as a live number. Aegis→M6J go-live is a separately gated operator decision (`CLAUDE.md` Live-execution posture) that may now cite this ADR as its risk-characterization input.
4. **F2 (TUW) status:** remains explicitly deferred. T1 is admitted as a 3-dimension triple (F1+F3+F4) by the operator's own Phase-0 scoping decision; a future amendment may add a TUW clause without reopening or altering this admission.

**Effective:** immediately (ratified 2026-07-15).
**Scope:** claim admission and documentation only. Zero `core/` behavior change — no locked parameter, allocation, `dd_protection` constant, test pin, or Pine byte is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **HOLD instead of RESOLVED** (accept the numbers but decline to admit a framework) | Not supported by the frozen §6 table — "≥1 declared triple clears both regime halves without crossing the impracticality bar" is an unconditional `RESOLVED` trigger, not a discretionary one. `H-SFRISK-1`'s own text names an admitting ADR *or* a dated HOLD as the Accept-side outcomes; nothing here is ambiguous or half-vacuous (both halves discriminate cleanly, no near-miss on either clause) — a HOLD would be inventing discretion the pre-registration didn't reserve. |
| **Fold T1 admission into the existing decompound-HOLD ADR** | Wrong layer: that ADR is a *parameter-configuration* decision (allocations/dd_protection HELD unchanged) evaluated against the *historical challenge-era* gates, which still breach on the decompounded panel. T1 is a *different, self-funded-native claim set* on the same instrument — conflating the two would misrepresent both: the challenge-era breach is real and stays recorded; T1's clearance is also real and is a separate question. |
| **Wait for F2 (TUW) before admitting anything** | The operator explicitly scoped the Phase-0 freeze to F1/F3/F4 only, deferring F2 by name — treating that deferral as a blocker on T1's own three clauses would override an explicit operator scoping decision without new grounds. T1 stands on what it declares; F2 is additive, not a precondition. |
| **Treat this as authorizing go-live directly** | Overreach — conflates "a falsifiable risk claim exists and clears" with "the operator has decided to go live," which involves considerations (capital readiness, execution rail state, R6/R7 residual-program status) outside this Pre-Q's scope. §4/§5 make the boundary explicit. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger (either limb fires → T1's admission is reopened, not silently edited):**

1. **Data-provenance:** a future re-derivation of the clean-vintage panel (a new export, a corrected stitch, a further engine fix in the class of `2026-07-06-bust-day-maxdd-inclusion`) moves F1's H1 p99 above 10% or F4's H1/H2 medians above 252 bd. Revert action: supersede this ADR with a fresh admitting-or-reverting ADR citing the re-derivation; do not edit the numbers in place here.
2. **New regime data:** the quarterly regime-check machinery (`docs/adr/2026-06-07-decompound-remc-hold.md` §4, next 2026-08-08) finds a trailing window materially worse than the recorded H1 — if a fresh half-panel cut under T1's own F1/F4 clauses would fail, that is grounds to reopen, not silently absorb into "the framework already cleared once."
3. **F2 amendment:** if a future TUW amendment to T1 fails on either half, that failure attaches to the *amended* triple, not this one — this ADR's admission of the 3-dimension T1 stands until superseded, per §2 item 4.

**Trigger check schedule:** ride the standing quarterly regime-check cadence (2026-08-08, 2026-11-08, 2027-02-08, 2027-05-08), alongside the decompound-HOLD ADR's own §4 trigger. **Note (2026-07-22):** that §4 trigger's *separate* C2→C0 revert-check companion (`time_to_pass.py --regime-check`) was retired the same day ([`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) §Addendum, D2) — the regime-check limb itself (and this trigger, which rides it) is unaffected and still stands.

---

## §5 — Forbidden moves (under this ADR)

- **Treating this ADR as a go-live authorization.** It supplies risk-characterization input to a separately gated decision; it is not that decision. Any future go-live ADR must cite this one, not assume it.
- **Reviving the historical 99.83/0.17/4.37 anchor as a live claim "because T1 also cleared."** T1 is a distinct claim set; the rescope ADR's re-labeling stands untouched.
- **Editing the decompound-HOLD ADR's §2/§4 to declare it "resolved" by this admission.** That ADR's parameter-configuration HOLD, evaluated against the historical challenge-era gates, is a separate decision layer and remains as recorded (both those gates still breach on the decompounded panel).
- **Silently overwriting the F1 fidelity delta (8.00% vs 7.76%) instead of citing the dated engine-fix explanation.** Recorded in §0/§2 of the closure record; the current figure is the one this ADR admits.
- **Adding an F2/TUW clause here "while we're at it."** Explicitly deferred by operator scope; a future amendment, not a same-ADR addition.
- **Editing `core/dd_protection.py`, `core/firm_rules.py`, or any locked constant "to align with T1."** Zero-behavior-change scope is what makes this ADR safe to accept without a re-MC of the locked book.

---

## §6 — Consequences

**Positive:**
- The 2026-11-08 completion falsifier is discharged well ahead of its hard date, with room for the operator to review at leisure rather than under deadline pressure.
- The self-funded scale path now has a falsifiable, dated, regime-split-tested risk claim in place of a documented vacuum — the exact gap the 2026-07-11 rescope ADR flagged as its own completion risk.
- The claim is conservative by construction: it clears on H1, the historically worse regime (both old challenge gates broke there), not merely on the benign H2 trend regime.

**Negative (real cost):**
- T1 is a 3-dimension triple; duration risk (TUW) is not yet a first-class gate. A future regime could produce a long, shallow underwater period that neither F1 (magnitude) nor F4 (median cadence) would catch on its own.
- The framework is validated against 2020–2026 history only; like every backtest-derived claim in this repo, it carries the standing caveat that history is not a guarantee.

**Risks:**
- A future regime resembling neither H1 nor H2 (e.g., a slow, grinding drawdown with rare severe days) could satisfy F1's p99 bar while still being operationally punishing in a way F4's median doesn't capture — mitigated by the standing quarterly regime-check plus the open door to a future F2 amendment.
- Treating "T1 cleared" as informally equivalent to "go-live is fine" despite §5's explicit prohibition — mitigated by that prohibition being named here and in the closure record, not left implicit.

**Downstream artifacts updated (this session, §7):**
- [`docs/briefs/Q-SFRISK-1-closure-resolved.md`](../briefs/Q-SFRISK-1-closure-resolved.md) — the closure this ADR is promoted from (done).
- `docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md` — `Status` flips `OPEN` → `CLOSED-RESOLVED`.
- `docs/adr/2026-07-11-challenge-era-claims-rescope.md` — dated addendum discharging §4's D1 completion falsifier.
- `STATE.md` — SFRISK forward-board entry updated to closed/RESOLVED.
- `docs/SESSIONS.md` — session entry.

---

## §7 — Implementation plan

Docs-only.

- **Phase 0** — §0 reads verified this session (`origin/main @ 432e14e`).
- **Phase 1** — this ADR + the closure record (both authored this session).
- **Phase 2** — parent brief `Status` flip; rescope ADR addendum; STATE.md + SESSIONS.md sweep.
- **Phase 3** — verification block executes; status ratified `Accepted` same day (2026-07-15), matching this repo's standing ADR ratification convention.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR referenced from the closure record and the parent brief
grep -n "2026-07-15-sfrisk-1-t1-admitting" docs/briefs/Q-SFRISK-1-closure-resolved.md docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md

# T1's three clauses cleared, as claimed here — cross-check against the Phase-1 report
grep -n "8.00%\|4.53%\|51.0\|16.0" lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md

# Decompound-HOLD ADR untouched (separate layer)
git diff --stat <pre-ADR-commit> -- docs/adr/2026-06-07-decompound-remc-hold.md
# Expected: empty

# Zero core/ touch
git diff --stat <pre-ADR-commit> -- core/
# Expected: empty

# Rescope ADR's completion falsifier discharge addendum present
grep -n "D1 completion falsifier discharged" docs/adr/2026-07-11-challenge-era-claims-rescope.md

# Validators unaffected
python scripts/verify_lock_anchors.py
# Expected: ROUTING: Closed
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md --type adr

git log -1 --format='%h %ci' -- docs/adr/2026-07-06-bust-day-maxdd-inclusion.md   # expect 83e589f
git log -1 --format='%h %ci' -- lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Initial authoring — T1 admitted, `Proposed`; promotes `Q-SFRISK-1`'s `RESOLVED` closure per its own §6/§9 | Joshua + Claude Code |
| 2026-07-15 | Ratified — status `Proposed` → `Accepted` (operator: "Flip it to Accepted") | Joshua |
