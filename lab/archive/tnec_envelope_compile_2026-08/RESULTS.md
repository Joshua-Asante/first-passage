# Q-TNEC-ENV-1 — TNEC envelope compiled per instrument

**Status:** CLOSED — H_B = 0, STOP / NULL per PREREG F7 · closure: docs/briefs/closures/Q-TNEC-ENV-1-closure.md
**Date:** 2026-08-11 · **Runner:** [run_envelope_compile.py](run_envelope_compile.py) · **Raw:** [RESULTS.json](RESULTS.json)
**Cost: $0.00 · K=0 · no manifest · no data pull · no network.** Pure arithmetic on committed constants
(owners: `cost_model.py`, `floor_scan.py`, Stage-1/2 instrument map, `firm_rules.py` via TNEC-1).
No candidate is proposed, admitted, scored, or licensed.

## §1 Why this exists
TNEC-1 (RATIFIED 2026-08-08) states the necessary conditions as limbs; the numbers existed for MNQ only
(K-wall §3). This compiles the envelope for the full measured pool so generation aims at a real region
instead of discovering the walls after authoring. Design: docs/superpowers/specs/2026-08-10-tnec-inverse-generation-design.md.

## §2 The compiled envelope

**Basis:** Tradeify_Select_100K eval - commission $0.95/side (TNEC-1 N-EDGE screen; actual $0.91) - slip 1 tick total_rt PRIMARY (Stage-1 map execution model), slip 0 DISCLOSURE - edge labels HYPOTHETICAL per 2026-08-08 edge-cohort correction

**DSR floors (confirm-stage bar, K=1/2/3):** 0.65 / 0.85 / 0.98

### MNQ — NON-EMPTY-CONDITIONAL(power)

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | 2.00 | $4.00 | $2.40 | 0.600R | 19.2 | 2.40 | 1.000R | 62/68/80 | UNSCR(panel_N) | DEAD(cost) |
| 20 | 5.00 | $10.00 | $2.40 | 0.240R | 19.2 | 0.96 | 0.640R | 25/27/32 | UNSCR(panel_N) | DEAD(cost) |
| 40 | 10.00 | $20.00 | $2.40 | 0.120R | 19.2 | 0.48 | 0.520R | 12/13/16 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 80 | 20.00 | $40.00 | $2.40 | 0.060R | 19.2 | 0.24 | 0.460R | 6/6/8 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 160 | 40.00 | $80.00 | $2.40 | 0.030R | 19.2 | 0.12 | 0.430R | 3/3/4 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |

### MYM — NON-EMPTY

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | 8.00 | $4.00 | $2.40 | 0.600R | 19.2 | 2.40 | 1.000R | 62/68/80 | 0.0891 | DEAD(cost) |
| 20 | 20.00 | $10.00 | $2.40 | 0.240R | 19.2 | 0.96 | 0.640R | 25/27/32 | 0.0891 | DEAD(cost) |
| 40 | 40.00 | $20.00 | $2.40 | 0.120R | 19.2 | 0.48 | 0.520R | 12/13/16 | 0.0891 | OPEN |
| 80 | 80.00 | $40.00 | $2.40 | 0.060R | 19.2 | 0.24 | 0.460R | 6/6/8 | 0.0891 | OPEN |
| 160 | 160.00 | $80.00 | $2.40 | 0.030R | 19.2 | 0.12 | 0.430R | 3/3/4 | 0.0891 | OPEN |

### MES — NON-EMPTY-CONDITIONAL(power)

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | 2.00 | $10.00 | $3.15 | 0.315R | 10.1 | 1.26 | 0.715R | 25/27/32 | UNSCR(panel_N) | DEAD(cost) |
| 20 | 5.00 | $25.00 | $3.15 | 0.126R | 10.1 | 0.50 | 0.526R | 10/11/13 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 40 | 10.00 | $50.00 | $3.15 | 0.063R | 10.1 | 0.25 | 0.463R | 5/5/6 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 80 | 20.00 | $100.00 | $3.15 | 0.032R | 10.1 | 0.13 | 0.431R | 2/2/3 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 160 | 40.00 | $200.00 | $3.15 | 0.016R | 10.1 | 0.06 | 0.416R | 1/1/1 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |

