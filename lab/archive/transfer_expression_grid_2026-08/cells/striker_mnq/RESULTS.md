# RESULTS — Q-TXG-1 cell striker × MNQ (Blocks 4–5)

**Verdict:** DEAD(N-SURV) · 2026-08-12 · \ · K declared=1 · K actual=1
**Closure:** [docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md](lab/archive/../../../../../docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md)
**Manifest:** [discovery_manifests/q_txg1_striker_mnq_20260812.json](lab/archive/../../../../../discovery_manifests/q_txg1_striker_mnq_20260812.json)

## Cost gate

| Metric | Value |
|---|---|
| N | 222 |
| Net USD | +22,789.58 |
| PF | 1.308 |
| mean_net_r | 0.0419 |
| required_net_r | 0.03 |
| static-equity recompute | OK (max \|Δ\| ~0) |
| Gate | **PASS_COST** |

## N-SURV (Tradeify_Select_100K, bar-derived MNQ_M15)

`
firm=Tradeify_Select_100K sizing_basis=\,000 half_boundary=2024-03-19
floor: bust≤3.0% ∧ P(pass)≥50%
full: bust=98.13% pass=1.87% FAIL (n=164)
H1: bust=96.76% pass=3.24% FAIL (n=82)
H2: bust=99.37% pass=0.63% FAIL (n=82)
N-SURV FAIL
`

Machine JSON: [PANEL_SCORE.json](PANEL_SCORE.json) · [NSURV_BLOCK.txt](NSURV_BLOCK.txt)
