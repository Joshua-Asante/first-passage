# Contract: the research round (2026-11-09)

**Status:** awaiting Codex review of this head, then Joshua's approval of the whole text. It
binds once its hash is recorded by scheduled self-email and `order-state.json` names it. In
witness mode it cannot be amended after that.
**Under:** [The Order](../the-order.md), adopted 2026-11-09 in witness mode (R10), step 1, Aim.
**Source:** the research terms in the [2026-11-09 rulings](../../notes/2026-11-09-rulings.md)
(R2, R7), the [continue-or-stop note](../../notes/audits/programme-audit/2026-11-09-continue-or-stop.md)
§4 step 2, and Joshua's rulings to the research coordinator listed in §8.
**Scope:** research only. The capped Tradeify eval run starts Mon 11-16 outside The Order,
under stop-rule Addendum 2 (#1178), and nothing in it continues, extends or rescues this
round, or the reverse. It needs a ruling that replaces R3 and money control 1, which the
Tradeify deployment coordinator owns.

Items 1 and 2 are Joshua's: he accepted their text on 2026-11-09 ("items 1 and 2 are acceptable
as written"). Other terms are marked **(R2)**, **(R7)** or **(note)** by source, or **(added)**
when they come from The Order or the research coordinator's draft.

## 1. Objective and measure (Joshua)

Find credible evidence of a systematic futures edge after costs, among the cards registered in
this round only. Four cards can close their own claims; they cannot show that no edge exists.

Progress is measured in decisive results: registered verdicts whose mapped action actually
happens. A clean stop counts as the process working, not as finding an edge.

## 2. Limiting input and comparable cases (Joshua)

The limiting input is an after-cost edge large enough to tell apart from selection on the
evidence that is left. Effect size, sample size and honest K decide that together, and the
remaining look budget is part of it. Agents can avoid wasting looks; they cannot create more
independent evidence. So agent work is paced to the cards that evidence can support, not to
agent capacity.

Comparable cases, all checkable:
- M6E: one prospectively registered expression rejected on costs
  (`lab/analysis/fx/m6e_european_breakout_2026_11/RESULTS.md`);
- R3 dossiers: 0 of 28 cells survived a literature and cost screen that read no market data
  (`git show 5510ca96^:docs/briefs/dossiers/R3/INDEX.md`);
- the MCL and MGC builder banks: 8 cards each, MCL's run validity unresolved;
- the builder power calibration: synthetic, so it gives detection odds, not how common real
  edges are (`lab/analysis/_inbox/builder_power_2026-11/RESULTS.md`);
- DYN-SURVEY-1 run 1: partial null (private run report
  `local_artifacts/sourcing-2026-11/dyn-survey-1-out/report.json`, sha256
  `d9117410be67aeaaeb6df86a48703c0cc3383927684fcd1689293c3eb4293fbc`).

No numerical base rate is defensible from these. The expected result, no confirmed card, is a
judgment, not an estimated probability.

## 3. Budgets and expiry

- **(R2)** One round, with a ceiling of 4 new cards. A slot may stay unused: four is a ceiling,
  not a quota.
- **(R2)** Allocation: 2 or 3 index-micro cards, each from a different mechanism family (sparse,
  low-turnover timing effects with a stated mechanism, not ORB parameter variants); at most 1
  MGC card, only if it was specified before the unread outcomes; no card from the cost-killed
  6J/M6E breakout families. Cards are not chosen because they fit the existing builder.
- **(R2)** All cards are named together in one registration before any result. Each records
  its ancestry and its reconciled historical K. MGC's and MCL's 8 banked cards each still
  count. The 4-card ceiling is not K.
- **(added)** A card that cannot show, before any result is opened, that its ancestry is
  reconciled and its test is still informative at that K is not registered; its slot stays
  unused.
- **(R2)** The cost re-read at the frozen slip is a kill test. No loosening, replacement,
  repair, neighbour or direction-flip card.
- **(R7)** Spend is the data line only. **(added)** No new data, compute or subscription is
  bought.
- **(added)** A card is consumed when its registration is marked started in `order-state.json`,
  or when it fails its cost re-read. R2's "ends at 4 consumed cards" is read as: no fifth card
  is started, and the fourth runs to its verdict.
- **(added)** DYN-SURVEY-1 is not part of this round: Joshua dropped its rerun ("Drop the
  rerun"). It stays closed at run 1's partial null.
- **(R2, tightened by Joshua, §8)** Deadline: 2026-11-30, not R2's 2026-12-31.

## 4. Outside answers (added)

| Question | Recipient | Asked | Human answer |
|---|---|---|---|
| May exported bars be used for offline tests? | TradingView | Not yet sent; Joshua sends it himself (date recorded when sent) | None |

The Order's step 2 (Ask) requires a dated human answer before work goes on, and Joshua's
acceptance of the licence risk (sitting ruling D16) is not one. **OVERRIDE, logged under step
7:** Joshua ruled "let's not wait for a human response. let's draft the email and see what they
say". The round proceeds without the answer. **(added; accepted by Joshua)** A written refusal
from TradingView received before the round ends stops it that day: the card in progress is
abandoned as NULL and its slot is spent. A yes, or silence, changes nothing.

No route-, venue- or account-specific work is done under this contract.

## 5. Stop conditions

**(R2, clarified in §3)** The round ends when the fourth consumed card has its verdict, or at the
deadline, whichever comes first. A card still running at the deadline is recorded as NULL.
**(added)** A Codex-verified CONFIRMED card, or a TradingView refusal (§4), also ends it. No
extension, no replacement, no repair round.

**(added)** A proposal to loosen a gate, add a card or instrument, or reread a verdict also ends
the round.

**(added)** Each card's registration maps outcomes to actions before it runs:

- **(R2)** CONFIRMED, verified by Codex by a separate route, opens only a separate deployment
  decision under its own contract (own-account economics, legal status, venue, current costs),
  after the quarantine.
- FALSIFIED or NULL closes the claim. The slot is spent and nothing is repaired.
- Each registration states the chance of a false CONFIRMED at zero edge, and Codex re-derives it
  before the run.

**(added)** Who acts. The research coordinator records each consumed card and, on the day the
round actually ends, opens a `closure:` PR that sets a 14-day quarantine in `order-state.json`.
Joshua merges it. From then `order-gates` enforces it repo-wide: it refuses new registrations
and registration starts, requires every commit to carry `closure:`, and allows only the paths
in `closure_paths`. A round that ends at the deadline gives a quarantine from 11-30 to 12-14;
an earlier end moves it earlier. The closing record is written in the quarantine.

**(added; accepted by Joshua)** Because the eval run may still be going during the quarantine,
the same PR sets `closure_paths` to the default closure paths (which already include
`docs/notes/*`) plus the eval run's public records, as the Tradeify deployment coordinator
listed them:

- `STATE.md`;
- `docs/briefs/pre-registration/2026-10-31-tradeify-forward-stop-rule-registration*` (the stop
  rule and the addenda it allows), not the whole folder, so no research registration draft can
  change;
- `docs/spec/*` (the build spec and the attended-session procedure, between sessions only);
- `AGENTS.md` (the money-control text, when Joshua re-rules after Q5);
- `docs/evidence/PRIVATE_EVIDENCE.sha256` (the hash index, if session records are registered).

The check fixes `closure_paths` for the whole quarantine, so they must be named when it starts.
It does not read content: during the quarantine these paths could change for any reason,
research included, and only review stops that. This changes neither The Order nor
`check_order.py`.

**(R2)** There is no automatic second round. Another needs new outside evidence, not cheaper
search.

## 6. Operator hours, rounds, end date

- **(R7, tightened)** Joshua: at most one hour a week for this round, for acceptance only,
  including this framework's administration. The eval run's hours are outside this cap.
- **(added)** At most four registered tests, one active at a time; one build item; two open
  decisions.
- **(R2, tightened by Joshua)** End date: 2026-11-30.

## 7. Holder, stake, review (added)

No holder: witness mode (scheduled self-email plus an OpenTimestamps proof). No stake. Review on
the later of 2027-01-16 and the quarantine's end.

## 8. Rulings

**Ruled by Joshua, 2026-11-09, typed to the research coordinator unless stated:**
1. **TradingView:** "let's not wait for a human response. let's draft the email and see what
   they say". Logged as an OVERRIDE of Ask (§4).
2. **Survey:** "Drop the rerun".
3. **Research deadline:** "(a) research to 11-30", then "keep 11-30" after the eval moved
   alongside research.
4. **Eval start:** "keep 11-16", and "Mon 11-16" to the Tradeify deployment coordinator; after
   #1177 merged, "I want to keep the eval from 11-16".
5. **The eval run and The Order:** "Coda outside Order", typed to the Tradeify deployment
   coordinator and relayed verbatim (options: "Coda outside Order", "Amend the Order").
6. **The §4 refusal stop and the §5 closure paths:** "Accept both".
7. **Items 1 and 2:** "items 1 and 2 are acceptable as written", of the text put to him after
   Codex's input.
