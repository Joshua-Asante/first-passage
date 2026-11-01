# Tradeify venue deep-dive and suggestions — DRAFT

**Status:** DRAFT, third pass of the [microstructure study](2026-11-01-prop-firm-microstructure-study-DRAFT.md); companion to the [venue-fact register](2026-11-01-prop-firm-venue-fact-register-DRAFT.md). It decides nothing, edits no firm row and authorizes nothing. Every suggestion in §6 is a proposal for Joshua or for the named owner ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal)).
**Date:** 2026-11-01 · **Author:** Claude Code (cloud) · **Repo base:** `main` at `2bc54b2`.
**Budget (Rule 2):** one dig pass over Tradeify's public pages plus one self-review; $0; K = 0. Stopped at the bound.

## Sources and labels

All quotes are **[W-raw]**: copied from the raw HTML of public pages fetched 2026-11-01. They are verbatim, but **not accepted into any owner record** (Rule 17).

- **Help centre:** read through Tradeify's Intercom mirror `intercom.help/tradeify/en/articles/<id>`, because `help.tradeify.co` returns 403 to scripted fetches. I listed 71 articles from the six rule collections and read 41. Each article's `dateModified` is given as "(mod. YYYY-MM-DD)".
- **Agreement:** `tradeify.co/funded-trader-agreement`. The page is titled **"Evaluation Services Agreement"**, says "Last modified: October 2026", and is cited below as **ESA §n**.
- **Home page:** `tradeify.co`.

No account data, Pine, port or research backtest figure appears in this note. Dollar figures are Tradeify's published rule, fee and payout figures.

---

## 1. What changed in the picture

1. **The evaluation agreement may forbid what the weekly preservation trade is.** ESA §6.5: "refraining from flipping contracts just to register a 'trading day'". ESA §6.9 requires "at least one trade per calendar week". The repo's standing practice is a minimal round trip each Mon–Fri week to keep the account alive ([STATE weekly trigger](../../STATE.md#scheduled-forward-triggers)). The two clauses pull against each other. No repo surface I searched cites §6.5 (search: "flipping contracts", "register a .trading day", "6.5 Consistency" across `docs ops core .claude`).
2. **Account-operation rules bear on agent-placed trades and remote hosts.**
   - Risk & Compliance FAQ 17069653 (mod. 2026-10-01; "Guidelines last updated: September 15, 2026"): "Each trader must personally own, control, verify, and operate their account." Review may follow access "through prohibited virtualization, remote-access, anonymization, or circumvention technologies."
   - ESA §6.7(b) prohibits "the management of a Trader's account by or on behalf of any third party."
   - KYT 17229690 (mod. 2026-10-17) is an "AI-conducted interview" that checks that "Trading activity reflects the account holder's own decisions". The trader must "Not use another person, software, AI tools, or any other aid to generate or dictate your answers."

   The repo authorizes agent-placed orders through computer use ([surface-allocation ADR, Addendum 2026-09-30b](../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b)) and a standing GO for the weekly trade. I found no record that weighs those against these Tradeify texts. **Whether an agent the account holder directs counts as "another person" or a "third party" is not settled by any text I read.** That is a question for Joshua and, if he chooses, Tradeify. It is not a finding of breach.
3. **Funded stage ≠ eval stage, and the repo models only the eval.**
   - Funded Select accounts start at reduced size and scale on EOD equity (12853966, mod. 2026-10-17). 100K starts at "3 minis / 30 micros" and reaches 8/80 at "$3,000 Equity".
   - Select Daily's 100K drawdown is **$2,500**, not $3,000.
   - A payout request before the natural lock **raises the floor at once**: "The lock can also trigger immediately when you request a payout" (10495897, mod. 2026-10-15).
4. **Live means a fresh, smaller game.**
   - Elite Live accounts start at "$0 starting balance" with fixed EOD drawdown, an 80/20 split, and the loss of all sim accounts (12969284; ESA §5.4).
   - "Traders who are transitioned to Tradeify Elite Live … may NOT hold ANY other funded accounts, challenge accounts" (ESA §4.2 note), and that extends to the household.
   - Firm-reported: 3.0% of funded participants were called up (home page disclosure, Aug 2025–Jul 2026).
