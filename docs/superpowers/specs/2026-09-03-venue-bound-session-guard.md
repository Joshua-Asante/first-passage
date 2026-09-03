# Venue-bound session guard — the exact edit for the three deadline-spanning strategies

**Status:** specification, authored by the orchestrator 2026-09-03.
**Authorised by:** [`2026-09-03-venue-legality-re-expression-lane.md`](../../adr/2026-09-03-venue-legality-re-expression-lane.md)
(`Proposed` — this edit may be applied and the exports produced, but **their results may not be inspected**
until that record is `Accepted`).
**Applies to:** `orb_mnq_recon_v7`, `vanguard_mgc_v04`, `aegis_6j1`.
**Scope:** adds a session bound. Changes nothing else. Any other edit voids the lane.

---

## §1 — What the venue requires, and what that means for a 15-minute chart

The deadline is **16:45 America/New_York** on a regular session and **12:59 America/New_York** on a CME
early-close date (`core/firm_rules.py` Tradeify block, re-verified 2026-07-22; `ops/prop_envelope_default.md`
§1 E1). The Phase 1 audit flags a trade when a deadline instant falls in the half-open interval
`(entry, exit]` — `lab/research_utils/trade_reconciliation.py`, `entry < deadline <= exit_`. An exit filled
*exactly at* 16:45 is therefore still a violation. **The fill must land strictly before the deadline.**

Two timing facts decide the bound, and both must hold at once:

1. **Pine fills the next bar.** A `strategy.close_all()` evaluated on bar *N* executes at the **open of bar
   N+1**, unless the script already declares `process_orders_on_close = true`. Do not add that flag — it
   changes every fill in the backtest, which is outside this lane.
2. **The export's timestamp convention is not pinned.** TradingView may stamp a fill at its bar's open or at
   its bar's close. The bound below is legal under **either** reading, so the re-export cannot fail on a
   convention we have not verified.

Working it through for a **15-minute** chart — all three strategies are 15-minute
(`phase1_config.json`, `declared_bar_size_minutes: 15`):

| | Regular session | CME early-close date |
|---|---|---|
| Venue deadline | 16:45 ET | 12:59 ET |
| Flatten **signals** on the bar opening | **16:00 ET** | **12:15 ET** |
| Order **fills** at the open of the bar | 16:15 ET | 12:30 ET |
| Worst-case exported stamp (bar-close reading) | **16:30 ET** | **12:45 ET** |
| Margin to the deadline | 15 min | 14 min |

⚠ **Do not move the signal one bar later.** Signalling on the 16:15 bar fills at the 16:30 bar, whose
bar-close stamp is **16:45** — exactly the deadline, and a violation under `deadline <= exit_`. The 16:00
signal bar is the last safe one, and the same arithmetic gives 12:15 on an early-close date.

---

## §2 — The block to paste

Insert once, after the strategy's inputs and before its entry/exit logic. Nothing above it changes.
Pine **v6** throughout (`//@version=6`), so keep each ternary on one line and indent every continuation line
further than the line it continues — the two syntax rules this repo's Pine skill flags first.

The early-close set is carried as a **comma-delimited string**, not `array.from`. A fixed list of roughly forty
dates is near the practical argument count for a variadic call, and the delimited-string lookup has no such
limit and is trivially eyeballed. The leading and trailing commas matter: without them a date could match as a
substring of a neighbouring token.

