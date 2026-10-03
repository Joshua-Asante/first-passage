# Protection redelivery source-health admission, D-7 = B for #631 (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-03. Drafted by a coordinator-(3) worker and not dispatched. **NOT DISPATCHABLE** until every §11 gate holds. Gate G-1 is Joshua's C3-rule admission of the named bound-code edits, and it is **PENDING Joshua**. Coordinator (3) then answers §12, commits the frozen revision under the committed-handoff rule, and records its SHA in the ledger before any executor starts. Dispatch is a separate decision.

**Base:** drafted at `origin/main` `04a86ac`. Every `file:line` below is at that commit unless it is marked otherwise.

**Authority:**
- **Operator ruling D-7 = B** (Joshua, directly to coordinator (3), 2026-10-03 at about 19:34Z: "go with your recommendation and proceed"). He was answering coordinator (3)'s recommendation of option B in #631's card §12 D-7 (`origin/claude/ra2-offline-card` `a38d89a`, `docs/briefs/handoffs/2026-10-03-ra2-offline-four-sources-card-DRAFT.md:265-271`). Option B sends the non-loosening prepared continuations (first-time attaches and tightenings) before the feed halt, and holds loosenings. This card records the ruling as coordinator (3) relayed it; coordinator (3) records it in the ledger at freeze.
- **The cost B carries, as coordinator (3) stated it with the same recommendation:** B "needs a small change to the order-protection code (book_protection_owner.py, bound qualification code)". That means its own card plus Joshua's admission of the edit. This is that card.
- **Not given:** Joshua's C3-rule admission of the bound-code edits. That is gate G-1 (§11), PENDING Joshua.

**Executor:** a Claude worker, single writer of `claude/protection-source-health` (proposed), cut per §9. **Not GLM.** The slice edits the protection owner's loosening admission, which is risk-control code.

**Coordinator:** coordinator (3). It owns the freeze, diff review, integration, the Codex relay, PRs, the ledger, and the re-scope of #631 that this card unlocks (§2.7).

