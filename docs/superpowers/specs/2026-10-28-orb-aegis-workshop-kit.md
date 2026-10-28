# ORB + Aegis workshop kit

Companion to the proposed [workflow](2026-10-28-orb-aegis-workshop-design.md).
Templates and examples only; all numbers below are fabricated or proposed bounds.

## Pilot card for later approval

**Must run locally:** Joshua attends; private records, if later authorized, stay
on their permitted surface. The proposed first pilot uses synthetic fixtures only.

| Field | Proposed pilot / binding needed before approval |
|---|---|
| Question | Does assisted capture reduce decision time without losing adverse or failed trials? |
| Owner / writer / reviewer | Joshua chooses named session owner, sole writer and independent reviewer before start |
| Surface | Existing text editor and saved fabricated result tables; no strategy runner needed |
| Bound | Option: 30 minutes Joshua attention, 60 minutes agent effort, six draft trial records and twelve fixture checks, ten minutes local compute; no paid services. Not adopted by this document |
| Work | Reconstruct the synthetic comparison below, then perform the twelve record-level checks using the six-trial mapping below; compare with an equivalent manual worksheet task |
| Decision rule | Option: all integrity cases handled; zero missing/duplicate trials; correct synthetic decision; at least 20% less active owner time than the matched manual task. Otherwise revise once or stop, within the original bound |
| Stop | First exhausted bound; permission/surface drift; unresolved process/output; actual strategy/account data appears |
| Output | Private session card/log with sanitized review summary; record practice/order effects and uncertainty, not a general speed claim |
| Approval | Pending Joshua and owning coordinator's acceptance of exact scope, bounds and identities |

Pilot 1 measures capture/integrity overhead only. It does not exercise hypothesis
selection or visual diagnosis, and cannot establish their speed or decision-quality
benefit. A separate later pilot needs plots, actual diagnosis/comparison choices
and its own approved bounds and rubric before those benefits can be assessed.
It can use static fabricated plots and existing tools; this is not a framework-build
dependency or approval to run that pilot. No parameter campaign starts from this
card. A later empirical pilot must bind all fields below and get the applicable
research/data/execution approvals first.

## Session binding template

Copy into an approved private session record; replace `unset` before dispatch.
Public review uses sanitized reference IDs rather than private values or paths.
Each expression's `source_config_pins_ref` identifies its own source revision,
resolved settings export/digest and execution semantics; `evidence_scope` records
what was actually tested/accepted and what remains unknown. Use `not_applicable`
with a reason for unused expressions, never copy another row's evidence. O-N/O-0
are ORB labels; Aegis uses its own identities in the corresponding contexts.
`bound_strategy_expression_refs` selects the identity row used for each enabled
strategy in this session; it may reference any declared row, not just the row
literally named `workshop`. The control/candidate/runtime fields below bind only
to those selected rows and must agree with their pins at readback. For example,
`orb: strategy_expressions.orb.o_0_native_solo` selects O-0; it does not inherit
the `workshop` or O-N row's evidence or grant permission to execute it.

```yaml
session_id: unset
question_and_mechanism: unset
decision_if_better_worse_or_inconclusive: unset
session_owner: unset
single_writer: unset
independent_reviewer: unset
approval_reference_and_scope: unset
budget_trial_compute_attention_cost: unset
stop_conditions_and_deadline: unset
strategy_expressions:
  orb:
    workshop: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
    o_n_portfolio: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
    o_0_native_solo: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
  aegis:
    workshop: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
    portfolio_model: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
    native: {identity_ref: unset, source_config_pins_ref: unset, evidence_scope: unset}
bound_strategy_expression_refs: {orb: unset, aegis: unset}
control_source_commit_and_private_manifest_ref: unset
candidate_resolved_config_digest: unset
source_and_runtime_version: unset
permitted_data_manifest_and_execution_surface: unset
actual_settings_export_method: unset
instrument_session_timezone_calendar_and_horizon: unset
scenario_ids_and_coupling_method: unset
account_stage_initial_state_rule_vintage_and_rule_source: unset
integer_sizing_margin_capacity_and_shared_protection: unset
fill_commission_slippage_fees_and_ledger_convention: unset
objective_metrics_thresholds_uncertainty_and_action_map: unset
prior_exposure_inventory_and_unknowns: unset
exploration_or_confirmation_partition_and_custodian: unset
existing_owner_release_dependencies: unset
```

## Trial log template

One row is one proposal; attempts are append-only child events. Record at allocation,
not just when a successful result is available. `not_applicable` requires a reason;
`unknown` blocks any claim needing that field. Keep private configuration values,
account state and outputs on the permitted private surface.

```yaml
trial_id: unset
parent_trial_and_attempt_id: unset
allocated_utc_and_actor: unset
hypothesis_parameter_delta_rationale: unset
information_seen_before_choice: unset
requested_config_and_control_ref: unset
actual_applied_settings_export_and_digest_before_after: unset
source_runtime_data_rule_cost_and_scenario_pins: unset
approval_readback_and_human_override: unset
attempts: # append transitions, errors and reconciliation evidence; never overwrite
  - attempt_id: unset
    state_and_time: prepared
    command_or_manual_action_and_output_location: unset
    process_receipt_result_hash_and_capture_completeness: unset
    failure_interrupt_duplicate_reconciliation: unset
result_validity_and_missing_arms: unset
metrics_uncertainty_path_and_settlement_ledger_refs: unset
data_exposure_added: unset
owner_agent_wall_compute_time_and_actual_or_estimated_cost: unset
decision_and_reason_next_question: unset
```

