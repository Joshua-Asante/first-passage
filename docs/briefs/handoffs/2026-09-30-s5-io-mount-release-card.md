# S5 fix: per-work io-mount release after custody (C3 memory stop)

**Type:** cc_handoff (fix card; it closes the C3 memory stop on `claude/s5-part-a`)

**Status:** FROZEN, 2026-09-30, under the operator's GO; amended as **A1**–**A4** the same day (below):
- In the coordinating session Joshua wrote "I agree with your recommendation. Send it to the S5 agent." He confirmed it directly in the S5 coordinator session: "Confirmed, proceed".
- The ruling is recorded in the C3 ledger addendum (`docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`, the entry beginning "Full S4-plus-Part-A selection: run `36673465130`").
- This card is committed before implementation, under the committed-handoff rule.

**Executor:** the Opus escalation lane (the surface-allocation ADR, as amended by #561). It is a single writer in a detached worktree cut from this card's commit. It contains no `.env`.

**Coordinator:** the S5 coordinator session. It owns the diff review, integration onto `claude/s5-part-a`, every push and dispatch, Codex, and the ledger.

**What this card is.** Instrumented run `36678879864` attributed the C3 memory stop, run `36673465130`:
- Each work's checkpoint io tmpfs pair is created in ops code (`ops/c1_rail/qualification/execution/campaign_supervisor.py:2084-2104`).
- It is stopped only by the verification harness's campaign cleanup (`tools/qualification_verification/campaign_host.py:155-170`).
- Its pages are charged to the shared qualification slice as shmem, at +3.17 MB per work.
- At 17 pairs (53.9 MB) the slice OOMed and killed the supervisor.

The fix releases each work's pair once custody no longer needs it.

**Amendment A1, 2026-09-30 (operator ruling "Bind mounts to the work"). It supersedes §2's release table, §3 and §4 tests 1–4 where they conflict.**

The executor returned NEEDS_CONTEXT at §0.3 (§7, first stop condition), and the coordinator verified the finding:
- The guardian's fixed bus child admits only `StartTransientUnit` (`deploy/qualification/bootstrap.py:93`, `tools/qualification_verification/container_ownership.py:79-81`).
- The enrolled polkit rule admits unit-scoped actions only for names starting with the run prefix `fpq<16hex>` (`tools/qualification_verification/campaign_host.py:88-93`).
- The mount units are named `var-lib-fpq-fpq-…`, so the guardian cannot `StopUnit` its mounts in scope.

The operator chose lifecycle binding:

1. **Mechanism.** `_io_mount_properties` adds exactly two unit properties to each io mount unit: `BindsTo=<the work's guardian unit>` and `After=<the work's guardian unit>`. systemd then stops the pair when that guardian unit stops.
   - No other mount property changes: not `size=`, mode, uid, options or `CollectMode`.
   - No new privilege, no polkit change, no bus-command change.
   - Campaign cleanup stays the backstop.
2. **The release point is the guardian unit's end.** This holds only if the guardian unit ends after `retain_checkpoint_capture` (committed works) or after `_archive_part_a_for_inspection` (IN_DOUBT) on every path. The executor must prove it from the source.
   - On a pre-capture guardian death the pair stops with the guardian. That is acceptable: recovery and retry read the store only (§0.2), and those paths have no capture to keep.
3. **New stop conditions (§7):**
   - The guardian unit's name is not known when the mounts are created.
   - Any path lets the guardian unit end before custody commits while a later step still needs the mount.
   - `BindsTo`/`After` cannot be set through the existing `StartTransientUnit` property path.
   - The guardian unit is not the right lifetime owner. Return the correct owner instead.
4. **Tests (these replace §4 1–4):**
   - (1) Fake bus: each mount unit's start properties carry exactly `BindsTo`/`After` on the work's guardian unit. With a simulated guardian exit, the live pairs are bounded by the works in flight across a multi-work ordering. It fails on `072c133`.
   - (2) IN_DOUBT: the inspection archive is staged before the guardian unit can end.
   - (3) Ordering: `retain_checkpoint_capture` precedes the guardian's end; a crash between stays recoverable.
   - (4) Linux, a required node under `QEXEC-01`: after each work's guardian ends, its `var-lib-fpq-*` pair is inactive or absent. The live pair count is ≤ in-flight works throughout.
5. **§5 Forbidden is narrowed accordingly.** "Any change to … mount properties" now excludes these two properties, and only these two.

**Amendment A2, 2026-09-30 (operator ruling "Amend node (c) as proposed"). It adds to A1.**

The executor returned NEEDS_CONTEXT under A1's §7: a reader of `out_path` runs after the inspection archive. The coordinator verified it. `test_campaign_part_a_linux.py::test_s5_payload_death_between_the_part_a_writes_is_in_doubt_with_the_prefix_retained` (`:546-564`) reads the output mount from the host *after* `settled_in_doubt`. Under A1 the pair unmounts as the guardian exits, so those reads would race. The operator allowed that node to be amended:

1. **Allowed edit, this node only.** The host reads of `out_path` move to *before* settlement. The node polls while the work is RUNNING until the prefix is final: `part-a-initial.jsonl` exists with mode 0444 (the SR-4 writer chmods only after its fsync), and `statvfs(out_path).f_ffree == 0` (the one-inode cap is full). Then it reads and asserts, unchanged in content:
   - the folder listing == `[part-a-initial.jsonl]`;
   - mode 0444;
   - `f_ffree == 0`;
   - `host_prefix = read_bytes()`, with its two panels of two outcomes;
   - no final artifact and no `result.frame` at that moment.
2. **After `settled_in_doubt`, every existing assertion is kept:**
   - the states and transitions;
   - `part_a_family(state) is None`;
   - `set(staged) == {'part_a_initial_prefix'}`;
   - `staged == host_prefix` and the equal sha256;
   - the failure reason;
   - the restart checks.

   One assertion is **added**: the work's io pair is inactive or absent, which is the release.
3. **Absence of a final artifact or frame after the read** is proven by the staged set being exactly `{part_a_initial_prefix}` and by the unchanged retained failure reason (the refused final create). No assertion is removed or weakened; each is moved earlier or kept.
4. **§2 and §5 are narrowed accordingly.** This one existing node may be edited as described, and no other existing test may be. Any other reader found stops the work under §7 as before.

**Amendment A3, 2026-09-30 (operator ruling "Freeze the guardian"). It supersedes A2's read timing, and adds to A1 test (4).**

Codex's review of `eff41ca..0ab8f6b` returned two P2 findings; production ordering, custody, BindsTo and Stage 1c were confirmed.
- **P2-1, node (c):** A2's pre-settlement read still races. Mode 0444 does not hold the guardian, which can archive, settle, exit and unmount before or during the host reads. This is the first failed correction of node (c); a second failure stops the work under §7.
- **P2-2, node (4):** mount-count sampling against a constant does not establish the per-guardian lifetime bound.

1. **Node (c), a held window.** Once the work is RUNNING, the test freezes the work's guardian unit cgroup (`cgroup.freeze` = 1, then waits for `cgroup.events` `frozen 1`). It waits for the payload to exit, the final create having been refused by the one-inode cap. It then reads and asserts, from the still-mounted `out_path`:
   - the listing == `[part-a-initial.jsonl]`;
   - mode 0444;
   - `f_ffree == 0`;
   - `host_prefix` bytes and panels;
   - no final artifact and no frame.

   It then thaws the guardian (`cgroup.freeze` = 0) in a `finally`, and after `settled_in_doubt` asserts every existing assertion plus the release check, as in A2.
   - **Precondition, proven from the source before writing:** a frozen guardian for that span cannot trip service supervision, a deadline, a budget or timer, recovery, or the evidence (for example CPU or wall accounting, or a heartbeat). If it can, stop and return NEEDS_CONTEXT.
   - The freeze is test-only. No production change.
2. **Node (4), exact intervals, not sampling.** For each worker work, the test obtains the guardian unit and the io mount units' active intervals from the system journal or the manager (monotonic timestamps: mounted/unmounted, guardian started/deactivated). It asserts:
   - each pair was observed active (a positive observation);
   - each pair's interval lies within its own guardian's interval, allowing only the manager's stop after the guardian's end;
   - the pairs of different works never overlap unless their guardians overlap;
   - no pair is active after settlement.

   A run that observes no pair fails.
3. **§2 and §5 are unchanged otherwise:** only node (c) and the new node (4) may be edited in the Linux file.

**Amendment A4, 2026-09-30 (operator ruling "Archive-based on Linux"). It supersedes A2 and A3 for node (c), and A3 item 2's end-record rule for node (4).**

Codex's review of `e7c9826`/`aeabbd4` returned three P2 findings:
1. The freeze is acquired after an unprotected race: the guardian can settle and unmount before the freeze lands.
2. The freeze does not stop the guardian's CLOCK_BOOTTIME SIGKILL timer or `RuntimeMaxUSec`, so a long hold can change the outcome.
3. Node (4) takes `UNIT_PROCESS_EXIT` as a mount's end, but an unmount helper's exit is not deactivation.

Findings 1–2 are node (c)'s **second failed correction**. Under the AGENTS.md two-failure rule, the coordinator stopped and returned to the operator, and node (c) restarts with the explicit criteria below. The lesson: a host read of a mount inside production's own flow cannot be made race-free from the test side. The archive's fidelity to the mount bytes is a property of `_archive_part_a_for_inspection`, and fake-bus test (2) already proves it deterministically.

**Node (c) criteria** (`test_s5_payload_death_between_the_part_a_writes_is_in_doubt_with_the_prefix_retained`):
- (c1) No host read of `out_path` or `in_path` anywhere in the node. Remove `held_guardian`, `payload_exited` and `final_prefix` if nothing else uses them. No freeze, no SIGSTOP, and no timing window of any kind.
- (c2) Keep, unchanged, the setup (`cap_output_mount_inodes`, the RUNNING wait) and every settled assertion from `072c133`:
  - the work and attempt `IN_DOUBT`;
  - `part_a_family(state) is None`;
  - N2 `COMMITTED`;
  - no `CAPTURED`/`SIGNING_INTENT`/`COMPLETED` transition;
  - `set(staged) == {'part_a_initial_prefix'}`;
  - the retained failure reason, the refused final create after the prefix fsync;
  - every restart check.
- (c3) The prefix-content checks move from `host_prefix` to the **staged bytes**: `_prefix_panels(staged['part_a_initial_prefix'])` has indices `[0, 1]`, each with 2 outcomes.
- (c4) Add the release check: `io_pair_released(boundary, attempt, 'pawork')`.
- (c5) Fake-bus test (2) in `test_campaign_io_release.py` stays, and must assert that the staged bytes equal the pre-release mount bytes, for both the abnormal-exit and the absent-frame paths. The node's docstring names it as the fidelity proof.
- **Removed from the Linux node, by operator ruling:** the host-side listing, the 0444 mode, `f_ffree == 0`, and "no final or frame on the mount". The staged set and the failure reason cover the "no final" fact.

**Node (4) criteria** (`test_s5_io_mount_pairs_are_released_with_each_work_guardian`), a first correction:
- (d1) A unit's interval ends only at a **deactivation** record: `UNIT_STOPPED` (`9d1aaa27…`) or `UNIT_SUCCESS` (`7ad2d189…`). `UNIT_PROCESS_EXIT` is never an end.
- (d2) Any `UNIT_FAILURE_RESULT` (`d9b373ed…`) for an io mount unit, or a `UNIT_PROCESS_EXIT` with a non-zero status for one, **fails the node**. That is a failed unmount or stop.
- (d3) The guardian's end is its own deactivation record. A failed guardian result also fails the node, because this sequence is the normal path.
- (d4) Keep the positive-observation, containment (with the 30 s bound-stop grace), cross-work overlap and nothing-live-after-settlement assertions. Note in the docstring that journal timestamps are receipt times, which is why the grace exists.

**Verification for the return:**
- the manifest, boundary-verification and io-release tests, with a record;
- the Linux file collects 5 nodes, with a record;
- `git diff --check`;
- a diff showing that node (c) contains no reference to `out_path`/`in_path` reads, `cgroup.freeze` or SIGSTOP (grep output).

A failure of node (c) under these criteria, or a third correction of it, stops the work under §7.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write]
constraints:
  - no_main_write
  - no_merge
  - no_push
  - no_linux_or_ci_dispatch
  - card_section2_files_only
  - no_stage1c_harness
  - no_budget_or_limit_change
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/execution/test_campaign_io_release.py
  - tests/ops/qualification/execution/test_campaign_n2.py
  - tests/ops/qualification/execution/test_campaign_part_a.py
  - tests/ops/qualification/execution/test_campaign_recovery.py
  - tests/test_qualification_invariant_manifest.py
  - tests/test_qualification_boundary_verification.py
