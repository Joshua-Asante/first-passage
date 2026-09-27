# Staged acceptance handoff set — bounded next steps toward deployment (2026-09-27)

**Status:** PREPARED 2026-09-27 under the operator direction recorded in the [deployment-checklist addendum 2026-09-27](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step). None is dispatched by this file.

**Ownership:**
- The campaign coordinator dispatches each card under the committed-handoff rule. At dispatch the coordinator copies the card into its own file with its `yaml authority` block, at most the grants listed on the card, and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*). This set carries no authority block because a file holds only one.
- The addendum owns sequencing and the checkpoints CP-1..CP-9. Each card's named owners keep their outcomes.

**Common rules:**
- Read `AGENTS.md` first.
- No agent places, amends or cancels an order. No merge, spend, arm, deploy, vendor contact or account access by an agent.
- No private source, account figure, P&L or credential is committed, quoted or sent to an external service. The book's Pine and runtime ports are read only in place in the operator's primary checkout ([§60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)).
- Commissioning results are labelled `COMMISSIONING_OBSERVATION` and never enter qualification (addendum §2).
- A finding that changes behavior returns to its owner decision before the freeze (addendum §5).

**Dispatch states:**
- **READY:** existing authorization covers it now.
- **READY ON <event>:** dispatch when that event is recorded.
- **LATER:** requirements recorded, not yet a card.

| Card | Workstream | State | Unlocks |
|---|---|---|---|
| H1 | S5 and resource limits | READY | CP-1 |
| H2 | Broker route commissioning | READY | CP-2, then CP-3 |
| H3 | ORB lifecycle and fence trace | READY (operator machine) | CP-4; H4 fence half |
| H4 | ORB lifecycle and fence implementation | READY ON H3 acceptance (fence half) / CP-4 (lifecycle half) | CP-5 evidence; the fence repair before the ORB freeze |
| H5 | Attended operations | Step (a) READY; step (b) READY ON acceptance of (a) | T13 construction |
| H6 | Settlement evidence | READY ON CP-2 (collection); rehearsal harness READY | CAP S1/S2 toward QUALIFIED |
| H7 | Production qualification host | READY | CP-1 (RC-4/RC-5 confirmation), later CP-8 |
| H8 | Feed (provider-neutral) | READY | CP-7 inputs; the F1 feed section |
| H9 | Result/seal and recovery | READY ON S5 Checkpoint C3 accepted | T06/S8 |
| H10 | Final launch | LATER | CP-9 |

---

## H1 — S5 Part A measurement proposal (existing workload)

**Uncertainty resolved:** the CPU, wall time and peak memory of PART_A at the S5 fixture's **maximum expansion** on the **existing** engine. This settles whether a per-phase TEST_ONLY ceiling exists that passes Σ-feasibility at binding for `/v7`. If none does, that is S5 draft §2.3's falsifier for the per-phase model.

**Prerequisites and existing authorization:**
- Operator ruling 2026-09-26 §6: "S5 measurement preparation is a separate bounded handoff" ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26)).
- The build-entry and C3 split ([ledger 2026-09-27](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)).
- Prior evidence to reuse: the [T10 step-4 measurement](../../notes/2026-09-24-t10-step4-representative-measurement.md) and its harnesses, the 2026-09-16 `benchmark_part_a` record, and the S4 C2 precedent (a Windows N2 measurement → the `/v6` N2 ceiling, `profile.py` `_JOINT_N2_DIAGNOSTIC_PHASE`).

**Work:**
1. **Workload.** The S5 fixture's frozen budget binding (`part_a_initial_paths` / `part_a_expanded_paths`, 4 / 8 per the [S5 packet](2026-09-21-full-e1-s5-part-a-DRAFT.md) §0), on the signed TEST_ONLY composition fixture, through `part_a._run_part_a` with expansion forced. If expansion cannot be forced economically, measure the initial and appended panels separately and compose them, and disclose that the result is composed.
2. **Reference runtime.** Propose one option and justify it:
   - (a) the `ubuntu-24.04` runner class used by the qualification workflows. This needs a measurement job and `ci.dispatch`, granted only by the dispatch card.
   - (b) a recorded Linux x86-64 host with the launcher's interpreter, backed by the Windows launcher for continuity with T10/C2.
   - Recommended: (b) for build entry, because C3 re-measures on the runner (RC-3b).
