# TB-I1 through fixed-book deployment implementation plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the bounded TB-I1 production components, then qualify and deploy the fixed four-leg book through the existing evidence and operator gates.

**Architecture:** One shared implementation owns per-leg sizing, policy validation and canonical fingerprints. Replay and the production rail consume it; the accepted offline models supply regression scenarios, while broker capabilities require separate evidence. Astra owns integration; Joshua owns substantive ratifications, merges and operational GOs.

**Tech Stack:** Python, pytest, existing rail/daemon and private adapter ports, Git, digest-pinned JSON and exchange-session calendars.

**Spec:** Read the following at the execution base, not the stale primary checkout:
- `docs/spec/2026-09-12-tradeify-book-protection-capacity-spec.md` (TB-S1).
- `docs/spec/2026-09-12-tradeify-synchronized-replay-spec.md` (TB-S2).
- `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` (TB-S3).
- `docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md` (TB-P2, including T0–T11).
- `docs/briefs/pre-registration/2026-09-12-track-b-final-validation-prereg.md` (TB-P1).
- `docs/notes/2026-09-12-track-b-scaling-faithfulness-read.md` (ruled O-1/O-5/O-6 and frozen export menu).
- `docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md` (packet ownership and gates).
- `tests/ops/tb_s3_kernel/{KERNEL_CONTRACT,EVIDENCE_CONTRACT,ACCOUNT_CONTRACT,ACCOUNT_VERIFICATION}.md` (accepted model boundary).

## Global constraints

- Fixed K=1: Aegis 6J, Striker MYM p250, Vanguard MGC, ORB MNQ. No alternative book or policy search.
- Fixed candidate policy: own running settled-close account peak, trigger `0.01`, scale `0.40`; prior-session close selects the next session's mode.
- Preserve historical `core/dd_protection.py` bytes and constants. Keep `POLICY_REGISTRY` unadmitted until TB-D0 after TB-E1.
- Implemented configuration remains disarmed. Positive deployed allocations and verified order-symbol bindings belong to TB-V1.
- Private bodies, exports, account evidence and qualification figures stay in approved ignored roots. Public artifacts contain permitted digests and verdicts.
- Qualification compute is single-process. Freeze sample streams, sizes, criteria and budget before decision-bearing runs.
- Models establish offline behavior only. No agent places trades. Live ceremonies, funding, emission, deployment and arming retain their existing gates.

## Evidence baseline and planning status

