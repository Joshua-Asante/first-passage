# Guardian→MGC transfer lane (R7) — SUBTRACT (DEAD/N-SURV)

> **SUBTRACT 2026-08-11** — cell closed `DEAD(N-SURV)` after exploratory N-SURV FAIL
> (margin-decisive). Pursuit record was RATIFIED PARK earlier the same day; Standing
> flips here because the data-block that justified PARK is now adversely resolved.
> Not a Q-TXG-1 grid-level decision (compile/election untouched).

**Class:** (b) parked lane · **Standing:** SUBTRACT
**Test applied:** N-SURV FAIL at frozen 2026-07-13 floors via `nsurv_channel.py` on the
v0.3 native MGC1! panel against `Tradeify_Select_100K` — bust **42.2%** full /
**72.4%** H1 / **16.5%** H2 vs ≤3.0% ceiling (5.5×–24× over on every partition).
**Re-entry armor:** requires **new mechanism evidence** plus an attached falsifier,
recorded through a governance channel (ADR or equivalent) — ADR §2.3 / rejected_candidates
bar. **Not** a locked-parameter retune, **not** a re-read of the AE-approximated score,
**not** firm-shopping. A genuine bar-derived `intraday_low` re-run that cleared ≤3.0% on
full + both halves would be the only instrumentation path that could challenge the
verdict; given the margin it is not an open rescue ticket.
**Aim served (if re-entered under armor):** A1
**Residuals:** `guardian_gold_futures_mgc_v0_{1,2,3}_prototype.pine` + CARDs (F1–F5
execution-mechanics port; locked v5.5 parameters byte-identical) — retained hot as
provenance under lab/strategy CATALOG convention; hash-pinned in `PORT_MANIFEST.sha256`.
N-ACT from real panels: 35.0% zero-trade weeks. Measurement + caveats recorded in the
closure (do not restate as authority here).

**N-SURV (measurement of record, exploratory grade):**

| Partition | Bust | P(pass) |
|---|---|---|
| Full (n=276 days) | 42.2% | 57.8% |
| H1 (2022-01→2024-07) | 72.4% | 27.6% |
| H2 (2024-07→2026-08) | 16.5% | 83.5% |

Caveats (named, not repaired): (1) half-boundary 2024-07-02 = unpre-registered
midpoint-by-day-count; (2) `intraday_low` from trade Adverse-Excursion, not bar-level
daily equity troughs.

**Closure:** [`2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](../briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)
**Cell PREREG (retroactive):** [`2026-08-11-guardian-mgc-transfer-cell-prereg.md`](../briefs/pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md)
**Registry:** [`rejected_candidates.md`](../rejected_candidates.md) — Guardian→MGC transfer cell

**Ratified PARK:** 2026-08-11 / JA · **SUBTRACT:** 2026-08-11 (this closure)
**Source:** [`R6 ADR`](../adr/2026-07-10-r6-nogo-futures-residual-disposition.md) §2 item 3 ·
[`07-16 ADR`](../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §2 item 1 ·
[`MGC ledger`](../../ops/instruments/MGC.md) · [`GSUB-1 inventory`](../briefs/programs/GSUB-1-inventory-and-dispositions.md) ·
[`Q-TXG-1 design`](../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) §5
