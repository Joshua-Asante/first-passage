---
name: inqhiori
description: Methodology for structural, low-reversibility, or statistically-gated investigation. Trigger on INQHIORI, The Algorithm, D-S-A pre-Q gate, Notice/Inquire phases, gate audits, observation routing, or framework refinement. Also fires when authoring decision briefs, proposing structural changes, formulating Inquire-phase questions, auditing deletion criteria, or evaluating whether artefacts are load-bearing vs ceremonial. Methodology layer only — does NOT modify strategy code, allocations, dd_protection, or MC calibration. Sibling: `ooda-loop` for tactical/recoverable/tempo work; exit this skill if a request needs speed over rigor. Hand off to prop-firm-challenge for operational/Rule-0 facts and pinescript-v6 for strategy code. Loop-selection canon: docs/methodology/inqhiori-canon.md (§14 three-loop binding).
---

# INQHIORI — Recursive investigation loop with D-S-A pre-Q gate

Component skill of the **INQHIORI ⊕ OODA dual-loop framework** (reactivated 2026-05-01). This skill scopes to INQHIORI; OODA is the sibling skill `ooda-loop`.

**Canonical reference:** `docs/methodology/inqhiori-canon.md` (§14 = the three-loop binding). When this skill disagrees with the canon, trust the canon. The Notion surface was retired 2026-06-12 (ADR `docs/adr/2026-06-12-notion-surface-retirement.md`; dead-ID map `docs/governance/notion-redirect-map.md`). Last reconciliation: 2026-05-01 (post-split).

**What this skill replaces.** The orthogonal-framing predecessors:
- INQHIORI reference page — `34cdc0b53c11812d96f8f6e9ee500d5e`
- The Algorithm reference page — `34ddc0b53c11811eb6a0d9192b63d252`
- Unified `inqhiori-algorithm` skill (pre-split) — superseded 2026-05-01

Both predecessor pages remain valid for their definitional content (loop structure on INQHIORI; operator semantics on The Algorithm); both are archived under `docs/methodology/archive/notion/`. The integration discipline lives in this skill and `docs/methodology/inqhiori-canon.md`.

---

## 0. Pre-loop gate: Rule 0 (audit-first)

**Before I begins, read production code directly.** Not memory, not prior briefs, not summaries. Source.

Rule 0 is canonical in `docs/rule_0.md`. For INQHIORI specifically, the instantiation is:

- The I/N corpus assembly is **derived** from production source. Memory and prior docs are inputs to the corpus; they are not the corpus.
- Any decision brief authored before the relevant production file has been read in the current session is a Rule-0 violation. The brief is suspect even if its conclusions happen to be right — it was authored without ground truth in scope.
- The gate (§3) audits what entered I/N. If the source-read step is missing, the gate has nothing trustworthy to filter.

This is the discipline that exists at both layers of the dual-loop. In OODA it instantiates as "read production state before forming observations." Same rule, different cadence.

If a session is about to begin INQHIORI work and Rule 0 has not been honored: stop. Read source. Then start I.

**Rule 2 (budget before acting)** is the spend boundary that sits next to this
read. Declare the loop class at task start and take the iteration budget from
[`docs/adr/2026-06-16-rule-2-budget-before-acting.md`](../../../docs/adr/2026-06-16-rule-2-budget-before-acting.md)
(canon §15). Pointer only — do not restate the numerals in this skill. The ADR
is still PROPOSED; do not graduate it from a session.

---

## 1. The unified loop

```
[Rule 0 read] → I → N → [ D → S → A ] → Q → H → I → O → R → I    (loop)
                              gate
```

Rule 0 sits ahead of Identify. The bracket is the pre-Q gate. **It filters, compresses, and indexes the data surfaced by Identify and Notice before any Question is asked.** Q operates on a sharper corpus. H is correspondingly sharper.

The outer loop and the inner gate share their operator language (D / S / A) but operate on different domains. Confusing the two is the primary failure mode this skill is built to prevent.

---

## 2. D-S-A operates in three domains — name the domain before acting

