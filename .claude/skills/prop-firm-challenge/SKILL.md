---
name: prop-firm-challenge
description: Use this skill for firm/venue rules and portfolio Monte Carlo — the four-firm configs in core/firm_rules.py, the historical FXIFY fixture, trailing-DD/eval/consistency/inactivity rules, dd_protection mechanics, integer-contract sizing (MNQ/MYM/MGC), firm onboarding pre-flight, re-MC triggers, and portfolio_mc methodology. Triggers on firm-tier questions, drawdown/bust semantics, MC runs, or sizing math. Live execution, arming and order questions route to `c1-rail`; current eval and rail posture is owned by AGENTS.md §Live-execution posture; broker CSV parsing goes to `trade-csv-reconcile`; strategy code to `pinescript-v6`. Narrowed 2026-10-24 to firm rules and MC: legacy-book execution rules were retired.
---

# Prop Firm / Portfolio Operations

Durable mechanics (firm rules, sizing, protection, MC) for the LOCKED legacy book (`core/firm_rules.py`) and any future firm re-open (R6 ADR §4); not a claim that a challenge is running. The Tradeify book's owners: [campaign record](../../../docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md), [venue edition](../../../ops/venue_editions/Tradeify_Select_100K.md).

**The repo is canonical; when this skill disagrees, trust the owner:** Pine for strategy code; `core/firm_rules.py`, `core/dd_protection.py`, `core/lifecycle.py` for sizing and risk constants; `core/strategies/CATALOG.md` → `core/strategies/_archive/<family>/LOCK.md` for locks; `docs/adr/` for decisions.

## Posture and routing

Rail and eval posture: [`AGENTS.md`](../../../AGENTS.md) money controls and [`STATE.md`](../../../STATE.md).

