# Cross-firm exclusivity and per-trader account caps: Bulenox, MFFU, BluSky, Futureify (ex-FXIFY Futures), Tradeify — DRAFT

**Status:** DRAFT read-and-record. It decides nothing and edits no firm row, envelope cell, register row or locked surface ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal), [Rule 16](../operational_rules.md#rule-16--firm-rules-one-source-and-a-pre-flight)). Nothing here is accepted into an owner record ([Rule 17](../operational_rules.md#rule-17--venue-facts-quote-source-date-scope)).
**Date:** 2026-11-03 · **Author:** Claude Code (cloud) · **Repo base:** `main` at `315ea66`.
**Question (Rule 9):** do the other firms allow one strategy to run across firms, and how many accounts may one trader hold at each? **Decision it informs:** Joshua's reconsideration of the 2026-10-30 "Order of expansion" ([four-firm ADR, Addendum 2026-10-29](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md)). Context: the same ADR's [Addendum 2026-11-08](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#addendum-2026-11-08--4-falsifier-fires-consequence-narrowed-by-operator-ruling-accepted) demotes the multi-firm mandate to research-only; scaling within Tradeify continues.
**Budget (Rule 2):** one research pass (primary pages for five firms) and one self-review; then, on Joshua's request to dig deeper, one second pass (every remaining primary page and terms document, plus a read-only mailbox search) and one self-review; $0; K = 0; no firm contacted, no account touched. Stopped at the bound.

## How the pages were read

- **[W-raw]:** text copied from the page source fetched on 2026-11-03 (UTC 21:15–21:35), or, where the page loads its text by script, from the rendered page's DOM text in headless Chromium after expanding each section. No model summarised any quote. Not saved into the repo; HTML hashes would not reproduce (per-request nonces).
- **Dates:** Intercom `dateModified` for MFFU, BluSky and Tradeify articles; the page's own stamp otherwise. Bulenox help pages carry no date.
- **Tradeify** was read through its Intercom mirror `intercom.help/tradeify/en/articles/<id>`, as in the [register](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#how-to-read-this).
- **FXIFY Futures is now "Futureify".** `fxifyfutures.com/` redirects to `futureify.com/`; the footer reads "FXIFY Futures Limited, Suite 302, 2 Pembroke Street Upper, Dublin". The FAQ articles keep the "Updated on September 28, 2026" stamp under the new name. The GTC PDF at `futureify.com/terms-and-conditions/` is titled "FUTUREIFY GENERAL TERMS AND CONDITIONS", page footers "September 10, 2026", sha256 `2c7b3997…5e6229223`. It differs from the Dec 2024 PDF the [rule sheet](2026-10-17-fxify-futures-flex-150k-evaluation-rule-sheet.md) hashed (`c25d2fa8…`). The clauses quoted below match the rule sheet's §A5 wording. **This note does not re-verify the `FXIFY_Futures_Flex_150K` row**; the rename and the new GTC are flagged for its owner (§6).
- **Second pass (2026-11-03, UTC 21:45–21:55).**
  - Coverage: every article each Intercom sitemap lists, keyword-searched (BluSky 73 of 73, MFFU 77 of 77). Every Futureify FAQ article (48). MFFU's Terms and Conditions at `myfundedfutures.com/terms` (no page date; HTML sha256 `4803e659…`). BluSky's Terms of Use 11490284, §§1–10 read in full. Every Bulenox help section, plus `legal/Risk_Disclosure.pdf` and `legal/Privacy_Policy.pdf`.
  - Web search was used only to look for primary pages missed; its results were vendor and review sites and are not cited.
- **[mail]:** Tradeify support replies, read 2026-11-03 from Joshua's Gmail (read-only), quoted verbatim. This is venue guidance, not a clause, as in the [route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-30--tradeify-answers-on-native-ownership-exclusivity-and-source-review).
  - Searches: mail to or from Bulenox, MFFU, BluSky and FXIFY Futures/Futureify, and sent mail naming any of them.
  - Result: no correspondence with those four firms' futures support, so **none of the §4 questions has been sent from this mailbox**. FXIFY CFD account and marketing mail exists; it was not opened.

**Dedup (Rule 8).** Searches run before reading:

```
$ ls docs/notes | grep -i -E "exclusiv|cross-firm|account-cap"
2026-10-10-tradeify-exclusive-use-replies.md
$ grep -rn -i "other prop firm\|another prop firm\|cross-firm\|account cap\|accounts per\|maximum number of accounts\|five Master\|simultaneous" \
    docs/notes/2026-10-19-firm-eligibility-register-first-cut.md docs/notes/2026-10-19-flex-firm-questions-DRAFT.md docs/notes/2026-11-01-*.md ops/prop_envelope_default.md
docs/notes/2026-11-01-prop-firm-microstructure-study-DRAFT.md:44: ... a strategy run at Tradeify may not run at another prop firm [R route record 10-30] ...
docs/notes/2026-11-01-prop-firm-microstructure-study-DRAFT.md:176: ... a Tradeify strategy may not run at another prop firm ...
docs/notes/2026-11-01-prop-firm-venue-fact-register-DRAFT.md:106: | D11 | M | Bulenox | ... "Up to five Master-level accounts at once" | Not in repo |
docs/notes/2026-11-01-prop-firm-venue-fact-register-DRAFT.md:121: | 1 | Other firms impose no Tradeify-style native-only or cross-firm exclusivity rule | ...
```

Found and reused, not re-derived: Tradeify's cross-firm answer (route record [Addendum 2026-10-30](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-30--tradeify-answers-on-native-ownership-exclusivity-and-source-review)); FXIFY copy-in vs copy-out, already open as **U4a** ([source-status note](2026-10-19-fxify-flex-vs-fundednext-futures-source-status.md)) and the [eligibility register](2026-10-19-firm-eligibility-register-first-cut.md) question 1; Tradeify limits (register §I.2, re-read below). No prior note held Bulenox, MFFU or BluSky cross-firm or account-cap text.

---

## 1. Per-firm evidence (items 1–6)

All rows **[W-raw]**, accessed 2026-11-03. "SILENT" means no page read states a rule; it is not permission (Rule 17).

### 1.1 Bulenox

Sources: help centre `bulenox.com/help-center/{qualification,master,funded,fast-track,momentum,connection,general-information,payment}` and `bulenox.com/faq` (no page dates; rendered); Terms of Use `bulenox.com/legal/Terms_of_Use.pdf`, "Updated October 2026", sha256 `cb4810bb…6b3109d`; `Risk_Disclosure.pdf` and `Privacy_Policy.pdf` (second pass; no relevant clause).

| Item | Text (verbatim) | Source |
|---|---|---|
| 1 Cross-firm use | **SILENT.** No page read mentions other prop firms. Nearest: "Only user-built tools intended solely for the account owner's personal use are permitted. Commercial, shared, rented or publicly distributed automation tools are not allowed." | FAQ "Can I use bots, algos or trade copiers?" |
| 1 Approval | "any third-party algorithm, automated trading software, or other third-party trading technology must be reviewed and approved by the Bulenox management team before use. Approval may be subject to additional requirements or conditions established by Bulenox." Whether a user-built strategy counts as "third-party" is not stated | ToS, "ALGORITHMS AND AUTO TRADING" |
| 2 Copiers, multi-account | "Yes. Bots, algorithms and trade copiers are permitted." Trader-to-trader copying, mirroring between the trader's own accounts, and one strategy on several own accounts are not separately addressed. "Balances, profits and drawdown limits cannot be combined between accounts." | FAQ; Master "Multiple Master Accounts" |
| 3 Cross-firm hedging | **SILENT.** No hedging clause in the ToS, Risk Disclosure, Privacy Policy, FAQ or any help section | — |
| 4 Automation route | "If a trader chooses to connect to Rithmic through a Third-Party API or Trader Composite Software, a $100 monthly fee applies." ToS: the fee "does not constitute approval of any specific algorithm, strategy, or software". Prohibited: "“scalping” algorithms, DTC Protocol Bridge API or automated discretional trading … Open and close hundreds or thousand of rapid trades". Platforms: Rithmic (R\|Trader Pro; "Allow Plugins is set to On") and "NinjaTrader Connection (Free License)" using "your Tradovate username and password". NinjaScript is not named. As written, the $100 fee attaches to a Rithmic third-party connection; the Tradovate route is not named in the fee clause. Funded (live) automation: SILENT; the Funded Account Agreement is not public ("You must accept the Funded Account Agreement") | Qualification "Rules"; ToS; Connection; Funded |
| 4 Platform conflict | Connection: "Bulenox accounts run on the Tradovate platform." Qualification: "Every account is linked to the same Rithmic User ID". The "Other Supported Platforms" section is empty on the page (second pass, re-rendered) | Connection "Tradovate Connection"; Qualification "Multiple Accounts" |
| 5 Caps | "There is no limit to the number of Qualification Accounts you can own. You may hold up to five active Master-level accounts in total — Master, Fast Track and Momentum Master in any combination." "All five can be activated right away — there is no unlocking sequence." Funded: "Master-level Account with 3 successful Rewards — eligible for transition to a Funded Account"; "Additional active Master-level Account with at least 1 successful Reward — may also be eligible to transition to a separate Funded Account, subject to Risk Management approval." No numeric Funded cap. Household: ToS F, "you are the sole authorized Bulenox trader profile holder within your household" | Qualification "Multiple Accounts"; Master; Funded "Transition of Master-level Accounts"; ToS |

### 1.2 MyFundedFutures (MFFU)

Sources: `help.myfundedfutures.com/en/articles/<id>` (all 77 in the sitemap); Terms and Conditions `myfundedfutures.com/terms` (second pass; no page date). Terms §1.6: "In the event of any conflict between these Terms and any such incorporated documents, these Terms shall prevail". Sim-funded trading is also governed by a "Simulated Trader Agreement and its Appendices" (§29), which is not public.

| Item | Text (verbatim) | Source (dateModified) |
|---|---|---|
| 1 Cross-firm use | **SILENT.** No article read mentions running a strategy at another firm. Automation: "Traders may make use of automated trading strategies tailored to their own specific settings so long as these automated tools do not aim to exploit the favorable fills offered in the Simulated Environment." "all accounts participating in our challenges are exclusively traded by the account owner" | 8444599 (2026-10-30); 8230018 (2026-08-24) |
| 2 Copy, multi-account | "MyFunded Futures allows copy trading across all account types." "Tradovate users can utilize the built-in group copier feature"; "External copy trading solutions can also be used with your accounts." Trader-to-trader: "Traders are not permitted to copy trade one another". "Collaborating with others to execute identical or opposite strategies across unconnected accounts is prohibited." Terms §23.1.3: accounts "within the Account Limits" "must belong to the same verified individual"; prohibited to "use multiple accounts to hedge, mirror, copy, or coordinate trades in a manner that provides an unfair advantage or manipulates simulated results" (§23.1.3.3). Copying from an account at another firm: not addressed | 10771500 (2026-08-24); 8444599; Terms |
| 3 Cross-firm hedging | "MyFundedFutures prohibits hedging of any kind. Hedging is defined as a trader entering both buy and sell positions on the same underlying asset, at the same time." "hedging through different unrelated assets is permitted." Terms §23.1.3.3 (above) likewise names no account scope. Neither text limits itself to MFFU accounts, so under Rule 17 (silence on scope reads broad) both are **recorded as reaching accounts outside MFFU**, pending MFFU's answer to question M2 | 12011241 (2025-11-10); 8444599; Terms |
| 4 Automation route | Platforms: NinjaTrader, Hyperprop, Tradovate, TradingView, Quantower, Volumetrica, DeepChart/DeepDom, ATAS. "High-frequency Trading is not allowed on our plans." Live: "Traders trading live accounts with automated trading must abide by CME guidelines." API, bridge, fee: SILENT. NinjaScript is not named | 8528335 (2026-10-08); 8444599 |
| 5 Caps | "Traders may hold a maximum of 10 active Evaluation Accounts at any given time." "Traders may maintain up to 5 active Sim-Funded Accounts when holding only $25K and/or $50K account sizes." Plan limits: Rapid EOD 25K/50K "Maximum of 3"; Builder 25K "Maximum of 2"; Builder 50K "Maximum of 1". "If a trader holds any $100K or $150K Sim-Funded Account, the maximum number of active Sim-Funded Accounts is 3." Live: "your Sim Funded Accounts will be merged into one Live Funded Account"; "Multiple live accounts can be discussed with your risk manager, but are reserved solely for high-performing traders"; "You cannot trade both Sim and Live data at the same time." | 16498635 (2026-09-04); 10101257 (2026-08-24); 12109396 (2025-11-10) |

### 1.3 BluSky

Sources: `help.blusky.pro/en/articles/<id>` (all 73 in the sitemap); `blusky.pro/faq/` (rendered and raw; no automation entry); Terms of Use 11490284 (2026-02-01; "Effective Date: May 31, 2025"), §§1–10 read in full: no automation, copy or cross-firm clause.

| Item | Text (verbatim) | Source (dateModified) |
|---|---|---|
| 1 Cross-firm use | **SILENT** on running one strategy at another firm. The envelope's [R] "Semi-automated and full automated" welcome (`ops/prop_envelope_default.md` §4) was **not re-found** in any of the 73 articles, the FAQ or the Terms of Use. Conduct policy: "using automated software (AI, ultra-high speed, bulk data entry) to unfairly influence outcomes" is forbidden | 12069208 (2026-02-23) |
| 2 Copy, multi-account | Account table: every plan row reads "Yes" in the "Trade Copier Allowed" column. "Traders in the same household, must be in control of their own accounts, and must be trading on different machines." **Conflict:** the conduct policy forbids "Account Mirroring: Copying trades from another trader, account, or signal provider" | 12433943 (2026-10-22) vs 12069208 (2026-02-23) |
| 3 Cross-firm hedging | **PROHIBITED, cross-firm by text.** "you cannot use multiple trading accounts to offset risk by placing opposite or correlated trades across them." "You should avoid opening opposing positions across separate accounts, even if: … The accounts are with different prop firms. You trade different but correlated futures contracts, such as ES and NQ. Your intention is to reduce risk rather than manipulate the evaluation." Same-account mini-vs-micro opposite: "✅ According to the policy, yes". Also: "you cannot go long in one account and short in another account under you user ID and control" | 17679634 (2026-10-20); 12433943 |
| 4 Automation route | Rithmic platforms incl. "NinjaTrader (Evaluation, BluLive and Sim Funded only)", Tradesea, Quantower, Sierra Chart and others; Tradovate: "NinjaTrader Prop", "Tradovate Prop"; Volumetrica. Explicit automation permission, API, bridge, fees: SILENT across every primary page read. NinjaScript is not named | 12433926 (2026-04-04) |
| 5 Caps | "You can have any number of Evaluation Accounts of any combination. Funded accounts can only be 3 at any time (Sim Funded, Instant Sim Funded or Direct to Funded Accounts." Table: Live Brokerage Accounts "2"; "If you are in Live Brokerage, you cannot trade in Sim Funded at the same time." | 12433943 |

### 1.4 Futureify (FXIFY Futures Limited; ex-`fxifyfutures.com`)

Sources: `futureify.com/faqs/<category>/<slug>/`, all 48 articles (second pass), stamped "Updated on September 28, 2026" except the Flex payout policy ("October 28, 2026"); GTC PDF (above).

| Item | Text (verbatim) | Source |
|---|---|---|
| 1 Cross-firm use | **Copy-in ALLOWED (quoted):** "Copying trades from another prop firm account to your Futureify account, provided both accounts are owned by the exact same user." Flex overview: "Expert Advisors (EAs) and copy trading permitted by default." Running the same strategy independently at another firm, and copy-out: **not addressed** in any of the 48 articles or the GTC (unchanged from U4a) | `does-futureify-allow-copy-trading`; `flex-plan-overview` |
| 2 Copy, multi-account | "Copying trades between your own active accounts within Futureify." "Copying trades from your personal trading account to your Futureify account, provided both accounts belong to the exact same user." Prohibited: "Copying trades from third-party traders, signal providers, or automated signal services (paid or free)"; "Copying trades between accounts owned by different individuals." "Group Trading: Collaborating with other traders to execute identical or opposite strategies across different accounts is not allowed." | same; `what-trading-strategies-are-prohibited` |
| 3 Cross-firm hedging | "Reverse Trading: Simultaneously taking opposite positions (long and short) on separate accounts to exploit market moves is not allowed at the Evaluation or Funded Phases." GTC 5.4.1.4: no trades "ALONE OR IN CONCERT WITH ANY OTHER PERSONS, INCLUDING BETWEEN CONNECTED ACCOUNTS, OR ACCOUNTS HELD WITH DIFFERENT FXIFY ENTITIES … FOR EXAMPLE BY SIMULTANEOUSLY ENTERING INTO OPPOSITE POSITIONS". "separate accounts" carries no firm qualifier, so under Rule 17 it is **recorded as reaching accounts at other firms**, pending Futureify's answer to question F2 | `what-trading-strategies-are-prohibited`; GTC |
| 4 Automation route | "the use of Expert Advisors (EAs) and automated trading scripts is permitted on both Flex and Direct accounts." "enabled by default across all account types. No prior permission or special setup request is required." "You can run automated strategies across supported platforms, including NinjaTrader, Tradovate, and TradingView." EA "news trading" etc. → "immediate account breach and deactivation". GTC 5.4.1.2 bars "AN EXTERNAL OR SLOW DATA FEED". API, bridge, fees: SILENT | `can-i-use-eas-expert-advisors-to-trade`; GTC |
| 5 Caps | "traders can hold a maximum of 5 active accounts in total across all Evaluation and Funded stages combined. This total allocation applies across both Flex and Direct plan types". "Once you reach the 5-account cap, you will not be able to purchase or activate additional accounts until an existing account is closed, failed, or fully processed." | `what-is-the-maximum-number-of-accounts-allowed` |
| Rename check (F3) | The Flex 150K figures under the new name match the [rule sheet](2026-10-17-fxify-futures-flex-150k-evaluation-rule-sheet.md) §A1: "$150,000 Account: $449 one-time fee"; "$9,000 profit target"; "$4,500 (3.0%)"; "$3,000 (2%)"; "Max 10 mini / 100 micro contracts"; reset "$209 for $150k". Read only; the row is not re-verified here | `flex-plan-overview`; `account-parameters-overview` |

### 1.5 Tradeify (item 6, and items 1–3 for comparison)

| Item | Text (verbatim) | Source (dateModified) |
|---|---|---|
| 1 Cross-firm use | **PROHIBITED.** "Exclusive Use: While you may use the bot on your personal accounts, using it across multiple firms is against Tradeify's policy. The bot should be solely for your own use within Tradeify." "We scan to ensure there are no similar orders on other accounts." Support, 2026-10-24: "you cannot run a strategy you own at another prop firm while also trading it at Tradeify" | 10468318 (2026-10-17); route record 10-30 |
| 1 What counts as "the same" [mail] | 2026-10-08 (help desk): "Using the same bot across multiple firms is against policy, even if risk limits, sizing, or weights differ." 2026-10-12, 15:29Z (support): "'Same bot' is defined by sole ownership and exclusive use … The focus is on exclusive use and ownership, not just code similarity or logic." and "If you write distinct strategies (different logic) running on one privately owned engine, you may use some exclusively on Tradeify and others elsewhere, as long as the strategies used on Tradeify are not used at other firms and you maintain sole ownership and exclusive use within Tradeify." The 10-12 reply is **new to the repo**; the 10-08 line is already in the [10-10 note](2026-10-10-tradeify-exclusive-use-replies.md) | Gmail thread "Clarification of algorithmic trading exclusive-use policy" |
| 2 Own accounts | Support, 2026-10-24: "Running one strategy across several of your own Tradeify accounts is allowed, as long as you are the sole owner and operator, and the strategy is not used at other prop firms." | route record 10-30 |
| 3 Hedging | "whether those positions sit in a single account or are spread across several of your accounts"; ESA §6.7(c),(i) extends to External Accounts | 10468318; register T3 |
| 6 Caps | "An individual user may have up to 5 Simulated Funded Accounts at any time"; "A household is also restricted to 5 Simulated Funded Accounts at any time (exception: V2 Select 300K funded accounts sit on top of the 5, for up to 8 in total)". "You can have up to 15 select evaluations per 30 days and as many Growth Evaluation accounts as you want". "You can pass as many evaluations as you want and bank those completions for later." "Each Select evaluation can be reset up to 10 times within a 30-day period" | 10468251 (2026-10-20) |

---

## 2. Reading: does the evidence support "other firms allow one strategy across firms"?

**Not yet, and the second pass did not change that.** No primary page or terms document read prohibits it outside Tradeify. Only Futureify says anything permissive, and that covers copying in. Bulenox, MFFU and BluSky are silent across every public page and terms document now read, and silence is not permission (Rule 17). The remaining answers can only come from the firms (§4) or from the non-public funded-stage agreements.

| Firm | Cross-firm use of one strategy | Cross-firm opposing positions | Note |
|---|---|---|---|
| Bulenox | **SILENT** | **SILENT** | ToS requires approval of a "third-party algorithm" before use; scope unclear |
| MFFU | **SILENT** | **PROHIBITED, read broad** ("hedging of any kind"; Terms §23.1.3.3; scope unstated, Rule 17) | Copiers incl. "External copy trading solutions" allowed; Terms bar copying "in a manner that provides an unfair advantage" |
| BluSky | **SILENT** | **PROHIBITED** across prop firms, correlated products included | Copier "Yes" vs conduct-policy mirroring ban |
| Futureify | **ALLOWED for copy-in** (quoted); independent run and copy-out SILENT | **PROHIBITED, read broad** ("separate accounts"; scope unstated, Rule 17) | Rename; new GTC |
| Tradeify | **PROHIBITED** (quoted) | **PROHIBITED** incl. External Accounts | Baseline |

**A rule that binds either ordering (inference):** Tradeify's ESA §6.7 and BluSky's hedging page both expressly reach accounts at other firms. MFFU's and Futureify's bans name no account scope, so they are read broad too (Rule 17) until questions M2 and F2 are answered. Distinct books at any two of these four firms must therefore never hold opposing positions in the same underlying at the same time. The scope differs by firm: the whole Product Group at Tradeify, correlated products at BluSky, and the same underlying at MFFU. This constraint applies whichever firm gets the best-evidenced book. Bulenox has no hedging clause on the pages read, so it stays SILENT (question B4).

**What a distinct Tradeify book must be ([mail], inference from the quotes in §1.5).** Tradeify says different sizing, risk limits or weights do not make a strategy distinct, while "distinct strategies (different logic)" may share one engine. So book B for Tradeify needs different trading logic from book A, not a re-sized or re-weighted copy. This bears on the operator ruling recorded as D4b in the [origin log](2026-10-15-deployment-decision-origin-log.md) (2026-09-28, as relayed in an agent report; the log notes Joshua's own words are absent: "Portfolios adapted to each firm's rules are treated as distinct strategies"). The 10-08 reply contradicts that reading where "adapted" means only sizing or weights. Joshua decides whether D4b stands (Rule 3).

## 3. Scaling comparison (inference, caps only; no P&L)

A "slot" is one simultaneously held funded-stage (sim-funded or Master-level) account. Evaluations are excluded, except at Futureify, where they share the cap. Caps are per trader; Tradeify also caps per household, and Bulenox allows one profile per household.

| Firm | Funded-stage slots per trader |
|---|---|
| Tradeify | 5 (up to 8 with V2 Select 300K) |
| Bulenox | 5 Master-level |
| MFFU | 5 if only 25K/50K (plan limits: Rapid EOD 3, Builder 2 or 1); 3 if any 100K/150K |
| BluSky | 3 |
| Futureify | 5 minus active evaluations |
| **Four non-Tradeify firms** | **16** (MFFU at 3, Futureify at 5 funded) to **18** (MFFU at 5) |

- **Tradeify-first** (ruling of 2026-10-30): book A gets **5** slots (8 with V2 300K). The other firms need a distinct book B, which gets 16–18 slots, if B exists.
- **Other-firms-first:** book A gets **16–18** slots, provided cross-firm use is allowed at each of the four firms. That is the SILENT readings above, and Bulenox's approval clause. Tradeify gets book B, with 5 slots, and B must differ from A in logic, not only in sizing or weights (§2).
- **With both books,** the total is the same, 21–23 slots. The ordering only decides which book gets the larger share: A gets 5 or 16–18. **With one book only,** the choice is 5 slots against 16–18.
- **Not counted here:** live-stage limits, which are small and discretionary everywhere (MFFU merges to one live account; BluSky 2 live, not concurrent with sim; Bulenox and Tradeify by review). Also not counted: eval throughput, fees, and whether one book even fits each firm's rules (flat-by times, products, drawdown type). These caps are an upper bound on parallel accounts, not a forecast.

## 4. Support questions for Joshua to send

Agents never contact firms. Each question names no strategy, size, parameter or account. Status after the second pass: **open** (no public text answers it), **narrowed** (public text answers part; the question now asks only the rest) or **partly answered**. None has been sent from Joshua's mailbox (see How the pages were read).

**Bulenox**
1. *Open.* May I run my own user-built automated strategy on my Bulenox accounts while running the same strategy, independently and not copied, on accounts at another prop firm? Is there any exclusivity requirement?
2. *Open.* Your Terms of Use say "any third-party algorithm, automated trading software, or other third-party trading technology must be reviewed and approved by the Bulenox management team before use." Does that apply to a strategy I wrote myself, running inside NinjaTrader on my own PC? If it does, how do I submit it, and what do you review?
3. *Narrowed.* Your fee text attaches the $100 monthly charge to connecting "to Rithmic through a Third-Party API or Trader Composite Software". Please confirm that a NinjaTrader strategy on the NinjaTrader (Tradovate credentials) route does not incur it.
4. *Open.* Do you prohibit opposing positions between my Bulenox accounts, or between a Bulenox account and an account I hold at another firm or a broker?
5. *Open.* Is automated trading permitted on a Bulenox Funded (live) account, and on the same terms as on Master accounts? May I read the Funded Account Agreement before qualifying?
6. *New.* Your Connection page says "Bulenox accounts run on the Tradovate platform", but the Qualification page links every account to one Rithmic User ID. Which platforms does a new account get, and can one account use both?

**MFFU**
1. *Open.* May I run my own automated strategy on MFFU accounts while the same strategy runs independently at another prop firm? Is there any exclusivity requirement?
2. *Open.* Do "hedging of any kind" and Terms §23.1.3.3 include opposing positions between an MFFU account and an account I hold at another prop firm or a personal brokerage account?
3. *Narrowed.* Your copy-trading article allows "External copy trading solutions", and Terms §23.1.3.3 bars copying across accounts "in a manner that provides an unfair advantage or manipulates simulated results". Is copying into MFFU from an account I own at another prop firm allowed, and what would make it an "unfair advantage"?
4. *Open.* On which platforms may a fully automated strategy run in evaluation, sim-funded and live (for example a NinjaTrader strategy)? Are third-party APIs or bridges restricted, and are there fees? May I read the Simulated Trader Agreement before passing?

**BluSky**
1. *Open.* May I run my own automated strategy on BluSky accounts while the same strategy runs independently at another prop firm? Is there any exclusivity requirement?
2. *Open.* Your Multiple Accounts page shows "Yes" under "Trade Copier Allowed", but the Ethical Trading & Conduct Policy forbids "Account Mirroring: Copying trades from another trader, account, or signal provider". Which governs? May I copy between my own BluSky accounts, or from an account I own at another firm?
3. *Open, and now the first BluSky question.* No current BluSky page or term states that automated trading is permitted at all. Is fully automated strategy execution permitted in evaluation, Sim Funded and Live Brokerage? On which platforms, and does it need any review?
4. *Open.* Your hedging page bans opposing or "correlated" positions across accounts "with different prop firms". Which products count as correlated beyond the ES/NQ example (for example MNQ against MYM)? Does the ban apply when the two strategies are independent?

**Futureify**
1. *Open.* Independent run and copy-out. This is the existing **U4a** question, restated: may the same strategy run independently, not copied, at another prop firm while it trades at Futureify?
2. *Open.* Does "Reverse Trading … on separate accounts" include accounts at other prop firms or brokers?
3. *Partly answered.* The rename is visible on the site, and the Flex 150K figures are unchanged (§1.4). Ask only this: does the GTC dated September 10, 2026 now govern FXIFY Futures accounts bought before the rename?

## 5. What this implies for the register's §E row 1 (proposed, not edited)

[Register §E row 1](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#e-unverified-assumptions-ranked): "Other firms impose no Tradeify-style native-only or cross-firm exclusivity rule", C 3, L 2, K 1, score 6.

Proposed replacement for the "Moved since the study?" cell, and the cost-to-check:

> **Partly answered (web, 2026-11-03, [this note](2026-11-03-cross-firm-exclusivity-and-account-caps-DRAFT.md)).** No Bulenox, MFFU, BluSky or Futureify page read states a cross-firm exclusivity or native-only rule. Futureify expressly allows copying in from the same owner's account at another prop firm. Bulenox, MFFU and BluSky are silent, and silence is not permission. New: Bulenox's ToS requires management approval of a "third-party algorithm" before use; BluSky's hedging ban reaches accounts "with different prop firms"; MFFU's Terms bar copying or hedging across accounts with no account-scope limit; and no current BluSky page states that automation is permitted. A second pass over every public help article and terms document of the four firms found nothing further. The first check is now the support questions in §4 of this note, so K becomes 2 (firm-side question), and the score becomes 3 × 2 ÷ 2 = 3.

The register's owner decides. No quote here supports changing L.

## 6. Flags for other owners (not acted on)

- **FXIFY row** (`core/firm_rules.py` `FXIFY_Futures_Flex_150K`; rule sheet): the site and product name changed to Futureify, and a new GTC (September 10, 2026, sha256 `2c7b3997…`) replaces the hashed Dec 2024 PDF. The Flex 150K figures read unchanged (§1.4). Re-verify under Rule 16 on Joshua's direction.
- **Origin log D4b and the Tradeify book:** Tradeify's 10-08 and 10-12 replies (§1.5) bear on whether a re-sized or re-weighted portfolio counts as a distinct strategy (§2). The 10-12 reply is not yet in any owner record; the [10-10 note](2026-10-10-tradeify-exclusive-use-replies.md) holds the 10-08 one.
- **Envelope §4 BluSky row:** the "Semi-automated and full automated" welcome was not re-found in any of BluSky's 73 articles, its FAQ or its Terms of Use; BluSky now has a dedicated cross-firm hedging page (17679634, 2026-10-20), and its copier table conflicts with the conduct policy.
- **Envelope §4a (hedging as candidate E8):** primary text now exists for MFFU, BluSky and Futureify hedging (§1). The ADR that graduation requires still needs Bulenox's answer (question 4).
- **Register D11:** the Bulenox cap is now read verbatim on three pages (§1.1).

## Self-review

- Every quote is copied from page text fetched this session; no model summarised any. Dates are as the page shows them; Bulenox pages carry none.
- Rule 13 and Rule 20: no account data, Pine, port, `effective_inputs.json` or research figure appears. The only dollar figure is Bulenox's published "$100 monthly fee", quoted.
- Second pass: MFFU's terms and BluSky's Terms of Use 11490284 were read; BluSky's longer terms (12907044, `blusky.pro/terms-and-conditions/`) were keyword-searched only. [mail] quotes were checked against the message text. The mailbox search covered sender, recipient and body terms for the four firms; it cannot show questions sent from another address or through a firm's chat widget.
- Not public, so not read: the Bulenox Master and Funded Account Agreements, MFFU's Simulated Trader Agreement, and every firm's funded-stage agreement.
