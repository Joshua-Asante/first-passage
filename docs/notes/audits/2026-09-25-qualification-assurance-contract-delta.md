# Qualification assurance contract — mechanism-by-mechanism delta

**Audit ID:** AUDIT-2026-09-25-qualification-assurance-contract-delta
**Date:** 2026-09-25
**Triggered by:** external observation. The operator challenged the architecture, a Claude session assessed it, and Codex returned a counter-review.
**Authors:** Joshua + Claude Code
**Scope:** framework layer. This is the assurance contract that Protected Full E1 implements: the execution-slices plan S1–S8, the governing N1 boundary spec, and the Track B release-binding ADR.
**Lives in:** `docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md`

**Status:** evidence record and proposal. It changes no contract, owner text, slice
scope, ceiling or statistical decision, and it authorizes nothing. Every
disposition below is a *proposal* for the qualification owner and the operator.
The decisions stay with their owners: the
[execution-slices plan](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md)
for engineering scope, the
[Track B umbrella](../../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)
and [campaign record](../../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md)
for statistical design, and the
[release-binding ADR](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md)
for activation.

---

## §0 — Source anchors

Everything was read at `origin/main@d92d828` (2026-09-25 15:28 −0400) unless another head is named. This was
a source and record read only. No test suite, harness, Linux run or probe was executed.

- `docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md` §3
  — the trust model and principal table (qclient / qexec / worker / qg5 / administrator).
- `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` — global constraints,
  contract decisions 1–6, the S2 resource-scope clarification, the R2b restart ruling, the S3
  acceptance (2026-09-22), C2 (2026-09-24) and the 09-24 handoff entry.
- `docs/superpowers/plans/2026-09-19-attended-batch-qualification.md` §B0 decision.
- `docs/notes/audits/2026-09-17-pr415-structural-assessment.md` — the original defect families.
- `docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md` §2a T10–T11,
  §2b and §3 — the GO artifact, the reseal and layer equality.
- `docs/briefs/handoffs/2026-09-24-full-e1-coordinator-handoff.md` §2.1–§2.2.
- `docs/notes/2026-09-24-t10-step4-representative-measurement.md` §1–§2 — the per-path `verify_for` cost.
- `docs/briefs/phase3-preparation/2026-09-15/freeze-candidate.md:50-80` — the draft seed roots.
- `docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md` — the S5 scope, which freezes on S4's merge.
- Code: `ops/c1_rail/qualification/regime.py:10-24` (`domain_seed`),
  `qualification/seed_identity.py`, `qualification/legality.py`,
  `qualification/production_source.py:627,848` (`_execution_snapshot`, `verify_for`),
  `execution/compute.py:16` (n3 refused), `execution/campaign_protocol.py:8,29`
  (1 MiB chunk operations), `ops/c1_rail/c1_rail_arm.py:58` (baked M1 acceptance path).
  Sizes under `ops/c1_rail/qualification/execution/`: 13,108 non-test lines. `campaign_store.py` has 3,353,
  `campaign_supervisor.py` 3,049 and `campaign_funding.py` 986.
- Branches, not merged: `claude/s4-c2-repair@8f18c57` (2026-09-25 15:01 −0400, 51 files,
  +5,142/−570 against main, with its S4 packet §7 continuation entries dated 2026-09-25), and
  `claude/t05-result-seal@6cf2732` (`campaign_result.py` 1,385, `campaign_seal.py` 553,
  `g5_result.py` 195, `seal_service.py` 169).

---

## §1 — Trigger

On 2026-09-25 the operator made an architectural critique. It argued that qualification is built as a security
boundary against an untrusted requesting agent, which is stronger than "run an honest
evaluation, review the evidence, deploy the approved version". It challenged ten
mechanisms. A Claude assessment and a Codex counter-review agreed on the direction. Codex
added two requirements: the replacement boundary must be defined as *actions that stay
impossible for a fallible agent*, and each retained component must be justified by
future cost, not by the fact that it was accepted. Both reviews asked for this table before
any pause or removal.

**Failure class:** decision failure, suspected and not yet established. The contract may be
stronger than the decision needs. No discipline check was bypassed.

---

## §2 — What actually happened

1. **2026-09-17.** The PR 415 audit found semantic defects: legality PASS with no screen, a 50000
   basis accepted, placeholder output roles, and TEST_ONLY manufactured completion reaching G5.
   It endorsed the service/worker/G5 boundary "under its explicit trusted-host assumptions" and
   also required semantic fixes that no boundary provides (audit §Structural changes 1–3).
