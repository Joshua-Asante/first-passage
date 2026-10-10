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

r3c's `SOURCE_REFUSALS` include `SCREEN` and `MONTE_CARLO`; there is no step-3 runner (design §1). The design adds a second, separately signed door: a `t00_screen_authority/v1` document signed under `APPROVE_T00_SCREEN_AUTHORITY`, a gated `screen_authority.screen_epoch`/`screen_bracket` scored by the unchanged `runner.evaluate_replay`, and a ledgered, resumable driver. This card turns design §9 and §9.1 into packets with disjoint write footprints, red-first tests per §2.2 row, and an integration order ending at head H, where A1 step 5 (one P7 re-run) happens.

## §2 — Claim manifest and packets

### §2.1 Claim manifest (write footprints; every path under the repo root)

| Packet | Writes (exactly) | Rows owned (count) |
|---|---|---|
| P-A | `ops/c1_rail/qualification/screen_authority.py` (new); `tests/ops/qualification/test_screen_authority.py` (new) | A1–A11, K1–K4, X2, X3 (17) |
| P-B1 | `ops/c1_rail/qualification/p7_evidence.py`; `tests/ops/qualification/test_p7_evidence.py` | K10, S2 (2) |
| P-B2 | `ops/c1_rail/qualification/production_source.py` (`_verify_identity`, `_consumed_splits`); `ops/c1_rail/qualification/screen_authority.py` (`screen_epoch`, `screen_bracket` only; amendment PB2-1); `tests/ops/qualification/test_production_source.py`; `tests/ops/qualification/test_source_consumers.py` | K5–K9 (5) |
| P-C | `ops/c1_rail/qualification/t00_screen/verdict.py` (new); `tests/ops/qualification/test_t00_screen_verdict.py` (new); `t00_screen/__init__.py` (K-3 bytes) | V1–V4 (4) |
| P-D | `t00_screen/state.py`, `t00_screen/journal.py` (new); `tests/ops/qualification/test_t00_screen_state.py` (new); `t00_screen/__init__.py` (K-3 bytes) | S1, S3, S9, S10, S13, S14, S16, B1 (8) |
| P-E | `t00_screen/plan.py` (new); `tests/ops/qualification/test_t00_screen_plan.py` (new); `t00_screen/__init__.py` (K-3 bytes); only if `plan.py` has an A10b finding, `tests/ops/qualification/test_source_consumers.py`, limited to ALLOWLIST entries for P-E's own (owner, capability) pairs and written after P-B2 merges (O-10) | R1–R3 (3) |
| P-F | `t00_screen/coordinator.py`, `worker.py`, `__main__.py` (new); `scripts/t00_screen_label_check.py` (new); `scripts/t00_screen.py` (new; amendment PF-2); `tests/ops/qualification/test_t00_screen_driver.py` (new); `t00_screen/__init__.py` (K-3 bytes); `tests/ops/qualification/test_source_consumers.py`, limited to ALLOWLIST entries for P-F's own (owner, capability) pairs and, under the P-F card note item 8, the bounded scan extension it names (the label script scanned, its owners resolved from the repository root, and one regression), written after P-B2 merges (O-10); `REPO_MAP.md`, limited to the generated scripts-table block produced by `python scripts/check_repo_map_scripts_table.py --write` | S4–S8, S11, S12, S15, B2–B5, X1, X4–X6 (16) |
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
| O-10 | A10b's meta-test (`test_source_consumers.py:195-202`) refuses an ALLOWLIST entry whose owner is missing or uses no capability, so P-B2 cannot pre-allowlist P-F's `screen_epoch`/`screen_bracket` calls or a `.contract` load (`CAPABILITY_ATTRIBUTE`) | P-F, and P-E only if `plan.py` has a finding, adds ALLOWLIST entries for its own (owner, capability) pairs only, after P-B2 merges; the capability owners are frozen in §3.2; P-F also makes the bounded scan extension of P-F card note item 8; any other edit to the file is a manifest violation |
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
- **Writes:** `production_source.py` (`_verify_identity`, `_consumed_splits` only), `screen_authority.py` (`screen_epoch`, `screen_bracket` only; amendment PB2-1), `test_production_source.py`, `test_source_consumers.py` (allowlist keyed by (owner, capability); `screen_bracket`, `screen_epoch`, `_replay_raw`, `_engine` added to the scan).
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
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/coordinator.py`, `t00_screen/worker.py`, `t00_screen/__main__.py` (`preflight`, `accept-p7`, `run`, `resume`, `finalize`, `verify`, `act`), `scripts/t00_screen_label_check.py`, `scripts/t00_screen.py` (amendment PF-2), `test_t00_screen_driver.py`; ALLOWLIST entries in `test_source_consumers.py` for its own (owner, capability) pairs and, under the P-F card note item 8, the bounded scan extension it names (the label script scanned, its owners resolved from the repository root, and one regression), after P-B2 merges (O-10); the scripts-table block of `REPO_MAP.md`, regenerated by `python scripts/check_repo_map_scripts_table.py --write` and changed nowhere else.
- **Builds:** run and run-root locks (§3.4), O_EXCL run directory, ledger-only writer, Job Object (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, suspended → assigned → resumed), pinned worker environment, budget gate and overhead reserve, probe sequencing, fixed console lines (§5.6), `verify` with k = 9 hash-derived re-executions inside the K3/K4 gate, `accept-p7` writing `p7_acceptance.json`, the worker command and journal names (§3.3), `worker.open_epoch` and `worker.bracket` as the only capability callers (§3.2), and `finalize` under the run lock from COMPLETE or TERMINAL only (`FINALIZE_NOT_COMPLETE`), calling `check_record` (O-11). The label script imports nothing from `t00_screen.verdict` (X5) and is written without reading P-C's implementation.
- **Red-first tests:** `test_S4`…`test_S8`, `test_S11`, `test_S12`, `test_S15`, `test_B2`…`test_B5`, `test_X1`, `test_X4`, `test_X5`, `test_X6`; integration I1 (every §4.4 crash window), I2 (Ctrl-C through `fp.ps1` and resume; lands as PF-3 says, note item 16), I3 (every ledger prefix folds to its durable state). Real subprocess workers, deterministic fake source, TEST_ONLY seam only.
- **Lane:** CC integration.
- **Depends on:** P-A, P-B1, P-B2, P-C, P-D, P-E merged.
- **Return:** §6, plus the revision-2 test map (design §10) checked off.
- **P-F card note** (coordinator (4), card owner, 2026-10-05; from coordinator (3)'s draft items 1–8 plus the §8 obligations; P-F is dispatched pinned to the card head that carries this note):
  1. **Pinning.** The P-F ticket cites this card at the commit carrying this note and `origin/main` at dispatch. P-A, P-B1, P-B2, P-C, P-D, P-E and R-REC are merged (`164e17b`), so no stand-in modules are needed.
  2. **Test seam.** The P7 precedent: a TEST_ONLY code root (`test_p7_evidence.py`, the TEST_ONLY root fixture) plus a real `ProductionSource` over synthetic `composition_fixture` artifacts. `worker.py` has no fake-source hook.
  3. **Entry points (amendment PB2-1).** `worker.open_epoch` calls `screen_authority.screen_epoch(source, *, authority)` and `worker.bracket` calls `screen_authority.screen_bracket(source, path, *, authority, epoch)`; both refuse a non-`ProductionSource`. They are the only callers (§3.2). P-F's ALLOWLIST entries name those two worker owners.
  4. **I/O causes.** When SEGMENT_END's cause is IO_EXHAUSTED, `workers[].reason` keeps the worker's IO_ERROR; a cap code is never its own I/O evidence. A worker append failure ends the segment with that worker's reason IO_ERROR; only the coordinator's own write error is a crash (F4).
  5. **Caps.** An INTERRUPTED segment that reaches the I/O cap counts its in-flight keys as losses (accepted as conservative). P-F calls `state.cap_finding` to fill SEGMENT_CRASHED.cap and to choose SEGMENT_END's cause (F8), **iterating to a fixed point**: call it with the segment's provisional cause, then again with the returned cap as `cause`, until the result is stable, and write that result, **only when `classify(provisional)` is STOPPED** (F8: a cap replaces only a cause whose class is below HALTED). A HALTED or TERMINAL provisional cause, item 11's `UNCLASSIFIED_ERROR` included, is written unchanged, and its `cap_finding` call uses that cause; if a cap is then reached but unwritten, the coordinator appends `HALT{cap}` before any SEGMENT_START (F8: SEGMENT_START and ALL_DONE are CORRUPTION while a cap is reached). Driver cases cover both: the INTERRUPTED sequence below, and a TERMINAL cause at a reached cap that stays TERMINAL. A single call can return `IO_EXHAUSTED` for an INTERRUPTED segment whose losses, once closed as `IO_EXHAUSTED`, reach `RESOURCE_EXHAUSTED`; `check_record` would then refuse `CORRUPTION`. A driver case covers that sequence. At finalize, a HALTED cap code that `check_record` reports on a TERMINAL run is informational; only TERMINAL-class codes are appended as failures.
  6. **`check_record`.** P-F passes the pinned, lifecycle-checked `source:` key set as `trusted_keys`, plus `now` (#678). An expired act fails closed (R-INT-1).
  7. **Epochs.** P-F keeps each epoch's `ProductionSource` alive until its close (P-A holds it weakly) and writes `EPOCH_CLOSE` with the full `closure` from `ScreenEpochClose.closure` (#678, #680; K6 as amended).
  8. **A10b scan (scope amended; bounded).** `test_source_consumers.py` scans one root, `ops/`, and resolves owners as `OPS / relative`. P-F may change exactly three things in it: (a) also scan the single file `scripts/t00_screen_label_check.py`, naming its owners relative to the repository root (`scripts/t00_screen_label_check.py:<function>`, the form `test_K9` uses); (b) the matching meta-test handling for that one file (its findings in the `flagged` set and its owner path resolution); (c) one regression test showing the script is scanned (a planted capability use in it is found). No other change to the scan logic or the meta-test. This amends §2.1, §2.9 *Writes*, O-10 and §10 for P-F.
  9. **No mutable module state.** No `t00_screen` module (coordinator.py, worker.py and __main__.py included) holds mutable module-level state: any in-process `c1_rail.qualification.*` module is re-executed and compared by `result_adjudication` (P-D's `_REFUSED` broke 12 phase3 tests). Probe: run the new tests, then `tests/ops/test_phase3_provenance_acceptance.py`, in one `-n 0` process.
  10. **CI budget.** New tests land in the sharded qualification children (#684); a child that nears its cap is a finding, not a reason to raise it.
  11. **Refusals inside library code (§3.3).** The worker reads `sys.p7_recorder.refusals` immediately before each PATH append and before WORKER_STOP. If it is non-empty, the worker appends no PATH. Its last record is WORKER_STOP with `reason` set to the first recorded refusal's code (the text before the first `:` of the recorder entry, `p7_evidence.py:116`) and **`key: null`**, so that the in-flight key stays in flight and counts as a loss (`state._segment_keys` clears an in-flight key only when WORKER_STOP names it). The worker then exits non-zero. The coordinator ends the segment with SEGMENT_END naming that worker with that reason; SEGMENT_END's `cause` is `state.classify(code)[1]`, so an unlisted `SCREEN_*` code is recorded as `UNCLASSIFIED_ERROR` (HALTED). No refusal is ever cleared.
  12. **Remaining write paths (§3.3).** As its first statements, before importing anything outside the standard library, `worker.py` installs a second audit hook. The bootstrap is unchanged, so `SCREEN_BOOTSTRAP_SHA256` is unchanged. The hook raises `SCREEN_WRITE_REFUSED` on, and records into `sys.p7_recorder.refusals`, the events `os.rename` (which covers `os.replace`), `os.link`, `os.symlink`, `os.truncate` with a path argument (an fd argument is covered by that descriptor's own open check), `os.remove` (which covers unlink), `os.rmdir`, `os.mkdir` and `shutil.rmtree`. If a real import chain turns out to need one of them (the CA-1 precedent), that is a stop (`NEEDS_CONTEXT` to the card owner), never a silent allowance. **Residuals under the §8 threat model** (drift between launch and epoch close, not an active writer; read-only install and venv), not hooked: third-party native writers; child processes (`subprocess.Popen`, which CA-1's `platform` path needs); and `_winapi.CreateFile`/`CreateJunction`. In addition, `finalize` refuses `CORRUPTION` if `run_dir/journal` holds any file the ledger does not name, and every journal is chain-verified by `journal.read`. **Tests** (P-F's own, in `test_t00_screen_driver.py`; not row S2, which is P-B1's): `test_worker_write_path_<event>` for each event above, a real-import smoke run of the worker under the hook, and a finalize case with a planted extra journal file.
  13. **Amendment PF-1, the worker's argv[0] (coordinator (4), card owner, 2026-10-05; P-F worker return).** On Windows under a venv, `sys.executable` is the venv redirector, which starts the real interpreter as its own child. The worker's `os.getppid()` is then the redirector, never the coordinator, so K4 (§3.4, the run lock's `pid` is `os.getppid()`) can never hold. Amended: the §3.3 command's first element is `sys._base_executable` when `os.name == 'nt'` and it differs from `sys.executable` (the Windows venv redirector case), with `__PYVENV_LAUNCHER__` set to `sys.executable` in the pinned worker environment; otherwise it is `sys.executable` (on POSIX, a venv's `sys._base_executable` is the base interpreter, and `__PYVENV_LAUNCHER__` is ignored). The interpreter consumes and deletes `__PYVENV_LAUNCHER__`, so no worker-side check of the pinned environment may expect it. Inside the worker, `sys.executable` (and so the bootstrap's venv derivation, `p7_evidence.py:261`, and the interpreter binding, `:639-640`) is unchanged, and its parent is the coordinator, which holds the lock. K4 is not weakened. A driver test asserts the worker's `os.getppid()` equals the coordinator's pid.
  14. **Amendment PF-2, the operator entry point.** `fp.py` runs from the repository root and strips `PYTHONPATH`, so design §5.1's `fp.ps1 python -m c1_rail.qualification.t00_screen …` cannot import `c1_rail`. Amended: P-F adds `scripts/t00_screen.py`, a thin entry point following the repository's per-script `sys.path` shim convention (`pyproject.toml:34-37`). It puts the `core` and `ops` layer roots on `sys.path` with the shared helper `scripts/layer_bootstrap.add_layer_roots('core', 'ops')` and calls `runpy.run_module('c1_rail.qualification.t00_screen', run_name='__main__', alter_sys=True)`, with no other logic and no capability use. The operator command is `.\fp.ps1 python scripts/t00_screen.py <preflight|accept-p7|run|resume|finalize|verify|act> …`, and I2 drives it.
  15. **Card-silent choices confirmed (card owner, 2026-10-05):** (a) a non-terminal, non-lapse stop in BOUND is HALT `UNCLASSIFIED_ERROR`; (b) a COMPLETE provisional cause goes through item 5's cap check as a STOPPED cause does; (c) overhead counts PREPARED's cost (the candidate worker's build, its candidate pass and the candidate epoch's integrity), each probe's path CPU and epoch costs, each segment's `overhead_cpu_s` (job CPU less booked path CPU) and each crash charge; (d) candidate journals are `c1-w0`, `c2-w0`, … with no gap; (e) an unnamed or unreadable journal file at `finalize` is TERMINAL `CORRUPTION` (item 12).
  16. **Amendment PF-3, Ctrl-C under `fp.ps1` (coordinator (4), card owner, 2026-10-05; P-F worker observation, raised by the deployment coordinator).** Design :400, :428 (W15), :684 (I2), :746, :788 and :858 assume that Ctrl-C under `fp.ps1` is a hard kill of the coordinator (W22). On the Windows venv, `fp.py`'s kill 0.25 s after the interrupt (`scripts/fp.py:274`, `:330`) reaches its own child, the venv redirector, not the coordinator interpreter behind it (PF-1). The coordinator receives the same Ctrl-C and stops as design :400 says a directly run coordinator does: SEGMENT_END STOPPED `INTERRUPTED`, in-flight keys not losses. **Amended:** I2 asserts that observed path. After Ctrl-C through the launcher, the ledger ends in SEGMENT_END `INTERRUPTED`; after that SEGMENT_END and the run lock's release, no coordinator or worker process for the run survives, checked by the coordinator's PID and the Job Object (busy workers finish their in-flight keys, so the coordinator outlives the launcher until its segment ends); and resume completes with the same results. **Operator note:** the launcher's prompt returns while the coordinator may still be finishing its segment; a `resume` in that window is refused by the held run lock (W14, design :427). Evidence: the P-F `test_I2` on the operator's venv, Python version recorded in its launcher record; a different Python build whose redirector ties its child's life to its own would land as W22, which test_S12 and I1[W22] cover. W22 itself stays exercised by `test_S12` and I1[W22]. The design's "Ctrl-C under `fp.ps1` = W22" statements are read as superseded by this note for the Windows venv; budgets are unaffected: an INTERRUPTED segment takes no crash charge, and its in-flight keys are losses only when it reaches the I/O cap (note item 5); design :400 already accepts it.

## §3 — Frozen interface (the coordinator re-states it verbatim in each packet ticket)

Derived from design §3–§5. Items marked (K-4) are card proposals where the design leaves a name or format open.

### §3.1 Authority, capability, bootstrap, plan

- `screen_authority.validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root, now) -> ValidatedScreenAuthority`
- `screen_authority.require_validated_screen_authority(auth, *, source_contract, now)`
- `screen_authority.validate_screen_act(act_bytes, approval_bytes, public_keys, *, authority, ledger_head, now)`
- `screen_authority.ScreenBracket(bracket: BracketReplayResult, deadline_failure: tuple[bool, bool], consumed_splits: tuple[tuple, tuple])`
- `screen_authority.open_screen_epoch(source, authority)`, `require_open_screen_epoch(epoch, *, source, authority)`, `close_screen_epoch(epoch)`, `bind_screen_run(run_dir, authority_sha256)`
- `screen_authority.screen_epoch(source, *, authority)`, `screen_authority.screen_bracket(source, path, *, authority, epoch) -> ScreenBracket` (amendment PB2-1)
- `p7_evidence.render_bootstrap(params)`, `P7_BOOTSTRAP`, `P7_BOOTSTRAP_SHA256`, `SCREEN_BOOTSTRAP`, `SCREEN_BOOTSTRAP_SHA256`
- `t00_screen.plan`: `seed(...)`, `candidates(...)`, `shape_check(run, failed, path)`

### §3.2 Capability consumers (A10b; O-10)

- `screen_authority.screen_epoch` has one owner, `c1_rail/qualification/t00_screen/worker.py:open_epoch`, and `screen_authority.screen_bracket` one, `c1_rail/qualification/t00_screen/worker.py:bracket` (K-4). The candidate pass, the probe, every path key and every `verify` re-execution call `bracket`. These two pairs, plus any `.contract` load in a P-F module, are P-F's ALLOWLIST entries. `_replay_raw` and `_engine` have no consumer outside `production_source.py`.
- `screen_authority.py` (which receives the contract as `source_contract`), `state.py`, `journal.py` and `verdict.py` have no A10b finding. `plan.py` has none unless P-E records one under O-10; `plan.candidates` receives the candidate worker's `ScreenBracket`s and calls no capability.
- *Amendment PB2-1 (2026-10-05, coordinator (4), card owner; Joshua's ruling "Move screen entry out", on Codex r4180236028 at #679).* `screen_epoch` and `screen_bracket` are module functions in `screen_authority.py` that take the source, not `ProductionSource` methods. `production_source.py` imports nothing from `screen_authority`, `p7_evidence` or `t00_screen` (guard `test_production_source_imports_no_screen_module`), so `PRODUCTION_TRUST_POLICY` and the operator-signed trust document are unchanged and screen code stays outside the production trust surface. The A10b allowlist names `screen_authority.py:screen_epoch` (contract) and `screen_authority.py:screen_bracket` (contract, `_engine`) as the only consumers outside `production_source.py`; this replaces, for those two owners only, the bullet above that says `_engine` has no consumer outside `production_source.py`. `screen_epoch` runs the loaded-closure check before `open_screen_epoch` (Codex r4179917167), which discharges R-INT-4 in P-B2. Sealed functions (K7) are unchanged.

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
- PR-4 docs PR merged at: `11a20f1a0ac7ea5620e767a0c295477402f9cfb4` (#703, 2026-10-05; pinned `5660f17`; prepared by the Codex deployment coordinator's worker; independent review CLEAN 6001905693; card-owner acceptance 6001910659).
- Packet heads (recorded by coordinator (4), 2026-10-04):
  - P-B1 (#650): accepted at `0b4b560` (coordinator (3)); merged `6e2ece62af2f6059cf37afa82728ff9068dacfd5` (pinned `43b09f6`).
  - P-D (#643): K-5 re-taken on `740f392` (includes #611); accepted at `0866dff`; merged `f7a4e53042042d7a8d44b0b69ce458f47e43e805` (pinned `a6cb6a5`).
  - P-C (#646): K-5 re-taken on the future base `740f392` + P-D (tree `4b48cad6`); accepted at `e473c5f`; merged `f9099a2bdea9b7833b85a9fc706ff7a86a192000` (pinned `e473c5f`).
  - P-A (#672): merged `6629627028909c2691e5d0687784a8b29709a031` (pinned `9c81ab2`).
  - P-B2 (#679): merged `3b5c6a29569c995b805ffcb3ae1e5c7e1c654dec` (pinned `c142221`).
  - P-E (#647): merged `164e17b3f79a45e1ee05bdeadda3748bc2c4281b` (pinned `d465f1c`).
  - P-F (#705): merged `5d25f9cfc1e8ff00bacda45478322f9858176e8b` (pinned `5f48703`). *Recorded by coordinator (4), 2026-10-07.*
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
- **D2 — forbidden-files exception at H (RULED: Joshua, 2026-10-07T00:42:28Z, "Yes", to the question Hyper put to him at 00:36:19Z; relayed by the deployment coordinator).** The §4 and §10 forbidden-files check at H keeps its original baseline and its raw diff. Exactly one file is excepted: `core/mc/simulation.py`, changed by #708 (four-firm I-17 mode-switching; commits `e53d2c6` and `0db500e`, merged at `debc133`), not by any T00 packet. Scope: BASE `e9a68b148f906eaf928e5c81fa49d18e24ef4c6b` → H candidate `5d25f9cfc1e8ff00bacda45478322f9858176e8b`, blob `27d0e61deefa32b6735755cd02d01fa985139141` → `e549223c3edff5dc8a8ae025de601c5b0c29bb77`. Verified by coordinator (4), card owner, 2026-10-07: the raw diff names only this file, both commits are in #708, and the H blob equals #708's merged blob. Any other forbidden-path change, or any further change to this file, fails the check. Every other H requirement stands. This resolves the operator decision only; it is not H acceptance.
- **H: `5d25f9cfc1e8ff00bacda45478322f9858176e8b`** — **ACCEPTED by Joshua, 2026-10-07, directly to coordinator (4) ("i accept"), on the evidence below.** It is the first `origin/main` commit containing P-A…P-F, #611, PR-2 and PR-4. Recorded by coordinator (4), card owner. The H check ran from a detached worktree at H (`core.autocrlf=false`, clean with `--untracked-files=all`) on the operations venv, Python 3.13.2. Launcher records (`status` / exit / `source_stable` / `capture_complete`):
  - `tests/ops/qualification`, `--workers 2`: `20261006T195327Z-7b4fd53a1dcc`, completed / 0 / true / true. 2,214 collected; 2,206 passed, 0 failed, 1 skipped (Linux-only), 7 xfailed (awaiting K3/RC-4). It covers the 2026-09-30 A1–A23 regression (every spec row maps to a passing node) and `test_K7`. An earlier attempt, `20261006T182254Z-8a8471c5b0ec`, was cut off by a tool timeout and stays `running`; it counts for nothing.
  - `tests/ops/test_book_adapters_parity.py` with real inputs, read in place from the operator's primary checkout through `FP_PORT_ROOT` (the step-3 corrected-ports root; four ports pinned at H, plus `effective_inputs.json` `66406dee…`), `FP_TV_EXPORT_DIR` (`local_artifacts/recovery-2026-09-24/surviving-inputs`; the four book exports match `phase1_config.json`) and `FP_BAR_DATA_DIR` (the six panels match H's `SHA256SUMS`). Coordinator (4) checked these input identities by hashing them in place before the run; the record does not capture them, and records only that all 13 cases ran: `20261007T015920Z-3f32d7b62aac`, completed / 0 / true / true; 13 of 13 passed, 0 skipped. The earlier input-free run `20261006T214103Z-1b454ac78b97` (1 passed, 12 skipped) is vacuous and not counted.
  - `fp check`: `20261006T214311Z-b3652562543d`, completed / 0 / true / true.
  - **K7:** the source of the seven sealed methods has the same SHA-256 at the pre-build base `e9a68b1` and at H (independent AST check).
  - **Forbidden files:** the raw diff from `e9a68b1` to H names only `core/mc/simulation.py`, the D2 exception above.
  - **Row red/green:** 39 test-bearing rows are evidenced by their packets' records and the acceptance or carry comments on #650, #643, #646, #672, #679 and #647. The 16 P-F rows (S4–S8, S11, S12, S15, B2–B5, X1, X4–X6) have a **reconstructed** RED at P-F's final base: `20261007T015800Z-958b6fbdd110`, at `196ae62` plus only `5f48703`'s two test files (overlay diff SHA-256 `ccc743ce…`), using the original RED's command. It is failed / 1 / true / true, with all 16 rows FAILED and 0 errors (absent-capability failures, F7). Its GREEN twin is `20261006T080424Z-76c8df1a40d4` at `5f48703`. G1–G5 are review rows and have no records by design.
  - The deployment coordinator's evidence reviews are on file, and Joshua's acceptance is the decision. Later commits on `main` do not move H.
- Design §12 item 9 (depth N) answered by Joshua (precondition for §7 step 1): **N = 1,002 per population** (design §6.4 option a, "N = 1,000"; N = 3 × `depth_per_root`, so `depth_per_root` = 334 for each of the roots 42, 123 and 2026). Joshua, 2026-10-05, directly to coordinator (4): "you know what, I have changed my mind. let's go with N = 1000". This supersedes his earlier "N = 3,000" the same day, which was never recorded on main. Frozen at ratification (#581 A6). **Budgets and windows** (Joshua, 2026-10-05, directly to coordinator (4): "go with your budget and window recommendations"; design §5.4 at option a's upper figures):
  - `path_cpu_seconds` = **961,920**, which is c × 3N at c = 320 s, the per-path upper bound with the integrity check hoisted (§6.3), and 3N = 3,006 paths. That is about 267 CPU-hours. The recommendation's "about 33 CPU-hours" was option a's 8-core elapsed figure (§6.4), mislabelled as CPU; Joshua was told this when he ruled.
  - `overhead_cpu_seconds` = **11,300**, which is (b + 2i) × (W × S + R) + p with W = 8, S = 3, R = 8 and p ≈ 1,100 s, about 11,206 s rounded up.
  - **Approval windows** (§12 item 10): each fresh r3c and screen approval has `expires_at` at least 72 h after the planned start. Option a's upper wall time is about 43 h (§6.4), which leaves room for `verify` and pauses. r3c-a2 expires 2026-10-09T01:52:19Z, so the approvals must be fresh.
- ~~Still open outside this card: #581 OD-1/OD-2 direct confirmation (design §12 item 3).~~ *2026-10-03:* confirmed directly by Joshua (sheet 4 item 3, "all recommended"; #629 approval comment 5965049542). This card merged as #634 at `cdbf597b2ef2c7b4e32ae4af476e3a392f75ca79`.

- **Step 12 on a Windows VM (RULED: Joshua, 2026-10-07, directly to coordinator (4), the card owner).** These answer the questions coordinator (4) put to him after his cloud-host ruling ([campaign §60 addendum 2026-10-07](../programs/2026-09-03-seven-strategy-select-campaign-state.md)):
  - **Route A, mirror.** The H clone (`core.autocrlf=false`, clean), `C:\Program Files\Python313`, the operations venv and the private inputs are placed byte- and path-identical on the VM. The signed screen authority (`241708a1…`, approval `7310fc27…`) and the r3c source approval (`2cc7195e…`) are kept. VM `preflight` is the gate.
  - **One no-write P7 reproduction on the VM before `run`:** `p7_evidence.accept_p7_record` must reproduce record `6f142c0c…`. It is not `t00_screen accept-p7`, and it never touches `p7_acceptance.json` (`253aae43…`). A non-reproduction stops step 12. This narrows the different-host residual; the VM's system DLLs and CPU are still not hashed.
  - **`--workers 24`, single segment** (RULED by Joshua, 2026-10-07, after #721 review P1). The signed overhead budget (11,300 CPU-s) is per run: at about 315.8 CPU-s per worker start, it covers about 32 starts in total. One W = 24 segment uses about 8,700. Any second segment (crash, Ctrl-C, lapse or pause) halts the run with `OVERHEAD_EXHAUSTED`, and it can resume only on Joshua's signed CONTINUE before 2026-10-14T02:08Z. Joshua accepted that risk over W = 8's three-segment headroom (about 33 h, upper about 43 h). The budgets are unchanged; they are part of the ratified #581 values.
  - **VM checks before `run`:** RAM of at least 16.5 GiB at W = 24 (24 × 562 MiB, design §6). The path budget assumes at most 320 CPU-s per path, measured on the local host, so a slower VM core risks `PROBE_OVER_BUDGET` (row B3). Only the console outcome is recorded before `finalize` (no `PROBE_*` stop means the probe was within budget). The PROBE values are read after `finalize`, because a read of the run directory before then is an exposure (row X2).
  - **Licence and IP exposure accepted** by Joshua for the exports and ports on the VM.
  - **Unchanged:** start by 2026-10-11T02:08Z; both approvals expire 2026-10-14T02:08Z; `verify` must finish inside the window.
- **Step 12 VM route WITHDRAWN; the run is local (RULED: Joshua, 2026-10-07, about 15:40Z, directly to the step-12 owner session: "I want to go ahead and run the screen on my local machine"; cloud quota for 32 vCPUs needed several business days).** The VM bullet above is superseded and stays as history: route A, the VM P7 reproduction and `--workers 24` do not apply. Step 12 runs on this host under the original §8 basis: `--workers 8` and the signed budgets as sized (W = 8, S = 3, R = 8). The P7 acceptance from this host (`253aae43…`), the authority `241708a1…` and both approvals are unchanged. The row-X2 no-read rule before `finalize` still applies. The §60 VM admission (2026-10-07 addendum) was not used for this run.
- **Steps 7, 9, 10 and 11 completed** (coordinator (4), 2026-10-07):
  - **Step 7.** Joshua signed a fresh r3c approval: payload `ecadb2da…`, envelope `2cc7195e…`, expires 2026-10-14T02:08Z. P7 was re-run once at H: record `6f142c0c…`, closure `a7ecf3db…`, with the R1/R2 digests matching the accepted `b2c9f9c` run. `accept-p7` gave `p7_acceptance.json` `253aae43…`.
  - **Step 9.** #581 was RATIFIED 2026-10-07 (#720, merge commit `612edfa`; C `40c650c`, C′ `99e5efe`; values block `3432eb81…`).
  - **Step 10.** The label script was reviewed (#705 comment 6030648071). Its P2s were accepted as residuals (6030953085).
  - **Step 11.** Joshua signed `APPROVE_T00_SCREEN_AUTHORITY`. `validate_screen_authority` ISSUED authority `241708a1…` with approval `7310fc27…`, expiring 2026-10-14T02:08Z. Step 12 has to start by 2026-10-11T02:08Z, so that 72 h remain.
- **T00 step 3 / design step 12 RESULT: NO-GO-evidence, robust** (2026-10-08; recorded by coordinator (4), T00 card owner, from the step-12 owner's return; hashes and labels only).
  - **Labels.** Verdict line `T00_SCREEN_VERDICT NO-GO-evidence-robust`; `T00_SCREEN_VERIFY VERIFIED` (exit 0).
  - **Hashes.** results.json `a5b985d0abd79177fd910648ffbfaec040f6a4ac04728c8acee1f1e347a742dc`; attestation.json `f627e805ba3e92ef1bc461804cb8877494d77c9a42d5344626c4795d379d1ed5`; REPORT.md `bebceb93e6dbd80567dd4f94436df32f1892c296818d131da4eb61283a5e9984`; authority `241708a1…`.
  - **Run.** Local host; detached H `5d25f9c`, clean throughout; operations venv 3.13.2; `--workers 8`. Exactly one `run` (15:43:29Z → `T00_SCREEN_COMPLETE` 00:04:25Z), with no resume and no acts. Then `finalize` (00:47:59–00:48:01Z) and `verify` (00:48:14–01:00:08Z), all inside the approval window. The run directory was not read before `finalize` (row X2). Private tallies stay in the private run directory.
  - **What it means (#581 A6 and its §6 rulings).** The book fails the pre-registered condition even under the optimistic `UNDETERMINED` assignment. Per amendment §T00 step 3, it goes to Joshua as an **investment decision**: adjust the book, or accept the risk into T15's F1. It is never routed automatically. Under OD-1 reading (c), a **robust** NO-GO does not meet D-feed condition (a), even with risk acceptance; meeting (a) needs an amendment of (a). This is not four-firm §4 falsifier evidence.
- **Successor stopping rule (Joshua; ruled 2026-10-08, venue unrecorded; RATIFIED 2026-10-08).** The original ruling's venue is not recorded; Joshua does not recall it. He ratified it in chat to the Deployment Coordinator on 2026-10-08 ("I agree with your recommendations") as the binding rule within the successor decision tree below.
  - **Rule.** Successor work on this four-strategy book stops if either of these confirms the pessimistic anchor (`UNDETERMINED` resolved as bust, judged on H2):
    - resolution of the R1/R2 intrabar ordering, or
    - the pre-registered successor screen.
  - **Consequence.** No further size vector is proposed for this book, and the program is re-scoped.
  - **Basis.** A private desk model of evaluation → funded → payout economics against a size multiplier k. It assumes P&L variance scales with k² and drift with k. It is an assumption, not evidence; no replay, MC or screen was run.
    - Under that anchor, a uniform cut that meets the 5% bust ceiling falls below what the integer ladders can express: ORB is already at 1 contract and Vanguard floors to 0.
    - At that cut, pass time stretches to years per attempt, and the venue's winning-day payout minimum leaves no payout within a year of funding.
    - Under the favourable anchor, a mid-sized cut could clear both the 5% evaluation bust ceiling and a 1% pre-lock funded-ruin ceiling.
    - Viability therefore turns on the R1/R2 resolution more than on k.
  - **Model implication.** The evaluation floor never locks, so an early-phase-only cut has to cover most of the path to target, which makes it a uniform cut. A genuine early-phase cut fits the funded stage, where the floor locks.
  - **Records.** Figures stay in the private checkpoint folder. The next evidence is the size-feasibility check (tree step 1). Tier 2 is held until that step routes to it.
- **Successor decision tree (Joshua, 2026-10-08, "I agree with your recommendations", to the Deployment Coordinator).** This is the single record. The size-feasibility prereg §11 (#738) points here. The successor-screen skeleton (#733) is to point here; its author owns that edit.
  1. **Size-feasibility check** (#735 as amended by #738 §11). Route by its label:
     - **FEASIBLE** or **CLOCK-DEPENDENT**: go to step 2.
     - **GRID-NO-CLEAR**: the Deployment Coordinator recommends stopping uniform-cut successors of the accepted book on `Tradeify_Select_100K`. That is Joshua's discretionary investment judgment under stated model uncertainty, not a mathematical exclusion. Joshua chooses a stop or step 2; a uniform-cut stop does not bar per-leg successors.
     - **GRID-GAP**, **PASS-LIMITED** or **INCONCLUSIVE**: no automatic route. The Deployment Coordinator returns the result to Joshua with a recommendation. Joshua chooses step 2 or a stop.
     - **INVALID**: fix and re-run under the prereg. No route until a valid label.
  2. **Lift the hold** (new H, P7 re-run, Tier-2 source approval). Run Tier 2 (#729/#731). Its pattern picks one successor configuration.
     - R1/R2 resolution may be built in parallel only after a FEASIBLE or CLOCK-DEPENDENT label, as Joshua approved (scoping admitted 2026-10-08). After any other label it is built only if Joshua explicitly chooses it.
  3. **One pre-registered successor screen** (#733 skeleton) of that configuration, scored under both A5 assignments.
  - **When the stopping rule fires.** "Confirms the pessimistic anchor" means either of these:
    - **(a)** The successor screen's H2 result under the pessimistic A5 assignment (`UNDETERMINED` counted as bust) fails the A6 bust ceiling, and no accepted R1/R2 resolution shows that assignment to be unrealistic.
    - **(b)** An accepted R1/R2 resolution shows that `UNDETERMINED` paths resolve predominantly as busts. "Predominantly" means more than half of the resolved `UNDETERMINED` paths resolve as busts, judged on H2.
      - *Clarification (Joshua, 2026-10-08 ET, in chat to the Deployment Coordinator: "add the clarification under definition (b) on the T00 card", then "yes you may" to the amendments below; fixed before any resolution output exists).*
        - **Measure.** The midpoint test governs, and it replaces "more than half of the *resolved* `UNDETERMINED` paths" whenever resolution is partial. The midpoint is the H2 agreed-bust share plus half the H2 `UNDETERMINED` share, computed exactly from the step-12 H2 tallies (results `a5b985d0…`) and never rounded. Every H2 `UNDETERMINED` path counts; an unresolved path counts as bust at the pessimistic end of the bracket and as not bust at the optimistic end. Under full resolution this equals "more than half".
        - **Reading.**
          - **Confirmed:** even the optimistic end of the tightened bracket is above the midpoint.
          - **Not confirmed:** even its pessimistic end is at or below the midpoint.
          - **Undecided:** the bracket straddles the midpoint. The bracket stands, and (a) applies unchanged.
        - **(a) after Not confirmed.** The successor screen is judged on the pessimistic end of the tightened bracket, not on the original pessimistic assignment.

    Joshua confirmed (a) and (b) and set the (b) threshold on 2026-10-08, before any resolution output existed, in chat to the Deployment Coordinator: "go with your recommendation for 1".
  - While step 1 is pending, the new H, P7 re-run and Tier-2 source approval stay on hold (Joshua, 2026-10-08).
  - *2026-10-09:* **Hold lifted (tree step 2).** Step 1 returned FEASIBLE (size-feasibility return record, #745).
    - Joshua's ruling: "sign the approval to lift the hold", given in chat to the deployment-path session at about 04:45Z and confirmed directly to the Deployment Coordinator ("confirmed").
    - Sequence: a new H, then the P7 re-run, then Joshua signs the Tier-2 source approval (Tier-2 card admission item 5, valid 7 days).
    - One bundled H. It includes #742 (R1/R2 evidence-located convention), so R1/R2 shares that H, the P7 re-run and the approval chain. The coordinator recommended this and Joshua did not object.
    - Joshua also ratified #742's evidence-located/v1 convention: "ratify 742's convention", confirmed directly with "confirmed". The convention as ratified is #742 at `19502bd`; the ratification record lands with #742.
    - #742 merged 2026-10-09 (`a28383a`).
  - *2026-10-10:* **Bundled H: `39e3f688d4c51c02373533c54a4c6de2466e00ee`, ACCEPTED by Joshua** directly to the Deployment Coordinator ("accept H"). It supersedes `5d25f9c` for the P7 re-run, Tier 2 and R1/R2. The H check ran locally from a detached worktree at H (`core.autocrlf=false`, clean with `--untracked-files=all`) on the operations venv, Python 3.13.2. Each launcher record is completed, exit 0, `source_stable`, capture complete:
    - (a) `tests/ops/qualification`, 4 workers: `20261009T222533Z-94c5e386c0a0`, 2343 passed, 0 failed, 1 skipped, 7 xfailed. `test_K7` passed. The 7 sealed methods are byte-identical between `5d25f9c` and H and equal `SEALED_SOURCE_SHA256`.
    - (b) Parity, no inputs: `20261009T235734Z-785d91bbc636`, 1 passed.
    - (c) Parity, real inputs in place: `20261010T003505Z-667598026994`, 13 passed, 0 skipped. Exports, corrected ports, effective inputs and panels matched H's pins first. An earlier (c) run, `20261009T235753Z-42f9f6008cad`, skipped the export tests because a hygiene move had taken the exports out of place; they were restored on Joshua's ruling and (c) was re-run.
    - (d) `fp check`: `20261009T235906Z-f7699086e48c`, all gates OK.
    - Code delta `5d25f9c..H` under `ops/ core/ scripts/`: #736, #742, #725, #726 and #728 as expected. Disclosed to Joshua before acceptance, and accepted with H as a D2-style forbidden-path exception for these files only: #748 changed four Markdown changelogs under `core/strategies/_archive/`. No Pine, port or forbidden-list code file changed.
    - Next: one P7 re-run at H under a fresh r3c source approval (§7), then the Tier-2 source approval.
- *2026-10-08:* size-feasibility prereg FROZEN 2026-10-08, freeze commit `103c5ea`, merged `65079a7`; §11 addendum #738.
- *2026-10-09:* size-feasibility result **FEASIBLE**: largest clearing k 0.5; 1.0 and 0.75 do not clear; reproductions (a) and (b) matched. The tree routes it to **step 2**. The public return record is [RESULTS](../../../lab/analysis/c1/size_feasibility_2026-10/RESULTS.md). FEASIBLE is a target range, not a successor result (§11).

## §10 — Audit hooks

```bash
# Card form and authority (expect RESULT: well-formed; exit 0).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md

# Design identity this card binds (expect 3742a95... at #629's head until it merges).
gh pr view 629 --json headRefOid -q .headRefOid

# Per packet, at return: footprint = its §2.1 row exactly.
git diff --name-only "$(git merge-base origin/main HEAD)" HEAD

# P-E/P-F (O-10): expect only ALLOWLIST entry lines naming c1_rail/qualification/t00_screen/ owners,
# plus, for P-F only, the bounded scan extension of card note item 8 (label script scanned, repo-root owner
# resolution for it, one regression test).
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
