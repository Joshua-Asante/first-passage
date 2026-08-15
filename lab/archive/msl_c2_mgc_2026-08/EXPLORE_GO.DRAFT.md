# MSL-C2 — Explore GO draft (UNPAID)

**Status:** `DRAFT` — operator explore GO **unpaid**. Promote = copy this file to
`EXPLORE_GO.md` (gitignored) and add a first-line stamp `ISSUED YYYY-MM-DD`.
**Parent:** [`PREREG_G0.md`](PREREG_G0.md) · [`STAGE1.md`](STAGE1.md)
**Harness:** [`run_construct_g0.py`](run_construct_g0.py) · [`construct_lib.py`](construct_lib.py)
**Cost / K at draft:** $0 · K=0. Scoring spends nothing until `--explore-go` after promote.

---

## Promote rule (operator)

1. Restore `core/data/bar_data/MGC_M15.csv` bytes matching
   `core/data/bar_data/SHA256SUMS` pin `88da9f1597daca5c6a118fa4539a117aba5ea4255d81e7475fd7029987caf3f3`.
2. `cp EXPLORE_GO.DRAFT.md EXPLORE_GO.md` and stamp `ISSUED <date>` on line 1.
3. Run: `python lab/archive/msl_c2_mgc_2026-08/run_construct_g0.py --explore-go`
4. Do **not** author Pine / TV until explore gate is `SHAPE-CLEAR` (or operator kill → C3).

---

## Partitions (frozen — identical to PREREG; no re-election)

| Partition | Window |
|---|---|
| **IS / EXPLORATION** | session dates **&lt; 2025-09-01** |
| **CONFIRM** | **2025-09-01 → 2026-08-12** inclusive — **RESERVED UNREAD** through step 8 |

Any CONFIRM peek voids the holdout.

---

## Panel

- Path: `core/data/bar_data/MGC_M15.csv`
- Schema: `time,open,high,low,close,volume` (UTC `Z`); TZ interpret as America/New_York for session windows
- sha256 must match `SHA256SUMS` pin above; runner **REFUSE**s on mismatch / missing bytes

---

## Delete / flip (Req 1a) — frozen operationalization (IS-only)

Constraint under test: **London extreme + failure reclaim** selects the trade.

### DELETE

Same reclaim / stop / target / k=1 geometry as constrained, but London H/L replaced by
**prior Globex-day RTH (08:20–15:59 ET) H/L** as the sham reference.

- Score arms separately on IS.
- **FAIL** (constraint does not SELECT) if sham arm mean net R ≥ constrained arm mean net R
  on that arm.
- Either arm DELETE-FAIL ⇒ that arm is not SHAPE-CLEAR.

### FLIP

At the **same reclaim bar**, enter **with** the extension (join = opposite side of the fade)
instead of fade; stop/target distance symmetry preserved (same stop_dist magnitude, flipped side).

- Score arms separately on IS (flip-long vs constrained-short on upside-fail signals;
  flip-short vs constrained-long on downside-fail signals).
- **FAIL** if flip arm mean net R ≥ fade (constrained) arm mean net R.
- Either arm FLIP-FAIL ⇒ that arm is not SHAPE-CLEAR.

---

## Primary / aux limbs (PREREG §4)

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap 95% CI |
| Halves | Older / newer IS session-date halves |
| DSR | ≥ **0.650** at `K_intrinsic=1` (disclosure floor; Cap disclosure-not-gate) |
| Cost-law | Gross/trade vs **$16.48** (4× RT $4.12) at realized stop distances |
| Placebo (aux) | Sign-randomized observed R; `PLACEBO_REPS=1000`; seed `20260812`; **not selection** |
| Disclose | WR · stop_dist · trades/session · coverage · $200/$750 at explored qty · EM six-char |

### Gate vocabulary (explore)

- **FALSIFIED** — both arms CI upper bound &lt; 0 (with n floor per runner).
- **SHAPE-CLEAR** — ≥1 arm primary CI lo &gt; 0 **and** DELETE PASS **and** FLIP PASS **and** declared aux live-pass (placebo p_emp &lt; 0.05 ∧ annSR ≥ 0.650 ∧ halves agree).
- **AMBIGUOUS-HOLD** — otherwise (incl. primary pass with aux/delete/flip fail).
- **VOID** — coverage / panel / token refusal (no score).

CONFIRM unread. Cap not claimed. Pine unpaid until SHAPE-CLEAR + operator.

---

## Forbidden moves

- Path-scoring CONFIRM; any CONFIRM peek.
- Pine / TV / B5 without explore PASS + runbook links to steps 2–5.
- θ retune (London window, stop buffer, TF, rr, k) after seeing results — new G0.
- Instrument hop; using stop-buffer sweep {0,1,2} for **selection**.
- Self-authorizing explore score without this token file present as `EXPLORE_GO.md`.

---

## Audit hooks

```text
test -f lab/archive/msl_c2_mgc_2026-08/EXPLORE_GO.md
python lab/archive/msl_c2_mgc_2026-08/run_construct_g0.py
# expect explore_scored false without --explore-go
python lab/archive/msl_c2_mgc_2026-08/run_construct_g0.py --explore-go
# expect REFUSE until EXPLORE_GO.md + MGC_M15 sha match
rg -n "2025-09-01|CONFIRM|DELETE|FLIP" lab/archive/msl_c2_mgc_2026-08/EXPLORE_GO.DRAFT.md
```
