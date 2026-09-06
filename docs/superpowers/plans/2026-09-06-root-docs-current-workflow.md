# Root documentation current-workflow implementation plan

> **For agentic workers:** Use subagent-driven-development or executing-plans to execute the checklist. The operator approved the preceding root-document review and instructed: "create a task list to completion and execute it" on 2026-09-06.

**Goal:** Make the existing five root documents a concise, accurate entry point to current research, operations, and outstanding work.

**Architecture:** README routes readers; CLAUDE supplies agent constraints and essential safeguards; PIPELINES explains workflow; STATE owns current priorities and obligations; REPO_MAP describes present architecture. Campaign plans own executable next steps, campaign records own evidence and decisions, and SESSIONS preserves history.

**Tech stack:** Markdown, existing Python document readers, pytest, and the gate manifest. Python source remains compatible with 3.11+.

**Spec:** The operator-approved review in this task, concretized by the scope and acceptance criteria below; existing [root-doc charter](../../adr/2026-07-16-root-doc-charter-dedup.md) and [Rule 7](../../operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror). The ownership amendment is recorded on existing ADRs, without creating a sixth root document.

## Global constraints

- Preserve the five root filenames and established section anchors where cited.
- Preserve CLAUDE's historical MC-anchor block and Protection section; no risk constants, strategy source, allocation, authorization, account, or rail changes.
- Retain REPO_MAP's generated script inventory and its generator contract.
- STATE retains the numbered queue, decision-index heading/date bullets, Last curated, and weekly/monthly deadline headings consumed by existing readers.
- M1 item 5 / B7 Stage 1 can run with the licensed test strategy independently of queue #1; arming still requires M1 RESOLVED and separate operator GO.
- The current Select implementation plan owns executable sequence; the campaign record owns evidence and operator decisions. Summaries confer no search, admission, or live authorization.
- Existing session entries and frozen ADR bodies remain unchanged; prospective policy amendments use dated addenda and reader intercepts.
- Keep real open obligations and their dates; remove completed rows only when their existing owner retains the record.
- No new word-count gate, status database, or duplicated governance index. About half the previous root word count is a directional editorial target.
- Work on the isolated codex/root-docs-current-workflow branch. Leave unrelated main-checkout files untouched; finish with a reviewed local commit.

## Task 1 — Establish scope and baseline

- [x] Read all five root files, the current campaign plan/record, charter, Rule 7, and document readers.
- [x] Create an isolated worktree from 7185ccf and inventory protected/read-by-code sections.
- [x] Run focused baseline tests and document gates using an available Python runtime; record environmental limitations separately from failures caused by this change.

## Task 2 — Rewrite the five root documents

**Files:** README.md, CLAUDE.md, PIPELINES.md, STATE.md, REPO_MAP.md; docs/governance/INDEX.md for the moved identifier glossary.

- [x] README: one task-based navigation table, accurate five-file roles, brief public-clone note; move glossary to the existing governance index.
- [x] CLAUDE: compact posture pointers and task routing; retain essential safety and continuous-improvement rules; scope parameter immutability to locked artifacts.
- [x] PIPELINES: correct the independent M1 lane; point current Select work to its executable plan; distinguish available discovery infrastructure from running campaigns; reduce legacy instructions to owner pointers.
- [x] STATE: retain the live queue and every still-owed trigger, compress decision bullets and recurrence evidence, remove discharged audit/dead-without-trigger rows; link directly to the current campaign plan.
- [x] REPO_MAP: present current ownership/import rules and live command entry points; consolidate migration history into archive references; retain generated table and compatible section headings.
- [x] Verify root links, STATE currency, layer-map parity, generated-table parity, and protected CLAUDE blocks.

## Task 3 — Make session routing independent of historical queue copies

**Files:** scripts/check_sessions_queue_bind.py, tests/test_sessions_queue_bind.py, scripts/gates.yml, docs/SESSIONS.md header, .cursor/rules/session-discipline.mdc, .cursor/rules/session-log.mdc.

