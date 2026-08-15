# MSL-S2A — Explore GO draft

**Status:** `DRAFT` — promote = copy to gitignored `EXPLORE_GO.md` and stamp `ISSUED YYYY-MM-DD`.
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`STAGE1.md`](STAGE1.md)
**Harness:** [`run_construct_g0.py`](run_construct_g0.py) · [`construct_lib.py`](construct_lib.py)
**Cost / K at draft:** $0 · K=0. Scoring spends nothing until `--explore-go` after promote.

Operator instruction 2026-08-13: continue locally with explore GO → IS harness + delete/flip.

---

## Promote rule (operator)

1. Restore `core/data/bar_data/MCL_M15.csv` bytes matching
   `core/data/bar_data/SHA256SUMS` pin `5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23`.
2. `cp EXPLORE_GO.DRAFT.md EXPLORE_GO.md` and stamp `ISSUED <date>` on line 1.
3. Run: `python lab/analysis/c1/msl_s2a_mcl_2026-08/run_construct_g0.py --explore-go`
4. Do **not** author Pine / TV until explore gate is `SHAPE-CLEAR` (or operator kill).

---

## Partitions (frozen — identical to PREREG; no re-election)

| Partition | Window |
|---|---|
| **IS / EXPLORATION** | session dates **&lt; 2025-07-01** |
| **CONFIRM** | **2025-07-01 → 2026-07-02** inclusive — **RESERVED UNREAD** through step 8 |

Any CONFIRM peek voids the holdout. FOMC + roll-excluded sessions dropped on IS identically (PREREG §1 lists).

---

## Panel

- Path: `core/data/bar_data/MCL_M15.csv`
- Schema: `time,open,high,low,close,volume` (UTC `Z`); TZ interpret as America/New_York for session windows
- sha256 must match `SHA256SUMS` pin above; runner **REFUSE**s on mismatch / missing bytes

---

## Delete / flip (Req 1a) — frozen operationalization (IS-only)

Constraint under test: **impulse window + failed-pullback resumption** selects the trade.

### DELETE

Random in-session bar at **matched time-of-day**: for each constrained trade at minute `m`, pick a random *other* IS session’s bar at the same `m` (seed `20260813`); enter the **same side** with the P-window stop construction and **no** impulse/failure filter.

- Score arms separately on IS.
- **FAIL** if sham arm mean net R ≥ constrained arm mean net R on that arm.
- Either arm DELETE-FAIL ⇒ that arm is not SHAPE-CLEAR.

### FLIP

At the **same trigger bar**, join the pullback (opposite side of the resumption); stop/target distance symmetry preserved.

- Score: constrained-long vs flip-short; constrained-short vs flip-long.
- **FAIL** if flip mean net R ≥ constrained mean net R.
- Either arm FLIP-FAIL ⇒ that arm is not SHAPE-CLEAR.

---

## Primary / aux limbs (PREREG §4)

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap 95% CI |
| Halves | Older / newer IS session-date halves |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor; compared to daily annSR as in C2) |
| Cost-law | Gross/trade vs **$16.48** (4× RT $4.12) at realized stop distances |
| Placebo (aux) | Sign-randomized observed R; `PLACEBO_REPS=1000`; seed `20260813`; **not selection** |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at qty=2 · EM six-char · trades/week (N-ACT) |

### Gate vocabulary (explore)

- **FALSIFIED** — both arms CI upper bound &lt; 0 (n≥100), **or** measured trades/week &lt; 1 (N-ACT solo fail).
- **SHAPE-CLEAR** — ≥1 arm primary CI lo &gt; 0 **and** DELETE PASS **and** FLIP PASS **and** declared aux live-pass (placebo p_emp &lt; 0.05 ∧ annSR ≥ 0.650 ∧ halves agree).
- **AMBIGUOUS-HOLD** — otherwise (incl. primary pass with aux/delete/flip fail).
- **VOID** — coverage / panel / token refusal (no score).

CONFIRM unread. Cap not claimed. Pine unpaid until SHAPE-CLEAR + operator.

---

## Forbidden moves

- Path-scoring CONFIRM; any CONFIRM peek.
- Pine / TV / B5 without explore PASS + runbook links to steps 2–5.
- θ retune (impulse/pullback windows, stop buffer, TF, rr, k, session window) after seeing results — new G0.
- Instrument hop; using robustness sweeps for **selection**.
- Self-authorizing explore score without this token file present as `EXPLORE_GO.md`.

---

## Audit hooks

```text
test -f lab/analysis/c1/msl_s2a_mcl_2026-08/EXPLORE_GO.md
python lab/analysis/c1/msl_s2a_mcl_2026-08/run_construct_g0.py
# expect explore_scored false without --explore-go
python lab/analysis/c1/msl_s2a_mcl_2026-08/run_construct_g0.py --explore-go
# expect REFUSE until EXPLORE_GO.md + MCL_M15 sha match
rg -n "2025-07-01|CONFIRM|DELETE|FLIP" lab/analysis/c1/msl_s2a_mcl_2026-08/EXPLORE_GO.DRAFT.md
```
