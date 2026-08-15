# NOTES — HARV-2026-001 Wave 1 (data assembly, roll rule, hygiene)

**Executor pickup:** 2026-07-12 (continues cfb2daa). Env: `.venv-research`
(databento 0.81.0, numpy 2.4.6, pandas 2.3.3, pyarrow 25.0.0). `DATABENTO_API_KEY`
present. All pulls via `.claude/skills/databento-data/scripts/db_fetch.py`
(estimate-gated); **no bare `timeseries.get_range`** in analysis code (audit hook 4).

## Databento scope + spend

- Schema `ohlcv-1d`, `--stype continuous`, symbols ES.c.0 / YM.c.0 / ZN.c.0 / GC.c.0
  (parents, 2010-06-06→2026-07-01) and MES.c.0 / MYM.c.0 (micros, 2019-05-06→2026-07-01).
- **Every daily-bar chunk estimates at $0.0000 USD** (billable ≈ 2–18 KB, ~180–310
  records/yr). Hard ceiling `--max-cost 1.00` per chunk, never approached. Total
  incremental Wave-1 spend ≈ **$0** (metadata dry-runs are free; the global
  `~/.databento_cache` re-serves prior pulls with no re-billing).
- Assembly driver: `assemble_panels.py` (yearly cost-gated chunks → `_yr_*.parquet`
  → concatenated `parents_ohlcv_1d.parquet` / `micros_ohlcv_1d.parquet`). It
  supersedes the ad-hoc `chunked_pull.py` / `pull_missing.py` /
  `pull_yearly_remaining.py` / `concat_parts.py` set (kept for provenance).
  Full-range single-request pulls stalled (long streaming; concurrent orphaned
  requests rate-limited each other) — yearly chunks complete in seconds each.

## Roll rule (databento Rule 3 — CONFIRMED, load-bearing)

- `.c.0` = **calendar roll (`c`), front-month (rank 0), UNADJUSTED** (raw
  front-month price with a discontinuity at each roll). Confirmed empirically:
  ES.c.0 daily closes 2024-03-15 (5116.25, ESH4 expiry Fri) → 2024-03-17 (5185.75,
  ESM4) = **+1.35% (+69.5 pt) phantom jump** over the roll weekend, no market move —
  the ESH4→ESM4 calendar spread. Definition-schema estimate for ES.c.0 confirms
  point-in-time specs available; the level jump is the decisive evidence.
- **Contamination geometry (matches frozen §4 pre-registration):** ES/YM/ZN roll
  quarterly (3rd-Fri expiry, mid-month); GC rolls in even delivery months. The
  **primary window close(T-3)→close(T-1)** is the last 3 trade dates of the month —
  the mid-month roll does NOT fall in it, so the primary window is roll-clean.
  **R_spread** spans last-month-T-1 → this-month-T-4 (≈ a full month) and therefore
  CONTAINS the mid-month roll for quarter-end months (Mar/Jun/Sep/Dec) — a ~135 bp
  phantom vs the 100 bp qualification threshold is material and can flip
  qualification/sign for those months on BOTH the ES and ZN legs.
- **Frozen handling (do not change):** §4 gates the POOLED panel; the
  `quarter_end` flag + ex-quarter-end split are reported as a **diagnostic only**
  (`diagnostics.py`), never a rescue or selection axis. Surface any
  pooled-vs-ex-quarter-end divergence in the §7 consolidated read.

## Trading-day calendar (§0.5 #3) — data-derived, not exchange_calendars

G1 suggested `exchange_calendars` `CMES` else a hard-coded CME holiday set. The
harness instead derives trading days from the **bars actually present** in the
ohlcv-1d feed (`trading_days_in_month` = dates with a bar). This is a *stronger*
match to the frozen "CME trading day" definition than any external calendar,
because the days used for offset counting are exactly the days that carry the
returns — no calendar/data mismatch, holidays/half-days handled by presence.
Verified by Step-0's n_trading_days ∈ [15,25] census.

