**Theme:** c1

# Firm feasibility atlas — design (frozen before any run)

**Status:** FROZEN 2026-11-04, committed before the harness ran. Nothing below is tuned after results.
**Authority:** Joshua, 2026-11-04 ("yes to all four, spawn the sessions"), commissioning the atlas.
**Question:** for a candidate's shape priors, what are pass, bust and time-to-pass at each tier in
`core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS`? **Decision it changes:** builder round step T3
(barrier feasibility, `TEMPLATE-builder-round.md` §A3, PR #1051) becomes a lookup; it also
informs D10 (generation note §10.2). **K = 0:** synthetic streams only; no vendor data, private
input or strategy result is read.
**Budget (Rule 2):** ≤12 iterations including ≤3 Codex review rounds; $0 (this container); K = 0.

## Prior art (Rule 8)

The A2 map (`../shape_feasibility_map_2026-08/`) covered Select, MFFU and Growth only, used
dollar risk levels, and drew one fixed 520-week panel per tuple; its 2026-08-24 intercept showed
that panel draw dominates near-gate cells. This atlas extends it to every listed tier, scales
risk to each tier's drawdown allowance, adds expectancy and time-to-pass, and **draws fresh trades
for every path** (no fixed panel), so its standard errors are the whole sampling error.

## Generative process (per path, in R; 1R = one full stop)

- Trades per session `N ~ Poisson(λ)`; `N = 0` is a zero-trade day (share `e^-λ`).
- Each trade wins with probability `p` and pays `+b R`, else loses `−1 R`, with
  `b = (E + 1 − p) / p`, so per-trade expectancy is exactly `E`. `E` is **net of costs**.
- Adverse excursion: a loser reaches its stop (`MAE = 1R`, no gap-through); a winner first
  dips `u ~ Uniform(lo, hi)` R. Within a day trades run in sequence; the day's intraday low is
  `min(0, min_i(cum_before_i − MAE_i))`, passed to the engine as `intraday_low`.
- Every trade opens and closes inside one session, so nothing is held past any firm's flatten
  clock or over a weekend. Dollars: `R$ = f × (max_dd_pct × starting_balance)`.

## Grid (coverage, not selection: 5 × 4 × 3 × 3 × 3 = 540 shapes)

| Axis | Values |
|---|---|
| `f`, risk per trade / drawdown allowance | 0.05, 0.10, 0.15, 0.25, 0.33 |
| `E`, expectancy (R, net) | 0.00, 0.05, 0.10, 0.20 |
| `p`, win rate (payoff `b` derived) | 0.35, 0.50, 0.65 |
| `λ`, mean trades per session | 0.25, 1, 3 |
| MAE profile of winners `(lo, hi)` | tight (0.0, 0.3), mid (0.2, 0.6), deep (0.5, 0.95) |

## Engine and configs

- `core.mc.simulation.simulate_path`, unmodified, one call per path, with
  `kwargs = core.mc.preflight.firm_kwargs(tier, inactivity_off=True, consistency=row/100)`,
  `dd_trigger=10.0`, `dd_scale=1.0` (fixed size, no protection, the gate-5h idiom).
- **Horizon 1,500 business days** (`HORIZON_CAP`, the Part A convention). Paths: **1,000 per
  cell**. Seed for shape `i` (row-major over the table above): `20261104 + i`; the same path set
  serves every config (common random numbers), so cross-firm differences are paired.
- Configs: all 15 tiers at their row's consistency, plus three labelled sensitivities —
  MFFU Rapid 50K/100K at consistency 0.30 (register A2.1), BluSky 50K/100K as a fixed-$ trail
  (`trailing_locking` with the unreachable offset, removing the F2 %-of-peak optimism).
  FXIFY runs with `allow_provisional_rules=True`. 19 configs × 540 shapes = 10,260 cells.
- Inactivity barrier **off** (repo convention; `preflight.INACTIVITY_OFF` comment). Zero-trade
  days still slow the pace and count against `min_trading_days`.

## Outputs per cell

pass, headline bust (daily + static + trailing), unresolved at horizon, standard errors;
time-to-pass p10/p50/p90 (business days, passing paths); P(pass ≤ 22 bdays ≈ 30 calendar days,
Bulenox's access window, register D14) and P(pass ≤ 63 bdays).

**Summary label** (for tables only): `FEASIBLE` when bust ≤ ceiling and pass ≥ floor, where both
numbers are parsed at runtime by `discovery.prop_survivor_scoring.load_scoring_thresholds()`
(their owner), never copied here.

## Reliability by tier (from the venue-fact register; decided before results)

| Tier | Mark | Why |
|---|---|---|
| Tradeify Select (4), Growth | HIGH | fixed-$ EOD ratchet + intraday breach is the venue rule (register I.2). Growth omits its soft DLL: bust is an upper bound on that axis. Select 25K cap conflict (T4) not modelled |
| MFFU Rapid (2) | MEDIUM | row mixes two plans (A2.1): read the 0.50 and 0.30 runs together; eval breach clock assumed intraday (conservative) |
| BluSky Premium (2) | MEDIUM | engine trails %-of-peak (F2, optimistic); the fixed-$ twin bounds it; eval lock unknown (D16) |
| FXIFY Flex 150K | PROVISIONAL | row provisional (fees, capture unverified); lock at start balance (B1) |
| Bulenox (5) | **EXCLUDED** from the lookup | venue ratchets on the intraday high including open positions; the engine ratchets on the EOD close (A1.1, severity H), so bust is a lower bound of unknown size. Tables are published as lower bounds only. 250K may not exist (A1.2) |

## Lookup contract (T3)

`atlas.lookup(tier, E, p, λ, f, mae)` brackets each axis between its grid neighbours and returns
the **worst** corner (max bust, min pass, max time) with the snapped coordinates and the tier's
mark. Off-grid values and EXCLUDED tiers are refused with a reason, never extrapolated.

## Limitations (disclosed, not fixed)

No gap-through-stop tail; two-point payoffs; no fill or slippage model (register D9, E-4); no
integer-contract or micro-cap binding; inactivity off (Tradeify T1 conflict on the preservation
trade); no funded or payout stage; flatten clocks bind only as "flat each session".

## Compute stop

Run here through the fp launcher. If projected wall time exceeds 6 hours, stop and package a VM
run instead of shrinking the grid.
