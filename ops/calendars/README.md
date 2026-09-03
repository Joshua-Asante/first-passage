# CME holiday & early-close calendars

Durable, reusable CME session calendars for 2022–2026. Landed 2026-09-03 under operator ruling
**D12** on the seven-strategy `Tradeify_Select_100K` campaign
([campaign state](../../docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md)),
so that no future session has to re-derive them.

| File | What it owns |
|---|---|
| [`cme_holiday_calendar_2022_2026.json`](cme_holiday_calendar_2022_2026.json) | 85 dated entries, per product group (equity index · metals · FX): status, close time in ET, confidence, and a per-entry note. Plus three derived lists and a 13-item `unresolved` register. |

## ⚠ Provenance is SECONDARY, not primary

**No CME primary source was fetched for any date in this file.** `www.cmegroup.com`,
`investor.cmegroup.com` and every broker mirror return 403 at the egress proxy's CONNECT layer.
Every cell is reconstructed from independent third-party encodings of the CME schedule
(QuantConnect Lean's market-hours database, `pandas_market_calendars`, `exchange_calendars`,
`vacanza/holidays`, one C++ reimplementation), cross-checked against in-repo measured bar panels.

Treat it as **working-grade, not audit-grade**. To close it out, allowlist `www.cmegroup.com` and
read the per-holiday clearing advisories, or make an authenticated CME Reference Data API pull
(Globex Trading Hours and Holiday Schedules). For historical dates prefer the post-hoc
settlement-times PDFs over the ex-ante advisories — CME finalises holiday hours roughly two weeks
out — and never conflate a settlement time with a Globex close time.

## The three derived lists

* **`venue_flat_dates`** (49) — dates where **any** of the three groups closes early. This is the set
  on which Tradeify's **12:59 ET** holiday-short force-flat deadline applies.
* **`full_closure_dates`** (16) — all three groups closed on the CME trade date. Load-bearing for the
  venue's ≥1-trade-per-Mon–Fri-week inactivity rule.
* **`sub_deadline_close_dates`** (3) — dates whose early close falls **before** 12:59 ET, which a
  12:59 deadline model structurally cannot express.

## One list per account, never one list per product

Tradeify's 12:59 ET deadline is an **account-level** rule with no per-product carve-out
([`ops/prop_envelope_default.md`](../prop_envelope_default.md), article `10495876`). A
product-group-specific list is therefore **unsafe**: on an ordinary US federal holiday CME FX runs a
normal session while equity index closes at 13:00 ET, so an FX-derived list would leave a 6J
position resting past the venue deadline. Use the **union**.

This is why the three venue-bound Pine bodies (Aegis 6J, Vanguard MGC, ORB MNQ) all carry the same
list rather than three different ones.

