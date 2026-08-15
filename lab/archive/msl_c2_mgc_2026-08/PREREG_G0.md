# MSL-C2 — Stage G0 PREREG — London-range failed-extension fade (MGC)

**Status:** `FROZEN` 2026-08-12 — operator **B4 GO** paid; explore GO **ISSUED 2026-08-13** → IS score **`FALSIFIED`** ([`RESULTS_g2.md`](RESULTS_g2.md) · [closure](lab/archive/../../../docs/briefs/closures/MSL-C2-closure-falsified.md)); Pine **not authorized**; CONFIRM unread
**Date:** 2026-08-12 (freeze) / 2026-08-13 (explore)
**Card / campaign:** MSL-C2 · [`STAGE1.md`](STAGE1.md) (`STAGE-1 PASS`)
**Parent charter:** [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](lab/archive/../../../docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md) step 5
**Slate:** [`docs/briefs/2026-08-12-msl-first-slate.md`](lab/archive/../../../docs/briefs/2026-08-12-msl-first-slate.md) §MSL-C2
**Mechanism id:** `london-range-failed-extension-fade` ([`MECHANISMS.md`](lab/archive/../../../ops/instruments/MECHANISMS.md) NEW 2026-08-12)
**Intake gate:** [`TNEC-1`](lab/archive/../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (downstream of survivor MC; not this freeze)
**`K_intrinsic = 1`**. Cap disclosure-not-gate → DSR floor **0.650** at K=1 ([ADR 2026-08-04](lab/archive/../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
**Cost so far:** **$0.0000** · **K spent: 0** (freeze + explore).
**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** No EXPLORATION path scores at freeze. CONFIRM unread.

---

## §0 — Rule-0 / Stage-1 discharge / door-check (parent-side)

| Check | Result |
|---|---|
| Stage-1 record | [`STAGE1.md`](STAGE1.md) — three $0 limbs PASS at RT **$4.12**; cheap falsifier PASS |
| Cost basis | `firm_rules.py` Tradeify comment `MGC=$1.06` + tick_value $1.00 × 2 sides → RT **$4.12**; 4× = **$16.48** |
| Cell door-check | `instrument_profiles.py cell MGC london-range-failed-extension-fade` → BINDING BAR `free-data-5th-leg-snag-closed-2026-07-01` answered **CLEAR by domain mismatch** under R-FRAMING **§2.1** |
| Index OHLCV raised bar | Does **not** bind (MGC non-index) |
| Adjacencies | R8 event-window / Guardian→MGC transfer — **not** this construct; transfer barred |
| Implied-SR | Disclosure only ([ADR 2026-08-13](lab/archive/../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md); interim MSL-only ADR absorbed). Not a freeze-time FAIL. |
| Delete/flip (Req 1a) | **Declared mandatory; unpaid at freeze** — IS-only; must PASS before Pine/TV (see §6) |

**Verdict:** Stage-1 + B4 license this G0 freeze. **Not** SHAPE-CLEAR. **Not** explore-scored.

---

## §1 — Universe and trade geometry (frozen)

| Element | Frozen value |
|---|---|
| Instrument | COMEX **MGC** continuous (`MGC1!` / venue-equivalent micro gold) |
| Signal TF | **15m** bars, exchange TZ mapped to **America/New_York** |
| London window | Each Globex day: bars with open time in **[03:00, 08:19] ET** inclusive |
| London H/L | High / low of that London window (prior to COMEX day-open probe) |
| Probe window | From **08:20 ET** through **15:59 ET** same day (flat by 16:00 ET) |
| Direction | Fade **failed** extension only (not join/continuation) |
| Independence | **First valid signal per session only** (EM3 / N-SHAPE k=1) |
| Cost | Tradeify Metals RT **$4.12**/contract (2×$1.06 + 2×$1.00); R = (pnl_usd − RT×qty) / stop_usd |
| Contracts (design disclose) | Stage-1 screen used **4**; live/explore qty is a scoring parameter, not a selection axis |
| Partitions | **IS** = bars/sessions with date **&lt; 2025-09-01**. **CONFIRM** = **2025-09-01 → 2026-08-12** inclusive — **reserved unread through step 8** |

---

## §2 — ENTRY (causal; all constants a priori)

After each **15m** bar close `t` in the probe window (known at close of `t`):

**Failed upside extension → SHORT**

1. A probe-window bar (or sequence) trades **above** London high (sweep).
2. A later 15m bar **closes back below** London high (reclaim / failure confirmation) with no prior entry today.
3. Enter **SHORT** at next 15m open.
4. **Stop** = max(London high, sweep extreme high) + **1 tick** ($0.10).
5. **Target** = 1.0 × stop distance (rr=1 geometry); also flat at **16:00 ET** if still open.

**Failed downside extension → LONG** (symmetric about London low).

**Arms:** long and short scored **separately**.

**Closed-door clearance:** ≠ `event-window-reversal` / R8 fix · ≠ Guardian transfer · ≠ `pdh-pdl-breakout-rth` through-break · ≠ ORB continuation · ≠ Asia-range reference · ≠ join-on-confirmation.

---

## §3 — K and robustness probes (not selection)

- **`K_intrinsic = 1`** — single axis: London-range failed-extension fade as frozen above.
- **Selection** is IS-only after explore GO; CONFIRM never used for selection.
- **Sweep axes pre-registered as robustness / plateau probes only** (not selection):
  - stop buffer ∈ {0, 1, 2} ticks (center = 1, frozen)
  - reclaim confirmation = close-back-through London extreme (no alternate confirmation family)
- Any post-freeze widening of reference class / direction / TF / window = **new K** and a new G0.

---

## §4 — Scoring (EXPLORATION only; after operator explore GO)

| Limb | Definition |
|---|---|
| Delete/flip (Req 1a) | Constraint (London extreme + failure reclaim) must SELECT the trade on **IS only**; flip / delete tests pre-registered at explore GO — **mandatory before Pine/TV** |
| Primary | Mean net R; session-block bootstrap 95% CI |
| Halves | Older/newer IS session-date halves |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor) |
| Cost-law | Gross/trade vs **$16.48** at realized stop distances |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at explored qty · EM six-char |

At G0 freeze: all TNEC N-* limbs **U**. Gate vocabulary at explore: `SHAPE-CLEAR` / `FALSIFIED` / `AMBIGUOUS-HOLD` / `VOID` as specified in explore GO.

**Deferred:** explore GO · delete/flip execution · Pine (CC-solo) · TV seat · survivor MC · Cap · rail/arming.

---

## §5 — Forbidden moves

- Path-scoring CONFIRM before step-8 survivor protocol; any CONFIRM peek voids the holdout.
- Inventing freeze-time `p` to gate implied-SR; treating Stage-1 placeholder p as edge.
- Re-opening R8 fix-window or Guardian-transfer under this G0.
- Instrument hop after scoring; post-hoc filters after seeing results.
- Using a sweep/plateau probe result for **selection**.
- Self-authorizing Pine/TV without explore GO + delete/flip PASS + runbook links to steps 2–5.
- `dry_run=false` / arming / Striker redeploy.

---

## §6 — Path after this freeze

1. **This G0** — FROZEN on introducing commit (Rule 8.7).
2. Operator **explore GO** (unpaid) → IS harness + **delete/flip** → explore RESULTS.
   Harness landed: [`EXPLORE_GO.DRAFT.md`](EXPLORE_GO.DRAFT.md) (promote → gitignored `EXPLORE_GO.md`) · [`construct_lib.py`](construct_lib.py) · [`run_construct_g0.py`](run_construct_g0.py). Restore `MGC_M15.csv` sha pin before `--explore-go`.
3. On explore PASS: **Pine CC-solo** (charter step 6; surface allocation — never fleets) + runbook linking steps 2–5 + this PREREG.
4. Operator TV (B5) → export → `msl_score` / survivor MC → TNEC string (steps 7–8).

---

## §7 — Audit hooks

```text
rg -n "CONFIRM|2025-09-01|K_intrinsic|london-range-failed-extension" lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md
python scripts/instrument_profiles.py cell MGC london-range-failed-extension-fade
# expected: BINDING BAR free-data-5th-leg… still answered in STAGE1 / this §0
```
