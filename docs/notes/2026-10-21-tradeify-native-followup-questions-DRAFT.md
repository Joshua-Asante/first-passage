# Tradeify follow-up questions for a native NinjaScript strategy (DRAFT, unsent)

**Status:** DRAFT for Joshua to send; not sent. Serves prerequisite P0.1 of the [native strategy plan](../superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md#2-prerequisites-before-any-build-operator-owned).

**What it replaces:** the 2026-10-13 five-question draft, which is not in this repo, for the native lane only. Its clause and §1.3-consent questions served the bridge route, which was superseded on 2026-10-16 ([addendum](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify)).

**How to send:** reply on ticket #144659998 (replying reopens it) or open a new ticket. Ask for written answers, and for the governing clause where one exists. Before sending, add the account reference privately; this public file deliberately omits account identifiers.

**What each answer decides:**

| Question | Answer decides |
|---|---|
| Q1 | Whether the plan's build is allowed at all. A no stops the plan (P0 stop rule). |
| Q2 | Whether the plan's build is allowed at all. A no stops the plan (P0 stop rule). |
| Q3 | Operating setup (P5–P6). |
| Q4 | Operating setup (P5–P6). |
| Q5 | Candidate eligibility (decision D2). |
| Q6 | Decision D4. |
| Q7 | Scale-up (P7). |
| Q8 | CME prerequisite P0.2, alongside CME ticket #04738415. |

---

## Message (paste-ready)

> Hello,
>
> Thank you for the October 12 replies. They confirmed that, for evaluation and Sim Funded accounts, all strategy logic must be native to a supported platform such as NinjaTrader (NinjaScript), and that external engines, bridges and direct API access are not permitted. I have dropped the external-engine approach entirely. I am now planning a strategy that runs only inside NinjaTrader 8, on my own PC, under Tradeify's NinjaTrader license, connected through Tradovate. Before I build it, could you confirm the following in writing? Where a rule comes from the Funded Trader Agreement or another agreement, please cite the clause.
>
> 1. **Offline development, fixed parameters.** I would research and test the strategy offline, using my own tools, including Python, and then compile it into a self-contained NinjaScript strategy with fixed input values. While it trades, every calculation, signal, position size and order happens inside NinjaTrader, with no external program, file feed or connection. Is that "native" under your rules for evaluation and Sim Funded accounts?
> 2. **Automated strategies under Tradeify's NinjaTrader license.** Does the Tradeify company NinjaTrader license allow an enabled NinjaScript strategy to submit, modify and cancel orders automatically on my evaluation and Sim Funded accounts? Are there restrictions on strategy features, such as ATM strategies, the Strategy Analyzer or Playback for testing, or unmanaged order handling?
> 3. **Ownership verification.** The guidelines say you may require a live video of me enabling the code on my own PC. When is this requested, at purchase, at payout or on review, and what must it show? I will write the strategy myself, with help from AI coding assistants and standard NinjaTrader indicators. Does that still count as "sole owner"?
> 4. **Where it runs.** The strategy would run on a dedicated PC at my home. Is it acceptable for that PC to run unattended during the session, and to check on it through a remote-desktop tool from my own devices? I understand that logging in over a VPN or VPS is not allowed.
> 5. **Meaning of "the same bot across multiple firms."** If a strategy at another firm shares a general idea, for example an opening-range rule, but is a separately written program with different logic and parameters, is it "the same bot"? What test do you apply?
> 6. **Personal accounts.** The guidelines say I may use the bot on my personal accounts. Does that include a personal, non-prop Tradovate brokerage account in my own name, running the same strategy at the same time as my Tradeify accounts?
> 7. **Several Tradeify accounts.** May I run the same NinjaScript strategy on each of my own Tradeify accounts, either as a separate instance per account or through NinjaTrader's multi-account order handling, with every account trading in the same direction? Will the "similar orders on other accounts" scan treat this as permitted grouping of my own accounts?
> 8. **Market data for automated use.** Your supported-platforms page says Level 1 CME data is included. Does that data licence cover an automated (non-display) NinjaScript strategy on evaluation and Sim Funded accounts, or must I hold a separate CME licence?
>
> Thank you,
> Joshua

---

## Notes

- **Omitted on purpose:**
  - **Agent-placed orders** (routes note route 4): the native plan doesn't need them.
  - **TradingView manual signals**: routes 2 and 3 are not part of this plan.
  - **The bridge clause:** branch (a) was withdrawn on 2026-10-16.
- **Already settled; not asked again:**
  - eval lock;
  - platform list;
  - Select Flex payout rules;
  - account limits;
  - same-direction copying is allowed;
  - hedging across own accounts is banned.

  These are in [Q-PATH-TO-PAYOUT-1 §5](research/2026-10-21-q-path-to-payout-1-memo.md#5-verification-of-open-items-2026-10-21).
- **Recording the answers:** record them as an addendum to the [route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md), where the 2026-10-12 guidance lives, and update the plan's P0 row.
