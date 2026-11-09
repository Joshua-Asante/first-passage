# Contract: the final research round (DRAFT, 2026-11-09)

**Status:** draft. It binds nothing until Joshua approves it, its hash is recorded by scheduled
self-email, and `order-state.json` names it. In witness mode it cannot be amended after that.
**It cannot be adopted while either open decision below is unsettled.**
**Under:** [The Order](../the-order.md) (itself a draft), step 1, Aim.
**Source:** the [continue-or-stop note](../../notes/audits/programme-audit/2026-11-09-continue-or-stop.md)
§4 step 2, and Joshua's words to the research coordinator on 2026-11-09: "I'll let you draft it".
**Scope:** research only. The capped eval run Joshua selected the same day (the note's option B)
is not covered here (open decision 2).

Terms marked **(note)** are the note's §4 step 2, unchanged. Terms marked **(added)** come from
The Order or from this draft, and are Joshua's to accept or strike. Items 1 and 2 are his to
write; their text here is a proposal.

## 1. Objective and measure (added)

Answer one question by 2026-12-31: is there an edge at all in the landed data? Progress is
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
- **(added)** A slot is spent when its card's registration is marked started in
  `order-state.json`, or when the card fails its cost re-read.
- **(added)** DYN-SURVEY-1 is not part of this round. Joshua dropped its rerun on 2026-11-09
  ("Drop the rerun"); it stays closed at run 1's partial null and advances no card.
- **(note)** Deadline: 2026-12-31.

## 4. Outside answers (added)

| Question | Recipient | Asked | Human answer |
|---|---|---|---|
| May exported bars be used for offline tests? | TradingView | Not asked | None |
| Q5, T1, T2 (who may operate the account; the weekly trade's shape) | Tradeify | Not sent | None. Not needed for this round; needed before any deployment |

The TradingView row is unsatisfied, and under The Order's step 2 (Ask) that blocks the round:
Joshua's acceptance of the licence risk (sitting ruling D16) is his acceptance, not an outside
answer, and spending nothing does not discharge it. See open decision 1.

No route-, venue- or account-specific work is done under this contract.

## 5. Stop conditions

**(note)** The round ends when the four cards are spent or on 2026-12-31, whichever comes
first, unless a card has reached CONFIRMED under the frozen gates and Codex has verified it.
No extension, no replacement batch, no repair round. **Without a Codex-verified CONFIRMED card,
the programme closes on 2027-01-02.**

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
merges it. From then the `order-gates` check enforces the quarantine. If the round ends on
12-31, the quarantine runs to 2027-01-14, the closing record is written and the programme
closed inside it by 2027-01-02, and closure-only limits continue to its end. No second round is
drafted.

## 6. Operator hours, rounds, end date

- **(note, tightened)** Joshua: at most one hour a week, for acceptance only. **(added)** That
  includes this framework's administration.
- **(added)** At most four registered tests, one active at a time; one build item; two open
  decisions.
- **(note)** End date: 2026-12-31.

## 7. Holder, stake, review (added)

No holder: witness mode (scheduled self-email plus an OpenTimestamps proof). No stake. Review on
the later of 2027-01-16 and the quarantine's end.

## Open decisions (Joshua)

1. **TradingView.** Either Joshua asks TradingView in writing whether exported bars may be used
   for offline tests, and the round waits for a dated human answer (a refusal ends it); or the
   round runs under the note alone and not under The Order, and this contract is withdrawn.
   No recommendation: this is a choice about which rule governs.
2. **Order against the eval run.** The Order allows one active hypothesis, and separate
   contracts do not lift that limit. Both end on 2026-12-31, so running them in sequence
   shortens one of them. Joshua rules one of: research first, then the eval run; the eval run
   first, then research; or side by side as a stated exception, with each contract barring
   its result from being used to continue the other. Recommended: research first. Four
   offline cards take days, and the eval run still waits on its own steps.
