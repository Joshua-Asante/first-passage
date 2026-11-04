# r2-mgc-cgb: MGC × compression-gated-breakout × BluSky

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MGC (COMEX Micro Gold) · Mechanism: `compression-gated-breakout` (existing; untested on MGC; XAUUSD cell AMBIGUOUS-PARKED) · Provisional firm: BluSky Premium (D10 proposed mapping, not decided) · Session: compression measured over the pre-COMEX window (London morning into the US pre-open); break traded in the COMEX day session; flat well before the venue flat-by. Window must not be the US equity cash open (keeps it off ORB).
- Event frequency: ≤1 per session, only on sessions the compression gate admits. Gate-pass fraction: **unpublished, unknown at K = 0** (it is a fraction of 2,325 by construction).

## Mechanism (harvest Req 1, path 1a | 1b)
- WHO pays: none named: path 1b. (Volatility-clustering / range mean reversion is a statistical regularity, not a mandated counterparty.)
- WHEN: compression state resolves into a directional break (state trigger, declarable ex ante).
- WHY it persists: no capacity/awkwardness argument available.
- HOW it dies: no constraint observable; edge CUSUM only.
- 1b limbs:
  - (i) ≥3 decades: **not met** for a directional compression break on gold. Volatility clustering itself on COMEX gold is long-documented (Cai, Cheung & Wong 2001, *JFM* 21(3):257–278, intraday volatility of COMEX gold; abstract-level via search only) but that is magnitude, not direction.
  - (ii) ≥3 cohorts: **not met** (no peer-reviewed gold compression-breakout cohort found; NR7/Crabel material is practitioner).
  - (iii) replication ≥10 y: **not met.**
  - (iv) no sign reversal: **unknown**; MNQ CON-2 gross-positive/net-negative, HTF-filter variant FALSIFIED.
- **Req 1: FAIL on both paths at K = 0.** Admissible only via the no-counterparty statistical channel (declared K ≤ 3).

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Web search for gold-futures compression / NR7 breakout cohort (2026-11-04) | — | none found; Quantified Strategies GLD post paywalled, no figures seen | — |
| XAUUSD CGB-001 (in-repo, `ops/instruments/XAUUSD.md` F4) | Pepperstone XAUUSD CFD, Guardian panel N=203, 2022–2026 | short payoff 100% censored (0/203 reach FE≥1.5R); inconclusive | Spot CFD sibling on a retired feed: prior only, not δ |
| MNQ CON-2 (in-repo, MECHANISMS.md) | MNQ dense-1m | gross ~+0.9–1.0 pt, net-negative at Tradeify RT | Cross-instrument: inadmissible |
- Decay haircut: n/a (no admissible δ); McLean & Pontiff 2016 58% would apply to any published δ.
- Screen figure: **UNSCREENABLE.** Supply route: in-house δ-extraction on the MGC dev window (one builder look, K ≥ 1) with a discriminator on the mechanism's own observable (post-compression range expansion vs a same-day time-placebo per M-17), so a payoff fail is read as `EXPRESSION-FAIL` vs `MARKET-NULL`.

