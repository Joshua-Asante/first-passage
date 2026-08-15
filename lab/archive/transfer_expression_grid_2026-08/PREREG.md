# SPEC: Q-TXG-1 — transfer/expression grid Block 1 (freeze)
Status: FROZEN · 2026-08-11 · authorizes nothing ($0 · K=0) · depends: design RATIFIED 2026-08-11 · ENV-1 CLOSED NULL
Objective: Compile the 4×7 mechanism×instrument transfer grid through the Phase-A wall battery; record H_A.

Steps:
1. CC: build + test mechanisms/atr_map/walls/runner; execute `--compile`.
2. CC: author GRID_RESULTS.md around the output; record H_A; board writes.
3. (not this block) Block 2 election packet gated on H_A ≥1 OPEN + operator election.

Gate: H_A RESOLVED-OPEN if ≥1 cell is OPEN after the kill walls; FALSIFIED if zero OPEN
      (UNSCREENABLE / PARKED / WITHDRAWN do not count as OPEN).
Boundary: no pulls · no MC · no PnL/return reads · no edits outside the campaign dir + board files ·
          no re-derived constants (firm_rules / envelope / floor_scan are owners) · no Pine reads ·
          no locked-parameter edits · no Striker-book redeploy · no new instruments · no session variants ·
          S7 bindingness not adjudicated here (Block 2).
Reads: docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md @ HEAD ·
       core/firm_rules.py _BASE_RISK + Tradeify_Select_100K @ HEAD ·
       core/dd_protection.py calculate_protection lifecycle composition @ HEAD ·
       core/strategies/_archive/{guardian,striker,nas,aegis}/LOCK.md @ HEAD ·
       git show pre-prune-2026-08-08:docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md ·
       git show pre-prune-2026-08-08:docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md ·
       git show pre-prune-2026-08-08:docs/audits/2026-05-28-striker-dj30-v45-indicator-strategy-diff.md ·
       git show pre-prune-2026-08-08:docs/audits/2026-05-28-striker-nas100-v1-indicator-strategy-diff.md ·
       lab/archive/tnec_envelope_compile_2026-08/{envelope.py,instruments.py,RESULTS.md,PREREG.md} @ HEAD ·
       lab/analysis/c1/q_rail_1_2026-07/f2_floors.json @ HEAD ·
       lab/discovery/cost_model.py INSTRUMENT_SPECS @ HEAD ·
       lab/archive/q_kbudget_1_2026-07/floor_scan.py @ HEAD ·
       docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md @ HEAD ·
       docs/spec/2026-07-27-third-leg-target-spec.md §7.1 S7 @ HEAD ·
       docs/pursuits/{b1,b2,b8}-*.md @ HEAD ·
       docs/rejected_candidates.md @ HEAD
Owner: docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md

## §0 Citation-chain (stop geometry — version-anchored; Pine not read)

| Mechanism | Version | Risk key | SL×ATR | ATR len | Session / DOW | Tier-1 source (verbatim owner) | Corroboration |
|---|---|---|---|---|---|---|---|
| Guardian | v5.5 | guardian | 1.55×ATR | 14 | Mon/Tue/Thu · 0800–1600 UTC | `core/strategies/_archive/guardian/LOCK.md` locked config | pre-prune audit 2026-05-08 (`atrLength=14`); May-08 audit is entry-scoped — SL from LOCK |
| Striker DJ30 | v4.5 | striker | 1.20×ATR | 11 | Tue/Fri · 13–17 UTC | `core/strategies/_archive/striker/LOCK.md` locked config | pre-prune audit 2026-05-28 (`stopAtr=1.2`, session 13–17 UTC) |
| Striker NAS100 | v1 | striker_nas100 | 1.20×ATR | 11 | Mon/Tue · 13–17 UTC | `core/strategies/_archive/nas/LOCK.md` locked config | pre-prune audit 2026-05-28 (`stopAtr=1.2`, session 13–17 UTC) |
| Aegis | v4.3 | aegis | 1.42×ATR | 19 | Mon/Tue/Wed · 1000–1345 chart TZ | `core/strategies/_archive/aegis/LOCK.md` locked config | pre-prune audit 2026-05-28 (`atr_sl_mult=1.42`, `atr_period=19`) |

Risk% owner (live import at runner time, not transcribed): `firm_rules._BASE_RISK` =
`{"guardian": 0.0034, "striker": 0.0070, "aegis": 0.0150, "striker_nas100": 0.0037}`.
Lifecycle multiplier disclosed at 1.00× (all four AUTHORIZED · MECHANISM); composition owner
`dd_protection.calculate_protection` (multiplicative with DD_SCALE). Account:
`FIRM_RULES["Tradeify_Select_100K"]["starting_balance"]` = 100_000. Micro cap: ENV-1 `MICRO_CAP` = 80.

## Freeze blocks (nothing below grows after this commit)

F1 — Mechanism axis (4): guardian · striker · striker_nas100 · aegis. Parameter axis LOCKED;
  port = declared venue mapping only (design §7).