> ⚠ **CORRECTION 2026-09-03 (Codex on [PR #291](https://github.com/Joshua-Asante/first-passage/pull/291), P2, accepted).**
> An earlier revision of this file built the guard list as `venue_flat_dates ∪ full_closure_dates`,
> justifying the union with "fully-closed dates are inert in a guard (no bars, no effect)."
> **That justification is wrong.** A Pine guard keys on the bar's **wall-clock** date, while
> `full_closure_dates` rows are keyed to the **CME trade date** — and this file's own `day_basis`
> note records that 2022-12-26, 2023-01-02 and their siblings carry real Globex bars from
> 18:00–24:00 ET on that wall-clock date. Listing them marks that reopened session as short, which
> can force a flatten or block entries in a session that is not short at all.
>
> **Use `venue_flat_dates` alone for a wall-clock guard.** The list below has been corrected to 49
> verified early-close dates plus the 10 unverified 2027 carry-over rows.
>
> **The three shipped bodies still carry the old 59+16 union, and that is deliberate.** The
> difference is a **measured no-op** on all five campaign strategies: zero activity on any of the 16
> full-closure dates and **zero stamps at or after 18:00 ET anywhere** in any of the five exports,
> so the evening reopen is never reached. Re-cutting the Pine would move its pinned hash, invalidate
> the exports already taken against it, and risk consuming the re-expression lane's single permitted
> attempt — for a change proven to alter nothing. The correction lands at each body's next
> legitimate edit. ⚠ It becomes load-bearing the moment a strategy trades the evening session.

Copy-paste list for a Pine `input.text_area` — **`venue_flat_dates` only** (49 verified 2022–2026,
plus 10 unverified 2027 carry-over):

```
20220117,20220221,20220530,20220620,20220704,20220905,20221124,20221125,20230116,20230220,20230407,
20230529,20230619,20230703,20230704,20230904,20231123,20231124,20240115,20240219,20240527,20240619,
20240703,20240704,20240902,20241128,20241129,20241224,20250109,20250120,20250217,20250526,20250619,
20250703,20250704,20250901,20251127,20251128,20251224,20260119,20260216,20260403,20260525,20260619,
20260703,20260907,20261126,20261127,20261224,20270118,20270215,20270531,20270618,20270705,20270906,
20271125,20271126,20271223,20271224
```

## Three traps a consumer must not walk into

1. **The three groups close at different times.** On an ordinary US federal holiday: equity index
   **13:00 ET**, metals **14:30 ET**, FX often **NORMAL**. A single date-level flag cannot express
   that, and is over-tight for metals and FX by 60–240 minutes. That is fine for a *venue* deadline
   (the venue rule is blanket) and wrong for an *exchange session* model.
2. **Day basis.** Every `FULL_CLOSURE` row is keyed to the **CME trade date**, not the wall clock.
   2022-12-26, 2023-01-02, 2023-12-25 and 2025-12-25 each carry ~360 minutes of real Globex trading
   on the calendar day — the 18:00–24:00 ET reopen, which belongs to the next trade date. TradingView
   bar exports are stamped by **wall clock**. Decide which basis you mean before joining on a date key.
3. **2025-11-28 is not an ordinary half-day.** The scheduled Black Friday early close did not execute:
   a cooling failure at the CyrusOne CH1 data centre took all of Globex down for roughly ten hours.
   No calendar library encodes the outage. An audit reading that date as merely shortened would
   wrongly conclude the week of Mon 2025-11-24 had a live Friday available for the inactivity rule.

## Contested cells

Thirteen items sit in the file's `unresolved` array with the competing readings, the sources on each
side, and the size of the error. They are almost entirely about close **times**, not about which
dates are early-close days — so they do not move `venue_flat_dates`, and a blanket venue deadline is
insensitive to all of them. The live ones worth knowing:

| Cell | Dispute | Size |
|---|---|---|
| FX on every US-holiday early close, 2022–2026 | Libraries say FX stopped observing US-holiday early closes from 2022; [`ops/instruments/6J.md`](../instruments/6J.md) defect **F3** records a direct 6J bar-panel measurement of a ~14:00 ET halt on MLK 2024-01-15 and Labor Day 2024-09-02 | up to 4h on 6J |
| Labor Day metals | Lean 14:30 ET vs `pandas_market_calendars` 13:00 ET, traced to an unwired `USLaborDayFrom2022` rule — a library defect, so 14:30 was adopted | 90 min on MGC |
| Black Friday / Christmas Eve metals & FX | Two broker channels publish directly contradictory numbers; the pmc-consistent 13:45/13:15 reading was adopted | 60–90 min |
| Friday-holiday shape (2025-07-04, 2026-06-19, 2026-07-03) | Lean says all three groups stop at 13:00 ET on a Friday holiday; pmc says ordinary Rule A | up to 4h on 6J |

## Regenerating

There is no generator script — this was a research pass, not a pipeline. To extend past 2026, either
resolve the primary source above, or re-derive from the same third-party encodings and record the
new rows with their own `confidence` and `note`. Never widen `coverage_end` without adding entries.
