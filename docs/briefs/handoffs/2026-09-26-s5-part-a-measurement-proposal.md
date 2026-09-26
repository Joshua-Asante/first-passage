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

## Executor return (2026-09-26)

**Status: DONE_WITH_CONCERNS.** The proposal is at [`docs/notes/2026-09-26-s5-part-a-measurement-proposal.md`](../../notes/2026-09-26-s5-part-a-measurement-proposal.md). The executor worked in worktree `s5-measurement`, branch `claude/s5-measurement-proposal`. `HEAD` descends from the dispatch revision `62c956f`. Under `ops/`, `tests/`, `tools/`, `deploy/`, `scripts/` and `.github/`, that head does not differ from `main@8e9e084`. No measurement, Linux dispatch, qualification service, artifact download, code, profile, budget or owner change was made. The executor ran only read-only `grep`/`git` checks and parsed an existing JSON record. Nothing here approves a rule or releases S5.

**Delivered:** items 1–6 and the RC table.
- **Items 1–6:** workload (§1), reference runtime (§2), capture method with exact commands and record format (§3), margin rules PA-1..PA-5 with PROPOSED parameters, sensitivity and triggers (§4), feasibility and D2 falsifier (§5), application procedure (§6).
- **RC table:** RC-1..RC-6 (§7). RC-1 is partly met (the ledger entry is on PR #517, not yet on `main`); RC-2 to RC-6 are unmet. **No S5 release proposal is supported.**
- **Operator decisions:** five are listed in §8.

**Concerns returned to the coordinator.** They are findings and change no owner record.
1. **The TEST_ONLY workload (2, 4, 2) can never expand.** The expansion test is pinned to `|p5 − 0.95| ≤ 0.01` (`contract.py:761-773`), and with 2 paths per panel no panel rate is within 0.01 of 0.95. The smallest depth that can expand is 17. Every existing composition run confirms this: none expanded. Maximum expansion therefore needs a forced-expansion harness, and the S5 packet's Linux "prescribed expansion" case is impossible on this fixture: the arithmetic boundary test must stand alone. This belongs in the RC-6 re-anchoring.
2. **`/v7` loses the N2 ceiling** (`profile.py:239` widens N2 for `v6` only; the M13 ruling says "/v6 only"). This is the same silent-SIGKILL class that checkpoint C2 found. It needs operator decision 3.
3. **`/v7` loses the TEST_ONLY cap** (`fixture_producer.py:154-156` covers release v3–v6 only). A `v7` release would fail Σ-feasibility at binding.
4. **No host factor is evidenced.** The "~137 s on Linux by scaling" figure (plan line 756) has no recorded basis, and its measurement record was not found locally. The S4 Linux run artifacts could calibrate it, but their retention ends about **2026-10-09** (Stage 0; needs approval).
5. **The engine's pilot predicate needs a ceiling term.** The engine refuses Part A when its throttled prediction of maximum expansion exceeds the remaining wall (`part_a.py:184-186`), even when no expansion will happen. The PART_A ceiling must cover that prediction (PA-2b).

**Unverified:** see proposal §9. Neither the Linux CPU of any stage nor the systemd accounting fields for an exited unit were read. The §1 CPU estimate is arithmetic from Windows per-call costs. The guardian's CPU while archiving two artifacts is unknown.

**Verification:** `./fp.ps1 check` ran on the final working tree immediately before the commit; the committed bytes are identical to it. The coordinator's return message carries the record path and result, the commit SHA and `git diff --stat`.
