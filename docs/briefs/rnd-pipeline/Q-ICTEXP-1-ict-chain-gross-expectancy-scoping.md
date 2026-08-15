# `Q-ICTEXP-1` — ICT raid→FVG chain gross-expectancy ceiling probe (scoping)

**Status:** `SCOPED — not run, not pre-registered, no K bound, no manifest, $0 committed.`
**Class:** **order-free, zero-run, zero-K** measurement — the same class as
[`ORB-MNQ-1`'s excursion-bounded exit kill tests](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md)
(*"Class: zero-run, zero-K measurements (strategy-validation §3 excursion-bounded
counterfactual + fill-realism audit). No construct change proposed; no re-run consumed."*),
which the MNQ ledger banks at **K=0** (finding **N3**).
**Purpose:** decide `Q-ICT-1MEXEC-1` **without** spending the last MNQ K seat — by testing
whether the chain has *any* harvestable gross edge before anyone pays for a validation.
**Occasioned by:** the [`Q-ICT-1MEXEC-1` draft pre-registration](../pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md)
§8, whose recommended disposition is **NO-GO**, and whose reason 3 ("there is no edge
hypothesis, only a removed objection") is the *only* one of its four NO-GO reasons that
evidence can actually move.
**Loop of record:** STRATEGIC (pre-Stage-0 falsifier). **Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

---

## §0 — Rule-0 reads (verified this session 2026-08-04)

- **[`lab/archive/ict_cascade_2026-06-18/PREREG-1M.md`](../../../lab/archive/ict_cascade_2026-06-18/PREREG-1M.md) @ `47cc3eb`** — read in full. **The load-bearing §0 finding of this scope:** the 1M **exit geometry is transcribed in prose**, not merely line-cited to the lost Pine. `dolMode = "range-extreme"` (gate-bearing, LOCKED; `nearest-pool` is REPORT-ONLY) L41-42; `useDOL = true` L43; the arm-time filter `targetR >= minRmult * hurdleR` with `minRmult = 4.0` L48; `minAbsR = 2.0` L49; the cost formula `hurdleR = (2*commPct*entryEst + 2*slipTk*mintick) / stopDist` L51/L55; tradeability floor `stop_dist >= max(1pt, cost)` L52; n-floor **100 closed trades → `INSUFFICIENT-N`** L69. ⚠ **CORRECTED 2026-08-04, before any measurement — this bullet originally claimed "every constant this probe needs survives the `.pine` loss." That is WRONG and the error is mine.** An exhaustive search (`grep -rn "stopDist|stop_dist|stopPx"` across the archive `.md` set, plus a corpus-wide hunt for any prose stop rule) confirms **the stop-placement rule is NOT transcribed anywhere** — `stopDist` appears only as a *variable inside* the `hurdleR` and tradeability-floor formulas, never as a definition. It is line-cited to the lost Pine only, exactly like `netBias`. **What IS transcribed and verified:** the DOL target (`range-extreme` ⇒ LONG `h1High` / SHORT `h1Low`, where those are `ta.highest(high,60)[1]` / `ta.lowest(low,60)[1]` on 1H, non-repaint — B2_B3_CHANGES.md L90-97 + PREREG-1H L32/L45 `lookN=60` LOCKED), the `noDraw` skip rule, `minRmult`, `minAbsR`, the `hurdleR` formula and its constants, and the entry (limit at FVG mid, `retraceK=6`). **Consequence — the probe is still buildable, and the fix makes its conclusive limb stronger:** §2 is re-specified **stop-free**, so no unreconstructable constant enters any verdict. See `PREREG_EXP.md` §1.
- **`PREREG-1M.md` L57 — the two-`4×` trap, carried into §3 below.** (a) `minRmult=4.0` is an **arm-time geometry** filter (per-trade target distance vs that trade's own `hurdleR`); (b) the **verdict-gate 4×** is on **population E[R] CI lower bound vs 4 × median(cost_R)**. *"The arm filter does NOT pre-satisfy the verdict gate; both must hold."* Same multiple, different objects. Conflating them would silently pre-pass the probe.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py`](../../../lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py) @ `9aaa578`** — the chain reconstruction this probe extends: heap-based raid scan (`pvLen=2`, `raidWin=8`) → same-direction displacement FVG pairing, **42 unit tests** incl. a flag-equivalence pin against the archived `detect_raid` semantics. Confirmed passing this session. **Part C explicitly OMITTED the DOL/stop geometry filters** (declared ≤~5% population trim) — that omission is precisely what this probe adds back.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md) @ `9aaa578`** — §4 scope limit, binding here: *"Nothing here measures edge. Fill mechanics only; no P&L was computed anywhere in Part C."* This probe is the first P&L ever computed on this chain.
- **[`lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md) @ `92abdbb`** — the zero-K precedent and the method template: an excursion-bounded counterfactual pre-killed **both** ORB exit-redesign directions with **zero runs** (tighter stops lose 0.03–0.06R; no fixed target beats baseline even resolving all ambiguous buckets favourably, `E_best` max +0.088 vs +0.099). Banked **K=0**.
- **[`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) @ `71ad728`** — **N6** modern MNQ cost hurdle **3.01 bp/session**; **N3** the zero-K excursion precedent; **N10** (added this session) the K-band arithmetic that makes this probe worth running at all; **W4** micro-era proxy discipline (re-parameterize fills on native micro data — satisfied by construction, this is native MNQ).
- **[`docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md`](../pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md) @ `71ad728`** — §2 (the reachability screen this probe cannot discharge), §2.4 (the four non-arguments), §5 FM-1 (any conditioning gate lifts `K_eff` to 4 and closes the band).
- **[`docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md`](../../notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md) @ `6d9e603`** — the free-category ruling. Its distinguishing feature is **"carries no deploy target"**; §9 below states honestly why this probe is a harder case than Parts B/C and proposes the resolution rather than assuming it.

**Data:** `MNQ.v.0` continuous 1m, databento GLBX.MDP3, 2019-05-06 → present, **2,552,025
bars**, pulled twice at **$0.0000** and regenerable at that price. No new data class, no new
vendor, no procurement decision.

---

## §1 — Context: what this probe is for, and the one NO-GO reason it can move

The `Q-ICT-1MEXEC-1` draft recommends NO-GO on four independent grounds:

| # | NO-GO reason | Can this probe move it? |
|---|---|---|
| 1 | `K_eff=3` → annSR floor **0.980** vs Cap **1.0**; a 0.020-wide band whose floor sits above `ORB-MNQ-1`'s +0.890/+0.835 | **No** — arithmetic, not evidence |
| 2 | Opening it takes `K_banked` 2→3, so the *next* MNQ seed hits `K_eff=4` → floor 1.060 > Cap. **Spending the seat forecloses MNQ discovery permanently** | **No** — structural |
| 3 | **No edge hypothesis exists** — Part C removed an objection, not a reason to expect money. W/D are structural and route away from deploy; 1H is FALSIFIED so the construct runs gate-free; the family's record is uniformly negative | **YES — this is the one** |
| 4 | ADR 2026-07-12 §4 cl.4 is directive: a campaign disclosing a minimum above its plausible-edge ceiling *"must not freeze as written"* | **No** — rule, not evidence |

So the probe's honest job is **asymmetric**: it can *kill* reason 3's counterfactual (there is
no edge, stop asking), or it can *fail to kill* it (leaving reasons 1, 2 and 4 completely
intact). **It cannot produce a GO.** That asymmetry is not a limitation to be worked around —
per §9 it is the design property that keeps the probe K-free, and per §5 it is the thing most
likely to be laundered later.

**Why it is worth running anyway.** Reason 3 is the only one that would keep resurfacing.
Reasons 1/2/4 are stable facts a future session will re-derive identically; reason 3 is an
*absence of evidence*, and absences invite re-litigation every time someone notices the fill
wall is gone. A conclusive kill closes the ICT line permanently at $0. A non-kill costs $0 and
changes nothing — which is itself worth knowing before the seat is ever discussed again.

---

## §2 — Design: three tiers, all order-free

Every tier runs off one pass over the native 1m panel. No orders are simulated; no fill model
beyond a bar-level touch at the FVG mid (the semantics already built and unit-tested in Part B/C).

**T0 — population, with the filters Part C omitted.** Re-run the Part C chain
(`pvLen=2` raid → `raidWin=8` same-direction pairing → displacement FVG at `dispMlt=1.5×ATR`,
`atrLen=14`), now applying the PREREG-1M **arm-time geometry**: `targetR >= 4.0 × hurdleR`,
`minAbsR = 2.0`, tradeability floor `stop_dist >= max(1pt, cost)`, `dolMode = range-extreme`.
Report `n` armed, and the count dropped at each filter. **Roll exclusion** (±4 days of
3rd-Friday Mar/Jun/Sep/Dec) applies at object origin, inherited from `PREREG_D_W.md` §2.

**T1 — perfect-foresight ceiling. This is the conclusive limb.** For each armed event, exit at
the **maximum favorable excursion** inside the holding window — i.e. grant the strategy a
perfect exit it could never achieve live. Zero free parameters on the exit side, so nothing is
searched and nothing is selected. This is an **absolute upper bound that no exit design, target
choice, trailing rule, or fill improvement can beat.** Compare `E[R]` (entry-event block CI) to
**4 × median(cost_R)** at the **Tradeify $0.91/side** basis — the live account, per the draft
pre-registration §3 and the `ORB-MNQ-1` Stage-7 rider that showed basis-specificity is real.

**T2 — the frozen geometry, for the honest number.** The actual `range-extreme` DOL target and
stop, same cost basis, same CI method. T2 ≤ T1 by construction.

**Generosity ledger — every assumption biases expectancy UP, and that is deliberate:**

- fill at the FVG mid on any bar-level touch — no queue position, no partial, no adverse selection
- zero entry slippage (T1/T2 gross; commission enters only through the `cost_R` comparison)
- stops fill exactly at the stop — no gap-through
- T1 additionally grants **perfect exit foresight**
- the `retraceK=6` arming window is applied at its most permissive measured cell

**This is the SLR-MYM-1 L1 discipline** (*"design the cheap proxy to be generous, so a failure
is conclusive"*), which killed that campaign at $0 where a tight proxy would have been
inconclusive and forced a paid pull. A FAIL here is dispositive. A PASS says almost nothing.

---

## §3 — Question

**Does the ICT raid→FVG→DOL chain carry any harvestable gross expectancy on native MNQ 1-minute
data — or is the ICT 1M line dead on expectancy grounds, independently of fills and of K?**

The question names a symptom (the chain's expectancy has never been measured — *anywhere*, on
any instrument or timeframe, in the whole ICT record) rather than a fix. It does not presuppose
an execution design, a target mode, a gate stack, or a deployment. The symptom-only rephrase is
the question itself: **nobody knows whether this chain makes money, and no one has ever
checked.** Part C established that orders would *fill*; it computed no P&L. Every ICT verdict on
record — W, D, 1H, 1M, the 5M substitution, `pharos_us500_sweepfvg` — is about structure,
gating, or mechanics. Expectancy is the one axis never measured.

---

## §4 — Falsifiable hypothesis

**H-ICTEXP-1 (the hypothesis under test).** The ICT raid→FVG→DOL chain, measured on native MNQ
1m under maximally generous order-free assumptions, produces a **perfect-foresight-ceiling**
gross expectancy whose entry-event block-CI **upper** bound reaches **4 × median(cost_R)** at
the Tradeify basis, on a population of **n ≥ 100** armed events.

**Falsifier — frozen trigger/threshold table. If a row's trigger fires, then the stated verdict
follows and no later tier is read.**

| # | Trigger | Threshold | Verdict / action |
|---|---|---|---|
| X1 | `n` armed after T0 filters | **< 100** | **`INSUFFICIENT-N`** → the K-bound campaign would hit the identical PREREG-1M n-floor. NO-GO stands, recorded permanently. Stop. |
| X2 | T1 `E[R]` **CI upper** bound vs `4 × median(cost_R)` | **below** | **`CONCLUSIVE-KILL`.** Perfect foresight + perfect fills already granted, so no exit redesign or execution refinement can rescue it. `Q-ICT-1MEXEC-1` dies before opening; MNQ seat preserved. Stop. |
| X3 | T1 clears, T2 `E[R]` CI lower vs the same bar | **below** | **`UNHARVESTABLE`** — directional content exists, the frozen exit does not harvest it. Exactly the `ORB-MNQ-1` **N3** shape. **NO-GO stands** — changing the exit is a new parameter, i.e. K. |
| X4 | T1 and T2 both clear | — | **`NOT-KILLED`.** **Licenses nothing** (see §5 FM-1). NO-GO reasons 1, 2 and 4 are untouched; only reason 3's counterfactual is removed. |

Stated in one line: **if** the generous ceiling cannot reach the cost bar, **then** the ICT 1M
line is dead at $0 and the seat is saved; **if** it can, **then** we have learned only that the
cheapest kill did not fire.

---

## §5 — Forbidden moves

- **FM-1 — Reading `NOT-KILLED` (X4) as GO, as a reachability discharge, or as evidence the 0.980 floor is attainable.** This is the single highest-risk move in this document. A gross ceiling under perfect foresight is not a net annualized Sharpe, and the gap between them is exactly where every ICT result so far has died. X4 removes one of four NO-GO reasons; the arithmetic wall, the permanent-foreclosure cost, and the directive ADR clause all survive it untouched.
- **FM-2 — Any grid, sweep, variant, or "also try" on `pvLen`, `raidWin`, `dispMlt`, `atrLen`, `retraceK`, `minRmult`, `minAbsR`, or the roll window.** One frozen construct, one measurement. A grid is candidate generation and **consumes K**, which destroys the entire purpose of running this instead of `Q-ICT-1MEXEC-1`.
- **FM-3 — Switching `dolMode` to `nearest-pool` after seeing `range-extreme` fail.** PREREG-1M L41-42 fixes `range-extreme` as gate-bearing and `nearest-pool` as REPORT-ONLY. Switching post-result is textbook selection, and PREREG-1M L128 already requires a *different pre-registration* for that target.
- **FM-4 — Conflating the two `4×`s** (arm-time `minRmult` geometry filter vs the population-E[R] verdict gate). PREREG-1M L57 is explicit that the arm filter does not pre-satisfy the verdict gate. Conflating them silently pre-passes the probe.
- **FM-5 — Tuning any filter after seeing `n`.** If T0 returns `n < 100`, the verdict is `INSUFFICIENT-N` — not an invitation to loosen `minAbsR` or the tradeability floor to fatten the population. PREREG-1M's own §7.B step-2 n-throttle rule requires reporting n-per-cell precisely so an n-driven "win" is visible.
- **FM-6 — Letting this probe grow an execution or deploy limb.** It computes expectancy on historical bars. It arms nothing, proposes no Pine, and touches no rail. The c1 rail stays **disarmed** (`dry_run=true`); M1 is not `RESOLVED`.
- **FM-7 — Any `core/`, lock, allocation, `dd_protection`, Pine, `LEG_MAP`, K-ledger, or manifest change**, and no edit to `lab/archive/` (the byte-identity pin every ICT results doc uses as an audit hook must keep returning empty).

---

## §6 — Gate criteria (binary)

Verdicts use the repo's canonical vocabulary, so this probe's outcome is legible to the standard
closure machinery. The probe-local names in §4 are labels for the *reading*, not a second scheme.

| Canonical verdict | Trigger | Probe-local reading | Consequence for `Q-ICT-1MEXEC-1` |
|---|---|---|---|
| **`INSUFFICIENT-N`** | X1 — `n` < 100 after T0 filters | population starved | **NO-GO permanent.** The identical PREREG-1M n-floor would bind the paid campaign. |
| **`FALSIFIED`** | X2 — T1 ceiling CI upper below `4 × median(cost_R)` | conclusive kill | **NO-GO permanent.** ICT 1M line closed on expectancy; seat preserved; record as a DEAD entry in the MNQ ledger. |
| **`AMBIGUOUS`** | X3 — T1 clears, T2 below the bar | real but unharvestable | **NO-GO stands.** Record alongside `ORB-MNQ-1` **N3** as a second "real but unharvestable" instance. Changing the exit is a new parameter, i.e. K. |
| **`RESOLVED`** | X4 — T1 and T2 both clear | cheapest kill did not fire | **NO-GO stands on reasons 1, 2 and 4.** Reason 3 discharged; binding constraints unchanged. |

> ⚠ **`RESOLVED` on this probe does NOT mean "there is an edge" and does NOT mean GO.** It means
> exactly one thing: *a maximally generous gross ceiling reached a cost bar.* It is not a net
> figure, not annualized, not risk-adjusted, and not multiplicity-corrected. The distance from
> here to the **0.980 annSR at DSR ≥ 0.95** that `Q-ICT-1MEXEC-1` must clear is the entire
> distance every prior ICT result failed to travel. See §5 FM-1 — this row is the laundering
> surface of this document.

**No outcome of this probe promotes anything.** That is the point, and it is what §9 rests on.

---

## §7 — Execution plan (one session)

1. Freeze a short pre-registration (`PREREG_EXP.md`) in `lab/analysis/_inbox/ict_mnq_2026-08/` carrying §2's tier definitions, §4's table, and the cost basis — **committed before any R is computed**, per the same freeze-ordering Parts A–C used (git-auditable: freeze commit must precede results commit).
2. Extend `run_1m_diag.py`'s chain reconstruction with the T0 arm-time filters, MFE computation (T1), and the frozen DOL/stop geometry (T2). New unit tests hand-computed on a synthetic fixture **before** touching real bars, mirroring the 42-test discipline already in place.
3. Regenerate the MNQ 1m parquet ($0.00 — cost dry-run first, per the standing databento rule).
4. Run; write `RESULTS_EXP.md` with the generosity ledger restated and n-per-filter reported.
5. Route the verdict per §6. Update the MNQ ledger with a dated disposition either way.

**Estimated marginal cost: $0.00 data, 0 K, no manifest, no Cap seat.** The expensive part
(chain detection + the heap raid scan that replaced a multi-day naive loop) already exists and
is unit-tested.

---

## §9 — Governance: why this is K-free, stated as an argument rather than assumed

**The precedent is direct.** `ORB-MNQ-1`'s excursion-bounded exit kill tests are classed
in-repo as *"zero-run, zero-K measurements"* and banked at **K=0** (`MNQ.md` **N3**). This probe
is the same instrument on a different construct.

**The honest complication.** `CONFIRM-FREE-NODEPLOY-2026-08-03`'s distinguishing feature for
the free category is *"carries no deploy target."* This probe exists to inform a
deploy-adjacent decision, so it is a harder case than Parts B/C, and pretending otherwise would
be the K-laundering both `WSTRUCT-M2K-1` and `SLR-MYM-1` warn about.

**The proposed resolution — structural, not rhetorical.** What consumes promotion-K is a look
that *could* inflate a best-of-K promotion. This probe is **structurally incapable of
promoting**: its outcome set is `{INSUFFICIENT-N, CONCLUSIVE-KILL, UNHARVESTABLE, NOT-KILLED}`,
it has **no GO state**, it runs one frozen construct with zero free parameters, and FM-1
forecloses reading its best outcome as license. A one-way falsifier cannot manufacture a false
positive, so it does not consume the budget that exists to prevent one.

**This should be affirmed, not assumed.** `CONFIRM-FREE-NODEPLOY` was taken as an explicit
operator ruling precisely because this category boundary is contested and the K arithmetic makes
it consequential. **Recommended:** a one-line operator affirmation before step 1 — *"a one-way
falsifier with no GO state is K-free"* — cited in `PREREG_EXP.md` §0. If the operator would
rather the probe be able to return GO, then it must be K-bound, and at that point it **is**
`Q-ICT-1MEXEC-1` and should be run as that instead.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze-ordering must be git-auditable: the prereg commit precedes the results commit.
git log --format='%h %cs %s' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_EXP.md | tail -1
git log --format='%h %cs %s' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md | tail -1

# No K may be bound and no manifest opened by this probe (expect NO match, rc=1):
ls discovery_manifests/ | grep -iE "ict|exp"

# MNQ K bank must still read 2 after this probe closes (expect 1, then "2 operator-stopped"):
python -c "import json;print(json.load(open('discovery_manifests/d5_nq_intraday_mom.json'))['K'])"
python -c "import json;d=json.load(open('discovery_manifests/st_eh_supertrend_grid.json'));print(d['K'],d['closure_mode'])"

# The archived detectors must stay byte-identical -- this probe extends, never edits them:
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/

# The exit-geometry constants this probe depends on must still be prose-transcribed
# (expect hits for dolMode, minRmult, minAbsR -- if these vanish the probe is unbuildable):
grep -nE "dolMode|minRmult|minAbsR|hurdleR" lab/archive/ict_cascade_2026-06-18/PREREG-1M.md

# The zero-K precedent this scope leans on must still read as zero-K:
grep -n "zero-run, zero-K" lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md

# The NO-GO reasons this probe canNOT move must still stand in the draft prereg:
grep -nE "FAIL-AS-WRITTEN|0\.980|Cap" docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md | head
```

---

## Amendment log (append-only)

- **2026-08-04 — SCOPED.** Not run, not pre-registered, no K bound, no manifest, $0 committed.
  Authored in response to an operator instruction to scope the free expectancy probe named as
  the constructive alternative to a bare NO-GO on `Q-ICT-1MEXEC-1`. §9 flags the one governance
  call (K-freeness of a one-way falsifier) that wants an operator line before step 1.
- **2026-08-04b — OPERATOR AFFIRMED K-FREE** (*"run the probe, it's K-free"*), discharging §9.
- **2026-08-04c — §0 CORRECTED before any measurement (my error, caught at build time).** The
  original §0 claimed every needed constant survived the `.pine` loss. **The stop-placement rule
  does not** — it is line-cited only, like `netBias`. §2's tiers are consequently re-specified
  **stop-free** in the frozen `PREREG_EXP.md`: the ceiling limb becomes a max-favorable-excursion
  bound in **points** against a points-denominated cost bar, which removes `stopDist` from both
  sides of the comparison entirely. The R-denominated arm-time filters (`minRmult`, `minAbsR`,
  tradeability floor) are **NOT APPLIED** for the same reason, and their omission is *generous* —
  they only ever trim the population, which is the direction this probe's design already commits
  to. Net effect: the conclusive limb no longer depends on any unreconstructable constant, so it
  is **stronger** than as scoped, not weaker.
