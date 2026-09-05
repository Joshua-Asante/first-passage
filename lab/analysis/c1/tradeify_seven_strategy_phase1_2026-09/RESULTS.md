# Tradeify five-active-source Phase 1 reconciliation

**Theme:** c1

**In-flight:** yes

**Status:** ACTIVE — strict five-source Tradeify source, accounting, deadline, cap, and provenance normalization

> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.

Campaign status: `RECONCILED_EXPLORATORY`

Phase 1 evidence verdict cap: `COMPLETE`

Runner generation: `tradeify-phase1-normalization-v4`

## Continuous-contract roll disposition

D13: `ACCEPTED_UNMODELED` — contract-month and seam attribution remain unavailable, not modeled or resolved.

Operator ruling 2026-09-03; docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md §6 D13(b).

- Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.
- A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.

## D17 frozen evidence policy

D17 ruling 2026-09-03: monthly totals are `RECONSTRUCTED` from the local canonical exit-month ledger; commission evidence is `AMENDED_OUT`.

Operator ruling 2026-09-03; campaign-state §6 D17: monthly totals reconstructed from canonical exit-month ledger and independent commissions amended out. D32, campaign section 38 (2026-09-04): overlap-keyed panel drawdown comparison.

- Monthly totals are local canonical-ledger reconstructions using exit_timestamp_naive in the configured source timezone. No independent total-commission panel exists; derived commission remains non-independent inventory. Panel drawdown remains separate: non-overlap uses a one-sided lower-bound check; overlap/ties record the panel under D32.
- The tracked manifest and report hold only local-ledger hashes and aggregate reconciliation facts; per-month figures remain in gitignored local artifacts.
- Derived commission inventory is not an independent operator anchor; venue/export fee auditing is unchanged.

## Strategy inventory

| Strategy | Status | Pine pin status | Pin ref | Divergence | Export bytes | Pine bytes | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| aegis_6j1 | RECONCILED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 28364 | 52092 | 242 | 121 | $27996.05 | 0 | 0 |
| orb_mnq_recon_v7 | RECONCILED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 160557 | 23765 | 1362 | 681 | $48118.16 | 0 | 0 |
| striker_dj30_mym_pyramid_250 | RECONCILED_EXPLORATORY | UNPINNED_MODIFIED | core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/striker_dj30_v4.5_mym_pyramid_250.pine | pyramid 250% vs locked 750%; initial_capital 100000 vs research-variant pin 200000 | 47348 | 27497 | 406 | 203 | $32057.36 | 0 | 0 |
| striker_nas100_mnq_dow_wed_excluded | RECONCILED_EXPLORATORY | UNPINNED_MODIFIED | core/strategies/PORT_MANIFEST.sha256:core/strategies/candidates/striker_nas100_v1_mnq_dow_wed_excluded.pine | day-of-week set {Mon,Tue,Thu,Fri} vs locked {Mon,Tue}; initial_capital 100000 vs research-variant pin 200000 | 88221 | 33013 | 756 | 378 | $112253.42 | 0 | 0 |
| vanguard_mgc_v04 | RECONCILED_EXPLORATORY | NOT_IN_PORT_MANIFEST | None | None | 74473 | 44177 | 676 | 338 | $18709.48 | 0 | 0 |

## Pine input override digests

| Strategy | pine_input_overrides_sha256 |
|---|---|
| aegis_6j1 | 460f40fa079c00a97711d743aa0a5acee62f1c8f2cc33972b8a92b7948e42d08 |
| orb_mnq_recon_v7 | 102635acd76a7cfb42380451b71a4628610a12aa434915e6b25af76245534203 |
| striker_dj30_mym_pyramid_250 | b7369ee32889f700cd45aa7e07ae19a87cf38ca10fa9c151340face16a5d6e1a |
| striker_nas100_mnq_dow_wed_excluded | ba59219aec5d2eec111045f402abe2e2e08101bcf238a0c18d3621d4ef3a2b11 |
| vanguard_mgc_v04 | 3bacd6f11ebc804b30bc30303bf9cbb253ba256afc55e232f92d7daaf9b58861 |

## Drawdown measurement bases

| Strategy | Closed-trade DD (LOWER BOUND for non-overlapping trades) | Walk DD (LOWER BOUND (excursion-tightened) for non-overlapping trades) | TV panel DD (separate anchor) |
|---|---:|---:|---:|
| aegis_6j1 | $1298.40 | $1470.40 | $1470.40 |
| orb_mnq_recon_v7 | $5436.20 | $6062.02 | $6062.02 |
| striker_dj30_mym_pyramid_250 | $4262.66 | $4568.68 | $4568.68 |
| striker_nas100_mnq_dow_wed_excluded | $8197.80 | $8269.62 | $8269.62 |
| vanguard_mgc_v04 | $1742.24 | $1804.36 | $1804.36 |

Drawdown acceptance policy: `OVERLAP_KEYED_D32`. Evidence coverage is not operator acceptance; the placeholder grants no waiver.

Closed-interval overlap is measured from canonical entry/exit timestamps; ties count. Overlapping or tied legs are RECORDED with INFO only. Otherwise the check is one-sided: walk <= panel + 0.01; equality is coincident INFO, never MATCH.
- aegis_6j1: measured overlap or tie = False.
- orb_mnq_recon_v7: measured overlap or tie = True.
- striker_dj30_mym_pyramid_250: measured overlap or tie = True.
- striker_nas100_mnq_dow_wed_excluded: measured overlap or tie = True.
- vanguard_mgc_v04: measured overlap or tie = True.

