# MNQ Pine → Tradeify — vet, generate, confirm, deploy outcome map

**Status:** `DRAFT · NO GO` — planning map only; authorizes no data pull, candidate
freeze, Pine promotion, lifecycle change, rail emission, order, or spend.  The
operator queue and every existing approval gate remain unchanged.

**Objective:** use the repository's MNQ evidence to produce one auditable,
falsifiable Pine v6 `strategy()` whose deployable expression can survive the
`Tradeify_Select_100K` evaluation geometry and can be reproduced on the ruled
Python signal host.  A positive outcome is not a good TradingView equity curve:
it is a chain of named artifacts in which every stage can honestly stop the work.

**Important architecture boundary:** Pine is the executable research and
TradingView export instrument.  It is **not** the live signal host.  The ruled
production path remains Python daemon → listener → CrossTrade → Tradovate, with
TradingView login automation prohibited.  Therefore “deployable Pine strategy”
means Pine/Python-identical strategy logic that clears venue scoring and then is
implemented on S2b; it does not mean routing a TradingView alert directly to the
account.

---

## 1. What the existing MNQ research says before we start

| Evidence | Decision for this plan |
|---|---|
| The frozen `ORB-MNQ-1` is `FALSIFIED_PARKED`. | It is evidence and a negative control, not a candidate to unpark or quietly retune. |
| `orb_mnq_recon_v3` is the best-known DD-reduction research iteration, but its k=1 intraday-honest bust is **20.78%**, versus the live **5.0%** ceiling; it is unregistered, selected through iterative tuning, begins only in 2022, and uses an MAE proxy. | Use it to identify failure geometry and to test the pipeline.  Do not call it a seed, survivor, or baseline pass. |
| The recon panel has 913 exits / 664 trade-days, 37.5% scale-in days, and constant quantity 2. | Pyramiding is a first-class candidate dimension and a likely incompatibility.  The new trade object defaults to no pyramiding unless a fresh venue-shape ruling says otherwise. |
| The corrected overnight-window work invalidated the prior large `Q-RANGECOND-1` effect. | Any overnight feature must use the corrected, strictly pre-entry 18:00–09:30 ET definition and pass Pine/Python fixture parity; the retracted result supplies no promotion evidence. |
| The existing `lab/pine` artifact is an `indicator()`, not a strategy, and exposes a known Python/Pine overnight-window parity boundary. | It is a diagnostic input only.  Close that boundary before reusing any of its features in a candidate. |
| The venue-edition ledger has no live Tradeify edition. | A research pass cannot inherit a deployment slot, size, or authorization from Striker or ORB. |

**Canonical threshold ruling:** use the 2026-08-26 survivor-scoring prereg v2
for the current evaluation ceiling: Run-2 headline bust ≤5.0% and P(pass) ≥50%
on at least two frozen $100K firms, including one `trailing_locking` firm.  The
older TNEC spec and viable-sequence overview still print 3.0%; treat that as
document skew, not a second selectable threshold.  Tradeify-only success may be
operationally deployable but does not discharge the programme-wide multi-firm
gate.

---

## 2. End-to-end stage map

```text
VET                 GENERATE / FREEZE             CONFIRM
evidence ledger  -> candidate contract         -> untouched holdout
failure geometry -> frozen Pine strategy()      -> Pine/Python parity
dedup / defects   -> append-only selection      -> cost + regime battery
STOP or one lane    freeze                        firm-geometry MC
                                                      |
                                                      v
DEPLOYABILITY       VENUE EDITION / DRY RUN      LIVE (operator gated)
N-ACT..N-SIZE    -> S2b Python implementation -> M1 RESOLVED
multi-firm gate     identity replay              B7-REFIRE + per-session GO
```

Every arrow is a gate, not a work suggestion.  A fail closes or returns the
candidate to diagnostics; it never licenses editing a frozen parameter against
the same holdout.

### Stage V — Vet the inherited evidence

**V1 — Build the evidence ledger.** Create a compact table for each MNQ family
actually considered: exact artifact/hash, data span, timeframe, session clock,
cost law, K status, look-ahead/parity defects, Pine status, and terminal verdict.
At minimum include frozen ORB, recon-v3, corrected overnight/range work,
selection-ceiling work, TNEC constructs, and MNQ tape/order-flow campaigns.

