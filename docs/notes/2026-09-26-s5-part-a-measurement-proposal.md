# S5 Part A measurement-and-margin proposal, and RC-1..RC-6 status

**Status:** PROPOSAL, returned for operator approval. Nothing here is approved. Every number marked PROPOSED is a proposed rule parameter, not a ceiling. S5 stays **HELD** ([ledger, 2026-09-26](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26)).
**Card:** [S5 Part A measurement proposal](../briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md), dispatched at `62c956f`. **Authority:** operator ruling 2026-09-26 §6 (resource-envelope decision), quoted in the card.
**Sources read at `62c956f`.** Under `ops/`, `tests/`, `tools/`, `deploy/`, `scripts/` and `.github/`, that head does not differ from `main@8e9e084` (`git diff --stat origin/main HEAD` over those paths is empty). The sources were the S5 decision draft, the execution-slices plan, the full-E1 spec §2.4–§2.6, the S5 packet draft, the [2026-09-24 measurement](2026-09-24-t10-step4-representative-measurement.md) and its raw data, and the code named in each section. **No measurement, Linux dispatch, qualification service, artifact download or S5 work was run.** Every figure below is either cited from an existing record or labelled as arithmetic from cited figures.

## 0. Summary

**What is returned for approval:** a measurement standard and a margin rule (§3, §4). The coordinator applies it to TEST_ONLY diagnostic ceilings only after approval (§6).

**Findings that shape the rule:**

1. **The TEST_ONLY workload S5 will run can never expand.** The contract pins the expansion test to `|p5 − 0.95| ≤ 0.01` for every domain (`contract.py:761-773`). The TEST_ONLY workload has 2 initial panels with 2 paths each (`composition_fixture.py:195`, `:236`, `:241`). A panel's pass rate is therefore 0, 0.5 or 1, and the initial p5 is never within 0.01 of 0.95. (The p5 is the nearest rank, `ceil(0.05 × 2) = 1`, so the minimum of the two panels.) The smallest per-panel depth that can expand is 17 (16/17 ≈ 0.941). So no genuine S5 campaign on this fixture takes the expansion branch, whatever the synthetic source. The existing record agrees: all six composition runs that reached Part A ran 3 panel proofs and 4 Part A paths, with no expansion (`2026-09-24-t10-step4/composition-sweep.json`, depths 2 and 10). **Maximum expansion (4 panels) therefore has to be measured with a forced-expansion harness (§3.3), not through the signed route.**
2. **No existing measurement covers maximum expansion.** `benchmark_part_a.py` measures one panel and one path and bypasses `ProductionSource`, so it omits the dominant cost (`benchmark_part_a.py:1`, `:45-77`). The 2026-09-24 composition harness runs the signed route, which never expands (finding 1).
3. **Per-call source re-verification dominates.** Every replay, including each panel proof, calls `verify_for` (`production_source.py:867`, `:891-894`). It cost about 1.04–1.05 s CPU per call on the fixture (Windows, CPython 3.13.2: 33.64 s / 32 calls and 58.38 s / 56 calls in `composition-sweep.json`). The N2 figure behind the 2026-09-24 ruling fits the same shape: 211.39 s CPU on Windows for 180 paths, about 1.17 s per path.
4. **The Part A engine already predicts maximum expansion, and refuses if the prediction exceeds its budget.** Its pilot predicts `probe + max_panels × (rebuild + depth × path)` and raises before any panel if that exceeds `budget_seconds` (`part_a.py:178-186`), even when expansion will not be needed. In the service route the pilot runs under the kernel CPU-rate quota (`campaign_supervisor.py:177-194`), so the PART_A ceiling must cover the throttled prediction of maximum expansion (§4, PA-2b).
5. **The recorded host factor has no recorded basis.** The C2 ruling states "roughly 137 s on Linux by scaling" (plan line 756) without evidence. The measurement record it cites (`20260924T034139Z-59ce3c4b7643`) was not found in any local checkout. The rule applies **no** host factor: it measures on the reference runtime directly.

**Build pitfalls for S5, returned to the coordinator (not changed here):**
- **`/v7` loses the N2 ceiling.** `diagnostic_budget_profile` widens N2 only when the profile schema is `v6` (`profile.py:239`), and the M13 ruling is "/v6 only" (plan line 757). A `/v7` profile would give N2 the shared 120 s CPU, below N2's measured 211 s. That is the silent-SIGKILL failure checkpoint C2 found. `/v7` needs either the M13 ruling extended or this rule applied to N2 (decision 3, §8).
- **`/v7` loses the fixture cap.** `fixture_producer.py:152-156` raises the TEST_ONLY cap to 10,000 s only for release `v3`–`v6`. A `v7` release would bind the default 120 s CPU / 180 s wall, and Σ-feasibility would fail at binding (§5).