- Live tier key: explicit `Tradeify_Select_100K`; no `ACTIVE_FIRM` switch.
- Eval geometry (no drawdown lock in eval for Tradeify/MFFU): [§4 withdrawal ADR](../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
- Cap allocation, flat deadline, hedging Product-Group, WATCH-1 / B7 inputs: [GO ADR](../../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) Addendum 2026-07-22; per-leg shares in `ops/c1_rail` constants; RESULTS under `lab/analysis/c1/`.
- ⚠ Bust/DD figures are **EOD-clock lower bounds** pending the [W1 ADR](../../../docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md).
- Self-funded lane [closed 2026-10-29](../../../docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md); manual CFD and FXIFY closed. FXIFY rules and the historical pin's `HISTORICAL_CHALLENGE_FIRM_KWARGS` live in [`core/historical_challenge.py`](../../../core/historical_challenge.py), not `FIRM_RULES` ([substrate ADR](../../../docs/adr/2026-07-22-challenge-era-substrate-retirement.md) §2-E).
- Arming, fills, disarm: `c1-rail`, [`ARMING_PROCEDURE.md`](../../../docs/notes/rail_build/ARMING_PROCEDURE.md). Live sizing: `BASE_RISK × DD_SCALE × lifecycle`, integer-qty floored in `ops/c1_rail/c1_sizing_host_reference.py`.
- Broker CSV work: `trade-csv-reconcile`, kept separate from MC (live P&L looks back on broker exports; MC looks forward on TV backtest CSVs).

## Audit-first

Before any decision brief touching risk controls (dd_protection, lot sizing, account rules, protection tiers), read the production code, not memory, prior docs or reconstructed specs.

- **Suspect single-rule descriptions of multi-rule systems:** look for the second rule.
- **Labels and paths are not data provenance.** Reconcile a CSV's trade count and headline metrics against the Pine-header backtest before accepting MC output, whatever its path says (2026-04-23 Aegis mislabel).

## Firms and challenge rules

[`core/firm_rules.py`](../../../core/firm_rules.py) `FIRM_RULES` is canonical for every live tier: read it for values. `dd_type` is `"static"` (from starting balance, never moves) or `"trailing"` (ratchets with equity, real-time or EOD by venue); `max_dd_pct` is against that basis; `daily_loss_pct: None` means no daily-loss rule, so trailing DD is the only bust mode; `weekend_holds: False` marks force-flat venues; `inactivity_max_idle_days` is no-progress days before flag/fail.

`AUTOMATION_FRIENDLY_PROP_FIRMS` lists target firms; status: [four-firm ADR](../../../docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md). The [R6 NO-GO](../../../docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md) bars only redeploying the locked legacy book.

**Onboarding a firm:** add it to `FIRM_RULES`, run an engine-support pre-flight (`daily_loss_pct: None` firms often need bespoke bust branches). If the execution feed differs from the MC's calibration feed, run `docs/spec/feed_equivalence_discovery_test_LOCKED.md` before re-MC against that tier key.

## Allocations and protection

Locked allocations: `core/firm_rules.py`. Sizing authority: `_BASE_RISK` (`core/firm_rules.py`), `BASE_RISK` (`core/dd_protection.py`). No re-sizing at pass. Per-strategy mechanics: [`references/strategy_reference.md`](references/strategy_reference.md).

Single-tier internal drawdown overlay: [`core/dd_protection.py`](../../../core/dd_protection.py), [concept-not-constant](../../../docs/adr/2026-07-13-dd-protection-concept-not-constant.md).

**It sits on top of, not instead of, the firm's own DD rule.** MC must thread the firm's `dd_type` through (`bust_trailing` vs `bust_static`/`bust_daily`).

### Re-MC triggers

- 6 months of live data accumulated
- Any strategy version bump: re-MC before locking
- Any allocation change beyond the documented Guardian safe band (needs Joshua's approval; AGENTS.md money control 4)
- Any `dd_protection` constant change
- Any firm/venue switch (new explicit tier key) or new firm onboarded

### A second protection tier

⚠ The equity tier's revert triggers are **LOST**: a new tier needs fresh pre-registration. Unratified prompts to *start* one: (1) bust above the live bar at a mix change; (2) a tail DD-protection cannot catch (slow bleed, peak tracking equity down); (3) a high-risk leg above its locked band, or a correlated fourth strategy. MC-validate any new tier against **live code semantics**.

## Futures sizing

CFD lot sizing is retired. DXTrade/TradingView `contractValue` defaults to 1 when unset; set it explicitly on CFD exports.

- Size = `floor(target_risk_$ / (stop_distance × tick_value))`, capped by `micro_contract_cap`: an integer count.
- **Granularity floor:** the balance below which intended risk rounds to 0 contracts. Guardian (single-position) tolerates it; in pyramided Striker DJ30/NAS100 a leg rounding to 0 breaks the edge. Derive floors first: `lab/analysis/legacy/futures_conversion_2026-07-01/derive_floors.py`.
- **RESERVE cap:** base size ≤ `floor(account_cap / (1 + pyramid_pct))`, keeping pyramid headroom. `account_cap` is **this leg's share** when legs share an account-aggregate cap (Tradeify); the whole cap per leg over-counts. A missing per-leg allocation must **HALT**, never fall back to the account cap.
- Re-derive tick value and commission per instrument from the venue's contract specs; never reuse CFD numbers.

## Futures-venue mechanics

- **Real-time vs EOD trailing** are different risk profiles. `bust_trailing` models %-of-peak, EOD: confirm the firm's semantic before trusting a re-MC bust rate.
- **Force-flat.** Venues typically flatten before session close, no overnight or weekend carry; multi-day holds (Guardian) do not fit as-is ([ADR](../../../docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md)).
- **Consistency and inactivity.** Most firms cap profit concentration (typically since-inception-cumulative on funded accounts, not per payout window) and require a cadence; read the tier's terms. Published MC figures assume the inactivity barrier OFF ([`load_bearing_numbers.md` §2](../../../docs/load_bearing_numbers.md)). Preservation-trade authority: AGENTS.md §Live-execution posture.
- **Eval economics.** Cheap-retry and one-shot evals warrant different bust gates; pre-register which model a threshold assumes before reading results.
- **Venue transfer.** A lock on one feed/venue does not transfer its edge: every switch is a gated hypothesis; run the feed-equivalence pre-flight first. Worked failures (P2, R5): R6 NO-GO.

## Portfolio Monte Carlo

`core/portfolio_mc.py` gives the pass/bust distribution for locked strategies under firm rules and `dd_protection`.

### When to run

- After a broker CSV export plus re-exported TV backtests, if pass/bust drift more than ~1σ from locked expectation (usually regime change, not breakage)
- Before any allocation or parameter change: ALWAYS re-MC before locking
- At any Re-MC trigger
- For each risk multiplier or reduced-risk arm: never scale a bust delta from another multiplier, because barrier interaction is non-linear ([S4 withdrawal §5](../../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md))

### Methodology

1. **Ingest** per-strategy TV CSVs for the panel; canonical feed `core/data/tv_exports/cme/`. Pair Entry/Exit rows by `Trade #`.
2. **Reconcile (MANDATORY)** each CSV against its Pine-header backtest: trade count, net P&L, PF, DD within 0.5%. Halt if any leg fails.
3. **Implied 1R:** Guardian (no BE): median loss. Striker DJ30/NAS100 and Aegis (BE exits): mean of `|losses| > 1%` of account. Median fallback ONLY on zero full stops; thin-cohort warning when `1 ≤ n < 5`.
4. **Scale factor:** `target_risk_pct / implied_risk_pct`, applied to every trade's P&L.
5. **Daily panel:** business-day index, strategy columns, scaled P&L summed on exit date, missing days zero.
6. **Week-block bootstrap:** Mon-anchored 5-day non-overlapping blocks, with replacement until the horizon fills.
7. **Simulate** from the firm's starting balance with `dd_protection` scaling; end on PASS, BUST (per `dd_type`) or INACTIVITY.
8. **Aggregate:** 10K sims × 3 seeds; report mean and σ.

Intraday-barrier runs (`simulate_path(intraday_low=...)`): take each day's excursion as the position's side-aware worst post-entry mark, never session `min(Low)`, and apply the same drawn block indices to both paired panels ([ORB Addendum 2026-08-02](../../../docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md)).

### Locked anchor (historical regression pin)

Literals: [`docs/mc_anchor_history.md`](../../../docs/mc_anchor_history.md), `ops/recall/guard.py` (historical anchor constant). Regression: `tests/core/test_mc_synthetic_engine.py`. Scope: [rescope ADR](../../../docs/adr/2026-07-11-challenge-era-claims-rescope.md).

The pin is FXIFY-shaped (static DD, one-shot eval): never apply it to trailing-DD tiers. Successor self-funded risk questions need a fresh Pre-Q (rescope ADR). Any new MC pin comes from a deterministic re-run of production code, never from a side script or eyeballed output ([forbidden moves](../../../docs/adr/2026-05-16-fxify-correct-timeout-semantic.md)).

### Methodology traps

- **Exit-date day-of-week misleads for long holds** (Guardian): segment by entry date.
- **Standalone MaxDD is the wrong sizing input:** portfolio tail contribution matters more.
- **Stationarity breaks across regimes:** re-run MC after any structural change.
- **Model live protection semantics:** `min()` vs `*=` in `dd_protection.py` must match in MC; read the code.

## Core principles

1. **Locked at the parameter axis.** Parameter/allocation changes require MC-validated re-locks. Capital authorization is a separate revocable axis: [`strategy_lifecycle.md`](../../../docs/methodology/strategy_lifecycle.md).
2. **No overlays.** No regime or conflict overlays on physical facts; reintroducing one needs a fresh INQHIORI loop showing base logic is insufficient (record: tag `pre-prune-2026-06-05`).
3. **Do not quote challenge-era pass/bust rates as live probabilities.** The pin is regression-only until a successor self-funded risk Pre-Q lands.

## Related skills

`pinescript-v6` (strategy code); `trade-csv-reconcile` (CSV metrics feed the MC); `strategy-validation` (robustness gates); `handoff-verify` (handoffs touching ops posture).
