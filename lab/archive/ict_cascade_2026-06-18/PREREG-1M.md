# Q-ICT-1M (Q-ICT-CASCADE-1, Layer 4 / Execution) — VERDICT PRE-REGISTRATION

**Registered before any List-of-Trades export is run through analysis. No criterion below may be moved after the first real-population (n>=100) run. The commit of this file is the lock that lifts the firewall.**

Parent campaign: [`lab/analysis/ict_cascade_2026-06-18/TEST_PLAN.md`](TEST_PLAN.md) (Layer 1M = §4 H-1M, §6 1M row, §7.B 1M, §8 PREREG-1M/-dolMode/-killzone)
Authored: 2026-06-18 · **Lock date: RATIFIED 2026-06-18** (operator delegated the genuine-choice calls to Claude with a "most faithful to the design" criterion; LOCKED — two design-faithful refinements vs the proposed defaults: drop-top-k SCALED, multi-regime window BINDING SPEC — see amendment log) · Lock commit: this file's introducing commit (resolve via `git log --oneline -- <this file>`; firewall lifts only from that commit onward)

> **Status: PROPOSED — not yet committed.** Every value below is rendered from TEST_PLAN §4/§6/§7.B/§8 verbatim. The thresholds are mechanically forced by §6; the items in "GENUINE PRE-REGISTRATION CHOICES" are real operator calls and stay PROPOSED until the operator commits this file.

---

## §0 — Rule-0 citation (production source read this session)

