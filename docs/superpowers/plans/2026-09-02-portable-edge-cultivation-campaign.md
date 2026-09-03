# Portable-edge cultivation campaign — 2026-09-02

> **Status:** `AUTHORIZED — CULTIVATION OPEN; NO CANDIDATE CONTRACT YET`  
> **Operator authorization:** 2026-09-02 — “start a research campaign for the candidate contract;
> keep looking until you find a satisfactory candidate.”  
> **Clock:** 2–3 calendar days from campaign start.  
> **Capital:** none. Paper/research only; no lifecycle promotion, rail arming, or live order authority.
> **Local execution handoff:**
> [`2026-09-02-local-handoff-portable-edge-cultivation.md`](../../briefs/handoffs/2026-09-02-local-handoff-portable-edge-cultivation.md)
> **Decision owner:**
> [`2026-09-02-portable-edge-cultivation-campaign-objective.md`](../../adr/2026-09-02-portable-edge-cultivation-campaign-objective.md)

## 0. Commercial objective and operator elections

The operator has resolved the four decisions left open by the 2026-09-02 leverage memo:

1. **Primary objective:** a portable genuine edge, preferably clearing
   `Tradeify_Select_100K`.
2. **Inactivity:** a manual weekly preservation trade is acceptable. Candidate alpha does not have
   to manufacture weekly activity.
3. **Clock and spend:** 2–3 days; compute/data spend is flexible subject to the approved envelope
   and fresh-GO rule owned by the decision ADR.
4. **Edition failure:** a genuine edge is preserved if it fails the chosen Tradeify edition.

“Flexible” is not treated as an unbounded blank cheque. The initial research tranche is **$0
external data spend and ≤48 local core-hours**. Any paid dataset or cloud compute gets a priced,
candidate-specific sub-line before purchase; staying within the 2–3 day clock does not waive Rule
2. This campaign may price such a sub-line without stopping, but may not incur it without a recorded
ceiling **and a new explicit operator GO**.

## 1. Campaign thesis

A strategy may be **cultivated** rather than arriving fully formed. The correct boundary is not
“fully formed at first observation”; it is:

- a mutable **cultivation object** may combine a mechanism, an existing expression, development
  evidence, and deliberately bounded amendments;
- it does not claim candidate status, reserve or consume Confirm, or inherit validation while it
  is mutable; and
- structural/source cultivation may make signal/entry/stop/exit/sizing fields complete before
  payoff access; and
- once complete, its catalogue, contract, and K manifest freeze before the first exploration
  payoff cell is scored.

This preserves iterative strategy development without laundering development choices into
confirmation. Cultivation may grow the specification before outcome access; outcome-guided
cultivation remains source evidence and cannot be wrapped retroactively in a candidate contract.

## 2. Satisfactory-candidate definition

The campaign keeps looking until it produces one **satisfactory candidate** or the 2–3 day clock
forces an honest dry disposition. “Satisfactory” means all of the following—not merely an
interesting source result:

1. exact executable signal, side, entry, stop, exit, holding horizon, and sizing policy;
2. a frozen cost authority and realistic slippage convention;
3. development evidence supporting positive net expectancy and a non-invented payoff-shape prior;
4. no hard fail on cost, latency, session legality, integer size, or coarse first-passage geometry;
5. a founding-frozen mechanism discriminator independent of payoff: observable/statistic, null,
   expected direction, decision threshold, and coverage/power requirement;
6. for a prospectively valid B/C object, a Confirm interval whose boundaries are committed before
   outcome access and whose first eligible bar is strictly later than the founding-freeze commit;
7. one immutable candidate contract with `K`, `α=0.05`, `M=1`, and Bonferroni identity recorded;
8. portable-edge evidence kept distinct from the `Tradeify_Select_100K` edition verdict; and
9. no unresolved evidence/configuration defect capable of changing the trade identity.

This is a **candidate admission** definition, not a claim of confirmed edge. Confirmation and venue
MC remain later gates.

## 3. Campaign envelope

| Field | Freeze |
|---|---|
| Mechanism/expression families cultivated | At most 3 |
| Candidate contracts that may open | At most 1, prospectively from B/C; exact P50 excluded |
| Confirm selections | `M=1` |
| Confirm family level | `α=0.05`, Bonferroni (`α/M=0.05`) |
| Initial external spend | $0 |
| Initial compute | ≤48 local core-hours |
| Research duration | 2–3 calendar days |
| Capital/sandbox | prohibited under this envelope |
| Rescue after Confirm access | 0; changed defining field is a new campaign |
| Rule-2 class | STRATEGIC: 3 constituent OUTER investigations (seats A/B/C) |
| Per-seat iteration tripwire | OUTER: 8 complete attempt-and-check iterations; no self-extension |

The three cultivation seats are not three Confirm looks. Only a prospectively frozen catalogue may
open the one available contract/Confirm slot. At a seat's 8/8 tripwire, emit spent/remaining/state/
extend-or-stop and stop pending operator adjudication or Rule-0 re-audit.

