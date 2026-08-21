# Audit Note — 2026-08-20 external-mechanism/framework-mapping move-class (meta layer, triggered)

**Audit ID:** AUDIT-2026-08-20-external-mapping-move-class
**Layer:** meta (methodology). The object audited is not a chartered methodology but an **emergent, repeated epistemic move**: import an external framework or peer firm's mechanism, map it onto `generate→evaluate→deploy→measure→update`, adversarially stress-test the result. Performed three times in three calendar days. Not the portfolio.
**Date:** 2026-08-20 · **Window:** 2026-08-18 → 2026-08-20 (the move-class's entire lifetime — this is its **first-ever audit**, so there is no prior-cycle baseline to compare against)
**Triggered by:** operator direction ("run the programme audit"), following [`N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md`](../../notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md) §4, which explicitly escalated from "flag for a future audit" to "run one now" after a third DROP under the most favorable conditions of the three.
**Not a scheduled quarterly.** This is a triggered audit of a specific move-class, like `2026-08-15-governance-belt-meta-audit.md`; it has no fixed cadence of its own and does not feed any existing quarterly tally.
**Method:** single-session, evidence-before-verdict — §3 assembled and the Rule-2 budget calculation executed before §4 was drafted. Primary evidence is the three Notices' own committed content plus this session's own workflow journals (`wf_882d7e37-327`, `wf_787ef978-ad8`); load-bearing citations were re-verified directly against primary repo files this session (see §0), not trusted from nested summaries alone.

**Cross-layer discipline:** no portfolio evidence (PF, DD, P&L, fill, allocation) is cited below. `Q-TRAINKILL-1` / `Q-COMPOSE-1` are cited as **methodology-layer** research findings (statistical-power and composition-test results), never as object-layer portfolio performance.

---

## Correction (2026-08-20, same session, post-close)

**§3.4's central finding rested on a false premise, discovered same session via a direct Glob/file-existence check this audit itself had not run.** The original §3.4 (and §0 row 6, and §5 action 2 below) claimed `Q-TRAINKILL-2` — the successor `Q-TRAINKILL-1`'s closure named — "remains named, not opened, as of this audit." That claim was sourced from the TK1 closure's own Iterate block ("Successor named Q-TRAINKILL-2 — not opened"), read as current state without checking whether it had *since* been opened. It had: `docs/briefs/Q-TRAINKILL-2-bounded-recovery-alt-dgp.md` and `docs/briefs/Q-TRAINKILL-3-neg-vs-dep-discriminator.md` (plus their pre-registrations and closures) exist on disk. Both were opened, executed, and closed **the same day as TK1, 2026-08-18** — before any of this program-week's three external-mapping instances ran. `TK2` closed `AMBIGUOUS-HOLD` (neither named alternate DGP was discriminated). `TK3` closed `AMBIGUOUS-HOLD` → **`STOP`**, with an explicit re-proposal bar: a new panel (fresh data, operator GO + K) or an operator election naming `NEG-FAMILIES` or `KILLS-INFORMATIVE-DEP` as working-model without claiming the other falsified.

**Consequence: there was no cheap, unexploited alternative sitting idle while instances 2 and 3 ran.** That specific thread had already been run to a legitimate, properly-gated stop. §3.4's framing — "the pipeline's own records kept surfacing a cheaper answer the search never once itself pursued" — is **retracted as stated**. What actually happened is narrower and less damning on this specific axis: this program-week's external-search instances failed to notice that the object-level question they kept citing as "the real next step" had *already been closed out* through the pipeline's own proper channel, days before instance 3 (and hours-to-a-day before instance 2) ever ran. Citing a stale "next step" is a Rule-0 failure of a different, milder shape than "ignored a live cheap win" — it does not, on its own, sustain a Degenerating reading.

**§4's disposition is reduced, not overturned.** Two of the seven diagnostics were independent of this error and stand unchanged: **§3.2** (belt churn — 5 adds, 0 removes, still true) and **§3.7** (the Rule-2 STRATEGIC cap — 3 constituent OUTER investigations, none formally declared as such going in — still true, and arguably now the single load-bearing finding rather than one of several). §3.1's LoR-declaration gap also stands, and is *compounded* by this correction, not contradicted by it (see next paragraph). §3.5 (GREEN, boundary respected) and §3.6 (Quantopian precedent) are both unaffected either way. The verdict **`DEGENERATING` is retained**, but on the narrower basis of §3.2 + §3.7 (and the LoR gap), not on a "cheap win ignored" narrative that turns out to be false.

**A new, more interesting finding this correction surfaces.** The TK1 closure document itself carries an internal inconsistency — its Iterate block states "Successor named Q-TRAINKILL-2 — not opened" while its own §3a, four sections later in the *same file*, states "Q-TRAINKILL-2 and Q-TRAINKILL-3 (both closed in this PR, both citing this closure as parent) inherited this packet's mechanism unchanged." Both this session's peer-firm workflow (whose stress-test agents cited the closure's Iterate-block framing as current fact) **and this audit's own first pass** read past that contradiction without resolving it against an actual file-existence check — exactly the `lesson_verify_content_not_path_or_id` / `lesson_corrections_land_where_read` failure class this repo has logged before, firing live, inside the audit meant to be checking for exactly this kind of thing. This is now folded into §3.1's already-identified gap (investigations running without declared LoR/Rule-2 headers) as a second, concrete instance of the same underlying weakness: **this move-class's own Rule-0 discipline has a real, demonstrated hole**, not merely a formatting gap.

