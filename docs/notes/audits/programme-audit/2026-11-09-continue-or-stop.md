# Continue or stop: the automated futures prop programme (2026-11-09)

**Asked by:** Joshua, 2026-11-09: "make a clear case for and against continuing … I want to know
at this point whether the programme is worth pursuing."
**Method:** seven evidence streams (edge, economics, external base rates, venue, operations,
assets and alternatives, the live pair), then a continue advocate and a stop advocate, a round of
rebuttal and a judge. Claude checked the deciding repo claims directly. External figures come from
the web-research stream and are marked *(external, not re-checked)*. Private figures (backtest
results, per-account dollars) were used in the analysis but are not reproduced here. Builds on the
[programme audit](2026-11-08-programme-audit.md).
**Codex challenge:** requested on this PR.

## Verdict (Claude)

**Stop the programme. It is not worth pursuing in its current or any expanded form.** The record
since 2026-08-14 is the expected outcome for this kind of search on this data, not bad luck.
Nothing on the horizon would change that without new outside evidence.

The owned evaluation is not a reason to continue. Joshua may still use it as a short, capped
coda, but only if he actively wants to sit the sessions, and only under terms registered before
session 1 (§4). The default recommendation is a full stop.

Both advocates reached this position independently. After rebuttal, the continue advocate's own
revised thesis was "stop the programme now; the only exception is an optional harvest of the paid
ticket".

## 1. The case for continuing (steelmanned)

1. **The one real experiment has never been run.** Three months produced a native, Sim101-tested
   pair on an owned eval, with a hash-registered forward stop rule. No strategy-signal fill has
   ever happened (STATE.md). Stopping now leaves the forward question unread for good.
2. **The marginal cash cost is small.** The eval is paid for. If the AI subscriptions are cut, the
   running cost falls to the data line.
3. **"No confirmed edge" is weak evidence of "no edge".** The engine is underpowered. A true
   annualised Sharpe of 1.0 rarely clears the builder gate at K = 8 on about 3 years of data (that
   gate needs about 1.73; `git show 5510ca96^:docs/notes/2026-11-01-generation-phase-strengthening-DRAFT.md` §8.1).
   Order flow, longer native history and pooled designs are untested, not falsified.
4. **The payoff is asymmetric.** Loss is capped at fees. Tradeify allows owned native bots, and
   the native build ports to other NinjaTrader firms (two affirmed automation in writing on 11-05).
5. **Some mechanism-backed intraday effects exist in the literature** (late-day index momentum,
   *external, not re-checked*).

## 2. The case for stopping