5. **Hedging reach is wider than one firm.** ESA §6.7(c) and (i) prohibit opposing positions between a Tradeify account and an "External Account", including "any proprietary trading firm, broker, or funding program". Breach needs no intent, and Tradeify "may rely on information provided to it by NinjaTrader, acting in this context as an authorized third-party trade-monitoring service". The repo records this for the personal lane ([personal clearance plan :222-234](2026-10-11-personal-clearance-plan-tradeify-book.md)) and as an open question in the [eligibility register](2026-10-19-firm-eligibility-register-first-cut.md) (P3, P5). It binds the multi-firm program's **other-firm strategies** too: a short MNQ at another firm while a Tradeify account is long MYM is a Tradeify breach.

---

## 2. Rule inventory (evaluation, Select and Growth)

| Rule | Text (verbatim, abridged) | Source | Repo |
|---|---|---|---|
| Drawdown clock | "The limit updates at end of day but is enforced in real time against your net liquidation value." "Applies to: All Tradeify accounts (Growth, Select, and Lightning)" | 10495897 (2026-10-15) | Matches (`core/mc/simulation.py:351-357`) |
| Eval lock | "Evaluation accounts do not have drawdown locking." | 10495897 | Matches (`core/firm_rules.py:284-286, :321`) |
| Select eval table | 100K: "Profit Target: $6,000 · Maximum Drawdown: $3,000 (End of Day) · Daily Loss Limit: None · Consistency Requirement: 40% (50% add-on available) · Maximum Contracts: 8 mini / 80 micro" | 12853921 (2026-10-19) | Matches (`:500`) |
| 25K eval cap | "1 mini / 10 micro" (12853921, 10495915) **vs** "During evaluation, you have access to the full contract limits (2/20, 4/40, 8/80, or 12/120 …)" (12853966) | conflict | Repo 10 (corrected 2026-07-22, `:223-226`) |
| 50K target | "Accounts purchased before the new dashboard launch retain their original $2,500 profit target" | 12853921 | Not encoded (100K unaffected) |
| Consistency | Select eval 40%, "no consistency rule for Select accounts in funded mode"; Growth funded 35%; Lightning 20/25/30% | 10468320 (2026-10-17) | Select matches (`:336`) |
| Time limit | "There is no time limit to complete a Growth or Select Evaluation" | 12268494 (2026-10-20) | — |
| Expiry | "your account remains active until you either pass, fail, or the account expires"; "Expired accounts cannot be reinstated" | 12268494 | **Undefined** — no page read states when an account expires |
| Activity | "at least one trade per week (Monday through Friday)" (help) vs "at least one trade per calendar week" (ESA §6.9); inactive accounts "deleted after an email warning" | 10468318, ESA, 12268494 | Matches the help version (`:181-200`) |
| Trading day | "at least one trade placed from 6:00 P.M. ET to 5:00 P.M. ET the next day" | 10468225 (2026-10-17) | — |
| Flat-by | "4:45 PM ET"; holiday "12:59 PM ET"; auto-close "will NOT result in account failure" | 10495876 (2026-10-17) | Matches (`:253-255`) |
| News | "news trading is allowed on all accounts" | 12268167 | Matches |
| Hedging | Product-group opposing positions banned "in a single account or … across several of your accounts"; ESA extends to External Accounts | 10495868 (2026-08-19); ESA §6.7 | Partly (§1 item 5) |
| Bots | Sole owner, exclusive within Tradeify, no HFT, "live video of you enabling the code on your own PC"; "We scan to ensure there are no similar orders on other accounts" | 10468318; ESA §6.6 | Matches the route record 10-30 |
| Platform route | NinjaTrader and TradingView "connect via Tradovate"; Rithmic accounts get Tradesea, Quantower, Sierra Chart, R\|Trader; "you cannot switch between brokers … without purchasing a new account" | 10468221 (2026-10-17) | Rithmic-platform automation not asked about |
| API | "The Tradovate API is only available for LIVE funded accounts" | 10468222 (2026-10-18) | Matches |
| Data feed | "Trading based on an external or delayed data feed is not allowed." | ESA §6.3 | Supports the native-only ruling |
| Sizing style | "avoiding maximum or larger contract sizes on single trades … maintaining consistent trading sizes, avoiding dollar-cost averaging" (ESA §6.5) **vs** "We do not have any rules against or guidelines around … Dollar Cost Averaging (DCA), flipping, or scaling" (10468318) | conflict | Bears on pyramided and volatility-sized expressions |
| Expired contracts | Trading an Expired Contract is "a breach … regardless of the Trader's intent"; no trading for a "Non-Market Price" from "stale, frozen, delayed … simulated" data | ESA §6.11 | Roll logic in any native strategy is a compliance item |
| Simulated conditions | Prohibited: "exploitation of simulated conditions" | 17069653 | Same theme as MFFU's "favorable fills" (register D9) |
| VPS/VPN | "You cannot log in with VPN/VPS. After logging in normally, you may use VPS for trading at your own risk." | 12268494 | Recorded ([follow-up draft :37](2026-10-21-tradeify-native-followup-questions-DRAFT.md)) |
| Limits | 15 Select evals per 30 days; 10 resets per eval per 30 days; 5 funded per individual **and household** (V2 300K up to 8) | 10468251 (2026-10-20) | Not encoded |
| Prices | Select 100K **$265**, reset **$169**; with 50% add-on $329 / $209; Growth 100K $255 / $169 | 14369021 (2026-10-19) | Ledger row d15 still open |

