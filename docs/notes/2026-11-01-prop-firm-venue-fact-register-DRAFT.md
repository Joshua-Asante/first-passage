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
| B6 | L | Skill and study both lack the 2026-10 Tradeify purchase limits (below, D2) | — | Gap, not error |
| B7 | M | `SLIPPAGE_TICKS_PER_SIDE = 1.0` still labelled unmeasured | `lab/discovery/cost_mnq.py:28`, `cost_mgc.py:16`; [Q-COSTGEO-2 :14](../briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md) | Measurement owner (§E) |
| B8 | L | Inactivity: engine counts a rolling window, the venue rule is a weekly bucket. Known and documented | `core/firm_rules.py:201-218` | Known; no action here |

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
| D1 | **H** | Tradeify | Funded lock table (10495897, 2026-10-15): EOD balance that triggers the lock at 100K is Growth $103,600 / Lightning $104,100 / Select Flex $103,100 / Select Daily $102,600; at 150K $155,100 / $155,350 / $154,600 / $153,600. The lock also triggers "immediately when you request a payout". Floor locks at "$100 above starting balance" | Implies funded DDs at 100K of $3,500 / $4,000 / $3,000 / **$2,500** (Select Daily). No funded rows exist in `firm_rules.py` |
| D2 | M | Tradeify | 12853921 (2026-10-19): "Maximum 15 evaluations can be purchased within any 30-day period"; "Each evaluation can be reset up to 10 times within a 30-day period"; "You can hold up to 5 funded accounts simultaneously"; a $300,000 Select tier ("limited release", KYC, no resets, 3 lifetime) | Caps account-level breadth and retries; $300K tier absent |
| D3 | **H** | Tradeify | Select funded payouts (12853921): Flex "Every 5 winning days", caps "Up to 50% of profits ($1,250 / $2,500 / $3,500 / $4,500 caps for accounts bought on or after September 1, 2026…)". Daily: caps "$600 / $1,250 / $1,750 / $2,500", "Daily Loss Limit: Yes ($500 / $1,000 / $1,250 / $1,750)", buffer "$1,100 / $2,100 / $2,600 / $3,600" | The repo has no payout owner (B1). These are the inputs a pass-value or "measure" step needs |
| D4 | M | Tradeify | Microscalping, funded only (10468318, 2026-10-17): payout requires "Over 50% of your trades are longer than 10 seconds" and "Over 50% of your profit must come from trades held longer than 10 seconds". Failing it blocks payouts, not the account | Constrains short-hold designs; weekly token trades count toward the trade-count half |
| D5 | **H** | Tradeify | 10468318: "Tradeify is looking for traders that … can be called up to live to eventually be copied by our own firm as well"; "We scan to ensure there are no similar orders on other accounts" | Sourced A-book intent for called-up traders (study §2, inference 1) |
| D6 | **H** | Tradeify | Home page disclosure, "Trader Performance Statistics (August 2025 – July 2026, calculated as of 9 August 2026)": "(a) 17.2% of evaluation accounts initiated were successfully completed …; (b) 40.3% of individual participants … advanced …, initiated a median of 3 each …; (c) 28.5% of individual participants at the Funded Level received a payout; and (d) 3.0% of individual participants trading in a Funded Account were called up to a Live Funded Account" | The only sourced population figures for "who trades". [INF] 17.2% sits near the study's zero-edge trailing benchmark (13.5% at T/D = 2), consistent with a near-zero-edge population, but the products are pooled, so read it only as context |
| D7 | M | Tradeify | 10468315 (2026-10-17): micro round trip $1.82 (MNQ/MYM/MES), $2.12 (MGC/MCL); minis ES/NQ/YM $5.76, GC $6.20. "Trading 10 MES contracts costs $18.20 per round trip, while 1 ES contract costs only $5.76" | At ≥10 micros of exposure, the mini costs ~68% less (arithmetic). The repo encodes micro costs only; mini+micro mixing is allowed (12268167) |
| D8 | M | Tradeify | Tradeify Brokerage LLC d/b/a Slay Markets, "a CFTC-registered introducing broker guaranteed by NinjaTrader Clearing, LLC" (home page) | Fits the 10-30 "NinjaTrader owns the clearing firm" reply |
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
| 2 | Funded-stage and payout rules are known well enough to value a pass | 3 | 2 | 1 | 6 | Accept D1, D3, D10 into an owner record | **Partly answered** by D1, D3, D10 (web, unaccepted) |
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
| Tradeify eval has no drawdown lock | `core/firm_rules.py:284-286` | [W-raw] 10495897: "Evaluation accounts do not have drawdown locking." |
| Tradeify EOD-updated, real-time-enforced trail | `core/mc/simulation.py:351-357` | [W-raw] 10495897, 12853921, 10495915 |
| Tradeify Select eval DD $1,000 / $2,000 / $3,000 / $4,500; caps 10/40/80/120 micro; 40% consistency (50% add-on); no DLL | `core/firm_rules.py:498-501, :335-336` | [W-raw] 12853921 (2026-10-19) |
| Tradeify flat-by 16:45 / 12:59; auto-close non-fatal | `core/firm_rules.py:253-255` | [W-raw] 10495876 (2026-10-17) |
| Tradeify weekly activity rule, per account | `core/firm_rules.py:181-200` | [W-raw] 10468318, 12268167 |
| Tradeify bots: sole owner, exclusive within Tradeify, no HFT, live video | route record 10-30 | [W-raw] 10468318 |
| Tradeify Tradovate API "only available for LIVE funded accounts" | envelope :42 | [W-raw] 10468222 (2026-10-18) |
| Tradeify: no M6J (micro FX = M6E, M6A); no US Treasuries | envelope §5; `core/firm_rules.py:270-275` | [W-raw] 10468222 root list |
| Tradeify micro costs $1.82 RT ($0.91/side), MGC/MCL $2.12 | `core/firm_rules.py:326, :330` | [W-raw] 10468315 |
| Growth 100K: $3,500 DD, $2,500 soft DLL, 80 micro cap, 1 day, no consistency | `core/firm_rules.py:551-559` | [W-raw] 10495915 |
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

- §2 inference 1: the A-book question is now partly sourced (D5, D6, D9). The text says so.
- §4.3: "monthly eval fees" replaced; Tradeify evals are a one-time payment with no deadline, and Bulenox access is valid for 30 days (A1.5).
- §5.2: points here for the re-ranked list.

## Self-review

- Every [R] line was opened this session. [W-raw] quotes were copied from extracted HTML text and spot-read against the page text; [W-x] quotes are labelled as model-extracted.
- No account data, Pine, port, `effective_inputs.json` or research backtest dollar figure appears. Dollar figures here are venue rule or fee figures.
- No firm was contacted, no order placed, no row or locked surface edited.
- Not done within budget: Bulenox accordion sections (Option 1/2 detail, Withdrawal Rules, Inactivity) load by script and were not read; BluSky and FXIFY ToS bot clauses were not read; nothing outside `*.py` was swept in §C.
