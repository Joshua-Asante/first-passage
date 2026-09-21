# PR #436 (S2 integrated candidate) — independent acceptance review

Reviewer: read-only, 2026-09-20. Worktree `pr-363-babysit-671b91`, branch `claude/s2-enforcement-gaps-fab5e6` @ `915035c`.
Diff reviewed: `git diff f2606b0...HEAD -- ops tools deploy scripts tests .github` (19 files, +3079/−111; no `tools/` or
`.github/` change on the branch). Repository untouched. Line numbers are HEAD working-tree lines. The G3 packet
(`docs/briefs/handoffs/2026-09-20-full-e1-s2-g3-resume-before-exec.md`) is read and its two defects (SIGUSR1 to runc init
before exec; no retained payload exit code on the non-credited path) are NOT re-reported below.

Read in full: CLAUDE.md; plan S2 slice + shared contract + contract decisions + every 2026-09-19/20 ledger entry through
"GLM continuation"; spec §2.5–2.8, §6 E01–E12, resource-scope clarification; coordinator handoff "Shared decisions";
G1/G2 packets (§0.5 defaults, §7 returns, G2 §7.8 coordinator addendum); both audit notes; the production sources
`campaign_supervisor.py` (1212 lines), `campaign_store.py` (diff + §165–410, §778–1235), `campaign_funding.py`
(diff + `_funding_projection`/`claim_scheduler_bootstrap`/`materialize`), `service.py` (diff + `recover_service`/`serve`),
`campaign_probe.py`, `bootstrap.py`, `campaign_budget.py` (state machine), `store.transaction`, the verification script,
the S2 workflow, the manifest diff, both Linux S2 test files, and the new/changed Windows tests.

## Verdict

**VERIFIED WITH CAVEATS.** No fail-open path found: nothing in the diff mints authority, refunds a charge, double-starts,
clears VOID, or lets the store credit a work the guardian did not alive-verify. The five enforcement gaps are closed in
code, and each has a registered Linux node that is non-vacuous for its load-bearing property on the cited green runs.
Production bytes at HEAD are identical to the three fifteen-green runs' heads. The caveats are semantic/liveness items
that S3 must not inherit unexamined (A1–A3 in particular), plus several places where a Linux node tolerates either side
of a race so the *stop* half of a behavior is proven only by Windows simulation or by a red run.

BLOCKING: 0 · ADVISORY: 9 · NOTE: 10

---

## Lens 1 — S2 contract coverage (behavior bullets + five gaps)

