# Third-leg Stage 2 -- measured sigma surfaces and tau_max

**Status:** **ACTIVE** -- 4 of 4 survivors measured on the ex-FOMC primary surface; cache coverage is 100% for every survivor's own IS window
> ⚠ **Slot-1 primary surface — F2 dependency (claim-alignment C31 / O-B).**
> The Slot-1 (`wed_thu`) restriction is derived from incumbent occupancy of a **deployed**
> two-leg book. Both legs were withdrawn 2026-08-04; per `ops/instruments/MYM.md` (2026-08-04)
> the symbols are **not thereby released** — that is fork **F2** (2026-08-08), so **until F2
> is ruled the primary surface still governs.**
>
> **If F2 releases them, what re-derives** (named, not resolved here): the wider `all_days`
> surface already measured below (N=450), the 0.0924 operational Clause-N floor, and the
> M6A COST→POWER flip. **No measurement cell edited.**



**Verdict:** `BAND NON-EMPTY (STAGE-2 — τ_max MEASURED on the ex-FOMC primary; mechanism-expressibility UNEVALUATED) -- largest measured tau_max 360min @ 10:30 (MYM) (capped at grid max -- true tau_max may exceed this) [tied across 7 (symbol, start) cells]`

**PRIMARY SURFACE: `wed_thu` EXCLUDING the pinned FOMC sessions.** A third leg would skip FOMC Wednesdays, so the operational surface is the one without them, and **tau_max, the joint table, the verdict, the sqrt-t diagnostic, the roll-span check and the binding-cell SE all read from it**. **Measured basis:** the worst announcement-day cell BREACHES the $125.00 ceiling on 3 of 4 measured survivors (MYM, M2K, MCL) -- see each instrument's FOMC-Wednesday section for the cell and its n.

**CONTEXT (demoted):** pooled `wed_thu` (announcement sessions included) and `all_days`. Both are still rendered per instrument -- the primary is defined by subtracting from the first of them, and a subtraction whose minuend is hidden cannot be audited -- but neither governs, and no tau_max may be lifted from either.

**EVIDENCE (retained):** the `fomc_only` surface and the pooled-pass/FOMC-breach ceiling-flip analysis. These are the reason the exclusion is the operational choice; they do not stop mattering because the baseline moved.

**The exclusion is not free, and both costs are computed below, not asserted:** it raises the Clause-N power floor on every instrument (§Cost 1) and it can LOWER tau_max where the announcement sessions were damping a cell rather than inflating it (§Cost 2).

`FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

**Reading the verdict token.** Design §5.1.1 pre-registers the unqualified `BAND NON-EMPTY` on "≥1 survivor whose τ_max is large enough to **host an expressible mechanism**". Stage 2 measured τ_max and **did not evaluate mechanism-expressibility** -- no mechanism has been proposed here, let alone shown to fit inside a measured window -- so the unqualified token stays **reserved**, exactly as Stage 1 reserved it for a different missing half. The parenthetical states the substitution on its face. The earlier `STAGE-2 VIABLE` wording is withdrawn: it withheld the token while asserting the withheld claim in plain English, since "viable" *is* a hosting claim.

**Basis:** daily-$ per contract at the $100K Tradeify Select basis (sigma ceiling **$125.00**/contract/day). Reuses the Stage-1 survivor set (MYM, M2K, MCL, M6A) unchanged.

**Re-runnable by design.** This script re-checks cache coverage on every invocation via `cache_coverage.coverage()` against each survivor's own `stage2_windows.is_window`. A symbol short of 100% coverage is reported PENDING here and contributes NOTHING to any sigma computation -- a panel missing months is a biased sample, not a smaller one, and is never silently presented as the instrument's sigma. Re-run after the background pull advances; no edits needed.

## Cost 1 of the exclusion: statistical POWER

Skipping FOMC Wednesdays removes tradeable sessions, and N is in the denominator of the Clause-N floor `1.96/sqrt(N)` -- the minimum detectable `d/s` at power 0.50. **Fewer sessions => a HIGHER bar for any future edge test.** The operational floor below is computed from each instrument's **measured** ex-FOMC session count (the pooled wed_thu dates in its own panel, minus the pinned announcement dates that fall in them) -- never from a theoretical 8 meetings/yr. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

**Scope guard.** `instrument_map.PANELS` and the Stage-1 flags are deliberately UNCHANGED. Stage 1 is a separately-reviewed artifact reporting the pooled-panel geometry and is correct on its own terms; Stage 2 reports the floor a third leg would actually face and names the divergence. Where the two disagree, both are printed.

| Symbol | Stage-1 N (pooled panel) | Stage-1 floor | measured pooled `wed_thu` | FOMC sessions dropped | ex-FOMC N | ex-FOMC floor | floor change | cost-tax (1t, r=1) | binds first: Stage-1 -> Stage-2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| MYM | 484 | 0.0891 | 486 | 36 | 450 | 0.0924 | +3.7% | 0.0742 | POWER -> POWER |
| M2K | 484 | 0.0891 | 486 | 36 | 450 | 0.0924 | +3.7% | 0.0742 | POWER -> POWER |
| MCL | 251 | 0.1237 | 252 | 19 | 233 | 0.1284 | +3.8% | 0.0902 | POWER -> POWER |
| M6A | 484 | 0.0891 | 486 | 36 | 450 | 0.0924 | +3.7% | 0.0902 | COST -> POWER **FLIP** |

**The operational floor is higher on all 4 measured instruments** -- exclusion costs power everywhere, with no offsetting instrument. MYM 0.0891 -> 0.0924 (+3.7%, N 484 -> 450); M2K 0.0891 -> 0.0924 (+3.7%, N 484 -> 450); MCL 0.1237 -> 0.1284 (+3.8%, N 251 -> 233); M6A 0.0891 -> 0.0924 (+3.7%, N 484 -> 450).

**1 of 4 re-scored rows FLIP their binding constraint.** **M6A: COST -> POWER.** Its cost-tax 0.0902 is > the Stage-1 floor 0.0891 but < the ex-FOMC floor 0.0924. Stage 1's own flag on such a row is not wrong -- it is correct for the pooled panel it describes. It is simply not the constraint that binds a leg which skips announcement days.

The two N columns do not agree by construction and are not meant to. Stage-1 N is calendar arithmetic (`panel_sessions`: days from the row's own sourced `panel_start` to the reserved-IS boundary, at 104 Slot-1 sessions/yr); the measured pooled count is the Wed/Thu dates actually present in the pulled panel. The ex-FOMC floor is built on the **measured** side, because that is the side that knows which sessions exist.

A power floor is a statement about what a future test could DETECT. It admits nothing, and no return-predictive statistic was computed here to compare against it.

## Cost 2 of the exclusion: tau_max, per symbol

Exclusion moves tau_max at 1 of 4 measured instruments: **1 cell(s) LOSE tau_max** (MCL). **A loss means the pooled cell was clearing the ceiling only because the announcement sessions in it were CALMER than the instrument's ordinary Wed/Thu behaviour and were dragging the pooled std down** -- so exclusion is a risk-control choice, not an unalloyed improvement.

- **MYM: no start time's tau_max changes** -- the primary and pooled rows are identical at every start, so on this instrument the exclusion costs power only.
- **M2K: no start time's tau_max changes** -- the primary and pooled rows are identical at every start, so on this instrument the exclusion costs power only.
- **MCL @ 09:30: 180min pooled -> 120min primary (SHORTER)** -- at 180min the sigma pair is pooled $124.67 vs primary $125.59 (ceiling $125.00), i.e. the excluded announcement sessions were DAMPING that cell and the pooled reading does not survive their removal -- **this instrument pays for the exclusion in tau_max as well as in power**.
- **M6A: no start time's tau_max changes** -- the primary and pooled rows are identical at every start, so on this instrument the exclusion costs power only.

Stated plainly: **excluding FOMC Wednesdays costs statistical power on EVERY measured instrument, and where it moves tau_max at all it can cost that too. It is a risk-control choice made because the announcement-day sigma is not survivable at this ceiling, not because the ex-FOMC surface is better.** `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

## Measured survivors

**Cache coverage across the measured survivors: 197/197 chunks held (100%).** The schema behind every one of those chunks is `ohlcv-1m` on GLBX.MDP3, which dry-ran at **$0.00** when probed -- see RESULTS.md Phase B for the probes themselves (a whole-window MYM estimate plus per-symbol chunk probes), which is what was measured; no per-chunk re-quote was taken at pull time. The coverage figure above is re-derived from `cache_coverage.coverage()` on every run, per symbol, against that symbol's own `stage2_windows.is_window` -- it is not a recorded number.

### MYM

Point value **$0.5000**/pt (derived, `tick_value_usd / tick_size`) - 1594297 1m bars, 19 detected rolls, span 2019-05-05 20:00:00-04:00 -> 2023-12-29 16:59:00-05:00.

Cache coverage for its own IS window: **56/56 chunks** (100% -- the gate this section sits behind; a symbol short of it is reported PENDING and measured nowhere).

#### sigma surface -- **PRIMARY: `wed_thu` EXCLUDING the pinned FOMC sessions** (Slot 1, incumbent legs cannot fire, full 80-contract cap is free)

**Operational surface.** A third leg would skip FOMC Wednesdays, so the 36 pinned announcement sessions are removed BEFORE the surface is measured: 486 pooled `wed_thu` sessions -> **450** tradeable. That subtraction is the whole point of this table, and it costs power -- see the operational power floor in the joint table. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $38.51 (n=447) | $49.33 (n=447) | $57.54 (n=448) | $63.71 (n=448) | $71.04 (n=448) | $81.70 (n=448) | $92.45 (n=448) | $104.57 (n=439) | $127.86 (n=439) |
| 10:00 | $33.15 (n=447) | $42.71 (n=447) | $47.74 (n=447) | $53.90 (n=447) | $67.82 (n=447) | $76.51 (n=447) | $89.79 (n=440) | $103.20 (n=439) | $126.43 (n=439) |
| 10:30 | $26.25 (n=448) | $36.80 (n=448) | $46.54 (n=448) | $52.03 (n=448) | $63.92 (n=448) | $72.36 (n=448) | $89.19 (n=439) | $99.70 (n=439) | $119.44 (n=438) |
| 11:00 | $25.51 (n=448) | $34.85 (n=448) | $41.46 (n=448) | $47.90 (n=448) | $56.43 (n=448) | $65.83 (n=440) | $82.08 (n=439) | $94.42 (n=439) | n/a (past 16:45 flat) |
| 12:00 | $22.75 (n=448) | $29.43 (n=448) | $38.11 (n=448) | $43.88 (n=440) | $58.73 (n=439) | $63.88 (n=439) | $76.39 (n=439) | $93.37 (n=439) | n/a (past 16:45 flat) |
| 13:00 | $21.87 (n=438) | $29.84 (n=438) | $37.18 (n=438) | $41.88 (n=438) | $54.53 (n=438) | $63.41 (n=438) | $86.70 (n=438) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $21.85 (n=439) | $31.65 (n=439) | $38.82 (n=439) | $44.64 (n=439) | $56.69 (n=439) | $74.94 (n=439) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $22.64 (n=439) | $31.03 (n=439) | $36.56 (n=439) | $53.81 (n=439) | $57.54 (n=437) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 450 `wed_thu ex-FOMC` sessions in this instrument's panel; best-supported cell 448.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 450 -> 448 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 448 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