2. **2026-09-18/19.** The execution-slices plan fixed the contract. The main terms are: lifetime resource
   charges start before admission (contract decision 2); every route phase has a reservation settled by
   measured CPU, with unknown usage consuming the full reservation (3); signing recovery returns a
   byte-identical receipt (6); and missing capture never licenses another draw (6).
3. **2026-09-19, B0.** Compared the service with the operator-launched batch *under that contract*
   and kept the service. Its only condition for reversing was whether "the warm-service intent producer
   cannot be bounded". It did not ask whether the contract itself was needed.
4. **2026-09-19 to 09-25.** Extending the contract from N1 to N2 cost repeated rounds:
   - Four red full Linux runs in a row stalled on N1-only phase gates. C2 traced seven sites, among them
     the liveness admit set, `pids.max`, the UID map, `G5_COMMIT_STATES`, `_terminal` and the
     `'N1'`-hard-coded retry.
   - The N2 compute exceeded its phase ceiling: 211 s CPU measured on Windows against about 100 s of payload
     allowance. Resolving it needed an operator ruling (M13).
   - S3's P1/P2 fixes made settlement authoritative over correct G5 decisions.
   - T05 found a seal work that would have stayed `RUNNING`, and a committed PASS on an exhausted campaign
     that could still be sealed.
   - On 2026-09-25 the cross-vendor review of the S4 repair found watchdog and settlement gaps
     (red record `20260925T183201Z-10899d8e6ef6`, 14 failed).
5. **2026-09-24, T10 step 4.** The per-path `verify_for` whole-source snapshot extrapolates to about 89 s
   per call and about 580 h for the draft 23,510-path workload, roughly 9× replay. This is an
   extrapolation 19× beyond the measured size; a confirming probe is owed.
6. **2026-09-25.** The S4 repair branch landed R2–R4 and the cross-vendor dispositions
   (`1468e5d`, `8f18c57`). S4 now waits only on frozen-head Windows selections, Linux subsets,
   two full Linux runs and acceptance.

---

## §3 — Discipline checks that should have caught it

| Check | Should have caught | Actual behavior |
|---|---|---|
| §1 Rule 0 reads | No. The source reads behind the contract were real | Fired: B0 and C2 are source-bound |
| §2 Falsifiable hypothesis | Partly. "Would a cheaper contract permit a failure that matters?" was never posed as a testable claim | Not applicable to engineering plans as written |
| §3 Forbidden moves | No | Forbidden-move lists protected statistics and ceilings correctly |
| §4 Gate criteria binary | No | Gates were binary. The question is whether each gate is needed |
| §5 Question form | **Yes.** B0 asked "service or batch?", which is a solution-shaped question. The symptom-shaped question is "what is the cheapest contract that makes the listed failures impossible?" | B0's selection was sound for the question it was asked |
| §6 Audit hooks runnable | — | — |
| §7–14 CC handoff checks | Check 11 ("what would make this moot") applies. No packet named "narrow the contract" as the upstream moot-maker | Pre-mortems named cheaper *evidence*, not a cheaper *contract* |

---

## §4 — Root cause analysis

