# S5 Part A measurement harness and dispatch-only workflow (H1 step (b))

**Status:** EXECUTED 2026-09-28 (see [Measurement execution](#measurement-execution-2026-09-28)). *Earlier status, kept as history:* PREPARED, NOT RUN. This directory holds the harness for the bounded S5 Part A measurement. Nothing in it has been measured. No engine workload, Stage 1a, Stage 0 or Stage 1b dispatch, re-run or artifact download has run. Output class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`. S5 stays **HELD**.

**Authority:**
- **Ruling:** the CP-1a ruling at commit `baa09ffd`, the ledger entry "Operator ruling — CP-1a decisions (1)–(6) adopted as recommended, hold kept, 2026-09-27". Read it with `git show baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`; it is on [#523](https://github.com/Joshua-Asante/first-passage/pull/523) and not yet on `main`. Decision (2) approves the bounded measurement dispatch of r2 §12. Decisions (1), (3), (4) and (6) set the parameters, the N2 value, the D2 split and the seam that this harness's stop screens use.
- **Dispatch record:** commit `61a2ca41`, `docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md`, "H1 steps (b) and (c): dispatch record (frozen 2026-09-27)". Where it differs from the inline brief, it governs.
- **Packet:** [r2](../2026-09-27-s5-part-a-measurement-proposal-r2.md) at `origin/main` `875ecf29`, including its §16 reconciliation. Where §16 or a dated correction amends earlier r2 text, the amendment governs.
- **Operator ruling 2026-09-27 on the returned harness:** r2 §12.9 and the dispatch record's "Amendment 2026-09-27: step (b) re-opened narrowly by operator ruling", both at commit `79985508` on [#523](https://github.com/Joshua-Asante/first-passage/pull/523). Read them with `git show 79985508:<path>`. Where they differ from anything else here, they govern.

## Files

| File | Role |
|---|---|
| `measure_part_a_max.py.txt` | The harness (r2 §6.3). The `.py.txt` suffix keeps it out of the import-boundary gate; `python <path>` runs it |
| `README.md` | This note |
| `../../../.github/workflows/qualification-s5-part-a-measurement.yml` | The dispatch-only Stage 1b workflow (r2 §12.3); it also runs Stage 1c (`stage=1c`) unchanged |
| `../../../tests/test_s5_part_a_measurement_harness.py` | The regression module the amendment allows. It loads the harness from its `.py.txt` path and uses synthetic inputs only |

r2 names no other support file. The accounting probe is the inline script r2 §12.3 step 6 prescribes, embedded in the workflow. The fixture is the existing `tests/ops/qualification/composition_fixture.py`, which the harness imports unchanged.

## Acceptance checks (amended 2026-09-27)

The amendment replaces the earlier PRELIMINARY checks with these:
- the committed regression module;
- subprocess tests of the exit semantics through the real `--summarize` and combine entry points;
- the workflow check, which shows record, cleanup and upload still run after an exit 3, and actionlint;
- launcher records on the final head for the module (serial and `--workers 2`) and for `check`.

These establish tooling behavior only. They are not a measurement.

**Measurement readiness is established later, not by these checks:**
- Windows **Stage 1a** on the operator's host (r2 §12.2);
- the approved Linux **accounting probe and dry run** (r2 §12.3). These include the I-1/I-6 failure handling, unit and artifact cleanup, and the image-first feasibility below.

The static image-context inspection below is an input to that feasibility, not proof of it.

## Image-first finding (CP-1a decision (2)(d))

**Finding: the worker image's build context cannot carry the harness or its fixtures. The workflow therefore defaults to `host_venv`, and it refuses `worker_image`.** PA-5 at C3 validates the host-to-container mismatch, as the ruling directs. Evidence, by static inspection at `875ecf29`:

1. **The context holds only the worker's import closure.** `prepare_context` builds its payloads from `source_closure(source, 'worker')` alone (`ops/c1_rail/qualification/execution/image.py:17-18`). It adds only `requirements-ops.lock` and the signing configuration (`:22-23`). The generated Dockerfile has one `COPY` line per payload and no other source (`:27-32`). `prepare_context` takes no parameter for extra files (`:13`).
2. **The closure cannot reach `tests/` or `docs/`.** `ENTRYPOINTS['worker']` is `c1_rail.qualification.execution.worker` (`ops/c1_rail/qualification/execution/runtime.py:15-17`). `source_closure` follows static imports from that entrypoint (`:26-64`, roots at `:28`). A static closure computation at `875ecf29` returned 64 files, all under `core/`, `deploy/` and `ops/`; none is under `tests/` or `docs/`. The fixture modules the harness needs are not in the closure: `composition_fixture.py`, `runtime_fixture.py`, `test_contract.py` and `test_trust_domain.py`. The harness itself is a `.py.txt` file, not an importable module. The existing test pins exactly this file set (`tests/test_qualification_worker_image.py:11-22`).
3. **The image's only entry is the worker role.** The Dockerfile's `ENTRYPOINT` is `bootstrap.py worker` (`image.py:37`). The bootstrap accepts only fixed process roles (`deploy/qualification/bootstrap.py:15-16`) and requires root-owned installed code (`:11-14`).
4. **The repository `.dockerignore` does not apply.** It scopes the Fly build of `deploy/c1_rail/Dockerfile` (`.dockerignore:1-19`). The worker build uses its own generated context directory (`image.py:26`, `:63-67`).
5. **The image is built only inside the boundary suite.** `build_worker` needs host state `host_ready_boundary_unconfigured` (`image.py:48`). Its only caller is the integration fixture (`tests/integration/qualification_boundary/conftest.py:58`), not `provision.sh`.

Carrying the harness in the image would need a change under `ops/` (the closure or `prepare_context`). That is outside step (b)'s allowed files. Two further facts are recorded for the feasibility read, not decided here:
- the image sets `PYTHONDONTWRITEBYTECODE=1` (`image.py:27`) and the bootstrap sets `sys.dont_write_bytecode` (`bootstrap.py:18`), so a worker never has warm bytecode;
- the dependencies would be present, since `pytest` is in `requirements-ops.lock` (`:1008`) and `cryptography` in the signing requirements (`tools/local_verification/requirements-extra.txt:6`, installed at `image.py:35`).

## Harness modes (r2 §6.3)

- **`--repeat-mode`** runs one repeat in the current process. On Linux it runs inside a unit; on Windows it runs as a job-object child of `--launcher`. Its steps follow r2 §6.3:
  - **(1) Clocks.** The engine is imported first, then the `start` clocks are read before any fixture import.
  - **(2) Setup.** `build_verified_composition(tmp, confirmation_depth=60, decision_alpha='0.05')` runs. The one `ProductionSource._build_composition` call is timed by a single wrapper that is removed as soon as setup returns. `admission` is charged; the rest of setup is `setup_excluded`.
  - **(3) Verify.** `verify_for` runs once.
  - **(4) Request.** It is `production._part_a_request(...)`, then `within_pp = 1.0` for `forced`, with `budget_seconds = 3600`.
  - **(5) Engine.** `_run_part_a(..., full_pass_rate=1.0, synthetic=True)` runs, with the clocks read immediately around it.
  - **(6) Serialize.** A stand-in canonical serialization (sorted-key compact JSON of `asdict`) of the prefix and the final panels.
  - **(7) Assert.** Forced must give 4 panels, expanded; prescribed must give 2, not expanded.
  - **(8) Memory.** The in-unit memory read is the last act (r2 §8.2). It reads `/proc/self/cgroup`, then `memory.peak`, `memory.swap.max`, `memory.swap.peak`, `memory.events` and `cpu.stat`. It is complete only if the path ends in the repeat's own unit name. `_peak_memory_bytes()` is always recorded as the lower bound.
  - **(9) Row.** One JSON row, never overwritten, even for a failed repeat. The exit code is 0, 5 (assertion) or 1 (error).
- **`--launcher`** (Windows only, Stage 1a) spawns each repeat with `CREATE_SUSPENDED`, assigns it to a fresh job object, then resumes it. It reads `TotalUserTime + TotalKernelTime`, the outer wall and the exit code. It purges the checkout's `__pycache__` before each arm's repeat 1 and does not drop the page cache (r1 §3.2). The order per arm is repeats 1..N, then instrumented repeat 0.
- **`--summarize PATH`** takes a Linux job directory or a Windows bundle. It writes `record.json` (for a bundle, `<bundle>.record.json`) in schema `s5-part-a-max-expansion-measurement/v2`. It exits 0 (valid), 3 (validity failure, re-runnable) or 4 (invalid, no re-run).
  - Given several per-job `record.json` inputs and `--record`, it writes a combined record. Ĉ, Ŵ, M̂ and P̂ are then maxima over both jobs (r2 §6.2), and the between-job median ratio is recorded as host variance. It refuses, writing nothing, unless the inputs are exactly one job `a` and one job `b` per-job record with one common run id. Records that differ in, or lack, `measured_commit`, `dispatched_head`, `harness_sha256` or `source_sha256` are I-7.
  - Combining also refuses in two more cases. The first is when the combining checkout is not the code that measured: its HEAD, harness SHA-256 or recorded source SHA-256s differ from what both records carry. Run the combine from the recorded revision. The second is when a job's artifact lacks `cleanup-receipt.json` for the same run, attempt and job with `cleanup_exit` 0, which the workflow's owned-cleanup step writes (r2 §12.3 step 9).
  - For a Windows bundle it compares the identity `--launcher` recorded after its last repeat (`executed_identity`: commit, harness SHA-256, source SHA-256s and `observe_runtime`) with the identity at summarize time. A missing identity, any mismatch, or an execution-time tracked tree that was not clean (`tree_clean_tracked` false or absent; r2 §5.1 "measured commit, clean tree") is I-7.
  - A record whose shape is not the fixed one (both arms; 5 timed repeats per arm in measure mode; r2 §6.2, §12.2) is `H-SHAPE`. `--launcher` still runs another shape for debugging, but it says so, and the bundle can never yield an acceptance record.
  - **Incomplete Stage 1b evidence (r2 §12.9 (3)).** A Stage 1b measure record, per job or combined, is incomplete when a required ceiling input is missing on either arm. The required inputs are any input to Ĉ, Ŵ or P̂, or to either arm's warm spread, on a completed timed repeat, for example an unset exit timestamp or `CPUUsageNSec`. The verdict is then:
    - `stop_class = INCOMPLETE_EVIDENCE`, with an `INCOMPLETE` reason naming each missing input;
    - `validity_ok = false`, `rule_applicable = false`, exit 3.

    `verdict.rerun_eligible` is true only when every failing job is on run attempt 1. The failure shares the single `--failed` re-run of §12.7 and grants no additional attempt, so on attempt 2 it stops the stage. An I-3 alongside keeps its own reason.
  - **Legacy bundles (r2 §12.9 (2)).** A Windows bundle without `timeout_s` or without `executed_identity` comes from a launcher older than this revision. Its verdict is `stop_class = LEGACY_UNACCEPTED`, `validity_ok = false`, `rule_applicable = false`, exit 4, with no re-run. The bundle stays readable and is never modified, deleted or upgraded; `--summarize` writes only `<bundle>.record.json` beside it. Stage 1a acceptance needs a bundle from the current launcher.
  - **Never rule-applicable (r2 §12.9 (4)).** Stage 1a and dry-run records always carry `rule_applicable = false`, whatever their exit code; an exit 0 there means only that their own requirements were met. Stage 1a does not need complete aggregate memory, and the incomplete-evidence gate applies to neither. `rerun_eligible` is null outside Stage 1b measure records.
  - **Dry-run requirements (reading of r2 §12.9 (4) and §12.7).** A dry run exists to show that the runner yields the measurement's inputs, so a completed dry-run repeat must carry them.
    - A missing runner accounting value (the unit's `CPUUsageNSec`, or its monotonic timestamps, which give `wall.outer` and so the workload wall) is I-1, exit 3, within the single dry-run re-dispatch. The reason names the exact value, for example `I-1: CPUUsageNSec unset on dry-run repeat forced-1`. The stop class keeps the §16 C8 label `MEMORY_EVIDENCE_MISSING`, which already covers an empty `CPUUsageNSec` in the probe; the reason text shows that no memory reading is missing.
    - A missing harness-emitted field is H-FIELDS, exit 4.
    - Only Stage 1b measure records move the ceiling-input fields out of H-FIELDS, into the incomplete-evidence gate.
    - A dry run is still never rule-applicable.
- **Workflow helpers** use the standard library only in their own process:
  - `--probe-verdict DIR` judges the accounting probe (r2 §8.4). For a Stage 1c job whose probe passed, it then stages SR-5 in a child process before the loop (see [Stage 1c path](#stage-1c-path-c3-2026-09-29)); its exit code stays the probe's;
  - `--check-stage STAGE` exits 0 for `1b` and `1c` (the `1c` path landed at C3). For `1c` it first self-checks the staging order and exits 2 if it is not shown.

It never drives the E1 route, the retired executor class or any service.

## Commands

**Stage 1a** (Windows host, grants `tests.run` and `worktree.write`; r2 §12.2):

```powershell
.\fp.ps1 doctor
$bundle = "docs/notes/2026-09-27-s5-part-a-measurement/windows-$((Get-Date).ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'")).json"
.\fp.ps1 python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --launcher --stage 1a --arms 'forced,prescribed' --repeats 5 --out $bundle
.\fp.ps1 python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --summarize $bundle --stage 1a
```

Each run writes its own UTC-stamped bundle (r2 §12.2): the launcher refuses to overwrite an existing bundle, and r2 §12.9 (2) forbids removing or overwriting one. *[Corrected 2026-09-27: the commands previously wrote a fixed `windows.json`, which a second run could not reuse.]* *[Corrected 2026-09-28: `--arms` is quoted. PowerShell reads a bare `forced,prescribed` as an array, and `fp.ps1` forwards it as two arguments.]*

Stage 1a validates the harness only. It checks panel counts, digest identity, prefix identity, all fields populated and call counts. Memory is always `UNVERIFIED` and the rule is never applied. A harness defect is fixed and re-run locally; it is not a validity-check count.

**Stage 1b** (the coordinator, after this file is on `main`; within the r2 §12.7 caps):

*[Coordinator record 2026-09-28: Stage 1b had already run under the ledger's H1(b) execution dispatch steps 3–4 as merged in #535, at 01:06–01:12 UTC, before the dispatch marker merged (#536, 03:18 UTC). The dry run was 36364714432 and the measure run 36364854404, both at head `7675c088`. Each run id was bound by listing this workflow's runs right after its dispatch: exactly one new run appeared each time, with its `headSha` confirmed, and the workflow has no other runs. Each run was watched to completion and its artifacts downloaded whole into a per-run directory, named by job and attempt. They are retained publicly under `stage1b/` and privately in first-passage-archive#844. The re-run decision was read from each job's record and summarize log: all exit 0, so no re-run was used. The executable sequence for any further Stage 1b dispatch is now r2 §12.3, merged in #539. It does not invalidate the executed runs; see the [CP-1b packet entry](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-cp-1b-packet--build-entry-status-2026-09-28).]*

```bash
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref main \
  -f stage=1b -f mode=dry-run -f runtime=host_venv -f note_dir=docs/notes/2026-09-27-s5-part-a-measurement
# after a clean dry run:
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref main \
  -f stage=1b -f mode=measure -f runtime=host_venv -f note_dir=docs/notes/2026-09-27-s5-part-a-measurement
# combine the two downloaded job records (one job a, one job b, one run), through the operations launcher
# (.\fp.ps1 python ... on Windows):
python -I scripts/fp.py python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --summarize <a>/record.json <b>/record.json --record <combined>.json
```

The lines above are the dispatches and the combine only. The executable sequence is r2 §12.3's dispatch block. It binds each dispatch to its run id, watches and downloads every run, reads the re-run decision from the downloaded records and cleanup receipts, and copies the evidence into `stage1b/`. *[Added 2026-09-28 (helper review of #523, C2, C3 and C7).]*

**Caps (r2 §12.7):**
- at most one re-dispatch of a failed dry run (I-1 or I-6);
- at most one `gh run rerun <id> --failed` of the measure dispatch (up to both jobs). Combining enforces this: it refuses a job record whose run attempt is outside 1–2, and it accepts the attempt-1/attempt-2 mixture a `--failed` re-run produces. The dry-run re-dispatch cap spans separate runs, so no single record can show it; the coordinator keeps that count;
- any failure after that stops the stage.

The artifact name carries the run attempt, so a re-run never replaces the failed attempt's evidence.

## Stage 1c path (C3, 2026-09-29)

Added under the operator GO of 2026-09-29 for authoring only (r2 §12.4). It lives on a measurement branch based on the S5 head (`<S5 head>` plus the harness commit only), never on the S5 branch. It is dispatched only after the coordinator records its read of this diff. The workflow is unchanged: it already accepts `stage=1c` and writes `git-parent.txt`.

**Repeat body** (`--repeat-mode --stage 1c`; r2 §12.4 replaces Stage 1b's steps 3–6):
- **(1) Clocks.** The worker and adapter modules (`execution.worker`, `execution.compute`) are imported first. The `start` clocks are then read, before any fixture import.
- **(2) Preconditions and P-7.** The harness checks that SR-1 `compute.PartAMeasurementOverride`, SR-3 `worker.run_part_a_body`, SR-4 `worker.write_part_a_artifact` and SR-6 `worker.PhaseBudgetGuard` exist; a missing one is I-8. The entry point is `worker.run_part_a_body`. P-7 is asserted as follows: it is the object bound to the global name that `run_worker`'s own bytecode loads (`run_worker.__globals__['run_part_a_body']`, with `run_worker.__globals__` the worker module's namespace and `'run_part_a_body'` in `run_worker.__code__.co_names`). The row records the qualified name, `id()`, both module SHA-256s and `identical`. The check is repeated after the call (`identical_after_call`). The harness calls that same object and nothing else; it never wraps or replaces it.
- **(3) Setup (excluded from Ĉ).** SR-5's staged mount is built once per job and copied, whole, into a repeat-local input directory. The copy is verified file by file against the staging manifest. Bundle verification, key loading and the PART_A plan check then run as `run_worker` performs them before the SR-3 body; this is the disclosed residual of r2 §7.6. Source admission is the worker's one `admit_source` call, charged as `admission` as at Stage 1b. The guard is `worker.PhaseBudgetGuard({'cpu_ns': 3600 s, 'wall_ns': 3600 s, 'memory_bytes': 64 GiB})` (SR-6).
- **(4) Boundary.** It opens immediately before the three staged predecessor files are read, with `worker.read_regular` in the worker's role order (`receipt`, `assessment`, `payload`). It then runs `run_part_a_body(context, plan, staged, admitted, budget, <repeat-local output>, measurement_override=...)`. The override is `PartAMeasurementOverride(within_pp=1.0)` for `forced` and `None` for `prescribed`. The boundary closes when the call returns, which is after the final artifact's fsync. `cpu.adapter` is that span; `cpu.workload = start + admission + adapter`.
- **(5) Assertions.** Forced must give 4 panels, expanded; prescribed must give 2, not expanded (I-5). The file check is `final[:len(initial)] == initial` (S5-D1). The files must equal the bytes the adapter returned, and the in-boundary staged capture must equal the manifest's; each failure is I-4. `measurement_forced` must match the arm (I-5), and P-7 must hold (I-8). Across arms, the forced initial-prefix digest must equal the prescribed initial-prefix digest (PA-4, P-6; I-4).
- **(6) Memory and row.** The in-unit memory read is exactly Stage 1b's: both stages call one shared helper. The row adds `n2_capture_sha256`, `initial_prefix_sha256` and `final_sha256` (r2 §12.4 "Files created"), `adapter_callable`, `n2_staging`, `n2_full_baseline` and the engine facts `probe_seconds`, `predicted_seconds` and `elapsed_seconds`. The instrumented repeat also records the call counts, which must match the same r2 §4 literals as Stage 1b, and `fsync_count`, which must be 2 (H-COUNTS).

**SR-5 staging (`--stage-n2 DIR`).** It builds `bundle_fixture.build_bundle(capability='FULL_E1', part_a=True)`, the composition fixture's workload with N2 depth 60. It then runs the genuine joint N2 `run_worker` once and stages its payload with the minimal receipt, assessment wrappers and PART_A plan, using `test_worker.part_a_stage_input` (the S5 worker tests' own SR-5 producer). The result is renamed into place only when whole, with a manifest of every file's SHA-256. The cache is `$RUNNER_TEMP/s5-part-a-measurement.n2-staged`, beside `$OUT`, so it is not uploaded; only its digests are recorded.

~~On Linux, the job's first repeat runs it in a child process, inside its unit, when the cache is absent. Its CPU is counted in `setup_excluded` through `RUSAGE_CHILDREN`. Its memory is in that unit's `memory.peak`, as all setup is (r2 §8.2).~~ *[SUPERSEDED 2026-09-29: the text struck here is the reviewed `0fe3e25` wording of decision 1's Linux placement; the correction below replaces it.]*

*[Corrected 2026-09-29 under the operator ruling "Fix harness, re-measure". Until this correction, the job's first repeat ran the staging in a child process inside its own unit when the cache was absent. That put the staging run's memory in the unit's `memory.peak`: in run 36634465166 the first repeat of each job peaked at 231,182,336 B (job a, forced-1) and 232,239,104 B (job b, prescribed-1), against about 157–158 MB for the other arm's cold repeat and 87–91 MB warm. That gave `PA3_FAILURE` from a workload that is not the PART_A payload.]* Staging now runs where no measured unit can see it:
- **Linux.** The workflow's probe step runs `--probe-verdict "$OUT"` (`.github/workflows/qualification-s5-part-a-measurement.yml:187`). It runs directly on the host venv, after `systemctl stop fp-s5pa-probe` (`:186`) and before the measurement loop step (`:189`) starts any `fp-s5pa-1c-*` unit (`:223-231`). When the probe passes and `git-parent.txt` is present, which the workflow writes only for `stage=1c` (`:112`), the verdict helper runs `scripts/fp.py --env <venv> python <harness> --stage-n2 <cache>` as a child, with the repeats' thread settings. It writes `n2-staging.json` to the job directory, which is uploaded. The file records the return code, wall time, children's CPU and peak RSS, the manifest and N2 digests, and the stager's own cgroup. Staging is refused if that cgroup is an `fp-s5pa-*` unit, or if a receipt or cache already exists. A failed staging keeps the probe's exit code, so the loop still runs and every repeat refuses.
- **Windows.** `--launcher --stage 1c` stages before the first job object, as before.
- **Repeats never stage.** A `--repeat-mode --stage 1c` repeat whose mount is absent, or has no valid manifest, refuses before any copy. The row records `n2_staging.refused` and exits 1; summarize makes it I-6.
- **Summarize (Linux 1c).** Once the loop has run, a missing or unreadable receipt is I-6, and so is a failed staging. A receipt that does not show `placement = probe_verdict_before_measurement_loop` and `stager_in_measured_unit = false` is H-SHAPE. So is a row with a non-null `generated_in_this_repeat`, the pre-fix placement. A completed repeat whose mount manifest SHA-256 is not the receipt's is I-4. The record carries the receipt as `n2_staging`.
- **`--check-stage 1c` (Validate inputs, `:108`)** checks two things before provisioning and exits 2 if either is not shown. First, the repeat-side functions reach no staging call, and the probe verdict does. Second, the workflow text still has this order: `git-parent.txt`, then the probe unit, the unit's stop, a direct host-venv `--probe-verdict` call not wrapped in `systemd-run`, and `--repeat-mode`.
- **Page cache.** The staged files' page cache is charged to the stager's cgroup. The cold repeat drops caches (`:217`), so its reads are charged to its own unit, and each repeat's copy of the mount is charged to that repeat. Nothing of the PART_A payload leaves a unit.

**Record additions (Stage 1c records only; Stage 1b records are unchanged):**
- `dispatched_parent`: `git-parent.txt` from the job directory, else null;
- `measured_parent`: `git rev-parse HEAD^` at summarize;
- `forcing.seam = adapter_measurement_override`, `forcing.adapter_callable_identity`, `forcing.p7_identity_all_repeats`;
- `n2_capture_sha256s` per arm.

A Linux Stage 1c job whose `dispatched_parent` is absent or differs from `HEAD^` is I-7. The coordinator still compares `dispatched_parent` with the S5 head reported at C3 (r2 §12.4); combining also requires both jobs to carry the same `dispatched_parent`. Stage 1c applies the Stage 1b validity rules and the same §12.7 caps. Its estimates are not provisional (Ĉ₁c; r2 §9 PA-1).

**Windows validation** (never a measurement): `--launcher --stage 1c --dry-run` runs one untimed, instrumented repeat per arm in job objects. Its summary is judged like Stage 1a: memory `UNVERIFIED`, never rule-applicable.

**Commands.** The sequence is r2 §12.3's dispatch block, with its Stage 1c form. Apply these substitutions throughout:
- title match `[stage 1b, ` → `[stage 1c, `;
- artifact prefix `s5-part-a-measurement-1b-` → `s5-part-a-measurement-1c-`;
- `S=<scratch>/s5-1b-…` → `s5-1c-…`;
- `D="$NOTE/stage1b"` → `D="$NOTE/stage1c"`, so the combined record is `stage1c/<run_id>-combined.json`;
- `-f stage=1b` → `-f stage=1c`;
- `--ref main` → `--ref "$BRANCH"`, the measurement branch on the S5 head;
- the step 2 check `repos/$R/commits/main` → `repos/$R/commits/$BRANCH`;
- messages that say "Stage 1b" → "Stage 1c".

It adds one check after each `fetch`: `jq -e --arg p "$S5_HEAD" '.dispatched_parent == $p' <job>/record.json`, where `S5_HEAD` is the S5 head reported at C3. A mismatch is I-7 (r2 §12.4) and stops the stage.

```bash
BRANCH=<measurement branch: the S5 head plus the harness commit>; S5_HEAD=<the S5 head reported at C3>
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref "$BRANCH" \
  -f stage=1c -f mode=dry-run -f runtime=host_venv -f note_dir=docs/notes/2026-09-27-s5-part-a-measurement
# after a clean dry run whose record carries dispatched_parent == $S5_HEAD:
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref "$BRANCH" \
  -f stage=1c -f mode=measure -f runtime=host_venv -f note_dir=docs/notes/2026-09-27-s5-part-a-measurement
# artifacts: s5-part-a-measurement-1c-<mode>-<job>-attempt<n>; retained under stage1c/<run_id>-<job>-attempt<n>/
# combine, from a core.autocrlf=false checkout at the measured head (the measurement-branch head):
python -I scripts/fp.py python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --summarize stage1c/<run_id>-a-attempt<n>/record.json stage1c/<run_id>-b-attempt<n>/record.json --record stage1c/<run_id>-combined.json
```

**Decisions r2 §12.4 left open:**
- SR-5 bytes are staged once per job and copied per repeat, not regenerated per repeat. This is r2 §12.6's nominal plan, not its contingency.
- The staging runs in a child process, so that no in-process cache warms the measured repeat.
- *[Corrected 2026-09-29, operator ruling "Fix harness, re-measure".]* The staging runs before the first timed or instrumented repeat and outside every measured unit. On Linux that is inside the probe step's `--probe-verdict` call; on Windows it is the launcher, before the first job object. A repeat never stages; without the staged mount it refuses (I-6). The earlier choice, staging inside the first repeat's unit and charging its memory as setup, is withdrawn: the staging run is not the PART_A payload, and its ~231 MB peak drove M̂ in run 36634465166. Rejected alternatives:
  - `--check-stage` runs on the system `python3` before provisioning (`:108`), so the repository dependencies are absent.
  - The dry run is a separate dispatch whose `$RUNNER_TEMP` does not persist, and its repeat is itself a unit.
  - Staging in a nested `systemd-run` unit from inside the first repeat would work as root, but it is more moving parts inside the loop's poll bound.
  - A per-fd `memory.peak` reset (kernel ≥ 6.12) cannot reset the systemd `MemoryPeak` that the loop reads with `systemctl show` (`:245`), which would still carry the staging peak.
- The boundary opens before the receipt and assessment reads, not at the payload's first byte. This charges two small reads more, the conservative direction.
- Admission is the whole `admit_source` call, including its internal `verify_for`.
- The memory limit is 64 GiB.
- An S5-D1 prefix failure is I-4, not I-5.
- The parent check is I-7 at summarize.

## Validity and stop classes (r2 §12.7 with §16 C8 and ruling (4))

| Code | Condition | Exit | Stop class |
|---|---|---|---|
| I-1 | Accounting probe failed (memory.peak below 64 MiB or absent, swap on, `CPUUsageNSec` empty), `probe.json` missing, truncated or not an object, or a dry-run repeat without the runner's `CPUUsageNSec` or unit timestamps | 3 | `MEMORY_EVIDENCE_MISSING` (§16 C8 relabel); memory `UNVERIFIED`, `rule_applicable = false` |
| I-2 | Warm CPU spread > 1.30 in an arm (Stage 1b; informational at 1a) | 3 | `INVALID_MEASUREMENT` |
| I-3 | A timed (or dry-run) repeat has no complete aggregate memory reading | 3 | `MEMORY_EVIDENCE_MISSING`; memory `UNVERIFIED`, `rule_applicable = false` |
| I-4 | Digests differ within an arm, or the forced prefix differs from the prescribed result | 4 | `INVALID_MEASUREMENT`; bears on D3 R7 only after diagnosis (§16 C8) |
| I-5 | Panel-count or `expanded` assertion failed | 4 | `INVALID_MEASUREMENT` |
| I-6 | A repeat exited non-zero, timed out (30 min poll bound, capped by the loop deadline), OOMed, left no row, or was not started before the loop deadline; or a measure-mode cold repeat (repeat 1) whose purge is not shown to have succeeded; or (Stage 1c) a repeat refused for want of the staged SR-5 mount, or the Linux pre-loop staging receipt is missing or failed | 3 | `INVALID_MEASUREMENT` |
| I-7 | Measured head differs from the dispatched head, or the tree is dirty (Stage 1b). A missing dispatched head, start head (`git-head.txt`) or summarize-time head also counts | 4 | `INVALID_MEASUREMENT` |
| I-8 | Stage 1c: an SR symbol the path needs is missing (SR-1 `PartAMeasurementOverride`, SR-3 `run_part_a_body`, SR-4 `write_part_a_artifact`, SR-6 `PhaseBudgetGuard`), or the P-7 identity is not shown before or after the call (r2 §7.7) | 4 | `BLOCKED` |
| H-FIELDS | A completed repeat left a required field empty. For Stage 1b measure records the ceiling-input fields are judged by INCOMPLETE instead; in a dry run the runner accounting values are I-1 | 4 | `INVALID_MEASUREMENT` (harness defect) |
| H-SHAPE | The record is not both arms with 5 timed repeats per arm (measure mode; r2 §6.2, §12.2) | 4 | `INVALID_MEASUREMENT` (not an acceptance shape) |
| H-COUNTS | A completed instrumented repeat's call counts differ from the r2 §4 literals (forced 14 replays, 5 proofs, 15 `verify_for`; prescribed 8, 3, 9), or are absent | 4 | `INVALID_MEASUREMENT` (harness defect: not the specified workload) |
| INCOMPLETE | Stage 1b measure, per job or combined: a completed timed repeat of either arm lacks an input to Ĉ, Ŵ, P̂ or a warm spread (r2 §12.9 (3)) | 3 | `INCOMPLETE_EVIDENCE`; `validity_ok = false`, `rule_applicable = false`, `rerun_eligible` only on attempt 1 |
| LEGACY | Stage 1a bundle without `timeout_s` or `executed_identity` (r2 §12.9 (2)) | 4 | `LEGACY_UNACCEPTED`; the bundle is retained unmodified |

From a valid record with complete memory:
- **Σ screen.** If the r2 §10.2 Σ-only row fails, the stop class is `D2_ACCOUNTING_FALSIFIER` (ruling (4)(i)). The row uses N2 at 360 s / 900 s (ruling (3)) and the P4 tuple extended to `/v7`. It fails when `max(120, max(2Ĉ, 1.5P̂) + 20) > 8,440` or `max(300, 3(Ŵ + 30)) > 6,100`.
- **PA-3a screen.** If `1.5 × M̂ > 256,000,000`, the stop class is `PA3_FAILURE`, which goes to an operator ruling.

Both are **screens, not the r2 §13 application**. The coordinator computes X and Y and records the ledger entry. Missing permission or a run not executed never engages D2 (ruling (4)(ii)). A per-job record's screen is a lower-side indication; the combined record is authoritative.

## r2 ambiguities resolved here (none changes a measured quantity)

- **Admission wrapper timing.** r2 §6.1 says the wrapper is "removed before step 2". It is removed as soon as the fixture setup returns, before `verify_for`, as r1 §3.1/§3.3 state ("removed immediately after").
- **Wall `start`.** It cannot be read in process. The workload wall is `outer − setup_excluded` (r1 §3.1), where `outer` comes from the unit's `ExecMainStart/ExitTimestampMonotonic` (Linux) or the launcher's clock (Windows). Per-boundary `perf_counter` spans are kept under `wall.boundaries`.
- **Fail closed.** Every input the verdict or ceiling uses must be present and in range. When one is absent, `[not set]`, null or out of range, the record is incomplete or invalid; the harness never falls back to another value:
  - **CPU input.** Ĉ's per-repeat input needs both `C_w` and the unit's `CPUUsageNSec` (on Windows, the job object's CPU). If either is missing, the repeat has no CPU input and the ceiling is `INCOMPLETE`.
  - **Completed repeat.** A repeat counts as completed only if all of these hold: its row is present; the row's exit status and the unit's `ExecMainStatus` are both 0; the unit's `Result` is `success`; `HarnessPollTimeout=no` is explicit (on Windows, `timed_out` is explicitly false); and no OOM was seen. Anything else is I-6, and a missing `.unit` file counts. Only completed repeats enter the statistics and the memory, field, count and digest checks.
  - **Panels and digests.** A completed repeat without panel, `expanded` or assertion evidence is I-5. One without both artifact digests is I-4.
  - **Record shape.** These are `H-SHAPE`: a row whose stage, arm, repeat, cold, instrumented or dry-run flag does not match the repeat it is filed as; a repeat outside the fixed shape; a job whose arm order breaks the r2 §6.2 alternation (combining refuses it too); a Windows bundle whose arm order is not the r2 §12.2 `forced,prescribed`, that has duplicate entries, or whose per-repeat timeout is not 1800 s; a Linux unit file whose recorded `HarnessPollBoundS` is not 1800.
  - **Code identity, on both platforms.** A Windows execution identity without `observe_runtime` is I-7. So is a Linux job whose summarize-time `observe_runtime` failed, and combining marks such a job I-7 too. The identity is attached and checked inside the job record, before its verdict.
  - **Run attempt.** A Stage 1b job record whose run attempt is absent or outside 1–2 is I-7; combining refuses one.
  - **CPU input on both arms.** The warm spread (PA-4) needs the CPU input of every completed timed repeat of both arms. A missing input, prescribed included, makes the record `INCOMPLETE`; a spread is never taken over a subset.
- **Spread basis.** The warm spread uses the ceiling CPU input, the larger of `C_w` and `CPUUsageNSec − setup_excluded` (r2 §6.1). It is applied per arm, and a job fails if either arm exceeds the limit. The in-process spread is also recorded. Following r2 §6.2, the record also reports the cold-inclusive spread (`spread_all`, and its in-process twin). CPU, wall and memory each get a max, median, min and spread over all timed repeats and over the warm ones, with a count of absent values.
- **Where code identity is taken.** Git, the harness hash, the source hashes and `observe_runtime` are taken at summarize time, outside the measured unit, so they add nothing to the unit's CPU or memory. `start_head` is recorded by the workflow before the loop. On Windows, `--launcher` also takes them after its last repeat, and `--summarize` requires the two to match (I-7).
- **Missing ceiling inputs.** Ruled on 2026-09-27 as r2 §12.9 (3): see "Incomplete Stage 1b evidence" above. When an `INCOMPLETE` and an I-3 apply together, both reasons are recorded and the stop class is `INCOMPLETE_EVIDENCE`. r2 §12.9 does not say which stop class wins when both apply; its (3) states the Stage 1b verdict explicitly, and the I-3 reason and `memory_feasibility = UNVERIFIED` are kept.
- **Dry run.** Its one untimed repeat per arm is also instrumented, so call counts are checked early. The dry run never applies the rule.
- **Schema additions.** The v2 fields are kept, with these additions:
  - repeat `arm`, `cpu_input_s`, `result`, `timed_out` and `error`;
  - `workload` keyed by arm;
  - `scope = job | combined`;
  - `verdict.sigma_screen` and `verdict.pa3a_screen`;
  - the stop class `MEMORY_EVIDENCE_MISSING` (§16 C8);
  - under r2 §12.9 (5): the stop classes `INCOMPLETE_EVIDENCE` and `LEGACY_UNACCEPTED`, `verdict.rerun_eligible`, the `INCOMPLETE` and `LEGACY` reason codes, and each arm's all-repeat and warm distributions (max, median, minimum, spread, absent count) for CPU input, workload wall and complete memory.
- **Call-count mismatch** against the r2 §4 expectation (forced 14 replays, 5 proofs, 15 `verify_for`; prescribed 8, 3, 9), or a completed instrumented repeat without counts, is `H-COUNTS`. That is a harness defect, not a note: the measured workload is not the specified one, so neither Stage 1a validation nor a Stage 1b ceiling can rest on it. The remaining notes are informational by r2: the probe-failed-first note (with I-1), the D3 R7 note (with I-4) and the Stage 1a warm spread (I-2 is a Stage 1b check, §12.7).
- **Workflow.** The workflow adds a per-repeat poll bound (30 min) so that a hang is an I-6 timeout, `persist-credentials: false`, and the run attempt in the artifact name. It also has a `runtime` input, whose `worker_image` value is refused (image-first finding).
- **Loop deadline.** r2 fixes `timeout-minutes: 120` (§12.3), which the workflow sets once, as the single-valued matrix key `timeout_min` that both `timeout-minutes` and `JOB_TIMEOUT_MIN` read, and budgets a measure job at 31 min (§12.6). r2's §12.3 loop sketch defaults the per-repeat poll bound to 1800 s (`REPEAT_POLL_BOUND_S`), the same 30 min this workflow sets; r2 sets no loop bound. *[Corrected 2026-09-27 after #523 merged: this previously said r2 sets no per-repeat bound either.]* The workflow stops starting repeats, and stops waiting on a hung one, at the job start plus 120 − 15 = 105 min. A repeat not started by then gets a `HarnessNotStarted=loop-deadline` unit file and is summarized as I-6. The 15 min `POST_LOOP_RESERVE_MIN` for summarize, owned cleanup, journal export and upload is a harness choice: r2 §12.6 budgets only 2 min for cleanup and upload, and does not budget summarize. It does not change any r2 budget, because a normal job ends well inside it.
- **Preconditions and fixed oracles.** Every precondition r2 sets for a repeat or a stage is checked and fails visibly. Every oracle is a fixed r2 value or a pinned hash, never derived from the input being checked:
  - **Cold repeat (r2 §6.2).**
    - On Windows, `--launcher` records per repeat the directories it purged and any `__pycache__` still present afterwards (`purge_failed_dirs`), or the purge error.
    - In the workflow, a purge or page-cache drop that fails, or leaves bytecode behind, stops the loop. A successful one is recorded as `HarnessColdPrep=done` in repeat 1's unit file.
    - A measure-mode repeat 1 without that evidence is **I-6**: the repeat's precondition was not established, which is a failed repeat and re-runnable.
    - I read I-6 over H-SHAPE here because the record's shape is correct and a host lock can cause the failure.
  - **Probe completion (r2 §8.4).** The probe unit must show `ExecMainStatus=0` and `Result=success`; otherwise it is I-1.
  - **Call counts (r2 §4).** Compared with the literal table (forced 14/5/15, prescribed 8/3/9), never with the counts the request implies. The row's `workload.expected` is recorded for reference only.
  - **Workload dimensions (r2 §4, §6.2, §6.3).** Each completed repeat's workload must equal the fixed values, else H-SHAPE:
    - initial 2 and expanded 4 panels;
    - 2 paths per panel;
    - horizon 5, inner block 5 and outer months 6;
    - `within_pp` 1.0 forced and 0.01 prescribed;
    - budget 3600 s, full pass rate 1.0, not idle, the composition fixture.
  - **Fixture identity.** r2 names no literal for sessions, bars per session or legs, which come from the fixture's own source. So `composition_fixture.py` and `runtime_fixture.py` are pinned by SHA-256; they are the same at r2's base `875ecf29` and at this revision. A different fixture is H-SHAPE: a workload change and a re-measurement trigger (r2 §9).
  - **Unit and threads (r2 §5.1, §12.3).** A Stage 1b repeat must have run in its own `fp-s5pa-<stage>-<arm>-<r>` unit, and every repeat's thread environment must be pinned to 1. Otherwise it is H-SHAPE.
  - Already in place: swap off (the probe and each repeat's memory), the in-unit cgroup path, and the per-repeat and launcher timeout bounds.
- **Retained failures, never a traceback.** Every unreadable artifact or failing call ends in a retained record or a clear refusal:
  - An unreadable, truncated or non-object `probe.json` is I-1.
  - An unreadable or malformed Windows bundle is summarized as I-6 for every repeat, and the bundle is left as it is.
  - An absent or unreadable `git-head.txt` is I-7. An unreadable `.unit` file counts as absent: I-6.
  - `--launcher` keeps every repeat: a failure to create, assign or run a job, or an unreadable row, becomes a failed entry (I-6). The bundle is always written, including after an interrupt, when it records `interrupted` and the missing repeats are I-6.
  - In the workflow, a unit that `systemd-run` cannot start gets a `HarnessLaunchFailed` unit file. A failed `systemctl show` leaves `HarnessShowFailed` with no `Result`. Both are I-6, and the loop goes on to the next repeat.
  - Inputs that carry no evidence are refused with a message, never a traceback, and nothing is written: a missing input path, a readable file that is not a launcher bundle, and, when combining, an unreadable or malformed job record. The job's retained rows and units can be re-summarized.
- **Summarize step exit.** The runner's default shell is `bash -eo pipefail`, so the summarize step turns `-e` off. An exit 3 or 4 from the summarizer, whose record is already written, then still reaches the step summary before the step returns that status. Cleanup and upload are `if: always()` and run after it (r2 §12.9 (3)).
- **Coordinator readings (r2 §12.9 (6)).** A run attempt outside 1–2 is I-7. A Windows bundle's arm order must be `forced,prescribed`.
- **Cleanup receipt.** r2 names no class for a failed owned cleanup. The job fails at that step, so it counts as a failed job under the §12.7 re-run cap, and combining refuses its record. That refusal is a harness choice. *[Corrected 2026-09-28: r2 §12.7 ("Failures outside the summarizer stop the stage") governs the re-run count. A failed owned cleanup is not an exit 3; it stops the stage for diagnosis, and any new dispatch needs a fresh approval. The combine refusal is unchanged.]*

## Measurement execution (2026-09-28)

The r2 §12 bounded measurement ran under the [execution dispatch](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-transfer-and-execution-dispatch--h1-step-b-measurement-2026-09-28). The results, the rule application and the CP-1b build-entry table are in the [CP-1b packet entry](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-cp-1b-packet--build-entry-status-2026-09-28). Every run measured `7675c088`.

| Stage | Run | Outcome | Files here |
|---|---|---|---|
| 0 | local read of the preserved S4 set | Coverage holds; calibration only | `stage0/` |
| 1a | Windows, detached LF checkout | Valid (exit 0); memory UNVERIFIED by design | `windows-20260928T010154Z.json`, `.record.json` |
| 1b dry run | 36364714432, attempt 1, job a | Valid (exit 0) | `stage1b/36364714432-a-attempt1/` |
| 1b measure | 36364854404, attempt 1, jobs a and b | Both valid; memory VERIFIED; no re-run used | `stage1b/36364854404-{a,b}-attempt1/`, `stage1b/36364854404-combined.json` |

- **Line endings.** Stage 1a and the combine ran from a checkout made with `git -c core.autocrlf=false worktree add --detach`. The harness pins the LF SHA-256 of both fixtures and hashes working-tree bytes, so a CRLF checkout can only exit 4 on Stage 1a and is refused at combine. `.gitattributes` here keeps the committed evidence byte-exact on every checkout.
- **Committed Linux files.** Each job directory holds the r2 §12.3 file list: `record.json`, `probe-in-unit.json`, `probe.unit`, `host-facts.txt`, the per-repeat `.json` and `.unit` files, and `cleanup-receipt.json`. The complete artifacts are private: `journal.log`, `summarize.log`, `probe.json` and `git-head.txt`. So are the Stage 1a launcher logs, including the first invocation that argparse refused before any repeat ran, and the raw Stage 0 extracts. All of them are in `h1b-stage1b-measurement-evidence-2026-09-28.tar.gz`, which is pinned in `docs/evidence/PRIVATE_EVIDENCE.sha256` and pushed to first-passage-archive#844. It counts as ARCHIVED once that PR merges.
- **Stage 0 public-clone review.** The extraction used r2 §16.4's block as it stood at `7675c088`, over both `journal.log` and `systemd-units.log`. So systemd CPU lines appear twice and carry no run labels; #536's corrected block post-dates the read. Every one of the 836 lines in `stage0/lines.txt` has the form `<UTC timestamp> <runner VM name> systemd[1]: <unit>: Consumed <CPU> CPU time[, <memory> memory peak, <swap> memory swap peak].` The unit names use only `[A-Za-z0-9._-]`. There is no host path, account or token, and the fixed journal prefix is kept verbatim. Two `Binary file … journal.sqlite matches` rows were dropped from `stage0/memory_peak.txt`; they were grep noise naming a local path. The preserved set's `SHA256SUMS` is cited by its SHA-256, `e2c142281d819e071d15f99a242358f93389a479dcc5e6b5c1f6a20d5db189a7`, not committed. A tracked `*SHA256SUMS` would register its 222 files as pinned private evidence (`scripts/evidence_archive.py`). Two of those files, the `boundary/journal.sqlite` files at about 110 MB each, exceed GitHub's per-file limit and cannot be archived.
- **Stage 1a bundle.** The bundle is committed unmodified, because r2 §12.9 (2) forbids altering a bundle. Its per-repeat `environment` records the local checkout and venv paths.
## Not run

*[History: this section describes the harness as returned on #526, before the 2026-09-28 execution above.]*

No measurement, engine workload, `_run_part_a` or `build_verified_composition` execution, Stage 0 read, Stage 1a, workflow dispatch, re-run, cancel or artifact download was made. The harness was invoked only in these ways:
- `py_compile`, `--help` and `--check-stage`;
- `--summarize`, combine and `--probe-verdict` on synthetic inputs, through the regression module.

The workflow's own step scripts ran only against stubbed system commands in that module. The accounting-probe script was compiled, not run.
