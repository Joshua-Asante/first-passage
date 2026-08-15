# `Q-ICTSTOP-1` — ICT chain stop-lever space-kill (order-free counterfactual)

**Status:** `RUN — NOT-KILLED (X4).` K=0, $0, no manifest, Cap seat untouched.
See [`RESULTS_STOP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_STOP.md).
**Class:** **order-free, zero-run, zero-K** measurement — ORB §2a excursion-bounded stop
space-kill shape, applied to the already-measured [`Q-ICTEXP-1`](Q-ICTEXP-1-ict-chain-gross-expectancy-scoping.md)
filled population.
**Purpose:** discharge [`RESULTS_EXP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md) §6.1's
open scope limit (the stop is the one untested lever) **without** inventing the lost Pine
stop-placement rule and **without** spending the MNQ Cap seat.
**Occasioned by:** ICTEXP landed `AMBIGUOUS` at the null end (T2 −1.039 pt, CI straddles 0,
n=32,355); reason 3 of the `Q-ICT-1MEXEC-1` NO-GO is measured; the stop residual is what keeps
the full frozen construct from being closed.
**Loop of record:** STRATEGIC (pre-Stage-0 falsifier completion). **Authored:** 2026-08-06 ·
Cursor (Composer), operator-directed via ratified plan
`ictexp_stop_counterfactual` (*"Implement the plan as specified"*).
**Parent:** `Q-ICTEXP-1` (RESULTS §6.1 scope limit).

---

## §0 — Rule-0 reads (verified this session 2026-08-06)

- **[`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_EXP.md) @ `d627a53`**
  — T2 −1.039 pt, CI [−3.589, +1.444], n=32,355; decomposition 26.1% / +97.9 vs 73.9% / −36.0;
  §6.1: stop is the one untested lever; inventing it was named K-bound. **This probe's job is
  the free alternative:** kill the *space* of stops without reconstructing the rule.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/PREREG_EXP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/PREREG_EXP.md) @ `30c79c9`**
  — stop-free redesign; FM-4 forbids inventing a stop; BAR = 5.640 pt; day-block bootstrap;
  no GO state. Constants and population contract inherited verbatim.
- **[`lab/analysis/_inbox/ict_mnq_2026-08/run_exp.py`](../../../lab/analysis/_inbox/ict_mnq_2026-08/run_exp.py) @ `d627a53`**
  — event builder: fill at FVG mid / `retraceK=6`, DOL `range-extreme` / `lookN=60`, E1 16:00 ET,
  MFE + signed T2. **MAE not computed today** — this probe adds it. `pair_fvgs_to_raids` returns
  FVG dicts only (boolean pair) — this probe enriches raid extreme price for `raid_dist`.
- **[`lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_tv_export_realism.md) @ `92abdbb`**
  — §2a tighter-stop counterfactual: stop at `f×OR-range` fires iff `AE_R ≥ f`; every tighter
  stop loses; classed **zero-run, zero-K**. Method template for this probe.
- **[`lab/archive/ict_cascade_2026-06-18/PREREG-1M.md`](../../../lab/archive/ict_cascade_2026-06-18/PREREG-1M.md) @ `47cc3eb`**
  — stop-placement still **absent in prose**; `stopDist` only inside `hurdleR` / tradeability;
  export columns `raidSellPx` / `raidBuyPx` suggest a raid-extreme *scale*, not a transcribed
  rule. Using raid distance as the ORB-analogue scale (not as *the* locked stop) is the honest
  reading.
- **[`docs/briefs/rnd-pipeline/Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md`](Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md) @ `ef43913`**
  — Stage-0C STOP on treating 1m mid-retrace expectancy as an untested residual. **This probe
  does not reopen that residual**; it closes ICTEXP's own declared scope limit only.

**Cheap falsifier (pre-authoring):** ICTEXP already measured n=32,355 on native MNQ 1m — no
power problem; this is a re-cut of that population, not a new panel or vendor class.
**Data:** same `MNQ.v.0` continuous 1m, regenerable at $0.0000.

---

## §1 — Context: what this probe completes

