# 2026-06-14 — Rejected-candidate structural patterns: taxonomy, dedup axes, add-back gate

**Status:** Accepted (2026-06-14) — taxonomy, dedup-axis separation, add-back gate, and the additive schema extension are all adopted; the §7 downstream sweep landed (SCHEMA.md note + registry pointer + `feedback.py` field extension with a round-trip test, 19/19 intake tests green).
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-11-gen1-pipeline-retirement.md` - dedup.py/feedback.py mechanism only; `2026-08-09-rejection-register-topology-and-bar-wiring.md` - registry topology only.
**Retain-until:** none
**Decision date:** 2026-06-14
**Authors:** Joshua + claude.ai (advisor, web session) → reconciled against repo by Claude Code
**Related:** [`2026-06-14-reject-usoil-rdm-spike-fader.md`](2026-06-14-reject-usoil-rdm-spike-fader.md) (companion — the worked exemplar this ADR's taxonomy classifies) · [`2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md) (the standing concept-intake-gate decision this extends)
**Layer:** methodology

> **Reconciliation note (Rule 0).** Authored in a web session with no repo access. The original draft proposed a *replacement* pipe-delimited registry schema and referenced `docs/registry/rejected_candidates.md` + `scripts/registry/check_registry.py`. Both are confabulations: the registry lives at `docs/rejected_candidates.md`, is **additions-only**, and is consumed by a **live parser** (`lab/validation/concept_intake/dedup.py`). This version *extends* the existing schema rather than replacing it, and corrects every path. See §3.

