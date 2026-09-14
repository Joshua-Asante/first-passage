# Tradeify contract closeout and implementation routing

**Status:** CONTRACT SET PARTIALLY CLOSED; PR readiness is recorded at observed heads below.
**Owner:** Astra coordinator. **Observed:** 2026-09-13 UTC.
**Boundary:** no portfolio implementation, qualification, live operations, deployment, arm, emission, or orders.

**Policy-review correction (PR #361 rev9, 2026-09-13):** the inventory below is a historical observation, not current merge/acceptance authority. #360 has since merged and expressly leaves #365 and replacement models #368–#370 unaccepted. For TB-P2/C10, follow the proposed admission ADR's complete T0–T11 trace: two separate ratifications, complete bootstrap/fingerprint freeze, and initial effective-activation checks after restart. A void seal requires stopping for the operator, not an automatic replacement outcome-bearing draw. The proposed text below is not a ratification or authorization; schedule decisions remain outstanding.

## Current TB-I1 first-slice reconciliation — 2026-09-13

**Execution base:** `f9427edfc42f5910726094022eb334d8119e5945`; plan commit `2374ae0d3f4f7a9607c4a7a56484808ff93d53dc`; branch `codex/tb-i1-book-policy`; local Python 3.14.3. See the [execution plan](../../superpowers/plans/2026-09-13-tb-i1-through-deployment.md). This section supersedes the readiness inventory and proposed decision shortcuts below; older sections are retained as historical observations, not current dispatch authority.

### Closed technical conflicts

- [TB-S1 §2](../../spec/2026-09-12-tradeify-book-protection-capacity-spec.md#2-quantity-law) now follows the already-ruled O-5 risk-scaled Striker law B, O-6 executed-base add law and O-1 off-rail Call-4 disposition. No new risk choice or ratification is recorded. The contract includes all mode/lifecycle rows, Striker's complete integer/add ladder and interval boundaries, and protected-capacity counterexamples.
- TB-S3 R-P/R-Q and TB-S2's sizing-consumer note now require the complete input context. Striker's rounded adapter-normal quantity cannot determine its protected quantity: the adapter produces stop distance; validated configuration produces the unscaled account risk budget, dollars-per-point and allocation; account/lifecycle owners provide mode/session and authorization. Adds use confirmed executed-base evidence. Production allocation remains zero until TB-V1.
- TB-P1 already records law B Striker, law A Vanguard, executed-base Striker adds and Call-4 off-rail. TB-P2 already assigns the corresponding `book_policy` corrections and canonical fingerprint implementation to TB-I1. Those decision texts are not edited or ratified by this slice.
- PRs #368/#369/#370 are now merged at the base, with primitive, producer and account acceptance records under `tests/ops/tb_s3_kernel/`. Their accepted model boundary remains offline; #365 is historical regression material. Old wording calling the three merged models unaccepted is historical and must not be used as a new model gate or as evidence of production readiness. Model suites were not rerun for this documentation slice.

### Release ledger

| Packet / obligation | Current disposition | Exact remaining gate |
|---|---|---|
| TB-I1 first slice: contract reconciliation | Locally verified; separate review commit | Arithmetic, strict document links, whitespace and repository check tier passed; production entry still awaits the ratifications below |
| TB-I1 production sizing, protocol docstring/parity, host bindings and fingerprints | BLOCKED — context-problem | Umbrella entry requires accepted TB-S1 plus operator ratification; TB-S3 Steps 1–2 require its §6 decisions and dated §5 S2b addendum, and the separately ratified P2 contract. No such ratification is inferred from the request to begin this slice. |
| Policy/fingerprint technical contract | Defined in P2 rev9 | The first P2 ratification is still absent; fingerprint implementation stays with TB-I1, not a second serializer in TB-T1. Second exact-depth approval is later and does not block specification reconciliation. |
| TB-I2 | BLOCKED — evidence and contract | Seven TB-R3-intaken exports and all reachable parity, corrected TB-I1, and accepted/reconciled S2; captured parity alone is insufficient. |
| TB-I3 offline | BLOCKED — dependency and ratification | TB-I1 plus TB-S3 §6/§5 ratifications; accepted models do not supply these approvals. |
| TB-C1 / unified schedule | Preparation available; schedule unresolved | Exact regular/early-close cutoff, own-flat, fill timing and backstop must agree across S2/S3/O1 before final acceptance/freeze. |
| TB-T1 | BLOCKED — policy transition | Accepted P2/C10 transition and shared TB-I1 fingerprint interface; its own account-evidence producer contract still applies. |
| TB-F1 / TB-E1 | BLOCKED — upstream gates | First P2 decision before F1; implementation/parity/calendar/consolidated evidence before freeze; exact positive Part A depth, budget and second dated ratification before E1. |

### Concrete decisions prepared for Joshua

These are review text, not approval records. Record each accepted decision as a dated addendum at its owning source, identifying the actual reviewed revision; partial acceptance leaves its dependent packets blocked. Previously ruled O-1/O-5..O-9 are not reopened.

1. **Execution contract:** “Ratify TB-S3 rev7 including its reconciled R-P/R-Q sizing-input contract, §5 S2b addendum, R-A3 late risk-reducing/barrier deviation, R-1 session latch and R-2 listener-owned daemon-loss recovery. R-L remains conditional on separate P2 ratification. Land the dated S2b addendum. Approval establishes the contract, not L1/L2 capability existence, source approval, deployment or arm authority.” The exact scope and retained conditions are the five rows of [TB-S3 §6](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md#6--operator-ratification-package-approval-pending), not the older R-1/R-2-only summary below. The base's S3 content was last changed at `091fbbd1063bc304a46c022b75c37eb18b1b50e7`; the current reconciliation diff must be included in the reviewed revision before recording this decision.
2. **First policy decision:** “Ratify TB-P2 rev9's fixed instance and five scoped concept-ADR supersessions, retained Part A construction, B1 statistic and B2 count correction, two-stage admission, canonical fingerprint contract, GO reseal and effective-activation checks. C10 invalidation stops for the operator and grants no automatic replacement outcome-bearing draw. Exact Part A depth requires a second dated ratification after TB-F1. This decision admits no registry row and authorizes no live action.” The full owner is [TB-P2 §7](../../adr/2026-09-12-tradeify-book-protection-instance-admission.md#7--ratification-package-both-decisions-pending); content at the execution base includes `cacd1f947ffc696bf9f6acfce8fdf7fa9f58e117`. The second decision must name the actual depth, deterministic budget and frozen runtime/tool/vector digests; it cannot be approved now without that evidence.
3. **Schedule direction, still proposed:** “Use 15:55 ET as the regular-session operator evidence check and 16:00 ET as portfolio own-flat completion; 16:30 ET is reconciliation only, never a holding allowance. Require a single pre-frozen schedule for replay and operations, including explicit risk-add cutoff, sufficient cancel/close lead time and early-close times from the official calendar.” This is a direction for the coordinated S2/S3/O1 amendment, not a fully specified scheduler: RC-8 currently includes next-open strategy exits at/after 16:00 and an active 16:30 flatten. Exact earlier risk-add cutoff and each early-close check/own-flat/backstop must be presented and accepted before schedule closure. Do not silently change strategy timing, infer a venue deadline, or label TB-F1 ready from accepting these three regular-session times alone.

**Evidence and scope:** production Rule-0 reads reconfirmed the current independent normal-base/add scaling, normal-integer-only helper, host risk expression, empty policy registry and existing lifecycle tiers. This slice reconciles their governing requirements; it does not claim that code now implements them. Literal arithmetic and document validation results are recorded in the execution plan after the checks run.

## 1. Historical source-backed inventory

| Obligation | Owner | Artifact / exact observed head | Evidence | Remaining gap / next action |
|---|---|---|---|---|
| TB-S1 sizing/protection/capacity | Astra → TB-I1 | `docs/spec/2026-09-12-tradeify-book-protection-capacity-spec.md` | production Rule-0 read; ruled O-1/O-5..O-9 | contract closed; implementation intentionally deferred |
| TB-S3 rail contract | #360 | `e1583232e543daa61e0db492440bb0bd1c32292a` | required check green; model link added | behind main; R-1/R-2 and S2b ratification outstanding; capability packet blocked where L-2 evidence absent |
| executable rail model | #365 | `f8e39afae6796cbea43b277fc6bd5d808c7a51e9` | 49 focused tests reported; required and path checks green; latest Codex review completed | merge-ready, not merged; test model is not a live implementation |
| TB-P2 admission/fingerprint | #361 | `6e419a30974de5b9a0d16eb1006d9a06752a4085` | required check green; review rounds folded | behind main; operator ratification required for exact Part-A depth/deviation and C10 disposition |
| TB-P1 prereg/calculator | #363 | `482fbf40f4ff2e2c27ec8b96724f8c68b4876130` | exact-rational boundary fix and digest scanner regression present | merge status BLOCKED while CI has not completed at observed head; align only after accepted P2 interface |
| TB-O1 procedure | #362 | `0e68cc05ccb8f883a56c596eaf178f8c86597926` | required and path checks green | clean/mergeable but schedule + GO/effective-activation propagation waits on accepted cross-contract ruling |
| snapshot sealer | TB-T1 | merged contract + packet | #358/#364 pointers reconciled | implementation packet READY only after P2 transition wording is ratified |

#356 remains credited for ports, candidate policy/capacity code, emulator and captured-size parity. #358/#364 own the frozen menu, snapshot contract/packet and pointer reconciliation; #359 owns replay rev 3. #353 and #344 stay closed without merge. No historical authorship is changed.

## 2. Findings ledger

| Finding | Producer → consumer | Reproducer / trace | Disposition | Remaining gate |
|---|---|---|---|---|
| normal base/add independently scaled | `book_policy.leg_quantities` → replay/sizing/rail | compare current function with ruled executed-base tier law | TB-S1 §2; TB-I1 correction assigned | explicit integer table tests |
| empty protection registry | TB-P2 → `dd_geometry` → arm/runtime | `POLICY_REGISTRY = {}` | correct pre-admission state | TB-E1, ratification, then TB-D0 |
| rail completion inferred without order evidence | broker reads → operation ledger | #365 regression suite | repaired in model | same-shape TB-I3 harness with real components |
| overlapping/partial closes and recovery | rail close queue → broker/ledger | #365 composed regressions | repaired in model, specified by #360 | TB-I3 harness and later route capability evidence |
| unknown accepted sends / persist-before-send crash | reservation → broker → restart | #360 sequences + #365 cuts | contract/model covered | durable TB-I3 implementation |
| seven scaled exports not demonstrated | private export intake → replay/parity | frozen TB-R2 menu | not discharged by captured-size parity | OP-1 + TB-R3; TB-I2 BLOCKED |
| activation checked only when config is written | snapshot/GO seal → running image | restart gap in procedure consumers | effective activation must revalidate account activity, expiry, image/config and GO transition | P2 ratification then O1/T1 propagation |
| regular-session time conflict | replay 16:30 backstop → 15:55 check / 16:00 own-flat | cited contracts | unresolved substantive schedule | operator decision below; then update S2/S3/O1 together |

## 3. One contract trace

The accepted dependency chain is TB-S1 quantity/state → TB-S2 replay → TB-S3 durable execution semantics → TB-P1 fixed preregistration → TB-P2 admission/seal → TB-T1 snapshot → TB-O1 effective activation. A fake/model implementation demonstrates reachability only. Existing route capability requires its own producer and fresh evidence:

- stop entry: broker order-level event → rail reconciler; unsupported means leg registry refusal and `BLOCKED — capability-problem`;
- attached brackets per fill: broker child-order evidence → expected-protection ledger; missing attachment blocks risk-add and invokes attended close recovery;
- component-wise amend preserving trail state: broker amend/cancel-replace events → protection ledger; unsupported or unknown enters protection-gap close recovery;
- cancel/close/working-order enumeration: broker snapshots with `as_of` → startup/EOD/kill reconciler; stale or position-only evidence cannot complete;
- feed and daemon health: daemon heartbeat/source timestamps plus listener control read → admission block; this never substitutes for terminal broker evidence.

TB-I3 must run the #365 scenario API against real daemon, listener, persistence, fake broker and telemetry components without weakening assertions. Later attended route verification uses the same cases without transmitting exploratory orders.

## 4. Historical proposed decisions — superseded by the current section

Previously ruled O-1 and O-5 through O-9 are not reopened.

### R-1 / R-2 and S2b amendment

**Proposed text:** “Ratify TB-S3's account-state model and risk-reducing source exception. A stale source may emit only the specified close/flat action for a scope not freshly confirmed flat; all entries/adds/amendments remain blocked. Stop entry, per-fill attachment, component-wise amend, working-order enumeration and order-level terminal evidence are mandatory capabilities; absence blocks the affected live packet and authorizes no fallback.”

**Conflict:** current single-leg rail and primary route evidence do not establish every L-2 capability. **Recommendation:** ratify the fail-closed interface, not capability existence. **Consequence:** TB-I3 offline becomes implementable; live testing stays capability-blocked. **Blocked consumers:** TB-V1/TB-I3 live packet/TB-O1 live use.

### P2 Part-A and snapshot C10

**Proposed text:** “Retain Part A inside the frozen n2 confirmation stream at the exact proposed bootstrap depth recorded by TB-P2; treat that depth as an explicit one-time deviation, not a reduced criterion. C10 replacement-run wording means mechanical rerun of the same frozen attempt only when no outcome-bearing sample was consumed; after any outcome-bearing observation or failed qualification, no replacement draw exists through expiry or reseal.”

**Conflict:** snapshot replacement-run language can otherwise contradict the one-attempt/no-extra-sample authority. **Recommendation:** ratify this narrow no-observation retry interpretation and the exact P2 depth. **Consequence:** failed confirmation/n3 stays terminal; P1/T1/O1 can share one trace. **Blocked consumers:** TB-F1, TB-D0, TB-T1 implementation.

### regular-session and early-close schedule

**Proposed text:** “For regular sessions, operator evidence check is 15:55 ET and the portfolio owns cancel-and-flat completion by 16:00 ET; 16:30 is a reconciliation backstop only and never permission to hold strategy exposure. For official early closes, derive analogous check/own-flat times from the frozen exchange calendar before preregistration. Qualification replay uses the same entry cutoff and flatten semantics as operations.”

**Conflict:** replay's 16:30 backstop can be read as a holding deadline while governing operations require own-flat by 16:00. **Recommendation:** preserve 16:00 own-flat and demote 16:30 to evidence recovery only. **Consequence:** S2, S3 and O1 need one coordinated amendment; no earlier arbitrary shutdown is inferred. **Blocked consumers:** TB-F1 and final O1 acceptance.

## 5. Historical bounded implementation packets — use the current release ledger

### TB-I1 — BLOCKED (contract ready; entry gates not met)

Base: post-merge TB-S1 and accepted P2 interface. Files: `ops/c1_rail/book_policy.py`, `ops/c1_rail/c1_sizing_host_reference.py`, `core/firm_rules.py`, `core/lifecycle.py`, focused tests. Existing interfaces: candidate policy, mode clock, capacity ledger. Proposed: executed-base tier calculation, lifecycle keys/allocations, reservation reconciliation. Inputs: accepted TB-S1; no private bodies. Stop after synthetic accepted/rejected cases pass; do not add the registry row, deploy or arm.

### TB-I3 offline — BLOCKED (R-1/R-2/S2b ratification)

Base: merged #365 + accepted #360. Files are limited to daemon/listener protocol, rail persistence/ledger/telemetry, HTTP and focused ops tests. Existing interfaces are enumerated in #360; the #365 model is the assertion oracle. Proposed interfaces must preserve operation ids, expected protection before send, order-level evidence and attended recovery. Stop when the same-shape synthetic harness passes; no live route, private port, emission or orders.

### TB-I2 — BLOCKED (evidence)

Base: merged S1/S2/P1 and frozen prereg. Files: replay implementation plus synthetic/public-safe tests and digest-only outputs. Inputs: TB-R3-intaken seven scaled exports and parity evidence from the approved private root. Existing captured-size parity is insufficient. Stop at reproducible replay mechanics; no qualification run and no result publication beyond authorized digests/verdict labels.

### TB-T1 — BLOCKED (P2/C10 ratification)

Base: merged snapshot contract/packet plus accepted P2 transition. Files are exactly the TB-T1 packet footprint. Inputs are private account observations from approved ignored locations; public fixtures are synthetic and redact values/identifiers. Implement byte serializer/normalizer version, exclusions and test vectors; verify GO-absent image and the sole allowed GO-artifact transition. Stop after synthetic seal/reseal/expiry/activity/drift/restart cases; do not snapshot a live account in this packet.

## 6. Ownership and stop condition

Astra owns coordination, specification, implementation planning, integration review and evidence assessment. Joshua owns substantive risk/trading ratification, merges and operational GOs. Claude/Fable are historical authors only and are not active dependencies; no `fable-judge` acceptance is required. Later owners: TB-I1 sizing; TB-I3 offline rail; TB-I2 replay; TB-T1 sealing; TB-D2 digest-only deployment decision packet. This record does not qualify the portfolio or authorize deployment.
