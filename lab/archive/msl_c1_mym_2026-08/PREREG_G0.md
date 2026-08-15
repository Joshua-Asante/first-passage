# MSL-C1 — Stage G0 PREREG — PDH/PDL failed-break reclaim (MYM)

**Status:** `FROZEN` 2026-08-13 — operator **B4 GO** paid; explore GO **ISSUED 2026-08-13** → IS score **`FALSIFIED`** ([`RESULTS_g2.md`](RESULTS_g2.md) · [closure](lab/archive/../../../docs/briefs/closures/MSL-C1-closure-falsified.md)); Pine **not authorized**; CONFIRM unread
**Date:** 2026-08-13 (freeze) / 2026-08-13 (explore)
**Card / campaign:** MSL-C1 · [`STAGE1.md`](STAGE1.md) (`STAGE-1 PASS`)
**Parent charter:** [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](lab/archive/../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 5
**Slate:** [`docs/briefs/2026-08-12-msl-first-slate.md`](lab/archive/../../../docs/briefs/2026-08-12-msl-first-slate.md) §MSL-C1
**Mechanism id:** `pdh-pdl-failed-break-reclaim` ([`MECHANISMS.md`](lab/archive/../../../ops/instruments/MECHANISMS.md); class minted on C3, unpaid M2K path [OPERATOR-KILL](lab/archive/../../../docs/briefs/closures/MSL-C3-closure-operator-kill.md))
**Occupancy:** Board **B8** — [`ADR 2026-08-12`](lab/archive/../../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)
**Intake gate:** [`TNEC-1`](lab/archive/../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (downstream of survivor MC; not this freeze)
**`K_intrinsic = 1`**. Cap disclosure-not-gate → DSR floor **0.650** at K=1 ([ADR 2026-08-04](lab/archive/../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)). Family bank disclosure: see [`MYM.md`](lab/archive/../../../ops/instruments/MYM.md) (does not gate).
**Cost so far:** **$0.0000** · **K spent: 0** (freeze + explore).
**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Explore scored; CONFIRM unread.

---

## §0 — Rule-0 / Stage-1 discharge / door-check (parent-side)

| Check | Result |
|---|---|
| Stage-1 record | [`STAGE1.md`](STAGE1.md) — three $0 limbs PASS at RT **$2.82**; cheap falsifier PASS; route ① + B8 |
| Cost basis | `firm_rules.py` Tradeify `cost_per_side_usd: 0.91` (index micros) + tick_value $0.50 × 2 sides → RT **$2.82**; 4× = **$11.28** |
| Cell door-check | `instrument_profiles.py cell MYM pdh-pdl-failed-break-reclaim` → BINDING BAR `index-intraday-ohlcv-directional-timing-2026-07-21` answered **CLEAR via route ①** (SLR MR-at-level); occupancy **CLEAR via B8** |
| Dense-1m PDH/PDL θ bar | Lane-scoped — does **not** bind this 15m failed-break reclaim (opposite selector) |
| Adjacencies | SLR-MYM-1 Stage-0 FALSIFIED (framings); C3 M2K unpaid path OPERATOR-KILL — **not** a class kill; Req 1a still mandatory |
| Implied-SR | Disclosure only ([ADR 2026-08-13](lab/archive/../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)). Not a freeze-time FAIL. |
| Delete/flip (Req 1a) | **Declared mandatory; unpaid at freeze** — IS-only; must PASS before Pine/TV (see §6) |
| Panel (explore later) | `core/data/bar_data/MYM_M15.csv` present locally; pin `24e169528f7ea669…` per `SHA256SUMS` / ledger M7 — **unread at this freeze** |

**Cheap falsifier (parent, 2026-08-13):** recompute Stage-1 design point — R/ct $160 vs 4×RT $11.28; all-win $628.72 ≥ $200; all-lose $651.28 ≤ $750 — **PASS**. B8 + SLR closure paths resolve on disk.

**Verdict:** Stage-1 + B4 license this G0 freeze. **Not** SHAPE-CLEAR. **Not** explore-scored.

---

## §1 — Universe and trade geometry (frozen)

| Element | Frozen value |
|---|---|
| Instrument | CBOT **MYM** continuous (`MYM1!` / venue-equivalent Micro Dow) |
| Signal TF | **15m** bars, exchange TZ mapped to **America/New_York** |
| Prior-day RTH | Prior Globex trade date’s RTH window: bars with open time in **[09:30, 15:59] ET** inclusive |
| PDH / PDL | High / low of that prior-day RTH window (only level class licensed) |
| Probe window | Same session **[09:30, 15:59] ET**; flat by **16:00 ET** |
| Direction | Fade **failed** break only (reclaim after non-follow-through) — not through-break / join |
| Independence | **First valid signal per session only** (EM3 / N-SHAPE k=1) |
| Cost | Tradeify Equity Index RT **$2.82**/contract (2×$0.91 + 2×$0.50); R = (pnl_usd − RT×qty) / stop_usd |
| Point / tick | **$0.50/pt**; 1 tick = **1.0 pt** = $0.50 |
| Contracts (design disclose) | Stage-1 screen used **4** and stop **320.0 pts** ($160 R/ct) for $0 limbs; live/explore qty and realized stop distance are scoring parameters, not selection axes |
| Partitions | **IS** = bars/sessions with date **&lt; 2025-09-01**. **CONFIRM** = **2025-09-01 → 2026-08-13** inclusive — **reserved unread through step 8** |

**Not licensed:** overnight extreme; OR boundary; through-break continuation; additional level class (+1 `K_intrinsic` each).

---

## §2 — ENTRY (causal; all constants a priori)

After each **15m** bar close `t` in the probe window (known at close of `t`):

**Failed upside break of PDH → SHORT**

1. A probe-window bar (or sequence) trades **above** PDH (sweep).
2. A later 15m bar **closes back below** PDH (reclaim / failure confirmation) with no prior entry today.
3. Enter **SHORT** at next 15m open.
4. **Stop** = max(PDH, sweep extreme high) + **1 tick** (1.0 pt).
5. **Target** = 1.0 × stop distance (rr=1 geometry); also flat at **16:00 ET** if still open.

**Failed downside break of PDL → LONG** (symmetric about PDL).

**Arms:** long and short scored **separately**.

**Closed-door clearance:** ≠ `pdh-pdl-breakout-rth` through-break · ≠ `ict-liquidity` / SLR framing · ≠ OR continuation/pressure · ≠ overnight-range reference · ≠ C3 M2K unpaid path revive · ≠ join-on-confirmation.

---

## §3 — K and robustness probes (not selection)

- **`K_intrinsic = 1`** — single axis: PDH/PDL failed-break reclaim as frozen above.
- **Selection** is IS-only after explore GO; CONFIRM never used for selection.
- **Sweep axes pre-registered as robustness / plateau probes only** (not selection):
  - stop buffer ∈ {0, 1, 2} ticks (center = 1, frozen)
  - reclaim confirmation = close-back-through PDH/PDL (no alternate confirmation family)
- Any post-freeze widening of reference class / direction / TF / window = **new K** and a new G0.

---

## §4 — Scoring (EXPLORATION only; after operator explore GO)

| Limb | Definition |
|---|---|
| Delete/flip (Req 1a) | Constraint (PDH/PDL + failure reclaim) must SELECT the trade on **IS only**; sham = non-prior-day clock level; flip = join extension at reclaim bar — **mandatory before Pine/TV** |
| Primary | Mean net R; session-block bootstrap 95% CI |
| Halves | Older/newer IS session-date halves |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor) |
| Cost-law | Gross/trade vs **$11.28** at realized stop distances |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at explored qty · EM six-char · entry-rate honesty (N-ACT) |

At G0 freeze: all TNEC N-* limbs **U**. Gate vocabulary at explore: `SHAPE-CLEAR` / `FALSIFIED` / `AMBIGUOUS-HOLD` / `VOID` as specified in explore GO.

**Deferred:** explore GO · delete/flip execution · Pine (CC-solo) · TV seat · survivor MC · Cap · rail/arming.

---

## §5 — Forbidden moves

- Path-scoring CONFIRM before step-8 survivor protocol; any CONFIRM peek voids the holdout.
- Inventing freeze-time `p` to gate implied-SR; treating Stage-1 placeholder p as edge.
- Silent revive of C3’s unpaid M2K G0 path; instrument hop after scoring; post-hoc filters after seeing results.
- Using a sweep/plateau probe result for **selection**.
- Re-opening dense-1m CON-4 through-break under this G0; treating SLR Stage-0 kill as a free pass on Req 1a.
- Self-authorizing Pine/TV without explore GO + delete/flip PASS + runbook links to steps 2–5.
- `dry_run=false` / arming / Striker redeploy.

---

## §6 — Path after this freeze

1. **This G0** — FROZEN on introducing commit (Rule 8.7).
2. Operator **explore GO** (unpaid) → IS harness + **delete/flip** → explore RESULTS. Panel pin: `MYM_M15.csv` sha256 `24e169528f7ea669…` (restore/verify before `--explore-go` if absent).
3. On explore PASS: **Pine CC-solo** (charter step 6; surface allocation — never fleets) + runbook linking steps 2–5 + this PREREG.
4. Operator TV (B5) → export → `msl_score` / survivor MC → TNEC string (steps 7–8).

---

## §7 — Audit hooks

```text
rg -n "CONFIRM|2025-09-01|K_intrinsic|pdh-pdl-failed-break-reclaim" lab/archive/msl_c1_mym_2026-08/PREREG_G0.md
python scripts/instrument_profiles.py cell MYM pdh-pdl-failed-break-reclaim
# expected: BINDING BAR index-intraday… still answered in STAGE1 / this §0 via route ① + B8
```