**V2 — Separate reusable facts from contaminated choices.** Reusable facts are
venue geometry, tick/cost law, corrected clocks, observed stop/MAE distributions,
and failure modes.  Contaminated choices include recon-v3's tuned parameters,
any threshold chosen after inspecting its 2022–2026 curve, and any feature whose
confirm window was already read.  Contaminated choices may form priors or
negative controls, never confirm evidence.

**V3 — Rank failure modes, not attractive curves.** The first scorecard is:

1. trailing-locking bust path and intraday adversity;
2. scale-in/pyramiding exposure;
3. cost turnover and ≥4× round-trip-cost hurdle;
4. 40% consistency extending time at risk;
5. weekly activity and session legality;
6. 2019–2021 / crash-regime omission;
7. timezone, overnight, and next-bar execution identity.

**V4 — Choose exactly one route.** Either (A) a genuinely new, complete trade
template whose mechanism predicts the required payoff shape, or (B) no candidate.
Do not revive the withdrawn Avenue-A Route-B checklist, unpark `ORB-MNQ-1`, or
promote a conditioner/correlation without an entry, stop, target/exit, and holding
horizon.  A dry vet is a valid positive process outcome.

**Vet exit artifact:** an evidence ledger plus one-page decision packet saying
`OPEN CONTRACT <id>` or `STOP — NO TRADEABLE TEMPLATE`, with every excluded family
and reason recorded.

### Stage G — Generate one frozen, executable candidate

**G0 — Open the campaign envelope and candidate contract before exploration.**
Use the accepted candidate-contract doctrine: one append-only, hash-addressed
contract for one fixed trade template and its declared catalogue.  Freeze:

- MNQ symbol/roll rule, bar resolution, `America/New_York` session windows, and
  complete signal → entry → hard stop → target/exit → max-hold object;
- same-bar/next-bar semantics, confirmed-bar rule, stop/target ordering,
  pyramiding (default 0), sizing method, and every exposed Pine input;
- exploration and untouched confirm windows, schema ladder, costs, K manifest
  run ID, catalogue size, alpha, confirm count `M`, and Holm/Bonferroni method;
- scoped `Tradeify_Select_100K` compliance snapshot and deployable integer-size
  assumptions; and
- Python/Pine parity fixtures and tolerances, fixed before either output is read.

No search starts until the contract K equals the `register_search.py` manifest K.
No separate preregistration may restate and drift these fields.

**G1 — Reject impossible payoff shapes cheaply.** Run the existing payoff-shape,
cost-geometry, and reachability pre-gates before any paid/high-resolution pull.
The candidate must plausibly satisfy no-pyramid hard-stop integrity, micro sizing,
session flatness, costs, activity, and the trailing rope.  A fail ends the campaign;
it does not invite a parameter sweep.

**G2 — Author Pine as the frozen test instrument.** Produce a Pine v6
`strategy()`—not an indicator—with explicit commission/slippage, session and
timezone behavior, confirmed signal timing, `process_orders_on_close` behavior,
pyramiding, stop/target precedence assumptions, and date filters.  Pin its hash.
Because the 2026-08-31 Hypothesize-exit ADR is still `Proposed`, this step is the
plan's candidate deliverable, not a claim that the ADR is already standing law.

**G3 — Explore only the frozen catalogue.** Score every declared cell on the
exploration window, charge every manual TradingView Tester look to K, and emit the
complete ranking—not only the winner.  Missing/skipped cells remain disclosed.

**G4 — Append the selection freeze.** Select at most the predeclared `M`, append
cell IDs, parameters, complete ranking, output hashes, and multiplicity procedure
to the contract, then seal exploration.  If no cell clears the frozen economic and
mechanism bars, close `MARKET-NULL` or `EXPRESSION-FAIL` as applicable.

**Generate exit artifact:** a pinned candidate contract, K manifest, Pine hash,
parity-fixture specification, full exploration results, and append-only selection
freeze.  Nothing at this point is “confirmed.”

### Stage C — Confirm once, then score the deployable expression

