# R3 source log and screen arithmetic (2026-11-04, K = 0)

No market data was read. Every figure below is from a cited publication, a repo owner record, or an illustrative price level labelled as such. Clock times from the papers are elided (public-file limit).

## Sources opened by the coordinator (primary text)

| Source | Copy read (2026-11-04) | Figures used, verbatim |
|---|---|---|
| Krohn, Mueller & Whelan, *Foreign Exchange Fixings and Returns Around the Clock*, BoC SWP 2021-48 (J. Finance 79(1) 2024 not opened) | https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf, pdftotext; sha256 `807fdb20dac0010b3b41f3f08c17b9bf7a233291fea449cd64cd86ad54fa0f46` (same file R2 verified) | Table I ("annualized average returns … t-statistics are reported in parentheses … January 1999 to December 2019"): AUD pre-T −7.15 (−8.24), post-T 4.66 (3.94), post-L 4.86 (3.75); EUR pre-T −4.54 (−8.83), post-T 5.89 (9.29), pre-E −8.87 (−7.24), post-L 6.87 (6.78); JPY pre-T −4.06 (−5.87), post-T 7.94 (8.22). Table VII reversal means (annualized) with t: Tokyo AUD 11.82 (8.03), EUR 10.44 (12.60), JPY 12.00 (10.12); Europe EUR 15.76 (9.95). N = 5,264 days is KMW's stated count (R2 coordinator check) |
| Gao, Han, Li & Zhou, *Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return*, working paper "December, 2015" (JFE 129(2) 2018 not opened) | https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf; sha256 `050d5680d1424a5f53aeb175de283bc796b130be3874abf319aa1980941cc374` | SPY, 1993-02-01..2013-12-31: "the average return of the timing strategy using the sign of the first half-hour return is 6.67% per annum with a standard deviation of 6.19%. The Sharpe ratio is thus 1.08". Volatility terciles: "from 0.54% (0.43) in the low volatility group, to 4.75% (2.27) in the medium volatility group, and then to 14.73% (3.80) in the high volatility group". Table 12 Panel A (ETF inception to 2013-12-31): QQQ 7.75 (3.65), Std 7.89; DIA 3.46 (2.35), Std 5.69; IWM 11.72 (5.18), Std 7.70 |
| Lucca & Moench, *The Pre-FOMC Announcement Drift*, NY Fed Staff Report 512 (revised Aug 2013; J. Finance 70(1) 2015 not opened) | https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf; sha256 `c7cb0f335c60cb9fc305189935fb7c51e98fa8461c2b33efd51eb5a5c3f2e34b` | "since 1994, the S&P500 index has on average increased 49 basis points in the 24 hours before scheduled FOMC announcements"; "for the 131 FOMC observations … 49 basis points, with a t-statistic of more than 4.5"; summary table, post-1994 pre-FOMC SPX window: mean .488, St.Dev. 1.215, N 131; "there are only eight scheduled FOMC meetings each year". Cohort is the SPX cash index, not futures |

## Sources read through a summary only (labelled [W-x], not byte-verified)

- Kurov, Wolfe & Gilbert, *The Disappearing Pre-FOMC Announcement Drift*, Finance Research Letters 40 (2021), DOI 10.1016/j.frl.2020.101781 ([IDEAS](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html)). Search summary: the drift "largely vanished after 2015". The PDF link returned HTML, not the paper. The post-2016 figure used (≈9.2 bp/event, δ/σ ≈ 0.08) is the [Q-INVENTORY-1 register entry](../../../../rejected_candidates.md)'s, not re-read at primary.
- Announcement-day SPX (+8.3 bp/event, δ/σ 0.075, power ≈ 0.22 at N ≈ 252): the same register entry; Savor–Wilson not opened.
- ORB academic cohorts: one search (2026-11-04) found no peer-reviewed per-trade figure for an ORB on ES, NQ, YM, RTY, GC or the FX futures; vendor backtests (edgeful, metrotrade, proptradingvibes) are not cohorts and were not used.

## Reused from R2 (PR #1061, coordinator-verified there)

- Boyarchenko, Larsen & Whelan, SR917: ES overnight drift "1.48 basis points per day" (1998–2020); NY Fed Liberty Street 2026-07-01: "averaged close to zero since 2021" (NOTES-MYM, NOTES-M2K).
- Baltussen, Da, Lammers & Martens, JFE 142 (2021) Table B3: GC βROD 1.09 (t 2.95), N 9,044 → δ/σ 0.031; no per-event mean reported (NOTES-MGC).
- McLean & Pontiff (2016): "58% lower post-publication" (central haircut 0.42×).

