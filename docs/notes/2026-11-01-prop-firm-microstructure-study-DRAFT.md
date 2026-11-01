# Prop-firm microstructure study (Harris, *Trading and Exchanges*, Parts I–III) — DRAFT

**Status:** DRAFT study note for Joshua's reading. It decides nothing, changes no firm row and authorizes nothing ([Rule 3](../operational_rules.md#rule-3--the-operator-decides-grants-are-literal)). Not a deployment, strategy or capital decision.
**Date:** 2026-11-01 · **Author:** Claude Code (cloud) · **Base:** `main` at `2bc54b2`; archive `first-passage-archive` at `a75a188` (sparse, `docs/adr` only).
**Budget (Rule 2):** one study pass plus one self-review; $0; K = 0 (no trials, no runs). Stopped at the bound.
**Scope:** the firms in `core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS` ([`core/firm_rules.py:645-673`](../../core/firm_rules.py)): Bulenox, Tradeify, MyFundedFutures (MFFU), BluSky, FXIFY Futures (provisional).

**Evidence labels used below.**
- **[R]** repo-held, with file:line. These are venue facts as the repo last recorded them (Rule 17 quotes live at the cited line). They are not re-verified here.
- **[RV]** repo-held but flagged by the repo itself as owed, provisional, proxied or conflicting: needs re-verification before use.
- **[INF]** inference or textbook model, not sourced. Never a venue fact.
- **No web research was done this pass.** Every venue fact below comes from the repo. Public firm pages were not re-read, so nothing here is newer than its cited repo date.

