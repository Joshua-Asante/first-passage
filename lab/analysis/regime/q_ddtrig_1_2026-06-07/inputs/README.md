# inputs/ — vendor-licensed TV exports (gitignored, local-only)

The four **proposed-bundle** Pepperstone TradingView exports this analysis consumes
are **vendor-licensed** (Pepperstone TOS: personal export OK, redistribution not) and
**gitignored** (`lab/analysis/**/inputs/*.csv`). Only this README is tracked.

These encode the *proposed de-risk bundle* (NOT the locked config): Guardian 0.25% +
1.25% day-DD stop, DJ30 0.50% / pyramid 750%, Aegis 1.50% (unchanged), NAS 0.37% /
pyramid 700% / **Mon-Tue-Fri**. All four are `percent_of_equity` (compounded) BT-OFF
exports spanning 2020-01 → 2026-06; the loader de-compounds them via roe reconstruction.

To reproduce, drop these exports into this directory with these exact filenames
(`bundle_remc.py:PROPOSED_FILES` maps by name):

| strategy | file | n trades | export-risk |
|---|---|---|---|
| Guardian Gold v5.5 (0.25% + day-stop) | `Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-07_2a8da.csv` | 321 | 0.25% |
| Striker DJ30 v4.5 (0.50% / pyr 750) | `Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-07_add05.csv` | 269 | 0.50% |
| Aegis USDJPY v4.3 (1.50%) | `Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-07_917de.csv` | 149 | 1.50% |
| Striker NAS100 v1 (0.37% / pyr 700 / Mon-Tue-Fri) | `Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-07_51027.csv` | 420 | 0.37% |

With the CSVs absent, the scripts error rather than skip — the data is the input, not
an optional fixture. Filename token says "v5.5/v4.5/v1" per the no-version-bump
doctrine, but the *behavior* is the proposed bundle (e.g. Guardian here has a day-DD
stop the locked v5.5 lacks — 23 `DD Limit` exits).
