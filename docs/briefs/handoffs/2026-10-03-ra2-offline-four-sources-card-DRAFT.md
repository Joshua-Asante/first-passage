# R-A2 offline four-source slice (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT. Drafted 2026-10-03 by a coordinator-(3) worker and not dispatched. §12 is answered; Joshua ruled D-7 = B. Coordinator (3) freezes after this D-7 fold and its review, commits the frozen revision under the committed-handoff rule, and records its SHA in the ledger before any executor starts. **Dispatch waits for the protection-health admission owner card's build to merge (P-row, §0).** Dispatch is a separate decision.

**Authority:**
- **Track B owner disposition, coordinator (3), A9-PREP Q3/Q5, 2026-10-02.** R-A2 is a separate offline card. Track B owns the per-product session window, the four-source composition and the loop's source-health halt. None of these goes into the #619 contract or into the TB-I3 interlock card.
- **Operator ruling A9-PREP Q1, 2026-10-02** (coordinator (3) sheet 2, item 3). If a bar has already been forwarded and a revised version arrives, the source latches `REFUSED` (`revision_after_delivery`). A late bar that cannot be verified also latches `REFUSED` (`late_bar_unverifiable`). #619 implements both at reviewed head `77373bd` (Codex relay CLEAN, 2026-10-03T03:17Z). This card consumes those latches. It does not implement them.
- **Operator ruling D-7 = B, Joshua to coordinator (3), 2026-10-03 ~19:34Z:** "go with your recommendation and proceed", replying to coordinator (3)'s recommendation of option B (§12 D-7).

**Executor:** a Claude worker, single writer of `claude/ra2-four-sources` (proposed), cut from the freeze base. **Not GLM.** This slice writes a halt path into the book loop, and AGENTS.md keeps risk-control code off the GLM lane.

**Coordinator:** coordinator (3). It owns the freeze, diff review, integration, the Codex relay, PRs and the ledger.

**Owners this card narrows (it changes none of them):**
- [Multi-leg rail extension spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) R-A2 (`:145`). The spec names `daemon.py` as the owner file and `test_four_sources_one_per_symbol` as the test.
- [Track B umbrella](2026-09-10-track-b-qualify-accepted-book-umbrella.md): Track B builds everything offline-testable (D-B5, `:76`) and never chooses the feed (O-4, `:108`).
- [S2b build ADR](../../adr/2026-08-08-s2b-signal-daemon-build.md) §2 Reconnect / Staleness / Fail-closed rows. #619 implements them for one source; this card adds the book-wide consequence.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - offline_synthetic_only
  - prerequisite_pr_619_merged
  - prerequisite_owner_card_merged
  - no_wiring_build_loop_cli_or_daemon
  - no_dockerfile_or_image_manifest_edit
  - no_listener_health_report
  - no_live_or_route_wiring
  - no_provider_code_or_credentials
  - no_calendar_code_or_data_edit
  - no_bar_source_contract_edit
  - no_book_account_owner_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_pine_or_port_access
  - no_private_bytes_committed
  - no_host_or_fly_command
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - card_section2_files_only
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_book_sources.py
  - tests/ops/test_book_loop_source_health.py
  - tests/ops/test_bar_source_contract.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_feed_omission_session_end.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
  - tests/ops/test_book_session_calendar.py
  - tests/ops/test_book_loop_continuation.py
  - tests/ops/test_book_protection_evidence.py
  - tests/ops/test_book_runtime_occurrences.py
  - tests/ops/test_book_ingress_validation.py