| Requirement | Where enforced | Kind | Linux node proving it | Vacuity check |
|---|---|---|---|---|
| Gap 1 — payload CPU independent of guardian | `campaign_supervisor.py:121-137` (`payload_cpu_quota_usec`), `:214-215` (`CPUQuotaPerSecUSec` on payload slice), `:205` (`RuntimeMaxUSec` on guardian), `:214` `BindsTo`; realized `cpu.max` verified in-guardian before any payload `:994-1002`/`:140-160`; absolute kernel timer `bootstrap.py:53-56` caps lifetime below RuntimeMax | kernel (`cpu.max`) × manager (RuntimeMax) × kernel timer; guardian poll `:1128` is early-stop only | `test_s2_payload_cpu_is_kernel_bounded_without_guardian` (`test_campaign_supervision_linux.py:450-566`) | Non-vacuous: ≥3 payload identities + two ≥150 ms/s intervals before STOP (`:486-503`), `peak ≥ baseline+0.15·window` (`:555`), `nr_throttled>0` (`:554`), upper bound `:549`, unit ended by SIGKILL at/after the deadline `:538-539`. Final run: peak 99.06 s / 100 s, 2970/2974 throttled. |
| Gap 2 — original deadline before bootstrap | `bootstrap.py:19-59` arms `CLOCK_BOOTTIME` SIGKILL from argv before `sys.path`/`importlib` (`:60,:78`); `guardian_deadline` cross-check `campaign_supervisor.py:163-173`, `:867-871`; already-past argv refused `bootstrap.py:57-59` | kernel timer | `test_s2_deadline_kills_guardian_before_bootstrap_completes` (`:591-653`) | STOP lands before any supervision event (`:609`), `Result=signal` not RuntimeMax `timeout` (`:638`), `resumed_at<deadline<=ended_at` (`:640`), payload never populated (`:647`). Caveat N1: the assertion tolerates a `DEADLINE` event (`:646`), in which case the kill could equally be `guardian_main`'s own second timer (`:878`); the recorded evidence run had `supervision_kinds=[]`, which does discriminate. Windows source-order guard `test_campaign_supervision.py:2259-2273`. |
| Gap 5 — verified identity before completion | `_run_probe` `:1097-1107` (alive read of `/proc/<pid>/{stat,status,cgroup}`, UID vs container `User`, cgroup under payload slice `:1072-1073,:1095`), gate `:1142-1148` (`PROCESS_UNOBSERVED` + refusal), credit only `exit_code==0 and RUNNING` `:1157` | guardian code (polled); **not** store-enforced (see A5) | `test_s2_probe_that_exits_before_observation_never_completes` (`:386-442`) | Non-vacuous on the win: no CAPTURED/COMPLETED/SIGNING_INTENT `:403`, zero payload-scope PROCESS `:406`, guardian self-identity present as negative control `:407`, FAILURE retained `:416`, IN_DOUBT with no observation `:419`, no guardian-authored recovery row `:420`, restart completes recovery with unspent slot `:426-430`, every COMPLETED work in the suite has a payload identity `:433-438`. Caveat N2: `PROCESS_UNOBSERVED` is optional (`:417`) — the informative refusal path is not required by the node. |
| Gap 3 — funded post-admission VOID authentication | transport `service.py:339-346` (retry/queue/status only); claim `campaign_store.py:496-535` (durable one-use charge object, refused when not admitted/terminal/pending/insufficient); verify under `controller_cpu_guard` `service.py:352-374`; refusal `campaign_store.py:545-559`; completion `:561-570`; charge folded into projection `campaign_funding.py:399-406`; integrity `campaign_store.py:1356-1385` | store transaction + kernel SIGKILL timers (`controller_cpu_guard` `campaign_supervisor.py:766-790`) | `test_s2_post_admission_void_authentication_is_charged_per_attempt_and_never_forged` (`test_campaign_service_linux.py:89-141`) | Non-vacuous: 3 forged attempts each +2 s, VALID; client peer refused before cost; valid key = 1 more charge → VOID; exact retry free; restart preserves. Exhaustion is Windows-only (G2 D8; `test_campaign_cancellation.py:239-281`, verifier provably not called). |
| Barrier (ruling C) | `_cancellation_barrier` `campaign_store.py:430-442`; `_check_budget` `:879` (admitted only), `reserve_work` `:1037` and `claim_scheduler_bootstrap` `campaign_funding.py:552-554` (unconditional) | store | `test_s2_queued_cancellation_bars_new_work_while_admission_still_settles` (`:171-234`) | Caveat N3: (a)'s private-route refusal accepts either race outcome (`:189-196`); the barrier observation is not required by the node. Windows pins every chokepoint (`test_campaign_cancellation.py:283-337`). Pre-admission refusal retained/cleared and post-receipt charged refusal are deterministic parts of the node. |
| Gap 4 — safe admission retry | `service.py:300-328` (resume only when `inspect_unstarted_admission` says resumable, under `dispatch_lock`+guard; `prepare_campaign_work` retains START_INTENT + one-use START_OWNER atomically `campaign_supervisor.py:98-114`; non-RESERVED → status `:352-353`); restart skip `service.py:553-570`; `inspect_unstarted_admission` `campaign_store.py:572-619`; `recover_campaign_work` RESERVED guard `campaign_supervisor.py:1202-1203` | store serialization (one-use rows) | `test_s2_admission_retry_after_service_death_never_double_starts` (`:237-279`) | Convergence only (≤1 dispatch, ≤1 START_OWNER, NRestarts=0, never PROVISIONAL+RESERVED). Caveat N4: whether any of the three samples actually lands in the RESERVED-no-intent state is recorded (`interrupted_left`) but not required; the deterministic RESERVED resume is Windows-only (`test_campaign_cancellation.py:537-575`, `640-656`). |
| "Stop and retain terminal status on overrun/OOM" | overrun stop `:1128-1135`; OOM stop on parent `memory.events` `oom_kill` increment over loop baseline `:1056,:1128-1129` (durable IN_DOUBT before kill) | guardian poll (stop); settlement retains facts | `test_s2_two_descendants_exhaust_owned_cpu` (`:156-181`), `test_s2_shared_memory_oom_is_retained_last` (`:656-678`) | Caveat A6: both nodes accept either the guardian stop or the timer/settle path; on the three green runs the OOM case went through settle (`oom_kill=1`), so the *stop-on-OOM* code path is host-proven only by the red run 35492219418 and by Windows `test_payload_oom_increment_stops_the_container_and_settles_without_completion`. |
| Counter loss charges the reservation | `observation()` `:573-603` (cpu `None` unless terminated and slice present) → `settle_work` `campaign_store.py:1113-1116` | store | guardian-death `:196-206`, deadline case `:650-651`, payload case `:561-562` | Non-vacuous (`charge == limits.cpu_ns` asserted). |
| Cleanup failure cannot restore authority | `_recover_campaign_work` `:311-326` (PENDING → `CLEANUP_PENDING`, recovery row stays open) | store | none new (Windows `test_recovery_commits_uncertainty_before_cleanup_failure`) | unchanged from S1/R1 |
| Restart recovers with unspent slot; second restart harmless | `recover_campaign_work` settled-guard `:1204-1206`; `_guardian_self_failure` never claims a slot `:965-991` | store | unobserved-exit case `:421-430` (one restart) | Caveat N5: no Linux node restarts a campaign with completed works twice; the restart-2 barrier fix is Windows-pinned only (`test_second_restart_skips_completed_recovery_and_keeps_new_work_schedulable`). |