| Location | Operator domain | Object | Purpose |
|---|---|---|---|
| **Pre-Q gate** (inside INQHIORI) | Data | The I/N corpus | Focus questioning |
| **Post-H build** (The Algorithm proper) | System | The artefact built from a finding | Optimize implementation |
| **Meta-process** (recursive) | Frameworks | The framework itself | Compress ceremonial scaffolding |

Same three operators (D, S, A). Three distinct objects. **Every brief that proposes a structural change must declare which of the three domains it is operating in.** Conflating domains is how forbidden D-tests sneak in unnoticed.

---

## 3. Mandatory brief headers

### When authoring an Inquire-phase brief

Add a 3-line "Pre-Q gate" header immediately after the Context section:

```
Pre-Q gate:
  D: <items deleted from I/N corpus> — test: <D-test applied>
  S: <compression rationale; what representation remains>
  A: <index / structure used to make Q cheap>
```

If any line reads "no action," state explicitly why the gate didn't engage in that domain. "S: no compression — corpus already at the per-trade row level needed for Q" is fine. Silence is not.

### When authoring a brief that proposes a structural change

Add a 1-line "D-S-A domain" header after the brief title:

```
D-S-A domain: <data | system | meta-process>
```

If the brief operates in more than one domain (legitimate; see the Notice-phase compression example), declare each and call out the cascade explicitly.

---

## 4. Operator definitions in the pre-Q (data) domain

### D — Delete
Remove items from the I/N corpus that fail a stated relevance test.
- Every deletion logs the test that killed it.
- The raw I/N corpus is preserved as the Rule 0 anchor; D produces a derived working set, never a destructive overwrite.
- D is reversible by re-running the gate with a revised test.

### S — Simplify
Reduce the remaining data to the lowest-dimension representation that **preserves the anomaly Noticed**.
- Compression test = preservation of N's signal, not byte-count.
- If S removes the signal, S has failed. Revert.

### A — Accelerate
Index / structure the simplified corpus so each subsequent Q costs O(seconds), not O(reload).
- This is what makes the Q–H iteration loop cheap enough to actually iterate.
- A is bounded. Expensive Accelerate on data you might not query is premature optimization.

---

## 5. The relevance test for D — most failure-prone step

**A datum stays if its presence could contradict a hypothesis you haven't formed yet.**

If answering the test requires forming the hypothesis first, the datum stays.

### Forbidden D-tests (these encode the conclusion the loop should reach)
- "Does this have a known physical / causal mechanism?"
- "Does this fit my model?"
- "Is signal-to-noise high?" (assumes you already know the signal)
- "Has this been useful before?"

### Permitted D-tests
- "Is this a known measurement artefact with a documented cause?"
- "Is this duplicated by a higher-fidelity source already in the corpus?"
- "Is this outside the temporal / instrument scope of the question class?"
- "Is this a literal copy / encoding of something already retained?"

If the test you want to apply is not on the permitted list and not trivially equivalent to one, **stop, write the test, declare it new, and surface it to Joshua before applying it**. New D-tests get logged in the gate audit trail.

### What to do when a forbidden D-test is detected
1. Stop the deletion.
2. Surface the test and the items it would have deleted to Joshua.
3. Do **not** quietly substitute a permitted test that produces the same deletion. That is the Iran-Hormuz failure replayed.
4. If the deletion is genuinely warranted, the corpus contains a structural duplicate or scope violation that a permitted test will catch. Find that test instead.

---

## 6. Guardrails

