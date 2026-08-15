# Q-KBUDGET-HARVEST-1 Phase-3 — extended floor scan RESULTS

**Status:** `COMPLETE` — harvest §6 **`RESOLVED`** (2026-07-16)
**Date:** 2026-07-16
**Zero pulls / zero K.** Parent Q-KBUDGET-1 remains RESOLVED (not reopened).

## Citations

- Parent Pre-Q: [`docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](../../../docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md)
- Frozen harvest pre-reg: [`Q-KBUDGET-HARVEST-1-verdict-preregistration.md`](../../../docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md) §B
- Inventory addendum: [`Q-KBUDGET-HARVEST-1-inventory-addendum.md`](../../../docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md)
- Phase-2 record: [`PHASE2_RATIFICATION.md`](PHASE2_RATIFICATION.md)
- Standing screen: [`lab/research_utils/axis_screen.py`](../../research_utils/axis_screen.py)
- Campaign harness (append-only): [`../q_kbudget_1_2026-07/floor_scan.py`](../q_kbudget_1_2026-07/floor_scan.py)
- Manifest: [`phase3_screen_manifest.json`](phase3_screen_manifest.json) (D1–D7 fixture + H1/H2)
- Machine output: [`phase3_results.json`](phase3_results.json)

## Harvest §6 verdict

**`RESOLVED`** — ≥1 harvested row operator-ratified (H1+H2) **and** `floor_scan.py` extended + run (also via `axis_screen` + manifest).

Extended fundable set (PASS both clauses): **3** axes — D5 (1) + harvest H1/H2 (2).

Screen PASS licenses campaign scoping only — does not bless a candidate, authorize a pull, or open K.

## Extended screen table (`axis_screen` on phase3_screen_manifest.json)

```
| Axis | Family | K_eff | floor(K_eff) | Clause K (Cap 1.0) | Clause N | Screen |
|---|---|---|---|---|---|---|
| D1 GC/MGC successor (any design) | GC/MGC | 3178 | 2.05 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D2 wide mining, other GLBX family | ES/NQ/YM | 1001-10001 | 1.925-2.165 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D3 HARV-class ES month-end mechanism | ES | 2-3 | 0.85-0.98 | PASS | INHERITED FAIL: P(primary|true) ~= 0.24-0.30, joint 0.05-0.06 (Q-HARV-1 SS-R DECLINE, commit 9bddd33; N ~= 100 month-ends 2018+) | **FAIL (Clause N, inherited)** |
| D4 XAU T3b swap-dealer COT (prop expression = GC/MGC) | GC/MGC | 3178-3179 | 2.05 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D5 NQ/MNQ intraday-momentum footprint (was: gamma-positioning) | MYM/MNQ | 1-3 | 0.65-0.98 | PASS | PASS: power=0.947 at N=1000, delta/sigma=0.113 (Baltussen et al. 2021 JFE NQ cohort (d5_clause_n_rescreen.md)) | **PASS** |
| D6 eurusd_pattern_enum Phase-4 (locked K=450) | 6E/EURUSD | 450 | 1.835 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D7 JPY month-end mechanism (6J expression) | 6J | 1-3 | 0.65-0.98 | PASS | FAIL (N): power=0.303 < 0.5 at N=100, delta/sigma=0.14444444444444443 (HARV class-analogue +13bp/90bp (Q-HARV-1 SS-R 9bddd33; d7_clause_n_screen.md)) | **FAIL (Clause N)** |
| H-OD-1 overnight-drift inventory-risk (2:00-3:00 ET) | ES | 2-3 | 0.85-0.98 | PASS | PASS: power=0.837 at N=1000, delta/sigma=0.093 (Boyarchenko/Larsen/Whelan FRBNY SR917 Table I; harvest addendum H1; Path 1a; RATIFIED 2026-07-16) | **PASS** |
| H-TSMOM-1 Moskowitz-Ooi-Pedersen 12m/1m TSMOM confirm (S&P 500 / ES) | ES | 2 | 0.85 | PASS | PASS: power=0.638 at N=192, delta/sigma=0.167 (Moskowitz/Ooi/Pedersen 2012 JFE Fig.2 S&P 500 gross SR=0.58 → δ/σ=0.167; H_TSMOM_1_fig2_scrape.md; harvest addendum H2; Path 1b PASS; N=192; RATIFIED 2026-07-16) | **PASS** |

Screened FAIL: 6/9 · PASS: 3 · UNSCREENABLE: 0
Verdict per pre-reg §D: RESOLVED (fundable set non-empty)
```

## Campaign harness confirmation (`floor_scan.py` after append-only H1/H2)

```
| Axis | Family | K_eff | floor(K_eff) | Clause K (Cap 1.0) | Clause N | Screen |
|---|---|---|---|---|---|---|
| D1 GC/MGC successor (any design) | GC/MGC | 3178 | 2.05 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D2 wide mining, other GLBX family | ES/NQ/YM | 1001-10001 | 1.925-2.165 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D3 HARV-class ES month-end mechanism | ES | 2-3 | 0.85-0.98 | PASS | INHERITED FAIL: P(primary|true) ~= 0.24-0.30, joint 0.05-0.06 (Q-HARV-1 SS-R DECLINE, commit 9bddd33; N ~= 100 month-ends 2018+) | **FAIL (Clause N, inherited)** |
| D4 XAU T3b swap-dealer COT (prop expression = GC/MGC) | GC/MGC | 3178-3179 | 2.05 | FAIL | UNSCREENABLE-moot (no citable delta; cannot flip — Clause K kills any GC/MGC expression independently) | **FAIL (Clause K)** |
| D5 NQ/MNQ intraday-momentum footprint (was: gamma-positioning) | MYM/MNQ | 1-3 | 0.65-0.98 | PASS | PASS: confirm-construct = intraday-momentum footprint (Baltussen et al. 2021 JFE NQ cohort, delta/sigma=0.113, power=0.947 at N=1000); DJ30 drop/down-weight; operator-ratified 2026-07-15 — see d5_clause_n_rescreen.md | **PASS** |
| D6 eurusd_pattern_enum Phase-4 (locked K=450) | 6E/EURUSD | 450 | 1.835 | FAIL | n/a — Clause K kills first | **FAIL (Clause K)** |
| D7 JPY month-end mechanism (6J expression) | 6J | 1-3 | 0.65-0.98 | PASS | FAIL (N, class-analogue): P(primary|true) ~= 0.30 < 0.50 at N~=100, delta/sigma=0.144 (HARV class-analogue, Q-HARV-1 SS-R 9bddd33) -- see d7_clause_n_screen.md | **FAIL (Clause N)** |
| H-OD-1 overnight-drift inventory-risk (2:00-3:00 ET) [harvest H1] | ES | 2-3 | 0.85-0.98 | PASS | PASS: power=0.837 at N=1000, delta/sigma=0.093 (FRBNY SR917 Table I; harvest addendum H1; Path 1a; RATIFIED 2026-07-16) | **PASS** |
| H-TSMOM-1 Moskowitz 12m/1m TSMOM (S&P500/ES) [harvest H2] | ES | 2 | 0.85 | PASS | PASS: power=0.638 at N=192, delta/sigma=0.167 (Moskowitz Fig.2; H_TSMOM_1_fig2_scrape.md; harvest addendum H2; Path 1b PASS; RATIFIED 2026-07-16) | **PASS** |

Screened FAIL: 6/9 · PASS: 3 · UNSCREENABLE: 0
Verdict per pre-reg §D: RESOLVED (fundable set non-empty)
```

## Per-harvest-row detail

| ID | Axis | K_eff | floor | Clause K | Clause N power | Screen |
|---|---|---|---|---|---|---|
| H1 | H-OD-1 overnight-drift inventory-risk (2:00-3:00 ET) | 2-3 | 0.85-0.98 | PASS | 0.837 | **PASS** |
| H2 | H-TSMOM-1 Moskowitz-Ooi-Pedersen 12m/1m TSMOM confirm (S&P 500 / ES) | 2 | 0.85 | PASS | 0.638 | **PASS** |

## Honesty riders (unchanged from addendum)

- **H1:** unconditional OD Sharpe collapses net of bid–ask (SR917 Table IX); 2021+ fade via RSV-dispersion compression. **MNQ/NQ (or MYM) expression is UNSCREENABLE** (`nq-native-delta-sigma-not-extracted`) — ES-only δ; ES→NQ transplant inadmissible (Phase-2 amendment / intake ADR req. 2).
- **H2:** gross Sharpe only; monthly event rate; haircut SR=0.45 fails Clause N at N=192; family ES only (no NQ transplant).

## Reproduce

```bash
PYTHONPATH=lab python -m research_utils.axis_screen \
  lab/analysis/q_kbudget_harvest_1_2026-07/phase3_screen_manifest.json \
  --out lab/analysis/q_kbudget_harvest_1_2026-07/phase3_results.json
# expect: PASS: 3 · … RESOLVED (D5 + H-OD-1 + H-TSMOM-1)

python lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -5
# expect: PASS: 3 · … RESOLVED (fundable set non-empty)
```
