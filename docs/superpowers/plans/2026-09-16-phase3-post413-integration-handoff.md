# Phase 3 Post-413 Signed Qualification Integration Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the preserved Phase 3 qualification implementation onto the post-413 baseline and independently accept its genuine signed synthetic source-to-dispatch-to-replay-to-result-to-seal route.

**Architecture:** Reuse the preserved qualification controller, source factory, signed trust domains, durable attempt journal and adjudicator. Selectively reconcile these with the accepted Phase 2 runtime instead of replacing current runtime files with old branch versions. Use PR 413's validated operations launcher and automatic source-bound verification records for acceptance.

**Tech Stack:** Existing Python operations environment, Ed25519 signing fixtures, pytest, durable journals, retained synthetic source files and `fp.ps1` verification tooling; no new execution service or production command surface.

**Spec:** [Phase 3 simplified plan](2026-09-16-phase3-simplified-qualification.md), work package 1; preserved `docs/briefs/phase3-preparation/2026-09-15/paused-checkpoint.md`; recovered `preflight-g5-unreviewed-checkpoint.md`; accepted qualification contracts and their existing tests.

## Global Constraints

- **DRAFT HANDOFF, 2026-09-16.** The current request authorizes drafting this handoff, not executing it. Once execution is separately instructed, its scope is the engineering integration and synthetic acceptance described here.
- Stop before actual source acceptance, F1 freeze, exact-depth approval, E1/n3 outcome-bearing execution, D0 admission, ORB GO, B7, provider actions, deployment or arming. Do not request those decisions merely to finish synthetic engineering.
- Preserve merged PR 409 behavior and PR 413 launcher/evidence tooling. Historical component passes are context, not acceptance of the integrated successor.
- Preserve all existing worktrees and primary-checkout untracked files. Use a new isolated integration worktree; do not rebase/reset the preserved branches or clean their files.
- Keep private inputs/outputs under approved ignored primary-checkout roots. This slice uses synthetic retained sources and TEST_ONLY authority; it needs no production credentials or account evidence.
- Do not weaken signature, identity, runtime-closure, source-issuance, one-attempt or no-redraw checks to make old fixtures pass.
- Tests must use the launcher belonging to the checkout being tested. Run doctor before project Python; diagnose environment failures rather than bypassing validation.
- One coordinator owns the complete integrated behavior and evidence. Independent review must evaluate the whole route, not just individual modules.

---

## Verified starting points

| Artifact | Revision / location | Disposition |
|---|---|---|
| PR 409 merge | `845fb13ed2141482649627f5b78a51f4cadbd61d` | Accepted Phase 2 offline runtime; preserve its settlement, feedback, command, capacity, cutoff and startup-clock fixes |
| PR 413 merge | `b4aa8efb0ee8f6d40b5aa332d5bb850bfa8b68ac` | GitHub confirmed MERGED while drafting; required baseline ancestor |
| PR 413 tested head | `89bd29194af772c937f21ead3370c4ec53b9a15c` | Historical tooling validation, not a Phase 3 pass |
| Preserved qualification branch | `codex/phase3-qualification-tooling`, HEAD `35fae36169f056600286081c44edcc53bf618880` | `.worktrees/phase3-f1-preparation`; last engineering `8f09a6266be671890cf4e0693664612eeded7a8a` |
| Recovered preflight/G5 work | `f9ff974decef0c7f008fd1998ae0621697283a86` | `.worktrees/phase3-qualification-control`; reconstructed two-file diff, unreviewed/incomplete; base `6dfca2ba5f73a3b0573c03483d45c2bdf9b4a866` |
| Local cached `origin/main` at drafting | `845fb13` | Stale relative to 413; refresh before selecting an execution base |

Read the preserved checkpoint rather than interpreting old green counts as a complete pass. It explicitly records unfinished domain-aware preflight/G5, fixture migration, full signed composition, final combined tests and independent whole-flow review. Prior timing results are provisional and do not establish an accepted compute budget.

This handoff narrows the earlier `2026-09-15-phase3-completion-handoff.md`: do not inherit its later F1/E1/admission sequence as part of this slice. The new engineering acceptance record should reference the historical pause without rewriting it as if work had already completed.

## Task 1: Establish the integration baseline and inventory

**Outcome:** A new worktree contains a known post-413 base and an explicit mapping of retained Phase 3 changes, without regressing current runtime behavior.