1. **Time budget (ε-greedy split).** Gate effort ≤10% of I/N effort. The split is ε-greedy: 10% explores criterion-space (which D-tests apply, which compressions preserve N), 90% exploits the established I/N collection methodology. Exceeding the budget signals **I/N was wrong**, not that the gate needs more time — restart the outer loop. Tune ε empirically after the first ~5 gated loops; 10% is the starting prior, not a fixed law.
2. **Audit on regret.** Anything deleted that later proves to matter triggers a gate audit — criterion review, not just data restoration. Log the failed criterion in `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md`.
3. **S preserves N.** S that removes N is not S. Compression that loses the anomaly is failure.
4. **Bounded A.** A must be cheaper than the queries it enables, in expectation. If A is the costly step, the gate has been misapplied.
5. **Recursion logging.** INQHIORI loops; the gate loops with it. Each iteration may surface I/N data the prior gate deleted. That's the criterion updating, which is fine — but log every such case explicitly. Repeat occurrences of the same criterion failing are the signal that the D-test class is too aggressive.
6. **Tail-methodology-exhaustion.** When three falsifiable hypotheses on the same investigation thread close NULL or AMBIGUOUS, STOP. Do not author H4 within the same framing. The pattern is not "I need a sharper hypothesis" — it is "the question itself is ill-formed at this level," and a 4th attempt at the same level burns budget without information gain.

   **Anchor:** the DJ30 anchor trade investigation. Q-DJ30-1 (macro proximity → null), Q-DJ30-2 (hard dollar cap → AMBIGUOUS / regime-robustness gate failed), Q-DJ30-3 (opening-gap magnitude → null, anchor at 43rd percentile). The locked methodology lesson is: "Tail methodology budget exhausted; no Q-DJ30-4 without new evidence." That lesson generalizes — it is this guardrail.

   **What to do at exhaustion:**
   - Reformulate the question itself, not the hypothesis. The Q-numbering resets; the new Q is structurally different (different framing, different unit of analysis, different D-test, or different domain — frequently this means moving from data-domain to system-domain or meta-process domain in the §2 sense).
   - OR accept that the original question may not have a falsifiable answer in the available corpus. Close the investigation thread AMBIGUOUS-by-exhaustion. This is not a failure mode; it is a legitimate terminal state. The brief documents the closure and the audit trail makes future re-investigation cheap if new evidence surfaces.
   - DO NOT silently relax the gate criteria for H4 to make it pass. That is the methodology-layer equivalent of `p`-hacking and is forbidden by the same logic that rules out forbidden D-tests in §5.

   **Convergence note.** This rule appears independently in `obra/superpowers:systematic-debugging` Phase 4.5 ("after 3 failed fix attempts, stop and question the architecture"). The two converged on the same invariant from different domains — investigation methodology in this skill, code debugging there. Independent convergence on the same shape suggests this is a domain-general feature of structured inquiry: three good-faith attempts at the same level failing is evidence about the level, not about the attempts. The mirror in `code-defect-debugging` §5 ports the rule to that skill's domain explicitly.

   **What this is NOT.** Three rejected hypotheses across DIFFERENT investigation threads is normal scientific yield, not exhaustion. The rule fires only when the three Hs share a parent question and a level of analysis. Q-DJ30-1/2/3 share the parent "what makes this anchor trade an anchor"; Q-A1 and Q5.1 (different investigations) do not count toward Q-DJ30's budget.

---

## 7. Worked example A — Iran-Hormuz overlay (counterfactual)

The overlay episode is the canonical clean test case for the gate. A properly applied D-S-A pre-Q gate would have refused to build the regime overlay.

**I:** Iran-Israel conflict, June 2025. Strait of Hormuz threatened.
**N:** Gold spiking, USDJPY whipsawing, Guardian / Aegis exhibiting unusual signal density. Physical traffic through Hormuz: continuous.

### What the overlay actually did (failed gate)

D-test implicitly applied: *"Does this price action have a physical / causal mechanism in the conflict zone?"*

Physical ground-truth (channel open, traffic continuous) → conclusion that the price action "lacked a mechanism" → overlay built that conditioned position sizing on physical conditions → overlay later deactivated 2026-04-23 after revert conditions met.

This D-test is **forbidden** under the formal gate. It encoded the hypothesis ("physical conditions drive price") inside the relevance test. The conclusion was baked in before Q ever ran.

### What the gate would have done (properly applied)

D-test applied: *"Could this datum contradict a hypothesis I haven't formed yet?"*

Two streams in the I/N corpus — physical ground-truth and headline-timestamped price action — both pass D. The **divergence** between them is the unformed hypothesis. Neither is deletable without pre-judging.

