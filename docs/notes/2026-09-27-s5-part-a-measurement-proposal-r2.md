# S5 Part A measurement-and-margin proposal, revision r2 (PART_A only, TEST_ONLY), with the CP-1a measurement dispatch

**Status:** PROPOSAL r2, returned for operator decision at **CP-1a**. Nothing here is approved. Every multiplier, allowance and threshold marked CANDIDATE is a candidate rule parameter, not a ceiling. S5 stays **HELD** ([ledger, 2026-09-27 ruling](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27)).

**Supersedes, for CP-1a purposes:** the #519 proposal r1, `8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md` ([pinned head](https://github.com/Joshua-Asante/first-passage/blob/8c15f1853e64f14f50995e3f1c55a620a0f674b7/docs/notes/2026-09-26-s5-part-a-measurement-proposal.md)). r1 also carries the fix round and the coordinator review "ACCEPTED AS INPUT; nothing approved; S5 stays HELD" (`8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md:52-79`). r1 stays the historical input. This r2 note is self-contained, and every change from r1 is listed in §1.

**Card:** [handoff H1](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h1--s5-measurement-correct-the-519-proposal-return-a-measurement-dispatch), step (a) only. **Sequencing owner:** [deployment-checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) §0–§5 (CP-1a, §4).

**Authority:**
- Operator ruling 2026-09-26 §6 authorizes *preparing* the proposal only ([ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26)).
- The 2026-09-27 operator direction splits build entry from C3 ([ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)).
- The 2026-09-27 ruling approves the staged gates with Part A-only rule scope and keeps the hold (ledger, linked above).
- The other 2026-09-27 rulings were read and do not bear on S5: [§59 Ruling 6](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-6--orb-resting-entry-lifecycle-l1-and-the-account-fence-classification-contract-2026-09-27), and [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27) and [§A11.3](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27).

**Sources read at `521d8f2`** (branch `claude/clever-wozniak-bx0u95`). Under `ops/`, `tests/`, `tools/`, `deploy/`, `scripts/` and `.github/`, `git diff --stat 8c15f18 HEAD` is empty. So every r1 code citation was re-checked against bytes identical to r1's, and each is re-verified in §2. **No measurement, Linux dispatch, workflow file, artifact download, qualification service or S5 work was run.** Every figure below is either cited or labelled as arithmetic.

**Not granted:**
- no measurement execution, CI-configuration change, Linux dispatch or artifact download;
- no approved numerical rule;
- no ceiling, profile, release-literal or budget change;
- no S5 release, freeze, dispatch or execution;
- no statistical dispatch;
- no production value;
- no production, activation or live authority.

---

## 0. Summary

**Returned for CP-1a** (decision list in §14):
1. **The rule.** PA-1..PA-5 remain CANDIDATES (§9). Their scope was ruled on 2026-09-27: PART_A only, TEST_ONLY.
2. **One measurement dispatch, as a single approval packet** (§12):
   - Stage 0: calibration download, which must run before about **2026-10-09**;
   - Stage 1a: Windows harness validation;
   - Stage 1b: a new `workflow_dispatch` workflow file and its two-job Linux run;
   - Stage 1c: at C3, through the built adapter;
   - Stage 2: service-route consistency at C3;
   - the choice of host venv or worker image.
3. **A separate ruling on the `/v7` N2 ceiling.** It is not under the rule.
4. **A D2 falsifier reconciliation** (added in the 2026-09-27 fix round): the owner's measurement limb against the H1 card's stop classification (§10.3).

**The two operator acceptance conditions:**
- **(1) Stage 1c forces maximum expansion through the built adapter** (§7). This is *not* BLOCKED. The forcing seam is PROPOSED: a TEST_ONLY measurement override of the Part A request's `within_pp`, injected only through a keyword argument of the built adapter, refused under non-TEST_ONLY authority, and absent from every signed document. The authority gate does **not** separate the measurement from the signed TEST_ONLY S5 route, because every signed S5 route is itself TEST_ONLY (`worker.py:37-38`). Exclusion of the signed route therefore rests on proof obligations P-3 (static and spy), P-4 (signed-document key sets) and P-5 (not adjudicable), and each is a hard C3 precondition (§7.3, §7.7). The S5 build must add the seam, so it is returned as PROPOSED S5 build requirements SR-1..SR-8 for the RC-6 re-anchor, together with proof obligations P-1..P-7, for approval at CP-1a (item 2(e)). If the built adapter at C3 lacks any of them, Stage 1c returns **BLOCKED** with this seam as the proposal.
- **(2) Aggregate memory is complete** (§8). The memory input on every timed repeat is the measured unit's cgroup v2 `memory.peak`, which includes every descendant, with swap off. It is read inside the unit and cross-checked against systemd `MemoryPeak`. A per-job accounting probe runs before any timed repeat. A job with any timed repeat that has only a lower bound is recorded with memory feasibility **UNVERIFIED**, and the rule is not applied to that record. That record is retained as it is. The CANDIDATE PA-4 re-run (once, on a fresh runner) can produce a second, complete record, but it never upgrades the first (§8.3). If memory is still UNVERIFIED after the allowed re-run, RC-3a stays unmet and build entry needs an operator ruling (§10.3).

**New in r2, beyond the carried findings:**
- **F7: no memory figure measures this workload.** The only in-repo memory figure is the lifetime peak working set of **one** Windows process that ran nine full composition E1 runs in sequence (setup, N1, N2, Part A where reached, and adjudication; depths 2, 10 and 30; six rows reached Part A). The recorded `process_peak_memory_bytes` rises monotonically from 121,028,608 to 136,695,808 bytes over the nine rows (`docs/notes/2026-09-24-t10-step4/composition-sweep.json`, top-level `processes: 1`; the harness calls `one_run(depth)` in one interpreter, `measure_composition.py.txt:177-179`, and records `production._peak_memory_bytes()` at `:149`; the note says "Runs used one process", [2026-09-24 note](2026-09-24-t10-step4-representative-measurement.md) line 8). It measures neither a single run nor the PART_A forced workload, and it is **not** a lower bound on M̂. *Orientation only, a different workload and not comparable:* the PA-3 threshold at the candidate m_m = 1.5 is 256,000,000 ÷ 1.5 = 170,666,667 bytes if the P4 tuple is extended to `/v7`, or 230,400,000 ÷ 1.5 = 153,600,000 bytes under the unextended default binding (P4, §8.1). The recorded maximum would be 80.1% or 89.0% of those (arithmetic). A Linux cgroup peak also counts the page cache and the launcher process. A PA-3 failure goes to an operator ruling (§9).
- **F8: a gap in r1's Stage 1c.** The built adapter builds its request from the frozen contract, whose expansion tolerance is pinned at 0.01 (`contract.py:763-773`). On (2, 4, 2) it therefore never expands. r1 re-ran "the Stage 1b job … against the built S5 adapter" (`8c15f18:…proposal.md:212`) without saying how the adapter's forced arm reaches `expanded_panels`. §7 closes the gap.

