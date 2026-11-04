# R3 cell screen: cost headroom first (index and ranking)

**Status:** zero-K screen for the next builder round (template Part A §A2–§A3 inputs, tasks T1–T3). **K = 0:** no market data was read. It decides nothing: cells, firms and rounds are Joshua's (Rule 3), and generation never blesses (Rule 25).
**Authority:** Joshua, 2026-11-04, verbatim: "go with option a, hold R2", with the next dossier wave re-aimed to lead with cost headroom ([generation note §11](https://github.com/Joshua-Asante/first-passage/pull/1064), PR #1064).
**Date / base:** 2026-11-04, `main` at `fd688b1`. **Budget (Rule 2):** one screen pass plus dossiers for survivors only; ≤3 Codex rounds; ~$0 compute; K = 0.
**Inputs read:** R2's [index and dossiers](https://github.com/Joshua-Asante/first-passage/pull/1061) (PR #1061); [template](https://github.com/Joshua-Asante/first-passage/pull/1051) Part A §A2–§A3 (PR #1051); [strategy_harvest](../../../methodology/strategy_harvest.md) Req 1, 2, 4, §4 and §4a (PR #1064); the generation note §1, §8.3, §9.2, §10.1, §10.2, §11; the [export ranking](../../../notes/2026-11-04-instrument-export-ranking-DRAFT.md); the eight instruments' ledgers, `MECHANISMS.md`, `PROFILES.md`, the [register](../../../rejected_candidates.md); the venue-fact register and microstructure study; [`lab/builder/README.md`](../../../../lab/builder/README.md).
**Dedup (Rule 8):** [DEDUP.md](DEDUP.md). Sources, quotes, hashes and the printed arithmetic: [sources/NOTES.md](sources/NOTES.md).

## Result

**No cell clears both cost headroom and power.** Of 28 cells screened, 0 survive, so no full dossier is written. The R3 recommendation is **no card**: every instrument's lifetime looks stay in reserve.

Every cell that clears 1.5 at both ends of the bracket is a scheduled-event cell (pre-FOMC, about 8 a year; macro announcement days): each fails power (≤ 0.22), and pre-FOMC also fails the builder's 200-trade minimum. Every cell with power ≥ 0.50 is a daily FX fix leg: its ratio is ≤ 0.94. Two index-momentum cells straddle 1.5 across the price bracket, but both fail power (≤ 0.17).

## Screen rule (stated before any figure was computed)

1. **Cost headroom:** ratio = cited per-event effect (after the §4 haircut, 0.42×) in ticks ÷ all-in round-trip cost in ticks. Cost = the provisional firm's round-trip commission + 2 ticks of slip (`THRESHOLDS["5b_slippage_ticks_per_side"]`). **Keep only a ratio ≥ 1.5 at both ends of the illustrative price bracket.**
2. **Power** (Req 4) ≥ 0.50 at the expected development event count: 1,492 sessions for MNQ, MYM, M2K and MES; 2,325 for MGC, 6J, M6E and M6A (R2's reach table, D9 holdout). Each instrument's lifetime look budget is D7/D9's: 2 for the index micros, 4 for the others.
3. **Builder floor:** at least `THRESHOLDS["5a_min_trades"]` = 200 development trades, or 5a kills the card.

Costs in round-trip ticks (repo commissions; sources in NOTES): MES 3.46 · MNQ, MYM, M2K 5.64 (Tradeify) · MGC 4.40 (BluSky NT proxy; 3.00 at its $0.50 eval rate) · 6J 2.82 (MFFU) · M6E 2.80 (Bulenox) · M6A 3.00 (Bulenox, the cheapest; no firm is mapped yet).

Price levels convert bp to ticks and are **illustrative, not market reads**: MES 3,000–6,000; MNQ 8,000–21,000; MYM 25,000–45,000; M2K 1,500–2,400; USD/JPY 100–150; EUR/USD 1.00–1.20; AUD/USD 0.60–0.75.

## The trade-off, in one line per instrument

A daily cell needs δ/σ ≥ 0.051 (index micros) or ≥ 0.041 (the others) after the haircut for power 0.50. Both bars together mean: haircut mean per event ≥ 1.5 × cost (in bp) **and** δ/σ ≥ that break-even. The table shows the window σ needed **if δ/σ sits exactly at the break-even** (σ ≥ 1.5 × cost ÷ δ/σ). It is conditional: a signal with twice the δ/σ needs half the σ, so a stronger signal on a shorter window can qualify.

| Instrument | Cost (bp, bracket) | Window σ needed at break-even δ/σ (bp) | Reading |
|---|---|---|---|
| MES | 1.4–2.9 | 43–85 | 35–70% of LM's 24-hour SPX σ (1.215%): a long intraday hold [INF] |
| MNQ | 0.7–1.8 | 20–52 | the cheapest index in bp at the high level; a shorter window could do [INF] |
| MYM | 1.3–2.3 | 37–67 | multi-hour [INF] |
| M2K | 2.4–3.8 | 69–111 | long intraday hold [INF] |
| MGC | 1.3–3.7 | 46–135 | multi-hour or longer [INF] |
| 6J | 1.4–2.1 | 52–78 | about 2–3× KMW's fix-window σ (~25–35 bp, derived from Table I mean, t and N) |
| M6E | 2.3–2.8 | 86–103 | about 3× KMW's fix-window σ |
| M6A | 4.0–5.0 | 148–185 | about 6× KMW's fix-window σ |

So a survivor needs **a haircut per-event mean of at least 1.5 × cost with δ/σ at or above the power break-even**. At the break-even that means a multi-hour or full-session window on an index micro or MGC (a gross daily Sharpe of about 0.12 before the haircut, about 1.9 a year); a higher-δ/σ signal can do it on a shorter window. No cited cohort in this pass offers either. Larger moves come only with rarer events, and those lose power faster than they gain headroom.

## Screen table (all 28 cells screened out; negative knowledge)

Ratio and slip are given at both ends of the bracket. "Slip allowed" is the total round-trip slip at which the ratio would reach 1.5. U = UNSCREENABLE (no cited per-event figure on an admissible cohort). Builder: **Y** = expressible now · **I** = ORB, expressible once the instrument is registered in `lab/builder/instruments.py` · **N** = needs a new block.

| # | Cell: instrument × mechanism (cohort) | Effect, haircut | Ratio | Slip allowed (ticks RT) | Power (events) | 5a | Builder | Why out | Priors (Rule 26) |
|---|---|---|---|---|---|---|---|---|---|
| I1 | MES × pre-FOMC drift (LM 2015, SPX cash 1994–2011) | 20.5 bp | **7.1–14.2** | 15–31 | 0.21 (47) | fail | N | power; 5a; the published window spans the flatten | Q-INVENTORY-1 power-wall; 10-21 note "dead (overnight hold)" |
| I1b | MES × pre-FOMC, post-2016 (register, KWG) | 9.2 bp | **3.2–6.4** | 6–13 | 0.08 (47) | fail | N | power; decayed after 2015 | same |
| I2 | MES × announcement-day premium (register) | 8.3 bp (gross) | **2.9–5.8** | 5–12 | 0.22 (register) | — | N | power; close-to-close cohort | Q-INVENTORY-1 |
| I3 | MES × intraday momentum (Gao SPY, 1993–2013) | 1.1 bp | 0.39–0.77 | ≤ 0.3 | 0.20 | ok | N | ratio; power; ETF transplant | index raised bar; MNQ class DEAD |
| I3v | MES × intraday momentum, high-vol tercile (Gao SPY) | 2.5 bp | 0.85–**1.70** | 0.5–2.5 | 0.13 (497) | ok | N | power; ratio fails at the low end | same |
| I5 | MNQ × intraday momentum (Gao QQQ, 1999–2013) | 1.3 bp | 0.73–**1.92** | ≤ 3.6 | 0.17 | ok | N | power; class DEAD on MNQ (NQ.md N3) | intraday-momentum DEAD MNQ/NQ |
| I6 | MYM × intraday momentum (Gao DIA) | 0.6 bp | 0.26–0.46 | none | 0.09 | ok | N | ratio; power | R2 r2-mym-intraday-momentum |
| I7 | M2K × intraday momentum (Gao IWM) | 2.0 bp | 0.52–0.83 | none | 0.34 | ok | N | ratio; power | R2 r2-m2k-imom |
| I8 | MES (and MNQ, MYM, M2K) × overnight drift (BLW, ES) | 0.6 bp | 0.22–0.43 | none | U | ok | N | ratio; decayed to ~0 since 2021 | R2 index holds |
| I9 | MNQ, MYM, M2K × pre-FOMC | U | U | — | U | fail | N | no own-index cohort (SPX→other index refused, Req 2) | Q-INVENTORY-1 |
| I10 | index micros × turn-of-month / pre-holiday | U | U | — | fails (monthly) | fail | N | Req 4 monthly precedent (D3, D7); no intraday cohort | SPX500 F5 TOM hard-absent |
| I11 | MES, M2K, MYM × ORB / opening auction | U | U | — | U | ok | I (MES), Y | no futures cohort; Req 1 fails (no payer, 1b unshown) | index raised bar; MYM ORC FALSIFIED |
| G1 | MGC × intraday momentum (BDLM GC) | U (no mean) | U | — | 0.09 | ok | N | power; no per-event mean | R2 NOTES-MGC |
| G2 | MGC × ORB / compression / PDH-PDL | U | U | — | U | ok | Y | Req 1 fails; no gold cohort | R2: skipped by Joshua |
| G3 | MGC × gold PM-fix public direction (Caminschi–Heaney GC, pre-2015 reform; MGC.md, `DELTA_EXTRACTION_R8.md`) | 0.55–1.35 bp | 0.15–1.07 (0.22–1.57 at BluSky's $0.50 eval rate) | 0.75 (2.15 at the eval rate), high end only | U (no σ in the extraction) | ok | N | ratio fails at the low end at both rates; power unscreenable; the 2015 auction reform is an adverse decay input not yet applied; the 3.21 bp top includes an end-block the extraction calls untimeable | 4× cost-law SCREEN-FAIL 2026-08-10 (deleted law; advisory). The Q-INVENTORY-1 K-kill was withdrawn by the K-bank ADR |
| F1 | 6J × post-Tokyo-fix (KMW JPY) | 1.3 bp | 0.63–0.94 | 0.4–1.0 | 0.63 | ok | N | ratio | R2 card, held |
| F2 | 6J × pre-Tokyo-fix | 0.7 bp | 0.32–0.48 | ≤ 0.1 | 0.37 | ok | N | ratio; power | — |
| F3 | 6J × Tokyo reversal, two legs (KMW Table VII) | 2.0 bp | 0.47–0.71 | 0.1–1.0 | 0.81 | ok | N | ratio | — |
| F4 | M6E × pre-ECB-fix (KMW EUR) | 1.5 bp | 0.53–0.63 | 0.2–0.4 | 0.52 | ok | N | ratio | R2 conditional cell; EURUSD fix-reversal bar |
| F5 | M6E × pre-Tokyo-fix | 0.8 bp | 0.27–0.32 | none | 0.69 | ok | N | ratio | same |
| F6 | M6E × post-Tokyo-fix | 1.0 bp | 0.35–0.42 | none | 0.74 | ok | N | ratio | same |
| F7 | M6E × post-London-fix | 1.1 bp | 0.41–0.49 | ≤ 0.1 | 0.47 | ok | N | ratio; power; flatten truncates the window | same |
| F8 | M6E × Europe reversal, two legs (KMW Table VII) | 2.6 bp | 0.47–0.56 | 0.2–0.5 | 0.79 | ok | N | ratio | same |
| F9 | M6A × pre-Tokyo-fix (KMW AUD) | 1.2 bp | 0.24–0.30 | none | 0.63 | ok | N | ratio | M6A A4: FX-fix δ refused pre-§4a |
| F10 | M6A × post-Tokyo-fix | 0.8 bp | 0.16–0.19 | none | 0.19 | ok | N | ratio; power | same |
| F11 | M6A × post-London-fix | 0.8 bp | 0.16–0.20 | none | 0.18 | ok | N | ratio; power | same |
| F12 | M6A × Tokyo reversal, two legs | 2.0 bp | 0.20–0.25 | none | 0.61 | ok | N | ratio | same |
| F13 | M6E × month-end London fix (Melvin–Prins) | U | U | — | fails (monthly) | fail | N | Req 4; panel-only estimate | EURUSD custodian month-end shelved |

**Reading limits.**
- The index-momentum (Gao) and pre-FOMC (SPX) cohorts are ETF or cash-index cohorts. Req 2 refuses cross-instrument transplants, and §4a admits spot cohorts for FX futures only. Their ratios are disclosure, not admissible screens; the conclusion holds even if they were admitted.
- §4a condition 1 names USD/JPY for 6J and EUR/USD for 6E/M6E. Whether it also covers AUD/USD for M6A is Joshua's reading; F9–F12 fail on cost either way.
- Every effect is gross of the cohort's own costs, and every power figure is before costs. The 252-day annualization, the illustrative levels and the tercile N (I3v) are my derivations (NOTES).
- I1b and I2 are register figures, not re-read at primary (labelled in NOTES).

## Ranking (closest misses, for the record)

1. **I3v MES high-vol intraday momentum** and **I5 MNQ intraday momentum** are the only cells near both bars: each clears 1.5 only at the high price level, and power is 0.13–0.17. Conditioning on volatility triples the per-event effect but cuts events to a third, so power falls. This is the trade-off in miniature.
2. **I1/I1b pre-FOMC** has the most headroom (ratio 3–14) and the least power (0.08–0.21 at about 47 events). The builder's 200-trade minimum kills it before any gate.
3. **F3/F8 FX reversals** have the most power (0.79–0.81) and a ratio ≤ 0.71. They would need limit fills with ≤ 0.1–1.0 tick of total slip, which an M-16 slip read on the future would have to show first.

## Mechanism families: expressibility and the block each would need

| Family | Cells | Builder now? | Block it would need (engine work) |
|---|---|---|---|
| Scheduled-release windows (FOMC, macro days) | I1, I1b, I2, I9 | No | an event-date input (calendar of releases, pinned like the holiday calendar) plus a clock-anchored entry and exit with market or limit orders. 5a's 200-trade floor would still kill any event under ~34 a year in a ~6-year window; changing it is Joshua's call |
| Opening auctions / ORB on new instruments | I11, G2 | ORB yes on MGC, M2K, MYM; MES, 6J, M6E, M6A need a `SESSION_OPEN` and `INSTRUMENT_SPECS` row | registration only, no new block. Missing input is a cohort, not code |
| Multi-hour trend legs | the frontier above | Partly: an ORB with a late `flat_at` and no target is a multi-hour hold | none for the ORB form. A non-ORB trend entry needs a new entry block |
| Intraday momentum (first window's sign → last window) | I3–I7, G1 | No | a time-entry block conditioned on an earlier window's sign, exiting at a clock time |
| FX fix legs | F1–F12 | No | a clock-entry, clock-exit block, plus a Globex-evening session model (the builder reads the US day session only) |

Venue note for any future event cell: Tradeify allows news trading on all accounts; MFFU prohibits Tier 1 releases (FOMC among them) on Rapid and Pro sim-funded plans (venue-fact register; R2 6J dossier).

## What this aims next

- **Cohort search, narrowed:** published futures cohorts on index micros or gold whose haircut per-event mean is ≥ 1.5 × cost with δ/σ at or above the power break-even: a multi-hour or full-session window at a gross daily Sharpe of about 0.12, or a shorter window with proportionally higher δ/σ.
- **Cost side:** an M-16 fill-slip read (limit vs market) on 6J and M6E in their fix hours. Only that could move F1, F3 or F8 (each needs ≤ ~1 tick of total round-trip slip), and it is already owed under §4a condition 4.
- **Owed after this screen:** ledger dispositions (Rule 27) for the eight instruments, at T8 by a seat that holds `governance.author` for them. This PR edits no ledger.