**S:** collapse both streams to a single comparison object — headline timestamp vs price reaction within an N-minute window. Preserves the anomaly (the divergence).
**A:** index by headline timestamp; Q-cost drops to seconds.
**Q (sharper):** Why does price react to headlines without corresponding physical follow-through?
**H:** Market participants price expectations and tail-risk premia, not physical state.

The properly-gated loop reaches the lesson **without building the overlay**. That is the specific value the gate adds.

---

## 8. Worked example B — Notice phase compression (2026-04-25, retrospective)

The Notice phase compression that landed on 2026-04-25 (commits `a05e9f3` → `cfea4a2`) was an unconscious application of the gate, framed at the time as "applying The Algorithm to the framework itself."

| Step | Domain | What happened |
|---|---|---|
| Q | Meta-process | "Is the Notice / Inquire bifurcation load-bearing or ceremonial?" |
| D | Meta-process AND Data | Deleted A3 / C3 threads from the framework AND deleted the JSON / figure / CSV intermediates the threads produced |
| S | Meta-process | Replaced two-phase ceremony with three-bucket routing gate (`docs/methodology/observation_routing.md`) |
| (no A) | — | The simplified gate didn't need acceleration |

**Cascade rule:** when D acts on a meta-process (a framework), it implicitly authorizes corpus-level D on the data that framework was producing. When D acts on data alone (the pre-Q gate), it does **not** authorize framework changes. Frameworks are governed by the meta-process domain, which has its own discipline.

---

## 9. First conscious test — Inquire-phase work (in flight)

The 2026-04-25 Claude Code brief sets up three Inquire-phase questions. Each is an opportunity to **explicitly run the gate and log the audit trail**:

1. **Q1 — Guardian 1R reconciliation.** I/N corpus: Guardian v5.5 OANDA backtest CSV + Pine sizing line + canonical 1R doc.
   - Pre-Q gate: Delete the bar-data findings (out of scope by temporal / instrument test); Simplify to per-trade equity-normalized loss; Accelerate by precomputing running equity.
   - Q: equity-compounding artefact or sizing problem? Cheapest falsification first.

2. **Q5 — XAU-USDJPY break window P&L.** I/N corpus: B2 finding + strategy P&L during 2025-10-30 → 2026-01-27.
   - Pre-Q gate has already partially run (Q5 selected over Q3 specifically because Q5 is the cheaper falsification — that's the gate's *Simplify* step on the question set, not just the data).

