# Tradeify venue deep-dive and suggestions — DRAFT

**Status:** DRAFT, third pass of the [microstructure study](2026-11-01-prop-firm-microstructure-study-DRAFT.md); companion to the [venue-fact register](2026-11-01-prop-firm-venue-fact-register-DRAFT.md). It decides nothing, edits no firm row and authorizes nothing. Every suggestion in §6 is a proposal for Joshua or for the named owner ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal)).
**Date:** 2026-11-01 · **Author:** Claude Code (cloud) · **Repo base:** `main` at `2bc54b2`.
**Budget (Rule 2):** one dig pass over Tradeify's public pages plus one self-review; $0; K = 0. Stopped at the bound.

## Sources and labels

Sources, labels and capture method: [register §I.1](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i1-sources-and-labels). Quotes are verbatim from raw HTML fetched 2026-11-01 and not accepted into any owner record (Rule 17). ESA = the Evaluation Services Agreement at `tradeify.co/funded-trader-agreement`.

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

## 2. Rule inventory

Maintained in [register §I.2](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i2-rule-inventory-evaluation-select-and-growth).

---

## 3. Funded and live stages (not modelled anywhere in the repo)

### 3.1 Terms

Funded terms: [register §I.3](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i3-funded-stage-select-flex-vs-select-daily-at-100k-12853966-10495897). Elite Live terms: [§I.4](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i4-elite-live-12969284-esa-5).

### 3.2 Arithmetic consequences (venue figures; labelled inference)

- **[INF] An early payout tightens the funded floor.** At Flex 100K, five winning days of $200 put EOD balance at $101,000 at minimum, with the floor at $98,000. Requesting a payout then locks the floor at $100,100, so the cushion falls from $3,000 to about $900 before the payout itself (≤ $500) is deducted. Waiting for the natural lock at $103,100 keeps a $3,000 cushion at the moment of lock.
- **[INF] Funded size starts at 3/8 of the eval cap at 100K** (30 vs 80 micros). A book sized near the eval cap must re-size at activation. Funded bust and payout timing are therefore a different simulation from the eval, at a different size.
- **[INF] Cost per pass at the firm's pooled rate.** At Select 100K pricing ($265 + $169 per reset) and the firm-reported 17.2% eval completion rate (pooled across products, so only indicative), expected spend per pass is about $265 + 4.8 × $169 ≈ $1,080. A strategy's own honest-clock pass rate replaces 17.2% in any real estimate.
- **[INF] Micros vs minis at size.** "Trading 10 MES contracts costs $18.20 per round trip, while 1 ES contract costs only $5.76" (10468315). At ≥10 micros of exposure the mini is cheaper per unit of risk, and mini+micro holding is allowed (12268167).

---

## 4. Who trades at Tradeify

Sourced facts: [register §I.5](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i5-who-trades-at-tradeify-sourced).

[INF] Harris reading: evaluation and sim-funded fills meet the simulator, not CME traders; the firm earns fees and pays sim payouts; a ~3% minority reaches real capital, where Tradeify intends to copy the flow. The rulebook (trailing floor, consistency, 10-second rule, hedging and cross-platform bans, ownership, KYT, "exploitation of simulated conditions") is the firm's defence against traders who would otherwise extract payouts from the simulator rather than from the market.

---

## 5. Conflicts and gaps

T1–T10 are maintained in [register §I.6](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i6-tradeify-conflicts-and-gaps-t1t10).

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

9. **Accept the verified Tradeify facts into owner records under Rule 17.** *Owner: envelope §4 Tradeify row and a new funded-stage note.* Use the register §I.2–I.4 quotes with URL and date. The overlay rows go stale after 2026-12-31 anyway; this does the Tradeify part now.
10. **Fix the two Tradeify-specific wording errors already found:** the envelope DD cell's "$100 lock" lead (register A3.1) and the skill's "Tradeify-style EOD-lock" (register A3.2). *Owners: envelope; skill release.*
11. **Record the cross-platform hedging constraint as a program-level rule** in the four-firm program record, not only in the personal-lane plan (T3). *Owner: four-firm ADR addendum, Joshua ratifies.* It changes how other-firm strategies are chosen: they must never hold an opposing Product-Group position while a Tradeify account is open, or must sit in different Product Groups.
12. **Register the 25K cap conflict (T4)** at the `firm_rules.py` comment. *Owner: firm_rules.* It doesn't touch the 100K live tier.

### 6.4 Research and modelling (each needs its own pre-registration and GO where it spends)

13. **Add a funded-stage simulation before any "measure" claim** (T8). Model Flex and Daily separately: drawdown, lock-on-payout, 30→80-micro scaling, 5-winning-day or buffer eligibility, caps, and the positive-cycle rule. *Owner: prop-firm-challenge methodology; Joshua GOs the engine work.* Without it, a pass has no modelled value, and the early-payout floor effect (§3.2) is invisible.
14. **Score the eval→funded size step explicitly.** Any Tradeify candidate's pre-registration should state its funded starting size (≤30 micros at 100K) and whether its edge holds at that size and the scaling path. Cheap to add to the pre-registration template.
15. **Use Tradovate Risk Settings as a venue-native protective backstop** for the native runbook. Tradovate's own daily loss limit "lock" works "on Tradeify evaluation and Sim Funded accounts" and closes positions and cancels orders (13196348). *Owner: native protection runbook.* It is not a hard stop, and the DLL page warns that losses can overshoot (10468321). But it is a platform-side layer that survives a strategy crash.
16. **Put contract-roll correctness on the native release checklist.** ESA §6.11 makes trading an expired contract a no-intent breach, and stale-price fills are forfeitable. *Owner: native runbook.*
17. **Prepare for verification by design.** Keep a plain-language strategy description Joshua can give unaided (KYT bars AI help during the interview), plus the evidence §6.6 names: sole ownership and "live video of you enabling the code on your own PC". *Owner: native plan; Joshua.*
18. **Treat sim fills as optimistic until measured.** MFFU's "favorable fills" text and Tradeify's "exploitation of simulated conditions" ban mean a strategy should be scored on backtest or live-realistic fills, never tuned on sim fills. *Owner: strategy-validation; fits the existing 1-tick slippage pre-flight.*
19. **Prefer minis at ≥10-micro exposure in Tradeify cost models** (§3.2). *Owner: lab cost models (`lab/discovery/cost_*.py`), which encode micros only.*

### 6.5 Not suggested

- No `core/firm_rules.py` edit from this note. Every value above is web-sourced and unaccepted.
- No contact with Tradeify by an agent. Questions 4–8 are for Joshua to send.
- No change to the standing GO by an agent. Item 1 is Joshua's call.

## Self-review

- Every quote above was re-found in the extracted page text before writing. Article modification dates come from each page's `dateModified`.
- §3.2 arithmetic: the cushion figures use Flex 100K ($3,000 DD; lock floor $100,100) and a $101,000 EOD balance. Pass cost uses $265 + (1/0.172 − 1) × $169 ≈ $265 + 4.81 × $169 ≈ $1,078.
- Search claims ("no repo surface cites §6.5") are bounded to the stated grep over `docs ops core .claude` (M-33).
- Not read within budget: the Lightning, Growth-funded, legacy-live and 300K articles in detail; restricted countries; the Rise payout terms.
- Codex review on PR #1022 (2026-11-01): the rule inventory, funded and live terms, sourced population facts and T1–T10 moved to [register §I](2026-11-01-prop-firm-venue-fact-register-DRAFT.md#i-tradeify-evidence-third-pass-2026-11-01) as the single evidence home; this note keeps implications and suggestions.
