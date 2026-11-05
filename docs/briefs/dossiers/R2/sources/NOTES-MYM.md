# NOTES — MYM R2 dossiers (2026-11-04, K = 0, no market data read)

## Ranking
1. **r2-mym-overnight-drift** (narrowly first). It is the only MYM cell found whose venue legality and distinctness are clean by construction:
   - long-only and time-disjoint from ORB-MNQ, so it cannot breach Tradeify ESA §6.7 whichever side ORB trades;
   - out of the index raised bar's own stated scope;
   - it names a payer and a HOW-dies observable.

   It is **UNSCREENABLE** (no YM number; ES transplant refused), and the authors' own 2021–2025 sample says the drift is about zero. That covers most of MYM's development window. **Expected outcome of a probe: null.**
2. **r2-mym-intraday-momentum.** It is screenable on the parent YM cohort (the best target-side figure available), but:
   - it fails Req 4 at the 58% haircut (power 0.14);
   - the in-house sibling (MNQ) shows OOS decay to negative;
   - route 1 of the raised bar is contested ("a different index is the exhausted move");
   - at the haircut figure the per-event edge sits below Bulenox commission before any slip;
   - **it conflicts with the Tradeify cross-firm hedging rule**: two-sided, holding into the close while ORB-MNQ may be open.

**Honest bottom line:** neither cell clears Req 2 and Req 4 today. If the coordinator spends one of MYM's two builder looks, the overnight cell's probe is the cleaner question: it is pre-post-2021 split-able and compliance-clean, and a null there is informative. The intraday cell would be spending a look against a sibling falsification.

## Provisional firm reasoning (both cells: Bulenox)
- D10 maps index→Tradeify, but the 10-30 ruling is "one strategy per firm; Tradeify scales by accounts", and Tradeify hosts ORB-MNQ. A second Tradeify index strategy contradicts that ruling while it stands. Joshua 2026-11-03: "For now we are not letting index stay Tradeify only."
- BluSky (metals) and MFFU (FX) hold D10 slots. Bulenox's slot is "6J … or held", the weakest. Bulenox also has the cheapest MYM cost ($0.61/side → 2.44 ticks RT) and a 16:59 ET flat-by.
- **Cross-firm hedging consequence, either way:** Tradeify ESA §6.7(c),(i) binds every Tradeify account against External Accounts. Wherever an MYM book runs, its short positions must never coincide with a long Tradeify Equity Index position (and vice versa).
  - Overnight cell: satisfied by construction.
  - Intraday cell: not satisfied unless restricted to long-only or given a cross-firm sign guard; both change the screened cohort.
- Gaps: Bulenox's own hedging rule; whether Bulenox counts an evening-reopen-to-pre-US-open position as intraday; NT8-over-Rithmic as the native route.

## Sources opened (verbatim support)
- **Boyarchenko, Larsen, Whelan, FRBNY Staff Report 917** — https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf (2026-11-04, pdftotext of the PDF):
  - "the largest positive returns are between [time elided] and [time elided] - the opening of European markets … averaging 3.7% on an annualized basis (1.48 basis points per day)"
  - "Our sample period spans January 5, 1998 – December 31, 2020 (23 years)." The data is "the most liquid e-mini contract" (S&P 500).
  - "Average returns for the hours {24-01, 01-02, 02-03} are equal to {0.46, 0.43, 1.5} basis points per hour per day (bps) with corresponding t-statistics equal to {2.8, 2.8, 7.1}"
  - "OD returns were positive in 20 out of 23 years … slightly negative in … 2002 and 2008, and again in 2019"
  - "the futures market is traded as a hedging instrument for the underlying"
  - Publication RFS 36(9) 2023 pp. 3502–3547 per RePEc https://econpapers.repec.org/RePEc:oup:rfinst:v:36:y:2023:i:9:p:3502-3547 (search result only; page not opened).
  - Abstract page: https://www.newyorkfed.org/research/staff_reports/sr917
- **Boyarchenko, Larsen, Whelan, "The Disappearing Overnight Drift," Liberty Street Economics, 2026-07-01** — https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ (2026-11-04, via fetch summary; quotes as returned):
  - "the [time elided] window that previously generated roughly 3.7 percent per annum has averaged close to zero since 2021"
  - "The same pattern holds in the E-mini Nasdaq-100 (NQ) and E-mini Dow Jones (YM) contracts" (no YM numbers)
  - Samples: 1998–2020 (5,691 trading days); 2021-01–2025-12 (1,245 days)
  - "the standard deviation of end-of-day RSV fell from 6.5 percent to 2.9 percent"
  - ⚠ The coordinator should re-open this page directly; I read it through a summarising fetch, not raw HTML.
