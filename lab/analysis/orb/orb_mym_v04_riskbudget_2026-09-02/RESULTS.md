# ORB-MYM-1 v0.4 — conditioning-filter screen, PR #259 verification, riskBudgetUsd input

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

**Post-Codex-review correction (2026-09-02, same day):** a [PR #265](https://github.com/Joshua-Asante/first-passage/pull/265)
review caught two engine-fidelity defects that changed every bust/pass magnitude below (not any
verdict) — see §5. All tables in §1–§3 are the corrected numbers; the pre-correction figures are
superseded, not restated.

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
  **after** its own findings were measured (offline, on the exported trade list — see §3); the
  edited file's own SHA-256 is `806619993410e2cdc666dc0e1bc7a1e42dd98ac6fab33dccb1870cbe6cc4e89b`.

---

## §1 — Pre-registered conditioning-filter screen

Frozen pre-registration: [`PREREG_filters.md`](PREREG_filters.md). Scripts:
[`feat_lib.py`](feat_lib.py) (day-frame + session-feature builder, reuses
`lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py` verbatim),
[`score_filters.py`](score_filters.py) (day-level lifts + enumerated circular-shift null),
[`bust_engine.py`](bust_engine.py) (canonical bootstrap engine — `core/mc/simulation.py`
verbatim, same method as `lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/bust_pass_sim.py`; blocks
via `core/mc/ingest.py::build_week_blocks`, see §5).

**Window:** 598 traded days with bar features + 60-session warm-up, 2020-09-24→2026-07-02
(39.7% of the 1,506-business-day span — see §5b). **Base on this window** (per contract): Net
$15,227 · PF 1.297 · maxDD $3,817 · RF 3.99 · worst day −$984. **`Hot` (the Pine's diagnostic-only
overnight-range tag) is confirmed identical to the instrument ledger's own `on_elev80`
conditioner** (label agreement 1.000, 598/598 days) — `ops/instruments/MYM.md`'s GRADUATE-eligible
`overnight-range→RTH-range` finding is already in this script, tagging only, never gating.

Primary set (K=3, Bonferroni α=0.0167): P1 skip the day if the first OR-high breach is after
11:00 ET; P2 half-size Hot days; P3 half-size days whose OR range exceeds its trailing-60-session
median. Decision rule frozen before scoring: promote to a TV-native A/B only if the cell is not
dominated by flat qty-1 or qty-2 sizing on **both** Select and Growth (bust and pass).

| cell | Select bust/pass | Growth bust/pass | verdict |
|---|---:|---:|---|
| base q1 | 41.7 / 58.3 | 31.3 / 68.6 | reference |
| base q2 (as-run) | 61.4 / 38.6 | 52.5 / 47.5 | reference |
| **P1** skip-after-11:00, q1 | 43.6 / 56.4 | 33.4 / 66.4 | **FAIL** — p=0.229 on the day-level lift, bust worse than base q1 |
| **P2** Hot×0.5 | 61.7 / 38.3 | 53.0 / 47.0 | **FAIL** — no better than q2-flat |
| **P3** wide-OR×0.5 | 55.2 / 44.9 | 45.6 / 54.5 | **FAIL** — dominated by q1-flat |
| Hot-only (exploratory) | 22.2 / 71.1 | 13.8 / 75.8 | not a candidate — 1 of ~30 looks, p=0.077 (2-sided), flat net in 2023–24, ~2× time-to-pass |

Full day-level table (25 exploratory looks incl. P1 threshold sensitivity, day-history state,
gap-in-calm, OR width, ToD-volume, day-of-week, directional [raised-bar class, disclosed not
proposed], prior-day CLV): [`score_filters_results.csv`](score_filters_results.csv). None of the
25 clears its own one-/two-sided shift-null test at a level that would survive any multiplicity
correction; all are reported for disclosure.

**All three primary filters FAIL.** The only cell with a rope-friendly shape (Hot-only) is
exploratory, not primary, and did not meet the frozen promotion bar even informally — it is named
here because it directly motivated §3, not because it is being proposed.

**Inactivity-barrier check (§5c): base_q1, the densest cell here at 39.7% trade-day density,
collapses to 99.3% total failure (barrier ON) if the standing weekly token-trade mitigation is
assumed absent — see §5c for why this is confirmation, not a new problem.**

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
| q2 (the size $31,947.96 was measured at) | **51.2 / 48.8** | **43.4 / 56.6** | **busts Select on day 42** (maxDD 2.83% vs the 3.0% trail) |
| q1 (not reported in PR #259) | 29.4 / 70.6 | 20.1 / 79.6 | pass, maxDD 1.93% |

**Verdict:** "even better results" is true for raw net/PF and false for survival at the size it
was measured. This is the third time this construct family has shown good raw TradingView metrics
and a bad canonical-engine bust rate (v0.3: 62–74% bust, `ops/instruments/MYM.md` M9 vs the
2026-09-01 correction; §1's Hot-only: exploratory only; now P50 at its own reported size).
PR #259's own RESULTS.md already carries the correct hedge (`SOURCE-STAGE EXPLORATORY...
not Confirm evidence... not authorization for live capital`) — this section is independent
confirmation of that hedge, using data the original screenshot-based comparison didn't have.

**Inactivity-barrier check (§5c):** q1 barrier ON → 0.0%/0.0% bust/pass (99.96–99.99%
pure-inactivity); q2 barrier ON → 2.0%/1.2% bust (S/G), 97.9–98.6% pure-inactivity. This construct
trades only ~22.6% of business days (the P50 gate itself is the reason), so it needs the standing
weekly token-trade mitigation more than most — see §5c.

---

## §3 — `riskBudgetUsd`: a mechanism-derived Pine input

**Mechanism** (from the Pine's own construction, not from mining §1/§2's P&L): the base stop and
every scale-in step are multiples of the completed opening range, so a day's planned worst case
scales with OR width (`(1+maxScaleIns) × stopLossMult × OR range × point value`) while the
Tradeify rope is fixed dollars. On 2020-03-20 the OR was 560 pts ⇒ **planned risk $4,200 at qty 2,
more than the entire Select rope on one day** — the worst day in the §2 panel (−$1,424/contract)
and the week containing day 42's realized bust.

Pre-registration: [`PREREG_risk_budget.md`](PREREG_risk_budget.md). Script:
[`risk_budget_screen.py`](risk_budget_screen.py) (ORR from the long bar panel, §0; offline risk
formula assumes the OR-range stop basis, matching what this export used — see §5a for the
ATR-basis caveat). Rule frozen at budget=$1,500 (half the Select rope) before scoring; 4 disclosed
neighbors/variants (K=5 this test).

| cell (on the §2 P50 panel, 384 days with ORR) | Select bust/pass | Growth bust/pass | median days-to-pass | realized path |
|---|---:|---:|---:|---|
| qty 1 flat | 29.0 / 71.0 | 19.7 / 80.1 | 459 / 489 | pass, maxDD 1.93% |
| qty 2 flat (as-exported) | 51.1 / 48.9 | 43.1 / 56.9 | 159 / 166 | **bust day 42** |
| primary: budget $1,500 on qty 2 | 43.9 / 56.1 | 33.9 / 66.1 | 239 / 251 | pass, maxDD 2.57% |
| neighbor: budget $1,000 | 56.5 / 43.3 | 46.9 / 52.1 | 509 / 555 | bust day 557 |
| neighbor: budget $2,000 | 50.5 / 49.6 | 40.9 / 59.1 | 204 / 215 | bust day 42 (S) |
| variant: hard cap only (qty 2 or skip) | 47.1 / 52.9 | 36.6 / 63.4 | 285 / 301 | bust day 46 |
| variant: budget $1,500 at base qty 1 | 23.9 / 75.8 | 15.3 / 84.0 | 509 / 539 | pass, maxDD 1.42% |

**Primary (qty 2) FAILS** the frozen dominance rule — real improvement over qty-2-flat, still
dominated by qty-1-flat on both tiers. **Per `PREREG_risk_budget.md`'s own decision rule, that is
where this stops: "neighbors are never promoted over the primary."** The qty-1 variant's own
bust/pass profile (23.9/75.8, 15.3/84.0) looks good in isolation — better than qty-1-flat on both
tiers — but it is the *observed winner among several scored variants*, not a pre-registered
outcome; the honest disposition is **report, no recommendation**, not a next-step A/B. (An earlier
draft of this document did recommend that A/B — a genuine violation of this file's own frozen
rule, caught in PR #265 review. Corrected here, not silently edited away.) A fresh pre-registration
on data this export never saw would be required before this variant is anything more than a
described observation: in practice it is a far-tail OR-width skip (11 of 384 days, ORR > ~400 pts:
5×2020, 2025-04-07 [ORR 801], 5×2026) whose own combined net is **+$903** — almost all the value is
removing the one −$1,424 day, not the other 10. **A tighter budget is worse** (neighbor $1,000:
56.5% bust, worst of any cell) — the 51 days it would skip carry 40% of the strategy's net. The
edge concentrates on wide-OR/Hot days; this input must stay a far-tail cap, never a vol-target
knob.

**Inactivity-barrier check (§5c):** primary (qty 2) barrier ON → 0.34%/0.09% bust (S/G),
~99.7–99.9% pure-inactivity; the qty-1 variant barrier ON → 0.0%/0.0% bust, 100% pure-inactivity;
neighbor $1,000 barrier ON → ~0%, ~100% pure-inactivity. Every skip-capable cell here needs the
standing weekly token-trade mitigation to be reachable at all — see §5c.

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
  The `riskBudgetUsd` Pine input is available for a future TV-native test; nothing in §3 licenses
  recommending a specific setting for one — that would need its own fresh pre-registration.
- Independently reproduces, a third time, that this construct's raw TradingView metrics do not
  predict its canonical-engine bust rate. Any future claim of "better results" on this construct
  should be checked the same way: real trade CSV, day-level reconstruction, canonical engine at
  the size actually proposed — not the raw net/PF/leg-DD alone.
- Confirms (§5c) that the standing weekly venue-idle token trade
  ([[feedback_inactivity_barrier_off_is_correct_weekly_token_trade]]) is load-bearing for this
  entire construct family, not optional — every cell tested, including the densest, fails almost
  totally without it.
- Does not touch `ops/instruments/MYM.md`'s M8/M9 record, PR #259's own findings, the LIVE
  Striker DJ30 v4.5 leg (M1), or the DEAD `opening-range-continuation` mechanism (M2). No `core/`,
  lock, allocation, `dd_protection`, lifecycle, or rail change.

## §5 — Corrections from PR #265 Codex review

Six findings, all verified before acting on them; two changed numbers, none changed a verdict.

**§5a — offline risk formula assumes OR-range stop basis.** `risk_budget_screen.py`'s planned-risk
estimator always uses `SL_MULT × ORR`; if the Pine's `stopBasis` input were set to `"ATR"` instead,
the live Pine (which reads its own `stopBasisDist`, correct at runtime either way) would size
correctly but this offline counterfactual would not. Disclosed limitation of the analysis script,
not the shipped input — the analyzed export used the OR-range default.

**§5b — P3's trailing-60-session median now skips nulls instead of lowering the threshold.** 3
sessions in the bar panel lack a 09:15/09:30 OR bar; the original fix (`min_periods=45`) let some
days classify off as few as 45 real observations — a shorter lookback than the pre-registered 60,
not the registered rule. Now requires 60 real (non-null) observations, always. Re-ran §1's
`feat_lib.py`/`score_filters.py`: scorable-day count unchanged (598); only the few P3-dependent
cells drifted by single-digit dollars in the full CSV — no table above changed from this fix alone.

**Week-block bootstrap was not Monday-anchored.** `bust_engine.py`/`verify_pr259.py`/
`risk_budget_screen.py` all reshaped the panel into 5-day blocks starting from whatever the
panel's first row happened to be (a Thursday, for §1's window) instead of anchoring to Monday like
the repo's own canonical `core/mc/ingest.py::build_week_blocks` — pairing Thu/Fri with the
*following* week's Mon–Wed rather than the same calendar week, and silently dropping the tail via
truncation. Fixed by importing and using that function directly in all three scripts. **This is
the fix that moved every bust/pass number in §1–§3** — uniformly toward higher bust / lower pass
(e.g. §1 base_q1 Select 34.7%→41.7%) — no verdict changed (every filter that failed still fails;
Hot-only and the risk-budget qty-1 variant still show the same qualitative shape, just at worse
absolute levels).

**§5c — inactivity barrier: confirmation, not a new finding.** Every bust/pass cell above used
`firm_kwargs`'s default `inactivity_off=True` (repo-wide convention). A review comment asked
whether cells that skip whole days (Hot-only, the risk-budget skip variants) risk breaching
Tradeify's real 5-business-day inactivity rule. **They do, mechanically and dramatically** — turning
the barrier on collapses bust/pass to near-0%/0% with 97–100% pure-inactivity failure for *every*
cell tested, including §1's base_q1 at 39.7% trade-day density (96.9–98.2% inactivity) and §3's
qty-2 primary at 97% of its own (already-filtered) days traded (99.7–99.9% inactivity). **This is
not evidence the barrier-off convention is wrong.** The operator maintains a standing weekly
venue-idle token trade specifically to satisfy this rule when the strategy itself hasn't fired
(`CLAUDE.md` live-execution posture; one such trade already executed 2026-08-12) — barrier-off is
the intended operational model, and this session's numbers are a concrete measurement of how
load-bearing that mitigation actually is for this construct family, not a reason to distrust it.
See [[feedback_inactivity_barrier_off_is_correct_weekly_token_trade]] for the full record and why
this should not be re-litigated as a fresh finding in future work here.

**§5d — record the post-edit Pine digest.** Done — see §0.

**§5e — pytest-collection CI failure (found after this review, same day).** `risk_budget_test.py`'s
name matched pytest's `*_test.py` discovery glob; the `validation-controls` CI job (`pytest lab/
--import-mode=importlib`) imported it as a test module, so its top-level code ran under pytest's
own `sys.argv` instead of a CLI CSV path, crashing on `IsADirectoryError`. Renamed to
`risk_budget_screen.py`; verified locally against the exact CI invocation (595 items collected, 0
errors).

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