- Excursion-tightened lower-bound basis: LOWER BOUND (excursion-tightened) for non-overlapping trades: closed <= walk <= true. Synthetic exit-order walk (exit_timestamp_naive, then exit_source_row): visit realized equity minus abs(mae_usd) before each net settlement, using the previous realized-equity peak and including realized exit declines. The walk never visits an intratrade peak (MFE), so drawdowns starting at those peaks are missed even without overlap; this is never the full path. Under overlap or timestamp ties neither field is guaranteed to bound synchronized account-equity drawdown; trade extrema are unsynchronized.

## Dropped source inventory

These exports are provenance only and are never normalized, counted, or used in ledgers or weekly results.

| Previous strategy ID | Export | Export SHA-256 | Pine | Pine SHA-256 | Pin ref | Reason |
|---|---|---|---|---|---|---|
| striker_dj30_qtxg1_swap_body_on_mym | Striker_DJ30_MNQ_Q-TXG-1_PROTOTYPE_CBOT_MINI_MYM1!_2026-09-02_82cba.csv | 2c2d893ba0daa127f1c857e81ec436b535e4e8eb85f0c728e2ba39dc6485826d | striker_dj30_v4.5_mnq_qtxg1_prototype.pine | 178a2a8e1c78e45a5142749f92284c09d286907a7e096883e1133297cb8a806d | core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/striker/striker_dj30_v4.5_mnq_qtxg1_prototype.pine | SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN |
| striker_nas100_qtxg1_swap_body_on_mnq | Striker_NAS100_MYM_QTXG1_CME_MINI_MNQ1!_2026-09-02_304f8.csv | f1e35c4ee1c9735c3ebbed99648a42034d9b3f57b53960f9e41f6e6c09b25f9c | striker_nas100_v1_mym_qtxg1_prototype.pine | 19264da29a3d9a30200600689e1950931f1abfb648e9071a232ee83fdec2756c | core/strategies/PORT_MANIFEST.sha256:core/strategies/_archive/nas/striker_nas100_v1_mym_qtxg1_prototype.pine | SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN |

## Evidence boundaries