3. **Q8 — Doc / code skew postmortem.** I/N corpus: ADR change log + recent decision briefs.
   - Pre-Q gate: Delete (Q8a only audits the last 60 days, not all-time — that's a D-test on temporal scope); Simplify (single audit table); Accelerate (grep-friendly).

**If a gate audit reveals a forbidden D-test was applied, that's the framework working as intended.** Log it; learn from it; tighten the D-test criterion next iteration.

---

## 10. Interaction with other rules and skills

- **`ooda-loop` is the sibling skill.** Tactical / recoverable / tempo work runs through OODA, not this skill. Selection criterion: if the work is structural / low-reversibility / requires statistical support, this skill. If tactical / recoverable / tempo-driven, exit and use OODA. Tiebreaker: if the falsifiable hypothesis cannot be stated in one sentence, the work is not yet INQHIORI territory — run OODA, gather observations, let INQHIORI activate when a hypothesis crystallizes. Canon: docs/methodology/inqhiori-canon.md (§14).
- **`code-defect-debugging` is the sibling for deterministic code bugs.** Code returning the wrong value, scripts crashing, output magnitudes implausible vs reference, cross-platform output diverging — those are not INQHIORI questions, they are deterministic-defect questions. Selection criterion: if the failure is "code is doing something inconsistent with its inputs" and re-runs reproduce deterministically, exit to that skill. If the failure is "the strategy / methodology is producing unexpected statistical behavior," this skill applies. Tail-methodology-exhaustion (§6 guardrail #6) and that skill's Phase 4.5 mirror each other; misrouting between the two skills is the most common cost in this region.
- **Rule 0** is canonical in `docs/rule_0.md`. Pre-loop gate at both layers — pre-Identify here, pre-Observe in OODA. See §0.
- **Rule 1 (small-cell variance prior)** — page `34cdc0b53c11812cbb4ff637ba44736e` — still binds. Small cohorts trigger caution at the Observe / Reflect phase regardless of how the gate filtered the corpus.
- **Overlay policy** is unchanged. No overlays without full INQHIORI. The gate is the front of that loop, not a relaxation of the back.
- **Observation routing gate** (`docs/methodology/observation_routing.md`) operates *after* the pre-Q gate. Observations that pass the gate get routed Closed / Action / Forward. The two gates compose; they don't compete.
- **Iterate exit is closure-resident and typed** (canon §16; ADR `docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`). The loop's terminal I is discharged on the closure artifact as a mandatory `## Iterate` block — Next: INTEGRATE | ITERATE | STOP, entry packet, stop rule, board write — pre-registered per verdict in the brief's §6 Disposition column. STOP is a ratified extension (v1's exit was binary); ITERATE names a successor but never opens one (operator GO). Template: `brief-authoring references/closure_record.md`.
- **`prop-firm-challenge` skill** governs the operational layer (live trading, MC, dd_protection). This skill governs the methodology layer for structural / statistical work. They co-fire on investigation tasks: prop-firm-challenge for the operational facts, this skill for the investigation discipline.
- **`pinescript-v6` skill** governs strategy code. Strategies are locked (current lock versions in `core/strategies/_archive/*/LOCK.md`; allocation ADR `docs/adr/2026-05-23-allocation-refresh-2.md`) and not in scope for this skill.

---

## 11. What this skill does not change

This skill governs how future loops are run, not what current production does. It does not modify strategy parameters, allocations, dd_protection constants, re-MC triggers, or binary-event pauses — those live in `core/dd_protection.py` / `core/firm_rules.py` and the allocation ADR `docs/adr/2026-05-23-allocation-refresh-2.md` (canonical), never restated here.

---

## 12. Audit trail format

When a gate audit fires (because a deletion proved wrong, because a forbidden D-test was caught, or because the time budget was exceeded), write a file at `docs/notes/audits/YYYY-MM-DD_gate_<slug>.md` with:

```markdown
# Gate audit — <slug> — <date>

**Trigger:** <regret on deletion | forbidden D-test caught | time-budget exceeded | other>
**Loop context:** <which INQHIORI loop the gate was attached to>

## What the gate did
- D-test applied: <verbatim>
- Items deleted: <list>
- S compression: <description>
- A index: <description>

## What went wrong
<one paragraph: what the gate missed and how it surfaced>

## Criterion update
- Old D-test: <verbatim>
- New D-test: <verbatim>
- Permitted-list addition (if any): <new entry>

## Cross-references
- Loop: <inqhiori-canon.md §ref or loop label>
- Affected decision: <ADR / brief / commit>
```

Keep these short. The point is the criterion update; everything else is provenance.

---

## 13. Usage notes for Claude (web and Code)

- **Loop selection precedes everything else.** Before any of the below, confirm the work is INQHIORI (structural / statistical / low-reversibility). If it's tactical/tempo, exit to `ooda-loop`. See §10.
- **Rule 0 first, every time.** §0 is not optional. Read source before authoring.
- **Both clients reference this skill and `docs/methodology/inqhiori-canon.md`**, not the orthogonal-framing predecessors.
- **Briefs that author Inquire-phase questions** include the mandatory Pre-Q gate header from §3.
- **Briefs that propose structural changes** include the mandatory D-S-A domain header from §3.
- **The gate is user-gated at D.** Both clients propose deletions; Joshua authorizes. Same discipline as The Algorithm proper.
- **When in doubt about which domain D-S-A is operating in, ask.** Domain conflation is the failure mode this skill exists to prevent.
- **Do not silently substitute a permitted D-test that produces the same deletion as a forbidden one.** That is the Iran-Hormuz failure replayed. If the deletion is real, a structural permitted test will catch it.
