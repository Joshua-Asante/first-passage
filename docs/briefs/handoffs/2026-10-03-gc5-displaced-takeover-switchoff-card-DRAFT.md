# GC-5-DISPLACED: Aegis takeover switch-off for the first release (replay RC-5 and rail R-E/S10)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-03. Drafted by a coordinator (3) worker for coordinator (3) to freeze; not dispatched. The coordinator answers §11's open decisions, commits the frozen revision under the committed-handoff rule and records its SHA before any worker starts.

**Authority (ruling, not this card):** operator ruling 2026-10-02 (sitting 1), [B–D packet GC-5 addendum](../../notes/2026-09-26-tradeify-bd-decision-packet.md) (`:131`): the first release runs **without the Aegis takeover** (fail-closed default); it replaces B-11's "Keep as declared" for the first release. Operator ruling 2026-10-02 (sitting 2), GC-5-DISPLACED (Joshua, "all recommended", 2026-10-03T01:42Z; sitting-2 recording plan §1.23 and §3, held privately under `local_artifacts/sitting2-2026-10-03/`): an Aegis entry that does not fit under the 80-micro cap is refused at admission as `capacity_refused` (refuse-never-clip) and is **not queued**. The handoff to coordinator (3) reads: "RC-5 replay_kernel takeover switch-off with updated takeover tests (e.g. protected_striker_ceiling_77_forces_takeover); rail R-E/S10 switch-off with a dated rail-spec §5 entry."

**Executor:** one Claude Code worker (not GLM; §0.5). Single writer of `claude/gc5-takeover-switchoff` (proposed), cut from the base the coordinator names at freeze (D1).

**Coordinator:** coordinator (3). It owns the freeze, the diff review, the rail-spec §5 entry (§2.4; `governance.author` is not granted to the worker), the PR, the Codex relay and the ledger.

**Owners this card narrows (it changes none of them):**
- Replay contract: [synchronized replay spec RC-5](../../spec/2026-09-12-tradeify-synchronized-replay-spec.md) (`:32`) and its case table (`:73-75`, `:90`).
- Rail contract: [rail extension spec](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) S10 (`:89`), R-E (`:153`), §5 (`:184-194`) and its Boundary line (`:212`: "no B1 field change or fail-closed change without the §5 addendum").
- Capacity law: [TB-S1 capacity spec](../../spec/2026-09-12-tradeify-book-protection-capacity-spec.md) `:93`, `:95` (O-6 consequences).
- Umbrella D-B8 priority and the TB-I3 build: [Track B umbrella](2026-09-10-track-b-qualify-accepted-book-umbrella.md).
- [Campaign §59 Ruling 3](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-3--adopt-route-native-expressions-for-orb-mnq-and-striker-mym-go-with-the-easier-fix) (`:3928`: the book keeps its "capacity rule and takeover ordering"). The GC-5 ruling overrides only the takeover, only for the first release; the D-B8 admission order (Aegis → Striker → Vanguard → ORB at the barrier) is unchanged.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - no_linux_or_ci_dispatch
  - card_section2_files_only
  - no_spec_or_governance_edit
  - no_takeover_code_deletion
  - no_runtime_config_or_env_switch
  - no_dd_protection_or_policy_value_change
  - no_qualification_or_e1_run
  - no_private_bytes_committed
  - no_glm_dispatch
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_aegis_takeover_switch.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/test_book_policy.py
  - tests/ops/test_book_capacity.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_book_takeover_phases.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_seal.py
