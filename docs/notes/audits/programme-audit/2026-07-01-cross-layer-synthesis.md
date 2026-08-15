# Cross-layer synthesis — 5-week programme audit (2026-05-27 → 2026-07-01)

**Date:** 2026-07-01 · **Authors:** Joshua + Claude Code
**Nature:** deliberate cross-layer document, per the programme-audit coupling rules ("if a cross-layer synthesis is wanted, it is a separate document with its own discipline"). The two layer audits stand on their own evidence; this note is allowed to read both and rank actions across them. It creates no verdicts.

**Inputs:** `2026-07-01-methodology-belt-scoped-audit.md` (#2/#7) · `2026-07-01-meta-layer-audit-completion.md` (#1/#3/#4/#5/#6 → PROPOSED PROGRESSIVE) · `2026-07-01-portfolio-audit.md` (7/7 → PROPOSED STABLE, conditional).

---

## The one-paragraph read

The decision machinery is in the best shape it has ever been — pre-committed gates reversed a same-session GO, a survivorship leak was caught and RED-tested before anything depended on it, the belt prunes and rejects more than it installs, and zero falsifier thresholds drifted. But the machinery is now running on a shrinking reality feed: the operator's hand was removed from execution (correctly) with nothing yet automated behind it, the live halves of two lock-decision falsifier sets went dormant without acknowledgment, the free-data alpha search is empirically exhausted (~33 negative terminal dispositions vs 10 positive in five weeks, every "positive" an exoneration or an instrument), and the futures venue that everything now routes through has produced zero validated numbers because the vendor data isn't in the environment. **The programme's binding constraint is no longer discipline or ideas — it is contact with reality.** Every high-leverage action below buys back falsifiability; almost nothing else is worth an hour until they're done.

---

## Recommendations, ranked by leverage

**R1 — Re-arm the live falsifier surface (the critical path; everything else is downstream).**
Land the vendor CSVs (DJ30 Pepperstone export, DJ30 BAR_EXPORT bars, NAS100 export — exact paths in `lab/archive/bulenox_futures_remc_2026-07-01/NOTES.md`) → run the **Bulenox force-flat re-MC** and the **integer-contract re-MC** (both already named go-live gates; engine built, TDD'd, waiting) → then firm/automation confirmation and the TV→TradersPost chain. This single sequence simultaneously: restores a live falsifier channel (obj-#7), reopens the corroboration channel (obj-#3), converts the pivot's PENDING theory-comparison into evidence (obj-#6), and is the only route back to income. *Owner: operator (data export) → CC (runs). Target: material progress before 2026-08-08.*

**R2 — Formally SNAG-close the 5th-leg/expansion domain; stop paying for free-data loops.**
The loop record: 5th-leg ≈17–22 consecutive negative closures with 0 admissions (past threshold, closure never formalized); regime-detection 9 (already SNAG-closed); within-strategy-alpha 6–7 (closed by synthesis); external sourcing 0/69. Write the registry-grade domain closure with re-proposal bar = **exogenous/paid data or a genuinely new venue class** — matching the bars the individual closures already set. Until R1 completes, the marginal research hour spent on another free-data loop has a five-week empirical expected value of zero; the SNAG doctrine exists precisely for this moment. *Owner: operator ratifies; CC authors. One session.*

**R3 — Install falsifier back-propagation for retirement events (cheap governance patch, closes the audit's one real contradiction).**
The same retirement ADRs that graded green as disciplined prunes (obj-#2) silently darkened other ADRs' live falsifier limbs (obj-#7) — and the 06-30 ADR proves the failure class was understood, because it flags unaccruability for its own metric. Rule: any ADR retiring a venue/feed/role must sweep standing falsifiers for limbs referencing the retired surface and annotate each with a dated re-arm condition. Apply retroactively now to the five instances named in the portfolio audit §5.1 (2026-05-23 limbs 2–3; decompound §4 limb 1; decay-gate README; STATE.md Q-NAS-ECR-1; gold-gate tripwire). *Owner: CC drafts, operator ratifies. One session.*

**R4 — Make the prereg freeze mechanically verifiable: freeze-commit must precede results-commit.**
Flagged independently by five verifiers across both layers: several flagship preregs (Q-INCUMBENT, clean-vintage, Phase B §0.5) are same-commit self-attested, and one run commit edited frozen verdict logic (Q-ORB-FRIDAY-1 — anti-candidate direction, this time). The repo already contains the gold-standard pattern (`46f47d1` freeze → `913829b` run); make it the rule and add a sentinel/`check_brief` check: prereg artifact and results may not land in one commit; run commits may not modify frozen verdict logic. *Owner: operator ratifies rule; CC wires the check.*

**R5 — Put a mechanical tripwire on the go-dark interval's one unmonitored risk: the operator.**
The no-manual repair is structurally sound but one day old, policy-only, against a ≥4×-recurrent pattern, with the idle DXTrade account still credential-accessible, and nothing watches it until 2026-08-08. Weekly zero-fills attestation (export → assert 0 fills → log line), plus consider deleting stored credentials. Cheap, and it converts §4's "permanent-until-automation" from a promise into a measurement. *Owner: operator. Standing until the account lapses.*

**R6 — 2026-08-08 readiness sweep.**
The quarterly slate is now the programme's single functioning falsifier checkpoint (HOLD trigger + C0-revert + CFD-reopen review + deferred maximal-harvest + de-risk-frontier re-check all converge on it), and it is mechanically scheduled (cron + sentinel verified). But the sentinel's own Action-routed precondition findings (regime calendar [M]/[L] rows; Rule-2 trip-log starvation) have sat unremediated for 38 days. Fix them ≥1 week ahead; dry-run `time_to_pass.py --regime-check` on a fresh panel export. *Owner: CC, operator supplies export.*

**R7 — One hygiene PR for the HEAD-state skews the audit surfaced.**
(a) Silver closure: merge/re-land the NOT-ADMITTED stamp (on HEAD the brief still says CONDITIONALLY APPROVED while STATE.md says CLOSED-superseded) + the owed `rejected_candidates.md` annotation. (b) Shadow gold gate: retire or re-scope its unfireable tripwire; README owes two falsification acknowledgments. (c) CBOE orphan panels: annotate or remove. (d) DRAFT-HOLD lift procedure: one paragraph codifying what PR #264's approval comment already did. *Owner: CC. One PR.*

**R8 — Reconcile the repository-visibility posture (operator ground truth beat the docs).**
GitHub shows the repo **private** (operator-verified 2026-07-01), while the 2026-07-01 py-port ADR's §0 asserts "Repo is public" and CLAUDE.md's posture section still opens "This repo is public." Confirm the timeline via GitHub's audit log; addendum-correct the ADR premise (the untracking decision survives; the accepted "history exposure" may never have occurred, since the port first landed 17 days *after* PRIVATIZE-ALL); fix CLAUDE.md; re-scope the parameter-transcription Forward question as contingent-on-re-publicization. Note for the belt: this failure class (M-12 / verify-source) appeared *inside an ADR's §0 verification block* — and this audit's own first-pass agent repeated it, trusting doc text as platform fact. Platform-state claims in §0 anchors need a platform-side check, not a repo-side grep. *Owner: operator (audit log + posture decision), CC (doc fixes).*

---

## Visible restraint (decided NOT to act on)

- **No change to the locked four, allocations, `dd_protection`, or the HOLD.** The de-risk frontier question reopened by the clean-vintage correction is scheduled for 2026-08-08; pulling it forward would violate the gated-re-MC prioritization discipline for zero new information.
- **No new alpha loops of any kind pre-R1**, including "just one" exogenous-data probe: Q-ORB-VIXTS-1 and the deferred maximal-harvest stay HELD to their existing dates.
- **No formal FXIFY account closure** — idle-not-closed was an explicit operator decision preserving free optionality; R5 monitors it instead.
- **No history purge / no re-privatization panic under R8** — the exposure analysis got *safer* under the corrected premise, not more dangerous.

## Watch list (dated)

| Item | Where | Date |
|---|---|---|
| Belt-growth magnitude recedes? | meta #2 (sibling) | ≈2026-09 audit |
| D4 add-back metric stability | meta #4 | ≈2026-09 audit |
| Operator-override frequency | meta #5 | ≈2026-09 audit |
| Rule-2 trip-log liveness | meta #7 (sibling) | ≈2026-12 |
| First execution of the HOLD's §4 trigger | obj #4/#7 | 2026-08-08 |
| Pivot go-live gates (re-MCs) run before any live futures claim on the anchor | obj #4/#6 | before go-live |
| 90-day methodology-archive review gate | standing | 2026-07-29 |
| Q7-close audit | standing | 2026-07-19 |
