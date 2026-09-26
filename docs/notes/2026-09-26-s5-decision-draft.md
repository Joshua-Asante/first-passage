# S5 decision draft: assurance boundary, N1 accounting and N2 recovery (proposed rulings)

**Status:** draft decision packet for the operator, revised 2026-09-26 after the executive review, with consistency-review corrections of the same date (listed after the revision table). It changes no owner document, code, contract, ceiling or statistic, and it does not release the S5 freeze. That freeze stays **HELD** under the [ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25). Every amendment below is *proposed* text for its named owner. The directions below were recommended by the executive review (2026-09-26), except items marked as the drafter's addition. ~~operator ruling pending. Nothing here is ruled.~~ The [operator ruling of 2026-09-26](#operator-ruling-2026-09-26-in-session) adopted D1–D3 as S5 directions in its own words, which that section quotes; the rest of each direction's text here remains the draft's recommendation. The ruling also retained RC-6 and set the resource-envelope preparation; S5 stays HELD.
**Dispatch:** Task 2 of the B–D packet card (`docs/briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md` at `f311578`). The card's own requirements and the operator's executive-review points (a)–(f) apply.
**Source anchors:** `main@24e3843`, read 2026-09-26. The sources were read, not run. No Linux run, probe or private source was used. Line numbers are at that head. The revision re-read the cited code at the same head; no code changed between `24e3843` and this branch.
**Inputs:** the [contract-delta audit](audits/2026-09-25-qualification-assurance-contract-delta.md) (§5.1, rows K3/N1/N2, §10), the [execution-slices plan](../superpowers/plans/2026-09-18-full-e1-execution-slices.md) (contract decisions 1–6, S2 clarification, S2/S3 and coordinator checkpoint C2 entries, S5), the [N1 boundary spec](../superpowers/specs/2026-09-17-qualification-execution-boundary-design.md) §3/§7, the [full-E1 spec](../superpowers/specs/2026-09-17-protected-full-e1-campaign.md) §2.4–§2.8/§5, the [release-binding ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) §2a T10–T11/§2b, the [S5 packet draft](../briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md), and the code under `ops/c1_rail/qualification/`.

## Operator ruling 2026-09-26 (in session)

Operator decisions, 2026-09-26. Source: "operator ruling and coordination, 2026-09-26, relayed in session", together with the operator's structured-question answers the same day (the option selected for these rulings: "Adopt D1–D3 directions, keep hold"). The written ruling is the governing text; it supersedes any shorthand recording of the same rulings made from the structured-question answers. The record is the [S5 hold ledger entry 2026-09-26](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26) (PR #517); this section is a derived mirror of it for readers of this draft. Where this draft says a D1–D3 direction is recommended with operator ruling pending, this ruling governs.

- **D1–D3: ADOPTED as S5 directions**, in the ruling's words below. The rest of this draft's D1–D3 text (§0 and §1–§3: for example the §5.1 boundary set B-1..B-5 and its conditions, the §2.1 direction items and the rule R1–R10) is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2. In the ruling's words:
  - **D1** (§0, §1): "Service-generated salt; private worker/G5 access; no client disclosure while computation or recovery remains possible."
  - **D2** (§0, §2): "Retain per-phase accounting."
  - **D3** (§0, §3): "Implement bounded same-sample recovery in a separate slice after S5 and before S8."
