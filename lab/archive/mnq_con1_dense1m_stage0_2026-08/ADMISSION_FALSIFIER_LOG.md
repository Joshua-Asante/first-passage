# Q-MNQDTL-CON-1 — cheap falsifier log (parent-side, pre / at G0 freeze)

**Date:** 2026-08-08
**Cell:** ES−NQ 5m log-return divergence vs 20-session median-|d| → MNQ session-flat @ G=10
**K_intrinsic:** 1 · **Cost:** $0.00 (cache reuse)

## Panels

| Symbol | Cache file | Coverage (UTC) |
|---|---|---|
| `MNQ.v.0` | `~/.databento_cache/ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn` | 2019-05-06 → 2026-08-05 (MNQSEL-2) |
| `ES.v.0` | `~/.databento_cache/ohlcv-1m_continuous_17b6c454408be685.dbn` | 2019-05-06 → 2026-08-02 |

Estimate-before-pull: **not required** — both files already on disk; no new Databento pull.

## Arithmetic bars (G=10, RT=1.41)

| Bar | Value | Derivation |
|---|---|---|
| EM1 pred move (0.40R disclosure) | **5.41 pt** | `0.40×10 + 1.41` |
| N-EDGE pred move (net R > 0) | **1.41 pt** | RT |
| EM1 WR (±G binary) | **0.7705** | `(1 + 0.40 + 1.41/10) / 2` |
| N-EDGE WR (±G binary) | **0.5705** | `(1 + 1.41/10) / 2` |

## Prior-art / sign / entry

| Check | Result |
|---|---|
| Prior-art effect for this exact cell | **None measured** → bar/2 rule idle (not `FALSIFIED-BY-ARITHMETIC`) |
| ENTRY named causal at bar open | **YES** — relative contrarian ES−NQ divergence |
| Sign invert | **Forbidden** — would become own-instrument momentum (C5 / D5-RECOST-1) |

## Harness recompute

```bash
python lab/archive/mnq_con1_dense1m_stage0_2026-08/run_construct_g0.py
pytest lab/archive/mnq_con1_dense1m_stage0_2026-08/test_construct_lib.py -q
```

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold.
**Explore:** **blocked** — Stage-0 / explore GO unpaid; path-PnL scorer is wired but
refuses real-panel scoring until `EXPLORE_GO.md` + `--explore-go`.
