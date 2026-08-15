# CC Handoff — Monorepo boundary restructure (`core/ | lab/ | ops/ | governance/`)

> **Type:** Claude Code handoff brief (spawn prompt / execution spec of record). Addresses recommendations 1–5 from the 2026-06-05 repo-partition review under the ratified architecture: **monorepo with enforced internal boundaries, `archive/` evicted, manifest gate guarding `core/`.**
> **Status:** READY (Phase A/B executing this session; Phase C gated on the ADR being flipped to ACCEPTED). Layout seams settled in `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (rev. 3).
> **Author:** Claude (Tech Advisor) — for PO (Joshua) + executor.
> **rev. 3 corrections folded in (2026-06-05):** (1) §0 edge inventory corrected — a real `ops→lab` edge (`parity_check.py:222`) the grep §0 missed, resolved by widening `tv_export_loader`→core (ADR §8 Q-d); (2) §0 Phase-0 probe upgraded grep→AST-aware; (3) §0.5 — **PO has granted SNAG ruling authority** for this execution, so Step B2 rules (overriding the options-only default + forbidden-move #5); (4) import strategy pinned = sys.path/pythonpath (Option B), not package-ification; (5) Step C1 lossless reconstruction check, Step C2 per-commit resolvability + pyproject ordering, Step C3 scanner name-uniqueness guard; (6) context-file sizes re-anchored on line counts (CRLF-stable). **rev. 4 — reconciled onto current main `0ec6e11`/PR#136:** the deletion instrument + prior REPO_MAP were retired on main (`a9d16d0`/`f341648`), so Step C4 is **WITHDRAWN**; the Step C2 seed rules are re-derived against current main (archived closed-Q scripts removed); §0 anchors updated (parity 223→222, archive 338→358); the Phase C3 manifest re-point derives from current main's M-9 manifest (`de3369c`).
> **Supersedes:** Q-SPLIT-1's two-repo framing. Q-SPLIT-1's §4 falsifier (zero direct lab↔ops imports) is **carried forward** as this brief's boundary contract.
> **Relates to:** Lean Portfolio meta-layer ADR (2026-06-04); manifest-integrity-gate ADR (2026-05-10); methodology-skills-under-VC ADR (2026-06-04).
> **Provenance note:** Built from `brief-authoring` SKILL.md body (§0/§0.5/§1/§2/§4/§5/§6/§7/§10 + CC patterns 7–10). Canonical `references/cc_handoff.md` is absent from VC (finding F-3, Q-SPLIT-1). Run `python scripts/check_brief.py <thisfile> --type cc_handoff` before dispatch.

---

## §0 — Rule 0: Production reads (verified on-disk 2026-06-05; rebased onto `origin/main` `0ec6e11` = PR#136)

**Verification anchor (Rule 0):** §0 reads verified on-disk 2026-06-05; the branch is now rebased onto `origin/main` `0ec6e11` (PR#136) and the load-bearing anchors re-confirmed there. Not memory-tier. **rev. 4 reconciles to current main; rev. 3 corrected the cross-layer-edge + context-size rows.**

| Fact this handoff relies on | On-disk anchor |
|---|---|
| Deletion instrument retired on main | `scripts/deletion_candidate_report.py` removed (`a9d16d0`) + prior `REPO_MAP.md` retired (`f341648`) by parallel sessions. Step C4 is **WITHDRAWN**; `REPO_MAP.md` is repurposed as the layer map (the `check_boundaries.py` companion), not a deletion feed. |
| **Cross-layer code edges (CORRECTED rev. 3)** | **(a)** `validation/sweep/engine.py:54` → `import dd_protection` = lab→core (**legal**). **(b)** `parity_check.py:222` (lazy, in-function) → `from analysis.oanda_stage1.tv_export_loader import pair_tv_export_dataframe` = **ops→lab** (forbidden). Edge (b) is dissolved at the move by widening `tv_export_loader`→`core/` (ADR §8 Q-d): it imports only `lib.mvd`(=core). Exhaustive AST-blind-spot grep ⇒ (b) is the ONLY ops→lab runtime edge. |
| `tv_export_loader.py` is core-shaped | `analysis/oanda_stage1/tv_export_loader.py:28` imports only `from lib.mvd import …`; consumed by ops (`parity_check`) + lab (`scripts/wfo/operations.py:17`, `*_stage1.py`, `tests/test_tv_export_loader.py`). |
| Two latent edges (correct classification) | `strategies/codification/emit.py:143` imports `validation` ⇒ `codification/`→`lab/`. `scripts/validate_candidate.py:42-49` imports `validation` ×8 ⇒ →`lab/`. |
| Core hub coupling + path-stability | `portfolio_mc.py` imported by `validation/` (lab) and `weekly_review_feeder/` (ops); locates panels via `Path(__file__).parent / "data" / "tv_exports"` (lines 72/80) → co-moving module+data is path-stable (H2). |
| Ops journal decoupled from core MC | `grep portfolio_mc live_journal/` → empty |
| `archive/` is dead tree-weight | **358** tracked files on current main (338 + 20 parallel additions); `grep -rn "import archive\|from archive" --include=*.py . \| grep -v '^./archive/'` → **empty**. |
| Context-file bloat | `CLAUDE.md` **193 lines** (Strategy Reference block is an append-only MC-anchor + Q-SWAP litigation log); `docs/SESSIONS.md` **346 lines**. (Byte counts omitted — CRLF-dependent, differ Windows vs CI.) |
| SNAG cluster | `docs/briefs/` Q-SWAP-1 (FALSIFIED) + Q-SWAP-2/3/4 (all AMBIGUOUS-HOLD) — three consecutive non-verdicts, one domain. |
| Existing enforcement infra to extend | `scripts/githooks/pre-commit` exists; `scripts/check_*.py` family (7 scripts); manifest gate = `strategies/MANIFEST.sha256` + `check_pine_manifest.py` + `check_data_manifests.py`. |

**Executor Phase 0 (MANDATORY before any move):** re-run the **AST-aware** lab↔ops probe (not the old line grep — that is what missed `parity_check.py:222`) plus the archive-coupling grep against the working tree at dispatch HEAD:
```
grep -rnE "(from|import)[[:space:]]+(analysis|validation)([.[:space:]]|$)" \
  accounts.py cli.py parity_check.py fxify_rule_validator.py tv_mt5_pnl_reconciliation.py \
  live_journal/ weekly_review_feeder/      # expect ONLY parity_check.py:222
