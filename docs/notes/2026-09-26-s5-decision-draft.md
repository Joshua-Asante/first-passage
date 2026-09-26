# S5 decision draft: assurance boundary, N1 accounting and N2 recovery (proposed rulings)

**Status:** draft decision packet for the operator. It changes no owner document, code, contract, ceiling or statistic, and it does not release the S5 freeze. That freeze stays **HELD** under the [ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25). Every amendment below is *proposed* text for its named owner.
**Dispatch:** Task 2 of the B–D packet card (`docs/briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md` at `f311578`). The card's own requirements and the operator's executive-review points (a)–(f) apply.
**Source anchors:** `main@24e3843`, read 2026-09-26. The sources were read, not run. No Linux run, probe or private source was used. Line numbers are at that head.
**Inputs:** the [contract-delta audit](audits/2026-09-25-qualification-assurance-contract-delta.md) (§5.1, rows K3/N1/N2, §10), the [execution-slices plan](../superpowers/plans/2026-09-18-full-e1-execution-slices.md) (contract decisions 1–6, S2 clarification, S2/S3/C2 entries, S5), the [N1 boundary spec](../superpowers/specs/2026-09-17-qualification-execution-boundary-design.md) §3/§7, the [full-E1 spec](../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) §2.4–§2.8/§5, the [release-binding ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) §2a T10–T11/§2b, the [S5 packet draft](../briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md), and the code under `ops/c1_rail/qualification/`.

## 0. Summary

| # | Decision | Recommended ruling | Owners amended | Blocks |
|---|---|---|---|---|
| D1 | §5.1 boundary B-1..B-5, with K3 seed custody | **Adopt, conditionally.** Each boundary counts as enforced only after its operational facts (OF-1..OF-7, §1.3) are verified on the actual host. For K3, the **service** generates the salt *after* the attempt is irrevocably admitted; F1 carries the custody rule, not a salt hash. Abandonment after generation consumes the attempt. | Boundary spec §3; umbrella §0.8 (TB-F1); full-E1 spec §2.4 | K3 before F1; OF before any production-authority release. S5 (TEST_ONLY) is not blocked |
| D2 | N1 resource accounting | **Keep the per-work cumulative bound and per-phase reservation sizing for every phase, PART_A/RESULT/SEAL included. Reject both the mixed model and the uniform campaign model for S5.** Adopt four narrowings: the invariant stated as written; the exhausted-campaign rule; no per-phase CPU figure in any acceptance decision; and (optional) coordinator-set TEST_ONLY ceilings | Slices plan contract decision 3; full-E1 spec §2.5 | S5 freeze (needs a measured PART_A ceiling at maximum expansion) |
| D3 | N2 interruption recovery | **Adopt bounded same-sample re-execution** (§3.3 R1–R10) as policy now. S5 freezes with today's terminal IN_DOUBT, which is the conservative subset. Build the rule as its own slice after S5 and before S8 | Full-E1 spec §2.4, §2.6, §5; slices plan contract decision 6 and S5 text | Production F1 (as a policy), not the S5 freeze |

**Mixed versus uniform (review point d), in one line:** a uniform campaign model beats the mixed model on forward complexity, because the mixed model's phase-conditional sizing rule is the defect class C2 found. The mixed model beats the uniform model on migration risk. Neither removes the reservation and settlement machinery, because a cumulative bound needs a per-work reservation (§2.2). The remaining cost of reaching Part A is stage plumbing that every model pays (§2.3), so for S5 the accepted per-phase model wins.

## 1. D1: assurance boundary B-1..B-5 and K3 seed custody

### 1.1 Recommended ruling

Adopt §5.1 as the closed set of actions that must stay impossible for the requesting agent. Each row is **enforced only while its operational facts hold**, and those facts are verified by the operator's attended host read, never assumed. The reason is that every enforcement mechanism in §5.1 rests on credentials and host permissions, not on process roles:

- qexec is root-equivalent through Docker (`tools/qualification_verification/README.md:11-17`).
- Under the accepted polkit rule, qexec can start arbitrary transient units (slices-plan S2 host-fix acceptance, item 5).
- An agent that can reach an administrator, Docker-socket or qexec credential defeats B-1, B-2 and B-3 at once, whatever the UID separation.

B-3 gains seed custody (§1.4). B-4 is recorded as **held only by operational facts today**:

- The arm check validates M1 structure and presence, not a signature.
- The rail host's boot gate does not check M1, so an edit to the `/data` config bypasses it (AGENTS.md, Live-execution posture).
- T11 is owed ([ADR §2a](../adr/2026-09-12-tradeify-book-protection-instance-admission.md), TB-I3).

### 1.2 Evidence

