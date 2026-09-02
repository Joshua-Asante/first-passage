# Portable-edge cultivation campaign objective and boundaries

**Status:** `Accepted` — direct operator election, 2026-09-02.  
**Decision date:** 2026-09-02  
**Supersedes:** none  
**Superseded-by:** none  
**Superseded-in-part-by:** none  
**Retain-until:** none  
**Authors:** Joshua (operator elections) + Codex (record and boundary reconciliation)  
**Layer:** research-program objective, campaign authorization, and candidate/edition separation.
No candidate admission, lifecycle promotion, allocation, rail arming, or capital authority.
**Loop-of-Record:** STRATEGIC — a short programme-level find/cultivate/stop decision.

## §0 — Evidence and governing decisions read

- The operator elected: portable genuine edge first; Tradeify Select preferred; manual weekly
  preservation acceptable; 2–3 calendar days; compute/data spend flexible; preserve a genuine edge
  after edition failure; start a candidate-contract research campaign and keep looking until a
  satisfactory candidate or the bounded campaign terminates.
- [`2026-08-30-candidate-contract.md`](2026-08-30-candidate-contract.md) requires the founding
  freeze and K declaration before exploration outcomes are read. A contract cannot be opened
  retroactively around an outcome-selected cell.
- [`2026-08-30-operator-approvals-campaign-envelope.md`](2026-08-30-operator-approvals-campaign-envelope.md)
  requires a fresh operator GO before exceeding a frozen spend/schema/window/K envelope.
- [`2026-08-30-terminal-taxonomy.md`](2026-08-30-terminal-taxonomy.md) reserves
  `EVIDENCE-VOID` and `EXPRESSION-FAIL` for contract/Confirm states and routes candidate-level
  pre-Explore reachability kills to `venue / cost-constraint`.
- [`2026-06-16-rule-2-budget-before-acting.md`](2026-06-16-rule-2-budget-before-acting.md) binds
  this STRATEGIC campaign to three constituent OUTER investigations, each capped at eight complete
  attempt-and-check iterations with no self-extension.
- [`orb_mym_volume_gate_2026-09-02/RESULTS.md`](../../lab/analysis/orb/orb_mym_volume_gate_2026-09-02/RESULTS.md)
  records that P50 was selected after viewing the Off/P50/P80 panel. No K manifest or candidate
  founding freeze preceded that read.

## §1 — Decision

### 1. Commercial objective

The campaign optimizes first for a **portable genuine edge**. `Tradeify_Select_100K` is the
preferred edition, not the definition of edge. A confirmed edge remains confirmed if Select or
another edition fails; the edition verdict is recorded separately.

Manual weekly account preservation is an accepted account-level control. Candidate alpha is not
required to manufacture weekly activity merely to keep the account alive.

### 2. Campaign authorization and bounds

The campaign is authorized for 2–3 calendar days, research/paper scope only. It may examine at most
three cultivation seats and may open at most one prospectively valid candidate contract with one
Confirm selection (`M=1`, family alpha `0.05`, Bonferroni identity). These are campaign mechanics,
not evidence that a candidate exists.

The initial approved spend envelope is **$0 external data/cloud spend and at most 48 local
core-hours**. “Flexible” means the operator is willing to consider priced extensions; it is not
advance authority to incur them. Any paid dataset, cloud run, wider schema/window, or other spend
above the initial envelope requires a **new explicit operator GO after the priced sub-line is
recorded**.

### 3. Rule-2 iteration tripwire

The STRATEGIC budget is three constituent OUTER investigations, mapped one-to-one to seats A/B/C.
Each seat has at most **8 complete attempt-and-check iterations**. An iteration is one natural
candidate unit: source-and-identity check; parse/normalize/test cycle; reachability run-and-review;
or bounded primary-source query-and-read pass.

At 8/8 on any seat, work stops for the Rule-2 structured report: spent, remaining, current state,
and extend-or-stop recommendation. There is no OUTER self-extension. Only explicit operator
adjudication or a Rule-0 re-audit may extend a seat. The 2–3 day clock and 48-core-hour ceiling are
additional limits, not substitutes for iteration accounting.

### 4. Cultivation boundary

