# Head of Research — Decision Log

Append-only. One entry per review. See
[design spec §5.2](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) for this
persona's definition and [`INDEX.md`](INDEX.md) for the roster.

**First-ever entry** — no prior log existed; stated explicitly rather than fabricating history.

## 2026-08-19 — Operator strategy session: "find a breakthrough in improving our research process for generating a viable strategy for Tradeify"

**Type:** Domain-owner strategic briefing, not a strict-D2 STRATEGIC-tier Delete review (this
persona's usual independence-rule trigger). Convened directly by the operator across this seat's
whole domain (a3 + a4), using today's Research Analyst near-miss as the opening case study.
Full minutes delivered in-session; this entry is the compressed record.

**Reviewed:** `lab/analysis/c1/research-analyst-mnq-atomic-facts-2026-08-19/DRAFT_INSTRUMENT_PROFILE.md`
(post-correction) + `ops/instruments/MNQ.md` + `docs/pursuits/a3-mnq-discovery-pipeline.md` +
`docs/pursuits/a4-harvest-external-mechanism-intake.md` + `docs/rejected_candidates.md` domain-level
SNAG/tail-exhaustion closures (~L653-800) + `docs/adr/2026-07-15-external-mechanism-harvest-intake.md`
(incl. R10 addendum, running count 0/2) + `docs/briefs/closures/Q-INVENTORY-1-closure-falsified.md` +
`docs/briefs/closures/Q-EVALSEQ-1-closure-falsified.md` + `docs/briefs/closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md`.

**Verdict:** No Delete/Graduate ratification requested or given — this was a "what's the real
blocker and is there a breakthrough" judgment call, not a gate on a specific artifact.

**Confirmed findings:**
1. The Research Analyst near-miss is a corpus-fragmentation failure (dedup surfaces are
   hand-enumerated, not mechanically complete), not an isolated ledger-miss — root-cause fix
   (ledger in mandatory reads + dedup corpus expansion) is necessary but only partially sufficient;
   the same class of gap (e.g. `docs/rejected_candidates.md`'s ORB-MNQ-1 row, which the draft's own
   B5 flags as carrying "no dedup-machinery tag — must be checked by hand") remains live elsewhere.
2. The standing atomic-fact synthesis function is real but secondary value (compression/legibility,
   consistent with this seat's own prior read of load-bearing-vs-ceremonial work) — it cannot
   manufacture edge that doesn't exist in the underlying research and should not be read as a
   breakthrough lever in itself.
3. The real blocker to a payable Tradeify strategy is not construct scarcity or K-budget — it is
   venue-specific DD/cost geometry colliding with static (not state-dependent) sizing on the one
   construct (`ORB-MNQ-1`) that already clears cost-law/DSR/cross-firm robustness. Both signal-search
   axes (a3 mining: SNAG-closed + tail-exhaustion-raised; a4 harvest: exhaustive 22-search burst,
   zero admissions, accept-idle recorded 2026-07-17) are exhausted or idle on their own terms.
4. Candidate breakthrough: reopen `Q-POLFRONT-1` (commissioned by Q-EVALSEQ-1's surviving finding —
   cushion-proportional sizing eliminated trailing-DD bust 20.18%→0.00% on the locked 2-leg book at
   1.06pt pass-prob cost, framed candidate-independent / N-SURV admissible-region widening) targeted
   explicitly at `ORB-MNQ-1`, gated on (a) the intraday-honest engine, not EOD-clock, and (b) a
   first-step skew measurement on `ORB-MNQ-1`'s own loss tail per Q-GEOFIT-1's skew-governs-survival
   finding, before assuming the locked book's favorable-skew result transfers.

**Evidence-Cited:** see Reviewed list above; full citation chain in the delivered minutes, not
restated here.

**Deviation-from-Precedent:** n/a — first entry.

**Ratified as recommended:** Pending — this is an independent recommendation surfaced to the
operator/CIO; opening `Q-POLFRONT-1` needs its own brief + operator GO per Q-EVALSEQ-1's own stop
rule, not a ratification of this log entry.

---

## 2026-08-20 — Addendum: the (a)/(b) pre-checks ran; findings materially refine (not confirm) the above

The operator ran both gating pre-checks named in finding 4 above, then two further rounds of
follow-on verification (each independently, adversarially checked — three full rounds total). This
addendum records the outcome so this log entry doesn't stand as-is once the record has moved past
it — the recommendation above is superseded in its specifics, not in its overall direction.

**Verdict:** Finding 4 of the 2026-08-19 entry is superseded in its specifics (literal `Q-POLFRONT-1`
reopen is not the right action) but confirmed in its overall direction (the lever is real; a sibling
Q now carries the remaining question forward).

**Confirmed findings:** see "What held" / "What changed" below.

**What held:** finding 3 (the real blocker is venue-specific DD/cost geometry colliding with static
sizing on `ORB-MNQ-1`) is now *more* substantiated, not less — cushion-proportional sizing does
eliminate `ORB-MNQ-1`'s trailing-DD bust, intraday-honestly (not just on the EOD clock finding 4(a)
flagged as a risk), and this is mathematically derivable and regime-agnostic (verified true across
every time slice and volatility bucket tested).

**What changed:** (i) applying the lever to the *original* `Q-EVALSEQ-1` 2-leg pyramided book (the
literal reading of finding 4) proved `NOT-REACHABLE-AT-$0` — no per-day intraday-excursion data
exists for that book, and reconstructing it needs real engineering (position-ladder reconstruction
across two pyramided, cross-instrument legs), correctly declined rather than faked. (ii) `ORB-MNQ-1`'s
own skew (finding 4(b)'s own-stated precondition) measured at +2.09, ~42% weaker than the book the
original 20.18pt headline came from — directionally supportive but not a full-magnitude transfer.
(iii) Once tested directly on `ORB-MNQ-1`'s own already-intraday-honest engine, bust-elimination held
but pass-rate improvement turned out sharply regime-dependent — a real, triple-verified, non-boundary-luck
break at ~2021-09-28 (bad before, clears the frozen re-`PARK` ADR's own gate after), but a trailing-
volatility mechanism test for *why* was **REFUTED** (window-unstable, no clean date-correlation).

**Corrected recommendation:** not "reopen `Q-POLFRONT-1`" as literally stated in finding 4 —
**`Q-POLFRONT-1` is not unopened; it closed `RESOLVED-QUANTIFIED` 2026-08-16, with a 2026-08-17
addendum finding its own 5.1× headline does not survive intraday-honest remeasurement** (a same-day
correction to this addendum's own first draft, which repeated the "unopened" error — see
`docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md` §2 for the full correction). What finding 4
actually pointed at and this probe found `NOT-REACHABLE-AT-$0` was a distinct, never-formally-opened
literal re-derivation of `Q-EVALSEQ-1`'s own result on the real 2-leg book — not `Q-POLFRONT-1`
itself. Instead: **`Q-ORBCUSH-1`** (`docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md`, sibling
to `Q-POLFRONT-1`, not a replacement) is now drafted and pre-registered, scoped narrowly to the one
remaining falsifiable question — does a trailing edge (mean-R) or cost-fraction classifier explain the
2021-09-28 break — before any deployment-adjacent decision treats that break as more than an
unexplained historical pattern. Named, not opened; needs its own operator GO for Phase 1, same
convention as every other Q in the roster.

**Evidence-Cited:** `lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/` (three independently-
verified probe rounds) + `docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md` + `docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md`.

**Deviation-from-Precedent:** refines finding 4 of this persona's own first entry, same day —
recorded as an addendum per this log's append-only convention, not an edit to the original entry.

**Ratified as recommended:** Pending — `Q-ORBCUSH-1` is named, not opened; Phase 1 needs a fresh
operator GO.
