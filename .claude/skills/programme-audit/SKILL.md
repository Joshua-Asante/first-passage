---
name: programme-audit
description: Use when a methodology or 4-strategy portfolio shows degeneration signals — belt-patches without independent corroboration, belt that only grows never prunes, falsifier thresholds drifting toward "we'd never hit this", methodology invoked to rationalize a decision already made, SNAG pattern (multiple null/ambiguous loops same domain), cross-layer contamination (methodology citing portfolio evidence or vice versa), or a negative heuristic crossed without repair. Also fires on scheduled cadence — quarterly for meta-layer methodologies (The Algorithm, INQHIORI, OODA, brief-authoring), semi-annual or triggered for the portfolio. Loads the Programme Audit Protocol — seven diagnostic questions, five disposition verdicts (Progressive / Stable / Degenerating / Falsified / Ambiguous), two-layer architecture rules. Hand off to inqhiori for follow-up falsifiable-H investigations, brief-authoring for audit artifact structure, prop-firm-challenge for live-ops facts.
---

# Programme Audit Protocol

This skill applies the Lakatos research-programmes diagnostic to Joshua's methodologies (meta layer) and the 4-strategy portfolio (object layer). It exists because methodologies and portfolios can degenerate silently — accumulating belt-patches without independent corroboration, drifting falsifier thresholds, or substituting layer evidence — and the cost of catching degeneration late is high. The first proof-of-value (2026-05-12) was the audit producing surplus content: the strategy-vs-instrument correlation finding surfaced as a byproduct of routine portfolio audit, falsifying an implicit belt assumption. That session is the canonical worked example.

**Source-of-truth hierarchy:** this SKILL.md body (discipline rules) → ADR-NNN-programme-audit-protocol.md when locked (canonical framework definition) → audit artifacts in `docs/notes/audits/programme-audit/` (lineage). When this skill disagrees with a more recent audit that demonstrably worked, the audit wins and the skill needs updating — flag this.

**Boundary with sibling skills:**

- `inqhiori` — investigates specific falsifiable Hs. The audit may spawn INQHIORI loops as follow-ups; the audit itself does not run them.
- `ooda-loop` — tactical/tempo decisions. Not relevant to programme audits except as a methodology being audited.
- `brief-authoring` — provides the audit-note template. This skill specifies *what* the audit examines; brief-authoring specifies *how* the artifact is structured.
- `prop-firm-challenge` — provides live-ops facts (PF, DD, edge-captured ratio, dd_protection state) that the portfolio-layer audit consumes. Audit does not modify live ops.
- `pinescript-v6` — strategy code is the object of portfolio-layer audits, never modified by the audit itself.

---

## Trigger conditions (degeneration signals primary; cadence secondary)

The skill fires **immediately** on any of the following degeneration signals — calendar cadence is a backstop, not the primary trigger:

1. **Belt-patches without independent corroboration.** A parameter, filter, gate, or constant was changed to accommodate an observation, but no independent evidence (separate data, separate test, separate mechanism) supports the change. The Q-DDP-1 → ADR override is the canonical edge case worth re-examining each audit.
2. **Belt that only grows, never prunes.** Adds outpace removes across consecutive audit windows. Healthy programmes prune as evidence converges.
3. **Falsifier thresholds drifting toward "we'd never hit this anyway."** Either explicit threshold revisions or implicit reinterpretation that softens triggers.
4. **Methodology invoked to rationalize a decision already made.** The audit was authored to justify a conclusion, not to test it. Tell: the disposition is written before the evidence is assembled.
5. **SNAG pattern.** Multiple null/ambiguous loops in the same domain — DJ30 Q-DJ30-1/2/3 (all null/ambiguous/null) is the canonical anchor. SNAG budget exhaustion is the right response, not infinite-patching.
6. **Cross-layer contamination.** Methodology audit verdicts cite portfolio performance as evidence, or vice versa. The two layers corroborate each other in the long run; they do not substitute in any given cycle.
7. **Negative heuristic crossed without repair.** A forbidden move appears in recent work and is tolerated rather than removed.

**Scheduled cadence (backstop):**

- **Methodologies:** quarterly. Cheap audits (no live data dependency); rhythm matters more than depth.
- **Portfolio:** semi-annual baseline, triggered between cycles on degeneration signals or on accumulation of ≥6mo new live data. Portfolio audits are expensive (require re-MC, edge-captured analysis); calendar-forced audits without new evidence are ceremony.

---