Manifest: exactly fifteen `test_s2_*` nodes under the two files (`invariant_manifest.json` diff), matching the file
contents; `--s2` requires all fifteen present-and-passed with zero skips/failures/errors
(`scripts/qualification_boundary_verification.py:39-45,:79-82,:109`).

## Lens 2 — fail-closed audit of every new refusal/settlement path

- `_run_probe` (`:1021-1170`): credit requires `seen_pids` non-empty **and** `exit_code==0` **and** work still `RUNNING`;
  `PROCESS_UNOBSERVED` + raise on empty identity; overrun/OOM commit IN_DOUBT *before* the kill; the `except OSError`
  re-inspect (`:1076-1094`) only continues when docker says not-running, raises after ~1 s of docker lag; the SIGUSR1
  send tolerates an exited container only when docker confirms not-running (`:1120-1122`). No authority minted. ✓
- `_guardian_self_failure` (`:965-991`): IN_DOUBT only from START_INTENT/RUNNING (negative transition; `_check_budget`
  skips funding gate and barrier but still refuses on VOID/terminal `campaign_store.py:886-889`, swallowed at `:981`);
  FAILURE event; best-effort container kill; never claims a slot, never calls `cleanup`. ✓ (A2 notes the CAPTURED case.)
- `recover_campaign_work` (`:1173-1212`): RESERVED-no-enrollment-no-row → status (reservation stays open, no refund);
  settled+completed-recovery → status; everything else claims the one-use slot in its own transaction. A legacy spent
  slot with no snapshot row falls into the first guard silently (N6) but authority stays blocked by the object scan
  `campaign_store.py:318-327`. ✓
- `recover_service` (`service.py:520-575`): unstarted admission → report only; expired → ownerless `recover_work`
  RESERVED path (`campaign_store.py:1200-1201`, no slot, no OS effect, terminal via `_observe_clock`). ✓ Runs before
  `bind()` (`service.py:602-607`), so no concurrent SUBMIT_E1. ✓
- `claim_void_authentication` (`campaign_store.py:496-535`): requires the exact queued body, a receipt, VALID, BOUND,
  no overlay/pending/recovery/dispatch, `bound ≤ remaining`; charge written before any verification; refusal returns
  status with the body still queued. `refuse_void_authentication`/`complete_void_authentication` require the charge to
  exist and be unresolved (`_charged_attempt` `:537-543`); completion calls `void()` inside the same reentrant
  transaction (`store.py:152-170`) and deletes the body atomically. No refund anywhere. ✓
- `_cancellation_barrier`: never sets validity; clears only by charged authentication or by VOID (moot). ✓
- `inspect_unstarted_admission` (`:572-619`): returns `resumable` only for VALID+PROVISIONAL+same boot+clock not
  backward+before deadline+no pending/recovery/dispatch+no control-slot objects; grants nothing itself — the resume
  still goes through `prepare_campaign_work`'s terminal/VALID/RESERVED checks. ✓
