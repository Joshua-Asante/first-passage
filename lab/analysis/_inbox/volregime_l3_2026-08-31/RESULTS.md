# Q-VOLREGIME-1 L3 chronological halves — 2026-08-31

**Status:** `ACTIVE` — L3 PASS independently on MNQ and MYM; the presence battery is complete on both instruments and L5 attribution remains open.

## Result

| Instrument | Scored `n` | Second-half start (UTC) | First-half minimum lift | Second-half minimum lift | L3 |
|---|---:|---|---:|---:|---|
| MNQ | 135,958 | 2023-08-15 08:00 | +21.7413 pp | +22.9892 pp | **PASS** |
| MYM | 139,605 | 2023-07-18 08:45 | +16.4755 pp | +16.3383 pp | **PASS** |

All four within-own-range-stratum lifts are positive in both chronological
halves on both instruments. Full conditional/reference counts and rates,
scored-frame spans, midpoint indices, panel hashes, and the executed script hash
are recorded in `l3_results.json`.

The execution-code manifest records both the CRLF worktree-byte hashes used at
runtime and the logically identical LF-normalized Git-blob hashes for the L3
wrapper and imported L4 scored-frame builder. Review hardening added complete
two-panel preflight, invalid-row filtering, empty-stratum-safe printing, and an
archive-visible dependency path after execution; the frozen observed statistic
was not rerun.

The run used the hash-pinned vendor panels:

| Instrument | Relative path | SHA-256 |
|---|---|---|
| MNQ | `core/data/bar_data/MNQ_M15.csv` | `6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a` |
| MYM | `core/data/bar_data/MYM_M15.csv` | `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58` |

No fresh K is charged: L3 is the already-owed presence diagnostic on
already-scored panels from already-closed, K-declared discovery manifests.

## Prior blocked state

Earlier on 2026-08-31 this packet was `BLOCKED-AT-INPUT` because the private
vendor CSVs were absent from that checkout. The exact hash-pinned files were
later restored from the primary checkout into this isolated worktree and
verified before execution. The prior block was an environment state, not an
empirical result, and is retained here rather than erased from the history.

## Disposition

Both instruments carry forward independently to the future Packet B / L5
design-amendment route. Q-VOLREGIME-1 remains `OPEN`: an L3 PASS completes the
presence battery but is neither `RESOLVED` nor `CERTIFIED`. Packets B-D were not
started in this execution session.
