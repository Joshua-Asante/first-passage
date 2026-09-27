# Staged acceptance handoff set — bounded next steps toward deployment (2026-09-27)

**Status:** PREPARED 2026-09-27 under the operator direction recorded in the [deployment-checklist addendum 2026-09-27](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step). None is dispatched by this file. **Revised the same day** after the operator's review of `9448373`:
- H1, H3 and H4 now continue [#519](https://github.com/Joshua-Asante/first-passage/pull/519)'s returns instead of redoing them.
- H1 separates proposal correction from measurement execution.
- H4 waits on an accepted classification contract.
- H5 returns a policy choice.
- H9 keeps its full-S5 dependency, with two checkpoints.

**Operator rulings of 2026-09-27 applied here:**
- ORB L1 and the fence classification contract ([§59 Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27));
- no same-session restart after an incident ([incident ADR §A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27));
- the S5 staged gates with Part A-only rule scope, hold kept ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27));
- preservation-trade read targets ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27)).

The operator also directed that H1(a), H2, H3, H5(a), H7 and H8 proceed now, reusing #519's returns, and that each commissioning row return as a ready-to-run row for explicit execution approval.

**Pinned inputs from #519.** The returns are unmerged and are read at the PR head `8c15f1853e64f14f50995e3f1c55a620a0f674b7`, for example `git show 8c15f18:<path>`:
- `docs/notes/2026-09-26-s5-part-a-measurement-proposal.md` and its card `docs/briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md` (fix round and coordinator review);
- `docs/notes/2026-09-26-orb-lifecycle-evidence.md` and `docs/notes/2026-09-26-account-fence-four-state-trace.md`, with the card `docs/briefs/handoffs/2026-09-26-orb-lifecycle-and-fence-trace.md`;
- `docs/notes/2026-09-26-close-semantics-c-a.md` and its card.

If #519 merges before dispatch, the same paths on `main` are used, once they are confirmed byte-identical.