- `launch_prepared_campaign_work` (`:375-397`): unchanged R1 tail; START_INTENT + no observation required. ✓
- Bootstrap timer / argv cross-check: `bootstrap.py:33-38` rejects missing/non-digit/≤0; `guardian_deadline` refuses
  any mismatch (`test_campaign_supervision.py:2238-2256`). ✓ The sigevent/timerspec ctypes layout is the correct
  x86_64 glibc ABI (`Event` 64 bytes, `TIMER_ABSTIME=1`, `SIGEV_SIGNAL=0`).

## Lens 3 — races and restart

Checked interleavings (evidence in Lens 2 lines): container start/exit vs first observation (G3, excluded), exit between
inspect and `/proc` read (tolerated), docker `Running` lagging scope removal (bounded), guardian death while running
(`BindsTo` retires payload; restart settles `cpu=None` → full charge + BUDGET_UNCERTAIN, asserted `:196-206`), service
restart once (RUNNING work → RECOVERY_OWNER → IN_DOUBT + cleanup kills a *healthy* guardian — operator-ruled R2b
behavior, A3), service restart twice (settled guard; Windows-pinned), VOID while running (claim succeeds → `void()`;
guardian's 1 s authority poll → self-failure; IN_DOUBT transition refused on VOID, FAILURE retained, work settled at the
next restart — fail-closed), VOID queued during the dispatch-pending window (claim refused → body pending → **A1**),
pending-cancellation barrier vs guardian transitions (**A1**), concurrent identical retries (dispatch_lock +
one-use START_OWNER + non-RESERVED → status), funded claim vs guardian authority poll (**A4**, pre-existing).
Single-lifetime clock: every save observes the clock (`_observe_clock`), deadlines derive from `start_clock` only
(`bind_budget` `:990`, `_dispatch_clock` `:225`, `inspect_unstarted_admission` `:610`), and the bootstrap/guardian
timers use `min(campaign deadline, reservation clock + wall)` consistently (`:170`, `:395`, `:554-555`).

## Lens 4 — evidence integrity

- Script: `S2_CASES` ordered tuple (service file first, `:19-21`), both files run in full, required set = every manifest
  node under either file (`:79-82`), zero skips (`:39-45`), owned cleanup must be `ok` (`:111-114`). ✓ A run cannot
  claim more than it proves on these axes. Workflow unchanged since #434 (cleanup exit propagates; `cancel-in-progress`;
  not a required check). Stale comment "Nine admissions" (`qualification-s2-supervision.yml:35`) — N7.
- Head binding: `git diff db667a2 HEAD -- ops tools deploy scripts tests .github` = only
  `test_campaign_supervision_linux.py` (the OOM-case tolerance, +9/−1); `5ac3ad0` likewise; `bbafe68`/`4281d2e` = HEAD
  byte-identical on those paths. So runs 35487909157 (`db667a2`), 35489657203 (`5ac3ad0`) and 35493582848 (`bbafe68`)
  all exercised HEAD's production bytes; the last also exercised HEAD's test bytes. ✓ Run 35494972519 (`4281d2e`, same
  bytes) was 14/15 — the G3 packet owns that; the "green on its final head" wording in the ledger is true per run, not
  a stability claim (N8).
- Windows records present under `.cache/fp-verification/` and match the ledger: `20260920T031137Z-eb07a39ec8ed`
  421/421/0 skipped @`9d7a731`; `20260920T032104Z-1eae37f5ac9b` 79 passed + 1 skipped @`9d7a731`;
  `20260920T040222Z-dfe69327a137` 1494 passed + 1 skipped of 1495 @`db667a2`; `20260920T043625Z-234eacf14883` check
  exit 0 @`db667a2`; all `source_stable=true`, `capture_complete=true`, ops-env Python. Production code at `9d7a731`
  equals HEAD (only the Linux test file changed after it). ✓

## Lens 5 — accounting

- Charges live in `full_campaign_objects` rows and are folded into the **funding projection** only
  (`campaign_funding.py:399-406`); the **snapshot** totals (`_totals` `campaign_store.py:837-844`) exclude them.
  Consequently `budget_snapshot()['remaining_cpu_ns']` and `reserve_work`'s own check (`:1055`) overstate the remaining
  allowance by the charged total, while `diagnostic_status` (funded branch) and `scheduler_status` include it. The
  Linux node even pins this (`test_campaign_service_linux.py:112-113`, `snapshot == frozen`). **No escape today**:
  the only new-work grant in v4 is `claim_scheduler_bootstrap`, gated on the projection (`campaign_funding.py:606-611`),
  and `materialize` never re-checks remaining. Double counting: none — the projection recomputes from the snapshot
  totals + the sum of charge objects on every save (`_validate_funding_predecessor` `:449-461` would reject drift);
  `claim_void_authentication` applies the identical arithmetic (`campaign_store.py:531-533`). → **A7**.
