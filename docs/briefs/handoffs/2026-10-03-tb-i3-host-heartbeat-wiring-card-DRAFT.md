# TB-I3-HOST: heartbeat host wiring for the book runtime and notifier (build card, synthetic scope)

**Date:** 2026-10-03.
**Status:** **DRAFT.** Writing authorized by Joshua, direct to coordinator (3), 2026-10-03 about 17:19Z: "I approve your recommendations". He was replying to a list that included "TB-I3-HOST: a new, synthetic-only card for heartbeat host wiring. I recommend yes; no daemon.py, deploy or arming." Coordinator (3) freezes this card after #628 merges and #637's build merges (§1). Nothing here is dispatched. As with other build cards, a worker packet needs the freeze and coordinator (3)'s dispatch record (§12).
**Base:** origin/main `ebe5c0b`. Other revisions read: #637 at `origin/claude/dmon-heartbeat-card` `63a733a` (DRAFT); #628 at `origin/claude/book-incident-notifier` `6e57fda` (OPEN); #633 at `origin/claude/tb-i3-card` `4dce572` (DRAFT); #631 at `origin/claude/ra2-offline-card` `76110a9` (DRAFT); #615 at `origin/claude/t13-first-session-card` `2193fb2` (PROPOSED); #635 at `origin/claude/dmon-grafana-binding-card` `4f41667` (DRAFT). Branch anchors hold only at those heads. **HB** means the #637 card, `docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md`, at `63a733a`. Its threshold constraints are at `:136` there (`:134` at `ec6e220`).
**Brief type:** CC handoff. A code build (TDD) inside a named file boundary, synthetic scope only. No live check.
**Parent:** the umbrella's TB-I3 row (`docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md:232`, STUB; footprint `ops/c1_signal_daemon/*`). HR §7 `:233` gives TB-I3 the watchdogs and host activation. HB P7 `:103`, P9 `:105` and P4 `:100` name this card as their pending owner.
**Finding being closed:** No host calls `step_with_heartbeat` or `notifier_round_with_heartbeat`. No production code builds a `BookAccountOwner`: `rg 'BookAccountOwner\(' ops` matches only the class definition (`ops/c1_rail/book_account_owner.py:347`). HR's owner reading, condition (4) (`docs/spec/2026-09-14-tb-s3-halt-resume-contract.md:71`), requires the missed-heartbeat monitor to cover both notifier and runtime liveness before any armed session. HB P4 cannot freeze T or P until this card supplies the cadence and duration inputs.
**Selected outcome:** A composition module, `ops/c1_signal_daemon/book_host.py`. It runs an injected, already-bound `FourLegEvaluateLoop` through `step_with_heartbeat` on a runtime thread. It runs an injected #628 `IncidentNotifier` through `notifier_round_with_heartbeat` on a separate notifier thread. A validated config-as-code binding refuses any threshold set that breaks HB `:136` (a)–(c) on either side. It is qualified by synthetic tests only. Registration in `daemon.py`, deploy and arming belong to the later live route packet (R-A1/R-H).
**Ownership:** One worker builds it (§11). Coordinator (3) freezes the card, accepts the build, and owns any PR and the ledger. Joshua merges.
**Return boundary:** A pushed branch that touches only the §5 allowed files, or a precise blocker.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_unless_coordinator_records_it
  - allowed_files_section_5_only
  - no_owner_record_edit
  - no_daemon_registration
  - no_route_integration
  - no_rail_deploy
  - no_rail_arm
  - no_account_traffic
  - no_broker_vendor_firm_or_provider_contact
  - no_external_send
  - no_provider_account_or_spend
  - no_secret_value_seen_or_handled_by_agent
  - no_credentials_or_private_data_in_repo
  - no_operator_decision_taken