## Worked synthetic comparison

Fabricated toy strategies `Toy-O` and `Toy-A` do not encode either strategy.
Control is O-window `2`, A-window `3`, integer quantity `1` for each enabled leg.
Candidate changes only Toy-O's window to `1`; A and all costs/rules stay frozen.
The hypothesis is faster eligibility with no additional breaches. There are four
shared scenario IDs, one fixed horizon and an absorbing evaluation stop. Costs
are already deducted. Each arm evolves its own floor and capacity. A later funded
stage is deliberately absent, so this cannot answer a first-landed-payout objective.

| Arm | s1 | s2 | s3 | s4 | Pass / breach / unfinished |
|---|---|---|---|---|---|
| O control | pass | unfinished | breach | unfinished | 1 / 1 / 2 |
| O candidate | pass | pass | breach | unfinished | 2 / 1 / 1 |
| A alone (same in both sets) | unfinished | pass | unfinished | unfinished | 1 / 0 / 3 |
| Pair control | pass | pass | unfinished | unfinished | 2 / 0 / 2 |
| Pair candidate | pass | pass | breach | unfinished | 2 / 1 / 1 |

Paired candidate-minus-control pair-pass indicators are `[0,0,0,0]`; breach
indicators are `[0,0,1,0]`. The candidate adds a standalone O pass but no pair pass,
and adds a pair breach. A fabricated trace identifies an earlier shared capacity
admission and later floor constraint on s3; summing standalone profits would miss
it. Joshua's declared rule rejects this candidate for the pair and records the
interaction question. Four fabricated paths support no population probability or
confidence claim. Keep the rejected trial and all plotted information in exposure.

Example log: `SYN-01` control captured; `SYN-02` candidate prepared and completed;
`SYN-03` two-factor draft abandoned before application; `SYN-04/a1` interrupted
after output publication, receipt reconciled and adopted once, no rerun;
`SYN-05/a1` known failure with error retained, `a2` explicit retry;
`SYN-06` manual override requested, missing cost model blocks dispatch. This is a
walkthrough, not a report that those runs occurred.

The six IDs are proposal/trial records, not six checks or six executions. For
Pilot 1, assign the twelve checks below as follows; each check operates on a
separate fabricated copy of its named trial record. Log `fixture_check_id`,
`trial_id`, any attempt transitions, expected/observed outcome and evidence. Copies
are independent so an injected stop or contamination cannot silently resume the
same session. They introduce no new hypothesis or executed parameter variant;
an actual new proposal would consume another trial and exceed this pilot's bound.

| Trial record | Assigned fixture checks |
|---|---|
| SYN-01 | Requested/actual config mismatch; wrong digest on control restoration |
| SYN-02 | Missing pair arm/rule mismatch; debit before bank receipt |
| SYN-03 | Draft cancellation/human override; fabricated early-confirmation-open event |
| SYN-04 | Duplicate attempt submission; interruption during publication |
| SYN-05 | Crash before output; manual change without settings export |
| SYN-06 | Missing cost/fill assumption; exhausted budget |

Every check is recorded, including blocked/failed observations. The simulated
retry in the example log is an attempt within SYN-05, not a seventh trial. Real
pilot checks or rechecks still consume attention/compute and the twelve-check
allowance; if any required coverage is incomplete when a bound is reached, stop
and report the pilot incomplete rather than silently adding cases or time.

### Synthetic settlement trace

At funded horizon start, toy balance is 100 units and receivable/cash zero. A
request for 10 changes no balance or cash. Approval alone changes neither. Debit
of 10 yields balance 90, receivable 10. Toy payment routes the receivable through
an intermediary; bank receipt yields receivable zero, landed cash 10. Sum is 100
at each stage before fees/trading. If a 1-unit settlement fee is charged, landed
cash is 9 and cumulative fee 1. If denied before debit, all remain at initial
values; a post-debit denial must record the actual refund or forfeiture event,
never both. These conventions require venue-specific binding before real use.

## Minimal workflow acceptance walkthrough

The future pilot owner performs these on fabricated records and retains observed
outcomes. This document specifies the expected behavior; it implements no validator
and claims none of these checks have run.

| Injection | Required observation |
|---|---|
| Requested O-window 1, actual export 2 | `config_mismatch`; dispatch blocked; actual settings retained |
| Missing cost/fill assumption | Invalid comparison; no optimistic default; dispatch blocked |
| Same trial/attempt submitted twice | Reconcile original receipt; one adopted result, duplicate event logged |
| Trial crashes before output | Failed attempt/error captured; trial remains visible, metrics unavailable |
| Manual change without export | Log manual exposure; block valid result until actual settings are recovered |
| Joshua cancels draft / overrides choice | Abandonment/override and rationale persist; locked/scope gates still apply |
| Stop during publication | Inspect process and receipt; reconcile once or remain uncertain; no blind retry |
| Restore control with wrong digest | Next trial blocked until actual frozen digest is verified |
| Confirmation chart opened early | Contamination logged; confirmatory interpretation stopped |
| Pair arm missing or rule vintage differs | Partial/unmatched diagnostic; no fabricated paired difference |
| Debit occurs before bank receipt | Receivable carries gap; no double-counted landed cash |
| Budget reached during analysis | Stop/reassess; do not add trials or weaken the decision rule |

Record each case as `expected, observed, evidence_ref, pass/fail`; unresolved cases
block workflow adoption. Lightweight checks for this documentation are relative
link validity, diff whitespace, scope/privacy inspection and repository pre-commit
gates. Those checks validate the proposal artifact, not empirical research or a
native implementation.