---

## 3. Funded and live stages (not modelled anywhere in the repo)

### 3.1 Select Flex vs Select Daily at 100K (12853966, 10495897)

| | Select Flex | Select Daily |
|---|---|---|
| EOD drawdown | $3,000 | **$2,500** |
| Lock trigger (EOD balance) → floor | $103,100 → $100,100 | $102,600 → $100,100 |
| Daily loss limit | none | $1,250 (soft) |
| Starting contracts → max | 3/30 → 8/80 (scaling at +$1,500 / +$2,000 / +$3,000 EOD equity) | same scaling |
| Payout eligibility | "Every 5 winning days", winning day ≥ "$200" at 100K | daily, above a "$2,600" buffer |
| Payout size | "Up to 50% of your total profits", cap **$3,500** (bought after 2026-09-01) | "up to 2× the profit earned between each payout request", cap **$1,750**; minimum $250 |
| Split | "90 Trader / 10 Tradeify" | 90 / 10 |
| Later payouts | "You must have positive net profit during each payout cycle" | same |

### 3.2 Elite Live (12969284; ESA §5)

- **Eligibility:** "3 payouts on a single account, or 10 total payouts since the last live transition". This is "not automatic qualification".
- **On transition:** "All Sim Funded and evaluation accounts are closed"; only accounts with ≥1 payout move.
- **100K Elite:** start balance $0, EOD drawdown $3,000, "4 mini / 40 micro" until above the drawdown, then 8/80, no DLL, lock at $3,100. "Elite Live: Trade with real capital in live markets, with daily payouts at an 80/20 profit split" (12268494).
- **Broker:** "all Tradeify Elite Live accounts are issued through and facilitated by NinjaTrader and GFF Brokers" (ESA §5).
- **Payout before lock:** the floor moves up first, then the payout is deducted, "leaving the trader with only $1,500 of effective drawdown room instead of $2,000" (50K example).

### 3.3 Arithmetic consequences (venue figures; labelled inference)

- **[INF] An early payout tightens the funded floor.** At Flex 100K, five winning days of $200 put EOD balance at $101,000 at minimum, with the floor at $98,000. Requesting a payout then locks the floor at $100,100, so the cushion falls from $3,000 to about $900 before the payout itself (≤ $500) is deducted. Waiting for the natural lock at $103,100 keeps a $3,000 cushion at the moment of lock.
- **[INF] Funded size starts at 3/8 of the eval cap at 100K** (30 vs 80 micros). A book sized near the eval cap must re-size at activation. Funded bust and payout timing are therefore a different simulation from the eval, at a different size.
- **[INF] Cost per pass at the firm's pooled rate.** At Select 100K pricing ($265 + $169 per reset) and the firm-reported 17.2% eval completion rate (pooled across products, so only indicative), expected spend per pass is about $265 + 4.8 × $169 ≈ $1,080. A strategy's own honest-clock pass rate replaces 17.2% in any real estimate.
- **[INF] Micros vs minis at size.** "Trading 10 MES contracts costs $18.20 per round trip, while 1 ES contract costs only $5.76" (10468315). At ≥10 micros of exposure the mini is cheaper per unit of risk, and mini+micro holding is allowed (12268167).

---

## 4. Who trades at Tradeify (sourced)

