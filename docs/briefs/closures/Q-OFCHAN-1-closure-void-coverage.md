# Q-OFCHAN-1 — CLOSURE: `VOID-COVERAGE` (Stage-G; empty candidates)

**Verdict:** `VOID-COVERAGE` — empty candidates; STOP this G0 catalogue
**Closed:** 2026-08-07
**Pre-registration:** [`PREREG_G0.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md)
**Parent:** [`Q-OFCHAN-1`](../Q-OFCHAN-1-orderflow-channel-route-b-scoping.md)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure · Cap **not claimed**
**Live effect:** none — CONFIRM unread
**Artifacts:** [`RESULTS_g2.md`](../../lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | G2 promote ∧ C0 ∧ Stage-C PASS at M=1 | G2 did not promote | — |
| `FALSIFIED` | Stage-G fails CI/placebo **or** Stage-C fails | not scored (coverage precedes) | — |
| `AMBIGUOUS-HOLD` / `VOID-COVERAGE` | VOID-POWER / VOID-COVERAGE / halves / magnitude | VOID-POWER PASS (n=**3,558** ≥ 2,000); **VOID-COVERAGE FIRE** — **3,558 / 48,360 = 7.36%** (< 90%); observed CI95 [−0.048, +0.024] includes 0 (not deciding); \|ρ\|=0.012; halves disagree | ✓ |
| Candidates | G3 empty list | **[]** | ✓ |

Frozen brief §6 pre-registered disposition for VOID-COVERAGE: **`AMBIGUOUS-HOLD` → ITERATE**. Operator / Avenue A checklist G3 recorded disposition: empty candidates → **STOP** this catalogue (RESULTS_g2; PREREG status line). Closure judgment elects **STOP** — legitimate per Iterate ADR §2 (frozen row stands; this block states why the other branch fired).

---

## 2. What the pre-registration predicted vs what happened

- Coverage floor was a named VOID route; it fired hard (7.36% retained).
- Likely driver (disclosure, not a retune): flicker filter requires ≥5 same-sign TBBO updates in the trailing 1 s; EXPLORATION day files are trade-tagged TBBO (`action=T`), so quiet minutes drop before ρ.
- CONFIRM reserved unread; Cap untouched.

---

## 3. What this closure does NOT license

- Retuning flicker / grid / catalogue post-hoc (FM-9 / Trap #12).
- Scoring CONFIRM on this cell.
- Claiming Cap, harvest PASS, or an edge.
- Reopening without a **new G0** / new mechanism.

---

## 4. Defects found in the frozen brief (recorded, not repaired)

§6 maps VOID-COVERAGE → ITERATE while G3 empty-list practice (and the landed RESULTS disposition) routes STOP. Recorded here; frozen brief not edited.

---

## 5. Lesson candidates

**2026-08-07 — flicker-on-trade-tagged TBBO at clock minutes can starve coverage below the 90% floor.** Cost: one explore session + cache reuse ($0). Below two-incident bar — watch.

---

## Iterate — loop exit

- **Verdict used:** `VOID-COVERAGE`
- **Model update:** Flicker-filtered L1 size imbalance on the RTH minute grid is **unscoreable** under the frozen filter on this EXPLORATION batch — failure is denseness/coverage, not a measured association. Reopen requires a new catalogue definition, not a quieter threshold.
- **Next:** STOP
- **Routing:** STOP — this G0 catalogue dies; CONFIRM stays unread. Successor OF cells only as **fresh Q-IDs / new G0**.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** Re-proposal = **new mechanism / new G0 catalogue**, not flicker retune, not horizon retune, not more days of the same cell.
- **Board write:** none — STOP, nothing owed (roster row deletion is bookkeeping only).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Closure authored (verdict landed 2026-08-07; artifact was missing) | Cursor + JA |
