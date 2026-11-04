# Instrument export ranking: which new contracts to export next — DRAFT

**Status:** DRAFT. It ranks; it decides nothing. Exports are operator acts (Rules 18, 19); admitting a symbol and extending the calendar each need their own landing and acceptance.
**Date:** 2026-11-04 · **Author:** Claude Code (cloud) · **Base:** `main` at `9509cf1`.
**Authority:** Joshua, 2026-11-04, verbatim: "yes to all four, spawn the sessions", answering a proposal to "have an agent rank new instruments for you to export".
**Budget (Rule 2):** one dig pass, ≤3 review rounds, $0, **K = 0** (no market data read; ranking from records and public contract facts only).
**Owner of the budget rules:** [generation-phase note](2026-11-01-generation-phase-strengthening-DRAFT.md) §9.2 (D7), §10.1 (D9), §11; this note applies them and changes none.

## Recommendation

**Decision (Joshua, 2026-11-04, verbatim, relayed by the coordinator): "go with M6A and MES".** M6A and MES are chosen for export. ZC is deferred until a grains strategy justifies a separate calendar file. SIL and 6C are not taken now.

Export these five now, 15m, BAR EXPORT v0.2, full depth (first available bar to the latest bar), using the §9.3 steps 1–3 landing as for M6E:

