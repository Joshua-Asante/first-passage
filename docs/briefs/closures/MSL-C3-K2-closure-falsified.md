# MSL-C3-K2 — CLOSURE: `FALSIFIED` (both axes, both-arms CI upper < 0 on IS)

**Verdict:** `FALSIFIED` — Axis A and Axis B each fail both fade arms (session-block 95% CI entirely below 0); promotion → STOP
**Closed:** 2026-08-13
**Lane:** MSL · card MSL-C3-K2 revive · mechanisms `pdh-pdl-failed-break-reclaim` + `overnight-range-failed-extension-fade` × **M2K** · `K_intrinsic=2`
**Pre-registration:** [`PREREG_G0.md`](../../../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md) (FROZEN 2026-08-13) · explore GO paid 2026-08-13 (gitignored `EXPLORE_GO.md`) · [ADR](../../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md)
**Spend / K:** $0.00 · `K_intrinsic=2` disclosure · Cap **not claimed** · DSR floor 0.850 disclosure
**Live effect:** none — CONFIRM reserved **unread**; no Pine / TV / arming
**Artifacts:** [`RESULTS_g2.md`](../../../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) · [`RESULTS.json`](../../../lab/archive/msl_c3_m2k_2026-08/RESULTS.json)
**Panel:** `core/data/bar_data/M2K_M15.csv` sha256 `8192257081f7f4796910a554caa395088c32e5e79146cdd1ddc8d2b04b912349` (TV BAR EXPORT `…_14faf`; span → 2026-07-02 UTC; IS cut 2025-08-31)

---

## 1. Verdict against the frozen gate

| Axis | Route | Actual | Fired? |
|---|---|---|---|
| A `pdh-pdl-failed-break-reclaim` | both arms n≥100 ∧ CI upper < 0 | long n=293 CI [−0.256, **−0.038**]; short n=295 CI [−0.307, **−0.089**] | ✓ FALSIFIED |
| B `overnight-range-failed-extension-fade` | both arms n≥100 ∧ CI upper < 0 | long n=359 CI [−0.220, **−0.021**]; short n=378 CI [−0.204, **−0.014**] | ✓ FALSIFIED |
| Promotion | ≤1 axis if non-FALSIFIED | both FALSIFIED → `promoted_axis=null` | STOP |

Pooled mean net R: A **−0.171R** · B **−0.114R**. Halves agree (both negative) on all four arms. AnnSR all &lt; 0.

DELETE: Axis A FAIL both arms (overnight sham less negative). Axis B PASS both (PDH/PDL sham worse). FLIP: mixed/PASS — **moot** under primary FALSIFIED.

## 2. Predicted vs happened

Stage-1 $0 screens PASSed; B4 + G0 freeze licensed dual-axis IS. Explore shows both licensed stories are **statistically negative** on M2K under the frozen G0. DELETE PASS on Axis B does not rescue a FALSIFIED primary. Does **not** clear or reopen C1 MYM kill of the PDH/PDL class — separate instrument row.

## 3. What this closure does NOT license

Reading CONFIRM · Cap · Pine/TV/B5 · θ-retune / silent drop to K=1 · treating DELETE PASS as survival · re-scoring with stop-buffer sweep as selection · arming · Striker redeploy · estate Cap/DSR/floor edits.

## 4. Defects found in the frozen packet

None load-bearing. Panel sha matched pin. Globex session key (18:00 ET → next calendar date) applied so overnight [18:00→09:29] coheres with RTH for Axis B. Panel ends **2026-07-02** — CONFIRM label in G0 ran to 2026-08-13 but unread bytes stop at panel (MCL precedent).

## 5. Lesson candidates

PDH/PDL failed-break reclaim now explore-FALSIFIED on **MYM and M2K**. Overnight-range failed-extension fade explore-FALSIFIED on M2K (first score). Below two-incident bar for a new methodology lesson file unless Board consolidates.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED` (both axes)
- **Model update:** Neither scored axis is an IS edge on M2K under this G0.
- **Next:** STOP catalogue / G0. Board slot freed — **S2B** may resume (was deferred for C3-K2).
- **Stop rule / re-proposal bar:** new mechanism evidence (different reference class / direction / TF / instrument story), **not** stop-buffer / window / rr retune on this G0; **not** silent revive of either axis.
- **Board write:** plan §6 P3.2b → explore FALSIFIED; Open/next → S2B or Board.

- **Registry:** rejected_candidates.md — ### MSL-C3-K2 dual-axis MR-at-level × M2K — FALSIFIED (explore IS; K=2)

## §10 audit-hook discharge

```text
# panel sha
8192257081f7f4796910a554caa395088c32e5e79146cdd1ddc8d2b04b912349  MATCH
# gate
FALSIFIED (A+B; both CI uppers < 0; promoted_axis=null)
# CONFIRM
unread (explore_end 2025-08-31; confirm reserved 2025-09-01→2026-08-13; panel bytes end 2026-07-02)
```
