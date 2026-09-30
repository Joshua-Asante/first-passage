# Handoff — Tradeify T00 step 1b: close candidate 3′ P7 with the retained real source

**Type:** cc_handoff (bounded producer completion + real-input verification; no screen or Monte Carlo)
**Date:** 2026-09-24
**Status:** **AUTHORIZED FOR T00 STEP 1b; TASK 1 INTERFACE/FACTS FROZEN.** General step-1b authority already exists. The coordinator accepted the Task-1 checkpoint and exact interface in §7 on 2026-09-24. Continue only through Tasks 2–4 under this packet. T00 step 2 remains excluded; publication or merge supplies no additional authority.
**Parent roadmap:** [deployment-checklist amendment §T00](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#t00--feasibility-evidence-for-the-selected-book-new-investment-decision-not-a-gate-250k500k-may-return-early). This is one bounded execution handoff inside T00 step 1, not T00 step 2.
**Executor:** one qualification/source executor on an isolated worktree, with read access to the primary checkout's ignored private inputs. **Coordinator:** owns scope, accepts the return and updates the T00 step-1 disposition. **Operator:** authorizes this packet, retains private-source custody, signs the exact reviewed OPERATOR contract, and alone may later ratify T00 step 2. **Combined acceptance remains with the coordinator.**
**Authority:** modify only the tracked files and private-root surfaces named in §3; run source-independent and private-input verification; stage the already-retained corrected Striker bytes only beneath the approved private output root after exact hash verification. No write to the primary active port root; no account, host, provider, broker, deployment, arm or order action. A `DONE` return supplies no permission for T00 step 2.

## 0. Owners and production code to read first

Read these at the execution head and record `git log -1 --format='%h %as' -- <path>` for every tracked owner used:

- [T00 step-1 return](2026-09-22-tradeify-t00-step1-producer-inventory.md), especially §§2, 7.4–7.5 and 7.8. Candidate 3′ is the selected producer: P1–P6 MET, P7 NOT MET. Candidate 1 recovery is not this packet.
- [Ratified path-position bracket](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23). Preserve the accepted `BookReplay._split` path; evaluate R1 and R2 independently; never manufacture agreement by combining one run's P&L with the other's lows.
- `ops/c1_rail/qualification/production_source.py`: `PRODUCER_GAPS`, `ScheduleExecutionEvidence`, `prepare_production_inputs`, `ProductionSource.build`, `replay`, and the exact required retained roles at lines 777–778.
- `ops/c1_rail/qualification/replay.py`: `BookReplay._split`, `_schedule` and `run`. One synchronized event loop owns shared cash, capacity, takeover and the emitted daily P&L / `intraday_low` pair.
- `ops/c1_rail/book_policy.py`: executable selected-book truth — `CANDIDATE_TRIGGER = "0.01"`, `CANDIDATE_SCALE = "0.40"`, `BOOK_LEGS`, `entry_quantities`, `add_quantity` and `CapacityLedger`.
- `core/dd_protection.py`: production Rule-0 cross-check only. Its frozen `DD_TRIGGER = 0.015` / `DD_SCALE = 0.40` historical anchor is **not** the T00 selected-book policy and must not enter this producer.
- `ops/c1_signal_daemon/book_adapters.py`: four runtime pins, historical and runtime-effective settings pins, stale-byte refusal and qualification loader.
- [T10 source/freeze packet](2026-09-21-tradeify-t10-source-and-freeze-packet.md) §7 and `docs/notes/2026-09-21-t10-phase1-source-reconciliation.md`: R1 reading (a), R2 panel-derived, F10's 2026-09-24 operator confirmation, and unresolved source-calendar facts. T10 phase 2 is not a predecessor to this packet.
- `docs/briefs/phase3-preparation/2026-09-15/{identity-ledger.md,production-readiness.md,requirements.md}` and the exact retained Step-3/Step-6 contracts and reviews they identify. Reuse accepted evidence by exact identity; do not re-create it from prose.
- `docs/load_bearing_numbers.md`: no screen figure is produced here; any later bust/pass claim still needs an intraday-honest RESULTS path and assumes the inactivity barrier is OFF unless its owner says otherwise.

### 0.1 Read-only dispatch baseline to reverify

The draft author's 2026-09-24 read-only check at working tree `3d7648b93b36cf283f41af5e94ce0ceaedaf23b9` found:

- All four M15 panels (`6J`, `MGC`, `MYM`, `MNQ`) match `core/data/bar_data/SHA256SUMS`.
- Aegis, Vanguard, ORB and historical `effective_inputs.json` in the primary ignored port root match their public pins.
- The primary `dj30_mym_p250.py` is the refused original `c81aa59c…`, not admitted `efd479b6…`.
- The exact admitted corrected Striker bytes are locally reachable at `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/corrected-ports/dj30_mym_p250.py` and hash to `efd479b6b4c7eeaa7d8df3f40f36593f87d96b9d5f512dc79c4dd9b0520211f4`.
- The path-position convention is ratified but not implemented. The eight required retained source roles are not present in a closed production artifact inventory.

These are dispatch observations, not acceptance. Reverify them before the first write. A changed or missing accepted byte is a checkpoint, not permission to reconstruct it.

### 0.5 Resolved dispatch rulings

1. **Authority:** general T00 step 1b / P7-closure authority exists. It covers Tasks 2–4 inside this packet and no T00 step-2 work.
2. **Reservation-only state:** the native replay's synchronous admit/submit/feedback sequence supports the schedule-boundary invariant assessed in §7. The accepted interface still fails closed if `reserved > 0` is observed without a broker-pending order; no reservation-only price branch exists.
3. **Private output root:** use `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/t00-p7-closure-2026-09-24/`, which is covered by the campaign-local `.gitignore`. Do not use repository-root `local_artifacts/`.

### 0.6 Pre-mortem and budget boundary

**Estimated execution envelope:** 250k–500k tokens for the bracket implementation, retained source pack, private-input run, focused review and return. The final P7 scoring/recompute portion was previously estimated at 100k–250k once inputs existed. These are planning estimates, not spend or statistical-run authority.

| Likely failure | Earliest detection | Required response |
|---|---|---|
| Stale Striker bytes are run or the accepted private original is overwritten | Pre-write SHA-256 inventory | Copy, never move, into the approved private staging root; require source and staged destination `efd479b6…`; do not overwrite the primary active port root. |
| R1/R2 reorders OHLC extrema, shares one run's lows, or adds signals/costs | Planted unit cases before any real-input run | Fail the interface freeze; retain `BookReplay._split` validation and fresh adapters/brokers/state per run. |
| Calendar construction silently omits a date or calls an unknown date closed | Source-calendar/population-index negative tests | Return the exact `UNKNOWN_SOURCE_DATE` or coverage gap. No extrapolation and no guessed closure. |
| A reservation-only schedule state has no ratified branch | Invariant test at interface freeze | Return `NEEDS_CONTEXT`; do not classify it as pending-only without a ruling. |
| A public test fixture is mistaken for reviewed production evidence | `ProductionSource.build` against the signed OPERATOR contract | Keep fixtures `TEST_ONLY`; the real run must consume exact retained bytes and review companions from the private closed inventory. |
| The FXIFY-C2 1.5% trigger leaks into the selected book | Rule-0 source audit and protected-boundary test | Reject the build. Candidate 3′ must use `candidate_book_protection_policy()` at 1%/0.40; do not edit `core/dd_protection.py`. |
| Private strategy, account or result content becomes tracked or printed | Before every commit and in final verification | Stop; remove it from the patch without deleting the private original; report only paths, hashes, counts and verdict labels allowed by the public posture. |

**What makes the packet moot:** a current accepted producer already meeting P7 under the ratified bracket, or loss/mismatch of an admitted source byte that prevents exact identity verification. In either case return to the coordinator before implementation.

## 1. Selected outcome, prerequisites and return boundary

**Selected outcome:** candidate 3′ can consume the exact admitted four ports, runtime-effective settings and four M15 panels through one reviewed source pack, then emit two complete synchronized path results—R1 and R2—each with its own daily P&L and matching unscaled `intraday_low`. P7 becomes MET only when the retained contract, reviews, real-input replay, protected/adds-off parity bindings and one hand-recomputed real bar-level day all agree.

**Prerequisites:** general step-1b authorization and the Task-1 interface freeze are resolved; accepted corrected Striker bytes and all four panels are currently reachable but must be reverified; the timing convention is ratified; T10 R2 is panel-derived; T10 phase 2, T06, T07/T08, a production feed and provider funding are not prerequisites.

**Ownership:** one executor owns the implementation and private source pack; the coordinator owns interface freeze, contract review, review disposition, P7 scoring and the T00 step-1 verdict; the operator owns this packet's authorization, the exact OPERATOR-contract signature and any later T00 step-2 ratification.

**Verification:** red/green focused tests, exact byte identities, signed OPERATOR-contract construction through `ProductionSource.build`, a real retained-input R1/R2 replay, the one-day hand recompute, independent refute-first review, and launcher evidence records from a stable source tree.

**Checkpoint:** Task 1 returned and its interface/fact freeze is accepted in §7. Continue at Task 2. Return immediately on an identity mismatch, violation of the frozen reservation invariant, a required file outside §3, or any proposed change to a frozen risk constant/policy value. Record progress and evidence in §7 of this packet and private details only in the approved private root.

**Return boundary:** `DONE` only with candidate 3′ P7 MET and the evidence in §5; otherwise `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED — <exact reason>`. Return without pre-registering or running T00 step 2, without a screen/MC verdict, and without selecting the next task.

## 2. Behavioral contract

**Integration owner:** the coordinator accepts the complete producer behavior; passing component tests or producing eight JSON files does not establish P7.

**State and decisions:**

- The exact signed OPERATOR contract and its retained artifact inventory own source identity. Caller callbacks, process-global caches and synthetic fixtures cannot supply authority.
- `BookReplay` remains the owner of the accepted OHLC path, one-bar signal cadence, shared cash/capacity/takeover state and daily excursion calculation.
- The bracket provider owns only the schedule instant's vertex position for a named run. It does not reorder the path or choose a policy mode.
- Each R1/R2 execution starts from fresh adapters, brokers, ledger, account state and protection clock. No result object, low series or mutable source state crosses between runs.
- `candidate_book_protection_policy()` remains 1%/0.40 for this selected book. The frozen `core/dd_protection.py` 1.5%/0.40 literals remain untouched.

**Acceptance cases:**

1. Long and short open positions choose adverse/favourable vertices exactly as the ratified table defines.
2. Pending-only cutoff chooses close/fill for R1 and open/cancel for R2 without assuming direction.
3. Position plus pending follows the position rule, and pending orders execute only along the reached prefix.
4. A reservation-only state is either proven unreachable or returns `NEEDS_CONTEXT`; it never silently receives a branch.
5. Tie, flat-open, flat-close and reduced-turn bars retain `_split` aggregation and turns; 20,000 random-bar coverage is repeated or exceeded.
6. Each run is independently evaluated and carries its own P&L and `intraday_low`; no hybrid contributes to P7.
7. Original `on_bar` calls, signals, commissions and source bars occur once per completed source bar. Schedule segments add none.
8. Missing source roles, reviews, schedule coverage, exact port/panel bytes or unknown calendar dates fail before a decision-bearing replay.

**Dependencies:** existing producers are the accepted panels, Step-3/Step-6 admissions, corrected ports and existing source parsers. The proposed producer is the bracket-aware schedule provider plus the eight-role reviewed source pack. T00 step 2 remains an excluded downstream consumer.

## 3. Tasks and authorized file boundary

### Task 1 — Freeze exact inputs and the bracket interface

- [x] Run `./fp.ps1 doctor` from the checkout being tested and record interpreter, HEAD and `git status --short`.
- [x] Hash the four active ports, `effective_inputs.json` and four M15 panels. Compare them to `book_adapters.py`, the runtime-effective successor derivation and `SHA256SUMS`.
- [x] Copy the retained corrected Striker port into the approved private staging root; copy, never move. Hash both source and staged destination as `efd479b6…`. Use the signed contract's retained bytes, or `FP_PORT_ROOT` for parity-only checks; do not overwrite `ops/c1_signal_daemon/ports/dj30_mym_p250.py`.
- [x] Write failing interface tests establishing the eight acceptance cases in §2, including reservation-only refusal and independent fresh state for R1/R2. The exact frozen-return assertions remain the first Task-2 update required by §7.
- [x] Present the proposed public types/signatures and red-test output to the coordinator for the interface-freeze checkpoint. Production implementation stopped until the §7 acceptance.

**Frozen interfaces (accepted 2026-09-24; §7 owns full semantics):**

```python
@dataclass(frozen=True, slots=True)
class ScheduleExposure:
    position: int
    pending: bool
    reserved: int

@dataclass(frozen=True, slots=True)
class ScheduleSplit:
    prefix: Bar
    suffix: Bar
    prefix_executes: bool

@dataclass(frozen=True, slots=True)
class BracketReplayResult:
    r1: ReplayResult
    r2: ReplayResult
```

- `ScheduleExecutionBracket.for_run(run_id: str) -> ScheduleExecutionEvidence`; only exact `R1` and `R2` identifiers are accepted, and every call returns a fresh run-local provider.
- `ScheduleExecutionEvidence.split_bar(..., *, exposure: ScheduleExposure) -> ScheduleSplit` and `split_interval(..., *, exposure: ScheduleExposure) -> ScheduleSplit`; there is no mutable `observe_exposure` or empty-prefix side channel.
- `BookReplay._split(..., exposures: Mapping[str, ScheduleExposure]) -> dict[str, ScheduleSplit]`. It retains the existing aggregation, validity, boundary-quote and reduced-turn validation for every returned pair. The caller executes only prefixes whose result has `prefix_executes is True`, then performs the scheduled action, then retains every suffix for the rest of the interval.
- `ProductionSource.replay_bracket(path) -> BracketReplayResult`, holding named `r1` and `r2` `ReplayResult` values built from separate fresh engines. No single-run default is added.

### Task 2 — Implement the ratified bracket without widening T00

- [ ] Implement the minimal bracket-aware schema/provider in `ops/c1_rail/qualification/production_source.py` and immutable exposure/result types in `ops/c1_rail/qualification/model.py`.
- [ ] Modify `ops/c1_rail/qualification/replay.py` only enough to capture the frozen exposure snapshot, return `ScheduleSplit` values, skip only explicitly non-executing prefixes, and retain `_split` as the aggregation/turn-order validator.
- [ ] Add `ProductionSource.replay_bracket` so R1 and R2 load fresh ports and execution state independently. Leave screen/kernel aggregation and GO/NO-GO adjudication untouched.
- [ ] First update the authored red tests to assert the exact frozen types and behavior in §7, including flat zero-volume R2 cancellation, subsequent splits, exposure timing and reservation refusal. Preserve the red state, then make those tests pass; run the existing replay, production-source, runner, panel and cost/schedule suites to detect semantic drift.

### Task 3 — Produce the reviewed retained source pack

Private output only under the §0.5 root. Bind all bytes by exact path and SHA-256 in the signed closed artifact inventory:

- [ ] `source_startup_policy`: explicit fresh-once initialization, exact path start, per-leg AUTHORIZED lifecycle, paper capital matching each adapter constructor, and cap80 request allocations. No defaulted field.
- [ ] `source_calendar` + `source_calendar_review`: panel-derived expected dates, deadlines, closures/denials, exact coverage/tail state and no `UNKNOWN` row. Do not treat deployment permission or the bounded forward calendar as historical coverage.
- [ ] `population_index` + `population_index_review`: exact FULL/H1/H2 chronological partition, expected exclusions, per-slot provenance and source binding to panels, ports, runtime settings and source-calendar hash.
- [ ] `schedule_execution_evidence` + `schedule_execution_evidence_review`: exact ratified bracket schema and source binding for R1/R2. This is a model convention, not observed source-instant history; label it accordingly.
- [ ] `cost_model`: exact accepted per-symbol cost terms, with no account-private amount and no reuse of a test fixture as evidence.
- [ ] Assemble a successor OPERATOR contract whose artifact inventory includes the eight roles and exact digests. The coordinator reviews the exact canonical bytes; the operator signs those exact bytes through the existing detached-approval ceremony. No agent signs or substitutes a test key. Validate the resulting contract and reviews through the existing parsers before replay.

### Task 4 — Verify P7 on real retained inputs and return

- [ ] Bind the accepted seven-bundle Step-3/Step-6 evidence for protected sizes and ORB adds-off by exact identity. Re-run parity only for a moved consumer or unbound accepted byte; do not recollect exports.
- [ ] Build the source through `ProductionSource.build(contract, artifact_root=...)`, then run `replay_bracket` on a retained real path containing at least one consumed intrabar schedule split. Flat/unused schedule evidence is not the acceptance example.
- [ ] For one real bar-level day, independently recompute opening equity, every fill/cost/mark, minimum excursion and closing P&L for both R1 and R2. Record private values privately; the public return carries hashes and equality/verdict labels only.
- [ ] Confirm each run's emitted `intraday_low` entries are unscaled excursions `<= 0`, have the exact horizon, and are passed with that run's own daily P&L. Do not call the statistical screen.
- [ ] Obtain one separate-session refute-first review covering the bracket contract, real-byte bindings, source pack, hand recompute and private/public boundary. Fixes receive focused re-review.
- [ ] Update §7 with the disposition. The coordinator—not the executor—updates the parent T00 step-1 verdict after reviewing the return.

**Tracked files authorized:**

- Modify: `ops/c1_rail/qualification/production_source.py`
- Modify: `ops/c1_rail/qualification/replay.py`
- Modify if the frozen interface requires the immutable types only: `ops/c1_rail/qualification/model.py`
- Test: `tests/ops/qualification/test_production_source.py`
- Test: `tests/ops/qualification/test_replay.py`
- Test if runner wiring is affected but no screen semantics change: `tests/ops/qualification/test_runner.py`
- Test: `tests/ops/test_book_adapters_parity.py`
- Return record: this file, §7 only

A needed tracked edit outside this list is a scope conflict and returns to the coordinator. Private artifact bytes and the corrected ignored port are not committed.

## 4. Hypothesis and mechanical verdict

**H:** candidate 3′ is a faithful P7 producer when supplied with the exact accepted private ports/panels/settings and the ratified two-run bracket through a reviewed closed source pack.

**FALSIFIED / P7 NOT MET:** any required byte or review is absent/mismatched; any source date remains UNKNOWN; either bracket run cannot complete; R1/R2 share mutable state or one run's low/P&L; the hand recompute differs; protected/adds-off parity is unbound; or a schedule-consuming real path needs an unratified state rule.

**RESOLVED / P7 MET:** all required bytes and reviews bind exactly, both independent runs complete on the real retained path, their own P&L/low pairs equal the hand recompute, and every acceptance case in §2 passes at the tested stable revision.

No GO-evidence or NO-GO-evidence verdict exists in this packet.

## 5. Verification and evidence

Run project Python only through the checkout's launcher, after `./fp.ps1 doctor`:

```powershell
./fp.ps1 --workers 2 python -m pytest tests/ops/qualification/test_production_source.py tests/ops/qualification/test_replay.py tests/ops/qualification/test_runner.py tests/ops/qualification/test_panel.py tests/ops/qualification/test_cost_schedule_validation.py tests/ops/test_book_adapters_parity.py -q
./fp.ps1 check
```

Before each recorded acceptance run, keep source and Git state unchanged. Report:

- command, validated interpreter, HEAD and working-tree state;
- `.cache/fp-verification/<run>/record.json` for every launcher pytest/check run;
- `status: completed`, zero exit, `source_stable: true`, complete capture and expected reports;
- exact private artifact/port/panel hashes without private contents;
- the R1/R2 real-path evidence digest and hand-recompute equality labels;
- independent-review identity and disposition;
- `git diff --check`, `git status --short`, and `git ls-files` evidence that no private artifact or ignored port entered the patch.

Focused tests passing does not permit describing the complete repository gate suite as passing if `check` reports a pre-existing or new failure.

## 6. Status taxonomy and forbidden work

**Gate verdict:** `RESOLVED` means P7 MET; `FALSIFIED` means P7 NOT MET; `AMBIGUOUS` is not acceptance and returns as `NEEDS_CONTEXT` with the unresolved fact.

Return exactly one:

- `DONE` — P7 MET under §4 with all §5 evidence.
- `DONE_WITH_CONCERNS` — the bounded implementation is complete but a named non-P7 concern remains; P7 is scored honestly.
- `NEEDS_CONTEXT` — a missing identity, source fact, reservation-only ruling or interface conflict prevents safe continuation.
- `BLOCKED — <reason>` — the same blocking condition has met the governing blocked threshold; cite the repeated evidence.

**Forbidden:** T00 step-2 pre-registration; any screen or Monte Carlo run; a GO/NO-GO investment verdict; changing 1%/0.40, sizing, lifecycle, capacity, takeover or firm rules; editing `core/dd_protection.py`; reconstructing private ports or Pine; accepting `c81aa59c…`; overwriting the primary active port root; agent signing or test-key substitution for the OPERATOR contract; provider signup/feed purchase/spend; account or broker access; deployment, activation, arming or orders; treating a synthetic fixture as real evidence; publishing private strategy bytes, account figures or path results.

## 7. Executor return

### Task 1 checkpoint — returned and accepted 2026-09-24

#### Task-1 disposition: `ACCEPTED — INTERFACE/FACT FREEZE COMPLETE`

General T00 step-1b authority already exists. The executor correctly stopped before production
implementation when the original tuple interface could not express the R2 empty
execution prefix. The coordinator accepts the input inventory, conflict finding,
reservation assessment and exact interface below. Candidate 3-prime P7 remains
NOT MET; Tasks 2–4 remain necessary. This disposition does not accept the red
tests as passing evidence and does not authorize T00 step 2.

#### Returned execution identity and evidence

- Task-1 worktree: `C:/Users/joshu/.codex/worktrees/t00-p7-task1/multi_firm_operations`;
  branch `codex/t00-p7-task1`; base `d1f3606861836579ef961e0a318293e4bb17d2e5`.
- Validated interpreter: `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`,
  CPython 3.13.2; `./fp.ps1 doctor` passed with 62 locked packages.
- Only the handoff return and additive TEST_ONLY changes in
  `tests/ops/qualification/test_replay.py` and
  `tests/ops/qualification/test_production_source.py` were made. No production
  source changed.
- Focused red record:
  `.cache/fp-verification/20260925T025834Z-0bd3d1fad162/record.json` — 16 failed,
  4 passed. Full selected-suite red record:
  `.cache/fp-verification/20260925T030028Z-9af5fedab66e/record.json` — 19 failed,
  164 passed, 12 skipped. All 19 failures are newly authored P7 interface tests;
  no pre-existing selected test failed. Both records are intentionally failed,
  source-stable red evidence, not acceptance. `./fp.ps1 check` was not run.
- The four admitted panels, Aegis/Vanguard/ORB ports, historical/runtime-effective
  settings, and retained corrected Striker were rehashed. The active original
  Striker `c81aa59c…` remained refused and untouched; the retained corrected source
  and ignored staged copy both matched `efd479b6…`. No private byte entered Git.
- The eight successor source roles remain unissued. No successor OPERATOR contract,
  production replay, hand recomputation, P7 score or independent review was produced.

#### Accepted interface

The exact public return types are the frozen dataclasses shown in Task 1:
`ScheduleExposure`, `ScheduleSplit` and `BracketReplayResult`. They live in
`qualification/model.py`; each is `@dataclass(frozen=True, slots=True)`. Boolean
values are rejected for the integer fields: `type(position) is int`,
`type(pending) is bool`, `type(reserved) is int`, and `reserved >= 0` are required.
`position` is signed broker-confirmed contracts, `pending` is whether the native
broker has any working order for the leg, and `reserved` is the non-negative ledger
contract count, never micro equivalents. `ScheduleSplit` requires exact `Bar`
instances for both segments and `type(prefix_executes) is bool`.

`ScheduleExecutionEvidence.split_bar(..., *, exposure=...)` and
`split_interval(..., *, exposure=...)` return one `ScheduleSplit`; a two-`Bar`
tuple is no longer accepted. There is no mutable exposure observer, no provider-owned
empty-prefix registry, and no post-split deletion/lookup side channel. Missing,
inactive or internally inconsistent exposure fails with `ReplayNeedsContext`.

`BookReplay._split(..., exposures=...) -> dict[str, ScheduleSplit]` remains the
single validator. For every leg it retains, without weakening, the current timestamp,
open/close continuity, high/low, volume aggregation, finite/valid OHLC, boundary-quote
and reduced-turn equality checks. It validates both returned bars even when
`prefix_executes` is false. It does not infer execution from timestamps, price
equality, volume or bar flatness.

The event order at a schedule boundary is fixed:

1. capture one immutable exposure snapshot for each supplied exposed leg;
2. obtain and validate its `ScheduleSplit`;
3. call `_process_segment` once with only the prefixes marked
   `prefix_executes=True`;
4. call `_schedule` at the selected boundary quote; and
5. retain every suffix as the remaining interval.

Thus R2 pending-only returns the ratified open-vertex prefix with
`prefix_executes=False`; cancellation occurs before any open-vertex fill. This is
required even when prefix and suffix have identical flat OHLC and zero volume. R1
pending-only returns its close/fill prefix with `prefix_executes=True`. Position-only
and position-plus-pending branches execute their selected prefix in both runs; the
position rule wins when both position and pending exposure exist.

For a subsequent boundary in the same source bar, the provider splits only the
current retained suffix. Exposure is captured again **after** the preceding prefix
processing and scheduled action, so cancellation, fills, flattening and reservation
release from the earlier boundary are visible. The second result is validated and
aggregated against that current suffix, not the original full bar. Its boundary quote
remains occurrence/run-local; repeated source dates cannot reuse a prior occurrence's
exposure-dependent split. Original adapter `on_bar` processing still occurs exactly
once after the completed source bar.

`ScheduleExecutionBracket.for_run` accepts only `R1` or `R2` and creates a fresh
run-local provider. `ProductionSource.replay_bracket(path)` returns exactly
`BracketReplayResult(r1: ReplayResult, r2: ReplayResult)` and constructs separate
loaders, adapters, brokers, ledgers, cash/account state and protection clocks. It
does not combine one run's P&L with the other's `intraday_low`, add a default
single-run path, or invoke the statistical screen.

#### Reservation invariant assessment

The native replay supports the invariant at each schedule callback:
`reserved[leg]` equals the still-outstanding admitted entry/add quantity, and a
positive reservation has a corresponding broker-pending order. `_admit` reserves and
records an order, and its caller submits synchronously before another schedule event;
the emulator then queues, fills or terminally rejects it. `_feedback` converts fills
to confirmed capacity and releases cancellation/rejection remainders. Native takeover
cancel/flatten is synchronous as well. Four planted cases—THIS_CLOSE, NEXT_OPEN and
two resting-stop placements—satisfied reservation/order-sum and
reservation-implies-pending at schedule callbacks.

That is a code argument plus bounded native-broker evidence, not a guarantee for
arbitrary injected brokers. The implementation must therefore check it at exposure
capture. `reserved > 0 and pending is False` is an inconsistent reservation-only
state and raises `ReplayNeedsContext`; it never selects R1 or R2. A pending-only leg
with `position == 0`, `pending is True` and a valid reservation remains the intended
pending-only branch. The tests must keep both the native invariant cases and the
defensive refusal.

#### Required test update before green implementation

The Task-1 test diffs were written against the pre-freeze proposal and do not yet
assert the explicit `ScheduleSplit.prefix_executes` contract. Before production
implementation, update them so they fail for the missing frozen behavior and cover:

1. exact frozen dataclass fields, immutability, type validation and method return
   types, including refusal of legacy two-`Bar` tuples and side-channel APIs;
2. R1/R2 long, short, pending-only and position-plus-pending choices;
3. R2 pending-only cancellation before an open-vertex fill on both ordinary bars and
   a flat zero-volume bar whose split OHLC cannot reveal an empty prefix;
4. `_split` aggregation, boundary and reduced-turn rejection unchanged, including at
   least 20,000 generated bars plus tie/flat/reduced-turn degeneracies;
5. two same-bar schedule boundaries proving that the second split receives the first
   split's suffix and a fresh post-action exposure snapshot;
6. reservation/order-sum, reservation-implies-pending and reservation-only refusal;
7. one adapter bar call, unchanged costs/signals, occurrence-local quotes and fully
   independent fresh R1/R2 engines/results.

Record that revised suite failing for missing implementation before making it green.
Task 2 may then implement only the accepted interface and authorized files. A need to
change these semantics, weaken `_split`, share R1/R2 state, or edit outside §3 returns
to the coordinator.

**Authorized continuation boundary:** resume at **Task 2**, then Tasks 3–4, solely
to close candidate 3-prime P7 under this step-1b packet. Return at the existing
identity/scope checkpoints and at final P7 scoring. No T00 step 2, screen, Monte
Carlo, provider/account action, deployment, activation, arm or order action is
authorized or occurred in Task 1.

### Task 2 return — 2026-09-29 (escalation lane, Claude)

#### Status: `DONE` for Task 2 — implementation returned for coordinator review; candidate 3-prime P7 remains NOT MET

GLM hit its iteration cap twice on this ticket, so it moved to the escalation lane and restarted
clean. GLM's draft was treated as unreviewed input. Its legacy-tuple compatibility shim and its
`observe_exposure` call were dropped.

The first return was `NEEDS_CONTEXT`: the frozen refusal of tuples and side channels broke
`bracket.py` and `benchmark.py`, and a `production_source → bracket` import broke the execution
closure. The coordinator's ruling of 2026-09-29 was (a) PORT, don't retire, with the constraints
applied below.

**Merge hold:** `execution/compute.py` and `part_a.py` on S5's branch import these modules. This
branch is not proposed for merge until S5 merges. It then rebases onto post-S5 main and
re-verifies. No PR has been opened.

- **Branch:** `claude/t00-task2-bracket`.
  - Base: `028c5ce`.
  - Red-test commit: `b98e0c1`.
  - Implementation commit: `92d9ecd`.
  - This §7 entry follows as a docs-only commit.
- **Files** (`git diff --stat 028c5ce..92d9ecd`):

  | File | Change |
  |---|---|
  | `model.py` | +50 |
  | `production_source.py` | 188 lines changed |
  | `replay.py` | 76 lines changed |
  | `bracket.py` | 113 lines changed |
  | `benchmark.py` | 5 lines changed |
  | `test_replay.py` | +456 |
  | `test_production_source.py` | +235 |
  | `test_bracket.py` | 18 lines changed |

  The first five are under `ops/c1_rail/qualification/`; the test files are under
  `tests/ops/qualification/`. `git diff --check` is clean. No private byte, port or artifact was
  touched.
- **Interpreter:** `C:/Users/joshu/multi_firm_operations/tmp/ops-env/Scripts/python.exe`,
  CPython 3.13.2. `fp.py doctor` passed with 62 locked packages.
- **Red record** (base production code at `028c5ce` plus the new tests; two test files):
  `.cache/fp-verification/20260930T011841Z-d2507d353f00/record.json`, rerun as
  `20260930T012039Z-b63179b87c4b`.
  - `status: failed`, exit 1, `source_stable: true`. 86 failed and 63 passed; there were no
    collection errors.
  - New tests failed on ImportError of the frozen names, or on `TypeError` from the legacy
    `_split`/`split_bar` signatures. Base code cannot pass an exposure at all.
  - Existing tests failed only where their fixtures were migrated to `ScheduleSplit` plus
    `exposure`.
- **Green, focused:** `20260930T011407Z-d2a62cec4f25`. Completed, exit 0, stable; 149 passed.
- **Green, full suite** (`tests/ops/qualification` plus `tests/ops/test_book_adapters_parity.py`,
  `--workers 2`): `20260930T023603Z-e3f0ef4f5d7b`.
  - Completed, exit 0, stable. 1707 passed and 13 skipped.
  - Skip reasons: 1 Linux-only SIGSTOP ordering case; 4 private ports absent from the worktree;
    8 `effective_inputs.json` absent from the port root.
  - This run covers the runner, panel and cost/schedule suites.
- **`fp.py check`:** `20260930T034404Z-3c0801d691ae`. Completed, exit 0, stable.

**Test → §7 "Required test update" item** (case names carry the item number):

| Item | Tests |
|---|---|
| 1 | `test_production_source.py`: `test_t2_item1_frozen_types_have_exact_fields_immutability_and_validation`, `…_for_run_accepts_only_exact_ids_and_issues_fresh_providers`, `…_retained_evidence_returns_executing_schedule_split`; `test_replay.py`: `test_t2_item1_split_refuses_legacy_two_bar_tuple`, `…_refuses_positional_legacy_provider`, `…_refuses_side_channel_providers[×2]`, `…_requires_a_captured_exposure_for_every_leg[×3]`, `…_returns_one_schedule_split_per_leg` |
| 2 | `test_t2_item2_provider_places_the_ratified_two_run_table`; `test_t2_item2_held_long_and_short_flatten_at_each_runs_vertex[×2]`; `test_t2_item2_position_plus_pending_follows_position_rule_and_prefix_reach` |
| 3 | `test_t2_item3_r2_pending_only_cancels_before_gap_open_fill_on_ordinary_bar`; `…_cancels_on_flat_zero_volume_bar`; `…_non_executing_prefix_is_refused_for_a_position_leg` |
| 4 | `test_t2_item4_frozen_splits_of_20000_generated_bars_pass_split_unchanged` (20,008 bars × 6 run/exposure cases, including tie, flat and zero-volume degeneracies); `test_t2_item4_split_rejections_unchanged_even_when_prefix_does_not_execute[True/False]` |
| 5 | `test_t2_item5_second_same_bar_boundary_splits_retained_suffix_with_fresh_exposure`; `test_t2_item5_provider_splits_the_current_suffix_and_stays_occurrence_local` |
| 6 | `test_t2_item6_native_states_satisfy_reservation_invariants_at_schedule_callbacks[×10]` (THIS_CLOSE, NEXT_OPEN, two resting stops and position plus add, under R1 and R2); `test_t2_item6_reservation_only_state_is_refused_before_any_split[×2]`; `test_t2_item6_provider_refuses_missing_inactive_and_reservation_only_exposure` |
| 7 | `test_t2_item7_one_bar_call_unchanged_costs_and_occurrence_local_quotes`; `test_t2_item7_replay_bracket_builds_two_fresh_engines_with_separate_results` (TEST_ONLY composition fixture holding ORB through the 15:55 intrabar flatten) |

**Order-sum: enforced at capture (coordinator ruling 2026-09-29).** The ruling reads "it" in
"The implementation must therefore check it at exposure capture" as the whole invariant:
"`reserved[leg]` equals the still-outstanding admitted entry/add quantity, and a positive
reservation has a corresponding broker-pending order". Native evidence is "not a guarantee for
arbitrary injected brokers", so both halves are checked at capture.

- **Commit `83b82d2`** (new; `92d9ecd` and `b42510c` are not rewritten). The existing
  reservation-only refusal is kept. `_capture_exposure` also raises `ReplayNeedsContext` naming
  the leg and both values when the ledger reservation differs from the outstanding admitted
  entry/add quantity.
- **Test:** `test_replay.py::test_t2_item6_reservation_order_sum_mismatch_is_refused_before_any_split[+1/-1]`.
  A resting ORB entry keeps its pending order while the ledger reservation is moved above or
  below its outstanding quantity. In both R1 and R2 the run is refused before any split. The
  provider records no split call and no placement, so neither run selects a branch.
- **Red on `92d9ecd` code:** `.cache/fp-verification/20260930T034858Z-9c3a527f991e/record.json`.
  Failed, exit 1, stable; 2 failed.
  - For +1, base code split the leg, and a later capture then raised the reservation-only
    refusal.
  - For −1, the cutoff cancel raised `CapacityError: release 1 exceeds reservation 0`.
- **Green, two test files:** `20260930T034951Z-0104597a0fcf`. Completed, exit 0, stable;
  151 passed.
- **Green, full suite** (`tests/ops/qualification` plus `tests/ops/test_book_adapters_parity.py`,
  `--workers 2`, at `83b82d2`): `20260930T035237Z-2052d59debde`. Completed, exit 0, stable;
  1709 passed and 13 skipped, with the same skip reasons as above.
- **`fp.py check` at `83b82d2`:** `20260930T050532Z-8eea6d6c7076`. Completed, exit 0, stable.

Item 6 in the test table above also covers this new test.

**Additions and review items:**

- **Accepted addition (ruling 4):** a fail-closed guard. The replay refuses a non-executing
  prefix unless the leg is pending-only and the prefix has one price.
- **Task 4 review item (ruling 5):** `replay_bracket` records a run's `ReplayDeadlineFailure` as
  that run's `ReplayResult`, following `run_bracket`.
- **Task 3 open item (ruling 6):** run-local providers ignore reviewed intrabar split rows.
  Provider precedence is placement, then reviewed quote, then ratified reading 3.

**Verbatim move (ruling 3).** `vertex_split` and `placement` moved from `bracket.py` into
`production_source.py`, and `bracket.py` re-exports them. SHA-256 of each `ast` source segment,
for base `bracket.py@028c5ce` and head `production_source.py`:

| Function | SHA-256 |
|---|---|
| `vertex_split` | `ffd9a5fda55aa086c08e33bc176c09a281e66aaa6016f5503e5ae796c3f24fba` (both) |
| `placement` | `432a65a510bf7c77a0f029e7d10affab5f83cfbd0986a674e33041abc40df52a` (both) |

`production_source` gains no new import edge: it already imported `.replay`, and `.bracket` is
not imported. `test_execution_closure.py` passes unchanged, and the policy was not edited.

**`bracket.py` port (ruling 1).** `BracketScheduleQuotes` delegates splits and prices to a fresh
`ScheduleExecutionBracket.for_run` provider over empty reviewed evidence. It adds only its
`Placement` record, and fails closed if the record disagrees with the provider. It no longer has
`observe_exposure` or `prefix_is_empty`. `run_bracket` is unchanged.

In `test_bracket.py` only interface shape changed; no expected value changed:

| Node | Old call shape | New call shape |
|---|---|---|
| module import | `PathOutcome, SessionSchedule` | adds `ScheduleExposure, ScheduleSplit` |
| `test_every_vertex_split_passes_the_engine_validator_unchanged` (via `_validate`) | stub `split_bar = lambda *args: (prefix, suffix)`; `left, right = BookReplay._split(stub, None, pb, bars, INSTANT)`; assert `(left['leg'], right['leg'])` | stub `lambda *args, exposure: ScheduleSplit(prefix, suffix, True)`; `BookReplay._split(..., INSTANT, {'leg': ScheduleExposure(1, False, 0)})['leg']`; assert `(split.prefix, split.suffix)` |
| `test_placement_refuses_without_observed_exposure` | `split_bar(session, pb, INSTANT, 'leg')` twice, with `observe_exposure(session, INSTANT - 1 min, {'leg': 1})` between | `split_bar(session, pb, INSTANT, 'leg', exposure=None)` twice; `observe_exposure` removed. The stale-instant sub-case has no analogue once no observer state exists, so the second block now repeats the missing-exposure refusal. |
| `test_interval_split_places_on_the_remaining_path` | `observe_exposure(session, INSTANT, {'leg': 1})`; `prefix, suffix = split_interval(session, None, remaining, INSTANT, 'leg')` | `split = split_interval(..., exposure=ScheduleExposure(1, False, 0))`; `prefix, suffix = split.prefix, split.suffix` |

All other `test_bracket.py` nodes, including every engine-level R1/R2 case, are unchanged and
pass on the ported class.

**`benchmark.py` equivalence (ruling 2).** `SyntheticQuotes.split_bar` now takes keyword-only
`exposure` and returns `ScheduleSplit(original, flat suffix, True)`. A pytest plugin captured
every call's prefix and suffix while running `test_benchmark`, `test_benchmark_part_a`,
`test_provider` and `test_seed_probability_vectors`. Each bar was encoded as `ts.isoformat()`
plus `float.hex` OHLCV.

| Tree | Tests | Calls | Log SHA-256 |
|---|---|---|---|
| Base: `028c5ce` production files | 76 passed | 1135 (9 nodes) | `5b8accbfac8b4bb2f9a5d95881de6f91762c9b6cbfbe1a42cc28b7267f9b9b17` |
| Head | 76 passed | 1135 (9 nodes) | `5b8accbfac8b4bb2f9a5d95881de6f91762c9b6cbfbe1a42cc28b7267f9b9b17` |

The two logs are byte-identical (`cmp`). The only difference is the flag: head records
`prefix_executes=True`, base records a legacy tuple. The capture script and both logs are in the
executor scratchpad and are not committed.

**Remaining:** Tasks 3–4 (retained source pack, signed OPERATOR contract, real-input R1/R2 replay,
hand recompute, independent review). No T00 step 2, screen, MC, real replay or private-input run
occurred.

### Tasks 3–4 Checkpoint 1 return — 2026-09-30 (local Claude, Opus)

#### Status: `NEEDS_CONTEXT`. Task 3 did not start and nothing was written.

**Setup.** The executor worktree is `.claude/worktrees/t00-p7-tasks-3-4`, on `claude/t00-p7-tasks-3-4` at `34f5b12` with a clean tree.
- `fp.ps1 doctor` passed on CPython 3.13.2 with 62 locked packages.
- `check_brief --type handoff` on the [dispatch card](2026-09-30-t00-p7-tasks-3-4-dispatch.md) reported 0 HARD and 0 WARN violations.

**§0.1 reverified; all MATCH.**
- The six `SHA256SUMS` panel rows pass, and the Aegis attested-prefix panel is `8ae083d0…`.
- The Aegis, Vanguard and ORB ports are at their pins.
- The corrected Striker `efd479b6…` matches in both the Step 3 root and the staged copy. The active Striker is still the refused `c81aa59c…`.
- The historical settings are `66406dee…`, and D19 is `2698f268…`.

**Blocker 1 (plan conflict).** `ProductionSource.build` accepts only a `ValidatedFrozenContract` from `validate_frozen_contract` under a signed production trust domain.
- That contract's role set is fixed at the full `REQUIRED_ARTIFACT_ROLES` plus every production code role (`contract.py:509`).
- It also requires the complete F1 qualification freeze: horizons, six stage specs, budget, decision rules and result plan.
- Several of those values amount to T00 step-2 pre-registration, which §6 forbids. A narrower route needs files outside §3.

**Blocker 2 (missing fact).** OPEN `source_calendar` rows need per-leg venue deadlines bound to a retained role. D19 was accepted for early-close membership only.

#### Operator rulings 2026-09-30

Joshua gave these on 2026-09-30 by structured answer in the coordinating session. The coordinator relayed them, and they are recorded verbatim:

> **Ruling 1, the contract. Option (b) chosen: "Source-only contract".** Design a separately signed source-only contract class that `ProductionSource.build` accepts. It is new trust-domain / authority code, so it is designed and reviewed before any of it is implemented. T00 stays in parallel with S5 → T06.
>
> **Ruling 2, the deadlines. The candidate reading is accepted, with residuals named.**
> - Date membership is panel-derived (R2).
> - A D19 `venue_flat_dates` date gets V = 12:59 ET for all legs. Every other date gets V = 16:45 ET (Tradeify's blanket account-level rule).
> - The facts are bound through the `calendar_producer` role.
> - Two residuals are carried by name: the 2025-11-28 Globex outage, and possible ad-hoc closures after 2026-05-28. The second is the non-conservative one.
> - If the P7 hand-recompute day is chosen, it must not be a residual date.

The coordinator's sequencing is [card §8.1](2026-09-30-t00-p7-tasks-3-4-dispatch.md#81--coordinator-sequencing-after-the-checkpoint-1-return-2026-09-30). The source-only design (Phase A) and the Task 3 source pack proceed in parallel. Signing, implementation and Task 4 wait for the accepted design.

#### Coordinator review 2026-09-30

The coordinator reviewed the first Task 3 source pack and ruled as follows. The executor recorded these rulings.

**Truncated tail, 2026-09-03: option (a) now, option (b) in the design.**
- The date is marked `policy_denied` with the reason "panel truncated at interval end: 9 slots 18:00–20:00 ET, no active-window bar; data truncation, not a venue denial". This is a stand-in for a missing typed disposition, not a venue fact.
- Option (c), a no-RTH pseudo-day kept in FULL, is rejected.
- The design adds a typed truncation disposition, which retires the stand-in.
- The 2022-09-01 head session keeps its intact RTH, and its missing 18:00–19:45 ET slots are named.

**Executor decisions:**

| Decision | Ruling |
|---|---|
| Paper capital | ACCEPTED as bound. Aegis, Striker and Vanguard use their constructor values, equal to the Step 3 emulator initial. ORB uses the hash-bound O-N emulator initial, and O-N equals O-P. |
| `path_start_date` | ACCEPTED as a PROPOSED path-label origin. It appears as an explicit field in the signed contract bytes. |
| Zero schedule rows | ACCEPTED. The Task 2 carry-forward is closed as moot. Task 4 names the real path and instant of a consumed vertex-placed split. |
| Review companions | CORRECTION: producer-written `ACCEPTED` companions are self-certification, so they are UNREVIEWED drafts and must not be cited as reviews. Companions are reviewer-authored after review, and the producer emits templates only. The coordinator reviews the regenerated bytes and produces the companions. |

**Regenerated pack.** The first pack (`task3-source-pack/`, inventory in place) stays immutable and is superseded. The r2 pack is in `task3-source-pack-r2/` under the private root; hashes only are given here.
- Its `inventory.json` SHA-256 is `190f8dd96a3399efd468b23989753292c4882a34a0b7c7a2dc3c5020dbab9d01`, and its producer SHA-256 is `a9a5c262…4a87`, run at code `48bf30a`.
- Every parser passed, with the templates checked for shape only.
- Counts: 1,036 source dates, of which 40 have V 12:59 ET, 995 have V 16:45 ET and one is `policy_denied`; none is UNKNOWN. FULL has 997 sessions (H1 499, H2 498), with 39 exclusions: 38 `missing_active_bar` and one `policy_denied`.

**Conflict noted.** The v1 review companion schema is closed, so the required statements cannot live inside v1 companion bytes. They are in the r2 `reviewer-notes.json`. The design's v2 companion adds `reviewer`, `reviewed_at` and `notes`.

#### Source-only contract design: review path and acceptance (2026-09-30)

The design is [`docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md`](../../superpowers/specs/2026-09-30-t00-source-only-contract-design.md). Each revision is additive and carries its own changes table.

| Revision | Commit | Review and outcome |
|---|---|---|
| 1 | `48bf30a` | Coordinator: REVISE, with two BLOCKING (a caller-supplied trust root; P7 not bound to code) and four required changes |
| 1 → typed truncation, reviewer-authored companions | `c9742f0` | The coordinator's Task 3 review rulings |
| 2 | `7e0c49c` | Codex (local): seven findings |
| 3 | `e6fad26` | Codex cloud `task_e_6abd361aed38832c9c9f2b847e08c267`: NOT RESOLVED, with two new P1s |
| 4 | `f1cfa4f`, `a6ab1e2` | Operator-approved scope simplification. Codex `task_e_6abd41a3f030832cb583866d33d63406`: cuts 1 and 4 resolved, three new P1s |
| 4.1 | `35f233e` | Three binding requirements (operator "yes"). Codex `task_e_6abd4caf4cb0832c9b6d12ea9b58d3a4`: record authentication and stale inputs RESOLVED; the pre-hook P1 remained because `-I` does not imply `-S` |
| 4.2 | this revision | The `-S` correction and test A23 |

**Operator acceptance, 2026-09-30 ("option 1").** Design ACCEPTED 2026-09-30 by the operator (option 1), on revision 4.2. The final Codex review, `task_e_6abd4caf4cb0832c9b6d12ea9b58d3a4`, resolved the record-authentication and stale-input P1s, and the pre-hook P1 is closed by the `-S` fix and A23 without a further design review. This is an explicit operator exception to the pre-committed stop rule, taken because the finding was a factual error with a one-flag correction.

**Next.**
1. A coordinator card amendment admits the implementation files.
2. The implementation proceeds with fail-first tests.
3. Codex reviews the code before any merge.
4. The merge hold until S5 merges still stands.

No code starts before the amendment.

**Revision 4.3.** 4.3 correction accepted by the operator 2026-09-30 (implementation conflict: production_source imports runner/mc.simulation).
- The refusal list is `part_a`, `bracket`, `benchmark`, `benchmark_part_a`, `production`, `orchestration`, `result_adjudication`, `seal` and `execution.*`, matched by exact name or package prefix.
- `runner` and `mc.simulation` load with their kernel entry points stubbed (`P7_FORBIDDEN_CALL`), with an identity check at record time.

The spec records this in its revision 4.3 section.

## 10. Audit hooks

```powershell
# Rule-0 distinction: expect the historical anchor and selected-book candidate to remain different.
rg -n 'DD_TRIGGER = 0.015|DD_SCALE = 0.40' core/dd_protection.py
rg -n 'CANDIDATE_TRIGGER = "0.01"|CANDIDATE_SCALE = "0.40"' ops/c1_rail/book_policy.py

# Exact corrected Striker pin and stale-byte refusal remain present.
rg -n 'c81aa59c|efd479b6' ops/c1_signal_daemon/book_adapters.py

# The source factory still requires all eight reviewed roles.
rg -n 'source_startup_policy.*source_calendar.*source_calendar_review.*population_index.*population_index_review' ops/c1_rail/qualification/production_source.py
rg -n 'schedule_execution_evidence.*schedule_execution_evidence_review.*cost_model' ops/c1_rail/qualification/production_source.py

# Private bytes must not enter version control.
git ls-files ops/c1_signal_daemon/ports lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts
git diff --check
git status --short
```
