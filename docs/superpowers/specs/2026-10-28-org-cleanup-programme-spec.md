# First Passage org cleanup programme — recommended spec

**Status:** Approved. Joshua approved D1–D14 as recommended on 2026-10-28 ("Approve all"), including D2 as his explicit request to rewrite the standing instructions listed there. Ratification GOs under D9 are still given per PR. Base: origin/main `bb6dbc1`, 2026-10-28.
**Question:** what is the safest route, at the fewest operator hours, to a ~25 KB session-start load, with every removed artifact retrievable? **Decision it changes:** which PRs open from 2026-10-29, in what order, and under which operator GOs.
**Evidence:** the seven map reports at `C:\Temp\claude\C--Users-joshu-multi-firm-operations--claude-worktrees-first-passage-org-review-2a02ee\7701e15c-1238-4a40-a866-34917866cd8f\scratchpad\map\`, plan `docs/superpowers/plans/2026-10-25-rule-consolidation-step-1.md` §6–§8, and the bodies of #855 and #935. **[U]** marks a claim that is not verified; the owning leg verifies it before it acts.

## 0. Summary

**Spine.** The subtraction design: four phases, deletion as the main lever, 26 PRs. Three pieces are grafted onto it:

- from **guard-first**: a ratcheting anchor and path checker, a byte-budget gate and a docs-reader CI job, all landed before any fold merges;
- from **throughput**: re-derivation of #935 by file class, short `rule-N` aliases, and the **11-09 red-main** deadline (verified in `check_state_currency.py`);
- from **subtraction**: closing #855 and #935, a per-batch retrieval table, and the tiered orientation definition.

**Calendar.** Critical path is about 28 days (10-28 → ~11-25). Operator time is about 4 h: 14 rulings, 5 ratification GOs and one 11-08 owner check.

**Hard dates:**

| Date | What must land |
|---|---|
| 10-30 | STATE weekly roll |
| 11-08 (Sat) | STATE `### 2026-11-08` heading marked DISCHARGED. From 11-09 every PR is red otherwise |
| 11-06, 11-13, 11-20 | Weekly rolls |

### End-state targets

