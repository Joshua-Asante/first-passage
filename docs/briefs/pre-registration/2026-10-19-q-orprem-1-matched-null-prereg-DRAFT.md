# Q-ORPREM-1 — Does the opening range keep its premium when the placebo is equalized?

**Status:** `OPEN — DRAFT (pre-lock)`, revision 3. Not frozen, not ratified, not authorized to run. No data has been read for this study.
**Authored:** 2026-10-19
**Closed:** N/A
**Authors:** Joshua (direction: "Draft the H-A matched-null pre-registration for my review. Draft only: no runs, no data ruling assumed.") + Claude Code (Opus 5.5, session `local_da95ffcf`).
- "H-A" is this session's label from the 2026-10-18 ORB diagnosis (workflow `wf_47ae3056-307`). That diagnosis has no committed owner; this file is the durable record of H-A as **H-ORPREM**.
**Parent question:** N/A. Lineage: the within-day placebo in the [ORB-MNQ-1 pre-registration](2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) and lesson M-17.
**Loop:** Inquire-phase Pre-Q. Gates whether ORB-MNQ-1's "the opening range is structurally special" certification survives a placebo that reduces the remaining-time, width and cost differences between the OR and later windows.
**Artifact path:** `docs/briefs/pre-registration/2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md`
**Must run locally:** the inputs are vendor-licensed TradingView CME exports held only in the primary checkout (`core/data/tv_exports/cme/`, gitignored, hash-pinned).

---

## §0 — Rule 0 reads

All read 2026-10-18/19. Repository anchors are `git log -1` on main `3d396e2`. Archive anchors are commit `5d47b4dc` of `first-passage-archive`.

| Source | Anchor | Supplies |
|---|---|---|
| `lab/analysis/orb/orb_mnq_2026-07/RESULTS.md` | `027a729` | The audited claim: "structurally special" (:15, :35), placebo p=0.0040 with mean +0.0029 (:34-36). n 1,846 (:19); gross +0.0823R, t 2.97 (:21). 2021+ gross +0.1020R and net +0.0894R (:28-32). Long/short +0.070/+0.063 (:48). Per-year net. The survival rationale is geometric: the OR range is large against the spread, and the trade is intraday-complete (:52-55). |
| `ops/instruments/NQ.md` N1 (:49) | `461df9a` | A second live citation of the placebo result p=0.0040. |
| `docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md` | `027a729` | The frozen construct and its §5 forbidden moves; the 2021+ temporal override; DJ30's own placebo failure (p=0.194, :114); the NQ 2010–18 control, which needs Databento caches. |
| Archive `lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py` | blob sha256 `e8b0caf8…5e9259` | The engine (details below). |
| Archive `lab/analysis/orb/orb_mnq_2026-07/run_orb_mnq_bulenox_blusky.py` | `5d47b4dc` | The MNQ instrument and the cost formula (details below). |
| Archive `lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md` | `5d47b4dc` | The close_tod ladder. Its 11:45 row is the OR exiting at 12:00, i.e. this study's OR arm. Q-SESSCONF-1 FALSIFIED. |
| Archive `lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md` | `5d47b4dc` | Range per minute is a decaying U: 09:30 3.575 bp, midday about 1.5–1.6 bp. Later windows are narrower. |
| `ops/instruments/MNQ.md` (read in full) | `2dcc3cd` | Ledger facts (details below). |
| `ops/instruments/MECHANISMS.md` :26-37 | `461df9a` | `opening-range-breakout` carries only the ZB sign-reversed placebo (p=0.0010). `opening-range-continuation` on MYM failed its placebo (p=0.2144). |
| `docs/methodology/lessons/methodology_lessons.md` M-17 | `32f513e` | The same-day window-slide placebo rule, and its claim that the slide holds "price scale, volatility, range distribution, and cost fixed". |
| `docs/rejected_candidates.md` | `739cc3a` | The ORB-ZB entry (an OR placebo passing on an instrument with negative gross edge). The index-intraday OHLCV raised bar (:1664ff), whose scope excludes "the incumbent survivor". |
| `docs/adr/2026-08-30-candidate-contract.md` :33-36 | `2cefc0f` | A proxy diagnostic cannot open a contract, consume a Confirm holdout or claim candidate status. |
| `docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md` §2-B(1) :41-42, §5 :82 | `770413b` | The a-priori criterion rule: a criterion is "never chosen after seeing which moments performed, and never read off a scored list". No filter sweeps; the F2 guard is unchanged. |
| `docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md` §5 | `770413b` | The 15:30-exit bar on ORB-MNQ-1. |
| `docs/adr/2026-07-10-databento-research-stack.md`, addendum 2026-09-10 | `2cb980d` | Databento is retired, and retained vendor data carries no new usage rights. |
| `discovery_manifests/burned_segments.json` | `fcb4ac7` | MNQ 2025-09-01 → 2026-08-05 is burned; "a second consultation is forbidden". |
| `docs/pursuits/b3-orb-mnq-payability-line.md` | `770413b` | b3 PARK expires 2026-11-08. Re-entry needs "new payability / cost-geometry evidence at an admissible venue". |
| `core/data/tv_exports/cme/SHA256SUMS` | `67d1f8c` | Pins for `86a38` (line 9) and `dd9d8` (line 11). |
| `docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md`, addendum 2026-08-29 | `28863be` | Two-implementer test: worked examples are mandatory (§4.4). |
| `docs/briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md` | `1ee3f07` (merged `e2dd699`) | The v7 S4 contract. Its text records the effective freeze as pending (:3, :14 "committed freeze by October 23", :301) and scoring as held. Joshua's signed attestation commits him to "disclose any further exposure identified before freeze" (RATIFICATION :51). This draft does not assert the v7 freeze state; §7 gates on it instead. |

