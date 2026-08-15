# Regime-conditional re-MC — RESULTS (Q-REGIME-ADAPT-1.T2b, 2026-06-22)

**Verdict: FALSIFIED-T2b** — primary VIX>20 / k=0.50 / lag-1 brake, stressed 43.4% of days. Pre-registered (commit predates this run).

**Panel:** decompounded 2026-06-07 canonical, 2020-01-06→2026-06-02 (1672 bd), H1/H2 split @ 2023-03-21. VIX `^VIX` 2020-01-06→2026-06-04. Locked allocations + dd_protection C2 unchanged; only the exogenous brake added.


| config | full | H1 (2020-2023) | H2 (2023-2026) |
|---|---|---|---|
| **baseline (no brake)** | pass 97.04% / bust 2.96% / p99 5.93% / med 31 | pass 75.45% / bust 24.54% / p99 8.57% / med 67 | pass 99.46% / bust 0.54% / p99 4.87% / med 18 |
| **+brake VIX>20 k=0.50** | pass 98.76% / bust 1.24% / p99 5.35% / med 36 | pass 81.56% / bust 18.00% / p99 8.39% / med 127 | pass 99.63% / bust 0.37% / p99 4.76% / med 20 |

**Gate (headline, H1 inside floor):** H1 bust<1% AND H1 p99<5% AND median≤45d AND H2 maintained AND leakage-clean.
- H1 +brake: bust 18.00% (<1%? N), p99 8.39% (<5%? N), median 127d (≤45? N)
- H2 +brake maintained: bust 0.37% / p99 4.76% (Y)
- Leakage (lag-2) H1: pass 81.93% / bust 17.46% / p99 8.37% / med 132 → fragile

## Robustness ladder (H1; reported in full — verdict rests on PRIMARY only)

| signal | stressed% | H1 |
|---|---|---|
| VIX>25, k=0.5 | 21.3% | pass 74.33% / bust 25.54% / p99 8.65% / med 96 |
| VIX>30, k=0.5 | 9.2% | pass 77.93% / bust 22.05% / p99 8.49% / med 73 |
| VIX>20, k=0.4 | 43.4% | pass 81.62% / bust 17.59% / p99 8.35% / med 143 |
| VIX>20, k=0.6 | 43.4% | pass 80.85% / bust 18.94% / p99 8.45% / med 111 |

## Read

- Baseline H1 (the regime-bound tail): bust 24.54%, p99 8.57% — the breach the brake must fix without an impractical pass-time.
- The brake does **not** clear H1 at median ≤45d (or fails leakage/H2) → **FALSIFIED**: the exogenous-VIX conditional lever does not beat the static de-risk tradeoff on this panel. 2026-06-07 HOLD stands. (Likely mechanism if FALSIFIED: VIX flags CRISIS but H1 busts include low-VIX chop, OR the de-risk slows pass-time past 45d — the chop-vs-crisis gap T2a flagged.)

**Scope:** research (`lab/`); zero `core/` touch; no lock/allocation/dd_protection change. Vendor inputs + VIX cache gitignored. Reproduce: `python run_regime_remc.py` (inputs + yfinance).
