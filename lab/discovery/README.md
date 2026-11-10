# `lab/discovery/` — Gen-2 K-ledger

| Module | Job |
|---|---|
| `register_search.py` | `open` / `close` → [`discovery_manifests/`](../../discovery_manifests/) |

`open` binds K **before** any p-value. Verdict is always a hand-off to the
gate, never a promotion. See [`PIPELINES.md`](../../PIPELINES.md) P1.

_Addendum 2026-11-10: the grow0 synthetic-calibration code (`grow0_dgp.py`, `grow0_harness.py`, `grow0_limb_c.py`, `grow0_red_patch.py`, `grow0_scoring.py`) was removed by Subtract; its manifests and ledgers in `discovery_manifests/` stay. Last present at `456452c`._

_Addendum 2026-11-10: the Stage-2/4 miner (`stage24_runner.py`, `miner.py`, `matrix_emit.py`, `scorer.py`, `motif_rules.py`, `ic_similarity.py`, `frozen_rules.py`, `return_series_index.py`, `realism_mgc.py`, `paired_synthetic.py`) was removed by Subtract on Joshua's confirmation of recommendation 5; `synthetic_bars.py` stays with its own test. Last present at `c7e0d44`._
