# INSTRUMENT LEDGER — MGC

**Symbol:** COMEX Micro Gold futures (MGC; Globex, Databento `GLBX.MDP3`) · **Parent family:** GC (un-ledgered as futures parent; CFD sibling [`XAUUSD.md`](XAUUSD.md) is a different venue) · **Asset class:** metals futures
**Status:** **RE-ENTERED — K-void cleared; class-attested; not elected.** Research/discovery only. Third-leg `E-K` elimination voided by [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md); DISC-CAMP-0 family history is **disclosure / Req-3 bank fact**, not inherited elimination. No live leg, no allocation, no K spend.
**Last updated:** 2026-08-12

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
    verdict: AMBIGUOUS-PARKED
    date: 2026-08-18
    source: "../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md"
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

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **G1** | **Voided kill: `E-K`.** Third-leg map eliminated MGC (bank 3177 → floor 2.05 > Cap). Banner + K-bank ADR: Clause K no longer eliminates; bank is disclosure (still large — cite manifests, don’t hardcode as authority). | [`third-leg RESULTS`](../../lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md) L35 + banner | **HIGH** (ADR void). |
| **G2** | **Standing non-K grounds.** Metals Product Group · E1–E7 class-fit · DISC-CAMP-0 family history as disclosure/Req-3 bank fact · micro proxy vs GC · cost-tax from third-leg row (re-cite: cost-tax 1t r=1 **0.0902**). | third-leg RESULTS · envelope · [`lab/CATALOG.md`](../../lab/CATALOG.md) disccamp0 row | **HIGH** as posture. |
| **G3** | **Envelope + TNEC class attestation (no candidate).** See table. N-SIZE = U. | this session | **MODERATE**. |
| **G4** | **`H-RANGESTATE-GC-1` (S1a, Step-0 slate row S1) — research verdict `NULL` (near-miss); ledger cell verdict `AMBIGUOUS-PARKED`** (the PROFILE `cells:` vocabulary has no `NULL` state — `AMBIGUOUS-PARKED` is the correct mapping: measured, inconclusive, blocking a same-cell re-attempt until the stated re-proposal bar is cleared). Daily top-quintile-TR → elevated-next-day-TR conditioner, GC parent train era (2010–2019, `MGC.v.0` 2019+ reserved). Conditional hit rate **0.5299** (n=451/2,116 scored); **3 of 4 frozen limbs pass** (n-floor, halves, placebo p=0.0095) — only the 60-day block-bootstrap CI lower bound fails (**0.4545**, 4.55pp under 0.50). Adversarially verified (4-lens + synthesis workflow) before trust: lookahead/leakage clean; one real defect caught and fixed pre-trust (CI block size 10d→60d + true circular wraparound, both corrections verdict-preserving and conservative — narrows toward NULL, not away from it). Live prior for the MCL sibling screen (S1b, same slate). | [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md) · [`PREREG_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/PREREG_S1A.md) | **HIGH** (frozen prereg, adversarially verified, $0/K=1 disclosed). |

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

## ACTIVE / OPEN

- Instrument-lane re-screen complete 2026-08-09. Election out of scope.
- Self-funded Guardian→MGC lane remains PARKED/CLOSED (program posture); this ledger does not reopen it.

## SESSION LOG

- **2026-08-18** — **`H-RANGESTATE-GC-1` (Step-0 slate S1a) → NULL, near-miss.** Daily
  range-state persistence conditioner screened on GC train era ($0, K=1 disclosed). 3/4 limbs
  pass; CI lower bound fails by 4.55pp. Adversarially verified before trust (4-lens workflow
  caught + fixed a CI-block-size defect, verdict-preserving). New `MECHANISMS.md` heading
  `daily-range-state-persistence`. Routes to S1b (MCL) per the slate queue. $0 / K=1.
  [`RESULTS_S1A.md`](../../lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md)
- **2026-08-12c** — **MSL P3.1 B4 GO → G0 FROZEN:** [`PREREG_G0`](../../lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md); explore/Pine unpaid. $0 / K=0.
- **2026-08-12b** — **MSL P3.1 Stage-1 PASS (pre-G0):** freeze `london-range-failed-extension-fade`; SNAG CLEAR via R-FRAMING §2.1; RT $4.12 screens PASS; delete/flip unpaid pending B4. [`STAGE1`](../../lab/archive/msl_c2_mgc_2026-08/STAGE1.md). $0 / K=0.
- **2026-08-12** — **PROFILE `bars:` Stage-0 (MSL P3.1 / C2):** registered `free-data-5th-leg-snag-closed-2026-07-01` → `docs/rejected_candidates.md` (SNAG-CLOSED 2026-07-01). Door-check non-vacuous; index OHLCV bar intentionally omitted (C2 outside that domain). `profiles.json` rebuilt same commit. $0 / K=0.
- **2026-08-11** — **PROFILE cell bound: `event-window-reversal` → `DEAD` (2026-08-10).** Q-TNEC-ENV-1 closure §4 named the missing consult cell (corpus-only prior). Cell source = R8 δ-extraction; DEAD-row updated with ENV-1 tick-concordant `FAIL/cost` (8.35 < 11.6) + notice. Re-proposal bar unchanged — quoted from R8's own closing terms. $0 / K=0 / no `core/` change. [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) · [`Q-TNEC-ENV-1-closure.md`](../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) · [`N-2026-08-11-daily-auction-settlement-MGC.md`](../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MGC.md)
- **2026-08-10b** — **R8 δ-extraction (operator GO) → `SCREEN-FAIL (informed-flow + Req-5 cost-law)`; DEAD-list row added.** Full text retrieved (UWA green-OA via the Pure API host — web-front copies are Cloudflare-challenged), tables extracted, arithmetic executed. The informed 9.6+4 bp is Req-2-inadmissible (third instance of the `H-FBEIA-1` signature); the causal public residue 1.3–3.2 bp/event fails every venue-legal 4× hurdle before the adverse post-reform haircut. Seed closes on its own mechanism record, as the re-stage intended. $0 / K=0 / no pull / manifests unchanged. [`DELTA_EXTRACTION_R8.md`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md)
- **2026-08-10** — **TNEC L2 sourcing pass re-stages the gold PM-fix seed onto this instrument: `SEED-OPEN (δ-extraction owed)`.** `Q-INVENTORY-1` R8 (Caminschi–Heaney *JFM* 2014, DOI `10.1002/fut.21636`) was killed 2026-07 on **Req-3 FAIL-K only** — a kill class the [K-bank ADR](../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) withdraws; no mechanism record exists to stand or fall on. Dedup executed (profile-consult `MGC event-window-reversal` → untested, no binding bar; registers + census clean; FX-fix cost kills disclosed as adjacency, not bar). Req-2 inputs named (pre-reform GC-cohort δ + *JFM* 2020 post-reform structural break `10.1002/fut.22120` — the 2015 auction reform is a mandatory decay input). **Not admissible; nothing screened on PnL.** Next step is operator-electable: ~$0 full-text δ extraction → §2.2 sniff vs the ≈6–8 bp/event MGC hurdle → manifest only on PASS. GC/MGC bank 3,177 (DISC-CAMP-0) disclosed. [`SOURCES_LOG`](../../lab/analysis/harvest/tnec_l2_sourcing_2026-08-10/SOURCES_LOG.md). $0/K=0; no pull; no election; no `core/` change.
- **2026-08-09** — **Ledger created + K-void re-screen** under [`instrument-lane SPEC`](../../docs/spec/2026-08-09-instrument-lane-mcl-mes-mgc-spec.md). Voided `E-K` vs standing Metals / E1–E7 / DISC-CAMP-0-disclosure grounds named. Disposition `RE-ENTERED — K-void cleared; class-attested; not elected`. No pull, no K, no election, no `core/` change.
