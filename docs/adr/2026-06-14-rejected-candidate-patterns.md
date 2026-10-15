# 2026-06-14 — Rejected-candidate structural patterns: taxonomy, dedup axes, add-back gate

**Current routing:** the [August 30 overlay](#expression-ladder-and-register-routing) owns the
`N_expr` expression ladder and candidate WHY-rejected map. [Evaluation order](2026-08-30-evaluation-order.md#confirm-verdicts)
owns confirm verdicts. The original parser descriptions below are historical; see the August 29 addendum.

**Status:** Accepted (2026-06-14) — taxonomy, dedup-axis separation, add-back gate, and the additive schema extension are all adopted; the §7 downstream sweep landed (SCHEMA.md note + registry pointer + `feedback.py` field extension with a round-trip test, 19/19 intake tests green).
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-11-gen1-pipeline-retirement.md` - dedup.py/feedback.py mechanism only
**Superseded-in-part-by:** `2026-08-09-rejection-register-topology-and-bar-wiring.md` - registry topology only.
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): the two spent authoring notes (Reconciliation, D-S-A domain), the §6 downstream list, §7 and Verification removed; §0 condensed to a pointer; §10 reduced to its still-runnable hooks (#1, #3, #4); §A USOIL anchor cell corrected. Pre-trim text at blob `122fc0206e787034925c2ceb30d61894bfcc6d38` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Decision date:** 2026-06-14
**Authors:** Joshua + claude.ai (advisor, web session) → reconciled against repo by Claude Code
**Related:** [`2026-06-14-reject-usoil-rdm-spike-fader.md`](2026-06-14-reject-usoil-rdm-spike-fader.md) (companion — the worked exemplar this ADR's taxonomy classifies) · [`2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md) (the standing concept-intake-gate decision this extends)
**Layer:** methodology

---

## §0 — Rule 0 reads (production-source verification)

Read 2026-06-14 for the reconciled version: `docs/rejected_candidates.md` @ `b46f30c` (additions-only registry); `lab/validation/concept_intake/dedup.py` @ `c106807`, `feedback.py` @ `6bf0dff` and `SCHEMA.md` @ `6473809` (all deleted 2026-07-11 — see the August 29 addendum); [`2026-06-05-concept-admissibility.md`](2026-06-05-concept-admissibility.md). Full reads: [prior revision](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-06-14-rejected-candidate-patterns.md).

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
| **edge-failure** | Mechanism tested, placebo-controlled on the **canonical execution-TF** panel, net-negative or indistinguishable from a matched random null. | A **genuinely new entry mechanism** (distinct mechanism class). NOT: re-tune, subset/regime slice, stop-geometry tweak. | USOIL-RDM-001 (canonical re-run confirmed 2026-06-14 — see companion ADR) |
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

---

## §10 — Audit hooks (runnable today)

```bash
# 1. New-entry schema compliance: every concept-intake-entry dated >= 2026-06-14
#    should carry class + role_tested + falsifier_failed. Lists entries missing them.
grep -n "concept-intake-entry" docs/rejected_candidates.md

# 3. Anti-degeneration: no edge-failure re-admitted without a NEW mechanism
grep -rin "readmit\|add-back\|addback" docs/rejected_candidates.md docs/adr/

# 4. Additions-only invariant: registry git history is append-only (no edited prior entries)
git log --follow -p -- docs/rejected_candidates.md | grep -c "^-.*concept-intake-entry"
# Expected: 0 (a deletion of a structured entry would show as a removed line)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-14 | Initial authoring (web session) — proposed schema *replacement*, confabulated `docs/registry/` + `scripts/registry/` paths | Joshua + claude.ai |
| 2026-06-14 | Reconciled to repo: schema *extension* (not replacement), paths corrected, `dedup.py` forward-compat verified, alternatives added | Claude Code |
| 2026-06-14 | §7 downstream landed (SCHEMA.md note, registry pointer, `feedback.py` extension + 3 tests); first §D entry written (`mean-reversion-spike-fade × USOIL`); status → `Accepted` | Claude Code |
| 2026-10-15 | Spent §6-downstream/§7/Verification and the two authoring notes removed; §0 condensed; §10 reduced to still-runnable hooks; §A anchor cell corrected (USOIL re-run confirmed 2026-06-14); prior body pinned in Revision | ADR decay audit |

## Addendum 2026-08-29 — dedup.py/feedback.py mechanism deleted 2026-07-11; registry topology moved on

`lab/validation/concept_intake/dedup.py` and `lab/validation/concept_intake/feedback.py` — the "live parser" and the `build_registry_entry()` machinery this ADR's §0/§7/§10 describe as the current mechanism — were deleted 2026-07-11 (`docs/adr/2026-07-11-gen1-pipeline-retirement.md` §7 Phase 2). The dedup and negative-rediscovery registry content was confirmed fully mirrored into `docs/rejected_candidates.md` before deletion. §7/§D/§10's references to `dedup.py`/`feedback.py` describe the pre-retirement mechanism for historical/provenance purposes only — they are not a live parser today. Live registry topology is now governed by `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md`; see `docs/rejected_candidates.md`'s DEAD SECTION note for the cross-reference this ADR never carried in-line. The spent §0/§7/§10 content was removed or condensed 2026-10-15 (see Revision); the remaining original text is unedited.

## Addendum 2026-08-30 — fifth class, expression ladder and register routing

This overlay carries the Accepted [August 30 terminal-taxonomy decision](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-terminal-taxonomy.md),
consolidated here on 2026-09-08. The original sections remain historical under the August 29 addendum (spent §0/§7/§10 content removed or
condensed 2026-10-15; see Revision). Existing classes and add-back conditions stand except for the two
explicit amendments below. [Evaluation order](2026-08-30-evaluation-order.md#confirm-verdicts)
owns the four confirm verdicts and their precedence; [candidate contract](2026-08-30-candidate-contract.md#contract-fields-and-freezes)
owns the frozen discriminator and evidence object.

### Expression ladder and register routing

| Class | Definition | Add-back condition |
|---|---|---|
| **expression-failure** (fifth class) | A powered, pre-specified mechanism discriminator passes while the specific entry/exit expression fails confirm. | A materially new expression class on a declared structural axis, such as stop logic, exit family or holding-horizon class; its own candidate contract, fresh K and fresh holdout; citation of the failed expression and ordinal history. A parameter retune does not qualify. |

The **mechanism**, across contracts, owns `N_expr` (default 2) and the running attempt history.
Persist both on the same scope-routed row that owns the mechanism's rejection entries.
Each expression contract declares attempt *k* of `N_expr` and names every prior failed
expression class. Omitting or contradicting the ledger count makes it integrity-invalid
at the pre-confirm contract check; a later contract cannot reset the ordinal to one.

After `N_expr` independent expression classes produce `EXPRESSION-FAIL` while the
discriminator keeps passing, the standard ladder closes. If a recorded failure actually
fired on a cost or execution-geometry limb, move the mechanism entry to
`venue / cost-constraint` under that class's add-back. Otherwise it remains
`expression-failure` with its ladder closed. A further expression must be structurally
distinct from **every** failed class and requires operator ratification citing the full
failure history. Do not invent a cost cause, treat a retune as a new class or enlarge the
bound ad hoc. Changing the generally applicable bound requires a prospective governing
decision; record it under the repository's selective ADR rule.

**`venue / cost-constraint` add-back amendment:** retain the original cost-law/geometry
clearance and materially lower-cost-venue routes, and additionally admit a shape/geometry
that clears the failed limb with margin, or a venue whose rules remove the constraint.
Its definition is unchanged. This covers the pre-Explore payoff-shape limb in
[reachability](2026-08-30-evaluation-order.md#reachability).

| Disposition | WHY-rejected destination |
|---|---|
| `MARKET-NULL` | `edge-failure`; the existing genuinely-new-mechanism add-back stands. |
| `EXPRESSION-FAIL` | `expression-failure`, under the mechanism's ladder above. |
| Candidate-level pre-Explore `TRADEABLE-REACHABLE` kill on cost, latency, geometry or payoff shape | `venue / cost-constraint`, recording **“priors-derived, no mechanism test run.”** Neither edge-failure nor expression-failure is available from that evidence. |
| `EVIDENCE-VOID` | No WHY-rejected entry. Record the exhausted attempt on the contract; a fresh campaign needs a fresh holdout. |
| `ROLE-BLOCKED` | No WHY-rejected entry. Record on the contract; re-screen only when the scoped role state changes. |
| Post-confirm `VENUE-FAIL` | No candidate rejection. The evidence status remains `CONFIRMED`; record the edition-axis failure separately. |
| `CHANNEL-FAIL` | No candidate rejection. Record the channel consequence on its owner. |

Apply [D3's scope router](2026-08-09-rejection-register-topology-and-bar-wiring.md#2--decision)
after choosing the WHY class: per-direction/instrument mechanisms belong in the instrument
ledger; domain/cross-instrument failures in `docs/rejected_candidates.md`; methodology
failures in `docs/methodology/rejected_signals.md`. A WHY class alone never chooses a register.
These rules apply to post-August-30 confirm verdicts and frozen-candidate pre-Explore kills;
they do not turn pre-contract intake dispositions into confirm verdicts.

**Implementation limit:** the ordinal/ladder integrity check is unbuilt. The audit-tier
`scripts/check_instrument_rejection_coverage.py` selects single-instrument closures and
uses a narrower verdict parser: explicit `MARKET-NULL` is missed while `VENUE-FAIL` and
`CHANNEL-FAIL` can be treated as negative. A green check does not establish this full map.
The first consolidated review and unresolved checks are tracked in
[evaluation review](2026-08-30-evaluation-order.md#first-review-and-unresolved-obligations) and `STATE.md`.