**Interface:** Preserve the existing checker filename, gate id, --state and --file options. The living SESSIONS header must contain a real relative Markdown link resolving to the supplied STATE file before the first dated entry. The STATE file must contain its OPERATOR QUEUE section. A queue change must not require rewriting or adding a historical entry. Open / next becomes optional, session-specific historical context.

- [x] Write regression tests for queue changes without journal changes and entries without Open / next. Negative cases: absent/incorrect header link, a link only in a historical entry, absent queue section, unreadable files. Exercise CLI results, not source-text tokens.
- [x] Run the new tests against the original reader and record the expected failures.
- [x] Implement the minimal header-routing check and update gate reachability for both consumed files and the checker.
- [x] Update the living session header and Cursor instruction mirrors; preserve all existing dated entry bytes.
- [x] Run the routing tests and relevant gate-manifest tests; obtain scoped review.

## Task 4 — Amend existing ownership records

**Files:** docs/operational_rules.md, docs/adr/2026-07-16-root-doc-charter-dedup.md, docs/adr/2026-08-07-w5-governance-diet.md, docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md, docs/governance/INDEX.md, STATE.md.

- [x] Rule 7: STATE owns current priorities, campaign plans own executable steps, session entries are historical; date the edit log.
- [x] Root charter: append the operator-approved execution record, exact scope of ownership change, retained parser surfaces, and current runnable verification commands; retain the existing semantic-loss falsifier.
- [x] W5 and Survive-bound: append pointers expressly replacing queue-copy requirements while retaining the queue cap and safety boundaries; intercept superseded instructions at reading entry points.
- [x] Resolve the outstanding posture-size item through actual trimming or an explicit bounded exception recorded in the charter; remove its STATE row only when discharged.
- [x] Add one concise session entry recording this judgment and linking the plan/owner amendment; no live queue copy.
- [x] Check relevant ADRs and regenerate an index only if its source headers changed.

## Task 5 — Verify and review

- [x] Run the five document checks plus lifecycle consistency, append-only/order checks, relevant ADR checks, and gate-manifest checks.
- [x] Run focused regression tests; broaden to the repository suite where the available runtime/dependencies support it.
- [x] Confirm unchanged safety blocks, unchanged prior SESSIONS entries, retained open obligations, and a clear current-plan/M1 route.
- [x] Record before/after root word counts without adding a permanent gate.
- [x] Obtain independent whole-change review, resolve findings, and rerun affected checks.

## Task 6 — Deliver

- [x] Complete this checklist with verification evidence and any remaining environmental limits.
- [x] Commit the reviewed change on the isolated branch and expose the diff to the operator.

## Execution evidence

Baseline: 7185ccf. Five root files contained 14,206 whitespace-delimited words. The original root-link, STATE currency, session queue, layer-map, and generated-table checks passed in the review. The main checkout's .venv launchers refer to an unavailable Python 3.11 interpreter; execution uses the available runtime without modifying that environment.


### Verification results — 2026-09-06

- Baseline focused suite: **42 passed**. Final focused suite: **145 passed** across
  `test_sessions_queue_bind`, `test_gate_manifest`, `test_roll_sessions`,
  `test_state_currency`, `test_repo_map_layers`, `test_repo_map_scripts_table`, and
  `tests/ops/test_recall_guard.py`.
- Routing regression RED: 5 failed / 3 passed against the former reader; GREEN:
  all 8 passed. Gate-trigger mutation: narrowing the selector to SESSIONS alone
  caused both new consumed-path tests to fail while the unrelated-path control
  passed. The manifest was restored; the final focused suite includes the fix.
- Full blocking manifest (`python scripts/gate_manifest.py --tier check`) passed.
  Direct root-liveness, STATE-currency, session-routing, layer-map, generated-table,
  lock-anchor, lifecycle, ADR-graph, and session order/append-only checks passed.
  Private data absent from this checkout produces the existing manifest warnings;
  M1 remains CODE_LANDED, not RESOLVED.
- Root links and heading anchors resolve. Generated script inventory remains 66
  rows. CLAUDE's Strategy Reference, Protection and Continuous improvement blocks
  match the baseline. Prior dated session bytes are unchanged (SHA-256
  `47f56b149e547397212804eac0aced1effbfdb929113b177fa690142cab03461`).
