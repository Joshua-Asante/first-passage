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
2. **`/v7` needs three edits in `diagnostic_budget_profile`** (corrected in the fix round below). `/v7` is refused outright until it is added to the accept tuple (`profile.py:219-226`). It must also be added to the funded branch (`:243-252`), or it gets an unfunded `/v2` budget profile. Its N2 value must be added at `:239`, or N2 falls back to the shared 120 s: the silent-SIGKILL class that checkpoint C2 found. The N2 value needs operator decision 3: extend the M13 ruling, or apply the rule on a §3-conformant N2 measurement (Stage 1b-N2). Stage 0 cannot supply it.
3. **`/v7` loses the TEST_ONLY cap** (`fixture_producer.py:154-156` covers release v3–v6 only). A `v7` release would fail Σ-feasibility at binding.
4. **No host factor is evidenced.** The "~137 s on Linux by scaling" figure (plan line 756) has no recorded basis, and its measurement record was not found locally. The S4 Linux run artifacts could calibrate it, but their retention ends about **2026-10-09** (Stage 0; needs approval).
5. **The engine's pilot predicate needs a ceiling term.** The engine refuses Part A when its throttled prediction of maximum expansion exceeds the remaining wall (`part_a.py:184-186`), even when no expansion will happen. The PART_A ceiling must cover that prediction (PA-2b).

**Unverified:** see proposal §9. Neither the Linux CPU of any stage nor the systemd accounting fields for an exited unit were read. The §1 CPU estimate is arithmetic from Windows per-call costs. The guardian's CPU while archiving two artifacts is unknown.

**Verification:** `./fp.ps1 check` ran on the final working tree immediately before the commit; the committed bytes are identical to it. The coordinator's return message carries the record path and result, the commit SHA and `git diff --stat`.

**Fix round (2026-09-26).** A fixer checked nine review findings against the sources and applied all nine to the proposal. It edited only the proposal and this section, and ran no measurement.
- **Cold start (§3.2, §3.4):** timed repeat 1 of each arm is now made cold (bytecode caches removed, page cache dropped) and is included in the maximum. The instrumented repeat runs last. The arm order alternates between the two jobs.
- **Like-for-like CPU (§3.1, §4):** CPU is split at the harness boundaries. The 10.4–12.4 s of fixture setup is excluded from Ĉ. The N2 FULL baseline derivation and the real S5-D1 artifacts are an explicit uncovered term, D̂, measured by a new Stage 1c at C3. A ceiling is provisional until then. PA-5 now compares like with like.
- **Windows accounting (§3.1):** `process_time`, a job object and `PeakWorkingSetSize`. Windows figures are marked not comparable to Linux.
- **`/v7` pitfall (§0):** restated with all three `profile.py` locations; see concern 2.
- **Reference runtime (§2):** Stage 1b measures the host venv, not the worker image. The host-to-container factor is unmeasured.
- **Owner citations (§1):** full-E1 spec lines 117–125, and the freeze candidate (not frozen) for depth 200 and horizon 500.
- **Estimate inputs (§0, §1, §5):** `verify_for` CPU is 1.02–1.16 s per call across all nine rows and rises with depth. Panel proofs cover the whole 174-session source. The production claim that per-call cost does not depend on content is withdrawn.
- **Stage 0 (§3.4, §4, §8):** calibration only. It cannot set the `/v7` N2 ceiling. That needs Stage 1b-N2 or an operator ruling extending M13.
- **D2 falsifier, correcting this return:** the TEST_ONLY setup does not rule out the D2 fallback. The falsifier stays **open** until a valid Stage 1b record exists. It is triggered if Stage 1b is not approved or cannot run before release, unless the operator sets the ceiling by ruling (§5).

**Coordinator review (2026-09-26): ACCEPTED AS INPUT; nothing approved; S5 stays HELD.** Reviewer: the coordinating session. Artifacts: `0a4cde5` and the fix round `32c4d40`. Refute-first reviews found nine issues (three major), all applied after verification: cold-start handling, setup CPU separated from workload CPU, and Windows capture. The coordinator spot-checked:
- `profile.py:239`: N2's 360 s ceiling applies only to `/v6`;
- `fixture_producer.py:154-156`: the test-cap raise is limited to releases v3–v6;
- `part_a.py:184-186`: the predicted-budget refusal.

**For operator decision (note §8):**
1. The PROPOSED margin rule.
2. Its scope.
3. The `/v7` N2 ceiling.
4. Two measurement steps that each need approval: downloading the S4 Linux run logs, which GitHub deletes around 2026-10-09 — time-sensitive; and a new Linux measurement job, which is both a CI change and a Linux dispatch.
5. Whether budget arithmetic before release counts as RC-3 feasibility evidence.

**RC status:** RC-1 is partly met (the ruling entry is on PR #517); RC-2 through RC-6 are unmet. **No S5 release proposal is supported.**

**New defects to route (not fixed here):**
- The test workload can never expand, so the "prescribed expansion" case is impossible on the current fixture.
- A `/v7` profile would silently lose N2's ceiling and the test budget cap.
