# r2-m6e-asialdn: M6E × asia-range-london-breakout-continuation × MFFU

Status: R2 dossier (Part A §A2–§A3, tasks T2–T3) · 2026-11-04 · K = 0 (no data read) · decides nothing; generation never blesses (Rule 25)

## Cell
- Instrument: M6E. There is no repo ledger yet; EURUSD.md, M6A.md and 6J.md are the nearest priors, labelled. · Mechanism: `asia-range-london-breakout-continuation` (NEW; nearest existing `prior-session-breakout-continuation`, then `opening-range-breakout`). · Provisional firm: MFFU Rapid (D10 proposed mapping, not decided). · Session: the reference range is formed in the Asia (Tokyo) session. The rule enters on the first break of that range after the London open, keeps the continuation through the London morning, and is flat by the US morning.
- Why NEW: `prior-session-breakout-continuation` takes its reference from the *full* prior native session. Swapping in an Asia sub-session window changes the volatility regime and the event population. That is the same load-bearing split rule MECHANISMS.md applies to `overnight-range-failed-extension-fade`. It also targets the DL-2 failure mode directly: a reference window wider than the move reachable before force-flat.
- Event frequency: at most one per session (first valid break, k=1). The fraction of sessions with a break is **unknown** (no published figure; it would need data).

## Mechanism (harvest Req 1, path 1b)
- WHO pays: none named, so this is path 1b. The intuition is that London-open order flow resolves overnight positioning. That is a preference/behavioural story and inadmissible under 1a.
- WHEN: scheduled session boundaries (Asia close / London open), declared before any data is read.
- WHY it persists: no argument beyond 1b.
- HOW it dies: no constraint observable. Only the edge CUSUM would show it.
- 1b limbs:
  - (i) ≥3 decades of sample: **not met**. I found no EUR/USD or 6E cohort for this construct.
  - (ii) ≥3 independent cohorts: **not met**. The nearest published cousins are other constructs or instruments: Elaut, Frömmel & Lampaert 2018 *JFM* 37(1), 35–51 (first/last-half-hour momentum, RUB/USD on MICEX, 2005–2014, abstract only); Baltussen et al. 2021 *JFE* (market intraday momentum, a last-30-minute construct, 60+ futures); Gao–Han–Li–Zhou (equity index).
  - (iii) replication ≥10 years after discovery: **not met**.
  - (iv) no known sign-reversal condition: **not met / adverse**. `opening-range-breakout` class finding: "Equity-index-specific — ZB *fades* its opening range … sign-reversed. Do not transplant". There is also a documented directional seasonality inside this window: EUR depreciates against USD from the European open to the ECB fix (KMW Table I, t = −7.24). A two-sided breakout rule would mix that drift into its long and short arms asymmetrically.
- **Req 1 verdict: not a seed today.** Neither 1a nor 1b holds.

## Effect priors (Req 2)
| Source (date accessed) | Cohort | Figure | Transplant? |
|---|---|---|---|
| Elaut, Frömmel, Lampaert, *J. Financial Markets* 37 (2018) 35–51, via search result https://econpapers.repec.org/RePEc:eee:finmar:v:37:y:2018:i:c:p:35-51 (2026-11-04, abstract only) | RUB/USD, MICEX, 2005–2014 | none taken (different construct) | Yes. Inadmissible |
| DL-2, `lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md` (repo, 2026-11-04) | M6A / 6A-parent, full-session reference | geometric feasibility: median R = 1.000 (lookback 1), 0.687 (lookback 2); 85–97% of fired trades never reach 1R | Sibling instrument, different reference window. Prior only, not a δ |

- Decay haircut: not applicable (no δ).
- Screen figure: **UNSCREENABLE**. What would supply it: a δ-extraction probe on M6E's own export (2016–2026). It would cost a data read and K, needs an operator GO, and must report per-session break frequency, the signed next-window return conditional on break direction, and its σ. The DL-2 entry packet makes the same probe carry the **geometric-feasibility-ratio diagnostic** for M6E. That diagnostic is R = (move reachable before MFFU's 16:10 ET auto-liquidation) / (Asia-range-derived stop width). The packet says "any successor must run this same diagnostic for its own target instrument".

