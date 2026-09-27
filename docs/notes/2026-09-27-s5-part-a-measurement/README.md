# S5 Part A measurement harness and dispatch-only workflow (H1 step (b))

**Status:** PREPARED, NOT RUN. This directory holds the harness for the bounded S5 Part A measurement. Nothing in it has been measured. No engine workload, Stage 1a, Stage 0 or Stage 1b dispatch, re-run or artifact download has run. Output class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`. S5 stays **HELD**.

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
| `../../../.github/workflows/qualification-s5-part-a-measurement.yml` | The dispatch-only Stage 1b workflow (r2 §12.3) |
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
- **Workflow helpers** use the standard library only:
  - `--probe-verdict DIR` judges the accounting probe (r2 §8.4);
  - `--check-stage STAGE` refuses `1c` until its C3 path lands (r2 §12.4, I-8).

It never drives the E1 route, the retired executor class or any service.

## Commands

**Stage 1a** (Windows host, grants `tests.run` and `worktree.write`; r2 §12.2):

```powershell
.\fp.ps1 doctor
.\fp.ps1 python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --launcher --stage 1a --arms forced,prescribed --repeats 5 --out docs/notes/2026-09-27-s5-part-a-measurement/windows.json
.\fp.ps1 python docs/notes/2026-09-27-s5-part-a-measurement/measure_part_a_max.py.txt --summarize docs/notes/2026-09-27-s5-part-a-measurement/windows.json --stage 1a
```

Stage 1a validates the harness only. It checks panel counts, digest identity, prefix identity, all fields populated and call counts. Memory is always `UNVERIFIED` and the rule is never applied. A harness defect is fixed and re-run locally; it is not a validity-check count.

**Stage 1b** (the coordinator, after this file is on `main`; within the r2 §12.7 caps):

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

**Caps (r2 §12.7):**
- at most one re-dispatch of a failed dry run (I-1 or I-6);
- at most one `gh run rerun <id> --failed` of the measure dispatch (up to both jobs). Combining enforces this: it refuses a job record whose run attempt is outside 1–2, and it accepts the attempt-1/attempt-2 mixture a `--failed` re-run produces. The dry-run re-dispatch cap spans separate runs, so no single record can show it; the coordinator keeps that count;
- any failure after that stops the stage.

The artifact name carries the run attempt, so a re-run never replaces the failed attempt's evidence.

## Validity and stop classes (r2 §12.7 with §16 C8 and ruling (4))

| Code | Condition | Exit | Stop class |
|---|---|---|---|
| I-1 | Accounting probe failed (memory.peak below 64 MiB or absent, swap on, `CPUUsageNSec` empty) | 3 | `MEMORY_EVIDENCE_MISSING` (§16 C8 relabel) |
| I-2 | Warm CPU spread > 1.30 in an arm (Stage 1b; informational at 1a) | 3 | `INVALID_MEASUREMENT` |
| I-3 | A timed (or dry-run) repeat has no complete aggregate memory reading | 3 | `MEMORY_EVIDENCE_MISSING`; memory `UNVERIFIED`, `rule_applicable = false` |
| I-4 | Digests differ within an arm, or the forced prefix differs from the prescribed result | 4 | `INVALID_MEASUREMENT`; bears on D3 R7 only after diagnosis (§16 C8) |
| I-5 | Panel-count or `expanded` assertion failed | 4 | `INVALID_MEASUREMENT` |
| I-6 | A repeat exited non-zero, timed out (30 min poll bound, capped by the loop deadline), OOMed, left no row, or was not started before the loop deadline | 3 | `INVALID_MEASUREMENT` |
| I-7 | Measured head differs from the dispatched head, or the tree is dirty (Stage 1b). A missing dispatched head, start head (`git-head.txt`) or summarize-time head also counts | 4 | `INVALID_MEASUREMENT` |
| I-8 | Stage 1c requested before its C3 path exists | 4 (workflow: refused at input validation) | `BLOCKED` |
| H-FIELDS | A completed repeat left a required field empty. At Stage 1b the ceiling-input fields are judged by INCOMPLETE instead | 4 | `INVALID_MEASUREMENT` (harness defect) |
| H-SHAPE | The record is not both arms with 5 timed repeats per arm (measure mode; r2 §6.2, §12.2) | 4 | `INVALID_MEASUREMENT` (not an acceptance shape) |
| H-COUNTS | A completed instrumented repeat's call counts differ from the r2 §4 workload, or are absent | 4 | `INVALID_MEASUREMENT` (harness defect: not the specified workload) |
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
- **Loop deadline.** r2 fixes `timeout-minutes: 120` (§12.3), which the workflow sets once, as the single-valued matrix key `timeout_min` that both `timeout-minutes` and `JOB_TIMEOUT_MIN` read, and budgets a measure job at 31 min (§12.6). It sets no per-repeat or loop bound. The workflow stops starting repeats, and stops waiting on a hung one, at the job start plus 120 − 15 = 105 min. A repeat not started by then gets a `HarnessNotStarted=loop-deadline` unit file and is summarized as I-6. The 15 min `POST_LOOP_RESERVE_MIN` for summarize, owned cleanup, journal export and upload is a harness choice: r2 §12.6 budgets only 2 min for cleanup and upload, and does not budget summarize. It does not change any r2 budget, because a normal job ends well inside it.
- **Summarize step exit.** The runner's default shell is `bash -eo pipefail`, so the summarize step turns `-e` off. An exit 3 or 4 from the summarizer, whose record is already written, then still reaches the step summary before the step returns that status. Cleanup and upload are `if: always()` and run after it (r2 §12.9 (3)).
- **Coordinator readings (r2 §12.9 (6)).** A run attempt outside 1–2 is I-7. A Windows bundle's arm order must be `forced,prescribed`.
- **Cleanup receipt.** r2 names no class for a failed owned cleanup. The job fails at that step, so it counts as a failed job under the §12.7 re-run cap, and combining refuses its record. That refusal is a harness choice.

## Not run

No measurement, engine workload, `_run_part_a` or `build_verified_composition` execution, Stage 0 read, Stage 1a, workflow dispatch, re-run, cancel or artifact download was made. The harness was invoked only in these ways:
- `py_compile`, `--help` and `--check-stage`;
- `--summarize`, combine and `--probe-verdict` on synthetic inputs, through the regression module.

The workflow's own step scripts ran only against stubbed system commands in that module. The accounting-probe script was compiled, not run.
