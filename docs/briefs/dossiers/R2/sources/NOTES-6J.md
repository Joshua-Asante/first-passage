# NOTES-6J — R2 worker notes (2026-11-04, K = 0, no market data read; no Pine, ports or effective_inputs read)

## Ranking
1. **r2-6j-tokyofix** (6J × `tokyo-fix-usd-demand` NEW × Bulenox).
   - Only 6J cell with a named payer (path 1a): importers and real-side customers filling at the bank Tokyo fix, with gotobi-date settlement custom.
   - Daily event, so Req 4 is reachable.
   - Has a target-pair cohort with t-stats (KMW Table I, JPY, 1999–2019).
   - The post-fix limb (H2) clears power 0.50 at the 58% haircut: 0.63.
   - Weaknesses:
     - Cost margin is thin to negative. At the 1 tick/side model the effect is about consumed.
     - The pre-fix limb fails power (0.37).
     - The gotobi limb is UNSCREENABLE.
     - It re-enters a Q-INVENTORY-1 dead class. That kill basis (4× cost law) was deleted 2026-10-24, but its "not a re-citation under a different paper" bar still reads against it.
     - Two-sided exposure creates a cross-firm hedging hazard against any Tradeify Currencies book.
2. **r2-6j-psbc** (6J × `prior-session-breakout-continuation` × Bulenox).
   - Supply-map #5, but:
     - no payer (path 1b);
     - 1b limb (iv) not met (documented decay, and intraday JPY costs eliminate gross returns);
     - δ UNSCREENABLE;
     - the only prior use of the id (M6A DL-2) was abandoned;
     - its stop-entry family shares 6J J16's failure shape.
   - Kept as the second cell because the brief asks for two distinct ones and the supply map named it, not on merit.

## Sources opened, with verbatim support
1. **Krohn, Mueller, Whelan — "Foreign Exchange Fixings and Returns Around the Clock", Bank of Canada Staff Working Paper 2021-48 (last updated 2021-10-06).** https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, accessed 2026-11-04. Downloaded PDF sha256 `807fdb20dac0010b3b41f3f08c17b9bf7a233291fea449cd64cd86ad54fa0f46` (scratchpad `dl_kmw/`). The J. Finance 2024 version was not opened.
   - Note 1: "Data is daily and covers the sample period from January 1999 to December 2019 (5,264 daily observations)." Pre-T window "starts at 5:00 p.m. ET until the Tokyo fix at [time elided]"; post-T "until [time elided]".
   - Table I row "JPY -4.06 7.94 -2.61 1.56 -2.92 -0.08 / (-5.87) (8.22) (-2.37) (1.42) (-3.03) (-0.04)". Columns: pre-T, post-T, pre-E, E-L, post-L, CTC; "annualized average returns … t-statistics are reported in parentheses".
   - Text: "The reversal after the Tokyo fix is equally statistically significant for all currencies in our sample, with the yen and the Norwegian krone exhibiting the highest magnitudes, which are 7.94% and 7.44% per annum".
   - Table II row "14-19 -1.59 2.08 … (-2.64) (2.25)" (dollar portfolio).
   - Table III row "CME Futures -4.06 5.61 … (-8.93) (10.00)": "Dollar portfolio returns from CME futures are computed from the EUR, GBP and JPY"; CME sample "January 2006 to December 2019".
   - Table VII Panel A JPY: "Fraction positive 0.57 … Mean 12.00 … t-stat (10.12) … Std. Dev. 5.42".
   - Table IX Panel A JPY pre+post: "AvgBA,100% -6.54", "AvgBA,50% 2.73", "AvgBA,0% 12.00".
   - Decay: "returns around the Tokyo fix have been around 5% or below since 2013, and the first year with a negative reversal return was recorded in 2018."
   - Fix time: "Tokyo at [time elided] which is [time elided]" ET; "Japan doesn't follow daylight savings time".
   - Arithmetic: δ/σ = t/√5264 (√5264 = 72.55).
     - pre-T: 5.87/72.55 = 0.0809
     - post-T: 8.22/72.55 = 0.1133
     - reversal: 10.12/72.55 = 0.1395
     - Haircut ×0.42 gives 0.0340 / 0.0476 / 0.0586.
     - Assumption: the t-stats are per-day, so t/√N is the per-day standardized mean. KMW do not say whether Table I t-stats are NW-adjusted. If they are, this reading is still a per-day ratio up to the HAC correction.
