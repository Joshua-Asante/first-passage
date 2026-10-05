# T00 screen authority: build card

**Type:** cc_handoff (build card; packets dispatched by the coordinator against this card once approved)

**Date:** 2026-10-03 (UTC).

**Status:** DRAFT — awaits Joshua's approval (design §8 step 5). No packet starts and no code is written before that approval is recorded in §8 below.

**Revision:** 2 — folds review r02 (P2-1…P2-6) under coordinator (3) rulings; #581 head `438b659`.

**Authority:**
- Operator ruling **A1** (Joshua, direct, 2026-10-02 ~01:50Z, "all recommended"): design → approval → build → one P7 re-run at the merged head → ratify #581 §3 → sign → step 3 once.
- **Design approval** (Joshua, 2026-10-02 local, "all recommended" on design §12; item 9, depth N, still open): [T00 screen-authority design](../../superpowers/specs/2026-10-02-t00-screen-authority-design.md), PR #629 head `3742a95ac3fb084da9cd722ed98721c78699e879`, revision 3.1. That file is the frozen contract for this build; a change to it needs a new operator acceptance.
- **This card** needs Joshua's own approval (design §8 step 5) before any packet starts. It narrows the design; it adds no authority to it.

**Coordinator:** coordinator (3). It freezes each packet, owns the claim manifest, reviews every diff, opens PRs, integrates, and records H. Joshua merges.

**Return boundary (card level):** every packet returns to the coordinator (§6). The card ends at step 7's accepted P7 record at H (§7); steps 8–12 are outside it.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - no_pr_open
  - packet_write_footprint_only
  - red_first
  - no_forbidden_file_edit
  - no_sealed_method_source_change
  - no_runner_or_bracket_semantics_change
  - no_source_refusals_change
  - no_r3c_bytes_or_pinned_key_change
  - no_dd_protection_edit
  - no_pine_or_port_copy_or_quote
  - no_private_bytes_in_git
  - no_real_source_test
  - no_real_source_screen_run
  - no_probe
  - no_mc
  - no_agent_signature
  - no_key_enrollment
  - no_glm_for_trust_auth_or_private_inputs
  - single_writer_per_branch
  - stop_at_coordinator_return
acceptance:
  - tests/ops/qualification/test_screen_authority.py
  - tests/ops/qualification/test_production_source.py
  - tests/ops/qualification/test_p7_evidence.py
  - tests/ops/qualification/test_source_consumers.py
  - tests/ops/qualification/test_t00_screen_verdict.py
  - tests/ops/qualification/test_t00_screen_state.py
  - tests/ops/qualification/test_t00_screen_plan.py
  - tests/ops/qualification/test_t00_screen_driver.py
  - tests/ops/test_book_adapters_parity.py
