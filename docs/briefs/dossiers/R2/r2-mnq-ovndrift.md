# r2-mnq-ovndrift: MNQ × `overnight-drift-inventory-reversal` × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MNQ · Mechanism: `overnight-drift-inventory-reversal` (NEW; nearest existing `event-window-reversal`, then `overnight-range-transmission`) · Provisional firm: **Bulenox** (deviates from D10's index→Tradeify default; reasons under Venue legality) · Session: Globex overnight, a long held across the European cash open, flat long before the US cash open
- Event frequency: two cohort-declared forms. (a) Unconditional: every session. (b) Cohort "buy-the-dip" form (SR917 Table IX, `RSV_{t−1} close < 0`): "half the trading days" (SR917 §Trading strategies, verbatim below). Card picks one form at G0; the other is a second K.

## Mechanism (harvest Req 1, path 1a)
- WHO pays: participants who demand immediacy at the US close and leave an order imbalance; risk-averse market makers absorb it and are paid to unwind it when European liquidity arrives. SR917: "the pattern is most likely driven by the overnight resolution of order imbalances arising from the end of the preceding U.S. trading day". Constraint: dealer inventory/VaR capacity ("demand shock asymmetry arises when dealers face value-at-risk (VaR)" constraints, SR917 §1). Clause (i) is arguable rather than clean: the payer is an immediacy demander (close-benchmarked execution, hedgers: "the futures market is traded as a hedging instrument for the underlying"), compensated by execution at the close.
- WHEN: declared by the cohort before any data: the hour before the European cash open, every session; sign from the prior US close imbalance (form b).
- WHY it persists: thin overnight liquidity, capacity small relative to institutional tickets; dealer risk-bearing capacity time-varying. Weak: the authors' own 2026 follow-up says the window "has averaged close to zero since 2021".
- HOW it dies: dispersion of end-of-day relative signed volume (RSV). Authors (2026): std of end-of-day RSV "fell from 6.5% to 2.9%", "the only input to the pricing equation that has shifted substantially". **This observable has already fired on ES.**

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Boyarchenko, Larsen, Whelan, NY Fed SR917 (RFS 36(9) 2023, 3502–3547), https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr917.pdf (2026-11-04) | ES (E-mini S&P 500), 1998–2020, mid quotes | European-open hour: "1.5 basis points per hour per day", t = 7.1 (Table I) | **Yes (ES→MNQ)** |
| Same, Table IX (2004–2020) | ES, BtD long only after negative closing RSV | Sharpe "1.8" gross, "1.1" post-cost (text p. 28) | **Yes** |
| Boyarchenko, Larsen, Whelan, "The Disappearing Overnight Drift", Liberty Street Economics, 2026-07-01, https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ (2026-11-04) | ES, 2021–2025 (1,245 days); NQ/YM named, no figures | "averaged close to zero since 2021"; "The same pattern holds in the E-mini Nasdaq-100 (NQ) and E-mini Dow Jones (YM) contracts" (pattern = the pre-2021 pattern; no NQ number) | n/a (ES); NQ qualitative only |
| In-house H-OD-1 (ES IS), `docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md` closure row | ES, IS era | +1.444 bp mean gross (Stage-2) | Yes |

- Arithmetic (ES, transplant, illustrative only — not a screen figure): unconditional δ/σ = t/√N = 7.1/√5,691 = 0.094 (in-house prereg used 0.093). BtD: with zeros on non-signal days (SR917 fn 36–37: volatility from daily data; "large number of zero returns"), per-active-day δ/σ ≈ SR_ann / (√252·√0.5) = 1.8/11.22 = **0.160 gross**, 1.1/11.22 = **0.098 net**.
- Decay haircut: McLean & Pontiff (JF 71(1) 2016) "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication" → 58% conservative central. But the authors' own post-publication observation (≈0, 2021–25, ES) overrides it for the unconditional form: effective haircut ≈ 100%. For form (b) no post-2020 figure is published.
- Screen figure: **UNSCREENABLE** — no MNQ/NQ cohort δ (SR917 reports ES only; the 2026 post gives no NQ number). Already recorded in-house: "any MNQ/NQ (or MYM) expression is `UNSCREENABLE:nq-native-delta-sigma-not-extracted`" (H-OD-1 prereg line 27). Supplier: a K-charged δ-extraction probe on native MNQ, restricted to the cohort-declared window and sign, post-2020 only, OR an author NQ table (ask/OA appendix).

