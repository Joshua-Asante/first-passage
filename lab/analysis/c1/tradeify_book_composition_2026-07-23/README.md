# tradeify_book_composition_2026-07-23

Tradeify Select 100K **prop-leg economics / book-composition gap analysis**
(2026-07-23). Feeds the 08-08 gate as measurement input — not a live-ops GO.

Companion brief (filed):
[`docs/briefs/programs/2026-07-23-tradeify-book-composition.md`](../../../docs/briefs/programs/2026-07-23-tradeify-book-composition.md)
(§1 posture corrected; §0.5/§6 split chain-rate vs bust-floor compose vs Q-COMPOSE-1 / Q-FUNNEL-1).

## Status

**ACTIVE** — harness ported; panels under `out/` reproduce the brief §2 anchors
under the **corrected** eval geometry (no eval-phase floor lock; article
10495897). See [`RESULTS.md`](RESULTS.md) for the 2026-07-28 before/after table
and the corrected 2-leg chain rate **$318/acct-mo** (was $339 under the
defective lock). Does **not** authorize ORB compose or Aegis unpark. See
Q-COMPOSE-1 (`CLOSED — FALSIFIED`) and live-ops posture (`dry_run=true`, B7
separate GO).

## Layout

| path | role |
|---|---|
| `inputs/` | gitignored TV List-of-Trades CSVs (2026-07-23 vintage) |
| `out/daily_panel.csv` | 2-leg business-day EOD panel (stage 1) |
| `out/book_panels.csv` | p2/p3/p4 + q2/q3/q4 (stage 4) |
| `gap_stage1.py` … `gap_stage4.py` | pipeline |
| `gap_stage2_capbound.py` | rail 69/11 re-sizing vs panel (imports into Q-CAPALLOC-1) |
| `rerun_section2.py` | §2 scenario set + ORB@k frontier re-derivation |
| `RESULTS.md` | eval-lock fix + before/after + M-24 sweep |
| `assert_anchors.py` | brief §10 headline checks (panel means / stack) |
| `paths.py` | reconcile import + CSV filename map |

## Inputs (drop into `inputs/`)

Exact filenames expected by `paths.CSV`:

- `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-23_626e8.csv`
- `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-23_0ebc6.csv`
- `Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-23_6aa5d.csv`
- `ORB_MNQ_v0.2_CME_MINI_MNQ1!_2026-07-23_ad732.csv`

## Run

```bash
# from repo root
python lab/analysis/tradeify_book_composition_2026-07-23/gap_stage1.py
python lab/analysis/tradeify_book_composition_2026-07-23/gap_stage2.py   # ~minutes
python lab/analysis/tradeify_book_composition_2026-07-23/gap_stage3.py   # ~minutes
python lab/analysis/tradeify_book_composition_2026-07-23/gap_stage4.py   # ~minutes
python lab/analysis/tradeify_book_composition_2026-07-23/assert_anchors.py
```

Reconcile loader: `.claude/skills/trade-csv-reconcile/scripts/reconcile.py`.

## Posture notes (do not erase)

- Account in repo ops: Tradeify Select **100K eval**, B6 dry-fire PASSED, **disarmed**.
- ORB active working edition is `orb_mnq_v0_2` (D1–D5; see
  [`orb_mnq_v0_2_CANDIDATE.md`](../../../core/strategies/orb/orb_mnq_v0_2_CANDIDATE.md));
  this study’s export is the pre-D5 v0.2 vintage (`…_ad732.csv`).
- Chain-rate objective ≠ Q-COMPOSE-1 survivor-scoring bust floor.