```

`test_campaign_io_release.py` is new (§2). The Linux node (§4, test 4) is outside this Windows-run set.

## 0. Phase 0: premise check, then Rule 0 reads, before any edit

1. **Premise.** Confirm that the worktree HEAD is this card's commit, that it descends from `072c133`, and that `git diff 072c133 HEAD -- ops core tests tools` is empty.
2. **Rule 0 reads** (read them; do not infer them). The files are `ops/c1_rail/qualification/execution/campaign_supervisor.py`, `ops/c1_rail/qualification/execution/campaign_store.py` and `tools/qualification_verification/campaign_host.py`. Within them:
   - `campaign_supervisor.py`:
     - `_run_n1_worker` in full, including `_write_worker_input` (`:1959-1975`);
     - the io mount creation (`:2084-2104`) and `_io_mount_properties`;
     - `_read_part_a_artifacts` (`:1902-1915`), `_archive_part_a_for_inspection` (`:1918-1930`) and `_bind_part_a_artifacts` (`:1932-1956`);
     - the PAYLOAD_EXIT to IN_DOUBT branches (`:2291-2342`), `retain_checkpoint_capture`'s call (`:2377`) and everything after it to COMPLETED;
     - `_recover_campaign_work` (`:556-620`) and `_run_n1_g5`/`_retry_parent` (`:2610-2660`);
     - `_guardian_bus_call` and how the guardian reaches the system manager.
   - `campaign_host.py:155-178` (cleanup stop plus absence poll).
   - `campaign_store.retain_checkpoint_capture` and `stage_checkpoint_artifact`.
3. **Unit authority.** Establish whether the guardian's bus identity may `StopUnit` the mount units it started, or whether the stop must go through another route. If it cannot, and no in-scope route exists, **stop: NEEDS_CONTEXT** (§7). Do not widen polkit or unit properties.

## 0.5. Routing (task-routing checklist, re-applied at dispatch)

This is a code fix in a protected TEST_ONLY qualification path, following a failed Linux acceptance run. The GLM ticket lane is not used: the operator's GO names the Opus escalation lane (#561). No secrets, `.env`, Pine or account data are involved. Linux runs are out of scope for the executor; the coordinator dispatches them.

## 1. Selected outcome

In a multi-work campaign, the live checkpoint io tmpfs mounts are bounded by the works in flight (at most one pair each), not by the works completed. Custody, IN_DOUBT inspection, retry and recovery behave exactly as before.

## 2. Scope

- **Edit:** `ops/c1_rail/qualification/execution/campaign_supervisor.py`, which owns the release.
- **Edit only if the backstop needs it:** `tools/qualification_verification/campaign_host.py`, where the cleanup absence poll must accept units that are already gone. Read it first; it may already accept them.
- **New:** `tests/ops/qualification/execution/test_campaign_io_release.py` (fake bus and store).
- **Linux:** a boundary node in `tests/integration/qualification_boundary/` inside the `s5` selection, either a new function in `test_campaign_part_a_linux.py` or a new file. It is registered in `tests/ops/qualification/invariant_manifest.json` under **`QEXEC-01`**, with `tests/test_qualification_invariant_manifest.py` updated if registration requires it.
- **Release points:**

| Path | Release after |
|---|---|
| Committed work (PAYLOAD_EXIT, frame present) | `retain_checkpoint_capture` (`:2377`) has returned |
| Abnormal exit or absent frame (Part A) | `_archive_part_a_for_inspection` (`:1918-1930`), **before** the IN_DOUBT transition |
| Any other exit before capture (pre-PAYLOAD_EXIT death, deadline, guardian death) | no new release; campaign cleanup covers it |
| Backstop | campaign cleanup (`campaign_host.py:155-178`), unchanged: an explicit stop plus absence poll |

## 3. Method

- Release is a system-manager `StopUnit` of the work's `in_unit` and `out_unit`, issued only after the store has committed what custody needs from those mounts.
- A release failure must never change the work's recorded outcome, state or receipts. It is logged, and cleanup remains the owner.
- No store schema change, no new state name, and no change to any mount property, limit or size.

## 4. Verification (falsifier-first)

**H:** releasing each work's io pair once custody has committed bounds the live io mounts by the works in flight, without changing any work's outcome, receipts, IN_DOUBT inspection copy, retry or recovery. **Reject if** (falsifier) any §4 test fails on the fix, any existing acceptance test changes outcome, or the Linux full selection on the fix head is not green. **Revert trigger:** any custody or recovery behavior differs from `072c133` apart from the mount lifetime.

Each test is written first and shown to **fail on `072c133`**, with its launcher record cited, then to pass on the fix.

1. **Bounded io mounts** (fake bus and store). Run a multi-work ordering: N1, N2 and Part A works in sequence, plus one exact-receipt retry. Assert that the live io-mount units never exceed **one pair per in-flight work** and are 0 once all works settle.
2. **IN_DOUBT keeps its inspection copy.** On an abnormal-exit Part A work, both artifacts (`part_a_initial_prefix` / `part_a_final`) are staged in `full_campaign_checkpoint_staged` **before** the pair is released, and the staged bytes equal the pre-release mount bytes.
3. **Ordering and crash window.** No release is issued before `retain_checkpoint_capture` returns. A crash injected between capture and release leaves the work recoverable, with the same outcome and receipts, and cleanup still stops the pair.
4. **Linux, a required node under `QEXEC-01`.** At each boundary in a multi-work sequence on one attempt, the live `var-lib-fpq-*.mount` count is ≤ 2 × in-flight works, and it is 0 after settlement. It runs in the coordinator's Linux selection.

Then, run by the coordinator:
- Windows lines 1–3, `check` and `git diff --check` on the fix head. Line 1's two known base whitespace failures are disclosed, not counted as passes.
- A closure re-run on the fix head (`docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`). `campaign_supervisor`, `campaign_store` and `campaign_host` are outside the 68-module measured closure at `072c133`, and must still be.
- A Codex review.
- One Linux full S4-plus-Part-A selection (`-f mode=s5`), read with `scripts/s2_run_evidence.py --expect-head <fix> --expect-scope S5_PART_A`.

**Clauses it must preserve (verified text):**
- **S3 D3** (`docs/briefs/handoffs/2026-09-21-full-e1-s3-n1-genuine-capture.md:30`): the output is "read by the guardian after `PAYLOAD_EXIT` and archived byte-for-byte".
- **The S3 D3 ruling** (the execution-slices ledger `:655`): "the explicit administrator stop + absence proof in `cleanup` is the ownership property". Its premise that the pages are charged to the writing worker is inaccurate (the guardian writes `in`). Record that; do not rely on it.
- **S5-D1 and the two-artifact capture** (S5 packet `:52`, `:230`): "On an abnormal exit or absent frame it archives for inspection, then goes to IN_DOUBT". Inspection is served by the archive.
- **Audit B-2** (`docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md:174`): `qg5` reads immutable captures.
- **S4 custody** (S4 packet `:25`, `:40`): N1_ONLY `executions` and T05's `checkpoint_receipts` read contract.
- **Recovery** (`:556-620`) and **retry** (`:2610-2660`) read the store only.

## 5. Forbidden

- Any change to a memory limit, `memory_bytes`, `MemoryMax`, THP, the profile, release documents or `size=` values.
- Any file in the 68-module measured Stage 1c closure, and any Stage 1c harness file.
- `core/` and `lab/`.
- Any store schema change, any new progression or state name, and any relaxed assertion.
- Pushing, opening a PR, dispatching any workflow, merging, or writing to the ledger.

## 6. Output and return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict on the return is RESOLVED (every §4 item holds) or FALSIFIED (an item fails, named, and returned to the executor). The return contains:
- the diff (`git diff --stat` plus the full diff);
- each §4 test's fail-on-base and pass-on-fix launcher records;
- the result of the §0 unit-authority finding;
- any clause from §4 the change touches, with its reasoning;
- the concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- The guardian cannot stop its mount units through an in-scope route (§0.3).
- Any reader of `in_path`/`out_path` is found after `retain_checkpoint_capture`, or after the inspection archive.
- A §4 test cannot be made to fail on `072c133`.
- A §5 file would need to change.
- Two failed corrections of the same issue.

## 8. Decision unlocked

With a green Linux full selection on the fix head and Codex RESOLVED, the C3 Linux grant resumes at Stage 2/PA-5. For TEST_ONLY, PA-5 is CPU-only (operator ruling 2026-09-30, option (a)). The held C3 addendum PR can then be opened.

## 9. Dispatch record

- Base: `072c1334c932c4c48f6a98fca7ab42c8d77ce7bf`.
- Dispatch revision: the commit that adds this card on `claude/s5-part-a`. The coordinator records it in the ledger.

## 10. Audit hooks (runnable)

```bash
# Card form and authority, through the checkout's launcher. Expected: RESULT: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-09-30-s5-io-mount-release-card.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-09-30-s5-io-mount-release-card.md
# Premise (Git Bash), in the executor worktree.
git merge-base --is-ancestor 072c1334c932c4c48f6a98fca7ab42c8d77ce7bf HEAD && echo "descends from 072c133" || echo "FAIL"
git diff --quiet 072c1334c932c4c48f6a98fca7ab42c8d77ce7bf HEAD -- ops core tests tools && echo "no code drift" || echo "FAIL: code drift"
test ! -e .env && echo "no .env" || echo "FAIL: .env present"
# Scope at return.
git diff --stat 072c1334c932c4c48f6a98fca7ab42c8d77ce7bf...HEAD
```