### MGC — NON-EMPTY-CONDITIONAL(power)

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | 0.80 | $8.00 | $2.90 | 0.362R | 11.6 | 1.45 | 0.762R | 31/34/40 | UNSCR(panel_N) | DEAD(cost) |
| 20 | 2.00 | $20.00 | $2.90 | 0.145R | 11.6 | 0.58 | 0.545R | 12/13/16 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 40 | 4.00 | $40.00 | $2.90 | 0.072R | 11.6 | 0.29 | 0.473R | 6/6/8 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 80 | 8.00 | $80.00 | $2.90 | 0.036R | 11.6 | 0.14 | 0.436R | 3/3/4 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |
| 160 | 16.00 | $160.00 | $2.90 | 0.018R | 11.6 | 0.07 | 0.418R | 1/1/2 | UNSCR(panel_N) | OPEN-CONDITIONAL(power) |

### M2K — NON-EMPTY

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | 0.80 | $4.00 | $2.40 | 0.600R | 19.2 | 2.40 | 1.000R | 62/68/80 | 0.0891 | DEAD(cost) |
| 20 | 2.00 | $10.00 | $2.40 | 0.240R | 19.2 | 0.96 | 0.640R | 25/27/32 | 0.0891 | DEAD(cost) |
| 40 | 4.00 | $20.00 | $2.40 | 0.120R | 19.2 | 0.48 | 0.520R | 12/13/16 | 0.0891 | OPEN |
| 80 | 8.00 | $40.00 | $2.40 | 0.060R | 19.2 | 0.24 | 0.460R | 6/6/8 | 0.0891 | OPEN |
| 160 | 16.00 | $80.00 | $2.40 | 0.030R | 19.2 | 0.12 | 0.430R | 3/3/4 | 0.0891 | OPEN |

### MCL — NON-EMPTY

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | UNSCR(pt_val) | $8.00 | $2.90 | 0.362R | 11.6 | 1.45 | 0.762R | 31/34/40 | 0.1237 | DEAD(cost) |
| 20 | UNSCR(pt_val) | $20.00 | $2.90 | 0.145R | 11.6 | 0.58 | 0.545R | 12/13/16 | 0.1237 | OPEN |
| 40 | UNSCR(pt_val) | $40.00 | $2.90 | 0.072R | 11.6 | 0.29 | 0.473R | 6/6/8 | 0.1237 | OPEN |
| 80 | UNSCR(pt_val) | $80.00 | $2.90 | 0.036R | 11.6 | 0.14 | 0.436R | 3/3/4 | 0.1237 | OPEN |
| 160 | UNSCR(pt_val) | $160.00 | $2.90 | 0.018R | 11.6 | 0.07 | 0.418R | 1/1/2 | 0.1237 | OPEN |

### M6A — NON-EMPTY

| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 8 | UNSCR(pt_val) | $8.00 | $2.90 | 0.362R | 11.6 | 1.45 | 0.762R | 31/34/40 | 0.0891 | DEAD(cost) |
| 20 | UNSCR(pt_val) | $20.00 | $2.90 | 0.145R | 11.6 | 0.58 | 0.545R | 12/13/16 | 0.0891 | OPEN |
| 40 | UNSCR(pt_val) | $40.00 | $2.90 | 0.072R | 11.6 | 0.29 | 0.473R | 6/6/8 | 0.0891 | OPEN |
| 80 | UNSCR(pt_val) | $80.00 | $2.90 | 0.036R | 11.6 | 0.14 | 0.436R | 3/3/4 | 0.0891 | OPEN |
| 160 | UNSCR(pt_val) | $160.00 | $2.90 | 0.018R | 11.6 | 0.07 | 0.418R | 1/1/2 | 0.0891 | OPEN |

**H_A: NON-EMPTY**

## §3 H_A verdict

H_A: **NON-EMPTY**.

