# TB-I3-HOST: heartbeat host wiring for the book runtime and notifier (build card, synthetic scope)

**Date:** 2026-10-03.
**Status:** **DRAFT.** Writing authorized by Joshua, direct to coordinator (3), 2026-10-03 about 17:19Z: "I approve your recommendations". He was replying to a list that included "TB-I3-HOST: a new, synthetic-only card for heartbeat host wiring. I recommend yes; no daemon.py, deploy or arming." That approval grants only what it states (AGENTS.md `:34`): writing. Coordinator (3) freezes this card after P1, P2 and P7 (§1). Dispatch: OQ-HOST-5 (b) APPROVED (Joshua, direct to coordinator (3), 2026-10-03 at about 18:04Z: "I approve the dispatch"). OQ-HOST-5 (a), narrowing TB-I1 for this card, awaits Joshua's confirmation. Dispatch still needs the freeze, (a) and coordinator (3)'s dispatch record (§12). Nothing here is dispatched.
**Base:** origin/main `ebe5c0b`. Other revisions read: #637 at `origin/claude/dmon-heartbeat-card` `63a733a` (DRAFT); #628 at `origin/claude/book-incident-notifier` `6e57fda` (OPEN); #633 at `origin/claude/tb-i3-card` `4dce572` (DRAFT); #631 at `origin/claude/ra2-offline-card` `76110a9` (DRAFT); #615 at `origin/claude/t13-first-session-card` `2193fb2` (PROPOSED); #635 at `origin/claude/dmon-grafana-binding-card` `6a0618e` (DRAFT; host-wiring exclusion `:244`). Branch anchors hold only at those heads. **HB** means the #637 card, `docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md`, at `63a733a`. Its threshold constraints are at `:136` there (`:134` at `ec6e220`).
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
  - "HH7's measured step and round figures, at the test binding's max_jobs_per_round, are reported with their record.json and stay within the test binding's declared bounds; FROZEN_BINDING passes validate_binding (HH4)"
