# P-L1: per-leg size in the live sizing context (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FROZEN 2026-10-11** by the live-wiring lane owner (single writer, delegated by the Deployment Coordinator on 2026-10-11), at the commit that adds this line. The freeze base is `origin/main` `7db42f1`. **Not dispatched:** the J-4 build gate (§11 G-3) is not open. *As drafted:* DRAFT, 2026-10-11. Drafted at Joshua's request ("draft the P-L1 and P-L2 build cards") for the Deployment Coordinator ("Portfolio deployment coordination") to freeze. Not frozen, not dispatched. **Not dispatchable until the §11 gates hold.**

**Base:** drafted at `origin/main` `b5571a9`; re-anchored at the freeze base `7db42f1`, where `book_sizing_context.py` is unchanged and only `book_account_owner.py` moved (#780). Every `file:line` is at `b5571a9` unless marked otherwise. `ops/c1_rail/book_sizing_context.py` last changed `4eec7e73` (2026-09-15).

**Parent scope:** [live size-vector wiring scope](../../notes/2026-10-11-live-size-vector-wiring-scope.md) (PR #773) §5 row P-L1. The successor [build card](2026-10-10-t00-successor-screen-build-card-DRAFT.md) §3.1 owns the interfaces this card consumes: `LegSize`, `SizeVector`, and `entry_quantities`/`add_quantity(..., size=None)`, where `None` is today's behaviour. **Sibling:** [P-L2](2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md) is the only caller that will pass a size.

**Authority:** G-1 and G-2 are recorded; G-3 waits on the J-4 build gate (§11). Each item is a separate act:
- G-1 is Joshua's admission of the bounded edit to bound code.
- G-2 is the coordinator's freeze.
- G-3 is the dispatch, which depends on the screen.

**Executor:** a Claude worker, single writer of `claude/live-size-p-l1` (proposed). **Not GLM.** The change is to order sizing (build card §5; AGENTS.md "Protection").

**Coordinator:** the Deployment Coordinator. It owns the freeze, diff review, integration, the PR and the ledger.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - offline_synthetic_only
  - card_section2_files_only
  - no_book_policy_edit
  - no_book_account_owner_edit
  - no_existing_test_or_fixture_edit
  - no_module_global_added_to_bound_modules_beyond_one_import_name
  - no_measured_closure_or_p7_closure_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_private_vector_value_read_or_committed
  - no_rail_arm
  - no_rail_deploy
  - no_account_traffic
  - no_host_or_fly_command
  - no_pine_or_port_access
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_live_size_vector_sizing_context.py
  - tests/ops/test_tradeify_sizing_integration.py
  - tests/ops/test_book_quantity_laws.py
  - tests/ops/test_book_policy.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_policy_fingerprint.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_seal.py
  - tests/ops/qualification/test_composition_fixture.py
  - tests/ops/qualification/test_composition_route.py
  - tests/ops/qualification/test_runtime_inventory.py
```

`test_live_size_vector_sizing_context.py` is new. The other fourteen exist and must stay green with no edit. The last five are listed because `book_sizing_context.py` is a trust-domain runtime dependency (`trust_domain.py:163`). It is also a TB-I1 policy-fingerprint component (`policy_fingerprint.py:29-32`), which is why `test_policy_fingerprint.py` is listed. Those suites hash bytes at runtime, and no tracked file pins the current SHA-256 (`884d31f6…`; checked at drafting, §0(c)).

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Read the files below and report the findings before writing any test. A contradiction with this card is a **stop** (§7).

- **(a) Base and bytes.** HEAD descends from `b5571a9`. `book_sizing_context.py` is byte-identical to `b5571a9` unless P-L1's own commits changed it. Report `git log -1 --format='%h %cs' -- ops/c1_rail/book_sizing_context.py`.
- **(b) Closure membership.** Run the measured-closure script at HEAD (§10). At drafting it gave **68 measured / 63 staging, membership unchanged**, and `book_sizing_context.py` was in neither set. Check the public P7 D8 list ([C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md) `:260-265`, 40 paths): at drafting it did not name `book_sizing_context.py`. A different answer is a **stop**, because then the edit would move H′ (build card §4).
- **(c) Pins.** `git grep` finds no tracked file holding `sha256(book_sizing_context.py)` or its first 16 hex characters.
- **(d) Callers.** Today's callers of `BookSizingBinding(` are `book_account_owner.py:1575` (positional) and `tests/ops/test_tradeify_sizing_integration.py:27` (positional). Today's callers of `size_book_request` are `book_account_owner.py:1819` (at `7db42f1`; `:1813` at `b5571a9`), `c1_sizing_host_reference.py:293` and the tests listed by `grep -rn size_book_request tests`. Report any other caller.
- **(e) The law the replay uses.** Read `qualification/replay.py:605-620` and confirm that `size=self.size_vector.leg(k)` is passed to both `entry_quantities` and `add_quantity`. Read `book_policy.py:434-438` (`_leg_size`) and `:484-560`. P-L1 must reproduce exactly that call shape.
- **(f) Image closure.** `deploy/c1_rail/Dockerfile:39` and `deploy/c1_signal_daemon/Dockerfile:37` already copy `book_sizing_context.py` and `book_policy.py`. No new file enters either image.

## 0.5. Routing and clarifying questions

Routing: Claude worker, local or cloud. The card touches no vendor data, secret, Pine, port or private value, so a cloud checkout is sufficient (§0.75 of the handoff template: `N/A`, nothing gitignored is read). Every test uses synthetic `LegSize` values. **Never use the FLOOR-HALF vector's values.** They are private, and this card does not need them.

Apply each recommended default unless a Phase-0 read contradicts it. On a contradiction, return `NEEDS_CONTEXT` and quote the conflict.

- **(A) Field shape.** **Recommended default:** append `size: LegSize | None = None` as the **last** field of `BookSizingBinding` (`book_sizing_context.py:48-62`, class at `:49`). Positional callers then stay valid. `None` means today's quantities, which is book_policy's own convention (`entry_quantities` docstring, `book_policy.py:518-525`). Requiring an explicit vector is P-L2's job, at the configuration boundary (the owner binding), not this pure function's.
- **(B) Where the size is checked.** **Recommended default:** in `_identities` (`:155-169`), add `_require(binding.size is None or (isinstance(binding.size, LegSize) and binding.size.leg_id == request.leg_id), "size_binding_mismatch")`. The halt reason is then a named reason rather than book_policy's `ValueError` text.
- **(C) Import.** **Recommended default:** add `LegSize` to the existing `from .book_policy import (...)` at `:20-23`. It is the only new module-level name. Add no constant, instance or helper at module level.
- **(D) Docstring.** **Recommended default:** add one sentence to `size_book_request`'s docstring: the binding's `size` reaches both laws, and `None` is today's quantities. Change no other prose.

## 1. Goal

The live sizing function, `size_book_request` (`book_sizing_context.py:242-289`), passes a per-leg `LegSize` to `entry_quantities` and `add_quantity`, exactly as `replay.py:612-616` does. The size comes from the binding, so that P-L2 can bind the frozen vector there. With `size=None`, every quantity, halt reason and capacity decision is unchanged.

**Not asked:**
- binding the vector in the owner (P-L2);
- configuration, loader, GO or activation (P-L4);
- the emulator (`book_bundle_execution.py`, P-L3);
- the legacy single-leg path (`c1_sizing_host_reference.process_signal`).

## 2. Scope

### 2.1 The change

- `BookSizingBinding` gains `size: LegSize | None = None` (D-A).
- `_identities` refuses a size that is not this leg's `LegSize`, with reason `size_binding_mismatch` (D-B).
- `size_book_request` passes `size=binding.size` to `entry_quantities` (`:256-259`) and to `add_quantity` (`:261-262`).
- The leg-allocation and account-capacity checks (`:264-271`) then run on the sized `qty`, unchanged.

### 2.2 What does not change

- `book_policy.py`, including `CANDIDATE_SCALE`, `require_policy` and the quantity laws. P-S1 already supplies `size=`.
- `BookSizingDecision` fields, `_session_mode`, `_exposure` and every existing halt reason.
- The account owner. Its `_context` keeps constructing the binding positionally without a size, so live behaviour is exactly today's until P-L2.

### 2.3 Files

| File | Edit |
|---|---|
| `ops/c1_rail/book_sizing_context.py` | §2.1 only |
| `tests/ops/test_live_size_vector_sizing_context.py` | new |

## 3. Method

1. Phase 0 (§0). Post the findings.
2. Write the §4 rows in the new test file. Run them on the base and record the **red** run. Every row must fail on the base: the new keyword does not exist there.
3. Make the §2.1 change. Record the **green** run of the new file, then the full acceptance list (§10).
4. Run `python -I scripts/fp.py test-ops` once, and `python -I scripts/fp.py check`. Cite each `record.json`.
5. Stage only the §2.3 files. Check every claim in the commit message against `git diff --cached`. Push the branch and return (§6).

No PR touching this file triggers the Qualification S2 supervision workflow: its path filters (`qualification-s2-supervision.yml:33-55`) name `book_policy.py`, `book_schedule.py` and `policy_fingerprint.py`, not `book_sizing_context.py`. CI is the ordinary suite.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes the scope note's P-L1 row; there is no hypothesis under test.

| Row | Test in `test_live_size_vector_sizing_context.py` | Fails if |
|---|---|---|
| LS1 | For each leg × mode × tier on the replay's ladder inputs, `size=None` gives `qty_out`, `prospective_add` and halt state equal to `entry_quantities`/`add_quantity` called with no size | The default changes any quantity |
| LS2 | For a synthetic non-identity `LegSize` on each leg (for example Aegis `base=4`; Striker risk `1/2`, cap at the canonical smallest; Vanguard ports `(1,0),(2,1)`), entry `qty_out` and `prospective_add` equal `entry_quantities(..., size=that)` for the same inputs, and differ from LS1 on at least one input per leg | The size does not reach the entry law |
| LS3 | An add request with Striker `adds=OFF` and a confirmed base above 0 gives `qty_out == 0` with no halt; with `UNCHANGED`, it equals `add_quantity(..., size=that)` | The size does not reach the add law |
| LS4 | Aegis `base=0`: entry gives `qty_out == 0`, no halt (the owner turns this into `zero_size`, as replay row Z7 does) | A leg at 0 halts or sizes above 0 |
| LS5 | A `LegSize` for another leg: halt with reason `size_binding_mismatch`, `qty_out` 0 | A mismatched size is accepted or sized |
| LS6 | A non-`LegSize` (a dict mapping): halt `size_binding_mismatch` | An untyped size is accepted |
| LS7 | An entry whose identity quantity would refuse `leg_allocation_refusal` fits under a smaller synthetic size, so the capacity check uses the sized quantity | Capacity is checked on the unsized quantity |

**Revert trigger:** any listed existing suite changes outcome, or any existing halt reason or quantity changes for `size=None`.

## 5. Forbidden

- Any edit to `book_policy.py`, `book_account_owner.py`, `c1_sizing_host_reference.py`, `book_bundle_execution.py`, `replay.py` or any `qualification/` file.
- Any edit to an existing test or fixture.
- Adding a module-level name to `book_sizing_context.py` beyond the one import (D-C).
- Making `size` required in this card. That changes the owner's call (`book_account_owner.py:1575`), which is P-L2's file and is held by the protection-health worker.
- Reading, choosing or quoting any real vector value; reading any private artifact, Pine, port or `effective_inputs.json`.
- `dd_protection`, `DD_TRIGGER`/`DD_SCALE`, `CANDIDATE_SCALE`, `BASE_RISK` or the lifecycle multipliers.
- The "while I was in there" refactor of neighbouring sizing code. Report it as a concern instead.
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

Return exactly one status to the coordinator:

| Status | When |
|---|---|
| `DONE` | §4 rows red on the base and green on the build; every acceptance suite green; `fp test-ops` and `fp check` records completed with exit 0; footprint equals §2.3 |
| `DONE_WITH_CONCERNS` | As DONE, but something off-pattern was noticed (for example, a caller not listed in §0(d)) |
| `NEEDS_CONTEXT` | A §0.5 default is contradicted by a Phase-0 read |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` covers a §0(b) closure hit |

**Gate verdict (coordinator, at review):**
- **RESOLVED** when the return is `DONE` and both §7 passes reproduce it.
- **FALSIFIED** when a §4 row cannot be made red on the base, or a revert trigger fires.
- **AMBIGUOUS** (held for the coordinator) on `DONE_WITH_CONCERNS`.

**Report:** the status; red and green record paths per row; the acceptance-suite records; `git diff --name-only b5571a9..HEAD`; concerns; the next action recommended.

## 7. Stop conditions and parent review

**Stop and return; do not work around:**
- §0(b) finds the file in a closure.
- A listed suite fails at the base.
- Any row cannot be made red on the base.
- A green run needs an edit outside §2.3.

**Parent review (coordinator):**
- **Pass 1, spec compliance:**
  - the diff names exactly the two §2.3 files;
  - the only new module-level name is `LegSize`;
  - `size=` reaches both calls;
  - no existing test changed.
- **Pass 2, quality:**
  - re-run LS1–LS7 and the acceptance list from a clean worktree at the returned head;
  - confirm the call shape matches `replay.py:612-616`;
  - confirm no halt reason other than `size_binding_mismatch` was added.

## 8. Out of scope and decision unlocked

**Out of scope:** P-L2 to P-L5 ([scope note](../../notes/2026-10-11-live-size-vector-wiring-scope.md) §5).

**Unlocks:** P-L2 can bind the frozen vector in the owner and pass `size=vector.leg(leg_id)` through this field.

## 9. Sequencing and file collisions

- **No in-flight card names `book_sizing_context.py`:** protection-health, GC-5-DISPLACED, TB-I3 and TB-I3-HOST were checked at drafting. Their footprints are in scope note §4. So P-L1 can run alongside protection-health.
- **P-L1 must merge before P-L2 is cut.**
- **Roadmap:** P-L1 is behaviour-changing frozen work for the deployment checklist. It lands before CP-6 (the F1 freeze; checklist T15 "complete all behavior-changing frozen work first").

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; 0 violations.
python scripts/check_brief.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md --type cc_handoff
python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md

# Closure membership (§0(b)). Expected: 68 measured / 63 staging; no book_sizing_context.py.
cp docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt "$TMP/closure.py"
python -I "$TMP/closure.py" . b5571a9 HEAD | grep -c book_sizing_context   # expect 0

# Pins (§0(c)). Expected: no output.
git grep -l "$(sha256sum ops/c1_rail/book_sizing_context.py | cut -c1-16)"

# Scope at return. Expected: exactly the two §2.3 files.
git diff --name-only b5571a9..HEAD

# The call shape matches the replay. Expected: size= on both calls in each file.
grep -n "size=" ops/c1_rail/book_sizing_context.py ops/c1_rail/qualification/replay.py

# Targeted run, then the suites. Each prints a record.json; cite it.
python -I scripts/fp.py python -m pytest tests/ops/test_live_size_vector_sizing_context.py <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1. Joshua's code admission.** Joshua names the §2.1 edit to `book_sizing_context.py` as bound code (`trust_domain.py:163`), knowing it moves the TB-I1 policy fingerprint (`policy_fingerprint.py:29-32`). One admission may cover P-L1 and P-L2 together (scope note Q5). The coordinator records his words and the time in the ledger. **RECORDED:** Joshua, 2026-10-11 (about 17:15Z), in the live-wiring lane session: "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended", on the [decision packet](../../notes/2026-10-11-live-wiring-decision-packet.md) (#788). One admission covers P-L1 and P-L2 (packet §2).
- **G-2. Coordinator freeze.** The coordinator answers §12, commits the frozen revision under the committed-handoff rule, and records its SHA. **DONE:** frozen 2026-10-11 by the lane owner at the commit that adds the Status line; the SHA is reported to the coordinator.
- **G-3. Dispatch.** **RULED (J-4):** the build may be dispatched when **either** the Tradeify successor screen returns GO **or** Q-SFCLEAR-1 resolves. Neither has happened at freeze. Building binds no vector; each lane activates only under its own gates (packet §4). A Tradeify NO-GO does not withdraw the card.

## 12. Open decisions (coordinator at freeze)

- **D-1. Dispatch timing.** **RULED:** J-4 (G-3).
- **D-2.** Confirm or replace the §0.5 defaults (A)–(D). **RULED:** confirmed (rest as recommended).

## Pre-mortem

- **Loop cost.** One targeted run plus one `fp test-ops` and one `fp check`. Budget: two full suite runs. A third run is a checkpoint, not another attempt. No S2 workflow run is triggered (§3).
- **Decisions the executor will hit:** none beyond (A)–(D), which are ruled in advance.
- **What would make this moot:** the screen returning NO-GO (withdraw), or Joshua choosing to bind the vector elsewhere than the owner (re-scope P-L1 and P-L2 together).
- **Evidence binding:** acceptance evidence is the targeted, `fp test-ops` and `fp check` records at the returned head only. A push after the green records voids them.
- **Measure:** wall time, runs and rounds are filled in at return.
