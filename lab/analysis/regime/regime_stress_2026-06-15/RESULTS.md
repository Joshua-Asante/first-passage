**Theme:** regime
**Status:** ACTIVE — regime-stress investigation chain
# Regime-stress investigation chain (2026-06-15)

Six-step OUTER/INQHIORI chain spawned from the claude.ai CC-handoff **Q-REGIME-STRESS-1**
(hostile-regime stress MC). Each step's falsifier redirected the next. **No `core/` / locked-config /
allocation / dd_protection change anywhere** — research only. The locked anchor (99.83 / 0.17 / 4.37) stands.

Operational output: a shadow gold participation gate, graduated to tracked ops tooling at
[`ops/regime_gate/`](../../../ops/regime_gate/README.md).

## The chain

| # | step | artifact | finding |
|---|---|---|---|
| 1 | Stress MC | [`Q-REGIME-STRESS-1.md`](Q-REGIME-STRESS-1.md) | **FALSIFIED-FAIRWEATHER** — the anchor is a benign-regime average; hostile (2020-22) bust **33%** / p99 **9%** vs benign 0.5%. Bust attribution flips to **Guardian 57%** (zero hostile edge, full DD). |
| 2a | Reallocation grid | [`realloc_grid.md`](realloc_grid.md) | drop-Guardian beats equal de-risk ~4× on the *compounded* hostile bucket; grid pointed at D3 (→Strikers). |
| 2b | Formal regime gate | [`realloc_gate.md`](realloc_gate.md) | **all FAIL** on the honest decompounded basis; **D3 backfires** (Striker pyramid tail un-hidden). No static reallocation is regime-robust. |
| 3 | Perfect-foresight oracle | [`oracle_test.md`](oracle_test.md) | **resizing is DEAD** — even perfect foresight needs 367–572 d median to clear the hostile half. Binding constraint = near-zero hostile **drift**, not detection. |
| 4 | Participation viability | [`participation_check.md`](participation_check.md) | participation (deploy-vs-wait) is **viable** — regimes are persistent multi-year blocks (median days-to-pass: hostile 65–219 d / benign 14–24 d). |
| 5 | Detector screen | [`detector_screen.md`](detector_screen.md) | only **gold** trend-persistence separates the regime (leg-specific); equities flat, USDJPY inverted (confirms the Aegis carry-trend insight). Weak (n=2 blocks). |
| 6 | Shadow gate | [`ops/regime_gate/README.md`](../../../ops/regime_gate/README.md) | gold-anchored deploy/wait gate, **shadow mode** (logs only), forward live-PnL tripwire pre-registered. Current call: WAIT. |

## Honest bottom line

The investigation ran to the limit of what backtesting can resolve: a gold-anchored signal *describes*
the hostile regime, but its *predictive* power can only be settled **forward** (n=2 regime blocks make
OOS validation near-powerless). The shadow gate is the terminal instrument — it costs nothing live and
accumulates the one kind of evidence that's missing. Cross-references the decompounded sibling PR #157
(`lab/analysis/decompound_remc_2026-06-07`) throughout.

## Reproduce

`.py` scripts reuse locked MC primitives (`core/portfolio_mc`) + the PR #157 decompound preprocessor;
they resolve the repo root by walking up to `CLAUDE.md`, so they run from this directory. Re-running
requires the gitignored vendor CSVs (Pepperstone panels + `core/data/bar_data/` OANDA bars + the four
2026-06-15 trade exports in `~/Downloads`). Results (`.json`) are committed; the scripts regenerate them.