| Metric | Now (measured at `bb6dbc1`) | Target | Measured by |
|---|---|---|---|
| Session-start load (T0, §3.1) | AGENTS 27,855 + STATE 42,879 = 70,734 B (AGENTS 29,403 B after #947) | **≤14,336 B** gated. **≤25,600 B** including the T1 read | `check_doc_budgets.py` (P1.1) |
| AGENTS.md | 27,855 B | ≤8,192 B (disclosed fallback ≤9,216 under D5) | same |
| STATE.md | 42,879 B | ≤5,120 B. Interim ≤9,216 B until the 11-08 section leaves | same |
| docs/operational_rules.md | 84,589 B | ≤45,056 B | same |
| PIPELINES.md | 10,902 B | ≤4,096 B | same |
| docs/SESSIONS.md | 248,651 B, 105 entries | ≤76,800 B, 30 entries (2.37 KB average × 30) | same |
| docs/ tracked files | 1,075 | ≤850. P0.8 manifest sets the binding figure | `git ls-files docs \| wc -l` |
| docs/ bytes | 23,305,484 | ≤17 MB [U estimate; S5 dump kept per D8] | `git ls-files -z docs \| xargs -0 cat \| wc -c` |
| docs/ top-level folders | 13 | 10 (lessons, skill-drafts, external removed) | `git ls-files docs \| awk -F/ 'NF>2{print $2}' \| sort -u \| wc -l` |
| ADR files (excluding INDEX, TOMBSTONES) | 140 | ≤100 after P1.3; ≤95 at close [U] | `git ls-files docs/adr \| wc -l` minus 2 |
| Max addendum headings per ADR | 14 (c1 GO) | 0 superseded addenda in the 7 folded ADRs. Corpus max ≤5 | `rg -c "^#+ .*[Aa]ddendum" docs/adr` |
| Repo skills, count / SKILL.md bytes | 23 / 365,590 B | 22 / ≤300 KB | `git ls-files -z '.claude/skills/*SKILL.md' \| xargs -0 cat \| wc -c` |
| DRAFT-named docs | 57 | ≤45 (orphans and executed cards only; code-named DRAFTs never move) | `git ls-files docs \| grep -ci draft` |
| Broken path and fragment links in living `.md` | B₀ unmeasured (no checker exists) | **0**, gated fail-closed. The frozen-file allowlist is non-increasing | `check_md_anchors.py` with no baseline (P3.6) |
| Open cleanup-shaped PRs | 4 (#855, #935, #944, #947) | 0 | `gh pr list` |

## 1. Scope

**In scope:**
- root docs, `docs/**` and `.claude/skills/**`;
- ADR chains;
- the tooling named in §3;
- the retrieval record.

**Out of scope:**

- **User-level memory store** (`~/.claude/projects/.../memory`), memedit and lint tooling, and user-level hooks. A separate memory-management session owns them. This programme only notifies it when paths it indexes are removed. The memory index (~16 KB) is real session-start load that this programme cannot reduce; it is reported here, not counted.
- **PR #947** (data-movement rules). It is an input. P0.2 waits for it, and every AGENTS/operational_rules leg keeps its Data-movement paragraph's rules intact. Those legs start only after it merges.
- **Operator account acts (listed, never done by agents):** (1) one `sync_skills.py` release from the primary checkout (Rule 38), preserving user-only `rule-0` (`sync_skills.py:105`); (2) pruning the claude.ai bundle (retired `fxify-challenge`, `live-execution-journal`, `inqhiori-algorithm`, `databento-data`; duplicate `anthropic-skills:*`); (3) optionally requesting promotion of the per-clone safety hookify rules (`locked-pine`, `locked-sizing-const`, `destructive-git`, `no-verify-commit`), absent from cloud sessions today; (4) `.claude/settings.local.json` cleanup; (5) merged `claude/step*`/`d9-*` branch deletion via repo-hygiene; (6) the 11-08 checks, owned by their owners.
- **Not done at all:** renaming `docs/superpowers/` or `docs/spec/` (D14); moving code-pinned paths (§6); edits to Pine, ports, `effective_inputs.json`, SHA256SUMS, frozen preregs, lock artifacts or constants; research trials.

## 2. Operator decisions (recommendation first)

| # | Decision | Recommendation | Unblocks |
|---|---|---|---|
| **D1** (first) | How to absorb #855 (CONFLICTING, head `5c44f05`, base 191 commits behind, 123 of 228 paths changed on main) and #935 (CONFLICTING, head `a9f76ab`, 72 rows) | **Close both. Re-derive against current main, reusing their dispositions. Do not rebase.** Rebasing burns review rounds on conflict resolution (Rule 6 limit), and the folds rewrite the same text anyway. <br>**#855:** its 46 removals plus TOMBSTONES text become card C-ADR (P0.8), re-verified per row. Its `load_tombstoned_names` fix and regression test are ported as P0.5. Its 21 trims are dropped: the P1.8, G4 and G5 current-text folds supersede them. <br>**#935:** rows on non-governance files (skills except strategy-validation, the 6 methodology files, `scripts/README.md`, `docs/spec/README.md`) are re-applied by P1.7, from #935's head text where the source still matches. Rows on AGENTS, operational_rules and ADRs feed the G-legs' meaning-preservation tables. <br>Mark plan step 6 "absorbed by this programme" in the P3.6 close-out. | P0.5, P0.8, P1.3, P1.7; most of §6 |
| **D2** | Explicit request to rewrite standing instructions (AGENTS §Continuous improvement item 6; Rule 36) | **Grant**, scoped as a meaning-preserving rewrite to the §0 budgets of AGENTS.md, STATE.md, docs/operational_rules.md, PIPELINES.md, REPO_MAP.md (non-generated part), `scripts/seat_authority.yml` comments and `.claude/skills/**`. | G1–G3, P1.7, P2.1 |
| **D3** | Retrieval record | **ADRs:** `docs/adr/TOMBSTONES.md` rows (mandatory, `2026-08-08-adr-ceremony-tiering.md:58`; read by `check_adr_graph`). <br>**Other docs:** one **"Removal batches"** table in `docs/ltm/README.md`, one row per merged removal PR: merge SHA, pre-removal parent SHA, path count, retrieval command `git show <parent>:<path>`, and the path list via `git diff --name-only --diff-filter=D <parent> <merge>`. <br>Rejected: `lab/ARCHIVED.json` (study-keyed, parsed by `archive_lab_analysis.py:641-651`; needs schema v2); a per-path JSONL plus checker (duplicates git, Rule 36); a new RETRIEVAL.md (second owner, Rule 29; `docs/ltm/README.md` already owns retrieval and the 09-06 precedent). | P1.3–P1.6, P3.5 |
| **D4** | Add three guards (new layers, Rules 36/38) | **Yes**, each fail-closed on *new* misses with a shrink-only baseline: <br>(a) `check_md_anchors.py`: path + fragment links, GitHub slugs plus explicit `<a id>`; <br>(b) `check_doc_budgets.py` reading `scripts/doc_budgets.yml`: per-file and T0 byte caps, LF-normalised, starting at current sizes and lowered by each content PR; <br>(c) a `docs-readers` job in `.github/workflows/tests.yml`, run on `**/*.md` and `.claude/**` paths, running the ~15 test files that read real docs. It ends the docs-only-PR pytest gap (`tests.yml:9-17`). <br>**Not adopted:** the guard-first G4 state-currency extension (false-failure risk; the backfill in G3 fixes the symptom) and its G8 retirement-record checker (git already indexes deletions). | P0.4, P1.1, P1.2, every later leg |
| **D5** | Rule links and the AGENTS budget | **Add `<a id="rule-N"></a>`** on each Core-rule heading in operational_rules. Keep the 42 full-slug anchors resolvable for other inbound links. AGENTS links `docs/operational_rules.md#rule-N`, saving about 1.6 KB. <br>**Hard cap 8,192 B.** If #947's paragraph plus the binding contents cannot fit, G2 discloses it and caps at 9,216 B. Rule links are never dropped to make the budget. | G1, G2 |
| **D6** | operational_rules Edit log (`:979` duty; log ≈8.7 KB) | **Replace the duty** with "each rule-edit PR states what changed and why; git holds the log". Delete the log with a blob pin. This is a rule-text change, so it is ratified with G1. | G1 |
| **D7** | SESSIONS | **Roll to 30 now** (`roll_sessions.py --keep 30`; one command, no tooling change). Retiring the surface (three gates, githooks, Rule 34, 149 inbound files) is a later, separate ruling. Separately: the operator says whether the stop hook `.claude/hookify.session-log.local.md` stays; nothing has been written since 10-09. | P1.9 |
| **D8** | S5 Part-A dump (`docs/notes/2026-09-27-s5-part-a-measurement/`, 224 files, ~2.3 MB) | **Keep in place for now.** It has live readers: workflow `qualification-s5-part-a-measurement.yml:95`, `tests/test_s5_part_a_measurement_harness.py:32` and pin `docs/evidence/PRIVATE_EVIDENCE.sha256:318`. It is not orientation load. P0.8 records whether the S5 qualification is closed [U]. If it is, a later leg may delete directory, workflow and test together under a separate GO. | — |
| **D9** | Ratification shape | **One batch GO per ADR-fold or ADR-removal PR**, covering its disposition table. **Separate GOs** for surface allocation (G4) and M1 (G5). Each ruling-class PR still gets direct operator confirmation before merge (merge-train `SKILL.md:21`). | P1.3, P1.8, G1, G2, G4, G5, P3.4 |
| **D10** | `2026-09-17-bounded-platform-protection-incident-contract` (121 KB, Proposed; decides nothing under Rule 32) | **Withdraw, with a TOMBSTONES row**, in P1.3. | P1.3 |
| **D11** | Post-11-08 owner dispositions | Rule after the 11-08 checks are recorded: <br>• no-counterparty channel: retired → tombstone and migrate the quarterly check; live → fold; <br>• decompound limb-2 (STATE:112): close → tombstone; <br>• databento ADR: **fold, do not tombstone**, because AGENTS/STATE cite its retirement addendum as owner; <br>• ORB-MNQ unpark: tombstone if discharged [U]. | P3.4 |
| **D12** | Mechanical STATE rolls beside the one open governance PR | **Allow**, when the roll PR touches only STATE and its archive pair and the open lane PR does not touch STATE. Push-collision is per file (`check_push_collision.py:88-93`). Covers 10-30, 11-06, 11-08 discharge, 11-13 and 11-20. | P0.1, P1.10, weekly rolls |
| **D13** | `scripts/retire_adr.py` (implements the obsolete hot-stub/cold-body flow, `:4-7`) | **Delete it and its tests.** Policy is TOMBSTONES-only (`ceremony-tiering.md:58-62`). | P2.3 |
| **D14** | Rename or merge `docs/superpowers/` and `docs/spec/` | **No.** It would re-arm `check_lifecycle_consistency.py:64-68`, rescope `check_spec_provenance`, and touch 36 code/skill readers and 5 open PRs. Dead content is deleted in place instead. | — |

**Operator time estimate.** About 1 h for D1–D14 in one sitting. Then about 2.5 h of GOs: P1.3, P1.8, G1, G2, G4, G5, P3.4 at roughly 20 min each with the disposition table. Then 11-08 owner work, which is outside this programme.

## 3. Phases and legs

### 3.1 Orientation definition (written into AGENTS §Purpose by G2; enforced by `doc_budgets.yml`)

| Tier | Contents | Budget |
|---|---|---|
| **T0: read in full at every session start** | AGENTS.md (auto-loaded), STATE.md, SessionStart hook output | 8,192 + 5,120 + 1,024 = **14,336 B**, gated |
| **T1: first routed read, exactly one** | The owner section that the active STATE queue row links, **or** PIPELINES.md (≤4 KB), **or** the non-generated part of REPO_MAP.md | ≤11,264 B. Guidance, not gated |
| **Reference: never orientation** | operational_rules full statements, ADRs, skills (load by trigger), SESSIONS, load_bearing_numbers, rejected_candidates, plans | none |

Total: **≤25,600 B.**

### 3.2 Lanes

| Lane | Contents | Concurrency |
|---|---|---|
| **GOV** | Any PR touching AGENTS, STATE, `docs/SESSIONS.md`, `docs/operational_rules.md` or `docs/adr/**` | Serial: one open at a time. STATE-only rolls run beside it under D12 |
| **N-a, N-b, N-c** | Disjoint non-governance PRs | At most 3 open at once |
| **off-lane** | Claude card or disposition drafting, no PR | Drafted while lane PRs are in review |

Generated files change only through their tool, in the PR that changes their inputs:

- `docs/adr/INDEX.md` via `check_adr_graph.py --regenerate-index`;
- `docs/methodology/LESSONS_INDEX.jsonl` via `_build_lessons_index.py`;
- `docs/notes/audits/docs-runtime-inventory.md` via `check_docs_runtime_inventory.py --write`.

### 3.3 Phase table

**Phase 0 (10-28 → 10-31): unblock and build guards.**
- *Entry:* this spec delivered.
- *Exit:* P0.1 merged by 10-30 23:59 ET; #947 merged; D1–D14 ruled; P0.4–P0.7 merged; cards C-ADR, C-DEL and C-935 frozen; B₀ recorded.

**Phase 1 (10-31 → 11-09): bulk subtraction and first folds.**
- *Entry:* Phase 0 exit; #944 merged or closed (it releases `gates.yml`); #936 confirmed limited to `strategy-validation`.
- *Exit:* P1.1–P1.10 merged; anchor baseline ≤ B₀; docs files ≤900.

**Phase 2 (11-04 → 11-18): rule and root rewrites.**
- *Entry:* #947 merged; P1.8 merged; D2, D5 and D6 ruled.
- *Exit:* operational_rules ≤45 KB; AGENTS ≤8 KB (or the D5 fallback); PIPELINES ≤4 KB; STATE ≤5 KB.

**Phase 3 (11-10 → ~11-25): constitution, safety owner, post-11-08 dispositions, close-out.**
- *Entry:* 11-08 checks recorded by their owners.
- *Exit:* every §0 target met or explicitly cut by the operator.

| Id | Goal | Impl → Rev | Group | Depends on | Files allowed | Files forbidden |
|---|---|---|---|---|---|---|
| **P0.1** | STATE weekly roll (deadline 10-30). `state_roll.py` rolls only once the deadline has passed (`roll_weekly`: `old_deadline >= today` returns unchanged). Prepare it on 10-30 with `--today 2026-10-31`, after the week's preservation-trade coverage is recorded, and merge it before 10-31 00:00 ET | Claude → Codex | GOV, beside under D12 | — | `STATE.md`, `docs/ltm/notes/archive/state/**` | everything else |
| **P0.2** | Land #947 | its owner, merge-train | GOV | — | #947's 5 files | — |
| **P0.3** | Operator rulings. After D1, close #855 and #935 with a link to this spec; keep their branches | operator; Claude comments | — | — | — | — |
| **P0.4** | Anchor and path ratchet checker | Codex → Claude | N-a | — | `scripts/check_md_anchors.py` (new), `scripts/md_anchor_baseline.txt` (new), `tests/scripts/test_check_md_anchors.py` (new) | `scripts/gates.yml` (frozen), all `.md` |
| **P0.5** | Port the #855 `load_tombstoned_names` fix | Codex → Claude | N-b | D1 | `scripts/check_adr_graph.py`, `tests/test_check_adr_graph.py` | `docs/**` |
| **P0.6** | Fix `session_divergence_hook.py` (stdin `cwd`, `git -C`, print checkout and branch). Delete the dead `SKEW-headroom-fixed1r` scan and its fixture. Fix the `post-merge:48` wording | Codex → Claude | N-b, after P0.5 | — | `scripts/session_divergence_hook.py`, `tests/scripts/test_session_divergence_hook.py` (new), `ops/sentinel/scan.py`, `tests/governance/test_sentinel.py`, `scripts/githooks/post-merge` | `.claude/settings.json`; `GOVERNANCE_PREFIXES` values |
| **P0.7** | Regenerate the docs-runtime inventory (stale since 09-20) | Codex → Claude | N-c | — | `docs/notes/audits/docs-runtime-inventory.md` | all else |
| **P0.8** | Cards: **C-ADR** (re-derived #855 removal table plus the D10 row), **C-DEL** (retention manifest for `docs/**` outside `docs/adr`), **C-935** (salvage rows) | Claude; Ultracode fan-out allowed | off-lane | D1, P0.7 | scratchpad only. Cards travel in the dispatch prompt and the PR body; committed handoffs are superseded (surface-allocation ADR `:913`) | committing card files |
| **P1.1** | Wire P0.4 into `gates.yml` (`always` tier, baseline mode). Add `check_doc_budgets.py` and `scripts/doc_budgets.yml` at current sizes | Codex → Claude | N-a | P0.4, D4, #944 settled | `scripts/gates.yml`, `scripts/check_doc_budgets.py`, `scripts/doc_budgets.yml`, `tests/scripts/test_check_doc_budgets.py`, `scripts/README.md` gate rows | governance files |
| **P1.2** | Add the `docs-readers` CI job | Codex → Claude | N-c | D4 | `.github/workflows/tests.yml`, `tests/README.md` | other workflows |
| **P1.3** | ADR removals per C-ADR (plus the D10 withdrawal): TOMBSTONES rows, inbound repoints and pins, INDEX regenerated | Codex → Codex ([ports of Claude-written content](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review)) | GOV | P0.4, P0.5, P0.8, D1, D3, D9 GO | card-listed `docs/adr/*.md`, `docs/adr/TOMBSTONES.md`, `docs/adr/INDEX.md` (tool), card-listed inbound-link lines in non-governance files | AGENTS, STATE, operational_rules, the 11-08 owners, surface allocation, M1, Track B-linked targets |
| **P1.4** | Delete docs batch A: `docs/notes/**` rows of C-DEL, plus one D3 row | Codex → Claude | N-b | P0.8 | card paths, `docs/ltm/README.md` (one row), inbound-link lines in non-governance, non-§6 files, repointed to `blob/<parent>` (Joshua, 2026-10-29) | `docs/notes/{rail_build,notice,audits,sentinel}/**`, S5 dump, open-PR paths (§6), `docs/evidence/**` |
| **P1.5** | Delete docs batch B: pre-09-20 executed `briefs/handoffs` and the 7 orphan DRAFTs, `briefs/phase{3,4}-preparation/**`, done `superpowers/plans`, `notes/2026-09-24-t10-step4/`, plus one D3 row | Codex → Claude | N-c | P0.8, D1 | card paths, `docs/ltm/README.md`, `scripts/handoff_brief_form_grandfathered.txt` (shrink only), inbound-link lines in non-governance, non-§6 files, repointed to `blob/<parent>` (Joshua, 2026-10-29) | moving or renaming any handoff; §6 paths |
| **P1.6** | Merge `docs/lessons/*` into `docs/methodology/lessons/`. Delete `docs/skill-drafts/` (after confirming `superpowers:related-case-review` covers it [U]), `docs/external/` and `docs/methodology/archive/notion/` | Codex → Claude | N-a, after P1.1 | P0.7, D3 | those paths, `scripts/_build_lessons_index.py`, `LESSONS_INDEX.jsonl` (tool), `methodology_lessons.md:433` link, inbound links, `docs/ltm/README.md` | governance files |
| **P1.7** | Re-apply C-935 non-governance rows. Plan §6 repairs 1–7, 9, 10, 12, 15, 21 where still unrepaired at head [U]. Link (do not restate) Rule 6 in the `seat_authority.yml` `pr.merge` comment and merge-train `SKILL.md:13` | Codex → Codex ([ports of Claude-written content](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-26--operator-ruling-cross-agent-review)) | N-b | D1, D2, #936 settled | `.claude/skills/**` (excluding strategy-validation), the 6 #935 methodology files, `scripts/README.md`, `docs/spec/README.md`, `scripts/seat_authority.yml` (comments only), `scripts/gates.yml` (repair #10 trigger only, after P1.1) | AGENTS, STATE, operational_rules, `docs/adr/**` |
| **P1.8** | ADR fold batch A: rule-2 (06-16), tradeify-descope (08-04), s2b daemon (08-08), c1 GO (07-17) | Claude → Codex (Rule 5 adjudication) | GOV | P1.3, D9 GO | those 4 ADRs, `docs/adr/INDEX.md` (tool) | evidence addendum bodies (kept verbatim under `## Evidence (frozen)` or moved out with a pin) |
| **P1.9** | SESSIONS roll to 30. First extend `check_advisor_dedup.load_corpus` (`scripts/check_advisor_dedup.py:177-185` reads only `docs/SESSIONS.md`) to also read `docs/ltm/notes/archive/sessions/*.md`, so rolled entries stay searchable | Codex → Claude | GOV | D7, P1.8 | `docs/SESSIONS.md`, `docs/ltm/notes/archive/sessions/**`, `scripts/check_advisor_dedup.py`, its test, `scripts/doc_budgets.yml` (own caps only) | hand edits to entries |
| **P1.10** | Weekly roll 11-06. **11-08 discharge:** mark `### 2026-11-08` DISCHARGED once the owners record their checks; merge on 11-08 ET | Claude → Codex | GOV, beside under D12 | owners' 11-08 records | `STATE.md`, archive pair | owner files (the owners write those) |
| **G1** | operational_rules to ≤45 KB: `rule-N` aliases (D5); legacy §1–§5 folded into Core rules, with Origin incidents as legacy-map rows pinned to blob; Edit log per D6; `docs/rule_0.md` merged into Rule 0 with 26 inbound files and 6 skills repointed; #935 operational_rules rows; #947 Rule 13 text verbatim | Claude → Codex | GOV | #947, P1.9, D2, D5, D6, D9 GO | `docs/operational_rules.md`, `docs/rule_0.md` (deleted), inbound-link lines, citing skills, `scripts/doc_budgets.yml` (own caps only) | the `## 7. One canonical owner` heading (`find_owner.py:61`), `\n## 9. ` (`test_private_pine_read_in_place.py:59-62`), the `#16-retention…` anchor, the 42 full-slug anchors |
| **G2** | AGENTS to ≤8 KB, PIPELINES to ≤4 KB. Content is listed in §4 | Claude → Codex | GOV | G1, D2, D9 GO | `AGENTS.md`, `PIPELINES.md`, receiving owners for moved sentences (non-governance only), `scripts/doc_budgets.yml` (own caps only) | §6 AGENTS literals and headings |
| **G3** | STATE to ≤5 KB. One-line index rows (`- **YYYY-MM-DD** — consequence + owner link`, ≤110 B). Backfill the 10-19→10-28 decisions from their owner records [U owners; the memory index is not a source]. Delete queue item 1 (Track B), the 10 strikethroughs and the discharged 11-08 section. Add `<a id="operator-queue"></a>` (38 links). Includes the 11-13 roll | Claude → Codex | GOV | P1.10, G2 | `STATE.md`, archive pair, `scripts/doc_budgets.yml` (own caps only) | heading formats in §6 |
| **P2.1** | Skill trims: `prop-firm-challenge` to ≤12 KB (drop FXIFY/CFD/DXTrade tables, link `core/historical_challenge.py`); `trade-csv-reconcile` (drop DXTrade/OANDA sub-rules, keep one "label ≠ data" paragraph); `task-routing` description for Claude/Codex/cloud | Codex → Claude | N-c | P1.7 | those 3 skills | `strategy-validation` |
| **P2.2** | Judgment skill trims: `code-defect-debugging`, `work-decomposition` (decision rules kept); merge `refine-question` into `inqhiori`, keeping its trigger phrases | Claude → Codex | N-a | P2.1 | those skills | — |
| **P2.3** | Delete `scripts/retire_adr.py` and its tests (D13) | Codex → Claude | N-b | D13 | the script, its tests, `scripts/README.md` row | — |
| **G4** | Surface-allocation current-text fold | Claude → Codex | GOV | G3; 7 quiet days with no new addendum; own GO | that ADR, INDEX (tool), `seat_authority.yml` header link | the bytes inside `<a id="addendum-2026-09-27">` and its Exempt table; `<a id="addendum-2026-09-30b">` |
| **G5** | M1: "Current gate" section first; superseded text deleted; the 07-31b inverted hooks pinned to blob. Full fold deferred | Claude → Codex | GOV | G4 or G3; own GO | `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`, INDEX | `docs/notes/rail_build/**`, the validator |
| **P3.4** | Post-11-08 dispositions per D11, then folds of ADR rows 9–21 as budget allows (≤1 PR) | Claude → Codex; Codex for tombstone mechanics | GOV | G5, D11 GO | listed ADRs, TOMBSTONES, INDEX, citing STATE lines | — |
| **P3.5** | Deferred deletions: files held in P0.8 only because governance files linked them, plus the 927 KB rule-consolidation plan, with a D3 row | Codex → Claude | N-a | G1–G3 | card paths, `docs/ltm/README.md`, inbound-link lines in non-governance, non-§6 files, repointed to `blob/<parent>` (Joshua, 2026-10-29) | §6 |
| **P3.6** | Close-out: baselines to zero on living files; `doc_budgets.yml` to the §0 targets; regenerate inventory; final measurement table in the PR body | Claude → Codex | GOV (last) | all | `scripts/md_anchor_baseline.txt`, `scripts/doc_budgets.yml`, inventory | — |

Count: 5 Phase-0 PRs (P0.1, P0.4–P0.7), 10 Phase-1, 6 Phase-2, 5 Phase-3. That is 26 PRs: 12 GOV and 14 non-GOV. Codex implements 15 of them (P0.4–P0.7, P1.1–P1.7, P1.9, P2.1, P2.3, P3.5).

## 4. Cards and leg notes

### 4.1 Standard Codex card frame (every Codex leg)

**Dispatch:** `scripts/dispatch_codex.ps1 -Worktree <C:\Users\joshu\multi_firm_operations\.claude\worktrees\cleanup-<leg>> -OutputFile <scratchpad>\<leg>.txt -Prompt <card>`. Run it from a fresh `.env`-free worktree cut from origin/main (the script refuses `.env`, `:28`).

**Authority block:** `pr.open` on a `codex/` branch; no merge; no governance.author outside the allowed list; no operator acts.

**Data rule (PR #947):** the card never carries, and Codex never reads, any of the following:
- Pine, ports or `effective_inputs.json`;
- account data;
- `first-passage-archive`;
- the primary checkout.

Deletion manifests carry paths only. The private read surface is untracked here, so it cannot appear in them.

**Return:** `git diff --stat origin/main...HEAD`, every acceptance command with its exit code, and the `record.json` paths.

**Out of scope (every card):** edits outside the allowed list; moves or renames (deletion only, unless the card says move); hand-editing generated files; `--no-verify`; force-push; `git stash`.

### 4.2 Codex leg stubs

| Leg | Goal | Allowed | Acceptance (in addition to §7.1) | Out of scope |
|---|---|---|---|---|
| P0.4 | Resolve `file.md#frag` and relative paths over tracked `**/*.md`, including `.claude/skills/**`. Slugs follow the GitHub algorithm (em-dash and `--`, duplicate `-1` suffix) plus `<a id>` and `<a name>`. Skip `blob/<sha>` and absolute URLs. Baseline identity is `src -> target [reason]` with an occurrence count; line numbers are for display only, so text inserted or removed above an unchanged broken link never fails the gate. `--baseline`: exit 1 if any identity's current count exceeds its baseline count, pass otherwise; `--update-baseline` only lowers counts or drops identities. Reuse `scripts/link_policy.markdown_links` | 3 new files | `.\fp.ps1 python -m pytest tests/scripts/test_check_md_anchors.py` covers slug, explicit id, duplicate heading, growth fails, shrink passes, and moving an unchanged broken link to another line passes. `.\fp.ps1 python scripts/check_md_anchors.py --baseline scripts/md_anchor_baseline.txt` exits 0. The PR body states B₀ and the `STATE.md#operator-queue` verdict | `gates.yml`; fixing any link |
| P0.5 | Cherry-pick the `load_tombstoned_names` hunk and its test from `5c44f05` | 2 files | `.\fp.ps1 python -m pytest tests/test_check_adr_graph.py`; `.\fp.ps1 python scripts/check_adr_graph.py` on head. Any new A2 finding is listed in the PR body and becomes a P1.3 card item [U: none expected] | fixing A2 findings |
| P0.6 | See the phase table | listed | `.\fp.ps1 python -m pytest tests/scripts/test_session_divergence_hook.py tests/test_governance_class.py tests/governance/test_sentinel.py` | `settings.json` |
| P0.7 | Regenerate the inventory | 1 file | `.\fp.ps1 python scripts/check_docs_runtime_inventory.py --write`, then `--check` exits 0 | — |
| P1.1 | Wire the gates; add the budget checker at current sizes, plus a `t0` cap = sum of AGENTS + STATE + 1,024 | listed | `.\fp.ps1 python -m pytest tests/scripts/test_check_doc_budgets.py tests/scripts/test_check_md_anchors.py` (over cap fails; LF normalised; unknown path fails closed); `.\fp.ps1 check` record shows both gates ran | lowering any cap |
| P1.2 | `docs-readers` job on `**/*.md`, `.claude/**`, running the ~15 doc-reading test files (live-readers map §3, plus the tests named in §7.2) | 2 files | The job runs green on this PR; a follow-up commit touching only `.md` triggers it (shown in the PR) | making it a required check |
| P1.3 | Apply C-ADR: delete rows, add a TOMBSTONES section (path, blob at the pre-removal parent, disposition, owner), repoint live callers, pin history links to `blob/<parent>` | listed | §7.1 A-16, A-ret; `.\fp.ps1 python scripts/check_adr_graph.py --regenerate-index`, then `check_adr_graph.py` clean (A2, A5, A6); the anchor gate shows no new miss | trims; any unlisted ADR |
| P1.4 / P1.5 | Delete the card paths; add one D3 row | listed | A-16, A-ret; `.\fp.ps1 python -m pytest tests/scripts/test_check_handoff_brief_form.py` (P1.5); `check_adr_graph.py` (no A5 orphan; an orphan moves its citer to "defer") | moves |
| P1.6 | Move the 2 lesson files; rebuild the index; delete the 3 small folders | listed | `.\fp.ps1 python -m pytest tests/test_lessons_index.py tests/test_check_skill_refs.py`; `.\fp.ps1 python scripts/check_skill_refs.py --all` | lesson text edits |
| P1.7 | Apply C-935 hunks whose source text matches head; apply the §6 repairs listed | listed | `.\fp.ps1 python scripts/check_skill_refs.py --all`; `.\fp.ps1 python -m pytest tests/test_check_skills_no_constants.py tests/test_reconcile_skill_schema.py tests/test_sync_skills.py tests/test_check_lifecycle_consistency.py` | rows whose source changed (list them, skip them) |
| P1.9 | `.\fp.ps1 python scripts/roll_sessions.py --keep 30 --dry-run`, then the real run | listed | a regression test that `load_corpus` returns an entry present only in the archive; the sessions-order and sessions-append-only gates pass in `.\fp.ps1 check`; `check_advisor_dedup` finds a rolled-out entry after the roll | other corpus changes |
| P2.1 | Trims per the phase table | 3 skills | `.\fp.ps1 python -m pytest tests/test_check_skills_no_constants.py tests/test_reconcile_skill_schema.py tests/test_lifecycle_call1.py`; `check_skill_refs.py --all` | judgment rewrites |
| P2.3 | Delete the script and its tests | listed | `.\fp.ps1 test` | — |
| P3.5 | Same as P1.4 | listed | Same as P1.4 | — |

### 4.3 Claude leg notes

- **P0.8 C-DEL rules.** Classify each file by R1–R5 (`operational_rules.md` §16) using the regenerated inventory and the four §16 scans. The output is delete / keep / defer.
  - **Defer** any file linked from a governance file; it goes to P3.5.
  - **Keep** any file named in code: `screen_authority.py:80-90` DRAFTs, `docs/spec/2026-09-14-tb-*`, `docs/notes/rail_build/**`, `docs/evidence/**`, `docs/briefs/{closures,pre-registration,rnd-pipeline,INDEX.md}`, `docs/notes/{notice,audits,sentinel}`, and `notes/2026-09-29-s5-c3-record` (live closure tool).
  - Any file in an open PR or on the §6 list is excluded.
  - The coordinator re-reads 10% of delete rows.
  - Batches are ≤60 paths, to protect the 3-review cap.
- **P0.8 C-ADR rules.** Drop a #855 removal row if any of these hold:
  - the ADR changed on main since `4121e84c` and gained obligations;
  - it is an 11-08 owner;
  - Track B links it (s2b W6, C2 relock, concept-not-constant);
  - #855 itself held it (§5.2).

  Add the five Cold ADRs (avenue-a, implied-sr gate, msl disclosure, msl channel, cc-cursor autonomous loop) after an inbound scan, plus D10. Every row carries a blob at head and an owner that exists at head.
- **Fold recipe (P1.8, G4, G5, P3.4;** `ceremony-tiering.md:43-56`**).** Read body and all addenda. Write a per-obligation disposition table (retained / discharged / superseded / retired, new owner) in the PR body. Add `**Revision:** 2026-11-DD — current-text fold; prior at blob <sha>` and a `## Decision / current rule` section. Delete superseded addenda. Keep evidence verbatim under `## Evidence (frozen)` or move it out with a pin. Add an explicit `<a id>` for every inbound-cited anchor (the gate proves it). Convert self-matching §10 hooks to `git show <blob>:…`, never re-counted. Regenerate INDEX by tool. Ultracode: one subagent per ADR; no adversarial or refute passes.
- **G1 and G2 meaning-preservation table.** Every removed sentence maps to its new owner line, or is marked "restated at <link>". Codex adjudicates premises (Rule 5), not just the diff.
- **G2 AGENTS content:**
  - **Keeps:**
    - §Purpose, with the T0/T1 sentence;
    - the rule index as 42 one-line gists (Rules 0–41), each linking `docs/operational_rules.md#rule-N`;
    - the posture core (≤1 KB): the M1 arm gate, per-session GO, disarm before `armed_until`, `order_id` DISPROVEN, the agent-order clause and the standing weekly GO link `#addendum-2026-09-30b`;
    - `## Strategy Reference (LOCKED legacy book — do not modify)`, heading exact, with the MC line verbatim and first in the file;
    - `## Protection`, with its constants, gate chain and LOST warning;
    - `## Public-clone posture`, with #947's Data-movement rules intact;
    - `### Gate composition authority`, with "Merges and credentials" folded into the Rule 6 line plus a link;
    - `## Live-execution posture` as a heading (11 inbound links).
  - **Moves out:**
    - the Standing-consequence table, to its owners (not to STATE);
    - Continuous improvement, to the `agent-improvement` skill;
    - Config-as-code, to Rule 39;
    - Python environment, as a 2-line link to `scripts/README.md#local-operations-launcher`.
  - **Dates:** every ISO date leaving AGENTS must exist in its owner, because sentinel `obligation_scan` reads AGENTS dates [U: `_OBLIGATION_FILES`].
  - **PIPELINES:** delete the P2/P3/P6 tombstones and history.
- **G3.** Rows reworded outside a roll are fine. I1 is checked only within a `state_roll.py` run against its pre-state (`state_roll.py:23-27,998-1014`). Run `--check` before and after anyway.

## 5. Dependency graph and critical path

```
P0.1(10-30) ─┐   P0.4 ─► P1.1 ─► P1.6        P0.5 ─► P0.6     P0.7 ─► P0.8 ─► P1.4, P1.5
#947 ────────┼─────────────────────────────────────────────────────────────────┐
D1..D14 ─────┴► P1.3(GOV) ─► P1.8 ─► P1.9 ─► G1 ─► G2 ─► G3 ─► G4 ─► G5 ─► P3.4 ─► P3.6
                                         P1.10(11-08, beside) ─────┘ (G3 needs it)
D1 + #936 ─► P1.7 ─► P2.1 ─► P2.2        D13 ─► P2.3        G1..G3 ─► P3.5 ─► P3.6
```

**Calendar.** Each GOV PR is planned at about 2 days: author pre-drafted off-lane; Codex review plus one fix; CI 22–32 min; operator GO.

| Date | GOV lane | Beside (D12) | Non-GOV |
|---|---|---|---|
| 10-28 → 10-30 | #947 | P0.1 roll (hard 10-30) | P0.4, P0.5→P0.6, P0.7; P0.8 drafting |
| 10-31 → 11-03 | P1.3 | — | P1.1, P1.2, P1.4 |
| 11-04 → 11-05 | P1.8 | — | P1.5, P1.6, P1.7 |
| 11-06 | P1.9 | weekly roll | P2.1 |
| 11-07 → 11-08 | G1 (in review) | **P1.10 discharge, 11-08 ET (hard)** | P2.2, P2.3 |
| 11-10 → 11-11 | G1 merge → G2 | — | — |
| 11-12 → 11-14 | G2 merge → G3 (includes the 11-13 roll) | — | — |
| 11-17 → 11-19 | G4, if 7 quiet days | — | P3.5 |
| 11-20 → 11-21 | G5 | weekly roll 11-20 | — |
| 11-24 → 11-25 | P3.4 → P3.6 | — | — |

- **Critical path:** #947 → P1.3 → P1.8 → P1.9 → G1 → G2 → G3 → G4 → G5 → P3.4 → P3.6, about **28 days**. Non-GOV legs have 7 or more days of float.
- **Biggest schedule risk:** operator GO latency. One day of delay moves the end date one day.
- **Slip rule:** if G4's quiet trigger has not fired by 11-21, G5 and P3.4 go ahead of it, and G4 leaves the programme exit. The end-state target for surface allocation is then reported as cut.

## 6. Freeze list and release triggers

| Frozen path or literal | Rule | Released by |
|---|---|---|
| AGENTS: the MC triple `99.83% pass / 0.17% bust, p99 DD 4.37%` (first match; `ops/recall/guard.py:119-126` fails open) | Byte-identical, first in file | Never, unless `guard.py` and `tests/ops/test_recall_guard.py` change in the same PR |
| AGENTS headings `## Protection`, `## Strategy Reference (LOCKED legacy book — do not modify)`, `## Public-clone posture`, `### Gate composition authority` (`seat_authority.yml:80-90`); `## Live-execution posture` | Exact headings | Never |
| `operational_rules.md` `#rule-N--…` 42 slugs, `## 7. One canonical owner`, `\n## 9. `, `#16-retention…` | Keep, or change the reader in the same PR | Never in this programme |
| `scripts/check_root_doc_liveness.py:48` five-root list | Unchanged (D14, PIPELINES stays) | Never in this programme |
| STATE `**Last curated:**`, `## Scheduled forward triggers`, `### YYYY-MM-DD`, the Weekly/Monthly heading forms, the `OPERATOR QUEUE` prefix | Edited only through state_roll conventions | Never reformatted |
| Surface-allocation `<a id="addendum-2026-09-27">` plus its Exempt table (`check_handoff_brief_form.py:63-65`); `<a id="addendum-2026-09-30b">` | Byte-identical | Never |
| Surface-allocation ADR (all other text) | No edits by the programme | G4 entry: 7 quiet days, after 10-30, own GO |
| `docs/adr/**`, `docs/pursuits/**`, `ops/instruments/**`, TOMBSTONES / AGENTS, operational_rules, `dispatch_codex.ps1` / `gates.yml`, `REPO_MAP.md`, `check_pine_manifest.py` / `strategy-validation` skill | No edits | D1 closes #855 / #947 merged / #944 settled / #936 settled |
| The eleven 11-08 owner files (inflight.md §3) and STATE's `### 2026-11-08` body | Byte-identical | 11-08 checks recorded, then P1.10 / P3.4 |
| `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` (§58–§60) | Never moved | Never |
| `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` | No edits | #845 closed, with AGENTS anchors repointed in the same PR |
| `docs/superpowers/specs/2026-10-28-orb-aegis-*`, `plans/2026-10-1{2,8}-*`, `plans/2026-10-21-*` | No edits | Aegis signer R3 closed; #946, #886, #888, #807 settled |
| `discovery_manifests/**`, `lab/CATALOG.md`, `lab/analysis/orb/orprem_mnq_2026-10/**`, `lab/analysis/_inbox/prop_payout_geometry_2026-10/**` | No edits | #937, #945, #875 settled (K ledger) |
| `docs/notes/2026-10-1*`, `2026-10-2*`, `docs/notes/research/2026-10-2*`, `docs/briefs/pre-registration/*-DRAFT*.md` | No edits | Their PRs settle (#882, #869, #867, #843, #841, #790, #791, #889, #941, #875) |
| `docs/notes/rail_build/**`, M1 JSON, `docs/evidence/**`, `docs/spec/2026-09-14-tb-*`, code-named DRAFTs, S5 dump (D8), `notes/2026-09-29-s5-c3-record/`, SHA256SUMS, `*.sha256`, Pine, ports, constants | Never moved or edited | Never |
| `docs/superpowers/plans/2026-10-25-rule-consolidation-step-1.md` (927 KB) | No edits | D1, then deleted in P3.5 |

## 7. Verification

### 7.1 Standard set (every leg cites the IDs it ran)

| Id | Check |
|---|---|
| A-doc | `.\fp.ps1 doctor` |
| A-chk | `.\fp.ps1 check`. Cite `record.json` with `status: completed`, exit 0, `source_stable: true` |
| A-test | `.\fp.ps1 test`, locally, until P1.2 lands. After P1.2, CI's `docs-readers` job covers docs-only PRs, and legs touching code still run `fp test`. A qualification-child 3,600 s timeout uses the standing CI substitution and is disclosed |
| A-anc | `.\fp.ps1 python scripts/check_md_anchors.py --baseline scripts/md_anchor_baseline.txt`: no new miss, and the baseline line count is ≤ its previous value |
| A-bud | `.\fp.ps1 python scripts/check_doc_budgets.py` (after P1.1). A content leg lowers its own caps in the same diff; `scripts/doc_budgets.yml` (own caps only) is in every content leg's allowed files |
| A-16 | The four §16 scans, pasted in the PR body for each deleted path: (1) `git grep -nF "<basename>"`; (2) `git grep -nE "<dir component>" -- "*.py" "*.yml" "*.ps1" "*.json" ".github/**"`; (3) A-anc plus a read of each glob reader in the inventory; (4) A-test |
| A-ret | A sample of 20 deleted paths per PR (all of them if ≤20): `git show <parent>:<path> > $null` succeeds. A TOMBSTONES row or D3 row exists |
| A-scope | `git diff --stat origin/main...HEAD` lists only allowed files |
| A-lit (any AGENTS-touching leg) | `git grep -c "99.83% pass / 0.17% bust" AGENTS.md` = 1; `git grep -c "p99 DD 4.37%" AGENTS.md` = 1; `.\fp.ps1 python -m pytest tests/ops/test_recall_guard.py tests/governance tests/test_check_lifecycle_consistency.py` |
| A-merge | Clean other-agent review at the head within 3 (or a clean 4th; ask the operator before a 4th Claude review of a Codex PR). Every check COMPLETED and green (gate on `status`, not `conclusion`). `.\fp.ps1 python scripts/merge_train.py gate <PR>` for Codex-reviewed PRs; a manual check for Claude reviews. Merge pinned to the literal 40-hex head. Ruling-class PRs need direct operator confirmation |

**Rollback (every leg):** a new PR with `git revert -m 1 <merge-sha>`. No force-push, no push to main, no stash. Deleted bodies are restored from `git show <parent>:<path>`; folded ADRs from their `Revision:` blob.

### 7.2 Extra checks per leg

| Leg | Checks |
|---|---|
| P0.1, P1.10, G3 | `.\fp.ps1 python scripts/state_roll.py --check` before and after; `.\fp.ps1 python scripts/check_state_currency.py` exits 0 (with `STATE_CURRENCY_TODAY=2026-10-31` for P0.1 and `2026-11-09` for P1.10); `.\fp.ps1 python -m pytest tests/test_state_roll.py tests/test_state_currency.py tests/test_sessions_queue_bind.py`; A-bud for G3 (≤5,120) |
| P1.8 | Per ADR: `.\fp.ps1 python scripts/check_brief.py --type adr <file>`; `.\fp.ps1 python scripts/check_rule2_trip_log_liveness.py`; `.\fp.ps1 python -m pytest tests/ops/test_c1_rail_arm.py tests/ops/test_c1_sizing_host_reference.py`; AGENTS anchors `#addendum-2026-09-01--f1-reversed…` and `#addendum-2026-08-24--test-strategy…` resolve (A-anc) |
| G1 | `.\fp.ps1 python -m pytest tests/test_find_owner.py tests/governance/test_private_pine_read_in_place.py tests/test_check_skill_refs.py tests/test_check_skill_refs_navdirs.py`; `.\fp.ps1 python scripts/check_skill_refs.py --all`; all 42 aliases `rule-0`…`rule-41` and all 42 slugs resolve (checked as an exact set); A-bud ≤45,056 |
| G2 | A-lit; A-bud AGENTS ≤8,192 and PIPELINES ≤4,096; `.\fp.ps1 python scripts/check_root_doc_liveness.py`; AGENTS links exactly the set `operational_rules.md#rule-0` … `#rule-41` (42 distinct, checked as a set); `rg "^\| Standing consequence" AGENTS.md` returns nothing; all four `seat_authority.yml` owner anchors resolve (A-anc) |
| G4 | `git diff` shows no change inside the `addendum-2026-09-27` block; `.\fp.ps1 python -m pytest tests/scripts/test_check_handoff_brief_form.py tests/test_claude_review_workflows.py`; `.\fp.ps1 python -m pytest tests -k "operator_acts or shell_command or handoff_authority or agent_handoff"`; 73 inbound links resolve |
| G5 | `.\fp.ps1 python -m pytest tests/test_validate_c1_monitoring_acceptance.py tests/ops/test_c1_rail_arm.py`, before and after with identical results; `git diff --stat` shows `docs/notes/rail_build/` untouched |
| P3.4 | P1.3 checks plus STATE forward-trigger citations repointed (`check_adr_graph.py` A7) |

### 7.3 Programme exit

- Every §0 row measured by its command and pasted in the P3.6 body.
- `.\fp.ps1 python scripts/check_md_anchors.py` with no baseline: 0 misses outside the frozen allowlist.
- `.\fp.ps1 check` and `.\fp.ps1 test` records completed with exit 0 at the final head.
- `gh pr list` shows no cleanup-shaped PR open.
- The memory-management session has been notified of removed paths.

## 8. Risks and unverified assumptions

### 8.1 Design comparison and contradictions resolved

| Criterion | Subtraction | Guard-first | Throughput |
|---|---|---|---|
| 25 KB | Yes, after 11-08 | 10 KB AGENTS interim | Yes, via aliases |
| Reader safety | Checker gated only at end | Strongest | Checker in Phase 0 |
| Operator / calendar | ~4 h / ~30 d | Most (15 D, 34 PRs) / longest | ~4 h / ~24 d, optimistic |
| Collision | Commits card files | 10 serial `gates.yml` merges | Low |

Chosen: subtraction tiers plus aliases; checker built in Phase 0 and gated before folds; cards in prompt/PR body; two `gates.yml` legs.

Contradictions and how each is resolved:

1. **#935: rebase vs re-derive.** Re-derive (D1). A rebase spends a GOV slot plus review rounds on text that G1 and G2 rewrite anyway.
2. **SESSIONS: retire vs roll.** Roll (D7). Retiring costs a ruling plus 3 gates; it does not touch orientation load.
3. **SESSIONS target (≤40 KB, 30 entries) is internally impossible.** 30 × 2.37 KB ≈ 71 KB, so the target is ≤76,800 B.
4. **`KEEP_ROWS` 15→8 is not needed.** 15 rows × ≤110 B ≈ 1.65 KB fits within 5 KB. The fallback, if G3 exceeds the cap, is a separate tooling PR, not a decision now.
5. **Retrieval home.** One owner, `docs/ltm/README.md`, rather than a new RETRIEVAL file or JSONL (Rule 29/36).
6. **Committed cards.** Not needed. The committed-handoff rule was superseded 10-24 (surface-allocation `:913`).
7. **The 11-09 red-main risk was missing from two designs.** Verified: `check_state_currency.problems` fails on any past `### YYYY-MM-DD` heading without DISCHARGED. P1.10 is therefore a hard leg.
8. **Atomic AGENTS + operational_rules PR vs split.** Split (G1 then G2), so moved content has a home before AGENTS drops it, and each PR stays within the review cap.

### 8.2 Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | 417 `#addendum` links break silently during folds | P0.4 before any fold; explicit `<a id>`; A-anc on every leg; gated in P1.1 |
| 2 | Docs-only PRs skip pytest | A-test until P1.2; then the `docs-readers` job |
| 3 | guard.py denylist empties silently | A-lit on every AGENTS leg |
| 4 | Obligation lost in a fold | Per-obligation disposition table; 11-08 freeze; Codex premise adjudication |
| 5 | A5 cascade when the only citer of an old Accepted ADR is deleted | `check_adr_graph.py` in every deletion leg; the citer moves to "defer" |
| 6 | 11-08 is a Saturday; the discharge depends on owners' records | Reserve P1.10 on 11-07/11-08. If owners have not recorded, the operator rules discharge-or-extend on 11-08. A heading extended with a new date is a hand edit the owner must justify |
| 7 | Surface-allocation churn (16 edits/week) | G4 quiet trigger; slip rule |
| 8 | AGENTS 8 KB unreachable with #947's rules intact | D5 disclosed fallback; links never dropped |
| 9 | GOV-lane PR hits 3 dirty reviews | Return it to its owner (Rules 6/7); the next GOV leg proceeds; the phase exit slips |
| 10 | Open-direction readers shrink (advisor-dedup, `repo_retrieve`, control-char scope) | Each leg names the reader it shrinks |
| 11 | Codex data class | Cards hold paths only; Claude screens C-DEL rows for account-class content first [U] |
| 12 | Stale user-level skills shadow repo trims; CRLF inflates bytes; concurrent sessions | Operator act 1; LF-normalised budgets; one worktree per leg, never stash |

### 8.3 Unverified assumptions

- B₀ (broken-link count).
- Whether GitHub resolves `STATE.md#operator-queue`.
- Owner records for the 10-19→10-28 decisions.
- Sentinel `_OBLIGATION_FILES` contents.
- Which plan §6 repairs are still open at head.
- Whether `superpowers:related-case-review` covers the skill draft.
- S5 qualification status.
- Live status of the no-counterparty channel and the ORB-MNQ unpark.
- Whether new A2 findings appear after P0.5.
- The docs file and byte end-state, which are estimates until the P0.8 manifest.
- The mergeability of the 22 feature PRs. Their paths are excluded, so they cannot collide.

## 9. Rule 2 budget line

`Rule 2: org cleanup programme — subtract to a ≤25 KB orientation load, meaning-preserving, every removal retrievable · OUTER 4 phases / ≤26 PRs (GOV ≤12, non-GOV ≤14) · INNER ≤3 reviews per PR (clean 4th only per Rule 6) and ≤2 failed corrections per leg, then the escalation lane (Rule 7) · ≤15 Codex implement dispatches plus ≤1 re-dispatch per leg, ≤40 Claude subagent runs · $0 new spend (CI + local; no VM, no vendor) · K = 0 · operator ≈4 h`. Stop structurally at any bound and report. A decision not listed in §2 returns to the operator; the programme does not widen to absorb it.
