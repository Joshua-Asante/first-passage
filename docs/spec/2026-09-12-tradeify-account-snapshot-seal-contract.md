# SPEC: Tradeify portfolio — account-snapshot seal contract (TB-T1 field and evidence contract)

Status: PROPOSED · 2026-09-12 · authorizes nothing ($0 · K=0) · depends: [Track B umbrella](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) TB-T1 / TB-B7 stubs · campaign-state §17 / D23 (evidence class) · [used-account kernel](../superpowers/plans/2026-09-05-tradeify-used-account-kernel.md)
Objective: fix the fields, evidence files, checks and output of the B7 account-snapshot sealer so Codex can build the tool now (TB-T1) while the fresh live snapshot itself stays a later operator gate; TB-P1 cites this contract instead of restating it.

Fields (the operator types the dashboard values; the tool derives, never guesses):

| Field | Source | Typed / derived | Rule |
|---|---|---|---|
| `original_basis` | `core/firm_rules.FIRM_RULES["Tradeify_Select_100K"]["starting_balance"]` | derived (tier constant) | never typed; the target and the fixed-dollar width scale off it (kernel spec) |
| `balance` | Tradeify dashboard `Balance` (evidence E1) | typed | positive, finite |
| `equity` | Tradovate positions/orders export (E2) or dashboard | typed | must equal `balance` when flat (C3) |
| `trailing_threshold` | dashboard `Trailing Max Drawdown` (E1) | typed | the venue's own number (PRIMARY class, campaign-state §17) |
| `historical_eod_peak` | `trailing_threshold + starting_balance × max_dd_pct / 100` | derived | never typed and never reconstructed from statements (D23) |
| `prior_trade_days` | dashboard `Trading days` numerator (E1) | typed | non-negative integer |
| `prior_max_day_profit` | dashboard `Highest Profit Day` (E1) | typed | non-negative |
| `consistency_display_pct` | dashboard `Consistency` (E1) | typed | informational cross-check (C6) |
| `profit_target_display` | dashboard `Profit Target` denominator (E1) | typed | must equal `starting_balance × profit_target_pct / 100` (C7) |
| `cash_adjustments_total` | statement (E3): deposits, withdrawals, fees outside commissions, manual adjustments | typed from E3 | zero, or reconciled (C8) |
| `token_trade_fill_dates` | statement (E3) | typed list of ISO dates | informational (weekly preservation-trade evidence); parse only |
| `positions_export_shows_flat` | E2 | typed boolean attestation | must be `true` (C3) |
| capture timestamps | one per evidence file | typed, ISO-8601 with zone | freshness (C5) |

Evidence files (each present, non-empty, SHA-256 recorded; paths private):
E1 the Tradeify dashboard capture (image) · E2 a Tradovate positions and working-orders export showing zero open positions and zero working orders · E3 a venue-backed account statement / transaction history covering the evaluation from its start to the capture.

Checks (every one binary; any failure refuses the seal and prints the failing check id only):
C1 every evidence file exists and is non-empty; digests computed. C2 `EvaluationState(original_basis, equity, historical_eod_peak, prior_trade_days, prior_max_day_profit)` constructs (the kernel's own validation, `core/mc/simulation.py`). C3 `equity == balance` and `positions_export_shows_flat` is true. C4 relational: `historical_eod_peak ≥ balance`; when `balance == trailing_threshold + width` the account is at its high-water mark (recorded as `at_high_water_mark: true`), otherwise the carried drawdown `peak − balance` is recorded. C5 freshness: all capture timestamps lie within `freshness_window_minutes` (frozen default 30) of each other; the seal happens within `seal_within_hours` (frozen default 24) of the latest capture; every capture and the seal fall inside one venue session boundary (`session_boundary_rule`: between a weekday 17:00 ET close and the following 18:00 ET reopen, or between Friday 17:00 ET and Sunday 18:00 ET) so no session activity can intervene. C6 when `balance − original_basis > 0`, `prior_max_day_profit / (balance − original_basis)` agrees with `consistency_display_pct` within one percentage point (the display caps at 100 %; a capped display passes when the ratio is ≥ 1). C7 `profit_target_display` equals the tier constant. C8 `cash_adjustments_total == 0`, or a non-empty `adjustments_reconciliation` note is supplied and recorded verbatim. C9 the output path is reported ignored by `git check-ignore` before anything is written; the tool never prints a field value — digests and check ids only.

Output: one private JSON (`values`, `derived`, `evidence` {path basename, sha256, captured_at}, `checks` {id: pass}, `seal_timestamp`, `tool_sha256`, `contract`: this file's path) written atomically under an ignored root (default `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/account_snapshots/`); stdout carries the sealed file's SHA-256 and the check ids that passed. The seal is **attested-by-evidence, not machine-verified against the broker**: no read API exists for the dashboard, and the tool says so in its output.

Steps:
1. Codex builds `scripts/seal_account_snapshot.py` + `tests/test_seal_account_snapshot.py` test-first per the [TB-T1 packet](../briefs/handoffs/2026-09-12-tb-t1-snapshot-sealer-packet.md).
2. The coordinator adjudicates (`fable-judge`); the operator merges.
3. At TB-B7 the operator captures E1–E3 and runs the sealer; the coordinator records the sealed digest and timestamp in the execution fingerprint.

Gate: RESOLVED if the tool refuses on every check C1–C9 with a named failing test and seals a synthetic fixture that passes them all, printing no value; FALSIFIED if any check needs a value the three evidence files do not carry.
Boundary: no reconstruction of the peak from statements; no default or inferred field; no seal without E3; no live account value in any tracked file, test fixture, log or PR body (synthetic fixtures only); no read of Tradovate or Tradeify by the tool.
Reads: `core/mc/simulation.py` `EvaluationState` @ `adccb7d` · `core/firm_rules.py` `Tradeify_Select_100K` @ `d4d1c5e` · campaign-state §17/§17a–§17d @ `origin/main` · umbrella TB-T1 stub · `scripts/certification_power.py` @ `5e5a216` (stdlib-script convention)
Owner: umbrella TB-T1 / TB-B7; TB-P1 cites this file for the snapshot boundary.