## 4. Cultivation seat A — ORB-MYM v0.4 + P50 opening-range volume gate

**Priority:** first, because it is the only current lead coupling a complete private strategy body
to an economically material conditioner result.

**Known evidence:** on the fully viewed TradingView panel, P50 improves net P&L and profit factor
and halves displayed maximum drawdown versus `Off`; P80 is worse than P50. This is selection and
development evidence, not confirmation.

> ⚠ **Superseded in part, 2026-09-02 (same day, later):** the P50 List-of-Trades was subsequently
> supplied and reconstructed. Raw net reconciles to the cent (986 exit rows / $31,947.96), but
> through the canonical engine **at the size the headline was measured (qty 2)** Select returns
> **51.2% bust / 48.8% pass** (Growth 43.4/56.6) and the realized historical path **busts Select on
> day 42**. Seat A's "economically material conditioner result" is therefore material on raw P&L
> and **not** on survival at size — the third time this construct family has shown that split.
> Owner: [`orb_mym_v04_riskbudget_2026-09-02/RESULTS.md`](../../../lab/analysis/orb/orb_mym_v04_riskbudget_2026-09-02/RESULTS.md) §2. This does not close seat A; it
> replaces its known-evidence line.

**Prospective-admission bar:** P50 was selected from the fully viewed Off/P50/P80 source catalogue
without a prior contract or K manifest. It is therefore **ineligible to open a candidate contract
under this campaign**. Seat A may reconstruct it only as development/source evidence; exact P50
needs a separate, operator-ratified legacy-intake ruling before any prospective admission path.

**Source-evidence blockers at campaign open:** the private Pine body is absent from the repository; full
Strategy Properties and List-of-Trades were not retained; leg-level pyramiding prevents interpreting
the displayed win rate as a candidate risk-unit win rate; intraday MAE and untouched evidence are
absent.

### A0 — Identity capture

Before another payoff comparison:

- obtain the exact Pine body matching SHA-256
  `9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071`;
- retain symbol, timeframe, full Properties, date span, weekday toggles, quantity, pyramiding,
  commission, and slippage;
- export the complete List-of-Trades for the already-selected P50 setting; and
- verify the export and source hashes before reading derived metrics.

If the source hash cannot be reproduced or the configuration cannot be identified, seat A is
`EVIDENCE-BLOCKED`, not a candidate or Confirm failure.

### A1 — Risk-unit reconstruction

Aggregate pyramided legs to the actual flat-to-flat position and trading-day units. Produce N,
cadence, idle weeks, net expectancy after authoritative costs, win/loss distribution, loss runs,
worst day, drawdown, and integer-size exposure. Reconstruct MAE from source bars only if the Pine's
order semantics make that honest; otherwise mark the MAE limb `UNSCREENABLE`.

No P55/P60/P65, weekday, stop, target, or exit search is permitted. An implementation repair needed
to reproduce the existing strategy is an evidence repair; a payoff-defining change consumes a new
cultivation seat.

### A2 — Reachability and source disposition

- If generous cost/shape/integer-size assumptions clearly fail, close seat A `PRE-CONTRACT DROP
  (venue/cost-constraint-shaped)`; do not increment `N_expr` or write a candidate rejection.
- If the object is plausible but MAE is missing, price the smallest data/export step that makes it
  screenable; do not substitute EOD drawdown.
- If all fields are complete and reachability is plausible, retain P50 as source evidence and
  present the named legacy-intake ruling required by the owning ADR. Do not open a contract or call
  a future P50 window Confirm under this campaign.

The historical P50 panel supplies priors only. It cannot acquire prospective status after the fact.

## 5. Cultivation seats B and C — complete-expression sourcing

Seats B/C search for **trade objects**, not predictors. Eligible sources are executable published
rules, reproducible research packages, licensed systems with exportable ledgers, or an existing
repository expression that gains genuinely new information. Intake requires:

- exact side/entry/stop/exit/horizon rules;
- an independent mechanism discriminator with frozen statistic, null, direction, threshold, and
  coverage/power requirement;
- code or trades sufficient for independent reproduction;
- credible net-positive prior after costs;
- a hard loss boundary and enough information to estimate adverse excursion;
- a Tradeify-legal futures product at integer size; and
- an interval that can remain untouched.

An incomplete but promising object may enter cultivation and acquire missing fields on development
information that does not expose payoff outcomes. Once its catalogue is complete, it must freeze a
contract/K manifest before payoff scoring. Screenshots, parameter menus, unsigned range predictors,
and discretionary “setups” do not consume a seat.

### Search order

1. repository expressions with a complete executable body plus unconsumed data;
2. primary research with explicit implementable rules and cost-aware results;
3. audited/licensable third-party code or trade ledgers;
4. new data modalities only when attached to a declared expression.

