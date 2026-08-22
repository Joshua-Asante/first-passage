# SPEC: GROW lane — generate→refine→confirm strategy growth with two-ledger K accounting

Status: PROPOSED · 2026-08-22 · authorizes nothing ($0 · K=0; ratification = ADR carrying
decision points D1–D3 + operator GO) · depends:
[TNEC-1](2026-08-08-tradeify-necessary-conditions-target-spec.md) `RATIFIED` ·
[Route B ADR](../adr/2026-08-05-avenue-a-generate-confirm-route.md) `Accepted` ·
[S6](2026-08-07-loop-s6-k-aware-generation-spec.md) `CODE_LANDED` ·
[F3 attestation-library spec](2026-08-22-eval-lock-geometry-attestation-library-spec.md)
`PROPOSED` (pooled-scoring dependency) · sibling:
[dense-1m lane](2026-08-09-dense1m-entry-mechanism-lane-spec.md) (paused; unchanged)

Objective: stand up a search topology in which candidates are **grown** — arbitrarily wide
mutation/refinement on frozen EXPLORATION windows at zero confirm-spend — and only **M ≤ 3
lineage survivors per campaign** ever consult a sealed CONFIRM segment, so the DSR/Cap wall
is paid at M, not at generation width.

Origin: operator thesis 2026-08-22 (session record) — Striker/Aegis were filtered and sized
into profitability from seeds that would not have passed intake raw; the one-shot
generate→gate topology (2026 record: ~40 FALSIFIED/zero-yield closures, no promotions)
tests seeds, not the refinement process that historically produced the book. This lane
makes that thesis falsifiable instead of assumed: its own Gate can kill it at $0.

## Ratification decision points (each an S5-style bounded amendment — exactly this, no wider)

- **D1 — grammar replaces catalogue (this lane only).** Route B G0's hard rule "the
  catalogue and windows do not grow" is amended for GROW campaigns: the frozen object is an
  **operator grammar** — enumerated mutation-operator families (entry/filter conditions,
  exit/stop geometry, sizing policy) with parameter ranges, a generation budget, and a
  selection rule — committed at G0 and immutable mid-campaign. New operator family = new
  campaign. Window discipline unchanged.
- **D2 — two-ledger K.** For GROW candidates, `K_select` (variants examined explore-side;
  unbounded; **disclosure-only**, logged per lineage in the campaign manifest) is split from
  `K_confirm` (sealed-segment consultations; = confirm-budget **M ≤ 3**, frozen at G0).
  TNEC-1 N-EDGE `DSR ≥ floor_at_k` and the S6 Cap-wall arithmetic evaluate at `K_confirm`;
  per-candidate confirm bars are Holm-adjusted for M per Route B C0. EM0's catalogue ≤ 3 is
  preserved as M ≤ 3. `K_select` is quoted in every RESULTS/closure — never hidden. The
  statistical claim underneath D2 (selection the sealed segment never saw deflates only
  through M) is **not assumed**: GROW-0 Limb B tests it and can falsify the lane.
- **D3 — bounded graveyard addback (GROW-1 only).** Rescue seeds are enumerated at PREREG
  from closed candidates; a rescued lineage is scored **exclusively** on a sealed segment
  disjoint from every window its original campaign scored — for seeds whose campaigns
  reserved CONFIRM windows still unread (CON-2…5, Q-OFCHAN-1, Q-R2FLOW-1 class), the D3
  exception licenses reading that reserved window **once**, at the M-adjusted bar,
  notwithstanding the closure's own "CONFIRM unread" STOP line — enumerated seeds only.
  Seeds with neither an unread reserved window nor an unscored terminal slice take a
  forward-accruing segment (scored once at its PREREG'd length) or are excluded. A rescued
  artifact is a **new lineage ID** entering `SURVIVAL-ONLY`; the original registry row,
  DEAD-list entry, and re-proposal bar stay intact (nothing is un-rejected); a failed
  rescue re-DEAD-lists under this lane's own bar. Seeds whose closure names re-entry armor
  this cohort cannot satisfy (e.g. Q-TXG-1's different-loss-side-shape / venue-class
  clause) are excluded at enumeration.

Steps:

1. **Rule 0 (implementer, before any build).** Read in full: the Reads list below at its
   anchors — especially Route B's G0 hard rule + C0 M-bar (what D1/D2 amend),
   `prop_survivor_scoring.py` + the 2026-07-13 survivor-scoring prereg (the frozen gate the
   fitness function embeds), and the dense-1m spec's two reader-intercepts (the two lane
   failure modes this spec inherits repairs for).
