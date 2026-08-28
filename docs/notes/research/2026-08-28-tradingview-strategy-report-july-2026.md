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

A Testing period chip can move the last fill by months on the **same** Pine. Entire-history Deep on the original recon v2 fills through late August; Last-365d Deep last-exits April; Last-90d Deep is a zero-trade report. That is **not** “the strategy died.” Dated front month / session-edge adjacency is a **different** pin (`MNQU2026`). Inventory the period chip before rewriting entries.

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
| **`v6-gate` on `MNQU2026`** | 30m | `2025-06-24 – 2026-08-27`, Default detalization | **14** | **2026-04-07 16:30** | Dated front month. Table: `Window: yes`, open 0. Legend OR near live print. Chart candles continue. |
| **recon v2 original, entire-history Deep** | 15m | `Dec 31, 1799 – Aug 27, 2026` Deep, Default detalization | **2397** | **2026-08-27 16:45** | Same script/defaults as the Last-365d row. Hover is trade 2397. Overview numbers are **not** a verdict. |
| **recon v2 original, Last 90d Deep** | 15m | Last 90d Deep, Default detalization | **0** | — | Empty-report copy: “This report requires trade data” — **not** the official “No data for the selected period” warehouse string. |

A prior 6yr List-of-Trades of the MNQ construct **did** fill through **2026-08-21** ([`aegis_orbmnq_combined_book` RESULTS](../../../lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md)). Entire-history Deep on the **original** recon v2 now also last-exits **2026-08-27**. Last-N on that same script does not.

### Cross-symbol split (2026-08-28)

Same account, same Deep Last-365d, same 15m, Default detalization:

| Symbol | Last report fill | Report B&H after April? |
|---|---|---|
| `MNQ1!` (ORB recon kitchen-sink) | 2026-04-30 16:45 | chart B&H continued; report series did not |
| `MGC1!` (Vanguard Gold v0.4) | 2026-08-25 16:45 | yes — hover on trade 99 |

That **falsifies** “Deep 2026 is broken” and “the July rewrite killed all `1!` recent warehouse bars.” Deep on this desk still prints August on COMEX micro gold. **Last-365d on `MNQ1!` still last-exits April** — that chip is not rehabilitated by gold. Dated front month later showed Pine adjacency can produce the same last-exit shape. Entire-history vs Last-N on the **same** original script is the next subsection — do not stop here.

Do not read the gold Overview numbers as a strategy verdict. This pin is **last-fill date / period UI only**.

`MGC1!` showed **Script execution (2)** — still open the real warning text; it did not stop that series.

### Hypothesis (not a TV-published formula)

Two stacked stories, now separable:

1. **`MNQ1!` 15m Last-365d Deep dies ~30 Apr while `MGC1!` 15m Last-365d Deep lives to 25 Aug.** Same menu. That is a **Last-N-on-MNQ** hole, not a platform Deep kill-date. Entire-history on the same original script later filled late August — do not read this row as “`MNQ1!` Deep has no August bars.”
2. **`MNQ1!` 30m Available chart range `2024-01-01 – 2026-08-27` dies 13 Apr with report B&H.** A from-start 40k-bar walk can still be a *second* limiter on that longer chip. Official Deep-over-2M keeps the **most recent** bars — the opposite. Do not collapse (2) into (1). Period-chip pin on the original recon v2 is below — do not stop at (1)–(2).

April 13 is **not** an MNQ roll (Mar / Jun / Sep / Dec).

**Dated front month does not clear the Pine.** `v6-gate` on `MNQU2026` 30m last-exits **2026-04-07 16:30** with `Window: yes` and OR levels in the legend sitting on the live print, not an April freeze. The Performance-tab tooltip on the rightmost node is the **last trade**, not proof the report series ended (that chart is trade-indexed). That pin stays. It does **not** explain Last-N emptiness on `MNQ1!` 15m — see the period-chip pin below.

### Period chip on the original recon v2 (2026-08-28)

Operator pin, same script (`ORB-MNQ-1 recon v2`), same defaults, `MNQ1!` 15m, Default detalization, Deep every time (any non-default period activates Deep):

| Period chip | Closed | Last report fill | Empty-state copy |
|---|---|---|---|
| Entire history (`Dec 31, 1799 – Aug 27, 2026`) | 2397 | **2026-08-27 16:45** | — |
| Last 365 days | 105 | **2026-04-30 16:45** | — |
| Last 90 days | 0 | — | “This report requires trade data” (not official no-data-for-period) |

Operator also said Last-N “doesn’t get past April 17.” Treat that as a different chip or earlier run; the Last-365d hover on this paste is **Apr 30**. Do not collapse the two dates.

**Read:** the original Pine **can** fill late August on this symbol/TF. Last-N Deep is a **different request** than entire-history Deep. Official Deep-over-2M keeps the **most recent** bars — Last-365d dying in April while entire-history includes August is the opposite of that rule, so this is silent partial / Last-N-specific slice, not “the script stopped in April.” Last 90d from late August sits **after** that April last-exit; a zero-trade report there is what you get if that chip’s series has no placeable bars (or the script places nothing on that slice). Official empty-warehouse copy is a different string — pin the copy you see.

Do **not** collapse this with the `MNQU2026` adjacency pin. Do **not** read 2397 / Overview % as a strategy verdict or an unpark. `v7-cal` remains the session-helper fix for gapped dated contracts; it is **not** required to obtain August fills on `MNQ1!` entire-history Deep.

### Pine logic (recon v6 / v6-gate / v6-mkt)

Owner reads: uploaded `orb-mnq.v6_0394.pine` (kitchen-sink), `orb-mnq.v6_ofix.pine`, `orb-mnq.v6_mkt.pine`. `v6-gate` is those plus a start-date input (table `Window: yes` on the last bar ⇒ the start gate is **not** excluding May–August).

