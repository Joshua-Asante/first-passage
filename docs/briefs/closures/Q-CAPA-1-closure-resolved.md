# Q-CAPA-1 — CLOSURE: `RESOLVED` (Cap seat spent; tripwire candidate)

**Verdict:** `RESOLVED`  
**Closed:** 2026-08-06  
**Pre-registration:** [`lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/PREREG.md) — frozen at `022c17d`  
**Phase-0:** [`PHASE0.md`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/PHASE0.md) (`CHARTER-CLEARS` + Cap-spend GO)  
**Spend / K:** $0.00 · `K_intrinsic=1` (Cap marked spent)  
**Live effect:** Cap seat status flip — **spent** on this Route A cell; no rail/Pine/lifecycle change; tripwire **not** wired  
**Artifacts:** [`RESULTS.md`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md) · [`RESULTS.json`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/RESULTS.json)

---

## 1. Verdict (§6 / PREREG §5 asserted against actual numbers)

| §6 / §5 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `VOID-POWER` | covered n < 30 | 255 | ✗ |
| `VOID-COVERAGE` | coverage < 90% | 100% | ✗ |
| `FALSIFIED` | CI includes 0 **or** \|Δ\| ≤ placebo p95 | CI excludes 0; \|Δ\| 0.022928 > 0.004356 | ✗ |
| `AMBIGUOUS-HOLD` | \|Δ\| < 0.00714 **or** halves disagree | \|Δ\| ≥ floor; halves same sign | ✗ |
| **`RESOLVED`** | clear of above | **all clear** | **✓** |

Difference **−0.022928**, CI95 **[−0.028061, −0.017558]**, placebo \|.\| p95 **0.004356** (p_emp **0.000**), coverage **100%** (255/255), H1/H2 both negative and excluding 0.

---

## 2. What the pre-registration predicted vs what happened

**Pre-registered expectation: Reject / Cap held.** Discharged as a **failed prediction** — forward persistence cleared every accept limb, and \|Δ\| was ≈2.4× N14’s pre-touch effect. The contemporaneous-tiny → forward-null story did not hold.

---

## 3. What this closure does NOT license

- ~~Auto-wire to PF-CUSUM / live decay monitors (separate GO).~~ **Wiring GO discharged 2026-08-06 as docs-only companion registration** — [`ADR 2026-08-06`](../../adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md) (`Accepted`). Still **not** live-wired / not Call-1 / not entry filter.  
- ORB entry filter / fifth conditioning gate (F2 GUARD).  
- PROX reopen or claim that the signature is ORB-specific.  
- MBP-10 / second Cap cell / horizon retune.  
- Lifecycle or payability change for ORB-MNQ-1.

---

## 4. Defects found in the frozen brief

None that move the verdict. Print-path Unicode crash in `run_capa.py` after `RESULTS.json` write — fixed post-run; numbers unchanged.

---

## 5. Lesson candidates

Below the two-incident bar — watch: Cap-spend cells with a strong “hold” prior can still clear when the forward window intensifies a pre-touch signature; do not treat “tiny contemporaneous” as a substitute for the forward measurement.

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `RESOLVED`
- **Model update:** N14’s against-break L1 tilt is not only contemporaneous — it **intensifies** in the 60 s after the ORB touch vs ToD-matched controls. Cap seat is no longer the idle “protected single discovery cell”; it is consumed by this tripwire-candidate cell. Wiring remains a separate decision.
- **Next:** **INTEGRATE**
- **Routing:** Board writes — Cap seat **spent**; brief CLOSED; STATE / MNQ / SESSIONS / INDEX / CATALOG. Wiring / PF-CUSUM companion GO is a **separate** operator packet (not opened here). Re-proposal of another Cap-seat discovery cell needs a fresh reservation.
- **Board write:** STATE decision index · MNQ ledger · SESSIONS · briefs INDEX · CATALOG — executed 2026-08-06. (Literal token line added 2026-08-07: the closure merged past HARD gate 14 without it — friction datum #1 on the Iterate ADR's §4 ledger; substance unchanged from Routing above.)
- **Stop rule / kill criteria for the Next:** Do not treat Cap spent as live monitor authorization. Do not convert `A_fwd` into an ORB gate without a new K-bound PREREG + GO. Do not reopen PROX to “explain” the Cap result.
- **What is explicitly NOT next:** MBP-10 escalation; Route B catalogue; outcome joins; ORB unpark.

### Addendum 2026-08-06 — wiring GO discharged (docs-only)

Operator chose companion registration (option 1). Iterate’s “wiring GO separate” is **discharged** by [`ADR 2026-08-06-capa-tripwire-pfcusum-companion-registration.md`](../../adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md) (`Accepted` 2026-08-06): tripwire standing = **registered companion** beside the PF-CUSUM seed — still not live-wired. Cap seat remains **spent**. Frozen Iterate text above is historical; this addendum owns the discharge.
