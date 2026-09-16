# PR 409 Slice A ingress correction Implementation Plan

> **For agentic workers:** Execute with superpowers:executing-plans; use superpowers:subagent-driven-development when bounded delegation is useful and authorized. Preserve the behavioral contract and integration owner. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reject malformed market data and executable actions before downstream effects, and retain an honest durable incident without serializing invalid input as a valid payload.

**Architecture:** Keep the owner, runtime, protocol, and serializer. Add a pure shared validation boundary in the signal-daemon package, called by both runtime and account owner. Keep incident recording separate from canonical action serialization; preserve existing normalization and emulator behavior.

**Tech Stack:** Python 3.11-compatible code, dataclasses, SQLite, pytest; standard library only for the new runtime code.

**Spec:** [Approved bounded correction](../../spec/2026-09-16-pr409-bounded-execution-correction.md).

## Global Constraints

- Offline synthetic execution only; no production transport, deployment, arming, or trading.
- No strategy parameters, sizing laws, allocation constants, protection-tier constants, or calibration changes.
- No production resume or general-purpose incident recovery in this correction.
- Preserve immutable historical operation/fact identities and retained obligations.
- Preserve the Python 3.11 language floor and existing repository layer boundaries.
- Runtime regression tests must execute without private strategy inputs or optional signing dependencies.

## Integration contract and limits

Integration owner: coordinating implementer of PR 409. Baseline reviewed code is `fc7cdc7`, equivalent to `a9175a1` for ops/tests. Refresh head and inspect intervening changes before execution; do not discard collaborators' work.

This plan implements Slice A only. Protection ownership/evidence, occurrence identity, takeover phases, and activation/migration remain governed by Slices B-D. Completion here does not close all six findings or make PR 409 merge-ready.

Existing path: source.poll -> runtime.on_completed_bar -> record_partial_bar -> completed barrier -> adapter.on_bar -> action journal -> listener handle_book_action -> owner.dispatch -> reservation -> attempt -> SyntheticBroker.send. Direct owner callers bypass runtime and therefore require the same structural action validation. Existing serializers reject NaN before a durable incident; this is a failure, not validation success.

Proposed pure interface in `ops/c1_signal_daemon/book_validation.py`:

```python
@dataclass(frozen=True)
class InputViolation:
    code: str
    field: str

def validate_bar(bar: Bar) -> InputViolation | None: ...
def validate_action(action: Action) -> InputViolation | None: ...
```

These signatures are proposed, not existing. Return only bounded static codes/field paths, never the raw invalid value. Validators do not mutate/coerce inputs, quantize prices, access the database, or grant authority. Successful validation preserves the original semantic payload. Account-state ownership is deliberately not decided here. Numeric fields at this adapter/feed boundary accept only exact built-in int/float values, excluding bool; Fraction, Decimal, and numeric strings are rejected rather than serialized as strings. This does not change the separate BrokerFact ingress contract.

Proposed owner interface:

```python
def record_input_incident(self, incident_id: str, violation: InputViolation,
                          *, source: str, now: datetime) -> None: ...
```

Trusted callers supply incident identity from known session/boundary/action-ordinal context where available. Direct untrusted calls with no trustworthy occurrence use a newly generated diagnostic identity; never hash/serialize invalid action content to manufacture it. Persist the diagnostic and authority fence atomically under the serializer, then report the validation error after commit. Repeated stable incident identity with the same diagnostic is idempotent even if redelivered later; conflicting diagnostic identity is an identity fault. Do not raise from inside a transaction in a way that rolls the fence back.

If persistence fails, propagate the storage failure, abort the current batch/send, and latch local send suppression for that owner instance; it cannot resume using cached RUNNING state. A successful subsequent status read is not a clearing mechanism. The failure must not be reported as a durably recorded incident. Existing boot fencing remains authoritative for replacement instances.

## Task 1: Invalid input cannot mutate adapters or reach a send

**Files:**
- Create `ops/c1_signal_daemon/book_validation.py`.
- Modify `ops/c1_signal_daemon/book_runtime.py`, `ops/c1_signal_daemon/book_evaluate_loop.py`, and `ops/c1_rail/book_account_owner.py`.
- Create `tests/ops/test_book_ingress_validation.py`.
- Inspect `ops/c1_signal_daemon/book_protocol.py`, `feed.py`, and `tv_broker_emulator.py`; do not change their valid-input semantics.

**Rules:**