```

## §0 — Production reads and prerequisites

**Reads** (every packet, at its base; record `git log -1 --format='%h %as' -- <path>`):
- the design in full at `3742a95`, especially §2.2 (60 rows), §3–§7, §8, §9, §9.1, §10, §11, §13;
- `ops/c1_rail/qualification/production_source.py`, `p7_evidence.py`, `p7_driver.py`, `contract.py` (`:366-435`, `:963-968`, `:1037-1062`, `:1168-1215`), `runner.py`, `bracket.py`, `blocks.py`, `paths.py`, `regime.py`;
- `tests/ops/qualification/test_source_consumers.py`, `test_p7_evidence.py`, `test_production_source.py`;
- [2026-09-30 spec](../../superpowers/specs/2026-09-30-t00-source-only-contract-design.md) A1–A23 (regression set);
- the packet's own §2 sub-section here.

Design line numbers are at `origin/main@152716d`. #611 edits `production_source.py`; P-B2 re-anchors those lines after #611 merges.

**Prerequisites** (each recorded by SHA in §8 before the packet it gates starts):

| # | Prerequisite | Gates |
|---|---|---|
| PR-1 | #629 merged at a reviewed head (coordinator review + one narrow Codex review, design §8 step 2). Today OPEN at `3742a95` | every packet |
| PR-2 | #581 merged **as DRAFT** with A5/A6 frozen and a dated note naming the frozen commit and the A5/A6 section hashes; design §3 item 8 settled **as drafted** (design §8 step 3, §12 item 5). Today OPEN, draft, head `438b659`; its A5/A6 bytes equal those at `f0208f3`, the head the design read (values in §2.6). The coordinator re-checks them at the merged commit before freezing P-C | P-C, P-A |
| PR-3 | #611 merged (design §8 step 1). Today OPEN, draft, head `76cc8c1` | P-B2 |
| PR-4 | The design §8 step-4 docs PR (§11 addendum to the 2026-09-30 spec; A10b reasons; #581 §5 item 3 wording; §3 cells as pointers to the values block) merged as its own PR. Must not touch #581's A5/A6 bytes | H |
| PR-5 | This card approved by Joshua (design §8 step 5) | every packet |

## §0.5 — Card decisions (Joshua answers with the card) and recommended defaults

The design's §9.1 packets leave five footprint collisions. The card resolves them as below; each is a packaging change, not a design change.

- **K-1. Split P-B into P-B1 and P-B2.** The design places `ScreenBracket` and the epoch helpers in `screen_authority.py` (§3.3, §9), which P-A owns, while P-B's `screen_epoch`/`screen_bracket` call them; and P-A's row K3 reads `SCREEN_BOOTSTRAP_SHA256`, which P-B's `p7_evidence.py` produces. One P-B packet would form a cycle with P-A. *Recommend:* P-B1 = `p7_evidence.py` (bootstrap template, `SCREEN_BOOTSTRAP_SHA256`, forbidden lists); P-B2 = `production_source.py` and A10b. Order P-B1 → P-A → P-B2. Both stay CC solo.
- **K-2. Move rows S2 and B1.** S2's enforcement is the worker audit hook, which lives in the bootstrap template (`p7_evidence.py`, §5.1). B1 is a record schema in `journal.py`. *Recommend:* S2 → P-B1; B1 → P-D. Row totals are unchanged (§2 table).
- **K-3. `t00_screen/__init__.py`.** P-C, P-D, P-E and P-F each need the package to exist. *Recommend:* each of those packets adds the file with exactly these bytes, which git merges as identical adds: `"""T00 step-3 screen driver (design 2026-10-02 section 9)."""` followed by one LF. Any other byte in it is a manifest violation.
- **K-4. Card-proposed names and formats** (the design leaves them open): `p7_evidence.render_bootstrap(params)` (template), `p7_evidence.SCREEN_BOOTSTRAP` and `SCREEN_BOOTSTRAP_SHA256`, `screen_authority.bind_screen_run(run_dir, authority_sha256)` (row K4's write-once binding, called by `t00_screen.worker`), and every item marked (K-4) in §3. *Recommend:* adopt; the coordinator may rename at freeze without a new approval if behaviour is unchanged.
- **K-5. Build ahead of merge.** P-D and P-E have no code dependency for their row tests, and P-E's tests use a fake source against the frozen design §3.3 signatures (card §3.1). *Recommend:* P-D, P-E and P-F may be built from wave 1 against the frozen interface in §3, but merge only in the §4 order and re-take their red and green records at the final rebased base (§2.2).

Missing facts or a contradicted default return `NEEDS_CONTEXT`; they are never assumed.

## §1 — Context

r3c's `SOURCE_REFUSALS` include `SCREEN` and `MONTE_CARLO`; there is no step-3 runner (design §1). The design adds a second, separately signed door: a `t00_screen_authority/v1` document signed under `APPROVE_T00_SCREEN_AUTHORITY`, a gated `ProductionSource.screen_epoch`/`screen_bracket` scored by the unchanged `runner.evaluate_replay`, and a ledgered, resumable driver. This card turns design §9 and §9.1 into packets with disjoint write footprints, red-first tests per §2.2 row, and an integration order ending at head H, where A1 step 5 (one P7 re-run) happens.

## §2 — Claim manifest and packets

### §2.1 Claim manifest (write footprints; every path under the repo root)

| Packet | Writes (exactly) | Rows owned (count) |
|---|---|---|
| P-A | `ops/c1_rail/qualification/screen_authority.py` (new); `tests/ops/qualification/test_screen_authority.py` (new) | A1–A11, K1–K4, X2, X3 (17) |
| P-B1 | `ops/c1_rail/qualification/p7_evidence.py`; `tests/ops/qualification/test_p7_evidence.py` | K10, S2 (2) |
| P-B2 | `ops/c1_rail/qualification/production_source.py`; `tests/ops/qualification/test_production_source.py`; `tests/ops/qualification/test_source_consumers.py` | K5–K9 (5) |
| P-C | `ops/c1_rail/qualification/t00_screen/verdict.py` (new); `tests/ops/qualification/test_t00_screen_verdict.py` (new); `t00_screen/__init__.py` (K-3 bytes) | V1–V4 (4) |
| P-D | `t00_screen/state.py`, `t00_screen/journal.py` (new); `tests/ops/qualification/test_t00_screen_state.py` (new); `t00_screen/__init__.py` (K-3 bytes) | S1, S3, S9, S10, S13, S14, S16, B1 (8) |
| P-E | `t00_screen/plan.py` (new); `tests/ops/qualification/test_t00_screen_plan.py` (new); `t00_screen/__init__.py` (K-3 bytes); only if `plan.py` has an A10b finding, `tests/ops/qualification/test_source_consumers.py`, limited to ALLOWLIST entries for P-E's own (owner, capability) pairs and written after P-B2 merges (O-10) | R1–R3 (3) |
| P-F | `t00_screen/coordinator.py`, `worker.py`, `__main__.py` (new); `scripts/t00_screen_label_check.py` (new); `tests/ops/qualification/test_t00_screen_driver.py` (new); `t00_screen/__init__.py` (K-3 bytes); `tests/ops/qualification/test_source_consumers.py`, limited to ALLOWLIST entries for P-F's own (owner, capability) pairs and written after P-B2 merges (O-10); `REPO_MAP.md`, limited to the generated scripts-table block produced by `python scripts/check_repo_map_scripts_table.py --write` | S4–S8, S11, S12, S15, B2–B5, X1, X4–X6 (16) |
| coordinator | review, audit hooks, this card's §8 | G1–G5 (5) |

Total 60 = design §2.2. `t00_screen/` is `ops/c1_rail/qualification/t00_screen/`.

**Overlaps flagged** (all resolved; the only shared writes are K-3's identical bytes and O-10's ALLOWLIST additions after P-B2 merges):

| # | Overlap in the design | Resolution |
|---|---|---|
| O-1 | `ScreenBracket`, `open_screen_epoch`, `require_open_screen_epoch`, `close_screen_epoch` sit in `screen_authority.py` but serve rows K6/K8 | P-A writes them to the §3 signatures; P-B2 tests them (K6, K8). K-1 |
| O-2 | K3 reads `SCREEN_BOOTSTRAP_SHA256` from `p7_evidence.py` | P-B1 produces it; P-A rebases on P-B1. K-1 |
| O-3 | S2's worker audit hook is in the bootstrap template | S2 → P-B1. K-2 |
| O-4 | B1's record schema is in `journal.py` | B1 → P-D. K-2 |
| O-5 | A9, A11 and V3 share `A5_TEXT_SHA256`, `A6_TEXT_SHA256`, the section spans (§2.6), `A6_HORIZON_SESSIONS`, the `a5_rule` IDs and `median_rule` | defined once in `t00_screen/verdict.py` (P-C), the spans as `section_text` (§3.7); `screen_authority` imports them (design §8 step 3: "the verdict code pins the hashes"). P-A rebases on P-C |
| O-6 | X3 spans `validate_screen_act` (P-A), the ACT transition in `state.advance` (P-D) and the act-file recording in `act`/`resume` (P-F) | `test_X3` (P-A) covers the validator; P-D covers ACT transitions under `test_S1`'s table; P-F covers recording in I1 |
| O-7 | K4 spans the check (P-A) and the binding call (P-F) | P-A defines `bind_screen_run`; P-F calls it once per worker |
| O-8 | K6's closure agreement across epochs is checked in `state.check_record` (P-D) | P-D implements the clause; `test_K6` stays in P-B2; I1/I3 (P-F) exercise it end to end |
| O-9 | `t00_screen/__init__.py` | K-3 |
| O-10 | A10b's meta-test (`test_source_consumers.py:195-202`) refuses an ALLOWLIST entry whose owner is missing or uses no capability, so P-B2 cannot pre-allowlist P-F's `screen_epoch`/`screen_bracket` calls or a `.contract` load (`CAPABILITY_ATTRIBUTE`) | P-F, and P-E only if `plan.py` has a finding, adds ALLOWLIST entries for its own (owner, capability) pairs only, after P-B2 merges; the capability owners are frozen in §3.2; any other edit to the file is a manifest violation |
| O-11 | S15 spans `coordinator.finalize` (run lock, `FINALIZE_NOT_COMPLETE`) and the "gap after COMPLETE is `CORRUPTION`" clause | S15 → P-F, which owns `test_S15`. The gap clause stays a P-D helper inside `check_record`, covered by P-D's non-row case `test_check_record_gap_after_complete`; P-F's `finalize` calls `check_record` |

### §2.2 Common rules (every packet)

- **Forbidden files** (design §9): `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py`, `replay.py`, `book_policy.py`, `core/` (including `dd_protection.py` and `mc/`), every Pine source, port and private artifact, r3c's bytes, `SOURCE_SIGNING_KEYS`, `SOURCE_REFUSALS` and the pinned key. Any file outside the packet's row of §2.1.
- **Sealed methods** in `production_source.py`: `replay`, `replay_bracket`, `proof`, `_seal`, `_check_path`, `_verify_integrity`, `verify_for` keep their source text (row K7).
- **Semantics:** `runner.evaluate_replay`, `runner._run_stage` and `bracket.run_bracket` behave exactly as at the base.
- **Tests:** TEST_ONLY keys generated in-process; only the pinned root and the validator's repository-root constant are monkeypatched; synthetic fixtures only. No test reads the real source (design §10).
- **Red-first:** each row test `test_<row>` is committed and recorded failing on the packet base through the launcher, then passing on the build; each asserts its row's code and has a passing twin. A row test that cannot be made red on the base is a stop (§6). **K-5 exception:** a packet built early against §3 rebases onto its final base (every §4 dependency merged) and re-takes its red and green `record.json` there before its PR opens; records from an earlier base do not count toward H.
- **Launcher records:** `.\fp.ps1 python -m pytest <files>` (or `python -I scripts/fp.py python -m pytest <files>`), each citing its `.cache/fp-verification/.../record.json` with `status: completed`, `verification_exit_code` and `source_stable`.
- **Branch:** `claude/t00-screen-<packet>` (or `glm/`, `cursor/` per lane), cut from `origin/main` after its §4 dependencies merge (a K-5 packet may be cut earlier; see red-first); one writer.

### §2.3 P-A — authority, validator, receipts, acts

- **Rows:** A1–A11, K1–K4, X2, X3.
- **Writes:** `screen_authority.py`, `test_screen_authority.py`.
- **Builds:** `SCREEN_AUTHORITY_FIELDS`; compiled r3c digest; compiled pre-registration chain (row A8) and A3 successor paths and patterns (row A10); `validate_screen_authority` (step order design §3.2: bytes → signature → `_check_bindings` → issue); `_check_bindings` (A5–A10, repository root `Path(__file__).resolve().parents[3]`, `git --end-of-options`, `core.autocrlf=false`); `ValidatedScreenAuthority` with weakref registry; `require_validated_screen_authority` (K1–K4, `SCREEN_APPROVAL_EXPIRED` re-code); `bind_screen_run`; `ScreenBracket`, `open_screen_epoch`, `require_open_screen_epoch`, `close_screen_epoch` with the stat guard (design §3.3); `validate_screen_act` (X2, X3). Scopes `APPROVE_T00_SCREEN_AUTHORITY`, `APPROVE_T00_SCREEN_ACT`. K4 reads the ledger and run lock through `journal.read` and `journal.read_lock`, and A9 recomputes the sections through `verdict.section_text` (§3).
- **Imports, never edits:** the `contract.py` helpers listed in design §3.2.
- **Red-first tests:** `test_A1`…`test_A11`, `test_K1`…`test_K4`, `test_X2`, `test_X3` (design §2.2 column 4 names the violating input of each).
- **Lane:** CC solo. Trust/auth: never GLM, never Cursor.
- **Depends on:** PR-1, PR-2, PR-5; P-B1 merged (O-2); P-C merged (O-5); P-D merged (K4 reads the ledger and lock, §3.4–§3.5).
- **Return:** §6 taxonomy, plus the §3 interface as built (signatures verbatim).

### §2.4 P-B1 — bootstrap template and forbidden lists

- **Rows:** K10, S2.
- **Writes:** `p7_evidence.py`, `test_p7_evidence.py`.
- **Builds:** one bootstrap template (`render_bootstrap`) generating `P7_BOOTSTRAP` with P7's parameters and `SCREEN_BOOTSTRAP` with the screen's (C8); `SCREEN_BOOTSTRAP_SHA256`; the screen's forbidden list (design §5.1) and stubs for `runner._run_stage` and `runner.run_synthetic_stage`; P7's list gains `c1_rail.qualification.screen_authority` and `c1_rail.qualification.t00_screen`; the screen audit hook refuses write-opens outside the worker's own journal (`SCREEN_WRITE_REFUSED`).
- **Red-first tests:** `test_K10`, `test_S2`; regression 2026-09-30 A16–A23 (`test_p7_evidence.py`) unchanged in outcome. `P7_BOOTSTRAP_SHA256` is expected to change (C8); record old and new values in the return.
- **Lane:** CC solo (P7 closure, security). Never GLM.
- **Depends on:** PR-1, PR-5.
- **Return:** §6, plus old/new `P7_BOOTSTRAP_SHA256` and `SCREEN_BOOTSTRAP_SHA256`.

### §2.5 P-B2 — the gated capability and A10b

- **Rows:** K5–K9.
- **Writes:** `production_source.py` (`screen_epoch`, `screen_bracket`, `_verify_identity`, `_consumed_splits` only), `test_production_source.py`, `test_source_consumers.py` (allowlist keyed by (owner, capability); `screen_bracket`, `screen_epoch`, `_replay_raw`, `_engine` added to the scan).
- **Red-first tests:** `test_K5` (spy on `_engine`), `test_K6` (mtime change mid-epoch), `test_K7` (seven sealed functions' source hashes recorded before the build equal those after), `test_K8` (deadline in R2 only), `test_K9` (planted call under an owner allowlisted only for `replay_bracket`). Regression: 2026-09-30 A1–A15 in `test_production_source.py` and `test_source_contract.py` unchanged in outcome.
- **Lane:** CC solo. Never GLM.
- **Depends on:** PR-3 (#611 merged; re-anchor line numbers), P-A merged (O-1).
- **Return:** §6, plus `git diff -U0` of `production_source.py` showing no hunk inside the seven sealed functions.

### §2.6 P-C — verdict (pure)

- **Rows:** V1–V4.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/verdict.py`, `test_t00_screen_verdict.py`.
- **Builds:** #581 A5 (1)–(3) and A6 by reference, exact integer comparisons (`20·bust ≤ n`, `2·pass ≥ n`), `UNDETERMINED` in every denominator, pessimistic assignment decides GO and optimistic labels NO-GO; returns `INSUFFICIENT(reasons)` or the labels, never both (V1); constants `A5_TEXT_SHA256`, `A6_TEXT_SHA256`, `A6_HORIZON_SESSIONS`, the `"T00_A5/v1"` rule ID and `"LOWER_NEAREST_RANK_INF_INCLUDED"`; `section_text` (§3.7).
- **Pinned values** (#581 at `438b659`, blob `545a2f55366e22cc92fcc35ff9282ef89866a360`; both sections byte-identical at `f0208f3`):
  - `A5_TEXT_SHA256 = "a8f6f25e025a2e136e477580b7e569531d770a1e35e712b72f5a6b9b50eb391b"`: the bytes from the start of the `### A5` line to the start of the `### A6` line;
  - `A6_TEXT_SHA256 = "b3bdc77baf3e6383f1df08afd2f0fbb8a7c930d95a0f56b0c5669a5e18b217d9"`: the bytes from the start of the `### A6` line to the start of the `## §3` line (one rule for both sections: from the section's heading line up to, not including, the next heading line; coordinator (3) ruling 2026-10-02, computed on #581 blob `545a2f55…a360`).
  `section_text` implements exactly these spans. P-C stops (§6) if PR-2's merged blob gives other values.
- **Red-first tests:** `test_V1` (reasons plus GO-shaped tallies), `test_V2` (bust count exactly 5%), `test_V3` (one constant changed), `test_V4` (hybrid row).
- **Lane:** GLM-eligible, synthetic rows only. `workdir` = a fresh worktree under `.claude/worktrees/` with no `.env`; the ticket carries no private value, no Pine or port path, no account data. The coordinator reads the full diff before acceptance (operator GLM rule). CC if GLM fails twice.
- **Depends on:** PR-1, PR-2, PR-5.
- **Return:** §6, plus the two section hashes and the blob they were taken from.

### §2.7 P-D — state, journal, transition function

- **Rows:** S1, S3, S9, S10, S13, S14, S16, B1.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/state.py` (`advance`, `classify`, `check_record`), `t00_screen/journal.py` (§3.4–§3.5: hash-chained append/fsync, torn-tail rule, lock reader, record schemas including B1's cost fields, canonical `results.json`), `test_t00_screen_state.py`.
- **Builds:** the §4.2 transition table exactly; the closed §4.3 class table; K6's closure-agreement clause in `check_record` (O-8); the S15 gap clause in `check_record` (O-11); S16's byte equality across W and segmentation.
- **Red-first tests:** `test_S1`, `test_S3`, `test_S9`, `test_S10`, `test_S13`, `test_S14`, `test_S16`, `test_B1`; plus an ACT-transition case table under `test_S1` (O-6) and the non-row case `test_check_record_gap_after_complete` (O-11). Fake source only.
- **Lane:** CC (the transition function is the crash model).
- **Depends on:** PR-1, PR-5. Built from wave 1 (K-5); merges per §4.
- **Return:** §6, plus the §4.2 table as implemented (state × event → state) for diff against the design, and §3.4–§3.6 as built.

### §2.8 P-E — plan

- **Rows:** R1–R3.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/plan.py` (`seed`, key universe and plan digest, `candidates`, `shape_check`), `test_t00_screen_plan.py`; `test_source_consumers.py` only under O-10.
- **Builds:** seed = first 8 bytes of SHA-256 of canonical `["t00-screen-rng/v1", purpose, root, population, path_index]`, never `regime.domain_seed`; candidates as the R1 ∩ R2 joint-flat intersection stored as indices plus digest (§5.2); `shape_check` per §5.3.
- **Red-first tests:** `test_R1` (W = 1 vs W = 4; collision scan against `domain_seed`), `test_R2` (block flat in R1 only), `test_R3` (short run without the flag).
- **Lane:** Cursor or CC. Read-only access to `blocks.py`, `paths.py`, `regime.py`.
- **Depends on:** P-B2's interface (§3); built from wave 1 against a fake source (K-5); merges after P-B2.
- **Return:** §6.

### §2.9 P-F — coordinator, worker, CLI, label script, integration

- **Rows:** S4–S8, S11, S12, S15, B2–B5, X1, X4–X6.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/coordinator.py`, `t00_screen/worker.py`, `t00_screen/__main__.py` (`preflight`, `accept-p7`, `run`, `resume`, `finalize`, `verify`, `act`), `scripts/t00_screen_label_check.py`, `test_t00_screen_driver.py`; ALLOWLIST entries in `test_source_consumers.py` for its own (owner, capability) pairs, after P-B2 merges (O-10); the scripts-table block of `REPO_MAP.md`, regenerated by `python scripts/check_repo_map_scripts_table.py --write` and changed nowhere else.
- **Builds:** run and run-root locks (§3.4), O_EXCL run directory, ledger-only writer, Job Object (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, suspended → assigned → resumed), pinned worker environment, budget gate and overhead reserve, probe sequencing, fixed console lines (§5.6), `verify` with k = 9 hash-derived re-executions inside the K3/K4 gate, `accept-p7` writing `p7_acceptance.json`, the worker command and journal names (§3.3), `worker.open_epoch` and `worker.bracket` as the only capability callers (§3.2), and `finalize` under the run lock from COMPLETE or TERMINAL only (`FINALIZE_NOT_COMPLETE`), calling `check_record` (O-11). The label script imports nothing from `t00_screen.verdict` (X5) and is written without reading P-C's implementation.
- **Red-first tests:** `test_S4`…`test_S8`, `test_S11`, `test_S12`, `test_S15`, `test_B2`…`test_B5`, `test_X1`, `test_X4`, `test_X5`, `test_X6`; integration I1 (every §4.4 crash window), I2 (Ctrl-C through `fp.ps1` lands as W22 and resumes), I3 (every ledger prefix folds to its durable state). Real subprocess workers, deterministic fake source, TEST_ONLY seam only.
- **Lane:** CC integration.
- **Depends on:** P-A, P-B1, P-B2, P-C, P-D, P-E merged.
- **Return:** §6, plus the revision-2 test map (design §10) checked off.

## §3 — Frozen interface (the coordinator re-states it verbatim in each packet ticket)

Derived from design §3–§5. Items marked (K-4) are card proposals where the design leaves a name or format open.

### §3.1 Authority, capability, bootstrap, plan

- `screen_authority.validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root, now) -> ValidatedScreenAuthority`
- `screen_authority.require_validated_screen_authority(auth, *, source_contract, now)`
- `screen_authority.validate_screen_act(act_bytes, approval_bytes, public_keys, *, authority, ledger_head, now)`
- `screen_authority.ScreenBracket(bracket: BracketReplayResult, deadline_failure: tuple[bool, bool], consumed_splits: tuple[tuple, tuple])`
- `screen_authority.open_screen_epoch(source, authority)`, `require_open_screen_epoch(epoch, *, source, authority)`, `close_screen_epoch(epoch)`, `bind_screen_run(run_dir, authority_sha256)`
- `ProductionSource.screen_epoch(*, authority)`, `ProductionSource.screen_bracket(path, *, authority, epoch) -> ScreenBracket`
- `p7_evidence.render_bootstrap(params)`, `P7_BOOTSTRAP`, `P7_BOOTSTRAP_SHA256`, `SCREEN_BOOTSTRAP`, `SCREEN_BOOTSTRAP_SHA256`
- `t00_screen.plan`: `seed(...)`, `candidates(...)`, `shape_check(run, failed, path)`

### §3.2 Capability consumers (A10b; O-10)

- `ProductionSource.screen_epoch` has one owner, `c1_rail/qualification/t00_screen/worker.py:open_epoch`, and `ProductionSource.screen_bracket` one, `c1_rail/qualification/t00_screen/worker.py:bracket` (K-4). The candidate pass, the probe, every path key and every `verify` re-execution call `bracket`. These two pairs, plus any `.contract` load in a P-F module, are P-F's ALLOWLIST entries. `_replay_raw` and `_engine` have no consumer outside `production_source.py`.
- `screen_authority.py` (which receives the contract as `source_contract`), `state.py`, `journal.py` and `verdict.py` have no A10b finding. `plan.py` has none unless P-E records one under O-10; `plan.candidates` receives the candidate worker's `ScreenBracket`s and calls no capability.

### §3.3 Worker process (rows S2, K3, K4; design §5.1)

- **Command**, built by the coordinator and started suspended in the Job Object: `[sys.executable, '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP, code_root, run_dir, authority_sha256, journal_name]`, every path absolute and resolved, `code_root` the checkout at H (K-4).
- **Entry point:** after installing its audit hook, recording finder and stubs, the bootstrap runs `runpy.run_module('c1_rail.qualification.t00_screen.worker', run_name='__main__', alter_sys=False)`, as P7 runs `p7_driver`. The recorder stays `sys.p7_recorder`; K3 compares its `bootstrap_sha256` with `SCREEN_BOOTSTRAP_SHA256` (K-4).
- **Journal path:** `journal_name` matches `^[csv][1-9][0-9]*-w[0-9]+[.]jsonl$`: `cN-w0` is the candidate-and-probe worker's N-th start, `sK-wI` segment K's worker I, `vN-wI` the N-th `verify`'s worker I (K-4). The bootstrap refuses any other name. The S2 audit hook allows a write-open (an `open` whose mode has `w`, `a`, `x` or `+`, or an `os.open` with a write, append or create flag) only of `realpath(join(run_dir, 'journal', journal_name))`, and, under contract amendment CA-1 below, of the null device. Any other raises `SCREEN_WRITE_REFUSED`.

*Contract amendment CA-1 and coordinator note 2026-10-03 (coordinator (3), card owner; P-B1 review r05 P1, and P-B1 concerns 1–3).* CA-1 changes frozen behavior. Design §5.1 :458 and row S2 refuse every write-open outside the worker's own journal, so CA-1 binds only with Joshua's explicit acceptance, which is recorded on its line. The other bullets close encodings that §3.3 left open.
- **CA-1 Null device (amends design §5.1 :458 and row S2; operator acceptance: ACCEPTED by Joshua 2026-10-03, about 17:19Z, directly to coordinator (3): "I approve your recommendations", in reply to a list that included "CA-1: the null-device exception. I recommend accepting.").** A write-open whose target is the null device (`os.devnull`, normalised as the hook normalises the journal path) is allowed. It holds no data, so the ledger stays protected. CPython's `platform._syscmd_ver` opens it read-write through `subprocess.DEVNULL`; it is reached from the worker import chain (`runner` → `core/mc/ingest.py` → `pandas` → `platform.machine()`) when a WMI query fails. Refusing it killed workers at random. Every other target is still refused.
- **Hook as built (P-B1).**
  - The rule is active from straight after `import os` in the bootstrap.
  - Targets are compared by `normcase(realpath(...))`.
  - A write-mode `open` of an int descriptor is allowed: that descriptor's own open was already checked.
  - A journal name that fails `re.fullmatch` on the pattern above exits `SCREEN_WRITE_REFUSED`.
  - The screen argv check is `len(sys.argv) < 5`.
- **Names and codes as built (P-B1).**
  - Public `SCREEN_FORBIDDEN_MODULES`.
  - `render_bootstrap` refuses any parameter set other than exactly {prefix, forbidden_modules, stubs, entry_module, min_argv, launcher, journal_name_pattern}.
  - The screen's refusal codes are P7's codes with the prefix `SCREEN`: `SCREEN_FORBIDDEN_IMPORT`, `SCREEN_WRITE_REFUSED`, `SCREEN_FORBIDDEN_CALL`, `SCREEN_BOOTSTRAP_MISMATCH`, `SCREEN_TREE_DIRTY`, `SCREEN_UNAUDITED_EXEC`, `SCREEN_ORIGIN_OUTSIDE_ROOT`, `SCREEN_UNBOUND_BYTECODE`, `SCREEN_MODULE_ALIAS` and `SCREEN_SOURCE_CHANGED_DURING_RUN`.
- **Refusals inside library code.** Refusals also collect in `sys.p7_recorder.refusals`, because library code can swallow the exception. How `worker.py` checks them (before each PATH append and at exit), and the remaining write-path gaps (rename, link, truncate, third-party writers), are P-F obligations. The coordinator's P-F card note freezes them before P-F is dispatched.
- Coordinator–worker messages over stdin/stdout are internal to P-F and not frozen.

### §3.4 Run-directory formats (design §4.1)

- Run root `<private_root>/t00-step3/`; run directory `<run_root>/<authority_sha256>/`.
- **Locks:** `<run_root>/lock` (rows S5, S6) and `<run_dir>/lock` (the run lock). Content `canonical_json_bytes({"host": socket.gethostname(), "pid": os.getpid(), "schema": "t00_screen_lock/v1"})`, no trailing newline, rewritten at offset 0 by the holder after it takes the lock. The lock is `msvcrt.locking(fd, LK_NBLCK, 1)` on the byte at `journal.LOCK_OFFSET = 1 << 20`, beyond the content, so a reader can read the content while the lock is held (K-4). Row K4 holds when the run lock's `pid` is `os.getppid()`, its `host` is this host, and a non-blocking lock attempt on that byte fails.
- **Records** (every line of `ledger/*.jsonl` and `journal/*.jsonl`): `canonical_json_bytes({"body": {...}, "prev_sha256": <hex or null>, "type": <record type>}) + b"\n"`. A record's SHA-256 is that of its line without the LF (K-4). `prev_sha256` is the previous record's SHA-256 in the same file. A journal's first record has `null`; the first record of `ledger/NNNN.jsonl` chains to the last valid record of the highest earlier ledger file (`null` in `0001`). `NNNN` is four digits, 1 + the highest existing number (empty and torn files count). `ledger/0001.jsonl` opens with AUTHORITY_BOUND (row K4).
- **`manifest.json`:** `{authority_sha256, contract_sha256, p7_record_sha256, code_head, populations: {<population>: {indices, candidates_sha256}}, plan_sha256}` (K-4 keys). `acts/<act_sha256>.json`, `results.json`, `REPORT.md`, `attestation.json` and `errors/` are as in design §4.1.

### §3.5 `t00_screen.journal` (P-D; every name K-4)

- `Record = Mapping[str, object]` (a parsed record line); `Key = tuple[str, str, int]` (root, population, path index; design §7), a JSON list in bodies; `Cost = {cpu_s, wall_s}`; `Outcome = Mapping[str, object]`.
- `read(path, *, prev_sha256) -> tuple[Record, ...]`: verifies the chain from `prev_sha256`; drops only a torn final line (no LF, or an unparseable last line); any other break raises `JournalCorrupt` with code `CORRUPTION` (row S3).
- `append(fd, type, body, *, prev_sha256) -> str`: one `os.write` of the record line to an fd opened `O_WRONLY | O_APPEND | O_BINARY`, then `os.fsync`; returns the record's SHA-256.
- `read_lock(path) -> tuple[int, str]`: (pid, host); refuses another schema. `LOCK_OFFSET = 1 << 20`.
- `outcomes(journals, keys) -> tuple[Outcome, ...]`: for each plan key, the first valid PATH body without `wall_s` and `cpu_s`, sorted by key.
- `results(*, authority_sha256, contract_sha256, p7_record_sha256, plan_sha256, verdict) -> bytes`: the canonical bytes of `results.json`, where `verdict` is `t00_screen.verdict.as_json(...)`; no timestamp, W, approval or timing (row S16).

**Ledger bodies** (design §4.2):

| Type | Body |
|---|---|
| AUTHORITY_BOUND | `authority_sha256`, `prereg_path`, `approvals` (SHA-256 of each r3c and screen approval used), `reused_directory` (row S6) |
| PREPARED | `manifest_sha256`, `build: Cost`, `integrity: Cost` |
| PROBE_START, ALL_DONE | `{}` |
| PROBE | `path_cpu_s`, `path_wall_s`, `peak_memory_bytes` |
| SEGMENT_START (heartbeat 0) | `k`, `w`, `assignment_sha256`, `witness_keys`, `approvals` |
| HEARTBEAT | `wall_s`, `job_cpu_s` |
| SEGMENT_END | `class`, `cause`, `workers: [{worker, reason}]`, `wall_s`, `job_cpu_s`, `path_cpu_s`, `overhead_cpu_s`, `peak_memory_bytes` |
| SEGMENT_CRASHED | `k`, `charge: Cost`, `losses: [Key]`, `cap` (`null`, `RESOURCE_EXHAUSTED` or `IO_EXHAUSTED`; §3.6a F1) |

*Clarification 2026-10-03 (coordinator (3), card owner; reconciled to design §5.4 at `3742a95` :509):* a crashed segment's `charge` follows design §5.4 — the last heartbeat (SEGMENT_START is heartbeat 0) plus one interval of wall, and that heartbeat's `job_cpu_s` **plus one interval × W**, all as overhead — **less the `path_cpu_s` already booked to the path budget by that segment's PATH records** (row B4 books it once). The subtraction removes only the double count; unrecorded worker CPU and the interval × W margin stay charged, so a crash still only overcharges (design :509). Without it, one late crash in a day-long segment would charge a day of path CPU to the overhead reserve and HALT the run. P-F owns the computation (rows S11, B5; `test_B5`); P-D's `SEGMENT_CRASHED{charge: Cost}` schema is unchanged.
| HALT; TERMINAL | `code`, `from`; `code` |
| ACT | `act_sha256`, `act` (`TERMINATE` or `CONTINUE`) |
| AGGREGATED; REPORTED; FINAL | `results_sha256`; `report_sha256`; `attestation_sha256` |
| VERIFY_START; VERIFY | `n`, `keys`; `n`, `keys`, `match` |

**Journal bodies** (design §4.1):

| Type | Body |
|---|---|
| EPOCH_OPEN | `build: Cost`, `integrity: Cost`, `closure_sha256`, `guard_sha256` |
| KEY_START | `key` |
| PATH | `key`, `seed`, `path_sha256`, `bracket_status`, `runs: {r1, r2}`, `wall_s`, `cpu_s`. Each run: P7's projection names (`p7_driver.py:55-65`: `digest`, `sessions`, `fills`, `events_sha256`, `deadline_failure`, `consumed_intrabar_split_count`, `consumed_intrabar_splits_sha256`) plus `status`, `sessions_to_pass`, `failure_reason`, `kernel_outcome`. No P&L series |
| CANDIDATES | `populations: {<population>: {indices, candidates_sha256}}` |
| PROBE_RESULT | `path_cpu_s`, `path_wall_s`, `peak_memory_bytes` |
| EPOCH_CLOSE | `integrity: Cost`, `closure_match` |
| WORKER_STOP | `reason`, `key` (or `null`); always the last record |

### §3.6 `t00_screen.state` (P-D)

- `State` (K-4): frozen; `name` is a §4.2 state, plus AGGREGATED and REPORTED between COMPLETE/TERMINAL and FINAL; `halted_from` is the HALT's from state, else `None`.
- `advance(state: State, event: Record) -> State`; an event not allowed raises `IllegalTransition` with code `ILLEGAL_TRANSITION` (row S1). `fold(ledger: Sequence[Record]) -> State` applies `advance` from the initial state (K-4; I3).
- `classify(cause: str | BaseException) -> tuple[str, str]`: (class, code), class `STOPPED`, `HALTED` or `TERMINAL` per design §4.3; an unlisted cause gives (`HALTED`, `UNCLASSIFIED_ERROR`) (row S9).
- `check_record(ledger: Sequence[Record], journals: Mapping[str, Sequence[Record]], manifest: Mapping[str, object] | None, acts: Mapping[str, bytes], *, keys: Sequence[Key]) -> RecordCheck` (K-4 parameters), `journals` keyed by journal name and `acts` by file name. `RecordCheck(code: str | None, completed: frozenset[Key], losses: Mapping[Key, int])` (K-4): `code` is `None` or the first failure, TERMINAL `CORRUPTION`, `NONDETERMINISM` or `CODE_OR_ARTIFACT_DRIFT`, or HALTED `RESOURCE_EXHAUSTED` or `IO_EXHAUSTED` (rows K6, S10, S13, S14, the S15 gap clause, X3).

### §3.6a Coordinator interface freeze, 2026-10-03 (from the P-D review of `3dc5819`)

Coordinator (3), as card owner, freezes these points so that P-D and P-F build against one reading. Each keeps design §4 unchanged and closes an encoding the design left open.

- **F1 Crash at a cap (preserves design §4.2: SEGMENT_CRASHED → "IDLE, or HALTED if a cap is reached").** One record, no second write. SEGMENT_CRASHED carries a `cap` field: `null`, or the HALTED-class code `classify` gives when this crash makes a loss or I/O cap reached (row S10). `advance`: SEGMENT_CRASHED{cap: null} → IDLE; SEGMENT_CRASHED{cap: code} → HALTED with `halted_from = "IDLE"`. The coordinator computes `cap` at resume from the durable ledger and journals before writing the record, so no crash window leaves a durable IDLE at an exhausted cap. `check_record` recomputes the cap finding and returns CORRUPTION if `cap` disagrees. Recovery is the ordinary HALTED path: CONTINUE (Joshua's signed act) returns to IDLE with the cap reset (design §4.2 :374; rows S8, X3).
- **F2 Witnesses.** SEGMENT_START's `witness_keys` holds exactly `min(W, |completed|)` keys, each one in `completed` and tagged. Worker `i` (0-based) runs `witness_keys[i]` as its first KEY_START whenever `i < len(witness_keys)`. `check_record` enforces both rules; a witness mismatch is NONDETERMINISM (W5).
- **F3 Assignment.** Worker `i` receives `sorted(K − completed)[i::W]`, with K in the plan's canonical key order. `assignment_sha256 = sha256(canonical_json_bytes([[i, [key, …]] for i in range(W)]))`. `check_record` recomputes it and compares. The plan's canonical key order (design §7 "sorted canonically") is Python `sorted()` over `Key` tuples: by `root`, then `population` as strings, then `path_index` as an integer. It is not canonical-JSON byte order. P-E's `plan` emits K in this order, and the plan digest hashes `canonical_json_bytes` of K in this order.
- **F4 Append failure.** After `journal.append` raises, the writer appends nothing more to that file. A worker whose append raised exits without WORKER_STOP and reports `IO_ERROR` on stdout. The coordinator, still running, ends the segment with SEGMENT_END naming that worker with `reason: IO_ERROR` (design :397, W13). That is an I/O-error segment for row S10, and the worker's in-flight key also counts one loss. Only the coordinator's own ledger write error leaves the segment crashed (design :397). A crashed segment counts losses (design :399), and its only I/O evidence is a journal WORKER_STOP reason. P-D may also poison the file inside the process, keyed by `(st_dev, st_ino)`.
- **F5 Encodings.**
  - `ACT{TERMINATE}` alone moves the run to TERMINAL, with no extra TERMINAL record.
  - The bytes of `manifest.json` are `canonical_json_bytes(manifest)`.
  - The act file is canonical JSON `{act_b64, approval_b64}`.
  - A lock rewrite truncates the file to the content length.
- **F6 Journal names.** A name must equal `f"{prefix}{n}-w{i}.jsonl"`, with `n` and `i` decimal and without leading zeros. Uniqueness is on the full identity `(prefix, n, i)`: `c1-w0`, `s1-w0` and `v1-w0` are distinct. A duplicate `(prefix, n, i)` is CORRUPTION.
- **F7 Red record.** For a new module, RED evidence means `status: failed`, a non-zero `verification_exit_code`, `source_stable: true`, and every row FAILED with no ERROR. `completed` with exit 0 is required only for GREEN (`scripts/record_verification.py:299-300`).
- **F8 Caps at every boundary (row S10; design §4.2 SEGMENT_END "by the highest class").**
  - P-D exports `cap_finding(ledger, journals, *, keys, cause=None, reasons=()) -> str | None`. It returns the row S10 cap that is reached and not reset by CONTINUE: `RESOURCE_EXHAUSTED` if any key has three losses, else `IO_EXHAUSTED` if there have been three I/O-error segments with no new completed key, else `None`. A trailing open segment is closed with `cause` and the worker `reasons`; `cause=None` reads as a crash. `check_record` applies the same function at every SEGMENT_END and SEGMENT_CRASHED. P-F calls it to fill `SEGMENT_CRASHED.cap` at resume and to choose a SEGMENT_END cause.
  - SEGMENT_END: when a cap is reached, a cause whose class is below HALTED must be replaced by the cap code, so that segment stops HALTED. A cap-code cause with no matching cap reached is CORRUPTION.
  - A HALT whose code is a cap code requires that cap to be reached. A SEGMENT_START or ALL_DONE while a cap is reached is CORRUPTION.
  - **Both caps on one record:** the record carries `RESOURCE_EXHAUSTED`, and CONTINUE resets only that cap (design §4.5). Before any SEGMENT_START, the coordinator then appends `HALT{IO_EXHAUSTED, from: "IDLE"}`, and a second CONTINUE is needed. No cap is reset without its own act.

### §3.7 `t00_screen.verdict` (P-C; names other than the three design constants are K-4)

- `A5_TEXT_SHA256`, `A6_TEXT_SHA256` (values in §2.6), `A6_HORIZON_SESSIONS`, `A5_RULE_IDS = ("T00_A5/v1",)`, `MEDIAN_RULE = "LOWER_NEAREST_RANK_INF_INCLUDED"`; `section_text(blob: bytes, section: str) -> bytes`, `section` `"A5"` or `"A6"`, with the §2.6 spans.
- `evaluate(outcomes: Sequence[Outcome], parameters: Mapping[str, object], reasons: Sequence[str]) -> Verdict` (design §5.5).
- `Verdict = Insufficient | Labelled`, both frozen:
  - `Insufficient(reasons: tuple[str, ...], completed: Mapping[str, int])`: sorted distinct codes, and completed scored paths per population only (row V1);
  - `Labelled(label: str, tallies: Mapping[str, Mapping[str, Mapping[str, int]]], descriptive: Mapping[str, Mapping[str, int]])`: `label` is `GO-evidence`, `NO-GO-evidence-robust` or `NO-GO-evidence-UNDETERMINED-dependent` (design §5.6); `tallies` is assignment (`pessimistic`, `optimistic`) → population → #581 A5 counter → count, the counter names frozen in P-C's return; `descriptive` is population → {`consumed_split_paths`, `undetermined_paths`} (row V4).
- `as_json(verdict) -> dict`: `{"kind": "INSUFFICIENT", ...}` or `{"kind": "LABELLED", ...}` with the fields above. `journal.results` takes it; `finalize` prints `INSUFFICIENT` or the `label`.

A packet that needs a different signature stops and returns (§6).

## §4 — Hypothesis, integration order and head H

**H (build):** with P-A…P-F merged, every design §2.2 row A1–X6 has a red-on-base, green-on-build launcher record; the 2026-09-30 A1–A23 regression, `tests/ops/qualification`, `tests/ops/test_book_adapters_parity.py` and `.\fp.ps1 check` are green at H; and `git diff --name-only <pre-build base> H` touches no §2.2 forbidden file. **Reject if** any row test cannot be made red on its base, any row is green only with a forbidden edit, the sealed-method source hashes change (K7), or the forbidden-file diff is non-empty. **Revert trigger:** any 2026-09-30 regression test or existing qualification test changes outcome at H.

**Dependency graph:**

```
PR-1 #629 ─┬───────────────────────────────────────────► every packet
PR-5 card ─┘
PR-2 #581 (DRAFT, A5/A6 frozen) ─► P-C ─┐
P-B1 ───────────────────────────────────┼─► P-A ─► P-B2 ─► P-E ─► P-F ─► H
P-D ────────────────────────────────────┘           ▲
PR-3 #611 ──────────────────────────────────────────┘
PR-4 docs PR (§11 addendum) ───────────────────────────────────────────► H
```

**Merge order** (each as its own PR, opened by the coordinator, merged by Joshua after Codex clean at the exact head and CI green):
1. Wave 1, in parallel: P-B1, P-C, P-D (and P-E, P-F built but not merged, K-5).
2. P-A, rebased on P-B1, P-C and P-D.
3. P-B2, rebased on #611 and P-A.
4. P-E, rebased on P-B2.
5. P-F, rebased on all.
6. PR-4 may merge at any point before H.

**Definition of H:** the first `origin/main` commit that contains P-A, P-B1, P-B2, P-C, P-D, P-E, P-F, #611, PR-2 and PR-4, at which the coordinator's H check (§10) is green with cited launcher records. The coordinator records H's full 40-hex SHA in §8. Step 7 and step 12 run from a detached worktree at H (`core.autocrlf=false`, clean with `--untracked-files=all`); later commits on `main` do not move H. A fix to any P7-closure or screen file after H defines a new H and repeats §7 (design §8, §13 "Head drift").

## §5 — Forbidden moves (not authorized by this card)

- Any code before Joshua approves this card; any packet before its §0 prerequisites are recorded in §8.
- Any edit outside the packet's §2.1 footprint; any §2.2 forbidden file; any change to a sealed method's source, to `runner.py`/`bracket.py` semantics, to `SOURCE_REFUSALS`, to r3c's bytes or to the pinned key.
- Any real-source **screen** run: step 12 needs a ratified #581 and a signed screen authority, neither of which this card supplies.
- Any probe beyond the two recorded in design §6 (row G4), and any Monte Carlo.
- Any test or run that reads the real source, other than the §7 P7 re-run.
- Copying, committing or quoting Pine, ports, private values, account identifiers or P&L; passing any of them, or a `workdir` holding them, to GLM or any external service.
- An agent signing, generating, holding or touching an operator key, approval or act; enrolling a key; editing `SOURCE_SIGNING_KEYS`.
- Merging, opening PRs (coordinator only), pushing to `main`, editing #581's A5/A6 text, or ratifying anything.
- GLM for P-A, P-B1, P-B2, or for any ticket that touches trust, auth, private inputs or the P7 closure.

## §6 — Return taxonomy and stop conditions

Each packet returns exactly one status to the coordinator:
- **DONE:** every owned row red-on-base and green-on-build, regression unchanged, footprint clean.
- **DONE_WITH_CONCERNS:** all of DONE, plus a named non-row concern. A failed row is never this.
- **NEEDS_CONTEXT:** a missing fact, prerequisite, ruling or interface decision. Name it.
- **BLOCKED:** context-problem, capability-problem, scope-problem or plan-itself-wrong, with the exact obstruction.

The return carries: branch, base, head SHA; `git diff --stat` and `--name-only` (checked against §2.1); per row, the red and green `record.json` paths; regression records; concerns.

**Stop and return (do not work around):** a footprint or interface change is needed; a forbidden file would change; a row cannot be made red on the base; a hook or guard refuses an action; two failed corrections of the same issue; more than three review rounds each with two or more P1/P2 findings (coordinator adjudicates); a second writer on the branch. The coordinator's verdict per packet is RESOLVED (every owned row holds) or FALSIFIED (named rows fail).

## §7 — After H: the P7 re-run under a fresh source approval (design §8 step 7; A1 step 5)

This is the only real-source run this card admits, and it runs only after H is recorded.

1. **Precondition:** Joshua has answered design §12 item 9 (depth N), recorded in §8. Neither this payload nor the screen-authority payload is written before that answer; this brings design step 8's item 9 ahead of step 7, and the budgets stay at step 8. **Payload.** The coordinator writes the approval payload's canonical bytes (`contract.canonical_json_bytes`, no trailing newline) to `payload.json` in the private root, outside any worktree: `{schema: "qualification_approval_payload/v1", scope: "APPROVE_T00_SOURCE_CONTRACT", subject_sha256: <r3c digest>, contract_sha256: <r3c digest>, issued_at, expires_at, authority_class: "OPERATOR"}`. `expires_at` covers steps 7–12 plus `verify` at that N (design §12 item 10; r3c-a2 expires 2026-10-09T01:52:19Z). If N later changes and needs a longer window, Joshua signs a renewal over the same r3c bytes (design C2) before step 12. The signing packet shows Joshua the payload bytes, their SHA-256, scope, schema, subject and key ID `source:1ebae5d45bc51280` (row G5).
2. **Joshua signs**, in Git Bash; the agent never touches the key:
   ```bash
   sha256sum <payload.json>     # must equal the SHA-256 in the signing packet; do not open or edit the file
   openssl pkeyutl -sign -rawin -inkey <your key.pem> -in <payload.json> -out <payload.sig>
   ```
3. **Assemble and verify.** The coordinator builds `{schema: "qualification_approval/v1", payload, signature: {algorithm: "Ed25519", key_id: "source:1ebae5d45bc51280", value_b64: base64(payload.sig)}}` as canonical JSON and verifies it with `contract.verify_detached_approval` (`allow_test_authority=False`) before use.
4. **One P7 re-run at H** under that approval, from the detached H worktree, by the accepted P7 procedure ([P7-closure packet](2026-09-24-tradeify-t00-p7-closure.md) §7, step-1b re-run). Its closure covers `production_source.py` and `p7_evidence.py` at H.
5. **`t00_screen accept-p7`** (coordinator, per §12 item 11; or Joshua himself to close the §13 residual) → record R and `p7_acceptance.json` in the private root. Public return: R's SHA-256, the acceptance SHA-256, H, closure MATCH and R1/R2 digest MATCH labels only.

The screen-authority signature (design §8 step 11) uses the same template with `scope: "APPROVE_T00_SCREEN_AUTHORITY"` and `subject_sha256 = contract_sha256 =` the authority SHA-256, under the same depth-N precondition. It is outside this card.

## §8 — Approval, prerequisites and H record

- Card approval (design §8 step 5): **APPROVED** by Joshua at `079b1b6`, 2026-10-03, directly to coordinator (3): "I approve of the recommendations, let's make it happen" (sheet 5; recorded at https://github.com/Joshua-Asante/first-passage/pull/634#issuecomment-5965354454). Coordinator (3) clarification at `143836d` (crash-segment charge; consistent with design §5.4). Depth N (design §12 item 9): ~~1,000 per population (sheet 5)~~. **Revised to 5,001 per population (1,667 per root)** by Joshua 2026-10-03, about 17:19Z, directly to coordinator (3): "I approve your recommendations", in reply to "Depth N: 5,001 recommended, against your 1,002". This follows the precision packet (`claude/t00-depth-decision-packet`, `90e2587`). At 1,002 (334 per root, the three-root layout's rounding of 1,000), the wrong-side risk at ±0.5 pp was about 24%; at 5,001 it is about 5%. The budgets (§5.4) and approval windows (§12 item 10) are set at design §8 step 8 for this N.
- PR-1 #629 merged at: `ad48cd5b059680f08f65a8e401c56a4ac66de609` (2026-10-03; relay CLEAN at `3742a95`, carried to `4f781a0`).
- PR-2 #581 merged (DRAFT, A5/A6 frozen) at: `b996803eb598bc5723652aafe12098782069f07b` (2026-10-03; relay CLEAN at `3b706c9`, pinned head `6ff2fb3`; pre-registration blob `6e6e5894b499fea8e16352415bab2f468488e91d`). A5/A6 section hashes recomputed by coordinator (3) at that merge commit: A5 `a8f6f25e025a2e136e477580b7e569531d770a1e35e712b72f5a6b9b50eb391b`, A6 `b3bdc77baf3e6383f1df08afd2f0fbb8a7c930d95a0f56b0c5669a5e18b217d9` — both MATCH §2.6.
- PR-3 #611 merged at: `f5b0f6ae4b615275b430f300080345949aa2e802` (2026-10-03; pinned `0d72f00`; recorded by coordinator (4), 2026-10-04).
- PR-4 docs PR merged at: —
- Packet heads (recorded by coordinator (4), 2026-10-04):
  - P-B1 (#650): accepted at `0b4b560` (coordinator (3)); merged `6e2ece62af2f6059cf37afa82728ff9068dacfd5` (pinned `43b09f6`).
  - P-D (#643): K-5 re-taken on `740f392` (includes #611); accepted at `0866dff`; merged `f7a4e53042042d7a8d44b0b69ce458f47e43e805` (pinned `a6cb6a5`).
  - P-C (#646): K-5 re-taken on the future base `740f392` + P-D (tree `4b48cad6`); accepted at `e473c5f`; merged `f9099a2bdea9b7833b85a9fc706ff7a86a192000` (pinned `e473c5f`).
  - P-A, P-B2, P-E, P-F: —.
- **K-4 ruling, row A8 values-block format (coordinator (4), card owner, 2026-10-04; raised by the P-A build as NEEDS_CONTEXT, since neither the design, this card nor #581 froze it):**
  - #581 §6 holds exactly one fenced block whose opening line is three backticks immediately followed by the info string `t00-step2-values/v1`, containing one line equal to `canonical_json_bytes(parameters)`.
  - Each active #581 §3 item's last cell reads exactly ``values block: `k1`, `k2` `` with this key map: item 1 → `depth_per_root`, `budget`; 2 → `pass_floor_halves`; 3 → `deadline_only_is_bust`; 4 → `rng`, `block`, `path_start_date`; 5 → `run1_diagnostic`; 7 → `scenarios`; 8 → `a5_rule`.
  - **PR-4 and #581's step-5 ratification follow this format.** They are the operator-visible surfaces, and Joshua ratifies #581 at step 5. P-A's §2.3 dependencies (PR-1, PR-2, PR-5, P-B1, P-C, P-D) are now all met; P-A is dispatched from `f9099a2` or later.
- **T00 threat model (RULED 2026-10-04: Joshua said "adopt all" in the merge agent's chat, then confirmed directly to coordinator (4), "confirm adopt all").** The T00 screen's integrity checks guard against code or artifact drift between launch and epoch close. They do not defend against an active writer to the interpreter, the venv or the run directory during a run. That is excluded by operating conditions: an attended host, with the Python install and venv read-only for the run's duration. Review findings that assume such a writer are out of scope and are closed by citing this statement.
- **H blockers** (coordinator (4), card owner, 2026-10-04; from the P-A reviews on #672). Each must be closed before H, either fixed (and merged, when the fix needs code) or accepted by Joshua as a named residual. Step 12 (the real screen run) cannot start while any is open:
  - **R-REC-1 — recorder reload overwrite.** `p7_evidence.py`'s recorder overwrites `third_party[name]` (`:332-333`) and `ports[filename]` (`:144`) on every load or compile. A recorded third-party module or port reloaded A→B→A inside one epoch executes B and still closes matching, against K6 (design `:151`). First-party is already refused (`:270-272`). Fix: a recorder follow-up packet under this card, in P-B1's scope, that refuses a re-digest, with red and green tests. #672 comment 5983384629.
  - **R-REC-2 — file-backed stdlib bytes unbound** (Codex r4178909762 on #672). The recorder keeps stdlib names only (`:335-336`), and the interpreter binding does not hash stdlib files. Changed stdlib Python or extension bytes could execute and close matching. **Needs Joshua's approval:** the frozen source-only design defines stdlib modules as name-only entries, so recording their bytes and binding them in P7 is a schema change, not a bounded follow-up. Until he approves a schema change (or accepts this as a named residual), H stays blocked. P-A cannot edit those files.
    - **RULED 2026-10-04T20:30:58Z** (Joshua, directly to coordinator (4): "approve the recommendations"), as revised after the scrutiny and C5's source check. **A base-install digest** (`pythonXY.dll`, `Lib/**` and `DLLs/**`, including `__pycache__`) goes into the P7 `interpreter` binding. It is checked **at launch and again at every epoch close**. The follow-up packet must prove the close-time check with a regression in which a stdlib file changes after the epoch opens. Per-module stdlib digests are not used. The packet goes with R-REC-1 (the recorder packet), and the P7 re-run at H (card §7) picks it up.
  - **R-INT-2 — cross-epoch closure equality** (Codex r4178909759 on #672). Design K6 (`:151`): "all epochs record the same closure". Valid lazy imports within an epoch do not relax that: completed epochs must have **equal final closure digests**. `t00_screen/state.py` collects only `EPOCH_OPEN.body.closure_sha256`. **Needs Joshua's approval:** §3.5 freezes `EPOCH_CLOSE` to exactly integrity plus `closure_match`, and §6 forbids changing it as an ordinary P-D or P-F follow-up. Carrying the final closure digest in `EPOCH_CLOSE` and comparing it across epochs is a frozen-interface change that needs his approval (or a design-authority ruling). No weakening of K6 meanwhile; H stays blocked.
    - **RULED 2026-10-04T20:30:58Z: an operator DESIGN AMENDMENT to K6** (Joshua, "approve the recommendations"). K6's "all epochs record the same closure" is amended to **per-module digest agreement across epochs**: `EPOCH_CLOSE` carries the full final closure, and `check_record` refuses any module that appears with two different rows across epochs. Final closures may otherwise differ (the probe shares the candidate's process, and verify workers take different paths). This amends §3.5's `EPOCH_CLOSE`. The rule names the journals it covers. Built in the same P-D follow-up packet as R-INT-1. **Covered journals (card owner, 2026-10-04):** all of them: candidate `c` (including the probe), segments `s` and verify `v`. **P-D follow-up footprint (authorized, card owner; Codex r4179244515 on #677):** `ops/c1_rail/qualification/t00_screen/state.py` (the R-INT-1 re-verification and the cross-epoch rule), `ops/c1_rail/qualification/t00_screen/journal.py` (the `EPOCH_CLOSE` schema gains the final-closure field, the amendment Joshua ruled at 20:30:58Z), and their tests. Nothing else.
  - **R-REC packet: scope, footprint and required attack classes** (coordinator (4), card owner, 2026-10-04; on Codex r4179226763, r4179226768 and r4179226773 on #677). The card records Joshua's approvals and authorizes the packet. It does **not** carry the packet's design, which gets its own red-first build, its own Codex review and coordinator acceptance.
    - **Footprint (authorized):** `ops/c1_rail/qualification/p7_evidence.py` (the recorder and the P7 `interpreter` binding), `ops/c1_rail/qualification/screen_authority.py` (the close-time check against that binding), and their tests. Nothing else. It merges after P-A.
    - **Attack classes the packet must close, each with a red test plus a passing twin:**
      - (1) A→B→A reload of a recorded third-party module or port (R-REC-1).
      - (2) Changed `pythonXY.dll`, `Lib/**`, `DLLs/**` or `__pycache__` bytes, **and the operations venv's site-packages tree** (RULED 2026-10-04, "adopt all" (i)), at launch and again at every epoch close. One tree digest in the P7 `interpreter` binding, with no per-module digests (R-REC-2 as approved).
      - (3) ~~Transient stdlib replacement within an epoch: changed, loaded and restored before close.~~ **Accepted as a named H residual** (RULED 2026-10-04, "adopt all" (ii); Codex r4179226768): a within-epoch swap-and-restore of a stdlib or site-packages file. Operational guard: the install and venv are read-only for the run's duration. Out of scope under the threat model.
      - (4) A first-seen third-party module whose site-packages file changed after launch but before its first import. This is closed by (2)'s venv tree digest, checked at close (r4179226763).
      - (5) Directly executed installed source via `runpy.run_path` or `exec(compile(...))` of an absolute site path (R-REC-3).
    - **Approval boundary:** class (5) and anything beyond (2) go beyond what Joshua approved. If closing any of them needs more than the authorized footprint or a further schema change, the packet returns to Joshua before building it.
  - **R-INT-1 — stored act approvals are not authenticated in the durable record check** (Codex r4178909767 on #672; confirmed: `state.py:277-286` checks only canonical base64, the file name against the act-bytes hash, and the act's authority, kind and ledger head, with no signature check). The signed subject stays `sha256(act_bytes)`. **This card prescribes no fix design.** Any fix that persists new evidence (for example an acceptance time) or changes the ACT body `{act_sha256, act}` or the act file `{act_b64, approval_b64}` changes §3.5's frozen interfaces, and a time held only in the local hash-chained ledger is not trusted evidence. **Joshua's decision**, among options the R-INT-1 packet presents with their trade-offs:
    - (a) an operator-countersigned acceptance record;
    - (b) re-verify the detached signature over the act bytes on every check, with validity enforced only at first acceptance and no persisted time;
    - (c) an approved §3.5 schema extension;
    - (d) accept the gap as a named residual.
    Until he decides and the chosen fix lands, or he accepts the residual, H stays blocked.
    - **RULED 2026-10-04T20:08:51Z: option (b), strict form.** Joshua, directly to coordinator (4): "Go with your best recommendation on R-INT-1" (the recommendation put to him was the strict form; it was also relayed through the merge agent's chat).
      - The durable record check (`t00_screen/state.py`, `_check_acts`/`check_record`) re-verifies each stored act's detached approval (`approval_b64`) on **every** check, by calling the existing `contract.verify_detached_approval(..., now=<real current time>, allow_test_authority=False)`.
      - There is no first-acceptance exception and no persisted acceptance time. §3.5's ACT body `{act_sha256, act}` and act file `{act_b64, approval_b64}` are unchanged, and `contract.py` is not edited.
      - An expired act fails closed. **There is no post-window re-audit** (Joshua, 2026-10-04T20:30:58Z, "confirm option 1", on Codex r4179166719): a completed run cannot be re-verified after its approval window, and there is no renewal store. §3.5 and X3 are unchanged, and the act file stays create-once at `acts/<act_sha256>.json`. Approval windows must be sized to cover every check the run needs, through `verify`.
      - **K-4 (card owner, corrected after Codex r4179166715):** `check_record`'s existing `keys` parameter is `Sequence[journal.Key]` (the screen-plan keys), not the trusted public keys. `check_record` gains two keyword-only parameters: `trusted_keys: Mapping[str, contract.TrustedApprovalKey]`, the pinned set passed to `verify_detached_approval`, and `now: datetime`.
      - **Named residuals, accepted:** (1) a genuinely operator-signed act that was never recorded can still be inserted late, but only inside its own signed validity window and only at the ledger head it names; (2) a run cannot be re-audited after its approval window (option 1).
      - **Rejected:** (a) countersignature (a new record type), (c) schema extension (a stored time is not trusted evidence), (d) an unrestricted residual.
      - **Fix packet:** a P-D follow-up (`state.py` plus its tests), red-first with forged-approval, expired-act and valid-act cases. Owner: coordinator (4). R-INT-1 closes when it merges.
- **P-F obligations added by the P-A, P-D, R-REC and P-B2 builds** (coordinator (4), 2026-10-04; also for the P-F card note):
  - P-F passes `check_record` the pinned, lifecycle-checked `source:` key set as `trusted_keys`, plus `now` (#678).
  - It keeps each epoch's `ProductionSource` alive until close (P-A holds it weakly; garbage collection makes the close fail).
  - It writes `EPOCH_CLOSE` with the full `closure` from `ScreenEpochClose.closure` (#678/#680).
  - It adds its `scripts/` label script to the A10b consumer scan, which today covers `ops/` only (#679).
- H: —
- Design §12 item 9 (depth N) answered by Joshua (precondition for §7 step 1): —
- ~~Still open outside this card: #581 OD-1/OD-2 direct confirmation (design §12 item 3).~~ *2026-10-03:* confirmed directly by Joshua (sheet 4 item 3, "all recommended"; #629 approval comment 5965049542). This card merged as #634 at `cdbf597b2ef2c7b4e32ae4af476e3a392f75ca79`.

## §10 — Audit hooks

```bash
# Card form and authority (expect RESULT: well-formed; exit 0).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md

# Design identity this card binds (expect 3742a95... at #629's head until it merges).
gh pr view 629 --json headRefOid -q .headRefOid

# Per packet, at return: footprint = its §2.1 row exactly.
git diff --name-only "$(git merge-base origin/main HEAD)" HEAD

# P-E/P-F (O-10): expect only ALLOWLIST entry lines naming c1_rail/qualification/t00_screen/ owners.
git diff -U0 "$(git merge-base origin/main HEAD)" HEAD -- tests/ops/qualification/test_source_consumers.py

# P-F: the generated scripts table is current (expect exit 0); REPO_MAP.md changes only inside it.
python -I scripts/fp.py python scripts/check_repo_map_scripts_table.py --check

# The A5/A6 values P-C pins (expect a8f6f25e...391b then b3bdc77b...17d9).
git show 438b659:docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md | python -c "import sys,hashlib;b=sys.stdin.buffer.read();i=lambda m:b.index(m)+1;a5,a6,s3=i(b'\n### A5'),i(b'\n### A6'),i(b'\n## \xc2\xa73');print(hashlib.sha256(b[a5:a6]).hexdigest(),hashlib.sha256(b[a6:s3]).hexdigest())"

# At H: forbidden files untouched by the build (expect no output). BASE = the pre-build origin/main SHA in §8.
git diff --name-only "$BASE" "$H" -- ops/c1_rail/qualification/{contract,trust_domain,runner,provider,blocks,paths,regime,bracket,model,replay}.py ops/c1_rail/book_policy.py ops/c1_signal_daemon/book_adapters.py core/

# At H: P7 forbids the screen; A10b scans the new capabilities.
rg -n "c1_rail.qualification.screen_authority|c1_rail.qualification.t00_screen" ops/c1_rail/qualification/p7_evidence.py
rg -n "screen_bracket|screen_epoch|_replay_raw|_engine" tests/ops/qualification/test_source_consumers.py

# At H: the screen seed tag never enters regime.py (expect 0).
rg -c "t00-screen-rng" ops/c1_rail/qualification/regime.py || echo "0 (expected)"

# At H: full regression, each with its record.json.
python -I scripts/fp.py --workers 2 python -m pytest tests/ops/qualification tests/ops/test_book_adapters_parity.py -q
python -I scripts/fp.py check

# No private value in this card (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md | grep -v 'rg -n'
```

## Pre-mortem

- **Most likely failure:** a packet needs an interface outside §3 (most likely P-B2 against `_engine`/`_quotes` after #611's re-anchoring). It stops at §6; the coordinator amends §3 here with Joshua's approval if behaviour changes.
- **What makes it moot:** a change to the design after approval; #581 ratified with different A5/A6 bytes (the build repeats from P-C); r3c lapsing before step 7 without a renewal.
- **Cost:** seven packet PRs, one P7 re-run (about 6 minutes wall, design §6.1), one signature.
