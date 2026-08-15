# Tradeify-native fade — Stage 0 + Stage 1

**Disposition:** ACTIVE
**Opened:** 2026-07-30
**Spec:** `docs/superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md`
**Plan:** `docs/superpowers/plans/2026-07-30-tradeify-fade-stage0-stage1.md`

Stage-0 instrumentation (1m-native integrity battery, TV/Databento roll exposure,
cost-per-notional pins) plus the Stage-1 compliance-first screen and feasible-region
calculator. **$0 spend, K=0, no mechanism scored.**

**Stage-0 item 3 DISCHARGED 2026-07-30:** M2K + MCL 2023 `ohlcv-1m` panels pulled
(estimate $0.00 each; monthly chunks via `pull_cost_pin_panels.py`) → measured
`cost_bp` pins in `RESULTS.md`. §4.2 input 1 unblocked.

Key results in `RESULTS.md`.

**All three pre-scoring rulings FROZEN 2026-07-31**, with no mechanism in existence and
nothing scored — the only moment at which they are not a §7 goalpost move:

- `ROLL-EXCLUDE-2026-07-31` — exposed sessions excluded from IS and OOS
  (`docs/notes/2026-07-30-tv-databento-roll-window-ruling.md`). Costs 4.65% of sessions,
  and they are quarterly — a **seasonal** subset the pre-registration must declare.
- `COST-MULT-4X-2026-07-31` — governing cost-law multiple **4×**, unchanged.
- `CONFIG-B-MCL-2026-07-31` — configuration **B, two-sided MCL**; the only configuration
  with no dependency on the Striker parking sequence.

Both of the latter, plus the reasoning and what they cost:
`docs/notes/2026-07-31-fade-stage1-frozen-rulings.md`.

**Correction 2026-07-31 — an earlier version of this card and of `RESULTS.md` claimed
"4× leaves one feasible cell needing Sharpe 1.81; 2× opens two at ~1.17–1.28".** That
described only the R:R 0.66 column. 4× leaves **two**, the second needing 0.814 — but
`min_sharpe` is not comparable across R:R columns, because the grid pins `p` while the
random-walk baseline moves. Compare on `excess_wr_required`. Do not propagate the old
claim; it is also still live in the `STATE.md` pointer log.

**Expressibility limb added 2026-07-31 (fourth limb).** The prior three all derive
`sigma_d` *from* the assumed bracket, so none could see that **M6A's cost-mandated barrier
was 1.65× its entire measured session σ** — it cleared all three and would have passed into
a Stage-2 K spend. M6A is now dead at every multiple; MYM/M2K/MCL unchanged.

**Fourth ruling 2026-07-31 — `SIGMA-NATIVE-2026-07-31`: the borrowed MCL σ is retired for
the native panel.** `SESSION_SIGMA_USD["MCL"]` **$112.70 → $112.17**, measured on
`mcl_1m.parquet` (2023-only, n=90) instead of the published 2021-08 → 2023-12 surface
(n=219). Same function, same ex-FOMC basis, same max-cell rule — only the cohort differs.
**`RESULTS_sigma_native.md`'s "DOES NOT REPRODUCE, −33.1%" is a statement about the pinned
CELL, not about the constant:** under the max-cell semantics the constant is actually
documented at, the native panel gives $112.17 against $112.70 — **−0.47%**. The maximum
relocated (240min@12:00 → 360min@09:30); its level survived. **No verdict moves** — gate
still PASS, still 3 feasible cells, `subperiod_ratio` 0.975/1.090/1.194 → 0.979/1.095/1.200
— and that neutrality is pinned by a regression test. What it costs: n 219 → 90, a
single-calendar-year panel with no regime split available on the constant. Reasoning,
costs, and the two published errors it surfaced:
`docs/notes/2026-07-31-fade-stage1-frozen-rulings.md` Ruling 4.

**FINDING 2026-07-31b — the screen never interrogates the EDGE, only the geometry.** All
four limbs ask whether the *bracket* is viable; none asks whether the *edge* it assumes is
achievable. `sharpe_reachable` looks like it does — it carries `SHARPE_CEILING`, docstring
*"plausibility ceiling on the Sharpe a mechanism could deliver"* — but applies that ceiling
to `min_sharpe_for_sigma(σ_d)`, a σ-window compatibility bound, and a **lower** bound at
that. Same defect class the `expressible` limb closed, one level up. New **reported**
column `implied_annualized_sr` (absent from `feasible`, pinned by
`test_implied_sr_is_REPORTED_not_GATED`): the frozen MCL cells imply **9.98 / 11.16 /
12.23**, and the **minimum over the entire admitted region is 2.98 — 1.63× the 1.83
ceiling**. Quote the 1.63×, not the 5.5×. Units are like-for-like: 1.83 is Aegis at 1.828,
annualized Sharpe of a daily P&L stream over 1141 bdays (Q-GATECART-1 §B) — a raised
frequency-mismatch objection was **withdrawn**. Two region properties recorded:
`excess_wr_required` is the **identity** `p − 1/(1+rr)` (cost and multiple cancel exactly —
Ruling 1's verdict survives, its stated reasoning does not), and **payability caps `p` from
above** at 0.6523 with the pinned `P_WIN = 0.65` sitting on the cap, clearing by $3.30.
**Disposition owed** — report-only as landed, or gated (which empties the region at every
`p`). See `docs/notes/2026-07-31-fade-stage1-frozen-rulings.md` Finding 2026-07-31b.

**2026-08-13 — implied-SR disposition discharged as report-only; region REOPENED.**
Ruling 5's 2026-08-10 promotion-to-gate is superseded
([`ADR 2026-08-13`](../../../docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)).
Implied annSR stays a reported column (absent from `feasible`). The 4× · CONFIG-B-MCL
cells are geometry-open again. **Still owed: a mechanism** (unchanged). Frozen Rulings
1–4 stand.

**Still owed: a mechanism.** Q-INVENTORY-1 staged zero seeds; three further sourcing
channels run 2026-07-31 staged **1 seed total**, screened **DEAD** at Req 1(iii) and again
at Req 2/4/5. A **fourth** pass 2026-08-01 closed the Rank-3 journal-filtered gap via
Crossref (36 searches, 6 journals) — **2 hits, 0 admissible**: the only live candidate is a
**calendar spread**, which is definitionally offsetting and so a **compliance SCREEN-FAIL
before scoring**. The **Rank-1 gap closed the same day** — S2's `isInfluential` filter
applied for the first time over 94 citing works from two Tier-A seeds: **5 influential, 0
cohort-and-shape**; unfiltered, 9 cohort-and-shape hits, none admissible (closest is a
**Chinese**-market intraday reversal — right shape, Req 2 cohort transplant). Four
consecutive nulls, structural rather than unlucky, and the citation channel is now
**COMPLETE rather than merely null**. **Load-bearing pattern: two of the three most on-point
published energy-reversion constructs are SPREADS** (2015 calendar, 2025 naphtha crack) —
and spreads are structurally illegal at this firm, so the venue obstruction is
mechanism-level, not just the 21.37 bp hurdle. The
Req-5 hurdle measures **21.37 bp/event**, 1.9× the 11.06 that killed D5 and 4.2× the 5.05
that killed H-OD-1; the only CL-family cohort δ in the repo is **−1.16 bp, wrong-signed**.
Also owed: the `subperiod_ratio` disposition
(median session delivers **exactly 4** resolutions on both RTH windows — neither clean
outcome), and which session window governs MCL integrity (narrowed but not answered: the
09:00 start is a dead pit artefact, the 14:30 end is a mandated settlement boundary).