## Two-layer architecture (load-bearing)

The most important structural rule. Methodologies and the portfolio are *nested* research programmes, not the same programme:

- **Meta layer (methodologies):** The Algorithm, INQHIORI, OODA, brief-authoring, programme-audit itself. Hard cores are *epistemic moves*. They generate decisions.
- **Object layer (portfolio):** the 4-strategy locked portfolio, allocations, dd_protection, firm deployments. Hard core is *empirical claims about market behavior and operational capacity*. It is the *output* of methodology layer.

**Coupling rules:**

1. Methodology verdicts do not automatically promote to portfolio verdicts. INQHIORI being progressive does not mean Aegis is progressive. They are judged on their own evidence.
2. Portfolio verdicts can trigger methodology audits but not the reverse. A failing portfolio is evidence about the methodology that built it; a thriving methodology is not evidence the portfolio still holds.
3. Cross-layer contamination is itself a degeneration signal (see trigger #6 above).

**Operational consequence:** when authoring a portfolio audit, do not reference methodology audit verdicts. When authoring a methodology audit, do not cite portfolio performance. Each audit stands on its own evidence base. If a future cross-layer synthesis is wanted, it is a separate document with its own discipline.

---

## The seven diagnostic questions

Every audit, regardless of layer, runs these seven questions. The phrasing differs slightly between layers (meta-layer asks about epistemic moves; object-layer asks about empirical claims) but the structure is identical.

**1. Hard core integrity.** Has the hard core been preserved across recent uses, or quietly violated under the programme's name?

- Meta example: running INQHIORI without a falsifiable H, then calling the output an INQHIORI finding.
- Object example: a locked strategy modified outside the formal version-lock cycle; dd_protection overridden tactically without ADR.

**2. Belt churn balance.** How many belt items added vs. removed since the last audit? Healthy programmes prune as evidence converges. Belts that only grow accumulate ceremony.

- Tally adds and removes. Net-positive growth across consecutive audits is a yellow flag; net-positive growth across ≥3 consecutive audits is a red flag.

**3. Progressive evidence.** Has the programme produced predicted-and-corroborated results in the audit window? Concrete examples required — predictions made *before* outcomes, then confirmed.

- Meta example: Aegis short-mirror falsification (INQHIORI predicted asymmetry, tested, confirmed).
- Object example: live PF within MC band; dd_protection firing correctly on the right regime; a tail event survived as projected.

**4. Degeneration evidence.** Has the programme been used to patch anomalies after the fact without independent support? Belt-patches existing only to rescue prior conclusions are the canonical signal.

- The diagnostic: when belt items were last revised, was the revision *predicted* by an independent model, or *rationalized* after the fact?

**5. Boundary respected.** Have moves the negative heuristic forbids appeared in recent work? If so, was the boundary repaired (move removed, lesson captured) or eroded (move tolerated, becoming new normal)?

- Meta example: a methodology used for a decision its negative heuristic forbids (INQHIORI on tactical, OODA on structural).
- Object example: a regime overlay built on physical facts; a rejected candidate quietly re-proposed without new mechanism evidence.

**6. Theory-comparison performance.** Where competing options existed, did the chosen option outperform the unchosen ones in subsequent evidence? Track the counterfactuals.

- Meta example: when the tiebreaker routed a question to INQHIORI vs OODA, did the chosen routing produce the better outcome?
- Object example: when allocation A was chosen over B, did A outperform B in subsequent live evidence?

**7. Falsifier check.** Are the programme's pre-committed falsifiers still in force at their original thresholds? Have any drifted toward "we'd never hit this anyway"?

- Verify by grep / diff against original locked values. Drift is mechanical to detect and disqualifying when found.

---

## Five disposition verdicts

Each audit cycle ends with one verdict per programme:

- **Progressive** — earning its existence; predictions corroborated; continue.
- **Stable** — delivering value but not generating new insight in the audit window; continue with watch flag, re-examine cadence.
- **Degenerating** — belt-patches without independent corroboration, or net-positive belt growth across consecutive audits, or methodology being used to rationalize. Intervene: prune belt, refactor procedures, or escalate to replacement.
- **Falsified** — pre-committed falsifier triggered or hard-core proposition failed. Abandon or fundamentally restructure the programme.
- **Ambiguous** — insufficient data for a verdict. Document explicitly and re-test at next cycle. AMBIGUOUS is not "we'll wait longer" — it is a verdict, dated, with re-test conditions named.

---

## Audit artifact structure (handoff to brief-authoring)

Programme audits produce an audit note in `docs/notes/audits/programme-audit/YYYY-MM-DD-<layer>-audit.md`. The artifact follows `references/audit_note.md` from brief-authoring with these audit-specific additions:

- §1 Context lists the programme being audited, the audit window (start date, end date), and the trigger (scheduled cadence vs specific degeneration signal).
- §3 (audit-specific) contains the seven diagnostic questions, each with a specific answer grounded in evidence anchors (commit hashes, file paths, specific numbers).
- §4 contains the disposition verdict with explicit reasoning.
- §5 lists any spawned follow-ups (INQHIORI loops opened, belt-prune ADRs queued, falsifier checks needed).
- §10 audit hooks runnable at the next cycle.

---

## Known traps

Failure modes that recur, in order of frequency:

**1. Audit authored to confirm a verdict already held.** The audit reads as justification for "we're doing fine" or "we need to change X" — predetermined. Repair: separate the evidence assembly from the verdict assignment. Write §3 (seven questions, with evidence) before writing §4 (verdict). If the verdict was decided before evidence, the audit is theater.

**2. Cross-layer leakage.** Methodology audit cites portfolio P&L. Portfolio audit cites methodology rigor. Repair: re-author with layer discipline enforced — no cross-layer citations.

**3. AMBIGUOUS used as "we don't want to decide."** AMBIGUOUS is a verdict requiring named re-test conditions. "We'll know more later" is not AMBIGUOUS — it is no verdict at all. Repair: name the specific evidence that would resolve the ambiguity and the date by which it should be available.

**4. Belt-churn metrics absent.** The audit notes "we made some changes" without counting adds and removes. Repair: explicit tally. The number matters because trend across audits matters.

**5. Falsifier check skipped.** Audit references that falsifiers exist without verifying current threshold values match locked values. Repair: grep / diff against the locked ADR; report the diff.

**6. Audit cadence ceremony.** Quarterly audit run on schedule when no new evidence has accumulated; produces "stable, no changes" with no real examination. Repair: collapse to a one-line status update; reserve full audit for cycles where new evidence or degeneration signals exist.

**7. Audit triggered by degeneration signal but spawned no follow-up action.** Degeneration was identified, recorded, and then nothing changed. Repair: every Degenerating verdict requires at least one named action (belt-prune ADR, INQHIORI loop, restructure proposal) with an owner and date.

---

## Discipline check summary

Run before declaring an audit complete:

```
[ ] Seven diagnostic questions answered, each with evidence anchor
[ ] Belt churn balance counted (adds vs removes, numbers explicit)
[ ] Falsifier check executed (grep / diff against locked thresholds)
[ ] Cross-layer contamination check passed (no cross-citations)
[ ] Disposition verdict assigned (one of five), with reasoning
[ ] If Degenerating or Falsified, follow-up actions named with owner and date
[ ] If Ambiguous, re-test conditions and target date named
[ ] §10 audit hooks runnable at next cycle
```

---

## Reference files (to be authored as audit history accumulates)

- `references/audit_template_methodology.md` — meta-layer audit template (when first methodology audit completes)
- `references/audit_template_portfolio.md` — object-layer audit template (when first portfolio audit completes)
- `references/degeneration_signals.md` — expanded catalog of degeneration signals as new ones are discovered in practice

Until these reference files are authored from lived audit experience, follow the structure in this SKILL.md body directly. The first two completed audits become the canonical templates.

---

## Worked example (canonical anchor)

**2026-05-12 portfolio audit, applying the seven diagnostic questions to the 4-strategy portfolio.** Audit produced surplus content as a byproduct: question 1 (hard core integrity) led to examining whether the implicit "instrument correlation ≈ strategy correlation" assumption had been preserved. Direct evidence from the existing locked portfolio (DJ30 / NAS strategy-level correlation materially lower than instrument-level correlation would predict) was inconsistent with the assumption. This was not predicted by the audit; it surfaced as a consequence of asking the question rigorously.

Outcome: belt-level falsification of an implicit assumption; Notice log captured; Pre-Q Q-CORR-1.1 (Guardian-on-Silver) opened to test the corrected belt. The audit also produced ADR-NNN (prop-firm-capital falsifiers) as a parallel artifact — the methodology was visibly producing belt-level findings and falsifier infrastructure in a single session.

This single example demonstrates the value of the protocol better than any pre-authored justification could. Treat it as the canonical anchor — replicate the discipline, not the specific finding.