3. **Capture.** At least three sequential repeats on an otherwise idle process. Record:
   - CPU user+system (children included);
   - wall time;
   - peak RSS;
   - interpreter hash, tree SHA and CPU model;
   - output digests, compared with the recorded digests where the shape matches.
4. **Proposed rule.** Give the form and the numbers: ceiling = max repeat × *k*, for CPU, wall and memory separately, with the controller charge unchanged. Justify *k* against the observed spread and the S4 precedent (measured 211 s CPU → 360 s ceiling). State how the coordinator applies the rule at C3.
5. **Feasibility.** Σ phase ceilings against the `/v7` TEST_ONLY cap, shown by a test or a computation on the fixture. No campaign is run.

**Limits:**
- Harnesses are kept as `.py.txt` beside the note, following the T10 step-4 convention.
- No edit under `ops/` or `tests/`, and no profile, ceiling or release-literal change.
- No S2/S3/S4 Linux run.
- Envelope: 250k tokens; split at the halfway review if the forced-expansion question is still open.

**Stop conditions:**
- Output digests differ from the recorded ones on a matching shape: stop and report, because that is an engine change.
- Maximum expansion cannot be produced or composed defensibly: return what was measured, with the gap.
- Σ-feasibility fails at every *k* ≥ 1: return at once (§2.3 falsifier).

**Recovery:** measurements are side-effect-free. A failed repeat is retained and re-run, never dropped.

**Evidence retained:**
- `docs/notes/<date>-s5-part-a-measurement.md`, with raw data and harness hashes in its folder;
- the launcher `record.json` paths;
- class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.

**Decision unlocked:** **CP-1.** The operator approves the measurement-and-margin rule and the provisional PART_A ceiling, and releases the S5 hold for the build.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the note's feasibility computation plus `tests/ops/qualification/test_part_a.py` passing unchanged on the measured tree.

## H2 — Route commissioning session packet (operator-run, automation disarmed)

**Uncertainty resolved:** what the exact route actually does, one micro contract at a time, for:
- an entry carrying its stop;
- the stop `Working` at the filled quantity;
- a cancel of a resting entry and its children;
- a rejected change;
- the normal case of whole-leg liquidation (C-a, investigation only);
- same-session and prior-session reconciliation reads.

**Prerequisites and existing authorization:**
- Gate A accepted (REST §6.11).
- The [drill plan](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) owns the rows. This packet sequences them and does not become a second owner.
- [Incident ADR §A11.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26) authorizes R-1/R-2 only, once entitlement is confirmed. It requires each order-producing row to be prepared individually with its environment, actions, exposure limits and abort/recovery. The race drill X-5 is deferred. There is no automatic fallback to the live eval.

**Work:** write `docs/notes/<date>-route-commissioning-session-packet.md`.
- **Stage 0 (read-only, CP-2):**
  - host confirmation that the rail is disarmed (`dry_run=true`, `emit_enabled=false`);
  - the §0.1 actor inventory as a checklist, with every Account Manager function disabled (CR-12);
  - the entitlement record;
  - the known-order confirmation, proposing the weekly preservation trade as the known order and as the settlement target (addendum §1.3);
  - R-1 in the same session and R-2 after a reset.
- **Stage 1 (order-producing, CP-3):** X-1, then X-4, then X-2 (after M2), then X-3 (after M, or folded into the residual-risk decision per CR-3). Each row gets:
  - its environment;
  - exact actions;
  - one micro contract per request and in total, with the stop in the same request;
  - placeholders for the operator-fixed stop distance, time in market, window and cost ceiling (no figures in the repo);
  - its stop conditions;
  - the drill plan's five-step recovery;
  - its evidence entries.
- **Session rule:** stop after the first unexpected result, return the traces, and review before any further row.
- **Operator-sent text:** the M and M2 vendor questions and the one permitted T08 follow-up, drafted for the operator to send. Vendor contact is the operator's.
- **CP-2 fact list:** entitlement, sim/demo availability, the known-order definition, whether drill costs count against the $700 ceiling, and preservation-trade treatment (drill plan q9, OPEN).

**Limits:**
- Documentary only: no account access, vendor contact, order or figure.
- Nothing wider than the drill plan's one-contract limit.
- X-5, C-b rows and the GC-5 takeover composite are excluded.

