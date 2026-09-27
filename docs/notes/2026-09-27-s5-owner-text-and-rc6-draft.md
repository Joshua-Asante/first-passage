# S5 owner text for build entry and Checkpoint C3: the §3.4(d) text, the RC-6 re-anchor and the RC-2 set

**Status:** DRAFT, returned for operator acceptance; no owner document is amended. Every PROPOSED text below is a candidate for the operator's acceptance. Owner documents change only after that acceptance, by a separate application commit. S5 stays **HELD**: nothing here releases the hold (CP-1b), freezes or dispatches S5, sets a ceiling or changes an approved value.

**Card:** [handoff H1](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h1--s5-measurement-correct-the-519-proposal-return-a-measurement-dispatch), step (c) ("Step (c), added at the acceptance of step (a)"; owner assigned for the cross-handoff critic's finding X-02).

**Anchor head.** Every current-text quotation is at `origin/main` = `875ecf297ddda6e12af12e4e69f117deca8008c3` (`875ecf29`), written `875ecf29:<path>:<line>`. This head is the **candidate** release head for the RC-6 re-anchor. Each anchor is re-verified at the actual release head, the head named in the operator's hold-release entry (CP-1b), before any text is applied. `ops/c1_rail/qualification/` is byte-identical between the S4 merge head `228447c` and `875ecf29` (`git diff --stat 228447c 875ecf29 -- ops/c1_rail/qualification` is empty), and nothing under `ops/`, `tests/`, `tools/`, `deploy/`, `scripts/` or `.github/` changed between r2's source head `521d8f2` and `875ecf29`.

**Ruling commit and dispatch record.**
- **Ruling:** commit `baa09ffd` (`baa09ffd574d88fb4fd6983451067de479a90973`), the ledger entry "Operator ruling — CP-1a decisions (1)–(6) adopted as recommended, hold kept, 2026-09-27", at `baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:936-1004` ([blob at `baa09ffd`](https://github.com/Joshua-Asante/first-passage/blob/baa09ffd574d88fb4fd6983451067de479a90973/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L936)). It is on PR [#523](https://github.com/Joshua-Asante/first-passage/pull/523), not yet on `main`. Every ruled item carried here is quoted from that commit's text (`git show baa09ffd:…`). Short form below: **CP-1a (n)**, cited as `baa09ffd:…:<line>`.
- **Dispatch record:** commit `61a2ca41` (`61a2ca41dd379d6280f0a39c19081aa2d2ce7ac0`), "H1 steps (b) and (c): dispatch record (frozen 2026-09-27)" in the handoff set, at `61a2ca41:docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md:143-197` ([blob at `61a2ca41`](https://github.com/Joshua-Asante/first-passage/blob/61a2ca41dd379d6280f0a39c19081aa2d2ce7ac0/docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#L143)), also on PR #523. It governs where the inline brief differs. Step (c)'s allowed file is this note only; its acceptance checks are the link check at `bad 0`, `check` exit 0 and a diff of this note only; its return is "a DRAFT returned for the operator's acceptance: the §3.4(d) text, the RC-6 re-anchor carrying the CP-1a SR-1..SR-9/P-1..P-7 set, and the RC-2 owner-text set", with open questions "listed, not decided" and "**no owner document is amended** until the operator accepts the text" (`61a2ca41:…:184-193`).

**Earlier rulings applied** (quoted in the ledger's own words where they bind text here):
- The ledger entries on `main` ([execution-slices plan](../superpowers/plans/2026-09-18-full-e1-execution-slices.md)): the S5 hold (2026-09-25); [D1–D3 adopted, hold kept](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-directions-adopted-hold-kept-2026-09-26) (2026-09-26); the [conditional Part A ruling](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--part-a-measurement-rule-conditionally-approved-s5-held-2026-09-26) (2026-09-26); the [build-entry/C3 split](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-direction--s5-build-entry-separated-from-checkpoint-c3-acceptance-2026-09-27) (2026-09-27); the [staged-gates ruling](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27) (2026-09-27); the [RC-4/RC-5 assignment](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-assignment--rc-5-host-checks-recorded-and-rc-4-seed-view-slice-pending-the-operator-2026-09-27) (2026-09-27); the [coordinator entry reconciling CP-1a](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-entry--cp-1a-packet-reconciled-with-519s-merged-corrections-2026-09-27) (2026-09-27).

**Inputs:** [r2](2026-09-27-s5-part-a-measurement-proposal-r2.md) (§2, §7, §10.3, §12.4, §13, §14.1, §16); the [#519 proposal](2026-09-26-s5-part-a-measurement-proposal.md) and its [card](../briefs/handoffs/2026-09-26-s5-part-a-measurement-proposal.md) (merged; `R1M:NN` = `875ecf29:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md:NN`); the [S5 decision draft](2026-09-26-s5-decision-draft.md) (§1.4, §1.5, §2.3, §2.5, §3.4, §4, §5, §6); the S5 packet it re-anchors, the [S5/T04 packet draft](../briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md) (named by the draft's Inputs line and by the ledger's "S5/T04 packet drafted" entry); the [H7 host-obligations note](2026-09-27-host-obligations-assignment.md); the owner documents of item 3.

**Not granted:** no owner-document edit; no S5 release, freeze, dispatch or execution; no measurement, CI change, dispatch or download; no ceiling, profile or release-literal change; no decision on anything the rulings leave open; no production, activation or live authority.

---

## 0. How to read this note

Each passage gives:
- **Current** — the owner text at `875ecf29`, quoted exactly as a blockquote, with file and line;
- **PROPOSED** — the replacement or insertion and its exact anchor string. Text taken from the S5 draft or r2 is marked with its source. Anything beyond that source is marked **drafter's addition D-n** and listed in §6, where each can be accepted or struck on its own;
- **Required by** — the ruling or finding;
- **Gate** — **build entry** (the §3.4(d) text or RC-6) or **C3** (RC-2).

Placeholders: `<release head>` is the head the CP-1b entry names; `<acceptance date>` is the date the operator accepts the text.

| Item | Owner | Gate | Section |
|---|---|---|---|
| §3.4(d) text | slices plan, contract decision 6 and S5 Behavior | Build entry | §1 |
| RC-6 re-anchor | S5/T04 packet draft | Build entry | §2 |
| RC-2 set | boundary spec §3.1; full-E1 spec §2.2a, §2.4, §2.5, §2.6, §5; slices plan contract decision 3 (and 6 and the S5 text, already applied at build entry); S5 draft §2.3 (D2 reading) | C3 | §3 |

The build-entry row of the ledger's direction table lists "**The §3.4(d) text** applied (S5 draft §4, consistency correction)" and "**RC-6**: the packet re-anchored at the release head, including #519's findings that the (2, 4, 2) fixture cannot expand and the three `/v7` profile pitfalls"; its C3 row lists "The full RC-2 owner-text set accepted and applied" (`875ecf29:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:851-852`; the rows are quoted in part because their relative link resolves only from the ledger's directory).

---

## 1. Build entry: the §3.4(d) text

**What the text is.** S5 draft §3.4(d) holds two insertions into the execution-slices plan: one into contract decision 6 and one into the S5 Behavior paragraph. S5 draft §4 says S5's build needs only that text:

> - **D1 and D3** can be ruled at the same time. S5's **build** needs from them only the text in §3.4(d). §1.5(c) is not a build prerequisite: it lets TEST_ONLY campaigns keep `tb-s2-rng-v2` and asks no S5 code change, so it is release owner text under RC-2 (consistency-review correction 2026-09-26; governs). S5's **release** needs every §5 condition, including RC-2's full owner-text set, RC-4 and RC-5.

The consistency correction it cites (S5 draft line 49) removed §1.5(c) from the build prerequisites; §1.5(c) is RC-2 text at C3 (§3.3 below):

> | §4, second bullet | "S5's **build** needs from them only the text in §1.5(c) and §3.4(d)." | S5's build needs only §3.4(d). §1.5(c) is release owner text under RC-2, not a build prerequisite | §1.5(c) lets TEST_ONLY synthetic campaigns keep `tb-s2-rng-v2` and asks no S5 code change. §0 D1 already says S5 needs "not the K3 build", and §0 D3 says "S5's build needs only the §3.4(d) text" |

The S5 draft's own text of §3.4(d):

> **(d) Slices plan** contract decision 6. After "Missing capture never licenses another draw;", add: "a spec §2.6 bounded same-sample re-execution is not a draw;". In **S5 Behavior**, after "…no panel resume, replacement pilot or checkpoint rerun.", add: "S5 builds this terminal subset; the §2.6 re-execution is a later slice after S5 and before S8, and S5-D1's retained initial prefix is the retained complete record that full-E1 spec §2.6's comparison schema compares."

**Required by:** the ledger direction's build-entry row (`875ecf29:…full-e1-execution-slices.md:851`); CP-1a status "RC-3a, the §3.4(d) text and the RC-6 re-anchor remain open" (`baa09ffd:…:991`); S5 draft §5 RC-6 ("with the §3.4(d) text in place, so S5 builds terminal IN_DOUBT only", `875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:387`). **Gate: build entry.**

### 1.1 Slices plan, contract decision 6

**Current** (`875ecf29:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:91`):

> 6. **Signing recovery is durable.** Fixed payload, key, signing time and intent identity precede signing. Recover exact signed candidate/receipt on retry. Missing capture never licenses another draw; missing deterministic G5 validation may be repeated only under the original remaining budget. VOID/expiry/revocation bar new authority while exact historical receipts remain inspectable with current validity.

**PROPOSED** (S5 draft §3.4(d), verbatim). After "Missing capture never licenses another draw;" insert:

> a spec §2.6 bounded same-sample re-execution is not a draw;

The resulting sentence reads: "Missing capture never licenses another draw; a spec §2.6 bounded same-sample re-execution is not a draw; missing deterministic G5 validation may be repeated only under the original remaining budget."

Also **D-1** (qualified tag) and **D-2** (bridging note), §1.3.

### 1.2 Slices plan, S5 Behavior

**Current** (`875ecf29:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:233`):

> **Behavior:** Worker and G5 independently derive the same N2 FULL pass rate from captured outcomes. Preserve the disjoint Part A pilot addresses, outer panel seeds, path addresses and source occurrence order, including legitimate duplicate occurrences. Retain the exact original prefix before extending indices `[initial_panels, expanded_panels)`; the final prefix must be byte-identical. Conditional expansion uses inclusive tolerance equality. Apply the final floor and FULL sanity comparison after required expansion. A crash during panels without complete durable capture is IN_DOUBT: no panel resume, replacement pilot or checkpoint rerun.

**PROPOSED** (S5 draft §3.4(d), verbatim). After "…no panel resume, replacement pilot or checkpoint rerun." append:

> S5 builds this terminal subset; the §2.6 re-execution is a later slice after S5 and before S8, and S5-D1's retained initial prefix is the retained complete record that full-E1 spec §2.6's comparison schema compares.

### 1.3 Build-entry consistency: the §2.6 text lands later

Both insertions cite a full-E1 spec §2.6 rule ("bounded same-sample re-execution", "comparison schema") that is itself RC-2 text, applied only at C3 (§3.6). Applied verbatim at build entry, the plan would cite a spec rule that does not yet exist between build entry and C3. The split came after the S5 draft was written: the draft had one release point, and the 2026-09-27 direction put §3.4(d) at build entry and RC-2 at C3.

- **D-1 (qualified tag).** Append `(AUDIT-2026-09-25-qualification-assurance-contract-delta#N2)` after the contract-decision-6 insertion. S5 draft RC-2 requires each amendment to cite the qualified tag (`875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:383`); the §3.4(d) text does not.
- **D-2 (bridging note).** Append to each of the two insertions: *"[Applied `<acceptance date>` at S5 build entry. The full-E1 spec §2.6 rule cited here is RC-2 owner text, applied at Checkpoint C3; until then its source is the operator's D3 direction (ledger, 2026-09-26) and S5 draft §3.3.]"*

Whether D-2 is wanted is **OQ-2** (§5).

---

## 2. Build entry: the RC-6 re-anchor of the S5 packet

**The packet.** `docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md`, 64 lines at `875ecf29`, last changed at `a4a047ec` (drafted at `52e7836`, ledger entry "S5/T04 packet drafted and its three decisions ruled"). Its §7 executor return is "_Pending._".

**Required by:** the ledger direction's build-entry row, RC-6 (`875ecf29:…full-e1-execution-slices.md:851`); "RC-6 retained" (ledger 2026-09-26, `:809`); CP-1a (6): "H1 step (c) carries the approved set into the RC-6 re-anchor draft, which goes to the operator for acceptance" (`baa09ffd:…:985`); the not-granted line "any S5 packet or owner-text edit before the operator accepts the RC-6 text" (`baa09ffd:…:1000`). **Gate: build entry**, for every passage in this section.

**What it carries** (task list, each mapped in §4):
- #519's findings, including that the (2, 4, 2) fixture cannot expand (§2.2);
- the three `/v7` profile pitfalls, and the fixture-cap tuple (§2.2);
- SR-1..SR-9 and P-1..P-7 as CP-1a (6) approved them, SR-9 as adopted in r2 §16 C2 (§2.5);
- the SR-7 exception at lines 8, 35, 49 and 61, which CP-1a (6) approved (§2.1, §2.6, §2.7, §2.10);
- P-3, P-4 and P-5 as hard, non-waivable C3 preconditions, and a missing SR or failing P at C3 as a C3 nonconformance returned to the S5 executor (§2.5, §2.9);
- the named worker-side residual, carried by PA-5 (§2.5);
- the SR-8 export extension with the PART_A result's `probe_seconds` and `predicted_seconds` (§2.5);
- the `/v7` N2 value (§2.1, §2.4).

**Re-verification rule.** Every anchor in §2.2 is at `875ecf29`. At the release head the applier re-runs the §2.2 commands (listed under "Verification of this note") and corrects any moved line before applying; a changed meaning returns to the coordinator.

### 2.1 Packet header: lines 4, 5 and 8

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:4-5`):

> **Date:** 2026-09-21 (DRAFT — **the three decisions in §0.5 were ruled by the operator on 2026-09-21 (all recommended options)**; becomes FROZEN when S4 has merged and the anchors are re-taken at the S4 merge head)
> **Status:** not dispatchable yet. Predecessor: **S4 accepted and merged** (joint N2/Part B green on Linux, `PART_A_READY` reached, the coordinator's acceptance entry in the ledger). Branch `claude/s5-part-a` off the S4 merge head; push; no PR until the coordinator says so.

**PROPOSED.** Line 4 is kept as history. Insert after it:

> **Re-anchored (RC-6), `<acceptance date>`:** the §0 anchors are re-read at `<release head>` (drafted at the candidate `875ecf29`; S4 merged at `228447c`, and `ops/c1_rail/qualification/` is unchanged between the two). The execution-slices plan carries the §3.4(d) text, so S5 builds terminal IN_DOUBT only (§3). Folded in: #519's findings and the three `/v7` profile pitfalls (§0.1); the `/v7` N2 value (§0.5); the Stage 1c measurement seam with SR-1..SR-9 and P-1..P-7 (§1a); and the SR-7 exception at the four tolerance sites (lines 8, 35, 49 and 61 of the pre-re-anchor packet). Source: the operator's CP-1a ruling (execution-slices ledger, 2026-09-27). This line neither freezes nor dispatches the packet. That follows only the operator's hold-release entry (CP-1b), and the anchors are re-verified at the head that entry names.

In line 5, replace "Predecessor: **S4 accepted and merged** (joint N2/Part B green on Linux, `PART_A_READY` reached, the coordinator's acceptance entry in the ledger). Branch `claude/s5-part-a` off the S4 merge head;" with:

> Predecessor: **S4 accepted and merged** (met: ledger "Coordinator checkpoint C2 close — S4 ACCEPTED, 2026-09-25"; merged at `228447c`). Branch `claude/s5-part-a` off the release head named in the CP-1b hold-release entry;

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:8`), tolerance site 1 of 4:

> **Authority:** the files in §2. Engine edits are limited to necessary store-free integration; **a numerical behavior discrepancy returns to the coordinator before any accepted formula changes**; no tolerance relaxed; no allowance/ceiling change; no S6+ work; no activation; no self-acceptance. A `DONE` status supplies no permission.

**PROPOSED** replacement of line 8:

> **Authority:** the files in §2. Engine edits are limited to necessary store-free integration; **a numerical behavior discrepancy returns to the coordinator before any accepted formula changes**; no tolerance relaxed, with one scoped exception (SR-7, §1a): the SR-1 measurement override only, never a route value, a contract value or a statistic; no allowance/ceiling change beyond the ruled `/v7` TEST_ONLY diagnostic values (§0.5: N2 360 s CPU / 900 s wall by the operator's CP-1a decision (3); a `/v7`-gated PART_A constant only if the coordinator's application entry under the approved rule requires it, and cited by that entry); no S6+ work; no activation; no self-acceptance. A `DONE` status supplies no permission.

**Required by:** SR-7 (CP-1a (6); r2 §7.4 SR-7, "The exception covers the SR-1 measurement override only; it is never a route value, a contract value or a statistic"); CP-1a (3); r2 §13 step 5 ("It lands with the S5 build, and the RC-6 packet gains the pointer"). Without the ceiling clause, line 8's "no allowance/ceiling change" would forbid the `/v7` profile edits that #519's pitfalls require (§2.2 P1–P3).

### 2.2 New §0.1: re-anchor, #519's findings and the `/v7` pitfalls

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:10-16`):

> ## 0. Rule 0 reads (Phase 0 — report anchors in §7; line numbers pinned at the S4 merge head)
> - The engine, read before any edit: `qualification/part_a.py` (`_run_part_a` — the sampling/append loop, its request/provider/proof inputs, the pilot addresses, outer panel seeds, path addresses and source-occurrence order), `regime.py`, `provider.py`, `replay.py`, the adjudicators (`adjudication.py`, `result_adjudication.py` — the exact-Decimal side), `benchmark_part_a.py`; `execution/compute.py` (`run_n1_compute`, S4's `run_n2_compute`, `stage_request`, `_ReplayProvider`, `_run_stage`, `initial_state`).
> - S4's generalized checkpoint route (every `{'N1','N2'}` closed set becomes `{'N1','N2','PART_A'}` — list each site in §7): `derive_checkpoint_plan`, `build_checkpoint_evidence` + parsers, `_checkpoint_projection`, `parse_checkpoint_snapshot`, work-phase sets (`PART_A`, `PART_A_CAPTURE`, `PART_A_G5` already exist in `campaign_budget.PHASES`), `g5.validate_campaign_checkpoint`, `campaign_protocol`, `campaign_funding` roles, `campaign_supervisor` role branches, `worker.main`, `release_schema`/`profile`.
> - Custody: S4's widened tables already admit `checkpoint='PART_A'` (S4-D1) — **no layout change in S5**; the family's checkpoint-keyed field sets gain the PART_A set (§1).
> - Budget: `part_a_initial_paths` / `part_a_expanded_paths` in the frozen budget binding (the fixture's 4 / 8) — reduced TEST_ONLY depths, to be reported distinctly from reference-depth qualification.
> - Harness: `test_campaign_n2_linux.py` helpers; the selector (S4's placement rule: before the S2 OOM case); subset iteration; `s2_run_evidence.py --expect-head`.
> - Repo constraints: no module-level mutable state (frozen-adjudicator walk); line 3 on committed bytes only.

**PROPOSED.** In line 14, after "(the fixture's 4 / 8)", insert "(`tests/ops/qualification/composition_fixture.py:242`; on this fixture Part A never expands, §0.1 F1)". Then insert a new section after line 16, before "## 0.5.":

> ## 0.1 Re-anchor at the release head (RC-6)
>
> Anchors below are at `875ecf29` and are re-verified at `<release head>`. Paths are under `ops/c1_rail/qualification/` unless stated.
>
> | §0 read | Anchor |
> |---|---|
> | `_run_part_a` | `part_a.py:127`; pilot `:178-186` (prediction `:184`, refusal `:185-186`); `within_pp` field `:32`, validated `:46`, read only at `:208` |
> | Existing request mapping | `production.py:89-96` (`_part_a_request`; `within_pp = float(part.expansion_tolerance)` at `:96`) |
> | `regime.py` | `domain_seed` `:10` |
> | `provider.py` | `_ReplayProvider` `:12` (imported by `execution/compute.py:4`) |
> | `execution/compute.py` | `initial_state` `:8`, `stage_request` `:14`, compute-start `verify_for` `:28`, `run_n1_compute` `:47`, `run_n2_compute` `:52` |
> | `runner.py` | `_run_stage` `:88` |
> | Adjudicators | `adjudication.py`; `result_adjudication.py` panel-count refusal `:418-420` |
> | Checkpoint route | `derive_checkpoint_plan` `checkpoint_plan.py:84`; `build_checkpoint_evidence` `evidence.py:877`; `_checkpoint_projection` `journal_snapshot.py:144`; the packet's `parse_checkpoint_snapshot` is **`parse_campaign_checkpoint_snapshot`**, `journal_snapshot.py:475`; `PHASES` `execution/campaign_budget.py:12-13`; `validate_campaign_checkpoint` `execution/g5.py:493`; roles `execution/campaign_protocol.py:92-94`; role branches `execution/campaign_supervisor.py:1520-1530`, UID map `:2553-2554` |
> | Worker | `run_worker` `execution/worker.py:25`; TEST_ONLY refusal `:37-38`; compute dispatch `:69-70`; result encode/validate/frame `:73-94`; `main`'s frame write and fsync `:143-150`; `PhaseBudgetGuard` `:156` |
> | Budget | `diagnostic_budget_profile` `execution/profile.py:215`; binding Σ check `execution/campaign_store.py:2776-2783` (memory term `:2781`) |
> | Harness | `scripts/qualification_boundary_verification.py` `S4_CASES` `:40`; `scripts/s2_run_evidence.py` `ACCEPTANCE_SCOPES` `:72`; workflow `mode` options `.github/workflows/qualification-s2-supervision.yml:26` |
>
> **Findings carried from #519** (its §0, re-verified by r2 §2 and re-read here):
> - **F1 — the (2, 4, 2) fixture can never expand.** The contract pins expansion to `abs(p5 − 0.95) ≤ 0.01` for every domain (`contract.py:761-773`; `Decimal("0.01")` at `:767`). The TEST_ONLY workload is `QualificationWorkloadPolicy(counts,5,5,6,2,4,2)` with PART_A depth 2 and `initial_panels=2, expanded_panels=4, paths_per_population_per_panel=2` (`tests/ops/qualification/composition_fixture.py:195`, `:236`, `:241`). A panel's rate is 0, 0.5 or 1, never within 0.01 of 0.95; the smallest expanding depth is 17 (16/17 ≈ 0.941). No genuine S5 campaign on this fixture takes the expansion branch, whatever the synthetic source. So the required-expansion case stands on the arithmetic boundary test (§4), and maximum expansion is reached only by the coordinator's Stage 1c measurement through §1a.
> - **F2 — no existing measurement covers maximum expansion.** `benchmark_part_a.py:1` measures "One representative synthetic Part A workload, never a qualification panel batch"; the 2026-09-24 harness runs the signed route, which never expands (F1).
> - **F3 — `verify_for` dominates.** It runs on every replay (`production_source.py:861-867`), in every panel proof (`:894`) and once at compute start (`execution/compute.py:28`): 1.02–1.16 s CPU per call on Windows.
> - **F4 — the pilot predicate.** The engine predicts `probe + max_panels × (rebuild + depth × path)` and refuses before any panel when that exceeds `budget_seconds` (`part_a.py:178-186`), even when no expansion follows. Under the service's CPU-rate quota the PART_A ceiling must cover it (PA-2b). It is validated at C3 from the SR-8 export's `probe_seconds` and `predicted_seconds` (§1a).
> - **F5 — no host factor is evidenced.** None is applied.
>
> **The three `/v7` profile pitfalls in `diagnostic_budget_profile`, and the fixture-cap tuple** (#519 §0 "Build pitfalls"; each missed edit fails differently):
> - **P1 — refused outright.** Any schema outside v3–v6 raises `fresh diagnostic execution profile required` (`execution/profile.py:219-226`). `parse_profile` (`:116`, per-schema fields from `:138`) must define `/v7` first.
> - **P2 — unfunded if only the accept tuple is extended.** The funded branch lists v4–v6 only (`:243-252`, `funding_intents` at `:250`). A `/v7` added only at `:219-226` gets `qualification_campaign_budget_profile/v2` with no `funding_intents`.
> - **P3 — N2 falls back to 120 s if the N2 branch is missed.** The N2 widening applies only when the schema is v6 (`:239`). Missed for `/v7`, N2 gets the shared 120 s CPU (`_DIAGNOSTIC_PHASE`, `:209`), below its measured 211 s: the silent-SIGKILL failure checkpoint C2 found. `/v7`'s value is 360 s CPU / 900 s wall (`_JOINT_N2_DIAGNOSTIC_PHASE`, `:211`), by the operator's CP-1a decision (3) (§0.5).
> - **P4 — the fixture cap.** `tests/integration/qualification_boundary/fixture_producer.py:152-156` raises the TEST_ONLY cap to 10,000 s CPU / 10,000 s wall / `memory_limit` only for releases v3–v6. A `/v7` release otherwise binds 120 s / 180 s / `memory_limit*9//10` and is `BUDGET_EXHAUSTED` at binding, on CPU, wall and memory (`execution/campaign_store.py:2776-2783`).

**Required by:** RC-6's own wording ("including #519's findings that the (2, 4, 2) fixture cannot expand and the three `/v7` profile pitfalls"); #519's RC-6 row, "re-read §0 at the release head. Fold in: §0 finding 1 …, both §0 pitfalls, and the §6 pointer" (`R1M:486`). The §6 pointer is §0.5's PART_A clause and line 8's ceiling clause.

### 2.3 Rule 0 reads: the corrected function name

Folded into §0.1's table (`parse_campaign_checkpoint_snapshot`, `journal_snapshot.py:475`). Current line 12 names `parse_checkpoint_snapshot`, which does not exist at `875ecf29` (`grep -rn "def parse_checkpoint_snapshot" ops/`: no hit). **PROPOSED:** in line 12, replace `parse_checkpoint_snapshot` with `parse_campaign_checkpoint_snapshot`. **Required by:** RC-6's re-read of the anchors (S5 draft RC-6, "The S5 packet's anchors are re-read at the head where release is proposed").

### 2.4 §0.5 S5-D3: `/v7` build notes and the N2 value

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:24`):

> **S5-D3 — Release/profile.** One new literal `qualification_execution_release/v7` + profile `/v7` with `supported_checkpoints = dispatch_checkpoints = ['N1','N2','PART_A']` (all three compute checkpoints; the result/seal route is still not enabled — that flag is T06/S8's, added with T05's integration); v6 stays exactly `['N1','N2']`; fresh attempts only. Snapshot `/v8` = `/v7` with the PART_A checkpoint entry (prefix digests, panel counts, expansion decision); budget-profile v3 pairs v5–v8. *Alternative rejected:* enabling finalization in the same literal (would let an S5 attempt claim a route that does not exist yet).

**PROPOSED.** Line 24 stays as ruled. Insert after it:

> **S5-D3 build notes (RC-6; not a change to the ruled decision).** `/v7` needs all three `diagnostic_budget_profile` edits and the fixture-cap tuple (§0.1 P1–P4). The `/v7` N2 compute phase takes **360 s CPU / 900 s wall**: the operator's CP-1a decision (3) (2026-09-27) extends the M13 values from `/v6` to the **`/v7` TEST_ONLY diagnostic profile only**. No N2 production value follows, and the margin rule does not apply to N2. Every other `/v7` phase keeps the shared 120 s CPU / 300 s wall, unless the coordinator's PART_A application entry under the approved measurement-and-margin rule sets a `/v7`-gated PART_A constant (r2 §13 step 5); that constant cites the entry.

**Required by:** CP-1a (3): "The M13 values, **360 s CPU / 900 s wall**, are extended from `/v6` to the **`/v7` TEST_ONLY diagnostic profile only**. … No N2 production value follows, and the margin rule does not apply to N2" (`baa09ffd:…:968`); #519 pitfall P3; r2 §13 step 5.

### 2.5 §1 Interfaces and the new §1a seam (SR-1..SR-9, P-1..P-7)

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:27`):

> - `compute.run_part_a_compute(contract, source, budget, *, n2_full_outcomes)` — adapts the existing `_run_part_a` loop and its request/provider/proof inputs; preserves the disjoint pilot addresses, outer panel seeds, path addresses and source-occurrence order including legitimate duplicates; returns the initial-prefix document and the final document as separate byte strings from one computation.

**PROPOSED** replacement of line 27:

> - `compute.run_part_a_compute(contract, source, budget, *, n2_full_outcomes, measurement_override=None)` — adapts the existing `_run_part_a` loop and its request/provider/proof inputs; preserves the disjoint pilot addresses, outer panel seeds, path addresses and source-occurrence order including legitimate duplicates; returns the initial-prefix document and the final document as separate byte strings from one computation. `measurement_override` is the §1a TEST_ONLY measurement seam (SR-1, SR-2); the route never passes it (P-3).

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:32`):

> - **Checkpoint C3** (before the first acceptance-grade Linux run): the PART_A field sets, the `/v8` snapshot diff, the two-artifact capture contract and its crash semantics, the baseline-transport contract, the float-vs-Decimal parity results on the supported frozen boundary configurations, and the E-case ownership for E04/E05 and the PART_A halves of E06/E08/E09.

**PROPOSED.** In line 32, before its final full stop, append: "; and the §1a conformance table (SR-1..SR-9 met, with the node IDs of P-1..P-7)".

**PROPOSED** new section after line 32, before "## 2. Files":

> ## 1a. Stage 1c measurement seam (approved by the operator at CP-1a, decision (6), 2026-09-27)
>
> The coordinator's Stage 1c measurement must reach maximum expansion through this build's own Part A worker body (r2 §7, §12.4). This section is how. It is TEST_ONLY and exists for that measurement only.
>
> **The seam** (r2 §7.3). The parameter is the Part A request's `within_pp`, read at one decision point only (`part_a.py:208`). The forced value is exactly `1.0`. It is injected only as the keyword-only `measurement_override=None` of the built adapter (or its accepted successor), whose value is an instance of the frozen type `PartAMeasurementOverride(within_pp=1.0)` with the fixed label `TEST_ONLY_MEASUREMENT_FORCED_EXPANSION`. The adapter first builds the request from the frozen contract exactly as in the route. Only if an override is present and the gate passes does it apply `dataclasses.replace(request, within_pp=override.within_pp)`; `SyntheticPartARequest.__post_init__` re-validates. The gate, applied before any source verification, compute or file write: `contract.trust_domain.authority_class == 'TEST_ONLY'`, `contract.trust_domain.permits_synthetic is True`, and the contract's `evidence_class = TEST_ONLY`. The gate admits the signed TEST_ONLY route too, so the exclusion of every signed route rests on P-3, P-4 and P-5.
>
> **S5 build requirements.** SR-1..SR-7 are r2 §7.4 verbatim (section numbers in the rows are r2's; "packet" means this packet at its pre-re-anchor line numbers). SR-8 carries the CP-1a extension, and SR-9 is r2 §16 C2 as adopted.
>
> | ID | Requirement |
> |---|---|
> | SR-1 | The override type and the adapter keyword of §7.3, in `execution/compute.py` (already in the packet's §2 file list). No `part_a.py` change is needed |
> | SR-2 | The gate of §7.3, applied before `verify_for`, before any compute and before any write |
> | SR-3 | The PART_A worker body after bundle and plan verification is one store-free callable that `run_worker` itself calls. It covers the parse of the staged N2 capture bytes, the N2 FULL derivation (S5-D2), the adapter compute, and both S5-D1 artifact writes with their fsync. Stage 1c calls **that** callable, never a harness copy, and `run_worker` calls it without an override |
> | SR-4 | The S5-D1 writer (prefix written and fsynced before the expansion decision; final written and fsynced after) is the same function in the route and in Stage 1c. It writes to a directory argument |
> | SR-5 | A producer of **genuine staged N2 capture bytes** for the TEST_ONLY composition, generated by S4's own N2 compute and capture code, not a hand-written vector, and bound to the contract the harness uses. The adapter's own "mismatched N2 FULL baseline" tests (packet §3) need the same input |
> | SR-6 | The worker's own `PhaseBudgetGuard` (`worker.py:156-200`) is constructable with measurement limits (`cpu_ns = wall_ns = 3600 s`, `memory_bytes` above the runner's memory). The per-replay budget checks then run production code, and the pilot predicate cannot abort. The limits are inputs, not a seam |
> | SR-7 | The RC-6 re-anchored packet states an explicit, scoped exception at each of its four tolerance sites: the Authority line "no tolerance relaxed" (packet line 8), §2 Forbidden "accepted formulas and tolerances" (line 35), §3 "never a relaxed tolerance" (line 49) and §6 Forbidden "a relaxed tolerance" (line 61). The exception covers the SR-1 measurement override only; it is never a route value, a contract value or a statistic |
> | SR-8 | (Stage 2, carried from r1 `:216`.) S5's run evidence exports the PART_A settled observation fields: `cpu_ns`, `memory_peak_bytes`, `oom_events`, the boottime from reservation to `CAPTURED`, and the payload/guardian CPU split where available, **and the PART_A result's `probe_seconds` and `predicted_seconds`** (CP-1a decision (1), 2026-09-27: the pilot-budget term is validated at C3 from Stage 2 through this export, and becomes final only when that check is recorded). They are read by `scripts/s2_run_evidence.py <run> --expect-head <sha>` |
> | SR-9 | The packet's rejection of an omitted or unnecessary expansion (§3) runs in G5 reconstruction (the route P-5 relies on) or after the SR-3 callable returns, never inside it. A refusal of the forced Stage 1c run is classified by its cause: a conforming build refused under a packet rule is **BLOCKED**; a non-conforming build (the rejection, or a re-derivation of the expansion decision from the contract, inside the SR-3 callable) is a **C3 nonconformance** returned to the S5 executor; a refusal traced to neither is **INVALID** and investigated (r2 §16 C2; #519 proposal round 2, F1a) |
>
> **Proof obligations** (S5 tests; node IDs named at C3). P-1..P-7 are r2 §7.5 verbatim:
>
> | ID | Obligation |
> |---|---|
> | P-1 | **Refused under production authority.** An OPERATOR-domain contract, or any contract failing the §7.3 gate, together with an override raises before `verify_for` is called (spy) and before any file exists in the output directory. P-1 is defence in depth only: it does not exclude the signed TEST_ONLY route (§7.3) |
> | P-2 | **Closed value.** `PartAMeasurementOverride(within_pp=x)` is refused for every `x ≠ 1.0` |
> | P-3 | **Unreachable from the route (static and spy; with P-4 and P-5, the sole signed-route exclusion proof).** An AST test asserts that under `ops/` only `execution/compute.py` defines or tests the override, and that `worker.py`, `service.py`, `campaign_supervisor.py`, `g5.py` and `campaign_protocol.py` never construct it. A spy test asserts that `run_worker`'s PART_A path calls the SR-3 callable with `measurement_override=None` |
> | P-4 | **Absent from signed documents.** The closed key sets of the `/v7` release and profile, the campaign plan, the checkpoint plan and the `/v8` snapshot are pinned, and each parser refuses a document with an added `measurement_override` or `within_pp` key |
> | P-5 | **Not adjudicable.** On (2, 4, 2), a forced-expanded result is refused by the PART_A G5 reconstruction as "unnecessary expansion" (packet §3). The existing result adjudicator already refuses a panel count that differs from the frozen expansion decision (`result_adjudication.py:417-420`). An escaped forced artifact therefore cannot yield `CONTINUE` |
> | P-6 | **Faithful.** With the override, the initial-prefix artifact is byte-identical to the one produced without it, on the same fixture |
> | P-7 | **Same code.** Stage 1c's entry point is the SR-3 callable object that `run_worker` uses (identity asserted in the harness record) |
>
> **At Checkpoint C3.** **P-3, P-4 and P-5 are hard, non-waivable C3 preconditions:** nothing else proves that no signed route reaches the seam. A missing SR or a failing P at C3 is a **C3 nonconformance returned to the S5 executor** under this packet. Stage 1c does not run until it is fixed, and the PART_A ceiling stays provisional meanwhile (r2 §16 C3).
>
> **Named worker-side residual, carried by PA-5** (r2 §7.6 and §16 C4). In the current worker shape these stay outside the SR-3 callable: the result encode, validate and frame (`execution/worker.py:73-94`); `main`'s frame write and fsync (`:143-150`); and the bundle verification and plan derivation that `run_worker` performs before the SR-3 body. Stage 1c does not measure them. The Stage 2 service figure includes them at the prescribed size, so PA-5's k carries them. Stage 1c ends the provisional status with this residual named (CP-1a decision (2)(e)).
>
> **The Stage 1c harness is not this packet's file.** It sits on the coordinator's measurement branch based on the S5 head (r2 §12.4), and the executor writes none of it.

**Required by:**
- CP-1a (6), whose approved items are "the r2 §7 seam, with S5 build requirements **SR-1..SR-9** (SR-9 as adopted, r2 §16 C2);", "proof obligations **P-1..P-7**;" and "the SR-7 exception at the packet's four tolerance sites (lines 8, 35, 49 and 61)." (`baa09ffd:…:981-983`), and "**P-3, P-4 and P-5 are hard, non-waivable C3 preconditions.** After the RC-6 fold-in, a missing SR or a failing P at C3 is a C3 nonconformance returned to the S5 executor." (`:985`);
- CP-1a (1): "It is validated at C3 from Stage 2, through SR-8's export extended with the PART_A result's `probe_seconds` and `predicted_seconds`" (`baa09ffd:…:950`); recommendation (1)(b)(i) in r2 §14.1;
- CP-1a (2)(e): "Stage 1c ends the provisional status with the worker-side residual (r2 §16 C4) named and carried by PA-5" (`baa09ffd:…:964`);
- the coordinator's adoption of C2 (SR-9) and C3 (ledger, `875ecf29:…full-e1-execution-slices.md:916-917`).

The seam paragraph restates r2 §7.3 without change. The worker-side residual list joins r2 §7.6's residual (bundle verification and plan derivation) and C4's named items.

### 2.6 §2 Files: tolerance site 2 of 4, and file scope

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:35`):

> `execution/{compute.py, worker.py, evidence.py, g5.py, service.py, campaign_store.py, campaign_supervisor.py, campaign_funding.py, campaign_protocol.py, release_schema.py, profile.py, release.py}`; `qualification/{checkpoint_plan.py, evidence.py, journal_snapshot.py}`; `qualification/part_a.py` **only** for store-free integration seams (report every line); installed fixtures; tests: new `tests/ops/qualification/execution/test_campaign_part_a.py`, extensions to `test_campaign_n2.py`, `test_campaign_recovery.py`, `test_worker.py`, `test_release.py`, `test_profile.py`, `test_journal_snapshot.py`, `tests/ops/qualification/{test_part_a.py, test_regime.py, test_evidence_reconstruction.py, test_result_adjudication.py}`; new Linux file `tests/integration/qualification_boundary/test_campaign_part_a_linux.py` registered per S4's placement rule. **Forbidden:** T05's modules and tests; `qualification/seal.py`; accepted formulas and tolerances; any S2/S3/S4 Linux assertion.

**PROPOSED.** Replace the last sentence ("**Forbidden:** T05's modules and tests; `qualification/seal.py`; accepted formulas and tolerances; any S2/S3/S4 Linux assertion.") with:

> **Forbidden:** T05's modules and tests; `qualification/seal.py`; accepted formulas and tolerances (one scoped exception, SR-7: the §1a SR-1 measurement override only, never a route value, a contract value or a statistic); any S2/S3/S4 Linux assertion; the coordinator's Stage 1c harness (§1a).

**D-5 (file scope for the S5 acceptance scope and the SR-8 read).** Before "; new Linux file", insert: "`scripts/qualification_boundary_verification.py` (the S5 selector and case set, under S4's placement rule) and `scripts/s2_run_evidence.py` (the S5 acceptance scope and the SR-8 export read); `.github/workflows/qualification-s2-supervision.yml` (an S5 value for its `mode` input) only under the operator's CI-configuration approval". Reason: SR-8 says the fields "are read by `scripts/s2_run_evidence.py`", but that script reads JUnit totals and file-set scope only (`scripts/s2_run_evidence.py:72`, `ACCEPTANCE_SCOPES = ("S4_JOINT_N2", "S3_N1_CAPTURE", "S2_DIAGNOSTIC_SUPERVISION")`), and the workflow's `mode` offers only `s2|s3|s4` (`.github/workflows/qualification-s2-supervision.yml:26`). r2 §12.5 already marks "the S5 scope S5 registers" as UNVERIFIED because S5 adds it. None of these files is in the §2 list. S4 met the same gap as its C2 decision 1, "Selector and scope" (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s4-joint-n2-part-b-DRAFT.md:78`). The workflow part is **OQ-4**.

### 2.7 §3 Behavior: SR-9 placement, terminal IN_DOUBT, tolerance site 3 of 4

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:38`):

> After the joint PASS receipt (`PART_A_READY`), one Part A operation produces the initial panels and, exactly when prescribed, the appended panels `[initial_panels, expanded_panels)`; the final prefix is byte-identical to the initial; conditional expansion uses inclusive tolerance equality; the final floor and the FULL sanity comparison apply after required expansion. Reject omitted or unnecessary expansion, a substituted or reordered prefix, altered source occurrences, a missing pilot identity, and a mismatched N2 FULL baseline. Interruption during expansion cannot relaunch; remaining-budget exhaustion blocks completion without inventing a statistical failure. Required assertions from the slice, verbatim in the adapter/capture test:

**PROPOSED.** In line 38:
- after "Reject omitted or unnecessary expansion" insert " (where SR-9 places the check)";
- after "remaining-budget exhaustion blocks completion without inventing a statistical failure." insert: "S5 builds terminal IN_DOUBT only (execution-slices plan, S5 Behavior, with the §3.4(d) text); bounded same-sample re-execution is the separate D3 slice after S5 and before S8."

**Required by:** SR-9 (CP-1a (6)); RC-6, "with the §3.4(d) text in place, so S5 builds terminal IN_DOUBT only" (S5 draft `:387`); D3 in the ruling's words, "Implement bounded same-sample recovery in a separate slice after S5 and before S8" (ledger `:807`).

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:49`), tolerance site 3:

> - [ ] Float compute vs exact-Decimal G5 on the supported frozen boundary configurations — a disagreement is an engine-contract conflict returned to the coordinator, never a relaxed tolerance.

**PROPOSED** replacement of line 49:

> - [ ] Float compute vs exact-Decimal G5 on the supported frozen boundary configurations — a disagreement is an engine-contract conflict returned to the coordinator, never a relaxed tolerance (one scoped exception, SR-7: the §1a SR-1 measurement override only, never a route value, a contract value or a statistic).

### 2.8 §4 Verification: the impossible prescribed-expansion case

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:54-55`):

> - Linux: subset iteration first, then acceptance-grade: the full S4 file set **plus** the Part A file. Required: genuine Part A without expansion → `FULL_PASS_READY`; with prescribed expansion (if a synthetic source can produce it economically; otherwise the arithmetic boundary test stands separately and is **not** called a full-route witness — disclose); a genuine below-floor or above-FULL failure → `PART_A_FAILED`; crash during expansion → IN_DOUBT with the initial prefix retained; g5 death + exact retry. Actual synthetic market/session sources for the Linux campaigns.
> - Return: heads, record IDs with counts, run IDs with record hashes, the `/v7` release/profile digests, the initial/final prefix identities per Linux campaign, the parity results, and the reduced TEST_ONLY depths stated distinctly.

**PROPOSED** replacement of line 54:

> - Linux: subset iteration first, then acceptance-grade: the full S4 file set **plus** the Part A file. Required: genuine Part A without expansion → `FULL_PASS_READY`; prescribed expansion cannot occur on the (2, 4, 2) fixture (§0.1 F1), so the required-expansion case stands on the arithmetic boundary test, which is **not** called a full-route witness (disclose); a genuine below-floor or above-FULL failure → `PART_A_FAILED`; crash during expansion → IN_DOUBT with the initial prefix retained; g5 death + exact retry. Actual synthetic market/session sources for the Linux campaigns. Maximum expansion through this build is exercised only by the coordinator's Stage 1c measurement (§1a), a TEST_ONLY measurement and never a route witness (P-5).

**PROPOSED.** In line 55, before its final full stop, append: "; the §1a conformance table (SR-1..SR-9, P-1..P-7 node IDs) and the SR-8 export fields, `probe_seconds` and `predicted_seconds` included".

**D-6 (the Linux crash case on a non-expanding fixture).** Line 54's "crash during expansion" has no Linux instance on this fixture either, because no genuine campaign expands (F1). The S5-D1 window that does exist is between the fsync of the initial-prefix artifact and the final artifact. Optional wording: replace "crash during expansion → IN_DOUBT with the initial prefix retained" with "crash after the initial-prefix artifact is fsynced and before the final artifact → IN_DOUBT with the initial prefix retained (on this fixture no appended panel exists; the during-expansion interruption stands on the pure boundary test)". This is the drafter's reading of F1's consequence; #519 and r2 name only the prescribed-expansion case.

### 2.9 §5 Checkpoint C3

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:58`):

> Push and return: head + `git diff --stat <S4 merge head>...HEAD`; the line-1 record; the §1 freeze as a table; the fixture ledger; fail-on-base; the parity results; anything S5-D1–D3 did not anticipate. Wait for GO.

**PROPOSED** replacement of line 58:

> Push and return: head + `git diff --stat <release head>...HEAD`; the line-1 record; the §1 freeze as a table; the §1a conformance table, with the P-1..P-7 node IDs; the fixture ledger; fail-on-base; the parity results; anything S5-D1–D3 did not anticipate. **P-3, P-4 and P-5 are hard, non-waivable C3 preconditions; a missing SR or a failing P is a C3 nonconformance returned to the executor (§1a).** The coordinator's C3 also takes RC-3b: Stage 1c through the SR-3 callable, only after the coordinator's recorded read of the `--stage 1c` harness diff; the executed `bind_budget` Σ-feasibility check on the built `/v7`; and Stage 2/PA-5 from the SR-8 export, with the named worker-side residual. The full RC-2 owner-text set is applied at C3 (execution-slices ledger, direction of 2026-09-27). Wait for GO.

**Required by:** CP-1a (6) (`baa09ffd:…:985`); CP-1a (2)(e) and (f) (`:964-965`); the ledger direction's C3 row (`875ecf29:…full-e1-execution-slices.md:852`). `<S4 merge head>` becomes `<release head>` because the branch now starts there (§2.1).

### 2.10 §6 Forbidden: tolerance site 4 of 4

**Current** (`875ecf29:docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md:61`):

> A second replay to reconstruct the prefix; a panel resume, replacement pilot or checkpoint rerun after interruption; a relaxed tolerance or a worker/G5 disagreement tolerated; a baseline passed as an unobserved number; changing an accepted formula without the coordinator's ruling; enabling the result/seal route in the v7 literal; writing any progression name outside F3; module-level mutable state; `git stash`; commits without `git diff --stat`; pushing while a Linux run is in flight; claiming acceptance.

**PROPOSED.** Replace "a relaxed tolerance or a worker/G5 disagreement tolerated;" with:

> a relaxed tolerance (one scoped exception, SR-7: the §1a SR-1 measurement override only, never a route value, a contract value or a statistic) or a worker/G5 disagreement tolerated; any route path that constructs or passes the override, or a signed-document key for it (P-3, P-4);

**Required by:** SR-7 (CP-1a (6)); P-3 and P-4 restated as forbidden moves.

---

## 3. Checkpoint C3: the RC-2 owner-text set

**Required by, for every passage here:** S5 draft RC-2, "Corrected owner text is accepted by the operator and applied to each named owner: boundary spec §3.1; full-E1 spec §2.2a, §2.4, §2.5, §2.6 (the two table rows and the new paragraph) and §5; slices plan contract decisions 3 and 6 and the S5 text; umbrella §0.8 O-10 if the operator chooses that optional landing place. Each cites the qualified tag `AUDIT-2026-09-25-qualification-assurance-contract-delta#<row>`" (`875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:383`); the ledger direction's C3 row, "The full RC-2 owner-text set accepted and applied" (`875ecf29:…full-e1-execution-slices.md:852`); ledger 2026-09-26, "RC-2 requires them accepted by the operator and applied" (`:813`). **Gate: C3**, for every passage in this section.

The D1–D3 directions are ruled in the operator's words. The rest of the draft's direction text "is the draft's recommendation, not ruling text; its owner-text form is reviewed under RC-2" (ledger `:804`). Accepting a passage below adopts that owner text.

### 3.1 Boundary spec §3.1: the boundary set and OF-1..OF-7

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md:81-99`); §3 has no subsection today:

> Service code/config are administrator-owned and not writable by qclient or worker.
> qg5 uses a distinct OS identity and protected code/key path. qexec's access to the
> Docker daemon makes it part of the privileged trusted computing base. No general
> Docker operation is exposed through its RPC interface. Docker documents why
> daemon control must be limited to trusted users:
> [Docker Engine security](https://docs.docker.com/engine/security/).
>
> The supervisor and G5 run from administrator-installed, immutable code and locked
> virtual environments whose exact manifests are approved in the release. The
> worker runs in the pinned container image. G5 is a one-shot protected entry point
> invoked by the operator/service manager under qg5; it accepts only an attempt ID
> and reads its configured service socket. The initial slice does not give qclient
> an arbitrary command runner or the ability to assume qg5's identity. The Linux
> test administrator invokes this same entry point under the real qg5 UID.
>
> Alternative rejected for this slice: a same-user subprocess with a private Python
> token. The caller could still modify its code/state or reach its credentials.
> A remote managed execution service could implement the same protocol later but
> adds infrastructure not needed for the first Linux boundary test.

**PROPOSED** (S5 draft §1.5(a), verbatim; the draft's insertion point is after line 86 and before line 88):

> > "### 3.1 Boundary set (AUDIT-2026-09-25-qualification-assurance-contract-delta#boundary)
> > The requesting agent must be unable to: (B-1) alter installed execution, adjudication or worker code for an admitted release; (B-2) replace or edit captured evidence or the journal; (B-3) produce a counted attempt nobody sees, choose which attempt counts, or learn seed values before reveal; (B-4) grant itself activation authority; (B-5) present fixture or TEST_ONLY output as production evidence. Each retained mechanism cites the row it enforces. These rows rest on credentials and host permissions, not process roles: `qexec` is root-equivalent through Docker, and any agent-reachable administrator, `sudo`, Docker-socket, `qexec`, `qg5`, `qseal`, signing or deploy credential defeats them. These operational facts are production acceptance obligations: (OF-1) no account or environment in which an agent session runs, the operator's workstation account included, can use administrator, `sudo`, `docker`-group or Docker-socket access on the production qualification host; (OF-2) no agent can authenticate as `qexec`, `qg5`, `qseal` or the administrator, and no polkit rule grants `manage-units` to an agent-reachable UID; (OF-3) execution, result, seal and operator-VOID private keys are unreadable by agent-reachable UIDs and absent from every worktree, every CI secret visible to an agent-editable workflow and every store an agent can reach; (OF-4) key-enrollment and trust-domain inputs are writable only by the operator; (OF-5) no agent holds rail-host deploy credentials, write access to the rail `/data` volume, or broker credentials; (OF-6) if E3 is adopted, the operator GO signing key is off-host and never loaded where an agent runs; (OF-7) before public reveal, the seed salt is readable only by the trusted administrator, `qexec`, the worker's read-only input and `qg5`'s private adjudication access. Each is verified by attended host read at provisioning, before any production-authority release, and after any access change; OF-5 also before any arm and at each session GO, OF-6 at TB-I3, and OF-7 also before F1 admission. Until a row's facts are verified and recorded, the row is reported as enforcement not established; that is not a finding that the row is breached. The disposable CI harness is evidence of mechanism, never of this boundary."

**D-3 (placement).** Insert the new `### 3.1` at the **end** of §3, after line 99 and before "## 4.", not between lines 86 and 88. Reason: at the draft's point, the heading would pull the rest of §3 (lines 88-99, the installation paragraph and the rejected alternative) under "3.1 Boundary set". The text is unchanged either way.

**D-4 (assignment pointer).** Append to the §3.1 text: "The owner, gate, record location and re-verification triggers of each attended read are the execution-slices ledger's RC-5 assignment entry (2026-09-27)." Reason: the RC-5 entry names this section as the OF definitions' owner ("The OF definitions' owner is boundary spec §3.1 once RC-2 applies S5 draft §1.5(a)", ledger `:893`), and the two records should point at each other.

**Consistency with the RC-5 assignment (checked, no change needed).** The §1.5(a) gate sentence ("Each is verified by attended host read at provisioning, before any production-authority release, and after any access change; OF-5 also before any arm and at each session GO, OF-6 at TB-I3, and OF-7 also before F1 admission") matches the stricter Q12 reading the coordinator recorded (ledger `:881`). S5 draft §6 Q12 is therefore resolved by the RC-5 entry, not by this text.

### 3.2 Full-E1 spec §2.2a: the client plan view

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:84`):

> FULL_E1 defines versioned authenticated plan-chunk retrieval with a canonical configured maximum of 1 MiB raw bytes per response, within the resolved RPC frame limit after base64/JSON encoding. Requests bind attempt, object digest, offset and length. Validate exact integer types (reject bool), nonnegative offset below object length, and positive length no greater than the chunk limit. The last chunk clips at EOF. Responses bind digest, offset, total length, actual chunk length and canonical base64 bytes. Every fetch verifies attempt/object membership and role access; arbitrary digest access is forbidden. Clients verify ordered offsets, total length and the reassembled SHA256. Identical reads recover identical bytes after restart. Read-only historical access after VOID does not authorize any new execution or publication.

**PROPOSED** (S5 draft §1.5(d), verbatim). After "Clients verify ordered offsets, total length and the reassembled SHA256." insert:

> > "For production-class campaigns (`tb-s2-rng-v3`), the plan object served to the client is a client view: the canonical plan with each seed value replaced by its digest. The admission receipt binds the client view's own digest and byte length beside the canonical plan's, and the client verifies the reassembled client view against them. Before the campaign is irrevocably closed to further computation and recovery, no chunk served to the client carries a seed value or the salt (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3). `qexec` retains the canonical plan, and G5 reads it through its checkpoint access."

**D-7 (receipt field names).** In that text, after "binds the client view's own digest and byte length", insert "(`client_view_sha256`, `client_view_byte_length`)". Reason: the RC-4 F1 admission check, condition 3, names those fields (ledger `:900`), and the RC-4 entry says the slice "depends on the full-E1 spec §2.2a amendment of S5 draft §1.5(d), applied under RC-2 at Checkpoint C3" (`:895`).

### 3.3 Full-E1 spec §2.4, first paragraph: K3 seed custody

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:113`):

> Reuse `runner._run_stage`, provider/replay/source admission, `regime.domain_seed`, seed identities, and pure `adjudicate_replay_outcomes`/`adjudicate_panel_inventory`. Extract store-free adapters where necessary; do not call `run_production_e1`, `_execute_e1` or construct `ProductionExecutor` for protected work.

**PROPOSED** (S5 draft §1.5(c), verbatim, placed at the end of this paragraph; the draft anchors it after the paragraph's first sentence, "Reuse `runner._run_stage`, … `adjudicate_panel_inventory`.", and either placement leaves the meaning unchanged):

> > "Production-class campaigns use the salted recipe `tb-s2-rng-v3`, which is `tb-s2-rng-v2` with the service-generated attempt salt added (AUDIT-2026-09-25-qualification-assurance-contract-delta#K3). The F1 freeze carries `root_rng_namespace`, the recipe and this custody rule, and no salt or salt hash. The salt and the consumed attempt are durably bound before any preview-capable work. An identical re-submission or a recovery reuses them and never generates new ones; an admission interrupted after that binding leaves the attempt closed IN_DOUBT (§2.6). The worker receives the salt in its read-only input, where it receives `root_rng_namespace` today, and derives its own seeds. G5 re-derives plans and seeds for each checkpoint it adjudicates from the salt it reads through its authorized private access, after checking the salt against the admission commitment. The client plan view carries seed digests, not seed values (§2.2a), and the salt is disclosed to the client only after the campaign is irrevocably closed to further computation and recovery. TEST_ONLY synthetic campaigns may keep `v2`."

**D-8 (the admission-crash consequence in full).** In that text, replace "an admission interrupted after that binding leaves the attempt closed IN_DOUBT (§2.6)" with: "an admission interrupted after that binding and before the ADMISSION work's capture consumes and closes the attempt: recovery makes the running ADMISSION work IN_DOUBT and the campaign terminal, the attempt identity, salt and commitment are retained, admission does not continue (a second ADMISSION reservation is refused, and ADMISSION is never re-execution-eligible), and no other salt or attempt is generated (operator ruling 2026-09-26; §2.6)". Reason: S5 draft §1.4's drafting note, "The proposed owner texts §1.5(b) and (c) state this consequence in short form; the RC-2 review should check that the applied text states it in full" (`875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:125`). The ruling's words: "Joshua explicitly accepts that an admission crash after salt binding but before capture consumes and closes the attempt, preserving its identity and salt without continuing admission or generating another" (ledger `:808`).

**Unchanged by CP-1a (5).** The accepted slice "K3/RC-4 — service salt and client plan view" moves K3's build out of TB-F1 (`baa09ffd:…:978`). §1.5(c) names no build slice or gate, so it needs no change for that.

### 3.4 Full-E1 spec §2.4, last paragraph: no panel resume

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:125`):

> Part A remains one dispatched compute operation using the existing append loop. This release does not promise partial-panel resume: interruption before a complete durable capture makes that operation IN_DOUBT. This preserves no-redraw behavior without redesigning the statistical engine.

**PROPOSED** (S5 draft §3.4(c), verbatim). After "…makes that operation IN_DOUBT." insert:

> §2.6's bounded re-execution reruns the whole checkpoint from its first panel under the same plan; it never resumes panels.

Plus **D-1**: `(AUDIT-2026-09-25-qualification-assurance-contract-delta#N2)`.

### 3.5 Full-E1 spec §2.5, last paragraph: exhaustion and retained receipts

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:137`):

> The profile defines phase reservation ceilings including verification/finalization, once in a canonical versioned configuration. Admission validates that a feasible route fits the frozen cap; inability to reserve a later phase aborts without draws. Reservations allocate the original allowance and never increase it. Check remaining budget before and immediately at dispatch, assessment commit, full-result commit and seal publication. Deadline reached means no new authority even if computation already passed. Diagnostic cleanup and read-only historical receipt retrieval may continue on separately bounded host resources; they cannot compute, authenticate or sign replacement qualification evidence.

**PROPOSED** (S5 draft §2.5(b), verbatim). After "Deadline reached means no new authority even if computation already passed." insert:

> > "A stage assessment committed before exhaustion remains evidence and is never revoked. Exhaustion ends all further work, and no result or seal is committed after it. A result or seal receipt committed before a later exhaustion is retained as history and cannot be sealed or used for activation; a settlement overrun of the committing work ends authority from the state its commit produced. A committed statistical FAIL is never recast as incomplete. A retained receipt is history: every consumer that grants new action (reservation, dispatch, result commit, seal, activation) checks the campaign's current authority and validity at use and refuses after exhaustion, revocation or VOID. Statistical accounting records committed evidence, a statistical FAIL included, whatever the later authority state; recording it grants no authority."

Plus **D-1**: `(AUDIT-2026-09-25-qualification-assurance-contract-delta#N1)`. S5 draft §6 Q1 (whether a committed FAIL on an exhausted campaign counts as FALSIFIED under ADR §4) stays with the statistical owner; this text records the FAIL and grants nothing, and does not answer Q1.

### 3.6 Full-E1 spec §2.6: bounded same-sample re-execution

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:147`, `:153`, `:155`):

> | START_INTENT or RUNNING, no complete durable capture | Persist IN_DOUBT before cleanup; stop owned worker; never relaunch this checkpoint |
>
> | VOID, terminal abort, IN_DOUBT or BUDGET_UNCERTAIN | Historical inspection and owned cleanup only; no continuation or sealing |
>
> A merely readable spool file is not a complete durable capture. Recovery requires the accepted N1 capture finalization protocol and content membership; absence of required facts leaves uncertainty. Cleanup failure cannot undo IN_DOUBT or make historical APIs unavailable. No new attempt ID may be allocated automatically to evade exhausted budget or uncertain dispatch; a separately authorized new campaign is outside retry semantics.

**PROPOSED** (S5 draft §3.4(a), verbatim):
- Row "START_INTENT or RUNNING, no complete durable capture" (line 147): replace its recovery cell with the text at S5 draft line 318:

> > "Persist IN_DOUBT before cleanup; stop owned worker. Never relaunch, except one bounded same-sample re-execution under the rule below."

- Row "VOID, terminal abort, IN_DOUBT or BUDGET_UNCERTAIN" (line 153): replace its first cell with the text at S5 draft line 322 (the recovery cell is unchanged):

> > "VOID, terminal abort, IN_DOUBT (except a work that is re-execution-eligible under the bounded same-sample rule below) or BUDGET_UNCERTAIN"

- After the paragraph ending "…outside retry semantics." (line 155), add the paragraph at S5 draft line 326:

> > "**Bounded same-sample re-execution (AUDIT-2026-09-25-qualification-assurance-contract-delta#N2).** A compute checkpoint (N1, N2 or PART_A) left IN_DOUBT by process interruption on the same boot, with no finalized capture, may be re-executed once, and at most twice per campaign. The service may do so only after the original worker is terminated, its absence is proven and its IN_DOUBT state is durable. The re-execution uses byte-identical sample, source, runtime and configuration identities and the same installed phase limits, under the campaign's original deadline and allowance, charged on top of the interrupted work's charge. The interrupted work, and any failed re-execution, stay in history. Retained complete records must match the re-execution on the fields named by the checkpoint's predeclared comparison schema, which also lists the excluded runtime-observation fields. With none retained, re-execution requires recorded reproducibility evidence meeting the standard set for the campaign's authority class; otherwise the work stays IN_DOUBT. A mismatch is a terminal reproducibility incident, never a result. Captured work, committed assessments (a statistical FAIL included), overruns, BUDGET_UNCERTAIN and VOID are never eligible. No re-execution allocates an attempt, salt, seed or plan, and the salt is not disclosed to the client while a re-execution remains possible."

**D-9 (sequencing clause).** Append to the new paragraph: "This rule is built by the separate recovery slice after S5 and before S8 (operator ruling 2026-09-26, D3). Until that slice is accepted, no release performs a re-execution and every IN_DOUBT stays terminal." Reason: applied at C3, the paragraph would be normative spec text while the S5 build under acceptance implements only terminal IN_DOUBT (§1.2). S5 draft §3.1 states that "That change must not ride inside S5"; the spec should say so where the rule is written.

Open items this text relies on and does not answer (S5 draft §6): Q2 (R4's "original deadline" read as the campaign's; the paragraph says "under the campaign's original deadline"); Q7 (R7's production evidence standard, "the standard set for the campaign's authority class"); Q9 (when a never-retried, retry-eligible IN_DOUBT counts as closed for reveal). See §5.

### 3.7 Full-E1 spec §5: forbidden moves

**Current** (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:198`):

> - Turn interrupted execution into statistical FAIL, redraw under the same attempt, reset an allowance, or allocate a fresh attempt automatically.

**PROPOSED** (S5 draft §3.4(b), verbatim). After "redraw under the same attempt" insert:

> (a §2.6 bounded same-sample re-execution is not a redraw)

Plus **D-1**: `(AUDIT-2026-09-25-qualification-assurance-contract-delta#N2)` at the end of the bullet.

### 3.8 Slices plan, contract decision 3: per-work bound and the rule's scope

**Current** (`875ecf29:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md:88`):

> 3. **Reservations cover the rest of the route.** Canonical installed configuration names admission, checkpoint/source proof/probe, capture/attestation, each G5 assessment, aggregate validation/commit and sealing/finalization ceilings. Validate feasibility against the frozen cap, including prescribed maximum expansion. Actual CPU counters settle reservations once; unknown usage consumes its full reservation. Remaining wall time includes queues and downtime. Memory is an enforced shared concurrent footprint, not independent full-size allowances per process.

**PROPOSED** (S5 draft §2.5(a), verbatim). After "…not independent full-size allowances per process." append:

> > "In this design the cumulative bound is per work and kernel-enforced: payload quota × guardian `RuntimeMaxUSec` plus the guardian's `LimitCPU` never exceeds that work's reservation, and settled charges plus open reservations never exceed the frozen cap (AUDIT-2026-09-25-qualification-assurance-contract-delta#N1). A campaign-level rate quota is not a substitute. Every phase, PART_A, RESULT and SEAL included, reserves its installed phase ceiling; PART_A's is measured at maximum expansion. No per-phase CPU figure enters a statistical decision. The operator fixes a measurement-and-margin rule (the measurement standard and the margin) by ruling. The coordinator may set TEST_ONLY diagnostic ceilings only by applying that rule (a cited measurement, the rule's margin, a ledger entry); anything outside it needs an operator ruling. Production ceilings and caps are frozen with F1 by their owners and are never set under that rule."

**D-10 (the approved rule's scope and the `/v7` N2 value).** Append: "The approved rule's scope is PART_A only, TEST_ONLY (operator rulings 2026-09-26 and 2026-09-27; CP-1a 2026-09-27). Every other TEST_ONLY diagnostic phase ceiling comes from an operator ruling: `/v7`'s N2 compute phase takes 360 s CPU / 900 s wall, the M13 values extended by CP-1a decision (3) to the `/v7` TEST_ONLY diagnostic profile only." Reason: §2.5(a) was drafted before any rule existed ("The operator fixes a measurement-and-margin rule … by ruling"). Since then the rule's scope was ruled PART_A-only (ledger `:869`), and N2's `/v7` value came from a separate ruling, CP-1a (3). This is the one owner text in the RC-2 set where the `/v7` N2 value is needed, because contract decision 3 is where TEST_ONLY ceilings are said to come only from the rule or a ruling.

### 3.9 Slices plan, contract decision 6 and the S5 text

Applied at build entry as the §3.4(d) text (§1.1, §1.2). RC-2 needs no further text for them; at C3 the check is that they are present. If the operator accepts D-2's bridging note, the C3 application removes it, because the spec §2.6 text then exists (§3.6).

**OQ-3 (§5)** asks whether SR-7's scoped exception should also reach the tolerance and threshold sentences in these RC-2 owners. Optional wording is given there.

### 3.10 S5 draft §2.3: the D2 falsifier read with the three-way split

**Current** (`875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:228`); r2 §10.3 names this text as the falsifier's owner:

> **Falsifier:** revisit the uniform model if PART_A's maximum-expansion CPU cannot be bounded ahead of time. That would mean a ceiling covering maximum expansion either fails the Σ-feasibility check against any admissible cap or cannot be measured before S5 is released.

**PROPOSED** wording for S5 draft §2.3, appended after line 228 (the falsifier sentence itself is kept):

> **Reading (operator, CP-1a decision (4), 2026-09-27: the three-way split).** Three outcomes are kept apart:
> - (i) **A Σ failure from a valid record is the D2 ACCOUNTING-DESIGN FALSIFIER stop.** A valid record means PA-4 validity and complete memory. The failure is Σ-feasibility failing at every admissible value, from the proposed-value arithmetic at build entry; at Checkpoint C3 the same test is the executed `bind_budget` on the built `/v7` (r2 §10.3). It returns the accounting-design question: revisit the uniform model.
> - (ii) **Missing permission, or a run not executed, never engages the falsifier.** It keeps the hold, because CP-1b needs RC-3a.
> - (iii) **An invalid measurement is investigated**, and re-measured only under a fresh approval.
> - (iv) The accounting-design question also returns if a diagnosis traces an invalid run to the workload itself.
>
> Memory evidence that stays incomplete after the allowed re-run is neither the falsifier nor a PA-3 failure: it leaves RC-3a unmet, and build entry then needs an operator ruling (r2 §8.3). This reading supersedes r2 §10.3's release-point reading. **Still open for the operator, when it arises:** whether a PART_A ceiling set by ruling, without a measurement, answers the "cannot be measured before S5 is released" limb.

**Required by:** CP-1a (4), "D2 timing: the three-way split" (`baa09ffd:…:970-976`), each item quoted from that commit:
- "(i) A Σ failure from a valid record is the D2 ACCOUNTING-DESIGN FALSIFIER stop (r2 §10.3)."
- "(ii) Missing permission, or a run not executed, never engages the falsifier. It keeps the hold, because CP-1b needs RC-3a."
- "(iii) An invalid measurement is investigated and re-measured only under a fresh approval."
- "(iv) The accounting-design question also returns if a diagnosis traces an invalid run to the workload itself."
- "No S5 draft §2.3 owner text changes here; that is RC-2, at C3."

The memory sentence restates r2 §8.3 and §12.7, which CP-1a (1) did not change. Item (v) is only noted (**OQ-1**).

**Owner note.** The S5 draft is in `docs/notes/`, and S5 draft RC-2's owner list does not name it. r2 §10.3 names it as the falsifier's owner ("owner: S5 draft §2.3"), and CP-1a (4) puts its text change under RC-2. This note therefore treats it as part of the RC-2 set.

### 3.11 RC-2 evidence at C3

S5 draft RC-2's evidence is "the delta's §10 hook no longer prints `UNROUTED` for the boundary, K3, N1 or N2". At `875ecf29` the hook's loop, restricted to those four rows, prints `UNROUTED` for boundary, N1 and N2, and **not** for K3. The ledger's RC-4 entry already carries the tag `AUDIT-2026-09-25-qualification-assurance-contract-delta#K3` (`875ecf29:…full-e1-execution-slices.md:897`), and the hook searches `docs/superpowers`. So the K3 line cannot show that §1.5(c)/(d) were applied. The C3 check should also read each named owner directly:

```bash
T=AUDIT-2026-09-25-qualification-assurance-contract-delta
grep -n "### 3.1 Boundary set" docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md
grep -c "$T#K3" docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md        # §2.2a and §2.4 (K3)
grep -c "$T#N1" docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md        # §2.5, with D-1
grep -c "$T#N2" docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md        # §2.4 last, §2.6, §5
grep -n "bounded same-sample re-execution is not a draw" docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
grep -n "$T#N1" docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md          # contract decision 3
```

---

## 4. Checklist: every item mapped to its proposed text

| # | Item (task) | Proposed text | Gate |
|---|---|---|---|
| 1 | §3.4(d) text: S5 draft §4 and its consistency correction | §1 (what it is), §1.1 contract decision 6, §1.2 S5 Behavior, §1.3 D-1/D-2 | Build entry |
| 2 | RC-6 re-anchor at a candidate release head, re-verified at the actual one | §2 header, §2.1 (re-anchor line), §2.2 re-verification rule | Build entry |
| 2a | #519's findings, including that (2, 4, 2) cannot expand | §2.2 new §0.1 F1–F5; §2.8 line 54 | Build entry |
| 2b | The three `/v7` profile pitfalls | §2.2 new §0.1 P1–P3 (and P4, the fixture cap); §2.4 | Build entry |
| 2c | SR-1..SR-9 (SR-9 via r2 §16 C2) and P-1..P-7 | §2.5 new §1a | Build entry |
| 2d | SR-7 exception at lines 8, 35, 49 and 61 | §2.1 (line 8), §2.6 (line 35), §2.7 (line 49), §2.10 (line 61) | Build entry |
| 2e | P-3/P-4/P-5 hard, non-waivable C3 preconditions | §2.5 (§1a "At Checkpoint C3"), §2.9 (line 58) | Build entry text; binds at C3 |
| 2f | Missing SR or failing P at C3 = C3 nonconformance to the S5 executor (r2 §16 C3) | §2.5 (§1a), §2.9 | Build entry text; binds at C3 |
| 2g | Worker-side residual (`worker.py:73-94`, `:143-150`), carried by PA-5 | §2.5 (§1a "Named worker-side residual") | Build entry text; binds at C3 |
| 2h | SR-8 extended with `probe_seconds` and `predicted_seconds` (CP-1a (1)) | §2.5 (§1a SR-8 row), §2.8 (line 55) | Build entry text; binds at C3 |
| 3a | Boundary spec §3.1 | §3.1 (with D-3, D-4) | C3 |
| 3b | Full-E1 spec §2.2a | §3.2 (with D-7) | C3 |
| 3c | Full-E1 spec §2.4 | §3.3 (first paragraph, with D-8), §3.4 (last paragraph) | C3 |
| 3d | Full-E1 spec §2.5 | §3.5 | C3 |
| 3e | Full-E1 spec §2.6 (two rows and the new paragraph) | §3.6 (with D-9) | C3 |
| 3f | Full-E1 spec §5 | §3.7 | C3 |
| 3g | Slices plan contract decision 3 | §3.8 (with D-10) | C3 |
| 3h | Slices plan contract decision 6 and the S5 text | §1.1, §1.2 (applied at build entry); §3.9 | Build entry, checked at C3 |
| 3i | CP-1a D2 reading (three-way split) as proposed S5 draft §2.3 wording | §3.10 | C3 |
| 3j | `/v7` N2 value (360 s CPU / 900 s wall, TEST_ONLY diagnostic profile only) where an owner text needs it | §2.1 (line 8), §2.4 (packet §0.5), §3.8 (D-10) | Build entry (packet); C3 (plan) |
| — | Umbrella §0.8 O-10 (optional landing place in S5 draft RC-2) | Not drafted; **OQ-5** | C3, if chosen |

---

## 5. Open questions only the operator can answer (not decided here)

- **OQ-1 — CP-1a decision (4)(v).** Whether a PART_A ceiling set by ruling, without a measurement, answers the falsifier's measurement limb. CP-1a leaves it "for the operator, when it arises" (`baa09ffd:…:976`). §3.10 only notes it.
- **OQ-2 — the §3.4(d) text before the spec §2.6 text exists.** Applied at build entry, the two insertions cite a spec §2.6 rule that lands only at C3 (§1.3). Options: (a) apply them verbatim and accept the forward reference until C3; (b) apply them with D-2's bridging note, removed at C3; (c) apply the §2.6 paragraph (§3.6) at build entry as well. Option (c) moves one RC-2 text from C3 to build entry, which the 2026-09-27 direction does not provide for.
- **OQ-3 — SR-7's reach beyond the packet.** CP-1a (6) approves the exception "at the packet's four tolerance sites". Four sentences in RC-2 owners carry the same kind of wording, and the seam's request-level `within_pp = 1.0` could be read against them:
  - slices plan Global constraints, "All depths, thresholds, namespaces and budgets come from the frozen contract, not copied constants." (`875ecf29:…full-e1-execution-slices.md:17`);
  - slices plan S5, "never relax a tolerance or let worker/G5 disagree" (`:238`);
  - full-E1 spec §2.4, "All depths, thresholds, namespaces and budgets come from the frozen contract, not copied constants." (`875ecf29:docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md:121`) and "do not silently change a threshold" (`:123`);
  - full-E1 spec §5, "adjust expansion thresholds to make synthetic acceptance pass" (`:200`).

  Either (a) they are read as binding route and contract values, which the seam never is (P-3, P-4) and which a forced result can never pass (P-5), so no text is needed; or (b) each gets the same scoped exception. Optional wording for (b), appended to each: "(Scoped exception: the TEST_ONLY Stage 1c measurement override of the S5 packet §1a, SR-1/SR-7, never a route value, a contract value or a statistic; operator CP-1a decision (6), 2026-09-27.)"
- **OQ-4 — the CI-configuration part of S5's file scope.** Whether the S5 executor may add an S5 value to the `mode` input of `.github/workflows/qualification-s2-supervision.yml`, a CI-configuration change, as S4 did for `s4` (§2.6, D-5). The script edits are a coordinator scope matter; the workflow edit needs the operator's approval under the handoff set's common rules.
- **OQ-5 — the optional umbrella O-10.** S5 draft RC-2 includes "umbrella §0.8 O-10 if the operator chooses that optional landing place". If chosen, its drafted gate cell "**TB-F1**" (`875ecf29:docs/notes/2026-09-26-s5-decision-draft.md:138`) conflicts with CP-1a (5), which moves K3 out of TB-F1 into the K3/RC-4 slice. The row would need that cell changed. Not drafted here.
- **OQ-6 — S5 draft §6 items the RC-2 texts rely on without answering.**
  - Q2: confirm R4's "original deadline" is the campaign's (§3.6's paragraph assumes it);
  - Q7: R7's production evidence standard, "owed by the operator with the statistical owner";
  - Q9: when a retry-eligible IN_DOUBT that is never retried counts as closed, and so when the salt is revealed;
  - Q1: whether a committed FAIL on an exhausted campaign counts under ADR §4 (statistical owner; §3.5).

## 6. Drafter's additions, each accepted or struck on its own

| ID | Where | What | Why |
|---|---|---|---|
| D-1 | §1.1, §3.4, §3.5, §3.7 | Append the qualified tag (`#N2`, `#N1`) where the S5 draft's text has none | S5 draft RC-2: "Each cites the qualified tag" |
| D-2 | §1.3 | Bridging note on the build-entry §3.4(d) insertions | Forward reference to C3 text (OQ-2) |
| D-3 | §3.1 | Place boundary spec §3.1 at the end of §3 | The draft's point would re-parent §3's last two paragraphs |
| D-4 | §3.1 | Pointer from §3.1 to the ledger's RC-5 entry | The RC-5 entry points here |
| D-5 | §2.6 | S5 file scope: selector, evidence reader, workflow `mode` (the last under OQ-4) | SR-8 needs a reader that does not exist; S4 precedent |
| D-6 | §2.8 | Linux crash case reworded for a non-expanding fixture | Consequence of F1 |
| D-7 | §3.2 | Receipt field names in §2.2a | Matches the RC-4 admission check, condition 3 |
| D-8 | §3.3 | Admission-crash consequence stated in full | S5 draft §1.4 drafting note |
| D-9 | §3.6 | Sequencing clause in the spec §2.6 paragraph | D3 is a separate slice after S5 |
| D-10 | §3.8 | Rule scope and `/v7` N2 value in contract decision 3 | Rulings of 2026-09-26/27 and CP-1a (3) |

Everything else marked PROPOSED is S5 draft or r2 text as the rulings adopted it, or a restatement of a ruling.

---

## Verification of this note

Commands run in this worktree at `875ecf29` (read-only, except creating this note):

```bash
git fetch origin; git rev-parse origin/main                              # 875ecf297ddda6e12af12e4e69f117deca8008c3
git diff --stat 521d8f2 HEAD -- ops tests tools deploy scripts .github   # empty
git diff --stat 228447c HEAD -- ops/c1_rail/qualification                # empty
git diff origin/main baa09ffd                                             # the CP-1a ruling (PR #523): ledger, r2 §14.1 banner, STATE, H1 row, CP-1a row
git show 61a2ca41:docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md | sed -n 143,197p   # the frozen dispatch record
git show baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md | sed -n 936,1004p
sed -n 1,160p docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
sed -n 785,935p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
cat -n docs/briefs/handoffs/2026-09-21-full-e1-s5-part-a-DRAFT.md
# S5 draft, r2 and #519 read in full or by section: §0-§6 and 1-461; r2 1-1147; R1M 1-60, 255-290
awk 'NR>=54 && NR<=100' docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md
awk 'NR>=78 && NR<=202' docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md
sed -n 205,255p ops/c1_rail/qualification/execution/profile.py
sed -n 150,157p tests/integration/qualification_boundary/fixture_producer.py
sed -n 761,774p ops/c1_rail/qualification/contract.py; grep -n 'Decimal("0.01")' ops/c1_rail/qualification/contract.py
sed -n '195p;236p;241p;242p' tests/ops/qualification/composition_fixture.py
sed -n 89,97p ops/c1_rail/qualification/production.py
grep -n "within_pp" ops/c1_rail/qualification/part_a.py; sed -n 176,190p ops/c1_rail/qualification/part_a.py
grep -n "def run_worker\|authority_class != 'TEST_ONLY'\|N1_ONLY release forbids\|compute = \|run = compute(\|encode_worker_result(context\|return frame\|destination = Path\|_os.fsync\|class PhaseBudgetGuard" ops/c1_rail/qualification/execution/worker.py
sed -n 414,421p ops/c1_rail/qualification/result_adjudication.py; sed -n 2774,2784p ops/c1_rail/qualification/execution/campaign_store.py
grep -n "^def _run_part_a\|^def initial_state\|^def stage_request\|^def run_n1_compute\|^def run_n2_compute\|^def _run_stage\|^def domain_seed" ops/c1_rail/qualification/{part_a,runner,regime}.py ops/c1_rail/qualification/execution/compute.py
grep -n "class _ReplayProvider" ops/c1_rail/qualification/provider.py; grep -rn "def parse_checkpoint_snapshot" ops/   # none
grep -n "^def derive_checkpoint_plan\|^def build_checkpoint_evidence\|^def _checkpoint_projection\|^def parse_campaign_checkpoint_snapshot\|^def validate_campaign_checkpoint" ops/c1_rail/qualification/{checkpoint_plan,evidence,journal_snapshot}.py ops/c1_rail/qualification/execution/g5.py
grep -rn "run_part_a_compute\|PartAMeasurementOverride\|measurement_override" ops/ tests/                               # none
grep -n "S4_CASES\s*=" scripts/qualification_boundary_verification.py; grep -n "ACCEPTANCE_SCOPES\s*=" scripts/s2_run_evidence.py; grep -n "options:" .github/workflows/qualification-s2-supervision.yml
grep -n "probe_seconds\|predicted" ops/c1_rail/qualification/part_a.py
for row in boundary K3 N1 N2; do grep -rlwF "AUDIT-2026-09-25-qualification-assurance-contract-delta#$row" docs/superpowers docs/adr docs/briefs || echo "UNROUTED: $row"; done   # UNROUTED: boundary, N1, N2; K3 found in the ledger
sed -n 17p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md; sed -n 238p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md
```

Every blockquote under **Current** was inserted by a scratch script (not committed) from the worktree files, and each quoted run of lines was then compared line for line with its source (81 quoted lines, 0 mismatches). `git diff --quiet 875ecf29 -- docs/` confirmed those files identical to `875ecf29` before the note was written. The ruled and ledger phrases quoted inline (39 strings: CP-1a items from `git show baa09ffd:docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md`, the dispatch record from `git show 61a2ca41:docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md`, and the `main` ledger, S5 draft, r1 and r2) were each checked as exact substrings of their source: 0 not found. The link check (`bad 0`) and the gate run are recorded in the PR.

## Limitations

- **Candidate head only.** Every anchor is at `875ecf29`. The release head is not known until CP-1b, and the §2 re-verification rule applies there.
- **The CP-1a ruling is not on `main`.** It is cited at `baa09ffd` (PR #523). If that PR changes before it merges, the citations here need re-checking.
- **No code, test, measurement or host was run or read beyond the cited lines.** The SR/P set states requirements for code that does not exist; names other than `measurement_override` and `PartAMeasurementOverride` are not fixed until the S5 build (r2 §15).
- **SR-1..SR-7 and P-1..P-7 are quoted verbatim from r2.** Their cross-references are r2's section numbers and the packet's pre-re-anchor lines, as §1a's lead-in says. They are not renumbered.
- **The drafter's additions D-1..D-10 are this note's own proposals.** None is required by a ruling in so many words. Each is separable.
- **Not covered:** umbrella §0.8 O-10 (OQ-5); the checklist addendum's S8/T06 sequencing record for the RC-4 slice, which CP-1a (5) assigns to the addendum; the H1 step (b) harness directory, which another worker owns.
