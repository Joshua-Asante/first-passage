# TradingView Strategy Report / Deep / `1!` warehouse — July 2026 updates note

**Date:** 2026-08-28
**Type:** Platform-ops research note — not a Pre-Q, ADR, skill, or ORB unpark.
**queue-exception:** operator asked for a written note from the ORB-MNQ-1 recon-v6 chart-diagnosis thread; live queue stays `#1` Phase B / `#2` B7-REFIRE.
**Disposition:** **KEEP as owner.** Point skills here. Do not open a Q unless someone wants a measured `MNQ1!` warehouse census. Does **not** unpark standalone ORB-MNQ-1 (still FALSIFIED/PARK for Tradeify on the intraday-MC record).

---

## Amendment-first (sub-rule 10)

New file. No existing owner can hold the July 2026 Strategy Report rewrite plus the `MNQ1!` engine-series cliff.

Attestation (literal search, 2026-08-28):

- `lab/CATALOG.md` — no hits for `Strategy Tester` / `Deep Backtesting` / `bar detalization` / `Strategy Report` / `Available chart range`.
- `docs/briefs/INDEX.md` — same; open Qs that *touch* TV (`Q-SIGID-1`, `Q-FILLTAX-1`) are signal-identity / fill-optimism, not tester-warehouse coverage.
- `docs/rejected_candidates.md` — no tester-rewrite row.
- `docs/methodology/lessons/methodology_lessons.md` — TV lessons exist (JPY `<30d` P&L, alert-vs-logic lag) and are a different class.
- [`pinescript-v6`](../../../.claude/skills/pinescript-v6/SKILL.md) “TradingView Platform Limits” is compile/object caps, not report-mode / `1!` Deep rules.
- [`d11`](../../pursuits/d11-tradingview-subscription.md) is the Premium/Deep *subscription* KEEP, not tester ops.
- [`trade-csv-reconcile`](../../../.claude/skills/trade-csv-reconcile/SKILL.md) owns CSV schema / pairing, not the warehouse that produced the CSV.

---

## What this note is for

A Pine strategy on `MNQ1!` can keep drawing OR lines and `plotchar` markers through May–August while the **Strategy Report** last fill and buy-and-hold both die in mid-April. That is a **platform series split**, not a frozen opening-range.

Use this note before treating a TV report, List-of-Trades export, or on-chart arrow drought as “the strategy stopped working.”

---

## What TradingView shipped (2026)

### July 2026 — Strategy Tester → Strategy Report

