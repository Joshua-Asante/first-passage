# Q-CAPFLOW-1 — CLOSURE: `FALSIFIED` (CI includes 0; Cap held)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-14
**Lane:** avenue-a-route-a-cap-spend
**Pre-registration:** [`lab/analysis/c1/mnq_capflow_orb_r_2026-08/PREREG.md`](../../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/PREREG.md) — Cap-spend GO signed 2026-08-08
**Parent reservation:** [`Q-CAPRES-2`](../Q-CAPRES-2-mnq-cap-seat-reservation.md) (RESOLVED)
**Spend / K:** $0.00 · K consumed: 0 · `cap_spent=false`
**Live effect:** none — Cap seat remains held; no ORB gate; C11 stands
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md) · [`RESULTS.json`](../../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.json)

---

**⚠ 2026-08-29 path correction:** the PREREG/RESULTS/RESULTS.json links above point to `lab/analysis/c1/mnq_capflow_orb_r_2026-08/`, which no longer exists — the campaign was archived 2026-08-21 (see `lab/CATALOG.md`). Current location: stub `lab/analysis/mnq_capflow_orb_r_2026-08/CARD.md`, full body `lab/archive/mnq_capflow_orb_r_2026-08/`. Verdict/numbers below are unaffected and unedited.

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| VOID-POWER | covered n < 30 | covered **255** | — |
| VOID-COVERAGE | usable fraction < 90% | coverage **1.000** (255/255) | — |
| `FALSIFIED` | CI includes 0 **or** fails placebo | ρ **+0.020012**; CI95 **[−0.089845, +0.114398]** includes 0; placebo \|·\| p95 **0.020012** (p_emp **1.000**) | **✓** |
| AMBIGUOUS-HOLD | clear except \|ρ\| < 0.02 **or** halves disagree | \|ρ\| ≈ 0.020 (at floor); H1 **+0.0419** / H2 **−0.0067** (sign disagree) — not reached; CI limb fires first | — |
| `RESOLVED` | all clear | not reached | — |

**Cap disposition:** held (`cap_spent=false`; `k_intrinsic=0`).

## 2. What the pre-registration predicted vs what happened

PREREG asked whether OR-window net signed aggressor size associates with ORB-MNQ-1 realized R enough to mark a fresh Cap seat spent. Coverage/power cleared (255/255). The association did **not**: session-block CI includes 0, and the observed \|ρ\| equals the within-session shuffle placebo p95. Halves disagree in sign as a non-reached secondary. Cap-held expectation **held**.

## 3. What this closure does NOT license

- Treating CapFLOW as a TNEC / WHO / slate-4 substitute.
- Converting any CapFLOW number into an ORB entry filter (C11) or Tradeify unpark.
- Re-pulling OFCHAN or re-scoring under a retuned horizon / event set / schema.
- Claiming Cap spent or `K_intrinsic=1`.

## 4. Defects found in the frozen brief (recorded, not repaired)

- PREREG markdown has mojibake on disk; construct table treated as frozen and not "fixed."
- `run_capflow.py` ORB_LIB path used `parents[2]` (`lab/orb/…`) after the theme nest; corrected to `parents[1]` (`lab/analysis/orb/…`) so unmodified `orb_lib.orb_backtest` could join R. `orb_lib.py` restored from pre-prune for the ACTIVE CapFLOW dependency.
- Gap TBBO blob was already local; day-parquet split was a $0 local decode (no Databento re-bill). `estimate_gap.py` still reported `ESTIMATE_OK_AWAITING_PULL_GO` because it ignores the gap blob — `pull_or_windows.py` correctly reported `reuse_gap_blob`.

## 5. Lesson candidates

Below the two-incident bar — watch: CapFLOW camp path math vs theme-nest prune can leave an ACTIVE Cap-spend harness unable to import its R engine until `orb_lib` is restored.

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `FALSIFIED`
- **Model update:** Tape-flow A in the OR window ending at the ORB trigger does not carry a Cap-spendable association with path R on this frozen event set. Coverage was not the wall; the ρ/CI limb was.
- **Next:** STOP
- **Routing:** STOP — CapFLOW Cap-spend cell closed; Cap held; reservation Q-CAPRES-2 discharged its unpaid score obligation.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** New Cap-spend cell requires a fresh Cap-reservation GO + Cap-spend GO + new G0/construct (different feature or survivor-tied question) — not a retune of ρ floor, OR window, or this event set.
- **Board write:** `SESSIONS Open/next: CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO.` Owner: this closure · [`RESULTS`](../../../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md)

- **Registry:** rejected_candidates.md — ### OR-window net signed aggressor size × MNQ — FALSIFIED (CI includes 0)

## §10 audit-hook discharge

```text
# Parent reservation hooks (Q-CAPRES-2 §10)
PRESENT docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md
PRESENT lab/archive/mnq_capflow_orb_r_2026-08/PREREG.md  # 2026-08-29: repointed post-2026-08-21 archival (was lab/analysis/c1/mnq_capflow_orb_r_2026-08/PREREG.md)
rg C11|Cap-reservation → hits in Q-CAPRES-2 (C11 bar stands)

# CapFLOW score
RESULTS.json verdict=FALSIFIED cap_spent=false coverage=1.0 n=255
pytest test_capflow_lib.py → 15 passed (pre-score)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Closure authored after single Cap-spend run | Joshua + Cursor |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-CAPFLOW-1-closure-falsified.md
```