**C0 — Integrity preflight.** Before opening the holdout, verify commit ordering,
contract/hash integrity, zero window overlap, declared K/M correction, corrected
time windows, and sufficient holdout coverage.  Any prior holdout read is
`EVIDENCE-VOID`, not a waiver.

**C1 — Pine/Python semantic parity.** On frozen event rows and session fixtures,
compare signal timestamps, direction, entries, exits, stop/target resolution,
quantity, and trade count.  Declare irreducible TradingView fill-model differences
in advance.  A mismatch is `EXPRESSION-FAIL`; it is not repaired after viewing P&L.

**C2 — One atomic untouched-holdout run.** Execute only the selected cell(s) on
the reserved window.  Report the mechanism discriminator and net trade outcome
separately so `MARKET-NULL` cannot be relabeled as an implementation issue.  Apply
the frozen multiplicity procedure.  No sibling timeframe, added filter, alternate
stop, or “one more TradingView look” is allowed.

**C3 — Realism and robustness battery.** Require all of:

- native MNQ cost law and ≥4× cost hurdle at deployable turnover;
- intraday-honest bar/event reconstruction, not daily P&L plus MAE proxy;
- temporal slices including 2019–2021 where data availability permits, both-half
  sign/quality checks, drop-top-year, regime slices, and admission CUSUM;
- gap-through-stop and session-boundary behavior;
- no-pyramid hard-stop and integer-contract expression; and
- TradingView list-of-trades reconciliation to the Python trade ledger.

**C4 — Firm-geometry Monte Carlo.** With the frozen daily/intraday path, run the
canonical engine at 10,000 simulations × seeds 42/123/2026, horizon 1500.  Run
consistency off and on, but gate Tradeify on Run-2 (`consistency_rule_pct=40`).
Score daily/static/trailing headline bust and P(pass), using the actual
`trailing_locking` floor and never a generic percentage-of-peak substitute.

**C5 — Confirm verdict.** Use only the accepted terminal vocabulary:
`CONFIRMED`, `MARKET-NULL`, `EXPRESSION-FAIL`, or `EVIDENCE-VOID`, with `VENUE-FAIL`
as the orthogonal venue axis.  `CONFIRMED` still does not authorize deployment.

---

## 3. The positive-outcome contract

A **research-positive** outcome exists only when all of these are true:

- the candidate was defined before its exploration and holdout were read;
- Pine v6 compiles and its strategy semantics match the Python reference fixtures;
- the untouched confirm verdict is `CONFIRMED`, net of frozen MNQ costs and
  multiplicity;
- results remain credible outside the attractive 2022–2026 recon window and do
  not depend on a look-ahead/scope-gap clock; and
- all outputs, hashes, K, manual Tester looks, and failures are append-only and
  reproducible.

A **Tradeify-deployable** outcome additionally clears, at deployable integer size:

| Gate | Evidence required |
|---|---|
| `N-ACT` | At least one trade per Mon–Fri week by construction (or a separately scored book); no token-trade assumption hidden inside strategy results. |
| `N-SURV` | Run-2 intraday-honest headline bust ≤5.0% and P(pass) ≥50% on `Tradeify_Select_100K`; both-half/regime caveat passes. |
| `N-EDGE` | Net expectancy >0, 95% CI excludes 0, DSR clears its K-dependent floor, and deployable gross edge clears the ≥4× cost hurdle. |
| `N-SHAPE` | No-pyramid hard-stop integrity, gap tail disclosed, flat/session/legal micro expression, and no occupancy conflict. |
| `N-SIZE` | Risk per trade is below the candidate's measured edge frontier at a stated bust tolerance; no inherited `$325` or Striker sizing. |
| Programme gate | The v2 cross-firm rule clears on ≥2 frozen firms including ≥1 `trailing_locking`; a Tradeify-only pass is labeled exactly that and does not discharge this limb. |

A **deployment-positive** outcome additionally completes the existing Phase-D
chain without collapsing its controls:

1. lifecycle `CANDIDATE` admission with CUSUM/death certificate and a registered
   Tradeify venue edition;
2. identical strategy logic implemented on `ops/c1_signal_daemon/` and replayed
   against the Pine/Python fixture ledger;