## Prior consult (advisory, Rule 26)
```text
===== overnight-drift-inventory-reversal
FATAL: unknown mechanism 'overnight-drift-inventory-reversal'. Declare it NEW in MECHANISMS.md.
exit=2
===== event-window-reversal  (nearest)
=== MNQ x event-window-reversal ===
ledger: ops/instruments/MNQ.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MNQ): The settlement limb does not reproduce at useful magnitude — MYM's third-Friday derivative-settlement reversal cleared exact-coverage sourcing (84/87, 96.6% PASS) but both power legs sit below the 0.2139 floor and the tradable limb is negative in 2024–2026. [MYM.md M5](MYM.md)
class finding (mechanism-wide, not specific to MNQ): *Auction limb (2026-07-27) — dies at the PROCUREMENT GATE, not on edge, on ANY instrument.* Closing-auction/MOC-imbalance is reject-at-bar for an instrument-independent reason, hence recorded as a class finding rather than a cell. [... full text in _consults.txt ...] Cheapest re-open is free: a published cohort δ for imbalance → index-futures response, citable without procurement. [F1 ruling](../../docs/briefs/programs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 3.01 bp/session (4x modern-era MNQ hurdle (D5-RECOST-1)) — VERIFY at #N6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: ORB-MNQ-1's fills are known-good - the cost fragility is a commission sensitivity, not a fill-mechanics defect (median intrabar penetration 81 ticks entries / 64 ticks stops, 0.7% shallow-touch, zero non-traded levels). [#N2]
prior: Both exit-redesign directions are pre-killed by an order-free counterfactual: tighter stops lose 0.03-0.06R (winners need the full-range stop) and no fixed profit target beats baseline - the 0.50R median close give-back is real but unharvestable. [#N3]
exit=1
===== overnight-range-transmission  (second nearest)
=== MNQ x overnight-range-transmission ===
verdict: AMBIGUOUS-PARKED (2026-08-30)
  source: ../../docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md
  BLOCKING — a parked concept holds this cell and shares the instrument's anti-SNAG budget; address it (and any decision date) in the pre-registration.
[class findings, bar, hurdle, priors as above — full text in _consults.txt]
exit=1
```
(Full unabridged output: [sources/consults-MNQ.txt](sources/consults-MNQ.txt).)
- Register hits: H-OD-1 (ES) closed Stage-2 cost-law KILL 2026-07-16, mechanism CONFIRMED-IS; its prereg forbids "Any MNQ/NQ/MYM expression — the unburned-K lure" (advisory now; Req 5 cost law deleted 2026-10-24 removes the kill basis but not the UNSCREENABLE). MOC-imbalance procurement gate (event-window-reversal auction limb) is adjacent: form (b)'s conditioner is a closing imbalance. LETF EOD-flow free-data bar not hit (different flow).
- Domain bars: **scope** of `index-intraday-ohlcv-directional-timing-2026-07-21` says it "Does not cover … overnight mechanisms (H-OD-1 — venue-walled)" — this cell is that excluded class; the tool still prints the bar, so route by route: **Route 1 claimed**: inventory-risk overnight resolution is outside the mapped price / cross-instrument / hold-time levers; form (b)'s moment criterion is causally named a priori by the cohort (ADR 2026-08-10 §2-B(1)), charges K (§2-B(2)). **Route 2 not claimed**: the cohort conditioner is signed volume (order flow), which the admitted TV OHLCV feed lacks (Rule 18); a price proxy (prior-close sell-off) is a new expression, not the cohort's. **Route 3 not claimable** (no evidence vs ORB-MNQ-1). EOD-adversity bar: not reached (no claim about the final RTH block).
- Dead/parked MNQ cells: intraday-momentum DEAD (D5) is late-session RTH continuation, different window and sign; opening-pressure DEAD is the US open; overnight-range-transmission PARKED is a range-magnitude conditioner — using overnight range as a gate here would launder that parked cell (forbidden move for the card); bar-closing-location-autocorrelation DEAD binds any close-location proxy for "sell-off" (do not use one); ict-liquidity / order-flow-depth DEAD unrelated.
- Family K bank (Req 3 disclosure): `K_banked(MNQ) = 22` (ledger last reconciled 2026-08-24; re-read `discovery_manifests/` at admission). Builder lifetime looks MNQ = 2 (generation DRAFT §11).

