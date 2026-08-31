# RESULTS — Q-RANGECOND-1 Phase 1-3: overnight-range-conditioned ORB-MNQ-1 payoff shape

> ## ⚠ CORRECTED 2026-08-31 — the `RESOLVED` verdict below is RETRACTED
>
> `data_lib.py::overnight_ohlc` had a look-ahead defect (Codex PR #227 review) that inflated the
> effect reported below. Under the corrected conditioner the effect vanishes (WR diff +24.75pp →
> +0.75pp, CI now includes 0; mean-win diff +0.711R → -0.058R, sign-flipped, CI includes 0) and
> the verdict flips to `FALSIFIED`. **See the "CORRECTED RESULTS (2026-08-31)" section at the
> bottom of this file — that section is authoritative.** Everything below this banner is the
> original, now-superseded run, preserved unedited as the record of what the defect actually
> produced. Full account:
> [`docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md`](../../../../docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md).
> Closure: [`Q-RANGECOND-1-closure-falsified.md`](../../../../docs/briefs/closures/Q-RANGECOND-1-closure-falsified.md).

**Verdict:** `FALSIFIED` — corrected 2026-08-31: WR diff +24.75pp to +0.75pp (CI now includes 0), mean-win diff +0.711R to -0.058R (sign-flipped); the `RESOLVED` line below is the original, now-superseded run, preserved unedited.

**Verdict: `RESOLVED`** (per pre-registration §C, all four limbs clear) — **with one disclosed
panel-vintage caveat that must be read before this verdict is treated as final** (see "Caveat"
below). Computed 2026-08-30, per Route ① operator ruling ("I rule Route ① satisfied, proceed with
Phase 1").

## Headline

| Quantity | Unconditioned | Conditioned (`bias_overnight=1`) | Diff | CI (block=20/draws=4000/seed=42) |
|---|---|---|---|---|
| n trades | 1,141 | 340 | — | — |
| Win rate | 41.72% | 66.47% | **+24.75pp** | `[+18.30pp, +31.31pp]` (excludes 0) |
| Mean win (R, winners only) | +0.860R | +1.571R | **+0.711R** | `[+0.543R, +0.887R]` (excludes 0) |

**Gate:** L1 (n≥30 conditioned) PASS — 340 ≫ 30. L2 (WR-diff CI excludes 0, positive) PASS. L3
(mean-win-diff CI excludes 0, positive) PASS. L4 (conditioned WR ≥ 0.55) PASS — 66.47% clears the
Tradeify floor's own lower bound by a wide margin. All four clear → `RESOLVED` per pre-reg §C.

## Method

Script: [`phase1_2_3_conditioned_orb.py`](phase1_2_3_conditioned_orb.py). Reused
`orb_lib.orb_backtest` / `orb_lib.session_panel` / `orb_lib._finalize` verbatim (the same arbiter
`ORB-MNQ-1`'s own G8 admission and R3 payability runs use), with the exact `Instrument`
construction from `run_orb_mnq_bulenox_blusky.py::make_inst` (`or_bars=2`, `open_tod=09:30 ET`,
`close_tod=15:45 ET`, `tick=0.25`, `spread_pt=0.25`, Tradeify `rt_cost_pt=1.41` — reproduced from
`cost_per_side_usd=0.91` + 1-tick slip, matching `MNQ.md`'s own cited figure exactly). Conditioner
reused verbatim from `candidate2_overnight_rth_transfer.py` (`WINDOW=60, Q_BIAS=0.80`,
strictly-prior) and `data_lib.py` (`overnight_ohlc`, `range_series`). No cached panel existed in
this worktree; built fresh from the hash-verified `core/data/bar_data/MNQ_M15.csv`
(`6c86f41a17b7dfce...`, matches `SHA256SUMS`).

**One real bug found and fixed during this run:** the initial epoch-conversion step hit the
known pandas-2.x `datetime64[us]`-vs-`[ns]` trap this repo already documented once (Q-ICTEXP-1,
`MNQ.md`) — `pd.to_datetime(...).astype("int64")` silently returned microseconds rather than
nanoseconds on this pandas version, producing dates near 1970-01-01 and a 3-trade, garbage first
run. Fixed by forcing `.astype("datetime64[ns, UTC]")` before the int64 cast; re-run reproduced a
sane 6-year span (2020-07-01 → 2026-07-02) and 1,541 trades. Disclosed rather than silently
corrected without a trace — the script's own docstring and this note are the record.

## Caveat — panel-vintage mismatch with `ORB-MNQ-1`'s original admission figures

This run's own sanity check (entry-trigger rate) came back close but not exact to the headline
figure cited in `ORB-MNQ-1`'s own `RESULTS.md`: **99.55%** here (1,541/1,548 RTH sessions) vs the
cited **99.4%** (1,846/1,857). The entry-trigger RATE matches closely (both ≈100%, confirming ORB
fires on nearly every session either way) but the ABSOLUTE session-day count differs by ~300
days. Investigated, not assumed: `RESULTS.md`'s own text states its panel spans **"2019-05-06→
present"** (its own header line 15) — over a year earlier than `MNQ_M15.csv`'s own **2020-07-01**
start. `ORB-MNQ-1`'s original G8 admission pipeline used a different, longer, native-databento
1-minute→15m panel; this brief's own Phase 1 (by design, stated in the brief's own §7) uses
`MNQ_M15.csv` — the TV BAR EXPORT v0.2 panel this entire `Q-RANGEXFER-1`/presence-battery research
line is built on, because the conditioner itself has no equivalent computed on the older,
longer databento-native panel. Using a different panel for the ORB leg than the conditioner leg
would introduce its own, worse mismatch (a large fraction of trades with no conditioner value at
all). **This was the correct, only internally-consistent choice given the brief's own design, but
it means this run's own summary stats (mean gross R, WR, PF on the full unconditioned population)
are not directly comparable, trade-for-trade, to `ORB-MNQ-1`'s originally-published G8 admission
figures** — they are computed on a ~300-day-shorter, more-recent-starting panel. The
unconditioned-population stats reported here (mean R +0.0813, t=2.65, WR 41.72%, PF 1.19) are a
real, statistically significant, positive edge in their own right (not garbage, not the pre-fix
1970-epoch bug) — consistent in shape and sign with `ORB-MNQ-1`'s own qualitative
characterization — but should be read as a fresh measurement on the current canonical panel,
not a reproduction-for-reproduction's-sake of the original headline numbers.

**What this caveat does and does not affect:** it does not affect this brief's own internal
comparison (conditioned vs. unconditioned, both measured on the identical panel, identical
`orb_backtest` call, differing only in the `bias_overnight` split) — that comparison is
apples-to-apples by construction. It does mean any future full re-MC (per this closure's own
INTEGRATE routing) should explicitly decide which panel to standardize on, and should not
silently blend panel vintages.

## Audit hooks

```bash
python lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py
# Expected (deterministic given seed=42): n_trades=1541, n_conditioned=340,
# WR conditioned=0.6647 / unconditioned=0.4172, mean-win conditioned=+1.5714 / unconditioned=+0.8603,
# WR-diff CI=[+0.1830,+0.3131], mean-win-diff CI=[+0.5430,+0.8868], VERDICT=RESOLVED

# Confirm the panel-vintage discrepancy
grep -n "2019-05-06" lab/analysis/orb/orb_mnq_2026-07/RESULTS.md
grep -n "2020-07-01" core/data/bar_data/MNQ_M15.csv | head -1

# Confirm the Tradeify cost basis reproduces MNQ.md's own cited figure
python -c "print(2.0*(0.91+0.50)/2.0)"
# Expected: 1.41
```

---

## CORRECTED RESULTS (2026-08-31) — authoritative

**Verdict: `FALSIFIED`.** Re-run after fixing `data_lib.py::overnight_ohlc`'s look-ahead defect
(full account: the audit note linked in the banner above). No script logic changed beyond the
upstream `data_lib.py` fix — same `phase1_2_3_conditioned_orb.py`, same frozen pre-registration
gate, same hash-verified `MNQ_M15.csv`.

### Corrected headline

| Quantity | Original (retracted) | Corrected | Diff | CI (block=20/draws=4000/seed=42) |
|---|---|---|---|---|
| n conditioned | 340 | 346 | — | — |
| n unconditioned | 1,141 | 1,135 | — | — |
| Win rate, conditioned | 66.47% | **47.98%** | — | — |
| Win rate, unconditioned | 41.72% | **47.22%** | — | — |
| WR diff | +24.75pp | **+0.75pp** | **-24.00pp** | `[-5.91pp, +7.18pp]` (**includes 0**) |
| Mean win, conditioned | +1.571R | **+1.045R** | — | — |
| Mean win, unconditioned | +0.860R | **+1.103R** | — | — |
| Mean-win diff | +0.711R | **-0.058R** | **-0.769R, sign-flipped** | `[-0.300R, +0.204R]` (**includes 0**) |

**Gate:** L1 (n≥30) PASS — 346 ≫ 30. L2 (WR-diff CI excludes 0) **FAIL** — CI includes 0. L3
(mean-win-diff CI excludes 0) **FAIL** — CI includes 0, and the point estimate is negative. L4
(conditioned WR ≥ 0.55) **FAIL** — 47.98% is below both the floor and the unconditioned baseline.
Per pre-reg §C: L1 passes but L2/L3 fail → `FALSIFIED`.

**Not a borderline result.** The corrected conditioned and unconditioned populations are
statistically indistinguishable on both win rate and mean win — the original +24.75pp/+0.711R
effect was entirely an artifact of the look-ahead-contaminated `bias_overnight` series.

### Audit hooks (corrected)

```bash
python lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py
# Expected (deterministic, seed=42, post data_lib.py fix): n_trades=1541, n_conditioned=346,
# WR conditioned=0.4798 / unconditioned=0.4722, mean-win conditioned=+1.0447 / unconditioned=+1.1030,
# WR-diff CI=[-0.0591,+0.0718], mean-win-diff CI=[-0.2997,+0.2044], VERDICT=FALSIFIED

# Confirm the upstream fix this correction depends on
grep -n "et_minute < RTH_OPEN_MIN" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py
```