- Root word count: **14,206 → 6,261**, a **55.9% reduction**. Live-execution posture
  is 22 lines including the following heading, meeting the existing 25-line limit.
- Open-obligation review retained the two queue items, private weekly ledger debt,
  recurring dates, monitoring/data prerequisites, November audits and reconciliation
  debts, and February expiry/starvation checks. The charter addendum records the
  completed rows removed. No `core/`, `ops/`, or `deploy/` files changed.
- Root-charter brief validation passed without warnings. ADR graph and supersession
  placement passed; no indexed ADR source headers changed, so index regeneration
  was unnecessary. W5 has the same two legacy brief-format hard errors as baseline
  7185ccf (missing §10 and §0 citation-anchor format); its frozen body was preserved.
- The repository-wide pytest attempt stopped at collection: 2 errors in
  `test_detector_kit.py` and `test_grow0_limb_c.py`, 7 skips. The installed SciPy
  extensions target Python 3.11, incompatible with the available 3.12 runtime.
  This is an environment limit; no full-suite success is claimed.
- Runtime: bundled Python 3.12.14 with its native libraries first and the existing
  venv's pure-Python test dependencies appended using a scratch `sitecustomize.py`.
  Pytest plugin auto-loading was disabled; timezone data was supplied from the
  existing venv. Temporary test directories were outside Git so session-roll
  no-history fixtures did not inherit this repository's history. No environment
  or dependency files were changed.
- Scoped session-routing review: spec **PASS**, quality **PASS**; its sole P2
  (missing STATE/checker selector coverage) was fixed and re-reviewed.
- Whole-document review found and resolved one omitted distinction: M-C's ECR
  pursuit wakes on a NAS100/MNQ-shaped leg's first live fill, independently of the
  separate add-slippage capture trigger. STATE now preserves both with their
  owner pointers. The reviewer confirmed the repaired row and found no further
  actionable documentation regressions.
- Whole-change review also found that the route scanner accepted Markdown examples
  and comments. Regression cases first reproduced the defect; the repaired scanner
  rejects comment-only and inline/fenced/indented code-only routes while accepting
  visible plain and code-formatted labels. The six-case boundary matrix passes.
- Final whole-change review: spec **PASS**, quality **PASS**, no remaining findings.
  Both P2 findings were fixed and re-reviewed. The completed 145-test suite, blocking
  gate manifest and whitespace check passed after the fixes. Delivery is a local
  commit on `codex/root-docs-current-workflow`; the main checkout is not modified
  by this task.
- PR #317 review follow-up: four failing CLI cases reproduced three Markdown-parser
  gaps before repair. The checker now accepts longer valid closing fences and
  reference-style links, and ignores dated headings in comments or fenced examples
  when locating the first historical entry. The final affected suite passed **149
  tests**, and the blocking gate manifest passed before the repair commit.
- The requested re-review exposed four further cases. A context-aware block scanner
  now keeps comment markers inside fences from hiding later links, STATE queue
  validation excludes comments and code examples, and shortcut references resolve.
  All four regressions failed before and passed after the second repair. The final
  affected suite passed **153 tests**, and the blocking gate manifest passed.
- The third PR review exposed raw HTML blocks, list-continuation indentation, and a
  closure-template ownership mismatch. Three initial parser regressions failed before
  repair; broader CommonMark cases then showed that a hand-built block scanner would
  duplicate container-stack semantics. It was replaced with `markdown-it-py` tokens;
  the project dependency and existing hashed lock now record that direct use. The
  routing suite covers raw HTML categories, lists, blockquotes, fences, comments,
  references, top-level heading/table scope, and heading word boundaries.
- Brief-authoring application tests reproduced the ownership ambiguity before the
  edit: two of three fresh scenarios used a SESSIONS Open / next line as the sole live
  record. After the skill and template amendment, all three routed cross-session work
  to STATE and campaign-local work to its existing owner, and rejected SESSIONS as the
  sole live board write.
- The final third-review repair passed **274 tests** with **1 skipped**, the canonical
  brief-authoring self-test, all skill-reference checks, the skill constants guard,
  Python compilation, and the full blocking gate manifest.