```
If a NEW hit appears (a second ops→lab edge), return `NEEDS_CONTEXT` before proceeding — the layer contract (§4) depends on the edge set being exactly what §0 records.

---

## §0.5 — Clarifying questions (resolved)

The rev.-1 seams (skills home, `data/` home, `tests/` status, layer names) are **decided in the ADR** (§2.1 + §8) and reflected in the Step C2 seed rules. The one prior open question — SNAG disposition authority — is **resolved for this execution:**

1. **SNAG disposition authority — GRANTED.** For the 2026-06-05 execution the PO has explicitly granted ruling authority on the Q-SWAP cluster. Step B2 therefore assembles the dossier **and issues a ruling** (apply `programme-audit` to the cluster, present the disposition options, then rule and record the authority grant). This overrides the standing options-only default and forbidden-move #5 for this run only; a future spawn without an explicit grant reverts to options-only.

If any path's layer is genuinely ambiguous at classification time (a *new* contested path, not one of the settled seams Q-a…Q-e), surface it and hold it in a `?`-tier in `REPO_MAP.md` — do not guess silently.

---

## §1 — Context & the five recommendations this handoff executes

The 2026-06-05 review found the R&D/ops split was a packaging answer to non-packaging pain. The repo's real friction is along a different axis (mutability, not research-vs-ops) plus three independent rot signals. The chosen architecture is a **monorepo with four enforced layers**, not two physical repos — ~90% of the separation benefit without cross-repo dependency-management overhead, poor value for a single operator.

The dependency DAG (the "enforced boundaries"):

```
            ┌─────────────┐
            │  governance │  (methodology, ADRs, briefs, skills, discipline checks)
            └──────┬──────┘
                   │ depended-on-by lab, ops
   ┌───────────────┴───────────────┐
   ▼                               ▼
┌──────┐                       ┌──────┐
│ lab  │  ── may import ──▶    │ ops  │   ✗ FORBIDDEN: lab↔ops direct
└──┬───┘     core, governance  └──┬───┘
   │              (NOT each other) │
   └──────────────┬────────────────┘
                  ▼
            ┌──────────┐
            │   core   │  stdlib + third-party ONLY. Imports nothing internal.
            └──────────┘   Locked, manifest-gated, must-not-change.
