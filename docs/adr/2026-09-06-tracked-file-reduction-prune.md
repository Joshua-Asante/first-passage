# ADR 2026-09-06 — Tracked-file reduction: present-need survivor set, verified archive preservation

**Status:** `Proposed` — operator (JA) adjudicated the survivor rules and path sets in-session 2026-09-06; merge of the reduction PR is the executed ratification; the §3 archive-push gate is satisfied. **Tier: full** — doctrine limb fires (mass deletion of decision and research records under §16 Retention).
**Decision date:** 2026-09-06
**Authors:** Joshua (direction + adjudication) + Claude Code (path sets, verification, implementation)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none — standing record of what left the tree and where it lives; the 2026-11-08 quarterly audit reads §6.
**Baseline:** `first-passage@2d40dbeb56c167844cab5136742d70787835f8e2` (origin/main, 3,039 tracked files).
**Preservation commit:** `first-passage-archive` branch `archive/preserve-2026-09-06` @ `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` — every removed path at its exact baseline blob.
**Index:** [`lab/ARCHIVED.json`](../../lab/ARCHIVED.json) — one entry per removed path (baseline blob SHA) and per affected study.

---

## 1. Decision

Reduce the tracked tree from **3,039 to 1,500 files** (≤ 1,519 ceiling; 50.64% reduction): **1,497 survivors, 1,542 removals, 3 additions** (this ADR, `lab/ARCHIVED.json`, and `tests/test_archive_lab_analysis_archived_index.py`). The survivor and removal path lists partition the baseline exactly — intersection empty, union equal to the 3,039 baseline paths, no duplicates — asserted on the emitted lists, not in memory.

Operator decisions (verbatim, 2026-09-06):

> * Approve removing the obsolete closure exemptions, while preserving checks for surviving closures.
> * Keep the small uncertain survivor groups for this pass. Further classification would add little value.
> * Require archive verification before removal, using immutable commit and blob references.
> * Include the surviving-document link cleanup in the implementation, rather than leaving broken navigation behind.

And the framing that governs every retention call below: *every retained bundle must earn its place through a present need. Historical complexity explains why pruning requires care; it should not decide the outcome.* A historical citation is a dependency to resolve — an archive reference — not a retention entitlement, unless the cited content is executed or gate-validated.

## 2. Survivor rules (the adjudicated object)

Built forward from operating code and current obligations, not backward from citations.