## Repo inputs

- Commissions (round trip, all-in): Tradeify index micros $1.82 (`core/firm_rules.py:241`); MFFU 6J $5.12 (`:373`); Bulenox M6A/M6E $0.50/side (`:102`); BluSky MGC $1.20/side NT proxy, $0.50 Rithmic-class eval (`:406-415`).
- Tick values: MES $1.25, MNQ/MYM/M2K $0.50, MGC $1.00 (`core/instrument_specs.py:17-21`); 6J $6.25 (R2 dossier, CME ¥12.5M contract); M6E $1.25 (R2 NOTES-M6E; Rule 17 re-read owed at landing); M6A $1.00 (`ops/instruments/M6A.md` A1).
- The all-in ticks agree with the [microstructure study](../../../../notes/2026-11-01-prop-firm-microstructure-study-DRAFT.md) table (≈5.6 ticks RT on MNQ/MYM).
- Slip: `lab/builder/gates.py` `THRESHOLDS["5b_slippage_ticks_per_side"]` = 1 (2 ticks RT); `"5a_min_trades"` = 200.
- Builder instruments: `lab/builder/instruments.py` `SESSION_OPEN` lists MCL, MGC, M2K, MYM, MNQ only; cards are `bar: 15m`, `session: day` only (`lab/builder/cards.py:139-140`).

## Screen arithmetic (plain Python, no project code, `python3 -I`)