**RC status:** RC-1 partly met; RC-2 to RC-6 unmet. **No S5 release proposal is supported** (§7).

## 1. Maximum-expansion workload

**Definition.** One PART_A compute work (phase `PART_A`, `campaign_budget.py:12-13`) that runs `_run_part_a` from pilot through appended panels `[initial_panels, expanded_panels)`. This is what the S5 adapter will do (`compute.run_part_a_compute`, S5 packet §1; the slice plan's "one Part A operation"). The work includes:
- worker start;
- source admission;
- one `verify_for` at compute start, the same shape as `compute.py:28`;
- the pilot: one outer panel, one proof replay of that whole panel, and one horizon path (`part_a.py:178-180`);
- for each panel index `0..expanded_panels−1`: outer sampling, one proof replay of the panel (`regime.py:83`), and `paths_per_population_per_panel` horizon paths, each evaluated (`part_a.py:195-204`);
- the N2 FULL baseline derivation from staged N2 capture bytes (S5-D1/D2);
- serialization and fsync of the initial-prefix and final artifacts.

The seeds depend only on panel and path index (`part_a.py:139-142`). A forced expansion therefore performs exactly the computation that a prescribed expansion would on the same contract, source and root, which makes the forced arm below a faithful workload.

**Owners of the numbers:**
- the frozen contract's `replay.part_a` and `replay` fields (`production.py:89-96` shows the mapping into the engine request);
- the workload policy (`trust_domain.py:382-385` pins production to 100/200 panels, 6 months and 5 sessions);
- the budget profile: "PART_A includes maximum expansion" (`profile.py:167`).

| Quantity | TEST_ONLY S5 workload (Linux fixture) | Production (reserved maximum) |
|---|---|---|
| initial → expanded panels | 2 → 4 (`composition_fixture.py:241`) | 100 → 200 (`trust_domain.py:382`) |
| paths per panel | 2 | per F1 (test document: 200, `test_contract.py:131`) |
| horizon / inner block / outer months | 5 / 5 / 6 (`composition_fixture.py:195`) | per F1 / 5 / 6 |
| source | composition fixture, trading variant: 174 sessions, 4 bars per session per leg, 4 legs (2026-09-24 note §1) | admitted cold-replay source (~95k M15 bars per leg, 2026-09-24 note §2) |
| replays at maximum expansion | 2 pilot + 4 × (1 proof + 2 paths) = **14** (5 panel proofs, 9 horizon paths) | 2 + 200 × 201 = 40,202 |
| `verify_for` calls | 15 | 40,203 |
| replays with no expansion | 8 | 20,102 |
| can the prescribed rule expand? | **No** (§0 finding 1) | Yes |
| budget binding paths | `part_a_initial_paths=4`, `part_a_expanded_paths=8` (`composition_fixture.py:242`) | per F1 |

**Arithmetic estimate, not a measurement and not a ceiling input.** At the cited ~1.05 s CPU per `verify_for` (Windows), 15 calls give about 16 s. Five panel proofs of about six months of fixture sessions, nine 5-session paths, and worker start with source admission add a few seconds. The expected TEST_ONLY maximum-expansion payload is therefore roughly 20–30 s CPU on the Windows development host. The Linux value is unknown (§0 finding 5).

## 2. Reference runtime

**TEST_ONLY reference runtime = the host class that runs S5's acceptance-grade Linux campaigns.** The ceiling only has to hold there. Recorded identity per run:

| Field | Value or source |
|---|---|
| Host class | GitHub-hosted `ubuntu-24.04` runner, as in `qualification-s2-supervision.yml:68`. The workflow does not pin hardware; each run records the `/proc/cpuinfo` model name and `nproc`. GitHub documents 4 vCPU / 16 GB for standard public-repository Linux runners; that is not verified here |
| OS | Ubuntu 24.04 x86_64, ext4 (`tools/qualification_verification/host.json`); kernel recorded from `uname -r` |
| Interpreter | CPython 3.12.3 (`host.json` `python_version`). The worker image base is `python:3.12.3-slim-bookworm`, resolved to a digest at build (`image.py:53-64`). Image digests therefore differ per install (S4 acceptance read: `775e780e…`, `65b0c63c…`), and each run records its digest |
| Dependencies | `requirements-ops.lock` SHA-256 `9aa7c17c…` (`host.json`); thread environment pinned to 1 (`profile.py`, `CAMPAIGN_RESOURCE_SCOPE.controller_environment`) |
| Code identity | measured commit, clean tree; worker runtime closure digest (`execution/runtime.observe_runtime(repo, 'worker')`); harness SHA-256; fixture file SHA-256s |
| Release identity | none exists before S5 (`/v7` is S5's). Stage 2 (§3.4) records the `/v7` release, profile and policy digests |

**Mapping to the production service host: none.**
- No production qualification host exists yet. Provisioning it is obligation OF-1 (draft §1.3).
- No host factor is evidenced: the "~137 s on Linux by scaling" figure has no recorded basis (§0 finding 5). The rule therefore uses **no host factor**. Windows figures serve only to develop the harness and check orders of magnitude.
- A production ceiling needs its own measurement on the production host class, under the production budget owner. The ruling says production budgets remain separately governed.

**Evidence that could calibrate a Windows/Linux factor already exists.** The S4 Linux runs (36180568493, 36181780676) retained `journal.log` and `systemd-units.log` for 14 days (`qualification-s2-supervision.yml:143-178`). Those logs may hold the consumed CPU of the N1/N2 payload units, which could be paired with the Windows figures of 13.36 s and 211.39 s. It is unverified that the lines are present. Reading them is Stage 0 (§3.4), a download that needs approval. **The retention expires about 2026-10-09.**

## 3. Capture method

### 3.1 What is measured

| Measure | Primary (inside the payload process) | Secondary (system manager, Linux) |
|---|---|---|
| CPU | `resource.getrusage` user+sys for `RUSAGE_SELF` plus `RUSAGE_CHILDREN`, from a fresh process per repeat | the transient unit's `CPUUsageNSec`, the cgroup `cpu.stat` total including every descendant |
| Wall | outer: process launch to exit (`ExecMainStartTimestampMonotonic` → `ExecMainExitTimestampMonotonic`); inner: `perf_counter` around the Part A call | — |
| Memory | `ru_maxrss` (as the engine's own `production._peak_memory_bytes` reads it) | the unit's `MemoryPeak` (cgroup `memory.peak`), swap off |
| Engine facts | `PartAResult.probe_seconds`, `predicted_seconds`, `elapsed_seconds`, panel count, `expanded` | — |
| Integrity | SHA-256 of the canonical initial-prefix and final serializations | — |
| Call counts | replay, proof and `verify_for` counts, from **one extra instrumented repeat per arm** that is excluded from timing statistics (counting wrappers perturb timing) | — |

The ceiling uses the **larger** of the primary and secondary CPU values. For memory it uses the cgroup `MemoryPeak` when present, else `ru_maxrss`, flagged as a lower bound.

### 3.2 Repeats, statistic and noise

- **Arms:** two, of which only `forced` sets the ceiling.
  - `prescribed` keeps the frozen tolerance of 0.01, so for (2, 4, 2) it never expands. It is the consistency anchor for Stage 2.
  - `forced` overrides the tolerance to 1.0 in the measurement request, so expansion always runs to `expanded_panels`.
- **Repeats:** 5 sequential fresh-process repeats per arm per runner, on **2 independent runner jobs**: 10 per arm. The first, coldest repeat is kept, because a real worker always starts cold.
- **Statistic for the ceiling:** the maximum over all valid repeats (Ĉ for CPU, Ŵ for wall, M̂ for memory). The median, minimum and spread (max ÷ min) are reported too.
- **Determinism:** the workload is deterministic. The root is fixed and unsalted (`tb-s2-rng-v2`, `regime.py:22`); the fixture keys change per run, but the seeds do not.
  - Every repeat of an arm must produce identical artifact digests.
  - The forced arm's first `initial_panels` panels must be byte-identical to the prescribed arm's result.
  - **Any mismatch invalidates the measurement and is returned to the coordinator.** It would also be evidence against D3's R7 reproducibility assumption.
- **Noise:**
  - A job whose CPU spread exceeds **1.30 (PROPOSED)** is invalid and is re-run once on a fresh runner. If it fails again, the measurement returns to the coordinator without a ceiling.
  - A between-job ratio of medians above 1.30 is recorded as host variance. Ĉ remains the maximum, and the application entry flags it.

### 3.3 Harness (to be written; specified here)

The harness is `measure_part_a_max.py`, kept as `.py.txt` beside its record under the 2026-09-24 convention, so the import-boundary gate does not treat it as a module. It reuses the 2026-09-24 harness's fixture setup and `benchmark_part_a.py`'s output conventions. Each repeat runs in a fresh `sys.executable` subprocess:

1. `setup = build_verified_composition(tmp, confirmation_depth=60, decision_alpha='0.05')`, the trading variant (`idle=False`). Depth 60 is the Linux fixture default (`composition_fixture.py:180`); Part A does not depend on it.
2. `setup.source.verify_for(setup.contract)` once, the same shape as `compute.py:28`.
3. Build the request exactly as `production._part_a_request` does (`production.py:89-96`), with two exceptions: `within_pp` takes the arm's tolerance, and `budget_seconds = 3600`, so the in-engine predicate never aborts the measurement. `predicted_seconds` is still recorded.
4. `_run_part_a(request, source.sessions, adjacent=source.adjacent, covered_until=source.covered_until, tail_covered=source.tail_covered, proof_provider=source.proof, replay_provider=source.replay, initial_state=compute.initial_state(contract), full_pass_rate=1.0, synthetic=True)`. `full_pass_rate` affects only the final sanity decision, not the compute. The N2 baseline derivation is excluded here and measured at Stage 2.
5. Serialize the initial prefix and the final panels canonically (sorted-key compact JSON of `asdict`). This stands in for the S5-D1 artifact format, which does not exist yet; Stage 2 replaces it.
6. Assert the panel count (forced: 4; prescribed: 2) and write one JSON row.

It never calls `_run_composition_e1`, `run_production_e1`, `_execute_e1` or `ProductionExecutor`. Its output class is `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.

### 3.4 Exact commands (proposed steps; none is run by this proposal)

**Stage 0 (approval needed: an artifact download). Existing Linux evidence, no new run.**
```bash
gh run download 36180568493 -n qualification-s2-supervision -D <scratch>/s4-36180568493
gh run download 36181780676 -n qualification-s2-supervision -D <scratch>/s4-36181780676
grep -hE "Consumed .* CPU time|memory peak" <scratch>/s4-*/journal.log <scratch>/s4-*/systemd-units.log
```
Output: the Linux N1 and N2 payload and guardian CPU, if logged, paired with the Windows 13.36 s and 211.39 s. This calibrates §0 finding 5. It also supplies the `/v7` N2 value if decision 3 applies the rule to N2.

**Stage 1a. Windows development pass (harness validation only; not the ceiling basis).**
```powershell
.\fp.ps1 doctor
.\fp.ps1 python docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py --arm prescribed --arm forced --repeats 5 --out docs/notes/<date>-s5-part-a-measurement/windows.json
```

**Stage 1b (approval needed: a Linux host dispatch). The reference measurement.**
It runs as a `workflow_dispatch`-only job on `ubuntu-24.04`:
- The host environment is provisioned exactly as the S2 workflow's setup steps provision `$host_root/env`.
- It uses no qualification service and no secrets, and uploads only the JSON.
- It needs a new workflow file, a CI configuration change with its own authorization.
- It runs as 2 jobs (matrix `job: [a, b]`).

Per job:
```bash
for arm in prescribed forced; do
  for r in 0 1 2 3 4 5; do   # r=0 is the instrumented call-count repeat, excluded from statistics
    unit="fp-parta-$arm-$r"
    sudo systemd-run --unit="$unit" --uid="$(id -u)" --gid="$(id -g)" --working-directory="$PWD" \
      -p CPUAccounting=yes -p MemoryAccounting=yes -p MemorySwapMax=0 -p RemainAfterExit=yes \
      -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 -E NUMEXPR_NUM_THREADS=1 \
      "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python \
        "$NOTE_DIR/measure_part_a_max.py" --arm "$arm" --repeat "$r" --in-process --out "$OUT/$arm-$r.json"
    until [ "$(systemctl show -p SubState --value "$unit")" = exited ] || \
          [ "$(systemctl show -p ActiveState --value "$unit")" = failed ]; do sleep 1; done
    systemctl show -p CPUUsageNSec -p MemoryPeak -p ExecMainStatus \
      -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic "$unit" > "$OUT/$arm-$r.unit"
    sudo systemctl stop "$unit"; sudo systemctl reset-failed "$unit" 2>/dev/null || true
  done
done
grep -m1 "model name" /proc/cpuinfo > "$OUT/cpu.txt"; nproc >> "$OUT/cpu.txt"; uname -r >> "$OUT/cpu.txt"
```
Dry-run first, with one repeat per arm, to confirm that `CPUUsageNSec` and `MemoryPeak` are populated for an exited `RemainAfterExit` unit on systemd 255. If they are not, fall back to the unit's `Consumed … CPU time` journal line and the primary `getrusage` values. The launcher's own overhead falls inside the unit, so it is charged conservatively.

**Stage 2 (at S5 packet Checkpoint C3; no new authority). Service-route confirmation.**
- The genuine S5 Linux campaign's PART_A work supplies its settled observation from the retained budget snapshot: `cpu_ns`, `memory_peak_bytes`, `oom_events`, and the boottime difference from the reservation clock to `CAPTURED`.
- Proposed C3 requirement on the S5 executor: export those fields in the run evidence, read with `scripts/s2_run_evidence.py <run> --expect-head <sha>`.
- The genuine campaign never expands (§0 finding 1), so Stage 2 checks the service route against Stage 1's **prescribed** arm (PA-5).

### 3.5 Evidence record

The record lives in `docs/notes/<date>-s5-part-a-measurement/`: the harness `.py.txt`, `windows.json`, the Linux job JSON and `.unit` files, `cpu.txt`, and a short note. The JSON schema is `s5-part-a-max-expansion-measurement/v1`:

```text
schema, artifact_class = TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING, decision_bearing = false,
recorded_utc, measured_commit, tree_clean, harness_sha256, source_sha256{path: sha},
runtime{os_id, os_release, kernel, arch, cpu_model, logical_cpus, implementation, python,
        executable_sha256, requirements_lock_sha256, thread_env, image_digest|null, runner, run_id, job},
workload{fixture, idle=false, sessions, bars_per_session_per_leg, legs, outer_months, inner_block_sessions,
         horizon_sessions, initial_panels, expanded_panels, paths_per_panel, root_rng_namespace, recipe,
         arm, within_pp, full_pass_rate_input=1.0, expected{replays, verify_for}},
repeats[{repeat, instrumented, cpu_self_s, cpu_children_s, cpu_total_s, unit_cpu_s|null, wall_outer_s,
         wall_inner_s, peak_rss_bytes, unit_memory_peak_bytes|null, panels, expanded, probe_seconds,
         predicted_seconds, elapsed_seconds, counts{replay, proof, verify_for}|null,
         initial_prefix_sha256, final_sha256, exit_code}],
summary{per arm: cpu/wall/memory max, median, min, spread; digests_identical; prefix_matches_prescribed},
validity{ok, reasons[]}
```

## 4. Proposed margin rule (every parameter PROPOSED, not approved)

**Symbols:**
- Ĉ, Ŵ and M̂ are the forced-arm maxima (§3.2).
- P̂ is the forced-arm maximum of `predicted_seconds`.
- O is the phase's installed orchestration charge (20 s diagnostic, `profile.py:212`).
- L is a launch allowance for the time from reservation to payload start.
- Ceilings round **up** to whole 10 s.

| Rule | Formula | PROPOSED parameter |
|---|---|---|
| **PA-1 CPU** | `B = max(m_c × Ĉ, 1.5 × P̂)` (payload); `cpu_ns(PART_A) = max(shared, B + O)` | m_c = **2.0**; shared = 120 s |
| **PA-2 wall** | `wall_ns(PART_A) = max(shared, m_w × (Ŵ + L))`, subject to m_w ≥ m_c ÷ (m_c − 1) | m_w = **3.0**; L = **30 s** until Stage 2 measures it; shared = 300 s |
| **PA-2b engine predicate** | Check `P̂ × wall ÷ B ≤ wall ÷ 1.5`: the engine's throttled prediction must use at most two-thirds of the window. The `1.5 × P̂` term in PA-1 guarantees it | — |
| **PA-3 memory** | Check `m_m × M̂ ≤ profile memory_bytes` (256,000,000 in `deploy/qualification/test-profile.json`). Memory is one shared campaign footprint (spec §2.5), so this rule never sets a per-phase value; a failure goes to an operator ruling | m_m = **1.5** |
| **PA-4 validity** | No ceiling is derived from a measurement that fails §3.2 (digests, prefix, spread) | spread 1.30 |
| **PA-5 Stage-2 consistency** | If the service-route PART_A charge exceeds the Stage 1 prescribed-arm maximum by a factor k > **1.25**, re-apply PA-1/PA-2 with Ĉ × k and Ŵ × k and record a new application | 1.25 |

**Why these values.**
- *The kernel couples wall and CPU.*
  - The payload's quota is `(cpu_ns − O) ÷ remaining_wall` (`campaign_supervisor.py:177-194`).
  - A throttled payload of CPU C finishes its CPU-bound part in `C × wall ÷ B`. At C = Ĉ that is `wall ÷ m_c`, whatever the wall ceiling.
  - The non-CPU time plus launch then needs `wall × (1 − 1/m_c)`, hence m_w ≥ m_c ÷ (m_c − 1) = 2. The value 3 adds headroom for launch and queue noise.
- *The noise seen so far.* In the 2026-09-24 records:
  - CPU spread within a depth was 1.04–1.08.
  - The Part A subprocess wall ranged 14.64–25.24 s (1.72, with a cold first repeat).
  - The internal total ranged 12.47–17.61 s (1.41).
  - Host-to-host variance is unmeasured; the two-job design measures it. m_c = 2 covers the worst observed band.
- *Cost asymmetry.* A ceiling that is too tight means a silent SIGKILL at the deadline, an IN_DOUBT terminal campaign and a blind Linux re-run (a full S4 run took 2,717 s). A ceiling that is too loose costs only Σ headroom, and the TEST_ONLY cap leaves about 8,300 s of it (§5).
- *Precedent.* The M13 ruling gave N2 a 340 s payload against 211 s measured on Windows, a factor of 1.61, without any Linux figure.
- *The shared floor.* Never going below the shared 120 s / 300 s keeps one rule for the other phases, as the N2 precedent does.

**Sensitivity (m_c = 2, O = 20 s).** The shared 120 s CPU suffices while Ĉ ≤ 50 s and P̂ ≤ 66 s. The shared 300 s wall suffices while Ŵ + L ≤ 100 s.

| Ĉ (s) | 25 (estimate §1) | 50 | 60 | 100 | 211 (N2-sized, hypothetical) |
|---|---|---|---|---|---|
| PART_A CPU ceiling (s) | 120 (shared) | 120 | 140 | 220 | 450 |

The Ĉ threshold for the shared ceiling moves with m_c: 66.7 s at m_c = 1.5, 50 s at 2, 40 s at 2.5 and 33.3 s at 3.

**Re-measurement triggers.** Any one of these invalidates the application for the next release or profile, which needs a fresh attempt anyway under contract decision 4:
1. A change to the worker runtime closure digest or to `requirements-ops.lock`. That includes `part_a.py`, `regime.py`, `paths.py`, `replay.py`, `provider.py`, `production_source.py` (in particular any N4 change to `verify_for`), `runner.evaluate_replay` and the S5 adapter.
2. A workload change: panels, paths per panel, horizon, outer months, inner block, fixture source size or legs.
3. A reference-runtime change: `host.json` pins, the worker base tag, or the runner class.
4. A change to the orchestration charge or to `CAMPAIGN_RESOURCE_SCOPE`.
5. Any Linux PART_A run whose settled charge exceeds 0.8 × B or whose wall exceeds 0.8 × the ceiling, and any PART_A overrun or OOM.
6. A Stage-2 factor k > 1.25 (PA-5).

**Scope choice for the operator (decision 2, §8):** approve the rule for PART_A only, or phase-generically for TEST_ONLY diagnostic ceilings. The phase-generic form would let the coordinator set `/v7`'s N2 ceiling from Stage 0's Linux N2 figure, instead of extending the "/v6 only" M13 ruling.

## 5. Budget feasibility

**The check at binding** (`campaign_store.py:2776-2783`):
- Σ phase `cpu_ns` ≤ cap;
- Σ phase `wall_ns` ≤ cap;
- the largest phase `memory_bytes` ≤ cap.

Each phase's `cpu_ns` already contains its orchestration charge (`profile.py:199-203` refuses a charge above the phase). The void-authentication term is zero at binding (`campaign_store.py:2794-2800`).

**The `/v6` TEST_ONLY diagnostic set** (`profile.py:209-243`):
- 12 phases;
- 11 × 120 s + N2 360 s = **1,680 s CPU**;
- 11 × 300 s + 900 s = **4,200 s wall**;
- memory 256,000,000 each.

**The TEST_ONLY cap** is 10,000 s CPU, 10,000 s wall, and memory equal to the profile's `memory_bytes` (`fixture_producer.py:154-156`), **for releases v3–v6 only** (§0 pitfall). A `/v7` release without that tuple extended binds 120 s CPU / 180 s wall and is `BUDGET_EXHAUSTED` at binding.

With the `/v7` PART_A ceiling set to X CPU and Y wall, and the other phases as in `/v6`:

| Allowance included | CPU feasible iff | Wall feasible iff | Ĉ limit under PA-1 | (Ŵ + L) limit under PA-2 |
|---|---|---|---|---|
| Σ phases only (the code check) | 1,560 + X ≤ 10,000 → X ≤ 8,440 | 3,900 + Y ≤ 10,000 → Y ≤ 6,100 | 4,210 s | 2,033 s |
| + one signing retry of a 120 s / 300 s phase (retries re-reserve outside Σ, `campaign_store.py:2879-2895`) | X ≤ 8,320 | Y ≤ 5,800 | 4,150 s | 1,933 s |
| + D3's future two compute re-executions (R9; not S5) | 1,680 + 3X ≤ 10,000 for X > 360 → X ≤ 2,773 | Y ≤ 1,933 | 1,376 s | 644 s |

**Proposed feasibility evidence for RC-3:**
- Before release: the arithmetic above, with the applied X and Y, recorded in the application entry.
- At C3: the executed binding test, which lands with S5 because `/v7` does not exist before the S5 build (see RC-3, §7).
- Two gaps the application entry states: Σ counts one reservation per phase, and no code checks wall slack for queues between works (cap − Σ = 5,800 s here).

**D2 falsifier** ("revisit the uniform model if PART_A's maximum-expansion CPU cannot be bounded ahead of time", draft §2.3):
- **TEST_ONLY: not triggered on present evidence.** The workload is fixed (14 replays) and deterministic (fixed root and source). Every row of the table above leaves room orders of magnitude beyond the §1 estimate. It **would** be triggered for S5 if Stage 1 cannot produce a valid measurement (§3.2 fails twice) or if the digests differ across repeats.
- **Production: out of scope, flagged.** Counts are fixed (40,203 `verify_for` calls) and the per-call cost does not depend on content, so the CPU is structurally boundable. Its size is another matter. The 2026-09-24 linear extrapolation of about 89 s per call would put Part A's re-verification alone near 994 h; that is an extrapolation, not a measurement. Whether it fits any admissible production cap is a question for the production budget owner and for N4.

## 6. TEST_ONLY application procedure (after approval only)

1. **Preconditions:**
   - an operator ruling approving the rule, with any amended parameters, recorded as a dated entry under the S5 ledger entries of the execution-slices plan;
   - a Stage 1b record with `validity.ok = true`.
2. **Compute** X, Y and the PA-3 check from the record. Show every input with its record path and SHA-256, and every rounding.
3. **Feasibility:** the §5 table with the applied values, including the two `/v7` preconditions from the §0 pitfalls (the fixture cap tuple and the N2 widening).
4. **Record** one ledger entry, "Coordinator application — PART_A TEST_ONLY diagnostic ceiling under the approved measurement-and-margin rule (date)". It states:
   - the rule version and the inputs;
   - X and Y, and whether the shared 120 s / 300 s ceiling suffices;
   - the feasibility result;
   - the scope: the TEST_ONLY `/v7` diagnostic profile only, with no production value set or implied.
5. **Implement only if X or Y exceeds the shared ceiling:**
   - Add a `/v7`-gated PART_A constant beside `_JOINT_N2_DIAGNOSTIC_PHASE` in `profile.py`, citing the ledger entry.
   - It lands with the S5 build (`profile.py` is in S5's file list).
   - When the packet is re-anchored (RC-6), the S5 packet's "no allowance/ceiling change" clause gains a pointer to the entry.
6. **At C3:** run Stage 2 and PA-5. A new value is a new profile revision and needs fresh attempts.
7. **Never** set a production ceiling or cap, a value outside the rule, or a value without a measurement under this procedure. Each of those needs an operator ruling.

## 7. RC-1..RC-6 status (S5 decision draft §5)

| RC | Status | Evidence | Owner | Next action |
|---|---|---|---|---|
| RC-1 rulings recorded | **Partly met** | The ledger entry "S5 directions adopted, hold kept" is at plan lines 801–815 on `ba7247a` (PR #517), which is **not on `main`**: `git merge-base --is-ancestor ba7247a origin/main` returns no, and `main@8e9e084` has only the 2026-09-25 HELD entry, at line 797. `main`'s STATE records the ruling with a pointer to PR #517 (`af81e54`) | Coordinator; operator merges | Merge PR #517; RC-1 is then met on `main` |
| RC-2 owner text applied | **Unmet** | None of draft §1.5, §2.5 or §3.4 is applied. Contract decision 3 is unchanged (plan line 88), and so is the spec §2.6 table (spec lines 143–153). The delta §10 hook, run on this head for boundary, K3, N1 and N2, prints `UNROUTED` for all four. Draft §6 Q12 (the OF-5..OF-7 gates) is unresolved | Coordinator drafts; operator accepts | After the stack lands: owner-text PRs for boundary spec §3.1, full-E1 spec §2.2a/§2.4/§2.5/§2.6/§5, and slices plan decisions 3 and 6 plus the S5 text; resolve Q12; re-run the hook |
| RC-3 PART_A envelope | **Unmet** | No maximum-expansion measurement exists (§0 findings 1–2). There is no `/v7` profile (`profile.py` defines v1–v6). This proposal returns the rule; it is not approved | Operator approves the rule; coordinator measures and applies | Decisions 1–4 (§8); Stage 0/1; the §6 application; Stage 2 at C3. Open point: RC-3 asks for Σ-feasibility "for the `/v7` profile", which exists only after the S5 build. This proposal offers the §5 arithmetic before release and the executed test at C3 (decision 5) |
| RC-4 client seed view | **Unmet** | The client may `FETCH_PLAN_CHUNK` (`campaign_protocol.py:92`), and the plan still carries seed values (`seed_identity.py:39`). No owner or slice is named, §1.5(d) is not applied, and there is no F1 admission check. The ruling names no gate owner | Unassigned (draft §6 Q10: TB-F1 or a qualification slice) | Name the owner and slice; apply §1.5(d); write the F1 admission-check text in the owner record |
| RC-5 OF-1..OF-7 assigned | **Unmet** | No owner record holds the assignment, and the Q12 gate discrepancy is open | Unassigned | Resolve Q12; for each OF, record the owner, the gate it precedes and where its record lands. Boundary spec §3.1 is the natural owner |
| RC-6 packet re-anchored | **Unmet** | S5 packet §7 is "_Pending._", and its §0 anchors were never taken at the S4 merge head (`228447c`). Its prerequisite, the §3.4(d) text, is not applied (RC-2) | Coordinator | After RC-2, re-read §0 at the release head. Fold in: §0 finding 1 (the Linux "prescribed expansion" case is impossible on (2, 4, 2), so the arithmetic boundary test stands alone), both §0 pitfalls, and the §6 pointer |

**Release proposal: none is supported.** Five of six conditions are unmet, and RC-1 is not yet on `main`. The two immediate blockers the draft names both remain open: corrected owner text (RC-2) and a defensible measured envelope (RC-3). RC-3 cannot close until the operator approves a rule and a Stage 1b record exists.

## 8. Operator decisions requested

1. **The rule:** approve, amend or reject PA-1 to PA-5 and their PROPOSED parameters: m_c = 2.0, m_w = 3.0, L = 30 s, m_m = 1.5, spread 1.30, PA-5 factor 1.25, and the shared-ceiling floor.
2. **The rule's scope:** PART_A only, or phase-generic for TEST_ONLY diagnostic ceilings (§4). This decides how `/v7` gets its N2 ceiling.
3. **The `/v7` N2 ceiling:** extend the M13 "/v6 only" ruling to `/v7`, or apply the rule. Applying the rule needs decision 2 to be phase-generic, and Stage 0.
4. **The measurement steps, approved separately:** Stage 0, an artifact download (**retention ends about 2026-10-09**); and Stage 1b, a new `workflow_dispatch` measurement job, which is both a CI configuration change and a Linux host dispatch.
5. **RC-3 feasibility evidence:** whether the §5 arithmetic on proposed `/v7` values counts as pre-release feasibility evidence, with the executed binding test at C3.

## 9. Unverified and limits

- **Linux CPU:** the Linux payload CPU of any stage is not read here. Whether the S4 artifacts' journals carry `Consumed … CPU time` lines is unverified (Stage 0).
- **Cited record:** the record `20260924T034139Z-59ce3c4b7643` (N2 211.39 s, N1 13.36 s) was not found locally. Both figures are cited from the ledger (plan line 756).
- **Runner hardware:** the GitHub runner hardware class comes from vendor documentation and is not verified. The Stage 1b dry run must confirm that systemd 255 populates `CPUUsageNSec` and `MemoryPeak` for an exited `RemainAfterExit` unit.
- **The §1 CPU figure** is arithmetic from Windows per-call costs, not a measurement, and is used only for orientation.
- **Capture and G5 phases:** PART_A_CAPTURE and PART_A_G5 costs are not covered. G5 does not replay (spec §2.7; slice S5 interfaces), so they are expected to be small. Stage 2 records their settled charges against the shared ceiling.
- **Guardian CPU:** the guardian's `LimitCPU` is O − 7 s = 13 s (`campaign_supervisor.py:284-297`). Whether it stays within that while archiving two Part A artifacts is observable only at C3. A guardian that exceeds it is killed and the work becomes IN_DOUBT. Changing O is profile-wide and outside this rule.
- **Out of scope:** the production mapping, the production cap and N4.

## Verification of this note

```bash
# Expansion pinned for every domain; TEST_ONLY workload (2 initial, 4 expanded, 2 paths per panel)
grep -n 'Decimal("0.95"), Decimal("0.01")' ops/c1_rail/qualification/contract.py
grep -n "QualificationWorkloadPolicy(counts,5,5,6,2,4,2)\|'PART_A':2\|initial_panels=2,expanded_panels=4" tests/ops/qualification/composition_fixture.py
# No Part A expansion in any measured composition run (expect PART_A REGIME 4 and 3 panel proofs)
python -c "import json;[print(r['confirmation_depth'],r['path_counts'].get('PART_A'),r['phases']['e1_run']['components'].get('proof.part_a_panel_proof',{}).get('calls')) for r in json.load(open('docs/notes/2026-09-24-t10-step4/composition-sweep.json'))['rows']]"
# verify_for on every replay and proof; one verify_for at compute start
grep -n "self.verify_for(self.contract)\|result = self.replay(path)" ops/c1_rail/qualification/production_source.py
grep -n "source.verify_for(contract)" ops/c1_rail/qualification/execution/compute.py
# Engine pilot predicate; seeds independent of the expansion decision
grep -n "predicted = \|def seed\|extend(request.max_panels)" ops/c1_rail/qualification/part_a.py
# /v6-only N2 widening; fixture cap tuple v3-v6 only
grep -n "== 'qualification_execution_profile/v6'" ops/c1_rail/qualification/execution/profile.py
grep -n "if release_doc\['schema'\] in" tests/integration/qualification_boundary/fixture_producer.py
# Binding feasibility and payload quota
sed -n 2776,2783p ops/c1_rail/qualification/execution/campaign_store.py
grep -n "quota = budget_cpu_ns" ops/c1_rail/qualification/execution/campaign_supervisor.py
# RC-1: the ruling entry is not on main
git merge-base --is-ancestor ba7247a origin/main && echo on-main || echo not-on-main
```