```

## §0 — Read first (report before writing code; otherwise `NEEDS_CONTEXT`)

| Input | Where | Read |
|---|---|---|
| Heartbeat card (HB) and its build | `git show 63a733a:docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md`; at dispatch, the merged `ops/c1_signal_daemon/book_heartbeat.py` | §0.5 item 7 `:73`, item 8 `:74`; P1-P9 `:97-105`; §3.1 `:129`; §3.3 constraints `:136`; §3.7 `build_pingers` `:150`; §3.9 `:153-156`; HQ6 `:223`, HQ7 `:224`, HQ9 `:226`. At dispatch, the merged signatures of `HeartbeatPinger`, `step_with_heartbeat`, `notifier_round_with_heartbeat` and `build_pingers` |
| #628 notifier | merged `ops/c1_rail/book_incident_notifier.py` (`6e57fda` at draft) | `MAX_OUTSTANDING_PUBLISHES` `:66`; `NotifierStoreError` `:105`; `publish_timeout_s` `:209`; `IncidentNotifier.__init__` `:266-279` (`read_incidents`, `clock`); journal `timeout=5` `:304`; `run_once` `:425-436`; `liveness()` `:438-445`; `publish_due` `:447-461`; `_publish_round` `:463`; `_bounded_publish` `:554` |
| #628 owner accessor | merged `ops/c1_rail/book_account_owner.py` | `read_incidents(path)` (`6e57fda:804-818`, `?mode=ro`, `timeout=5`); `_transaction` `:520-528` (`BEGIN IMMEDIATE`, `timeout=5`); `status()` `:999-1001` (`:982` at `ebe5c0b`) |
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
| Runtime exception model | `ops/c1_signal_daemon/daemon.py:136-145`; `ops/c1_signal_daemon/book_runtime.py:423`; spec `:157` (R-H) | §3.4 default |
| Legacy daemon heartbeat (not edited) | `ops/c1_signal_daemon/heartbeat.py`, `http_status.py`; S2b ADR `docs/adr/2026-08-08-s2b-signal-daemon-build.md:51` | the pull-only `GET /` snapshot |
| Rules | `AGENTS.md` | launcher `:222-226`; *Configuration as code* `:229-238` |

**The report states:** the dispatch revision; the #628 merge commit; the #637 build merge commit and whether the merged `book_heartbeat.py` signatures match HB §3; P7's cap, its name and its merge commit; whether #631 has merged; and every anchor above that moved.

## §0.5 — Clarifications and recorded facts

1. **Authority.** Joshua's 2026-10-03 approval (Status) authorizes writing this card, synthetic scope only. Its terms bind: no `daemon.py`, no deploy and no arming. It does not authorize dispatch or narrow the umbrella's TB-I1 prerequisite; both are Joshua's rulings (OQ-HOST-5). Dispatch, (b), was approved separately (Joshua, direct to coordinator (3), 2026-10-03 at about 18:04Z: "I approve the dispatch"). (a) awaits his confirmation.
2. **A separate card, not a #633 amendment.** #633 forbids `ops/c1_signal_daemon/**` (`:212`) and route wiring in `daemon.py`, `build_loop` or the CLI (`:206`). Its authority is "no route integration" (`:7`), and it is held at a HARD STOP on D-3. Amending it would reopen its freeze.
3. **The API consumed (HB §3, re-read at the merged head).**
   - `step_with_heartbeat(loop, pinger, *, now, read_status)` calls `step`, then `read_status`, then `mark_progress`. An exception propagates unchanged, and no mark is set.
   - `notifier_round_with_heartbeat(notifier, pinger)` calls `run_once` and reads #652's `progress()` (NF6). It marks only when that count increased since its previous call, never on a clock value. HB `:154` still reads the `liveness()` timestamp; that is routed to the #637 owner (coordinator (3)), and a merged wrapper that marks on `liveness()` is NEEDS_CONTEXT.
   - `mark_progress()` returns at once.
   - `build_pingers(runtime_binding, notifier_binding)` refuses a shared reference or a shared resolved URL (H12).

   A different merged API is NEEDS_CONTEXT.
4. **Placement constraint (HB §0.5 item 7, `:73`), enforced here.** The notifier never runs on the runtime loop thread, so a slow publish or a `NotifierStoreError` cannot delay `step`. The one shared resource is the owner DB file lock (§3.3), whose wait `max_step_duration` counts. The notifier heartbeat is marked from the notifier's own loop (HB `:154`). HH1-HH3 test this.
5. **The notifier side marks on `progress()`, not on the clock (NF6).** #652's `progress()` is a per-instance count of `run_once` calls that completed without raising and without a loud class-U deferral (NF3). A loud pass therefore sets no mark, by design, and N expires after T_n under HR's owner reading, condition (4) (`:71`). A frozen or backward notifier clock no longer stops marks, as it did when marks followed the `liveness()` timestamp (`6e57fda:436`). The caller still gives the notifier a clock that advances between rounds (§3.3): it sets due times and backoff, and a backward step loosens #652's NF2 retry-spacing bound. The notifier's clock need not be the host's.
6. **Round duration has no job cap (OQ-HOST-2 resolves it).** `publish_due` runs one round per due pending job, in sequence (`6e57fda:447-461`). Each channel publish waits up to `publish_timeout_s`, which defaults to 10 s (`:209`). Each journal transaction may wait 5 s for the lock (`:304`), and `read_incidents` may wait 5 s on the owner DB (§3.3). A provider that answers just inside the timeout frees its slot each time, so `MAX_OUTSTANDING_PUBLISHES` (`:66`) does not bound the round. `max_round_duration` therefore grows with due jobs × channels × `publish_timeout_s`, plus journal time. HB `:156` counts only timeout × channels, which undercounts.
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
| P4 | Joshua's ruling under OQ-HOST-5: (a) whether the TB-I1 prerequisite is narrowed for this card; (b) dispatch | (b) **APPROVED** (Joshua, direct to coordinator (3), 2026-10-03 at about 18:04Z: "I approve the dispatch"). (a) **OPEN**, awaiting Joshua's confirmation | Dispatch |
| P5 | Coordinator (3) freeze record (§12) | OPEN | Dispatch |
| P6 | #631 merged | OPEN (DRAFT; freezes when #619 merges) | Not dispatch. If #631 merges after this build, HH7 is re-run and `max_step_duration` is re-declared |
| P7 | #652 merged: NF1 cap, NF4 ingestion bound, NF5 pending fetch, NF6 `progress()` (OQ-HOST-2) | **OPEN** (#652 DRAFT, `origin/claude/notifier-round-cap-card`) | Freeze |

Freeze needs P1, P2, P7 and the OQ-CAP-3 choice (§9). Dispatch needs the freeze (P3, P5) and P4.

## §2 — P4 inputs and the threshold

| Input | Meaning | Supplied by, and when |
|---|---|---|
| `step_interval_s` | Target spacing between step starts | This card's binding. Frozen at this card's freeze |
| `max_step_duration` | Longest `step` plus `read_status` on a healthy host | Declared at freeze as the sum of declared bounds: four source polls, owner checks, any dispatch inside `step`, and up to 5 s of owner DB busy wait per owner transaction in `step` and `read_status` (§3.3). HH7 measures it on synthetic sources. Provisional here (fake sources, no transport). Re-measured after #631. Final value comes from the live route packet: its transport timeout plus the #619 source bounds |
| `max_step_interval` | Longest gap between step starts on a healthy host | Derived: `max(step_interval_s, max_step_duration) + scheduler_slack_s` (fixed-rate schedule, §3.2). HH7 measures it |
| `ping_timeout` | Send timeout of each `HeartbeatPinger` (`timeout_s`) | The #637 build exposes it as the constructor `timeout_s` (HB `:100`); this card's binding sets the value per side (HB `:150`). Coordinator (3) freezes the runtime and notifier values at this card's freeze, under (a) |
| `P` | Minimum spacing between runtime pings (`period_s`) | Coordinator (3) at this card's freeze, under (a) and (b) |
| `T` | IRM heartbeat timeout of the runtime integration | Coordinator (3) under HB OQ-H1 (lean 1 min). The final T for HB-L1 is set at this card's freeze. Joshua sets it in IRM (HB OA-H1) |
| `notifier_interval_s`, `max_round_duration`, `max_notifier_loop_interval`, `P_n`, `T_n` | The same quantities for the notifier loop | As above. `max_round_duration` is declared at freeze as #652's NF8 bound on one `run_once`: `W_o + T_parse(n) + (2 + 2·k·c)·W_j + k·c·publish_timeout_s`. W_o is the owner DB busy wait in `read_incidents` (5 s). T_parse(n) is the declared time to read and parse n ≤ `max_retained_incidents` rows (NF4). W_j is each journal transaction's lock wait (5 s, `6e679cc:304`): the poll, the pending fetch and, per (job, channel), admission and close. k is P7's cap (`max_jobs_per_round`, NF1); c is the channel count. A cap alone bounds neither `poll`, which parses every historical row with `INSERT OR IGNORE` (`6e679cc:396-421`), nor the pending fetch (`:455-459`). HH7 measures it at k and n = `max_retained_incidents`. OQ-CAP-3 (§9) |
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
   - Fields: `step_interval_s`, `max_step_duration_s`, `notifier_interval_s`, `max_round_duration_s`, `max_jobs_per_round`, `scheduler_slack_s`, `runtime_timeout_s` (T), `notifier_timeout_s` (T_n), `ingestion_allowance_s` and `chain_s`. It also holds the two ping bindings in HB §3.7's shape, `{"secret_ref", "period_s", "timeout_s"}`, with references only; each `timeout_s` is this card's `ping_timeout` (§2).
   - `max_jobs_per_round` is a positive integer equal to P7's cap. `BookHost` refuses, at construction, a notifier whose configured cap differs; the cap's merged name is recorded at freeze (§12).
   - `validate_binding` runs at construction, the consumption boundary. It refuses non-finite or non-positive values and any breach of §2 (a)-(c) on either side. Each refusal names the constraint and the side, never a URL.
   - `PROTECTION_PERIOD` is imported from its owner, not restated.
   - `binding_digest` is SHA-256 over canonical JSON, so validation and later activation name the same configuration.
   - `FROZEN_BINDING` holds the values recorded at the freeze (§12).
   - The binding reads no environment. Pingers are built only through #637's `build_pingers`, in tests too (§6), so H12 always applies.
2. **Runtime thread.** Steps start on a fixed-rate schedule: the next start is the previous start plus `step_interval_s`. After an overrun, the next step starts at once, with no catch-up burst. Each side's scheduler takes an injected `monotonic()` (seconds) and `wait(seconds)`; production binds them to `time.monotonic` and the stop event's `wait`. Start gaps and durations are measured on `monotonic`. Each step calls `step_with_heartbeat(loop, runtime_pinger, now=wall_clock(), read_status=read_status)`, with `wall_clock` injected. The caller binds `read_status` to the owner's `status()`.
3. **Notifier thread.** A second thread runs `notifier_round_with_heartbeat(notifier, notifier_pinger)` at `notifier_interval_s`, under the same fixed-rate rule.
   - The caller builds the notifier with `read_incidents` bound to the owner's path (the read-only C-1 seam) and with a clock that advances between rounds (§0.5 item 5).
   - The notifier loop function takes only the notifier, its pinger and its cadence, so the live packet can move it into its own process without editing it (OQ-HOST-1).
   - No Python-level lock, queue or join is shared between the two threads; they share only the stop event (§3.5). The owner DB file lock is the one shared resource: `read_incidents` opens the DB read-only (`book_account_owner.py` `6e57fda:804-818`, `timeout=5`), while owner transactions in `step` and `status()` take `BEGIN IMMEDIATE` (`:520-528`, `timeout=5`) without WAL. Either side can delay the other by up to that 5 s busy timeout; §2 counts it.
4. **Exceptions (OQ-HOST-3).** A step or round that raises is not progress, and the wrapper sets no mark. The host records the exception class and a count, never the message. It never retries within a slot, never touches owner state, and never turns an exception into a mark.
   - Runtime side (default): the runtime thread stops after any exception from `step` or `read_status`, and R expires after T and pages. The legacy loop also ends on an exception (`daemon.py:136-145`). An exception inside `step` can follow a committed fact before adapter feedback (`book_runtime.py:423`), adapters hold state in memory, and recovery is a restart that restores state first (R-H, spec `:157`). Continuing instead needs the `book_runtime.py` owner's evidence that re-entering `step` after any exception equals restart replay.
   - Notifier side: the thread continues at the next scheduled start, so a persistent failure expires N after T_n.
5. **Stop and counters.** `stop()` sets one event. Each thread finishes its current call and exits. The join waits a bounded time and reports any thread that has not exited (for example, a hung step) instead of blocking. Per side, the host keeps in-memory counters: calls started, raises by class, the largest observed duration and the largest observed start gap. It has no restart logic: process supervision, including whether a stopped runtime thread ends the process, is R-H's.
6. **Imports.** `book_host` imports `book_heartbeat`, `PROTECTION_PERIOD` and the standard library only. The notifier and the loop are duck-typed. It imports nothing from `daemon.py`, `__main__`, the CLI, `book_incident_notifier`, the IRM channel module, arm or config-write modules, or broker or dispatch transports. It reads no `dry_run` or `armed_until`. It is not added to `_ENTRYPOINTS`.
   - The ban is transitive. Forbidden modules: `c1_signal_daemon.daemon`, `.__main__`, `.listener_client`; `c1_rail.book_incident_notifier`, `.book_incident_grafana_irm`, `.c1_rail_arm`, `.write_volume_config`, `.c1_rail_listener`, `.c1_rail_http_server`, `.crosstrade_payload`. At `ebe5c0b`, importing `book_protection_owner` loads 9 project modules, none of them forbidden.

## §4 — Hypothesis and falsifier

**H:** A host that runs the loop and the notifier on separate threads, through the #637 wrappers, at cadences validated against HB `:136`, keeps both fake receivers alive while both sides progress. When one side stalls, raises or hangs, only that side's receiver expires. The step cadence stays within `max_step_interval` whatever the notifier does; any owner DB lock wait it causes is inside `max_step_duration` (§3.3).
**Falsifier:** any of the following.
- `run_once` runs on the runtime thread, or a raising, hanging or slow notifier pushes a step start gap above `max_step_interval`.
- A binding that breaks (a), (b) or (c) on either side is accepted, or a notifier whose cap differs from `max_jobs_per_round` is accepted.
- A healthy synthetic host expires either receiver, or a stall on one side expires the other side's receiver.
- A mark follows a step or round that raised, or, under the runtime default (§3.4), `step` runs again after a `step` or `read_status` that raised.
- A measured step duration or start gap on synthetic sources exceeds the declared value.
- `book_host` imports a §3.6 forbidden module, directly or transitively, or it appears in `_ENTRYPOINTS`.
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
- #637 `HeartbeatPinger`s sending to loopback fake receivers, R (runtime) and N (notifier). Their `env:` references are set by the test to `http://127.0.0.1` with #637's test-only flag. They are built through `build_pingers` only (§3.1). If the merged `build_pingers` cannot target loopback receivers, the return is NEEDS_CONTEXT; tests never construct a `HeartbeatPinger` directly.
- One fake clock per side drives that side's `monotonic`, `wait`, pinger and receiver expiry; the notifier's `clock` reads the notifier side's. The fake `wait` advances its side's clock without sleeping, so start gaps are deterministic. Real monotonic time only in HH7.

| ID | Test | Pass | Criterion / basis |
|---|---|---|---|
| HH1 | `test_step_and_notifier_run_on_separate_threads` | Spies record different thread ids for `step` and `run_once`. `run_once` never runs on the runtime thread, and `step` never runs on the notifier thread | (a); HB `:73` |
| HH2 | `test_raising_notifier_leaves_step_cadence_bounded` | `run_once` raises `NotifierStoreError` every round; separately, the notifier is built with an injected `read_incidents` that raises (HQ9's store-loss path) while the owner DB stays readable. On the runtime side's fake clock, step start gaps stay within `max_step_interval`, and at least 50 steps finish before a 10 s real-time deadline. R never expires. N expires after T_n. The notifier thread continues; the class is counted and no message is logged | (a); HB `:73`, `:74`, HQ9 `:226` |
| HH3 | `test_hung_notifier_leaves_step_cadence_bounded` | `run_once` blocks on a held event. On the runtime side's fake clock, step start gaps stay within `max_step_interval`, and at least 50 steps finish before a 10 s real-time deadline. R never expires. N expires after T_n. `stop()` reports the hung thread within its bounded join | (a); HB `:73` |
| HH4 | `test_binding_validator_refuses_constraint_breaches[a,b,c × runtime,notifier]` | Each breach is refused, naming the constraint and the side. Equality is refused because each constraint is strict. Non-finite and non-positive values are refused. A valid binding passes, and its digest is stable. `FROZEN_BINDING` passes. `BookHost` refuses a notifier whose cap differs from `max_jobs_per_round` | (b); HB `:136`, `:156` |
| HH5 | `test_hq6_through_host_notifier_stalled_runtime_alive` | N expires after T_n; R does not | (c); HB HQ6 `:223` |
| HH6 | `test_hq7_through_host_runtime_stalled_notifier_alive` | `step` blocks; or `step` raises once and the runtime thread stops with no second `step` (§3.4); or stepping stops. R expires after T; N does not. The owner's `incidents` and `status()` compare equal before and after the expiry | (c); HB HQ7 `:224` |
| HH7 | `test_measured_step_and_round_within_declared_bounds` | On a test binding at test-scale cadences (not `FROZEN_BINDING`, which HH4 validates), on real monotonic time: at least 200 steps on synthetic sources and 200 rounds. The notifier journal is seeded with history up to the test `max_retained_incidents`, and `read_incidents` returns that many rows. At least 20 rounds have `max_jobs_per_round` jobs due, on a channel stub that holds every publish to the test `publish_timeout_s`. Asserted against the test binding: the largest step duration is at most `max_step_duration_s`; the largest start gap is at most `max(step_interval_s, max_step_duration_s) + scheduler_slack_s`, with slack at least 0.1 s (Windows timers resolve about 15.6 ms); the largest round is at most `max_round_duration_s`, declared by the NF8 formula (§2) at the test values. The count, maximum and p99 are printed for the return, not asserted | (d); P4 |
| HH8 | `test_host_import_and_scope_boundary` | An AST check finds only §3.6's direct imports and no `dry_run` or `armed_until`. A fresh `sys.executable` subprocess that imports `book_host` loads no §3.6 forbidden module. No `book_host` in `_ENTRYPOINTS`, `daemon.py` or `__main__.py` | §3.6; §5 |

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
- Process supervision, restart, whether a stopped runtime thread ends the process, and the notifier's final process placement (R-H; OQ-HOST-1).
- HB-L1, HB-L2 and the host-kill drill.
- HB's operating bracket at planned stops (HB OQ-H2, #615).
- Building the #628 per-round job cap (P7; the #628 owner's) and the dot path (HB §3.6).

**Overlaps:**
- **#633:** not amended (§0.5 item 2).
- **No second loop runner.** The live route packet registers `book_host` and writes no step loop of its own.
- **The legacy `GET /` heartbeat** is not extended (§0.5 item 7).
- **#631** changes `step` to poll all four sources and then check health (`76110a9:106-118`). That changes `max_step_duration`, so HH7 is re-run after #631 merges. The two cards share no file.
- **Timing owners** each declare their bound once: #631 the step body, #619 the source backoff, and the route transport its dispatch timeout. This card sums declared bounds and does not re-derive them.

## §9 — Decisions and open questions

**Recorded:** Joshua's 2026-10-03 authorization to write this card (Status; §0.5 item 1).

**Proposed (coordinator (3) confirms at freeze):** D-H1, a separate card rather than a #633 amendment (§0.5 item 2). D-H2, the notifier on its own thread, with a loop function that does not depend on its process (§3.3). D-H3, after an exception the runtime thread stops and the notifier thread continues, neither marking (§3.4). D-H4, fixed-rate scheduling (§3.2).

**OPEN:**
- **OQ-HOST-1** (coordinator (3)). Notifier placement. Lean: a thread now. A separate process would let the notifier page committed incidents while the runtime process hangs; decide that with the live packet under R-H.
- **OQ-HOST-2 — RESOLVED in drafting; coordinator (3) confirms at freeze.** How to bound `max_round_duration` (§0.5 item 6). The host cannot bound it inside §5: `publish_due` walks every due pending job in the journal (`6e57fda:447-461`), and pending jobs persist across rounds until closed, so the due set is not a host input. Resolution: the #628 owner adds a per-round job cap (P7, which blocks freeze). The binding declares it as `max_jobs_per_round` (§3.1), and HH7 measures at it. Raising T_n bounds nothing. Separately, HB `:156`'s undercount is routed to the #637 owner.
- **OQ-HOST-3** (coordinator (3); `book_runtime.py` owner). Whether the runtime thread may continue after an exception instead of stopping (§3.4 default). Only on that owner's evidence that re-entering `step` after any exception equals restart replay. The notifier side continues.
- **OQ-HOST-4** (coordinator (3), HB OQ-H1). The frozen values: `step_interval_s`, `notifier_interval_s`, `scheduler_slack_s`, the declared maximum durations, `max_jobs_per_round` (P7's cap), the runtime and notifier `timeout_s` (`ping_timeout`; HB `:100`, `:150`), P, P_n, T, T_n and `ingestion_allowance_s`. Lean: T = T_n = 1 min, with P and P_n set under (b).
- **OQ-HOST-5** (Joshua). Two rulings. (a) Whether the TB-I1 prerequisite is narrowed for this card. The umbrella's TB-I3 row depends on "TB-S3 accepted, TB-I1" (`:232`); TB-I1 is "production BLOCKED pending ratifications" (`:230`). The 2026-10-02 narrowing covers the interlock card only (#633 `:10`). (b) Dispatch. That ruling kept dispatch separate (umbrella `:232`, "Dispatch is a separate decision"; #633 `4dce572:7`, "Dispatch is separate"). The 2026-10-03 approval covers writing only, and a ruling "grants only what it states" (AGENTS.md `:34`). A coordinator cannot waive an umbrella prerequisite. *Ruling (b): APPROVED, Joshua, direct to coordinator (3), 2026-10-03 at about 18:04Z: "I approve the dispatch". (a) is not stated in that approval and awaits Joshua's confirmation (AGENTS.md `:34`).*
- **OQ-HOST-6** (coordinator (3)). The executor. The umbrella routes TB-I3 to Codex local (`:232`); HB routes its build to Opus/CC (HB §11). It is not GLM either way (§11).
- **OQ-CAP-3** (coordinator (3); routed from #652; a freeze item for this card). Choose `publish_timeout_s`, the declared journal lock wait W_j, `max_jobs_per_round` or T_n so that the NF8 `max_round_duration` (§2) is under 30 s, which notifier-side (b) needs at the lean T_n = 60 s (OQ-HOST-4). At #628's defaults it exceeds 30 s even at k = 1: with two channels NF8 gives 55 s before T_parse, or 85 s when a `COMMIT` lock wait doubles W_j.

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

- **Status:** DRAFT. Writing was authorized 2026-10-03 (§0.5 item 1). After P1, P2 and P7, coordinator (3) freezes the card and records here: the frozen revision; the #628 merge commit and the #637 build merge commit; the merged `book_heartbeat.py` signatures; P7's cap name and value; the frozen binding values and their `binding_digest`, which HB §12 also records before HB-L1; and every moved anchor. Known drift to re-read: HB cites HR at `a5ca41e` (`:34`, `:57`, `:59`, `:61`, `:143`), which are `:36`, `:61`, `:63`, `:65` and `:233` at `ebe5c0b`.
- **Executor (planned):** after the freeze and Joshua's OQ-HOST-5 ruling, one worker, seat worker, in a worktree under `.claude/worktrees/`, on a pushed branch. No PR unless the coordinator records one.
- **Pre-dispatch checks:** the first two §10 hooks, run on the frozen file.
