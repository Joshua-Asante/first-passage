# Contract: the final research round (DRAFT, 2026-11-09)

**Status:** draft. It binds nothing until Joshua approves it, its hash is recorded by scheduled
self-email, and `order-state.json` names it. In witness mode it cannot be amended after that.
**It cannot be adopted while the open term in §4 is unsettled.**
**Under:** [The Order](../the-order.md) (itself a draft), step 1, Aim.
**Source:** the [continue-or-stop note](../../notes/audits/programme-audit/2026-11-09-continue-or-stop.md)
§4 step 2, and Joshua's words to the research coordinator on 2026-11-09: "I'll let you draft it".
**Scope:** research only. The capped eval run Joshua selected the same day (the note's option B)
is not covered here; Joshua ruled research first (§8).

Terms marked **(note)** are the note's §4 step 2, unchanged. Terms marked **(added)** come from
The Order or from this draft, and are Joshua's to accept or strike. Items 1 and 2 are his to
write; their text here is a proposal.

## 1. Objective and measure (added)

Answer one question by 2026-11-30: is there an edge at all in the landed data? Progress is
measured in decisive results: registered cards that reach a verdict and whose mapped action
happens. The round succeeds if it ends in one Codex-verified CONFIRMED card or in a clean stop.

## 2. Scarce input and base rate (added)

The scarce input is genuine edge after costs. Agents cannot produce more of it per dollar, so
agent work is paced to four cards, not to agent capacity. The programme's own record, as
description and not as a success rate: commit subjects since 2026-08-14 carry 15 FALSIFIED,
3 NULL, 2 abandoned and no CONFIRMED label, and several of them report the same result; the
builder's 16 recorded cards on MCL and MGC all stopped at the same gate; DYN-SURVEY-1 run 1 was
a partial null. The expected result of this round is no confirmed card.

## 3. Budgets and expiry

- **(note)** At most **4 cards in total**, across all instruments, covering every development
  card and every holdout attempt. K = 4 is banked whether or not a card runs to the end. No
  replacement batches, no added instruments.
- **(note, narrowed)** Eligible instruments: only those with landed, hash-registered data and
  remaining lifetime looks: the index micros, M6E and 6J. The note also lists MGC. It is left
  out: MGC is parked with eight banked cards (sitting ruling D18), and the note alone does not
  unpark it. MCL is parked the same way.
- **(note)** All four cards are named in one registration before any exploration, chosen by
  stated rationale from existing dossiers and parked cards, never by outcome.
- **(note)** A card must pass a cost re-read at the builder's frozen slip before it spends a
  look. A card that fails the re-read still counts against the four.
- **(note)** No gate is loosened, and no data is bought. **(added)** No compute or subscription
  is bought either: new spend is $0.
- **(added)** A card takes its slot when its registration is marked started in
  `order-state.json`, or when it fails its cost re-read. Taking the fourth slot does not end
  the round: the started card runs to its verdict.
- **(added)** DYN-SURVEY-1 is not part of this round. Joshua dropped its rerun on 2026-11-09
  ("Drop the rerun"); it stays closed at run 1's partial null and advances no card.
- **(note, tightened; ruled by Joshua as option (a), §8)** Deadline: 2026-11-30, not the note's
  2026-12-31, so that the eval run can follow.

## 4. Outside answers (added)

| Question | Recipient | Asked | Human answer |
|---|---|---|---|
| May exported bars be used for offline tests? | TradingView | Not yet sent; Joshua sends it himself (date recorded when sent) | None |
| Q5, T1, T2 (who may operate the account; the weekly trade's shape) | Tradeify | Not sent | None. Not needed for this round; needed before any deployment |

The Order's step 2 (Ask) requires a dated human answer before work goes on, and Joshua's
acceptance of the licence risk (sitting ruling D16) is not one. **OVERRIDE, logged under step
7:** Joshua ruled on 2026-11-09: "let's not wait for a human response. let's draft the email
and see what they say". The round therefore proceeds without the answer. **(added, proposed; Joshua
accepts or strikes)** A written refusal from TradingView received before the round ends stops
it that day: the card in progress is abandoned as NULL and its slot is spent. A yes, or
silence, changes nothing.

No route-, venue- or account-specific work is done under this contract.

## 5. Stop conditions

**(note, clarified)** The round ends when the fourth card has its verdict, when a card fails its cost
re-read and no slot is left, or at the deadline, whichever comes first. A card still running
at the deadline is recorded as NULL. **(added)** A Codex-verified CONFIRMED card ends the
round too, since it permits only the separate deployment decision below.
No extension, no replacement batch, no repair round.

**(added)** A proposal to loosen a gate, add a card or instrument, or reread a verdict also
ends the round. The note sets this term for the eval run, not for research.

**(added)** Each card's registration maps outcomes to actions before it runs:

- CONFIRMED, verified by Codex by a separate route, permits only a separate deployment
  decision, under its own contract, after quarantine, with a payout model built first (note
  §4 step 5).
- FALSIFIED or NULL closes the claim. The slot is spent and nothing is repaired.
- Each registration states the chance of a false CONFIRMED at zero edge, and Codex re-derives
  it before the run.

**(added)** Who acts. The research coordinator records each spent slot and, on the day the
round ends, opens a `closure:` PR that sets a 14-day quarantine in `order-state.json`. Joshua
merges it. From then the `order-gates` check enforces the quarantine. The quarantine covers the
whole repository: the `order-gates` check blocks new registrations, contract changes and
non-closure paths until it ends. If the round ends on 11-30, the quarantine runs to 12-14.
No second round is drafted.

**(note)** Without a Codex-verified CONFIRMED card, the programme closes on 2027-01-02. The
closing record is written in the quarantine; the eval run (§8) is the programme's only
remaining activity until that date.

## 6. Operator hours, rounds, end date

- **(note, tightened)** Joshua: at most one hour a week, for acceptance only. **(added)** That
  includes this framework's administration.
- **(added)** At most four registered tests, one active at a time; one build item; two open
  decisions.
- **(note, tightened)** End date: 2026-11-30.

## 7. Holder, stake, review (added)

No holder: witness mode (scheduled self-email plus an OpenTimestamps proof). No stake. Review on
the later of 2027-01-16 and the quarantine's end.

## 8. Rulings

**Ruled by Joshua, 2026-11-09:**
1. **TradingView:** "let's not wait for a human response. let's draft the email and see what
   they say". Logged as an OVERRIDE of Ask (§4).
2. **Order against the eval run:** "research first". The Order allows one active hypothesis,
   so the eval run starts only after this round ends.
3. **The quarantine against the eval run:** "(a) research to 11-30". The options as put to
   him, kept for the record:

**The quarantine against the eval run.** The quarantine starts the day the round
ends and lasts 14 days. The Order allows only closure work in it, and `order-gates` refuses to
start any registration until it ends. So the eval run starts only after the quarantine. Its own
terms (note §4 step 4, option B) end it on 2026-12-31, and also end it if Tradeify gives no
human answer on Q5, T1 or T2 by 2026-12-01. Q5 has not been sent. Joshua rules one of:

- **(a) Strict, research to 11-30 (recommended).** If research ends by 11-30, the quarantine
  clears by 12-14 and eval sessions may start on 12-15, leaving 11 to 12 weekdays to 12-31
  (12-25 closed, 12-24 shortened). The eval run's contract and registration merge before
  research ends, so nothing new is registered in the quarantine. Sessions still depend on the
  eval run's other terms, above all a Tradeify answer by 12-01.
- **(b) Strict, the note's 12-31.** Research may still end early, on its fourth verdict, but no
  eval window is guaranteed, and none remains if research runs to its deadline.
- **(c) Change the framework.** Let eval sessions run in the quarantine. This is not a scope
  choice: `order-gates` refuses to start a registration in quarantine whatever the paths, the
  commits must carry `closure:`, and The Order's protected rule E3 (closure-only quarantine)
  cannot be changed in witness mode. It needs an explicit change to The Order and to
  `check_order.py`, decided before the outcome it affects.

(a) is recommended because four offline cards take days, not weeks, and it keeps the Order
intact. The 12-01 Tradeify condition binds under every option: unless Joshua sends Q5 and gets
a human answer by then, the eval run ends before any option lets it start.
