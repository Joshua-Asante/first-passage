# NOTES-M6E — R2 worker notes (2026-11-04, K = 0)

## 1. Ranking
1. **r2-m6e-prefix** (M6E × `fx-fix-dealer-prehedge-drift` NEW × MFFU), ranked first.
   - It is the only cell with a named payer under path 1a: benchmark-execution customers, with dealer pre-hedging under inventory constraints.
   - It trades daily, and its effect figure comes from the EUR/USD spot parent with a t-statistic. Power at the conservative 58% haircut is 0.52, which is marginal; at 32% it is 0.91.
   - It is fully distinct from the ORB book.
   - Weaknesses:
     - (a) It probably trips the letter of D2's bar ("NOT … a different fix (Tokyo/Frankfurt)").
     - (b) Cost geometry is the binding risk. After the 58% haircut and commission, 0.3–0.6 tick of round-trip slip consumes the effect. That is the same wall D2 hit.
     - (c) The ECB reference-rate publication moved in July 2016, inside the dev window.
     - (d) The window runs in US pre-dawn hours, so attended operation is a burden.
2. **r2-m6e-asialdn** (M6E × `asia-range-london-breakout-continuation` NEW × MFFU), ranked second.
   - It is not a seed today: it meets neither 1a nor 1b, and it is UNSCREENABLE (no EUR/USD cohort δ).
   - It probably fails the D10 mechanism-distinctness limb against ORB.
   - Its stop entry carries the highest exposure to MFFU's favorable-fills clause.
   - The DL-2 geometric-feasibility diagnostic is owed before any freeze.
   - I kept it because the brief named it and because it records what a δ-extraction probe on the M6E export would need to deliver.

## 2. Sources opened (verbatim support; coordinator to re-verify)
- **Krohn, Mueller, Whelan, Bank of Canada Staff Working Paper 2021-48**, "Foreign Exchange Fixings and Returns Around the Clock". This is the working-paper version of *J. Finance* 79(1) 2024, 541–578, DOI 10.1111/jofi.13306, per EconPapers. https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, accessed 2026-11-04. I extracted the full PDF text locally with pdftotext. I did not open the published JF version, so its figures may differ (Rule 20).
  - Abstract: "the U.S. dollar pre-fix and a depreciation post-fix. We propose an explanation based on constrained intermediation by foreign exchange dealers … evidence of an unconditional demand for U.S. dollars at currency fixings. Dealers hedge this demand pre-fix".
  - Table I, EUR row (sample Jan 1999–Dec 2019): "pre-T -4.54 (-8.83); post-T 5.89 (9.29); pre-E -8.87 (-7.24); E-L 1.58 (1.35); post-L 6.87 (6.78); CTC 0.92 (0.43)". These are annualised average returns, with t in parentheses.
  - Table II, dollar portfolio, 14-19 row: "-1.59 (-2.64) 2.08 (2.25) -3.14 (-2.28) -1.52 (-1.02) 2.16 (1.62) -2.01 (-0.76)". This is the post-Feb-2015 period I used for the decay ratios.
  - Table III, CME Futures row (2006–2019): "-4.06 (-8.93) 5.61 (10.00) -5.06 (-5.81) 0.36 (0.38) 1.88 (2.60) -1.27 (-0.79)".
  - Window definitions (note 2): "For the 'Europe' window the short position is held from [time elided] until the ECB fix at [time elided], and the long position is held starting with the London fix at [time elided] until 5:00 p.m. ET."
  - Anchor change: "the ECB has moved the publication of the reference rates to [time elided] in July 2016 while keeping the methodology unchanged … Subsequently, the Reuters [time elided] fix was introduced".
  - WMR window change, footnote 8: "Before 15 February 2015, the length of the window to calculate the fix rate was only a one-minute interval from 3:59:30 p.m. to [time elided]:30 p.m."
  - Costs: "Incorporating the full transaction costs adjustment as implied by the indicative quotes, again, reverses the picture, and average returns for most windows turn negative". Also: "it is not obvious that this can be exploited by the average trader".
  - Table IX, EUR Europe at 50% bid-ask: "pre 5.45 post 3.19 pre+post 8.64"; at 100% bid-ask: "2.02 -0.50 1.52".
  - Decay in sample: "dropped to below 5% during the last two years in our sample". Also: "some arbitrage capital is allocated to exploiting the reversal patterns".
  - Month-end channel: "our results are not driven by and end-of-month equity hedging channel as studied by Melvin and Prins (2015)".
  - Obs count used for N: Table VIII "Obs 47,358". Dividing by 9 currencies to get ~5,262 days is my derivation, not the paper's.
- **McLean & Pontiff, "Does Academic Research Destroy Stock Return Predictability?", *J. Finance* 71(1) 2016, 5–32.** https://Www.Gwern.net/doc/economics/2016-mclean.pdf, accessed 2026-11-04, extracted with pdftotext. Abstract: "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication … We estimate a 32% (58%–26%) lower return from publication-informed trading."
- **Melvin & Prins, "Equity hedging and exchange rates at the London 4 p.m. fix", *J. Financial Markets* 22 (2015) 50–72.** I read the 2013 ECB workshop draft at https://www.ecb.europa.eu/events/pdf/conferences/131216/Third_FX_Workshop_MELVIN_PRINS_Equity%20hedging%20and%20exchange%20rates%20Nov%202013.pdf, accessed 2026-11-04, not the published version.
  - Sample: "April 28, 2004 and end on December 31, 2012 giving us a sample period of 8.66 years".
  - Panel regression: "ri,T FX = −0.0142 ri,T−1 EQ, R2 = 0.03".
  - Effect size: "a 10% equity appreciation leads to 14 basis points of currency depreciation. Though significant, this seems like quite a small effect."
  - This is a panel estimate only; the draft reports no EUR-specific return coefficient in what I read.
