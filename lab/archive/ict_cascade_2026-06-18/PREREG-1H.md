# Q-ICT-CASCADE-1 / Layer 1H (Premium/Discount) — VERDICT PRE-REGISTRATION

**Registered before the 1H export is scored offline. No criterion below may be moved after the first real-population (de-overlapped) run. The commit of this file is the lock that lifts the firewall for the 1H layer.**

Parent campaign: [`TEST_PLAN.md`](TEST_PLAN.md) (§4 H-1H + H-CASCADE, §5 forbidden, §6 1H row, §7.B 1H, Appendix A 1H-E1..E6)
Sibling format reference: [`docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md`](lab/archive/../../docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md)
Authored: 2026-06-18 · **Lock date: RATIFIED 2026-06-18** (operator delegated the genuine-choice calls to Claude with a "most faithful to the design" criterion; all eight LOCKED at their proposed values incl. the halves superset — see amendment log) · Lock commit: this file's introducing commit (resolve via `git log --oneline -- <this file>`; firewall lifts only from that commit onward)

> **Status: PROPOSED.** Every value flagged in the "Genuine pre-registration choices" section is a real choice, not mechanically forced by §6, and is PROPOSED until the operator commits this file. The frozen-config and gate tables below are then frozen by that commit.

---

## §0 — Rule 0 citation block (production-source verification, CITATION-CHAIN mode)