| # | TradingView symbol | Export file stem (existing style) | Export range | Calendar extension needed | Lifetime builder looks (D7 + D9) |
|---|---|---|---|---|---|
| 1 | `CME_MINI:M6A1!` | `CME_MINI_M6A1!` | first bar (contract trades from 2009-03-23) → latest | none (FX column lists 6A) | 4 |
| 2 | `CBOT:ZC1!` | `CBOT_ZC1!` | first bar TradingView returns → latest | **new grains status column or file** (see §3) | 4, after the extension |
| 3 | `CME_MINI:MES1!` | `CME_MINI_MES1!` | first bar (contract trades from 2019-05-06) → latest | none | 2 |
| 4 | `COMEX_MINI:SIL1!` | `COMEX_MINI_SIL1!` | first bar TradingView returns → latest | none (metals column lists SI) [INF: SIL follows SI's hours] | 4 if the export reaches 2016-01 |
| 5 | `CME:6C1!` | `CME_6C1!` | first bar TradingView returns → latest | none (FX column lists 6C) | 4 |

Symbol prefixes are TradingView's `source_id` from its public symbol search (read 2026-11-04). They match the admitted files' prefixes for MNQ (`CME_MINI`), MGC (`COMEX_MINI`), MCL (`NYMEX`) and 6J (`CME`) in [`SHA256SUMS`](../../core/data/tv_exports/cme/SHA256SUMS). The MCL file stem `NYMEX_MCL1` drops the `!`; the others keep it.

**If only three:** M6A, ZC, MES. M6A is the strongest on every axis but distinctness from M6E. ZC opens a product group no book touches, at the cost of a calendar extension. MES is the cheapest landing and gives the Tradeify scaling family new looks.

Each new symbol also needs, at landing and not before (create-on-touch, as §9.3 step 4 lists for M6E): a `PRICE_COL_BY_INSTRUMENT` entry, an `INSTRUMENT_SPECS` row with a fresh Rule 17 CME quote, an instrument ledger (M6A, MES exist; ZC, SIL, 6C are new) and a regenerated `PROFILES.md`. Every builder card on any of them reads the ledger first and appends a disposition (Rule 27).

## 1. Ranked table

Firm letters: **T** Tradeify, **B** Bulenox, **M** MFFU, **S** BluSky, **F** FXIFY. Costs are round trip (RT), all-in, as each firm publishes them.

| Rank | Candidate | Firms offering it | Costs (RT) | History start → looks | Calendar | Sizing (tick; 20-tick illustrative stop, 1 contract, vs $3,000 Select 100K DD) | Distinctness | Priors (advisory, Rule 26) |
|---|---|---|---|---|---|---|---|---|
| 1 | **M6A** micro AUD/USD | T, B, M; not on S's page; F unknown | T $1.60; B $1.00; M $1.44 | 2009-03-23 → calendar binds at 2016 → **4** | covered | $1.00; $20 (0.7%) | Currencies group with 6J and M6E: Tradeify's opposing-position rule binds across them | Stage-1 Currencies SURVIVOR (`FLAG-COSTBIND`); DL-2 PDH/PDL **ABANDONMENT**, that construction retired on M6A ([ledger](../../ops/instruments/M6A.md)); Q-TNEC-ENV-1 envelope non-empty |
| 2 | **ZC** corn (full-size; ZS alternate) | ZC: T, M; ZS: T, B, M; neither on S's page | ZC: T $7.20, M $6.12. ZS: T $15.20, B $5.72, M $6.12 | listed long before 2016 [INF; first bar settles it] → **4** | **not covered** | $12.50; $250 (8.3%) | **Grains group: shared with no existing family**, so no opposing-position constraint against any current book | none: no ledger, no K spent |
| 3 | **MES** micro S&P 500 | T, B, M, S; F unknown | T $1.82; B $1.22; M $1.90 | 2019-05-06 → **2** | covered | $1.25; $25 (0.8%) | lowest: Equity Index group with MNQ, MYM, M2K; same family as the Tradeify ORB book | [ledger](../../ops/instruments/MES.md): re-entered, "not elected"; index-intraday domain bar; index raised bar |
| 4 | **SIL** micro silver (1,000 oz) | M, S, F; **not T** ("MGC is the only supported micro metal"); not B (lists SI only) | M $2.84 | 1,000-oz contract announced for June 2013 (secondary, below) → **4** if TV reaches 2016 | covered | $5.00; $100 (3.3%) | Metals group with MGC; gold and silver co-move more than either does with equities [3P] | none in repo beyond MGC.md's fix-window family note |
| 5 | **6C** Canadian dollar (full-size; no micro at any firm) | T, B, M; not on S's page | T $6.20; B $4.72; M $5.12 | listed long before 2016 [INF] → **4** | covered | $5.00; $100 (3.3%) | Currencies group with 6J, M6E, M6A | none |
| 6 | MBT micro bitcoin | B, M (MFFU "treated as a mini contract"), F (counts 1:1); **not T** (no crypto); not on S's page | B $5.52; M $3.50 | 2021 [unverified date] → about 1 | not covered (crypto session) | coarse [not computed] | new asset class | none |
| 7 | 6B / 6S full-size; M6B micro | 6B, 6S: T, B, M. M6B: B only | T 6B $6.20, 6S $10.20; B $4.72; M $5.12 | before 2016 → 4 | covered | 6B, 6S $6.25 tick | Currencies group | M6B ledger: no K, no candidate; "venue_tradable: false" at Tradeify |
| 8 | FDXM mini-DAX (Eurex) | T only (Tradovate accounts) | not read | not checked | **not covered** (Eurex calendar) | not computed | **Equity Index group** at Tradeify, despite the European session | §8.3 feed-gap #3 |
| — | MHG micro copper | S only; **not T** (not listed), not B, not M (HG restricted) | — | 2022-05-02 → **0** (K = 1 floor 0.95 > 0.89 at 756 development sessions; reaches one look around 2027-04) | metals column lists HG | $1.25 | distinct from gold [3P] | none |
| — | MNG micro Henry Hub | no checked firm | — | — | — | — | — | NG ledger: event-window DEAD |
| — | ZN / ZB / ZF | S lists ZN; not T, not M; not B | — | — | not covered | — | — | treasury-complex tail exhaustion bar; three DEAD cells ([ZN.md](../../ops/instruments/ZN.md)) |
| — | QM / QG | T, B, M (QG restricted at M) | — | — | — | — | Energy group with MCL; adds little beyond MCL | NG DEAD |

**Why this order.** The score is new lifetime looks × firms offering it × distinctness, with a calendar extension and coarse sizing counted against. M6A wins on looks, firms, cost and sizing. ZC is the only candidate that opens a product group with no existing family, so it is the cleanest seed for a separate firm (§10.2), but it needs a calendar extension and is full-size only. MES is low on distinctness but has the widest firm coverage and lands with no extension. SIL is a second metal for the non-Tradeify firms (MFFU, BluSky, FXIFY), where §10.2 already maps metals. 6C is a coarser second FX contract. MHG would be distinct, but it has no look under D7 today.

## 2. History depth and looks

Looks follow the §8.1 closed form with D9's fixed 378-session holdout and D7's reach test (floor ≤ 0.89 at banked K), development sessions = 252 × years − 378. I reproduced `lab/builder/gates.reachability()` with the standard library, as §8.1 prescribes, because this cloud container has no operations environment for the `fp` launcher (`fp: Operations virtual environment missing`). It reproduces §11's 4 / 2 / 1:

| Usable window | Development sessions | Looks | Floor at that K / P(pass) at true 0.89 |
|---|---|---|---|
| 2016-01 → 2026-11 (calendar binds) | 2,354 | 4 | 0.88 / 0.51 |
| 2019-05 → 2026-11 (MES) | 1,512 | 2 | 0.88 / 0.51 |
| 2021-07 → 2026-11 (MCL, reference) | 958 | 1 | 0.84 / 0.54 |
| 2022-05 → 2026-11 (MHG) | 756 | 0 | K = 1: 0.95 / 0.46 |

Pre-2016 depth would raise the budgets for M6A, ZC, SIL and 6C, but it needs a primary-sourced calendar extension first (§11).

**Launch-date sources.**
- M6A: CME E-micro FX launch, trade date 2009-03-23 ([CME release, 2009-02-18](https://www.cmegroup.com/media-room/press-releases/2009/2/18/cme_group_to_launchforexe-microcontracts.html); [CME clearing advisory NPadv09-04](https://www.cmegroup.com/tools-information/lookups/advisories/clearing/files/NPadv09-04.pdf)). The M6E export's first bar, 2009-03-23 (§11), is consistent.
- MES: 2019-05-06 (§9.1's CME citations).
- SIL: CME announced a physically delivered 1,000-oz silver contract for June 2013 ([CME release, 2013-04-18](https://www.cmegroup.com/media-room/press-releases/2013/4/18/cme_group_announcesnewphysicallydelivered1000ozsilverfuturescont.html)). That it is the same product TradingView lists as `SIL1!` is **unverified**; the export's first bar settles the depth.
- MHG: listed 2022-05-02 ([CME release, 2022-04-05](https://www.cmegroup.com/media-room/press-releases/2022/4/05/cme_group_to_launchmicrocopperfuturesonmay2.html)).
- ZC, 6C: decades older than the calendar; not looked up, since the calendar binds.

These are search-result readings dated 2026-11-04 (cmegroup.com itself is unreachable from this egress, per the [calendars README](../../ops/calendars/README.md)). They are Rule 17 quotes to re-read when each symbol is encoded.

## 3. Calendar coverage

The admitted [2016–2026 calendar](../../ops/calendars/cme_holiday_calendar_2016_2026.json) has three status columns: `equity_index` (ES/MES, NQ/MNQ, YM/MYM), `metals` (GC/MGC, SI, HG) and `fx` (6J, 6E, 6B, 6A, 6C, 6S). M6A, MES, SIL and 6C fall inside them.

**Grains need an extension, and its shape matters.** The builder closes a date when **any** recorded `*_status` is not `NORMAL` (`lab/builder/data.py` `_entry_closed`, option B). The closure is account-level by design, because Tradeify's 12:59 ET deadline is account-wide ([calendars README](../../ops/calendars/README.md), "One list per account"). So adding a `grains_status` column to the shared file would also close grains-only early-close dates for every existing instrument, MNQ included; registrations pinned to the current file by hash would keep the old closed set, so the two would diverge. Two options, for the calendar owner and Joshua:
- a separate grains-scoped calendar file under the same `cme_holiday_calendar/v1` schema, which a grains run pins in place of, or alongside, the current one; or
- a builder change that selects groups per instrument (an engine change with its own review).

Either needs the same operator acceptance as #1045 (date membership), and a sourced CBOT agricultural holiday and early-close schedule for 2016–2026. Grains also trade a day session and a separate overnight session with a daily break, so the builder's `INSTRUMENTS` session model (`lab/builder/instruments.py`) needs checking before a grains card is registered [INF].

The calendar has no energy column either; MCL already runs on the union (§9.3). MBT would need a crypto-session calendar; FDXM a Eurex one.

## 4. Firm availability: sources

| Firm | Source, read 2026-11-04 | Label |
|---|---|---|
| Tradeify products | [10468222](https://intercom.help/tradeify/en/articles/10468222) (Intercom mirror): CME micros "MES, MNQ, M2K … M6E, M6A"; CBOT "YM, MYM, ZC, ZW, ZS, ZL, ZM"; COMEX "GC, SI, HG, QO, MGC"; "Micro Silver (SIL) is not supported. MGC is the only supported micro metal."; "If a root symbol is not on this list, it is not supported"; no cryptocurrency derivatives | [W-x] |
| Tradeify costs | [10468315](https://intercom.help/tradeify/en/articles/10468315): M6A $1.60, MES $1.82, 6C $6.20, 6B $6.20, 6S $10.20, ZC $7.20, ZS $15.20, ZW $17.20 RT. M6A and MES agree with [`core/firm_rules.py`](../../core/firm_rules.py) (Tradeify block) | [W-x] |
| Bulenox | [Rates PDF](https://bulenox.com/legal/Bulenox-Rates.pdf) "Updated Aug/11/2026" (the same date the register cites): M6A/M6B/M6E 0.50, MES 0.61, 6B/6C/6S 2.36, ZS/ZW 2.86, MBT 2.76 per side; no SIL, MHG, MNG or ZC row | [W-x] |
| MFFU | [9735811](https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list), "August 24, 2026": M6A $1.44, MES $1.90, SIL $2.84, 6C $5.12, ZC/ZS/ZW $6.12, MBT $3.50 RT; SI, HG, PL, NG, QG "currently restricted from trading"; metals micros capped 3/5/10/15 contracts (25K–150K); "MBT is treated as a mini contract" | [W-x] |
| BluSky | [17115915](https://help.blusky.pro/en/articles/17115915-markets-symbols-commissions), 2026-09-23: lists NQ, MNQ, ES, MES, YM, MYM, RTY, M2K, CL, MCL, NG, GC, MGC, SI, SIL, HG, MHG, 6E, ZN. The page says account availability "may differ", so absence is not proof of unavailability. **M6E is not on it** | [W-x] |
| FXIFY | [rule sheet](2026-10-17-fxify-futures-flex-150k-evaluation-rule-sheet.md): position limit counts "MBT/MET 1:1, SIL 1:5"; no product list read | [R] |

[W-x] quotes were extracted by a summarising fetch tool, so they are not byte-verified (M-32), as in the [venue-fact register](2026-11-01-prop-firm-venue-fact-register-DRAFT.md). Re-read by hand before encoding any of them (Rule 17). None is accepted into an owner record here.

**Finding for D10 ([§10.2](2026-11-01-generation-phase-strengthening-DRAFT.md#102-d10-which-family-seeds-which-firm)).** BluSky's page lists 6E but not M6E. The proposed mapping puts M6E at MFFU, not BluSky, so it is unaffected, but any BluSky FX seed would be full-size 6E. M6A gives Bulenox's "second FX" slot a micro contract at $0.50/side, where 6J is full-size only.

## 5. Distinctness

The binding test is Tradeify's product groups ([envelope §4a](../../ops/prop_envelope_default.md)): opposing directions within a group are banned in one account or across accounts. M6A and 6C share the Currencies group with 6J and M6E; MES shares Equity Index with MNQ, MYM and M2K; SIL shares Metals with MGC. **ZC is the only ranked candidate in a group with no existing family.**

Return correlation is a weaker, secondary signal here, and the public figures found are practitioner tables, not studies [3P]: gold and silver correlate more with each other than either does with the S&P 500 ([tastylive](https://www.tastylive.com/news-insights/gold-price-overall-market-correlation-how-it-works)); EUR/USD and AUD/USD correlate positively at daily and longer horizons, with large variation by window ([OANDA-style table](https://www.scribd.com/document/481992305/Currensee-Correlation-OANDA)). Per §8.1 lever 4, pooling helps only across asset classes, so M6A is weak as a pooled leg with M6E, and ZC is strong.

**Honest K (Rule 23).** `k_scope: instrument` gives each new symbol its own bank. A card that repeats a mechanism already run on a correlated sibling (an ORB on MES after MNQ; a continuation on M6A after M6E) is still one more look at the same hypothesis, and the registration should say so.

## 6. Not done

- No market data read; no tick-size, multiplier or price was taken from anything but the public contract facts and the ledgers cited.
- FXIFY's product list and costs were not read; MBT's and FDXM's launch dates and FDXM's TradingView data entitlement were not checked.
- Tradeify's product article shows no exact modified date ("Updated over 2 weeks ago").