`Q-ICTEXP-1` answered expectancy under maximally generous **stop-free** assumptions and landed
at the null end of `AMBIGUOUS`. RESULTS §6.1 left one door open: a real stop truncates the
−36 pt bleed leg and could move T2 either way (it also exits winners that dipped). Closing that
door by **reconstructing** the lost Pine stop would violate ICTEXP FM-4 and is the K-bound path
RESULTS named.

The free path is the ORB path: ask whether **any** stop width on a construct-native scale can
lift mean signed expectancy's block-CI above the frozen **5.640 pt** bar. If the whole space
fails, the lever is dead without inventing a rule. If some width clears, the outcome is only
`NOT-KILLED` — licenses a future K-bound pre-registration, never GO.

---

## §2 — Design: MAE space-kill on the frozen ICTEXP population

**Population:** identical to ICTEXP T2 fills (FVG mid touch within `retraceK=6`, `noDraw`,
DOL `range-extreme`, E1 window). Stop-free T2 signed remains the no-stop baseline.

**Per-event geometry:**

1. **MAE** from fill over the holding window to the natural T2 exit (target touch bar, else E1):
   long `fill − min(low)`; short `max(high) − fill`.
2. **`raid_dist`:** |fill − paired raid extreme|. Bull (SSL raid) → raid low; bear (BSL) →
   raid high. Enrich pairing to attach swept pool price. Scale `s = f × raid_dist`. Drop /
   report non-positive `raid_dist` (no invented floor).
3. **Counterfactual at f:** if `MAE ≥ s` → exit **−s**; else keep T2 signed. Path-order-free
   for stop firing (ORB §2a). Same-bar / dual-reach: **E_best** credits target when target was
   touched despite `MAE ≥ s`; **E_worst** credits **−s**. Kill requires failure under E_best.

**Frozen f-grid (pre-data):** `{0.5, 0.75, 1.0, 1.25, 1.5, 2.0}` — isomorphism to ORB's
`f×OR-range`; **not** an absolute-points grid.

