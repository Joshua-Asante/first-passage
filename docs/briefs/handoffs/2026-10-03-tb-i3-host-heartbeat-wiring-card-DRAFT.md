# TB-I3-HOST: heartbeat host wiring for the book runtime and notifier (build card, synthetic scope)

**Date:** 2026-10-03.
**Status:** **FROZEN 2026-10-06 by coordinator (4), card owner**, at the commit that adds this line; base `38fc875ce15336df082c0f7d8eebba9012f4250d`. The §2 HOST-1 values and the §0.5 item 9 clock gates are BOUND at this freeze, as proposed and re-checked CLEAN (PR #713 comment 6008699002). Dispatch follows separately (§12). *As prepared:* **PROPOSED freeze preparation, not FROZEN or dispatched.** Prepared for coordinator (4) (C4), card owner, on 2026-10-05 under the bounded deployment-coordinator handoff. C4 alone records effective freeze after independent Claude review; combined acceptance remains with the parent deployment coordinator. Joshua authorized writing on 2026-10-03 (direct to coordinator (3), about 17:19Z: "I approve your recommendations") and dispatch separately (about 18:04Z: "I approve the dispatch"). OQ-HOST-5(a) is also **APPROVED**: Joshua directly to coordinator (4), 2026-10-03, "yes to OQ-HOST-5 (a)" (relayed in this preparation handoff). No repeat ruling is needed. Effective freeze and the separate §12 dispatch record remain owed. HOST-1 and all timing selections below are **PROPOSED for C4 acceptance**, with the revised clock-observation gate in §0.5.9 still subject to reviewer recheck and C4 binding acceptance.
**Base:** origin/main `38fc875ce15336df082c0f7d8eebba9012f4250d`. The reopened handoff named #701's merge `de0e4129ce48016244812a1837f3d0bb63491809`; subsequent main changes through this base do not change this card's cited timing/monitoring owners. #651 merged `c73d616`; #628 merged `6e679cc`; #652's card merged `af506f7`, frozen `e997223`, and its build #669 merged `d63bf32`; heartbeat card #637 frozen through #695 (`7c23b21`), build #701 merged `de0e412`; #633 card merged `a68e3c6`; #631 card merged `6328521`, its build still absent. **HB** means `docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md` at this base. Current §0 anchors and §12's old→new map supersede the draft's branch anchors. Explicit SHA-qualified historical citations below remain historical, not present-state claims.
**Brief type:** CC handoff. A code build (TDD) inside a named file boundary, synthetic scope only. No live check.
**Parent:** the umbrella's TB-I3 row (`docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md:232`, STUB; footprint `ops/c1_signal_daemon/*`). HR §7 `:233` gives TB-I3 the watchdogs and host activation. HB P7 `:103`, P9 `:105` and P4 `:100` name this card as their pending owner.
**Finding being closed:** No host calls `step_with_heartbeat` or `notifier_round_with_heartbeat`. No production code builds a `BookAccountOwner`: `rg 'BookAccountOwner\(' ops` matches only the class definition (`ops/c1_rail/book_account_owner.py:347`). HR's owner reading, condition (4) (`docs/spec/2026-09-14-tb-s3-halt-resume-contract.md:71`), requires the missed-heartbeat monitor to cover both notifier and runtime liveness before any armed session. HB P4 cannot freeze T or P until this card supplies the cadence and duration inputs.
**Selected outcome:** A composition module, `ops/c1_signal_daemon/book_host.py`. It runs an injected, already-bound `FourLegEvaluateLoop` through `step_with_heartbeat` on a runtime thread. It runs an injected #628 `IncidentNotifier` through `notifier_round_with_heartbeat` on a separate notifier thread. A validated config-as-code binding refuses any threshold set that breaks HB `:137` (a)–(c) on either side, or the notifier-side constraints (d) and (e') (§2). It is qualified by synthetic tests only. Registration in `daemon.py`, deploy and arming belong to the later live route packet (R-A1/R-H).
**Ownership:** One future worker builds it (§11). Coordinator (4), card owner, freezes the card and accepts the build after independent review; the parent deployment coordinator retains combined acceptance. This preparation is a single-card docs PR only. Joshua merges; this preparer neither accepts nor dispatches the build.
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
| Heartbeat card (HB) and its build | HB at this base; merged `ops/c1_signal_daemon/book_heartbeat.py` | HB §0.5 items 7–8 `:73-74`; P1–P10 `:97-106`; §3.1 `:129-130`; §3.3 `:137-139`; §3.7 `:151`; §3.9 `:153-157`; HQ6/HQ7/HQ9/HQ10 `:224-228`. Code: constructor `:114-116`, runtime wrapper `:346-355`, notifier wrapper `:358-369`, `build_pingers` `:379-397` |
| #628 notifier and #669 follow-up | `ops/c1_rail/book_incident_notifier.py` at base | `ESCALATION_STEP_S` `:63`; `MAX_OUTSTANDING_PUBLISHES` `:67`; `NotifierStoreError` `:109`; config `:213-219`; constructor `:280-282`; journal `:319-357` (`timeout=5` `:349-352`); `poll` `:435-470`; `run_once` `:474-488`; `liveness()` `:490-497`; `progress()` `:499-505`; `publish_due` `:507-530`; `_publish_round` `:576`; `_bounded_publish` `:667-692` |
| #628 owner accessor | merged `ops/c1_rail/book_account_owner.py` | `read_incidents(path)` (`6e57fda:804-818`, `?mode=ro`, `timeout=5`); `_transaction` `:520-528` (`BEGIN IMMEDIATE`, `timeout=5`); `status()` `:999-1001` (`:982` at `ebe5c0b`) |
| #628 build card | `docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md` (on #628) | §1 `:148-168`; §8 `:306` (heartbeat), `:308` (host wiring) |
| Loop | `ops/c1_signal_daemon/book_evaluate_loop.py` | docstring `:1-5` (no config constructor or CLI registration); `step` `:29-58` |
| Timing constants | `ops/c1_signal_daemon/book_protocol.py:39-40` (`BAR_PERIOD`, `BAR_SLACK`); `ops/c1_rail/book_protection_owner.py:24` (`PROTECTION_PERIOD`) | constants only |
| Loop fixtures | `tests/ops/test_book_loop_continuation.py:1-31` | how a `FourLegEvaluateLoop` is built on synthetic sources |
| Halt/resume contract (HR; accepted) | `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md` | storage failure `:36`; attendance `:61`; thresholds qualified before live use `:63`; missed-heartbeat monitoring `:65`; owner reading `:67-71` (condition 4 `:71`); §7 `:233` |
| TB-I3 interlock card #633 | `docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md` | authority `:7`; TB-I1 narrowing `:10`; forbidden wiring `:211`, daemon files `:217`; predecessor sequence `:255`; D-3 now RULED U `:281` |
| R-A2 card #631 | `docs/briefs/handoffs/2026-10-03-ra2-offline-four-sources-card-DRAFT.md` | §2.2 `:115-135`; forbidden wiring `:209`; duration measurement explicitly outside its scope `:247`. Merged card is not a merged build |
| Umbrella | `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md` | TB-I3 row `:232`; reserved files and one writer per file `:245` |
| Multi-leg spec | `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` | R-A1 `:144`; R-H `:157`; R-K split `:163` |
| Image manifest (not edited) | `tests/ops/test_c1_signal_daemon_image_manifest.py:10-15` | `_ENTRYPOINTS` |
| Runtime exception model | `ops/c1_signal_daemon/daemon.py:136-145`; `ops/c1_signal_daemon/book_runtime.py:423`; spec `:157` (R-H) | §3.4 default |
| Legacy daemon heartbeat (not edited) | `ops/c1_signal_daemon/heartbeat.py`, `http_status.py`; S2b ADR `docs/adr/2026-08-08-s2b-signal-daemon-build.md:51` | the pull-only `GET /` snapshot |
| Rules | `AGENTS.md` | launcher `:222-226`; *Configuration as code* `:229-238` |

**The report states:** the dispatch revision; the #628 merge commit; the #637 build merge commit and whether the merged `book_heartbeat.py` signatures match HB §3; P7's cap, its name and its merge commit; whether #631 has merged; and every anchor above that moved.

## §0.5 — Clarifications and recorded facts

1. **Authority.** The Status quotes authorize writing and the two OQ-HOST-5 rulings. C4 reopened this bounded preparation after #701 merged, then supplied HOST-1 and revised values through the deployment coordinator (source response identified as browser Message 223). This is proposal authority only: no implementation, live qualification, effective freeze, dispatch or merge is performed here.
2. **A separate card, not a #633 amendment.** #633 forbids `ops/c1_signal_daemon/**` (`:217`) and route wiring in `daemon.py`, `build_loop` or the CLI (`:211`). Its authority is "no route integration" (`:7`). Its old D-3 HARD STOP has been resolved as RULED U (`:281`); that does not grant this card a freeze or a build dispatch.
3. **The API consumed (HB §3, re-read at the merged head).**
   - `step_with_heartbeat(loop, pinger, *, now, read_status)` calls `step`, then `read_status`, then `mark_progress`. An exception propagates unchanged, and no mark is set.
   - `notifier_round_with_heartbeat(notifier, pinger)` calls `run_once` and reads #652's `progress()` (NF6). It marks only when that count increased since its previous call, never on a clock value. HB `:155` specifies this seam. A merged wrapper that marks on `liveness()` is NEEDS_CONTEXT.
   - `mark_progress()` returns at once.
   - `build_pingers(runtime_binding, notifier_binding)` refuses a shared reference or a shared resolved URL (H12).

   A different merged API is NEEDS_CONTEXT.
4. **Placement constraint (HB §0.5 item 7, `:73`), enforced here.** The notifier never runs on the runtime loop thread, so a slow publish or a `NotifierStoreError` cannot delay `step`. The one shared resource is the owner DB file lock (§3.3), whose wait `max_step_duration` counts. The notifier heartbeat is marked from the notifier's own loop (HB `:155`). HH1-HH3 test this.
5. **The notifier side marks on `progress()`, not on the clock (NF6).** #652's `progress()` is a per-instance count of `run_once` calls that completed without raising and without a loud class-U deferral (NF3). A loud pass therefore sets no mark, by design, and N expires after T_n under HR's owner reading, condition (4) (`:71`). A frozen or backward notifier clock no longer stops marks, as it did when marks followed the `liveness()` timestamp (`6e57fda:436`). The caller still gives the notifier a clock that advances between rounds (§3.3): it sets due times and backoff, and a backward step loosens #652's NF2 retry-spacing bound. The notifier's clock need not be the host's.
6. **P7 is built; timing remains a host binding.** #669 (`d63bf32`) caps passes and provides `progress()`. NF8 (`docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md:254-265`) includes `ε` and uses **one** `publish_timeout_s` for every channel (`book_incident_notifier.py:213`, `:688`). The cap defaults to 10 (`:217`), with 1000 retained incidents (`:219`). The proposed host override is k=8, not a change to either default. NF4 logs an over-bound crossing after reading/parsing and continues processing (`:435-470`); there is no pre-parse cap and this proposal adds none.
7. **The legacy heartbeat is not this path.** The daemon's `GET /` snapshot (`heartbeat.py`, `http_status.py`; S2b ADR `:51`) has to be pulled; it is not an external monitor. It is not extended.
8. **No operator act is needed for this build.** The heartbeat URLs (HB OA-H1 to OA-H4) matter only for HB-L1 and HB-L2, outside this card. Tests use loopback fake receivers and `env:` references that the test sets.

9. **HOST-1 — PROPOSED healthy-host envelope and duration-gated marks (C4, card and halt/resume owner; acceptance pending).** C4's relayed ruling interprets the timing qualification under HR `docs/spec/2026-09-14-tb-s3-halt-resume-contract.md:63` and the independent notifier monitor at `:65-71`. Durations, parsing, `ε`, owner-read and journal-lock allowances are **healthy-host assumptions**, not deadlines guaranteed by the implementation. `validate_binding` proves arithmetic only. HH7 supplies synthetic healthy-host evidence, not a hard timing guarantee or live qualification. No SQLite, parser, IO, notifier or heartbeat module change, in-process cancellation, or extra host execution threads is authorized by HOST-1. C4 subsequently selected and signed the host clock-wrapper observation path for review findings P2-1/P2-2; the correction below remains a proposal until independent recheck and effective freeze.

   The future `book_host.py` measures the whole `step` plus `read_status`, or whole `run_once` plus progress observation, on the injected monotonic clock. It uses the existing wrappers with a host-owned deferred-mark facade: wrapper count observations remain per side; `mark_progress()` only requests a mark. After a successful return, the host forwards that request to the actual pinger only for a finite, nonnegative elapsed time **at most** the side's declared duration. It discards the request after an exception or overrun, including a late successful return. A hanging call never reaches that decision and earns no mark. The actual pingers still come only from `build_pingers`; their secret/reference independence is unchanged. No wrapper is called with an actual pinger that could mark before the elapsed check. No mark is queued for a later slot. This is the explicit HOST-1 host-composition amendment to §3, not a claim that #701 already gates durations.

   In-flight work finishes under #628/#652's journal, J0 serialization, idempotency and late-outcome rules. The host never starts an overlapping call or repeats an abandoned call. After return it uses §3's fixed-rate rule without a catch-up burst; runtime exceptions still stop the runtime thread, while notifier exceptions follow its existing next-slot rule. The stricter host mark does not modify notifier `progress()` or durable state. A subsequent timely successful call can mark; no incident recovery authority follows from that mark.

   **Residual proposed by C4:** constraint (d)'s 60 s retry coverage applies only inside the healthy-host envelope and NF2's existing representative-count precondition. A whole-call hang, raise or persistent overrun suppresses progress and uses the notifier's independent heartbeat (T_n plus assumed ingestion to the provider alert, with the separate notification-chain allowance). It cannot promise a 60 s retry while unhealthy. A transient overrun followed by timely progress need not produce a heartbeat page. HR's acknowledgment, attendance, independent monitoring and pre-live qualification requirements remain; no escalation threshold is amended here.

   **P2-1/P2-2 correction — C4-signed clock observation, PROPOSED pending recheck.** [Review at `54f4509`](https://github.com/Joshua-Asante/first-passage/pull/713#issuecomment-6008392566) found that whole-call duration alone misses poll delay and between-round scheduler delay. C4 selected the existing constructor `clock` injection, not a new notifier accessor or an edit outside `book_host.py`. The host-supplied recording callable is passed when the caller constructs `IncidentNotifier(clock=...)` (`book_incident_notifier.py:280-293`); the host still constructs no notifier. `BookHost` must verify that the supplied observer is the exact callable used by the injected notifier (the existing `_clock` attribute at `:293`), rather than accepting unrelated observations. This private-field/order dependency is expressly part of C4's owner-signed source contract, pinned and tested below; it adds no notifier seam.

   **Observation source and isolation.** `_now()` invokes the injected callable (`:402-406`). On a successful, non-loud `run_once`, the host notifier thread calls it in this exact order: `poll()` at `:442`, `publish_due()` at `:517` **after acquiring `_round_lock`**, then the completion/liveness read at `:487`. Thus C4's “first now in publish_due” means the **second** clock call within `run_once`, never the first poll-start read. The observer opens a per-invocation recording scope on the host notifier thread, calls the original wall clock unchanged, and records a host-monotonic timestamp after each return, including any delay in that clock call. It passes the wall-clock return value through unchanged. It never gates on differences of wall-clock values: HB HQ10's backward-wall-clock behavior is retained. Constructor/rebuild (`:304`), late-publish thread (`:712`) and `record_delivery` (`:734`) clock reads must not become a pass timestamp. Record only the scoped host thread; same-thread unexpected/reentrant calls make the invocation ineligible. No stack inspection is required by the design: the pinned successful-call order identifies the second read; HH7 verifies that order against the real notifier. A missing/extra read, mismatched observer, non-finite or backward monotonic observation fails closed for marking and is reported as a contract/observation fault, not a healthy sample.

   **Three notifier forward conditions, all inclusive:** (1) whole-call elapsed ≤ `max_round_duration_s` = **38.4 s**; (2) host-monotonic elapsed from the invocation start to its captured `publish_due` clock read ≤ `poll_bound_s` = **2.1 s**; (3) host-monotonic spacing from the preceding pass's captured `publish_due` read ≤ `max_notifier_loop_interval + poll_bound_s` = **41.5 s**. All intervals must be finite and nonnegative, the call must succeed, the clean three-read shape must match and NF6 progress must increase. Only then may the deferred request reach the actual pinger. The spacing directly covers the quantity used in (d), including a late wake between calls; a separate 39.4 s start-gap gate is not required by C4's selected spacing rule. Runtime forwarding retains only its existing whole-call gate, since its start interval feeds (b), not (d).

   **History and failed calls.** The first eligible pass seeds the prior timestamp and earns no notifier mark because no prior spacing is observed. Every later unambiguously captured pass timestamp replaces the previous timestamp even when duration, poll or spacing rejects its mark, or NF3 makes the pass loud (the normal loud path has exactly the first two reads). Never retain only the last *marked* timestamp, which would prevent recovery after a delayed pass. An exception/ambiguous clock shape invalidates the spacing baseline; a later clean pass seeds it without marking, then the next eligible pass may mark. A hung call earns no mark and is not overlapped. The existing wrapper's per-side progress observation still runs, so rejected marks are never replayed. These rules are local observation state only; journal/progress and wall-clock semantics are unchanged.

   **Remaining residual, explicitly retained:** these are post-return mark gates, not cancellation or a promise of a page for every isolated timing violation. Persistent poll/spacing/whole-call violations withhold marks; a later timely pass can recover observation and ping before T_n, so a transient gap need not page. Independent receiver expiry covers sustained absence of marks, subject to HB-L1/L2 qualification. The distinct W_o/W_j/parse/ε assumptions need no individual gate for (b): they enter through whole duration. The separately used poll/spacing terms in (d) now have stated coverage. NF2's representative-count precondition and advancing notifier wall-clock assumption remain; this proposal makes no new wall-clock-drift guarantee and no HR escalation-contract amendment.

A contradicted fact, a missing producer or a needed edit outside §5 returns NEEDS_CONTEXT.

## §1 — Goal, scope, dependencies

**Goal.** Build the host composition that the later live route packet registers unchanged. It ties the runtime heartbeat to step progress and the notifier heartbeat to notifier progress, on separate threads, at declared and validated cadences. HB's T and P can then be frozen from real inputs.

**Scope.** `BookHostBinding` and its validator; `BookHost`, which owns the runtime thread, the notifier thread, stop and in-memory counters; synthetic tests. The host builds nothing it runs: the loop, the owner status reader, the notifier, the pingers and the clocks are all injected.

| ID | Dependency | State at draft | Blocks |
|---|---|---|---|
| P1 | #628 merged | **DONE**: `6e679cc` | Freeze |
| P2 | #637 card frozen and its build merged (`book_heartbeat.py` on main) | **DONE**: #695 `7c23b21`; #701 `de0e412`; signatures read at base (§12) | Freeze |
| P3 | Frozen binding values (§2) | **Done**: the HOST-1 values in §2 and the §0.5 item 9 clock gates were bound at the freeze by coordinator (4), 2026-10-06 | Dispatch |
| P4 | Joshua's OQ-HOST-5 rulings | **DONE**: (a) Joshua directly to C4, 2026-10-03, "yes to OQ-HOST-5 (a)"; (b) Joshua directly to coordinator (3), same date about 18:04Z, "I approve the dispatch" | Dispatch; separate record still owed |
| P5 | C4 effective freeze record (§12) | **OPEN**, this PR is preparation only; independent Claude review and C4 acceptance owed | Dispatch |
| P6 | #631 card and later build | Card merged `6328521`; **build still owed** (current `step` remains the old sequence) | Not dispatch. Re-run HH7 and re-declare the runtime envelope after that build, then again at the live route binding |
| P7 | #652 NF1/NF3/NF4/NF5/NF6/NF8 build | **DONE**: card `af506f7`, freeze `e997223`, #669 build `d63bf32`; `max_jobs_per_round` default 10, `progress()` `:499-505`; proposed instance k=8 | Freeze |

Freeze needs P1, P2, P7 and the OQ-CAP-3 choice (§9). Dispatch needs the freeze (P3, P5) and P4.

## §2 — P4 inputs and the threshold

| Input | Meaning | Supplied by, and when |
|---|---|---|
| `step_interval_s` | Target spacing between step starts | This card's binding. Frozen at this card's freeze |
| `max_step_duration` | Healthy-host envelope for the entire `step` plus `read_status` | **PROPOSED 10 s**, C4 HOST-1 aggregate assumption. Source trace: four polls and owner/schedule/pending-boundary/dispatch work in `book_evaluate_loop.py:29-58`, runtime continuations `book_runtime.py:432-476`, owner transactions/status `book_account_owner.py:520-528`, `:999-1001`. The sum includes all those operations, their busy waits and processing, not just four polls. No per-operation guaranteed bound or fixed transaction count is claimed. HOST-1 replaces the draft requirement for a sum of individually guaranteed bounds with this provisional aggregate envelope and overrun/no-mark behavior. HH7 measures the synthetic scope; #631 build and the final live route must re-declare it with their actual source and dispatch inputs |
| `max_step_interval` | Longest gap between step starts on a healthy host | Derived: `max(step_interval_s, max_step_duration) + scheduler_slack_s` (fixed-rate schedule, §3.2). HH7 measures it |
| `ping_timeout` | Send timeout of each `HeartbeatPinger` (`timeout_s`) | The #637 build exposes it as the constructor `timeout_s` (HB `:100`); this card's binding sets the value per side (HB `:151`). Coordinator (4) freezes the runtime and notifier values at this card's freeze, under (a) |
| `P` | Minimum spacing between runtime pings (`period_s`) | Coordinator (4) at this card's freeze, under (a) and (b) |
| `T` | IRM heartbeat timeout of the runtime integration | Coordinator (4) under HB OQ-H1 (lean 1 min). The final T for HB-L1 is set at this card's freeze. Joshua sets it in IRM (HB OA-H1) |
| `notifier_interval_s`, `max_round_duration`, `max_notifier_loop_interval`, `P_n`, `T_n` | Notifier timing | C4 HOST-1 proposal below, using merged NF8 **with ε**: `W_o + T_parse(n <= M) + (2 + 2kc) W_j + kcτ + ε`. NF8 owner `docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md:254-265`. W_o=1 s and W_j=0.1 s are healthy-host envelopes; the code still allows 5 s busy waits (`book_account_owner.py:812`, notifier `:349-352`) and a separate COMMIT wait (`:333`). T_parse and ε are assumptions, not code limits. The common τ=2 s is enforced as the per-publish join timeout (`:688`), not a promise that the underlying channel thread finishes |
| `retry_max_s`, `poll_bound_s` | Retry cap and healthy poll bound | **PROPOSED** retry cap 10 s (config `book_incident_notifier.py:215`, validation `:237-240`), and `poll_bound_s = W_o + T_parse(M) + W_j = 2.1 s`. HOST-1 observes invocation start to the `publish_due` clock read and gates this quantity at 2.1 s (§0.5.9). `BookHost` refuses a retry-cap mismatch |
| `ingestion_allowance_s`, `chain_s` | IRM ingestion allowance; `chain_s` = 90 s, the SMS-to-call fail threshold (HB §0.5 item 3) | Coordinator (4) at freeze. HB-L1 measures ingestion |

**Threshold (HB `:137` and `:157`, restated without change; (d) is this card's).** Runtime side:
- (a) `ping_timeout < P`
- (b) `P + max_step_interval + max_step_duration + ping_timeout < T`
- (c) `T + ingestion_allowance_s + chain_s < PROTECTION_PERIOD` (15 min, `book_protection_owner.py:24`)

The notifier side is the same, with `P_n`, `max_notifier_loop_interval`, `max_round_duration` and `T_n`. It also carries:
- (d) `retry_max_s + max_notifier_loop_interval + poll_bound_s < ESCALATION_STEP_S` (60 s; `6e679cc:60-62`, HR `:63`, `:73`), checked at the frozen `max_jobs_per_round`: `max_round_duration_s`, which `max_notifier_loop_interval` cannot be below, and `poll_bound_s` are declared by NF8 at that k, and HH7 measures them there
- (e') `max_jobs_per_round >= K_FLOOR`, with `K_FLOOR` = 8 (coordinator (3)'s card-owner ruling (c), 2026-10-03): k_first = 5, one origin incident plus at most one close-outcome incident per leg, which is one halt's realistic first-pass set, plus margin, the low end of the owner's stated k ≈ 8-10. #652 derives both in §0.5 item 11 (`bfacb9e:116-137`) under the halt/resume owner's OQ-NF-3 ruling (a), the first-page reading, 2026-10-03. #652's default k is 10. (e') replaces (e), k ≥ 51, which that ruling withdrew

(d) carries the precondition of #652's representative guarantee (NF2, `bfacb9e:192-193`): while at most k representatives are due per pass, each halt sequence without an accepted page gets a retry in every 60 s escalation interval when `retry_max_s` plus the gap between passes is below 60 s. `max_notifier_loop_interval` is measured between `run_once` starts, but attempt times are `publish_due`'s `now`, taken after `poll`, so one `poll_bound_s` is added. (b) does not imply (d): `max_round_duration` = 10 s and `max_notifier_loop_interval` = 35 s can pass (b) at T_n = 60 s, yet at the default `retry_max_s` of 30 s, 30 + 35 > 60. The freeze needs both (b) and (d), independently. HOST-1 proposes T_n = 120 s because (b) fails at 60 s; (d) retains its 60 s threshold. (e') floors the cap at one halt's realistic first-pass set plus margin, so that set runs in one pass. #652's NF2 sorts each unpaged sequence's representative ahead of its other class-U jobs: the first job (tier 0), or, once that job has run and while it is not due, the oldest-due later job (tier 1). While at most k representatives are due in a pass, a burst above k defers only other class-U jobs (tier 2) and class A: #652's accepted residual R6 (`bfacb9e:453-456`). A pass with more than k due representatives also defers representatives, tier 1 before tier 0, and is loud (NF3).

Why (b) keeps a healthy receiver alive: after a send, the next send needs P to pass and then a mark. Marks come at step ends, at most `max_step_interval + max_step_duration` apart, and a send arrives within `ping_timeout`. Consecutive arrivals are therefore less than T apart.

**HOST-1 binding proposal (all values PROPOSED for C4 freeze; seconds unless stated).** Source: C4 revised HOST-1 relayed through the deployment coordinator; merged-owner constraints and enforcement are cited below. No value here is accepted, measured, deployed or a provider setting.

| Field | PROPOSED value | Basis / actual enforcement |
|---|---|---|
| Runtime `step_interval_s`, `max_step_duration_s`, `scheduler_slack_s` | 10, 10, 1 | C4 aggregate healthy-host proposal; source trace in §2; host elapsed gate only (§0.5.9) |
| Runtime `max_step_interval` | `max(10,10)+1 = 11` | Fixed-rate healthy envelope |
| Runtime P, ping timeout, T | 12, 5, 60 | C4 proposal; HB §3.3 constraints; pinger validates `timeout_s < period_s` at `book_heartbeat.py:117-120`; 60 s is HB's stated provider floor (`:139`), still qualified through HB-L1 |
| k, `K_FLOOR`, M (`max_retained_incidents`), c | 8, 8, 1000, 2 | Host k override; NF8/NF4 and `NotifierConfig:217-219`; floor from #652 §0.5 item 11; two configured channel kinds `grafana_irm` and `local_file` (binding card `:149`) |
| Common `NotifierConfig.publish_timeout_s` τ | 2 | **Merged-form correction:** one value applies to both channels (`book_incident_notifier.py:213`, `:688`). No per-channel 0.5 s timeout exists. C4's proposed local-file 0.5 s is not used to reduce NF8 |
| W_o, W_j, T_parse(n ≤ M), ε | 1, 0.1, 1, 1 | C4 healthy-host assumptions, not SQLite/IO/CPU deadlines. M is not a pre-parse cap; over-bound history retains NF4 behavior |
| `max_round_duration_s` | `1+1+34×0.1+8×2×2+1 = 38.4` | Merged NF8 includes ε and common τ. C4's channel-specific calculation was 26.4; **delta +12 s** |
| `notifier_interval_s`, `max_notifier_loop_interval` | 10, `max(10,38.4)+1 = 39.4` | C4 cadence; derived healthy envelope, +12 s versus C4's 27.4 |
| `retry_max_s`, `poll_bound_s` | 10, `1+1+0.1 = 2.1` | Configured backoff cap, separate healthy poll envelope; initial retry stays its existing 5 s default |
| Notifier P_n, ping timeout, T_n | 12, 5, 120 | 60 s fails (b); proposed 120 s passes. HB-L1/L2 must confirm provider setting and delivery; no claim that 120 s is the smallest offered option |
| `ingestion_allowance_s`, `chain_s` | 30, 90 | C4 ingestion assumption, measured at HB-L1; chain fail threshold from HB §0.5 item 3 (`:69`), not a guaranteed provider latency |

**Arithmetic under those assumptions, unchanged strict inequalities:**
- Runtime (a): `5 < 12`; (b): `12 + 11 + 10 + 5 = 38 < 60`; (c): `60 + 30 + 90 = 180 < 900`.
- Notifier (a): `5 < 12`; (b): `12 + 39.4 + 38.4 + 5 = 94.8 < 120` (fails at 60); (c): `120 + 30 + 90 = 240 < 900`.
- Notifier (d): `10 + 39.4 + 2.1 = 51.5 < 60` (8.5 s margin, healthy-host/NF2 scope only). Raising T_n contributes nothing to this inequality.
- (e'): `8 >= 8`. The code default remains 10; `BookHost` requires the selected instance to use 8.

HH7 evidence, independent reviewer recheck of §0.5.9's clock-observation gate and C4 binding acceptance remain owed. The arithmetic does not qualify the future implementation or live monitor.

## §3 — Design

1. **Binding (config as code; AGENTS.md `:229-238`).** `BookHostBinding` is a frozen dataclass in `book_host.py`.
   - Fields: `step_interval_s`, `max_step_duration_s`, `notifier_interval_s`, `max_round_duration_s`, `max_jobs_per_round`, `retry_max_s`, `poll_bound_s`, `scheduler_slack_s`, `runtime_timeout_s` (T), `notifier_timeout_s` (T_n), `ingestion_allowance_s` and `chain_s`. It also holds the two ping bindings in HB §3.7's shape, `{"secret_ref", "period_s", "timeout_s"}`, with references only; each `timeout_s` is this card's `ping_timeout` (§2).
   - `max_jobs_per_round` is a positive integer equal to P7's cap, and `retry_max_s` equals the notifier's `config.retry_max_s` (`6e679cc:211`, `:278`). `BookHost` refuses, at construction, a notifier whose configured cap or `retry_max_s` differs; the cap's merged name is recorded at freeze (§12).
   - `validate_binding` runs at construction, the consumption boundary. It refuses non-finite or non-positive values and any breach of §2 (a)-(c) on either side or of (d) or (e') on the notifier side. Each refusal names the constraint and the side, never a URL.
   - `PROTECTION_PERIOD` is imported from its owner, not restated. `ESCALATION_STEP_S` cannot be imported (§3.6 bans `book_incident_notifier`), so `book_host` restates it as 60.0 and HH4 pins it to the notifier's constant. `K_FLOOR` = 8 is restated from #652's §0.5 item 11 (`bfacb9e:131-134`), and HH4 pins the notifier's default cap at or above it.
   - `binding_digest` is SHA-256 over canonical JSON, so validation and later activation name the same configuration.
   - Under HOST-1, `BookHostBinding` also carries the proposed notifier τ, M, channel-kind/count expectation and the W_o/W_j/T_parse/ε envelopes once, deriving the round and poll bounds rather than duplicating their numeric results. Its digest includes these inputs and both pinger bindings. `BookHost` rejects mismatches against injected notifier config for k, retry cap, common publish timeout, M and the two channel kinds/count; it does not construct the notifier or change its config. HH4 tests each mismatch. No check claims enforcement of healthy-host assumptions.
   - `FROZEN_BINDING` is built only from values C4 eventually accepts (§12); this preparation does not produce a binding digest or a runtime constant.
   - The binding reads no environment. Pingers are built only through #637's `build_pingers`, in tests too (§6), so H12 always applies.
2. **Runtime thread.** Steps start on a fixed-rate schedule: the next start is the previous start plus `step_interval_s`. After an overrun, the next step starts at once, with no catch-up burst. Each side's scheduler takes an injected `monotonic()` (seconds) and `wait(seconds)`; production binds them to `time.monotonic` and the stop event's `wait`. Start gaps and durations are measured on `monotonic`. Each step calls `step_with_heartbeat` through the duration-gated facade (§0.5.9), with `now=wall_clock()` and `read_status=read_status`, with `wall_clock` injected. The caller binds `read_status` to the owner's `status()`.
3. **Notifier thread.** A second thread runs `notifier_round_with_heartbeat` through its own duration-gated facade (§0.5.9) at `notifier_interval_s`, under the same fixed-rate rule.
   - The caller builds the notifier with `read_incidents` bound to the owner's path (the read-only C-1 seam) and the host recording wrapper around a clock that advances between rounds (§0.5 items 5 and 9). The host checks observer identity and measures whole-call, start-to-publish-clock and consecutive-publish-clock intervals before forwarding a mark; returned wall-clock values are never used as elapsed measurements.
   - The notifier loop function takes only the notifier, its pinger and its cadence, so the live packet can move it into its own process without editing it (OQ-HOST-1).
   - No Python-level lock, queue or join is shared between the two threads; they share only the stop event (§3.5). The owner DB file lock is the one shared resource: `read_incidents` opens the DB read-only (`book_account_owner.py` `6e57fda:804-818`, `timeout=5`), while owner transactions in `step` and `status()` take `BEGIN IMMEDIATE` (`:520-528`, `timeout=5`) without WAL. The 5 s busy timeout is per SQLite lock wait, not a whole-call bound; COMMIT can also wait. HOST-1's smaller W_o/W_j are assumptions, not code changes or enforced guarantees (§0.5.9).
4. **Exceptions (OQ-HOST-3).** A step or round that raises is not progress, and the wrapper sets no mark. The host records the exception class and a count, never the message. It never retries within a slot, never touches owner state, and never turns an exception into a mark.
   - Runtime side (default): the runtime thread stops after any exception from `step` or `read_status`, and R expires after T and pages. The legacy loop also ends on an exception (`daemon.py:136-145`). An exception inside `step` can follow a committed fact before adapter feedback (`book_runtime.py:423`), adapters hold state in memory, and recovery is a restart that restores state first (R-H, spec `:157`). Continuing instead needs the `book_runtime.py` owner's evidence that re-entering `step` after any exception equals restart replay.
   - Notifier side: the thread continues at the next scheduled start, so a persistent failure expires N after T_n.
5. **Stop and counters.** `stop()` sets one event. Each thread finishes its current call and exits. The join waits a bounded time and reports any thread that has not exited (for example, a hung step) instead of blocking. Per side, the host keeps in-memory counters: calls started, raises by class, the largest observed duration and the largest observed start gap. It has no restart logic: process supervision, including whether a stopped runtime thread ends the process, is R-H's.
6. **Imports.** `book_host` imports `book_heartbeat`, `PROTECTION_PERIOD` and the standard library only. The notifier and the loop are duck-typed. It imports nothing from `daemon.py`, `__main__`, the CLI, `book_incident_notifier`, the IRM channel module, arm or config-write modules, or broker or dispatch transports. It reads no `dry_run` or `armed_until`. It is not added to `_ENTRYPOINTS`.
   - The ban is transitive. Forbidden modules: `c1_signal_daemon.daemon`, `.__main__`, `.listener_client`; `c1_rail.book_incident_notifier`, `.book_incident_grafana_irm`, `.c1_rail_arm`, `.write_volume_config`, `.c1_rail_listener`, `.c1_rail_http_server`, `.crosstrade_payload`. At `ebe5c0b`, importing `book_protection_owner` loads 9 project modules, none of them forbidden.

## §4 — Hypothesis and falsifier

**H:** A host that runs the loop and the notifier on separate threads, through the #637 wrappers, at cadences validated against HB `:137` and §2 (d), keeps both fake receivers alive while both sides progress. When one side stalls, raises or hangs, only that side's receiver expires. The step cadence stays within `max_step_interval` whatever the notifier does; any owner DB lock wait it causes is inside `max_step_duration` (§3.3).
**Falsifier:** any of the following.
- `run_once` runs on the runtime thread, or a raising, hanging or slow notifier pushes a step start gap above `max_step_interval`.
- A binding that breaks (a), (b) or (c) on either side, or (d) or (e') on the notifier side, is accepted, or a notifier whose cap or `retry_max_s` differs from the binding's is accepted.
- A healthy synthetic host expires either receiver, or a stall on one side expires the other side's receiver.
- A mark follows a step or round that raised, exceeded its declared whole-call duration, or completed late after that duration, or, under the runtime default (§3.4), `step` runs again after a `step` or `read_status` that raised.
- In healthy HH7 samples, a measured step duration/start gap or notifier round/poll/publish-clock spacing exceeds its declared envelope. In deliberate unhealthy cases, **any notifier mark** after a round >38.4 s, start-to-publish-clock >2.1 s or publish-clock spacing >41.5 s falsifies HOST-1, even if the other two quantities pass. A mark on absent/ambiguous observations or a falsely seeded first pass also falsifies it.
- `book_host` imports a §3.6 forbidden module, directly or transitively, or it appears in `_ENTRYPOINTS`.
- A URL appears in a log, `repr`, counter or exception.

## §5 — Files

**Allowed:**
- `ops/c1_signal_daemon/book_host.py` (new): `BookHostBinding`, `validate_binding`, `binding_digest`, `FROZEN_BINDING`, `ESCALATION_STEP_S`, `K_FLOOR`, `BookHost`.
- `tests/ops/test_book_host.py` (new): HH1-HH8.
- This card: the §12 freeze record and the executor return only.

**Forbidden (stop and return if a change seems needed):**
- Registration and route wiring: `ops/c1_signal_daemon/daemon.py`, `build_loop`, `ops/c1_signal_daemon/__main__.py`, the daemon CLI and any HTTP endpoint. Registration belongs to the live route packet (R-A1/R-H; spec `:144`, `:157`).
- `ops/c1_signal_daemon/book_evaluate_loop.py` (#631), `book_runtime.py`, `book_protocol.py`, `heartbeat.py`, `http_status.py`, `evaluate_loop.py`.
- `ops/c1_rail/book_account_owner.py`, whose edit order is #628, then GC-5, then TB-I3 S2 (#633 `:255`), and every other `ops/c1_rail/book_*.py`.
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
| HH2 | `test_raising_notifier_leaves_step_cadence_bounded` | `run_once` raises `NotifierStoreError` every round; separately, the notifier is built with an injected `read_incidents` that raises (HQ9's store-loss path) while the owner DB stays readable. On the runtime side's fake clock, step start gaps stay within `max_step_interval`, and at least 50 steps finish before a 10 s real-time deadline. R never expires. N expires after T_n. The notifier thread continues; the class is counted and no message is logged | (a); HB `:73`, `:74`, HQ9 `:227` |
| HH3 | `test_hung_notifier_leaves_step_cadence_bounded` | `run_once` blocks on a held event. On the runtime side's fake clock, step start gaps stay within `max_step_interval`, and at least 50 steps finish before a 10 s real-time deadline. R never expires. N expires after T_n. `stop()` reports the hung thread within its bounded join | (a); HB `:73` |
| HH4 | `test_binding_validator_refuses_constraint_breaches[a,b,c × runtime,notifier; d,e' × notifier]` | Each breach is refused, naming the constraint and the side. Equality is refused for (a)-(d), which are strict; (e') accepts it. Non-finite and non-positive values are refused. A binding that passes (b) but breaks (d) is refused (for example `max_round_duration_s` 10 s, `max_notifier_loop_interval` 35 s, `retry_max_s` 30 s). `book_host.ESCALATION_STEP_S` equals `book_incident_notifier.ESCALATION_STEP_S`. A binding with `max_jobs_per_round` = 7 is refused, naming (e'), and 8 meets (e'). `book_host.K_FLOOR` is 8, and the notifier's default `max_jobs_per_round` is at least it. A valid binding passes, and its digest is stable. `FROZEN_BINDING` passes. `BookHost` refuses a notifier whose cap differs from `max_jobs_per_round` or whose `retry_max_s` differs from the binding's | (b); HB `:137`, `:157`; §2 (d), (e'); #652 `bfacb9e:192-193`, `:116-137` |
| HH5 | `test_hq6_through_host_notifier_stalled_runtime_alive` | N expires after T_n; R does not | (c); HB HQ6 `:224` |
| HH6 | `test_hq7_through_host_runtime_stalled_notifier_alive` | `step` blocks; or `step` raises once and the runtime thread stops with no second `step` (§3.4); or stepping stops. R expires after T; N does not. The owner's `incidents` and `status()` compare equal before and after the expiry | (c); HB HQ7 `:225` |
| HH7 | `test_measured_step_and_round_within_declared_bounds` | On a test binding at test-scale cadences (not `FROZEN_BINDING`, which HH4 validates), on real monotonic time: at least 200 steps on synthetic sources and 200 rounds. The notifier journal is seeded with history up to the test `max_retained_incidents`, and `read_incidents` returns that many rows. At least 20 rounds have `max_jobs_per_round` jobs due, on a channel stub that holds every publish to the test `publish_timeout_s`. Asserted against the test binding: the largest step duration is at most `max_step_duration_s`; the largest start gap is at most `max(step_interval_s, max_step_duration_s) + scheduler_slack_s`, with slack at least 0.1 s (Windows timers resolve about 15.6 ms); the largest round is at most `max_round_duration_s`, declared by the NF8 formula (§2) at the test values. The count, maximum and p99 are printed for the return, not asserted | (d); P4 |
| HH8 | `test_host_import_and_scope_boundary` | An AST check finds only §3.6's direct imports and no `dry_run` or `armed_until`. A fresh `sys.executable` subprocess that imports `book_host` loads no §3.6 forbidden module. No `book_host` in `_ENTRYPOINTS`, `daemon.py` or `__main__.py` | §3.6; §5 |

**HOST-1 proposed HH7 extension (same test file; no implementation in this preparation):** retain the original healthy measurement assertions separately from deliberately unhealthy cases. With an injected monotonic clock, on both sides test success at the duration boundary, success just above it, an exception, a held call past its duration and its late successful return. At/under the boundary may mark only if the other applicable conditions pass; all above-bound, exceptional and still-held cases forward zero marks, and a late return never flushes a discarded request. Instrument the actual pinger so premature marks inside the merged wrapper fail. Calls never overlap; runtime exceptions still stop and notifier exceptions follow their existing next-slot rule. Use the real NF6 counter; a late counter increment alone never forwards a mark. A hung call must allow fake receiver expiry, without promising a page for every transient fault.

**Clock-observation HH7 cases (P2-1/P2-2):** use a real `IncidentNotifier` with its constructor `clock` bound to the host observer, not a fake supplying nonexistent timestamps. Prove the source order `poll → publish_due → run_once completion` and the selected second-read timestamp on the host thread. Seed the first clean pass without a mark, then independently exercise exact/just-over boundaries: duration 38.4; start-to-publish-clock 2.1; consecutive publish-clock spacing 41.5. Arrange every other condition to pass when isolating a failure. Equality passes after seeding; each just-over case suppresses the actual mark. Use a fake `wait` that creates >41.5 s spacing before a fast round with poll ≤2.1 s: no mark, even though whole-call duration is short. A subsequent eligible pass, measured from the rejected pass's captured timestamp, may mark; no catch-up burst or replay occurs. Test normal loud passes, an exception before the publish-clock observation, a late clock return, missing/extra same-thread reads, observer mismatch and the first-pass reset rule. Verify that constructor/record-delivery reads outside the scope and a real late-publish worker's clock read cannot shift the selected ordinal or update the prior-pass baseline. Retain HB's backward-wall-clock case: values can go backward while monotonic observations and NF6 increase normally. HH7's healthy report includes maxima for both new measured quantities alongside whole duration and starts; source/order drift returns NEEDS_CONTEXT.

**Retained 20 s poll diagnostic, now a rejection test:** use a synthetic reader that consumes 20 s on the injected monotonic clock, followed by 1 s of other work. The real notifier's first clock read occurs **before** that reader (`:442`), and the second occurs in `publish_due` (`:517`), so the host observes a 20 s poll although the 21 s whole round is below 38.4 s. NF6 can increase, but the poll gate must forward zero marks. A mutant selecting the first read or checking only whole duration would mark and fails this test. Separately, hold `_round_lock` before `publish_due` on the real notifier: the selected second observation includes that wait and suppresses the mark when start-to-observation exceeds 2.1 s. No notifier source is edited. The old `10+39.4+20=69.4` counterexample remains the reason for this gate, not an accepted poll residual.

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
- Building #652 (P7), whose NF1, NF4, NF5 and NF8 bound the round (OQ-HOST-2), and the dot path (HB §3.6).

**Overlaps:**
- **#633:** not amended (§0.5 item 2).
- **No second loop runner.** The live route packet registers `book_host` and writes no step loop of its own.
- **The legacy `GET /` heartbeat** is not extended (§0.5 item 7).
- **#631** changes `step` to poll all four sources and then check health (`76110a9:106-118`). That changes `max_step_duration`, so HH7 is re-run after #631 merges. The two cards share no file.
- **Timing owners** each declare their bound once: #631 the step body, #619 the source backoff, and the route transport its dispatch timeout. This card sums declared bounds and does not re-derive them.

## §9 — Decisions and open questions

**Recorded:** Joshua's 2026-10-03 authorization to write this card (Status; §0.5 item 1).

**Proposed (coordinator (4) confirms at freeze):** D-H1, a separate card rather than a #633 amendment (§0.5 item 2). D-H2, the notifier on its own thread, with a loop function that does not depend on its process (§3.3). D-H3, after an exception the runtime thread stops and the notifier thread continues, neither marking (§3.4). D-H4, fixed-rate scheduling (§3.2).

**OPEN:**
- **OQ-HOST-1** (coordinator (4)). Notifier placement. Lean: a thread now. A separate process would let the notifier page committed incidents while the runtime process hangs; decide that with the live packet under R-H.
- **OQ-HOST-2 — P7 build merged; C4 timing acceptance still owed.** #669 supplies NF1 bounded job counts, NF4 over-bound detection, NF5 pending selection and NF6 progress. NF8 gives the whole-invocation formula only under its assumptions. HOST-1 adds the proposed healthy envelope and duration-gated host mark; it does not make parsing, IO or journal completion hard-bounded (§0.5.9). Raising T_n changes neither those assumptions nor constraint (d).
- **OQ-HOST-3** (coordinator (4); `book_runtime.py` owner). Whether the runtime thread may continue after an exception instead of stopping (§3.4 default). Only on that owner's evidence that re-entering `step` after any exception equals restart replay. The notifier side continues.
- **OQ-HOST-4 — PROPOSED, C4 acceptance owed.** The full HOST-1 table and arithmetic in §2 replace the draft lean. Runtime T=60; notifier T_n=120; common notifier publish timeout=2; no per-channel 0.5 s guarantee. §0.5.9 records C4's owner-signed clock-observation proposal, retained residual and pending reviewer recheck; no effective freeze is claimed.
- **OQ-HOST-5 — both operator rulings recorded.** (a) Joshua directly to coordinator (4), 2026-10-03: "yes to OQ-HOST-5 (a)". (b) Joshua directly to coordinator (3), same date about 18:04Z: "I approve the dispatch". These do not replace C4 acceptance or the separate §12 dispatch record.
- **OQ-HOST-6** (coordinator (4)). The executor. The umbrella routes TB-I3 to Codex local (`:232`); HB routes its build to Opus/CC (HB §11). It is not GLM either way (§11).
- **OQ-CAP-3 — PROPOSED HOST-1 replacement, not accepted.** Use the merged NF8 formula with ε, a common τ=2 s, k=8 and c=2 (§2); its 38.4 s healthy envelope replaces the draft 19.45 s illustration and C4's unsupported per-channel 26.4 s calculation. (b) requires T_n above 94.8 s at this proposal; T_n=120 s is proposed. (d) independently passes at 51.5 s only under the declared component assumptions and NF2 precondition. P2-1/P2-2 are addressed by the proposed host clock-observation gates (§0.5.9), pending independent recheck; the post-return/transient residual is explicitly retained. No SQLite/IO/parser enforcement is added and no code timing guarantee is inferred from HH7.

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

## §12 — Proposed freeze and separate dispatch record

- **Status:** **FROZEN 2026-10-06 by coordinator (4), card owner, at the commit that adds this line**, after the independent Claude reviews (PR #713 comments 6008392566 and 6008699002). Every value and gate marked PROPOSED in §0.5 item 9, §2 and §9 (OQ-HOST-4, OQ-CAP-3) is bound as written; the PROPOSED labels record how each was prepared. Prepared by the deployment coordinator's worker. *As prepared:* PROPOSED for coordinator (4) acceptance after independent Claude review. This preparer does not freeze, accept, dispatch or merge. Base `38fc875ce15336df082c0f7d8eebba9012f4250d`; initial reopened base `de0e4129ce48016244812a1837f3d0bb63491809`. This is one docs-only preparation PR for #651. HOST-1, the corrected timing table, aggregate runtime-envelope interpretation and the revised §0.5.9 clock-observation contract need independent recheck and explicit C4 binding acceptance before effective freeze. C4 selected/signed the existing clock-wrapper path for P2-1/P2-2; this is not self-acceptance by the preparer. Dispatch remains a later, separate record even after that acceptance.
- **Prerequisite evidence:** P1 #628 `6e679cc9f96451ba2b7e6e766974074344bf4da9`; P2 heartbeat freeze #695 `7c23b21f2ee276f4c689b643ddf2593e850241e4` and build #701 `de0e4129ce48016244812a1837f3d0bb63491809`; P7 #652 card `af506f7`, freeze `e997223`, build #669 `d63bf324ea2c330f55d8741c48dffbdc21c4b896`. P6 #631 is a merged card (`6328521`), not a built loop change. P4 records both operator rulings; P3/P5 remain proposed/open.
- **Merged signatures:** `HeartbeatPinger(secret_ref, *, period_s, timeout_s, clock=time.monotonic, environ=None, allow_loopback_http=False)` (`book_heartbeat.py:114-116`); `step_with_heartbeat(loop, pinger, *, now, read_status)` (`:346`); `notifier_round_with_heartbeat(notifier, pinger)` (`:358`); `build_pingers(runtime_binding, notifier_binding, *, environ=None, allow_loopback_http=False, clock=time.monotonic)` (`:379-380`). The wrappers mark successful progress immediately; HOST-1's deferred-mark facade is future #651 work. No signature change is proposed. NF6 `progress()` is at `book_incident_notifier.py:499-505`.
- **Cap and binding:** merged `max_jobs_per_round` defaults to 10 (`book_incident_notifier.py:217`); proposed instance override 8 meets K_FLOOR=8. Other values and all (a)–(e') calculations are in §2. Values are PROPOSED, not FROZEN. `binding_digest` is owed with the accepted config-as-code binding; do not fabricate an implementation-dependent digest in this docs preparation. HB §12 must record the accepted binding before HB-L1.
- **Moved-anchor map (draft → this base):** notifier `ESCALATION_STEP_S :60-62→:63`, `MAX_OUTSTANDING_PUBLISHES :66→:67`, `NotifierStoreError :105→:109`, config `publish_timeout_s :209→:213`, `retry_max_s :211→:215`, constructor `:266-279→:280-282`, journal timeout `:304→:349-352` (transaction `:319-340`), `run_once :425-436→:474-488`, `liveness :438-445→:490-497`, `publish_due :447-461→:507-530`, `_publish_round :463→:576`, `_bounded_publish :554→:667-692`, historical poll `:396-421→:435-470`, pending fetch `:455-459→:516-530`. #633 wiring `:206→:211`, daemon exclusion `:212→:217`, predecessor sequence `:250→:255`; D-3's historical stop is now RULED U `:281`. #631 `:106-118→:115-135`, `:179→:209`; #615 RH3 `:156→:158`; #635 host-wiring exclusion draft `:244` is now the §8 exclusion at `:290`. Historical HR `:34/:57/:59/:61/:143→:36/:61/:63/:65/:233` was already reflected in this card's §0; current HR anchors are unchanged. Owner `status :982→:999-1001` was already corrected; read-incidents `:804-818` and transaction `:520-528` remain. HB §3.3/§3.9 `:137/:139/:157` and its cited P/HQ rows remain. #628 goal/prerequisite section `:156→:148-168` now names the full section. Other §0 paths/ranges (loop, constants, fixtures, multi-leg spec, umbrella, image manifest, daemon, runtime, S2b ADR, AGENTS) retain their draft anchors at this base. SHA-qualified historical examples remain explicitly historical.
- **Preparation verification:** run launcher doctor, authority `--all`, brief-form, target brief checks, link/anchor inspection, one-file diff and a completed source-stable `fp check` capture. The PR/worker return carries exact head, commands and the local record path; this paragraph does not assert a pass. No HH build/live test is run by this preparation.
- **Build executor and dispatch:** not selected or dispatched by this preparer. C4 records the effective frozen revision and the separate build dispatch after review, recording acceptance of the reviewed clock-observation contract, retained residual and any other open owner decisions. No provider setup, credentials, paging, installation, source registration, deployment, arming, trading or spend is authorized by this preparation.

- **Review correction at the next proposal commit (not an effective freeze):** the independent Claude [review of `54f4509`](https://github.com/Joshua-Asante/first-passage/pull/713#issuecomment-6008392566) confirms the common-timeout arithmetic and identifies P2-1 start gaps, P2-2 poll measurement and P3-1 stale owner references. C4's relayed ruling selects the host-supplied clock wrapper, pins the existing notifier read order, and signs its `book_host.py` footprint. §0.5.9, §3.3, §4 and HH7 now specify the duration/poll/consecutive-pass gates, first-pass/reset rules, cross-thread exclusion, oversleep, delayed lock, late-return and backward-wall-clock cases. Active freeze/decision references name coordinator (4); coordinator (3) remains only in historical rulings. Source timing/code anchors are unchanged from the preparation base; no implementation or owner file is edited. Reviewer recheck and C4 binding acceptance remain owed.
