# `core/data/tv_exports/` — CME futures TV trade-lists

Canonical live research feed (`cme/`). CSV bytes gitignored; `SHA256SUMS`
is tracked. Integrity:
`python scripts/check_data_manifests.py --check`.

Loader: [`../../tv_export_loader.py`](../../tv_export_loader.py).
OANDA / Pepperstone feeds are retired — do not reintroduce without an ADR.