```

The lab↔ops isolation is the load-bearing invariant. It is **not** clean as-shipped — `parity_check.py:222` is a real ops→lab edge — but it is made clean at the move by widening the one shared parser (`tv_export_loader`) into core (ADR §8 Q-d). That is the H1-sanctioned "absorb into core," not a contract relaxation.

**Recommendation → phase map (the "systematically" requirement):**

| Rec | What | Phase | Reversibility |
|---|---|---|---|
| **#3 + #5** | Four-layer architecture + boundary enforcement + manifest scope | A (ADR) + C2/C3 | Low — ADR-gated |
| **#2** | Evict `archive/` from working tree (tag + `git rm`) | B1 | High (git revert + tag) |
| **#4** | Resolve Q-SWAP SNAG — dossier + ruling (authority granted) for PO record | B2 | High (authoring only) |
| **#1** | Prune `CLAUDE.md`/`SESSIONS.md`: current-state stays, history → `docs/mc_anchor_history.md` | A (policy) + C1 | Low — ADR-gated |

Sequencing principle: bank the cheap reversible wins (B) before the irreversible move (C); hard-stop between them for ratification.

Standing doctrine: Rule 0 (the rev.-3 edge correction is a Rule-0 win — production code falsified a doc claim); The Algorithm (delete → simplify → automate); forward-asymmetry (keep this dev-stream reorg from perturbing the still-broken ECR op-stream falsifier; scoped to NOT touch `live_journal/` internals beyond relocation); `programme-audit` (the SNAG and the context-bloat are both its named degeneration signals).

---

## §2 — Execution plan (phased; HARD GATE between B and C)

Each step ends in its own commit. Steps B1/B2 are independent and need no ADR. **Phase C must not begin until the PO flips the Phase-A ADR to ACCEPTED.** If running autonomously, **halt after Phase B and return `NEEDS_CONTEXT` (awaiting ADR ratification).**

### Phase A — Author the decision (no tree changes)

**Step A1.** Author `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (PROPOSED, rev. 3): (a) four-layer DAG; (b) boundary contract (§4); (c) archive-eviction policy (#2); (d) state-file separation (#1); (e) manifest-gate scope = `core/`; (f) the rev.-3 edge corrections (Q-d/Q-e). §0 anchored to this handoff's §0. `python scripts/check_brief.py … --type adr` → well-formed.

**Step A2.** Commit this handoff at `docs/spec/CC-HANDOFF-monorepo-boundaries.md`. `check_brief.py … --type cc_handoff` → well-formed.

### Phase B — Bankable reversible wins (execute now, commit each)

**Step B1 — Evict archive (#2).**
- `git tag pre-prune-2026-06-05` (recovery anchor) and confirm it resolves.
- Grep live pointers first: `grep -rn "archive/" --include=*.md docs/ STATE.md CLAUDE.md README.md`. Re-point any **live** link to the tag path `git show pre-prune-2026-06-05:archive/...`; leave historical ADR/brief bodies as record.
- `git rm -r archive/`; commit `chore: evict archive/ from working tree (preserved at tag pre-prune-2026-06-05)`.
- Sanity: `pytest tests/ -q` green; `check_pine_manifest.py` passes (MANIFEST has no archive entries — verified, 8 lines all under `strategies/`).

**Step B2 — SNAG disposition dossier + ruling (#4).**
- Assemble `docs/methodology_audit/Q-SWAP-cluster-disposition.md`: the four Q-SWAP closures, verdicts, shared domain (overnight-swap cost vs lock criteria), budget spent, the surviving belt finding.
- Apply `programme-audit` to the *cluster*. Present 2–3 disposition **options** — (i) promote one verdict on existing evidence; (ii) retire the domain on SNAG-budget exhaustion (Q-CORR-1 precedent); (iii) one more decisive loop with a pre-registered binary gate — **then rule** (authority granted §0.5; record the grant in the dossier).

### ── HARD GATE: PO ratifies ADR (PROPOSED → ACCEPTED) before Phase C ──

### Phase C — Gated structural move (only after ACCEPTED)

**Import strategy = sys.path / editable-install (Option B), NOT package-ification.** The tree is already half sys.path-driven (flat `py-modules` in `pyproject.toml`, `lib` as a flat package, real packages elsewhere, an established `sys.path.insert(REPO_ROOT)` shim idiom, a try/except dual-import in `portfolio_mc.py`). Option B keeps locked core modules **byte-identical** (the H2-decisive property). Package-ifying would rewrite ~200 import lines incl. locked `portfolio_mc.py`/`dd_protection.py` — colliding with relocate-only and forbidden-move #6.

**Step C1 — Prune context files (#1).**
- Create `docs/mc_anchor_history.md`; move the MC-anchor evolution + Q-SWAP-1/2/3/4 narrative + supersession/retraction prose out of `CLAUDE.md`'s Strategy Reference block into it.
- Leave in `CLAUDE.md`: the locked-strategy table, the *single current* MC anchor (99.83/0.17/4.37, median 26), protection constants, a one-line pointer. Target: Strategy Reference block < ~40 lines.
- **Losslessness check (required, not asserted):** every line removed from `CLAUDE.md` must reappear verbatim in `mc_anchor_history.md`. Verify by reconstruction — `git show HEAD:CLAUDE.md` must equal (new `CLAUDE.md` minus the one new pointer line) ∪ (`mc_anchor_history.md` body); `diff` the sorted line-sets so the only delta is the added pointer line. Any dropped/edited content line → do not commit the prune.
- `SESSIONS.md` left as-is (already a history file by design; PO confirm if otherwise).

**Step C2 — Author `REPO_MAP.md` + execute the move.**
- Author `REPO_MAP.md`: classify **every** `git ls-files` path (post-B1, against **current main**) into exactly one of `{core | lab | ops | governance}` (+ tier P0–P3 — the rubric the now-retired `deletion_candidate_report.py` used; embed it directly in `REPO_MAP.md`). Zero unmapped. Seed rules (per ADR §2.1 + §8 — settled, do not deviate without surfacing):
  - **core/**: `portfolio_mc.py`, `dd_protection.py`, `firm_rules.py`, `csv_parser.py`, **`tv_export_loader.py`** (widened from `analysis/`, §8 Q-d), `strategies/` (locked source + LOCK.md + MANIFEST.sha256 + CHANGELOGs, **minus `codification/`**), shared `lib/`, `config/`, `core/data/` (backtest panels — immutable shared inputs)
  - **lab/**: `analysis/` (`eurusd_pattern_enum`, `oanda_stage1`, `*swap_impact`, `time_to_pass`, `q_swap_4_v56_oanda_corroborative`), `validation/`, **`strategies/codification/`** (§8 Q-e), research `scripts/` (`q_mcto_1_*`, `mc_user_guardian`, `pine_lint`, `fetch_oanda_bars`, `build_us_releases`, **`validate_candidate`** §8 Q-e), `scripts/wfo/`. **Re-derived against current main post-eviction:** the closed-Q one-shots the `139be9f` list named (`q_preconditions_*`, `dj30_nas100_*`, `losing_quarter_analysis`, `quarterly_analysis`, `replay_state_h5`, `portfolio_mc_inactivity`/`three_scenarios`, `q_dj30_decomp`, and `analysis/{q_corr_2,q_gdn_ddcap,silver_v15_*}`) were archived by parallel sessions (`5a8a7c9`/`3f25d32`/`7dd3f5f`/`1ffe66f`) → now evicted, no longer classified.
  - **ops/**: `accounts.py`, `cli.py` (move WITH their mutable state — §8 Q-a), `fxify_rule_validator.py`, `parity_check.py`, `tv_mt5_pnl_reconciliation.py`, `live_journal/` (incl. canonical `journal_review.py`), `weekly_review_feeder/`, `ops/data/` (`accounts.json` + live state), ops `scripts/` (`preprocess_pine_ecr_logs`, `inactivity_simulator`, `lock_event_hook`, `run_ecr`)
  - **governance/**: `docs/`, `.claude/skills/` (markdown discipline — §8 Q-b), `.github/`, discipline `scripts/` (`check_brief*`, `check_brief_evidence_coverage`, `check_skill_*`, `check_data_manifests`, `check_pine_manifest`, `validate_params`, `verify_lock_anchors`, `validate_alert_payloads`, `sync_*`); `CLAUDE.md README.md STATE.md Makefile pyproject.toml` stay physically at repo root (editable-install + hook/CI necessity), classified governance. (`deletion_candidate_report` is **gone** — retired on main; `check_brief_evidence_coverage` **retired/deleted 2026-06-08** — ADR `2026-05-16-fixture-test-requirement` Amendment.)
- **`tv_export_loader` widening (§8 Q-d):** `git mv analysis/oanda_stage1/tv_export_loader.py core/tv_export_loader.py`; update `parity_check.py:222` and the lab importers (`scripts/wfo/operations.py:17`, the three `*_stage1.py`, `tests/test_tv_export_loader.py`) to `from tv_export_loader import …`. This dissolves the only ops→lab edge.
- **`data/` split (§8 Q-a):** `accounts.py` + `cli.py` follow `accounts.json` into `ops/` (relative `Path(__file__).parent` path tracks — zero path edit). Core imports nothing from accounts/cli; `accounts.py` imports only `firm_rules` (→core, legal as ops).
- **ECR dedup (§8 Q-b):** keep `ops/live_journal/scripts/journal_review.py`; `git rm` the `.claude/skills/live-execution-journal/scripts/` copy; skill references the canonical path. End state: exactly one `journal_review.py`, under `ops/`. (A specific ADR-sanctioned dedup, not a general deletion sweep — there is no deletion sweep; the instrument was retired on main.)
- Move with **`git mv`** only (history-preserving — never delete+recreate). Update every intra-repo import path and doc link broken by the move. `tests/` stays top-level and contract-exempt (§8 Q-c).
- **`pyproject.toml`:** `pythonpath = ["."]` → `["core","lab","ops","governance","."]`, landed **in (or before) the core move commit** (non-existent later-layer entries are harmless; `"."` keeps not-yet-moved modules resolvable); update `py-modules`/`packages` homes. Stays at repo root.
- **Per-commit resolvability (load-bearing, not just end-state):** sequence **core → governance → lab → ops**. After EACH layer commit verify individually: `python -c "import portfolio_mc, dd_protection, firm_rules, accounts, cli"` resolves AND `pytest tests/ -q` is green. A red at any layer commit halts the sequence there. Commit as one reviewable move per layer where feasible (4 commits).

**Step C3 — Stand up boundary enforcement (#3/#5).**
- Write `scripts/check_boundaries.py`: static **AST** import scan asserting the §4 DAG (must catch aliased / relative / `from X import Y` / lazy in-function forms). Exit non-zero on any illegal edge; `file:line` message. `tests/` exempt. **Plus a cross-layer name-uniqueness guard:** since Option B flattens all four roots onto `sys.path`, a top-level module/package name appearing in >1 layer would make both the scanner and Python resolve silently to the wrong file — assert uniqueness and hard-error (`ambiguous module '<name>' across layers {a,b}`). Verified zero collisions today; the assert keeps a future one loud.
- Wire into the existing `scripts/githooks/pre-commit` and the `.github/` CI, alongside the `check_*.py` family.
- Re-point the manifest gate (`MANIFEST.sha256` path column `strategies/`→`core/strategies/` with digests byte-identical; `check_pine_manifest.py` `PINE_ROOTS`/`DEFAULT_MANIFEST`; `check_data_manifests.py` `MANIFEST_DIRS`→`core/data/…`; the pre-commit staged-path filter; `.github/workflows/manifest-check.yml` + `tests.yml`). Confirm `check_pine_manifest.py` passes (content not paths changed).

**Step C4 — WITHDRAWN (deletion instrument retired on main).**
- Deletions are **out of scope**. A parallel session retired `scripts/deletion_candidate_report.py` (`a9d16d0`) and the prior `REPO_MAP.md` (`f341648`); the `docs/inventory/deletion_candidates.md` deliverable is **withdrawn** — the deletion question was answered on main. The fresh `REPO_MAP.md` authored in C2 is the standing **layer map** (the `check_boundaries.py` companion), not a deletion feed. Any further pruning is a separate decision. (Phase C's deliverable narrows accordingly: the four-layer `git mv` + `check_boundaries.py` + CI + the layer-map `REPO_MAP.md` — no `deletion_candidates.md`.)

---

## §4 — Falsifiable hypothesis / acceptance contract

**H (boundary):** after the move — including the `tv_export_loader`→core widening and the `validate_candidate`/`codification`→lab classifications — a static AST import scan finds **zero** illegal edges, where illegal = {`core/`→ any internal layer} ∪ {`lab/`↔`ops/` direct} ∪ {`governance/`→`lab/` or `ops/`}.

**Falsifier:** if `check_boundaries.py` reports ≥1 illegal edge that cannot be resolved by widening `core/` (i.e. a genuine lab↔ops runtime coupling where neither side can be lifted to core), the four-layer model is wrong for this tree — **halt C2, return `DONE_WITH_CONCERNS`**, report the offending edge(s). Do not "fix" by relaxing the contract. The known `parity_check.py:222` edge is **not** falsifying (it is absorbed by §8 Q-d); a falsifying edge is one with no liftable shared artifact.

**H (integrity):** `check_pine_manifest.py`, `check_data_manifests.py`, and `tests/core/test_mc_anchors.py` all pass post-move with **unchanged hashes/anchors** (the move relocates; it must not mutate locked content; `Path(__file__).parent` data location makes this hold by construction).

**Falsifier:** any manifest hash or MC anchor changes value → a locked artifact was mutated, not moved → **BLOCKED (plan-itself-wrong if intentional, context-problem if accidental)**; revert the layer commit and report. Never regenerate hashes to paper over.

---

## §5 — Forbidden moves (genuinely tempting, ruled out)

1. **Start Phase C before ADR ACCEPTED.** The tree move is low-reversibility; the ADR is the ratification gate. Hard stop.
2. **`rm`/recreate instead of `git mv`.** Destroys history on the most history-load-bearing files (locked strategies, ADRs). `git mv` only.
3. **Relax the boundary contract to make the scan pass.** Defeats the point. A real illegal edge is a finding to report, not a contract to loosen (§4). Re-classifying `validate_candidate`→lab or widening `tv_export_loader`→core is correct placement, NOT relaxation.
4. **Regenerate manifest hashes to "make the gate green" after a move that changed content.** Red post-move means content mutated — investigate.
5. **Rule on the Q-SWAP SNAG without authority.** Standing default: CC drafts options, PO rules. **For this execution the PO has granted ruling authority (§0.5), so Step B2 rules and records the grant** — this forbidden move is lifted for this run only; absent an explicit grant it stands.
6. **Scope-creep the move into refactors.** "While I'm moving `portfolio_mc.py` I'll also clean up X." No. Relocate only; behavior-preserving. The only content edits permitted are mechanical relocation bookkeeping (import paths, the `tv_export_loader` import line, pyproject/checker paths). Any tempting logic refactor → note in §6 return, do not execute.
7. **Touch `live_journal/` internals.** Op-stream falsifier code; relocation only, zero logic edits (forward-asymmetry).
8. **Declare lab↔ops clean from a line grep.** The rev.-1/2 §0 did and missed `parity_check.py:222`. Use the AST-aware Phase-0 probe (§0).

---

## §6 — Reporting format (four-state taxonomy)

Return one of:
- **DONE** — all dispatched phases complete, §4 contracts green, §7 review-ready.
- **DONE_WITH_CONCERNS** — completed but flagged: an illegal boundary edge found (§4), a tempting-but-skipped refactor, or any off-pattern observation. List each concern for PO resolution before acceptance.
- **NEEDS_CONTEXT** — a missing input that can be supplied. Expected returns: after Phase B (awaiting ADR ratification for Phase C); or §0 Phase-0 AST probe surfaced a NEW ops↔lab edge.
- **BLOCKED** — unresolvable obstruction. State sub-case: **context-problem** (re-dispatch w/ more context) · **capability-problem** (needs stronger model / human) · **scope-problem** (decompose) · **plan-itself-wrong** (escalate to PO — e.g. §4 integrity falsifier fired).

Report per-step commit hashes so the parent can review each independently.

---

## §7 — Parent-session review (run by Claude/PO on return)

Two distinct passes, then a consolidated read (multi-step handoff, CC pattern 10):

1. **Spec-compliance pass** — did the executor build EXACTLY §2, nothing added? Specifically: no logic changes inside moved modules beyond mechanical relocation bookkeeping (diff each moved file; only import/path lines may differ); no deletions actioned **beyond** the one ADR-sanctioned ECR dedup (the duplicate skill-copy) — no deletion sweep is run (Step C4 WITHDRAWN — instrument retired on main); the Q-SWAP verdict ruled **only under the §0.5 authority grant**; `archive/` only evicted, not destroyed (tag resolves).
2. **Quality pass** — is `check_boundaries.py` a real AST scan (not a grep that misses aliased/lazy imports) with the uniqueness guard? Does the ADR's falsifier actually bind? Is the `CLAUDE.md` prune lossless (reconstruction check)? Did `tv_export_loader`→core dissolve the ops→lab edge?
3. **Consolidated read** — after all C-phase commits, one read across the whole diff: do the four layer-moves compose into a tree where `check_boundaries.py` + manifest gate + full `pytest` all pass *together*? Per-step green does not guarantee integration-green.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Archive eviction reversible + clean
git tag -l pre-prune-2026-06-05 | grep -q . && echo "recovery tag OK" || echo "FAIL: no recovery tag"
test -d archive && echo "FAIL: archive still in tree" || echo "archive evicted OK"
git show pre-prune-2026-06-05:archive/ >/dev/null 2>&1 && echo "archive recoverable from tag OK"

# 2. AST-aware lab<->ops probe (the §0 Phase-0 mandate; catches lazy imports grep misses)
grep -rnE "(from|import)[[:space:]]+(analysis|validation)([.[:space:]]|$)" \
  accounts.py cli.py parity_check.py fxify_rule_validator.py tv_mt5_pnl_reconciliation.py \
  live_journal/ weekly_review_feeder/ 2>/dev/null
echo "(pre-move: ONLY parity_check.py:222. post-move: ZERO — loader is core. else NEW edge)"

# 3. Boundary contract green (the §4 falsifier)
python scripts/check_boundaries.py && echo "boundaries OK" || echo "ILLEGAL EDGE — see output"

# 4. tv_export_loader widened to core (§8 Q-d)
test -f core/tv_export_loader.py && ! test -f analysis/oanda_stage1/tv_export_loader.py \
  && echo "loader in core OK" || echo "CHECK §8 Q-d"

# 5. Locked content unchanged (move not mutate)
python scripts/check_pine_manifest.py && python scripts/check_data_manifests.py \
  && python -m pytest tests/core/test_mc_anchors.py -q && echo "integrity OK"

# 6. Context file pruned + lossless (loaded every session)
test "$(wc -l < CLAUDE.md)" -lt 193 && echo "CLAUDE.md shrank OK"
test -f docs/mc_anchor_history.md && echo "history file exists" || echo "FAIL: history not extracted"

# 7. Layer map present (REPO_MAP = check_boundaries companion, NOT a deletion feed —
#    deletion instrument retired on main a9d16d0; deletion deliverable withdrawn)
test -f REPO_MAP.md && echo "layer map present OK" || echo "REPO_MAP layer map missing"

# 8. SNAG dossier authored + ruled under authority grant
test -f docs/methodology_audit/Q-SWAP-cluster-disposition.md && echo "dossier OK" || echo "FAIL"
grep -qi "ruling\|authority granted" docs/methodology_audit/Q-SWAP-cluster-disposition.md \
  && echo "ruling recorded under §0.5 grant OK" || echo "CHECK: dossier should record the ruling + grant"

# 9. No scope creep into moved-module logic (relocate-only)
git diff pre-prune-2026-06-05 --stat -- '*portfolio_mc.py' '*dd_protection.py' '*firm_rules.py' '*live_journal/*' \
  | grep -v "rename\|=> " && echo "WARN: content change in a relocate-only file" || echo "relocate-only OK"

# 10. ECR engine deduped (§8 Q-b): exactly ONE journal_review.py, under ops/
test "$(find . -name journal_review.py -not -path './.git/*' | wc -l)" -eq 1 \
  && find . -name journal_review.py -not -path './.git/*' | grep -q '^./ops/' \
  && echo "single canonical ECR engine under ops/ OK" || echo "DUPLICATE or misplaced ECR engine"

# 11. accounts co-located with its state (§8 Q-a): accounts.py in ops/, not core/
test -f ops/accounts.py && ! test -f core/accounts.py \
  && echo "accounts code+state co-located in ops/ OK" || echo "CHECK §8 Q-a"
```

---

## Verification (run before dispatch / on commit)

```bash
python scripts/check_brief.py docs/spec/CC-HANDOFF-monorepo-boundaries.md --type cc_handoff   # expect well-formed
git log -1 --oneline origin/main           # base = 0ec6e11 (PR#136) or later
sed -n '54p' validation/sweep/engine.py    # the legal lab->core edge
sed -n '222p' parity_check.py              # the ops->lab edge resolved by ADR §8 Q-d
grep -rn "import archive\|from archive" --include=*.py . | grep -v '^./archive/'  # expect empty
```
