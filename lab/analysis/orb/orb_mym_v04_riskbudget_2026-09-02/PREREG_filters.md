# PREREG — ORB-MYM-1 v0.4 conditioning-filter screen (informal, Downloads lane)

**Frozen:** 2026-09-02, before any P&L-by-feature was computed. Written after (and only
after) Stage A (`build_features.py`): tag identification and the Pine read
(`orb_mym_4_edition.pine`). No conditional P&L was looked at before this file existed.

**Lane / status:** informal research on an untracked Downloads-lane construct
(CANDIDATE, never AUTHORIZED). No `register_search open` (no admission file, no repo
manifest); K is DISCLOSED here and must enter K accounting if any survivor is ever
re-proposed into the repo pipeline. Mechanism-first lane would refuse K≥4 at open —
this screen is therefore exploratory by construction, not admission evidence.

**Panel:** operator TV export `ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-01_76b9e.csv`
(1,849 exits / 703 traded days, 2020-01-02→2026-08-28, qty 2 const, long-only; Step-0
clean with `--tz UTC`). Bars: `core/data/bar_data/MYM_M15.csv` sha256 `24e16952…`
(2020-07-02→2026-07-02). **Scorable window = traded days with bars + 60-session warm-up:
598 days (Hot=160).** All comparisons (filtered vs base) are on this common window.

**Already considered (NOT proposed as new):** overnight-range P80 regime (= `Hot` tag,
label agreement 1.000 with the ledger's `on_elev80`), OR-volume floor (knob at 0.5×;
0.65/0.8/1.0 swept on v0.1), breakeven (DEAD), trail (DEAD), TP tightening (DEAD),
stall cut time (single-peaked at 13:00), scale-in count, session end, qty (flat).

## Named null

Zero association between an **ex-ante** day label and that day's strategy P&L,
**conditional on the label's own autocorrelation**: circular shift of the label series
over the time-ordered traded days (every distinct rotation enumerated, identity
included; n=598 ≤ 2,500). Unconditional long-only drift is common to both groups and
the shift preserves the kept-day count, so drift is not rediscovered as "edge".
Statistic: **lift = mean(day P&L | kept) − mean(day P&L | dropped)**, one-sided in the
pre-fixed direction. Sizing rules have no natural null; they are judged on the canonical
bust engine (below) by dominance.

## Primary set — K_primary = 3, Bonferroni α = 0.05/3 = 0.0167 (for the p-value-tested one)

| id | rule (ex-ante at 09:45 ET) | direction fixed a priori | rationale | test |
|---|---|---|---|---|
| **P1** | skip the day if the first OR-high breach (base-entry timestamp) is **after 11:00 ET** | kept (early) > dropped (late) | late breakouts have less session left to reach the adds; construct has no late-entry knob | lift + shift-null p; engine bust/pass at k=1,2 |
| **P2** | **Hot** days (overnight range ≥ P80, the existing tag) traded at **half size** (qty 1/leg vs 2) | downsize Hot | Hot days: 1.5× daily σ, 2× worst day; risk parity on the regime the operator already tags; tag is diagnostic-only today | engine ladder (dominance) |
| **P3** | days whose **OR range (09:15–09:45) > trailing-60-session median ORR** traded at half size | downsize wide-OR | SL = 2.5×ORR ⇒ $-risk/contract scales with ORR; fixed-contract sizing ignores it; threshold is self-normalizing (no free parameter) | engine ladder (dominance) |

**Engine protocol (mirrors `lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/bust_pass_sim.py`):**
`core/mc/simulation.py` `run_seed`/`simulate_path` verbatim; per-contract daily P&L
(day sum / 2) and MAE proxy (worst per-trade Adverse Excursion / 2) on `bdate_range`;
5-day week blocks; seeds (1,2,3) × **4,000 sims** (MC s.e. ≈ 0.45pp at 50%); horizon 1,500;
`dd_trigger=dd_scale=1.0` (protection rule off, as in the canonical harness);
`Tradeify_Select_100K` with consistency 0.40 (Run-2) and `Tradeify_Growth_100K`
(consistency None); **intraday-honest clock** (MAE proxy as `intraday_low`) is the
headline, EOD-clock reported for the base only. Sizing ladder: qty1-flat, qty2-flat,
rule (2 calm / 1 hot-or-wide). Filtered-out days = flat (0).