acceptance:
  - "Every red-first test in §6 (HH1-HH8) fails at the base revision (or is absent) and passes at the returned head; the failing-first run is recorded"
  - "The §7 regression set passes unchanged"
  - "git diff --stat origin/main...HEAD lists only §5 allowed files"
  - "python -I scripts/fp.py check: status completed, exit 0, source stable; or a pre-existing failure disclosed with its reproduction on unmodified origin/main"
  - "HH7's measured step and round figures are reported with their record.json and stay within the frozen binding"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Heartbeat card (HB) and its build | `git show 63a733a:docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md`; at dispatch, the merged `ops/c1_signal_daemon/book_heartbeat.py` | §0.5 item 7 `:73`, item 8 `:74`; P1-P9 `:97-105`; §3.1 `:129`; §3.3 constraints `:136`; §3.7 `build_pingers` `:150`; §3.9 `:153-156`; HQ6 `:223`, HQ7 `:224`, HQ9 `:226`. At dispatch, the merged signatures of `HeartbeatPinger`, `step_with_heartbeat`, `notifier_round_with_heartbeat` and `build_pingers` |
| #628 notifier | merged `ops/c1_rail/book_incident_notifier.py` (`6e57fda` at draft) | `MAX_OUTSTANDING_PUBLISHES` `:66`; `NotifierStoreError` `:105`; `publish_timeout_s` `:209`; `IncidentNotifier.__init__` `:266-279` (`read_incidents`, `clock`); journal `timeout=5` `:304`; `run_once` `:425-436`; `liveness()` `:438-445`; `publish_due` `:447-461`; `_publish_round` `:463`; `_bounded_publish` `:554` |
| #628 owner accessor | merged `ops/c1_rail/book_account_owner.py` | `read_incidents(path)` (`6e57fda:804`); `status()` `:982` at `ebe5c0b` |
| #628 build card | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` (on #628) | §1 `:156`; §8 `:306` (heartbeat), `:308` (host wiring) |
| Loop | `ops/c1_signal_daemon/book_evaluate_loop.py` | docstring `:1-5` (no config constructor or CLI registration); `step` `:29-58` |
| Timing constants | `ops/c1_signal_daemon/book_protocol.py:39-40` (`BAR_PERIOD`, `BAR_SLACK`); `ops/c1_rail/book_protection_owner.py:24` (`PROTECTION_PERIOD`) | constants only |
| Loop fixtures | `tests/ops/test_book_loop_continuation.py:1-31` | how a `FourLegEvaluateLoop` is built on synthetic sources |
| Halt/resume contract (HR; accepted) | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | storage failure `:36`; attendance `:61`; thresholds qualified before live use `:63`; missed-heartbeat monitoring `:65`; owner reading `:67-71` (condition 4 `:71`); §7 `:233` |
| TB-I3 interlock card #633 | `git show 4dce572:docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md` | authority `:7`; TB-I1 narrowing `:10`; §5 `:206`, `:212`; §9 `:250` |
| R-A2 card #631 | `git show 76110a9:docs/briefs/handoffs/2026-10-03-ra2-offline-four-sources-card-DRAFT.md` | §2.2 `:106-118`; §5 `:179` |
| Umbrella | `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md` | TB-I3 row `:232`; reserved files and one writer per file `:245` |
| Multi-leg spec | `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` | R-A1 `:144`; R-H `:157`; R-K split `:163` |
| Image manifest (not edited) | `tests/ops/test_c1_signal_daemon_image_manifest.py:10-15` | `_ENTRYPOINTS` |
| Legacy daemon heartbeat (not edited) | `ops/c1_signal_daemon/heartbeat.py`, `http_status.py`; S2b ADR `docs/adr/2026-08-08-s2b-signal-daemon-build.md:51` | the pull-only `GET /` snapshot |
| Rules | `AGENTS.md` | launcher `:222-226`; *Configuration as code* `:229-238` |

**The report states:** the dispatch revision; the #628 merge commit; the #637 build merge commit and whether the merged `book_heartbeat.py` signatures match HB §3; whether #631 has merged; and every anchor above that moved.

