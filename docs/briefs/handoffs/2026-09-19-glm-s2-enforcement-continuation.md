# GLM continuation — S2 enforcement integration, PR #436

Use superpowers:executing-plans and the repository's applicable implementation/review workflows. Read this contract and the referenced durable records before editing. This is the S2 enforcement task, not the separate qualification-host issues #423/#424.

## Stocktake checked by Codex

At drafting, GitHub reports:

- Draft PR https://github.com/Joshua-Asante/first-passage/pull/436 is OPEN on `claude/s2-enforcement-gaps-fab5e6`, head `cce72c9ef6189adb4bef57135ee05351bc7c8784`.
- G2 service-side work is recorded as component-accepted at `d60c242` and included in the integration branch. Claude reports 406 execution-package tests with zero skips and three G2 Linux cases passing on runs 35472053638, 35473241020 and 35474214547. This continuation has read the durable return but has not independently revalidated all those artifacts.
- G1 supervisor branch `claude/s2-g1-supervisor-enforcement` is at `efd91c4664d6e3c6efd8a7a2c4160884e347399a`. Its interim return is in section 7 of its handoff. The three repairs after the 9/12 run are implemented and reported Windows-green, not yet Linux-accepted.
- Run 4, https://github.com/Joshua-Asante/first-passage/actions/runs/35478031666, is **in progress**, at that exact G1 head. Provisioning and host facts succeeded; targeted S2 execution was running. Refresh this status first; do not dispatch a duplicate merely because the handoff says it was running.
- PR #436's body is stale: it still cites G1 `ddf76c2` and run 3. Its ledger already points to the newer return. Update the body when returning verified current status.
- S2 is **INCOMPLETE / NOT ACCEPTED**. S3 preparation is read-only; no S3 dispatch or activation is authorized.

The five-gap count does not imply only two supervisor obligations remain. G2's accepted outcomes cover funded VOID authentication, pending-cancellation behavior and admission retry/restart handling; G1 still owes integrated evidence for payload CPU enforcement, pre-bootstrap deadline enforcement and identity-gated completion, including the associated recovery repairs.

## Execution contract

**Selected outcome:** Deliver PR #436 with G1 and G2 integrated, the twelve registered S2 Linux cases genuinely exercised on the final integrated source, relevant local verification complete, and an evidence/review packet ready for Codex acceptance. Fix in-scope failures and cross-component defects needed for that outcome.

**Prerequisites:** Refresh remote heads and run 4; inspect local changes before using any checkout; read the governing roadmap/specification, both G1/G2 packets and the PR #434 review. Use the operations launcher from the checkout being tested. Disposable GitHub-hosted qualification runs are available through the existing S2 workflow. A green workflow badge alone is not sufficient evidence.

**Ownership:** GLM is the continuation implementation/integration owner. Codex is the returning coordinator and independent reviewer, retaining final S2 acceptance. Component acceptance of G2 does not override a confirmed integration defect. No parallel agents are necessary to resume; do not recreate the prior 21-agent review exercise.

**Verification:** Bind every claim to source SHA/fingerprint, interpreter, command, record/artifact paths, counts and skips. Inspect record completion/exit, source stability, capture completeness, report errors, twelve exact invariant node IDs and cleanup receipts. Run the merged local selections prescribed in the original packets and the final integrated S2 workflow. Disclose missing or failed checks rather than substituting unrelated green results.

**Checkpoint:** Record run-4 disposition, confirmed diagnoses, integration conflicts and verification in the existing execution-slices ledger. Report a consequential scope/contract conflict to Codex before dependent changes. Routine fixes within this selected outcome are authorized. Preserve evidence and source at each stable checkpoint.

**Return boundary:** Return to Codex after the final integrated test/evidence packet is ready for review, or with a concrete blocker and preserved partial result. Updating/pushing the existing work branches and draft PR #436 for the required CI is within this continuation; do not create another PR, merge to main, mark S2 accepted, activate anything, close unrelated issues or dispatch S3. Codex's review and acceptance entry follow this return.

## Durable inputs and workspace

Read these at the relevant branch heads, not from the stale shared checkout:

1. `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` — governing execution roadmap and coordinator checkpoint.
2. `docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md` — governing behavior and resource/authority constraints.
3. `docs/briefs/handoffs/2026-09-19-full-e1-s2-g1-supervisor-enforcement.md` — complete assignment, especially section 0.5, verification section 2.6 and interim section 7, on G1 `efd91c4`.
4. `docs/briefs/handoffs/2026-09-19-full-e1-s2-g2-service-metering.md` — accepted component contract and section 7 return.
5. `docs/notes/audits/2026-09-19-pr434-s2-host-fixes-independent-review.md` — five advisories, not a blanket dismissal of integration concerns.
6. Applicable AGENTS.md and the S2 workflow `.github/workflows/qualification-s2-supervision.yml`.

Observed local checkouts (recheck status/branch/HEAD; never reset or overwrite uncommitted work):

- Integration: `C:/Users/joshu/multi_firm_operations/.claude/worktrees/pr-363-babysit-671b91`.
- G1: `C:/Users/joshu/multi_firm_operations/.claude/worktrees/agent-a2bce9c0a6c68d602`.
- G2: `C:/Users/joshu/multi_firm_operations/.claude/worktrees/agent-aba80bda5cfb20250` (locked worktree; do not remove/unlock it).

Reuse valid isolation or create an isolated checkout using the worktree workflow. Never stash/reset other work. Do not reimplement accepted G2 from the summary.

## Remaining work, in order