Planning performed 2026-09-13. Successfully fetched `origin/main` to `f9427ed` (merge of #371); #370 is included. The primary checkout remains `133f043` with pre-existing untracked work, which this plan does not overwrite. Production and contract reads used `git show origin/main:<path>` after discovering the checkout lag. Acceptance records report model evidence; those tests were not rerun for this planning task.

Read production first: `book_policy.py`, sizing host, `dd_geometry.py`, `dd_protection.py`, firm rules and lifecycle. Existing `leg_quantities` independently scales normal base/add; the host still exposes `process_signal(payload, current_equity)` and historical sizing. `BookProtectionClock` and `CapacityLedger` are existing offline helpers, not a durable broker-connected account owner.

This is a gated delivery plan. Task 1 is actionable immediately. Tasks 2–5 are a proposed TB-I1 implementation design, released only after Task 1 closes its contract conflicts and entry gates. Later packets have explicit outcomes and entry gates; their own executable implementation plans must use their then-current source. This document does not invent interfaces for unresolved broker or snapshot contracts.

## Task 1 — Reconcile the execution base and TB-I1 contract

**Outcome:** One revision-bound sizing/fingerprint contract and a READY/BLOCKED packet ledger.

**Files:** TB-S1, scaling-faithfulness note, TB-P2, TB-S2, TB-S3, TB-O1 procedure and existing closeout/umbrella status records. Change only the consumers affected by the reconciled decision.

- [x] At execution time create an isolated `codex/tb-i1-book-policy` worktree from verified current main using the worktree skill; preserve the primary checkout and its private roots.
- [x] Read applicable repository instructions and record full base SHA, governing document revisions, model acceptance evidence and installed Python patch version.
- [x] Reconcile TB-S1 §2's generic `floor(normal_base × policy × lifecycle × beta)` with the already-ruled Striker law B. Striker must scale risk before the floor/cap, not scale a previously floored quantity. Preserve its executed-base add law. Correct the spec and affected consumers to the existing ruling; do not ask Joshua to select O-5/O-6 again.
- [x] Remove the implied on-rail Call-4 beta multiplier from the TB-I1 contract: O-1 records Call-4 off-rail. Preserve unrelated lifecycle functionality and the ordinary per-leg lifecycle multiplier.
- [x] Produce a literal table for all four legs, both modes and all reachable lifecycle states. Record inputs required by law B, which cannot be reconstructed from the normal integer alone.
- [ ] Reconcile TB-I1's ratification entry condition with the exact accepted P2 interface. Record the dated evidence when satisfied. A merged PROPOSED ADR is not a ratification.
- [x] Prepare concrete decision text for the remaining policy and execution ratifications and unified schedule. Preserve separate P2 decisions: initial policy/deviation ratification before TB-F1, then ratification of the exact Part A depth after TB-F1 and before TB-E1.
- [x] Reconcile R-1/R-2/S2b and any later execution amendments against the latest TB-S3; identify capability requirements separately from operator acceptance of the behavior.
- [x] Present the schedule proposal: regular-session evidence check 15:55 ET, own-flat completion 16:00 ET, 16:30 reconciliation backstop. These remain proposed until ratified. Freeze corresponding early-close rules from the official calendar, including entry cutoff and settlement semantics, identically in replay, rail and procedure.

**Exit evidence:** corrected cross-document quantity trace; literal expected rows; dated ratifications or explicit blocked consumers; no new policy choice inferred from this plan. Fingerprint technical work may be separately released only if the accepted interface and TB-I1 entry authority support it.

### First-slice execution record — 2026-09-13

Plan committed as `2374ae0d3f4f7a9607c4a7a56484808ff93d53dc` on `codex/tb-i1-book-policy`, based on `f9427edfc42f5910726094022eb334d8119e5945`. Worktree: `.worktrees/tb-i1-book-policy`; Python 3.14.3. The primary checkout and its unrelated work were preserved.

The first slice corrected S1 and its S2/S3 consumers for O-5 law B, O-6 confirmed-base adds and O-1 off-rail Call-4; supplied literal quantities and capacity cases; and updated the umbrella footprint to include the protocol docstring/parity and single fingerprint owner. R-P requires complete risk/configuration inputs, not inverse sizing from `qty_normal`. Production files remain unchanged.

The [current release ledger and concrete decision text](../../briefs/handoffs/2026-09-13-tradeify-contract-closeout.md#current-tb-i1-first-slice-reconciliation--2026-09-13) identify the still-pending S3/P2 ratifications and incomplete unified schedule. Checked boxes above mean reconciliation/preparation was performed, not that Joshua approved the proposal. Task 1's ratification entry remains open, and Tasks 2–5 have not started. Exact Part A depth remains a later F1/E1 decision.

Arithmetic verification passed for all 8 mode/lifecycle rows, 23 Striker base/add rows and 264 rational boundary cases, plus the non-cap law discriminator and protected-capacity arithmetic. These checks validate the written vectors, not the production sizing code or private export parity. Plan commit hooks passed. Strict relative-link validation passed for all six changed documents (40 links), and `git diff --check` passed. The repository check tier (`python scripts/gate_manifest.py --tier check`) passed under existing Python 3.13.2, including 72 evidence-store tests with 3 skips; the first Python 3.14.3 attempt stopped because that interpreter lacked PyYAML. No dependency files changed. Existing absent-private-data and advisory warnings remain; those skips do not verify private evidence. A Git-blob comparison confirmed seven relevant production files match the execution base. The first-slice reconciliation is verified locally; this record belongs to its separate review commit. Policy and execution ratifications remain pending.

## Parallel evidence track — Seven exports and intake

**Owner:** Joshua supplies chart evidence; Astra performs TB-R3 intake and parity. This track does not depend on finishing TB-I1, but any final quantity parity uses its corrected law.

| Export | Required chart change from captured state |
|---|---|
| S-P | Striker Account Size × 0.40 |
| S-W1 | Striker Account Size × 0.50 |
| S-W1P | Striker Account Size × 0.20 |
| S-W2 | Striker Account Size × 0.25 |
| S-W2P | Striker Account Size × 0.10 |
| O-N | ORB contracts 1, long/short chart margin 0%, scale-in enabled |
| O-P | ORB contracts 1, long/short chart margin 0%, scale-in disabled |

- [ ] Supply each List of trades CSV plus Inputs and Properties screenshots in the exact export state; preserve the frozen symbol/body, 15-minute timeframe, coverage and other properties.
- [ ] Intake CSVs under `core/data/tv_exports/cme/` and screenshots under `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/` in the approved primary private roots. Verify ignored status before copying; never assume a worktree contains the private data.
- [ ] Verify source/body and override digests, normalization, reconciliation and coverage before parity; reject unidentified or mismatched exports.
- [ ] Run the existing private parity harness for every reachable size/mode, including size-dependent halt feedback and ORB adds-off behavior. Publish only permitted verdict/digest records.

**Exit:** all seven intaken and all required parity PASS. Missing or failed evidence blocks TB-I2 decision-bearing use and TB-F1; synthetic TB-I1 tests do not substitute for it.

## Task 2 — One per-leg quantity implementation

**Outcome:** identical inputs produce identical quantities in policy and sizing-host consumers, including zero/refusal cases.

**Files:** modify `ops/c1_rail/book_policy.py`, `tests/ops/test_book_policy.py`; add `tests/ops/fixtures/tradeify_quantity_vectors.json`. Footprint is proposed until Task 1 closes.

**Existing interfaces:** `require_policy`, `LegSpec`, `leg_quantities`, `quantity_table`, `reachable_quantity_menu`, `BookProtectionClock`.

**Proposed interface:** `entry_quantities(leg_id: str, *, policy: ProtectionPolicy | None, mode: Mode, lifecycle_tier: str, normal_base: int | None, risk_dollars: Fraction | None, per_contract_risk: Fraction | None) -> tuple[int, int]`. Striker requires unscaled risk dollars and per-contract risk; missing law-specific inputs halt. `normal_base` supports Vanguard's already-computed normal ladder and is not a substitute for Striker risk inputs. Fixed legs derive their normal quantity from their leg definition. One helper derives add quantity from the confirmed executed base, with per-leg rules. Migrate callers so the old normal-integer-only API cannot silently size Striker.

**Contract to implement after reconciliation:**
- Aegis: fixed 8 before protection/lifecycle, exact floor afterward, no adds.
- Striker: `base = min(floor(risk_dollars × policy_multiplier × lifecycle_multiplier / per_contract_risk), floor(80 / 3.5))`; add `floor(confirmed_executed_base × 2.5)`. Capacity admission still independently enforces aggregate usage.
- Vanguard: quantity-floor law; protected and WATCH/RETIRED rows zero; a positive authorized normal base 1/2 produces add 1/2 via `max(1, pine_round(base × 0.8))`.
- ORB: authorized base 1; normal adds 1 each, protected adds 0; WATCH/RETIRED base/add zero. No beta haircut added on rail.

- [x] Add literal vectors before production edits, including a Striker case with risk dollars 700 and per-contract risk 10: normal 22/55, protected 22/55, WATCH-1 protected 14/35, WATCH-2 protected 7/17. These synthetic boundary inputs distinguish law B from quantity-floor law A.
- [x] Add Aegis authorized normal 8/0 and protected 3/0, protected WATCH-1 1/0 and WATCH-2 0/0; Vanguard 1/1 and 2/2 authorized normal, all protected/WATCH rows 0/0; ORB normal 1/1 and protected 1/0.
- [x] Add absent/wrong policy, unknown leg/mode/tier, nonfinite/nonpositive risk denominator, zero-base/add and exact integer-boundary rejection cases. Test partial executed-base add sizing independently from intended base size.
- [x] Run the focused tests and retain the observed regression failures; implement the minimal shared law and migrate the menu/table consumers.
- [x] Run `python -m pytest tests/ops/test_book_policy.py -q`; require the literal vectors to pass without deriving expected values from the implementation.

**Boundary:** this API calculates quantities. It does not prove broker fills, reserve capacity, admit the policy, or implement live execution.

### Second-slice execution record — 2026-09-13

The operator requested commit/push/separate PRs and continuation to the next slice. Plan [PR #372](https://github.com/Joshua-Asante/first-passage/pull/372) contains `2374ae0`; first-slice [PR #373](https://github.com/Joshua-Asante/first-passage/pull/373) contains `d620602` and is stacked on the plan branch. Both were verified open, non-draft, mergeable with successful checks and no review threads; CodeRabbit skipped review and is not an independent code approval. Explicit public-publication consent was recorded for those two commits after automatic review required it.

The continuation authorizes this bounded offline implementation; it does not populate S3/P2 ratification addenda or enable live behavior. Local branch `codex/tb-i1-quantity-laws` starts at `d620602e0bc2e247f0e5513558eb512aa50c13ed`. Task 2 is implemented locally in `book_policy.py`, with literal vectors in `tests/ops/test_book_quantity_laws.py` rather than a separate JSON fixture. Host wiring, durable evidence, registry admission, allocations, fingerprints and private port changes are outside this slice.

Implemented API: `entry_quantities` requires explicit policy, mode and lifecycle; Striker additionally requires unscaled `risk_dollars`, `per_contract_risk` and integer `cap_alloc`. Its returned add is prospective, assuming full base execution. Actual add sizing uses `add_quantity(leg_id, confirmed_base, *, mode, policy, lifecycle_tier)` and preserves per-leg rounding without a second haircut. The caller still must prove execution evidence and pass capacity admission.

`StrikerRiskInputs` records explicit input samples for `quantity_table(..., striker_inputs=...)` and `reachable_quantity_menu(..., striker_inputs=...)`. Each row retains its input sample. Normal-integer-only Striker callbacks fail closed; supplied samples demonstrate quantities but do not prove complete private-data reachability. Existing tests that asserted the superseded eight-contract protected ceiling and Vanguard WATCH-1 exposure were replaced by the ruled-law cases. Seven-export parity remains owed.

Red/green evidence: 196 initial new cases failed because the APIs were absent; the explicit-risk table test then failed before migration; six additional input-validation cases reproduced missing rejections before correction. The first combined focused run after implementation/migration passed 254 tests with 12 private-input skips. Errors-only pylint passed after identifying intentional missing-argument rejection tests. Final `py -3.13 -m pytest tests/core tests/ops -q --tb=short`: **1,531 passed, 16 skipped, 6 dependency deprecation warnings** in 276.41 seconds. The repository check tier passed under Python 3.13.2 (72 evidence-store tests, 3 skips); absent-private-data/advisory warnings remain. Errors-only pylint passed for all four changed Python files; document links and whitespace checks passed. Six host/governance/protocol source blobs match the first-slice base. Task 2 is implemented and verified; this record accompanies its separately requested review commit. Code review in this slice is focused coordinator self-review, not independent acceptance or a live-capability claim.

## Task 3 — Host bindings, session state and capacity contract

**Outcome:** an explicit candidate policy and validated account context drive the real sizing host; uncertain evidence produces a halt and unresolved capacity stays reserved.

**Files:** `ops/c1_rail/c1_sizing_host_reference.py`, `ops/c1_rail/book_policy.py`, `core/firm_rules.py`, `core/lifecycle.py`, `ops/c1_signal_daemon/book_protocol.py` (R-P docstring), `tests/ops/test_c1_sizing_host_reference.py`, `tests/ops/test_book_policy.py`, `tests/ops/test_book_adapters_parity.py`; add `tests/ops/test_tradeify_sizing_integration.py` and a focused protocol-semantic test. Private ports remain unchanged; B1 transport implementation belongs to TB-I3.

**Producer/consumer trace:** adapter signal → host quantity request → shared quantity function → capacity decision. The later TB-I3 account owner supplies validated active session/mode and terminal order evidence; TB-T1 supplies the sealed initial account state. Lifecycle state supplies per-leg authorization. The host never uses intraday equity to switch this book's mode.

- [x] Specify the typed account-context boundary in the Task 1 contract: operation identity, leg/symbol, active session/mode, settled-session evidence and seal, policy digest, lifecycle authorization, intended and confirmed base, reserved/confirmed exposure and evidence time. Missing required fields halt. This is a proposed production boundary, not an existing broker feed.
- [x] Add explicit candidate-policy/context arguments to the book sizing path. Preserve the existing M1/historical behavior under its own tests; do not silently substitute the new policy into legacy calls.
- [x] Add four lifecycle keys and inert host/config bindings with zero deployed allocation. Positive test allocations are explicit fixture inputs. Reuse the accepted risk-expression values; do not repurpose historical BASE_RISK constants or derive quantities from zero production allocations.
- [x] Test a 100000 peak and 99000 settled close entering protection on the next session, the rounding boundary immediately around 1%, duplicate/out-of-order settlement refusal, missing/stale/unsealed state and restart with mismatched state. Carried positions retain quantity; protected transition blocks ORB adds pending terminal cancellation.
- [x] Test 6J=10 and micro=1 accounting; all-or-refuse requests at 80; confirmed exposure plus unresolved reservations, partial fill transfer, and terminal-only release. Protected Aegis consumes 30 and capped Striker 77, so coexistence requires refusal/takeover rather than a claim that protection guarantees capacity.
- [x] Test only Aegis may displace, whole legs lowest-priority first. Partial/rejected/stale/unknown close evidence and contended takeover preserve the block. Per-operation identity must prevent duplicate release/fill accounting; if current per-leg helpers cannot express it, define the event reducer boundary here and leave durable journal ownership explicitly with TB-I3.
- [x] Run the focused host/policy/integration tests. Record which assertions use real host/policy components and which rely on synthetic account evidence.

**Stop:** TB-I1 owns pure decisions and validated interfaces. Durable reserve-before-send, broker reconciliation, concurrent account serialization, protected-transition completion and restart recovery are not accepted as production-complete until Task 6 integrates TB-I3.

### Task 3a — Inert identity bindings, 2026-09-13

Task 2 was committed as `9606c62` and published in separate [PR #374](https://github.com/Joshua-Asante/first-passage/pull/374), stacked on the first-slice branch. Continuation work uses `codex/tb-i1-host-bindings` at that revision.

This bounded part of Task 3 adds the four fixed-book identities to `firm_rules.py`, accepts their explicit lifecycle keys, and exposes `generate_book_bindings()` with zero capacity allocation and no verified order symbols. The existing sizing path explicitly refuses these IDs, including exit/flat bookkeeping, before historical sizing or state reads. The identity tuple remains separate from historical risk constants; its correspondence to `BOOK_LEGS` is tested. Existing image dependencies already include the affected core modules.

The session/policy/evidence sizing interface, account event reducer and capacity integration remain open Task 3 work. No new evidence schema is frozen by these identity bindings. TB-I3 owns durable execution integration, and TB-V1 owns deployed allocation and verified broker symbols. The historical host does not become a book execution route through this change.

Tests first failed in all 18 new cases, then passed after implementation. Focused host, lifecycle and quantity regressions passed: 303 tests, 4 existing skips. Full core/ops regressions passed under Python 3.13.2: 1549 passed, 16 skipped, 6 dependency warnings. Error-level lint, the repository check tier (including 72 evidence-store tests with 3 skips), strict plan links and whitespace checks passed. Frozen `dd_protection.py` and `dd_geometry.py` are unchanged. These results were recorded against the local working tree before committing Task 3a. No private evidence or broker integration is validated by these tests.

PR #374's final refreshed head was `9606c62dc72f40fffc70dc8831bad81985f57c77`: open, non-draft, clean and mergeable, current with its base, all checks successful and no review threads or submitted reviews. CodeRabbit skipped review of the stacked branch; its success status is not independent code approval.

Task 3a was published in [PR #375](https://github.com/Joshua-Asante/first-passage/pull/375). Its initial full-repository CI caught two historical Call-4 membership regressions outside the earlier core/ops run. The repair keeps `STRATEGY_KEYS` at the historical four legs and uses separate `BOOK_STRATEGY_KEYS` only to extend state validation. A new regression proves retired book legs cannot de-risk the historical Call-4 book. Both original failing tests remain unchanged. The repaired focused coldstore/lifecycle/host suite passed 109 tests with 4 skips, and error-level lint passed; the complete repository CI is rerun on the repair.

### Task 3b — Explicit session/account boundary, 2026-09-13

At `c68e768a67d7de66c99b257ef153dc7fbcbba723`, the operator requested completion of
the explicit boundary and connection to shared sizing. Branch
`codex/tb-i1-session-context` reuses the existing isolated worktree. The footprint
adds `ops/c1_rail/book_sizing_context.py` to keep typed validation separate from
quantity arithmetic and historical file-based sizing. The host's new
`process_book_signal` delegates to it; TB-S1 §6 and the Task 1 closeout specify
the caller/producer obligations. Historical code, policy admission and deployed
bindings remain unchanged.

The boundary accepts explicit request, candidate policy, account context, trusted
binding and clock time. It compares account/boot/operation/leg/symbol/session and
digest identities, full settled evidence against the binding, lifecycle and
evidence timing. It derives mode only from the prior close and calls the shared
entry or confirmed-base add law. It checks all four gross exposure/reservation
rows and refuses over-cap requests without clipping. All results have
`submit=False`; successful observations are not durable capacity admission.

This completes the requested interface and sizing connection, not the remaining
Task 3 account event reducer, durable settlement order, terminal cancellation,
takeover or reservation reconciliation. Snapshot authentication and canonical
fingerprinting remain TB-T1/Task 4; real owner inputs and atomic execution remain
TB-I3. The Docker recipe and `.dockerignore` include the pure import closure;
the listener still cannot route book orders. No image was deployed.

Tests initially failed on the absent interface. Focused review added a failing
changed-settlement/same-seal case, then bound the full verified record instead of
comparing only its digest. The boundary suite now passes 96 synthetic cases.
The full-repository
run exposed the image import-closure guard: lazy imports must also be packaged.
The recipe/allowlist now include the boundary, policy/geometry and protocol/feed
dependencies. The unchanged closure guard plus a new isolated-process import
test pass; combined boundary/image tests pass 101 cases. Local Docker is unavailable,
so this is manifest/import validation, not a Docker build claim.

Final full-repository run under Python 3.13.2: 4394 passed, 63 skipped, 23 warnings
and one failure (the packaging guard), in 1168.03 seconds. That run began before
the packaging repair; the repaired guard and new smoke test pass in the 101-case
focused rerun. The full suite was not repeated after the packaging-only repair.
Initial full-suite collection lacked statsmodels; hash-pinned statsmodels 0.14.6
and patsy 1.0.2 were installed into a temporary test directory, leaving repository
and global dependencies unchanged. Final error-level lint and the repository
check tier passed (including 72 evidence-store tests with 3 skips); strict links
and whitespace checks passed. Frozen drawdown/geometry, lifecycle and firm
rules source files match the slice base. These results were recorded before the
separately requested commit and PR publication.

### Task 3c execution packet — operation-aware capacity events

Opened from `796a4897bc193a11de2f1d35aebaa6142c422e76` on
`codex/tb-i1-capacity-events`. The coordinator owns integration. The legacy
per-leg `CapacityLedger` remains an offline compatibility helper; its misleading
durability docstring will be corrected. This slice adds a pure immutable reducer
in `ops/c1_rail/book_capacity.py`, with focused tests and a projection into the
existing typed sizing context. No broker producer or durable journal is invented.

Execution trace: host sizing demand → owner reserve command → new reducer state
→ owner persistence (TB-I3) → broker send (TB-I3) → validated execution/terminal/
reduction facts → reducer → gross exposure and pending-operation projection.
Every command carries a retained event ID and external causal sequence. Reserve
identity binds operation, leg, symbol and quantity; fills and reductions also
retain broker fact IDs. Exact repeats are idempotent; conflicting identities or
invalid evidence retain an account block without releasing capacity. This layer
consumes normalized facts from the future verified producer, not raw broker JSON.

- [x] Test operation-bound reservations, no clipping, 6J conversion and exact cap.
- [x] Test partial fill transfer, cumulative terminal agreement, terminal-only
  remainder release and request-attributed execution reductions. Duplicate IDs
  must not double count; stale, reordered, unknown or conflicting facts block.
- [x] Test only Aegis can initiate takeover, lowest-priority whole legs first.
  Keep its block until all displaced reservations are terminal and executions
  reduced to zero, with fresh post-update quiescence evidence. A competing request
  or partial/unknown evidence cannot clear the block or reserve the requester.
- [x] Project reducer exposure/pending IDs/blocks into typed context, preserving
  account/owner identity and other verified evidence; test through the real host.
- [x] Run focused regressions and required repository gates; record the remaining
  durable, snapshot-authentication and broker-route obligations explicitly.

Implementation uses immutable operation records, execution facts, request-attributed
reductions, retained event receipts and completed takeover identities. Refused
operation IDs cannot become new reservations on retry. Entry and close requests
share a unique namespace; a close request cannot change leg or contract symbol.
An invalid or unreserved late execution retains a block and the raw typed event;
known exposure is not represented as complete evidence in that state. No generic
block-clear or snapshot/epoch reset is supplied. A valid completion clears only
its own takeover block after terminal order facts, execution reductions and a
newer quiescence acquisition covering gross, working, protection and pending state.

`project_capacity` feeds gross counts, pending IDs and retained blocks into the
existing real sizing host. The owner must bind reducer state to the authenticated
snapshot behind that context; projection does not renew timestamps, verify seals
or prove evidence completeness. Successful sizing remains `submit=False`.
The new module is not yet imported by the deployed listener; image contents are
unchanged. TB-I3 must integrate the owner, persistence and packaging together.

At the Task 3c close, remaining Task 3 work included the combined settlement/transition
acceptance cases and focused R-P semantic contract, now addressed by Task 3d below.
Task 4 fingerprint serialization,
TB-I3 durable reservation/recovery, verified evidence producers, calendar and
snapshot tooling remain open. These synthetic events do not qualify a live route
or supply policy/execution ratifications or the seven private exports.

Verification on the uncommitted slice over `796a489`: initial tests failed because
the reducer module was absent. Later red/green regressions caught repeated
takeover-completion handling, cross-leg close-request reuse, and entry/close
request-ID collisions. Final `py -3.13 -m pytest tests/ops -q --tb=short`:
**1,402 passed, 12 skipped, 2 dependency warnings** in 96.79 seconds. Error-level
lint passed for the changed Python files. The repository check tier passed,
including 72 evidence-store tests with 3 skips; private-data/advisory warnings
remain. Strict plan links and whitespace checks passed. An independent read-only
review found no actionable defects within this boundary and separately ran the
38 capacity tests successfully. Core policy/lifecycle/firm-rule files and deployed
image manifests match the slice base. No full-repository or live-route result is
claimed; publication is separate from this local engineering record.

### Task 3d execution packet — settlement/transition and R-P closure

Starts at `589ecce8229b99440cad3d286cb8330883ce948b` on
`codex/tb-i1-session-protocol`, reusing the isolated worktree. Coordinator owns
integration. Use the existing clock, typed session boundary and capacity reducer;
do not invent a durable settlement owner or broker cancellation producer.

- [x] Test prior-close mode selection and rounding through the real host, duplicate
  and out-of-order settlement refusal without state mutation, and restarted host
  rejection of mismatched account/session/policy/snapshot evidence.
- [x] Add an immutable transition descriptor binding account, owner epoch, session,
  modes and the complete owner-supplied resting ORB-add operation IDs. A pure
  projection derives its block from retained terminal evidence, preserves carried
  quantities and unrelated blocks, and halts on unknown/mismatched operations.
  TB-I3 must authenticate completeness, persist this descriptor before cancellation,
  and send/reconcile broker actions; this projection sends nothing.
- [x] Document R-P adapter-normal entry/add quantities, confirmed-scope exits,
  unchanged brackets and admitted emulator quantities. Test shared admission/host
  parity using complete inputs, partial confirmed bases and missing-input refusals.
  B1 mapping remains TB-I3; no private port bodies change.
- [x] Run operations regressions, required gates, lint and independent review;
  record the exact bounded completion and remaining owner dependencies.

Task 3's bounded implementation is complete locally. The clock-to-host tests
cover prior-close selection at and around the rounding threshold, duplicate/older
settlement refusal without mutation, and mismatched evidence on a new host.
`ProtectionTransition` retains the owner-captured add IDs and binds the session,
account, epoch and modes. `project_transition` projects capacity and derives a
block until every captured operation is terminal. It neither clears existing
blocks nor changes carried quantities. A fill/cancel race preserves the filled
quantity; missing/unknown facts remain blocked. Feed this function fresh owner
context each time: an earlier projection is not evidence and its blocks are never
implicitly cleared. Invalid bindings raise and require caller halt.

R-P is now documented on `OrderIntent`; shared-admission versus real-host tests
cover all four legs, modes and lifecycle tiers, confirmed-base adds, absent risk
or fill evidence, and unchanged exit scope/bracket semantics. These tests use
explicit normalized synthetic owner inputs, not private adapters or a B1 builder.
Actual production replay, payload mapping, descriptor persistence before send,
authenticated completeness, concurrent ownership, cancellation/recovery and live
restart qualification remain TB-I2/TB-I3 responsibilities. Calendar and snapshot
authentication remain their named owners; Task 1 ratifications are still pending.

Verification over `589ecce`: six transition tests first failed because the new
API was absent, then passed. An initial R-P fixture referenced `side` instead of
the existing `entry_side` field; corrected without production behavior changes.
The combined focused suite passed 227 tests before additional race coverage.
`py -3.13 -m pytest tests/ops -q --tb=short` passed **1,462 tests, 12 skipped,
2 dependency warnings**, in 125.62 seconds. A final added two-operation terminal
case was verified in the **160-passing** integration-file run. Error-level lint
and the required repository check tier passed (72 evidence-store tests, 3 skips;
existing private-data/advisory warnings). Independent review found no actionable
defects and separately passed the then-current 159 integration cases. Core risk,
lifecycle and firm-rule sources and deployed image manifests match the base;
the protocol constructor and emulator behavior are unchanged. This is local
implementation evidence, not PR review/merge, policy admission or live capability.

## Task 4 — Canonical fingerprint implementation

**Outcome:** every later producer and verifier can call one side-effect-free serializer under a pinned runtime; unauthorized changes alter identity or fail validation.

**Create:** `ops/c1_rail/policy_fingerprint.py`, `tests/ops/test_policy_fingerprint.py`, `tests/ops/fixtures/policy_fingerprint_vectors.json`.

**Proposed functions:** `canonical_policy_bytes(row: Mapping[str, str]) -> bytes`, `normalized_geometry_bytes(source: bytes) -> bytes`, `sha256_bytes(data: bytes) -> str`. The policy serializer accepts exactly the four canonical string fields; caller-side policy conversion is explicit. Runtime/recipe/tool-manifest validation is a separate pure check, with an exact schema fixed during Task 1. Registry contents/provenance are checked independently of exclusion; normalization never constitutes admission.

- [ ] Add a literal policy byte vector with instance `tradeify_portfolio@Tradeify_Select_100K`, reference `trailing`, scale `"0.4"`, trigger `"0.01"`. Expected bytes are `b'{"instance_key":"tradeify_portfolio@Tradeify_Select_100K","reference_mode":"trailing","scale":"0.4","trigger":"0.01"}'`.
- [ ] Test key-order equivalence, UTF-8/no BOM/no newline, sorted compact JSON, and rejection of extra/missing fields, floats/bools and noncanonical/nonfinite numeric strings. Serialize with `ensure_ascii=False` and `allow_nan=False`.
- [ ] Parse geometry with `ast.parse(..., mode="exec", type_comments=True)`. Require one top-level simple registry assignment; reject repeated, indirect or ambiguous rebinding. Remove exactly that node; dump with `annotate_fields=True`, `include_attributes=False`, `indent=None`; hash UTF-8 bytes without newline.
- [ ] Pin literal normalized bytes and SHA-256 vectors for permitted pre/post admission; mutate each other AST component and require a changed digest. Include extra registry rows/provenance violations in the independent governance check so exclusion cannot conceal them. Ordinary comments are not represented by this AST recipe; do not claim raw-byte coverage of them.
- [ ] Hash full bytes for `book_policy.py` and every other unexcluded shared component. Validate exact CPython patch, recipe version and tool/dependency digests; keep the tool's own digest outside its hashed payload.
- [ ] Define deterministic config serialization and vectors for T11's only allowed initial-arm delta: `dry_run` to false and `armed_until` to the explicitly authorized deadline. Reject every other config change. The helper validates bytes only and does not perform activation.
- [ ] Run `python -m pytest tests/ops/test_policy_fingerprint.py -q`; retain literal independently checked byte/hash evidence and publish the complete manifest schema for E1/D0/T1/B7/D2/I3 consumers.

## Task 5 — Accept the bounded TB-I1 packet

- [ ] Run `python -m pytest tests/core tests/ops -q` and the current repository-required checks from the isolated execution base. Include the accepted model suites to detect shared-import regressions; their historical test counts are not current evidence.
- [ ] Verify original `core/dd_protection.py` bytes unchanged, registry still unadmitted, live allocations inert and private files absent from the diff.
- [ ] Trace the real host → shared policy → capacity decision and policy/config → canonical bytes → digest → verifier boundaries with both accepted and refused inputs.
- [ ] Review quantity literals independently of implementation formulas, rejected evidence paths, and fingerprint exclusions. Record exact tested SHA and unresolved TB-I3/TB-T1 producers.
- [ ] Prepare a bounded review packet with changed behavior, regression evidence, contract sources, consumer migration list and remaining capability/evidence gates. Commit/PR/merge follow their separately authorized workflow; this planning request performs none of them.

**TB-I1 complete means:** corrected shared quantities, explicit host policy/context threading, inert bindings, tested state/capacity decisions and canonical fingerprints are accepted at a specific revision. It does not mean parity, qualification, durable rail integration or deployment is complete.

## Task 6 — Deliver dependent production packets

| Packet | Entry gate | Deliverable and acceptance |
|---|---|---|
| TB-I2 replay | accepted S2, TB-I1, required panels and seven-export intake/parity | continuous synchronized replay using the shared law/calendar; synthetic matrix and regenerated-ledger parity; no qualification run in implementation packet |
| TB-I3 offline | accepted/ratified S3 and TB-I1 | real daemon/listener/persistence/telemetry through the accepted primitive/producer/account scenarios; reserve-before-send and all crash cuts, terminal evidence, FIFO/protection ownership, episode recovery, barrier, interlock and replay restore |
| TB-C1 calendar | horizon and unified schedule settled | forward calendar and closure overlay with source provenance and required attestation; early-close/closure/DST tests; fail closed beyond coverage; preserve frozen D19 |
| TB-T1 snapshot tooling | accepted P2/C10 transition and snapshot contract | exact existing packet footprint; shared fingerprint tool; synthetic freshness, history/adjustment, relational, expiry/activity/drift and reseal checks; private inputs and digest-only public output |

- [ ] Write each packet's code-level plan from its actual production base and accepted interfaces before implementation. Keep one coordinator for their combined account behavior.
- [ ] Integrate all four through one quantity law, capacity accounting, protection clock and calendar. Replay and rail must agree on quantity, refusal, priority and flatten behavior.
- [ ] Qualify actual L1/L2 producer/route semantics separately; an offline model cannot invent stop-entry, per-fill brackets, amend behavior or order-level terminal evidence.

## Task 7 — Freeze and qualify the fixed book

- [ ] TB-F1: require the implementation/parity/consolidated-read gates, calendar artifacts and first P2 ratification. Resolve every freeze field: book/policy, reachable sizes/modes, allocations, port/code/tool/runtime digests, source panels/warm-up, costs/fill/capacity rules, initial state, calendars, RNG namespaces, streams and exact n1/n2/n3 sizes.
- [ ] Measure runtime on non-decision-bearing synthetic workloads. Use the accepted calculator to select exact sample sizes and produce the deterministic compute budget; freeze them before any outcome-bearing draw.
- [ ] Freeze Part A's six-month source-block construction, venue-session length, truncation, rebuilt inner five-session blocks, percentile method, seeds, positive per-panel depth and 100/close-call-200 panel rule. Obtain the second dated ratification of that exact depth before TB-E1. No sample-size/depth number is chosen by this plan.
- [ ] TB-E1: execute the prescribed legality screen → n1 → n2/Part A/Part B → seal sequence once, with terminal failure and no alternative candidate or extra sample. Publish permitted digest/verdict evidence.
- [ ] TB-D0: after the seal, admit exactly the sealed policy row with both ratifications and FBR provenance; run non-vacuous governance-chain checks. Obtain separate TB-D1 ORB GO from the book-level evidence.

## Task 8 — Complete live prerequisites and attended integration

- [ ] Advance M1's attended A7/A8 work under its existing procedure until RESOLVED; preparation can overlap offline development.
- [ ] Open feed selection/funding only after its A9 conditions; implement the approved source and pass TB-I5 feed-equivalence testing with frozen criteria.
- [ ] Complete actual broker capability evidence, all four symbol verifications and TB-I4 dedupe after M1 and its required GO/disarmed reads. Unknown or unsupported capabilities block live use.
- [ ] TB-V1 materializes the already-frozen allocations and active-leg identity after E1/D0/D1 and symbol verification. Include admission, binding and dedupe in the tested image.
- [ ] Run the separately authorized attended TB-I3 live-feed integration with real adapters and listener verified `dry_run=true` before and after. Pass source/route/feedback/recovery checks on the exact candidate image.

## Task 9 — B7, sole n3, deployment GO/reseal and initial arm

- [ ] Rehearse elapsed time for n3 plus adjudication/GO/reseal/build/verification on synthetic inputs before capturing an expiring account seal.
- [ ] Joshua supplies fresh B7 dashboard, zero positions/working orders and full account-history evidence; TB-T1 seals it and the execution fingerprint. Prove every shared component equals FBR.
- [ ] Run the sole final n3 under the frozen contract. Part A is not rerun here. Failure ends the attempt; void/expired seals follow the accepted P2 disposition and stop for the operator, never an automatic replacement outcome-bearing draw.
- [ ] Prepare the digest/verdict deployment packet; obtain deployment GO and perform only its allowed GO-artifact/reseal transition. Recheck all shared components and complete image/config identity.
- [ ] Joshua performs the attended initial arm. At effective activation after restart, validate actual image/config/GO, current seal validity and fresh no-activity attestation bound to the boot/request. Persist acknowledgment before risk-add admission; a config write alone is not completion.

## Delivery order and operator touchpoints

Critical engineering chain: **Task 1 → TB-I1 Tasks 2–5 → dependent replay/rail integration → TB-F1 → TB-E1 → admission/runtime binding → attended live integration → B7 → sole n3 → GO/reseal → initial arm**.

Exports/intake, decision preparation, calendar preparation and M1 preparation can advance alongside engineering within their own gates. Snapshot implementation waits for its accepted transition. Feed funding remains at its named checkpoint.

The next concrete review artifact is Task 1's reconciled contract and TB-I1 release ledger. Joshua's next contributions are the seven export bundles and concrete outstanding ratifications; exact-depth approval comes only after TB-F1 supplies the number. Existing O-1/O-5..O-9 rulings are reused. No deployment date is promised before external evidence, measured compute feasibility and route qualification clear.
