# MSL-C1 — CLOSURE: `FALSIFIED` (both-arms CI upper &lt; 0 on IS)

**Verdict:** `FALSIFIED` — both fade arms mean net R negative with session-block 95% CI entirely below 0
**Closed:** 2026-08-13
**Lane:** MSL · card MSL-C1 · mechanism `pdh-pdl-failed-break-reclaim` × **MYM**
**Pre-registration:** [`PREREG_G0.md`](../../../lab/archive/msl_c1_mym_2026-08/PREREG_G0.md) (FROZEN 2026-08-13) · [`EXPLORE_GO.DRAFT.md`](../../../lab/archive/msl_c1_mym_2026-08/EXPLORE_GO.DRAFT.md) (promoted → gitignored `EXPLORE_GO.md` ISSUED 2026-08-13)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-13) reserved **unread**; no Pine / TV / arming
**Artifacts:** [`RESULTS_g2.md`](../../../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [`RESULTS.json`](../../../lab/archive/msl_c1_mym_2026-08/RESULTS.json)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper &lt; 0 | long n=406 CI [−0.267, **−0.083**]; short n=444 CI [−0.197, **−0.017**] | ✓ |
| `SHAPE-CLEAR` | ≥1 arm CI lo &gt; 0 ∧ DELETE PASS ∧ FLIP PASS ∧ aux live-pass | both means negative | — |
| `AMBIGUOUS-HOLD` | otherwise | moot — FALSIFIED fired | — |

Primary means: long **−0.176R** · short **−0.107R** · WR ≈ 0.461 / 0.486 · annSR ≈ −1.46 / −0.92.

DELETE: PASS both arms (constrained less negative than overnight sham). FLIP: long FAIL / short PASS — moot under FALSIFIED.

## 2. Predicted vs happened

Stage-1 $0 screens PASSed (cost-law / $200 / $750; route ① + B8). Explore on pinned `MYM_M15` IS shows the fade is **statistically negative** on both arms. DELETE PASS does not rescue a FALSIFIED primary.

## 3. What this closure does NOT license

Reading CONFIRM · Cap · Pine/TV/B5 · θ-retune rescue of this G0 · treating DELETE PASS as survival · silent revive of C3 M2K unpaid path · instrument hop · arming · Striker redeploy.

## 4. Defects found in the frozen packet

None load-bearing. Harness + DRAFT delete/flip authored pre-score; panel sha matched pin `24e16952…`.

## 5. Lesson candidates

Below two-incident bar — watch: PDH/PDL failed-break reclaim now FALSIFIED on MYM after C3 OPERATOR-KILL on M2K unpaid path; class had no surviving host on the **first** MSL slate (C2→C3→C1). ⚠ Not a current-board claim — M2K dual-axis revive explore also **FALSIFIED** ([closure](MSL-C3-K2-closure-falsified.md)); PDH/PDL class now dead on MYM and M2K under their G0s.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** Prior-day RTH PDH/PDL failed-break reclaim on MYM is not an IS edge under the frozen G0.
- **Next:** STOP
- **Routing:** STOP this catalogue / G0. First MSL slate (C2→C3→C1) complete: C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED. Board review of next slate / channel yield is outside this closure.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new mechanism evidence (different reference class / direction / TF), not stop-buffer or overnight-sham retune on this G0.
- **Board write:** plan §6 P3.3 → FALSIFIED (explore IS); Open/next → Board (slate exhausted).

- **Registry:** rejected_candidates.md — ### MSL-C1 PDH/PDL failed-break reclaim × MYM — FALSIFIED (explore IS)

## §10 audit-hook discharge

```text
# panel sha
24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58  MATCH
# gate
FALSIFIED (both CI uppers < 0)
# CONFIRM
unread (explore_end 2025-08-31; confirm reserved 2025-09-01→2026-08-13)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-13 | Filed FALSIFIED after local explore GO + IS score | Cursor + JA |