F2 — Instrument axis (7): MNQ, MYM, MES, MGC, M2K, MCL, M6A — owner ENV-1 PREREG F1.
  No new instruments.

F3 — Session axis: NOT COMPILED. Mechanism's own session is part of its expression.
  Slot overlay ($125 σ-ceiling, wed_thu, S7) disclosed per cell, never compiled.

F4 — Transfer-type tags (every cell):
  same-underlying: striker×MYM · striker_nas100×MNQ · guardian×MGC.
  cross-underlying: all other pairs. Cross-underlying cells carry the transplant prior
  (record 0/2 — EURGBP, USDCAD both dead) as a named burden, not a Block-1 kill.

F5 — Wall battery (kill walls first; disclosure walls never kill):
  W-DEDUP (kill): frozen disposition map below — WITHDRAWN(F1) / PARKED(b8) / DEAD(registry).
    Runner applies the map; execute-time `rg` + `instrument_profiles` consult is pasted into
    GRID_RESULTS.md §Dedup as attestation, not as a live branch.
  W-VENUE (kill): instrument must be venue-tradable at Tradeify Select (ENV-1 pool ∩ firm product
    set — all seven are); Equity Index Product Group ⇒ long-or-flat only (all four mechanisms are
    long-only by LOCK — clears); force-flat 16:45 ET vs mechanism session/exit — kill only if the
    locked session *requires* a hold past 16:45 ET (none of the four do: Guardian ends 16:00 UTC
    = 12:00 ET; Strikers 13–17 UTC = 09–13 ET; Aegis 10:00–13:45 chart). S7 occupancy = DISCLOSURE
    only in Block 1 (see §12.4).
  W-CAP (kill): qty = min(⌊balance × risk% × lifecycle / (stop_ticks × tick_value)⌋, 80) at the
    mapped stop cell (or at each ladder rung when stop UNSCREENABLE — see F6); DEAD(cap) if
    qty < 1 at locked 1.00× risk%. When stop UNSCREENABLE, evaluate qty at the ENV-1 OPEN rung
    with largest R/ct that still yields qty≥1 if any; if every ladder rung yields qty<1 → DEAD(cap);
    else W-CAP clears with disclosure `stop_unscreenable_qty_at_best_open_rung`.
  W-COST (kill): requires mapped stop cell (F6). cost_tax_r from `envelope.cell` at that rung.
    DEAD(cost) iff the ENV-1 cell `killed_by == "cost"`. measured_edge_R table is empty in Block 1
    (no PnL-derived constants); 6J +0.342R frictionless precedent is DISCLOSURE only (6J ∉ pool).
    OPEN cells carry required_net_R = cost_tax_r as the port-must-beat number.
  W-CADENCE / W-REGIME: DISCLOSURE only (design §4).

F6 — Stop-cell mapping (ATR-in-ticks → ENV-1 ladder `{8,20,40,80,160}`):
  stop_ticks = sl_mult × (atr_median_pts / tick_size).
  Map = nearest ladder rung by absolute distance (ties → larger rung).
  Committed ATR sources (ATR length must match mechanism):
    MYM / MNQ ATR(11): f2_floors.json recent_90d — usable by striker + striker_nas100 only.
    All other (mechanism, instrument) pairs → UNSCREENABLE-INPUT(stop_cell);
      route = "commit ATR(<len>)-matched median for <sym>; never invent".

F7 — Frozen W-DEDUP disposition map (28 cells; anything absent = no pre-kill):
  striker×MYM → WITHDRAWN(F1) — de-scope ADR; c1 leg withdrawn.
  striker_nas100×MNQ → WITHDRAWN(F1) — de-scope ADR; c1 leg withdrawn.
  guardian×MGC → PARKED(b8) — docs/pursuits/b8-guardian-mgc-transfer-lane.md (PROPOSED).
  aegis× (EURGBP/USDCAD/6J) → out of pool; registry DEAD cited at attestation only.
  guardian×XAGUSD → out of pool; SNAG-closed cited at attestation only.
  (Execute-time attestation may add DEAD(registry) rows if rg surfaces a pool cell kill —
   those land as GRID_RESULTS amendments in the same Block-1 RESULTS commit, not as quiet PREREG edits.)

F8 — Per-cell verdict vocabulary: OPEN · DEAD(<wall>) · UNSCREENABLE-INPUT(<x>) ·
  PARKED(b8) · WITHDRAWN(F1). First kill wall in order W-DEDUP → W-VENUE → W-CAP → W-COST wins.
  UNSCREENABLE on W-COST mapping does not by itself kill the cell if prior walls cleared —
  cell may still be OPEN with stop_cell unscreenable (cost numbers absent; port-must-beat row
  marks UNSCR). H_A counts only verdict == OPEN.

F9 — Dispositions (Iterate — Block 1 records H_A only; full closure is a later block):
  H_A EMPTY (0 OPEN) → jump to closure FALSIFIED (design §6 / §9) — out of Block 1 scope beyond
    recording the verdict + board write that Block 2 is not authorized.
  H_A ≥1 OPEN → Block 2 election packet authorized (operator elects or HOLDs).
