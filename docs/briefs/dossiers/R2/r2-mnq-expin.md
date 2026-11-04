# r2-mnq-expin: MNQ × `expiry-atm-strike-pinning` × Bulenox

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: MNQ · Mechanism: `expiry-atm-strike-pinning` (NEW; nearest existing `expiry-oi-strike-convergence`, which keys on the max-OI strike; this variant keys on the at-the-money strike of the published strike grid, so it needs price only, no OI feed) · Provisional firm: **Bulenox** (deviates from D10's index→Tradeify; competes with `r2-mnq-ovndrift` for the same slot under the one-strategy-per-firm ruling) · Session: US afternoon of an E-mini Nasdaq-100 option expiry day, flat at or before the US cash close
- Event frequency: E-mini Nasdaq-100 options expire every weekday since Tuesday/Thursday weeklies launched "on October 3" 2022, complementing "the existing Monday, Wednesday and Friday Weeklies" (Mondovisione reprint of the CME release, 2022-09-08). Daily inside that regime; Friday-only (or M/W/F, start dates unverified) before it.

## Mechanism (harvest Req 1, path 1a)
- WHO pays: option market makers delta-hedging short-dated positions; as expiry nears, hedge rebalancing (plus investor resale/early exercise) pulls the future toward the strike. Golez & Jackwerth: "driven by the interplay of market makers' rebalancing of delta hedges due to the time decay of those hedges as well as in response to reselling (and early exercise) of in the money options by individual investors". Constraint (hedging requirement / expiry mechanics), clause (i) admissible per the existing class.
- WHEN: expiry days, final hours before the option cut; G-J: much of the shift is "solely within the last 30 min of trading".
- WHY it persists: hedging is mandate-inelastic; capacity per expiry is small (G-J lower bound $115M notional per expiry on ES, monthly).
- HOW it dies: observable = near-ATM open interest / short-dated option volume share; sign flip (anti-pinning) shows in the realized distance-to-strike distribution.
- **Clause weakness, load-bearing:** the sign is not entailed. G-J find pinning on serial futures-option expiries but "anti cross pinning" before S&P 500 *index* option expiry, and the Avellaneda–Lipkin model they cite predicts anti-pinning where they found pinning. On NQ, futures options, NDX index options and QQQ options now all expire daily, so which force dominates is unknown ex ante — the class's own rejected sibling ("constraint carries neither sign", MECHANISMS.md) is close.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Golez & Jackwerth, JFE 106(3) 2012, 566–585, open copy https://kops.uni-konstanz.de/bitstreams/b9492112-cab3-4217-a7d0-d2c4f5ba7825/download (2026-11-04) | ES futures, serial (monthly, non-quarterly) option expiries, Nov 1992–Nov 2009 | "a shift of at least 11.00 bps from Thursday PM to expiration Friday PM" (§ on Ni et al. method) — a lower bound on a distributional shift in absolute returns, **not a signed mean; no σ** | **Yes (ES→MNQ)**, and monthly not daily |
| In-house MSL-S4 Explore-confirm (MECHANISMS.md `expiry-oi-strike-convergence`) | MGC, weekly+monthly expiries, 75 cycles | real displacement reduction **negative** (divergence), 42.8th pct of surrogate null, FLIP FAIL | Different instrument and strike rule |

- Decay haircut: McLean & Pontiff (JF 71(1) 2016): "58% lower post-publication" — would apply, but there is no target δ to haircut. Daily NQ expiries post-date the cohort entirely (structural change, not just decay).
- Screen figure: **UNSCREENABLE** — no NQ/MNQ cohort; G-J gives no signed δ/σ even on ES. Supplier: a K-charged δ-extraction probe on native MNQ expiry days (signed move toward the nearest grid strike over the declared late window vs matched non-expiry control sessions), with the strike grid sourced from the CME contract spec (Rule 17).

## Prior consult (advisory, Rule 26)
```text
===== expiry-atm-strike-pinning
FATAL: unknown mechanism 'expiry-atm-strike-pinning'. Nearest: 'expiry-oi-strike-convergence'. Declare it NEW in MECHANISMS.md.
exit=2
===== expiry-oi-strike-convergence  (nearest)
=== MNQ x expiry-oi-strike-convergence ===
ledger: ops/instruments/MNQ.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MNQ): G0 frozen on operator B4 GO 2026-08-21; Explore-confirm (charter step 5a) **deferred by explicit operator override** at freeze (no Databento/market-data access in the sourcing session's environment) rather than scored — Pine authored CC-solo directly off the frozen construct, with the operator's own TV backtest as the first empirical evidence instead of a pre-Pine Explore score. This is a disclosed deviation from the charter's default step ordering, not a silent skip. [`STAGE1`](../../../../lab/analysis/c1/msl_s4_mgc_2026-08/STAGE1.md) · [`PREREG_G0`](../../../../lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md) · [`RUNBOOK`](../../../../lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md).
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
cost hurdle: 3.01 bp/session (4x modern-era MNQ hurdle (D5-RECOST-1)) — VERIFY at #N6
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: ORB-MNQ-1's fills are known-good - the cost fragility is a commission sensitivity, not a fill-mechanics defect (median intrabar penetration 81 ticks entries / 64 ticks stops, 0.7% shallow-touch, zero non-traded levels). [#N2]
prior: Both exit-redesign directions are pre-killed by an order-free counterfactual: tighter stops lose 0.03-0.06R (winners need the full-range stop) and no fixed profit target beats baseline - the 0.50R median close give-back is real but unharvestable. [#N3]
exit=1
```
- Tool gap: the consult prints only the stale first class finding; the later `AMBIGUOUS-HOLD` Explore result (wrong sign, FLIP FAIL, MGC) sits in a non-"Class finding" bullet and does not print. Disclosed here by hand.
- Register hits: Q-ORB-FRIDAY-1 G3 "OPEX-flow mechanism FALSIFIED (triple-witching weakest)" (a gate on ORB, not this construct); MYM-3FPS-1 third-Friday settlement reversal DEAD with bar "NOT … MNQ rescue" (different mechanism: settlement reversal, not strike pinning — but a reviewer may read it as adjacent); dealer-gamma GEX regime gate on NAS100 DEAD (sign-of-gamma; this cell must not use gamma sign).
- Domain bars: **Route 1 claimed**: expiry hedging mechanics are outside the mapped price / cross-instrument / hold-time levers; the moment (expiry day, late window) is named a priori by the cohort (ADR 2026-08-10 §2-B(1)); each window/strike-rule choice charges K (§2-B(2)). **Route 2 not claimed**: an OI or options-flow expression would be a different modality but needs a non-admitted feed (Rule 18) and, at Tradeify, hits ESA §6.3 "Trading based on an external or delayed data feed is not allowed". **Route 3 not claimable.** EOD-adversity bar (final RTH block): a late-session window is inside its scope if the card's claim is framed as final-block anomaly; frame it as expiry-conditional only, and expect a reviewer to ask for the multiplicity test that bar names.
- Dead/parked MNQ cells: intraday-momentum DEAD (D5, Baltussen hedging-demand momentum) is the opposite-sign dealer-hedging story in the same late window — strongest adjacent prior; opening-pressure, ict-liquidity, order-flow-depth DEAD unrelated; overnight-range-transmission / daily-range-state-persistence / intraday-bar-volume-regime PARKED not to be used as gates (laundering).
- Family K bank (Req 3 disclosure): `K_banked(MNQ) = 22` (ledger, 2026-08-24; re-read manifests). Builder lifetime looks MNQ = 2.

## Venue legality at Bulenox
- Native route: Rithmic third-party API, "$100 monthly fee" (envelope §4, 2026-10-02) · Product offered: index micros, $0.61/side (`core/firm_rules.py:140`) · Flat-by: 16:59 ET ("3:59 PM (CT)", envelope §4, 2026-10-02); E-mini NQ weekly options' termination time is reported only in a search summary of CME SER-9050, **not opened (403/JSON)** — verify before the card · News: allowed (envelope) · Hold: intraday only.
- Cross-firm hedging / product group: **binding conflict.** The window overlaps ORB-MNQ's cash-open-to-close hold, and ORB trades both sides. Tradeify ESA §6.7(c),(i) bars opposite positions between a Tradeify account and any other firm's account (deep-dive DRAFT item 5); Tradeify's Equity Index group includes MNQ/NQ/ES/MYM (envelope §4a). The card would have to be sign-constrained against the live ORB position (skip or flatten when opposite), coupling two strategies at two firms. At Tradeify itself the same rule binds within and across accounts.

## Distinctness
- vs index ORB book: different mechanism (mean reversion toward a strike vs breakout continuation) and window (expiry-day afternoon vs cash open), but **holding-time overlap** with ORB on most days and same product group — weaker distinctness than `r2-mnq-ovndrift`.
- vs other R2 dossiers: Distinct in mechanism (expiry pinning) from every other dossier. Shares its **instrument** with the index ORB book and overlaps its US afternoon hold, so it fails the working test's instrument limb and needs sign coordination with ORB. Same product group as the MYM and M2K dossiers.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **1,492**: window 2019-05-06..2026-11-02 ≈ 1,870 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.676 | 0.664 | 0.698 | yes |
  | 2 (the reserve look) | 0.890 | 0.461 | 0.500 | yes, at the boundary |
  | 3 | 1.027 | 0.334 | 0.370 | no |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 2 looks (generation note §11).
- Power at expected event count: **not computable (UNSCREENABLE)**. Expected N in development (calendar estimate, not data): the ~1,492-session window from 2019-05 ends near 2025-04; daily-expiry regime from 2022-10-03 ≈ 2.5 years ≈ ~640 sessions daily, plus earlier Friday/MWF expiries (dates unverified). A pooled-regime card mixes a structural break.
- Cost and entry-slip sensitivity (M-16, printed only): round trip at Bulenox 2.44 ticks commission + 2 ticks modelled slip = **4.44 ticks**; Tradeify 5.64 ticks. Entry would be a market/limit toward the strike, not a stop. Slip that consumes the effect: **not computable** (no signed δ).
- Barrier feasibility: pending atlas (sibling session).
