# Q-R2AGRUN-1 — CLOSURE: `AMBIGUOUS-HOLD` (magnitude; non-promotable)

**Verdict:** `AMBIGUOUS-HOLD` (magnitude floor) — operator-elected **non-promotable close** of this G0 catalogue
**Closed:** 2026-08-08
**Pre-registration:** [`PREREG_G0.md`](../../lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md) · parent [`Q-R2AGRUN-1`](../Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md)
**Successor:** named, not opened — [`Q-R2FLOW-1`](../Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md) (clock-minute net signed aggressor size → 60 s mid)
**Spend / K:** $0.00 · `K_intrinsic=1` disclosure only · Cap seat **not claimed**
**Live effect:** none — CONFIRM unread; no rail / Pine / arming
**Artifacts:** [`RESULTS_g2.md`](../../lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md) · [`RESULTS_g2.json`](../../lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.json)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | G2 promote ∧ Cap ∧ C0 ∧ Stage-C PASS | G2 did not promote | — |
| `FALSIFIED` | Stage-G fails CI/placebo **or** Stage-C fails | CI PASS · placebo PASS · halves PASS | — |
| `AMBIGUOUS-HOLD` | VOID-* / halves disagree / \|ρ\| < 0.02 | \|ρ\| **0.001306** < **0.02**; n=22,304,297; coverage 100%; ρ −0.001306; CI95 [−0.002589, −0.000020]; placebo p95 0.000398; H1/H2 both negative | ✓ |

Frozen brief §6 pre-registered disposition for `AMBIGUOUS-HOLD`: **ITERATE**. Operator closure judgment elects **STOP** (non-promotable) — legitimate per Iterate ADR §2 (frozen row stands; this block states why the other branch fired).

---

## 2. What the pre-registration predicted vs what happened

- **Expected most-likely:** association null (R2VBUCK-shaped) or coverage pathology (OFCHAN-shaped).
- **Actual:** coverage/power cleared; CI + placebo + halves cleared; **magnitude floor** was the deciding limb. A *tiny* negative association is detectable at n≈22M but was pre-registered as non-interpretable below 0.02.
- **Surprise:** CI excluded 0 despite \|ρ\| ≪ floor — large-n precision, not a tradable signal under EM1 honesty (§7).

---

## 3. What this closure does NOT license

- Raising / lowering the 0.02 floor after seeing ρ (FM-9 / Trap #12).
- Scoring CONFIRM on this cell.
- Claiming Cap or harvest admission.
- Treating “detectable ≠ 0” as Route B candidate status.
- Redeploying Striker / arming the rail.

---

## 4. Defects found in the frozen brief (recorded, not repaired)

None that change the verdict. Implementation note (not a §4 defect): bootstrap/placebo used sufficient-statistics / `SeedSequence.spawn` equivalents for the frozen Pearson limbs — disclosed in `RESULTS_g2.json`; not a limb edit.

---

## 5. Lesson candidates

**2026-08-08 — large-n OF association cells can clear CI/placebo while failing a pre-registered magnitude floor.** Cost: one explore-GO session + ~22M-pair Stage-G. Watch: do not treat CI-excludes-0 alone as promotion when a magnitude floor is frozen. Below the two-incident bar for a standing lesson — watch.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (magnitude floor)
- **Model update:** Aggressor-*run length* is not a Route B promotable associate of 60 s mid under the frozen 0.02 bar. Detectability at industrial n is not interpretability. Third consecutive OF catalogue (OFCHAN coverage → R2VBUCK association-null → AGRUN magnitude) reinforces: next cell must change the **causal object**, not the denseness fix.
- **Next:** STOP
- **Routing:** STOP — this G0 catalogue is **non-promotable**; operator closes it. CONFIRM stays unread. A successor OF cell is a **new Q / new G0**, not an ITERATE retune of `N_min`/horizon/floor.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** Re-open of *aggressor-run length → 60 s mid* requires new **mechanism** evidence (not `N_min`/horizon/floor edit, not more days of the same feature). Sibling OF cells under MNQDTL R2 are allowed only as **fresh Q-IDs** with a new named feature.
- **Board write:** `SESSIONS Open/next: Operator explore GO on Q-R2FLOW-1 (named successor) — or decline. Carry: weekly token; S2b; 08-08 audit; F1 2026-11-08.` Owner: this closure · [`Q-R2FLOW-1`](../Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)

---

## §10 audit-hook discharge

```text
# G0 / RESULTS present
lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md  OK
lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md  OK
# Verdict tokens
rg AMBIGUOUS-HOLD RESULTS_g2.md → present
rg "0\.02|magnitude" RESULTS_g2.md → present
# CONFIRM unread
rg "confirm_untouched.: true" RESULTS_g2.json → true
# Cap
rg "cap_seat_claimed.: false" RESULTS_g2.json → false
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-08 | Closure filed — AMBIGUOUS-HOLD; operator non-promotable STOP; successor Q-R2FLOW-1 named not opened | Cursor + JA |