The 1H draft Pine and its transfer counterparts are **gitignored** (`.gitignore:75` -> `**/*.pine`) AND live outside the repo in `C:\Users\joshu\Downloads\`. A future reader cannot diff the gitignored bytes, so this is a CITATION-CHAIN anchor: file + `LastWriteTimeUtc` + line ranges. Read verbatim (full contents, line-numbered) this session. **A resuming session MUST re-anchor** (Downloads is mutable; line numbers drift if edited).

| Source file (Downloads) | Bytes | LastWriteUTC anchor | Role here |
|---|---|---|---|
| `ict_1h_premium_discount_DRAFT.pine` | 7556 | 2026-06-18T17:53:06Z | the 1H layer under test (B2-1H gate-basis draft) |
| `ict_1m_execution.pine` | 18163 | 2026-06-18T15:56:17Z | live gate the transfer must license (lines 62, 91-92, 94-95, 100, 106-107) |
| `constellation_ict_lib.pine` | 10260 | 2026-06-18T15:56:24Z | `pd()` shared primitive (lines 195-202) |

**WARNING — timestamp display trap (the repo EDT-display trap, see memory `reference_platform_display_tz_edt`):** the Bash `ls -la` view renders these as `11:56` / `13:53` (local ET, UTC-4). The authoritative `LastWriteTimeUtc` above is from PowerShell `Get-ChildItem | Select LastWriteTimeUtc`. The DRAFT (`17:53:06Z`, 7556 B) is the B2-1H build and is **newer** than the original `ict_1h_premium_discount.pine` (`15:56:22Z`, 5911 B) that TEST_PLAN §0 anchors; this PREREG tests the DRAFT.

**Line ranges the frozen-config values come from (DRAFT unless noted):**
- anchor rule default `lookback-extremes` (gate-relevant) + `swing-pair` exploration-only: lines 22-25.
- `pvLen=5` (swing-pair only, INERT for the gate path): line 26.
- `lookN=60` (must equal 1M `pdLookN`): line 27. **1M `pdLookN=60`** at `ict_1m_execution.pine:62`.
- `eqBand=0.05`: line 29. **1M `eqBand=0.05`** at `ict_1m_execution.pine:63`.
- `fwdK=12` (MEASUREMENT window, not a trade knob): line 31.
- native [0]-fresh zone basis: lines 44-57 (`ta.highest/lowest(high/low, lookN)` against 1H `close`).
- GATE-basis `zoneGate` on the [1]-lagged lookback-extremes range: lines 65-66 (`ta.highest(high,lookN)[1]` / `ta.lowest(low,lookN)[1]`), scored via `ict.pd(...)` line 70; on-chart `zone agree%` lines 72-78.
- overlapping follow-through scoring (smoke test only): lines 80-103.
- export columns `zone, eq, premHit, discHit, zoneGate, zoneAgree`: lines 143-149.
- 1M gate basis (the price-BASIS axis): `ict_1m_execution.pine:94-95` reads the [1]-lagged hourly range via `request.security(..., "60", ...)` against the **1-MIN `close`** at line 100; gate polarity `longPDok = zone==-1` / `shortPDok = zone==1` lines 106-107; entries require `structBias` (line 91-92) AND PD (never PD alone). Lib `pd()` returns `[zone,eq]`, +1=premium/sell, -1=discount/buy, 0=eq (`constellation_ict_lib.pine:195-202`).

---

## Test object — frozen configuration (zero touches permitted during the verdict window)

| Parameter | Value | Status | Source (DRAFT line) |
|---|---|---|---|
| Layer anchor rule (gate-relevant) | `lookback-extremes` | LOCKED (matches 1M gate basis) | 22 |
| `swing-pair` anchor | present | REPORT-ONLY (exploration; NOT in lock budget) | 23-25, 45/48 |
| `lookN` (extremes lookback) | 60 | LOCKED — must equal 1M `pdLookN=60` | 27; 1M:62 |
| `eqBand` (EQ stand-down half-width) | 0.05 | LOCKED (matches 1M `eqBand=0.05`) | 29; 1M:63 |
| `fwdK` (follow-through window K) | 12 | LOCKED — measurement horizon, NOT a trade knob | 31 |
| `pvLen` (swing strength) | 5 | INERT for gate path (swing-pair only; exploration-only per §8 PREREG-pvLen) | 26 |
| zone polarity | +1 premium->expect down; -1 discount->expect up; 0 EQ stand-down | LOCKED (lib `pd`) | 195-196; lib:199-202 |
| gate-basis range | `[1]`-lagged lookback-extremes (`zoneGate`) | LOCKED (range-LAG axis of transfer) | 65-66 |
| price-basis of live gate | 1-MIN `close` vs this script's 1H `close` | LOCKED — OFFLINE-only (price-BASIS axis) | 1M:94-95,100 |
| follow-through hit defn | premHit = (zone[fwdK]==1 AND close < close[fwdK]); discHit = (zone[fwdK]==-1 AND close > close[fwdK]) | LOCKED | 81-86 |
| feed | canonical TV/Pepperstone SPX-class (US500), native 1H | LOCKED (tv-csv-canonical-feed-policy) | n/a |
| live on-chart premRate/discRate table | overlapping/autocorrelated | NOT the verdict (smoke test only) | 15-16, 102-103, 126-131 |

**Verdict instrument = the de-overlapped OFFLINE estimate** on the exported `zone/eq/premHit/discHit/zoneGate/zoneAgree` columns. The on-chart `prem->down`/`disc->up` table cells (lines 126-131) are autocorrelated by the script's own admission (lines 15-16) and are forbidden as the verdict (§ Forbidden #1).

---

## Resampling unit — de-overlap (frozen)

Every bar contributes a scored window, so consecutive `premHit`/`discHit` rows share up to `fwdK-1=11` bars of forward path and are **pseudo-replicates**. Two de-overlap estimators, BOTH required for a RESOLVED:

1. **Stride-by-`fwdK`=12 (primary).** One scored row every 12 bars (per zone) so forward windows do not overlap. Effective independent windows per zone = `floor(N_scored_zone / fwdK)`.
2. **Moving-block bootstrap (cross-check).** Block length = `fwdK`=12 bars; resample blocks, recompute the rate; CI is the block-bootstrap percentile interval. (Block resampling, not iid `binomial` — the iid CI understates SE and is NOT the verdict instrument, mirroring 1H-E2.)

The point estimate of each rate (premRate, discRate) may be read on all scored rows; the **CI and the placebo comparison resample by the de-overlap unit above** (stride for primary, block for cross-check). Effective-N, not `N_scored`, governs the power floor below.

---

## Power disclosure (read before judging the verdict)

The unit is a binary hit per scored window, so the dispersion is a **rate variance** `p(1-p)` (max 0.25 at p=0.5), not a per-trade sigma in R — there are no R outcomes at this layer (the 1H layer measures directional follow-through, not P&L). For a rate near 0.55, the per-window SE on `n` **independent** windows is `sqrt(0.25/n)`: at n=30 that is +/-0.091 (so a 2pp clearance of 0.5 is well inside one SE), at n=60 +/-0.065, at n=100 +/-0.050. Overlap inflates this: the effective-N after stride-by-12 de-overlap is roughly `N_scored/12` per zone, so a 1H export covering ~3000 confirmed bars in premium yields ~250 raw scored rows -> only ~21 independent premium windows. **Decision rules below are expectation/CI-based, not significance tests** — a "CI clears 0.5 by >= 2pp" is a credibility upgrade routed to path-independent confirmation, NOT a p<0.05 claim and NOT a deploy.

**n-floor (PROPOSED choice):** effective independent windows = `floor(N_scored / fwdK)`. Pre-registered floor = **30 independent windows per zone** (premium and discount each). Below 30 in a zone, that zone's verdict is **INSUFFICIENT-N**, not a decision — a starved zone returns ambiguity indistinguishable from a null, and reading a wide CI that "straddles 0.5" on n<30 as FALSIFIED would be a power artifact. If BOTH zones fall below 30 after stride de-overlap, the layer verdict is INSUFFICIENT-N (re-spec the export window — longer/multi-regime — before any 1H verdict).

---

## Transfer pre-gate (E1 / H-CASCADE — the load-bearing cascade claim)

A 1H PASS licenses the 1M PD gate ONLY if the transfer pre-gate clears. Two axes, both pre-registered:

- **(a) range-LAG axis — ON-CHART, measurable on the 1H export.** Native [0]-fresh zone (`zone`) vs [1]-lagged `zoneGate` (DRAFT lines 65-72). Metric = sign-agreement `zoneAgree` rate (`agreeRate`, line 78) over confirmed bars, plus the rate gap |premRate/discRate(native) - rate(zoneGate basis)|.
- **(b) price-BASIS axis — OFFLINE-only, against the paired 1M export.** 1-min `close` vs 1H `close` against the same [1]-lagged hourly range (1M lines 94-95,100). Requires the paired 1M PD-zone export; not computable from the 1H export alone.

**Thresholds (frozen):** sign-agreement **>= 90%** AND rate gap **<= 3pp**, on BOTH axes.
**REJECT the transfer** (and the offline-layer economy) if agreement **< 90%** OR gap **> 3pp** on EITHER axis. On REJECT, a 1H unconditional PASS licenses NOTHING about the 1M gate; the only valid evidence becomes the full 1M end-to-end run.
**Pre-condition:** `lookN` here MUST equal 1M `pdLookN=60` and `eqBand` MUST equal 1M `eqBand=0.05`, or `agree%`/gap is meaningless (both hold at default — frozen-config table).

---

## Placebo (1H-E5 — regression-to-the-range) — frozen

A [0]-fresh range extreme mean-reverts mechanically, so a naive premHit/discHit rate is inflated by regression-to-the-range, not by ICT information. The real rate must **beat** a null built one of two pre-registered ways (BOTH reported; the verdict uses the stronger/closer one):
- **random-EQ null:** shuffle the EQ split point within the dealing range (random premium/discount label assignment at matched base frequency), recompute the rate.
- **sign-shuffle null:** block-permute the `zone` sign labels against the realized forward returns (block = `fwdK`).
The real de-overlapped rate must exceed the placebo's de-overlapped rate (the placebo is the floor the regression-to-the-range mechanism alone produces). If the real rate does not beat the placebo, the >0.5 reading is the mean-reversion confound (1H-E5 null still alive).

---

## Anchor sweep + multiplicity penalty (1H-E4) — frozen grid

Gate-relevant selection surface (the `swing-pair` anchor is REPORT-ONLY and is NOT in the lock budget):
- anchor = `lookback-extremes` (1 gate-relevant level)
- `lookN` in {40, 60, 80} (PROPOSED grid)
- `eqBand` in {0, 0.05, 0.10} (PROPOSED grid)
- => **9 gate-relevant cells** (1 x 3 x 3). Declared BEFORE the first run.

Penalty = deflated-Sharpe / Bonferroni over the 9 cells (a max-statistic correction, not per-cell naive CI). The winning cell must clear 0.5 (by the >= 2pp margin, both estimators) **after the penalty**. Each cell reports n-per-cell, because `eqBand` is an n-throttle (`eqBand=0` scores every bar, worsening overlap and fattening n — 1H-E6); an n-driven "win" must be visible. The grid is booked into the campaign §8.5 DSR/PBO ledger; the 9-cell cardinality is part of the joint family-wise budget over the UNION of selection surfaces (lock ORDER mitigates dependence, not FWER).

---

## Bias-conditioned variant (1H-E3) — frozen (gate-relevant conditional)

The 1M only trades `structBias` AND PD (never PD alone; 1M lines 91-92, 106-107). The unconditional 1H rate measures reversion to the range; the 1M needs trend-continuation under the bias. So **also report each rate split by the sign of the weekly `structBias`** (premHit | bias=+1 vs bias=-1; discHit likewise). This bias-conditioned rate is the gate-relevant conditional and drives the AMBIGUOUS-HOLD trigger below. (Requires the weekly `structBias` series joined to the 1H export by timestamp.)

---

## Verdict gate (binary) — maps to TEST_PLAN §6, 1H row

| Verdict | Trigger (all conditions ANDed for RESOLVED; ANY for FALSIFIED) |
|---|---|
| `RESOLVED` (-> path-independent confirmation, NOT deploy) | a rate's de-overlapped CI clears 0.5 by **>= 2pp** under **BOTH** stride AND block-bootstrap estimators · AND the real rate **beats** the placebo (1H-E5) · AND the winning anchor cell clears 0.5 by >= 2pp **after** the 9-cell multiplicity penalty (1H-E4) · AND the **transfer pre-gate clears** (agreement >= 90% AND gap <= 3pp on both the range-LAG and price-BASIS axes) · AND effective-N >= 30 in the scored zone |
| `FALSIFIED` | **both** premium-down AND discount-up de-overlapped rate CIs **straddle 0.5** across anchors after the multiplicity penalty (the split is decorative) |
| `AMBIGUOUS-HOLD` | clears the unconditional gate but **fails the bias-conditioned variant** (1H-E3) — i.e. unconditional rate clears but the `structBias`-conditioned rate (the gate-relevant conditional) does not -> HOLD, name the re-test object/window, no downstream 1M PD-gate licensing |
| `INSUFFICIENT-N` | effective-N < 30 per zone after stride de-overlap (both zones) -> not a decision; re-spec the export window (longer / multi-regime), re-run |

**Cascade-licensing rule (do not skip):** even a RESOLVED 1H verdict does NOT license the 1M PD gate unless the transfer pre-gate clears. A 1H PASS measured on the [0]-fresh / 1H-close basis while `zoneGate`/1-min agreement is < 90% or gap > 3pp licenses NOTHING (this is the cascade's load-bearing failure, 1H-E1). On transfer REJECT, route the claim to the full 1M end-to-end run.

**§6-superset note (flagged, operator-ratifiable — consistency with W/D).** TEST_PLAN §6's 1H row, unlike the W row, does NOT make halves/thirds stationarity an explicit RESOLVED trigger. To keep the three rate layers (W, D, 1H) consistent under the identical single-export single-regime power caveat, this PREREG adds — as a flagged superset, NOT a silent widening — a **halves-stationarity disjunct to AMBIGUOUS-HOLD**: even if the unconditional + bias-conditioned gates clear, a rate that clears overall **but flips sign of its >0.5 margin across the two chronological halves** (one half ≤ 0.5) routes to AMBIGUOUS-HOLD (one-regime), not RESOLVED. This is strengthening (harder to PASS) and mirrors the §6 W row + the PREREG-D one-regime disjunct. Operator may decline this superset at ratification (reverting 1H to the literal §6 1H row); it is listed in GENUINE CHOICES as item 8.

**Path-independence on confirmation/unpark:** a RESOLVED 1H routes to a confirmation that is independent on **price path / period / instrument** — NOT merely a different feed of the same path (a re-export of the same SPX 1H bars from another vendor is the same path and confirms nothing about regime robustness). The single export is one regime; cross-regime stationarity (halves/thirds) is part of RESOLVED stationarity expectations and the confirmation must vary the period or the instrument.

---

## Forbidden (during the verdict window) — drawn from §5, only the moves that bite the 1H layer

1. **Reading the on-chart premRate/discRate table as the verdict.** Lines 102-103/126-131 are overlapping/autocorrelated by the script's own admission (lines 15-16). The verdict is the de-overlapped offline estimate only. Citing the table number is the autocorrelation trap (1H-E2).
2. **Reporting overlapping windows as iid (1H-E2).** Computing a CI vs 0.5 with a binomial/iid SE on the raw scored rows. Every CI uses the stride or block de-overlap unit above.
3. **Free anchor x lookN x eqBand with a "maximize" claim and no penalty (1H-E4).** Picking the best-of-9 cell and reporting its raw >0.5 rate. The winner must clear 0.5 AFTER the declared 9-cell penalty, with n-per-cell shown.
4. **Crediting a 1H PASS to the 1M gate before the transfer pre-gate clears.** A PASS on the [0]-fresh/1H-close basis does not license the [1]-lagged/1-min-close gate until agreement >= 90% AND gap <= 3pp (H-CASCADE).
5. **Outcome-conditional `eqBand` tuning.** Choosing `eqBand` to fatten n and then reading the rate on that n (`eqBand` is both a measurement knob and an n-throttle, 1H-E6). The grid is frozen above; n-per-cell is reported.
6. **Promoting the `swing-pair` anchor into the lock budget.** It is REPORT-ONLY exploration (lines 22-25); validating it does not validate the live gate (which uses lookback-extremes). Do not count its rate toward RESOLVED or spend a best-of-K cell on it.
7. **Silently re-defining the EQ/anchor convention mid-window.** anchor rule, `eqBand`, `lookN` are definitional/locked; changing one after data arrives is the Iran/Hormuz silent-relabel shape (§5). Flag, ratify, re-run — never patch in place.

---

## Audit hook

Reviewer question at verdict time: *"Was any criterion above — the n-floor, the de-overlap unit, the 9-cell grid + penalty, the placebo design, the 90%/3pp transfer thresholds, or the bias-conditioned variant — moved, reinterpreted, or supplemented after the de-overlapped run?"* Any **yes** -> the verdict is void and the 1H pattern stays unresolved.

Runnable checks:
```bash
# §0 re-anchor (Downloads is mutable, outside the repo, gitignored):
#   PowerShell:
#   Get-ChildItem 'C:\Users\joshu\Downloads\ict_1h_premium_discount_DRAFT.pine' |
#     Select Name,LastWriteTimeUtc,Length
#   Expect 7556 bytes / 2026-06-18T17:53:06Z. If LastWriteUTC differs -> RE-READ before trusting any line citation.
#   (Bash `ls` shows ET/local time — use PowerShell LastWriteTimeUtc as authoritative.)