Four instruments clear outright: MYM, M2K, MCL, and M6A each carry ≥1 OPEN cell against a computed
power floor from committed Stage-1 panel N (0.0891 for MYM/M2K/M6A, 0.1237 for MCL) — verdict
**NON-EMPTY**. The remaining three — MNQ, MES, MGC — clear the same cost wall on ≥1 cell but their
power floor is `UNSCREENABLE-INPUT(panel_N)` (no committed Stage-1 N per F5); per F5's generous
falsifier a missing input must not manufacture EMPTY, so they land **NON-EMPTY-CONDITIONAL(power)**
and still count toward H_A. Every DEAD cell in the pool (10 of 35) dies on the **cost** wall
(`killed_by: cost`, required gross at the 4× hurdle exceeds 0.85R of the cell's own stop) — no cell
anywhere is killed on qty (F4 K-QTY never fires at this ladder). The cost wall claims the 8-tick rung
on all seven instruments, and additionally the 20-tick rung on MNQ, MYM, and M2K — the three
instruments whose smaller per-tick R_usd keeps the cost tax above 0.85R through 20 ticks. M6A, MCL,
MES, and MGC clear cost already at 20 ticks (larger per-tick R_usd). The ladder opens at 20 ticks for
M6A/MCL/MES/MGC and at 40 ticks for MNQ/MYM/M2K, staying open (OPEN or OPEN-CONDITIONAL) through 160
ticks for all seven.

## §4 What this does NOT establish
1. No cell measures achieved edge — every OPEN cell states a REQUIREMENT only.
2. Edge labels are hypothetical (2026-08-08 correction); frontier cells re-derive per candidate.
3. OPEN-CONDITIONAL(power) cells carry UNSCREENABLE-INPUT(panel_N) — route: re-derive the Stage-1
   session arithmetic from the pre-prune tag.
4. A NON-EMPTY verdict admits nothing: harvest Req 1-5, DSR-at-K, N-SURV MC, and the regime gate are
   independent and unweakened.
5. The slot overlay ($125 σ-ceiling, wed_thu surface, S7, F2) is disclosed, not compiled (slot_n column).

## §5 Reproduce
python -X utf8 lab/archive/tnec_envelope_compile_2026-08/run_envelope_compile.py --self-check
python -X utf8 lab/archive/tnec_envelope_compile_2026-08/run_envelope_compile.py --compile
python -X utf8 -m pytest lab/archive/tnec_envelope_compile_2026-08/test_envelope.py -v

## §6 Phase B — census pass (one pass, PREREG F6 taxonomy)

**Date:** 2026-08-11 · **$0 · K=0 · zero panel PnL/returns examined** (no price, return, or PnL
data was read anywhere in this pass; published literature and market-structure facts only).
One pass over the **8 frozen F6 classes × 7 NON-EMPTY instruments = 56 cells**. Stop rule:
taxonomy exhaustion, regardless of count (F6). Entries live in
[`entries/`](entries/); scored via `--entry`; verdicts below are verbatim.

**What "no entry" means here.** Per Req 1a(i) a cell earns an entry only if a counterparty class
trades it under a **mandate, benchmark, or mechanical rule**. A cell offering only a preference
story ("retail chases", "stops get hunted"), or one foreclosed by a binding registry bar, is
recorded as one line — **a defensible no-entry is worth more than an indefensible entry.**
No δ was invented anywhere: `delta_ticks_per_event` is either a cited magnitude with the
conversion arithmetic shown, or `null` → `UNSCREENABLE(δ)`.

**Two scope corrections applied before enumerating** (both change which cells survive):
1. The **≥2 independent events/day** law that killed BE3/SFX-1 is a **fade-program** screening
   law, ruled out of scope for TNEC work by the 2026-08-10 L2 pass
   ([`SOURCES_LOG.md`](lab/archive/../harvest/tnec_l2_sourcing_2026-08-10/SOURCES_LOG.md): *"TNEC N-ACT is
   weekly"*). It is **not** used as a kill below. Req 4's practical bar (daily-or-better event
   frequency) is used instead.
2. Family **K-banks are disclosure, not a gate** ([ADR 2026-08-04](lab/archive/../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
   No cell below is killed on bank arithmetic — including GC/MGC.

### §6.1 The census grid — one row per class × instrument

| class | instrument | entry | verdict | wall / route |
|---|---|---|---|---|
| contract-roll | MNQ | no entry — 3FPS add-back bar names **"MNQ rescue"** and **"pooled-index variant"** verbatim; 4 rolls/yr fails Req 4 | — | registry (3FPS/ORC) + Req 4 |
| contract-roll | MYM | no entry — F4/P3-5 hold this cell, `BLOCKED-BY-REGISTRY`; re-scored below | re-score **F4** `UNSCREENABLE(δ)`; **P3-5** `UNSCREENABLE(δ)` | needs a discriminating observation the 3FPS record lacked |
| contract-roll | MES | no entry — 3FPS "pooled-index variant" bar; 4/yr Req 4 | — | registry + Req 4 |
| contract-roll | MGC | no entry — GSCI/BCOM metals roll is a genuine published mandate but names a **calendar-spread** direction (sell front / buy deferred); an outright micro launders direction (delete/flip) | — | constraint does not SELECT the trade |
| contract-roll | M2K | no entry — as MNQ/MES | — | registry + Req 4 |
| contract-roll | MCL | no entry — same spread-not-outright kill; nearest registry hit `commodity-carry-term-structure on USOIL` FALSIFIED 2026-06-06 as a *"disguised long-oil trend trade"* — the same failure mode | re-score **SFX-1** `UNSCREENABLE(δ)` | constraint does not SELECT the trade |
| contract-roll | M6A | no entry — IMM quarterly roll 4/yr (Req 4); spread direction; **no ledger** (consult exit 2) | — | Req 4 + spread + unconsultable |
| index-rebalance | MNQ | no entry — NDX reconstitution ~1/yr | — | Req 4 (annual) |
| index-rebalance | MYM | no entry — Dow committee changes irregular, ~1/yr | — | Req 4 (annual) |
| index-rebalance | MES | no entry — S&P quarterly share/float updates 4/yr; documented δ is **cash-equity**, Req 2 refuses transplant | re-score **P3-1 ETF-AP-BASIS** `UNSCREENABLE(δ)` | Req 4 + Req 2 |
| index-rebalance | MGC | no entry — GSCI/BCOM January reweight ~1/yr | — | Req 4 (annual) |
| index-rebalance | M2K | no entry — Russell recon ~1/yr, cash-δ only | re-score **P4-3 LIT-RUSSELL** `UNSCREENABLE(δ)` | Req 4 + Req 2 |
| index-rebalance | MCL | no entry — commodity-index annual reweight ~1/yr | — | Req 4 (annual) |
| index-rebalance | M6A | no entry — no index mandates a scheduled AUD-futures rebalance at scale; nearest real mandate (currency-hedged index hedge resets) is month-end, routed to that class | — | no constraint-holder in this class |
| expiry/settlement | MNQ | no entry — quarterly SOQ 4/yr; 3FPS bar names "MNQ rescue" | — | registry + Req 4 |
| expiry/settlement | MYM | no entry — **cell is DEAD in the ledger** (`MYM-3FPS-1`, 2026-07-21; consult exit 1 BLOCKING) | — | add-back needs new target-instrument mechanism evidence |
| expiry/settlement | MES | no entry — 3FPS "pooled-index variant" bar; 4/yr | — | registry + Req 4 |
| expiry/settlement | MGC | no entry — COMEX FND/delivery does force non-deliverable longs out (a hard rule), but the entailed direction is **front-vs-deferred**, not outright | — | constraint does not SELECT the trade |
| expiry/settlement | M2K | no entry — 3FPS pooled-index bar; 4/yr | — | registry + Req 4 |
| expiry/settlement | MCL | no entry — CME **spot-month position limits** force non-commercials out in the last 3 days (~36 events/yr, a genuine mechanical rule, newly enumerated this pass) — but again the direction is a **calendar spread**; an outright MCL trade launders it | re-score **P4-5 LIT-EIA-PHYS** `UNSCREENABLE(δ)` | constraint does not SELECT the trade |
| expiry/settlement | M6A | no entry — IMM final settlement 4/yr; no ledger | — | Req 4 + unconsultable |
| month-end/quarter-end | MNQ | no entry — F5 `BLOCKED-BY-REGISTRY` (D3 ES power 0.24–0.30 · D7 6J 0.30 · HARV2026-001 falsified); 12/yr presumptively dead under Req 4 | — | registry + Req 4 |
| month-end/quarter-end | MYM | no entry — as MNQ | — | registry + Req 4 |
| month-end/quarter-end | MES | no entry — as MNQ | re-score **F5** `UNSCREENABLE(δ)` | registry + Req 4 |
| month-end/quarter-end | MGC | no entry — no metals-specific month-end mandate carrying a declared intraday WHEN | — | clause (ii) fails |
| month-end/quarter-end | M2K | no entry — as MNQ | — | registry + Req 4 |
| month-end/quarter-end | MCL | no entry — as MNQ | — | registry + Req 4 |
| month-end/quarter-end | M6A | no entry — custodian month-end FX hedge rebalance IS a mandate and IS outright-signed, but the registry sibling *Custodian-family month-end equity-hedging flow on EURUSD* is shelved with an add-back bar barring *"a different fix-window"*; 12/yr | — | registry sibling + Req 4 |
| daily auction/settlement | MNQ | no entry — the auction limb class finding is **instrument-independent** (*"dies at the PROCUREMENT GATE … on ANY instrument"*); MOC add-back bars *"different index"* | — | procurement gate |
| daily auction/settlement | MYM | no entry — F1 reject-at-bar 2026-07-27; cell DEAD in ledger (consult exit 1). P4-1 re-ran the reopen route and failed it | re-score **F1** `UNSCREENABLE(δ)` | procurement gate; reopen input **still unsupplied** as of the 2026-08-10 L2 sweep (C4: *JFQA* 2026 auction paper is a cash-equity execution-cost cohort, not the imbalance→index-futures δ) |
| daily auction/settlement | MES | no entry — LETF EOD rebalance is `free-data-domain-bar` (public-AUM-derivable); add-back bars *"a different index/leverage tier"* | re-score **F2** `UNSCREENABLE(δ)` | free-data domain bar |
| daily auction/settlement | **MGC** | **ENTRY** [`mgc-benchmark-fix-window-r8-rescore`](entries/mgc-benchmark-fix-window-r8-rescore.json) — London gold benchmark-fix window; **the only cell in the census with a cited per-event δ**. [Notice log](lab/archive/../../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MGC.md) | **`FAIL` — wall `cost`** · checks: `cell 20t OPEN-CONDITIONAL(power)`, `delta 8.35 < req 11.6 ticks` | cost wall. Known-answer anchor: independently corroborates the **R8 `SCREEN-FAIL`** of 2026-08-10 through a different unit system and commission basis |
| daily auction/settlement | M2K | no entry — BE1's kill is campaign-independent: the constraint carries **neither sign nor level**; direction laundered from price | re-score **BE1** `UNSCREENABLE(δ)` | constraint does not SELECT the trade |
| daily auction/settlement | **MCL** | **ENTRY** [`mcl-tas-settlement-window-replication`](entries/mcl-tas-settlement-window-replication.json) — CME settlement-window (14:28–14:30 ET) benchmark replication. Re-opened because BE3's kill was the **fade-scoped** $200/1.83 design law. [Notice log](lab/archive/../../../docs/notes/notice/N-2026-08-11-daily-auction-settlement-MCL.md) | **`UNSCREENABLE`** — *"delta uncited — route: delta-extraction probe needed (harvest Req 2 relief valve)"* · re-score **BE3** `UNSCREENABLE(δ)` | δ probe. **Non-circular** (CME publishes TAS volumes free) — unlike F1/MOC |
| daily auction/settlement | M6A | no entry — F3 fix-family cost-law kill + P3-4. *Disclosure only (cross-instrument, Req-2-inadmissible as a δ):* the M6A hurdle is 11.6 ticks = **11.6 pips**, against a ~2 bp-scale cited FX-fix effect — **>7× short at any plausible AUD level** | re-score **P3-4 MULTI-FIX-FX** `UNSCREENABLE(δ)` | cost-law + registry |
| margin-cycle | MNQ | no entry — the daily variation-margin cycle IS a mechanical rule, but the forced side is set by the day's own move ⇒ **direction laundered from price**; the band is per-account equity ⇒ unobservable ⇒ stops-get-hunted geometry (SLR-MYM-1 delete/flip) | — | direction laundered + unobservable threshold |
| margin-cycle | MYM | no entry — as MNQ | re-score **P3-2 SESSION-HANDOFF** `UNSCREENABLE(δ)` | inventory sign unobservable |
| margin-cycle | MES | no entry — as MNQ; exchange margin hikes are additionally a few events/yr and announced effective next session | — | direction laundered + Req 4 |
| margin-cycle | MGC | no entry — as MNQ. Commercial hedging-pressure variant foreclosed: **Basu hedging-pressure is already EXCLUDE** in the harvest radar SOURCES_LOG | — | direction laundered + radar EXCLUDE |
| margin-cycle | M2K | no entry — as MNQ | — | direction laundered + unobservable threshold |
| margin-cycle | MCL | no entry — as MGC (hedging-pressure limb EXCLUDE in radar) | — | direction laundered + radar EXCLUDE |
| margin-cycle | M6A | no entry — as MNQ; no ledger | — | direction laundered + unconsultable |
| mandated hedging | MNQ | no entry — vendor-walled by the taxonomy's own parenthesis; `dealer-gamma-regime-gate on NAS100` (rejected 2026-06-25) requires **paid NDX-native** gamma to re-propose | re-score **F6 0DTE-gamma** `UNSCREENABLE(δ)`; **P3-3 VOLTARGET** `UNSCREENABLE(δ)` | vendor wall + registry |
| mandated hedging | MYM | no entry — same vendor wall; the futures-prop venue is **options-free** (index-dispersion venue finding), so the greeks observable is structurally unreachable | — | vendor/venue wall |
| mandated hedging | MES | no entry — same wall. Newly enumerated variant (insurer/VA dynamic hedging, a genuine statutory mandate) dies at clause (ii): the WHEN needs the vendor-walled aggregate delta | — | vendor wall (clause ii) |
| mandated hedging | MGC | no entry — central-bank reserve programs and miner hedge books are real mandates but carry **no declared intraday WHEN**; reporting is monthly/irregular | — | clause (ii) fails |
| mandated hedging | M2K | no entry — same vendor wall | — | vendor/venue wall |
| mandated hedging | MCL | no entry — the largest sovereign/producer hedge program is ~1/yr and executed opaquely over months (clause ii + Req 4); hedging-pressure literature EXCLUDE in radar | — | clause (ii) + Req 4 |
| mandated hedging | M6A | no entry — currency-overlay hedge rolls are mandate-driven and outright-signed, but monthly (Req 4) and inherit the custodian month-end shelf bar | — | Req 4 + registry sibling |
| eval-cohort | MNQ | no entry — **DEAD on transmission, programme-wide** (pass-2 SETTLED 2026-07-30): at all four `AUTOMATION_FRIENDLY_PROP_FIRMS` the mass funded stage fills in **simulation** — no exchange footprint to trade against | — | transmission |
| eval-cohort | MYM | no entry — as MNQ | — | transmission |
| eval-cohort | MES | no entry — as MNQ | — | transmission |
| eval-cohort | MGC | no entry — as MNQ | — | transmission |
| eval-cohort | M2K | no entry — as MNQ. **Discharges pass 2's explicitly-undrafted successor**: the Elite/Brokerage **live**-only re-scope is enumerated here and closed — live tiers are invitation/threshold-gated (mass fails) and the liquidation band is per-account equity ⇒ unobservable ⇒ preference-shaped | re-score **PROPENG-RATCHET** `UNSCREENABLE(δ)` | transmission + unobservable threshold |
| eval-cohort | MCL | no entry — as MNQ | re-score **PROPENG-EJECT** `UNSCREENABLE(δ)` | transmission |
| eval-cohort | M6A | no entry — as MNQ; no ledger | — | transmission + unconsultable |

**Row accounting: 56 rows = 8 classes × 7 instruments. 2 entry rows · 54 no-entry rows.**
17 prior-log entries are re-scored inside those rows (derivation in §6.2).

### §6.2 Re-score protocol and the prior entries left out

Prior entries in [`N-2026-07-26-forced-flow-census.md`](lab/archive/../../../docs/notes/notice/N-2026-07-26-forced-flow-census.md)
are **re-scored, not re-enumerated** (F6). That log is not edited. Derivation, applied uniformly:

- `delta_ticks_per_event` = **`null`** for all 17 — underivable **by construction**, because that log
  forbade quoting δ (*"No entry quotes PnL, δ, or any edge number"*). Every re-score therefore returns
  `UNSCREENABLE(δ)`; the scorer short-circuits on δ before the cell and horizon checks.
- `stop_ticks` = the instrument's **shallowest OPEN rung** (MNQ/MYM/M2K 40 · MES/MGC/MCL/M6A 20), the
  most generous surviving cell, so a failure would be conclusive. Not declared by any prior entry.
- `events_per_year` 252 and `horizon_seconds` 120 assigned generously; likewise undeclared.

**Load-bearing consequence:** the entire prior census is **δ-blind by construction**, so the envelope
cannot discriminate among its entries — it can only report that none of them ever acquired the one
input the cost wall consumes. That is a property of the census's own zero-δ discipline, not a new
finding about the mechanisms.

Seven prior entries take no JSON, with the reason stated rather than dropped:

| prior entry | why no re-score JSON |
|---|---|
| F3 — WMR 4pm-London fix (M6E) | M6E is **out of the F1 instrument pool** (E-COST at Stage 1, unaffected by the K ADR) |
| F7 — own-execution loop (c1 fills/exits) | fits **no F6 class**; deferred by operator choice, waits on live fills |
| P2-5 — M6A-FIGURE-FADE | fits no F6 class — order *placement* is a preference, which is the kill |
| P4-1 — LIT-MOC-FUT | same cell as F1 (daily auction × MYM); folded into that row, not double-counted |
| P4-2 — LIT-COT-ES | positioning-extreme reversal fits no F6 class |
| P4-4 — LIT-ORB-TIE | survivor-tie feature hunt, fits no F6 class |
| P4-6 — Koijen/Bouchouev carry / TSMOM | self-labelled out-of-channel in the source log |

### §6.3 H_B

**H_B: 0 SEED-GRADE entries.** Both authored entries fail an envelope wall — one on **cost** with a
genuinely cited δ (`FAIL`, 8.35 < 11.6 ticks), one on **δ absence** (`UNSCREENABLE`) — and all 17
re-scored prior entries return `UNSCREENABLE(δ)`. Per **PREREG F7** this closes **STOP / NULL**: the
envelope stands as documentation; re-entry requires a **new class or a new instrument**, not a
re-run of this taxonomy. Nothing is admitted, proposed, or licensed here; harvest Req 1–5, DSR-at-K,
N-SURV MC and the regime gate are untouched and unweakened. No sourcing-pointer edit is proposed
(that branch of F7 is reached only at H_B ≥ 1). *§Status in the header is left as authored — the
campaign-level disposition write belongs to the closure step, not to this append.*

### §6.4 What this pass adds beyond the verdict

1. **A fourth jaw for the census pincer — the outright/spread mismatch.** Passes 1–3 found
   constraint-flow mechanisms sit behind a public-derivability kill, a paid-data procurement gate,
   or a simulated-counterparty transmission failure. This pass adds a structural one that is
   independent of all three: **most genuine mandated flows name a SPREAD direction** — front vs
   deferred, cash vs futures, hedged vs unhedged — while the TNEC envelope is an
   **outright single-instrument** frame. It fired on 5 cells across 3 classes (roll × MGC/MCL/M6A,
   expiry × MGC/MCL) and is not a δ question: no amount of citation work fixes it. The surviving
   outright-signed mandated flows are exactly the ones already registry-dead, procurement-gated, or
   Req-4-dead — which is why the grid is 54/56 empty.
2. **The envelope reproduces an independently-derived kill.** R8 killed the gold benchmark-fix seed
   in **bp against a bp hurdle** at $1.06/side + 2 ticks; this envelope kills it in **ticks against a
   tick hurdle** at $0.95/side + 1 tick `total_rt`. Concordant. That is a known-answer anchor for the
   `--entry` path, in the spirit of PREREG F2's MNQ ladder anchor.
3. **One cell is blocked only on δ, with a non-circular probe route.** MCL settlement-window
   replication (BE3's WHO/WHEN, freed from a fade-scoped kill) needs a published cohort δ or a
   δ-extraction probe; CME publishes TAS volumes free, so unlike F1/MOC the route does not require
   the data it is gated on. Recorded as the census's single live route — **not** a proposal.
4. **Two housekeeping observations for the operator** (out of this task's touch scope, not repaired
   here): (a) `ops/instruments/MGC.md` has **no cell** for the 2026-08-10 R8 `SCREEN-FAIL`, so
   `instrument_profiles cell MGC event-window-reversal` still exits 0 on a cell that is closed —
   the consult under-reports; (b) **M6A has no ledger at all** (`ops/instruments/` holds 27 files,
   none for M6A), so every M6A cell in this grid is **unconsultable** — `cell M6A <mech>` exits 2
   FATAL. Seven of 56 cells were screened without the profile-consult limb the entry contract names.
