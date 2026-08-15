# Q-ICT-1H-REVCON-1 / Phase 0b — VERDICT PRE-REGISTRATION (multi-regime confirmatory)

**Registered BEFORE the longer multi-regime 1H export is scored. No criterion below may move after the first scored 0b run. The commit of this file is the firewall lift.**

> **SCORED 2026-06-19 → VERDICT: AMBIGUOUS → CLOSED NOT-CONFIRMED.** Confirmatory run on the out-of-sample 2022-bear page (14615 bars, committed harness/PREREG `760435d` preceded the page — firewall clean). The 0a headline cell non-replicated (0.60→0.46); the only stride-clearers are bias-drift near-misses failing the robust block CI → no full-gate clearance. Disposition: forward-watch belt, campaign closed. Full record: [`CLOSURE-1H-REVCON-AMBIGUOUS.md`](CLOSURE-1H-REVCON-AMBIGUOUS.md).

Parent: [`Q-ICT-REVCON-PLAN.md`](Q-ICT-REVCON-PLAN.md) (§3 Q-ICT-1H-REVCON-1, §4 H-1H-REVCON, §6 Phase-0 gate)
Inherits frozen config from: [`../ict_cascade_2026-06-18/PREREG-1H.md`](lab/archive/ict_cascade_2026-06-18/PREREG-1H.md) (the 1H layer config is REUSED; the reversion VERDICT is not)
Authored: 2026-06-19 · **Status: RATIFIED 2026-06-19 (operator-delegated "best judgement") — commit BEFORE the 0b export is scored (firewall lift).** All four genuine choices resolved below (bias-sign sole partition; ER regime dropped). The only remaining gate is operator confirmation that a multi-regime 1H export is obtainable (TV 1H caps at ≈6.5 mo).

> **Phase 0a (the existing 6.5-mo `PEPPERSTONE_US500, 60_a6b6b.csv`) is EXPLORATORY** — it generates the continuation/conditional hypothesis and may NOT be read as a verdict (the reversion FALSIFIED was already produced on that exact data; a second hypothesis on the same data is hypothesis-generation, not confirmation — parent §5, INQHIORI §5). This PREREG governs the **fresh 0b multi-regime export only.**

---

## §0 — Rule 0 citation (same chain as the parent §0)

Gitignored Pine, citation-chain mode. Re-anchor on resume:
- `ict_1h_premium_discount_DRAFT.pine` — **7554 B / 2026-06-18T22:42:04Z** (zone L44-57; zoneGate L65-72; follow-through L80-86; exports L143-149).
- `harness_1h.py` — working tree, M-15-fixed decision-bar `recompute_hits` (the Phase-0a base; the continuation probe is added ON TOP, reusing stride/block/placebo/effective_n).
The 0b export must use **lookN==60, eqBand==0.05, fwdK==12** (the PREREG-1H frozen config — or the partition/agreement comparisons are meaningless).

---

## Test object — frozen configuration

| Parameter | Value | Status |
|---|---|---|
| anchor rule | `lookback-extremes` | LOCKED (inherited; gate-relevant) |
| lookN / eqBand / fwdK | 60 / 0.05 / 12 | LOCKED (inherited from PREREG-1H) |
| zone polarity | +1 premium, −1 discount, 0 EQ stand-down | LOCKED (lib `pd`) |
| **reversion rate** | premHit = (zone==+1 → close[+fwdK] < close) ; discHit = (zone==−1 → close[+fwdK] > close) | LOCKED (decision-bar; the M-15-correct form) |
| **continuation rate (NEW)** | premUp = (zone==+1 → close[+fwdK] > close) ; discDown = (zone==−1 → close[+fwdK] < close) | LOCKED definition (the explicit complement-direction measure) |
| verdict instrument | de-overlapped OFFLINE estimate (stride-by-fwdK=12 primary + moving-block bootstrap block=12 cross-check) | LOCKED (reused) |
| feed | canonical TV/Pepperstone US500, native 1H, **multi-regime window** (via BAR_EXPORT) | LOCKED |

**Note on complement:** unconditionally, continuation ≈ 1 − reversion − (EQ/flat), so the *unconditional* direction flip is near-trivial and is NOT the test. The test is **conditional** (below): does the winning direction FLIP across partitions?

---

## Data pathway + discriminator design (ADDED 2026-06-19; validated)

