# Tradeify follow-up for a native NinjaScript strategy (DRAFT v2, unsent)

**Status:** DRAFT for Joshua to send; not sent. Serves the [native strategy plan](../superpowers/plans/2026-10-21-tradeify-native-ninjascript-strategy-plan-DRAFT.md#2-prerequisites-by-what-they-gate) before any strategy is enabled on an evaluation account. It is not a prerequisite for bounded offline research or prototyping, which existing internal approvals govern.

**History:**
- **v1** (commit d2807b7c) asked eight questions.
- **v2** follows Joshua's 2026-10-21 triage: one statement of the architecture, then one priority eligibility question. The other topics are routed or deferred (§2).
- **Replaces:** for the native lane only, the 2026-10-13 five-question draft, which is not in this repo. Its bridge-route questions lapsed with the [2026-10-16 supersession](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-10-16--track-b-superseded-for-tradeify).

**How to send:**
- Reply on ticket #144659998 (replying reopens it) or open a new ticket.
- Add the account reference privately; this public file omits it.
- Fill the bracketed candidate details once decision D2 names the rule. If the candidate is not a published rule, rewrite the question rather than send it as is.

## 1. Message (paste-ready once the brackets are filled)

> Hello,
>
> Thank you for the October 12 replies on evaluation and Sim Funded accounts. I have dropped the external-engine approach. What I plan is a NinjaScript strategy that runs entirely inside NinjaTrader 8 under Tradeify's NinjaTrader license, connected through Tradovate. Every calculation, signal, position size and order happens in NinjaScript while it trades, with fixed inputs and no external program, file feed or connection. Research and testing happen offline beforehand.
>
> **My question is about ownership and exclusivity.** The strategy would be my private NinjaScript implementation of a published trading rule: [rule name; authors; publication; year]. It would use the published parameters, [or: parameters I selected]. I write the code with the help of AI coding assistants, and no one else has access to it or uses it.
>
> 1. Does a private implementation of a published rule, written this way, meet Tradeify's requirement that I be "the sole owner of the bot or strategy"? Does it also meet the bot exclusivity terms in the Funded Trader Agreement §6.6–6.7?
> 2. If it does, what evidence would establish that, for example the source code, development records, or a written description of the rule and its source?
> 3. Your October 8 reply said ownership must be provable on request. For a strategy like this, is any verification required before I enable it on an evaluation account, or only on request?
>
> Thank you,
> Joshua

## 2. Topics not in the message, and where each goes

| Topic | Disposition | Ask Tradeify when |
|---|---|---|
| Offline research, fixed native parameters | Stated once in the architecture paragraph, not asked. Researching a rule outside NinjaTrader does not make the runtime external when every trading decision happens in NinjaScript ([NinjaTrader automated trading](https://ninjatrader.com/support/helpGuides/nt8/automated_trading.htm)). This does not settle research-data rights | Not planned |
| Company license and automated orders | Treated as a technical check. Native automated strategies are a documented NinjaTrader capability, and Tradeify documents use of its company license ([setup guide](https://help.tradeify.co/en/articles/12268716-ninjatrader-8-setup-guide)). Check the installed entitlement and the documentation for the features this strategy actually needs (plan P1). A menu being present proves neither trading permission nor correct execution | Only if the local and documentary checks leave a concrete gap. Then ask one narrow question about that feature |
| Ownership verification video | Already published ([guidelines](https://help.tradeify.co/en/articles/10468318-guidelines-for-traders)). Only the timing and evidence parts are asked, in §1 Q2–Q3 | — |
| Unattended home PC, remote desktop | Deferred. The first release is attended locally. The [FAQ](https://help.tradeify.co/en/articles/12268494-common-faqs) (2026-10-20) says "You cannot log in with VPN/VPS. After logging in normally, you may use VPS for trading at your own risk." It neither bans all remote operation nor approves remote desktop | Before any unattended or remote operation |
| "Same bot" at another firm | Deferred for a Tradeify-only pilot. Asked on 2026-10-08 and left undefined; the reply said the policy turns on ownership and exclusivity ([10-10 replies §3](2026-10-10-tradeify-exclusive-use-replies.md#3-answers-r1-paraphrased-per-point)). Different filenames, rewritten code or changed parameters cannot settle it. When asked, describe a genuinely distinct strategy honestly, and do not ask for detection tests or scan thresholds: the [compliance FAQ](https://help.tradeify.co/en/articles/17069653-risk-compliance-guidelines-faq) says those may stay confidential | Now, only if the answer decides which candidate D2 picks; otherwise before any cross-firm use |
| Same strategy on a personal brokerage account | Mostly answered: the [Funded Trader Agreement §6.6–6.7](https://tradeify.co/funded-trader-agreement) permits personal-account use and prohibits use across firms. That reading still sits under the other rules, including the bans on hedging across accounts. **Recorded conflict:** support's 2026-10-08 reply ("used only within Tradeify", [10-10 replies](2026-10-10-tradeify-exclusive-use-replies.md#3-answers-r1-paraphrased-per-point)) cuts the other way. The [routes note](2026-10-13-tradeify-compliant-automation-routes.md) treats this as an unresolved interpretation | Before any concurrent personal-account operation, citing both texts |
| Several own Tradeify accounts | Already permitted ([copy-trading guidance](https://help.tradeify.co/en/articles/13196343-tradovate-order-entry-copy-trading)). The remaining questions are engineering ones: copier versus separate instances, and safety | Not planned. Settle in the plan's P7 design |
| CME data rights | Routed to the existing licensing thread, not a new generic question: obtain the legal distributor and the exact subscriber agreement from Tradeify/Tradovate, then take the open classification through CME ticket #04738415 ([CME note](2026-10-10-cme-non-display-licensing-research.md)). Keep native automation, internal bars and caching separate from any optional research export | Through that thread |

## 3. Recording the answer

Record the reply as an addendum to the [route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md), where the 2026-10-12 guidance lives, and update the plan's §2.

A negative answer rules out enabling that candidate on Tradeify. It does not make bounded research or implementation work impermissible. Existing internal build approvals still apply either way.
