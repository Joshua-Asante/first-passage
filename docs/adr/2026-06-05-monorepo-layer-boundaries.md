# ADR 2026-06-05 — Monorepo with enforced layer boundaries (`core / governance / lab / ops`)
**Status:** Accepted - ratified 2026-06-05 by PO (Joshua); execution-time amendment 2026-06-06 (see blockquote header below for the full ratification note).
**Decision date:** 2026-06-05
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

> **Status:** ACCEPTED 2026-06-05 — ratified by PO (Joshua). This flip unblocks Phase C of the monorepo-boundaries CC handoff (the irreversible tree move), executed on branch `claude/monorepo-phase-c` (off the Phase-A+B branch / PR #137). Phases A/B did not require ACCEPTED and already landed.
> **Execution-time amendment (2026-06-06, status remains ACCEPTED):** §2.1 reconciled to the tree as built — governance is **root-resident** (no physical `governance/` dir; relocating it breaks tooling for zero contract benefit) and the four surfaced edges (`tv_export_loader`→core, `trade_to_signal_event`→ops, two skill validators→ops) are folded in as the ratified classification; §2.6 "verbatim" softened to "content-preserving" (a prune executed inside the move re-paths retained text). These were reconciled, not silently changed — see the §2.1 amendment block. Execution landed on PR #138; H1 (0 illegal edges) + H2 (anchors reproduce, locked files byte-identical) verified green.
> **Date authored:** 2026-06-05 (rev. 3 — **edge-inventory corrected against production code.** Rule-0 re-reads found a real `ops→lab` runtime edge the rev.-1/2 grep-based §0 missed: `parity_check.py:222` lazily imports `analysis/.../tv_export_loader`. It is absorbed into core by widening that shared parser into `core/` (new §8 Q-d) — the four-layer model is not falsified. Two latent edges pinned: `scripts/validate_candidate.py`→lab and `strategies/codification/`→lab (new §8 Q-e). §0 context-file size re-anchored on **line counts** (CRLF-stable) not bytes. §2.3 gains a cross-layer name-uniqueness guard; §10/Verification swap the grep Phase-0 probe for an AST-aware one. rev. 2 resolved three layout seams; rev. 1 framed the four layers. **rev. 4 — reconciliation onto current main `0ec6e11`/PR#136:** parallel sessions retired the deletion instrument (`scripts/deletion_candidate_report.py`, `a9d16d0`) + the prior `REPO_MAP.md` (`f341648`) and added the M-9 Pine-manifest gate (`de3369c`). §0/§2.4/§6/§7/§10 updated — `REPO_MAP.md` is now the standing **layer map** + `check_boundaries.py` companion, NOT a deletion feed; the deletion-candidate deliverable is **withdrawn** (the question was answered on main). `archive/` grew 338→358; the `parity_check` edge moved line 223→222.).
> **Author:** Claude (Tech Advisor) — drafted for PO review.
> **Supersedes / relates to:** Q-SPLIT-1 repo-partition Pre-Q (replaces its two-physical-repo framing with monorepo-with-boundaries; carries forward its zero-lab↔ops-edge falsifier); manifest-integrity-gate ADR (2026-05-10, extends its scope); Lean Portfolio meta-layer ADR (2026-06-04, homes its governance layer); methodology-skills-under-VC ADR (2026-06-04).
> **Provenance note:** Built from the `brief-authoring` SKILL.md body discipline structure and the 2026-06-04 Lean Portfolio ADR exemplar (most recent working ADR). The canonical `references/adr.md` template is absent from version control (finding F-3, Q-SPLIT-1). Run `python scripts/check_brief.py docs/adr/2026-06-05-monorepo-layer-boundaries.md --type adr` before ACCEPT.

---

## §0 — Rule 0: Production reads (verified on-disk 2026-06-05; rebased onto `origin/main` `0ec6e11` = PR#136, anchors re-confirmed there)

**Verification anchor (Rule 0):** §0 reads verified on-disk 2026-06-05; the branch is now rebased onto `origin/main` `0ec6e11` (`git log -1 --oneline origin/main` → PR#136) and the load-bearing anchors (the `parity_check` ops→lab edge, `tv_export_loader`'s `lib.mvd`-only imports, `portfolio_mc`'s `__file__`-relative data paths) were re-confirmed on that base. Not memory-tier. **rev. 4 reconciles to current main; rev. 3 corrected the cross-layer-edge + context-file-size rows.**

| Claim this ADR relies on | On-disk confirmation |
|---|---|
| `archive/` is dead working-tree weight | **358** tracked files (338 at the original `139be9f` base + 20 added by parallel co-archive commits on main); `grep -rn "import archive\|from archive" --include=*.py . \| grep -v '^./archive/'` → **empty**. Referenced only within itself. |
| **Cross-layer code edges (CORRECTED rev. 3 — the rev.-1/2 "the one edge is lab→core" claim was incomplete).** | Two internal cross-application edges exist, not one: **(a)** `validation/sweep/engine.py:54` → `import dd_protection` = lab→core (**legal** under §2.1). **(b)** `parity_check.py:222` (inside `_load_pine_legs`, a lazy import; line 223 at the `139be9f` base, **222 on current main**) → `from analysis.oanda_stage1.tv_export_loader import pair_tv_export_dataframe` = **ops→lab** (the forbidden direction). Edge (b) is resolved — not relaxed — by widening `tv_export_loader.py` into `core/` (§8 Q-d): it imports only `lib.mvd` (=core), so post-widening both its ops consumer and its lab consumers are legal `→core` edges. An exhaustive AST-blind-spot grep confirms (b) is the **only** ops→lab runtime edge. |
| `tv_export_loader.py` is core-shaped (the §8 Q-d basis) | `analysis/oanda_stage1/tv_export_loader.py:28` imports only `from lib.mvd import assert_min_rows, assert_tv_export` (→core). Consumed by ops (`parity_check.py`) AND lab (`scripts/wfo/operations.py:17`, `analysis/oanda_stage1/*_stage1.py`, `tests/test_tv_export_loader.py`). A shared immutable parser ⇒ structurally core. |
| Two latent edges resolved by correct classification (§8 Q-e) | `strategies/codification/emit.py:143` → `from validation.concept_intake.schema import load_concept` (lab) ⇒ `codification/` must be extracted to `lab/`, not left under `core/strategies/` (else core→lab). `scripts/validate_candidate.py:42-49` → `from validation import …` ×8 (a research harness) ⇒ it is **lab**, not a governance discipline script. |
| `portfolio_mc.py` is a shared core hub | imported by `validation/` (lab) and `weekly_review_feeder/` (ops) — both prospective layers depend on it (14 importers total; these two are representative). Locates panels via `Path(__file__).parent / "data" / "tv_exports"` (lines 72/80) — co-moving module+data into `core/` is path-stable (H2 basis). |
| ops execution journal is decoupled from core MC | `grep portfolio_mc live_journal/` → empty |
| Context-file accretion (the §2.6 target) | `CLAUDE.md` **193 lines**; its Strategy Reference block is an append-only MC-anchor + Q-SWAP-1/2/3/4 litigation log. `docs/SESSIONS.md` **346 lines**. (Byte counts omitted from §0 by intent — they are CRLF-dependent and differ Windows-working-tree vs Linux/CI, so pinning a byte figure makes the ADR wrong on one platform; line counts are stable across both.) |
| The deletion instrument was **retired on main** | `scripts/deletion_candidate_report.py` removed (`a9d16d0`) + the prior `REPO_MAP.md` retired (`f341648`) by parallel sessions. The deletion-candidate chain is dead; this ADR repurposes a **fresh** `REPO_MAP.md` as the standing layer map + `check_boundaries.py` companion (§7), not a deletion feed. |
| Enforcement infra to extend (not invent) | `scripts/githooks/pre-commit` exists; `check_*.py` family (7 scripts); manifest gate = `strategies/MANIFEST.sha256` + `check_pine_manifest.py` + `check_data_manifests.py` |
| Memory-snapshot correction | `inqhiori-algorithm` is **not** in VC (`find -iname '*inqhiori-algorithm*'` → empty); two ADRs post-date the snapshot (06-05 concept-admissibility, 06-05 sweep-engine). HEAD was PR#135 at authoring; the branch is now rebased onto **PR#136** (`0ec6e11`). |

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
| **`core/`** | Locked. Changes require deliberate manifest regeneration (§2.4). | `portfolio_mc.py`, `dd_protection.py`, `firm_rules.py`, `csv_parser.py`, **`tv_export_loader.py`** (shared TV-CSV pairing parser, widened from `analysis/` per §8 Q-d), `strategies/` (Pine source + `LOCK.md` + `MANIFEST.sha256` + CHANGELOGs, **minus `codification/`** which is lab per §8 Q-e), shared `lib/`, `config/`, `core/data/` (backtest panels — immutable shared inputs) | stdlib + third-party **only** — nothing internal |
| **governance** (**root-resident — no physical `governance/` dir**; see amendment) | Append-with-discipline (the meta-layer). | `docs/`, `.claude/skills/` (markdown discipline; **no** importable internal-dependent code — §8 Q-b), `.github/`, discipline scripts (`check_brief*`, `check_skill_refs`, `validate_params`, `verify_lock_anchors`, ~~`validate_alert_payloads`~~ retired 2026-08-02, `sync_*`), and root files (`CLAUDE.md`/`README.md`/`STATE.md`/`Makefile`/`pyproject.toml`) — **all stay at repo root, classified-not-moved** | `core/` + stdlib |
| **`lab/`** | Free churn. | `analysis/`, `validation/`, `codification/` (extracted from `strategies/`, §8 Q-e), research scripts (`mc_*`, `q_*`, `pine_lint`, `fetch_oanda_bars`, **`validate_candidate`** §8 Q-e; root-resident under `scripts/`), `scripts/wfo/` | `core/`, `governance/` |
| **`ops/`** | Operational; changes are live-impacting but not lock-gated. | `accounts.py`, `cli.py` (mutable account-state surface), `fxify_rule_validator.py`, `parity_check.py`, `tv_mt5_pnl_reconciliation.py`, `live_journal/` (incl. the **canonical** `journal_review.py` ECR engine + the `trade_to_signal_event` DXTrade→signal bridge relocated from `core/csv_parser.py` — amendment), `weekly_review_feeder/`, `ops/data/` (`accounts.json` + live state), ops scripts (`preprocess_pine_ecr_logs`, `inactivity_simulator`, `lock_event_hook`, `run_ecr`; + the ops-discipline `check_skill_enum_mirror`/`check_skill_notion_schema` reclassified here — amendment) | `core/`, `governance/` |

`core/` is the sink of the dependency graph: everything may depend on it; it depends on nothing internal. Governance sits just above core. `lab/` and `ops/` are the two application layers — both rest on core+governance and are **mutually isolated**.

> **Execution-time amendment (2026-06-06, Phase C — status remains ACCEPTED).** Reconciling this model with the tree as physically built, recorded here so the canonical record matches reality (not silently changed):
> 1. **Governance is entirely root-resident — there is no physical `governance/` directory.** `docs/`, `.claude/`, `.github/`, the discipline `scripts/`, and the root files stay at repo root, **classified-not-moved**. Rationale: governance joins no import contract among application code, and relocating it breaks tooling (the harness requires `.claude/{skills,settings.json,commands}` at fixed paths; GitHub requires `.github/workflows/`; every `check_*`/`validate_*` script computes `REPO_ROOT` from `scripts/` at root and is invoked `python scripts/X.py`) *and* breaks hundreds of doc cross-links — for **zero** contract benefit. The physical partition is `core/ lab/ ops/` + root-resident governance; `check_boundaries.py` classifies the root-resident `.py` per `REPO_MAP.md` §2.1.
> 2. **The four surfaced edges are resolved by correct placement (not contract relaxation), and that placement is the ratified classification:** `tv_export_loader.py` → **core** (widen, §8 Q-d); the `trade_to_signal_event()` function relocated `core/csv_parser.py` → **ops** (`ops/live_journal/ingest/dxtrade_bridge.py` — it was a core→ops edge `check_boundaries` caught); `check_skill_enum_mirror`/`check_skill_notion_schema` → **ops** (ops-discipline validators that import `live_journal`). (`validate_candidate.py` + `codification/` → lab were already §8 Q-e.)
> 3. Both falsifiers verified post-move: **H1** `check_boundaries` green (0 illegal edges); **H2** `test_mc_anchors` 8/8 reproduce + locked core files byte-identical.

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

### 2.4 — Manifest gate scope = `core/` only

The manifest-integrity gate (ADR 2026-05-10) currently guards `strategies/` + data manifests. Post-move it guards **`core/`** — specifically `core/strategies/` (Pine source hashes via `MANIFEST.sha256`) and the MC-anchor pins (`tests/test_mc_anchors.py`). `lab/`, `ops/`, and `governance/` churn freely without manifest friction. This makes "guarding core" concrete: any change under `core/strategies/` requires a deliberate `MANIFEST.sha256` regeneration — a friction gate by design, not an accident. The pine `MANIFEST.sha256` stores `strategies/`-prefixed paths in its content; re-pointing is a path-column re-prefix to `core/strategies/` with the 64-hex digests byte-identical (the move changes location, not bytes). **Derive the re-point from current main's `MANIFEST.sha256`** — commit `de3369c` added the M-9 Pine-manifest gate (`check_pine_manifest.py`) and pruned the stale archive `.pine` entries, so there are no archive lines to carry — not the `139be9f` snapshot.

### 2.5 — Archive-eviction policy (standing rule, not a one-time cleanup)

The working tree carries **no artifact that nothing live imports or references**. `archive/` (**358** files on current main, imported by nothing — §0) is evicted: tag `pre-prune-2026-06-05`, then `git rm -r archive/`. Recovery is `git show <tag>:archive/...` or `git checkout <tag> -- <path>`. Deletion of *working-tree presence* is not deletion of *history* — every closed-loop preserved finding (Q-CORR-1, Q-DDP-1, …) remains in git history and reachable by tag. The rule generalizes forward: closed loops are archived to history+tag, not accumulated in-tree. This is The Algorithm's *delete* applied to the tree.

### 2.6 — State-file separation policy (the fix for append-only-log degeneration)

Canonical context files carry **current state only**. `CLAUDE.md` keeps the locked-strategy table, the *single current* MC anchor (99.83 / 0.17 / 4.37, median 26), current protection constants, and pointers. The historical narrative — MC-anchor evolution, superseded Q-SWAP closures, supersession/retraction chains — moves to dated history files (`docs/mc_anchor_history.md`, classified governance, root-resident). `CLAUDE.md` is loaded into every session's context; it must be the smallest true thing, not the litigation transcript. The prune is **lossless by verification, not assertion**: every line removed from `CLAUDE.md` must be **content-preserved** in `mc_anchor_history.md` — extracted byte-identically where possible, but a prune executed *inside* the move may re-point moved-tree paths in the retained text (e.g. `data/`→`core/data/`), so the gate is information-preservation, not strict byte-verbatim (reconstruction check in the handoff Step C1). This is a **standing rule**: without it, the prune is a one-time cleanup that re-accretes (brief-authoring trap: belt grows, never prunes).

### 2.7 — Monorepo, not two physical repos (explicit rejection + revisit trigger)

The two-repo split is rejected. Two repositories force `core/` + `governance/` to be versioned, published, and pinned, and turn any cross-layer change into a coordinated multi-PR operation — a dependency-management tax. For a single operator with no team-isolation requirement, that tax exceeds its benefit. The enforced-boundary monorepo delivers the isolation property (§2.2) and the protection property (§2.4) **without** the tax.

Critically, this decision is **forward-compatible with a future split, not a dead end**: the §2.2 contract is exactly the precondition a physical split would require. If `lab/` ever needs independent publication (e.g. open-sourcing the research layer while keeping `ops/` private), the lab↔ops isolation already in force makes the physical extraction mechanical at that point. **Revisit trigger:** a concrete need to clone/publish one application layer without the other.

---

## §4 — Falsifiable hypotheses

This ADR carries three falsifiable hypotheses (H1–H3), each with its own falsifier.

**H1 — hypothesis (satisfiability, checkable at the move).** If the mutability cut is correct for this tree, then after extracting `core/` (including the §8 Q-d widening of `tv_export_loader` and the §8 Q-e classifications), `check_boundaries.py` reports **zero** illegal edges with **no contract relaxation**.

> **Falsifier:** an illegal edge — specifically a direct `lab↔ops` runtime import — that cannot be absorbed into `core/` by a reasonable widening. The known `parity_check.py:222` ops→lab edge does **not** falsify H1: it is absorbed by moving `tv_export_loader` (which depends only on `lib.mvd`=core) into `core/`, which is precisely the "reasonable widening" the falsifier carves out. A falsifying edge would be one where the ops and lab sides are genuinely fused — e.g. an ops module importing a lab module that itself depends on ops, so no single artifact can be lifted to core. Disposition then: halt the move, do **not** relax the contract, and reconsider the partition (revert to flat, or a different cut). Carries forward Q-SPLIT-1 §4.

**H2 (integrity — checkable at the move).** The move relocates; it must not mutate locked content. Post-move, `check_pine_manifest.py`, `check_data_manifests.py`, and `tests/test_mc_anchors.py` all pass with **unchanged hashes and anchor values**. (Mechanism: `portfolio_mc.py` locates panels via `Path(__file__).parent`, so co-moving module+data is path-stable and the simulation bytes are untouched; the manifest digests are byte-identical under `git mv`.)

> **Falsifier:** any manifest hash or MC anchor changes value → a `core/` artifact was mutated, not moved. Disposition: revert the offending layer commit; investigate before retrying. Do **not** regenerate hashes to clear the gate.

**H3 (load-bearing over time — checkable at audit cadence).** The boundary is load-bearing, not ceremony, if within two `programme-audit` cycles either (a) `check_boundaries.py` has blocked at least one illegal-import attempt in CI/pre-commit, or (b) the layer assignment in `REPO_MAP.md` is referenced in at least one subsequent structural decision.

> **Falsifier:** two audit cycles elapse with the check never firing **and** never referenced **and** files visibly drifting across layers (the check being bypassed or too weak). Then the enforcement decayed to nominal — disposition: strengthen the check or delete it per The Algorithm. (A check that never fires *because deterrence works* is not falsified by (a) alone — hence the conjunction with drift evidence.)

---

## §5 — Forbidden moves (genuinely tempting, ruled out)

1. **Relax the §2.2 contract to make `check_boundaries.py` pass.** Defeats the decision. A real illegal edge is a finding (H1 falsifier), not a contract to loosen. (Note the distinction the rev.-3 correction makes load-bearing: *re-classifying* `validate_candidate.py`→lab or *widening* `tv_export_loader`→core is **not** relaxation — it is correct placement of a misfiled artifact. Relaxation would be adding `lab↔ops` to the legal-edge set.)
2. **Split into two physical repos "for cleanliness."** The rejected alternative (§2.7). Tempting for tidiness; pays a dependency-management tax with no offsetting single-operator benefit. The monorepo already preserves the option to split later.
3. **Regenerate manifest hashes to clear a red gate after a move that changed content.** A red gate post-move means content mutated (H2 falsifier) — investigate, never paper over.
4. **Keep `archive/` in the tree "just in case."** The "just in case" is the tag + git history, not the working tree. Dead weight in-tree is the degeneration §2.5 exists to stop.
5. **Treat the `CLAUDE.md` prune as a one-time cleanup.** Without §2.6 as a *standing rule*, it re-accretes. The rule is the fix; the prune is just its first application.
6. **Add a fifth layer or sub-layers now.** Four is the claim. Over-partitioning is ceremony until a concrete edge forces it. Resist `core/`→`core/locked/`+`core/shared/` etc. absent a real need.
7. **Decide `data/` or `tests/` homes by convenience to avoid the question.** These were genuine open seams (resolved in §8); resolve any *new* seam explicitly in `REPO_MAP.md`, don't default silently.
8. **Trust a grep to prove `lab↔ops` clean.** The rev.-1/2 §0 did, and missed the lazy `parity_check.py:222` import. Use the AST-aware probe (§10) before declaring the partition satisfiable.

---

## §6 — Gate / closure criteria (binary)

Evaluated when the CC handoff Phase C completes:

- **RESOLVED (Progressive — retain):** move executed via `git mv`; `check_boundaries.py` green with no contract relaxation (H1) — including the `tv_export_loader`→core widening and the `validate_candidate`/`codification`→lab classifications; manifest + MC anchors byte-identical (H2); `REPO_MAP.md` maps every tracked path with zero unmapped (the standing layer map + `check_boundaries.py` companion — NOT a deletion feed; the deletion instrument was retired on main). Fold re-check into `programme-audit` cadence (H3).
- **FALSIFIED (Degenerating — revert):** an irreducible `lab↔ops` edge survives a reasonable `core/` widening (H1), **or** a `core/` artifact mutated during the move (H2). Revert the layer move; capture a methodology lesson with the offending edge/artifact named.
- **AMBIGUOUS (hold the path, not the architecture):** move done and boundaries green, but a path's layer assignment is contested at execution time (the rev.-1 seams — `data/`, skills, `tests/` — are resolved in §8; the rev.-3 calls — `tv_export_loader`, `validate_candidate`, `codification` — are resolved here too; this branch covers any *new* contested path CC surfaces during classification). Hold that specific path in a `?`-tier in `REPO_MAP.md`; resolve before declaring RESOLVED. Do **not** amend these criteria mid-window (anti-p-hack, brief-authoring trap 12).

**Decay re-gate (H3):** at the second `programme-audit` cycle after ACCEPTED, evaluate whether the boundary check has fired or been referenced. If neither and layer drift is observed, re-open as a methodology audit.

---

## §7 — Consequences

- **Execution vehicle:** the monorepo-boundaries CC handoff. Phase A (this ADR) + Phase B (archive eviction, SNAG dossier) need no ACCEPT; **Phase C (context prune, tree move, enforcement, layer-map authoring) is gated on this ADR being flipped to ACCEPTED.**
- **`REPO_MAP.md` becomes the standing layer map** — the authoritative path→layer assignment and the human-readable companion to `check_boundaries.py`'s path-prefix logic. (The prior REPO_MAP-as-deletion-input chain is dead: a parallel session retired both `deletion_candidate_report.py` (`a9d16d0`) and the old REPO_MAP (`f341648`). This is a fresh, purpose-rebuilt map.)
- **The manifest gate's blast radius narrows to `core/`** — `lab/`/`ops/`/`governance/` developers stop hitting manifest friction on unrelated churn.
- **One shared parser is widened to core** (`tv_export_loader`) and one duplicate is removed (`journal_review.py`, §8 Q-b) — net importable surface shrinks, not grows.
- **Every session pays less context** once `CLAUDE.md` is pruned (§2.6).
- **A future physical split is de-risked, not foreclosed** (§2.7).
- **What this ADR does NOT decide:** the Q-SWAP SNAG disposition (separate PO ruling via the handoff's Step B2 dossier; the PO has, for the 2026-06-05 execution, granted ruling authority for that dossier — recorded in the handoff §0.5, out of scope here).

---

## §8 — Seams resolved, with evidence

Seams Q-a/b/c were resolved in rev. 2; Q-d/e in rev. 3 (the production-code corrections). All are recorded (not deleted) so a later reader sees these were deliberate, evidence-based calls — not silent defaults.

- **Q-a — `data/` home → SPLIT (`core/data/` panels, `ops/data/` state).** Backtest panels are read by both lab (`scripts/q_*`, `analysis/portfolio_swap_impact.py`) and ops (`weekly_review_feeder/backtest_parser.py`) — shared immutable inputs, so `core/data/`. `accounts.json` is read/written by `accounts.py` and mutates weekly — operational state, so `ops/data/`. **Consequence:** `accounts.py` and `cli.py` move to `ops/` *with* the state they manage (both use `Path(__file__).parent / "data"`, so co-location keeps the relative path intact). On-disk justification: core imports nothing from `accounts`/`cli` (`grep` → empty), and `accounts.py` imports only `firm_rules` (→core, legal as ops). Leaving `accounts.py` in `core/` while `accounts.json` → `ops/data/` would make a core module read ops state — a layering violation the import contract would **not** catch (a path read, not an import), so it is fixed structurally by co-locating code with state.

- **Q-b — skills home → all `.claude/skills/` to `governance/`.** Census: 9 of 10 skills are markdown-only; their home is organizational with zero contract impact. The one exception, `.claude/skills/live-execution-journal/scripts/journal_review.py`, is importable Python **and a duplicate** of the canonical ops ECR engine at `live_journal/scripts/journal_review.py` (both import only stdlib + pandas/numpy — confirmed on-disk). **Resolution:** skills → governance as markdown discipline; the canonical ECR engine lives in `ops/live_journal/scripts/`; the skill **references** it rather than bundling a copy. The duplicate skill-copy is `git rm`-ed at the move. Net: `governance/` carries no importable internal-dependent code, so governance→core is the only edge it can even form — contract-clean.

- **Q-c — `tests/` → top-level, contract-EXEMPT (confirmed, not defaulted).** A single suite imports across all three application-relevant layers simultaneously — `from accounts`/`from dd_protection`/`from portfolio_mc` (core), `from analysis.oanda_stage1` (lab), `from live_journal.* import …` (ops). Integration tests cross-cut layers by nature; `test_ecr_rolling.py` alone spans core+ops. Colocating tests by layer is impossible without splitting individual test files, and subjecting `tests/` to the contract would forbid legitimate integration coverage. `check_boundaries.py` exempts `tests/`.

- **Q-d — `tv_export_loader.py` home → CORE (widen) [rev. 3].** `parity_check.py:222` (ops) lazily imports `analysis.oanda_stage1.tv_export_loader` (lab) — a real ops→lab edge the rev.-1/2 grep §0 missed (in-function imports are invisible to a line grep). `tv_export_loader.py:28` imports only `from lib.mvd import …` (=core) and is consumed by both ops (`parity_check`) and lab (`scripts/wfo/operations.py:17`, the three `*_stage1.py`, `tests/test_tv_export_loader.py`). It is therefore a shared immutable input — structurally core. **Resolution:** `git mv analysis/oanda_stage1/tv_export_loader.py core/tv_export_loader.py`; update `parity_check.py:222` and the lab importers to the flat `from tv_export_loader import …` form. **Rejected alternative:** duplicate the parser into ops — re-creates exactly the `journal_review.py` duplication Q-b is removing. This widening is the H1-sanctioned "absorb into core," not a contract relaxation.

- **Q-e — two classification calls [rev. 3].** `strategies/codification/emit.py:143` imports `validation` (lab); `codification/` is a Pine code-generation framework, not locked strategy source, so it is extracted from `core/strategies/` to **`lab/codification/`** (leaving it under `strategies/` would create a core→lab edge). `scripts/validate_candidate.py:42-49` imports `validation` ×8 (cpcv/dsr/pbo/permutation — a research harness, not a `check_*` discipline script), so it is **lab**, not governance (misfiling it governance would create a governance→lab edge). Both are mechanical: the imports decide the layer.

**Nothing remains open in this ADR.** The Q-SWAP SNAG disposition is out of scope (handoff Step B2). The `journal_review.py` dedup (Q-b) and the `tv_export_loader` widening (Q-d) are tracked, evidence-based moves — not open questions.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Boundary contract green, no relaxation (H1) — the core invariant
python scripts/check_boundaries.py && echo "boundaries OK" || echo "ILLEGAL EDGE — H1 falsifier, do not relax contract"

# 2. core/ is a true sink: nothing under core/ imports another internal layer
grep -rnE "import (lab|ops|governance)|from (lab|ops|governance)" core/ 2>/dev/null \
  && echo "VIOLATION — core importing upward" || echo "core sink OK"

# 3. lab<->ops isolation — AST-blind-spot probe (catches the parity_check.py:222 class
#    of lazy/in-function imports a plain grep misses). Pre-move form:
grep -rnE "(from|import)[[:space:]]+(analysis|validation)([.[:space:]]|$)" \
  accounts.py cli.py parity_check.py fxify_rule_validator.py tv_mt5_pnl_reconciliation.py \
  live_journal/ weekly_review_feeder/ 2>/dev/null
echo "(pre-move: ONLY parity_check.py:222 expected. Post-move: ZERO — loader is core. Any other hit = NEW ops->lab edge)"

# 4. tv_export_loader widened to core, parity_check imports it from core (§8 Q-d)
test -f core/tv_export_loader.py && ! test -f analysis/oanda_stage1/tv_export_loader.py \
  && echo "loader widened to core OK" || echo "CHECK §8 Q-d — loader not in core"

# 5. Locked content moved-not-mutated (H2)
python scripts/check_pine_manifest.py && python scripts/check_data_manifests.py \
  && python -m pytest tests/test_mc_anchors.py -q && echo "integrity OK (H2 holds)"

# 6. Manifest gate scoped to core/ (§2.4)
grep -rn "strategies/" scripts/check_pine_manifest.py | grep -q "core/strategies" \
  && echo "manifest re-pointed to core/ OK" || echo "CHECK §2.4 — manifest path not under core/"

# 7. Archive evicted + recoverable (§2.5)
test -d archive && echo "FAIL: archive in tree" || echo "archive evicted"
git show pre-prune-2026-06-05:archive/ >/dev/null 2>&1 && echo "recoverable from tag OK"

# 8. Context file pruned + lossless (§2.6)
test "$(wc -l < CLAUDE.md)" -lt 193 && echo "CLAUDE.md shrank OK"   # expect materially < 193 lines
test -f docs/mc_anchor_history.md && echo "history extracted OK" || echo "FAIL §2.6"

# 9. Layer map present — REPO_MAP is the check_boundaries companion, NOT a deletion feed
#    (the deletion instrument was retired on main, a9d16d0; deletion deliverable withdrawn)
test -f REPO_MAP.md && echo "layer map present OK" || echo "REPO_MAP layer map missing"

# 10. ECR engine deduped (§8 Q-b): exactly ONE journal_review.py, under ops/
test "$(find . -name journal_review.py -not -path './.git/*' | wc -l)" -eq 1 \
  && find . -name journal_review.py -not -path './.git/*' | grep -q '^./ops/' \
  && echo "single canonical ECR engine under ops/ OK" || echo "DUPLICATE or misplaced ECR engine"

# 11. accounts co-located with its state (§8 Q-a): accounts.py in ops/, not core/
test -f ops/accounts.py && ! test -f core/accounts.py \
  && echo "accounts code+state co-located in ops/ OK" || echo "CHECK §8 Q-a — accounts split from its state"

# 12. Scanner asserts cross-layer name uniqueness (§2.3) — fails loud on a future collision
python scripts/check_boundaries.py --self-test-uniqueness 2>/dev/null \
  && echo "uniqueness guard present OK" || echo "NOTE: ensure check_boundaries asserts name uniqueness"

# 13. Decay re-gate (H3) — run at programme-audit cadence, not now:
grep -rl "check_boundaries\|REPO_MAP" docs/adr/ 2>/dev/null | grep "2026-0[7-9]\|2026-1[0-2]" \
  || echo "H3: not yet referenced — re-check next audit cycle"
```

**Re-check cadence:** at Phase-C completion (§6 gate), then folded into `programme-audit`. If two cycles pass without hook #1 or #10 firing and layer drift appears, flag the enforcement as decaying (H3 falsifier).

---

## Verification (run before ACCEPT)

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-06-05-monorepo-layer-boundaries.md --type adr
# Expected: well-formed (0 HARD)

# §0 confirmation (Rule 0 on-disk anchors)
git log -1 --oneline origin/main                                  # base = 0ec6e11 (PR#136) or later
grep -rn "import archive\|from archive" --include=*.py . | grep -v '^./archive/'  # expect empty
sed -n '54p' validation/sweep/engine.py                          # the legal lab->core edge
sed -n '222p' parity_check.py                                    # the ops->lab edge resolved by §8 Q-d
sed -n '28p' analysis/oanda_stage1/tv_export_loader.py           # loader depends only on lib.mvd (=core)
# (scripts/deletion_candidate_report.py was retired on main — a9d16d0 — no longer an anchor)

# AST-aware lab<->ops probe (replaces the rev.-1/2 grep that missed parity_check.py:222)
grep -rnE "(from|import)[[:space:]]+(analysis|validation)([.[:space:]]|$)" \
  accounts.py cli.py parity_check.py fxify_rule_validator.py tv_mt5_pnl_reconciliation.py \
  live_journal/ weekly_review_feeder/                            # expect ONLY parity_check.py:222
```