- [ ] Refresh origin and choose current accepted main containing both merge commits. Record exact base/HEAD and dirty state. If newer relevant changes exist, include their interface impact in the inventory.
- [ ] Create an isolated `codex/phase3-post413-integration` branch/worktree, or reuse an existing matching integration worktree only after checking its provenance and changes.
- [ ] Read this checkout's `AGENTS.md`, `scripts/README.md` launcher section, governing qualification plans, both preserved checkpoint notes and current runtime integration evidence.
- [ ] Inventory branch history/diffs by behavior: qualification-only modules; shared runtime/loader/schedule changes; tests; historical evidence/docs. For each shared change record whether main already has an equivalent, needs a qualification-specific extension, or requires an exact conflict resolution.
- [ ] Integrate coherent qualification changes selectively. Do not copy the old account owner, settlement, capacity or scheduler over main. Mixed commits such as `bb21d77` require hunk-level assessment; existing equivalent fixes should not be reapplied.
- [ ] Preserve PR 413's root instructions, launcher, recorder and lock/environment files. Do not restore historical bare-Python recipes as operative instructions.

**Starting file footprint:** `ops/c1_rail/qualification/`, `tests/ops/qualification/`, the qualification loader/runtime-inventory consumers and existing Phase 3 preparation documents. Shared runtime files may need narrowly justified compatibility work; unrelated runtime redesign is outside this slice. Record the exact dependent behavior before expanding the footprint.

**Deliverable:** An integration inventory in `docs/briefs/phase3-preparation/2026-09-16/post413-integration-acceptance.md`, with source commits, selected baseline, retained/equivalent/rejected changes and unresolved integration defects. This record is evidence, not a new governing contract.

## Task 2: Complete trust-bound preflight and result/seal composition

**Outcome:** The validator-issued contract/domain flows through retained sources, durable dispatch, replay and authenticated result/seal without a substitutable identity or authority boundary.

**Files:** `qualification/{contract,trust_domain,preflight,attempt,production_source,production,orchestration,result_adjudication,seal}.py` and their existing tests. Read the recovered `f9ff974` diff; it is a repair starting point, not an accepted implementation to cherry-pick blindly.

**Existing interface anchors to reconcile:**

```python
exact_depth_subject(contract, *, attempt_id)
validate_e1_preflight(contract, *, attempt_id, output_root,
                     exact_depth_approval_bytes, trusted_keys, now, trust_domain)
run_production_e1(contract, *, source, store, preflight,
                  exact_depth_approval_bytes, trusted_keys, now)
authenticate_result(result, authentication_bytes, *, trusted_keys, now, trust_domain)
commit_authenticated_result(attempt_store, result, *, trusted_keys, now, trust_domain)
seal_e1_pass(result, seal_record_bytes, *, sealed_utc, trusted_keys, now,
             result_trusted_keys, attempt_store, trust_domain)
```

These names exist in preserved code; reverify final signatures and callers together. `run_production_e1` must reject TEST_ONLY authority. The internal `_run_composition_e1` test route must use the same core execution behavior under the signed test domain, never promote its results to production.

- [ ] Run the existing signed composition test to expose integration failures, retaining the failed run evidence. Begin with `test_signed_composition_uses_real_source_dispatch_replay_and_g5_across_reopen` in `test_composition_route.py`.
- [ ] Bind preflight, retained receipts/checkpoint plans, result authentication/commit and seal to the validated domain and actual enrolled key bytes. Same key ID with different key bytes must not pass.
- [ ] Migrate remaining unit fixtures to genuine signed domains and validator-issued objects. Keep fixed synthetic test clocks internally consistent; do not use wall-clock expiry failures as a reason to relax validation.
- [ ] Preserve source factory issuance and derived-state digest checks, retained-byte rehashing, original executor contract/source/store/domain binding, single initialization and immutable runtime inventory/adjudication binding.
- [ ] Fix each demonstrated defect with a reproducing failing case and minimal repair. Check related producers/consumers and equivalent validation paths when the defect involves shared state or duplicated validation.
- [ ] Keep preflight's fresh-output-root reservation distinct from read-only inspection; keep attempt reopen/boot ownership distinct from status. Partial persistence or uncertain dispatch cannot allocate a replacement sample.

**State ownership:** G1 issues the frozen validated contract; the domain binds enrolled authority; the retained source factory binds source bytes/derived state; `AttemptStore` owns attempt and dispatch/checkpoint history; the adjudicator owns result validation; enrolled result/seal roles authenticate actual digests. No caller-supplied `PASS`, public synthetic flag or reconstructed dataclass substitutes for those transitions.

## Task 3: Demonstrate the signed route and rejection matrix

**Outcome:** Real synthetic source bytes traverse actual validation, dispatch/replay, adjudication, signed result commit and seal, with evidence surviving reopen and failures.

- [ ] Pass the complete positive composition using retained synthetic sources, actual signed G1/exact-depth/result/seal subjects and actual journal persistence. Demonstrate the same attempt and committed identities across reopen.
- [ ] Prove production entry points refuse signed TEST_ONLY input and no test receipt/result/seal grants production permission.
- [ ] Execute the existing negative cases and extend only where the integrated behavior reveals a missing boundary. Do not replace the end-to-end path with a hand-built successful result envelope.