Definitions:
- effect (bp) = annualized mean ÷ 252 × 100, × 0.42 haircut unless the figure is already post-publication;
- ticks = effect ÷ (bp per tick at the illustrative level);
- cost (ticks) = RT commission ÷ tick value + 2, × legs;
- ratio = ticks ÷ cost;
- δ/σ = t ÷ √N_cohort (or daily Sharpe), × 0.42; power = Φ(√N_events·δ/σ − 1.96), N_events = development sessions × event share (1,492 for index micros, 2,325 for MGC/6J/M6E/M6A, from R2's reach table);
- "slip allowed" = total RT slip (all legs) at which the ratio would be exactly 1.5.

Illustrative levels (not market reads): MES 3,000 / 6,000; MNQ 8,000 / 21,000; MYM 25,000 / 45,000; M2K 1,500 / 2,400; USD/JPY 100 / 150; EUR/USD 1.00 / 1.20; AUD/USD 0.60 / 0.75.

Printed output (2026-11-04):

```text
I1 pre-FOMC (LM 2015)                    MES  eff  20.50bp ticks  24.60/ 49.19 cost  3.46 ratio  7.12/14.23 slip@1.5  14.94/ 31.34 d/s 0.1651 N 47 power 0.21
I1b pre-FOMC post-2016 (register/KWG)    MES  eff   9.20bp ticks  11.04/ 22.08 cost  3.46 ratio  3.19/ 6.39 slip@1.5   5.90/ 13.26 d/s 0.0800 N 47 power 0.08
I2 announcement-day (register)           MES  eff   8.30bp ticks   9.96/ 19.92 cost  3.46 ratio  2.88/ 5.76 slip@1.5   5.18/ 11.82 power: see note
I3 intraday momentum SPY                 MES  eff   1.11bp ticks   1.33/  2.67 cost  3.46 ratio  0.39/ 0.77 slip@1.5  -0.57/  0.32 d/s 0.0286 N 1492 power 0.20
I3v high-vol tercile SPY                 MES  eff   2.46bp ticks   2.95/  5.89 cost  3.46 ratio  0.85/ 1.70 slip@1.5   0.51/  2.47 d/s 0.0381 N 497 power 0.13
I3 intraday momentum QQQ                 MNQ  eff   1.29bp ticks   4.13/ 10.85 cost  5.64 ratio  0.73/ 1.92 slip@1.5  -0.88/  3.59 d/s 0.0260 N 1492 power 0.17
I3 intraday momentum DIA                 MYM  eff   0.58bp ticks   1.44/  2.59 cost  5.64 ratio  0.26/ 0.46 slip@1.5  -2.68/ -1.91 d/s 0.0161 N 1492 power 0.09
I3 intraday momentum IWM                 M2K  eff   1.95bp ticks   2.93/  4.69 cost  5.64 ratio  0.52/ 0.83 slip@1.5  -1.69/ -0.51 d/s 0.0403 N 1492 power 0.34
I4 overnight drift ES (BLW)              MES  eff   0.62bp ticks   0.75/  1.49 cost  3.46 ratio  0.22/ 0.43 slip@1.5  -0.96/ -0.46 power: see note
F1 6J post-Tokyo                         6J   eff   1.32bp ticks   1.76/  2.65 cost  2.82 ratio  0.63/ 0.94 slip@1.5   0.36/  0.95 d/s 0.0476 N 2325 power 0.63
F2 6J pre-Tokyo                          6J   eff   0.68bp ticks   0.90/  1.35 cost  2.82 ratio  0.32/ 0.48 slip@1.5  -0.22/  0.08 d/s 0.0340 N 2325 power 0.37
F3 6J Tokyo reversal                     6J   eff   2.00bp ticks   2.67/  4.00 cost  5.64 ratio  0.47/ 0.71 slip@1.5   0.14/  1.03 d/s 0.0586 N 2325 power 0.81
F4 M6E pre-ECB                           M6E  eff   1.48bp ticks   1.77/  1.48 cost  2.80 ratio  0.63/ 0.53 slip@1.5   0.38/  0.19 d/s 0.0419 N 2325 power 0.52
F5 M6E pre-Tokyo                         M6E  eff   0.76bp ticks   0.91/  0.76 cost  2.80 ratio  0.32/ 0.27 slip@1.5  -0.19/ -0.30 d/s 0.0511 N 2325 power 0.69
F6 M6E post-Tokyo                        M6E  eff   0.98bp ticks   1.18/  0.98 cost  2.80 ratio  0.42/ 0.35 slip@1.5  -0.01/ -0.15 d/s 0.0538 N 2325 power 0.74
F7 M6E post-London                       M6E  eff   1.15bp ticks   1.37/  1.15 cost  2.80 ratio  0.49/ 0.41 slip@1.5   0.12/ -0.04 d/s 0.0392 N 2325 power 0.47
F8 M6E Europe reversal                   M6E  eff   2.63bp ticks   3.15/  2.63 cost  5.60 ratio  0.56/ 0.47 slip@1.5   0.50/  0.15 d/s 0.0576 N 2325 power 0.79
F9 M6A pre-Tokyo                         M6A  eff   1.19bp ticks   0.89/  0.71 cost  3.00 ratio  0.30/ 0.24 slip@1.5  -0.40/ -0.52 d/s 0.0477 N 2325 power 0.63
F10 M6A post-Tokyo                       M6A  eff   0.78bp ticks   0.58/  0.47 cost  3.00 ratio  0.19/ 0.16 slip@1.5  -0.61/ -0.69 d/s 0.0228 N 2325 power 0.19
F11 M6A post-London                      M6A  eff   0.81bp ticks   0.61/  0.49 cost  3.00 ratio  0.20/ 0.16 slip@1.5  -0.59/ -0.68 d/s 0.0217 N 2325 power 0.18
F12 M6A Tokyo reversal                   M6A  eff   1.97bp ticks   1.48/  1.18 cost  6.00 ratio  0.25/ 0.20 slip@1.5  -1.02/ -1.21 d/s 0.0465 N 2325 power 0.61
{'MES': 3.456, 'MNQ': 5.64, 'MYM': 5.64, 'M2K': 5.64, 'MGC': 4.4, '6J': 2.819, 'M6E': 2.8, 'M6A': 3.0}
```

Derivation notes (mine, not the papers'):
- I3v: the tercile figure is read as annualized ×252 over the tercile's own days; N_cohort = 5,270/3 (one third of the SPY sample days). A shorter out-of-sample span would raise δ/σ: at N_cohort ≈ 1,333 power is still 0.16.
- I1: δ/σ uses the "more than 4.5" t over 131 events (0.393), below the table's mean/σ (0.402). Events in development ≈ 1,492 × 8/252 ≈ 47.
- I1b and I2 carry no extra haircut: the I1b figure is post-publication, and I2's register power (0.22) is quoted as the register gives it.
- 6J and M6A signs: KMW Table I reports foreign-currency appreciation as positive, which carries over to 6J (USD per JPY) and to M6A/M6E unchanged (§4a condition 2).