**Ownership:**
- The campaign coordinator dispatches each card under the committed-handoff rule. At dispatch the coordinator copies the card into its own file with its `yaml authority` block and runs the pre-dispatch read ([surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md#decision), *Action classes and the authority block*). This set carries no authority block because a file holds only one.
- **A card never grants what its dispatcher lacks.** Capabilities listed under "Grants at dispatch" narrow the dispatching seat's own grants. Any CI-configuration change, Linux dispatch, artifact download, account action or spend also needs the operator approval named on the card; the card only records that approval.
- The addendum owns sequencing and the checkpoints CP-1a..CP-9. Each card's named owners keep their outcomes.

**Common rules:**
- Read `AGENTS.md` first.
- No agent places, amends or cancels an order. No merge, spend, arm, deploy, vendor contact or account access by an agent.
- No private source, account figure, P&L or credential is committed, quoted or sent to an external service. The book's Pine and runtime ports are read only in place in the operator's primary checkout ([§60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25)).
- Commissioning results are labelled `COMMISSIONING_OBSERVATION` and state their scope. After review they may support capability acceptance for that scope. They are never production E1/n3 results, portfolio admission or whole-route acceptance (addendum §2).
- A synthetic result never marks an obligation that needs a real producer as resolved.
- A finding that changes behavior returns to its owner decision before the freeze (addendum §5).

**Dispatch states:**
- **READY:** existing authorization covers it now.
- **READY ON <event>:** dispatch when that event is recorded.
- **LATER:** requirements recorded, not yet a card.

| Card | Workstream | State | Unlocks |
|---|---|---|---|
| H1 | S5 and resource limits | Step (a) **RETURNED and ACCEPTED 2026-09-27** ([r2 CP-1a packet](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md)); step (b) **RETURNED 2026-09-27; tooling accepted as PRELIMINARY** ([#526](https://github.com/Joshua-Asante/first-passage/pull/526) at `27df508f`: the harness, its README and the dispatch-only workflow). Coordinator re-check in a clean detached worktree at `27df508f` (Linux; ops environment, CPython 3.11.15, through `python3 -I scripts/fp.py --env <ops-env>`), repeated 2026-09-27 18:06 UTC to retain the records: `python -m pytest tests/ops/qualification/test_part_a.py -q` gave 11 passed (record `20260927T180621Z-71bad46c8b99`, `record.json` SHA-256 `3148c330b5f8c81ba08f28dec0d8b60382a5028be924b5fd91ae44063414da7f`); `check` exited 0 (record `20260927T180630Z-2534fb8215cf`, SHA-256 `c36bb4c4a09dbf4c1f6be6d2fec05e3ba75bf2a0f87f681be7c4168ee55aca79`, with the vendor-data absent-tree skips). Both records show `status: completed`, verification exit 0, `source_stable: true`, complete capture and no report errors. **Retained 2026-09-27** in the private `first-passage-archive` by content address (`evidence/sha256/<aa>/<digest>`, one `evidence/INDEX.tsv` row each), commit `41eab925` on branch `claude/evidence-h1b-526-verification`, pending the operator's merge into the archive's `main`: both directories' files byte for byte, plus the package `h1b-526-verification-evidence-2026-09-27.tar.gz` (SHA-256 `45cd25db6031e259b11bc272c8ad9bb98fbc1e3741507f8ec0f5138057950823`; both directories and a `MANIFEST.tsv` of paths, sizes and hashes). The coordinator re-hashed every archived blob from a fresh clone of that pushed branch, and the package extracted from it verifies against its manifest. The pins are registered in `docs/evidence/PRIVATE_EVIDENCE.sha256`; `scripts/evidence_archive.py audit` reads the archive's `main`, so it reports them UNPUSHED until that merge lands and ARCHIVED after. The harness compiles and calls no production entry point. Image-first finding (static inspection): the worker image's build context cannot carry the harness (`image.py`, `runtime.py` import closure), so `host_venv` is the expected runtime under CP-1a (2)(d). That inspection is an input, not proof: the runtime is decided only when the Linux probe and dry run record image-first feasibility ([dispatch record](#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27)). If Stage 1b runs on `host_venv`, PA-5 validates the mismatch at C3. **Measurement readiness is not established.** It still needs Windows Stage 1a and the Linux accounting probe and dry run, including failure handling and cleanup ([dispatch record](#h1-steps-b-and-c-dispatch-record-frozen-2026-09-27)). After the operator merges: Stage 1a, the optional Stage 0 and then the Stage 1b dispatch, within the §12.7 caps; step (c) **RETURNED, REVISED twice and ACCEPTED 2026-09-27** ([#525](https://github.com/Joshua-Asante/first-passage/pull/525) at `011ce9e4`). The first revision carries the same-day rulings on its open questions and drafter's additions ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--h1c-draft-open-questions-and-drafters-additions-2026-09-27)). The second applies the operator's three review corrections, made before full-text acceptance: the S5 run-tooling scope covers the workflow validators, the subset handling, `guard_s2_runs.py` and the regression tests; the C3 order is explicit (review, grant, run, then Stage 2/PA-5); and the build-entry text is applied against a pinned head that CP-1b then names. The coordinator verified all three at `875ecf29`. **Full text ACCEPTED by the operator at `011ce9e4`** ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-acceptance--h1c-full-text-accepted-build-entry-sections-to-be-applied-2026-09-27)). The build-entry sections are **applied in [#527](https://github.com/Joshua-Asante/first-passage/pull/527) at `afa26a66`**, against the pinned head `875ecf29`. That PR changes only two files: the S5 packet (RC-6 re-anchor) and the slices plan (§3.4(d)). The coordinator verified all 96 added lines against the accepted note at `011ce9e4`: the only differences are the filled placeholders. RC-6 is met once #527 is merged and reviewed and CP-1b names that revision. The RC-2 sections wait for C3. Still open: OQ-1, plus Q1, Q7 and Q9 to C3 | RC-3a for CP-1b |
| H2 | Broker route commissioning | **RETURNED and ACCEPTED 2026-09-27**: [packet](../../notes/2026-09-27-route-commissioning-session-packet.md). Owed before any CP-3: the §3.7 request-body step (primary checkout). The M2 dispatch (X-2) is carded 2026-09-27 ([M2 card](2026-09-27-m2-modify-semantics.md)); its execution needs a local session in the primary checkout | CP-2 now; then CP-3 per row |
| H3 | ORB lifecycle and fence: disposition, owner text for Ruling 7, H4 card | **RETURNED and ACCEPTED 2026-09-27** ([disposition](../../notes/2026-09-27-orb-fence-ruling6-disposition.md)); operator answers applied (§5 addendum entry; inclusive stale boundary) | H4 |
| H4 | Fence classification: synthetic repair plus ORB L1 replay correction | **RETURNED and ACCEPTED 2026-09-27**, synthetic scope ([PR #522](https://github.com/Joshua-Asante/first-passage/pull/522) at `9e18d85`; [card](2026-09-27-h4-fence-classification-orb-l1-repair.md), *Coordinator acceptance of the return*; the real producer, route integration and the CC-3 halt are still owed) | Synthetic half of the fence obligation; the replay correction before freeze; CP-5 input |
| H5 | Attended operations | Step (a) **RETURNED and ACCEPTED 2026-09-27** (halt/resume amendment, with the O-6/O-7 clarifications applied); step (b) **RETURNED and ACCEPTED (PARTIAL, §7 (B)) 2026-09-27** ([PR #521](https://github.com/Joshua-Asante/first-passage/pull/521) at `32e0863`; [card](2026-09-27-h5b-attended-incident-rehearsal.md), *Coordinator acceptance of the return*; CC-3 stays open); the stale-individual-signal node was removed by a recorded variance (§10), and the operator ruled the classification the same day (a late bar is a source incident; halt/resume §4.1) | T13 construction |
| H6 | Settlement evidence | Collection READY ON CP-2; rehearsal harness READY | CAP S1/S2 toward QUALIFIED |
| H7 | Production qualification host | **RETURNED and ACCEPTED 2026-09-27** ([note](../../notes/2026-09-27-host-obligations-assignment.md)); RC-5 recorded in the ledger; RC-4 slice accepted at CP-1a (5), so the RC-4/RC-5 assignment at build entry is met ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--cp-1a-decisions-16-adopted-as-recommended-hold-kept-2026-09-27)); host cost owed before CP-8 | RC-4/RC-5 assignment (S5 build entry); later CP-8 |
| H8 | Feed (provider-neutral) | Step (a) **RETURNED and ACCEPTED 2026-09-27** ([note](../../notes/2026-09-27-feed-provider-neutral-preparation.md); [draft spec](../../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md)); step (b) **RETURNED and ACCEPTED 2026-09-27** as documentary classification ([PR #524](https://github.com/Joshua-Asante/first-passage/pull/524) at `a1a3c3e`; [note](../../notes/2026-09-27-h8b-feed-gap-classification.md), *Coordinator acceptance*; Q-1 PROPOSED in spec §4.3, Q-2 parked, Q-3/Q-4 ruled into halt/resume §4.1); step (c) PREPARED, READY ON this card's merge and #521 ([card](2026-09-27-h8c-omission-incident-session-end.md)) | CP-7 inputs; the F1 feed section; the empty-interval rule before CP-6; verification of the omitted-slot ruling |
| H9 | Result/seal and recovery | Preparation READY ON S5 C3 accepted; R1 ON S5 acceptance; R2 ON D3 text and R1 | T06/S8 |
| H10 | Final launch | LATER | CP-9 |

---

## H1 — S5 measurement: correct the #519 proposal, return a measurement dispatch

**Continues:** the #519 S5 Part A measurement proposal at `8c15f18`, which carries its coordinator review ("ACCEPTED AS INPUT; nothing approved; S5 stays HELD"). It is not redone.

**Uncertainty resolved:** (a) whether the proposal, corrected for the 2026-09-27 split, is ready for the operator's approval as a rule plus a concrete measurement dispatch. (b) After approval: the measured CPU, wall time and memory of PART_A at forced maximum expansion on the existing engine, and the provisional ceiling that follows.

**Prerequisites and existing authorization:**
- Step (a): operator ruling 2026-09-26 §6, which authorizes *preparing* the proposal only.
- Step (b): **CP-1a approval of the dispatch returned by (a)**. Preparation authority does not authorize any measurement, CI-configuration change, Linux dispatch or artifact download.

**Step (a) work: amend the #519 proposal; write a corrected revision, not a new analysis.**
- **Carry forward unchanged, as findings:**
  - the (2, 4, 2) fixture cannot expand, so maximum expansion needs the forced arm (§0.1);
  - no existing measurement covers maximum expansion;
  - `verify_for` dominates;
  - the engine's pilot predicate needs the PA-2b term;
  - no host factor is evidenced;
  - the three `/v7` `diagnostic_budget_profile` pitfalls and the fixture-cap tuple.
- **Keep every review correction:**
  - the cold repeat is included;
  - setup CPU is excluded from Ĉ;
  - D̂ stays uncovered until Stage 1c;
  - Windows figures validate the harness only;
  - host venv versus worker image is disclosed;
  - Stage 0 is calibration only;
  - the D2 falsifier stays open until a valid Stage 1b record.
- **Preserve the requirements:**
  - maximum expansion (forced arm, 4 panels);
  - the reference runtime (the `ubuntu-24.04` qualification runner class, identity recorded per run);
  - aggregate memory: PA-3 is a check against the one shared campaign footprint, never a per-phase value;
  - measurement validity: PA-4 (digests identical, prefix byte-identical to the prescribed arm, spread ≤ 1.30 with one re-run).
- **Update for 2026-09-27:**
  - RC-1 is met on `main` (#517 merged at `5ad04cf`).
  - The RC table is restated on the build-entry, C3 and before-F1 split ([ledger](../../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27)).
  - Pre-build feasibility is §5's arithmetic on the proposed `/v7` values; the executed `bind_budget` check moves to C3 (RC-3b).
  - RC-4/RC-5 are assigned via H7 and do not wait on F1.
  - **Rule scope: PART_A only, TEST_ONLY** (ruling 2026-09-27). Drop Stage 1b-N2 and the phase-generic option. `/v7`'s N2 ceiling is returned as a separate operator decision (for example, extending the M13 "/v6 only" ruling). The multipliers stay candidates.
- **Return a concrete measurement dispatch, as one approval packet.** For each step it gives the exact commands, the files created, the grants it needs, its limits, stop conditions and outputs:
  - Stage 0: download the S4 run artifacts, calibration only. It must run before the logs expire around **2026-10-09**. *[2026-09-27: the download was done on 2026-09-26 (ledger, conditional ruling entry). The read step is optional calibration, and the expiry binds only if the preserved set does not cover its inputs ([r2 §16.4](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#164-stage-0)).]*
  - Stage 1a: Windows harness validation.
  - Stage 1b: a new `workflow_dispatch` measurement workflow file, which is a CI-configuration change, and its two-job Linux run.
  - Stage 1c at C3.
  - The host-venv or worker-image choice.

  Also give the total expected runner time and the re-run limit (one per failed validity check).
- **Operator decisions for CP-1a:** *[2026-09-27: superseded by the six decisions in [r2 §14.1](../../notes/2026-09-27-s5-part-a-measurement-proposal-r2.md#141-refreshed-decision-list-2026-09-27), which fold in #519's decisions 1–7.]* #519 proposal §8 decisions 1 and 4 (the rule's parameters, and the measurement steps including host venv versus worker image). Decision 2 (scope) and decision 5 (arithmetic as pre-build feasibility) were **ruled 2026-09-27**. Decision 3 (the `/v7` N2 ceiling) returns as a separate ruling, not under the rule.

**Acceptance conditions for the corrected proposal (operator, 2026-09-27).** Step (a) is not accepted unless both hold.
1. **Stage 1c forces maximum expansion through the built adapter.** The dispatch specifies exactly how the Stage 1c run reaches `expanded_panels` through the S5 adapter's own Part A compute (`compute.run_part_a_compute` or its accepted successor). The run includes the **real N2 FULL baseline derivation from staged N2 capture bytes** and the **real S5-D1 two-artifact writing with its fsync**, all inside the measured workload boundary. Forcing uses a TEST_ONLY measurement override whose existence and scope are stated: which parameter, where it is injected, and proof that no production or signed route can reach it. A harness-level stand-in or a prescribed (non-expanding) arm does not satisfy this. If the adapter cannot be forced without a production-reachable seam, return BLOCKED with the proposed seam.
2. **Complete aggregate-memory evidence.** The memory input is the peak for the whole measured unit, every descendant included: cgroup `memory.peak` / systemd `MemoryPeak` with swap off, taken on each timed repeat. It is compared against the one shared campaign footprint (PA-3). If any repeat lacks it and only a lower-bound fallback exists (`ru_maxrss` of one process, or a Windows working set), **memory feasibility is recorded as UNVERIFIED**, the rule is not applied to that record, and the dispatch says so. A lower bound never satisfies PA-3.

**Step (b) work (after CP-1a only):** execute exactly the approved steps. Then apply the approved rule per #519 proposal §6 as a **provisional** TEST_ONLY ceiling, recorded in a ledger entry. Nothing outside the approval.

**Limits:**
- Step (a) is documentary: no measurement or dispatch, and no edit under `ops/`, `tests/`, `tools/` or `.github/`.
- Step (b): only the approved workflow file and harness files; no profile, ceiling or release-literal edit (those land with the S5 build).
- No production value, ever.

**Stop conditions (b):**
- a PA-4 validity failure twice;
- digests differ between repeats;
- Σ arithmetic fails at every admissible value.

Each of these returns at once; the last is the D2 falsifier.

**Recovery:** measurements are side-effect-free. A failed repeat is retained, never dropped.

**Evidence retained:**
- (a) the corrected proposal revision and the dispatch packet;
- (b) `docs/notes/<date>-s5-part-a-measurement/` in #519 proposal §3.5 schema, with run IDs and records;
- class `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`.

**Decision unlocked:** (a) → **CP-1a**. (b) → RC-3a, and with the other build-entry conditions, **CP-1b** (hold release for the build).

**Step (c), added at the acceptance of step (a) (2026-09-27; owner assigned for the cross-handoff critic's finding X-02):** draft, for the operator's acceptance, the S5 owner text that build entry and C3 need:
- the §3.4(d) text (S5 draft §4 and the consistency correction), a build-entry condition;
- the RC-6 re-anchor of the S5 packet at the release head, carrying #519's findings, the three `/v7` pitfalls and the SR/P set approved at CP-1a (with the SR-7 exception only if approved);
- the RC-2 owner-text set (boundary spec §3.1; full-E1 spec §2.2a, §2.4, §2.5, §2.6 and §5; slices plan contract decisions 3 and 6 and the S5 text), a C3 condition.

Drafting may start now. Owner documents are amended only after the operator accepts the text. The RC-6 re-anchor waits for CP-1a's SR/P decision.

**Grants at dispatch:**
- (a) and (c) coordinator: `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.
- (b) worker: `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`, plus `ci.dispatch` only for the CP-1a-approved workflow. Acceptance: the approved harness's validity checks and `tests/ops/qualification/test_part_a.py` passing unchanged.

### H1 steps (b) and (c): dispatch record (frozen 2026-09-27)

**Instruction.** On 2026-09-27 the operator directed, in session:
- "Continue preparing the approved H1(b) harness and dispatch-only workflow; CP-1a already authorizes that work";
- "Prepare the H1(c) owner-text and RC-6 draft alongside it, returning that draft for acceptance";
- "Keep the ruling PR separate from implementation".

Its follow-up direction: freeze each worker's instructions; treat H1(b)'s checks as preliminary; correct the H8(b) file ownership.

**Frozen inputs** (both steps):
- **Ruling:** the CP-1a ruling at commit `baa09ffd`, the ledger entry "Operator ruling — CP-1a decisions (1)–(6) adopted as recommended, hold kept, 2026-09-27". Each worker reads it as `git show baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` while [#523](https://github.com/Joshua-Asante/first-passage/pull/523) is pending.
- **Packet:** r2 at `origin/main` `875ecf29`, including its §16 reconciliation.
- **Branch base:** `origin/main` `875ecf29`.
- **This record:** the commit that adds it. Where the inline worker briefs and this record differ, this record governs.

**Step (b): the harness and the dispatch-only workflow** (branch `claude/h1b-part-a-measurement-harness`; one PR).
- **Allowed files:**
  - the harness directory `docs/notes/2026-09-27-s5-part-a-measurement/`: `measure_part_a_max.py.txt`, the support files r2 names, and a `README.md`;
  - one new dispatch-only workflow under `.github/workflows/`, triggered by `workflow_dispatch` only.

  Nothing else. That excludes any profile, ceiling, release literal, anything under `ops/` or `core/`, and every owner or governance document.
- **Acceptance checks, which are PRELIMINARY: they establish basic tooling behavior only.**
  - `check` exit 0;
  - any workflow inventory or lint tests pass;
  - `py_compile` of the harness;
  - `--help`;
  - `--summarize` on synthetic rows;
  - the diff limited to the allowed files.

  **Measurement readiness is established later, not by these checks**:
  - Windows **Stage 1a** on the operator's host (r2 §12.2);
  - the approved Linux accounting **probe and dry run** (r2 §12.3), including the I-1/I-6 failure handling, unit and artifact cleanup, and the **image-first feasibility** that step (b) records first (CP-1a decision (2)(d)).

  The static image-context inspection is an input to that feasibility, not proof of it.
- **Return boundary:**
  - one ready-for-review PR against `main`, with the status, the files, an r2 requirement map, the image-first finding and what was not run;
  - no measurement, engine run, dispatch, re-run or artifact download;
  - the operator merges.

  The Stage 1a, Stage 0 and Stage 1b execution that follows stays under the CP-1a dispatch approval and its §12.7 caps.

**Step (c): the owner-text and RC-6 draft** (branch `claude/h1c-s5-owner-text-draft`; one PR).
- **Allowed file:** `docs/notes/2026-09-27-s5-owner-text-and-rc6-draft.md` only.
- **Acceptance checks:**
  - the link check reports `bad 0`;
  - `check` exit 0;
  - the diff is only that note.
- **Return boundary:**
  - a DRAFT returned for the operator's acceptance: the §3.4(d) text, the RC-6 re-anchor carrying the CP-1a SR-1..SR-9/P-1..P-7 set, and the RC-2 owner-text set;
  - open questions stay listed, not decided;
  - **no owner document is amended** until the operator accepts the text.

**Exclusions, corrected 2026-09-27.** H8(b)'s deliverable is its classification note, `docs/notes/2026-09-27-h8b-feed-gap-classification.md` ([#524](https://github.com/Joshua-Asante/first-passage/pull/524)). Neither step touches it. The feed-preparation note and the feed-equivalence spec draft are **not assigned to the H8(b) worker**. They stay out of both steps because they are outside scope. Any edits to them are follow-up owner work, assigned separately. Status rows in this handoff set are coordinator-owned; neither worker edits them.

**Unchanged:** S5 stays **HELD** until RC-3a and the remaining build-entry requirements support CP-1b.

## H2 — Route commissioning session packet (operator-run, automation disarmed)

**Uncertainty resolved:** what the exact route actually does, one micro contract at a time, for:
- an entry carrying its stop;
- the stop `Working` at the filled quantity;
- a cancel of a resting entry and its children;
- a rejected change;
- the normal case of whole-leg liquidation (C-a, investigation only);
- same-session and prior-session reconciliation reads.

**Prerequisites and existing authorization:**
- Gate A accepted (REST §6.11).
- The [drill plan](../../notes/2026-09-26-tradeify-route-drill-plan-draft.md) owns the rows. This packet sequences them and does not become a second owner.
- [Incident ADR §A11.1](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a111--operator-ruling-close-direction-2026-09-26) authorizes R-1/R-2 only, once entitlement is confirmed. It requires each order-producing row to be prepared individually with its environment, actions, exposure limits and abort/recovery. The race drill X-5 is deferred. There is no automatic fallback to the live eval.
- **Consumed, not redone:** the #519 close-semantics return. M questions and §1.1a (a)–(e) are all OPEN or CONFLICTING. It also supplies the draft vendor question (note §6), two actor-inventory candidates (the platform timed exit and firm-side auto-liquidation), a packet §1.1 wording correction, and the X-3 read addition.

**Work:** write `docs/notes/<date>-route-commissioning-session-packet.md`.
- **Stage 0 (read-only; before it: CP-2):**
  - host confirmation that the rail is disarmed (`dry_run=true`, `emit_enabled=false`);
  - the §0.1 actor inventory as a checklist, with every Account Manager function disabled (CR-12) and #519's two candidates added;
  - the entitlement record;
  - the known-order confirmation;
  - R-2 and the T07 reads on a completed preservation trade where it meets their evidence requirements;
  - R-1 only in the same session as a preservation trade the operator places anyway (addendum §1.3).
- **Stage 1 (order-producing; before each row: its own CP-3 written authorization):**
  - X-1, X-4 and X-2 (the last after M2).
  - X-3 only as part of the operator's residual-risk decision (CR-3), because #519 left M OPEN/CONFLICTING. It includes #519's X-3 read addition.

  Each row gets:
  - its environment;
  - exact actions;
  - one micro contract per request and in total, with the stop in the same request;
  - placeholders for the operator-fixed stop distance, time in market, window and cost ceiling (no figures in the repo);
  - its stop conditions;
  - the drill plan's five-step recovery;
  - its evidence entries.
- **Session rule:** one row at a time; its traces return and are reviewed before the next row is authorized.
- **Operator-sent text:** #519's vendor-question draft, and the one permitted T08 follow-up. Vendor contact is the operator's.
- **CP-2 fact list:** entitlement, sim/demo availability, the known-order definition and read target, whether drill costs count against the $700 ceiling, and preservation-trade treatment (drill plan q9, OPEN).

**Limits:**
- Documentary only: no account access, vendor contact, order or figure.
- Nothing wider than the drill plan's one-contract limit.
- X-5, C-b rows and the GC-5 takeover composite are excluded.

**Stop conditions to write into the packet:**
- any `unknown` outcome: no resend, read first;
- a stop not `Working` at quantity 1 within the wait;
- an unexpected position or working order;
- competing-actor activity;
- a rail state other than disarmed;
- the time limit reached.

**Evidence retained:**
- the packet itself;
- after a session: original bytes under the drill plan's private manifest (hashes only in the repo), plus one outcome line per step, recorded against CAP R2–R5 / T08 §7 behavior rows as `COMMISSIONING_OBSERVATION` with scope.

**Decision unlocked:** **CP-2**, then **CP-3** row by row. Reviewed traces support capability acceptance for their scope and feed CP-5.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `python scripts/check_handoff_authority.py --all` and `make check` clean on the branch.

## H3 — ORB lifecycle and fence: disposition, owner text for Ruling 7, H4 card

**Continues:** the #519 ORB lifecycle evidence and four-state trace at `8c15f18`, each "ACCEPTED AS INPUT". No new source read or trace. The decisions are made ([§59 Ruling 7](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27): L1 with the earlier operational cutoff, and the fresh-evidence classification contract).

**Uncertainty resolved:** the exact owner text that implements Ruling 7, and a bounded, verifiable repair card.

**Prerequisites and existing authorization:** Ruling 7, which authorizes "the bounded synthetic repair and corresponding specification/replay corrections, retaining real-producer and route acceptance obligations".

**Work:**
1. **Coordinator disposition.** For each lifecycle-note conflict C1–C5 and each trace defect and ambiguity, record whether it is resolved by Ruling 7 or still open, with the owner.
2. **Owner text, applied as dated amendments under each owner's own convention:**
   - **Rail spec:** the §1 `pending` clarification (trace §6.1) worded to Ruling 7(b). S2's one-bar sentence per L1. S4's "stale resting entries" and AC-8 aligned to L1. The halt/resume §5 cutoff overlay is unchanged.
   - **Replay spec:** RC-9 amended so the one-bar cancel does not end ORB's base entry. RC-4's parity basis is kept.
   - **Edition pre-registration:** ORB-1 states the L1 lifecycle in words (it is DRAFT, with a dated marker).
   - Where #519's §6.2 text and Ruling 7(b)'s "stale at one bar" differ at the boundary, **the ruling's words govern**. The divergence is recorded, and the boundary is pinned as the ruling states it.
3. **H4 dispatch card,** in its own file with its `yaml authority` block:
   - **Scope:** trace §6.2–§6.4 against the synthetic seam, plus the qualification replay correction (`replay.py:507-509` and its pinned test), as separate checkpoints.
   - **Owed items:** the real evidence producer, route integration and the ordinary-unknown halt (packet CC-3; T09/TB-I3).
   - **Freeze-inventory effect** of the replay change.

**Limits:**
- No code change.
- No private source read.
- No wording beyond what Ruling 7 decides. Any extra choice (for example strict versus inclusive, if the ruling's words leave it open) is returned, not made.

**Stop conditions:**
- An owner's change-control forbids the amendment form.
- Ruling 7 does not decide a point the text needs.

In either case return with the question.

**Recovery:** not applicable (documentary).

**Evidence retained:** the disposition note, the owner-text diffs and the H4 card, citing `8c15f18` line anchors.

**Decision unlocked:** coordinator acceptance of the owner text and the card, which makes H4 dispatchable.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean and `python scripts/check_handoff_authority.py --all` clean.

## H4 — Fence classification: synthetic repair plus the ORB L1 replay correction

**Uncertainty resolved:**
- Whether the owner and its consumers classify and act on states (i)–(iv) as Ruling 7(b) says, before any real producer exists.
- Whether the qualification replay keeps ORB's base entry working per L1.

**Prerequisites and existing authorization:** Ruling 7, which authorizes the bounded synthetic repair and the replay correction. H3's owner text and this card's final form must be accepted by the coordinator before dispatch.

**Work, in two checkpoints returned separately:**
- **(F) Fence**, tests first. Cover trace §6.4 cases 1–12 as Ruling 7(b) words them:
  - stale at one bar, pinned;
  - a positive lookup does not resolve state (iii);
  - terminal evidence resolves only the request it covers;
  - refreshed evidence never restores permission after a halt.

  These run against the `SyntheticBroker` seam with synthetic evidence acquisitions. Then the change in `book_account_owner.py` and each traced consumer: admission, loosening amends (`book_protection_owner.py`), takeover fence and quiescence (`book_takeover_owner.py`), with the unchanged consumers re-pinned. The pinned behavior at `tests/ops/test_book_feedback_journal.py:41-55` changes only as the ruling requires, and is listed explicitly.
- **(R) Replay:** correct the one-bar cancel so ORB's base entry follows L1, with `test_replay.py:214-223` re-pinned and parity with the emulator shown. This is an E1 freeze-inventory change. Its record goes to the freeze inventory, and qualification Linux evidence is refreshed as the coordinator directs.

**The return must separate:**
- **(1) Verified synthetically:** classification and consumer behavior per case, and the replay correction, each with node IDs.
- **(2) Still owed:** production of real order-level evidence (the producer), route integration, and the rev9 halt for ordinary unknowns (T09/TB-I3). It must also state that **the fence obligation is not resolved** until (2) is accepted.

**Limits:**
- No production transport (T09).
- No `lab↔ops` import, locked parameter or DD constant.
- No private port run.
- Branch and PR; the operator merges.

**Stop conditions:**
- a consumer the trace missed;
- a needed change outside the owner, its consumers and the replay;
- an emulator-parity break.

In each case return to the coordinator.

**Recovery:** a branch revert. No shared state is touched.

**Evidence retained:** the node IDs per case, the launcher `record.json`, `make check`, and the replay's before/after parity record.

**Decision unlocked:**
- The synthetic half of the fence obligation and the replay correction are accepted before the freeze inventory is fixed.
- Both are input to **CP-5**.
- The remaining half is named in T09's scope.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the node set named in H3's card.

## H5 — Attended operations: apply the resumption ruling, then synthetic incident rehearsal

**Uncertainty resolved:**
- (a) The halt/resume owner text that implements §A11.2.
- (b) Whether alerts, escalation, heartbeat, fencing, manual intervention and restart behave as ruled, tested with synthetic incidents.

**What is ruled:**
- [§A11.2](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27) (2026-09-27): for commissioning and the first attended release, an incident ends automated trading for that session. Operator recovery and evidence collection continue, and review comes before another session. It applies to incidents, not to correctly handled signal or capacity refusals.
- §A11 items 1, 2 and 4 stand.
- Rev9 §4's conditional same-session resumption remains the text for other contexts. The ruling does not decide later releases.

**Work:**
- **(a)** A dated amendment to the [halt/resume contract](../../spec/2026-09-14-tb-s3-halt-resume-contract.md) §4 applying §A11.2 to those two contexts, following that contract's amendment convention. Also a pointer in the [Phase 5 plan](../../superpowers/plans/2026-09-16-phase5-attended-operations.md) stating that its proposed restriction is now ruled for these contexts. Then a step (b) dispatch card with its `yaml authority` block.
- **(b)** After (a) is accepted: a synthetic incident script (lost response, stale evidence, missed alert, restart during halt, ambiguous protection). Show that no automation restart path exists within the session after an incident, including a deliberate operator stop (O-6), and that a correctly handled refusal does not end the session. *Amended at acceptance 2026-09-27 (cross-handoff critic X-06):* real delivery and 60 s escalation are measured in T13 (Phase 5 WP2). The exception is if the operator runs the delivery leg on an existing, no-spend channel at dispatch.

**Limits:**
- No rail deploy or arm, and no account traffic.
- A notification channel that needs spend or a new account returns to the operator before use.
- (a) adds no rule beyond §A11.2.

**Stop conditions:** any path that restarts automation in the same session after an incident, or that ends a session on a correctly handled refusal. Stop and return; it is a defect.

**Recovery:** rehearsal state lives in disposable stores and is discarded after its evidence is retained.

**Evidence retained:** (a) the owner-text diff and the (b) card. (b) Delivery and escalation timing traces, restart and restore traces, and the incident-versus-refusal cases.

**Decision unlocked:** (a) → coordinator acceptance, then (b). (b) → T13 construction, with H2's commissioning traces folded in before any session that could produce an unresolved request.

**Grants at dispatch:**
- (a) coordinator: `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`.
- (b) worker: `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`.
- Acceptance for (b): the rehearsal test nodes named in the (b) card.

## H6 — Settlement collection and reconstruction rehearsal

**Uncertainty resolved:**
- Actual report coverage.
- The three S2 source facts: the `Timestamp` offset, the `Date` meaning after the rollover and the query-bound semantics ([CAP addendum 2026-09-24](../phase4-preparation/2026-09-16/capability-decision.md)).
- Missing-data detection.
- Whether the verifier and account owner reconstruct an anchor and a subsequent close from original bytes.

**Prerequisites and existing authorization:**
- The 2026-09-25 account-side read authorization (T07).
- The target is ruled ([incident ADR §A11.3](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a113--operator-ruling-preservation-trade-evidence-as-the-target-of-authorized-reads-2026-09-27), 2026-09-27): a completed operator-placed preservation trade, where it meets the reads' evidence requirements, in place of the D1 transaction. CP-2 confirms the transaction identity. A completed trade cannot supply a new same-session observation. No additional trade is authorized.
- The rehearsal harness may be prepared before CP-2.

**Work:**
- **Operator collection.** Report originals covering the target transaction, with the report context captured: timezone setting, query bounds, and a row after the rollover. Stored in the private root and hashed into its manifest.
- **Agent rehearsal**, on the operator's machine for private bytes:
  - isolated anchor ingestion and a subsequent-close ingestion;
  - correction refusal and restoration;
  - a missing-data case;
  - the time the procedure takes.

**Limits:**
- Read-only exports; no account reset; no API use while API entitlement is unverified.
- Private bytes never committed.

**Stop conditions:** an unsupported decisive source fact. Return promptly and continue only independent collection (T07 checkpoint).

**Recovery:** the rehearsal stores are disposable. No silent predecessor reset.

**Evidence retained:** manifest hashes, consumer traces with record IDs, and the timed procedure. CAP S1/S2 rows are proposed for coordinator acceptance.

**Decision unlocked:**
- The S3/B7 predecessor decision.
- The requirement for an operator-facing sign/submit entry point, scoped to T09 or tooling.

**Grants at dispatch (worker, for the harness):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. Acceptance: the reconstruction consumer test nodes named at dispatch. Collection is operator-performed.

## H7 — Production qualification host: specification and OF assignment

**Uncertainty resolved:**
- Who verifies each of OF-1..OF-7, at which gate, and where the record lands (RC-5).
- Which gate set governs OF-5..OF-7 (S5 draft §6 Q12).
- The owner and slice of the client plan-view seed change (RC-4).
- What a production-class host needs, and what it costs.

**Prerequisites and existing authorization:** the 2026-09-26 direction to "assign seed-view implementation and host attestations to their specified gates". The seat does not choose the owner itself; it proposes.

**Work:**
- **Proposed owner text.** Recommend the stricter reading of Q12: every OF at provisioning, before any production-authority release and after any access change, plus the specific OF-5/OF-6/OF-7 gates.
- **Host specification:**
  - OS and cgroup v2 / systemd features;
  - the `qclient`/`qexec`/`qg5`/`qseal` principals;
  - key storage and custody;
  - enrollment inputs;
  - K3 salt custody.
- An itemized cost line if provisioning needs spend.
- A named slice for the RC-4 seed view, with its F1 admission check.

**Limits:** documentary only. No host rental, credential creation or key generation.

**Stop conditions:** an OF that cannot be verified by an attended read. Return it as a contract question.

**Recovery:** not applicable.

**Evidence retained:** the proposal note and the owner-text diffs, pending acceptance.

**Decision unlocked:**
- The RC-4/RC-5 assignment, which is a build-entry condition for S5 (ledger 2026-09-27). The implementation and the attestations stay before F1.
- Later, **CP-8**: provisioning and admission.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

## H8 — Feed: provider-neutral preparation

**Uncertainty resolved:** what the funded provider must satisfy for all four symbols before trading use, stated before any provider is chosen.

**Prerequisites and existing authorization:** STATE's source disposition, which allows provider-neutral preparation. D-feed bars signup, subscription and credential staging.

**Work:**
- The TB-I5 successor, a CME execution-feed equivalence test specification (no such spec is on disk).
- Symbol, roll and session mapping for the four legs.
- Gap, reconnect, correction/backfill, duplicate/out-of-order, stale-symbol and DST/early-close handling, specified against the canonical panels.
- The **later-binding rule** text for the F1 packet (addendum §1.4).
- A shadow-collection design with emission disabled.

**Limits:** no provider contact, account, credential or spend. No equivalence tolerance set after seeing data.

**Stop conditions:** a requirement that only a specific provider can answer. Record it as a funding-decision question.

**Recovery:** not applicable.

**Evidence retained:** the spec drafts and the rule text.

**Decision unlocked:** inputs to **CP-7** (funding) and to the T10 phase-2 F1 packet.

**Grants at dispatch (coordinator):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

**Step (b), added at the acceptance of step (a) (2026-09-27; owner assigned for the cross-handoff critic's finding X-05).**
- **What:** classify the private gap queue (`calendar-gap-queue.json`, digest `509346d6…`; execution domain `:485–:502`) against the consumer's contiguity and four-leg barrier rules (`book_runtime.py:376–:391`). That includes the 171 residual regular-session gaps (`:689–:691`): are they no-trade quiet slots or missing input?
- **Where:** documentary, run on the operator's machine, because the queue is private. No data is committed; only counts, classes and digests return.
- **Returns to:** the operator, for the spec §4.3 empty-interval rule. If an omitted in-session slot would halt the book, it also goes to TB-I3 and to the halt/resume owner (the §A11.2 incident question).
- **When:** before CP-6.
- **Grants (coordinator, on the operator's machine):** `repository.read`, `worktree.write`, `governance.author`, `branch.push`, `pr.open`. Acceptance: `make check` clean.

**Step (b) acceptance (2026-09-27).** Step (b) is ACCEPTED as a documentary classification. The return is [PR #524](https://github.com/Joshua-Asante/first-passage/pull/524), merged at `a1a3c3e`. The acceptance establishes the classification result: one observed affected permitted session in the reconciled common window, and 170 of the 171 residual gaps on holiday account days. It does not settle the cause of the omission, give a rate, or qualify a live feed ([note](../../notes/2026-09-27-h8b-feed-gap-classification.md#coordinator-acceptance-2026-09-27)). Carried forward:
- **Q-1:** PROPOSED text in the draft equivalence spec §4.3. The operator adopts it at freeze, before CP-6.
- **Q-2:** parked until an exchange record or an independent source can corroborate the event.
- **Q-3 and Q-4:** ruled by the operator on 2026-09-27, in session. The ruling is recorded in the [halt/resume contract §4.1](../../spec/2026-09-14-tb-s3-halt-resume-contract.md#41-amendment-2026-09-27-incident-versus-correctly-handled-refusal), *Qualifications*.
- **Outstanding:** a later-session re-arming design, for TB-I3 and the resume decision. No handoff builds it now.

**Step (c), added at the acceptance of step (b) (2026-09-27).** [Worker card H8(c)](2026-09-27-h8c-omission-incident-session-end.md) verifies the omitted-slot ruling against the existing owners, synthetically. It covers three things:
- the three omission detectors, and the late-bar regression kept separate;
- recovered bars, repeated activation and a reopened journal, through real entry points only;
- duplicate ids kept distinct from separate detector records.

The card changes no production code and invents no resume interface. It is READY ON its own merge and on #521's. The coordinator keeps acceptance of its results.

## H9 — Result/seal integration and bounded same-sample recovery (two checkpoints)

**Uncertainty resolved:** whether S1–S5 and the frozen T05 build hold as one integrated identity under interruption and exhaustion. Two checkpoints, returned separately. The coordinator keeps combined acceptance.

**Prerequisites and existing authorization:**
- **Integration preparation:** S5 Checkpoint C3 accepted (the PART_A field sets, the `/v8` snapshot and the capture contract are stable), and the existing T05 build acceptance.
- **Checkpoint R1, integration acceptance:** full S5 acceptance. This is the existing dependency ("Integrate the frozen head `6cf2732` after S5 acceptance"); it is not replaced.
- **Checkpoint R2, recovery-slice acceptance:** the D3 owner text (S5 draft §3.4) accepted, and R1 accepted.

**Work:**
- **Preparation**, from S5 C3: a branch integrating `claude/t05-result-seal@6cf2732` onto the S5 head, with the interface diff:
  - unify `_settlement_terminal`;
  - take main's `031d79a` roll, "never a fresh one";
  - seam row 11: the real seal principal and its host-provisioning change.

  No acceptance-grade run until S5 is accepted.
- **R1:** re-base the prepared integration on the accepted S5 head and run the acceptance-grade Linux result/seal node set. Return it on its own.
- **R2:** the D3 slice (R1–R10). The recovery retains every failed attempt and never renews the allowance or deadline. It allocates no attempt ID, salt, seed or plan, and makes no public reveal while recovery remains possible. Return it on its own.

**Limits:**
- No production authority, no route-enabling release literal before T06, and no accepted formula or tolerance change.
- No push while a Linux run is in flight.

**Stop conditions:**
- An integration conflict that changes an accepted interface.
- An S5 change after C3 that invalidates the prepared branch.
- Any path that redraws or renews allowance.

In each case return to the coordinator.

**Recovery:** branch-level only. Retained attempts are never deleted.

**Evidence retained:**
- R1: Linux qseal and result-G5 cases, and exhaustion and receipt-history cases (a receipt is history, not authority), plus Windows lines and `check`.
- R2: interruption and retry cases, retained-attempt history, and the no-renewal assertions.

**Decision unlocked:** R1 and R2, each accepted separately, then the coordinator's combined acceptance and T06/S8 dispatch on one identity.

**Grants at dispatch (worker):** `repository.read`, `tests.run`, `worktree.write`, `branch.push`, `pr.open`. The coordinator holds `ci.dispatch` for the Linux runs under its own grants. Acceptance: the R1 and R2 node sets named at each dispatch.

## H10 — Final launch: exact-candidate rehearsal and one attended session (LATER)

**Recorded now so it is not rediscovered:**
- The timed rehearsal runs on the exact T16 candidate with synthetic inputs: B7 capture → sole n3 → verdict/expiry/void rules → GO/reseal → restart → activation acknowledgment.
- Deployment GO and initial-session authority are separate operator acts at **CP-9**.
- The session is one attended session under preserve-and-block. Explicit review follows before any extension (§A11 item 1).
- Failure leaves the candidate disarmed or halted as prescribed. Elapsed time is never approval.
- The card is written when T16 is accepted.