| Input | Required validation |
|---|---|
| Bar | Typed Bar; aware timestamp; OHLC finite exact built-in int/float excluding bool; volume of the same numeric types, finite and nonnegative; low <= open/close <= high. Existing freshness/session/sequence checks still apply. |
| Action envelope | Exact supported action shape; nonempty known leg identity; typed Side and FillTiming where applicable; supported kind/order type; valid identity strings; aware optional bar timestamp. |
| Quantity | Exact positive integer excluding bool for entry/add; exit/flat exact positive integer or None. Preserve adapter-normal versus admitted quantity distinction. |
| Stop trigger / supplied stop or limit | Finite positive exact built-in int/float executable price, excluding bool, Fraction, Decimal, and numeric strings. Preserve accepted off-tick values for existing normalization. |
| Bracket | Typed Bracket or allowed None; supplied trailing parameters paired exact integers, activation >= 0 and offset > 0. Empty defined bracket is not silently interpreted as working protection; state-dependent authority belongs to Slice B. |
| Scope | None or tuple of unique nonempty string identities. Empty scope must remain an explicit no-target outcome, never expand to all fills. Ownership/liveness checks belong to Slice B. |
| Other fields | Validate serialized field types: optional OCA identity, textual reason, finite nonnegative exact built-in int/float stop distance excluding bool. Existing leg-specific sizing requirements remain in their owner. |

Do not introduce a universal bar-price tick-alignment requirement, coerce numeric strings, reject legitimate off-tick brackets, move rounding before stop-crossing evaluation, or use validation to infer protection health.

- [x] Add failing integration tests before writing validators. Representative tests using existing synthetic fixtures:

```python
@pytest.mark.parametrize("changes", [
    {"high": 90, "low": 110}, {"close": float("nan")},
    {"open": float("inf")}, {"volume": -1}, {"close": True},
])
def test_bad_bar_halts_before_partial_or_adapter(tmp_path, changes):
    account = runtime_owner(tmp_path, [])
    adapters = inert_adapters()
    runtime = FourLegRuntime(account, adapters)
    sample = replace(bars()["orb_mnq_v7"], **changes)
    with pytest.raises(AccountOwnerError):
        runtime.on_completed_bar("orb_mnq_v7", sample, now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.retained_partial_bars == ()
    assert adapters["orb_mnq_v7"].bars == []
    assert account.synthetic_broker.commands == []
    assert account.incidents

@pytest.mark.parametrize("price", [-1, 0, float("nan"), float("inf"), True, "100"])
def test_bad_trigger_halts_before_reservation(tmp_path, price):
    account, route = owner(tmp_path, [])
    action = replace(intent(), order_type="stop", price=price)
    with pytest.raises(AccountOwnerError):
        account.dispatch(action, now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.observable_accounting()["operations"] == ()
    assert account.unresolved_attempts == ()
    assert route.commands == []
```

Import runtime_owner/inert_adapters/bars from `test_four_leg_runtime`; owner/intent from `test_book_account_owner`; import NOW from the fixture matching the case. Use the real owner, SQLite journal, and runtime rather than mocked validation success.

- [x] Run `python -m pytest tests/ops/test_book_ingress_validation.py -q -p no:cacheprovider --tb=short`. Record failures showing retained invalid partials/sends or an unfenced exception, not merely a missing proposed helper.
- [x] Implement the pure rules and safe owner incident transaction. Call bar validation before runtime serialization and in the loop's invalid-source-value path. Call action validation before `_body(asdict(action))` in direct dispatch.
- [x] Validate each raw return from both `set_mode` and `on_bar` before extending a batch, sorting with `_sort_actions`, or serializing with `_action_body`. Require a list/tuple container and validate every member; None, a generator, a scalar, or an untyped member is a protocol violation. Then validate the complete batch before `record_barrier_actions` and before dispatching any member. Persist its diagnostic if any member fails. Do not silently discard the bad action and send the remainder.
- [x] Add the branch-specific assertions: wrong types in timestamps/scopes/brackets never escape as an unfenced TypeError; action failure preserves prior valid input history without marking the barrier dispatched; all prior broker obligations remain retained.
- [x] Run the focused file and `tests/ops/test_four_leg_runtime.py tests/ops/test_book_account_owner.py tests/ops/test_pr409_owner_lifecycle.py tests/ops/test_pr409_review2.py tests/ops/test_pr409_review3.py` once the new tests pass. Investigate semantic changes rather than rewriting expectations for convenience.
- [x] Independently review producer -> validation -> diagnostic/fence -> reservation/send boundaries and commit only this tested deliverable.

## Task 2: Failure/replay and valid-semantic compatibility are proven

**Files:** extend `tests/ops/test_book_ingress_validation.py`; inspect/extend `tests/ops/test_tv_broker_emulator.py` for explicit unchanged semantic vectors; adjust only the Task 1 production files if the tests demonstrate a defect.

**Dependencies:** Task 1's validator and incident interface. No new protection or resume API is introduced here.