## Venue legality at Bulenox
- Native route: algos via Rithmic third-party API, "$100 monthly fee" (envelope §4, re-verified 2026-10-02) · Product offered: index micros, $0.61/side (`core/firm_rules.py:140`) · Flat-by: "All positions must be closed by 3:59 PM (CT)" = 16:59 ET (envelope §4, 2026-10-02); whether a hold across the European open counts as intraday inside Bulenox's trading day is **not verified** (gap) · News: "News trading allowed" (envelope, 2026-10-02) · Hold: no overnight/weekend holds (microstructure study §1.1); window ends before the US open · Cross-firm hedging / product group: Tradeify ESA §6.7(c),(i) bars opposing positions between a Tradeify account and "any proprietary trading firm" account (deep-dive DRAFT item 5, 2026-11-01). Cell is long-only in a window disjoint from ORB-MNQ's cash-open-to-close hold, so it cannot oppose ORB by construction. Tradeify §6.6 ("using it across multiple firms is against Tradeify's policy", routes note 2026-10-13) binds the ORB strategy, not a distinct one.
- Why not Tradeify: D10 assigns Tradeify the ORB index book and the 10-30 ruling is one strategy per firm; a second MNQ strategy at Tradeify also adds a same-group, same-account exposure. Tradeify itself would be legal on clock (session 18:00 → 16:45 ET, envelope §4) if Joshua wants it there.

## Distinctness
- vs index ORB book: different session (European open vs US cash open), different mechanism (timed inventory reversal, no breakout trigger), long-only, no clock overlap.
- vs other R2 dossiers: Same mechanism and source (Boyarchenko–Larsen–Whelan overnight drift) as r2-mym-overnight-drift and r2-m2k-ondrift, in the same Tradeify product group (Equity Index): the three are **not distinct from one another**, so at most one can run in R2 (D9: each card a different mechanism). It also shares its **instrument** with the index ORB book, so it fails the working distinctness test's instrument limb (generation note §10.2 open question 2). Differs from every non-index dossier in instrument, product group and mechanism.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: **not computable (UNSCREENABLE)**. Illustrative ES transplant only (inadmissible as screen): form (b) N ≈ 1,492 × 0.5 = 746; at 0.160 gross × (1 − 0.58) = 0.067 → Φ(√746·0.067 − 1.96) = Φ(−0.13) = **0.45**; at net 0.098 × 0.42 = 0.041 → **0.20**. Unconditional N = 1,492 at 0.094 × 0.42 → 0.33; at the authors' post-2021 "close to zero" → ≈ 0.03. Most of MNQ's development window (2019-05 onward) lies inside the faded era.
- Cost and entry-slip sensitivity (M-16, printed only): round trip at Bulenox = $1.22 commission = 2.44 ticks, + 1 tick/side modelled slip (`SLIPPAGE_TICKS_PER_SIDE = 1.0`, unmeasured) = **4.44 ticks**; at Tradeify 3.64 + 2 = 5.64 ticks. Entry is a timed order, not a stop, so M-16's stop-slip anchor applies weakly. Slip that consumes the haircut effect: **not computable** (no MNQ δ); conversion when one exists: ticks = δ_bp × P / 2,500 at price P.
- Barrier feasibility: pending atlas (sibling session).
