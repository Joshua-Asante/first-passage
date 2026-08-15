# Q-ICT-CASCADE-1 / Layer D (Daily Draw-on-Liquidity) — VERDICT PRE-REGISTRATION

**Registered before the offline Daily reconstruction is run on real OHLC. No criterion below may be moved after the first real-population run. The commit of this file is the lock that lifts the firewall for Layer D.**

Parent campaign: [`TEST_PLAN.md`](TEST_PLAN.md) (§4 H-D, §6 D row, §7.A B3 / §7.B D, §8 `PREREG-D.md` stub, Appendix A D-1/D-2/D-2b/D-3/D-4/LIB-2)
Sibling format anchor: [`docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md`](lab/archive/../../docs/ltm/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md)
Authored: 2026-06-18 · **Status: RATIFIED 2026-06-18** (operator delegated the genuine-choice calls to Claude with a "most faithful to the design" criterion; all five LOCKED at their proposed values + both §6-supersets ACCEPTED — see amendment log) · Lock commit: this file's introducing commit (resolve via `git log --oneline -- <this file>`; firewall lifts only from that commit onward)

---

## §0 — Rule-0 citation block (CITATION-CHAIN mode)

The Pine sources are **gitignored** (`.gitignore:75` → `**/*.pine`) and live outside the repo in `C:\Users\joshu\Downloads\`. A future reader cannot diff the gitignored bytes, so each value below is cited by **file + LastWriteUTC anchor + line range** (read verbatim this session). Re-anchor at session start: if `LastWriteUTC` or `Bytes` differ from this table, RE-READ before trusting any line citation.

| Source file (Downloads) | Bytes | LastWrite (UTC) anchor | Role for Layer D |
|---|---|---|---|
| `ict_daily_dol.pine` | 8456 | 2026-06-18T15:56:18Z | Daily consumer — the frozen config + the live aggregate-rate logic this PREREG re-implements offline |
| `constellation_ict_lib_DRAFT.pine` | 10571 | 2026-06-18T17:53:06Z | **Carries the D-1 fix** (`markTouchedFVGs`, L121-134) — the original `constellation_ict_lib.pine` (10260 B, 2026-06-18T15:56:24Z) is pre-fix and is NOT the test object |

> NOTE on the `ls` display (the `platform-display-tz-edt` trap): the UTC anchors in this table (`17:53:06Z` draft, `15:56:24Z`/`15:56:18Z` originals) are the authoritative **PowerShell `LastWriteTimeUtc`** values; a Bash `ls -la` renders the same files in local ET (UTC-4) as `13:53` / `11:56`. Use PowerShell UTC to re-anchor. The **byte counts** (8456 / 10571 / 10260) are the unambiguous identity anchor and are unaffected by the TZ display. `ict_daily_dol.pine` has **no `_DRAFT`** sibling on disk — its D-1 fix rides entirely in `constellation_ict_lib_DRAFT.pine`.

**Line ranges the frozen-config and method values come from:**
- `ict_daily_dol.pine:21` — `useBody = input.bool(false, ...)` (wick basis, REPORT-ONLY toggle).
- `ict_daily_dol.pine:23` — `pvLen = input.int(3, ...)` (Daily pool universe; provisional per B5).
- `ict_daily_dol.pine:24` — `dispMlt = input.float(1.5, ...)` (FVG displacement filter).
- `ict_daily_dol.pine:25` — `atrLen = input.int(14, ...)` (ATR for displacement).
- `ict_daily_dol.pine:26` — `drawK = input.int(10, ...)` (the K-window = hypothesis horizon, days).
- `ict_daily_dol.pine:28` — `maxReg = input.int(5000, ...)` (registry cap; spans the panel).
- `ict_daily_dol.pine:43,45` — `ict.pushPool(pools, ..., bar_index - pvLen, maxReg)` → **pool t0 = TRUE pivot bar** (`bar_index - pvLen`), not the confirmation bar.
- `ict_daily_dol.pine:51,54` — `ict.pushFVG(fvgs, ..., bar_index, maxReg)` → **FVG t0 = registration bar**.
- `ict_daily_dol.pine:80` — `if p.swept and (p.sweptBar - p.bar) <= drawK` → pool hit measured from the pivot bar (clock recovers sweeps inside the pvLen confirmation lag).
- `ict_daily_dol.pine:88,90` — `f.touched and (f.touchedBar - f.bar) <= drawK` → FVG hit measured from the registration bar.
- `ict_daily_dol.pine:168-171` — `plot(... display = display.data_window)` exports ONLY aggregates (`dolBias`, `dolDirRate`, `poolRate`, `fvgRate`) at the last bar; **no per-object event stream**.
- `constellation_ict_lib_DRAFT.pine:125-134` — `markTouchedFVGs`: the D-1 fix `if not f.touched and barIdx > f.bar` (L128) requires a **strictly-later** touch bar; the original (`constellation_ict_lib.pine:121-130`, pre-fix, no `barIdx > f.bar` guard) pinned `fvgRate` ~100%.

**Consequence that defines this PREREG's instrument:** because the Daily indicator exports only aggregate rates at the last bar (L168-171) and those are **autocorrelated smoke tests by the script's own admission** (L130-132), the verdict is **reconstructed offline from Daily OHLC by re-implementing the lib detectors** (`bullFVG`/`bearFVG`/`bullBounds`/`bearBounds`/`pushPool`/`detectRaid`/`markTouchedFVGs` with the D-1 guard), **NOT** read off the indicator export. Reading the live `fvgRate`/`poolRate` table as the verdict is a forbidden move (§ Forbidden, item 1).

---

## Test object — frozen configuration (zero touches permitted during the verdict window)

Re-implemented offline from Daily OHLC; every parameter pinned to the cited Pine line. LOCKED = void-the-verdict on change; provisional = measurement knob swept inside §6 (D-4); REPORT-ONLY = descriptive, NOT eligible for the verdict.

| Rule | Value | Status | Source (`ict_daily_dol.pine` / lib draft) |
|---|---|---|---|
| K-window (draw horizon) | `drawK = 10` days | **LOCKED** (hypothesis horizon, not a trade knob) | daily L26 |
| FVG basis | wicks (`useBody = false`) | REPORT-ONLY (body is a separate frozen config, not a sweep) | daily L21 |
| Displacement filter | `dispMlt = 1.5 × ATR`, `atrLen = 14` | **LOCKED** for the headline; enters D-4 grid as a swept axis | daily L24-25 |
| Pool universe (pivot strength) | `pvLen = 3` | **provisional** (measurement knob; swept {2,3,5} in D-4) | daily L23 |
| Registry cap | `maxReg = 5000` per side | **LOCKED** (spans panel; FIFO eviction below cap is inert at Daily) | daily L28 |
| Raid / touch convention | inclusive: BSL `hi >= price`, SSL `lo <= price`; FVG near-edge touch | **LOCKED** (symmetric; matches lib `detectRaid` + `markTouchedFVGs`) | lib L99/L104, L129/L132 |
| FVG self-touch guard (D-1) | touch counts only at `barIdx > f.bar` (offline: K-window scan starts `f.bar+1`) | **LOCKED** | lib DRAFT L128 |
| Pool clock origin (D-2) | pool t0 = **TRUE pivot bar** = `bar_index - pvLen`; K-window scan recovers sweeps inside the pvLen confirmation lag | **LOCKED** (genuine choice — see below) | daily L43/L45, L80 |
| FVG clock origin (D-2b) | FVG t0 = **registration bar**, touch scan from `f.bar+1` | **LOCKED** (genuine choice — see below) | daily L51/L54, L88; lib DRAFT L128 |
| Object measured (a) | `poolRate` = P(pool swept within K of pivot t0) | **LOCKED** | daily L80-83, L92 |
| Object measured (b) | `fvgRate` = P(FVG near-edge touched within K of registration t0, touch ≥ f.bar+1) | **LOCKED** | daily L88-91, L93 |
| Base-rate null (D-3) | radius-matched random pseudo-levels per side; MC ≥ 5000 draws; bootstrap CI | **LOCKED** (radius-match defn is a genuine choice — see below) | KILL condition daily L13-14; null never computed in code |
| `dolBias` / nearest-pool magnet | NOT under test | QUARANTINED (REPORT-ONLY; the magnet target is the 1M layer's `dolMode` decision) | daily L62-68, L130-132 |

**Side split (frozen):** pool/FVG rates are computed and gated **per side** — BSL (buyside) vs SSL (sellside) — never pooled across sides, because the base-rate null is radius-matched within a side (BSL distances are above price; SSL below). A pooled rate would mix two distance distributions and break the matched footing.

---

## Resampling unit — block correction (frozen)

Daily objects in the same neighborhood share the same forward price path within K=10 days, so naive per-object rows are pseudo-replicates (the same D-2/D-2b confound the campaign flags). **Point estimates** use all objects in the in-window population (per side). **CIs and the base-rate comparison resample by object-origin block** = one draw per **distinct origin bar** (`pivot bar` for pools, `registration bar` for FVGs), so two objects stamped on the same bar collapse to one block. The block length for the moving-block bootstrap is `drawK = 10` Daily bars (the horizon over which outcomes overlap). The effective-N reported is **block count per side**, not raw object count.

Censoring (frozen): an object whose origin t0 is within `drawK` of the **last bar** has an incomplete K-window — it is **dropped** (right-censored, identical rule for pool and FVG so the comparison stays like-for-like). This is the common-origin / identical-censoring discipline of §7.B D step 3.

---

## Power disclosure (read before judging the verdict)

The decision instrument is a **rate vs a radius-matched base rate with bootstrap CIs — it is an expectation/CI comparison, not a significance test.** "PASS" means a corrected rate clears `base_rate + 95% bootstrap CI half-width`; it does not assert p < 0.05 in the frequentist sense and does not lock or deploy anything.

Per-unit dispersion is rate variance: for a per-side rate `r` over `n_eff` independent blocks, the binomial-floor SE is `sqrt(r(1-r)/n_eff)`; the **block bootstrap is the reported SE** (it absorbs the within-K overlap the binomial floor ignores, so the true SE is wider). At `r ≈ 0.5` and `n_eff = 30` blocks/side, SE ≈ ±0.091 (binomial floor) and is wider under the block bootstrap — i.e. a real rate must beat its base rate by a visibly large margin to clear the CI half-width on this n.

**n-FLOOR (genuine choice, see below) — UNIT = EFFECTIVE BLOCKS, not raw objects: a per-side rate is a decision only at ≥ 30 effective blocks (distinct origin-bar blocks, per the Resampling unit above) of that type on that side after censoring.** Below 30 blocks, the verdict for that object/side is `INSUFFICIENT-N`, NOT a `FALSIFIED` or `RESOLVED` — a starved rate returns ambiguity indistinguishable from a null, and the campaign's standing rule is that a green offline table is not a verdict. (Blocks ≤ objects, because same-bar objects collapse to one block; the SE math above and every verdict-gate trigger use blocks, so the floor must too.) If pools clear n-floor on a side but FVGs do not (or vice versa), only the object that clears is eligible to drive the verdict for that side.

**Single-panel caveat:** this is one SPX-class TV/Pepperstone Daily export. A PASS upgrades credibility and routes to a **path-independent confirmation** — re-run on an **independent price path / period / instrument** (NOT merely a different broker feed of the same SPX series; a feed swap is not independence). Cross-regime stationarity is checked inside §6 via halves; a one-regime PASS is `AMBIGUOUS-HOLD`, not `RESOLVED`.

---

## Verdict gate (binary) — maps to TEST_PLAN §6 "D" row

| Verdict | Trigger |
|---|---|
| `RESOLVED` | After D-1/D-2/D-2b/D-3 fixes, on matched footing: corrected `poolRate` AND/OR `fvgRate` (per side, the side that clears) **> base_rate + 95% bootstrap CI half-width** · AND the clearing object meets the n-floor (≥ 30 blocks that side) · AND the effect is stationary across both halves (both halves' point estimates on the same side of base_rate) · AND the D-4 selectivity probe does NOT explain the clearance (the rate's edge over base_rate survives at matched selectivity) |
| `FALSIFIED` | Neither `poolRate` nor `fvgRate` clears `base_rate + CI half-width` on any side that meets the n-floor, after all D-1/D-2/D-2b/D-3 fixes are applied |
| `AMBIGUOUS-HOLD` | A rate clears base_rate **only** on one censoring or one selectivity/clock convention (e.g. clears at `pvLen=3` but not across the {2,3,5} selectivity-matched cells, OR clears under one clock-origin convention but not the frozen one), OR clears but is one-regime (one half on each side of base_rate) — hold, name the re-test (independent period/instrument) |
| `INSUFFICIENT-N` | No object/side reaches the n-floor (≥ 30 blocks) after censoring — re-spec the panel window (longer/multi-regime), re-test. NOT a falsification of the claim. |

**§6-superset note (flagged, not silent).** This gate is a deliberate *superset* of the literal TEST_PLAN §6 "D" row in two ways, both strengthening (harder to PASS), both booked here for operator sign-off: (i) **D-2b** is added to the fix list (§6 names only "D-1/2/3"; D-2b is the K-window-ORIGIN asymmetry from Appendix A, a legitimately-missed error — the fix is the common-origin clock already in genuine-choice #1); (ii) the **one-regime AMBIGUOUS-HOLD disjunct** ("clears but one half on each side of base_rate") is added beyond §6's "clears only on one censoring/selectivity convention" — it imports the halves-stationarity discipline the §6 W row carries explicitly. Neither weakens the gate; both are operator-ratifiable here.

**Pre-registered before any OHLC touches the offline reconstruction.** Amending this gate mid-run to match emerging numbers is methodology-layer p-hacking (close `AMBIGUOUS-HOLD`, capture why, open fresh).

---

## Forbidden (during the verdict window) — §5 moves that bite Layer D

1. **Reading the live `fvgRate`/`poolRate`/`dolRate` table cell as the verdict.** They are computed over overlapping/autocorrelated windows and the script says so (`ict_daily_dol.pine:130-132`); the pre-fix `fvgRate` was pinned ~100% by the D-1 self-touch. The verdict is the **de-overlapped offline reconstruction with the D-1 guard**, never the export.
2. **Comparing unfiltered pools vs displacement-filtered FVGs without selectivity-matching** (LIB-2 / D-4 confound, lib via daily L42-45 pools vs L49-54 FVGs). Pools are every confirmed pivot; FVGs survive a `1.5×ATR` displacement gate. A raw `poolRate` vs `fvgRate` two-proportion read is confounded by selectivity, not draw-reliability. The D-4 grid (`dispMlt × pvLen`) is the matched-selectivity instrument; report n-per-cell.
3. **Mixing clock origins.** Pool t0 = pivot bar (`bar_index - pvLen`), FVG t0 = registration bar with touch from `f.bar+1`. Silently switching a pool to its confirmation bar (or an FVG to `f.bar`) re-introduces D-2 / D-2b and the D-1 self-touch. The common-origin convention above is frozen; any change voids the verdict.
4. **Skipping the base-rate null (D-3).** The layer is **unfalsifiable** without it — the KILL condition the script names (daily L13-14, "neither rate clears the unconditional base rate") references a null the code never computes. No verdict may be declared until the radius-matched MC null exists with a bootstrap CI.
5. **n-throttle / outcome-conditional tuning of `pvLen` or `dispMlt` to fatten the rate.** Loosening `pvLen` floods the pool universe with minor pivots and lowering `dispMlt` floods FVGs; either can move the headline rate by changing the population, not the draw mechanism. Every D-4 cell reports n-per-cell so an n-driven "win" is visible; the headline is the LOCKED/provisional cell, not the best cell.
6. **Locking `pvLen` (or any D-4 cell) without booking it into the §8.5 DSR/PBO ledger.** The D-4 grid is `dispMlt ∈ {0, 1.5, 3.0} × pvLen ∈ {2, 3, 5} = 9 cells` — declared into the selection budget here, before run 1.
7. **Crediting a Daily PASS toward the 1M DOL gate.** The Daily draw-rate is a descriptive object-reliability claim; the 1M `dolMode` target is range-extreme (REPORT-ONLY `nearest-pool`), a separate ratification. A Daily PASS licenses nothing downstream by itself.

---

## §8.5 DSR/PBO ledger entry (Layer D selection surfaces, declared pre-run)

| Selection surface | Cardinality | n-throttle? | Booking |
|---|---|---|---|
| D-4 selectivity grid `dispMlt{0,1.5,3.0} × pvLen{2,3,5}` | 9 cells | YES (`pvLen` and `dispMlt` both alter the object population) → report n-per-cell | counts toward the campaign DSR/PBO budget; headline = LOCKED/provisional cell only |
| Object choice (pool vs FVG, per side) | 2 objects × 2 sides = 4 | NO | the verdict may credit "AND/OR" per §6; each clearing object/side is one selection — apply the per-cell penalty |
| Base-rate MC | not a selection (null) | n/a | MC ≥ 5000 draws fixed; not a swept knob |

**Combined Layer-D selection budget (declared pre-run): 9 (D-4 grid) + 4 (object×side) = 13 cells.** This figure is the per-cell-penalty base for Layer D and is registered into the campaign-wide joint DSR/PBO budget in [`DSR_PBO_LEDGER.md`](DSR_PBO_LEDGER.md) (surfaces S2 + S3); the base-rate MC is excluded (it is a null, not a selection).

---

## GENUINE PRE-REGISTRATION CHOICES (operator ratification required before run 1)

Every value below is a real choice, not mechanically forced by §6. **PROPOSED until the operator commits this file.** Object only by editing here before the introducing commit; after commit they are frozen.

1. **Clock-origin convention (D-2 / D-2b).** PROPOSED: pool t0 = **TRUE pivot bar** (`bar_index - pvLen`), so the offline reconstruction recovers sweeps that occur inside the pvLen confirmation lag (matches daily L43/L45/L80); FVG t0 = **registration bar** with touch scanned from `f.bar+1` (D-1 guard, lib DRAFT L128). Rationale: this is the faithful clock and the only one that makes pool and FVG K-windows start from a common, like-for-like origin (Appendix B #4 recommends pre-registering exactly this; mixed origins are rejected). Alternative not chosen: pool t0 = confirmation bar (`bar_index`) — simpler, but censors real intra-lag sweeps and is the D-2 defect.

2. **Base-rate null — radius-match definition (D-3).** PROPOSED: for each side, draw MC ≥ 5000 random pseudo-levels per object, each placed at a distance from price drawn from the **same empirical distance distribution as the real objects on that side**, scanned over the **same K-window and same censoring**. The base rate is the fraction of pseudo-levels "drawn to" (swept/touched) within K. PASS band = `real_rate > base_rate + 95% bootstrap CI half-width`. Rationale: matches "did price wander K days far enough to reach a level at this distance," isolating draw-reliability from the trivial fact that nearer levels get hit more. Alternative not chosen: a fixed-offset or uniform-distance null (does not control for the real objects' distance profile → unfair).

3. **n-floor.** PROPOSED: **≥ 30 effective blocks per side** (per object type; block = distinct origin bar per the Resampling unit, **NOT** raw object count — same-bar objects collapse to one block) after censoring for a rate to be a decision; below 30 blocks → `INSUFFICIENT-N`. Rationale: at n_eff≈30 blocks the block-bootstrap CI half-width is already wide (≈0.09+ at r≈0.5); below that the "straddles base_rate" outcome is indistinguishable from starvation. The unit is blocks (not objects) so the floor, the power-disclosure SE, and the verdict-gate triggers all reference the same N. Alternative considered: 50 blocks (stricter, but likely starves a single-panel Daily export → forces INSUFFICIENT-N on most cells).

4. **`pvLen` headline value.** PROPOSED: **Daily `pvLen = 3` as the provisional headline** (daily L23), with {2,3,5} swept in the D-4 grid for selectivity-matching only — NOT a best-of-cell pick. Rationale: 3 is the on-disk default and the B5 pin marks Daily=3 provisional (measurement knob); the headline must be the pinned cell so the grid cannot be mined.

5. **Side-disaggregation of the verdict.** PROPOSED: gate **per side** (BSL / SSL) and report both; the §6 "AND/OR" clears if the qualifying object on **either** side clears its matched base rate at n-floor. Rationale: the radius-match is per-side by construction; a pooled rate mixes distance distributions. Alternative not chosen: pooled both-sides rate (breaks matched footing).

---

## Audit hook

Reviewer question at verdict time: *"Was any criterion above moved, reinterpreted, or supplemented after the offline reconstruction was run on real OHLC?"* Any **yes** → the verdict is void and Layer D stays unresolved. This file's introducing commit/date anchors the registration; evaluation appends below, never edits above.

Runnable checks:

```bash
# §0 re-anchor — confirm the test-object bytes before trusting any line citation:
#   PowerShell:
#   Get-ChildItem 'C:\Users\joshu\Downloads\ict_daily_dol.pine','C:\Users\joshu\Downloads\constellation_ict_lib_DRAFT.pine' |
#     Select Name,Length,LastWriteTimeUtc
#   Expect Length 8456 / 10571. If different -> RE-READ the Pine before evaluating.