* **Wholesale survive:** `core/ ops/ scripts/ tests/ .github/ .claude/ .cursor/ .agents/ deploy/ discovery_manifests/`; every root file; `lab/` infrastructure (`CATALOG.md`, `README.md`, `conftest.py`, `replay_funding.py`, `validation_selftest.py`, `research_utils/`, `discovery/`, `tools/`, `databento_fetch/`, `pine/`, `data/`); `docs/ltm/`, `docs/methodology/`, `docs/pursuits/` (gate-validated register), `docs/notes/{rail_build,sentinel}/`; the seven docs root files; `docs/{adr,briefs}/{README,INDEX}.md`; every loose `docs/briefs/Q-*.md` (§16 R1: open briefs); the live campaign-state document.
* **Explicit study list (present need traced, not inferred from the `ACTIVE` label):** the Queue-#1 campaign body; studies named in the live campaign document's instrument-provenance table; studies named in STATE.md; the CATALOG *In flight* registry; the R5 falsifier directory `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/` (the 2026-11-08 S4-discharge falsifier commands execute its scripts); studies a surviving test executes or reads. Where only a named file is needed, only that file survives.
* **Executed or gate-validated citation only:** docs targets cited from CLAUDE.md, STATE.md, README.md, code, tests, harness config, `docs/methodology/`, the campaign document; lab targets cited from `core/**` (locked record — not edited to repoint), runtime `spec_from_file_location` in `scripts/`/`ops/`, `ops/instruments/{MECHANISMS.md,PROFILES.md,profiles.json}` and per-symbol ledger `source:` cells (`instrument_profiles.py` resolves them with `.exists()`), `discovery_manifests/`, skills and rules (`check_skill_refs`), `docs/load_bearing_numbers.md` (names each live figure's sole owner); ADR header `Supersedes*` edges to closure (`check_adr_graph`); sibling `import` closure for surviving lab modules; the `lab/analysis/<slug>/CARD.md` stub wherever any `lab/archive/<slug>/` file survives.
* **Not citing surfaces (historical by definition):** `REPO_MAP.md`, `PIPELINES.md`, `docs/SESSIONS.md`, `docs/rejected_candidates.md`, `docs/mc_anchor_history.md`, `lab/CATALOG.md`, `docs/ltm/**`, `docs/pursuits/**`, per-symbol ledger prose rows, INDEX/README files.
* **Kept on judgment for this pass (operator):** nine files whose only signal is the CATALOG In-flight label; two files cited from WARN-only/unscanned skill references; `docs/pursuits/` wholesale.

The per-path reason column of the survivor list is the audit trail (`survivor_reasons.tsv` in the reduction working set).

## 3. Archive preservation and verification

* `archive/main` was frozen at 2026-08-15, twenty-one days behind the baseline. Blob comparison of all 1,542 removals: 967 already identical there, 95 stale, 480 absent. Deleting without preservation would have destroyed 575 files.
* Preservation commit `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` (branch `archive/preserve-2026-09-06`, parent `archive/main` @ `73971f1`) restores all 1,542 paths from `2d40dbe`. Verification: `git ls-tree -r` of the preservation commit against the baseline — **1,542 / 1,542 blob SHAs identical**. The commit was made in a hook-free clone; no gate was bypassed.
* **Merge precondition — satisfied 2026-09-06.** The preservation commit is pushed: `first-passage-archive` `refs/heads/archive/preserve-2026-09-06` resolves to `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2`. Verified against the remote, not the local clone — the ref was fetched into an empty object store and its `git ls-tree -r` compared to the baseline: **1,542 / 1,542 removed paths present, every blob SHA identical**. `lab/ARCHIVED.json` `archive_commit_pushed_and_verified` is `true`. ⚠ The archive repository was `archived` (GitHub read-only) and had to be unarchived to accept the push — a future preservation push hits the same wall and the same fix.
* Retrieval on this clone needs no archive: `git show 2d40dbeb56c167844cab5136742d70787835f8e2:<path>`.

## 4. Executed in the implementation diff

1. `git rm` of the 1,542 paths (literal pathspecs from the adjudicated list).
2. `lab/ARCHIVED.json` — 1,542 file entries (baseline blob, archive status at generation) and 191 study entries (102 hot-table, 89 archived-table; 39 with files retained) carrying theme/status/one-liner/closed from the baseline CATALOG — every baseline CATALOG row whose body lost a file, checked by slug set-difference against the regenerated CATALOG (baseline-only slugs: 0).
3. `scripts/archive_lab_analysis.py` — `load_archived_index()` / `_rows_from_archived_index()`; `scan_lab()` step (c) adds an archived-elsewhere row per indexed study (body cell = archive URL, `hot="no"`), replacing any partial on-disk remnant row for the same slug so no slug renders twice; `render_catalog()` splits Hot/Archived on `hot`, not on body prefix. Tests: `tests/test_archive_lab_analysis_archived_index.py`. No gate resolves index paths against disk; the index is a retrieval and rendering aid, nothing more.
4. `scripts/check_closure_disposition.py` — 14 names removed from `GRANDFATHERED` (their closures left the tree; `test_grandfather_list_matches_the_adr_boundary` asserts every listed name exists). The registry snapshot sets (`REGISTRY_*`, pinned 66/30/36, forward-only) are untouched: they are consulted only for closures on disk.
5. Navigation: **1,188 markdown links in 286 surviving files** repointed to `https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc…/<path>` (`/tree/` for directories), anchors preserved. Classes: ops instrument ledgers 277, briefs 403, ADR bodies 198, `rejected_candidates.md` 98, notes 69, pursuits 52, spec 50, superpowers 23, methodology 5, analytics 4, root docs 4, docs/README + operational_rules 4, governance 1. Ledger `source:` cells were not touched (their targets survive).
6. Regenerated: `docs/adr/INDEX.md` (`check_adr_graph.py --regenerate-index`), `lab/CATALOG.md` (`archive_lab_analysis.py --regenerate-catalog`; 223 rows — 9 in-flight, 22 hot, 192 archived, of which 191 carry an archive-URL body).
7. Pointers: CLAUDE.md §Purpose retrieval sentence, `docs/ltm/README.md` lookup order, `REPO_MAP.md` banner.

## 5. Deliberately not done

* **Frozen surfaces keep their dead links** (archive-resolvable via §3): `docs/SESSIONS.md` (append-only gate), `docs/briefs/pre-registration/**` and campaign-resident `PREREG*.md` (frozen registrations), `docs/ltm/**` (cold store), retained research bodies under `lab/` (evidence; some are hash-pinned by private receipts), `core/**`, `tests/**`.
* `REPO_MAP.md` and `PIPELINES.md` narrative sections describing pruned directories are not rewritten — banner + link repoints only. Rewriting the map is a follow-up the operator judges separately.
* Partial-retention studies (39) render from their `ARCHIVED.json` row; their on-disk remnants are fixtures, not bodies.

## 6. Verification

Dry-run on a throwaway copy of the survivor tree before implementation: all blocking gates green (`instrument_profiles`, `check_falsifier_reachability`, `check_skill_refs`, `check_status_consistency`, `check_supersession_placement`, `check_lifecycle_consistency`, `check_closure_disposition`, `check_pursuit_records`, `check_boundaries`, `check_path_liveness`, `check_state_currency`, sessions gates); residue was exactly the obligations executed in §4 (root-doc links, INDEX drift, CATALOG drift). `pytest lab/ --import-mode=importlib`: 100 passed. `pytest tests/`: 2,794 passed, 33 skipped; the eight prune-induced failures resolved by §4 items 3–6 and three retained fixtures; the five `tests/test_temporal_consistency.py` failures read `docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`, absent from the baseline itself, and fail on the untouched tree — pre-existing, not prune-induced.

Implementation branch (this diff, complete runs, 2026-09-06): `python scripts/gate_manifest.py --tier pre-commit` — every gate OK, exit 0 (`check_status_consistency` 0 advisory notes after the index fix in §4 item 2). `pytest tests/` — 2,804–2,805 passed, 34 skipped across two full runs; failures: the same five `test_temporal_consistency.py` cases, re-confirmed failing on the untouched baseline tree in the same session (5 failed / 7 passed there; the file they read is absent from `2d40dbe`), plus one first-run failure that was not a tree change — `test_tradeify_phase1_runner::test_committed_manifest_matches_frozen_five_strategy_acceptance` hashes `tradeify_commission_schedule.json` from disk, and the implementation worktree had checked that file out CRLF (`core.autocrlf=true`, file attribute `eol=lf`); index and baseline blobs are identical (`32c2ec97…`), re-checkout with the attribute gives the manifest hash and the test passes. `pytest lab/ --import-mode=importlib` — 100 passed.

## 7. Residual judgment and pre-existing conditions

* Pre-existing, unchanged by this ADR: the five `test_temporal_consistency.py` failures above; `archive_lab_analysis.py --check` (full mode) notes for unstubbed archiveable closes (`tnec_l2_sourcing_2026-08-10`, `orb_mnq_recon_v3_2026-08-31`) present on the baseline.
* Follow-ups for the operator: rewrite `REPO_MAP.md`/`PIPELINES.md` for the reduced tree; decide whether the nine In-flight-label-only files and the two WARN-reference files stay at the next audit.