| Row | Enforcement today (file:line) | What it actually depends on |
|---|---|---|
| B-1 code | Spec §3 principal table; service and worker code administrator-owned; release digests (accepted S2) | No agent holds admin or qexec on the service host. The **CI harness is not a boundary host**: `.github/workflows/qualification-s2-supervision.yml:106-168` provisions and reads evidence with `sudo`, from a workflow an agent can edit and dispatch |
| B-2 evidence | `qexec` owns the store; worker output is one fsynced frame on a bounded mount (`execution/worker.py:137-149`); store refuses `CAPTURED` after `IN_DOUBT` (`execution/campaign_budget.py:95-98`) | Same as B-1: root or Docker access can rewrite the SQLite journal |
| B-3 counted attempt | Once-only compute reservation (`execution/campaign_store.py:2896-2901`); unique execution key (boundary spec §7) | K3: a seed preview can happen **outside** the service (§1.4). Today the client role can also fetch plan chunks (`execution/campaign_protocol.py:92`), and the plan carries seed values (`qualification/checkpoint_plan.py:222-233` → `seed_identity.py:35-40`, the `seed` field) |
| B-4 activation | `c1_rail_arm.py` interlock; per-session GO | Not machine-enforced on the host (see §1.1). Held by OF-5/OF-6 until TB-I3 |
| B-5 fixture output | Authority class and `production_execution=false` in the release/profile (slices plan, Global constraints) | Release install is an administrator act (OF-1), not a merge. Branch protection alone does not enforce B-5 |

### 1.3 Operational facts to verify (review point a)

| OF | Fact (must hold) | Protects | Verification (operator-attended, recorded) | When |
|---|---|---|---|---|
| OF-1 | No account or environment in which an agent session runs can use administrator, `sudo`, `docker`-group or `/var/run/docker.sock` access on the production qualification host. That includes the operator's own workstation account when agents run under it | B-1, B-2, B-3, B-5 | Host: `getent group sudo docker`, `stat` of the socket, `sudo -l -U <user>` for each login; workstation: no host SSH key, token or agent-forwarded credential reachable by the agent's account | Host provisioning; before any production-authority release; after any access change |
| OF-2 | No agent can authenticate as `qexec`, `qg5`, `qseal` or the administrator, and no polkit rule grants `manage-units` to an agent-reachable UID | B-1..B-3 | Host: `/etc/polkit-1/rules.d` listing; `authorized_keys` per principal | Same |
| OF-3 | Execution, result, seal and operator-VOID private keys are unreadable by agent-reachable UIDs. They are absent from every worktree, every CI secret visible to an agent-editable workflow, and every store the agent can reach | B-2, B-3 (receipts), K7 | Key-path owner/mode read; `gh secret list` compared against the workflow files; worktree scan by filename, not content | Same |
| OF-4 | The key-enrollment and trust-domain inputs are writable only by the operator | B-1, B-3 | Owner/mode of the enrollment files on the host | Same |
| OF-5 | No agent holds rail-host deploy credentials (Fly token or flyctl session), write access to the rail `/data` volume, or broker credentials | B-4 | Operator reads the agent environments' credential stores; Fly access list | Before any arm; each session GO |
| OF-6 | If E3 is adopted, the operator GO signing key is off-host and never loaded where an agent runs | B-4 | Key custody record | TB-I3 |
| OF-7 | The seed salt (§1.4) is readable only by `qexec`, the worker input mount and `qg5` staging until reveal | B-3 (K3) | Mode/ownership of the salt row and objects; negative client-fetch test (§1.6) | Before F1 admission |

A row whose OF is unverified is reported as **unenforced**, not as assumed.

### 1.4 K3 seed custody (review point b)

