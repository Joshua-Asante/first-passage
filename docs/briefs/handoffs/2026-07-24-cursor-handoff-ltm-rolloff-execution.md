# Cursor Handoff — LTM roll-off execution (SESSIONS roll + repair, briefs/spec/notes roll, lab archive backlog)

**Date:** 2026-07-24
**Parent session:** Claude Code operator session — Algorithm repo review (umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** Cursor — **LOCAL DISPATCH ONLY, on the PRIMARY CHECKOUT** (see routing test 0).
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** N/A — executes the standing STM/LTM designs against their measured backlog.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Move/roll/repair only — no content rewrites; STATE.md and CLAUDE.md are OUT OF SCOPE** (owned by operator directive 2026-07-23 #4's separate session).
**Dispatch order:** independent of briefs #1–#4; run when a quiet window exists on the primary checkout (the SESSIONS roll edits a merge=union file — do it when no other session is writing). **Rescoped 2026-08-03 — see §0-REFRESH below.** Step 2.1 and the INDEX sub-item of Step 2.3 are DISCHARGED (already executed outside this brief); remaining scope is the archive-mojibake repair, Step 2.2, the spec/notes sub-item of Step 2.3, and Step 2.4 (count corrected 14→19).

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`)

- **Test 0 (dispatch environment) — LOCAL, full stop.** Three reasons: (a) `scripts/archive_lab_analysis.py --check` and `make check` gates hard-fail on checkouts without the gitignored heavy files (standing quirk, memory `reference_worktree_commit_gate_quirk`); (b) `docs/SESSIONS.md` is merge=union (`.gitattributes`) — rolling it from a stale checkout multiplies entries; (c) CATALOG regeneration must run where the full `lab/` tree lives. Cloud dispatch is NOT eligible.
- **Test 1:** No locked surface. Files: `docs/SESSIONS.md`, `docs/briefs/**` moves to `docs/ltm/**`, `docs/briefs/INDEX.md` rows, `docs/spec/**` + `docs/superpowers/**` + `docs/notes/**` moves, `lab/analysis/**` archive runs via the OWNED SCRIPT, `lab/CATALOG.md` via regeneration ONLY (hand-editing corrupts it — standing memory). No core, no Pine, no ADR content edits.
- **Test 2:** Yes — mechanics are owned by existing scripts + the inbound-link rule in §0.5(A); item lists are Phase-0-computed against frozen criteria, not judgment.
- **Test 3:** Clears easily (largest brief of the series).

---

## §0 — Rule 0 reads (PHASE 0 — read-report before any move)

Anchors verified at `33356ea` (2026-07-24). Report each; `NEEDS_CONTEXT` on contradiction.

- `scripts/roll_sessions.py` — report its contract (docstring: keep newest N=20 live), the archive destination convention (`docs/ltm/notes/archive/sessions/SESSIONS-2026-Q*.md`), and `--dry-run` support. Parent-measured **133** live entries (`grep -c "^## 2026-" docs/SESSIONS.md`) as of the 2026-07-24 merge of `origin/main`; archives currently end at 2026-07-11. **The exact count is not load-bearing** — it drifts with every landed session and only the keep-20 delta matters; re-measure and proceed, do not bounce on a count difference alone.
- `docs/SESSIONS.md` corruption sites — report: entry headers at lines ~212 (`## 2026-07-22 ? OPENPRESS-1 …`) and ~222 (`## 2026-07-21 ? MYM third-Friday …`) carrying `?`/`�` mojibake (bodies too: ~214, 216, 218, 225, 226, 228); date-ordering inversions (a 07-21 entry between two 07-22 entries near lines 122–142; 07-22 below 07-21 near 202–212; a 07-16 above a 07-17 near 553–573). Both corrupt entries came from the `cursor/mym-third-friday-probe-98f0` branch and were missed by the `e6d823f` restore.
- `scripts/archive_lab_analysis.py` — report: the `--slug` archive flow, `--regenerate-catalog`, `--check --catalog-only`, and the verdict-parse rules it reads from study files (needed for §2.4(b)). NEVER hand-edit `lab/CATALOG.md`.
- `lab/CATALOG.md` — report the **14** rows tagged "archive owed" (parent-measured count; list the slugs). Also report the rows for `striker_mym_reconstruction_candidate1_2026-07` (reads ACTIVE; its own `DEVELOPMENT_RESULTS.md` opens "Development-only verdict: **FALSIFIED**") and `regime_fit_2026-06-17` (closed by its RESULTS).
- `docs/ltm/README.md` + `docs/briefs/INDEX.md` — report the roll conventions (closed briefs → `docs/ltm/briefs/**` mirroring subdirs; INDEX rows deleted on close per its lines 8–9) and the 5 CLOSED rows still in the Open table (parent-verified: Q-RAIL-1, Q-PYRPARITY-1, Q-INVENTORY-1, Q-BUSTGATE-1, Q-KBUDGET-HARVEST-1 — leaving Q-XMEM-1 open + 2 partials).
- `lab/research_utils/prereg_paths.py` — report its LTM-roll mechanism (a rolled pre-registration is a one-line path change; live importers: `universe_gate.py`, `temporal_consistency.py`, `stage24_runner.py`, 4 test files).
- **Inbound-link census (the load-bearing §0 computation):** for EVERY candidate move file, compute inbound links from the HOT set (`CLAUDE.md`, `STATE.md`, `README.md`, `PIPELINES.md`, `REPO_MAP.md`, `docs/operational_rules.md`, `docs/briefs/**` non-moving files, `docs/adr/**`, `.claude/skills/**`, `ops/**`, `lab/**` non-archived). Report the two buckets: zero-inbound (Phase-1 movable) vs linked (Phase-2, deferred). Parent-measured context: STATE.md alone carries ~62 unique `docs/briefs/` links — bulk-moving linked files would shatter the root docs the queued authority-sync session owns.
- **Parent-verified keep-list (do NOT move):** `docs/spec/2026-06-27-session-log-rolloff-design.md` (design of a LIVE recurring workflow), `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md` (deliberately PARKED record), `docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md` (live trigger-dated decision), `docs/notes/2026-06-06-codifier-signal-fn-bridge-sketch.md` (cited by live `lab/codification/compose.py`), `lab/analysis/legacy/usoil_regime_capture/` (PARKED, 08-08 revisit), `lab/analysis/legacy/guardian_parity_2026-06-23/` (hosts PORT_MANIFEST.sha256 — open QUESTION item), all `docs/briefs/pre-registration/` files with live `prereg_paths.py` importers unless the path constant is updated in the same commit.

---

## §0-REFRESH — 2026-08-03 (repo-truth-sync rescope)

Per-item re-measurement against `main` @ `131b99b` (post SESSIONS-roll commit `0392011`). This section supersedes §0's counts where they conflict; §0's mechanics (script contracts, conventions) are unchanged and still authoritative.

- **Step 2.1 (SESSIONS repair+roll) — DISCHARGED, but with a residual not in the original scope.** `python scripts/roll_sessions.py` was run directly on the primary checkout 2026-08-03 (`0392011`): `docs/SESSIONS.md` now holds **20** live entries (`grep -c "^## " docs/SESSIONS.md` = 20); 14 entries rolled into `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md` (227 entries total there now, from 213). This is the exact condition §4 named as falsifying ("SESSIONS already rolled to 20") — **do not re-dispatch Step 2.1.**
  - **Ordering-inversion premise: RESOLVED, unrelated cause.** The three inversions §0 cited (07-21-between-07-22, 07-22-below-07-21, 07-16-above-07-17) do not appear anywhere in the current live file or the Q3 archive (`grep -n "^## 2026-07-1[5-8]\|^## 2026-07-2[0-3]" docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md` — strictly descending, zero inversions). Closed independently by `e0fcab7` ("order same-date entries by git author time, and gate it") before this roll ran. §0.5(C) is moot.
  - **Mojibake premise: NOT resolved, now archived instead of live.** The roll ran without the §0.5(B) repair-first step, so both flagged corrupt entries carried into the archive uncorrected: `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md:2009` (`## 2026-07-22 ? OPENPRESS-1 …`, body mojibake at :2011) and `:2059` (`## 2026-07-21 ? MYM third-Friday …`). **New residual task, in-scope for whoever picks this up next:** repair those two headers/bodies in place in `SESSIONS-2026-Q3.md` per §0.5(B)'s restore-from-`STATE.md`-parallel-text method — same fix, different file, smaller blast radius (2 entries, not a live-file roll).
- **Step 2.3, INDEX.md sub-item — DISCHARGED, already done.** All 5 flagged rows (Q-RAIL-1, Q-PYRPARITY-1, Q-INVENTORY-1, Q-BUSTGATE-1, Q-KBUDGET-HARVEST-1) are gone from `docs/briefs/INDEX.md`'s Open table — they're correctly filed under "Recently closed" instead. Current Open table holds exactly 5 rows (Q-FUNDPOL-1, Q-XMEM-1, Q-TOM-SPX-1, Q-TVCOV-1, Q-SIGID-1), none of them stale. Do not re-dispatch this sub-item. (Unclear which commit did this — not attributed here; re-verified by direct read of `INDEX.md`, not inferred.)
- **Step 2.3, spec/superpowers/notes sub-item — UNVERIFIED, still open.** Not re-measured this pass (would need a fresh zero-inbound-link census, the brief's own "load-bearing §0 computation" — too expensive to redo without dispatching it). Whoever redispatches this must re-run the inbound-link census fresh; do not reuse the 07-24 buckets.
- **Step 2.4 (lab archive backlog) — count moved, did not shrink: 14 → 19.** `grep -c "archive owed" lab/CATALOG.md` = **19** (grew, not drifted down — five new studies landed archive-owed status since 07-24: `c1_capalloc_2026-07-27`, `geofit_skew_probe_2026-07-25`, `q_funnel_1_2026-07`, `slr_mym_phase05_2026-07-29`, plus one more — full current list: `c1_capalloc_2026-07-27`, `d5_recost_2026-07`, `feed_divergence_2026-06`, `geofit_skew_probe_2026-07-25`, `mym_3fps_recon_2026-07`, `ng_eia_recon_2026-07`, `opening_pressure_map_2026-07`, `orb_zb_recon_2026-07`, `q_bookfit_1_2026-07`, `q_fbeia_1_2026-07`, `q_fccarry_1_2026-07`, `q_funnel_1_2026-07`, `q_geofit_1_2026-07`, `q_kbudget_1_2026-07`, `q_pyrparity_1_2026-07`, `q_znauc_1_2026-07`, `rates_ev_zf_recon_2026-07`, `slr_mym_phase05_2026-07-29`, `xindex_rv_recon_2026-07`).
  - The two §0.5(D) verdict-line targets are **unchanged, both still needed**: `striker_mym_reconstruction_candidate1_2026-07` still reads `ACTIVE` in CATALOG despite its own `DEVELOPMENT_RESULTS.md:3` stating `Development-only verdict: **FALSIFIED**`; `regime_fit_2026-06-17` still reads `ACTIVE` despite its `RESULTS.md` being a closed two-part verdict (structural decay RULED OUT / execution FIX-EXECUTION) dated 2026-06-17.
- **Keep-list — all 6 confirmed still present, unchanged:** `docs/spec/2026-06-27-session-log-rolloff-design.md`, `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md`, `docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md`, `docs/notes/2026-06-06-codifier-signal-fn-bridge-sketch.md`, `lab/analysis/legacy/usoil_regime_capture/`, `lab/analysis/legacy/guardian_parity_2026-06-23/`.

**Net effect on §4's H:** the original H is **partially falsified by its own named condition** (SESSIONS rolled to 20) — that shape-change is exactly what §4 said would bounce `NEEDS_CONTEXT`. Rather than bounce, this refresh narrows the brief in place: **Step 2.1 and the INDEX sub-item of Step 2.3 are removed from anything to dispatch** (both discharged); the SESSIONS-archive mojibake repair is added as a small new item; Steps 2.2, the spec/notes sub-item of 2.3, and 2.4 remain open with 2.4's count corrected to 19 (up, not down). A future dispatch should carry only: archive-mojibake repair, briefs zero-inbound roll (2.2), spec/superpowers/notes zero-inbound roll (2.3 remainder), lab archive backlog at 19 slugs + 2 verdict-lines (2.4).

---

## §0.5 — Clarifying questions (Cursor variant — parent-recommended defaults)

- **(A) Linked-file moves.** **Recommended default:** Phase 1 (this PR) moves ONLY zero-inbound-link files. Files with any hot-set inbound link are listed in the closure report as the Phase-2 worklist for the operator's authority-sync session — NOT moved, NOT link-rewritten here. Exception: a file whose ONLY inbound link is `docs/briefs/INDEX.md`'s row being deleted in §2.3 counts as zero-inbound.
- **(B) Mojibake repair source.** **Recommended default:** restore the corrupted characters from the same entries' clean parallel text in `STATE.md` (the OPENPRESS-1 and MYM-3FPS-1 pointer-log lines carry the same phrases with correct em-dashes/×/→) and from `git show` of the originating `cursor/mym-third-friday-probe-98f0` commits if available. Write UTF-8 no BOM. If a character cannot be confidently restored, use a plain ASCII hyphen and note it — never leave `�`/mis-encoded bytes.
- **(C) Ordering-inversion repair.** **Recommended default:** reorder whole entry blocks to strict reverse-chronological by header date, preserving every byte of entry bodies. Do this BEFORE running the roll so the keep-20 window is date-correct.
- **(D) Unflagged closed studies (§2.4(b)).** **Recommended default:** for `striker_mym_reconstruction_candidate1_2026-07` and `regime_fit_2026-06-17` only, add the parseable one-line `**Verdict:** <STATUS>` header the regenerator reads (exact format from the Phase-0 read of `archive_lab_analysis.py`; FALSIFIED per DEVELOPMENT_RESULTS, and the regime_fit status per its own RESULTS.md), then regenerate. Any OTHER suspected-stale CATALOG row: report only.
- **(E) Roll batch size.** **Recommended default:** four commits in one PR — (1) SESSIONS repair+roll, (2) briefs/INDEX roll, (3) spec/superpowers/notes roll, (4) lab archive+catalog — so a defect in one batch doesn't hold the rest hostage.

---

## §1 — Context

The review measured a stalled roll-off across every LTM mechanism the repo built: SESSIONS at 130 live entries vs the keep-20 contract (plus mojibake + ordering corruption from a Cursor branch); ~84% of `docs/briefs/` hot files tied to closed investigations; INDEX.md's Open table 5/8 dead rows; 8 spec/plan split pairs and ~10 consumer-free notes; 14 CATALOG-flagged "archive owed" lab studies (69 files) plus unflagged closed-but-ACTIVE rows. The machinery (roll_sessions, archive_lab_analysis, ltm conventions, prereg_paths) all exists — this handoff runs it, at scope frozen by the inbound-link rule so it cannot collide with the queued CLAUDE/STATE authority-sync session.

**Deliverable:** one `cursor/*` PR (4 commits per §0.5(E)) from the primary checkout, plus a Phase-2 worklist (linked files deferred) in the closure report.
**NOT asked:** editing STATE.md/CLAUDE.md, rewriting any rolled content, touching ADRs, archiving anything on the keep-list, hand-editing CATALOG.

---

## §2 — Execution plan

### Step 2.1 — SESSIONS repair + roll — ~~Cursor~~ **DISCHARGED 2026-08-03, do not re-dispatch**

The roll itself is done (`0392011`, 20 live / 227 archived). **Residual, not the original action:** repair the two mojibake entries now sitting in `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md` at lines ~2009 and ~2059 — same §0.5(B) restore-from-`STATE.md`-parallel-text method, applied to the archive file instead of the live one. Ordering repair (§0.5(C)) is moot — see §0-REFRESH.
- **Per-step gate (for the residual only):** `grep -n "�\|^## .* ? " docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md` → zero.

### Step 2.2 — Briefs roll (zero-inbound only)

- **Action:** `git mv` each zero-inbound closed brief (closures/, spent handoffs/, spent pre-registrations with no live importer or with the `prereg_paths.py` one-line update in the same commit, closed top-level Q briefs, spent rnd-pipeline scopings) to the mirrored `docs/ltm/briefs/**` path.
- **Per-step gate:** `python scripts/check_path_liveness.py` + `python scripts/check_root_doc_liveness.py` green; `pytest tests/ -k prereg -q` green if `prereg_paths.py` was touched.

### Step 2.3 — INDEX.md + spec/superpowers/notes roll — **INDEX sub-item DISCHARGED 2026-08-03, remainder OPEN**

- ~~Action: delete the 5 CLOSED rows from INDEX.md's Open table~~ — already done; all 5 (Q-RAIL-1, Q-PYRPARITY-1, Q-INVENTORY-1, Q-BUSTGATE-1, Q-KBUDGET-HARVEST-1) are gone from the Open table. Do not re-dispatch this sub-item.
- **Remaining action:** move the zero-inbound spent items from `docs/spec/` (minus keep-list), the rolled-plan design halves in `docs/superpowers/specs/`, and the consumer-free `docs/notes/` files (minus keep-list) to their mirrored `docs/ltm/**` homes. **Counts are stale (07-24 figures) — re-run the zero-inbound-link census fresh at dispatch time; do not reuse `~7` / `8` / `~10`.**
- **Per-step gate:** liveness gates green; keep-list files untouched (`git status` scan).

### Step 2.4 — Lab archive backlog — count corrected 14 → 19 (2026-08-03)

- **Action:** (a) for each of the **19** "archive owed" slugs (list in §0-REFRESH): `python scripts/archive_lab_analysis.py --slug <slug>` (body → `lab/archive/`, stub CARD.md remains); (b) apply §0.5(D) verdict lines (both targets unchanged: `striker_mym_reconstruction_candidate1_2026-07`, `regime_fit_2026-06-17`); (c) regenerate CATALOG via the script.
- **Per-step gate:** `make lab-catalog-check` green; `python scripts/archive_lab_analysis.py --check --catalog-only` green; the 19 slugs now show archived rows; zero hand edits to CATALOG.md (`git diff` on it is regeneration-shaped).

### Step 2.5 — Closure

Report per §6. Closure report MUST include: counts moved per batch, the Phase-2 deferred worklist (linked files, grouped by linking root doc), and any keep-list adjacency observations.

---

## §4 — Falsifiable hypothesis

**H (premise, not an investigation):** the parent-measured backlog (SESSIONS well over the keep-20 contract — 133 at authoring, 14 CATALOG-owed archives, 5 dead INDEX rows) and the keep-list still hold at dispatch time. **Falsified if** a Phase-0 re-measurement contradicts the *shape* of the backlog (e.g. SESSIONS already rolled to 20, or zero owed archives) or a keep-list file has moved — bounce `NEEDS_CONTEXT` with the delta quoted. A mere count drift (new sessions landed) is NOT a falsification; re-measure and proceed.

**2026-08-03 — this H's named falsifying condition FIRED** ("SESSIONS already rolled to 20" — see §0-REFRESH). Per the brief's own rule this would bounce `NEEDS_CONTEXT` wholesale; instead of bouncing, the brief was rescoped in place (§0-REFRESH) since most of the remaining scope (2.2, 2.3-remainder, 2.4) was unaffected by that specific condition. **Rescoped H:** the remaining backlog — 2 archived mojibake entries, an unmeasured briefs/spec/notes zero-inbound census, and 19 CATALOG-owed archives (up from 14) plus 2 unchanged verdict-line targets — holds as of 2026-08-03. Falsified under the same rule if a fresh Phase-0 at next dispatch finds any of these already zero or already fixed.

---

## §5 — Forbidden moves

- **Moving a linked file and "helpfully" rewriting the inbound links** in STATE.md/CLAUDE.md — that is the authority-sync session's scope (operator directive 2026-07-23 #4). Defer per §0.5(A).
- **Hand-editing `lab/CATALOG.md`** — regeneration only (standing memory: hand edits corrupt it).
- **Archiving keep-list items** — each is deliberately live/parked/blocked (§0 keep-list).
- **Running the SESSIONS roll from a worktree or stale checkout** — merge=union multiplies entries.
- **Content edits during moves** ("fix this typo while moving") — moves must be byte-identical so `git log --follow` stays clean; the ONLY content edits authorized are §2.1 repairs and §0.5(D) verdict lines.
- **Rolling `docs/briefs/pre-registration/` files with live importers without the same-commit `prereg_paths.py` update.**

---

## §6 — Gate + status return

Report EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>` per `references/cc_handoff.md` §6, with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the per-step gates is the entire closure.

---

## §7 — Parent-session review (after return)

Pass 1: per-batch counts match the Phase-0 buckets; keep-list untouched; no linked file moved. Pass 2: liveness gates + full `make check` green ON THE PRIMARY CHECKOUT; spot-`git log --follow` three moved files; SESSIONS archives byte-contain the rolled entries. Pass 3: read the four commits together — INDEX rows deleted must correspond to briefs actually rolled (or already in ltm); CATALOG regeneration must reflect exactly the §2.4 archive set.

---

## §10 — Audit hooks (runnable)

```bash
grep -c "^## 2026-" docs/SESSIONS.md                                  # expect: 20
grep -c "archive owed" lab/CATALOG.md                                  # expect: 0
python scripts/check_path_liveness.py && python scripts/check_root_doc_liveness.py
python scripts/archive_lab_analysis.py --check --catalog-only
git ls-files docs/spec/2026-06-27-session-log-rolloff-design.md docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md
# Expected: both still present (keep-list).
```

---

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cursor-handoff-ltm-rolloff-execution.md
# And post-merge, on the primary checkout:
make check
```