**RC status on the 2026-09-27 split** (§11):
- **Build entry.** RC-1 is **met** (#517 merged at `5ad04cf`, an ancestor of `521d8f2`). The §3.4(d) text, the RC-4/RC-5 assignment, the RC-6 re-anchor and RC-3a are open, and so is the hold-release entry (CP-1b). *Coordinator note at acceptance:* H7 has returned (`docs/notes/2026-09-27-host-obligations-assignment.md`, published when accepted). RC-5 is recorded by the coordinator when H7 is accepted; the RC-4 slice needs the operator's naming (CP-1a item 5, below).
- **C3 and acceptance.** RC-3b, RC-2 and the packet's C3 items are open.
- **Before F1.** Open.

**No S5 release proposal is supported.**

## 1. Change table r1 → r2

| # | r1 (`8c15f18:…proposal.md`) | r2 | Reason |
|---|---|---|---|
| 1 | Status "PROPOSAL", governed by ruling 2026-09-26 (`:3-5`) | PROPOSAL r2; supersedes r1 for CP-1a; sources re-read at `521d8f2` | H1 step (a): write a corrected revision, not a new analysis |
| 2 | Code citations taken at `62c956f` | Every citation re-verified at `521d8f2` (§2). None of r1's anchors moved. Two anchors that r2 itself introduced were wrong (P3's `_DIAGNOSTIC_PHASE` / `_JOINT_N2_DIAGNOSTIC_PHASE` lines, and §8.2's description of `scripts/fp.py:274`) and were corrected in the 2026-09-27 fix round. Two are made more precise: the fixture cap is the default at `fixture_producer.py:152-153` and the v3–v6 raise at `:154-156` (r1 used both "152-156" and "154-156"); `within_pp` is read only at `part_a.py:208` | H1: "re-verify each cited line at HEAD 521d8f2" |
| 3 | RC-1 "partly met" (`:356`) | RC-1 **met**: #517 merged at `5ad04cf`, an ancestor of HEAD | Ledger 2026-09-27; `git merge-base --is-ancestor` |
| 4 | One RC-1..RC-6 table (`:352-363`) | Restated on the build-entry / C3-and-acceptance / before-F1 split, with RC-3a and RC-3b as the ledger defines them (§11) | Ledger direction 2026-09-27 |
| 5 | Decision 2: PART_A only, or phase-generic (`:293`, `:368`) | **Ruled 2026-09-27**: PART_A only, TEST_ONLY. The phase-generic option is deleted | Scope: the ledger ruling, "The margin rule's scope is **PART_A only, TEST_ONLY**" (slices plan line 844). Deleting the phase-generic option: the H1 card applying that ruling (handoffs line 94) |
| 6 | Stage 1b-N2 arm (`:210`), stage `1b-N2` in the schema (`:226`), the N2 precondition in §6 step 1 (`:337`) | All removed | The H1 card (handoffs line 94, "Drop Stage 1b-N2 and the phase-generic option") applying the ledger ruling ("do not silently extend the rule to N2", slices plan line 839; "`/v7`'s N2 ceiling therefore cannot come from the rule", line 845) |
| 7 | `/v7` N2 value from "extend M13, or apply the rule" (`:23`, `:369`) | Only from a **separate operator ruling**, for example extending the M13 "/v6 only" ruling to `/v7`. Returned as CP-1a item 3 | Ledger ruling 2026-09-27 (slices plan line 845) |
| 8 | Decision 5: arithmetic as pre-release feasibility (`:375`) | **Ruled 2026-09-27**. §10's arithmetic is the build-entry evidence (RC-3a). The executed `bind_budget` check moves to C3 (RC-3b) | Ledger ruling and direction 2026-09-27 |
| 9 | RC-4/RC-5 "unassigned" (`:359-360`) | Assignment by handoff H7 (`docs/notes/2026-09-27-host-obligations-assignment.md`, forthcoming, status open). It does not wait on F1 | Ledger ruling 2026-09-27; H1 card |
| 10 | Stage 1c: "the Stage 1b job is re-run against the built S5 adapter" (`:212`), with no forcing mechanism | Forcing through the built adapter specified (§7): seam, gate, S5 build requirements SR-1..SR-8, proof obligations P-1..P-7, BLOCKED rule | Operator acceptance condition 1; finding F8 |
| 11 | Memory: "cgroup `MemoryPeak` when present, else the primary value, flagged as a lower bound" (`:123`) | A complete aggregate is required on every timed repeat (in-unit `memory.peak` plus systemd `MemoryPeak`, swap off, a probe per job). A lower bound means memory is UNVERIFIED and the rule is not applied to that record (§8) | Operator acceptance condition 2 |
| 12 | No memory figure cited | F7: the only in-repo memory figure is one Windows process's lifetime peak over nine full composition E1 runs; it is not a lower bound on M̂ and not comparable to the PA-3 threshold (§0) | New read of an existing record (corrected in the 2026-09-27 fix round) |
| 13 | D2 falsifier triggered by an invalid measurement, digest mismatch, or Stage 1b not approved (`:326-329`) | The owner's two limbs are separated (§10.3). The **Σ limb** is the stop class **D2 ACCOUNTING-DESIGN FALSIFIER** (Σ infeasible at every admissible value). The **measurement limb** ("cannot be measured before S5 is released") stays live: an INVALID MEASUREMENT, non-approval or non-execution does not fire D2 when it occurs, but if no valid Stage 1b record exists at the release point it engages, unless the operator sets the ceiling by ruling. **This changes, and does not keep, the timing of r1's triggers and of the fix-round clause** that non-approval triggers D2: they engage at the release point, not on the event; reconciliation is CP-1a item 4 | H1 card stop classification (handoffs lines 116-121: "the last is the D2 falsifier"); owner text S5 draft line 228 |
| 14 | Commands invoked `measure_part_a_max.py` while the harness is kept as `.py.txt` (`:149` against `:174`, `:198`); `systemd-run --uid/--gid` (`:194`) | Commands use the `.py.txt` path (Python runs any path as a script). Units run as root, like the S2 workflow's own invocation (`qualification-s2-supervision.yml:135`, `:141-142`, under `sudo`) | Consistency; `--uid` depended on unverified read access to a root-provisioned venv |
| 15 | Workflow described in six bullets (`:179-183`), with no cleanup step | The workflow file is specified in full (§12.3): triggers, matrix, steps, owned cleanup, artifact names, retention, and the note that it must reach the default branch to be dispatchable (UNVERIFIED) | H1: "describe the YAML content fully enough to be written" |
| 16 | No runner-time estimate or re-run limit | Runner-minute arithmetic (§12.6); one re-run per failed validity check | H1 card |
| 17 | Stage 0 greps journal lines only (`:167`) | Adds download hashes, run metadata, and the retained `memory_peak_bytes` values, all for calibration only | Calibration completeness; still sets no value |
| 18 | Stage 2 compares CPU only (PA-5) | Also records the campaign-parent `memory_peak_bytes` against the same footprint | Condition 2; the service already enforces it (`campaign_store.py:2985-2986`) |
| 19 | Schema `s5-part-a-max-expansion-measurement/v1` (`:221-242`) | `/v2` (§12.8): memory block, forcing block, stop class, Stage 1c artifact fields; `1b-N2` removed | Items 6, 10, 11, 13 |
| 20 | — | Flags the conflict between the measurement seam and the S5 packet's four tolerance sites: the Authority line "no tolerance relaxed" (line 8), §2 Forbidden "accepted formulas and tolerances" (line 35), §3 "never a relaxed tolerance" (line 49) and §6 Forbidden "a relaxed tolerance" (line 61). Returned as PROPOSED SR-7 for the RC-6 re-anchor and CP-1a | The seam must be explicit, not an implicit packet breach |
| 21 | Worker-image option described (`:87`) | Kept, with its preconditions stated for CP-1a (§5.3) | H1: "host venv versus worker image is disclosed" |
| 22 | §6 application preconditions (`:334-337`) | Updated: the record must have complete memory (r2's derivation from the ruling's condition (2), slices plan line 848); no N2 value under the rule, and a proposed N2 value for the arithmetic; the application is provisional until Stage 1c | Items 6, 11 |

## 2. Findings carried forward, re-verified at `521d8f2`

| # | Finding (r1 anchor) | Evidence at `521d8f2` | Status |
|---|---|---|---|
| F1 | **The (2, 4, 2) fixture can never expand; maximum expansion needs a forced arm** (`:13`) | Expansion is pinned to `abs(p5 − 0.95) ≤ 0.01` for every domain (`contract.py:763-773`; `should_expand` at `:110-114`). The workload is `QualificationWorkloadPolicy(counts,5,5,6,2,4,2)` (`composition_fixture.py:195`), PART_A depth 2 (`:236`), `initial_panels=2, expanded_panels=4, paths_per_population_per_panel=2` (`:241`). With 2 paths a panel's rate is 0, 0.5 or 1, and none is within 0.01 of 0.95. The smallest expanding depth is 17 (16/17 ≈ 0.941, arithmetic). All six composition rows that reached Part A ran `REGIME` 4 paths and 3 panel proofs (re-parsed, §Verification) | Holds |
| F2 | **No existing measurement covers maximum expansion** (`:14`) | `benchmark_part_a.py:1` ("One representative synthetic Part A workload, never a qualification panel batch") uses `synthetic_replay`, not `ProductionSource` (`:51-77`). The 2026-09-24 harness runs the signed route, which never expands (F1) | Holds |
| F3 | **`verify_for` dominates** (`:15`) | Called on every replay (`production_source.py:861`, `:867`) and every panel proof (`:891-894`), and once at compute start (`compute.py:28`). Re-parsed per-call CPU: 1.021–1.051 s (depth 2, 32 calls), 1.042–1.087 s (depth 10, 56 calls), 1.077–1.160 s (depth 30, 107 calls). Windows, CPython 3.13.2 | Holds |
| F4 | **The engine's pilot predicate needs the PA-2b term** (`:16`) | Pilot at `part_a.py:178-182`, prediction `probe + max_panels × (rebuild + depth × path)` at `:184`, refusal at `:185-186`, even when no expansion follows. The service's payload quota is `(cpu_ns − O) × 10⁶ ÷ remaining_wall` (`campaign_supervisor.py:177-194`, `:191`) | Holds |
| F5 | **No host factor is evidenced** (`:17`) | The "roughly 137 s on Linux by scaling" figure is in the plan's M13 entry (`2026-09-18-full-e1-execution-slices.md:756`). The record `20260924T034139Z-59ce3c4b7643` was not found in the checkout: `find` has no hit, and `git log --all -S` finds only the commits that cite it (`5a46cb30`, `0a4cde58`) | Holds |
| P1 | **`/v7` is refused outright** (`:21`) | The accept tuple for v3–v6 is at `profile.py:220-225`, and the raise `fresh diagnostic execution profile required` at `:226`. `parse_profile` selects its fixed fields per schema at `:116-140` | Holds (`:219-226` range as cited) |
| P2 | **`/v7` is unfunded if only the accept tuple is extended** (`:22`) | The funded branch is v4–v6 only (`profile.py:243-252`, `funding_intents` at `:250`) | Holds |
| P3 | **N2 falls back to 120 s if the `:239` branch is missed** (`:23`) | `if profile.values['schema'] == 'qualification_execution_profile/v6'` at `profile.py:239`; `_JOINT_N2_DIAGNOSTIC_PHASE` 360 s / 900 s at `:211`; shared `_DIAGNOSTIC_PHASE` 120 s / 300 s at `:209` (line numbers corrected in the 2026-09-27 fix round; `:207` is a comment). **r2 change:** the N2 value for `:239` comes from the separate operator ruling (§14 item 3), never from the rule | Holds; routing changed |
| P4 | **The fixture-cap tuple** (`:24`) | The default contract budget is 120 s CPU / 180 s wall / `maximum_memory_bytes = memory_limit*9//10` (`fixture_producer.py:152-153`), that is 230,400,000 bytes for a 256,000,000-byte profile (arithmetic). The 10,000 s / 10,000 s / `memory_limit` raise applies only for releases v3–v6 (`:154-156`), where `memory_limit` is the release profile's `memory_bytes` (`:96`). An unextended `v7` release binds 120 s / 180 s / 230,400,000 bytes and is `BUDGET_EXHAUSTED` at binding, on CPU and wall Σ and also on memory, since a phase `memory_bytes` of 256,000,000 exceeds 230,400,000 (`campaign_store.py:2776-2783`, the `max(p['memory_bytes'] …) > binding['maximum_memory_bytes']` term at `:2781`) | Holds (default memory cap added in the 2026-09-27 fix round) |

Other r1 anchors used below were re-verified unchanged:
- `part_a.py:139-142` (seeds by panel and path index);
- `regime.py:22` (`tb-s2-rng-v2`), `:68-78` (outer panel filled to the source length), `:83` (panel proof);
- `production.py:89-96` (`_part_a_request`) and `:99-122` (`_peak_memory_bytes`);
- `trust_domain.py:382-385`;
- `campaign_budget.py:12-13` (`PHASES`);
- `campaign_store.py:2794-2801` (void term) and `:2879-2895` (retries; compute phases excluded at `:2887`);
- `campaign_supervisor.py:284-297` (guardian `LimitCPU` = 20 − 3 × (1 + 1) − 1 = 13 s, arithmetic from `CAMPAIGN_RESOURCE_SCOPE`, `profile.py:55-66`);
- `image.py:53-64`;
- `qualification-s2-supervision.yml:68` (`runs-on: ubuntu-24.04`) and `:143-179` (evidence export, `retention-days: 14`).

## 3. Review corrections kept

| Correction (fix round and coordinator review, `8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md:52-66`) | Where in r2 |
|---|---|
| The cold repeat is timed and included in the maximum. It follows a `__pycache__` purge and page-cache drop; the arm order alternates between jobs; the instrumented repeat runs last | §6.2; §12.3 loop |
| Setup CPU (fixture, keys, signing, trust domain, contract: 10.36–12.38 s on Windows, re-parsed) is excluded from Ĉ | §6.1 |
| D̂ (the N2 FULL derivation plus the real S5-D1 artifacts) stays **uncovered** until Stage 1c; any earlier application is **provisional** | §4, §9 PA-1, §13 |
| Windows figures validate the harness only and never enter a ceiling | §6.1, §12.2 |
| Host venv versus worker image is disclosed as an unmeasured factor; PA-5 at C3 is its only check | §5.3, §9 PA-5 |
| Stage 0 is calibration only and can set no value | §12.1 |
| The D2 falsifier stays **open** until a valid Stage 1b record exists | §10.3. **Kept.** The same fix-round bullet's second clause ("It is triggered if Stage 1b is not approved or cannot run before release, unless the operator sets the ceiling by ruling", `8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md:61`) is **changed, not kept**: r2 treats non-approval or non-execution as engaging the owner's measurement limb only at the release point (§10.3). Reconciliation is CP-1a item 4 |

## 4. Maximum-expansion workload

**Definition** (r1 `:30-37`, unchanged). The workload is one PART_A compute work (`campaign_budget.py:12-13`) that runs `_run_part_a` (`part_a.py:127`) from the pilot through the appended panels `[initial_panels, expanded_panels)`. It includes:
- worker start;
- source admission;
- one compute-start `verify_for` (the shape of `compute.py:28`);
- the pilot (`part_a.py:178-182`);
- for each panel `0..expanded_panels−1`: outer sampling, one panel proof replay (`regime.py:83`) and `depth` horizon paths (`part_a.py:195-204`);
- the N2 FULL baseline derivation from staged N2 capture bytes (S5-D2, [S5 packet](../briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md) line 22);
- writing the two S5-D1 artifacts with fsync (packet line 20).

The seeds depend only on panel and path index (`part_a.py:139-142`), so a forced expansion performs exactly the computation a prescribed expansion would.

**Owners of the numbers** (r1 `:43-52`, re-read):
- full-E1 spec §2.4 lines 117–125;
- the freeze candidate, "DRAFT — NOT FROZEN", for production depth 200 and horizon 500;
- `production.py:89-96`;
- `trust_domain.py:382-385`;
- `profile.py:167` ("PART_A includes maximum expansion").

| Quantity | TEST_ONLY S5 workload | Production (freeze **candidate**, not frozen) |
|---|---|---|
| initial → expanded panels | 2 → 4 (`composition_fixture.py:241`) | 100 → 200 (`trust_domain.py:382`) |
| paths per panel | 2 | 200 (candidate) |
| horizon / inner block / outer months | 5 / 5 / 6 (`composition_fixture.py:195`) | 500 (candidate) / 5 / 6 |
| replays at maximum expansion | 2 pilot + 4 × (1 proof + 2 paths) = **14** (arithmetic) | 2 + 200 × 201 = 40,202 (arithmetic) |
| `verify_for` calls | 15 (arithmetic) | 40,203 (arithmetic) |
| replays with no expansion | 8 (arithmetic) | 20,102 (arithmetic) |
| can the frozen rule expand? | **No** (F1) | Yes |

**Estimate (arithmetic, orientation only).** 15 calls at 1.02–1.16 s/call gives about 15–18 s, plus panel proofs, 9 short paths, start and admission (about 2.0 s source build). That is roughly 20–30 s CPU on the Windows development host for the forced workload, excluding setup and D̂. The Linux value is unknown (F5).

**Not covered before C3:** D̂. The derivation code and the two-artifact format are S5's. Stage 1b cannot measure them, and Stage 1c does (§7).

## 5. Reference runtime

### 5.1 Identity recorded per run (r1 `:77-85`, kept)

- **Host class:** GitHub-hosted `ubuntu-24.04` (`qualification-s2-supervision.yml:68`). Hardware is not pinned; each run records `/proc/cpuinfo` model, `nproc`, `uname -r` and `systemctl --version`. The vendor's 4 vCPU / 16 GB figure is UNVERIFIED.
- **OS:** Ubuntu 24.04 x86_64, ext4 (`tools/qualification_verification/host.json`).
- **Dependencies:** `requirements-ops.lock` SHA-256 `9aa7c17c…` (`host.json`); thread environment pinned to 1.
- **Code identity:** measured commit, clean tree; `observe_runtime(repo, 'worker')` (`runtime.py:75`); harness SHA-256; fixture file SHA-256s.
- **Release identity:** none exists before S5. Stage 1c records the S5 head and the adapter module's SHA-256, and Stage 2 records the `/v7` release, profile and policy digests.

### 5.2 Mapping to the production host: none

No production qualification host exists (OF-1). No host factor is evidenced (F5). The rule applies **no** host factor. Production budgets remain separately governed.

### 5.3 Host venv versus worker image (disclosed; CP-1a item 2)

| | `host_venv` (**recommended default**) | `worker_image` |
|---|---|---|
| Interpreter | Ubuntu `/usr/bin/python3` 3.12.3 (`host.json`), as `$host_root/env` from `provision.sh` | `python:3.12.3-slim-bookworm` resolved to a digest (`image.py:53-64`), a separately built CPython on Debian, with an overlay filesystem |
| Matches the S5 worker? | No. The host-to-container factor is **unmeasured**; PA-5 at C3 is its only check | Yes, in interpreter and filesystem |
| Precondition | None beyond S2's provisioning | UNVERIFIED that the worker build context (`prepare_context`, `image.py:63-64`) can carry the harness and test fixtures. It needs a Docker run under a measurement slice, and `image_digest` becomes required |
| Cost | As §12.6 | More provisioning time. Not estimated: an image build was not timed in any record read |

Recommendation: `host_venv` for Stages 1b and 1c. The build-entry ceiling is provisional anyway, and the worker-image factor is caught at C3 by PA-5 against the genuine worker. Choosing `worker_image` makes Stage 1b's record carry the image digest and removes the factor from PA-5.

## 6. Capture method

### 6.1 CPU and wall (r1 §3.1, kept)

Boundary clocks are read in the harness at each of the following points:

| Component | Boundary | In Ĉ? |
|---|---|---|
| `start` | process start → harness entry, before any fixture import | yes |
| `admission` | the one `ProductionSource._build_composition` call, timed by a single wrapper that is removed before step 2 (the `measure_composition.py.txt:58-72` pattern) | yes |
| `setup_excluded` | the rest of the fixture, keys, signing, trust domain and contract setup | **no** |
| `verify` (1b) | the compute-start `verify_for` | yes |
| `part_a` (1b) | immediately around `_run_part_a` | yes |
| `serialize` (1b) | stand-in canonical serialization of the prefix and the final panels | yes |
| `adapter` (1c) | from the start of staged-N2 parsing to the return of the second artifact's fsync, through the built adapter (§7.4) | yes |

- **Linux:** `getrusage` user+sys for `RUSAGE_SELF` + `RUSAGE_CHILDREN` at every boundary. The secondary figure is the unit's `CPUUsageNSec`, the cgroup `cpu.stat` total including descendants. The ceiling's CPU input per repeat is the **larger** of the workload `C_w` and `CPUUsageNSec − setup_excluded`, so launcher overhead is charged.
- **Windows (Stage 1a):** `time.process_time()`, and a job object per repeat (`TotalUserTime + TotalKernelTime`). Not comparable to Linux.
- **Wall:** outer `ExecMainStartTimestampMonotonic` → `ExecMainExitTimestampMonotonic`, with `perf_counter` at the boundaries.
- **Engine facts:** `probe_seconds`, `predicted_seconds`, `elapsed_seconds`, panel count, `expanded`.
- **Integrity:** the SHA-256 of the initial-prefix and final bytes.
- **Call counts:** from one extra instrumented repeat per arm, run last and excluded from statistics.

### 6.2 Repeats, statistic and noise (r1 §3.2, kept; the memory term is new)

- **Arms.** `forced` sets every ceiling input. `prescribed` keeps the frozen 0.01 and is the consistency anchor.
- **Repeats.** 5 timed fresh-process repeats per arm per job, on 2 independent jobs, plus 1 instrumented repeat per arm, run last.
- **Cold repeat.** Timed repeat 1 of each arm is cold: `__pycache__` purged and `drop_caches` before it. It is included in the maximum. Arm order alternates: job `a` runs `forced prescribed`, job `b` runs `prescribed forced`.
- **Statistic.** Maxima over all valid timed repeats, cold included: Ĉ (workload CPU), Ŵ (workload wall), M̂ (memory, §8). The median, minimum and spread are reported with and without the cold repeat.
- **Determinism (PA-4).** Every repeat of an arm produces identical artifact digests. The forced arm's first `initial_panels` panels are byte-identical to the prescribed result. Any mismatch is an INVALID MEASUREMENT with no re-run (§12.7), and it is also evidence against D3's R7.
- **Noise (PA-4).** A job whose warm (repeats 2–5) CPU spread exceeds the CANDIDATE 1.30 is re-run once on a fresh runner; a second failure stops the measurement. A between-job median ratio above 1.30 is recorded as host variance.

### 6.3 Harness (to be written in step (b); specified here)

The path is `docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py.txt` (the `.py.txt` convention keeps it out of the import-boundary gate; `python <path>` runs it). Its modes:
- `--repeat-mode`: one repeat in the current process. It is run inside a unit on Linux.
- `--launcher`: Windows only. It spawns fresh `sys.executable` repeats in job objects.
- `--summarize`: computes summary, validity and stop class, writes `record.json`, and exits 0 (valid), 3 (validity failure, re-runnable) or 4 (invalid, no re-run).

Stage 1b repeat steps (r1 `:151-157`, kept):
1. Take the boundary clocks.
2. `build_verified_composition(tmp, confirmation_depth=60, decision_alpha='0.05')`, trading variant.
3. `verify_for` once.
4. Build the request as `production._part_a_request` does, with two exceptions: `within_pp` is the arm's tolerance (forced **1.0**, the maximum `SyntheticPartARequest` admits at `part_a.py:46-49`, so `close` at `:208` is true for every p5), and `budget_seconds = 3600`.
5. Run `_run_part_a(..., full_pass_rate=1.0, synthetic=True)`.
6. Serialize canonically.
7. Assert the panel count: forced 4, prescribed 2.
8. **In-unit memory read (§8.2).**
9. Write one JSON row.

It never calls `_run_composition_e1`, `run_production_e1`, `_execute_e1` or `ProductionExecutor`. This harness-level forcing is used only for Stage 1b, which measures the **existing** engine and has no adapter. Stage 1c forces through the adapter (§7).

## 7. Acceptance condition 1: Stage 1c forces maximum expansion through the built adapter

### 7.1 Why a seam is needed

No S5 adapter exists at `521d8f2` (`grep -rn run_part_a_compute ops/ tests/`: no hit). The packet says only that `compute.run_part_a_compute(contract, source, budget, *, n2_full_outcomes)` "adapts the existing `_run_part_a` loop and its request/provider/proof inputs" (S5 packet §1, line 27). It is therefore **expected**, not established, to build its Part A request from the **frozen contract** the way the existing mapping does (`production._part_a_request`, `production.py:89-96`, which takes `within_pp = float(part.expansion_tolerance)` at `:96`). This expectation stands until C3. Every contract pins that tolerance at 0.01 (`contract.py:763-773`). If the expectation holds, the adapter never expands on (2, 4, 2) (F1), whatever the source. Stage 1c can reach `expanded_panels` through the adapter's own compute only if a request-level override exists.

### 7.2 Alternatives rejected

| Alternative | Why rejected |
|---|---|
| A TEST_ONLY contract with `expansion_tolerance = 1.0` | The contract validator refuses any value but 0.01 for every domain (`contract.py:763-773`). Relaxing it would put the forcing into a **signed** artifact, which is exactly what condition 1 forbids |
| A deeper fixture (depth ≥ 17) that genuinely expands | It measures a different workload from (2, 4, 2), and it needs a synthetic source that lands the initial p5 within 0.01 of 0.95. The packet already doubts that is economical ("if a synthetic source can produce it economically", line 54) |
| The harness monkeypatches `_part_a_request` or `SyntheticPartARequest` | The measured code path is then no longer the worker's own objects; it depends on adapter internals S5 may inline; and it carries no refusal proof. It is a harness-level stand-in, which condition 1 rejects |
| A prescribed (non-expanding) arm through the adapter | Condition 1 rejects it explicitly |

### 7.3 The proposed seam (TEST_ONLY measurement override)

- **Parameter:** the Part A request's `within_pp` (`part_a.py:32`). It is read at exactly one decision point, `close = abs(p5 − floor) ≤ within_pp` (`part_a.py:208`). It changes nothing else: seeds, sampling, the prefix, the final floor and the FULL sanity rule are untouched (`part_a.py:139-142`, `:209-215`).
- **Forced value:** exactly `1.0`. It is a closed value, not a free float, so the seam cannot express an arbitrary relaxed tolerance.
- **Where it is injected:** a keyword-only argument on the built adapter (or its accepted successor), `measurement_override=None`. Its value is an instance of a frozen type `PartAMeasurementOverride(within_pp=1.0)` with the fixed label `TEST_ONLY_MEASUREMENT_FORCED_EXPANSION`. The adapter first builds the request from the frozen contract exactly as in the route. Only if an override is present and the gate passes does it apply `dataclasses.replace(request, within_pp=override.within_pp)`; `SyntheticPartARequest.__post_init__` re-validates.
- **Gate** (refused before any source verification, compute or file write): the override is accepted only when `contract.trust_domain.authority_class == 'TEST_ONLY'` and `contract.trust_domain.permits_synthetic is True` (`trust_domain.py:303`, `:313-314`), and the contract's authority is `evidence_class = TEST_ONLY` (`contract.py:848-852`). This is the property of the TEST_ONLY diagnostic release (the worker already refuses anything else, `worker.py:37-38`).
- **What the gate does not do.** The gate is coextensive with the signed TEST_ONLY worker route: every signed S5 route, including the genuine TEST_ONLY campaigns for S5 acceptance and Stage 2, satisfies it. It excludes production authority only (P-1), which the worker cannot reach anyway (`worker.py:37-38`). It does **not** exclude the signed route. The exclusion of every signed route rests solely on P-3 (the static AST test and the `run_worker` spy test), P-4 (signed-document key sets) and P-5 (a forced result is not adjudicable). Each is a hard C3 precondition (§7.7). A discriminating condition that the signed route cannot satisfy (for example, the SR-3 callable refusing a non-`None` override whenever it is invoked with a worker execution context) is **not** proposed here, because it would make Stage 1c call the callable differently from the route and so weaken P-7. The operator may add one at CP-1a.
- **Never a field of any signed document:** the `/v7` release and profile, the campaign plan, the checkpoint plan, the dispatch and the `/v8` snapshot carry no key that maps to it. `run_worker` (`worker.py:25`; its compute dispatch is at `:69`) never passes it.

### 7.4 PROPOSED S5 build requirements (for the RC-6 re-anchor; for CP-1a approval, item 2(e))

| ID | Requirement |
|---|---|
| SR-1 | The override type and the adapter keyword of §7.3, in `execution/compute.py` (already in the packet's §2 file list). No `part_a.py` change is needed |
| SR-2 | The gate of §7.3, applied before `verify_for`, before any compute and before any write |
| SR-3 | The PART_A worker body after bundle and plan verification is one store-free callable that `run_worker` itself calls. It covers the parse of the staged N2 capture bytes, the N2 FULL derivation (S5-D2), the adapter compute, and both S5-D1 artifact writes with their fsync. Stage 1c calls **that** callable, never a harness copy, and `run_worker` calls it without an override |
| SR-4 | The S5-D1 writer (prefix written and fsynced before the expansion decision; final written and fsynced after) is the same function in the route and in Stage 1c. It writes to a directory argument |
| SR-5 | A producer of **genuine staged N2 capture bytes** for the TEST_ONLY composition, generated by S4's own N2 compute and capture code, not a hand-written vector, and bound to the contract the harness uses. The adapter's own "mismatched N2 FULL baseline" tests (packet §3) need the same input |
| SR-6 | The worker's own `PhaseBudgetGuard` (`worker.py:156-200`) is constructable with measurement limits (`cpu_ns = wall_ns = 3600 s`, `memory_bytes` above the runner's memory). The per-replay budget checks then run production code, and the pilot predicate cannot abort. The limits are inputs, not a seam |
| SR-7 | The RC-6 re-anchored packet states an explicit, scoped exception at each of its four tolerance sites: the Authority line "no tolerance relaxed" (packet line 8), §2 Forbidden "accepted formulas and tolerances" (line 35), §3 "never a relaxed tolerance" (line 49) and §6 Forbidden "a relaxed tolerance" (line 61). The exception covers the SR-1 measurement override only; it is never a route value, a contract value or a statistic |
| SR-8 | (Stage 2, carried from r1 `:216`.) S5's run evidence exports the PART_A settled observation fields: `cpu_ns`, `memory_peak_bytes`, `oom_events`, the boottime from reservation to `CAPTURED`, and the payload/guardian CPU split where available. They are read by `scripts/s2_run_evidence.py <run> --expect-head <sha>` |

### 7.5 PROPOSED proof obligations (S5 tests, node IDs named at C3; for CP-1a approval, item 2(e))

| ID | Obligation |
|---|---|
| P-1 | **Refused under production authority.** An OPERATOR-domain contract, or any contract failing the §7.3 gate, together with an override raises before `verify_for` is called (spy) and before any file exists in the output directory. P-1 is defence in depth only: it does not exclude the signed TEST_ONLY route (§7.3) |
| P-2 | **Closed value.** `PartAMeasurementOverride(within_pp=x)` is refused for every `x ≠ 1.0` |
| P-3 | **Unreachable from the route (static and spy; with P-4 and P-5, the sole signed-route exclusion proof).** An AST test asserts that under `ops/` only `execution/compute.py` defines or tests the override, and that `worker.py`, `service.py`, `campaign_supervisor.py`, `g5.py` and `campaign_protocol.py` never construct it. A spy test asserts that `run_worker`'s PART_A path calls the SR-3 callable with `measurement_override=None` |
| P-4 | **Absent from signed documents.** The closed key sets of the `/v7` release and profile, the campaign plan, the checkpoint plan and the `/v8` snapshot are pinned, and each parser refuses a document with an added `measurement_override` or `within_pp` key |
| P-5 | **Not adjudicable.** On (2, 4, 2), a forced-expanded result is refused by the PART_A G5 reconstruction as "unnecessary expansion" (packet §3). The existing result adjudicator already refuses a panel count that differs from the frozen expansion decision (`result_adjudication.py:417-420`). An escaped forced artifact therefore cannot yield `CONTINUE` |
| P-6 | **Faithful.** With the override, the initial-prefix artifact is byte-identical to the one produced without it, on the same fixture |
| P-7 | **Same code.** Stage 1c's entry point is the SR-3 callable object that `run_worker` uses (identity asserted in the harness record) |

### 7.6 Stage 1c measured boundary

The boundary opens at the first byte read of the staged N2 capture and closes when the second artifact's fsync returns. Inside it:
- the N2 FULL derivation;
- `verify_for`;
- the pilot and all four panels;
- both artifact writes and fsyncs;
- the worker's per-replay budget checks.

Source admission and `start` are charged as in Stage 1b. Outside it, as setup: generating the staged N2 bytes (SR-5) and the fixture. Also outside it: the bundle verification and plan derivation that `run_worker` performs before the SR-3 body. That residual is disclosed; the Stage 2 service figure includes it, so it lands in PA-5's k.

### 7.7 BLOCKED rule

Stage 1c is **not** BLOCKED at this revision: the seam is specified. Production authority cannot reach it (the §7.3 gate and P-1). The signed TEST_ONLY route satisfies the gate, so its exclusion is proved only by P-3, P-4 and P-5 (§7.3). At C3, if the built adapter lacks any of SR-1..SR-6, or any of P-1..P-7 fails, Stage 1c returns **BLOCKED**, with this section as the proposed seam. A missing or failing P-3, P-4 or P-5 is always BLOCKED, never waived, because nothing else proves that no signed route can reach the seam. RC-3b then stays unmet and S5 acceptance cannot proceed. No stand-in substitutes for it.

## 8. Acceptance condition 2: complete aggregate-memory evidence

### 8.1 The shared footprint

PA-3 compares against the **one shared campaign memory footprint**:
- the profile's `memory_bytes` = 256,000,000 (`deploy/qualification/test-profile.json`; it is carried unchanged into the diagnostic profiles as a `_LIMITS` field, `profile.py:30`, `:261`);
- the TEST_ONLY binding's `maximum_memory_bytes` = that same value for v3–v6 (`fixture_producer.py:96`, `:156`). For any other release the default binding sets it to `memory_limit*9//10` = 230,400,000 bytes (`:152-153`; arithmetic). **PA-3's 256,000,000 therefore holds only with the P4 tuple extended to `/v7`.** Unextended, the binding itself is `BUDGET_EXHAUSTED` (P4), so PA-3 would not be reached.

The service compares the campaign-parent cgroup's aggregate `memory.peak` against the binding's `maximum_memory_bytes`, not the profile's `memory_bytes` (`campaign_supervisor.py:82` "The parent supplies aggregate peak/OOM", `:974`; `campaign_store.py:2980-2986`). It is never a per-phase value.

### 8.2 What is read on every timed repeat

- **(A) In-unit (primary).** As the harness's last act after the workload boundary closes, it reads its own cgroup path from `/proc/self/cgroup` (`0::/…/<unit>.service`). From that cgroup it reads `memory.peak`, `memory.swap.max`, `memory.swap.peak` (if present), `memory.events` and `cpu.stat`. `memory.peak` is hierarchical: it covers the `fp.py` launcher, the harness, and every descendant, including the launcher's environment-check subprocess (`scripts/fp.py:107`) and the command it launches (`:274`). The read is complete only if the path ends in the repeat's own unit name.
- **(B) systemd (secondary).** After the unit exits: `systemctl show -p MemoryPeak -p MemorySwapPeak -p CPUUsageNSec -p ControlGroup`.
- **Swap off.** Swap is off twice over: `sudo swapoff -a` at job start (recorded as `swapon --show` empty and `SwapTotal: 0 kB`), and `MemorySwapMax=0` on each unit (recorded as `memory.swap.max == 0`, where that file exists).
- **The repeat's M** is the larger of (A) and (B), whichever are present. It is **complete** if at least one is present, and swap is shown off.
- **Lower bound (never sufficient).** `ru_maxrss` via `production._peak_memory_bytes()` is always recorded as a lower bound; on Windows the lower bound is `PeakWorkingSetSize`.

Both reads include the setup and the file page cache charged to the cgroup, so they overstate the worker. The service's campaign-parent reading has the same page-cache semantics.

### 8.3 Consequences

- **Every timed repeat complete:** M̂ = the maximum over them, and PA-3 is applied. The record states `memory_feasibility = VERIFIED` if `m_m × M̂ ≤ 256,000,000`, or `FAILED` otherwise (FAILED goes to an operator ruling, §9 PA-3).
- **Any timed repeat with only the lower bound:** that job's record states `memory_feasibility = UNVERIFIED` and `rule_applicable = false`, and it is retained as it is. **The rule is not applied to that record**, CPU included, and the return says so. This follows the ruling: "A lower-bound memory fallback leaves memory feasibility unverified and cannot support the rule's application" (slices plan line 848). A lower bound never satisfies PA-3.
- **One re-run (CANDIDATE, under PA-4).** The job may be re-run once on a fresh runner (§12.7). A complete re-run produces a new record; it does not upgrade the retained one. The re-run itself is a CP-1a candidate (item 1, PA-4), not something the ruling grants.
- **Still UNVERIFIED after the allowed re-run:** memory cannot be shown complete on this runner class with this method. The rule cannot be applied, so RC-3a stays unmet, and build entry needs an operator ruling: for example, an alternative memory method or runner, or a ruled memory disposition. This is neither the D2 falsifier nor a PA-3 failure (§10.3).
- **Stage 1a (Windows) is always `UNVERIFIED`** for memory. It sets nothing.

### 8.4 Can the ubuntu-24.04 runner expose `memory.peak`?

| Fact | Evidence | Status |
|---|---|---|
| cgroup v2 `memory.peak` exists for non-root cgroups from Linux 5.19 | Kernel cgroup-v2 documentation (not re-read here) | UNVERIFIED here |
| The runner kernel is ≥ 5.19 | Ubuntu 24.04's GA kernel series is 6.8 (Canonical release information, not re-read here). The runner's kernel is not recorded in any repo record found (`grep` for kernel and systemd versions: no hit) | UNVERIFIED |
| `memory.peak` was readable on this runner class on 2026-09-25 | *Indirect, in-repo.* `test_s2_shared_memory_oom_is_retained_last` reads `(parent/'memory.peak').read_text()` (`test_campaign_supervision_linux.py:760-770`). It is in the S4 case set (`qualification_boundary_verification.py:40-41`, supervision file last), and the S4 acceptance runs 36180568493 and 36181780676 passed 22/22 (ledger, C2 close entry). Separately, a genuine N2 PASS needs a readable campaign-parent `memory.peak`, because a `None` peak makes the campaign `BUDGET_UNCERTAIN` (`campaign_store.py:2970-2971`). The run artifacts themselves were not read | Indirect; artifact UNVERIFIED |
| systemd 255 populates `MemoryPeak` for an exited `RemainAfterExit` transient unit, and keeps the unit's cgroup until stop | Not established | UNVERIFIED. (A) does not depend on it |
| The runner has swap enabled by default | Not established | UNVERIFIED. `swapoff -a` makes it moot |

**The dry run must confirm it** (§12.3 step 6): a probe unit whose parent spawns a child that allocates and touches 64 MiB and exits, after which the parent reads (A). The probe passes only if:
- (A) ≥ 67,108,864 bytes, which proves the descendant is included;
- `SwapTotal` is 0;
- `CPUUsageNSec` is populated.

Whether (B) is populated is recorded. The probe runs in every job, before any timed repeat.

## 9. Margin rule (scope RULED: PART_A only, TEST_ONLY; every parameter a CANDIDATE)

**Symbols:**
- Ĉ, Ŵ, M̂: forced-arm maxima over timed repeats, cold included; Ĉ and Ŵ are workload values (setup excluded).
- D̂: the derivation plus the real artifacts, uncovered until Stage 1c, whose forced-arm maximum Ĉ₁c replaces Ĉ + D̂.
- P̂: the forced-arm maximum of `predicted_seconds`.
- O: the 20 s orchestration charge (`profile.py:212`).
- L: the launch allowance.
- Ceilings round **up** to whole 10 s.

| Rule | Formula | CANDIDATE |
|---|---|---|
| **PA-1 CPU** | `B = max(m_c × (Ĉ + D̂), 1.5 × P̂)`; `cpu_ns(PART_A) = max(120 s, B + O)`. Before Stage 1c, D̂ is uncovered, the value is **provisional**, and no acceptance-grade run relies on it. After Stage 1c: `B = max(m_c × Ĉ₁c, 1.5 × P̂₁c)` | m_c = 2.0 |
| **PA-2 wall** | `wall_ns(PART_A) = max(300 s, m_w × (Ŵ + L))`, with m_w ≥ m_c ÷ (m_c − 1); Ŵ comes from Stage 1c when it exists | m_w = 3.0; L = 30 s until Stage 2 measures it |
| **PA-2b engine predicate** | `P̂ × wall ÷ B ≤ wall ÷ 1.5`, guaranteed by PA-1's `1.5 × P̂` term | — |
| **PA-3 memory** | `m_m × M̂ ≤ 256,000,000` (the binding's `maximum_memory_bytes`, which equals 256,000,000 only with the P4 tuple extended to `/v7`; §8.1), where M̂ is from **complete** aggregate readings only (§8). A failure goes to an operator ruling; this rule never sets a per-phase memory value | m_m = 1.5 |
| **PA-4 validity** | No application from a record that fails §6.2 (digests, prefix, spread) or §8.3 (memory completeness) | spread 1.30; one re-run |
| **PA-5 Stage-2 consistency** | `k = service ÷ harness`. *Service* is the Stage 2 PART_A payload CPU if separated, else the whole settled charge. *Harness* is the Stage 1c **prescribed**-arm maximum workload CPU (derivation and real artifacts included). If k > 1.25, re-apply PA-1/PA-2 with Ĉ₁c × k and Ŵ × k | 1.25 |

**Why these values** (r1 `:263-275`, kept):
- A throttled payload of CPU Ĉ finishes its CPU-bound part in `wall ÷ m_c`, hence m_w ≥ 2. The value 3 adds headroom.
- The 2026-09-24 CPU spreads were 1.04–1.08; the wall spread was 1.72 with a cold first repeat.
- Asymmetry: too tight means a silent SIGKILL and IN_DOUBT; too loose costs only Σ headroom.
- The M13 precedent gave N2 1.61× its Windows figure (arithmetic: 340 s ÷ 211.39 s).

**Sensitivity** (arithmetic, m_c = 2, O = 20 s). The shared 120 s suffices while Ĉ + D̂ ≤ 50 s and P̂ ≤ 66 s; the shared 300 s wall suffices while Ŵ + L ≤ 100 s.

| Ĉ + D̂ (s) | 25 | 50 | 60 | 100 | 211 |
|---|---|---|---|---|---|
| PART_A CPU ceiling (s) | 120 | 120 | 140 | 220 | 450 |

**Re-measurement triggers** (r1 `:285-291`, kept):
1. a change to the worker runtime closure or the lock;
2. a workload change;
3. a reference-runtime change;
4. a change to O or `CAMPAIGN_RESOURCE_SCOPE`;
5. a Linux PART_A charge above 0.8 × B, a wall above 0.8 × the ceiling, or any overrun or OOM;
6. k > 1.25.

## 10. Budget feasibility (arithmetic on proposed `/v7` values: RULED 2026-09-27 as the pre-build feasibility)

### 10.1 The code check at binding

`campaign_store.py:2776-2783`:
- Σ phase `cpu_ns` ≤ cap;
- Σ phase `wall_ns` ≤ cap;
- max phase `memory_bytes` ≤ cap.

The void term is zero at binding (`:2794-2801`).

### 10.2 Inputs and arithmetic

The inputs:
- the `/v6` diagnostic set (`profile.py:207-252`): 12 phases, 11 × 120 + 360 = 1,680 s CPU and 11 × 300 + 900 = 4,200 s wall;
- the TEST_ONLY cap of 10,000 s CPU / 10,000 s wall / 256,000,000 bytes memory, **provided the P4 tuple is extended to v7** (unextended: 120 s / 180 s / 230,400,000 bytes, and binding fails, P4);
- **N2 at 360 s / 900 s, which assumes CP-1a item 3 extends M13 to `/v7`**. For any other N2 ruling, shift the constants 1,560 and 3,900 below by (N2 CPU − 360) and (N2 wall − 900).

| Allowance included (cumulative) | CPU feasible iff | Wall feasible iff | Ĉ limit, PA-1 | (Ŵ + L) limit, PA-2 |
|---|---|---|---|---|
| Σ phases (the code check) | 1,560 + X ≤ 10,000 → X ≤ 8,440 | 3,900 + Y ≤ 10,000 → Y ≤ 6,100 | 4,210 s | 2,033 s |
| + one signing retry of a 120 s / 300 s phase (compute phases cannot retry, `:2887`) | X ≤ 8,320 | Y ≤ 5,800 | 4,150 s | 1,933 s |
| + D3's two future compute re-executions (not S5) | 1,680 + 3X ≤ 10,000 → X ≤ 2,773 | 4,200 + 3Y ≤ 10,000 → Y ≤ 1,933 | 1,376 s | 644 s |

The Σ-only row allows about 168× the ~25 s estimate before failing (arithmetic: 4,210 ÷ 25). The application entry states two gaps: Σ counts one reservation per phase, and no code checks wall slack between works.

### 10.3 D2 falsifier (owner: S5 draft §2.3)

The owner text in full ([S5 decision draft](2026-09-26-s5-decision-draft.md) line 228): "**Falsifier:** revisit the uniform model if PART_A's maximum-expansion CPU cannot be bounded ahead of time. That would mean a ceiling covering maximum expansion either fails the Σ-feasibility check against any admissible cap or cannot be measured before S5 is released."

It has two limbs. r2 classifies them as follows. This follows the H1 card's stop classification (handoffs lines 116-121: "Σ arithmetic fails at every admissible value … the last is the D2 falsifier"), which names the stop class returned during step (b). The card does not amend the owner's definition, and neither does this note.

- **Open** until a valid Stage 1b record exists (review correction, kept).
- **Σ limb: the stop class D2 ACCOUNTING-DESIGN FALSIFIER.** It fires only if Σ is infeasible at every admissible value. That means: from a record with `validity.ok = true` and complete memory, the Σ-only row fails even at the least-headroom point the approved rule admits. At the candidates, that is Ĉ (or Ĉ₁c) > 4,210 s, or Ŵ + L > 2,033 s (arithmetic). At C3 the same test is the executed `bind_budget` on the built `/v7` (RC-3b).
- **Measurement limb ("cannot be measured before S5 is released"): live.** An INVALID MEASUREMENT (PA-4 failed twice, digest or prefix mismatch), a Stage 1b that is not approved, or one that cannot run does not fire D2 when it happens: it says nothing about the accounting design, and a fresh approval can re-attempt the measurement. But if **no valid Stage 1b record exists at the release point**, this limb engages, unless the operator sets the PART_A ceiling by ruling (which would also amend the measurement requirement, as r1 `:329` noted for RC-3; under the split, RC-3a). r1 made three events immediate triggers: no valid measurement after two attempts, differing digests, and Stage 1b not approved or unable to run before release (`:326-329`). The fix round repeated the third (`8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md:61`). **r2 changes their timing, not their existence**: each engages the measurement limb at the release point if no valid record exists by then, rather than on the event itself. Under the 2026-09-27 split the release point is taken to be the hold-release entry (CP-1b). That mapping is r2's reading and is not ruled. Both points are returned as CP-1a item 4.
- **Memory UNVERIFIED after the allowed re-run** (§8.3) is neither limb: the falsifier concerns CPU. It leaves RC-3a unmet, and build entry needs an operator ruling (§8.3, §12.7).
- **Production:** out of scope, flagged as in r1 `:330`. Per-call growth over 40,203 calls is not established.

## 11. RC status on the 2026-09-27 split

The conditions are the ledger's ([direction table](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27), slices plan lines 828-830), cited by line, not restated as a second owner. The third column holds r2's additions. None of them changes a ledger condition: each is either PROPOSED for approval at CP-1a or labelled as r2's derivation from a ruling.

| Stage | Condition (ledger wording, slices plan) | r2 additions (not ledger text) | Status at `521d8f2` | Evidence / next action |
|---|---|---|---|---|
| **Build entry** | **RC-1**: "D1–D3 ruled" (line 828) | — | **Met** | #517 merged at `5ad04cf` (`git merge-base --is-ancestor 5ad04cf HEAD`: yes) |
| | "**The §3.4(d) text** applied (S5 draft §4, consistency correction)" (line 828) | — | Open | The proposed sentence ("a spec §2.6 bounded same-sample re-execution is not a draw") is absent from the slices plan (`grep`: no hit) |
| | "**RC-4/RC-5 assignment**: the seed-view owner and slice, with the F1 admission-check text, and an owner, gate and record location for each of OF-1..OF-7, resolving S5 draft §6 Q12" (line 828) | — | Open | Handoff H7 is producing `docs/notes/2026-09-27-host-obligations-assignment.md` (forthcoming, status open); the coordinator records it in the ledger (line 843) |
| | "**RC-6**: the packet re-anchored at the release head, including #519's findings that the (2, 4, 2) fixture cannot expand and the three `/v7` profile pitfalls" (line 828) | **PROPOSED (CP-1a item 2(e)):** the re-anchored packet also carries SR-1..SR-8 and P-1..P-7 (§7.4, §7.5), including the SR-7 exception at the packet's four tolerance sites | Open | After §3.4(d) |
| | "**RC-3a**: an operator-approved measurement-and-margin rule; a valid (PA-4) record from an operator-approved forced-expansion measurement of the **existing** `_run_part_a` on the reference runtime (#519 Stage 1b); the rule applied as a **provisional** PART_A TEST_ONLY ceiling, with D̂ uncovered; Σ-feasibility shown as **arithmetic on the proposed `/v7` values** (#519 proposal §5)" (line 828) | **Derived from the 2026-09-27 ruling's condition (2)** (line 848: a lower-bound fallback "cannot support the rule's application"): the record must have complete memory, or the rule cannot be applied. **Derived from the 2026-09-27 ruling** (line 845: the N2 ceiling "cannot come from the rule"): the §10 arithmetic needs a proposed `/v7` N2 value, and this note proposes that it come from the separate ruling (CP-1a item 3). A proposed value suffices for the arithmetic | Open | CP-1a, then Stage 1b, then the §13 application |
| | "Then an operator hold-release entry here" (line 828) (**CP-1b**) | — | Open | After all of the above |
| **C3 and acceptance** | "The S5 packet's C3 items" (line 829) | — | Open | — |
| | "**RC-3b**: the adapter-specific measurement (#519 Stage 1c), which covers D̂ and ends the provisional status; the **executed** `bind_budget` Σ-feasibility check on the built `/v7` profile; the Stage 2 service-route consistency check (PA-5)" (line 829) | **PROPOSED (CP-1a item 2(e)):** Stage 1c through the forcing seam of §7 | Open | At C3, within the approved rule |
| | "The full RC-2 owner-text set accepted and applied" (line 829) | — | Open | — |
| **Before F1** | "The RC-4 seed-view change landed, with its F1 admission check; OF-1..OF-7 attested by attended reads; K3 built" (line 830) | — | Open | — |

**No S5 release proposal is supported:** RC-3a, RC-4/RC-5 assignment, RC-6 and §3.4(d) are open.

## 12. Measurement dispatch: one approval packet for CP-1a

**Common limits:**
- TEST_ONLY synthetic only;
- no qualification service, secret, vendor or account contact, or trading-service network call;
- output class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`;
- no profile, ceiling or release-literal edit (those land with the S5 build);
- a failed repeat is retained, never dropped;
- no push to the dispatched branch while a run is in flight.

### 12.1 Stage 0: S4 run artifacts, calibration only (deadline about 2026-10-09)

- **When:** immediately after CP-1a. The artifacts are retained for 14 days (`retention-days: 14`, `qualification-s2-supervision.yml:179`). The expiry of about 2026-10-09 is taken from the H1 card (handoffs line 96) and the #519 coordinator review (`8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md:72`). It implies creation on about 2026-09-25 (arithmetic: 2026-10-09 − 14 days). The runs' `createdAt` was **not read** and is UNVERIFIED: a 2026-09-24 creation would give about 2026-10-08. The `gh run view` step records `createdAt`, and the return states the exact expiry.
- **Grant:** artifact download (operator approval at CP-1a). It makes network calls to the GitHub API only.
- **Commands:**
```bash
S=<scratch>/s5-stage0; D=docs/notes/<date>-s5-part-a-measurement/stage0; mkdir -p "$S"
for run in 36180568493 36181780676; do
  gh run view "$run" -R Joshua-Asante/first-passage --json databaseId,headSha,createdAt,conclusion > "$S/$run.json"
  gh run download "$run" -R Joshua-Asante/first-passage -n qualification-s2-supervision -D "$S/$run"
done
( cd "$S" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum ) > "$S/SHA256SUMS"
grep -hE "Consumed .* CPU time|memory peak" "$S"/*/journal.log "$S"/*/systemd-units.log > "$S/lines.txt" || true
grep -rhoE '"memory_peak_bytes": *[0-9]+' "$S" | sort | uniq -c > "$S/memory_peak.txt" || true
# public-clone review, before anything enters the repository: read every extracted line
less "$S/lines.txt" "$S/memory_peak.txt"
# only after the review finds nothing but unit names, CPU times and byte counts:
mkdir -p "$D"
jq -s . "$S"/36180568493.json "$S"/36181780676.json > "$D/runs.json"
cp "$S/SHA256SUMS" "$S/lines.txt" "$S/memory_peak.txt" "$D/"
```
- **Files created:** in scratch, `$S/<run>.json`, `$S/<run>/…` (the raw artifacts), `$S/SHA256SUMS`, `$S/lines.txt` and `$S/memory_peak.txt`. In the repository, only after the review: `docs/notes/<date>-s5-part-a-measurement/stage0/{runs.json,SHA256SUMS,lines.txt,memory_peak.txt}`, where `runs.json` merges the two run-metadata files. The raw logs stay outside the repository and only their hashes are committed. The logs have not been read, so whether their extracted lines are fit for a public repository is UNVERIFIED until the review step. A line that names a host path, account, token or anything beyond a unit name, CPU time or byte count is dropped from the committed copy, and the drop is recorded.
- **Limits:** read-only, one download per run, no re-run.
- **Stop:** artifacts expired or missing. Record `UNAVAILABLE`; nothing downstream depends on Stage 0.
- **Output:** the Linux N1/N2 unit CPU and memory lines, if logged, paired with the Windows 13.36 s and 211.39 s figures. **It sets no ceiling, and it cannot supply the `/v7` N2 value.** It informs F5 and the operator's N2 ruling.

### 12.2 Stage 1a: Windows harness validation

- **Grant:** `tests.run` and `worktree.write` on the executing seat's Windows host. No CI change.
- **Commands:**
```powershell
.\fp.ps1 doctor
.\fp.ps1 python docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py.txt --launcher --stage 1a --arms forced,prescribed --repeats 5 --out docs/notes/<date>-s5-part-a-measurement/windows.json
.\fp.ps1 python docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py.txt --summarize docs/notes/<date>-s5-part-a-measurement/windows.json --stage 1a
```
- **Files created:** the harness `.py.txt` and `windows.json` (`platform_accounting = windows_process_time_job_object`, `memory.complete = false`).
- **Limits:** about 12 processes (planning ≤ 20 min, arithmetic from the §4 estimate).
- **Stop:** a harness defect; fix and re-run locally. It is not a validity-check count.
- **Output:** harness validation only: panel counts forced 4 / prescribed 2, digest identity, prefix identity, and all fields populated. It sets no value.

### 12.3 Stage 1b: new workflow file and two-job Linux run (the reference measurement)

**Grants** (each needs operator approval at CP-1a):
- (i) a CI-configuration change: the new workflow file;
- (ii) `ci.dispatch` for this workflow only;
- (iii) download of this workflow's own artifacts.

**Dispatchability (UNVERIFIED):** GitHub's documentation states that a `workflow_dispatch` workflow must exist on the default branch to be triggered. The file would therefore land on `main` by operator merge before any dispatch. Being dispatch-only, landing it runs nothing.

**Workflow file:** `.github/workflows/qualification-s5-part-a-measurement.yml`. It is **described, not created**; step (b) writes it after CP-1a.
- `name: Qualification S5 Part A measurement (TEST_ONLY, dispatch only)`.
- `run-name: S5 Part A measurement [stage ${{ inputs.stage }}, ${{ inputs.mode }}] (${{ github.ref_name }})`.
- **Triggers:** `on: workflow_dispatch` **only**. There are no `push`, `pull_request` or `schedule` triggers. Inputs:
  - `stage`: choice `1b | 1c`, default `1b`;
  - `mode`: choice `dry-run | measure`, default `dry-run`;
  - `note_dir`: string, required.
- **Settings:**
  - `permissions: contents: read`;
  - `concurrency: group: s5-part-a-measurement-${{ github.ref }}`, `cancel-in-progress: false`.
- **Job `measure`:**
  - `runs-on: ubuntu-24.04` and `timeout-minutes: 120`;
  - `strategy: fail-fast: false`, with `matrix: job: ${{ fromJSON(inputs.mode == 'dry-run' && '["a"]' || '["a","b"]') }}`;
  - `env`: `STAGE`, `MODE` and `NOTE_DIR` come from the inputs, through `env` only, never interpolated into scripts; `ARM_ORDER` is `forced prescribed` for job `a` and `prescribed forced` for job `b`; `OUT` is `$RUNNER_TEMP/s5-part-a-measurement`.
- **Steps:**
  1. `actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5`, the pin the S2 workflow uses.
  2. **Validate inputs.** `NOTE_DIR` must match `^docs/notes/[0-9]{4}-[0-9]{2}-[0-9]{2}-s5-part-a-measurement$` and contain `measure_part_a_max.py.txt`. Record `git rev-parse HEAD` (and, for `stage=1c`, `git rev-parse HEAD^`), and require an empty `git status --porcelain`. Checkout depth must be at least 2 for `HEAD^` (`fetch-depth: 2` on step 1).
  3. **Swap off and host facts:** `sudo swapoff -a`. Then write to `$OUT/host-facts.txt`: `uname -r`, `systemctl --version | head -1`, `stat -fc %T /sys/fs/cgroup`, `cat /sys/fs/cgroup/cgroup.controllers`, `grep -m1 'model name' /proc/cpuinfo`, `nproc`, `grep SwapTotal /proc/meminfo`, `swapon --show`.
  4. **Provision**, exactly as S2 (`qualification-s2-supervision.yml:104-107`): `sudo /bin/bash tools/qualification_verification/provision.sh --manifest-output "$RUNNER_TEMP/qualification-manifest"`.
  5. **Doctor**, as S2 (`:130-135`): derive `host_root` from the manifest, then run `sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" doctor`.
  6. **Accounting probe** (every job, before any timed repeat). A transient unit `fp-s5pa-probe` with `-p MemoryAccounting=yes -p CPUAccounting=yes -p MemorySwapMax=0 -p RemainAfterExit=yes` runs `$host_root/env/bin/python -I -c` with an inline script. The script spawns a child that allocates and touches 64 MiB and exits, then reads its own cgroup's `memory.peak`, `memory.swap.max` and `cpu.stat`. Then `systemctl show -p MemoryPeak -p MemorySwapPeak -p CPUUsageNSec -p ControlGroup fp-s5pa-probe`. Write `$OUT/probe.json`, and exit 3 unless in-unit `memory.peak` ≥ 67,108,864, `SwapTotal` = 0 and `CPUUsageNSec` is populated.
  7. **Measurement loop.** In `dry-run` mode it runs one untimed repeat per arm, labelled `dry_run`. In `measure` mode it runs the loop below.
  8. **Summarize:** `sudo "$host_root/env/bin/python" -I scripts/fp.py --env "$host_root/env" python "$NOTE_DIR/measure_part_a_max.py.txt" --summarize "$OUT" --stage "$STAGE" --job "${{ matrix.job }}" --run-id "$GITHUB_RUN_ID"`. It writes `$OUT/record.json` and exits 0, 3 or 4 (§6.3).
  9. **Owned cleanup**, `if: always()`, as S2 (`:143-171`): `sudo /usr/bin/python3 -I tools/qualification_verification/cleanup.py --manifest "$manifest"`. The journal is exported to `$OUT/journal.log` and ownership fixed with `chown`.
  10. **Upload**, `if: always()`, with `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02`: `name: s5-part-a-measurement-${{ inputs.stage }}-${{ matrix.job }}`, `path: ${{ runner.temp }}/s5-part-a-measurement/`, `retention-days: 14`.

**Measurement loop (step 7, `measure` mode):**
```bash
set -euo pipefail
PY="$host_root/env/bin/python"; H="$NOTE_DIR/measure_part_a_max.py.txt"
for arm in $ARM_ORDER; do
  for r in 1 2 3 4 5 0; do            # r=1 cold, timed, included; r=0 instrumented, last, excluded
    if [ "$r" = 1 ]; then
      find "$GITHUB_WORKSPACE" -name __pycache__ -type d -prune -exec sudo rm -rf {} +
      sync; echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
    fi
    unit="fp-s5pa-$STAGE-$arm-$r"
    sudo systemd-run --unit="$unit" --working-directory="$GITHUB_WORKSPACE" \
      -p CPUAccounting=yes -p MemoryAccounting=yes -p MemorySwapMax=0 -p RemainAfterExit=yes \
      -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 -E NUMEXPR_NUM_THREADS=1 \
      "$PY" -I scripts/fp.py --env "$host_root/env" python "$H" \
        --repeat-mode --stage "$STAGE" --arm "$arm" --repeat "$r" --unit "$unit" --out "$OUT/$arm-$r.json"
    until [ "$(systemctl show -p SubState --value "$unit")" = exited ] || \
          [ "$(systemctl show -p ActiveState --value "$unit")" = failed ]; do sleep 1; done
    systemctl show -p CPUUsageNSec -p MemoryPeak -p MemorySwapPeak -p ExecMainStatus -p ControlGroup \
      -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic "$unit" > "$OUT/$arm-$r.unit"
    sudo systemctl stop "$unit"; sudo systemctl reset-failed "$unit" 2>/dev/null || true
  done
done
```

**Dispatch commands (step (b), after CP-1a and after the workflow file is on `main`):**
```bash
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref <measure-branch> \
  -f stage=1b -f mode=dry-run -f note_dir=docs/notes/<date>-s5-part-a-measurement
gh run watch <run_id> -R Joshua-Asante/first-passage --exit-status
gh run download <run_id> -R Joshua-Asante/first-passage -D <scratch>/s5-1b-dry
# only if the dry run fails a re-runnable check (I-1 or I-6), once per stage: re-dispatch the same dry run
# after a clean dry run:
gh workflow run qualification-s5-part-a-measurement.yml -R Joshua-Asante/first-passage --ref <measure-branch> \
  -f stage=1b -f mode=measure -f note_dir=docs/notes/<date>-s5-part-a-measurement
gh run download <run_id> -R Joshua-Asante/first-passage -D <scratch>/s5-1b
# only if a job exits 3 (a re-runnable validity failure), once per stage; it re-runs every failed job (up to both):
gh run rerun <run_id> -R Joshua-Asante/first-passage --failed
```

**Files created by step (b):**
- the workflow YAML above;
- `docs/notes/<date>-s5-part-a-measurement/measure_part_a_max.py.txt`;
- `docs/notes/<date>-s5-part-a-measurement/stage1b/<run_id>-<job>/{record.json,probe.json,host-facts.txt,<arm>-<r>.json,<arm>-<r>.unit}`;
- a short note `docs/notes/<date>-s5-part-a-measurement/README.md`.

**Output:** Ĉ, Ŵ, M̂ and P̂ for the forced arm, the prescribed anchor, the validity and memory verdicts, and the stop class.

### 12.4 Stage 1c: at C3, through the built adapter

- **When:** at S5 packet Checkpoint C3, before any acceptance-grade run relies on the ceiling.
- **Preconditions:** SR-1..SR-6 built and P-1..P-7 passing, with node IDs in the C3 return (§7). Otherwise **BLOCKED** (§7.7).
- **Grants:** `ci.dispatch` of the same workflow and download of its artifacts. If approved at CP-1a, the dispatch is executed at C3. The approval is **conditional**: the harness gains its `--stage 1c` path only at C3, so the operator would otherwise approve code that does not yet exist. Before the Stage 1c dispatch the coordinator reads the harness diff (the `--stage 1c` path against the Stage 1b harness) and records that read. Without that record the dispatch is not made.
- **Where the harness lives:** the S5 packet's §2 file list (packet line 35) does not include `docs/notes/…`, and its executor is the single writer for those files. The harness therefore stays **off** the S5 branch. It is committed on a separate measurement branch based on the S5 head (`<S5 head>` plus the harness commit only), and Stage 1c is dispatched with `--ref` on that branch. The record's `dispatched_head` is the measurement-branch head. For `stage=1c`, step 2 of the workflow also records `git rev-parse HEAD^`, and the coordinator checks that it equals the S5 head reported at C3. A mismatch is treated as I-7.
- **Repeat body.** Steps 3–6 of §6.3 are replaced by:
  - setup (excluded): the composition fixture and SR-5's staged N2 capture bytes copied into a repeat-local input directory;
  - boundary open;
  - the SR-3 callable, with `PhaseBudgetGuard` measurement limits (SR-6) and `measurement_override = PartAMeasurementOverride(within_pp=1.0)` for `forced` or `None` for `prescribed`, writing to a repeat-local output directory;
  - boundary close;
  - assertions: forced `expanded` true with 4 panels, prescribed 2; the S5-D1 prefix assertion (`final[:len(initial)] == initial`, packet §3); the forced initial-prefix bytes equal to the prescribed ones; the object identity of P-7;
  - the in-unit memory read.
- **Commands:** as §12.3, with `--ref <measurement branch on the S5 head> -f stage=1c`: a dry run (at most one re-dispatch of a failed dry run), then `measure`, then at most one `--failed` re-run (§12.7).
- **Files created:** `docs/notes/<date>-s5-part-a-measurement/stage1c/<run_id>-<job>/…`, with the same layout plus `n2_capture_sha256` and the two artifact digests per repeat.
- **Output:** Ĉ₁c, Ŵ₁c, P̂₁c and M̂₁c. They cover D̂ and end the provisional status (§13 step 6).

### 12.5 Stage 2: service-route consistency at C3 (no new authority)

- **What:** read the genuine S5 Linux campaign's PART_A settled observation (SR-8) from the acceptance-grade run the S5 C3 route already dispatches: `python scripts/s2_run_evidence.py <run_id> --expect-head <sha> --expect-scope <the S5 scope S5 registers>`. The scope name is UNVERIFIED because S5 adds it.
- **PA-5:** `k = service ÷ Stage 1c prescribed maximum`.
- **Memory:** `memory_peak_bytes` is the campaign-parent aggregate (`campaign_supervisor.py:974`). It is recorded against the binding's `maximum_memory_bytes`: 256,000,000 if the P4 tuple is extended to `/v7`, or 230,400,000 under the default binding (`fixture_producer.py:152-156`; §8.1). The service itself ends the campaign `BUDGET_EXHAUSTED` above that binding value (`campaign_store.py:2980-2986`). The record states which binding value applied.
- **Files created:** `docs/notes/<date>-s5-part-a-measurement/stage2.json`.

### 12.6 Runner time (arithmetic; a planning bound, not a measurement)

Planning inputs:
- a per-repeat bound of 90 s, about 2× the Windows forced estimate of ~45 s (setup 10.4–12.4 s + workload 20–30 s + start);
- provisioning 6–8 min (S2 workflow comment at `:75`), taken as 8;
- checkout, doctor and probe 3 min;
- cleanup and upload 2 min.

| Dispatch | Per job (min) | Jobs | Runner-min | With the SR-5 contingency (+5 min per repeat) |
|---|---|---|---|---|
| 1b dry-run (2 untimed repeats) | 8 + 3 + 2 × 1.5 + 2 = 16 | 1 | 16 | 16 |
| 1b dry-run re-dispatch (at most one) | 16 | ≤ 1 | ≤ 16 | ≤ 16 |
| 1b measure (12 units) | 8 + 3 + 12 × 1.5 + 2 = 31 | 2 | 62 | 62 |
| 1b `--failed` re-run (at most one, up to both jobs) | 31 | ≤ 2 | ≤ 62 | ≤ 62 |
| 1c dry-run (+5 min N2 staging, +0.5 min per repeat) | 8 + 3 + 5 + 2 × 2 + 2 = 22 | 1 | 22 | 22 + 2 × 5 = 32 |
| 1c dry-run re-dispatch (at most one) | 22 | ≤ 1 | ≤ 22 | ≤ 32 |
| 1c measure | 8 + 3 + 5 + 12 × 2 + 2 = 42 | 2 | 84 | 2 × (42 + 12 × 5) = 204 |
| 1c `--failed` re-run (at most one, up to both jobs) | 42 | ≤ 2 | ≤ 84 | ≤ 204 |

All figures are arithmetic:
- **Nominal (no re-run):** 1b 16 + 62 = 78, and 1c 22 + 84 = 106, so **184 runner-minutes**. With the SR-5 contingency: 78 + (32 + 204) = **314**.
- **Worst case with every allowed re-run:** 1b 16 + 16 + 62 + 62 = 156, and 1c 22 + 22 + 84 + 84 = 212, so **368**. With the SR-5 contingency: 156 + (32 + 32 + 204 + 204) = 156 + 472 = **628**.
- The SR-5 contingency applies if SR-5's staged bytes must be regenerated per repeat (UNVERIFIED; it depends on S5's contract binding). A 1c measure job is then 42 + 60 = 102 min, which `timeout-minutes: 120` covers.
- Stage 0 and Stage 1a use no runner minutes.

### 12.7 Stop conditions and re-run limit

**Re-run cap (one statement, per stage).** Each failed validity check marked "Once" allows one re-run of the job that failed it, which is how r2 reads the card's "one per failed validity check" (handoffs line 102). Per stage (1b, 1c) that is operated as follows:
- at most **one re-dispatch of a failed dry run** (I-1 or I-6 in the dry run);
- at most **one `gh run rerun --failed`** of the measure dispatch. It re-runs every failed job (up to both), whatever failure classes caused it;
- any failure after that re-run stops the stage.

Both caps are CANDIDATES under PA-4 (CP-1a item 1). §12.6 budgets exactly these re-runs. Every stop returns to the coordinator at once. A failed or re-run job's evidence is retained.

| Class | Condition | Re-run? | Effect |
|---|---|---|---|
| **INVALID MEASUREMENT** | I-1: the probe fails (`memory.peak` below 64 MiB or absent, swap on, `CPUUsageNSec` empty) | Once (fresh runner) | Second failure: memory cannot be complete on this runner class, so memory is UNVERIFIED, the rule is not applicable, and the return says so. RC-3a then stays unmet, and build entry needs an operator ruling (an alternative memory method or runner, or a ruled memory disposition; §8.3). Neither D2 nor a PA-3 failure |
| | I-2: warm CPU spread > 1.30 in a job (PA-4) | Once | Second failure: stop (PA-4 failed twice); no ceiling |
| | I-3: any timed repeat without a complete aggregate memory reading | Once | The first record is retained as `memory_feasibility = UNVERIFIED`, `rule_applicable = false` (§8.3). Second failure: the same, and RC-3a stays unmet, so build entry needs an operator ruling (§8.3). Neither D2 nor a PA-3 failure |
| | I-4: artifact digests differ between repeats of an arm, or the forced prefix differs from the prescribed | **No** | Immediate stop; no ceiling; evidence against D3 R7 |
| | I-5: a panel-count or `expanded` assertion fails (forced ≠ 4, prescribed ≠ 2) | **No** | Immediate stop: a harness or seam defect |
| | I-6: a timed repeat exits non-zero, times out or OOMs | Once | The repeat is retained; the second failure stops |
| | I-7: the measured head differs from the dispatched head, or the tree is dirty | **No** | Immediate stop |
| | I-8 (1c): SR/P preconditions unmet | — | **BLOCKED** (§7.7) |
| **D2 ACCOUNTING-DESIGN FALSIFIER** (the owner's Σ limb) | From a **valid** record with complete memory, Σ is infeasible at every admissible value (§10.3) | — | Returned as the D2 falsifier: revisit the uniform model (S5 draft §2.3). Not a measurement failure |
| **PA-3 failure** | A valid, complete record has `m_m × M̂ > 256,000,000` (with the P4 tuple extended; §8.1) | — | An operator ruling (§9). Neither invalid nor D2 |

An INVALID MEASUREMENT does not fire the Σ limb and does not clear D2. If no valid Stage 1b record exists at the release point, for any reason (invalid measurement, non-approval or non-execution), the owner's measurement limb engages unless the operator sets the ceiling by ruling (§10.3; reconciliation is CP-1a item 4).

### 12.8 Record schema `s5-part-a-max-expansion-measurement/v2`

```text
schema, artifact_class = TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING, decision_bearing = false,
recorded_utc, measured_commit, tree_clean, dispatched_head, harness_sha256, source_sha256{path: sha},
stage = 1a | 1b | 1c, mode = dry-run | measure,
runtime{runtime_kind = host_venv | worker_image, os_id, os_release, kernel, systemd_version, arch, cpu_model,
        logical_cpus, implementation, python, executable_sha256, requirements_lock_sha256, thread_env,
        image_digest (required when worker_image, else null), platform_accounting, runner, run_id,
        run_attempt, job, arm_order, swap_total_kb},
probe{in_unit_peak_bytes, systemd_peak_bytes|null, cpu_usage_nsec|null, swap_off, ok},
forcing{seam = harness_request (1b) | adapter_measurement_override (1c), within_pp, label,
        adapter_callable_identity|null (1c)},
workload{fixture, idle=false, sessions, bars_per_session_per_leg, legs, outer_months, inner_block_sessions,
         horizon_sessions, initial_panels, expanded_panels, paths_per_panel, root_rng_namespace, recipe,
         arm, full_pass_rate_input|null, n2_capture_sha256|null (1c), expected{replays, verify_for}},
repeats[{repeat, cold, instrumented, dry_run,
         cpu{start, admission, setup_excluded, verify|null, part_a|null, serialize|null, adapter|null,
             workload, process_total}, unit_cpu_s|null, unit_cpu_workload_s|null,
         wall{outer, setup_excluded, workload},
         memory{complete, method = cgroup_in_unit | systemd_memory_peak | lower_bound_ru_maxrss |
                lower_bound_windows_working_set, in_unit_peak_bytes|null, systemd_peak_bytes|null,
                swap_max|null, swap_peak_bytes|null, cgroup_path|null, oom_events|null, lower_bound_bytes},
         panels, expanded, probe_seconds, predicted_seconds, elapsed_seconds,
         counts{replay, proof, verify_for}|null, initial_prefix_sha256, final_sha256, fsync_count|null,
         exit_code}],
summary{per arm: workload cpu/wall max, median, min; warm spread; cold ÷ warm median; memory max (complete only);
        digests_identical; prefix_matches_prescribed; memory_complete_all_timed_repeats},
verdict{validity_ok, memory_feasibility = VERIFIED | FAILED | UNVERIFIED, rule_applicable,
        stop_class = none | INVALID_MEASUREMENT | BLOCKED | D2_ACCOUNTING_FALSIFIER | PA3_FAILURE,
        reasons[]}
```

## 13. TEST_ONLY application procedure (after CP-1a only)

1. **Preconditions:**
   - the CP-1a ruling recorded as a dated ledger entry;
   - a Stage 1b record with `verdict.validity_ok = true`, `rule_applicable = true` and `memory_feasibility` other than `UNVERIFIED`;
   - a proposed `/v7` N2 value for the §10 arithmetic. A proposed value suffices for RC-3a's arithmetic (slices plan line 828). This note proposes that the value come from the separate operator ruling (CP-1a item 3), because the N2 ceiling "cannot come from the rule" (line 845). The ruled value is needed for the `profile.py:239` edit that lands with the S5 build (step 3).

   N2 is not set under this rule.
2. **Compute** X, Y and PA-3 from the record, with every input's record path and SHA-256 and every rounding. Mark X and Y **provisional (D̂ uncovered)**.
3. **Feasibility:** the §10 table with the applied X and Y. Include the `/v7` preconditions: the P4 cap tuple, and the three `profile.py` edits (`:219-226`, `:243-252`, `:239` with the ruled N2 value).
4. **Record** one ledger entry, "Coordinator application: PART_A TEST_ONLY diagnostic ceiling under the approved measurement-and-margin rule (date)". It gives the rule version, inputs, X and Y, whether the shared ceilings suffice, and feasibility. Its scope is the `/v7` TEST_ONLY diagnostic profile only, with no production value set or implied.
5. **Implement only if X or Y exceeds the shared ceiling.** Add a `/v7`-gated PART_A constant beside `_JOINT_N2_DIAGNOSTIC_PHASE` (`profile.py:211`), citing the entry. It lands with the S5 build, and the RC-6 packet gains the pointer.
6. **At C3:** run Stage 1c (§7), re-apply PA-1/PA-2 from Ĉ₁c, which ends the provisional status, then run Stage 2 and PA-5. A new value is a new profile revision and needs fresh attempts.
7. **Never** set a production ceiling or cap, a value outside the rule, or a value without a valid measurement under this procedure. Never apply the rule to a record with UNVERIFIED memory.

## 14. CP-1a decision list

**Already RULED 2026-09-27** ([ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27)); not asked again:
- the staged build-entry / C3 / before-F1 structure;
- **rule scope: PART_A only, TEST_ONLY**;
- **pre-build feasibility is arithmetic on the proposed `/v7` values**, and the executed `bind_budget` check is at C3 (RC-3b);
- the RC-4/RC-5 assignment may be made now (H7).

**For decision at CP-1a:**
1. **The rule's parameters.** Approve, amend or reject each CANDIDATE:
   - PA-1: m_c = 2.0, the `1.5 × P̂` term, the 120 s floor;
   - PA-2: m_w = 3.0, L = 30 s, the 300 s floor;
   - PA-2b: the check;
   - PA-3: m_m = 1.5 against 256,000,000, on complete aggregate memory only. That value holds only with the P4 tuple extended to `/v7`; the default binding is 230,400,000 (§8.1). No existing figure measures this workload (F7);
   - PA-4: spread 1.30; digest and prefix identity; memory completeness; the re-run caps of §12.7 (one re-dispatch of a failed dry run and one `--failed` re-run per stage, covering up to both jobs); and the one re-run of a memory-incomplete job, which the ruling does not itself grant (§8.3);
   - PA-5: k = 1.25.
2. **The measurement dispatch (§12), step by step:**
   - (a) **Stage 0**, an artifact download, calibration only; it must run before about 2026-10-09.
   - (b) **Stage 1a**, Windows harness validation.
   - (c) **Stage 1b:** the CI-configuration change (the new dispatch-only workflow file, landed on `main` by operator merge if GitHub requires that; UNVERIFIED), `ci.dispatch` for one dry run (at most one re-dispatch if it fails), one measure run and at most one `--failed` re-run (up to both jobs), and download of its own artifacts.
   - (d) **Runtime:** `host_venv` (recommended) or `worker_image` (§5.3).
   - (e) **Stage 1c at C3,** including the PROPOSED TEST_ONLY forcing seam as S5 build requirements SR-1..SR-8, the SR-7 exception at the packet's four tolerance sites (lines 8, 35, 49, 61), and proof obligations P-1..P-7. P-3, P-4 and P-5 are the sole proof that no signed route reaches the seam (§7.3). If approved at CP-1a, the dispatch is executed at C3, and only after the coordinator has read and recorded the `--stage 1c` harness diff. The harness sits on a separate measurement branch based on the S5 head, outside the S5 packet's file scope (§12.4).
   - (f) **Stage 2:** no new authority; it needs the SR-8 export.
   - Totals (arithmetic, §12.6): nominal 184 runner-minutes, and a worst case of 368 with every allowed re-run. With the SR-5 per-repeat regeneration contingency: 314 and 628.
3. **A separate ruling, not under the rule: the `/v7` N2 ceiling.** For example, extend the M13 "/v6 only" ruling (360 s CPU / 900 s wall in the TEST_ONLY diagnostic profile only; plan line 757) to `/v7`. Without it:
   - `profile.py:239` has no `/v7` value (P3);
   - the §10 arithmetic needs a proposed N2 value. A proposed value suffices for RC-3a's arithmetic (slices plan line 828), and this note proposes that it come from this ruling;
   - the `/v7` profile's N2 value in the S5 build has no owner (slices plan line 845).
4. **D2 falsifier reconciliation (operator or coordinator item; beyond the card's three items).** The owner text has two limbs (S5 draft line 228). The H1 card's stop list names only the Σ limb as "the D2 falsifier" (handoffs lines 116-121). The #519 fix round made non-approval an immediate trigger. r2 keeps the Σ limb as the step (b) stop class, keeps the measurement limb live, and moves its engagement to the release point, read as CP-1b (§10.3). Confirm or amend: (i) that timing, (ii) the mapping of "S5 is released" onto CP-1b, and (iii) whether a PART_A ceiling set by ruling answers the measurement limb.

## 15. Unverified and limits

- **Linux figures:** no Linux CPU, wall or memory figure for any stage has been read. Stage 0 artifacts are unread.
- **`memory.peak` on the runner:** only indirect in-repo evidence (§8.4). systemd `MemoryPeak` retention for an exited `RemainAfterExit` unit, the runner kernel and systemd versions, and swap defaults are UNVERIFIED. The dry-run probe confirms them.
- **GitHub `workflow_dispatch` on a non-default branch:** UNVERIFIED (vendor documentation, §12.3).
- **The worker-image option:** its build-context feasibility is UNVERIFIED (§5.3).
- **SR-3..SR-5 shapes:** the exact S5 callable and fixture names do not exist before the S5 build. §7 states requirements, not names, except the proposed `measurement_override` and `PartAMeasurementOverride`.
- **§12.6 minutes:** arithmetic from Windows estimates. The Linux per-repeat time is unknown.
- **Stage 1c boundary:** it excludes bundle verification and plan derivation before the SR-3 body; PA-5 carries that residual.
- **The cited N2 record** `20260924T034139Z-59ce3c4b7643` was not found. Its figures are cited from the ledger (line 756).
- **Guardian CPU** (`LimitCPU` 13 s) while archiving two Part A artifacts is observable only at C3.
- **Derived-text discrepancy for the coordinator (not edited here):** the addendum's CP-1a row (§4) still lists "optional Stage 1b-N2", which the H1 card removed (handoffs line 94) in applying the 2026-09-27 ruling.
- **D2 release point:** r2 reads "S5 is released" (S5 draft line 228) as the hold-release entry CP-1b. That reading is not ruled (CP-1a item 4).
- **Stage 0 run creation dates:** not read; the exact expiry is UNVERIFIED until `gh run view` records `createdAt` (§12.1).
- **Out of scope:** the production mapping, the production cap and N4.

## Verification of this note

Commands run (read-only) at `521d8f2`, working tree otherwise untouched:

```bash
git log --oneline -3; git status --short
git diff --stat 8c15f18 HEAD -- ops tests tools deploy scripts .github           # empty
git merge-base --is-ancestor 5ad04cf HEAD && echo 5ad04cf-on-HEAD                # 5ad04cf-on-HEAD
git show 8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md | cat -n
git show 8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md | cat -n
sed -n 205,260p ops/c1_rail/qualification/execution/profile.py
grep -n "fresh diagnostic execution profile required\|== 'qualification_execution_profile/v6'\|funding_intents='qualification_campaign_funding/v1'\|PART_A includes maximum expansion\|_DIAGNOSTIC_CONTROLLER_CPU_NS = " ops/c1_rail/qualification/execution/profile.py
sed -n 145,160p tests/integration/qualification_boundary/fixture_producer.py
sed -n 758,775p ops/c1_rail/qualification/contract.py
sed -n 20,55p ops/c1_rail/qualification/part_a.py; sed -n 135,215p ops/c1_rail/qualification/part_a.py
grep -n "within_pp" ops/c1_rail/qualification/part_a.py
sed -n 80,125p ops/c1_rail/qualification/production.py
cat -n ops/c1_rail/qualification/execution/compute.py
grep -rn "run_part_a_compute\|within_pp\|expansion_tolerance" ops/ tests/ --include=*.py
sed -n 400,421p ops/c1_rail/qualification/result_adjudication.py
grep -n "permits_synthetic\|production_workload_required\|TEST_ONLY" ops/c1_rail/qualification/trust_domain.py
sed -n 25,96p ops/c1_rail/qualification/execution/worker.py; sed -n 156,200p ops/c1_rail/qualification/execution/worker.py
sed -n 78,100p ops/c1_rail/qualification/execution/campaign_supervisor.py; sed -n 960,1015p ops/c1_rail/qualification/execution/campaign_supervisor.py
sed -n 2962,2990p ops/c1_rail/qualification/execution/campaign_store.py; sed -n 2774,2802p ops/c1_rail/qualification/execution/campaign_store.py; sed -n 2877,2897p ops/c1_rail/qualification/execution/campaign_store.py
sed -n 755,780p tests/integration/qualification_boundary/test_campaign_supervision_linux.py
sed -n 21,45p scripts/qualification_boundary_verification.py
sed -n 1,179p .github/workflows/qualification-s2-supervision.yml
cat tools/qualification_verification/host.json; cat tools/qualification_verification/provision.sh
sed -n 240,280p scripts/fp.py
grep -n "memory_bytes" deploy/qualification/test-profile.json
# composition-sweep re-parse (F3 per-call verify_for CPU and call counts, §3 setup CPU, F1 PART_A paths and
# panel proofs, F7 process_peak_memory_bytes); one line per row, prints depth, repeat, CPU/call, calls, setup CPU,
# PART_A path counts, panel-proof calls, peak bytes:
python3 -c "import json;d=json.load(open('docs/notes/2026-09-24-t10-step4/composition-sweep.json'));print('processes',d['processes']);[print(r['confirmation_depth'],r['repeat'],round(r['phases']['e1_run']['components']['proof.source_reverify']['cpu']/r['phases']['e1_run']['components']['proof.source_reverify']['calls'],3),r['phases']['e1_run']['components']['proof.source_reverify']['calls'],r['phases']['setup_fixture_domain_contract_source']['cpu'],r['path_counts'].get('PART_A'),r['phases']['e1_run']['components'].get('proof.part_a_panel_proof',{}).get('calls'),r['process_peak_memory_bytes']) for r in d['rows']]"
#   processes 1; CPU/call 1.021-1.051 (depth 2, 32 calls), 1.042-1.087 (depth 10, 56), 1.077-1.160 (depth 30, 107);
#   setup 10.36-12.38 s; PART_A {'REGIME': 4} with 3 panel proofs on the six depth-2/10 rows, none on depth 30;
#   peak bytes 121028608, 122392576, 124071936, 125886464, 127492096, 129118208, 131211264, 136695808, 136695808
grep -n "_peak_memory_bytes\|def one_run\|for depth\|for r in\|one_run(" docs/notes/2026-09-24-t10-step4/measure_composition.py.txt
python3 -c "print(256000000*9//10, 256000000/1.5, 256000000*9//10/1.5, 136695808/(256000000/1.5), 136695808/(256000000*9//10/1.5))"
#   230400000 170666666.67 153600000.0 0.801 0.890
grep -n "bounded same-sample re-execution is not a draw" docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md   # no hit
find . -name "*59ce3c4b7643*"; git log --all --oneline -S"59ce3c4b7643"
python3 scripts/check_handoff_authority.py --all   # executor run: 0 card(s) with an authority block, 0 violation(s); exit 0 (fix-round re-run: 2 cards, from files other agents are writing concurrently, 0 violations; exit 0)
python3 - <<'PY'   # every relative link and heading anchor in this note resolves from docs/notes/
import re,os
n='docs/notes/2026-09-27-s5-part-a-measurement-proposal-r2.md'
slug=lambda h:re.sub(r'[^\w\- ]','',h.strip().lower()).replace(' ','-')
bad=0;cnt=0
for t,u in re.findall(r'\[([^\]]*)\]\(([^)\s]+)\)',open(n).read()):
    if u.startswith('http'):continue
    cnt+=1;f,_,a=u.partition('#');p=os.path.normpath(os.path.join(os.path.dirname(n),f)) if f else n
    if not os.path.exists(p):print('MISSING',u);bad+=1;continue
    if a and a not in {slug(m) for m in re.findall(r'^#+ (.*)$',open(p).read(),re.M)}:print('ANCHOR',u);bad+=1
print(cnt,'relative links,',bad,'unresolved')
PY
#   after the fix round: 13 relative links, 0 unresolved
```

Edits to this note. The executing session applied line-anchor corrections with `sed -i`. Their exact expressions were not retained in its return, so they are **UNVERIFIED** here; their result is the text re-verified in this fix round. The 2026-09-27 fix round edited the note only with the Edit tool and short Python string replacements, each of which asserted exactly one match of the replaced text. What each changed is listed in the fix-round section below. The fix round added these read-only commands:

```bash
sed -n 1,20p docs/notes/2026-09-24-t10-step4-representative-measurement.md                  # line 8 "Runs used one process"
sed -n 205,213p ops/c1_rail/qualification/execution/profile.py                              # :209 _DIAGNOSTIC_PHASE, :211 _JOINT_N2_DIAGNOSTIC_PHASE
grep -n "subprocess" scripts/fp.py                                                          # :107 environment check, :274 launched command
sed -n 90,100p tests/integration/qualification_boundary/fixture_producer.py; sed -n 148,158p tests/integration/qualification_boundary/fixture_producer.py
sed -n 2774,2785p ops/c1_rail/qualification/execution/campaign_store.py; sed -n 2966,2990p ops/c1_rail/qualification/execution/campaign_store.py
sed -n 30,42p ops/c1_rail/qualification/execution/worker.py                                 # :37-38 TEST_ONLY/permits_synthetic refusal
grep -rn "run_part_a_compute" ops/ tests/                                                   # no hit
sed -n 86,97p ops/c1_rail/qualification/production.py                                       # :96 float(part.expansion_tolerance)
sed -n 224,230p docs/notes/2026-09-26-s5-decision-draft.md                                  # :228 falsifier, both limbs
git show 8c15f18:docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md | sed -n 50,80p   # :61 fix-round D2 clause, :72 expiry
git show 8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md | sed -n 324,331p         # r1 D2 triggers
sed -n 80,130p docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md               # :94 scope, :96 expiry, :102 re-run limit, :116-121 stops
sed -n 815,852p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md               # :828-830 direction table, :834-850 ruling
grep -n "roughly 137 s on Linux\|N2 compute phase gets 360 s" docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md   # :756, :757
sed -n 5,10p docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md; sed -n 20,64p docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md   # :8, :27, :35, :49, :61
grep -n "retention-days" .github/workflows/qualification-s2-supervision.yml                 # :179
python3 scripts/check_handoff_authority.py --all
```

No gate suite (`make check` / `fp.py check`), test, measurement, dispatch or download was run.

## Review and fix round (2026-09-27)

Two review passes returned findings with overlapping IDs. They are labelled **A-R1..A-R10** (first pass) and **B-R1..B-R7** (second pass). Every finding was checked against its cited source before any edit (commands under "Verification of this note"). All 17 were verified and applied; none was rejected. Only this note was edited.

| ID | Verdict | What changed, and why |
|---|---|---|
| A-R1 | Applied | F7 restated: `composition-sweep.json` has `processes: 1`, and the harness runs all nine rows in one interpreter (`measure_composition.py.txt:177-179`, `:149`). The values are one process's rising lifetime peak over full composition E1 runs, not per-row figures and not a lower bound on M̂. The 80.1% figure is kept only as orientation, labelled "different workload, not comparable". §0, §1 row 12 and §14 item 1 were updated |
| A-R2 | Applied | §10.3 quotes S5 draft line 228 in full and separates the Σ limb (the stop class) from the measurement limb, which stays live and engages at the release point. §3's D2 row discloses that the fix-round clause (`8c15f18:…handoffs…:61`) was changed, not kept. §1 row 13, §12.7 and new CP-1a item 4 were updated |
| A-R3 | Applied | §1 rows 5-7 now quote the ledger ruling's own words (slices plan lines 839, 844, 845). "Drop Stage 1b-N2 and the phase-generic option" is attributed to the H1 card (handoffs line 94) |
| A-R4 | Applied, option (b) | §7.3 and §7.7 now state that the authority gate is coextensive with the signed TEST_ONLY route (`worker.py:37-38`). P-3, P-4 and P-5 are named as the sole signed-route exclusion proof, and each is a hard C3 precondition that cannot be waived. P-1 is labelled defence in depth. Option (a) is not proposed, because it would make Stage 1c call the callable differently from the route (P-7); it is left to the operator |
| A-R5 | Applied | Anchors verified and corrected: `_DIAGNOSTIC_PHASE` is at `profile.py:209` and `_JOINT_N2_DIAGNOSTIC_PHASE` at `:211` (P3, §13 step 5). In §8.2, `scripts/fp.py:107` is the environment check and `:274` the launched command. §1 row 2 no longer says "None moved" |
| A-R6 | Applied (with B-R1) | The RC-3a additions are labelled as r2's derivation. Memory completeness comes from ruling condition (2), line 848. The N2 input is reworded: a proposed value suffices for the arithmetic, and this note proposes that it come from the separate ruling. §11, §13 step 1 and §14 item 3 were updated |
| A-R7 | Applied | SR-7 and §1 row 20 list all four packet tolerance sites: lines 8, 35, 49 and 61 |
| A-R8 | Applied (with B-R5) | Stage 0 gains a merge and copy step into `stage0/`, and "Files created" separates the scratch outputs from the repository outputs |
| A-R9 | Applied (with B-R7) | The placeholder and empty-heredoc commands are replaced by the exact scripts, which were re-run from the note's own text. The executor's `sed -i` edits are disclosed as UNVERIFIED, because their expressions were not retained |
| A-R10 | Applied | §7.1 marks the adapter's request construction as an **expectation** until C3 (packet line 27; `production.py:89-96`). No `run_part_a_compute` exists under `ops/` or `tests/` |
| B-R1 | Applied | §11 now quotes the ledger conditions by line (828-830), with r2's additions in a separate column marked PROPOSED (CP-1a item 2(e)) or derived. The §7.4 and §7.5 headings are marked PROPOSED, for CP-1a approval |
| B-R2 | Applied | One re-run cap per stage: one re-dispatch of a failed dry run and one `--failed` re-run covering up to both jobs. §12.6 was recomputed (arithmetic). Nominal is 184; the worst case is 368, not 257. With the SR-5 contingency the figures are 314 and 628. §12.3, §12.4 and §14 were aligned |
| B-R3 | Applied | P4 and §8.1 state the default memory binding of `memory_limit*9//10` = 230,400,000 (`fixture_producer.py:152-153`). PA-3's 256,000,000 holds only with the P4 tuple extended; unextended, binding fails on memory too (`campaign_store.py:2781`). The unextended orientation figure (89.0%, arithmetic) was added to F7, and the binding value to §12.5 |
| B-R4 | Applied | §0 is aligned with §8.3. The incomplete record is retained as UNVERIFIED, and the one re-run is a PA-4 candidate that never upgrades it. Memory still UNVERIFIED after the allowed re-run leaves RC-3a unmet and needs an operator ruling, and is neither D2 nor a PA-3 failure. §10.3 and §12.7 (I-1, I-3) were updated |
| B-R5 | Applied | Stage 0's expiry is now cited to the card (handoffs line 96) and to the #519 review (`:72`), with `createdAt` marked UNVERIFIED and recorded by `gh run view`. A public-clone review of the extracted lines was added before any commit |
| B-R6 | Applied | Stage 1c's approval is conditional: "if approved at CP-1a, executed at C3", and only after a recorded coordinator read of the `--stage 1c` harness diff. The harness sits on a separate measurement branch based on the S5 head, outside the packet's §2 file scope. The head check was added (workflow step 2 records `HEAD^`) |
| B-R7 | Applied | Same as A-R9 |

**Not granted by this fix round:** no measurement, dispatch, workflow file, artifact download, owner-document edit, or approval of any candidate.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED as the CP-1a packet.** Reviewer: the coordinating session. The artifact was the executor draft plus the fix round, which applied all 17 findings of two refute-first reviews. Verification: the full gate suite ran clean on the published commit, in a clean worktree (recorded in the PR). The coordinator read §0, §7, §8, §10.3, §11, §12.6–§12.7 and §14 in full. It spot-checked `worker.py:37-38`, `contract.py:763-773`, `fixture_producer.py:152-156` and `profile.py:209-211`, `:239`. The cross-handoff critic's findings X-01, X-02, X-03, X-09, X-10 and X-14 are dispositioned here.

**Dispositions:**
- **Condition 1, the signed-route exclusion (critic X-03).** Stage 1c is not BLOCKED at the design level. The authority gate admits the signed TEST_ONLY route (§7.3), so the exclusion rests only on P-3, P-4 and P-5 as hard C3 preconditions. The alternative is a discriminating gate that the signed route cannot satisfy. This is now an explicit operator choice (item 6 below). **Coordinator recommendation:** accept P-3/P-4/P-5 as hard C3 preconditions. A discriminating gate would make Stage 1c call the worker body differently from the route, which weakens P-7, the "same code" proof that condition 1 exists to secure.
- **Condition 2 (complete aggregate memory):** met by design (§8). The dry-run probe must confirm `memory.peak` on the runner before any timed repeat. UNVERIFIED memory after the allowed re-run leaves RC-3a unmet, and that is an operator ruling, not a waiver.
- **The D2 timing reading (critic X-10): accepted as the coordinator's reading, pending operator confirmation (item 4).** The owner text's "cannot be measured before S5 is released" is evaluated at the release point. Mapping that point to CP-1b follows from the 2026-09-27 split, and it is not a card deviation in substance. The #519 fix-round wording made the trigger immediate; r2 records the change openly (§10.3).
- **Missing owners (critic X-02).** The §3.4(d) text, the RC-6 re-anchor (including the SR set approved at CP-1a) and the RC-2 owner-text set are assigned to [handoff H1 step (c)](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h1--s5-measurement-correct-the-519-proposal-return-a-measurement-dispatch). Drafting may start now; application needs the operator's acceptance.
- **Stale derived text (critic X-09).** The addendum's CP-1a row is corrected in the same commit.

**CP-1a decision list: additions to §14.** Items 1–4 stand as written. Add:
5. **The RC-4 slice (critic X-01).** Accept H7 §B.2 (`docs/notes/2026-09-27-host-obligations-assignment.md`, published when accepted): a qualification slice "K3/RC-4 — service salt and client plan view", dispatched after S5 acceptance and landed before S8/T06, which moves K3 out of TB-F1. Or name another slice, such as TB-F1. The RC-4 assignment is complete only once the operator names it.
6. **The Stage 1c signed-route exclusion (critic X-03).** Accept P-3/P-4/P-5 as hard C3 preconditions (recommended), or require a discriminating gate.

**Timing (critic X-14).** Stage 0 must run before the S4 run artifacts expire, about **2026-10-08 to 2026-10-09**; the creation date is UNVERIFIED. **CP-1a can be split:** item 2(a) (Stage 0, calibration only, a read-only artifact download) can be approved on its own now. The rest of CP-1a can wait for this packet's review. Latest useful date for Stage 0 approval: **2026-10-07**.

**Not granted:** unchanged from the Status line. No measurement, download, CI change or dispatch runs until the operator approves it at CP-1a.