- **Admission crash, accepted by the operator** (§1.4): "Joshua explicitly accepts that an admission crash after salt binding but before capture consumes and closes the attempt, preserving its identity and salt without continuing admission or generating another."
- **RC-6 retained** (§5): "Retain RC-6."
- **Gates for the seed view and host attestations.** The ruling directs: "Assign seed-view implementation and host attestations to their specified gates." It names no gate, owner, slice or record location. The seed view's gate in this draft: the client plan-view seed change (seed digests only) before F1, with an F1 admission check that refuses while the client can fetch seed values (§1.4, RC-4). For the attended host reads OF-1..OF-7 this draft specifies two gate sets that differ for OF-5..OF-7: the §1.3 table and the §1.5(a) proposed owner text (§6 Q12). The record does not choose between them; the discrepancy stays open for the coordinator's owner-text and RC-5 work. The assignment is not yet made: RC-4 and RC-5 stay unmet until their owner records hold the text each row requires (§5).
- **Resource-envelope decision** (ruling §6; §2.1 items 7–8, RC-3). The coordinator prepares a concrete measurement proposal identifying the maximum-expansion workload, the reference runtime, CPU/wall/memory capture, the proposed margin and budget feasibility, and returns the measurement-and-margin rule for operator approval. No numerical rule is approved yet. Once the rule is approved, the coordinator may apply it to TEST_ONLY diagnostic ceilings with recorded evidence. Production budgets remain separately governed. This preparation does not authorize held S5 execution. S5 measurement preparation is a separate bounded handoff; combined acceptance stays with the coordinator.
- **Hold kept.** In the ruling's words, S5 release remains "subject to their recorded gates", and the resource-envelope preparation "does not authorize held S5 execution". The coordinator returns "an RC-1–RC-6 status table and, when supported, a concrete S5 release proposal". S5 therefore stays **HELD**. The release conditions are this draft's §5 RC-1..RC-6, and under §5 only an operator ruling recorded as a new ledger entry releases the hold; that release gate is this draft's, not ruling text.
- **Owner text.** After the stack (#515–#518) lands, the coordinator applies the decisions to their canonical owners and reconciles dependent wording. The proposed owner amendments in §1.5, §2.5 and §3.4 are not yet applied; RC-2 requires them accepted by the operator and applied.

**Not granted:** no S5 release, freeze, dispatch or execution; no approved numerical measurement-and-margin rule; no statistical dispatch; no Gate B, C or D acceptance; no production, activation or live authority. The ruling does not independently add merge authorization. Its closing boundary: "Gate A stays accepted. B–D acceptance, S5 release, order-producing drills, production qualification, deployment and arming remain subject to their recorded gates."

## Revision 2026-09-26 (executive review)

The executive review of 2026-09-26 corrected this draft. The recommendations are revised in place. The coordinator review appended at the end reviewed the pre-revision text (`dbb38b8`) and is kept as written; where it differs from the revised text, this revision governs. Every direction remains recommended (executive review 2026-09-26); operator ruling pending. S5 stays HELD.

| Section | Change |
|---|---|
| §0 | Summary restated to the corrected directions |
| §1.1–§1.3 | OF-1..OF-7 are **production acceptance obligations**. An unverified fact now reads "enforcement not established", not "unenforced": it shows missing evidence, not missing enforcement |
| §1.4 | G5's **private** seed access, needed to adjudicate checkpoints before the campaign ends (`evidence.py:981-989`, `:1310-1316`), is separated from disclosure to the client. Public reveal waits until the campaign is irrevocably closed to computation and recovery; a retry-eligible IN_DOUBT does not reveal. New crash-safe admission row, which states what a crash after the salt-binding commit produces (a consumed, closed attempt). The worker derives seeds from the root in its input, so it receives the salt; OF-7 now names it and the administrator. The plan-chunk finding and the client plan-view change are kept |
| §1.5–§1.7 | Owner text corrected to match. The sentence "G5 re-derives seeds only from the revealed salt" is withdrawn. OF-1..OF-7 are written into the boundary-spec text. The umbrella row O-10 is optional and lands after O-9, the table's last row; §1.5(c) no longer depends on it. New §1.5(d) amends spec §2.2a for the client plan view. Tests added |
| §2 | The per-phase model is kept for S5; the executive review revised its earlier simplification recommendation after the §2.3 comparison. Claims that every cumulative bound needs per-work reservations are narrowed to the current design. Direction items added: receipt consumers, coordinator TEST_ONLY ceilings only within a recorded measurement-and-margin rule, production budgets governed separately. §2.4 separates consumers that grant new action from statistical accounting, and states that exhaustion ends an earlier completion's authority, not its record. §2.2's systemd/cgroup semantics are labelled by basis |
| §3 | Recovery rule tightened: original worker terminated and fenced; sample, source, runtime and configuration identities; no renewed deadline or allowance; failed attempts retained; a predeclared comparison schema; no public reveal while recovery remains possible. Two agreeing repeats at reduced depth are not proof of production determinism. §3.4 also amends spec §2.6's "VOID, terminal abort, IN_DOUBT or BUDGET_UNCERTAIN" row |
| §4, §5 | Sequencing updated; §4 separates what S5's build needs from what its release needs. New §5, S5 release conditions, labelled RC-1..RC-6 so they do not collide with coordinator checkpoints C1/C2 or S5 packet Checkpoint C3. RC-6, and the operator fixing the measurement-and-margin rule (§2.1 item 7), are the drafter's additions |
| §6 | Former §5. Q7–Q11 added |

The kept coordinator review uses the pre-revision numbering. Its Q1–Q5 match §6 items 1–5. Its "Q6 (landing place)" is the landing-place question (now §1.5(b), optional O-10), not §6 item 6. Its "S5 C3" is S5 packet Checkpoint C3, not release condition RC-3.

## Consistency-review corrections (2026-09-26, after the executive review; these govern)

A consistency review of this draft against the B–D decision packet, the UB-8 comparison, the route drill-plan draft and the allocation map made the corrections below. Each governs over the text it replaces; the replaced wording is quoted here. They are drafting corrections, not operator rulings. Every direction remains recommended (executive review 2026-09-26); operator ruling pending. S5 stays HELD.

| Where | Was | Now | Why |
|---|---|---|---|
| §1.5(a), quoted anchor | "…limited to trusted users: `[Docker Engine security](…)`." | The same anchor with the owner's real link target | The placeholder rendered as a broken link. The boundary spec §3 paragraph ends with the link to `https://docs.docker.com/engine/security/`. The proposed amendment is unchanged |
| §4, second bullet | "S5's **build** needs from them only the text in §1.5(c) and §3.4(d)." | S5's build needs only §3.4(d). §1.5(c) is release owner text under RC-2, not a build prerequisite | §1.5(c) lets TEST_ONLY synthetic campaigns keep `tb-s2-rng-v2` and asks no S5 code change. §0 D1 already says S5 needs "not the K3 build", and §0 D3 says "S5's build needs only the §3.4(d) text" |
| Labels (new note) | — | B-1..B-5 are the contract-delta audit's §5.1 boundary rows. D1–D3 and RC-1..RC-6 are local to this draft | Other drafts of the same date reuse the letters. The B–D decision packet has its own B-1..B-13 and D-numbers, and the rail spec's S2 cites an RC-9. None of those is an item here. "S5" here is always the qualification S5 freeze, not the rail spec's S5 (scoped exit/flat) |

## 0. Summary

| # | Decision | Recommended direction (executive review 2026-09-26; ~~operator ruling pending~~). Each row opens with the direction as [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session) adopted it, in its words; the rest of the row is the draft's recommendation | Owners amended | Blocks |
|---|---|---|---|---|
| D1 | §5.1 boundary B-1..B-5, with K3 seed custody | **D1 adopted as an S5 direction by operator ruling 2026-09-26, in its words:** "Service-generated salt; private worker/G5 access; no client disclosure while computation or recovery remains possible." The operator accepts that an admission crash after salt binding but before capture consumes and closes the attempt, preserving its identity and salt without continuing admission or generating another (§1.4). The ruling directs that seed-view implementation and host attestations be assigned to their specified gates; no assignment is made yet, so RC-4 and RC-5 stay unmet ([ruling](#operator-ruling-2026-09-26-in-session)). *The rest of this cell is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2:* **Adopt, with conditions.** A boundary's enforcement is established only by an attended host read of its operational facts (OF-1..OF-7, §1.3), which are production acceptance obligations. For K3 the **service** generates the salt; the salt and the consumed attempt are durably bound before any preview-capable work. F1 carries the custody rule, not a salt hash. `qexec`, the worker (through its read-only input) and G5 hold private seed access during the campaign; the client gets seed values only after the campaign is irrevocably closed. Before F1 the client plan view carries seed digests only | Boundary spec §3; full-E1 spec §2.2a, §2.4; umbrella §0.8 O-10 optional (TB-F1) | K3 and the client plan-view change before F1; OF before any production-authority release. S5 (TEST_ONLY) needs the ruling and the §5 conditions, not the K3 build |
| D2 | N1 resource accounting | **D2 adopted as an S5 direction by operator ruling 2026-09-26, in its words:** "Retain per-phase accounting." The resource-envelope decision (ruling §6) governs §2.1 item 7 and RC-3. *The rest of this cell is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2:* **Keep the accepted per-phase model for S5**: the per-work cumulative bound and per-phase reservation sizing for every phase, PART_A/RESULT/SEAL included. Do not adopt the mixed or the uniform model for S5. Direction items in §2.1 | Slices plan contract decision 3; full-E1 spec §2.5 | S5 release (needs a defensible measured PART_A envelope, §5) |
| D3 | N2 interruption recovery | **D3 adopted as an S5 direction by operator ruling 2026-09-26, in its words:** "Implement bounded same-sample recovery in a separate slice after S5 and before S8." *The rest of this cell, including the rule R1–R10, is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2:* **Adopt bounded same-sample re-execution as direction** (§3.3 R1–R10), built as its own slice after S5 and before S8. S5 keeps today's terminal IN_DOUBT, the conservative subset | Full-E1 spec §2.4, §2.6 (two table rows and a new paragraph), §5; slices plan contract decision 6 and S5 text | The recovery slice before S8, and production F1 as a policy. S5's build needs only the §3.4(d) text; S5's release needs every §5 condition |

**Mixed versus uniform (review point d), in one line:** a uniform campaign model beats the mixed model on forward complexity, because the mixed model's phase-conditional sizing rule is the defect class coordinator checkpoint C2 found. The mixed model beats the uniform model on migration risk. Neither, as specified, removes the reservation and settlement machinery: the current code's only cumulative CPU bound is per work (§2.2), and neither proposal specifies another cumulative mechanism. The remaining cost of reaching Part A is stage plumbing that every model pays (§2.3), so for S5 the accepted per-phase model wins.

## 1. D1: assurance boundary B-1..B-5 and K3 seed custody

### 1.1 Recommended direction

**D1 adopted as an S5 direction** by [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session), in its words: "Service-generated salt; private worker/G5 access; no client disclosure while computation or recovery remains possible." S5 stays HELD. *The rest of §1 (the recommendation below, the B-1..B-5 boundary set and its conditions, the OF table and the custody rules) is the draft's recommendation and evidence, not ruling text, except the ruling quoted in §1.4; its owner-text form is reviewed under RC-2.*

The draft recommends: adopt §5.1 as the closed set of actions that must stay impossible for the requesting agent. Each row's enforcement rests on operational facts about credentials and host permissions, not on process roles. Enforcement is **established** only when the operator's attended host read records those facts. Until then it is **not established**: that describes the evidence, and is not a finding that the row is breached. The reasons:

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
| B-3 counted attempt | Once-only compute reservation (`execution/campaign_store.py:2896-2901`); unique execution key (boundary spec §7) | K3: a seed preview can happen **outside** the service (§1.4). Today the client role may fetch plan chunks (`execution/campaign_protocol.py:92`), the service returns slices of the whole stored plan (`execution/campaign_store.py:2409-2434`), and the plan carries seed values (`qualification/checkpoint_plan.py:222-233` → `seed_identity.py:35-40`, the `seed` field) |
| B-4 activation | `c1_rail_arm.py` interlock; per-session GO | Not machine-enforced on the host (see §1.1). Held by OF-5/OF-6 until TB-I3 |
| B-5 fixture output | Authority class and `production_execution=false` in the release/profile (slices plan, Global constraints) | Release install is an administrator act (OF-1), not a merge. Branch protection alone does not enforce B-5 |

### 1.3 Operational facts: production acceptance obligations (review point a)

OF-1..OF-7 are **production acceptance obligations**. Each is verified by an attended operator host read and recorded before the gate in its **When** column. None gates the TEST_ONLY S5 build, but each needs an assigned owner before S5 is released (§5 RC-5).

| OF | Fact (must hold) | Protects | Verification (operator-attended, recorded) | When |
|---|---|---|---|---|
| OF-1 | No account or environment in which an agent session runs can use administrator, `sudo`, `docker`-group or `/var/run/docker.sock` access on the production qualification host. That includes the operator's own workstation account when agents run under it | B-1, B-2, B-3, B-5 | Host: `getent group sudo docker`, `stat` of the socket, `sudo -l -U <user>` for each login; workstation: no host SSH key, token or agent-forwarded credential reachable by the agent's account | Host provisioning; before any production-authority release; after any access change |
| OF-2 | No agent can authenticate as `qexec`, `qg5`, `qseal` or the administrator, and no polkit rule grants `manage-units` to an agent-reachable UID | B-1..B-3 | Host: `/etc/polkit-1/rules.d` listing; `authorized_keys` per principal | Same |
| OF-3 | Execution, result, seal and operator-VOID private keys are unreadable by agent-reachable UIDs. They are absent from every worktree, every CI secret visible to an agent-editable workflow, and every store the agent can reach | B-2, B-3 (receipts), K7 | Key-path owner/mode read; `gh secret list` compared against the workflow files; worktree scan by filename, not content | Same |
| OF-4 | The key-enrollment and trust-domain inputs are writable only by the operator | B-1, B-3 | Owner/mode of the enrollment files on the host | Same |
| OF-5 | No agent holds rail-host deploy credentials (Fly token or flyctl session), write access to the rail `/data` volume, or broker credentials | B-4 | Operator reads the agent environments' credential stores; Fly access list | Before any arm; each session GO |
| OF-6 | If E3 is adopted, the operator GO signing key is off-host and never loaded where an agent runs | B-4 | Key custody record | TB-I3 |
| OF-7 | Before public reveal, the seed salt (§1.4) is readable only by the trusted administrator (OF-1), `qexec`, the worker's read-only input (from which the worker can derive every seed of the campaign) and `qg5`'s private adjudication access | B-3 (K3) | Mode/ownership of the salt row and objects; negative client-fetch test (§1.6) | Before F1 admission |

A row whose OF has not been verified is reported as **enforcement not established**. That is not evidence that enforcement is absent, and the row is never reported as assumed.

### 1.4 K3 seed custody (review point b)

A hash commitment in F1 (the delta's form) needs the salt to exist before F1. Its creator could then preview outcomes with the source and the code, and decide whether to freeze. The direction therefore makes the **service** the generator and places generation **after** the attempt is durably admitted and **before** any preview-capable work.

Two kinds of access are kept apart:
- **Authorized internal access** is what the service needs to run and adjudicate the campaign. `qexec` derives the plan. The worker does not receive seeds: it derives them itself from the contract root in its read-only input (`execution/compute.py:21` passes `contract.replay.root_rng_namespace`; `runner.py:95` and `part_a.py:140` call `domain_seed(root=...)`). Under the salted recipe the worker therefore receives the salt in that input and can derive every seed of the campaign; OF-7 covers it. This draft keeps that design; the alternative, a worker that consumes plan-supplied seeds instead of the root, would add a worker change to the K3 build. G5 re-derives plans and seeds for every checkpoint it adjudicates while the campaign is still running. The N1 path rebuilds the whole plan and requires byte equality (`evidence.py:981-989`); the joint N2 path re-derives the seed inputs (`evidence.py:1310-1316`); both are reached from G5 (`execution/g5.py:536-546`). Spec §2.7 already requires this: "G5 independently derives expected plans from the frozen contract".
- **Disclosure** releases the salt or seed values to the requesting client. That is the preview K3 closes.

| Question | Proposed rule | Grounding |
|---|---|---|
| Who generates | `qexec`, `secrets.token_bytes(32)`. Never the operator, an agent or the F1 author | Spec §2.2: `qexec` is trusted and owns plans. Today's root is an author-chosen contract string (`contract.py:152,805`) |
| When configuration is irrevocably committed | F1 freezes `root_rng_namespace`, recipe `tb-s2-rng-v3` (salted) and this custody rule. It carries **no salt and no salt hash**. The attempt row is durable from the provisional intent (`campaign_store.py:2635-2748`); the salt is generated in the transaction that first binds the F1 contract's budget (`campaign_store.py:2750-2802`) | Current recipe `regime.py:22-24`, seed input `seed_identity.py:29-41` |
| Crash-safe admission | No preview-capable work (plan derivation, dispatch, a G5 fetch) and no disclosure happens until the salt, its commitment and the consumed attempt are durable in one committed transaction. A repeated binding returns the stored salt and never generates another. An identical re-submission returns the stored admission; nothing allocates a new salt or attempt. **Crash before that commit:** no salt exists and nothing is derived from one. A request not durably admitted is retried with the same identity; an ADMISSION work that had already started is closed IN_DOUBT by recovery as today, with no salt to retain or reveal. **Crash after that commit, before the ADMISSION work's capture:** the attempt is consumed and closed. Recovery makes the running ADMISSION work IN_DOUBT and the campaign terminal; the salt is retained with its commitment; admission does not continue (a second ADMISSION reservation is refused, and ADMISSION is not re-execution-eligible under §3.3 R1); reveal follows under the public-reveal row once recovery completes. Continuing admission after such a crash would need a new admission-recovery rule, which this draft does not propose | The binding runs inside the RUNNING ADMISSION work (`campaign_supervisor.py:1456-1470`), and the plan is derived after it (`:1499`); an identical re-submission returns the existing admission (`campaign_store.py:1080-1089`, `:2654-2662`); an identical re-binding does not bind again (`:2765-2772`); ADMISSION is reserved once per attempt (`:2896-2901`); recovery of a START_INTENT or RUNNING work sets IN_DOUBT and ends campaign authority (`:3207-3213`). Spec §2.6's first row, "Retry admission with same identity", covers only a request not durably admitted, where "no execution existed" |
| Private access before reveal | The trusted administrator (OF-1); `qexec` store; the worker's read-only input, which carries the salt where it carries the root today, so the worker can derive every seed of the campaign; G5 through its authenticated checkpoint access and private staging, checking the salt against the admission commitment on every use. **Not `qclient`**: before reveal the client plan view carries seed *digests*, not seed values | The client can fetch the whole plan today (§1.2 B-3). G5 fetches the plan as a checkpoint member (`g5.py:671`), under the `g5` role (`campaign_protocol.py:93`). Worker seed derivation: `compute.py:21`, `runner.py:95`, `part_a.py:140` |
| Commitment | `sha256(salt)` in the admission receipt, client-visible at once. Canonical form: 64 lowercase hex, refused otherwise at generation and reveal | Delta K3 entropy rule retained |
| Public reveal | Only after the campaign is **irrevocably closed** to further computation and recovery: no work of any phase can still be reserved, dispatched, re-executed or recovered, every work is settled, and no recovery barrier is pending (`campaign_budget.py:166-168`). Examples, once those conditions hold: sealed; a committed statistical FAIL; BUDGET_EXHAUSTED; BUDGET_UNCERTAIN; VOID; an IN_DOUBT that is no longer re-execution-eligible under §3.3. A **retry-eligible IN_DOUBT does not reveal** | While a same-sample retry remains possible, a requesting party that knew the seeds could preview the pending checkpoint's outcome. It could then ask the operator to VOID, or otherwise influence the attempt, and so reach a successor with a fresh salt. The client role itself has no VOID operation: VOID is the operator's (`campaign_protocol.py:92`, `:94`). The retry reuses the same seeds (§3.3 R10) |
| Abandonment | Generating the salt **consumes** the F1-authorized attempt. Every closed state after generation is retained with the commitment and shown in `STATUS`: VOID, deadline lapse, host loss, or an interruption that is no longer re-execution-eligible. The service refuses a second admission under the same authorization (unique attempt key, boundary spec §7). A successor attempt needs a fresh operator authorization that cites the predecessor's record | Spec §2.6: "No new attempt ID may be allocated automatically" |
| Alternative, not recommended now | A public randomness beacon round fixed in F1 after attempt registration. It removes administrator preview, but adds an external dependency and a signature verifier | — |

**Crash during admission: operator ruling 2026-09-26.** In the ruling's words: "Joshua explicitly accepts that an admission crash after salt binding but before capture consumes and closes the attempt, preserving its identity and salt without continuing admission or generating another." *Drafting note, not part of the ruling:* the "Crash-safe admission" row above states the same consequence together with the mechanism behind it (recovery makes the running ADMISSION work IN_DOUBT and the campaign terminal, and a second ADMISSION reservation is refused); that mechanism is draft text for the RC-2 owner review, not ruling text. See also the "Abandonment" row. The proposed owner texts §1.5(b) and (c) state this consequence in short form; the RC-2 review should check that the applied text states it in full.

**Client plan view (new finding, kept).** The client role may fetch plan chunks, and the plan carries seed values (§1.2 B-3). Before F1 the client plan view must carry seed digests only. The client today checks the whole fetched plan against the receipt's `plan_sha256` (`execution/client.py:67-93`), so the client view needs its own digest in the receipt (Q10). Full-E1 spec §2.2a describes exactly that whole-plan client verification, so it needs the amendment in §1.5(d).

### 1.5 Proposed owner amendments

**(a) Boundary spec** `docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md`, §3. Insert a new subsection `### 3.1` after the paragraph that ends "…limited to trusted users: [Docker Engine security](https://docs.docker.com/engine/security/)." and before "The supervisor and G5 run from administrator-installed…":

> "### 3.1 Boundary set (AUDIT-2026-09-25-qualification-assurance-contract-delta#boundary)
> The requesting agent must be unable to: (B-1) alter installed execution, adjudication or worker code for an admitted release; (B-2) replace or edit captured evidence or the journal; (B-3) produce a counted attempt nobody sees, choose which attempt counts, or learn seed values before reveal; (B-4) grant itself activation authority; (B-5) present fixture or TEST_ONLY output as production evidence. Each retained mechanism cites the row it enforces. These rows rest on credentials and host permissions, not process roles: `qexec` is root-equivalent through Docker, and any agent-reachable administrator, `sudo`, Docker-socket, `qexec`, `qg5`, `qseal`, signing or deploy credential defeats them. These operational facts are production acceptance obligations: (OF-1) no account or environment in which an agent session runs, the operator's workstation account included, can use administrator, `sudo`, `docker`-group or Docker-socket access on the production qualification host; (OF-2) no agent can authenticate as `qexec`, `qg5`, `qseal` or the administrator, and no polkit rule grants `manage-units` to an agent-reachable UID; (OF-3) execution, result, seal and operator-VOID private keys are unreadable by agent-reachable UIDs and absent from every worktree, every CI secret visible to an agent-editable workflow and every store an agent can reach; (OF-4) key-enrollment and trust-domain inputs are writable only by the operator; (OF-5) no agent holds rail-host deploy credentials, write access to the rail `/data` volume, or broker credentials; (OF-6) if E3 is adopted, the operator GO signing key is off-host and never loaded where an agent runs; (OF-7) before public reveal, the seed salt is readable only by the trusted administrator, `qexec`, the worker's read-only input and `qg5`'s private adjudication access. Each is verified by attended host read at provisioning, before any production-authority release, and after any access change; OF-5 also before any arm and at each session GO, OF-6 at TB-I3, and OF-7 also before F1 admission. Until a row's facts are verified and recorded, the row is reported as enforcement not established; that is not a finding that the row is breached. The disposable CI harness is evidence of mechanism, never of this boundary."

**(b) Track B umbrella, optional** `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md`, §0.8. Only if the operator chooses this landing place (the kept coordinator review's routing: "only if the operator prefers"); (c) and (d) do not depend on it. Append a row after O-9, the table's last row (the umbrella body is closed; §0.8 is the named landing place):

> "| O-10 | Seed custody for F1 (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3) | **TB-F1** | F1 freezes `root_rng_namespace`, recipe `tb-s2-rng-v3` and this custody rule, and no salt or salt hash. `qexec` generates a 32-byte CSPRNG salt in the committed transaction that binds the F1 contract's budget for the single authorized attempt, before any preview-capable work, and publishes only `sha256(salt)` in the admission receipt. An identical re-submission or a recovery reuses the stored salt and attempt; an admission interrupted after that binding closes the attempt. `qexec`, the worker (through its read-only input, from which it can derive every seed) and G5 have private access during the campaign, as does the trusted administrator. The client plan view carries seed digests only, and the salt is disclosed to `qclient` only after the campaign is irrevocably closed to further computation and recovery; a retry-eligible IN_DOUBT is not closed. Generation consumes the attempt: every later closed state, abandonment included, is retained and visible, and a successor needs a new operator authorization citing it. |"

**(c) Full-E1 spec** §2.4, first paragraph. After "Reuse `runner._run_stage`, provider/replay/source admission, `regime.domain_seed`, seed identities, …", add:

> "Production-class campaigns use the salted recipe `tb-s2-rng-v3`, which is `tb-s2-rng-v2` with the service-generated attempt salt added (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3). The F1 freeze carries `root_rng_namespace`, the recipe and this custody rule, and no salt or salt hash. The salt and the consumed attempt are durably bound before any preview-capable work. An identical re-submission or a recovery reuses them and never generates new ones; an admission interrupted after that binding leaves the attempt closed IN_DOUBT (§2.6). The worker receives the salt in its read-only input, where it receives `root_rng_namespace` today, and derives its own seeds. G5 re-derives plans and seeds for each checkpoint it adjudicates from the salt it reads through its authorized private access, after checking the salt against the admission commitment. The client plan view carries seed digests, not seed values (§2.2a), and the salt is disclosed to the client only after the campaign is irrevocably closed to further computation and recovery. TEST_ONLY synthetic campaigns may keep `v2`."

**(d) Full-E1 spec** §2.2a, second paragraph. After "Clients verify ordered offsets, total length and the reassembled SHA256.", add:

> "For production-class campaigns (`tb-s2-rng-v3`), the plan object served to the client is a client view: the canonical plan with each seed value replaced by its digest. The admission receipt binds the client view's own digest and byte length beside the canonical plan's, and the client verifies the reassembled client view against them. Before the campaign is irrevocably closed to further computation and recovery, no chunk served to the client carries a seed value or the salt (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3). `qexec` retains the canonical plan, and G5 reads it through its checkpoint access."

### 1.6 Verification

- Before F1 admission (OF-7) and before any production-authority release (all), the operator records an attended host-read attestation for OF-1..OF-7.
- **Salt tests:**
  - a contract with no bound salt cannot derive seeds;
  - the salt must hash to the admission commitment, at G5 use and at reveal;
  - a salt not in canonical 64-hex form is refused at generation and at reveal;
  - G5 adjudicates N1 and N2 before reveal through its private access;
  - no salt or seed value reaches the `client` role through `STATUS`, `FETCH_PLAN_CHUNK` or the receipt before closure;
  - a retry-eligible IN_DOUBT does not reveal; the same campaign reveals once it is closed.
- **Crash-safe admission tests:**
  - an ordering test: no plan derivation, dispatch or G5 fetch before the salt-binding commit;
  - a crash before that commit leaves no salt; a request not durably admitted retries with the same identity;
  - a crash after that commit, before the ADMISSION capture, then re-submission or recovery, returns the same commitment and attempt, closed IN_DOUBT; admission does not continue, and the salt is revealed once recovery completes;
  - a repeated binding returns the stored salt.
- **Abandonment tests:**
  - a second admission under the same authorization is refused;
  - a VOID after salt generation leaves a visible, counted closed record.
- The delta's §10 routing hook stops printing `UNROUTED: boundary` and `UNROUTED: K3`.

### 1.7 Residual risk

- The administrator can read the salt before reveal. This is trusted by design (spec §3); the beacon alternative removes it.
- G5's private access adds `qg5` to the pre-reveal readers. OF-2, OF-3 and OF-7 cover it.
- The worker's read-only input carries the salt, so a worker can derive every seed of the campaign, not only its own work's. OF-7 covers the input; B-1 (installed worker code) is what keeps the worker from disclosing it.
- OF verification is attended, and it becomes stale when access changes.
- B-4 stays procedural until TB-I3.
- Deterministic domain separation is not a proof of independence (freeze-candidate §Seeds).

## 2. D2: N1 resource accounting

### 2.1 Recommended direction

Recommended (executive review 2026-09-26); ~~operator ruling pending~~ **D2 adopted as an S5 direction** by [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session), in its words: "Retain per-phase accounting." The ruling's resource-envelope decision (§6 of the ruling) governs item 7 below. *Items 1–8 below are the draft's recommendation, not ruling text, except the ruling quoted in items 7 and 8; their owner-text form is reviewed under RC-2.* The executive review earlier recommended simplification in principle. After the comparison in §2.3 it recommends keeping the accepted per-phase model for S5.

1. **Name the invariant; do not replace it for S5.** The delta's "one outer cgroup per campaign (CPU, memory, wall)" is not, as written, a cumulative bound: `cpu.max` limits rate only, and spec §2.5 already says: "OS CPU-rate limits alone do not enforce cumulative CPU seconds." In the current code the per-work mechanism (§2.2) is the only cumulative bound. That is evidence about this design, not proof that every cumulative-bound design needs per-work reservations. A replacement would have to show its own enforced cumulative bound; none is proposed.
2. **Keep per-phase reservation sizing for all phases** (N1…SEAL). The **PART_A ceiling covers maximum expansion**, as the budget-profile owner already states (`execution/profile.py:167`). It is measured before S5 is released (§5 RC-3) and re-confirmed on the S5 adapter at S5 packet Checkpoint C3.
3. **Retain committed evidence after exhaustion** (review point e, §2.4). A stage assessment committed before exhaustion stays evidence.
4. **After exhaustion, no further work and no new completion authority** (§2.4).
5. **A retained receipt never stands in for current authority.** Preserving a receipt must not let a downstream consumer ignore exhausted or revoked campaign authority (§2.4). Consumers that grant new action (reservation, dispatch, result commit, seal, activation) check current authority and validity at use. Statistical accounting records committed evidence, a stage FAIL included, whatever the later authority state (§6 Q1). A result committed before a later exhaustion is retained as history and cannot be sealed or used for activation.
6. **No per-phase CPU number enters any statistical decision.** This is already true and should be pinned by a test.
7. **Coordinator TEST_ONLY diagnostic ceilings, only within a recorded measurement-and-margin rule.** The operator fixes the rule itself (the measurement standard and the margin), in the D2 ruling or a separate ruling. The coordinator only applies it: a cited measurement record for the phase, the rule's margin, and a ledger entry. A value outside the rule, or without a measurement, needs an operator ruling. (The executive review did not name who fixes the rule; that the operator does is the drafter's addition.) The M13 round (coordinator checkpoint C2, 2026-09-24) needed an operator ruling because the packet barred ceiling changes. *Operator ruling 2026-09-26 (resource-envelope decision):* the coordinator prepares a concrete measurement proposal identifying the maximum-expansion workload, the reference runtime, CPU/wall/memory capture, the proposed margin and budget feasibility, and returns the measurement-and-margin rule for operator approval. No numerical rule is approved yet. Once the rule is approved, the coordinator may apply it to TEST_ONLY diagnostic ceilings with recorded evidence. This preparation does not authorize held S5 execution. *Drafting note, not part of the ruling:* returning the rule for operator approval matches this item's addition that the operator fixes the rule; the rule's content stays open until approved (§6 Q11).
8. **Production budgets are governed separately.** Production ceilings and caps are frozen with F1 by their owners. The TEST_ONLY rule never sets or changes them. *Operator ruling 2026-09-26:* "Production budgets remain separately governed."

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

**Basis of the systemd/cgroup semantics above.** This draft cites no vendor documentation for them. Each is **DOCUMENTED in the repo only**, with the Linux evidence named:
- cgroup v2 `cpu.max` limits rate and there is no cumulative CPU cap: the docstring at `campaign_supervisor.py:180`, and spec §2.5. Evidence: `test_s2_payload_cpu_is_kernel_bounded_without_guardian`, which shows the rate × lifetime product holding with the guardian stopped (`tests/integration/qualification_boundary/test_campaign_supervision_linux.py:548-549`), not that no cumulative cap exists.
- `RuntimeMaxUSec` is enforced by the system manager (PID 1), not by the guardian's Python, and the guardian's end retires the payload slice through `BindsTo`: the docstring at `campaign_supervisor.py:180-183`. Evidence: the same S2 node.
- `LimitCPU` is `RLIMIT_CPU`: the guardian refuses to run unless `getrlimit(RLIMIT_CPU)` equals the unit's `LimitCPU` (`campaign_supervisor.py:1431-1435`).
- Whether a garbage-collected idle slice keeps its `cpu.stat` counter (below): **UNVERIFIED**.

Hence, in the current design, cumulative campaign CPU ≤ Σ over works of (quota × RuntimeMax + LimitCPU + helper bound) ≤ cap, and each term is kernel-enforced. The bound survives a service restart because BOOTTIME continues and the store persists. A reboot changes the boot ID, which makes the campaign `BUDGET_UNCERTAIN`: it fails closed, and cross-boot continuation is unsupported (spec §2.5). Linux evidence: S2 nodes `test_s2_payload_cpu_is_kernel_bounded_without_guardian`, `test_s2_deadline_kills_guardian_before_bootstrap_completes` and `test_s2_original_deadline_survives_service_downtime` (S2 acceptance, 2026-09-21).

The delta's outer-cgroup form, as written, would need quota_campaign × (deadline − start) ≤ cap to act as a cumulative bound. That forfeits CPU during queues and downtime and throttles every phase to the campaign-average rate. It would also need a way to attribute each work's usage; whether a garbage-collected idle slice keeps its counter is UNVERIFIED on the host. These are costs of that form, not of every possible campaign-level design.

### 2.3 Per-phase, mixed and uniform campaign compared (review point d)

| Criterion | **Per-phase everywhere** (accepted) | **Mixed** (delta): per-phase for N1/N2; campaign scope for PART_A, RESULT, SEAL | **Uniform campaign**: every work sized from the remaining campaign allowance |
|---|---|---|---|
| Cumulative bound | Yes (§2.2) | Only if campaign-scope works keep a per-work reservation or the design adds another enforced cumulative mechanism (none is specified). The outer cgroup as written is rate-only | Same as mixed |
| Forward complexity | One sizing rule. Each new phase needs a measured ceiling that fits the Σ-feasibility check | **Two** rules across `reserve_work` (`:2873-2878`), the binding feasibility (`:2776-2783`), the funding projection, the closed profile phase set (`profile.py:195` requires every `PHASES` entry) and T05's result/seal reservations. A phase-conditional rule is the defect class coordinator checkpoint C2 traced (N1-only sites, 2026-09-24) | One rule and no ceilings, but it must still hold back a tail for G5, RESULT and SEAL, which reintroduces per-phase amounts for the tail |
| Tail liveness | A runaway compute stops at its ceiling, and G5/RESULT/SEAL stay funded | Runaway PART_A can consume the tail unless one is held back | Same as mixed |
| Migration risk against accepted evidence | None | N1/N2 untouched. T05 (built, not accepted) changes. New budget-profile version | New budget profile and release, then re-runs of the S2/S3/S4 Linux node sets (15/19/22) under it; contract decisions 1 and 4 require fresh attempts |
| Cost to reach S5 | PART_A ceiling measurement, plus a ruling or the measurement-and-margin rule. Stage plumbing (below) | Plumbing plus the new seam and its tests | Plumbing plus a rewrite and full Linux re-acceptance |
| Statistical protection | Identical in all three: no-redraw is `campaign_store.py:2896-2901` plus plan binding, not budget size. Depth is a planning number (ADR Deviation A1) | Identical | Identical |

**Plumbing every model pays at S5:** role branches `n2_worker`/`n2_g5` (`campaign_supervisor.py:1520-1530`), the UID map (`:2546-2555`), `PROGRESSION_PHASES` (`campaign_store.py:180-182`), `CHECKPOINT_ADVANCES` and `CHECKPOINT_PROGRESSION_STATES` (`:120-124`), and the literal state set at `campaign_supervisor.py:2504`. The delta's §10 N1 hook counts 4 sites in the supervisor and 32 in the store at this head. Those are progression sites, not sizing sites, and none of them disappears under either alternative. The coordinator checkpoint C2 round's liveness generalization (`_live`, `:1278-1287`) has already made the accounting side phase-generic.

**Falsifier:** revisit the uniform model if PART_A's maximum-expansion CPU cannot be bounded ahead of time. That would mean a ceiling covering maximum expansion either fails the Σ-feasibility check against any admissible cap or cannot be measured before S5 is released.

### 2.4 Exhausted campaign with a valid stage result (review point e)

Rule:
- A committed stage assessment is **retained as evidence and never revoked**.
- Exhaustion ends all further work: no new reservation, dispatch, assessment, result or seal.
- No whole-campaign completion (`RESULT_COMMITTED_*`, `SEALED_PASS`) is committed after exhaustion. A result or seal receipt committed **before** a later exhaustion is retained as history; it cannot be sealed or used for activation. Precedence: exhaustion wins over an earlier completion's authority, never over its record. The T05 design already works this way (branch `claude/t05-result-seal` at `6cf2732`, not on `main`): the committing result or seal work settles after its commit, and a settlement overrun ends authority from `RESULT_COMMITTED_*` or `SEALED_PASS`, leaving the receipt historical (`execution/campaign_result.py:75-83`, `:921-932`, `:955-956`); a committed PASS whose campaign is in a refused budget state is not seal-eligible (`:66`, `:1233-1239`). At `main@24e3843` the store has no result or seal states.
- A committed stage FAIL stays binding in the attempt's record and can never be recast as "incomplete" to justify a successor attempt.
- **A retained receipt is history, not authority.** It serves two roles, kept apart:
  - *Consumers that grant new action* (reservation, dispatch, result commit, seal, activation) read the campaign's current authority state and validity at use, and refuse after exhaustion, revocation or VOID. The checkpoint-commit replay returns `validity` and a retry flag, `historical` (`campaign_store.py:908-913`), not the budget authority state, so `VALID` there is not live authority.
  - *Statistical accounting* records committed evidence, a stage FAIL included, whatever the later authority state. How that evidence counts under the release-binding ADR §4 is §6 Q1. Recording it grants no completion, seal or activation authority.

This matches current code and spec:
- `_settlement_terminal` ends authority from the progression states, and the receipt stays historical (`campaign_store.py:2612-2617`, the S3 P1 fix);
- spec §2.5: "Deadline reached means no new authority even if computation already passed";
- spec §5 forbids returning "a historical receipt without current validity";
- T05 refuses a seal on `REFUSED_BUDGET_STATES` (branch, T05 follow-up 2026-09-22).

### 2.5 Proposed owner amendments

**(a) Slices plan** `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`, contract decision 3. Append after "…not independent full-size allowances per process.":

> "In this design the cumulative bound is per work and kernel-enforced: payload quota × guardian `RuntimeMaxUSec` plus the guardian's `LimitCPU` never exceeds that work's reservation, and settled charges plus open reservations never exceed the frozen cap (AUDIT-2026-09-25-qualification-assurance-contract-delta#N1). A campaign-level rate quota is not a substitute. Every phase, PART_A, RESULT and SEAL included, reserves its installed phase ceiling; PART_A's is measured at maximum expansion. No per-phase CPU figure enters a statistical decision. The operator fixes a measurement-and-margin rule (the measurement standard and the margin) by ruling. The coordinator may set TEST_ONLY diagnostic ceilings only by applying that rule (a cited measurement, the rule's margin, a ledger entry); anything outside it needs an operator ruling. Production ceilings and caps are frozen with F1 by their owners and are never set under that rule."

**(b) Full-E1 spec** §2.5, last paragraph. After "Deadline reached means no new authority even if computation already passed.", add:

> "A stage assessment committed before exhaustion remains evidence and is never revoked. Exhaustion ends all further work, and no result or seal is committed after it. A result or seal receipt committed before a later exhaustion is retained as history and cannot be sealed or used for activation; a settlement overrun of the committing work ends authority from the state its commit produced. A committed statistical FAIL is never recast as incomplete. A retained receipt is history: every consumer that grants new action (reservation, dispatch, result commit, seal, activation) checks the campaign's current authority and validity at use and refuses after exhaustion, revocation or VOID. Statistical accounting records committed evidence, a statistical FAIL included, whatever the later authority state; recording it grants no authority."

### 2.6 Verification

- A test that no acceptance or adjudication path reads a phase CPU figure.
- Exhausted-campaign tests for N1 and N2 on the service path:
  - a committed N1 FAIL followed by a `N1_G5` settlement overrun gives `BUDGET_EXHAUSTED`, the receipt is `historical=true`, and no RESULT reservation is possible;
  - the same after a committed `PART_A_READY`;
  - a consumer holding a `VALID` checkpoint receipt from an exhausted campaign cannot reserve, commit a result or seal.
- The PART_A ceiling is measured at maximum expansion and recorded before S5 is released, and re-confirmed on Windows and Linux at S5 packet Checkpoint C3; `bind_budget` feasibility passes for the v7 profile.
- The three S2 nodes in §2.2 stay green at S5 (reuse of unchanged evidence).

### 2.7 Residual risk

- An overrun detected at settlement ends the campaign after the fact. The kernel bound caps its size, not its occurrence.
- The per-phase ceilings still need calibrating for each new phase.
- Cross-campaign memory interference on a shared host parent can invalidate every attempt (S2 clarification).
- Reboot is terminal.

## 3. D3: N2 bounded same-sample re-execution

### 3.1 Recommended direction

Recommended (executive review 2026-09-26); ~~operator ruling pending~~ **D3 adopted as an S5 direction** by [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session), in its words: "Implement bounded same-sample recovery in a separate slice after S5 and before S8." *The rest of §3, including the rule R1–R10, is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2.* The draft recommends adopting bounded same-sample recovery under R1–R10 below as direction, implemented as its own slice after S5 and before S8. S5 keeps today's terminal IN_DOUBT. Adding the rule changes a terminal campaign state into a re-execution-eligible one: `record_work_transition` and `recover_work` both call `_settlement_terminal(state, 'IN_DOUBT')` (`campaign_store.py:3157-3160`, `:3210-3213`). That change must not ride inside S5.

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
| R2 **Terminate and fence first** | The original worker is terminated and fenced before the retry is reserved: the original work's recovery completed with an absence proof for its guardian, payload slice, container and `qg5` unit, and the store holds it IN_DOUBT, so no late `CAPTURED` is legal. If absence cannot be proven, the work stays terminal |
| R3 **Identities committed before execution** | The retry's reservation carries `reexecution_of=<work_id>` and byte-identical identities: **sample** (plan and seed inventory), **source** (source bundle and admission evidence), **runtime** (release, image, interpreter and pinned thread environment) and **configuration** (contract, policy, profile and predecessor receipt), with the same `input_sha256`. Any difference refuses |
| R4 **Original envelope and deadline** | Same installed phase limits (no enlargement). The retry is charged from the same cap **on top of** the interrupted work's charge (unknown = full reservation, no refund), under the campaign's **original** absolute BOOTTIME deadline. No renewed deadline and no renewed or enlarged allowance. If it does not fit, the campaign ends exhausted |
| R5 **Attempts retained** | The interrupted work, any failed or interrupted retry, their observations and any saved bytes stay in history. The retry is a new linked work under the **same** attempt ID and checkpoint key |
| R6 **Predeclared comparison schema** | Each compute checkpoint has a versioned comparison schema, installed with the release before admission, that names the compared statistical fields and the excluded runtime-observation fields (for example elapsed time, resource counters, host and container identifiers). It cannot change for an admitted campaign. Retained complete records (Part A's initial-prefix artifact) must match the retry on the compared fields |
| R7 **Zero retained records** | The zero-capture case rests on reproducibility evidence. It is allowed only when the installed release carries recorded evidence for that checkpoint: complete repeat executions of its plan on the pinned runtime that agree under the R6 schema, with all R3 identities equal. The evidence standard for production (depth, repeat count, hosts) is set by the operator with the statistical owner. Two agreeing repeats at reduced TEST_ONLY depth are evidence for those conditions only, not proof of production determinism. Without the required evidence the work stays **unresolved** (terminal IN_DOUBT) |
| R8 **Disagreement** | Any R6 mismatch, or any divergence found later, is an **incident**: the campaign becomes terminal (a new reason, e.g. `REPRODUCIBILITY_INCIDENT`), never a result and never retry-eligible, and the release's reproducibility record is suspended pending review |
| R9 **Limits** | At most one re-execution per interruption and two per campaign. An interruption of the second re-execution is terminal |
| R10 **No new namespace; no reveal** | Repeated interruption never allocates an attempt ID, salt, seed or plan. The salt is not disclosed to the client while a re-execution remains possible (§1.4). A timing-driven abort on a retry (`part_a.py:185-191`) is an operational terminal, not a result |

### 3.4 Proposed owner amendments

**(a) Full-E1 spec** §2.6, table row "START_INTENT or RUNNING, no complete durable capture". Replace its recovery cell with:

> "Persist IN_DOUBT before cleanup; stop owned worker. Never relaunch, except one bounded same-sample re-execution under the rule below."

In the same table, row "VOID, terminal abort, IN_DOUBT or BUDGET_UNCERTAIN", replace its first cell with (the recovery cell is unchanged):

> "VOID, terminal abort, IN_DOUBT (except a work that is re-execution-eligible under the bounded same-sample rule below) or BUDGET_UNCERTAIN"

After the paragraph ending "…outside retry semantics.", add:

> "**Bounded same-sample re-execution (AUDIT-2026-09-25-qualification-assurance-contract-delta#N2).** A compute checkpoint (N1, N2 or PART_A) left IN_DOUBT by process interruption on the same boot, with no finalized capture, may be re-executed once, and at most twice per campaign. The service may do so only after the original worker is terminated, its absence is proven and its IN_DOUBT state is durable. The re-execution uses byte-identical sample, source, runtime and configuration identities and the same installed phase limits, under the campaign's original deadline and allowance, charged on top of the interrupted work's charge. The interrupted work, and any failed re-execution, stay in history. Retained complete records must match the re-execution on the fields named by the checkpoint's predeclared comparison schema, which also lists the excluded runtime-observation fields. With none retained, re-execution requires recorded reproducibility evidence meeting the standard set for the campaign's authority class; otherwise the work stays IN_DOUBT. A mismatch is a terminal reproducibility incident, never a result. Captured work, committed assessments (a statistical FAIL included), overruns, BUDGET_UNCERTAIN and VOID are never eligible. No re-execution allocates an attempt, salt, seed or plan, and the salt is not disclosed to the client while a re-execution remains possible."

**(b) Full-E1 spec** §5, second bullet. After "redraw under the same attempt", add: "(a §2.6 bounded same-sample re-execution is not a redraw)".

**(c) Full-E1 spec** §2.4, last paragraph. After "…makes that operation IN_DOUBT.", add: "§2.6's bounded re-execution reruns the whole checkpoint from its first panel under the same plan; it never resumes panels."

**(d) Slices plan** contract decision 6. After "Missing capture never licenses another draw;", add: "a spec §2.6 bounded same-sample re-execution is not a draw;". In **S5 Behavior**, after "…no panel resume, replacement pilot or checkpoint rerun.", add: "S5 builds this terminal subset; the §2.6 re-execution is a later slice after S5 and before S8, and S5-D1's retained initial prefix is the retained complete record that full-E1 spec §2.6's comparison schema compares."

### 3.5 Verification

- **Reproducibility evidence** on the pinned runtime, compared under the predeclared schema and recorded in release evidence with its depth and conditions. Evidence at reduced TEST_ONLY depth is labelled as such and is never cited as production determinism.
- **Scenario tests:**
  - an interrupted N2 then re-executed on zero records, with the evidence present, succeeds;
  - the same without the evidence stays IN_DOUBT;
  - a Part A run interrupted after the initial prefix is re-executed with a matching prefix;
  - an altered prefix gives the incident terminal;
  - a retry-eligible IN_DOUBT reveals no salt to the client.
- **Refusal tests:**
  - a CAPTURED, FAIL-committed, overrun, BUDGET_UNCERTAIN or VOID work refuses a re-execution;
  - a third interruption is terminal;
  - a changed `input_sha256`, runtime or configuration identity refuses;
  - a re-execution before the absence proof refuses;
  - a comparison schema other than the one installed at admission refuses.
- **Linux:** kill a guardian mid-N2, then restart, re-execute and commit through the real `qg5` unit.

### 3.6 Residual risk

- Undetected nondeterminism: reproducibility evidence supports the tested conditions only, not proof, especially at reduced TEST_ONLY depth compared with production depth.
- Reboot stays terminal.
- Re-execution consumes allowance, so a late interruption may end the campaign exhausted anyway.

## 4. Sequencing against the S5 hold

*Superseded in part by the [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session): D1–D3 are now ruled, in the ruling's words, so the first two bullets' references to ruling them are historical. Their build-versus-release split, and the need for every §5 condition before release, still stand.*

- **Ruling D2** and a defensible measured PART_A envelope are what S5 itself needs, with the other §5 conditions.
- **D1 and D3** can be ruled at the same time. S5's **build** needs from them only the text in §3.4(d). §1.5(c) is not a build prerequisite: it lets TEST_ONLY campaigns keep `tb-s2-rng-v2` and asks no S5 code change, so it is release owner text under RC-2 (consistency-review correction 2026-09-26; governs). S5's **release** needs every §5 condition, including RC-2's full owner-text set, RC-4 and RC-5.
- **K3 implementation** belongs with TB-F1 (before F1). The **client plan-view change** lands before F1 in a slice the operator names (§5 RC-4).
- **N2 implementation** belongs in a slice after S5 and before S8.

These directions do not release the hold. The coordinator may propose release only when every §5 condition holds; only the operator releases it, by a new ledger entry.

## 5. S5 release conditions

**The immediate S5 blocker is corrected owner text and a defensible Part A resource envelope.**

The coordinator may propose releasing the S5 hold only when all of these hold. The proposal goes to the operator; only an operator ruling, recorded as a new entry under the [S5 hold ledger entry](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-freeze-held-2026-09-25), releases the hold.

| # | Condition | Evidence the proposal cites |
|---|---|---|
| RC-1 | Operator rulings on D1, D2 and D3 are recorded in the S5 hold ledger entry of the execution-slices plan, or a dated entry beneath it | The ledger entry, with the operator's words and date |
| RC-2 | Corrected owner text is accepted by the operator and applied to each named owner: boundary spec §3.1; full-E1 spec §2.2a, §2.4, §2.5, §2.6 (the two table rows and the new paragraph) and §5; slices plan contract decisions 3 and 6 and the S5 text; umbrella §0.8 O-10 if the operator chooses that optional landing place. Each cites the qualified tag `AUDIT-2026-09-25-qualification-assurance-contract-delta#<row>` | The merge commits; the delta's §10 hook no longer prints `UNROUTED` for the boundary, K3, N1 or N2 |
| RC-3 | A defensible measured Part A resource envelope: CPU, wall and memory for PART_A at maximum expansion of the TEST_ONLY workload S5 will run, measured on the reference runtime with a cited record; the ceiling set from it by applying the operator-fixed measurement-and-margin rule (§2.1 item 7), or by operator ruling; and Σ-feasibility at binding (`campaign_store.py:2776-2783`) passing for the `/v7` profile against that workload's cap. *Operator ruling 2026-09-26 (resource-envelope decision):* the coordinator prepares a concrete measurement proposal (maximum-expansion workload, reference runtime, CPU/wall/memory capture, proposed margin, budget feasibility) and returns the measurement-and-margin rule for operator approval; no numerical rule is approved yet; once approved, the coordinator may apply it to TEST_ONLY diagnostic ceilings with recorded evidence; production budgets remain separately governed; this preparation does not authorize held S5 execution | Measurement record IDs; the profile values; the feasibility test result |
| RC-4 | The client plan-view seed change (digests only; §1.4) has landed, or is explicitly scheduled before F1 with its gate: a named owner and slice, the full-E1 spec §2.2a client-view amendment (§1.5(d)) applied, and an F1 admission check that refuses while the client can fetch seed values. *Operator ruling 2026-09-26:* the ruling directs that seed-view implementation be assigned to its specified gate (this row's: before F1, with that admission check). It names no owner or slice. RC-4 stays unmet until the change lands, or until its owner record holds the scheduling text this row requires: a named owner and slice, the §1.5(d) amendment applied, and the F1 admission check | The commit, or the scheduled slice and gate text in its owner |
| RC-5 | Host-check obligations OF-1..OF-7 are assigned: an owner for each attended read, the gate it precedes (OF-7 before F1 admission; all before any production-authority release) and where the record lands. Assignment only; the reads themselves are not S5 prerequisites. *Operator ruling 2026-09-26:* the ruling directs that host attestations be assigned to their specified gates. It names no owner or record location. This draft's gates for OF-5..OF-7 differ between the §1.3 table and §1.5(a) (§6 Q12); that stays open for the coordinator's owner-text and RC-5 work. RC-5 stays unmet until an owner record holds the assignment text: an owner for each attended read, the gate it precedes and where the record lands | The assignment text in its owner record |
| RC-6 | ~~*Drafter's addition, not in the executive review's list; the operator may keep or drop it (§6 Q11).*~~ **Retained** by [operator ruling 2026-09-26](#operator-ruling-2026-09-26-in-session) ("Retain RC-6."); originally the drafter's addition. The S5 packet's anchors are re-read at the head where release is proposed, with the §3.4(d) text in place, so S5 builds terminal IN_DOUBT only | The re-anchored packet |

These directions, and meeting these conditions, do not by themselves release S5. They grant no Gate B, C or D acceptance, no drill authorization, and no dispatch, deployment, production, activation or live authority.

## 6. Open questions and unverified items

1. Whether a committed statistical FAIL on an exhausted campaign should still count as a FALSIFIED attempt under ADR §4 without a result commit. The rule above keeps the FAIL binding in the record; this is a statistical-owner question.
2. "Original deadline" in R4 is read as the **campaign's** original BOOTTIME deadline, not the interrupted work's own (the latter would make a late retry infeasible). This needs confirming.
3. Not verified on a host: whether a garbage-collected systemd slice keeps its `cpu.stat` history (§2.2), and PART_A's maximum-expansion CPU (not measured; §5 RC-3).
4. Whether Part A or N2 captures carry timing fields. This now feeds the R6 comparison schema. The Part A loop reads a timer (`part_a.py:183-191`); whether elapsed values reach the capture bytes is not verified. It needs a read of the capture schema before the schema is fixed.
5. Every OF (§1.3) is unverified by this draft. It read no host, credential store or secret list. That means enforcement is not established, not that it is absent.
6. The unanchored §0 inputs of the delta audit remain unrecorded (delta §0).
7. The production evidence standard for R7 (depth, repeat count, hosts) is owed by the operator with the statistical owner.
8. G5's private salt route: a new checkpoint member served to the `g5` role, or a `qg5`-private staged object. Either must keep the salt out of the client's reach and fall under OF-7.
9. Closure of a retry-eligible IN_DOUBT that is never retried: is the campaign closed (and the salt revealed) once no retry can fit the original deadline, or only by an operator VOID?
10. Owner of the client plan-view change (TB-F1, or a qualification slice before it), and whether the client-view digest joins the admission receipt beside `plan_sha256`.
11. Whether to keep release condition RC-6 (re-anchor the S5 packet before release). The drafter added it; the executive review did not list it. The same applies to §2.1 item 7's proposal that the operator fixes the measurement-and-margin rule. **Answered by operator ruling 2026-09-26:** RC-6 is retained ("Retain RC-6."). The measurement-and-margin rule is returned to the operator for approval, and once approved the coordinator may apply it to TEST_ONLY diagnostic ceilings with recorded evidence (resource-envelope decision); approval of the rule therefore rests with the operator, as §2.1 item 7 proposed. Still open: the rule's content. No numerical rule is approved yet; the coordinator prepares the concrete measurement proposal that returns it.
12. **The OF-5..OF-7 gates differ between §1.3 and §1.5(a)** (a drafting inconsistency found in review of the ruling record, 2026-09-26; not a ruling). The §1.3 **When** column puts OF-1..OF-4 at host provisioning, before any production-authority release and after any access change, but OF-5 only before any arm and at each session GO, OF-6 only at TB-I3, and OF-7 only before F1 admission. The §1.5(a) proposed owner text puts all seven at provisioning, before any production-authority release and after any access change, with the OF-5, OF-6 and OF-7 gates in addition; §1.6 and RC-5 ("all before any production-authority release") read the same way as §1.5(a). The operator ruling directs assignment to the "specified gates" and does not choose between the two. Open for the coordinator's owner-text or RC-5 work.

## Verification of this draft

```bash
# K3 recipe and root (expect no salt yet)
grep -n "payload = \|return int.from_bytes" ops/c1_rail/qualification/regime.py
grep -n "root_rng_namespace" ops/c1_rail/qualification/seed_identity.py ops/c1_rail/qualification/contract.py
# Client may fetch plan chunks; the service serves the whole stored plan; plan carries seed values
grep -n "'client':" ops/c1_rail/qualification/execution/campaign_protocol.py
grep -n "AND role='plan'" ops/c1_rail/qualification/execution/campaign_store.py
grep -n "'seed':seed" ops/c1_rail/qualification/seed_identity.py
# G5 re-derives plans and seeds while the campaign runs (private access needed before reveal)
grep -n "expected_plan = derive_n1_plan\|_joint_plan_vector(contract, policy)" ops/c1_rail/qualification/evidence.py
grep -n "plan_bytes = fetch(members\['plan'\])" ops/c1_rail/qualification/execution/g5.py
# Admission idempotency: identical re-submission and re-binding
grep -n "immutable admission identity conflict\|immutable budget binding conflict" ops/c1_rail/qualification/execution/campaign_store.py
# VOID is the operator's, not the client's
grep -n "'operator': {'STATUS', 'VOID'}" ops/c1_rail/qualification/execution/campaign_protocol.py
# The worker derives seeds from the contract root in its input
grep -n "root_rng_namespace" ops/c1_rail/qualification/execution/compute.py
grep -n "domain_seed(root=request.root_rng_namespace" ops/c1_rail/qualification/runner.py ops/c1_rail/qualification/part_a.py
# T05 (branch, not main): settlement overrun ends authority from the result/seal commit states
git show 6cf2732:ops/c1_rail/qualification/execution/campaign_result.py | grep -n "a8a983e\|^REFUSED_BUDGET_STATES"
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

