# Claude handoff: exact funding evidence for a supplied candidate execution

**Type:** cc_handoff  
**Date:** 2026-09-05  
**Status:** Frozen implementation contract; parent review required before merge  
**Owner:** Claude implementation; Codex integration/review; operator merge

## 0. Current sources

Repository baseline: `846a437d6f1ccbd30435c81730725cdb553b6beb`. Read `lab/README.md`, `REPO_MAP.md`, `tests/conftest.py`, `pyproject.toml`, and `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`. This is an isolated research helper; no production sizing or admission caller is changed.

Primary formulas and limits: [TradingView leverage model](https://www.tradingview.com/support/solutions/43000717375-how-to-simulate-trading-with-leverage-in-pine-script/), [fixed-quantity capital requirement](https://www.tradingview.com/support/solutions/43000478450-i-ve-successfully-added-a-strategy-to-my-chart-but-it-doesn-t-generate-orders/), and [strategy properties](https://www.tradingview.com/support/solutions/43000628599-strategy-properties/). Read those references. A positive arithmetic witness within the domain below is an inference from these rules; it is not a platform execution certification.

## 0.5. Clarification and cloud availability

All required implementation inputs are public in this handoff and repository. Fixtures below are invented. No private strategy source, account state, capture, export, token or external account access is required or authorized. If the contract is contradictory, report the exact conflict; do not substitute a policy. Routine implementation choices are yours.

## 1. Problem and purpose

A chronological replay needs evidence that a supplied candidate execution is strictly within a fully funded interior. Separate that small arithmetic proof from the caller's order lifecycle, price formation and accounting. A submission-time witness cannot authorize a later fill after a price gap. The caller must establish fresh facts at each candidate fill.

## 2. Scope and deliverables

Create only `lab/replay_funding.py` and `tests/test_replay_funding.py`, plus a factual completion note in this handoff if useful. Standard library only. Follow repository import conventions. No core edits, integrations, CLI, new framework or external data fetching at runtime.

Export frozen dataclasses `FundingFacts` and `FundingAssessment`, string enums `FundingStatus` and `FundingReason`, and pure `assess_funding(facts: FundingFacts) -> FundingAssessment`.

`FundingFacts` fields:

- Decimal: `cash_before`, `point_value`, `execution_price`, `current_mark`, `execution_cost`, `margin_ratio`.
- Integer: `requested_quantity`, `open_quantity`, `competing_entry_count`.
- String: `direction` (supported value `LONG`).
- Boolean: `known_state`, `execution_price_established`.

The Decimal fields must actually be finite Decimal values; no float coercion. Prices and point value must be positive; cost and margin ratio nonnegative. Cash may be negative. Counts must be nonnegative integers and must reject booleans, fractions and floats. Boolean fields must actually be booleans. A string direction other than LONG is outside the supported domain; a non-string is invalid. Invalid facts return INVALID_INPUT without a positive proof, including a wrong facts object type.

## 3. Frozen behavior

Supported domain: known state; established candidate price; LONG; requested quantity exactly one; margin ratio exactly one; open quantity zero; no competing entry. Competing entries include submitted requests with zero reservation. The caller, not this helper, verifies those attestations, consistent currency units, complete prior accounting, order ownership and current execution-point mark. Slippage is already included in execution_price; execution_cost is the total known cost charged for this candidate execution, with no duplicate slippage charge.

Evaluate invalid input first. For valid inputs, use this stable precedence: UNKNOWN_STATE, UNESTABLISHED_EXECUTION_PRICE, UNSUPPORTED_SIDE_MARGIN_QUANTITY, EXISTING_POSITION, COMPETING_ENTRY, then arithmetic. Scope misses return status OUTSIDE_PROVEN_DOMAIN and the corresponding reason. Their arithmetic witness fields are None.

For facts within the domain, compute exactly:

```text
cash_after_cost = cash_before - execution_cost
funding_basis = max(execution_price, current_mark)
required_at_basis = requested_quantity * point_value * funding_basis
surplus = cash_after_cost - required_at_basis
post_fill_margin_cushion = cash_after_cost - requested_quantity * point_value * execution_price
```

Return these five Decimal witnesses in FundingAssessment. Strictly positive surplus gives status PROVEN_POSITIVE_CUSHION, reason POSITIVE_CUSHION. Zero or negative surplus gives OUTSIDE_PROVEN_DOMAIN, reason NON_POSITIVE_CUSHION, retaining arithmetic witnesses. All enumerated reasons plus INVALID_INPUT are required. Assessments are immutable.

Exact comparisons and witness values must not change with ambient Decimal precision or rounding mode; do not add epsilon, cent rounding, fitted tolerance or context-global mutations. Use an explicit exact arithmetic approach. Preserve all input values. The helper performs no I/O and mutates no external state.

OUTSIDE_PROVEN_DOMAIN means only that this proof does not apply. It must not mean reject, clip, liquidate, cancel or accept an order. No output authorizes a broker action. The helper cannot establish fill price, resolve simultaneous orders, prove no hidden commitments, or certify platform parity. For fixed post-fill cash, quantity and entry price, equity minus 100%-long required margin is the returned post-fill cushion; a new fill/fee requires new assessment.

## 4. Falsifiable hypothesis and independent pins

H: the helper returns an exact conservative witness for the declared interior without assuming an order lifecycle. Falsifier: any outside-domain input returns a positive proof, ambient Decimal context changes a result, or the following literal expected values fail.

Base invented facts: cash 1000, point value 5, execution price 100, mark 99, execution cost 3, requested quantity 1, open quantity 0, competing count 0, margin ratio 1, direction LONG, both booleans true.

| Independent case | Expected |
|---|---|
| Base | after-cost 997; basis 100; required 500; surplus 497; post-fill cushion 497; positive |
| Mark 101 | basis 101; required 505; surplus 492; post-fill cushion still 497 |
| Cash 503, price/mark 100 | surplus 0, outside; cash 503.01 gives .01 positive; 502.99 gives -.01 outside |
| Separate later candidate price/mark 201 | required 1005; surplus -8, outside; prior immutable result unchanged |
| Cost 0, then cost 4 | surplus 500, then 496 |
| Each separate domain miss | unknown, price unestablished, short, ratio .5, requested qty 0 or 2, open qty 1, competing count 1 produce the named outside reason |
| Input rejection | NaN/infinities, non-Decimal numeric fields, bad signs, non-integral/boolean counts, wrong boolean types and wrong facts object produce INVALID_INPUT |
| Immutability/context | repeated calls identical; inputs/output immutable; low/high Decimal precision and changed rounding produce exact same witnesses; include precision-sensitive long decimal coefficients |

Include a test distinguishing the mark-based conservative surplus from the post-fill cushion and reason-precedence tests. Expected values must be independently written, not computed by calling the implementation under test.

## 5. Forbidden moves

- Do not add broker acceptance, rejection, quantity resizing, liquidation, price normalization or source policy.
- Do not promote any broader funding capability or remove another execution gate.
- Do not import private artifacts, real account/strategy values, campaign outcomes or reference trades into code, tests, comments or this PR.
- Do not alter core, configuration, campaign/search gates, dependencies, workflow permissions or other agents' files.
- Do not merge, auto-merge, deploy or publish performance/probability claims.

## 6. Gate and return taxonomy

RESOLVED only when exact contract, independent tests and repository-required checks pass, with parent review of the actual diff. Otherwise report FALSIFIED with a concrete failing case, or AMBIGUOUS if a contract dependency is unresolved.

Return DONE or DONE_WITH_CONCERNS with commit, changed files, exact test results, limits and remaining concerns. Use NEEDS_CONTEXT for a missing factual input. BLOCKED must identify whether it is a tool/environment problem, contradictory spec, or outside-scope dependency. These statuses never authorize merge.

## 7. Execution and review

Read the listed sources once in a consolidated pass. First post a short Phase 0 scope/dependency report, then implement without waiting for further permission when no conflict exists. Add failing expected-value tests before code. Verify only affected tests during development, then required CI. Provide a two-pass self-review: specification compliance, then code quality. Keep results on this PR's existing branch. Codex independently reviews the final head and owns integration; operator merges.

## 10. Audit hooks

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-09-05-claude-funding-evidence.md --type cc_handoff
python -m pytest tests/test_replay_funding.py -q
git diff --check
git diff --stat origin/main...HEAD
```

CI may add its existing required checks. Do not claim private replay parity or an integrated caller from a green helper test suite.

