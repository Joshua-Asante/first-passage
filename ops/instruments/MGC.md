# INSTRUMENT LEDGER — MGC

**Symbol:** COMEX Micro Gold futures (MGC; Globex, Databento `GLBX.MDP3`) · **Parent family:** GC (un-ledgered as futures parent; CFD sibling [`XAUUSD.md`](XAUUSD.md) is a different venue) · **Asset class:** metals futures
**Status:** **RE-ENTERED — K-void cleared; class-attested; not elected.** Research/discovery only. Third-leg `E-K` elimination voided by [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md); DISC-CAMP-0 family history is **disclosure / Req-3 bank fact**, not inherited elimination. No live leg, no allocation, no K spend. ⚠ **`Tradeify_Select_100K` CLOSED** (operator-ratified 2026-08-25 — granularity wall, see W5/G5); scoped to that firm-tier only, does not touch MGC's general research status.
**Last updated:** 2026-08-25

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created **2026-08-09** as the live touching session for [`instrument-lane SPEC`](../../docs/spec/2026-08-09-instrument-lane-mcl-mes-mgc-spec.md) — ADR [`2026-07-25`](../../docs/adr/2026-07-25-instrument-profile-index.md) §5. Thin ledger.

## PROFILE (machine-readable)

```yaml
symbol: MGC
asset_class: metals-futures
family: []
venue_tradable: true
venue_note: "Tradeify Metals Product Group (GC/QO/MGC/SI/HG/PL/PA). Micro proxy vs GC — re-scale economics; do not inherit parent fill model."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: event-window-reversal
    verdict: DEAD
    date: 2026-08-10
    source: "../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md"
  - mechanism: daily-range-state-persistence
    verdict: DEAD
    date: 2026-08-18
    source: "../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md"
  - mechanism: london-range-failed-extension-fade
    verdict: DEAD
    date: 2026-08-13
    source: "../../docs/briefs/closures/MSL-C2-closure-falsified.md"
  - mechanism: expiry-oi-strike-convergence
    verdict: AMBIGUOUS-PARKED
    date: 2026-08-21
    source: "../../lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md"
bars:
  - id: free-data-5th-leg-snag-closed-2026-07-01
    source: "../../docs/rejected_candidates.md"
structure:
  - claim: "Third-leg E-K elimination is void as a gate after K-bank ADR; large disclosed bank remains a Req-3 fact, not an inherited kill. DISC-CAMP-0 history is disclosure, not re-litigation."
    source: "#G1"
```

---

## STANDING WARNINGS

