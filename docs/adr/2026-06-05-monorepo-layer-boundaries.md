# ADR 2026-06-05 — Monorepo with enforced layer boundaries (`core / governance / lab / ops`)
**Status:** Accepted - ratified 2026-06-05 by PO (Joshua); execution-time amendments 2026-06-06, 2026-09-11 and 2026-09-17; body trimmed 2026-10-15 (see Revision).
**Decision date:** 2026-06-05
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): drafting blockquote, §0 read table, §2.1 path inventories and amendment items 2–3, §2.4/§2.5 execution detail, §4 H1/H2 bodies, §5 items 3–5, §6 branch detail, §7 execution bullets, §8 seam evidence, §10 hooks 3–13, the re-check cadence and the pre-ACCEPT Verification removed; H3 re-gate retired (cadence retired 2026-09-08; satisfied in fact). Decision, §2.2–§2.3 with amendments, §2.6 rule, §2.7 and the H3 standard unchanged. Pre-trim text at blob `c682a7ccb9c6bb0630af7bf72503c35c852f9ad6` (commit [`4121e84c95f4990b71962e3b9570c4c3fad88426`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/adr/2026-06-05-monorepo-layer-boundaries.md)).

> Ratified 2026-06-05; Phase C executed (PR #138): H1 0 illegal edges; H2 locked files byte-identical. Drafting revisions and provenance: prior text (Revision).

---

## §0 — Rule 0: Production reads

Verified on-disk 2026-06-05 against `origin/main` `0ec6e11` (PR#136); the read table is in the pre-trim text (Revision). Current enforcement sources: `scripts/check_boundaries.py`, `scripts/repo_map_layers.yml`.

---

## §1 — Context & doctrine linkage

`multi_firm_operations` began (per `CLAUDE.md` Purpose) as a lot-size multiplier lookup tool — `firm_rules` + `accounts` + `csv_parser` + `cli`. It has since accreted ~five distinct concerns into one flat tree: MC simulation, the methodology/decision-artifact framework, a validation/sweep R&D harness, live execution journaling (ECR), and the Copygram automation pipeline.

The 2026-06-05 partition review (Q-SPLIT-1, then a second pass) found that the originally-proposed R&D-vs-ops split cuts along the wrong axis. The friction that actually hurts is **mutability**: experimental churn (sweep engine, concept-admissibility, in-flight investigations) living in the same flat namespace as **locked production risk controls** (Guardian v5.5 source, `dd_protection` constants, MC anchors). R&D-vs-ops cuts *across* that — `portfolio_mc.py` is research but locked-load-bearing; `validation/sweep/` is research but freely mutable.

This ADR installs a four-layer boundary on the mutability axis, inside one repo, and makes the boundary machine-enforced. It also homes the governance meta-layer that the Lean Portfolio ADR (2026-06-04) installed conceptually but left without a physical location.

Standing doctrine this connects to: Rule 0 (audit-first — §0 above, and the rev.-3 correction is itself a Rule-0 win: production code falsified a doc claim); The Algorithm (delete → simplify → automate — archive eviction and context-prune are *delete*, the enforcement check is *automate*); the manifest-integrity gate (2026-05-10, scope extended here); forward-asymmetry (this is dev-stream work — it must not perturb the still-broken ECR op-stream falsifier; hence the relocation-only constraint on `live_journal/`).

---

## §2 — Decision

Adopt a single repository partitioned into four layers on the mutability axis, with a machine-enforced dependency contract. Reject the two-physical-repo split (§2.7).

### 2.1 — The four layers

| Layer | Mutability | Holds | May import |
|---|---|---|---|
| **`core/`** | Locked. Changes require deliberate manifest regeneration (§2.4). | Shared engines, frozen controls, locked strategy sources and backtest panels | stdlib + third-party **only** — nothing internal |
| **governance** (**root-resident — no physical `governance/` dir**; see amendment) | Append-with-discipline (the meta-layer). | Docs, skills (markdown discipline), `.github/`, discipline scripts and root files — classified-not-moved | `core/` + stdlib |
| **`lab/`** | Free churn. | Research: analysis, validation, codification and research scripts | `core/`, `governance/` |
| **`ops/`** | Operational; changes are live-impacting but not lock-gated. | Operational services, live journaling and operational state | `core/`, `governance/` |

Current per-path classification: `scripts/repo_map_layers.yml` ([REPO_MAP](../../REPO_MAP.md) §1–§2).

`core/` is the sink of the dependency graph: everything may depend on it; it depends on nothing internal. Governance sits just above core. `lab/` and `ops/` are the two application layers — both rest on core+governance and are **mutually isolated**.

> **Execution-time amendment (2026-06-06, Phase C — status remains ACCEPTED).** Reconciling this model with the tree as physically built, recorded here so the canonical record matches reality (not silently changed):
> 1. **Governance is entirely root-resident — there is no physical `governance/` directory.** `docs/`, `.claude/`, `.github/`, the discipline `scripts/`, and the root files stay at repo root, **classified-not-moved**. Rationale: governance joins no import contract among application code, and relocating it breaks tooling (the harness requires `.claude/{skills,settings.json,commands}` at fixed paths; GitHub requires `.github/workflows/`; every `check_*`/`validate_*` script computes `REPO_ROOT` from `scripts/` at root and is invoked `python scripts/X.py`) *and* breaks hundreds of doc cross-links — for **zero** contract benefit. The physical partition is `core/ lab/ ops/` + root-resident governance; `check_boundaries.py` classifies the root-resident `.py` per `REPO_MAP.md` §2.1.

### 2.2 — The dependency contract (the enforced boundary)

```
                 governance ──▶ core
                    ▲             ▲
        ┌───────────┘             └───────────┐
       lab ───────────▶ core ◀─────────────── ops
        │           (+ governance)             │
        └──────────────  ✗  ───────────────────┘
                  lab ↔ ops : FORBIDDEN
```

Legal edges: `governance→core`; `lab→core`; `lab→governance`; `ops→core`; `ops→governance`. **Illegal:** any `core→{governance,lab,ops}`; any `governance→{lab,ops}`; any direct `lab↔ops`.

The load-bearing property is the **lab↔ops isolation**: experimental R&D churn cannot reach into live operational code, and operational changes cannot silently depend on in-flight research. This is the safety invariant the flat tree could not express. The one real present-day violation of it — `parity_check.py:222` (ops) → `analysis/.../tv_export_loader` (lab) — is dissolved at the move by widening the parser into `core/` (§8 Q-d), not by relaxing the contract.

### 2.3 — Enforcement mechanism

`scripts/check_boundaries.py` — an **AST-based** import scan (not grep; must catch aliased, relative, `from X import Y`, AND lazy/in-function forms — the in-function form is exactly what the rev.-1/2 grep missed at `parity_check.py:222`). Maps each module to its layer by path prefix, asserts no edge violates §2.2, exits non-zero on violation. **It must additionally assert cross-layer module-name uniqueness:** because the move puts all four layer roots on `sys.path` (the flat-module import strategy), two top-level modules/packages sharing a name across layers would make both the scanner's name→layer index AND Python's own import resolution silently pick the wrong file — so a name appearing in >1 layer is a hard error (`ambiguous module '<name>' across layers {a,b}`). Verified zero collisions in the current tree; the assert keeps a future one loud. Wired into the existing `scripts/githooks/pre-commit` and `.github/` CI alongside the `check_*.py` family. `tests/` is **exempt** (integration tests legitimately cross layers; §8 Q-c).

> **Execution-time amendment (2026-09-11, status remains ACCEPTED).** PR #341 (sections 1–2 of a larger #337 split) replaced the bare top-level `name→layer` lookup this section originally described with **path resolution**, reconciling the record to the build:
> 1. **Path resolution, not a name-to-layer dict.** `build_index()` resolves every importable name to its actual repository-relative path(s) — under the bare repo root (full dotted path) and under each documented flat import root — instead of a single `name → layer` mapping. `layer_of_file()` is then applied to the resolved path, so `_first_party_targets` yields `(line, name, path)` and legality is checked from that path's layer, not a name lookup.
> 2. **Flat-root mirror.** `FLAT_IMPORT_ROOTS = ("core", "lab", "ops", "ops/c1_rail", "ops/c1_signal_daemon", "scripts")` in `check_boundaries.py` names every root that is import-root-flat in practice (pytest via `pyproject.toml`, the rail entry points, direct `scripts/*.py` execution). It is mirrored in `scripts/repo_map_layers.yml` under `flat_import_roots:` and cross-checked by `scripts/check_repo_map_layers.py`, including that script's no-PyYAML fallback parser (`_parse_simple_yml`) — the same drift gate §2.3's name/prefix maps already used.
> 3. **Collision handling is layer-scoped, not path-scoped.** A name resolving to paths in more than one *layer* is still the hard `NAME COLLISION` this section originally specified, now reported with every candidate path. A name resolving to multiple paths within the *same* layer is not flagged: §2.2's legal-edge contract depends only on source/target layer, and every candidate there shares one layer, so the ambiguity cannot change the verdict.
> 4. **Relative imports are resolved, not blanket-legal.** `from . import x` / `from .. import x` now resolve from the importing file's package path to a concrete target and run through the same layer check as an absolute import, replacing the prior "relative ⇒ same-layer ⇒ always legal" shortcut — that shortcut could not see a relative import inside a mixed-layer `scripts/` file cross layers (e.g. governance-classified `scripts/check_brief.py` doing `from . import lock_event_hook`, which resolves to the ops-classified `scripts/lock_event_hook.py`). A relative import whose level walks above the repository root is reported distinctly (`INVALID RELATIVE`), not conflated with an ordinary unresolved import.
> 5. **Unresolved first-party imports fail closed.** An import rooted at a known first-party name (`core`, `lab`, `ops`, `scripts`, or any other resolved index root) that does not resolve to an actual path is now a reported failure (`UNRESOLVED first-party import`), distinct from an ordinary external/stdlib import, which remains silently ignored.
> 6. **Scope boundary unchanged.** The scanner remains a static AST import scan. Dynamic imports (`importlib.import_module`, `__import__`, string-built module paths) and filesystem reads (`open()`, `Path.read_text()`, config-driven loading) stay outside its coverage — the scanner checks only statically visible `import` / `from import` edges; this detection limit does not relax §2.2's dependency contract.
>
> §2.2's legal-edge contract is unchanged by this amendment: `governance→core`; `lab→{core,governance}`; `ops→{core,governance}`; same-layer; `lab↔ops` forbidden. `tests/` remains exempt (§8 Q-c).

> **Execution-time amendment (2026-09-17, status remains ACCEPTED) — one layer-map definition.** Item 2 above (and the 2026-08-23 pain-point packet P5 that created the gate) described the name/prefix maps and `FLAT_IMPORT_ROOTS` as hard-coded in `check_boundaries.py` with `scripts/repo_map_layers.yml` as a *mirror* cross-checked by `check_repo_map_layers.py`. Operator direction 2026-09-17 (configuration-as-code consolidation) replaced the mirror with a single definition, reconciling the record to the build:
> 1. `scripts/repo_map_layers.yml` is the only copy of `app_layer_prefix`, `governance_prefixes`, `scripts_layer` and `flat_import_roots`. `check_boundaries.py` loads it at import (`load_layer_maps`, PyYAML — a declared project dependency, the footing the check tier already stands on via `markdown_it`); `check_repo_map_scripts_table.py` reads the same file for REPO_MAP §2.1. The no-PyYAML fallback parser named above is retired with the compare it served.
> 2. `check_repo_map_layers.py` (gate `repo-map-layers`, id and tier unchanged) is now a schema gate — required sections and types, prefix/layer rules, an app prefix naming its own directory, tracked-script and directory existence — rather than a dict↔YAML compare. This supersedes P5's "keep the hard-coded dicts; compare them" instruction.
> 3. `EXEMPT_PREFIXES` (scan scope) and `LEGAL_EDGES` (the §2.2 contract) stay in the scanner; they are not layer classification. §2.2 is unchanged.

### 2.4 — Manifest gate scope = `core/` only

The manifest-integrity gate guards `core/` (Pine `MANIFEST.sha256`, `PORT_MANIFEST.sha256`, data `SHA256SUMS`); `lab/`, `ops/` and governance carry no manifest friction. Scope and commands: [manifest-integrity ADR](2026-05-10-manifest-integrity-gate.md) and AGENTS.md §Vendor-data integrity gate.

### 2.5 — Archive-eviction policy (standing rule, not a one-time cleanup)

Closed loops leave the working tree; retrieve them from tags/history. Retention test: [operational rules §16](../operational_rules.md#16-retention--an-artifact-must-earn-its-place-and-deletion-is-classified-by-execution-not-by-folder).

### 2.6 — State-file separation policy (the fix for append-only-log degeneration)

Canonical context files carry **current state only**. The root agent file is `AGENTS.md` (`CLAUDE.md` retired 2026-09-20); root-document roles are owned by [Rule 7](../operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror) and the [five-root charter](2026-07-16-root-doc-charter-dedup.md). It carries current constraints and pointers. The historical challenge-era MC triple stays there, labelled historical, only because `ops/recall/guard.py` reads it as its denylist source. The historical narrative — MC-anchor evolution, superseded Q-SWAP closures, supersession/retraction chains — moves to dated history files (`docs/mc_anchor_history.md`, classified governance, root-resident). The prune is **lossless by verification, not assertion**: every line removed from `CLAUDE.md` must be **content-preserved** in `mc_anchor_history.md` — extracted byte-identically where possible, but a prune executed *inside* the move may re-point moved-tree paths in the retained text (e.g. `data/`→`core/data/`), so the gate is information-preservation, not strict byte-verbatim (reconstruction check in the handoff Step C1). This is a **standing rule**: without it, the prune is a one-time cleanup that re-accretes (brief-authoring trap: belt grows, never prunes).

### 2.7 — Monorepo, not two physical repos (explicit rejection + revisit trigger)

The two-repo split is rejected. Two repositories force `core/` + `governance/` to be versioned, published, and pinned, and turn any cross-layer change into a coordinated multi-PR operation — a dependency-management tax. For a single operator with no team-isolation requirement, that tax exceeds its benefit. The enforced-boundary monorepo delivers the isolation property (§2.2) and the protection property (§2.4) **without** the tax.

Critically, this decision is **forward-compatible with a future split, not a dead end**: the §2.2 contract is exactly the precondition a physical split would require. If `lab/` ever needs independent publication (e.g. open-sourcing the research layer while keeping `ops/` private), the lab↔ops isolation already in force makes the physical extraction mechanical at that point. **Revisit trigger:** a concrete need to clone/publish one application layer without the other.

---

## §4 — Falsifiable hypotheses

This ADR carries three falsifiable hypotheses (H1–H3), each with its own falsifier.

**H1/H2** — each hypothesis verified at Phase C (0 illegal edges; locked files byte-identical). Bodies and falsifiers: pre-trim text (Revision).

**H3 (load-bearing over time — checkable at audit cadence).** The boundary is load-bearing, not ceremony, if within two `programme-audit` cycles either (a) `check_boundaries.py` has blocked at least one illegal-import attempt in CI/pre-commit, or (b) the layer assignment in `REPO_MAP.md` is referenced in at least one subsequent structural decision.

> **Falsifier:** two audit cycles elapse with the check never firing **and** never referenced **and** files visibly drifting across layers (the check being bypassed or too weak). Then the enforcement decayed to nominal — disposition: strengthen the check or delete it per The Algorithm. (A check that never fires *because deterrence works* is not falsified by (a) alone — hence the conjunction with drift evidence.)

Satisfied in fact: the `boundaries` gate is live (`scripts/gates.yml`) and later structural ADRs cite it; the audit cadence that scheduled the re-check was retired 2026-09-08.

---

## §5 — Forbidden moves (genuinely tempting, ruled out)

1. **Relax the §2.2 contract to make `check_boundaries.py` pass.** Defeats the decision. A real illegal edge is a finding (H1 falsifier), not a contract to loosen. (Note the distinction the rev.-3 correction makes load-bearing: *re-classifying* `validate_candidate.py`→lab or *widening* `tv_export_loader`→core is **not** relaxation — it is correct placement of a misfiled artifact. Relaxation would be adding `lab↔ops` to the legal-edge set.)
2. **Split into two physical repos "for cleanliness."** The rejected alternative (§2.7). Tempting for tidiness; pays a dependency-management tax with no offsetting single-operator benefit. The monorepo already preserves the option to split later.
6. **Add a fifth layer or sub-layers now.** Four is the claim. Over-partitioning is ceremony until a concrete edge forces it. Resist `core/`→`core/locked/`+`core/shared/` etc. absent a real need.
7. **Decide `data/` or `tests/` homes by convenience to avoid the question.** These were genuine open seams (resolved in §8); resolve any *new* seam explicitly in `REPO_MAP.md`, don't default silently.
8. **Trust a grep to prove `lab↔ops` clean.** The rev.-1/2 §0 did, and missed the lazy `parity_check.py:222` import. Use the AST-aware probe (§10) before declaring the partition satisfiable.

---

## §6 — Gate / closure criteria (binary)

**RESOLVED** at Phase C (PR #138): H1 and H2 held (§4). The FALSIFIED/AMBIGUOUS branches and the H3 decay re-gate are in the pre-trim text (Revision); the re-gate is retired (audit cadence retired 2026-09-08; satisfied in fact, §4).

---

## §7 — Consequences

- **`REPO_MAP.md` becomes the standing layer map** — the authoritative path→layer assignment and the human-readable companion to `check_boundaries.py`'s path-prefix logic. (The prior REPO_MAP-as-deletion-input chain is dead: a parallel session retired both `deletion_candidate_report.py` (`a9d16d0`) and the old REPO_MAP (`f341648`). This is a fresh, purpose-rebuilt map.)

---

## §8 — Seams resolved, with evidence

Seams Q-a/b/c were resolved in rev. 2; Q-d/e in rev. 3. Dispositions below; the per-seam evidence is in the pre-trim text (Revision).

- **Q-a — `data/` home → SPLIT (`core/data/` panels, `ops/data/` state);** `accounts.py`/`cli.py` moved to `ops/` with the state they manage.
- **Q-b — skills home → all `.claude/skills/` to `governance/`** as markdown discipline; the duplicate skill-bundled `journal_review.py` was removed at the move, so governance carries no importable internal-dependent code.
- **Q-c — `tests/` → top-level, contract-EXEMPT (confirmed, not defaulted).** A single suite imports across all three application-relevant layers simultaneously — `from accounts`/`from dd_protection`/`from portfolio_mc` (core), `from analysis.oanda_stage1` (lab), `from live_journal.* import …` (ops). Integration tests cross-cut layers by nature; `test_ecr_rolling.py` alone spans core+ops. Colocating tests by layer is impossible without splitting individual test files, and subjecting `tests/` to the contract would forbid legitimate integration coverage. `check_boundaries.py` exempts `tests/`.
- **Q-d — `tv_export_loader.py` home → CORE (widen) [rev. 3].** Shared TV-CSV parser widened into `core/` (ops→lab edge dissolved).
- **Q-e — two classification calls [rev. 3].** `codification/` → `lab/codification/`; `scripts/validate_candidate.py` → lab (the imports decide the layer).

**Nothing remains open in this ADR.** The Q-SWAP SNAG disposition is out of scope (handoff Step B2). The `journal_review.py` dedup (Q-b) and the `tv_export_loader` widening (Q-d) are tracked, evidence-based moves — not open questions.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Boundary contract green, no relaxation (H1) — the core invariant
python scripts/check_boundaries.py && echo "boundaries OK" || echo "ILLEGAL EDGE — H1 falsifier, do not relax contract"

# 2. core/ is a true sink: nothing under core/ imports another internal layer
grep -rnE "import (lab|ops|governance)|from (lab|ops|governance)" core/ 2>/dev/null \
  && echo "VIOLATION — core importing upward" || echo "core sink OK"
```
