# P2 replay — Phase-A NOTES (no RESULTS: nothing scored)

**Date:** 2026-07-03 · **Branch:** `analysis/p2-replay-2026-07` (off `origin/main` @ `ad96228`)
**Handoff:** `C:\Users\joshu\Downloads\2026-07-03-cc-handoff-p2-replay-k2-e1.md` (Phase A §2.1–2.6 only)
**Status:** Phase A DONE + HALT. Phase B awaits Joshua's 4 exports + window pin (§0.5-b) + K2/E1 gate ratification.

## §0 Phase-0 read results (with `git log -1 --oneline -- <path>`)

1. **Parent ADR** `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` — `9347458` — **PREMISE-CONFIRMED**. Gates verbatim: **K2** "KILL a leg if divergence > 10% of signals **[RATIFY]**; below that, the measured delta becomes an input to the E1 envelope rather than a pass" (§2); **E1** "Envelope per leg **[RATIFY]**: PF ≥ 0.8× baseline AND net ≥ 0.7× baseline" (§2). Both `[RATIFY]`-pending → the harness carries them only as `*_RATIFY_PENDING` reference constants; every scorer takes explicit values, no defaults.
2. **Feed-canon ADR** `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` — `6f2f468` — **PREMISE-CONFIRMED**. Both replay exports are TV Strategy-Tester CSVs → inside canon. Bar panels enter this pipeline ONLY as classification aids (roll-seam dates via `roll_mask`, bar-existence indexes for SESSION/BASIS/DATA-GAP labels), never as canonical price/verdict inputs — consistent with §2.2 staging-only doctrine. No Dukascopy/non-TV price source anywhere (handoff §5.4).
3. **trade-csv-reconcile conventions** `.claude/skills/trade-csv-reconcile/` — `d72c58c` — **PREMISE-CONFIRMED**. Two TV export schemas exist (legacy `Trade #` vs current `Trade number`/`Net PnL USD`/`Size (value)`; SKILL.md trap #13/#14 — the current schema previously zeroed pyramid-share attribution). The ingest REUSES the skill's `load_csv` (COLUMN_ALIASES both-schema normalization, BOM, exits-only P&L per Q-A1-c) rather than re-deriving a parser. Pyramid adds handled under BOTH layouts: current = per-leg `... Add` Signal detection; legacy = 2nd+ Entry row per Trade # ordinal detection.
4. **Baseline lineage** `core/data/tv_exports/pepperstone/SHA256SUMS` — `6f18a6a` — **PREMISE-CONFIRMED**. Pinned Pepperstone vintages exist for both legs (latest: `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-26_74bd5.csv`, `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-26_6facd.csv`). NOTE: the E1 baseline is the **new paired same-window Pepperstone export** Joshua makes per EXPORT_SPEC.md — never the pinned MC anchors and not these older vintages (handoff §5.5); the manifest is lineage context only. Vendor CSVs are gitignored and ABSENT from this worktree — all fixtures are synthetic.
5. **Fixture requirement** `docs/adr/2026-05-16-fixture-test-requirement.md` — `5df088e` — **PREMISE-CONFIRMED**. This harness is brief-evidence code → fixture tests mandatory; delivered (31 tests, all green; see below). The §0.5-e first-trade sanity check is the F-1/JPY-153× defect-class insurance that ADR anchors.

Reuse read (recon item): `lab/analysis/futures_conversion_2026-07-01/roll_mask.py` — `5dcdbea` — REUSED via `p2_diff_k2.seam_timestamps_from_bars` (symbol map MYM1!/MNQ1! → YM/NQ parent roll cycles; no new roll calendar written). Its documented SCOPE (per-bar safety, not path reconstruction) is respected — it is used here only to date seam bars for divergence classification.

## Design decisions (frozen)

- **Pairing key:** ET bar timestamp of each Entry row (pyramid adds are signals in their own right and join the union set). Direction flip at a paired timestamp counts as a divergence.
- **Timezone:** exports declared chart-TZ New York (EXPORT_SPEC); `load_export` localizes DST-aware (`ambiguous=True`, `nonexistent="shift_forward"` — identical rule both feeds, so pairing is unaffected) and converts to ET.
- **Grid:** every timestamp must sit on the 15m grid; violation → `GridAlignmentError` ("NEEDS_CONTEXT: …"), exit 3 in the CLI — never silently resampled (§0.5-d). Advisory-only warning for all-minute-zero exports (possible hourly chart).
- **Classification precedence:** ROLL-SEAM (±2 bars of a seam bar) > SESSION (bar on exactly one feed) > BASIS (both bars exist) > DATA-GAP (neither). SESSION/BASIS/DATA-GAP require per-feed bar-timestamp indexes; absent → NEEDS_CONTEXT, no guessing.
- **Roll treatments (§0.5-c):** both always emitted. `with-roll` = divergent/union; `ex-roll` = ROLL-SEAM-classified divergent signals removed from BOTH numerator and denominator (carve-out removes those signal points from the set). Presented side by side; carve-out decision is Joshua's at scoring time — nothing decided here.
- **Window:** always an explicit input (`--window-start/--window-end`, `filter_window` required args). No dates hardcoded anywhere in the harness. E1 filters BOTH sides inside `e1_ratios` with the same bounds (identical-window enforcement, §7). Trade ∈ window iff its FIRST entry ts ∈ [start, end); an included trade keeps its full realized P&L.
- **Envelope guards:** exits-only P&L; zero-loss PF and non-positive baseline net are hard NEEDS_CONTEXT errors (ill-conditioned ratios), not silent verdicts.
- **Scoring:** `score_k2`/`score_e1` have NO default thresholds; the CLI `--score` additionally requires `--gates-ratified` + explicit values + the §0.5-c treatment choice.

## Fixture schema coverage

| Fixture | Schema | Exercises |
|---|---|---|
| `pep_diff_new.csv` / `cme_diff_new.csv` | current | all 4 divergence classes + direction-flip + E1 ratios |
| `pep_pyramid_new.csv` / `cme_pyramid_new.csv` | current | pyramid-add pairing (per-leg `Long Add`) |
| `dj30_pyramid_legacy.csv` | legacy | legacy multi-entry pyramid: signals, sanity, exits-once P&L |
| `first_trade_clean_new.csv` / `first_trade_corrupt_new.csv` | current | §0.5-e first-trade sanity pass / 153× fail |
| `misaligned_grid_new.csv` | current | off-grid hard error (§0.5-d) |
| `legacy_basic.csv` | legacy | legacy-schema parse |

ROLL-SEAM's seam source is a synthetic 3-bar CME panel run through the real `roll_mask` calendar (0.72% gap on 2026-06-10, inside the quarterly June window).

## Seeded-defect verification (performed 2026-07-03)

Temporarily replaced `window = ROLL_SEAM_BAR_WINDOW * BAR_INTERVAL` with `window = 0 * BAR_INTERVAL` in `p2_diff_k2.classify_divergence` (kills the ±2-bar seam window). Result: **4 failed, 27 passed** — `test_taxonomy_one_fixture_per_class_and_sums_to_total`, `test_each_divergent_signal_classified_as_designed`, `test_both_roll_treatments_emitted`, `test_score_k2_takes_explicit_threshold_only` all failed (T2 mis-classified BASIS; ex-roll number shifted). Restored the line; suite back to **31 passed**. The ROLL-SEAM classifier fixture demonstrably fails on its seeded defect.

## Freeze declaration (handoff §5.3)

The alignment and classification rules — ET normalization (incl. the DST conventions), the 15m grid assertion, the timestamp pairing key, the ROLL-SEAM ±2-bar window, the SESSION/BASIS/DATA-GAP precedence, and the ex-roll carve-out arithmetic — are **FROZEN as of this Phase-A fixture-green commit**. They must not be adjusted after real exports arrive to make divergence counts drop. Any genuine defect discovered in Phase B routes through NEEDS_CONTEXT back to the operator, not through a silent rule edit.

## Phase-B inputs owed (awaiting Joshua)

1. The 4 CSVs per `EXPORT_SPEC.md` (+ adjustment-mode screenshots).
2. The §0.5-b window pin.
3. Ratification (or revision) of K2 10% / E1 0.8×+0.7× gate values and the §0.5-c roll-treatment call at scoring time.
4. Per-feed 15m bar-timestamp indexes for cause classification (UTC-`time` CSVs; classification aid only) — the CME ones also feed `roll_mask` seam dating.
