# P-L3: per-leg size in the offline bundle emulator, with three-way parity (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **FREEZE REVISION 2026-10-12, effective on the coordinator's countersignature.** The live-wiring lane writer (single writer for this lane, by the Deployment Coordinator's 2026-10-11 directive) prepared this revision at the commit that adds this line. The review fixes on #788 are folded in. The freeze base is `origin/main` `7db42f1`. The directive exists in chat only, and the committed-handoff rule (surface-allocation ADR, "Committed-handoff rule") does not count a chat-only direction. So the freeze takes effect only when the coordinator commits the delegation or countersigns this revision's SHA (the decision packet §6). Until then the card is a candidate freeze, not a frozen card. **Not dispatched:** the J-4 build gate (§11 G-2) is not open. *As drafted:* DRAFT, 2026-10-11. Drafted at Joshua's request ("draft the P-L3 emulator parity card") for the Deployment Coordinator ("Portfolio deployment coordination") to freeze. Not frozen, not dispatched. **Not dispatchable until the §11 gates hold.**

**Base:** `origin/main` `b5571a9`. Every `file:line` below is at that commit. `ops/` is unchanged through `ba000b2`. `ops/c1_signal_daemon/book_bundle_execution.py` and `book_bundle_intake.py` last changed `3cf42e43` (2026-09-16).

