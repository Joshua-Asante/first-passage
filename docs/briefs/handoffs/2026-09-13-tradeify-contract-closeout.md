# Tradeify contract closeout and implementation routing

**Status:** CONTRACT SET PARTIALLY CLOSED; PR readiness is recorded at observed heads below.
**Owner:** Astra coordinator. **Observed:** 2026-09-13 UTC.
**Boundary:** no portfolio implementation, qualification, live operations, deployment, arm, emission, or orders.

## 1. Source-backed inventory

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

## 4. Consolidated operator decisions still required

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

## 5. Bounded implementation packets

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
