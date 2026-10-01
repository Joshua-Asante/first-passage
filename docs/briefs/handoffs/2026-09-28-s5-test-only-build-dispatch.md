# S5 TEST_ONLY build — dispatch card for the frozen S5 packet (Protected Full E1 / T04)

**Type:** cc_handoff (dispatch card; it freezes and dispatches an existing packet and adds no build requirement)
**Status:** DISPATCH-READY 2026-09-28. The operator merged it in #547. The dispatch revision is `eef77836473f7bc304018217f452fb68daa40f17`, frozen in §9. Dispatch itself still needs the coordinator's grant. *[Status updated 2026-09-28 on the merge; before it, the card was a DRAFT for coordinator and operator review.]*
**Executor:** GLM, single writer for every file in the packet's §2 (packet header). It is reached through `glm_agent` from a Claude coordinator session, in a worktree that contains no `.env` (§0.5). **Coordinator:** Claude; it owns the pre-dispatch read, diff review, Checkpoint C3, integration and acceptance. **Operator:** the separate C3 dispatch grant for Linux runs, the merge, and any versioned change.

**What this card is.** The [CP-1b ruling](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1b-s5-hold-released-for-the-test_only-build-2026-09-28) released the S5 hold **for the TEST_ONLY build only**. It named the release head `05f3788d9e4895308d6734e650a42875c59f669c` (the merge of #537), and it said: "The next coordinator issues the bounded S5 build handoff from this release head." The build specification is the [S5 packet](2026-09-21-full-e1-s5-part-a-DRAFT.md), which "freezes only at the CP-1b hold-release" (packet line 4). This card freezes it at that head and bounds the dispatch: build up to the packet's Checkpoint C3 push-and-return (packet §5), then stop. **The packet governs every build requirement.** Where this card and the packet differ, the packet governs, and the difference is a defect in this card, to be returned.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_until_coordinator_says
  - no_linux_or_ci_dispatch
  - packet_section2_files_only
  - no_stage1c_harness
  - stop_at_c3_return
acceptance:
  - tests/ops/qualification/execution/test_campaign_part_a.py
  - tests/ops/qualification/execution/test_profile.py
  - tests/ops/qualification/execution/test_release.py
  - tests/ops/qualification/execution/test_worker.py
  - tests/ops/qualification/execution/test_campaign_n2.py
  - tests/ops/qualification/execution/test_campaign_recovery.py
  - tests/ops/qualification/test_journal_snapshot.py
  - tests/ops/qualification/test_part_a.py
  - tests/ops/qualification/test_regime.py
  - tests/ops/qualification/test_evidence_reconstruction.py
  - tests/ops/qualification/test_result_adjudication.py
  - tests/test_qualification_boundary_verification.py
  - tests/test_s2_run_evidence.py
  - tests/test_s2_evidence_tooling_acceptance.py
  - tests/test_guard_s2_runs.py
  - tests/test_s2_evidence_tooling_followups.py
```

`test_campaign_part_a.py` is new (packet §2) and absent at `05f3788`. The list is the Windows-run set. The Linux file `test_campaign_part_a_linux.py` and the conditional `tests/test_qualification_invariant_manifest.py` (packet §2, "only if the registration requires it") are outside it.

## 0. Phase 0: premise check, then Rule 0 reads, before any edit

The first act is the §9 premise check, reported before any edit: the executor runs the repository items, and the coordinator runs the two `glm_agent` items (card text and workdir) before the first ticket. Any failure is a stop (§7), returned under §6. A contradiction between this card, the packet and what the executor reads is returned as `NEEDS_CONTEXT` ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), handoff contract item 2). The executor does not choose a reading itself.

**Test 0 (secrets and private sources).** The build reads and writes only public repository code, tests and documentation. It reads no `.env`, credential, Pine source, runtime port, account figure or private evidence package. The workdir given to `glm_agent` is a worktree under `.claude/worktrees/`, never the primary checkout, which holds a `.env` (§0.5).

**Inputs (read first; at the release head unless stated):**
- the S5 packet, in full. Its §0 and §0.1 are the Rule 0 reads, with the anchors re-taken at `875ecf29` and still valid at `05f3788` (CP-1b ruling, "Anchor re-check against it");
- the CP-1b ruling entry: the four `/v7` preconditions, the provisional memory margin, and what stays open. It landed after `05f3788`, so a worktree cut from the release head does not contain it. It is read at the dispatch revision, and the coordinator quotes its "Build preconditions" and "Memory" items in each ticket;
- the [coordinator's PART_A application entry](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-application-part_a-test_only-diagnostic-ceiling-under-the-approved-measurement-and-margin-rule-2026-09-28): X = 120 s and Y = 300 s equal the shared values, so **no `/v7`-gated PART_A constant** follows (packet §0.5, S5-D3 build notes);
- the [S4 packet](2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md), for the line-1 selection, the placement rule and the precedent for tooling registration;
- the [T05 packet §0.5 F3](2026-09-21-full-e1-t05-result-and-seal.md), for the only progression names S5 may write;
- `AGENTS.md`, "Python environment and local checks".

**The four `/v7` preconditions land with this build** (CP-1b ruling, "Build preconditions"; packet §0.1 P1–P4). Each missed edit fails in a different way:
1. add `/v7` to the P4 tuple at `tests/integration/qualification_boundary/fixture_producer.py:154-155`;
2. add `/v7` at `ops/c1_rail/qualification/execution/profile.py:219-226`;
3. add `/v7` at `profile.py:243-252`;
4. extend `profile.py:239` to `/v7` with 360 s CPU / 900 s wall.

`fixture_producer.py` is an installed fixture under packet §2 (the S4 packet spells out "installed fixtures" as `fixture_producer.py`, `fixture_install.py`, `conftest.py` and the rest), and precondition 1 (packet §0.1 P4, §0.5 build notes; CP-1b ruling) requires its edit. No file outside packet §2 is admitted (§7).

## 0.5. Routing (task-routing checklist, re-applied at dispatch)

`Routing: local`, for three reasons:
- **Verification uses the Windows operations launcher on frozen bytes** (packet §4, the Windows line), and records land in the checkout's `.cache/fp-verification/`.
- **GLM is reached through the local `glm` MCP server.** Its traffic goes to Z.ai, so its `workdir` must hold no secret. Use a fresh worktree: `git worktree add .claude/worktrees/s5-part-a -b claude/s5-part-a 05f3788d9e4895308d6734e650a42875c59f669c`. Confirm that no `.env` exists in it before the first `glm_agent` call. Use `dry_run: true` on the first ticket.
- **No Linux run falls in this card** (§5), so no cloud or CI environment is needed.

**Ticketing.** The coordinator may split the build into sequential `glm_agent` tickets along the packet's §2 file groups:
1. the adapter and the §1a seam, with the adapter boundary tests;
2. the checkpoint route, G5, the worker, `/v7` and `/v8`, with the four preconditions;
3. the S5 run tooling and its focused regression tests.

Each ticket quotes the packet sections it implements, names its files, and states its acceptance tests. None widens §2. After each ticket the coordinator reads the actual diff (not the summary) and runs the named tests before the next ticket. A ticket that fails twice under GLM leaves GLM (the coordinator's GLM rule; AGENTS.md "two failed corrections") and goes to the escalation lane.

## 1. Selected outcome

The S5 TEST_ONLY build on branch `claude/s5-part-a`, cut from the release head `05f3788`. It is pushed, with **no PR** until the coordinator says so (packet header). It implements packet §1, §1a, §2 and §3 and the four `/v7` preconditions. Packet §4's Windows verification passes on its committed bytes. It stops at the packet's §5 push-and-return, **before any Linux run**.

The build is TEST_ONLY at reduced depths (packet §0: "reduced TEST_ONLY depths, to be reported distinctly from reference-depth qualification"). It is not an S5 acceptance, a C3 decision or a qualification.

## 2. Scope (by reference; the packet governs)

| Item | Owner text |
|---|---|
| Interfaces, including the pre-decision prefix-custody form chosen and reported in the §1 freeze | Packet §1 |
| Stage 1c measurement seam: SR-1..SR-9 and P-1..P-7, with **P-3, P-4 and P-5 hard** | Packet §1a |
| Files: single writer, S5 run tooling bounded, the forbidden list | Packet §2 |
| Behavior: the three verbatim assertions and the five checklist lines | Packet §3 |
| Decisions S5-D1..D3, which are constraints, not options | Packet §0.5 |
| `/v7` preconditions 1–4 | CP-1b ruling (§0 above) |

**Not in scope:** the coordinator's Stage 1c harness (packet §1a, last paragraph); T05's modules and `seal.py`; D3's bounded same-sample re-execution (a separate slice); RC-2 owner text; any production value.

## 3. Method

1. Run the §9 premise check and report it.
2. Do the Rule 0 reads (packet §0, §0.1). Report every anchor and every closed `{'N1','N2'}` set site in the §7 return, as packet §0 requires.
3. Build the adapter boundary tests before wiring (packet §3, first checklist line).
4. Integrate through the route. Report every `part_a.py` line touched as a store-free seam (packet §1, §2).
5. Run the Windows verification (§4) on committed bytes. Keep source and Git state unchanged while a recorded check runs (AGENTS.md).
6. Push `claude/s5-part-a`, and return under §6. Do not push while any recorded check is running.

A numerical behavior discrepancy, or a float-versus-Decimal disagreement, **returns to the coordinator before any accepted formula changes** (packet Authority line; §3 parity line). It is never absorbed by a tolerance.

## 4. Verification (falsifier-first)

This section adds no requirement. It restates the packet's and the ruling's requirements as the checks the coordinator applies to the return, and names the section each comes from.

**H:** the build on `claude/s5-part-a`, cut from `05f3788`, meets packet §1–§3, the four `/v7` preconditions and the Windows part of packet §4, and it stops before any Linux run. **Reject if** any item below is falsified; **accept for C3 step 1 review if** all hold on the returned head.
- **Premise first** (§0, §9). *Falsified by* an edit before the premise check was reported, or a premise failure that did not stop the work.
- **Base** (§1). *Falsified by* a branch that does not descend from `05f3788`, or a `git diff --stat 05f3788...HEAD` showing a file outside packet §2 (installed fixtures, `fixture_producer.py` among them, are inside it).
- **`/v7` preconditions** (§0). *Falsified by* a `/v7` release refused, unfunded, or bound to 120 s N2 CPU, or bound to the unextended fixture cap. Each is pinned by a test in `test_profile.py`, or in the Part A tests for the fixture cap.
- **Seam exclusion** (packet §1a). *Falsified by* a missing SR, or a failing or missing test for any of P-1..P-7. P-3, P-4 and P-5 are hard.
- **Prefix custody** (packet §0.5 S5-D1; §1, the correction for finding 5). *Falsified by* an expansion decision evaluated, or a panel at index `initial_panels` or above sampled, before the initial-prefix artifact is fsynced. The focused ordering test must pin this.
- **Behavior** (packet §3). *Falsified by* a missing verbatim assertion, a missing rejection among the five, or an interruption that relaunches.
- **Windows verification** (packet §4, Windows line). *Falsified by* any of these:
  - line 1 (the S4 selection plus `test_campaign_part_a.py` plus the §2 extensions, `--workers 2`) with a skip or a failure;
  - line 2 or line 3 failing on committed bytes;
  - `check` not completed with exit 0 and `source_stable: true`;
  - `git diff --check` not clean;
  - fail-on-base not shown: `part_a_worker` refused on `/v6`, and `validate_campaign_checkpoint('PART_A')` refused by the S4 builder.
- **No Linux run** (§5). *Falsified by* any workflow dispatch, `gh workflow run`, or artifact download under this card.
- **Existing tooling behavior** (packet §2, "Existing S2–S4 behaviour is preserved"). *Falsified by* a changed `s2`/`s3`/`s4` result, a changed default mode (`s4`), or a changed `DEFAULT_SCOPE` (`S4_JOINT_N2`).
- **Return shape** (§6). *Falsified by* a missing item of §6's list or a missing §1a conformance table. The list covers packet §5's push-and-return, the Windows-producible C3 items of packet §1 line 70 (the `/v8` snapshot diff and the E04/E05, E06/E08/E09 PART_A ownership among them) and the Windows return items of packet §4. The Linux-only items are deferred (§6).

## 5. Forbidden

Everything in packet §6 and §2's forbidden list, plus these, which bound this card's grant:
- **any Linux or CI dispatch**: `gh workflow run`, `-f mode=s5`, a subset iteration, or an artifact download. Neither is in this card. Every `s5` dispatch, the subset iteration first (packet §4), needs its own grant at C3 (packet §2), and the acceptance-grade run is the C3 step 2 separate dispatch grant (packet §5);
- opening a PR, merging, or pushing to `main`;
- the Stage 1c harness, the Stage 1c or Stage 2 measurement, and the `bind_budget` execution. These are the coordinator's, at C3 step 1 (packet §5);
- any production value, budget or cap; any `/v7`-gated PART_A constant (§0); any change to a locked or frozen control;
- files outside packet §2;
- `.env`, credentials, private sources or private evidence in any `glm_agent` task or workdir;
- `git stash` (use a WIP commit); a commit without `git diff --stat`;
- claiming acceptance or a C3 decision.

## 6. Output and return (status taxonomy)

- Branch `claude/s5-part-a`, pushed, with no PR.
- The packet's §7 "Executor return" section, filled in on that branch. It carries every item that packet §5's push-and-return list names, every C3 item of packet §1 (line 70) that a Windows build can produce, and the Windows-producible items of packet §4's return line:
  - the head, and `git diff --stat 05f3788...HEAD`;
  - the line-1 record, and the line-2, line-3 and `check` records, each cited by its `record.json` path and SHA-256 with its actual counts and skips;
  - the §1 freeze as a table, including the custody form chosen;
  - the §1a conformance table, with the node IDs for P-1..P-7;
  - the fixture ledger, fail-on-base, the parity results, and the `/v7` release and profile digests;
  - the PART_A field sets, the `/v8` snapshot diff, the two-artifact capture contract with its crash semantics, and the baseline-transport contract (packet §1, line 70);
  - the E-case ownership for E04 and E05 and the PART_A halves of E06, E08 and E09 (packet §1, line 70);
  - the reduced TEST_ONLY depths, stated distinctly;
  - every closed-set site and `part_a.py` seam line;
  - anything S5-D1..D3 did not anticipate.

  The Linux-only return items of packet §4 (run IDs with record hashes, the initial and final prefix identities per Linux campaign, and the SR-8 export fields) are deferred to the post-grant run. Their absence does not make this return incomplete.
- For each GLM ticket, the coordinator's diff-read note: files touched, tests run, and keep or revert. Include the git checkpoint revert line when one is present.

**Status.** The return states exactly one:
- `DONE`: every §4 item holds on the pushed head, and the return is complete.
- `DONE_WITH_CONCERNS`: as `DONE`, plus a named concern that the coordinator adjudicates at C3 step 1.
- `NEEDS_CONTEXT`: a §7 stop that is an ambiguity or a contradiction: in the packet, between the packet and the code at `05f3788`, or in the premise check. Name it with the evidence and stop.
- `BLOCKED`: any other §7 stop, named. Stop.

The coordinator either accepts the return for C3 step 1 review (verdict RESOLVED: every §4 item holds) or corrects it (verdict FALSIFIED: an item fails, named, returned to the executor as a C3 nonconformance under packet §1a). It records the verdict in the execution-slices ledger.

## 7. Stop conditions (return to the coordinator; do not work around)

- The premise check fails (§9).
- A numerical behavior discrepancy, or a float-versus-Decimal disagreement (packet Authority line; §3).
- The build needs a file outside packet §2, a `part_a.py` change that alters a seed, sample, decision input or prefix byte, or an accepted formula or tolerance change beyond SR-7.
- An anchor in packet §0.1 does not match the code at `05f3788`.
- Any step would need a Linux run, a CI dispatch, a PR, a merge or a production value.
- Two failed corrections of the same issue (AGENTS.md), or one GLM ticket failing twice (§0.5).

## 8. Decision unlocked

A `DONE` return opens **C3 step 1** (packet §5), the coordinator's review. It has four parts:
- the interfaces and the §1a conformance table, with P-3, P-4 and P-5 hard;
- the Stage 1c measurement through the SR-3 callable, run only after the coordinator's recorded read of the `--stage 1c` harness diff. Its M̂₁c is read against the carried memory margin: 1.35%, or 0.78% on the all-repeats reading (CP-1b ruling). A figure that erodes it goes to an operator ruling;
- the executed `bind_budget` Σ check on the built `/v7`;
- the RC-2 owner text, accepted and applied.

Linux runs follow packet §4's order, subset iteration first, and every `s5` dispatch needs its own grant at C3 (packet §2): the subset iteration first, then C3 step 2, the **separate dispatch grant** for the acceptance-grade Linux run (packet §5). Then the run, then Stage 2/PA-5, then S5 acceptance. T05 integration preparation may start once C3 is accepted. Integration acceptance still waits on full S5 acceptance (deployment checklist, S5 → T05 → S8 row).

**Not granted:** the Stage 1c harness or measurement; any Linux or CI run; C3; S5 acceptance; any production value, budget or cap; production qualification, activation, arm, deployment or trade; any change to a locked or frozen control.

## 9. Dispatch record

- **Dispatch-time premise check** (reported before any edit; the first three items are the executor's, the last two the coordinator's, run before the first `glm_agent` call):
  - `HEAD` of `claude/s5-part-a` is `05f3788` at branch creation, or descends from it;
  - the S5 packet at the dispatch revision is byte-identical to the packet at `05f3788` (SHA-256 of `git show 05f3788:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md` = `058c265e48a81adbde049cdb108858c6a093c2c58e872ee48000dcc05e9d68c9`);
  - no file under `ops/`, `core/`, `tests/`, `scripts/`, `tools/` or `.github/` differs between `05f3788` and the dispatch revision. If one does, the anchors the packet covers are re-checked first (packet line 5), and the executor returns `NEEDS_CONTEXT`;
  - this card at the dispatch revision matches the text the coordinator hands to `glm_agent`;
  - the `glm_agent` workdir holds no `.env`.

  Any failure is a stop.
- **2026-09-28 (drafted):** carded on the operator's instruction "draft the S5 build handoff". At drafting, `origin/main` was `d86f6ff`. Against `05f3788` it changes no code (`git diff --stat 05f3788 d86f6ff` over the paths above is empty), and the packet is unchanged (same digest). **Owed:** coordinator review, then the operator's merge, then the dispatch with the frozen SHA recorded here.
- **2026-09-28 (review folded):** one focused read-only reviewer on `6bf194d` returned 4 FIX and 3 NIT, no BLOCKER. All seven are folded, each checked against its source first: (FIX 1) `fixture_producer.py` is a §2 installed fixture (S4 packet line 96), so the "outside §2" carve-outs are removed; (FIX 2) the CP-1b ruling is absent at `05f3788` and is read at the dispatch revision; (FIX 3) §6 adds the packet §1 line-70 items and defers the Linux-only return items; (FIX 4) seven §2 test files join the acceptance list, with the journal-snapshot test at its actual path `tests/ops/qualification/test_journal_snapshot.py` (the reviewer's `execution/` path does not exist); (NIT 1) the subset-iteration grant is separated from the C3 step 2 grant, subset first; (NIT 2) `DISPATCH` replaces the `<dispatch-sha>` placeholder; (NIT 3) every §10 test prints a failure line, and the two `glm_agent` premise items are the coordinator's. The four CP-1b anchors were re-read on `d86f6ff` and hold, and `origin/main` was still `d86f6ff`.
- **2026-09-28 (fold reviewed):** one focused reviewer on the fold (`f178c17`) found no BLOCKER, 1 FIX and 4 NIT, all applied. The FIX widened §4 "Return shape" to match §6. The NITs: the new-file and Windows-set note under the acceptance list; the grant wording now follows packet §2's "any dispatch"; a `DISPATCH` guard in §10; and the §10 hooks labelled by runner.
- **2026-09-28 (dispatch SHA recorded):** the operator merged #547 at 19:53:16Z. **Dispatch revision: `eef77836473f7bc304018217f452fb68daa40f17`**, the merge commit, which carries this card.
  - The card at that SHA is byte-identical to the Codex-accepted head `f98380d`.
  - Premise items 2 and 3 re-checked against it: the packet digest is still `058c265e…d68c9`, and `git diff --quiet 05f3788 eef7783 -- ops core tests scripts tools .github` is clean.
  - The later commit that records this SHA changes only this line, the Status line and the §10 `DISPATCH` value. The card text handed to `glm_agent` is the one at `eef7783`.
  - Recording the SHA dispatches nothing. The GLM dispatch still needs the coordinator's grant.

## 10. Audit hooks (runnable)

```bash
# Coordinator, at the dispatch revision (a worktree cut from 05f3788 does not contain this card).
# Card form and authority block, through the checkout's launcher. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-09-28-s5-test-only-build-dispatch.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-28-s5-test-only-build-dispatch.md

# §9 premise check (Git Bash). Set DISPATCH to the frozen SHA recorded in §9.
REL=05f3788d9e4895308d6734e650a42875c59f669c
DISPATCH=eef77836473f7bc304018217f452fb68daa40f17
git rev-parse --verify -q "$DISPATCH^{commit}" >/dev/null || echo "FAIL: DISPATCH not set to a commit"
git merge-base --is-ancestor "$REL" HEAD && echo "descends from the release head" || echo "FAIL: not descended"
test "$(git show "$REL":docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md | sha256sum | cut -c1-64)" \
  = 058c265e48a81adbde049cdb108858c6a093c2c58e872ee48000dcc05e9d68c9 && echo "packet pinned at the release head" || echo "FAIL: packet digest"
git diff --quiet "$REL" "$DISPATCH" -- docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md && echo "packet unchanged at dispatch" || echo "FAIL: packet changed"
git diff --quiet "$REL" "$DISPATCH" -- ops core tests scripts tools .github && echo "no code drift since the release head" || echo "FAIL: code drift; re-check anchors, NEEDS_CONTEXT"
# Coordinator, before the first ticket: diff each ticket's quoted card text against
#   git show "$DISPATCH":docs/briefs/handoffs/2026-09-28-s5-test-only-build-dispatch.md
# then, in the glm_agent workdir:
test ! -e .env && echo "no .env in the workdir" || echo "FAIL: .env present"

# Scope at return: only packet §2 files (installed fixtures included).
git diff --stat "$REL"...HEAD
```