**Owners this card narrows (it changes none of them):**
- [#631's R-A2 card](https://github.com/Joshua-Asante/first-passage/pull/631) §2.2 and §12 D-7, the consumer of the input this card adds.
- [Track B umbrella](2026-09-10-track-b-qualify-accepted-book-umbrella.md): offline-testable build, and "No two live packets share a file" (`:245`).

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_joshua_c3_admission_recorded
  - offline_synthetic_only
  - card_section2_files_only
  - book_account_owner_order_per_section_9
  - c1_rail_listener_per_d3
  - no_book_evaluate_loop_edit
  - no_existing_test_or_fixture_edit
  - no_classifier_edit
  - no_schema_migration_table_or_occurrence_state
  - no_module_global_added_to_bound_modules
  - no_measured_closure_or_p7_closure_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_rail_arm
  - no_rail_deploy
  - no_account_traffic
  - no_live_or_route_wiring
  - no_host_or_fly_command
  - no_pine_or_port_access
  - no_private_bytes_committed
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_book_protection_source_health.py
  - tests/ops/test_book_runtime_occurrences.py
  - tests/ops/test_book_protection_evidence.py
  - tests/ops/test_book_loop_continuation.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_feed_omission_session_end.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_book_protection_lifecycle.py
  - tests/ops/test_book_protection_ownership.py
  - tests/ops/test_book_protection_producer.py
  - tests/ops/test_book_protection_review.py
  - tests/ops/test_book_protection_review6_edges.py
  - tests/ops/test_book_ingress_validation.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_seal.py
  - tests/ops/qualification/test_composition_fixture.py
  - tests/ops/qualification/test_composition_route.py
  - tests/ops/qualification/test_runtime_inventory.py
```

`test_book_protection_source_health.py` is new. The other nineteen exist and must stay green unchanged. The last five are there because two edited files are bound qualification code (§11 G-1): the trust-domain and seal suites, and the three composition suites, since `tests/ops/qualification/composition_fixture.py:83` binds `c1_rail.book_account_owner` as `listener_account_owner`. A module global that was not value-comparable once broke 33 seal and composition tests (`docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md:736-739`), so the targeted run includes all five, and the revert trigger (§4) covers them.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

1. **Premise.**
   - Gate G-1 is recorded in the ledger: Joshua's words and time, naming the §2.6 edits to `book_protection_owner.py` and `book_account_owner.py`.
   - The frozen card's SHA is recorded.
   - Every §9 predecessor is merged, and HEAD descends from those merges.
   - No `.env` exists in the worktree.
   - If any of these fails, **stop**.
2. **Rule-0 reads.** Read each one; do not infer it. Line numbers are at `04a86ac`; re-locate each one on the build base.
   - `ops/c1_rail/book_protection_owner.py`:
     - `_protection_admission` (`:475-496`): the fence (`:477-478`); `SCHEDULED_EXIT` (`:479-480`); the settlement binding (`:481-483`); the loosening admission (`:484-495`), including the session bound (`:487`), which returns `risk_add_not_authorized` (`:495`).
     - `_dispatch_protection_locked` (`:498-517`): every reason outside `(None, 'awaiting_evidence', 'intervention_fence')` (`:500`) marks unsent children `refused` and the operation `terminal` (`:501-516`).
     - `_prepare_dispatch_protection_locked` (`:519-`):
       - the fences `:525-526` and `:577-578`;
       - the `attach` primitive for a never-protected fill (`:556`) and its deadline (`:559-561`);
       - the pending-operation deferral at preparation (`:546-549`);
       - the dispatch-time read (`:568-572`);
       - the evidence waits (`:583-586`);
       - `amend_deferred` and `consumed_protection` (`:589-593`);
       - the loosening test on the refreshed row (`:594-596`), the admission call (`:597-600`), the no-change `noop` (`:602-605`), the reservation (`:611-615`) and `unchanged_protection` (`:616-617`).
     - `_check_protection_deadlines_locked` (`:177-182`) and `PROTECTION_PERIOD` (`:24`).
   - `ops/c1_rail/book_protection.py`: `is_loosening` (`:140-149`). Against `None` it compares with an empty `Bracket()`, so a limit change reads as loosening (`:141-143`).
   - `ops/c1_rail/book_account_owner.py`:
     - `dispatch` (`:1654-1660`);
     - `_dispatch_locked` (`:1662-1731`): the send-suppression raise (`:1664-1665`), the continuation test (`:1694-1696`) and the stored-result replay when it fails (`:1697-1698`), the protection branch (`:1707-1708`) and the occurrence disposition (`:1728-1730`);
     - `_halt_db` (`:2088-`): an inserted incident raises the owner generation (`:2093-2094`), so after any halt every prepared continuation fails the continuation test;
     - `request_classification` (`:853-858`), `FENCED_STATES` (`:279`), and STALE one bar after an entry with no accepted terminal (`:893-896`), which the loosening admission reads at `book_protection_owner.py:492`;
     - `occurrence_state` (`:1628-1637`) and `_validate_occurrence_state_db` (`:1590-1611`).
   - `ops/c1_signal_daemon/book_runtime.py`:
     - `FourLegRuntime.__init__` (`:97-99`, owner type check);
     - `_retain_local_refusal` (`:271-280`);
     - `on_completed_bar`'s barrier completion (`:426`);
     - `redeliver_prepared_boundary` (`:432-468`): the ownership check (`:436-437`), the window check (`:438-440`), the redelivery filter (`:453-454`), dispatch (`:456`), `waiting` (`:458`) and completion (`:464-467`).
   - `ops/c1_rail/c1_rail_listener.py` `handle_book_action` (`:81-91`): a type check and a forward, nothing else.
   - `ops/c1_signal_daemon/book_evaluate_loop.py` `step` (`:29-58`), read only. Redelivery is at `:43-46`, and #631 owns this file.
   - `ops/c1_rail/qualification/trust_domain.py` `_PRODUCTION_CODE` (`:140-181`): `'listener_account_owner':'c1_rail.book_account_owner'` (`:146`) and the runtime dependency `'c1_rail.book_protection_owner'` (`:162`).
   - #631's card at `49f1b69` (`origin/claude/ra2-offline-card`): §2.2 (`:115-135`), cases 14-18 (`:178-184`), its premise rule (`:186`), §12 D-7 (`:280-286`).
   - Test fixtures: `waiting_runtime` (`tests/ops/test_book_runtime_occurrences.py:40-64`, a first-time attach; it hard-codes `Bracket(stop=98)` at `:53`); the synthetic broker's `drop_reads` (`ops/c1_rail/book_synthetic_protection.py:52`); the binding extension in `tests/ops/test_book_loop_continuation.py:51-57`; `ProtectionScenario` (`tests/ops/book_protection_fixtures.py:12`, `establish` `:73`).
3. **Findings returned before code.** The coordinator acknowledges each one.
   - (a) **Closures and pins.** Report whether any §2.6 file is in the 68-module Stage 1c measured closure or the T00 P7 40-module first-party closure (C′ card D8, `docs/briefs/handoffs/2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md:259-264`). Report whether it is in the import closure of the S5 Linux selection (ledger `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:1921`). Report whether any committed file pins its SHA-256.
     - **The drafter's reading at `04a86ac`:**
       - The closure table (`stage1c_closure_table.py.txt . 072c133 04a86ac`) gives 68 modules, membership the same as at `072c133`, and none of the four code files.
       - The P7 list holds none of them.
       - An approximate static closure of `test_campaign_part_a_linux.py` plus the boundary `conftest` (91 modules; the S4 nodes were not computed) holds none of them.
       - `git grep` of each file's blob SHA-256 finds no pin.
     - **Any yes is a stop.** A measured-closure member routes to coordinator (3) for the ENG-2 re-measure (ledger `:983`) before any code.
   - (b) **Who produces `awaiting_evidence`.** Report whether anything in `ops/` other than `book_protection_owner.py:584` and `:586` returns `awaiting_evidence`, which would put a non-`BracketAmend` into redelivery. Any other producer is a **stop**.
   - (c) **Refusal-reason vocabulary.** Report whether any code or fixture treats `refusal_reason` as a closed vocabulary that would reject or misread `held_unhealthy`: adapters' refusal handling, `tests/sequence_verification/**`, migration fixtures, telemetry. Give `file:line`. The drafter found none in `ops/`.
   - (d) **Existing callers.** List every caller of `redeliver_prepared_boundary`, `handle_book_action` and `BookAccountOwner.dispatch`, and confirm none passes `sources_healthy`. The drafter found these:
     - `book_evaluate_loop.py:44`;
     - `book_runtime.py:412`, `:418`, `:456`;
     - `test_book_protection_evidence.py:19`;
     - `test_book_runtime_occurrences.py:73`, `:78`, `:86`, `:103`;
     - the direct `dispatch`/`handle_book_action` calls in the owner and runtime tests.
   - (e) **Module globals.** Confirm the build adds no module-level global to `book_protection_owner.py` or `book_account_owner.py` (bound modules; see the seal note under the authority block). The new reason string is a literal inside functions.
   - (f) **Recovery and halts.** Confirm that a new runtime, a new boot or any halt never lets a held member be redelivered, exactly as for an evidence wait. The runtime's ownership check is `:436-437`. The owner's generation and boot check is `:1694-1696`; a halt raises the generation (`:2093-2094`), so the owner replays the stored result with no command (`:1697-1698`).

## 0.5. Routing and clarifying questions

This is a Claude worker, not GLM. It is offline and synthetic: synthetic brokers, clocks injected by tests, and no network, account, host, Pine, port, `.env` or private value. Coordinator (3) answers §12 at freeze. G-1 is Joshua's. Any open decision that Phase 0 needs is returned as NEEDS_CONTEXT and never assumed.

**Correction to the dispatch request.** The request placed `redeliver_prepared_boundary` in `book_account_owner.py`. It is `FourLegRuntime.redeliver_prepared_boundary` in `ops/c1_signal_daemon/book_runtime.py:432`. It reaches the owner through `handle_book_action` (`c1_rail_listener.py:81-91`), then `BookAccountOwner.dispatch` (`:1654`), then `_dispatch_protection_locked` (`book_protection_owner.py:498`). So `book_runtime.py` is **strictly required**. It holds the signature, the waiting test (`:458`) and the local-refusal filter (`:273`). The listener shim is on the path too (D-3).

## 1. Goal

Add a source-health input to prepared-continuation redelivery: `redeliver_prepared_boundary(bar_time, *, now, sources_healthy=True)`.
- **When `sources_healthy` is False,** the owner's admission still sends first-time attaches and non-loosening amends (tightening, or equal, which stays a no-op). It judges each one by its **own** fresh dispatch-time read and its own loosening test (`:568-572`, `:594-596`). A loosening that the owner would otherwise send is **held**: a new non-terminal waiting result, `held_unhealthy`. It is never refused or terminal, so a later healthy step of the same runtime can still send it, inside its continuation window and before its protection deadline, **but only when no incident intervenes**.
- **After any halt, a held loosening is never redelivered** (coordinator (3) R2, 2026-10-03; ACCEPTED as the B behaviour, in the safe direction). The halt raises the owner generation (`book_account_owner.py:2093-2094`). The continuation test then fails (`:1694-1696`), and the owner replays the stored `held_unhealthy` result with no command (`:1697-1698`). The loosening ends in the protection-deadline fault (G8), with the position still on its existing, tighter protection. In #631's flow the `feed` halt follows every unhealthy redelivery in the same step, so there a held loosening always ends this way.
- **When the input is True or omitted,** behaviour is exactly as today.

**B's residual.** An attach with no fresh evidence still returns `awaiting_evidence` (`:583-586`), and after the feed halt that follows it is never redelivered either (the same replay; G3). B narrows A's unprotected-fill exposure; it does not close it (#631 `:271`).

**Boundary:** nothing is wired. This card adds the input and its owner semantics. #631's loop passes it (§2.7), under #631's own re-scoped card.

## 2. Scope

### 2.1 The input, end to end (keyword-only, default True)

- **`FourLegRuntime.redeliver_prepared_boundary(bar_time, *, now, sources_healthy=True)`** (`book_runtime.py:432`).
  - The first statement requires `type(sources_healthy) is bool`; otherwise it raises `TypeError` and dispatches nothing. This runs before the ownership check at `:436`.
  - The value is forwarded on the dispatch call at `:456`.
- **`handle_book_action(action, owner, *, occurrence=None, now, sources_healthy=True)`** (`c1_rail_listener.py:81-91`): forward to `owner.dispatch` only (D-3).
- **`BookAccountOwner.dispatch(..., sources_healthy=True)`** (`:1654`).
  - It raises `TypeError` for a non-`bool` before acquiring the serializer, and records nothing.
  - `_dispatch_locked` (`:1662`) forwards the value only at the `BracketAmend` branch (`:1708`). Every other action type ignores it (finding (b): only a `BracketAmend` continuation is ever redelivered).
- **Owner protection path:** `_dispatch_protection_locked` (`:498`), then `_prepare_dispatch_protection_locked` (`:519`), then `_protection_admission` at the call `:597-598`. Each passes the keyword through.
- **Existing callers pass nothing** (finding (d)) and keep today's behaviour byte for byte (D-2).

### 2.2 Owner admission (`book_protection_owner.py`)

- `_protection_admission(db, occurrence, rows, *, now, weakening, sources_healthy=True)`. Today's body runs first and unchanged: the fence, `SCHEDULED_EXIT`, the settlement binding, then the loosening admission (`:477-495`). **Only** where today's body would return `None` (admit), and `weakening` is true, and `sources_healthy` is False, it returns `'held_unhealthy'`.
  - So a refusal or a fence always takes precedence over a hold. A hold replaces only a send.
  - A loosening refused today (outside the session `:487`, or any other `:486-494` condition) is still `risk_add_not_authorized`, and still terminal (`:500-516`).
- **Classification is the owner's own and is unchanged.** `weakening` becomes true only through `old is not None and is_loosening(old, effective, side)` (`:595-596`), on the row as the dispatch-time read (`:568-572`) and the evidence checks (`:583-586`) leave it. The loop never classifies (#631 §2.2).
  - A first-time attach (`old is None`; primitive `attach`, `:556`) is never weakening, so with fresh evidence it is sent.
  - A limit change is loosening by the owner's test (`book_protection.py:142-143`), so it is held.
  - An equal bracket stays a `noop` and returns `unchanged_protection` (`:602-605`, `:616-617`), as today.
- **Early return.** `held_unhealthy` leaves by the same early-return path as `awaiting_evidence` (`:584`, `:586`). The `operations` table gets no insert (`:611-615`), and nothing is sent.
  - The children keep status `awaiting_evidence`. Each protection row keeps its `pending_operation` and `deadline`.
  - Earlier children in the same loop keep the partial updates that today's early returns already leave (`quantity`/`old`, or `noop`).
- **Mixed scope.** `weakening` accumulates across children (`:595-596`), so a parent with any loosening child is held whole, tightening children included (D-5).
- **`_dispatch_protection_locked`** (`:500`): add `'held_unhealthy'` to the exempt tuple, so a held parent's children are not marked `refused` and its operation is not made `terminal` (`:501-516`).

### 2.3 Owner occurrence disposition (`book_account_owner.py`)

At `:1729`, a `held_unhealthy` result stores occurrence **state** `awaiting_evidence`. The stored result keeps reason `held_unhealthy`.
- That keeps the occurrence a continuation (`:1694-1696`), and keeps it visible to the runtime's redelivery filter (`book_runtime.py:453`).
- No new state is added, and `_validate_occurrence_state_db` (`:1590-1611`) is unchanged.

### 2.4 Runtime continuation (`book_runtime.py`)

- `:458`: `waiting` is true for `awaiting_evidence` **or** `held_unhealthy`. So the barrier stays incomplete (`:464-467`), and `bar_time` stays in `pending_bar_times`.
- `:273`: `_retain_local_refusal` treats `held_unhealthy` like `awaiting_evidence`. It records no local refusal, and the adapter gets no refusal feedback.
- `on_completed_bar` (`:426`) is unchanged and never passes the input.

### 2.5 What does not change

- **Healthy steps** (True or omitted): byte-identical, including evidence timing and terminal rules.
- **After a halt nothing is sent, through two existing mechanisms.**
  - *A prepared continuation* (every redelivery) never reaches protection dispatch. The halt raises the owner generation (`book_account_owner.py:2093-2094`), the continuation test fails (`:1694-1696`), and the owner replays the stored result with no command (`:1697-1698`). So a redelivery after a halt returns the stored reason (`awaiting_evidence` or `held_unhealthy`), not `intervention_fence` (G3, G8).
  - *A fresh dispatch* under INTERVENTION returns `intervention_fence` at `book_protection_owner.py:525-526` (or `:577-578`), before the admission call, so the hold is never reached (G4). After an input-incident storage failure, `_dispatch_locked` raises first (`book_account_owner.py:1664-1665`).
  - The admission's own fence (`:477-478`) stays ahead of the hold, so a hold never replaces a fence.
- **Every loosening refusal** (`:486-495`, including outside-session `:487`): still refused and terminal.
- **The evidence waits** (`:583-586`) and `amend_deferred`/`consumed_protection` (`:589-593`): unchanged, and still ahead of admission.
- **Protection deadline** (`:177-182`): a held member keeps the deadline it was prepared with (`prepared + PROTECTION_PERIOD`, `:559`). A hold never clears or extends it.
- **Continuation ownership and window** (`book_runtime.py:436-440`; `book_account_owner.py:1694-1696`): unchanged.
- **The classifier** (`is_loosening`, `changed_components`, `book_protection.py`): untouched.

### 2.6 Files

- **Allowed:**
  - `ops/c1_rail/book_protection_owner.py`: `_protection_admission` (§2.2); `_dispatch_protection_locked` (the `:500` tuple and the pass-through); `_prepare_dispatch_protection_locked` (the pass-through at `:597-598`). Nothing else.
  - `ops/c1_rail/book_account_owner.py`: `dispatch` (`:1654-1660`) and `_dispatch_locked` (the signature at `:1662`, the forward at `:1708`, the disposition at `:1729`). Nothing else. The disposition line goes beyond a pass-through, and it is strictly required: without it a held occurrence becomes `complete` and is never redelivered.
  - `ops/c1_signal_daemon/book_runtime.py`, **strictly required** (§0.5): `redeliver_prepared_boundary` (`:432-468`) and `_retain_local_refusal` (`:273`). Nothing else.
  - `ops/c1_rail/c1_rail_listener.py` `handle_book_action` (`:81-91`): the keyword forward only, subject to D-3.
  - `tests/ops/test_book_protection_source_health.py` (new). Its synthetic fixtures live in that file.
- **Everything else is out of scope (§5).** That includes `book_evaluate_loop.py`.

### 2.7 The interface #631 consumes (canonical here; #631 builds the loop side)

This card's API is canonical (coordinator (3) R1, 2026-10-03). #631 is at `49f1b69` (`origin/claude/ra2-offline-card`), which carries the folds this card's review found owed to it (below).
- **The exact call.** When a source is unhealthy in session, #631's loop calls `runtime.redeliver_prepared_boundary(bar_time, now=now, sources_healthy=False)` for each pending boundary, then `owner.halt(..., "feed", now=now)`, and returns. The method is `FourLegRuntime.redeliver_prepared_boundary(bar_time, *, now, sources_healthy=True)` (§2.1): keyword-only, exact `bool`, default `True`. A healthy step omits the keyword. `book_runtime.py` stays forbidden to #631.
- **What #631 relies on:**
  - a loosening that would be sent returns reason `held_unhealthy`, never a refusal or `terminal`: its child stays `awaiting_evidence` with no `operations` row, and the protection row keeps `pending_operation` and `deadline` (§2.2);
  - the stored occurrence state for `held_unhealthy` is `awaiting_evidence` (§2.3), so the occurrence stays a continuation and stays visible to the redelivery filter (`book_runtime.py:453`);
  - barrier semantics: the runtime counts `held_unhealthy` as waiting (`:458`), so `B` stays in `pending_bar_times`, its retained barrier is not completed (`:464-467`), and no local refusal is recorded (`:273`). A redelivery with no member still waiting completes the barrier, as today;
  - tightenings, equal brackets and attaches with fresh evidence behave exactly as with `True` (G1, G2).
- **After the halt (R2).** The `feed` halt follows the hold in the same step, so a held loosening is never redelivered. The halt raises the owner generation (`book_account_owner.py:2093-2094`), and any later redelivery replays the stored result with no command (`:1694-1698`). The loosening ends in the protection-deadline fault (G8), with the position still on its existing, tighter protection. The "later healthy step" (§1) exists only when no incident intervenes. Coordinator (3) ruled this ACCEPTED as the B behaviour (safe direction).
- **Ordering when redelivery raises.** Redelivery can raise: at the window check (`book_runtime.py:438-440`), the occurrence-replay halt (`:447-449`) or the undispatched-member check (`:451-452`). In B's order a raise would skip the `feed` halt, so #631 owes a halt that runs even when redelivery raises (a `finally`).
- **Folds owed to #631 from this card's review, carried at `49f1b69`:**
  - step 2 names this API (at `7dc1ebc` it named `BookAccountOwner.redeliver_prepared_boundary`, which does not exist);
  - finding (f) checks this API and the `:458` waiting rule, and its §10 grep includes `book_runtime.py`;
  - case 14 observes the entry's accepted terminal and asserts no fenced state (F1's premise, §3);
  - case 15 cites the replay (`:1694-1698`, `:2093-2094`), not the `:525-526` fence;
  - the halt runs in a `finally` (case 18);
  - R2 is stated in its §2.2 and §12 D-7.

  Coordinator (3) confirms these at #631's freeze.
- #631's case 14 holds: the loosening returns `held_unhealthy`, `B` stays incomplete, and nothing is sent for it. Cases 15 and 16 invert: the tightening, and the attach with fresh evidence, are sent before the halt.
- #631's B build starts from `main` after this card's build merges.

## 3. Method

- **Tests first.**
  - On the base, every new case that passes `sources_healthy` fails at the call with `TypeError`, because the keyword is absent. That counts as red only for the interface, as #631 §3 counts a missing module.
  - Each fail-first case (F1, F2) must also be shown red **on an assertion** against each of its named scratch mutants of the build.
  - Each guard case (G1-G8) must be green on the build and red against its named mutant.
  - A mutant is a scratch edit made in the worktree, run once through the launcher, and reverted before commit. It is never committed, and `git diff --stat` at return must not show it.
- **Preservation** suites stay green on base and build, unchanged. No red evidence is fabricated for them.
- **Fixtures.** Import, never edit:
  - `waiting_runtime` for a first-time attach. It hard-codes `Bracket(stop=98)` (`test_book_runtime_occurrences.py:53`), so G2's limit variant uses a local copy of its body (`:40-64`) in the new file, with the bracket as a parameter. The original stays unedited;
  - the binding extension pattern of `test_book_loop_continuation.py:51-57`, monkeypatched inside the new file, **plus the entry's accepted terminal**, so that a loosening passes today's admission:
    - the terminal is `account.observe(BrokerFact.terminal(<entry operation id>, "filled", 1, t))`, with `t` inside the entry's first bar and before `B` is prepared;
    - without it, the entry request is STALE one bar after entry (`book_account_owner.py:893-896`), and the loosening admission refuses it as `risk_add_not_authorized` (`book_protection_owner.py:492`) before any hold;
    - if D-4 orders this card after TB-I3 S2, S2's latch also closes admission once it observes STALE (TB-I3 card §2.6), so the terminal must come before any classification read made one bar or more after entry;
  - `ProtectionScenario.establish` for an established bracket and for multi-fill scope;
  - the synthetic broker's `drop_reads` for a member with no fresh evidence.
- **Premise assertions.** Cases that rely on a loosening or a tightening assert their premise with the owner's own test on the refreshed row (`ever_protected`, `observed` not `None`, and `is_loosening(observed, effective, side)` True or False), as #631 `:186` does. Attach cases assert the target is not `ever_protected` and its `observed` is `None`. Every case that sends or holds a loosening also asserts that no value of `account.request_classification(now=<dispatch now>)` is in `FENCED_STATES` (`book_account_owner.py:279`).

## 4. Acceptance checks (falsifier-first)

**H:** with this slice built, no synthetic trace lets a prepared continuation dispatched with `sources_healthy=False` send a loosening, as the owner classifies it after its dispatch-time read. No such trace holds or refuses anything that the same trace with `sources_healthy=True` would send, unless it loosens. A held loosening is never terminal: when no halt intervenes, a later step of the same runtime with `sources_healthy=True`, inside the continuation window and before the protection deadline, sends it exactly as today. After a halt it is never redelivered: the owner replays its stored result with no command, and it ends in the protection-deadline fault (R2; G8). With the input True or omitted, every outcome equals the base.

**Reject if:**
- a fail-first case is not red on an assertion against each of its named mutants;
- a guard case is not green on the build, or not red against its mutant;
- any case fails on the build;
- any preservation suite changes outcome;
- the closure re-check (§10) shows a §2.6 file in the measured closure, or a membership change;
- `git diff --name-only` leaves §2.6.

**Revert trigger:** any outcome change in an existing suite in the authority block.

**Fail-first cases** (`test_book_protection_source_health.py`):
1. **F1: an unhealthy loosening is held, then sent on a healthy step.**
   - *Set-up:* a fill with established protection and the entry's accepted terminal (§3), then a later prepared boundary `B` whose `BracketAmend` loosens. The amend is `awaiting_evidence` and unattempted, admitting evidence has arrived, and the binding is extended. *Premise:* no value of `request_classification(now=t1)` is in `FENCED_STATES` (§3).
   - *Step 1:* `redeliver_prepared_boundary(B, now=t1, sources_healthy=False)` gives:
     - reason `held_unhealthy` and no broker command;
     - occurrence state `awaiting_evidence`, not attempted;
     - child status `awaiting_evidence`, not `refused`, and no `operations` row for the child;
     - the protection row keeps `pending_operation` and `deadline`;
     - `B` still in `pending_bar_times`, and the retained barrier not completed;
     - `pending_feedback` unchanged (no local refusal).
   - *Step 2:* the same runtime, at `t2` inside the window and before the deadline, with the input omitted and no halt or other incident in between, sends exactly one bracket command with the loosened bracket, and `B` completes.
   - *Mutants, each red on its own:*
     - (i) the hold branch removed, so the keyword is accepted and ignored (step 1 sends);
     - (ii) the `:500` tuple not extended (the children are refused, and step 2 sends nothing);
     - (iii) `:1729` not mapped (the occurrence is `complete`, and step 2 skips it);
     - (iv) `:458` not counting the hold (`B` completes at step 1);
     - (v) `:273` not excluding it (a local refusal is recorded).
2. **F2: exact-bool input.** `sources_healthy` set to `0`, `None`, `"False"` or an object raises `TypeError` at `redeliver_prepared_boundary` and at `BookAccountOwner.dispatch`, before any dispatch. There is no broker command and no row change.
   - It includes an unowned call: `redeliver_prepared_boundary(<a bar_time not prepared in this runtime>, now=..., sources_healthy="False")` raises `TypeError` at the runtime. On an owned `bar_time` the owner's check would raise anyway, so only the unowned call shows the runtime check, which runs before the ownership return at `:436-437`.
   - *Mutants, each red on its own:* (i) a truthiness test (`"False"` is then treated as healthy); (ii) the runtime check removed (the unowned call returns `()`).

**Guard cases** (`test_book_protection_source_health.py`):
- **G1: an unhealthy tightening is sent.** This is F1's set-up with a tightening amend. With `False` it sends the same command as with `True`, and `B` completes. A parametrized equal bracket returns `unchanged_protection` with no command, in both modes. *Mutant:* hold every amend when unhealthy.
- **G2: an unhealthy first-time attach with fresh evidence is sent.** Use `waiting_runtime`, with evidence arriving as in `test_book_protection_evidence.py:16-20`. With `False` the attach command is sent and `B` completes. Parametrize the attach with a bracket carrying a limit, using the local copy of `waiting_runtime` (§3): the owner never treats an attach as weakening (`old is None`, `:595`), although `is_loosening(None, ...)` alone reads the limit as loosening. *Mutant:* drop the `old is not None` guard at `:595`.
- **G3: B's residual.** Use `waiting_runtime` with no fresh evidence (`broker.drop_reads = True`). With `False` the result is `awaiting_evidence`, with no command and `B` incomplete. Then `owner.halt(<unique id>, "feed", now=...)`, then a healthy redelivery inside the window. The owner generation is one higher (`book_account_owner.py:2093-2094`), the continuation test fails (`:1694-1696`), and the owner replays the stored result (`:1697-1698`). So the reason is `awaiting_evidence`, not `intervention_fence`; there is no command; and `B` stays in `pending_bar_times`. *Mutant:* the evidence checks (`:583-586`) skipped when the input is False.
- **G4: a hold never replaces the fence on a fresh dispatch.** Halt the owner (`owner.halt(<unique id>, "feed", now=...)`). Then dispatch new occurrences directly with `BookAccountOwner.dispatch(..., sources_healthy=False)`, each on its own fixture: a tightening, a first-time attach with evidence, and a loosening, each with its premise asserted before the halt (§3). Each returns `intervention_fence` at `book_protection_owner.py:525-526` and sends nothing; the loosening does not return `held_unhealthy`. A continuation after a halt never reaches this fence (§2.5); G3 and G8 cover that route. *Mutant:* under `False`, `held_unhealthy` returned ahead of the `:525-526` fence.
- **G5: an outside-session loosening is still refused.** Use a binding variant whose `session.risk_add_cutoff` falls inside the continuation window, with a loosening whose evidence has arrived, the entry's accepted terminal (§3), and `now >= risk_add_cutoff`. The test does not run `advance_schedule`, so authority stays NORMAL. With the premise asserted (no fenced state, §3), the session bound (`:487`) is what refuses. With `False`:
  - the reason is `risk_add_not_authorized`;
  - the child's `protection_operations` status is `refused`, and the protection row's `pending_operation` and `deadline` are cleared (`:509-514`);
  - the child was never attempted, so it has no `operations` row (rows are inserted only at `:611-615`), and the `UPDATE` at `:515-516` changes nothing. Assert that no `operations` row exists for it;
  - a later healthy redelivery sends nothing.

  *Mutant:* the hold check placed ahead of the loosening refusal (`:484-495`).
- **G6: a mixed-scope parent is held whole.** Two fills under one `BracketAmend` scope; one child tightens and one loosens (`ProtectionScenario`, with `BookAccountOwner.dispatch` called directly on one occurrence, so the case holds under either D-3 route). With `False`: `held_unhealthy`, and no command for either child. Then, on the same occurrence inside the deadline, with the input omitted: both are sent. *Mutant:* a per-child hold that sends the tightening child.
- **G7: a healthy step equals the base.** For the traces of F1, G1, G2, G3 and G5, two fresh fixtures run the same trace, one with the input omitted and one with `sources_healthy=True`. After random identifiers (account epoch, boot id, attempt ids) are replaced by stable placeholders, they must give equal:
  - broker command sequences (primitive, bracket, quantity, operation id);
  - results;
  - `action_occurrences`, `protection_operations` and protection row bodies.

  In both runs F1's loosening is sent at step 1, as on the base. *Mutant:* the default flipped to `False`.
- **G8: a hold keeps its deadline, with or without a halt (R2).**
  - (a) After F1's step 1, with no healthy redelivery, a step at `prepared + PROTECTION_PERIOD` records the protection deadline fault (`protection:deadline:<op>`, `:177-182`), exactly as an evidence wait does.
  - (b) #631's flow. After F1's step 1, `owner.halt(<unique id>, "feed", now=...)`, then a redelivery with the input omitted inside the window. The owner replays the stored `held_unhealthy` result (`book_account_owner.py:1694-1698`; generation raised at `:2093-2094`), with no command and `B` still pending. Then the step at `prepared + PROTECTION_PERIOD` records the same deadline fault, and the protection row's `observed` bracket is still the pre-amend one.

  *Mutant:* the hold clears the row's `pending_operation` and `deadline` (both parts red).

**Preservation** (green before and after, unchanged): every other suite in the authority block.

**Runs.** Run each one through the launcher, and cite `record.json`, `verification_exit_code` and `source_stable`:
- `python -I scripts/fp.py doctor`
- `python -I scripts/fp.py python -m pytest <the authority-block acceptance list>`: base (the new file red by interface), then build (green)
- each mutant: `python -I scripts/fp.py python -m pytest tests/ops/test_book_protection_source_health.py -k <case>`
- `python -I scripts/fp.py test-ops`
- `python -I scripts/fp.py check`
- the closure re-check and `git diff --check` (§10)

Disclose any gate failure that already exists on the base; never describe it as a pass.

## 5. Forbidden

- `ops/c1_signal_daemon/book_evaluate_loop.py` (#631 owns it), `daemon.py`, `feed.py`, `bar_source_contract.py` and `book_sources.py`.
- **Inside an allowed file:**
  - any line outside the functions §2.6 names;
  - any change to a fence, evidence, deadline or loosening-refusal condition;
  - any change to the classifier (`is_loosening`, `changed_components`, `ops/c1_rail/book_protection.py`);
  - any new module-level global in `book_protection_owner.py` or `book_account_owner.py`.
- A schema change, migration, new table, new row kind or new occurrence state; any edit to `_validate_occurrence_state_db`.
- **Existing tests and fixtures:** `book_protection_fixtures.py`, the `test_four_leg_runtime.py` helpers, `tests/fixtures/**`, `tests/sequence_verification/**`, `tests/ops/tb_s3_kernel/**`.
- **Locked and qualification code:** `core/**`, `dd_protection`, frozen constants, `book_policy.py`, `POLICY_REGISTRY`, `trust_domain.py`, every qualification module, every measured-closure or T00 P7 closure module.
- **Packaging:** `deploy/**`, Dockerfiles, `.dockerignore`, image manifests and their scripts. The image tests run as preservation only.
- **Documents:** the spec, the umbrella, #631's card, ADRs, STATE and the ledger (coordinator-reserved).
- Pine, ports, manifests and private values.
- GLM; opening a PR, merging or pushing to `main`; arming, deploying, or any host, Fly or account action.

## 6. Return (status taxonomy)

Return exactly one status, as umbrella §6 defines them: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED with its sub-case. The coordinator's verdict is RESOLVED (every §4 item holds) or FALSIFIED (the named items fail, and the card goes back to the executor). The return holds:
- the branch, head SHA, base SHA, `git diff --stat` and the name list;
- the Phase-0 findings (a)-(f);
- for F1 and F2, the red-on-base (interface) record and the red-on-each-mutant and green-on-build record IDs;
- for G1-G8, the green-on-build and red-on-mutant record IDs, with each mutant's diff shown and then reverted;
- preservation, `test-ops`, `check`, the closure re-check and `git diff --check`;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- G-1 is not recorded, or it names fewer edits than §2.6 needs.
- A finding (a) or (b) is yes. Finding (c) finds a closed vocabulary that rejects `held_unhealthy`. Finding (e) needs a module global. Finding (f) fails.
- A §9 predecessor is unmerged, or D-3 is unruled while `c1_rail_listener.py` is still in §2.6.
- Any change outside §2.6 is needed, including an edit to an existing test, a new state or a schema change.
- A held member cannot be made redeliverable inside §2.6.
- A loosening case's premise (no fenced state, §3) cannot be met on the build base, for example because TB-I3 S2's latch closes admission.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- A second writer appears on the branch.

## 8. Out of scope and decision unlocked

**Out of scope:**
- #631's loop change and its re-scope (§2.7);
- source health itself (R-A2);
- `on_completed_bar` under an unhealthy source (#631 feeds no bar then);
- what happens to held or evidence-waiting members across an attended resume (today's deadline and window rules apply unchanged);
- closing B's residual for an attach with no fresh evidence, which needs an evidence-free attach path and a separate ruling;
- production wiring, listener health (R-N) and any live source.

**Unlocked:** once this slice is RESOLVED and merged, coordinator (3) re-scopes #631 to B (§2.7) and freezes it.

## 9. Sequencing and file collisions (coordinator (3) ruling owed: D-3, D-4)

- **`book_account_owner.py`:** the fixed single-writer order (TB-I3 card §9 and GC-5 card §9, coordinator (3) 2026-10-03) is #628, then the GC-5-DISPLACED build, then TB-I3 S2. #628 merged at 2026-10-03T18:19Z.
  - This card's hunks are `dispatch` (`:1654-1660`) and `_dispatch_locked` (`:1662`, `:1708`, `:1729`).
  - They are disjoint from GC-5's: the `__init__`/`boot` keyword, `_decode_reserve` at `_capacity` (`:748`), `Reserve` stamping (`:1804`), the D4 refusal branch and the D5 halt.
  - They are disjoint from TB-I3 S2's latch: `_request_classification_db`, `observe_synthetic_order_evidence`, the entry/add and takeover risk-add branches, and latch path 3 in the terminal branch of `_observe_locked`.
  - The umbrella's single-writer rule (`:245`) still applies. **Proposed: fourth, after TB-I3 S2** (D-4). On that base, the loosening cases must observe the entry terminal before any classification read made one bar or more after entry (§3; S2's latch).
- **`book_protection_owner.py`:** no open card edits it. #631 §5 forbids it, and the GC-5 and TB-I3 cards do not list it.
- **`book_runtime.py`:** no open card edits it. #631 §5, GC-5 §2.5, #651 (TB-I3-HOST) and the D-MON cards (#635, #637) forbid it.
- **`c1_rail_listener.py`:** open draft PR #571 (`claude/c1-unknown-block-durable`, parked) edits `handle_signal` (hunks at `:222` and `:415-429`), not `handle_book_action` (`:81-91`). See D-3.
- **`book_evaluate_loop.py`:** #631 only. This card never touches it.
- **#631 depends on this card:** #631's B build starts from `main` after this card merges.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; 0 violations.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-protection-health-admission-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-protection-health-admission-card-DRAFT.md
# Premise (Git Bash), in the executor worktree.
git rev-parse HEAD; test ! -e .env && echo "no .env" || echo "FAIL: .env present"
gh pr view 628 --json state -q .state                                    # expected: MERGED
gh pr view 571 --json state -q .state                                    # per D-3
grep -n "'c1_rail.book_protection_owner'\|'listener_account_owner'" ops/c1_rail/qualification/trust_domain.py   # bound: :146, :162
grep -n "book_runtime\|c1_rail_listener" ops/c1_rail/qualification/trust_domain.py                             # expected: nothing
grep -rn "refusal_reason=.awaiting_evidence" ops/                        # finding (b): only book_protection_owner.py:584, :586
grep -rn "redeliver_prepared_boundary\|handle_book_action(\|sources_healthy" ops tests   # finding (d)
# Measured-closure re-check (finding (a); at return). Expected: 68 True []
cp docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt "$SCRATCH/closure.py"
python "$SCRATCH/closure.py" . 072c133 HEAD | python -c "import json,sys; m=json.load(sys.stdin)['measured']; print(m['module_count'], m['same_membership'], [r['path'] for r in m['rows'] if r['path'].endswith(('book_protection_owner.py','book_account_owner.py','book_runtime.py','c1_rail_listener.py'))])"
# Scope at return.
git diff --stat "$BASE"...HEAD
git diff --name-only "$BASE"...HEAD | grep -v -e '^ops/c1_rail/book_protection_owner.py$' \
  -e '^ops/c1_rail/book_account_owner.py$' -e '^ops/c1_signal_daemon/book_runtime.py$' \
  -e '^ops/c1_rail/c1_rail_listener.py$' -e '^tests/ops/test_book_protection_source_health.py$' && echo "FAIL: scope"
git diff --check "$BASE"...HEAD
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1: Joshua's C3-rule admission of the named edits. PENDING Joshua.**
  - **Why it is needed.** Both owner files are bound qualification code. In the production trust domain's `_PRODUCTION_CODE`, `book_account_owner` is the `listener_account_owner` role (`trust_domain.py:146`), and `book_protection_owner` is a runtime dependency (`:162`). Editing them changes that code inventory.
  - **What it admits.** The edits are named in §2.2 and §2.6 (`book_protection_owner.py`) and in §2.3 and §2.6 (`book_account_owner.py`).
  - **Who records it.** Coordinator (3) puts the admission to Joshua and records his words and time in the ledger.
  - **Inputs for the admission** (finding (a), drafter's reading at `04a86ac`): neither file, nor `book_runtime.py` or `c1_rail_listener.py`, is in the 68-module measured closure, the T00 P7 closure, or the approximate S5 Linux selection closure. No committed digest pin exists. So this card adds no measured-closure change to the ENG-2 PART_A re-measure (ledger `:983`). If finding (a) differs at the build base, the measurement question routes to coordinator (3), the ENG-2 owner, before any code.
  - `book_runtime.py` and `c1_rail_listener.py` are not in the bound set.
- **G-2: coordinator (3) freeze.** §12 answered, the frozen revision committed, and its SHA recorded in the ledger.
- **G-3: §9 predecessors merged,** in the order D-4 fixes, with D-3 ruled.

## 12. Open decisions (coordinator (3) at freeze)

- **D-1 Result name.** **Recommended:** `held_unhealthy`. It is distinct from `awaiting_evidence`, so the loop, the tests and the operator can tell a held loosening from an evidence wait. Its occurrence state is still `awaiting_evidence` (§2.3).
- **D-2 Default `True`, keyword-only, exact `bool`.** **Recommended.** It keeps `book_evaluate_loop.py` (#631's) and every existing caller unchanged. **Cost:** a caller that omits the input gets today's behaviour, and a loosening is sent. #631's case 14 is the guard against that.
- **D-3 Route.**
  - **Recommended: through `handle_book_action`** (§2.1). It keeps one runtime-to-owner route for redelivery and fresh dispatch. That shares `c1_rail_listener.py` with parked draft PR #571 (disjoint hunks, §9). Coordinator (3) rules whether a parked draft counts as a live packet under the umbrella's single-writer rule (`:245`). If it does, this card waits for #571.
  - **Fallback:** the runtime's redelivery calls `self.owner.dispatch(...)` directly, and `c1_rail_listener.py` leaves §2.6. That is behaviour-equivalent: the runtime already requires a `BookAccountOwner` (`book_runtime.py:98-99`), and the shim adds only that check (`c1_rail_listener.py:89-91`).
- **D-4 Position in the `book_account_owner.py` order.** **Recommended:** fourth, after TB-I3 S2. Coordinator (3) may move it ahead of TB-I3 S2 to unblock #631 sooner. Either way it is cut from `main` after its predecessor merges.
- **D-5 Mixed-scope parent held whole.** **Recommended.** It matches the owner's all-or-nothing parent (one `changes` list, `:573-617`) and today's whole-parent refusal. Splitting would need per-child dispositions. **Cost:** a tightening on one fill waits with a loosening on another fill in the same scope.
- **D-6 Freeze base.** **Recommended:** `main` immediately after the D-4 predecessor merges.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop with launcher records. No Docker, no Linux run, no host.
- **Decisions the executor will hit:** none open after freeze. G-1 is Joshua's, and D-1 to D-6 are coordinator (3)'s.
- **What makes it moot:**
  - Joshua declines G-1, so #631 stays at A;
  - #631 is withdrawn, or a ruling moves source health to the listener (R-N);
  - the attempt ends before a live source matters.
- **Measurements the return fills in:** Phase-0 findings (a)-(f), the per-case and per-mutant record IDs, and the closure re-check.
