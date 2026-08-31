# Q-VOLREGIME-1 L3 chronological halves — 2026-08-31

**Status:** `ACTIVE` — BLOCKED-AT-INPUT: deterministic L3 scorer complete; both
hash-pinned vendor panels are absent from this checkout.

The scorer and its boundary tests
are complete, but neither hash-pinned vendor panel is present in this checkout.
No L3 statistic was computed and no instrument verdict changed.

## Hard stop

Packet A1 of the authorized plan requires `MNQ_M15.csv` and `MYM_M15.csv` to
match their tracked hashes before scoring. This checkout contains only
`core/data/bar_data/README.md` and `SHA256SUMS`; a full-filesystem search found
no copy of either CSV, and no Databento or TradingView credential is available
in the environment. The plan explicitly makes absent or mismatched bytes a hard
stop, so substituting a public proxy, reconstructing aggregates, or proceeding
to L5 would violate the freeze.

Expected inputs:

| Instrument | Relative path | Required SHA-256 |
|---|---|---|
| MNQ | `core/data/bar_data/MNQ_M15.csv` | `6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a` |
| MYM | `core/data/bar_data/MYM_M15.csv` | `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58` |

## Prepared execution

`l3_halves.py` reuses the frozen L4 scored-frame builder, sorts valid pairs by
UTC timestamp, fixes the split at the observation midpoint, and scores each
half using the minimum lift across the two own-range strata. L3 passes only if
that minimum is strictly positive in both halves. The script writes the panel
hashes, exact split boundary, counts, rates, four per-instrument stratum lifts,
half minima, and verdict to `l3_results.json`.

Run once the exact vendor bytes are restored:

```bash
python lab/analysis/_inbox/volregime_l3_2026-08-31/l3_halves.py
```

Packet B–D remain intentionally unexecuted: their entry gate is at least one
real-panel L3 PASS. This is an input block, not an empirical failure of either
volume-regime hypothesis.
