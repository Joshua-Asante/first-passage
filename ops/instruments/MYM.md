# INSTRUMENT LEDGER — MYM

**Symbol:** CBOT Micro E-mini Dow futures (MYM; Globex, Databento `GLBX.MDP3`) · **Parent:** YM ($5) · **$0.50/pt** · **Asset class:** equity index futures
**Status (2026-08-04):** ⚠ **NO LONGER A LIVE c1 LEG — withdrawn from deployment.** The Tradeify venue is de-scoped as a deployment target for the locked Striker book, evaluation included ([`ADR 2026-08-04`](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md); ⚠ **narrowed same day, Addendum 2026-08-04** — the bar is on redeploying this leg, not on Tradeify-shaped base-construct research); this leg never took a strategy-signal-originated fill and now has no venue. **Lifecycle unchanged: `Striker` stays `AUTHORIZED · MECHANISM @ 1.00×`** (canonical: [`strategy_lifecycle.md`](../../docs/methodology/strategy_lifecycle.md)) — no `core/lifecycle.py` write, no demotion; venue-fit is not decay. Pine, parameters and `LEG_MAP` untouched. Prior status line preserved below as record.

**Status (prior, through 2026-08-03):** **LIVE c1 leg (disarmed).** Hosts the Striker DJ30 v4.5 **venue edition** (`striker_dj30_v4.5_mym.pine`) as one of the two c1 legs on the Tradeify Select 100K eval — `dry_run=true`, WATCH-1 0.50×, **no strategy-signal-originated fill yet** (rail has canned B4 fills: B6 dry-fire 2026-07-20 + 2026-07-27 SIM; account not pristine — see [`CLAUDE.md`](../../CLAUDE.md) live-execution posture). The **reconstruction** track on this instrument (opening-range *continuation*) is **TERMINAL**.
**Last updated:** 2026-08-29

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Any session deriving/testing/adjudicating on MYM MUST read this at session start and append a dated disposition. **Created 2026-07-25.** Sibling parent ledger: [`YM.md`](YM.md) (W1/W2 + the DJ30→MYM transfer falsification Y3). **The DEAD list is the point** — this instrument's highest-value content is what has been ruled out on it.

## PROFILE (machine-readable)

```yaml
symbol: MYM
asset_class: equity-index-futures
family: [YM]
venue_tradable: false
venue_note: "AUTHORIZED-but-venue-less incumbent (Striker DJ30 MYM edition); no live book to correlate new work against — check venue_note before book-correlation gate."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 6.57
  units: "bp/event"
  basis: "4x Tradeify hurdle"
  source: "#M6"
cells:
  - mechanism: trend-following
    verdict: LIVE
    date: 2026-07-23
    source: "../../docs/briefs/2026-07-23-tradeify-book-composition.md"
  - mechanism: opening-range-continuation
    verdict: DEAD
    date: 2026-07-16
    source: "../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md"
  - mechanism: event-window-reversal
    verdict: DEAD
    date: 2026-07-21
    source: "../../docs/briefs/closures/MYM-3FPS-1-closure-falsified.md"
  - mechanism: opening-pressure
    verdict: DEAD
    date: 2026-07-21
    source: "../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md"
  - mechanism: venue-transfer
    verdict: DEAD
    date: 2026-07-09
    source: "../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md"
  - mechanism: ict-liquidity
    verdict: DEAD
    date: 2026-07-29
    source: "../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md"
  - mechanism: pdh-pdl-failed-break-reclaim
    verdict: DEAD
    date: 2026-08-13
    source: "../../docs/briefs/closures/MSL-C1-closure-falsified.md"
  - mechanism: daily-range-state-persistence
    verdict: AMBIGUOUS-PARKED
    date: 2026-08-29
    source: "../../docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md"
  - mechanism: overnight-range-day-session-transfer
    verdict: CONTINGENT-FORWARD
    date: 2026-08-29
    source: "../../docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md"
  - mechanism: intraday-bar-volume-regime
    verdict: CONTINGENT-FORWARD
    date: 2026-08-29
    source: "../../docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md"
  - mechanism: overnight-gap-magnitude-range-conditioning
    verdict: CONTINGENT-FORWARD
    date: 2027-03-01
    source: "../../docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md"
  - mechanism: bar-closing-location-autocorrelation
    verdict: CONTINGENT-FORWARD
    date: 2026-11-08
    source: "../../docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "Not a barren instrument — the incumbent locked leg is profitable here; one narrow continuation expression failed."
    source: "#M1"
```

---

## STANDING WARNINGS (read first)

