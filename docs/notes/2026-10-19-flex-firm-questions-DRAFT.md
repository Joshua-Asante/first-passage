# FundedNext and FXIFY Flex 150K: written questions before any purchase (DRAFT, 2026-10-19)

**Status:** DRAFT for Joshua to send. Nothing has been sent.
- Funded by Joshua on 2026-10-19 as Step 3 item 1 of the [qualification proposal](2026-10-19-flex-qualification-candidate-proposal.md): "Fund Step 3 item 1 now: draft the FundedNext and FXIFY firm questions for me to send, through the coordinator's eligibility register."
- Narrowed the same day to questions that can change basis selection, gate E (funded economics) or a blocking ruling.

**Routing:**
- Joshua sends both emails from his own account.
- Replies go to the coordinator's eligibility register. The register owns firm facts and the dated FXIFY-vs-FundedNext note (EMERY-RESEARCH-DOCS-1).
- Raw replies stay in Joshua's mailbox or a gitignored private store. Public notes carry sanitized rule answers only, with no ticket numbers, names or addresses.
- FXIFY rule-sheet corrections go to the #867/#869 writers.

**Sources:**
- Each question was mapped to current official pages read 2026-10-19: FundedNext help articles dated 2026-09-30 to 10-14; FXIFY FAQs updated 2026-09-28; the FXIFY GTC, footer 6 Dec 2024, sha256 `c25d2fa8…abfc72f`.
- The full source map, with each question's documented position and sources, goes to the coordinator with this draft. It is not committed.

**Disclosure:**
- The emails name instruments and long/short directions, because the hedging and cap rules turn on them.
- They name no other firm, sizes, parameters, results, account identifiers or private data.
- They describe a planned setup; no native implementation exists yet.

**Supersedes:** venue-note [§12](2026-10-14-funded-venue-alternatives-assessment.md) FXIFY Q1–Q8, whose sent status is unverified.
- Q1–Q3 (CrossTrade and bridge routes) are moot for the native route.
- The rest map as follows: Q4 to FX-5b (deferred); Q5 to FX-3; Q6 to FX-2; Q7 to FX-7 and FX-N2 (deferred); Q8 to FX-N8.
- **Before sending,** Joshua confirms whether any of Q1–Q8 already went out by email, chat or ticket. If one did, Email 2 cites that thread.

---

## Email 1: FundedNext Futures (7 questions)

**To:** support@fundednext.com, the published written channel. A chat answer counts only once it is confirmed by email.
**Subject:** Pre-purchase questions: Flex 150K Challenge and Flex FundedNext Account

> Hello,
>
> Before buying a Flex 150K Challenge, I would like a short written answer to each question below, with the rule or clause it rests on.
>
> My planned setup: my own self-written automated strategies, one per instrument, running natively as NinjaScript strategies in NinjaTrader 8 on the FundedNext-issued Tradovate login. They would run on my own PC or a dedicated VPS, sometimes attended and sometimes unattended. They trade intraday only and are flat before the daily close. One account may hold a **short full-size Japanese yen (6J)** position at the same time as **long Micro Dow (MYM)** and **long Micro Gold (MGC)** positions.

1. **Automation and hosting.** Is this setup permitted in both the Flex Challenge and the Flex FundedNext Account? If the VPS trading IP differs from the IP I use for the dashboard, does terms 2.1.7 require prior approval? If so, how do I request it?
2. **Correlated instruments.** Under terms 2.2.13 and the prohibited-strategies article, is holding short 6J while long MYM or long MGC in one account a prohibited hedge of correlated instruments? Which instruments share an "Asset Group", and where is that list published?
3. **Contract cap.** For the 8-mini / 80-micro cap, does one full-size 6J contract count as one mini? Is the cap a total across all instruments held at once?
4. **Strategy source code.** Under terms 2.2.6, can FundedNext require me to provide strategy source code, or only a description and execution records? Does the ToS 14.2 content licence apply to anything provided?
5. **Maximum Loss Limit trail.** The challenge article says the limit updates from the "highest balance that day", while terms 1.2.15 and 1.2.19 refer to the end-of-day balance. Does the threshold trail the day's closing balance or the highest balance reached during the day? Is the Flex FundedNext Account the same?
6. **Withdrawals.** The Flex FundedNext 150K withdrawal limit is up to 50% of "accumulated profit" per cycle, max $4,000.
   - Is "accumulated profit" the profit since the last withdrawal, the whole balance above the starting balance, or another basis?
   - Is the $4,000 cap applied to the requested amount, before the 95% share, or to the amount paid after it?
7. **After the 5th reward.** When the 5th Performance Reward concludes a Flex FundedNext Account, what follows: a live account, or nothing? If a live account, are automated NinjaScript strategies allowed there?

> Thank you.

---

## Email 2: FXIFY Futures (8 questions)

**To:** support@fxifyfutures.com. GTC §12.2 names this address, and §12.1 makes email written communication.
**Subject:** Pre-purchase questions: Flex 150K evaluation and Flex Funded

> Hello,
>
> Before buying a Flex 150K evaluation, I would like a short written answer to each question below, with the article or GTC clause it rests on.
>
> My planned setup: my own self-developed automated strategies, one per instrument, running natively as NinjaScript strategies in NinjaTrader 8 on the FXIFY-issued Tradovate connection. They would run on my own computer or a dedicated VPS, sometimes attended and sometimes unattended. They trade intraday only and are flat before 4:59 PM ET. One account may hold a **short full-size Japanese yen (6J)** position at the same time as **long Micro Dow (MYM)** and **long Micro Gold (MGC)** positions.