- "This is how a futures prop firm works: you trade the firm's simulated capital and receive real payouts when you meet the payout rules." (12268494)
- "Tradeify is looking for traders that … can be called up to live to eventually be copied by our own firm as well." (10468318)
- Trader Performance Statistics, Aug 2025–Jul 2026 (home page): 17.2% of evaluations completed; 40.3% of participants reached funded (median 3 evaluations each); 28.5% of funded participants received a payout; 3.0% of funded participants were called up to live.
- "Tradeify Brokerage LLC d/b/a Slay Markets is a CFTC-registered introducing broker guaranteed by NinjaTrader Clearing, LLC" (home page). The 10-30 reply says "NinjaTrader owns the clearing firm" (route record).
- "Simulated Funded Account … your trades mirror what would happen in the live markets, but your profits and losses are not real." (10468257, mod. 2026-10-20). Tradeify claims sim realism; MFFU says its sim gives "favorable fills" (register D9). Neither firm publishes its fill model.

[INF] Harris reading: evaluation and sim-funded fills meet the simulator, not CME traders; the firm earns fees and pays sim payouts; a ~3% minority reaches real capital, where Tradeify intends to copy the flow. The rulebook (trailing floor, consistency, 10-second rule, hedging and cross-platform bans, ownership, KYT, "exploitation of simulated conditions") is the firm's defence against traders who would otherwise extract payouts from the simulator rather than from the market.

---

## 5. New conflicts and gaps (add to the register)

| # | Sev | Item | Evidence |
|---|---|---|---|
| T1 | **H** | ESA §6.5 "flipping contracts just to register a 'trading day'" vs the weekly preservation round trip and ESA §6.9 | §1 item 1 |
| T2 | **H** | Agent-operated orders and remote or VM hosts vs "personally … operate their account", "third party" management, KYT, and "prohibited virtualization, remote-access" | §1 item 2 |
| T3 | **H** | Cross-platform opposing positions bind every other-firm strategy, not just the personal lane | ESA §6.7(c), (i) |
| T4 | M | 25K eval cap: 1/10 (12853921, 10495915) vs 2/20 (12853966) | §2 |
| T5 | M | ESA §6.5 "avoiding dollar-cost averaging … consistent trading sizes" vs 10468318 "no rules against … DCA, flipping, or scaling" | §2 |
| T6 | M | Activity: "Monday through Friday" (help) vs "calendar week" (ESA §6.9) | §2 |
| T7 | M | "Account expires" appears in FAQs without a stated condition | 12268494, 10468256 |
| T8 | M | Funded rows (Flex, Daily), scaling, payout mechanics and live terms are absent from `core/firm_rules.py` and every lab harness I know of | §3 |
| T9 | L | ESA §4.1 still lists "Advanced Challenge"; the stats pool "Growth, Advanced and Select" | ESA; home page |
| T10 | L | Rithmic-platform (Sierra Chart, Quantower, Tradesea) native automation was never asked about; only NinjaTrader, Tradovate and TradingView were named in the 10-12 reply | 10468221; route record 10-12 |

---

## 6. Suggestions

Ordered by value ÷ cost. **None is authorized by this note.** Each names who decides and what it changes. "Agent-doable" means an agent can do it on direction within existing seat grants.

### 6.1 Before the next weekly trade (deadline 2026-11-06)

1. **Decide who places the weekly trade until T2 is settled.** *Joshua.*
   - Option (a): Joshua places it by hand, which removes the agent and remote-access question for that act.
   - Option (b): keep the standing GO, record that it was weighed against 17069653 / ESA §6.7(b) / KYT, and say why it holds.

   Either way, write the reasoning where the standing GO lives ([Addendum 2026-09-30b](../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-30b)). Cheap, and it removes the only H-severity item with a date on it.
2. **Make the weekly trade look like trading, not a flip.** *Joshua (practice), agent-doable (runbook wording).* T1 suggests a single small position held past 10 seconds with a normal entry and exit, rather than an immediate open-close round trip. Record the practice next to the STATE trigger. This does not settle T1; it lowers the chance that the trade reads as "just to register a trading day".
3. **Check the incumbent account's expiry terms (T7).** *Joshua (dashboard Billing page); agent-doable as a page read if a terms page exists.* An evaluation retained since July is exposed if accounts expire on a clock nobody has recorded.

### 6.2 Questions to send Tradeify (one message, Joshua sends)

Add these to the existing follow-up thread ([follow-up draft](2026-10-21-tradeify-native-followup-questions-DRAFT.md)) rather than opening a new ticket:

