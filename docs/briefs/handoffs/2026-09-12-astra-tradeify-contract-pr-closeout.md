# Coordinator handoff — Tradeify contract and PR closeout

**Status:** Draft for dispatch. This document has not launched an agent.
**Repository:** `Joshua-Asante/first-passage`
**Primary checkout:** `C:\Users\joshu\multi_firm_operations`
**Integration owner:** the receiving Astra coordinator.
**Objective:** Close the remaining specification and review gaps around the Tradeify portfolio, deliver the five existing PRs to verified merge readiness, and leave dependency-complete implementation packets. Do not begin portfolio implementation or qualification as a continuation of this assignment.

## 1. Operator direction and scope

Joshua has retired Claude/Fable from the Tradeify deployment campaign. Astra now owns coordination, specifications, implementation planning, review integration and evidence assessment. Preserve prior work and historical authorship; eliminate Claude/Fable as an active dependency, including `fable-judge` requirements in the affected campaign packets.

When dispatched, this handoff covers source investigation, contract drafting/correction, the code and tests already within #363/#365, necessary regression fixtures, ownership/status reconciliation, and preparing/updating the relevant PRs and their review responses. Prefer continuing existing PRs after securing their branches. A new coordinator PR should own shared governance changes and TB-S1; avoid replacement PRs that duplicate existing work without a concrete reason.

Joshua retains substantive trading/risk rulings, ratifications, merges and operational GOs. Present concrete, source-backed recommendations before requesting a decision. Existing rulings remain effective: do not ask again for O-1 or O-5 through O-9. Resolve routine technical choices autonomously and continue independent work while a genuine decision is pending.

This assignment excludes live host operations, A7/A8 execution, provider selection or spend, qualification runs, registry admission, production rail/daemon or private-port implementation, deployment, arming, emission and orders. No agent places trades. Do not implement TB-I1/I2/I3/T1 here merely because their packets become ready.

## 2. Establish the current state first

The following is a starting inventory, not current-head acceptance evidence. GitHub metadata was refreshed on 2026-09-13 UTC / September 12 ET:

