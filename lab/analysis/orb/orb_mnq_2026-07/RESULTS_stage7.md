# ORB-MNQ-1 Stage-7 realism RESULTS — confirm gate at all four FRIENDLY firms + slip stress

**Campaign:** `orb_mnq_intraday_breakout` · **Pre-reg:** [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md)
**Harness:** [`run_stage7.py`](run_stage7.py) — commissions read **live** from `core/firm_rules.py` `cost_per_side_usd` at the $100K survivor-scoring band; Sharpe-limb gate via production `deflated_sharpe`. Precedes [`RESULTS_stage6.md`](RESULTS_stage6.md).
**Cost model:** symmetric RT (the frozen §R.1 model), `rt_pt = comm_side + k·$0.50` (MNQ $2/pt, 1 tick = $0.50). Data already native MNQ (no parent→micro rescale). rt only enters `R=(pnl−rt)/range`, so all cells are computed analytically from one gross backtest per window.

---

## Verdict — the edge is **robust on the 2021+ regime at ALL four firms**; the full-window pass is **Bulenox-and-tight-fills-specific**

### Table 1 — each firm at the frozen 1-tick slip (`rt = comm/side + $0.50`)

| Firm | comm/side | RT (pt) | FULL window (annSR / DSR / gate) | 2021+ (annSR / DSR / gate) |
|---|---|---|---|---|
| **Bulenox** | $0.61 | 1.11 | +0.890 / 0.9754 / **PASS** | +1.185 / 0.9922 / **PASS** |
| **Tradeify** | $0.91 | 1.41 | +0.835 / 0.9644 / **FAIL** | +1.140 / 0.9893 / **PASS** |
| **MFFU** | $0.95 | 1.45 | +0.827 / 0.9627 / **FAIL** | +1.134 / 0.9889 / **PASS** |
| **BluSky-NT** | $0.95 | 1.45 | +0.827 / 0.9627 / **FAIL** | +1.134 / 0.9889 / **PASS** |
| BluSky-Rithmic\* | $0.50 | 1.00 | +0.911 / 0.9786 / PASS | +1.202 / 0.9931 / PASS |

\* BluSky's own $0.50-flat micro rail is Rithmic/Volumetrica/Tradesea eval-only — it does **not** carry the NT8/CrossTrade automation the prop-portfolio program assumes, so it is an informational lower bound, not a deployable path.

### Table 2 — slip stress (`P/F  annSR/DSR`; gate = DSR≥0.95 AND annSR≥0.85)

| Firm | window | +0 tick | +1 tick | +2 tick | +3 tick |
|---|---|---|---|---|---|
| Bulenox | FULL | P +0.98/.987 | **P +0.89/.975** | F +0.80/.955 | F +0.70/.924 |
| Bulenox | 2021+ | P +1.26/.996 | P +1.19/.992 | P +1.11/.987 | P +1.04/.979 |
| Tradeify | FULL | P +0.93/.981 | F +0.83/.964 | F | F |
| Tradeify | 2021+ | P +1.22/.994 | P +1.14/.989 | P +1.07/.982 | P +0.99/.972 |
| MFFU | FULL | P +0.92/.980 | F +0.83/.963 | F | F |
| MFFU | 2021+ | P +1.21/.993 | P +1.13/.989 | P +1.06/.982 | P +0.98/.971 |
| BluSky-NT | FULL | P +0.92/.980 | F +0.83/.963 | F | F |
| BluSky-NT | 2021+ | P +1.21/.993 | P +1.13/.989 | P +1.06/.982 | P +0.98/.971 |

**Sign-limb (6a) is cost-robust:** every firm at 1-tick slip holds 6/8 positive years (full) and 5/6 (2021+) — cost does not flip the year signs.

---

## Reading

1. **The full-window gate needs the cheapest firm AND ≤1-tick fills.** Only Bulenox
   ($0.61/side) clears the full window at 1-tick slip; the three costlier firms
   ($0.91–0.95/side) already fail there, and even Bulenox fails once slip reaches 2 ticks.
   The Stage-6 full-window RESOLVED was therefore correctly flagged as Bulenox-and-tight-fills
   specific — Stage 7 confirms it precisely.
2. **The 2021+ regime window is robust across the whole matrix.** All four firms pass at up to
   **3 ticks** of added slip (annSR +0.98 → +1.28, DSR ≥ 0.97 everywhere). On the regime the
   mechanism actually lives in (post-2020, per N2), firm choice and realistic fill degradation
   do **not** break the edge. This is the operationally-relevant read — a live deployment runs
   on the current regime, not the 2019–2020 dead period.
3. **So the honest synthesis:** the candidate is a **real, firm-and-slip-robust edge on the
   post-2020 regime**; its viability rests on that regime persisting (the standing N2 caveat,
   with 2026-partial the live tripwire). The *full-window* number is the more conservative test
   and it is marginal — which is expected, because the full window dilutes the live regime with
   the two dead years the mechanism is documented to have been off during.

## Caveats carried forward (unchanged by Stage 7)

- **Symmetric-RT slip is conservative** vs an asymmetric entry-only slip (exit-at-close is a
  clean market order), so a realistic entry-slip-only model passes at least as well — the grid
  is a lower bound on survival.
- **Pre-selected construct** (Stage-6 caveat 2): the 2021+ robustness is partly circular — both
  the construct and the 2021+ window were selected knowing that period was strong. The full
  window is the less-circular test, and it is the marginal one. Both are reported; neither is
  hidden.
- **Integer micro sizing** (the other Stage-7 axis): the per-trade R is normalized by OR range,
  so the *edge magnitude* is sizing-invariant; whether the risk-per-trade fits each $100K tier's
  trailing-DD is a Stage-8 / deployment-fork question, and the Phase-A floors
  (`futures_conversion_2026-07-01`) already price MNQ integer rounding (~8% loss at $150K).

## Disposition

- **Stage-7:** realism mapped. **Edge survives all four FRIENDLY firms on the 2021+ regime**
  (up to 3-tick slip); **full-window survival is Bulenox-and-≤1-tick-specific.** Not a
  deployment authorization.
- **Manifest:** stays **open** (Stage 8 breadth pending).
- **Next:** Stage-8 breadth (ENB / correlation-delta vs the book + exposure declaration) with the
  comparison-target question (CFD 4-leg anchor vs the emerging prop-portfolio book) resolved
  first. Only after Stage 8 does lifecycle CANDIDATE admission arise; rail/account/live-spend
  stay separately gated. The regime-dependence (2021+ carries it; 2026-partial the watch item) is
  the dominant open risk, not firm cost.

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_stage7.py
```
