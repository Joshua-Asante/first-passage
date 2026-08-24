# ORB-MNQ payability line (orb_mnq · eodadv) — PARK

**Class:** (b) parked lane · **Standing:** PARK
**re-entry:** new payability / cost-geometry evidence at an admissible venue
**expiry:** 2026-11-08 (converts to SUBTRACT absent explicit operator renewal — ADR §2.3)
**Aim served (if re-entered):** A2
**Residuals:** `lab/analysis/orb/orb_mnq_2026-07/`, `eodadv_mnq_2026-08/` stay hot; `sessconf_mnq_2026-08` continues live under pursuit a3 (not parked — distinct lane)
**Test applied:** expired-park-shaped (T2 payability FIRED 2026-08-03, 15:30 exit barred; the prior repo park lacked both re-entry and expiry fields — this record supplies them for the first time per ADR §2.3)

**Ratified:** 2026-08-09 (GSUB-1 Phase 3)
**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row b3

---

## Addendum 2026-08-24 — R3 tested at all four AUTOMATION_FRIENDLY firms: FAIL everywhere, standing unchanged

Operator GO 2026-08-24 ("GO on ORB-MNQ-1 at Bulenox/BluSky", extended same date to "Test
MFFU_Rapid_100K too") authorized the ADR §4 R3 survivor-scoring-pass precondition check at
Bulenox_100K, BluSky_Premium_100K, and MFFU_Rapid_100K — the three of the four
`AUTOMATION_FRIENDLY_PROP_FIRMS` not already tested by T2 (Tradeify). Result: **no (firm, k)
clears both frozen limbs** (bust ≤3.0% ∧ P(pass) ≥50%) at any of the three, k ∈ {1,2,3} — bust
ranges 62.37–82.22%, 21–27× the ceiling at every firm. Full measurement, controls, and the
barrier-geometry finding explaining why BluSky/MFFU (higher cost) land close to Tradeify's own T2
figures while Bulenox (lower cost) does not:
[`RESULTS_bulenox_blusky_payability.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_bulenox_blusky_payability.md).

**R3 does not fire anywhere** (a PASS was the precondition; every firm measured FAIL). **Standing
stays PARK, unchanged.** With MFFU included, **all four `AUTOMATION_FRIENDLY_PROP_FIRMS` this
repo tracks have now been tested and all four fail** — venue migration inside the currently-tracked
friendly-firm set is exhausted as a re-entry path for this construct. A future re-entry would need
either a firm outside that set, or genuinely new payability/cost-geometry evidence per this
document's own re-entry clause, not another venue swap among these four. $0 spend, no K, no
manifest, nothing armed.