- Unmetered work: signature verification only after a committed charge (`service.py:352-374`); pre-admission bodies
  are paid by the admission work (`campaign_store.py:698-716`, no charge object, contiguous own sequence). A crash
  between charge and outcome leaves a charge with no refusal (D3, `test_campaign_cancellation.py:460-483`). ✓
- The claim path samples no budget clock (`:498-500`): an authentication after the deadline or across a boot is still
  charged and can set VOID (harmless negative fact) — N9.

## Lens 6 — regressions

`campaign_protocol.permitted` unchanged (no diff); N1_ONLY `VOID` branch (`service.py:265-282`) unchanged; dormant v1/v2
`_campaign_request` path unchanged; `diagnostic_status` v3 (non-funded) branch keeps snapshot totals and gains the
three cancellation fields (widened `void_pending` documented by G2 §7.3; dormant status/v1 unchanged, pinned in
`test_campaign_admission.py`); integrity walk validates the three new object roles only when present; old rows have
none. `lifecycle_model.py` is **not** extended for the charge/barrier/identity semantics (spec §6 asks E-cases to extend
the SQL-free model) — N10. No pre-existing test assertion was weakened (diff of the seven touched pre-existing test
files is additive only; `test_qualification_boundary_verification.py` strengthens the S2 selection check).

## Lens 7 — ledger/packet claims vs code

All checked claims hold: `_guardian_self_failure` shape; settled-recovery skip; fifteen nodes; OOM baseline stop;
in-guardian `cpu.max` verification (service-side check removed, `:568-571`); argv deadline + `DEADLINE` event; RESUMED
retained on first send; `payload_process_events` classifier; barrier scoping (D1) and unconditional new-work refusals;
expired-unstarted terminalisation; A1 wording corrected in `campaign_supervisor.py:497-505` and
`2026-09-19-s2-local-supervision.md:11`. Not yet done from the #434 review: ADVISORY-3 (no store-side validator for
`control_`/`event_` work-id prefixes — `campaign_store.py:382` still `'supervision_' + work_id`) and ADVISORY-4 (README
`tools/qualification_verification/README.md:165-170` still does not say qexec may start arbitrary transient units incl.
`User=root`). Carried as N11. One packet inaccuracy: G2 D6 says a legacy admission carrying a RECOVERY_OWNER claim
"keeps today's path (`RECOVERY_PENDING` on a spent slot)" — true only when a snapshot recovery row exists; a v3-era
claim object without a row now returns status silently (N6).

---

## Findings

### BLOCKING
None.

### ADVISORY
- **A1 — A queued-but-unauthenticated body kills in-flight work, and a barrier-induced terminal state makes the
  VOID unrecordable.** `_check_budget` applies the barrier to every positive transition of an admitted campaign
  (`campaign_store.py:876-879`), and the guardian's `_transition(RUNNING|CAPTURED|SIGNING_INTENT|COMPLETED)` and
  `launch_gate(role='payload')` go through it (`campaign_supervisor.py:793-798`, `:1039`, `:1133`, `:1159`, `:1169`).
  Scenario 1 (trusted operator peer, no key): the peer queues any well-formed VOID body once
  (`queue_diagnostic_void` `:391-407`) and never resends it; the barrier stays up until the exact bytes are re-sent, so
  the next positive step of a running work raises `CANCELLATION_PENDING` → `_guardian_self_failure` → durable IN_DOUBT
  → campaign terminal; no key was ever presented. Scenario 2 (legitimate VOID): the request lands while a dispatch row
  is unacknowledged (the ms between `launch_gate` and `acknowledge_dispatch`, `:1039-1042`) → `claim_void_authentication`
  refuses (`doc['dispatch_pending']`, `:520-523`) → body pending → the guardian's next positive transition fails the
  same way → campaign IN_DOUBT → every later claim is refused on `doc['state'] != 'BOUND'` → `void_pending=true`,
  `validity='VALID'` forever; the operator's VOID is never recorded and `void_retry` never answers. Authority is
  fail-closed in both cases and the ruling explicitly lists completion transitions, but "the barrier is transient in the
  fundable case" (G2 D1) is false whenever the barrier itself terminalises the campaign first. Options: let the
  guardian treat `CANCELLATION_PENDING` as wait-and-repoll (bounded by its deadline) instead of failure; and/or allow
  the funded claim on terminal-but-VALID campaigns so a VOID intent can always be recorded as a negative fact
  (mirrors the N1_ONLY `VOID`, which verifies regardless of budget state).
