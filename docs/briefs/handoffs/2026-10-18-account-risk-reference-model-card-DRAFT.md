# Shared account-risk reference model: bounded build card

> **For agentic workers:** Execute with superpowers:executing-plans after admission, freeze and dispatch. One outcome; return before any follow-on work.

**Type:** cc_handoff (worker build card)

**Status:** DRAFT 2026-10-18, proposal for Codex. Joshua asked for "a bounded Codex implementation proposal" of the shared account-risk interface. That request authorizes this draft only; code admission, freeze and dispatch are Joshua's (§0.5).

**Base:** `origin/main` = `3d396e28bd96b2717f5924279b40080f0d4285a1` at drafting. Refresh at dispatch.

**Goal:** A pure Python reference model of the account owner that implements [runbook §6](../../notes/2026-10-18-native-protection-recovery-pilot-runbook.md#6-shared-account-risk-interface) and passes every [§7 scenario](../../notes/2026-10-18-native-protection-recovery-pilot-runbook.md#7-deterministic-scenarios), with each incorrect variant detected.

**Architecture:** One deterministic reducer, `step(state, event) -> (state, outputs)`, with frozen dataclasses for configuration, events, state and outputs. No I/O, clock, broker, persistence or randomness; time arrives only as event `as_of` and `Tick`. The journal is the ordered list of `(event, outputs)` pairs, so replay is a fold.

**Tech stack:** Python standard library, pytest, the project launcher.

**Spec:** runbook §2 (rules), §6 (interface), §7 (scenarios). The runbook governs; any contradiction found returns as `BLOCKED — plan-itself-wrong`.

**Parent scope:** native protection and recovery pilot, stage P0 (runbook §3). Track B and `ops/c1_rail/` are not touched.

## 0. Source reads and question

Public source inspected at commit `3d396e28bd96b2717f5924279b40080f0d4285a1` (2026-10-18):

| Boundary | Evidence |
|---|---|
| Accepted capacity laws | `ops/c1_rail/book_capacity.py` (`_reserve`, `_fill`, `_terminal`, `apply_event`): reserve before send, whole or refuse, terminal matches fills, invalid evidence becomes a sticky block |
| Why not reuse that module | It binds the fixed four-leg book (`BOOK_LEGS`, `ACCOUNT_MICRO_CAP`, the Aegis takeover) and imports rail and daemon types; the interface needs configured legs and limits |
| Native rules and limits | Runbook §2.1–§2.8, all `⟨L-…⟩` unbound |

**Question:** Is runbook §6 complete and consistent enough that one deterministic implementation passes all of §7, with every incorrect variant failing?

**Decision changed:** Whether §6 can be frozen as the native owner's contract and P0 can use this model as its oracle. A failure sends the specific gap back to the runbook.

**Budget:** One outcome; at most two correction cycles. One red run, one green run, one run per named mutant, one `test-ops` and one `check` after the final change. No paid services, real data, platform or account.

## 0.5. Prerequisites and admission gates

1. Joshua's code admission must cover the §2 footprint. This draft is not admission.
2. Joshua owns freeze; dispatch is recorded in §11 after a documentation-only commit of the frozen card.
3. Refresh the base at dispatch and record its full SHA; if runbook §6 or §7 changed, return for reconciliation.
4. Single writer on the §2 files.

## 1. Roadmap and ownership

Admit and freeze → build → Claude (coordinator) reviews against §4 → Joshua approves any merge at its exact head after checks finish green → the coordinator records the result in the runbook. Later, separately authorized: a journal-replay adapter for NinjaScript exports, and P1.

**Executor:** Codex, single writer, public sources only. **Acceptance:** Claude as coordinator, returned to Joshua.

**Return boundary:** Return when the patch and evidence are reviewable, or at once on a scope or specification contradiction. Do not merge, touch the platform, bind limits or start P1.

## 2. Proposed authority and footprint

This block describes the proposed build grant and is inactive until §0.5 is satisfied.

```yaml authority
seat: worker
parent: docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md
max_risk: low
capabilities: [repository.read, tests.run, worktree.write]
constraints:
  - admission_freeze_dispatch_required
  - public_source_and_synthetic_inputs_only
  - four_file_footprint_only
  - single_writer
  - no_private_read
  - no_c1_rail_or_daemon_edit
  - no_policy_or_frozen_constant_edit
  - no_limit_values_bound
  - no_platform_vm_or_account_traffic
  - no_main_write
  - no_merge_or_force_push
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_account_risk_scenarios.py
```

| File | Allowed change |
|---|---|
| `ops/account_risk/__init__.py` | New; exports only |
| `ops/account_risk/reference_owner.py` | New; the reducer and its types |
| `tests/ops/test_account_risk_scenarios.py` | New; §7 scenarios, variants and replay checks |
| `REPO_MAP.md` | One row for `ops/account_risk/` in the ops table |

`ops/account_risk/` imports only the standard library: nothing from `ops/c1_rail`, `ops/c1_signal_daemon`, `core` or `lab`. Any wider edit returns as a scope conflict.

## 3. Behavioral contract

1. `AccountRiskConfig.load(mapping)` validates per runbook §6.2 and returns a config with `config_id` = SHA-256 of its canonical JSON. Invalid input raises; it never fills defaults.
2. `initial_state(config, *, dirty_epoch)` starts `HALTED`. An `OperatorStart` event moves it to `RUNNING` only if the epoch is clean and nothing is open or reserved.
3. `step(state, event)` implements §6.3–§6.8 exactly: bar batches in rank order, whole-or-refuse admission with §6.6 reasons in table order, reservations and usage per §6.5, protection per §6.7, latches and the uncertain set per §6.8. Every command output is preceded in the same output tuple by its `JournalRecord`.
4. An invalid or contradictory event never raises out of `step`; it latches per §6.8.
5. `replay(config, events)` folds `step` and returns the full journal; two replays of the same events are equal.

## 4. Acceptance checks — falsifier-first

**Hypothesis:** §6 is sufficient for one deterministic owner to produce every §7 expectation. Reject if any §7 row fails, if any incorrect variant passes, or if satisfying a row needs behavior §6 does not state (return that gap instead of inventing it).

| Row | Required executable evidence | Fails if |
|---|---|---|
| A1 | One test per §7 row (CE-1…RC-5) with the §7 fixture configuration, asserting decisions, refusal reasons, commands with quantities, latches, uncertain set and usage | Any expectation differs |
| A2 | Each row's incorrect variant built as a mutant of the reducer (see below) makes that row fail | A variant survives |
| A3 | Replay: for every row, `replay(events)` equals the step-by-step journal; permuting arrival order inside one bar batch leaves decisions unchanged | Replay or permutation changes a result |
| A4 | Every command output has a preceding `JournalRecord`; a simulated journal failure produces no command and latches `INCIDENT` | A command without a record |
| A5 | Configuration: each unbound field, duplicate rank, non-positive `micro_equiv`, and opposite-side legs on one instrument is rejected; limits come only from the config (a test with a second fixture, cap 6, changes CE-1's outcome to both admitted) | A default or hard-coded limit |
| A6 | No latch is cleared by any later event in the same session, across every row | A latch drops |

**Named mutants** (one at a time): M1 decide in arrival order; M2 clip to remaining capacity; M3 count only confirmed quantity; M4 release a reservation on cancel acknowledgment; M5 size protection to requested quantity; M6 count acknowledged protection as working; M7 accept a terminal that exceeds correlated fills; M8 restore `RUNNING` on reconnect; M9 close an uncorrelated position; M10 skip snapshot `B`; M11 honour a stored `RUNNING` at start; M12 resend a rejected order. Each must turn its §7 row red.

**Revert trigger:** a surviving mutant or a row that passes only through behavior absent from §6.

## 5. Forbidden moves

- Edits outside §2; any import from rail, daemon, `core` or `lab`.
- Binding or proposing any `⟨L-…⟩` value; fixture values stay in tests.
- Reading Pine, runtime ports, `effective_inputs.json` or any private path; NinjaTrader, VM or account work.
- Editing the runbook to make a test pass; merge, force-push or delegated agents.

## 6. Gate and return taxonomy

**RESOLVED:** A1–A6 pass, every mutant fails its row, required suites and gates finish green, and the diff equals the §2 footprint. **FALSIFIED:** a row cannot pass under §6 as written; return the gap with the row. **AMBIGUOUS:** incomplete evidence.

Return `DONE` only for RESOLVED with records; `DONE_WITH_CONCERNS` for a completed patch with named unresolved evidence; `NEEDS_CONTEXT` for missing admission or base; `BLOCKED — scope-problem / capability-problem / plan-itself-wrong` for the named contradiction. After two failed corrections, return for a cleaner prompt on the escalation lane.

## 10. Audit hooks and required evidence

Draft validation:

```powershell
.\fp.ps1 doctor
.\fp.ps1 python scripts/check_brief.py docs/briefs/handoffs/2026-10-18-account-risk-reference-model-card-DRAFT.md --type cc_handoff
.\fp.ps1 python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-18-account-risk-reference-model-card-DRAFT.md
```

After authorized implementation:

```powershell
.\fp.ps1 --workers 2 python -m pytest tests/ops/test_account_risk_scenarios.py
.\fp.ps1 test-ops
.\fp.ps1 check
git diff --check
git diff --name-only
```

Record commands, interpreter, base and returned revision, red, green and mutant outcomes, and each printed `record.json`. Acceptance requires `status: completed`, exit zero, stable source and complete capture. Cite skips and pre-existing failures; the standing CI substitution applies only to a qualification-child timeout.

## 11. Admission record

- **Draft requested:** Joshua, 2026-10-18, in the Claude session: "a bounded Codex implementation proposal".
- **Code admission:** not granted.
- **Freeze:** not granted.
- **Dispatch:** none.
- **Merge:** a later exact-head approval from Joshua after every check finishes green.
