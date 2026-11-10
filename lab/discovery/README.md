# `lab/discovery/` — Gen-2 K-ledger + Stage-2/4 runner

| Module | Job |
|---|---|
| `register_search.py` | `open` / `close` → [`discovery_manifests/`](../../discovery_manifests/) |
| `stage24_runner.py` | Generic Stage-2/4 runner |

`open` binds K **before** any p-value. Verdict is always a hand-off to the
gate, never a promotion. See [`PIPELINES.md`](../../PIPELINES.md) P1.

_Addendum 2026-11-10: the grow0 synthetic-calibration code (`grow0_dgp.py`, `grow0_harness.py`, `grow0_limb_c.py`, `grow0_red_patch.py`, `grow0_scoring.py`) was removed by Subtract; its manifests and ledgers in `discovery_manifests/` stay. Last present at `456452c`._
