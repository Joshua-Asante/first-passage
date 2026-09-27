# H5(b) — Attended operations: synthetic incident rehearsal — worker card

**Status:** PREPARED 2026-09-27 by [handoff H5 step (a)](2026-09-27-staged-acceptance-handoffs.md#h5--attended-operations-apply-the-resumption-ruling-then-synthetic-incident-rehearsal). **Not dispatched.** The card can be dispatched only after the coordinator accepts step (a):
- the dated 2026-09-27 amendment to the [halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md): its header callout, the §4 marker and [§4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal);
- the dated pointer in the [Phase 5 plan](../../superpowers/plans/2026-09-16-phase5-attended-operations.md);
- this card, including the coordinator's answer to §7's known-path decision.

At dispatch the coordinator records the dispatch revision in §10 and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*).

**Parent:** [staged acceptance handoff set, card H5](2026-09-27-staged-acceptance-handoffs.md#h5--attended-operations-apply-the-resumption-ruling-then-synthetic-incident-rehearsal). The parent file carries no authority block, so it bounds nothing beyond this card's own seat checks.

**Authority:** [incident ADR §A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27) (operator ruling 2026-09-27). In its words: "during commissioning and the first attended release, an incident ends automated trading for that session. Continue operator recovery and evidence collection; review before another session." and "This applies to incidents—not ordinary, correctly handled signal or capacity refusals." H5 step (b) authorizes a synthetic rehearsal of that ruling against the existing owners. This card grants nothing its dispatcher lacks.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - tests_and_evidence_note_only
  - no_production_code_change
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_or_vendor_contact
  - no_external_send
  - no_paid_channel_without_operator
  - no_new_account_without_operator
  - disposable_state_only
  - no_private_source_read
  - no_lab_ops_import
  - no_ci_dispatch
  - no_owner_record_edit
acceptance:
  - tests/ops/test_attended_incident_rehearsal.py::test_lost_entry_response_blocks_risk_add_at_once
  - tests/ops/test_attended_incident_rehearsal.py::test_lost_entry_response_terminal_does_not_restart_automation_in_session  # under §7 option (B) an XFAIL here is NOT acceptance of §A11.2 behavior; (b) acceptance is then partial
  - tests/ops/test_attended_incident_rehearsal.py::test_stale_broker_fact_halts_and_blocks_same_session_activation
  - tests/ops/test_attended_incident_rehearsal.py::test_feed_silence_halt_survives_feed_recovery_in_session
  - tests/ops/test_attended_incident_rehearsal.py::test_missed_acknowledgment_never_changes_halt_or_permission
  - tests/ops/test_attended_incident_rehearsal.py::test_restart_during_incident_halt_boots_halted_with_new_generation
  - tests/ops/test_attended_incident_rehearsal.py::test_activation_refused_after_incident_and_restart_in_same_session
  - tests/ops/test_attended_incident_rehearsal.py::test_ambiguous_protection_halts_into_intervention_and_fences_mutations
  - tests/ops/test_attended_incident_rehearsal.py::test_activation_refused_after_protection_incident_in_same_session
  - tests/ops/test_attended_incident_rehearsal.py::test_operator_halt_leaves_no_same_session_activation_path
  - tests/ops/test_attended_incident_rehearsal.py::test_only_bootstrap_activation_writes_running_permission
  - tests/ops/test_attended_incident_rehearsal.py::test_capacity_refusal_leaves_session_running
  - tests/ops/test_attended_incident_rehearsal.py::test_zero_size_sizing_refusal_leaves_session_running
  - tests/ops/test_attended_incident_rehearsal.py::test_duplicate_signal_refusal_leaves_session_running
  - tests/ops/test_attended_incident_rehearsal.py::test_incomplete_barrier_before_expiry_leaves_session_running
```

## 0. Read first (report before any test code; otherwise `NEEDS_CONTEXT`)

Read these in full:
- `AGENTS.md`;
- the halt/resume contract §1–§4.1 and §7, as amended 2026-09-27;
- incident ADR §A11, §A11.1 and §A11.2;
- the Phase 5 plan: Global Constraints, the design table, and WP1, WP2 and WP4 acceptance.

Then confirm these anchors at the dispatch revision. They were read at `521d8f2`. This table is their home: the contract's §4.1 implementation-status record points here rather than carrying them.

| Anchor | What it is |
|---|---|
| `ops/c1_rail/book_account_owner.py:1112-1124` | `halt(...)` and its reason set |
| `:1868-1882` | `_halt_db`; an incident marks the bootstrap ineligible at `:1876` |
| `:383-389` | Restart: the bootstrap invalidated, a new boot ID and generation, HALTED/INTERVENTION |
| `:768-798` | `_ordinary_unknown_orders_db`; fence clearing at `:795` |
| `:1605-1612` | Risk-add admission: `risk_add_not_authorized`, `unknown_order`, `close_unreconciled` |
| `:1918-1921` | Stale broker fact halts (`stale-fact`) |
| `:855-866` | Feed-silence halt |
| `ops/c1_rail/book_bootstrap.py:106-175` | The one-use activation: history refusal `:136-141`; RUNNING written at `:174` |
| `ops/c1_rail/book_protection_owner.py:175` | Protection halt |
| `ops/c1_rail/book_halt.py:1-5` | Halt-only; RUNNING rejected |
| `ops/c1_rail/c1_rail_telemetry.py:157-224` | `OperatorNotifier`, `FileAckNotifier`, including `is_acknowledged` at `:223-224` |

Also read the [#519](https://github.com/Joshua-Asante/first-passage/pull/519) trace at its pinned head: `git show 8c15f18:docs/notes/2026-09-26-account-fence-four-state-trace.md`, rows `:12`, `:64`, `:104`. It already establishes:
- an ordinary unknown outcome is fenced but not halted (CC-3);
- no resume path exists.

Reuse those findings. Do not redo that trace.

**The report must state:**
- the dispatch revision;
- whether each anchor still matches;
- the fixtures you will reuse (for example `tests/ops/book_bootstrap_fixtures.py`, UNVERIFIED as suitable);
- whether any owner in `ops/` emits an incident notification or escalates. At `521d8f2` a grep for `notif|alert|escalat` in `book_account_owner.py`, `book_halt.py` and `book_protection_owner.py` found nothing. That grep is not exhaustive.

A mismatch is a stop (§7).

## 1. Scope

**In scope:** synthetic tests and one evidence note against the **existing** owners. The tests show three things:
- after each scripted incident, no path restarts automation within the session;
- a correctly handled refusal leaves the session running;
- the notification components behave as far as they exist, and where they do not exist, the note says so.

**Files you may change:**
- `tests/ops/test_attended_incident_rehearsal.py` (new);
- a new fixture module under `tests/ops/`, only if an existing fixture cannot be reused;
- `docs/notes/<date>-h5b-attended-incident-rehearsal.md` (the evidence note).

**Anything else is a stop (§7).** That includes every file under `ops/`, `core/`, `tools/` and `.github/`, and every existing test.

**Reuse, do not duplicate:**
- `tests/ops/test_book_halt.py::test_running_injected_into_database_never_grants_permission`;
- `tests/ops/test_book_bootstrap_migration.py::test_empty_history_cannot_rearm`, `::test_running_activation_is_noop_after_activity`, `::test_halt_wins_serialized_race_with_fresh_activation`;
- `tests/ops/test_c1_rail_telemetry.py::test_file_ack_notifier_notify_and_acknowledge`;
- H4's pending `test_refreshed_evidence_never_restores_permission_after_incident_halt` and `test_stale_evidence_blocks_admission_loosening_and_takeover` ([H4 card](2026-09-27-h4-fence-classification-orb-l1-repair.md)).

Cite these in the evidence note. Do not copy them.

## 2. The synthetic incident script

The class of each case comes from halt/resume §4.1, cited by §2 row. Each case runs in a disposable store (`tmp_path`) with a synthetic account, session and clock. Account identifiers, figures and credentials are synthetic.

| # | Scripted incident | §2 row / §4.1 class | Must show |
|---|---|---|---|
| S1 | **Lost response:** an entry dispatch whose outcome is unknown | `:26` uncertain outcome: **incident** | Risk-adds are blocked at once. After an accepted, postdating terminal, automation **does not** resume in the same session. See §7's known path. |
| S2 | **Stale evidence:** (a) a broker fact older than `MAX_FACT_AGE`; (b) feed silence past the preserved timeout, followed by fresh bars | (a) `:26` loss of required evidence; (b) `:28` via `:27`: **incidents** | Each halts into INTERVENTION. Fresh bars or facts afterwards do not restore permission or allow activation in that session (§3). Stale **order-level** evidence (Ruling 7(b)) is OPEN O-1: it is H4's, and this card asserts nothing about whether it ends the session. |
| S3 | **Missed alert:** an incident with no acknowledgment, then a late acknowledgment | Attendance (§3) | Neither a missed nor a late acknowledgment changes the halt, generation or permission. See §3 below for the timing measurement. |
| S4 | **Restart during halt:** a process restart while an incident halt is held | `:33` restart **after** an incident (settled) | Boots HALTED with a new boot ID and generation. Incident rows are retained. The bootstrap stays ineligible, so no activation is possible in that session. |
| S5 | **Ambiguous protection:** a protection fact whose identity, quantity or ownership is uncertain | `:26` protection fault: **incident** | Halts into INTERVENTION. Every runtime mutation is fenced, including tightening and attach. No activation in that session. |
| S6 | **Operator stop** | `:26` operator stop: **Incident** (O-6 decided 2026-09-27) | Assert that after an operator halt no activation path exists in that session (as S4, without the restart). By the operator's 2026-09-27 clarification (O-6), this is the §A11.2 incident behavior. |
| S7 | **Correctly handled refusals:** capacity; zero-size sizing; recognized duplicate; stale individual signal; an incomplete barrier before expiry | `:35` and `:30` before expiry: **not incidents** | Only that request is refused. Permission stays RUNNING/NORMAL, the generation is unchanged, and no incident row is written. The next valid request in the same session is admitted. |

**No permission transition to RUNNING other than bootstrap (structural).** The test `test_only_bootstrap_activation_writes_running_permission` scans `ops/c1_rail/*.py` for every `INSERT INTO owner_state` and `UPDATE owner_state` statement and every write of `authority='NORMAL'`, whether the value is a literal or a bound parameter (`permission=?`, `authority=?`). It asserts that the only statement setting RUNNING or NORMAL is `book_bootstrap.py`'s activation. At `521d8f2` the statements are `book_account_owner.py:334` (INSERT, HALTED), `:388`, `:680`, `:1748`, `:1873`, `book_bootstrap.py:174` and `book_migration.py:412`. A second RUNNING or NORMAL site, or a parameterized one whose value the scan cannot resolve, is a stop (§7), not a test update. The scan covers permission transitions only. An admission-level restart, where permission stays RUNNING and nothing is written, is covered by S1 and S7, not by the scan.

**OPEN cases are not rehearsed as decided.** O-1 to O-5 in §4.1 are not asserted either way (O-6 was decided on 2026-09-27 and S6 asserts it):
- O-1: stale order-level evidence;
- O-2: daemon-side suppression;
- O-3: early authorization expiry;
- O-4: a restart with no prior incident;
- O-5: operator platform action without a stop;
- O-6: **decided 2026-09-27** (an incident). S6 asserts it, and it is no longer an open item.

A case that needs one of them decided is a stop.

## 3. Notification delivery and 60 s escalation

The rule being measured:
- the contract (halt/resume §3, *Attendance and notification*) targets acknowledgment within 60 s;
- if there is no acknowledgment 60 s after the first notification attempt, the owner escalates through an alternate configured channel;
- a delivery failure goes to the remaining channels immediately.

The Phase 5 plan's Global Constraints preserve the same rule.

For each item, measure what exists and record what does not:
- **Incident → notification:** does any owner emit a notification when it halts? (§0 grep: none found at `521d8f2`.) If none does, record **ABSENT**, owner Phase 5 WP2 / T13. Do not build it.
- **Alert write → acknowledgment:** for `FileAckNotifier`, record the local timing on a synthetic clock. This is **local consumer behavior only** (Phase 5 WP2: "mocks prove only the local consumer behavior").
- **60 s escalation and immediate failure routing:** if no owner implements them, record **ABSENT**. A harness-level stand-in is not a measurement of the owner.
- **Independent missed-heartbeat monitor:** record whether one exists. The daemon's `heartbeat.py` is a `GET /` liveness snapshot, not an external monitor. The external monitor is unselected (halt/resume §3).

**The operator's channel.** By default the real-delivery leg is **OWED** to Phase 5 WP2 / T13, together with the real-delivery requirement (Phase 5 WP2 and completion). No owner sends an incident notification today (§0), and this card forbids building one, so the worker has nothing to send with. The worker sends nothing to any external channel (`no_external_send`); this card holds no capability for it. If the coordinator wants the leg now, it is an **operator-run step**: the operator sends and acknowledges on their own existing, no-spend channel, with messages labelled `SYNTHETIC REHEARSAL` and carrying no account content, and the worker records only the local synthetic-clock timestamps and the operator's reported times, labelled as operator-reported. Any agent-initiated send to an external channel needs an explicit operator approval recorded in §10 and a capability this card does not hold, so it is a return to the coordinator, not a leg of this card. Credentials stay outside the repository. **Any channel that needs spend, a new account or a new provider returns to the operator before use.**

## 4. Synthetic versus owed

| Established by this card (synthetic) | Owed elsewhere |
|---|---|
| Owner-level incident-versus-refusal behavior, restart-during-halt, structural absence of a RUNNING transition other than bootstrap, local notifier behavior | Real delivery and acknowledgment timing on the operator's qualified channels; alternate-channel escalation and the external heartbeat monitor (Phase 5 WP2, T13) |
| Traces in the [deployment-checklist addendum §2](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#2-evidence-classes-and-what-each-may-support) class *Synthetic / replay engineering* | H2 commissioning traces (`COMMISSIONING_OBSERVATION`), folded in before any session that could produce an unresolved request (parent card H5, *Decision unlocked*) |
| — | The ordinary-unknown halt (CC-3, TB-I3/T09); the durable resume/activation owner (TB-I3, Phase 5 WP4) |

A synthetic result never marks as resolved an obligation that needs a real producer.

## 5. Evidence retained

The evidence note contains:
- one row per §2 case, with its §2 row, its §4.1 class, the observed permission, authority, generation and incident rows before and after, and the verdict;
- the §3 measurements, with MEASURED, ABSENT or OWED for each;
- the structural scan's result;
- restart and restore traces;
- the `record.json` paths.

Rehearsal state lives in `tmp_path` stores and is discarded after its evidence is retained.

## 6. Verification commands

Run through your own checkout's launcher. Report the command, interpreter, revision, tree state and results. Cite each printed `record.json`, and check `status: completed`, exit 0 and `source_stable: true`.

- `python -I scripts/fp.py doctor`.
- `python -I scripts/fp.py python -m pytest tests/ops/test_attended_incident_rehearsal.py -q`.
- Related suites, unchanged:
  - `tests/ops/test_book_halt.py`;
  - `tests/ops/test_book_bootstrap_migration.py`;
  - `tests/ops/test_book_account_owner.py`;
  - `tests/ops/test_book_protection_evidence.py`;
  - `tests/ops/test_c1_rail_telemetry.py`;
  - `tests/ops/test_pr409_review4.py`.
- `python -I scripts/fp.py test-ops` and `python -I scripts/fp.py check` on the final tree. Disclose any pre-existing gate failure.

## 7. Stop conditions (return to the coordinator; do not work around)

- **Any path that restarts automation in the same session after an incident, or that ends a session on a correctly handled refusal.** That is a defect (parent card H5). Return the trace.
- **Known path, a decision for the coordinator at dispatch.** By code reading at `521d8f2` (the §0 anchors; halt/resume §4.1 implementation-status record), S1 is expected to reproduce the first stop condition: automated risk-add admission continues in the same session after a `:26` incident without any halt (the CC-3 gap).
  - no halt is raised for an ordinary unknown outcome (#519 trace `:12`, `:64`; CC-3);
  - risk-adds are refused while the outcome is unresolved, and the fence clears on an accepted, postdating terminal (`book_account_owner.py:795`);
  - risk-adds are then admitted again while permission is still RUNNING, with no operator action.

  The coordinator records one choice in §10:
  - **(A) default:** stop at the first reproduction and return the trace, as the parent card H5's stop condition requires;
  - **(B):** pin it with `pytest.mark.xfail(strict=True)`, with a reason naming CC-3 and §A11.2, and continue the other cases. Choosing (B) is a **recorded coordinator variance** from the parent H5 stop condition ("Stop and return; it is a defect"). Under (B) the S1 node's XFAIL is **not** acceptance of §A11.2 behavior: (b)'s acceptance is then partial, CC-3 stays an open defect (TB-I3/T09), and the evidence note says so.

  The repair is TB-I3/T09's either way. It is never this card's.
- A needed change outside §1's file list, including any file under `ops/`.
- A second write site of RUNNING permission, or any activation path other than the one-use bootstrap.
- A notification or acknowledgment path that can change permission or send a broker command (Phase 5 WP2 acceptance).
- A case that needs an OPEN item (O-1 to O-5) decided. O-6 was decided on 2026-09-27.
- A named acceptance node that cannot be expressed against an existing owner, for example no owner-level representation of a "stale individual signal" refusal. Return it; do not substitute a stand-in.
- A channel that needs spend, a new account or a new provider.
- An anchor mismatch at the §0 read.
- Two failed corrections of the same issue (AGENTS.md): stop and summarize.

## 8. Forbidden moves

- Any edit under `ops/`, `core/`, `tools/` or `.github/`; any repair of a found defect; adding a halt, resume or activation path.
- Any rail deploy or arm, any config write to a host, any account, broker, vendor or trading-service traffic, and any order. No agent places, amends or cancels an order.
- Real account identifiers, figures, P&L or credentials in any file, test or message.
- Deciding O-1 to O-5, or asserting a later-release policy (not ruled).
- Treating a mock or local file acknowledgment as delivery, or ABSENT as MEASURED.
- Editing the halt/resume contract, the incident ADR, the Phase 5 plan, the handoff set, STATE or the campaign record. Contradictions return to the coordinator.
- A merge or a push to `main`; CI dispatch.

## 9. Return boundary

- A `claude/*` (or `codex/*`/`glm/*`) branch and one PR, holding the §1 files only.
- The four-state status: `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`.
- Separate lists:
  - the §5 evidence;
  - the §4 synthetic-versus-owed table, filled in;
  - each defect found, with its owner;
  - the `record.json` paths.
- **The operator merges.** Acceptance is the coordinator's. It unlocks T13 construction (parent card H5), with H2's commissioning traces folded in before any session that could produce an unresolved request.
- **Recovery:** a branch revert. No shared state is touched.

## 10. Dispatch record

**Dispatched 2026-09-27 on the operator's instruction "dispatch H4 and H5b".**
- **Dispatch revision:** the commit that adds this record, on `claude/clever-wozniak-bx0u95` (PR #520). Read this card there with `git show <revision>:<path>`.
- **Executor:** a Claude Code worker subagent in its own git worktree.
- **Branch:** `claude/h5b-incident-rehearsal`, cut from `origin/main` (`5ad04cf`). The halt/resume amendment it rehearses is on PR #520 and is read at the dispatch revision.
- **Coordinator acceptance of step (a):** `54d6710`.
- **§7 known path: (B).** S1 (`test_lost_entry_response_terminal_does_not_restart_automation_in_session`) is pinned `pytest.mark.xfail(strict=True)`, with a reason naming CC-3 and §A11.2, and the other cases continue. **Variance from the parent H5 stop condition** ("Stop and return; it is a defect"): the defect is already established by code reading; the S1 XFAIL is not acceptance of §A11.2 behavior; (b)'s acceptance is partial; CC-3 stays an open defect (TB-I3/T09).
- **§3 real-delivery leg: OWED** (default) to T13 / Phase 5 WP2. No operator-run leg was requested, and there is never an agent send.
- **Pre-dispatch read:** `check_handoff_authority.py --all` clean at `54d6710`. §0 anchor re-verification is the worker's first act.

**Variance 2026-09-27 (coordinator, on the worker's §7 return).** The worker stopped on the node `test_stale_individual_signal_refusal_leaves_session_running`. No owner refuses a stale individual signal as a single request: the account owner never checks a signal's bar time; a late completed bar halts the book into INTERVENTION (`book_runtime.py:350-353`, pinned by `test_four_leg_runtime.py::test_stale_or_future_completed_bar_halts_before_dispatch`); and a wrong-bar intent is recorded as an input incident and halts (`book_runtime.py:208-217`).
- **Choice (i):** the node is removed from `acceptance`, and S7's stale-individual-signal sub-case is not rehearsed. The evidence note records the finding: "no owner implements the `:35` stale-individual-signal refusal; the nearest behavior halts." A strict xfail is not used, because there is no owner call to pin, and a stand-in is what §7 forbids.
- **Classification ruled 2026-09-27 by the operator:** "a late bar is a source incident; the halt is correct." It is recorded in the [halt/resume contract §4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal) (*Qualifications*). The finding is therefore not a defect. The evidence note records the ruling and cites the existing pinning test; the removed node stays removed.
- The other 15 nodes and the §7 (B) choice for S1 are unchanged.

**Not granted:**
- a rail deploy or arm, account traffic, an order or a session;
- a notification provider purchase or a new account;
- any agent-initiated message to an external channel or notification provider;
- CI dispatch, a merge, deployment or GO;
- any later-release policy;
- T13 acceptance.

## Verification of this card

- The authority block was checked at `521d8f2`, with the step (a) and concurrent working-tree edits present:
  - `python3 scripts/check_handoff_authority.py --all`: "2 card(s) with an authority block, 0 violation(s)", exit 0;
  - `python3 scripts/check_handoff_authority.py` on this file alone: 1 card, 0 violations, exit 0.
- Relative links and heading anchors in this card, the amended contract and the Phase 5 plan were resolved with a local script (GitHub-style slugs): 0 unresolved.
- **Anchors** were read at `521d8f2`:
  - `book_account_owner.py:383-389`, `:780-798`, `:855-866`, `:1105-1124`, `:1600-1612`, `:1868-1882`;
  - `book_bootstrap.py:100-175`, `book_halt.py:1-40`, `c1_rail_telemetry.py:150-222`;
  - `test_book_halt.py:60-72`, and the test list of `test_book_bootstrap_migration.py`.
- **Greps** were run at `521d8f2`:
  - `permission='RUNNING'` writes in `ops/c1_rail/*.py`: one, at `book_bootstrap.py:174`;
  - `owner_state` writes (`INSERT`/`UPDATE`) in `ops/c1_rail/*.py`: `book_account_owner.py:334`, `:388`, `:680`, `:1748`, `:1873`, `book_bootstrap.py:174`, `book_migration.py:412`; only `:174` sets RUNNING/NORMAL;
  - `notif|alert|escalat` in the three book owners: none;
  - `escalat` in `ops/**/*.py`: one unrelated hit, in `c1_rail_slippage.py:20` (unqualified over `ops/`, further hits are in Markdown/JSON only).
- **File check:** `tests/ops/test_attended_incident_rehearsal.py` does not exist at `521d8f2`, so every acceptance node is new.
- No test was run for this card. The S1 expectation in §7 comes from code reading and is UNVERIFIED until (b) runs it.

## Review and fix round (2026-09-27)

Each finding was re-checked against its cited source before it was applied. Files touched: the halt/resume contract and this card. The Phase 5 plan pointer needed no change.

- **F1 — applied.** Confirmed: `git diff --word-diff` showed `[-Scheduled cutoff/closure cannot be overridden.-]`, and the sentence was at `521d8f2` line 63. Restored verbatim; the §4 marker now follows it and says both preceding sentences are kept. Re-run: `git diff --word-diff` on the contract shows 0 `[-…-]` deletions, and `grep -c` on the sentence gives 1.
- **F2 — applied, reworded.** "Restart" overstated the trace. "Nothing stops" does not hold either: risk-adds are refused `unknown_order` while the outcome is unresolved (`book_account_owner.py:1608-1609`) and admitted again after the fence clears (`:795`). Both the contract record and §7 now say admission continues in the same session after a `:26` incident without any halt (the CC-3 gap).
- **F3 — applied.** `TEST_ONLY_SYNTHETIC` appears in no owner; the deployment-checklist addendum §2 names the class *Synthetic / replay engineering*. §4 now cites and links that class.
- **F4 — applied.** Confirmed: `grep -rn escalat ops/` has further hits in Markdown/JSON; `--include=*.py` gives one, at `c1_rail_slippage.py:20`. The scope is now qualified.
- **F5 — applied.** `is_acknowledged` is at `c1_rail_telemetry.py:223-224`. The anchor is now `:157-224`.
- **F6 — applied.** Confirmed: the paragraph directly after the plan's design table is the account-session paragraph. O-4 now names the table's first row and the paragraph beginning "Distinguish a planned, disarmed initial-activation boot".
- **F7 — applied.** Confirmed: `:28` and `:29` state no action. Both basis cells are now labelled *Reading, not row text*, with the strict-reading alternative (move to OPEN) left to the coordinator. The feed-silence halt is at `book_account_owner.py:865`.
- **H5a-R1 — applied.** Confirmed: the capabilities include no external send (`scripts/seat_authority.yml` capability list), no owner sends a notification, and the card forbids building one. §3 now makes the real-delivery leg OWED by default. It can be an operator-run step instead, where the worker records timestamps only. Any agent send is a return to the coordinator. The card adds the constraint `no_external_send`, updates §10 to match, and adds a Not-granted line.
- **H5a-R2 — applied.** Confirmed: §1 (`:16` at `521d8f2`) separates "an incident or manual takeover", and no line calls an operator stop an incident. §4.1 now splits the operator stop out of `:26` as **OPEN O-6**, with the coordinator as owner for operator decision. S6 asserts code behavior only; its node is renamed `test_operator_halt_leaves_no_same_session_activation_path`, and the O-lists read O-1 to O-6.
- **H5a-R3 — applied.** Confirmed: the parent H5 stop condition reads "Stop and return; it is a defect." Option (B) is now a recorded coordinator variance. Under (B), an XFAIL is not acceptance of §A11.2 behavior, acceptance is partial, and CC-3 stays open. The same qualifier is a YAML comment on the `:37` acceptance node.
- **H5a-R4 — applied.** The contract's implementation-status record now states the §2 `:26` gap and the §4 and §A11.2 consequence. It cites the #519 trace (`:12`, `:64`, `:104`) and points to this card's §0 for the code anchors, which no longer appear in the contract (Rule 7).
- **H5a-R5 — applied.** Confirmed: `owner_state` is written at `book_account_owner.py:334`, `:388`, `:680`, `:1748`, `:1873`, `book_bootstrap.py:174` and `book_migration.py:412`. Only `:174` sets RUNNING/NORMAL. §2 is retitled and the scan widened to cover every `owner_state` INSERT/UPDATE, `authority='NORMAL'` and bound parameters. Admission-level restarts are assigned to S1/S7.
- **H5a-R6 — applied as a concern only; no edit outside this task's files.** Confirmed: the header callout and §4.1 shift the contract's line numbers. `docs/notes/2026-09-27-orb-fence-ruling6-disposition.md:63` (`…contract.md:67`) and `:143` (`…:26`) cite unpinned working-tree lines. Some rows of `docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md` cite `:37`, `:30`, `:67–:73` and `:28` unpinned; another row is pinned to `521d8f2`. The coordinator should require `521d8f2:<path>:<line>` or section-and-row citations, or re-anchor those files after H5a is accepted.

Re-run after the fixes: `python3 scripts/check_handoff_authority.py --all` gave "2 card(s) with an authority block, 0 violation(s)", exit 0; run on this file alone it gave 1 card, 0 violations, exit 0. A local relative-link and heading-anchor check over the three H5a files found 0 unresolved. `git diff --word-diff` showed 0 deletions in the contract and 0 in the Phase 5 plan.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED as the H5 step (b) dispatch card. Status: READY.** H5 step (a) is accepted in the same commit: the halt/resume amendment, applying the operator's O-6 and O-7 clarifications, and the Phase 5 pointer.

**Coordinator dispositions:**
- **§7 known path: the coordinator intends choice (B), to be recorded in §10 at dispatch.** S1 is pinned `xfail(strict=True)`, with the reason naming CC-3 and §A11.2, and the other cases continue. This is a **recorded variance** from the parent H5 stop condition. Under it, (b)'s acceptance is partial, CC-3 stays an open defect (TB-I3/T09), and the S1 XFAIL is not acceptance of §A11.2 behavior. The reason for (B): the defect is already established by code reading, and stopping at its first reproduction would leave S2–S6 unrehearsed.
- **Parent scope (cross-handoff critic X-06).** Step (b) establishes owner-level incident-versus-refusal behavior, restart-during-halt behavior, the structural absence of other activation paths, and local notifier behavior, all synthetically. **Real delivery and 60 s escalation are measured in T13 (Phase 5 WP2).** The exception is if the operator runs the delivery leg on an existing, no-spend channel at dispatch, as this card allows. The parent H5 card and the addendum's §3 H5 row are amended to match.
- **O-6 and O-7:** decided by the operator on 2026-09-27 (incident ADR §A11.2, clarifications). S6 is updated.

---

## Coordinator acceptance of the return (2026-09-27)

**ACCEPTED, PARTIAL under the §7 (B) variance.** The return is [PR #521](https://github.com/Joshua-Asante/first-passage/pull/521), head `32e0863` on `claude/h5b-incident-rehearsal`, cut from `origin/main` `5ad04cf`. Worker status: `DONE_WITH_CONCERNS`. The operator merges.

**Coordinator re-verification (clean detached worktree at `32e0863`, launcher with the scratchpad operations environment, Python 3.11):**
- The diff holds exactly the two §1 files: the new test module and the new evidence note. There is no production code, no existing-test edit and no fixture module.
- The test node names match the amended `acceptance` list exactly: 15 nodes.
- `pytest tests/ops/test_attended_incident_rehearsal.py tests/ops/test_four_leg_runtime.py -q`: 35 passed, 3 skipped, 1 xfailed; record completed, exit 0, source stable.
- `check`: completed, exit 0, source stable.
- The worker's disclosed `test-ops` failure (`test_qualification_isolation.py::test_qualification_suite_in_clean_process`, `ModuleNotFoundError: cryptography`) reproduces on unmodified `origin/main` in the same environment. It is environmental and not this PR's. The complete `test-ops` suite is not claimed to pass.

**Review round.**
- **One finding, fixed in `ae9fe50`.** The first revision's S7 incomplete-barrier node sent a direct owner request stamped with the incomplete bar's time and asserted it was accepted. That is evidence against §2 `:30` ("No risk-add dispatch from that bar"). The node now drives the four-leg runtime: three of four legs deliver, nothing is evaluated or dispatched, and there is no halt and no incident. The fourth leg then completes the bar before expiry, and that bar's entry is admitted.
- **The observation on the owner, confirmed by coordinator reading.** The owner's direct `dispatch` does not check barrier completeness. The `:30` gate is the runtime's (`book_runtime.py:390`). The only `ops/` caller of `handle_book_action` is the runtime (`book_runtime.py:412`, `:418`, `:456`), and `handle_book_action` documents itself as the offline Phase-2 boundary with no production route. No TB-I3 item is raised.

**What the return establishes (synthetic / replay engineering only):**
- S2 and S4–S6 end automation for the session: a stale fact, feed silence, a restart during a halt, ambiguous protection and an operator stop.
- The S7 refusals refuse only the request.
- No RUNNING/NORMAL write site exists other than `book_bootstrap.py:_activate_bootstrap`.
- The local notifier cannot change the halt, generation or permission.

**What stays open:**
- **CC-3 (TB-I3/T09):** the S1 XFAIL(strict) is not acceptance of §A11.2 behavior. A repair turns it into an XPASS, which fails the suite.
- **Incident → notification emission, 60 s escalation, failure routing and the external heartbeat:** ABSENT.
- **Real delivery:** OWED to T13 / Phase 5 WP2.
- **Restore from backup:** Phase 5 WP3.
- **O-1 to O-5:** with their §4.1 owners.
- **The late-bar ruling:** it covers late bars only. A future bar, a bar outside the session and a wrong-bar intent are not classified.

**Unlocks:** T13 construction (parent card H5), with H2's commissioning traces folded in before any session that could produce an unresolved request. **Not granted:** a merge, a session, a drill, an arm, a deployment, GO, account traffic, or any later-release policy.