| Boundary / event | Required observable result |
|---|---|
| Replacement key with enrolled ID; independently signed foreign domain | Reject at the consuming boundary; no new authority or checkpoint |
| Contract/source/store/domain cross-wire; import alias identity mismatch | Refuse mismatched issuance/identity, preserving prior durable state |
| Retained source mutation or copied/mutated derived source; executor reinitialization | Refuse substitution; no altered replay accepted |
| Receipt persistence failure, crash/reopen after possible dispatch | Preserve uncertainty and original attempt; no redraw or duplicate stage |
| Changed runtime inventory or adjudicator dependency | Reject stale closure/evidence rather than accepting matching labels |
| Result replacement, wrong attestation scope, wrong attempt or seal-before-commit | No authenticated commit/seal of substituted or incomplete output |
| Duplicate commit/seal and lost response | Follow existing idempotency rules or reject; never substitute a second result |
| Expired approval before a durable dispatch | Refuse that dispatch; retain completed prior state |
| Shared runtime integration | Preserve current 409 command/settlement/capacity/schedule behavior under affected regression tests |

A green synthetic route establishes engineering acceptance only. Missing private source/settings/calendar facts stay at their actual consuming gates; no production capability claim follows.

## Task 4: Verify with the post-413 launcher and obtain whole-flow review

**Outcome:** The final stable source state has reproducible recorded tests, explicit skips/limitations and independent review of the complete contract.

Run from the integration checkout, serially:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python -m pytest tests/ops/qualification/test_composition_route.py -q
.\fp.ps1 python -m pytest tests/ops/qualification -q
.\fp.ps1 test-ops -q
.\fp.ps1 check
```

Without PowerShell 7.3+, use `python -I scripts/fp.py <command>` for the equivalent bootstrap. Do not invoke system Python for project execution or borrow another checkout's launcher. Project-spawned Python uses `sys.executable`. Keep the research environment separate.

- [ ] Run doctor before the first project Python command. Record interpreter and environment. Confirm the optional signing dependency is present: a skipped signed positive route does not satisfy this slice. Resolve environment problems through the documented setup procedure.
- [ ] Preserve failing focused records during repair. On final stable bytes, run the positive/negative composition, full qualification suite, operations suite and repository gates above; run any additional required checks selected by affected manifests.
- [ ] Inspect automatic verification records and JUnit results. Acceptance requires `completed`, verification exit zero, complete capture, stable source and execution of the decisive signing tests. Exit zero with relevant tests skipped is insufficient.
- [ ] Keep HEAD/index/files stable during recorded checks. PR 413 does not fingerprint ignored/external inputs, so retain the synthetic input/domain/runtime digests in the test evidence as well.
- [ ] Obtain independent whole-flow review covering source → authority → durable attempt → result → seal, with the rejection matrix and current 409 compatibility. Resolve findings and rerun affected checks on final bytes.
- [ ] Use the documented PR 413 Linux verification harness if needed for import/path/runtime parity or required image checks; preserve its actual platform limits. Do not invent Docker command flags or assume the prior sequence run covered the new qualification code.
- [ ] Update the acceptance record and existing preparation `execution.md`/`tooling-review.md` with actual command, interpreter, tested revision/dirty state, counts, skips, failures, record paths and reviewer disposition. Do not claim the entire gate suite passed if any pre-existing gate fails.

No broad rerun is required merely for reassurance after accepted checks; repeat when fixes, source drift or an unresolved finding changes the tested behavior. Keep compute single-process. A synthetic engineering timing observation may be recorded, but representative budget refresh and production-data measurements are a later preparation task, not this slice's exit condition.

## Deliverables and stop point

Successful completion requires:

1. A reviewable integration diff on a base containing PR 413, with merged 409 behavior preserved.
2. Genuine signed synthetic full-route PASS and the required rejection/restart cases executed, not skipped.
3. Final source-bound qualification/operations/gate evidence, with independent whole-flow review and explicit limitations.
4. Updated preparation inventory identifying what is now accepted and what remains before F1: actual input/settings/schedule acceptance, full runtime/compute budget preparation, unresolved freeze definitions and separate operator decisions.

Commit/push/PR publication follows the execution instruction's actual scope; this drafting request does not authorize it. Do not merge or start qualification because engineering acceptance is complete. If blocked, preserve the integrated work and report the exact defect or missing environment dependency and the failing evidence record; do not request live credentials or F1 approval as a workaround.

Drafting verification: PR 413 merge identity and preserved checkpoint provenance were read; no worktree integration, Python execution, qualification test or engineering acceptance was performed for this handoff.
