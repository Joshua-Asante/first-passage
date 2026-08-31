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
fail** (3.29% / 5.37%, vs. the 3.0% ceiling — the Part A eval bust ceiling in force at measurement
time; ⚠ Correction 2026-08-26: raised to 5.0% ~1hr later the same day by the operator
risk-tolerance override, [prereg v2](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md)
§3, still the live ceiling — under 5.0%, h1 (3.29%) clears alone but h2 (5.37%) still does not, so
this paragraph's both-halves-fail conclusion is unchanged) — the one cell this document's §9 note above still
credited as passing both halves does not survive full compounding. As of §10, no tested
configuration of this combined book, on either window, survives a full both-halves +
tail-sizing + intraday-honesty gate. This addendum's own re-entry-clause reasoning above should be
read as **superseded in strength, not withdrawn in kind**: the combined-book construct is still a
distinct payability question from ORB-MNQ solo (which stays exactly as parked either way), but the
specific evidence originally cited here no longer clears the eval ceiling under any tested
correction. One item (a native TradingView re-export at exactly 4 Aegis contracts) remains
genuinely open and could still move this picture; see that RESULTS.md §10.4.

## Addendum 2026-08-30 — overnight-range-conditioned ORB-MNQ-1: new payability evidence, standalone leg, on point for this document's own re-entry clause

`Q-RANGECOND-1` ([`closure`](../briefs/closures/Q-RANGECOND-1-closure-resolved.md)) tested whether
`Q-RANGEXFER-1`'s own presence-verified overnight-range conditioner (a day-selection filter,
independently derived, never touching this instrument's own trade log — see that closure's own
F2-GUARD distinction) changes `ORB-MNQ-1`'s own realized win-rate/mean-win shape enough to matter
for Tradeify payability, operator-ruled Route ① satisfied same day. Result: **conditioned-subset
win rate 66.47% vs. unconditioned 41.72% (+24.75pp, CI `[+18.30pp,+31.31pp]`); mean win (winners
only) +1.571R vs +0.860R (+0.711R, CI `[+0.543R,+0.887R]`)**, n_conditioned=340 (≫ the 30-trade
floor). Both clear the pre-registered gate; `RESOLVED`. This is new payability/cost-geometry
evidence at an admissible venue (Tradeify), on `ORB-MNQ-1` **as a standalone leg** (not an overlay
inside a combined book, the class of evidence the Aegis-6J1 addenda above concerned) — on point
for this document's own re-entry clause.

**Disclosed caveat, must be read before acting on the headline figures above:** this run's own
unconditioned-population summary stats are computed on `MNQ_M15.csv` (2020-07→2026-07, 1,548 RTH
sessions), a ~300-day-shorter, more-recent-starting panel than this pursuit's own original G8
admission pipeline used (`orb_mnq_2026-07/RESULTS.md`'s own cited "2019-05-06→present," 1,857
sessions) — a newly-disclosed panel-vintage drift, not previously flagged anywhere in this
document. The conditioned-vs-unconditioned comparison itself is unaffected (both legs measured on
the identical panel); the absolute figures are a fresh measurement, not a byte-for-byte
reproduction of this pursuit's own originally-published numbers. Full account:
[`rangecond_1_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.md).

**Re-entry / re-scoping this pursuit around a conditioned-entry framing, if warranted, is an
operator call, not made here** — same discipline this document's own prior addenda apply. This
closure's own INTEGRATE routing names (does not authorize) a full Tradeify re-MC on the
conditioned trade population as the natural next step, needing its own operator GO, fresh K
declaration, and an explicit panel-vintage standardization decision (the observed-sample split
above used the current canonical panel; a re-MC should not silently blend panel vintages). $0
spend, `K_intrinsic=1` disclosure only, nothing armed.

---

## ⚠ Addendum RETRACTED 2026-08-31 — the payability evidence above does not hold

The `RESOLVED` finding this addendum reported (conditioned WR 66.47% vs. unconditioned 41.72%,
+24.75pp) was computed against a look-ahead-defective overnight-range conditioner
(`data_lib.py::overnight_ohlc` silently included bars from *after* the outcome it was meant to
predict — found in Codex's [PR #227](https://github.com/Joshua-Asante/first-passage/pull/227)
review, independently re-verified and quantified 2026-08-31). Corrected, the effect vanishes
entirely: WR diff +0.75pp (CI now includes 0), mean-win diff -0.058R (sign-flipped, CI includes
0). Corrected closure: [`Q-RANGECOND-1-closure-falsified.md`](../briefs/closures/Q-RANGECOND-1-closure-falsified.md).
Full account: [`2026-08-31-mnq-overnight-window-lookahead-defect.md`](../notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md).

**This addendum supplies NO new payability/cost-geometry evidence for this pursuit's own
re-entry clause.** `ORB-MNQ-1` stays `PARKED`, standing unchanged — read the addendum above as
historical record of a since-corrected claim, not as live evidence. No full re-MC is named or
owed from this thread; the re-MC this addendum previously named as a next step is withdrawn along
with the finding that motivated it.

## Addendum 2026-08-31 — recon-v3 DD-reduction candidate measured: FAILS the live gate, supplies no re-entry evidence

`core/strategies/candidates/orb_mnq_recon_v3.pine` — a chart-only DD-reduction research
reconstruction (v1→v7 tuning lineage, parameters diverge from `ORB-MNQ-1`'s own frozen construct;
not the file this document's own body concerns) — got its first account-level bust/pass
measurement: [`lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/RESULTS.md`](../../lab/analysis/orb/orb_mnq_recon_v3_2026-08-31/RESULTS.md).
Result: **FAILS** the live gate (bust ≤5.0% ∧ P(pass) ≥50%,
[prereg v2](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §3) at every
tested k ∈ {1,2,3} — k=1 intraday-honest bust **20.78%**, 4.2× over; k=2 **53.70%**; k=3
**64.11%**. A real ~3.25× improvement over the frozen construct's own 67.67% (T2 ADR, 2026-08-03)
but not close to clearing the ceiling.

**This is not new payability/cost-geometry evidence for this pursuit's own re-entry clause** — it
is a negative result on a distinct, divergent-parameter candidate, not evidence about `ORB-MNQ-1`
itself. `ORB-MNQ-1` stays `PARKED`, standing unchanged. `core/strategies/orb/orb_mnq_CARD.md` now
carries a pointer to `orb_mnq_recon_v3.pine` as the current reference research candidate in this
lineage — explicitly not authorized, not promoted, not cleared for capital. No re-MC, no ADR, no
lifecycle change owed from this thread.
