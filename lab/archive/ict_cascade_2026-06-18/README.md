# Q-ICT-CASCADE-1 — offline harness suite (README)

**Disposition:** CLOSED — Q-ICT-CASCADE-1 CLOSED (1M insufficient N)

Built 2026-06-18 (front-load session). These harnesses are the **offline verdict
instruments** for the five-layer ICT cascade. They are built + unit-tested NOW so
that the moment the operator runs the TV exports, each layer's verdict falls out.
Nothing here is a verdict yet — no real export exists on disk.

> Read first: [`TEST_PLAN.md`](TEST_PLAN.md) (campaign tracker + Progress Ledger),
> then the per-layer `PREREG-*.md` (frozen thresholds + binary verdict gates) and
> [`DSR_PBO_LEDGER.md`](DSR_PBO_LEDGER.md) (joint selection budget, M=65).
> The PREREGs are **PROPOSED** until the operator commits them (the commit is the
> firewall-lift). The harnesses encode the PROPOSED thresholds; a ratification
> change to a flagged GENUINE CHOICE is a one-line constant edit, not a rebuild.

---

## Files

| File | Role |
|---|---|
| `_ict_offline.py` | Shared module: faithful numpy port of `constellation_ict_lib_DRAFT.pine` detectors (FVG orientation/bounds, D-1 touch guard, pivots, raid, pd-zone, ATR) + the campaign's pre-registered statistics (moving-block bootstrap, autocorr block-length rule, max-stat label permutation, drop-top-k, two-proportion diff CI, radius-matched base rate, ET fields). Single source of truth — the four harnesses import it. |
| `harness_w.py` | Layer W (Weekly bias). Verdict per `PREREG-W.md`. |
| `harness_d.py` | Layer D (Daily DOL). Verdict per `PREREG-D.md`. **Fully offline reconstruction from Daily OHLC** (the Daily indicator only exports aggregates). |
| `harness_1h.py` | Layer 1H (Premium/Discount). Verdict per `PREREG-1H.md`. Includes the price-basis transfer residual (impossible on a TV chart). |
| `harness_1m.py` | Layer 1M (Execution). Verdict per `PREREG-1M.md`. Cost-law + gate-ablation + drop-top-k + static-$200K. Reuses `dsr.py` from the USDCAD chain. |
| `test_*.py` | TDD unit tests (synthetic fixtures; no vendor data). |

## Running

```bash
# Unit tests (run NOW — synthetic fixtures, no external data; not in the default `pytest tests/`):
python -m pytest lab/analysis/ict_cascade_2026-06-18/ -q          # 158 passed

# A layer verdict (skips cleanly until its export exists):
python lab/analysis/ict_cascade_2026-06-18/harness_w.py
python lab/analysis/ict_cascade_2026-06-18/harness_d.py
python lab/analysis/ict_cascade_2026-06-18/harness_1h.py
python lab/analysis/ict_cascade_2026-06-18/harness_1m.py
```

Each `main()` prints exactly which export(s) it needs and exits 0 (no verdict) when
absent. `_ict_offline` is imported by relative name; run from the repo root or the
campaign dir (the test files insert the dir on `sys.path`).

---

## Operator TV-execution checklist (the wall — these are yours)

Per the campaign Open/next: publish the patched lib **Private** on TV, substitute
`<your_tv_username>` in the 3 consumers (confirm `/1`), compile the 4
`Downloads/*_DRAFT.pine`, run on a **genuinely multi-regime** window (the F8
dissent), then export. DST sanity on compile: a 9:30-ET bar must fall in NY-AM in
both Jan (EST) and Jul (EDT).

What each harness needs you to export:

| Layer | Chart | Export | Notes |
|---|---|---|---|
| **W** | Weekly | data-window CSV: `time, bias, outcome, vStruct, vSeason, vRates, vEarn, hit, gateBias, gateHit, gateScored, scored` | The vote-importance sub-verdict needs an **all-votes-ON, W-2-fixed** export (vRates regenerated `close[1]`). `emaLen` MUST equal 1M `wEmaLen=20`. |
| **D** | Daily | **Daily OHLC bars** of the SPX-class series (BAR_EXPORT pipe `epoch_ms\|O\|H\|L\|C\|V`, or plain OHLC CSV) | NOT a TV-indicator export — the harness re-implements the detectors offline. The current on-disk US500 BAR_EXPORT is 15m, not Daily. |
| **1H** | 1H | data-window CSV: `time, OHLC, zone, eq, premHit, discHit, zoneGate, zoneAgree` | Plus the **paired 1M export** (below) for the price-basis transfer axis, and optionally a weekly `structBias` export for the bias-conditioned variant. Set `lookN==pdLookN==60`, `eqBand==0.05`. |
| **1M** | 1m | **16 labeled List-of-Trades exports** = 8 ablation combos (bias×PD×killzone) × 2 `useBody` variants, all on `dolMode=range-extreme` | Plus optional 1M data-window (`netBias, zone, inKZ`) for the 1H price-basis axis. `nearest-pool` exports, if any, are REPORT-ONLY. Filename convention or a JSON manifest — see `harness_1m.main()`. |

A minor TV column rename is a one-line fix in each harness's schema-adapter
(`COLMAP` / `_ALIASES`).

---

## What the suite does NOT do

- It does **not** read the on-chart tables as the verdict (autocorrelated smoke
  tests by the scripts' own admission — §5 forbidden). Verdicts are the
  de-overlapped offline estimates.
- It does **not** sweep parameters before the selection-level tests (§5).
- It does **not** touch `core/` / lock / allocation / dd_protection.
- A layer PASS does **not** license the 1M gate until the 1H transfer pre-gate
  clears (H-CASCADE; the cascade's load-bearing joint).

## Provenance

Detectors ported verbatim from `constellation_ict_lib_DRAFT.pine` (10587 B,
LastWriteUTC 2026-06-18T22:42:47Z — re-anchor on resume; Bash `ls` shows local ET).
Statistics encode the PROPOSED PREREG methods. Built via a TDD workflow; the
load-bearing detector port + D reconstruction clocks + 1M cost-law were
hand-verified against the lib + PREREGs (the workflow's adversarial-review phase
hit a session limit and was completed manually).