### Data-hygiene fix (Sunday-bar contamination) — FIXED 2026-07-12

Databento GLBX `ohlcv-1d` buckets by **UTC calendar day**, so the Sunday-evening
Globex reopen (Sun 18:00 ET) lands in its own thin bar whose derived `settle_date`
is a **Sunday** (e.g. a March-2024 sample had 7 Sunday bars in 38; the harness's
month-end T-1 for March-2024 resolved to **Sun 2024-03-31** instead of the true
last CME equity trade date **Thu 2024-03-28** — Fri 03-29 was Good Friday). Left
in, these phantom weekend days shift every month-end T-k offset. **Fix:**
`load_symbol_frame` drops `settle_date` weekday > 4 (Sat/Sun); the real Monday
trade date is always carried by its own Monday bar, so nothing real is lost.
Regression test `test_load_symbol_frame_drops_weekend_bars` added (the pre-existing
synthetic tests use `bdate_range`, so they never exercised a weekend bar and passed
while the real-data path was wrong).

## Bar-print convention (§0.5 #4) — close print

ohlcv-1d bars are stamped `ts_event` = 00:00 UTC; each bar's window is ET ≈
[prev-day 19–20:00, this-day 19–20:00], so the daily **close is the last trade of
the UTC-day bar (≈19–20:00 ET), not the 16:00 ET equity settlement print**. Both
window endpoints use the same convention, so close(T-3)→close(T-1) is a consistent
2-day close-to-close return; the few-hour offset from the equity settle is a
disclosed, second-order approximation (it does not touch the frozen gate). The C
decomposition (open→close per session) inherits the same convention and is a
non-gating deployability annotation only.

## ES∩ZN ladder divergence (review finding 1) — verified negligible

`build_monthly_panel` builds the T-k ladder on `es.index ∩ zn.index`. Over the full
panel that intersection is essentially ES's own calendar: of 4163 ES weekday trade
dates, only **3 are ES-only** (ZN missing a bar where ES has one — the sole
ladder-shift risk case): 2014-10-03 (early-month, does not touch T-1..T-13),
2020-02-28 and 2023-06-19 (month-end-adjacent → a 1-day offset shift in at most 2 of
163 qualifying months). 6 dates are ZN-only (benign — the intersection drops them from
the ES ladder, which is correct). Net effect on the pooled estimate: nil. Building the
ladder on `es.index` alone would be marginally more spec-faithful but changes ≤2 months
by 1 day and would not move the verdict; left as-is (frozen construction).

## Assembler note

`assemble_concurrent.py` (thread-pool, in-process db_fetch, single-symbol yearly,
MYM dropped — unused by `run_harv0`) replaced the sequential subprocess assembler:
databento's per-request overhead (python startup + `import databento` + 4 metadata
round-trips ≈ 15 s even on a cache hit) and its stalls on large/multi-symbol requests
made "one process + concurrency + small reliable requests" the fast, reliable pattern.

## Hashes / provenance

- `parents_ohlcv_1d.parquet` sha256: `f096b116aab62c02a8071179d92d6c4aac2a032a63e43f3eb2eda4d9283e9f8e`
  (ES 4984 / YM 4988 / ZN 4943 / GC 4360 raw bars pre weekend-drop; 2010-06-07→2026-06-30)
- `micros_ohlcv_1d.parquet` sha256: `db83cb82b3f39ee38fe9093f6a3cbc721c44c96ae5f465a923a9e0792b86091b`
  (MES 2229 raw bars; 2019-05-06→2026-06-30)
- Panel: **192 months** (2010-07→2026-06), **163 qualifying** (trade rate 84.9%).
- Verdict: **AMBIGUOUS** (P-placebo magnitude clause); H1 +19.21 bp, perm-p 0.0129;
  DEPLOYABLE-DEFAULT-ENVELOPE **YES**. See RESULTS.md / results.json / diagnostics.json.