1. **There is no edge to run, and the live pair failed its own test.**
   [`pair_evidence_case_2026-11/RESULTS.md`](../../../../lab/analysis/c1/pair_evidence_case_2026-11/RESULTS.md):
   "PRIOR STANDS". The pair fails the August gate at eval sizing in both halves (Codex-verified,
   #1151 and #1170). D1 records that no out-of-sample edge is established. Commit subjects since
   08-14 show 15 FALSIFIED, 3 NULL, 2 ABANDON and 0 confirmed.
2. **The research engine cannot change that on the data the programme keeps.** The builder gate
   needs an annualised Sharpe of about 1.73 at K = 8 on about 3.2 years of TradingView data
   (§8.1 above). The best futures-native edge ever measured here is well below that, and the
   literature's top-decile net Sharpe for this class is about 0.85. More search only raises K.
   Recent independent tests of ORB and OHLCV intraday momentum on NQ/MNQ find a small gross signal
   that costs consume *(external, not re-checked)*.
3. **The eval barely tells skill from luck.**
   [`PASS63_CHECK.md`](../../../../lab/analysis/_inbox/prop_payout_geometry_2026-10/PASS63_CHECK.md):
   the probability of passing within 63 days is 0.15 at zero edge and 0.39 at an annualised Sharpe
   of 2.0, a Sharpe the pair has never shown. A pass is worth a likelihood ratio of about 2 at best.
   Comparable books need many months to pass, so any capped run most likely ends inconclusive.
4. **Even success has a low ceiling, and one counterparty controls it.** Exclusivity (D4) keeps the
   logic at Tradeify. Funded accounts are few, correlated and payout-capped, on a simulated account
   the firm can refuse to pay. `core/firm_rules.py` has no funded, payout or scaling rows.
   T1, T2 and Q5 have no written answer from a human, and Q5 has not been sent. Tradeify's
   October 2026 compliance FAQ lists accounts controlled by someone other than the registrant as a
   violation, which bears on the agent-operated premise *(external, not re-checked)*. Industry data
   show that a small minority of evaluation buyers are ever paid *(external, not re-checked)*.
5. **At zero edge the economics are roughly fair before costs and negative after them.** The
   recurring overhead is $370/mo ([ledger](../../../pursuits/SUBSCRIPTION_LEDGER.md)), mostly
   AI tooling. Breaking even needs a live after-cost Sharpe of about 1 or more on one account.
6. **Joshua's attention is the binding cost, and nothing here saves it.**
   - The record: daily merges, rulings on most days, and a 20-decision sitting.
   - Every session needs its own GO and must be attended to the 16:45 ET force-flat.
   - Under D8 he places the weekly trade by hand.
   - The "automated" strategy needs a human throughout.
7. **The programme has shown it will not stop itself.** It loosened gates after adverse results,
   and it narrowed a fired falsifier after the outcome was known (audit Q4 and Q7). A wind-down has
   to be ruled now, before any outcome, or the next result will be absorbed the same way.

## 3. What survived the rebuttal round

- **Continue side.**
  - Survived: the forward read is otherwise lost, and the marginal cash cost is small.
  - Did not survive: "a pass is strongly informative" (refuted by PASS63); "ORB has a
    mechanism-backed effect" (that evidence is for ORB-MNQ-1, and D1 says nothing transfers to
    O-0); "the failures were management failures, so fixable" (the market-facing results are
    negative either way).
- **Stop side.**
  - Overstated: the length of an uncapped run, and some economics drawn from unreviewed scenario
    code.
  - None of those carry the verdict. Points 1–3 above carry it on their own.

## 4. What stopping means

**Ruled now, before any outcome:**
1. The programme ends as an investment. Stop all generation: the November channel, DYN-SURVEY-1
   and the 16 parked cards. No new tooling, rail, gates or governance documents.
2. Cut recurring spend to the data line or zero by 2026-11-30, unless the AI subscriptions serve
   other work. Close the open ledger rows.
3. Choose one:
   - **(A) Full stop (default).** Stop the weekly preservation trade, let the eval lapse, write one
     closing RESULTS file (counts and hashes only) and archive.
   - **(B) Coda.** Only if Joshua positively wants to sit the sessions. Register before session 1,
     labels only:
     - a bust retires the pair and ends the prop path;
     - zero resets and zero purchases at any firm;
     - a hard cap of 20 attended sessions or 2026-12-31, whichever comes first, with no extension;
     - a stop-rule drop or halt ends it;
     - any human objection from Tradeify, or silence on Q5, T1 or T2 past 2026-12-01, ends it;
     - a proposal to loosen anything after an outcome ends it;
     - a pass authorises nothing; a funded stage would be a new decision with a payout model built
       first.

     The coda buys closure and a small lottery chance, not evidence.
4. Close the programme by 2027-01-02 in every case.

**Kept:** the negative knowledge (the rejection register, closures and K ledgers), the validation
and Monte Carlo engines, the native build, and the operating lessons (requirements first; register
the kill rule before the outcome).

## 5. What would reopen it

Only new outside evidence, not momentum:
- a pre-registered, Codex-verified CONFIRMED result at an honestly reconciled K, on deeper native
  data obtained under a rights ruling at a fixed budget;
- or a written answer from a human at Tradeify clearing T1, T2 and Q5, together with a reviewed
  funded and payout model showing positive cash at a Sharpe the candidate has actually shown.
