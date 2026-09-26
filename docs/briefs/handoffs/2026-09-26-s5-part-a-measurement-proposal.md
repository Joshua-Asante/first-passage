# S5 Part A measurement-and-margin proposal, and RC status — bounded handoff

**Status:** DISPATCHED 2026-09-26 by the coordinating session (Claude Code, Opus 5.5) on the operator's instruction "start the close semantics, S5 measurement and ORB trace handoffs". **Dispatch revision:** the commit that adds this card; the executor verifies its `HEAD` descends from it. **Executor:** one assessor subagent in its own worktree. **Coordinator:** accepts or corrects the return.

**Authority (operator ruling 2026-09-26, §6):** "Prepare a concrete measurement proposal identifying maximum-expansion workload, reference runtime, CPU/wall/memory capture, proposed margin and budget feasibility. Return the measurement-and-margin rule for operator approval; no numerical rule is approved yet. Once approved, the coordinator may apply that rule to TEST_ONLY diagnostic ceilings with recorded evidence. Production budgets remain separately governed. This preparation does not authorize held S5 execution." The S5 hold stays in place ([execution-slices plan ledger, 2026-09-25 and 2026-09-26 entries](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25)).

## Selected outcome

A concrete, reviewable **measurement-and-margin rule** for the Part A phase ceiling, returned for operator approval. It specifies:

1. **Maximum-expansion workload.** The exact definition: stages, populations, paths and depth at maximum prescribed expansion, as fixed by the frozen plan's owners. Derive it from the governing sources and cite them: the full-E1 spec, the freeze candidate, the Part A engine (`ops/c1_rail/qualification/part_a.py`) and the budget profile (`execution/profile.py`: "PART_A includes maximum expansion").
2. **Reference runtime.** Host class, OS, CPU model class, Python/runtime pin and release identity. State how the measured runtime maps to the production service host, including any host factor and its evidence.
3. **Capture method.**
   - What is measured: CPU as cumulative user plus system time, including children; wall time; peak memory (peak RSS and/or cgroup `memory.peak` on Linux).
   - Repeats and the statistic reported, and how nondeterminism or noise is handled.
   - The exact commands. Use existing harnesses where they apply: `benchmark_part_a.py`, and the [2026-09-24 representative measurement](../../notes/2026-09-24-t10-step4-representative-measurement.md) and its harness.
   - The evidence record format.
4. **Proposed margin rule.** A concrete formula with **proposed numeric parameters, marked PROPOSED — not approved**. Include the reasoning, the sensitivity, and what triggers re-measurement.
5. **Budget feasibility.** Show that the resulting PART_A ceiling fits the campaign cap together with the other phases. That is the `bind_budget` Σ-feasibility check (`execution/campaign_budget.py`, `campaign_store.py`), including the orchestration bound. Include the S5 draft's D2 falsifier: if maximum-expansion CPU cannot be bounded ahead of time, revisit the uniform model.
6. **TEST_ONLY application procedure** once the rule is approved: what the coordinator records, and where. Production budgets remain separately governed.

**Also deliver: an RC-1 to RC-6 status table** for the S5 release conditions in the [S5 decision draft](../../notes/2026-09-26-s5-decision-draft.md) §5. For each condition give its current status (met, unmet or partly met), the evidence (`file:line` or commit), the owner and the next action. Include a concrete S5 release proposal **only if** every condition is evidence-supported. Otherwise state plainly that no release proposal is supported yet, and why.

## Limits

This is a proposal only. Cite existing measurements; **run no new measurement**, no qualification service, no Linux host dispatch, and no S5 execution. If the proposal needs a fresh measurement, specify it exactly as a step for approval. No changes to code, owners, profiles or budgets.

## Output

`docs/notes/2026-09-26-s5-part-a-measurement-proposal.md`, plus an executor-return section appended to this card.
