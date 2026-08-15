# Q-ICT-CASCADE-1 -- §8.5 DSR/PBO SELECTION-MULTIPLICITY LEDGER

**Seeded 2026-06-18 (pre-data). APPEND-ONLY.** This is the single family-wise
accounting surface for the whole cascade. Every selection that could manufacture
a >baseline reading -- best-of-K grid, gate-ablation matrix, object/side choice,
n-throttle knob, and every LOCK knob -- is enumerated here and booked into ONE
joint budget over the UNION of selection surfaces. The pre-registered lock ORDER
(B1->B5, then per-layer §7.B steps, plateaus last) reduces *sequential
dependence* between picks; it does **NOT** bound family-wise error. That is what
this ledger is for.

> Authority chain: TEST_PLAN §5 ("Locking a knob without booking its selection
> into the §8.5 DSR/PBO ledger" = forbidden move), §8 ("state a joint DSR/PBO
> budget over the UNION of selection surfaces"), Appendix C "Multiplicity (HIGH)".
> Per-layer surfaces are transcribed from the four **PROPOSED** PREREGs
> (`PREREG-W.md`, `PREREG-D.md`, `PREREG-1H.md`, `PREREG-1M.md`) -- all four are
> PROPOSED (not yet committed). This ledger's seed is contingent on their commit;
> any pre-commit change to a flagged GENUINE CHOICE propagates here.
>
> **STATUS: RATIFIED 2026-06-18 (operator-delegated) / pre-data.** The [OP-GATED]
> cells in §1 are now **RATIFIED** at their PREREG values — the operator delegated
> the genuine-choice calls to Claude with a "most faithful to the design" criterion
> (see each owning PREREG's amendment log). **M = 65 stands**: no grid bound moved,
> so no cardinality changed. (The two 1M refinements — drop-top-k SCALED to
> ceil(0.06 x n_blocks), multi-regime window BINDING SPEC — are stringency/scope
> calls, not cardinality changes.) The §6 booking log remains the live append
> surface as each cell is credited.
>
> **Standing rule:** no layer verdict may credit a selected cell (best-of-K
> winner, ablation arm, swept knob) until that cell's selection is booked below
> AND the per-cell penalty has been applied AND the cell is inside the joint
> budget AND the cell clears its owning PREREG's n-floor (§4 INSUFFICIENT-N gate).
> A green cell that is not in this ledger is not a verdict.

---

## §0 -- Rule-0 / citation provenance

Selection surfaces are defined by the four **PROPOSED** PREREGs and by the gitignored
Pine sources they cite (`.gitignore:75` -> `**/*.pine`, outside the repo in
`C:\Users\joshu\Downloads\`). This ledger does NOT re-read the Pine -- it
transcribes the grids each PREREG already pinned against its own §0 citation
chain. The PREREGs are PROPOSED (uncommitted); committing them is what lifts their
firewalls and ratifies the [OP-GATED] cells below. If a PREREG is amended (its
Amendment log gains an entry that changes a grid cardinality), this ledger MUST
gain a matching append entry in the same commit, or the joint budget is stale.

| PREREG (test object) | Surfaces it contributes | Config anchor (PROPOSED) |
|---|---|---|
| `PREREG-W.md`  | W vote-importance best-of-K (4) + W LOCK knobs | structure-only `gateHitRate`; `emaLen=20` |
| `PREREG-D.md`  | D-4 selectivity grid (9) + object/side choice (4) + D LOCK knobs | `pvLen=3` prov / `dispMlt=1.5` / `drawK=10` |
| `PREREG-1H.md` | 1H anchor x lookN x eqBand (9) + 1H LOCK knobs | `lookback-extremes` / `lookN=60` / `eqBand=0.05` / `fwdK=12` |
| `PREREG-1M.md` | 1M variant(2) x gate-ablation(8) + dolMode + 1M LOCK knobs | `dolMode=range-extreme` / `useBody`{T,F} / `useKillzone` ablated |

---

## §1 -- Enumeration of selection surfaces (the UNION)

Two classes are tracked. **BUDGETED** surfaces consume family-wise error and
take a per-cell penalty. **REPORT-ONLY** surfaces are excluded from the budget
(rationale in §3) and may never drive a verdict or spend a best-of-K / permutation
cell. n-throttle knobs are flagged: they alter the population (n), so an "win"
that is really an n-effect must be visible -- they REQUIRE n-per-cell reporting.

**[OP-GATED] inventory (RATIFIED 2026-06-18, operator-delegated).** The following booked
cells carry a value/bound the owning PREREG flagged as a GENUINE PRE-REGISTRATION
CHOICE; all are now **RATIFIED at their PREREG values** (operator-delegated, design-faithful)
and frozen against post-data tuning. None changed a cardinality, so M=65 is unaffected:
- **S4** 1H grid bounds `lookN{40,60,80} x eqBand{0,0.05,0.10}` -- PREREG-1H GENUINE CHOICEs (the ±20 / {0,0.10} neighbors).
- **S6** 1M `useBody` two-frozen-variant split -- PREREG-1M GENUINE CHOICE #2.
- **L9** Daily `pvLen=3` provisional headline -- PREREG-D GENUINE CHOICE #4.
- **L11 / L12** D pool/FVG clock origins -- PREREG-D GENUINE CHOICE #1.
- **L18** 1M `dolMode=range-extreme` as the gate-bearing target -- PREREG-1M GENUINE CHOICE #1.
Everything else (cardinalities forced by §6/§7.B, the LOCK values transcribed from the drafts) is not operator-gated. M is computed on the PROPOSED set; ratification does not change M unless a bound moves.

### 1.A -- BUDGETED best-of-K / selection grids

| # | Layer | Selection surface | Cardinality | n-throttle | PREREG source |
|---|---|---|---|---|---|
| S1 | W   | Vote-importance best-of-K (solo hit-rate per vote vs structure-only baseline): `vStruct, vSeason, vRates, vEarn` | **4 cells** | no | PREREG-W frozen-config "Vote set"; verdict "Vote-importance sub-verdict" |
| S2 | D   | D-4 selectivity grid `dispMlt{0,1.5,3.0} x pvLen{2,3,5}` | **9 cells** | **YES** (`pvLen` + `dispMlt` both alter object population) | PREREG-D §8.5 entry; forbidden #5/#6 |
| S3 | D   | Object choice `(pool vs FVG) x side (BSL/SSL)` | **4 cells** | no | PREREG-D §8.5 entry; verdict "AND/OR per side" |
| S4 | 1H  | Anchor x lookN x eqBand (gate-relevant): `lookback-extremes(1) x lookN{40,60,80} x eqBand{0,0.05,0.10}` | **9 cells** | **YES** (`eqBand=0` scores every bar -> 1H-E6) | PREREG-1H "Anchor sweep + multiplicity penalty" |
| S5 | 1M  | Gate-ablation matrix `bias x PD x killzone` (all on/off combos, 2^3) | **8 cells** | partial (each gate prunes n; marginal-E[R] CI must exclude 0, not just prune) | PREREG-1M frozen-config "Killzone gate"; assertion "exactly 8 labeled exports" |
| S6 | 1M  | Variant split `useBody` (wick / body) -- two frozen configs, each evaluated end-to-end | **2 cells** | no | PREREG-1M GENUINE CHOICE #2 |

**Best-of-K / grid subtotal (BUDGETED): 4 + 9 + 4 + 9 + 8 + 2 = 36 cells.**

> **Scope note (ledger SYNTHESIZES, does not merely transcribe).** TEST_PLAN §5
> names only "two explicit best-of-K grids (1H anchor x lookN x eqBand; W vote
> set)" = S4 + S1. The other four budgeted surfaces -- **S2** (D-4 selectivity),
> **S3** (D object/side), **S5** (1M gate-ablation), **S6** (1M variant split) --
> are ledger-derived expansions of the TEST_PLAN's under-specified multiplicity
> surface (each is a real selection the per-layer §7.B steps introduce). This is a
> deliberate *strengthening* (more cells priced = more conservative), not a drop:
> a future auditor seeing only "two grids" in §5 should read this note, not assume
> S2/S3/S5/S6 were removed from a PREREG.

> S5 x S6 interaction note: the variant split (S6) is run THROUGH the ablation
> matrix (S5) -- i.e. each of the 2 `useBody` configs has its own 2^3 ablation,
> so the realized 1M selection space is 2 x 8 = 16 distinct labeled exports.
> The ledger books the AXES (S5=8, S6=2) and the joint 1M cardinality (16) in
> §2; the penalty is applied over the joint 1M family, NOT 8 and 2 independently
> (booking them as 10 would under-count the cross-product).

### 1.B -- BUDGETED n-throttle knobs (single-value LOCKs that still throttle n)

These are not multi-cell grids in the verdict path, but each is an
outcome-conditional n lever (TEST_PLAN §5: "choosing `eqBand`/`minAbsR` to fatten
n and then reading the rate on that n"). They are booked so that any future
sensitivity move on them is already in the family, and they REQUIRE n-per-cell
reporting wherever they appear.

| # | Layer | n-throttle knob | Locked value | Why it throttles n | PREREG source |
|---|---|---|---|---|---|
| T1 | 1M  | `minAbsR` (>=2.0R min target) | 2.0 (LOCKED) | raises the target floor -> drops sub-2R setups -> shrinks n | PREREG-1M frozen-config; forbidden #3 |
| T2 | 1M  | `eqBand` (1H equilibrium band, used in 1M PD gate) | 0.05 (LOCKED, =1H) | `eqBand=0` would score every bar; band width gates stand-down | PREREG-1M; mirrors 1H-E6 |
| T3 | 1M  | `useDOL` (DOL target on/off vs fixed-R) | true (LOCKED for verdict; off is §7.B step-5 comparative) | nearest/range target can starve n->0 (B4 starvation) | PREREG-1M; TEST_PLAN §7.A B4 |

> `eqBand` also appears as a SWEPT axis inside S4 (1H grid {0,0.05,0.10}); T2 is
> its 1M-side LOCK. They are the SAME knob at two layers -- booked once per layer
> because the 1M gate and the 1H measurement are different objects. Any change to
> 1M `eqBand=0.05` voids PREREG-1H's transfer pre-gate (the `lookN`/`eqBand`
> desync constraint) AND PREREG-1M.

### 1.C -- BUDGETED LOCK knobs (the ~16 from Appendix C)

Each LOCKed faithfulness/config constant is a *selection that has already been
made* (a point chosen out of a space of alternatives). Appendix C counts ~16.
They consume family-wise error implicitly: a config that survives only because
these were set favorably is overfit. Booking them makes "we picked this value"
auditable and forces any later sensitivity sweep on them into the family. None is
a multi-cell grid in the current verdict path (cardinality 1 each), but each is a
booked degree of freedom.

| # | Layer | LOCK knob | Locked value | PREREG source |
|---|---|---|---|---|
| L1  | LIB | FVG orientation convention | standard-ICT (`bull = low[0] > high[2]`) | TEST_PLAN §7.A B1; Appendix B #1 |
| L2  | LIB | Raid/touch convention | inclusive symmetric (`>=`/`<=`); FVG near-edge | PREREG-D frozen-config; Appendix B #5 |
| L3  | LIB | FVG edge convention (scoring vs magnet) | near-edge scoring/touch | Appendix B #3 |
| L4  | W   | `emaLen` (structure EMA) | 20 (== 1M `wEmaLen`) | PREREG-W frozen-config; forbidden #5 |
| L5  | W   | Flat-week scoring | exclude `realized==0` from rate; report flat count | PREREG-W frozen-config; Appendix B #7 |
| L6  | W   | Denominator basis | recompute `scored`/`gateScored` (never `mean(hit)`) | PREREG-W frozen-config |
| L7  | D   | `drawK` (draw horizon) | 10 days | PREREG-D frozen-config |
| L8  | D   | `dispMlt` headline (FVG displacement) | 1.5 x ATR (`atrLen=14`) | PREREG-D frozen-config (also S2 axis) |
| L9  | D   | `pvLen` headline (Daily) | 3 provisional (also S2 axis) | PREREG-D §7.A B5; GENUINE CHOICE #4 |
| L10 | D   | `maxReg` (registry cap) | 5000 / side | PREREG-D frozen-config |
| L11 | D   | Pool clock origin (D-2) | TRUE pivot bar `bar_index - pvLen` | PREREG-D GENUINE CHOICE #1 |
| L12 | D   | FVG clock origin (D-2b) + self-touch (D-1) | registration bar; touch scan `f.bar+1` | PREREG-D GENUINE CHOICE #1; B3 D-1 |
| L13 | 1H  | Anchor rule (gate-relevant) | `lookback-extremes` (also S4 fixed axis) | PREREG-1H frozen-config |
| L14 | 1H  | `lookN` headline | 60 (== 1M `pdLookN`; also S4 axis) | PREREG-1H frozen-config; forbidden #4 |
| L15 | 1H  | `fwdK` (follow-through window) | 12 (measurement horizon) | PREREG-1H frozen-config |
| L16 | 1M  | `pvLen` (raid pools) | 2 LOCKED (gate-bearing) | PREREG-1M frozen-config; PREREG-pvLen |
| L17 | 1M  | `raidWin` (raid->entry window) | 8 bars | PREREG-1M frozen-config |
| L18 | 1M  | `dolMode` (DOL target) | range-extreme (gate-bearing) | PREREG-1M; PREREG-dolMode |
| L19 | 1M  | `minRmult` (hurdle multiple) | 4.0 (this is the §6 4x) | PREREG-1M frozen-config |
| L20 | 1M  | Killzone zone set + windows | London 0200-0500 + NY-AM 0700-1000 ON / NY-PM 1330-1600 OFF, ET DST-safe | PREREG-1M; PREREG-killzone (FROZEN, not swept) |

> Count is 20 booked LOCK knobs (Appendix C's "~16" is the order-of-magnitude
> floor; this enumeration is the exact set and is the canonical count -- if a
> later session disputes "~16 vs 20", the discrepancy is reconciled HERE, not in
> CLAUDE.md). L1/L2/L3 are LIB-foundation locks shared by all consumers; L8/L9
> and L13/L14 double as S2/S4 swept axes -- their headline VALUE is the booked
> LOCK, the SWEEP is the booked grid; the headline is always the pinned cell, NOT
> the best cell (PREREG-D forbidden #5, PREREG-1H forbidden #3).

---

## §2 -- The JOINT budget (over the UNION, not per-layer)

The family-wise error is bounded over the **union** of BUDGETED surfaces. Booking
each layer's grid against its own per-layer penalty (as the four PREREGs do
locally) is necessary but NOT sufficient -- four locally-clean layers can still
constitute a 36-cell fishing expedition jointly. The joint budget is the gate.

**Joint BUDGETED cell count (the family size M):**

```
  best-of-K / grids (§1.A):  S1(4) + S2(9) + S3(4) + S4(9) + [S5 x S6 = 8 x 2 = 16]  = 42
  n-throttle LOCKs (§1.B):   T1 + T2 + T3                                            =  3
  LOCK knobs (§1.C):         L1..L20                                                 = 20
  ----------------------------------------------------------------------------------------
  JOINT FAMILY SIZE  M  =  42 + 3 + 20                                               = 65
```

> Note the 1M family is booked as the **cross-product** 16 (S5 x S6), not the
> axis sum 10 -- the 2 variants x 8 ablation arms are 16 distinct labeled
> exports (PREREG-1M run-time assertion: "exactly 8 labeled exports" PER variant).
> Booking 10 would under-count the joint 1M selection space by 6 cells and
> under-penalize. The conservative joint family size is **M = 65**.

**Budget allocation.** Family-wise alpha is allocated, not spent per-layer in
isolation:

- **Headline-cell exemption.** Each layer's HEADLINE is the PINNED cell (the
  LOCKed/provisional value), not a selected winner. A headline reading does NOT
  spend a best-of-K cell -- it is the pre-registered point estimate. The penalty
  applies to the SELECTION among cells (best-of-K winner, ablation arm marginal,
  swept-grid best), not to reading the pinned cell. This keeps the budget from
  double-charging the pre-registered point.
- **Selected-cell charge.** Any cell credited toward a verdict OTHER than the
  pinned headline -- a best-of-K importance winner (S1), a swept-grid cell that
  beats the headline (S2/S4), an ablation arm whose marginal-E[R] is read (S5), a
  non-pinned object/side that drives the §6 AND/OR (S3) -- spends one cell of the
  joint family M and takes the per-cell penalty in §4.
- **Joint family-wise control.** The per-cell penalty (§4) is computed against
  the **joint** M (=65 conservative; =59 if the 1M family is booked as the axis
  sum 10 -- the conservative M=65 governs). A cell that clears its LOCAL per-layer
  penalty but NOT the joint penalty does **not** earn a PASS. This is the line
  Appendix C draws: lock ORDER mitigates sequential dependence; only the joint
  budget bounds FWER.

**Why the lock ORDER is not enough (recorded, do not re-litigate).** B1->B5 then
§7.B steps then plateaus is a *dependency* ordering (each later pick is taken
given the earlier locks). It removes some conditioning paths but does nothing
about the fact that 65 degrees of freedom were available to make the cascade look
good. FWER scales with M, not with the order in which M was traversed. The joint
budget is the only instrument that prices M.

---

## §3 -- REPORT-ONLY surfaces (EXCLUDED from the budget) -- and why

These surfaces are descriptive only. They may appear in tables, but they may
NEVER drive a verdict and they spend NO best-of-K / permutation budget. Excluding
them is itself a pre-registered choice (booked here so it is auditable); promoting
any of them into the verdict later is a forbidden move and voids the relevant
PREREG.

| # | Layer | REPORT-ONLY surface | Cardinality (descriptive) | Why excluded |
|---|---|---|---|---|
| R1 | 1H | `swing-pair` anchor | (exploration) | The live 1M gate uses **lookback-extremes**, not swing-pair. Validating swing-pair validates nothing about the gate; counting it would spend a cell on a non-gate object. PREREG-1H forbidden #6. |
| R2 | 1M | `dolMode = nearest-pool` | 1 alt | Gate-bearing target is **range-extreme** (PREREG-dolMode). nearest-pool is the descriptive alternative; letting it into the lock decision is the "dolMode selection-leak" the D1 review flagged. PREREG-1M forbidden #5. |
| R3 | D  | Base-rate MC null draws (>=5000) | 5000 draws | A **null**, not a swept knob. The 5000 draws are a fixed MC sample size for the radius-matched base rate, not a selection among configs -- nothing is "chosen" from them. Booking them as 5000 cells would be a category error. PREREG-D §8.5 ("not a selection"). |
| R4 | 1M | `useDOL = false` (fixed-R) arm | 1 | §7.B step-5 **comparative** (DOL vs fixed-R at comparable n), not a gate cell. Reported for context; the verdict is on the LOCKed `useDOL=true` config. (The on/off LEVER is booked as n-throttle T3; the fixed-R comparative READING is REPORT-ONLY.) |
| R5 | * | `pointVal=1.0` ($/notional) + static-$200K $/DD series | n/a | The headline currency is **R**; `pointVal` is R-invariant (1M-E3) and any $/DD is REPORT-ONLY off the static-$200K recompute. No selection; no budget. PREREG-1M frozen-config L43; TEST_PLAN §5. |

> **DOW x arm-time-killzone one-slice permutation partitions (20).** These are
> NOT a selection surface and are NOT budgeted here. They are a *concentration
> check* (the §6 "no single slice carries the edge" test): a permutation null
> over partitions, not a best-of-K from which a winner is chosen. The 5 DOW x 4
> arm-time-zone = 20 partitions are the slices the permutation scans; the
> permutation B (>=5000) prices the multiple comparisons WITHIN that test
> internally (max-statistic over slices). Booking them as 20 budget cells would
> double-count -- the permutation already controls its own family. They are
> recorded here for completeness and explicitly EXCLUDED from M.

---

## §4 -- Per-cell penalty method (per surface)

Each BUDGETED surface declares its penalty BEFORE its first run. The penalty is a
**max-statistic / deflated** correction over the cells, computed against the joint
family M where the surface's winner competes cascade-wide; the local per-layer
penalty is the floor, the joint is the gate (§2).

| Surface | Cells | Penalty method (declared pre-run) | n-per-cell required? |
|---|---|---|---|
| S1 (W vote-importance) | 4 | **Max-statistic label-permutation, B=10000** over the 4 inputs (PREREG-W). A vote dies unless it solo-beats structure-only after the max-stat penalty. | no |
| S2 (D selectivity grid) | 9 | **Deflated-Sharpe / Bonferroni (max-stat)** over the 9 `dispMlt x pvLen` cells. Headline = pinned cell; any beating cell takes the 9-cell penalty AND must survive the joint-M penalty. | **YES** (population changes with `pvLen`,`dispMlt`) |
| S3 (D object/side) | 4 | **Per-cell penalty** over the 2 objects x 2 sides; each clearing object/side that drives the §6 AND/OR is one selection. | implicit (n-floor >=30 blocks/side; report n) |
| S4 (1H anchor grid) | 9 | **Deflated-Sharpe or Bonferroni (max-stat)** over the 9 `lookback-extremes x lookN x eqBand` cells (PREREG-1H). Winner must clear 0.5 by >=2pp AFTER the penalty. | **YES** (`eqBand=0` is an n-throttle, 1H-E6) |
| S5 (1M gate-ablation) | 8 | **Marginal-E[R] CI-excludes-0 per retained gate** within the 2^3 matrix; each gate must LIFT E[R], not prune n. Permutation B>=5000 (block, by entry event). | **YES** (each gate prunes n; report n-per-arm) |
| S6 (1M variant split) | 2 | **Both frozen, both reported**; neither dropped after seeing which wins (PREREG-1M forbidden #3). No best-of-2 pick. | report n per variant |
| S5 x S6 joint | 16 | The 1M family penalty is over the **16** cross-product cells, applied jointly (not 8 and 2 separately). | as above |
| T1/T2/T3 (n-throttle LOCKs) | 1 ea | No grid penalty at the pinned value; **n-per-cell MANDATORY** so any future sensitivity move on them is visible as an n-effect, not a signal. | **YES (mandatory)** |
| L1..L20 (LOCK knobs) | 1 ea | No grid penalty at the pinned value (cardinality 1); booked as degrees of freedom. **Any later sensitivity sweep** on an L-knob converts it to a grid surface and MUST be appended here with its own max-stat penalty BEFORE that sweep runs. | n/a until swept |

**Joint-M correction (the gate).** The campaign's standing instrument is
**deflated-Sharpe (DSR)** for R-denominated continuous metrics (1M E[R]) and
**PBO** (probability of backtest overfitting, combinatorially-symmetric
cross-validation) for the plateau/lock-order step (§7.B 1M step-8). For binary
rate layers (W, D, 1H) the max-statistic label/block permutation against the
per-layer null IS the per-cell penalty; the joint correction multiplies the
effective family size to M=65 (conservative) when a selected cell competes for a
cascade-level credibility upgrade. **Bonferroni is the conservative fallback**
where a rate's null distribution is ill-behaved at small effective-N (PREREG-1H
GENUINE CHOICE #4). The penalty FAMILY (DSR vs Bonferroni vs PBO) per surface is
pinned in that surface's PREREG; this ledger records which applies and that the
JOINT M is the denominator, not the per-layer cell count.

**n-per-cell reporting (the n-throttle discipline).** For every surface flagged
"YES" above -- S2, S4, S5, and the T1/T2/T3 knobs (`eqBand`, `minAbsR`,
`useDOL`) -- the appended verdict row MUST carry n-per-cell. The failure shape
this prevents: a cell "wins" only because the knob fattened n (lower `minAbsR`,
`eqBand=0`, `useDOL=true` flooding setups), and the rate is read on that fattened
n. n-per-cell makes an n-driven win visible (TEST_PLAN §5; PREREG-D forbidden #5;
PREREG-1H forbidden #5; PREREG-1M forbidden #3).

**INSUFFICIENT-N gate (binds the booking log, §6).** A booked cell whose
**n-per-cell is below the owning PREREG's n-floor** (W: 30 effective scored weeks;
D: 30 effective blocks/side; 1H: 30 effective windows/zone; 1M: 100 closed trades)
is **`INSUFFICIENT-N` -- never a PASS and never a FAIL**, regardless of the
joint-M penalty result. The joint-M penalty is a *selection* control; it cannot
rescue a starved cell, and a starved cell that happens to clear the penalty is a
power artifact, not a verdict. So a §6 booking row's "Verdict vs joint budget"
column is `INSUFFICIENT-N` whenever n-per-cell < the layer floor, and only cells
at/above the floor are eligible for PASS/FAIL. This closes the gap where an
n-throttled cell (the exact failure the n-per-cell discipline names) could be
booked PASS on the joint-M penalty alone.

---

## §5 -- Append protocol (this ledger is OPENED now, APPENDED as each lock books)

This file is **seeded pre-data (2026-06-18)** with the enumeration, the joint
budget, the REPORT-ONLY exclusions, and the penalty methods. It is **append-only**
from here:

1. **Each lock booking** (when a layer's PREREG is committed and its firewall
   lifts, or when a selected cell is credited toward a verdict) appends ONE row to
   §6 below: surface ID, the cell selected, n-per-cell (if flagged), the local
   per-layer penalty result, the joint-M penalty result, PASS/FAIL against the
   joint budget, date, commit. **The "Verdict vs joint budget" column is
   `INSUFFICIENT-N` whenever n-per-cell is below the owning PREREG's n-floor (§4
   INSUFFICIENT-N gate) -- the joint-M penalty is not even consulted for a starved
   cell.**
2. **No edits above §6.** The enumeration (§1), joint budget (§2), exclusions
   (§3), and penalty methods (§4) are frozen at seed. Changing a grid cardinality
   requires a matching PREREG amendment AND an append entry in §6 noting the M
   change -- never a silent edit to §1/§2.
3. **A selected cell is not a verdict until its §6 row exists** with the joint-M
   penalty applied. A green offline cell absent from §6 is, per the campaign
   standing rule, not a verdict.
4. **M is recomputed on every append that changes the family** (a new swept
   L-knob, a PREREG grid amendment). The recomputed M and its derivation go in
   the §6 row; the new M governs all subsequent penalties.

---

## §6 -- BOOKING LOG (append-only; one row per lock/selected-cell)

| Date | Surface | Cell selected | n-per-cell | Local penalty result | Joint-M penalty (M) | Verdict vs joint budget | Commit |
|---|---|---|---|---|---|---|---|
| 2026-06-18 | -- (SEED) | ledger opened; family enumerated | n/a | n/a | M = 65 (conservative; 59 if 1M booked as axis-sum 10) | n/a -- pre-data | this file's introducing commit |

_(append below this line as each lock is booked -- never edit the seed row or anything above §6)_

---

## §7 -- Audit hook (runnable)

Reviewer question at any verdict: *"Is every cell credited toward this verdict
booked in §6, with n-per-cell where flagged, and did it clear the JOINT-M penalty
(not just its local per-layer penalty)?"* Any **no** -> the verdict is void.

```bash
# This ledger's introducing commit anchors the seed (M=65 frozen pre-data):
git log --oneline -- lab/analysis/ict_cascade_2026-06-18/DSR_PBO_LEDGER.md | tail -1

# Family-size consistency: every BUDGETED grid cardinality here must match its PREREG.
#   S1 W vote set = 4:
grep -nE 'vStruct.*vSeason.*vRates.*vEarn|4 inputs' lab/analysis/ict_cascade_2026-06-18/PREREG-W.md
#   S2 D selectivity grid = 9 (dispMlt{0,1.5,3.0} x pvLen{2,3,5}):
grep -nE 'dispMlt.*0.*1.5.*3.0|9 cells' lab/analysis/ict_cascade_2026-06-18/PREREG-D.md
#   S4 1H grid = 9 (lookN x eqBand, anchor fixed) -- match literal tokens as written:
grep -nE '9 gate-relevant cells|lookN.*eqBand|eqBand.*lookN' lab/analysis/ict_cascade_2026-06-18/PREREG-1H.md
#   S5 1M ablation = 8 ("exactly 8 labeled exports", bias x PD x killzone) -- literal tokens (no regex metachars):
grep -nFe 'exactly 8 labeled' -e 'bias x PD x killzone' lab/analysis/ict_cascade_2026-06-18/PREREG-1M.md
#   S6 1M variant = 2 (useBody T/F):
grep -nE 'useBody.*true AND false|two frozen variants' lab/analysis/ict_cascade_2026-06-18/PREREG-1M.md

# REPORT-ONLY exclusions must NOT be credited in any §6 row:
#   swing-pair (R1), nearest-pool (R2) must appear ONLY in §3, never §6 "Cell selected".
grep -nE 'swing-pair|nearest-pool' lab/analysis/ict_cascade_2026-06-18/DSR_PBO_LEDGER.md
#   Expect hits in §1 (1H S4 fixed-axis note), §3 (R1/R2) -- NEVER in the §6 booking log.

# Joint-M guard: a selected cell that clears local penalty but not joint-M is NOT a PASS.
#   ASSERT for each §6 row with a non-headline cell: joint-M column applied at M(current) AND PASS only if joint penalty clears.

# Append-only guard: §1-§5 + the §6 seed row are frozen; only rows are added under §6.
#   git diff on this file across a booking commit must touch ONLY lines below the §6 seed row.
```

---

## Amendment log (append-only)

- **2026-06-18 — RATIFIED (operator-delegated; criterion: most faithful to the design).** The [OP-GATED] cells (§1) are ratified at their PREREG values. **M = 65 unchanged** (no grid bound moved; the 1M drop-top-k scaling + multi-regime window binding are stringency/scope refinements, not cardinality changes). The §6 booking log is the live append surface.

_(seeded pre-data 2026-06-18; the §6 booking log is the live append surface.)_
