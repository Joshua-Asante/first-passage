# ORB-MYM v0.4 opening-range volume gate — operator TradingView read, 2026-09-02

**Status:** `SOURCE-STAGE EXPLORATORY — P50 SELECTED FOR FORWARD TEST, NOT CONFIRMED`
**Instrument:** MYM, TradingView chart/Strategy Tester
**Source:** private Downloads-local `orb_mym_4_edition.pine`
**Pine SHA-256:** `9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071`

> **Cultivation routing, 2026-09-02:** assigned seat A in the operator-authorized
> [`portable-edge cultivation campaign`](../../../../docs/superpowers/plans/2026-09-02-portable-edge-cultivation-campaign.md).
> Exact P50 is source/development evidence only: its Off/P50/P80 selection preceded any contract/K
> freeze, so this campaign cannot open a candidate contract around it retroactively. Source/config
> and List-of-Trades capture remain owed for provenance; this routing does not promote the result.

## Question and tested catalogue

Does a causal completed-opening-range volume gate improve the existing ORB-MYM v0.4 source
construct? Three settings were read manually in TradingView with the operator reporting that the
volume-gate setting was the only change:

1. `Off` — no opening-range volume gate;
2. `P50` — completed opening-range volume at or above the median of the prior 60 completed opening
   ranges;
3. `P80` — completed opening-range volume at or above the 80th percentile of the same prior-60
   history.

The implementation classifies today's completed opening-range volume before appending it to the
history array. Warm-up blocking is enabled when a gate is active. `Off` is the identity/control.

This is an **opening-range aggregate-volume conditioner**, not the exact `Q-VOLREGIME-1` M15
trigger-bar conditioner. It uses the same causal prior-history principle but tests a distinct
expression attached to this Pine strategy.

## Operator-reported Strategy Tester results

| Gate | Net P&L | Profit factor | Max drawdown | Profitable closed legs | Closed legs | Net / closed leg |
|---|---:|---:|---:|---:|---:|---:|
| Off | $26,330.76 | 1.198 | $9,634.98 | 55.31% | 1,891 | $13.92 |
| P50 | **$31,947.96** | **1.451** | **$4,621.18** | **57.91%** | 986 | **$32.40** |
| P80 | $9,524.48 | 1.248 | $5,016.00 | 55.08% | 443 | $21.50 |

### Contrasts

- **P50 vs Off:** +$5,617.20 net (+21.3%), PF +0.253, max drawdown -$5,013.80
  (-52.0%), 905 fewer closed legs (-47.9%), profitable-leg rate +2.60pp, and net/closed-leg
  +132.7%.
- **P80 vs P50:** -$22,423.48 net (-70.2%), PF -0.203, max drawdown +$394.82 (+8.5%),
  543 fewer closed legs (-55.1%), and profitable-leg rate -2.83pp.
- Because the P80 set is nested inside P50 under the same causal lookback, the approximate P50–P80
  middle-volume cohort accounts for 543 closed legs and $22,423.48 of net P&L. That arithmetic is
  descriptive only; gross-profit/loss components and day aggregation are absent.

## Disposition

**P50 is the selected exploratory source setting.** It dominates both Off and P80 on net P&L,
profit factor, maximum drawdown, and net per closed leg on the displayed panel. P80 shows that the
relationship is not monotonic: restricting participation to the extreme-volume tail removes most
of the apparent value and slightly worsens drawdown versus P50.

Stop percentile testing here. Do not add P55/P60/P65/etc. on this fully viewed panel. The next
admissible use of P50 is a frozen forward/paper test on genuinely new data, with the Pine hash and
full Strategy Properties retained before the read.

## Evidence limitations

- These are manual screenshot reads, not retained TradingView List-of-Trades exports. Net P&L,
  profit factor, and drawdown are readable; trade-level reconciliation and independent day-level
  aggregation are not available.
- TradingView counts pyramided legs as closed trades. The displayed profitable-trade rate is
  therefore leg-level and is not the construct's day-level win rate.
- The screenshot header displays `Dec 31, 1799 — Sep 1, 2026`; the plotted/traded curve begins in
  2020, consistent with the Pine's default entry-date gate. Exact first/last fill timestamps require
  the missing trade exports.
- The operator reported only the volume-gate setting changed across the three reads, but complete
  Strategy Properties screenshots were not retained, so configuration identity is not independently
  proven.
- The history is fully viewed and the source lineage already carries substantial informal K. This
  comparison establishes an economic prior and selects a paper-test default; it is not Confirm
  evidence, lifecycle promotion, or authorization for live capital.
- Current private Pine defaults include Monday/Thursday/Friday enabled and Tuesday/Wednesday
  disabled. Unless the operator's chart properties overrode them, the result is scoped to that
  weekday-filtered expression.

## Local evidence identities

The screenshots remain local-only and are not committed. Their SHA-256 identities are:

| Setting | Local screenshot SHA-256 |
|---|---|
| P50 | `8662625e915900d39e5b33acb2a937962879add17f89b34da7c0181b7e76d991` |
| Off | `9fe80c3cabb4cf0fb727bdbbd5eb5b69fcc4869875e4e5bfc5b8e3b791d50f4` |
| P80 | `5461713b89c82012dae220ef87b0a6812248397ded392fc5413aa348b7338169` |

## Reproduction requirements for the next read

Retain, before opening the result: the private Pine body and SHA-256, symbol/timeframe, full
Strategy Properties, date window, weekday toggles, quantity/cost/slippage settings, and the
complete List-of-Trades export. Aggregate base/add legs by position/day before reporting win rate,
mean win/loss, yearly stability, or forward verdict.
