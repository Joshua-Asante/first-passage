# Futures-prop venue compatibility of the 4 locked legs — hold-duration + automation audit

**Disposition:** CLOSED — R6 NO-GO — futures-prop pivot closed

**Date:** 2026-06-30 · **Scope:** lab-only (no `core/`/lock/allocation/`dd_protection`/Pine change). Lock HELD 99.83/0.17/4.37.
**Trigger:** the Q-BTC-3 Phase-0 gate ([`docs/ltm/briefs/Q-BTC-3-closure-falsified.md`](lab/archive/../../docs/ltm/briefs/Q-BTC-3-closure-falsified.md)) established that **every US futures-prop firm force-flattens every position by EOD (no overnight/weekend carry)** and 5/6 restrict full automation. Operator asked: does that threaten the broader futures-prop pivot ([[project_futures_prop_pivot]]), i.e. can the 4 locked legs themselves survive on the venue?

## Method

Measured per-leg hold durations empirically from the canonical Pepperstone TV exports (entry→exit paired by `Trade number`), which is Rule-0-clean (actual realized holds, no reliance on the private Pine source). Harness: [`hold_durations.py`](hold_durations.py) (reads the vendor-licensed exports in `~/Downloads`, same source as the 2026-06-21 decompound run). Decisive metric = **% of trades whose exit is a later calendar day than entry** (= held past at least one daily force-flatten), plus % held across a Saturday and max hold.

## Result — the swing-hold wall bites Guardian, not the index legs

| Leg (planned futures map) | N | median hold | max hold | **% held >1 day** | % over weekend | EOD-flat verdict |
|---|--:|--:|--:|--:|--:|---|
| **Guardian (XAUUSD → MGC)** | 317 | 9.50 h | **15.31 d** | **46.4%** | **20.8%** | **BLOCKED** |
| Striker DJ30 (→ MYM) | 272 | 0.75 h | 2.32 d | **3.7%** | 2.9% | mostly-OK (tail clipped) |
| Striker NAS100 (→ MNQ) | 305 | 1.00 h | 0.16 d | **0.0%** | 0.0% | **COMPATIBLE** |
| Aegis USDJPY (OANDA fx) | 150 | 0.50 h | 0.42 d | **0.0%** | 0.0% | COMPATIBLE (on OANDA anyway) |

- **Guardian is a multi-day trend-rider** — 46.4% of trades are held into a later calendar day, 20.8% across a weekend, max hold **15.3 days** (consistent with its `maxHold 850`-bar Pine cap and the Q-SWAP-1 finding that Guardian = **99.4% of portfolio overnight-swap cost**). A venue that force-flattens every position daily would truncate ~half of Guardian's trades → it **cannot run as-is on any US futures-prop firm**.
- **DJ30 is ~96% intraday** but 3.7% of trades hold overnight (max 2.3 d). EOD-flat would clip that tail — probably survivable, but it changes the strategy and needs a small quantified check (does force-closing 3.7% of trades before their exit degrade the edge / the locked MC?).
- **NAS100 and Aegis are fully intraday** (0% multi-day). NAS100 → MNQ is clean; Aegis stays on OANDA MT4 forex regardless.

## Automation (from the Q-BTC-3 Phase-0 workflow, 6 primary-sourced firms)

Full lights-out automation (the TradingView→TradersPost→Tradovate/ProjectX chain the no-manual-trading decision requires) is **prohibited/restricted at 5/6 researched firms** — Apex (banned all account types), Topstep (personal-device only, VPS banned), MyFundedFutures (supervised-only), TradeDay (no trader API), Take Profit Trader (manual-only). **Only Bulenox** clearly permits full automation among the six (but Bulenox runs on Rithmic/NinjaTrader, not the TradersPost→Tradovate rail). A dedicated automation-friendly-firm search is owed before committing the surviving legs.

## The structural split this surfaces

Futures-prop EOD-flat is a **prop-firm risk rule, not an exchange rule** — a *self-funded* CME futures account (via a retail FCM / IBKR / Tradovate API) has no forced daily flat and **can** swing-hold. So:

- **Prop-firm scaling is available only to INTRADAY strategies.** NAS100 (clean) and DJ30 (mostly) qualify; Guardian and BTC do not.
- **Multi-day-hold strategies (Guardian gold, BTC trend) can only be run self-funded** (own capital, no prop leverage) — same wall that closed Q-BTC-3.

Cross-check on Guardian's venue options confirms it is currently **un-hostable with automation for a US person**: FXIFY CFD retired/un-automatable ([[project_no_manual_trading_cfd_retirement]]); OANDA US is forex-only, no gold ([[project_ea_conversion_state]]); futures-prop force-flattens (this doc). Its only automatable home is a **self-funded** MGC futures account.

## Implication for the pivot (does NOT touch the lock)

The futures-prop pivot as scoped (re-map Guardian+DJ30+NAS to CME micros) is viable for **NAS100 (MNQ)** cleanly and **DJ30 (MYM)** with a small tail-clip check, but **not for Guardian (MGC)** — the gold trend-rider needs a swing-hold-capable venue (self-funded futures), not a prop firm. Guardian carries meaningful portfolio weight, so a prop book that drops it is a **different portfolio** than the locked 4-leg MC (99.83/0.17/4.37) describes; any prop-scaled subset must be re-MC'd on its actual leg set before it can claim the anchor. No `core/`/lock/Pine change here — this is a venue-feasibility finding.

## Owed next (operator's call)

1. **Automation-friendly firm search** — which US futures-prop firms permit the full TradersPost→Tradovate/ProjectX automation chain (beyond Bulenox)?
2. **DJ30 tail-clip quantification** — re-MC DJ30 with its 3.7% overnight trades force-closed at EOD; does the edge/anchor survive?
3. **Guardian venue decision** — self-funded MGC (own capital, swing-hold OK) vs. leaving Guardian on the retired CFD path vs. parking it.

## Reproduce

```bash
python lab/analysis/futures_prop_hold_compat_2026-06-30/hold_durations.py
# reads the Pepperstone Guardian/DJ30/NAS/Aegis exports in ~/Downloads
```