- **Evans, "Forex trading and the WMR Fix"**, abstract only (search result). It is in *J. Banking & Finance* 87 (2018) 233–247, DOI 10.1016/j.jbankfin.2017.09.017. The brief said JIE; that is incorrect. Source: https://ideas.repec.org/a/eee/jbfina/v87y2018icp233-247.html. Per the search summary, the working-paper version reports "extraordinary volatility and negative serial correlation around the Fix". I opened no figure from it and used none.
- **MFFU help centre** pages, fetched 2026-11-04 through a summarising tool [W-x]. The quotes are model-extracted, so re-read them by hand.
  - 8230009 (news policy): "Trading on T1 News events is prohibited for the following:" Rapid Sim Funded and Pro Sim Funded. "permitted for the following:" All evaluations and Builder Plans. "No positions or orders (including limit orders) can be open 2 minutes before and after the release." T1 list: "FOMC Meetings, FOMC Minutes, Employment Report, CPI". "Last updated: August 31, 2026".
  - 8444599 (fair play): "Traders may make use of automated trading strategies tailored to their own specific settings". "do not aim to exploit the favorable fills offered in the Simulated Environment". "Exploiting the absence of slippage and utilizing tight brackets to gain from favorable fills are not permitted." "High-frequency Trading is not allowed on our plans." "MyFunded Futures prohibits hedging of any kind." The page states no same-strategy-elsewhere rule. Page date: "Updated this week."
- Search-only leads, not used as evidence:
  - Pragma report on the post-2015 fix: "momentum effect on ordinary days has weakened since the change, but the reversion appears just as strong". This is a vendor finding via euromoney.com.
  - NewChange FX claims the wider window raised execution costs by up to 60% (fx-markets.com). Also a vendor finding.
  - Baltussen, Da, Lammers, Martens 2021 *JFE* (https://www3.nd.edu/~zda/intramom.pdf), not opened.
  - Elaut et al. 2018, abstract only.

## 3. Alternatives considered and rejected
- **London WMR post-fix leg** (long EUR from the London fix into the US afternoon). This is the brief's named "US morning" fix.
  - EUR spot δ/σ = 6.78/√5262 = 0.0935.
  - The dollar-portfolio 2014–19 ratio is 0.59 (t 1.62, not significant), so it has decayed since the window change.
  - On CME futures the dollar portfolio shows only 1.88% at t 2.60, giving δ/σ 0.044.
  - At the 58% haircut, power is Φ(48.22 × 0.0393 − 1.96) = 0.47.
  - MFFU's 16:10 ET liquidation truncates the paper's window, which runs to 17:00 ET.
  - It is D2's exact direction (cost-killed), and it overlaps the falsified 6E dealer-wake span.
  - Net of commission it has about 0 tick of room after the 58% haircut.
  - Verdict: ranked below the pre-ECB leg.
- **Tokyo fix legs.** EUR δ/σ is 0.122 pre-T and 0.128 post-T, the strongest on full sample. But the dollar-portfolio 2014–19 ratios are 0.45 and 0.49, KMW report "negative returns for the EUR … since" about 2013 net of 50% bid-ask, and D2's bar names "Tokyo" explicitly. Same mechanism as cell 1. It could be a second K_intrinsic expression of cell 1 if the coordinator wants one (K ≤ 3).
- **Month-end WMR hedging (Melvin–Prins).** This has a named payer, but at monthly frequency N ≈ 2,325/21 ≈ 110. Taking √R² = 0.17 as an optimistic δ/σ-equivalent (panel, not EUR, 2004–2012), power is Φ(√110 × 0.17 − 1.96) = 0.43 before any haircut and 0.11 after 58%. It fails Req 4, and D1 (EURUSD custodian month-end) is shelved. Rejected.
- **`prior-session-breakout-continuation` as-is on M6E** (full prior session reference). The DL-2 geometry (median R = 1.0 on M6A at a later force-flat) predicts the same pathology, and MFFU's earlier 16:10 flat makes it worse. Rejected in favour of the Asia sub-window variant.
- **Baltussen-class intraday momentum on M6E.** The `intraday-momentum` class finding is dead on MNQ. The FX "close" window sits at 17:00 ET, after MFFU's 16:10. Not pursued.

## 4. Could not verify / open issues
- I did not open the published JF tables; all KMW figures come from the 2021 SWP.
- N_days ≈ 5,262 (1999–2019) and N ≈ 1,315 (2014–19) are my derivations.
- The 252-day annualisation in the bp conversion is an assumption.
- The EUR/USD 1.0–1.2 level used for ticks is an assumption. It is not a market-data read.
- There is no EUR-specific post-2014 subsample in KMW. The decay ratio is borrowed from the dollar portfolio, which includes EUR, and is disclosed.
- MFFU pages were read through a summarising fetch [W-x], not verbatim HTML.
- The M6E tick ($1.25) is quoted only in the generation DRAFT §9.1 (the CME spec page). `core/instrument_specs.py` has no M6E row. Rule 17 re-read is owed at landing.
- **D10 premise check.** "Cheapest M6E costs" at MFFU is contradicted by repo figures. `core/firm_rules.py` gives Bulenox M6A/M6B/M6E at 0.5/side ($1.00 RT), below MFFU's $1.44 RT and Tradeify's $1.60 RT. MFFU is cheapest only among MFFU, Tradeify and BluSky-NT ($0.84/side).
- I did not read the third-leg Stage-1 M6E `E-COST` record (archive RESULTS). It is a disclosed cost-side prior on M6E, cited by M6B.md W4, and the coordinator should read it before freezing either cell.
- Attended-operation feasibility for European-morning windows is an operator question (envelope E6, Rule 11 "attended only").
