# Prop-firm venue-fact register: conflicts, stale facts, gaps and unverified assumptions — DRAFT

**Status:** DRAFT companion to the [microstructure study](2026-11-01-prop-firm-microstructure-study-DRAFT.md). It decides nothing and edits no firm row, envelope cell or locked surface ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal), [Rule 14](../operational_rules.md#rule-14--locked-parameters-and-protection)). Each row names the owner that would have to change.
**Date:** 2026-11-01 · **Author:** Claude Code (cloud) · **Repo base:** `main` at `2bc54b2`.
**Budget (Rule 2):** one dig pass (repo sweep plus public firm pages) and one self-review; $0; K = 0. Stopped at the bound.

## How to read this

**Source labels**
- **[R]** repo-held: the `file:line` cited.
- **[W-raw]** public page fetched 2026-11-01. The quote is copied from the raw HTML text, so it is verbatim. Still **unverified against the repo**: nothing here has been accepted into an owner record (Rule 17).
- **[W-x]** public page read 2026-11-01 through a fetch tool that summarizes. The quotes were extracted by a model, so they are not byte-verified (M-32). Re-read by hand before relying on one.
- **[3P]** third-party site or search snippet. A lead only, never evidence.

**Pages read [W-raw]:**
- Tradeify help centre: `help.tradeify.co` returned 403, so the same articles were read through its Intercom mirror `intercom.help/tradeify/en/articles/<id>`. Each article's `dateModified` is given where it is cited.
- Bulenox: `bulenox.com/help-center/qualification`, `/help-center/master`, `/help-center/funded`, `/accounts-pricing`, `/legal/Bulenox-Rates.pdf` (sha256 `35b9ce39…023167d`, the same file the envelope recorded on 10-02).
- MFFU: articles 9735811, 13134709 and 8444599 at `help.myfundedfutures.com`.
- Tradeify home page: `tradeify.co`.

The HTML pages embed per-request nonces, so their hashes identify a capture; they do not reproduce. No page was saved into the repo.

**Pages read [W-x]:** MFFU 11994562, 13286542 and 9558251; BluSky 12434059 and 17115915.

**Severity:** **H** = could flip a pass/bust, eligibility or compliance call. **M** = biases a figure or a plan. **L** = provenance or wording.

---

## A. Conflicts

### A1. Venue page vs repo

| # | Sev | Fact | Repo says | Venue says now | Owner to amend |
|---|---|---|---|---|---|
| A1.1 | **H** | Bulenox Option 1 trail reference | Engine raises the peak only on the **end-of-day close**, and trails as %-of-peak (`core/mc/simulation.py:561-562`, `:233-238`; F2 caveat `core/mc/preflight.py:30-34`) | [W-raw] accounts-pricing: "Your loss limit follows your highest point — including open positions, in real time. Tracked live during the session, commissions included." | Engine (needs an ADR and a re-MC). Until then, label every Bulenox figure, intraday-honest ones included, as optimistic on this axis |
| A1.2 | M | Bulenox_250K tier | Row exists with $5,500 DD and a 250-micro cap (`core/firm_rules.py:492`); the skill table repeats it (`.claude/skills/prop-firm-challenge/SKILL.md:92`) | [W-raw] accounts-pricing lists only $25,000 / $50,000 / $100,000 / $150,000 (envelope :41 flagged the same on 10-02) | `core/firm_rules.py` row plus the skill mirror; the operator decides retire vs keep |
| A1.3 | M | BluSky contract cap consequence | Caps 50/100 encoded like a hard limit (`core/firm_rules.py:569-570`); envelope §4a treats an over-cap position as a breach unless a firm says otherwise | [W-x] 12434059: "We will not fail you for using too many contracts", yet exceeding terms can bring "liquidation, account restart, or denied brokerage entry" | Envelope §4 BluSky row |
| A1.4 | M | BluSky failure modes | Envelope :44: "only one way to fail" = the trailing floor | [W-x] the same article also lists "Hedging is not allowed in Futures Trading" under things that fail the account. The page contradicts itself | Envelope §4 BluSky row; ask BluSky to clarify |
| A1.5 | M | Eval fee model (the clock behind M-18) | Skill: "a failed eval costs a modest monthly fee, re-purchasable" (`SKILL.md:155`); my study §4.3 said "monthly eval fees" | [W-raw] Bulenox: "$145 one-time … Access valid for 30 days" (25K; $175 / $215 / $325 for 50K / 100K / 150K). Tradeify home page: "one time payment", and the eval has no time limit ([W-raw] 10495915, modified 2026-10-20: "There is no deadline to hit the profit target") | Skill line 155; study §4.3 (corrected in this pass). Bulenox's **30-day access window** is a real deadline the engine does not model |
| A1.6 | L | BluSky NT-rail cost unit | Envelope :44 calls the Tradovate/NT table "a per-side table" | [W-x] 17115915 (dated 2026-09-23): the Tradovate figures are "not explicitly labeled" per side or round trip; the page's per-side definition covers the commission table | Envelope §4 BluSky row; `firm_rules.py:476` proxy |
| A1.7 | L | FXIFY futures product name | Row `FXIFY_Futures_Flex_150K` (`core/firm_rules.py:583`) | [3P] review sites name the futures plans "Standard / Expert / Direct to Sim Live", with no Flex. Unreliable; check against the 10-17 rule sheet's primary capture | FXIFY rule sheet owner |

### A2. Venue page vs venue page (the firm contradicts itself)

| # | Sev | Firm | Conflict | Consequence |
|---|---|---|---|---|
| A2.1 | **H** | MFFU Rapid | [W-x] 13286542 "Rapid Plan 100k" (updated 2026-07-01): "Maximum Loss Limit (EOD)" with "50% (Eval Only)". [W-x] 11994562 (updated 2026-09-25): "30% on our Rapid EOD plans and 50% for Rapid Intraday and Pro plans". [W-raw] 13134709 (Rapid 50K, modified 2026-08-24) also labels the eval MLL "(EOD)" | The repo row (`core/firm_rules.py:339-341, :385`) copies the older pair. The newer page puts **30%** on the EOD plan. Either the article is stale or the plans changed; the row cannot be right for both |
| A2.2 | **H** | Tradeify | [W-raw] home page: "End-of-day drawdown - no intraday traps". [W-raw] help 10495897 (modified 2026-10-15): "enforced in real time against your net liquidation value … your account fails immediately - recovering before the close does not undo it" | Marketing copy contradicts the rule page. The rule page governs; read the marketing line as wrong. This is exactly the misreading behind the 10-02 withdrawal |
| A2.3 | L | Tradeify | The home page's plan tiles carry template text ("Profit Target ? Lorem ipsum dolor. $0") and identical figures across sizes | Never source a number from the home page tiles |

### A3. Repo vs repo

| # | Sev | Conflict | Where | Owner |
|---|---|---|---|---|
| A3.1 | M | Envelope Tradeify DD cell leads with "fixed-$ + $100 lock" while the eval has no lock | `ops/prop_envelope_default.md:42` | Envelope §4 |
| A3.2 | M | Skill says "Tradeify-style EOD-lock" and "`bust_trailing` currently models %-of-peak, EOD", which blurs eval no-lock with the intraday breach | `.claude/skills/prop-firm-challenge/SKILL.md:152` | Skill (release discipline, Rule 38) |
| A3.3 | M | Execution posture: AGENTS.md says c1 is "warm and **disarmed**"; the subscription ledger records CrossTrade cancelled "after the c1 rail retirement" (10-31); envelope E6 still names TV→listener→CrossTrade→Tradovate as the default path | AGENTS.md §Live-execution posture; `docs/pursuits/SUBSCRIPTION_LEDGER.md:21, :42`; `ops/prop_envelope_default.md:21` | Operator (posture); envelope E6 changes only by ADR |
| A3.4 | L | `load_bearing_numbers.md` §1 says "all 7 `dd_type="trailing"` tiers — Tradeify/MFFU **and** Bulenox/BluSky". Tradeify and MFFU are `trailing_locking`; the 7 trailing tiers are Bulenox (5) and BluSky (2) | `docs/load_bearing_numbers.md:17` | That file |
| A3.5 | L | `firm_rules.py` header says "four" in places while the target set has five families (FXIFY provisional) | `core/firm_rules.py:12-14` vs `:645-673`; skill description line 3 says "four-firm configs" | Wording only |
| A3.6 | L | The archive's `CLAUDE.md` (session-loaded with the archive clone) says "No agent may place a trade" and "four automation-friendly prop firms". Both are superseded on `main` (AGENTS.md, Addendum 2026-09-30b; five families) | `first-passage-archive/CLAUDE.md` | None: archive is history. Do not read it as current |

---

## B. Stale facts and stale pointers

| # | Sev | Item | Evidence | Action owed (by owner) |
|---|---|---|---|---|
| B1 | M | Owner-of-record pointer to a missing file: `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` | `core/firm_rules.py:191-192`; not in `git ls-files`, no `lab/ARCHIVED.json` hit | Repoint, or record retrieval via [archive guidance](../ltm/README.md) |
| B2 | L | Bulenox source URLs `/help/qualification-account/` and `/help/master-account/` 404 since the restructure | `core/firm_rules.py:53-56, :122`; envelope :41 | Repoint the comments |
| B3 | M | Envelope overlay rows verified 2026-10-02; stale after **2026-12-31** under the 90-day rule | `ops/prop_envelope_default.md:81` | Scheduled re-verification |
| B4 | L | Growth-specific re-read of 10495897 marked owed | `core/firm_rules.py:542-543` | **Dischargeable:** [W-raw] 10495897 (2026-10-15): "Applies to: All Tradeify accounts (Growth, Select, and Lightning). All accounts use End-of-Day (EOD) trailing drawdown", enforced in real time; and 10495915 (2026-10-20) repeats the real-time rule for Growth |
| B5 | L | Skill eval-economics paragraph ("modest monthly fee") | `SKILL.md:155` | See A1.5 |
| B6 | L | Skill and study both lack the 2026-10 Tradeify purchase limits (§I.2) | — | Gap, not error |
| B7 | M | `SLIPPAGE_TICKS_PER_SIDE = 1.0` still labelled unmeasured | `lab/discovery/cost_mnq.py:28`, `cost_mgc.py:16`; [Q-COSTGEO-2 :14](../briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md) | Measurement owner (§E) |
| B8 | L | Inactivity: engine counts a rolling window, the venue rule is a weekly bucket. Known and documented | `core/firm_rules.py:201-218` | Known; no action here |
| B9 | L | Dispatch paths not found: `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` and `docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md` are absent from the archive at `a75a188` under those paths (sparse `docs/adr` + `docs/ltm/briefs` checkout). The envelope §4 supersedes the survey for venue facts | `git ls-tree` at `a75a188` | None for these notes |

---

## C. Independent re-encodings to sweep whenever a venue fact changes (M-24)

These agree with the venue **today**. They hold their own copy of a value, so they will not follow a `firm_rules.py` edit.

| Venue fact | Independent copy |
|---|---|
| Tradeify flat-by 16:45 ET / 12:59 ET | `ops/c1_rail/book_session_calendar.py:407`; `ops/c1_rail/qualification/production_source.py:859`; `ops/c1_rail/c1_rail_arm.py:327` (message text); `lab/discovery/remc_series_builder.py:130` (`LATE_EXIT_ET = time(16, 45)`, applied regardless of firm; Bulenox allows 16:59) |
| MFFU auto-liquidation 16:10 ET | `lab/discovery/remc_series_builder.py:127, :228-232` |
| Tradeify $0.91/side | `ops/c1_signal_daemon/book_adapters.py:50, :60` (`pine_commission_per_side=0.91`); `lab/research_utils/tv_static_equity.py:24`; `lab/discovery/grow0_harness.py:28` (a pinned expectation) |
| $0.95 (MFFU/BluSky proxy) | `ops/c1_rail/qualification/contract.py:769` (context unread; check before a fee change) |
| Bulenox $0.61 | `lab/discovery/cost_mnq.py:24` (comment) |
| Eval lock literals 103_100 / 100_100 | **None found** in `*.py` outside tests (the 07-28 instance is gone) |

Sweep commands used: `grep -rIn` for those literals over `core ops lab/discovery lab/research_utils` (`*.py`). Notebooks, Pine and private checkouts were not searched.

---

## D. Gaps: venue facts the repo does not hold

[W-raw] unless marked. None of these has been accepted into an owner record.

| # | Sev | Firm | Fact (verbatim where quoted) | Why it matters |
|---|---|---|---|---|
| D1–D8 | — | Tradeify | Moved to §I: funded lock table and payouts → §I.3; Elite Live → §I.4; limits, prices, microscalping and costs → §I.2; copy intent, performance statistics and brokerage → §I.5 | One evidence home (Codex review, PR #1022) |
| D9 | **H** | MFFU | 8444599 (modified 2026-10-30): automated strategies allowed "so long as these automated tools do not aim to exploit the favorable fills offered in the Simulated Environment"; "Exploiting the absence of slippage and utilizing tight brackets to gain from favorable fills are not permitted" | First-party admission that **sim fills are favourable and slippage-free**. A strategy that passes because of that is non-compliant, and it will not survive live. Changes rank of §E-4 |
| D10 | M | MFFU | Rapid 100K sim-funded [W-x] 13286542: "$3,000 from your equity high-water mark (HWM)", "Intra-day trailing", lock at $100; payouts need a "$3,100" buffer, "$500" minimum, daily, 90/10 split. 50K [W-raw] 13134709: "$2,000 from your equity high-water mark", "Intra-day trailing", "Max Loss Lock at $100" | Funded stage is intraday-trailing on the HWM (harsher than eval). No funded rows in repo |
| D11 | M | Bulenox | Account types "Fast Track" and "Momentum" (help-centre navigation and pricing page); "Up to five Master-level accounts at once" | Not in repo |
| D12 | M | Bulenox | Master: "your account is automatically submitted for review … Bulenox verifies your trading activity"; Funded: "After completing three successful payouts on your active Master Accounts, your accounts may be considered for transition to a Funded Account … at Bulenox's discretion"; "A Funded Account provides access to live futures trading using capital provided by Bulenox" | So Qualification and Master are not live capital; live starts only after three payouts, at discretion |
| D13 | L | Bulenox | Professional-status market data "billed at $116/month"; choice "locked for the life of the account" | Cost line not in the repo |
| D14 | M | Bulenox | "Access valid for 30 days" on a one-time fee; suspended accounts can be reset "before" the subscription "expiration date" | A real calendar clock (see A1.5) |
| D15 | M | BluSky | [W-x] Launch plans carry a Launch Fee due within 14 days; non-payment loses the pass | Not in repo |
| D16 | M | All | Lock behaviour of BluSky eval and funded stages, and of the FXIFY funded stage | Unrecorded or unverified |

---

## E. Unverified assumptions, ranked

Score = cost-if-wrong × likelihood-wrong ÷ cost-to-check, each 1–3. Cost-to-check: 1 = read a page or a file; 2 = a re-run, an engine change, or an operator- or firm-side question; 3 = money or live trading. Ties are ordered by cost-if-wrong, then by relevance to the Tradeify-first ruling.

| Rank | Assumption | C | L | K | Score | First check | Moved since the study? |
|---|---|---|---|---|---|---|---|
| 1 | Other firms impose no Tradeify-style native-only or cross-firm exclusivity rule | 3 | 2 | 1 | 6 | Read Bulenox, MFFU, BluSky, FXIFY ToS bot and ownership clauses (MFFU 8444599 allows own automation; BluSky bans mirroring) | Unchanged |
| 2 | Funded-stage and payout rules are known well enough to value a pass | 3 | 2 | 1 | 6 | Accept §I.3–I.4 and D10 into an owner record | **Partly answered** by §I.3–I.4 and D10 (web, unaccepted) |
| 3 | The MFFU Rapid row's clock and consistency belong to one plan | 2 | 3 | 1 | 6 | Decide which MFFU page governs (A2.1); ask MFFU if needed | Sharpened: the firm's own pages conflict |
| 4 | **Sim fills are at least as hard as backtest fills** (1 tick/side) | 3 | 3 | 2 | 4.5 | Attended demo fill study, under operator direction | **Raised:** MFFU states sim fills are favourable and slippage-free (D9). A backtest may be harsher than the eval sim, but such a pass won't carry to live, and exploiting it is barred |
| 5 | No-deadline venues carry no clock | 2 | 2 | 1 | 4 | Read Bulenox access-window and renewal terms | New (A1.5, D14): Bulenox access is valid for 30 days |
| 6 | The engine models Bulenox Option 1 faithfully | 2 | 3 | 2 | 3 | Engine change + ADR + re-MC | **Confirmed wrong** on the text (A1.1); only the size of the effect is unknown |
| 7 | Bulenox_250K exists | 1 | 3 | 1 | 3 | Ask Bulenox, or retire the row | New (A1.2) |
| 8 | BluSky cap and hedging consequences are as encoded | 1 | 3 | 1 | 3 | Ask BluSky to resolve A1.3–A1.4 | New |
| 9 | 1 tick/side **live** slippage and negligible impact at cap sizes | 2 | 2 | 2 | 2 | Run the MNQ flow-depth PREREG | Unchanged |
| 10 | BluSky eval has no lock; NT-rail cost ~0.95/side | 1 | 2 | 1 | 2 | Re-read with unit confirmation (A1.6) | Unchanged |
| 11 | FXIFY Flex lock at start and fees are as encoded | 1 | 2 | 1 | 2 | Byte-verified primary capture (A1.7) | Product name now questioned |
| 12 | Growth breach is intraday like Select | 1 | 1 | 1 | 1 | — | **Resolved** on the page (B4) |

---

## F. Confirmed unchanged on 2026-11-01 (web vs repo agree)

| Fact | Repo | Page |
|---|---|---|
| Tradeify (all confirmations) | see the "Repo" column of §I.2 | — |
| MFFU micro costs $1.90 RT, MGC $2.20, MCL $1.16 | `core/firm_rules.py:387, :390` | [W-raw] 9735811 (2026-08-24) |
| MFFU 16:10 ET auto-liquidation; holiday breach | `core/firm_rules.py:374-376` | [W-x] 9558251 (2026-08-24) |
| MFFU HFT ban, trader copy ban, hedging ban on same underlying | envelope :43 | [W-raw] 8444599 |
| Bulenox 15:59 CT flat-by, no overnight, no min days, Rithmic third-party API $100/month | `core/firm_rules.py:120`; envelope :41 | [W-raw] qualification page |
| Bulenox 25K–150K DD and caps (3/7/12/15 contracts, 1 mini = 10 micros) | `core/firm_rules.py:488-491` | [W-raw] accounts-pricing |
| Bulenox all-in rates MES/MNQ/MYM 0.61, MGC 0.76, 6J 2.36 (no M6J) | `core/firm_rules.py:140` | [W-raw] Rates PDF "Updated Aug/11/2026", second column 1.22 / 1.52 / 4.72 reads as round trip, consistent with the per-side resolution at `:94-113` |
| BluSky EOD trail, breach "at any point", 34% Premium consistency, 4:45 PM recommendation | `core/firm_rules.py:466-473`; envelope :44 | [W-x] 12434059 |

The Bulenox PDF's printed second column (2 × the first) is new support for the per-side reading that `core/firm_rules.py:94-113` argued by arithmetic.

---

## G. Corrections applied to the study draft in this pass

- §2 inference 1: the A-book question is now partly sourced (§I.5, D9). The text says so.
- §4.3: "monthly eval fees" replaced; Tradeify evals are a one-time payment with no deadline, and Bulenox access is valid for 30 days (A1.5).
- §1.3 and §5.2: replaced by links to §A–B and §E (Codex review, PR #1022).

## Self-review

- Every [R] line was opened this session. [W-raw] quotes were copied from extracted HTML text and spot-read against the page text; [W-x] quotes are labelled as model-extracted.
- No account data, Pine, port, `effective_inputs.json` or research backtest dollar figure appears. Dollar figures here are venue rule or fee figures.
- No firm was contacted, no order placed, no row or locked surface edited.
- Not done within budget: Bulenox accordion sections (Option 1/2 detail, Withdrawal Rules, Inactivity) load by script and were not read; BluSky and FXIFY ToS bot clauses were not read; nothing outside `*.py` was swept in §C.

---

## H. Tradeify third pass

See §I. Its three H-severity items are T1 (the agreement's §6.5 against the weekly preservation trade), T2 (account-operation, KYT and remote-access rules against agent-placed trades and VM hosts) and T3 (cross-platform hedging binding other-firm strategies). Suggestions live in the [deep-dive §6](2026-11-01-tradeify-venue-deep-dive-DRAFT.md#6-suggestions).

---

## I. Tradeify evidence (third pass, 2026-11-01)

The one maintained home for Tradeify venue evidence gathered on 2026-11-01. The [Tradeify deep-dive](2026-11-01-tradeify-venue-deep-dive-DRAFT.md) links here and keeps only implications and suggestions. Nothing below is accepted into an owner record (Rule 17).

### I.1 Sources and labels

All quotes are **[W-raw]**: copied from the raw HTML of public pages fetched 2026-11-01. They are verbatim, but **not accepted into any owner record** (Rule 17).

- **Help centre:** read through Tradeify's Intercom mirror `intercom.help/tradeify/en/articles/<id>`, because `help.tradeify.co` returns 403 to scripted fetches. I listed 71 articles from the six rule collections and read 41. Each article's `dateModified` is given as "(mod. YYYY-MM-DD)".
- **Agreement:** `tradeify.co/funded-trader-agreement`. The page is titled **"Evaluation Services Agreement"**, says "Last modified: October 2026", and is cited as **ESA §n**.
- **Home page:** `tradeify.co`.

No account data, Pine, port or research backtest figure appears in this note. Dollar figures are Tradeify's published rule, fee and payout figures.

### I.2 Rule inventory (evaluation, Select and Growth)

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
| Simulated conditions | Prohibited: "exploitation of simulated conditions" | 17069653 | Same theme as MFFU's "favorable fills" (D9) |
| VPS/VPN | "You cannot log in with VPN/VPS. After logging in normally, you may use VPS for trading at your own risk." | 12268494 | Recorded ([follow-up draft :37](2026-10-21-tradeify-native-followup-questions-DRAFT.md)) |
| Limits | 15 Select evals per 30 days; 10 resets per eval per 30 days; 5 funded per individual **and household** (V2 300K up to 8) | 10468251 (2026-10-20) | Not encoded |
| Products | No M6J (micro FX = "M6E, M6A"); no US Treasuries in the root list; micro round trip "$1.82" (MNQ/MYM/MES), "$2.12" (MGC/MCL); minis ES/NQ/YM "$5.76" | 10468222 (2026-10-18); 10468315 (2026-10-17) | Matches (`core/firm_rules.py:270-275, :326, :330`) |
| Prices | Select 100K **$265**, reset **$169**; with 50% add-on $329 / $209; Growth 100K $255 / $169 | 14369021 (2026-10-19) | Ledger row d15 still open |

### I.3 Funded stage: Select Flex vs Select Daily at 100K (12853966, 10495897)

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

### I.4 Elite Live (12969284; ESA §5)

- **Eligibility:** "3 payouts on a single account, or 10 total payouts since the last live transition". This is "not automatic qualification".
- **On transition:** "All Sim Funded and evaluation accounts are closed"; only accounts with ≥1 payout move.
- **100K Elite:** start balance $0, EOD drawdown $3,000, "4 mini / 40 micro" until above the drawdown, then 8/80, no DLL, lock at $3,100. "Elite Live: Trade with real capital in live markets, with daily payouts at an 80/20 profit split" (12268494).
- **Broker:** "all Tradeify Elite Live accounts are issued through and facilitated by NinjaTrader and GFF Brokers" (ESA §5).
- **Payout before lock:** the floor moves up first, then the payout is deducted, "leaving the trader with only $1,500 of effective drawdown room instead of $2,000" (50K example).

### I.5 Who trades at Tradeify (sourced)

- "This is how a futures prop firm works: you trade the firm's simulated capital and receive real payouts when you meet the payout rules." (12268494)
- "Tradeify is looking for traders that … can be called up to live to eventually be copied by our own firm as well." (10468318)
- Trader Performance Statistics, Aug 2025–Jul 2026 (home page): 17.2% of evaluations completed; 40.3% of participants reached funded (median 3 evaluations each); 28.5% of funded participants received a payout; 3.0% of funded participants were called up to live.
- "Tradeify Brokerage LLC d/b/a Slay Markets is a CFTC-registered introducing broker guaranteed by NinjaTrader Clearing, LLC" (home page). The 10-30 reply says "NinjaTrader owns the clearing firm" (route record).
- "Simulated Funded Account … your trades mirror what would happen in the live markets, but your profits and losses are not real." (10468257, mod. 2026-10-20). Tradeify claims sim realism; MFFU says its sim gives "favorable fills" (D9). Neither firm publishes its fill model.

### I.6 Tradeify conflicts and gaps T1–T10

| # | Sev | Item | Evidence |
|---|---|---|---|
| T1 | **H** | ESA §6.5 "flipping contracts just to register a 'trading day'" vs the weekly preservation round trip and ESA §6.9 | [deep-dive §1](2026-11-01-tradeify-venue-deep-dive-DRAFT.md#1-what-changed-in-the-picture) item 1 |
| T2 | **H** | Agent-operated orders and remote or VM hosts vs "personally … operate their account", "third party" management, KYT, and "prohibited virtualization, remote-access" | deep-dive §1 item 2 |
| T3 | **H** | Cross-platform opposing positions bind every other-firm strategy, not just the personal lane | ESA §6.7(c), (i) |
| T4 | M | 25K eval cap: 1/10 (12853921, 10495915) vs 2/20 (12853966) | §I.2 |
| T5 | M | ESA §6.5 "avoiding dollar-cost averaging … consistent trading sizes" vs 10468318 "no rules against … DCA, flipping, or scaling" | §I.2 |
| T6 | M | Activity: "Monday through Friday" (help) vs "calendar week" (ESA §6.9) | §I.2 |
| T7 | M | "Account expires" appears in FAQs without a stated condition | 12268494, 10468256 |
| T8 | M | Funded rows (Flex, Daily), scaling, payout mechanics and live terms are absent from `core/firm_rules.py` and every lab harness I know of | §I.3–I.4 |
| T9 | L | ESA §4.1 still lists "Advanced Challenge"; the stats pool "Growth, Advanced and Select" | ESA; home page |
| T10 | L | Rithmic-platform (Sierra Chart, Quantower, Tradesea) native automation was never asked about; only NinjaTrader, Tradovate and TradingView were named in the 10-12 reply | 10468221; route record 10-12 |
