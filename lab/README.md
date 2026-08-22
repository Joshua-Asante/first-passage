# `lab/` — research (free-churn)

Imports `core` + root-resident governance. **Open [`CATALOG.md`](CATALOG.md)
first** — do not glob `analysis/` to infer what is live.

| Path | Job |
|---|---|
| [`CATALOG.md`](CATALOG.md) | Generated registry (hot / HOLD / archived) |
| [`analysis/`](analysis/) | Hot campaign bodies (`<theme>/<slug>/`) + flat `CARD.md` stubs |
| [`archive/`](archive/) | Cold bodies for archived slugs |
| [`research_utils/`](research_utils/) | Stable primitives (DSR, Step-0, universe gate, …) |
| [`discovery/`](discovery/) | Gen-2 K-ledger + Stage-2/4 runner |
| [`databento_fetch/`](databento_fetch/) | Cost-gated Databento client |
| [`tools/`](tools/) | Research CLIs (e.g. econ export) |

What is turning: [`PIPELINES.md`](../PIPELINES.md) P1. Layer contract:
[`REPO_MAP.md`](../REPO_MAP.md).