**tau_max (PRIMARY -- wed_thu ex-FOMC, `sigma <= $125.00` ceiling). This is the row the joint table and the verdict read:**

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 240 | 240 | 360 | 240 | 240 | 180 | 120 | 90 |

#### Context surfaces (DEMOTED -- do not lift a tau_max from here)

Both tables below include sessions the primary excludes, or days Slot 1 does not trade. They are kept because the primary is defined by subtraction from the first of them, and a reader cannot audit a subtraction whose minuend is hidden.

sigma surface -- pooled `wed_thu` (FOMC sessions INCLUDED; context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $38.11 (n=483) | $48.53 (n=483) | $56.59 (n=484) | $62.40 (n=484) | $69.61 (n=484) | $79.58 (n=484) | $89.72 (n=484) | $101.27 (n=475) | $128.07 (n=475) |
| 10:00 | $32.68 (n=483) | $42.53 (n=483) | $47.65 (n=483) | $53.47 (n=483) | $66.20 (n=483) | $74.26 (n=483) | $87.30 (n=476) | $100.76 (n=475) | $128.81 (n=475) |
| 10:30 | $25.77 (n=484) | $35.99 (n=484) | $45.69 (n=484) | $50.97 (n=484) | $62.31 (n=484) | $70.51 (n=484) | $86.52 (n=475) | $99.71 (n=475) | $121.79 (n=474) |
| 11:00 | $25.15 (n=484) | $34.22 (n=484) | $40.60 (n=484) | $46.83 (n=484) | $55.18 (n=484) | $64.07 (n=476) | $80.41 (n=475) | $95.05 (n=475) | n/a (past 16:45 flat) |
| 12:00 | $22.17 (n=484) | $28.81 (n=484) | $37.18 (n=484) | $42.91 (n=476) | $57.05 (n=475) | $63.21 (n=475) | $78.81 (n=475) | $98.94 (n=475) | n/a (past 16:45 flat) |
| 13:00 | $21.38 (n=474) | $29.04 (n=474) | $36.22 (n=474) | $42.43 (n=474) | $56.78 (n=474) | $66.89 (n=474) | $92.47 (n=474) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $25.04 (n=475) | $34.41 (n=475) | $43.95 (n=475) | $50.11 (n=475) | $65.04 (n=475) | $82.37 (n=475) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $25.19 (n=475) | $35.28 (n=475) | $41.36 (n=475) | $58.44 (n=475) | $61.87 (n=473) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 486 `wed_thu (pooled)` sessions in this instrument's panel; best-supported cell 484.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 486 -> 484 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 484 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

tau_max (pooled `wed_thu`, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 240 | 240 | 360 | 240 | 240 | 180 | 120 | 90 |

sigma surface -- `all_days` (context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $42.09 (n=1200) ! | $51.91 (n=1201) ! | $59.63 (n=1201) ! | $65.02 (n=1201) ! | $74.52 (n=1200) ! | $83.70 (n=1200) ! | $91.97 (n=1201) ! | $100.94 (n=1158) ! | $120.91 (n=1160) ! |
| 10:00 | $32.61 (n=1200) ! | $43.59 (n=1200) ! | $51.28 (n=1198) ! | $56.95 (n=1199) ! | $70.38 (n=1199) ! | $75.18 (n=1199) ! | $85.75 (n=1167) ! | $97.20 (n=1160) ! | $123.24 (n=1161) ! |
| 10:30 | $26.31 (n=1199) ! | $36.87 (n=1200) ! | $45.55 (n=1199) ! | $52.95 (n=1200) ! | $59.48 (n=1200) ! | $66.77 (n=1201) ! | $78.85 (n=1158) ! | $91.76 (n=1160) ! | $112.68 (n=1158) ! |
| 11:00 | $26.62 (n=1198) ! | $36.85 (n=1199) ! | $41.99 (n=1200) ! | $46.37 (n=1199) ! | $55.20 (n=1200) ! | $62.07 (n=1166) ! | $76.13 (n=1159) ! | $88.11 (n=1160) ! | n/a (past 16:45 flat) |
| 12:00 | $22.65 (n=1198) ! | $28.55 (n=1200) ! | $35.97 (n=1199) ! | $41.39 (n=1167) ! | $53.33 (n=1158) ! | $59.40 (n=1160) ! | $72.35 (n=1161) ! | $95.73 (n=1161) ! | n/a (past 16:45 flat) |
| 13:00 | $20.62 (n=1155) ! | $29.80 (n=1156) ! | $35.80 (n=1157) ! | $42.27 (n=1158) ! | $52.93 (n=1157) ! | $60.80 (n=1158) ! | $87.69 (n=1158) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $22.36 (n=1158) ! | $31.40 (n=1159) ! | $38.33 (n=1158) ! | $44.71 (n=1160) ! | $56.52 (n=1159) ! | $76.57 (n=1160) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $23.26 (n=1160) ! | $33.59 (n=1160) ! | $41.05 (n=1160) ! | $59.34 (n=1161) ! | $60.74 (n=1157) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 1449 `all_days` sessions in this instrument's panel; best-supported cell 1201.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 1449 -> 1201 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 1201 is (b). **61 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

tau_max (all_days, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

Against `wed_thu (pooled)`: the two tau_max rows agree at every start time. Against `all_days`: **that context row is the FLATTERING one** -- the primary is strictly TIGHTER at 2 start(s) (09:30 240 vs 360min; 10:00 240 vs 360min), so lifting its tau_max would overstate what is tradeable. Slot 1 trades Wed+Thu and a third leg skips FOMC Wednesdays, so **the `wed_thu ex-FOMC` row is the one that governs** -- both context rows are shown for audit and must not be lifted in its place.

#### sqrt-t error -- how wrong a sqrt(t) extrapolation would have been

Computed on the **PRIMARY (wed_thu ex-FOMC)** surface, not the pooled context -- a sqrt-t verdict about a surface this book would not trade is a stale claim. Anchored on the shortest window (15min); **`predicted/measured - 1`, so POSITIVE = sqrt(t) OVERSTATES the measured sigma and NEGATIVE = sqrt(t) UNDERSTATES it.** This tests the design's own premise for refusing sqrt-t scaling in favour of direct measurement.

The sign is the operational content, and it is **mixed** across this surface -- so an unsigned |error| headline would hide the two opposite failure modes. Where sqrt-t **overstates**, a sqrt-t-based screen would have **wrongly rejected** holds that direct measurement shows are viable. Where it **understates**, that same screen would have **waved through** holds riskier than modelled. Full signed surface (the anchor column is 0 by construction):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | 0.0% (anchor) | +10.4% | +15.9% | +20.9% | +32.8% | +33.3% | +44.3% | +47.3% | +47.6% |
| 10:00 | 0.0% (anchor) | +9.8% | +20.3% | +23.0% | +19.7% | +22.5% | +27.9% | +28.5% | +28.4% |
| 10:30 | 0.0% (anchor) | +0.9% | -2.3% | +0.9% | +0.6% | +2.6% | +1.9% | +5.3% | +7.7% |
| 11:00 | 0.0% (anchor) | +3.5% | +6.6% | +6.5% | +10.7% | +9.6% | +7.7% | +8.1% | n/a (past 16:45 flat) |
| 12:00 | 0.0% (anchor) | +9.3% | +3.4% | +3.7% | -5.1% | +0.7% | +3.1% | -2.6% | n/a (past 16:45 flat) |
| 13:00 | 0.0% (anchor) | +3.7% | +1.9% | +4.4% | -1.8% | -2.4% | -12.6% | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | 0.0% (anchor) | -2.3% | -2.5% | -2.1% | -5.6% | -17.5% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | 0.0% (anchor) | +3.2% | +7.3% | -15.8% | -3.6% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Max OVERSTATEMENT (PRIMARY, wed_thu ex-FOMC): +47.6%** at start=09:30, duration=360min -- sqrt(t) predicts a sigma this much LARGER than measured, so a sqrt-t screen would have **wrongly rejected** this hold as too risky when the measurement says it is not.
**Max UNDERSTATEMENT (PRIMARY, wed_thu ex-FOMC): -17.5%** at start=14:00, duration=120min -- sqrt(t) predicts a sigma this much SMALLER than measured, so a sqrt-t screen would have waved this hold through at a risk level the measurement does not support. **This is the dangerous direction.**

#### FOMC-Wednesday hazard -- the EVIDENCE for excluding these sessions from the primary

Slot 1 is Wed+Thu and FOMC lands on Wednesday afternoons ~8x/yr. This instrument's pooled `wed_thu` session set contains **36 pinned FOMC dates**, and the primary surface above is exactly that set with these removed. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote. Both conditionals below are **measured directly** on their own day sets, not backed out of the pooled variance algebraically. This section is retained in full: it is the reason the exclusion is the operational choice, and it does not stop being load-bearing because the baseline moved.

tau_max, PRIMARY (FOMC excluded) against the pooled context row:

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max PRIMARY (min) | 240 | 240 | 360 | 240 | 240 | 180 | 120 | 90 |
| tau_max pooled, context (min) | 240 | 240 | 360 | 240 | 240 | 180 | 120 | 90 |

**The primary and pooled tau_max rows are identical on this instrument, and that does NOT mean FOMC is harmless here.** tau_max is also a *clipped* statistic: the afternoon starts bracketing the 14:00 ET announcement are already short-capped by the 16:45 flat deadline (14:00 caps at 120min, 15:00 caps at 90min), so their tau_max cannot register an increase in sigma unless that sigma breaches the $125.00 ceiling outright. Read the sigma tables below, not the tau_max row, for the FOMC hazard.

sigma surface -- **`fomc_only`** (announcement days only -- the sessions the primary DROPS; note the much smaller n per cell):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $33.10 (n=36) | $37.74 (n=36) | $43.59 (n=36) | $43.54 (n=36) | $49.22 (n=36) | $46.37 (n=36) | $44.03 (n=36) | $45.17 (n=36) | $132.16 (n=36) |
| 10:00 | $26.35 (n=36) | $40.82 (n=36) | $47.03 (n=36) | $48.47 (n=36) | $41.71 (n=36) | $36.73 (n=36) | $48.00 (n=36) | $64.86 (n=36) | $156.93 (n=36) |
| 10:30 | $18.19 (n=36) | $23.79 (n=36) | $33.44 (n=36) | $35.67 (n=36) | $37.40 (n=36) | $41.58 (n=36) | $42.20 (n=36) | $100.30 (n=36) | $149.28 (n=36) |
| 11:00 | $20.44 (n=36) | $25.54 (n=36) | $27.87 (n=36) | $30.82 (n=36) | $36.73 (n=36) | $36.66 (n=36) | $57.05 (n=36) | $103.53 (n=36) | n/a (past 16:45 flat) |
| 12:00 | $13.18 (n=36) | $19.85 (n=36) | $22.84 (n=36) | $28.63 (n=36) | $29.50 (n=36) | $55.08 (n=36) | $105.12 (n=36) | $153.08 (n=36) | n/a (past 16:45 flat) |
| 13:00 | $14.26 (n=36) | $16.50 (n=36) | $21.76 (n=36) | $49.29 (n=36) | $79.74 (n=36) | $100.77 (n=36) | $147.32 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $50.13 (n=36) | $58.48 (n=36) | $83.76 (n=36) | $94.75 (n=36) | $130.20 (n=36) | $146.95 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $46.66 (n=36) | $69.31 (n=36) | $80.04 (n=36) | $99.31 (n=36) | $101.01 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

sigma delta (pooled minus PRIMARY; positive = the excluded FOMC days were ADDING to sigma, negative = they were DAMPING it):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | -0.40 | -0.80 | -0.95 | -1.30 | -1.43 | -2.12 | -2.72 | -3.30 | +0.22 |
| 10:00 | -0.47 | -0.18 | -0.09 | -0.43 | -1.62 | -2.25 | -2.48 | -2.44 | +2.38 |
| 10:30 | -0.47 | -0.81 | -0.86 | -1.06 | -1.61 | -1.85 | -2.67 | +0.01 | +2.35 |
| 11:00 | -0.36 | -0.62 | -0.86 | -1.08 | -1.25 | -1.76 | -1.67 | +0.63 | n/a (past 16:45 flat) |
| 12:00 | -0.58 | -0.62 | -0.94 | -0.97 | -1.69 | -0.67 | +2.42 | +5.57 | n/a (past 16:45 flat) |
| 13:00 | -0.49 | -0.80 | -0.96 | +0.55 | +2.25 | +3.47 | +5.77 | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | +3.19 | +2.77 | +5.13 | +5.47 | +8.36 | +7.43 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | +2.55 | +4.25 | +4.80 | +4.64 | +4.33 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Worst measured FOMC-day cell: $156.93 at start=10:00, duration=360min (n=36 announcement sessions) -- 126% of the $125.00 ceiling.** That cell **BREACHES** the $125.00 ceiling on announcement days, by 26%. Pooled sigma at the same cell is **$128.81** (n=475, which itself BREACHES the ceiling) -- FOMC days **RAISED** sigma at that cell (1.22x).
**5 cell(s) PASS the ceiling pooled but BREACH it on announcement days** -- worst: 12:00/240min (pooled $98.94 -> FOMC $153.08); 10:30/360min (pooled $121.79 -> FOMC $149.28); 13:00/180min (pooled $92.47 -> FOMC $147.32). This is the decision-relevant form of the hazard and the direct argument for excluding these sessions: a pooled tau_max certifies those durations as usable while the announcement-day conditional is over the ceiling. **The primary surface above already excludes them, so these cells are the hazard the exclusion removes, not a residual risk in the headline numbers.**
**Most elevated cells (fomc_only / PRIMARY sigma ratio -- how much an announcement day lifts a cell above the surface this book would actually trade):** 14:00/90min (2.30x: $130.20 vs $56.69, n=36); 14:00/15min (2.29x: $50.13 vs $21.85, n=36); 15:00/30min (2.23x: $69.31 vs $31.03, n=36).
**Weigh all of the above against its n.** The FOMC-only surface rests on 36 sessions in every cell (36 pinned FOMC dates fall in this instrument's pooled wed_thu session set), against n=475 at the same cell on the pooled context surface (10:00/360min) -- so each FOMC cell carries a correspondingly wider sampling error. It is a hazard flag, not a calibrated number. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

#### Roll-spanning check

**0** of the **27007** PRIMARY (wed_thu ex-FOMC) contributing (start, duration, session) windows span a detected roll (out of 19 rolls detected over the panel). Counted on the primary panel, not the pooled one -- the check exists to test whether back-adjustment is load-bearing for the sigma this artifact actually reports. Back-adjustment is therefore NOT doing any lifting for the reported within-day sigma: **no contributing measured window crossed a detected roll.** This is CHECKED on every run, not assumed. It is also all the count proves -- the grid's longest window ends at 16:30 ET, so a roll between then and the 16:45 flat deadline would be inside session hours and still uncounted, as would any roll on a session outside this day set. Those are unmeasured, not shown absent.

### M2K

Point value **$5.0000**/pt (derived, `tick_value_usd / tick_size`) - 1540356 1m bars, 19 detected rolls, span 2019-05-05 20:00:00-04:00 -> 2023-12-29 16:59:00-05:00.

Cache coverage for its own IS window: **56/56 chunks** (100% -- the gate this section sits behind; a symbol short of it is reported PENDING and measured nowhere).

#### sigma surface -- **PRIMARY: `wed_thu` EXCLUDING the pinned FOMC sessions** (Slot 1, incumbent legs cannot fire, full 80-contract cap is free)

**Operational surface.** A third leg would skip FOMC Wednesdays, so the 36 pinned announcement sessions are removed BEFORE the surface is measured: 486 pooled `wed_thu` sessions -> **450** tradeable. That subtraction is the whole point of this table, and it costs power -- see the operational power floor in the joint table. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $38.32 (n=447) | $51.01 (n=447) | $61.03 (n=446) | $66.29 (n=448) | $71.71 (n=447) | $79.57 (n=448) | $88.18 (n=448) | $94.00 (n=440) | $115.58 (n=440) |
| 10:00 | $31.05 (n=446) | $39.90 (n=447) | $47.09 (n=447) | $49.59 (n=447) | $59.93 (n=447) | $66.40 (n=447) | $76.34 (n=441) | $85.24 (n=440) | $108.49 (n=440) |
| 10:30 | $25.67 (n=448) | $33.37 (n=447) | $42.03 (n=448) | $45.67 (n=448) | $55.45 (n=448) | $61.65 (n=448) | $73.76 (n=440) | $81.89 (n=440) | $103.04 (n=432) |
| 11:00 | $23.69 (n=447) | $30.60 (n=447) | $35.80 (n=447) | $42.76 (n=447) | $49.84 (n=447) | $56.40 (n=441) | $68.18 (n=440) | $79.21 (n=440) | n/a (past 16:45 flat) |
| 12:00 | $19.16 (n=446) | $25.88 (n=448) | $32.79 (n=447) | $36.72 (n=441) | $46.25 (n=440) | $52.76 (n=440) | $63.88 (n=440) | $81.60 (n=440) | n/a (past 16:45 flat) |
| 13:00 | $18.46 (n=439) | $25.19 (n=439) | $31.54 (n=439) | $35.97 (n=439) | $47.48 (n=439) | $52.97 (n=439) | $72.26 (n=439) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $18.94 (n=440) | $27.87 (n=440) | $34.11 (n=439) | $38.06 (n=440) | $49.10 (n=440) | $60.97 (n=440) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $19.23 (n=440) | $27.81 (n=440) | $32.22 (n=440) | $41.74 (n=440) | $44.84 (n=432) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 450 `wed_thu ex-FOMC` sessions in this instrument's panel; best-supported cell 448.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 450 -> 448 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 448 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

**tau_max (PRIMARY -- wed_thu ex-FOMC, `sigma <= $125.00` ceiling). This is the row the joint table and the verdict read:**

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

#### Context surfaces (DEMOTED -- do not lift a tau_max from here)

Both tables below include sessions the primary excludes, or days Slot 1 does not trade. They are kept because the primary is defined by subtraction from the first of them, and a reader cannot audit a subtraction whose minuend is hidden.

sigma surface -- pooled `wed_thu` (FOMC sessions INCLUDED; context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $38.25 (n=483) | $50.75 (n=483) | $60.83 (n=482) | $66.44 (n=484) | $71.73 (n=483) | $79.31 (n=484) | $86.97 (n=484) | $93.14 (n=476) | $117.03 (n=476) |
| 10:00 | $30.64 (n=482) | $39.89 (n=483) | $46.73 (n=483) | $49.29 (n=483) | $58.98 (n=483) | $64.81 (n=483) | $74.73 (n=477) | $83.37 (n=476) | $112.21 (n=476) |
| 10:30 | $25.30 (n=484) | $32.91 (n=483) | $41.29 (n=484) | $44.86 (n=484) | $54.45 (n=484) | $60.23 (n=484) | $72.11 (n=476) | $82.14 (n=476) | $106.69 (n=468) |
| 11:00 | $23.43 (n=483) | $30.18 (n=483) | $35.30 (n=483) | $42.25 (n=483) | $48.96 (n=483) | $55.34 (n=477) | $66.69 (n=476) | $81.12 (n=476) | n/a (past 16:45 flat) |
| 12:00 | $18.85 (n=482) | $25.46 (n=484) | $32.35 (n=482) | $36.45 (n=477) | $45.56 (n=476) | $52.14 (n=476) | $67.20 (n=476) | $87.44 (n=476) | n/a (past 16:45 flat) |
| 13:00 | $18.05 (n=475) | $24.50 (n=475) | $30.66 (n=475) | $35.53 (n=475) | $49.34 (n=475) | $57.82 (n=475) | $79.43 (n=475) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $23.02 (n=476) | $31.18 (n=476) | $38.84 (n=475) | $44.99 (n=476) | $58.21 (n=476) | $70.01 (n=476) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $21.46 (n=476) | $31.22 (n=476) | $36.27 (n=476) | $45.92 (n=476) | $48.58 (n=468) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 486 `wed_thu (pooled)` sessions in this instrument's panel; best-supported cell 484.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 486 -> 484 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 484 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

tau_max (pooled `wed_thu`, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

sigma surface -- `all_days` (context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $40.87 (n=1199) ! | $52.86 (n=1201) ! | $60.45 (n=1199) ! | $65.79 (n=1201) ! | $74.46 (n=1197) ! | $80.42 (n=1197) ! | $87.70 (n=1197) ! | $93.91 (n=1159) ! | $110.08 (n=1160) ! |
| 10:00 | $30.14 (n=1200) ! | $40.40 (n=1201) ! | $48.70 (n=1199) ! | $52.19 (n=1198) ! | $60.68 (n=1197) ! | $65.95 (n=1195) ! | $74.25 (n=1167) ! | $81.58 (n=1160) ! | $101.92 (n=1162) ! |
| 10:30 | $26.02 (n=1200) ! | $35.70 (n=1198) ! | $42.90 (n=1199) ! | $47.21 (n=1198) ! | $54.17 (n=1196) ! | $59.26 (n=1198) ! | $68.15 (n=1160) ! | $76.84 (n=1158) ! | $93.28 (n=1143) ! |
| 11:00 | $24.08 (n=1198) ! | $31.50 (n=1196) ! | $36.95 (n=1197) ! | $41.85 (n=1194) ! | $48.22 (n=1195) ! | $53.79 (n=1167) ! | $63.88 (n=1160) ! | $73.50 (n=1162) ! | n/a (past 16:45 flat) |
| 12:00 | $19.22 (n=1191) ! | $25.43 (n=1194) ! | $31.88 (n=1191) ! | $35.70 (n=1164) ! | $43.40 (n=1158) ! | $49.29 (n=1158) ! | $60.34 (n=1159) ! | $76.89 (n=1159) ! | n/a (past 16:45 flat) |
| 13:00 | $17.32 (n=1156) ! | $24.60 (n=1156) ! | $30.10 (n=1157) ! | $35.33 (n=1156) ! | $44.14 (n=1156) ! | $50.90 (n=1158) ! | $69.20 (n=1158) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $19.82 (n=1159) ! | $27.57 (n=1156) ! | $32.65 (n=1158) ! | $38.09 (n=1160) ! | $47.73 (n=1160) ! | $60.05 (n=1160) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $18.74 (n=1161) ! | $27.03 (n=1161) ! | $32.28 (n=1160) ! | $43.49 (n=1162) ! | $44.46 (n=1143) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 1450 `all_days` sessions in this instrument's panel; best-supported cell 1201.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 1450 -> 1201 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 1201 is (b). **61 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

tau_max (all_days, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

Against `wed_thu (pooled)`: the two tau_max rows agree at every start time. Against `all_days`: the two tau_max rows agree at every start time. Slot 1 trades Wed+Thu and a third leg skips FOMC Wednesdays, so **the `wed_thu ex-FOMC` row is the one that governs** -- both context rows are shown for audit and must not be lifted in its place.

#### sqrt-t error -- how wrong a sqrt(t) extrapolation would have been

Computed on the **PRIMARY (wed_thu ex-FOMC)** surface, not the pooled context -- a sqrt-t verdict about a surface this book would not trade is a stale claim. Anchored on the shortest window (15min); **`predicted/measured - 1`, so POSITIVE = sqrt(t) OVERSTATES the measured sigma and NEGATIVE = sqrt(t) UNDERSTATES it.** This tests the design's own premise for refusing sqrt-t scaling in favour of direct measurement.

The sign is the operational content, and it is **mixed** across this surface -- so an unsigned |error| headline would hide the two opposite failure modes. Where sqrt-t **overstates**, a sqrt-t-based screen would have **wrongly rejected** holds that direct measurement shows are viable. Where it **understates**, that same screen would have **waved through** holds riskier than modelled. Full signed surface (the anchor column is 0 by construction):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | 0.0% (anchor) | +6.2% | +8.8% | +15.6% | +30.9% | +36.2% | +50.5% | +63.1% | +62.4% |
| 10:00 | 0.0% (anchor) | +10.1% | +14.2% | +25.2% | +26.9% | +32.3% | +40.9% | +45.7% | +40.2% |
| 10:30 | 0.0% (anchor) | +8.8% | +5.8% | +12.4% | +13.4% | +17.8% | +20.6% | +25.4% | +22.0% |
| 11:00 | 0.0% (anchor) | +9.5% | +14.6% | +10.8% | +16.4% | +18.8% | +20.4% | +19.6% | n/a (past 16:45 flat) |
| 12:00 | 0.0% (anchor) | +4.7% | +1.2% | +4.3% | +1.5% | +2.7% | +3.9% | -6.1% | n/a (past 16:45 flat) |
| 13:00 | 0.0% (anchor) | +3.6% | +1.3% | +2.6% | -4.8% | -1.4% | -11.5% | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | 0.0% (anchor) | -3.9% | -3.8% | -0.4% | -5.5% | -12.1% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | 0.0% (anchor) | -2.2% | +3.4% | -7.9% | +5.0% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Max OVERSTATEMENT (PRIMARY, wed_thu ex-FOMC): +63.1%** at start=09:30, duration=240min -- sqrt(t) predicts a sigma this much LARGER than measured, so a sqrt-t screen would have **wrongly rejected** this hold as too risky when the measurement says it is not.
**Max UNDERSTATEMENT (PRIMARY, wed_thu ex-FOMC): -12.1%** at start=14:00, duration=120min -- sqrt(t) predicts a sigma this much SMALLER than measured, so a sqrt-t screen would have waved this hold through at a risk level the measurement does not support. **This is the dangerous direction.**

#### FOMC-Wednesday hazard -- the EVIDENCE for excluding these sessions from the primary

Slot 1 is Wed+Thu and FOMC lands on Wednesday afternoons ~8x/yr. This instrument's pooled `wed_thu` session set contains **36 pinned FOMC dates**, and the primary surface above is exactly that set with these removed. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote. Both conditionals below are **measured directly** on their own day sets, not backed out of the pooled variance algebraically. This section is retained in full: it is the reason the exclusion is the operational choice, and it does not stop being load-bearing because the baseline moved.

tau_max, PRIMARY (FOMC excluded) against the pooled context row:

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max PRIMARY (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |
| tau_max pooled, context (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

**The primary and pooled tau_max rows are identical on this instrument, and that does NOT mean FOMC is harmless here.** tau_max is also a *clipped* statistic: the afternoon starts bracketing the 14:00 ET announcement are already short-capped by the 16:45 flat deadline (14:00 caps at 120min, 15:00 caps at 90min), so their tau_max cannot register an increase in sigma unless that sigma breaches the $125.00 ceiling outright. Read the sigma tables below, not the tau_max row, for the FOMC hazard.

sigma surface -- **`fomc_only`** (announcement days only -- the sessions the primary DROPS; note the much smaller n per cell):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $37.80 (n=36) | $47.75 (n=36) | $59.04 (n=36) | $68.50 (n=36) | $72.63 (n=36) | $75.65 (n=36) | $69.19 (n=36) | $82.14 (n=36) | $128.18 (n=36) |
| 10:00 | $25.17 (n=36) | $40.22 (n=36) | $42.50 (n=36) | $45.95 (n=36) | $45.53 (n=36) | $39.55 (n=36) | $51.03 (n=36) | $54.56 (n=36) | $150.41 (n=36) |
| 10:30 | $20.09 (n=36) | $26.84 (n=36) | $31.02 (n=36) | $33.31 (n=36) | $40.00 (n=36) | $38.31 (n=36) | $48.35 (n=36) | $85.44 (n=36) | $143.85 (n=36) |
| 11:00 | $19.80 (n=36) | $23.89 (n=36) | $27.87 (n=36) | $34.83 (n=36) | $35.61 (n=36) | $40.14 (n=36) | $43.61 (n=36) | $97.71 (n=36) | n/a (past 16:45 flat) |
| 12:00 | $14.69 (n=36) | $19.76 (n=36) | $26.57 (n=35) | $33.43 (n=36) | $36.51 (n=36) | $44.18 (n=36) | $97.54 (n=36) | $141.43 (n=36) | n/a (past 16:45 flat) |
| 13:00 | $11.75 (n=36) | $13.68 (n=36) | $16.75 (n=36) | $29.63 (n=36) | $68.68 (n=36) | $97.69 (n=36) | $140.88 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $51.58 (n=36) | $58.70 (n=36) | $72.35 (n=36) | $94.46 (n=36) | $123.31 (n=36) | $140.60 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $40.05 (n=36) | $59.33 (n=36) | $69.52 (n=36) | $81.77 (n=36) | $81.46 (n=36) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

sigma delta (pooled minus PRIMARY; positive = the excluded FOMC days were ADDING to sigma, negative = they were DAMPING it):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | -0.08 | -0.26 | -0.20 | +0.14 | +0.02 | -0.26 | -1.21 | -0.86 | +1.46 |
| 10:00 | -0.41 | -0.00 | -0.37 | -0.30 | -0.94 | -1.59 | -1.61 | -1.87 | +3.73 |
| 10:30 | -0.37 | -0.46 | -0.74 | -0.81 | -1.00 | -1.42 | -1.64 | +0.24 | +3.65 |
| 11:00 | -0.26 | -0.41 | -0.50 | -0.51 | -0.88 | -1.06 | -1.48 | +1.91 | n/a (past 16:45 flat) |
| 12:00 | -0.30 | -0.42 | -0.43 | -0.27 | -0.69 | -0.62 | +3.32 | +5.84 | n/a (past 16:45 flat) |
| 13:00 | -0.41 | -0.68 | -0.88 | -0.44 | +1.86 | +4.85 | +7.17 | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | +4.08 | +3.30 | +4.73 | +6.93 | +9.11 | +9.03 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | +2.23 | +3.42 | +4.05 | +4.18 | +3.74 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Worst measured FOMC-day cell: $150.41 at start=10:00, duration=360min (n=36 announcement sessions) -- 120% of the $125.00 ceiling.** That cell **BREACHES** the $125.00 ceiling on announcement days, by 20%. Pooled sigma at the same cell is **$112.21** (n=476, which passes the ceiling pooled) -- FOMC days **RAISED** sigma at that cell (1.34x).
**6 cell(s) PASS the ceiling pooled but BREACH it on announcement days** -- worst: 10:00/360min (pooled $112.21 -> FOMC $150.41); 10:30/360min (pooled $106.69 -> FOMC $143.85); 12:00/240min (pooled $87.44 -> FOMC $141.43). This is the decision-relevant form of the hazard and the direct argument for excluding these sessions: a pooled tau_max certifies those durations as usable while the announcement-day conditional is over the ceiling. **The primary surface above already excludes them, so these cells are the hazard the exclusion removes, not a residual risk in the headline numbers.**
**Most elevated cells (fomc_only / PRIMARY sigma ratio -- how much an announcement day lifts a cell above the surface this book would actually trade):** 14:00/15min (2.72x: $51.58 vs $18.94, n=36); 14:00/90min (2.51x: $123.31 vs $49.10, n=36); 14:00/60min (2.48x: $94.46 vs $38.06, n=36).
**Weigh all of the above against its n.** The FOMC-only surface rests on 35-36 sessions per cell (36 pinned FOMC dates fall in this instrument's pooled wed_thu session set), against n=476 at the same cell on the pooled context surface (10:00/360min) -- so each FOMC cell carries a correspondingly wider sampling error. It is a hazard flag, not a calibrated number. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

#### Roll-spanning check

**0** of the **27014** PRIMARY (wed_thu ex-FOMC) contributing (start, duration, session) windows span a detected roll (out of 19 rolls detected over the panel). Counted on the primary panel, not the pooled one -- the check exists to test whether back-adjustment is load-bearing for the sigma this artifact actually reports. Back-adjustment is therefore NOT doing any lifting for the reported within-day sigma: **no contributing measured window crossed a detected roll.** This is CHECKED on every run, not assumed. It is also all the count proves -- the grid's longest window ends at 16:30 ET, so a roll between then and the 16:45 flat deadline would be inside session hours and still uncounted, as would any roll on a session outside this day set. Those are unmeasured, not shown absent.

### MCL

Point value **$100.0000**/pt (derived, `tick_value_usd / tick_size`) - 820454 1m bars, 29 detected rolls, span 2021-08-01 18:00:00-04:00 -> 2023-12-29 16:59:00-05:00.

Cache coverage for its own IS window: **29/29 chunks** (100% -- the gate this section sits behind; a symbol short of it is reported PENDING and measured nowhere).

#### sigma surface -- **PRIMARY: `wed_thu` EXCLUDING the pinned FOMC sessions** (Slot 1, incumbent legs cannot fire, full 80-contract cap is free)

**Operational surface.** A third leg would skip FOMC Wednesdays, so the 19 pinned announcement sessions are removed BEFORE the surface is measured: 252 pooled `wed_thu` sessions -> **233** tradeable. That subtraction is the whole point of this table, and it costs power -- see the operational power floor in the joint table. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $40.07 (n=230) | $51.43 (n=229) | $68.70 (n=227) | $73.09 (n=228) | $90.76 (n=228) | $101.16 (n=230) | $125.59 (n=228) | $143.53 (n=225) | $165.68 (n=218) |
| 10:00 | $38.47 (n=227) | $51.69 (n=226) | $62.91 (n=228) | $75.92 (n=227) | $88.03 (n=228) | $108.49 (n=226) | $127.48 (n=226) | $149.54 (n=226) | $157.84 (n=219) |
| 10:30 | $46.99 (n=228) | $64.24 (n=226) | $74.44 (n=226) | $81.24 (n=227) | $103.04 (n=225) | $110.40 (n=226) | $136.18 (n=224) | $155.89 (n=221) | $157.03 (n=211) |
| 11:00 | $34.95 (n=226) | $52.38 (n=228) | $63.12 (n=227) | $74.72 (n=226) | $83.90 (n=226) | $99.23 (n=225) | $122.25 (n=224) | $134.78 (n=220) | n/a (past 16:45 flat) |
| 12:00 | $29.65 (n=224) | $43.92 (n=226) | $71.93 (n=224) | $67.70 (n=226) | $89.35 (n=223) | $97.10 (n=225) | $111.54 (n=220) | $112.70 (n=219) | n/a (past 16:45 flat) |
| 13:00 | $28.09 (n=225) | $41.66 (n=224) | $47.92 (n=222) | $56.69 (n=226) | $76.37 (n=221) | $79.54 (n=220) | $83.27 (n=219) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $28.22 (n=224) | $45.35 (n=221) | $52.15 (n=218) | $52.67 (n=220) | $57.90 (n=218) | $60.12 (n=219) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $14.73 (n=214) | $23.33 (n=217) | $25.37 (n=215) | $31.09 (n=218) | $32.87 (n=210) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 233 `wed_thu ex-FOMC` sessions in this instrument's panel; best-supported cell 230.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 233 -> 230 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 230 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

**tau_max (PRIMARY -- wed_thu ex-FOMC, `sigma <= $125.00` ceiling). This is the row the joint table and the verdict read:**

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 120 | 120 | 120 | 180 | 240 | 180 | 120 | 90 |

#### Context surfaces (DEMOTED -- do not lift a tau_max from here)

Both tables below include sessions the primary excludes, or days Slot 1 does not trade. They are kept because the primary is defined by subtraction from the first of them, and a reader cannot audit a subtraction whose minuend is hidden.

sigma surface -- pooled `wed_thu` (FOMC sessions INCLUDED; context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $39.83 (n=249) | $51.78 (n=248) | $68.93 (n=246) | $73.47 (n=247) | $91.17 (n=247) | $101.69 (n=249) | $124.67 (n=247) | $141.98 (n=244) | $163.31 (n=237) |
| 10:00 | $38.37 (n=246) | $51.82 (n=245) | $61.99 (n=247) | $75.85 (n=246) | $87.39 (n=247) | $107.30 (n=245) | $125.75 (n=245) | $147.07 (n=245) | $156.66 (n=238) |
| 10:30 | $46.12 (n=247) | $63.47 (n=245) | $74.01 (n=245) | $80.94 (n=246) | $102.25 (n=244) | $109.48 (n=245) | $133.83 (n=243) | $154.52 (n=240) | $154.96 (n=230) |
| 11:00 | $35.14 (n=245) | $51.96 (n=247) | $62.38 (n=246) | $73.80 (n=245) | $82.65 (n=245) | $97.43 (n=244) | $119.35 (n=243) | $132.10 (n=239) | n/a (past 16:45 flat) |
| 12:00 | $29.22 (n=243) | $42.81 (n=245) | $70.23 (n=243) | $66.26 (n=245) | $87.36 (n=242) | $94.74 (n=244) | $109.98 (n=239) | $111.11 (n=238) | n/a (past 16:45 flat) |
| 13:00 | $28.29 (n=244) | $40.83 (n=243) | $46.89 (n=241) | $55.49 (n=245) | $76.10 (n=240) | $79.08 (n=239) | $83.12 (n=238) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $28.82 (n=243) | $46.94 (n=240) | $51.68 (n=237) | $52.56 (n=239) | $57.79 (n=237) | $60.73 (n=238) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $16.01 (n=233) | $24.32 (n=236) | $26.51 (n=234) | $31.64 (n=237) | $33.64 (n=229) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 252 `wed_thu (pooled)` sessions in this instrument's panel; best-supported cell 249.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 252 -> 249 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 249 is (b). All 61 unclipped cells hold at least 90% of the raw denominator.

tau_max (pooled `wed_thu`, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 180 | 120 | 120 | 180 | 240 | 180 | 120 | 90 |

sigma surface -- `all_days` (context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $42.06 (n=619) ! | $57.49 (n=618) ! | $70.91 (n=615) ! | $77.04 (n=615) ! | $95.71 (n=615) ! | $107.38 (n=615) ! | $123.77 (n=612) ! | $136.16 (n=608) ! | $154.84 (n=573) ! |
| 10:00 | $37.88 (n=615) ! | $50.68 (n=613) ! | $61.95 (n=614) ! | $73.40 (n=614) ! | $88.72 (n=613) ! | $102.32 (n=612) ! | $121.29 (n=610) ! | $134.31 (n=604) ! | $146.49 (n=576) ! |
| 10:30 | $40.87 (n=613) ! | $56.64 (n=612) ! | $65.92 (n=610) ! | $76.92 (n=612) ! | $93.04 (n=609) ! | $106.29 (n=608) ! | $121.57 (n=607) ! | $138.34 (n=583) ! | $141.12 (n=563) ! |
| 11:00 | $33.05 (n=609) ! | $50.46 (n=612) ! | $62.81 (n=608) ! | $70.57 (n=612) ! | $84.94 (n=609) ! | $94.65 (n=610) ! | $110.08 (n=601) ! | $121.28 (n=579) ! | n/a (past 16:45 flat) |
| 12:00 | $30.31 (n=604) ! | $45.18 (n=608) ! | $59.89 (n=607) ! | $62.43 (n=609) ! | $75.51 (n=606) ! | $83.24 (n=602) ! | $98.11 (n=579) ! | $101.60 (n=576) ! | n/a (past 16:45 flat) |
| 13:00 | $29.56 (n=605) ! | $44.35 (n=606) ! | $47.12 (n=595) ! | $54.92 (n=602) ! | $71.24 (n=583) ! | $75.52 (n=579) ! | $81.23 (n=576) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $27.64 (n=598) ! | $46.17 (n=583) ! | $50.83 (n=575) ! | $51.89 (n=579) ! | $57.71 (n=573) ! | $59.11 (n=576) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $16.51 (n=561) ! | $21.81 (n=571) ! | $24.69 (n=565) ! | $28.70 (n=573) ! | $30.61 (n=561) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 750 `all_days` sessions in this instrument's panel; best-supported cell 619.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 750 -> 619 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 619 is (b). **61 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

tau_max (all_days, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 180 | 180 | 180 | 240 | 240 | 180 | 120 | 90 |

Against `wed_thu (pooled)`: **that context row is the FLATTERING one** -- the primary is strictly TIGHTER at 1 start(s) (09:30 120 vs 180min), so lifting its tau_max would overstate what is tradeable. Against `all_days`: **that context row is the FLATTERING one** -- the primary is strictly TIGHTER at 4 start(s) (09:30 120 vs 180min; 10:00 120 vs 180min; 10:30 120 vs 180min; 11:00 180 vs 240min), so lifting its tau_max would overstate what is tradeable. Slot 1 trades Wed+Thu and a third leg skips FOMC Wednesdays, so **the `wed_thu ex-FOMC` row is the one that governs** -- both context rows are shown for audit and must not be lifted in its place.

#### sqrt-t error -- how wrong a sqrt(t) extrapolation would have been

Computed on the **PRIMARY (wed_thu ex-FOMC)** surface, not the pooled context -- a sqrt-t verdict about a surface this book would not trade is a stale claim. Anchored on the shortest window (15min); **`predicted/measured - 1`, so POSITIVE = sqrt(t) OVERSTATES the measured sigma and NEGATIVE = sqrt(t) UNDERSTATES it.** This tests the design's own premise for refusing sqrt-t scaling in favour of direct measurement.

The sign is the operational content, and it is **mixed** across this surface -- so an unsigned |error| headline would hide the two opposite failure modes. Where sqrt-t **overstates**, a sqrt-t-based screen would have **wrongly rejected** holds that direct measurement shows are viable. Where it **understates**, that same screen would have **waved through** holds riskier than modelled. Full signed surface (the anchor column is 0 by construction):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | 0.0% (anchor) | +10.2% | +1.0% | +9.6% | +8.2% | +12.0% | +10.5% | +11.7% | +18.5% |
| 10:00 | 0.0% (anchor) | +5.3% | +5.9% | +1.3% | +7.0% | +0.3% | +4.5% | +2.9% | +19.4% |
| 10:30 | 0.0% (anchor) | +3.5% | +9.3% | +15.7% | +11.7% | +20.4% | +19.5% | +20.6% | +46.6% |
| 11:00 | 0.0% (anchor) | -5.7% | -4.1% | -6.5% | +2.0% | -0.4% | -1.0% | +3.7% | n/a (past 16:45 flat) |
| 12:00 | 0.0% (anchor) | -4.5% | -28.6% | -12.4% | -18.7% | -13.6% | -7.9% | +5.2% | n/a (past 16:45 flat) |
| 13:00 | 0.0% (anchor) | -4.6% | +1.5% | -0.9% | -9.9% | -0.1% | +16.8% | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | 0.0% (anchor) | -12.0% | -6.3% | +7.2% | +19.4% | +32.8% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | 0.0% (anchor) | -10.7% | +0.6% | -5.2% | +9.8% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Max OVERSTATEMENT (PRIMARY, wed_thu ex-FOMC): +46.6%** at start=10:30, duration=360min -- sqrt(t) predicts a sigma this much LARGER than measured, so a sqrt-t screen would have **wrongly rejected** this hold as too risky when the measurement says it is not.
**Max UNDERSTATEMENT (PRIMARY, wed_thu ex-FOMC): -28.6%** at start=12:00, duration=45min -- sqrt(t) predicts a sigma this much SMALLER than measured, so a sqrt-t screen would have waved this hold through at a risk level the measurement does not support. **This is the dangerous direction.**

#### FOMC-Wednesday hazard -- the EVIDENCE for excluding these sessions from the primary

Slot 1 is Wed+Thu and FOMC lands on Wednesday afternoons ~8x/yr. This instrument's pooled `wed_thu` session set contains **19 pinned FOMC dates**, and the primary surface above is exactly that set with these removed. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote. Both conditionals below are **measured directly** on their own day sets, not backed out of the pooled variance algebraically. This section is retained in full: it is the reason the exclusion is the operational choice, and it does not stop being load-bearing because the baseline moved.

tau_max, PRIMARY (FOMC excluded) against the pooled context row:

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max PRIMARY (min) | 120 | 120 | 120 | 180 | 240 | 180 | 120 | 90 |
| tau_max pooled, context (min) | 180 | 120 | 120 | 180 | 240 | 180 | 120 | 90 |

**The primary and pooled tau_max rows are NOT identical.** 1 start time(s) move once the 19 pinned FOMC sessions are excluded:
- **09:30: 180min pooled -> 120min PRIMARY (SHORTER on the primary).** At 180min the pooled sigma is **$124.67** (PASSES the $125.00 ceiling) against **$125.59** on the primary (BREACHES it). The pooled cell therefore clears **only because the announcement sessions in the pool are CALMER there** than this instrument's ordinary Wed/Thu behaviour and drag the pooled std down. **The exclusion COSTS tau_max at this start** -- the pooled row's reading does not survive removing them. That is a fragility result, and it is the opposite of harmless.
Every other start time is unchanged between the two rows. For those, tau_max is also a *clipped* statistic: the afternoon starts bracketing the 14:00 ET announcement are already short-capped by the 16:45 flat deadline (14:00 caps at 120min, 15:00 caps at 90min), so their tau_max cannot register an increase in sigma unless that sigma breaches the $125.00 ceiling outright. Read the sigma tables below, not the tau_max row, for the FOMC hazard.

sigma surface -- **`fomc_only`** (announcement days only -- the sessions the primary DROPS; note the much smaller n per cell):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $37.75 (n=19) | $57.03 (n=19) | $71.37 (n=19) | $76.03 (n=19) | $97.85 (n=19) | $110.52 (n=19) | $116.19 (n=19) | $125.35 (n=19) | $135.76 (n=19) |
| 10:00 | $36.02 (n=19) | $51.41 (n=19) | $48.51 (n=19) | $76.69 (n=19) | $81.31 (n=19) | $94.36 (n=19) | $105.53 (n=19) | $116.93 (n=19) | $145.57 (n=19) |
| 10:30 | $34.73 (n=19) | $53.59 (n=19) | $69.34 (n=19) | $77.85 (n=19) | $94.09 (n=19) | $98.27 (n=19) | $103.95 (n=19) | $141.43 (n=19) | $133.49 (n=19) |
| 11:00 | $38.32 (n=19) | $47.79 (n=19) | $54.20 (n=19) | $63.52 (n=19) | $67.38 (n=19) | $73.58 (n=19) | $79.48 (n=19) | $98.46 (n=19) | n/a (past 16:45 flat) |
| 12:00 | $24.36 (n=19) | $25.73 (n=19) | $45.31 (n=19) | $45.19 (n=19) | $60.83 (n=19) | $61.39 (n=19) | $92.33 (n=19) | $92.94 (n=19) | n/a (past 16:45 flat) |
| 13:00 | $27.69 (n=19) | $28.24 (n=19) | $30.81 (n=19) | $39.22 (n=19) | $69.75 (n=19) | $73.20 (n=19) | $80.12 (n=19) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $35.51 (n=19) | $60.53 (n=19) | $46.91 (n=19) | $51.12 (n=19) | $56.19 (n=19) | $66.98 (n=19) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $26.99 (n=19) | $34.40 (n=19) | $37.92 (n=19) | $38.05 (n=19) | $41.81 (n=19) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

sigma delta (pooled minus PRIMARY; positive = the excluded FOMC days were ADDING to sigma, negative = they were DAMPING it):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | -0.24 | +0.35 | +0.23 | +0.37 | +0.41 | +0.54 | -0.92 | -1.55 | -2.37 |
| 10:00 | -0.10 | +0.13 | -0.92 | -0.08 | -0.65 | -1.19 | -1.74 | -2.47 | -1.17 |
| 10:30 | -0.87 | -0.77 | -0.42 | -0.30 | -0.79 | -0.92 | -2.34 | -1.37 | -2.06 |
| 11:00 | +0.19 | -0.42 | -0.74 | -0.92 | -1.25 | -1.81 | -2.89 | -2.68 | n/a (past 16:45 flat) |
| 12:00 | -0.42 | -1.11 | -1.70 | -1.44 | -1.99 | -2.36 | -1.57 | -1.59 | n/a (past 16:45 flat) |
| 13:00 | +0.21 | -0.83 | -1.04 | -1.19 | -0.27 | -0.46 | -0.15 | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | +0.60 | +1.59 | -0.47 | -0.11 | -0.11 | +0.62 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | +1.28 | +0.99 | +1.13 | +0.55 | +0.77 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Worst measured FOMC-day cell: $145.57 at start=10:00, duration=360min (n=19 announcement sessions) -- 116% of the $125.00 ceiling.** That cell **BREACHES** the $125.00 ceiling on announcement days, by 16%. Pooled sigma at the same cell is **$156.66** (n=238, which itself BREACHES the ceiling) -- FOMC days are **CALMER** than the pool at that cell (0.93x), so this is the worst FOMC cell but **not an FOMC-caused** reading.
**No cell passes the ceiling pooled and breaches it on announcement days** -- the FOMC lift on this instrument stays inside the ceiling everywhere the pooled surface already cleared it. The exclusion is therefore not load-bearing for the ceiling test on THIS instrument -- but it is **not free here either**: it costs power AND it costs tau_max at 09:30 (see §Cost 2 above).
**Most elevated cells (fomc_only / PRIMARY sigma ratio -- how much an announcement day lifts a cell above the surface this book would actually trade):** 15:00/15min (1.83x: $26.99 vs $14.73, n=19); 15:00/45min (1.49x: $37.92 vs $25.37, n=19); 15:00/30min (1.47x: $34.40 vs $23.33, n=19).
**Weigh all of the above against its n.** The FOMC-only surface rests on 19 sessions in every cell (19 pinned FOMC dates fall in this instrument's pooled wed_thu session set), against n=238 at the same cell on the pooled context surface (10:00/360min) -- so each FOMC cell carries a correspondingly wider sampling error. It is a hazard flag, not a calibrated number. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

#### Roll-spanning check

**0** of the **13630** PRIMARY (wed_thu ex-FOMC) contributing (start, duration, session) windows span a detected roll (out of 29 rolls detected over the panel). Counted on the primary panel, not the pooled one -- the check exists to test whether back-adjustment is load-bearing for the sigma this artifact actually reports. Back-adjustment is therefore NOT doing any lifting for the reported within-day sigma: **no contributing measured window crossed a detected roll.** This is CHECKED on every run, not assumed. It is also all the count proves -- the grid's longest window ends at 16:30 ET, so a roll between then and the 16:45 flat deadline would be inside session hours and still uncounted, as would any roll on a session outside this day set. Those are unmeasured, not shown absent.

### M6A

Point value **$10000.0000**/pt (derived, `tick_value_usd / tick_size`) - 1222069 1m bars, 19 detected rolls, span 2019-05-05 20:00:00-04:00 -> 2023-12-29 16:59:00-05:00.

Cache coverage for its own IS window: **56/56 chunks** (100% -- the gate this section sits behind; a symbol short of it is reported PENDING and measured nowhere).

#### sigma surface -- **PRIMARY: `wed_thu` EXCLUDING the pinned FOMC sessions** (Slot 1, incumbent legs cannot fire, full 80-contract cap is free)

**Operational surface.** A third leg would skip FOMC Wednesdays, so the 36 pinned announcement sessions are removed BEFORE the surface is measured: 486 pooled `wed_thu` sessions -> **450** tradeable. That subtraction is the whole point of this table, and it costs power -- see the operational power floor in the joint table. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $8.57 (n=408) | $11.44 (n=414) | $14.43 (n=406) | $16.41 (n=414) | $19.23 (n=415) | $21.75 (n=389) ! | $24.48 (n=338) ! | $28.53 (n=304) ! | $30.91 (n=285) ! |
| 10:00 | $8.71 (n=405) | $11.13 (n=416) | $13.53 (n=398) ! | $15.44 (n=415) | $17.52 (n=387) ! | $19.81 (n=371) ! | $22.56 (n=349) ! | $25.69 (n=335) ! | $28.43 (n=364) ! |
| 10:30 | $7.98 (n=400) ! | $11.27 (n=417) | $12.67 (n=381) ! | $13.64 (n=392) ! | $16.73 (n=372) ! | $18.44 (n=342) ! | $23.86 (n=304) ! | $25.34 (n=286) ! | $27.92 (n=289) ! |
| 11:00 | $6.88 (n=381) ! | $9.03 (n=394) ! | $11.71 (n=374) ! | $13.13 (n=377) ! | $15.44 (n=339) ! | $17.06 (n=346) ! | $21.17 (n=338) ! | $22.49 (n=388) ! | n/a (past 16:45 flat) |
| 12:00 | $5.36 (n=312) ! | $7.87 (n=310) ! | $9.51 (n=300) ! | $10.66 (n=317) ! | $14.64 (n=284) ! | $15.65 (n=311) ! | $17.38 (n=353) ! | $19.82 (n=332) ! | n/a (past 16:45 flat) |
| 13:00 | $6.31 (n=262) ! | $7.91 (n=265) ! | $10.07 (n=249) ! | $10.51 (n=290) ! | $13.20 (n=255) ! | $14.40 (n=330) ! | $17.61 (n=308) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $7.27 (n=249) ! | $7.93 (n=253) ! | $9.43 (n=245) ! | $9.42 (n=329) ! | $12.19 (n=242) ! | $12.73 (n=305) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $4.15 (n=271) ! | $6.13 (n=277) ! | $6.76 (n=269) ! | $7.24 (n=347) ! | $8.72 (n=280) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 450 `wed_thu ex-FOMC` sessions in this instrument's panel; best-supported cell 417.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 450 -> 417 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 417 is (b). **52 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

**tau_max (PRIMARY -- wed_thu ex-FOMC, `sigma <= $125.00` ceiling). This is the row the joint table and the verdict read:**

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

#### Context surfaces (DEMOTED -- do not lift a tau_max from here)

Both tables below include sessions the primary excludes, or days Slot 1 does not trade. They are kept because the primary is defined by subtraction from the first of them, and a reader cannot audit a subtraction whose minuend is hidden.

sigma surface -- pooled `wed_thu` (FOMC sessions INCLUDED; context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $8.52 (n=440) | $11.31 (n=448) | $14.35 (n=438) | $16.22 (n=447) | $18.84 (n=449) | $21.26 (n=420) ! | $23.98 (n=361) ! | $27.70 (n=329) ! | $32.87 (n=319) ! |
| 10:00 | $8.53 (n=436) ! | $10.91 (n=449) | $13.24 (n=429) ! | $15.07 (n=449) | $17.11 (n=418) ! | $19.32 (n=399) ! | $21.91 (n=381) ! | $25.48 (n=369) ! | $30.51 (n=398) ! |
| 10:30 | $7.84 (n=431) ! | $11.11 (n=450) | $12.51 (n=412) ! | $13.39 (n=423) ! | $16.41 (n=400) ! | $18.15 (n=364) ! | $23.17 (n=328) ! | $25.95 (n=319) ! | $30.25 (n=315) ! |
| 11:00 | $6.73 (n=413) ! | $8.82 (n=425) ! | $11.43 (n=402) ! | $12.81 (n=405) ! | $15.13 (n=363) ! | $16.53 (n=379) ! | $21.36 (n=372) ! | $24.60 (n=423) ! | n/a (past 16:45 flat) |
| 12:00 | $5.29 (n=334) ! | $7.74 (n=331) ! | $9.31 (n=321) ! | $10.41 (n=343) ! | $14.30 (n=304) ! | $16.52 (n=339) ! | $20.40 (n=382) ! | $23.53 (n=361) ! | n/a (past 16:45 flat) |
| 13:00 | $6.12 (n=286) ! | $7.77 (n=288) ! | $9.93 (n=273) ! | $12.27 (n=322) ! | $16.51 (n=286) ! | $18.83 (n=363) ! | $22.31 (n=340) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $9.67 (n=284) ! | $10.09 (n=286) ! | $14.59 (n=280) ! | $14.36 (n=364) ! | $18.68 (n=275) ! | $18.29 (n=339) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $5.33 (n=304) ! | $8.14 (n=311) ! | $8.60 (n=300) ! | $9.10 (n=382) ! | $10.45 (n=308) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 486 `wed_thu (pooled)` sessions in this instrument's panel; best-supported cell 450.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 486 -> 450 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 450 is (b). **53 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

tau_max (pooled `wed_thu`, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

sigma surface -- `all_days` (context):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $8.10 (n=1061) ! | $11.17 (n=1084) ! | $13.71 (n=1056) ! | $15.67 (n=1065) ! | $19.19 (n=1087) ! | $21.23 (n=1023) ! | $24.52 (n=847) ! | $26.31 (n=772) ! | $31.61 (n=754) ! |
| 10:00 | $8.21 (n=1077) ! | $10.67 (n=1088) ! | $12.86 (n=1053) ! | $15.35 (n=1109) ! | $17.27 (n=1039) ! | $19.90 (n=964) ! | $21.65 (n=887) ! | $23.54 (n=859) ! | $27.14 (n=936) ! |
| 10:30 | $7.44 (n=1041) ! | $11.10 (n=1093) ! | $12.26 (n=982) ! | $13.45 (n=1026) ! | $16.10 (n=951) ! | $17.63 (n=853) ! | $20.29 (n=772) ! | $23.34 (n=746) ! | $25.98 (n=725) ! |
| 11:00 | $6.62 (n=1003) ! | $8.58 (n=1049) ! | $10.72 (n=955) ! | $12.11 (n=971) ! | $14.24 (n=870) ! | $15.33 (n=886) ! | $18.88 (n=864) ! | $21.12 (n=1009) ! | n/a (past 16:45 flat) |
| 12:00 | $5.11 (n=800) ! | $7.59 (n=777) ! | $8.72 (n=745) ! | $9.72 (n=787) ! | $12.41 (n=705) ! | $14.17 (n=770) ! | $17.11 (n=888) ! | $19.26 (n=827) ! | n/a (past 16:45 flat) |
| 13:00 | $5.45 (n=664) ! | $7.31 (n=661) ! | $9.23 (n=605) ! | $10.67 (n=727) ! | $13.91 (n=651) ! | $15.38 (n=830) ! | $17.79 (n=775) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $7.35 (n=608) ! | $8.09 (n=635) ! | $11.15 (n=616) ! | $11.30 (n=829) ! | $14.38 (n=633) ! | $14.31 (n=761) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $4.61 (n=692) ! | $6.47 (n=732) ! | $7.08 (n=705) ! | $7.61 (n=887) ! | $8.90 (n=697) ! | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Day-set denominator: 1450 `all_days` sessions in this instrument's panel; best-supported cell 1109.** Each cell's `n` is the subset of day-set sessions where BOTH endpoint 1m bars exist, and it can fall short for two different reasons. **(a)** Dates in the day set with no RTH window at all -- Globex Sunday evenings and holidays sit in the panel as dates but have no 09:30-16:45 session. That is calendar structure, not selection, and it bounds the 1450 -> 1109 gap. **(b)** Minutes with **no print**: on `ohlcv-1m` a missing bar means no trade in that minute, so the sessions a cell drops are the *quiet* ones and its sigma is biased **upward** (conservative for a ceiling test, but a selected subset either way). Anything below 1109 is (b). **61 of 61** unclipped cells rest on under 90% of the raw denominator and are marked `!` above.

tau_max (all_days, context):

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

Against `wed_thu (pooled)`: the two tau_max rows agree at every start time. Against `all_days`: the two tau_max rows agree at every start time. Slot 1 trades Wed+Thu and a third leg skips FOMC Wednesdays, so **the `wed_thu ex-FOMC` row is the one that governs** -- both context rows are shown for audit and must not be lifted in its place.

#### sqrt-t error -- how wrong a sqrt(t) extrapolation would have been

Computed on the **PRIMARY (wed_thu ex-FOMC)** surface, not the pooled context -- a sqrt-t verdict about a surface this book would not trade is a stale claim. Anchored on the shortest window (15min); **`predicted/measured - 1`, so POSITIVE = sqrt(t) OVERSTATES the measured sigma and NEGATIVE = sqrt(t) UNDERSTATES it.** This tests the design's own premise for refusing sqrt-t scaling in favour of direct measurement.

The sign is the operational content, and it is **mixed** across this surface -- so an unsigned |error| headline would hide the two opposite failure modes. Where sqrt-t **overstates**, a sqrt-t-based screen would have **wrongly rejected** holds that direct measurement shows are viable. Where it **understates**, that same screen would have **waved through** holds riskier than modelled. Full signed surface (the anchor column is 0 by construction):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | 0.0% (anchor) | +5.9% | +2.9% | +4.5% | +9.2% | +11.5% | +21.3% | +20.2% | +35.8% |
| 10:00 | 0.0% (anchor) | +10.7% | +11.5% | +12.8% | +21.8% | +24.4% | +33.8% | +35.6% | +50.1% |
| 10:30 | 0.0% (anchor) | +0.2% | +9.2% | +17.1% | +16.9% | +22.4% | +15.9% | +26.0% | +40.1% |
| 11:00 | 0.0% (anchor) | +7.8% | +1.8% | +4.8% | +9.2% | +14.1% | +12.6% | +22.4% | n/a (past 16:45 flat) |
| 12:00 | 0.0% (anchor) | -3.7% | -2.3% | +0.7% | -10.2% | -3.1% | +6.9% | +8.3% | n/a (past 16:45 flat) |
| 13:00 | 0.0% (anchor) | +12.8% | +8.5% | +20.1% | +17.1% | +24.0% | +24.1% | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | 0.0% (anchor) | +29.6% | +33.5% | +54.4% | +46.1% | +61.5% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | 0.0% (anchor) | -4.3% | +6.4% | +14.6% | +16.6% | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Max OVERSTATEMENT (PRIMARY, wed_thu ex-FOMC): +61.5%** at start=14:00, duration=120min -- sqrt(t) predicts a sigma this much LARGER than measured, so a sqrt-t screen would have **wrongly rejected** this hold as too risky when the measurement says it is not.
**Max UNDERSTATEMENT (PRIMARY, wed_thu ex-FOMC): -10.2%** at start=12:00, duration=90min -- sqrt(t) predicts a sigma this much SMALLER than measured, so a sqrt-t screen would have waved this hold through at a risk level the measurement does not support. **This is the dangerous direction.**

#### FOMC-Wednesday hazard -- the EVIDENCE for excluding these sessions from the primary

Slot 1 is Wed+Thu and FOMC lands on Wednesday afternoons ~8x/yr. This instrument's pooled `wed_thu` session set contains **36 pinned FOMC dates**, and the primary surface above is exactly that set with these removed. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote. Both conditionals below are **measured directly** on their own day sets, not backed out of the pooled variance algebraically. This section is retained in full: it is the reason the exclusion is the operational choice, and it does not stop being load-bearing because the baseline moved.

tau_max, PRIMARY (FOMC excluded) against the pooled context row:

| start_et | 09:30 | 10:00 | 10:30 | 11:00 | 12:00 | 13:00 | 14:00 | 15:00 |
|---|---|---|---|---|---|---|---|---|
| tau_max PRIMARY (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |
| tau_max pooled, context (min) | 360 | 360 | 360 | 240 | 240 | 180 | 120 | 90 |

**The primary and pooled tau_max rows are identical on this instrument, and that does NOT mean FOMC is harmless here.** tau_max is also a *clipped* statistic: the afternoon starts bracketing the 14:00 ET announcement are already short-capped by the 16:45 flat deadline (14:00 caps at 120min, 15:00 caps at 90min), so their tau_max cannot register an increase in sigma unless that sigma breaches the $125.00 ceiling outright. Read the sigma tables below, not the tau_max row, for the FOMC hazard.

sigma surface -- **`fomc_only`** (announcement days only -- the sessions the primary DROPS; note the much smaller n per cell):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | $7.89 (n=32) | $9.62 (n=34) | $13.55 (n=32) | $13.66 (n=33) | $13.07 (n=34) | $12.92 (n=31) | $14.00 (n=23) | $14.55 (n=25) | $43.34 (n=34) |
| 10:00 | $5.71 (n=31) | $7.37 (n=33) | $8.35 (n=31) | $9.18 (n=34) | $9.83 (n=31) | $10.42 (n=28) | $12.48 (n=32) | $23.51 (n=34) | $45.77 (n=34) |
| 10:30 | $5.49 (n=31) | $8.91 (n=33) | $10.40 (n=31) | $9.56 (n=31) | $11.38 (n=28) | $12.93 (n=22) | $11.45 (n=24) | $30.35 (n=33) | $44.30 (n=26) |
| 11:00 | $4.53 (n=32) | $5.33 (n=31) | $6.36 (n=28) | $7.22 (n=28) | $9.93 (n=24) | $9.35 (n=33) | $23.55 (n=34) | $39.64 (n=35) | n/a (past 16:45 flat) |
| 12:00 | $4.19 (n=22) | $5.42 (n=21) | $5.76 (n=21) | $6.86 (n=26) | $8.32 (n=20) | $24.58 (n=28) | $41.33 (n=29) | $47.94 (n=29) | n/a (past 16:45 flat) |
| 13:00 | $3.46 (n=24) | $5.92 (n=23) | $8.37 (n=24) | $23.02 (n=32) | $33.24 (n=31) | $41.67 (n=33) | $47.73 (n=32) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | $19.55 (n=35) | $20.01 (n=33) | $31.04 (n=35) | $34.45 (n=35) | $41.08 (n=33) | $42.64 (n=34) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | $11.00 (n=33) | $17.52 (n=34) | $18.13 (n=31) | $19.75 (n=35) | $21.35 (n=28) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

sigma delta (pooled minus PRIMARY; positive = the excluded FOMC days were ADDING to sigma, negative = they were DAMPING it):

| start \\ duration (min) | 15 | 30 | 45 | 60 | 90 | 120 | 180 | 240 | 360 |
|---|---|---|---|---|---|---|---|---|---|
| 09:30 | -0.06 | -0.14 | -0.08 | -0.19 | -0.39 | -0.49 | -0.50 | -0.83 | +1.96 |
| 10:00 | -0.18 | -0.22 | -0.29 | -0.38 | -0.41 | -0.49 | -0.65 | -0.22 | +2.09 |
| 10:30 | -0.14 | -0.16 | -0.16 | -0.25 | -0.32 | -0.29 | -0.69 | +0.61 | +2.33 |
| 11:00 | -0.15 | -0.21 | -0.29 | -0.32 | -0.31 | -0.53 | +0.20 | +2.12 | n/a (past 16:45 flat) |
| 12:00 | -0.07 | -0.14 | -0.20 | -0.25 | -0.34 | +0.87 | +3.02 | +3.70 | n/a (past 16:45 flat) |
| 13:00 | -0.19 | -0.14 | -0.14 | +1.77 | +3.31 | +4.43 | +4.69 | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 14:00 | +2.40 | +2.16 | +5.16 | +4.95 | +6.49 | +5.56 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |
| 15:00 | +1.18 | +2.00 | +1.85 | +1.85 | +1.73 | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) | n/a (past 16:45 flat) |

**Worst measured FOMC-day cell: $47.94 at start=12:00, duration=240min (n=29 announcement sessions) -- 38% of the $125.00 ceiling.** It sits 62% under the ceiling. Pooled sigma at the same cell is **$23.53** (n=361, which passes the ceiling pooled) -- FOMC days **RAISED** sigma at that cell (2.04x).
**No cell passes the ceiling pooled and breaches it on announcement days** -- the FOMC lift on this instrument stays inside the ceiling everywhere the pooled surface already cleared it. The exclusion is therefore not load-bearing for the ceiling test on THIS instrument, and it moves no tau_max cell here either; what it costs this instrument is **power** (see the joint table's operational floor).
**Most elevated cells (fomc_only / PRIMARY sigma ratio -- how much an announcement day lifts a cell above the surface this book would actually trade):** 14:00/60min (3.66x: $34.45 vs $9.42, n=35); 14:00/90min (3.37x: $41.08 vs $12.19, n=33); 14:00/120min (3.35x: $42.64 vs $12.73, n=34).
**Weigh all of the above against its n.** The FOMC-only surface rests on 20-35 sessions per cell (36 pinned FOMC dates fall in this instrument's pooled wed_thu session set), against n=361 at the same cell on the pooled context surface (12:00/240min) -- so each FOMC cell carries a correspondingly wider sampling error. It is a hazard flag, not a calibrated number. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

#### Roll-spanning check

**0** of the **20478** PRIMARY (wed_thu ex-FOMC) contributing (start, duration, session) windows span a detected roll (out of 19 rolls detected over the panel). Counted on the primary panel, not the pooled one -- the check exists to test whether back-adjustment is load-bearing for the sigma this artifact actually reports. Back-adjustment is therefore NOT doing any lifting for the reported within-day sigma: **no contributing measured window crossed a detected roll.** This is CHECKED on every run, not assumed. It is also all the count proves -- the grid's longest window ends at 16:30 ET, so a roll between then and the 16:45 flat deadline would be inside session hours and still uncounted, as would any roll on a session outside this day set. Those are unmeasured, not shown absent.

## Stage 1 x Stage 2 joint table

**Every Stage-2 column reads the PRIMARY (wed_thu ex-FOMC) surface** -- the tau_max headline, the sigma at the binding cell, its SE and its distance to the ceiling. The pooled and `all_days` rows in the per-symbol sections above are context and are not represented here. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

The table carries **both** power floors. `Stage-1 power floor` is reproduced unchanged from `instrument_map` (the row's own POOLED panel, `1.96/sqrt(N)`); `ex-FOMC power floor` is the same statistic on the MEASURED ex-FOMC session count -- the sessions a leg that skips announcement days actually gets. The `binds first` column shows Stage 1's cost-vs-power verdict and the one recomputed against the operational floor; see §Cost 1 for the derivation and for which rows flip.

tau_max derives from a **fully-exposed 1-contract position** held the entire window -- an UPPER BOUND on a real strategy's exposure (a strategy with stops and selective entry has less), so tau_max is **conservative**. A tau_max reading of 360min (the grid's own maximum duration) means "at least this long" -- the true tau_max may exceed the grid, not that it was measured to be exactly that value.

Where several start times reach the same tau_max, **every tied start is listed** -- a single `@ HH:MM` would silently elect one winner out of a tie. The headroom column quotes the **tightest** of the tied cells (the largest sigma at that duration), because that is the cell that binds.

**Read the headroom against its sampling error, not on its own.** Each sigma is a sample std over `n` sessions, so the ceiling test is a threshold verdict on an estimate. `SE(sigma) = sigma / sqrt(2(n-1))` is about **3% of sigma at n ~ 480**, so a headroom under roughly one SE (~3%) is **not a distinguishable pass** -- it is a reading that could sit either side of the ceiling on a re-draw of the same length. Rows within 2 SE are flagged `!!` in the distance column.

Two things make that SE an **under**statement of the real uncertainty. (1) The normal-theory formula assumes normal increments; index-futures returns are fat-tailed, which inflates the sampling variance of a std estimate, so the true SE is **larger** than the figure shown -- treat it as a lower bound. (2) tau_max is a **max over the 72-cell (8 starts x 9 durations) grid**, so the binding cell is *selected* for having come in on the favourable side of its own noise. Both effects push the same way: the headline tau_max is optimistic, and a cell sitting a fraction of an SE under the ceiling should be read as **at** it.

tau_max itself is `max(durations whose OWN sigma <= ceiling)`, not the longest passing prefix: on a non-monotone row a shorter duration can breach while a longer one passes. That breach stays visible in the per-symbol sigma surfaces above -- read the row, not only the tau_max cell.

| Symbol | Stage-2 | tau_max headline (PRIMARY, ex-FOMC) | sigma at that cell (headroom vs ceiling) | SE(sigma) at binding cell | distance to ceiling | cost-tax (1t, r=1) | Stage-1 power floor (pooled panel) | ex-FOMC power floor (OPERATIONAL) | binds first: Stage-1 -> Stage-2 |
|---|---|---|---|---|---|---:|---:|---:|---|
| MYM | measured | 360min @ 10:30 | $119.44 @ 10:30 (4.4% under $125.00) | $4.04 (3.38% of sigma, n=438) | **+1.38 SE** !! within 2 SE -- not distinguishable | 0.0742 | 0.0891 | 0.0924 (N=450) | POWER -> POWER |
| M2K | measured | 360min @ 09:30, 10:00, 10:30 (3-way tie) | $115.58 @ 09:30 (7.5% under $125.00) | $3.90 (3.37% of sigma, n=440) | **+2.42 SE** | 0.0742 | 0.0891 | 0.0924 (N=450) | POWER -> POWER |
| MCL | measured | 240min @ 12:00 | $112.70 @ 12:00 (9.8% under $125.00) | $5.40 (4.79% of sigma, n=219) | **+2.28 SE** | 0.0902 | 0.1237 | 0.1284 (N=233) | POWER -> POWER |
| M6A | measured | 360min @ 09:30, 10:00, 10:30 (3-way tie) | $30.91 @ 09:30 (75.3% under $125.00) | $1.30 (4.20% of sigma, n=285) | **+72.54 SE** | 0.0902 | 0.0891 | 0.0924 (N=450) | COST -> POWER **FLIP** |

## What this does NOT establish

A survivor is not admissible. **Nothing here admits a candidate**, and moving the primary surface changes nothing about that. R1 is now *measured* rather than assumed for the survivors above, but T2/T3/T4/T5 and the whole §7.4 mechanism limb remain untouched, and **no mechanism has been proposed or tested**.

**The standing disclaimers all still apply to the primary surface, unchanged.** tau_max is measured on a **fully-exposed 1-contract position** held the whole window -- an upper bound on a real strategy's exposure, so tau_max is **conservative**. The SE beside each binding cell is a **lower bound** (normal-theory formula, fat-tailed returns). tau_max is a **max over the 72-cell grid**, so the binding cell is selected on the favourable side of its own noise.

**The exclusion itself is a cost, not a free improvement.** It raises the Clause-N floor on every measured instrument (§Cost 1) and can lower tau_max (§Cost 2). And because the primary surface is now *defined* by `FOMC_DATES_ET`, the headline numbers inherit that list's provenance directly. `FOMC_DATES_ET` in `stage2_run.py` is **hand-pinned from memory of the public FOMC calendar, NOT fetched** -- best-effort provenance only. That caveat now binds **harder** than it did when the ex-FOMC surface was a side comparison: this list DEFINES the primary surface, so a wrong or missing date moves the headline numbers themselves, not a footnote.

"Measured" is not "comfortably clear". Every headline tau_max in the joint table rests on a SINGLE binding cell, itself the max over a 72-cell grid. **1 of 4** measured binding cells sit within 2 standard errors of the ceiling (MYM (+1.38 SE)) -- a ceiling test that close is not a distinguishable pass, and the SE shown is itself a lower bound (see the joint-table notes).

**No K was consumed and no manifest was opened** -- this pass computed no return-predictive statistic (sigma is an instrument property, not a selection-shaped look at edge: no strategy, no signal, no PnL). The first pass that computes a return-predictive statistic on this data changes that.

> **Regeneration note.** Emitted by `python -X utf8 stage2_run.py` from cached `.dbn` chunks only -- never pulls. Re-run after the background `stage2_pull.py --execute` advances to pick up newly-complete survivors.