| PR | Scope | State / head at handoff authoring |
|---|---|---|
| [#360](https://github.com/Joshua-Asante/first-passage/pull/360) | TB-S3 multi-leg rail/daemon contract | OPEN · `e1583232e543daa61e0db492440bb0bd1c32292a` |
| [#361](https://github.com/Joshua-Asante/first-passage/pull/361) | TB-P2 protection-instance admission | OPEN · `6e419a30974de5b9a0d16eb1006d9a06752a4085` |
| [#362](https://github.com/Joshua-Asante/first-passage/pull/362) | TB-O1 operating procedure | OPEN · `0e68cc05ccb8f883a56c596eaf178f8c86597926` |
| [#363](https://github.com/Joshua-Asante/first-passage/pull/363) | TB-P1 preregistration, ORB skeleton, power calculator | OPEN · `482fbf40f4ff2e2c27ec8b96724f8c68b4876130` |
| [#365](https://github.com/Joshua-Asante/first-passage/pull/365) | Test-only executable rail kernel model | OPEN · `f8e39afae6796cbea43b277fc6bd5d808c7a51e9` |

Last fetched main in the originating session: `17292651f494d22aa4418c4aae20b132e8cf5619`. Primary checkout was still `133f043`; it contained unrelated untracked settings, private ports and `tmp/`, plus the new roadmap. Do not reset or clean it.

1. Read repository instructions and run the applicable handoff-verification workflow. Inspect worktrees, local modifications, remote main, all five PR heads, CI, reviews, unresolved threads and any newer related PRs.
2. Check for concurrent writers before editing. The #363 discussion linked Claude Actions run `34732403583`; its head moved during handoff preparation. Verify whether that or another campaign-specific Claude job is active and stop that work under the retirement direction before taking ownership. Do not cancel unrelated CI or disable repository-wide automation. If stopping it is unavailable, secure a separate worktree and report the precise collision rather than racing its writes.
3. Use isolated worktrees, with `codex/` branches for new work. Preserve existing PR branch names when continuing them; historical `claude/` names do not require recreating a PR.
4. Produce a compact inventory: obligation, current owner, artifact/head, evidence, remaining gap, next action. Read full changed files and review replies: a stale PR description or unresolved thread flag alone does not establish an unfixed defect.

Credit merged #356 for ports, candidate policy/capacity code, emulator and original-export parity; #358/#364 for the frozen export menu, snapshot contract/packet and reconciled pointers; #359 for replay spec rev 3. Do not reopen #353 or #344: they closed without merge after material was folded into #354/#343. Respect #356's closed general review loop; route relevant integration gaps to their actual owners.

## 3. Mandatory source reads

Read the current versions of `CLAUDE.md`, `STATE.md`, `PIPELINES.md`, `docs/operational_rules.md` and the following owners:

- [Astra deployment roadmap](../../superpowers/plans/2026-09-12-tradeify-astra-deployment-roadmap.md), Tasks 1–2 and open-PR dispositions.
- `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md`: rulings, claim manifest, closed-body rule, wave gates and packet scopes.
- `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md`, especially the acceptance and later sizing rulings; `docs/notes/2026-09-10-tradeify-protection-selection.md`.
- `docs/notes/2026-09-12-track-b-scaling-faithfulness-read.md`; `docs/notes/2026-09-11-track-b-adapters-and-book-rules.md`; the merged replay and account-snapshot contracts.
- Full current files on #360–#363 and #365; the governing regime-robustness procedure, concept ADR, rail GO ADR and Track A plan wherever those files cite them.

Apply Rule 0 before making a risk-control claim: read production sources first. At minimum inspect `core/dd_protection.py`, `core/dd_geometry.py`, `core/firm_rules.py`, `core/lifecycle.py`, `core/mc/simulation.py`, `core/mc/preflight.py`, `ops/c1_rail/book_policy.py`, sizing host, listener, arm helper, HTTP server, ledger/telemetry, daemon protocol/adapters/emulator, and deployment image inputs. Identify private sources/inputs by approved digests when needed; do not print their bodies or account observations.

The earlier source check found `book_policy.leg_quantities` scaling rounded normal base/add independently and an empty `POLICY_REGISTRY`. Recheck before relying on either finding. Code shows implemented behavior; operator rulings define required behavior. A mismatch is implementation debt, never permission to reverse the ruling.

## 4. Execution order and ownership

You own the combined result. Organize work into these units, handling them sequentially or through bounded Astra contributors when available. Keep one writer per branch/file set; contributors do not merge. If using contributors, give each its exact base, full contract, footprint and acceptance cases, and obtain independent review of substantial changes. Do not start a second coordinator with overlapping ownership.

### A. Shared contract and ownership reconciliation — coordinator

Own the umbrella's live manifest/open-items/ownership sections, campaign-state routing, STATE, TB-S1 and cross-contract decisions. Respect the umbrella's closed-body convention: use its permitted sections or the owning spec rather than rewriting historical dispatches. Shared indexes are integrated serially or regenerated after dependencies land.

Author `docs/spec/2026-09-12-tradeify-book-protection-capacity-spec.md` as TB-S1 unless a current equivalent exists; reuse that owner if it does. Specify the ruled per-leg sizing and lifecycle behavior, account settled-close mode, carried positions, add cancellation and capacity reservation/reconciliation. Explicitly assign correction of `book_policy.py` and its tests to the later TB-I1 footprint. No production sizing edit belongs in this closeout.

Trace protection through adapter paper state → account settled-close mode → per-leg quantities → reservation → broker evidence → ledger → next-session state. Cover zero quantities, partial fills and failed/contended takeovers. Do not claim that captured-export parity discharges the seven protected/WATCH/ORB-mode exports still owed.

### B. Rail contract and executable model — #360 + #365

Treat the pair as one acceptance unit with separate PR footprints. Reuse the reference model and reproduced regressions. Findings within its represented behavior should have concrete reproductions; findings about omitted behavior or unavailable real interfaces remain valid contract findings and must receive an owner/test obligation rather than being dismissed because the model cannot express them.

Close the full behavior for uncertain entries, persist-before-send crashes, order-level reconciliation, expected protection recorded before send, missing attachment, component-wise amendments preserving trail state, queued overlapping closes, partial-close recovery, EOD, kill, feed/daemon loss and restart. Acceptance is confirmed completion or a durable block with a defined attended recovery path; HTTP acceptance is not execution evidence.

For every L-1/L-2 capability name its actual evidence producer, consumer, unsupported behavior and later verification gate. Distinguish specified interface, fake implementation, existing live route capability and unverified requirement. Read current primary route documentation where useful; do not transmit orders to discover capability. Record a capability-blocked live packet if evidence is missing.

Prepare the required R-1/R-2 ratification text and S2b amendment. Review requirements outside the model (sizing, barrier, calendars, checkpoints, arm interlock, dedupe boundaries) on their own merits. Define the same-shape harness through which TB-I3 must later pass these scenarios with real components.

### C. Admission, fingerprints and effective activation — #361

Own one complete trace: freeze → source-independent confirmation/regime evidence → admitted row → tested candidate image → account/execution seal → sole n3 → deployment GO → permitted reseal → effective running-process activation. Include failed confirmation, failed n3, account activity, expiry and code/config drift.

Resolve the complete Part A bootstrap construction, retained criteria, proposed depth deviation and its exact-value ratification. Define one byte-level fingerprint serializer/normalizer with an implementation owner, version/exclusion rules and test vectors; close the pre-admission policy-row digest cycle without hiding material changes. Specify a buildable GO-absent image and a mechanically verifiable allowed GO-artifact transition if retaining that design.

Reconcile snapshot C10's replacement-run wording with the one-attempt/no-extra-sample authority. Recommend the exact permitted disposition and obtain any necessary ruling before calling the contract accepted. Failed qualification never becomes a fresh draw through expiry or resealing. Revalidate seal, account activity and image/config identity when activation actually takes effect after restart, not only at the config-writing `--arm` invocation.

Keep proposed scope amendments visible. Do not silently ratify Part A reductions, new live behavior, or an exception to post-B7 immutability. Make all consumers use the accepted trace and annotate later implementation/evidence still owed.

### D. Statistical contract and publication checks — #363

Inspect `482fbf4` or the newer head first: earlier findings may already be fixed. Validate the additive calculator with independent exact-boundary cases, including target=alpha=0.05 at n=1 and alpha immediately below that target; reject unattainable exact power and preserve the legacy CLI/pins. Check the actual diff and tests, not only prior reported counts.

Align preregistration and ORB falsifier with the accepted #361 regime construction, workload, four final limbs and failure dispositions. Keep streams/sizes fixed before outcomes and the preregistration DRAFT until TB-F1. Verify publication checks accept valid digest notation, reject prohibited result figures and actually examine their inputs. Reproduce reported calculator outputs exactly where the contract requires them.

### E. Operating procedure and cross-contract propagation — #362 + coordinator

Verify commands against actual code and their execution environment: host versus local paths, available image files, both services' evidence capture, alert/ack joins, feed-health checks and running-instance identity. Make missing send results and accepted sends without terminal broker evidence part of startup reconciliation. Clearly mark future interlocks as TB-I3 obligations.

Resolve the regular-session timing conflict between replay's 16:30 backstop and the governing 15:55 operator check / 16:00 own-flatten obligation. Trace early closes too. Do not assume an earlier operational shutdown preserves qualified strategy behavior; prepare the exact schedule and authority needed, then update replay, rail and procedure together.

Propagate the accepted GO/reseal and effective-activation contract into the procedure and snapshot consumers. Preserve the distinctions that editing config does not restart, expiry does not deliberately disarm, and disarm does not prove flatness. Retain private historical runbook bytes and account-value redaction.

## 5. Review and convergence

Maintain one findings ledger in the coordinator PR or existing owner record: finding, producing/consuming surfaces, reproducer or concrete trace, disposition, fixing SHA, verification and remaining gate. Do not create another general governance system.

After each contract correction, recheck every affected producer, consumer, persisted state, duplicated prerequisite and acceptance case. Batch related fixes; do not repeatedly request broad review of unchanged surfaces. A review request is not acceptance, and green CI is not contract closure. Bound reviews to the changed behavior while still following newly demonstrated integration defects through to their owners.

Run relevant tests for #363/#365, documentation/link/ADR/status gates for changed records, and the repository's required check tier. Use synthetic/private-safe fixtures. Exercise both accepted and rejected cases; tests mirroring prose without demonstrating reachability do not establish implementability. Refresh CI/reviews at the exact final head before recommending merge. Follow the repository's babysit workflow for PRs you create or update; no self-merge.

A proposed merge order is #365 before or together with #360 acceptance, #361's resolved contract before final alignment of #363/#362, then coordinator routing/packet reconciliation. Derive the actual graph from changed files and references: #363's calculator repairs can proceed independently, and the two contract groups can converge without waiting for operator exports or A7. Do not require unrelated whole-PR completion where a fixed interface suffices.

## 6. Deliverables and stopping condition

Return:

1. Current main and a five-PR table: exact head, changes made/reused, tests/CI, review disposition, merge dependency and operator gate. Distinguish merge-ready, ratification-pending and actually merged.
2. One consistent TB-S1/S2/S3/P1/P2/O1/snapshot contract set, with the cross-component traces above and named owners for missing capabilities.
3. A compact consolidated operator decision packet: exact proposed text, source conflict, recommendation, consequence and blocked consumers. Include only decisions not already ruled; resolve technical questions before presenting it.
4. Updated campaign ownership and manifest, including #365 and necessary later TB-I1/I3/D2 footprints. No active Claude/Fable adjudication dependency.
5. Bounded READY/BLOCKED implementation packets for TB-I1, TB-I3 offline, TB-I2 and TB-T1, each with verified base, files, existing versus proposed interfaces, inputs, tests, private locations and stopping condition. READY requires its actual entry conditions; TB-I2 remains evidence-blocked until required parity. Do not fabricate complete implementation packets for unresolved contracts.

Success is **contract closure and verified PR readiness**, with any required ratifications explicitly outstanding or recorded by Joshua. If an external capability or substantive ruling remains missing, finish unaffected work and name the precise blocked contract; do not label the whole campaign ready. Continue through authorized fixes and review follow-up instead of returning only an inventory.

Stop before portfolio implementation, qualification or live operations. Merging any of these PRs does not itself qualify the portfolio or authorize deployment.
