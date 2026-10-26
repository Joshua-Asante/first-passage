# Q-TFYNATIVE-1 — Native Tradeify lane: candidate qualification pre-registration (DRAFT)

**Status: DRAFT. Proposed; decides nothing** ([Rule 32](../../operational_rules.md#rule-32--adrs-only-under-the-admission-rule)). It takes effect only after a Codex pre-ratification adjudication ([Rule 5](../../operational_rules.md#rule-5--a-separate-reviewer)), operator ratification and merge. No candidate is nominated here, no run is authorised, and no capital, arming or spend authority is granted ([Rule 15](../../operational_rules.md#rule-15--capital-authorization-is-separate-and-revocable)).

**Question.** Is there a strategy that can run natively at Tradeify, exclusively there, with enough edge that running it on the Select 100K evaluation and funded account has positive expected net cash over 126 trading days within a fee budget? **The decision it changes:** whether a nominated candidate may proceed to native implementation and the deployment gates, or the lane stays parked under draft 11-08 branch (d).

**Budget.** Drafting this document: one session, $0, K = 0. Each candidate later nominated by amendment adds K = 1. Spend (for example a NinjaTrader licence) is not authorised here.

## §D — Disclosure: what was seen before this draft was written

- The synthetic studies in [PASS63_CHECK.md](../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/PASS63_CHECK.md), which use Gaussian and Student-t days and no strategy data:
  - with resets, passing is mostly a fee problem;
  - first-payout cash net is negative at zero edge, about break-even near Sharpe 1–1.5, and positive from about Sharpe 2;
  - eval and funded sizing optima differ.

  These shaped the gates below. They are not evidence about any candidate.
- The 2026-10-19 ruling that no book-lineage configuration has an evidence case for this evaluation ([addendum](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-19--no-book-lineage-configuration-has-an-evidence-case-for-the-tradeify-evaluation)).
- The ORB MNQ v7 lineage record ([S4 ratification](2026-10-18-orb-mnq-v7-s4-RATIFICATION.md) and its exposure table):
  - Tradeify payability previously failed;
  - the solo panel busts at every tested size on the end-of-day clock.

  ORB MNQ v7 is paused, not failed. It is disclosed here as prior exposure, not nominated.
- No candidate's returns were examined for this draft.

## §0 — Reads (owners)

- **Route:** [Track B superseded for Tradeify](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify). Tradeify permits native NinjaScript automation. It prohibits external Python signals, bridges and the same bot across firms.
- **Draft 11-08 rules:** [addendum 2026-10-13](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-13--track-b-suspended-11-08-decision-rules-draft). Branch (b) is #807 stage 1, a read-only native toolchain assessment.
- **Firm rules:** `core/firm_rules.py` `Tradeify_Select_100K` ([Rule 16](../../operational_rules.md#rule-16--firm-rules-one-source-and-a-pre-flight)).
- **Funded-model calibration:** [Joshua-Asante/first-passage#940](https://github.com/Joshua-Asante/first-passage/issues/940).
- **Live-execution posture and gates:** [AGENTS.md](../../../AGENTS.md#live-execution-posture).

## §1 — Objective (restated; [proposed in PASS63_CHECK.md](../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/PASS63_CHECK.md))

Maximise **expected net cash = E[total payouts received − total fees paid]** over 126 trading days from the start date. Two constraints apply:
- P(total fees > B) ≤ 0.05;
- attempts stop once fees reach B without a payout.

B is an operator input (§11). P(pass) is reported but decides nothing.

## §2 — Eligibility (G0; binary, checked before any scoring)

A candidate is eligible only if all of the following hold:
1. **Native:** all signal and order logic can live in NinjaScript, with parameters fixed in the nominating amendment. There are no external signals, parameter feeds or bridges.
2. **Exclusive:** the operator signs that the strategy is not deployed, and not planned, at any other firm, as the same-bot rule requires.
3. **Not closed:** it is not a member of the book lineage closed on 2026-10-19, unless the amendment cites new mechanism evidence ([Rule 26](../../operational_rules.md#rule-26--rejections-bar-re-proposal)).
4. **Toolchain feasible:** #807 stage 1 has returned a written read-only finding that the native toolchain can express the strategy and its fixed sizing on the account.

## §3 — Admissible evidence

- **Data:** daily net P&L from the canonical feed only, CME futures TV exports ([Rule 18](../../operational_rules.md#rule-18--feeds-are-admitted-never-assumed)).
  - At least 3 years of business days, on a complete calendar.
  - Costs at `cost_per_side_usd` from `firm_rules.py`.
  - The intraday low per day is required for the drawdown clock.
- **Edge statistic:**
  - SR̂ is the annualised net Sharpe.
  - SR_LB is the one-sided 80% lower bound, SR̂ − z·SE, with Lo's (2002) standard error adjusted for autocorrelation at lags 1–5.
  - z = Φ⁻¹(1 − 0.20/K), where K is the lane's cumulative nominated-candidate count.
- **Private inputs** (Pine source, ports, account state) are read in place only. Their values never enter the repo ([Rule 13](../../operational_rules.md#rule-13--private-data-and-the-public-clone)).

## §4 — Gates, in evaluation order ([Rule 24](../../operational_rules.md#rule-24--verdicts-from-the-pre-registered-gates-in-order))

| Gate | Test | Inputs frozen before it runs |
|---|---|---|
| **G0** Eligibility | §2 items 1–4 all hold | Nominating amendment, with exclusivity signature |
| **G1** Edge, both halves | SR̂ > 0 in each chronological half, and SR_LB computed | Data window, cost settings, and all of §7 (frozen before G1, not before G2) |
| **G2** Economics | On the candidate's own days moved to SR_LB by the §7 item 4 transform (not Gaussian), all three must hold: E[net cash] > 0; P(net cash > 0) ≥ 0.50; P(fees > B) ≤ 0.05 under the stop rule | The §7 recipe, frozen before G1: the calibrated funded model (#940), the multi-payout simulator, the optimiser, the SR_LB transform and B. Eval and funded sizes come from the optimiser, not by hand |
| **G3** Incumbent state | G2 re-run from the incumbent evaluation's real state through `EvaluationState`, privately on the operator's machine. Only the verdict leaves the machine | Same as G2 |
| **G4** Native parity | Over a frozen window, the NinjaScript port on NinjaTrader playback matches the research reference on the risk path G2 used: (a) every trade has the same quantity, and ≥ 95% of trades have the same entry and exit bar; (b) on ≥ 95% of days, net P&L and the intraday low each differ by ≤ max($25, 5%); (c) replaying both day series through the evaluation rules gives the same breach days; (d) G2 re-run on the port's own day series still passes | Port commit; window; tolerances (a)–(c) |

G5 is not part of this verdict. Deployment still needs the NinjaTrader instance's own monitoring acceptance, a separate operator GO to arm, and a GO for each session ([Rule 10](../../operational_rules.md#rule-10--live-execution-gates), [Rule 11](../../operational_rules.md#rule-11--rail-operating-invariants)).

## §5 — Forbidden moves

- Change parameters, the data window, costs or B after any G1 output has been seen.
- Use SR̂ instead of SR_LB in G2, or Gaussian days when the candidate's own series exists.
- Choose eval or funded size by hand, or re-run with new seeds to change a verdict.
- Treat an evaluation pass, by simulation or live, as evidence of edge.
- Nominate a strategy that runs, or is planned, at another firm, or route anything through CrossTrade, an API or a bridge.
- Commit account figures, Pine source or port bodies.
- Score a candidate before its nominating amendment is merged.

## §6 — Verdict table (first matching row wins)

| Outcome | Verdict | Consequence |
|---|---|---|
| G0 fails | INELIGIBLE | Candidate rejected for this lane. Any re-proposal needs new mechanism evidence |
| Under 3 years of admissible data, or the frozen §7 recipe (including #940) missing | UNDETERMINED | No scoring. Fix the input, not the gate |
| G1 fails (a non-positive half) | NO-GO (edge) | Registry line, [Rule 26](../../operational_rules.md#rule-26--rejections-bar-re-proposal) |
| G2 or G3 fails | NO-GO (economics) | Registry line. Lane stays parked |
| G4 fails | NO-GO (port) | Fix the port. One re-test, counted in K |
| All pass | GO-CANDIDATE | Eligible to enter the deployment gates. No capital, arming or spend authority |

## §7 — Recipe that must exist and be frozen before G1

1. **Multi-payout simulator.** It extends `payout_sim.first_payout` to every payout within 126 days, with Tradeify's funded payout cadence, cap and buffer. It must pass a parity test: its first payout matches `first_payout` on fixed seeds.
2. **Calibrated funded rules and settings** from #940.
3. **Optimiser.** It chooses eval and funded contract counts (integers within the 80-micro cap) to maximise §1 under the constraints. It uses the transformed day distribution from item 4, resampled in 5-day blocks with each day's intraday low paired to it. Path count, seeds and the contract grid are fixed in the frozen recipe.
4. **SR_LB transform.** Each day's net P&L x is replaced by x + Δ, where Δ = (SR_LB − SR̂)·σ̂/√252 per contract and σ̂ is the daily standard deviation, so the volatility is unchanged. Each day's intraday low ℓ is replaced by min(ℓ + Δ, 0, x + Δ): because Δ ≤ 0, the full shift is applied to the low, which is conservative. No other transformation of returns or paths is permitted.

## §8 — Gate reachability (computed for this draft; [Rule 23](../../operational_rules.md#rule-23--pre-register-count-k-honestly))

SR_LB at K = 1 (z = 0.84), for an i.i.d. daily series. The annualised SE is √((1 + SR̂²/504)/Y) for Y years, so SR_LB ≈ SR̂ − 0.84/√Y:

| SR̂ \ years | 3 | 5 | 8 |
|---|---|---|---|
| 1.5 | 1.01 | 1.12 | 1.20 |
| 2.0 | 1.51 | 1.62 | 1.70 |
| 2.5 | 2.01 | 2.12 | 2.20 |
| 3.0 | 2.51 | 2.62 | 2.70 |

Under the Gaussian proxy, G2 breaks even near Sharpe 1–1.5. So a candidate with SR̂ ≈ 2 over 3 or more years can reach G2, SR̂ ≈ 1.5 is marginal, and anything below that cannot. Autocorrelation and fat tails widen the SE and lower these bounds. The gate is reachable for a strong candidate, not for a typical one. That is intended.

**Binding:** the 11-08 branch (b) decision consumes the G0 item 4 output, and a GO-CANDIDATE is the only route into the deployment gates.

## §10 — Audit hooks

- Each gate's output records the commit, input hashes and seed.
- The G3 verdict is a signed one-line private record, with no values.
- A reviewer can re-run G1, G2 and G4 from the merged amendment and the public tooling.

## §11 — Open operator decisions (to fill before ratification)

1. Fee budget B, for example $1,000.
2. Whether the lane uses the incumbent Select 100K evaluation (G3) or a fresh Select 50K. [PASS63_CHECK.md](../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/PASS63_CHECK.md) favours the 50K on fees.
3. The 126-day window start rule: the date the GO-CANDIDATE is reached, or the first trade.
4. Who nominates candidates, and the cap on K for this lane.

## §12 — Freeze procedure

1. Codex adjudicates this draft.
2. The operator fills §11 and ratifies it.
3. Merge freezes it.
4. The §7 recipe is merged and frozen, with its tests, before any nominating amendment.
5. Each candidate enters only by a merged nominating amendment (G0 inputs plus its fixed parameters) before any G1 computation.
