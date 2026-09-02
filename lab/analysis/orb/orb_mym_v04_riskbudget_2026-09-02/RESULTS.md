# ORB-MYM-1 v0.4 — conditioning-filter screen, PR #259 verification, risk-budget input

**Status:** `EXPLORATORY — NO FILTER PROMOTED; ONE PINE INPUT ADDED, DEFAULT OFF`. Candidate
construct only (`orb_mym_4_edition.pine`, CANDIDATE lifecycle, never AUTHORIZED, chart-only paper
vehicle — see `ops/instruments/MYM.md` M8/M9). No lifecycle, allocation, `dd_protection`, rail, or
deployment change. The `.pine` source itself is not committed (repo-wide gitignored,
`core/strategies/MANIFEST.sha256` convention) — this directory is the evidence trail, not the
strategy file.

Three linked pieces of work, same session (2026-09-02), same construct family:

1. **§1 — Pre-registered conditioning-filter screen** on the v0.4 base export (before PR #259's
   P50 gate existed). Three primary filters, all FAIL against a frozen dominance rule.
2. **§2 — Independent verification of [PR #259](https://github.com/Joshua-Asante/first-passage/pull/259)'s**
   `orb_mym_volume_gate_2026-09-02` P50 claim, using the real trade-list CSV instead of the
   screenshot reads that RESULTS.md relied on for two of its three cells.
3. **§3 — A new Pine input** (`riskBudgetUsd`, mechanism-derived from §2's finding), pre-registered
   and engine-scored before being written into the script.

K is disclosed, not admitted — none of this went through `discovery.register_search open`
(mechanism-first admission would refuse most of these cells at the declared K; see
`docs/methodology/strategy_harvest.md`). Cumulative informal K on this construct family, this
session: §1 ≈30, §2 (verification, not a new look) 0, §3 5 → **≈35**. Anything re-proposed into
the repo pipeline (`futures-anomaly-discovery`) must carry this count forward, not restart at 0.

---

## §0 — Data audit

- **v0.4 base export** (§1): `ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-01_76b9e.csv`, operator-
  supplied, not committed. 1,849 exit rows / 703 traded days, qty 2 constant, long-only,
  2020-01-02→2026-08-28. Step-0 battery clean (`--tz UTC`; see `lab/research_utils/step0_battery.py`
  for why). Exits-only Net reconciles to the file's own Cumulative PnL to the cent ($34,560.64).
  Entry census: Mon 223 / Thu 248 / Fri 227 traded days, **zero Tuesday or Wednesday entries** —
  the Pine's day-filter defaults are all-ON; this export ran with Tue/Wed off (provenance
  undocumented at the time).
- **PR #259 P50 export** (§2): `ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-02_49508.csv`, operator-
  supplied, not committed. 986 exit rows / 385 traded days, 2020-01-02→2026-08-20. Pine SHA-256
  `9292bd4ec0ca9074d6d6523491dcdde3709424bd53edf9c75dea79f3b9f65071` matches PR #259's own
  `orb_mym_volume_gate_2026-09-02/RESULTS.md` citation exactly. Net (exit-only sum, $31,947.96)
  matches that RESULTS.md's P50 row to the cent. Same Tue/Wed-off schedule.
- **Bar panel**: `core/data/bar_data/MYM_M15.csv` (gitignored vendor data; BAR EXPORT v0.2,
  sha256 `24e16952…`, 2020-07-02→2026-07-02) for §1. §3 additionally needs a longer panel — the
  operator's `BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv` (170,417 bars,
  2019-05-05→2026-07-31, the same file PR #259's `mym_breakout_entry_2026_09` study parsed) — to
  reach the 2020 H1 window §3's worst day falls in; not committed, parsed via
  `scripts/parse_bar_export.py` (see §3 reproduction).
- **Pine**: `orb_mym_4_edition.pine`, private Downloads-local. §1 and §2 ran against the
  pre-riskBudgetUsd build (SHA-256 `9292bd4e…`, same as PR #259 cites). §3's Pine edit was applied
  **after** its own findings were measured (offline, on the exported trade list — see §3), so the
  edit's own SHA-256 differs and is recorded there.

---

## §1 — Pre-registered conditioning-filter screen

Frozen pre-registration: [`PREREG_filters.md`](PREREG_filters.md). Scripts:
[`feat_lib.py`](feat_lib.py) (day-frame + session-feature builder, reuses
`lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py` verbatim),
[`score_filters.py`](score_filters.py) (day-level lifts + enumerated circular-shift null),
[`bust_engine.py`](bust_engine.py) (canonical bootstrap engine — `core/mc/simulation.py`
verbatim, same method as `lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/bust_pass_sim.py`).

**Window:** 598 traded days with bar features + 60-session warm-up, 2020-09-24→2026-07-02.
**Base on this window** (per contract): Net $15,227 · PF 1.297 · maxDD $3,817 · RF 3.99 · worst
day −$984. **`Hot` (the Pine's diagnostic-only overnight-range tag) is confirmed identical to the
instrument ledger's own `on_elev80` conditioner** (label agreement 1.000, 598/598 days) —
`ops/instruments/MYM.md`'s GRADUATE-eligible `overnight-range→RTH-range` finding is already in
this script, tagging only, never gating.

Primary set (K=3, Bonferroni α=0.0167): P1 skip the day if the first OR-high breach is after
11:00 ET; P2 half-size Hot days; P3 half-size days whose OR range exceeds its trailing-60-session
median. Decision rule frozen before scoring: promote to a TV-native A/B only if the cell is not
dominated by flat qty-1 or qty-2 sizing on **both** Select and Growth (bust and pass).

| cell | Select bust/pass | Growth bust/pass | verdict |
|---|---:|---:|---|
| base q1 | 34.7 / 65.3 | 24.3 / 75.6 | reference |
| base q2 (as-run) | 60.8 / 39.2 | 50.6 / 49.4 | reference |
| **P1** skip-after-11:00, q1 | 35.7 / 64.2 | 25.4 / 74.4 | **FAIL** — p=0.229 on the day-level lift, bust worse than base q1 |
| **P2** Hot×0.5 | 58.8 / 41.2 | 49.0 / 51.0 | **FAIL** — dominated by q1-flat |
| **P3** wide-OR×0.5 | 51.4 / 48.6 | 41.0 / 59.1 | **FAIL** — dominated by q1-flat |
| Hot-only (exploratory) | 16.3 / 76.1 | 9.7 / 79.6 | not a candidate — 1 of ~30 looks, p=0.077 (2-sided), flat net in 2023–24, ~2× time-to-pass |

Full day-level table (25 exploratory looks incl. P1 threshold sensitivity, day-history state,
gap-in-calm, OR width, ToD-volume, day-of-week, directional [raised-bar class, disclosed not
proposed], prior-day CLV): [`score_filters_results.csv`](score_filters_results.csv). None of the
25 clears its own one-/two-sided shift-null test at a level that would survive any multiplicity
correction; all are reported for disclosure.

**All three primary filters FAIL.** The only cell with a rope-friendly shape (Hot-only) is
exploratory, not primary, and did not meet the frozen promotion bar even informally — it is named
here because it directly motivated §3, not because it is being proposed.

---

## §2 — PR #259 P50 claim, verified against the real trade list

PR #259's `orb_mym_volume_gate_2026-09-02/RESULTS.md` reports three manual TradingView
Strategy-Tester screenshot reads (Off/P50/P80) of a redesigned percentile OR-volume gate, with
this caveat already on record there: *"These are manual screenshot reads, not retained
TradingView List-of-Trades exports... profitable-trade rates are leg-level under pyramiding."*
The operator subsequently supplied the real trade-list CSV behind the P50 cell (§0). Script:
[`verify_pr259.py`](verify_pr259.py).

**Reconciliation: P50's raw numbers are real.** 986 exit rows / $31,947.96 net (exit-only sum)
match PR #259's screenshot row to the cent. Day-level reconstruction (real trades, per contract):
385 days, WR 56.1%, PF 1.459, maxDD $2,137 (raw-$ $4,274 — RESULTS.md's own $4,621.18 is close;
the residual is the known TV-intrabar-vs-close-reconstruction gap, not a defect), RF 7.47, worst
day −$1,424.

**Then through the same canonical bootstrap engine, at the size the headline was measured (qty 2):**

| size | Select bust/pass | Growth bust/pass | realized historical path |
|---|---:|---:|---|
| q2 (the size $31,947.96 was measured at) | **51.1 / 48.9** | **41.4 / 58.6** | **busts Select on day 42** (maxDD 2.83% vs the 3.0% trail) |
| q1 (not reported in PR #259) | 25.4 / 74.5 | 16.6 / 83.0 | pass, maxDD 1.93% |

**Verdict:** "even better results" is true for raw net/PF and false for survival at the size it
was measured. This is the third time this construct family has shown good raw TradingView metrics
and a bad canonical-engine bust rate (v0.3: 62–74% bust, `ops/instruments/MYM.md` M9 vs the
2026-09-01 correction; §1's Hot-only: exploratory only; now P50 at its own reported size).
PR #259's own RESULTS.md already carries the correct hedge (`SOURCE-STAGE EXPLORATORY...
not Confirm evidence... not authorization for live capital`) — this section is independent
confirmation of that hedge, using data the original screenshot-based comparison didn't have.

---

## §3 — `riskBudgetUsd`: a mechanism-derived Pine input

**Mechanism** (from the Pine's own construction, not from mining §1/§2's P&L): the base stop and
every scale-in step are multiples of the completed opening range, so a day's planned worst case
scales with OR width (`(1+maxScaleIns) × stopLossMult × OR range × point value`) while the
Tradeify rope is fixed dollars. On 2020-03-20 the OR was 560 pts ⇒ **planned risk $4,200 at qty 2,
more than the entire Select rope on one day** — the worst day in the §2 panel (−$1,424/contract)
and the week containing day 42's realized bust.

Pre-registration: [`PREREG_risk_budget.md`](PREREG_risk_budget.md). Script:
[`risk_budget_screen.py`](risk_budget_screen.py) (ORR from the long bar panel, §0). Rule frozen at
budget=$1,500 (half the Select rope) before scoring; 4 disclosed neighbors/variants (K=5 this
test).

| cell (on the §2 P50 panel, 384 days with ORR) | Select bust/pass | Growth bust/pass | median days-to-pass | realized path |
|---|---:|---:|---:|---|
| qty 1 flat | 22.1 / 77.8 | 14.0 / 85.7 | 471 / 493 | pass, maxDD 1.93% |
| qty 2 flat (as-exported) | 50.0 / 50.0 | 39.8 / 60.2 | 167 / 177 | **bust day 42** |
| primary: budget $1,500 on qty 2 | 40.7 / 59.3 | 29.9 / 70.2 | 256 / 267 | pass, maxDD 2.57% |
| neighbor: budget $1,000 | 51.4 / 48.4 | 40.5 / 58.1 | 528 / 581 | bust day 557 |
| neighbor: budget $2,000 | 49.3 / 50.7 | 37.8 / 62.2 | 216 / 228 | bust day 42 (S) |
| variant: hard cap only (qty 2 or skip) | 45.1 / 54.9 | 34.2 / 65.8 | 291 / 306 | bust day 46 |
| **variant: budget $1,500 at base qty 1** | **15.7 / 83.9** | **9.0 / 90.1** | 536 / 557 | pass, maxDD 1.42% |

**Primary (qty 2) FAILS** the frozen dominance rule — real improvement over qty-2-flat, still
dominated by qty-1-flat. **The variant at base qty 1 meets the rule** on both tiers (+14%
time-to-pass, within the 25% tolerance) — in practice a far-tail OR-width skip (11 of 384 days,
ORR > ~400 pts: 5×2020, 2025-04-07 [ORR 801], 5×2026), whose own combined net is **+$903** — almost
all the value is removing the one −$1,424 day, not the other 10. **A tighter budget is worse**
(neighbor $1,000: 51.4% bust, worst of any cell) — the 51 days it would skip carry 40% of the
strategy's net. The edge concentrates on wide-OR/Hot days; this input must stay a far-tail cap,
never a vol-target knob.

**Pine implementation** (applied after the above was measured, so it postdates the SHA-256 cited
in §0/§2): `riskBudgetUsd` input, default **0 (off)** — reproduces every previously-measured
number in the file's header exactly. New state (`plannedRiskPerContract`, `qtyToday`) computed
once at the OR close, same place `slLong`/`tpLong` are set, so it cannot float mid-day even under
`stopBasis="ATR"`. Both the base entries and `scaleInQty` size off `qtyToday`. Compiled clean
against the TradingView Guest endpoint: `python scripts/pine_check.py <file>` → `OK`. The
`.pine` file itself is not committed (see header of this document); its dated changelog block
documents this one addition only, scoped explicitly to avoid claiming credit for the P50-gate /
`stallH` / `scaleInStepMult` / take-profit-multiple changes already present in the file from
earlier the same day, which remain undocumented in its own header — a pre-existing gap, not
introduced here.

---

## §4 — What this does and doesn't establish

- No filter or sizing rule cleared its own frozen promotion bar at the size it would actually run.
  The one variant that did (`riskBudgetUsd=1500` at qty 1) is a Pine input now available for a
  TV-native test, not a validated result — offline, export-anchored evidence only, one export,
  no holdout (§1's own panel has none left — the v0.3/v0.4 lineage has been fully viewed by TV
  tuning since 2026-08-25).
- Independently reproduces, a third time, that this construct's raw TradingView metrics do not
  predict its canonical-engine bust rate. Any future claim of "better results" on this construct
  should be checked the same way: real trade CSV, day-level reconstruction, canonical engine at
  the size actually proposed — not the raw net/PF/leg-DD alone.
- Does not touch `ops/instruments/MYM.md`'s M8/M9 record, PR #259's own findings, the LIVE
  Striker DJ30 v4.5 leg (M1), or the DEAD `opening-range-continuation` mechanism (M2). No `core/`,
  lock, allocation, `dd_protection`, lifecycle, or rail change.

## Reproduction

```bash
# §1 — filter screen (needs core/data/bar_data/MYM_M15.csv locally + the v0.4 base CSV)
python feat_lib.py "<local ORB-MYM-1_v0.4_..._2026-09-01_76b9e.csv>"
python score_filters.py
N_SIMS=4000 python bust_engine.py

# §2 — PR #259 P50 verification (needs the P50 trade-list CSV locally)
python verify_pr259.py "<local ORB-MYM-1_v0.4_..._2026-09-02_49508.csv>"

# §3 — risk-budget screen (needs the long BAR_EXPORT + the P50 CSV locally)
python ../../../../scripts/parse_bar_export.py --symbol MYM \
    --in "<local BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv>" --out /tmp/MYM_M15_long.csv
python risk_budget_screen.py /tmp/MYM_M15_long.csv "<local ...49508.csv>"
```

All CSVs above are operator-exported / vendor-sourced and are not committed, matching this repo's
standing posture for TV trade-list and bar exports (`core/data/tv_exports/`, `core/data/bar_data/`).
