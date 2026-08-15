# Q-FUNNEL-1 — funnel EV sweep RESULTS

**Status:** `RESOLVED` — mechanical readout of pre-reg §6 (not the study closure-of-record; that is operator/CC-side §9).
**Verdict: CLOSED — RESOLVED (funnel-EV materially prefers 1.00x over ratified WATCH-1 0.50x on 2/4 horizon-robust trigger points; 2/4 are horizon-fragile per post-merge sensitivity check). Canonical closure: [`docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md`](lab/archive/../../docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md).**
**Pre-registration (FROZEN):** [`Q-FUNNEL-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md)
**Eval fee pin (Q-RAIL-1 Phase 4):** $328 list / $258 promo (list used).
**MAX_RETRIES:** 5 · **§3(a) floor:** 25% relative
**n_lineages/cell:** 500 · wall 804.6s

## §0.5 resolutions applied

- **A** — busted-post-funding keeps prior payouts (no clawback)
- **B** — funded continuation from same week-block-bootstrap panel
- **C** — winning-day counter resets after each payout (cycle-based)
- **D** — per-leg de-mean before recombine

## §6 gate application (mechanical)

**Verdict: `RESOLVED`**

- Resolved points (a+b+c): 4
- Ambiguous points (a+b but not c): 2

### RESOLVED triggers

- edge=`edge_panel_historical` policy=`no_retry` better_rung=`1.0` H1_lift=923.3% H2_lift=309.7%
- edge=`edge_panel_historical` policy=`retry_to_cap` better_rung=`1.0` H1_lift=1016.8% H2_lift=275.6%
- edge=`edge_half_panel` policy=`no_retry` better_rung=`1.0` H1_lift=405.4% H2_lift=379.5%
- edge=`edge_half_panel` policy=`retry_to_cap` better_rung=`1.0` H1_lift=471.9% H2_lift=368.2%

### AMBIGUOUS-HOLD triggers

- edge=`edge_0` policy=`no_retry` H1_better=`0.25` H2_better=`1.0` (direction reverses H1↔H2)
- edge=`edge_0` policy=`retry_to_cap` H1_better=`0.25` H2_better=`1.0` (direction reverses H1↔H2)

## Cell table (EV/day + bootstrap 5th–95th)

| rung | policy | edge | half | EV/day | boot 5th | boot 95th | mean days |
|---|---|---|---|---:|---:|---:|---:|
| 0.25× | no_retry | edge_0 | H1 | -0.3405 | -0.3511 | -0.3318 | 963.4 |
| 0.50× | no_retry | edge_0 | H1 | -0.7451 | -0.7912 | -0.7102 | 427.5 |
| 1.00× | no_retry | edge_0 | H1 | -1.4675 | -1.6722 | -1.2065 | 185.2 |
| 0.25× | retry_to_cap | edge_0 | H1 | -0.3395 | -0.3436 | -0.3354 | 5797.2 |
| 0.50× | retry_to_cap | edge_0 | H1 | -0.7624 | -0.7825 | -0.7400 | 2480.7 |
| 1.00× | retry_to_cap | edge_0 | H1 | -1.4939 | -1.5669 | -1.3962 | 1038.4 |
| 0.25× | no_retry | edge_0 | H2 | 0.5139 | 0.4374 | 0.6002 | 1530.1 |
| 0.50× | no_retry | edge_0 | H2 | 2.0771 | 1.8911 | 2.2600 | 772.7 |
| 1.00× | no_retry | edge_0 | H2 | 4.4772 | 4.0488 | 4.9703 | 333.1 |
| 0.25× | retry_to_cap | edge_0 | H2 | 0.4471 | 0.4012 | 0.4899 | 3941.1 |
| 0.50× | retry_to_cap | edge_0 | H2 | 2.0844 | 1.9523 | 2.2241 | 1368.1 |
| 1.00× | retry_to_cap | edge_0 | H2 | 3.8306 | 3.5662 | 4.1339 | 940.6 |
| 0.25× | no_retry | edge_panel_historical | H1 | 0.2895 | 0.2103 | 0.3526 | 1579.7 |
| 0.50× | no_retry | edge_panel_historical | H1 | 1.6452 | 1.4979 | 1.7653 | 1022.2 |
| 1.00× | no_retry | edge_panel_historical | H1 | 2.9625 | 2.7260 | 3.1799 | 695.0 |
| 0.25× | retry_to_cap | edge_panel_historical | H1 | 0.2556 | 0.1967 | 0.3120 | 2203.0 |
| 0.50× | retry_to_cap | edge_panel_historical | H1 | 1.6310 | 1.4941 | 1.7666 | 1051.8 |
| 1.00× | retry_to_cap | edge_panel_historical | H1 | 2.8540 | 2.6080 | 3.1021 | 693.5 |
| 0.25× | no_retry | edge_panel_historical | H2 | 2.9140 | 2.7791 | 3.0531 | 949.0 |
| 0.50× | no_retry | edge_panel_historical | H2 | 6.0163 | 5.7096 | 6.2651 | 598.5 |
| 1.00× | no_retry | edge_panel_historical | H2 | 11.9399 | 11.5326 | 12.3996 | 464.2 |
| 0.25× | retry_to_cap | edge_panel_historical | H2 | 3.0430 | 2.9153 | 3.2110 | 923.1 |
| 0.50× | retry_to_cap | edge_panel_historical | H2 | 5.6833 | 5.4176 | 5.9390 | 608.2 |
| 1.00× | retry_to_cap | edge_panel_historical | H2 | 11.4304 | 10.9347 | 11.8470 | 493.8 |
| 0.25× | no_retry | edge_half_panel | H1 | -0.1852 | -0.1925 | -0.1776 | 1704.0 |
| 0.50× | no_retry | edge_half_panel | H1 | 0.2106 | 0.1358 | 0.2909 | 1178.7 |
| 1.00× | no_retry | edge_half_panel | H1 | 0.5658 | 0.3385 | 0.8030 | 455.3 |
| 0.25× | retry_to_cap | edge_half_panel | H1 | -0.1770 | -0.1821 | -0.1711 | 9479.1 |
| 0.50× | retry_to_cap | edge_half_panel | H1 | 0.1460 | 0.0976 | 0.1908 | 3693.4 |
| 1.00× | retry_to_cap | edge_half_panel | H1 | 0.6583 | 0.5511 | 0.7874 | 1412.9 |
| 0.25× | no_retry | edge_half_panel | H2 | 1.8164 | 1.7153 | 1.9539 | 1289.0 |
| 0.50× | no_retry | edge_half_panel | H2 | 4.2945 | 4.0572 | 4.5045 | 765.4 |
| 1.00× | no_retry | edge_half_panel | H2 | 8.7102 | 8.3022 | 9.1393 | 485.9 |
| 0.25× | retry_to_cap | edge_half_panel | H2 | 1.8657 | 1.7458 | 1.9698 | 1363.9 |
| 0.50× | retry_to_cap | edge_half_panel | H2 | 4.1609 | 3.9605 | 4.3807 | 825.9 |
| 1.00× | retry_to_cap | edge_half_panel | H2 | 8.7352 | 8.3363 | 9.1416 | 620.2 |

## Sanity — edge ordering

Per Step 2.4 gate: for each (rung, policy, half), `edge_0` EV/day should be ≤ `edge_panel_historical` (more edge must not produce less EV). Failures listed below (empty = pass).

_(none)_


## Artifacts

- Raw JSON: [`sweep_results.json`](sweep_results.json)
- Harness: [`funnel.py`](funnel.py) · [`run_funnel_sweep.py`](run_funnel_sweep.py)
- Regression pin: `test_funnel.py::test_regression_pin_matches_watch1_ratification`

