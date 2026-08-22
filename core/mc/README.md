# `core/mc/` — Monte Carlo engine

Vendor-free engine regression:
[`tests/core/test_mc_synthetic_engine.py`](../../tests/core/test_mc_synthetic_engine.py).
Historical MC-anchor record (not a live claim):
[`docs/mc_anchor_history.md`](../../docs/mc_anchor_history.md).

| Module | Job |
|---|---|
| [`simulation.py`](simulation.py) | Path simulation |
| [`ingest.py`](ingest.py) | Trade-list ingest |
| [`modes.py`](modes.py) | Broker panels (`PANELS_BY_BROKER`) |
| [`preflight.py`](preflight.py) | Firm-rule preflight |

Portfolio wrapper: [`../portfolio_mc.py`](../portfolio_mc.py).
Pipeline status: [`PIPELINES.md`](../../PIPELINES.md) P3.