Two real defects, both in the session helpers:

1. **Adjacent-bar OR edge** (`newOR = inOR and not inOR[1]`, `orJustEnded = not inOR and inOR[1]`). That only fires when the previous *existing* bar flips. On a thin dated contract (or any 30m series that skips the post-OR slot), yesterday’s last print can itself be an OR bar. Then today’s first OR bar has `inOR[1] == true` → **no `newOR`**, **no `orJustEnded`**. `orArmedToday` stays true (it only clears on `newOR`), so even a later `orJustEnded` is rejected by `not orArmedToday`. OR high/low can still move via `else if inOR` — which matches a live legend with no new fills.

2. **Place and leave on the same bar.** Kitchen-sink flatten is `sessionEndBar = lastBarOfSession or not inSession` then `cancel` + `close_all` every overnight bar. ofix/mkt narrowed that to `lastBarOfSession or leftSession`, but on a gapped series `leftSession` is the first bar after yesterday’s last in-session print. If that bar is also the first bar after yesterday’s OR (`orJustEnded`), v6-mkt **cancels the market entry it just placed**. ofix even plots that collision as ✕.

Neither defect needs a April calendar. They fire whenever the 30m (or gapped 15m) series stops putting a non-OR bar immediately after the OR window. Back-month `MNQU` is exactly that shape until it is front-month — and the last fill sitting on an EOD flatten (`16:30`) is consistent with “the last day that still had a post-OR bar.”

Not the date input (`Window: yes`). Not volume (off on gate/mkt). Not “OR froze.”

---

## UI traps learned on this rewrite

1. **“Reset to chart session” gray** — already on the default period. Default can still be a Deep-class / warehouse series (`Available chart range` with a 2024–2026 chip).
2. **Detalization menu visible ≠ High is on.** Default is 4 ticks. The menu exists on the report toolbar after July; that is not Bar Magnifier “on.”
3. **Script execution (1)** in the UI is often the **calc-event dropdown** (`On bar close`), not the unread warning log. Open the actual script-warning text.
4. **Do not gate diagnostic tables on `barstate.islast`.** Compiler warns; the live last bar is unconfirmed; the table belongs on the **candlestick pane**, not Overview.
5. **Order labels vanish** long before the emulator stops. `plotchar` / a `var table` of `strategy.closedtrades` is the count.
6. **Custom dates / Last 90 / Last 365** → pink DEEP + detalization. Official leave-Deep: Reset to chart session — when it is enabled. Last-N and entire-history are **different Deep requests** on the same script — flip the chip before rewriting Pine.
7. Kitchen-sink `strategy.exit` / flatten-every-overnight-bar **moves** the last fill (7 Apr → 16 Apr on 15m) and can hit order/trade memory; it does not by itself open a May–August warehouse hole.
8. Empty-report **“This report requires trade data”** ≠ official **“No data for the selected period.”** Zero trades vs empty warehouse. Pin the copy.

---

## What is not the May hole

Already ruled out on this construct, and the docs agree:

- Frozen `orHigh` / `orLow` — lime/red steps through May on the **price** pane.
- Volume filter — Deep empty with filter on **and** off.
- “Forgot to reset Deep” — Reset disabled because the period was already the advertised default.
- v6 9,000-order **stop** — current regular mode **trims**; it does not freeze new trades. A May-empty Deep report with ~40–100 trades is not this cap.
- **Platform-wide Deep 2026 hole** — `MGC1!` 15m Last-365d Deep last fill **2026-08-25 16:45** on this same desk.
- **“Original Pine cannot fill May–August on `MNQ1!` 15m”** — entire-history Deep on recon v2 last-exits **2026-08-27 16:45**. Last-N emptiness is the chip, not a script death.

---

## What to run instead of arguing with `MNQ1!` Deep

**Period chip is the first lever on `MNQ1!` 15m.** Entire-history Deep on the original recon v2 already fills through late August. Last 365 / Last 90 are different Deep requests. Do not paste `v7-cal` to “fix” Last-N on this symbol.

1. Export **List of trades** from the entire-history Deep pane if you want a CSV of the August last-exit. Overview % is not a claim.
2. `v7-cal` stays the kitchen-sink paste for **`MNQU2026` / gapped 30m** (session-edge). Source: session-local `uploads/orb-mnq.v7_cal.pine` (gitignored). `v6-logic` remains the stripped diagnostic.
3. Open the real script-warning text.
4. Do **not** unpark ORB-MNQ-1 off either pin.

---

## Skill / home recommendation

**Do not create a new skill.** This is platform-ops, not a third Pine-authoring pipeline. A standalone skill would rot next to `pinescript-v6` and `trade-csv-reconcile`.

**Do (this commit):**

- Keep **this note as owner**.
- Add a short trap block to [`pinescript-v6`](../../../.claude/skills/pinescript-v6/SKILL.md) so any TV/Pine session hits the pane/warehouse **and** session-edge checks before rewriting entries.
- Point [`trade-csv-reconcile`](../../../.claude/skills/trade-csv-reconcile/SKILL.md) last-exit << chart last bar at this note: flip Last-N vs entire-history on the same script first; dated front month dying does not prove warehouse; Last-N emptiness on `MNQ1!` does not prove adjacency.

**Do not (unless it keeps biting):**

- A methodology lesson — would dual-home the same traps. Promote later if a second session re-derives this.
- A Q / lab slug — period-chip cheap check on the original script already ran (entire-history fills late August; Last-N does not). Not a Q. `v7-cal` stays the gapped-contract paste.
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
