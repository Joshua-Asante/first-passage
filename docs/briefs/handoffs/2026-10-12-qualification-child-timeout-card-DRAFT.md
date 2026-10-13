# Qualification child timeout: an overridable hang bound (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FROZEN 2026-10-12** by the Deployment Coordinator at the commit that adds this line (committed-handoff rule), on Joshua's word, verbatim: "Freeze the timeout card" (G-1 and G-2). §12's upper bound is 14400 s as proposed. **Not dispatched**: G-3 is the coordinator's dispatch record to Codex.

**Base:** `origin/main` `6cf684a`. Every `file:line` is at that commit.

**Parent:** none. This is a test-harness fix. It serves every build that runs the full `fp test-ops` locally.

**Executor (proposed):** Codex local, as single writer of `codex/qualification-child-timeout`. Codex owns CI and infrastructure. Not GLM.

**Coordinator:** the Deployment Coordinator, who freezes, reviews the diff and opens the PR. Joshua decides the merge.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - card_section2_files_only
  - no_ci_workflow_edit
  - no_shard_selection_or_assertion_change
  - no_private_read
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_qualification_isolation.py
  - tests/ops/test_qualification_child_timeout.py
```

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Read `tests/ops/test_qualification_isolation.py` in full. The cap is at `:74` (`child_timeout = 3600`), and `:68-73` explains it: "its timeout is a hang bound, not a performance gate; runner variance alone must not fail this test". Also read `scripts/fp.py` (how `test-ops` launches and which environment it passes on) and `.github/workflows/` (CI's own job timeouts).

Report:
- (a) how the child inherits its environment (`:65-69`);
- (b) CI's job-level timeout for the job that runs this test;
- (c) whether any other test or gate reads `qualification_child_timeout_s`.

**Evidence that motivates this card (local runs, 2026-10-12, all recorded on their worker worktrees):** the `[core]` and `[execution]` children hit 3600 s with no failing test in the P-L1, P-L3, G4-a and G0-a builds. G0-a's record shows `[core]` at 60% and `[execution]` at 88% at cutoff. CI runs the same shards inside the cap.

## 0.5. Routing and clarifying questions

Codex local; offline; low behavioural risk (`max_risk: medium` only because branch push is a medium capability). CI must keep its current behaviour exactly. Only a local override changes.

## 1. Goal

Let a slow local host finish the clean-process qualification children, while CI keeps its 3600 s hang bound.

## 2. Scope

Files:
- `tests/ops/test_qualification_isolation.py`: the timeout source only.
- `tests/ops/test_qualification_child_timeout.py`: new.
- `scripts/README.md`: one line documenting the variable.

**Forbidden:** CI workflows, shard selections, the signed/provenance assertions, `scripts/fp.py`, and every other file.

## 3. Method

1. Replace the literal with a helper:
   - It reads `FP_QUALIFICATION_CHILD_TIMEOUT_S`.
   - Unset: 3600, the unchanged default.
   - Set: the value must be an integer between 3600 and 14400 inclusive. Anything else (lower, higher, non-integer, empty) fails the test with a named error. It never falls back silently.
2. Record the value actually used. `record_property("qualification_child_timeout_s", …)` already exists. Also record whether the value came from the override.
3. Document the variable in `scripts/README.md` next to the launcher's local-run notes: set it for slow local hosts; CI leaves it unset.

## 4. Acceptance checks (falsifier-first)

**H:** if the helper follows §3, then unset gives 3600, valid values pass through, and invalid values refuse. **Falsifier:** any default other than 3600, or any accepted value outside [3600, 14400], rejects the build.

| Row | Check |
|---|---|
| T1 | Unset gives 3600 |
| T2 | 3600 and 14400 are accepted (boundaries) |
| T3 | 3599, 14401, `abc`, `""` and `1e4` refuse with the named error |
| T4 | The recorded property shows both the value and that it came from the override |
| T5 | The existing isolation test still passes unchanged in substance, run once with the variable unset |

**Named mutants:**
- default changed to anything other than 3600;
- lower bound removed;
- upper bound removed;
- a silent fallback to 3600 on bad input.

Each row is red before the change and green after. Record every run through the launcher.

## 5. Forbidden

Everything in the authority block. In particular:
- changing a CI workflow;
- changing shard composition or the evidence assertions;
- weakening the signed/provenance checks;
- a silent fallback on a bad override value.

## 6. Return (status taxonomy)

`DONE`, `DONE_WITH_CONCERNS`, `BLOCKED` or `NEEDS_CONTEXT`. Map to the verdict: all §4 rows passing is RESOLVED; a falsifier hit is FALSIFIED; anything else is AMBIGUOUS.

Return:
- the Phase 0 findings;
- `git diff --stat`;
- the head SHA;
- each command, with counts and `record.json` path, status and exit code.

## 7. Stop conditions and parent review

Stop if any of these holds:
- Phase 0 shows CI already sets an environment variable that this change would pick up;
- another test reads the timeout property in a way that would break;
- the change needs a file outside §2.

## 8. Out of scope and decision unlocked

**Out of scope:** making the suite itself faster; the Azure runner (#746).

**Unlocks:** a completed local `fp test-ops` on this laptop, with the variable set, for future builds. This removes the recurring CI-substitution deviation.

## 9. Sequencing and file collisions

No in-flight card edits these files. This card does not run the full `fp test-ops`; its own acceptance is the focused files above.

## 10. Audit hooks (runnable)

```bash
python -I scripts/fp.py python -m pytest tests/ops/test_qualification_child_timeout.py -q   # expect all passed
git diff --stat origin/main...HEAD   # expect only §2 files
```

## 11. Gates

- **G-1:** Joshua reviews this draft.
- **G-2:** the coordinator freezes it.
- **G-3:** the coordinator dispatches it.

## 12. Open decisions (coordinator at freeze)

**Settled at freeze:** 14400 s (4 h), as proposed, covering the observed 60% at 3600 s on `[core]` with margin.

## Pre-mortem

- **A large override could hide a real hang locally for up to 4 hours.** The cap is bounded, and CI is unaffected.
- **CI might export the variable some other way.** Phase 0 (b) and the §7 stop guard against this.

## Amendment 2026-10-13 — T5 evidence route (coordinator; worker hook block)

**Trigger:** the Codex Phase 0 return (2026-10-13, BLOCKED/AMBIGUOUS, no code changed, head `13e5d2e`, launcher record status `failed`, exit 5). `tests/ops/conftest.py` `pytest_collection_modifyitems` removes `test_qualification_isolation.py`'s items from every focused or filtered selection (`_isolate_qualification` is true only for an unfiltered ancestor-directory run), so T5 as written cannot run. Not bypassed. Phase 0's other findings stand: the child uses `sys.executable` and strips `PYTEST_ADDOPTS` and three xdist variables; CI's `tests.yml` `pytest` job runs `pytest tests/` with no job timeout; no CI configuration sets the variable; nothing else reads `qualification_child_timeout_s`.

**T5 is replaced by T5a and T5b.** All other rows, mutants, scope and forbidden lists are unchanged; `tests/ops/conftest.py` stays forbidden.

| Row | Check |
|---|---|
| T5a (local, recorded) | With the variable unset, `.p.ps1 python -m pytest tests/ops --collect-only -q` collects the bridge's shard items and none under `tests/ops/qualification` or the provenance file. Collection only; no qualification child runs locally. |
| T5b (CI, at the build head) | The `pytest (3.11)` job passes on the build PR's exact head. It runs `pytest tests/` unfiltered with the variable unset, so the bridge runs the shards at the 3600 s default and records `qualification_child_timeout_s` = 3600 and the not-overridden flag. The return cites the job and the property from the retained `pytest-evidence` artifact. |

**T1–T4 helper tests:** the new `test_qualification_child_timeout.py` imports only the helper (a non-`test_` name) from the isolation module, so no bridge test function is re-collected under the new module. It runs focused as normal.

**Return:** T5a's launcher record locally; T5b is evidence only once CI is green at the exact head. A local full `fp test-ops` is not required (§9).