**Source details.**
- **orb_lib engine.**
  - `load_bar_export`, `session_panel` and `orb_backtest`.
  - `placebo_within_day`, whose `exec_win` closure works as follows:
    - it draws offsets from 1 to 23 (offset 1 overlaps the OR's second bar);
    - it exits at the RTH close;
    - it charges round-trip cost in each window's own range.
  - `CLOSE_TOD_US` is the last bar's *open*, so close_tod 11:45 means an exit at 12:00.
- **MNQ instrument (archive `run_orb_mnq_bulenox_blusky.py`).**
  - 15m bars from 09:30 to 15:45 ET; tick 0.25.
  - Cost formula: `rt_cost_pt = 2 × (cost_per_side_usd + $0.50 slip) / $2`. At Tradeify's $0.91 per side this is 1.41 pt.
- **MNQ.md ledger facts.**
  - N1–N4.
  - The F2 guard (:160).
  - `K_banked(MNQ)=22` (:72), with the ledger's own caveat that `mnq_dailygeom_notice_20260829` (K=5) is not yet reconciled (:176-177).
  - `K_eff = K_intrinsic`.
  - TV `1!` series are not back-adjusted. This was measured on other exports (:398).
  - Q-TODVOL-1 (:329).

**Instrument-profile consult** (sub-rule 8). The command was `.\fp.ps1 python scripts/instrument_profiles.py cell MNQ opening-range-breakout` (rc=1; first lines):

```
=== MNQ x opening-range-breakout ===
ledger: ops/instruments/MNQ.md
verdict: AMBIGUOUS-PARKED (2026-07-23)
  source: ../../docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md
  BLOCKING — a parked concept holds this cell and shares the instrument's anti-SNAG budget; address it (and any decision date) in the pre-registration.
class finding (mechanism-wide, not specific to MNQ): Equity-index-specific — ZB *fades* its opening range; the within-day placebo returned p=0.0010, sign-reversed. Do not transplant to a risk-off instrument. [ZB.md B1](ZB.md)
BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
```

How this draft answers each item:
- **BLOCKING (parked concept).** The parked concept is ORB-MNQ-1 itself (b3, decision date 2026-11-08). This study is a K=0 diagnostic of that concept's own certification. It proposes no new concept in the cell.
- **BINDING BAR.** The bar's scope "does not cover … the incumbent survivor". ORB-MNQ-1 is that survivor, and no new candidate is proposed.

### §0.1 — Literal search and pin output (sub-rule 8)

```
$ grep -n -i -E "placebo|opening.range|window.slide|matched.null|ORPREM" lab/CATALOG.md docs/briefs/INDEX.md | cut -c1-160
lab/CATALOG.md:92:| b2_london_fix_wake_2026-08-24 | CLOSED | B2.2 battery: 6E and 6B both DEAD via orthogonality (\|t\|<2/wrong-signed); placebo leg decisive on
lab/CATALOG.md:140:| harv_0_month_end_rebalance_es_2026-07 | CLOSED | H1 corroborated but placebo magnitude un-passable; successor pre-... | — | https://githu
lab/CATALOG.md:191:| orb_universe_2026-06-22 | ACTIVE | which FXIFY CFD best suits Opening Range Breakout | — | https://github.com/Joshua-Asante/first-passage

$ .\fp.ps1 python scripts/check_advisor_dedup.py --keywords "opening range placebo matched null window offset remaining time"
check_advisor_dedup: keywords: 'opening range placebo matched null window offset remaining time'
  slugs found:    (none)
  keywords found: 9 significant terms

POSSIBLE PRIOR ART — review before treating the keywords as new work (top 8 of 230 candidate(s)):

  [  9] ops/instruments/MNQ.md — INSTRUMENT LEDGER — MNQ
        shared terms: ['matched', 'null', 'offset', 'opening', 'placebo', 'range', 'remaining', 'time'] (+1 more)

  [  9] ops/instruments/SPX500.md — INSTRUMENT LEDGER — SPX500
        shared terms: ['matched', 'null', 'offset', 'opening', 'placebo', 'range', 'remaining', 'time'] (+1 more)

  [  8] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/05-cosmetic.md — 05 — COSMETIC tier (both rounds)
        shared terms: ['matched', 'offset', 'opening', 'placebo', 'range', 'remaining', 'time', 'window']

  [  8] ops/instruments/MECHANISMS.md — MECHANISMS — candidate mechanism vocabulary
        shared terms: ['matched', 'null', 'offset', 'opening', 'placebo', 'range', 'time', 'window']

  [  8] ops/instruments/MYM.md — INSTRUMENT LEDGER — MYM
        shared terms: ['matched', 'null', 'opening', 'placebo', 'range', 'remaining', 'time', 'window']

  [  8] ops/instruments/NAS100.md — INSTRUMENT LEDGER — NAS100
        shared terms: ['null', 'offset', 'opening', 'placebo', 'range', 'remaining', 'time', 'window']

  [  8] ops/instruments/PROFILES.md — INSTRUMENT PROFILES — mechanism x instrument verdict index
        shared terms: ['matched', 'null', 'offset', 'opening', 'placebo', 'range', 'time', 'window']

  [  7] docs/briefs/closures/MNQBASE-1-closure-intake-dry.md — `MNQBASE-1` Step 2 — CLOSURE: the intake well is dry, and it is dry at P2
        shared terms: ['matched', 'null', 'offset', 'opening', 'range', 'time', 'window']

$ git log --oneline -20
3d396e2 Merge pull request #872 from Joshua-Asante/claude/protection-recovery-native-execution-2d4c50
a9278d3 Merge pull request #866 from Joshua-Asante/claude/standing-ci-substitution
5980094 docs(notes): record operator rulings D-N1 to D-N3 in the native pilot runbook
a5440ad docs(notes): native protection and recovery pilot runbook and unproved controls (proposal)
e2dd699 Merge pull request #868 from Joshua-Asante/codex/orb-s4-freeze-controls
1ee3f07 Publish exact ratified ORB contract and signed exposure record
d0d12c3 Prepare bounded ORB solo release controls and record remaining blocker
f7c52a4 research: verify ORB executor preparation and reconcile approved budget
0da3101 research: prepare ratified ORB solo S4 freeze candidate
9078357 Merge pull request #871 from Joshua-Asante/claude/first-passage-handoff-d9ff87
75c983e Merge pull request #870 from Joshua-Asante/claude/state-weekly-roll-2026-10-23
2033921 docs(ledger): ORB setup exhausted after the 10-18 verification; prereg hash and K state
f453e59 docs(ledger): record Session Relay deliveries SR-2 to SR-4 (2026-10-18)
3bea81a docs(ledger): coordinator transfer to the Claude deployment coordinator (Joshua 2026-10-17)
da4aa80 docs(state): weekly roll to 2026-10-23 (bucket 10-19→10-23)
3d815e5 Merge pull request #865 from Joshua-Asante/claude/track-b-superseded-tradeify
669ee22 docs(agents): standing CI substitution for the local qualification-child timeout (Joshua 2026-10-16)
f46ad7b docs(state): Track B superseded for Tradeify (Joshua 2026-10-16)
a5c7133 Merge pull request #864 from Joshua-Asante/claude/s4-ceiling-orb-fxify
8931ba3 docs(adr): four-firm program — 5.0% ceiling, ORB MNQ v7 as the fresh §4 candidate, FXIFY Futures Flex registration (Joshua 2026-10-16)

$ sha256sum "BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-13_86a38.csv" "BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-21_dd9d8.csv"   # in core/data/tv_exports/cme, primary checkout, 2026-10-19
a369ad3e5967fb393c583a50b854e180ae74d9384829335e204a782192209c51 *BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-13_86a38.csv
8e156791c1331175cbcb1bcf516c4c62ae22102f3cd42fb958909b0d62db87ca *BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-21_dd9d8.csv

$ git show 5d47b4dc:lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py | sha256sum   # in first-passage-archive
e8b0caf8032439ced8b565df9ce3a3077c7b685c0ddfe6e093493d78f25e9259 *-
```

Each listed prior-art file was opened. None runs an equalized window-slide. The cosmetic-tier audit note and PROFILES are vocabulary hits only.

**Amendment-first.** No existing owner can hold a new study's frozen design. The parent pre-registration is frozen, and M-17 is a lesson, not a study.

---

## §1 — Context

ORB-MNQ-1's within-day placebo (p=0.0040) is the evidence that its opening range is "structurally special". Where it is cited:
- RESULTS.md :15 and :35;
- MNQ.md N1 and NQ.md N1;
- the archived ORB-MNQ-1 admission.

The same kind of test passed on NAS100 (p=0.014) and SPX500 (p=0.0123), and failed on DJ30 (p=0.194) and on NAS100 before 2020 (p=0.133).

The placebo pits the OR (09:30–10:00, held about six hours) against later two-bar windows that differ in three ways:
- **Cost.** It scores net of cost in each window's own range, and later windows are narrower. This handicaps them by construction.
- **Remaining time and width.** Later windows have less session left and a smaller range. Under a driftless path with fills at the levels, gross R has zero expectation at any width or hold.
  - The engine's both-touch rule is exact: such a bar is −1R whichever level was touched first. In this engine a stop on the entry bar happens only on a both-touch bar.
  - So time and width differences can favour the OR only through continuation, which a longer hold captures more of and which scales as drift/ω in R.

So the open question is whether the OR's gross continuation exceeds that of later windows once hold and width are made comparable. A positive answer means OR-specific information. The 2026-10-18 diagnosis ranked this unaudited.

---

## §2 — Prior art and lineage

- **M-17** (CANDIDATE). This study tests whether M-17's null is adequate. It is not offered as the "second use" M-17's promotion needs.
- **Q-SESSCONF-1** (FALSIFIED 2026-08-02). Truncating the OR's own hold does not pay. The door to adopting a shorter hold is closed. It says nothing about later windows.
- **Q-TODVOL-1** (D2 FAIL 2026-08-20). A later-bar range trigger had no continuation edge, +0.25 pt against a 2.82 pt bar. This is a different construct, measured in points.
- **Placebo record across instruments.**
  - Pass: MNQ (0.0040), NAS100 2020+ (0.014), SPX500 (0.0123), ZB sign-reversed (0.0010).
  - Fail: DJ30 (0.194), NAS100 2014–19 (0.133), and MYM opening-range-continuation (0.2144, a different construct).
  - The geometry premise reads the failures as instruments or eras with no continuation to scale, so they are consistent with it. The ZB case shows a placebo pass is not edge.
- **D5-RECOST.** Unconditional NQ intraday momentum is absent on modern MNQ.
- **Era dependence.** ORB-MNQ-1 is era-bound (N1). The 2021-09-28 break is unexplained (Q-ORBCUSH-1, Q-ORBPOS-1).
- **What is novel here.** No study has compared the OR with later windows at equal remaining time, comparable width and zero cost.

---

## §3 — Question

**Q-ORPREM-1:** How much of the opening range's measured advantage over later same-day windows remains when the comparison holds remaining time equal, makes width comparable and removes cost?

---

## §4 — Hypothesis, estimator and frozen thresholds

**H-ORPREM:** once remaining time is equal, width is matched and cost is removed, the cash-open OR earns no gross premium of decision size over later two-bar windows on the same days. The placebo's advantage is then attributable to the recorded width, cost and hold geometry, not to auction-specific information.

- **Reject H-ORPREM if** the premium Δ₃ has a one-sided 97.5% lower bound above 0. The OR is then special beyond the matched geometry: the result is falsified.
- **Accept H-ORPREM if** Δ₃ has a one-sided 95% upper bound below m = 0.032R.
- **Ambiguous-hold if** neither condition holds.

### §4.1 Data and sample

- **Panels.**
  - **E2 (primary):** 2021-01-01 → 2025-08-31, from `BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-21_dd9d8.csv` only (sha256 `8e156791…87ca`).
  - **E1 (report only):** 2019-09-01 → 2020-12-31. It uses `…_2026-07-13_86a38.csv` (`a369ad3e…9c51`) for dates up to 2020-06-30 and `dd9d8` from 2020-07-01.
  - Both files are loaded by `orb_lib.load_bar_export`, unchanged.
- **Date cut.** Immediately after decoding, rows dated after 2025-08-31 are dropped, before any statistic is computed. The G0 record asserts that the maximum date is no later than 2025-08-31. The decode-rate gate counts rows only.
- **Eligible session.**
  - The RTH session has all 26 fifteen-minute bars (bar opens 09:30 … 15:45 ET).
  - The previous eligible session exists, and its mean bar range Aₐ = mean(high − low) over its 26 bars is greater than 0. That session may lie before the window start; for example, E2's first session takes Aₐ from 2020-12-31 in `dd9d8`.
  - It passes the **intra-RTH discontinuity guard**: no RTH bar opens more than 0.5% from the close of the bar before it in the export. For the 09:30 bar, that is the 09:15 Globex bar. Excluded sessions are listed.
  - The guard does not see roll gaps at session boundaries. Those cannot affect intraday R.
  - Eligibility uses prices only.

### §4.2 Trade rule

Δ₁–Δ₃ use gross R (zero cost). Δ₀ alone is net. The engine is the frozen ORB-MNQ-1 rule with one change, a fixed horizon.

1. **Window.** For session d and offset w, the window is bars w and w+1.
   - Range ω = max(high) − min(low). If ω ≤ 0, the window is skipped.
   - Width covariate x = ln(ω / Aₐ).
2. **Horizon.** Bars w+2 … w+1+H. Primary H = 8. For "exit at close", the horizon runs to the 15:45 bar.
3. **Entry.** The first horizon bar whose high ≥ the window high (long) or whose low ≤ the window low (short), filled at that level.
   - If a bar touches both levels, the side is long when the bar's open ≤ the window midpoint.
   - If no bar touches either level, R is undefined and the window is dropped.
4. **Exit.**
   - The stop is the opposite extreme.
   - The trade is stopped if any bar from the entry bar through the end of the horizon touches the stop (the inherited approximation includes the entry bar). It exits at the stop level.
   - Otherwise it exits at the close of the last horizon bar.
5. **R** = signed P&L / ω. For Δ₀ only, subtract `rt_cost_pt` 1.11 before dividing.
6. **Offsets.**
   - OR: w = 0. Bars 09:30–10:00; its H = 8 horizon ends at 12:00.
   - Null: w ∈ {2, …, 16}. Offset 1 overlaps the OR. Offset 16 is the last whose horizon ends by 16:00.

**Why H = 8.** H = 8 is where the OR's horizon ends at 12:00 while 15 null offsets (10:00 through 13:30 starts) all complete by 16:00.
- **Disclosed:** H was set by an author who had already seen the close_tod ladder (§8). Its 11:45 row is this OR arm's construct, net, on Databento.
- **Effect on Δ₃:** the null arm is truncated to H too, so the sign of the effect is unknown. Δ₁ − Δ₂ shows the truncation effect.
- **Not adoptable:** the 12:00 end is a measurement convention, not an exit any construct may adopt (§5).

### §4.3 Primary estimator Δ₃ (fixed in full before any R is computed)

1. **Trim band (common support).**
   - The band is [p5, p95] of x over all eligible E2 OR windows with ω > 0. Quantiles use `numpy.quantile` (default linear method) and the band is inclusive.
   - **Both arms** are trimmed to it: OR and null windows outside the band leave Δ₃.
   - The untrimmed OR mean is reported alongside.
2. **Cutpoints.**
   - Quintile cutpoints c1…c4 of x over the trimmed OR windows, same method.
   - Strata are [band low, c1), [c1, c2), [c2, c3), [c3, c4) and [c4, band high].
   - Band and cutpoints are prices only, fixed once, and used unchanged for E1 and in every bootstrap replicate.
3. **Strata.** Assign each trimmed OR and null window to s = 1…5.
4. **OR mean.** R̄_OR = mean of the defined R of trimmed OR windows.
5. **Weights.** p_OR(s) = the share of those defined OR trades that fall in stratum s.
6. **Matched null.** N̄ = Σₛ p_OR(s) · mean{defined null R in s}.
   - In any replicate where a stratum has no defined null R, p_OR is renormalised over the non-empty strata.
   - The count of such replicates is reported. It is not a routing trigger.
7. **Premium.** Δ₃ = R̄_OR − N̄.

**Inference.**
- Moving-block bootstrap over eligible sessions in date order, non-circular, as in `orb_lib.block_bootstrap_ci`.
  - Block length 5. Block starts are drawn uniformly from [0, N−5]. Use ⌈N/5⌉ blocks, truncated to N sessions.
  - B = 10,000, seed 42.
- Every window of a resampled session moves with it. p_OR(s) and the stratum means are recomputed; the cutpoints and trim band are not.
- Bounds are percentiles: the 2.5% percentile (one-sided 97.5% lower) and the 95% percentile (one-sided 95% upper).
- Reported only: seeds 123 and 2026, and a 10-session block.

**Ladder.** Each rung is the OR mean minus a null mean on E2, with its bootstrap interval. "Unweighted" means the pooled mean of every defined null R. Only Δ₃ gates.

| Rung | Construction | Role |
|---|---|---|
| Δ₀ | Net (`rt_cost_pt` 1.11, the recorded Bulenox basis); exit at close; null w ∈ {1…23}, unweighted | Equalization baseline. It approximates the certified comparison on this feed. |
| Δ₁ | Gross; exit at close; null w ∈ {2…23}, unweighted | Removes cost and the offset-1 overlap. |
| Δ₂ | Gross; H = 8; null w ∈ {2…16}, unweighted | Reduces the remaining-time difference. |
| Δ₃ | Gross; H = 8; width-matched as above | Primary: also reduces the width difference. |

Also reported:
- The attribution Δ₀−Δ₁, Δ₁−Δ₂ and Δ₂−Δ₃.
- E1's Δ₃ and N̄ against E2, with no gate.

**Why m = 0.032R.** m is twice the OR's round-trip cost in R at the Tradeify basis over the E2-proxy era.
- On the 2021+ panel, the recorded cost is 0.1020 − 0.0894 = 0.0126R at `rt_pt` 1.11.
- Scaled to 1.41 (`firm_rules` Tradeify $0.91 per side plus 1 tick) that is 0.0160R; twice that is 0.032R.
- A premium below m cannot, by itself, reach half of the 4× cost-law bar.

**Remaining confound (a named limitation).**
- x is normalised by the previous session's mean bar range, not by range at that time of day, so width matching favours high-activity null windows.
- The OR horizon (10:00–12:00) and the null horizons are not volatility-matched.
- The residual plausibly runs against the OR. It therefore mainly weakens a RESOLVED reading.

### §4.4 Worked examples (two-implementer check; synthetic data, H = 2)

**Example 1** (7-bar day; bars given as open, high, low, close):

| Bar | O | H | L | C |
|---|---|---|---|---|
| b0 | 100 | 104 | 98 | 102 |
| b1 | 102 | 105 | 99 | 103 |
| b2 | 103 | 106 | 102 | 105 |
| b3 | 105 | 109 | 104 | 108 |
| b4 | 108 | 110 | 107 | 109 |
| b5 | 109 | 109.5 | 101 | 102 |
| b6 | 102 | 103 | 100 | 101 |

| Window | hi, lo, ω | Horizon | Entry | Stopped? | Exit | R |
|---|---|---|---|---|---|---|
| OR w = 0 (b0–b1) | 105, 98, 7 | b2–b3 | b2 high 106 ≥ 105, long at 105 | lows 102, 104 > 98: no | b3 close 108 | **+0.4286** |
| w = 2 (b2–b3) | 109, 102, 7 | b4–b5 | b4 high 110 ≥ 109, long at 109 | b5 low 101 ≤ 102: yes | 102 | **−1.0000** |
| w = 3 (b3–b4) | 110, 104, 6 | b5–b6 | b5 low 101 ≤ 104 (high 109.5 < 110), short at 104 | highs 109.5, 103 < 110: no | b6 close 101 | **+0.5000** |

**Pooling with a second day.**
- Day 2, given directly: the OR has R −1.0000 in stratum B; null w = 2 has R +0.2000 and w = 3 has R −0.4000, both in stratum A.
- Day 1: the OR and w = 2 are in A; w = 3 is in B.
- R̄_OR = (0.4286 − 1.0000)/2 = −0.2857, with p_OR(A) = p_OR(B) = 0.5.
- Null stratum means: A = (−1.0 + 0.2 − 0.4)/3 = −0.4000; B = +0.5000.
- N̄ = +0.0500, so **Δ₃ = −0.3357**.
- The unweighted null mean is −0.1750, so Δ₂ = −0.1107.

**Example 2** (edge cases). One window, hi 10 and lo 8 (ω = 2, midpoint 9), with Aₐ = 4, so x = ln(0.5) = −0.6931.
- **(a) Both-touch bar.** The first horizon bar is O 8.8, H 10.5, L 7.5. Both levels are touched, and the open 8.8 ≤ 9, so the trade is long at 10. The stop at 8 is touched on the same bar, so it is stopped: R = (8 − 10)/2 = **−1.0000**.
- **(b) Undefined.** Both horizon bars have highs ≤ 9.5 and lows ≥ 8.5. No entry occurs, R is undefined, and the window leaves every mean.
- **(c) Trim.** If the band's low end is −0.5000, this window (x = −0.6931 < −0.5000) leaves Δ₃ whatever its R and whichever arm it belongs to. The trim uses x only.

Phase 0 encodes both examples as unit tests.

### §4.5 Power and expected outcome (INFERRED, stated before any read)

- **Inputs.**
  - The recorded gross σ is about 1.19R (0.0823 × √1846 / 2.97).
  - E2 has about 1,170 sessions, and within-session pairing applies, so SE(Δ₃) is taken to be 0.03–0.04R. Trimming both arms to the band removes about 10% of OR windows, which raises SE slightly.
- **Decision rules.**
  - FALSIFIED needs Δ̂₃ > 1.96·SE.
  - RESOLVED needs Δ̂₃ + 1.645·SE < 0.032.
- **Normal-approximation verdict probabilities, at SE = 0.035R.** Across SE 0.03–0.04, P(decisive) moves by up to about ±0.13 from these:

| True Δ₃ | −0.02 | 0.00 | +0.02 | +0.04 | +0.06 | +0.08 | +0.10 |
|---|---|---|---|---|---|---|---|
| P(FALSIFIED) | 0.01 | 0.02 | 0.08 | 0.21 | 0.40 | 0.63 | 0.82 |
| P(RESOLVED) | 0.44 | 0.23 | 0.10 | 0.03 | 0.01 | 0.00 | 0.00 |
| P(AMBIGUOUS) | 0.56 | 0.74 | 0.82 | 0.76 | 0.59 | 0.37 | 0.18 |

- **Expected values.**
  - Δ₀ ≈ +0.10R, from the recorded 2021–2025 per-year net figures less a placebo mean of about 0.003.
  - Δ₀ − Δ₁ ≈ 0.01–0.015R. This is the cost difference implied by the range-per-minute profile.
- **Expected verdict.**
  - AMBIGUOUS is the most likely verdict for true Δ₃ between about −0.026R and +0.07R.
  - FALSIFIED becomes more likely than not only above about +0.07R, where the OR keeps most of its edge.
  - RESOLVED becomes more likely than not only below about −0.026R, where the OR underperforms the matched null.
  - Even if H-ORPREM is exactly true (Δ₃ = 0), P(RESOLVED) is only 0.23.
- **VOID-SUPPORT routing.** Its probability is unknown before G0. G0 decides it from prices alone, before any R.
- **The sample cannot grow** inside this Q (§5). This is why AMBIGUOUS edits nothing (§6).

---

## §5 — Forbidden moves

- **Adopting anything this study measures** into a construct, filter or session rule: the H = 8 hold, the 12:00 OR horizon end, any offset, width stratum or window.
  - The parent pre-registration's §5, the MNQ.md F2 guard, ADR 2026-07-31 §5 and Q-SESSCONF-1 close these doors.
  - ADR 2026-08-10 §2-B(1) bars any later criterion read off these outputs.
- **Using the retained Databento caches, or running the NQ 2010–18 control,** without an explicit operator data ruling. Retirement grants no right to use them, and no ruling is assumed.
- **Computing any statistic on dates after 2025-08-31.**
- **Choosing H, the strata, the trim band, m or the block length after any R exists, or adding unlisted sensitivity analyses.**
  - Considered at design and excluded: a parametric extrapolation null, which predicts outside the null's support, and an H sweep.
- **Treating the result as v7 evidence, payability or cost-geometry evidence, b3 re-entry or non-re-entry evidence, or a reason to touch ORB S4 or its held budget.**
- **Rescuing an AMBIGUOUS result** with more eras, another horizon or another feed inside this Q.

---

## §6 — Gate

**Order of evaluation:** VOID-PARITY, then the VOID-SUPPORT routing, then FALSIFIED → RESOLVED → AMBIGUOUS.

| Verdict | Trigger | Disposition |
|---|---|---|
| `VOID-PARITY` | Either the harness fails a Phase 0 test, or the decode rate on `dd9d8` is below 99%. The decode rate is the rows `load_bar_export` returns after its dedup, divided by the file's `Entry` rows | `ITERATE` — fix the named defect and re-run once from Phase 0; a second VOID ends at STOP. If the overlap check fails — fewer than 99.5% of overlapping RTH bars (matched on epoch) agree on open, high, low and close within 0.25 — drop only the E1 report |
| VOID-SUPPORT routing (decided at G0 from prices only, before any R) | Any one of, in any stratum: fewer than 200 trimmed null windows; null windows from fewer than 100 distinct sessions; fewer than 5 distinct offsets; or a gap of more than 0.10 between the mean x of trimmed null windows and that of trimmed OR windows. Windows are counted whether or not they would trade | Not a verdict. Δ₂ becomes the primary (remaining time and cost only), with the same thresholds. Every label carries "width unmatched", and the disposition texts below drop every width claim: "time- and cost-matched"; "the recorded cost and hold geometry" |
| `FALSIFIED` (the OR premium survives the matched comparison) | One-sided 97.5% lower bound of Δ₃ > 0 | `INTEGRATE` — note at RESULTS.md §Verdict, MNQ.md N1, NQ.md N1 and M-17 that the anchor premium survives a time-, width- and cost-matched placebo, with the §4.3 remaining confound named; add a class note under MECHANISMS `opening-range-breakout`. Doc-only |
| `RESOLVED` (no premium of decision size) | One-sided 95% upper bound of Δ₃ < 0.032R | `INTEGRATE` — caveat "structurally special" at RESULTS.md :15/:35, MNQ.md N1 and NQ.md N1: the placebo premium is attributable to the recorded width, cost and hold geometry, and no auction-specific information is shown beyond it. Name the §4.3 remaining confound, which weighs mainly against this reading. Amend M-17 (the slide is not anchor-only); add a MECHANISMS class note |
| `AMBIGUOUS` | Neither | `STOP — underpowered`. The closure records the interval and the ladder. Make **no** edit to N1, NQ.md, RESULTS.md or M-17. Any re-test, possible only if a later data ruling admits more sessions, is a new Q-ID with its own pre-registration |

**Feed-scoped label (reported, not a verdict).** If Δ₀'s E2 point estimate falls outside [+0.05, +0.15]R:
- every label carries "feed-scoped";
- FALSIFIED and RESOLVED become `STOP — feed-scoped`, recorded in the closure only, with no edit to RESULTS.md, N1, NQ.md or M-17, because the study then does not speak to the Databento certification.

**Freezing.** Thresholds freeze at ratification. Amending them after any R exists is Known Trap #12.

---

## §7 — Execution plan (not authorized by this draft)

- **Phase 0 — build (synthetic data only).**
  - New camp `lab/analysis/orb/orprem_mnq_2026-10/`.
  - It vendors `orb_lib.py` as an LF byte copy of `git show 5d47b4dc:lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py` (sha256 `e8b0caf8…5e9259`). The file is marked `-text` in the camp's `.gitattributes` so line endings cannot change.
  - The harness imports only that copy and writes the sha256 of `orb_lib.__file__` into every record.
  - New function `exec_win_h(day, w, H)`.
  - Test (a), reference parity. `exec_win` is a closure inside `placebo_within_day`, so a verbatim copy of its body lives in the test file as the reference. With H set to the remaining bars and zero cost, `exec_win_h` must equal that reference on synthetic sessions, and must equal `orb_backtest` at w = 0.
  - Test (b): both §4.4 examples.
  - Test (c): decoding a synthetic v0.2 export. MNQ.md records a v0.2 break in a different loader.
  - Test (d): cutpoints, trim and renormalisation.
  - Test (e): bootstrap determinism.
- **Phase 1 — G0 blind pre-flight (prices only, no R).**
  - Re-hash both CSVs; decode; apply the date cut.
  - Overlap check (E1 only); decode rate; eligibility and guard lists.
  - Trim band, cutpoints, support and balance checks, and the routing decision.
  - Commit the G0 record `lab/analysis/orb/orprem_mnq_2026-10/G0.json` before Phase 2. It carries `max_session_date`, `orb_lib_sha256`, the input hashes and the routing.
- **Phase 2 — one scoring run.**
  - **v7 gate.** It may start only after either the v7 S4 owner records the S4 freeze as effective at a named commit (the scoring code commit must descend from it), or Joshua rules that this study's exposure enters the v7 disclosure.
    - Q-ORPREM-1 tests the ORB-MNQ-1 anchor, not v7. Waiting costs a K=0 diagnostic nothing.
    - It keeps the v7 attestation's "before freeze" disclosure promise intact.
  - Output: the ladder Δ₀–Δ₃ on E2 and the E1 report, written to `run_records/<run_id>/record.json` and committed. The record carries the input hashes, `orb_lib_sha256`, `code_commit` (the commit the run executed at), the seed and `max_session_date`.
- **Phase 3 — verdict.** Apply §6 mechanically and write the closure (§9).

**Budget (Rule 2).**
- Phase 0: about 1 agent-day. Phases 1–3: about 0.5 agent-day.
- Bound: 2 agent-days. Reaching the bound triggers reassessment, not expansion.
- Under 1 CPU-hour on the operator laptop. $0.
- About 30 operator minutes.
- Executor: an authorized local Claude session. Not GLM and no external service.

---

## §8 — K, exposure and authority

**K.**
- `K_intrinsic = 0`, on the precedent of the K=0 diagnostics OPENPRESS-1, ORB-ZB and Q-SESSCONF-1. Candidate contract :33-36 bounds what such a diagnostic may claim: no contract, no Confirm, no candidate status.
- No manifest.
- `K_banked(MNQ) = 22` is disclosed as recorded. The ledger notes that the K=5 `mnq_dailygeom_notice_20260829` manifest is unreconciled, which would make it 27. Re-read `discovery_manifests/` at freeze.

**No-adoption.** Any later candidate citing these outputs lists them as exposure. Under ADR 2026-08-10 §2-B(1), it may not take its criterion from them.

**Exposure: what the author (session `local_da95ffcf` and workflow `wf_47ae3056-307`) has seen.**
- **The OR arm's construct at H = 8.** The sessconf close_tod 11:45 row: n 1,796, meanR +0.0361 (net, rt 1.41, Databento `_mnq_15m.pkl`, 2019-05 → 2026-07). The full ladder.
- **ORB-MNQ-1 RESULTS.** Full-window, 2021+, per-year, long/short and placebo summary figures.
- **TV-panel ORB figures in MNQ.md:**
  - N2: n 1,026 entries; penetration 81/64 ticks.
  - N3: TV baseline +0.099, E_best +0.088, tighter stops −0.03 to −0.06R, give-back 0.50R.
  - N4: 2026 harness −0.0118 against TV −0.0246, n 136.
- **b3.** An unconditioned win rate of 41.72% and a mean win of +0.860R.
- **Other.** The EODADV range profile; NAS100 OR15/30/45; D5-RECOST; Q-TODVOL-1; ORB recon-v3, payability and v7-research summaries.

**Exposure: what the author has not seen.** Any R for a non-OR window at H = 8. Any per-offset or width-stratified R. Any gross E2 statistic on `dd9d8`.

**Design choices made with that knowledge.** H (§4.2); m (anchored to recorded cost); E2 (pre-declared earlier).

**Attestation and GO.** Joshua's attestation is owed at ratification. Execution needs Joshua's ratification words and a separate run GO; this draft authorizes neither.

**Decision this changes.** Whether the "structurally special" wording at RESULTS.md, MNQ.md N1 and NQ.md N1, and the M-17 null, stand as written or carry a geometry caveat. That in turn decides whether a future ORB-family candidate's Req-1 claim may cite the anchor premium.

**What it does not decide.** b3: re-entry needs payability or cost-geometry evidence at an admissible venue, which this study cannot supply.

---

## §9 — Closure

- **File:** `docs/briefs/closures/Q-ORPREM-1-closure-<verdict>.md`, from `references/closure_record.md`.
- **Contents:**
  - the G0 record;
  - the ladder;
  - every bound against its threshold;
  - the labels (width unmatched, feed-scoped);
  - predicted versus actual (§4.5);
  - the typed `## Iterate` block.
- **Registry:** `n/a — K=0 diagnostic, not a candidate` (every verdict).
- **Board write:** none unless an INTEGRATE edit is left owed.

---

## §10 — Audit hooks

Run from the primary checkout, `C:/Users/joshu/multi_firm_operations`:

```bash
# Git Bash: inputs and vendored engine unchanged
P=C:/Users/joshu/multi_firm_operations; CAMP=$P/lab/analysis/orb/orprem_mnq_2026-10
( cd "$P/core/data/tv_exports/cme" && sha256sum -c <(grep -E "_86a38.csv|_dd9d8.csv" SHA256SUMS) )
test "$(sha256sum "$CAMP/orb_lib.py" | cut -d' ' -f1)" = e8b0caf8032439ced8b565df9ce3a3077c7b685c0ddfe6e093493d78f25e9259 && echo ENGINE_OK
```

```powershell
# PowerShell, primary checkout. Checks: dates and engine hash in G0.json and every run record;
# G0.json was first added strictly before each run's code_commit; each code_commit descends from the v7 gate commit.
$camp = "lab/analysis/orb/orprem_mnq_2026-10"; $E = "e8b0caf8032439ced8b565df9ce3a3077c7b685c0ddfe6e093493d78f25e9259"
$v7 = "<v7 freeze commit named at ratification; omit this check if Joshua ruled disclosure instead>"
$commits = .\fp.ps1 python -c "import json,glob,sys; c,E=sys.argv[1],sys.argv[2]; rs=[json.load(open(f)) for f in glob.glob(c+'/run_records/*/record.json')]; g=json.load(open(c+'/G0.json')); assert rs and all(x['max_session_date']<='2025-08-31' and x['orb_lib_sha256']==E for x in rs+[g]); print('\n'.join(x['code_commit'] for x in rs))" $camp $E | Where-Object { $_ -match '^[0-9a-f]{40}$' }
$g0 = git log --diff-filter=A --format=%H -- "$camp/G0.json" | Select-Object -Last 1
foreach ($c in $commits) {
  git merge-base --is-ancestor $g0 $c; if ($LASTEXITCODE -ne 0 -or $g0 -eq $c) { throw "ORDER_FAIL $c" }
  git merge-base --is-ancestor $v7 $c; if ($LASTEXITCODE -ne 0) { throw "V7_GATE_FAIL $c" }
}
"DATE_ENGINE_ORDER_OK"
# harness tests, including both §4.4 examples
.\fp.ps1 python -m pytest $camp -q
```

## Verification

```powershell
.\fp.ps1 python scripts/check_brief.py docs/briefs/pre-registration/2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md --type inquire
.\fp.ps1 python "$env:USERPROFILE\.claude\skills\brief-authoring\scripts\check_brief.py" docs/briefs/pre-registration/2026-10-19-q-orprem-1-matched-null-prereg-DRAFT.md --type inquire
```

## Change history

- **Revision 1, 2026-10-19.** Initial draft. The pre-ratification panel (`wf_545a8c9a-c0b`) returned BLOCKED.
- **Revision 2, 2026-10-19.** Folds the panel's four BLOCKERs:
  - B1: corrected the exposure list and the reason for H;
  - B2: literal search output;
  - B3: power table, and AMBIGUOUS now edits nothing;
  - B4: RESOLVED wording; b3 routing removed.
  - It also folds concerns C1–C15 and the NITs.
- **Revision 3, 2026-10-19.** Folds the fold-check (`wf_a456296b-f8d`):
  - **v7 freeze state.** No longer asserted; Phase 2 gates on a recorded v7 freeze or Joshua's disclosure ruling.
  - **Common support.** Both arms are trimmed to the band, with the balance check on trimmed windows, and the bootstrap-renormalisation trigger is dropped.
  - **Width wording.** Width claims are removed from routed dispositions, and the remaining confound is named in RESOLVED.
  - **Feed-scoped case.** It now edits nothing.
  - **Power prose.** Corrected to match the table.
  - **Engine claim.** The both-touch claim is corrected and the engine-approximation G0 rates are removed.
  - **Vendored engine.** The engine copy is pinned, and the audit hooks are rebuilt to assert.
  - **AMBIGUOUS re-test.** It is a new Q-ID.
  - **Two-implementer gaps.** Closed.
- **Left to the operator (D1 and B3(c)):** whether to run at all. A decisive verdict is unlikely unless the OR keeps most of its edge (Δ₃ ≳ +0.07R) or trails the matched null (Δ₃ ≲ −0.026R).
