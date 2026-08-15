# Q-COMPOSE-1 — Phase-0 architecture confirm (pre-reg §8, executed before Phase 1)

**Date:** 2026-07-17 · **Status:** `CONFIRMED — Phase 1 authorized to run`
**Pre-reg:** [`Q-COMPOSE-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md) (FROZEN 2026-07-16, operator-signed §9)

## §0 anchors re-verified (pre-reg §10 audit hooks, run 2026-07-17)

| Anchor | Expected | Got |
|---|---|---|
| `run_class_s_c1_regime_gate.py` | `163b0b5` | `163b0b5` ✓ |
| `RESULTS_stage8_neff.md` | `9620138` | `9620138` ✓ |
| `2026-07-13-prop-survivor-scoring-prereg.md` | `be6dda6` | `be6dda6` ✓ |
| Floor grep (3.0% / 50%) | unchanged | unchanged ✓ |
| "SINGLE frozen weight" declaration | §2 row | present ✓ |
| Compose harness pre-existing | none expected | none existed pre-Phase-1 ✓ |

`phase0_verify()` (c1 2026-07-15 signature, NO-Aegis declaration, `ACTIVE_FIRM=="FXIFY"`
fixture, gate ceilings 0.03/0.5, frozen tier tuple) passes; both panel CSVs sha256-verified.

## Injection-shape determination (§2 clause — ratified reading)

`build_scaled_panel` itself **cannot** ingest ORB-MNQ-1: it is TV-export-CSV-specific
(sha-pinned `PANEL_FILES`; §8.3 full-stop 1R guard), and ORB's R is definitionally
OR-range-normalized — no fill-derived full-stop cohort exists **by construction**. Any
synthetic CSV or guard bypass would be the §2-forbidden workaround.

The §2 clause is a disjunction — *"into `build_scaled_panel` / book-daily construction"* —
and the executed injection takes the **book-daily-construction** site with zero edits to
any frozen primitive:

1. 2-leg panel via the untouched frozen `build_scaled_panel` (EXPECTED_1R guards intact) —
   span 2020-01-06 → 2026-06-30, 1692 bdays.
2. ORB daily R (engine-faithful: `orb_daily_dated`, R-multiset-asserted identical to
   `orb_lib.orb_backtest` — same self-check as Stage-8) → USD **at the allocation layer**:
   `R × 0.0037 × 200,000` (the committed Stage-8 precedent the pre-reg §0 itself cites).
3. ORB column reindexed onto the 2-leg panel's **frozen** index (fillna 0.0 = flat
   no-trade days, identical treatment to the book legs; 1,665 ORB trade days in-window,
   181 dropped outside — ORB's span fully covers the panel window, so no out-of-window
   zero-fill arises and H1/H2 midpoint partitions are byte-identical to the c1 rider).
4. Only then `book_daily_at_100k(panel3)` collapses the composed 3-column panel.

**Run-2 consistency faithfulness:** `core/mc/simulation.py` L119-124 computes
`max_day_profit − consistency_frac × total_profit` on whatever daily series the sim
receives — under this injection that is the **true composed daily series**, satisfying
§2's "NOT post-hoc on `daily_100k`". `NEEDS_CONTEXT` does not fire.

## Smoke + falsifier (wiring validation, pre-full-run)

- `--smoke` (n_sims=200, n_panels=5, all 4 tiers): runs end-to-end; breadth declaration
  **byte-reproduces Stage-8** (dependence N_eff 1.9948 → 2.9502; risk 1.9593 → 1.9628).
- **2-leg smoke control:** same harness, ORB column omitted, n_sims=200 → full-panel bust
  **2.83%/2.83%** on Tradeify/MFFU vs frozen full-run baseline **2.65%/2.64%** — within
  smoke noise. The harness at smoke scale is faithful; the composed-book bust movement is
  attributable to the ORB column, not a wiring defect.
- Daily magnitude record (100K basis): 2-leg std $273/day; ORB column alone $438/day;
  composed $539/day (§7 risk-dominance disclosure, observed).

## Deviations (documented, non-gating)

- `median_days_to_pass` not surfaced by `summarize_outcomes` — pass_rate reported as the
  practicality proxy (same recorded deviation as the haircut sibling).
- Reproduction control at full n: skipped — not mandated by the compose pre-reg; the
  frozen 2-leg baseline (`REGIME_GATE.md` @163b0b5) was reproduced by the haircut
  sibling's 1.00× control on this machine/venv 2026-07-17, and the smoke-scale control
  above re-confirms harness fidelity.
- DBN cache (`ohlcv-1m_continuous_ce119c1e8f923316.dbn`) sha256 recorded in the run
  report (integrity record; the engine-faithfulness gate is the R-multiset assert).

## Phase-1 authorization

Frozen engine: 10,000 sims × seeds 42/123/2026, horizon 1500, inactivity off,
dd_protection OFF, Run-2 consistency-on where present; partitions full/H1/H2/bootstrap
(n=100, block 126 bd, seed 20260715) × 4 tiers. Driver:
[`run_compose_regime_remc.py`](run_compose_regime_remc.py).
