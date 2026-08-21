# ADR 2026-07-01 — Add-back metric layer split (meta-layer signal vs object-layer strategy)

**Path:** `docs/adr/2026-07-01-add-back-metric-layer-split.md`
**Status:** Accepted — ratified by operator (JA) 2026-08-21, as an explicit override ahead of §4's evidentiary graduation gate (no programme audit has ever computed both layers' add-back rates since authoring — checked across every audit note under `docs/notes/audits/programme-audit/`, zero hits post-2026-07-01). See Addendum 2026-08-21.
**Decision date:** 2026-07-01
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Date:** 2026-07-01
**Owner:** Joshua
**Author:** Claude Code (spawned follow-up task `task_f61cabfa` from the 2026-07-01 methodology-belt scoped audit §5.1).
**Layer:** methodology (meta-layer governance).
**Loop-of-Record:** STRATEGIC — this amends a canon calibration metric (governance of what governs); low-reversibility canon edit. Landed PROPOSED; graduation PROPOSED→ACCEPTED is the owner's Strategic act (no-borrowing per `docs/adr/2026-06-12-three-loop-methodology-binding.md` D3 — CC proposes, owner ratifies).
**Rule-2 budget:** OUTER (8 iterations) for the authoring execution. Landed under budget.
**Amends / extends:** `docs/adr/2026-06-12-three-loop-methodology-binding.md` §2 **D4** (add-back-rate metric) + its canon mirror `docs/methodology/inqhiori-canon.md` §14. For the **add-back metric definition specifically, this ADR governs**; the three-loop ADR governs the binding.

---

## §0 — Reads (Rule 0)

Read at on-disk-byte fidelity before authoring, 2026-07-01, worktree `competent-poincare-0b32d9`.

