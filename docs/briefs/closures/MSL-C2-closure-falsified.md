# MSL-C2 — CLOSURE: `FALSIFIED` (both-arms CI upper &lt; 0 on IS)

**Verdict:** `FALSIFIED` — both fade arms mean net R negative with session-block 95% CI entirely below 0
**Closed:** 2026-08-13
**Lane:** MSL · card MSL-C2 · mechanism `london-range-failed-extension-fade` × MGC
**Pre-registration:** [`PREREG_G0.md`](../../../lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md) (FROZEN 2026-08-12) · [`EXPLORE_GO.DRAFT.md`](../../../lab/archive/msl_c2_mgc_2026-08/EXPLORE_GO.DRAFT.md) (promoted → gitignored `EXPLORE_GO.md` ISSUED 2026-08-13)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap **not claimed**
**Live effect:** none — CONFIRM (2025-09-01→2026-08-12) reserved **unread**; no Pine / TV / arming
**Artifacts:** [`RESULTS_g2.md`](../../../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md) · [`RESULTS.json`](../../../lab/archive/msl_c2_mgc_2026-08/RESULTS.json) · [explore-GO card](../handoffs/2026-08-13-msl-c2-explore-go-card.md)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` | both arms n≥100 ∧ CI upper &lt; 0 | long n=327 CI [−0.287, **−0.071**]; short n=310 CI [−0.292, **−0.075**] | ✓ |
| `SHAPE-CLEAR` | ≥1 arm CI lo &gt; 0 ∧ DELETE PASS ∧ FLIP PASS ∧ aux live-pass | both means negative; DELETE FAIL both arms | — |
| `AMBIGUOUS-HOLD` | otherwise | moot — FALSIFIED fired | — |

Primary means: long **−0.179R** · short **−0.182R** · WR ≈ 0.471 both · annSR ≈ −1.67 / −1.66.

## 2. Predicted vs happened

Stage-1 $0 screens PASSed (cost-law / $200 / $750 at design geometry). Explore on pinned `MGC_M15` IS shows the fade is **economically and statistically negative** on both arms; DELETE FAIL (sham prior-RTH mean less negative than London-constrained) — the London constraint does not SELECT favorably. FLIP PASS (fade slightly less bad than join) is moot under FALSIFIED.

## 3. What this closure does NOT license

Reading CONFIRM · Cap · Pine/TV/B5 · θ-retune rescue of this G0 · treating FLIP PASS as survival · Guardian→MGC transfer re-open · instrument hop to “fix” the fade · arming.

## 4. Defects found in the frozen packet

None load-bearing. Harness + DRAFT delete/flip were authored pre-score; panel sha matched pin `88da9f15…`.

## 5. Lesson candidates

Below two-incident bar — watch: Stage-1 design-point arithmetic can PASS while IS path-PnL is deeply negative when stop distances realize ~6 pt (≪ Stage-1 16 pt design disclose).

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** London-range failed-extension fade on MGC is not an IS edge under the frozen G0; Req 1a DELETE also fails (constraint harms vs sham).
- **Next:** STOP
- **Routing:** STOP this catalogue / G0. Serialized slate hands slot to **P3.2 MSL-C3 (M2K)** — Stage-0 L3 one-shot + WSTRUCT sequencing before flight (not opened here).
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new mechanism evidence (different reference class / direction / TF), not stop-buffer or window retune on this G0. Re-proposal ≠ C3.
- **Board write:** Open/next → P3.2 C3 Stage-0 (L3 + WSTRUCT read) — owner [`msl-first-slate`](../2026-08-12-msl-first-slate.md) §MSL-C3 · [`msl-program-plan`](../2026-08-12-msl-program-plan.md) §6.

- **Registry:** rejected_candidates.md — ### MSL-C2 London-range failed-extension fade × MGC — FALSIFIED (explore IS)

## §10 audit-hook discharge

```text
# panel sha
88da9f1597daca5c6a118fa4539a117aba5ea4255d81e7475fd7029987caf3f3  MATCH
# gate
FALSIFIED (both CI uppers < 0)
# CONFIRM
unread (explore_end 2025-08-31; confirm reserved 2025-09-01→2026-08-12)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-13 | Filed FALSIFIED after local explore GO + IS score | Cursor + JA continue |
