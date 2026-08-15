# Carry δ extraction — Koijen et al. 2018 Table 1 (cheap recovery)

**Date:** 2026-07-16  
**Status:** **Moments recovered; carry-timing Req-2 still UNSCREENABLE** (honest — no class→instrument transplant)  
**Source:** Koijen, Moskowitz, Pedersen & Vrugt, *Carry*, *JFE* 127 (2018) 197–225, **Table 1** Panel A (accepted manuscript / Chicago Booth PDF mirror).  
**Rows targeted:** `H-CARRY-FX-1` (6J/6E), `H-CARRY-CM-1` (CL/WTI)  
**Zero pulls / zero K.**

---

## What Req-2 needs vs what Table 1 supplies

| Needed for staged design | Table 1 supplies | Admissible? |
|---|---|---|
| Per-instrument **δ/σ of the confirm rule** — sign of **own carry** predicting next-month excess return (time-series carry timing) | Per-instrument **unconditional** excess-return mean/stdev + carry mean/stdev | **No** — different object |
| Cohort-cited effect size on **6J / 6E / CL** | Japan / Euro / WTI (and Brent "Crude oil") FX/commodity rows | Moments yes; timing δ no |
| Class timing SR (paper Table 6: FX **0.53**, commodities **0.75**) | Asset-class portfolios | **Forbidden transplant** (harvest Req 2 / strategy_harvest §1 Req 2) |

Paper text confirms carry timing is studied as a **strategy class** ("buy when carry positive / above historical mean… Sharpe ratios that average 0.6") and via **panel** regressions — not as published per-currency / per-contract timing Sharpes for JPY, EUR, or WTI alone.

---

## Extracted Table 1 moments (annualized %; ± transcription tolerance)

Currency rows (USD-based FX forwards/futures universe in the paper):

| Instrument (Table 1 label) | Begin | Excess ret mean | Excess ret σ | Carry mean | Carry σ | Uncond SR (=mean/σ) | Uncond monthly δ/σ (=SR/√12) |
|---|---|---:|---:|---:|---:|---:|---:|
| **Japan** | Nov-83 | 1.7 | 11.4 | −2.7 | 0.7 | 0.149 | **0.043** |
| **Euro** | Feb-99 | 1.2 | 10.8 | −0.3 | 0.4 | 0.111 | **0.032** |

Commodity rows (CL family):

| Instrument | Begin | Excess ret mean | Excess ret σ | Carry mean | Carry σ | Uncond SR | Uncond monthly δ/σ |
|---|---|---:|---:|---:|---:|---:|---:|
| **WTI crude** | Feb-87 | 11.6 | 33.5 | 1.5 | 7.0 | 0.346 | **0.100** |
| Crude oil (Brent) | Feb-99 | 21.1 | 32.0 | 0.8 | 5.4 | 0.659 | 0.190 |

**Do not plug uncond δ/σ into Clause N for `H-CARRY-*`.** Those numbers are buy-and-hold excess-return Sharpes, not carry-timing effect sizes. Using them would silently change the axis design (forbidden).

---

## Clause-N informational (only if someone mistook uncond for timing — do not screen)

At Default-#1 N≈86: Japan uncond power ≈ Φ(√86·0.043 − 1.96) ≪ 0.50. WTI uncond 0.100 → still well below 0.50 at N=86. Even the wrong object fails Default #1 — reinforcing that a **timing** δ would need to be substantially larger *and* still survive N≈86, or else die the same Clause-N death as H-TSMOM-6J.

---

## Disposition of the two stubs

| Row | After this extraction | Next cheap move |
|---|---|---|
| `H-CARRY-FX-1` | Moments on disk for Japan/Euro; **Req-2 timing δ still UNSCREENABLE** | (a) Locate a **named** per-contract predictive δ (appendix / replication / AQR data library with instrument-level timing SR), **or** (b) fund a **δ-extraction probe** (costs data + K — separate Pre-Q), **or** (c) drop |
| `H-CARRY-CM-1` | Moments on disk for WTI (+ Brent); **same UNSCREENABLE** | Same three paths; prefer WTI/CL over Brent for CME expression; **not GC** (FAIL-K) |

**Honesty rider:** inventing a per-instrument timing δ by scaling class SR 0.53/0.75 by any ad-hoc factor is a Req-2 violation. Not done here.

---

## Provenance

- PDF: Chicago Booth faculty mirror / CBS accepted manuscript (Koijen et al. 2018).  
- Digitization: text extract of Table 1 Panel A rows Japan / Euro / WTI crude / Crude oil (this session).  
- Related radar docs: [`CANDIDATE_ROWS.md`](CANDIDATE_ROWS.md), [`SOURCES_LOG.md`](SOURCES_LOG.md).  
