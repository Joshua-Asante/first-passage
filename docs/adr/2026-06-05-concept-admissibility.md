# ADR 2026-06-05 — Concept-admissibility contract (R&D pipeline stage-1 gate)

**Status:** `Accepted`
**Machinery-status:** ⚠ **RETIRED 2026-07-11; the decision is NOT withdrawn.** The tree this ADR
ratified (`validation/concept_intake/` → later `lab/validation/concept_intake/`) was deleted by
[`2026-07-11-gen1-pipeline-retirement.md`](2026-07-11-gen1-pipeline-retirement.md), which names this ADR as
"the concept-intake contract being retired". Read every present-tense claim below — including §Effective's
"already enforced in `validation/concept_intake/`" — as **historical**. The *doctrine* survives and is live:
an economic-mechanism requirement before any data is mined, and dedup against `docs/rejected_candidates.md`.
Its enforcement is now **discipline, not code** — the dedup attestation must be **executed** and its output
pasted (see that registry's own corrected §Queryable index, 2026-08-08).
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-07-11-gen1-pipeline-retirement.md`](2026-07-11-gen1-pipeline-retirement.md) (machinery only — the doctrine survives per the Machinery-status line above)
**Retain-until:** none
**Decision date:** 2026-06-05
**Authors:** Joshua + claude.ai (advisor)
**Supersedes:** none
**Related:** `docs/adr/2026-06-05-sweep-engine.md` (stage-3 companion) · `docs/adr/2026-06-04-lean-portfolio-meta-layer.md` (parent doctrine: the pass-rate objective) · `docs/notes/2026-06-05-rnd-pipeline-anchor-correction.md` (source-doc anchor correction)
**Layer:** infrastructure (R&D pipeline stage 1) — operationalizes methodology doctrine; does not author it

---

## §0 — Rule 0 reads (production-source verification)

This ADR ratifies a contract that is already built and enforced in-repo; §0 lists the production sources read before authoring. The decision being recorded is the *admissibility contract* — the `admissibility_contract.yaml` values are canonical, this ADR is the *why*. No `.pine` reads are involved (the gate is hermetic on a public clone via the pinned `locked_book`, so no gitignored-source citation chain is needed).

- `validation/concept_intake/SCHEMA.md` — anchor `0f5a05d` (verified `git log -1` on 2026-06-05). The rationale body being lifted; its status line directs this lift "once the §2.5 controls pass."
- `validation/concept_intake/admissibility_contract.yaml` — anchor `0f5a05d`. **Canonical** machine-enforceable contract: 6 required fields, 6 forbidden fields, the mechanism/falsifier/portfolio_fit marker contracts (`mechanism.min_words=8`, `falsifier.min_words=6`, `portfolio_fit.min_words=6`), `dedup.near_match_threshold=0.45`, and the 4-row `locked_book`.
- `validation/concept_intake/check_concept.py` — anchor `0f5a05d`. The enforcer (mechanical required/forbidden-field + semantic-marker checks).
- `validation/concept_intake/dedup.py` — anchor `0f5a05d`. Composite-key dedup; **reads `docs/rejected_candidates.md` at call time** and raises (not CLEAR) if the registry is missing.
- `validation/concept_intake/contract.py` — anchor `0f5a05d`. Deep-freezes the loaded contract to `MappingProxyType`/tuples; assignment raises `ContractMutationError` (the no-self-tune property).
- `docs/rejected_candidates.md` — anchor `0f5a05d`. The registry the §2.4 feedback hook appends to and dedup reads (loop-closure target; current entry: Guardian-family-on-XAGUSD).
- `docs/adr/2026-06-04-lean-portfolio-meta-layer.md` — anchor `c5df37c` (2026-06-04). Parent doctrine: the challenge-window pass-rate objective this gate pushes upstream to proposal time.

**Lift precondition (verified):** `pytest validation/concept_intake/` → **14 passed** on 2026-06-05. SCHEMA.md's lift condition ("once the §2.5 controls pass") is met.

---

## §1 — Context

The R&D-automation architecture (concept → codify → sweep → validate) places two gates around the expensive middle. The *back* gate — the multiple-testing-corrected validation harness (`validation/`, CPCV/DSR/PBO/permutation) — stops overfit survivors after compute has already been spent. The *front* gate is this concept-intake contract: it runs **before any data is mined**, so the economic-mechanism requirement costs nothing and is the single highest-leverage filter against data-mined garbage. The build (`validation/concept_intake/`) was completed and §7-accepted on 2026-06-05 (14 controls pass); SCHEMA.md was authored as the build-time rationale body with an explicit instruction to lift its *decision* into a dated ADR once the controls passed. This ADR is that ratification — the decision is recorded separately from the build per handoff doctrine.

**Decision driver (one sentence):** the gate is now built, enforced, and control-verified, so its admissibility rules must be ratified as a standing decision (with a falsifier and forbidden-moves boundary) rather than living only as a build artifact's prose.

---

## §2 — Decision

**Decision:** The concept-intake gate's **admissibility contract** is ratified as the front gate of the R&D-automation pipeline. A concept record is admissible **iff** it carries all six required fields (`mechanism`, `falsifier`, `regime`, `portfolio_fit`, `logic_family_hint`, `provenance`), carries **no** parameter-grid field, and satisfies three semantic contracts enforced by `check_concept.py`:

1. **Economic mechanism, not a backtest observation** — `mechanism` is ≥8 words and, if it uses a backtest-performance phrase, must also carry an economic-claim marker (`because` / `exploits` / `inefficiency` / `order flow` / …). A record reducing to "backtested well" FAILS.
2. **Binary, observable, self-immunization-free falsifier** — `falsifier` is ≥6 words with a condition marker AND a death marker, and contains **no** unfalsifiable marker (`always works`, `in all regimes`, `eventually`, …). Mirrors the skill-side `check_brief.py` falsifier check.
3. **Non-trivial portfolio complementarity, not standalone edge** — `portfolio_fit` is ≥6 words naming decorrelation / gap-coverage / regime-complementarity vs the existing four (Guardian/Striker/Aegis/NAS100); a standalone-Sharpe-only claim FAILS (the lean-portfolio pass-rate objective pushed upstream).

Dedup uses the composite key **(mechanism_family × instrument)**: an exact match is a hard `DUPLICATE`; a high mechanism-text Jaccard overlap (≥ `0.45`) is a `NEAR_MATCH` routed to **human review** (never auto-rejected); both are checked against the pinned `locked_book` and against `docs/rejected_candidates.md` read at call time. The contract is loaded **read-only**; the gate enforces it and never tunes it — threshold/required-field changes route through programme-audit by editing the YAML in a reviewed commit and bumping `contract_id`/`version`.

**Effective:** immediately upon acceptance (the contract is already enforced in `validation/concept_intake/`).
**Scope:** every concept submitted to the R&D-automation pipeline. Proposers are human/advisor-sourced only (Claude Tech-Advisor or Joshua); autonomous generation is out of scope.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Free-text proposals, human review only (no mechanical gate)** | Doesn't scale, re-litigates already-rejected directions every cycle (no registry read), and gives no hermetic behavior on a public clone. The mechanical required/forbidden-field + marker checks are cheap and catch the common failure shapes deterministically. |
| **Post-hoc filtering only (rely on the back-gate harness)** | Spends codification effort and sweep compute on bad concepts before rejecting them. The entire leverage of a front gate is that it runs *before* data is mined — the economic-mechanism requirement is then free. |
| **Autonomous concept generation feeding the gate** | Forbidden move #2 (generation out of scope). A generator that also gates its own output is the generator-gates-itself degeneration; keeping generation human/advisor-sourced preserves an independent proposer. |
| **Runtime-tunable thresholds** | Forbidden move #1. A gate that can adjust its own thresholds will tune them to pass a borderline concept. The read-only `MappingProxyType` freeze (`contract.py`) makes self-tuning raise rather than silently succeed. |
| **Pre-specifying a parameter grid in the concept record** | Pre-overfitting — the sweep (stage 3) finds params. `forbidden_fields` rejects `parameter_grid`/`params`/`grid`/… at parse time (`pydantic extra='forbid'`). |
| **Status quo — no front gate** | The pipeline's expensive middle would have no admissibility filter; data-mined garbage would consume codification + compute, and rejected directions would regenerate indefinitely. |

---

## §4 — Falsifier (revert trigger)

This gate is a calibration; it can be wrong by being non-discriminating (admits garbage) or over-tight (rejects genuine concepts).

**Hypothesis (H):** the admissibility contract discriminates good concepts from data-mined ones cheaply — i.e. concepts it admits clear the downstream validation harness at a materially higher rate than concepts it rejects, and it does not kill genuine concepts. The falsifier below is the binary condition under which that hypothesis is treated as falsified and the contract is revised.

**Revert trigger (binary):** If **either** of the following is observed, the hypothesis is falsified, the contract's markers/thresholds are revisited, and `contract_id`/`version` bumped (the gate is *not* silently edited):
- **No-signal:** across the first **≥10 concepts admitted** by the gate, the admitted set's downstream validation-harness pass-rate is statistically indistinguishable from a sample of gate-*rejected* concepts re-run through the harness (the gate adds no discrimination), **or**
- **False reject:** a gate-rejected concept is admitted via a documented manual override and **survives the back-gate harness** (a genuine concept the contract killed), **or**
- **Dedup mis-fire:** a `DUPLICATE`/`NEAR_MATCH` verdict is overturned on human review as a genuine new mechanism in ≥2 separate cycles (the `0.45` Jaccard threshold or the family-alias map is mis-calibrated).

**Revert action:** open a programme-audit on the concept-intake contract; supersede this ADR with a new dated ADR carrying the revised contract version. Do **not** edit the thresholds in place.

**Trigger check schedule:** evaluated at each R&D-pipeline cycle review, and unconditionally once the cumulative admitted-concept count first crosses 10.

---

## §5 — Forbidden moves (under this ADR)

- **Tuning the contract to admit a borderline concept** — forbidden move #1. The YAML is read-only at runtime (`ContractMutationError` on assignment); any threshold/field change is a reviewed YAML commit through programme-audit, never a gate-side adjustment.
- **Silently editing thresholds in place instead of superseding** — `p`-hacking at the gate layer (Known Trap #12). A wrong threshold is fixed by bumping `contract_id`/`version` + a superseding ADR, not an in-place edit.
- **Adding autonomous concept generation** — forbidden move #2. Proposers stay human/advisor-sourced; a self-generating, self-gating loop is out of scope.
- **Pre-specifying a parameter grid** — the sweep finds params (`forbidden_fields`); admitting a record that smuggles a grid pre-overfits the pipeline.
- **Auto-rejecting a `NEAR_MATCH`** — near-matches route to human review only. A near-rephrasing may be a genuine variant; auto-reject would re-introduce the false-negative the §4 trigger guards against.
- **Letting the rejected-candidates registry become append-only** — dedup must read `docs/rejected_candidates.md` at call time. A registry written but never read is a graveyard, not a control; `dedup` raising on a missing registry (rather than returning CLEAR) is the deliberate guard.
- **Re-proposing a `DUPLICATE` with new parameters instead of new mechanism evidence** — re-proposal requires new *mechanism* evidence (the rejected-candidates re-proposal rule), not a parameter tweak.

---

## §6 — Consequences

**Positive consequences:**
- The cheapest, highest-leverage filter: the economic-mechanism requirement runs before any data is mined, so data-mined "backtested well, no why" concepts are stopped for free.
- Loop-closure: harness rejections flow back to `docs/rejected_candidates.md` (§2.4 feedback hook) and dedup reads it every call, so the pipeline cannot regenerate an already-rejected direction.
- Hermetic on a public clone: `locked_book` is pinned in the contract, so dedup against the four locked strategies works without the gitignored Pine source.
- End-to-end schema consistency: a record passing `check_concept.py` carries exactly the fields `dedup` needs and the feedback hook writes in the shape `dedup.load_registry` reads (validate → dedup → feedback share one schema).

**Negative consequences (real cost, not theatrical):**
- The semantic checks are keyword/marker-based, so the marker lists are a maintenance surface that can drift and must be revised through programme-audit (not casually).
- A human-review queue exists for `NEAR_MATCH` verdicts and thin-`regime` WARNs — the gate is not fully autonomous by design.
- The gate is **necessary, not sufficient**: a well-worded concept with no real mechanism can pass the marker checks. This is accepted because the back-gate harness catches overfit survivors downstream — defense in depth, not a single gate.

**Risks (probabilistic, distinct from costs):**
- *Gaming via economic-sounding prose* — a proposer writes mechanism-flavored words with no real claim. Mitigation: human review still reads admitted records; the harness is the second gate.
- *Jaccard threshold mis-calibration* (`0.45`) — mis-flags a genuine variant as `NEAR_MATCH`. Mitigation: `NEAR_MATCH` → human review, never auto-reject; the §4 dedup-misfire trigger escalates if it recurs.

**Downstream artifacts that need updating (this ADR's §7):**
- `validation/concept_intake/SCHEMA.md` — status line repointed from "lift into `docs/adr/NNN-concept-admissibility.md`" to this dated ADR (lift complete).
- `validation/concept_intake/admissibility_contract.yaml` — header comment "becomes the body of `docs/adr/NNN-concept-admissibility.md`" repointed to the dated path.

---

## §7 — Implementation plan

This ADR is largely **policy ratification** — the gate is already built, enforced, and control-verified. The only mechanical edits are the two doc-pointer updates that retire the `NNN` placeholder now that the dated ADR exists.

- **Phase 0** — §0 reads re-verified current at authoring time (all at `0f5a05d`; lean-portfolio at `c5df37c`); `pytest validation/concept_intake/` → 14 passed.
- **Phase 1** — repoint `SCHEMA.md` status line and `admissibility_contract.yaml` header comment to this ADR's dated path.
- **Phase 2** — grep-sweep for the `NNN-concept-admissibility` placeholder; confirm no stale references remain.
- **Phase 3** — verification block executes; status `Accepted` (downstream sweep complete).

---

## §10 — Audit hooks (runnable)

```bash
# The gate is enforced and control-verified
python -m pytest validation/concept_intake/ -q
# Expected: 14 passed

# The contract is the canonical source (this ADR is the why); confirm the
# load-bearing values this ADR quotes still match the YAML
grep -nE "min_words:|near_match_threshold:|^required_fields:|^forbidden_fields:" \
  validation/concept_intake/admissibility_contract.yaml
# Expected: mechanism/falsifier/portfolio_fit min_words 8/6/6; near_match_threshold 0.45

# No LIVE doc still points at the NNN placeholder as a pending TODO (Phase 2
# sweep). Excludes this ADR (which quotes the retired "NNN" string descriptively
# in §6/§7/§10) and docs/SESSIONS.md (a historical timeline entry, not a live
# pointer). Trap M-AHF: the hook matches the artifact's stored form, not intent.
grep -rn "NNN-concept-admissibility" docs/ validation/ 2>/dev/null \
  | grep -v "docs/adr/2026-06-05-concept-admissibility.md" \
  | grep -v "docs/SESSIONS.md"
# Expected: no matches (the CC-HANDOFF doctrine note was repointed to this ADR)

# SCHEMA + contract pointers resolve to this dated ADR
grep -n "2026-06-05-concept-admissibility" \
  validation/concept_intake/SCHEMA.md \
  validation/concept_intake/admissibility_contract.yaml
# Expected: one hit in each

# The no-self-tune property is test-pinned (read-only contract raises on mutation)
grep -rn "ContractMutationError" validation/concept_intake/
# Expected: raised in contract.py, asserted in a control

# Dedup reads the registry at call time (loop-closure not a graveyard)
grep -n "rejected_candidates" validation/concept_intake/dedup.py
# Expected: load path present

# §4 trigger reminder: re-evaluate once cumulative admitted concepts > 10
```

---

## Verification

```bash
# Discipline checks (mechanical) — canonical skill-side checker
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/adr/2026-06-05-concept-admissibility.md --type adr
# Expected: all 6 checks PASS
# Repo-side subset (CI-accessible): scripts/check_brief.py <file> --type adr

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format='%h %ci' -- validation/concept_intake/admissibility_contract.yaml
$ python -m pytest validation/concept_intake/ -q   # 14 passed (lift precondition)

# Downstream artifact update verification (§6 list)
$ grep -n "2026-06-05-concept-admissibility" \
    validation/concept_intake/SCHEMA.md \
    validation/concept_intake/admissibility_contract.yaml
# Expected: both repointed (NNN placeholder retired)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-05 | Initial authoring — lifts `validation/concept_intake/SCHEMA.md` rationale into a ratified decision after the §2.5 controls passed (14/14) | Joshua + claude.ai |
