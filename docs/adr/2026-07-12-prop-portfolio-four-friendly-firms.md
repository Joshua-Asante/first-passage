# ADR 2026-07-12 — Prop-portfolio program: multi-firm ops target the four automation-friendly futures firms

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Retain-until:** none
**Decision date:** 2026-07-12
**Authors:** Joshua (decision) + Cursor Cloud Agent (recorder)
**Supersedes:** `2026-07-10-r6-nogo-futures-residual-disposition.md` in part - R6's locked-book futures-prop fan-out and edge-transfer falsifiers stand; R6's "sole active scale lane = self-funded Aegis->M6J" and "no futures-prop operational target" posture is replaced by this program for multi-firm operations.
**Superseded-in-part-by:** `2026-07-14-prop-portfolio-existing-strategy-candidates.md` - accepted 2026-07-15; candidate-class scoping only (Section 2 R6-boundary sentence + Section 5 bullet 2). Firm set, registry, gating, Section 4 falsifier, and every other clause stand.
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - `ACTIVE_FIRM="FXIFY"` retention/prohibition only. Firm set, registry, envelope scoring, and the §4 falsifier stand.
**Superseded-in-part-by:** `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` - the §4 discharge status only (Class-S candidate #1's 2026-07-15 result withdrawn on corrected eval-lock geometry). Program, four-firm target set, envelope, and the 2026-11-08 hard date stand unchanged.
**Related:** [`docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md`](../ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md) (eligibility survey); [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) (E1–E7 build envelope); [`docs/notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md`](../notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md) (KEEP rail = TV→CrossTrade→NT8); [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) (Gen-2 discover→admit pipeline); [`docs/adr/2026-06-06-firm-constants-single-source.md`](2026-06-06-firm-constants-single-source.md) (`firm_rules` canonical).
**Layer:** execution + portfolio operations — **not** locked-parameter. No change to the locked four-strategy allocations, `dd_protection` constants, Pine source, or FXIFY MC regression pin.

---

## §0 — Rule-0 reads (production-source verification)

- [`docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md`](../ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md) — content-read 2026-07-12. Four `FRIENDLY` firms under attended-automation bar + CrossTrade/NT8 rail: Bulenox, Tradeify, MyFundedFutures, BluSky Trading.
- [`core/firm_rules.py`](../../core/firm_rules.py) — working-tree read 2026-07-12. Bulenox (5 tiers) + Tradeify Select (4 tiers) already encoded; MFFU + BluSky tiers added by this ADR; `ACTIVE_FIRM = "FXIFY"` unchanged (MC anchor pin).
- [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) — content-read 2026-07-12. Default E1–E7 envelope + §4 per-firm overlays for FRIENDLY/CONDITIONAL firms.
- [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) — content-read 2026-07-12. Locked-book fan-out NO-GO + DJ30→MYM falsification — **not reversed** by this ADR.
- [`core/config/params.toml`](../../core/config/params.toml) — HEAD read 2026-07-12. Locked G/DJ30/A/NAS allocations + `dd_protection` C2 unchanged.

---

## §1 — Context

Q-AUTO-FIRM-1 (2026-07-12) resolved that **four** US futures-prop firms clear the **attended-automation** bar on the **TV→CrossTrade→NT8** rail — materially wider than Q-BTC-3's single-firm lights-out result. R6 (2026-07-10) correctly closed the **locked four-strategy book's** futures-prop fan-out after P2/R5 edge-transfer falsification; it also demoted all futures-prop to NO-GO and named self-funded Aegis→M6J the sole active scale lane.

The operator directive (2026-07-12) reframes **multi-firm operations**: not redeploy the falsified locked book, but **discover, productionalize, and execute new portfolio strategies** engineered to **pass prop challenges and scale allocations** across the four automation-friendly firms. Firm targets and constraints must live in `core/firm_rules.py` as the single reference surface (ADR 2026-06-06).

**Decision driver (one sentence):** eligibility evidence + operator intent now justify a **greenfield prop-portfolio program** at four attended-automation firms, with `firm_rules` as the constraint registry — distinct from the R6-falsified locked-book transfer question.

---

## §2 — Decision

**Multi-firm operations targets challenge-passing and post-pass allocation scaling at the four Q-AUTO-FIRM-1 `FRIENDLY` firms:**

| Firm | `firm_rules` family key | Representative eval tiers (this ADR) |
|---|---|---|
| Bulenox | `bulenox` | `Bulenox_25K` … `Bulenox_250K` (pre-existing) |
| Tradeify | `tradeify` | `Tradeify_Select_25K` … `Tradeify_Select_150K` (pre-existing) |
| MyFundedFutures | `myfundedfutures` | `MFFU_Rapid_50K`, `MFFU_Rapid_100K` (added) |
| BluSky Trading | `blusky` | `BluSky_Premium_50K`, `BluSky_Premium_100K` (added) |

**Operational program (end-to-end):**

1. **Discover** — Gen-2 lab pipeline (`lab/` discovery campaigns). Candidates must declare `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` against [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) at closure; portfolio composition is a first-class design target (multi-leg books that pass together, not single-strategy heroics).
2. **Productionalize** — admitted survivors (`CANDIDATE` lifecycle intake per [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md)) through codification → sweep → validation; prop-firm constraints pulled from `firm_rules.FIRM_RULES[<tier>]` + envelope overlays, never hard-coded in research artifacts.
3. **Execute** — attended automation on **TV → CrossTrade → NT8 → Rithmic/Tradovate** per the 2026-07-06 rail note. **Rail build and account registration remain gated** — this ADR sets the *target* and *constraint registry*, not a live-start authorization.

**`firm_rules` registry:** `AUTOMATION_FRIENDLY_PROP_FIRMS` maps each family to its tier keys; all tier dicts carry challenge targets/constraints (profit target, DD type/level, flat posture, contract caps, consistency where applicable). `ACTIVE_FIRM` stays **`FXIFY`** — the 99.83/0.17/4.37 MC anchor remains a historical regression pin, not the live prop target.

**R6 boundary (amended 2026-07-15 — candidate class only):** deploying the **locked** Guardian / Striker DJ30 / Aegis / NAS100 book as a futures-prop fan-out at locked CFD allocations, or on any claim of CFD-edge transfer, is still **NO-GO** (R5/P2 remain FALSIFIED). The program builds prop-envelope portfolios from **either** Gen-2 discovery survivors **or** pre-registered existing-strategy books (native-futures expressions of the locked legs, scored at firm tiers on bust-geometry). Amendment vehicle: [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md).

**Effective:** immediately upon acceptance (2026-07-12).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep R6 posture (self-funded Aegis→M6J sole lane; futures-prop dormant)** | Operator directive explicitly retargets multi-firm ops to prop challenge-passing at the four FRIENDLY firms; leaving R6's ops posture unchanged would orphan Q-AUTO-FIRM-1 and block `firm_rules` as a live constraint surface. |
| **Redeploy the locked four-strategy book to Bulenox/Tradeify** | R6 falsifiers stand (DJ30→MYM 0.559 < 0.8×; NAS100 dead on micros). Firm eligibility ≠ edge-transfer clearance. |
| **Include CONDITIONAL firms (Apex, Topstep, TradeDay, Earn2Trade) in the operational target set** | Q-AUTO-FIRM-1 scored rail mismatch or policy caveats; operator scoped to the four `FRIENDLY` firms only. CONDITIONAL firms remain in envelope §4 for a future expansion ADR. |
| **Skip `firm_rules` encoding; keep constraints only in `prop_envelope_default.md` prose** | Violates ADR 2026-06-06 single-source doctrine; MC/re-MC harnesses and ops tooling need machine-readable tier dicts. |
| **Switch `ACTIVE_FIRM` to a prop firm now** | Would break FXIFY MC anchor byte-reproducibility without a deliberate re-MC + engine pre-flight ADR. Prop tiers are **reference configs**, not the active MC fixture. |

---

## §4 — Falsifier (revert trigger)

**H (program success):** at least one **pre-registered** prop-portfolio candidate (multi-leg or single-leg) achieves **challenge-pass simulation** — bust rate below an operator-pre-registered ceiling on **≥2** of the four `FRIENDLY` firm tiers — under attended-automation + EOD-flat envelope modeling, using `firm_rules` configs, before any live account spend.

**Revert trigger (binary):** by **2026-11-08**, no pre-registered portfolio candidate clears the pass-rate ceiling on **any** `AUTOMATION_FRIENDLY_PROP_FIRMS` tier in a dated lab re-MC → demote this program to **research-only** (firm configs retained as reference; no execution-rail ADR may cite this ADR as live mandate without new pass-rate evidence).

**Secondary trigger (eligibility):** any `FRIENDLY` firm issues a written policy reversal banning attended webhook/EA/semi-auto per Q-AUTO-FIRM-1 §4 falsifier → remove that family from `AUTOMATION_FRIENDLY_PROP_FIRMS` and re-run eligibility for the tier only.

**Revert action:** supersede this ADR; restore R6 sole-lane posture if operator confirms; never edit §2 in place.

**Trigger check schedule:** quarterly — next **2026-08-08**, 2026-11-08 (hard date for primary falsifier), 2027-02-08.

---

## §5 — Forbidden moves (under this ADR)

- **Treating firm eligibility as locked-book edge-transfer clearance** — Q-AUTO-FIRM-1 explicitly forbids this; R6 falsifiers are not vacated.
- **Deploying the locked four-strategy portfolio to prop firms under this ADR at locked CFD allocations, or on any claim of CFD-edge transfer** — still forbidden. A pre-registered book of locked-leg *futures* expressions with per-tier weights is admissible as a scoring candidate per [`2026-07-14-prop-portfolio-existing-strategy-candidates.md`](2026-07-14-prop-portfolio-existing-strategy-candidates.md); locked Pine/SL/TP/ATR and the CFD allocation lock stay immutable.
- **Switching `ACTIVE_FIRM` off FXIFY without a firm-onboarding ADR + re-MC** — breaks engine regression pins.
- **Building the CrossTrade/NT8 rail as an implied consequence of this ADR** — execution rail requires its own gated ADR with parity checklist.
- **Hard-coding firm names or challenge constants in `lab/` research artifacts** — envelope §2 rule; constraints enter via `firm_rules` + §4 overlays at the deployment fork only.
- **Full lights-out / unattended 24h operation** — attended bar only (envelope E6); Q-BTC-3 lights-out framing is superseded for ops targeting, not revived.

---

## §6 — Consequences

**Positive:**
- Single ops target across four firms with a machine-readable constraint registry in `firm_rules`.
- Discover→productionalize→execute path aligned with Gen-2 lab pipeline and prop envelope defaults.
- Clear separation from the R6-falsified locked-book question.

**Negative (real cost):**
- Parallel program surface: prop-portfolio work coexists with parked self-funded lanes until explicitly re-ranked.
- `firm_rules` prop tiers use engine semantics (`trailing`, `trailing_locking`) that require pre-flight before trust-pass re-MC (daily_loss_pct `None` hazard documented in module docstring).
- Rail still unbuilt — program can research and productionalize before execution is possible.

**Downstream artifacts updated by this ADR:**
- `core/firm_rules.py` — `AUTOMATION_FRIENDLY_PROP_FIRMS` + MFFU/BluSky tiers
- `tests/core/test_automation_friendly_prop_firms.py` — registry integrity guard

**Downstream artifacts NOT changed (explicit):**
- `ACTIVE_FIRM`, locked allocations, `dd_protection`, Pine, FXIFY MC pins
- `docs/methodology/strategy_lifecycle.md` go-live gates (rail build still separate)

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified (this session).
- **Phase 1** — `firm_rules.py`: add `AUTOMATION_FRIENDLY_PROP_FIRMS`, MFFU Rapid 50K/100K, BluSky Premium 50K/100K; refresh module provenance docstring.
- **Phase 2** — ADR (this file) + registry test.
- **Phase 3** — audit hooks §10; status `Accepted`.

---

## §10 — Audit hooks

```bash
# ADR accepted + four-firm target
grep -n "Accepted\|AUTOMATION_FRIENDLY_PROP_FIRMS\|FRIENDLY" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md

# Registry: four families, all keys in FIRM_RULES
python -c "
from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES
assert len(AUTOMATION_FRIENDLY_PROP_FIRMS) == 4
for fam, keys in AUTOMATION_FRIENDLY_PROP_FIRMS.items():
    assert keys, fam
    for k in keys:
        assert k in FIRM_RULES, k
print('OK', list(AUTOMATION_FRIENDLY_PROP_FIRMS))
"

# MC anchor pin untouched
python -c "import firm_rules; assert firm_rules.ACTIVE_FIRM == 'FXIFY'"

# Locked constants untouched
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/firm_rules.py | grep -v firm_rules || true
pytest tests/core/test_automation_friendly_prop_firms.py tests/core/test_firm_constants_single_source.py -q
```

**Hook staleness note (2026-07-24).** The "MC anchor pin untouched" hook above
(`assert firm_rules.ACTIVE_FIRM == 'FXIFY'`) **hard-fails as written** since substrate-retirement
Phase 1 (`f8f8db1`, 2026-07-22): `ACTIVE_FIRM` is now `Tradeify_Select_100K` and the historical MC
pin is `FIRM_RULES["FXIFY"]` **by name**, not via the selector. The property the hook was written to
guard is intact — read it as *"the anchor path pins FXIFY by name, not through `ACTIVE_FIRM`."* The
hook line is left unedited so the audit trail of what was originally asserted stays legible. The same
staleness in the **frozen** scoring gate's §10 hook 7 is recorded (and deliberately not edited) in
[`docs/notes/2026-07-24-class-s-scoring-chain-coupling-and-stale-hooks.md`](../notes/2026-07-24-class-s-scoring-chain-coupling-and-stale-hooks.md) §1.

---

## Addendum 2026-08-22 — §4's success/revert dichotomy does not cover an exactly-one-tier clear (PROPOSED)

**Status:** `Proposed` — drafted by Claude Code, awaiting operator (JA) ratification. Not yet
effective; §4's original text (H, revert trigger, both hard-coded below) is unchanged unless and
until this addendum is **`Accepted`**. **Tier: FULL** — ceremony-tiering limb 4 fires (creates a
disposition rule for a falsifier threshold that binds how the 2026-11-08 hard-date verdict is
read); limb 2 arguably also fires (this is the open "sibling fork" to the already-queued F1 item,
STATE.md queue row 1). Ambiguity on limb 2 does not matter — limb 4 alone forces FULL. **Vehicle:**
amend-in-place addendum on this file, per the 2026-08-15 "amend-in-place beats a sibling ADR"
convention ([`ceremony-tiering ADR`](2026-08-08-adr-ceremony-tiering.md) addendum) — this is the
ADR that defines §4 itself, so no sibling ADR is minted. **$0 / K=0.** No live-risk surface, Pine,
allocation, or `dd_protection` constant touched. Structurally modeled on the harvest-intake ADR's
own 2026-08-16 "§4 gains a fourth branch" addendum
([`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](2026-07-15-external-mechanism-harvest-intake.md)) —
same shape of gap, same tightening/completeness-only remedy.

**Operator note (2026-08-23, 12:23):** ratification explicitly deferred, not declined — same posture as
the sibling F1 item (STATE.md queue row 1): deciding this before the exactly-one-tier state
actually occurs would pre-empt §4 on evidence that doesn't exist yet (currently 0-of-4 clearers,
per §0 below). Revisit at trigger time (first tier clearance, or the 2026-11-08 hard date,
whichever comes first). Status stays `Proposed` until then.

⚠ **Superseding note (2026-08-23, 12:59, concurrent session — reconciled on merge, Rule 14
correction-lands-where-read):** F1 itself was ruled 36 minutes after the note above, by explicit,
considered operator election, ahead of trigger time —
[`Addendum 2026-08-23`](2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-08-23--f1-ruled-a-tradeify-resting-discharge-does-not-satisfy-4)
to the 2026-08-04 de-scope ADR. The "same posture as the sibling F1 item" analogy above is now
**historical** — F1 no longer sits at trigger-time deferral. **This addendum's own ratification
is unaffected**: it was deferred on its own merits (§4's own evidentiary-floor logic, independent
of F1's disposition), not solely by analogy to F1, and stays `Proposed` pending trigger time as
written above. Flagged so a future reader does not mistake the stale analogy for a reason to
reopen this addendum's status.

### §0 — Rule 0 reads for this addendum (production-source verification, 2026-08-22)

- This file, §4 (H: "≥2 of the four FRIENDLY firm tiers"; revert trigger: "no pre-registered
  portfolio candidate clears the pass-rate ceiling on **any** ... tier ... by 2026-11-08") —
  anchor `027a729` (2026-08-14, this file's post-transplant seed commit; content unchanged from
  the original 2026-07-12 acceptance and 2026-07-25 header repair).
- [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
  §6 (frozen gate table: RESOLVED = "≥1 candidate clears ... on ≥2 distinct firms"; FALSIFIED =
  "No pre-registered candidate clears Part A on **any** tier by 2026-11-08"; AMBIGUOUS = the
  §7(9) calibration reference itself clears the ceiling) — anchor `027a729` (2026-08-14). The
  same two-condition shape as §4, reproduced verbatim, with a third row that is scoped to a
  discriminability failure, not to a partial clearance count.
- [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
  (full text) — anchor `0723587` (2026-08-22). Confirms the discharge that once rested on two
  tiers (Tradeify 2.65%/MFFU 2.64%) was withdrawn on corrected eval-lock geometry; **current
  measured state at the four frozen $100K tiers is zero Part A clearers**
  ([`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md:15`](../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md),
  anchor `027a729`, 2026-08-14: "there are zero Part A clearers"). The exactly-one-clear state
  has **not occurred yet** — this addendum closes the gap pre-emptively, before any result would
  make the ruling self-serving (the same discipline the 2026-07-13 pre-registration's own §1
  invokes against ad-hoc scoring).
- [`lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md`](../../lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md)
  (full text) — anchor `027a729` (2026-08-14). Two Part A clearers exist, but only at the
  diagnostic-only **50K** band (`Tradeify_Select_50K` / `MFFU_Rapid_50K`), which the prereg's §3
  frozen tier cross-section explicitly excludes from §4 discharge — confirms the $100K count is
  the only count that matters here, and it is currently 0-of-4, not 1-of-4.
- [`docs/adr/2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md`](2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md)
  (full text) — anchor `b476860` (2026-08-16). §2/§5 explicitly decline to touch "any
  programme-level, date-boxed hard falsifier (e.g. the prop-portfolio §4 ... existence test)" —
  confirming that ADR is not a ruling on this gap and §4's exact wording remains untouched by it.
- [`docs/adr/2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) (full text)
  — anchor `91e6caa` (2026-08-15) — tier test applied above; its own 2026-08-15 addendum
  ("amend-in-place beats a sibling ADR") governs the vehicle choice.
- [`STATE.md`](../../STATE.md) — anchor `0723587` (2026-08-22). Queue row 1 (F1, the
  Tradeify-resting-discharge fork) and the "Standing base case" line ("absent an N-clear
  candidate, the 2026-11-08 §4 falsifier reads FALSIFIED") are the closest existing repo
  statements adjacent to this gap — neither rules on an exactly-one-tier clear specifically; F1
  is a different question (whether a discharge *resting on Tradeify* counts, not whether *one*
  tier is enough), and the base-case line is an informal heuristic in a forward-obligation
  register, not a governing definition of §4's own disposition space.
- [`docs/SESSIONS.md`](../SESSIONS.md) — anchor `3ff0fee` (2026-08-23, this branch's current
  head). Carry-forward lines name a never-elaborated "D3 fork" alongside "AMBIGUOUS-HOLD
  counting" as siblings from an "original diagnostic slate... governance holes"
  (e.g. line 1501). Repo-wide search (content and `git log -S "D3 fork"`) found no definition
  reachable in this checkout beyond those two carry-forward mentions — **this addendum does not
  claim "D3 fork" is this gap**; it is flagged only as an unconfirmed adjacent possibility, not
  relied upon.
- **External-lens note** (non-authoritative, per scope): a sanitized, genericized version of
  this exact success/revert-dichotomy shape was also run through the sanctioned
  stateless second-opinion lane under
  [`2026-08-22-ox-alpha-adversarial-lens-scope.md`](2026-08-22-ox-alpha-adversarial-lens-scope.md)
  (anchor `b2e5f15`, 2026-08-22) as a blind candidate-objection check; per that ADR's
  own §2/§5, its output carries **zero authority** over this ruling and is not otherwise
  reproduced or relied upon here — this addendum's reasoning below is derived independently from
  the real, unsanitized artifacts cited above.

### The gap this closes

§4 as written is a two-condition dichotomy: **H (success)** requires clearing on "≥2 of the four
`FRIENDLY` firm tiers"; the **revert trigger** requires "no pre-registered portfolio candidate
clears ... on **any**" tier. The 2026-07-13 pre-registration's frozen §6 gate table reproduces the
identical shape almost verbatim: **RESOLVED** needs ≥2 distinct firms; **FALSIFIED** needs zero
tiers cleared on any candidate; **AMBIGUOUS** is scoped only to a calibration-reference
discriminability failure (the §7(9) non-candidate reference itself clearing the ceiling), which
is a different failure mode entirely and does not cover a genuine partial clearance.

If, at the 2026-11-08 hard date, **exactly one** of the four frozen $100K tiers has cleared Part A
(bust ≤3.0% + pass ≥50%, Run-2) and no second distinct firm has also cleared, that state satisfies
**neither** H (needs ≥2) **nor** the revert trigger (needs zero) **nor** the AMBIGUOUS branch
(wrong failure mode). No document in this repo rules on it. This is not hypothetical scope-padding
— the pre-registration's own stated purpose (§1) is to prevent exactly this kind of disposition
being written only after a candidate's numbers are already visible (the "best-of-K / criteria-drift"
failure the `programme-audit` protocol's degeneration signal #4 names). The gap is currently
dormant (measured state is 0-of-4, not 1-of-4, per §0 above) — which is precisely why it should be
closed now, not left to be resolved for the first time under the pressure of an actual near-miss
result at the hard date.

### Ruling (proposed)

**Fourth branch, added to §4's disposition space** (and, on acceptance, pointed to by a
reader-intercept banner on the prereg — see Implementation, below; the prereg's frozen §6 body is
**not** edited in place):

If, at 2026-11-08, exactly one of the four frozen `Bulenox_100K` / `Tradeify_Select_100K` /
`MFFU_Rapid_100K` / `BluSky_Premium_100K` tiers has a pre-registered candidate clearing Part A and
no second distinct firm has also cleared:

- **H does not fire.** No G8 admission proceeds under §4's own authority — the ≥2-firm
  cross-validation bar (and, where the clearer is `trailing_locking`, the geometry-diversity
  rationale in the prereg's §3 F2 optimism labels) is the operative design intent, not a
  formality; one tier is not "the ceiling doesn't discriminate," but it is also not
  cross-validated evidence of a deployable programme-level edge.
- **The revert trigger does not fire.** It is written as "no candidate clears ... on any tier" —
  literally false when one has. Auto-demoting to research-only on this state would fire the
  falsifier on evidence that contradicts its own trigger condition, the same category of error
  the 2026-08-16 ADR named for AMBIGUOUS-HOLD (though that ADR explicitly declines to reach this
  falsifier — §0 above).
- **Disposition: `PARTIAL`.** The programme is **not** discharged and **not** demoted. The single
  clearing candidate carries forward as an ordinary lifecycle `CANDIDATE`-track lead (ordinary
  `strategy_lifecycle.md` gates apply), but **without** §4-authority G8 admission or any claim
  that the programme-level falsifier is resolved. The falsifier stays open, re-read at the
  **next quarterly programme audit (2027-02-08)** — the cadence §4 already names ("Trigger check
  schedule: quarterly ... 2027-02-08") — under the same frozen ceiling, tiers, and discharge rule
  (no re-derivation; Trap #12 stays in force).
- **At that 2027-02-08 re-check:** if a second distinct firm has since cleared, H fires and the
  programme discharges normally. If the count is still ≤1, the revert trigger is read as
  satisfied by extension — a single clearer sustained three additional months without a second
  corroborating firm is treated as the functional equivalent of "no cross-validated candidate
  exists," which is what the revert trigger exists to detect — and the programme demotes to
  research-only at that point, closing the gap definitively rather than leaving it open
  indefinitely.

### §3 — Alternatives considered

| Alternative | Why not chosen |
|---|---|
| Round n=1 up to RESOLVED | Contradicts §4's own explicit "≥2" text and the prereg's explicit rejection of single-geometry (Bulenox/BluSky-only) clearance as insufficient; would discharge the programme on evidence the designers deliberately said was not enough. |
| Round n=1 down to FALSIFIED at 2026-11-08 | Over-reads the revert trigger, which requires **zero**, not "fewer than two." A candidate that did clear one real tier is not the same evidence class as "no pre-registered candidate clears any tier" — collapsing them loses real information the falsifier was designed to detect. |
| Leave the gap open, rule ad hoc if it ever happens | The status quo, and the exact failure mode this addendum exists to close — the pre-registration's own §1 names ad-hoc post-hoc scoring as the degeneration pattern to avoid, and it is avoidable here because the state has not occurred yet. |
| Extend indefinitely with no re-check date | Rejected — an open-ended "wait for a second clearer" would let the programme run past 2026-11-08 forever without any accountable falsifier state, defeating the entire point of a date-boxed programme-level existence test. The chosen ruling reuses §4's own already-named quarterly cadence (2027-02-08) instead of inventing a new one. |

### Forbidden moves (under this addendum)

- **Treating `PARTIAL` as a `FALSIFIED`-equivalent or `RESOLVED`-equivalent strike anywhere else**
  (the harvest-intake §4, the no-counterparty channel §4, or any other date-boxed existence
  falsifier). This ruling is scoped to this ADR's own §4 only.
- **Moving the 3.0% ceiling, the 50% pass floor, the `trailing_locking` requirement, or the frozen
  four-tier cross-section to manufacture a second clearer.** The gate stays frozen; only the
  *disposition* for an already-observed one-tier state is being defined.
- **Editing the pre-registration's frozen §6 body in place.** On acceptance, only a
  reader-intercept banner (matching the established convention — the 2026-07-22 ADR's own
  W1 banners; the 2026-08-16 ADR's dense-1m banner) is added, pointing here; Trap #12 (no
  amendment after a result is seen) is honored by the fact that no n=1 result exists yet.
- **Treating this addendum as also ruling on F1** (whether a discharge resting on Tradeify, or on
  the withdrawn Striker book, counts). F1 is a different question — orthogonal to *how many*
  tiers clear — and stays a separate, still-open queue item (STATE.md row 1). Deciding it here
  would be exactly the pre-emption STATE.md's own F1 note warns against.
- **Treating the sanitized external-lens pass as evidence for or against this ruling.** Per
  [`2026-08-22-ox-alpha-adversarial-lens-scope.md`](2026-08-22-ox-alpha-adversarial-lens-scope.md)
  §2/§5, that lane is zero-authority tripwire input only; this ruling stands or falls on the real
  artifacts cited in §0, not on that lane's output.

### What is unchanged

§4's original H text, revert trigger, secondary (eligibility) trigger, and 2026-11-08 hard date;
the prereg's frozen §2 protocol, §3 ceiling/tiers, §4 H-SCORE, §5 forbidden moves, and §6
RESOLVED/FALSIFIED/AMBIGUOUS rows — all untouched. This addendum adds a fourth, previously
uncovered disposition; it does not withdraw or loosen any existing one.

### Implementation (owed only upon acceptance — not executed while this addendum is Proposed)

1. Reader-intercept banner (top of file, below any existing banner) on
   `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`, pointing to this
   addendum for the exactly-one-tier-clear disposition. No edit to its frozen §2–§7 body.
2. One STATE.md forward-obligation line update noting the `PARTIAL` disposition and its
   2027-02-08 re-check, alongside the existing F1 queue row (kept as a separate row — Forbidden
   move 4 above).
3. `docs/SESSIONS.md` entry recording the ratification, per this repo's session-log discipline.

### Falsifier (for this ruling itself)

**H:** the `PARTIAL`/2027-02-08-extension disposition correctly distinguishes "one real clearer,
cross-validation still pending" from both outright programme failure and programme success,
without functionally extending the hard date in a way that erodes the falsifier's bindingness.

**Revert trigger:** if this disposition is ever invoked and, at the 2027-02-08 re-check, the
operator judges in hindsight that the extension delayed a demotion decision that should have
fired at 2026-11-08 (i.e., the single clearer never looked like a real path to a second firm), a
superseding addendum should tighten the ruling — e.g., dropping the extension and reading n=1 as
FALSIFIED-at-the-hard-date on any future occurrence — rather than reverting to today's undefined
gap.

**Trigger check schedule:** at 2026-11-08 (does the gap fire for real) and, if it does, again at
2027-02-08 (was the extension the right call).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-12 | Initial acceptance | Joshua + Cursor Cloud Agent |
| 2026-07-15 | Superseded in part (candidate class) by existing-strategy-candidates ADR — header + §2 R6-boundary + §5 deploy bullet annotated | Joshua + Cursor |
| 2026-07-24 | §10 hook-3 staleness note added (`ACTIVE_FIRM == 'FXIFY'` hard-fails since substrate Phase 1; property intact, hook line unedited). Non-material — no §2/§4 edit, no decision or status change; the §4 falsifier's status is owned by [`2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](2026-07-22-prop-portfolio-s4-discharge-withdrawal.md). | Claude Code |
| 2026-07-25 | `Superseded-in-part-by` reciprocal added for `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` (§4 discharge status only). Was invisible to `check_adr_graph.py`'s A2 check — the withdrawal ADR's `Supersedes:` line uses markdown-link citation style, which the edge parser silently dropped rather than flagging; fixed in the same pass (`scripts/check_adr_graph.py`). Non-material header repair — no §2/§4 prose edit. | Claude Code |
| 2026-08-22 | **Addendum drafted (`Proposed`, not yet `Accepted`):** §4's success/revert dichotomy does not cover an exactly-one-of-four-tiers-clears state; proposes a fourth `PARTIAL` disposition holding the falsifier open to the existing 2027-02-08 quarterly check rather than firing either branch on the wrong evidence. No §2/§4 original text edited; awaits operator ratification. | Claude Code |