**Bar / CI:** mean signed **points**, day-block bootstrap `B=2000`, seed **`20260806`**
(distinct from ICTEXP's `20260804`), vs **5.640 pt**. Stay in points — do not reintroduce R /
`stopDist` into the verdict.

**Disclosure (never verdict):** MAE quartiles of target-hit vs bleed legs — mechanism check
("do winners sit through deep drawdown?").

**Generosity:** E_best is the optimistic limb for the kill; bar-level touch; no gap-through;
same ICTEXP fill generosity.

---

## §3 — Question

**Can any raid-scaled stop width rescue the ICT raid→FVG→DOL chain's mean signed expectancy
above 4× round-trip cost on the already-measured native MNQ 1m population — or is the stop
lever dead as a space, independently of reconstructing the lost Pine rule?**

Symptom only: the stop was never tested; the chain's stop-free expectancy is null. No
execution design, no Pine reconstruction, no deploy limb.

---

## §4 — Falsifiable hypothesis

**H-ICTSTOP-1.** On the ICTEXP filled population with positive `raid_dist`, **every** f in the
frozen grid has E_best mean-signed block-CI **upper** bound **below** 5.640 pt (n ≥ 100 after
the raid_dist filter).

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| X1 | n after raid_dist filter | **< 100** | **`INSUFFICIENT-N`** — lever untestable this way; seat untouched |
| X2 | For **every** f, E_best CI **upper** | **< 5.640 pt** | **`FALSIFIED`** (space-kill) — stop lever cannot rescue ICTEXP |
| X3 | Best f clears CI upper; **no** f has CI **lower** ≥ 5.640 | — | **`AMBIGUOUS`** — not harvestable at the bar; NO-GO stands |
| X4 | Some f has CI **lower** ≥ 5.640 under E_best | — | **`NOT-KILLED`** — **licenses nothing**; any real stop rule needs a new K-bound prereg |

---

## §5 — Forbidden moves

- **FM-1 — Reading `NOT-KILLED` (X4) as GO**, as reachability discharge, or as license to
  reconstruct the Pine stop without a fresh K-bound pre-registration.
- **FM-2 — Inventing *the* locked stop** (raid extreme = the rule, ATR stop, fixed points as
  verdict axis). Raid distance is a **scale**, not a reconstructed constant (ICTEXP FM-4).
- **FM-3 — Post-hoc f densification** or switching scale to ATR / absolute points after seeing
  results.
- **FM-4 — Any grid on entry / DOL / `retraceK` / `pvLen` / holding window.** One frozen
  population, one f-sweep.
- **FM-5 — Reopening Q-ICTNF near-field OHLCV** under cover of this probe.
- **FM-6 — Any `core/`, lock, rail, Pine, K-ledger, manifest, or `lab/archive/` edit.**

---

## §6 — Gate criteria (binary)

| Canonical verdict | Trigger | Consequence for `Q-ICT-1MEXEC-1` |
|---|---|---|
| `INSUFFICIENT-N` | X1 | NO-GO stands; method failed, not the lever |
| `FALSIFIED` | X2 | NO-GO permanent on expectancy **including** the stop residual; seat preserved |
| `AMBIGUOUS` | X3 | NO-GO stands (same reading as ICTEXP X3) |
| `RESOLVED` / local `NOT-KILLED` | X4 | NO-GO stands on reasons 1/2/4; only "stop could never help" is removed |

**No outcome promotes anything. The probe has no GO state.**

Disposition map (ADR 2026-08-04 iterate-closure): X2 → `STOP`; X3 → `STOP` (NO-GO stands);
X4 → `ITERATE` only as "K-bound stop-reconstruction prereg if operator elects"; X1 → `ITERATE`
(method).

---

## §7 — Execution plan (one session after freeze)

1. Operator K-freeness: **affirmed by plan ratification** (*Implement the plan as specified*,
   plan locks K=0) — same class discharge as ICTEXP §9's one-liner.
2. Freeze `PREREG_STOP.md` in `lab/analysis/_inbox/ict_mnq_2026-08/` **before** any stop-counterfactual
   number on real bars.
3. Hand-computed unit tests (MAE, raid_dist orientation, f-PnL, E_best/E_worst) **before**
   touching the panel.
4. Extend pairing + runner; run on MNQ 1m ($0); write `RESULTS_STOP.md`; update MNQ ledger /
   STATE pointer.

**Estimated marginal cost: $0.00 data, 0 K, no manifest, Cap seat untouched.**

---

## §9 — Governance: why this is K-free

Identical structural case to ICTEXP §9 and ORB N3: one-way falsifier, no GO state, zero free
parameters on the entry/DOL side, f-grid is space characterization (kill if *all* fail) not
candidate generation. X4 explicitly forbids promotion. Operator affirmation: plan
implementation directive 2026-08-06.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering: PREREG_STOP commit precedes RESULTS_STOP
git log --format='%h %cs %s' -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_STOP.md | Select-Object -Last 1
git log --format='%h %cs %s' -- lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_STOP.md | Select-Object -Last 1

# No K / no ICTSTOP manifest
Get-ChildItem discovery_manifests | Select-String -Pattern 'ict|stop'

# Archive detectors byte-identical
git --no-pager diff HEAD -- lab/archive/ict_cascade_2026-06-18/

# Stop still absent in prose
Select-String -Path lab/archive/ict_cascade_2026-06-18/PREREG-1M.md -Pattern 'stopDist'

# Bar still 5.640
python -c "print('rt=%.3f bar=%.3f' % (2*0.91/2.00 + 2*1*0.25, 4*(2*0.91/2.00 + 2*1*0.25)))"
```

---

## Amendment log (append-only)

- **2026-08-06 — SCOPED.** Space-kill design locked from plan `ictexp_stop_counterfactual`.
  K=0 affirmed by operator plan-implementation directive. Not run, no PREREG yet at this
  amendment's authorship instant — PREREG follows in the same session after this file lands.
- **2026-08-06b — RUN → `NOT-KILLED` (X4).** PREREG frozen `30a89a0` pre-measurement.
  n=30,156; every f clears E_best CI lower vs 5.640; E_worst means ~0.4–1.0 pt. Licenses
  nothing. Cap seat untouched. [`RESULTS_STOP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_STOP.md).