**Stop conditions to write into the packet:**
- any `unknown` outcome: no resend, read first;
- a stop not `Working` at quantity 1 within the wait;
- an unexpected position or working order;
- competing-actor activity;
- a rail state other than disarmed;
- the time limit reached.

**Evidence retained:**
- the packet itself;
- after a session: original bytes under the drill plan's private manifest (hashes only in the repo), plus one outcome line per step, recorded against CAP R2–R5 / T08 §7 behavior rows as `COMMISSIONING_OBSERVATION`.

**Decision unlocked:** **CP-2** (route facts) and then **CP-3** (row-by-row written authorization). Traces feed CP-5.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `python scripts/check_handoff_authority.py --all` and `make check` clean on the branch.

## H3 — ORB resting-entry lifecycle resolution and four-state fence trace

**Uncertainty resolved:**
- Does the accepted ORB cancel a resting entry after one bar or at session end, in source and in its accepted replay (§59 Ruling 5; B–D packet B-13)?
- How does the rail spec classify a known working order with fresh evidence (state (i))?
- How does each consumer classify states (i)–(iv) (B–D packet fence row and four-state table)?

**Prerequisites and existing authorization:**
- Ruling 5 approves preparation and fixes the resolution order: source and replay first, the lifecycle ruling separate from the fence trace.
- The B–D packet assigns the source/replay resolution and the trace to the coordinator.
- §60 read access, in place on the operator's primary checkout. A cloud session cannot read the port.

**Work:**
- Trace, source to consumer: `book_account_owner.py` `_ordinary_unknown_orders_db` and its consumers (admission `:1608`, takeover, protection re-arm, close operations, capacity release), plus every other consumer found.
- Read the rail spec's §1 `pending`/`W` rows, S1, S2/RC-9 and E3.
- Read the declared ORB's cancel behavior and the qualification replay's cutoff cancel (`replay.py`).
- Return:
  - the four-state table, confirmed or corrected;
  - a proposed spec clarification;
  - a lifecycle proposal with its alternatives and their consequence for the fence, the edition pre-registration and requalification.

**Limits:**
- Read-only. No edition replay (the pre-registration forbids one before freeze).
- Pine or port bodies and values are neither quoted nor committed; describe behavior only.
- No code change.

**Stop conditions:**
- Source and replay disagree: return both, with no choice made.
- Neither behavior may be chosen to make the fence stop blocking (B–D packet).

**Recovery:** not applicable (read-only).

**Evidence retained:** the return note with file:line anchors in public code, and behavior-level descriptions of the private sources.

**Decision unlocked:**
- **CP-4**, the operator's B-13 ruling.
- The coordinator's acceptance of the trace, which makes H4's fence half dispatchable.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

## H4 — ORB lifecycle and fence: implementation in replay and synthetic consumer tests

**Uncertainty resolved:** whether the owner and replay behave as ruled across every request state, before any real route is involved.

**Prerequisites and existing authorization:**
- The fence half needs H3's trace accepted. Its behavior is fixed for the first release by §A11 item 1, so it does not wait on gate D (addendum §1.2(b)).
- The lifecycle half needs CP-4.

**Work:**
- Tests first, then the change in `book_account_owner.py` and each traced consumer. Cases:
  - fresh-working, stale, unknown and terminal requests;
  - reservation held and released;
  - the incident halt path (TB-I3 scope boundary respected);
  - cutoff, flatten and deadline;
  - takeover revalidation.
- The pinned behavior at `tests/ops/test_book_feedback_journal.py:41-55` changes only as the trace and ruling require, and is listed explicitly.
- If the ruled lifecycle differs from the qualification replay's cancel behavior, the replay change is a **CHECKPOINT** before any edit. It changes qualification behavior, so it enters the edition pre-registration and requalification (addendum §5).

**Limits:**
- `SyntheticBroker` seam only; no production transport (T09).
- No `lab↔ops` import, locked parameter or DD constant.
- Branch and PR; the operator merges.

**Stop conditions:**
- A consumer the trace missed.
- A needed change outside the owner and its consumers.
- Any replay edit.

In each case return to the coordinator.

**Recovery:** a branch revert. No shared state is touched.

**Evidence retained:** the test node IDs per case, the launcher `record.json`, and `make check`.

