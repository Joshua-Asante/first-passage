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
- **RC table:** RC-1..RC-6 (§7). RC-1 is partly met (the ledger entry is on PR #517, not yet on `main`); RC-2 to RC-6 are unmet. **No S5 release proposal is supported.** *(RC-1 status superseded 2026-09-26: see the coordinator correction below, H1.)*
- **Operator decisions:** five are listed in §8.

**Concerns returned to the coordinator.** They are findings and change no owner record.
1. **The TEST_ONLY workload (2, 4, 2) can never expand.** The expansion test is pinned to `|p5 − 0.95| ≤ 0.01` (`contract.py:761-773`), and with 2 paths per panel no panel rate is within 0.01 of 0.95. The smallest depth that can expand is 17. Every existing composition run confirms this: none expanded. Maximum expansion therefore needs a forced-expansion harness, and the S5 packet's Linux "prescribed expansion" case is impossible on this fixture: the arithmetic boundary test must stand alone. This belongs in the RC-6 re-anchoring.
2. **`/v7` needs three edits in `diagnostic_budget_profile`** (corrected in the fix round below). `/v7` is refused outright until it is added to the accept tuple (`profile.py:219-226`). It must also be added to the funded branch (`:243-252`), or it gets an unfunded `/v2` budget profile. Its N2 value must be added at `:239`, or N2 falls back to the shared 120 s: the silent-SIGKILL class that checkpoint C2 found. The N2 value needs operator decision 3: extend the M13 ruling, or apply the rule on a §3-conformant N2 measurement (Stage 1b-N2). Stage 0 cannot supply it.
3. **`/v7` loses the TEST_ONLY cap** (`fixture_producer.py:154-156` covers release v3–v6 only). A `v7` release would fail Σ-feasibility at binding.
4. **No host factor is evidenced.** The "~137 s on Linux by scaling" figure (plan line 756) has no recorded basis, and its measurement record was not found locally. The S4 Linux run artifacts could calibrate it, but their retention ends about **2026-10-09** (Stage 0; needs approval). *(Superseded 2026-09-26: the download was approved and done; see the coordinator correction below, Stage 0 status.)*
5. **The engine's pilot predicate needs a ceiling term.** The engine refuses Part A when its throttled prediction of maximum expansion exceeds the remaining wall (`part_a.py:184-186`), even when no expansion will happen. The PART_A ceiling must cover that prediction (PA-2b).

**Unverified:** see proposal §9. Neither the Linux CPU of any stage nor the systemd accounting fields for an exited unit were read. The §1 CPU estimate is arithmetic from Windows per-call costs. The guardian's CPU while archiving two artifacts is unknown.

**Verification:** `./fp.ps1 check` ran on the final working tree immediately before the commit; the committed bytes are identical to it. The coordinator's return message carries the record path and result, the commit SHA and `git diff --stat`.

**Fix round (2026-09-26).** A fixer checked nine review findings against the sources and applied all nine to the proposal. It edited only the proposal and this section, and ran no measurement.
- **Cold start (§3.2, §3.4):** timed repeat 1 of each arm is now made cold (bytecode caches removed, page cache dropped) and is included in the maximum. The instrumented repeat runs last. The arm order alternates between the two jobs.
- **Like-for-like CPU (§3.1, §4):** CPU is split at the harness boundaries. The 10.4–12.4 s of fixture setup is excluded from Ĉ. The N2 FULL baseline derivation and the real S5-D1 artifacts are an explicit uncovered term, D̂, measured by a new Stage 1c at C3. A ceiling is provisional until then. PA-5 now compares like with like. *(Superseded 2026-09-26: Stage 1c's forced arm needs Stage 1c-prep, and the worker-side residual R̂ stays uncovered after it; see the coordinator correction below, F1.)*
- **Windows accounting (§3.1):** `process_time`, a job object and `PeakWorkingSetSize`. Windows figures are marked not comparable to Linux.
- **`/v7` pitfall (§0):** restated with all three `profile.py` locations; see concern 2.
- **Reference runtime (§2):** Stage 1b measures the host venv, not the worker image. The host-to-container factor is unmeasured.
- **Owner citations (§1):** full-E1 spec lines 117–125, and the freeze candidate (not frozen) for depth 200 and horizon 500.
- **Estimate inputs (§0, §1, §5):** `verify_for` CPU is 1.02–1.16 s per call across all nine rows and rises with depth. Panel proofs cover the whole 174-session source. The production claim that per-call cost does not depend on content is withdrawn.
- **Stage 0 (§3.4, §4, §8):** calibration only. It cannot set the `/v7` N2 ceiling. That needs Stage 1b-N2 or an operator ruling extending M13.
- **D2 falsifier, correcting this return:** the TEST_ONLY setup does not rule out the D2 fallback. The falsifier stays **open** until a valid Stage 1b record exists. ~~It is triggered if Stage 1b is not approved or cannot run before release, unless the operator sets the ceiling by ruling (§5).~~ *(Superseded 2026-09-26 by the F3 correction below.)*

**Coordinator review (2026-09-26): ACCEPTED AS INPUT; nothing approved; S5 stays HELD.** Reviewer: the coordinating session. Artifacts: `0a4cde5` and the fix round `32c4d40`. Refute-first reviews found nine issues (three major), all applied after verification: cold-start handling, setup CPU separated from workload CPU, and Windows capture. The coordinator spot-checked:
- `profile.py:239`: N2's 360 s ceiling applies only to `/v6`;
- `fixture_producer.py:154-156`: the test-cap raise is limited to releases v3–v6;
- `part_a.py:184-186`: the predicted-budget refusal.

**For operator decision (note §8):**
1. The PROPOSED margin rule.
2. Its scope.
3. The `/v7` N2 ceiling.
4. Two measurement steps that each need approval: ~~downloading the S4 Linux run logs, which GitHub deletes around 2026-10-09 — time-sensitive;~~ and a new Linux measurement job, which is both a CI change and a Linux dispatch. *(Corrected 2026-09-26: the download was approved and done; see below.)*
5. Whether budget arithmetic before release counts as RC-3 feasibility evidence.

~~**RC status:** RC-1 is partly met (the ruling entry is on PR #517); RC-2 through RC-6 are unmet.~~ **No S5 release proposal is supported.**

**New defects to route (not fixed here):**
- The test workload can never expand, so the "prescribed expansion" case is impossible on the current fixture.
- A `/v7` profile would silently lose N2's ceiling and the test budget cap.

**Coordinator correction and refreshed disposition, 2026-09-26 (PR #519 review; governs over the RC line struck above and over the executor-return statements marked superseded: RC-1, the Stage 0 retention and Stage 1c).** A review of PR #519 at `8c15f18` inspected documents and cited code and ran no tests. It found three P2 defects in the proposal and one stale status. The coordinator's corrections are in the note as dated edits, with superseded sentences struck, not deleted; the executor's return and fix-round text above stay as its record, except one superseded fix-round sentence on the D2 falsifier, which is struck. **Disposition: the note remains an input only. Its rule and its measurement steps are not approved, and these corrections apply before either is put for approval.** Nothing here approves the rule, closes an RC, releases S5 or authorizes execution. Every numeric parameter stays PROPOSED.
- **F1, Stage 1c forcing (note §3.4).** Stage 1c had no mechanism to force expansion through the real adapter. The adapter does not exist yet; its specified interface has no tolerance input; and the signed contract pins the tolerance at 0.01, with the source bound to that one contract object. So no measurement-only injection point exists without a change. The note proposes **Stage 1c-prep**, for its own approval: a structural requirement that the S5 adapter build its engine request through one call-time module-level function, as the N1/N2 compute does with `stage_request`, plus a substitution of that function inside the Stage 1c harness only. It stays outside production and signed acceptance. The alternative, an expansion-capable fixture of at least 17 paths per panel, is recorded as a different workload and not chosen. *Round 2:* two additions. First, `run_part_a_compute` returns byte strings (packet line 27). The worker's encode, validate, frame, output write and fsync (`worker.py:69-94`, `:140-150`) are outside it, so they are a named uncovered residual, R̂, and Ĉ₁c no longer claims the whole §1 workload. Whether a run may rely on an application with R̂ uncovered is an operator decision. Second, Stage 1c-prep now also pins the packet's unnecessary-expansion rejection (packet lines 30, 38) in G5, or after the adapter returns. A refusal is Blocked, a C3 build defect, or Invalid, according to its cause.
- **F2, memory (note §3.1, §4 PA-3/PA-4).** A process memory value is a lower bound. M̂ now comes only from aggregate cgroup evidence covering the whole measured unit. Without it, memory feasibility is **UNVERIFIED**, PA-3 is not evaluated, and RC-3 cannot close. *Round 2:* the service's shared `memory.max` is on the host-run parent cgroup (`campaign_supervisor.py:830`, `:811`). That parent also holds qexec, the launch clients and the guardian (`:802-804`, `:1413-1414`). The unit aggregate therefore covers the payload container's own limit only (`:2592-2593`), and that check is renamed PA-3a. Feasibility against the shared limit stays **UNVERIFIED** until the new PA-3b checks Stage 2's parent `memory_peak_bytes` (`:974`) at C3. Stage 2 never expands, so PA-3b's maximum-expansion composition rests on an unmeasured assumption. Whether RC-3 can close on payload-only memory evidence is decision 7.
- **F3, D2 falsifier (note §5).** A blocked measurement retains the S5 hold, and an invalid one is investigated; neither triggers the falsifier. Only evidence that the bound cannot be established returns the accounting-design question. This supersedes the fix-round bullet above that treated a missing Stage 1b approval as a trigger. *Round 2:* several refinements.
  - A missing aggregate memory reading is Blocked for RC-3's memory item, not Invalid, and CPU and wall still apply.
  - A missing Stage 1c-prep seam is Blocked only before approval. After approval it is a C3 build defect.
  - A digest mismatch bears on R7 only after diagnosis.
  - This reading of "cannot be measured" departs from the literal draft wording (draft line 228). The D2 ruling words are only "Retain per-phase accounting." (plan line 806). The reading therefore goes to the operator as decision 6, and is named for the RC-2 review of draft §2.3.
- **H1, refreshed RC disposition (note §7).** PR #517 merged as `5ad04cf`, and `origin/main` is `5ad04cf`. **RC-1 is recorded on the reviewed base** (`main@5ad04cf`, execution-slices plan lines 801–815). **RC-2 to RC-6 remain open.** No S5 release proposal is supported. The executor's RC table in note §7 is kept and labelled as its snapshot at `0a4cde5`/`32c4d40`.
- **Stage 0 status.** The operator approved the download of both S4 run artifacts (runs 36180568493 and 36181780676, artifact `qualification-s2-supervision`) on 2026-09-26. They are preserved in the operator's primary checkout at `local_artifacts/s4-linux-run-logs-2026-09-25/` (gitignored): 222 files listed in `SHA256SUMS`, whose SHA-256 is `e2c142281d819e071d15f99a242358f93389a479dcc5e6b5c1f6a20d5db189a7`; `sha256sum -c` passes. They are preserved only and have not been analysed. Interpreting them remains Stage 0 work under the measurement rule once that rule is approved.

**For operator decision, updated:** items 1–3 and 5 above are unchanged. Item 4 is now Stage 1b (a CI change and a Linux dispatch), **Stage 1c-prep** (a change to the S5 packet text plus the harness substitution, or the fixture alternative), and Stage 1c at C3 (note §8). *Round 2 (2026-09-26):* item 4 also asks whether an acceptance-grade run may rely on an application with the worker-side residual R̂ named and uncovered. New item 6: confirm or reject the reading of the D2 falsifier, under which a blocked or invalid outcome does not trigger it. New item 7: RC-3 memory coverage. That asks whether RC-3 may close before release on payload-only memory evidence (PA-3a), with PA-3b at C3, and whether PA-3b's maximum-expansion composition is accepted, or a measured non-payload allowance or the fixture alternative is required.
