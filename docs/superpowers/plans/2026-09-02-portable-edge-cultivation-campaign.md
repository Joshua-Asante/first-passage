# Portable-edge cultivation campaign — 2026-09-02

> **Status:** `AUTHORIZED — CULTIVATION OPEN; NO CANDIDATE CONTRACT YET`  
> **Operator authorization:** 2026-09-02 — “start a research campaign for the candidate contract;
> keep looking until you find a satisfactory candidate.”  
> **Clock:** 2–3 calendar days from campaign start.  
> **Capital:** none. Paper/research only; no lifecycle promotion, rail arming, or live order authority.

## 0. Commercial objective and operator elections

The operator has resolved the four decisions left open by the 2026-09-02 leverage memo:

1. **Primary objective:** a portable genuine edge, preferably clearing
   `Tradeify_Select_100K`.
2. **Inactivity:** a manual weekly preservation trade is acceptable. Candidate alpha does not have
   to manufacture weekly activity.
3. **Clock and spend:** 2–3 days; compute/data spend is flexible.
4. **Edition failure:** a genuine edge is preserved if it fails the chosen Tradeify edition.

“Flexible” is not treated as an unbounded blank cheque. The initial research tranche is **$0
external data spend and ≤48 local core-hours**. Any paid dataset or cloud compute gets a priced,
candidate-specific sub-line before purchase; staying within the 2–3 day clock does not waive Rule
2. This campaign may price such a sub-line without stopping, but may not incur it without a recorded
ceiling.

## 1. Campaign thesis

A strategy may be **cultivated** rather than arriving fully formed. The correct boundary is not
“fully formed at first observation”; it is:

- a mutable **cultivation object** may combine a mechanism, an existing expression, development
  evidence, and deliberately bounded amendments;
- it does not claim candidate status, reserve or consume Confirm, or inherit validation while it
  is mutable; and
- once it has exact signal/entry/stop/exit/sizing fields and passes the cheap reachability screen,
  it freezes into the one candidate contract required by the candidate-contract ADR.

This preserves iterative strategy development without laundering development choices into
confirmation. Cultivation is allowed to grow the plant; the contract fixes the genotype before the
untouched test.

## 2. Satisfactory-candidate definition

The campaign keeps looking until it produces one **satisfactory candidate** or the 2–3 day clock
forces an honest dry disposition. “Satisfactory” means all of the following—not merely an
interesting source result:

1. exact executable signal, side, entry, stop, exit, holding horizon, and sizing policy;
2. a frozen cost authority and realistic slippage convention;
3. development evidence supporting positive net expectancy and a non-invented payoff-shape prior;
4. no hard fail on cost, latency, session legality, integer size, or coarse first-passage geometry;
5. a genuinely untouched or forward Confirm interval reserved before final specification freeze;
6. one immutable candidate contract with `K`, `α=0.05`, `M=1`, and Bonferroni identity recorded;
7. portable-edge evidence kept distinct from the `Tradeify_Select_100K` edition verdict; and
8. no unresolved evidence/configuration defect capable of changing the trade identity.

This is a **candidate admission** definition, not a claim of confirmed edge. Confirmation and venue
MC remain later gates.

## 3. Campaign envelope

| Field | Freeze |
|---|---|
| Mechanism/expression families cultivated | At most 3 |
| Candidate contracts that may open | At most 1 |
| Confirm selections | `M=1` |
| Confirm family level | `α=0.05`, Bonferroni (`α/M=0.05`) |
| Initial external spend | $0 |
| Initial compute | ≤48 local core-hours |
| Research duration | 2–3 calendar days |
| Capital/sandbox | prohibited under this envelope |
| Rescue after Confirm access | 0; changed defining field is a new campaign |

The three cultivation seats are not three Confirm looks. They are pre-contract development objects;
only one may freeze and only one Confirm slot exists.

## 4. Cultivation seat A — ORB-MYM v0.4 + P50 opening-range volume gate

**Priority:** first, because it is the only current lead coupling a complete private strategy body
to an economically material conditioner result.

**Known evidence:** on the fully viewed TradingView panel, P50 improves net P&L and profit factor
and halves displayed maximum drawdown versus `Off`; P80 is worse than P50. This is selection and
development evidence, not confirmation.

**Contract blockers at campaign open:** the private Pine body is absent from the repository; full
Strategy Properties and List-of-Trades were not retained; leg-level pyramiding prevents interpreting
the displayed win rate as a candidate risk-unit win rate; intraday MAE and untouched evidence are
absent. Therefore **opening the candidate contract now would violate the candidate-contract ADR**.