**Parent scope:** [live size-vector wiring scope](../../notes/2026-10-11-live-size-vector-wiring-scope.md) (PR #773) §1 row L4 and §5 row P-L3. The successor [build card](2026-10-10-t00-successor-screen-build-card-DRAFT.md) §3.1 owns the vector interfaces. **Prerequisite:** [P-L1](2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md) merged, because LE2's three-way parity calls `size_book_request` with a size. **Siblings:** [P-L2](2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md); [P-L4](../../notes/2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md).

**Authority:** G-1 is recorded; G-2 waits on P-L1 and the J-4 build gate (§11). **No code admission is needed:** this file is not bound code (§0(b)).

**Executor:** a Claude worker (D-2, ruled), single writer of `claude/live-size-p-l3` (proposed). **Not GLM:** the change is to order sizing.

**Coordinator:** the Deployment Coordinator.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - cut_after_p_l1_merged
  - offline_synthetic_only
  - card_section2_files_only
  - no_book_bundle_intake_edit
  - no_book_policy_edit
  - no_book_sizing_context_edit
  - no_existing_test_or_fixture_edit
  - no_private_vector_value_read_or_committed
  - no_pine_or_port_access
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_live_size_vector_emulator.py
  - tests/ops/test_book_bundle_execution.py
  - tests/ops/test_book_bundle_intake.py
  - tests/ops/test_book_bundle_reduction_feedback.py
  - tests/ops/test_book_runtime_close_feedback.py
  - tests/ops/test_book_adapters_parity.py
  - tests/ops/test_book_policy.py
  - tests/ops/test_live_size_vector_sizing_context.py
```

- `test_live_size_vector_emulator.py` is new.
- `test_live_size_vector_sizing_context.py` is P-L1's and must stay green.
- The others exist and stay green with no edit.
- `test_book_adapters_parity.py` skips without the private ports (its own `:45`, `:66`). A skip there is not evidence; §3 says where it counts.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Report each finding before any test. A contradiction is a **stop** (§7).

- **(a) Base.** HEAD contains P-L1's merge: `BookSizingBinding` ends in `size: LegSize | None = None`, and `size_book_request` passes it to both laws. Report `git log -1 --format='%h %cs'` for `book_bundle_execution.py`.
- **(b) Not bound.** At drafting, `book_bundle_execution.py`:
  - is absent from `trust_domain.py` `_PRODUCTION_CODE`;
  - is absent from `policy_fingerprint.py` `REQUIRED_COMPONENTS`;
  - is absent from `composition_fixture.py`;
  - is absent from both Dockerfiles;
  - is absent from the measured closure (68/63) and from the public P7 D8 list.
  - No tracked file pins its SHA-256.

  Re-run the §10 hooks. Any hit is a **stop**: the file would then need a G-1-style admission this card does not carry.
- **(c) Call sites.** `BundleExecution.admit` (`:142-183`) calls `entry_quantities` (`:159-164`) and `add_quantity` (`:168-169`) with no `size=`. `SizingInputs` is the frozen dataclass at `:19-26`. `__init__` validates the inputs at `:116-123`. Report any other sizing call in the file.
- **(d) Consumers.**
  - `book_bundle_intake.py:263` builds `SizingInputs(leg_id=leg_id, **sizing)` from an admitted manifest. That manifest's `sizing` key set is **closed**: `{"mode", "lifecycle_tier", "cap_alloc", "risk_dollars", "pointvalue"}` (`:111-112`).
  - Tests construct `SizingInputs` positionally (`test_book_runtime_close_feedback.py:52`) and by keyword.
  - The route-native edition cards (`2026-09-26-orb-striker-edition-production.md:90`, `2026-09-26-vanguard-fixed-stop-edition-production.md:62`) cite `admit` as the place where sizing happens once. They read it; they do not edit it.

  Report any other constructor.
- **(e) The reference law.** `qualification/replay.py:612-616` and P-L1's `size_book_request` pass `size=` to both laws. P-L3 reproduces that call shape.

## 0.5. Routing and clarifying questions

Routing: a Claude worker (D-2), local or cloud. No vendor data, secret, Pine, port body or private value is read (template §0.75: `N/A`). `test_book_adapters_parity.py` needs the private ports for a non-skip run. Only the coordinator's review run in the operator's checkout counts for that file (§3, §7). Tests use synthetic `LegSize` values only.

Apply each recommended default unless Phase 0 contradicts it. On a contradiction, return `NEEDS_CONTEXT` and quote the conflict.

- **(A) Field.** **Recommended default:** append `size: LegSize | None = None` as the **last** `SizingInputs` field. Positional callers stay valid, and `None` means today's quantities, which is book_policy's convention.
- **(B) Validation.** **Recommended default:** in `__init__`, add `require(inputs.size is None or (isinstance(inputs.size, LegSize) and inputs.size.leg_id == inputs.leg_id), "size_identity_mismatch")`, beside the existing identity checks.
- **(C) The call.** **Recommended default:** pass `size=cfg.size` to both `entry_quantities` and `add_quantity` in `admit`. Change nothing else in `admit`: the zero-quantity reject (`shared_sizing_zero`), pending bookkeeping and the allocation check all run on the sized quantity.
- **(D) Bundle admission stays identity-only.** **Recommended default:** do not touch `book_bundle_intake.py`. Its closed `sizing` set refuses any `size` key, so admitted bundles keep sizing at the declared book's quantities. That is correct: their parity reference is a TradingView export run at those quantities. LE7 pins this behaviour.
- **(E) Import.** **Recommended default:** add `LegSize` to the existing `from c1_rail.book_policy import (...)` at `:13-15`.

## 1. Goal

The offline bundle emulator sizes with the same per-leg `LegSize` as the live sizing context (P-L1) and the qualification replay. For identical inputs, all three produce identical quantities. With `size=None`, the emulator and bundle admission behave exactly as today.

**Why build it.** Without P-L3, the emulator is the one sizing call site that cannot take the vector. A later synthetic rehearsal on the successor (checklist T17, "rehearse the entire timed procedure on the final candidate with synthetic inputs") could then silently size at declared-book quantities. LE2's three-way parity becomes T16 evidence that the shared sizing law is the same in all three places. D-1 asks whether this is worth building.

**Not asked:** bundle admission or its manifest schema; the owner binding (P-L2); configuration or activation (P-L4, R-SV); any port, Pine or real vector value.

## 2. Scope

### 2.1 The change (`book_bundle_execution.py`)

- `SizingInputs` gains `size` (A).
- `BundleExecution.__init__` refuses a mismatched or untyped size (B).
- `admit` passes `size=` to both laws (C).
- One import (E).

### 2.2 What does not change

- `book_bundle_intake.py`, including its closed `sizing` set (D).
- `run_sized_adapter`, `check_margin_phase`, the reduction and feedback paths, and every existing refusal reason.
- `book_policy.py` and `book_sizing_context.py`.

### 2.3 Files

| File | Edit |
|---|---|
| `ops/c1_signal_daemon/book_bundle_execution.py` | §2.1 only |
| `tests/ops/test_live_size_vector_emulator.py` | new |

## 3. Method

1. Phase 0 (§0). Post the findings.
2. Write the §4 rows. Run them at the cut base and record the **red** run. LE1–LE6 must be red there, because the field does not exist. LE7 is a pin that is green at the base.
3. Make the §2.1 change. Record the **green** run of the new file, then the acceptance list.
4. Run `python -I scripts/fp.py test-ops` once and `python -I scripts/fp.py check`. Cite each `record.json`.
5. Stage only the §2.3 files, check the commit message against `git diff --cached`, push and return.

`test_book_adapters_parity.py` skips without private ports. The coordinator's §7 review runs it unskipped in the operator's checkout, with the ports read in place (AGENTS.md private read surface). No PR touching this file triggers the S2 workflow (path filters, `qualification-s2-supervision.yml:33-55`).

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes the scope note's P-L3 row; there is no hypothesis under test.

| Row | Test in `test_live_size_vector_emulator.py` | Fails if |
|---|---|---|
| LE1 | `size=None`: for each leg's ladder inputs, the admitted quantity equals `entry_quantities`/`add_quantity` called with no size | The default changes any quantity |
| LE2 | **Three-way parity.** For a synthetic non-identity `LegSize` per leg, and the same mode, tier, allocation, risk dollars and stop distance, three values are equal: the emulator's admitted entry quantity; P-L1's `size_book_request(...).qty_out` with `binding.size` set; and `entry_quantities(..., size=that)`, the call `replay.py:612-616` makes. The value also differs from LE1 on at least one input per leg | Any of the three diverges, or the size has no effect |
| LE3 | Striker `adds=OFF`, with a confirmed base above 0: the add yields the `shared_sizing_zero` reject to the adapter and no action. With `UNCHANGED`, the add equals `add_quantity(..., size=that)` | The add law ignores the size |
| LE4 | Aegis `base=0`: entry yields `shared_sizing_zero`, no action and nothing pending | A zero leg emits an order |
| LE5 | A `LegSize` for another leg, or a dict: `BundleExecution(...)` raises `size_identity_mismatch` | A mismatched or untyped size is accepted |
| LE6 | An entry whose identity quantity would hit `allocation_refusal` fits under a smaller synthetic size | The allocation check uses the unsized quantity |
| LE7 | *(Pin, green at base.)* An admitted-bundle manifest whose `sizing` carries a `size` key is refused `incomplete_sizing_inputs` | Bundle admission can be steered off identity |

**Revert trigger:** any listed suite changes outcome, or any quantity or refusal changes for `size=None`.

## 5. Forbidden

- Any edit outside §2.3. In particular: `book_bundle_intake.py` and its manifest schema; `book_policy.py`; `book_sizing_context.py`; `replay.py`; `tv_broker_emulator.py`; `book_parity.py`.
- Editing an existing test or fixture.
- Running bundle admission or parity over real exports with a non-identity size. Declared-book exports cannot reference a successor size.
- Any real vector value, private artifact, Pine or port body. In the coordinator's unskipped run, the ports are read in place and never copied, quoted or committed.
- `dd_protection`, `DD_TRIGGER`/`DD_SCALE`, `CANDIDATE_SCALE`, `BASE_RISK` or the lifecycle multipliers.
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | LE1–LE6 red at the cut base and green on the build; LE7 green at both; every acceptance suite green; `fp test-ops` and `fp check` records completed with exit 0; footprint equals §2.3 |
| `DONE_WITH_CONCERNS` | As DONE, with an off-pattern observation (for example, a §0(d) constructor not listed) |
| `NEEDS_CONTEXT` | A §0.5 default is contradicted |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` covers a §0(b) bound-code hit |

**Gate verdict (coordinator, at review):**
- **RESOLVED** when the return is `DONE` and both §7 passes reproduce it, including the unskipped parity run.
- **FALSIFIED** when a row cannot be made red on the base, or a revert trigger fires.
- **AMBIGUOUS** (held for the coordinator) on `DONE_WITH_CONCERNS`.

**Report:** the status; red and green record paths per row; the acceptance records; `git diff --name-only <cut base>..HEAD`; concerns; the next action recommended.

## 7. Stop conditions and parent review

**Stop and return; do not work around:**
- any §0 finding that contradicts this card;
- a listed suite red at the cut base;
- a row that cannot be made red;
- an edit needed outside §2.3.

**Parent review (coordinator):**
- **Pass 1, spec compliance:**
  - the diff is exactly §2.3;
  - the only new module-level name is `LegSize`;
  - `size=` reaches both calls;
  - intake is untouched.
- **Pass 2, quality:**
  - re-run LE1–LE7 and the acceptance list at the returned head;
  - run `test_book_adapters_parity.py` **unskipped** in the operator's checkout (ports in place);
  - confirm the call shape matches `replay.py:612-616` and P-L1.
- **Pass 3, consolidated read:** read P-L1, P-L2 and P-L3 together, and confirm one size argument travels identically through the replay, the live owner and the emulator.

## 8. Out of scope and decision unlocked

**Out of scope:** bundle admission with a successor size, which needs a sized reference that no TradingView export supplies; P-L4; R-SV; P-L5.

**Unlocks:** T16's "prove equality to qualified shared components" can cite LE2 for the sizing law in all three places.

## 9. Sequencing and file collisions

- **No in-flight card edits `book_bundle_execution.py`.** Protection-health, GC-5, TB-I3 and TB-I3-HOST were checked. The 2026-09-26 edition cards only cite `admit`.
- **Cut after P-L1 merges** (LE2). P-L3 is independent of P-L2 and may run alongside it.
- **Roadmap:** before CP-6 with P-L1/P-L2 (its quantities are behaviour on a sizing call site), and cited at T16.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; 0 violations.
python scripts/check_brief.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l3-emulator-parity-card-DRAFT.md --type cc_handoff
python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l3-emulator-parity-card-DRAFT.md

# Not bound (§0(b)). Expected: no output from any line.
grep -n "book_bundle" deploy/*/Dockerfile ops/c1_rail/qualification/trust_domain.py ops/c1_rail/policy_fingerprint.py tests/ops/qualification/composition_fixture.py
git grep -l "$(sha256sum ops/c1_signal_daemon/book_bundle_execution.py | cut -c1-16)"
cp docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt "$TMP/closure.py"
python -I "$TMP/closure.py" . b5571a9 HEAD | grep -c book_bundle        # expect 0

# Intake's sizing set is still closed (D). Expected: the five-key set at :111-112.
grep -n "incomplete_sizing_inputs" -B1 ops/c1_signal_daemon/book_bundle_intake.py

# Scope at return. Expected: exactly the two §2.3 files.
git diff --name-only <cut-base>..HEAD

# Call shape. Expected: size= on both calls in each of the three files.
grep -n "size=" ops/c1_signal_daemon/book_bundle_execution.py ops/c1_rail/book_sizing_context.py ops/c1_rail/qualification/replay.py

# Suites. Each prints a record.json; cite it.
python -I scripts/fp.py python -m pytest tests/ops/test_live_size_vector_emulator.py <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until both hold)

- **G-1. Coordinator freeze.** The coordinator answers §12, confirms §0(b) (no code admission needed), commits the frozen revision and records its SHA. **DONE:** frozen 2026-10-11 by the lane owner; §0(b) re-confirmed at `7db42f1` (68/63, no hit); the SHA is reported to the coordinator.
- **G-2. Dispatch.** **RULED (J-4):** dispatched after P-L1 merges, once the build gate is open (the Tradeify successor screen GO **or** the personal clearance study (Q-SFCLEAR-1: #752 or its re-scoped ID) returns **RESOLVED**). It may run in parallel with P-L2.

## 12. Open decisions (coordinator at freeze)

- **D-1. Build it at all?** **RULED:** build ("rest as recommended", Joshua, 2026-10-11 (about 17:15Z), in the live-wiring lane session: "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended").
- **D-2. Executor.** **RULED:** a Claude worker, to keep one writer for the lane (decision packet §5). Not GLM, and no @codex unless Joshua asks.
- **D-3.** Confirm the §0.5 defaults (A)–(E). **RULED:** confirmed.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test-ops` and one `fp check` by the worker, plus the coordinator's one unskipped parity run. Budget: two full suite runs. A third run is a checkpoint.
- **Decisions the executor will hit:** none beyond (A)–(E).
- **What would make this moot:** D-1 = withdraw. A Tradeify NO-GO does not make it moot (J-4).
- **Evidence binding:** only the worker's records at the returned head, plus the coordinator's unskipped parity run at that same head. A later push voids them.
- **Measure:** wall time, runs and rounds are filled in at return.