## Prior consult (advisory, Rule 26)
```text
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M6E prior-session-breakout-continuation; echo "exit=$?"
FATAL: no ledger for 'M6E'. Known: 6J, BTCUSD, ES, EURGBP, EURUSD, GER40, M2K, M6A, M6B, MCL, MES, MGC, MJY, MNQ, MYM, NAS100, NG, NQ, SPX500, USDCAD, USOIL, XAGUSD, XAUUSD, YM, ZB, ZF, ZN
exit=2
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M6E asia-range-london-breakout-continuation; echo "exit=$?"
FATAL: no ledger for 'M6E'. Known: 6J, BTCUSD, ES, EURGBP, EURUSD, GER40, M2K, M6A, M6B, MCL, MES, MGC, MJY, MNQ, MYM, NAS100, NG, NQ, SPX500, USDCAD, USOIL, XAGUSD, XAUUSD, YM, ZB, ZF, ZN
exit=2
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell EURUSD asia-range-london-breakout-continuation; echo "exit=$?"
FATAL: unknown mechanism 'asia-range-london-breakout-continuation'. Nearest: 'prior-session-breakout-continuation'. Declare it NEW in MECHANISMS.md.
exit=2
--- nearest proxies (PROXY, not M6E) ---
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell EURUSD prior-session-breakout-continuation; echo "exit=$?"
=== EURUSD x prior-session-breakout-continuation ===
ledger: ops/instruments/EURUSD.md
venue: NOT TRADABLE at the live firm — FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present.
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to EURUSD): (M6A, 2026-08-22 — same day as minting): DL-2's TRAIN scoring closed AMBIGUOUS/ABANDONMENT the same day this id was minted — nominee V9 fails 3 of 4 nomination gates; a same-day geometric-feasibility diagnostic found the construction structurally infeasible on M6A and retired it for that instrument, with a stop-rule/re-proposal bar binding any successor. [`RESULTS.md`](../../../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: The London 16:00 WM/Reuters fix carries a genuine ~2bp gross post-fix reversal (reproducing the source paper's magnitude) but FXIFY retail all-in cost (~0.8 pip) exceeds the 0.277-pip best-of-grid break-even — the edge is real but not retail-tradeable. [#F1]
exit=0
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell M6A prior-session-breakout-continuation; echo "exit=$?"
=== M6A x prior-session-breakout-continuation ===
ledger: ops/instruments/M6A.md
verdict: AMBIGUOUS-PARKED (2026-08-22)
  source: ../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md
  BLOCKING — a parked concept holds this cell and shares the instrument's anti-SNAG budget; address it (and any decision date) in the pre-registration.
class finding (mechanism-wide, not specific to M6A): (M6A, 2026-08-22 — same day as minting): DL-2's TRAIN scoring closed AMBIGUOUS/ABANDONMENT the same day this id was minted — nominee V9 fails 3 of 4 nomination gates; a same-day geometric-feasibility diagnostic found the construction structurally infeasible on M6A and retired it for that instrument, with a stop-rule/re-proposal bar binding any successor. [`RESULTS.md`](../../../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).
cost hurdle: 2.82 USD/round-trip (1-tick slip) (Stage-1 third-leg map Inputs: commission $0.91/side; RT 1t $2.82 / 2t $3.82; cost-tax 1t r=1 = 0.0902 (FLAG-COSTBIND vs own-panel floor 0.0891). Commission input disputed — core/firm_rules.py places M6A in the cheaper M6E/M6A $1.60-RT group, not the $1.82-RT index-micros group this figure derives from; correction disclosed but not yet applied, see docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md §0.) — VERIFY at #A1
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Stage-1 Currencies SURVIVOR under FLAG-COSTBIND — cost-tax binds before the own-panel Clause-N floor on the pooled panel; Stage-2 ex-FOMC flips the binding constraint COST->POWER. [#A1]
prior: Q-TNEC-ENV-1 envelope NON-EMPTY at 20/40/80/160-tick cells (8-tick DEAD on cost); census authored no M6A entry; published FX-fix delta refused as cross-instrument transplant under strategy_harvest Requirement 2. [#A4]
exit=1
$ python3 -I scripts/fp.py python scripts/instrument_profiles.py cell 6J prior-session-breakout-continuation; echo "exit=$?"
=== 6J x prior-session-breakout-continuation ===
ledger: ops/instruments/6J.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to 6J): (M6A, 2026-08-22 — same day as minting): DL-2's TRAIN scoring closed AMBIGUOUS/ABANDONMENT the same day this id was minted — nominee V9 fails 3 of 4 nomination gates; a same-day geometric-feasibility diagnostic found the construction structurally infeasible on M6A and retired it for that instrument, with a stop-rule/re-proposal bar binding any successor. [`RESULTS.md`](../../../../lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md).
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: [Aegis-to-6J venue-transfer prior; its figures are elided from this copy because they describe the locked Aegis book (Rule 13). Read them at the owner, `ops/instruments/6J.md`.] [#J1]
prior: [Venue sizing-throttle prior on Aegis; figures elided from this copy (Rule 13, locked sizing target). Read them at `ops/instruments/6J.md`.] [#J5]
exit=0
```
- Register hits:
  1. M6A `prior-session-breakout-continuation` is **AMBIGUOUS-PARKED** (BLOCKING exit 1: "shares the instrument's anti-SNAG budget"). It binds M6A, not M6E, but the DL-2 stop rule binds any successor "reusing this stop/target/hold construction … on any instrument or mechanism id".
  2. EURUSD and 6J × the same id: untested (exit 0).
  3. The EURUSD ledger prints its fix prior (#F1) on every consult. It is not relevant to this mechanism.
  4. Two class findings bear on it. The ZB sign-reversal under `opening-range-breakout`. And MYM `opening-range-continuation`, which failed placebo and cost together.
- Domain bars: the index-intraday OHLCV raised bar is out of scope (FX). No FX domain bar exists.
- Family K bank (Req 3 disclosure): `fc_carry_6e6j6cl.json` K = 1 (closed). The EURUSD pattern-enum harness is K = 450 (spot, closed), and its 450 patterns included intraday technical archetypes; zero cleared the prefilter. DL-2 on M6A is K_intrinsic ≈ 10 (separate family). Declared K_intrinsic for this cell: ≤ 3 if it is ever admitted.

## Venue legality at MFFU
- Native route: own-settings automation is allowed and HFT is banned (8444599, read 2026-11-04 [W-x]). Envelope E6 assumes attended automation. **The London open falls in US pre-dawn hours, so attended operation is an operational burden.**
- Product offered: M6E at $1.44 RT ($0.72/side), per the `core/firm_rules.py` comment citing 9735811 (verified 2026-07-13, re-verified 2026-10-02 per the envelope).
- Flat-by: 16:10 ET auto-liquidation (9558251, envelope re-verified 2026-10-02). On holiday half-days there is no auto-liquidation and a miss "will result in breaching". The cell is flat long before that.
- News: Tier 1 covers US FOMC, FOMC Minutes, Employment Report and CPI. They are prohibited on Rapid/Pro Sim Funded with a ±2-minute no-position rule, and permitted on evaluations (8230009, "Last updated August 31, 2026" [W-x]). A London-morning hold that runs into the US morning collides with the 08:30 ET Employment and CPI releases. In sim-funded those days must be skipped or the position flattened, and the pre-registration must state the collision frequency (envelope E7).
- Hold: intraday only.
- Fills: **high exposure to the "favorable fills" clause.** The entry is a stop/break order, and MFFU states "Exploiting the absence of slippage and utilizing tight brackets to gain from favorable fills are not permitted" (8444599 [W-x]; register D9). A pass that depends on zero-slip sim stop fills would be non-compliant and would not carry to live.
- Cross-firm hedging / product group: MFFU bans "hedging of any kind" on the same underlying. The cell is two-sided, so it can be short M6E while a Currencies-group long (e.g. 6J at Bulenox or Tradeify) is open elsewhere. Tradeify §4a bans opposing Currencies-group directions across "any accounts under your control". Sign coordination is needed if any Currencies book runs at Tradeify.

## Distinctness
- vs index ORB book: the instrument (M6E vs MNQ), product group (Currencies vs Equity Index) and session (London open vs US cash open) all differ. **The mechanism does not differ much.** Both are session-range breakout continuations with stop entries. On the D10 working test (instrument, session window **and** mechanism all different), this cell probably **fails the mechanism limb** (D10 open question 2).
- vs other R2 dossiers: Shares the London-morning session-break family with r2-6j-psbc (same Currencies group); distinct only by instrument and reference range. A stop-entry session-range break, so it is the FX dossier closest to ORB's construct.

## Reach (T3)
- 5f reach (D7, `gates.reachability(k, n)` run 2026-11-04 through the fp launcher; arithmetic only, no data read). Banked builder K on this instrument: **0** on the public record (R1 is MCL-only and unrun; the builder ledger is private, so `ledger.k()` must confirm it at registration). Development sessions n ≈ **2,325**: window 2016-01-04..2026-11-02 (the calendar's 2016 start binds, not the export) ≈ 2,703 sessions by `ops/calendars/cme_holiday_calendar_2016_2026.json` (sha256 `407d93bb815ee6b2…`; weekdays less non-`NORMAL` dates), less D9's 378-session holdout. The pinned export sets the real n; FX holidays differ from the equity columns, so the calendar estimate is coarser for FX. M6E's export landed locally 2026-11-03; its repo landing (ledger, specs, SHA256SUMS) is owed before any card.
  | K (banked + this card) | 5f floor (annual SR) | P(pass \| SR 0.85) | P(pass \| SR 0.89) | Reachable (D7) |
  |---|---|---|---|---|
  | 1 (this card) | 0.542 | 0.825 | 0.855 | yes |
  | 2 | 0.713 | 0.662 | 0.705 | yes |
  | 3 | 0.822 | 0.533 | 0.581 | yes |
  | 4 | 0.888 | 0.454 | 0.502 | yes, at the boundary |
  Normal approximation; 5f only, so every other gate lowers P(pass). The instrument's lifetime budget is 4 looks (generation note §11).
- Power at expected event count: N ≤ 2,325 (at most one per dev session; the break fraction is unknown). Power is **not computable (UNSCREENABLE)**.
- Cost and entry-slip sensitivity (M-16, printed only): commission at MFFU is $1.44 RT = **1.15 ticks RT** (M6E tick $1.25, per the CME spec quoted in the generation DRAFT §9.1; Rule 17 re-read owed). Slip-to-consume-edge is **not computable** because there is no δ. M-16 binds hardest here, since this is a stop-entry construct. The first probe must run the slip sweep {0, 0.5, 1, 1.5} ticks before any exit or MC work.
- Barrier feasibility: pending atlas (sibling session).