- **Immediate cause:** B0 compared two implementations of one assurance contract and
  held the contract fixed, which its handoff instructed ("resolve … contract deltas against
  governing owners"). A contract-level question was never assigned to anyone.
- **Contributing factor:** each defect family found under PR 415 was repaired by adding a
  mechanism. There was no matching step asking whether an existing mechanism could be removed. Accounting,
  recovery and signing-retry rules then had to generalize across every new phase, and C2
  shows that generalization is where the rounds went.
- **Structural cause:** the threat model is stated as "untrusted requesting agent", but
  neither its consequences nor its limits are listed as a closed set of *actions that must stay impossible*.
  Without that list, every mechanism looks equally load-bearing, and one that protects
  a property nobody consumes cannot be told apart from one that protects activation.

---

## §5 — Repair plan

### Immediate

- [ ] Operator/owner decision: adopt the boundary list in §5.1 as the baseline, or reject it. Every row
  in §5.2 depends on it.
- [ ] Decide rows N1 and N2 **before S5 freezes**. S5 freezes on S4's merge, and it extends the same phase
  sets and reservations to `PART_A`/`PART_A_CAPTURE` (S5 packet line 12).
- [ ] Close gap K3 (the seed root can be previewed) before F1, whatever the other dispositions.
- [ ] Run the T10 `verify_for` confirming probe (handoff §5 item 5) before deciding row N4.
- [ ] Decide row E3 before TB-I3 / TB-D2 is packetized. It is not built yet, so a change costs nothing.

### 5.1 Proposed boundary: actions that must stay impossible for the requesting agent

This follows Codex's framing. Each boundary is stated so that it holds even when the agent is confident
the action is right. Per [M-46](../../methodology/lessons/methodology_lessons.md), each must be
**enforced by permissions, not instructions**.

| # | Must stay impossible | Enforcement today | Gap |
|---|---|---|---|
| B-1 | Altering installed execution, adjudication or worker code for an admitted release | Spec §3: service and worker code are administrator-owned; `qclient` cannot edit them; release manifest digests (accepted S2) | None for the service host. It holds only while agents lack administrator access on that host, and that is an operational fact to verify, not an assumption |
| B-2 | Replacing or editing captured evidence or the journal | `qexec` owns the attempt DB; the worker has a bounded output mount; `qg5` reads immutable captures (S3) | None found |
| B-3 | Producing a counted attempt that nobody sees, or choosing which attempt counts | Service-owned attempt registry and once-only dispatch (S1–S3) | **K3:** a preview *outside* the service is possible. See row K3 |
| B-4 | Granting itself activation authority | Arm interlock (`c1_rail_arm.py`), per-session operator GO | T11 checks are owed (ADR §2a), not built |
| B-5 | Presenting fixture or TEST_ONLY output as production evidence | Authority class in the release/profile; production execution disabled | None found at this read |

Anything **not** needed for B-1 to B-5, or for a semantic-validity property, carries the
burden of a separate justification. That is the test applied below.

### 5.2 Contract-delta table (summary)

Status values: **A** = accepted on `main`; **B** = built on a branch, not accepted; **O** = owed, not built.

| ID | Mechanism | Proposed disposition | Status | Where forward cost remains |
|---|---|---|---|---|
| K1 | Protected capture and execution attestation | Keep | A (N1); B (N2, S4 repair) | S5 Part A adapter |
| K2 | Semantic validation (legality, basis, output roles, batch shape) | Keep | A + B (R4 shape closure) | S5 Part A shape |
| K3 | Fixed sampling plan and seed commitment | Keep, **close gap** | A (plan); gap open | F1 freeze |
| K4 | Retained attempt history and custody integrity | Keep | A; B (v9 widening) | Each schema bump |
| K5 | Exact release identity and release-to-checkpoint binding | Keep | A; B (R4) | S5 `/v7` release |
| K6 | Principal separation (qclient / qexec / worker / qg5) | Keep | A (S2) | Production host provisioning |
| K7 | Independent G5 adjudication | Keep | A (N1); B (N2) | S5, T05 |
| K8 | Explicit activation and fresh account reconciliation | Keep | Partly A (arm interlock); O (T11) | TB-I3, TB-O1 |
| N1 | Fine-grained resource accounting and settlement authority | **Narrow** | A (S1/S2); B (N2) | S5, T05, S8 |
| N2 | Interruption recovery and no-redraw | **Narrow** (precise rule) | A (IN_DOUBT posture) | S5, S8 |
| N3 | Publication, VOID serialization, byte-identical signing recovery | **Narrow** | A (N1); B (T05) | T05, S8 |
| N4 | Per-path whole-source re-verification (`verify_for`) | **Narrow**, if the probe confirms | A | Production E1 wall time |
| N5 | Approval packets (D0 / D1 / TB-D2 GO / per-session GO) | **Narrow** (consolidate) | Mostly O | Deployment track |
| E1 | Separate seal authority and seal service | **Evaluate replacement** | B (T05, ~2.3k lines, not accepted) | T05 integration, S8 |
| E2 | Custom artifact transport (1 MiB chunk operations) | **Evaluate replacement** (low priority) | A | S5, T05 chunk ops |
| E3 | Approval-driven image rebuild (GO reseal, layer equality) | **Evaluate replacement** | O | TB-I3, TB-D2 |
| X1 | Final n3 (sole fresh-state replay) | **Separate decision** (not in scope) | O (T12) | — |
| X2 | Any change to statistical acceptance (depths, thresholds, D-B4) | **Separate decision** (not in scope) | Ruled | — |

### 5.3 Row detail

Each row gives: failure prevented · cheaper replacement · residual failure it permits ·
consumers affected · decisive verification · migration and remaining cost. "Keep" rows
give the replacement as "none proposed" and explain why.

**K1 — Protected capture and attestation.**
- *Prevents:* invented results, and completion marked without the computation running (PR 415 family 3).
- *Cheaper:* none proposed. This row is what B-2 and B-5 rest on.
- *Residual:* —.
- *Consumers:* G5, the result commit, the release dossier.
- *Verification:* the existing S3 Linux PASS/FAIL cases and the fabrication-refusal tests.
- *Cost:* remaining work is the S5 Part A adapter only.

**K2 — Semantic validation.**
- *Prevents:* a correct run of an invalid contract, and evidence that does not mean what the result
  claims (PR 415 families 5 and 6; C2's batch-shape findings).
- *Cheaper:* none. Codex point 4 applies here: wrong sample membership invalidates a correct formula.
- *Residual:* —.
- *Consumers:* G1, G5, the dossier.
- *Verification:* coherent-substitution refusal tests (R4 on the repair branch).
- *Cost:* S5 Part A shape closure.

**K3 — Fixed sampling plan and seed commitment.**
- *Prevents:* selective reruns, and picking a favourable random stream.
- *Gap:* seeds are
  `sha256(['tb-s2-rng-v2', purpose, domain, root, stage, population, panel, path])`
  (`regime.py:22-24`). The root is an author-chosen string, and draft roots are already published
  (`freeze-candidate.md:56-60`). Anyone with the source and the code can compute n1/n2 outcomes
  outside the service, or try several roots, before dispatch. The service's once-only controls cannot
  see a preview.
- *Cheaper fix:* an operator-generated salt, committed by hash in F1 and revealed only at dispatch,
  so that the root cannot be known until after the commitment.
- *Residual:* a preview is still possible *after* reveal, which is harmless because the plan is then
  committed.
- *Consumers:* `seed_identity`, `domain_seed`, the F1 contract, and the G5 re-derivation.
- *Verification:* a test showing that a contract with the salt still in commitment state cannot derive seeds;
  the committed hash matches the revealed salt at dispatch.
- *Cost:* small, touching the RNG recipe version and the F1 schema.
- *Timing:* not live today, because the production source is deferred (O-4) and n3 depends on snapshot S. It must be
  closed before F1.

**K4 — Retained attempt history and custody.**
- *Prevents:* hidden or overwritten attempts.
- *Cheaper:* none for the property itself. The *cost driver* is schema widening at each stage
  (8→9 needed an exact-DDL predecessor check).
- *Residual:* —.
- *Consumers:* the journal and every store.
- *Verification:* the v9 widening and integrity tests on the repair branch.
- *Cost:* each future stage pays a widening, so fewer journal tables per stage lowers it (see N1).

**K5 — Release identity and checkpoint binding.**
- *Prevents:* evaluating one configuration and deploying another, and a release admitting stages it does not implement
  (C2: v5 admitted `N2`).
- *Cheaper:* none.
- *Consumers:* service, G5, arm.
- *Verification:* R4 release-binding tests.
- *Cost:* one release/profile revision per stage while staged development continues (contract decision 4).
  This is a cost of *staging*, not of the property.

**K6 — Principal separation.**
- *Prevents:* the requesting client reaching keys, the journal, the Docker socket or code. This is the enforcement behind B-1 to B-3.
- *Cheaper:* none proposed. It is accepted and it is what makes §5.1 enforced rather than
  instructed.
- *Residual:* an administrator or a malicious approved worker (trusted by design, spec §3).
- *Consumers:* the production host.
- *Verification:* the S2 Linux nodes.
- *Cost:* production-host provisioning only. The open operational check is that no agent session holds
  administrator access on that host.

**K7 — Independent G5 adjudication.**
- *Prevents:* the component that computes an outcome also declaring its own success.
- *Cheaper:* none. The operator's critique and both reviews agree that independent verification earns its place.
- *Consumers:* the result commit.
- *Verification:* S3 Linux qg5 unit cases.
- *Cost:* the S5 and T05 integration of Part A.

**K8 — Explicit activation and fresh reconciliation.**
- *Prevents:* activation without approval, and qualification evidence applied to a different account state.
- *Cheaper:* none for reconciliation.
- *Residual:* —.
- *Consumers:* `c1_rail_arm.py`, TB-O1.
- *Verification:* T11 checks per ADR §2a.
- *Cost:* owed. E3 changes how the GO is carried, not whether it is checked.

**N1 — Fine-grained resource accounting.**
- *Prevents:* runaway spend, work escaping its approved budget, and retries creating extra computational opportunity.
- *Evidence of cost:*
  - §2 item 4 (C2's seven N1-only sites, M13, S3 P1/P2, T05 stranding, today's watchdog findings);
  - contract decisions 2–3 require charging admission, signing, serialization and custody
    against one lifetime cap, and "cross-campaign interference and group OOM can invalidate every
    attempt on that host" (S2 clarification).
- *Cheaper:* separate the **statistical sampling limit**, which stays fixed in the frozen plan, from the
  **infrastructure limit**. The infrastructure limit becomes one outer cgroup per campaign (CPU, memory, wall) plus a
  per-work timeout. Settlement then *ends the campaign on overrun* but never retroactively revokes a
  committed decision of a deterministic stage.
  Part A depth was sized from the compute budget at F1 (ADR Deviation A1). That is a planning number,
  and runtime enforcement of it adds no statistical protection once the depth is frozen.
- *Residual:* an overrun is detected per campaign rather than per phase, and a runaway phase burns the shared
  allowance before it stops.
- *Consumers:* `campaign_store`, `campaign_supervisor`, `campaign_funding`, `budget`,
  `campaign_budget`, T05 result/seal settlement, and the S2 Linux nodes that assert per-phase settlement.
- *Verification:*
  - a test that an overrun of the outer limit ends the campaign without fabricating FAIL;
  - a test that no per-phase CPU number appears in any acceptance decision;
  - the S2 nodes for exhaustion and for the original deadline surviving downtime, re-expressed at campaign scope.
- *Cost:* **highest forward saving and highest migration risk.** The machinery is accepted code
  spread through the three largest modules, and S2's accepted Linux evidence asserts it. The
  cheapest cut is probably to *freeze* per-phase reservations at their N1/N2 form and give `PART_A`, result and seal
  the campaign-scope rule only. That avoids a rewrite. It needs an owner amendment to contract decisions 2, 3 and 6
  and to spec §2.6.

**N2 — Interruption recovery and no-redraw.**
- *Prevents:* repeating an unfavourable run, and restarting from a different stream.
- *Cheaper:* allow deterministic re-execution of the *same* sample only when every one of these holds:
  - the release, input manifest, runtime and seed addresses are identical;
  - there is no dependence on time, concurrency or mutable files;
  - every attempt is recorded, including the interrupted one;
  - a fixed acceptance rule is stated in advance: the re-run output must match every complete record retained
    from the interrupted attempt, compared record by record on the retained prefix, and any mismatch is an
    incident, not a result;
  - retries are bounded at one per interruption and at most two per campaign.

  (Codex point 3.) The design already treats "missing deterministic G5 validation may be repeated" as not being a
  new draw (contract decision 6). This extends the same logic to compute.
- *Residual:* undetected nondeterminism. A reproducibility test is evidence for particular conditions, not proof.
- *Consumers:* `recover_service`, `recover_campaign_work`, the IN_DOUBT paths, and the R2b ruling.
- *Verification:* a bitwise-reproducibility test per stage on the pinned runtime; an interrupted-then-re-executed
  case whose retained prefix matches; an altered-prefix case that ends as an incident.
- *Cost:* moderate. It depends on K3, since re-execution is only safe when the root was not previewable, and it must be ruled
  before F1.

**N3 — Publication, VOID and signing recovery.**
- *Prevents:* partial output treated as complete, cancelled results staying usable, and a retry publishing a
  conflicting result.
- *Cheaper:* a single writer with staged artifacts, an atomic completion record, and a current approval/revocation check
  at activation. Keep VOID serialization. **Drop byte-identical receipt recovery** unless a named consumer
  verifies old receipts offline. The byte identity exists because the signing instant is inside the signed
  payload.
- *Residual:* a retry after a lost acknowledgement yields a second, equally valid receipt for the same result, and consumers
  must key on the result digest, not on the receipt bytes.
- *Consumers:* T1/T2 intent handling, the T05 result/seal commits, and the S3 E06/E07 scene.
- *Verification:* a lost-acknowledgement retry test showing both receipts bind the same result digest and that VOID beats either.
- *Cost:* small for T05, which is not accepted. The N1 implementation is accepted and can stay.

**N4 — Per-path source re-verification.**
- *Prevents:* a worker using a source object that differs from the admitted one partway through the run.
- *Cheaper:* verify the whole-source snapshot **once** per worker start against the frozen digest. The worker's
  source is read-only (K1, K6), so it cannot drift between paths.
- *Residual:* mutation inside the worker's process memory between paths. Within the trust model that is only possible
  through the approved worker code.
- *Consumers:* `production_source.verify_for`, `result_adjudication.verify_for`, and the T10 budget.
- *Verification:* the confirming T10 probe first. Then a test that a mutated source is refused at worker start, and a
  timing record.
- *Cost:* possibly the largest *wall-time* saving (extrapolated about 580 h against 66–122 h of replay). The snapshot is
  an integrity control, so any change goes through its owner (T10 note §2).

**N5 — Approval packets.**
- *Prevents:* confusing engineering completion, statistical acceptance, funding permission and permission to trade.
- *Cheaper:* one release dossier with separate decision fields, plus a distinct session activation.
- *Residual:* the same person approves several fields in one sitting. That is acceptable while one operator holds every
  authority.
- *Consumers:* D0, D1, TB-D2, TB-O1.
- *Verification:* the dossier schema keeps each field separately signed or recorded, and the arm checks each one.
- *Cost:* mostly owed, so it can be consolidated at authoring time.

**E1 — Separate seal authority.**
- *Prevents:* a component that computes or adjudicates also manufacturing the final authorization.
- *Cheaper:* the operator's release approval, detached and signed, referencing the committed result digest.
  K7 already provides independent adjudication.
- *Residual:* no mechanical second signer. The seal signer would re-check the same facts through shared code under
  the same administrator, so the protection lost is small.
- *Consumers:* T05 (`campaign_seal.py`, `seal_service.py`), S8, D0.
- *Verification:* a test that activation refuses a result without the operator approval, and refuses an approval that
  names another digest.
- *Cost:* the seal code is about 720 lines, built but not accepted. Dropping it avoids its acceptance, its
  Linux evidence and its S8 lifecycle cases, but costs an amendment to the slices plan's S7.

**E2 — Custom artifact transport.**
- *Prevents:* truncated or substituted artifacts, and unauthorized reads.
- *Cheaper:* read-only files with a manifest of content hashes, published atomically.
- *Residual:* none for a local, attended release.
- *Consumers:* `FETCH_PLAN_CHUNK` and the checkpoint chunk operations.
- *Verification:* a truncated file and a substituted file are both refused by manifest hash.
- *Cost:* the code is accepted and small. B0 already narrowed transport to the local socket. The saving is limited to
  not adding chunk operations for Part A and the result. **Low priority.**

**E3 — Approval-driven image rebuild.**
- *Prevents:* activating without approval, and gating on a mutable file.
- *Cheaper:* a detached GO signed by an operator key held off-host, verified at arm against a public key baked into the
  image v1. ADR §3 rejected only an *unsigned* volume file, citing the rationale at `c1_rail_arm.py`. A signed artifact
  answers that objection. There is no image v2, no reseal, no layer-equality proof and no build-context diff.
- *Residual:* key management for the operator key; and a compromised administrator can swap the running image. The
  second is already trusted by design.
- *Consumers:* TB-I3 (`deployment_go.py`, not built), TB-D2, TB-O1, T11.
- *Verification:* the arm refuses an unsigned, wrongly signed, expired or wrong-digest GO, and a swapped public key changes
  the execution fingerprint.
- *Cost:* **near zero if decided before TB-I3.** It needs an ADR revision to §2b and §3.

**X1 / X2 — separate decisions.** Replacing the sole n3 with an operating envelope, or changing depths, thresholds
or D-B4, is a statistical amendment rather than a simplification. It needs its own ruling before F1, and the account
is used rather than pristine. This note proposes nothing for these rows.

### 5.4 S4 in light of the table

The earlier proposal to pause S4 at R2–R4 is **overtaken**. The repair branch implemented R2–R4 and the
cross-vendor dispositions on 2026-09-25 (§0, §2 item 6). By row, the R-items fall as follows:
- R3 (snapshot closure) and R4 (release binding, shape closure, service-path commits, refusals) → K2, K4 and K5.
- R2's custody widening and integrity walk → K4.
- R2's `_terminal` liveness and E08 N2 cases, R5b (M13) and today's watchdog fixes → N1.

What remains for S4 is Linux evidence and acceptance on the frozen head. Finishing S4 is therefore cheap relative to
the rows above. **The decisions that bite are upstream of S5's freeze** (N1, N2) and of T05 integration (N3, E1).

### Structural

- [ ] If §5.1 is adopted: record it where the threat model lives (spec §3) as the boundary set that each
  retained mechanism must cite. This is an owner amendment, not this note.
- [ ] Add a "what would a cheaper *contract* permit?" line to brief-authoring check 11 (pre-mortem). Do this only if
  the operator wants it; standing instructions are not edited here.

---

## §6 — Lessons to capture

- **Candidate lesson:** comparing implementations under a fixed contract does not test the contract.
  Ask the symptom-shaped question ("which failures must be impossible, and what is the cheapest enforcement?")
  before choosing between architectures.
  - Anchor: B0 (2026-09-19) and this audit.
  - Cost counterfactual: the per-phase accounting generalization rounds in §2 item 4. These are not yet costed in hours.
  - Registry destination: `docs/methodology/lessons/methodology_lessons.md`.
  - Promotion status: Candidate. It is one firing and needs recurrence or an operator structural approval.
- Already covered in part by M-46 (prefer structural fixes that scale over vigilance), which supports the
  "enforced, not instructed" requirement on §5.1.

---

## §7 — Programme-audit signal check

- [x] **Belt that only grows, never prunes.** Every defect family since PR 415 added a mechanism, and none was
  retired. This audit is the first pruning pass.
- [ ] Belt-patches without independent corroboration. No: fixes were independently reviewed.
- [ ] Falsifier thresholds drifting. No.
- [ ] Methodology invoked to rationalize a prior decision. Not observed.
- [ ] SNAG pattern. No.
- [ ] Cross-layer contamination. No: statistical rows are explicitly excluded.
- [ ] Negative heuristic crossed without repair. No.

One box is checked, so this note is **input** to a programme audit of the qualification engineering layer if the
operator opens one. It is not a verdict on that layer.

---

## §10 — Audit hooks

```bash
# K3: seed roots must not be predictable before F1 commitment (expect a salt/commitment field once closed)
grep -n "root_rng_namespace\|salt\|commitment" ops/c1_rail/qualification/regime.py ops/c1_rail/qualification/seed_identity.py

# N1: count phase-scoped admit/reservation sites that each new stage must extend (trend should fall, not grow)
grep -c -E "PROVISIONAL|BOUND|N2_READY|PART_A_READY" ops/c1_rail/qualification/execution/campaign_supervisor.py ops/c1_rail/qualification/execution/campaign_store.py

# N4: per-path re-verification call sites (expect verify_for outside the per-path loop once narrowed)
grep -n "verify_for" ops/c1_rail/qualification/*.py ops/c1_rail/qualification/execution/*.py

# E3: the GO carrier chosen (expect a signature check, not a layer-equality reseal, if E3 is adopted)
grep -rn "DEPLOYMENT_GO\|layer" ops/c1_rail/*.py

# Disposition follow-through: each row ID should appear in its owner once decided
grep -rn "AUDIT-2026-09-25-qualification-assurance-contract-delta" docs/superpowers docs/adr docs/briefs
```

Re-run at S5 freeze and at TB-I3 packetization, the two points where the dispositions stop being cheap.

---

## §11 — Closure

- **Status:** `Open`. It waits on the operator's decision on §5.1 and the owners' rulings on rows N1–N5 and E1–E3.
- **Immediate repair completed:** —
- **Structural repair completed:** —
- **Lessons graduated to standing rule:** none
- **Follow-up audits triggered:** a programme audit of the qualification engineering layer (optional, §7).

**Limits.** This is a source and record read, with no execution. Costs are qualitative or line counts, not hours. S4
branch state is as recorded in its packet §7 on `claude/s4-c2-repair@8f18c57`, not re-run. This note has not been
independently reviewed; the PR-level Codex review is that step (M-47).

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md --type audit
$ python scripts/check_brief.py docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md --type audit
# Expected: NOT CHECKED (repo-side declines audit)
$ sed -n 22,24p ops/c1_rail/qualification/regime.py            # K3 seed recipe
$ grep -n "verify_for" ops/c1_rail/qualification/production_source.py   # N4
$ git log -1 --format=%h origin/claude/s4-c2-repair               # §0 branch anchor (8f18c57 at authoring)
```
