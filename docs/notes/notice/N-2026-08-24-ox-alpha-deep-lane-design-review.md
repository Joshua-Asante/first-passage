# NOTICE 2026-08-24 — ox-alpha sanitized review: deep-iteration lane design (what was missed/overlooked)

**Notice ID:** N-2026-08-24-ox-alpha-deep-lane-design-review
**Observed:** 2026-08-24
**Author:** Claude Code (Fable 5), operator direction ("reflecting on the deep iteration lever,
what may we have missed or overlooked about its implementation? ... judge it yourself, and pose
this question to ox-alpha")
**Type:** Notice-phase. External adversarial-lens review, reconciled against real repo state.
$0 · K=0 · no camp · no card. No live-risk surface touched.
**Status:** `RESOLVED` — reconciliation complete; several objections survive (two genuinely new),
several are refuted by the charter's own text, several converge with this session's own
independent judgment (delivered in-chat before the external response was read).

---

## §0 — Governance basis

Sent under [`docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)
§2's **base scope** (adversarial lens on a chartered channel's design/methodology — a
decision-authoring artifact class), at explicit operator direction. Not the candidate-generation
extension; no mechanism ideas were requested and the response's occasional design *proposals*
(group-sequential reads, novelty relaxation) are recorded as candidate governance input only,
never adopted here.

**Sanitization applied:** no firm name, instrument ticker, dollar figure, campaign codename
(DL-1/DL-2/GROW-0), K constants beyond generic ranges ("low tens"), or repo/date identifiers.
The A2-vs-design-box tension was included as neutral facts (a feasibility study's win-rate
findings vs. the channel's chartered envelope) without this session's own inference, as a clean
test of independent detection — the lens caught it and escalated it to its top-line synthesis.
Prompt: `ox_alpha_deep_lane_prompt.txt` (scratchpad, not committed).

**Send/receive record:** `stealth/ox-alpha` via OpenRouter chat-completions, 2026-08-24.
prompt_tokens=980 / completion_tokens=13,749 / content 11,403 chars. finish_reason=stop, one
attempt, ~8.4 min. No transcript of the hidden-reasoning channel stored in-repo (standing bar).

**Sequencing note:** this session's own six-finding judgment (delivered in-chat) was authored
and verified against repo sources *before* the external response was read — the convergences
below are independent, not echoes.

---

## §1 — Reconciliation table

| # | ox-alpha objection | Real repo state (verified this session) | Survives? |
|---|---|---|---|
| 1 | "The design never verified that its own constraints are jointly satisfiable" — no satisfiability check at charter/nomination time; K-deflated floor + power ≥0.5 may be arithmetically unsatisfiable for whole campaign classes. | The charter's §2.2 conjunct (iii) IS this check, as a **refusal rule at freeze**: "A prereg whose own target edge cannot clear its own floor at ≥ 0.50 power is refused, not disclosed-and-waved-through," with a worked example (target 1.83, K=33, 6.5y → floor 1.475, power ≈0.82). The lens also assumed Bonferroni z-arithmetic (~2.8σ); the repo's floor is DSR-based (`floor_at_k`, SR units, se≈1/√years). | **No** — refuted in its literal form. The residue (power is computed against a *random* variant's named target, not the argmax-*selected* one) survives under row 3. |
| 2 | **Power 0.5 and the two-strike falsifier are jointly reckless:** at the design's own POWER_MIN, two consecutive true-premise campaigns still both miss with probability 0.25 — the falsifier has up to a 25% false-falsification rate at its own admissible floor. | Verified: `POWER_MIN = 0.50` is a binding refusal floor (§2.2(iii)); §4's yield limb ("2 consecutive... fails the confirm read") carries **no power-conditioning**. GO-2 set the first campaign at power ≈0.93 (P(two misses)≈0.005), but nothing prevents boundary-admissible 0.5-power campaigns from feeding the same two-strike counter. | **Yes — genuinely new.** Neither the charter, the audit, nor this session's own six findings had computed this coupling. The falsifier's error rate is a function of per-campaign power and the charter treats them as independent. |
| 3 | Selection-adjusted (winner's-curse) power never computed — declared power is for a random variant; the argmax nominee's true effect is shrunk, so real detection odds are below declared. | Verified: §2.2(iii) power is "against the campaign's design-target edge, named a priori"; nomination is strict argmax-on-train (§2.3); GROW-0's calibration planted SR=4.0 (Limb A, confirm-clear ≈1.0 by design) and a pure null (Limb B) — no marginal-effect condition, so neither nomination accuracy nor selection-shrunk power was ever measured. | **Yes** — convergent with this session's findings #4/#5, with a cleaner mechanism statement. |
| 4 | Multiplicity mispriced both directions: within-campaign K-deflation ignores variant correlation (effective K ≪ K — floor overpays in power); across campaigns, no channel-level alpha budget and the family-*selection* search is unbounded/uncorrected. | Within-campaign: charging full K on correlated variants is **deliberate ratified doctrine** (family-K ADR: "a grid pays in full") — a chosen conservatism, though its power cost compounds row 2/3 and was never priced into a composite. Cross-campaign: §2.2(iv) discloses confirm-window consultations but no channel-level alpha exists, and nothing anywhere prices *which-family-gets-a-campaign* selection. | **Partial** — the within-campaign half is a ruled election, not an oversight; the cross-campaign/family-selection half **survives** (sharper form of this session's finding #7). |
| 5 | The falsifier conflates heterogeneous failure modes, and the half-split fragility control *feeds* it: a pooled-pass/half-fail survivor accrues a strike toward falsifying a premise the pooled evidence supported. | **Verified against §4's verbatim text this session:** the yield limb counts "fails the confirm read **(or passes confirm and then fails N-SURV)**" — so (a) `FALSIFIED-FRAGILE` (pooled-pass, half-fail, §2.4) is a confirm-read failure and plausibly strikes; (b) even a post-confirm **N-SURV/venue-shape death strikes** — meaning envelope-vs-venue incompatibility (see the design-box reconciliation, in flight) can falsify the *depth* premise. Rough illustration, not asserted as measurement: a true edge near the floor with per-half se ≈ 0.55 SR has material odds of failing one half by chance alone. | **Yes** — and the verification made it *stronger* than the objection as sent. The falsifier cannot distinguish "depth finds no edges" from "the envelope was aimed at a venue-infeasible region" or "the fragility control fired on noise." Exact rates owed to a GROW-0-style computation (row 8), not asserted here. |
| 6 | Train-stage abandonment decisions have no specified treatment of sampling error; unstated whether train scoring is net of stop-slippage. | **Largely refuted by the §4 running-count record:** DL-1/DL-2's train gates included **SPA consistent-p (gate 2b, vs ≤0.10 over the full variant universe)** — a sampling-error-aware multiplicity test — and **M-16 +1-tick slippage-stressed re-scoring (gate 2d)**. The abandonments were not naked point estimates. | **No** in its stated form. The residue — the abandonment battery's *false-abandonment rate* under a marginal true edge was never calibrated (GROW-0 gap) — survives under rows 3/8. |
| 7 | No purge/embargo at the train/holdout seam — trades opened in train closing in holdout leak across the partition. | Checked against the construct class: every lane-eligible construct is intraday force-flat (hard stop, k=1, session-bounded; both real campaigns force-flat EOD) — no position spans the seam; lookback features crossing the boundary are ordinary walk-forward, not label leakage. Purge/embargo bites on overlapping-label designs this lane doesn't currently run. | **No, at current materiality** — worth a standing one-line disclosure in preregs (and it becomes real if a future family holds overnight), not a live defect. |
| 8 | Synthetic validation validated the arithmetic, not the world model — a cheap pre-flight (daily range vs stop+target span) would have caught campaign 2's death for free. | Convergent with this session's finding #4. The specific prescription **already landed** post-DL-2: the geometric-feasibility gate is armed via DL-2's Iterate packet (supply audit, belt add (c)). The wider gap — GROW-0 never characterized the abandonment branch or composite operating characteristics at realistic effect sizes — stands. | **Convergent** — prescription already implemented reactively; the calibration gap survives as the named GROW-0 "Limb C" follow-up. |
| 9 | The consultation ledger is "caution theater" — disclosure without teeth; and tacit exposure (researcher memory of the holdout era, old-era out-of-regime data) is contamination no ledger sees. | Disclosure-only was a **deliberate, same-session-ratified election** (two-ledger K ADR, explicitly mirroring family-K's disclosure-not-gate shape) — an opinion against a ruled disposition, not an overlooked defect. The tacit-exposure point is real, acknowledged, and structurally un-modelable. | **No** on the "theater" charge (ruled); the tacit-exposure residue is recorded as an acknowledged, unpriceable limitation. |
| 10 | Ideation is ungoverned — no ex-ante screen for economic rationale/crowding/capacity on which family earns a campaign; family selection optimizes governance-cleanliness. | Family selection IS screened (registry re-proposal bars, standing-pause attestation, cost-law, `instrument_profiles` cell consult) — but for *governance admissibility*, not *edge plausibility*. The supply audit's own Q6 found exactly this: DL-2's family chosen on "clean governance door + cheapest RT," then died on the unscreened dimension. | **Partial/convergent** — the audit had already named the worked instance; the general statement (the channel governs confirmation meticulously and ideation only for admissibility) survives. |
| 11 | (b)-table synthesis: every protection is positioned downstream of a stage the channel cannot reliably reach; the two actual killers had no protection until patched ad hoc. | Matches the record: both deaths pre-confirm; all funded machinery guards the confirm read. Convergent with this session's finding #2 ("the apparatus prices the wrong risk"), independently derived on both sides. | **Yes — convergent.** |
| 12 | Historical diagnosis mismatch: the old book failed out-of-regime; the design responded with multiplicity controls plus one frozen window — "regime disease treated with multiplicity medicine." | Partially unfair as stated: §2.4's half-split is explicitly aimed at the regime lesson ("the CFD lesson, priced"). But one split of one window is a thin dose, and per row 5 its strictness feeds the falsifier rather than informing it. | **Partial** — the charter did aim a control at the disease; adequacy-of-dose is a fair open question. |
| 13 | (c): the record indicts the *search space*, not the search discipline — the envelope was inherited from an earlier spec and never re-derived; repeated train-emptiness is Bayesian evidence against the envelope; the charter has no branch for the audit's own "space is empty" outcome ("dead-end governance"). | All three verified: the design box predates and was never reconciled against the A2 map (the reconciliation run is now in flight, operator-GO'd this session); §4 has inertness/yield/abandonment limbs but **no branch consuming the supply audit's AMBIGUOUS/empty-intersection outcome** — its re-test conditions dangle with no mandated consequence. Convergent with this session's findings #1/#3. | **Yes — convergent**, with "no charter branch for the audit outcome" a sharper formulation than this session's own. |
| 14 | (d): stacked conservatisms (K-deflation × winner's-curse × half-split × power floor) have an undeclared composite acceptance probability — "the channel may be structurally incapable of accepting anything." | Verified that no composite operating characteristic has ever been computed (GROW-0's Limb A at SR=4.0 gives ≈1.0, uninformative at realistic effects). This is computable with existing tooling. | **Yes** — and it names the concrete follow-up: extend GROW-0 with a marginal-effect condition and report P(accept \| true edge at design-box-realistic size) through the full gate stack. |
| 15 | (d)6: the post-abandonment integrity audit "was the wrong instrument... certified compliance precisely when the failure was aim." | **Refuted:** the 2026-08-23 audit was operator-scoped as a *supply-side* audit and its §3.5 is precisely the aim diagnosis — it found the empty triple-intersection. The lens under-modeled the audit from the sanitized summary. | **No.** |
| 16 | (d)2/(d)4/(c)-proposals: group-sequential holdout reads with alpha-spending; permit per-variant holdout computation for learning; relax "genuinely new" to novel-combination. | Each contradicts a deliberate standing doctrine (single-read discipline; per-variant holdout ban; novelty bars). They are coherent alternative designs, not detected defects. | **Recorded as candidate governance input only** — operator elections if ever taken up; adopting any needs its own ADR, not this notice. |

## §2 — What survives, net

**Two genuinely new findings** (neither in this session's own independent six, both verified
against charter text before logging):

1. **The falsifier's error rate is coupled to per-campaign power and the charter treats them as
   independent** (row 2): at the admissible POWER_MIN=0.50 floor, two true-premise campaigns
   falsify the lane with probability up to ~0.25. Any future campaign prereg at boundary power
   should carry this number; alternatively the yield limb could be made power-conditioned — an
   operator call, flagged not made.
2. **The composite acceptance probability through the full stacked gate set has never been
   computed** (row 14) — concrete, cheap follow-up: a GROW-0 "Limb C" run planting effects at
   design-box-realistic sizes and reporting end-to-end P(accept | true edge), which would also
   discharge rows 3/6-residue (false-abandonment rate, nomination accuracy) in the same harness.

**Verified-stronger during reconciliation** (row 5): §4's yield limb counts post-confirm N-SURV
deaths and (plausibly, per §2.4's own language) `FALSIFIED-FRAGILE` half-split deaths as strikes —
so venue-shape incompatibility or fragility-control noise can falsify the *depth* premise. This
compounds the design-box question now being measured (reconciliation workflow in flight).

**Convergent with this session's own findings** (rows 3, 8, 11, 13): apparatus-prices-the-wrong-
risk, GROW-0's uncalibrated abandonment branch, starvation-not-falsification, and
change-the-WHAT/envelope-never-re-derived — independently reached on both sides.

**Refuted / already ruled** (rows 1, 6, 7, 9-in-part, 15): the satisfiability check exists
(conjunct (iii)); the train gates carried SPA + slippage stress; purge/embargo is immaterial for
force-flat intraday constructs; disclosure-only ledger was a ruled election; the audit did
diagnose aim. These refutations are themselves useful — three of them exist only because the
sanitized prompt could not carry the charter's full text, and the lens filled gaps adversarially,
as designed.

**Since this Use produced multiple objections that survive reconciliation, revert trigger (b)
(three consecutive zero-value uses) does not tick.**

## §3 — What this does NOT license

- No charter amendment, no falsifier redesign, no GROW-0 Limb C run, no lane continuation or
  termination — every action item above is flagged for operator election, not taken.
- Does not pre-judge the design-box vs A2 reconciliation (in flight as its own reviewed
  workflow); row 5's consequence becomes concrete only if that measurement lands adverse.
- Row 16's alternative designs carry zero authority (parent ADR §2/§5).

## §10 — Audit hooks (runnable)

```bash
# Conjunct (iii) refusal rule exists (row 1 refutation)
grep -n "refused, not disclosed-and-waved-through" docs/adr/2026-08-16-deep-iteration-lane-charter.md
# POWER_MIN floor + yield limb carry no power-conditioning (row 2)
grep -n "POWER_MIN" docs/adr/2026-08-16-deep-iteration-lane-charter.md
grep -n "passes confirm and then fails N-SURV" docs/adr/2026-08-16-deep-iteration-lane-charter.md
# Train gates included SPA + slippage stress (row 6 refutation)
grep -n "SPA consistent p\|M-16 \+1-tick" docs/adr/2026-08-16-deep-iteration-lane-charter.md
# GROW-0 planted SR=4.0 / null only — no marginal-effect condition (rows 3/8/14)
grep -n "SR=4.0\|nominal_p0" docs/briefs/closures/GROW-0-closure-resolved.md
# No charter branch consumes the supply audit's outcome (row 13)
grep -n "AMBIGUOUS" docs/adr/2026-08-16-deep-iteration-lane-charter.md   # expect: no §4 branch hit
```

## Verification

```bash
python scripts/check_brief.py docs/notes/notice/N-2026-08-24-ox-alpha-deep-lane-design-review.md --type notice
```
