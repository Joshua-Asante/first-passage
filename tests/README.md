# `tests/` — single suite (contract-exempt)

Imports `core` + `lab` + `ops` at once by design
([boundaries ADR](../docs/adr/2026-06-05-monorepo-layer-boundaries.md) §8 Q-c).
`pyproject.toml` sets `pythonpath = ["core","lab","ops","."]`.

| Path | Mirrors |
|---|---|
| [`core/`](core/) | `core/` modules |
| [`ops/`](ops/) | rail / daemon / tearsheet |
| [`lab/`](lab/) | research primitives (also many root `test_*.py`) |
| [`governance/`](governance/) · [`scripts/`](scripts/) | gate / discipline scripts |
| [`fixtures/`](fixtures/) | committed fixtures (vendor CSVs skip-if-missing) |

```text
make test
make test-ops
```