## §0.5 — Clarifications and recorded facts

1. **Authority.** Joshua's 2026-10-03 approval (Status) authorizes writing this card, synthetic scope only. Its terms bind: no `daemon.py`, no deploy and no arming. It does not authorize dispatch (§12; OQ-HOST-5).
2. **A separate card, not a #633 amendment.** #633 forbids `ops/c1_signal_daemon/**` (`:212`) and route wiring in `daemon.py`, `build_loop` or the CLI (`:206`). Its authority is "no route integration" (`:7`), and it is held at a HARD STOP on D-3. Amending it would reopen its freeze.
3. **The API consumed (HB §3, re-read at the merged head).**
   - `step_with_heartbeat(loop, pinger, *, now, read_status)` calls `step`, then `read_status`, then `mark_progress`. An exception propagates unchanged, and no mark is set.
   - `notifier_round_with_heartbeat(notifier, pinger)` calls `run_once` and reads `liveness()`. It marks only when the timestamp advanced.
   - `mark_progress()` returns at once.
   - `build_pingers(runtime_binding, notifier_binding)` refuses a shared reference or a shared resolved URL (H12).

   A different merged API is NEEDS_CONTEXT.
4. **Placement constraint (HB §0.5 item 7, `:73`), enforced here.** The notifier never runs on the runtime loop thread, so a slow publish or a `NotifierStoreError` cannot delay `step`. The notifier heartbeat is marked from the notifier's own loop (HB `:154`). HH1-HH3 test this.
5. **One clock for host and notifier.** `liveness()` returns the notifier's injected clock time after a `run_once` that completes without raising (`6e57fda:436`). The wrapper marks only when that value advances. The host's wall clock and the notifier's clock must therefore be the same source. With a frozen fake clock, notifier marks silently stop. Tests advance the clock.
6. **Round duration has no job cap (finding for OQ-HOST-2).** `publish_due` runs one round per due pending job, in sequence (`6e57fda:447-461`). Each channel publish waits up to `publish_timeout_s`, which defaults to 10 s (`:209`). Each journal transaction may wait 5 s for the lock (`:304`). A provider that answers just inside the timeout frees its slot each time, so `MAX_OUTSTANDING_PUBLISHES` (`:66`) does not bound the round. `max_round_duration` therefore grows with due jobs × channels × `publish_timeout_s`, plus journal time. HB `:156` counts only timeout × channels, which undercounts.
7. **The legacy heartbeat is not this path.** The daemon's `GET /` snapshot (`heartbeat.py`, `http_status.py`; S2b ADR `:51`) has to be pulled; it is not an external monitor. It is not extended.
8. **No operator act is needed for this build.** The heartbeat URLs (HB OA-H1 to OA-H4) matter only for HB-L1 and HB-L2, outside this card. Tests use loopback fake receivers and `env:` references that the test sets.

A contradicted fact, a missing producer or a needed edit outside §5 returns NEEDS_CONTEXT.

## §1 — Goal, scope, dependencies

**Goal.** Build the host composition that the later live route packet registers unchanged. It ties the runtime heartbeat to step progress and the notifier heartbeat to notifier progress, on separate threads, at declared and validated cadences. HB's T and P can then be frozen from real inputs.

**Scope.** `BookHostBinding` and its validator; `BookHost`, which owns the runtime thread, the notifier thread, stop and in-memory counters; synthetic tests. The host builds nothing it runs: the loop, the owner status reader, the notifier, the pingers and the clocks are all injected.

| ID | Dependency | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged | **OPEN** (`6e57fda`) | Freeze |
| P2 | #637 card frozen and its build merged (`book_heartbeat.py` on main) | **OPEN** (DRAFT `63a733a`; build not dispatched) | Freeze |
| P3 | Frozen binding values (§2) | **OWED** to coordinator (3) at this card's freeze (HB OQ-H1) | Dispatch |
| P4 | OQ-HOST-5 recorded (TB-I1 prerequisite) | **OPEN** | Dispatch |
| P5 | Coordinator (3) freeze record (§12) | OPEN | Dispatch |
| P6 | #631 merged | OPEN (DRAFT; freezes when #619 merges) | Not dispatch. If #631 merges after this build, HH7 is re-run and `max_step_duration` is re-declared |