The 1M Pine is **gitignored** (`.gitignore:75` -> `**/*.pine`, confirmed by grep) and lives outside the repo in `C:\Users\joshu\Downloads\`. A future reader **cannot diff these bytes** — this is **CITATION-CHAIN mode**: file + LastWriteUTC + line ranges are the anchor; re-read on resume (Downloads is mutable; line numbers drift if edited).

| Source file (Downloads) | Bytes | LastWrite (UTC) anchor |
|---|---|---|
| `ict_1m_execution_DRAFT.pine` | 22182 | 2026-06-18T18:42:43Z |

> **TZ note (`platform-display-tz-edt` trap):** the anchor above is the authoritative **PowerShell `LastWriteTimeUtc`** (`18:42:43Z`). A Bash `ls -la` renders the same file in local ET (UTC-4) as `14:42:43` — do NOT record the Bash value as the UTC anchor. The **byte count (22182)** is the TZ-independent identity anchor.

Read verbatim (full contents, with line numbers) in session 2026-06-18. **The campaign's §0 line citations point at the pre-patch `ict_1m_execution.pine` (18163 B); this PREREG cites the DRAFT (22182 B, killzone folded in) — line numbers below are DRAFT lines and supersede the pre-patch refs for the 1M layer.** Re-anchor command (PowerShell UTC):
`Get-ChildItem 'C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine' | Select Name,@{n='UTC';e={$_.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')}},Length`
If LastWriteUTC != 2026-06-18T18:42:43Z (or bytes != 22182) -> RE-READ before trusting any line citation here.

Frozen-config values below are sourced from these DRAFT lines: 25, 26, 33, 35-41, 45, 67-75, 78, 80-81, 82, 83, 85, 87, 89, 90, 92, 129-133, 228, 260, 344-350.

---

## Test object — frozen configuration (zero touches permitted)

Object under test: **post-cost E[R] per closed trade**, R-denominated, off TV's **List-of-Trades** export (entry / exit / PnL / MAE-MFE excursions). **NEVER $ off `strategy.equity`** — it compounds and `pointVal=1.0` (line 85) mis-scales index notional (1M-E3/E4). Any $/DD criterion uses the **static-$200K recompute** (strip compounding; evaluate $/DD on the static series).

| Rule | Value | Status | Source (`ict_1m_execution_DRAFT.pine`) |
|---|---|---|---|
| Strategy commission | `commission_value = 0.002` (=0.002%/side) | LOCKED | L25 |
| Strategy slippage | `slippage = 1` tick | LOCKED | L26 |
| FVG basis variant | `useBody` default `false` (wick) | **TWO frozen configs: wick AND body** | L33 |
| Swing strength (raid pools) | `pvLen = 2` | LOCKED (gate-bearing; PREREG-pvLen) | L35-41 |
| Raid -> entry window | `raidWin = 8` bars | LOCKED | L45 |
| DOL target mode | `dolMode = "range-extreme"` | **gate-bearing (LOCKED for verdict)** | L80-81, L223/L255 |
| DOL target mode (alt) | `nearest-pool` | **REPORT-ONLY** (not in lock decision; consumes no K/perm budget) | L80-81 |
| Use DOL target | `useDOL = true` | LOCKED (vs fixed-R is §7.B step 5, comparative not gate) | L78 |
| Risk % equity / trade | `riskPct = 0.5%` | LOCKED (R-invariant; $-only) | L83 |
| Point value | `pointVal = 1.0` | REPORT-ONLY (1M-E3; breaks $/DD, NOT the R-claim) | L85 |
| Commission (cost-law) | `commPct = 0.00002` | LOCKED | L87 |
| Slippage (cost-law) | `slipTk = 1` tick | LOCKED | L89 |
| Target clears hurdle by | `minRmult = 4.0` | LOCKED — **in-code ARM-TIME GEOMETRY filter** (`targetR >= minRmult*hurdleR`, per-trade target distance vs per-trade `hurdleR`); distinct from the verdict-gate 4x below | L90, L230/L262 |
| Min absolute target R | `minAbsR = 2.0` | LOCKED (n-throttle — report n-per-cell) | L92 |
| Killzone gate (arm) | `useKillzone` (ablated); London `0200-0500` + NY-AM `0700-1000` ON, NY-PM `1330-1600` OFF; ET via `America/New_York` (DST-safe) | FROZEN zone set + windows (NOT swept); PREREG-killzone | L67-75, L129-133 |
| Cost-law (per trade) | `hurdleR = (2*commPct*entryEst + 2*slipTk*mintick) / stopDist` | LOCKED (geometry, not outcome) | L228 (long) / L260 (short) |
| Tradeability floor (ledger F8) | drop trades with `stop_dist < max(1pt, cost)` | LOCKED — runtime filter; REPORT count dropped | TEST_PLAN §7.A B0 / ledger F8 |
| Data-window exports relied on | `netBias, zone, inKZ, eq_1h, hurdleR, raidSellPx, raidBuyPx` | LOCKED (the offline-reconstruction basis) | L344-350 |

**Cost hurdle (FROZEN).** `cost_R` per trade = `(2*commPct*entryEst + 2*slipTk*mintick)/stopDist` with `commPct=0.00002`, `slipTk=1` (units verified to agree: `commission_value=0.002`% = `commPct=0.00002` fraction; `slippage=1` tick = `slipTk=1` — §7.B 1M step 2, pin with comment so a future edit can't desync). **HURDLE = 4 x median(cost_R) on the tradeable population** (the post-floor population). cost_R is geometry, not an outcome — it is computed before any outcome is read.

**Two distinct uses of "4x" — do not conflate.** (a) The **in-code `minRmult = 4.0`** (DRAFT L230/L262) is an **arm-time geometry filter**: a trade is only placed if its own `targetR >= 4 * its own hurdleR` — a per-trade admissibility test on target distance. (b) The **verdict-gate 4x** (below) is on the **population E[R] CI lower bound vs 4 x median(cost_R)** — an outcome test on realized expectancy. Same multiple, different objects (per-trade target distance vs population expectancy), different hurdle bases (per-trade `hurdleR` vs `median(cost_R)`). The arm filter does NOT pre-satisfy the verdict gate; both must hold.

**Static-$200K recompute (FROZEN).** Strip `strategy.equity` compounding; per-trade %xstatic-$200K BEFORE evaluating any $/DD delta. The headline currency is **R**; the $/DD series is REPORT-ONLY and never the verdict.

## Resampling unit — block correction (frozen)

**Block-resample by ENTRY EVENT** (one draw per arming raid / FVG entry), NOT iid by trade-row — the 1M layer is the **same ICT-geometry family as the FALSIFIED D2** (`Q-ICT-SWEEPFVG-1`, US500 15m, falsified 2026-06-17 on §6 robustness), so F8's pseudo-replication dissent binds: the iid bootstrap understates SE and is **not** the verdict instrument. CIs and the DOW/session permutation resample by entry-event block. The window **MUST be genuinely multi-regime** (TEST_PLAN §7.A B0 dissent) — a single benign window reproduces D2's drop-top-k-carried, thirds-back-loaded failure; **drop-top-k concentration check is mandatory, not optional.**

## Power disclosure (read before judging the verdict)

Per-trade sigma in R is expected ~1.0-1.2R. At the n-floor (n=100), SE ~= +-0.10R to +-0.12R (iid, optimistic); after de-overlap to entry-event blocks the effective N is lower and SE wider. **Conventional significance is likely unreachable** at this n. Decision rules below are **expectation/CI-based, not significance tests**: the gate reads CI lower bounds against a fixed hurdle, not a p<0.05 on E[R]. A PASS **upgrades credibility and routes to forward / out-of-regime confirmation (independent price path / period / instrument) — it does NOT lock or deploy.** The direction/slice permutation kills random-labeling only; path-overfit stays alive after any permutation (Appendix D seed).

**n-floor (mandatory power gate).** **n < 100 closed trades after the starvation fix (B4) -> `INSUFFICIENT-N`** — the verdict is **unfalsifiable on this data; HALT** and re-spec the DOL target / window before any further verdict. Below 100 the E[R] CI is too wide to separate a null from a true edge; ambiguity there is indistinguishable from a starved null (this is the difference between `INSUFFICIENT-N` and a `FALSIFIED` decision).

## Verdict gate (binary)

Maps exactly to TEST_PLAN §6 row **1M**. E[R] is post-cost, R-denominated, block-resampled by entry event, on the gate-bearing config (`dolMode=range-extreme`); evaluated separately for each frozen variant (`useBody` true and false).

| Verdict | Trigger |
|---|---|
| `RESOLVED` (-> forward, not deploy) | E[R] block-CI **lower bound > 4 x median(cost_R)** (= `minRmult x median-hurdle`) **at n >= 100** · AND each **retained** gate (bias / PD / killzone) shows **positive marginal E[R] with CI excluding 0** in the 2^3 ablation (earns its place, not merely prunes n) · AND **no single DOW slice AND no single arm-time killzone slice carries the edge beyond the entry-event permutation null** · AND drop-top-k concentration check holds (edge survives removing the top-k entry-event blocks) |
| `FALSIFIED` | ANY: E[R] CI **subset of (-inf, hurdle]** (CI lower <= 4x median-hurdle) · OR **both gates add nothing** (no retained gate's marginal-E[R] CI excludes 0) · OR the edge **lives in one slice** (one DOW or one arm-time killzone slice beyond the permutation null) · OR drop-top-k removes the edge |
| `AMBIGUOUS-HOLD` / `INSUFFICIENT-N` | **n < 100 after the B4 starvation fix** -> `INSUFFICIENT-N` (claim unfalsifiable on this data; re-spec the DOL target, re-test on an independent multi-regime window) |

**Pre-registered before any data touches analysis.** Amending this gate mid-campaign to match emerging evidence is methodology-layer p-hacking — close AMBIGUOUS, capture why, open fresh.

## Forbidden (during the verdict window) — the moves that bite THIS layer (TEST_PLAN §5)

1. **Any $-denominated metric off the raw TV print.** `strategy.equity` compounds and `pointVal=1.0` mis-scales index notional; headline is R, $/DD only off the static-$200K recompute. (The single most tempting shortcut — the TV table prints net profit in $ right there.)
2. **Treating the default-config run as evidence about the ablation arms.** The double-raid short-bias defect (LIB-5/1M-E6) is dormant in the default and lives only in a gates-off arm; "the default passed" is false reassurance. Audit the arm-specific path (all 8 runs), not just the default.
3. **Outcome-conditional tuning.** Specifically: dropping the no-draw skips and *then* measuring E[R]; or picking `eqBand` / `minAbsR` to fatten n and *then* reading the rate on that fattened n. n-throttle knobs (`minAbsR`, `eqBand`, `useDOL`) must **report n-per-cell** so an n-driven "win" is visible.
4. **A single benign window.** The 1M layer is the D2 family; a benign-only window reproduces D2's drop-top-k-carried failure. The window must be genuinely multi-regime and the drop-top-k check must run.
5. **Letting `nearest-pool` enter the lock decision.** `dolMode=nearest-pool` is REPORT-ONLY: it does not enter the verdict and consumes **no** best-of-K / permutation budget (closes the dolMode selection-leak).
6. **Reading the on-chart table (winRate / pf / netprofit / fillRate) as the verdict.** Those are live, autocorrelated, and $-denominated; the verdict is the de-overlapped, entry-event-block, R-denominated offline estimate only.
7. **Sweeping any parameter before the selection-level tests run** (variant split, ablation, permutation, drop-top-k). Plateaus last, DSR/PBO-budgeted (§8.5).

## Audit hook

Reviewer question at verdict time: *"Was any criterion above moved, reinterpreted, or supplemented after the outcome run — in particular: was the n-floor (100), the 4x-hurdle multiple, the entry-event block unit, the multi-regime window requirement, or the range-extreme-only lock relaxed after the trades arrived?"* Any **yes** -> the verdict is void and the pattern stays unresolved.

Runnable checks (the cheapest are the fastest falsifiers in the whole 1M layer):

```bash
# §0 re-anchor (source is outside the repo, gitignored) — must match the §0 table (PowerShell UTC; Bash ls shows local ET = UTC-4).
Get-ChildItem 'C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine' | Select Name,@{n='UTC';e={$_.LastWriteTimeUtc.ToString('yyyy-MM-ddTHH:mm:ssZ')}},Length
#   Expect 22182 bytes / 2026-06-18T18:42:43Z.

# Confirm the gitignore line that forced CITATION-CHAIN mode (expect a hit at line 75).
grep -n '\*\*/\*\.pine' .gitignore

# B4 starvation / n-floor (1M unfalsifiable check): on the FIRST 1M export, if
# skip:cost/R dominates and closedtrades < 100 under useDOL=true -> INSUFFICIENT-N.
# (Read the on-chart "closed trades" + "skip: cost/R" cells; verdict still uses the export.)

# Killzone gate present (faithfulness — must be a real time gate, not a comment):
grep -nE 'America/New_York|killzoneOK|useKillzone' 'C:\Users\joshu\Downloads\ict_1m_execution_DRAFT.pine'
#   Expect hits at the input block (L67-75) AND the logic block (L129-133). Zero logic hits => no gate.

# Cost-law unit equivalence (must stay true after any edit):
#   commission_value 0.002 == 0.002% == 0.00002 fraction == commPct ; slippage 1 tick == slipTk 1.
#   A future edit changing one side only desyncs the hurdle.
```

Assertion at run time: the gate-ablation matrix is **exactly 8 labeled List-of-Trades exports** (bias x PD x killzone, all on/off combos); a verdict claiming gate marginal-E[R] from fewer than 8 distinct exports is void.

---

## GENUINE PRE-REGISTRATION CHOICES (operator ratification required before run 1)

These are real choices, not mechanically forced by §6. They are **PROPOSED** until the operator commits this file. (Thresholds in the verdict gate above are forced by §6 and are NOT in this list.)

1. **DOL target under test = `range-extreme` (gate-bearing); `nearest-pool` = REPORT-ONLY.** Forced direction by §8 PREREG-dolMode, but the operator must affirm range-extreme is the target the R-claim is tested against (the claim's R depends entirely on this — Appendix B #2). If the operator wants nearest-pool in the lock decision, that is a different pre-registration.
2. **Two frozen variants: `useBody` true AND false** — both run, each gets its own post-cost E[R] + entry-event-block CI; neither is dropped after seeing which wins. (Forbidden move #3 is "keep what wins" without pre-committing both.)
3. **The multi-regime window itself.** **RATIFIED — BINDING SPEC (exact dates named at export):** the window MUST span BOTH documented regimes — the **2020-2023 chop** (the regime in which the D2-family geometry FAILED: drop-top-k-carried, thirds-back-loaded) **AND the 2023-2026 trend**. A window confined to either alone is a Forbidden #4 single-regime window and voids the verdict. Rationale (design-faithful): the F8/B0 dissent exists precisely because a benign window reproduces D2's failure mode; binding the span to the *documented* chop+trend split is the strongest faithful guard. The operator names the precise dates at export (data-availability dependent) and asserts the span covers both regimes.
4. **Entry-event block definition for the resample.** Proposed: one block per arming raid -> FVG entry (the "fvg_bar"-analogue). Operator confirms the block key before CIs run (switching iid<->block after outcomes is forbidden, sibling Forbidden #2).
5. **drop-top-k: the value of k. RATIFIED — SCALED: `k = ceil(0.06 x n_blocks)`.** Rationale (design-faithful): the D2 sibling's drop-top-3 was calibrated to ~48 FVG-blocks (~6% removed); at n>=100 entry-event blocks here a fixed k=3 would remove a *smaller fraction* and weaken the concentration check. Scaling k to hold the sibling's **~6% removal fraction** preserves the sibling's stringency at the larger block count — the faithful choice. This is exactly what `harness_1m.py` implements (`DROP_TOP_K_FRAC = 0.06`, `k = ceil(0.06 * n_blocks)`), so PREREG and harness agree.
6. **Permutation B (resample count)** and the slice partitions (DOW; arm-time killzone). Proposed B >= 5000 block-permutations; partitions = 5 DOW x {London, NY-AM, NY-PM, out} arm-time. Operator pins B and the slice set.
7. **Tradeability-floor unit.** §7.A/F8 fixes `stop_dist < max(1pt, cost)`; operator confirms "1pt" is the correct minimum tick-distance for the SPX-class instrument under test (the sibling dropped 1 sub-spread setup at this floor — report the count here too).

Path-independence note: any PASS routes to confirmation on an **independent price path / period / instrument** (never "a different feed" — a re-export of the same path is not independence). Unpark / deploy is explicitly **out of scope** for this PREREG; the gate's RESOLVED verdict is "forward, not deploy."

---

## Amendment log (append-only)

- **2026-06-18 — RATIFIED (operator-delegated; criterion: most faithful to the design).** Genuine choices LOCKED. Confirmed at proposed values: range-extreme = gate-bearing / nearest-pool REPORT-ONLY (the design's own D1(a)); both `useBody` variants frozen (no post-hoc "keep what wins"); entry-event block unit; permutation B>=5000 over DOW x {London,NY-AM,NY-PM,out} arm-time; tradeability floor **1pt** (the SPX-class minimum, max(1pt,cost) per ledger F8). **Two design-faithful refinements vs the proposed defaults:** (a) **drop-top-k SCALED** to `ceil(0.06 x n_blocks)` (holds the D2 sibling's ~6% removal fraction at n>=100 — stronger + matches `harness_1m.py`); (b) **multi-regime window = BINDING SPEC** — must span the documented 2020-2023 chop AND 2023-2026 trend (exact dates named at export). Pre-data: no criterion may move after run 1; n<100 -> INSUFFICIENT-N/HALT. Firewall lifts on this file's commit.