- **A2 — Non-zero exit with retained identity leaves a settled `RUNNING` work under a VALID/BOUND campaign until an
  unrelated restart flips it to IN_DOUBT.** `_run_probe:1149-1170` settles but never transitions; `settle_work`
  (`campaign_store.py:1097-1120`) only terminalises on overrun/OOM/counter loss; `record_work_transition` refuses
  `START_INTENT|RUNNING` after settlement (`:1157-1158`) but not `CAPTURED` — so the store would still accept a
  CAPTURED/COMPLETED for that work. Restart recovery then makes it IN_DOUBT and the campaign terminal
  (`recover_work:1215-1221`). The campaign's terminal state therefore depends on whether a restart happens, and spec
  §2.6 ("RUNNING, no complete durable capture → persist IN_DOUBT") is satisfied only after a restart. Pinned as
  intended by `test_nonzero_probe_exit_settles_without_completion` (`test_campaign_supervision.py:2503-2526`). Benign
  for probes; an S3 N1 worker that exits non-zero must not be left in this shape. Fix shape: transition IN_DOUBT before
  settling on the non-credited path (the overrun stop already does), or have `record_work_transition` refuse CAPTURED on
  a settled work.
- **A3 — Any service restart destroys every running work, healthy guardian included.** `recover_service`
  (`service.py:571-575`) calls `recover_campaign_work` for every non-skipped work; a RUNNING work with no observation is
  claimed, settled with `cpu=None`/`termination_known=False` (the slice is populated, `:584-593`), marked IN_DOUBT, and
  `cleanup` SIGKILLs its guardian (`:625-647`). Operator-ruled for R2b and spec-consistent, but it means an S3
  checkpoint cannot survive a supervisor restart or crash-restart loop; record it as an S3 precondition (a live-guardian
  reconciliation path, or accept the loss explicitly).
- **A4 — (pre-existing, interacts with G1) A funded claim for work B can kill running work A.** `budget_snapshot`
  raises `campaign funding pending` while `bootstrap_pending_work_id` is set (`campaign_store.py:1230-1234`,
  `campaign_funding.py:409-421`), i.e. between the `claim_scheduler_bootstrap` and `materialize` commits of another
  work; the guardian's once-per-second authority read (`campaign_supervisor.py:1065-1066`) and every `_transition`
  (`:794`) use it, and any raise now routes to `_guardian_self_failure` → IN_DOUBT. Window is ms per schedule request;
  no Linux node overlaps two works of one campaign. Tolerate the funding-pending read in the guardian (retry within the
  poll) or refuse the private route while a sibling work is RUNNING.
- **A5 — The identity gate lives only in guardian code.** `record_work_transition` has no precondition tying
  CAPTURED/COMPLETED to a retained payload-scope `PROCESS` event, and `integrity()` does not check "COMPLETED ⇒ ≥1
  payload identity". The suite asserts it post hoc (`test_campaign_supervision_linux.py:433-438`). A future S3 caller
  completing a work through the store directly would not be refused. Add the store-side invariant (transition
  precondition or integrity-walk check).
- **A6 — Stop-on-OOM is not proven by a green Linux run.** `test_s2_shared_memory_oom_is_retained_last:678` and
  `test_s2_two_descendants_exhaust_owned_cpu:181` accept IN_DOUBT (guardian stop) *or* BUDGET_* (settle/timer path).
  All three cited green runs took the settle path for OOM (`oom_kill=1`, ledger); the stop half of "stop and retain
  terminal status on overrun/OOM" is host-evidenced only by the red run 35492219418 and by Windows simulation. Either
  add a stop-specific assertion when the guardian's IN_DOUBT transition precedes the observation, or record explicitly
  that the OOM *stop* is Windows-proven.
