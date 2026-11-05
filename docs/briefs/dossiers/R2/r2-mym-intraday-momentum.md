# r2-mym-intraday-momentum: MYM × `intraday-momentum` × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MYM (CBOT Micro E-mini Dow) · Mechanism: `intraday-momentum` (existing, Baltussen-class) · Provisional firm: **Bulenox** (deviates from D10's index→Tradeify; reason under Venue legality) · Session: the US cash-session close (New York late afternoon). The direction comes from the session's return so far, held into the cash close.
- Event frequency: every session (Baltussen 2021 and Gao 2018 time every trading day).

## Mechanism (harvest Req 1, path 1a)
- WHO pays: short-gamma option hedgers and leveraged/inverse ETFs, whose daily rebalance is a mechanical mandate (Baltussen, Da, Lammers, Martens 2021, §5: "hedging demand coming from short gamma exposure"). This is a constraint, not a preference. **Met** in class. For the Dow specifically, the size of Dow-linked gamma and leveraged-ETF AUM is unmeasured here.
- WHEN: the last half hour before the cash close, a published schedule fixed ex ante. **Met.**
- WHY it persists: the demand is mandate-inelastic. **Contested:** the in-house class finding says Baltussen-class momentum is "statistically ABSENT on modern MNQ … OOS edge decayed negative", corroborating the published post-2021 decay.
- HOW it dies: leveraged-ETF AUM (public) and dealer net gamma (paid or unobserved), watched with the edge CUSUM. **Partly met:** gamma is not on the admitted feed.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Baltussen, Da, Lammers, Martens, JFE 142(1) 2021, 377–403, Table B1 Panel B (author PDF academicweb.nd.edu/~zda/intramom.pdf, 2026-11-04) | **YM** (Dow futures), 1997-10-08→2020-05-01, 5,639 obs (Table A1) | rROD (rest of day) → last half hour: β 5.02, NW t **4.12**, R² 2.20%, R²OOS 2.18%; first half hour: β 6.07, t 3.28, R² 1.34% | Parent mini of the same index (YM→MYM); not cross-index |
| Gao, Han, Li, Zhou, "Intraday Momentum…" working paper, Dec 2015 version (JFE 129(2) 2018, 394–414), Table 12 Panel A (mql5-hosted PDF, 2026-11-04) | **DIA** ETF (Dow), inception→2013-12-31 | timing strategy Avg Ret 3.46% p.a. (NW t 2.35), Std 5.69% p.a.; INS R² 1.16%, OOS R² 1.03% | Same index, cash ETF; working-paper numbers, not the final JFE table |
| In-house D5 / D5-RECOST, MNQ (`intraday-momentum` class finding; NQ.md N3) | MNQ, post-2021 | OOS gross Sharpe +0.88→−0.13 | Sibling index; prior only |
- Decay haircut: **58%** (McLean–Pontiff 2016, JF 71(1): "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication"). I chose the larger figure because the in-house sibling shows full decay on MNQ.
- Screen figure: **δ/σ = 4.12/√5,639 = 0.0549** (t-scaled conservative central, the harvest §4 D5 precedent; the R²-derived √0.022 = 0.148 is optimistic). Haircut: 0.0549 × 0.42 = **0.0231**. Corroboration from DIA: (3.46/252)/(5.69/√252) = 0.038, assuming 252 days per year. The pinned screen figure is 0.0231.

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell MYM intraday-momentum; echo "exit=$?"
=== MYM x intraday-momentum ===
ledger: ops/instruments/MYM.md
venue: NOT TRADABLE at the live firm — AUTHORIZED-but-venue-less incumbent (Striker DJ30 MYM edition); no live book to correlate new work against — check venue_note before book-correlation gate.
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MYM): Baltussen-class intraday momentum is statistically ABSENT on modern MNQ — the cost-geometry thesis was real (hurdle fell 11.06→3.01 bp) but the OOS edge decayed negative (gross Sharpe +0.88→−0.13), corroborating the published post-2021 decay and an external 14-signal-family falsification (arXiv 2605.04004). [NQ.md N3](NQ.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 6.57 bp/event (4x Tradeify hurdle) — VERIFY at #M6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Not a barren instrument — the incumbent locked leg is profitable here; one narrow continuation expression failed. [#M1]
exit=1
```
- Register hits: none for MYM × intraday-momentum. Adjacent entries: D5 (NQ/MNQ, Stage-2 cost law; D5-RECOST OOS decayed) is a counted in-domain closure of the raised bar; its manifest notes "DJ30/MYM dropped". The leveraged-ETF end-of-day rebalance flow on ES/NQ is rejected under the free-data domain bar (2026-07-24). Its re-proposal bar says "NOT … a different index/leverage tier", and this cell rides the same leveraged-ETF limb on a different index. The end-of-day adversity raised bar (2026-08-02) records MYM's final-block drift t = −2.18, unremarkable after multiplicity; that is an unconditional measure, not this conditional sign. The ledger's AMBIGUOUS-PARKED cells (range, gap, day-range state) are conditioner-role and unaffected.
- Domain bars: `index-intraday-ohlcv-directional-timing-2026-07-21` **binds** (single index future, OHLCV, directional, flat-by-close). **Route 1 is claimed and contested.** The closing window and the rest-of-day sign are causally named a priori by Baltussen (ADR 2026-08-10 §2-B), but the bar text calls "a different index" the exhausted move, and D5 is this mechanism on NQ. Route 1 holds only if the coordinator rules that MYM's own published YM cohort makes this a within-instrument timing claim, not an index swap. Any extra selectivity (for example, only large-|rest-of-day| days, the mechanism's hedging-intensity proxy) is a further K axis. **Route 2 not claimed** (OHLCV only; gamma or flow data is paid and gated). **Route 3 not claimed** (no evidence it beats ORB-MNQ net).
- Family K bank (Req 3 disclosure): as in r2-mym-overnight-drift. By manifest read it is 7 (`st_eh` 1 + `mymdd_1` 5 + `q_txg1_striker_nas100_mym` 1); the ledger says 6; unreconciled. Disclosure only. MYM has 2 lifetime builder looks.

## Venue legality at Bulenox
- Native route: Rithmic third-party API, "$100 monthly fee" (envelope §4, 2026-10-02). The NT8-over-Rithmic native route is **unverified**.
- Product offered: MYM at 0.61/side (Rates PDF "Updated Aug/11/2026", venue register §F, 2026-11-01).
- Flat-by: 15:59 CT = 16:59 ET (help-center/qualification, envelope §4, 2026-10-02). The cash close sits about an hour earlier. MFFU's "4:10 PM EST" auto-liquidation leaves about 10 minutes (envelope §4 MFFU row), which is tight.
- News: "News trading allowed" (envelope §4, 2026-10-02).
- Hold: the closing half hour, intraday.
- Cross-firm hedging / product group: **binding conflict.** Tradeify ESA §6.7(c),(i) and help article 10495868 ban opposing Equity Index positions across all of the trader's accounts, external firms included. A same-group, different-symbol hedge (MYM vs. MNQ) is "monitored separately … reviewed by our risk team" with no threshold (envelope §4a, re-read 2026-10-02). This cell is two-sided and holds into the cash close, the window in which ORB-MNQ can still be open. Its short side would breach Tradeify whenever ORB-MNQ is long. The MNQ ledger records the ORB-MNQ reconstruction baseline as long-only (MNQ.md 2026-08-25); the current Tradeify native edition's side is **not verified here**. Compliant expressions are: (a) long-only, which halves events and is not the published two-sided cohort; or (b) a cross-firm sign guard, which cannot be expressed natively across firms and would need agent coordination (T2 / Rule 4 issue). Either expression changes the screen.
- Why not Tradeify: the same 10-30 one-strategy-per-firm ruling as the sibling dossier. At Tradeify the same-group rule applies within and across accounts too, so moving firms does not remove the conflict.

## Distinctness
- vs index ORB book: the window is the cash close rather than the open, and the mechanism is hedging-demand continuation rather than opening-range break. **Holding windows can overlap** (ORB holds to the close). Both are intraday directional index trades in one product group, so P&L correlation with ORB-MNQ is plausible and unmeasured.
- vs withdrawn Striker DJ30 MYM editions: Striker is a long-only pyramided trend-follower. This cell also rides intraday direction, so the overlap in mechanism family is real. The locked windows are private and not read. Distinctness rests on the fixed closing window, the single half-hour hold, no pyramid and two sides, and it is weaker than for the overnight cell.
- vs other R2 dossiers: Same mechanism (Baltussen-class intraday momentum) as r2-m2k-imom, and the mechanism D5 killed on MNQ: not distinct from r2-m2k-imom; at most one of them runs. Its late-session hold overlaps the ORB book's window in the same product group, so its short side needs sign coordination. Differs from the non-index dossiers in instrument and product group.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: N = 1,492 dev sessions × 1/session = 1,492 (two-sided expression; long-only ≈ half, no cited fraction). Power = Φ(√1,492 × 0.0231 − 1.96) = Φ(−1.07) = **0.14** at the screen figure. Unhaircut 0.0549 gives Φ(0.16) = 0.56. Break-even δ/σ = 0.051, i.e. it fails Req 4 at any haircut above about 7.6%. DIA corroboration at 58%: 0.09.
- Cost and entry-slip sensitivity (M-16, printed only): Bulenox RT $1.22 = **2.44 ticks** (1 pt = $0.50). Tradeify 3.64, MFFU 3.80, BluSky Rithmic 2.00. Price terms come from DIA only (Gao, 1998–2013, ETF gross): 3.46%/252 = 1.37 bp/event. At illustrative L = 40,003.59 (DJIA 2024-05-17 close), that is ≈5.5 ticks gross, leaving ≈3.0 ticks for total entry+exit slip at Bulenox. At the 58% haircut, 0.58 bp ≈ 2.3 ticks: **already below the 2.44-tick commission with zero slip.** This is a market entry into the close, so slip is a market-impact charge, not a stop-through.
- Barrier feasibility: pending atlas (sibling session).