**§5 action 2 is withdrawn as moot** (there is nothing to "decide on opening" — TK1→TK2→TK3 already ran to `STOP`) and replaced below. **§5 action 3's Rule-2 trip-log entry** needs its own correction, made directly in `rule-2-trip-log.md`.

---

## §0 — Rule 0 reads (verified this session)

| # | Source | Verification | What it establishes |
|---|---|---|---|
| 1 | [`N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`](../../notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md) | Full read, this session | Instance 1. `DROP` on domain-conflation, citing the GRAND ADR's own §3 alternatives ruling. |
| 2 | [`N-2026-08-20-anthropic-training-principles-pipeline-mapping.md`](../../notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md) | Authored this session | Instance 2. 0/6 candidates survived; both standing guardrails (domain-conflation, evidentiary-substitution) first stated here. |
| 3 | [`N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md`](../../notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md) | Authored this session | Instance 3. 0/2 candidates survived despite the highest structural-fit score measured (Numerai, 5/5); both guardrails sharpened, not merely re-triggered. |
| 4 | [`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md`](../../../adr/2026-08-09-grand-tier-quintessentials-binding.md) §3 | Direct grep-read this session (not via nested summary) | §3 row 1, verbatim: "Fold the Quintessentials into The Algorithm as additional operators — Distinct object class: Subtract removes *pursuits*; Delete removes *parts/requirements* within surviving pursuits. Merging them conflates exactly what the §2.4 domain guard exists to keep separate." This is instance 1's actual ruling authority. |
| 5 | [`docs/adr/2026-06-16-rule-2-budget-before-acting.md`](../../../adr/2026-06-16-rule-2-budget-before-acting.md) | Direct grep-read this session | Verbatim: "STRATEGIC (funding/kill-continue/programme-tier): **3 constituent OUTER investigations. No self-extension.**" and "Extension authority mirrors the three-loop binding… OUTER/STRATEGIC extension is owner adjudication or a re-audit — never self-granted." Load-bearing for §3.7 below. |
| 6 | [`docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md`](../../../briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md) | Full read this session | `AMBIGUOUS-HOLD`, closed 2026-08-18. Successor **named Q-TRAINKILL-2 — not opened** per the closure's own Iterate block. ⚠ **This row is itself the source of the correction above — the closure's own §3a (not caught on first read) says TK2/TK3 were already closed same-PR; verified by direct Glob this session: `docs/briefs/Q-TRAINKILL-2-*.md` and `Q-TRAINKILL-3-*.md` both exist, both closed 2026-08-18.** See "Correction" section above. |
| 7 | `lab/discovery/ic_similarity.py`, `lab/research_utils/breadth.py`, `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`, `docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`, `docs/adr/2026-08-13-dedup-first-before-new-work.md`, `docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md`, `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` | Existence verified directly this session (all 8 files confirmed present before citation in instance 3); content sourced from instance-3's stress-test agents, which quoted specific line-level detail (docstrings, forbidden-move text) internally consistent across independent agents | Instance 3's core evidence base — see that Notice's §3 for the full adversarial record. |
| 8 | [`docs/notes/audits/rule-2-trip-log.md`](../rule-2-trip-log.md) | Full read this session | One row, a declared OUTER non-trip baseline (2026-06-16). Zero STRATEGIC-tier entries to date. This audit adds the first — see §5 action 3. |
| 9 | `docs/notes/audits/programme-audit/2026-08-15-governance-belt-meta-audit.md` | Full read this session | Structural precedent for this audit's format (§0/§3/§4/§5/§10, per-question grading, executed-not-asserted falsifier check). No content borrowed as evidence for this audit's subject. |

