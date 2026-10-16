# Q-SFCLEAR-3 fixed-leg live sizing: bounded build card

> **For agentic workers:** Execute with superpowers:executing-plans after admission, freeze and dispatch. This is one outcome; return before any follow-on gate work.

**Type:** cc_handoff (worker build card)

**Status:** FROZEN 2026-10-15 — Joshua selected option (a) and authorized this draft in the Codex chat: "Go with (a). Update to current main, draft the bounded build card, and bring it back for my code admission before building. Do not run FG." Code admission recorded from Joshua in this Codex chat: "yes i do", answering the request to admit the production-code changes in this card. Joshua subsequently authorized freeze and execution, verbatim: "Yes, freeze the card and proceed with the bounded build. Do not run FG. Bring the result back for review; every merge still needs my approval."

**Base:** fetched `origin/main` = `ecd83bb522c234a3e958f3dd223c9b3309e23661`. All source anchors below refer to this base.

**Goal:** Fixed-quantity legs reach shared live sizing without treating the source quantity as a normal-base override, matching the personal replay contract.

**Architecture:** The bundle executor and account owner each project source intents into shared sizing inputs. For `aegis_6j` and `orb_mnq_v7`, supply `None` for `normal_base`; keep the shared policy responsible for quantity, size-vector, lifecycle and mode decisions. Preserve the source intent and all other leg inputs.

**Tech Stack:** Python, pytest, existing offline synthetic brokers and project launcher.

**Spec:** TB-S1 (F), as captured by `ops/c1_rail/book_policy.py:209-214`; [run-path scope](../../notes/2026-10-12-q-sfclear-2-run-path-code-scope.md); [Q-SFCLEAR-3](../pre-registration/Q-SFCLEAR-3-verdict-preregistration.md), incorporating Q-SFCLEAR-2 except §S. This card repairs consumer inputs; it does not amend the study.

**Parent scope:** The personal lane's live-law/replay parity requirement. This is a separate production-code admission, not an extension of card D Part 1's test-only grant.

## 0. Source reads and question

Public source inspected at commit `ecd83bb522c234a3e958f3dd223c9b3309e23661` (2026-10-15):

| Boundary | Evidence |
|---|---|
| Source intent to bundle law | `ops/c1_signal_daemon/book_bundle_execution.py:160-167` passes `action.qty` as `normal_base` for every entry |
| Source intent to owner request | `ops/c1_rail/book_account_owner.py:1623-1628` passes entry `action.qty` to `BookSizingRequest` |
| Owner decision | `ops/c1_rail/book_sizing_context.py` forwards `request.normal_base` to `entry_quantities`; invalid inputs become a halted decision |
| Fixed policy | `ops/c1_rail/book_policy.py:547-594` permits absent fixed-leg `normal_base`; a supplied mismatch raises before size-vector application |
| Personal replay | `ops/c1_rail/qualification/personal_replay.py:394-403` supplies source `normal_base` only for Vanguard; Striker receives risk inputs |
| Existing parity fixture | `tests/ops/test_personal_replay_live_parity.py` uses `NORMAL_BASE` matching the fixed quantities, so its fixed-leg rows miss the below-cap source case |

**Question:** Can both live consumers admit a valid fixed-leg signal independently of its source quantity while preserving the existing shared sizing and refusal laws?

**Decision changed:** Whether this bounded live-path repair can be accepted and returned to the run-path coordinator. A synthetic result does not discharge FG.

**Budget:** One outcome; at most two correction cycles. One targeted baseline/red run, one green regression pass, one pass per named mutant, one `test-ops` and one `check` after the final code change. Diagnose failures; at the bound, return findings rather than expand scope. No paid services or real-data runs.

## 0.5. Prerequisites and admission gates

