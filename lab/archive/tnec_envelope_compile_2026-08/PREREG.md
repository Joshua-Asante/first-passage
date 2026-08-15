# SPEC: Q-TNEC-ENV-1 — TNEC envelope compile + aimed census (freeze)
Status: FROZEN · 2026-08-10 · authorizes nothing ($0 · K=0) · depends: TNEC-1 (RATIFIED 2026-08-08)
Objective: Compile the TNEC necessary-conditions envelope per instrument; iff NON-EMPTY somewhere, run one frozen-taxonomy census pass aimed at it.

Steps:
1. CC: build + test the arithmetic stack (instruments/envelope/runner); execute `--compile`.
2. CC: author RESULTS.md around the output; record the H_A verdict; board writes.
3. (gated on H_A NON-EMPTY) CC: author census entries per the frozen taxonomy; score via `--entry`; record H_B.
4. CC: closure with the pre-registered Iterate disposition; operator reads.

Gate: H_A RESOLVED-NON-EMPTY if ≥1 instrument has ≥1 cell with no kill; FALSIFIED if all instruments EMPTY.
      H_B RESOLVED if ≥1 census entry scores SEED-GRADE in one taxonomy pass; NULL if zero.
Boundary: no pulls · no MC · no PnL reads · no edits outside the campaign dir + notice logs + board files ·
          no re-derived constants (cost_model / floor_scan / firm_rules are the owners) · no threshold invention ·
          screen the class never a scored list (EM §2.0a) · outputs must be pre-committed K=1–2 (EM0) ·
          no loosening of Req 1–5 / EM0 / regime gate under cover of necessity (TNEC boundary).
Reads: docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md @ HEAD ·
       docs/spec/2026-08-05-eval-mechanism-shape-screen.md §2/§2.0a/§3a @ HEAD ·
       docs/methodology/strategy_harvest.md §1/§2.3/§5 @ HEAD ·
       lab/discovery/cost_model.py @ HEAD · lab/archive/q_kbudget_1_2026-07/floor_scan.py @ HEAD ·
       lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md + RESULTS_stage2.md @ HEAD ·
       lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md @ HEAD ·
       docs/notes/notice/N-2026-07-26-forced-flow-census.md @ HEAD
Owner: docs/superpowers/specs/2026-08-10-tnec-inverse-generation-design.md (design, ratified conversationally 2026-08-10)

## Freeze blocks (nothing below grows after this commit)

F1 — Instrument pool (7): MNQ, MYM, MES, MGC, M2K, MCL, M6A. Per the Stage-1 map's 2026-08-04
  supersession banner every row screens at K_eff = K_intrinsic (floor 0.650 at K=1); the old
  E-K / E-KCAP eliminations do not bind. M6E stays out (E-COST at Stage 1, unaffected by the K ADR).

F2 — Stop ladder, all instruments: {8, 20, 40, 80, 160} ticks. Tick-space is primary (convention-safe);
  a points column renders only where cost_model.SPECS carries the instrument's point_value.
  On MNQ this ladder reproduces the K-wall §3 rows {2, 5, 10, 20, 40} pt exactly (known-answer anchor).

F3 — Cost model: rt_cost_usd(spec, commission_per_side=0.95, slip_ticks, slip_convention="total_rt")
  with slip_ticks=1 PRIMARY (the Stage-1 map's frozen 1-tick execution model at the TNEC screen
  commission) and slip_ticks=0 DISCLOSURE (bare-commission $1.90 RT — the K-wall/EM1 basis).
  Req-5 admission hurdle: COST_LAW_MULTIPLE (4.0, imported) × RT, quoted in ticks per event.

F4 — Kill predicates (per cell; both owner-derived, nothing else kills a cell):
  K-QTY:  ⌊risk$ ÷ (stop_ticks × tick_value)⌋ < 1 at ALL hypothetical frontier risks
          {$250, $275, $325} (labels: hypothetical 0.49R/0.65R/0.85R — 2026-08-08 correction) → DEAD(qty).
  K-COST: required gross per trade at the 4× hurdle, in R of the cell's own stop —
          (COST_LAW_MULTIPLE × RT_$) ÷ (stop_ticks × tick_value) — exceeds 0.85R, the best-ever
          measured construct band on record (hypothetical-labeled reference; K-wall §2 precedent
          "K=3 only for a candidate expected to beat every result on record") → DEAD(cost).
  Cells also report (never kill on): cost tax R, required-δ ticks, δ/stop ratio, 0.40R inversion
  line (disclosure only per TNEC-1), qty at each frontier risk, power floor.

F5 — Power rule: min detectable δ/σ = 1.96/√N at the instrument's committed N
  (Stage-1 own-panel N: MYM 484 · M2K 484 · MCL 251 · M6A 484; Stage-2 ex-FOMC slot overlay:
  450/450/233/450). MNQ/MES/MGC have no committed N ("—" at Stage 1): their power cell is
  UNSCREENABLE-INPUT(panel_N), route = re-derive the map's Slot-1 session arithmetic from the
  pre-prune tag. A cell whose ONLY unresolved wall is power is OPEN-CONDITIONAL(power) and
  counts toward NON-EMPTY (generous falsifier: a missing input must not manufacture EMPTY).

F6 — Phase-B taxonomy (8 classes; a class invented mid-pass is a new campaign):
  contract-roll mechanics · index-rebalance flows · expiry/settlement mechanics ·
  month-end/quarter-end benchmark flows · daily auction/settlement windows ·
  margin-cycle mechanics · mandated hedging programs (commodity/FX; dealer-gamma vendor-walled) ·
  eval-cohort mechanics.
  One pass over classes × NON-EMPTY instruments; entries in N-2026-07-26-forced-flow-census.md are
  re-scored, not re-enumerated. Entry contract: four Req-1a clauses + envelope-fit declaration
  (instrument+cell · cited δ source · event frequency vs power floor · horizon ≥5s · loss-shape note)
  + dedup attestation + instrument_profiles consult + venue check. Zero-K: no panel PnL examined.
  Stop rule: taxonomy exhaustion, regardless of count.

F7 — Dispositions (Iterate block, pre-registered):
  H_A EMPTY everywhere → STOP / FALSIFIED (board write; re-aims sourcing to transfer/Route A; no hook).
  H_B = 0            → STOP / NULL (envelope stands as documentation; re-entry = new class or new instrument).
  H_B ≥ 1            → INTEGRATE (propose ONE sourcing pointer line — strategy_harvest §2.3 census row
                        or TNEC-1 Reads — as its own operator-ratified edit; named, never executed here).
