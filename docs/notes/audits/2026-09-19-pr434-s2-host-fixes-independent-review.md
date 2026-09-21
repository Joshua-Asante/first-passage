# PR #434 independent review — S2 CI supervision job + six S2 host-side fixes

Reviewer: read-only, 2026-09-19. Repository untouched. Diff reviewed: `fed0450..f2606b0` restricted to the
#434 branch (second parent `cf4c6d8`; 17 branch commits `16a03c7..cf4c6d8`). Non-#434 content that rode
in through the merges (`c9c7f53` = #433 tail, `3151b38` = origin/main) was identified and excluded
(`campaign_funding.py`, `test_campaign_funding.py`, `tests.yml`, `test_qualification_isolation.py`).

External sources checked (fetched to scratchpad, cited by line): systemd **v255** (Ubuntu 24.04 ships
255.4) `src/core/{dbus-manager,dbus,dbus-util,dbus-unit,dbus-job,dbus-cgroup,cgroup,service,scope,slice}.c`,
`src/busctl/busctl.c`; polkit `src/polkitbackend/{init.js,polkitbackendduktapeauthority.c}`; Linux v6.8
`Documentation/admin-guide/cgroup-v2.rst`, `mm/memcontrol.c`. GitHub Actions run metadata via `gh` (read).

## Verdict

No BLOCKING finding. All six fixes are correct against the failures they repaired, and the systemd
justification for both semantic changes is accurate on the systemd side. One of the two recorded
justifications overstates what now carries "group OOM termination" (ADVISORY-1); the evidence ledger cites
a run that is not head-bound while a head-bound green run exists but is unrecorded (ADVISORY-2). Details
below; counts and verbatim list at the end.

## Lens 1 — correctness of the six fixes

| # | Failure (run) | Fix | Verdict |
|---|---|---|---|
| 1 | `MemoryOOMGroup` rejected by `StartTransientUnit` (35453843198) | `campaign_host.py:35-40` sends only `MemoryMax/MemorySwapMax/MemoryAccounting/CPUAccounting` | **Correct.** systemd v255 `dbus-cgroup.c` defines no `MemoryOOMGroup` property (0 matches; Memory* vtable at :475-490, setters :1151-1279). An unknown name fails the whole call. Unit test `tests/test_qualification_campaign_host.py:47-65` pins the property set. |
| 2 | Enrollment unreadable by the service in the `0o711` run root | `campaign_host.py:18-25` moves `campaign-host.json` to `code/qualification-installation/`; runtime reads `Path(config['installation_root'])/'campaign-host.json'` (`campaign_supervisor.py:405-407`) | **Correct.** Run root is created `0o711` (`host.py:544`); `read_regular` pins every directory (`files.py:33-41`), which needs read on the directory. `code/` is root `0o755` (`host.py:587`); `installation.mkdir(mode=0o755)` precedes `campaign_host.install` (`fixture_install.py:39,65`) and `installation_root` is that directory (`fixture_install.py:52-53`). `install_release` (`release.py:56-83`) does not enumerate the directory, so the extra file is tolerated. Cleanup reads the same path (`campaign_host.py:114-117`) and runs before tree removal (`host.py:698-700`). |
| 3 | `common scope requires group OOM termination` unsatisfiable | Runtime check removed (`campaign_supervisor.py:416-421`); installer verifies only `memory.max`/`memory.swap.max` (`campaign_host.py:61-64`) | **Correct as a fix; see Lens 2 for the justification's scope.** |
| 4 | busctl `invalid option -- 'I'` (35456019676) | `--` inserted before `call` (`container_ownership.py:72-77`) | **Correct.** `busctl.c:2400` uses `getopt_long(argc, argv, "hH:M:qjl", ...)` — no leading `+`, so GNU permutation scans the later `-I`/`--attempt`; `--` ends option parsing. `bootstrap.py:25,33` imports the same constant, so the installed `campaign_control` prefix check stays consistent. Test `tests/test_qualification_campaign_host.py:95-105`. |
| 5 | polkit denied `StartTransientUnit` (rule threw on `action.lookup("unit").indexOf`) | New rule `campaign_host.py:82-87`: `unit === undefined || unit.indexOf(prefix)==0` → YES | **Correct as a fix.** polkit `init.js:4-6` returns `this["_detail_"+name]` — `undefined` when absent; a throwing rule ends `check_authorization_sync` with `!good → POLKIT_IMPLICIT_AUTHORIZATION_NOT_AUTHORIZED` (`polkitbackendduktapeauthority.c:1058-1060`), which is why the old rule denied rather than "skipped". See Lens 2 for scope. |
| 6 | SQL `LIKE 'supervision_control_%'` matched `supervision_controller` (KeyError 'data', 35459484982) | `GLOB 'supervision_control_*'` (`campaign_store.py:262-268`, `campaign_host.py:134`) | **Correct.** GLOB treats `_` literally. Regression test `tests/ops/qualification/execution/test_campaign_scheduler.py:484-495`. Only remaining `LIKE` in the qualification tree is the sqlite_master query (`attempt.py:384`), harmless. Adjacent latent collision remains — ADVISORY-3. |

Also in the PR and checked: guardian poll cost (`campaign_supervisor.py:867-882,903`: 200 ms poll, authority
re-read once/s; `authority_checked=0.0` makes the first iteration check immediately); settlement race in
`test_s2_two_descendants_exhaust_owned_cpu` (`test_campaign_supervision_linux.py:92-95`, waits for
`observation_bytes_b64` — tighter, not weaker); guardian CPU tolerance (`:154-158`, NOTE-4);
`service.py:574-578` prints tracebacks only for non-`ValueError` defects; `_control` error text
(`campaign_supervisor.py:456-460`) now carries the control child's stderr tail.

## Lens 2 — the two semantic changes

### (3) common slice no longer asserts `memory.oom.group=1`

Recorded justification (ledger `2026-09-18-full-e1-execution-slices.md:515`; `campaign_host.py:31-33,51-53`;
`campaign_supervisor.py:417-421`): systemd rewrites the attribute on every realization and sets 1 only for
`OOMPolicy=kill` service/scope units, never a slice; group OOM termination "is carried by the guardian unit's
`OOMPolicy=kill` and the payload's `BindsTo` interlock".

systemd v255 check — **accurate**:
- `cgroup.c:1881` writes `memory.oom.group = one_zero(c->memory_oom_group)` unconditionally whenever the
  memory mask is applied (`cgroup_context_apply`, called from realization at `cgroup.c:2555`;
  `unit_realize_cgroup_now` :2929 returns early at :2941 only when the realized/enable masks are unchanged —
  a child that needs a new controller in the parent re-applies the parent's attributes, so a manual root-side
  write would be reverted at the first guardian start (`TasksMax=1` enables `pids`)).
- `memory_oom_group` is assigned only in `service.c:846` and `scope.c:178` (`= oom_policy == OOM_KILL`);
  `slice.c` never sets it → slices always read `0`.
- No D-Bus property exists for it (Lens 1 #1).

Kernel check — the sentence "group OOM termination lives on the guardian unit and the BindsTo interlock"
**overstates**:
- `mm/memcontrol.c:2151-2156` (`mem_cgroup_get_oom_group`) walks from the victim's memcg up to the OOM
  domain and takes the *highest* memcg with `oom_group` set; if none, one task dies
  (`cgroup-v2.rst:1328-1344`).
- Under #434: host slice `0`, campaign/work/payload slices `0`, Docker's container scope `0`
  (runc's systemd driver delegates; `scope.c:175-176` → delegated scope defaults to `OOM_CONTINUE`), guardian
  `1` but it is a single-task cgroup (`TasksMax=1`, `campaign_supervisor.py:146`).
- Therefore a common-slice OOM whose victim is a payload process is a **single-process kill**; the payload
  is not group-killed, and `BindsTo` (`:153`) only fires when the *guardian* dies. The guardian's poll loop
  (`:878-903`) checks CPU only, never `memory.events`; OOM is read at settlement
  (`observation()` :488-490) and flips the attempt to `BUDGET_EXHAUSTED`
  (`campaign_store.py:804-811`). So authority is fail-closed, but "stop on OOM" (plan S2 Behavior, :140)
  is immediate only when the container's init process is the victim; otherwise the payload runs to its
  CPU or wall bound (≤300 s/phase) with a partially killed tree.
- The spec's shared-counter invalidation ("group OOM can invalidate every attempt on that host",
  spec :277) still holds, because `observation()` reads the *parent's* hierarchical `memory.events`
  (`:489`, cgroup v2 `memory.events` includes descendants) and counters are never reset.
- `docs/superpowers/plans/2026-09-19-s2-local-supervision.md:11` still says the host slice "shares
  MemoryMax, swap=0 and group OOM"; that is now false for group OOM.

→ ADVISORY-1.

### (5) qexec polkit rule allows `manage-units` when no `unit` detail is present

Recorded justification (ledger :515; README `tools/qualification_verification/README.md:165-170`;
`campaign_host.py:77-81`): `StartTransientUnit` is authorized by systemd's generic check with no details, so a
transient start cannot be prefix-bound; inside the trust model; `campaign_control` still hard-checks the
fixed command prefix.

systemd v255 check — **accurate**:
- `dbus-manager.c:1087-1110`: `method_start_transient_unit` → `bus_verify_manage_units_async` (:1108) →
  `dbus.c:1191-1192` passes `details = NULL`.
- Unit-scoped verbs go through `bus_verify_manage_units_async_full` (`dbus-util.c:151-175`) with
  `"unit", u->id, "verb", verb` → the `indexOf(prefix)==0` branch does bind start/stop/kill/reset of
  existing units to the prefix.
- Other details-less `manage-units` sites the new rule also grants qexec: `method_clear_jobs`
  (`dbus-manager.c:1185`), `method_reset_failed` (:1206), `method_enqueue_marked_jobs` (:2146),
  job cancel (`dbus-job.c:57`). None exceeds what `StartTransientUnit` already grants.

Weakening assessment: `StartTransientUnit` with no name/property constraint lets qexec start any transient
unit, including `User=root` services — i.e. polkit no longer contributes any containment for qexec's unit
starts. The prior rule never authorized transient starts at all (it threw → NOT_AUTHORIZED), so the change
is deny→allow-all-transient, not bound→unbound. Neither the spec nor the S2 plan/handoffs require a polkit
prefix bind (grep: no `polkit`/`manage-units`/prefix requirement in `2026-09-17-protected-full-e1-campaign.md`,
`2026-09-18-full-e1-execution-slices.md` S2 slice, `2026-09-19-full-e1-s2-*.md`,
`2026-09-19-s2-local-supervision.md`). The README trust model (`README.md:13-17`) already declares qexec
root-equivalent. What now keeps units inside the attributed hierarchy is code only:
`guardian_unit_spec` fixes `Slice=work_slice` (`campaign_supervisor.py:143`), the guardian verifies its own
cgroup and `pids.max` (`:763-768`) and its `RLIMIT_CPU` (`:775`), and the probe verifies the container's
cgroup is under the payload slice (`:890-892`). `campaign_control` (`bootstrap.py:33`) checks only the
busctl prefix up to the signature, not the unit name or properties.

→ ADVISORY-4 (wording + optional hardening). Not blocking under the recorded trust model.

## Lens 3 — evidence integrity

- Wrapper (`scripts/qualification_boundary_verification.py`): `--s2` runs the whole S2 file (:97),
  requires `passed == collected` with zero failed/errors/skipped (:39-45), requires the 7 registered nodes to
  be present-and-passed (:79-82,:109; manifest `invariant_manifest.json:366-372`;
  `check_qualification_invariants.py:171-177,251-257` report renamed/deleted nodes as missing), and requires
  owned cleanup `ok=True` (:111-114). A run cannot claim more than it proves on these axes.
- The two cases added by #433/#434 (`test_s2_private_route_is_service_peer_only_and_bounded_in_framing`,
  `test_s2_warm_service_starts_one_guardian_per_work_with_no_scheduler_unit`) are **not registered** in the
  manifest; their deletion would not be detected by `invariants.json passed=true` — ADVISORY-5.
- Workflow (`qualification-s2-supervision.yml`): `pull_request` is path-filtered (:12-23) — no `push`
  trigger, so no run exists on `main` after merge; `concurrency.cancel-in-progress` (:28-30) cancelled the
  intermediate heads (c9c7f53, 3151b38). Not a required check (by design, :7). Cleanup step exits with the
  cleanup status (:76-78,:95); a missing manifest exits 0 only when provisioning already failed the job
  (:70-73). Artifact `if-no-files-found: warn` (:102) is harmless because the run step is the gate.
- Head-binding of the recorded evidence: the ledger (`…execution-slices.md:511`) cites run **35460338493**
  at `77dee89`. After that head the branch changed materially (`campaign_store.py` base class,
  `campaign_host.py` imports, the tolerance edit `cf4c6d8`, plus the #433 tail via `c9c7f53`). Run
  **35463688322** at `afa6b90` **failed** (CPUUsageNSec 12.998549 s); the tolerance edit was then made and
  run **35464802898** at `cf4c6d8` (pull_request merge-ref) is **green: "9 passed in 548.01s",
  `verification_exit_code 0`, `source_stable true`**. That head-bound run is not recorded in the ledger —
  ADVISORY-2.
- `record.data['metadata']['purpose']` reads `'boundary_acceptance'` for `--s2` (:69) although
  `acceptance_scope='S2_DIAGNOSTIC_SUPERVISION'` — NOTE-1.
- Journal export (`:83-88`) is the whole boot journal; `run_id` is already public
  (`host.py:66-73`), keys never enter logs by design; `service.py:577` tracebacks contain paths/messages
  only — NOTE-2.

## Lens 4 — fail-closed / fail-open

- Fail-closed, correct: `_realize_common_slice` refuses an unrealized or divergent slice
  (`campaign_host.py:57-64`); runtime refuses limit/swap drift (`campaign_supervisor.py:413-415`);
  cleanup refuses a populated scope (`campaign_host.py:124-125`) and propagates to `require_cleanup`;
  `_control` refuses non-zero exit or non-job acknowledgement (`:456-464`); guardian self-checks
  (`:763-775`); every guardian exception routes through `recover_campaign_work` (`:822-826`).
- Spurious-refusal risks (closed, not open): exact `memory.max` string compare needs page-aligned
  `memory_bytes` (256000000 = 62500×4096 today; a non-aligned future value would refuse) — NOTE-3; a
  ≤50 ms window between systemd's `mkdir` and attribute write could read `memory.max`=`max` and refuse
  (bounded by the 5 s deadline loop only on `exists()`, not on value) — NOTE-3.
- No fail-open found. The only softened assertion is the 10 ms lower tolerance on `CPUUsageNSec`
  (`test_campaign_supervision_linux.py:158`); the load-bearing facts (`ActiveState=failed`,
  `ExecMainStatus=9`, `LimitCPU=LimitCPUSoft=13`, upper bound 14 s) are unchanged — NOTE-4.
- Polkit: `subject.user` undefined → `!= "qexec"` → NOT_HANDLED; rule file written `xb` after the
  enrollment is durable (`campaign_host.py:91-95`); partial installs are retired by cleanup
  (`:112-159`, `host.py:698-700`).

## Lens 5 — N1_ONLY boundary path

No regression found.
- `conftest.py:68-77` now converts installer `CalledProcessError` to `AssertionError`; no N1 test expects
  `CalledProcessError` from `admin()`/`prepare()` (grep of `tests/integration/qualification_boundary/test_*.py`).
- `conftest.py:45-48,86-96`: `ClientProcessError` subclasses `CalledProcessError`, keeps `.stderr` and the
  `returned non-zero` message; N1 tests that depend on both (`test_boundary_lifecycle.py:161,351-354`,
  `restart()` :217-219) still work.
- Enrollment relocation and `campaign_host.cleanup` early return (`:115-116`) are S2-only paths; the N1
  installer never calls `campaign_host.install` (`fixture_install.py:58-65`).
- Evidence: N1 boundary run **35460340344** at `77dee89` green on both hosts; `conftest.py` did not change
  after that head.

## Findings

### BLOCKING
None.

### ADVISORY
- **ADVISORY-1 — "group OOM termination" justification overstated; stop-on-OOM is not immediate.**
  Scenario: the `descendants`-style payload (container init + children) drives the common slice to
  `memory.max`; the kernel kills one child (`memcontrol.c:2151-2156`; every cgroup between victim and the
  slice reads `memory.oom.group=0`); the container keeps running; the guardian loop
  (`campaign_supervisor.py:878-903`) checks only CPU, so the payload continues until the CPU or 300 s wall
  bound; only settlement (`:488-490` → `campaign_store.py:810`) marks `BUDGET_EXHAUSTED`. Authority is
  fail-closed; the "stop" is late. Fix options: (a) read the parent's `memory.events` `oom_kill` in the loop
  and kill+`IN_DOUBT` on increment; (b) at minimum correct the wording in the ledger (:515),
  `campaign_host.py:51-53`, `campaign_supervisor.py:417-421`, and
  `2026-09-19-s2-local-supervision.md:11` ("group OOM" no longer holds on the slice).
- **ADVISORY-2 — ledger cites a non-head-bound run; the head-bound green run is unrecorded.**
  Scenario: an auditor binds record `715817af…` to the merged bytes and finds it was produced at `77dee89`,
  before the `cf4c6d8` tolerance edit that answered a *failed* run (35463688322). Record run
  **35464802898** (`cf4c6d8` merge-ref, 9 passed, exit 0, source_stable) in the ledger as the head-bound
  evidence, and note the intermediate failure and its fix.
- **ADVISORY-3 — role-namespace collision survives the GLOB fix.** `role = 'supervision_' + work_id`
  (`campaign_store.py:327`) shares a prefix with `supervision_control_…`/`supervision_event_…`. A work
  named `control_x` or `event_x` (identity regex allows it, `protocol.py:77-80`) would be parsed as a
  control claim/event: `_recovery_pending` KeyError (`:268-270`) and, on the next store open, the integrity
  walk (`:1073-1089`) raises → the service refuses to start for the whole host. Reachable only from the
  service-UID private route today (`service.py:348-349`; SUBMIT_E1 fixes `work_id='admission'`, :308), so
  not exploitable by qclient, but S3+ checkpoint names must never start with `control_`/`event_`. Fix:
  reject those prefixes in `identity()`-adjacent validation for work ids, or use a separator that cannot
  occur in identities.
- **ADVISORY-4 — polkit wording and residual containment.** README :165-170 and ledger :515 should state
  plainly that qexec may now start arbitrary transient units (including `User=root`), so polkit provides no
  containment for transient starts and hierarchy membership rests on code
  (`campaign_supervisor.py:143,763-768,890-892`); `campaign_control` (`bootstrap.py:33`) checks only the
  busctl prefix. Optional hardening if a prefix bind is ever wanted: a root-owned template unit
  (`fpq<hash>-guardian@.service`) started via `StartUnit` (details present → prefix-bound) with per-work
  properties set through unit-scoped `SetUnitProperties`.
- **ADVISORY-5 — two S2 cases unregistered in the invariant manifest.** Scenario: a later edit deletes
  `test_s2_private_route_…` or `test_s2_warm_service_…`; the run still reports 7/7 registered nodes and
  `invariants.json passed=true`. Register both in `tests/ops/qualification/invariant_manifest.json`.

### NOTE
- **NOTE-1** `purpose: 'boundary_acceptance'` for `--s2` records (`qualification_boundary_verification.py:69`);
  `acceptance_scope` disambiguates, but the label invites over-reading.
- **NOTE-2** Whole-boot `journal.log` export (`workflow:88`) and the new `_control`/RPC error tails
  (`campaign_supervisor.py:456-460`, `service.py:578`) carry paths, unit names and manager refusal text; no
  key material by construction. Keep exception messages free of request bytes.
- **NOTE-3** Exact `memory.max` read-back requires page-aligned `memory_bytes` (currently aligned) and a
  50 ms poll that could observe `max` pre-attribute; both refuse rather than pass.
- **NOTE-4** `CPUUsageNSec` lower tolerance (10 ms) was chosen after one observed 12.998549 s sample; the
  comment attributes it to cgroup-sample skew, which is consistent with RLIMIT_CPU being enforced on
  process cputime at tick granularity. Primary assertions unchanged.
- **NOTE-5** `_start_common_slice` (administrator side) omits `--`; its arguments contain no
  dash-prefixed values, so it is not exposed to the busctl permutation.
- **NOTE-6** `campaign_host.cleanup` returns early when the enrollment file is absent (`:115-116`); a host
  enrolled with the pre-#434 layout would keep its slice/rule. Disposable hosts only; no live case.

## Summary

BLOCKING: 0 · ADVISORY: 5 · NOTE: 6

BLOCKING items (verbatim): none.