```pine
// ─── Venue session bound — Tradeify_Select_100K ───────────────────────────
// Deadline 16:45 ET regular / 12:59 ET on CME early-close dates.
// Signals one bar early so the NEXT-BAR fill still lands strictly before it.
// See docs/superpowers/specs/2026-09-03-venue-bound-session-guard.md
VENUE_TZ = "America/New_York"

// Flatten-signal bar open, in minutes past ET midnight. 15-minute chart:
// 16:00 -> fills 16:15, worst-case stamp 16:30 (deadline 16:45)
// 12:15 -> fills 12:30, worst-case stamp 12:45 (deadline 12:59)
VENUE_FLAT_REGULAR = 16 * 60 + 0
VENUE_FLAT_SHORT   = 12 * 60 + 15

// CME early-close dates as YYYYMMDD, comma-delimited with leading and
// trailing commas so a lookup can never match a partial token.
// Generated — see ops/calendars/cme_holiday_calendar.json. Do not hand-edit.
var string VENUE_EARLY_CLOSE = ",<<< PASTE THE GENERATED LIST HERE >>>,"

venueYmd = year(time, VENUE_TZ) * 10000 + month(time, VENUE_TZ) * 100 + dayofmonth(time, VENUE_TZ)
venueIsShortDay = str.contains(VENUE_EARLY_CLOSE, "," + str.tostring(venueYmd) + ",")
venueBarOpenMin = hour(time, VENUE_TZ) * 60 + minute(time, VENUE_TZ)
venueFlatFrom   = venueIsShortDay ? VENUE_FLAT_SHORT : VENUE_FLAT_REGULAR
venueAtOrPastFlat = venueBarOpenMin >= venueFlatFrom

// (a) no new entry on the flatten bar or later — otherwise the guard would
//     manufacture zero-duration trades it immediately closes.
venueEntryBlocked = venueAtOrPastFlat

// (b) forced flatten.
if venueAtOrPastFlat and strategy.position_size != 0
    strategy.close_all(comment = "VENUE_FLAT")
// ──────────────────────────────────────────────────────────────────────────
```

Then guard **every** entry call the strategy already makes, adding the one clause and changing nothing else:

```pine
// before
if longSignal
    strategy.entry("L", strategy.long)

// after
if longSignal and not venueEntryBlocked
    strategy.entry("L", strategy.long)
```

Pyramiding add-ons are entries too — guard those as well. Exits, stops, targets, trails and break-even
logic are **not** guarded and **not** touched: they must remain free to fire before the flatten.

**Timezone note.** `hour(time, VENUE_TZ)` resolves the bar to New York wall-clock and follows US daylight
saving automatically. If a strategy currently derives its session from a fixed UTC offset or from exchange
time, that is precisely the bug this replaces — do not preserve it.

---

## §3 — Per-strategy application

| | `orb_mnq_recon_v7` | `vanguard_mgc_v04` | `aegis_6j1` |
|---|---|---|---|
| Instrument / chart | MNQ1! | MGC1! | 6J1! |
| Declared session today | `09:15-16:55` ET | `09:00-16:59` ET | `10:00-13:45` ET, Mon–Wed, flatten 16:30 ET |
| Deadline-spanning trades | 310 / 681 | 226 / 343 | 9 / 122 |
| Nature of the defect | session runs **10 min past** 16:45 | session runs **14 min past** 16:45 | session ends 3 h before the deadline yet 9 trades still span it |
| Edit | paste §2, guard entries | paste §2, guard entries | paste §2, guard entries, **and delete the existing 16:30 flatten** so there is one guard, not two |
| Also expected to clear | 3 Friday→Sunday holds | — | — |

**On Aegis.** Its declared session closes at 13:45 ET and its Pine already declares a 16:30 ET flatten, so
no trade should approach 16:45 at all. Nine do. The most likely cause is that the existing flatten is
computed in a fixed offset or in exchange time rather than New York wall-clock, so it lands an hour late
during part of the year. Replacing it with the §2 block fixes that class of bug by construction. Please
check the old flatten's timezone handling before deleting it and tell me what it was — it is the one piece
of evidence that would confirm or refute the diagnosis, and it belongs in the lineage note.

**On ORB-MNQ's pyramiding.** `pine_pyramiding_pct` is 100, so the guard must sit on the add-on entries too,
or the flatten will close a position that a later bar re-opens.

---

## §4 — The venue-legal editions

Save each under a **new filename** — never edit a body in place under its old name.