# Transfer pre-condition: lookN(1H) == pdLookN(1M) and eqBand(1H) == eqBand(1M), else agree% is meaningless:
grep -nE 'lookN|pdLookN|eqBand' 'C:\Users\joshu\Downloads\ict_1h_premium_discount_DRAFT.pine' \
  'C:\Users\joshu\Downloads\ict_1m_execution.pine'
#   Expect 1H lookN default 60 / eqBand 0.05 ; 1M pdLookN 60 / eqBand 0.05.

# gitignore that drove CITATION-CHAIN mode:
grep -n '\*\*/\*\.pine' .gitignore   # expect line 75
```
This file's introducing-commit hash/date anchors the registration; evaluation appends below, never edits above.

---

## GENUINE PRE-REGISTRATION CHOICES (operator ratification required before run 1)

These are real choices — NOT mechanically forced by §6 — and are **PROPOSED** until the operator commits this file. Sign off each before the first de-overlapped run.

| # | Choice | PROPOSED value | Why it is a genuine choice (not forced) | Rationale |
|---|---|---|---|---|
| 1 | n-floor (effective independent windows per zone) | **30** | §6 says "INSUFFICIENT-N if starved" but names no number; 30 is a power call, not a §6 derivation | At n=30 the per-window SE is +/-0.091 near p=0.5, so a 2pp clearance is ~0.22 SE — 30 is the minimum at which the CI test is interpretable rather than a power artifact; below it, ambiguity is indistinguishable from a null |
| 2 | `lookN` sweep grid | **{40, 60, 80}** | §6/E4 mandate "a penalty over a declared grid" but not the grid points; 60 is forced (gate-match), the +/-20 neighbors are a choice | Symmetric one-step neighbors around the gate-matched 60 probe plateau-vs-knife-edge without inflating the cell count; wider/finer grids change the multiplicity penalty |
| 3 | `eqBand` sweep grid | **{0, 0.05, 0.10}** | same — grid points are a choice; 0.05 is forced (gate-match) | 0 (n-throttle extreme, scores every bar) and 0.10 (double the lock) bracket the locked 0.05; reporting n-per-cell exposes the 1H-E6 n-throttle effect across the bracket |
| 4 | grid cardinality / penalty family | **9 cells; deflated-Sharpe or Bonferroni (max-stat)** | follows from choices 2+3; the penalty FAMILY (DSR vs Bonferroni) is a methodology choice | DSR is the campaign's standing instrument; Bonferroni is the conservative fallback if the rate's null distribution is ill-behaved at small effective-N. Operator picks one before run 1 |
| 5 | placebo design (1H-E5) | **random-EQ AND sign-shuffle, both reported; verdict uses the closer (higher) null** | §6/E5 require "beats the placebo" but not which null | Two independent constructions of the regression-to-the-range floor; using the higher one is the conservative test (real rate must beat the stronger placebo) |
| 6 | block length for the bootstrap cross-check | **fwdK = 12 bars** | the de-overlap stride (12) is forced by `fwdK`; reusing it as the bootstrap block is a (defensible) choice, not the only option | Matching block length to the overlap horizon is the standard de-overlap correction; a longer block would be more conservative but starves effective-N faster |
| 7 | bias-conditioned join source | **weekly `structBias` series joined by timestamp to the 1H export** | §6 AMBIGUOUS-HOLD requires the bias-conditioned variant but not the join mechanic | The 1M gate's bias is the weekly `structBias` (1M:91-92); the 1H export must be joined to the SAME weekly bias series, not a 1H-local proxy, or the conditional is not gate-relevant |
| 8 | halves-stationarity superset (the §6-superset note above) | **ADD a one-regime halves disjunct to AMBIGUOUS-HOLD** | §6's 1H row omits halves/thirds (the W row includes it); adding it is a strengthening choice, not a §6 derivation | Keeps W/D/1H consistent under the identical single-export power caveat; operator may decline to revert 1H to the literal §6 1H row |

Items frozen/forced (NOT operator choices, recorded for completeness): anchor=lookback-extremes (forced — gate basis), `lookN=60` / `eqBand=0.05` defaults (forced — must equal 1M to keep transfer meaningful), `fwdK=12` (measurement horizon, frozen), zone polarity (lib `pd`), the 90%/3pp transfer thresholds and the >=2pp margin (set by §4 H-CASCADE / §6, not re-openable here), `pvLen=5` (inert — swing-pair only, per §8 PREREG-pvLen exploration-only), the two-axis transfer structure (E1).

---

## Amendment log (append-only)

- **2026-06-18 — RATIFIED (operator-delegated; criterion: most faithful to the design).** All genuine choices **LOCKED at their proposed values**: (1) n-floor = 30 effective windows/zone; (2) `lookN` grid {40,60,80}; (3) `eqBand` grid {0,0.05,0.10}; (4) 9-cell penalty — **deflated-Sharpe (DSR) as PRIMARY** (the campaign's standing instrument), Bonferroni as the conservative fallback only if the rate null is ill-behaved at small effective-N; (5) placebo = random-EQ AND sign-shuffle, verdict uses the closer/higher null; (6) bootstrap block = `fwdK`=12; (7) bias-conditioned join = weekly `structBias` by timestamp; (8) **halves-stationarity superset ACCEPTED** (the one-regime AMBIGUOUS disjunct, for W/D/1H consistency). 60 / 0.05 / fwdK=12 / lookback-extremes remain forced (gate-match), not choices. **No value changed.** Pre-data: no criterion may move after run 1. Firewall lifts on this file's commit.
- **2026-06-18b -- PRICE-BASIS AXIS EQ-HANDLING: ALIGN ratified (operator-delegated; pre-data, firewall-safe).** The Transfer pre-gate's two axes feed the same 90%/3pp threshold but had inconsistent EQ-handling: the range-LAG axis is EQ-inclusive (pinned to Pine `agreeRate`, per FINDING 1H-CRITICAL), while the price-BASIS axis dropped EQ rows (`restrict_nonzero=True`). The PREREG was **silent** on the price-BASIS axis's EQ handling (it has no Pine `agreeRate` counterpart to pin it), so this is a genuine-choice ratification, not a faithfulness fix. **Ratified: ALIGN** -- the price-BASIS agreement is now **EQ-inclusive raw equality over valid & gateValid joined bars**, consistent with the range-LAG axis and the gate's own 1H-E1 conservative-transfer purpose. Rationale: dropping EQ-vs-nonzero rows (1H directional, the 1M-basis the live gate reads in EQ stand-down) hid GENUINE transfer failures and inflated agreement toward a false 1M-gate license -- the same shape as 1H-CRITICAL, minus the Pine anchor; the valid mask excludes warmup `0==0` rows so EQ-inclusion does not inflate the other way. **No threshold changed** (90%/3pp untouched). Implementation: `harness_1h.py` `transfer_price_basis_axis` (`restrict_nonzero=False`, valid-masked join via `_join_hour_to_minute`) + regression `test_transfer_price_basis_eq_inclusive_counts_disagreements`; recommendation memo `FOLLOWUP-1H-price-basis-axis.md`. Pre-data: no real 1H/1M export has been run, so the audit-hook "moved after run 1" stricture is not engaged.
- **2026-06-19 -- RUN 1 (as first scored) DECLARED VOID (instrument defect); FAITHFULNESS FIX `M-ICT-1H-OFFSET`; corrected verdict = FALSIFIED.** The first real-export scoring (US500 1H `PEPPERSTONE_US500, 60_a6b6b.csv`, 3039 bars, 2025-12-11..2026-06-18 UTC) surfaced a CRITICAL scoring defect in `recompute_hits`: it transcribed Pine's HISTORICAL offset `series[fwdK]` (= fwdK bars BACK; Pine DRAFT L81-86) as a FORWARD array index `series[i+fwdK]`, so it conditioned each hit on the FUTURE zone and reversed the price comparison -- scoring "price ROSE into a premium zone" (the COMPLEMENT of premium->down). Empirical: a backward reconstruction of Pine's formula matched the EXPORTED `premHit/discHit` columns 100%; `recompute_hits` matched only ~36%, and its rates were the complement of Pine's (1-0.5226=0.4774 vs 0.4725; 1-0.4525=0.5475 vs 0.5430). The look-ahead audit fired `ok=False` (~49% mismatch) but the harness mis-handled it -- discarding the CORRECT exported columns in favor of the buggy recompute and routing the inverted scoring into the verdict. **The first scoring is therefore declared VOID (it did not measure `premHit/discHit` per this PREREG's §0/L52 definition); it is NOT a verdict.** **FIX (faithfulness, direction-agnostic, NO criterion moved):** `recompute_hits` re-expressed at the DECISION bar (`prem[i]=zone[i]==+1 AND close[i+fwd_k]<close[i]`, the identical premium->down EVENT as Pine, consistent with `_zone_hit_vectors`/`bias_conditioned`/`placebo_random_eq` which select on `zone[i]`); `audit_exported_hits` now validates the exported columns against Pine's RESOLUTION-bar form (`_pine_resolution_hits`) so a faithful export reads `ok=True`; `placebo_sign_shuffle` direction labels corrected; the three `test_recompute_hits_*` + the two audit tests re-pinned to the correct polarity; new regression guard `test_recompute_hits_scores_event_not_complement` fails loudly if the inversion returns; `make_hour_export` fixtures now emit the resolution-bar columns. 42/42 1H tests, 178/178 campaign tests, `check_boundaries` OK. **No §-criterion (n-floor, de-overlap unit, 9-cell grid + penalty, placebo design, 90%/3pp transfer thresholds, bias-conditioned join, halves superset) was moved, reinterpreted, or supplemented** -- only the hit-scoring was corrected to match the frozen L52 definition, and it is direction-agnostic (the VOID buggy run and the corrected run BOTH return FALSIFIED). **CORRECTED VERDICT = FALSIFIED:** audit `ok=True` (0.0000 mismatch); effective-N prem=151 / disc=92 (both >= 30 -> a powered decision, not INSUFFICIENT-N); prem->down stride 0.5085 / block 0.4725 (both straddle 0.5; placebo floor 0.4656; penalty winner lookN=80/eqBand=0.05 rate 0.5085 < e_max 0.5623, pass_dsr False); disc->up stride 0.5641 / block 0.5430 (both straddle; placebo floor 0.5340; penalty winner lookN=60/eqBand=0 rate 0.5798 < e_max 0.5812 by 0.0014, pass_dsr False) -> **both premium-down AND discount-up de-overlapped CIs straddle 0.5 after the 9-cell penalty (the split is decorative)**. The range-LAG transfer axis cleared (agree 0.994 / gap 0.000) and the price-BASIS axis is moot (no PASS to license; the 1M export was correctly not required). **Regime caveat:** this is ONE benign uptrend regime (the longest 1H history TV serves for US500); per the path-independence note, a FALSIFIED stands as a negative on the available data but **re-proposal requires multi-regime / longer 1H data, NOT re-tuning the frozen knobs**. The **discount->up near-miss** (0.54-0.58, fails the penalty by 0.0014) is recorded as a forward-watch belt finding, not an action. **Blast radius (4-agent adversarial audit + follow-up):** the defect is isolated to `harness_1h.recompute_hits`; the recorded W (RESOLVED) and D (SSL-RESOLVED/BSL-FALSIFIED) verdicts and the pending 1M are UNAFFECTED (W reads Pine-precomputed `gateHit`/`gateScored`; D reconstructs draws with genuine forward scans from the correct origin; 1M consumes TV's already-paired List-of-Trades -- none re-port a Pine `series[fwdK]` offset offline). Closure record: `CLOSURE-1H-FALSIFIED.md`; lesson `M-ICT-1H-OFFSET` (registry M-15) in `docs/methodology/lessons/methodology_lessons.md`.
