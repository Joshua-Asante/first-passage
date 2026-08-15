# inputs/ — vendor-licensed TV exports (gitignored, local-only)

The six raw Pepperstone TradingView exports this analysis consumes are
**vendor-licensed** (Pepperstone TOS: personal export OK, redistribution not) and
are **gitignored** (`lab/analysis/**/inputs/*.csv`). They are not committed to this
public repo. Only this README is tracked.

To reproduce the analysis, drop these BT-OFF + daily-cap exports (2020-01 → 2026-06,
Pepperstone) into this directory with these exact filenames (the loader maps them by name):

| strategy | file(s) |
|---|---|
| Guardian Gold v5.5 | `Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-07_6f4dd.csv` (2020-H1) + `..._47d56.csv` (2020-07+) |
| Striker DJ30 v4.5 | `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-07_96110.csv` (2020-2022) + `..._1a81c.csv` (2022+, 3-day seam dedup) |
| Aegis USDJPY v4.3 | `Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-07_ea6ce.csv` |
| Striker NAS100 v1 | `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-07_2ad6c.csv` |

Then run `python decompound.py` (round-trip self-check) and the rest of the pipeline
per `../RESULTS.md` § Reproduce. With the CSVs absent, the scripts error rather than
skip — the data is the input, not an optional fixture.
