# T00 successor screen: build card

**Type:** cc_handoff (build card; packets dispatched by the coordinator against this card once approved)

**Date:** 2026-10-10 (UTC).

**Status:** DRAFT — awaits Joshua's approval. No packet starts and no code is written before that approval is recorded in §8.

**Authority:**
- Operator rulings Q2, Q3 and Q5 (Joshua, 2026-10-10, directly to the Deployment Coordinator: "agreed on Q2, Q3, Q5"), recorded in §8. They answer the [readiness map](../../notes/2026-10-10-successor-screen-readiness-map.md) (PR #757) §5.
- The successor decision tree, step 3 ([T00 card](2026-10-03-t00-screen-authority-build-card-DRAFT.md) §8): one pre-registered successor screen of one configuration.
- **This card** needs Joshua's own approval before any packet starts. It narrows the rulings; it adds no authority to them.

**Coordinator:** the Deployment Coordinator ("Portfolio deployment coordination"). It freezes each packet ticket, owns the claim manifest, reviews every diff, opens PRs, integrates and records H′. Joshua merges.

**Return boundary (card level):** every packet returns to the coordinator (§6). The build ends at an accepted H′ (§4). §7 lists the governance chain after H′; each of its operator acts needs its own GO.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-10-03-t00-screen-authority-build-card-DRAFT.md
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
  - no_protection_cell_change
  - no_a5_a6_text_change
  - no_r1r2_build
  - no_edit_of_733_outside_p_s5
acceptance:
  - tests/ops/test_book_policy.py
  - tests/ops/qualification/test_replay.py
  - tests/ops/qualification/test_production_source.py
  - tests/ops/qualification/test_screen_authority.py
  - tests/ops/qualification/test_t00_screen_driver.py
  - tests/ops/qualification/test_source_consumers.py
  - tests/ops/test_book_adapters_parity.py
```

## §0 — Production reads and prerequisites

**Reads** (every packet, at its base; record `git log -1 --format='%h %as' -- <path>`):
- the readiness map (#757) §1–§5 in full;
- the [screen-authority design](../../superpowers/specs/2026-10-02-t00-screen-authority-design.md) §2.1, §2.2 rows A1–A11, §3, §4.5 and §9;
- the T00 card §2.2, §3 and §8 (H record, threat model, R-INT-1, D2);
- [#581](../pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md) §2 A5/A6, §3 and §6; [#733](../pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md) in full;
- the packet's own code: `ops/c1_rail/book_policy.py` (`entry_quantities` `:279-315`, `add_quantity` `:255-276`, `LegSpec` `:141-192`), `ops/c1_rail/qualification/replay.py` (`:300-315`, `:590-615`), `production_source.py` (`request_sizing_inputs` `:92-110`, `parse_startup_policy` `:174-204`, `_engine` `:1337-1360`), `screen_authority.py` (`:44-110`, `:174-245`, `:292-455`, `:603-620`), `t00_screen/verdict.py`.

Line numbers are at `origin/main@85563a4`.

**Prerequisites** (each recorded by SHA or date in §8 before the packet it gates starts):

| # | Prerequisite | Gates |
|---|---|---|
| PS-1 | This card approved by Joshua, including §0.5 decisions S-1…S-7 | every packet |
| PS-2 | #757 (readiness map) merged or its head pinned in §8 | every packet |
| PS-3 | Tier-2 report delivered and accepted; Q1 answered (§8) | §7 step 2 onward, not the build |
| PS-4 | P-S5 (the #733 rewrite) merged | §7 step 4 (freeze), not H′ |

The build does not wait for Q1 or the Tier-2 report: every packet is written for any vector (§1.2).

## §0.5 — Card decisions (Joshua answers with the card) and recommended defaults

- **S-1. The vector lives in the replay, not in the policy object.** `candidate_book_protection_policy()` is hard-checked (`require_policy`, `book_policy.py:99-115`) and stays unchanged. *Recommend:* a separate `SizeVector` value, passed to `BookReplay` at construction and from there to `entry_quantities` and `add_quantity`. The default is the identity vector, which gives today's quantities exactly. The live rail does not pass a vector, so its behaviour is unchanged; `book_policy.py`'s bytes do change, which moves the TB-I1 policy fingerprint (`policy_fingerprint.py:29-32`) and the qualification policy's `source_owner_sha256` (`test_semantic_policy.py:34-36`). No test pins those bytes (`test_semantic_policy.py` hashes at runtime); the engineering manifest fixture is a dated record and stays unchanged.
- **S-2. Striker's entry is a multiplier pair plus an optional ceiling.** Striker's size is risk-derived (1..22), so "whole contracts" cannot be its only form. *Recommend:* `risk_multiplier`, `cap_reserve_multiplier` (exact rationals in [0, 1]) and an optional integer `max_base`. Every form can only lower the quantity. Q1 may choose any of them.
- **S-3. Bind the successor contract by derivation from r3c, not by a compiled r3d digest.** r3d's bytes depend on Q1, so a compiled r3d digest would make the build wait for Q1 and force a new H whenever the vector changes. *Recommend:* under the successor purpose, the authority binds the digest it carries. That digest must equal the receipt's and the P7 record's. It must also pass a derivation check: r3d's canonical document, with `contract_id` and the `source_startup_policy` artifact row put back to r3c's compiled values, hashes to `R3C_CONTRACT_SHA256`. Any other changed role is refused. The coordinator supplies r3c's `contract_id` and its complete startup-policy artifact row (every field, `producer` and `authority_class` included; no private bytes) in the P-S3 ticket. The v2 policy minus `sizing` must also equal r3c's v1 policy fields (schema aside), so the vector is the only startup change: P-S3 reads r3c's startup bytes from `artifact_root` at the row's path, checks them against the row's digest, and refuses the authority if the file is missing or differs. This changes design rows A6 and A7 for the new purpose only, so it needs Joshua's approval (§3.2).
- **S-4. Each purpose binds its own pre-registration chain entry.** Appending #733 to `PREREG_CHAIN` would make "last entry" refuse #581. *Recommend:* the original purpose binds entry 0 (#581) and the successor purpose binds entry 1 (#733). The original purpose's outcomes do not change. Needs Joshua's approval (design row A8, "the compiled chain's last entry").
- **S-5. The successor refuses the identity vector and the step-12 RNG roots.** *Recommend:* a v1 startup policy, or a v2 policy whose vector gives today's quantities, is refused under the successor purpose (it would be a re-run of the declared book, not a successor). `is_identity` is computed over the quantity table (every leg × mode × ladder input), not over the encoding, and `validate_size_vector` requires a canonical encoding (reduced fractions; no field equal to a no-op, such as an Aegis `adds` other than `UNCHANGED`, `OFF_WHEN_PROTECTED` on Vanguard or ORB, which is already today's rule, or any `max_base` at or above the cap term it can never undercut, which includes 22), so one vector has one `size_vector_sha256`. `rng.roots` and `rng.probe_root` must be disjoint from step 12's compiled roots (`42`, `123`, `2026` and its probe root), so successor keys are disjoint from step 12 and from Tier 1 and Tier 2, whose keys come from step 12's run. Seeds hash the compiled tag, the literal `path` or `probe`, root, population and index (`t00_screen/plan.py:49`; `worker.py:318`, `:344`), never the authority's purpose, so new roots are the disjointness. The tag is compiled (`screen_authority.py:66`), so #733 §7's "distinct RNG tag" is reworded by P-S5.
- **S-6. No verdict code (P-S4 option A).** Under Q5 the binding verdict is #581 A6's, byte for byte (§1.1). *Recommend:* build nothing in `verdict.py`. Option B, a reported R1-alone tally, changes the frozen §3.7 verdict interface and `results.json` bytes; it is built only if Joshua chooses it.
- **S-7. Names.** *Recommend:* purpose `T00_SUCCESSOR_SCREEN`, grant `T00_SUCCESSOR_SCREEN_ONCE`, evidence class `T00_SUCCESSOR_SCREEN`, refusals unchanged (`PARAMETER_CHANGE` kept, with Q3's meaning), startup schema `qualification-source-startup/v2` with a `sizing` field, and the §3 names. The coordinator may rename at ticket freeze without a new approval if behaviour is unchanged.

Missing facts or a contradicted default return `NEEDS_CONTEXT`; they are never assumed.

## §1 — Context

The step-12 screen of the declared book returned `NO-GO-evidence-robust` (T00 card §8). The decision tree's step 3 is one pre-registered screen of one successor configuration. The current authority cannot run it (map §1 item 1). This card adds a second purpose beside the first, a per-leg size vector carried by a signed startup policy, and a rewrite of #733 into #581's form. It ends at a new head H′.

### §1.1 What Q5 means for #733's gates

Q5 copies #581's A5 and A6 into #733 byte for byte, because `_check_sections` compares them with compiled hashes. The binding verdict is therefore #581 A6: the pessimistic bust ceiling on FULL, H1 and H2, and the pass floor on FULL (and the halves if `pass_floor_halves` is `BINDING`). #733's draft gates map as follows:

| #733 gate | Under Q5 |
|---|---|
| G1 bust, pessimistic, FULL/H1/H2 | A6, binding, unchanged |
| G3 pass floor, pessimistic, FULL | A6, binding, unchanged |
| G2 bust, R1 alone, H2 | **Implied by G1.** An R1 bust is either an agreed FAILURE with a bust run, or an `UNDETERMINED` path; the pessimistic assignment counts both as busts. So a pessimistic H2 pass of the ceiling implies the R1-alone pass, for GO versus NO-GO. Not separately bound |
| G4 pass floor, R1 alone, H2 | **Implied by the H2 pass floor** when `pass_floor_halves` is `BINDING`: every pessimistic pass is an agreed PASS, so R1 passes no later. With `REPORTED` (#581's step-12 value) it is not enforced at all. Joshua decides `pass_floor_halves` at freeze |
| G5 funded survival | Reported, non-binding (Q6, OWED); no producer exists, so it is reported as "not produced" |
| G6 economics | Outside A6; reported only |

**Label subtype.** The implications cover the GO versus NO-GO decision only. #733 §6 rule 4 makes a failed R1-alone gate a *robust* NO-GO; under #581 A6 the same paths can be labelled `UNDETERMINED`-dependent, because the optimistic assignment does not count an undetermined R1 bust and does count an undetermined R1 pass (`verdict.py:173-175`). Under Q5 A6's labels govern; P-S5 states this in #733.

The stopping rule's definition (a) reads the H2 pessimistic bust result. That is one of A6's own comparisons, so the existing `results.json` tallies answer it; no new code is needed. R1/R2 is on hold, so no accepted R1/R2 resolution exists and (a) applies as written.

### §1.2 Any vector, including a leg at 0

A leg at 0 stays in the contract and its signals are still generated. Every entry is rejected with "zero policy quantity" (`replay.py:612-614`), before `ledger.request` (`:620`), any takeover or order insertion; P-S1's row Z7 proves it in a replay. Removing a leg from the contract is out of scope (map §3).

## §2 — Claim manifest and packets

### §2.1 Claim manifest (write footprints)

| Packet | Writes (exactly) | Rows |
|---|---|---|
| P-S1 | `ops/c1_rail/book_policy.py` (`SizeVector`, `LegSize`, `validate_size_vector`, `IDENTITY_SIZE_VECTOR`; `entry_quantities` and `add_quantity` gain a keyword-only `size`); `ops/c1_rail/qualification/replay.py` (`BookReplay` takes `size_vector` and passes each leg's entry; `:309` cap term included); `tests/ops/test_book_policy.py`; `tests/ops/qualification/test_replay.py` | Z1–Z10 |
| P-S2 | `ops/c1_rail/qualification/production_source.py` (`parse_startup_policy`, `StartupPolicy`, `_engine` only); `tests/ops/qualification/test_production_source.py` | Y1–Y5 |
| P-S3 | `ops/c1_rail/qualification/screen_authority.py`; `tests/ops/qualification/test_screen_authority.py` (new rows, plus the `:474` assertion `PREREG_CHAIN[-1] == PREREG` amended to the per-purpose entry); `tests/ops/qualification/test_t00_screen_driver.py` (W9 case only) | W1–W10 |
| P-S4 | Option A (recommended): nothing. Option B: `ops/c1_rail/qualification/t00_screen/verdict.py`, `tests/ops/qualification/test_t00_screen_verdict.py` | V5 (B only) |
| P-S5 | `docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md` only | D1–D7 |
| coordinator | review, H′ check, the K₀ ledger PR (§7 step 3), this card's §8 | G1–G4 |

No two packets write the same file. Coordinator rows: **G1** each packet's diff equals its §2.1 row; **G2** the forbidden-file diff at H′ is empty; **G3** the sealed methods equal `SEALED_SOURCE_SHA256` at H′; **G4** every signing packet shows scope, schema, subject and key ID (design row G5).

### §2.2 Common rules (every packet)

- **Forbidden files:** `contract.py`, `trust_domain.py`, `p7_evidence.py`, `p7_driver.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py` (all under `ops/c1_rail/qualification/`); `t00_screen/state.py`, `journal.py`, `plan.py`, `coordinator.py`, `worker.py`, `__main__.py`, and `verdict.py` unless P-S4 option B is chosen; `scripts/t00_screen_label_check.py`, `scripts/t00_screen.py`; `ops/c1_signal_daemon/book_adapters.py`; `core/` (including `dd_protection.py`, `lifecycle.py` and `mc/`); every Pine source, port, `effective_inputs.json` and private artifact; r3c's bytes, `SOURCE_SIGNING_KEYS`, `SOURCE_REFUSALS`, `SOURCE_PURPOSES` and the pinned key; #581; any file outside the packet's §2.1 row.
- **Sealed methods** (`production_source.py`): `replay`, `replay_bracket`, `proof`, `_seal`, `_check_path`, `_verify_integrity`, `verify_for` stay byte-identical; `test_K7`'s `SEALED_SOURCE_SHA256` is unchanged. No re-pin is needed: P-S2 edits only `parse_startup_policy`, `StartupPolicy` and `_engine`, none of them sealed.
- **Frozen at today's values:** the protection cell (1% trigger, 0.40 scale, prior-close timing, 80-micro capacity, Aegis-priority takeover, ORB base unreduced, ORB adds off when protected); `CANDIDATE_SCALE`; `TIER_MULTIPLIER`; `orb_normal_base == 1`; `P7_BOOTSTRAP_SHA256` and `SCREEN_BOOTSTRAP_SHA256`; `A5_TEXT_SHA256`, `A6_TEXT_SHA256`, `VALUES_SCHEMA`, `SECTION3_KEYS`, the Status regex; the original purpose's constants, grant, refusals, evidence class and `R3C_CONTRACT_SHA256`.
- **Tests:** synthetic fixtures and TEST_ONLY keys only; no test reads the real source; only the pinned root and the validator's repository-root constant are monkeypatched (T00 card §2.2), plus, in the driver tests, the compiled constants the existing driver tests already patch in their TEST_ONLY code root (`test_t00_screen_driver.py:60-63`, `:119`, `:138`) and their successor counterparts (`R3C_CONTRACT_ID`, `R3C_STARTUP_POLICY_ROW`, `STEP12_RNG_ROOTS`).
- **Red-first:** each row test `test_<row>` is committed and recorded failing on the packet base through the launcher, then passing on the build, with a passing twin. A row that cannot be made red on its base is a stop (§6), except the regression rows Y5 and W2, which are green on base by design and are evidenced by green records only. A packet built early against §3 re-takes its red and green records on its final rebased base before its PR opens (T00 card K-5).
- **Launcher records:** `.\fp.ps1 python -m pytest <files>` (or `python -I scripts/fp.py python -m pytest <files>`), each citing its `record.json` with `status: completed`, `verification_exit_code` and `source_stable`; RED per T00 card F7.
- **Review:** one Codex review per packet PR at the exact head (merge-train rules), then coordinator acceptance. More than three rounds each with two or more P1/P2 findings goes to the coordinator (§6).
- **Branch:** `claude/t00-successor-<packet>`, cut from `origin/main` after its §4 dependencies merge; one writer.

### §2.3 P-S1 — the size vector in sizing and replay

- **Builds:** `LegSize` per leg and `SizeVector` (all four legs; frozen dataclasses holding only int, str, tuple or Enum fields, so they pass `_execution_snapshot` (`production_source.py:1013-1061`) unchanged; rationals are kept as reduced `"n/d"` strings and parsed to `Fraction` where used):
  - Aegis: `base` integer 0..8; `adds` (no-op, Aegis has none).
  - Striker: `risk_multiplier`, `cap_reserve_multiplier` (rationals in [0, 1], given as `"n/d"` strings, never floats); optional `max_base` 0..22. Base = min(floor(risk × scale × lifecycle × m / per-contract risk), floor(cap_alloc × c / (1 + add%)), `max_base`), exact rationals.
  - Vanguard: `base_by_port` `{"1": 0..1, "2": 0..2}`; base = floor(v(q) × scale) when AUTHORIZED.
  - ORB: `base` 0 or 1, never scaled in protected mode (unchanged rule).
  - `adds` per leg: `UNCHANGED`, `OFF_WHEN_PROTECTED` or `OFF`. Never turns on an add today's rule refuses.
  - `validate_size_vector(mapping) -> SizeVector` refuses unknown or missing legs, extra fields, non-integers, floats, values above today's, and a negative or > 1 multiplier. `SizeVector.is_identity` over the quantity table; canonical encoding per S-5.
- **Red-first tests:**
  - `test_Z1`: no `size`, and the identity vector, give today's quantities for every leg × mode × tier × ladder input (matrix twin). Red on base: `size` is not accepted.
  - `test_Z2`: Aegis `base` b gives b in NORMAL and floor(b × 0.40) in PROTECTED.
  - `test_Z3`: Striker multipliers and `max_base`, including the cap term, as exact rationals.
  - `test_Z4`: Vanguard `base_by_port`.
  - `test_Z5`: ORB `base` 0 and 1; protected mode leaves it unscaled.
  - `test_Z6`: each `adds` value against `add_quantity`, NORMAL and PROTECTED.
  - `test_Z7`: a leg at 0 in a synthetic `BookReplay`: every entry is rejected "zero policy quantity", no order, no capacity reserved, no takeover triggered, no exception; another leg's admission uses the freed capacity.
  - `test_Z8`: `validate_size_vector` refusals, one case each, including each non-canonical encoding of S-5; `is_identity` true on directly constructed objects that give today's quantities.
  - `test_Z9`: the `:309` cap-term diagnostic and the recorded `sizing_inputs` row use the vector; `cap_binds` reports the cap term only, and a binding `max_base` is recorded separately.
  - `test_Z10`: the replay's add path (`replay.py:603`) in a synthetic `BookReplay`: `adds` `OFF` rejects every add intent, `OFF_WHEN_PROTECTED` rejects it in PROTECTED only, `UNCHANGED` matches today's add.
- **Regression:** `tests/ops/test_book_policy.py`, `tests/ops/qualification/test_replay.py`, `tests/ops/qualification` unchanged in outcome.
- **Lane:** CC solo. Risk-control code consumed by the rail (Rule 0); never GLM.
- **Depends on:** PS-1, PS-2.
- **Return:** §6, plus the §3.1 interface as built.

### §2.4 P-S2 — startup policy v2 schema and the source path

- **Builds:** `parse_startup_policy` accepts v1 unchanged and `qualification-source-startup/v2`, which is v1's fields plus `sizing`, validated by `book_policy.validate_size_vector`. Every v1 rule still applies (fresh-once construction, 80-micro caps, `AUTHORIZED` only, four legs, weekday origin). `StartupPolicy` gains `size_vector` (identity for v1). `_engine` passes it to `BookReplay`.
- **Red-first tests:**
  - `test_Y1`: a v1 policy parses to today's `StartupPolicy` with the identity vector, and a synthetic r3c-shaped source replays byte-identically to base (fixture digests).
  - `test_Y2`: a v2 policy parses; each v1 rule still refuses its own violation under v2.
  - `test_Y3`: a v2 policy with a bad `sizing` is refused with `validate_size_vector`'s reason; extra and missing fields refused.
  - `test_Y4`: a synthetic source with a v2 policy passes the vector to `BookReplay` (spy on construction).
  - `test_Y5` (regression row): the seven sealed methods' source hashes equal `SEALED_SOURCE_SHA256` (existing `test_K7`, re-run as the row's evidence).
- **Regression:** 2026-09-30 A1–A23 and the P7 tests unchanged in outcome.
- **Lane:** CC solo (P7 closure). Never GLM.
- **Depends on:** P-S1 merged.
- **Return:** §6, plus `git diff -U0` of `production_source.py` showing no hunk inside a sealed method.

### §2.5 P-S3 — the successor purpose in the screen authority

- **Builds:** a purpose profile table: purpose → (grant, evidence class, chain entry, contract rule, expressions rule). The original row is today's behaviour exactly. The successor row:
  - purpose, grant and evidence class per S-7; refusals unchanged;
  - `PREREG_CHAIN` = (#581, #733 path); entry per S-4;
  - contract rule per S-3, applied in `_check_source`, `_check_p7` and `require_validated_screen_authority`;
  - `parameters.expressions` = `{"base": "DECLARED_BOOK", "size_vector_sha256": <hex>}`. In `_check_source`, the receipt's `source_startup_policy` bytes are read from `artifact_root`, checked against the receipt's role digest, and parsed; the schema must be v2, the vector not the identity (S-5), and `sha256(canonical_json_bytes(sizing))` must equal `size_vector_sha256`;
  - RNG roots disjoint from step 12's (S-5);
  - everything else as the original: A5/A6 hashes, values block, §3 cells, Status, A3 answers, P7 binding, budgets, run root.
- **`PARAMETER_CHANGE` under the successor (Q3):** any change beyond the frozen size vector. The checks above are its enforcement: the vector is bound three ways (pre-registration values block, authority, signed r3d), every other contract role must equal r3c's, every other parameter has the original rules, and the grant is once.
- **Red-first tests:**
  - `test_W1`: successor constants and closed document; mixed purpose/grant/evidence class refused.
  - `test_W2` (regression row): a #581 authority under the original purpose validates exactly as at base (fixture); the existing `test_screen_authority.py` cases are unchanged in outcome, except the `:474` assertion amended in §2.1.
  - `test_W3`: under the successor, receipt, authority and P7 record must carry the same contract digest; r3c's digest refused under the successor; a successor digest refused under the original.
  - `test_W4`: an r3d with one other role changed (for example `cost_model`) fails the derivation check.
  - `test_W5`: `size_vector_sha256` mismatch; v1 policy; identity v2 vector; role bytes not matching the receipt digest; a v2 policy whose fields other than `sizing` differ from r3c's v1 policy. Each refused.
  - `test_W6`: a step-12 root, or the step-12 probe root, refused under the successor.
  - `test_W7`: cross-binding of purpose and chain entry refused both ways.
  - `test_W8`: a successor pre-registration with one byte changed in A6 refused (A9 under the new purpose).
  - `test_W9` (driver file): a successor authority on the TEST_ONLY seam runs to FINAL after a consumed #581-path run; `PREREG_CONSUMED` and `SCREEN_ATTEMPT_OPEN` unchanged.
  - `test_W10`: `require_validated_screen_authority` refuses a source contract other than the authority's bound digest under the successor.
- **Lane:** CC solo (trust and auth). Never GLM, never Cursor.
- **Depends on:** P-S1 merged (`validate_size_vector`, `is_identity`); may be built from wave 1 against §3.1 and re-take records on its final base.
- **Return:** §6, plus the purpose profile table as built.

### §2.6 P-S4 — verdict

- **Option A (recommended, S-6):** no packet. §1.1 shows the binding verdict, and the stopping rule's (a), need no new code.
- **Option B (only on Joshua's choice):** `verdict.r1_alone` adds a reported per-population R1-alone bust and pass tally under A5 (1) to `Labelled.descriptive`. It never enters the label. `test_V5`: a hybrid fixture where the R1-alone tally differs from both assignments; the label is unchanged. It changes the frozen §3.7 interface and `results.json` bytes, so it needs Joshua's approval. Lane: GLM-eligible on synthetic rows from a `.claude/worktrees/` `workdir` with no private data, coordinator reads the full diff; CC if GLM fails twice.

### §2.7 P-S5 — the #733 rewrite (docs)

- **Writes:** #733 only, at its current path (`PREREG_CHAIN` names the path; keeping it avoids a second rename).
- **Builds** (#581's structure, so that `_check_prereg` and `_check_sections` accept it once ratified):
  - **D1:** title, blank line, then the Status line `` **Status:** `DRAFT — NOT RATIFIED.` ``; at ratification `` `RATIFIED <date>` `` (Q5: the status word changes from FROZEN).
  - **D2:** `### A5` and `### A6` byte-identical to #581's, followed by `## §3`; their hashes equal `a8f6f25e…391b` and `b3bdc77b…17d9`.
  - **D3:** `## §3` with items 1–8 (item 6 withdrawn) whose last cells read exactly as #581's (`values block: ...`, T00 card K-4 ruling); `## §6` with one `t00-step2-values/v1` fence, the `- **Ruling:**`, `- **OD-1 / OD-2:**` and `- **Ratifying commit SHA:**` fields.
  - **D4:** the configuration fields C-1…C-7, K₀, the reader log (adding RM-1, the T2 rows from map §6, and every reader of the step-12 run directory, design §4.5) and G4–G6 kept outside A5/A6, with §1.1's mapping and its label-subtype note stated. #733 §7's "distinct RNG tag" becomes "the compiled tag with roots disjoint from step 12's" (S-5).
  - **D5:** OD-1 is the D-feed reading for a successor verdict (#733 §8 item 5); OD-2 is the base expressions (C-2). The stopping-rule summary and the decision-tree pointer stay.
  - **D6:** the anchors the copied A5/A6 text cites exist in #733: A1 (the successor expressions: r3d and the size vector), A2, A3, A4, §1b, §3 items 2, 3, 7 and 8, and §4 OD-1/OD-2, with A6 immediately followed by `## §3` (`verdict.py:44`, `:56-58`).
  - **D7:** #733's §10 hooks gain the section-hash check (§10 below) and the authority's ratification-completeness check.
- **Acceptance:** `check_brief.py --type brief` well-formed; the §10 hash hook prints #581's two hashes; every C-n and OWED field still reads OWED (nothing frozen here).
- **Lane:** CC (governance text with exposure accounting). Codex review. No GLM.
- **Depends on:** PS-1. Parallel with every code packet; must merge before §7 step 4, not before H′.

## §3 — Frozen interfaces

### §3.1 New interfaces (card proposals; the coordinator re-states them in each ticket)

- `book_policy.LegSize`, `book_policy.SizeVector` (frozen dataclasses; `.leg(leg_id) -> LegSize`, `.is_identity`); `book_policy.IDENTITY_SIZE_VECTOR`; `book_policy.validate_size_vector(mapping) -> SizeVector`.
- `book_policy.entry_quantities(..., size: LegSize | None = None)`, `book_policy.add_quantity(..., size: LegSize | None = None)`; `None` is today's behaviour.
- `replay.BookReplay(..., size_vector: SizeVector = IDENTITY_SIZE_VECTOR)`.
- `LegSize`/`SizeVector` field types: int, str, tuple or Enum only (P-S2's `_execution_snapshot` constraint); `base_by_port` is stored as a tuple of (port base, size) pairs.
- `production_source.StartupPolicy.size_vector`; startup schema `qualification-source-startup/v2` = v1 fields + `sizing`:
  `{"aegis_6j": {"base", "adds"}, "dj30_mym_p250": {"risk_multiplier", "cap_reserve_multiplier", "max_base"?, "adds"}, "vanguard_mgc": {"base_by_port", "adds"}, "orb_mnq_v7": {"base", "adds"}}`.
- `screen_authority`: successor constants (S-7); `PREREG_CHAIN` of two entries; `R3C_CONTRACT_ID`, `R3C_STARTUP_POLICY_ROW` (the complete artifact row; public values from the coordinator); `STEP12_RNG_ROOTS`; `parameters.expressions` as above; `size_vector_sha256 = sha256(canonical_json_bytes(sizing))`.

A packet that needs a different signature stops and returns (§6).

### §3.2 Interfaces the design freezes, and what this card does to each

| Frozen item (owner) | This card | Joshua's approval |
|---|---|---|
| `book_policy.py`, `replay.py` on the design §9 forbidden list | Edited by P-S1 (default = today) | **Yes**, with card approval |
| `production_source.py` outside the screen entry points (design §9) | P-S2 edits `parse_startup_policy`, `StartupPolicy`, `_engine`; sealed methods unchanged | **Yes**, with card approval |
| Compiled r3c digest in rows A6, A7 and `require_validated_screen_authority` | Unchanged for the original purpose; the successor uses S-3's derivation | **Yes** (S-3) |
| Row A8 "the compiled chain's last entry" | Per-purpose entry (S-4) | **Yes** (S-4) |
| Row A11 `expressions = "DECLARED_BOOK"` | Unchanged for the original; successor value bound to the vector | Covered by Q3 |
| Purpose, grant, refusals, evidence class (row A1) | Original unchanged; new successor set | Covered by Q3 (names: S-7) |
| A5/A6 hashes, spans, values-block name, §3 cells, Status regex (rows A8, A9) | Unchanged | Covered by Q5 |
| Startup policy v1 schema, `AUTHORIZED`-only rule | Unchanged; v2 added | Covered by Q2 |
| Verdict interface §3.7 and `results.json` bytes | Unchanged (option A) | Only for option B |
| Journal, ledger, state, plan, driver interfaces (T00 card §3.3–§3.6a) | Unchanged | No |
| P7 bootstrap and closure rules; `SOURCE_REFUSALS`; `SOURCE_PURPOSES`; r3c bytes | Unchanged; r3d validates under the existing source purpose | No |
| Protection cell, `dd_protection`, `BASE_RISK`, locked Pine and ports | Unchanged | No (any change is outside this card) |

## §4 — Hypothesis, integration order and head H′

**H′ (build):** with P-S1, P-S2 and P-S3 merged (and P-S4 if option B), every row Z1–Z10, Y1–Y4, W1 and W3–W10 (and V5) has a red-on-base, green-on-build launcher record, and Y5 and W2 green records; `fp test-ops` (which covers `tests/ops/qualification` and every `book_policy` consumer test), `tests/ops/test_book_policy.py`, `tests/test_remc_series_quantity_parity.py`, `tests/core/test_mc_mode_switching.py`, the parity suite with real inputs read in place, and `fp check` are green at H′; the sealed methods equal `SEALED_SOURCE_SHA256`; and the raw diff from the pre-build base to H′ names no §2.2 forbidden file. **Reject if** a row cannot be made red on its base, a row is green only with a forbidden edit, the sealed hashes change, or the forbidden-file diff is non-empty without a recorded D2-style exception. **Revert trigger:** any existing qualification, book-policy or replay test changes outcome at H′, except the `test_screen_authority.py:474` assertion amended under §2.1.

**Dependency graph:**

```
PS-1 card ─┬─► P-S1 ─┬─► P-S2 ─┐
PS-2 #757 ─┘         └─► P-S3 ─┴─► H′ ─► §7
P-S5 (docs, parallel) ─────────────────► §7 step 4
```

**Merge order** (each its own PR, opened by the coordinator, merged by Joshua after Codex clean at the exact head and CI green):
1. P-S1; P-S5 any time.
2. P-S2 and P-S3, each rebased on P-S1, in either order (disjoint files).
3. P-S4 option B, if chosen, any time before H′.

**Definition of H′:** the first `origin/main` commit containing P-S1, P-S2 and P-S3 (and P-S4 if chosen), at which the coordinator's H′ check (§10) is green with cited launcher records. The coordinator records its 40-hex SHA in §8; Joshua accepts it. Later commits on `main` do not move H′. A fix to any file in the P7 closure or `screen_authority.py` after H′ defines a new H′ and repeats §7 step 1, then steps 5–6 (step 5 only if the r3d approval window requires it), and step 7 if the authority was already signed. The #733 freeze is not repeated.

## §5 — Forbidden moves (not authorized by this card)

- Any code before Joshua approves this card; any packet before its §0 prerequisites are recorded in §8.
- Any edit outside the packet's §2.1 footprint or to a §2.2 forbidden file; any change to a sealed method, `runner.py`/`bracket.py` semantics, `SOURCE_REFUSALS`, r3c's bytes or the pinned key.
- Changing the protection cell, `DD_TRIGGER`/`DD_SCALE`, `BASE_RISK`, lifecycle multipliers, locked Pine, ports or effective inputs.
- Any real-source replay, screen, probe or Monte Carlo; any test that reads the real source. The only real-source runs are §7's P7 and the one screen, each under its own GO.
- Choosing or proposing a vector (Q1 is Joshua's), sweeping vectors, or screening more than one configuration.
- Anything for R1/R2 (on hold).
- Editing #733 outside P-S5, or #581 at all; editing the stopping rule or decision tree.
- An agent signing, generating, holding or touching an operator key, approval or act.
- Merging, opening PRs (coordinator only), pushing to `main`, freezing or ratifying anything.
- GLM for P-S1, P-S2, P-S3 or P-S5, or for any ticket touching trust, auth, sizing, private inputs or the P7 closure.
- Publishing a private value: vector values beyond what Joshua makes public, result counts, rates, keys or P&L.

## §6 — Return taxonomy and stop conditions

Each packet returns exactly one status to the coordinator:
- **DONE:** every owned row red-on-base and green-on-build (regression rows Y5 and W2: green only), regression unchanged, footprint clean.
- **DONE_WITH_CONCERNS:** all of DONE, plus a named non-row concern. A failed row is never this.
- **NEEDS_CONTEXT:** a missing fact, prerequisite, ruling or interface decision. Name it.
- **BLOCKED:** context-problem, capability-problem, scope-problem or plan-itself-wrong, with the exact obstruction.

The return carries: branch, base, head SHA; `git diff --stat` and `--name-only` (checked against §2.1); per row, the red and green `record.json` paths; regression records; concerns.

**Stop and return (do not work around):** a footprint or interface change is needed; a forbidden file would change; a row cannot be made red on its base; a hook or guard refuses an action; two failed corrections of the same issue; more than three review rounds each with two or more P1/P2 findings (coordinator adjudicates); a second writer on the branch. The coordinator's verdict per packet is RESOLVED (every owned row holds) or FALSIFIED (named rows fail).

## §7 — After H′: the governance chain

Each operator act below needs its own GO. Agents never touch a key.

| # | Step | Owner | Needs | Estimate |
|---|---|---|---|---|
| 1 | **H′ check** (§10) from a detached worktree at H′ (`core.autocrlf=false`, clean with `--untracked-files=all`); Joshua accepts H′ | coordinator, Joshua | §4 | 0.5 d (about 3 h of runs) |
| 2 | **r3d assembly:** startup policy v2 bytes with Q1's vector; r3d = r3c with only that artifact row and `contract_id` changed; derivation check (S-3) run locally; `size_vector_sha256` computed | coordinator | PS-3 (Q1) | 0.25 d |
| 3 | **K₀ ledger entry:** the coordinator opens a PR registering this book's lineage in `discovery_manifests/` (map §6), merged before step 4 | coordinator, Joshua merges | PS-3 | 0.25 d, parallel with step 2 |
| 4 | **#733 freeze (ratification), before any replay over r3d** (#733 §R; P7 replays a real path over r3d's contract, `p7_driver.py:1-6`): Joshua fills Q1/C-1…C-7, K₀, the reader log, G4–G6 and Q6, Q7 (depth), `pass_floor_halves`, OD-1/OD-2 and the values block (with `size_vector_sha256`, new RNG roots, budget); C then C′ per #581's procedure | Joshua | P-S5 merged; steps 2, 3 | 0.5 d |
| 5 | **Fresh source approval over r3d** (`APPROVE_T00_SOURCE_CONTRACT`, key `source:1ebae5d45bc51280`), verified with `verify_detached_approval(allow_test_authority=False)` | Joshua signs | step 4 | 0.1 d |
| 6 | **P7 at H′ over r3d**, one run by the accepted P7 procedure. `p7_acceptance.json` is write-once (`coordinator.py:1290-1292`, `P7_ACCEPTANCE_EXISTS`), so the current acceptance is first renamed aside in place, not deleted, on Joshua's GO (the 2026-10-10 precedent, T00 card §8); step 12's attestation hashed that file's earlier version, and step 12's window closes 2026-10-14 in any case. Then `t00_screen accept-p7` | coordinator | steps 1, 5 | 0.25 d (about 1 h) |
| 7 | **Screen authority** under the successor purpose, over r3d, the P7 record and ratified #733; `validate_screen_authority` ISSUED | Joshua signs | steps 4, 6 | 0.25 d |
| 8 | **One run**, `--workers 8`, one segment planned; no read of the run directory before `finalize` (row X2) | executor | step 7 | 9–44 h |
| 9 | **`finalize`, then `verify`**, inside both approval windows | executor | step 8 | about 0.1 d |

**Approval windows.** Step 12 took about 8.35 h at N = 1,002 and `--workers 8` (T00 card §8; map §1 item 8). A cut book passes and busts later, so its paths run longer; the map's range is 9–44 h. The design's upper bound (c = 320 CPU-s per path) is about 43 h at W = 8, and the signed budget covers it.
- **Screen authority:** `expires_at` at least 72 h after the planned start. That covers 44 h, `finalize` and `verify` (about 15 min last time), and one pause and resume. Start by `expires_at` − 72 h.
- **r3d source approval:** the receipt must stay unexpired through `verify` (R-INT-1: no post-window re-audit). Sign it immediately before step 6 with a 7-day window; the run must start by its expiry − 72 h. If the authority signature slips past that, Joshua signs a renewal over the same r3d bytes.
- **Budget:** at N = 1,002, the #581 formula gives the same values (961,920 path CPU-s; 11,300 overhead at W = 8, S = 3, R = 8). Recorded in #733's values block at freeze (Q7).

**After the run:** the coordinator reports the verdict label, the hashes, and whether definition (a) fires (the H2 pessimistic bust comparison, read privately from `results.json`; label only). The stopping rule on the T00 card governs.

## §8 — Approval, rulings and H′ record

- **Card approval:** *pending.*
- **Operator rulings, Joshua, 2026-10-10, directly to the Deployment Coordinator: "agreed on Q2, Q3, Q5"** (recorded as relayed in this card's dispatch):
  - **Q2:** "the successor size vector (per-leg whole-contract size plus an adds rule) lives in a signed v2 of the source startup policy, an r3d artifact covered by the existing source-approval chain. No locked Pine, port, dd_protection constant or BASE_RISK is touched."
  - **Q3:** "a NEW screen-authority purpose for successor screens, distinct from T00_STEP3_SELECTED_BOOK_SCREEN. Under it, PARAMETER_CHANGE means 'any change beyond the size vector frozen in the successor pre-registration' (de-risking allowed, re-optimization refused). The original purpose and its refusals stay unchanged for #581."
  - **Q5:** "rewrite #733 to #581's structure (status word, A5/A6 sections, values-block name) so that it passes the authority's existing pre-registration checks, rather than generalizing those checks. The successor path is appended to PREREG_CHAIN. The rewrite itself is a separate docs packet in the card; don't edit #733 in this PR." This departs from the map's Q5 recommendation (generalize); the ruling governs.
- **R1/R2: ON HOLD** (Joshua, 2026-10-10). The successor is judged on (a), the pessimistic A5 assignment. This card builds nothing for R1/R2.
- **Still OPEN:**
  - **Q1 — OPEN.** Which whole-contract vector stands for "half size", and whether the 1-lot legs ORB and Vanguard are kept at 1 or dropped. Decided after the Tier-2 report. The build works for any vector, including a leg at 0.
  - **Q6 — OPEN (OWED, Joshua to confirm).** Recommendation: G5 reported and non-binding.
  - **Q7 — OPEN (OWED, Joshua to confirm).** Depth stays N = 1,002 per population (T00 card §8) unless Joshua re-rules.
  - **K₀ — OPEN (OWED, Joshua to confirm).** Recommendation: K₀ = 8, this successor K = 9 (map §6).
  - **Card decisions S-1…S-7** (§0.5), answered with card approval; S-3, S-4 and S-6 option B change frozen design items (§3.2).
- **Prerequisites:** PS-2 #757 at: *pending.* PS-3 Tier-2 report SHA-256 and Q1: *pending.* PS-4 P-S5 merged at: *pending.*
- **Packet heads:** *pending.*
- **H′:** *pending.*

## §9 — Effort and critical path

| Packet | Effort (CC session days, including CI at 22–32 min per push and Codex rounds) | Lane |
|---|---|---|
| P-S1 sizing | 1.5 | CC solo |
| P-S2 startup policy v2 | 1 | CC solo |
| P-S3 screen authority | 1.5–2 (built from wave 1; 0.5 after P-S1 to rebase and re-take records) | CC solo |
| P-S4 verdict | 0 (option A); 0.5 (option B) | GLM-eligible (B only) |
| P-S5 #733 rewrite | 0.5 plus Joshua's review | CC |
| H′ check | 0.5 | coordinator |

**Critical path from card approval:** P-S1 (1.5 d) → P-S2 or P-S3 rebased (1 d) → H′ check (0.5 d) = **about 3–4 calendar days to H′**. Then §7: r3d and K₀ entry (0.25 d) → #733 freeze (0.5 d) → approval and P7 (0.35 d) → authority (0.25 d) → run (0.4–1.9 d) → finalize and verify (0.1 d) = **about 2–3.5 days**. **Total about 5–7.5 calendar days**, if Q1 is answered by the time H′ is accepted; any later Q1 date adds its delay after H′. The map's estimate was 6–9 days counted from the Tier-2 report; building before Q1 is what saves the difference.

## §10 — Audit hooks

```bash
c=docs/briefs/handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md
# Card form and authority (expect RESULT: well-formed; exit 0).
python -I scripts/fp.py python scripts/check_brief.py --type handoff "$c"
python -I scripts/fp.py python scripts/check_handoff_brief_form.py
python -I scripts/fp.py python scripts/check_handoff_authority.py "$c"

# Per packet, at return: footprint = its §2.1 row exactly.
git diff --name-only "$(git merge-base origin/main HEAD)" HEAD

# P-S2: no hunk inside a sealed method; at H′, test_K7 passes.
git diff -U0 "$(git merge-base origin/main HEAD)" HEAD -- ops/c1_rail/qualification/production_source.py
python -I scripts/fp.py python -m pytest tests/ops/qualification/test_production_source.py -k K7 -q

# P-S5: the rewritten #733's A5/A6 hashes equal #581's (expect a8f6f25e...391b then b3bdc77b...17d9).
git show HEAD:docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md | python -c "import sys,hashlib;b=sys.stdin.buffer.read();i=lambda m:b.index(m)+1;a5,a6,s3=i(b'\n### A5'),i(b'\n### A6'),i(b'\n## \xc2\xa73');print(hashlib.sha256(b[a5:a6]).hexdigest(),hashlib.sha256(b[a6:s3]).hexdigest())"

# At H′: forbidden files untouched (expect no output). BASE = the pre-build origin/main SHA in §8.
git diff --name-only "$BASE" "$H2" -- ops/c1_rail/qualification/{contract,trust_domain,p7_evidence,p7_driver,runner,provider,blocks,paths,regime,bracket,model}.py ops/c1_rail/qualification/t00_screen/{state,journal,plan,coordinator,worker,__main__}.py scripts/t00_screen_label_check.py scripts/t00_screen.py ops/c1_signal_daemon/book_adapters.py core/ docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md

# At H′: the original purpose and its anchors are unchanged.
rg -n "^SCREEN_PURPOSE|^SCREEN_GRANTS|^R3C_CONTRACT_SHA256|PARAMETER_CHANGE|^PREREG_CHAIN" ops/c1_rail/qualification/screen_authority.py
rg -n "^A5_TEXT_SHA256|^A6_TEXT_SHA256" ops/c1_rail/qualification/t00_screen/verdict.py

# At H′: the protection cell is unchanged (expect the fixed 0.40 scale and the require_policy check).
rg -n "CANDIDATE_SCALE =|def require_policy" ops/c1_rail/book_policy.py

# At H′: full regression, each with its record.json.
python -I scripts/fp.py test-ops
python -I scripts/fp.py --workers 2 python -m pytest tests/ops/test_book_policy.py tests/test_remc_series_quantity_parity.py tests/core/test_mc_mode_switching.py tests/ops/test_book_adapters_parity.py -q
python -I scripts/fp.py check

# No private value in this card (expect no output).
rg -n 'P&L =|\$[0-9]{2,}|account [0-9]' "$c" | grep -v 'rg -n'
```

## Pre-mortem

- **Most likely failure:** S-3's derivation check needs r3c's artifact-row form exactly, and the contract's canonical form makes "restore two fields" harder than it looks (row ordering, a path change). P-S3 stops at §6; the fallback is a compiled r3d digest, which makes the build wait for Q1.
- **Second:** a leg at 0 interacts with takeover or capacity in a way Z7 does not cover. The stop is a failed Z7 twin, not a workaround.
- **Third:** a reviewer finding that §1.1's implication misses a case; the fallback is P-S4 option B.
- **What makes it moot:** Tier 2 returns row 6, or row 4 alone (#733 §1 returns to Joshua); Q1 picks a signal reshape (map Q8, out of scope); Joshua stops successor work.
- **Cost:** three code PRs (four with option B), one docs PR, one P7 run, two signatures, one screen run.