- **Baltussen, Da, Lammers, Martens, "Hedging demand and market intraday momentum," JFE 142(1) 2021, 377–403** — https://academicweb.nd.edu/~zda/intramom.pdf (2026-11-04, pdftotext -layout):
  - Table A1 row YM: start 1997-10-08, end 2020-05-01, Obs 5639, 09:30–16:00.
  - Table B1 Panel B row YM: βONFH 6.07 (3.28), R² 1.34, R²OOS 1.31; βROD 5.02 (4.12), R² 2.20, R²OOS 2.18∗∗∗ ("Newey and West (1986) robust t-statistics are in parentheses … Adjusted R2, R2OOS, and slope coefficients are multiplied by 100").
  - §5: "hedging demand coming from short gamma exposure"; "Sharpe ratios between 0.87 and 1.73" (pooled, not YM).
- **Gao, Han, Li, Zhou, "Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return,"** working paper, "Current Version: December, 2015" (published JFE 129(2) 2018, 394–414 per RePEc) — https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf (2026-11-04):
  - "they include domestic alternative stock indices such as the Dow … (DIA, QQQ, and IWM)"
  - "the in-sample R2 ranges from 1.16% for DIA to 8.54% for EEM"
  - Table 12 Panel A row DIA: Avg Ret 3.46∗∗ (2.35), Std Dev 5.69, INS R² 1.16, OOS R² 1.03, CER 4.16. Table 11: DIA inception 01/20/1998; "sample period for each ETF is from its inception date to December 31, 2013, excluding days with fewer than 100 trades."
  - ⚠ These are working-paper numbers; the final JFE table may differ.
- **McLean & Pontiff, JF 71(1) 2016** — https://Www.Gwern.net/doc/economics/2016-mclean.pdf (2026-11-04): "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication."
- **DJIA 40,000 close (illustrative level only)** — https://spokesman.com/stories/2024/may/17/dow-closes-above-40000-for-the-first-time and https://www.cbsnews.com/news/dow-closes-above-40000-for-first-time-notching-new-milestone: closed at 40,003.59 on 2024-05-17. These are search-result summaries; pages not opened.

## Repo figures used (owner, read 2026-11-04)
- Costs per side, all MYM:
  - Bulenox 0.61 (`core/firm_rules.py:140`; venue register §F)
  - Tradeify 0.91 (`:326`; RT $1.82, 10468315)
  - MFFU 0.95 (`:389`)
  - BluSky 0.95 NT proxy / $0.50 Rithmic (`:480`; envelope §4)
- MYM tick: 1 pt = $0.50 (MYM.md header and 2026-09-02 session log).
- Dev sessions 1,492: coordinator's estimate (brief).
- Builder looks for MYM: 2 lifetime (generation note §11).
- The consult tool's "cost hurdle: 6.57 bp/event (4x Tradeify hurdle)" derives from the deleted Req 5 (2026-10-24). It is stale as a gate; I disclose it and do not use it.

## Alternatives considered and rejected
- **Overnight-range transmission / gap magnitude / daily-range-state persistence** (AMBIGUOUS-PARKED). These are conditioner-role (range, not direction). Q-RANGEXFER-1 closed `AMBIGUOUS-DESIGN` for MYM parent and `.b`, and `FALSIFIED` for `.a-MYM`. ITERATE return target (a): "the panel reaches ≥7 qualifying years". **The new 2019-05→2026-11 MYM export may now meet that.** That re-measure needs no direction claim; it is worth flagging to the coordinator but is not a builder cell (no entry). Re-proposal bar for `.a-MYM`: "new mechanism evidence — a materially different construct or a longer panel".
- **Opening-range continuation, PDH/PDL reclaim, sweep-failure continuation, opening-pressure, third-Friday reversal, ict-liquidity** — DEAD on MYM, each with an explicit re-proposal bar (ledger DEAD table; register). They also sit near ORB's session.
- **ORB+scale-in (M8 / ORB-MYM v0.4)** — the same mechanism as the index ORB book. It fails distinctness and has no untouched holdout.
- **MOC-imbalance on MYM** — paid-data procurement gate; UNSCREENABLE.
- **Pre-FOMC / macro-release drift** — monthly-or-rarer events; fails Req 4 by class precedent (D3, D7).
- **Leveraged-ETF EOD flow on the Dow** — the register's re-proposal bar says "NOT … a different index"; covered as a disclosed limb of the intraday cell rather than a cell of its own.

## Could not verify
- A YM- or MYM-specific overnight-drift figure (the authors name YM without numbers; the online appendix was not searched).
- The final JFE 2018 Table for DIA (I used the working paper).
- Bulenox: hedging rule; treatment of evening-reopen positions; NT8/Rithmic native automation.
- The side of the current Tradeify ORB-MNQ native edition (the ledger shows a long-only reconstruction baseline only).
- Striker DJ30 MYM edition windows (private; not read, by rule).
- The K-bank count: 7 by manifest read vs. 6 in the ledger (the ledger omits `q_txg1_striker_nas100_mym_20260812`).
- What "venue-walled" means for H-OD-1 in the raised-bar scope line (H-OD-1 died at the cost law; not separately sourced).
