# Q-NSURV-2 — Can a magnitude-resampling second-uncertainty-layer be added to N-SURV reporting without touching any closed verdict's headline number?

**Addendum (2026-08-29, decay-audit correction):** This brief RESOLVED same-day, 2026-08-20 — see `docs/briefs/closures/Q-NSURV-2-closure-resolved.md` and `docs/adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md` (Accepted, ratified 2026-08-20). The Status/Closed lines and Pre-Lock Checklist below are the as-drafted pre-lock snapshot and are frozen as historical record, not current state. Separately, §7/§10's planned path `lab/analysis/c1/nsurv_layer_design_2026-08-20/` was never used; the actual Phase-1 artifacts landed and remain at `lab/archive/nsurv_layer_design_2026-08-20/` (stub: `lab/analysis/nsurv_layer_design_2026-08-20/CARD.md`; registry: `lab/CATALOG.md`).

**Status:** `OPEN — DRAFT (pre-lock)`
**Authored:** 2026-08-20
**Closed:** N/A
**Authors:** Joshua (operator election: "go bigger — open formal Pre-Qs") + Claude Code (Sonnet 5)
**Parent question:** `Q-NSURV-1` (`RESOLVED` 2026-08-20) — this Q is the deferred forward obligation named in that closure's own `## Iterate` block, opened one session earlier than that closure's own stated bar (see §2)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gates on whether an additive, headline-preserving wrapper design is buildable
**Artifact path:** `docs/briefs/Q-NSURV-2-second-uncertainty-layer-design.md`

---

## §0 — Rule 0 reads (production-source verification)

- `lab/discovery/prop_survivor_scoring.py` (`blocks_from_daily_pnl`, L327–343) — anchor `027a729` (verified `git log -1` 2026-08-20). Confirms the mechanism claim this Q's design rests on: block-bootstrap resamples *order*, never magnitude, of an already-observed daily series.
- `lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json` — anchor `19139a7` (2026-08-20). Candidate 1 (c1 book) fitted family + N=50 resampled bust distribution — the artifact any wrapper must reproduce headline numbers against.
- `lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json` — anchor `bf81496` (2026-08-20). Candidate 2 (ORB-MNQ-1) fitted family + N=50 resampled pass distribution — the second artifact any wrapper must reproduce against.
- `docs/briefs/closures/Q-NSURV-1-closure-resolved.md` — anchor `983db58` (2026-08-20). §1 confirms both candidates' headline point estimates (c1: bust 4.7433%; ORB-MNQ-1: bust 0.0000%/pass 52.2700%) and the axis-dependency finding this Q's design must not disturb.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` — anchor `6608339` (verified 2026-08-20; addendum landed 2026-08-18). The precedent this Q's `RESOLVED` branch would reuse: a disclosure-only convention that changes no gate behavior and no headline number.
- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md` §4 — anchor `027a729` (2026-08-20). Confirms the estate's existing tolerance convention for "reproduces a published number" (2.0pp on a bust%, the same style of check this Q's H uses for a bit-identical reproduction test).

---

## §1 — Context & motivation

`Q-NSURV-1` closed `RESOLVED` today, confirming on 2/2 independently-fitted candidates (c1: flat sizing, bust-axis sd 7.07pp; ORB-MNQ-1: cushion-proportional sizing, pass-axis sd 24.17pp) that the estate's N-SURV single-history block-bootstrap is blind to magnitude uncertainty, and that the blindspot's *location* is sizing-mechanism-dependent, not book-dependent. That closure explicitly deferred design work — "does the estate's N-SURV gate need a second uncertainty layer" — naming its own re-proposal bar: "needs a third candidate or a principled reason to act on 2, given axis-dependency was already a surprise once." Operator direction today elects to open this now rather than wait for a third candidate. This Q takes the "principled reason" branch: it scopes the design to something buildable and testable on the two data points already in hand, by asking only whether an **additive, non-retroactive** layer is possible — deliberately not asking whether the *gate's pass/fail logic* should change, which is a materially heavier question this Q does not open.

