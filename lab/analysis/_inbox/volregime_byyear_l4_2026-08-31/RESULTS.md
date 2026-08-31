# Q-VOLREGIME-1 bar-level by-year L4 — 2026-08-31

**Status:** ACTIVE — L4 PASS independently on MNQ and MYM; L3 (halves-stability) and L5 (attribution) remain open.

## Result

L4 **PASS** on MNQ and MYM independently.

| Instrument | `N_valid` | Positive years | Required | L4 |
|---|---:|---:|---:|---|
| MNQ | 7 | 7 | 5 | **PASS** |
| MYM | 7 | 7 | 5 | **PASS** |

Annual minimum within-own-range-stratum lifts, 2020 through 2026:

- MNQ: +22.30, +21.57, +26.07, +19.01, +23.01, +21.61, +22.80 pp.
- MYM: +18.25, +19.94, +14.65, +12.82, +16.81, +16.00, +18.04 pp.

Every year independently clears `n_cond >= 20` in both own-range strata. The
2020 and 2026 calendar years are partial panels, but they qualify under the
frozen observation-count rule; no full-year requirement is added after seeing
the result.

## Method and integrity

The calculation reconstructs each instrument's frozen stage-1 scored frame
from its vendor M15 panel, then applies the corrected `Q-RANGEXFER-1` per-stratum
L4 convention: both own-range strata must independently clear the annual
conditional-count floor, and the annual statistic is their minimum lift.

Before scoring, the script verifies the gitignored vendor bytes against tracked
`core/data/bar_data/SHA256SUMS` values. The reconstructed pooled frames reproduce
the committed stage-1 results: MNQ `n_scored=135,958`, lifts +22.3427/+27.3928 pp;
MYM `n_scored=139,605`, lifts +16.4888/+24.5484 pp. Full per-year rates, counts,
and lifts are in `byyear_l4_results.json`.

## Interpretation boundary

This closes L4 specifically and removes panel length as a forced
`AMBIGUOUS-HOLD` route. It does **not** discharge the full presence battery
and does **not** resolve Q-VOLREGIME-1: **L3 (both chronological halves of the
conditional cases show lift > 0) has not been computed for this construct and
remains open**, alongside the frozen L5 joint-surrogation attribution limb.
Neither instrument can reach `RESOLVED` until L3 is scored and L5
independently clears.

No fresh K is charged: this is the already-owed, K-free presence diagnostic on
already-scored vendor panels.

## Reproduce

```bash
python lab/analysis/_inbox/volregime_byyear_l4_2026-08-31/byyear_l4.py
```

Expected headline:

```text
MNQ: n_valid=7 n_pass=7 required=5 L4=PASS
MYM: n_valid=7 n_pass=7 required=5 L4=PASS
```