- **W1 / W2 — inherited from [`YM.md`](YM.md) unchanged.** `.c.0` continuous is calendar-roll, front-month, **unadjusted** (quarterly mid-month, 3rd-Fri Mar/Jun/Sep/Dec) → any window spanning a roll carries a phantom calendar-spread jump. Databento `ohlcv-1d` buckets by UTC calendar day → phantom weekend bars; drop settle-date weekday > 4.
- **W3 — a live-ops panel refresh silently invalidated a research pin here.** `S-MYM-ORC-02`'s `runspec.json` pins `298ab8c8…`; `core/data/bar_data/SHA256SUMS` now reads `24e16952…` after commit `da075a1` (2026-07-21) landed fresher BAR EXPORTs. `run_development.py` raises `IntegrityError` before loading, so the frozen run is **not reproducible**. Re-pin deliberately; treat vendor refreshes as breaking changes to every frozen study that pinned the old bytes.
- **W4 — micro-era OOS is a reserved gate.** MYM trades from 2019-05. Re-parameterize slippage/fills on native micro data; do not inherit the YM parent fill model.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **M1** | **The incumbent locked leg is profitable on this instrument.** Striker DJ30 v4.5 MYM venue edition on its own export: **PF 1.80 / WR 40.3% / n=263 / net $35,121.70**. This is the correct reference when reading the reconstruction failures below — MYM is **not** a barren instrument; one narrow *continuation* expression failed on it. | [`2026-07-23-tradeify-book-composition.md`](../../docs/briefs/2026-07-23-tradeify-book-composition.md) | **HIGH** (measured export). |
| **M2** | **Opening-range CONTINUATION does not survive on MYM.** `S-MYM-ORC-02` (session-aware, N=403): **D0/D1/D9 PASS, D2–D8 FAIL** — placebo **p=0.2144**, gross/cost ratio **0.693** against a 4.00 bar, net **−0.0210R**, PF **0.951**. Seven independent failures where one suffices under §6.2. | [`closure`](../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md) | **HIGH** (pre-registered). |
| **M3** | **D3 is arithmetically unrescuable by sizing.** The gross/cost ratio reduces to mean gross $ ÷ mean cost $ = **0.655** — contracts and stop-width cancel out. No position-size, risk-%, or R-renormalization can move it; only hold-time or venue can, and hold-time is an explicitly-mapped exhausted lever. | [`closure` §D3](../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md) | **HIGH** (algebraic). |
| **M4** | **ORC-01's AMBIGUOUS was the gate working, not a runner bug.** Its exit-2 was the **pre-registered AMBIGUOUS-HOLD branch operating correctly** against a blind spot in the frozen candidate-1 semantic — a universal 16:00 force-flat vs **53 exchange early closes**. Cited correctly: this is a spec blind-spot finding, not a code defect. | [`closure` §3](../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md) | **HIGH**. |
| **M5** | **Third-Friday derivative-settlement reversal does not reproduce at useful magnitude.** Native `MYM.v.0` minute data, **$0.00**, exact coverage **84/87 (96.6%) PASS**: overnight **+1.54 bp** (power 0.042), short reversal **+2.68 bp** (power 0.067) — both below the **0.2139** standardized-effect floor; cost-law also FAIL (**+2.68 bp vs 6.57 bp** 4× Tradeify hurdle). Year signs unstable; the tradable limb is **negative in 2024–2026**. | [`mym_3fps_recon_2026-07/RESULTS.md`](../../lab/archive/mym_3fps_recon_2026-07/RESULTS.md) | **HIGH** (native data, pre-registered). |
| **M6** | **Cost hurdle, pinned.** 4× Tradeify hurdle ≈ **6.57 bp/event** on MYM. Any new MYM construct must clear this in the same units at admission (harvest Req 5), not at sourcing time. ⚠ 2026-08-04: Tradeify is no longer the programme's binding venue (successor is fork **F3**), so re-price against the elected venue once F3 rules — friendly-firm per-side costs span **$0.50–$0.95**, so the hurdle moves by well under 2×. | [`MYM-3FPS-1 closure`](../../docs/briefs/closures/MYM-3FPS-1-closure-falsified.md) | **HIGH**. |
| **M7** | **Panel provenance.** BAR EXPORT v0.2 `CBOT_MINI:MYM1!` → `core/data/bar_data/MYM_M15.csv`, n=**141,471**, span 2020-07-01 → 2026-07-03Z. Provisional 1R floor (locked-risk mirror, roll-seam-masked ATR(11)×1.20): full-median **$3,234** / recent-90d **$4,350**. | [`STATE.md`](../../STATE.md) reconstruction line | **HIGH**. |
| **M9** | **45min session-close refresh (supersedes M8's 55min-close numbers for MYM alone) + first MYM+MNQ combined-book passability calculation.** Operator re-exported v0.3 with session-close moved 16:55→**16:45** (more buffer before Tradeify's ~16:59 force-flat). Freshly parsed and Step-0-verified directly from the raw CSV (1,422 trades, qty=2 constant, cumPnL reconciles to the cent, span 2022-01-03→2026-08-24): **net $19,509 (was $16,858), PF 1.190 (was 1.172), maxDD $5,085 (was $5,042), RF 3.84 (was 3.34)** — the earlier close improves every headline metric, not a tradeoff. Standalone rope-walk cross-check at qty=2: **80.0% bust**, closely reproducing M8's 82.7%-bust figure (methodology-agreement check). At qty=1: **0.0% bust**, also reproduced. **NEW — combined MYM+MNQ book**, per-contract-normalized daily P&L + adverse-excursion worst-marks, 981 shared trading days, rolling starts (MNQ leg = the same-day `ORB-MNQ-1 recon_v2` export, `MNQ.md` session log):<br>`Select_100K`: (MYM×1,MNQ×1) 50.6%/46.9% · (2,2) 17.8%/81.4% · (1,2) 19.7%/78.4% · (2,1) 30.9%/67.9% · (3,3) 21.1%/78.3% (pass%/bust%)<br>`Growth_100K`: (1,1) **77.5%/19.5%, median 86 days** · (2,2) 29.3%/69.8% · (1,2) 38.5%/59.5% · (2,1) 52.0%/45.5% · (3,3) 31.1%/68.3%<br>**Headline: MYM×1+MNQ×1 on Growth is the best cell measured across either leg's entire body of work today** — beats every standalone qty/tier combo for either instrument alone. On Select the same sizing is a near coin-flip, essentially riding MNQ's own qty1 standalone risk (48.4%/48.9% alone) with MYM's contribution nearly free (MYM alone at qty1 never busts). **Running both legs at their as-exported qty=2 is a clear NO-GO** (17.8%/81.4% Select) — both legs' own qty=2 standalone bust rates (80.0%/58.0%) compound rather than diversify. Contract-cap check: even 3+3=6 micros uses under 8% of Select_100K's 80-micro account-aggregate cap. **Two disclosed, unresolved-direction caveats** (no raw bar file for either leg, only trade-list CSVs): (1) each day's worst mark is that trade's own Adverse Excursion column, coarser than a true intrabar path — understates risk; (2) a day's COMBINED worst mark sums each leg's own worst mark as if simultaneous — overstates joint risk. Net bias not resolved. Six MYM + two MNQ trades span >1 calendar day, all at Thanksgiving/Christmas early-closes — plausibly the correct early-close fallback, not independently verified against either Pine source. | this pass, 2026-08-25 — operator-supplied `ORB-MYM-1_v0.3_..._f7482.csv` + `ORB-MNQ-1_recon_v2_..._097d9.csv`, both parsed and Step-0-verified directly (cumPnL reconciles exactly to the file's own totals); untracked, no in-repo artifact | **MEDIUM-HIGH** on the single-leg refresh (directly re-verified from the raw CSV); **MEDIUM** on the combined-book figures (sound composition of two verified per-leg panels, but the two excursion-timing approximations above are unresolved in net direction, and this has not been TV-native validated as a joint book). |
| **M8** | ⚠ **A SEPARATE, NON-STRIKER CANDIDATE — sizing reframes its Tradeify verdict, but no untouched holdout remains to trust it.** Distinct from the LIVE `trend-following` Striker DJ30 v4.5 edition (M1) and the DEAD `opening-range-continuation` mechanism (M2) — a new, informally-sourced ORB-breakout + pyramided scale-in construct (parity-matched to the `ORB-MNQ-1` shape), operator-selected Downloads lane, 2022-01→2026-08 panel. **v0.1 offline survey: NULL** (8 families / ~85 cells, everything PF 0.80–1.10; the MNQ ORB construct's PF 1.399 does not transfer — PF 0.995 OOS). **Operator hand-tuned on TradingView through v0.2→v0.3** (2 scale-in adds + underwater-only stall stop): TV-native **net $16,858, PF 1.172, maxDD −$5,042, RF 3.34**; WR fell 44.3%→35.3% by construction (the stall makes cuts certain losses) but meanWin rose $325→$395. **The sizing-lever finding, export-anchored (810 rolling starts): at qty 1/leg NOTHING busts on either tier (0.0%)**, worst equity DD −$2,138 vs a $3,000/$3,500 rope, and 100% of RESOLVED starts pass — independently reproduces the 2026-08-22 engine finding ("MYM never busts, median ~17mo") by a different method; cost becomes CALENDAR (median 207–478 days), not drawdown. `Tradeify_Growth_100K` preferred over Select (~2× pass rate; no consistency rule) — but **the 40% consistency rule DOES bind for THIS pyramided shape** (14.6% vs 20.7% pass at Select; top day 34.3% of net), contra the general 630-cell map's "never binds," because that map explicitly never tested a shape this skewed — corroborating, not contradicting, the map's own scoping caveat and the original 2026-08-22 Tradeify consistency/pyramid mechanism. ⚠ **Method lesson, load-bearing:** an offline re-simulator built to avoid TV round-trips FAILED validation (+70% net overstatement even after one fix, inverted 2024's sign) — root cause, scale-in adds fill at BAR CLOSE + slippage, not at the trigger level; discarded for counterfactual use, so every number above is either a TV export or an export-anchored replay that changes only exit behaviour on real fills. ⚠⚠ **CROSS-BRANCH CAVEAT (2026-08-25, from the sibling 6J survey) — read before trusting the sizing-lever headline:** 6J's `orb-ny-breakout` construct produced a **structurally identical in-sample claim** (0.0% bust, high pass rate) and **inverted completely on a clean, pre-registered, one-shot OOS holdout** (55.2% bust, 0.0% pass) — payoff ratio held, hit rate collapsed. Not evidence MYM's number is wrong (different instrument, different construct, TV-native not offline-sim) but it is the one sibling branch where a holdout survived to test an identically-shaped claim, and it failed. **No untouched MYM holdout remains** — TV tuning saw the full chart — so treat "bust is now a sizing choice" as in-sample/tuned-panel standing, not established; weight forward paper accordingly. | operator TV-native runs 2026-08-25 (`orb_mym_1/2/3_edition.pine`, `MYM_15m_edge_survey_2026-08-25.md` + addenda) — untracked, no in-repo artifact | **MEDIUM** (TV-native, not offline-sim — a stronger basis than a pure sim claim; but zero holdout remains and the sibling 6J branch just falsified a structurally identical claim on the one holdout that existed across all four diversification-lever instruments). |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator (the test that killed it) | K | Source |
|---|---|---|---|
| `S-MYM-ORC-02` — session-aware opening-range continuation | D2–D8 FAIL at N=403; placebo p=0.2144; gross/cost 0.693 vs 4.00; net −0.0210R | 2 | FALSIFIED 2026-07-16 — [`closure`](../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md) |
| `S-MYM-ORC-01` — universal-force-flat continuation | AMBIGUOUS-HOLD branch fired: frozen 16:00 force-flat blind to 53 exchange early closes | — | CLOSED-AMBIGUOUS 2026-07-16 — [`closure`](../../docs/briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-1-ambiguous.md) |
| `MYM-3FPS-1` — third-Friday settlement reversal | Both power limbs below the 0.2139 floor **and** cost-law FAIL (2.68 vs 6.57 bp); tradable limb negative 2024–26 | 0 | FALSIFIED 2026-07-21 — [`RESULTS.md`](../../lab/archive/mym_3fps_recon_2026-07/RESULTS.md) |
| `OPENPRESS-1` (MYM limb) — opening-volume × directional efficiency | **Wrong-signed** plus cost FAIL; no threshold/window/instrument rescue licensed | 0 | FALSIFIED 2026-07-21 — [`RESULTS.md`](../../lab/archive/opening_pressure_map_2026-07/RESULTS.md) |
| Striker DJ30 → MYM *transfer* (R5 successor) | OOS PF ratio **0.559 < 0.8×** on structural venue costs — fired the R6 §4 falsifier | — | FALSIFIED 2026-07-09 — see [`YM.md`](YM.md) Y3 |
| `SLR-MYM-1` — liquidity sweep-and-reclaim at the open (`ict-liquidity`) | **Closed at Stage 0 on two independent gates, mechanism never tested.** (a) Harvest Req-1a: both constraint framings fail the delete- and flip-tests (ADR 2026-07-26 §2-A). (b) **S3 order-symbol occupancy** — shares `MYM1!` with the incumbent leg, and the venue nets one position per symbol, so Tue+Fri close structurally; best compliant day set Mon+Wed+Thu = **81 IS entries vs a 120 floor** (upper-bound proxy) | **0** | FALSIFIED (as scoped) 2026-07-29 — [`closure`](../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) |
| `pdh-pdl-failed-break-reclaim` × MYM (MSL-C1) | Explore IS both-arms session-block 95% CI entirely &lt; 0 (long n=406; short n=444). CONFIRM unread. | 0 | FALSIFIED 2026-08-13 — [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) |

**Re-proposal bar (standing).** A candidate #3 on the continuation mechanism requires fresh operator authorization **and** a fresh frozen pre-registration. Named-forbidden by the ORC-02 closure: lower-cost rerun, parameter grid, opening-window selection, date deletion, gross-only rescue. Ahead of that, the 2026-07-21 **raised bar** on single-instrument index-futures intraday OHLCV directional timing gates any new candidate of this class ([`rejected_candidates.md`](../../docs/rejected_candidates.md)).

## ACTIVE / OPEN

- **[`MSL-S2B` STAGE-1 FAIL (route)](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) (2026-08-14).** `sweep-failure-filtered-continuation` × MYM — pre-G0 kill; [closure](../../docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md). G0 never frozen; CONFIRM unread.
- **[`MSL-C1` FALSIFIED](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) (2026-08-13).** `pdh-pdl-failed-break-reclaim` × MYM explore IS — [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md). G0 was frozen; CONFIRM unread.
- **MYM family K bank = 1 → 6 as of 2026-08-29 — still a DISCLOSURE, not a gate** (bank
  corrected 2026-07-29; gating status amended 2026-08-04). ⚠ **New this session:** the
  2026-08-29 batch's closed manifest (`discovery_manifests/mymdd_1_2026_08_29.json`, `--lane
  blind`, K=5) banks into the family count per the same 2026-08-18 operator ruling that banked
  `MNQSR-1` ("Notice-phase closed manifests bank") — 1 + 5 = **6**. Since `K_eff = K_intrinsic`
  under [ADR 2026-08-04](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md), this
  bank increment does not itself change the screening floor for any *individual* future
  `K_intrinsic`-declared seed — it is bookkeeping, not a brake. Source: `st_eh_supertrend_grid.json` banks executed `K=2` spanning **two** families — the split is 1 MNQ + 1 MYM per its `executed_looks`; do **not** add 2 to either. ⚠ **The floor arithmetic below is superseded:** under [ADR 2026-08-04](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) (`Accepted`) **`K_eff = K_intrinsic`**, so a `K_intrinsic=1` seed screens at **`K_eff` 1 → floor 0.650** (headroom 0.350), not `K_eff=2` → 0.85. The bank is still read and still **must be disclosed**; it no longer gates. **Consequence for the "widest remaining runway" framing: it is void** — every family now screens at the same floor for the same `K_intrinsic`, so MYM has no comparative K advantage over MNQ, M2K, or any other instrument, and "spend it wisely because it is scarce" is no longer the right reason to be careful. Be careful instead because `K_intrinsic` is now the **only** brake on selection inflation. Governing rules: [ADR 2026-07-26 §2-C](../../docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) (what banks) + [ADR 2026-08-04](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) (what a bank does).
  - ⚠ **Unreconciled, and as of 2026-08-04 no longer consequential:** this ledger's own DEAD table records `K` = **2** for `S-MYM-ORC-02`, which lives outside `discovery_manifests/`. The codified convention (harvest Req 3) banks from **closed manifests only**, so the bank is 1. The original worry — *"if those trials are ever ruled bankable the family goes to 3 ⇒ `K_eff` 4 ⇒ floor 1.06 > Cap, closing MYM to new seeds"* — is **void** under [ADR 2026-08-04](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md): banks do not enter `K_eff` and cannot close a family. Reconciling the count is now a **bookkeeping** question (the disclosure should be accurate) rather than a live threat to MYM's availability.
- **S3 — order-symbol occupancy (new standing constraint, 2026-07-29).** Any *second* strategy on this instrument in the **same account** shares the `MYM1!` order symbol with the incumbent leg, and the venue holds **one net position per symbol per account**. A second MYM strategy therefore cannot hold an independent position on any day the incumbent can fire (**Tue, Fri**) — **regardless of contract-cap allocation**. This is orthogonal to, and stricter than, the third-leg spec's cap-based Slot framing. Source: [`SLR-MYM-1 closure`](../../docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) F1.
- **[`overnight-range-day-session-transfer` GRADUATE-eligible, Pre-Q deferred](../../docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md) (2026-08-29, corrected same day).** ⚠ **Supersedes the original same-day HOLD-until-2027-03-01 line, struck below.** A design-flaw catch (marginal-rate comparison ≠ "matched conditioning") triggered a stratified re-run: within-stratum lift +31.8pp / +22.1pp, bootstrap CI [+10.4pp, +32.2pp] entirely positive, p=0.00025. D5 stage-1 precondition (2) decisively cleared. Conditions 3 (joint-surrogate null design, adversarial-reviewed) and 4 (operator GO) still outstanding; Pre-Q authoring deferred to the planned MNQ+MYM pooling session per the operator's own batch framing — not opened here. No raised-bar route needed (conditioner-role, same as candidate 1).
  ~~$0 cheap falsifier AMBIGUOUS (diff +0.0297, CI straddles 0); HELD until 2027-03-01~~ — struck 2026-08-29, same day, superseded by the stratified correction above (marginal comparison was the wrong statistic, not a wrong answer to the right one).
- **[`overnight-gap-magnitude-range-conditioning` HELD until 2027-03-01](../../docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md) (2026-08-29, corrected same day).** Same stratified-design correction as the overnight-range sibling — the original marginal "clean kill" (diff −0.1039) inverted sign entirely: within-stratum lift +14.0pp / +6.7pp, bootstrap CI [−4.2pp, +14.8pp] straddling 0, p(lift≤0)=0.1247. Moved DEAD → CONTINGENT-FORWARD (was never a graduate-worthy pass, but no longer a kill either). Re-check on the grown panel.
- **[`intraday-bar-volume-regime` GRADUATE-eligible, Pre-Q deferred](../../docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md) (2026-08-29, corrected same day).** ⚠ **Supersedes the original same-day DROP line, struck below.** Same marginal-vs-stratified design flaw as the overnight-range/gap-magnitude pair, caught separately because this construct doesn't cite the D5 spec so the first adversarial pass didn't scan it for the pattern. Stratified on the bar's own already-elevated range: within-stratum lift +16.5pp / +24.5pp, bootstrap CI [+15.4pp, +17.6pp] entirely positive, p≈0, n=139,605 — the largest-magnitude and most tightly-estimated correction in this batch. Cross-instrument-corroborated by MNQ's independently-run, independently-stratified same-day candidate 3 (+20.6pp/+25.6pp, also GRADUATEd). No raised-bar route needed (conditioner-role, same as candidates 1/2).
  ~~$0 increment falsifier clean NO-INCREMENT (diff −0.0049, CI [−0.0085,−0.0012]); DROPPED~~ — struck 2026-08-29, same day, superseded by the stratified correction above (marginal comparison masked a real +16-25pp effect behind a same-bar volume/range correlation of 0.86).
- **[`bar-closing-location-autocorrelation` HELD until 2026-11-08](../../docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md) (2026-08-29).** SIGNAL-EXCESS (obs −0.0370, CI entirely negative, p=0.005) — admission-route status under the directional-timing raised bar is unresolved; not GRADUATEd on this session's own authority. ⚠ No longer the batch's largest-magnitude finding by CI tightness/effect size — `intraday-bar-volume-regime`'s corrected +16.5pp/+24.5pp now exceeds it — but remains the only *unconditional shape-persistence* result and the only one with an open governance (not just design) question.

## RECORD — c1 leg (withdrawn)

- **c1 MYM leg — venue edition, WITHDRAWN from deployment 2026-08-04 (see Status, L4). Record only; nothing here is open.** WATCH-1 0.50×, per-leg cap **69**, expected sizing 8 base / 60 add, hedging rule clears by construction (long-only), disposition fork **F2**. ⚠ **Corrected 2026-08-02 — this line read `9` / `67`, the PRE-2026-07-22 whole-cap values.** At `cap_alloc=69`, `reserve_cap = ⌊69/8.5⌋ = **8**`. Re-pin: [`c1_nt8_sizing_host_impl.md`](../../docs/spec/c1_nt8_sizing_host_impl.md) §7 · synthetic entry `qty=8`. Sweep note lives in the private archive.
- **Reconstruction track: TERMINAL.** No open MYM research question **on that track**
  (opening-range CONTINUATION, M2/M3). A separate, non-reconstruction candidate (ORB-breakout
  + pyramided scale-in, unrelated mechanism) opened and was tuned 2026-08-25 — see **M8**; it
  does not reopen this TERMINAL ruling.

## SESSION LOG

- **2026-08-29 (correction #2, follow-up)** — **Same design-flaw class caught on candidate 3
  (`intraday-bar-volume-regime`), missed by the first adversarial pass because this construct
  doesn't cite the D5 magnitude-persistence spec** (it's a different mechanism family), so the
  review that scanned candidates 2/4 for the marginal-vs-stratified pattern didn't scan this one.
  `c3_volume_regime.py` diffed two MARGINAL conditional rates (volume-conditioned vs.
  own-range-conditioned) — same flawed shape as the corrected `c2_c4_increment_falsifiers.py`.
  Independently verified before rerunning: same-bar volume/range Spearman correlation on MYM's
  own data = **0.8618** (not merely assumed by analogy to the cited MNQ figure of 0.88) —
  exactly the regime where a marginal comparison is unreliable. Corrected script
  (`c3_stratified_rerun.py`) stratifies on the bar's own already-elevated range: within-stratum
  lift **+16.5pp / +24.5pp**, bootstrap CI **[+15.4pp, +17.6pp]** entirely positive, p≈0,
  n=139,605 — **the largest-magnitude, most tightly-estimated reversal in the whole 2026-08-29
  batch** (original marginal diff was −0.49pp, read as a clean DROP). **DROPPED→GRADUATE**,
  Pre-Q authoring deferred to the same MNQ+MYM pooling session as candidate 2; no raised-bar
  route needed (conditioner-role). Cross-instrument corroboration: MNQ's own same-day candidate
  3 (informally `bar-volume-regime`, correctly stratified from the start, no landed
  MECHANISMS.md heading of its own yet) found a similar shape (+20.6pp/+25.6pp) and reached the
  same GRADUATE decision independently. `N-2026-08-29-mym-bar-volume-regime.md` rewritten in
  place (§1 superseded, not appended-around); `MECHANISMS.md`'s `intraday-bar-volume-regime`
  class finding updated the same way. **Scope-bounded:** candidates 1, 4, 5 untouched (candidate
  4's own HOLD re-check isn't due until 2027-03-01, not reopened here). No `core/`, lock,
  allocation, `dd_protection`, Pine, or rail change. $0 spent; no new K (re-measurement of an
  already-registered/closed look under `mymdd_1_2026_08_29`, matching the RE-MEASUREMENT
  convention). Scripts + JSON:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c3_stratified_rerun.py` +
  `c3_stratified_results.json`.
- **2026-08-29 (merge)** — **Merged origin/main (PR #195 landed as `b2f940f`), reconciling
  against the MNQ Phase-1 sibling batch (PR #194) and three `instrument_profiles.py`
  multi-line-truncation fixes (PRs #196/#197/#198) that landed while this PR was open.** Only
  real conflict: `lab/CATALOG.md` (both branches inserted a new `_inbox` row at the same
  alphabetical slot; kept both, slug-sorted). `MECHANISMS.md`/`PROFILES.md`/`profiles.json`
  auto-merged cleanly (non-overlapping heading positions), verified by reading the merged
  heading list + rerunning `build`/`check` (27 ledgers, 64 cells, OK) + the full pytest suite
  (79 passed). **Taxonomy reconciliation (not a mechanical merge artifact):** MNQ's landed
  `overnight-range-transmission` heading (with a real Pre-Q, `Q-RANGEXFER-1`) covers the
  identical D5 "S2" role this ledger's `overnight-range-day-session-transfer` /
  `overnight-gap-magnitude-range-conditioning` pair covers — both authored the same day before
  either session could see the other's work; MNQ combined both predictors under one id with a
  real joint stratification (gap is a nested, sign-unstable sub-question of overnight range, not
  co-equal); MYM split them into two ids without yet running that joint check. Kept as separate
  ids (already cited across this ledger's Notice-log files); added explicit cross-reference notes
  in both directions in `MECHANISMS.md` so the fork is documented, not silent. Reconciling the
  two organizations is the deferred MNQ+MYM pooling session's job.
- **2026-08-29 (correction, same day)** — **Design-flaw catch on candidates 2/4, from an
  adversarial review of the batch below: marginal conditional-rate comparison ≠ "matched
  day-session-history conditioning."** The batch entry immediately below scored both candidates
  with `c2_c4_increment_falsifiers.py`, which diffed two MARGINAL conditional rates — P(y=1|bias_new=1)
  vs. P(y=1|bias_hist=1) — rather than stratifying on `bias_hist` and measuring `bias_new`'s lift
  within each stratum held fixed, the design the D5 spec's own "matched ... conditioning" language
  actually calls for. Verified independently before rerunning: the underlying `bias`/`bias_hist`/`y`
  definitions in the corrected script (`c2_c4_stratified_rerun.py`) are algebraically identical to
  the original — only the aggregation step changed. **Both candidates flipped or strengthened:**
  #2 overnight-range went from AMBIGUOUS (marginal diff +0.0297, CI straddling 0) to a **decisive
  INCREMENT** (within-stratum lift +31.8pp / +22.1pp, bootstrap CI [+10.4pp,+32.2pp] entirely
  positive, p=0.00025) — **DROPPED→HOLD→GRADUATE** (Pre-Q authoring deferred to the planned MNQ+MYM
  pooling session, per the operator's own batch framing; no raised-bar route needed, conditioner-role
  same as candidate 1). #4 gap-magnitude went from a clean, decisive NO-INCREMENT (marginal diff
  −0.1039, CI [−0.164,−0.040]) to **sign-flipped AMBIGUOUS** (within-stratum lift +14.0pp / +6.7pp,
  bootstrap CI [−4.2pp,+14.8pp] straddling 0) — **DROPPED→HOLD until 2027-03-01**. Both original
  marginal results are retained as disclosed secondary measurements (not deleted; not the D5
  stage-1 answer) alongside the stratified results.
  `N-2026-08-29-mym-overnight-rth-range-transfer.md` and `N-2026-08-29-mym-gap-magnitude-rth-range.md`
  rewritten in place (§1 superseded, not appended-around); `MECHANISMS.md` class findings for both
  ids updated the same way. **Scope-bounded:** candidates 1, 3, and 5 were explicitly out of scope
  for this correction and are untouched. Separately noted, not acted on: `instrument_profiles.py`'s
  definition parser reportedly truncates multi-line `##` heading prose (affects all 4 of this
  session's new `MECHANISMS.md` headings) — a tooling fix is in flight elsewhere; re-run
  `python scripts/instrument_profiles.py build` once it lands rather than hand-patching the
  truncated entries here. Scripts + JSON:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_stratified_rerun.py` +
  `c2_c4_stratified_results.json`. No `core/`, lock, allocation, `dd_protection`, Pine, or rail
  change. $0 spent; no new K (re-measurement of the same two already-registered/closed looks under
  `mymdd_1_2026_08_29`, not a new search — the closed discovery manifest is left untouched, matching
  the repo's own RE-MEASUREMENT convention for the GC/CL corrected-battery precedent).
- **2026-08-29** — **Atheoretical bar-mechanism Notice-phase batch, MYM Phase 2 (mirrors an
  MNQ Phase-1 batch run separately) — 5 candidates, 5 real Notice-log entries, K=5 registered
  (`mymdd_1_2026_08_29`, `--lane blind`).** Rule-0 read this ledger + `MECHANISMS.md` +
  the two governing raised bars in `docs/rejected_candidates.md` first. **Two constraint-audit
  catches, mid-session, before running anything on the affected candidates:** (a) the "overnight
  range → RTH range" and "gap magnitude → RTH range" candidates are the frozen magnitude-
  persistence spec's own PAUSED "S2" role (cross-series, same-session, common-regime-confounded)
  — reread against `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 D5
  before running, not assumed reusable "verbatim" as originally framed; both instead ran only the
  spec's own owed $0 cheap falsifier. (b) The bar-volume-regime candidate carries the identical
  cross-series confound one bar-lag down; scored the same way. **Results:** #1
  `daily-range-state-persistence` × MYM (session TR, full Globex day) → **SIGNAL-GENERIC**
  (obs 0.6777, presence real, attribution canon-generic — 3rd instrument scored, 2nd
  SIGNAL-GENERIC of 3) → **DROPPED**, not pursued as a conditioner (the identical verdict shape
  already failed cost-effectiveness on the sibling CL instrument, `Q-CONDVAL-1`). #2
  `overnight-range-day-session-transfer` (NEW id) → $0 falsifier **AMBIGUOUS** (diff +0.0297, CI
  straddles 0) → **HELD until 2027-03-01**. #3 `intraday-bar-volume-regime` (NEW id) → $0
  falsifier **clean NO-INCREMENT** (n=139,605 bar-pairs, diff −0.0049, CI entirely <0 but
  economically negligible) → **DROPPED**. #4 `overnight-gap-magnitude-range-conditioning` (NEW
  id) → $0 falsifier **clean, decisive NO-INCREMENT** (diff −0.1039, CI [−0.164,−0.040]) →
  **DROPPED**. #5 `bar-closing-location-autocorrelation` (NEW id) → **SIGNAL-EXCESS** (lag-1
  CLV serial correlation −0.0370, CI entirely negative, p=0.005, sign-stable across 7 years and
  both halves — the strongest statistical result of the batch) → **HELD until 2026-11-08**,
  admission-route status under the single-instrument directional-timing raised bar left
  unresolved on purpose (flagged, not assumed cleared). 4 `MECHANISMS.md` headings added (one
  extended). No `core/`, lock, allocation, `dd_protection`, Pine, or rail change. $0 spent /
  K=5 registered (all disclosure-only screens, no Pre-Q opened). Scripts + JSON results:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/`. Notices:
  [`N-...rangestate-persistence`](../../docs/notes/notice/N-2026-08-29-mym-rangestate-persistence.md) ·
  [`N-...overnight-rth-range-transfer`](../../docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md) ·
  [`N-...bar-volume-regime`](../../docs/notes/notice/N-2026-08-29-mym-bar-volume-regime.md) ·
  [`N-...gap-magnitude-rth-range`](../../docs/notes/notice/N-2026-08-29-mym-gap-magnitude-rth-range.md) ·
  [`N-...closing-location-autocorrelation`](../../docs/notes/notice/N-2026-08-29-mym-closing-location-autocorrelation.md).
- **2026-08-25** — **New non-Striker candidate sourced, tuned on TV through v0.1→v0.3, sizing
  lever found — see M8.** Third of the MNQ/MYM/MGC/6J diversification branches, after the
  same-day `ORB-MNQ-1` DD-reduction session. Offline survey NULL (8 families / ~85 cells);
  operator TV-tuned an ORB+scale-in construct to net $16,858 / PF 1.172 / RF 3.34, then found
  (export-anchored, 810 rolling starts) that **qty 1/leg busts 0.0% on Select or Growth** —
  reframes "Tradeify FALSIFIED for MYM" to "bust is a sizing choice, the real constraint is
  calendar time (~1–2yr)"; the 40% consistency rule DOES bind for this pyramided shape
  specifically. Same-day sibling 6J branch found a structurally identical IS claim and
  falsified it on OOS — cross-branch caveat recorded in M8; **no MYM holdout remains** to run
  the same test. An offline re-simulator built this session FAILED validation (scale-in adds
  fill at bar close, not trigger) and was discarded — every number above is TV-native or
  export-anchored. Does not touch the LIVE `trend-following` M1 leg or the DEAD
  `opening-range-continuation` M2 mechanism — a separate candidate on a separate track.
  Evidence untracked (Downloads lane) — `orb_mym_1/2/3_edition.pine` + survey MD + addenda,
  local only, not in this repo. $0/K=0 (disclosed informal search + TV tuning; re-proposal
  would need K accounting if ever promoted into the repo pipeline).
- **2026-08-14 (Stage-1)** — **MSL-S2B STAGE-1 FAIL (route)** ([`STAGE1.md`](../../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) · [closure](../../docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md)). Raised bar unbound for continuation *entry*; SLR route ① filter-only; temporal-selectivity paused; composite refused. B8 occupancy CLEAR. No G0 / Pine / $0 · K=0.
- **2026-08-13 (explore)** — **MSL-C1 FALSIFIED** ([`RESULTS_g2.md`](../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](../../docs/briefs/closures/MSL-C1-closure-falsified.md)). Both arms CI upper &lt; 0; CONFIRM unread; $0 · K=0.
- **2026-08-13 (G0)** — **MSL-C1 G0 FROZEN** ([`PREREG_G0.md`](../../lab/archive/msl_c1_mym_2026-08/PREREG_G0.md)). Operator B4 GO; `K_intrinsic=1`; CONFIRM `2025-09-01→2026-08-13` reserved unread. $0 · K=0.
- **2026-08-13 (Stage-1)** — **MSL-C1 Stage-1 PASS** ([`STAGE1.md`](../../lab/archive/msl_c1_mym_2026-08/STAGE1.md)). After C3 [OPERATOR-KILL](../../docs/briefs/closures/MSL-C3-closure-operator-kill.md); elected existing `pdh-pdl-failed-break-reclaim` on MYM; route ① + B8 occupancy CLEAR; three kill limbs PASS at RT $2.82 / stop 320 pts / 4 contracts ($0.50/pt). No Pine, pull, $0 · K=0.
- **2026-08-12** — **Occupancy RELEASED for new non-Striker research/G0 (MSL Board B8).** [`ADR`](../../docs/adr/2026-08-12-msl-mym-occupancy-release.md): `MYM1!` headroom is no longer reserved by the withdrawn Striker DJ30 leg for MSL / Tradeify-shaped candidates (incl. MSL-C1). **Unchanged:** S1 keep-warm/disarmed; de-scope Striker redeploy bar; no `LEG_MAP` code edit; no arming. The 2026-08-04 “not thereby released / get F2 ruled” posture is discharged by that ADR for this scope. $0/K=0.
- **2026-08-04b** — **Cross-reference: MYM's own measured 0.49R edge included in the slow-archetype eval-time-limit study (MNQ.md N13).** Tradeify's Select 100K eval confirmed to have no time limit (verified in-browser, three primary sources). At k=1 (independent), safely sized to the rope, MYM's edge produces a **46-day median pass at 0.8% bust** and clears the $200 funded floor. Weaker than MNQ's 0.85R row (21 days) but not disqualifying — the constraint MYM actually failed in the funded-phase de-scope (pyramid-dependent, >40-micro days) is untouched by this study, which is flat-sized. $0/K=0. [`RESULTS`](../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md)
- **2026-08-04** — **MYM loses its live-leg standing.** The Tradeify venue was de-scoped as a program target **including the evaluation** ([`ADR`](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)); the Striker DJ30→MYM leg is withdrawn from deployment having never taken a strategy-signal-originated fill. **`Striker` lifecycle UNCHANGED at `AUTHORIZED @ 1.00×`** — no demotion, no `lifecycle.py` write; venue-fit is not decay, and the ladder is a decay instrument with zero live fills to trigger Call 1. ⚠ **Consequence for S3 order-symbol occupancy:** the incumbent's claim on `MYM1!` Tue+Fri was predicated on a *deployed* leg. It is **not** thereby released — the legs are withdrawn from a venue, not parked, and `LEG_MAP` is untouched; any candidate reasoning from a freed `MYM1!` must first get fork **F2** (rail disposition) ruled. Reconstruction track stays **TERMINAL**; the 5 DEAD rows and the bank-1 arithmetic are unaffected. No `core/`, lock, allocation, `dd_protection`, Pine, rail, or `LEG_MAP` change.
- **2026-08-02** — **Hosted the out-of-sample confirmatory limb of `Q-DRIFTEX-1`** (drift exhaustion against a constant hazard). **No MYM construct was proposed, scored, or promoted** — MYM was used strictly as a **bar-level property** panel, so the `opening-range-continuation` DEAD row and the TERMINAL reconstruction ruling are untouched; the K bank is **unchanged at 1** and **$0 / K=0 / no manifest**. Result: **FALSIFIED**. L1 (drift decay) PASSED — NW(5) slope −7.015e-05/min, **t = −2.522**; L2 (flat hazard) PASSED — expected 4.07% vs observed **3.91%**, dev −3.9%; but **`t*` came out degenerate at 195.5 min = 03:15 ET**, before the session opens (fitted drift 0.0123 already below a 0.0407 hazard cost at 10:00), so P3 missed by **719.5 min against a 45-min tolerance**. **Two MYM facts worth keeping:** (a) MYM's exit-time ladder is **negative at every horizon** (best cell +0.001 @ 15:15, full session −0.101) — its argmax coincides with MNQ's, so the *phenomenon* replicates while the *mechanism* does not; (b) MYM's final-block signed drift is **−0.02999 with cross-day sd 0.529** ⇒ **t = −2.18**, sitting *at* the expected max of 11 blocks, i.e. unremarkable once multiplicity is counted. That measurement is what closed the end-of-day line as tail-exhausted (raised bar in [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md)). Panel pin: `MYM_M15.csv` sha256 `24e169528f7ea669…`, 2020-07-02 → 2026-07-02, 1,548 days / 1,538 breakout days. No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.
- **2026-07-30** — **Forced-flow census pass 2** (`N-2026-07-26-forced-flow-census.md` §PASS 2; pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`) screened MYM as the **alternate** host for `PROPENG-RATCHET` (prop-engine peak-anchored liquidation-cascade fade) — verdict **`UNSCREENABLE-PROBE`, BLOCKED**, no probe licensed. Why MYM is the alternate rather than the primary: the $0 in-repo 1m panel makes it the cheap probe home, but a probe must run on the **target's own cohort** (Req-2 forbids cross-instrument transplant), so electing MYM pins the target to MYM and spends its bank (1 → 2, `K_eff` 2, floor **0.850**). **Blocking issue, unresolved:** a sim-vs-live **transmission contradiction** — a sibling screen established (screen-verified, not parent-verified) that the named prop cohort largely fills against **simulated** books, which would void clause (i); a dedicated adjudication was launched twice 2026-07-30 and did not complete. **Two standing MYM constraints re-confirmed against this candidate:** (a) the ⚠ unreconciled `S-MYM-ORC-02` K=2 claim remains a live contingency — if ever ruled bankable the family reaches `K_eff` 4 ⇒ floor **1.06 > Cap**, closing MYM to new seeds *including this one*; (b) **S3 order-symbol occupancy** binds at deployment (not at probe) — MYM1! Tue+Fri stay closed until the Striker leg parks and its TradingView alerts are deleted, and the census's config-A long-only framing exists precisely to defer that. Distinct from the DEAD rows above: not continuation (`S-MYM-ORC-02`), not settlement-calendar (`MYM-3FPS-1`), and not `SLR-MYM-1` — which it answers rather than repeats, being the first census entry to pass **both** delete and flip on the SLR §2-A standard. **K bank unchanged at 1; $0 spent, 0 K consumed, no manifest, no pre-registration.** No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.
- **2026-07-29** — `SLR-MYM-1` (liquidity sweep-and-reclaim at the open) opened and **closed at Stage 0** the same cycle: `FALSIFIED (as scoped)`, **$0 spent, 0 K consumed, no manifest opened, no pre-registration authored**. Two independent gates fired — harvest Req-1a (both constraint framings fail the delete/flip tests) and **S3 order-symbol occupancy** (new standing constraint, recorded above). Added the `ict-liquidity` cell + DEAD row. **Corrected the stale "K bank remains 0" line to 1** per ADR 2026-07-26 §2-C, and disclosed the unreconciled `S-MYM-ORC-02` K=2 claim. Independently re-verified the Tradeify rule pins against the firm's published policy article and reached the same result as the parallel session that landed [`2026-07-24-tradeify-rulepin-verification.md`](../../docs/notes/2026-07-24-tradeify-rulepin-verification.md) (PR #545): $200 winning-day minimum **confirmed**; "40-micro funded start tier" **refuted** (actual 30, four-step equity ladder); Flex minimum payout **mis-attributed**. That note is canonical — this branch's duplicate was deleted at merge. No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.
- **2026-07-25** — Ledger created (attention-efficiency audit). Seeded W1–W4, M1–M7, and the DEAD list from the ORC-01/02, MYM-3FPS-1, OPENPRESS-1 and book-composition records. Recorded W3 (vendor refresh invalidating a frozen research pin) as a standing warning. No `core/`, lock, allocation, `dd_protection`, or Pine change.
