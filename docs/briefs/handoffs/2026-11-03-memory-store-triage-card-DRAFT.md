# CC Handoff — Claude-project memory store triage

**Must run locally.** The memory store is the operator's Claude-project memory (`MEMORY.md` and its files) under `~/.claude/projects/<this project>/memory/` on his machine. A cloud container has no copy, and Remote Control cannot attach a hidden folder under the home directory. Some entries may also hold private-class content, which must be screened in place (Rule 13).

**Date:** 2026-11-03
**Parent session:** the 2026-11-08 sitting coordinator session (cloud); Joshua asked for this card on 2026-11-03.
**Spawn target:** Claude Code, `local`, on Joshua's machine, from the primary checkout.
**Repo:** `first-passage` (primary checkout), plus `first-passage-archive` for any private-class migration.
**Brief type:** CC handoff (multi-step, with one operator checkpoint).
**Parent question:** `N/A`. This card executes an operator direction, not a Pre-Q. Joshua, 2026-11-03: "write the memory triage card to run locally", after the coordinator found 69 `external-unmigrated` stubs in `docs/methodology/LESSONS_INDEX.jsonl` and proposed archive candidates.
**Authority:** Joshua (operator). Committing and pushing this card's own `claude/` branches and opening PRs needs no per-action go (operator ruling 2026-10-24). Merges follow Rule 6. **Moving, archiving or editing any memory file needs Joshua's approval of the triage table at the §2 checkpoint.** It is his store. A `DONE` status supplies no further permission.

**Why.** `docs/SESSIONS.md:7` says the memory store is "assistive-only, never attestation". Durable facts belong with their owners. The index still lists 69 memories by name only (`content_verified: false`), so cloud sessions see the names and cannot see the lessons. This triage closes that gap: keep what is still true, migrate durable lessons to an owner that every session can read, and archive what is retired.

---

## §0 — Rule 0 reads (Phase 0, before any §2 work)

Report each read with its anchor (`git log -1 --format='%h %ad' -- <path>` for repo files; file mtime and sha256 for memory files):

- `~/.claude/projects/<project>/memory/MEMORY.md` and **every** memory file it indexes, plus any unindexed file in that folder. Report the count, the names, and any file not in the index. Do not paste bodies into the PR or the return.
- `docs/methodology/LESSONS_INDEX.jsonl`, `docs/methodology/LESSONS_INDEX.md` (schema; the `status` vocabulary is at L41), `scripts/_build_lessons_index.py` (the generator; the index is generated, never hand-edited) and `tests/test_lessons_index.py`.
- `docs/methodology/lessons/methodology_lessons.md` §Format spec: the light format for any migrated lesson.
- `AGENTS.md` §Public-clone posture, data movement rules (Joshua, 2026-10-28), and Rules 13, 29, 30 and 31 in `docs/operational_rules.md`.
- `docs/ltm/README.md`: archive retrieval guidance, and how `first-passage-archive` takes additions.

## §0.75 — Local-only dependency check

- **Gitignored vendor data:** not touched. `N/A`.
- **Secrets:** none needed. Report and skip, without copying, any memory file that holds a credential (for example a `reference_*_credentials` entry); it is flagged for Joshua to revoke or delete.
- **Private read surface:** the memory folder is read in place. Its content follows the data-movement class rules. Content goes to a public commit only after the §2.3 screen, and never goes to Codex if it is private-class.

## §0.5 — Clarifying questions (halt on ambiguity)

Recommended defaults apply unless the Phase 0 read contradicts them. If it does, return `NEEDS_CONTEXT` and quote the conflict.

- **(A) The meaning of "archive".** **Recommended default:** move the file to `memory/_archive/2026-11/` and remove its line from `MEMORY.md`. Never delete, so it stays retrievable.
- **(B) The index status for archived stubs.** The schema has no such status (`LESSONS_INDEX.md:41`). **Recommended default:** add `retired` to the schema doc, the generator and the test's allowed set, with `status_note` naming the date, the reason and the repo evidence path. Do not overload `DORMANT`, which belongs to registry lessons.
- **(C) Where a durable lesson migrates.** **Recommended default:** a general, public-class lesson goes into `methodology_lessons.md` in the light format with its dated incident, and its index row becomes `migrated`. A project fact with an existing owner (ADR, instrument ledger, pursuit) goes to that owner, only if the owner lacks it. Private-class content goes to `first-passage-archive`.
- **(D) Memory files the repo never cites.** **Recommended default:** triage them the same way, but add no index row unless they migrate.

---

## §1 — Context

The coordinator could not read the store from the cloud. From names cited in the repo, it proposed these candidates. They are **hypotheses to verify against content**; do not act on a name alone (the `LESSONS_INDEX.md` stub rule).