2. **Ito & Yamada — "Puzzles in the Forex Tokyo 'Fixing': Order Imbalances and Biased Pricing by Banks", Columbia CJEB WP 352, June 2016.** Published J. Int. Econ. 109 (2017) 214–234 (published version not opened). https://business.columbia.edu/sites/default/files-efs/imce-uploads/Research/Research_Papers/WP_352.Ito-Yamada.Tokyo_Fixing_Puzzles.pdf, accessed 2026-11-04 (scratchpad `dl_itoyamada/`).
   - "the buying orders of foreign currency (US dollar and Euro) by importers regularly exceed the selling orders by exporters. It is commonly known that the USD tends to appreciate vis-à-vis the yen around the fixing time. This situation is more evident when large amounts of payments are due, typically on the days of the 5th, 10th, 15th, 20th, 25th, and 30th".
   - "if the switching time is at the moment of the Tokyo fixing ([time elided]), the average return becomes 1.8bp. This return is slightly above the transaction cost from the bid-ask spread."
   - "the return becomes particularly high at 5th and 10th days (except for the days close to the end of month)". Figure only, no number.
   - Table 5: "5th and 10th days 1.73e-05 ** … 7.82e-05 ***". The dependent variable is the fix-minus-market gap, not a tradable return.
   - "While return reversals are reported at the London fixing … they are not found at the Tokyo fixing (Table 4)". This is at the spike/1-minute scale and is not a contradiction of KMW's multi-hour windows, but the reviewer should weigh it.
3. **Bessho, Sugimoto, Suzuki — "Forex Trading Strategy That Might Be Executed Due to the Popularity of Gotobi Anomaly", arXiv 2301.13204 (v1 2023-01-29).** https://arxiv.org/abs/2301.13204 and /html/2301.13204v1, accessed 2026-11-04.
   - Abstract: "Our previous research has confirmed that the USD/JPY rate tends to rise toward [time elided] every morning in the Gotobi days, which are divisible by five."
   - Body, as extracted by the fetch tool (model-summarized, so re-verify; M-32): EBS data 2018-01-01..2020-12-31. Gotobi strategy "N=185, PF=1.46, PR=0.94, W=0.60"; non-Gotobi "N=185, PF=0.51". No mean, σ or t is reported, so no δ/σ.
   - Prior work it cites: Akiyama, Sugimoto, Sakemoto, Suzuki (2021), JAFEE Journal 19, 57–78 (in Japanese). **Not opened.**
4. **McLean & Pontiff (2016), "Does Academic Research Destroy Stock Return Predictability?", J. Finance 71(1) 5–32.** PDF https://Www.Gwern.net/doc/economics/2016-mclean.pdf, accessed 2026-11-04 (scratchpad `dl_mp/`). Abstract: "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication."
5. **Neely & Weller, "Lessons from the Evolution of Foreign Exchange Trading Strategies", FRB St. Louis WP 2011-021D (revised April 2013).** https://files.stlouisfed.org/files/htdocs/wp/2011/2011-021.pdf, accessed 2026-11-04 (scratchpad `dl_nw/`).
   - Olson (2004) "finds that returns declined from the 1970s to about zero in the 1990s".
   - "Neely and Weller (2003) found that realistic transaction costs eliminated very high gross excess returns in the case of four highly liquid currencies, the German mark, the Japanese yen, the British pound and the Swiss franc."