A strategy need not arrive fully formed. Before outcome access, a cultivation seat may clarify
mechanism, source identity, exact executable rules, costs, data availability, and candidate
catalogue. Once it has a complete trade object, the candidate contract and K manifest must freeze
**before the first exploration payoff cell is scored**. Outcome-guided development outside that
freeze may generate hypotheses or source priors, but it cannot later be wrapped in a contract and
presented as prospectively selected.

Every contract must also founding-freeze the independent **mechanism discriminator** required by
the candidate-contract/terminal-taxonomy chain: observable and statistic, null, expected direction,
decision threshold, and coverage/power requirement, adjudicated independently of the expression's
payoff test. A complete trade object without this field is still contract-incomplete; `CONFIRMED`
requires both the discriminator and payoff/temporal test to pass.

The Confirm interval is committed prospectively on the draft contract as required by the existing
reservation doctrine, but its **first eligible bar must be strictly later than the founding-freeze
commit**. Bars occurring after the last source read but before the freeze are intervening historical
data and are excluded from Confirm. “After the last viewed bar” alone is insufficient.

This is the admissible form of cultivation: grow the specification before outcome access; freeze
the catalogue; then learn through the accepted Explore/Confirm sequence. A payoff-defining change
after outcomes is a new prospectively frozen campaign, never an append to the old one.

### 5. P50 ruling

The exact ORB-MYM P50 expression is a **historical/source-stage development lead only** in this
campaign. Because P50 was selected from the fully viewed Off/P50/P80 catalogue without a preceding
candidate contract or K manifest, this campaign may not:

- open a candidate contract retroactively around exact P50;
- call a future P50 paper window “Confirm” under the current campaign; or
- represent its three-cell source selection as preregistered.

Seat A may capture and reconstruct P50 solely to establish provenance, risk-unit shape, and its
value as a cultivation prior. Admission of exact P50 would require a separate operator-ratified
legacy/source-intake decision that explicitly reconciles the missing prospective K/freeze; this ADR
does not create that exception. A genuinely distinct successor expression may enter only through a
fresh, prospective contract frozen before any outcome read.

### 6. Pre-contract disposition vocabulary

Before a contract exists:

- missing private source/config/export → `EVIDENCE-BLOCKED`;
- duplicate, incomplete, or non-tradeable source → `PRE-CONTRACT DROP` with the specific intake
  limb;
- clear cost/latency/geometry/shape unreachability → `PRE-CONTRACT DROP
  (venue/cost-constraint-shaped)` and no `N_expr` increment.

`EVIDENCE-VOID`, `EXPRESSION-FAIL`, and candidate-level register routing are unavailable until the
states defined by the terminal-taxonomy ADR actually exist.

## §2 — Consequences

1. The campaign plan owns execution and ledger detail; this ADR owns the durable objective and
   elections. `STATE.md` and `docs/SESSIONS.md` point here rather than restating rationale.
2. Seats B/C must prospectively freeze any complete catalogue before outcome scoring. If no such
   object exists within the campaign budget, the honest terminal state is dry/evidence-blocked.
3. Q-VOLREGIME remains research infrastructure and may motivate prospective cultivation; it does
   not license candidate status or waive the freeze/K boundary.
4. No capital-facing action follows from this ADR.

## §3 — Forbidden moves

- Retroactively declaring Off/P50/P80 selection preregistered or shrinking its K to one.
- Freezing a contract without the complete independent mechanism-discriminator rule.
- Letting a Confirm interval begin before or at the founding-freeze commit.
- Treating a recorded paid-spend ceiling as authorization without a new operator GO.
- Using `EVIDENCE-VOID` or `EXPRESSION-FAIL` for pre-contract access/intake failures.
- Counting a pre-contract drop against the mechanism's `N_expr` ladder.
- Letting the calendar/core-hour ceiling replace Rule 2's iteration tripwire.
- Requiring the alpha leg to solve inactivity after manual preservation was accepted.
- Erasing a confirmed portable edge because its edition axis fails.

## §4 — Verification

```bash
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
python scripts/check_sessions_queue_bind.py
python scripts/check_rule2_trip_log_liveness.py
python scripts/check_md_relative_links.py
```

## §5 — Ratification record

Accepted from the operator's direct 2026-09-02 elections and campaign instruction. The P50
prospective-freeze restriction and pre-contract vocabulary are reconciliations required by the
already-Accepted candidate-contract, evaluation-order, approvals, and terminal-taxonomy ADRs; they
do not narrow the elected portable-edge objective.