```

`tests/ops/test_aegis_takeover_switch.py` is new (§3). Every other acceptance file exists on `origin/main@1a350ec`.

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

1. **Premise.** HEAD is the frozen base (D1). As of `origin/main@1a350ec` (2026-10-03) the takeover is live in both decision points below, and none of the sitting-2 GC-5 markers is on main: rail spec R-E `:153` carries no 2026-10-02 marker, and replay RC-5 `:32` carries none. Coordinator (2)'s batch writes them (§9). No `.env` in the worktree.
2. **Rule-0 reads** (read them; do not infer them). There are **two independent takeover decision points**, and the ruling binds both:
   - **Offline / replay.** `ops/c1_rail/book_policy.py:598-639`, `CapacityLedger.request`: when a priority-1 leg (Aegis) does not fit, it plans a whole-leg `TakeoverPlan` of lower-priority legs, lowest first (`:620-639`); every other leg is refused with event `capacity_refused` (`:612-616`). `Takeover` (`:506-568`) and `begin_takeover`/`settle_takeover` (`:641-688`) run it. The qualification `replay_kernel` (`ops/c1_rail/qualification/trust_domain.py:142` → `c1_rail.qualification.replay`) builds its own `CapacityLedger()` (`replay.py:151`) and executes the plan in `_admit` (`replay.py:423-447`: cancel, `_flatten(..., "capacity_takeover_close")`, `capacity_takeover_*` events).
   - **Rail / production owner.** `ops/c1_rail/book_capacity.py:163-196`, `_reserve`: for `aegis_6j` over the cap it sets `status="takeover"` and a sticky `blocks=("takeover:<op>",)` (`:180-193`). `book_account_owner.py:1810-1823` records `takeover_pending`, publishes the takeover (`_publish_takeover_db`) and returns `refusal_reason="takeover_pending"`; every other over-cap request returns `"insufficient_observed_capacity"`. Continuation lives in `book_takeover_owner.py` and `c1_signal_daemon/book_runtime.py:297`, `:321-326`, `:413-414`. Persisted takeover state is part of the migration schema (`tests/fixtures/book_migration/{1,2,3}-pending_takeover.json`, `*-completed_takeover.json`).
   - **Existing pinned behaviour (the red-first evidence).** `tests/ops/qualification/test_replay.py:476` `test_protected_striker_77_displaced_by_protected_aegis_30` (Striker 22+55=77 flattened, Aegis 3 admitted, `capacity_takeover_admitted`) is the code name of the spec's `protected_striker_ceiling_77_forces_takeover` (replay spec `:75`). Also `test_replay.py:347`, `:498`; `test_book_policy.py:182`, `:203`; `test_book_capacity.py:110-145`; `test_book_account_owner.py:363`; `test_book_takeover_phases.py` (75 takeover references). The rail spec's R-E test names (`test_seq_s10_takeover_each_failure_class_refuses`, `test_protected_striker_77_takeover_path`) do **not** exist in `tests/` at `1a350ec`.
   - **Baseline run (drafter, worktree at `1a350ec`):** `python -I scripts/fp.py python -m pytest -q tests/ops/qualification/test_replay.py tests/ops/test_book_policy.py tests/ops/test_book_capacity.py -k "takeover or 77 or aegis"` gave 24 passed, 152 deselected (record `.cache/fp-verification/20261003T030240Z-be683b27ae82/record.json`: `status` completed, `verification_exit_code` 0, `source_stable` true). The takeover tests pass today, so the takeover fires at the base.
   - **Freeze inventory.** `book_policy.py` and `replay.py` are both in the Stage 1c 68-module measured closure (closure table `docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt`, run by this drafter at `origin/main@1a350ec`); `book_capacity`, `book_takeover` and `book_takeover_owner` are runtime dependencies in the qualification trust domain (`trust_domain.py:155-170`). This change is therefore an E1 freeze-inventory change (as replay spec `:7` says of H4) and moves the measured closure.
3. **Findings returned before any code (checkpoint; the coordinator acknowledges each):**
   - (a) every production call site of `CapacityLedger(...)`, `CapacityLedger.request`, `book_capacity.apply_event`/`_reserve`, and every path that reads `status == "takeover"` or `takeover_pending`, as `file:line`;
   - (b) the full list of existing tests that assert a takeover fires, split into "re-pinned to OFF" and "kept, explicitly enabled" (§3.2);
   - (c) what the owner does today on boot or migration with a persisted `takeover_pending` row, and what it would do under OFF (D5);
   - (d) whether any `capacity_refused` emission exists on the rail path today (the drafter found none: the rail refusal is `insufficient_observed_capacity`, `book_account_owner.py:1823`, `book_sizing_context.py:272`) (D4).

## 0.5. Routing and clarifying questions

**Not GLM.** This changes risk/capacity admission and takeover logic on the protected qualification and rail paths (AGENTS.md GLM rule: risk controls and production-incident-adjacent logic stay with Claude; `book_policy.py` also carries the policy interlock). Nothing here is sent to `glm_agent` or any external service. No Pine, port bodies, account data or private bytes are read or committed.

Unanswered §11 decisions that Phase 0 needs return `NEEDS_CONTEXT`; they are never assumed.

## 1. Goal

Make the first release's capacity behaviour match the GC-5 rulings in both decision points: an Aegis entry or add that does not fit under the 80-micro cap is **refused at admission** (`capacity_refused`, refuse-never-clip), **never queued**, and never displaces another leg. Retain the takeover machinery, tested, behind one canonical switch that defaults OFF, so a later release can re-enable it by a reviewed change. Within-cap admission, D-B8 barrier order, reservations, protection policy and quantity laws are unchanged.

## 2. Scope

### 2.1 Mechanism (recommendation: a code-level configuration switch defaulting OFF; not deletion; not a runtime config field)

- **One canonical switch** in `ops/c1_rail/book_policy.py` beside `ACCOUNT_MICRO_CAP`: an enum (proposed `AegisTakeover.OFF | AegisTakeover.WHOLE_LEG_PRIORITY`) and the constant `AEGIS_TAKEOVER: AegisTakeover = AegisTakeover.OFF`, with a dated comment citing both GC-5 rulings. Use an enum, not a bare string, so the frozen-module value compares by value (lesson: frozen-module globals need value-comparable types). An import-time validator, in the `_validate_protection_rule` pattern, refuses any other type.
- **Consumers reference it, never copy it.** `CapacityLedger.request` and `book_capacity._reserve` read the switch through an explicit keyword (`takeover=` on `CapacityLedger`, a reducer parameter or `CapacityState` field for `book_capacity`; D3) whose default **is** the canonical constant. Under `OFF`, a priority-1 over-cap request takes the same refusal branch as every other leg: no `TakeoverPlan`, no `Takeover`, no `blocks`, no displaced cancel or close. Replay emits `capacity_refused`; rail emission per D4.
- **No production caller passes the keyword.** A test (§3.1 case 6) walks the AST of `ops/` and fails if any non-test module passes it. Only tests that exercise the retained machinery pass `WHOLE_LEG_PRIORITY` explicitly.
- **Why this shape (AGENTS.md "Configuration as code"):** the rule is defined once in a canonical source; consumers reference it; it is validated at its consumption boundary; and because `book_policy.py` is in the trust-domain inventory and the measured closure, the resolved value's identity is bound by the same digests that validation and activation use.
- **Why not a runtime/deploy config field or env var:** an edit to `/data` config would re-enable an unqualified behaviour without code review or requalification. AGENTS.md already records this bypass for M1 (the rail boot gate does not check M1, "so editing the `/data` config bypasses it"). The switch is code, so changing it is a reviewed, requalified change.
- **Why not code removal:** removal deletes tested machinery the later re-enable needs (`book_takeover.py`, `book_takeover_owner.py`, the replay branch). It also cascades into the persisted-state/migration schema (takeover fixtures) and roughly fifteen test files, and it makes re-enable a rebuild rather than a reviewed switch. Removal also exceeds the ruling, which decides the first release only.

### 2.2 Replay (RC-5, `replay_kernel`)

- `replay.py`'s `CapacityLedger()` takes the default (OFF). The `_admit` takeover block (`:423-447`) stays and is reachable only with the switch enabled. A refused Aegis intent goes through the existing `_reject(intent, bar, decision.reason)`. It is not stored, retried or re-admitted on a later bar without a fresh adapter intent (not queued; RC-9's duplicate key is unchanged).

### 2.3 Rail (R-E / S10)

- `book_capacity._reserve` under OFF returns `status="refused"` for an over-cap Aegis request, with no `Takeover` and no `blocks`. `book_account_owner` records a `refused` operation, sends nothing for any displaced leg, and returns the refusal (D4 names the reason/telemetry surface). The continuation paths (`book_takeover_owner`, `book_runtime` `takeover_pending` handling) stay, unreachable from new admissions under OFF.
- Persisted takeover state under OFF follows D5 (recommended: fail closed at boot/migration with a named refusal, since the first release starts from a TB-V1-seeded flat account).

### 2.4 Rail-spec §5 entry (coordinator-written, not the worker's)

The S10/R-E switch-off is a **fail-closed change** (more refusals, no displacement), so the Boundary line (`:212`) requires a dated §5 entry. Coordinator (3) writes it **only after coordinator (2)'s sitting-2 batch PR merges** (it lands the R-E `:153` marker and the A12-STALE §5 entry, sitting-2 plan §1.9 and §7 C3). It inserts the entry after the A12-STALE 2026-10-02 entry, before the code PR merges. Proposed text:

> **§5 addendum entry 2026-10-02 (operator rulings 2026-10-02, sittings 1 and 2, GC-5-DISPLACED): Aegis takeover off for the first release.** For the first release, S10 and the takeover branch of R-E are off. An Aegis entry or add that does not fit under the 80-micro cap is refused at admission (`capacity_refused`, refuse-never-clip). It is never queued and never displaces another leg. This makes the contract more fail-closed. No B1 field, quantity law, reservation rule or D-B8 admission order changes. Implementation: one canonical switch in `book_policy.py`, defaulting OFF, consumed by `CapacityLedger` and `book_capacity` (card `docs/briefs/handoffs/2026-10-03-gc5-displaced-takeover-switchoff-card-DRAFT.md`). Re-enabling needs its own operator ruling and a new §5 entry. Armed commissioning and later releases are not decided here.

If #605 merges first, its RS-S5 entry precedes this one, and this entry is appended after it. #605's `:324` "Not changed" list must then name this entry too (D6).

### 2.5 Files

**Allowed:**
- Edit: `ops/c1_rail/book_policy.py` (switch, validator, `CapacityLedger.request` branch), `ops/c1_rail/book_capacity.py` (`_reserve` branch and switch plumbing), `ops/c1_rail/book_account_owner.py` (refusal surface only, per D4/D5), `ops/c1_rail/qualification/replay.py` (only if the default cannot reach it through `CapacityLedger()`; return first).
- New: `tests/ops/test_aegis_takeover_switch.py`.
- Extend in place, never replace: the acceptance test files in the authority block, plus `tests/ops/test_book_review_followups.py`, `test_pr409_owner_lifecycle.py`, `test_pr409_review3.py`, `test_feed_omission_session_end.py`, `test_book_fence_classification.py`, `test_book_bootstrap_migration.py`, `test_book_runtime_occurrences.py`, `test_attended_incident_rehearsal.py` and `tests/sequence_verification/book_event_sequences.py`. These changes are limited to passing the explicit enable where a test exercises the retained machinery (finding (b)).

**Forbidden:** every `docs/` file (specs, packets, campaign record, checklist, ledger: the coordinator and coordinator (2) own them); `book_takeover.py`, `book_takeover_owner.py`, `c1_signal_daemon/book_runtime.py` (except D5's boot refusal, if the coordinator places it there); `tests/fixtures/book_migration/*` and `manifests.json`; `tests/ops/tb_s3_kernel/*` (historical model evidence); `core/dd_protection.py`, `POLICY_REGISTRY`, `policy_fingerprint.py`; any Pine, port or private file; `.claude/settings.json`.

## 3. Method (red first)

### 3.1 New red→green cases (`tests/ops/test_aegis_takeover_switch.py`; each must fail at the base and pass at the build)

1. **Replay, protected 77 vs 30, default switch:** the `test_replay.py:476` scenario (Striker 22+55 protected, Aegis 30 protected) without any override → Aegis rejected with the capacity reason; event `capacity_refused`; no `capacity_takeover_*` event; Striker keeps 77; no flat with reason `capacity_takeover_close`. At the base, the takeover fires (the existing test proves it).
2. **Replay, not queued:** same start; on a later bar Striker exits by its own path. With no fresh Aegis intent, no Aegis order or fill appears. A fresh intent on that later bar is admitted normally.
3. **`CapacityLedger.request`, default:** an Aegis over-cap request returns `admitted=False`, `takeover is None`, event `capacity_refused`, and leaves the ledger with no pending takeover. A following request from any leg is not answered "takeover in progress".
4. **Rail reducer, default:** `book_capacity._reserve` for an over-cap `aegis_6j` → `status="refused"`, `takeover is None`, `blocks == ()`.
5. **Rail owner, default:** the `test_book_account_owner.py:363` scenario without override → the Aegis dispatch is refused; no `takeover_pending` row; the broker receives no `flat` for the displaced leg; displaced exposure is unchanged.
6. **No production enable:** an AST scan of `ops/**/*.py` finds no call passing the enable keyword, and `book_policy.AEGIS_TAKEOVER is AegisTakeover.OFF`. Red at the base because the switch does not exist; that is acceptable for this case only, and the return says so.
7. **Persisted takeover under OFF (per D5):** an owner booted on a `*-pending_takeover` fixture state refuses with the named reason and dispatches nothing.

### 3.2 Updated existing tests

- `test_replay.py:476` is renamed to the spec's name, `test_protected_striker_ceiling_77_forces_takeover`, and passes `WHOLE_LEG_PRIORITY` explicitly. Its assertions are unchanged: it now pins the retained machinery, not the first-release rule. Likewise `:347`, `:498`, `test_book_policy.py:182`, `:203`, `test_book_capacity.py:110-145`, `test_book_account_owner.py:363` and the `test_book_takeover_phases.py` scenarios.
- `test_replay.py:133` (Aegis within cap; others refused without clip) passes **unchanged and without override** (preservation).
- No assertion is weakened. A test whose outcome changes under OFF either moves to §3.1 (new expected outcome, with the ruling cited in its docstring) or is explicitly enabled; finding (b) lists which.

## 4. Acceptance checks (falsifier-first)

**H:** with the switch at its default, no admission path in the replay or the rail can plan, publish or execute an Aegis takeover; an over-cap Aegis request is refused like any other leg's and is not retried; and with the switch explicitly enabled, every pre-existing takeover test passes with its assertions unchanged. **Reject if** any §3.1 case cannot be made to fail at the base (case 6 excepted, as stated), fails at the build, or any pre-existing test outside finding (b)'s list changes outcome. **Revert trigger:** any within-cap admission, reservation, quantity or barrier-order outcome differs at the build head from the base.

Verification (launcher, from the worktree; cite each printed `record.json` with `status`, `verification_exit_code`, `source_stable`):
- `python -I scripts/fp.py doctor`
- `python -I scripts/fp.py python -m pytest <the authority-block acceptance files> <the §2.5 extended files>`. Include `test_seal.py` and `test_trust_domain.py`, because `book_policy.py` is a frozen, digest-bound module.
- Base run of the §3.1 file (red evidence) on a scratch copy at the base head, cited separately.
- `python -I scripts/fp.py check`; any pre-existing gate failure is disclosed, not called a pass.

## 5. Forbidden

- Deleting or disabling takeover code, tests or fixtures (§2.1).
- Any runtime, deploy, `/data` config or environment-variable switch for the takeover.
- Changing the cap, micro-equivalents, priority order, quantity laws, reservation rules, `DD_TRIGGER`/`DD_SCALE` or any policy value.
- Queuing, deferring or retrying a refused Aegis intent; clipping it to fit.
- Editing any spec, packet, campaign record, checklist or ledger (§2.4 is the coordinator's).
- Running any qualification, E1, S-stage or Linux/CI dispatch; sending anything to GLM.

## 6. Return (status taxonomy)

**Gate:** RESOLVED if every §4 check holds at the build head with cited records; FALSIFIED if the H's reject condition or revert trigger fires; AMBIGUOUS (returned as NEEDS_CONTEXT) if a §11 decision is needed to judge a case.

Return one of: **DONE** (all §4 checks green, record.json paths cited, base-red evidence cited); **DONE_WITH_CONCERNS** (green, with a named residual, e.g. a rail refusal surface that D4 left open); **NEEDS_CONTEXT** (a §11 decision or Phase-0 finding blocks progress); **BLOCKED** (a premise is false, e.g. the switch cannot reach a decision point without editing a forbidden file). Include the branch head SHA, `git diff --stat <base>...HEAD`, the finding (a)–(d) answers, and the Stage 1c closure table re-run (expected: `book_policy` and `replay` differ, nothing else outside the allowed list).

## 7. Stop conditions (return to the coordinator; do not work around)

- A third takeover decision point exists beyond the two in §0.
- Reaching OFF needs an edit to a forbidden file, or to `replay.py` beyond taking the default.
- A pre-existing non-takeover test changes outcome.
- Persisted takeover state can reach dispatch under OFF, and D5 does not cover the path.
- Coordinator (2)'s batch has not merged and the work would need the §5 entry or the R-E marker in place to be correct.

## 8. Out of scope, and what a later re-enable still needs

Out of scope: the GC-5 route trace and documentary sequence; C-a close realization; TB-I3's remaining scope (TB-I3-CARD, a separate card); ED-10-SPLIT; every doc marker (coordinator (2)'s batch); mirrors (§10 list).

**What a later re-enable needs** (each one is separate; none is authorized here):
1. A new operator ruling replacing the GC-5 first-release rule.
2. The GC-5 row's own evidence: a documentary sequence under the accepted close realization, then the operator-performed trace (B–D packet `:124`, B-11 `:157`).
3. A reviewed code change flipping `AEGIS_TAKEOVER` to `WHOLE_LEG_PRIORITY`, with the explicitly enabled tests moved back to default.
4. A new rail-spec §5 entry, removal of the R-E and RC-5 markers, and the S10 executable sequence tests the spec names (absent today).
5. Re-acceptance of the E1 freeze inventory and requalification. The replay's mode and capacity sequences change, so any first-release qualification evidence does not carry over.
6. Rail-side `capacity_takeover_*` telemetry and persisted-state migration checks re-verified against the then-current schema.

## 9. Sequencing

- **Rail-spec §5 entry:** after coordinator (2)'s sitting-2 batch merges (plan §7 C3: the main entry lands first; #605 then merges main, appends RS-S5 and amends `:324`). The code PR cites the entry and does not merge before it is on main.
- **`replay.py` single writer:** ED-10-SPLIT (coordinator (3)) also edits `replay.py` and is also a `replay_kernel` change accepted before E1. Run the two sequentially on one branch line, or accept them as one freeze-inventory change (D2).
- **Measured closure:** the change moves two of the 68 measured modules. Land it before coordinator (3)'s pre-S8 re-measure on the integrated candidate head (sitting-2 ENG-2), so that measure covers it.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: well-formed; exit 0.
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-gc5-displaced-takeover-switchoff-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-gc5-displaced-takeover-switchoff-card-DRAFT.md
# Premise: both decision points live; no GC-5 markers yet (run at the base).
grep -n "takeover=plan\|capacity_takeover_planned" ops/c1_rail/book_policy.py
grep -n 'request.leg_id == "aegis_6j"' ops/c1_rail/book_capacity.py
grep -n "Marker 2026-10-02" docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md docs/spec/2026-09-12-tradeify-synchronized-replay-spec.md
# Return: switch default and no production enable.
grep -rn "AEGIS_TAKEOVER\|AegisTakeover" ops/
git diff --stat "$BASE"...HEAD
```

