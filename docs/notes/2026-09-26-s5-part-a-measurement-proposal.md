# S5 Part A measurement-and-margin proposal, and RC-1..RC-6 status

**Status:** PROPOSAL, returned for operator approval. Nothing here is approved. Every number marked PROPOSED is a proposed rule parameter, not a ceiling. S5 stays **HELD** ([ledger, 2026-09-26](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26)). *Qualified 2026-09-26: the operator conditionally approved the §4 numerical defaults for PART_A TEST_ONLY measurement only, not yet applicable; see the ruling block below the corrections. No ceiling is set.*
**Card:** [S5 Part A measurement proposal](../briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md), dispatched at `62c956f`. **Authority:** operator ruling 2026-09-26 §6 (resource-envelope decision), quoted in the card.
**Sources read at `62c956f`.** Under `ops/`, `tests/`, `tools/`, `deploy/`, `scripts/` and `.github/`, that head does not differ from `main@8e9e084` (`git diff --stat origin/main HEAD` over those paths is empty). The sources were the S5 decision draft, the execution-slices plan, the full-E1 spec §2.4–§2.6, the S5 packet draft, the [2026-09-24 measurement](2026-09-24-t10-step4-representative-measurement.md) and its raw data, and the code named in each section. **No measurement, Linux dispatch, qualification service, artifact download or S5 work was run.** Every figure below is either cited from an existing record or labelled as arithmetic from cited figures.

