# Tradeify Portfolio Deployment Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the accepted Tradeify portfolio's qualification and deployment checklist under Astra ownership, preserving the operator's decisions and operational gates.

**Architecture:** Reuse the merged adapters, emulator, candidate policy and parity harness. Make sizing, replay and the live rail obey one accepted contract, then qualify and seal that exact portfolio before requesting deployment GO. Astra owns coordination, implementation, review integration, evidence assessment and readiness recommendations; Joshua retains substantive ratifications, merges, funding, attended inputs and operational GOs.

**Tech Stack:** Python; pytest; private Pine-derived ports and TradingView exports; GitHub; Docker/Fly listener and daemon; existing Tradeify/Tradovate/CrossTrade route.

**Spec:** [Track B umbrella](https://github.com/Joshua-Asante/first-passage/blob/17292651f494d22aa4418c4aae20b132e8cf5619/docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md), the linked campaign authorities, and the operator's 2026-09-12 instruction retiring Claude from this campaign. Open specifications below remain proposals until their applicable acceptance and ratification gates clear.

## Global constraints

- Fixed K=1: Aegis 6J, Striker MYM p250, Vanguard MGC, ORB MNQ. No fifth leg, substitute book, policy grid or runner-up.
- Preserve the selected 1%/40% policy and the later O-1/O-5..O-9 rulings. Frozen historical `core/dd_protection.py` constants are not this instance's configuration surface.
- Private source, exports, account evidence and numerical qualification outputs remain in approved ignored roots. Public records carry permitted digests and verdicts.
- Compute remains single-process. Freeze streams, workloads, acceptance criteria and compute budget before decision-bearing runs.
- Claude/Fable is no longer an implementation, coordination or adjudication dependency. Historical authorship and evidence remain intact.
- No agent places trades. A7 is a separate attended, disarmed ceremony. Funding, deployment GO and each armed session retain their operator gates.
- This is a sequencing and acceptance roadmap, not a claim that the missing specifications are already implementable. Write bounded code-level packets only after their named contract issues close.

## Evidence baseline

GitHub checked on 2026-09-13 UTC / September 12 ET. Fetched `origin/main` = `17292651f494d22aa4418c4aae20b132e8cf5619`. Primary working checkout remains `133f043`; existing untracked files were preserved. Reviewed the latest 45 PR records, selected campaign discussions and review threads, current merged sources and open specification branches. No live host state was inspected and no qualification batch was run.

| Work | Verified repository state | What remains |
|---|---|---|
| [#329](https://github.com/Joshua-Asante/first-passage/pull/329), [#336](https://github.com/Joshua-Asante/first-passage/pull/336), [#342](https://github.com/Joshua-Asante/first-passage/pull/342), [#343](https://github.com/Joshua-Asante/first-passage/pull/343) | Merged: accepted configuration, Track B umbrella/release, deferred production-feed decision | Acceptance of a configuration does not establish qualification or deployment authority |
| [#332](https://github.com/Joshua-Asante/first-passage/pull/332), #339, #346–#352, [#354](https://github.com/Joshua-Asante/first-passage/pull/354), [#355](https://github.com/Joshua-Asante/first-passage/pull/355), [#357](https://github.com/Joshua-Asante/first-passage/pull/357) | Merged: M1 infrastructure, validation, recorded listener/daemon deployments and A7 preparation | A7 ceremony, A8 acceptance and acceptance-bearing image verification |
| [#353](https://github.com/Joshua-Asante/first-passage/pull/353), [#344](https://github.com/Joshua-Asante/first-passage/pull/344) | Closed without merge; useful material folded into #354 and #343 respectively | Do not reopen as missing work |
| [#356](https://github.com/Joshua-Asante/first-passage/pull/356) | Merged: four private adapter implementations, candidate policy/capacity code, emulator, parity harness; original-export parity recorded | Correct later sizing rulings; seven new export intake/parity obligations; runtime integration. Respect its closed general review loop |
| [#358](https://github.com/Joshua-Asante/first-passage/pull/358), [#364](https://github.com/Joshua-Asante/first-passage/pull/364) | Merged: reconciled inventory, ruled finite export menu, warm-up record, snapshot contract/packet, corrected menu pointers | Seven operator exports; TB-T1 implementation; remaining private inventory/provenance reconciliation |
| [#359](https://github.com/Joshua-Asante/first-passage/pull/359) | Merged replay specification rev 3 | Header remains PROPOSED; reconcile acceptance/status and cross-spec conflicts before TB-I2. No synchronized replay implementation delivered by this PR |

PR test counts and parity results above are recorded historical evidence, not tests rerun in this planning session.

## Open PR disposition

| PR / observed head | Astra's next action | Acceptance condition |
|---|---|---|
| [#360](https://github.com/Joshua-Asante/first-passage/pull/360) `e158323` — TB-S3 | Review with #365; reconcile sizing, EOD timing, deployment-GO and recovery contracts; prepare R-1/R-2 and S2b amendments for ratification | Model scenarios map to real interfaces; every external capability has a producer and evidence gate; required ratifications recorded |
| [#365](https://github.com/Joshua-Asante/first-passage/pull/365) `f8e39af` — executable kernel model | Close review against this head, preserve reproduced regressions, align #360 and the same-shape integration harness | Test-only reference accepted; no claim that fake-broker support proves live support. Latest fetched review summary was running |
| [#361](https://github.com/Joshua-Asante/first-passage/pull/361) `6e419a3` — TB-P2 | Finish admission-to-effective-arm trace and propagate accepted changes to consumers | Resolve full Part A bootstrap construction, activation-time seal validation, and canonical fingerprint algorithm; then obtain required ratifications |
| [#363](https://github.com/Joshua-Asante/first-passage/pull/363) `f442979` — TB-P1 | Verify/fix exact binomial boundary and digest-scanner findings; align with final #361 contract | Exact-equality and adjacent-unequal cases pass independently; digest syntax accepted without admitting private figures; preregistration remains draft until TB-F1 |
| [#362](https://github.com/Joshua-Asante/first-passage/pull/362) `0e68cc0` — TB-O1 | Verify latest reconciliation and deadline fixes; align final procedure with accepted #360/#361 | All commands have valid host/local contexts; missing transport records remain unresolved; both services' evidence is captured; effective activation is checked |

Review-thread flags alone are not a defect inventory: several threads contain fixes while still marked unresolved. Verify each finding against the exact head before counting it open or closed. PR descriptions also lag revisions, especially #361. These rows are dispositions, not merge approvals.

## Task 1 — Establish Astra ownership and one current checklist

**Outcome:** No remaining campaign packet depends on Claude or `fable-judge`; one manifest owns delivery state.

**Files:** existing Track B umbrella; `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md`; `STATE.md`; affected active packet ownership lines.

- [ ] On an isolated `codex/` worktree from current main, record Joshua's ownership decision and replace active Claude/Fable assignments with Astra. Preserve historical evidence and operator authority.
- [ ] Reconcile the umbrella's QUEUED/STUB rows with merged #356/#358/#359 and the five open PRs; add #365's test-only footprint and the proposed footprint amendments from #361.
- [ ] Inspect existing writers before editing their branches. #363's discussion contains a Claude job link (`34732403583`); determine whether it is still active and end any remaining campaign execution under the retirement decision before taking over its files. This session has not verified or cancelled that run.
- [ ] Classify each item as delivered, contract review, implementable, evidence-blocked or operator-gated. Remove duplicate checklists by pointing to owners.

**Acceptance:** Fresh main/PR inventory, ownership recorded, no concurrent writer on a claimed footprint, and no stale dependency on already merged work.

## Task 2 — Close the contract gaps before implementing the portfolio

**Outcome:** One consistent sizing-to-replay-to-arm contract, with proposals distinguished from operator decisions.

**Files:** new TB-S1 protection/capacity specification under `docs/spec/`; existing TB-S2 specification; #360 TB-S3; #361 TB-P2; #363 preregistration; #362 procedure; snapshot seal contract.

- [ ] Author TB-S1 from the ruled O-1/O-5..O-9 behavior and actual source. Merged `ops/c1_rail/book_policy.py::leg_quantities` still scales an already-rounded normal base and add independently. Striker must recompute the risk-scaled ladder and derive adds from executed base; Vanguard's ruled WATCH restrictions also need implementation. Do not seal the old tables.
- [ ] Trace one protection transition through private adapter paper state, account settled-close mode, quantity generation, capacity reservation, broker fill, ledger update and next-session state. Include zero-size legs, carried positions, ORB add cancellation, partial fills and rejected takeovers.
- [ ] Reconcile EOD behavior: merged TB-S2 RC-8 uses a 16:30 regular-session backstop, while #362's latest procedure stops risk-add before the governing 15:55 operator check / 16:00 own-flatten obligation. Determine the approved observable schedule and make replay, rail and procedure agree before freeze; do not silently shorten strategy trading in implementation.
- [ ] Close #361's Part A construction and exact-depth proposal, one canonical serializer/normalizer, the pre-admission policy fingerprint cycle, artifact-only GO image reseal, and effective-activation checks after restart. Propagate the final choices to #360/#362/#363 and TB-T1 consumers.
- [ ] Resolve the snapshot/no-extra-sample contract explicitly: merged seal C10 voids expired/activity-affected seals and dependent n3 results and calls for replacement evaluation; the campaign forbids extra qualification attempts. Ratify the precise replacement rule before any run, with failed qualification never becoming a retry opportunity.
- [ ] Record L-1 execution-evidence and L-2 route-capability requirements from TB-S3, including scoped atomic close/partial protection adjustment, attachment and native trailing amendment. Plan read-only capability verification early. An unsupported requirement blocks the proposed live design; it does not authorize a substitute behavior.

**Acceptance:** Concrete success, rejection, uncertain-send, restart, partial-close, expiry and failed-qualification sequences have named state owners and reachable outcomes. Joshua receives only the remaining substantive decisions after Astra has resolved technical inconsistencies.

## Task 3 — Complete independent preparation and M1

**Outcome:** Advance source-independent work while awaiting operator evidence.

**Files:** `scripts/seal_account_snapshot.py`, `tests/test_seal_account_snapshot.py`; Track A plan and `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md`; `M1_MONITORING_ACCEPTANCE.json`; TB-C1 calendar/overlay artifacts named in the umbrella.

- [ ] Build TB-T1 from the merged packet, after verifying its field contract. Test all C1–C10 refusals, timestamp ordering, distinct evidence, zero absolute adjustments, output/evidence collisions, ignored output and public-safe stdout. The tool can be built before a fresh account snapshot exists.
- [ ] Complete TB-C1 forward calendar and closure overlay against the proposed horizon, verifying current primary sources when doing that work; preserve frozen D19 and require the named venue attestation.
- [ ] Complete A9-PREP's provider-neutral source contract and mocked tests. Keep provider selection and spend at the existing post-TB-E1 checkpoint.
- [ ] Joshua supplies OP-1: five Striker Account Size multipliers (0.40, 0.50, 0.20, 0.25, 0.10), plus one-contract ORB normal and adds-off exports with both margins at zero. Each requires its exact-state Inputs and Properties screenshots. Follow the [frozen menu](https://github.com/Joshua-Asante/first-passage/blob/17292651f494d22aa4418c4aae20b132e8cf5619/docs/notes/2026-09-12-track-b-scaling-faithfulness-read.md); no extra Aegis/Vanguard exports are currently owed.
- [ ] Execute A7 in its attended session at/after the recorded Sunday September 13 reopening, following the frozen injection window and teardown. A7 preparation is not A7 evidence.
- [ ] Complete A8: genuine event evidence and operator signoff, validator success, merged acceptance record and verified deployed image carrying matching RESOLVED evidence; perform the documented re-bake if pins require it.

**Acceptance:** Tool/calendars/source contract have their own evidence; A7/A8 complete only from actual ceremony and deployed-artifact evidence. No feed or portfolio readiness inferred from M1 alone.

## Task 4 — Deliver the source-faithful offline portfolio

**Outcome:** Replay and runtime implementation obey the corrected, accepted rules.

**Files:** `ops/c1_rail/book_policy.py`, `core/firm_rules.py`, `core/lifecycle.py`, `ops/c1_rail/c1_sizing_host_reference.py`; private adapter root and `core/strategies/PORT_MANIFEST.sha256`; `tests/ops/`; `lab/analysis/c1/tradeify_book_replay_2026-09/`; `tests/lab/tradeify_book_replay/`; rail/daemon/deploy files named by the amended TB-I3 packet.

- [ ] TB-I1: implement TB-S1's corrected per-leg laws, explicit candidate policy threading and lifecycle/host bindings. Keep the registry unadmitted. Include `book_policy.py` and its tests in the actual footprint.
- [ ] TB-R3: intake the seven exports with source identity, new override digests, normalization and reconciliation. Resolve remaining TB-R1 retrieval/manifest obligations without replacing lost overrides with falsely original provenance.
- [ ] TB-A/TB-A0: reuse the ports, correct ruled behavior where needed, prove parity at every reachable exercised mode and integrate verified private-port digests. A parity failure blocks the affected gate; no tuning to improve performance.
- [ ] TB-I2: only after accepted TB-S2 and required parity, implement continuous synchronized replay with path/source clocks, lifetime-scoped excursions, coverage exclusions, legal flattening, source-state continuity and account-capacity ordering. Benchmark one representative full path before freezing a batch workload.
- [ ] TB-I3 offline: after accepted/ratified TB-S3 and TB-I1, implement real listener/daemon recovery, barrier, feedback, checkpoints, active-leg interlock and GO validation. Reuse #365's scenarios through a real-component harness. Cover decision-persisted/send-result-missing crashes, queued broad closes, partial recovery and missing protection.

**Acceptance:** Private parity evidence and executable integration evidence refer to the same rule/port revisions. Model tests alone do not discharge implementation, route capability or live-feed gates.

## Task 5 — Freeze and qualify once, before feed funding

**Outcome:** A viable fixed portfolio or a conclusive stopped attempt.

- [ ] TB-F1: consolidate accepted contracts, parity, calendar/overlay, quantities, initial state, sample streams/sizes, Part A construction/depth, runtime budget, fingerprint algorithm and stress/monitoring actions. Obtain TB-P2 ratification and any required exact-depth ratification before TB-E1.
- [ ] TB-E1: run the frozen legality screen, n1 and n2, including the accepted regime gate, once. Failure ends this attempt with no substitute portfolio. Success seals the fixed-book replay fingerprint.
- [ ] TB-D0: only on the passed evidence, land the admitted policy row and provenance, governance-chain checks and public decision-record validator.
- [ ] TB-D1: resolve the ORB R2 decision from that evidence and obtain the separate operator GO. No ORB-free fallback.

**Acceptance:** All prerequisite fingerprints and acceptance results verified; no changed rule or selected alternative after observing outcomes. This milestone, not today's PR count, opens the feed-funding checkpoint.

## Task 6 — Prove the live route and freeze the deployed candidate

**Outcome:** The exact four-leg candidate is tested on the approved source while disarmed.

- [ ] Joshua selects/funds the production source only after A9's six conditions are satisfied. Verify current eligibility, CME/CBOT/COMEX entitlements, total cost and credential containment at that time.
- [ ] Complete source implementation and TB-I5 using the frozen provider-neutral CME equivalence test; verify all four order symbols and record source/config identity.
- [ ] Complete TB-I4 dedupe after M1 RESOLVED, its separate GO and the required disarmed host read; run the preregistered planted-defect tests.
- [ ] Complete TB-V1 runtime binding with frozen per-leg allocations and active-leg digest; verify required L-1/L-2 capabilities on the actual route.
- [ ] Run TB-I3's separately authorized live-feed test on the final candidate image, with real adapters and a listener verified disarmed before and after; include admission, dedupe and binding in the tested image.

**Acceptance:** Source equivalence, route capability, actual-symbol verification and disarmed live integration all pass for the image/components about to be sealed. Unsupported atomic/protection semantics remain a hard design blocker.

## Task 7 — Seal, adjudicate and obtain deployment GO

**Outcome:** Operator can activate the exact qualified portfolio under a valid account seal and approved procedure.

- [ ] Before the live-account ceremony, measure the full n3 plus adjudication/GO/build/verification duration using non-decision-bearing fixtures. Choose a session-boundary window large enough for the accepted seal contract; do not capture a seal that will predictably expire during the sequence.
- [ ] TB-B7: Joshua captures fresh dashboard, positions/working-orders and full account-history evidence; TB-T1 seals it. Seal execution identity and prove shared-component equality with the replay fingerprint.
- [ ] TB-E2: run the sole frozen n3 from that seal, adjudicated by Astra against the fixed criteria. Failure blocks deployment and follows the accepted admission-retirement path.
- [ ] TB-D2: prepare the digest/verdict decision packet; obtain Joshua's separate deployment GO; perform only the accepted GO-artifact/reseal sequence. Recheck all shared components, permitted image differences, configuration identity and account-seal validity.
- [ ] TB-B10: Joshua arms using the accepted TB-O1 procedure. Verify effective running-process activation, not only the configuration write, inside the valid seal window with no intervening account activity. Start the forward clock and frozen monitoring/down-only controls.

**Acceptance:** Real running image/config/active legs match approved evidence; account identity and seal are still valid at effective activation; monitoring and recovery are operable. Any expiry, intervening activity or code drift follows the previously accepted disposition, never an improvised rerun.

## Immediate order and operator touchpoints

**First Astra milestone:** ownership reconciliation, TB-S1, #360/#365 contract acceptance, and the cross-PR #361/#363/#362 closeout. TB-T1 and provider-neutral preparation can advance independently of exports and A7. Do not wait for every open PR before doing independent preparation.

**Joshua's earliest input:** seven OP-1 exports/screenshots and the separately attended A7 ceremony. Later: the consolidated live-risk/admission rulings and exact-depth ratification, source selection/funding, ORB/dedupe/emit GOs where required, B7 account evidence, and final deployment/session GO. Previously ruled O-1/O-5..O-9 do not need to be asked again.

**Calendar obligation:** current STATE records September 18 as the next operator-placed preservation-trade deadline. Read STATE again before acting; this roadmap does not advance or discharge it.

**Completion of this planning task:** evidence-backed sequence and unresolved contracts documented. Deployment date remains conditional on exports, contract closure, compute feasibility, route capability and qualification outcomes. No claim of current merge readiness, host readiness or qualification is made.