- **A7 — Two allowance views.** Snapshot totals exclude VOID charges; the funding projection includes them (Lens 5).
  `budget_snapshot()`/`reserve_work` overstate `remaining_cpu_ns`; `diagnostic_status`/`scheduler_status` are correct.
  Safe today because the funded claim is the sole new-work gate, but any S3 path that reserves through `reserve_work`
  or reads the snapshot's remaining would spend charged allowance twice. Either fold charges into `_totals` (snapshot
  schema change G2 avoided) or make `reserve_work` consult the projection.
- **A8 — Dead guardians are reconciled only by the guardian itself or by a service restart.** A guardian killed by its
  bootstrap timer (`test_s2_deadline_kills…:642`), refused at `bootstrap.py:59`, or SIGSTOPped leaves its work
  START_INTENT/RUNNING with `dispatch_pending=false`, `recovery_pending=false`, campaign VALID/BOUND; other phases can
  still be scheduled and the campaign only turns terminal when a later clock observation passes the campaign deadline
  or the service restarts. No late authority is possible (E12 holds), but the service has no watcher for guardian unit
  exit. S3 should decide whether the schedule route may proceed with an unreconciled sibling work.
- **A9 — Carried from the #434 review, still open on this candidate:** ADVISORY-3 (work-id prefixes `control_`/`event_`
  collide with supervision-object roles; no validator) and ADVISORY-4 (README trust-model wording). Neither is in G1/G2
  scope, but the ledger says the #434 review note is "to be folded into the integration PR".

### NOTE
- N1 — Deadline case tolerates a `DEADLINE` event (`:646`), which would not discriminate the bootstrap timer from
  `guardian_main`'s second timer; the recorded evidence (`supervision_kinds=[]`) does. `/proc/<pid>/timers` is captured
  by the STOPPER (`:580-584`) but never asserted — asserting the armed `signal 9`/`clockid 7` timer would make the case
  discriminating on every run.
- N2 — Unobserved-exit case makes `PROCESS_UNOBSERVED` optional (`:417`); FAILURE-only wins are accepted.
- N3 — Queued-cancellation case (a) accepts either race side for the private-route refusal (`:189-196`).
- N4 — Admission-retry case does not require any sample to land in RESERVED-no-intent; RESERVED resume is Windows-only.
- N5 — No Linux node restarts a campaign with completed works twice (restart-2 fix Windows-pinned only).
- N6 — `recover_campaign_work`'s RESERVED guard returns status for a v3-era spent RECOVERY_OWNER object with no snapshot
  row (no `RECOVERY_PENDING` label); authority remains blocked by `_recovery_pending`'s object scan.
- N7 — Workflow comment "Nine admissions" (`qualification-s2-supervision.yml:35`) is stale (fifteen nodes, up to ten
  fresh admits in the unobserved case); the 90-minute ceiling still holds (1509 s observed).
- N8 — Three fifteen-green runs and one 14/15 on byte-identical production code: the branch is green-but-not-stable
  until G3 lands; the ledger should say so where it says "green on its final head".
- N9 — `claim_void_authentication` samples no budget clock (`:498-500`): an authentication after the deadline or across
  a boot is charged and may set VOID; harmless (negative fact), but the deadline/boot fact is not observed by that path.
- N10 — `tests/ops/qualification/execution/lifecycle_model.py` not extended for charge/barrier/identity/RESUMED semantics
  (spec §6: E-cases extend the manifest *and* the SQL-free model); the R2b `FundingIntentModel` does not model VOID
  charges.

## Summary

BLOCKING: 0 · ADVISORY: 9 (A1–A9) · NOTE: 10 (N1–N10)

BLOCKING items (verbatim): none.

**Verdict on S2 acceptance readiness: VERIFIED WITH CAVEATS.** The integrated candidate closes the five enforcement
gaps with kernel/manager enforcement where the packets promised it (payload CPU, pre-bootstrap deadline, controller
guard), store-serialized one-use authority everywhere else, and fifteen registered Linux nodes that are non-vacuous on
their load-bearing properties on runs whose production bytes equal HEAD. Nothing found mints authority, refunds, or
double-starts. Accept as "the enforced work boundary, not statistical execution" only with these caveats written into the
acceptance: (i) G3's liveness repair remains owed before any S3 worker start; (ii) A1/A2/A3/A7 are S3 preconditions —
they do not fail closed *wrongly*, but they change what state a failed/interrupted/cancelled checkpoint leaves and what
"remaining allowance" means, and S3's N1 vertical would inherit them silently; (iii) A6 should be stated as
"OOM stop Windows-proven" unless a discriminating assertion is added.