**Correction 2026-09-26 (PR #519 review).** A review of PR #519 at `8c15f18` found three defects in this proposal and one stale status. The reviewer inspected documents and cited code and ran no tests. The dated corrections below govern. Superseded sentences are struck, not deleted. The corrections were checked against the sources at `8c15f18`, whose tree outside `docs/` equals `main@5ad04cf` (`git diff --name-only 5ad04cf HEAD` lists only notes and handoff cards). Nothing here approves the rule, closes an RC, releases S5 or authorizes execution. Every numeric parameter stays PROPOSED.
- **F1 (§1, §3.4 Stage 1c, §4, §6, §8, §9).** Nothing specified how Stage 1c would force expansion through the real S5 adapter. At this head no measurement-only way to do that exists without a change. A new Stage 1c-prep proposes one, for separate approval.
- **F2 (§3.1, §3.4, §3.5, §4, §6, §9).** A process memory value is a lower bound and cannot pass PA-3. Without aggregate peak-memory evidence, memory feasibility is **UNVERIFIED** and RC-3 cannot close.
- **F3 (§5).** A blocked or invalid measurement is not the D2 falsifier. Outcomes are now classified as blocked, invalid, or bound-not-establishable, each with its own consequence.
- **H1 (§0, §7).** PR #517 has merged (`main@5ad04cf`). §7 now opens with the coordinator's current disposition. The executor's table is kept as its snapshot at `0a4cde5`/`32c4d40`.
- **Stage 0 status (§2, §3.4, §8, §9).** The operator approved the S4 artifact download on 2026-09-26. The logs are preserved locally and have not been analysed.

**Correction 2026-09-26 (PR #519 review, round 2).** A refute-first review of the corrections above returned twelve findings; two pairs overlap. Each was checked against the sources at `8c15f18` and applied below as a dated round-2 edit. Nothing here approves the rule, closes an RC, releases S5 or authorizes execution.
- **F2a, shared memory (§3.1, §3.4 Stage 2, §3.5, §4 PA-3, §6, §7, §8, §9).** The measured unit is still not the scope the shared limit charges. The service's `memory.max` sits on the host-run parent cgroup, which also holds qexec, the launch clients and the guardian. The Stage 1b/1c M̂ therefore covers the payload only (PA-3a). Feasibility against the shared limit stays **UNVERIFIED** until Stage 2's parent `memory.peak` is checked (new PA-3b). Whether RC-3 can close on payload-only evidence is decision 7.
- **F1a, Stage 1c coverage (§1, §3.4, §4, §5, §8).** `run_part_a_compute` returns byte strings. The worker-side result path (encode, validate, frame, output write, fsync) is outside it, so Stage 1c does not measure it. That path is now a named uncovered residual, R̂, and Ĉ₁c no longer claims the whole §1 workload. Stage 1c-prep now also pins where the packet's unnecessary-expansion rejection is enforced. A refusal is classified by its cause.
- **F3a, outcome taxonomy (§3.2, §5, §8).** A missing aggregate memory reading does not make a run Invalid. A missing Stage 1c-prep seam is Blocked only before approval. A digest mismatch bears on R7 only after diagnosis. The reading of the D2 falsifier goes to the operator (decision 6).
- **Housekeeping.** PA-5 without a forced arm (§4); a superseded Stage 0 sentence struck (§2); one citation corrected in place (`:2596`, §3.1).

**Operator ruling 2026-09-26 (in session): conditional, PART_A TEST_ONLY measurement only.** Owner: the [execution-slices ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26) ("Conditional Part A-only approval"), which governs; this block mirrors it. It qualifies the Status line above for the numbers below only; everything else in this note stays a proposal.
- **Conditionally approved numbers (§4), for PART_A TEST_ONLY measurement only; not for other phases, not for production:** m_c = 2.0; m_w = 3.0 with L = 30 s; m_m = 1.5; warm-repeat spread threshold 1.30; PA-5 service/harness threshold 1.25; the retained shared floors (120 s CPU, 300 s wall) and upward rounding. The pilot-budget formula is not among them: it needs validation under the service's throttling.
- **Applicability conditions.** The rule applies only after the identified measurement defects are corrected and reviewed, including: a concrete way to exercise maximum expansion through the built adapter (including the baseline derivation and real artifact writing); aggregate memory evidence (a lower bound cannot establish memory feasibility); separation of missing permission, invalid measurements and genuine evidence against the accounting design; and measurement in the worker image where practicable, with any runtime mismatch explicit and requiring validation. *(Recording consequence, not ruling text: until then, §6 does not start.)*
- **Not closed or authorized:** no provisional ceiling closes RC-3; no S5 execution or production budget. S5 stays **HELD**.
- **Returns owed by the coordinator:** the corrected harness/workflow and its exact dispatch scope, for approval (preparation is authorized; S4 evidence preservation is done); an explicit `/v7` N2 disposition (N2 kept separate; no silent revert or carry-forward); an explicit staged gate amendment separating permission to build S5 from acceptance of its completed adapter (C3 adapter measurements cannot count as completed pre-build evidence).

## 0. Summary

**What is returned for approval:** a measurement standard and a margin rule (§3, §4). The coordinator applies it to TEST_ONLY diagnostic ceilings only after approval (§6).

**Findings that shape the rule:**

1. **The TEST_ONLY workload S5 will run can never expand.** The contract pins the expansion test to `|p5 − 0.95| ≤ 0.01` for every domain (`contract.py:761-773`). The TEST_ONLY workload has 2 initial panels with 2 paths each (`composition_fixture.py:195`, `:236`, `:241`). A panel's pass rate is therefore 0, 0.5 or 1, and the initial p5 is never within 0.01 of 0.95. (The p5 is the nearest rank, `ceil(0.05 × 2) = 1`, so the minimum of the two panels.) The smallest per-panel depth that can expand is 17 (16/17 ≈ 0.941). So no genuine S5 campaign on this fixture takes the expansion branch, whatever the synthetic source. The existing record agrees: all six composition runs that reached Part A ran 3 panel proofs and 4 Part A paths, with no expansion (`2026-09-24-t10-step4/composition-sweep.json`, depths 2 and 10). **Maximum expansion (4 panels) therefore has to be measured with a forced-expansion harness (§3.3), not through the signed route.**
2. **No existing measurement covers maximum expansion.** `benchmark_part_a.py` measures one panel and one path and bypasses `ProductionSource`, so it omits the dominant cost (`benchmark_part_a.py:1`, `:45-77`). The 2026-09-24 composition harness runs the signed route, which never expands (finding 1).
3. **Per-call source re-verification dominates.** Every replay, including each panel proof, calls `verify_for` (`production_source.py:867`, `:891-894`). On the fixture it cost 1.02–1.16 s CPU per call (Windows, CPython 3.13.2; all nine rows of `composition-sweep.json`, `proof.source_reverify` CPU ÷ calls). The per-call cost rises with run depth: 1.02–1.05 s at depth 2 (32 calls), 1.04–1.09 s at depth 10 (56 calls) and 1.08–1.16 s at depth 30 (107 calls). The cause is not identified. The 2026-09-24 note reports 1.2–1.5 s per call in wall time (its §1). The N2 figure behind the 2026-09-24 ruling is the same size: 211.39 s CPU on Windows for 180 paths, about 1.17 s per path.
4. **The Part A engine already predicts maximum expansion, and refuses if the prediction exceeds its budget.** Its pilot predicts `probe + max_panels × (rebuild + depth × path)` and raises before any panel if that exceeds `budget_seconds` (`part_a.py:178-186`), even when expansion will not be needed. In the service route the pilot runs under the kernel CPU-rate quota (`campaign_supervisor.py:177-194`), so the PART_A ceiling must cover the throttled prediction of maximum expansion (§4, PA-2b).
5. **The recorded host factor has no recorded basis.** The C2 ruling states "roughly 137 s on Linux by scaling" (plan line 756) without evidence. The measurement record it cites (`20260924T034139Z-59ce3c4b7643`) was not found in any local checkout. The rule applies **no** host factor: it measures on the reference runtime directly.

**Build pitfalls for S5, returned to the coordinator (not changed here):**
- **`/v7` needs three edits in `diagnostic_budget_profile`, and each one missed fails differently.**
  - **Refused outright today.** The function raises `fresh diagnostic execution profile required` for any schema outside v3–v6 (`profile.py:219-226`). Until `/v7` is added there, no `/v7` diagnostic budget profile can be built. (`parse_profile` also selects its fixed fields per schema, `profile.py:116-140`, so the `/v7` execution profile must be defined there first.)
  - **Unfunded if only the accept tuple is extended.** The funded budget-schema branch lists only v4–v6 (`profile.py:243-252`). If `/v7` is added only at `:219-226`, it gets `qualification_campaign_budget_profile/v2` with no `funding_intents`.
  - **N2 falls back to 120 s if the N2 branch is missed.** The N2 widening applies only when the schema is `v6` (`profile.py:239`), and the M13 ruling is "/v6 only" (plan line 757). If `/v7` is added at `:219-226` and `:243-252` but not at `:239`, N2 gets the shared 120 s CPU, below its measured 211 s. That is the silent-SIGKILL failure checkpoint C2 found. Adding `/v7` at `:239` needs an N2 value: either the operator extends the M13 ruling, or the rule is applied to N2 on its own §3-conformant N2 measurement (decision 3, §8).
- **`/v7` loses the fixture cap.** `fixture_producer.py:152-156` raises the TEST_ONLY cap to 10,000 s only for release `v3`–`v6`. A `v7` release would bind the default 120 s CPU / 180 s wall, and Σ-feasibility would fail at binding (§5).

~~**RC status:** RC-1 partly met; RC-2 to RC-6 unmet.~~ **RC status (corrected 2026-09-26, PR #519 review):** RC-1 is recorded on the reviewed base, `main@5ad04cf`. RC-2 to RC-6 remain open. **No S5 release proposal is supported** (§7).

## 1. Maximum-expansion workload

**Definition.** One PART_A compute work (phase `PART_A`, `campaign_budget.py:12-13`) that runs `_run_part_a` from pilot through appended panels `[initial_panels, expanded_panels)`. This is what the S5 adapter will do (`compute.run_part_a_compute`, S5 packet §1; the slice plan's "one Part A operation"). The work includes:
- worker start;
- source admission;
- one `verify_for` at compute start, the same shape as `compute.py:28`;
- the pilot: one outer panel, one proof replay of that whole panel, and one horizon path (`part_a.py:178-180`);
- for each panel index `0..expanded_panels−1`: outer sampling, one proof replay of the panel (`regime.py:83`), and `paths_per_population_per_panel` horizon paths, each evaluated (`part_a.py:195-204`);
- the N2 FULL baseline derivation from staged N2 capture bytes (S5-D2: the worker derives the N2 FULL pass rate from `n2_full_outcomes`, S5 packet draft line 22);
- serialization and fsync of the initial-prefix and final artifacts (S5-D1).

**Not covered before C3.** The last two items do not exist until the S5 build: the derivation code and the two-artifact format are S5's. Stage 1 (§3) cannot measure them. §4 carries them as an explicit term, D̂, that is **uncovered** until C3 measures it (§3.4, Stage 1c). *Correction 2026-09-26 (PR #519 review, F1):* Stage 1c can measure them at maximum expansion only if it can force expansion through the built adapter, and nothing yet provides that. §3.4 Stage 1c-prep proposes a mechanism, which needs its own approval. *Correction 2026-09-26 (PR #519 review, round 2, F1a):* even with that mechanism, Stage 1c covers these items only up to the adapter's return of the two documents as byte strings (S5 packet §1, line 27). The worker-side result path that follows, including the output write and fsync, is a named uncovered residual, R̂ (§3.4).

The seeds depend only on panel and path index (`part_a.py:139-142`). A forced expansion therefore performs exactly the computation that a prescribed expansion would on the same contract, source and root, which makes the forced arm below a faithful workload.

**Owners of the numbers:**
- **the full-E1 spec §2.4, which defines the Part A work unit** (`docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md`):
  - line 117: Part A uses `contract.replay.part_a` and the N2 FULL pass rate, recomputed by the worker and by G5 from captured N2 bytes; the probe is charged to the campaign budget; no extra pilot on recovery;
  - line 119: the inverse-ECDF rank `ceil(percentile × initial_panels)`, the inclusive tolerance test, and appending only `[initial_panels, expanded_panels)`;
  - line 121: the initial prefix is retained, and the first `initial_panels` entries of an expanded result must be byte-identical to it;
  - line 125: Part A is one dispatched compute operation using the existing append loop, with no partial-panel resume;
- **the freeze candidate for the production depth** (`docs/briefs/phase3-preparation/2026-09-15/freeze-candidate.md`, marked "DRAFT — NOT FROZEN" at line 3): 200 paths per panel, 100 initial panels and reserved panels 100..199 (lines 110-113), and continuous 500-session paths (line 98). Its compute-depth companion gives 100 × 200 = 20,000 ordinary and 200 × 200 = 40,000 reserved-maximum Part A paths (`compute-depth.md:59-60`). `test_contract.py:131` carries the same 200 as a test document, not as an owner;
- the frozen contract's `replay.part_a` and `replay` fields (`production.py:89-96` shows the mapping into the engine request);
- the workload policy (`trust_domain.py:382-385` pins production to 100/200 panels, 6 months and 5 sessions);
- the budget profile: "PART_A includes maximum expansion" (`profile.py:167`).

| Quantity | TEST_ONLY S5 workload (Linux fixture) | Production (reserved maximum; freeze **candidate**, not frozen) |
|---|---|---|
| initial → expanded panels | 2 → 4 (`composition_fixture.py:241`) | 100 → 200 (`trust_domain.py:382`; freeze candidate lines 110-113) |
| paths per panel | 2 | 200 (freeze candidate line 110; not frozen, and every production count below depends on it) |
| horizon / inner block / outer months | 5 / 5 / 6 (`composition_fixture.py:195`) | 500 (freeze candidate line 98) / 5 / 6 |
| source | composition fixture, trading variant: 174 sessions, 4 bars per session per leg, 4 legs (2026-09-24 note §1) | admitted cold-replay source (~95k M15 bars per leg, 2026-09-24 note §2) |
| replays at maximum expansion | 2 pilot + 4 × (1 proof + 2 paths) = **14** (5 panel proofs, 9 horizon paths) | 2 + 200 × 201 = 40,202 |
| `verify_for` calls | 15 | 40,203 |
| replays with no expansion | 8 | 20,102 |
| can the prescribed rule expand? | **No** (§0 finding 1) | Yes |
| budget binding paths | `part_a_initial_paths=4`, `part_a_expanded_paths=8` (`composition_fixture.py:242`) | per F1 |

**Arithmetic estimate, not a measurement and not a ceiling input.** At the cited 1.02–1.16 s CPU per `verify_for` (Windows, §0 finding 3), 15 calls give about 15–18 s. The rest adds a few seconds:
- five panel proofs, each over a panel as long as the whole source (174 sessions, since `sample_outer_panel` concatenates six-month blocks until the panel reaches `len(sessions)`, `regime.py:68-78`);
- nine 5-session paths;
- worker start and source admission (the source build alone cost about 2.0 s CPU, `proof.source_build` in `composition-sweep.json`).

The expected TEST_ONLY maximum-expansion payload is therefore roughly 20–30 s CPU on the Windows development host. This excludes the harness's fixture setup, which is not worker work (10.4–12.4 s CPU in the same record, `setup_fixture_domain_contract_source`), and it excludes D̂. The Linux value is unknown (§0 finding 5).

## 2. Reference runtime

**TEST_ONLY reference runtime = the host class that runs S5's acceptance-grade Linux campaigns.** The ceiling only has to hold there. Recorded identity per run:

| Field | Value or source |
|---|---|
| Host class | GitHub-hosted `ubuntu-24.04` runner, as in `qualification-s2-supervision.yml:68`. The workflow does not pin hardware; each run records the `/proc/cpuinfo` model name and `nproc`. GitHub documents 4 vCPU / 16 GB for standard public-repository Linux runners; that is not verified here |
| OS | Ubuntu 24.04 x86_64, ext4 (`tools/qualification_verification/host.json`); kernel recorded from `uname -r` |
| Interpreter measured by Stage 1b | The **host venv**: Ubuntu's `/usr/bin/python3`, CPython 3.12.3 (`host.json` `python` and `python_version`), provisioned as `$host_root/env`. Stage 1b runs outside any container and without the qualification service. Recorded as `runtime_kind = host_venv` |
| Interpreter the S5 worker runs | A **different build**: the Docker worker image, based on `python:3.12.3-slim-bookworm` (a separately built CPython on Debian) and resolved to a digest at build (`image.py:53-64`). Image digests differ per install (S4 acceptance read: `775e780e…`, `65b0c63c…`). Build flags, glibc and the overlay filesystem can differ from the host venv. Only Stage 2 (C3) runs on this interpreter |
| Dependencies | `requirements-ops.lock` SHA-256 `9aa7c17c…` (`host.json`); thread environment pinned to 1 (`profile.py`, `CAMPAIGN_RESOURCE_SCOPE.controller_environment`) |
| Code identity | measured commit, clean tree; worker runtime closure digest (`execution/runtime.observe_runtime(repo, 'worker')`); harness SHA-256; fixture file SHA-256s |
| Release identity | none exists before S5 (`/v7` is S5's). Stage 2 (§3.4) records the `/v7` release, profile and policy digests |

**Host venv to worker container: an unmeasured factor.** Stage 1b measures the host venv, not the worker image. The host-to-container factor is therefore **unmeasured**, just as the Windows-to-Linux factor is. The only check on it before any acceptance-grade reliance is PA-5 at C3. The better design runs the harness inside the built worker image, under a cgroup with the payload's limits, and records the image digest. It is not specified here, because it is unverified that the worker build context (`prepare_context`, `image.py`) carries the test fixtures the harness needs. If the operator prefers it (decision 4), the harness runs in the image, `runtime_kind = worker_image`, and `image_digest` becomes a required field; with `host_venv` it stays null.

**Mapping to the production service host: none.**
- No production qualification host exists yet. Provisioning it is obligation OF-1 (draft §1.3).
- No host factor is evidenced: the "~137 s on Linux by scaling" figure has no recorded basis (§0 finding 5). The rule therefore uses **no host factor**. Windows figures serve only to develop the harness and check orders of magnitude.
- A production ceiling needs its own measurement on the production host class, under the production budget owner. The ruling says production budgets remain separately governed.

**Evidence that could calibrate a Windows/Linux factor already exists.** The S4 Linux runs (36180568493, 36181780676) retained `journal.log` and `systemd-units.log` for 14 days (`qualification-s2-supervision.yml:143-178`). Those logs may hold the consumed CPU of the N1/N2 payload units, which could be paired with the Windows figures of 13.36 s and 211.39 s. It is unverified that the lines are present. ~~Reading them is Stage 0 (§3.4), a download that needs approval. **The retention expires about 2026-10-09.**~~ *(Superseded 2026-09-26: see the correction below.)*

*Correction 2026-09-26 (PR #519 review; Stage 0 status):* the operator approved the download on 2026-09-26. Both runs' `qualification-s2-supervision` artifacts are preserved in the operator's primary checkout at `local_artifacts/s4-linux-run-logs-2026-09-25/`, which is gitignored there. It holds 222 files, 111 per run (`run-36180568493/`, `run-36181780676/`), listed in `SHA256SUMS`. That file's SHA-256 is `e2c142281d819e071d15f99a242358f93389a479dcc5e6b5c1f6a20d5db189a7`, and `sha256sum -c` over the listed files passes. GitHub's expiry therefore no longer removes the only copy. The logs are preserved only: they have not been read or analysed. Reading them for calibration remains Stage 0 work under the measurement rule, once that rule is approved.

## 3. Capture method

### 3.1 What is measured

**CPU is split at the harness boundaries.** Each fresh repeat process does work a service worker never does: fixture generation, Ed25519 key generation and signing, and trust-domain and contract validation, all inside `build_verified_composition`. On Windows that setup cost 10.4–12.4 s CPU (`setup_fixture_domain_contract_source` in `composition-sweep.json`), against an estimated 20–30 s workload (§1). A whole-process figure would therefore inflate the Stage 1 value and bias PA-5 downward. The harness reads the CPU clock at each boundary of §3.3 and records these components separately:

| Component | Boundary (§3.3) | In Ĉ? |
|---|---|---|
| `start` | process start → harness entry, read before any fixture import (interpreter start and engine imports; the worker's start) | yes |
| `admission` | the source build inside setup (`ProductionSource._build_composition`, one call, timed by a single wrapper that is removed immediately after, as `measure_composition.py.txt:58-72` does) | yes |
| `setup_excluded` | the rest of step 1 (fixture, keys, signing, trust domain, contract) | **no** |
| `verify` | step 2, the compute-start `verify_for` | yes |
| `part_a` | step 4, immediately before and after `_run_part_a` | yes |
| `serialize` | step 5 (stand-in serialization) | yes |

The **workload CPU** of a repeat is `C_w = start + admission + verify + part_a + serialize`. The N2 baseline derivation and the real S5-D1 serialization are not in it; they are D̂ (§1, §4).

| Measure | Primary (inside the repeat process) | Secondary (system manager, Linux) |
|---|---|---|
| CPU, Linux | `resource.getrusage` user+sys for `RUSAGE_SELF` plus `RUSAGE_CHILDREN`, read at every boundary above; the whole-process total at exit | the transient unit's `CPUUsageNSec` (cgroup `cpu.stat` total including every descendant). Its workload share is `CPUUsageNSec − setup_excluded` |
| CPU, Windows (Stage 1a only) | CPython on Windows has no `resource` module. Boundaries use `time.process_time()`, which is `GetProcessTimes` user+kernel of the process itself. The Stage 1a launcher puts each repeat process in a job object and reads `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION` `TotalUserTime + TotalKernelTime`, which includes terminated children, as the whole-process total | — |
| Wall | outer: process launch to exit (`ExecMainStartTimestampMonotonic` → `ExecMainExitTimestampMonotonic`); boundaries: `perf_counter` at the same points as CPU. Workload wall = outer − `setup_excluded` wall | — |
| Memory | `production._peak_memory_bytes()` called at exit, so the engine's own reader is used on each platform: `ru_maxrss` on Linux, `PeakWorkingSetSize` from `GetProcessMemoryInfo` on Windows (`production.py:99-121`). The high-water mark includes setup, so it overstates the worker. *Corrected 2026-09-26 (F2):* it covers one process and omits cgroup-charged memory, so it is recorded for orientation and never becomes M̂ (below) | the unit's `MemoryPeak` (cgroup `memory.peak`), swap off. *Corrected 2026-09-26 (F2):* the only admissible source of M̂ (below) |
| Engine facts | `PartAResult.probe_seconds`, `predicted_seconds`, `elapsed_seconds`, panel count, `expanded` | — |
| Integrity | SHA-256 of the canonical initial-prefix and final serializations | — |
| Call counts | replay, proof and `verify_for` counts, from **one extra instrumented repeat per arm**, run **last** and excluded from timing statistics (counting wrappers perturb timing) | — |

The ceiling's CPU input per repeat is the **larger** of `C_w` and the unit's workload share (`CPUUsageNSec − setup_excluded`), so the launcher's overhead is charged. ~~For memory it uses the cgroup `MemoryPeak` when present, else the primary value, flagged as a lower bound.~~

**Correction 2026-09-26 (PR #519 review, F2): memory needs aggregate evidence.** The service enforces memory on the cgroup, not on a process:
- it checks that the supervisor's parent cgroup has `memory.max` equal to the profile's `memory_bytes` (`campaign_supervisor.py:830`);
- it sets the worker container's `Memory` and `MemorySwap` to that value, under the payload slice, with a tmpfs `/tmp` (`:2592-2596`);
- it observes that parent cgroup's `memory.peak` (`:974`).

The primary value is one process's resident set (`production.py:117-120`). The measured unit holds more than that process: `scripts/fp.py` first runs an environment probe (`fp.py:107-110`) and then starts the harness as a child (`:274`). A resident set also omits memory the cgroup charges outside it, such as page cache and tmpfs. A process value is therefore a lower bound, and a lower bound below the limit does not show that the workload fits. So:
- **M̂ comes only from aggregate evidence covering the whole unit:** the unit's `MemoryPeak` (cgroup `memory.peak`), or another reading of that same counter, such as the unit cgroup's `memory.peak` file read before the unit is stopped.
- **A fallback is admissible only when the record establishes its coverage:** every process in the unit, and the memory the limit charges. No such fallback is specified here.
- **If any timed forced-arm repeat lacks aggregate evidence, M̂ is undefined.** Memory feasibility is then **UNVERIFIED**: PA-3 is not evaluated (it neither passes nor fails), and RC-3 cannot close. The process values stay in the record for orientation only.
- CPU and wall may still be applied from their own evidence. That does not make memory verified.

**Correction 2026-09-26 (PR #519 review, round 2, F2a): the unit aggregate covers the payload, not the shared footprint.** The rule above, that M̂ comes only from an aggregate over the whole unit, stands. But the whole unit is still less than what the shared limit charges:
- The `memory.max` the service checks (`:830`) belongs to the host-run parent, `self.parent = _host_path(host_run_id)` (`:811`, `:766-773`). That parent is the persistent host slice qexec runs in, and all campaigns observe it "including shared qexec/launch clients" (`:802-804`). The guardian unit runs beneath the work slice (`:1413-1414`). The payload slice, which holds the worker container (`:2594`), sits beneath the same parent (`manager_start_arguments`, `:740-750`; `_scope_path`, `:776-788`).
- The spec's scope includes "all campaign controllers/guardians, launch clients, workers, descendants and role helpers" (full-E1 spec line 277). It treats memory as "a maximum concurrent campaign footprint" (spec §2.5, line 135).
- The Stage 1b/1c unit runs none of the non-payload processes. Its `MemoryPeak` is evidence only for the payload container's own `Memory`/`MemorySwap` limit (`:2592-2593`), subject to the host-venv/container gap of §2. It is **not** evidence for the shared host-run limit (`:830`). In the bullets above, "PA-3" now means PA-3a, the payload check (§4).
- **Feasibility against the shared limit stays UNVERIFIED** until there is an aggregate covering the host-run scope. The only one this proposal collects is Stage 2's settled PART_A `memory_peak_bytes`, read from the parent's `memory.peak` (`:974`). That counter is never reset per work (`:804`; spec line 279), so it is the host-run high-water mark through PART_A settlement. The new PA-3b checks it (§4). No measured allowance for the non-payload processes is specified, and m_m is not assumed to cover them.
- Stage 2 runs the genuine campaign, which never expands (§0 finding 1). Its parent peak therefore covers the shared scope at the prescribed workload, not at maximum expansion. §4 PA-3b states how that gap is handled.
- Whether RC-3's memory item can close on payload-only evidence is an operator decision (decision 7, §8). Until the operator rules, it cannot.

**Windows figures are not comparable** to the Linux `getrusage` and cgroup figures: the clock, the child accounting and the memory measure (working set against resident set) all differ. They validate the harness only and never enter a ceiling.

### 3.2 Repeats, statistic and noise

- **Arms:** two, of which only `forced` sets the ceiling.
  - `prescribed` keeps the frozen tolerance of 0.01, so for (2, 4, 2) it never expands. It is the consistency anchor for Stage 2.
  - `forced` overrides the tolerance to 1.0 in the measurement request, so expansion always runs to `expanded_panels`.
- **Repeats:** 5 sequential timed fresh-process repeats per arm per runner, on **2 independent runner jobs**: 10 per arm. Each arm also has one instrumented call-count repeat, which runs **after** its five timed repeats and is excluded from the statistics.
- **The cold repeat.** A real worker always starts cold. In the 2026-09-24 record the cold first repeat was the dominant wall outlier (25.24 s against 14.64 s and 15.20 s, 2026-09-24 note §3). So:
  - **Timed repeat 1 of each arm is the cold one, and it is included in the maximum.** Immediately before it, the job deletes the checkout's `__pycache__` directories and drops the page cache (`sync; echo 3 > /proc/sys/vm/drop_caches`). The first repeat therefore reads source and compiles bytecode, and so bounds a worker whose image carries no compiled bytecode.
  - **The arm order alternates between jobs.** Job `a` runs `forced` first and job `b` runs `prescribed` first. The forced arm, which sets every ceiling input, then also runs first on a fresh runner in job `a`.
  - The instrumented repeat never runs first, so it cannot absorb the cold start.
  - On Windows (Stage 1a) the page cache is not dropped; its repeat 1 is only as cold as the host allows. Stage 1a validates the harness and sets no value.
- **Statistic for the ceiling:** the maximum over all valid timed repeats, cold repeats included: Ĉ for workload CPU (§3.1), Ŵ for workload wall, M̂ for memory. The median, minimum and spread (max ÷ min) are reported too, with and without the cold repeats.
- **Determinism:** the workload is deterministic. The root is fixed and unsalted (`tb-s2-rng-v2`, `regime.py:22`); the fixture keys change per run, but the seeds do not.
  - Every repeat of an arm must produce identical artifact digests.
  - The forced arm's first `initial_panels` panels must be byte-identical to the prescribed arm's result.
  - **Any mismatch invalidates the measurement and is returned to the coordinator.** ~~It would also be evidence against D3's R7 reproducibility assumption.~~ *Correction 2026-09-26 (PR #519 review, round 2):* a mismatch bears on D3's R7 reproducibility assumption only after diagnosis rules out harness, host and instrumentation causes, such as a nondeterministic serialization field (§5, Invalid row).
- **Noise:**
  - A job whose CPU spread over its **warm** timed repeats (2–5) exceeds **1.30 (PROPOSED)** is invalid and is re-run once on a fresh runner. If it fails again, the measurement returns to the coordinator without a ceiling. The cold repeat is a deliberate treatment, not noise, so it is kept out of the spread test; its ratio to the warm median is recorded, and it still enters the maximum.
  - A between-job ratio of medians above 1.30 is recorded as host variance. Ĉ remains the maximum, and the application entry flags it.

### 3.3 Harness (to be written; specified here)

The harness is `measure_part_a_max.py`, kept as `.py.txt` beside its record under the 2026-09-24 convention, so the import-boundary gate does not treat it as a module. It reuses the 2026-09-24 harness's fixture setup and `benchmark_part_a.py`'s output conventions. Each repeat runs in a fresh `sys.executable` subprocess:

0. At harness entry, before importing any fixture module, read the CPU and wall boundary clocks (§3.1, `start`).
1. `setup = build_verified_composition(tmp, confirmation_depth=60, decision_alpha='0.05')`, the trading variant (`idle=False`). Depth 60 is the Linux fixture default (`composition_fixture.py:180`); Part A does not depend on it. Read the boundary clocks before and after; the single `_build_composition` wrapper separates `admission` from `setup_excluded` and is removed before step 2.
2. `setup.source.verify_for(setup.contract)` once, the same shape as `compute.py:28`. Read the boundary clocks before and after (`verify`).
3. Build the request exactly as `production._part_a_request` does (`production.py:89-96`), with two exceptions: `within_pp` takes the arm's tolerance, and `budget_seconds = 3600`, so the in-engine predicate never aborts the measurement. `predicted_seconds` is still recorded.
4. `_run_part_a(request, source.sessions, adjacent=source.adjacent, covered_until=source.covered_until, tail_covered=source.tail_covered, proof_provider=source.proof, replay_provider=source.replay, initial_state=compute.initial_state(contract), full_pass_rate=1.0, synthetic=True)`. `full_pass_rate` affects only the final sanity decision, not the compute. Read the boundary clocks immediately before and after this call only (`part_a`). The N2 baseline derivation is not in this harness: its code does not exist before the S5 build. It is part of D̂, uncovered until Stage 1c (§3.4).
5. Serialize the initial prefix and the final panels canonically (sorted-key compact JSON of `asdict`), with boundary reads before and after (`serialize`). This stands in for the S5-D1 artifact format, which does not exist yet; Stage 1c replaces it with the built adapter's two artifacts and their fsync.
6. Assert the panel count (forced: 4; prescribed: 2), call `production._peak_memory_bytes()`, and write one JSON row.

It never calls `_run_composition_e1`, `run_production_e1`, `_execute_e1` or `ProductionExecutor`. Its output class is `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.

### 3.4 Exact commands (proposed steps; none is run by this proposal)

**Stage 0 (~~approval needed: an artifact download~~; corrected 2026-09-26: download approved and done, read step pending). Existing Linux evidence, no new run.**
```bash
gh run download 36180568493 -n qualification-s2-supervision -D <scratch>/s4-36180568493
gh run download 36181780676 -n qualification-s2-supervision -D <scratch>/s4-36181780676
grep -hE "Consumed .* CPU time|memory peak" <scratch>/s4-*/journal.log <scratch>/s4-*/systemd-units.log
```
Output: the Linux N1 and N2 payload and guardian CPU, if logged, paired with the Windows 13.36 s and 211.39 s. **Stage 0 is calibration and orientation only, and it can set no ceiling.** It reads the journals of two existing runs: one sample per stage per run, with no repeat design, no spread check and no digest check. By PA-4 and §6 step 7 a ceiling cannot come from it. It informs §0 finding 5 and the choice in decision 3. It does not supply the `/v7` N2 value.

*Correction 2026-09-26 (PR #519 review; Stage 0 status):* the download half of Stage 0 is done. The operator approved it on 2026-09-26, and both artifacts are preserved in the primary checkout (§2 correction), so the two `gh run download` lines are spent. The read step (the `grep` line) has not run. It remains Stage 0 work under the measurement rule once that rule is approved, and it runs against the preserved copies, with its paths adjusted to their layout.

**Stage 1a. Windows development pass (harness validation only; not the ceiling basis).**
```powershell
.\fp.ps1 doctor
.\fp.ps1 python docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py --arm forced --arm prescribed --repeats 5 --out docs/notes/<date>-s5-part-a-measurement/windows.json
```
On Windows the harness uses the accounting path of §3.1: `time.process_time()` at the boundaries, a job object per repeat process for the whole-process CPU, and `PeakWorkingSetSize` through `production._peak_memory_bytes()`. It never imports `resource`. The instrumented repeat runs last in each arm. The output is marked `platform_accounting = windows_process_time_job_object` and is not comparable to Linux figures.

**Stage 1b (approval needed: a Linux host dispatch). The reference measurement.**
It runs as a `workflow_dispatch`-only job on `ubuntu-24.04`:
- The host environment is provisioned exactly as the S2 workflow's setup steps provision `$host_root/env`.
- It uses no qualification service and no secrets, and uploads only the JSON.
- It needs a new workflow file, a CI configuration change with its own authorization.
- It runs as 2 jobs (matrix `job: [a, b]`), with `ARM_ORDER="forced prescribed"` in job `a` and `ARM_ORDER="prescribed forced"` in job `b` (§3.2).

Per job:
```bash
for arm in $ARM_ORDER; do
  for r in 1 2 3 4 5 0; do   # r=1 is the cold repeat, timed and included; r=0 is the instrumented call-count repeat, run last and excluded
    if [ "$r" = 1 ]; then    # make the arm's first timed repeat cold
      find "$PWD" -name __pycache__ -type d -prune -exec rm -rf {} +
      sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
    fi
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
Dry-run first, with one repeat per arm, to confirm that `CPUUsageNSec` and `MemoryPeak` are populated for an exited `RemainAfterExit` unit on systemd 255. If they are not, fall back to the unit's `Consumed … CPU time` journal line and the primary `getrusage` values. The launcher's own overhead falls inside the unit, so it is charged conservatively. *Correction 2026-09-26 (PR #519 review, F2):* that fallback serves CPU only. For memory the only fallback is another reading of the same cgroup aggregate (§3.1 correction). If none is populated, memory stays **UNVERIFIED**.

**Stage 1b-N2 (only if decision 3 chooses to apply the rule to N2; approval as for Stage 1b).** A third arm, `n2`, on the same two jobs, with the same repeat design, cold repeat, validity checks (§3.2) and record schema. Its step 4 runs the N2 compute as `compute._run_checkpoint_compute('n2', …)` does (`compute.py:24-44`): `stage_request(contract, 'n2', 3600)`, a `_ReplayProvider` over the source, and `_run_stage`, with a budget object that measures but never aborts. Only a valid record from this arm can set `/v7`'s N2 ceiling under the rule (§6 step 1). Stage 0 cannot.

**Stage 1c (at S5 packet Checkpoint C3, before any acceptance-grade run relies on the ceiling; a Linux dispatch, approved as for Stage 1b).** It measures D̂. The Stage 1b job is re-run against the built S5 adapter. Steps 4–5 are replaced by the adapter's Part A compute inside the same workload boundaries: the N2 FULL baseline derivation from staged N2 capture bytes (the S5 executor supplies the staged-capture fixture its adapter tests use), `_run_part_a`, and ~~the two S5-D1 artifacts with their fsync~~ *(corrected 2026-09-26, round 2, F1a: the construction of the two S5-D1 documents as byte strings; their writing and fsync are worker-side, R̂, below)*. ~~Its forced-arm maximum, Ĉ₁c, covers the whole §1 workload and replaces `Ĉ + D̂` in PA-1 (§4).~~ Until Stage 1c has a valid record, the application is **provisional** (§6).

**Correction 2026-09-26 (PR #519 review, F1): the forced arm has no mechanism through the real adapter at this head.** Stage 1b forces expansion by building the engine request itself (§3.3 step 3). Stage 1c calls the adapter instead, and that route cannot be forced today:
- **The adapter does not exist yet.** `execution/compute.py` defines only the N1 and N2 computes (`compute.py:24-55`). S5 packet §1 specifies `compute.run_part_a_compute(contract, source, budget, *, n2_full_outcomes)`, which has no tolerance input.
- **The tolerance comes from the signed contract.** The only existing request mapping, `production._part_a_request`, reads it from `contract.replay.part_a` (`production.py:89-96`), and the packet's interface gives the adapter no other source. The validator pins it to 0.01 for every domain (`contract.py:765-773`), and the source refuses any contract object other than the one it was issued for (`production_source.py:855-858`). A measurement therefore cannot supply a different contract.

No measurement-only injection point exists without a change. The proposed mechanism is **Stage 1c-prep**, which needs its own approval (decision 4):
1. **A structural requirement on the S5 build.** This is a change to the S5 packet text, folded in at the RC-6 re-anchoring. `run_part_a_compute` builds its engine request only through one module-level function in `execution/compute.py`, looked up at call time, as `_run_checkpoint_compute` already does with `stage_request` (`compute.py:14-21`, `:41`). The adapter reads the expansion tolerance nowhere else and takes the expansion decision from the engine result (`PartAResult.expanded`, `part_a.py:79`, `:209`). The requirement adds no parameter, flag, environment variable or configuration input, and it leaves the signed route's behavior unchanged.
   *Correction 2026-09-26 (PR #519 review, round 2, F1a): where the expansion is judged against the signed contract.* The packet requires the Part A operation to "Reject omitted or unnecessary expansion" (S5 packet §3, line 38). It puts `expansion_required` and `tolerance_comparison` in the PART_A assessment field set (packet §1, line 30), and `expansion_required` and "the inclusive-tolerance comparison inputs" in the capture (S5-D1, line 20). It does not fix where any of these is computed or enforced. A forced run is an unnecessary expansion by construction, so the requirement also pins:
   - Inside `run_part_a_compute`, `expansion_required` and the tolerance-comparison inputs, if the adapter computes them, come only from the request that function returns and from the engine result (`PartAResult.expanded`). The adapter makes no comparison against the signed contract's tolerance. That is how "reads the expansion tolerance nowhere else" holds alongside the recorded comparison.
   - The packet's rejection of an omitted or unnecessary expansion is enforced outside `run_part_a_compute`. It runs in G5, which reconstructs the expansion decision (packet §1, line 29; §3 checklist, line 48: "independent G5 reconstruction; the five rejections"), or in worker-side validation after the adapter has returned both documents. The packet does not place the rejection in the adapter, so pinning it outside the adapter leaves the signed route's behavior unchanged: the route still rejects an unnecessary expansion.
   - On the forced run, the packet's assertion `actual_panel_count == (expanded_panels if expansion_required else initial_panels)` (line 42) then holds, because `expansion_required` comes from the substituted request.
   - If the S5 executor cannot meet this without moving a packet-required check into the adapter, Stage 1c-prep is unavailable. The route is then the fixture alternative or an operator ruling (below).
   *Round 2, missing seam:* before Stage 1c-prep is approved, a build without this seam is a blocked measurement. After it is approved and folded into the packet at RC-6, a build without the seam fails the packet: a C3 nonconformance returned to the S5 executor, with the ceiling provisional meanwhile (§5).
2. **The substitution lives only in the Stage 1c harness.** In its own subprocess, the harness replaces that function with a wrapper that calls the original and returns the request with `within_pp = 1.0` and `budget_seconds = 3600`, as Stage 1b step 3 does. Everything else runs in the real adapter: the N2 FULL baseline derivation from the staged capture bytes, `_run_part_a` through all four panels, and ~~both S5-D1 artifacts with their fsync~~ *(corrected 2026-09-26, round 2, F1a: the construction of both S5-D1 documents as the byte strings the adapter returns, packet §1, line 27; the writing and fsync are worker-side, R̂, below)*. The harness passes a budget object that measures but never aborts, as Stage 1b-N2 does. The substitution is not placed in `part_a.py`: that module is a retained runtime code role (`trust_domain.py:143`), which the frozen adjudicator's module walk checks against retained source (`result_adjudication.py:148-195`). The 2026-09-24 harness removed its wrappers before that walk for this reason (`measure_composition.py.txt:68-70`).
3. **It stays outside production and signed acceptance.**
   - The harness is a `.py.txt` beside its record. No product code imports it, and pytest does not collect it.
   - It runs only in the `workflow_dispatch` measurement job. It never runs through `worker.main`, the guardian, the qualification service, G5 or the adjudicator.
   - It writes no custody row, receipt or checkpoint. Its output class is `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.
   - The prescribed arm runs the unmodified adapter. Forced-arm artifacts are never compared with, or substituted for, signed-route evidence; PA-5 uses the prescribed arm.
   - The S5 packet's prohibition of a relaxed tolerance (packet §6) still binds the product.
4. ~~**A refused forced run is a failed measurement.** If the built adapter refuses the forced run (for example because it re-derives the decision from the contract), the forced arm is **invalid** (§5 correction).~~ The step returns to the coordinator; the adapter is not weakened to admit it.
   *Correction 2026-09-26 (PR #519 review, round 2, F1a): a refusal is classified by its cause* (§5):
   - The build conforms to the approved Stage 1c-prep requirement, and the refusal still follows a packet rule, for example the §3 rejection of an unnecessary expansion. The requirement has then proved incompatible with the packet, so the mechanism is unavailable. That is **Blocked**, not a measurement defect.
   - The build does not conform: for example, it enforces that rejection, or re-derives the decision from the contract, inside the adapter. That is a **C3 nonconformance**, returned to the S5 executor under the packet. The ceiling stays provisional meanwhile.
   - Only a refusal that cannot be traced to a packet rule or to the requirement is **Invalid** and investigated.

With Stage 1c-prep approved and a valid record, the Stage 1c forced-arm maximum, Ĉ₁c, ~~covers the whole §1 workload and replaces `Ĉ + D̂` in PA-1 (§4)~~ *(corrected 2026-09-26, round 2, F1a: covers the §1 workload up to the adapter's return of both documents, and replaces `Ĉ + D̂` in PA-1 (§4) except for the worker-side residual R̂, below)*. The §3.2 prefix check then compares panel records, not whole artifacts, because the forced artifacts may record the substituted tolerance.

**Correction 2026-09-26 (PR #519 review, round 2, F1a): the worker-side result path is a named residual, R̂.** `run_part_a_compute` returns the initial-prefix and final documents as byte strings (S5 packet §1, line 27). In the existing compute/worker split, everything after the compute belongs to the worker. `run_worker` calls `encode_worker_result`, the self-validating `parse_worker_result`, two `encode_frame` passes and the budget re-measurement (`worker.py:69-94`). `main` then writes the output-mount file and calls `os.fsync` (`worker.py:140-150`). The Stage 1c harness calls none of them. So:
- **R̂ is the CPU of the worker-side result path at maximum expansion, and it is uncovered.** Ĉ₁c does not cover the whole §1 workload. After Stage 1c, PA-1 is `B = max(m_c × Ĉ₁c, 1.5 × P̂₁c)`, and the application entry names R̂ as uncovered.
- At the prescribed size, R̂'s work falls inside Stage 2's service figure, so PA-5 checks it there, at 2 panels, not 4.
- **Driving the worker path was considered and not chosen.** The harness could call `run_worker(..., checkpoint='PART_A')` on an input directory staged the way the S5 worker tests stage one. The N2 case already does this: `joint_stage_input`, `test_worker.py:132-158`, then `run_worker`, `:168-170`. The harness could then copy `main`'s write and fsync. But `parse_worker_result` checks the result against the plan's depths and seed inventory (`evidence.py:186-195`, `:46-69`, `:224`). Whether a forced four-panel result passes depends on how the S5 PART_A plan enumerates panels, and that plan does not exist before the build. If the result does not pass, the harness would have to bypass a product check, which this proposal does not do. At C3, once the plan exists, the coordinator may revisit this route as a separately approved amendment.
- **An operator decision is needed before an acceptance-grade run relies on an application with R̂ named and uncovered** (§8, decision 4). Until the operator rules, the application stays provisional (§6 step 6).
- The S5 build may place the initial-prefix write inside the adapter call. S5-D1 (line 20) has the worker write that file "before deciding expansion", which the §1 interface, returning both documents, does not show. In that case the harness supplies a temporary output directory, the write falls inside Ĉ₁c, and R̂ excludes it.

**Alternative, not chosen: an expansion-capable fixture.** A TEST_ONLY workload policy with at least 17 paths per panel (§0 finding 1), and a synthetic source whose lower initial panel lands at 16 of 17 passes, would let the unmodified adapter expand. It is a different workload:
- At 17 paths per panel, maximum expansion is 2 + 4 × 18 = 74 replays (75 `verify_for` calls), against 14 (15). The budget binding paths become 34 and 68, against 4 and 8 (`contract.py:793-794` computes them as panels × depth).
- It needs a new trust-domain workload policy and fixture (the S5 file list includes installed fixtures, packet §2).
- It is unestablished that a synthetic source can hit that pass rate. S5 packet §4 already hedges the prescribed-expansion case: "if a synthetic source can produce it economically".
- Its maximum could bound the (2, 4, 2) workload only unscaled, because per-call cost is not shown to scale linearly (§0 finding 3).
- *Round 2 (2026-09-26, F2a):* if its synthetic source does expand, the genuine campaign expands too. Stage 2's parent peak would then cover the shared footprint at maximum expansion directly (PA-3b, §4), without the composition's assumption.

**If neither is approved,** D̂ stays uncovered for the whole route. Every application stays provisional (PA-1), and no acceptance-grade run at C3 may rely on it (§6 step 6), so S5 cannot reach acceptance on that ceiling. That is a **blocked** measurement (§5 correction), not a falsifier trigger. Because the Stage 1c-prep requirement constrains the S5 build, it has to be decided before release, at the RC-6 re-anchoring.

**Stage 2 (at S5 packet Checkpoint C3; no new authority). Service-route confirmation.**
- The genuine S5 Linux campaign's PART_A work supplies its settled observation from the retained budget snapshot: `cpu_ns`, `memory_peak_bytes`, `oom_events`, and the boottime difference from the reservation clock to `CAPTURED`.
- Proposed C3 requirement on the S5 executor: export those fields in the run evidence, read with `scripts/s2_run_evidence.py <run> --expect-head <sha>`. Where the evidence separates the payload's CPU from the guardian's, export both.
- The genuine campaign never expands (§0 finding 1), so Stage 2 checks the service route against the Stage 1c **prescribed** arm's workload CPU (setup excluded) under PA-5. This is the like-for-like comparison: both sides then include the derivation and the real artifacts.
- *Correction 2026-09-26 (PR #519 review, round 2):* two qualifications apply.
  - **Memory (F2a).** Stage 2's `memory_peak_bytes` is the host-run parent's `memory.peak` (`campaign_supervisor.py:974`). It is the only memory aggregate in this proposal that covers the host-run scope, and PA-3b checks it (§4).
  - **Worker-side work (F1a).** On the harness side, the prescribed arm stops at the adapter's return, so the worker-side result path (R̂) is on the service side only. Like k's orchestration residual, that errs toward re-measurement.

### 3.5 Evidence record

The record lives in `docs/notes/<date>-s5-part-a-measurement/`: the harness `.py.txt`, `windows.json`, the Linux job JSON and `.unit` files, `cpu.txt`, and a short note. The JSON schema is `s5-part-a-max-expansion-measurement/v1`:

```text
schema, artifact_class = TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING, decision_bearing = false,
recorded_utc, measured_commit, tree_clean, harness_sha256, source_sha256{path: sha},
stage = 1a | 1b | 1b-N2 | 1c,
runtime{runtime_kind = host_venv | worker_image, os_id, os_release, kernel, arch, cpu_model, logical_cpus,
        implementation, python, executable_sha256, requirements_lock_sha256, thread_env,
        image_digest (required when worker_image, else null), platform_accounting, runner, run_id, job, arm_order},
workload{fixture, idle=false, sessions, bars_per_session_per_leg, legs, outer_months, inner_block_sessions,
         horizon_sessions, initial_panels, expanded_panels, paths_per_panel, root_rng_namespace, recipe,
         arm, within_pp, full_pass_rate_input=1.0, expected{replays, verify_for}},
repeats[{repeat, cold, instrumented,
         cpu{start, admission, setup_excluded, verify, part_a, serialize, workload, process_total}, unit_cpu_s|null,
         unit_cpu_workload_s|null, wall{outer, setup_excluded, workload, part_a},
         peak_memory_bytes, memory_method, unit_memory_peak_bytes|null, panels, expanded, probe_seconds,
         predicted_seconds, elapsed_seconds, counts{replay, proof, verify_for}|null,
         initial_prefix_sha256, final_sha256, exit_code}],
summary{per arm: workload cpu/wall and memory max, median, min; warm spread; cold ÷ warm median;
        digests_identical; prefix_matches_prescribed},
validity{ok, reasons[]}
```

*Correction 2026-09-26 (PR #519 review, F2):* each repeat also records `memory_coverage`, either `cgroup_aggregate` or `process_only`. The summary records M̂ only when every timed forced-arm repeat is `cgroup_aggregate`; otherwise it records `memory_feasibility = UNVERIFIED` and no M̂. *(F1):* a Stage 1c record also names the substituted function by module and name (§3.4 Stage 1c-prep); `harness_sha256` already covers the wrapper.

*Correction 2026-09-26 (PR #519 review, round 2):* `cgroup_aggregate` means the harness unit's cgroup, so the summary labels M̂ `memory_scope = payload_unit` (F2a). Shared-scope memory is not in this record; it comes from Stage 2's run evidence (PA-3b). A Stage 1c summary also lists `uncovered = [R̂]`, the worker-side result path (F1a, §3.4).

## 4. Proposed margin rule (every parameter PROPOSED, not approved)

**Symbols:**
- Ĉ, Ŵ and M̂ are the forced-arm maxima (§3.2) over timed repeats, cold repeats included. Ĉ and Ŵ are **workload** values: setup is excluded (§3.1).
- D̂ is the CPU of the N2 FULL baseline derivation plus the real S5-D1 artifact writing, beyond the stand-in serialization. It is **uncovered** until Stage 1c measures it. Stage 1c's forced-arm maximum Ĉ₁c then replaces `Ĉ + D̂` (§3.4).
- *Added 2026-09-26 (PR #519 review, round 2):*
  - R̂ is the CPU of the worker-side result path at maximum expansion: encode, validate, frame, output write and fsync (§3.4). It is **uncovered**, and Ĉ₁c does not replace it.
  - M̂ is a payload-unit aggregate (§3.1). P₂ is Stage 2's settled PART_A `memory_peak_bytes`, from the host-run parent cgroup. M̂ₚ is the prescribed-arm maximum of the same unit aggregate.
- P̂ is the forced-arm maximum of `predicted_seconds`.
- O is the phase's installed orchestration charge (20 s diagnostic, `profile.py:212`).
- L is a launch allowance for the time from reservation to payload start.
- Ceilings round **up** to whole 10 s.

| Rule | Formula | PROPOSED parameter |
|---|---|---|
| **PA-1 CPU** | `B = max(m_c × (Ĉ + D̂), 1.5 × P̂)` (payload); `cpu_ns(PART_A) = max(shared, B + O)`. **Before Stage 1c**, D̂ is uncovered: the value computed from Stage 1b is applied as **provisional**, the application entry names the N2 baseline derivation and the real artifact writing as uncovered, and no acceptance-grade run relies on a provisional ceiling. **After Stage 1c**, `B = max(m_c × Ĉ₁c, 1.5 × P̂₁c)` from the Stage 1c record | m_c = **2.0**; shared = 120 s |
| **PA-2 wall** | `wall_ns(PART_A) = max(shared, m_w × (Ŵ + L))`, subject to m_w ≥ m_c ÷ (m_c − 1). Ŵ comes from Stage 1c once that exists, under the same provisional rule as PA-1 | m_w = **3.0**; L = **30 s** until Stage 2 measures it; shared = 300 s |
| **PA-2b engine predicate** | Check `P̂ × wall ÷ B ≤ wall ÷ 1.5`: the engine's throttled prediction must use at most two-thirds of the window. The `1.5 × P̂` term in PA-1 guarantees it | — |
| **PA-3 memory** | Check `m_m × M̂ ≤ profile memory_bytes` (256,000,000 in `deploy/qualification/test-profile.json`). Memory is one shared campaign footprint (spec §2.5), so this rule never sets a per-phase value; a failure goes to an operator ruling. *Corrected 2026-09-26 (F2):* evaluated only when M̂ comes from aggregate evidence (§3.1 correction). Otherwise memory feasibility is **UNVERIFIED**, PA-3 is not evaluated, and RC-3 stays open. *Corrected 2026-09-26 (round 2, F2a):* this check is now **PA-3a, payload**. It establishes feasibility only against the payload container's own `Memory` limit (`campaign_supervisor.py:2592-2593`), not against the shared host-run limit (`:830`); see PA-3b | m_m = **1.5** |
| **PA-3b memory, shared** *(added 2026-09-26, round 2, F2a)* | Check `m_m × P₂ ≤ profile memory_bytes`, where P₂ is Stage 2's settled PART_A `memory_peak_bytes` from the host-run parent cgroup (`:974`), a high-water mark never reset per work (`:804`). Until this is evaluated at C3, memory feasibility against the shared limit is **UNVERIFIED**. Stage 2 never expands (§0 finding 1), so P₂ covers the prescribed workload only. For maximum expansion, a proposed composition is `m_m × (P₂ + max(0, M̂ − M̂ₚ)) ≤ memory_bytes`, with M̂ and M̂ₚ from the same Stage 1c record. It assumes that expansion raises the shared peak by no more than it raises the payload unit's peak. That assumption is unmeasured and goes to the operator (decision 7). A failure goes to an operator ruling, as for PA-3a | m_m = **1.5** |
| **PA-4 validity** | No ceiling is derived from a measurement that fails §3.2 (digests, prefix, spread). *Corrected 2026-09-26 (F2):* no memory conclusion is drawn from incomplete memory accounting. M̂ needs aggregate evidence on every timed forced-arm repeat; a process-only value can neither pass nor fail PA-3 | spread 1.30 |
| **PA-5 Stage-2 consistency** | Compare like with like. `k = service ÷ harness`, where:<br>– *service* is the Stage 2 PART_A payload CPU when the evidence separates it from the guardian's, else the whole settled charge with nothing deducted;<br>– *harness* is the Stage 1c prescribed-arm maximum of workload CPU (setup excluded; derivation and real artifacts included).<br>If k > **1.25**, re-apply PA-1/PA-2 with Ĉ₁c × k and Ŵ × k and record a new application. Orchestration left in the service figure raises k, so that residual errs toward re-measurement. The host-to-container factor (§2) also sits in k, in an unknown direction | 1.25 |

*Correction 2026-09-26 (PR #519 review, F1):* "after Stage 1c" in PA-1 and "Ŵ from Stage 1c" in PA-2 mean a valid Stage 1c **forced** arm. That arm needs Stage 1c-prep (§3.4). Without it, PA-1 and PA-2 stay on the provisional Stage 1b values with D̂ uncovered. *Round 2:* the same applies to PA-5, because `Ĉ₁c × k` exists only with a valid forced arm. Without one, a k > 1.25 re-application scales the provisional Stage 1b inputs (`Ĉ × k`, `Ŵ × k`), stays provisional, and leaves D̂ uncovered. With one, R̂ stays named as uncovered (§3.4).

**Why these values.**
- *The kernel couples wall and CPU.*
  - The payload's quota is `(cpu_ns − O) ÷ remaining_wall` (`campaign_supervisor.py:177-194`).
  - A throttled payload of CPU C finishes its CPU-bound part in `C × wall ÷ B`. At C = Ĉ that is `wall ÷ m_c`, whatever the wall ceiling.
  - The non-CPU time plus launch then needs `wall × (1 − 1/m_c)`, hence m_w ≥ m_c ÷ (m_c − 1) = 2. The value 3 adds headroom for launch and queue noise.
- *The noise seen so far.* In the 2026-09-24 records:
  - CPU spread within a depth was 1.04–1.08.
  - The Part A subprocess wall ranged 14.64–25.24 s (1.72, with a cold first repeat; §3.2 now keeps a cold repeat in every arm).
  - The internal total ranged 12.47–17.61 s (1.41).
  - Host-to-host variance is unmeasured; the two-job design measures it. m_c = 2 covers the worst observed band.
- *Cost asymmetry.* A ceiling that is too tight means a silent SIGKILL at the deadline, an IN_DOUBT terminal campaign and a blind Linux re-run (a full S4 run took 2,717 s). A ceiling that is too loose costs only Σ headroom, and the TEST_ONLY cap leaves about 8,300 s of it (§5).
- *Precedent.* The M13 ruling gave N2 a 340 s payload against 211 s measured on Windows, a factor of 1.61, without any Linux figure.
- *The shared floor.* Never going below the shared 120 s / 300 s keeps one rule for the other phases, as the N2 precedent does.

**Sensitivity (m_c = 2, O = 20 s).** The shared 120 s CPU suffices while Ĉ + D̂ ≤ 50 s and P̂ ≤ 66 s. The shared 300 s wall suffices while Ŵ + L ≤ 100 s.

| Ĉ + D̂ (s) | 25 (estimate §1, D̂ excluded) | 50 | 60 | 100 | 211 (N2-sized, hypothetical) |
|---|---|---|---|---|---|
| PART_A CPU ceiling (s) | 120 (shared) | 120 | 140 | 220 | 450 |

The Ĉ + D̂ threshold for the shared ceiling moves with m_c: 66.7 s at m_c = 1.5, 50 s at 2, 40 s at 2.5 and 33.3 s at 3.

**Re-measurement triggers.** Any one of these invalidates the application for the next release or profile, which needs a fresh attempt anyway under contract decision 4:
1. A change to the worker runtime closure digest or to `requirements-ops.lock`. That includes `part_a.py`, `regime.py`, `paths.py`, `replay.py`, `provider.py`, `production_source.py` (in particular any N4 change to `verify_for`), `runner.evaluate_replay` and the S5 adapter.
2. A workload change: panels, paths per panel, horizon, outer months, inner block, fixture source size or legs.
3. A reference-runtime change: `host.json` pins, the worker base tag, or the runner class.
4. A change to the orchestration charge or to `CAMPAIGN_RESOURCE_SCOPE`.
5. Any Linux PART_A run whose settled charge exceeds 0.8 × B or whose wall exceeds 0.8 × the ceiling, and any PART_A overrun or OOM.
6. A Stage-2 factor k > 1.25 (PA-5).

**Scope choice for the operator (decision 2, §8):** approve the rule for PART_A only, or phase-generically for TEST_ONLY diagnostic ceilings. The phase-generic form would let the coordinator set `/v7`'s N2 ceiling under the rule, instead of the operator extending the "/v6 only" M13 ruling, but **only from a §3-conformant N2 measurement** (Stage 1b-N2, §3.4): the §3.2 repeats, cold repeat and validity checks, and a record with `validity.ok = true`. Stage 0's journal figures are two samples with no repeat design, spread check or digest check. By PA-4 they cannot set a ceiling. Without Stage 1b-N2, the only way to set `/v7`'s N2 ceiling is an operator ruling extending M13.

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
- **TEST_ONLY: open, not ruled out.** The falsifier has two limbs. The Σ limb looks clear: the workload is fixed (14 replays) and deterministic (fixed root and source), and every row of the table above leaves room orders of magnitude beyond the §1 estimate. The measurement limb is **open**: no maximum-expansion measurement exists (§0 finding 2), and the only route to one, Stage 1b, needs its own approval (decision 4). The falsifier stays open until a valid Stage 1b record exists. ~~It is **triggered** for S5 if any of these happens:~~
  1. ~~Stage 1 cannot produce a valid measurement (§3.2 fails twice).~~
  2. ~~The digests differ across repeats.~~
  3. ~~Stage 1b is not approved, or cannot run before S5 is released, unless the operator instead sets the PART_A ceiling by ruling.~~ RC-3 allows the ceiling to be set "by operator ruling" (decision draft line 378), as the M13 ruling did for N2. But RC-3 as drafted still asks for a measured envelope with a cited record, so a ruling without a measurement would also amend RC-3. Whether such a ruling answers the falsifier is the operator's decision.

  **Correction 2026-09-26 (PR #519 review, F3): three different outcomes, only one of which is the falsifier.** The struck list treated missing permission and a failed measurement as evidence against the accounting design. They are not. The draft states the falsifier as a ceiling that "either fails the Σ-feasibility check against any admissible cap or cannot be measured before S5 is released" (decision draft line 228). RC-3 requires the measured envelope before release (line 378). A measurement that has not happened therefore keeps S5 held; it cannot release S5 unmeasured. "Cannot be measured" is read here as evidence that no valid bound can be obtained, not as an absent approval or run.

  | Outcome | What it establishes | Consequence |
  |---|---|---|
  | **Blocked.** Stage 1b, Stage 1c-prep or Stage 1c is not approved; the job cannot be dispatched; ~~or the S5 build lacks the §3.4 Stage 1c-prep seam~~. *Round 2 (2026-09-26):* also blocked: an S5 build that lacks the Stage 1c-prep seam while Stage 1c-prep is unapproved; a refusal of the forced run by a build that conforms to the approved requirement, because the requirement has proved incompatible with the packet (§3.4 Stage 1c-prep item 4); and, for RC-3's memory item only, a missing aggregate memory reading (memory UNVERIFIED, §3.1). *After* Stage 1c-prep is approved into the packet (RC-6), a build without the seam, or one that refuses because it enforces the packet's expansion check inside the adapter, is not blocked. It is a **C3 build defect**, returned to the S5 executor under the packet, with the ceiling provisional meanwhile | Missing permission or evidence | **Before release: retain the S5 hold**, and RC-3 stays open. **At C3** (Stage 1c): the ceiling stays provisional, and no acceptance-grade run relies on it (§6 step 6). Either way the falsifier is **not** triggered. An operator ruling that sets the ceiling without a measurement would also amend RC-3 (above); whether it answers the falsifier is the operator's decision |
  | **Invalid.** A run fails §3.2 or PA-4: the warm spread fails twice, digests differ across repeats, the prefix differs, ~~required accounting fields are absent, or the adapter refuses the forced run~~ *(round 2, 2026-09-26:* a CPU or wall accounting field is absent: the boundary CPU and wall reads, the whole-process CPU total, the unit's `CPUUsageNSec` or its journal fallback (§3.4 Stage 1b), the unit's start and exit timestamps, the engine facts, the digests or the exit code; or the adapter refuses the forced run for a cause not traceable to a packet rule or to Stage 1c-prep. A missing aggregate memory reading does **not** make a run Invalid: CPU and wall still apply, and memory is UNVERIFIED, which is Blocked for RC-3's memory item) | A measurement or reproducibility defect | **Investigate the failure:** harness, host, instrumentation or engine nondeterminism. Re-measure after diagnosis; S5 stays held meanwhile. A digest mismatch is a reproducibility defect that needs diagnosis, ~~and it bears on D3's R7 assumption (§3.2)~~ *(round 2: it bears on D3's R7 assumption only once diagnosis has ruled out harness, host and instrumentation causes, §3.2)*. By itself it says nothing about per-phase accounting |
  | **Bound cannot be established.** Either a valid record whose rule-derived PART_A ceiling fails Σ-feasibility against every admissible cap (the draft's first limb; the TEST_ONLY cap is 10,000 s, §5), or a diagnosis that traces an invalid run to the workload itself: repeats of the fixed, deterministic workload do not stay within any stated bound once harness, host and instrumentation causes are excluded | Evidence against bounding maximum-expansion CPU ahead of time | **Return the accounting-design question** (the uniform-model revisit, decision draft line 228) to the operator through the coordinator |

  *Correction 2026-09-26 (PR #519 review, round 2): the reading of "cannot be measured" goes to the operator.* The reading above departs from the literal draft wording, which includes "or cannot be measured before S5 is released" (decision draft line 228). That wording is the draft's recommendation, not ruling text. The D2 ruling words are only "Retain per-phase accounting." (execution-slices plan line 806), and the owner-text form of the rest of the draft's D1–D3 text is reviewed under RC-2 (plan line 804). This note therefore does not settle what the falsifier means. The reading is put to the operator as decision 6 (§8) and named for the RC-2 owner-text review of draft §2.3. Until the operator rules, the table above is the coordinator's proposed classification.
- **Production: out of scope, flagged.** Counts are fixed: 40,203 `verify_for` calls at the freeze candidate's 200 paths per panel (§1; not frozen). The per-call cost is not shown to be content-independent. It grows with source size (about 3.2 ms per session plus 0.23 ms per bar, 2026-09-24 note §2) and, on the fixture, rose from 1.02–1.05 s at depth 2 to 1.08–1.16 s at depth 30 for an unidentified reason (§0 finding 3). The CPU is boundable only if that growth over a 40,203-call run is bounded, and that is not established. Its size is a further question. The 2026-09-24 linear extrapolation of about 89 s per call would put Part A's re-verification alone near 994 h; that is an extrapolation, not a measurement. Whether it fits any admissible production cap is a question for the production budget owner and for N4.

## 6. TEST_ONLY application procedure (after approval only)

1. **Preconditions:**
   - an operator ruling approving the rule, with any amended parameters, recorded as a dated entry under the S5 ledger entries of the execution-slices plan; *operator ruling 2026-09-26 (in session; [ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26)): the approval is conditional, for PART_A TEST_ONLY measurement only, and the rule applies only after the identified measurement defects are corrected and reviewed (recording consequence, not ruling text: this precondition is not met, and this procedure does not start, until then);*
   - a Stage 1b record with `validity.ok = true`;
   - for an N2 value under a phase-generic rule (decisions 2 and 3): a Stage 1b-N2 record with `validity.ok = true`. Stage 0 never satisfies this.
2. **Compute** X, Y and the PA-3 check from the record. Show every input with its record path and SHA-256, and every rounding. Until a valid Stage 1c record exists, mark X and Y **provisional (D̂ uncovered)** (PA-1). *Corrected 2026-09-26 (F2):* evaluate PA-3 only on an aggregate M̂ (§3.1 correction); otherwise record memory feasibility as **UNVERIFIED**, not as passed. *Corrected 2026-09-26 (round 2, F2a):* that check is PA-3a, which covers the payload only. Record memory feasibility against the shared host-run limit as **UNVERIFIED** until PA-3b is evaluated on Stage 2's P₂ at C3 (§4), unless decision 7 rules otherwise.
3. **Feasibility:** the §5 table with the applied values, including the `/v7` preconditions from the §0 pitfalls: the fixture cap tuple, and the three `diagnostic_budget_profile` edits (`profile.py:219-226`, `:243-252`, and `:239` with its N2 value).
4. **Record** one ledger entry, "Coordinator application — PART_A TEST_ONLY diagnostic ceiling under the approved measurement-and-margin rule (date)". It states:
   - the rule version and the inputs;
   - X and Y, and whether the shared 120 s / 300 s ceiling suffices;
   - the feasibility result;
   - the scope: the TEST_ONLY `/v7` diagnostic profile only, with no production value set or implied.
5. **Implement only if X or Y exceeds the shared ceiling:**
   - Add a `/v7`-gated PART_A constant beside `_JOINT_N2_DIAGNOSTIC_PHASE` in `profile.py`, citing the ledger entry.
   - It lands with the S5 build (`profile.py` is in S5's file list).
   - When the packet is re-anchored (RC-6), the S5 packet's "no allowance/ceiling change" clause gains a pointer to the entry.
6. **At C3, before any acceptance-grade run relies on the ceiling:** run Stage 1c and re-apply PA-1/PA-2 from its record, which ends the provisional status. Then run Stage 2 and PA-5. *Corrected 2026-09-26 (F1):* only a valid Stage 1c forced arm ends the provisional status, and that arm needs Stage 1c-prep (§3.4). A Stage 1c run with only the prescribed arm does not. A new value is a new profile revision and needs fresh attempts. *Corrected 2026-09-26 (round 2):* even a valid forced arm leaves the worker-side residual R̂ uncovered (§3.4, F1a). Whether an acceptance-grade run may rely on an application with R̂ named and uncovered is decision 4 (§8); until the operator rules, the application stays provisional. At Stage 2, also evaluate PA-3b on P₂ (§4, F2a).
7. **Never** set a production ceiling or cap, a value outside the rule, or a value without a measurement under this procedure. Each of those needs an operator ruling.

## 7. RC-1..RC-6 status (S5 decision draft §5)

**Coordinator disposition, 2026-09-26 (PR #519 review; governs over the snapshot below).** Reviewed base: `main@5ad04cf`, the merge of PR #517.

| RC | Current disposition | Evidence |
|---|---|---|
| RC-1 | **Recorded on the reviewed base** | `main@5ad04cf`, execution-slices plan lines 801–815: the entry "S5 directions adopted, hold kept, 2026-09-26", dated beneath the 2026-09-25 HELD entry at line 797. `git merge-base --is-ancestor ba7247a origin/main` now succeeds, with `origin/main` at `5ad04cf` |
| RC-2 | Open | As in the snapshot |
| RC-3 | Open | As in the snapshot, plus two corrections: memory feasibility needs aggregate evidence and is otherwise UNVERIFIED (§3.1, F2); the Stage 1c forced arm needs Stage 1c-prep (§3.4, F1). *Round 2 (2026-09-26):* the Stage 1b/1c M̂ covers the payload only (PA-3a). Memory against the shared host-run limit stays UNVERIFIED until PA-3b at C3, and whether RC-3 can close on payload-only memory evidence is decision 7 (F2a). The worker-side residual R̂ is uncovered even after Stage 1c (F1a) |
| RC-4 | Open | As in the snapshot |
| RC-5 | Open | As in the snapshot |
| RC-6 | Open | As in the snapshot. If Stage 1c-prep is approved, the re-anchoring also folds in its structural requirement on the adapter (§3.4) |

**No S5 release proposal is supported.** Five conditions remain open, including both immediate blockers the draft names, RC-2 and RC-3. This disposition records status only. It approves no rule, closes no condition and releases nothing.

**Executor snapshot at `0a4cde5`/`32c4d40`** (historical, kept as returned; the table and the paragraph after it):

| RC | Status | Evidence | Owner | Next action |
|---|---|---|---|---|
| RC-1 rulings recorded | **Partly met** | The ledger entry "S5 directions adopted, hold kept" is at plan lines 801–815 on `ba7247a` (PR #517), which is **not on `main`**: `git merge-base --is-ancestor ba7247a origin/main` returns no, and `main@8e9e084` has only the 2026-09-25 HELD entry, at line 797. `main`'s STATE records the ruling with a pointer to PR #517 (`af81e54`) | Coordinator; operator merges | Merge PR #517; RC-1 is then met on `main` |
| RC-2 owner text applied | **Unmet** | None of draft §1.5, §2.5 or §3.4 is applied. Contract decision 3 is unchanged (plan line 88), and so is the spec §2.6 table (spec lines 143–153). The delta §10 hook, run on this head for boundary, K3, N1 and N2, prints `UNROUTED` for all four. Draft §6 Q12 (the OF-5..OF-7 gates) is unresolved | Coordinator drafts; operator accepts | After the stack lands: owner-text PRs for boundary spec §3.1, full-E1 spec §2.2a/§2.4/§2.5/§2.6/§5, and slices plan decisions 3 and 6 plus the S5 text; resolve Q12; re-run the hook |
| RC-3 PART_A envelope | **Unmet** | No maximum-expansion measurement exists (§0 findings 1–2). There is no `/v7` profile (`profile.py` defines v1–v6). This proposal returns the rule; it is not approved | Operator approves the rule; coordinator measures and applies | Decisions 1–4 (§8); Stage 1b (Stage 0 is calibration only); the §6 application, provisional until Stage 1c; Stage 1c and Stage 2 at C3. Open point: RC-3 asks for Σ-feasibility "for the `/v7` profile", which exists only after the S5 build. This proposal offers the §5 arithmetic before release and the executed test at C3 (decision 5) |
| RC-4 client seed view | **Unmet** | The client may `FETCH_PLAN_CHUNK` (`campaign_protocol.py:92`), and the plan still carries seed values (`seed_identity.py:39`). No owner or slice is named, §1.5(d) is not applied, and there is no F1 admission check. The ruling names no gate owner | Unassigned (draft §6 Q10: TB-F1 or a qualification slice) | Name the owner and slice; apply §1.5(d); write the F1 admission-check text in the owner record |
| RC-5 OF-1..OF-7 assigned | **Unmet** | No owner record holds the assignment, and the Q12 gate discrepancy is open | Unassigned | Resolve Q12; for each OF, record the owner, the gate it precedes and where its record lands. Boundary spec §3.1 is the natural owner |
| RC-6 packet re-anchored | **Unmet** | S5 packet §7 is "_Pending._", and its §0 anchors were never taken at the S4 merge head (`228447c`). Its prerequisite, the §3.4(d) text, is not applied (RC-2) | Coordinator | After RC-2, re-read §0 at the release head. Fold in: §0 finding 1 (the Linux "prescribed expansion" case is impossible on (2, 4, 2), so the arithmetic boundary test stands alone), both §0 pitfalls, and the §6 pointer |

**Release proposal: none is supported.** Five of six conditions are unmet, and RC-1 is not yet on `main`. The two immediate blockers the draft names both remain open: corrected owner text (RC-2) and a defensible measured envelope (RC-3). RC-3 cannot close until the operator approves a rule and a Stage 1b record exists. *Operator ruling 2026-09-26 (in session; [ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26)): no provisional ceiling closes RC-3.*

## 8. Operator decisions requested

1. **The rule:** approve, amend or reject PA-1 to PA-5 and their PROPOSED parameters: m_c = 2.0, m_w = 3.0, L = 30 s, m_m = 1.5, spread 1.30, PA-5 factor 1.25, and the shared-ceiling floor.
2. **The rule's scope:** PART_A only, or phase-generic for TEST_ONLY diagnostic ceilings (§4). This decides how `/v7` gets its N2 ceiling.
3. **The `/v7` N2 ceiling:** extend the M13 "/v6 only" ruling to `/v7`, or apply the rule. Applying the rule needs decision 2 to be phase-generic **and** a valid Stage 1b-N2 record under §3 (decision 4). Stage 0 cannot supply the value: it is calibration only (§3.4, PA-4). Without Stage 1b-N2, the only route is extending the M13 ruling.
4. **The measurement steps, approved separately:**
   - ~~Stage 0, an artifact download, for calibration only (**retention ends about 2026-10-09**);~~ *Corrected 2026-09-26:* the Stage 0 download was approved and done on 2026-09-26, and the logs are preserved (§2 correction). Reading them for calibration remains Stage 0 work once the rule is approved;
   - Stage 1b, a new `workflow_dispatch` measurement job, which is both a CI configuration change and a Linux host dispatch; with the Stage 1b-N2 arm only if decision 3 applies the rule to N2;
   - *Added 2026-09-26 (F1):* **Stage 1c-prep** (§3.4): the structural requirement on the S5 adapter's request builder, a change to the S5 packet text, together with the Stage 1c harness substitution. The alternative is the expansion-capable fixture, a different workload. Without either, D̂ stays uncovered and no acceptance-grade run can rely on the ceiling (§6 step 6). The choice constrains the S5 build, so it is needed before release;
   - Stage 1c at C3, a re-dispatch of that job against the built S5 adapter;
   - whether Stage 1b runs on the host venv (as specified) or inside the built worker image (§2), which would make `image_digest` required;
   - *Added 2026-09-26 (round 2, F1a):* whether an acceptance-grade run may rely on an application whose worker-side residual R̂ (§3.4) is named and uncovered, or whether R̂ must first be covered, for example by driving the worker's PART_A result path once the S5 plan exists. Without this ruling the application stays provisional.
5. **RC-3 feasibility evidence:** whether the §5 arithmetic on proposed `/v7` values counts as pre-release feasibility evidence, with the executed binding test at C3.
6. *Added 2026-09-26 (round 2).* **The reading of the D2 falsifier:** confirm or reject the §5 reading that "cannot be measured before S5 is released" (decision draft line 228) means evidence that no valid bound can be obtained, so that a Blocked or Invalid outcome does not trigger the falsifier. The draft's literal wording is broader. The same reading is named for the RC-2 owner-text review of draft §2.3.
7. *Added 2026-09-26 (round 2, F2a).* **RC-3 memory coverage.** The Stage 1b/1c M̂ covers the payload only. Memory against the shared host-run limit is checked only by PA-3b, on Stage 2 at C3, and at the prescribed workload. Rule on:
   - whether RC-3's memory item may close before release on payload-only PA-3a, with PA-3b at C3, as decision 5 proposes for Σ-feasibility;
   - whether PA-3b's composition for maximum expansion, `P₂ + max(0, M̂ − M̂ₚ)`, is accepted despite its unmeasured additive assumption, or whether a measured allowance for the non-payload processes, or the expansion-capable fixture, is required instead.

   Until the operator rules, RC-3's memory item cannot close.

## 9. Unverified and limits

- **Linux CPU:** the Linux payload CPU of any stage is not read here. Whether the S4 artifacts' journals carry `Consumed … CPU time` lines is unverified (Stage 0). *Corrected 2026-09-26:* the artifacts are now preserved locally but still unread (§2 correction).
- **Stage 1c forcing (F1, 2026-09-26):** no measurement-only way to force expansion through the S5 adapter exists at this head; the adapter is not built. Whether the built adapter meets the Stage 1c-prep requirement, and whether it accepts the forced request, can be checked only at C3.
- **Memory (F2, 2026-09-26):** whether systemd 255 populates `MemoryPeak` for an exited unit is unverified. If no aggregate reading is available, memory feasibility stays UNVERIFIED and RC-3 cannot close.
- **Shared memory scope (round 2, F2a, 2026-09-26):** no stage measures the host-run footprint at maximum expansion. Stage 2's parent peak covers the prescribed workload only. The memory the non-payload processes use (qexec, launch clients, guardian) is unmeasured; if the S4 journals log parent peaks, Stage 0 can orient on it but cannot set a value.
- **Worker-side residual (round 2, F1a, 2026-09-26):** R̂, the worker's encode, validate, frame, write and fsync at maximum expansion, is not measured by any stage.
- **Cited record:** the record `20260924T034139Z-59ce3c4b7643` (N2 211.39 s, N1 13.36 s) was not found locally. Both figures are cited from the ledger (plan line 756).
- **Runner hardware:** the GitHub runner hardware class comes from vendor documentation and is not verified. The Stage 1b dry run must confirm that systemd 255 populates `CPUUsageNSec` and `MemoryPeak` for an exited `RemainAfterExit` unit.
- **The §1 CPU figure** is arithmetic from Windows per-call costs, not a measurement, and is used only for orientation.
- **D̂ is uncovered before C3.** The N2 FULL baseline derivation and the real S5-D1 artifact writing do not exist before the S5 build. Any ceiling applied before Stage 1c is provisional (PA-1).
- **Host venv against worker image:** Stage 1b measures the host venv, not the worker image. The factor between them is unmeasured (§2). PA-5 at C3 is the only check.
- **Windows accounting:** the job-object and `process_time` path (§3.1) is specified from the platform APIs and not yet exercised by any harness here.
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
# Per-call verify_for CPU on every row (range 1.02-1.16 s; rises with depth) and setup CPU (10.4-12.4 s)
python -c "import json;[print(r['confirmation_depth'],r['repeat'],round((c:=r['phases']['e1_run']['components']['proof.source_reverify'])['cpu']/c['calls'],3),r['phases']['setup_fixture_domain_contract_source']['cpu']) for r in json.load(open('docs/notes/2026-09-24-t10-step4/composition-sweep.json'))['rows']]"
# Outer panel filled to the whole source length
grep -n "while len(panel) < len(sessions)" ops/c1_rail/qualification/regime.py
# /v7 refused (accept tuple v3-v6), funded branch v4-v6, N2 widening v6 only; fixture cap tuple v3-v6 only
grep -n "fresh diagnostic execution profile required\|funding_intents='qualification_campaign_funding/v1'\|== 'qualification_execution_profile/v6'" ops/c1_rail/qualification/execution/profile.py
# Windows memory reader used by the engine
grep -n "def _peak_memory_bytes\|PeakWorkingSetSize\|ru_maxrss" ops/c1_rail/qualification/production.py
# Freeze-candidate production depth and horizon
grep -n "NOT FROZEN\|continuous500-session\|Part A candidate d=200\|append reserved panels" docs/briefs/phase3-preparation/2026-09-15/freeze-candidate.md
grep -n "if release_doc\['schema'\] in" tests/integration/qualification_boundary/fixture_producer.py
# Binding feasibility and payload quota
sed -n 2776,2783p ops/c1_rail/qualification/execution/campaign_store.py
grep -n "quota = budget_cpu_ns" ops/c1_rail/qualification/execution/campaign_supervisor.py
# RC-1: the ruling entry is not on main
git merge-base --is-ancestor ba7247a origin/main && echo on-main || echo not-on-main
```

*Correction 2026-09-26 (PR #519 review):* the last check now prints `on-main` (`origin/main` = `5ad04cf`). Checks for the corrections, at `8c15f18`:

```bash
# H1: the S5 ruling entry sits beneath the HELD entry on main (expect lines 797 and 801)
git show 5ad04cf:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md | grep -n "^### Operator ruling — S5"
# F1: no Part A adapter yet; the N1/N2 request builder is looked up at call time; tolerance pinned; source bound to one contract
grep -rn "run_part_a_compute" ops/ tests/ || echo no-adapter
grep -n "def stage_request\|_run_stage(stage_request" ops/c1_rail/qualification/execution/compute.py
grep -n 'Decimal("0.95"), Decimal("0.01")' ops/c1_rail/qualification/contract.py
grep -n "self.contract is not contract" ops/c1_rail/qualification/production_source.py
grep -n "'part_a_runner':'c1_rail.qualification.part_a'" ops/c1_rail/qualification/trust_domain.py
# F2: the service limits and observes cgroup memory; fp.py runs a probe and the command as children
grep -n "'memory.max'\|'memory.peak'\|'Memory': context.profile.memory_bytes" ops/c1_rail/qualification/execution/campaign_supervisor.py
grep -n "subprocess.run(\|return subprocess.call(command" scripts/fp.py
# Stage 0 preservation (run in the operator's primary checkout; expect the stated hash and a clean check)
sha256sum local_artifacts/s4-linux-run-logs-2026-09-25/SHA256SUMS
(cd local_artifacts/s4-linux-run-logs-2026-09-25 && sha256sum -c --quiet SHA256SUMS && echo all-222-match)
```

*Round 2 (2026-09-26):* checks for the round-2 corrections, at `8c15f18`:

```bash
# F2a: the limit and peak are on the host-run parent, which also holds qexec, launch clients, the guardian and the payload slice
grep -n "self.parent = _host_path\|including shared qexec/launch clients\|Counters are never reset per work\|expected_parent = _scope_path(runtime.parent\|'Tmpfs'" ops/c1_rail/qualification/execution/campaign_supervisor.py
grep -n "Include all campaign controllers/guardians\|Memory is a maximum concurrent campaign footprint" docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md
# F1a: the adapter returns byte strings; the worker encodes, validates, frames, writes and fsyncs; the packet's rejection and assessment fields
grep -n "returns the initial-prefix document and the final document as separate byte strings\|Reject omitted or unnecessary expansion\|expansion_required., .tolerance_comparison" docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md
grep -n "encode_worker_result(context\|parse_worker_result(\|_os.fsync" ops/c1_rail/qualification/execution/worker.py
# Falsifier text against the D2 ruling words
grep -n "cannot be measured before S5 is released" docs/notes/2026-09-26-s5-decision-draft.md
grep -n 'D2: "Retain per-phase accounting."' docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
```