4. Does a weekly minimum-activity trade conflict with ESA §6.5's "flipping contracts just to register a 'trading day'"? What form of weekly trade do they consider compliant? (T1, T6)
5. May the account holder use an AI assistant or software agent, operated by and under the sole direction of the holder, to place orders through the platform UI? Is a holder-controlled cloud VM a "prohibited virtualization" technology after a normal login? (T2)
6. When does an evaluation account "expire"? (T7)
7. Is a native strategy on a Rithmic-side platform (Sierra Chart ACSIL, Quantower) within the 10-12 "native" boundary, or only NinjaTrader, Tradovate and TradingView? (T10)
8. Which governs on sizing style, ESA §6.5 or 10468318? (T5)

### 6.3 Repo records (agent-doable on direction; owners named)

9. **Accept the verified Tradeify facts into owner records under Rule 17.** *Owner: envelope §4 Tradeify row and a new funded-stage note.* Use §2–§3 quotes with URL and date. The overlay rows go stale after 2026-12-31 anyway; this does the Tradeify part now.
10. **Fix the two Tradeify-specific wording errors already found:** the envelope DD cell's "$100 lock" lead (register A3.1) and the skill's "Tradeify-style EOD-lock" (register A3.2). *Owners: envelope; skill release.*
11. **Record the cross-platform hedging constraint as a program-level rule** in the four-firm program record, not only in the personal-lane plan (T3). *Owner: four-firm ADR addendum, Joshua ratifies.* It changes how other-firm strategies are chosen: they must never hold an opposing Product-Group position while a Tradeify account is open, or must sit in different Product Groups.
12. **Register the 25K cap conflict (T4)** at the `firm_rules.py` comment. *Owner: firm_rules.* It doesn't touch the 100K live tier.

### 6.4 Research and modelling (each needs its own pre-registration and GO where it spends)

13. **Add a funded-stage simulation before any "measure" claim** (T8). Model Flex and Daily separately: drawdown, lock-on-payout, 30→80-micro scaling, 5-winning-day or buffer eligibility, caps, and the positive-cycle rule. *Owner: prop-firm-challenge methodology; Joshua GOs the engine work.* Without it, a pass has no modelled value, and the early-payout floor effect (§3.3) is invisible.
14. **Score the eval→funded size step explicitly.** Any Tradeify candidate's pre-registration should state its funded starting size (≤30 micros at 100K) and whether its edge holds at that size and the scaling path. Cheap to add to the pre-registration template.
15. **Use Tradovate Risk Settings as a venue-native protective backstop** for the native runbook. Tradovate's own daily loss limit "lock" works "on Tradeify evaluation and Sim Funded accounts" and closes positions and cancels orders (13196348). *Owner: native protection runbook.* It is not a hard stop, and the DLL page warns that losses can overshoot (10468321). But it is a platform-side layer that survives a strategy crash.
16. **Put contract-roll correctness on the native release checklist.** ESA §6.11 makes trading an expired contract a no-intent breach, and stale-price fills are forfeitable. *Owner: native runbook.*
17. **Prepare for verification by design.** Keep a plain-language strategy description Joshua can give unaided (KYT bars AI help during the interview), plus the evidence §6.6 names: sole ownership and "live video of you enabling the code on your own PC". *Owner: native plan; Joshua.*
18. **Treat sim fills as optimistic until measured.** MFFU's "favorable fills" text and Tradeify's "exploitation of simulated conditions" ban mean a strategy should be scored on backtest or live-realistic fills, never tuned on sim fills. *Owner: strategy-validation; fits the existing 1-tick slippage pre-flight.*
19. **Prefer minis at ≥10-micro exposure in Tradeify cost models** (§3.3). *Owner: lab cost models (`lab/discovery/cost_*.py`), which encode micros only.*

### 6.5 Not suggested

- No `core/firm_rules.py` edit from this note. Every value above is web-sourced and unaccepted.
- No contact with Tradeify by an agent. Questions 4–8 are for Joshua to send.
- No change to the standing GO by an agent. Item 1 is Joshua's call.

## Self-review

- Every quote above was re-found in the extracted page text before writing. Article modification dates come from each page's `dateModified`.
- §3.3 arithmetic: the cushion figures use Flex 100K ($3,000 DD; lock floor $100,100) and a $101,000 EOD balance. Pass cost uses $265 + (1/0.172 − 1) × $169 ≈ $265 + 4.81 × $169 ≈ $1,078.
- Search claims ("no repo surface cites §6.5") are bounded to the stated grep over `docs ops core .claude` (M-33).
- Not read within budget: the Lightning, Growth-funded, legacy-live and 300K articles in detail; restricted countries; the Rise payout terms.