## §2 — Prior art / lineage

- `Q-NSURV-1` (`RESOLVED`, 2026-08-20) — the parent finding; this Q is its named forward obligation, opened one session early per operator election.
- `N-2026-08-15-nsurv-single-history-magnitude-blindspot.md` (Notice, `GRADUATED` via `Q-NSURV-1`) — original observation; §4 explicitly forbids "building a fix... without a dedicated Pre-Q." This Q is that dedicated Pre-Q.
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md` (`Accepted`, addendum 2026-08-18) — direct structural precedent for the `RESOLVED` disposition: a prior estate-wide finding was operationalized as disclosure-only, zero gate-behavior change, zero K/live-risk surface.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` — precedent for the *process* (multi-round adversarial hardening before ratification of a methodology-layer channel), not the content.

## §3 — Question (Q-NSURV-2)

**Q-NSURV-2:** Can a magnitude-resampling second-uncertainty-layer be attached to the estate's N-SURV reporting surface as a pure addition — reproducing both already-measured candidates' headline point estimates unchanged while also surfacing the resampled percentile bands already computed informally — or does reproducing those headlines require touching `run_partition_mc`/`blocks_from_daily_pnl` internals?

(Symptom-only check: the question names what's uncertain — buildability and blast radius of a specific design shape — not "should we build X." A design that turns out to require touching core internals is itself an answer, not a prescribed fix.)

## §4 — Falsifiable hypothesis (H-NSURV-2)

**H-NSURV-2:** If a wrapper can be built around the two candidates' existing fitted-family artifacts (`characterize.json` for c1; `nsurv_magnitude_probe_results.json` for ORB-MNQ-1) that (a) reproduces each candidate's already-published headline bust%/pass% point estimate to within the estate's existing 2.0pp fidelity tolerance without calling `run_partition_mc`/`blocks_from_daily_pnl` with different arguments or logic than production already uses, and (b) additionally emits the resampled percentile-band statistics already measured today, then a light disclosure-only ADR (mirroring the 2026-08-04/08-18 K-bank precedent) is sufficient — no gate-logic change is needed. Otherwise, a heavier System-domain ADR (own blast-radius accounting, own K/review cost) is required before any wrapper ships, and this Q does not open that ADR itself.

**Reject H-NSURV-2 if:** the wrapper cannot reproduce EITHER candidate's headline point estimate within 2.0pp without modifying `run_partition_mc`/`blocks_from_daily_pnl` call signature or internal logic.
**Accept H-NSURV-2 if:** the wrapper reproduces BOTH candidates' headlines within tolerance, additively, with zero changes to `run_partition_mc`/`blocks_from_daily_pnl`.
**Ambiguous-hold if:** the wrapper reproduces ONE candidate's headline but not the other within tolerance — would indicate the two candidates' fitted-family provenance is too heterogeneous for one wrapper design; re-test after a build attempt scoped to just the failing candidate. Re-test window: next session touching either candidate's N-SURV surface.

---

## §5 — Forbidden moves

- **Re-scoring or re-opening any already-closed N-SURV verdict's point estimate using the new layer's output.** Carried forward verbatim from `Q-NSURV-1` §3. Ruled out because the parent closure explicitly reserved this and a wrapper that changes a closed number is not "additive" by this Q's own H.
- **Treating a `RESOLVED` verdict here as authorization to wire the layer into the live gate's PASS/FAIL logic.** Genuinely tempting — a working wrapper invites "just gate on it." Ruled out because this Q is scoped to whether a *disclosure-only* version is buildable; changing what counts as a pass is a separate, heavier decision this Q does not make and has not evaluated the cost of.
- **Fitting a third family to satisfy `Q-NSURV-1`'s own "need a 3rd candidate" bar and quietly claiming that bar was met instead of the "principled reason" bar this Q actually uses.** Ruled out because `Q-NSURV-1`'s closure named two distinct paths (3rd candidate, or a principled reason to act on 2) — this Q takes the second path explicitly and must not blur the two in its own closure.
- **Loosening the 2.0pp reproduction tolerance if the first build attempt misses it.** A miss is informative (routes to Ambiguous-hold or the heavier-ADR branch), not a threshold to renegotiate after seeing the result (Known Trap #12).
- **Outcome-conditional D-test:** selecting which of the two candidates' artifacts to test the wrapper against based on which one is easier to reproduce. Both candidates run; both results report, regardless of outcome.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Wrapper reproduces both candidates' headline point estimates within 2.0pp, zero changes to `run_partition_mc`/`blocks_from_daily_pnl`, and emits the resampled bands additively | `INTEGRATE — draft the disclosure-only ADR (K-bank pattern), attach to future N-SURV verdicts; no core gate-logic touch` |
| `FALSIFIED` | Wrapper cannot reproduce either headline within tolerance without touching `run_partition_mc`/`blocks_from_daily_pnl` internals | `STOP — the additive/disclosure-only shape isn't achievable; a heavier System-domain ADR with its own blast-radius accounting is a separate, later decision, not opened here` |
| `AMBIGUOUS-HOLD` | Reproduces one candidate but not the other within tolerance | `ITERATE — re-test after a build attempt scoped to the failing candidate; re-test window: next session touching either candidate's N-SURV surface` |

---

## §7 — Execution plan

Self-executing (small, mechanical, single session) — no CC handoff needed.

- **Phase 0 — Rule-0 reads.** §0 above, already done.
- **Phase 1 — Build the wrapper.** New script under `lab/analysis/c1/nsurv_layer_design_2026-08-20/`, importing the two candidates' already-committed artifacts unchanged; compute resampled percentile bands from data already on disk (no fresh MC draw needed for c1; ORB-MNQ-1's N=50 draws are already in `nsurv_magnitude_probe_results.json`); assert bit-identical (within 2.0pp) reproduction of both headline numbers before reporting anything else.
- **Phase 2 — Verdict assertion.** Run the §6 gate against the reproduction-tolerance results; produce closure artifact per §9.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

`docs/briefs/pre-registration/Q-NSURV-2-verdict-preregistration.md` — frozen before Phase 1 runs.

Pre-registration commit hash: `<populated at pre-registration commit>`
Pre-registration date: 2026-08-20

---

## §9 — Closure record format

Per `references/closure_record.md`. `RESOLVED` → `docs/briefs/closures/Q-NSURV-2-closure-resolved.md`; `FALSIFIED` → `...-closure-falsified.md`; `AMBIGUOUS-HOLD` → `...-closure-ambiguous.md`.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm §0 anchors still resolve
git log -1 --format='%h' -- lab/discovery/prop_survivor_scoring.py            # expect 027a729
git log -1 --format='%h' -- docs/briefs/closures/Q-NSURV-1-closure-resolved.md # expect 983db58

# Confirm the mechanism claim (order-only resampling) still holds at HEAD
grep -n "def blocks_from_daily_pnl" lab/discovery/prop_survivor_scoring.py

# Confirm the disclosure-only precedent this Q's RESOLVED branch reuses still exists
grep -n "Disclosure-only\|disclosure-only" docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md

# Re-run the wrapper reproduction check (once Phase 1 lands)
python lab/analysis/c1/nsurv_layer_design_2026-08-20/run_wrapper_reproduction_check.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-NSURV-2-second-uncertainty-layer-design.md --type inquire

git log -1 --format='%h %ci' -- lab/discovery/prop_survivor_scoring.py
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-NSURV-1-closure-resolved.md

git log --oneline docs/briefs/pre-registration/Q-NSURV-2-verdict-preregistration.md
# Expected: pre-registration commit predates first Phase 1 script run
```

## Pre-Lock Checklist (DRAFT briefs only)

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [x] §5 forbidden moves are genuinely tempting, not strawmen
- [x] §6 gates have specific numerical triggers
- [ ] §8 pre-registration committed BEFORE Phase 1 runs — see companion file
- [x] §10 audit hooks are runnable commands
- [ ] Verification block executed and passing — owed once Phase 1 script exists