---

## §3 — The seven diagnostics

### §3.1 Hard-core integrity

The implicit hard core of this move-class, as stated across all three Notices: **an external source is worth importing only if, after adversarial review, it supplies a concrete mechanism at one named pipeline stage that the pipeline hasn't already reinvented, feeding the existing evidentiary gates rather than replacing them.**

**Preserved:** no locked surface was touched by any of the three instances — no Pine, no `dd_protection` constant, no `core/`. Both guardrails were applied consistently and were never weakened to let a candidate through (§3.5 below).

**A real gap, not a violation:** none of the three instances was run under a declared Loop-of-Record or Rule-2 budget statement. Per `inqhiori-canon.md` §14, work of this shape — structural, low-reversibility-adjacent (each instance consumed real multi-agent budget and produced a routing verdict), statistical in its adversarial-verification method — is squarely **OUTER**-loop shaped. None of the three carried an INQHIORI Sources-Read block or D-S-A pre-Q gate header; each was authored under the lighter Notice-log convention ("Notice-phase artifacts are lightweight… the discipline of a falsifier comes at the Inquire phase, not here" — `notice_log.md`). That convention is legitimate for a single raw observation. It is a poor fit for three multi-agent research-and-verify cycles that, in aggregate, are exactly what Rule 2's OUTER/STRATEGIC tiers exist to budget. **The move-class accumulated OUTER-investigation weight without ever declaring itself as OUTER-investigation work**, which is why its own budget cap was never consciously in view until this audit computed it retroactively (§3.7).

**Grade: YELLOW.** No locked-surface violation; a real process gap in self-classification.

### §3.2 Belt churn — numbers

Belt items (auxiliary devices protecting the hard core / doing the actual screening) added across the three instances, this move-class's entire lifetime:

| # | Item | Introduced | Type |
|---|---|---|---|
| 1 | Guardrail #1 — domain-conflation (generalized from the GRAND/Quintessentials precedent) | Instance 2 | ADD |
| 2 | Guardrail #2 — evidentiary-substitution (generalized from the Iran-Hormuz lesson) | Instance 2 | ADD |
| 3 | Three-lens adversarial stress-test procedure (feasibility / evidentiary / domain-conflation) | Instance 2 | ADD |
| 4 | Guardrail #1 sharpened — "altitude/stage-reach conflation" (a mechanism's *inputs or outputs*, not just its label, can conflate stages) | Instance 3 | ADD |
| 5 | Guardrail #2 sharpened — "budget-starvation is a kill by another name" (disclosed-not-gating doesn't neutralize substitution risk if it's the sole input steering a fixed budget) | Instance 3 | ADD |

**Removed: 0.**

**Tally: 5 adds / 0 removes across 3 instances in 3 calendar days.** This is the move-class's first measurement, so the "≥3 consecutive audits" red-flag threshold from the skill's own trigger list does not literally apply yet — but the *within-window* trend is unambiguous: every single instance added to the belt and none pruned or simplified it. Unlike the 08-15 governance-belt audit (37:11, an *improving* 3.4:1 ratio with a documented counterweight), there is no counterweight to record here.

