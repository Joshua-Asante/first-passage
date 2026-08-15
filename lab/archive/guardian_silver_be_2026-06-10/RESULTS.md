# Guardian Silver v1.0 — beTriggerAtr=4.8 vs no-BE baseline (TV/Pepperstone)

**Date:** 2026-06-10
**Brief:** [`docs/ltm/briefs/2026-06-10-cc-handoff-guardian-silver-be-validation.md`](../../docs/ltm/briefs/2026-06-10-cc-handoff-guardian-silver-be-validation.md)
**Script:** [`be_validation.py`](be_validation.py) (run: `python lab/analysis/guardian_silver_be_2026-06-10/be_validation.py`)

## Verdict: `DONE_WITH_CONCERNS`

**The parent-session "+50.7% RF improvement" claim inverts against the true no-BE
baseline.** The 4.8 export reproduces the parent sweep table exactly (all four
claimed values match to the cent). The freshly-exported no-BE baseline does **not**
match the parent table's baseline row on any metric — and measured against it,
beTriggerAtr=4.8 is **RF-negative on the full panel and in H1**, the half it was
claimed to repair. Only H2 is marginally positive, and that edge nearly vanishes
on the static-$200K basis the challenge actually trades on.

| RF ratio, 4.8 / baseline | raw (compounded TV $) | static $200K (decompounded) |
|---|---|---|
| Full panel | **0.81× (−19.0%)** | **0.89× (−10.7%)** |
| H1 2022–2023 | **0.64× (−35.7%)** | **0.71× (−29.3%)** |
| H2 2024–2026 | 1.11× (+11.3%) | 1.01× (+1.2%) |

## Inputs (manifest-pinned, gitignored)

| File | sha256 (first 8) | Config | N |
|---|---|---|---|
| `Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_d87c2.csv` | `b5e5d22a` | baseline, BE off | 226 |
| `Guardian_Silver_v1.0_PEPPERSTONE_XAGUSD_2026-06-10_7c8c2_be4.8.csv` | `7c8c2bdb` | beTriggerAtr=4.8, BE on | 239 |

Both pinned in [`core/data/tv_exports/pepperstone/SHA256SUMS`](../../core/data/tv_exports/pepperstone/SHA256SUMS).
The be4.8 file arrived as `4.8.csv`; renamed to convention (suffix = first 5 of
content sha256, config tag per the `_ddcap*` precedent). Both files: TV 2026-06
export column format (`Trade number` / `Net PnL USD`); the analysis script
normalizes to the canonical `reconcile.py` columns before processing.

## Headline metrics

Raw = TV compounded dollars as exported. Static = decompounded to a fixed $200K
base (`pnl × 200,000 / equity_before_trade`; trades verified non-overlapping, so
the equity divisor is exact). DD reconstruction from $200K initial; RF = Net / maxDD$.
1R = median loss (Guardian-family pinning). Cross-checked against canonical
`reconcile.py --strategy guardian` (exact agreement on N/PF/WR/Net/DD/RF).

| Config / segment | N | WR | PF | Net | maxDD$ (%) | RF | max consec. losses |
|---|---|---|---|---|---|---|---|
| baseline full raw | 226 | 15.93% | 2.875 | $271,663.79 | $10,979 (2.38%) | **24.74** | 19 |
| baseline full static | 226 | 15.93% | 2.729 | $177,484.45 | $10,105 (4.74%) | **17.56** | 19 |
| baseline H1 raw | 96 | 12.50% | 1.857 | $42,273.40 | $10,516 (4.93%) | 4.02 | 19 |
| baseline H2 raw | 130 | 18.46% | 3.401 | $229,390.39 | $10,979 (2.62%) | 20.89 | 9 |
| be4.8 full raw | 239 | 23.01% | 2.864 | $231,298.69 | $11,540 (4.95%) | **20.04** | 18 |
| be4.8 full static | 239 | 23.01% | 2.722 | $159,030.35 | $10,138 (4.37%) | **15.69** | 18 |
| be4.8 H1 raw | 102 | 15.69% | 1.574 | $25,191.48 | $9,742 (4.38%) | 2.59 | 18 |
| be4.8 H2 raw | 137 | 28.47% | 3.570 | $206,107.21 | $8,866 (2.40%) | 23.25 | 9 |

(Static H1/H2 in the script output; H2 static RF baseline 28.62 vs be4.8 28.96.)

## Critical trade (Aug 2023 runner)

Identical entry in both files: 2023-08-17 19:30 @ 22.656 → exit 2023-08-23 13:45
@ 24.127.

| Config | P&L |
|---|---|
| baseline (no BE) | **+$10,861.72** — held the runner; nothing to scratch it |
| be4.8 | +$10,734.92 — 3R trigger left room, runner held |