- `docs/methodology/inqhiori-canon.md` §14 — anchor `06e416d` (2026-06-16). Add-back sentence at `:295`: *"**Add-back rate** (Strategic Deletes later legitimately reversed on new mechanism evidence) is tracked at programme audits as the deletion-calibration metric; anchor datum: Guardian Silver re-open on beTriggerAtr=4.8 RF gate after the 2026-05-14 Q-CORR-1 closure."* — Guardian Silver is an **object-layer strategy**.
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` §2 D4 — anchor `e122582` (2026-06-13), `:55`: single pooled metric, same object-layer anchor (Q-CORR-1 / Guardian Silver). Status PROPOSED. Also references the metric at §4 H (`:74`), §7 (`:107`–`:108`), §10 hook #6 (`:137`–`:138`).
- `docs/methodology/rejected_signals.md` — anchor `7c864aa` (2026-06-04). Meta-layer rejection registry; **1 entry** (Starvation, REJECTED 2026-06-04, uncleared re-proposal bar). This is the (a)-branch data source.
- `docs/rejected_candidates.md` — object-layer strategy/track/instrument rejection registry with per-entry `addback_condition` fields (the §C per-candidate add-back **gate** from `docs/adr/2026-06-14-rejected-candidate-patterns.md`, a *distinct* device from the D4 aggregate **rate**). This is the (b)-branch data source. **Not modified by this ADR.**
- `docs/adr/2026-06-12-notion-surface-retirement.md` §10 hook #6 — anchor `e122582`. The Notion-surface add-back check "feeds the binding ADR's D4 metric." Notion-surface re-emergence is a **governance/meta-layer** reversal — reviewed **qualitatively** at methodology audits (via that ADR's own falsifier); it is **not** pooled into the registry-scoped (a) rate (§2 D1). (Grep-surfaced surplus finding: D4 as written already conflated a meta-layer reversal (Notion) with an object-layer one (Guardian Silver) — motivating the meta/object split.)
- Trigger artifact: `docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md` §5.1 (local, uncommitted at authoring).

**Rule-0 verdict:** the cross-reference grep (brief-authoring §0 sub-rule) found the metric referenced in **six** places, not the two the spawning task named. Only canon §14 + three-loop D4 carry the *definition* (edited here); the rest are pointers that remain valid because D4 now has two branches (§7).

---

## §1 — Context

The 2026-07-01 methodology-belt scoped programme audit (diagnostics #2 + #7) needed to compute the add-back rate for its #2 diagnostic. It found that the canon defines add-back over "**Strategic Deletes** … reversed on new mechanism evidence" with its **only** worked anchor being **Guardian Silver — an object-layer strategy** — yet the metric is "tracked at programme audits," which for a *methodology* audit is a meta-layer event. Under the programme-audit **two-layer rule** (`docs/adr/2026-06-12-three-loop-methodology-binding.md` coupling rules; `programme-audit` SKILL — "when authoring a methodology audit, do not cite portfolio performance"), a methodology audit may not cite object-layer strategy reversals as evidence about the belt's health. The audit therefore had to hand-carve a meta-layer-only reading (numerator = rejected *methodology signals* re-accepted; 0/1, under-sampled) rather than apply the canon definition as written.

The definition-as-written is a **latent cross-layer contamination** (programme-audit trap #2) baked into a canon calibration metric — it silently invites the exact leakage the two-layer rule bars. The grep also showed the metric already conflates a governance-surface reversal (Notion) with a strategy reversal (Guardian Silver), i.e. it was never single-layer to begin with.

**Decision driver (one sentence):** a canon metric that a methodology audit must consult cannot be defined in a form that forces object-layer citation — it must be split so each layer's audit computes only its own layer's add-back.

---

## §2 — Decision

**D1 — Split the D4 add-back-rate metric into two layer-segregated instruments (never pooled).**

- **(a) Meta-layer signal add-back rate** = (rejected **methodology signals** in `docs/methodology/rejected_signals.md` later re-accepted on a dated incident) ÷ (rejected methodology signals issued). **Consumed by methodology (meta-layer) programme audits only.** No object-layer anchor. Current value: **0 / 1** (numerator 0; denominator 1 = the Starvation rejection; under-sampled). **Registry-scoped by design** so the rate stays computable. Other meta-layer governance-surface/device Delete reversals — a retired workflow surface re-instated (e.g. `docs/adr/2026-06-12-notion-surface-retirement.md` §10 add-back hook) or a retired hook restored — are **also meta-layer**, but are tracked via their own ADR falsifiers and reviewed **qualitatively** at methodology audits; they are **not pooled into the (a) rate** (pooling would make the denominator ill-defined, since it would then have to enumerate every governance prune).
- **(b) Object-layer strategy/track/instrument add-back rate** = (object-layer Strategic Deletes in `docs/rejected_candidates.md` — strategies, tracks, instruments — later legitimately reversed on new mechanism evidence) ÷ (such object-layer Deletes issued). **Consumed by portfolio (object-layer) audits only.** **Anchor datum: Guardian Silver** re-open on beTriggerAtr=4.8 clearing the RF +50.7% gate (Q-CORR-1 closure 2026-05-14).

**D2 — Two-layer coupling enforced on add-back.** A methodology audit computes and cites **only (a)**; a portfolio audit **only (b)**. A methodology audit citing Guardian Silver (or any strategy/track/instrument reversal), or a portfolio audit citing a rejected-signal re-accept, is trap-#2 contamination and **disqualifying**. The umbrella framing — "add-back as a Strategic calibration metric" — is **retained** (the STRATEGIC loop owns kill/continue for both layers), but the two instruments are never summed into one number.

**D3 — The 10%-rule interpretation bands apply per-instrument, within each layer's own audit.** Each rate is judged against the ~10% band separately (0 over ≥2 cycles → deletion too conservative; sustained ≫10–15% → too aggressive / kill evidence too thin). Pooling would let object-layer strategy reversals mask meta-layer signal calibration and vice versa — the precise failure this ADR prevents.

**D4 — Guardian Silver is retained as the object-layer (b) anchor only.** It is removed from the meta-layer statement. No object-layer constant, strategy, allocation, or MC value is touched by this ADR.

**Effective:** immediately upon acceptance. **Scope:** the D4 add-back calibration metric and its canon §14 mirror; all future programme audits (meta and object).

---

## §3 — The Algorithm pass (on this ADR itself)

- **Question:** the requirement ("a methodology-audit metric must not force object-layer citation") originates from a measured event — the 2026-07-01 audit had to hand-carve a meta-only reading — not an abstraction.
- **Delete:** could we delete the meta-layer add-back and track only object-layer? Rejected — The Algorithm's 10% rule applies to the belt too (that is the whole #2 diagnostic); a methodology audit needs a deletion-calibration metric of its own. Could we delete the metric entirely? Rejected — it is D4, load-bearing to the three-loop ADR's own falsifier.
- **Simplify:** smallest sufficient form — one metric, two layer-segregated instruments, one coupling rule, bands per-instrument. Rejected larger forms (a third "cross-layer synthesis" rate; a telemetry table).
- **Accelerate:** the meta-layer add-back hook (§10) makes (a) computable in O(seconds) at each methodology audit.

---

## §4 — Falsifiable hypothesis

**H:** If, over the next two programme-audit cycles, each layer's add-back rate is computable **from its own layer's registry alone** (meta: `rejected_signals.md`; object: `rejected_candidates.md`) **without any cross-layer citation**, and no audit pools the two, then the split is load-bearing and graduates PROPOSED→ACCEPTED at the first audit where both layers have been computed once.

**Otherwise:** if an audit must pool the two instruments to produce a rate, OR a methodology audit cites an object-layer reversal (or vice versa) to compute add-back, the split is ceremony-as-implemented — disposition at audit is amend-or-delete, not silent retention.

**Falsifier (revert trigger):** the split is **falsified** if the two registries prove indistinguishable in practice (every meta-layer add-back is also an object-layer one, so the segregation never changes a number across two audit cycles) → revert to the pooled D4 with a note that the layers do not diverge for this operation. **Revert action:** supersede this ADR, restore the single-metric D4 text (preserved verbatim in §0). **Check schedule:** the two meta-layer audits at ≈2026-09 and ≈2026-12.

---

## §5 — Forbidden moves (each genuinely tempting)

1. **Pooling (a) and (b) into one add-back number "for simplicity."** That reinstates the exact cross-layer contamination this ADR removes. The two are reported side-by-side, never summed.
2. **Using Guardian Silver — or any strategy/track/instrument reversal — as evidence in a *methodology* audit.** Object-layer anchor for (b) only. Symmetric: no rejected-signal re-accept in a *portfolio* audit.
3. **Amending the metric definition in place without an ADR of record.** A Strategic canon edit needs a recorded decision (this ADR); a silent in-canon patch is the no-borrowing violation (three-loop D3).
4. **Letting either band auto-tune a threshold.** The three-loop ADR §5 #6 already forbids self-tuning governance; restated here per-instrument. Bands inform the audit; the audit decides.
5. **Editing `docs/rejected_candidates.md` per-entry `addback_condition` fields or the 2026-06-14 rejected-candidate-patterns §C gate.** Those are the object-layer per-candidate *gate* (a distinct device); this ADR splits the aggregate *rate*, not the gate. Out of scope.

---

## §6 — Gate (binary adoption criteria)

ADOPTED (PROPOSED→ACCEPTED) when all hold; otherwise OPEN with the failing item named:

1. This ADR committed to `docs/adr/` (date-prefixed), Status PROPOSED, §0 anchors present.
2. `docs/methodology/inqhiori-canon.md` §14 add-back sentence rewritten to the (a)/(b) split, Guardian Silver tagged **object-layer anchor only**, pointing to this ADR.
3. `docs/adr/2026-06-12-three-loop-methodology-binding.md` §2 D4 rewritten to the (a)/(b) split with an inline amendment banner pointing to this ADR; canon §14 and D4 **agree** (no residual pooled-metric text contradicting the split).
4. The meta-layer add-back hook (§10) is runnable and reconciles with the 2026-07-01 audit's 0/1 meta-layer figure.

**Graduation:** per §4 H at the first programme audit computing both layers. **FALSIFIED/AMENDED:** per §4 otherwise-branch. If neither has accrued evidence by the audit → **AMBIGUOUS**, hold PROPOSED one cycle.

---

## §7 — Consequences

**Downstream references — remain valid (point to D4, now two-branch); no edit required:**
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` §4 H (`:74`), §7 (`:107`–`:108`): "the add-back rate is computable" is true of **both** branches — unchanged.
- §10 hook #6 (`:137`, greps `rejected_candidates.md`) is now specifically the **object-layer (b)** hook — still correct as written.
- `docs/governance/systematic-trading-lifecycle.md:38` (telemetry pointer to D4) — valid; D4 now has two branches.
- `docs/adr/2026-06-12-notion-surface-retirement.md` §10 hook #6 — its Notion add-back is a **meta-layer** governance-surface reversal, reviewed **qualitatively** at methodology audits (via that ADR's own falsifier); it is **not** pooled into the registry-scoped (a) rate.