Official Pine release notes ([`release-notes` § July 2026](https://www.tradingview.com/pine-script-docs/release-notes/)):

| Old control | New control | Default meaning |
|---|---|---|
| Strategy Tester | **Strategy Report** | Same panel, new name and menus |
| “Using bar magnifier” checkbox | **Bar detalization** (`Default` / `High`) | `use_bar_magnifier` only sets the default |
| Scattered calc checkboxes | **Script execution** menu | `On bar close` always on; others additive |
| Custom / Last-N date pickers | **Testing period** menu | Any **non-default** period **activates Deep** |
| 9,000-order **error and stop** (regular mode) | 9,000-order **trim oldest**, keep simulating | Deep still keeps every trade up to 1M |

Also renamed in Properties: Heikin Ashi fill mode, limit-order execution dropdown, order-execution delay, long/short **leverage** (margin args still accepted and converted).

New declaration flag: `calc_on_every_history_tick` (Premium/Ultimate, standard candles only). Pairs with detalization tick count.

Pine docs: selecting a different period from the Testing period menu **activates Deep Backtesting**, and the main chart will not scroll from that report ([Strategies](https://www.tradingview.com/pine-script-docs/concepts/strategies/)).

### August 2026 — not tester

`once` keyword, UDT binary-search, Pine Screener index source. Same-year, not the report rewrite.

### Help Center that now matches the UI

- [How Deep Backtesting works](https://www.tradingview.com/support/solutions/43000666265-how-deep-backtesting-works/) — pink icon; results **only** in the report; **Reset to chart session** leaves Deep.
- [Why Deep trades are not on the chart](https://www.tradingview.com/support/solutions/43000670566-why-are-the-results-of-deep-backtesting-not-shown-on-the-chart/) — chart arrows are **always** regular-mode (chart-loaded bars), even when Deep is on.
- [Regular vs Deep mismatch](https://www.tradingview.com/support/solutions/43000666266-why-do-the-data-of-the-regular-mode-and-deep-backtesting-not-match/) — Deep starts at the **range start**; regular starts at the **chart’s first loaded bar**. EMAs/RMAs (and anything path-dependent) diverge even on overlapping calendars.
- [How much Deep data exists](https://www.tradingview.com/support/solutions/43000668210-how-much-data-is-available-for-deep-backtesting/) — **silent partial data** (quoted below).
- [`1!` Deep restrictions](https://www.tradingview.com/support/solutions/43000730038-what-restrictions-apply-while-using-the-deep-backtesting-mode-on-continuous-futures/) — extra load-shed on spliced continuous futures.
- [Bar detalization](https://www.tradingview.com/support/solutions/43000786180-bar-detalization/) — tick table.
- [Script executions](https://www.tradingview.com/support/solutions/43000786178-script-executions/) — the menu is **not** the Pine log / warning badge.
- [Strategy Report: How to start](https://www.tradingview.com/support/solutions/43000764138-tradingview-strategy-report-how-to-start/) — Overview buy-and-hold is a **report-series** benchmark.

---

## Official rules that bite this desk

### 1. Chart series ≠ report series

| Surface | What it uses | What you see |
|---|---|---|
| Price pane + `plot` / `plotchar` | Chart-loaded bars (plan cap: 5k / 10k / 20k / 25k / 40k intraday) | OR lines, markers, live candles through “today” |
| Regular Strategy Report | Same chart-loaded bars | On-chart trade arrows; List of trades |
| Deep / any non-default testing period | Warehouse bars in the **selected calendar**, subject to symbol/TF holes | Report only; pink DEEP; no chart arrows for those fills |

Premium here is confirmed ([`d11`](../../pursuits/d11-tradingview-subscription.md)). Plan bar caps: [intraday history](https://www.tradingview.com/support/solutions/43000480679-i-can-t-see-all-historical-data-on-resolutions-lower-than-1-day/).

### 2. Deep on continuous futures (`MNQ1!`, `NQ1!`, `ES1!`, …)

From the official `1!` article:

- Minute TF of `N` minutes: max requested depth is **`N × 3` years, counted from today**.
- Second TF of `N` seconds: **`N × 3` months from today**.
- That clock starts from **today even if the date picker end date is earlier**.
- Plus the global Deep cap: **2 million bars / 1 million trades**. If a window exceeds 2M bars, Deep keeps the **most recent** 2M.

`15m` → 45y lookback, `30m` → 90y lookback. This rule mainly **cuts old** history. It does **not** by itself explain a May–August hole. It does prove `1!` Deep is a **different, load-shed warehouse** than the price pane.

### 3. Silent partial warehouse (the May hole rule)

Quoted from [Deep data availability](https://www.tradingview.com/support/solutions/43000668210-how-much-data-is-available-for-deep-backtesting/):

> If only some intraday data is available within the selected period, the strategy will calculate in its typical fashion.

No error. Date chip can still read `Jan 1, 2024 – Aug 27, 2026`. Empty warehouse → `"No data for the selected period and chart timeframe"`. Partial warehouse → **quiet short series**.

Buy-and-hold on the **report** dying on the same bar as the last fill means the **engine ran out of bars**. It does not mean the OR logic died. Chart B&H / candles can continue.

### 4. Bar detalization is a second warehouse

[Official tick table](https://www.tradingview.com/support/solutions/43000786180-bar-detalization/):

| Chart TF | High detalization LTF | Ticks / bar |
|---|---|---|
| 15m | 2m | 28 |
| 30m | 5m | 24 |
| 60m | 10m | 24 |
| Default (any) | none (OHLC/OLHC) | 4 |

`High` needs that lower-TF store. A hole in 2m/5m `MNQ1!` Deep can empty a High run even when Default 15m/30m still has bars. `On history bar tick` multiplies script runs by that tick count (Premium; standard candles only).

### 5. Trade-list limits (current, not folklore)

| Mode | Official trade memory |
|---|---|
| Regular (default testing period) | Keep latest **9,000**; **trim** older (July 2026: no longer error-and-stop) |
| Deep | Keep **all**, cap **1,000,000** |

`500` is the **max labels/lines/boxes** ceiling, not a documented closed-trade cap. A List-of-Trades that stops on trade number 500 is still an observation — treat as undocumented path until an export proves more than 500 on that same pane.

---

## Empirical pin (this desk, 2026-08-27/28)

ORB-MNQ-1 recon v6 and stripped diagnostics on **`MNQ1!`**, ETH, B-ADJ. Source of truth = on-chart table / List of trades, **not** order-label arrows (TV stops drawing those).

| Run | TF | Period UI | Closed | Last exit | Read |
|---|---|---|---|---|---|
| Kitchen-sink, Deep last-365d | 15m | Last 365d Deep | 105 | 2026-04-30 16:45 | EOD flatten; chart B&H continued |
| Kitchen-sink, filter off | 15m | Chart session | 74 | 2026-04-21 15:30 | Chart B&H through Aug |
| `v6-ofix` | 15m | Chart | — | still 21 Apr | Exit hygiene did not open May |
| `v6-mkt` | 15m | Deep (custom dates crept back) | 94 | April | `newOR` / `orJustEnded` chars continued |
| `v6-bare` | 15m | Chart | 101 | 2026-04-16 16:45 | Extras off; still April |
| `v6-bare2` | 30m | Chart | **500 exactly** | 2026-04-07 16:30 | Plotchars through May |
| `v6-gate` Jan 2026 start | 30m | Deep custom Jan–Aug | 40 | **2026-04-13 16:30** | B&H **and** equity die same day |
| Same gate after “reset” | 30m | **Available chart range** `2024-01-01 – 2026-08-27` | **40** | **2026-04-13 16:30** | Reset gray; `inWindow: yes`; Default detalization |
| **Vanguard Gold Futures v0.4** on **`MGC1!`** | 15m | **Last 365d Deep**, Default detalization | 99 | **2026-08-25 16:45** | Report B&H continues through Aug; same Deep UI as the MNQ 15m Last-365d run that died 2026-04-30 |

A prior 6yr List-of-Trades of the MNQ construct **did** fill through **2026-08-21** ([`aegis_orbmnq_combined_book` RESULTS](../../../lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md)). So the **symbol can have post-April trades**; this week’s `MNQ1!` tester pane did not.

### Cross-symbol split (2026-08-28)

Same account, same Deep Last-365d, same 15m, Default detalization:

| Symbol | Last report fill | Report B&H after April? |
|---|---|---|
| `MNQ1!` (ORB recon kitchen-sink) | 2026-04-30 16:45 | chart B&H continued; report series did not |
| `MGC1!` (Vanguard Gold v0.4) | 2026-08-25 16:45 | yes — hover on trade 99 |

That **falsifies** “Deep 2026 is broken,” “Last-365d Deep cannot see past April,” and “the July rewrite killed all `1!` recent warehouse bars.” Deep on this desk still prints August on COMEX micro gold. The April cliff is **`MNQ1!` (or that pane’s warehouse)**, not a global Deep outage.

Do not read the gold Overview numbers as a strategy verdict. This pin is **last-fill date / period UI only**.

`MGC1!` showed **Script execution (2)** — still open the real warning text; it did not stop that series.

### Hypothesis (not a TV-published formula)

Two stacked stories, now separable:

1. **`MNQ1!` 15m Last-365d Deep dies ~30 Apr while `MGC1!` 15m Last-365d Deep lives to 25 Aug.** Same menu. That is a **symbol warehouse** hole (or an MNQ-only bar budget inside Last-365d), not a platform Deep kill-date.
2. **`MNQ1!` 30m Available chart range `2024-01-01 – 2026-08-27` dies 13 Apr with report B&H.** A from-start 40k-bar walk can still be a *second* limiter on that longer chip. Official Deep-over-2M keeps the **most recent** bars — the opposite. Do not collapse (2) into (1).

April 13 is **not** an MNQ roll (Mar / Jun / Sep / Dec). Dated front month (`MNQU2026`) is still the clean split of “this Pine” vs “`MNQ1!` warehouse.”

---

## UI traps learned on this rewrite

1. **“Reset to chart session” gray** — already on the default period. Default can still be a Deep-class / warehouse series (`Available chart range` with a 2024–2026 chip).
2. **Detalization menu visible ≠ High is on.** Default is 4 ticks. The menu exists on the report toolbar after July; that is not Bar Magnifier “on.”
3. **Script execution (1)** in the UI is often the **calc-event dropdown** (`On bar close`), not the unread warning log. Open the actual script-warning text.
4. **Do not gate diagnostic tables on `barstate.islast`.** Compiler warns; the live last bar is unconfirmed; the table belongs on the **candlestick pane**, not Overview.
5. **Order labels vanish** long before the emulator stops. `plotchar` / a `var table` of `strategy.closedtrades` is the count.
6. **Custom dates / Last 90 / Last 365** → pink DEEP + detalization. Official leave-Deep: Reset to chart session — when it is enabled.
7. Kitchen-sink `strategy.exit` / flatten-every-overnight-bar **moves** the last fill (7 Apr → 16 Apr on 15m) and can hit order/trade memory; it does not by itself open a May–August warehouse hole.

---

## What is not the May hole

Already ruled out on this construct, and the docs agree:

- Frozen `orHigh` / `orLow` — lime/red steps through May on the **price** pane.
- Volume filter — Deep empty with filter on **and** off.
- “Forgot to reset Deep” — Reset disabled because the period was already the advertised default.
- v6 9,000-order **stop** — current regular mode **trims**; it does not freeze new trades. A May-empty Deep report with ~40–100 trades is not this cap.
- **Platform-wide Deep 2026 hole** — `MGC1!` 15m Last-365d Deep last fill **2026-08-25 16:45** on this same desk.

---

## What to run instead of arguing with `MNQ1!` Deep

In order:

1. **Dated front month** (`MNQU2026` / `MNQU6`) same TF and script. Single contract → `1!` Deep restrictions do not apply. If May–August fills appear, the Pine is fine and the `MNQ1!` warehouse is the defect. (Cross-symbol Deep is already split: `MGC1!` Last-365d lives to 25 Aug.)
2. **1h / 4h `MNQ1!`** — fewer bars, longer calendar, same continuous rules. Distinguishes “no recent MNQ warehouse” from “30m / 15m bar budget exhausted.”
3. **`MNQ1!` Last 90 days Deep** — if that is **also** empty while candles print, the *recent* MNQ warehouse is the hole (the `MGC1!` Last-365d pin already shows Last-N Deep can see August on another `1!`).
4. Export **List of trades** (not Overview screenshots). Last exit date is the claim.
5. Open the real script-warning text.

Do not use this tester pane to judge post-April logic on `MNQ1!` until one of those splits the series.

---

## Skill / home recommendation

**Do not create a new skill.** This is platform-ops, not a third Pine-authoring pipeline. A standalone skill would rot next to `pinescript-v6` and `trade-csv-reconcile`.

**Do (this commit):**

- Keep **this note as owner**.
- Add a short trap block to [`pinescript-v6`](../../../.claude/skills/pinescript-v6/SKILL.md) so any TV/Pine session hits the series-split before rewriting entries.
- Add a CSV-provenance sub-rule to [`trade-csv-reconcile`](../../../.claude/skills/trade-csv-reconcile/SKILL.md): last exit << chart last bar on a `1!` export is a warehouse/period claim, not a silent “strategy died.”

**Do not (unless it keeps biting):**

- A methodology lesson — would dual-home the same traps. Promote later if a second session re-derives this.
- A Q / lab slug — no cheap falsifier beyond “open MNQU6”; not a strategy question.
- Fold into `d11` — that row is subscription KEEP, not UI doctrine.
- Unpark ORB-MNQ-1 off this note.

---

## Related owners (different questions)

- [`Q-FILLTAX-1`](../../briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md) — fill optimism / Pine↔Python parity. Detalization changes *how* a bar fills; it does not restore missing warehouse bars.
- [`Q-SIGID-1`](../../briefs/Q-SIGID-1-intra-bar-signal-identity.md) — mid-bar `alert()` vs close. Script-execution / history-tick settings can move that gap; they are not this note’s cliff.
- [`Q-TVCOV-1`](../../briefs/closures/Q-TVCOV-1-closure-falsified.md) (closed) — Databento/TV **bar coverage**, not Strategy Report warehouse vs chart pane.

---

## Sources (official first)

1. [Pine release notes — July 2026](https://www.tradingview.com/pine-script-docs/release-notes/)
2. [Pine — Concepts / Strategies](https://www.tradingview.com/pine-script-docs/concepts/strategies/) (testing period → Deep; 9,000 trim; `first_index`)
3. [Pine — Writing / Limitations](https://www.tradingview.com/pine-script-docs/writing/limitations/) (9,000 / 1,000,000)
4. [Deep Backtesting — how](https://www.tradingview.com/support/solutions/43000666265-how-deep-backtesting-works/)
5. [Deep — data availability + silent partial](https://www.tradingview.com/support/solutions/43000668210-how-much-data-is-available-for-deep-backtesting/)
6. [Deep — not drawn on chart](https://www.tradingview.com/support/solutions/43000670566-why-are-the-results-of-deep-backtesting-not-shown-on-the-chart/)
7. [Deep vs regular mismatch](https://www.tradingview.com/support/solutions/43000666266-why-do-the-data-of-the-regular-mode-and-deep-backtesting-not-match/)
8. [Deep on continuous futures](https://www.tradingview.com/support/solutions/43000730038-what-restrictions-apply-while-using-the-deep-backtesting-mode-on-continuous-futures/)
9. [Bar detalization + tick table](https://www.tradingview.com/support/solutions/43000786180-bar-detalization/)
10. [Script executions](https://www.tradingview.com/support/solutions/43000786178-script-executions/)
11. [Intraday bar limits by plan](https://www.tradingview.com/support/solutions/43000480679-i-can-t-see-all-historical-data-on-resolutions-lower-than-1-day/)
12. [Strategy Report: How to start](https://www.tradingview.com/support/solutions/43000764138-tradingview-strategy-report-how-to-start/)
