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

## Addendum 2026-08-26 — new payability evidence: a combined book with Aegis-6J1 clears Tradeify in bootstrap; ORB-MNQ-1 solo does not

Operator-supplied TradingView exports (Aegis-6J1 v3, ORB-MNQ-1 v6; 1yr/3yr/6yr) enabled a
combined-book sweep at `Tradeify_Select_100K`, independent of the Bulenox/BluSky/MFFU R3 test
above: [`lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md`](../../lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/RESULTS.md).
**ORB-MNQ-1 solo confirms this addendum's own standing** — the corrected full 6-year panel finds
it now busts on its own single realized path at every tested size (1-8 contracts), worse than
previously measured, not better. **But a naive equal-\$-risk combination with Aegis-6J1** (weighted
so ORB-MNQ contributes a sliver, 0.18-0.40 contracts, never a comparably-sized leg) bootstraps to
**1.51% bust / 1.49pp margin (3yr)** and **0.01% bust / 2.98pp margin (1yr)** against the 3.0%
ceiling — under EOD-clock replay, with several open hypotheses still unresolved (rescale bias,
EOD-vs-intraday clock correction — see that RESULTS.md §6/§8).

This is new payability/cost-geometry evidence at an admissible venue (Tradeify) — on point for
this document's own re-entry clause — but it is evidence about ORB-MNQ **as a small overlay inside
a specific combined construct**, not about ORB-MNQ as a standalone leg (which this addendum leaves
exactly as parked as the R3 finding above). Re-entry / re-scoping this pursuit around a combined-book
framing, if warranted, is an operator call, not made here. $0 spend, no K, no manifest, nothing
armed; exploratory research only, not pre-registered.

**Same-day follow-up (§9 of the cited RESULTS.md, landed after this addendum) materially weakens
the 1.51%/0.01% figures above — do not cite them without also reading that section.** A proper
both-halves regime-robustness bootstrap (not run when this addendum was first filed) finds the
**1yr construct fails outright** (second half alone: 4.02% bust, masked by the pooled 0.01%
figure); the 3yr construct passes both halves at its original basis but fails once a
tail-risk-consistent sizing ratio and a trade-level intraday-honest proxy are applied together
(4.34%). Net: this is still new payability evidence worth the re-entry-clause note above, but it
is materially thinner evidence than the figures first quoted here suggested — closer to "a narrow,
unconfirmed possibility" than "clears the ceiling with real margin."

**Further local-session follow-up (§10 of the cited RESULTS.md) reverses the remaining survivor
above — do not cite this addendum's headline figures at all without reading that section too.**
§10 re-tested the 3yr construct's both-halves pass under its own already-identified corrections
(tail-risk-consistent sizing + a genuine timestamp-sequenced intraday-honest remeasure,
superseding §9's trade-level proxy) applied together, split by regime half: **both halves now
fail** (3.29% / 5.37%, vs. the 3.0% ceiling) — the one cell this document's §9 note above still
credited as passing both halves does not survive full compounding. As of §10, no tested
configuration of this combined book, on either window, survives a full both-halves +
tail-sizing + intraday-honesty gate. This addendum's own re-entry-clause reasoning above should be
read as **superseded in strength, not withdrawn in kind**: the combined-book construct is still a
distinct payability question from ORB-MNQ solo (which stays exactly as parked either way), but the
specific evidence originally cited here no longer clears the eval ceiling under any tested
correction. One item (a native TradingView re-export at exactly 4 Aegis contracts) remains
genuinely open and could still move this picture; see that RESULTS.md §10.4.