- **Archive (subject retired; evidence in the repo):**
  - OANDA, Pepperstone and Dukascopy feeds: `reference_oanda_credentials`, `feedback_two_tier_canonical_pepperstone_oanda`, `feedback_oanda_dow_feed_artifact`, `feedback_per_strategy_pepperstone_baseline_uncommitted`, `reference_dukascopy_adapter`. Evidence: `AGENTS.md` §Strategy Reference ("OANDA and Pepperstone are retired") and `docs/adr/2026-06-24-oanda-retirement.md`.
  - Databento: `project_databento_research_stack`, `lesson_databento_ohlcv1d_weekend_bars`. Evidence: `docs/adr/2026-07-10-databento-research-stack.md`, addendum 2026-09-10.
  - CFD/FXIFY route: `project_copygram_migration_state`, `reference_copygram_option_semantics`, `project_ea_conversion_state`, `project_core_fxify_anchoring_audit`, `project_us_legal_master_research`. Evidence: `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`.
  - CrossTrade: `reference_crosstrade_tradovate_relink`. Evidence: `docs/pursuits/SUBSCRIPTION_LEDGER.md` (cancelled 10-31) and the c1 retirement addendum.
  - Lapsing or retiring at the 2026-11-08 sitting, so act only after those PRs merge: `project_aegis_6j_transfer_state` (b1), `project_pyramid_is_strategy_for_nas100` (b6), `project_decompound_remc_canonical_shift_2026_06_07` (decompound HOLD) and `project_4strategy_mc_anchor_2026_05_05` (legacy book; `AGENTS.md` keeps the historical literals).
  - Already closed: `project_btc_fifth_leg_lead` (`ops/instruments/BTCUSD.md:61`) and `project_ict_cascade_true_state_qict1_moot`.
- **Update, not archive:** `project_futures_prop_pivot` (superseded by the four-firm ADR addenda of 10-29 and 11-08), `project_rnd_pipeline_state` and `project_strategy_lifecycle_governance`.
- **Keep or migrate, never archive:**
  - Falsified-strategy memories such as `project_dj30_mym_prototype_falsified` and `project_q_nas_4_closure`. They remain Rule 26 advisory priors.
  - General `feedback_*` lessons.
  - `project_tv_egress_automation`: the TradingView login-automation bar still stands.

**Deliverables:**
1. A triage table for Joshua, kept local and private, at `local_artifacts/memory-triage-2026-11/TRIAGE.md`. One row per memory file: name | index id/status | data class (public / private / account / credential) | disposition (KEEP / UPDATE / MIGRATE-PUBLIC / MIGRATE-PRIVATE / ARCHIVE) | one-line reason | repo evidence path.
2. After approval: the memory moves (§2.2), one public PR (§2.3–§2.4) and, if needed, one archive-repo PR.

**Not asked:**
- Rewriting kept memories beyond the approved UPDATE rows.
- Editing owner records beyond adding migrated content.
- Changing any lesson's promotion status.
- Touching skills or `AGENTS.md`.

---

## §2 — Execution plan

### Step 2.1 — Inventory and triage (read-only)
- **Action:** read every memory file and fill the triage table. Verify each §1 hypothesis against the file's actual content and record AGREE or DISAGREE with the reason. Classify data class per `AGENTS.md` data movement.
- **Per-step gate:** every file has exactly one disposition. Any credential file is flagged.
- **Checkpoint:** return `NEEDS_CONTEXT — awaiting operator approval of TRIAGE.md`. Show Joshua the table by name, disposition and reason only, with no bodies. **Stop until he approves, edits or rejects rows.**

### Step 2.2 — Apply approved memory moves (operator-approved rows only)
- **Action:** for ARCHIVE rows, apply default (A). For UPDATE rows, make the approved edit. Write a local manifest, `local_artifacts/memory-triage-2026-11/MANIFEST.tsv`, listing name, action, and sha256 before and after.
- **Per-step gate:** `MEMORY.md` has no dangling lines, and every archived file exists under `_archive/`.

### Step 2.3 — Migrate approved MIGRATE rows
- **Public:** add each lesson to `methodology_lessons.md` in light format (default C), citing its dated incident. Screen each one first: no account identifiers or figures, P&L, prices, sizes, parameter values, Pine, ports, vendor data, absolute home paths or credentials (`AGENTS.md` data movement). Anything that fails the screen becomes MIGRATE-PRIVATE.
- **Private:** commit to `first-passage-archive` on a `claude/` branch with its own PR, following `docs/ltm/README.md`.
- **Per-step gate:** every public addition passes the screen, and the public diff contains no memory body copied verbatim beyond the lesson text itself.