6. econpapers listing of arXiv 2301.13204 (https://econpapers.repec.org/paper/arxpapers/2301.13204.htm): abstract only. u-tokyo repository record 42697: HTTP 503, not read. Wiley JF page: 403.

Search-result leads **not used as evidence** (practitioner or third-party, M-32): forexdetox Substack, alphainacademia "20-Year USD/JPY Backtest" (~1,175 windows, ~4.5 pips gross), ForexFactory 7-year tick test (OOS degradation), EBC, investinglive (formerly ForexLive) "backfitted narrative" commentary 2023-10-05. They are worth a reviewer's glance as decay/skeptic leads only.

## Prior-consult outputs (full pastes)
- `cell 6J tokyo-fix-gotobi-flow` → `FATAL: unknown mechanism 'tokyo-fix-gotobi-flow'. Declare it NEW in MECHANISMS.md.` exit=2.
- `cell 6J tokyo-fix-usd-demand` → same FATAL, exit=2.
- `cell 6J event-window-reversal` → exit=0 (pasted in r2-6j-tokyofix).
- `cell 6J turn-of-month` → exit=0:
```text
=== 6J x turn-of-month ===
ledger: ops/instruments/6J.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to 6J): No tradeable turn-of-month premium on SPX500's canonical Pepperstone feed (2017–2026, n=113 turns) — the existence battery is hard-absent (Welch t=0.64, label-perm p=0.25), the effect is entirely COVID-concentrated, and the halves sign-reverse. [SPX500.md F5](SPX500.md)
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Aegis-to-6J venue-transfer retains measured panel evidence (n=129, PF 2.318, ~50% venue haircut vs canonical) - parked as a scale-path decision, not falsified by the evidence. [#J1]
prior: The venue structurally throttles Aegis sizing: the 12-contract cap binds on 76% of trades, realizing effective risk ~0.5-1.0% against the locked 1.5% target. [#J5]
exit=0
```
- `cell 6J prior-session-breakout-continuation` → exit=0 (pasted in r2-6j-psbc).

## Prior entries checked (fix or gotobi)
- `ops/instruments/6J.md`: no fix or gotobi entry (grep "gotobi|fixing|tokyo" returns nothing relevant). J16 ORB and the Aegis track only.
- `docs/rejected_candidates.md`: no gotobi entry. Fix-related entries:
  - Custodian EURUSD month-end (shelved 2026-06-10)
  - fx-fixing-reversal-session-mr EURUSD (2026-06-22; bar names "a different fix (Tokyo/Frankfurt)")
  - Q-INVENTORY-1 (2026-07-17; "FX fixing-window 6E/6J drift (Krohn-Mueller-Whelan)", cost-wall at 4× under the deleted Req 5)
- Discrepancy to flag: Q-INVENTORY-1 cites that row as "n=2515, 2009–2018 … EUR pre-Europe window published net +5.53%/yr, SR 0.99". These figures **do not match** the KMW working paper I opened (5,264 obs, 1999–2019; Table IX EUR pre-ECB at 50% BA is 5.45). The row may cite the J. Finance version or a different paper. Not resolved.

## Alternatives considered and rejected
- **6J × London/WMR fix (KMW post-L):** JPY behaves oppositely to the other currencies (post-L −2.92, t −3.03), and the JPY "Europe" reversal portfolio is null (Table VII Panel B JPY mean −0.31, t −0.21). No coherent cell.
- **6J × turn-of-month / month-end:** D7 died on power 0.30 (monthly). Req 4 presumption.
- **6J × carry timing:** F-C SCREEN-FAIL (δ/σ 0.0267).
- **6J × opening-range-breakout (US window):** J16 OOS-falsified.
- **6J × intraday-momentum (first-half-hour → last):** no 6J cohort found in the time available, same breakout/trend decay prior, and closer to the ORB family.
- **Gotobi-only as the whole cell:** rejected as primary because its δ is UNSCREENABLE and inactivity may trip at Bulenox. Kept as limb H3 inside the K ≤ 3 band.

## Could not verify
- Any gotobi-conditional mean and σ (Akiyama et al. 2021 not opened; Bessho et al. gives PF and win rate only; Ito & Yamada is figure-only).
- Whether KMW Table I t-stats are HAC-adjusted.
- The JPY-only CME-futures leg (KMW reports only the futures dollar portfolio).
- The behaviour of the effect after 2019 (no cohort). KMW records a negative 2018.
- The annualization factor (÷252 assumed; KMW implies about 250.7 trading days a year from 5,264 obs over 21 years).
- The weekend-gotobi shift convention, behind the calendar frequency estimate of ~72 a year.
- USDJPY level for tick-to-bp conversion: L = 100/150 illustrative only.
- Whether Aegis 6J's trading hours overlap either window. Aegis was deliberately not read; the coordinator should route this to whoever may read Aegis.
- Bulenox ToS on hedging or cross-firm rules (venue register §E row 1: unread).
