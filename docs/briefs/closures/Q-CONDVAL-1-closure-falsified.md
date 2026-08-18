# Q-CONDVAL-1 — CLOSURE: `FALSIFIED` (CL range-state lift misses the pre-declared R-term bar)

**Verdict:** `FALSIFIED` — committed C−U lift 0.1297 < frozen `L_star` 0.4226; S1b conditioner-engineering branch parked
**Closed:** 2026-08-18
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-CONDVAL-1-verdict-preregistration.md`](../pre-registration/Q-CONDVAL-1-verdict-preregistration.md) — frozen on disk at sha256 `d1265eb2b0fa328c18b8a744a6f438d06611238fd2ada14ca12d06645748b386` (printed by the runner **before** `s1b_results.json` was opened)
**Spend / K:** $0.00 · K consumed: **0** · no manifest
**Live effect:** none on rail / `core/` / `dd_protection`. Conditioner-engineering GO off S1b is no longer electable.
**Artifacts:** [parent brief](../Q-CONDVAL-1-range-state-r-terms.md) · [prereg](../pre-registration/Q-CONDVAL-1-verdict-preregistration.md) · [`RESULTS`](../../../lab/analysis/_inbox/q_condval_1_2026-08/RESULTS.md)
**Parent notice:** [`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | `L ≥ L_star` (0.422564) | L=0.129694 | — |
| `FALSIFIED` | `L < L_star` | 0.129694 < 0.422564; ΔE=0.0337R vs bar 0.1099R | ✓ |
| `AMBIGUOUS-HOLD` | missing keys or `E_box ≤ 0` | both keys present; E_box=0.26 | — |

Walked the disclosure corners: every positive-gross slate-2 cell fails the gating bar. The easy envelope end (R=$200, RT=$2.82) would clear a 0.50× hurdle at the *same* center ΔE — recorded, not a rescue (prereg §B).

## 2. What the pre-registration predicted vs what happened

Prereg §C predicted `FALSIFIED` from the class (GENERIC clustering produces high-teen / low-20s raw C−U, not a 42 pp lift). Observed L=0.130 sits in that class. No surprise. O2 is discharged: the connecting arithmetic exists, and the measured lift does not clear it.

## 3. What this closure does NOT license

- Retracting SIGNAL-GENERIC or rewriting C5.
- Discharging MCL mechanism-owed.
- Moving `L_star` / rr / WR / R / RT to the easy envelope end and calling it KEEP.
- Opening a conditioner-engineering prereg from this close.
- Using 0.60 as a derived rate (it remains DECLARED-NOT-DERIVED; this Q replaced the *need* for it with a computed `L_star`, which the lift missed).
- Touching S2 / S3 un-pause conditions.

## 4. Defects found in the frozen brief (recorded, not repaired)

Parent notice observation D attributed "+0.052 C−U, 41st percentile of its own surrogate lift band" to S1b. Those are the **GC** lift numbers from `RESULTS_CORRECTED` §1. CL's committed C−U is 0.1297. The runner ignored the notice's number and read the JSON keys. No brief amendment.

## 5. Lesson candidates

Below the two-incident bar — watch: the 0.60 DECLARED-NOT-DERIVED number sat 2 pp from obs_CL 0.6282. Had it been used as the "minimum-useful rate," this Q would have been a KEEP by construction. The freeze-the-levers-before-the-lift rule is what prevented that laundering. Dated: 2026-08-18, this close. Dollar cost: $0 (caught at the cheap falsifier).

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED`
- **Model update:** A typed GENERIC range-state finding can be real at the pooled construction and still be economically empty at the N-EDGE cell the estate actually cites. Verdict-string continuation of the conditioner branch was the wrong justification.
- **Next:** STOP
- **Routing:** S1b conditioner-engineering prereg is not electable. Attention returns to the notice's remaining packets (Q-EXPR-1, Q-TRAINKILL-1) and to S2/S3 as spec-resident obligations — none of them opened here.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new *host geometry* declared as a named alternative *before* any lift re-read, or a new finding (not SIGNAL-GENERIC on this object). θ-moves of `L_star`, R, RT, or the 0.50 fraction do not reopen. Easy-envelope clear is not a re-proposal.
- **Board write:** STATE decision-index 2026-08-18 Q-CONDVAL-1 line; SESSIONS 18e Open/next drops "S1b conditioner-engineering prereg is electable."
- **Registry:** n/a — conditioner-branch park; SIGNAL-GENERIC finding stands; not a strategy-grounds seed kill

## §10 audit-hook discharge

```
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-CONDVAL-1-range-state-r-terms.md
→ hits (parent cite)

rg -n "0\.60" docs/briefs/pre-registration/Q-CONDVAL-1-verdict-preregistration.md
→ FORBIDDEN / DECLARED-NOT-DERIVED wording only; not an input to L_star

rg -n "prereg_sha256" lab/analysis/_inbox/q_condval_1_2026-08/RESULTS.md
→ d1265eb2b0fa328c18b8a744a6f438d06611238fd2ada14ca12d06645748b386

python lab/analysis/_inbox/q_condval_1_2026-08/run_condval.py
→ L 0.129694  L_star 0.422564  verdict FALSIFIED  (bit-identical re-run)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | Closure authored | Cursor (this session) |