## §2 — P4 inputs and the threshold

| Input | Meaning | Supplied by, and when |
|---|---|---|
| `step_interval_s` | Target spacing between step starts | This card's binding. Frozen at this card's freeze |
| `max_step_duration` | Longest `step` plus `read_status` on a healthy host | Declared at freeze as the sum of declared bounds: four source polls, owner checks, and any dispatch inside `step`. HH7 measures it on synthetic sources. Provisional here (fake sources, no transport). Re-measured after #631. Final value comes from the live route packet: its transport timeout plus the #619 source bounds |
| `max_step_interval` | Longest gap between step starts on a healthy host | Derived: `max(step_interval_s, max_step_duration) + scheduler_slack_s` (fixed-rate schedule, §3.2). HH7 measures it |
| `ping_timeout` | Send timeout of `HeartbeatPinger` (`timeout_s`) | The #637 build. Consumed here |
| `P` | Minimum spacing between runtime pings (`period_s`) | Coordinator (3) at this card's freeze, under (a) and (b) |
| `T` | IRM heartbeat timeout of the runtime integration | Coordinator (3) under HB OQ-H1 (lean 1 min). The final T for HB-L1 is set at this card's freeze. Joshua sets it in IRM (HB OA-H1) |
| `notifier_interval_s`, `max_round_duration`, `max_notifier_loop_interval`, `P_n`, `T_n` | The same quantities for the notifier loop | As above. HH7 measures `max_round_duration` at a declared due-job count (OQ-HOST-2) |
| `ingestion_allowance_s`, `chain_s` | IRM ingestion allowance; `chain_s` = 90 s, the SMS-to-call fail threshold (HB §0.5 item 3) | Coordinator (3) at freeze. HB-L1 measures ingestion |

**Threshold (HB `:136` and `:156`, restated without change).** Runtime side:
- (a) `ping_timeout < P`
- (b) `P + max_step_interval + max_step_duration + ping_timeout < T`
- (c) `T + ingestion_allowance_s + chain_s < PROTECTION_PERIOD` (15 min, `book_protection_owner.py:24`)

The notifier side is the same, with `P_n`, `max_notifier_loop_interval`, `max_round_duration` and `T_n`.

Why (b) keeps a healthy receiver alive: after a send, the next send needs P to pass and then a mark. Marks come at step ends, at most `max_step_interval + max_step_duration` apart, and a send arrives within `ping_timeout`. Consecutive arrivals are therefore less than T apart.

*Illustrative only, not a selection:* T = 60 s, `ping_timeout` = 5 s, `step_interval_s` = 10 s, `max_step_duration` = 10 s and slack 1 s give `max_step_interval` = 11 s, so (b) needs P < 34 s. With 30 s of ingestion allowance, (c) gives 60 + 30 + 90 = 180 s, below 900 s.

## §3 — Design

1. **Binding (config as code; AGENTS.md `:229-238`).** `BookHostBinding` is a frozen dataclass in `book_host.py`.
   - Fields: `step_interval_s`, `max_step_duration_s`, `notifier_interval_s`, `max_round_duration_s`, `scheduler_slack_s`, `runtime_timeout_s` (T), `notifier_timeout_s` (T_n), `ingestion_allowance_s` and `chain_s`. It also holds the two ping bindings in HB §3.7's shape, `{"secret_ref", "period_s", "timeout_s"}`, with references only.
   - `validate_binding` runs at construction, the consumption boundary. It refuses non-finite or non-positive values and any breach of §2 (a)-(c) on either side. Each refusal names the constraint and the side, never a URL.
   - `PROTECTION_PERIOD` is imported from its owner, not restated.
   - `binding_digest` is SHA-256 over canonical JSON, so validation and later activation name the same configuration.
   - `FROZEN_BINDING` holds the values recorded at the freeze (§12).
   - The binding reads no environment. Pingers are built only through #637's `build_pingers`.