- **W1 — Metals Product Group / hedge overlay.** Same-group opposing signs violate envelope §4a if co-accounted. Design sign-constrained when co-legged.
- **W2 — Micro vs GC proxy discipline.** Deep history may use GC parent; re-scale tick/margin; reserve native-micro era as OOS ([databento proxy-discipline](../../.claude/skills/databento-data/reference/proxy-discipline.md)).
- **W3 — No Stage-2 σ/τ measured here.** Third-leg N was `—`. Do not invent cells. Future panel need → estimate → operator GO.
- **W4 — DISC-CAMP-0 is closed calibration, not a reopenable kill on MGC alone.** Cite manifests / campaign artifacts for bank facts; do not hardcode floors as gates ([K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
- **W5 — `Tradeify_Select_100K` granularity wall (CLOSED, operator-ratified 2026-08-25).** MGC's smallest tradeable unit (1 micro) costs a firm-tier-**dependent** share of that tier's DD rope, not a fixed %. At a 0.75×ADR20 stop and $10/pt: **6.7% of the $3,000 Select rope in 2022** (ADR20 ≈27pts) vs **34% in 2026** (ADR20 ≈136pts). Vol-scaled sizing does NOT rescue this — tested null, implied qty stays 1.00–1.25 contracts every year (no gear below 1 micro); dropping the 1-contract floor instead makes the construct never trade (100% unresolved). Not a mechanism finding — applies regardless of signal. Scope is `Tradeify_Select_100K` at 2026 volatility specifically — re-run the division (`min-unit stop $ ÷ tier rope $`) before trusting this at a different tier or a calmer regime. Evidence: informal Downloads-lane survey + rope-walk sim, untracked by design (operator-selected lane) — no in-repo artifact; see SESSION LOG 2026-08-25.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **G1** | **Voided kill: `E-K`.** Third-leg map eliminated MGC (bank 3177 → floor 2.05 > Cap). Banner + K-bank ADR: Clause K no longer eliminates; bank is disclosure (still large — cite manifests, don’t hardcode as authority). | [`third-leg RESULTS`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md) L35 + banner | **HIGH** (ADR void). |
| **G2** | **Standing non-K grounds.** Metals Product Group · E1–E7 class-fit · DISC-CAMP-0 family history as disclosure/Req-3 bank fact · micro proxy vs GC · cost-tax from third-leg row (re-cite: cost-tax 1t r=1 **0.0902**). | third-leg RESULTS · envelope · [`lab/CATALOG.md`](../../lab/CATALOG.md) disccamp0 row | **HIGH** as posture. |
| **G3** | **Envelope + TNEC class attestation (no candidate).** See table. N-SIZE = U. | this session | **MODERATE**. |
| **G4** | ⚠ **CORRECTED 2026-08-18 — test invalidated, see [audit note](../../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md).** `H-RANGESTATE-GC-1` (S1a, Step-0 slate row S1) — ledger cell verdict `AMBIGUOUS-PARKED` (unchanged). Daily top-quintile-TR → elevated-next-day-TR conditioner, GC parent train era. **Raw battery reading `NULL`** (conditional hit rate 0.5299, n=451/2,116; CI lower bound 0.4545 fails by 4.55pp) — **bottom line unchanged**, but the placebo pass (p=0.0095) originally cited as partial corroboration is **not valid corroboration**: the sibling CL screen (S1b) showed this same placebo construction is cleared by zero-mechanism AR(1) surrogates at a *higher* rate than either real dataset. Do not cite "3 of 4 limbs pass" as meaningful; the CI-limb failure is the only trustworthy reason this cell is `NULL`. The "live prior for MCL" framing originally here is retracted — S1b's own raw SIGNAL was independently downgraded to NOT-CONFIRMED for the identical reason. | [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) (correction banner) · [`RESULTS_S1B.md`](../../lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md) | **HIGH** (frozen prereg, adversarially verified; battery defect itself is HIGH-confidence, quantified via 20/20 surrogate trials). |
| **G5** | ⚠ **`Tradeify_Select_100K` CLOSED (operator-ratified 2026-08-25) — granularity-blocked, not a mechanism kill.** 1-micro min-risk ÷ tier rope = 34% at 2026 volatility (was 6.7% in 2022); vol-scaled sizing tested NULL (implied qty 1.00–1.25 every year, no sub-micro gear; dropping the floor instead never trades). Scope-limited to this firm-tier at current volatility — see W5. | this session (2026-08-25) — informal Downloads-lane survey + rope-walk sim; no in-repo artifact | **HIGH** (bar-honest sim mirrors `core/mc/simulation.py` `trailing_locking` semantics; not yet TV-native validated — treat the qualitative wall as robust, exact magnitudes as directional). |

### Envelope E1–E7 + TNEC class attestation

| Limb | Token | Grounds (one line) |
|---|---|---|
| E1 EOD flat | **P** | Micro metals; flat-by-16:00 build target design-legal. |
| E2 Consistency | **P** | Soft checkpoint; no instrument-specific kill. |
| E3 Trailing DD | **P** | Intraday trail firm-parameter; no MGC-specific foreclosure. |
| E4 Daily loss | **P** | Present-by-default. |
| E5 Micro sizing | **P** | MGC is the micro unit vs GC. |
| E6 Attended automation | **P** | Envelope default. |
| E7 News/event | **N/A** | Overlay-only — default does not constrain. |
| N-SHAPE | **P** (class) | Metals Product Group · micro-expressible · flat target; sign-constrain if co-legged (§4a). |
| N-SIZE | **U** | No candidate edge; frontier re-derives per candidate. |

**Dated disposition token:** `RE-ENTERED — K-void cleared; class-attested; not elected`

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator | Source |
|---|---|---|
| ~~`E-K` (third-leg)~~ | **VOID as gate** — K-bank ADR; bank remains disclosure | RESULTS banner 2026-08-04+ |
| DISC-CAMP-0 wide mining (GC/MGC family) | Closed campaign — **disclosure / Req-3**, not inherited MGC elimination | campaign artifacts via [`lab/CATALOG.md`](../../lab/CATALOG.md) |
| Benchmark-fix-window flow (LBMA PM/AM fix) on GC/MGC — family-scoped to venue-legal metals incl. SI/SIL · mechanism cell `event-window-reversal` | **Informed-flow + Req-5 cost-law, on the seed's own record** (replaces the void 2026-07 R8 K-kill). Caminschi–Heaney *JFM* 2014 (DOI `10.1002/fut.21636`) GC cohort: adjusted (fix-direction-signed) drift ~9.6+4 bp is participant-knowledge — inadmissible; **public unadjusted first-2-min ≈ −1.8 bp, i=3,4 n.s.**; causal MKTDIR residue **1.32–3.21 bp/event** vs 4× hurdles **6.34–10.30 bp (MGC)** / **3.40 bp (full GC, generous top)** — under at every legal expression *before* the adverse post-2015-reform haircut (*JFM* 2020: spreads↓ depth↑). **ENV-1 concordant kill (second unit system):** envelope re-score δ **8.35 ticks** vs **11.6-tick** 4× hurdle → `FAIL/cost` ([`mgc-benchmark-fix-window-r8-rescore.json`](../../lab/archive/tnec_envelope_compile_2026-08/entries/mgc-benchmark-fix-window-r8-rescore.json); [`N-2026-08-11-daily-auction-settlement-MGC.md`](../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MGC.md)). **Re-proposal bar** (quoted from R8 closure): *a post-reform, publicly-conditioned cohort δ ≥ the 4× hurdle at a named venue-legal expression — not a re-read of pre-reform tables, not the informed-side numbers, not a window re-tune* | `SCREEN-FAIL` 2026-08-10 — [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) |
| `london-range-failed-extension-fade` × MGC (MSL-C2) | Explore IS both-arms session-block 95% CI entirely &lt; 0 (long n=327; short n=310; mean ≈ −0.18R). CONFIRM unread. | FALSIFIED 2026-08-13 — [closure](../../docs/briefs/closures/MSL-C2-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md) |

## ACTIVE / OPEN

- **MSL-S4 `expiry-oi-strike-convergence` — G0 FROZEN 2026-08-21, Explore-confirm RUN 2026-08-21 →
  `AMBIGUOUS-HOLD` → operator `PARKED` 2026-08-21.** First WHO named since the 2026-08-14
  estate-wide WHO-track sweep found the door dry; discharges E1. Explore-confirm (deferred at
  freeze, no data access) ran on 75 IS-window cycles: negative-signed real effect (net divergence,
  not convergence), `p_upper=0.5724` not significant, FLIP-FAIL. Not formally FALSIFIED under the
  frozen gate's literal threshold, but the operator elected to park the card rather than pursue a
  TV backtest or further build-out —
  [`candidates_CARD.md`](../../core/strategies/candidates/candidates_CARD.md). Re-proposal bar:
  new mechanism evidence, not a θ-retune or a re-read of this same result. See
  `lab/analysis/c1/msl_s4_mgc_2026-08/`.
- Instrument-lane re-screen complete 2026-08-09. Election out of scope.
- Self-funded Guardian→MGC lane remains PARKED/CLOSED (program posture); this ledger does not reopen it.

## SESSION LOG

- **2026-08-25** — **`Tradeify_Select_100K` CLOSED (operator-ratified) — granularity wall, not
  a mechanism kill.** Downloads-lane survey (6 families / ~46 disclosed cells, all NULL;
  least-bad construct — session-open-sign continuation, long arm — FALSIFIED out-of-sample, IS
  PF 1.23 → OOS PF 0.85) plus a bar-honest Tradeify rope walk (mirrors
  `core/mc/simulation.py` `trailing_locking` semantics) found MGC's smallest tradeable unit (1
  micro) costs **6.7% of the $3,000 Select rope at 2022 volatility but 34% at 2026 volatility**
  (0.75×ADR20 stop, $10/pt — ADR20 27pts → 136pts across the panel). Vol-scaled sizing (the
  textbook fix for this exact diagnosis) was tested and is **NULL**: holding dollar risk
  constant implies 1.00–1.25 contracts in every year — there is no gear below one micro to
  scale into; dropping the 1-contract floor instead makes the construct never trade (100%
  unresolved). Scope is `Tradeify_Select_100K` specifically, not a blanket MGC kill — see
  W5/G5. Operator: *"closing MGC out as an instrument for the Tradeify eval."* Evidence
  deliberately untracked (operator-selected informal Downloads lane, not a formal repo
  campaign) — `MGC_15m_edge_survey_2026-08-25.md` + `mgc_pm_continuation_v0.2.pine`, local
  only, not committed to this repo. $0 / K=0 (disclosed informal search; re-proposal at this
  tier would need K accounting per the survey's own restraint log).
- **2026-08-21e** — **MSL-S4 candidate `PARKED`** (operator decision, post-`AMBIGUOUS-HOLD`
  Explore-confirm) — [`candidates_CARD.md`](../../core/strategies/candidates/candidates_CARD.md).
  Not `FALSIFIED_PARKED` (the frozen `p_upper>0.95` line wasn't crossed). Never hash-pinned.
- **2026-08-21d** — **MSL-S4 Explore-confirm EXECUTED (not just drafted)** — 75 completed
  weekly+monthly OG cycles pulled (IS window only, CONFIRM never read), pilot-calibrated
  rank-ACF tolerance fresh (not borrowed from the corrected-null-battery's own numbers), official
  IAAFT test (M=1000, frozen seed block) + delete/flip run. **Verdict `AMBIGUOUS-HOLD`**: real mean
  displacement reduction is negative (−5.52pts, net divergence) at the 42.8th percentile of the
  surrogate null (`p_upper=0.5724`, not significant); FLIP FAILs (divergence beats convergence).
  Not formally FALSIFIED under the frozen `p_upper>0.95` line, but the qualitative story (wrong
  sign + FLIP-FAIL) reads the same as most FALSIFIED cases this program has produced. `K_intrinsic`
  unchanged. $0 / K=0.
  [`_explore_confirm_2026-08-21_LOG.md`](../../lab/analysis/c1/msl_s4_mgc_2026-08/_explore_confirm_2026-08-21_LOG.md).
- **2026-08-21c** — **MSL-S4 real Explore-confirm drafted** — the informal cheap falsifier's
  fixed-offset control turned out trend-confounded (same cycles converged/diverged in both
  windows); corrected design adopts an IAAFT-surrogate null (same methodology this repo already
  proved out for `daily-range-state-persistence`'s analogous autocorrelation confound), weeklies +
  monthlies, and a partition boundary excluding what's already been viewed. Statistical core
  unit-tested (23/23) on synthetic data; no live pull yet. $0 / K=0.
  [`EXPLORE_GO.DRAFT.md`](../../lab/analysis/c1/msl_s4_mgc_2026-08/EXPLORE_GO.DRAFT.md).
- **2026-08-21b** — **MSL-S4 Stage-1 PASS → operator B4 GO → G0 FROZEN → Pine authored CC-solo,
  same session.** New mechanism `expiry-oi-strike-convergence` (NEW, `MECHANISMS.md`): near a
  published Gold options expiry, price converges toward the strike carrying the largest open
  interest; entry direction read off observable price-vs-strike displacement, never off an
  assumption about dealer gamma sign — the reason it survives where a directional dealer-gamma
  sibling construct stays dead (BE1 sign-not-entailed). BINDING BAR
  `free-data-5th-leg-snag-closed-2026-07-01` answered **CLEAR via R-FRAMING §2.1**, inheriting
  MSL-C2's own resolution of the identical bar. RT $4.12 screens PASS. Cheap falsifier NOT
  AVAILABLE (no market-data access this session — disclosed, not skipped). Explore-confirm
  (charter step 5a) **deferred by explicit operator override** — no `SHAPE-CLEAR` verdict exists;
  Pine was authored directly off the frozen construct, with the operator's own TV backtest named
  as the first empirical evidence instead. Sourced by a dedicated cross-lane search after the
  estate-wide WHO-track (2026-08-14) found the door dry — first WHO discharging that stop rule.
  $0 / K=0 (nothing scored on real data). [`STAGE1`](../../lab/analysis/c1/msl_s4_mgc_2026-08/STAGE1.md) ·
  [`PREREG_G0`](../../lab/analysis/c1/msl_s4_mgc_2026-08/PREREG_G0.md) ·
  [`RUNBOOK`](../../lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md).

- **2026-08-18c** — **OFFICIAL corrected-null re-score: cell → `DEAD`; near-miss framing
  retracted (CASE A).** Under the frozen class battery (IAAFT normal-scores null + L4 by-year
  limb, [spec+ADDENDUM-1](../../docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md)):
  **NULL (driving L2+L4)** — obs 0.5299 at the **8.4th pct** of GC's own linear-ACF band
  (below the zero-mechanism benchmark's center); by-year 5/9 vs required 7. No SUB-LINEAR flag
  (p_lower 0.0849); real lift at the 41st pct of the surrogate lift band (base-rate artifact
  note per A13). Re-proposal bar: corrected battery + different construction or longer panel.
  $0 / K unchanged (re-measurement). [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) §6 ·
  [`RESULTS_CORRECTED.md`](../../lab/analysis/_inbox/rangestate_corrected_2026-08/RESULTS_CORRECTED.md)
- **2026-08-18b** — **G4 corrected — placebo test invalidated, not the bottom-line verdict.**
  Adversarial review of the sibling CL screen (S1b) found the four-limb battery's placebo does
  not control for True-Range autocorrelation (20/20 zero-mechanism AR(1) surrogates cleared it
  at a higher rate than the real data). S1a's `NULL` stands (CI limb independently fails), but
  the placebo-pass corroboration and "live prior for S1b" framing are retracted. Audit note:
  [`2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md`](../../docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md).
  $0 / K=0 (correction only, no new spend).
- **2026-08-18** — **`H-RANGESTATE-GC-1` (Step-0 slate S1a) → NULL, near-miss.** Daily
  range-state persistence conditioner screened on GC train era ($0, K=1 disclosed). 3/4 limbs
  pass; CI lower bound fails by 4.55pp. Adversarially verified before trust (4-lens workflow
  caught + fixed a CI-block-size defect, verdict-preserving). New `MECHANISMS.md` heading
  `daily-range-state-persistence`. Routes to S1b (MCL) per the slate queue. $0 / K=1.
  [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md)
- **2026-08-13** — **MSL-C2 explore FALSIFIED** ([closure](../../docs/briefs/closures/MSL-C2-closure-falsified.md) · [`RESULTS_g2`](../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)). `london-range-failed-extension-fade` × MGC; both-arms IS 95% CI entirely &lt; 0; CONFIRM unread; $0 / K=0.
- **2026-08-12c** — **MSL P3.1 B4 GO → G0 FROZEN:** [`PREREG_G0`](../../lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md); explore/Pine unpaid. $0 / K=0.
- **2026-08-12b** — **MSL P3.1 Stage-1 PASS (pre-G0):** freeze `london-range-failed-extension-fade`; SNAG CLEAR via R-FRAMING §2.1; RT $4.12 screens PASS; delete/flip unpaid pending B4. [`STAGE1`](../../lab/archive/msl_c2_mgc_2026-08/STAGE1.md). $0 / K=0.
- **2026-08-12** — **PROFILE `bars:` Stage-0 (MSL P3.1 / C2):** registered `free-data-5th-leg-snag-closed-2026-07-01` → `docs/rejected_candidates.md` (SNAG-CLOSED 2026-07-01). Door-check non-vacuous; index OHLCV bar intentionally omitted (C2 outside that domain). `profiles.json` rebuilt same commit. $0 / K=0.
- **2026-08-11** — **PROFILE cell bound: `event-window-reversal` → `DEAD` (2026-08-10).** Q-TNEC-ENV-1 closure §4 named the missing consult cell (corpus-only prior). Cell source = R8 δ-extraction; DEAD-row updated with ENV-1 tick-concordant `FAIL/cost` (8.35 < 11.6) + notice. Re-proposal bar unchanged — quoted from R8's own closing terms. $0 / K=0 / no `core/` change. [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) · [`Q-TNEC-ENV-1-closure.md`](../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) · [`N-2026-08-11-daily-auction-settlement-MGC.md`](../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MGC.md)
- **2026-08-10b** — **R8 δ-extraction (operator GO) → `SCREEN-FAIL (informed-flow + Req-5 cost-law)`; DEAD-list row added.** Full text retrieved (UWA green-OA via the Pure API host — web-front copies are Cloudflare-challenged), tables extracted, arithmetic executed. The informed 9.6+4 bp is Req-2-inadmissible (third instance of the `H-FBEIA-1` signature); the causal public residue 1.3–3.2 bp/event fails every venue-legal 4× hurdle before the adverse post-reform haircut. Seed closes on its own mechanism record, as the re-stage intended. $0 / K=0 / no pull / manifests unchanged. [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md)
- **2026-08-10** — **TNEC L2 sourcing pass re-stages the gold PM-fix seed onto this instrument: `SEED-OPEN (δ-extraction owed)`.** `Q-INVENTORY-1` R8 (Caminschi–Heaney *JFM* 2014, DOI `10.1002/fut.21636`) was killed 2026-07 on **Req-3 FAIL-K only** — a kill class the [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) withdraws; no mechanism record exists to stand or fall on. Dedup executed (profile-consult `MGC event-window-reversal` → untested, no binding bar; registers + census clean; FX-fix cost kills disclosed as adjacency, not bar). Req-2 inputs named (pre-reform GC-cohort δ + *JFM* 2020 post-reform structural break `10.1002/fut.22120` — the 2015 auction reform is a mandatory decay input). **Not admissible; nothing screened on PnL.** Next step is operator-electable: ~$0 full-text δ extraction → §2.2 sniff vs the ≈6–8 bp/event MGC hurdle → manifest only on PASS. GC/MGC bank 3,177 (DISC-CAMP-0) disclosed. [`SOURCES_LOG`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/SOURCES_LOG.md). $0/K=0; no pull; no election; no `core/` change.
- **2026-08-09** — **Ledger created + K-void re-screen** under [`instrument-lane SPEC`](../../docs/spec/2026-08-09-instrument-lane-mcl-mes-mgc-spec.md). Voided `E-K` vs standing Metals / E1–E7 / DISC-CAMP-0-disclosure grounds named. Disposition `RE-ENTERED — K-void cleared; class-attested; not elected`. No pull, no K, no election, no `core/` change.