1. Joshua's code admission must explicitly cover both production paths in §2 and the synthetic regression file. Selection of option (a) authorized drafting only.
2. Joshua owns freeze; dispatch is recorded only after admission and freeze. A committed handoff must identify the reviewed card revision before execution; do not execute this uncommitted draft.
3. Refresh the build base from main at dispatch and record its full SHA. Confirm the source premise and existing interfaces still hold; a semantic conflict returns for reconciliation.
4. Reserve both production files with the coordinator before editing; respect P4/GC-5/TB-I3 writers. No concurrent writer on these files.
5. Q-SFCLEAR-3 stays frozen at F3 `15bea250fc8ee9a57b59735c9e8be685c4ddbf22`. The coordinator must account for changed code identities in any later driver binding; a previous binding is not evidence for changed code. This build does not rebind drivers or run freeze hooks requiring private inputs.

## 1. Roadmap and ownership

The larger run path remains: admit/freeze this repair card → build and review this outcome → Joshua approves any merge at its exact head after checks finish green → coordinator reconciles driver code identities and remaining FG-card decisions → separately authorized private FG → clearance run.

Only the repair is selected here. Combined run-path acceptance remains with the Deployment Coordinator; Codex coordinates this public repair while Claude is unavailable. Joshua retains code admission, freezes, VM opening and every merge approval. Private work waits for Claude.

**Selected outcome:** One reviewable patch proves the fixed-leg input projection at both consumers and verifies observable synthetic admission/refusal behavior.

**Prerequisites:** §0.5; option (a), code admission and freeze authorized; dispatch recorded in §11.

**Ownership:** Executor: Codex, single writer, public-only. Repair acceptance: Codex acting as repair coordinator, returned to Joshua for review. Combined campaign/run-path acceptance: Deployment Coordinator.

**Verification:** §4 rows and mutants, §10 commands, complete launcher records and tested source identity. No skipped required row counts as success.

**Checkpoint:** Return the draft to Joshua before implementation. Once dispatched, report first red reproduction and any premise/footprint conflict in this chat; retain evidence with the task return, not in frozen study files.

**Return boundary:** Return after the patch and required evidence are reviewable, or immediately on a blocking scope/dependency contradiction. Do not advance to merge, driver binding, FG-card amendment, private reads, VM work, FG or clearance execution.

## 2. Proposed authority and footprint

This block describes the proposed build grant and is inactive until §0.5 is satisfied.

```yaml authority
seat: worker
parent: docs/notes/2026-10-12-q-sfclear-2-run-path-code-scope.md
max_risk: low
capabilities: [repository.read, tests.run, worktree.write]
constraints:
  - admission_freeze_dispatch_required
  - public_source_and_synthetic_inputs_only
  - three_file_footprint_only
  - single_writer
  - no_private_read
  - no_fg_or_clearance_run
  - no_policy_or_frozen_constant_edit
  - no_replay_edit
  - no_existing_test_edit
  - no_vm_or_account_traffic
  - no_driver_binding
  - no_main_write
  - no_merge_or_force_push
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_fixed_leg_live_sizing.py
  - tests/ops/test_book_bundle_execution.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_live_size_vector_sizing_context.py
  - tests/ops/test_personal_replay_live_parity.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/qualification/test_personal_replay.py
```

| File | Allowed change |
|---|---|
| `ops/c1_signal_daemon/book_bundle_execution.py` | Entry `normal_base` projection only |
| `ops/c1_rail/book_account_owner.py` | Entry `BookSizingRequest.normal_base` projection only |
| `tests/ops/test_fixed_leg_live_sizing.py` | New public synthetic regressions and local test helpers |

The card itself is the planning artifact, outside the implementation diff. No new production helper/module, dependency, shared schema or configuration. Any necessary wider edit returns as a scope conflict.

## 3. Behavioral contract and implementation sequence

**Producer:** Public synthetic `OrderIntent` instances, structurally valid positive quantities, correct leg identity and side. Never import accepted runtime ports or read effective inputs.

**Consumers:** `BundleExecution.admit` and the owner's existing request-construction path into `BookSizingRequest` and shared sizing. Policy owns actual quantity; the owner retains capacity, reservations and broker dispatch. Feedback remains owned by the existing consumers. No persisted schema changes.

**Proposed projection:**