- [x] Add malformed output tests for both `set_mode` and `on_bar`: a None container, an untyped member, an unknown leg, and a valid intent followed by an invalid bracket. Assert the validation fence happens before sorting/serialization, zero commands and reservations for the entire batch, a retained incident, and no completed dispatch marker. Include Fraction/Decimal action prices to prove no string-valued price reaches the journal/send.
- [x] Add a diagnostic-redelivery test using the same trusted boundary identity and a later acquisition time. Assert one incident generation increment and no send.
- [x] Add a storage-failure test at incident persistence: after failure, restore database availability and attempt a valid action on the same owner. Assert zero sends and explicit local suppression; do not assert a durable incident for the failed write. A fresh boot remains halted.
- [x] Add restart/replay after a durable invalid-input incident. Assert authority stays INTERVENTION, no invalid bar/action reaches adapters, no resend, and unresolved preexisting attempts are still present. Preserve a failed/incomplete action boundary as such rather than inventing an empty successful batch.
- [x] Add valid vectors for off-tick stop triggers/brackets, long/short directional rounding, trigger crossing before existing quantization, zero trail activation with positive offset, legitimate bare entry, and partial-fill quantities. Compare real emitted payloads and emulator outcomes to explicit existing expected values. Do not replace these with a validator-only PASS assertion.
- [x] Run `python -m pytest tests/ops/test_book_ingress_validation.py tests/ops/test_tv_broker_emulator.py tests/ops/test_four_leg_runtime.py -q -p no:cacheprovider --tb=short` and review changed failure/replay paths before committing.

## Task 3: Package and accept Slice A without overstating PR completion

**Files:** inspect/update `deploy/c1_signal_daemon/Dockerfile` and `deploy/c1_rail/Dockerfile` only if their explicit copy sets need the new module; update the matching `LISTENER_FILES` and `DAEMON_FILES` inventories in `scripts/c1_image_validation.sh`; tests `tests/ops/test_c1_signal_daemon_image_manifest.py`, `tests/ops/test_c1_rail_image_manifest.py`, and `tests/scripts/test_c1_image_validation.py`; this plan/spec for evidence links.

- [x] Verify both image import closures include the shared validator and the runtime-validation inventories exactly match each image's COPY set. Run `python -m pytest tests/ops/test_c1_signal_daemon_image_manifest.py tests/ops/test_c1_rail_image_manifest.py tests/scripts/test_c1_image_validation.py -q -p no:cacheprovider --tb=short`; do not weaken the inventories to pass.
- [x] Run `python -m pytest tests/ops -q -p no:cacheprovider --tb=short` and `python scripts/gate_manifest.py --tier check`. In this Windows environment use `C:/Program Files/Python313/python.exe` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` if needed, recording that configuration with results.
- [x] Independently review the complete slice against V1-V7 and the original failing cases. Explicitly disclose that B-D remain outstanding.
- [ ] On authorized PR update, run normal commit/push hooks and check CI on the actual head. Keep production activation and deployment out of scope.
- [x] Record revision-bound results, skips and environment limitations. Slice A passes only if every malformed input is refused before its first forbidden effect, durable failure/restart behavior holds, and valid semantic vectors are unchanged.

## Next design gates

Before Slice B implementation, specify the durable protection-owner schema and complete synthetic evidence producer, the stable source-occurrence interface for runtime/direct/internal producers, and authority predicates for attachment/tightening/loosening. Before C, map those evidence types into takeover transitions and current admission revalidation. Before D, specify bootstrap identity and explicit schema-version recognition, including treatment of existing ambiguous owners. These are required interface-design gates, not permission to supply mock capabilities or silently enlarge this plan into production recovery.

## Execution evidence — provisional, 2026-09-16

Integration workspace: `.worktrees/phase2-four-leg-execution`, branch
`codex/phase2-four-leg-execution`, refreshed base/head `fc7cdc781c892207abdbfe0b7d9a4c7f046aa816`.
Historical evidence below applies to the Slice A working tree subsequently committed as `26636b8`. Final acceptance evidence follows below.
No PR update, production activation, or deployment occurred.

- Initial integration reproduction: 28 failures against the unchanged executable baseline,
  including accepted malformed bars/prices and unfenced serialization/type exceptions.
- Added pure shared structural validation, atomic bounded diagnostic/fence recording,
  owner-local send suppression after failed incident persistence, producer/container/batch
  checks, explicit empty scope refusal, and validation of retained bars during recovery.
- SQLite trigger-induced failure verifies transaction rollback and persistent local send
  suppression after database availability returns. Restart keeps outstanding attempts;
  incomplete adapter-output boundaries retain `actions=None` and are not replayed as empty success.
- Independent read-only review reproduced a legacy invalid-partial replay bypass. A new
  integration test failed before the correction; retained partial and complete replay now
  validate before adapters. Reviewer verified 68 ingress tests passing and found no additional
  blocking implementation defect, conditional on the compatibility decision below.
- Full `tests/ops`: **2385 passed, 15 skipped, 1 failed**, two third-party plotting deprecation
  warnings. Environment: Windows, `C:/Program Files/Python313/python.exe`,
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`; elevated execution was needed to access installed Python
  dependencies. Python 3.11 compatibility is retained in syntax but was not executed on 3.11.