**Decision rules (frozen):**
- P1 "worth a TV-native A/B" iff shift-null p ≤ 0.0167 **and** intraday-honest bust% at
  k=1 (Select, Run-2) is ≥ 5pp lower than base **and** pass% not > 3pp lower than base.
- P2/P3 "worth a TV-native A/B" iff the rule is **not dominated** by either flat sizing
  (higher pass at ≤ bust, or lower bust at ≥ pass) on **both** tiers.
- Anything else: report, no recommendation.

## Exploratory looks — disclosed, counted, never claimed (≈ 25)

P1 threshold sensitivity 10:30 / 11:30 / 12:00 / 13:00 (4) · yesterday-RTH-range `bprime`
keep / drop (2) · |gap| ≥ P80 within NotHot, keep (1, one-sided per ledger calm-stratum
result) · OR-width/ATR keep-narrow / keep-wide (2) · 09:30-bar volume ToD-ratio > 1 keep
(1; ≈ the existing knob at 1.0×, engine-measured for the first time) · Hot-only /
NotHot-only (2) · day-of-week single-day drop (5) · overnight-return sign and prior-day RTH
sign (4; **raised-bar class — single-instrument directional timing — not proposable
without a Route 1/2/3 ruling, shown for disclosure only**) · prior-day CLV halves (2) ·
sizing variants at k=1 base (2).

**Total looks K ≈ 28.** Any exploratory hit is a hypothesis for a fresh, pre-registered
test on data this export never saw — not a result.

## Known limits (stated up front)
- No untouched holdout: v0.3 was TV-tuned on the full chart; v0.4 adds 2020–21 but the
  operator ran it end-to-end. Everything here is in-sample screening.
- MAE proxy is trade-level, not bar-level (same caveat as the recon-v3 measurement).
- v0.4's export does **not** reproduce M9 (v0.3) on the common window (N 1,258 vs 1,422;
  net +5.8%; maxDD +13%) despite the header's identity claim — unresolved, flagged.
- Bar coverage ends 2026-07-02; the last ~2 months of trades are unscored.

## Addendum 2026-09-02 (append-only; frozen definitions/directions unchanged)

1. **Day-of-week filter was ON in the export.** Raw-export census: Mon 223 / Thu 248 /
   Fri 227 traded days, **zero Tue/Wed entries** (0 of 1,849 entry rows). The Pine's
   defaults are all-ON; the operator's run had Tue+Wed off. Consequence: DoW is
   *already applied*, not an unconsidered filter; the 5 "drop-<day>" exploratory looks
   reduce to 3 informative ones (Tue/Wed cells are identity). Every number in this screen
   is conditional on a Mon/Thu/Fri schedule whose provenance is undocumented — a
   selection risk in its own right (BPC day-placebo lesson). 5 Sunday-dated "days" are
   holiday early-close EOD fills landing at the Sunday reopen; they have no session
   features and are outside the scorable window.
2. **Construction fix before the engine ran on a valid frame:** the trailing-60 median
   ORR used `min_periods=60`; 3 sessions with a missing 09:15/09:30 bar (ORR NaN)
   poisoned every following 60-session window, shrinking the scorable set 598→524.
   Changed to `min_periods=45`. Stage B was run once on the defective 524-day frame
   (results superseded, not deleted: `score_filters_results.csv` is overwritten by the
   re-run); Stage C (engine) was stopped before producing any cell. The P3 rule
   (`ORR > trailing median`) and every direction are unchanged.
3. Engine cells added (exploratory): Hot-only and NotHot-only at qty 2 (the as-run size),
   alongside the qty-1 versions already listed. K_total ≈ 30.