```python
# BundleExecution entry call: replace only the normal_base argument.
normal_base=(None if self.leg_id in ("aegis_6j", "orb_mnq_v7") else action.qty)

# BookSizingRequest's normal_base argument: preserve add behavior.
(action.qty if action.kind == "entry"
 and action.leg_id not in ("aegis_6j", "orb_mnq_v7") else None)
```

Keep Striker's current diagnostic quantity and explicit risk inputs, Vanguard's source ladder input, and all add/reduction behavior. Do not catch policy exceptions or relax policy validation. Do not overwrite source intent quantities. Unknown identities must still be rejected by existing identity checks.

- [ ] Read `superpowers:executing-plans` and `superpowers:test-driven-development` at execution; verify gates and establish the three-file build branch from the recorded base.
- [ ] Add §4 regressions in the new file. Reuse public helpers from `test_personal_replay_live_parity.py`, `test_four_leg_runtime.py` and `book_bootstrap_fixtures.py` without editing them. Use `dataclasses.replace` on synthetic intents to vary quantity; use an independent replay sizing callback matching personal replay's per-leg projection, not the old fixture's all-leg override.
- [ ] Run F1/F2 against unchanged production code. Require bundle failure at the fixed-base check and owner refusal at the real sizing boundary; collection/import failures are not reproduction.
- [ ] Apply only the two argument projections above.
- [ ] Run F1–F6 and the focused regressions; then each mutant independently in a disposable copy, restoring before the next. Record mutation diff, failing node and restored-source identity.
- [ ] Run the final suites/gates once source is stable, inspect complete records, and return patch, evidence and unresolved concerns. Do not commit/push implementation under this grant; any integration grant is separate.

## 4. Acceptance checks — falsifier-first

**Hypothesis:** The mismatch is solely the fixed-leg source quantity being supplied as a policy override at the two live boundaries. Reject if either boundary still refuses a valid nonmatching fixed-leg signal, or if the repair changes another leg's contract.

All vectors, bars, accounts and brokers below are public synthetic fixtures. Assert expected quantities from explicit synthetic inputs as well as cross-path equality; comparing two calls to the same helper is insufficient.

| Row | Required executable evidence | Fails if |
|---|---|---|
| F1 | Parameterize Aegis source quantities 1 through 8 through bundle and owner/runtime, with NORMAL mode, AUTHORIZED lifecycle, sufficient capacity and synthetic size base 3. Each first entry admits 3 and delivers its real synthetic fill feedback; the original intent retains its source quantity. Compare to replay with absent fixed-leg override. | A source quantity below the captured fixed base refuses, changes admission, or mutates the intent |
| F2 | ORB source quantity 2 through the same boundaries with a synthetic size base 1; separately test absent size vectors for both fixed legs using policy defaults. ORB's protected-mode rule stays fixed and adds remain governed by policy. | Either caller still passes a conflicting override, drops `size`, or changes default sizing |
| F3 | Synthetic Aegis base 0 produces bundle `shared_sizing_zero`, owner `zero_size`, replay `zero policy quantity`, exactly one feedback event per attempted entry, no broker command/fill and no owner reservation. Run with source quantity 1. | The original exception masks zero refusal, a reason changes, or zero risk reaches dispatch/reservation |
| F4 | Vanguard source quantities 1 and 2 retain distinct synthetic `base_by_port` outputs; invalid source quantity 3 is still rejected. Striker retains current risk-before-floor sizing and diagnostic rejection of out-of-range source quantity, including existing add/partial-fill regressions. | A broad removal of `normal_base` changes another leg's behavior |
| F5 | Aegis synthetic base 3 in PROTECTED mode yields the existing floor-scaled quantity; a lifecycle tier whose production multiplier is zero refuses risk. Use real consumer paths and unchanged public policy. | Mode/lifecycle scaling is bypassed |
| F6 | Direct `entry_quantities` calls with explicitly conflicting fixed-leg `normal_base` still raise; existing identity and capacity refusal tests remain green. | The fix weakens policy validation or bypasses owner admission |