**Decision unlocked:**
- The fence repair is recorded as resolved before the ORB freeze.
- The results are input to **CP-5** (gates B–D).

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the new owner-consumer test nodes named in the dispatch card.

## H5 — Attended operations: owner reconciliation, then synthetic incident rehearsal

**Uncertainty resolved:**
- (a) Which resumption rule governs: halt/resume rev9 allows same-session resumption; §A11 and the [Phase 5 plan](../../superpowers/plans/2026-09-16-phase5-attended-operations.md) do not.
- (b) Do alerts, escalation, heartbeat, fencing, manual intervention, restart and resume behave as specified with synthetic incidents?

**Prerequisites and existing authorization:** §A11 items 1, 2 and 4 are ruled. The Phase 5 plan is PROPOSED. Step (b) waits for the operator's acceptance of (a).

**Work:**
- (a) Proposed owner text for the halt/resume contract §2–§4, consistent with §A11: no same-session reactivation after an incident; acknowledgment never equals permission to resume; manual intervention is subject to fencing, outcome evidence and reconciliation.
- (b) A synthetic incident script (lost response, stale evidence, missed alert, restart during halt, ambiguous protection). It is exercised against the existing owners with a notification channel the operator names. Measure delivery and 60 s escalation.

**Limits:**
- No rail deploy or arm, and no account traffic.
- A notification channel that needs spend or a new account returns to the operator before use.

**Stop conditions:** any path that resumes without a fresh operator authorization. Stop and return; it is a defect.

**Recovery:** rehearsal state lives in disposable stores and is discarded after its evidence is retained.

**Evidence retained:** delivery and escalation timing traces, restart and restore traces, and the refused automatic-resume case.

**Decision unlocked:**
- T13 construction on accepted text.
- Commissioning traces from H2 folded into the T13 procedure before any session that could produce an unresolved request.

**Grants at dispatch:**
- (a) coordinator: `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`.
- (b) worker: `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`.
- Acceptance for (b): the rehearsal test nodes named at dispatch.

## H6 — Settlement collection and reconstruction rehearsal

**Uncertainty resolved:**
- Actual report coverage.
- The three S2 source facts: the `Timestamp` offset, the `Date` meaning after the rollover and the query-bound semantics ([CAP addendum 2026-09-24](../phase4-preparation/2026-09-16/capability-decision.md)).
- Missing-data detection.
- Whether the verifier and account owner reconstruct an anchor and a subsequent close from original bytes.

**Prerequisites and existing authorization:**
- The 2026-09-25 account-side read authorization (T07).
- CP-2 retargets the reads from the D1 transaction to the preservation-trade transaction (addendum §1.3).
- The rehearsal harness may be prepared before CP-2.

**Work:**
- **Operator collection.** Report originals covering the target transaction, with the report context captured: timezone setting, query bounds, and a row after the rollover. Stored in the private root and hashed into its manifest.
- **Agent rehearsal**, on the operator's machine for private bytes:
  - isolated anchor ingestion and a subsequent-close ingestion;
  - correction refusal and restoration;
  - a missing-data case;
  - the time the procedure takes.

**Limits:**
- Read-only exports; no account reset; no API use while API entitlement is unverified.
- Private bytes never committed.

**Stop conditions:** an unsupported decisive source fact. Return promptly and continue only independent collection (T07 checkpoint).

**Recovery:** the rehearsal stores are disposable. No silent predecessor reset.

**Evidence retained:** manifest hashes, consumer traces with record IDs, and the timed procedure. CAP S1/S2 rows are proposed for coordinator acceptance.

**Decision unlocked:**
- The S3/B7 predecessor decision.
- The requirement for an operator-facing sign/submit entry point, scoped to T09 or tooling.

**Grants at dispatch (worker, for the harness):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the reconstruction consumer test nodes named at dispatch. Collection is operator-performed.

## H7 — Production qualification host: specification and OF assignment

**Uncertainty resolved:**
- Who verifies each of OF-1..OF-7, at which gate, and where the record lands (RC-5).
- Which gate set governs OF-5..OF-7 (S5 draft §6 Q12).
- The owner and slice of the client plan-view seed change (RC-4).
- What a production-class host needs, and what it costs.

**Prerequisites and existing authorization:** the 2026-09-26 direction to "assign seed-view implementation and host attestations to their specified gates". The seat does not choose the owner itself; it proposes.

