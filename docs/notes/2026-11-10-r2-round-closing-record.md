# R2 research round: closing record (2026-11-10)

**Status:** closed. Zero cards registered, zero consumed. Quarantine 2026-11-10 to 2026-11-24
(`docs/framework/order-state.json` at `1a16212`).
**Written by:** the research coordinator (Claude), in the quarantine, as contract §5 requires.
Codex reviews it. Joshua's paragraph in §7 is his, by hand.
**Contract:** [`2026-11-09-final-research-round-contract-DRAFT.md`](../framework/contracts/2026-11-09-final-research-round-contract-DRAFT.md),
sha256 `d6add078…5017f0`, merged 2026-11-10 at `456452c`.

## 1. What stopped

The R2 round: at most four pre-registered cards testing whether a systematic futures strategy
has an edge after costs, to end by 2026-11-30. Joshua stopped it on 2026-11-10 ("Stop the
round"), on the day its contract merged. It was a discretionary stop. None of the contract's
stop conditions (§5) had fired: no fourth card, no deadline, no CONFIRMED card, no refusal
from TradingView, no proposal to loosen a gate.

No card was registered, so there is no CONFIRMED, FALSIFIED or NULL verdict to record, and no
registered mapping to execute.

## 2. Why it stopped now

The Choose step produced no card that could be registered, and the time left could not
change that.

**Three proposals, all stopped before any return was read:**

| Proposal | Outcome | Record |
|---|---|---|
| GAPFAIL-1 (MNQ cash-open gap failure) | Closed on trade count: 56 trades in 2020–2024, floor 200 | [`MNQ.md`](../../ops/instruments/MNQ.md), 2026-11-10 entry |
| Q-HARV-THR-1 (threshold rebalancing, MES) | FAILED-COUNT: sparse expressions 57 and 142 events; the daily one declined as not sparse | [`ES.md`](../../ops/instruments/ES.md), 2026-11-10 entry |
| ANNPREM-1 (CPI and jobs-report days, ES/MES) | Withdrawn by its author: it re-cites the announcement-day class that Q-INVENTORY-1 closed | [`rejected_candidates.md`](../rejected_candidates.md), Q-INVENTORY-1 entry |

**What bound the round:**
- **Count.** Owned daily history starts 2010-06. An event that happens once a month reaches
  about 193 events, under the 200-event floor the proposals were held to.
- **Closed classes.** The proposals drawn from published work fell inside classes already
  closed, whose reopening needs new external evidence.
- **No evaluation route.** The builder runs opening-range cards only, and R2 bars
  opening-range variants. Any other card needed an evaluator that did not exist.
- **Power.** Codex's arithmetic (gate 5f only, independent outcomes): with 400 development
  events, an edge is detected 80% of the time only at about 0.12 to 0.18 standard deviations
  per event for K of 1 to 5. That is roughly an annual Sharpe of 0.9 to 1.3 for a weekly
  event.
- **Time.** Twenty days remained. Codex judged a schedule to source, build and independently
  verify an evaluator, register and run inside them "not credible as an acceptance plan".

Stopping on 2026-11-10 ends the quarantine on 11-24. A round run to its deadline would have
ended it on 12-14.

## 3. What this does and does not show

It shows that this round, with this data, budget and time, established no registration-ready
card. It does **not** show that no admissible card exists, or that no edge exists. Codex's
end-round review put it this way: "zero registration-ready cards have been established."

## 4. Left untested

Named in Codex's end-round review, and not assessed for ancestry, count or an evaluation
route:
- timing within the cycle between FOMC meetings;
- weekly option-expiry hedging and unwind;
- weekly or biweekly salary-flow timing;
- the same questions on other index micros.

Also unresolved, and unchanged by this round: MGC and MCL stay parked with eight banked
builder cards each, and their K still counts.

This list is a record of what was not done. It is not a plan. Under The Order a closed claim
reopens only on a new external fact that is dated after closure, meets the reopening
condition and was registered before it was observed.

## 5. Work done under the contract (Subtract)

Merged 2026-11-10, each reviewed clean by Codex at its exact head with CI green:

| PR | Change |
|---|---|
| #1181, #1183 | Dead core/ops and lab code removed |
| #1182, #1184 | GAPFAIL-1 and Q-HARV-THR-1 closures recorded |
| #1185 | 2026-11-10 rulings on recommendations 1 and 5–8 recorded; STATE updated |
| #1186, #1187, #1192, #1193 | DYN-SURVEY code, `breadth`/`cov_prekill`, the Stage-2/4 miner and gate 5h removed |
| #1188, #1189 | Lint config removed; deployment proposal marked superseded; one backtest dollar figure redacted |
| #1190, #1191 | Two vendor-derived data files removed; `pine_check` removed |
| #1194 | This closure: step Stop and the quarantine |

Kept until 2026-11-30 by ruling: `builder_5e_check` and `pine_lint.py`. Recommendations 2, 3
and 4 of the 2026-11-09 rulings stay open.

## 6. Chronology of the stop, and departures

All on 2026-11-10. Times are UTC, from GitHub.

1. The research session withdrew ANNPREM-1, and the coordinator asked whether to end the
   round with zero cards. Joshua had Codex review that first. Codex: a zero-card stop is
   allowed as a discretionary stop, and the record must not claim the search was exhausted.
2. **Joshua: "Stop the round".** The coordinator's message before it listed the quarantine
   dates.
3. 19:57 the coordinator merged #1193 (gate 5h removal). 19:59 it opened closure PR #1194.
4. Joshua asked why there is a two-week quarantine, and whether a profitable strategy could
   be found under current conditions. He then asked for a spec for further testing. The
   coordinator declined to draft it, citing the quarantine.
5. **Joshua withdrew the stop:** "I didn't remember that by stopping the round I was enabling
   a 14 day quarantine, or else I wouldn't have stopped it. I meant to stop this particular
   approach, but I do want to continue the strategy research".
6. The coordinator treated that as a clarification. 20:08 it closed #1194 unmerged, told the
   research session the round continued, drafted a Choose-method spec and sent it to Codex.
   Joshua ruled on one of the spec's questions, and the research session returned a
   dates-only data inventory.
7. **Codex:** "NOT DEFENSIBLE as written. The sourcing method could fit an otherwise active
   round, but the draft cannot establish continuation merely because the STOP was withdrawn
   before its enforcement PR merged." Its reading: a programme STOP starts the quarantine
   when it is ruled, the merge only turns on enforcement, and witness mode has no mechanism
   to withdraw one.
8. **Coordinator (Claude):** "I think Codex's reading is right: continuing is an override of
   protected rule E3, and I should have put it to you that way."
9. **Joshua: "The stop stands".** 20:37 #1194 reopened at the head Codex had reviewed.
10. 20:42 and 20:43 Joshua merged #1190 and #1191. 20:50 the coordinator merged #1194.

**Departures, logged as The Order requires:**
- **Work during the quarantine.** On the reading that the quarantine began at step 2, steps
  3 to 6 and 10 include work that was not closure work: three Subtract merges (#1193, #1190,
  #1191), a spec draft and its review, one ruling on that spec, and direction to the
  research session. The spec and its review were never committed and are set aside. The
  ruling in step 6 has no effect, because the round it applied to is closed.
- **Same-day reversal.** The stop was withdrawn and reinstated on the day it was ruled. Codex
  notes this is not automatically The Order's same-day-ruling breach, which concerns ruling
  on the day results appear.
- **Security review.** #1190 and #1191 changed ignore rules and the boundary layer map and
  merged without the `@codex security review` comment AGENTS.md asks for.
- **Coordinator's error.** It should have presented the withdrawal as an override decision
  and sought Codex's review before acting on it.

No override was taken. Joshua was offered a logged override to continue and declined it.
That is one "attractive continuation declined and logged at the time" under The Order's own
test of the framework.

## 7. Joshua's paragraph

*By hand, in the quarantine: should this objective continue at all, and what else could these
hours buy?*

> _(to be written by Joshua)_

## 8. Numbers for the weekly review

| Measure | Value |
|---|---|
| Decisive results (registered verdicts whose action happened) | 0 |
| Proposals closed before registration | 3 |
| Cards registered / consumed | 0 / 0 |
| Operator hours | not measured for this round |
| Spend | none |

## 9. Not affected

The eval coda (R12) starts Mon 2026-11-16 outside The Order, each session under its own GO.
Its public records are on the quarantine's closure paths.