**Named mutants:** M1 restore the old bundle argument (F1/F2 red); M2 restore the old owner argument (F1/F2 red at owner); M3 remove `normal_base` for every leg (F4 red); M4 drop `size` at the bundle call (F1/F3 red); M5 drop `size` from the owner's sizing binding (F1/F3 red); M6 suppress bundle zero-refusal feedback (F3 red). Run one at a time, never on an account-connected process.

**Revert trigger:** Any changed existing test outcome or surviving mutant blocks acceptance. Do not edit old tests to make this patch pass.

## 5. Forbidden moves

- FG, clearance, real-data execution, VM opening, driver binding, scoring or freeze-output inspection.
- Reads or service transmission of Pine, runtime ports, `effective_inputs.json`, e0, R1 tuple values, freeze/score/T00/replay outputs, or anything under `C:\Users\joshu\t00-step3-console`.
- Policy/constant/parameter changes, replay changes, altered refusal names, weakened identity/capacity checks, existing-test edits, or edits outside §2.
- Merge, force-push, deployment, arm, account traffic or delegated agents.

## 6. Gate and return taxonomy

**RESOLVED:** F1–F6 pass, every mutant fails its designated row, existing selected regressions and required suites/gates finish green, and the implementation diff is exactly the §2 footprint. This verdict concerns the repair only.

**FALSIFIED:** The proposed projection fails a required case or a mutant survives. **AMBIGUOUS:** evidence incomplete or a prerequisite conflicts. Neither permits build acceptance.

Return `DONE` only for RESOLVED with records; `DONE_WITH_CONCERNS` for a completed patch with explicitly unresolved evidence (not accepted); `NEEDS_CONTEXT` for missing admission, source or writer-order input; `BLOCKED — scope-problem / capability-problem / plan-itself-wrong` for the named contradiction. After two failed corrections, return for a cleaner bounded prompt on the governing escalation lane.

## 10. Audit hooks and required evidence

Run from the checkout being tested. Draft validation is separate from future implementation acceptance:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_brief.py docs/briefs/handoffs/2026-10-15-q-sfclear-3-fixed-leg-live-sizing-build-card-DRAFT.md --type cc_handoff
.\fp.ps1 python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-15-q-sfclear-3-fixed-leg-live-sizing-build-card-DRAFT.md
```

After authorized implementation:

```powershell
.\fp.ps1 --workers 2 python -m pytest tests/ops/test_fixed_leg_live_sizing.py tests/ops/test_book_bundle_execution.py tests/ops/test_book_account_owner.py tests/ops/test_book_quantity_laws.py tests/ops/test_live_size_vector_sizing_context.py tests/ops/test_personal_replay_live_parity.py tests/ops/test_four_leg_runtime.py tests/ops/qualification/test_personal_replay.py
.\fp.ps1 test-ops
.\fp.ps1 check
git diff --check
git diff --name-only
```

Record exact commands, interpreter, base and returned revision/source diff, baseline failures, red/green/mutant outcomes, and each printed `record.json`. Acceptance requires `status: completed`, exit zero, stable source, complete capture and expected reports. Cite skips and pre-existing failures; do not call the complete gate suite passing if any required check failed. Do not change source or Git state during a recorded check.

## 11. Admission record

- **Option (a) selected / draft authorized:** Joshua, directly in this Codex chat, 2026-10-15, quoted in Status.
- **Production code admission:** GRANTED — Joshua, directly in this Codex chat: "yes i do", answering "Do you admit the production-code changes described in this card?" This covers the two production paths and new synthetic regression file in §2.
- **Freeze:** GRANTED — Joshua, directly in this Codex chat, quoted in Status.
- **Committed card revision / dispatch:** The documentation-only commit containing this freeze record is the execution contract. Codex dispatches inline immediately after that commit, on `codex/sfclear3-fixed-leg-live-sizing`, from main `ecd83bb522c234a3e958f3dd223c9b3309e23661`. Both production files are reserved to this bounded public repair; no concurrent writer is known under the operator transfer. Return any discovered writer conflict before editing.
- **Merge:** a later exact-head approval from Joshua, after every check finishes green.