## Prior consult (advisory, Rule 26)
```text
=== MGC x compression-gated-breakout ===
ledger: ops/instruments/MGC.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MGC): A compression-gated short-primary construct on XAUUSD is not killed by the cheap tests, but the intended trailing-short payoff is 100% in the censored region (0/203 trades reach short FE≥1.5R) — a design-test mismatch that blocked a build decision pending a bar-level backtest. [XAUUSD.md F4](../../../../ops/instruments/XAUUSD.md)
class finding (mechanism-wide, not specific to MGC): Dense-1m MNQ compression→expansion with-break at G=10 session-flat (`Q-TNEC-CON-2`) is gross-positive (~+0.9–1.0 pt) but net-negative under Tradeify RT 1.41 (`AMBIGUOUS-HOLD` non-promotable). An HTF-5m-bias → LTF-1m directed with-break filter on the same family is `FALSIFIED` at the parent cheap falsifier (both arms CI entirely &lt;0). [MNQ.md](../../../../ops/instruments/MNQ.md)
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Third-leg E-K elimination is void as a gate after K-bank ADR; large disclosed bank remains a Req-3 fact, not an inherited kill. DISC-CAMP-0 history is disclosure, not re-litigation. [#G1]
exit=1
```
Nearest-id consult also run: `htf-compression-breakout-5m` → untested on MGC; class finding MNQ CON-3 AMBIGUOUS-HOLD; same binding bar; exit=1.
- Register hits: (1) `free-data-5th-leg` SNAG-CLOSED 2026-07-01 — as in r2-mgc-pdhpdl (prior MGC cards cleared it via MSL R-FRAMING §2.1; MSL closed; coordinator to rule; advisory). (2) **`daily-range-state-persistence` × MGC DEAD** (GC parent, corrected battery: NULL, obs at the 8.4th pct of the linear-ACF band). Adjacent: that tested top-quintile range → next-day range; this cell conditions on low range → expansion + direction. Re-proposal bar: "the corrected battery + a different construction or longer panel" — this is a different construction, and any range-expansion discriminator here **must use the IAAFT corrected null**, not a block-shuffle placebo (MGC.md G4 audit). (3) London fade FALSIFIED — different (fade at London extreme); bar "different reference class / direction / TF" met. (4) XAUUSD CGB-001 AMBIGUOUS-PARKED (spot panel deleted) — this cell reopens it on the venue-legal contract; parked re-entry needs its own pre-registration. (5) MGC.md 2026-08-25 informal ~46-cell MGC 15m survey, all NULL, families unrecorded — **possible overlap, unverifiable**.
- Domain bars: index-intraday OHLCV raised bar does not apply (non-index).
- Family K bank (Req 3 disclosure): GC/MGC **3,177** (`disccamp0_gc_2010_18.json`). Disclosure only. MGC builder looks: 4 lifetime (§11).

## Venue legality at BluSky
- Native route: full automation welcomed; NinjaScript on Tradovate/NT or Rithmic-class rails; mirroring banned (envelope §4 BluSky row, 17115915 / 12069208, 2026-10-02). · Product offered: MGC (17115915 table, 2026-10-02). · Flat-by: "We recommend closing all trades before 4:45PM EST" (12434059 dated 2026-08-12, re-verified 2026-10-02). · News: "at your own risk", does not fail eval (12434059). · Hold: intraday only (`weekend_holds: False`). · Cross-firm hedging / product group: "Hedging is not allowed in Futures Trading" (12434059; scope unclear, register A1.4); BluSky ToS bot / cross-firm clauses unread; Tradeify ESA §6.7(c),(i) bites only with an opposing Tradeify Metals position (none). Sign-constrain if any other Metals leg is co-accounted (MGC.md W1).
- Rope: BluSky_Premium_100K $3,000 EOD trail — **W5's division transfers (34% at 2026 vol on W5's reference stop)**. A stop at the opposite compression extreme is narrower than a prior-day range by construction, so this cell's 1-micro risk share is likely below W5's figure [INF; atlas to measure].

## Distinctness
- vs index ORB book: Metals vs Equity Index group; trigger is a compression state, not the opening range; window precedes and is not anchored to the US equity cash open. Risk: if compression were measured on the COMEX open's first bars it collapses toward ORB — registration must anchor it pre-open.
- vs other R2 dossiers: The only Metals-group dossier, so it differs from every other R2 dossier in instrument and product group. Mechanism (compression-gated breakout) is shared with no other dossier; it is a stop-entry break like ORB, so its compression window must be anchored before the COMEX open to stay distinct from an opening-range construct.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count: **not computable (UNSCREENABLE).** Break-even δ/σ for power 0.50: 0.041 if every session qualified (N = 2,325); 0.057 at half; 0.081 at a quarter (illustrative grid). Gate filtering lowers N, so the break-even rises.
- Cost and entry-slip sensitivity (M-16, printed only): same as r2-mgc-pdhpdl — MGC $1.00/tick; BluSky proxy $1.20/side (not venue-published) = 2.4 ticks RT commission, +2 ticks builder slippage → **≈ 4.4 ticks RT** (3.0–4.6 across BluSky's published rails). Slip ticks to consume δ: not computable. A narrower compression stop makes a fixed tick cost a larger share of R, so the M-16 slip sweep is the first test.
- Barrier feasibility: pending atlas (sibling session).