3. real non-zero strategy event emitted with `dry_run=true`, followed by M1
   acceptance and operator signoff;
4. `validate_c1_monitoring_acceptance.py --require-resolved` green;
5. operator-only B7-REFIRE, hours-scoped `armed_until`, separate per-session GO,
   broker-side protection decision, and clean disarm/reconciliation; and
6. first fill recorded through EventLedger, with no parameter or sizing edits
   outside lifecycle controls.

The final success sentence should be mechanically fillable:

> `<candidate-id>` is `CONFIRMED`; Pine hash `<sha>` equals Python reference
> behavior on `<fixture-hash>`; `Tradeify_Select_100K` Run-2 bust is `<x>%` and
> P(pass) is `<y>%` at `<k>` MNQ; N-ACT/N-EDGE/N-SHAPE/N-SIZE are PASS; the
> multi-firm limb is `<PASS|TRADEIFY-ONLY>`; M1 is `RESOLVED`; venue edition
> `<id>` completed one attended, reconciled strategy-signal fill and was
> disarmed cleanly.

---

## 4. Stop rules and decision points

| Point | PASS | Honest stop |
|---|---|---|
| Vet | one uncontaminated, complete trade template | no contract; publish dry inventory |
| Shape/reachability | plausible venue-compatible payoff before data spend | close pre-freeze; do not tune |
| Explore | selected cell clears frozen bars | empty selection; bank K correctly |
| Parity | byte-/fixture-faithful Pine↔Python behavior | `EXPRESSION-FAIL` |
| Confirm | untouched, multiplicity-adjusted evidence | `MARKET-NULL` or `EVIDENCE-VOID` |
| Realism | result survives honest costs, clocks, tails, regimes | research-only |
| Tradeify MC | bust/pass/shape/activity/size all clear | `VENUE-FAIL` |
| Multi-firm | v2 ≥2-firm rule clears | label `TRADEIFY-ONLY` or programme fail |
| Deployment | M1 + operator gates + reconciled fill | remain disarmed |

No numerical gate may move after a result is visible.  A changed signal, stop
family, target family, or holding horizon is a new contract and new K—not an
amendment to rescue the old one.

---

## 5. Recommended first packet (bounded, no research run)

The next packet should perform **Vet only**:

1. enumerate the inherited MNQ families into the V1 evidence ledger;
2. mark every panel/window already read and every known clock/parity defect;
3. derive a failure-geometry brief from recon-v3 without copying its parameters;
4. nominate at most one complete trade template—or record `STOP`;
5. draft, but do not open, the candidate-contract founding freeze; and
6. return the explicit operator decision: `GO CONTRACT`, `REVISE TEMPLATE`, or
   `STOP MNQ`.

This packet costs $0, consumes no new K, does not touch the confirm holdout, and
keeps the highest-value decision—whether a genuinely uncontaminated candidate
exists—before Pine polishing or data spend.

## 6. Source map

- Current posture and ruled host: [`CLAUDE.md`](../../../CLAUDE.md) §Live-execution posture.
- Dynamic pipeline and retired bridge: [`PIPELINES.md`](../../../PIPELINES.md) P1–P6.
- Existing strategy/evidence: [`orb_mnq_CARD.md`](../../../core/strategies/orb/orb_mnq_CARD.md) and [`recon-v3 RESULTS`](../../../lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/RESULTS.md).
- Candidate freeze doctrine: [`candidate-contract ADR`](../../adr/2026-08-30-candidate-contract.md) and [`evaluation-order ADR`](../../adr/2026-08-30-evaluation-order.md).
- Pine test-instrument proposal: [`hypothesize-exit ADR`](../../adr/2026-08-31-hypothesize-exit-pine-test-instrument.md).
- Venue scoring: [`survivor-scoring prereg v2`](../../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) and [`firm_rules.py`](../../../core/firm_rules.py).
- Tradeify edition state: [`Tradeify_Select_100K.md`](../../../ops/venue_editions/Tradeify_Select_100K.md).
- Pine diagnostic boundary: [`lab/pine/README.md`](../../../lab/pine/README.md).
- Existing deployment chain: [`Phase D`](2026-08-23-viable-strategy-phase-d-deployment.md).