**Data source (replaces the indicator-export path; the 1H indicator export caps at TV's ~6.5-mo single-regime limit):**
- **1H OHLC** ← **BAR_EXPORT v0.1 pages** (`core/bar_export_loader.decode_bar_signal`), multi-page concat. **Parity VALIDATED 2026-06-19:** on the 0a overlap, BAR OHLC is **byte-identical** to the TV chart feed (2922/2922 bars, max |Δ|=0.000000 on O/H/L/C) — the §4 same-feed / §6 path-independence requirement is met by *identity*.
- **zone** ← offline `H.zone_series(60, 0.05)`. **VALIDATED:** reproduces Pine's exported `zone` at **100%** (2862 non-warmup bars, both feeds).
- **structBias** ← offline `close vs weekly EMA-20, prior-week [1] lag` — the **FAITHFUL gate definition**, confirmed by Rule-0 Pine read: `ict_1m_execution_DRAFT.pine` L103-105 (`structBias = sign(wClose[1] − wEma[1])`) and `ict_weekly_bias_DRAFT.pine` L68-69/116 (`vStruct = sign(close − wEMA20)`, `gateBias = vStruct`); L111-112 states the live gate is **structBias-only (EMA), NOT EMA+market-structure**. (Optionally overridable by a real weekly `gateBias` export, `[1]`-lagged.) Harness: `revcon_0b.py` (TDD 9/9; reuses the audit-verified 0a/cascade primitives).

**Discriminator design (operator choice 2026-06-19 — "one bear/chop page first"):** the FIRST confirmatory run scores the §6 gate on **ONE genuinely OUT-OF-SAMPLE bear/chop BAR_EXPORT page** (e.g. ~2021–2023 spanning the 2022 bear), NOT the post-2024 benign window already explored. Disposition: **RESOLVED** on that regime → escalate to the FULL multi-regime panel; **FALSIFIED** → close (the 1H layer carries no stable conditional edge on either axis; bias → forward-watch belt); **INSUFFICIENT-N** → export a longer page.

**Lowered-prior note (exploratory preview, 2026-06-19):** an exploratory run on the deeper 18-mo (still benign-regime) BAR window showed the 0a bias signal is **cell-unstable** — `prem|bearish` washed out (0.60 → 0.49) while `disc|bullish` became marginally-best (~0.58, CI-lo ~0.51). The apparent 0a edge does not replicate on adjacent benign data → the prior on a stable bias edge is **lowered**, and the out-of-sample discriminator is the proper adjudicator. This preview touched the recent-trend window, so the confirmatory page MUST be the untouched bear/chop regime (firewall-clean).

---

## Partition set (the conditional test) — GENUINE CHOICE, ratify before 0b

The directional rates are evaluated WITHIN each partition bucket. Both the reversion and continuation rate are computed per bucket; the gate asks whether a decision-time-observable partition yields a clearing rate.

1. **Weekly-bias sign (PRIMARY, decision-time-observable — proposed LOCKED).** Split scored 1H bars by the sign of the weekly `structBias` (`gateBias`, close vs weekly EMA-20), joined with a **PRIOR-week (`[1]`) lag** — a 1H bar in ET-week W carries the sign of the **fully-closed week W−1**, mirroring the live gate's `gateBias[1]` / `ta.ema(close, wEmaLen)[1]` convention (harness_w.py prior-week pairing; 1M `ict_1m_execution_DRAFT.pine` L104-106). Buckets: bias=+1, bias=−1.
   - **DECISION-TIME-OBSERVABILITY GUARD (added 2026-06-19, audit LA-1):** the **current-week** join (a week's own end-of-week close labeling its earlier bars) is a **look-ahead** and is FORBIDDEN. The 0b join MUST use the `[1]`-lag; a guard analogous to `test_weekly_bias_proxy_is_decision_time_observable` (perturbing a week's closing bar must not move any same-week-or-earlier label) is required before scoring. The prior PREREG text ("joined as in PREREG-1H 1H-E3 … observable at the decision bar") is **superseded** by this lag requirement — 1H-E3's plain current-week join is not observable.
2. **Regime chop-vs-trend (ER) — DROPPED 2026-06-19 (operator-delegated best judgement; CHOICE #4 resolved).** 0a showed the Kaufman-ER partition fragments n and **starves the trend bucket** (floor n 48→21→6→2 across thr 0.20–0.50, below the 30 floor at every thr ≥ 0.30), and the (weak) flip direction contradicts the motivating prior. The axis is observability-clean but not answerable on the available 1H data, and keeping it would force a much larger chop-spanning export the TV 1H feed cannot serve (≈6.5-mo cap). Per The Algorithm (delete the fragile axis) it is dropped from 0b. **Re-proposable later** with new mechanism evidence (rejected-candidates discipline) — NOT permanently foreclosed. **Bias-sign (partition #1) is the SOLE 0b partition.**

---

## Power / n-floor (per partition)

Effective independent windows per bucket = `floor(N_scored_bucket / fwdK)`. **n-floor = 30 per bucket per zone** (inherited from PREREG-1H GENUINE CHOICE 1). A bucket below 30 → that bucket is INSUFFICIENT-N (not a decision). If the candidate partition's buckets are all starved → AMBIGUOUS-HOLD, re-spec the export window (longer / explicitly chop-spanning).

**Estimator PIN (added 2026-06-19, audit F3/F5):** the n-floor=30 gate is on the **`floor(N_scored_bucket / fwdK)`** form ONLY — NOT `stride_rate_ci`'s greedy-kept count (which can exceed the floor by up to ~4.6× on sparse/clustered buckets and would let a starved bucket spuriously clear the floor). Any 0b report must label the two distinctly (`n_floor` vs `n_ci`).

**0a power evidence (informs the export sizing):** on the 0a window the **ER-regime trend bucket is starved** (`floor` n 48 → 21 → 6 → 2 at ER 0.20/0.30/0.40/0.50; below 30 at every threshold ≥ 0.30). The 0b export must therefore be sized so each **TREND bucket** (not merely each zone) clears 30, or the regime partition pre-commits to AMBIGUOUS-HOLD.

---

## Placebo (regression-to-the-range) — frozen

Same as PREREG-1H 1H-E5: random-EQ AND sign-shuffle nulls, both reported, verdict uses the closer/higher. A clearing directional rate must EXCEED the placebo floor **within its partition bucket** (the regression-to-the-range confound is partition-local).

---

## Multiplicity — the joint family (declare BEFORE scoring)

**RATIFIED 2026-06-19 (CHOICE #3, bias-only):** with partition #2 dropped and the bias buckets sparse, the lookN×eqBand 9-cell anchor grid is **FIXED at the locked gate cell (lookN=60, eqBand=0.05)** — NOT re-swept per bucket (re-sweeping would inflate the family and the noise on sparse bias buckets). Declared family = **{zone prem, disc}** × **{bias +1, −1}** × **{reversion, continuation}** = **8 directional rates** at the fixed anchor (*corrected 2026-06-19 from the earlier "4" which omitted the zone axis; the larger N=8 is the more conservative, faithful count — the harness `penalty_8way` uses N=8*). Penalty = deflated-Sharpe (primary) / Bonferroni (fallback) max-stat over those 8, on the **`floor(N_scored/fwdK)` basis** (re-audit F1). The winning zone+bias+direction must clear 0.5 by ≥2pp AFTER the penalty. **The doubling (reversion+continuation) is the cost of asking the conditional question — it is paid in the penalty, not waved.**

**Winner-selection note (re-audit, conservative):** `penalty_8way` selects the winner by argmax-RATE among the fully-clearing candidates and tests *that* cell's stride CI lower bound against the family-wise `e_max` — faithful to the audited ancestor `harness_1h.deflated_max_stat_penalty`. A candidate with a lower rate but tighter CI can be masked, routing a real edge to AMBIGUOUS/HOLD (re-test), never to a false RESOLVED. This is a known conservative property (it can only fail to escalate, never wrongly escalate).

---

## Verdict gate (binary) — maps to parent §6 Phase-0

| Verdict | Trigger |
|---|---|
| `RESOLVED-CONDITIONAL` | a **decision-time-observable** partition bucket's directional rate (reversion OR continuation) clears 0.5 by ≥2pp under BOTH stride AND block · beats its partition-local placebo · survives the joint multiplicity penalty · effective-N ≥ 30 in that bucket |
| `FALSIFIED` | in EVERY ratified partition bucket, BOTH reversion AND continuation de-overlapped CIs straddle 0.5 after the penalty |
| `AMBIGUOUS-HOLD` | clears on 0a (exploratory) but 0b candidate bucket starved (eff-N < 30), OR clears only on a non-observable/hindsight partition | re-spec export; name re-test object |

A RESOLVED-CONDITIONAL routes to **Phase 1** (entry redesign in the confirmed direction) — NOT deploy, NOT a 1M-gate license on its own.

---

## Forbidden (during the 0b verdict window)

1. Reading Phase 0a (the 6.5-mo file) as confirmation — it is exploratory (the data already produced the reversion FALSIFIED).
2. Choosing the partition / threshold AFTER seeing 0b (best-of-K regime label) — the set is frozen here before scoring.
3. A hindsight (non-decision-time-observable) regime label as the partition.
4. Re-tuning lookN/eqBand/fwdK on the reversion claim to lift it (re-tune of a closed verdict).
5. Reporting an unconditional direction flip as the finding (near-trivial complement; the test is conditional).

---

## Audit hook

Reviewer question at verdict time: *"Was the partition set, the n-floor, the placebo, the multiplicity family, the ≥2pp margin, or the decision-time-observability requirement moved or reinterpreted after the 0b run? Was 0a (the 6.5-mo file) read as anything other than exploratory?"* Any **yes** → verdict void.

```bash
# Firewall: this file committed BEFORE the 0b export is scored:
git log --oneline -- lab/analysis/ict_revcon_2026-06-19/PREREG-0B.md
# 0a-is-exploratory clause present:
grep -niE 'EXPLORATORY' lab/analysis/ict_revcon_2026-06-19/PREREG-0B.md
```

---

## GENUINE PRE-REGISTRATION CHOICES — RATIFIED 2026-06-19 (operator-delegated "best judgement")

All four resolved BEFORE any 0b data is scored (firewall intact), grounded in the audit-verified [`PHASE-0A-FINDINGS.md`](PHASE-0A-FINDINGS.md): the **bias-sign axis** is robust (premium→down under bearish prior-week bias ≈ 0.60, survived the LA-1 observability fix); the **ER-regime axis** is fragile (starves the trend bucket, weakly contradicts the motivating direction, and a chop-spanning 1H export exceeds TV's ≈6.5-mo 1H cap).

| # | Choice | RATIFIED | Basis |
|---|---|---|---|
| 4 | Whether to include partition #2 (ER regime) | **NO — bias-sign is the SOLE 0b partition** | 0a: regime axis starves + contradicts the prior; keeping it needs data TV cannot serve |
| 1 | Regime proxy / threshold | **MOOT** (partition #2 dropped) | — |
| 2 | n-floor per bias bucket per zone | **30** on `floor(N_scored/fwdK)` | inherited; bias buckets ≈ 38/35 on the 0a window, comfortable on a longer window |
| 3 | Multiplicity family scope | **Anchor FIXED at gate cell (60/0.05); family = {prem,disc}×{bias±1}×{rev,cont} = 8 directional rates** (corrected from "4"); penalty on the floor-n basis | sparse buckets — re-sweeping the 9-cell grid per bucket inflates family + noise |

**Binding 0b feasibility note (operator):** the 1H confirmatory needs a genuinely multi-regime window, but the cascade established **TV's 1H chart export caps at ≈6.5 months (single benign regime)**. If the longest obtainable 1H US500 window is still single-regime, the bias signal is **data-blocked for a confirmatory verdict** → it routes to a **forward-watch belt finding** (like the cascade's disc→up near-miss), NOT a re-tune and NOT a lock. Confirm the available 1H history span before scoring 0b.

## Amendment log (append-only)
- 2026-06-19 — DRAFTED (PROPOSED). To be ratified + committed next session before the 0b export is scored.
- 2026-06-19 — **Pre-data refinements from the Phase-0a run + 21-agent adversarial audit** (firewall NOT yet lifted; no 0b data scored). (a) Partition #1 join pinned to the **`[1]`-prior-week lag** + an observability-guard requirement (audit LA-1: the current-week join is a look-ahead; the prior "observable at the decision bar" text is superseded). (b) n-floor **estimator pinned** to `floor(N_scored/fwdK)` with a `n_floor`/`n_ci` labeling requirement (audit F3/F5). (c) 0a power evidence added (trend bucket starves) + per-BUCKET export sizing. (d) GENUINE CHOICES annotated with 0a evidence (bias axis favored; regime axis fragile). All from EXPLORATORY 0a + audit, which by construction cannot confirm the hypothesis — the 0b verdict remains firewalled.
- 2026-06-19 — **Data pathway = BAR_EXPORT + discriminator design ADDED** (pre-data; firewall intact). Resolves the multi-regime data-feasibility gate: 1H OHLC from BAR_EXPORT v0.1 pages (parity byte-identical to the chart feed, 2922/2922), offline zone (100% vs Pine), offline structBias (Pine-confirmed EMA-only gate definition). Operator chose the **one-bear-page discriminator** (score the §6 gate on a single out-of-sample bear/chop page; escalate-or-close). Harness `revcon_0b.py` (TDD 9/9). Exploratory preview lowered the prior (bias signal cell-unstable on the 18-mo benign extension). Confirmatory page must be OUT-OF-SAMPLE (untouched bear/chop). Firewall: commit this file before scoring any bear page.
- 2026-06-19 — **GENUINE CHOICES RATIFIED (operator-delegated "best judgement").** CHOICE #4 = **NO** (ER-regime partition #2 DROPPED; bias-sign is the sole 0b partition); #1 moot; #2 = n-floor 30 per bias bucket per zone on `floor(N/fwdK)`; #3 = anchor FIXED at the gate cell (60/0.05), family = {rev,cont}×{bias±1} = 4. Rationale: 0a found the bias axis robust and the regime axis fragile + data-infeasible at 1H. Firewall still intact (no 0b data scored); commit this file before any 0b run. Binding open gate: operator confirms a multi-regime 1H export is obtainable (TV 1H ≈6.5-mo cap) — else the bias signal is a forward-watch belt finding, not a confirmatory verdict.
- 2026-06-19 — **0b harness `revcon_0b.py` adversarially audited (M-15 discipline) BEFORE any scoring; 3 verdict-corrupting defects found + TDD-fixed in the NEW penalty/gate logic.** **F1** (CRITICAL-class): `penalty_8way` fed the inflated stride greedy-kept count into the deflated-max-stat variance instead of `floor(N_scored/fwdK)` — the false-positive (spurious-RESOLVED) direction the §Estimator-PIN forbids; fixed to the floor-n basis, matching the audited `harness_1h.deflated_max_stat_penalty`. **F2** (MAJOR): the penalty winner was the global argmax-rate incl. block-failing cells → a spurious high-rate non-candidate could demote a genuine RESOLVED to AMBIGUOUS; fixed — the winner is restricted to fully-clearing candidates (`eligible`), e_max still over the full 8-cell family. **F4** (MINOR): a stride-clears/block-fails near-miss fell to FALSIFIED; fixed — FALSIFIED fires ONLY when no cell clears the stride CI in any direction (matches `harness_1h.verdict_1h`'s disposition + the PREREG "both straddle" definition); near-misses → AMBIGUOUS. +5 regression guards (the original tests had the M-15 self-referential masking — `n_eff==n_floor` fixtures, coinflip-only FALSIFIED). Weekly-`gateBias` override hardened (sort+dedup before the `[1]`-lag) + tested. **15/15 0b tests, 211 total green.** (3 of the first audit's 7 agents died on connection errors; a re-audit of the fix is verifying no new defect + covering the lost placebo/loader surface.)
- 2026-06-19 — **Re-audit of the fix CLEAN on the F1/F2/F4 fixes** (3/3 lenses: correct + faithful to the ancestor, no false-RESOLVED path, M-15 prior absent). Surfaced + fixed **one more verdict-corrupting mis-route (F4-1, safe "false-FALSIFIED" direction):** `any_stride_clear` was evaluated only over POWERED cells, so a starved-but-stride-clearing cell (all powered cells dead) wrongly FALSIFIED instead of the AMBIGUOUS-HOLD this PREREG mandates for a starved bucket → fixed (any_stride_clear over ALL cells; starved clearer → AMBIGUOUS). Plus two non-corrupting improvements: **P-1** the placebo was a base-rate-deflated near-no-op (inherited) → replaced with a proper **bucket forward-direction drift floor** (`bucket_fwd_floor`; a zone's bias-conditioned rate must beat the bucket's own directional drift, e.g. beat the bull-bucket up-rate — a real regression-to-range gate, and O(n) so the suite dropped 16min→6s); **L-1/L-2** `load_bar_pages` now carries the entry-price==encoded-close **format-drift cross-check** + skips epoch-less legacy rows. **Family count reconciled 4 → 8** (the genuine multiplicity is {prem,disc}×{bias±1}×{rev,cont}=8 directional rates; the harness already used N=8 — the larger, more conservative, faithful count). argmax-rate winner documented as a known conservative property (never false-RESOLVED). **+3 regression guards; 18/18 0b, 215 total green.** Firewall still intact — commit before scoring any bear page.
