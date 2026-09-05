# Used evaluation account — kernel specification and implementation plan

**Status:** implemented, 2026-09-05; verification recorded below. This is the independent
used-account part of Task 2 in the
[approved campaign plan](2026-09-02-seven-strategy-tradeify-select-configuration.md).
It does not close source intake, synchronized bar replay, portfolio execution or
the statistical freeze. No campaign sampling is authorized by this implementation.

**Rule 0:** read `core/mc/simulation.py`, `core/mc/preflight.py`,
`core/firm_rules.py` Select configuration and `core/dd_protection.py` directly at
`8df70fa` before authoring this interface. The current engine resets equity/peak
to the original basis and resets prior trade days and best day to zero. Its
fixed-dollar trail and consistency denominator already use the original basis;
those expressions must keep that meaning.

## Global constraints

- Preserve the existing public return shapes, outcome taxonomy, RNG draws and
  results of calls that omit the new state argument.
- Keep production risk/venue constants and sizing policy unchanged. Use synthetic
  evidence only; no private account values, vendor data or portfolio search.
- Keep account state separate from firm rules and path excursions. Maintain
  the historical-fixture totality guard and package/flat import compatibility.
- Use the existing daily transition and boundary arithmetic; do not build a
  second simulator. The operator retains all merges and deployment decisions.

## Task 1 — Add validated evaluation state to the existing simulation

**Owned files:** `core/mc/simulation.py`, documentation in
`core/mc/preflight.py`, and `tests/core/test_mc_initial_state.py`. Existing
synthetic tests may be extended only where interface coverage needs it. The
controller owns this plan and all campaign/governance records.

### Interface and supported snapshot

Add a frozen `EvaluationState` dataclass in `core.mc.simulation` with five
required fields, without defaults:

| Field | Meaning |
|---|---|
| `original_basis` | Original evaluation starting equity; never current balance |
| `current_equity` | Settled equity at the start of the next modeled session |
| `historical_eod_peak` | Highest prior end-of-day equity, including original basis |
| `prior_trade_days` | Prior qualifying trading days |
| `prior_max_day_profit` | Largest prior net profitable day, zero if none |

The snapshot is a flat, settled session-boundary snapshot with no pending orders,
no current-session trading, and no deposits, withdrawals or account adjustments.
The caller must establish those facts; five numbers do not prove them. Snapshot
provenance/digests and broker capture belong to the later private binding layer.

Validate amounts as finite real numbers, rejecting booleans, strings and NaN/inf.
Basis, current equity and peak must be positive; best-day profit is nonnegative.
Trade days must be a nonnegative integer, rejecting booleans/fractional values.
Peak must be at least both basis and current equity. Zero prior trade days require
the pristine values (equity = peak = basis; best day = zero). A positive prior
peak gain requires a positive best day and cannot exceed prior trade days times
best-day profit (compare currency totals at cents precision). These conditions
check internal consistency; they do not certify the supplied history.

Add keyword-only `initial_state: EvaluationState | None = None` to both
`simulate_path` and `run_seed`. Keep it out of the historical firm fixture by
adding it to `_NON_FIRM_KEYWORDS`. `run_seed` passes the same immutable snapshot
to every simulation; do not carry one path's ending state into another. Reject
`initial_state` inside `firm_kwargs`, just as `intraday_low` is rejected there.

Document the integration in `preflight.firm_kwargs`: its `account` argument is
the original basis, and consistency remains an explicit existing argument.
Callers build firm kwargs from that basis and pass `initial_state` separately.
No new convenience wrapper or implicit change to `firm_kwargs` defaults is needed.

### Initialization and transition

When state is absent, retain the legacy initialization and behavior exactly.
When it is present:

1. Require the exact dataclass and require its basis to match `starting_equity`.
   Reject mismatches rather than rebasing the target or fixed-dollar drawdown.