2. **CC drafts the ratifying ADR** carrying D1–D3 verbatim, full §0–§7 tier (amends
   doctrine), Supersedes-in-part lines against the Route B ADR (D1, D2) and
   `rejected_candidates.md` governance (D3). Operator ratifies or strikes each decision
   point independently — D3 struck still leaves a lane (GROW-1 becomes fresh-generation
   only, renumbered).
3. **GROW-0 — synthetic non-vacuity + accounting-validity harness** (Cursor builds from
   this spec after ADR Accept; $0 data; blocks everything downstream):
   - **Limb A (power):** a planted DGP with net-positive intraday edge above the Req-5
     cost floor, embedded in realistic noise; the loop must recover it on EXPLORATION and
     its survivor must clear the sealed synthetic segment at the M-adjusted bar.
   - **Limb B (calibration — D2 under test):** ≥ 20 pure-noise panels (magnitude-matched
     surrogates, Q-NSURV-2 wrapper pattern); the full pipeline runs on each; the fraction
     of panels whose promoted survivors clear the sealed-segment bar must sit at or below
     the frozen adjusted-α binomial envelope (exact α, panel count, and envelope frozen in
     GROW-0's PREREG before build). Excess clears = leakage ⇒ D2 unsound as implemented.
   - **RED-first** (F3/W1 precedent): rig a leaking pipeline and a powerless loop; watch
     Limb B fail and Limb A fail respectively before trusting either green.
4. **Engine.** Extend `lab/discovery/stage24_runner.py` with the refine loop; fitness is a
   frozen composite scored on EXPLORATION only — hard constraints N-ACT and N-SHAPE
   (flat-by-16:00 ET, no pyramiding, micro-expressible, deployable integer sizing);
   objective = `prop_survivor_scoring` intraday-honest bust + P(pass) at Req-5 costs
   ($0.91/side Tradeify actual; $0.95 screen) + net-of-cost expectancy. Sizing-policy
   operators include flat and cushion-proportional (bust-elimination measured 20.18% → 0.00%
   at Q-EVALSEQ-1; EOD-clock fragility per Q-POLFRONT-1 — intraday-honest scoring is the
   lane default and **no fitness term may read an EOD-clock metric**). Eval-geometry
   patching through the F3 library (`lab/research_utils/eval_lock_geometry.py`) once
   landed; until then the attested per-worker pattern inline. `universe_gate`/DSR calls
   keep module default `var_trials = 1/n`.
5. **Partition per campaign PREREG.** EXPLORATION windows (refinement + loop-internal
   validation splits — still explore-side) · sealed CONFIRM segment (exact dates frozen at
   G0; disjoint from all EXPLORATION windows and, for GROW-1, from every seed's originally
   scored windows per D3). One consultation per survivor, ledgered in the campaign
   manifest; a burned segment is never re-cut for a successor campaign — fresh holdout or
   fresh instrument.
6. **Door checks per campaign (dense-1m step-1a pattern — executed, not remembered).**
   `python scripts/instrument_profiles.py cell <SYM> <mechanism-family>` output pasted into
   the campaign PREREG §0 with every `BINDING BAR` answered by route — for index-intraday
   OHLCV directional cells the default declared route is ③ beats-incumbent-ORB-MNQ
   net-of-cost, which the fitness function already scores; grammar mechanism families are
   declared in `MECHANISMS.md` at PREREG (the CLI hard-fails unknowns). Dedup attestation
   against `rejected_candidates.md` + instrument DEAD lists for generated lineages; GROW-1
   seeds instead disclose their registry row and the D3 exception covering them.
7. **Campaign order** (each under its own Q-ID `Q-GROW-<n>`, frozen PREREG committed
   strictly before any score, operator explore GO; cache-reuse only — any Databento pull
   takes its own cost dry-run + separate GO): GROW-0 synthetic → GROW-1 graveyard rescue
   (D3 cohort) → GROW-2 fresh blind generation. No campaign opens while its predecessor's
   verdict is unfiled.
8. **Survivor routing unchanged.** Close with the TNEC-1 verdict string
   `N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)`; an N-clear routes
   to operator GO → (post-M1, post-S4) S5 sandbox admission. The lane creates no deploy
   path, no Pine, no arming, no `LEG_MAP` claim. Survivors enter the authorization axis
   `SURVIVAL-ONLY` (lifecycle-owner default for unexplained discovery-stack signals):
   smaller start / faster review / tighter trigger.
9. **Lane stop-rule** (2026-08-16 amended form, inherited): 3 consecutive
   FALSIFIED-or-zero-yield campaigns → lane-review packet to the operator, never a 4th by
   default; a close resets the streak only if it yields an admitted candidate.

Gate: RESOLVED if GROW-0 passes both limbs (A: planted edge recovered ∧ sealed-clear at the
M-adjusted bar; B: noise-panel sealed-clear rate ≤ its frozen binomial envelope) with the
RED-first controls on record — resolving the **spec** (machinery + accounting sound);
GROW-1+ verdicts belong to their own PREREGs. FALSIFIED if Limb B exceeds its envelope (D2
unsound as implemented — lane dead pending a redesign ADR), if any sealed segment is
consulted outside the ledger, or if the loop runs on real panels before GROW-0 resolves.
Boundary (each genuinely tempting): no fitness term on any EOD-clock metric · no second
consultation of a burned segment "to sanity-check" · no grammar additions or M growth after
G0 — new campaign, always · no θ-retune claims on LOCKED-book parameters and no Striker-leg
redeploy (rescued Striker-descended lineages are research artifacts under new IDs) · no
un-rejecting registry rows (D3 leaves the original row + bar intact) · no reading GROW
survivors as deployable without the full TNEC-1 → operator GO → S5 chain · no Databento
spend in GROW-0/GROW-1 beyond existing caches.
Reads (verified 2026-08-22 at branch HEAD `6377a28`): TNEC-1 @ `85a83ba` ·
[Route B checklist](../methodology/avenue_a_generate_confirm.md) (G0 hard rule + C0 M-bar)
· S6 spec @ `85a83ba` (explore-free/confirm-spends; Cap crosses at K=4) ·
`lab/discovery/register_search.py` @ `4028be7` (blind lane; `--prereg` binding) ·
`lab/discovery/stage24_runner.py` + `prop_survivor_scoring.py` + `k_count.py` @ `85a83ba` ·
[survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
@ `85a83ba` (frozen gate: intraday-honest bust ≤ 3.0% ∧ P(pass) ≥ 50%) ·
`docs/rejected_candidates.md` @ `85a83ba` (re-proposal rule + per-row addback conditions) ·
`docs/methodology/strategy_lifecycle.md` @ `fc95425` (`SURVIVAL-ONLY` default for
discovery-stack signals) · dense-1m lane spec (step-1a door-check + amended stop-rule) ·
F3 spec (attested patching) ·
[Q-EVALSEQ-1 closure](../briefs/closures/Q-EVALSEQ-1-closure-falsified.md) (cushion-sizing
bust finding) ·
[Q-POLFRONT-1 closure](../briefs/closures/Q-POLFRONT-1-closure-resolved-quantified.md)
(EOD-clock fragility) ·
[Q-NSURV-2 closure](../briefs/closures/Q-NSURV-2-closure-resolved.md) (magnitude-resampling
wrapper) · `lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md` (Cap wall)
Verify (Phase-0, implementer runs before build): `rg -n "do not grow"
docs/methodology/avenue_a_generate_confirm.md` (expect the G0 hard rule D1 amends) ·
`rg -n "def floor_at_k" lab/research_utils/axis_screen.py` ·
`python scripts/instrument_profiles.py cell MNQ orb-open-drive 2>&1 | head -3` (expect
`BINDING BAR` or unknown-mechanism FATAL — proves the door check executes) ·
`ls lab/research_utils/attested_patch.py` (F3 pending — inline attested pattern until it
lands)
Owner: TNEC-1 §2 intake (second construct lane beside dense-1m); the step-2 ADR becomes the
lane's doctrine owner on Accept; campaigns dock under `Q-GROW-<n>`.