**Edits applied by this ADR:** canon §14 (D-level statement) + three-loop ADR §2 D4 (§6 gate items 2–3).

**New machinery:** the `programme-audit` skill / audit-note flow gains the meta-layer add-back hook (§10) so a methodology audit computes (a) mechanically.

**Cost (real):** two add-back numbers to report at audits instead of one; a per-audit discipline check that neither layer cites the other.

**Risk:** the two registries could prove to track the same reversals in practice (the §4 falsifier), making the split ceremony — mitigated by the two-cycle revert trigger.

---

## §10 — Audit hooks (runnable)

```bash
# (a) META-LAYER signal add-back — denominator (rejected signals issued)
grep -c '^### REJECTED' docs/methodology/rejected_signals.md
# numerator (rejected signals re-accepted on a dated incident): expect 0 at 2026-07-01
grep -niE 're-?accept|readmit|re-?admitted|re-?opened' docs/methodology/rejected_signals.md
# Meta-layer add-back RATE = numerator / denominator (0/1 at 2026-07-01) — registry-scoped.
# Governance-surface reversals (Notion surface, retired hooks) are meta-layer but reviewed
# QUALITATIVELY via their own ADR falsifiers — NOT added to this rate's denominator.

# (b) OBJECT-LAYER strategy add-back — the existing three-loop §10 hook #6 (unchanged)
grep -riE 're-open|reopen|add-back|unparked' docs/rejected_candidates.md docs/briefs/ --include='*.md' | head

# Consistency: canon §14 and three-loop D4 both carry the (a)/(b) split, Guardian Silver object-only
grep -n 'meta-layer signal add-back\|object-layer.*add-back\|object-layer anchor' \
  docs/methodology/inqhiori-canon.md docs/adr/2026-06-12-three-loop-methodology-binding.md
# Expected: both files show the split; Guardian Silver appears only under the (b)/object-layer branch

# Contamination guard: no methodology audit note cites Guardian Silver as add-back evidence
grep -rn 'Guardian Silver' docs/notes/audits/programme-audit/ | grep -i 'add-back' || echo "clean"
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-01-add-back-metric-layer-split.md --type adr
# Expected: RESULT: well-formed

# §0 anchors resolve
git log -1 --format='%h %ci' -- docs/methodology/inqhiori-canon.md                      # 06e416d
git log -1 --format='%h %ci' -- docs/adr/2026-06-12-three-loop-methodology-binding.md   # e122582
git log -1 --format='%h %ci' -- docs/methodology/rejected_signals.md                    # 7c864aa

# Split is applied and consistent (§6 gate items 2-3)
grep -c 'meta-layer signal add-back' docs/methodology/inqhiori-canon.md docs/adr/2026-06-12-three-loop-methodology-binding.md
# Expected: >=1 in each
```

