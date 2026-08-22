# `lab/discovery/` — Gen-2 K-ledger + Stage-2/4 runner

| Module | Job |
|---|---|
| `register_search.py` | `open` / `close` → [`discovery_manifests/`](../../discovery_manifests/) |
| `stage24_runner.py` | Generic Stage-2/4 runner |

`open` binds K **before** any p-value. Verdict is always a hand-off to the
gate, never a promotion. See [`PIPELINES.md`](../../PIPELINES.md) P1.