### A0 — Identity capture

Before another payoff comparison:

- obtain the exact Pine body matching SHA-256
  `9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071`;
- retain symbol, timeframe, full Properties, date span, weekday toggles, quantity, pyramiding,
  commission, and slippage;
- export the complete List-of-Trades for the already-selected P50 setting; and
- verify the export and source hashes before reading derived metrics.

If the source hash cannot be reproduced or the configuration cannot be identified, seat A is
`EVIDENCE-VOID`, not a candidate failure.

### A1 — Risk-unit reconstruction

Aggregate pyramided legs to the actual flat-to-flat position and trading-day units. Produce N,
cadence, idle weeks, net expectancy after authoritative costs, win/loss distribution, loss runs,
worst day, drawdown, and integer-size exposure. Reconstruct MAE from source bars only if the Pine's
order semantics make that honest; otherwise mark the MAE limb `UNSCREENABLE`.

No P55/P60/P65, weekday, stop, target, or exit search is permitted. An implementation repair needed
to reproduce the existing strategy is an evidence repair; a payoff-defining change consumes a new
cultivation seat.

### A2 — Reachability and contract decision

- If generous cost/shape/integer-size assumptions clearly fail, close seat A `EXPRESSION-FAIL`.
- If the object is plausible but MAE is missing, price the smallest data/export step that makes it
  screenable; do not substitute EOD drawdown.
- If all founding fields are complete and reachability is plausible, reserve future data beginning
  strictly after the last viewed eligible bar, then open and hash the candidate contract.

The historical P50 panel supplies priors only. Confirm must be genuinely forward because the
threshold catalogue and panel are viewed.

## 5. Cultivation seats B and C — complete-expression sourcing

Seats B/C search for **trade objects**, not predictors. Eligible sources are executable published
rules, reproducible research packages, licensed systems with exportable ledgers, or an existing
repository expression that gains genuinely new information. Intake requires:

- exact side/entry/stop/exit/horizon rules;
- code or trades sufficient for independent reproduction;
- credible net-positive prior after costs;
- a hard loss boundary and enough information to estimate adverse excursion;
- a Tradeify-legal futures product at integer size; and
- an interval that can remain untouched.

An incomplete but promising object may enter cultivation and acquire missing fields on development
data. It may not open a contract until §2 is satisfied. Screenshots, parameter menus, unsigned
range predictors, and discretionary “setups” do not consume a seat.

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
4. reserve its Confirm/forward interval before final contract freeze.

### Day 3, only if needed

1. close remaining evidence gaps that do not change the chosen expression;
2. freeze one contract and append its hash, or publish a dry campaign disposition; and
3. price—not execute—any next data step outside the initial envelope.

**Stops:** one satisfactory contract freezes; the clock expires; all three seats close; or the only
remaining work requires outcome-conditional repair. The user's “keep looking” instruction means do
not stop at the first incomplete idea; it does not authorize infinite threshold search or breaking
the 2–3 day commercial clock.

## 8. Campaign ledger

| Timestamp | Event | Disposition |
|---|---|---|
| 2026-09-02 | Operator fixed portable-edge-first objective, Select preference, manual preservation acceptance, flexible spend, and edge preservation across edition failure | envelope inputs resolved |
| 2026-09-02 | Campaign opened; seat A assigned to ORB-MYM P50 | `CULTIVATING — CONTRACT BLOCKED ON A0` |
| 2026-09-02 | Q-VOLREGIME classified as infrastructure with a valid strategy-cultivation role | off candidate critical path |
| 2026-09-02 | External web-search tool returned HTTP 401 before results; no web evidence was admitted | environment/access event, not a seat disposition |
| 2026-09-02 | Searched `/workspace`, `/root`, and `/tmp` for the named Pine and MYM/ORB trade exports; neither the Pine nor a P50 List-of-Trades export is present | A0 access blocker confirmed; exact operator capture remains next action |

## 9. Required terminal artifact

At campaign close, append exactly one of:

- `CONTRACT-FROZEN`: candidate id, founding hash, reserved Confirm span, and reachability packet;
- `DRY-CAMPAIGN`: each seat's typed reason and precise add-back condition; or
- `EVIDENCE-BLOCKED`: only when a named artifact/access step, rather than research uncertainty,
  prevents adjudication, with the next executable command or operator capture named.
