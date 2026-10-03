# T00 screen authority: build card

**Type:** cc_handoff (build card; packets dispatched by the coordinator against this card once approved)

**Date:** 2026-10-03 (UTC).

**Status:** DRAFT — awaits Joshua's approval (design §8 step 5). No packet starts and no code is written before that approval is recorded in §8 below.

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
| PR-2 | #581 merged **as DRAFT** with A5/A6 frozen and a dated note naming the frozen commit and the A5/A6 section hashes; design §3 item 8 settled **as drafted** (design §8 step 3, §12 item 5). Today OPEN, draft, head `0b50d08`; the design read it at `f0208f3`, so the coordinator re-checks A5/A6 bytes between the two heads before freezing P-C | P-C, P-A |
| PR-3 | #611 merged (design §8 step 1). Today OPEN, draft, head `76cc8c1` | P-B2 |
| PR-4 | The design §8 step-4 docs PR (§11 addendum to the 2026-09-30 spec; A10b reasons; #581 §5 item 3 wording; §3 cells as pointers to the values block) merged as its own PR. Must not touch #581's A5/A6 bytes | H |
| PR-5 | This card approved by Joshua (design §8 step 5) | every packet |

## §0.5 — Card decisions (Joshua answers with the card) and recommended defaults

The design's §9.1 packets leave five footprint collisions. The card resolves them as below; each is a packaging change, not a design change.

- **K-1. Split P-B into P-B1 and P-B2.** The design places `ScreenBracket` and the epoch helpers in `screen_authority.py` (§3.3, §9), which P-A owns, while P-B's `screen_epoch`/`screen_bracket` call them; and P-A's row K3 reads `SCREEN_BOOTSTRAP_SHA256`, which P-B's `p7_evidence.py` produces. One P-B packet would form a cycle with P-A. *Recommend:* P-B1 = `p7_evidence.py` (bootstrap template, `SCREEN_BOOTSTRAP_SHA256`, forbidden lists); P-B2 = `production_source.py` and A10b. Order P-B1 → P-A → P-B2. Both stay CC solo.
- **K-2. Move rows S2 and B1.** S2's enforcement is the worker audit hook, which lives in the bootstrap template (`p7_evidence.py`, §5.1). B1 is a record schema in `journal.py`. *Recommend:* S2 → P-B1; B1 → P-D. Row totals are unchanged (§2 table).
- **K-3. `t00_screen/__init__.py`.** P-C, P-D, P-E and P-F each need the package to exist. *Recommend:* each of those packets adds the file with exactly these bytes, which git merges as identical adds: `"""T00 step-3 screen driver (design 2026-10-02 section 9)."""` followed by one LF. Any other byte in it is a manifest violation.
- **K-4. Card-proposed names** (the design does not name them): `p7_evidence.render_bootstrap(params)` (template), `p7_evidence.SCREEN_BOOTSTRAP` and `SCREEN_BOOTSTRAP_SHA256`, `screen_authority.bind_screen_run(run_dir, authority_sha256)` (row K4's write-once binding, called by `t00_screen.worker`). *Recommend:* adopt; the coordinator may rename at freeze without a new approval if behaviour is unchanged.
- **K-5. Build ahead of merge.** P-D and P-E have no code dependency for their row tests, and P-E's tests use a fake source against the frozen §3.3 signatures. *Recommend:* P-D, P-E and P-F may be built from wave 1 against the frozen interface in §3, but merge only in the §4 order.

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
| P-D | `t00_screen/state.py`, `t00_screen/journal.py` (new); `tests/ops/qualification/test_t00_screen_state.py` (new); `t00_screen/__init__.py` (K-3 bytes) | S1, S3, S9, S10, S13–S16, B1 (9) |
| P-E | `t00_screen/plan.py` (new); `tests/ops/qualification/test_t00_screen_plan.py` (new); `t00_screen/__init__.py` (K-3 bytes) | R1–R3 (3) |
| P-F | `t00_screen/coordinator.py`, `worker.py`, `__main__.py` (new); `scripts/t00_screen_label_check.py` (new); `tests/ops/qualification/test_t00_screen_driver.py` (new); `t00_screen/__init__.py` (K-3 bytes) | S4–S8, S11, S12, B2–B5, X1, X4–X6 (15) |
| coordinator | review, audit hooks, this card's §8 | G1–G5 (5) |

Total 60 = design §2.2. `t00_screen/` is `ops/c1_rail/qualification/t00_screen/`.

**Overlaps flagged** (all resolved; none is a shared write except K-3's identical bytes):

| # | Overlap in the design | Resolution |
|---|---|---|
| O-1 | `ScreenBracket`, `open_screen_epoch`, `require_open_screen_epoch`, `close_screen_epoch` sit in `screen_authority.py` but serve rows K6/K8 | P-A writes them to the §3 signatures; P-B2 tests them (K6, K8). K-1 |
| O-2 | K3 reads `SCREEN_BOOTSTRAP_SHA256` from `p7_evidence.py` | P-B1 produces it; P-A rebases on P-B1. K-1 |
| O-3 | S2's worker audit hook is in the bootstrap template | S2 → P-B1. K-2 |
| O-4 | B1's record schema is in `journal.py` | B1 → P-D. K-2 |
| O-5 | A9, A11 and V3 share `A5_TEXT_SHA256`, `A6_TEXT_SHA256`, `A6_HORIZON_SESSIONS`, the `a5_rule` IDs and `median_rule` | defined once in `t00_screen/verdict.py` (P-C); `screen_authority` imports them (design §8 step 3: "the verdict code pins the hashes"). P-A rebases on P-C |
| O-6 | X3 spans `validate_screen_act` (P-A), the ACT transition in `state.advance` (P-D) and the act-file recording in `act`/`resume` (P-F) | `test_X3` (P-A) covers the validator; P-D covers ACT transitions under `test_S1`'s table; P-F covers recording in I1 |
| O-7 | K4 spans the check (P-A) and the binding call (P-F) | P-A defines `bind_screen_run`; P-F calls it once per worker |
| O-8 | K6's closure agreement across epochs is checked in `state.check_record` (P-D) | P-D implements the clause; `test_K6` stays in P-B2; I1/I3 (P-F) exercise it end to end |
| O-9 | `t00_screen/__init__.py` | K-3 |

### §2.2 Common rules (every packet)

- **Forbidden files** (design §9): `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py`, `replay.py`, `book_policy.py`, `core/` (including `dd_protection.py` and `mc/`), every Pine source, port and private artifact, r3c's bytes, `SOURCE_SIGNING_KEYS`, `SOURCE_REFUSALS` and the pinned key. Any file outside the packet's row of §2.1.
- **Sealed methods** in `production_source.py`: `replay`, `replay_bracket`, `proof`, `_seal`, `_check_path`, `_verify_integrity`, `verify_for` keep their source text (row K7).
- **Semantics:** `runner.evaluate_replay`, `runner._run_stage` and `bracket.run_bracket` behave exactly as at the base.
- **Tests:** TEST_ONLY keys generated in-process; only the pinned root and the validator's repository-root constant are monkeypatched; synthetic fixtures only. No test reads the real source (design §10).
- **Red-first:** each row test `test_<row>` is committed and recorded failing on the packet base through the launcher, then passing on the build; each asserts its row's code and has a passing twin. A row test that cannot be made red on the base is a stop (§6).
- **Launcher records:** `.\fp.ps1 python -m pytest <files>` (or `python -I scripts/fp.py python -m pytest <files>`), each citing its `.cache/fp-verification/.../record.json` with `status: completed`, `verification_exit_code` and `source_stable`.
- **Branch:** `claude/t00-screen-<packet>` (or `glm/`, `cursor/` per lane), cut from `origin/main` after its §4 dependencies merge; one writer.

### §2.3 P-A — authority, validator, receipts, acts

- **Rows:** A1–A11, K1–K4, X2, X3.
- **Writes:** `screen_authority.py`, `test_screen_authority.py`.
- **Builds:** `SCREEN_AUTHORITY_FIELDS`; compiled r3c digest; compiled pre-registration chain (row A8) and A3 successor paths and patterns (row A10); `validate_screen_authority` (step order §3.2: bytes → signature → `_check_bindings` → issue); `_check_bindings` (A5–A10, repository root `Path(__file__).resolve().parents[3]`, `git --end-of-options`, `core.autocrlf=false`); `ValidatedScreenAuthority` with weakref registry; `require_validated_screen_authority` (K1–K4, `SCREEN_APPROVAL_EXPIRED` re-code); `bind_screen_run`; `ScreenBracket`, `open_screen_epoch`, `require_open_screen_epoch`, `close_screen_epoch` with the stat guard (§3.3); `validate_screen_act` (X2, X3). Scopes `APPROVE_T00_SCREEN_AUTHORITY`, `APPROVE_T00_SCREEN_ACT`.
- **Imports, never edits:** the `contract.py` helpers listed in design §3.2.
- **Red-first tests:** `test_A1`…`test_A11`, `test_K1`…`test_K4`, `test_X2`, `test_X3` (design §2.2 column 4 names the violating input of each).
- **Lane:** CC solo. Trust/auth: never GLM, never Cursor.
- **Depends on:** PR-1, PR-2, PR-5; P-B1 merged (O-2); P-C merged (O-5).
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
- **Builds:** #581 A5 (1)–(3) and A6 by reference, exact integer comparisons (`20·bust ≤ n`, `2·pass ≥ n`), `UNDETERMINED` in every denominator, pessimistic assignment decides GO and optimistic labels NO-GO; returns `INSUFFICIENT(reasons)` or the labels, never both (V1); constants `A5_TEXT_SHA256`, `A6_TEXT_SHA256` (from PR-2's frozen bytes), `A6_HORIZON_SESSIONS`, the `"T00_A5/v1"` rule ID and `"LOWER_NEAREST_RANK_INF_INCLUDED"`.
- **Red-first tests:** `test_V1` (reasons plus GO-shaped tallies), `test_V2` (bust count exactly 5%), `test_V3` (one constant changed), `test_V4` (hybrid row).
- **Lane:** GLM-eligible, synthetic rows only. `workdir` = a fresh worktree under `.claude/worktrees/` with no `.env`; the ticket carries no private value, no Pine or port path, no account data. The coordinator reads the full diff before acceptance (operator GLM rule). CC if GLM fails twice.
- **Depends on:** PR-1, PR-2, PR-5.
- **Return:** §6, plus the two section hashes and the blob they were taken from.

### §2.7 P-D — state, journal, transition function

- **Rows:** S1, S3, S9, S10, S13–S16, B1.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/state.py` (`advance`, `classify`, `check_record`), `t00_screen/journal.py` (hash-chained append/fsync, torn-tail rule, record schemas of §4.1 including B1's cost fields, canonical `results.json`), `test_t00_screen_state.py`.
- **Builds:** the §4.2 transition table exactly; the closed §4.3 class table; K6's closure-agreement clause in `check_record` (O-8); S16's byte equality across W and segmentation.
- **Red-first tests:** `test_S1`, `test_S3`, `test_S9`, `test_S10`, `test_S13`, `test_S14`, `test_S15`, `test_S16`, `test_B1`; plus an ACT-transition case table under `test_S1` (O-6). Fake source only.
- **Lane:** CC (the transition function is the crash model).
- **Depends on:** PR-1, PR-5. Built from wave 1 (K-5); merges per §4.
- **Return:** §6, plus the §4.2 table as implemented (state × event → state) for diff against the design.

### §2.8 P-E — plan

- **Rows:** R1–R3.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/plan.py` (`seed`, key universe and plan digest, `candidates`, `shape_check`), `test_t00_screen_plan.py`.
- **Builds:** seed = first 8 bytes of SHA-256 of canonical `["t00-screen-rng/v1", purpose, root, population, path_index]`, never `regime.domain_seed`; candidates as the R1 ∩ R2 joint-flat intersection stored as indices plus digest (§5.2); `shape_check` per §5.3.
- **Red-first tests:** `test_R1` (W = 1 vs W = 4; collision scan against `domain_seed`), `test_R2` (block flat in R1 only), `test_R3` (short run without the flag).
- **Lane:** Cursor or CC. Read-only access to `blocks.py`, `paths.py`, `regime.py`.
- **Depends on:** P-B2's interface (§3); built from wave 1 against a fake source (K-5); merges after P-B2.
- **Return:** §6.

### §2.9 P-F — coordinator, worker, CLI, label script, integration

- **Rows:** S4–S8, S11, S12, B2–B5, X1, X4–X6.
- **Writes:** `t00_screen/__init__.py` (K-3), `t00_screen/coordinator.py`, `t00_screen/worker.py`, `t00_screen/__main__.py` (`preflight`, `accept-p7`, `run`, `resume`, `finalize`, `verify`, `act`), `scripts/t00_screen_label_check.py`, `test_t00_screen_driver.py`.
- **Builds:** run lock, O_EXCL run directory, ledger-only writer, Job Object (`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, suspended → assigned → resumed), pinned worker environment, budget gate and overhead reserve, probe sequencing, fixed console lines (§5.6), `verify` with k = 9 hash-derived re-executions inside the K3/K4 gate, `accept-p7` writing `p7_acceptance.json`. The label script imports nothing from `t00_screen.verdict` (X5) and is written without reading P-C's implementation.
- **Red-first tests:** `test_S4`…`test_S8`, `test_S11`, `test_S12`, `test_B2`…`test_B5`, `test_X1`, `test_X4`, `test_X5`, `test_X6`; integration I1 (every §4.4 crash window), I2 (Ctrl-C through `fp.ps1` lands as W22 and resumes), I3 (every ledger prefix folds to its durable state). Real subprocess workers, deterministic fake source, TEST_ONLY seam only.
- **Lane:** CC integration.
- **Depends on:** P-A, P-B1, P-B2, P-C, P-D, P-E merged.
- **Return:** §6, plus the revision-2 test map (design §10) checked off.

## §3 — Frozen interface (the coordinator re-states it verbatim in each packet ticket)

From design §3.2–§3.3, plus the K-4 names:
- `screen_authority.validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root, now) -> ValidatedScreenAuthority`
- `screen_authority.require_validated_screen_authority(auth, *, source_contract, now)`
- `screen_authority.validate_screen_act(act_bytes, approval_bytes, public_keys, *, authority, ledger_head, now)`
- `screen_authority.ScreenBracket(bracket: BracketReplayResult, deadline_failure: tuple[bool, bool], consumed_splits: tuple[tuple, tuple])`
- `screen_authority.open_screen_epoch(source, authority)`, `require_open_screen_epoch(epoch, *, source, authority)`, `close_screen_epoch(epoch)`, `bind_screen_run(run_dir, authority_sha256)`
- `ProductionSource.screen_epoch(*, authority)`, `ProductionSource.screen_bracket(path, *, authority, epoch) -> ScreenBracket`
- `p7_evidence.render_bootstrap(params)`, `P7_BOOTSTRAP`, `P7_BOOTSTRAP_SHA256`, `SCREEN_BOOTSTRAP`, `SCREEN_BOOTSTRAP_SHA256`
- `t00_screen.verdict`: `A5_TEXT_SHA256`, `A6_TEXT_SHA256`, `A6_HORIZON_SESSIONS`, the rule IDs; `t00_screen.state`: `advance(state, event)`, `classify(cause)`, `check_record(...)`; `t00_screen.plan`: `seed(...)`, `candidates(...)`, `shape_check(run, failed, path)`

A packet that needs a different signature stops and returns (§6).

## §4 — Hypothesis, integration order and head H

**H (build):** with P-A…P-F merged, every design §2.2 row A1–X6 has a red-on-base, green-on-build launcher record; the 2026-09-30 A1–A23 regression, `tests/ops/qualification`, `tests/ops/test_book_adapters_parity.py` and `.\fp.ps1 check` are green at H; and `git diff --name-only <pre-build base> H` touches no §2.2 forbidden file. **Reject if** any row test cannot be made red on its base, any row is green only with a forbidden edit, the sealed-method source hashes change (K7), or the forbidden-file diff is non-empty. **Revert trigger:** any 2026-09-30 regression test or existing qualification test changes outcome at H.

**Dependency graph:**

```
PR-1 #629 ─┬─────────────────────────────────────────────► every packet
PR-5 card ─┘
PR-2 #581 (DRAFT, A5/A6 frozen) ─► P-C ─────┐
P-B1 ───────────────────────────────────────┼─► P-A ─► P-B2 ─► P-E ─┐
PR-3 #611 ──────────────────────────────────────────► P-B2          ├─► P-F ─► H
P-D ────────────────────────────────────────────────────────────────┘
PR-4 docs PR (§11 addendum) ─────────────────────────────────────────────────► H
```

**Merge order** (each as its own PR, opened by the coordinator, merged by Joshua after Codex clean at the exact head and CI green):
1. Wave 1, in parallel: P-B1, P-C, P-D (and P-E, P-F built but not merged, K-5).
2. P-A, rebased on P-B1 and P-C.
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

1. **Payload.** The coordinator writes the approval payload's canonical bytes (`contract.canonical_json_bytes`, no trailing newline) to `payload.json` in the private root, outside any worktree: `{schema: "qualification_approval_payload/v1", scope: "APPROVE_T00_SOURCE_CONTRACT", subject_sha256: <r3c digest>, contract_sha256: <r3c digest>, issued_at, expires_at, authority_class: "OPERATOR"}`. `expires_at` covers steps 7–12 plus `verify` at the chosen N (design §12 item 10; r3c-a2 expires 2026-10-09T01:52:19Z). The signing packet shows Joshua the payload bytes, their SHA-256, scope, schema, subject and key ID `source:1ebae5d45bc51280` (row G5).
2. **Joshua signs**, in Git Bash; the agent never touches the key:
   ```bash
   sha256sum <payload.json>     # must equal the SHA-256 in the signing packet; do not open or edit the file
   openssl pkeyutl -sign -rawin -inkey <your key.pem> -in <payload.json> -out <payload.sig>
   ```
3. **Assemble and verify.** The coordinator builds `{schema: "qualification_approval/v1", payload, signature: {algorithm: "Ed25519", key_id: "source:1ebae5d45bc51280", value_b64: base64(payload.sig)}}` as canonical JSON and verifies it with `contract.verify_detached_approval` (`allow_test_authority=False`) before use.
4. **One P7 re-run at H** under that approval, from the detached H worktree, by the accepted P7 procedure ([P7-closure packet](2026-09-24-tradeify-t00-p7-closure.md) §7, step-1b re-run). Its closure covers `production_source.py` and `p7_evidence.py` at H.
5. **`t00_screen accept-p7`** (coordinator, per §12 item 11; or Joshua himself to close the §13 residual) → record R and `p7_acceptance.json` in the private root. Public return: R's SHA-256, the acceptance SHA-256, H, closure MATCH and R1/R2 digest MATCH labels only.

The screen-authority signature (design §8 step 11) uses the same template with `scope: "APPROVE_T00_SCREEN_AUTHORITY"` and `subject_sha256 = contract_sha256 =` the authority SHA-256. It is outside this card.

## §8 — Approval, prerequisites and H record

- Card approval (design §8 step 5): **pending**.
- PR-1 #629 merged at: —
- PR-2 #581 merged (DRAFT, A5/A6 frozen) at: — ; A5/A6 section hashes: —
- PR-3 #611 merged at: —
- PR-4 docs PR merged at: —
- Packet heads (P-A, P-B1, P-B2, P-C, P-D, P-E, P-F): —
- H: —
- Still open outside this card: design §12 item 9 (depth N, needed at step 8); #581 OD-1/OD-2 direct confirmation (design §12 item 3).

## §10 — Audit hooks

```bash
# Card form and authority (expect RESULT: well-formed; exit 0).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md
python -I scripts/fp.py python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md

# Design identity this card binds (expect 3742a95... at #629's head until it merges).
gh pr view 629 --json headRefOid -q .headRefOid

# Per packet, at return: footprint = its §2.1 row exactly.
git diff --name-only "$(git merge-base origin/main HEAD)" HEAD

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
