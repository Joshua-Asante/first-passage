# MNQ/MYM mechanism diagnostic — TradingView handoff

`mnq_mym_mechanism_diagnostic_v0_1.pine` is a **non-trading Pine v6
indicator** for the next-session parity test. It intentionally contains no
`strategy.*` calls.

## What it measures

- The completed 18:00–09:30 America/New_York overnight high-low range and its
  strictly-prior 60-session P80 reference.
- The unsigned RTH-open gap against the previous RTH close.
- The developing 09:30–16:00 RTH range and its strictly-prior session median.
- On a 15-minute chart, volume and high-low range relative to the prior 60
  observations from the same time-of-day slot.
- Next-bar elevated-range rates for the 2x2 trigger-bar state table
  (`range_hot` x `volume_hot`).

The defaults follow the live research scripts (`60`, not the older prose-only
`20` value). Every threshold excludes the observation it classifies. Volume
and range states finalize only on a confirmed bar; their outcome is evaluated
on the following confirmed bar.

## Next-session checklist

1. Paste the script into TradingView and select Pine v6.
2. Load `CME_MINI:MNQ1!` and `CBOT_MINI:MYM1!` on separate 15-minute charts.
3. Leave the chart timezone unrestricted; the script performs its clocks in
   `America/New_York` explicitly.
4. Confirm the table says `M15 ready` and allow at least 60 observations per
   time slot to warm up.
5. Compare a frozen sample of dates against the Python research outputs before
   interpreting the table rates.
6. Record TradingView symbol, chart interval, loaded date span, script inputs,
   and screenshots/exports with the comparison.

## Known parity boundary

The indicator implements the intended **pre-RTH** overnight window
(18:00–09:30 ET). The Python helper currently describes that window but selects
all non-RTH bars assigned to a trading day; a parity review must determine
whether post-RTH 16:00–17:00 bars entered the historical overnight aggregate.
Do not change this indicator to reproduce that behavior without an explicit
methodology ruling.

This artifact is an Inquire-phase measurement harness. It does not certify the
conditioners, provide direction, define a tradeable candidate, or authorize
entry, sizing, or parameter optimization.

## Q-VOLREGIME-1 focused harness (v0.2)

`mnq_mym_volume_regime_diagnostic_v0_2.pine` is the preferred TradingView
harness for the current volume-regime loop. Unlike the broader v0.1 mechanism
dashboard, it reproduces the frozen instrument-specific presence definitions:

- MNQ uses 60 strictly-prior same-slot observations and classifies volume with
  `>=` the median.
- MYM uses 20 strictly-prior same-slot observations and classifies volume with
  `>` the median.
- Both instruments classify range with `>` the median, and score the next bar
  against the next bar's own same-slot threshold.

Use separate 15-minute `MNQ1!` and `MYM1!` charts. Leave **Instrument
semantics** on `Auto` only when TradingView's ticker contains `MNQ` or `MYM`;
otherwise select the instrument explicitly. The table reports the same 2x2
presence diagnostic used by L1-L4 and provides confirmed-bar alerts suitable
for prospective observation.

The v0.2 script deliberately does **not** reproduce Packet B's L5 nested
logistic comparison, null generation, calibration, or verdict. Those require
the hash-pinned panels and full replicate-level re-estimation outside
TradingView. The indicator can check feed parity and collect prospective
examples, but cannot certify attribution or serve as a strategy.

### Expected outcomes and interpretation

The hash-pinned Python panels provide a **parity reference, not Pine pass
bands**. Across 2020–2026 they produced these pooled next-bar elevated-range
rates:

| Instrument | Trigger-bar range | Low-volume rate | Elevated-volume rate | Lift |
|---|---|---:|---:|---:|
| MNQ | low | 26.46% | 48.80% | +22.34pp |
| MNQ | high | 46.79% | 74.18% | +27.39pp |
| MYM | low | 28.79% | 45.28% | +16.49pp |
| MYM | high | 46.95% | 71.50% | +24.55pp |

Testing the TradingView diagnostic can produce several legitimate outcomes:

1. **Close replication:** both lifts are positive and broadly similar to the
   reference. This supports implementation/feed parity and prospective
   persistence, but does not add an independent L5 attribution result.
2. **Positive but attenuated:** both lifts remain positive but are materially
   smaller. Record symbol, contract construction, loaded span, and counts;
   this can reflect feed or sample differences and is not automatically a
   falsification.
3. **Mixed strata:** one lift is positive and the other is near zero or
   negative. Treat this as a failed Pine/feed replication until date-level
   parity checks distinguish an implementation difference from a genuine
   sample result. Never rescue it with the pooled rate.
4. **Null or reversed:** both lifts are near zero or negative. This is strong
   evidence that the effect does not reproduce on the loaded TradingView
   panel, but it does not retroactively invalidate the hash-pinned result.
5. **Insufficient or malformed:** the table remains warming, reports very low
   cell counts, or instrument/timeframe readiness fails. This is no empirical
   result; restore M15 history or correct the instrument mode first.

Do not infer direction or profitability from any row. The measured outcome is
only whether the next bar's range exceeds its own causal same-slot median.
Before interpreting differences, compare a frozen set of bar timestamps,
medians, trigger states, and next-bar outcomes between Pine and Python. Do not
introduce post-result thresholds or tune the lookback to make the table match.