- Explicit synthetic compatibility vectors cover off-tick trigger preservation and crossing
  before quantization, long/short bracket rounding, zero activation with positive offset,
  bare entry and partial-fill admitted quantities.
- Both Docker COPY sets and validation inventories include the new module. `.dockerignore`
  also required an allowlist entry; initial packaging tests exposed this and it was corrected.
- Check-tier gate output contains no failures; absent private-data/catalog warnings remain.
  Local command outputs are retained in `tmp-slice-a-*.txt` in this worktree.

### Unresolved compatibility decision

`test_accepted_private_orb_trigger_reaches_shared_fixed_base` emits activation **12 (int)**
and trailing offset **0 (int)** for its synthetic bars. The private adapter computes the
trailing offset by rounding its calculated price distance into ticks. The new validator
implements the approved `offset > 0` requirement and rejects this output. The previous
emulator accepts zero and calculates a stop at the tracked extreme after activation.

The operator requested discussion before changing the contract. No validator relaxation,
strategy parameter change, adapter change, or test-expectation rewrite has been made.
An earlier conversational description as a floating-point offset was incorrect and was
corrected after inspecting the actual emitted value. At this checkpoint, Slice A acceptance and commit were pending this decision; the operator decision and final acceptance below supersede that provisional status. Slices B-D remain entirely outstanding; this does not establish PR
409 merge readiness or live capability.

### Operator decision — 2026-09-16

The operator explicitly directed: keep zero-offset rejection until intended strategy
behavior is established, commit, and continue Slice A to completion. The `offset > 0`
contract remains unchanged. The existing synthetic private-adapter case must assert
rejection for its zero-offset output; a separate positive-offset adapter case will
retain the fixed-base admission assertion. This is an authorized contract correction,
not an adapter or strategy-parameter change. All 23 packaging tests passed after the
Docker build-context allowlist correction.


## Final Slice A acceptance � 2026-09-16

Implementation commit: `26636b8760530f2752b6571681eeb81e7f89e665` (normal commit hooks passed).
Final acceptance includes the follow-up test/documentation commit containing this section.
Production modules are unchanged from `26636b8`.

The operator retained zero-offset rejection. Both unchanged real-adapter outputs are now
covered: synthetic half-range 1 produces offset 0 and is durably rejected before any
operation, attempt or command; half-range 10 produces offset 4, preserves its bracket,
and admits the same fixed-base quantity 1. The offset is derived from range, not absolute
price. No rounding clamp, strategy parameter change, or validator relaxation was made.
The broader intended strategy treatment of zero offsets remains unqualified; Slice A
continues to reject them pending separate evidence and approval.

Final verification (Windows, Python 3.13, plugin autoload disabled):

- Full `tests/ops`: **2387 passed, 15 skipped, 2 warnings**, exit 0. Skips: 12 private
  adapter/parity input cases and 3 private Striker cases; warnings are third-party plotting
  deprecations. Output retained locally in `tmp-slice-a-ops-final.txt`.
- Focused ingress/emulator/runtime/owner/lifecycle/review regression set: **209 passed**.
- Synthetic ingress suite with nonexistent `FP_PORT_ROOT` and imports of `cryptography`
  and `nacl` explicitly blocked: **68 passed**. No private/signing capability is required
  by these new runtime regressions.
- Image import-closure/build-context/manifest suite: **23 passed**; includes both exact
  Docker COPY sets and runtime inventories. No packaging bytes changed after that run.
- Repository `gate_manifest.py --tier check`: **exit 0**, with documented absent private
  data/catalog notices. Commit hooks also check layer boundaries and Python 3.11 syntax floor;
  execution under a Python 3.11 interpreter was not performed.
- Independent review accepted `fc7cdc7..26636b8` plus the final two-case ORB regression.
  Its demonstrated retained-partial defect was fixed and verified; no actionable Slice A
  findings remain.

Scoped invariant disposition: V1 is established for malformed fresh/retained bars and
fresh adapter/direct actions; diagnostic redelivery and failure preservation exercise
Slice A's V4/V5/V6 obligations; unchanged payload/emulator vectors exercise V7. Structural
leg/scope checks support V3 without claiming state-dependent ownership. This does not
establish the broader V2-V6 protection, occurrence, takeover, activation or migration
requirements reserved to B-D.

The PR-update checkbox is intentionally not executed: the operator requested local commits,
not push/deployment. No current remote-head CI or whole-PR readiness is claimed.
