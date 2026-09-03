# ORB-MYM v0.4 opening-range volume gate — operator TradingView read, 2026-09-02

**In-flight:** yes
**Status:** `SOURCE-STAGE EXPLORATORY — P50 SELECTED FOR FORWARD TEST, NOT CONFIRMED`
**Instrument:** MYM, TradingView chart/Strategy Tester
**Source:** private Downloads-local `orb_mym_4_edition.pine`
**Pine SHA-256:** `9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071`

> **Cultivation routing, 2026-09-03:** exact P50 is **retired as the lead**, not a live Seat A
> workstream. The spent A0 search stays charged on Seat A (1/8 STOPPED). The Sep 2 campaign was
> rebound to VOLREGIME translation and closed at T0 as `PRE-CONTRACT DROP`
> ([`addendum 2026-09-03b`](../../../../docs/adr/2026-09-02-portable-edge-cultivation-campaign-objective.md#addendum-2026-09-03b--t0-pre-contract-drop)).
> This result remains source/development evidence only: Off/P50/P80 was viewed before any
> contract/K freeze, so no campaign may open a candidate contract around exact P50 retroactively.
> It is a different observable from Q-VOLREGIME `bias_volume`.

> ## ⚠ Reader-intercept 2026-09-03 — the P50 row below is a TradingView read, and the canonical engine disagrees with it
>
> **The numbers in the table below are real and reproduce; they are not a survival verdict.**
> The operator's List-of-Trades CSV behind the P50 cell was later put through the repo's canonical
> bust engine at **the size the $31,947.96 headline was measured at (qty 2)**:
> **Select 51.2% bust / 48.8% pass**, and the realized historical path **busts Select on day 42**.
> Exit-only net reconciles **to the cent** (986 rows / $31,947.96) — raw P&L is not what fails;
> survival at size is.
>
> ⚠ **Corrected 2026-09-03** (Codex round 4): this banner first read "maxDD 2.83% against the 3.0%
> trail", which is internally contradictory — those are two different quantities. **2.83% is the
> engine's `max_dd`: end-of-day equity, as a fraction of the running peak** — `core/mc/simulation.py`
> fixes both deliberately and says so in its own docstring. The barrier is a fixed **$3,000 below
> the EOD peak, tested against the day's intraday low** (`equity_test`, supplied by this run via
> `intraday_low=`). So 2.83% is not the number the barrier reads, and its being under 3.0% is no
> contradiction. An EOD-only breach would have required a peak ≥ **$106,007** — above the account's
> own **$106,000** profit target — so the intraday excursion is the likely trigger; confirming that
> needs the operator-local trade CSV, which is not in this tree.
> Owner of that measurement:
> [`orb_mym_v04_riskbudget_2026-09-02/RESULTS.md`](../orb_mym_v04_riskbudget_2026-09-02/RESULTS.md) §2.
>
> **Which number is authoritative:** the canonical engine. TradingView net / PF / max-drawdown are
> **leg-level under pyramiding** and carry no firm DD geometry, so they cannot express a prop-tier
> bust. This is the **third** time this construct family has shown good raw TV metrics against a bad
> canonical bust rate (v0.3 62–74% bust, [`ops/instruments/MYM.md`](../../../../ops/instruments/MYM.md)
> M9; §1 Hot-only; now P50 at its own reported size). Body below is unedited — the `SOURCE-STAGE
> EXPLORATORY … NOT CONFIRMED` status above was always correct; this banner only puts the
> disagreement upstream of the table instead of one directory away
> ([`operational_rules.md`](../../../../docs/operational_rules.md) §14).

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
