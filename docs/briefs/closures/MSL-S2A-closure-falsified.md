# MSL-S2A — CLOSURE: `FALSIFIED` (N-ACT: trades/week &lt; 1 on IS)

**Verdict:** `FALSIFIED` — measured entry rate 0.511 trades/week &lt; 1 (N-ACT solo explore-gate); long FLIP FAIL co-fires
**Closed:** 2026-08-13
**Lane:** MSL · card MSL-S2A · mechanism `pullback-failure-resumption` × MCL
**Pre-registration:** [`PREREG_G0.md`](../../../lab/analysis/c1/msl_s2a_mcl_2026-08/PREREG_G0.md) (FROZEN 2026-08-13) · [`EXPLORE_GO.DRAFT.md`](../../../lab/analysis/c1/msl_s2a_mcl_2026-08/EXPLORE_GO.DRAFT.md) (promoted → gitignored `EXPLORE_GO.md` ISSUED 2026-08-13)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap **not claimed**
**Live effect:** none — CONFIRM (2025-07-01→2026-07-02) reserved **unread**; no Pine / TV / arming
**Artifacts:** [`RESULTS_g2.md`](../../../lab/analysis/c1/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [`RESULTS.json`](../../../lab/analysis/c1/msl_s2a_mcl_2026-08/RESULTS.json)

---

## 1. Verdict against the frozen gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `FALSIFIED` (CI) | both arms n≥100 ∧ CI upper &lt; 0 | long n=31 CI [−0.464, **0.144**]; short n=46 CI [−0.287, **0.146**] | — |
| `FALSIFIED` (N-ACT) | measured trades/week &lt; 1 | **0.511** (77 trades / 753 IS sessions) | ✓ |
| `SHAPE-CLEAR` | ≥1 arm CI lo &gt; 0 ∧ DELETE PASS ∧ FLIP PASS ∧ aux live-pass | CI lo &lt; 0 both arms; long FLIP FAIL; aux fail both | — |
| `AMBIGUOUS-HOLD` | otherwise | moot — FALSIFIED fired | — |
| `VOID` | coverage / panel / token refusal | panel sha match; GO issued; 753 sessions scored | — |

Primary means: long **−0.1749R** · short **−0.0769R** · WR 0.355 / 0.435 · annSR −0.64 / −0.40.
DELETE PASS both arms. Long FLIP FAIL (join-pullback **+0.047R** vs resume **−0.175R**).

**Not `BOOK-CONDITIONAL(cadence)`:** N-ACT is the explore-gate trigger, but long FLIP FAIL (Req 1a) and negative means co-fire. TNEC-AU-1 cadence-only token does not apply.

## 2. Predicted vs happened

Stage-1 $0 screens PASSed (cost-law / $200 / $750 at **180-tick** design geometry). Explore on pinned `MCL_M15` IS: the construct **rarely fires** (designed 1/session; realized 77/753 ≈ 10% of sessions) and **fails N-ACT**. Realized stop ≈ 0.80 pt (~80 ticks, 4.9× RT) — cost-law at realized span still clears; the kill is cadence, not 4×. DELETE PASS (constraint less negative than matched-TOD sham). Long FLIP FAIL — joining the pullback beat the resumption on that arm, so the WHO unwind story did not select.

## 3. What this closure does NOT license

Reading CONFIRM · Cap · Pine/TV/B5 · θ-retune rescue of this G0 (impulse/pullback windows, stop buffer, rr, k, 09:00–14:30) · treating DELETE PASS as a continuation edge · `BOOK-CONDITIONAL(cadence)` · CONFIG-B-MCL fade re-open · Q-MCLTAS-1 re-open · instrument hop · arming.

## 4. Defects found in the frozen packet

Harness: first DELETE sham pass produced a short-arm mean ≈ −7×10¹⁰ from a sub-tick stop_dist. Guard `stop_dist ≥ 1 tick` added **before** RESULTS-of-record; constrained means unchanged; short sham repaired to **−0.312R**. Not a G0 rewrite.

## 5. Lesson candidates

Below two-incident bar — watch: Stage-1 entry-rate honesty was a **design** 1/session after ~14% roll-exclude; measured coverage was 10% of IS sessions. N-ACT is a measured limb, not a design attestation.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** MCL pullback-failure resumption under this G0 is not an IS-viable solo construct (cadence). The continuation constraint beats a TOD sham but the long arm is better as a pullback *join* than as a resumption — Req 1a direction fails on that arm.
- **Next:** STOP
- **Routing:** STOP this catalogue / G0. Slate-2 slot remaining was **S2B**; board 2026-08-13 inserted [C3-K2 revive](../../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) ahead of S2B (S2B route still unresolved — do not take the TV seat). Not opened here.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new mechanism evidence (different reference class / direction / TF), not I/P-window, stop-buffer, or rr retune on this G0. Re-proposal ≠ S2B.
- **Board write:** Open/next was S2B at close; **superseded 2026-08-13** by [C3-K2 revive](../../adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) ahead of S2B — live pointer [`SESSIONS`](../../SESSIONS.md) top · plan §6 P3.2b.

- **Registry:** rejected_candidates.md — ### MSL-S2A pullback-failure resumption × MCL — FALSIFIED (explore IS)

## §10 audit-hook discharge

```text
# panel sha
5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23  MATCH
# gate
FALSIFIED (N-ACT 0.511 trades/week)
# CONFIRM
unread (explore_end 2025-06-30; confirm reserved 2025-07-01→2026-07-02)
# TNEC
F U U U U | U | U | L-0.1749/S-0.0769
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-13 | Filed FALSIFIED after local explore GO + IS score | Cursor + JA continue |