```

`test_book_sources.py` and `test_book_loop_source_health.py` are new. The other nine already exist and must stay green unchanged (§4). The last four drive `FourLegEvaluateLoop` or its redelivery, which §2.2 reorders.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

1. **Premise.** PR #619 (`claude/a9-prep-barsource`, reviewed head `77373bd`) is **MERGED**, and HEAD descends from that merge. When this card was drafted, #619 was **OPEN** and `origin/main` was `1a350ec`. No `.env` exists in the worktree. The build of the protection-health admission owner card (card on branch `claude/protection-health-admission-card`) is also **MERGED**, and HEAD descends from it (P-row, D-7 = B).
2. **Rule-0 reads.** Read each one; do not infer it. Line numbers are at `a83a464` unless marked "after #619".
   - `ops/c1_signal_daemon/bar_source_contract.py` (after #619): `LEG_FEEDS` (`:53`), `SymbolBinding.__post_init__`, and `ContractBarSource.__init__` (`:192`), which takes typed `binding` and `policy` and a `session_window(ts)` returning an object with `opens_at`/`closes_at`, or `None`. Also `state`/`refusal` (`:199`), `healthy()` (`:214`), `poll()` (`:220`) and `_refuse` (`:304`). The refusal reasons are `auth_rejected`, `binding_expired`, `revision_after_delivery` and `late_bar_unverifiable`. The state vocabulary is `CONNECTED`, `DISCONNECTED` and `REFUSED`.
   - `ops/c1_signal_daemon/book_evaluate_loop.py` `FourLegEvaluateLoop.step` (`:29-58`): the pre-gate block (`:32-38`), then prepared-boundary redelivery (`:43-48`), then the leg loop, which polls each leg and feeds its bar before polling the next (`:49-55`). Redelivery runs before any source is polled.
   - `ops/c1_signal_daemon/book_runtime.py`: `LEG_ORDER` (`:27`), and the bound session `self.owner.binding["session"]` with `opens_at`, `closes_at` and `session_id` (`:349`). `redeliver_prepared_boundary` (`:432-468`) re-dispatches only unattempted `awaiting_evidence` members (`:453-456`) and completes the barrier once none still waits (`:464-467`). `expire_barrier` skips a prepared boundary (`:481-482`).
   - `ops/c1_rail/book_account_owner.py`: `check_source_silence` (`:1046-1065`), which already owns in-session silence, and `halt(incident_id, reason, *, now)` (`:1311`). Reasons are a closed set that includes `feed`. Calling it again with the same id at a different `now` raises "conflicting incident identity" (`:1321-1322`), and that check runs before `_halt_db`. `check_source_silence` already makes its id unique per occurrence: `feed-silence:<session_id>:<anchor>` (`:1064`). An occurrence keeps `awaiting_evidence` as its state (`:1729`). Under INTERVENTION the schedule, close resumption and every runtime send stop (`:1963-1964`, `:1456-1457`, `:1743-1744`).
   - `ops/c1_rail/book_protection_owner.py`, read only. `awaiting_evidence` comes only from the amend path (`:584`, `:586`), so every redelivered member is a `BracketAmend`. Whether an amend loosens is decided only inside dispatch, after the dispatch-time protection read (`:568-572`, `:594-596`). Before the owner card, the loosening admission (`:484-495`) has no source-health input; at the freeze base it takes `sources_healthy` (D-7 = B). These line numbers are pre-owner-card. Under INTERVENTION every amend is refused, tightening included (`:477-478`, `:525-526`).
   - `ops/c1_rail/book_session_calendar.py`: `load_ratified_calendar` (`:583`), `SessionCalendar.rows`, `.products` and `.ratified_at`, plus the `SessionSchedule` fields `permission`, `overlay_blocked`, `opens_at` and `closes_at`. The loaded rows keep neither each product's `matching_open_utc` nor its `matching_close_utc`, and `v` folds in the venue deadline, so neither stands in for a product bound.
   - `ops/calendars/RATIFIED.json`, every calendar file it names (at drafting, `book_session_calendar_2026-09.json` and `-10.json`; `-11.json` from #622 is on `main` but not yet ratified), and `book_closure_overlay.json`, read only.
   - `tests/ops/test_c1_signal_daemon_image_manifest.py`: `_ENTRYPOINTS` includes `book_evaluate_loop.py`, so the loop's import closure must stay inside the daemon image.
3. **Findings returned before code.** The coordinator acknowledges each one.
   - (a) Whether #619 merged with exactly the `state`/`refusal` vocabulary above. Any difference is a **stop**.
   - (b) Whether `LEG_FEEDS` roots equal `SessionCalendar.products` on both ratified calendars, and `set(LEG_FEEDS) == set(LEG_ORDER)`. Any difference is a **stop**.
   - (c) Whether any existing loop test's fake source carries a `state` attribute equal to `REFUSED` or `DISCONNECTED` (`file:line`). Any such fake would change outcome under §2.2; report it, never edit the test.
   - (d) Whether `book_evaluate_loop.py` is in the T00 P7 40-module first-party closure or the 68-module Stage 1c measured closure, and whether any qualification manifest pins its digest. Any yes is a **stop**.
   - (e) Whether anything in `ops/` other than `book_protection_owner.py:584` and `:586` returns `awaiting_evidence`. Any other producer is a **stop**: §2.2 would then also hold back a continuation that is not an amend, and §12 D-7 does not cover that.
   - (f) Whether the merged owner card defines `BookAccountOwner.redeliver_prepared_boundary(..., sources_healthy: bool)`, with the admission at `book_protection_owner.py:484-495` taking `sources_healthy`; whether the loop reaches it without editing `book_runtime.py` (today's redelivery entry is `FourLegRuntime.redeliver_prepared_boundary`, `book_runtime.py:432`); and whether a held loosening leaves its barrier incomplete (today `book_runtime.py:458` and `:464` count only `awaiting_evidence` as waiting). Any difference is a **stop**.

## 0.5. Routing and clarifying questions

This is a Claude worker, not GLM. It is offline and synthetic: fake transports, clocks injected by tests, and the two committed ratified calendars read in place. No secrets, `.env`, Pine, ports, account data, provider code or network are involved. The coordinator answers §12 at freeze; Joshua ruled D-7 = B. Any open decision that Phase 0 needs is returned as NEEDS_CONTEXT and never assumed.

## 1. Goal

Make R-A2 true offline. The book has exactly one contract-enforcing source per order symbol, and each source is bounded by the operator-ratified session calendar. The four-leg loop halts the whole book (reason `feed`) as soon as any source is refused or disconnected inside the bound session, including the two Q1 latches. Before that halt it sends prepared attaches and tightenings that have fresh evidence, and holds loosenings (D-7 = B).

**Boundary:** nothing is wired. The slice adds no daemon constructor, CLI, image change, listener report or live source, so it cannot run outside tests until a later live packet wires it.

## 2. Scope

### 2.1 New `ops/c1_signal_daemon/book_sources.py`

- **`session_window(calendar, product) -> Callable[[datetime], SessionSchedule | None]`.**
  - It refuses (`ValueError`) a calendar whose `ratified_at` is `None` (that is, not loaded through `load_ratified_calendar`), and a `product` that is not in `calendar.products`.
  - The returned callable takes an aware `ts`. It returns the row with `opens_at <= ts < closes_at` only if `row.permission == "PERMITTED"` and `not row.overlay_blocked`. Otherwise, and outside coverage, it returns `None`. The returned row has `opens_at`/`closes_at`, which is the duck type `ContractBarSource` reads.
  - It uses `closes_at`, not `risk_add_cutoff`, because exits and the scheduled flatten need bars after the cutoff.
  - The callable is the same for every product. The §4 calendar tripwire is what makes "per product" true: on every PERMITTED row, each product's raw matching bounds equal the row's.
- **`compose_book_sources(*, transports, bindings, policy, calendar, clock) -> dict[str, ContractBarSource]`.**
  - It returns exactly four `ContractBarSource`s, keyed and ordered by `LEG_ORDER`, with one `TransportPolicy` shared by all four.
  - Each source's `session_window` is `session_window(calendar, LEG_FEEDS[leg][0])`.
  - **It refuses (`ValueError`, building nothing) on any of these:**
    - the key set of `transports` or `bindings` is not exactly `LEG_ORDER`;
    - `bindings[leg].leg_id != leg`, which covers a duplicated leg;
    - two bindings share a `provider_code` or a `venue_contract`;
    - one transport object is reused across legs.
  - Root and exchange checks stay in `SymbolBinding` and are not re-implemented.
- **Imports:** `bar_source_contract`, `book_runtime.LEG_ORDER` and `c1_rail.book_session_calendar`. This module is not in the daemon image closure, and §2.2 must not import it.

### 2.2 Edit `ops/c1_signal_daemon/book_evaluate_loop.py` `FourLegEvaluateLoop.step`

- The pre-gate block stays first and unchanged: protection deadlines, `check_source_silence`, `advance_schedule` (scheduled flatten and close resumption, `book_runtime.py:470-475`), barrier expiry and the INTERVENTION return (`book_evaluate_loop.py:32-38`). The health check never runs ahead of these risk-reducing paths.
- **Prepared-boundary redelivery moves behind the health check** (review P2, #631). Today it runs at `:43-48`, before any poll. A waiting loosening `BracketAmend` is re-dispatched there and passes the loosening admission, which has no source-health input (`book_protection_owner.py:484-495`). The amend is sent and the barrier completes (`book_runtime.py:464-467`), even when a source is already `REFUSED` or `DISCONNECTED`.
- **Then, in this order:**
  1. **Poll** all four sources in `LEG_ORDER` and hold the results. Redeliver nothing and feed nothing yet. An exception from `poll()` propagates out of `step`, so nothing continues unless all four polls return.
  2. **Check health.** Let `session = runtime.owner.binding["session"]`. If `session.opens_at <= now < session.closes_at`, take the first leg in `LEG_ORDER` whose `getattr(source, "state", None)` is `"REFUSED"` or `"DISCONNECTED"`. If there is one (an unhealthy step), in this order:
     - **Redeliver** each pending prepared boundary through the owner card's health-aware entry point, `BookAccountOwner.redeliver_prepared_boundary(..., sources_healthy=False)`, whose admission at `book_protection_owner.py:484-495` takes `sources_healthy` (D-7 = B). The owner sends attaches and tightenings and holds loosenings as waiting (below). An exception from redelivery propagates out of `step` with no bar fed.
     - **Halt:** call `runtime.owner.halt("source-unhealthy:<session_id>:<leg>:<detail>:<now.isoformat()>", "feed", now=now)`, whether or not redelivery left authority INTERVENTION.
     - **Feed no polled bar.** Return the redelivery result under today's `completed` rule (`:43-46`), or `None` if nothing was redelivered.

     `<session_id>` is `session.session_id`. `<detail>` is the state, followed by `:<refusal>` when `refusal` is a non-empty `str`. For example, `source-unhealthy:<session_id>:aegis_6j:REFUSED:revision_after_delivery:<now.isoformat()>`. The id is unique per occurrence (D-2, ruled), following `feed-silence:<session_id>:<anchor>` (`book_account_owner.py:1064`). A repeat of the same leg and detail, in a later session or after an attended resume in the same session, therefore records a new halt and never raises "conflicting incident identity".
  3. **Healthy step, unchanged: redeliver** prepared boundaries exactly as today (`:43-46`); where the owner card's entry point carries the call, `sources_healthy=True` keeps today's admission. If authority is then INTERVENTION, return the redelivery result and feed nothing, as today (`:47-48`). **Disclosed change:** the held bars are dropped. Today, in a healthy step where redelivery reaches INTERVENTION, those bars are never polled and stay with their sources; after §2.2 they have been polled and are lost. After an attended resume, the gap fails closed at the runtime's sequence check (`book_runtime.py:371-381`).
  4. **Feed** the held bars in `LEG_ORDER` through `runtime.on_completed_bar`, exactly as today, then run the trailing `expire_barrier` pass.
- **What an unhealthy step sends and holds (D-7 = B).** The owner, not the loop, classifies each waiting member at its dispatch-time read (`book_protection_owner.py:568-572`, `:594-596`). With `sources_healthy=False` it sends first-time attaches and tightenings whose evidence has arrived, and holds each loosening in the owner card's waiting status, not a terminal refusal. A member whose evidence has not arrived still returns `awaiting_evidence` (`:583-586`) and waits. A held member's barrier stays incomplete, because `expire_barrier` skips prepared boundaries (`book_runtime.py:481-482`). The `feed` halt then fences every held member, the scheduled flatten and close resumption until an attended resume (`book_protection_owner.py:477-478`, `:525-526`; `book_account_owner.py:1963-1964`, `:1456-1457`). After the halt, the owner's existing INTERVENTION and protection-deadline rules apply unchanged (`book_protection_owner.py:177-182`).
- **Why the loop does not sort them.** A `BracketAmend` on a fill that has never been protected becomes primitive `attach` (`book_protection_owner.py:556`), and the owner never treats it as weakening, because its test requires `old is not None` (`:595`). Only the owner classifies, after its dispatch-time read. A loop-side check would read older evidence, and the fresh read could turn its "tightening" into a loosening that is then sent. Flatten and cancel never wait for evidence (finding (e)), so redelivery never carries them; the scheduled flatten and close resumption run in the pre-gate block only while authority is not INTERVENTION.
- **B residual.** An attach with no fresh evidence by the unhealthy step is held and fenced, so its fill has no stop until an attended resume (case 17). B narrows the exposure; it does not close it.
- The loop reads the `state` and `refusal` attributes only. It never calls `healthy()` and never imports `bar_source_contract` or `book_sources`. A fake without `state` counts as healthy, so existing fakes keep their behavior.
- **Staleness at session open never halts.** A connected source with no bar yet is not `REFUSED` or `DISCONNECTED`, and silence stays with `check_source_silence`. Outside the bound session, no source state halts.

### 2.3 Files

- **Allowed:** `ops/c1_signal_daemon/book_sources.py` (new), `ops/c1_signal_daemon/book_evaluate_loop.py` (§2.2 only), `tests/ops/test_book_sources.py` (new), `tests/ops/test_book_loop_source_health.py` (new). Synthetic fixtures go in those test files only.
- **Everything else is out of scope (§5).**

## 3. Method

- **Tests first.** Write each §4 fail-first case and show it failing on the freeze base, with a launcher record, before writing code. On the base, the `book_sources` cases (1-4, including the case-4 tripwire) fail at import because the module is absent. That counts as red only because the missing module is the target. The loop fail-first cases must fail on an assertion.
- **Guard cases** (§4 G1-G4) hold on the base by design. Show each one green on the base, red against its named over-halting mutant, then green on the build. Each mutant is a scratch edit of the built `step`, made in the worktree, run once through the launcher, and reverted before commit. It is never committed, and the return's `git diff --stat` must not show it. Preservation suites stay green on both base and build, and no red evidence is fabricated for them.
- **Fail-closed.** A refused composition builds no source. An exception from `owner.halt` propagates out of `step` with no bar fed.
- **Synthetic sources.** Health cases use real `ContractBarSource`s over a scripted fake `BarTransport` wherever the case concerns the contract's own latches. That covers the Q1 cases (delivered revision, late unverifiable bar), auth rejection and binding expiry. Duck-typed fakes are used only for ordering and spy cases.

## 4. Acceptance checks (falsifier-first)

**H:** with this slice built, no synthetic trace lets the four-leg loop feed a bar, send a loosening continuation, or complete a barrier that still holds a loosening or an evidence-less member, in a step where any source is `REFUSED` or `DISCONNECTED` inside the bound session. In that step, prepared attaches and tightenings with fresh evidence are sent before the `feed` halt (D-7 = B). The pre-gate block still runs first in that step. A step that reaches the health check with an unhealthy source records exactly one `feed` halt; a later step returns at the INTERVENTION guard and records none (case 10). A source at session open with no bar yet never halts. The composition admits only four distinct, calendar-bounded, contract-enforcing sources.

**Reject if:**
- a fail-first case below cannot be made to fail on the base (cases 1-4 count as red by missing module, as §3 says);
- a guard case (G1-G4) is not green on the base, is not red against its named mutant, or is not green on the build;
- a case fails on the build;
- any preservation suite changes outcome;
- the loop's import closure leaves the daemon image.

**Revert trigger:** any outcome change in `test_four_leg_runtime.py`, `test_feed_omission_session_end.py`, `test_book_loop_continuation.py` or `test_c1_signal_daemon_image_manifest.py`.

**Fail-first cases** (`test_book_sources.py`):
1. `test_four_sources_one_per_symbol` (the spec-named test): the result has four sources keyed in `LEG_ORDER`, each a `ContractBarSource` whose binding's leg, root and exchange match `LEG_FEEDS`.
2. Composition refuses: a missing or extra leg, a binding whose `leg_id` differs from its key (a duplicated leg), a duplicate `provider_code`, a duplicate `venue_contract`, and a reused transport object. Each refusal builds nothing.
3. The session window returns:
   - `None` for a DENIED row, an overlay-blocked row, and before and after coverage;
   - the row (`opens_at`, `closes_at`) for a PERMITTED row, with `closes_at` and not `risk_add_cutoff` as the upper bound;
   - a refusal for an unratified calendar and for an unknown product.
4. **Calendar tripwire:** the test reads the **raw JSON** of every calendar file named in `RATIFIED.json`, so a newly ratified month is covered without a test edit. On every PERMITTED row, every product's `matching_close_utc` must equal `closes_utc` and its `matching_open_utc` must equal `opens_utc`. At drafting this held for 2026-09 (18 PERMITTED rows) and 2026-10 (23), and also for the unratified 2026-11 (20), with no mismatch. This test pins the assumption that the calendar's loaded rows cannot express. A future early-close PERMITTED row fails the test and does not pass silently.

**Fail-first cases** (`test_book_loop_source_health.py`):

5. An in-session `REFUSED` source halts at once with reason `feed`, parametrized over `auth_rejected`, `binding_expired`, `revision_after_delivery` (Q1) and `late_bar_unverifiable` (Q1). Each case drives a real `ContractBarSource` into the latch and checks that the incident id is `source-unhealthy:<session_id>:<leg>:REFUSED:<refusal>:<now.isoformat()>`.
6. An in-session `DISCONNECTED` source, after a failed connect or a transport error, halts with reason `feed` (D-1, ruled).
9. **Poll all, then check.** Legs 2–4 delivered boundary `B` in an earlier step. In this step, leg 1 delivers `B` and leg 4 is `DISCONNECTED`. The result is one halt, no dispatch, no `on_completed_bar` call and no completed barrier. Today's code dispatches.
10. With several unhealthy legs, exactly one halt is recorded, for the first in `LEG_ORDER`. The next `step` returns at the INTERVENTION guard and never reaches the health check again, so there is no conflicting-identity raise.
12. Incident ids for the same leg and detail differ across two bound sessions, and each session records its own `feed` halt with no raise.
13. **Halt, resume, halt again.** In one bound session, a leg goes unhealthy and one `feed` halt is recorded. A synthetic resume follows: the test fixture returns the owner's authority to NORMAL, and this card adds no resume API and no owner edit. The same leg is then unhealthy again with the same detail at a later `now`. The result is a second recorded `feed` halt with a different id, no "conflicting incident identity" raise, and no bar fed.
14. **No loosening continuation while unhealthy** (review P2, #631; D-7 = B). A boundary `B` is prepared in this runtime. Its loosening `BracketAmend` is `awaiting_evidence` and unattempted, and protection evidence that admits it has arrived. Use the binding extension at `test_book_loop_continuation.py:51-57`, so that on the base the amend passes the loosening admission and is sent. In the next step one source is `DISCONNECTED`. The result is no broker command for the amend; the amend's result is the owner card's waiting status, not a terminal refusal (its operation is neither `refused` nor `terminal`; today a non-waiting refusal goes terminal, `book_protection_owner.py:500-515`); `B` still in `runtime.pending_bar_times`; `B`'s retained barrier not completed; exactly one `feed` halt; and no bar fed. On the base the amend is sent and `B` completes, so the case fails on the send assertion.
15. **Twin: tightening under the same staleness, sent** (D-7 = B). Same set-up, but the amend tightens. The result is one broker command for the amend, then exactly one `feed` halt, and no bar fed. The send itself shows it preceded the halt, because after the halt the owner refuses every amend (`book_protection_owner.py:525-526`). If the amend was `B`'s only waiting member, `B`'s barrier completes. On the base the amend is sent but no halt is recorded, so the case fails on the halt assertion.
16. **Attach twin, sent** (D-7 = B). Same staleness, but the waiting member is a first-time attach: its target fill has never been protected, so the prepared child's primitive is `attach` (`book_protection_owner.py:556`), as in `waiting_runtime`. Protection evidence that admits it has arrived. The result is one broker command for the attach, then exactly one `feed` halt, and no bar fed: the fill is protected before the halt fences the book. On the base the attach is sent but no halt is recorded, so the case fails on the halt assertion.
17. **B residual: evidence-less attach held and fenced** (D-7 = B). As case 16, but no admitting protection evidence has arrived (`book_protection_owner.py:583-586`). The result is no broker command, the attach's result `awaiting_evidence`, `B` incomplete, exactly one `feed` halt and no bar fed. The case then documents the residual: the fill has no stop, and a later `step` sends nothing for it, because the loop returns at the INTERVENTION guard (`book_evaluate_loop.py:37-38`) before any redelivery, `owner.resume_closes` returns `()` (`book_account_owner.py:1456-1457`), and `owner.advance_schedule` returns `()` under INTERVENTION (`:1963-1964`). On the base no halt is recorded, so the case fails on the halt assertion.

Under D-7 = B (ruled), cases 15 and 16 are the inverted forms (sent before the halt), case 14 is held, and case 17 pins the B residual.

Cases 14 and 15 assert their premise with the owner's own test (`book_protection_owner.py:595`): the target row is `ever_protected`, its `observed` bracket after the dispatch-time read is not `None`, and `c1_rail.book_protection.is_loosening(observed, effective, side)` (`book_protection.py:140-149`) is True for case 14 and False for case 15. Cases 16 and 17 assert the target is not `ever_protected` and its `observed` is `None`; case 17 also asserts that no admitting evidence has arrived (`:583-586`). `is_loosening` alone cannot classify an attach: against `None` it compares with an empty `Bracket()`, so an attach that carries a limit reads as loosening (`:142-143`). The cases may import `waiting_runtime` (`test_book_runtime_occurrences.py:40`) and `ProtectionScenario.establish` (`book_protection_fixtures.py:73`); they edit no existing test or fixture.

Cases 7, 8 and 11 moved to the guard group below (G1-G3); the numbers are not reused.

**Guard cases** (`test_book_loop_source_health.py`; green on the base by design, so they are not fail-first). Each is shown red against a scratch over-halting mutant, as §3 says:
- G1 (was 7). The same states with `now` outside the bound session do not halt. *Mutant:* the health check ignores the session bounds.
- G2 (was 8). A connected source with no bar at `session.opens_at` does not halt (its `healthy()` would be False). Silence is still fenced by `check_source_silence`, unchanged. *Mutant:* a source with no bar yet counts as unhealthy.
- G3 (was 11). The loop never calls `healthy()` (a spy raises if it is called). An AST read of `book_evaluate_loop.py` shows no import of `bar_source_contract` or `book_sources`, and `test_c1_signal_daemon_image_manifest.py` stays green. *Mutants:* `step` calls `healthy()`; `book_evaluate_loop.py` imports `bar_source_contract`. Each must turn G3 red on its own.
- G4 (new). In a step where one source is unhealthy in session, the pre-gate block still runs: spies on `owner.check_protection_deadlines` and `runtime.advance_schedule` each record one call, as `test_idle_loop_checks_protection_deadlines` does (`test_book_runtime_occurrences.py:27`). *Mutant:* the health check moved ahead of the pre-gate block.

**Preservation** (green before and after, unchanged): `test_bar_source_contract.py`, `test_four_leg_runtime.py`, `test_feed_omission_session_end.py`, `test_c1_signal_daemon_image_manifest.py`, `test_book_session_calendar.py`, `test_book_loop_continuation.py`, `test_book_protection_evidence.py`, `test_book_runtime_occurrences.py`, `test_book_ingress_validation.py`.

**Runs.** Run each through the launcher and cite `record.json`, `verification_exit_code` and `source_stable`:
- `python -I scripts/fp.py doctor`
- `python -I scripts/fp.py python -m pytest <the authority-block acceptance list>`, red on the base, then green on the build
- `python -I scripts/fp.py test-ops`
- `python -I scripts/fp.py check`
- `git diff --check`

Disclose any gate failure that already exists on the base; never describe it as a pass.

## 5. Forbidden

- Wiring: `daemon.py`, `build_loop`, the daemon CLI and `__main__.py`, any config constructor, and any HTTP endpoint.
- `deploy/**`, the Dockerfile, `.dockerignore`, `tests/ops/test_c1_signal_daemon_image_manifest.py` and every other image-manifest test or script.
- Listener health reports (R-N), `listener_client.py`, `c1_rail_http_server.py`, telemetry and any route code.
- `bar_source_contract.py`, `feed.py`, `book_runtime.py`, `ops/c1_rail/book_account_owner.py`, `book_protection_owner.py`, `book_halt.py`, and calendar code and data (`book_session_calendar.py`, `ops/calendars/**`). The D-7 = B owner-side edit is the owner card's.
- Provider code, credentials, transports beyond test fakes, any network call, and choosing a feed (O-4).
- `core/**`, `book_policy.py`, Pine sources, runtime ports, `PORT_MANIFEST.sha256`, `BOOK_SOURCES.sha256`, and any private value.
- The spec, the umbrella, ADRs, STATE and the ledger (coordinator-reserved).
- GLM. Opening a PR, merging, or pushing to `main`.

## 6. Return (status taxonomy)

Return DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. The coordinator's verdict is RESOLVED (every §4 item holds) or FALSIFIED (the named items fail and the card goes back to the executor). The return holds:
- branch, head SHA, base SHA, `git diff --stat` and the name list;
- Phase-0 findings (a)–(f);
- for each fail-first case, the fail-on-base and pass-on-build launcher record IDs; for each guard case, the green-on-base, red-on-mutant and green-on-build record IDs, plus each mutant's diff, shown and then reverted;
- preservation results, `test-ops`, `check` and `git diff --check`;
- concerns.

## 7. Stop conditions (return to the coordinator; do not work around)

- #619 is not merged, or it merged with a `state`/`refusal` vocabulary other than the one in §0 (finding (a)).
- Finding (b), (d) or (e) is yes.
- The owner card's build is not merged, or finding (f) differs.
- Any change outside §2.3 is needed, including any edit to an existing test.
- Two failed corrections of the same issue (AGENTS.md).
- **Operator review-round rule (2026-10-02):** after more than three review rounds that each return two or more P1/P2 findings, stop folding; the coordinator adjudicates a rewrite or a narrower scope.
- A second writer appears on the branch.

## 8. Out of scope and decision unlocked

**Out of scope:**
- `build_loop`, the CLI, the Dockerfile, the image manifest, listener health reports (R-N), and live and route wiring.
- Building 15-minute bars from finer bars (OPEN-1, #617).
- Ratifying the backoff cap.
- The Track A `:236` checkbox.
- The TB-I3 interlock and A12-STALE latch.
- The production feed (O-4).
- The owner-side health-aware admission and its waiting status (owner card, D-7 = B).
- The `max_step_duration` measurement behind the #637/#651 P4 inputs. That is integration work owned by the TB-I3-HOST card (#651). §2.2 reorders work inside `step`; this card neither measures nor bounds its duration.

**Unlocked:** with this slice RESOLVED and the Codex relay clean, R-A2's offline (mock) tag is met in source. The coordinator records that at the spec and umbrella owners. The live (source) tag still waits on O-4, TB-I5 and the live packet that wires `book_sources` into the daemon and its image.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; 0 violations.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-ra2-offline-four-sources-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-ra2-offline-four-sources-card-DRAFT.md
# Premise (Git Bash), in the executor worktree.
gh pr view 619 --json state -q .state                                   # expected: MERGED
git rev-parse HEAD; test ! -e .env && echo "no .env" || echo "FAIL: .env present"
grep -n '"REFUSED"\|"DISCONNECTED"\|"CONNECTED"' ops/c1_signal_daemon/bar_source_contract.py   # finding (a)
grep -n "^LEG_FEEDS" ops/c1_signal_daemon/bar_source_contract.py         # finding (b)
grep -rn "refusal_reason=.awaiting_evidence" ops/                      # finding (e): only book_protection_owner.py:584, :586
grep -n "sources_healthy" ops/c1_rail/book_protection_owner.py ops/c1_rail/book_account_owner.py   # finding (f)
grep -n "import" ops/c1_signal_daemon/book_evaluate_loop.py              # after build: no bar_source_contract / book_sources
# Scope at return.
git diff --stat "$BASE"...HEAD
git diff --name-only "$BASE"...HEAD | grep -v -e '^ops/c1_signal_daemon/book_sources.py$' \
  -e '^ops/c1_signal_daemon/book_evaluate_loop.py$' -e '^tests/ops/test_book_sources.py$' \
  -e '^tests/ops/test_book_loop_source_health.py$' && echo "FAIL: scope"
```

## 12. Open decisions (coordinator (3) at freeze; D-7 ruled by Joshua)

- **D-1 Immediate halt on in-session `DISCONNECTED`. RULED (coordinator (3)): keep the immediate halt.** This is the strict reading of the frozen spec §7, which the operator confirmed. One failed connect or transport error inside the session halts the book, so #619's capped-backoff reconnect can never recover a source in session. **Cost, stated explicitly:** #619's routine renewal path (`_maintain` → `renewal_failed`) sets `DISCONNECTED`. So any lease or renewal blip inside the session becomes a session-ending `feed` halt that needs an attended resume. The rejected alternative was a grace window bounded by M5 (`BAR_SLACK`). It would need #619 to expose when the source disconnected, which is a contract change outside this card. A reconnect still serves the next session.
- **D-2 Incident-id uniqueness. RULED (coordinator (3)): mandatory.** The id is unique per occurrence: `source-unhealthy:<session_id>:<leg>:<detail>:<now.isoformat()>`, following `feed-silence:<session_id>:<anchor>` (`:1064`). Without it, the id repeats in every later session and after any attended resume in the same session. `halt` then raises "conflicting incident identity" (`:1321-1322`) before `_halt_db`. `step` would raise on every poll, authority would stay NORMAL, no `feed` incident would be recorded, and the book would resume silently when the source reconnected. A daemon exit on the uncaught exception would also clear the in-memory REFUSED latch on restart. Cases 12 and 13 are unconditional.
- **D-3 Spec owner file. RULED (coordinator (3)):** the spec names `daemon.py` for R-A2, and this slice uses a new module plus the loop. The spec R-A2 owner-file annotation is coordinator (3)-reserved. It lands in coordinator (3)'s ledger batch after coordinator (2)'s rail-spec entries (conflict C3). The executor never edits the spec (§5).
- **D-4 Duck-typed health read.** The loop reads `state` without a type check. That keeps the existing fakes valid and the contract module out of the image. The alternative, an `isinstance` check against `ContractBarSource`, would pull the contract into the daemon closure. **Recommended: duck-typed, as frozen.**
- **D-5 Tripwire breadth. RULED (coordinator (3)): keep.** Case 4 reads every calendar named in `RATIFIED.json` and checks product opens as well as closes, because the runtime seeds only from `session.opens_at` (`book_runtime.py`, the first-bar check after `:349`). The composition's transport-reuse refusal (case 2) is also kept.
- **D-6 Freeze base.** **Recommended:** `main` immediately after #619 merges. Earlier bases fail Phase 0 (a).
- **D-7 Prepared continuations under an unhealthy source. RULED B (Joshua, direct to coordinator (3), 2026-10-03 ~19:34Z): "go with your recommendation and proceed",** replying to coordinator (3)'s recommendation of B.
  - **B.** In an unhealthy in-session step, the loop redelivers through the owner's health-aware admission (`sources_healthy=False`) before the `feed` halt. The owner sends first-time attaches and tightenings with fresh evidence and holds each loosening as waiting, not terminal, so its barrier stays incomplete (§2.2; cases 14-17). The loop cannot sort the set itself (§2.2).
  - **Owner card.** B needs a source-health input at the owner's loosening admission (`book_protection_owner.py:484-495`). That file is bound qualification code (`ops/c1_rail/qualification/trust_domain.py:162`), so the edit has its own owner card (branch `claude/protection-health-admission-card`). Joshua's C3-rule admission of that edit is a dispatch gate on the owner card, **PENDING Joshua**. This card's build waits for the owner card's build to merge (P-row); §5 still forbids `book_protection_owner.py`.
  - **B residual.** An attach whose protection evidence has not arrived by the unhealthy step still returns `awaiting_evidence` (`book_protection_owner.py:583-586`) and is held and fenced: after the `feed` halt the owner stops the scheduled flatten, close resumption and every send until an attended resume (`book_account_owner.py:1963-1964`, `:1456-1457`, `:1743-1744`). That fill has no stop until then (case 17). B narrows the unprotected-fill exposure; it does not close it. D-1 already accepts the fence for positions that are already protected.
  - **Rejected A** (hold everything, loop-only): a new fill whose first stop was waiting stays unprotected until an attended resume, even when its evidence has arrived.
  - **No feed-silence precedent.** Redelivery is valid only while `now <= B + 15m30s` (`book_runtime.py:439-440`). A feed-silence halt needs `now > anchor + 30m30s`, with `anchor >= B` once `B` has a barrier (`book_account_owner.py:1059-1063`). The two never co-occur, so no feed-silence halt lands on a wait that can still be redelivered. The health halt is the first `feed` halt that routinely does, and with D-1 any renewal blip triggers it.

## Pre-mortem (README rule)

- **Loop cost:** one Windows build loop with launcher records. No Docker, no Linux run, no host.
- **Decisions the executor will hit:** D-1, D-2 and D-7 (B), all ruled (§12). Dispatch waits for the owner card's build to merge.
- **What makes it moot:**
  - #619 is withdrawn or reworked with a different state vocabulary;
  - an operator ruling moves source health to the listener (R-N) instead of the loop;
  - the attempt ends before a live source matters.
- **Measurements the return fills in:** Phase-0 findings (a)–(f), and the red and green record IDs for each case.