**Work:**
- **Proposed owner text.** Recommend the stricter reading of Q12: every OF at provisioning, before any production-authority release and after any access change, plus the specific OF-5/OF-6/OF-7 gates.
- **Host specification:**
  - OS and cgroup v2 / systemd features;
  - the `qclient`/`qexec`/`qg5`/`qseal` principals;
  - key storage and custody;
  - enrollment inputs;
  - K3 salt custody.
- An itemized cost line if provisioning needs spend.
- A named slice for the RC-4 seed view, with its F1 admission check.

**Limits:** documentary only. No host rental, credential creation or key generation.

**Stop conditions:** an OF that cannot be verified by an attended read. Return it as a contract question.

**Recovery:** not applicable.

**Evidence retained:** the proposal note and the owner-text diffs, pending acceptance.

**Decision unlocked:**
- At **CP-1**: confirmation that RC-4/RC-5 are F1-entry conditions, with the assignment made.
- Later, **CP-8**: provisioning and admission.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

## H8 — Feed: provider-neutral preparation

**Uncertainty resolved:** what the funded provider must satisfy for all four symbols before trading use, stated before any provider is chosen.

**Prerequisites and existing authorization:** STATE's source disposition, which allows provider-neutral preparation. D-feed bars signup, subscription and credential staging.

**Work:**
- The TB-I5 successor, a CME execution-feed equivalence test specification (no such spec is on disk).
- Symbol, roll and session mapping for the four legs.
- Gap, reconnect, correction/backfill, duplicate/out-of-order, stale-symbol and DST/early-close handling, specified against the canonical panels.
- The **later-binding rule** text for the F1 packet (addendum §1.4).
- A shadow-collection design with emission disabled.

**Limits:** no provider contact, account, credential or spend. No equivalence tolerance set after seeing data.

**Stop conditions:** a requirement that only a specific provider can answer. Record it as a funding-decision question.

**Recovery:** not applicable.

**Evidence retained:** the spec drafts and the rule text.

**Decision unlocked:** inputs to **CP-7** (funding) and to the T10 phase-2 F1 packet.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

## H9 — Result/seal integration and bounded same-sample recovery

**Uncertainty resolved:** whether S1–S5 and the frozen T05 build hold as one integrated identity under interruption and exhaustion.

**Prerequisites and existing authorization:**
- S5 Checkpoint C3 accepted (the PART_A field sets, the `/v8` snapshot and the capture contract are stable).
- The D3 owner text (S5 draft §3.4) accepted.
- The existing T05 build acceptance.

**Work:**
- Integrate `claude/t05-result-seal@6cf2732` on the S5 head:
  - unify `_settlement_terminal`;
  - take main's `031d79a` roll, "never a fresh one";
  - create the real seal principal and its host-provisioning change (seam row 11).
- Then the D3 slice (R1–R10). The recovery retains every failed attempt and never renews the allowance or deadline. It allocates no attempt ID, salt, seed or plan, and makes no public reveal while recovery remains possible.

**Limits:**
- No production authority, no route-enabling release literal before T06, and no accepted formula or tolerance change.
- No push while a Linux run is in flight.

**Stop conditions:**
- An integration conflict that changes an accepted interface.
- Any path that redraws or renews allowance.

In either case return to the coordinator.

**Recovery:** branch-level only. Retained attempts are never deleted.

**Evidence retained:**
- Linux qseal and result-G5 cases, exhaustion and interruption cases, and receipt-history cases (a receipt is history, not authority);
- Windows lines and `check`.

**Decision unlocked:** T06/S8 dispatch on one identity.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`, `ci.dispatch`. Acceptance: the integrated result/seal Linux node set named at dispatch.

## H10 — Final launch: exact-candidate rehearsal and one attended session (LATER)

**Recorded now so it is not rediscovered:**
- The timed rehearsal runs on the exact T16 candidate with synthetic inputs: B7 capture → sole n3 → verdict/expiry/void rules → GO/reseal → restart → activation acknowledgment.
- Deployment GO and initial-session authority are separate operator acts at **CP-9**.
- The session is one attended session under preserve-and-block. Explicit review follows before any extension (§A11 item 1).
- Failure leaves the candidate disarmed or halted as prescribed. Elapsed time is never approval.
- The card is written when T16 is accepted.