2. **Runtime thread.** Steps start on a fixed-rate schedule: the next start is the previous start plus `step_interval_s`. After an overrun, the next step starts at once, with no catch-up burst. Each step calls `step_with_heartbeat(loop, runtime_pinger, now=wall_clock(), read_status=read_status)`. The caller binds `read_status` to the owner's `status()`.
3. **Notifier thread.** A second thread runs `notifier_round_with_heartbeat(notifier, notifier_pinger)` at `notifier_interval_s`, under the same fixed-rate rule.
   - The caller builds the notifier with `read_incidents` bound to the owner's path (the read-only C-1 seam) and with the host's clock (§0.5 item 5).
   - The notifier loop function takes only the notifier, its pinger and its cadence, so the live packet can move it into its own process without editing it (OQ-HOST-1).
   - While the host runs, no lock, queue or join is shared between the two threads.
4. **Exceptions (OQ-HOST-3).** A step or round that raises is not progress, and the wrapper sets no mark. The host records the exception class and a count, never the message, and continues at the next scheduled start. It never retries within a slot, never touches owner state, and never turns an exception into a mark. A persistent failure therefore expires that side's receiver after its T.
5. **Stop and counters.** `stop()` sets one event. Each thread finishes its current call and exits. The join waits a bounded time and reports any thread that has not exited (for example, a hung step) instead of blocking. Per side, the host keeps in-memory counters: calls started, raises by class, the largest observed duration and the largest observed start gap. It has no restart logic: process supervision is R-H's.
6. **Imports.** `book_host` imports `book_heartbeat`, `PROTECTION_PERIOD` and the standard library only. The notifier and the loop are duck-typed. It imports nothing from `daemon.py`, `__main__`, the CLI, `book_incident_notifier`, the IRM channel module, arm or config-write modules, or broker or dispatch transports. It reads no `dry_run` or `armed_until`. It is not added to `_ENTRYPOINTS`.

## §4 — Hypothesis and falsifier

**H:** A host that runs the loop and the notifier on separate threads, through the #637 wrappers, at cadences validated against HB `:136`, keeps both fake receivers alive while both sides progress. When one side stalls, raises or hangs, only that side's receiver expires. The step cadence stays within `max_step_interval` whatever the notifier does.
**Falsifier:** any of the following.
- `run_once` runs on the runtime thread, or a raising, hanging or slow notifier pushes a step start gap above `max_step_interval`.
- A binding that breaks (a), (b) or (c) on either side is accepted.
- A healthy synthetic host expires either receiver, or a stall on one side expires the other side's receiver.
- A mark follows a step or round that raised.
- A measured step duration or start gap on synthetic sources exceeds the declared value.
- `book_host` has an import path to `daemon.py`, the CLI, deploy, arm, config-write, a broker or dispatch transport, or the notifier module, or it appears in `_ENTRYPOINTS`.
- A URL appears in a log, `repr`, counter or exception.

## §5 — Files

