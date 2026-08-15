# Q-OBJCOHERE-1 — Closure: `FALSIFIED-COHERENT`

**Parent brief:** [`docs/briefs/Q-OBJCOHERE-1-objective-coherence-audit.md`](../Q-OBJCOHERE-1-objective-coherence-audit.md)
**Pre-registration:** [`docs/briefs/pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md`](../pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md) — FROZEN at commit `ad438ed`, 2026-07-30, strictly before any Phase 1 read.
**Closed:** 2026-07-30
**Verdict:** **`FALSIFIED-COHERENT`** — every constructed tension resolves to quoted precedence text in a ratified artifact. H-OBJCOHERE-1's fragmentation claim (and the parent thesis's H-EDGE clause it operationalized) is **FALSIFIED**.

---

## §1 — What was tested

Whether the operation's five scoped ratified objective instruments (admission, program success, allocation, protection, rung selection) compose coherently, or whether some constructible decision — inside currently-admissible parameter ranges, decidable on paper without a new measurement — gets contradictory dispositions from two live instruments with no written precedence rule deciding between them.

## §2 — Method

Six-reader evidence workflow (`wf_555e6886-487`, resumed once to fix a JS aggregation bug in post-processing — no agent prompt was re-run or altered; 15 agents total, 0 errors):