---

## Addendum 2026-08-21 — Operator ratification (explicit override, not §4 graduation)

**Does not amend §2 / §4 / §6.** §6's mechanical landing criteria (items 1–4) are independently
re-verified this session: canon §14 and the three-loop ADR §2 D4 both carry the (a)/(b) split and
agree with each other; the contamination guard is clean — a grep for "Guardian Silver" +
"add-back" across every file under `docs/notes/audits/programme-audit/` finds only the 2026-07-01
founding audit, and it is already correctly scoped meta-layer-only, never a later contamination.

**§4's actual graduation trigger has never fired.** §4 requires both layers' add-back rates to be
computed *at a programme audit*, without cross-citation, at least once. A grep for "add-back"
across every programme-audit note since authoring returns zero hits outside 2026-07-01 itself —
across at least eight subsequent audit cycles (07-11, 07-15, 07-21, 08-03, 08-05, 08-08 quarterly,
08-14, 08-15). This is not a case where the split was tested and came back ambiguous; it is a gate
no audit has ever consulted — the same shape as `lesson_gate_reachability_preregistration`'s
UNBINDING failure mode, applied to this repo's own methodology layer rather than a research gate.

**Ratified anyway**, by explicit operator instruction, 2026-08-21. Supporting evidence gathered
this session — a direct re-run of §10 hook 1, **not** a programme audit, so it does not itself
satisfy §4's "at a programme audit" language: `docs/methodology/rejected_signals.md` currently
carries 2 rejected signals (grown from 1 at authoring), 0 re-accepted — meta-layer rate **0/2**,
cleanly computable, no cross-layer citation observed.

**This is an override, not a claim the evidentiary bar was met** — logged as such per the same
convention already used for the Rule 2 ratification
([`docs/adr/2026-06-16-rule-2-budget-before-acting.md`](2026-06-16-rule-2-budget-before-acting.md)
Addendum 2026-08-21): the gate result is recorded honestly (never fired), and the operator's
separate judgment sits alongside it, not inside it.

**Audit discipline is unchanged.** Future programme audits should still run the §10 add-back
computation on their own cadence — ratification here does not retroactively manufacture an
audit-time computation that never happened. Worth flagging to whoever runs the 2026-11-08
quarterly: this gate has sat unexercised since authoring and is due a real first run.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-01 | Initial authoring — split D4 add-back into meta-layer (a) + object-layer (b); PROPOSED | Joshua + Claude Code |
| 2026-08-21 | Ratified `Accepted` as an explicit operator override (Addendum 2026-08-21) | Claude Code, per operator direction |