A hash commitment in F1 (the delta's form) needs the salt to exist before F1. Its creator could then preview outcomes with the source and the code, and decide whether to freeze. The ruling therefore makes the **service** the generator and places generation **after** irrevocable admission.

| Question | Proposed rule | Grounding |
|---|---|---|
| Who generates | `qexec`, `secrets.token_bytes(32)`, inside the admission transaction of the single authorized attempt. Never the operator, an agent or the F1 author | Spec §2.2: `qexec` is trusted and owns plans. Today's root is an author-chosen contract string (`contract.py:152,805`) |
| When configuration is irrevocably committed | F1 freezes `root_rng_namespace`, recipe `tb-s2-rng-v3` (salted) and this custody rule. It carries **no salt and no salt hash**. The attempt commits when admission binds the F1 contract digest and budget (`campaign_store.py:2750-2802`); the salt is generated in that commit | Current recipe `regime.py:22-24`, seed input `seed_identity.py:29-41` |
| Visibility before reveal | `qexec` store, the worker's read-only input manifest and `qg5` private staging. **Not `qclient`**: before reveal the client plan view carries seed *digests*, not seed values. The administrator can read it, so OF-1 applies | The client can fetch plan chunks today (`campaign_protocol.py:92`), and seeds are in the plan (§1.2 B-3) |
| Commitment | `sha256(salt)` in the admission receipt, client-visible at once. Canonical form: 64 lowercase hex, refused otherwise at generation and reveal | Delta K3 entropy rule retained |
| Reveal | At the campaign's **terminal** state: a result commit, a statistical FAIL, IN_DOUBT, BUDGET_*, or VOID. Never earlier than the last compute capture | A preview after the last capture cannot select anything |
| Abandonment | Generating the salt **consumes** the F1-authorized attempt. Every terminal state after generation is retained with the commitment and shown in `STATUS`: VOID, deadline lapse, host loss or an interruption left unresolved. The service refuses a second admission under the same authorization (unique attempt key, boundary spec §7). A successor attempt needs a fresh operator authorization that cites the predecessor's terminal record | Spec §2.6: "No new attempt ID may be allocated automatically" |
| Alternative, not recommended now | A public randomness beacon round fixed in F1 after attempt registration. It removes administrator preview, but adds an external dependency and a signature verifier | — |

### 1.5 Proposed owner amendments

**(a) Boundary spec** `docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md`, §3. Insert a new subsection `### 3.1` after the paragraph that ends "…limited to trusted users: [Docker Engine security](…)." and before "The supervisor and G5 run from administrator-installed…":

> "### 3.1 Boundary set (AUDIT-2026-09-25-qualification-assurance-contract-delta#boundary)
> The requesting agent must be unable to: (B-1) alter installed execution, adjudication or worker code for an admitted release; (B-2) replace or edit captured evidence or the journal; (B-3) produce a counted attempt nobody sees, choose which attempt counts, or learn seed values before reveal; (B-4) grant itself activation authority; (B-5) present fixture or TEST_ONLY output as production evidence. Each retained mechanism cites the row it enforces. These rows rest on credentials and host permissions, not process roles: `qexec` is root-equivalent through Docker, and any agent-reachable administrator, `sudo`, Docker-socket, `qexec`, `qg5`, `qseal`, signing or deploy credential defeats them. Operational facts OF-1..OF-7 (listed in the S5 decision record) are verified by attended host read at provisioning, before any production-authority release, and after any access change. A row with an unverified fact is reported as unenforced. The disposable CI harness is evidence of mechanism, never of this boundary."

**(b) Track B umbrella** `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md`, §0.8. Append a row after O-4 (the umbrella body is closed; §0.8 is the named landing place):

> "| O-10 | Seed custody for F1 (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3) | **TB-F1** | F1 freezes `root_rng_namespace`, recipe `tb-s2-rng-v3` and this custody rule, and no salt or salt hash. `qexec` generates a 32-byte CSPRNG salt inside the admission of the single authorized attempt, after the F1 contract digest is bound, and publishes only `sha256(salt)` in the admission receipt. Seed values are withheld from `qclient` until the campaign is terminal. Generation consumes the attempt: every later terminal state, abandonment included, is retained and visible, and a successor needs a new operator authorization citing it. |"

**(c) Full-E1 spec** §2.4, first paragraph. After "Reuse `runner._run_stage`, provider/replay/source admission, `regime.domain_seed`, seed identities, …", add:

> "Production-class campaigns use the salted recipe `tb-s2-rng-v3`, which is `tb-s2-rng-v2` with the service-generated attempt salt added (umbrella §0.8 O-10). G5 re-derives seeds only from the revealed salt, after checking it against the admission commitment. Before reveal, the client plan view carries seed digests, not seed values. TEST_ONLY synthetic campaigns may keep `v2`."

### 1.6 Verification

- Before F1, the operator records an attended host-read attestation for OF-1..OF-7.
- **Salt tests:**
  - a contract in the pre-reveal state cannot derive seeds;
  - the revealed salt must hash to the admission commitment;
  - a salt not in canonical 64-hex form is refused at generation and at reveal;
  - `FETCH_PLAN_CHUNK` under the `client` role returns no seed value before reveal.
- **Abandonment tests:**
  - a second admission under the same authorization is refused;
  - a VOID after salt generation leaves a visible, counted terminal record.
- The delta's §10 routing hook stops printing `UNROUTED: boundary` and `UNROUTED: K3`.

### 1.7 Residual risk

- The administrator can read the salt before reveal. This is trusted by design (spec §3); the beacon alternative removes it.
- OF verification is attended, and it becomes stale when access changes.
- B-4 stays procedural until TB-I3.
- Deterministic domain separation is not a proof of independence (freeze-candidate §Seeds).

## 2. D2: N1 resource accounting

### 2.1 Recommended ruling

1. **Name the invariant; do not replace it.** The delta's "one outer cgroup per campaign (CPU, memory, wall)" is not a cumulative bound. `cpu.max` limits rate only, and spec §2.5 already says: "OS CPU-rate limits alone do not enforce cumulative CPU seconds." The accepted mechanism (§2.2) is the only cumulative bound, and **every model must keep it**.
2. **Keep per-phase reservation sizing for all phases** (N1…SEAL). Size PART_A from measured CPU at **maximum expansion**, as the budget-profile owner already states (`execution/profile.py:167`), and set it before S5's C3.
3. **Exhausted-campaign rule** (review point e), §2.4.
4. **No per-phase CPU number enters any statistical decision.** This is already true and should be pinned by a test.
5. *(Optional, the operator's call.)* The coordinator may set TEST_ONLY diagnostic ceilings as measured usage × a stated margin, recorded in the ledger. Production ceilings are frozen with F1 by the operator. The M13 round (C2, 2026-09-24) needed an operator ruling only because the packet barred ceiling changes.

### 2.2 The cumulative bound and the restart-surviving deadline today (review point c)

| Layer | Mechanism | File:line |
|---|---|---|
| Per-work payload | Kernel quota × lifetime ≤ payload reservation. The quota is `(cpu_ns − orchestration) × 10⁶ ÷ remaining_wall`, and the realized `cpu.max` is verified before the payload starts | `campaign_supervisor.py:177-194` (docstring: "cgroup v2 has no cumulative CPU cap"), `:197-221`, `:2641-2642` |
| Per-work lifetime | Guardian `RuntimeMaxUSec` (enforced by PID 1, not the service) plus `BindsTo` retiring the payload slice. `qg5` unit: the same pattern | `:309`, `:335-341`; `qg5` `:1713-1728` |
| Per-work controller | `LimitCPU` (RLIMIT_CPU) on the single-task guardian, inside the fixed orchestration charge | `:286-311` |
| Early stop | Guardian polls `cpu.stat`. The poll is the accounting path and the early stop, "never the enforcement" | `:2787-2792` |
| Campaign sum | Reserve only if settled + open reservations + new ≤ cap; unknown counters charge the full reservation; settle once | `campaign_store.py:2514-2532`, `:2908-2909`; `campaign_budget.py:45-50`, `:159-163`; `campaign_store.py:2988-3022` |
| Route feasibility | At binding, Σ phase ceilings ≤ cap (CPU and wall), otherwise `BUDGET_EXHAUSTED` before any draw | `campaign_store.py:2776-2783` |
| Deadline | The campaign's `deadline_boottime_ns` is its original start plus maximum wall, persisted. Each clock read checks boot ID and non-regression (`BUDGET_UNCERTAIN`) and the deadline (`BUDGET_EXHAUSTED`) | `campaign_store.py:2785-2787`, `:2619-2633` |
| Deadline before any campaign code | `bootstrap.py` arms an absolute `CLOCK_BOOTTIME` timer from the fixed argv before any campaign import. The argv value must equal the durable reservation deadline | `deploy/qualification/bootstrap.py:52-76`; `campaign_supervisor.py:224-237` |

Hence cumulative campaign CPU ≤ Σ over works of (quota × RuntimeMax + LimitCPU + helper bound) ≤ cap, and each term is kernel-enforced. The bound survives a service restart because BOOTTIME continues and the store persists. A reboot changes the boot ID, which makes the campaign `BUDGET_UNCERTAIN`: it fails closed, and cross-boot continuation is unsupported (spec §2.5). Linux evidence: S2 nodes `test_s2_payload_cpu_is_kernel_bounded_without_guardian`, `test_s2_deadline_kills_guardian_before_bootstrap_completes` and `test_s2_original_deadline_survives_service_downtime` (S2 acceptance, 2026-09-21).

A campaign-level cumulative bound through one outer cgroup would need quota_campaign × (deadline − start) ≤ cap. That would forfeit CPU during queues and downtime and throttle every phase to the campaign-average rate, and it still needs per-work settlement, because an idle slice is garbage-collected along with its counter (not verified on the host).

### 2.3 Per-phase, mixed and uniform campaign compared (review point d)

| Criterion | **Per-phase everywhere** (accepted) | **Mixed** (delta): per-phase for N1/N2; campaign scope for PART_A, RESULT, SEAL | **Uniform campaign**: every work sized from the remaining campaign allowance |
|---|---|---|---|
| Cumulative bound | Yes (§2.2) | Yes, only if campaign-scope works keep a per-work reservation. The "outer cgroup" alone is rate-only | Same as mixed |
| Forward complexity | One sizing rule. Each new phase needs a measured ceiling that fits the Σ-feasibility check | **Two** rules across `reserve_work` (`:2872-2878`), the binding feasibility (`:2776-2783`), the funding projection, the closed profile phase set (`profile.py:195` requires every `PHASES` entry) and T05's result/seal reservations. A phase-conditional rule is the defect class C2 traced (N1-only sites, 2026-09-24) | One rule and no ceilings, but it must still hold back a tail for G5, RESULT and SEAL, which reintroduces per-phase amounts for the tail |
| Tail liveness | A runaway compute stops at its ceiling, and G5/RESULT/SEAL stay funded | Runaway PART_A can consume the tail unless one is held back | Same as mixed |
| Migration risk against accepted evidence | None | N1/N2 untouched. T05 (built, not accepted) changes. New budget-profile version | New budget profile and release, then re-runs of the S2/S3/S4 Linux node sets (15/19/22) under it; contract decisions 1 and 4 require fresh attempts |
| Cost to reach S5 | PART_A ceiling measurement plus a ruling or the optional coordinator rule. Stage plumbing (below) | Plumbing plus the new seam and its tests | Plumbing plus a rewrite and full Linux re-acceptance |
| Statistical protection | Identical in all three: no-redraw is `campaign_store.py:2896-2901` plus plan binding, not budget size. Depth is a planning number (ADR Deviation A1) | Identical | Identical |

**Plumbing every model pays at S5:** role branches `n2_worker`/`n2_g5` (`campaign_supervisor.py:1520-1530`), the UID map (`:2544-2555`), `PROGRESSION_PHASES` (`campaign_store.py:180-182`), `CHECKPOINT_ADVANCES` and `CHECKPOINT_PROGRESSION_STATES` (`:120-124`), and the literal state set at `campaign_supervisor.py:2504`. The delta's §10 N1 hook counts 4 sites in the supervisor and 32 in the store at this head. Those are progression sites, not sizing sites, and none of them disappears under either alternative. C2's liveness generalization (`_live`, `:1278-1287`) has already made the accounting side phase-generic.

**Falsifier:** revisit the uniform model if PART_A's maximum-expansion CPU cannot be bounded ahead of time. That would mean a ceiling covering maximum expansion either fails the Σ-feasibility check against any admissible cap or cannot be measured before C3.

### 2.4 Exhausted campaign with a valid stage result (review point e)

Rule:
- A committed stage assessment is **retained as evidence and never revoked**.
- Exhaustion ends all further work: no new reservation, dispatch, assessment, result or seal.
- Whole-campaign completion (`RESULT_COMMITTED_*`, `SEALED_PASS`) is withheld unless its own receipt was committed before the exhaustion event.
- A committed stage FAIL stays binding in the attempt's record and can never be recast as "incomplete" to justify a successor attempt.

This matches current code:
- `_settlement_terminal` ends authority from the progression states, and the receipt stays historical (`campaign_store.py:2612-2617`, the S3 P1 fix);
- spec §2.5: "Deadline reached means no new authority even if computation already passed";
- T05 refuses a seal on `REFUSED_BUDGET_STATES` (branch, T05 follow-up 2026-09-22).

### 2.5 Proposed owner amendments

**(a) Slices plan** `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`, contract decision 3. Append after "…not independent full-size allowances per process.":

> "The cumulative bound is per work and kernel-enforced: payload quota × guardian `RuntimeMaxUSec` plus the guardian's `LimitCPU` never exceeds that work's reservation, and settled charges plus open reservations never exceed the frozen cap (AUDIT-2026-09-25-qualification-assurance-contract-delta#N1). A campaign-level rate quota is not a substitute. Every phase, PART_A, RESULT and SEAL included, reserves its installed phase ceiling; PART_A's covers maximum expansion. No per-phase CPU figure enters a statistical decision. [Optional:] TEST_ONLY diagnostic ceilings are set by the coordinator as measured usage × a recorded margin; production ceilings are frozen with F1 by the operator."

**(b) Full-E1 spec** §2.5, last paragraph. After "Deadline reached means no new authority even if computation already passed.", add:

> "A stage assessment committed before exhaustion remains evidence and is never revoked; exhaustion ends all further work, and whole-campaign completion (result commit or seal) is withheld unless its own receipt was committed before the exhausting event. A committed statistical FAIL is never recast as incomplete."

### 2.6 Verification

- A test that no acceptance or adjudication path reads a phase CPU figure.
- Exhausted-campaign tests for N1 and N2 on the service path:
  - a committed N1 FAIL followed by a `N1_G5` settlement overrun gives `BUDGET_EXHAUSTED`, the receipt is `historical=true`, and no RESULT reservation is possible;
  - the same after a committed `PART_A_READY`.
- The PART_A ceiling is measured at maximum expansion on Windows and Linux and recorded before C3; `bind_budget` feasibility passes for the v7 profile.
- The three S2 nodes in §2.2 stay green at S5 (reuse of unchanged evidence).

### 2.7 Residual risk

- An overrun detected at settlement ends the campaign after the fact. The kernel bound caps its size, not its occurrence.
- The per-phase ceilings still need calibrating for each new phase.
- Cross-campaign memory interference on a shared host parent can invalidate every attempt (S2 clarification).
- Reboot is terminal.

## 3. D3: N2 bounded same-sample re-execution

### 3.1 Recommended ruling

Adopt R1–R10 below as policy. S5 freezes with today's terminal IN_DOUBT. The rule is then built as its own bounded slice after S5's acceptance and before S8. Adding it changes a terminal campaign state into a re-execution-eligible one: `record_work_transition` and `recover_work` both call `_settlement_terminal(state, 'IN_DOUBT')` (`campaign_store.py:3157-3160`, `:3210-3213`). That change must not ride inside S5.

**Why adopt it:**
- Under a fixed plan and determinism, re-execution cannot change an outcome.
- The alternative after a real interruption is a separately authorized new attempt. Under K3 that attempt gets a **new salt**, which is a genuine redraw.
- So a bounded same-sample retry is the stronger no-redraw posture for a long production run.
- A3 means every service restart destroys every running work (S2 acceptance, recorded preconditions).

### 3.2 Evidence

| Fact | File:line |
|---|---|
| Today: START_INTENT/RUNNING without capture → IN_DOUBT → campaign terminal; recovery commits before cleanup | `campaign_store.py:3157-3160`, `:3180`, `:3210-3213`; spec §2.6 table |
| One compute reservation per phase ("no replacement draws"); only a *signing* retry is linked (`signing_retry_of`), and never for N1/N2/PART_A | `campaign_store.py:2879-2901` |
| Fence at the store: `CAPTURED` is legal only from START_INTENT/RUNNING, so a late original cannot publish after IN_DOUBT | `campaign_budget.py:95-98` |
| Fence at the OS: a recovery owner is one-use, and completion binds a cleanup event (absence proof) | `campaign_supervisor.py:3048-3106`; `campaign_budget.py:171-181` |
| N1/N2 workers write **one** frame at the end, so an interrupted N1/N2 retains **zero** complete records (the typical case) | `execution/worker.py:137-149` |
| Part A retains the initial-prefix artifact, fsynced before expansion (S5-D1) | S5 packet §0.5 |
| Part A has a wall-time *completion* predicate: the pilot aborts on a predicted overrun, which changes whether a result exists, not its outcomes | `qualification/part_a.py:185-191` |
| Thread-count environment is pinned in the container body | S2 acceptance, G5 addendum |

### 3.3 The rule (review point f)

| # | Condition |
|---|---|
| R1 **Eligibility** | Only a compute work (N1, N2, PART_A) in IN_DOUBT from process interruption on the **same boot**, with no finalized capture. Never: CAPTURED, SIGNED or COMPLETED works; any committed assessment (a **completed statistical FAIL is never eligible**); BUDGET_UNCERTAIN (reboot or clock); a resource overrun or OOM (`BUDGET_EXHAUSTED`); VOID. Only the service's recovery path triggers it; no client operation exists |
| R2 **Fence first** | The re-execution may be reserved only after the original work's recovery completed with an absence proof for its guardian, payload slice, container and `qg5` unit, and the store holds it in IN_DOUBT (so no late `CAPTURED`). If absence cannot be proven, it stays terminal |
| R3 **Identities committed before execution** | The retry's reservation carries `reexecution_of=<work_id>` and a byte-identical `input_sha256` and checkpoint plan (seed inventory, release, image, profile, source and predecessor receipt). Any difference refuses |
| R4 **Original envelope and deadline** | Same installed phase limits (no enlargement). The retry is charged from the same cap **on top of** the interrupted work's charge (unknown = full reservation, no refund), under the campaign's **original** absolute BOOTTIME deadline (no reset or extension). If it does not fit, the campaign ends exhausted |
| R5 **Attempts retained** | The interrupted work, its observations and any saved bytes stay in history as IN_DOUBT; the retry is a new linked work under the **same** attempt ID and checkpoint key |
| R6 **Retained-prefix check** | If the interrupted attempt retained complete records (Part A's initial-prefix artifact), the retry's corresponding bytes must be identical, compared on the statistical record fields. Declared runtime-observation fields are excluded, and that list is frozen in the rule |
| R7 **Zero retained records** | Allowed only when the installed release carries a recorded per-stage reproducibility demonstration: two complete executions of that checkpoint's plan on the pinned image give byte-identical capture bytes, and all R3 identities are equal. Otherwise the work stays **unresolved** (terminal IN_DOUBT) |
| R8 **Disagreement** | Any R6 mismatch, or any divergence found later, is an **incident**: the campaign becomes terminal (a new reason, e.g. `REPRODUCIBILITY_INCIDENT`), never a result and never retry-eligible, and the release's reproducibility record is suspended pending review |
| R9 **Limits** | At most one re-execution per interruption and two per campaign. An interruption of the second re-execution is terminal |
| R10 **No new namespace** | Repeated interruption never allocates an attempt ID, salt, seed or plan. A timing-driven abort on a retry (`part_a.py:185-191`) is an operational terminal, not a result |

### 3.4 Proposed owner amendments

**(a) Full-E1 spec** §2.6, table row "START_INTENT or RUNNING, no complete durable capture". Replace its recovery cell with:

> "Persist IN_DOUBT before cleanup; stop owned worker. Never relaunch, except one bounded same-sample re-execution under the rule below."

After the paragraph ending "…outside retry semantics.", add:

> "**Bounded same-sample re-execution (AUDIT-2026-09-25-qualification-assurance-contract-delta#N2).** A compute checkpoint (N1, N2 or PART_A) left IN_DOUBT by process interruption on the same boot, with no finalized capture, may be re-executed once, and at most twice per campaign. The service may do so only after the original work's absence is proven and its IN_DOUBT state is durable, using the byte-identical plan and seed inventory, the same installed phase limits, and the campaign's original deadline, charged on top of the interrupted work's charge. The interrupted work stays in history. Retained complete records must match the re-execution on their statistical fields. With none retained, re-execution requires the release's recorded per-stage reproducibility demonstration; otherwise the work stays IN_DOUBT. A mismatch is a terminal reproducibility incident, never a result. Captured work, committed assessments (a statistical FAIL included), overruns, BUDGET_UNCERTAIN and VOID are never eligible, and no re-execution allocates an attempt, salt, seed or plan."

**(b) Full-E1 spec** §5, second bullet. After "redraw under the same attempt", add: "(a §2.6 bounded same-sample re-execution is not a redraw)".

**(c) Full-E1 spec** §2.4, last paragraph. After "…makes that operation IN_DOUBT.", add: "§2.6's bounded re-execution reruns the whole checkpoint from its first panel under the same plan; it never resumes panels."

**(d) Slices plan** contract decision 6. After "Missing capture never licenses another draw;", add: "a spec §2.6 bounded same-sample re-execution is not a draw;". In **S5 Behavior**, after "…no panel resume, replacement pilot or checkpoint rerun.", add: "S5 builds this terminal subset; the §2.6 re-execution is a later slice before S8, and S5-D1's retained initial prefix is its R6 input."

### 3.5 Verification

- **Per-stage reproducibility test** on the pinned runtime: two runs, byte-identical captures, recorded in release evidence.
- **Scenario tests:**
  - an interrupted N2 then re-executed on zero records, with the reproducibility record present, succeeds;
  - the same without the record stays IN_DOUBT;
  - a Part A run interrupted after the initial prefix is re-executed with a matching prefix;
  - an altered prefix gives the incident terminal.
- **Refusal tests:**
  - a CAPTURED, FAIL-committed, overrun, BUDGET_UNCERTAIN or VOID work refuses a re-execution;
  - a third interruption is terminal;
  - a changed `input_sha256` refuses;
  - a re-execution before the absence proof refuses.
- **Linux:** kill a guardian mid-N2, then restart, re-execute and commit through the real `qg5` unit.

### 3.6 Residual risk

- Undetected nondeterminism: a reproducibility demonstration is evidence for the tested conditions, not proof, especially at reduced TEST_ONLY depth compared with production depth.
- Reboot stays terminal.
- Re-execution consumes allowance, so a late interruption may end the campaign exhausted anyway.

## 4. Sequencing against the S5 hold

- **Ruling D2** is what the S5 freeze needs. The freeze also needs a measured PART_A ceiling at maximum expansion, or the optional coordinator rule.
- **D1 and D3** can be ruled at the same time. They need no S5 change beyond the text in §1.5(c) and §3.4(d).
- **K3 implementation** belongs with TB-F1 (before F1).
- **N2 implementation** belongs in a slice between S5 and S8.

After the rulings, the operator may release the hold by a new ledger entry. This draft does not release it.

## 5. Open questions and unverified items

1. Whether a committed statistical FAIL on an exhausted campaign should still count as a FALSIFIED attempt under ADR §4 without a result commit. The rule above keeps the FAIL binding in the record; this is a statistical-owner question.
2. "Original deadline" in R4 is read as the **campaign's** original BOOTTIME deadline, not the interrupted work's own (the latter would make a late retry infeasible). This needs confirming.
3. Not verified on a host: whether a garbage-collected systemd slice keeps its `cpu.stat` history (§2.2), and PART_A's maximum-expansion CPU (not measured).
4. Whether Part A or N2 captures carry timing fields that R6 must exclude. This needs a read of the capture schema at S5's C3.
5. Every OF (§1.3) is unverified by this draft. It read no host, credential store or secret list.
6. The unanchored §0 inputs of the delta audit remain unrecorded (delta §0).

## Verification of this draft

```bash
# K3 recipe and root (expect no salt yet)
grep -n "payload = \|return int.from_bytes" ops/c1_rail/qualification/regime.py
grep -n "root_rng_namespace" ops/c1_rail/qualification/seed_identity.py ops/c1_rail/qualification/contract.py
# Client may fetch plan chunks; plan carries seed values
grep -n "'client':" ops/c1_rail/qualification/execution/campaign_protocol.py
grep -n "'seed':seed" ops/c1_rail/qualification/seed_identity.py
# Cumulative bound = quota x RuntimeMax per work
grep -n "cgroup v2 has no cumulative CPU cap\|never the enforcement" ops/c1_rail/qualification/execution/campaign_supervisor.py
# No replacement draws; IN_DOUBT terminal
grep -n "no replacement draws\|_settlement_terminal(state, 'IN_DOUBT')\|_settlement_terminal(state, target)" ops/c1_rail/qualification/execution/campaign_store.py
# Delta N1 hook (4 / 32 at main@24e3843)
grep -c -E "PROVISIONAL|BOUND|N2_READY|PART_A_READY" ops/c1_rail/qualification/execution/campaign_supervisor.py ops/c1_rail/qualification/execution/campaign_store.py
```

---

## Coordinator review (2026-09-26): ACCEPTED AS INPUT; S5 stays held

Reviewer: the coordinating session. Artifact: `dbb38b8`. Citations spot-checked at `main@24e3843`, under `ops/c1_rail/qualification/execution/`:
- `campaign_protocol.py:90-95`: the client may `FETCH_PLAN_CHUNK`;
- `checkpoint_plan.py:222-233` → `seed_identity.py:35-40`: plan chunks carry `seed`;
- `campaign_supervisor.py:177-194`: the docstring states that the rate quota × `RuntimeMaxUSec` bounds cumulative payload CPU, because cgroup v2 has no cumulative cap;
- `worker.py:137-149`: one fsynced frame is written at the end.

**Where this draft departs from earlier proposals** (surfaced for the operator; not adopted):

| Topic | Earlier proposal | This draft | Coordinator note |
|---|---|---|---|
| N1 accounting | Audit: narrow to campaign scope (the mixed model); executive review: approve simplification in principle | Keep the accepted **per-phase** model for S5. Reject the mixed and uniform models for now. Add four narrowings (explicit invariant, exhausted-campaign rule, no per-phase CPU in acceptance, measured TEST_ONLY ceilings) | Evidence-backed: the cumulative bound already exists, and uniform needs S2–S4 Linux re-runs. The operator chooses between "simplify now" and "narrow in place". Both keep the exhausted-campaign rule |
| K3 seed custody | Audit: salt committed by hash in F1, revealed at dispatch | The service generates the salt at admission, after the F1 digest is bound. F1 carries the custody rule, not a hash. Seeds are withheld from the client until the campaign ends | Addresses the creator-preview gap the executive review named. It needs a **code change**: the client plan view must carry digests only (new finding), before F1 |
| N2 recovery | Bounded same-sample re-execution before S5 | Adopt the policy (R1–R10) now; build it as its own slice after S5 and before S8; S5 freezes with terminal IN_DOUBT | A scheduling choice for the operator. Because a single end frame makes the zero-record case the norm, the reproducibility demonstration carries the rule |

**Open items routed:**
- **Q1** (a FAIL on an exhausted campaign) → the statistical owner.
- **Q2** (the "original deadline" is the campaign's) → consistent with the executive review's "retain the original resource envelope and deadline"; confirm at the ruling.
- **Q3/Q4** (host `cpu.stat` retention; PART_A CPU at maximum expansion; timing fields in the prefix comparison) → S5 C3.
- **Q5** (seven operational facts) → an attended operator host read before any boundary counts as enforced.
- **Q6** (landing place) → rulings are recorded in the S5 hold ledger entry of the execution-slices plan, with dated amendments to each named owner. Umbrella §0.8 row O-10 only if the operator prefers.