1. **Phase0-Grounding** — full reads of Q-BUSTGATE-1 closure, Q-COMPOSE-1 closure, and the fork-B ADR's §7 revert triggers in full surrounding context.
2. **Inventory** — three parallel sweeps (Accepted ADRs / RATIFIED specs / FROZEN pre-registrations) produced a **105-row instrument inventory** (instrument · artifact · status · decision class · denomination · scope-or-precedence clause).
3. **Adjudicate** — T1–T4 each piped through two stages: (a) construct a concrete, fully-specified decision object from real estate numbers and run an initial precedence sweep; (b) an **independent adversarial pass**, briefed explicitly to steelman coherence or refute it, reading full source text (not the prior pass's excerpts) and searching for precedence the prior pass might have missed.
4. **PairwiseSweep** — one bounded search over the 105-row inventory for additional candidate pairs sharing a decision class, run twice (once per workflow execution) for redundancy: first pass swept 27 candidate pairs and found zero live tensions; second pass swept 14 (some re-grouped) and surfaced **one** additional candidate (P-BUSTCEIL-1), which was then run through the same two-stage adjudication.

**Parent-side spot-verification:** six of the most load-bearing quotes (fork-B ADR §2/§5, third-leg spec S4/SCREEN-FAIL table, envelope §4a, GO ADR §5 hedging addendum, survivor-scoring Part A) were independently re-read against the live files by the closing session, not merely accepted from subagent output — all verified verbatim, no misquotation, no missing qualifier.

## §3 — Per-tension results

| Tension | Decision object | Contradiction on raw disposition? | Resolves via | Verdict |
|---|---|---|---|---|
| **T1** — rung-selection (fork-B EV, Accepted) vs candidate-admission (survivor-scoring Part A, FROZEN) at a hypothetical 4.0% bust, both-halves PASS | An already-admitted book's rung vs a new candidate's admission, same numeric bust band | No — the two instruments were never adjudicating the same decision | Fork-B ADR's four-fold redundant scope clause (§0 L46, §2 L43, §3 alternatives L55, §5 forbidden-move L82) + independent corroboration from the *already-executed* G8_INTAKE.md scoring record (2026-07-15/17, predates the ADR) showing the admission/rung split was standing practice, not a post-hoc carve-out | `FALSIFIED-COHERENT` |
| **T2** — Stage-8 admission limb (`n_eff_risk_delta > 0`) vs composed Part-A bust ceiling, ORB-MNQ-1's real +0.003 pass / 38.75% composed bust | A candidate clearing the written pre-screen vs the same candidate failing the actual survival gate | No — necessary-not-sufficient by the instrument's own text | Four independently-dated confirmations: the canonical Stage-8 doctrine row, methodology lesson M-21, the third-leg spec's explicit "necessary, not sufficient" line, and STATE.md's own forward-board restatement — plus the 2026-07-13 book-segregation + Stage-8-companion ADRs which predate ORB-MNQ-1 by three days, so the hierarchy was ratified before the incident, not invented after it | `FALSIFIED-COHERENT` |
| **T3** — was there a live instrument mandating a different cap split than the 2026-07-22 69/11 allocation, given Q-CAPALLOC-1 found its stated premise false on P&L | The 69/11 decision (2026-07-22) vs Q-CAPALLOC-1 (frozen 2026-07-27, re-run 2026-07-29) | No — Q-CAPALLOC-1's own §9 scope ("measurement only. No LEG_MAP edit") and §6 gate (best case routes to "operator + amending ADR," an instrument that doesn't exist yet) mean it never mandates a disposition | Two convergent facts: no cap-allocation pricing instrument existed at decision time (a **temporal coverage gap**, not a live contradiction), and the one instrument that could price it today explicitly disclaims mandating authority | `FALSIFIED-COHERENT` — **with a flagged residual**: this is real evidence of a process gap (compliance-driven allocation changes have no standing ex-ante EV/survival pricing requirement), carried to the composition map, not scored as incoherence |
| **T4** — decorrelation/risk-breadth reward (`n_eff_risk_delta > 0`) vs the hedging-compliance veto, on a same-Product-Group negatively-correlated leg | The one tension the estate's own text (envelope L75) names as unresolved: "exactly what this rule forbids" | **Yes, on raw text** — reward vs. absolute prohibition point opposite ways | Two independently-ratified sequencing rules: the GO ADR's 2026-07-22 addendum ("screened for Product Group + sign **before** scoring") and the third-leg spec's SCREEN-FAIL-before-R4 adjudication order (S4 kills the candidate before R4 is ever scored) — proven live by the ORB-MNQ-1 negative control, which clears R4 and still fails on S4 | `FALSIFIED-COHERENT` — **with a flagged residual**: `ops/prop_envelope_default.md` §4a itself is stale — it still reads as an unresolved "note this interacts" and was never updated to cross-reference the GO ADR addendum or the third-leg spec that actually resolve it |
| **P-BUSTCEIL-1** (pairwise-found) — Q-BUSTGATE-1's fee/upside re-derivation of the 3.0% ceiling vs the third-leg spec's T5 bust screen, same numeric figure, two nominally-independent revision channels | Two channels both claiming authority over "≤3.0%" | No — both currently agree the figure is 3.0%, unchanged | The fork-B ADR (produced by Q-BUSTGATE-1's own resolution) explicitly retains 3.0% as "the candidate-ADMISSION falsifier," and explicitly forbids exactly the confusion this pairing worried about ("treat '4.37%' as the new bust ceiling number" is a named category error) | `FALSIFIED-COHERENT` — **with a flagged residual**: the third-leg spec never cites Q-BUSTGATE-1 by name, a documentation cross-reference gap, not a live divergence |

**A labeling defect surfaced and corrected during synthesis, not silently accepted:** the adversarial-pass agents for T2 and T4 selected the enum value `RESOLVED-INCOHERENT-CANDIDATE` while their own prose rationale concluded the opposite (no live contradiction; explicit precedence found) — they used the label to mean "the naive contradictory reading is itself incoherent [refuted]," not "this tension is a live incoherence." The closing session read past the enum field to the substantive rationale in both cases before scoring — the same discipline the estate's own M-AHF lesson names ("audit hooks check storage form, not human-readable property"). Both are recorded here as `FALSIFIED-COHERENT` on the strength of their prose, not their selected label.

## §4 — Gate application

Per the frozen pre-registration (§6, commit `ad438ed`): **zero** paper-decidable contradictions survived the precedence sweep across T1–T4 and the one pairwise-found candidate; the two flagged residuals (T3's timing gap, T4's documentation staleness) are explicitly non-contradictions under the pre-committed contradiction definition, carried forward as findings rather than scored incoherence. This is the `FALSIFIED-COHERENT` trigger exactly as pre-registered — not a mixed or ambiguous outcome, since no tension landed in the "constructibility undecidable on paper" branch (every tension's *coherence question*, as opposed to its underlying economic question, was fully decidable from existing ratified text).

## §5 — Disposition

Per §9 of the parent brief:
- Composition map published: [`docs/methodology/objective_composition_map.md`](../../methodology/objective_composition_map.md).
- Falsification addendum appended to the parent thesis: [`docs/notes/2026-07-29-comparative-advantage-thesis.md`](../../notes/2026-07-29-comparative-advantage-thesis.md) §4 Addendum.
- **No charter ADR is authored.** The estate does not need a new operation-level objective document — it already states, redundantly and in multiple independent locations, the precedence rules a charter would have had to invent. What it needs, named in the two flagged residuals, is smaller: one process gap (T3) and two documentation cross-reference fixes (T4, P-BUSTCEIL-1) — neither rises to the level this brief was authorized to fix (§5 forbids editing any threshold or gate; these are process/doc suggestions for the operator to route, not executed here).

## §6 — What this does NOT change

No `core/`, allocation, `dd_protection`, Pine, rail, threshold, or rung was touched — verified by the parent brief's §10 audit hooks (all still pass). Q-CAPALLOC-1 stays `AMBIGUOUS (d)`; Q-CAPALLOC-2 is unaffected; the rung stays WATCH-1 0.50×/disarmed; ORB-MNQ-1 stays PARKED. Nothing here re-opens any of those.

## §7 — Lesson candidates (not yet dollar-anchored; recorded per Trap #9)

- **Candidate:** an agent adversarially verifying a prior pass's conclusion should be prompted to restate its classification in the SAME enum semantics as stage 1 explicitly, not left to infer them from context — the T2/T4 labeling drift (enum contradicting prose) cost nothing here because the closing session read the prose, but a less careful synthesis pass would have banked the wrong verdict from the enum alone. Anchor: this audit, 2026-07-30. No dollar cost (caught before any downstream use); below promotion threshold on a single instance.
- **Candidate:** the estate's redundant-scope-clause discipline (nearly every Accepted ADR since 2026-06 carries an explicit "Scope:" / "Downstream NOT changed" / "Does not supersede" line) is *why* this audit found coherence rather than fragmentation — worth naming as a positive practice to continue, in the same register as `feedback_visible_restraint_in_closing_brief` memory (restraint decisions deserve equal billing). Anchor: 105-row inventory, this audit.

## §8 — Programme-audit signal check

Checked against the seven degeneration signals: no belt-patch without corroboration (every finding here traces to independently-re-verified primary text); belt did not only grow (this audit found zero new gates to add — it found the existing gates already sufficient); no falsifier threshold drifted; methodology was not invoked to rationalize a prior decision (the audit's own pre-registration was frozen before any tension was read); no SNAG pattern (this is the audit's first and only run); no cross-layer contamination; no negative heuristic crossed. Clean.

---

## Verification

```bash
$ rg -n "Scope: the c1 book's rung selection only" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
$ rg -n "Extending the EV objective to candidate ADMISSION" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
$ rg -n "necessary, not sufficient" STATE.md docs/spec/2026-07-27-third-leg-target-spec.md
$ rg -n "Decorrelation candidates must now be screened for" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
$ rg -n "exactly what this rule forbids" ops/prop_envelope_default.md
$ rg -n "SCREEN-FAIL" docs/spec/2026-07-27-third-leg-target-spec.md | head -1
# All six executed 2026-07-30 against worktree HEAD — all confirmed verbatim, quoted in §3 above.

$ git log --oneline -- docs/briefs/pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md
# Expected: pre-reg commit ad438ed precedes this closure's commit — confirmed by construction (pre-reg committed, then this audit ran, then this closure authored in the same session, no intervening edit to the pre-reg).
```