### Step 2.4 — Update the index through its generator
- **Action:** in `scripts/_build_lessons_index.py`, set each archived stub to `retired` (default B) and each migrated one to `migrated`, with its `full_ref` and `siblings`. Add `retired` to `LESSONS_INDEX.md:41` and to the test's allowed set if the test enforces one. Regenerate with `python scripts/_build_lessons_index.py > docs/methodology/LESSONS_INDEX.jsonl`.
- **Per-step gate:** `.\fp.ps1 python -m pytest tests/test_lessons_index.py` passes.

### Step 2.N — Completion record
- **Action:** one public PR on branch `claude/memory-triage-2026-11` with steps 2.3 and 2.4. Its body gives counts per disposition and names only. Then comment `@codex review`. Codex reviews the public diff only, never the memory store or private rows.
- Add a `docs/SESSIONS.md` entry per its convention.

## §4 — Falsifiable hypothesis

`N/A`: this card executes Joshua's 2026-11-03 operator direction, and no hypothesis is under test.

Row-level rule:
- **If** a memory's content contradicts its §1 proposed disposition, **then** the row is re-triaged with the contradiction quoted, and Joshua decides it at the checkpoint.
- **Otherwise** the §1 disposition stands as a proposal for his approval.
- No row is acted on from its name alone.

## §5 — Forbidden moves

- **Acting on a name.** Archiving or migrating from the file name or the §1 list without reading the content. The stub rule in `LESSONS_INDEX.md` exists for exactly this.
- **Deleting a memory.** Archive only (default A). Deletion is Joshua's separate act.
- **Moving or editing before the checkpoint.** No memory move, edit or migration before Joshua approves `TRIAGE.md`.
- **Publishing private content.** Pasting memory bodies into the PR, the return or any Codex-visible surface. Copying private-class content into the public repo.
- **Hand-editing `LESSONS_INDEX.jsonl`.** It is generated; change the generator.
- **Scope creep.** Rewriting kept memories "while in there", or promoting a lesson to standing guidance. Promotion needs a high-severity or independently recurring incident (`AGENTS.md` §Continuous improvement item 5).

### §5.1 — Authority block

```yaml authority
seat: coordinator
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, governance.author, branch.push, pr.open]
constraints: [no_main_write, operator_approval_before_memory_moves, private_class_screen]
acceptance: [tests/test_lessons_index.py]
```

## §6 — Gate and status return

The card is complete when:
- Joshua has approved `TRIAGE.md`;
- every approved row has been applied and recorded in `MANIFEST.tsv`;
- the acceptance tests below pass at the public PR's head;
- that head has a clean Codex review.

A stop at the checkpoint is `NEEDS_CONTEXT`, not completion.

Return exactly one status:
- `DONE`;
- `DONE_WITH_CONCERNS`;
- `NEEDS_CONTEXT`;
- `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

Step 2.1 always returns `NEEDS_CONTEXT` for the checkpoint. This is records hygiene, not research, so no RESOLVED / FALSIFIED / AMBIGUOUS verdict applies.

### §6.0 — Acceptance tests

| Test | Property it must violate to fail | Owner |
|---|---|---|
| `tests/test_lessons_index.py` | the index is well-formed JSONL with unique IDs, no invented content on stubs, and resolving `full_ref` anchors | parent |
| `grep -c "status\": \"external-unmigrated\"" docs/methodology/LESSONS_INDEX.jsonl` | falls from 69 by exactly the approved MIGRATE plus ARCHIVE count | parent |

```
Status: <...>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...], 2.4 [...]
Counts: KEEP n / UPDATE n / MIGRATE-PUBLIC n / MIGRATE-PRIVATE n / ARCHIVE n / credential flags n
Diffs (files touched): <list>
PRs: <public PR>, <archive PR or none>
Concerns surfaced: <list>
Next action recommended: <one sentence>
```

## §7 — Parent-session review

- **Pass 1, spec compliance:**
  - Only approved rows were acted on.
  - The public diff touches only `methodology_lessons.md`, owner records named in approved rows, the generator, `LESSONS_INDEX.{jsonl,md}`, the test's allowed set and `SESSIONS.md`.
  - No memory body appears in the PR.
- **Pass 2, quality:**
  - Each migrated lesson has a dated incident and passes the data-class screen.
  - Index counts reconcile with the triage counts.
- **Pass 3, consolidated read:**
  - The memory moves, migrations and index rows all agree, row by row, with `MANIFEST.tsv`.

## §10 — Audit hooks

```bash
python -m pytest tests/test_lessons_index.py
grep -c '"status": "external-unmigrated"' docs/methodology/LESSONS_INDEX.jsonl
grep -c '"status": "retired"' docs/methodology/LESSONS_INDEX.jsonl
git diff origin/main...claude/memory-triage-2026-11 --name-only
```

## Verification

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-11-03-memory-store-triage-card-DRAFT.md --type cc_handoff
python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-11-03-memory-store-triage-card-DRAFT.md
```