- The source CSV/Pine bytes, row-level event/trade/weekly ledgers, and five detailed issue reports remain local and gitignored.
- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.
- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.
- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.
- CME holiday-short coverage is `COMPLETE` through D19-accepted SECONDARY venue-date membership; it is not a primary-CME upgrade, product close-time model, or exchange-session model.
- CME early-close coverage note: D19 accepts this SECONDARY venue-date membership evidence only over the declared 2022-09-01 through 2026-09-02 window, not product close-time or exchange-session modeling. The 2025-11-28 scheduled-half-day/outage classification is conservatively included; possible ad-hoc closures from 2026-05-28 through 2026-09-02 may be missing and are not conservative. The preserved secondary metadata retains 13 unresolved items and 3 sub-deadline close notes.
- Secondary provenance is retained without a primary-CME upgrade: `ops/calendars/cme_holiday_calendar_2022_2026.json` SHA-256 `2698f2688cce582b08df58516fd770fa4a71a18de04870d9c14511731ea181e9` under `cme_holiday_calendar/v1`.
- Secondary provenance note: NO CME PRIMARY SOURCE WAS FETCHED FOR ANY DATE IN THIS FILE. www.cmegroup.com, investor.cmegroup.com and every broker mirror returned 403 at the egress proxy's CONNECT layer. Every cell is reconstructed from independent third-party encodings of the CME schedule (QuantConnect Lean's market-hours database, pandas_market_calendars, exchange_calendars, vacanza/holidays, one C++ reimplementation) cross-checked against in-repo measured bar panels. Treat as WORKING-GRADE, not audit-grade. Close it out by allowlisting www.cmegroup.com and reading the per-holiday clearing advisories, or by an authenticated CME Reference Data API pull (Globex Trading Hours and Holiday Schedules). For historical dates prefer the post-hoc settlement-times PDFs over the ex-ante advisories (CME finalises holiday hours roughly two weeks out) and never conflate a settlement time with a Globex close time.
- D19 provenance acceptance: `D19` `ACCEPTED_SECONDARY` on 2026-09-03 — Operator ruling 2026-09-03; campaign-state §6 D19: secondary CME calendar provenance accepted.
- Day basis: `CME_TRADE_DATE` — Every FULL_CLOSURE row is keyed to the CME trade date, not the wall clock. Dates such as 2022-12-26 and 2023-01-02 carry roughly 360 minutes of real Globex trading on the calendar day (the 18:00-24:00 ET reopen, which belongs to the NEXT trade date) yet read FULL_CLOSURE. TradingView bar exports are stamped by WALL CLOCK. Do not join this file to an export on a date key without deciding which basis you mean.
- CME trade-date full-closure inventory is not converted into wall-date deadlines: All three product groups FULL_CLOSURE on the CME TRADE DATE. Load-bearing for the venue's >=1-trade-per-Mon-Fri-week inactivity rule. ⚠ DO NOT PUT THESE IN A WALL-CLOCK-KEYED GUARD LIST (Codex on PR #291, P2, accepted). A Pine guard keys on the bar's wall-clock year/month/day, but these rows are trade-date-keyed, and dates such as 2022-12-26 and 2023-01-02 carry real Globex bars from 18:00-24:00 ET on that wall-clock date - the reopen belonging to the NEXT trade date. Including them marks that reopened session short, which can force a flatten or block entries in a session that is not short at all. The earlier justification that they are 'inert - no bars, no effect' was WRONG. Use derived.venue_flat_dates alone for a wall-clock guard, or translate trade dates to explicit session intervals first.
- Secondary full-closure inventory (16): 2022-04-15, 2022-12-25, 2022-12-26, 2023-01-01, 2023-01-02, 2023-12-24, 2023-12-25, 2023-12-31, 2024-01-01, 2024-03-29, 2024-12-25, 2025-01-01, 2025-04-18, 2025-12-25, 2026-01-01, 2026-12-25
- Pre-12:59 market closes remain limitations, never modeled closure/no-trade rules: Dates where at least one group's early close falls BEFORE 12:59 ET. A single 12:59 ET deadline model cannot express these: the session has already ended, so no force-flat bar exists to fire on. Any strategy whose session window opens at or after these times simply never trades; any strategy that could hold into them needs a no-trade block, not a deadline.
- Sub-deadline inventory (3):
  - 2023-04-07 Good Friday (coincides with the March Employment Situation / NFP release) — equity_index=09:15, fx=11:15
  - 2025-01-09 National Day of Mourning — former President Jimmy Carter (one-off, non-recurring) — equity_index=09:30
  - 2026-04-03 Good Friday (coincides with the March Employment Situation / NFP release) — equity_index=09:15, fx=11:15
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/QuantConnect/Lean/cfc7e8ac451e384b08b697465e33016ab26c1263/Data/market-hours/market-hours-database.json
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/calendars/cme_globex_equities.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/calendars/cme_globex_energy_and_metals.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/calendars/cme_globex_fx.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/calendars/cme.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/holidays/cme.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/holidays/cme_globex.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/holidays/us.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/tests/test_exchange_calendar_cme_globex_equities.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/tests/test_exchange_calendar_cme_globex_fx.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/pandas_market_calendars/tests/test_exchange_calendar_cme_globex_energy_and_metals.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/rsheftel/pandas_market_calendars/275890784073a3a3a347e4f05f4dc986456e6a75/docs/change_log.rst
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/gerrymanoim/exchange_calendars/5de07333a58052eee033246bfe63f24e71da958f/exchange_calendars/exchange_calendar_cmes.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/gerrymanoim/exchange_calendars/5de07333a58052eee033246bfe63f24e71da958f/exchange_calendars/us_holidays.py
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/LironKruchinin/backtesting/5f4d909180aa84f1536d842939e073577a83d4f7/crates/crucible-data/src/calendar/tables/cme_globex_commodities.toml
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/LironKruchinin/backtesting/5f4d909180aa84f1536d842939e073577a83d4f7/crates/crucible-data/src/calendar/tables/cme_globex.toml
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/LironKruchinin/backtesting/5f4d909180aa84f1536d842939e073577a83d4f7/docs/SESSION_ERAS.md
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/EPOCHDevs/EpochFrame/d2545a3/src/calendar/calendars/cme_globex.cpp
- Secondary source URL (inert provenance): https://raw.githubusercontent.com/vacanza/holidays/a5aca80f6b5f91485da14d23f79b99c109fa2f2d/holidays/financial/chicago_mercantile_exchange.py
- Secondary source URL (inert provenance): https://pypi.org/project/pandas-market-calendars/
- Secondary source URL (inert provenance): https://pypi.org/project/exchange-calendars/
- Secondary source URL (inert provenance): file:///home/user/first-passage/lab/analysis/c1/tradeify_book_composition_2026-09/data/cme_equity_sessions.json
- Secondary source URL (inert provenance): file:///home/user/first-passage/lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/cme_early_close_calendar.json
- Secondary source URL (inert provenance): file:///home/user/first-passage/ops/instruments/6J.md
- Secondary source URL (inert provenance): file:///home/user/first-passage/docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md
- Secondary source URL (inert provenance): file:///home/user/first-passage/lab/research_utils/trade_reconciliation.py
- Secondary unresolved 2022-01-01: PROVENANCE — NO CME PRIMARY SOURCE WAS EVER FETCHED FOR ANY DATE IN THIS CALENDAR. Every contributing lane independently reported that www.cmegroup.com, investor.cmegroup.com and every broker mirror (ampfutures, cannontrading, mrtopstep, discounttrading, crosstrade, tradinghours, edgeclear, optimusfutures) return 403 at the egress proxy's CONNECT layer, and that the session WebSearch budget was exhausted. The initial per-year research files listed 20-40 cmegroup.com advisory-PDF URLs each under a field defined as 'URLs you actually fetched'; those URLs were surfaced or path-constructed, never opened, and several of the /tools-information/holiday-calendar/files/<year>-<holiday>-advisory.pdf patterns do not match any corroborated CME URL shape. source_urls in THIS artifact has been cut to what was demonstrably retrieved (raw.githubusercontent.com, PyPI, in-repo files). Consequence: this calendar is SECONDARY-SOURCED throughout and no entry is audit-grade against CME. Close it out by allowlisting www.cmegroup.com and reading the per-holiday clearing advisories, or by an authenticated CME Reference Data API pull (Globex Trading Hours and Holiday Schedules endpoint). For historical dates prefer the post-hoc settlement-times PDFs over the ex-ante advisories, since CME finalises holiday hours roughly two weeks out — and never conflate a settlement time with a Globex close time.
- Secondary unresolved 2022-01-17: FX (6J) STATUS ON EVERY RULE A US-HOLIDAY EARLY CLOSE, 2022-2026 — CLASS-WIDE DISPUTE. Emitted as NORMAL on the strength of: pandas_market_calendars, where every FX Monday/weekday-holiday rule is era-capped at 2021-12-31 and the class docstring reads 'Accurate 2020-2022 inclusive / TODO - Add 2023+ once known'; QuantConnect Lean, whose Future-cme-6J rows on these dates equal 6J's own normal 16:00 CT close with a normal 17:00 CT lateOpen, byte-identical across 6E/6B/6A/6C/6S; an archive-measured session calendar reporting 6E trading to 15:58 CT on MLK 2022-01-17 while ES stopped at 12:00, and 'none from 2022' for every recurring holiday 2022-2026; and broker/corroboration sources (Cannon: 'FX & Crypto: Thursday trading halt at 4:00 PM'), plus CME's own 2025 mourning press release naming FX among the normal-hours groups. AGAINST, and unreconciled: (a) ops/instruments/6J.md DEFECT LOG row F3 records a DIRECT bar-panel observation on 6J itself that on CME early-close days — naming MLK 2024-01-15 and Labor Day 2024-09-02 — 'market halts ~14:00 ET, the 16:30 trigger bar never prints', which forced a dated early-close calendar into the Aegis 6J build and was re-verified with 'zero stamps >=17:00'; that is measurement grade and it also puts the halt an hour LATER than any equity-index time; (b) one reviewer argues Lean's degenerate 16:00 CT/17:00 CT rows are unpopulated placeholder data rather than an affirmative statement of a full session, noting the five NORMAL dates are exactly the five where Lean's 6J record is degenerate; (c) undated pre-2022 CME press-release language ('CME Globex trading halts for Interest Rate and Foreign Exchange products at 12:00 noon') is retired-regime but keeps surfacing in search. Affects 2022-01-17/02-21/05-30/06-20/07-04/09-05/11-24 and every Rule A date in 2023, 2024, 2025 and 2026. Resolve against a CME per-holiday advisory before any 6J venue-legality call.
- Secondary unresolved 2022-09-05: LABOR DAY METALS (MGC) CLOSE TIME — recurs identically on 2023-09-04, 2024-09-02, 2025-09-01 and 2026-09-07. Emitted as 14:30 ET (13:30 CT). Three encodings give three answers: QuantConnect Lean says 14:30 ET, matching every sibling holiday in the same year; pandas_market_calendars says 13:00 ET (12:00 CT); an independent C++ reimplementation (EpochFrame) omits Labor Day from both buckets and would report metals NORMAL. The pmc figure is traceable to a library defect rather than a CME distinction — USLaborDayFrom2022 and USLaborDayPre2022 are both defined in holidays/cme_globex.py exactly parallel to the MLK/Presidents/Memorial/July-4/Thanksgiving pairs, but the metals calendar references neither, leaving the unbounded legacy USLaborDay (start_date 1887) in the 12:00 CT bucket; Labor Day is the ONLY holiday in that file whose From2022/Pre2022 pair is defined but unwired, and USLaborDayFrom2022 is referenced only by the crypto calendar. 14:30 ET is therefore the pattern-consistent and Lean-backed reading, but it is an inference about a library bug, not a sourced CME time. 2022-09-05 is additionally the FIRST date inside the 2022-09-01 audit window.
- Secondary unresolved 2022-11-25: RULE B (BLACK FRIDAY / CHRISTMAS EVE) METALS AND FX CLOSE TIMES — CLASS-WIDE, affects 2022-11-25, 2023-11-24, 2024-11-29, 2024-12-24, 2025-11-28, 2025-12-24, 2026-11-27 and 2026-12-24. Emitted as metals 13:45 ET (12:45 CT) and FX 13:15 ET (12:15 CT). THE TWO CORROBORATION CHANNELS DIRECTLY CONTRADICT EACH OTHER: one reports Cannon Trading and OneUp Trader publishing identical numbers for 2025-11-28 — 'Equities & Interest Rates 12:15 CT; Energy, Metals, FX 13:45 CT', i.e. metals AND FX both at 14:45 ET — while the other reports AMP publishing '12:15 p.m. CST for Equities, Interest Rates and Currencies; 12:45 p.m. CST for Energies and Metals', i.e. metals 13:45 ET and FX 13:15 ET. pandas_market_calendars supports the second reading with uncapped rules (FridayAfterThanksgiving at 12:45 CT metals; USThanksgivingFriday and ChristmasEveInOrAfter1993 at 12:15 CT FX). QuantConnect Lean is internally inconsistent across years: 2024-11-29 MGC 13:45 ET / 6J 12:15 CT and 2024-12-24 6J 12:15 CT, but 2025-11-28 MGC 14:45 ET / 6J 13:45 CT and 2025-12-24 6J 12:45 CT; it also carries NO 11/29/2024 entry at all for MYM, MGC or 6J despite that certainly being an early-close session, so its Rule B coverage has demonstrable gaps. The pmc-consistent 13:45/13:15 reading was adopted for cross-year coherence; the 14:45/14:45 reading is live and is what the initial 2026 research emitted. A 60-90 minute error either way on an MGC or 6J force-flat deadline.
- Secondary unresolved 2023-07-03: DAY-BEFORE-INDEPENDENCE-DAY METALS AND FX — recurs on 2024-07-03 and 2025-07-03. Emitted as metals 13:45 ET and FX 13:15 ET on the Rule B half-day pattern plus broker sources. AGAINST: neither pandas_market_calendars' Energy/Metals calendar nor its FX calendar contains a July-3 rule in ANY era (EpochFrame's metals calendar has none either), so both libraries return a full normal 17:00 ET close; QuantConnect Lean carries no 7/3/2025 key in earlyCloses for MGC/GC/SI/HG or for 6J/6E/6B/6A/6C/6S. One reviewer concluded both groups ran NORMAL on 2025-07-03; another concluded both cells are simply UNKNOWN. Two further complications: (a) the emitted 13:15 ET FX figure is constructed as the NYSE 13:00 ET cash half-day close plus 15 minutes, and CME FX has no NYSE-half-day linkage, so a cash-derived time is unmotivated for 6J; (b) there is an unconsidered structural fork — July 3 may follow the Independence Day HOLIDAY shape (12:00 CT = 13:00 ET) rather than the SIFMA half-day shape (12:15 CT = 13:15 ET), differing by 15 minutes on equity and up to 90 on metals. Note the pmc metals calendar also lacks a Christmas Eve rule, so its silence on eve-of-holiday metals sessions is a coverage gap, not a finding of NORMAL. The equity 13:15 ET cell on these dates is separately sound.
- Secondary unresolved 2024-11-29: BLACK FRIDAY / CHRISTMAS EVE EQUITY-INDEX CLOSE, 13:00 ET vs 13:15 ET — reviewers directly contradict each other, and the same standoff applies to 2024-12-24. Two 2024 reviewers report pandas_market_calendars' CME_Equity and CBOT_Equity classes AND exchange_calendars CMES both returning 13:00 ET via USBlackFridayInOrAfter1993 / ChristmasEveInOrAfter1993 in a 12:00 CT bucket, and observe that the CME_Equity class has no 12:15 CT bucket at all and is therefore structurally incapable of expressing 13:15 ET. A third 2024 reviewer reports pandas_market_calendars' CMEGlobexEquities class placing USThanksgivingFriday and ChristmasEveInOrAfter1993 in a 12:15 CT bucket, yielding 13:15 ET, and QuantConnect Lean gives MYM/MNQ 13:15 ET on both dates. 13:15 ET was adopted (Globex-specific pmc class + Lean + AMP/broker + the multi-year Rule B pattern + the in-repo MYM_M15 census that found a distinct minute-780 class ending 13:15 ET with no NYSE analogue), but the disagreement is between two different pmc calendar classes and has not been adjudicated against a CME advisory. exchange_calendars flattens every special close to 13:00 ET and cannot arbitrate.
- Secondary unresolved 2024-12-24: CHRISTMAS EVE METALS (MGC) STATUS AND TIME, 2024-12-24 / 2025-12-24 / 2026-12-24. Emitted as EARLY_CLOSE 13:45 ET (12:45 CT) from QuantConnect Lean plus analogy to the Black Friday metals rule. The status itself is UNCONFIRMED in the other direction: pandas_market_calendars' CMEGlobexEnergyAndMetals special_closes contains no Christmas Eve rule of any kind — its only buckets are 12:00 CT, 12:45 CT (FridayAfterThanksgiving alone) and 13:30 CT — so it returns a full normal 17:00 ET close. Reviewers agree that output is an obviously-wrong library omission rather than a finding of NORMAL (metals certainly do not trade to 17:00 ET on Christmas Eve), which means the metals cell on these dates has exactly one supporting source and no independent check. A calendar generated from pmc alone overstates the 2024-12-24 and 2025-12-24 MGC session length by roughly 3h15m.
- Secondary unresolved 2025-07-04: FRIDAY-HOLIDAY METALS AND FX SHAPE — affects 2025-07-04, 2026-06-19 and 2026-07-03, the three in-scope US holidays that fall on a Friday with no evening reopen. Two mutually exclusive models. MODEL 1 (emitted): the Friday exception — all three groups stop at 12:00 CT = 13:00 ET. Supported by QuantConnect Lean's per-symbol rows (MGC/GC 13:00 ET and 6J 12:00 CT on all three dates, versus 14:30 ET metals and 16:00 CT FX on Monday/Thursday holidays), by the same Friday shape in Lean for 7/3/2015 and 7/3/2020, and by an archive-measured session calendar stating 'on a Friday holiday CL and GC close at 12:00 CT rather than 13:30 (2025-07-04, 2026-06-19, 2026-07-03 — three for three)'. MODEL 2: no Friday exception — metals 13:30 CT = 14:30 ET and FX NORMAL, i.e. ordinary Rule A. Supported by pandas_market_calendars (USJuneteenthFrom2022 and USIndependenceDayFrom2022 both sit in the metals 13:30 CT bucket with no weekday carve-out, and its executed 2026 schedule returns 14:30 ET on both dates) and by both corroboration channels' broker-derived tables. Note Model 1's own strongest source ALSO asserts CME FX stopped observing US-holiday early closes entirely from 2022, which contradicts the FX half of the value it supplies. Up to 90 minutes on MGC and up to 4 hours on 6J. Also note the equity leg on 2025-07-04 is settled: the initial research's FULL_CLOSURE was falsified by three independent lines and corrected to EARLY_CLOSE 13:00 ET.
- Secondary unresolved 2025-11-28: UNSCHEDULED CME GLOBEX OUTAGE — the emitted EARLY_CLOSE with Rule B times is the SCHEDULED rule, which did not execute. A cooling-system failure at the CyrusOne CH1 data centre in Aurora, Illinois (later attributed to human error) took ALL of Globex down for roughly ten hours starting late on 2025-11-27; EBS reopened around 07:00 ET and CME reopened futures and options around 07:30 CT, with equity index, gold and major FX all explicitly dark. One review argues normal futures trading resumed only at the Sunday 18:00 ET open and that the row should therefore read FULL_CLOSURE or a distinct OUTAGE status; on the other reading the 2025-11-28 equity-index session ran roughly 07:30 to 12:15 CT — under five hours against a ~23-hour normal Globex day. Neither calendar library encodes the outage in any form, so any calendar generated from them reports this as an ordinary post-Thanksgiving half-day. LOAD-BEARING for the ≥1-trade-per-Mon-Fri-week venue-inactivity rule: an audit reading 2025-11-28 as merely shortened would wrongly conclude the week of Mon 2025-11-24 had a live Friday available. The Nov 28 to Sun Nov 30 no-session window is also unrecorded. Resolve the exact reopen time and the intended status convention before this date is used operationally.
- Secondary unresolved 2025-12-24: CHRISTMAS EVE FX (6J) CLOSE, 13:15 ET vs 13:45 ET, on 2025-12-24 and 2026-12-24. Emitted as 13:15 ET (12:15 CT), grouping FX with equity index, on pandas_market_calendars' uncapped ChristmasEveInOrAfter1993 rule in the FX 12:15 CT bucket (start_date 1993, days_of_week Mon-Thu) and on Lean's own 12:15 CT value for 2024-12-24. AGAINST: Lean gives 6J 12:45 CT (13:45 ET) for 2025-12-24 and 2026-12-24, grouping FX with metals instead — an unexplained year-over-year inconsistency within a single source. One reviewer also notes pmc's FX module is unmaintained past 2022 for holiday rules generally, though the Christmas Eve rule specifically is uncapped and does fire. A 30-minute error on a 6J force-flat deadline.
- Secondary unresolved 2026-01-19: 2026 FX NORMAL CELLS — the initial 2026 research's own cited counter-evidence is FALSE and has been struck, but a separate reviewer dissent remains. The initial note justified MEDIUM-to-LOW confidence on fx_status=NORMAL by citing 'pandas_market_calendars puts MLK in a 12:00 CT special-close bucket'; the rule in that bucket is USMartinLutherKingJrAfter1998Before2022 with end_date 2021-12-31, so pmc cannot fire in 2026 and in fact AGREES with NORMAL (executed pmc returns 2026 FX early closes on only 04-03, 11-27 and 12-24). That single misreading was propagated verbatim as the 'same FX caveat' to 2026-02-16, 05-25, 09-07 and 11-26 — five cells rested on one non-existent conflict. THE LIVE DISSENT: one reviewer argues Lean's 6J rows on those five dates are degenerate placeholders (earlyClose 16:00 CT AND lateOpen 17:00 CT, both byte-identical to 6J's regular session boundaries) rather than affirmative statements of a full session, notes the five NORMAL dates are exactly the five degenerate rows, and calls the table internally incoherent — no product rule closes FX at 12:00 CT on Juneteenth-Friday and July-3-Friday yet runs it to 16:00 CT on Thanksgiving Day. Same underlying question as the 2022-01-17 class dispute.
- Secondary unresolved 2026-01-05: CITED-BUT-UNUSED NATIONAL DAY OF MOURNING ADVISORY — investigated and resolved as NO 2026 CLOSURE, recorded here so it is not rediscovered as a phantom gap. The initial 2026 research listed https://www.cmegroup.com/media-room/press-releases/2025/12/30/cme_group_announcestradinghoursforusnationaldayofmourningtohonor.html in source_urls with no corresponding entry, which one reviewer flagged as a possible untabulated early-to-mid-January 2026 closure. Two other reviewers resolved it: vacanza/holidays cites that exact URL (via a 2025-07-15 archive snapshot that PREDATES the 2025-12-30 path date, proving the path is a CMS artefact) as the source for the Jimmy Carter National Day of Mourning, which it maps to 2025-01-09 — already carried in this calendar and outside 2026. Independently, exchange_calendars' USNationalDaysofMourning array ends at 2025-01-09, pandas_market_calendars' equivalent ends at 2025-01-09 (its NYSE calendar carries a dedicated JimmyCarterDeath2025 rule and returns exactly the 10 statutory holidays for 2026 with no eleventh), and an archive-measured calendar's dated-exceptions list contains only 2018-12-05 and 2025-01-09. Coverage of this check runs to 2026-05-27 (newest library build). The URL has been removed from source_urls. Residual risk: an ad-hoc closure between 2026-05-28 and 2026-09-02 is outside every source reachable in these sessions and cannot be ruled out; the only scheduled holidays in that window (06-19, 07-03) are both present.
- Secondary unresolved 2022-12-26: DAY-CONVENTION AMBIGUITY, CALENDAR-WIDE. Every FULL_CLOSURE row in this calendar is keyed to the CME TRADE DATE, not to the wall clock, but the schema carries no discriminator and the initial per-year research files never declared the convention. Concretely: 2022-12-26, 2023-01-02, 2023-12-25 and 2025-12-25 each carry ~360 minutes of real Globex trading on the calendar day (the 18:00-24:00 ET reopen belonging to the NEXT trade date), while 2022-12-25, 2023-01-01, 2023-12-24 and 2023-12-31 carry a genuine zero — yet all eight read FULL_CLOSURE. Symmetrically, 2025-12-24 (EARLY_CLOSE) and 2025-12-31 (NORMAL) are structurally identical on a wall-clock reading: both shut and neither reopened that evening. Because MYM/MNQ/MGC/6J bar exports are normally stamped by wall-clock timestamp rather than CME trade date, and because the known downstream consumer (lab/research_utils/trade_reconciliation.py, rows of {date, deadline_local}, selecting 12:59 vs 16:45 America/New_York by calendar-date membership) is calendar-date-keyed and product-group-blind, an undeclared convention is exactly the silent-failure mode this calendar exists to prevent. Recommend adding an explicit basis field, or splitting status into trade_date_status plus calendar_day_minutes, before ingestion. Related: a single date-level 12:59 ET early-close flag cannot express the three distinct per-group times this calendar records and will be over-tight for MGC and 6J on Rule A days by 60-240 minutes.
- Secondary source revisions remain provenance limits, not captured-byte proof: Codex on PR #291 (P2, accepted): unpinned master/main URLs stop identifying the data once those branches move, and several emitted cells were decided by choosing between CONFLICTING library encodings - so an unpinned reference cannot support an audit of which revision backed which cell. Every raw.githubusercontent URL above is now commit-pinned. ⚠ HONEST LIMIT: these are the branch tips resolved by `git ls-remote` at pin time on 2026-09-03, roughly an hour after the research pass read the same branches UNPINNED. They are the best available reconstruction, NOT a proven capture of the exact bytes read. A branch that moved inside that window would not be detected. To make this audit-grade rather than audit-plausible, retain hashed captures of the source files alongside this calendar, or resolve the primary CME source and retire the secondary reconstruction entirely.

## Frozen hashes

- Config: `a00bdd32687744b729510efe16704b0eb2c094d8551a7d91e87c5d6b878d9acb`
- Tradeify fee capture: `61c8957a4adfabf6b8e8c4eb984e6d9388a223145f90b0b9ca66b3dd7ca28750`
- CME calendar capture: `6eeb3b9d198eabf0a5a2115c4648f69629720a500616f38e219dff7bc57d0334`
- Independent TradingView anchors: `22d6ab6e7356b7b3052177b6385783f850a8a43f7a8cc9abd0146e6b0cf69376`
- Canonical events: `3a6b754ec145db0e5c09ce18413d7d42d60fa1ce8ac034bd6d6878ae4251d3ac`
- Canonical trades: `7e650599241b8150d0ee31ea04a7406c200e1f009c9530908a9644e56bed765a`
- Weekly exit blocks: `d0b3e5ab840ef0a88c9f7b4b2c7254b3774142b85a55a9cfaeaa04fa5fe7934a`
- Detail report aegis_6j1: `42a784e3b3ccd79e4af82a80a08ad4f40b8f4e690cc3a0a45cc74635b700db2f`
- Detail report orb_mnq_recon_v7: `31c09388bf94bfcf3b333d5e11aa5df4504a2a75bbff901342d1a0ce725390f2`
- Detail report striker_dj30_mym_pyramid_250: `09796afb37da8114bef200ce02d46b47d37131c3534914f3a642dc81334e335f`
- Detail report striker_nas100_mnq_dow_wed_excluded: `87fba3c502e696432f60d094b43209a1bb4ef0cf7e5c0b8167717a6f8c797d3a`
- Detail report vanguard_mgc_v04: `57e5ed7e06815e14725b90f05a96d01b5aac4f524df3d2695a2079be247ed537`
- Local monthly reconciliation aegis_6j1: `5242591bbb40a93480e5356011f31a4d6fd0575d1d0f1f73ee1236926c343ca1`
- Local monthly reconciliation orb_mnq_recon_v7: `632382c8bffea9644486b961e706d5f94a7f782235ecc4b7d5b9bab29070e2ad`
- Local monthly reconciliation striker_dj30_mym_pyramid_250: `bd34b13a72d6c771cdbb654d3798bb53307f60ac144e1553141efe5df4303070`
- Local monthly reconciliation striker_nas100_mnq_dow_wed_excluded: `7163605aeddd8953d73e44b46162ec051d4d45587c508701079acbd4a6e7568a`
- Local monthly reconciliation vanguard_mgc_v04: `5b1f2a5872aac49ef4988b423bc3d042232c16f5056c1816bddc4eeebde56acb`

## Issues by strategy

### aegis_6j1

- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `WARNING` `PINE_EXPORT_COMMISSION_MISMATCH` × 1
- `WARNING` `PINE_VENUE_COMMISSION_MISMATCH` × 1
- `INFO` `TV_DRAWDOWN_COINCIDENT` × 1

### orb_mnq_recon_v7

- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `INFO` `TV_DRAWDOWN_RECORDED` × 1

### striker_dj30_mym_pyramid_250

- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `INFO` `TV_DRAWDOWN_RECORDED` × 1

### striker_nas100_mnq_dow_wed_excluded

- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `INFO` `TV_DRAWDOWN_RECORDED` × 1

### vanguard_mgc_v04

- `WARNING` `CONTINUOUS_CONTRACT_ROLL_UNRESOLVED` × 1
- `INFO` `TV_DRAWDOWN_RECORDED` × 1

## Independent TradingView summary reconciliation

G1.4 coverage: `COMPLETE`. All five pinned 2026-09-03 runs have independent TradingView Key-stats panels recorded in campaign section 18a. Historical capital-delta attribution is UNESTABLISHED under D30; older panels are not rebound to these exports.

The panel drawdown is a separate anchor, never an equality target for the exit-order walk. Only a non-overlapping walk exceeding the panel by more than 0.01 blocks; overlap and timestamp ties are recorded with INFO. No DD row is a MATCH; no series is repaired. DD rows leave Observed unset; their Difference is walk minus panel, as shown separately above.

### aegis_6j1

TradingView Key stats panel captured 2026-09-04 for the pinned 2026-09-03 run: Sep 1, 2022 - Sep 2, 2026, Deep, 100K USD, Default detalization, Script execution 1; campaign-state section 18a.

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 121 | 121 | 0 | 0 | MATCH |
| net_pnl_usd | 27996.05 | 27996.05 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 63.6363636400 | 63.64 | -0.0036363600 | 0.01 | MATCH |
| profit_factor | 3.4216569931 | 3.422 | -0.0003430069 | 0.01 | MATCH |
| tv_panel_max_drawdown_usd | None | 1470.40 | 0.00 | 0.01 | COINCIDENT |

### orb_mnq_recon_v7

TradingView Key stats panel captured 2026-09-04 for the pinned 2026-09-03 run: Sep 1, 2022 - Sep 2, 2026, Deep, 100K USD, Default detalization, Script execution 1; campaign-state section 18a.

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 681 | 681 | 0 | 0 | MATCH |
| net_pnl_usd | 48118.16 | 48118.16 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 57.2687224700 | 57.27 | -0.0012775300 | 0.01 | MATCH |
| profit_factor | 1.4452530618 | 1.445 | 0.0002530618 | 0.01 | MATCH |
| tv_panel_max_drawdown_usd | None | 6062.02 | 0.00 | 0.01 | RECORDED |

### striker_dj30_mym_pyramid_250

TradingView Key stats panel captured 2026-09-04 for the pinned 2026-09-03 run: Sep 1, 2022 - Sep 2, 2026, Deep, 100K USD, Default detalization, Script execution 2; campaign-state section 18a.

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 203 | 203 | 0 | 0 | MATCH |
| net_pnl_usd | 32057.36 | 32057.36 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 42.3645320200 | 42.36 | 0.0045320200 | 0.01 | MATCH |
| profit_factor | 1.6925876219 | 1.693 | -0.0004123781 | 0.01 | MATCH |
| tv_panel_max_drawdown_usd | None | 4568.68 | 0.00 | 0.01 | RECORDED |

### striker_nas100_mnq_dow_wed_excluded

TradingView Key stats panel captured 2026-09-04 for the pinned 2026-09-03 run: Sep 1, 2022 - Sep 2, 2026, Deep, 100K USD, Default detalization, Script execution 2; campaign-state section 18a.

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 378 | 378 | 0 | 0 | MATCH |
| net_pnl_usd | 112253.42 | 112253.42 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 54.4973545000 | 54.50 | -0.0026455000 | 0.01 | MATCH |
| profit_factor | 2.6038264920 | 2.604 | -0.0001735080 | 0.01 | MATCH |
| tv_panel_max_drawdown_usd | None | 8269.62 | 0.00 | 0.01 | RECORDED |

### vanguard_mgc_v04

TradingView Key stats panel captured 2026-09-04 for the pinned 2026-09-03 run: Sep 1, 2022 - Sep 2, 2026, Deep, 100K USD, Default detalization, Script execution 2; campaign-state section 18a.

| Metric | Observed | Anchor | Difference | Tolerance | Status |
|---|---|---|---|---|---|
| trade_count | 338 | 338 | 0 | 0 | MATCH |
| net_pnl_usd | 18709.48 | 18709.48 | 0.00 | 0.01 | MATCH |
| win_rate_pct | 50.5917159800 | 50.59 | 0.0017159800 | 0.01 | MATCH |
| profit_factor | 1.9275251098 | 1.928 | -0.0004748902 | 0.01 | MATCH |
| tv_panel_max_drawdown_usd | None | 1804.36 | 0.00 | 0.01 | RECORDED |

## Reproduce

Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.