- [ ] Read run 4 on the exact G1 head. If still running, let it finish and perform independent source/review preparation; avoid duplicate expensive runs. If failed, download its retained artifacts and inspect the precise failed nodes, recorder and cleanup rather than guessing from the job summary.
- [ ] Review G1 section 7 against the source and evidence. Its previous startup failure was a class-indentation error that left `observation` and `cleanup` as unreachable nested functions while mock-runtime tests passed. Preserve the concrete adapter regression and verify actual runtime behavior.
- [ ] Resolve the evidence/semantic questions below. Reproduce confirmed defects with focused regressions, repair minimally, rerun affected checks and then obtain fresh G1 Linux evidence when source changes invalidate run 4. Do not spend another 20-minute host run to rediscover a locally diagnosable defect.
- [ ] Integrate G1 into `claude/s2-enforcement-gaps-fab5e6`, preserving accepted G2. Inspect the full merge diff. Expect an invariant-manifest conflict: resolve by semantic union, retaining the seven original S2 nodes, two R2b route nodes and three G1 nodes, with no duplicates or lost non-S2 invariants. Reconcile any duplicated S2_CASES lists with the canonical manifest.
- [ ] Run doctor, then the merged Windows selections from both packets, `./fp.ps1 check` and `git diff --check` on stable integrated bytes. Relevant execution-package and host/manifest/lifecycle checks must include both owners' changes. If the isolation bridge again exceeds its bound, retain the actual failure and distinguish any alternative child-selection evidence from a passing bridge; do not claim `make audit` or any unrun gate passed.
- [ ] Push the existing integration branch and use PR #436's S2 workflow as the integrated task-2 run. Check the workflow's actual source identity (PR merge ref may differ from branch head) and bind evidence to that tested tree. A G1-only run does not establish G1+G2 compatibility. Avoid further pushes during the evidence run unless fixing a known failure; concurrency can cancel earlier runs.
- [ ] Inspect final artifacts: all twelve required S2 nodes passed, no required skips, invariants passed, record completed/exit 0, stable sources, complete capture, no report errors, cleanup successful. Inspect the relevant retained observations, not only counts. Correct misleading documentation and the stale PR description to match the final behavior and remaining limitations.
- [ ] Return the packet below to Codex. Keep the PR draft and S2 incomplete pending review closure. If Codex requests repairs, preserve this same evidence discipline; acceptance is a later coordinator action.

## Questions that must receive an explicit disposition

1. **Payload CPU test validity.** Run 3 held the upper bound but observed only 549 ms, and the repair changed `budget // 2 <= peak` to `0 < peak`. Determine why. Inspect the payload-bound artifact, unit lifecycle, cgroup counters, guardian STOP time and payload lifetime. Demonstrate that runnable descendants actually exercised the independent kernel bound while the guardian could not poll. A trivially early-exiting payload is not proof. Do not restore an arbitrary lower bound or increase ceilings merely to make CI pass; choose a justified, discriminating workload/assertion within the existing contract.
2. **Unobserved-exit proof.** The host-kill test is racy. Confirm the final case really observes exit before any retained PROCESS identity and refuses completion. A guarded no-op kill alone does not prove this. If ten attempts never exercise the target, do not silently downgrade/delete the Linux invariant or replace it with a mock-only claim; return the evidence-design conflict or implement a justified deterministic test mechanism within scope.
3. **OOM stopping and accounting.** Verify the repaired nonzero-exit path settles observations and withholds completion credit. Check the PR #434 stop-on-OOM advisory against current G1: parent `memory.events` can increment while a surviving container continues. Distinguish budget invalidation, eventual termination and immediate group termination; correct overstated claims, and implement any stop behavior owed by the accepted contract. Do not silently change expected terminal states to fit output.
4. **ABORTED predecessor semantics.** G1 reports `WORK_PREDECESSORS['ABORTED'] == ('RESERVED',)` while its packet called for ABORTED on a started unobserved exit. Trace actual transition calls and durable states. Resolve the mismatch with the governing state machine and related recovery cases; do not casually add predecessors that bypass capture/authority rules.
5. **Restart recovery for completed work.** G1 reports `recover_service` revisits completed work and can spend a new RECOVERY_OWNER slot. Confirm against integrated G2, including repeated restarts and already-retired resources. Prove no repeated charge, lost recovery capacity or newly blocked valid work. Treat the report as a claim to verify, not an accepted diagnosis.
6. **Guardian self-failure.** Confirm self-failure records IN_DOUBT and the refusal/failure event, retires what it safely owns, and leaves the service able to recover without the guardian killing itself after spending the only recovery slot.

Do not broaden this work into qexec trust redesign, larger allowances, profile/schema churn, #423/#424, or S3. Necessary contract changes beyond the selected scope return to Codex with concrete evidence.

## Useful read-only commands

```powershell
gh pr view 436 --json headRefName,headRefOid,state,body
gh run view 35478031666 --json status,conclusion,headSha,jobs,url
git status --short
git rev-parse HEAD
git diff --check
```

Run project Python only after `./fp.ps1 doctor` in the implementation checkout, through that checkout's launcher. Without PowerShell 7.3+, use the documented `python -I scripts/fp.py <command>` bootstrap. Read exact selections in G1 section 2.6 and G2's verification contract; preserve their known environmental caveats. Use `sys.executable` for child Python processes.

## Return packet

Return integration branch/HEAD, G1 and G2 included SHAs, clean/dirty state, changed-file inventory, all review-question dispositions, manifest's twelve-node inventory, local command/interpreter/results and recorder paths, final Linux run URL/tested SHA/artifact paths, source-stability/capture/invariant/cleanup results, remaining advisories and exact missing checks. Update the ledger and PR description without marking acceptance. Preserve local evidence and any uncommitted source outside disposable worktrees before removing anything.

**Current boundary:** Ready for GLM continuation; run 4 was still in progress when checked. No new implementation, merge, workflow dispatch or external message was performed while preparing this handoff.
