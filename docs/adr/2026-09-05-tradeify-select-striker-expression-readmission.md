# ADR 2026-09-05 — admit the two campaign Striker expressions to evaluation scope

**Status:** `Accepted` — records the operator's 2026-09-05 election; no deployment GO
**Decision date:** 2026-09-05
**Supersedes:** `2026-08-04-tradeify-venue-descope-eval-included.md` in part — evaluation eligibility of the two exact campaign expressions below
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

## §0 — Rule 0 reads

Read before this record: `core/firm_rules.py` Select 100K configuration,
`core/mc/simulation.py` initial-state and consistency logic, `core/dd_protection.py`
and `ops/c1_rail/c1_sizing_host_reference.py` at `2a89348`; the prior de-scope ADR
and `ops/venue_editions/Tradeify_Select_100K.md`; the campaign's phase1_config.json.
The two private Pine bodies were located, hashed against that configuration and
their sizing/DD/soft-stop branches read on 2026-09-05. Their identities are:

| Campaign expression | Pine SHA-256 |
|---|---|
| `striker_dj30_mym_pyramid_250` | `712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7` |
| `striker_nas100_mnq_dow_wed_excluded` | `fa6a70cde002131bbd266bee70defb01e32deae2de79fdc327d661f829115c39` |

Effective chart-input binding remains an intake requirement. Source hashes alone
do not establish the behavior of the captured chart.

For the same-day co-exposure amendment, production/source reads were refreshed
at `c88965a`: the payload builder, sizing host, firm rules, DD protection and
source inventory. The amendment below records the specific findings.

## §1 — Context

The operator elected to include these two expressions in the Select configuration
campaign and retained the incumbent evaluation. The prior de-scope must not be
silently bypassed by assigning new IDs or interpreting an old measurement as a
new re-scope result. This record makes the exception explicit before selection.
**Decision driver:** the campaign must have a truthful, bounded eligibility set.

## §2 — Decision

Admit the two named expressions to selection and conditional deployment eligibility
for the **Tradeify Select 100K evaluation only**, by explicit operator election.
This is the admitting ground. It does not assert that the prior ADR's T1 fired,
that T1 is mathematically unsatisfiable, or that either expression will qualify.
**Effective:** the operator election of 2026-09-05, recorded here for merge.

Selection is from the five retained campaign expressions. The operator's
same-day co-exposure amendment below replaces the former at-most-one-MNQ limit.
Each admitted expression still needs bound effective inputs, valid size evidence,
the frozen campaign acceptance tests, winner execution parity, M1 RESOLVED and a
separate operator GO. Existing locked Striker editions remain WITHDRAWN at zero
allocation. Funded deployment remains barred for those editions and these
expressions. The four-firm programme's 2026-11-08 obligation is unchanged.

### Same-day amendment — long-only co-exposure

The operator confirmed that ORB MNQ, Striker NAS100 MNQ and Striker DJ30 MYM are
long-only, then approved removing the blanket MNQ exclusion ("Go with your
recommendation"). The recorded `direction_evidence` for all three in
`lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json`
agrees. Effective input binding remains required; this clarification does not
replace that gate.

Both MNQ expressions may be included, with overlapping long positions, alongside
the MYM expression. All five retained expressions may therefore be eligible in
one configuration; none is mandatory. The former maximum of four was derived
from excluding one MNQ expression and is also removed. Eligibility does not
establish that the five-expression book will qualify or be selected.

Keep one execution controller per actual order symbol, with separate filled
quantity and order ownership for each strategy. Simultaneous same-direction
signals are not rejected merely for sharing a symbol. Freeze deterministic
priority and rejection behavior when account-wide contract or risk headroom is
insufficient, including outstanding reservations and additions. An exit may
reduce only its strategy's filled allocation; cancellation and fill races must
not flatten another allocation or create an unintended short. Account-wide
emergency/session flattening remains an explicit coordinated operation.

**Grounding for this amendment:** before writing it, read
`ops/c1_rail/crosstrade_payload.py`, `ops/c1_rail/c1_sizing_host_reference.py`,
`core/firm_rules.py`, `core/dd_protection.py` and the source inventory at
`c88965a`. The current payload builder requests `flatten_first=true` on entry
and can omit quantity on symbol-wide exits. The legacy `LEG_MAP` cap allocations
remain zero. Shared-symbol execution is therefore an implementation obligation, not
an existing capability or an authorization to change those allocations.

**Acceptance and failure:** before search, joint replay must implement the same
quantity ownership, aggregate exposure, reservations, skipped-signal and exit
policy intended for execution. Before deployment, prove it under partial fills,
duplicate/delayed messages, simultaneous stop/target events, cancellations and
restart reconciliation. Unproved ownership or parity blocks deployment; failure
does not authorize a post-result policy change or a second final validation.
The existing single-attempt budget, S1/S2 and eval-only authorization remain.

## §3 — Alternatives considered

| Alternative | Disposition |
|---|---|
| Exclude both expressions | Declined by the operator's election. |
| Treat new IDs as escaping the old bar | Rejected; eligibility is explicit rather than inferred from names. |
| Claim the old re-scope trigger fired | Rejected; no such qualifying measurement has been established. |
| Keep the blanket one-MNQ exclusion | Replaced by the operator-approved long-only co-exposure amendment; shared-symbol ownership and joint risk must be proved instead. |

## §4 — Failure and withdrawal handling

This is an operator scope election, not an empirical claim with a new performance
falsifier. Existing intake, validation and execution gates own their failures.
An identity mismatch stops that expression at intake; a failed final validation
ends the campaign attempt under D33. Neither event authorizes substitutions or
funded trading. If the operator withdraws this election, then this scope exception is revoked
and recorded by a successor decision. Check scope at candidate freeze and deployment review.

## §5 — Forbidden moves

- Do not infer altered trade streams by scaling realized P&L through active
dollar/equity stops. Do not promote the old locked editions through these new
rows, treat operator election as empirical falsification, or add a new token-trade
capacity test to reopen the already accepted inactivity mitigation.

## §6 — Downstream propagation

The prior ADR receives the reciprocal partial-supersession pointer. The venue
ledger receives two CANDIDATE rows with zero capital and no live leg IDs. Campaign
§49 and the current plan point here. Winner-specific lifecycle/LEG_MAP bindings
remain Phase 8 work; no production allocation or risk constant changes here.
The benefit is a definite eligibility set; the cost is intake and possible execution
work on expressions that may still fail. No new empirical RESOLVED or FALSIFIED
verdict follows from the election.

## §7 — Implementation

Apply the reciprocal header edge, add the two candidate ledger rows, and update
the campaign and plan pointers in this PR. Preserve all old withdrawn rows.
At a winner's Phase 8, verify its actual identity and runtime bindings against this
scope; do not infer those bindings from the candidate ledger.

## §10 — Audit hooks

```bash
python scripts/check_adr_graph.py
python scripts/check_brief.py docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md --type adr
python scripts/gate_manifest.py --tier check
git diff -- ops/venue_editions/Tradeify_Select_100K.md
```

## Verification

Run `python scripts/check_adr_graph.py`,
`python scripts/check_brief.py docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md`
and the gate-manifest check tier. Inspect the ledger to confirm both old editions
remain WITHDRAWN, both new rows are CANDIDATE at zero, and the live set is empty.
This record does not consume a Monte Carlo path or a deployment authorization.