**Grade: RED**, with the explicit caveat that this is a first-cycle measurement — the next audit of this move-class (if a fourth instance is ever GO'd) should show at least one item consolidated or retired, not a sixth pure add.

### §3.3 Progressive evidence

**Real, but narrow.** A genuine predicted-then-tested episode exists: instance 3's own guardrail text carried an explicit ex-ante carve-out ("a peer firm's portfolio-construction technique is closer to a harvestable seed than to an abstract framework") — a stated reason to expect this instance had the best odds of any of the three. The prediction was tested, not merely asserted: Numerai scored the only 5/5 structural fit measured, and its mechanism was still killed 0/2. That is a real, dated, falsifiable prediction (this instance is the exercise's best shot) cleanly disconfirmed on the optimistic reading and confirmed on the pessimistic one (the guardrails bind even in the best case). Guardrail #1 and #2, once stated in instance 2, correctly predicted the failure mode of every one of the 8 total candidates across instances 2 and 3 — a genuine, repeated, independent confirmation of the guardrails' discriminating power.

**Absent:** none of this is progressive evidence about the *object-level* question the move-class exists to answer — why regularities die at conversion (H1/H2/H3), or whether an external mechanism can fix it. The progressive content is entirely about the **belt's own predictive accuracy**, not about the market or the pipeline's actual bottleneck. One partial exception, credited fairly: instance 3 surfaced a genuinely new, still-open, testable reframing of the bottleneck (the "individually-sufficient-signal architecture" question — does the pipeline's total absence of a portfolio-combination layer contribute to zero-ever conversion, independent of H1/H2/H3?). That is real novel content, though it was not what the search was chartered to find, and it remains untested.

**Grade: YELLOW.**

### §3.4 Degeneration evidence — the central finding

> ⚠ **See the "Correction (2026-08-20, same session, post-close)" block above before reading
> this section.** The "cheap alternative sat unopened" claim below is **retracted** —
> `Q-TRAINKILL-2`/`-3` were already run to `STOP` on 2026-08-18. Left as originally written for
> the audit trail; do not cite this section's framing as current.

**Zero of 8 candidate mechanisms, across all three instances, survived adversarial stress-test.** That number alone is not damning — a well-functioning skeptical process can legitimately kill everything it's shown. What makes this Degenerating rather than merely unlucky is what the move-class's *own adversarial output* kept independently pointing at instead:

- Instance 3's feasibility lens on candidate 1 read `Q-TRAINKILL-1`'s own closure directly and found it: "**the prescribed, already-named next step (successor Q-TRAINKILL-2, not yet opened) is a narrow CI-recovery task on 7 specifically listed BOUNDED rows… The candidate mechanism advances none of this — it proposes an unrelated new instrument instead of the pipeline's own already-designed, cheaper next step.**"
- Instance 2's own mapping work never named Q-TRAINKILL-2 at all — the pipeline's actual cheapest, already-scoped next move on the actual named bottleneck was invisible to the *first* external-search attempt and only surfaced, unprompted, when the *second* attempt's adversarial layer went and read the closure itself.

**This is the pattern that matters:** across two independent instances (2 and 3), spending real multi-agent research budget searching *outward* for a borrowable mechanism, the pipeline's *own* records kept surfacing a cheaper, already-authorized-in-shape, already-scoped answer — sitting unopened the entire time, never once itself the object of the search. Verified directly this session (§0 row 6): `Q-TRAINKILL-2` remains **named, not opened**, as of this audit, exactly as it was before instance 1 ever ran.

Separately, and independently corroborated (not merely asserted): the belt refinements themselves (§3.2 items 4–5) were checked against fresh, specific, freshly-read repo evidence at the time they were made (the Stage-8 ADR's own Forbidden Move list; the 2026-08-19 breadth-revival spec's explicit, one-day-old rejection of "Approach B"), not invented to rescue a foregone conclusion — so this is **not** classic ad hoc belt-patching in the narrow Lakatosian sense. The degeneration is at a higher altitude: **the move-class as a whole is producing an ever-more-sophisticated apparatus for explaining why imported mechanisms fail, while the actual object-level problem it exists to unstick has advanced by exactly one open, untested reframing and zero deployed mechanisms — and the pipeline's own cheaper, correct next step went unexecuted throughout.**

**Grade: RED.**

### §3.5 Boundary respected

The negative heuristic here — the two guardrails — was tested against 8 total candidates across instances 2 and 3. **Every single crossing was caught and killed; none was tolerated, softened, or waved through.** 6/8 candidates failed domain-conflation, 7/8 failed evidentiary-substitution, and no candidate that tripped either guardrail was allowed to survive on the strength of its feasibility case alone. Instance 3's stress-test explicitly weighed the harvest-channel carve-out fairly (rather than either dismissing it or using it to excuse a real conflation) on both candidates and still returned `risk=true` on the merits each time.

**Grade: GREEN.** The enforcement layer is functioning with real integrity — this is not a case of a boundary quietly eroding. The failure this audit records is upstream of the boundary, not at it.

### §3.6 Theory-comparison performance

No true counterfactual was run (only Numerai was deep-dived; the four runners-up were scored but not pursued). One real, unplanned natural experiment exists in the survey data itself: **Quantopian actually built and ran, on real capital, a mechanism structurally adjacent to what this move-class was searching for** — a named "Alpha Combination" pipeline stage between discovery and portfolio construction. The business failed anyway (shut down 2020). This is sobering, independent evidence bearing on the whole search direction, not just on this session's specific candidates: even a company that built the general shape of "combine many weak signals into something fundable" did not survive on that alone.

**Grade: YELLOW**, leaning RED on what it implies for continuing the search direction as currently framed.

### §3.7 Falsifier check — executed, not asserted

**This move-class has a real, pre-existing, doctrine-level falsifier that was never consciously invoked until this audit computed it: Rule 2's STRATEGIC budget.**

Per `docs/adr/2026-06-16-rule-2-budget-before-acting.md` (verified verbatim, §0 row 5): a programme/kill-continue-tier question is capped at **3 constituent OUTER investigations, no self-extension** — extension requires **owner adjudication or a re-audit**, never self-granted. Reading the three instances as three constituent OUTER investigations of one implicit STRATEGIC-tier question ("can an external framework or firm's mechanism close the conversion-death bottleneck?") — which is the correct reading per §3.1's own finding that each instance carried OUTER-investigation weight without declaring it — **the cap is now exactly consumed: 3 of 3, with zero of them ever formally opened as budgeted OUTER work in the first place.**

No threshold drifted (the cap has never been touched or reinterpreted — it simply was never applied). The defect is reachability, not drift: work of a shape and cost the cap was built to bound accumulated three full instances deep before the cap was ever checked against it. This is the identical failure *shape* (not the same cap) as the gate-reachability lesson class already logged repeatedly in this repo (`lesson_gate_reachability_preregistration`, 5+ prior firings per project memory) — a control that exists on paper but was never wired to the thing it was meant to bound.

**Grade: RED.**

---

## §4 — Disposition

### Verdict: **DEGENERATING**

Five of seven diagnostics graded RED or RED-leaning (§3.2, §3.4, §3.6, §3.7 outright; §3.1 a real process gap); one YELLOW with only narrow/self-referential progressive content (§3.3); one clean GREEN (§3.5). Per the skill's own disposition rule, a Degenerating verdict requires belt-patches without independent corroboration **or** net-positive belt growth **or** methodology invoked to rationalize a decision already made **or** a SNAG pattern — this audit finds the SNAG pattern (three DROPs, same domain, all cited by name) **and** net-positive, un-pruned belt growth (§3.2) **and**, as the load-bearing finding, a doctrine-level budget cap that has been silently exceeded (§3.7) while a cheaper, already-scoped, correct alternative sat unexecuted throughout (§3.4).

**What the verdict is not.** This is not a verdict that the guardrails are broken, or that adversarial review was performed sloppily — §3.5 is clean, and §3.4's own central finding was *surfaced by the move-class's own adversarial layer*, not by an external critic. The belt-refinements were independently corroborated, not invented to rescue a conclusion (§3.4). Peer-firm and external-framework research also produced real, honestly-reported negative knowledge worth keeping (Numerai's own True Contribution metric having near-zero persistence one layer down from MMC; Quantopian's real-world precedent). **The programme is not failing at rigor. It is failing to notice, across three full cycles, that its own output kept pointing at a cheaper question it wasn't asking.**

**Scope.** This verdict applies to the external-mechanism/framework-mapping move-class as practiced this week. It says nothing about INQHIORI, The Algorithm, OODA, or any other standing methodology, and nothing about the 4-strategy portfolio — no object-layer evidence was consulted (see cross-layer discipline statement above).

---

## §5 — Actions (every Degenerating verdict names at least one, with owner and date)

1. **Stop further instances of this move-class without a fresh, explicit owner GO.** The Rule-2 STRATEGIC cap (3 constituent OUTER investigations) is exactly consumed; per the ADR's own text, extension is "owner adjudication or a re-audit — never self-granted." This audit is that re-audit; it does not itself grant an extension. **Owner: operator. Due: before any fourth attempt, event-gated not calendar-gated.**
2. ~~Decide on Q-TRAINKILL-2~~ — **withdrawn as moot** (see "Correction (2026-08-20, same session, post-close)" above). `Q-TRAINKILL-2`/`-3` already ran to `STOP` on 2026-08-18 with their own re-proposal bar (a new panel — fresh data, operator GO + K — or an operator election between `NEG-FAMILIES`/`KILLS-INFORMATIVE-DEP`). **Replacement:** there is no cheap pending alternative on this specific object-level question left to redirect to. If the operator wants further progress on the conversion-death bottleneck at all, the honest menu is: (a) fund a new TRAINKILL panel, (b) make the TRAINKILL operator election, (c) pursue a genuinely different object-level angle — not another external-framework search, since the STRATEGIC cap for that move-class is spent (action 1) — or (d) accept the bottleneck's current state and direct attention elsewhere. This audit does not recommend among (a)–(d); that choice belongs to the operator, on its own evidence, not to this move-class's re-audit. **Owner: operator. Due: n/a — no longer time-pressured by this audit's original framing.**
3. **Log the Rule-2 trip.** Append a first-ever STRATEGIC-tier row to `docs/notes/audits/rule-2-trip-log.md`, per that log's own instruction ("append one row each time a budget trips… at each programme audit, confirm ≥1 entry per active loop class"). **Owner: this audit. Done below, same session.**
4. **Consolidate the two sharpened guardrails into one canonical location.** They currently live embedded inside two separate Notice bodies (instances 2 and 3); a fourth instance, if ever GO'd, would need to re-read both in full to inherit them rather than citing one place. No placement decision is made here — named, not opened, per this repo's standing convention for un-GO'd work. **Owner: operator (placement call). Due: n/a until GO'd.**
5. **Cross-reference this audit from all three Notices.** So a future reader lands here rather than re-deriving the pattern a fourth time. **Owner: this audit. Not yet done — flagged for immediate follow-up in this same session if the operator wants it.**

---

## §10 — Audit hooks (runnable at the next cycle, or before any fourth instance)

```bash
# 1. Has a fourth instance of this move-class run without a fresh owner GO recorded?
grep -rl "external-mapping-move-class\|external-mechanism.*mapping" docs/notes/notice/ | wc -l
# Expected now: 3 (the three audited instances). A 4th hit needs a paired operator-GO citation.

# 2. Rule-2 STRATEGIC row exists (action 3)
grep -c "STRATEGIC" docs/notes/audits/rule-2-trip-log.md
# Expected after this audit: >=1

# 3. Q-TRAINKILL-2 disposition (action 2)
grep -rn "Q-TRAINKILL-2" docs/briefs/ STATE.md 2>/dev/null | grep -iv "not opened\|named, not"
# Expected pre-decision: no hit (still named-not-opened everywhere). A hit here means action 2 was actioned.

# 4. Belt churn at next audit of this move-class — must show >=1 removal/consolidation, not a 6th pure add
grep -c "sharpened\|ADD$" docs/notes/audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md

# 5. Cross-reference discharge (action 5)
grep -l "AUDIT-2026-08-20-external-mapping-move-class" docs/notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md docs/notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md
# Expected after action 5: all three
```

**Discipline check:** seven diagnostics answered with evidence anchors ✓ · belt churn counted (5/0) ✓ · falsifier check executed against the actual ADR text, not asserted ✓ · no cross-layer citation ✓ · verdict assigned with reasoning ✓ · Degenerating ⇒ five actions named with owner ✓ (dates event-gated where a calendar date would be false precision) · §10 hooks runnable ✓.

---

## Verification

```bash
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md --type audit
```
