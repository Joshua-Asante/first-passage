# Native implementation ↔ research comparison contract

**Status:** v1 interface specification, 2026-10-18. Candidate bindings await portfolio selection; no native comparison has run.
**Owner:** Deployment Coordinator.

## Comparison boundary

Compare the selected research reference with NinjaScript on frozen, identical inputs. Bind source/configuration digests, data/calendar, initialization, runtime/build, execution mode and comparison policy before scoring. A Python reference needs its source-equivalence evidence and limitations attached. Python/emulator agreement alone establishes no NinjaScript agreement.

Keep three results separate:

1. **Input equivalence:** bars, sessions, warm-up and external account/event inputs agree.
2. **Decision equivalence:** signals, admissions, quantities, exits and state transitions agree under controlled execution feedback.
3. **Execution equivalence:** independently produced native orders, callbacks, fills and resulting state agree under the bound execution model.

Results 2–3 require actual NinjaScript-generated traces. Historical, replay/simulation and connected execution are separate scopes; success in one does not certify another. OHLC path models cannot establish exchange fills. Data coverage and session legality retain [separate verdicts](../notes/2026-09-15-calendar-parity-separation-amendment.md#3-separate-verdicts-and-acceptance-checks).

## Required comparisons

| Surface | Freeze and compare |
|---|---|
| Bars and sessions | Contract/roll/adjustment, bar type/period/series, raw timestamp convention and UTC open/close, session timezone/calendar/trading-date key. Cover overnight, DST, holidays/early closes, gaps, duplicates and partial bars. Compare inputs first; never shift traces to hide a bar lag. |
| Evaluation timing | Bar-close/intrabar evaluation, series/event order, order creation versus eligible execution, same-close/next-open behavior, flatten decision/execution deadlines and historical-to-realtime transition. |
| Warm-up | History start, indicator seeds, readiness predicate/first eligible event, session resets and carried state. Compare readiness; exclude only the frozen unscored prefix. Missing history blocks comparison. Restarts must match uninterrupted continuation. |
| Signals | Every evaluation including no-action/suppression reasons; side, entry/add/exit/flatten, trigger/limit, expiry, occurrence, parent/base fill and lot scope. Preserve order and multiplicity. |
| Sizing | Separate strategy-normal, account-admitted and executed quantity. Bind account state, allocation, lifecycle/protection, instrument units, stop/risk inputs, capacity/margin and confirmed base fills. Compare arithmetic, rounding/clamping order, refusals and commands, including integer boundaries, invalid inputs and partial-base-fill adds. Legacy constants/rescaling are not inherited. |
| Exits | Per-lot stops/targets/trailing state and activation, amendments/OCO, partial exits, reversals, session flatten and protection after rejection/cancellation. Bind simultaneous stop/target precedence; unknown intrabar order cannot prove it. Retain terminal pending orders/open lots. |
| Order events | Intent → admission → submit/change/cancel → acknowledgement/working → partial/full fill, reject or cancel, including races. Preserve callback arrival order and IDs; update position-dependent state from confirmed outcomes. Include duplicate/delayed feedback, reconnect/restart and account/position reconciliation. |

Equal relevant inputs require the same non-quantity decision prefix. Any authorized size-only difference needs a demonstrated causal transition; it cannot excuse an unrelated wrong exit. Each engine computes its own admissions, commands and feedback state. Reference refusals/checkpoints cannot be imported to erase divergence.

## Reusable test interface

This is an offline interface specification. The machine-readable [case envelope](native-research-comparison-case.schema.json) binds artifacts; it does not implement exporters, replay or semantic validation.

```text
run(profile, inputs, policy, implementation_binding) -> trace artifact
normalize(raw_trace, frozen_mapping) -> canonical JSONL artifact
compare(completed_case_envelope) -> report artifact
```

The reference custodian produces reference traces/source-equivalence evidence; the native implementer produces NinjaScript build/run identity and raw/canonical traces. Assemble the completed envelope after both runs. The future offline comparator consumes it; the Coordinator accepts combined results. Instrumentation and comparator implementation remain future handoffs.

The case envelope requires digest-bound artifacts for:

- **profile:** source/config/runtime, instrument/units, timing/session/warm-up, sizing/exits, execution/friction, restart and semantic state projection;
- **inputs:** ordered bar/tick/session/account/event history, warm-up/scored intervals, initial orders/lots/account state and terminal observation boundary;
- **policy:** exact fields, numeric tolerances with units/rationale, normalization, allowed callback partial order, required scenarios and coverage;
- **reference binding:** reference implementation/build/config, source-equivalence evidence, anchor identities and their coverage/limitations;
- **native binding:** NinjaScript source/assembly/config hashes, platform/build, mode, exporter version and run provenance;
- **reference/native traces:** raw and canonical artifacts, row counts and complete capture evidence. Store private artifacts in authorized custody; public envelopes contain sanitized locators/digests only.

Every canonical JSONL row has these fields:

```text
run_id, seq, event_id, cause_ids[], input_event_id,
event_time_utc, observed_time_utc, session_key, series_id, bar_id,
strategy_key, account_alias, kind, occurrence_key,
logical_order_key, native_order_id, execution_id,
payload, state_before, state_after
```

Use precise UTC timestamps, increasing capture `seq`, unique `event_id` and cross-engine `occurrence_key` (input event + strategy + role + ordinal). `cause_ids` links local predecessors. Logical order keys preserve parent/lot/OCO relationships; retain native IDs. Non-applicable fields are null. Prices/cash use finite decimal strings and profile units; contracts use integers. Unavailable indicators are tagged, never NaN.

`kind`: `input`, `readiness`, `decision`, `admission`, `command`, `order_event`, `checkpoint`, `terminal`. The profile defines payloads and sufficient state: consumed indicators/session/readiness, pending orders, lots/position, sizing/account and recovery state. Reject insufficient projections. Normalization may rename/convert units or timestamp conventions, never drop/merge/fabricate events. Callback differences need the frozen partial-order mapping, preserving raw arrival order and decision/feedback dependencies.

Run two explicit modes:

- **Controlled feedback:** both decision engines consume one frozen exogenous execution-event tape. Each command must satisfy the tape's logical order precondition before feedback; divergence stops that branch. This tests decisions, not native execution. An unavailable native injection seam is incomplete coverage.
- **Independent execution:** each engine consumes its own outcomes. Compare commands/outcomes/feedback under the bound model; never replace native outcomes with emulator outcomes. Incompatible models or insufficient tick/path resolution prevent execution parity and require a model-binding decision before rerun.

Reports contain artifact/run identities, per-surface/scenario status and coverage, missing/extra occurrences, all mismatch counts, first causal divergence with raw/canonical locators/state, terminal exposure/orders and limitations. Display limits cannot truncate counting. P&L/trade totals are secondary checks.

## Verdicts and acceptance cases

`PASS`: complete required coverage within frozen policy. `FAIL`: valid comparable inputs expose a violation. `INCOMPLETE`: absent/unbound/invalid evidence or unavailable capability. Aggregate precedence: FAIL, then INCOMPLETE, then PASS. Empty/no-trade runs establish only explicitly required no-action cases. No tolerance defaults, fuzzy timestamps, post-result widening or silent exclusions.

Before trusting the comparator, demonstrate these synthetic traces through the same interface:

| Input / transition | Required result |
|---|---|
| Identical valid traces, complete required coverage | PASS for that synthetic case only |
| Same completed ledger, signal shifted one evaluation or duplicate command | FAIL at the first differing occurrence |
| Readiness flips early, or session reset loses a pending exit | FAIL on readiness/state before any misleading trade match |
| Partial base fill → add; reject → later signal; cancel races with fill | Compare command preconditions, actual outcomes and independently updated state; mismatches FAIL |
| Restart with pending bracket/open lot | Restored continuation must equal uninterrupted continuation; missing capture/state is INCOMPLETE |
| Coarse bar touches both exit levels with no bound precedence/path evidence | Execution surface INCOMPLETE; no inferred fill ordering |
| Native trace absent but Python and emulator agree | Native comparison INCOMPLETE |

After portfolio selection, bind fixtures, tolerances, state/payload schemas, runtime modes and scenario applicability **before scoring**. Cover applicable session/readiness/sizing/exit/event/restart boundaries above; unsupported scenarios remain coverage gaps. Acceptance needs every required surface/scenario to pass on actual native captures. Live fill realism and operational readiness retain separate gates.

## Evidence reuse and limits

| Existing artifact | Reuse | Limit |
|---|---|---|
| [`book_protocol.py`](../../ops/c1_signal_daemon/book_protocol.py) | Intent/confirmed-feedback separation, per-fill scope and timing vocabulary | Fixed-book Python protocol; not a native exporter or universal timing policy |
| [`book_parity.py`](../../ops/c1_signal_daemon/book_parity.py) | Pinned export intake, missing/extra trade, quantity/price/net reconciliation | Completed-trade matching and filtered windows do not establish full event/state coverage; its tolerances and quantity scaling are not inherited |
| [`tv_broker_emulator.py`](../../ops/c1_signal_daemon/tv_broker_emulator.py), [synthetic tests](../../tests/ops/test_tv_broker_emulator.py) | Captured-TV-derived path, gap, timing, bracket and friction cases as expected-behavior candidates | TV-model/Python evidence; partial fills and most rejects are not modelled by this emulator |
| [Quantity-law tests](../../tests/ops/test_book_quantity_laws.py), [sizing-host reference tests](../../tests/ops/test_c1_sizing_host_reference.py) | Integer sizing/refusal/feedback boundary case designs | Historical policy and Python oracle scope; rebind the selected policy before native use |
| [Gen-2 results](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md), [mutation tests](../../tests/lab/test_q_filltax_1_parity_mutations.py) | Defect-detection patterns and positive control | Results explicitly distinguish synthetic harness discrimination from family anchor parity; neither proves NinjaScript agreement |

These are inspected sources, not fresh test results. Historical results need matching inputs/revisions/capture/scope and their original limitations.

## Bounded delivery record

**Selected outcome:** this comparison contract and reusable case interface, ready for later candidate binding.
**Prerequisites:** existing public parity interfaces/evidence inspected; portfolio, fixtures and tolerances deliberately unbound.
**Ownership:** Codex drafts and checks inline; Deployment Coordinator owns candidate binding and combined native acceptance.
**Verification:** inspect source links, parse case schema, review timing/readiness/partial-fill/restart and absent-native traces against verdict rules; record working-tree identity in the task return.
**Checkpoint:** return artifacts and verification to the current chat after specification review; budget three recoverable draft/review iterations.
**Return boundary:** delivery of the checked specification; native ports, exporters/comparator implementation, candidate fixtures/tolerances and scored runs require later bounded handoffs.
