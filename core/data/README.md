# `core/data/` — immutable shared panels

CSV bytes are gitignored (vendor TOS); only `SHA256SUMS` + READMEs are tracked.
Integrity: `python scripts/check_data_manifests.py --check`.

| Tree | README |
|---|---|
| [`bar_data/`](bar_data/) | Frozen CME micros |
| [`tv_exports/`](tv_exports/) | CME futures TV trade-lists (live research feed) |
| [`external/`](external/) | Other pinned externals |

Do not restate panel hashes here — they live in the per-dir manifests.
