# MSL-C3-K2 — Stage G0 PREREG — dual-axis MR-at-level (M2K)

**Status:** `FROZEN` 2026-08-13 — operator **B4 GO** paid; explore GO **ISSUED 2026-08-13** → IS score **`FALSIFIED`** (both axes) ([`RESULTS_g2.md`](RESULTS_g2.md) · [closure](../../../docs/briefs/closures/MSL-C3-K2-closure-falsified.md)); Pine **not authorized**; CONFIRM unread
**Date:** 2026-08-13 (freeze)
**Card / campaign:** MSL-C3-K2 revive · [`STAGE1_K2.md`](STAGE1_K2.md) (`STAGE-1 PASS`) · prior ≤1-story path [OPERATOR-KILL](../../../docs/briefs/closures/MSL-C3-closure-operator-kill.md)
**Parent charter:** [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 5
**Slate / election:** [first slate §MSL-C3](../../../docs/briefs/2026-08-12-msl-first-slate.md) · [ADR 2026-08-13 K2 revive](../../../docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md)
**Mechanism ids (both scored axes):** `pdh-pdl-failed-break-reclaim` · `overnight-range-failed-extension-fade` ([`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md))
**Intake gate:** [`TNEC-1`](../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (downstream of survivor MC; not this freeze)
**`K_intrinsic = 2`**. Cap disclosure-not-gate → DSR floor **0.850** at K=2 ([ADR 2026-08-04](../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)). Family bank disclosure: `K_banked(M2K)=0` ([`M2K.md`](../../../ops/instruments/M2K.md)) — does not gate.
**Cost so far:** **$0.0000** · **K spent: 0** (explore scored; Cap not claimed).
**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Explore scored; CONFIRM unread.

---

## §0 — Rule-0 / Stage-1 discharge / door-check (parent-side)

| Check | Result |
|---|---|
| Stage-1 record | [`STAGE1_K2.md`](STAGE1_K2.md) — three $0 limbs PASS at RT **$2.82**; dual-axis license; cheap falsifier PASS; route ① |
| Cost basis | `firm_rules.py` Tradeify Equity Index `cost_per_side_usd: 0.91` + tick_value $0.50 × 2 sides → RT **$2.82**; 4× = **$11.28** |
| Cell door-check A | `instrument_profiles.py cell M2K pdh-pdl-failed-break-reclaim` → BINDING BAR answered **CLEAR via route ①** |
| Cell door-check B | `instrument_profiles.py cell M2K overnight-range-failed-extension-fade` → BINDING BAR answered **CLEAR via route ①** |
| Occupancy | **CLEAR** — M2K never occupied; B8 is MYM/MNQ-only |
| Dense-1m / CON-5 pause | Lane-scoped — does **not** bind session-scale 15m failed-break reclaim |
| Adjacencies | C1 MYM explore **FALSIFIED** on Axis-A class — adjacency, not auto-kill; Req 1a still mandatory per axis |
| Implied-SR | Disclosure only ([ADR 2026-08-13](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)). Not a freeze-time FAIL. |
| Delete/flip (Req 1a) | **Declared mandatory per axis; unpaid at freeze** — IS-only; must PASS before Pine/TV for that axis |
| Panel | **Absent** this clone (W4). No `M2K*` / `RTY*` under `core/data/bar_data/`. **Unread** at freeze. Explore later needs **fresh W4 dry-run** before any pull ([STAGE0](STAGE0.md) §3). |

**Cheap falsifier (parent, 2026-08-13, this freeze):** R/ct **$160** vs 4×RT **$11.28**; all-win **$628.72** ≥ $200; all-lose **$651.28** ≤ $750 — **PASS**. `floor_at_k(2)=0.85` reproduced. Did not invent `p`. Did not read IS/CONFIRM. Both cell paths resolve on disk.

**Verdict:** STAGE1_K2 + B4 license this G0 freeze. **Not** SHAPE-CLEAR. **Not** explore-scored.

---

## §1 — Universe and trade geometry (frozen)

| Element | Frozen value |
|---|---|
| Instrument | CME **M2K** continuous (`M2K1!` / venue-equivalent Micro Russell 2000) |
| Signal TF | **15m** bars, exchange TZ mapped to **America/New_York** |
| Probe window | Same session **[09:30, 15:59] ET**; flat by **16:00 ET** |
| Axis A levels | Prior Globex trade date’s **RTH** H/L: bars with open in **[09:30, 15:59] ET** → PDH/PDL |
| Axis B levels | Globex **overnight** H/L: bars with open in **[18:00 ET prior Globex day, 09:29 ET]** inclusive → ONH/ONL |
| Direction | Fade **failed** break only (reclaim after non-follow-through) — not through-break / join |
| Independence | **First valid signal per axis per session** (EM3 / N-SHAPE k=1 within axis) |
| Cost | Tradeify Equity Index RT **$2.82**/contract (2×$0.91 + 2×$0.50); R = (pnl_usd − RT×qty) / stop_usd |
| Point / tick | **$5.00/pt**; 1 tick = **0.10 pt** = $0.50 |
| Contracts (design disclose) | Stage-1 screen used **4** and stop **32.0 pts** ($160 R/ct); live/explore qty and realized stop distance are scoring parameters, not selection axes |
| Partitions | **IS** = bars/sessions with date **&lt; 2025-09-01**. **CONFIRM** = **2025-09-01 → 2026-08-13** inclusive — **reserved unread through step 8** |

**Not licensed:** OR boundary; through-break continuation; London/COMEX (C2); WSTRUCT weekly; a third mechanism (+1 `K_intrinsic`); silent drop to K=1 after seeing results.

---

## §2 — ENTRY (causal; all constants a priori)

After each **15m** bar close `t` in the probe window (known at close of `t`):

### Axis A — Failed upside break of PDH → SHORT

1. A probe-window bar (or sequence) trades **above** PDH (sweep).
2. A later 15m bar **closes back below** PDH (reclaim) with no prior Axis-A entry today.
3. Enter **SHORT** at next 15m open.
4. **Stop** = max(PDH, sweep extreme high) + **1 tick** (0.10 pt).
5. **Target** = 1.0 × stop distance (rr=1 geometry); also flat at **16:00 ET** if still open.

**Failed downside break of PDL → LONG** (symmetric about PDL).

### Axis B — Failed upside break of ONH → SHORT

Same geometry with **ONH/ONL** replacing PDH/PDL. First Axis-B signal per session only.

**Arms:** long and short scored **separately within each axis**.

**Closed-door clearance:** ≠ `pdh-pdl-breakout-rth` through-break · ≠ `london-range-failed-extension-fade` · ≠ OR continuation/pressure · ≠ WSTRUCT weekly · ≠ join-on-confirmation · ≠ silent revive of the unpaid ≤1-story C3 path without this dual-axis freeze.

---

## §3 — K and robustness probes (not selection)

- **`K_intrinsic = 2`** — two scored axes frozen above (A = PDH/PDL failed-break reclaim; B = overnight-range failed-extension fade).
- **Selection** among axes is IS-only after explore GO under the promotion rule in §4; CONFIRM never used for selection.
- **Sweep axes pre-registered as robustness / plateau probes only** (not selection):
  - stop buffer ∈ {0, 1, 2} ticks (center = 1, frozen)
  - reclaim confirmation = close-back-through level (no alternate confirmation family)
- Any post-freeze widening of reference class / direction / TF / window / third story = **new K** and a new G0.
- **Forbidden:** dropping to K=1 post-hoc after seeing IS results.

---

## §4 — Scoring (EXPLORATION only; after operator explore GO)

| Limb | Definition |
|---|---|
| Delete/flip (Req 1a) | **Per axis** on IS only. Axis A DELETE sham = overnight ONH/ONL (or non-prior-day clock level); Axis B DELETE sham = prior-day RTH PDH/PDL (or non-overnight clock level). FLIP = join extension at reclaim bar. Mandatory before Pine/TV for that axis |
| Primary | Mean net R; session-block bootstrap 95% CI — per arm per axis |
| Halves | Older/newer IS session-date halves — per axis |
| DSR | ≥ **0.850** at `K_intrinsic=2` (disclosure floor) |
| Cost-law | Gross/trade vs **$11.28** at realized stop distances |
| Promotion (pre-registered) | Each axis emits its own explore verdict. Pine/TV for **at most one** axis: (1) exactly one non-`FALSIFIED` → that axis; (2) both clear → higher IS mean net R (long/short pooled); tie → Axis A; (3) both `FALSIFIED` → STOP catalogue |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at explored qty · EM six-char · entry-rate honesty (N-ACT) · which axis promoted |

At G0 freeze: all TNEC N-* limbs **U**. Gate vocabulary at explore: `SHAPE-CLEAR` / `FALSIFIED` / `AMBIGUOUS-HOLD` / `VOID` as specified in explore GO.

**Deferred:** explore GO · W4 dry-run + panel · delete/flip execution · Pine (CC-solo) · TV seat · survivor MC · Cap · rail/arming.

---

## §5 — Forbidden moves

- Path-scoring CONFIRM before step-8 survivor protocol; any CONFIRM peek voids the holdout.
- Inventing freeze-time `p` to gate implied-SR; treating Stage-1 placeholder p as edge.
- Silent drop from K=2 to K=1 after seeing results; scoring a third story; θ-retune rescue.
- Treating C1 MYM explore kill as cleared for Axis A; instrument hop after scoring; post-hoc filters.
- Using a sweep/plateau probe result for **selection**.
- Panel pull / Databento without fresh W4 dry-run; self-authorizing Pine/TV without explore GO + delete/flip PASS + runbook links to steps 2–5.
- `dry_run=false` / arming / Striker redeploy.

---

## §6 — Path after this freeze

1. **This G0** — FROZEN on introducing commit (Rule 8.7).
2. Operator **explore GO** (unpaid) → fresh **W4 dry-run** → panel restore/verify → IS harness + **delete/flip both axes** → explore RESULTS + promotion.
3. On explore PASS for the promoted axis: **Pine CC-solo** (charter step 6; never fleets) + runbook linking steps 2–5 + this PREREG.
4. Operator TV (B5) → export → `msl_score` / survivor MC → TNEC string (steps 7–8).

---

## §7 — Audit hooks

```text
rg -n "CONFIRM|2025-09-01|K_intrinsic|pdh-pdl-failed-break-reclaim|overnight-range-failed-extension-fade" lab/analysis/c1/msl_c3_m2k_2026-08/PREREG_G0.md
python3 scripts/instrument_profiles.py cell M2K pdh-pdl-failed-break-reclaim
python3 scripts/instrument_profiles.py cell M2K overnight-range-failed-extension-fade
# expected: BINDING BAR still answered CLEAR via route ① in STAGE1_K2 / this §0
PYTHONPATH=lab python3 -c "from research_utils.axis_screen import floor_at_k; assert floor_at_k(2)==0.85"
```