2. This five-field interface supports the campaign's accepted inactivity-OFF
   model only: require `inactivity_limit > horizon`. Historical inactivity-ON
   state needs information absent here; reject rather than reset its history.
   Validate the horizon/inactivity counts and relevant rule inputs sufficiently
   to prevent malformed inputs from disabling a new-state barrier or pass check.
   Support the three existing drawdown types with finite, correctly signed,
   supplied barrier parameters; reject an unknown/inert drawdown configuration.
3. Initialize equity, peak, trade days and best day from the snapshot. Initialize
   max DD from current drawdown against the historical peak. This metric covers
   the snapshot and simulated future, not unknown earlier historical troughs.
4. Test the initial account against its drawdown floor using the same existing
   rounding and comparison as the daily barrier. An already-breached or floor-touch
   snapshot raises `ValueError`; it cannot start a new evaluation or be counted
   as a passing attempt. Barrier validity is checked before initial pass status.
5. If the valid initial state already meets target, trade-day and consistency
   conditions, return `("pass", 0, initial_max_dd, None)` without processing a day.
   Otherwise use the existing daily transition, with day counts in the returned
   result measuring additional modeled business days. Prior trade days affect
   qualification only; they are not added to returned time-to-pass.
6. Keep target, daily-loss basis, fixed-dollar rope/lock, and net-profit consistency
   denominator tied to original `starting_equity`. EOD peak ratchets and intraday
   floor tests keep their existing timing. Prior peak also governs the existing
   DD protection scale. Do not change the protection threshold or multiplier.

Factor small private barrier/pass helpers if needed so initial and daily checks
share the same semantics. Do not change legacy terminal ordering or float rounding.
Reject an invalid explicit state even when `run_seed` requests no simulations;
an empty batch must not bypass the state contract.

### Verification (TDD)

Write and run failing tests before production edits. Use independent synthetic
expected outcomes rather than assertions copied from a new helper:

- Omitting state and passing None preserve the existing results. An explicit
  pristine state agrees under supported, initially nonterminal conditions.
- A used account reaches the original target sooner without moving that target.
  Passing current equity as `account` instead is rejected as a basis mismatch.
- Two valid states with equal equity and different peaks have different floors.
  A touched intraday floor fails even if the close recovers.
- The initial peak activates the existing protection haircut when appropriate.
- Prior best-day profit can delay consistency clearance; prior trade days count
  toward minimum days, and neither is added to additional elapsed time.
- An already-passing state returns day zero; malformed and already-breached
  states fail closed. Cover bad numeric types, NaN/inf, inconsistent history,
  inactivity-ON, and incomplete/inert new-state rule arguments.
- `run_seed` applies the same state independently to each path, pairs intraday
  blocks as before, rejects state in `firm_kwargs`, and validates empty batches.
- Existing synthetic, float-boundary, trailing-locking, inactivity, preflight,
  historical-fixture and facade regressions stay green, including flat imports.

Focused command: `python -m pytest -q tests/core/test_mc_initial_state.py`.
Integration command: `python -m pytest -q tests/core` (record any normal vendor
skips separately). Run the repository check tier before publication. No campaign
Monte Carlo, n1/n2/n3 sample or private-account scoring is part of these tests.

Deliver the implementation and test evidence for independent review. Keep the
parent plan's bar-to-equity adapter unchecked: this kernel does not supply it.

## Implementation and verification

Specification commit `1046588` preceded implementation `fa5039a` and fix `6e423fb`.
The task review identified an empty-batch initial-floor bypass and a NaN behavior
change in the extracted pass predicate. Five new failing cases reproduced them;
the fix shares initial validation across both entry points and preserves the
legacy positive comparisons. On Python 3.12.14, the final focused state tests pass
56 cases and the six-file state/interface regression set passes 123 cases.

The original simulation/calculator baseline passed 56 tests with one vendor skip.
Private binding and the bar adapter are still outside this kernel; no campaign
sampling or account-value validation has occurred.