| Superseded body | Venue-legal edition (new Pine filename) | New `strategy_id` |
|---|---|---|
| `orb_mnq_7_reconstruction.pine` | `orb_mnq_7_reconstruction_venue_bound.pine` | `orb_mnq_recon_v7_venue_bound` |
| `Vanguard_Gold_MGC_v0.4.pine` | `Vanguard_Gold_MGC_v0.4_venue_bound.pine` | `vanguard_mgc_v04_venue_bound` |
| `aegis_6J1.pine` | `aegis_6J1_venue_bound.pine` | `aegis_6j1_venue_bound` |

Each new body is hash-pinned in `core/strategies/PORT_MANIFEST.sha256` under `core/strategies/candidates/`
with a provenance comment naming the superseded body, its pin, and the single change — the same shape
[#286](https://github.com/Joshua-Asante/first-passage/pull/286) used for the two Striker research variants.

---

## §5 — Re-export settings, which must not drift

Hold every one of these identical to the superseded export, or the replacement is not comparable:

- **Date range** `Sep 1, 2022 — Sep 2, 2026`, DEEP backtest.
- **Chart** the same continuous symbol (`MNQ1!`, `MGC1!`, `6J1!`) and the same 15-minute timeframe.
- **Initial capital** the same figure the superseded export used — MGC and ORB-MNQ ran at **100K**, so keep
  100K. ⚠ See the note in §6 about the Strikers.
- **Commission and slippage** unchanged: ORB-MNQ `$0.91`/side and 1 tick; MGC `$1.06`/side and 3 ticks;
  Aegis `$1.30`/side and 1 tick, which is the figure its Pine declares.
- **Pyramiding** unchanged: ORB-MNQ 100, MGC 80, Aegis 0.
- **Chart timezone** `America/New_York`, as ruled in D9.
- **Bar detalization** stays on **Default** (4 OHLC ticks), exactly as the supplied panels show. Switching to
  `High` pulls a lower timeframe for intrabar fills and would change the fills themselves, which is a different
  measurement, not a re-expression.
- **DEEP** backtest stays on. Regular mode trims at 9,000 trades; Deep holds up to 1M.

Then send me, per strategy: the export CSV, the new Pine file, and the **Performance Summary** screenshot
including the commission and monthly rows.

---

## §6 — Verification, before you send anything

1. In the Strategy Tester's trade list, sort by exit time and confirm **no exit is stamped at or after
   16:45 ET**, and none at or after 12:59 ET on an early-close date.
2. Confirm no position is carried across a weekend.
3. Confirm the trade count *fell* relative to the superseded export. If it rose, the guard is blocking
   exits rather than entries and has been pasted in the wrong place.
4. Diff the new Pine against the superseded body and confirm the only changes are the §2 block, the
   `and not venueEntryBlocked` clauses, and — for Aegis only — the deleted old flatten.

⚠ **A separate finding, not part of this edit.** The two Striker exports were produced at **200K** initial
capital while the campaign targets a **$100K** Select account. That does not affect the three strategies in
this spec, and I am not asking you to change it here, but it means the Striker exports' position sizes are
not the sizes a 100K account would produce. I have raised it in the campaign-state artifact as its own
decision item; it will need its own ruling before Phase 2.

---

## §7 — One convention deliberately not adopted, and why

The repo's Pine skill carries the **config-fingerprint convention**
([ADR 2026-06-11](../../adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md), proposal P3): active-derivation
strategy scripts embed a `[cfgNN]` tag in the strategy title so an export filename self-identifies its
configuration, and existing scripts adopt "at their next legitimate edit" — which this edit is.

**These three editions do not adopt it**, on the convention's own stated exemption for frozen and pre-registered
scripts, whose "exports are identified by the pre-registration itself". This campaign pins **both** the Pine body
and the export by SHA-256 in `phase1_config.json` and verifies them at load, which is strictly stronger than a
title tag: a tag catches a mislabeled export, a hash catches any altered byte. Adopting the tag would also change
each strategy's title, hence its export filename, hence a field the frozen config already pins — churning the
freeze to gain a weaker check.

Flagging it rather than deciding silently: if the operator wants the tag adopted anyway, say so **before** the
re-export, because it changes the export filenames that get pinned.