Reading limits: every bust figure quoted is from its RESULTS owner ([Rule 20](../operational_rules.md#rule-20--figures-come-from-their-owner)); the closed-form numbers in §4 are model arithmetic on repo venue inputs, labelled [INF], not MC results and not claims about any strategy.

---

## 0. Harris in one paragraph, mapped to this program

Harris asks three questions of any market: what are the **rules** (order types, priority, who may trade when), **who trades** and why (informed traders, uninformed or utilitarian traders, dealers who supply liquidity, and parasitic traders who exploit order flow), and **where liquidity and transaction costs come from** (spread = order-processing + inventory + adverse-selection components; impact rising with size relative to depth). A prop-firm evaluation is a market layered over CME: the firm writes a second rulebook (drawdown, target, consistency, flat-by, platform), runs most of the trading on a simulator, and is itself a counterparty to the trader's *option* on the payout. The program's costliest reversals were all second-rulebook facts: the DJ30→MYM cost and force-flat wall ([archive R6 ADR:20,33](https://github.com/Joshua-Asante/first-passage-archive/blob/a75a188/docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md)), the eval-lock correction ([ADR 07-22 §1–§2](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#1--context)), the intraday-honest withdrawal ([Addendum 10-02](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-10-02--the-2026-09-03-discharge-withdrawn-an-intraday-honest-clear-is-required-accepted)), and the native-logic reply ([route record 10-12](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts)).

---

## 1. Trading rules (Harris Part I)

### 1.1 Per-firm, per-tier table (evaluation stage unless stated)

Common to the rows below unless noted: profit target 6% of starting balance; no weekend or overnight holds; evaluation rows only. File lines are `core/firm_rules.py` unless another file is named. "Envelope" = [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) §4, rows at lines 41–44, verified 2026-10-02.

| Tier | Start | Max DD ($) | DD type and clock | Lock in eval? | DLL | Consistency | Min days | Micro cap | Cost/side (index micros) |
|---|---|---|---|---|---|---|---|---|---|
| Bulenox_25K/50K/100K/150K/250K | 25K…250K | 1,500 / 2,500 / 3,000 / 4,500 / 5,500 [R :488-492] | Option 1 trailing; trails the high "including both realized and unrealized (open) profits" [R envelope :41] → **intraday ratchet and intraday breach** | No (lock is Master-stage, start + $100) [R :59-87 comment] | None (Option 1) [R :135] | None at eval; 40% at payout [R :122-124] | 0 [R :137] | 30/70/120/150/250 [R :488-492]; 250K tier **not on the 10-02 pricing page** [RV envelope :41] | $0.61 (MGC $0.76) [R :140] |
| Tradeify_Select_25K/50K/100K/150K | 25K…150K | 1,000 / 2,000 / 3,000 / 4,500 [R :498-501] | Fixed-$ trail; floor ratchets on EOD balance; breach "enforced in real time against your net liquidation value" [R envelope :42; `core/mc/simulation.py:351-357`] | **No** — "Evaluation accounts do not have drawdown locking" [R :284-286] | None (Flex) [R :322] | 40%, soft at-pass gate [R :336, :245-247] | 3 (forced by consistency) [R :335] | 10/40/80/120, **account-aggregate** [R :219-233, :498-501] | $0.91 (MGC $1.06) [R :326] |
| Tradeify_Growth_100K | 100K | 3,500 [R :554] | As Select; Growth-specific re-read of art. 10495897 **owed** [RV :535-543] | No [R :552] | $2,500 **soft** (stops the day, does not fail) [R :520-533, :555] | None [R :558] | 1 [R :556] | 80 [R :557] | $0.91 [R :552] |
| MFFU_Rapid_50K/100K | 50K/100K | 2,000 / 3,000 [R :563-564] | EOD trailing MLL in eval; funded switches to intraday + $100 lock [R :339-341] | No [R :379] | None [R :380] | 50% soft [R :385] — **conflicts with envelope**, see §1.3 C1 | 2 [R :382] | 50/80; over-cap "can result in a BREACH" [R :358-364] | $0.95 (MGC $1.10) [R :387] |
| BluSky_Premium_50K/100K | 50K/100K | 2,000 / 3,000 [R :569-570] | EOD trail, floor ratchets on EOD peak; breach if balance hits floor "at any point" [R envelope :44] | Not recorded either way [gap] | None in primary article [R :467] | 34% soft (re-scales target) [R :473] | 0 [R :469] | 50/100 [R :569-570] | $0.95 **NT-schedule proxy, not venue-published** [RV :476, :409-414] |
| FXIFY_Futures_Flex_150K | 150K | 4,500 [R :588] | Fixed-$ EOD trail [R :587] | **Yes, at the starting balance** (`dd_lock_offset_usd: 0.0`) [RV :589; provisional :573-582] | $3,000 soft, read-only [R :591] | 50% soft [R :594] | 2 (derived) [R :593] | 100 [R :596] | **Unknown** [RV :598] |

### 1.2 Firm-wide rules (flat-by, news, inactivity, platform, automation, funded vs eval)

| Firm | Flat-by (ET) | News | Inactivity | Platforms and automation | Eval → funded differences; payouts |
|---|---|---|---|---|---|
| Bulenox | 16:59 (15:59 CT), "All positions must be closed by 3:59 PM (CT)" [R envelope :41] | "News trading allowed" [R envelope :41] | ≥1 trade per 5 trading days [R :124-132, :139] | Algos via Rithmic third-party API, "$100 monthly fee" [R envelope :41] | Master: no reset; floor locks at start + $100; 40% payout consistency, cumulative [R :59-87, envelope :41]. Payout split and caps: **not in repo** |
| Tradeify | 16:45 regular, 12:59 holiday-short; auto-flatten non-fatal [R :253-255, envelope :42] | "Tier 1 News Trading: You're allowed" (Select eval) [R envelope :42] | ≥1 trade per Mon–Fri week; inactive accounts "deleted after an email warning", not reactivatable [R :181-200] | Eval and sim-funded: strategy logic must be native to NinjaTrader, Tradovate or TradingView-via-Tradovate; no bridges or direct API; API only on live funded ("No exceptions") [R route record 10-12]; strategy owned exclusively; **a strategy run at Tradeify may not run at another prop firm** [R route record 10-30]. Hedging across a Product Group banned, in one account or across accounts [R :256-266; envelope §4a] | Lock exists only in sim-funded (start + $100) [R :284-286]; consistency removed in funded [R :245-247]; funded caps scale from a reduced base [R :220-221]. Payout rules: owner pointer is **dangling** (§1.3 C5) |
| MFFU | 16:10 auto-liquidation; holiday half-days no auto-liq and "will result in breaching" [R envelope :43] | T1 permitted on all evaluations; prohibited on Rapid and Pro sim-funded [R envelope :43] | ≥1 trade/week [R :384] | Own-settings automation OK; HFT banned; trader-to-trader copying banned [R envelope :43] | Funded: intraday trail + $100 lock [R :340-341]; SI/HG/PL/NG/QG restricted; metals micros capped [R envelope :43]. Payouts: not in repo |
| BluSky | ~16:45 derived; "We recommend closing all trades before 4:45PM EST" [R envelope :44] | "at your own risk"; does not fail the account [R envelope :44] | "inactive for 30 consecutive days may be closed at our discretion" → encoded 22 idle business days [R :431-471] | "Semi-automated and full automated" welcomed; conduct policy bans account mirroring [R envelope :44] | Funded pricing "set by brokerage" [R :406-408]. Payouts: not in repo |
| FXIFY Futures | not encoded [gap] | open conflict, unencoded [RV :578-579] | 14 calendar days + 7 grace, unencoded [R :597] | not encoded here; see the [rule sheet](2026-10-17-fxify-futures-flex-150k-evaluation-rule-sheet.md) | Funded lock unverified [R rule sheet :36] |

### 1.3 Conflicts, gaps and stale entries found

| # | Finding | Evidence | Direction if wrong |
|---|---|---|---|
| C1 | **MFFU Rapid row mixes two plans.** The row encodes an EOD MLL with 50% consistency. The envelope's 10-02 re-read says "30% on our Rapid EOD plans and 50% for Rapid Intraday", and the 100K source article 13286542 is the Intraday-Drawdown Rapid. | `core/firm_rules.py:339-341, :385` vs envelope :43 | Either the clock (EOD vs intraday) or the consistency (30 vs 50) is wrong for any one plan |
| C2 | **Bulenox Option 1 ratchets on the intraday high; the engine ratchets on the EOD close and as %-of-peak.** `intraday_low` fixes the breach test only; the peak update is `if equity > peak` on the close. The F2 %-of-peak caveat is known; an intraday-high ratchet gap was **not found** in the closure, preflight or R1 RESULTS I searched (not proof of absence, M-33). | envelope :41; `core/mc/simulation.py:533, :561-562`; `core/mc/preflight.py:30-34, :151-152` | Optimistic: every Bulenox bust figure, honest-clock included, is low on this axis |
| C3 | BluSky cost proxy 0.95 vs the 10-02 published NT-rail table ($0.94 free / $0.84 monthly / $0.64 lifetime; MGC $1.29/$1.19/$0.99) and $0.50 flat on Rithmic-class eval rails. Flagged, not edited. | `core/firm_rules.py:476`; envelope :44 | Proxy slightly pessimistic on the free plan |
| C4 | Envelope Tradeify DD cell opens "Trailing-locking (Select, fixed-$ + $100 lock)" before saying eval has no lock. | envelope :42 | Misreads the eval as locked (the 07-22 defect, M-24) |
| C5 | `firm_rules.py` names `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md` as the owner of record for inactivity enforcement; the file is not in the tree, and no `lab/ARCHIVED.json` entry by that name was found. No repo surface owns **payout rules** for any firm. | `core/firm_rules.py:191-192` | Funded-stage economics unmodeled |
| C6 | Bulenox comment sources cite `/help/qualification-account/` and `/help/master-account/`, which 404 since the 10-02 restructure; the Rates PDF moved and its hash drifted (values unchanged). | `core/firm_rules.py:53-56, :122`; envelope :41 | Provenance only |
| C7 | Inactivity: venue is a weekly bucket, engine counts rolling idle business days (over-fires on a complete calendar, under-fires on a sparse one). Known and documented. | `core/firm_rules.py:201-218`; [`load_bearing_numbers.md` §2](../load_bearing_numbers.md) | Known both ways |
| C8 | E6 default still names the TV→listener→CrossTrade→Tradovate chain. CrossTrade is cancelled and the rail described as retired (ledger 10-31), Tradeify bars bridges for eval, while AGENTS.md says c1 is "warm and **disarmed**". Posture wording disagrees across surfaces. | envelope :21, amendment 08-06; [`SUBSCRIPTION_LEDGER.md:21, :42`](../pursuits/SUBSCRIPTION_LEDGER.md); AGENTS.md §Live-execution posture | Stale default |
| C9 | Growth's intraday-breach reading rests on a Select-page read; Growth-specific re-read owed. | `core/firm_rules.py:535-543` | Probably none (same article) |
| C10 | FXIFY row provisional: commissions unknown, news conflict, FAQ capture not byte-verified. | `core/firm_rules.py:573-598` | Unknown |
| G1 | Overlay rows were verified 2026-10-02; the 90-day rule makes them stale after **2026-12-31**. | envelope :81 | Due date |
| G2 | Dispatch paths not found: `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` and `docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md` are absent from the archive at `a75a188` under those paths (sparse `docs/adr` + `docs/ltm/briefs` checkout). The envelope §4 supersedes the survey for venue facts. | `git ls-tree` at `a75a188` | None for this note |

---

## 2. Who trades (Harris Part II)

### 2.1 Sourced facts

- **Eval and sim-funded accounts are simulated.** Tradeify names its pre-live stage "Sim Funded" [R `firm_rules.py:284-286`]; the Tradovate API is "only available for LIVE funded accounts" [R envelope :42]; MFFU and BluSky name SimFunded stages [R envelope :43; `firm_rules.py:432-434`]. Tradeify Compliance: "Market data is provided through CQG. NinjaTrader owns the clearing firm" [R route record, Addendum 10-30].
- **Firms police the population with conduct rules:** HFT bans (Tradeify, MFFU), trader-to-trader copy bans (MFFU), mirroring bans (BluSky), hedging bans across accounts and product groups (Tradeify, MFFU), exclusive ownership and no cross-firm use (Tradeify), possible live-video verification and source review (Tradeify) [R envelope :42-44, §4a; route record 10-30].
- **Inactive or abandoned accounts are deleted or closed** (Tradeify mandatory; BluSky discretionary) [R `firm_rules.py:181-200, :431-464`].

### 2.2 Inferences (Harris framing) [INF]

1. **In eval and sim-funded, no CME participant takes the other side.** Fills come from the platform simulator against the CQG feed. The economic counterparty is the firm: the trader pays a fee for an option whose payoff is a future payout, and the firm's P&L is fees minus payouts (plus resets and add-ons). Whether any firm copies successful traders' flow to a live account (A-book) or simply pays from fee income (pure B-book on a simulator) is **not sourced in the repo**.
2. **The rulebook is the firm's adverse-selection defence.** In Harris's terms the firm is a dealer facing a mix of uninformed traders (most fee payers) and informed or option-exploiting traders. Each rule targets a known exploit of a free option: the trailing drawdown caps the option's payoff relative to peak; consistency rules block one lucky day; hedging bans across accounts block the "long in one account, short in another, one always passes" construction; cross-firm exclusivity and copy bans stop one edge being sold to many firms; HFT bans and source review screen out traders who exploit the simulator's fill model rather than the market. A strategy that looks like any of these will be treated as one.
3. **Simulator fills are the grading surface.** The eval is scored on the simulator's fill model, not CME queue position. A thin edge can pass or fail on how the simulator fills stops and limits and how it applies the auto-flatten ("non-fatal (slippage only)", [R envelope :42]). The repo holds **no measurement** of any firm's simulator fill model (§5 rank D).
4. **At the live funded stage, CME counterparties apply.** Standard microstructure says micro equity-index and gold futures flow meets electronic market makers and other short-horizon liquidity providers at the touch, with larger directional participants mostly in the full-size contracts that micros arbitrage against. None of this is sourced in the repo; no CME participant-composition data was read.

---

## 3. Origins of liquidity and costs (Harris Part III)

### 3.1 Repo-held cost inputs

| Instrument | Tick | Tick value | Commission RT (Tradeify / Bulenox / MFFU) | 1-tick/side slip, RT | All-in RT, Tradeify | All-in RT in ticks |
|---|---|---|---|---|---|---|
| MNQ | 0.25 | $0.50 | $1.82 / $1.22 / $1.90 | $1.00 | **$2.82** | 5.6 |
| MYM | 1.0 | $0.50 | $1.82 / $1.22 / $1.90 | $1.00 | **$2.82** | 5.6 |
| MGC | 0.10 | $1.00 | $2.12 / $1.52 / $2.20 | $2.00 | **$4.12** | 4.1 |
| M6J | — | — | **not offered at any checked firm** [R envelope §5 finding] | — | — | — |

Sources: ticks [`core/instrument_specs.py:17-22`](../../core/instrument_specs.py); commissions `firm_rules.py:140, :326, :387` (per side ×2); slippage `SLIPPAGE_TICKS_PER_SIDE = 1.0` in [`lab/discovery/cost_mnq.py:28`](../../lab/discovery/cost_mnq.py) and `cost_mgc.py:16`, which the repo itself calls **unmeasured, 35–45% of the round trip** ([Q-COSTGEO-2 :14](../briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md)). The Tradeify MNQ/MYM $2.82 matches the ST-EH-1 frozen cost ([prereg :102](../briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md)); Bulenox MNQ RT $2.22 matches [ORB RESULTS :102](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md).

### 3.2 What the costs mean

- **Spread vs fill.** At one tick of spread, a limit entry that fills at its price earns the half-spread; a stop entry pays at least the half-spread plus momentum slip. M-16's anchor: a real effect with +0.058R cost-net edge went negative at ~0.9 pt of entry slip ([M-16](../methodology/lessons/methodology_lessons.md)). Commission alone is 3.6 ticks RT on MNQ/MYM at Tradeify, so an edge must clear ~5.6 ticks per round trip before it is real (Harris: order-processing cost dominates in a one-tick market; adverse selection shows up as stop-entry slip).
- **Impact at capped sizes.** Caps are 10–250 micros (§1.1) and account-aggregate. The repo holds **no depth or impact measurement** (the MNQ flow-depth study has a PREREG and no RESULTS: `lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/`). [INF] at single-digit to tens of micros per order, impact in MNQ/MYM is likely small against displayed depth outside the open, the flatten and releases; it is not small for pyramided stacks — the DJ30→MYM edition ran "up to 114-contract pyramid stacks", above Tradeify Select 100K's 80-micro account cap ([prototype RESULTS :28](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md)).
- **Force-flat.** Every firm flattens intraday (16:10–16:59 ET, §1.2). This caps holding time, truncates trend-day winners, and concentrates exits into a crowded minute. The DJ30→MYM falsification names exactly this: commission + slippage on large stacks, "EOD force-flat truncating trend-day holds", and integer/RESERVE pyramid quantization; OOS PF ratio 0.559 against a 0.8× bar ([archive R6 ADR :20, :33](https://github.com/Joshua-Asante/first-passage-archive/blob/a75a188/docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md)).
- **Intrabar ordering.** With bar data, a bar that touches both stop and target has unknown order. Pessimistic ordering (stop first) is the honest default against an intraday breach clock, because a touch of the floor fails the account even if the bar closes up (`simulation.py:351-357`).

---

## 4. Barrier dynamics

### 4.1 Geometry: target-to-trail ratio T/D (repo inputs; arithmetic)

T = 6% target, D = max DD, both from §1.1.

| T/D | Tiers |
|---|---|
| 1.00 | Bulenox_25K |
| 1.20 | Bulenox_50K |
| 1.50 | Tradeify_Select_25K/50K, MFFU_Rapid_50K, BluSky_Premium_50K |
| 1.71 | Tradeify_Growth_100K |
| 2.00 | Bulenox_100K/150K, Tradeify_Select_100K/150K, MFFU_Rapid_100K, BluSky_Premium_100K, FXIFY_Flex_150K |
| 2.73 | Bulenox_250K |

### 4.2 Zero-edge benchmark: static vs trailing [INF, textbook]

For a driftless continuous random walk, P(reach +T before a **static** floor D below start) = D/(D+T). Against a **continuously trailing** floor (always D below the running peak), the gain made before the first drawdown of size D is exponential with mean D, so P(pass) = e^(−T/D).

| T/D | Static | Trailing |
|---|---|---|
| 1.00 | 50.0% | 36.8% |
| 1.50 | 40.0% | 22.3% |
| 1.71 | 36.8% | 18.0% |
| 2.00 | 33.3% | 13.5% |
| 2.73 | 26.8% | 6.5% |

Read: at the common T/D = 2, trailing cuts a coin-flipper's pass rate from one in three to one in seven. Costs make the drift negative, so a zero-gross-edge trader does worse than this column. An EOD-only ratchet sits between the columns (the floor moves less often); an intraday breach test moves results toward the trailing column and beyond (§4.4). Growth's extra $500 of rope at the same target buys +4.5 pp here, the "binding gate" point the [Growth ADR](../adr/2026-08-24-tradeify-growth-tier-scoring-only.md) and `firm_rules.py:512-518` make.

### 4.3 With edge: why it is a Sharpe race (M-18) [INF]

For drift μ and daily volatility σ, the gain made before a trailing drawdown D is exponential with mean m = (σ²/2μ)(e^(2μD/σ²) − 1), so P(pass) = exp(−T/m). Write x = 2μD/σ² and r = T/D: P(pass) = exp(−r·x/(e^x − 1)). At r = 2:

| x = 2μD/σ² | 0.5 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| P(pass) | 21% | 31% | 54% | 73% | 86% |

x rises as size falls (σ shrinks faster than μ), so with no clock, smaller is always safer. The clock is what binds: expected time to target ≈ T/μ. Holding P(pass) = 73% (x = 3) at Tradeify_Select_100K (D = $3,000, T = $6,000), with per-day Sharpe s = SR/√252, gives σ = D·2s/3 and days ≈ T/(sσ):

| Annual SR | Daily σ allowed (hypothetical) | Trading days to target |
|---|---|---|
| 0.85 (corrected published top-decile, [M-19](../methodology/lessons/methodology_lessons.md)) | $107 | ~1,050 (~4 years) |
| 1.00 | $126 | ~760 (~3 years) |
| 1.83 (best in-house validated edge, Aegis, M-19) | $231 | ~230 (~11 months) |
| 2.00 | $252 | ~190 (~9 months) |

These are model dollars, not strategy figures. Every firm in scope removes the explicit deadline (the M-18 rule is retired because no tier carries one, [M-18](../methodology/lessons/methodology_lessons.md)), but the clock comes back through monthly eval fees (Tradeify's carrying cost is still unrecorded, [ledger :22](../pursuits/SUBSCRIPTION_LEDGER.md)), weekly activity rules, the program's own dates (four-firm §4, 2026-11-08) and opportunity cost. So the pass rate achievable in calendar-relevant time is set by **edge × √(independent bets per day)**, not by sizing. That is M-18's finding restated for no-deadline venues: more independent setups per day beat a fatter single edge.

### 4.4 Intraday vs EOD measurement (repo figures)

The floor ratchets on EOD balance, but the breach is tested intraday at Tradeify, BluSky ("at any point") and Bulenox Option 1 (and Bulenox ratchets intraday too, C2). Same books, same seeds, EOD clock vs intraday-honest clock:

| Book · tier · size | EOD bust | Honest-clock bust | Owner |
|---|---|---|---|
| Class-S #1 · Tradeify · 1.00× (guard run, not gate-grade) | 2.50% | **32.33%** | [RESULTS_INTRADAY_W1 :19](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) |
| Live candidate book · Bulenox_100K · 1.00× | 3.51% | **26.77%** | [R1 7-tier RESULTS :218](../../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md) |
| Live candidate book · BluSky_Premium_100K · 1.00× | 4.44% | **32.26%** | R1 RESULTS :12 |
| Live candidate book · Bulenox_100K · 0.50× | 0.08% | **0.59%** | R1 RESULTS :219 |

Three readings:
1. **The effective risk budget is D minus the worst intraday excursion, not D.** At 0.50× the W1 run's deepest bar excursion was about 43% of the $3,000 trail (RESULTS_INTRADAY_W1 :19); at 1.00× it roughly doubles and eats most of the rope.
2. **Bust is strongly convex in size.** Halving size cut Bulenox honest-clock bust about 45-fold (26.77% → 0.59%). In §4.3 terms, halving size doubles x.
3. **EOD-clock figures are lower bounds**, as [`load_bearing_numbers.md` §1](../load_bearing_numbers.md#1-standing-rule--eval-bust-figures-are-eod-clock-lower-bounds) rules; the 10-02 withdrawal and the 10-06 FALSIFIED early-fail re-MC ([ADR 07-22 addenda](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-10-06--dated-re-mc-verdict-falsified--early-fail-recorded)) are this effect.

### 4.5 Locking

- **Eval without a lock (Tradeify, MFFU, presumably BluSky):** the floor trails all the way to the target. Modelling a funded-style $100 lock in the eval was optimistic: at 100K the lock engaged at EOD $103,100 against a $106,000 target, leaving the modelled floor up to $2,900 below the real one; corrected EOD bust rose 2.65% → 4.74% (Tradeify) and 2.64% → 4.25% (MFFU) (`firm_rules.py:287-299`; [ADR 07-22 §2](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#2--decision)).
- **Eval with a lock at the starting balance (FXIFY Flex, provisional):** once EOD balance reaches $154,500 the floor freezes at $150,000 [RV `firm_rules.py:589`]. Arithmetic: the last $4,500 to the $159,000 target is run against a static floor $9,000 away, so the second half of the eval is close to the static column of §4.2. Of the tiers in scope it is the only eval whose geometry improves with progress.
- **Funded (Tradeify, MFFU, Bulenox Master):** lock at start + $100; after the lock, the account is a static-floor account (§4.2 static column) whose cushion is whatever profit sits above start + $100.

### 4.6 Why M-21's risk-breadth point follows

A dollar barrier feels the book's dollar variance: in §4.3, x ∝ μ/σ². Adding a leg raises x only if it adds more drift than it adds variance. Correlation breadth is scale-free; it cannot see whose dollars own the tail. M-21's anchor: the added ORB leg's daily $-std was ~1.6× the existing two-leg book's, the composed book ~2.0×, so σ² rose ~3.9× and μ would have had to rise ~3.9× to hold x; composed bust went from ~2.65% to 38.75% on Tradeify ([M-21](../methodology/lessons/methodology_lessons.md); [Q-COMPOSE-1 closure](../briefs/closures/Q-COMPOSE-1-closure-falsified.md)). Against a trailing barrier the admission test is risk-space (covariance) breadth, and the daily-$-std ratio ρ is the seconds-cost falsifier.

---

## 5. Implications

### 5.1 What most constrains what can pass (ranked by how much it narrows the strategy space)

1. **Route and ownership rules.** Tradeify eval logic must be native (NinjaScript, Tradovate, TV-via-Tradovate); a Tradeify strategy may not run at another prop firm [R route record 10-12, 10-30]. So the multi-firm program needs **distinct strategies per firm**, and each needs its own search, so K and the DSR floor (M-19) rise with each firm added.
2. **Intraday breach against a trailing dollar floor.** Only strategies with small intraday adverse excursion relative to D survive (§4.4). Wide-stop, hold-and-hope and pyramided expressions are structurally disadvantaged.
3. **Edge × frequency.** A thin single setup cannot pass in calendar-relevant time (§4.3). Favour many independent, short-hold bets per day with low variance (information-ratio exits, M-18).
4. **Forced intraday flatten and costs.** Intraday-only holds; ~5.6 ticks RT on MNQ/MYM; stop entries pay extra slip (M-16). Mean-reversion or limit-entry designs fit the cost structure better than breakout stop entries, other things equal [INF].
5. **Account-aggregate caps and hedging bans.** One cap shared across legs; no opposite-signed legs within a product group, in any account under the same control (envelope §4a). Same-group legs must be sign-constrained, which removes the natural hedge M-21 would otherwise reward.
6. **Activity rules.** Weekly at Tradeify, MFFU; 5-trading-day at Bulenox; strategies that go quiet need the token trade (load-bearing, `load_bearing_numbers.md` §2).

### 5.2 Unverified assumptions, ranked by cost-if-wrong × likelihood ÷ cost-to-check

Scale 1–3 each (cost-to-check: 1 = read a page or a file; 2 = a re-run, an engine change, or an operator- or firm-side question; 3 = money or live trading).

| Rank | Assumption | Cost if wrong | Likelihood wrong | Cost to check | Score | First check |
|---|---|---|---|---|---|---|
| 1 | **Payout and funded-stage rules** are understood well enough to value a pass (split, caps, buffers, minimum days, lock timing). No repo owner (C5). | 3 | 2 | 1 | 6 | Read each firm's payout pages; record under Rule 17 |
| 2 | **Other firms impose no Tradeify-style native-only or exclusivity rule.** Only Tradeify has answered. | 3 | 2 | 1 | 6 | Read Bulenox/MFFU/BluSky/FXIFY ToS for bots, ownership and cross-firm clauses |
| 3 | **MFFU Rapid row** clock and consistency belong to one plan (C1). | 2 | 3 | 1 | 6 | Re-read 11994562 and 13286542; pick the plan |
| 4 | **Bulenox Option 1 modelled faithfully** (C2: intraday-high ratchet and fixed-$ vs %-of-peak). | 2 | 3 | 1 | 6 | Re-read the qualification page; then size the gap (engine change, ADR) |
| 5 | **Tradeify eval carrying cost** is small enough not to shorten the effective clock (§4.3). | 2 | 2 | 1 | 4 | Operator answer for ledger row d15 |
| 6 | **Simulator fills ≈ backtest fills** (1 tick/side, stop vs limit behaviour, auto-flatten slippage). Unmeasured. | 3 | 2 | 2 | 3 | A sim-account fill study on a demo, attended, with operator direction |
| 7 | **1 tick/side live slippage and negligible impact** at cap sizes on CME micros. Unmeasured. | 2 | 2 | 2 | 2 | Run the MNQ flow-depth PREREG |
| 8 | **BluSky has no eval lock and its NT-rail cost is ~0.95** (C3). | 1 | 2 | 1 | 2 | Re-read BluSky drawdown and commission pages |
| 9 | **FXIFY Flex lock-at-start and fees** (C10). | 1 | 2 | 1 | 2 | Byte-verified capture; fee page |
| 10 | **Growth breach is intraday like Select** (C9). | 1 | 1 | 1 | 1 | Re-read 10495897 from a Growth context |

Ties at 6 are ordered by cost-if-wrong, then by relevance to the Tradeify-first ruling (route record 10-30).

### 5.3 What this does not decide

No row edit, no re-MC, no strategy or venue choice. Rows 1–4 and 8–10 are page reads an agent can do under Rule 17 when directed; rows 5–7 need Joshua.

---

## Self-review (the one allowed pass)

Checked after drafting:
- Every [R] citation was opened this session at the cited file; line ranges are to the `main` checkout at `2bc54b2`.
- No account data, Pine, port, `effective_inputs.json` or research backtest dollar figure is quoted. §4.4 and §4.6 use bust percentages and ratios; §4.3's dollar column is labelled hypothetical model arithmetic on the venue's $3,000/$6,000 rule figures.
- No new bust figure is asserted for any strategy; §4.2–4.3 are labelled textbook models.
- Corrected in review: the G1 envelope line (49 → 81). C2 originally read as "unrecorded"; narrowed to "not found in the surfaces searched" (M-33). The MFFU conflict (C1) was rechecked against both lines.
- Residual risk: the venue facts are repo-recorded as of 2026-10-02 at the latest; firms change pages often, and no page was re-read here.