Mirrors that still describe the takeover as live (coordinator (3) mirror sweep; not this card): TB-S1 capacity spec `:93`, `:95`, `:131`, `:144` (not in coordinator (2)'s batch list); halt/resume contract and `2026-09-16-pr409-bounded-execution-correction.md` takeover mentions; campaign §59 Ruling 3 `:3928` ("takeover ordering"); commissioning `:558` and drill plan `:480` ("GC-5 not planned", sitting-2 mirror sweep).

## 11. Open decisions (for the coordinator at freeze)

- **D1 Base.** `origin/main` after coordinator (2)'s batch merges (recommended), or `1a350ec` with the §5 entry following.
- **D2 Replay single writer.** GC-5 first, then ED-10-SPLIT rebased; or one combined `replay_kernel` acceptance.
- **D3 Rail plumbing.** A reducer keyword or a `CapacityState` field for `book_capacity`. A state field persists, so it needs a migration-schema decision. A keyword is recommended.
- **D4 Rail refusal surface.** The ruling names `capacity_refused`. The rail returns `insufficient_observed_capacity` for every leg and emits no `capacity_refused` telemetry. Options: keep the reason and add a `capacity_refused` telemetry event (R-E's telemetry list already names the kind); or rename the reason (this touches persisted rows and other legs). Recommended: add the event, keep the reason.
- **D5 Persisted takeover under OFF.** Fail closed at boot or migration with a named refusal (recommended), or keep the existing continuation for a pre-existing takeover. The first release starts flat (TB-V1 seed, sitting-2 ED-27).
- **D6 §5 ordering with #605.** Whether the GC-5 §5 entry precedes or follows RS-S5, and who amends `:324`.
- **D7 Mirrors.** Whether TB-S1 capacity spec `:93`/`:95` and §59 Ruling 3 get dated markers in coordinator (3)'s mirror batch, since coordinator (2)'s batch does not list them.