1. **News trading by automated strategies.** Your EA article says an EA that breaks your Prohibited Trading Strategies policy causes an immediate breach, and it gives news trading as an example. That policy's only news item is "High Leverage News Trading". Your News Trading Policy says news trading is allowed.
   - Which news trading by an automated strategy is prohibited on the Flex evaluation and Flex Funded?
   - What counts as "large, leveraged", which events count, and what window counts as "around" them?
   - May an automated strategy hold positions with resting stops through scheduled releases?
2. **The 30-day evaluation.** Can the Flex evaluation be extended more than once? If so, at what fee and for how many days each time? Are the 30 days calendar days or trading days?
3. **Automation and hosting.** Is this setup permitted on both the Flex evaluation and Flex Funded? Is any notice, approval, VPS restriction or disclosure of strategy code required?
4. **Instruments and the cap.** Are full-size 6J (including short positions) and Micro Gold (MGC) tradable? Does one 6J count as one mini against the 10-mini / 100-micro cap?
5. **Several instruments in one account.** Is holding short 6J alongside long MYM and long MGC in one account treated as hedging, "one-sided bets" or "overexposure" under GTC 5.4.1.4 or 5.4.1.7?
6. **The lock during the evaluation.** Does the "Locking the Drawdown" rule apply during the Flex 150K evaluation, fixing the threshold at $150,000 once the end-of-day balance reaches $154,500? Or does it apply only on Flex Funded?
7. **Payouts and add-ons.**
   - Your payout policy's example applies the cap before the split and reduces the balance by the payout. After the first payout, is "total trading returns" the balance above the $150,000 start, or the profit since the last payout? Is "total account returns", used for the $1,500 minimum, the same measure?
   - Of the checkout add-ons (Daily Loss Limit removal, the +$250 limit, the 100% split), which apply during the evaluation, and which carry into Flex Funded?
8. **The funded agreement.** Can you send the Flex Funded agreement before purchase? Does it end the account after a number of payouts, or describe a move to a live account?

> Thank you.

---

## How replies feed the proposal (for the register)

Keyed by item and source-map ID.

| Proposal item | FundedNext | FXIFY |
|---|---|---|
| Basis selection (§5 Step 3 item 2) | 1 (FN-3), 2 (FN-2), 3 (FN-1), 7 (FN-11) | 1 (FX-2), 2 (FX-1), 3 (FX-N1), 4 (FX-3), 5 (FX-N3) |
| Gate E, funded economics (item 3) | 6 (FN-10), 7 (FN-11) | 2 (FX-1), 7 (FX-6 and FX-4), 8 (FX-N8) |
| Blocking rulings: private source, hedging (item 4) | 1 (FN-3), 2 (FN-2), 4 (FN-9) | 3 (FX-N1), 5 (FX-N3), 8 (FX-N8) |
| Kernel features (items 5–6) | 5 (FN-4) | 6 (FX-8), 7 (FX-4) |

**Rules for reading replies:**
- Silence counts as no.
- A yes from either firm on running strategies elsewhere does not clear Tradeify. Its help desk says a bot must be used only within Tradeify ([replies record](2026-10-10-tradeify-exclusive-use-replies.md)).

**The Tradeify weekly trade is not asked about.** Two placements avoid FundedNext 1.2.21 and FXIFY's reverse-trading ban:
- keep that trade out of the book's instruments and their likely Asset Groups; or
- place it only while the FundedNext or FXIFY account is flat.

That choice is Joshua's.

## Deferred questions

Deferred until the answers above leave a basis standing. None of them changes basis selection or gate E on its own.

| Firm | Deferred question | Why deferred | Source-map id |
|---|---|---|---|
| FundedNext | 3:10 PM CT auto-close as a breach; half-day closes | The strategy is flat by 16:00, and shortened sessions are denied | FN-6 |
| FundedNext | "Before major market events": which events, what window | No news rule is published | FN-7 |
| FundedNext | Profit-target basis (closed P&L or equity) | Modelling detail | FN-5 |
| FundedNext | Per-symbol commissions | The cost rule already fixes a conservative default | FN-8 |
| FundedNext | Same own strategies in other accounts (copy/group policy; terms 2.2.5) | A program question, not this qualification | FN-12 |
| FundedNext | Does included data cover automated use? | CME ticket #04738415 is the authority | FN-13 |
| FundedNext | Flex 150K and reset prices (official pages conflict) | Read at checkout without buying | FN-14 |
| FXIFY | MLL breach clock (intraday or end-of-day) | The harness already models the conservative case (intraday) | FX-7 |
| FXIFY | GTC 5.4.1.2 "external data feed" | Low risk on the native route | FX-5b |
| FXIFY | GTC 5.4.1.6 gap clause | Intraday only; it binds only before long closures | FX-5a |
| FXIFY | 4:59 PM auto-close; holiday flat times; meaning of "EST" | The strategy is flat by 16:00 | FX-N2 |
| FXIFY | DLL basis | The add-on can remove it | FX-N6 |
| FXIFY | Profit-target basis | Modelling detail | FX-N7 |
| FXIFY | "Tight brackets" prohibition | A behavioural rule; ask before any native build | FX-N9 |
| FXIFY | Commissions and fees | The cost rule already fixes a conservative default | FX-N4 |
| FXIFY | Does supplied data cover automated use? | CME ticket #04738415 is the authority | FX-N5 |