**Allowed:**
- `ops/c1_signal_daemon/book_host.py` (new): `BookHostBinding`, `validate_binding`, `binding_digest`, `FROZEN_BINDING`, `BookHost`.
- `tests/ops/test_book_host.py` (new): HH1-HH8.
- This card: the §12 freeze record and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- Registration and route wiring: `ops/c1_signal_daemon/daemon.py`, `build_loop`, `ops/c1_signal_daemon/__main__.py`, the daemon CLI and any HTTP endpoint. Registration belongs to the live route packet (R-A1/R-H; spec `:144`, `:157`).
- `ops/c1_signal_daemon/book_evaluate_loop.py` (#631), `book_runtime.py`, `book_protocol.py`, `heartbeat.py`, `http_status.py`, `evaluate_loop.py`.
- `ops/c1_rail/book_account_owner.py`, whose edit order is #628, then GC-5, then TB-I3 S2 (#633 `:250`), and every other `ops/c1_rail/book_*.py`.
- `ops/c1_signal_daemon/book_heartbeat.py`, `book_heartbeat_live_check.py` and `tests/ops/test_book_heartbeat.py` (#637).
- `ops/c1_rail/book_incident_notifier.py` and its tests (#628); `book_incident_grafana_irm.py` (#635).
- `deploy/**`, including `deploy/c1_signal_daemon/Dockerfile`, plus `.dockerignore`, `fly.toml`, `tests/ops/test_c1_signal_daemon_image_manifest.py` and every other image-manifest test or script. The Dockerfile `COPY` and the `_ENTRYPOINTS` entry go with the live packet when `book_host` becomes an entrypoint.
- Arming: `ops/c1_rail/c1_rail_arm.py`, `write_volume_config.py`, `operator_keys.json`, `.env*`, `/data`.
- Locked and risk surfaces: `core/dd_protection.py`, `core/firm_rules.py`, `core/strategies/**`, every `*.pine`, and `ops/c1_signal_daemon/ports/**` (never read).
- Governance: `AGENTS.md`, `STATE.md`, `PIPELINES.md`, `REPO_MAP.md`, `docs/adr/**`, `docs/spec/**` (HR included), the umbrella, the checklist, and the #633, #637, #628, #631 and #615 cards.
- `.claude/settings.json`, `scripts/gates.yml`. Existing tests are not edited.

## §6 — Red-first tests and return taxonomy

The tests live in `tests/ops/test_book_host.py`. Run the file at the base revision first and record the failure (the module is absent), then implement.

**Fixtures:**
- A real `FourLegEvaluateLoop` on synthetic sources, as in `test_book_loop_continuation.py`.
- A real #628 `IncidentNotifier` with `FakeChannel`, its `read_incidents` bound to the owner's path.
- #637 `HeartbeatPinger`s sending to loopback fake receivers, R (runtime) and N (notifier). Their `env:` references are set by the test to `http://127.0.0.1` with #637's test-only flag.
- Fake clocks for expiry. Real monotonic time only in HH7, at test-scale cadences.

| ID | Test | Pass | Criterion / basis |
|---|---|---|---|
| HH1 | `test_step_and_notifier_run_on_separate_threads` | Spies record different thread ids. `run_once` never runs on the runtime thread. No lock, queue or join is shared while running | (a); HB `:73` |
| HH2 | `test_raising_notifier_leaves_step_cadence_bounded` | `run_once` raises `NotifierStoreError` every round; separately, `read_incidents` raises (HQ9's store-loss path). Step start gaps stay within `max_step_interval`. R never expires. N expires after T_n. The class is counted and no message is logged | (a); HB `:73`, `:74`, HQ9 `:226` |
| HH3 | `test_hung_notifier_leaves_step_cadence_bounded` | `run_once` blocks on a held event. Step start gaps stay within `max_step_interval`. R never expires. N expires after T_n. `stop()` reports the hung thread within its bounded join | (a); HB `:73` |
| HH4 | `test_binding_validator_refuses_constraint_breaches[a,b,c × runtime,notifier]` | Each breach is refused, naming the constraint and the side. Equality is refused because each constraint is strict. Non-finite and non-positive values are refused. A valid binding passes, and its digest is stable | (b); HB `:136`, `:156` |
| HH5 | `test_hq6_through_host_notifier_stalled_runtime_alive` | N expires after T_n; R does not | (c); HB HQ6 `:223` |
| HH6 | `test_hq7_through_host_runtime_stalled_notifier_alive` | `step` blocks, or stepping stops. R expires after T; N does not. The owner's `incidents` and `status()` compare equal before and after the expiry | (c); HB HQ7 `:224` |
| HH7 | `test_measured_step_and_round_within_declared_bounds` | At least 200 steps and 200 rounds on synthetic sources, on real monotonic time at test-scale cadences. The largest step duration is at most `max_step_duration_s`. The largest start gap is at most `max(step_interval, max_step_duration) + slack`. The round duration at the declared due-job count is at most `max_round_duration_s`. The count, maximum and p99 are printed for the return | (d); P4 |
| HH8 | `test_host_import_and_scope_boundary` | An AST check finds only §3.6's imports, no `dry_run` or `armed_until`, and no `book_host` in `_ENTRYPOINTS`, `daemon.py` or `__main__.py` | §3.6; §5 |

**Return taxonomy.**
- DONE: every red-first test is recorded red at base and green at head; the §7 regression, `test-ops` and `check` are green with records cited; the diff stays inside §5.
- DONE_WITH_CONCERNS: the outcome is established, with a disclosed baseline limitation that is unrelated to the patch and reproduced on unmodified origin/main.
- NEEDS_CONTEXT: a missing input, a contradicted fact (for example, a merged #637 API that differs from §0.5 item 3) or conflicting owner text. Name it.
- BLOCKED: a needed edit outside §5, or an environment failure that the launcher cannot repair.

The coordinator's verdict on the returned build is RESOLVED (every HH test and every §7 check holds) or FALSIFIED (the failing items are named and returned to the executor).

A failed required criterion is never DONE_WITH_CONCERNS. The worker's DONE is not qualification. Registration, HB-L1, HB-L2 and the host-kill drill remain.

## §7 — Acceptance checks (the worker runs them; the coordinator re-runs them at the returned head)

```
python -I scripts/fp.py doctor
python -I scripts/fp.py python -m pytest tests/ops/test_book_host.py              # red at base, green at head
python -I scripts/fp.py python -m pytest tests/ops/test_book_heartbeat.py tests/ops/test_book_incident_notifier.py tests/ops/test_book_loop_continuation.py tests/ops/test_c1_signal_daemon_evaluate_loop.py tests/ops/test_c1_signal_daemon_image_manifest.py
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
git diff --stat origin/main...HEAD                                               # §5 allowed files only
```

Report the command, interpreter, head and each printed `record.json` (`status: completed`, exit 0, `source_stable`). Disclose any pre-existing failure with its reproduction on unmodified origin/main (AGENTS.md `:222-226`). These live checks are out of scope here: HB-L1 and HB-L2 (operator-run, HB §6.3) and the host-kill drill (#615 RH3, `2193fb2:156`).

## §8 — Out of scope and overlaps

**Out of scope:**
- Route integration, and daemon registration (`daemon.py`, `build_loop`, `__main__`, the CLI).
- Deploy, the image `COPY` and `_ENTRYPOINTS`; arming and `dry_run`; any order path, broker or dispatch transport.
- Process supervision, restart, and the notifier's final process placement (R-H; OQ-HOST-1).
- HB-L1, HB-L2 and the host-kill drill.
- HB's operating bracket at planned stops (HB OQ-H2, #615).
- A per-round job cap in #628 (OQ-HOST-2) and the dot path (HB §3.6).

**Overlaps:**
- **#633:** not amended (§0.5 item 2).
- **No second loop runner.** The live route packet registers `book_host` and writes no step loop of its own.
- **The legacy `GET /` heartbeat** is not extended (§0.5 item 7).
- **#631** changes `step` to poll all four sources and then check health (`76110a9:106-118`). That changes `max_step_duration`, so HH7 is re-run after #631 merges. The two cards share no file.
- **Timing owners** each declare their bound once: #631 the step body, #619 the source backoff, and the route transport its dispatch timeout. This card sums declared bounds and does not re-derive them.

## §9 — Decisions and open questions

**Recorded:** Joshua's 2026-10-03 authorization to write this card (Status; §0.5 item 1).

**Proposed (coordinator (3) confirms at freeze):** D-H1, a separate card rather than a #633 amendment (§0.5 item 2). D-H2, the notifier on its own thread, with a loop function that does not depend on its process (§3.3). D-H3, continue after an exception without marking (§3.4). D-H4, fixed-rate scheduling (§3.2).

**OPEN:**
- **OQ-HOST-1** (coordinator (3)). Notifier placement. Lean: a thread now. A separate process would let the notifier page committed incidents while the runtime process hangs; decide that with the live packet under R-H.
- **OQ-HOST-2** (coordinator (3); #628 owner). How to bound `max_round_duration` (§0.5 item 6). Options:
  - (i) The binding declares `max_due_jobs_per_round` as a recorded assumption, and HH7 measures at that count. The bound is not sound beyond it.
  - (ii) The #628 owner adds a per-round job cap.
  - (iii) Raise T_n.

  Lean: (ii), routed to the #628 owner, with (i) as the interim. Separately, route HB `:156`'s undercount to the #637 owner.
- **OQ-HOST-3** (coordinator (3)). After an exception, continue at the next start without marking (lean), or stop that thread. Stopping turns any transient error into a page and needs restart logic that is out of scope here.
- **OQ-HOST-4** (coordinator (3), HB OQ-H1). The frozen values: `step_interval_s`, `notifier_interval_s`, `scheduler_slack_s`, the declared maximum durations, P, P_n, T, T_n and `ingestion_allowance_s`. Lean: T = T_n = 1 min, with P and P_n set under (b).
- **OQ-HOST-5** (coordinator (3), or Joshua). The umbrella's TB-I3 row depends on "TB-S3 accepted, TB-I1" (`:232`). The 2026-10-02 ruling narrowed TB-I1 for the interlock card only (#633 `:10`). Coordinator (3) records whether the 2026-10-03 approval covers this card's dispatch the same way, or asks Joshua.
- **OQ-HOST-6** (coordinator (3)). The executor. The umbrella routes TB-I3 to Codex local (`:232`); HB routes its build to Opus/CC (HB §11). It is not GLM either way (§11).

## §10 — Audit hooks

```bash
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md
gh pr view 628 --json state,mergeCommit                     # P1
gh pr view 637 --json state,headRefOid                      # P2 (card); §12 records the build's merge commit
rg -n '^\s*(from|import)\s' ops/c1_signal_daemon/book_host.py   # Expected: book_heartbeat, book_protection_owner, stdlib only
rg -n 'dry_run|armed_until' ops/c1_signal_daemon/book_host.py   # Expected: no match
rg -n 'book_host' ops/c1_signal_daemon/daemon.py ops/c1_signal_daemon/__main__.py tests/ops/test_c1_signal_daemon_image_manifest.py deploy   # Expected: no match
rg -n 'BookAccountOwner\(' ops                              # Expected: the class definition only
git diff --stat origin/main...HEAD
```

## §11 — GLM eligibility

**Not GLM-eligible.** Under `C:\Users\joshu\.claude\CLAUDE.md:15`, work stays with Opus "for security, secrets … or production incidents". This card places the safety monitor of the incident path and builds pingers from secret references. The executor is open (OQ-HOST-6).

## §12 — Dispatch record

- **Status:** DRAFT. Writing was authorized 2026-10-03 (§0.5 item 1). After P1, P2 and P4, coordinator (3) freezes the card and records here: the frozen revision; the #628 merge commit and the #637 build merge commit; the merged `book_heartbeat.py` signatures; the frozen binding values and their `binding_digest`, which HB §12 also records before HB-L1; and every moved anchor. Known drift to re-read: HB cites HR at `a5ca41e` (`:34`, `:57`, `:59`, `:61`, `:143`), which are `:36`, `:61`, `:63`, `:65` and `:233` at `ebe5c0b`.
- **Executor (planned):** one worker, seat worker, in a worktree under `.claude/worktrees/`, on a pushed branch. No PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.