The brief's §1 claim that "baseline exited next day at −$35 (BE at 1.5R triggered
by brief dip)" **cannot describe a no-BE config and is contradicted by this
export**. A no-BE trend-rider has no BE to trigger; this baseline held the trade.

## Divergence classification (mechanical, not signal)

Same strategy, BE-only delta — not a version/feed difference:

* 219 entry timestamps common to both files; entry prices **100% identical** on
  the common set.
* Scratch signature: baseline has **0** exits with |pnl%| ≤ 0.20%; be4.8 has
  **37** at ≤ 0.05% (the BE stop-outs) — matching the BE-on/BE-off semantics.
* be4.8's 20 extra entries cluster in 2023 (10 of 20): BE scratches free the
  strategy to re-enter — consistent with the parent's "20 scratches, 16/24 H1
  months" observation.

## Parent-table reconciliation

| Row | Parent claim | This export | Status |
|---|---|---|---|
| 4.8: N / RF / H1 RF / H2 RF | 239 / 20.04 / 2.59 / 23.25 | 239 / 20.04 / 2.59 / 23.25 | **exact reproduction** |
| baseline: N / RF / H1 RF / H2 RF | 271 / 13.30 / 0.69 / 17.20 | 226 / 24.74 / 4.02 / 20.89 | **no metric matches** |

Working hypothesis for the parent baseline row: it was run with **BE armed**
(plausibly the default trigger ≈ 1.5R) — its own critical-trade narrative says
the "baseline" exited via "BE at 1.5R", and its N=271 ≈ the 2.4-config's N=271.
If so, the sweep measured *BE-trigger placement* (4.8 vs ~1.5R defaults), not
*BE vs no-BE*: "4.8 beats a badly-placed BE" is supported; "BE at 4.8 beats no
BE" is **falsified by this data** (full-panel and H1), with only a marginal H2
edge that shrinks to +1.2% static.

This is the [[on-disk-artefact-can-be-wrong]] / re-fetch-as-hypothesis shape:
the contradiction routes back to the parent session for a re-check of the
original baseline run's `beMode` / `beTriggerAtr` inputs — **not** self-resolved
here.

## Scope notes

* Dukascopy leg of the original brief: **dropped by operator decision**
  (2026-06-10) — all runs TradingView-side. Feed-divergence steps (§2.1/§2.5)
  void.
* Rejected-candidates collision (Guardian-family on XAGUSD, closed 2026-05-14):
  **explicit operator override** for this validation work — see the brief
  amendment. The registry entry itself stands; the concept-intake bar
  (new mechanism evidence) is untouched for any portfolio-admission move.
* `baselines.md` not updated (brief §5 forbidden move 3 — parent-session call).
* No lock decision is taken or implied here (§5 forbidden move 5); on current
  evidence the BE-on-vs-off question would need the parent baseline re-run
  before any lock brief cites an improvement number.

## Addendum (same day) — portfolio-level probe: the BE question is nearly portfolio-invariant

[`portfolio_mc_silver_probe.py`](portfolio_mc_silver_probe.py) (exploratory,
zero-fork via `_load_all` `panels_override` + `fixed_1r_reference`; anchor
reproduced 99.83/0.17/4.37/26 before any 5-leg read) adds Silver as a 5th leg
on the canonical compounded 2022-26 Pepperstone panel, both configs:

| config | pass % | bust % | p99 DD % | median d |
|---|---:|---:|---:|---:|
| anchor (4-strategy) | 99.83 | 0.17 | 4.37 | 26 |
| + Silver no-BE @ 0.15% | 99.89 | 0.11 | 4.32 | 21 |
| + Silver be4.8 @ 0.15% | 99.90 | 0.10 | 4.32 | 22 |
| + Silver no-BE @ 0.34% | 99.57 | 0.43 | 4.85 | 18 |
| + Silver be4.8 @ 0.34% | 99.58 | 0.42 | 4.84 | 19 |

At the portfolio level the two configs are statistically indistinguishable on
this panel — the BE-on/off dispute (above) matters for the strategy's own merit
narrative and admission argument, not for portfolio tail shape at ≤0.34%. The
be4.8 cells independently reproduce the sibling analysis
[`lab/analysis/silver_regime_2026-06-10/`](lab/analysis/silver_regime_2026-06-10/RESULTS.md)
(salvaged onto this branch 2026-06-11) to the third
decimal; that analysis's decompounded 2020-26 regime gate — Silver raises the
hard-regime H1 2020-23 bust 24.5% → 29.8% (0.15%) → 32.1% (0.20%) — is the
load-bearing deployability constraint, not these compounded-panel numbers.