> **D-S-A domain:** Meta-process — this changes the rejected-candidates **registry methodology**, not a data corpus and not a built artefact. A meta-process D authorizes deleting the ceremonial scaffolding it replaces (here: rejection-class conflation in free-text notes) but does **not** authorize any data- or system-domain change. Locked strategies, allocations, `dd_protection`, MC: untouched.

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this reconciled version (the web draft's §0 read nothing on disk — that is the defect this section repairs):

- `docs/rejected_candidates.md` — anchor `b46f30c` (verified `git log -1` on 2026-06-14). The actual registry: prose `### <heading>` entries + pending-list bullets + structured `<!-- concept-intake-entry … -->` records. Header states **additions-only**: "never edit or delete a prior rejection; the gate's loop depends on the lineage staying intact."
- `lab/validation/concept_intake/dedup.py` — anchor `c106807`. `dedup_check()` reads the registry at call time; `_KV_RE = (\w+)\s*=\s*"([^"]*)"` (line 57) extracts **all** `key="value"` pairs from the comment and `kv.get(...)` consumes only `mechanism_family` + `instrument` (lines 137–139). **Unknown attributes are silently ignored → the schema is forward-compatible with new fields.**
- `lab/validation/concept_intake/feedback.py` — anchor `6bf0dff`. `build_registry_entry()` (lines 49–96) emits the 5 base fields. Adding the new fields to *auto-appended* entries requires extending this function (§7); hand-authored entries can carry them today.
- `lab/validation/concept_intake/SCHEMA.md` — anchor `6473809`. The "End-to-end consistency" section pins validate → dedup → feedback to one schema; the schema-extension note belongs here (§7).
- `docs/adr/2026-06-05-concept-admissibility.md` — the standing intake-gate decision (falsifier + forbidden moves) this ADR builds on, not supersedes.

---

## §1 — Context

The registry audit found that **conflating the rejection class with the dedup axes** degrades the dedup gate: a single free-text "why rejected" note cannot answer "is this new?" cleanly, so near-rediscoveries slip through and legitimately-distinct candidates get wrongly blocked. Across the last five rejections, recurring structural patterns surfaced (cost-geometry, proxy-escalation, subset-not-edge, role-asymmetry) that belong in methodology, not scattered across session records. The intake gate already *machine-enforces* dedup ([`dedup.py`](../../lab/validation/concept_intake/dedup.py): `CLEAR | DUPLICATE | NEAR_MATCH` on the composite `(mechanism_family × instrument)` key); what is missing is (a) a named **class** per rejection with per-class **add-back conditions**, (b) explicit separation of class from the dedup axes, (c) a structured **add-back gate** (the anti-degeneration rule), and (d) the cross-candidate lessons captured with dated anchors.

**Decision driver (one sentence):** with five clean rejections and zero validated concepts, the programme-audit watch-flag needs reframing — the count is the gate *correctly rejecting*, but only if re-litigation by re-tune is mechanically forbidden, which today it is not.

---

## §2 — Decision

**Decision:** Adopt a 4-class rejection taxonomy with per-class add-back conditions (§A), keep the three dedup axes orthogonal to the class field (§B), enforce a structured add-back gate (§C), and **extend** the existing `<!-- concept-intake-entry … -->` registry schema with five new attributes (§D) — additions only, no rewrite of prior entries, no parser change required.

**Effective:** on acceptance, for every registry entry written from 2026-06-14 onward.
**Scope:** the rejected-candidates registry (`docs/rejected_candidates.md`) and the concept-intake dedup loop. Legacy entries are **not** retro-fitted (additions-only invariant).

### §A — Rejection taxonomy (4 classes, each with its add-back condition)

The class records **why** a candidate was rejected. Add-back conditions differ by class — that is the whole point of not conflating them.

| Class | Definition | Add-back condition (binary) | Anchor |
|---|---|---|---|
| **edge-failure** | Mechanism tested, placebo-controlled on the **canonical execution-TF** panel, net-negative or indistinguishable from a matched random null. | A **genuinely new entry mechanism** (distinct mechanism class). NOT: re-tune, subset/regime slice, stop-geometry tweak. | USOIL-RDM-001 (pending canonical re-run — see companion ADR) |
| **portfolio-fit / tail** | Standalone edge may exist, but admission degrades the portfolio tail (bust / p99 DD). | A **validated counterbalance leg** OR an allocation change that demonstrably neutralizes the tail (re-MC ≤ prior bust). | Guardian Silver v1.0 (bust 24.54%→29.82%) |
| **venue / cost-constraint** | Edge may exist gross, but realized execution geometry/cost makes it uncapturable. | A geometry that **clears the cost-law pre-flight with margin** (from the *realized* stop, not assumed k·ATR) OR a materially lower-cost venue. | USDCAD 1.42×ATR(15m) 0.097R round-trip |
| **non-rediscovery / role-duplicate** | Duplicates a registry entry on the same mechanism **and** role. | Differing **mechanism OR role** (e.g. same signal as *exit* vs *entry*). | Sovereign rate-spread (net-neg entry; useful exit) |

A candidate may carry a primary class plus a secondary; the **primary** governs the add-back condition.

### §B — Dedup axes (already machine-enforced; orthogonal to class)

These are the three axes `dedup_check()` already evaluates — this ADR names them so the class field never re-absorbs them:

1. **Mechanism** — is the causal mechanism distinct from every registry entry? (`mechanism_family`, not instrument, not parameters.)
2. **Portfolio-fit** — diversifier/counterbalance/capacity, or a known tail-amplifier already rejected on portfolio-fit?
3. **Non-rediscovery** — is `(mechanism, role)` absent? A signal rejected as an *entry* is **not** a rediscovery when proposed as an *exit* (role-asymmetry — see §lessons L-ROLE-ASYMMETRY).

The dedup gate runs **before** investigation; the class + add-back governs **re-entry** of something already rejected. They compose; they do not compete.

### §C — Add-back gate (the anti-degeneration rule)

> A previously-rejected candidate is re-admissible **only** by satisfying the add-back condition for its primary class (§A).

**Re-tuning an edge-failure is not an add-back — it is the degeneration move.** Searching parameters/slices until a placebo-failed concept yields a positive cell is "a parameter plateau around a spurious selection still passes." The add-back gate makes that move cost a *new mechanism*, not a new sweep. Add-back requests log: rejected ID, class, add-back condition claimed met, evidence. An add-back that cannot name which condition it satisfies is rejected without investigation.

### §D — Schema extension (additions to the EXISTING comment schema)

The registry's structured record stays the `<!-- concept-intake-entry … -->` HTML comment that `dedup.load_registry` parses. From 2026-06-14, hand-authored and ADR-sourced entries **add** these attributes (the harness-auto path gains them via §7):

```
<!-- concept-intake-entry
     mechanism_family="…"  instrument="…"  rejection_reason="…"
     harness_disposition_ref="…"  date="YYYY-MM-DD"          ← existing 5, unchanged
     class="edge-failure|portfolio-fit|venue|non-rediscovery[+secondary]"
     role_tested="entry|exit|filter|size"
     falsifier_failed="the test + numbers that killed it"
     addback_condition="the binary re-entry condition for the primary class"
     config_fingerprint="<standing fingerprint convention>" -->
```

`role_tested` and `falsifier_failed` are **mandatory** on new entries (they fix the entry/exit dedup hole and mirror the gate-audit "D-test applied, verbatim"). Because `_KV_RE` ignores unknown keys, **`dedup.py` needs no change** for these to coexist; the existing composite-key + Jaccard logic is unaffected. The USOIL-RDM-001 entry in the companion ADR is the worked exemplar.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Replace** the registry with a pipe-delimited schema (the web draft's §schema) | Breaks the live `dedup.load_registry` parser (regex keyed to `<!-- concept-intake-entry … -->` + prose `###`), and "replaces the single free-text note" violates the **additions-only** invariant the dedup loop depends on. Extension (§D) gets the same fields at zero parser-risk. |
| Add the fields to the intake `ConceptRecord` (pydantic `extra='forbid'`) | Wrong object: those fields describe a *rejection post-mortem*, not a *proposal*. `extra='forbid'` would reject them. The registry comment is the correct home. |
| Pure-prose methodology doc, no schema touch | Leaves the entry/exit dedup hole open (`role_tested` would stay un-recorded) and keeps `falsifier_failed` as free text the parser can't key on later. The cost of the extension is ~5 attributes; the benefit is a queryable falsifier/role record. |
| Status quo — keep free-text notes only | The audit's finding stands: class/dedup conflation already let same-instrument NEAR_MATCH boosts fire on every USOIL concept (sim 0.52 vs the carry corpse, per the USOIL ledger). The taxonomy + role field is what separates them cleanly. |

---

## §4 — Falsifier (revert trigger)

**Hypothesis (H, falsifiable):** the rejected-candidate taxonomy is *self-correcting* — with the add-back gate in place, the registry rejects bad concepts without re-litigation, so "zero validated from N runs" reflects the gate working, not the pipeline failing.

The taxonomy is **Progressive/working** iff: (a) every registry entry since this ADR carries `class` + `role_tested` + `falsifier_failed` + `addback_condition`, **and** (b) zero rejected candidates were re-admitted except via a satisfied §C add-back condition. It is **Degenerating** iff any edge-failure was re-admitted by re-tune/slice, or any belt-patch was applied to a placebo-failed concept.

**Revert trigger:** at the next scheduled programme audit (**2026-08-08**), if either limb fails — a post-2026-06-14 entry missing a mandatory field, OR any re-tune re-admission — this ADR is downgraded and the gate is re-opened for redesign.

**Revert action:** supersede with a fresh ADR; do not silently edit the taxonomy.

**Trigger check schedule:** quarterly programme audit, next **2026-08-08** (co-scheduled with the regime check).

---

## §5 — Forbidden moves (under this ADR)

- **Letting the class field re-absorb the dedup axes.** The exact conflation this ADR fixes. Class and dedup axes are separate attributes (§A vs §B).
- **Rewriting or deleting a prior registry entry to "apply the new schema."** Forbidden — additions-only (`feedback.py` docstring §5 #5; dedup lineage). New fields apply to new entries only.
- **Graduating L-COST-GEOMETRY / L-PROXY-ESCALATION to load-bearing now on counterfactual alone.** Lessons need a dated anchor **and** the E1/E2 bar (single incident >$3K, or three firings across separate windows). Adopt the *gates* now (near-free); keep the *lessons* candidate-status.
- **Treating "Working" as permanent.** The health verdict is re-tested 2026-08-08; one re-tune re-admission flips it to Degenerating.

---

## §6 — Consequences

**Positive:**
- Closes the entry/exit dedup hole (`role_tested` mandatory) and makes `falsifier_failed` queryable, not buried in prose.
- Reframes the "zero validated from five runs" watch-flag as the gate *correctly rejecting* — conditional on no re-tune re-litigation, which §C now forbids mechanically.
- Zero risk to the live dedup parser (extension, not replacement).

**Negative (real cost):**
- New entries carry ~5 extra attributes to fill — author overhead per rejection.
- Until §7 lands, harness-auto-appended entries (`feedback.py`) will *not* carry the new fields; only hand-authored / ADR-sourced entries will. Mixed-completeness registry until then.

**Risks:**
- If `feedback.py` is extended carelessly, an auto-append could emit a malformed comment that the regex still parses (silently dropping a field). Mitigation: §10 hook #1 + a `feedback.py` test asserting the new attributes round-trip.

**Gate cross-ref:** the 2026-08-08 health check returns a binary verdict — *Progressive* (taxonomy adopted) or *Degenerating* (this ADR **FALSIFIED** → §4 revert).

**Downstream artifacts that need updating (→ §7):**
- `lab/validation/concept_intake/SCHEMA.md` — note the registry-entry extension under "End-to-end consistency."
- `lab/validation/concept_intake/feedback.py` — extend `build_registry_entry()` to emit `class/role_tested/falsifier_failed` from the `DispositionRecord` (+ test).
- `docs/rejected_candidates.md` — header note pointing new authors at this ADR's §D.

---

## §7 — Implementation plan

- **Phase 0** — re-verify §0 anchors current at implementation time. ✅
- **Phase 1 (policy, adopted)** — taxonomy/dedup-axes/add-back gate adopted; new entries follow §D. No code change needed for `dedup.py` to keep working. ✅ First entry written under §D: `mean-reversion-spike-fade × USOIL` (companion ADR), `dedup.load_registry` parses it, 16/16 intake tests green.
- **Phase 2 (flipped Proposed→Accepted)** — ✅ SCHEMA.md "End-to-end consistency" note added; ✅ `docs/rejected_candidates.md` queryable-index pointer added; ✅ `feedback.py` `build_registry_entry()` extended to emit `class/role_tested/falsifier_failed/addback_condition` (+ optional `config_fingerprint`) with harness-suitable defaults (edge-failure/entry; add-back derived per §A), `append_rejection` forwards overrides, 3 round-trip tests added (`test_gate_controls.py`), 19/19 intake tests green. The harness-auto path now emits compliant entries with no caller change.
- **Phase 3 (optional enforcer, not blocking)** — write `lab/validation/concept_intake/check_registry.py` to assert every post-2026-06-14 entry carries the mandatory attributes. Until then, §10 hook #1 (grep) is the manual check. *(The web draft's `scripts/registry/check_registry.py` path does not exist and is not adopted.)*

---

## §10 — Audit hooks (runnable today)

```bash
# 1. New-entry schema compliance: every concept-intake-entry dated >= 2026-06-14
#    should carry class + role_tested + falsifier_failed. Lists entries missing them.
grep -n "concept-intake-entry" docs/rejected_candidates.md

# 2. Class/dedup separation intact: dedup parser still keys only on the composite axis
grep -n "mechanism_family\|instrument" lab/validation/concept_intake/dedup.py | head

# 3. Anti-degeneration: no edge-failure re-admitted without a NEW mechanism
grep -rin "readmit\|add-back\|addback" docs/rejected_candidates.md docs/adr/

# 4. Additions-only invariant: registry git history is append-only (no edited prior entries)
git log --follow -p -- docs/rejected_candidates.md | grep -c "^-.*concept-intake-entry"
# Expected: 0 (a deletion of a structured entry would show as a removed line)

# 5. Health-verdict inputs at next audit (2026-08-08): count rejections vs re-admissions
grep -c "date=" docs/rejected_candidates.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-06-14-rejected-candidate-patterns.md --type adr
# Expected: all 6 checks PASS

# Rule-0 anchors
git log -1 -- docs/rejected_candidates.md lab/validation/concept_intake/dedup.py

# Cited candidate dispositions exist in repo
grep -rl "Guardian Silver v1.0\|Sovereign\|BPC USDCAD\|USDCAD-RDM-001" docs/ ops/

# Schema forward-compat claim: dedup parser ignores unknown attributes
grep -n "_KV_RE" lab/validation/concept_intake/dedup.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-14 | Initial authoring (web session) — proposed schema *replacement*, confabulated `docs/registry/` + `scripts/registry/` paths | Joshua + claude.ai |
| 2026-06-14 | Reconciled to repo: schema *extension* (not replacement), paths corrected, `dedup.py` forward-compat verified, alternatives added | Claude Code |
| 2026-06-14 | §7 downstream landed (SCHEMA.md note, registry pointer, `feedback.py` extension + 3 tests); first §D entry written (`mean-reversion-spike-fade × USOIL`); status → `Accepted` | Claude Code |

## Addendum 2026-08-29 — dedup.py/feedback.py mechanism deleted 2026-07-11; registry topology moved on

`lab/validation/concept_intake/dedup.py` and `lab/validation/concept_intake/feedback.py` — the "live parser" and the `build_registry_entry()` machinery this ADR's §0/§7/§10 describe as the current mechanism — were deleted 2026-07-11 (`docs/adr/2026-07-11-gen1-pipeline-retirement.md` §7 Phase 2). The dedup and negative-rediscovery registry content was confirmed fully mirrored into `docs/rejected_candidates.md` before deletion. §7/§D/§10's references to `dedup.py`/`feedback.py` describe the pre-retirement mechanism for historical/provenance purposes only — they are not a live parser today. Live registry topology is now governed by `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md`; see `docs/rejected_candidates.md`'s DEAD SECTION note for the cross-reference this ADR never carried in-line. Never edit §1-§10 above in place — this addendum records the deletion and re-pointer only.