The mined OHLCV session-geometry neighbourhood is not categorically forbidden, but a near-neighbour
must bring new causal information and an unconsumed evaluation route. Renaming another ORB/fade
window is not cultivation.

## 6. Q-VOLREGIME relationship

Q-VOLREGIME remains research infrastructure, not a candidate. Its important contribution is now
empirical: volume information appears capable of **improving an existing expression**, which is a
valid cultivation role even before the general attribution programme resolves.

The campaign therefore makes two distinctions:

1. P50 opening-range aggregate volume may cultivate ORB-MYM on its own exact expression evidence;
   it does not inherit Q-VOLREGIME's M15 mechanism identity or validation.
2. The expensive general L5 programme proceeds only on its reusable research-infrastructure value;
   it is not a prerequisite for capturing, reconstructing, or forward-testing the distinct P50
   expression.

This avoids both errors: calling Q-VOLREGIME a strategy, and discarding useful conditioner evidence
because it is not independently a strategy.

## 7. Work sequence and stop rules

### Day 1

1. capture seat-A source/config/trades or record the exact access blocker;
2. build the deterministic flat-to-flat/day aggregation packet if the export exists;
3. inventory repository expressions against §2; and
4. begin the bounded primary-source search for seats B/C.

### Day 2

1. run seat-A cost/shape/reachability if A0 cleared;
2. cultivate at most two alternatives far enough to decide whether they can satisfy §2;
3. choose at most one object prospectively; and
4. commit its Confirm/forward boundaries on the draft contract, with the first eligible bar set
   strictly after the later founding-freeze commit; exclude every intervening pre-freeze bar.

### Day 3, only if needed

1. close remaining evidence gaps that do not change the chosen expression;
2. freeze one contract and append its hash, or publish a dry campaign disposition; and
3. price—not execute—any next data step outside the initial envelope.

**Stops:** one satisfactory contract freezes; the clock expires; all three seats close; or the only
remaining work requires outcome-conditional repair. The user's “keep looking” instruction means do
not stop at the first incomplete idea; it does not authorize infinite threshold search or breaking
the 2–3 day commercial clock.

## 8. Campaign ledger

Rule-2 count at this review: seat A **1/8 OUTER iterations** (filesystem source/artifact search and
check); seats B/C **0/8**. Governance authoring/review repair is campaign setup, not an empirical
seat iteration.

| Timestamp | Event | Disposition |
|---|---|---|
| 2026-09-02 | Operator fixed portable-edge-first objective, Select preference, manual preservation acceptance, flexible spend, and edge preservation across edition failure | envelope inputs resolved |
| 2026-09-02 | Campaign opened; seat A assigned to ORB-MYM P50 | `SOURCE CULTIVATION — PROSPECTIVE CONTRACT INELIGIBLE; A0 EVIDENCE-BLOCKED` |
| 2026-09-02 | Q-VOLREGIME classified as infrastructure with a valid strategy-cultivation role | off candidate critical path |
| 2026-09-02 | External web-search tool returned HTTP 401 before results; no web evidence was admitted | environment/access event, not a seat disposition |
| 2026-09-02 | Searched `/workspace`, `/root`, and `/tmp` for the named Pine and MYM/ORB trade exports; neither the Pine nor a P50 List-of-Trades export is present | A0 access blocker confirmed; exact operator capture remains next action |
| 2026-09-02 | Authored a copy/paste local-session execution handoff with A0→A2 commands, B/C continuation, evidence rules, and required terminal states | ready for next local session after PR merge |
| 2026-09-02 | Codex review reconciliation: P50 cannot be retroactively frozen; A0 uses EVIDENCE-BLOCKED; pre-contract reachability uses PRE-CONTRACT DROP; fresh GO required above spend; Rule-2 tripwire bound | decision ADR owns durable rulings |
| 2026-09-02 | Operator supplied the P50 List-of-Trades; reconstructed and run through the canonical engine ([`RESULTS`](../../../lab/analysis/orb/orb_mym_v04_riskbudget_2026-09-02/RESULTS.md) §2) — exit-only net reconciles to the cent, but qty-2 Select/Growth bust 51.2%/43.4% and the realized path busts Select on day 42 | A0 no longer evidence-blocked; seat A's raw-metric claim stands, its survival claim does not |
| 2026-09-02 | Second Codex review reconciliation: every B/C contract must freeze an independent mechanism discriminator; Confirm begins strictly after the founding-freeze commit, not merely after the last source read | prospective contract checklist corrected |

## 9. Required terminal artifact

At campaign close, append exactly one of:

- `CONTRACT-FROZEN`: prospectively valid B/C candidate id, K-manifest id, founding hash, reserved
  Confirm span whose first eligible bar is after that founding hash's commit, frozen discriminator,
  and reachability packet;
- `DRY-CAMPAIGN`: each seat's typed reason and precise add-back condition; or
- `EVIDENCE-BLOCKED`: only when a named artifact/access step, rather than research uncertainty,
  prevents adjudication, with the next executable command or operator capture named.