# D-1 guard present in the test-object lib draft (else fvgRate is pinned ~100% and measures nothing):
grep -n 'barIdx > f.bar' 'C:/Users/joshu/Downloads/constellation_ict_lib_DRAFT.pine'   # expect a hit at L128

# D-1 falsifier on the live Daily (smoke test only, NOT the verdict): first Daily run with the
# patched lib must show the "FVG draw-rate" table cell < 100.0% with fvg n > 0. A 100.0% cell = bug live.

# .pine gitignore that drove CITATION-CHAIN mode:
grep -n '\*\*/\*\.pine' 'C:/Users/joshu/multi_firm_operations/.claude/worktrees/agitated-leavitt-63fd12/.gitignore'  # expect L75

# Verdict-integrity assertion (the base-rate null must exist before any PASS/FAIL):
#   ASSERT: base_rate_mc_draws >= 5000 AND bootstrap_ci computed per side
#   ASSERT: every reported per-side rate has n_blocks >= 30 OR is labeled INSUFFICIENT-N
#   ASSERT: pool t0 == pivot bar (bar_index - pvLen) AND fvg touch scan starts at f.bar+1
```

---

## Amendment log (append-only)

- **2026-06-18 — RATIFIED (operator-delegated; criterion: most faithful to the design).** All five genuine choices **LOCKED at their proposed values**, each being the design-faithful call: (1) clock origins = TRUE pivot bar for pools / registration bar + `f.bar+1` for FVGs (the faithful common-origin clock, Appendix B #4); (2) D-3 radius-matched MC null per side (the only fair "did price wander far enough to reach a level at this distance" null); (3) n-floor = 30 EFFECTIVE BLOCKS/side; (4) `pvLen=3` headline (the on-disk Daily default + B5 pin), {2,3,5} swept for selectivity only; (5) per-side (BSL/SSL) verdict. **Both §6-supersets ACCEPTED** (D-2b in the fix list; the one-regime halves disjunct on AMBIGUOUS-HOLD) — strengthenings consistent with the W/1H rate layers. **No value changed.** Pre-data: no criterion may move after run 1. Firewall lifts on this file's commit.
- **2026-06-18b -- PRE-DATA RE-ANCHOR (lib publishability fix; behavior-preserving).** The DRAFT lib `constellation_ict_lib_DRAFT.pine` was edited to make it PUBLISHABLE on TradingView: the exported `dol()` carried an unused `method` argument, which is a BLOCKING compile error for an `export` function (CE10237 -- a dead parameter cannot survive a published library API), not the non-blocking warning it is for a regular-indicator local. Fix (lib line 223): `bias` -> `method == 0 ? bias : 0`, which references `method` and returns the identical `bias` for `method==0` (every real call; `method 0 = NEAREST` is the only implemented mode) -- BEHAVIOR-PRESERVING, so the `_ict_offline` port stays faithful. The lib was then published PRIVATE as `jalexante_trades/constellation_ict_lib/1`.
  - **New anchors (these SUPERSEDE the section-0 table + the Audit-hook runnable check at line 150):** `constellation_ict_lib_DRAFT.pine` = **10587 B / 2026-06-18T22:42:47Z** (was 10571 / 17:53:06Z); `ict_daily_dol.pine` = **8454 B / 2026-06-18T22:46:54Z** (was 8456 / 15:56:18Z; operator header/import edits, behavior-identical). The section-0 table and the "Expect Length 8456 / 10571" check retain their ratification-time values as the historical record; a re-anchor check WILL mismatch them -- that is expected, and is resolved here. The 10260 B / 15:56:24Z pre-fix original lib is unchanged.
  - **Behaviors re-verified byte-identical at the new sizes** (no line-number shift for the cited rules): D-1 guard `barIdx > f.bar` (lib L128); strict `age > drawK` MISS rule (daily L82/L90); displacement `na(atrVal) ? false : rng > mult*atrVal` (lib L71-73); pool t0 / FVG t0 clocks (daily L43/45/51/54/80/88). The working-pointer cites in `_ict_offline.py`, `harness_d.py`, and `README.md` were updated to the new anchors; the frozen section-0 table (and `TEST_PLAN.md` section 0) keep the ratification-time anchors. **No verdict criterion, frozen constant, or genuine choice changed.** PRE-DATA provenance correction (no real OHLC has been run), so the audit-hook "moved after run 1" stricture is not engaged.

- **2026-06-19 — POST-DATA CLARIFICATION (documentation-only; NO criterion moved, reinterpreted, or supplemented; recorded D verdict UNAFFECTED).** A code audit of `harness_d._censor` surfaced a genuine **offline-vs-Pine** semantic divergence in the FROZEN right-censor (the "Resampling unit — block correction" section above). It is documented here (and in the `_censor` docstring + a pinning test `test_censor_drops_right_edge_fast_hit_conservative_vs_pine`) as a **deliberate conservative simplification**; the censor is **not** changed.
  - **What the frozen rule says, and what the offline implements (UNCHANGED):** "an object whose origin t0 is within `drawK` of the last bar … is **dropped**" — ALL such objects, with **no hit-exception**. `harness_d._censor` implements exactly that (`bar < n − 1 − drawK`, strict). The implementation is faithful to the **frozen PREREG rule**; the divergence below is PREREG-vs-Pine, not implementation-vs-PREREG.
  - **The divergence:** `ict_daily_dol.pine` **L80** (pool) / **L88** (FVG) **COUNT a swept/touched-WITHIN-K object as a HIT even when its age ≤ drawK**, excluding from the population **only** the UNSWEPT age≤drawK objects (truly incomplete window). The offline censor is stricter — it also drops the within-K **right-edge fast-hits** Pine keeps. The prior `_censor` docstring documented only the `age == drawK` strictness ("mirror the STRICT Pine rule") and did **not** flag this fast-hit difference; that omission is what this note + the docstring expansion repair.
  - **Why it is correct, not a bug:** per **Forbidden item 1**, the verdict is the **de-overlapped offline reconstruction**, explicitly **NOT** the Pine aggregate table (an autocorrelated smoke test by the script's own admission, daily L130-132). Keeping right-edge fast-hits while dropping their unswept-incomplete neighbors would bias the rate **upward** at the right edge (a right-censoring / immortal-time bias — you retain only objects that resolved fast enough to be observed). Dropping every age≤drawK object gives each survivor a fully-observable K-window. The effect is **(i) UNIFORM across pools and FVGs** (the like-for-like footing the frozen rule requires is preserved) and **(ii) strictly CONSERVATIVE** for a RESOLVED verdict (restoring fast-hits can only RAISE a rate; the offline rate is a **lower bound** on the Pine-faithful rate).
  - **Verdict impact: NONE — robust both directions.** SSL.fvg **RESOLVED** (0.795 vs base 0.712, +0.083 margin) holds *a fortiori* — the Pine-faithful rate is ≥ 0.795. BSL **FALSIFIED** is robust: the right-censored region is ≤ `drawK` = 10 of 4,570 bars → at most a handful of fast-hit objects → sub-0.01 rate movement, far inside the ≈0.09 block-CI half-width that BSL.fvg (0.729 ≈ base 0.731) and both pools (0.55/0.34 vs base 0.76/0.61) would need to cross.
  - **Disposition chosen: (a) document — do NOT make the censor hit-aware.** Option (b) (a hit-aware censor that keeps `hit_within_K` objects to bit-match Pine) is a **post-run change to a FROZEN criterion** that would **trip the audit hook and VOID the recorded D verdict**, would **reintroduce** the right-edge censoring bias the frozen rule removes, and is **not executable** in-repo (the Daily OHLC export is gitignored on the operator's machine, so `evaluate()` cannot be re-run on real data to confirm invariance). This clarification changes **no value, threshold, or implemented behavior** — the `_censor` bytes are behaviorally identical pre/post. PRE-existing behavior, POST-data documentation → the audit-hook "moved after run 1" stricture is **not** engaged (nothing moved).
