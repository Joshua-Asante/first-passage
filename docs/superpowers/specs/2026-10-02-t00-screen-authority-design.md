# T00 screen authority: design

**Date:** 2026-10-02.
**Status:** DRAFT — design only; Joshua approves before any code (operator ruling A1 2026-10-02).
**Changelog:**
- Revision 2, 2026-10-02: folds review of 101cf1b.
- Revision 3, 2026-10-02: folds the round-2 review of 09486ef (1 P1, 10 P2, 6 P3). Rebuilds §3, §4 and §5.5–§5.6 on the §2.2 invariant table, with one transition function for run state and one cross-field check per record. Hoists the integrity check to per-worker epochs, records the second timing probe and replaces every cost figure, records the relayed sitting-2 rulings on #581 OD-1 and OD-2, compresses §12 to 11 decisions, and adds Appendix A (finding → invariant).
- Revision 3.1, 2026-10-02: applies the round-3 judge's 10 edits (final round under the stopping rule); no further review round.

This document adds no code and admits no file for editing. §9 lists the files a later, operator-approved build card may admit.

**Authority** (operator rulings, Joshua, direct, 2026-10-02 ~01:50Z, "all recommended"):
- **A1.** T00 step 3 cannot run on current code. The order is fixed:
  1. lift the #611 and A9-PREP holds;
  2. **design** a T00 screen authority: a new contract class that Joshua signs, bound to r3c's 25 inputs and to the ratified #581, and still refusing stages, seal, admission and deployment;
  3. Joshua approves the design **before any code**;
  4. build it (driver, A5 counting, A6 verdict);
  5. one P7 re-run at the merged head, under a fresh source approval;
  6. set and ratify #581 §3;
  7. Joshua signs the screen authority;
  8. run step 3 once.
- **A2.** Amend [spec 2026-09-30](2026-09-30-t00-source-only-contract-design.md) at `:124` and `:358` so that a signed screen authority may use replays built from r3c. Approved in principle and decided with this design. The amendment text is §11 here, as a proposed dated addendum; this PR does not edit that spec.
- **A3.** ORB-3 and VAN-3 are answered before any step-3 output exists. This ruling is standing.
- **A4.** One real-source timing probe, measuring wall and CPU time only and no outcomes, is allowed before #581 is ratified. It ran as a timed P7 re-run (§6.1).
- **Second probe.** Joshua's direct answer on 2026-10-02 (sheet 2 item 1, "all recommended"): "one more probe at two window lengths, wall and CPU only". It ran (§6.2). Any further probe needs its own dated answer (row G4).

**Relayed, confirmation pending** (sitting 2; Joshua's confirmation is pending in coordinator (3)'s chat):
- **#581 OD-1 = (c), label-sensitive.** Operator acceptance satisfies D-feed (a) only for an `UNDETERMINED`-dependent NO-GO; a robust NO-GO needs (a) amended. It is recorded at the D-feed owner before step 3 returns (§8 step 9).
- **#581 OD-2.** Screen the declared book, not the editions; a GO speaks to the declared expressions only. **This design requires it** (row A11, §12 item 3): choosing the editions voids the r3c binding and this design.

**Precedent:** [T00 source-only contract design](2026-09-30-t00-source-only-contract-design.md), revision 4.2, operator-accepted. Its structure, attribution rule and refusal discipline carry over here.

**Review path:** the coordinator reviews, then one narrow Codex review, then Joshua approves (A1 step 3).

**Code read at:** `origin/main@152716d`. Revision 3 re-opened every cited line there. `git diff d5d559b 152716d` touches no cited file, and the cited `ops/`, `tests/` and `scripts/` files are byte-identical to `d716106`, where both timing probes ran. #611 (OPEN, head `76cc8c1`) edits `production_source.py` and `test_production_source.py`; its line numbers are re-anchored after it merges.

**Pre-registrations read:** #581 at its PR head `f0208f3`, `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md`, status DRAFT; the two A3 successors at `152716d`. This design binds #581 by section and hash. It restates only the #581 values named in row G2.

**Private-value rule.** This file holds no Pine, port body, private value, account identifier or P&L. The r3c digest, the key ID, the P7 record digest, the probe-harness digests, the timings and the dates below are not private values.

---

## 0. Design basis: three proposals judged

Three proposals were drafted independently, each through one lens. Each was scored on four criteria:
- whether it keeps the r3c fence and the accepted P7 machinery intact;
- whether it keeps #581 A4 and A6 true as written;
- the size of the trust surface it adds;
- whether its crash and compute story is complete.

| Proposal | Score /10 | Strength | Weakness |
|---|---|---|---|
| **Authority lens** (backbone) | **8.5** | Adds one gated capability on `ProductionSource` that returns an unsealed `BracketReplayResult`. The **unchanged** `runner.evaluate_replay` scores it, so #581 A4 ("through `runner.evaluate_replay`") stays literally true. It edits nothing in `contract.py`, `trust_domain.py`, `book_adapters.py` or `runner.py`. It has the most precise schema and validation order. | Its crash and resume model is thin. It binds the r3c *approval* digest, which blocks approval renewal. It pins the A5/A6 hash without settling when the text freezes. |
| **Integrity lens** | 8.0 | Spots several real problems: a hand-built `AcceptedP7Record` proves nothing (`p7_evidence.py:435-440`); `code_head` voids acceptance at any other head; A10b misses `_replay_raw` and `_engine`; P7 says nothing about the kernel. Also contributes the A3 digest binding, a one-line console, and coordinator recompute with a hash-derived re-execution sample. | Its "closure-only enumeration" misses modules imported lazily inside functions (`_engine` imports at call time, `production_source.py:1239-1245`). It voids a whole attempt on any infrastructure crash. |
| **Execution lens** | 7.0 | Best state model: crash windows, hash-chained journal, timestamp-free `results.json`, budget across segments, probe cost model, deterministic re-partitioning. | Duplicates the scorer on top of sealed outputs. That makes #581 A4's wording false, needs #581 edits, and opens a drift surface. Its stated reason, keeping the P7 closure untouched, is moot: a P7 re-run is already planned (A1 step 5). It also has no in-run probe, although #581 A6 names one. |

**Backbone:** the authority proposal. **Grafted:** from the integrity proposal, the A10b widening, the A3 binding, the console policy, coordinator recompute and re-execution, the rule that only record bytes are accepted, and the refusal on an F1 source. From the execution proposal, the state model and journal, crash windows, budget accumulation across segments, the probe cost model, deterministic re-partitioning, and approval expiry held only in the approval payload.

**Conflicts resolved** (C1–C8 are conflict numbers; the capability invariants are rows K1–K10):

| # | Conflict | Resolution | Why |
|---|---|---|---|
| C1 | Scoring: a duplicated scorer over sealed rows (execution) against a raw `BracketReplayResult` from a gated method (authority, integrity) | **Gated `screen_bracket`**, scored by the unchanged `evaluate_replay` | #581 A4 and A6 name `runner.evaluate_replay` and `runner.py` lines. A duplicate would need #581 rewording and a differential test forever. The edit to `production_source.py` falls in the P7 re-run that is already planned. |
| C2 | Whether the authority binds the r3c **approval** digest (authority) | **It does not.** It binds the r3c **contract** digest and the P7 record digest. Any valid pinned OPERATOR approval over the r3c bytes may build the source. Each one is recorded in the attestation. | Every approval over r3c is an equally authoritative signature over the same bytes. Binding one approval's digest would make an expiry mid-run unrecoverable even when Joshua renews. |
| C3 | P7 check at launch: re-run `accept_p7_record` (integrity), or check bindings only | **Check bindings only, with no re-execution, plus two compiled checks:** the record's `bootstrap_sha256` equals the compiled `P7_BOOTSTRAP_SHA256`, and its `code_closure_sha256` recomputes from its `loaded_closure` (row A7). The signing packet carries the acceptance evidence. | Re-executing would be a second P7 run, which A1 does not allow. Joshua's signature authenticates the bytes he is shown, not that a reproduction happened; §13 names that residual. |
| C4 | Screen code identity: a signed `screen_closure_sha256` from an enumeration (integrity/execution), or the commit | **Bind `code_head` H (clean tree) plus the interpreter.** Every worker records its loaded closure, and all epochs must agree (row K6). | A git commit binds every first-party byte, including modules imported lazily. Enumerating without running would under-record them. |
| C5 | Crash disposition: VOID the attempt (integrity), or resume (execution, authority) | **Deterministic resume.** A non-deterministic stop never ends a run: it STOPs, or HALTs for Joshua's act after repeats. Only a deterministic #581 A6 cause, evidence of corruption, a key-lifecycle event or a signed act is terminal (row S9; §12 item 7). | Each per-path outcome is a pure function of (receipt bytes, authority bytes, key). A resume draws nothing new and cannot select outcomes. |
| C6 | In-run probe: none (execution), or present (authority) | **Present.** One `probe_root` path is timed in an already-built worker, and path CPU × total paths must fit the path budget (rows B2, B3). | #581 A6 names the budget probe and its refusal. It is also the first timing of a true 1,500-session path (§6.3). |
| C7 | Shard plan: signed into the authority (integrity), or a launch value | **A launch value**, recorded in the ledger | Results do not depend on W (row S16), and a resume may change W. A resume on another machine is impossible anyway: the interpreter binding records an absolute `site_packages_path` (`p7_evidence.py:421`), and the run root is bound (row A6). |
| C8 | Bootstrap: parametrize `p7_evidence` (authority), or a separate copy (implied) | **Parametrize one template.** P7's string is generated from it with P7's parameters; workers check the screen's hash (row K3). | One implementation of the audit hook and recording finder, instead of two security-critical copies. The P7 re-run absorbs the `P7_BOOTSTRAP_SHA256` change. |

---

## 1. Problem

r3c (`a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97`) has purpose `T00_P7_SOURCE_VERIFICATION`. Its `SOURCE_REFUSALS` include `SCREEN` and `MONTE_CARLO` (`contract.py:964-968`), and they are enforced exactly (`contract.py:1086-1088`).

There is no step-3 runner today. The current code blocks the screen at five points:

| Point | What it does | Where |
|---|---|---|
| 1 | `ProductionSource.build` accepts r3c, but `verify_for` raises `SOURCE_ONLY_NOT_QUALIFICATION` | `production_source.py:1037`, `:1184-1191` |
| 2 | On r3c, `replay`, `replay_bracket` and `proof` return the sealed `SourceOnly*` types | `:1203-1213`, `:1215-1237`, `:1265-1294` |
| 3 | `evaluate_replay` refuses anything that is not a `ReplayResult` | `runner.py:23-24` |
| 4 | `_run_stage` draws only qualification-stage seeds and calls a single-run provider | `runner.py:88-123`; `regime.py:12` |
| 5 | `run_bracket` needs an engine-level `build_replay` | `bracket.py:115-134` |

Two more facts shape the design:
- A single-run replay (`run is None`) refuses any instant without a reviewed schedule price (`production_source.py:442-452`, `:475-479`). On the real source, a candidate-edge pass therefore needs the bracket rather than `proof`.
- The production executors are retired or TEST_ONLY (`production.py`, `orchestration.py`).

Widening r3c would change its digest and void the P7 identity that #581 A1 binds. The screen therefore needs a **second, narrower door**: a separately signed object that wraps r3c and does not edit it.

---

## 2. Behavioral contract

### 2.1 What it is

A **T00 screen authority** is a canonical JSON document with schema `t00_screen_authority/v1`. One operator signature under the new scope `APPROVE_T00_SCREEN_AUTHORITY` turns it into a `ValidatedScreenAuthority` receipt.

**What the receipt authorizes, exactly:**
- **One consumer path**, inside a screen-bootstrap worker of a ledgered run (rows K3, K4), on a source built from the bound r3c receipt: `ProductionSource.screen_epoch` once per worker epoch, then `ProductionSource.screen_bracket(path, *, authority, epoch)` → `ScreenBracket` (a `BracketReplayResult` plus each run's deadline flag and consumed splits, §3.3), then `runner.evaluate_replay` on each run, then the A5 counting and A6 verdict functions. This is used **once**, for T00 step 3 under the ratified #581.
- The timing probes (§6) do not use the receipt. Ruling A4 and Joshua's second-probe answer are their authority.

**What it refuses, as a declaration** (enforced by rows A11, K7, K10 and X6):
- qualification stages, Part A, F1 and decision rules;
- seal, admission, deployment and arm;
- four-firm §4 falsifier evidence (#581 §1b);
- parameter changes.

**What does not change:**
- The r3c receipt, `build`, `verify_for` and `_resolve_domain` are unchanged.
- The sealed `replay`, `replay_bracket` and `proof`, and their helpers `_seal`, `_check_path` and `_verify_integrity`, are unchanged. `replay_bracket` still runs the full integrity check on every call (row K7).
- `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py` and `core/` are unchanged.
- Without a screen authority, every statement in the 2026-09-30 spec holds unchanged.

### 2.2 Invariant table

Each row is one claim, the code that enforces it, the one test that violates only that claim, and the owning module. Every test is red-first, asserts the row's code and has a passing twin (§10). Cross-field claims are checked in one function each, with the whole record in hand:
- at launch, `screen_authority._check_bindings` (rows A5–A10);
- over a run, `t00_screen.state.check_record` (ledger, journals, manifest and acts together; rows K6, S10, S13–S15, X3).

Durable run state changes only through `t00_screen.state.advance` (row S1). Every round-1 and round-2 finding maps to at least one row (Appendix A). The prose in §3–§5 points at these rows and does not restate them.

**A. Authority validation** (`screen_authority.validate_screen_authority`; §3)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| A1 | The authority is canonical JSON with the closed field set and the exact `schema`, `purpose`, `grants`, `refusals` and `evidence_class`; every excluded field (§3) is refused | `SCREEN_AUTHORITY_FIELDS` | `test_A1`: an `expires_at` field added to a valid authority | `screen_authority` step 1 |
| A2 | The signature is checked second, before any `git` call or file read: OPERATOR, a pinned `source:` signer, the pinned trust document, scope `APPROVE_T00_SCREEN_AUTHORITY`, subject = the authority SHA-256 | `SCREEN_TRUST_ROOT_MISMATCH`, `SOURCE_KEY_*` | `test_A2`: a TEST_ONLY signer; a spy shows no `git` call ran | `screen_authority` step 2 |
| A3 | Scopes are exclusive: a screen approval or act verifies as nothing else, and nothing else verifies as either | scope check (`contract.py:389`) | `test_A3`: a source-scope approval over the authority digest | `contract.verify_detached_approval` (unchanged) |
| A4 | Unsigned text never reaches `git` unchecked: every commit field matches `^[0-9a-f]{40}$`, every path equals a compiled constant, and `git` runs with `--end-of-options` | `SCREEN_AUTHORITY_FIELDS` | `test_A4`: `prereg.commit = "--output=x"` | `screen_authority` step 1 |
| A5 | Reality is read, never supplied: HEAD, a clean tree (`--untracked-files=all`, `core.autocrlf=false`) and the interpreter come from the validator's fixed repository root | `SCREEN_P7_MISMATCH` | `test_A5`: one untracked file | `_check_bindings` |
| A6 | Source and run root: `source.contract_sha256` equals the compiled r3c digest and the issued, unexpired receipt's; `run_root_sha256` equals the SHA-256 of the resolved `<private_root>/t00-step3` path | `SCREEN_SOURCE_MISMATCH`, `SCREEN_RUN_ROOT_MISMATCH` | `test_A6`: the same authority presented with a copied private root | `_check_bindings` |
| A7 | P7 binding: the record bytes hash to `p7.record_sha256`; its `schema` is P7's and its `contract_sha256` is r3c's; `code_head` = HEAD; `bootstrap_sha256` = the compiled `P7_BOOTSTRAP_SHA256`; `code_closure_sha256` = SHA-256 of canonical `loaded_closure` (`p7_evidence.py:558-560`); `_current_bytes_check` passes (`:443-471`); the authority's `p7.*` fields equal the record's | `SCREEN_P7_MISMATCH` | `test_A7`: a record listing the true current file hashes under a different `bootstrap_sha256` | `_check_bindings` |
| A8 | #581 binding: `prereg.path` is the compiled chain's last entry; C is an ancestor of C′, and C′ is reachable from `origin/main`; `git diff C C′` changes only the §6 "Ratifying commit SHA" line, which reads C; at C the Status reads `RATIFIED <date>`, the §6 Ruling and OD-1/OD-2 fields are non-blank, the values block is present and equals `parameters`, and each active §3 *Ratified value* cell names only its block keys, and C is the oldest commit reachable from `origin/main` at which #581's Status reads `RATIFIED` | `SCREEN_PREREG_MISMATCH` | `test_A8`: C′ also edits one §3 cell | `_check_bindings` |
| A9 | A5/A6 text is frozen: the section hashes recomputed from the blob equal the compiled `A5_TEXT_SHA256` and `A6_TEXT_SHA256` | `SCREEN_PREREG_MISMATCH` | `test_A9`: one byte changed inside A6 | `_check_bindings` |
| A10 | A3 is answered: compiled successor paths; commits reachable from `origin/main`; in each blob, the first `\| ORB-3 ` (resp. `\| VAN-3 `) row, which is the §3 row, is the only line that successor's compiled answerer-exposure regex matches, and that successor's compiled OWED pattern does not match it | `SCREEN_A3_UNANSWERED` | `test_A10`: the §3a mapping row carries the exposure marker while the §3 row still reads `\| **OWED (operator)**` | `_check_bindings` |
| A11 | Parameters are supported: `scenarios = ["S0"]`; `run1_diagnostic = "WAIVED"`; `expressions = "DECLARED_BOOK"`; `horizon_sessions` = the compiled `A6_HORIZON_SESSIONS`; three distinct RNG roots and a distinct `probe_root`; `horizon % L == 0` and `L ≤` the smallest pool; the compiled `a5_rule` and `median_rule`; finite positive budgets with a non-empty basis | `SCREEN_PARAMETER_UNSUPPORTED` | `test_A11`: `scenarios = ["S0","S1"]` | `screen_authority` step 1 |

**K. Capability** (`production_source.py` and `screen_authority.py`; §3.3)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| K1 | The screen serves only a source-only source whose receipt **is** the authority's bound object, with equal SHA-256 values | `SCREEN_REQUIRES_SOURCE_RECEIPT`, `SCREEN_SOURCE_MISMATCH` | `test_K1`: same SHA-256, a different receipt object | `require_validated_screen_authority` |
| K2 | Both approval windows and the pin lifecycle are re-checked at every call, and a screen expiry is named as such | `SCREEN_APPROVAL_EXPIRED`, `SOURCE_APPROVAL_EXPIRED`, `SOURCE_KEY_*` | `test_K2`: the screen approval expires between two calls | `require_validated_screen_authority` |
| K3 | Only a screen-bootstrap process serves the screen: `_STATE.bootstrap_sha256 == SCREEN_BOOTSTRAP_SHA256`, as P7 checks its own (`p7_driver.py:91-92`) | `SCREEN_BOOTSTRAP_MISMATCH` | `test_K3`: a valid authority in a plain interpreter | `require_validated_screen_authority` |
| K4 | Only a ledgered run serves the screen: the process's write-once run binding names `<private_root>/t00-step3/<authority_sha256>/`, whose ledger opens with a durable AUTHORITY_BOUND for this authority and whose run lock is held by the process's parent | `SCREEN_RUN_UNBOUND` | `test_K4`: the right bootstrap, a run directory without AUTHORITY_BOUND | `require_validated_screen_authority`, `t00_screen.worker` |
| K5 | Every refusal fires before any engine is built | refusal order | `test_K5`: each K1–K4 and K6 refusal, with a spy on `_engine` that sees no call | `screen_bracket` |
| K6 | Integrity per epoch: a full `_verify_integrity` and a loaded-closure check open and close each worker epoch; every call runs the identity, lifecycle and path checks and a stat guard; all epochs record the same closure | `SCREEN_EPOCH_REQUIRED`; `SCREEN_EPOCH_STALE` (STOPPED); a failed full check at close, a loaded module whose bytes recorded at load differ from its blob at H, or a closure mismatch is `CODE_OR_ARTIFACT_DRIFT` (TERMINAL); a file that differs only on disk is STOPPED `TREE_CHANGED` | `test_K6`: an r3c artifact file's mtime changes mid-epoch | `screen_epoch`, `screen_bracket`, `state.check_record` |
| K7 | The fence is unchanged: `replay`, `replay_bracket`, `proof`, `_seal`, `_check_path`, `_verify_integrity` and `verify_for` keep their source text, still return sealed types and still refuse qualification | `SOURCE_ONLY_NOT_QUALIFICATION` | `test_K7`: with a valid authority, `verify_for` and `replay_bracket` on r3c; the seven functions' source hashes equal those recorded before the build | `production_source.py` |
| K8 | The wrapper's flags equal the sealed ones: per run, `deadline_failure` and `consumed_splits` equal `SourceOnlyReplay.deadline_failure` and `consumed_intrabar_splits` on the same path | equality | `test_K8`: a fake path with a deadline in R2 only | `screen_bracket`, `_consumed_splits` |
| K9 | No unreviewed static consumer: every call or attribute load of `screen_bracket`, `screen_epoch`, `_replay_raw` or `_engine` outside `production_source.py` has an allowlist entry keyed by (owner, capability) | A10b failure | `test_K9`: a planted `screen_bracket` call in `scripts/` under an owner allowlisted only for `replay_bracket` | `test_source_consumers.py` |
| K10 | P7 never imports the screen, and the screen never imports execution | `P7_FORBIDDEN_IMPORT`, `SCREEN_FORBIDDEN_IMPORT` | `test_K10`: the P7 bootstrap importing `c1_rail.qualification.t00_screen.plan` | `p7_evidence.py` forbidden lists |

**R. Plan and per-path rules** (`t00_screen.plan`; §5.2–§5.3)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| R1 | A seed is a function of (`t00-screen-rng/v1`, purpose, root, population, path index) only, and never equals `domain_seed` for the same indices | determinism | `test_R1`: seeds under W = 1 and W = 4; a collision scan against `domain_seed` | `plan.seed` |
| R2 | Candidates come once, from chronological `screen_bracket` runs in the candidate pass: the intersection of the R1 and R2 flat edges, stored as indices with a digest that every worker rebuilds and matches; the candidate worker's epoch closes (EPOCH_CLOSE, match) before `manifest.json` and PREPARED are written; the probe opens a new epoch in the same process | `CANDIDATES_UNAVAILABLE` (TERMINAL); a mismatch is `CORRUPTION` | `test_R2`: a block flat in R1 only | `plan.candidates` |
| R3 | A run is scored only if it has full length and no deadline flag, or the flag with a terminal failed prefix; every replayed session has a finite `intraday_low ≤ 0`; occurrence and source-session ids equal the path prefix | `CONTEXT_REFUSAL`, `INTRADAY_LOW_MISSING` (TERMINAL) | `test_R3`: a short run without the flag | `plan.shape_check` |

**S. Run state and durability** (`t00_screen.state`, `t00_screen.journal`, `t00_screen.coordinator`; §4)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| S1 | Run state is a pure fold of the ledger through `advance` (§4.2); an event not allowed in the current state is refused and nothing is written | `ILLEGAL_TRANSITION` | `test_S1`: SEGMENT_START from HALTED | `state.advance` |
| S2 | The coordinator is the only ledger writer; a worker writes only its own journal; no file is appended after its writer stops | `SCREEN_WRITE_REFUSED` (worker audit hook) | `test_S2`: a worker opens the ledger for append | worker bootstrap |
| S3 | Every file is hash-chained; only a torn final line is dropped; any other break is corruption | `CORRUPTION` (TERMINAL) | `test_S3`: a record removed mid-file | `journal.read` |
| S4 | Step-3 output exists from a durable AUTHORITY_BOUND, and #581 is consumed then: `run` refuses an authority whose `prereg.path` an AUTHORITY_BOUND under the run root already names | `PREREG_CONSUMED` | `test_S4`: a second authority (another L) after an interrupted first | `coordinator.run` |
| S5 | One open attempt at a time: `run` refuses while any run directory is past AUTHORITY_BOUND and not FINAL | `SCREEN_ATTEMPT_OPEN` | `test_S5`: an open attempt under another pre-registration path | `coordinator.run` |
| S6 | The run directory is created with O_EXCL under the run-root lock; one without a durable AUTHORITY_BOUND is reused only under that lock, and its AUTHORITY_BOUND records the reuse; one with it refuses `run` | `SCREEN_ALREADY_RUN` | `test_S6`: `run` twice | `coordinator.run` |
| S7 | `resume` re-runs the launch checks; a failure refuses with no state change | `RESUME_LAUNCH_CHECK` | `test_S7`: an untracked file at resume; the ledger bytes are unchanged | `coordinator.resume` |
| S8 | `resume` refuses while any lock is held, while an act file has no ledger record, and from HALTED without a CONTINUE act | `SCREEN_WORKERS_ALIVE`, `SCREEN_ACT_PENDING`, `SCREEN_HALTED` | `test_S8`: `resume` from HALTED | `coordinator.resume` |
| S9 | Stop classes are closed (§4.3): a non-deterministic cause reaches only STOPPED or HALTED; TERMINAL needs a deterministic A6 cause, evidence of corruption or nondeterminism, a key-lifecycle event, or a recorded act; an unlisted exception HALTs; any terminal-class stop makes the segment terminal | `UNCLASSIFIED_ERROR` (HALTED) | `test_S9`: an unlisted exception in a worker | `state.classify` |
| S10 | Losses are durable: a worker fsyncs KEY_START before replaying; a KEY_START with neither a result nor a WORKER_STOP naming it counts one loss, across segments, unless its segment ended INTERRUPTED; a third loss of one key, or a third consecutive I/O-error segment with no new completed key, HALTs | `RESOURCE_EXHAUSTED`, `IO_EXHAUSTED` (HALTED) | `test_S10`: three coordinator kills during one key, across restarts | `state.check_record` |
| S11 | SEGMENT_START is durable before any worker starts and is heartbeat 0; a segment without SEGMENT_END is charged its last heartbeat plus one interval | crash charge (row B5) | `test_S11`: a crash between SEGMENT_START and the first spawn | `coordinator` |
| S12 | Workers die with the coordinator: a Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, a non-inheritable handle, and workers created suspended, assigned, then resumed | crashed segment (STOPPED) | `test_S12`: kill the coordinator; no worker survives | `coordinator` |
| S13 | Determinism is checked: duplicate keys must project identically; a resume first recomputes min(W′, completed) tagged witness keys, and none when no key remains | `NONDETERMINISM` (TERMINAL) | `test_S13`: a divergent duplicate | `state.check_record` |
| S14 | Every record's key is in the plan and in its worker's assignment, or is a tagged witness | `CORRUPTION` (TERMINAL) | `test_S14`: a key outside the plan | `state.check_record` |
| S15 | `finalize` holds the run lock and runs only from COMPLETE or TERMINAL; after COMPLETE every key occurs exactly once | `FINALIZE_NOT_COMPLETE`; a gap after COMPLETE is `CORRUPTION` | `test_S15`: `finalize` from STOPPED; the ledger bytes are unchanged | `coordinator.finalize` |
| S16 | `results.json` is a pure function of (authority, r3c and P7-record digests, plan digest, sorted outcome multiset); W, segmentation and timing never change its bytes | byte equality | `test_S16`: W = 1, W = 4 and a three-segment run | `journal.results` |

**B. Budget** (`t00_screen.coordinator`; §5.4)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| B1 | Costs are ledgered apart: BUILD and INTEGRITY per worker epoch, path CPU and wall per path record, probe path CPU and wall, job CPU per heartbeat | record schema | `test_B1`: an epoch record without its INTEGRITY time | `journal` |
| B2 | The probe is timed once: after the authority and r3c checks, PROBE_START is durable; then one `probe_root` path runs in an already-built worker; an interrupted probe HALTs and is re-timed only after a CONTINUE act; it is never scored | `PROBE_INTERRUPTED` (HALTED) | `test_B2`: a crash between PROBE_START and PROBE | `coordinator` |
| B3 | Probe refusals are #581 A6's: a probe that ends in a deadline failure or cannot complete, or `probe path CPU × total paths > path_cpu_seconds`, is TERMINAL | `PROBE_INCOMPLETE`, `PROBE_OVER_BUDGET` | `test_B3`: a projection one second over budget | `coordinator` |
| B4 | The dispatch gate charges path CPU only, and no key is dispatched once it reaches `path_cpu_seconds`; a refusal with keys left is TERMINAL; a run whose gate never refused a key is scored, and its overrun recorded; the gate sums `cpu_s` over the first PATH record of each plan key only; witness and duplicate records are overhead (row B5) | `BUDGET_EXHAUSTED` | `test_B4`: a budget equal to the sum of every path but the last | `coordinator` |
| B5 | Overhead (builds, integrity checks, the candidate pass, the probe and the crash charge) is checked against `overhead_cpu_seconds` before each segment; exhaustion HALTs and is never TERMINAL by itself | `OVERHEAD_EXHAUSTED` (HALTED) | `test_B5`: repeated kills exhaust the reserve | `coordinator` |

**V. Verdict** (`t00_screen.verdict`, pure; §5.5)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| V1 | Tallies are never read while any insufficiency reason exists; an INSUFFICIENT report shows completed counts only | signature: reasons or tallies, never both | `test_V1`: reasons plus tallies that would give GO | `verdict` |
| V2 | #581 A5 (1)–(3) and A6 are implemented by reference, with exact integer comparisons; `UNDETERMINED` stays in every denominator; the pessimistic assignment decides GO and the optimistic one labels NO-GO | label equality | `test_V2`: a bust count of exactly 5% | `verdict` |
| V3 | Each compiled verdict constant (`A6_HORIZON_SESSIONS`, the 1/20 and 1/2 thresholds) occurs as a token in the A6 text that `A6_TEXT_SHA256` pins | token test | `test_V3`: one constant changed | `verdict` |
| V4 | No R2-P&L/R1-lows hybrid enters the verdict; the two A5 descriptive counts are reported per population and have no verdict role | label equality | `test_V4`: a hybrid row in the input | `verdict` |

**X. Exposure and acceptance** (`t00_screen.coordinator`, `screen_authority`; §4.5, §5.6)

| ID | Invariant | Enforced by | Test that violates only this row | Owner |
|---|---|---|---|---|
| X1 | Each subcommand prints only its fixed lines (§5.6), and stderr carries one refusal code only: no count, rate, key, progress or timing | exact output | `test_X1`: each subcommand on fakes; any extra output fails | `t00_screen.__main__` |
| X2 | Exposure is any read of the run directory or any console output beyond the fixed lines; every act lists every reader as `seen` or `not seen`; a renewal request carries only the expiry code | `SCREEN_ACT_FIELDS` | `test_X2`: an act with an empty `readers` list | `screen_authority.validate_screen_act` |
| X3 | Acts are Joshua's: canonical `t00_screen_act/v1`, signed under `APPROVE_T00_SCREEN_ACT`, binding the authority SHA-256 and the ledger head at signing; written with O_EXCL to `acts/` and fsync'd before its ledger record; an act whose ledger head is stale is refused; `validate_screen_act` takes the authority bytes, checks their SHA-256 against the run's AUTHORITY_BOUND, and checks only the act approval's own window and the key lifecycle, never the authority's or r3c's window; `act` and `resume` first append the ACT record of any unrecorded act file whose ledger head is current | `SCREEN_ACT_UNSIGNED`, `SCREEN_ACT_STALE` | `test_X3`: a valid act presented after a later record | `validate_screen_act`, `state.advance` |
| X4 | `verify` re-executes k hash-derived keys inside the same gate (rows K3, K4), under the run lock, and journals them; an expired approval gives `VERIFY_BLOCKED_APPROVAL_EXPIRED`, never VERIFIED | `VERIFY_BLOCKED_APPROVAL_EXPIRED` | `test_X4`: an expired screen approval | `coordinator.verify` |
| X5 | The label recompute imports nothing from `t00_screen.verdict` and is committed before Joshua signs | import scan | `test_X5`: the script imports the verdict module | `scripts/t00_screen_label_check.py` |
| X6 | P7 enters only as a precondition: the screen reads the record's binding fields, never its result fields; the acceptance evidence's SHA-256 is in the signing packet and the attestation | key-access scan | `test_X6`: a planted read of the record's `result` field in the screen package | `screen_authority`, `t00_screen` |

**G. Governance** (this design, #581 and the coordinator; checked by audit hooks and review)

| ID | Invariant | Enforced by | Check that violates only this row | Owner |
|---|---|---|---|---|
| G1 | Every cited code line is re-opened at the stated head before each revision | "Code read at" line | the audit hooks at the end | this design |
| G2 | The design restates only these #581 values: A6's 1,500-session horizon, A6's 5% and 50% thresholds (as `20·bust ≤ n` and `2·pass ≥ n`), and r3c-a2's expiry (#581 §5) | row V3 for the horizon and thresholds | `test_V3` | this design, `verdict` |
| G3 | Every act or choice of Joshua's is a §12 decision, including the change to A1's order (§12 item 5) and the OD-1 record (§8 step 9) | §12 | review | this design |
| G4 | No pre-ratification probe runs without its own dated answer, reads beyond P7's path windows, or reports more than wall and CPU time | §6 records | review of §6.1–§6.2 | coordinator |
| G5 | Every signing packet shows scope, schema and subject: the authority packet (§8 step 11) and the act packet (§4.5) | §4.5, §8 | review | coordinator |

---

## 3. Schema and validator

Canonical bytes are `contract.canonical_json_bytes` (`contract.py:266`), and they must round-trip through `parse_canonical_json` (`:289`). The authority SHA-256 is the SHA-256 of those bytes.

| Field | Content | Rows |
|---|---|---|
| `schema`, `authority_id`, `purpose`, `grants`, `refusals`, `evidence_class` | `"t00_screen_authority/v1"`; nonempty text; `"T00_STEP3_SELECTED_BOOK_SCREEN"`; `["T00_STEP3_SCREEN_ONCE"]`; `["QUALIFICATION_STAGES","PART_A","F1","DECISION_RULES","SEAL","ADMISSION","DEPLOYMENT","ARM","FALSIFIER_EVIDENCE","PARAMETER_CHANGE"]`; `"T00_STEP3_SCREEN"` | A1 |
| `source.contract_sha256` | the r3c digest; it binds r3c's 25 roles, so no role map is carried | A6 |
| `run_root_sha256` | SHA-256 of the resolved `<private_root>/t00-step3` path string, where `<private_root>` is the `artifact_root` the receipt was validated against | A6 |
| `p7.record_sha256`, `p7.code_head`, `p7.code_closure_sha256`, `p7.bootstrap_sha256`, `p7.interpreter` | the accepted P7 record's values | A7 |
| `prereg.path`, `prereg.ratifying_commit` (C), `prereg.commit` (C′), `prereg.blob_sha256`, `prereg.a5_text_sha256`, `prereg.a6_text_sha256` | #581's path, its commits, the C′ blob digest, and the section hashes (exact bytes between the A5/A6 headings and the next heading) | A4, A8, A9 |
| `a3_answers` | `[{path, commit, blob_sha256}]` for the two 2026-10-02 successors | A4, A10 |
| `parameters` | the closed set below; byte-equal to the canonical values block `t00-step2-values/v1` in the ratified #581 §6 | A8, A11 |
| `source_trust` | `_source_trust_document(SOURCE_SIGNING_KEYS)` (`contract.py:1037-1041`) | A2 |

**`parameters`** is a closed set. Each key maps to a #581 item, and each active §3 *Ratified value* cell names only its keys (row A8), so the values exist once.

| Key | #581 item | Rule (row A11 unless stated) |
|---|---|---|
| `expressions` | A1, OD-2 | `"DECLARED_BOOK"` only. The editions would need another source contract and P7 |
| `scenarios` | 7 | `["S0"]` only. r3c carries PRISTINE only (`contract.py:1156-1159`); S1 needs a new source contract |
| `initial_state` | §2 A3 | equals `receipt.initial_state` |
| `horizon_sessions` | A6 | equals the compiled `A6_HORIZON_SESSIONS` (row V3) |
| `rng` | 4, A6 | `{tag:"t00-screen-rng/v1", roots:[3 distinct strings], probe_root}`; Joshua sets the roots (item 4) and `probe_root` (A6's probe "in its own RNG domain"); `probe_root` differs from every root |
| `depth_per_root` | 1 | `{FULL,H1,H2}` → positive integers. The three roots pool per population, so N = 3 × `depth_per_root` |
| `block` | 4 | `{family:"JOINT_FLAT_BOTH_RUNS", length_sessions:L}`; `horizon % L == 0` (`paths.py:48-49`) and `L ≤` the smallest pool |
| `path_start_date` | 4 | equals `receipt.path_start_date` |
| `pass_floor_halves` | 2 | `"BINDING"` or `"REPORTED"` |
| `deadline_only_is_bust` | 3 | bool |
| `run1_diagnostic` | 5 | `"WAIVED"` only. The runner fixes `consistency=.40` (`runner.py:27`) |
| `a5_rule` | 8 | `"T00_A5/v1"`, or a successor ID compiled in the verdict module |
| `median_rule` | A2/A5 reading | `"LOWER_NEAREST_RANK_INF_INCLUDED"` |
| `budget` | 1 | `{path_cpu_seconds, overhead_cpu_seconds, basis}`: finite and positive; `basis` is non-empty text recording the §5.4 formula inputs (rows B4, B5) |

**Excluded** (row A1): the F1 fields (`replay`, `result_plan`, `approval_policy`, `coverage`, `clocks`, `trust_domain_sha256`, `policy_sha256`); the r3c-only fields (`artifacts`, `historical_pins`, `port_runtime_pins`, `populations`); the r3c approval digest (C2); a role map; a seed-pooling field; shard and worker counts (C7); and any expiry, which lives only in the approval payload (`contract.py:382-385`), so the authority SHA-256 is stable when Joshua renews.

### 3.1 Approval

A detached Ed25519 approval verified by `verify_detached_approval` (`contract.py:366-435`): scope `APPROVE_T00_SCREEN_AUTHORITY`, `subject_sha256 = contract_sha256 =` the authority SHA-256, `authority_class = OPERATOR`, `allow_test_authority=False`, signed by the pinned `source:1ebae5d45bc51280` (§12 item 2). The trust checks follow `contract.py:1168-1195` (row A2). Scope exclusivity is in the signed bytes (`contract.py:389`; row A3). `source:` key IDs stay refused in qualification domains (`contract.py:1001-1005`; `trust_domain.py:318-319`), and the authority never enters a `QualificationTrustDomain`.

### 3.2 Validator and receipt

New module `ops/c1_rail/qualification/screen_authority.py`. It **imports** the existing `contract.py` helpers (`_fields`, `_text`, `_receipt_snapshot`, `_pinned_source_keys`, `_source_trust_document`, `_check_source_key_lifecycle`, `verify_detached_approval`, `require_validated_source_contract`, `canonical_json_bytes`) and edits none of them.

`validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root, now)` takes no HEAD, tree, interpreter or reader argument (row A5). It reads them from a fixed repository root, the checkout that holds the module (`Path(__file__).resolve().parents[3]`); tests monkeypatch only that constant. `artifact_root` stays an argument because `_current_bytes_check` re-hashes every artifact under it (`p7_evidence.py:446-450`). `now` stays an argument, as in every existing validator; every use re-checks with `_now()` (row K2).

Order, so that unsigned input never reaches `git`:
1. The bytes alone: rows A1, A4 and A11.
2. The signature: rows A2 and A3.
3. `_check_bindings`, with the authority, receipt, P7 record, the reality it reads and every blob in hand: rows A5–A10.
4. Issue a frozen `ValidatedScreenAuthority` (authority SHA-256, approval, key SHA-256, a reference to the exact `source_receipt`, read-only `parameters`, the P7 and pre-registration bindings, `evidence_class`), registered with a weakref and a snapshot as at `contract.py:1211-1215`.

`require_validated_screen_authority(auth, *, source_contract, now)` runs on every use and enforces rows K1–K4. It wraps `_check_source_key_lifecycle` (`contract.py:1044-1062`) and re-codes its `SOURCE_APPROVAL_EXPIRED` as `SCREEN_APPROVAL_EXPIRED` for the screen approval; the key codes stay, because one key signs both approvals.

`validate_screen_act(act_bytes, approval_bytes, public_keys, *, authority, ledger_head, now)` enforces rows X2 and X3 (§4.5).

**P7 acceptance evidence** (row X6). `AcceptedP7Record` exists only in memory (`p7_evidence.py:435-440`, `:507-508`), and `fp.ps1 python` writes a `.cache/fp-verification` record only for pytest and `check` (`scripts/fp.py:241-254`). So `t00_screen accept-p7` runs `accept_p7_record` and writes `p7_acceptance.json` (record SHA-256, `accepted_at`, HEAD, exit status) to the private root. The signing packet and the attestation carry its SHA-256. The validator cannot re-establish it without a second P7 run (C3); §13 names the residual.

### 3.3 The capability: `screen_epoch` and `screen_bracket`

```python
@dataclass(frozen=True)
class ScreenBracket:                         # screen_authority.py; model.py untouched
    bracket: BracketReplayResult             # r1, r2 (model.py:224-235)
    deadline_failure: tuple[bool, bool]      # per run, as replay_bracket's `failed` (production_source.py:1229-1233)
    consumed_splits: tuple[tuple, tuple]     # per run, the placements _seal derives (:913-915)

def screen_epoch(self, *, authority):        # once per worker start: about 71 s (§6.2)
    if not _is_source_only(self.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT')
    from .screen_authority import open_screen_epoch, require_validated_screen_authority   # lazy: P7 never loads it
    require_validated_screen_authority(authority, source_contract=self.contract, now=_now())
    self._verify_integrity()                 # unchanged: snapshot (:1172-1173), retained-bytes re-hash (:1179)
    return open_screen_epoch(self, authority)   # records the stat-guard set

def screen_bracket(self, path, *, authority, epoch):
    if not _is_source_only(self.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT')
    from .screen_authority import ScreenBracket, require_open_screen_epoch, require_validated_screen_authority
    require_validated_screen_authority(authority, source_contract=self.contract, now=_now())
    require_open_screen_epoch(epoch, source=self, authority=authority)   # issued for (self, authority); stat guard
    self._verify_identity()                  # new: the O(1) checks of _verify_integrity (:1169-1171, :1174-1178)
                                             # and the r3c lifecycle (:1180-1182)
    by_id = {s.session_id: s for s in self.sessions}                     # path membership, as _check_path (:1195-1197)
    if not path or any(by_id.get(s.source.session_id) != s.source for s in path):
        raise ValueError('path contains a source session outside retained covered panel')
    from .replay import ReplayDeadlineFailure
    bracket, results, failed, splits = ScheduleExecutionBracket(self._quotes), [], [], []
    for run_id in BRACKET_RUNS:              # replay_bracket's loop (:1224-1234), unsealed; replay_bracket untouched
        provider = bracket.for_run(run_id)
        try:
            result, flag = self._engine(provider).run(path), False
        except ReplayDeadlineFailure as exc:
            result, flag = exc.result, True
        results.append(result); failed.append(flag); splits.append(_consumed_splits(provider))
    return ScreenBracket(BracketReplayResult(*results), tuple(failed), tuple(splits))
```

- **Own loop, sealed path untouched** (rows K7, K8). `screen_bracket` copies `replay_bracket`'s loop instead of refactoring it, and `_consumed_splits(provider)` copies `_seal`'s placement expression instead of moving it. `replay_bracket` and `_seal` (and so `replay`, which calls `_seal` with `provider=None`, `:1213`) keep their source text. `test_K8` holds the copies to the originals.
- **Why a wrapper.** A bare `BracketReplayResult` holds only the two `ReplayResult`s (`model.py:176-184`, `:224-235`). Without the flags, a short series could not be told apart from a confirmed deadline failure (A6, row R3), and #581 A5's consumed-split count could not be computed.
- **Integrity per epoch** (row K6). `_verify_integrity` costs about 71.4 s per call (§6.2), almost all in the two O(source-size) checks: the execution-state snapshot (`:1172-1173`, a full traversal, `:927-934`) and the retained-bytes re-hash (`:1179`). Both read memory, not disk: a built source replays from its retained bytes (`:1246`), and a module is loaded once per process. So:
  - each worker epoch opens with `screen_epoch` (one full check) and closes with `close_screen_epoch`, which runs the full check again and compares every loaded module's file with the bytes recorded at load (as `p7_evidence.py:526-528`) and every first-party module with its blob at H;
  - every `screen_bracket` call runs the O(1) identity checks, both lifecycles, the path check and a **stat guard**: (size, `mtime_ns`, file id) of every r3c artifact file, every tracked first-party file and the interpreter and lock files, against the values recorded at epoch open;
  - a stat-guard change stops the worker before KEY_START (`SCREEN_EPOCH_STALE`, STOPPED); the worker still closes its epoch. A failed close is TERMINAL `CODE_OR_ARTIFACT_DRIFT`, because then a drifted byte may have run. A change that nothing loaded leaves the segment STOPPED, and `resume` refuses until the tree is restored (row S7).
  - **Residual.** An in-process mutation of the source between open and close is caught only at close; the run then ends TERMINAL, so no such path is scored. A file rewritten with its size, mtime and file id restored evades the stat guard; the close catches it if the worker loaded it, and the next worker start's clean-tree check catches it otherwise. A worker killed before its close leaves records that no closing check covered; they rest on the opening check, the per-call checks, the resume witnesses (row S13) and `verify`'s re-execution (row X4).
- **Ordering.** Every refusal fires before `_engine` is called (row K5). A path started inside an approval window completes; the next call refuses (row K2).

---

## 4. Run state model

### 4.1 Persistence (private root only; absolute path outside any worktree)

The run directory is `<private_root>/t00-step3/<authority_sha256>/`; the authority binds the run root (row A6).

| Path | Writer and discipline | Content |
|---|---|---|
| `lock` | the coordinator, for its whole invocation (`msvcrt.locking`) | pid, host |
| `ledger/NNNN.jsonl` | one file per coordinator invocation, numbered 1 + the highest existing number (empty and torn files count); append + fsync; hash-chained, its first record chained to the previous file's last valid record; the coordinator only (row S2) | the events of §4.2 |
| `journal/sK-wI.jsonl` | one file per worker per segment; that worker only; append + fsync; hash-chained; nothing after WORKER_STOP | EPOCH_OPEN{BUILD and INTEGRITY cpu/wall, closure SHA-256, guard-set SHA-256}; KEY_START{key}; PATH{key, seed, `path_sha256`, `wall_s`, `cpu_s`, and per run: status, `sessions_to_pass`, failure reason, `kernel_outcome`, sessions replayed, `deadline_failure`, consumed-split count and SHA-256 (as `p7_driver.py:62-65`), `events_sha256`, run digest (the `p7_driver.py:55-59` projection)}; the candidate worker's CANDIDATES and PROBE_RESULT; EPOCH_CLOSE{INTEGRITY cpu/wall, closure match}; WORKER_STOP{reason, key?} last. No P&L series |
| `journal/vN-wI.jsonl` | `verify` workers, same discipline | re-executed PATH records |
| `acts/<act_sha256>.json` | O_EXCL, fsync'd before its ACT record (row X3) | the signed act and its approval |
| `manifest.json` | temp file → fsync → `os.replace`, once, before PREPARED | the authority, r3c, P7-record and code-head digests; per population, candidate block-start indices and `candidates_sha256`; the plan digest |
| `results.json` | canonical JSON, atomic replace | row S16: A5 tallies under both assignments, the two A5 descriptive counts per population, the A6 verdict, labels; **no timestamps, W, approvals or timings** |
| `REPORT.md` | rendered from `results.json` only, by a fixed template | cites the SHA-256 of `results.json` |
| `attestation.json` | atomic | the SHA-256s of results, report, ledger head and every journal head; every r3c and screen approval used; acts; segments; epoch closures; the `p7_acceptance.json` SHA-256 |
| `errors/` | the coordinator | tracebacks of unclassified errors; reading one is exposure (row X2) |

### 4.2 Events and the one transition function (row S1)

`advance(state, event)` is the only code that changes durable run state; the coordinator appends the event only after `advance` accepts it. The state is the fold of the ledger. RESUMABLE means BOUND, PREPARED or IDLE with no lock held.

| From | Event (ledger record) | To |
|---|---|---|
| none | AUTHORITY_BOUND{authority SHA-256, `prereg.path`, approvals} | BOUND |
| BOUND | PREPARED{manifest SHA-256, BUILD, INTEGRITY} | PREPARED |
| Any state except RUNNING and FINAL | TERMINAL{code}, code in the TERMINAL class by `classify` (§4.3), including a `check_record` failure found at `resume` or at `finalize` (`finalize` appends it before AGGREGATED, so V1 receives the reason) | TERMINAL |
| PREPARED | PROBE_START | PROBING |
| PROBING | PROBE{path CPU, path wall, peak memory} | IDLE |
| BOUND, PREPARED, PROBING, IDLE | HALT{code, from}, code in the HALTED class by `classify` (§4.3) | HALTED |
| IDLE | SEGMENT_START{k, W, assignment SHA-256, witness keys, approvals}, heartbeat 0 | RUNNING |
| IDLE, no key left | ALL_DONE | COMPLETE |
| RUNNING | HEARTBEAT{wall, job CPU} every 60 s | RUNNING |
| RUNNING | SEGMENT_END{class, cause, workers[{worker, reason}], wall, job CPU, path CPU, overhead CPU, peak memory} | IDLE (STOPPED), HALTED, COMPLETE or TERMINAL, by the highest class (§4.3) |
| RUNNING, found unlocked at resume | SEGMENT_CRASHED{k, charge, losses} | IDLE, or HALTED if a cap is reached (row S10) |
| BOUND, PREPARED, IDLE, HALTED | ACT{TERMINATE} | TERMINAL{`OPERATOR_TERMINATED`} |
| HALTED | ACT{CONTINUE} | the HALT's from state; PROBING resumes as PREPARED |
| COMPLETE, TERMINAL | AGGREGATED → REPORTED → FINAL | FINAL |
| FINAL | VERIFY_START, VERIFY{keys, match} | FINAL |

A lapse inside BOUND or PREPARED writes nothing. Any other non-terminal stop there appends HALT{code, from} (at `resume` if the coordinator died); the candidate pass repeats only after CONTINUE. There is no `CANDIDATES` loss key.

### 4.3 Stop classes (closed; row S9)

Precedence when several workers stop differently: TERMINAL > HALTED > STOPPED > COMPLETE.

| Cause | Detected | Class and code |
|---|---|---|
| r3c or screen approval expired, before KEY_START or at a call | lifecycle check (row K2) | STOPPED `APPROVAL_LAPSE`; a renewal over the same bytes resumes; only a TERMINATE act ends it |
| `SOURCE_KEY_REVOKED`, `SOURCE_KEY_CHANGED` or `SOURCE_KEY_REMOVED` (`contract.py:1055-1062`) | lifecycle check | TERMINAL `SOURCE_KEY_LIFECYCLE`; no renewal exists without a new pinned root, which means a new H |
| `ReplayNeedsContext`, a shape failure, a missing or invalid `intraday_low` | worker (row R3) | TERMINAL `CONTEXT_REFUSAL` or `INTRADAY_LOW_MISSING` |
| Empty population or candidate set, a chronological deadline failure, discontinuous edges | candidate pass (row R2) | TERMINAL `CANDIDATES_UNAVAILABLE` |
| Probe failure, or a projection over budget | probe (row B3) | TERMINAL `PROBE_INCOMPLETE` or `PROBE_OVER_BUDGET` |
| Path budget reached with keys left | dispatch gate (row B4) | TERMINAL `BUDGET_EXHAUSTED` |
| Divergent duplicate or witness mismatch | `check_record` (row S13) | TERMINAL `NONDETERMINISM` |
| Chain break, key outside the plan or assignment, candidate mismatch, a gap after COMPLETE | `check_record` (rows S3, S14, S15, R2) | TERMINAL `CORRUPTION` |
| Failed epoch close, or closures that differ across epochs | worker, `check_record` (row K6) | TERMINAL `CODE_OR_ARTIFACT_DRIFT` |
| Stat guard changed | worker (row K6) | STOPPED `TREE_CHANGED` |
| Head, tree, interpreter, artifact or P7 drift at `resume` | launch checks (row S7) | `resume` refused; no state change |
| `OSError` on a journal or ledger write | worker or coordinator | STOPPED `IO_ERROR`; the third consecutive one with no new completed key is HALTED `IO_EXHAUSTED` (row S10). A coordinator write error closes the job and exits, so the segment is crashed |
| `MemoryError`, or a worker exit without WORKER_STOP | coordinator | STOPPED `WORKER_LOST`; each in-flight KEY_START is a loss; a third loss of one key is HALTED `RESOURCE_EXHAUSTED` (row S10) |
| Coordinator crash or kill | `resume` (SEGMENT_CRASHED) | STOPPED, with the same loss rule |
| Ctrl-C | under `fp.ps1` the launcher kills the coordinator about 0.25 s after the interrupt (`scripts/fp.py:274`, `:330`) | as a coordinator kill; run directly, the coordinator writes SEGMENT_END `INTERRUPTED`, whose in-flight keys are not losses |
| Overhead reserve reached | before a segment (row B5) | HALTED `OVERHEAD_EXHAUSTED` |
| PROBE_START without PROBE | coordinator or `resume` (row B2) | HALTED `PROBE_INTERRUPTED` |
| Anything else | worker or coordinator | HALTED `UNCLASSIFIED_ERROR` |

A misattributed code changes the reason text only, never the class. No failure can resume indefinitely: every repeatable cause is capped, and a HALT needs Joshua's act.

### 4.4 Crash windows

Revision 2's window numbers are kept for traceability.

| # | Window or event | Outcome | Rows |
|---|---|---|---|
| W0 | Crash in BOUND, before the manifest is durable | Step-3 output exists (row S4). HALTED; after CONTINUE, `resume` repeats the candidate pass | S1, X3 |
| W1 | Crash in PREPARED, before PROBE_START | Resume times the probe | S1 |
| W2 | Worker lost mid-path | STOPPED `WORKER_LOST`; the key is a loss and is recomputed identically | S10 |
| W3 | Torn final line | That line is dropped; the key is recomputed | S3 |
| W4 | Duplicate key after a resume | Identical: deduplicated. Divergent: `NONDETERMINISM` | S13 |
| W5 | Resume witness mismatch | `NONDETERMINISM` | S13 |
| W6 | Crash during aggregation, report or attestation | Re-run `finalize`; outputs are byte-identical | S15, S16 |
| W7 | Crash after REPORTED, before FINAL | `finalize` re-verifies the digests and appends FINAL | S15 |
| W8 | Approval lapse | STOPPED `APPROVAL_LAPSE` | K2, X3 |
| W9 | Path budget reached with keys left | TERMINAL `BUDGET_EXHAUSTED` | B4 |
| W10 | Context refusal, shape failure or key-lifecycle event | TERMINAL | R3, K2 |
| W11 | Drift found at `resume` | `resume` refused; no state change | S7 |
| W12 | Drift during a segment | STOPPED `TREE_CHANGED`, or TERMINAL `CODE_OR_ARTIFACT_DRIFT` if a drifted byte may have run | K6 |
| W13 | Disk full, or an antivirus lock | STOPPED `IO_ERROR`, capped | S10 |
| W14 | A second coordinator, or `resume` while any lock is held | Refused; the running segment is unaffected | S8 |
| W15 | Ctrl-C | Under `fp.ps1`, W22 | S12 |
| W16 | TERMINATE act | TERMINAL `OPERATOR_TERMINATED`; never GO | X3 |
| W17 | A key outside the plan or assignment, not a tagged witness | `CORRUPTION` | S14 |
| W18 | Machine sleep | No effect on the CPU budgets; wall is recorded, not gated. Disable sleep for the run | B4 |
| W19 | Probe refused | TERMINAL `PROBE_*` | B3 |
| W20 | Candidates unavailable | TERMINAL `CANDIDATES_UNAVAILABLE` | R2 |
| W21 | PROBE_START without PROBE | HALTED `PROBE_INTERRUPTED`; it takes precedence over a lapse, which the pre-probe checks catch first | B2 |
| W22 | Coordinator killed hard | The Job Object kills every worker; at resume SEGMENT_CRASHED charges the last heartbeat plus one interval; in-flight keys are losses | S10, S11, S12 |
| W23 | Overhead reserve reached | HALTED `OVERHEAD_EXHAUSTED` | B5 |

### 4.5 Acts, the freeze point and re-attempts (§12 item 8)

- **Freeze point** (row S4). Step-3 output exists from the first durable AUTHORITY_BOUND: the candidate pass reads chronological deadline flags, and the probe reads a deadline result. From then on #581 is consumed for step 3. `run` refuses any authority under the same `prereg.path` (`PREREG_CONSUMED`), and refuses while any attempt is open (`SCREEN_ATTEMPT_OPEN`, row S5).
- **Re-attempts.** After any AUTHORITY_BOUND, whatever the outcome, a further attempt needs a successor pre-registration that carries an exposure statement for every reader of the earlier run directory. It is accepted only by a code change that appends its path to the compiled pre-registration chain (row A8), which means a new H and A1 step 5 again. The earlier run directory is kept. This follows the ORB and Vanguard precedent, whose originals were closed for replay-output exposure and replaced by successors.
- **Acts** (rows X2, X3). Only Joshua signs them, under the pinned key and scope `APPROVE_T00_SCREEN_ACT`. An act is canonical `t00_screen_act/v1` `{authority_sha256, act: TERMINATE | CONTINUE, ledger_head_sha256, statement, readers: [{name, exposure: seen | not seen}]}`:
  - `TERMINATE` ends the run from BOUND, PREPARED, IDLE or HALTED as TERMINAL `OPERATOR_TERMINATED`. It is how Joshua declines a renewal after a lapse, or declines to continue after a HALT;
  - `CONTINUE` lets a HALTED run resume once and resets the cap that halted it;
  - agents never sign or request acts beyond relaying the stop code.
- **Act packet** (row G5): the act bytes, their SHA-256, the scope, the schema, the subject (the act SHA-256), the authority SHA-256, the ledger head it binds and the stop code being answered. No count, key or timing is in it.
- **Renewal** is not an act: Joshua signs a fresh approval over the same bytes. The request carries only the expiry code (row X2).

---

## 5. Driver

### 5.1 Process topology (local machine only; private data never leaves it)

**Coordinator.** `fp.ps1 python -m c1_rail.qualification.t00_screen {preflight|accept-p7|run|resume|finalize|verify|act} <args>`. It holds the run lock, is the only ledger writer (row S2), dispatches keys through the budget gate (row B4) and writes heartbeats.

**Workers.**
- Each worker is `sys.executable -I -S -B -c SCREEN_BOOTSTRAP`, generated from the shared bootstrap template (C8), with an audit hook and recording finder as P7 has (`p7_evidence.py:57-339`). The audit hook also refuses write-opens outside the worker's own journal (row S2).
- The environment is pinned: `PYTHONHASHSEED=0`, and `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` all `=1`.
- Workers run in a Windows Job Object created through `ctypes` (row S12). The job's accounted CPU includes exited workers (row B1).
- A worker receives the run directory and authority SHA-256 on its command line, checks its bootstrap hash and binds the run once (rows K3, K4), validates r3c and the authority, builds its own `ProductionSource` (`contract.py:1211-1215`; `production_source.py:1159-1164`), and opens its epoch (row K6). Workers pickle nothing.
- W is a launch value, chosen after the probe: W = min(8, ⌊0.8 × RAM / probe peak working set⌋). A lost worker ends the segment; the coordinator may start the next segment itself after a `WORKER_LOST` or `IO_ERROR` stop, under the same launch checks as `resume` and the caps of row S10.

**Forbidden modules** (exact name or package prefix, `p7_evidence.py:51-52`, `:241`; row K10):
- The screen forbids `production`, `orchestration`, `result_adjudication`, `seal`, `execution`, `part_a`, `benchmark`, `benchmark_part_a` and `p7_driver` under `c1_rail.qualification`, and stubs `runner._run_stage` and `runner.run_synthetic_stage`. `evaluate_replay`, `simulate_path` and `bracket` load live.
- P7's list gains `c1_rail.qualification.screen_authority` and `c1_rail.qualification.t00_screen`. The screen driver is a package, so the prefix rule covers every module in it.

### 5.2 Candidate pass and probe (PREPARED, then PROBING)

One worker, the candidate worker, runs both:
1. For each population pool, in `partition_populations` order (`blocks.py:35-38`): assemble the chronological path as `proof` does (`production_source.py:1268`), run `screen_bracket`, derive each run's edges as `proof` does (`:1282-1291`) and the joins from `self.adjacent`, and compute `JointFlatBlocks(pool, edges_r, L, joins).candidates()` (`blocks.py:28-32`) for R1 and R2. The candidates are the intersection (row R2), mirroring `provider.py:36-54`.
2. The coordinator writes `manifest.json` and PREPARED.
3. The coordinator checks the authority and r3c lifecycles, writes PROBE_START, and has the same worker time one path: `probe_root`, population FULL, index 0. The worker reports path CPU, path wall and peak memory; the coordinator writes PROBE (rows B2, B3).

`proof` is not used: its single-run provider refuses unreviewed instants (§1), and on r3c its sealed output holds edges of a single run only.

### 5.3 Per path

```
coordinator: key = next key of worker i, if budget.gate() allows                 # row B4
worker:      check both lifecycles (row K2); stat guard (row K6); fsync KEY_START{key}   # row S10
             seed = int.from_bytes(sha256(canonical(["t00-screen-rng/v1", purpose, root, population, path_index]))[:8], "big")
             path = PathAssembler(path_start_date).sample(candidates[population], Random(seed), horizon_sessions=H)   # paths.py:44-51
             s = source.screen_bracket(path, authority=auth, epoch=epoch)
             for run, failed in zip((s.bracket.r1, s.bracket.r2), s.deadline_failure):
                 shape_check(run, failed, path); outcome = evaluate_replay(run, initial_state=initial)   # row R3; runner.py:20-44
             fsync PATH{key, seed, path_sha256, outcomes, s.consumed_splits, status, wall_s, cpu_s}   # status: bracket.py:95-112
             report (key, cpu_s) to the coordinator
```

- **Seeds** (row R1) are separate from the qualification streams (`'tb-s2-rng-v2'`, `regime.py:22`) and do not use `regime.domain_seed`, whose stage set is qualification-only (`regime.py:12`). They depend on neither the authority digest nor W.
- **`shape_check`** (row R3) mirrors `provider.py:76-83` and #581 A6 with the run's own `deadline_failure` flag. Each run satisfies one of: `failed` is false and the run has length H; or `failed` is true with `0 < len ≤ H`, the last row not flat-before-deadline and every earlier row flat. Both also need one finite `intraday_low ≤ 0` per replayed session and `occurrence` and `source_session_id` equal to the path prefix.
- **`initial`** is the `EvaluationState` built from `receipt.initial_state`, as `production_source.py:1259-1261` builds it.

### 5.4 Budget (rows B1–B5; §12 item 7)

Both budgets are CPU seconds, which do not depend on W or on host contention. Wall time is recorded, not gated; the approval windows bound elapsed time.

```
path_cpu_seconds      ≥ c × 3N                       gated per key (row B4)
overhead_cpu_seconds  ≥ (b + 2i) × (W × S + R) + p     checked before each segment (row B5)
```

- c is the per-path CPU with the integrity hoisted: about 136 s, or 320 s at the slope's upper bound (§6.3). The in-run probe re-measures it (row B3).
- b is the build (about 173 s) and i the integrity check (about 71.4 s); each worker epoch costs b + 2i.
- W is the worker count, S the expected segments and R the spare worker starts.
- p is the candidate pass plus the probe: one epoch, the three chronological brackets (1,994 path-sessions, about 185 s or 430 s upper) and one probe path.
- Example: W = 8, S = 3, R = 8 and p ≈ 1,100 s give about 11,200 s, roughly 3.1 CPU-hours.
- **Crash charge.** A segment without SEGMENT_END is charged its last heartbeat (SEGMENT_START counts as heartbeat 0) plus one interval of wall, and that heartbeat's job CPU plus one interval × W, all as overhead. A crash can only overcharge.
- **Final-path overrun.** A run is scored if the gate never refused a key, and the overrun is recorded. #581 A6 makes a budget stop INSUFFICIENT "before every population reaches its frozen depth", and this reading follows that text. It knowingly differs from `runner.py:120-122`; strict parity is the alternative in §12 item 7.

### 5.5 Finalize and verdict (rows S15, S16, V1–V4)

`finalize` takes the run lock, folds the ledger, runs `check_record`, then aggregates through the pure verdict module. `t00_screen.verdict` implements #581 A5 (1)–(3) and A6 **by reference to those sections**. It takes outcome rows, `parameters` and the insufficiency reasons, and returns `INSUFFICIENT(reasons)`, `GO-evidence` or `NO-GO-evidence{robust | UNDETERMINED-dependent}`. With the verdict, `results.json` carries per population the count of paths with a consumed split in either run and the count of `UNDETERMINED` paths, descriptively.

**Mapping of the #581 A6 triggers to screen codes.** The A6 text is left verbatim.

| #581 A6 trigger | Screen code and row |
|---|---|
| `ReplayNeedsContext`, a source refusal, or a short series without a confirmed deadline failure | `CONTEXT_REFUSAL` (R3); `SOURCE_KEY_LIFECYCLE` (K2) |
| A run lacks its own synchronized `intraday_low` | `INTRADAY_LOW_MISSING` (R3) |
| P7 is not accepted for A1's identities at the executing head | the authority does not validate (A5, A7); `CODE_OR_ARTIFACT_DRIFT` mid-run (K6) |
| The runner raises `NeedsContext` (budget, a missing prerequisite, or a probe that cannot complete) before full depth | `BUDGET_EXHAUSTED` (B4); `PROBE_INCOMPLETE`, `PROBE_OVER_BUDGET` (B3); `CANDIDATES_UNAVAILABLE` (R2); `OPERATOR_TERMINATED` after an unrenewed lapse or a HALT (X3) |
| Any §3 item is unset | the authority does not validate (A8, A11) |
| A confirmed own-flat deadline failure on a scored path | a scored outcome, never INSUFFICIENT (R3) |
| "No reduced depth, substitute clock or extra draw is run in its place" | `PREREG_CONSUMED` (S4) |

### 5.6 Console, access and acceptance (rows X1–X6; §12 item 11)

**Console** (row X1). stderr carries one refusal code on refusal and nothing else; an unexpected exception prints `UNCLASSIFIED_ERROR` and writes its traceback to `errors/`.

| Subcommand | stdout, exactly |
|---|---|
| `preflight` | `T00_SCREEN_PREFLIGHT OK authority_sha256=<hex>` |
| `accept-p7` | `T00_SCREEN_P7_ACCEPTED acceptance_sha256=<hex>` |
| `run`, `resume` | the launch line `T00_SCREEN_RUN authority_sha256=<hex>`, then one stop line: `T00_SCREEN_STOPPED <code>`, `T00_SCREEN_HALTED <code>`, `T00_SCREEN_TERMINAL <code>` or `T00_SCREEN_COMPLETE` |
| `finalize` | `T00_SCREEN_VERDICT <GO-evidence\|NO-GO-evidence-robust\|NO-GO-evidence-UNDETERMINED-dependent\|INSUFFICIENT> results_sha256=<hex>` |
| `verify` | `T00_SCREEN_VERIFY <VERIFIED\|REFUTED\|VERIFY_BLOCKED_APPROVAL_EXPIRED>` |
| `act` | `T00_SCREEN_ACT_RECORDED <TERMINATE\|CONTINUE> act_sha256=<hex>` |

**Exposure** (row X2) is any read of the run directory (journals, ledger, heartbeats, SEGMENT_START witness keys, PROBE, `errors/`) or any console output beyond these lines. No count, rate, key, progress or timing appears on a console, in CI or in a PR. Rows are read only by `finalize` and `verify`, and by the coordinator after the verdict line prints.

**`verify`** (the coordinator seat; rows X4, X5):
1. Re-validate offline the authority, the approvals and r3c.
2. Check the verdict line's digest against `sha256(results.json)`, the hash chains, `check_record` and coverage.
3. Recompute the label with `scripts/t00_screen_label_check.py`, which does not import `t00_screen.verdict`, from the ratified #581 A5/A6 text. It is committed and reviewed before Joshua signs (§8 step 10).
4. Re-execute k = 9 keys (one per root × population), chosen from `sha256(results.json)`, inside the gate of rows K3–K4, and compare their rows byte for byte.

The result is VERIFIED or REFUTED. Under an expired approval it is `VERIFY_BLOCKED_APPROVAL_EXPIRED`, which is neither, and the label stays unaccepted until Joshua renews.

**Public reporting.** Only the label is public. A public figure may only cite the private RESULTS path (`load_bearing_numbers.md` §1).

---

## 6. Timing probes and cost model

### 6.1 Probe 1: ruling A4

The A4 probe was a timed P7 re-run. The coordinator re-ran P7 at `origin/main@d716106` under r3c / r3c-a2 on 2026-10-03 (UTC), with timing. The record (SHA-256 `6718b665900ee0d43a80544913cd5a2f35d533d059c9e5e20ea35329b5a4565d`) was ACCEPTED: closure `48bdc104…9139` MATCH, and the R1 and R2 digests MATCH. As a re-run of the path P7 had already run, it exposed no outcome beyond the record already accepted. It is not A1 step 5, which re-runs P7 at H after the build (§8).

| Measure | Value |
|---|---|
| P7 wall, 80 session-replays (2 runs × 40 sessions) | 352.6 s |
| Acceptance re-execution | 316.8 s wall, 279.2 s CPU, single-threaded |
| Peak memory | 564 MiB |

Probe 1 could not separate fixed from per-session cost. Probe 2 supersedes its per-session reading.

### 6.2 Probe 2: two window lengths

- **Authority.** Joshua's direct answer on 2026-10-02 (sheet 2 item 1, "all recommended"): "one more probe at two window lengths, wall and CPU only".
- **Harness.** `t00_probe2.py`, SHA-256 `3c8130c7…ad2e`, plus a v2 build-only variant (`8cf9ec07…7dd7b`). Both are scratch files, not committed.
- **Scope.** It ran on head `d716106` over the P7 path only, at 20 and 40 sessions, with no outcome read.

| Measure (CPU unless stated) | Value |
|---|---|
| Build | about 173 s (166–180); peak 562 MiB working set |
| Integrity check through `verify_for` (`_verify_integrity`, `production_source.py:1166-1182`) | about 71.4 s per call, repeated on every `replay_bracket` call (`_check_path`, `:1193-1194`) |
| `replay_bracket` | t = 74.36 ± 1.39 + (0.0885 ± 0.044) × sessions. The slope's 95% interval is [−0.034, 0.211], so it is not distinguishable from zero |
| Wall | about 1.2–1.3 × CPU, because of host contention |
| Kernel (`evaluate_replay`) | not timed; the in-run probe includes it |
| Host | i3-N305, 8 cores, 15.6 GiB |

### 6.3 Cost model and linearity

- **One screen path** (1,500 sessions × 2 runs, one call), as `replay_bracket` runs today: about 207 s CPU, or 390 s at the slope's upper bound.
- **With the integrity check hoisted** to per-worker epochs (row K6): about 136 s per path, 320 s upper.
- **Overheads** (row B5): each worker epoch costs the build plus two integrity checks, about 316 s; an 8-worker segment adds about 0.7 CPU-hours. The candidate pass adds one epoch, about 185 s (430 s upper) of chronological brackets, and the probe path.
- **Linearity is untested beyond 40 sessions.** The slope comes from two short windows, and its interval includes zero. The in-run probe (rows B2, B3) runs after the freeze and is the first timing of a true 1,500-session path. A cost above the budget-implied rate refuses there, as INSUFFICIENT, and that consumes #581 (row S4). Setting the path budget from the upper column below confines that refusal to a cost above probe 2's 95% bound.

**Projections (recorded; per-call integrity, as `replay_bracket` runs today):**

| N per population (×3 populations) | 8 cores, point | 8 cores, upper |
|---|---|---|
| 1,000 | 21.6 h | 40.7 h |
| 3,000 | 64.8 h | 122 h |
| 10,000 | 9.0 d | 16.9 d |
| 30,000 | 27 d | 51 d |

### 6.4 Depth options (§12 item 9)

The table below is derived from §6.3 with the integrity hoisted (× 136/207 at the point, × 320/390 at the upper bound): CPU on 8 cores, and wall at 1.2–1.3 × CPU. It excludes overheads (§6.3). The standard error is √(p(1−p)/N) at the threshold, per population. A2 scores point estimates, so a true rate within about 2 SE of a threshold can fall on either side in another draw.

| Option | N per population | Pass-floor SE at 50% | Bust-ceiling SE at 5% | CPU, point–upper | Wall, about |
|---|---|---|---|---|---|
| a | 1,000 | 1.6% | 0.69% | 14–33 h | 17–43 h |
| b | 3,000 | 0.9% | 0.40% | 42–100 h | 2.1–5.4 d |
| c | 10,000 | 0.5% | 0.22% | 5.9–13.9 d | 7–18 d |
| d | 30,000 (prereg v2's reading: 10k × 3 seeds) | 0.29% | 0.13% | 18–42 d | 21–54 d |

N = 3 × `depth_per_root`, so options a and c round to 1,002 and 10,002. Joshua sets N (#581 §3 item 1), the two budgets (§5.4) and the approval windows (§12 item 10) from this table before ratification. No depth is reduced after it (#581 A6). The memory check is W × peak ≤ 0.8 × RAM: 8 × 562 MiB is about 4.4 GiB of 15.6 GiB, and the in-run probe re-measures the peak at full length (§5.1).

---

## 7. Sharding and compute

- **Key universe.** `K = {(root, population, path_index) : path_index < depth_per_root[population]}`, sorted canonically. The plan digest is the SHA-256 of that list.
- **Assignment.** Round-robin by ordinal mod W, so every shard gets a mix of populations. A resume may change W: the coordinator re-partitions `K − completed` among W′ workers, and SEGMENT_START records the assignment digest and the witness keys (row S13). The coordinator dispatches each key through the gate (row B4).
- **Determinism.** Each outcome is a pure function of (receipt bytes, authority bytes, key). Every `screen_bracket` builds fresh engines (`production_source.py:1239-1263`), and no process-global cache selects a replay (rows R1, S16).
- **Scale.** prereg v2's reading is 30,000 paths per population (90,000 in total): 27 days on 8 cores at the probe-2 point, 51 at the upper bound, or about 18–42 days with the integrity hoisted (§6.3–§6.4).
- **Where it runs.** On the operator's local machine only. r3c's inputs include the accepted runtime ports, which may not leave the operator's primary checkout or go to any external service (AGENTS.md, private read surface), and the private root is local. So there is no cloud and no GLM. The options are a dedicated local run with sleep disabled, at a depth from §6.4 (§12 item 9).
- **Integrity cost.** `_verify_integrity` runs on every `replay_bracket` call, about 71.4 s each (§6.2). The screen hoists it to two checks per worker epoch (row K6); `replay_bracket` keeps its per-call check.

---

## 8. Sequencing with #611 and P7

Every build PR must land **before** H. P7 acceptance is tied to its exact head: `code_head` is in the record and is not a volatile field (`p7_evidence.py:38`), so a record presented at any other head fails. Step 3 then runs from a detached worktree at H, and later commits on `main`, including ratification, do not affect it. Neither timing probe (§6) is step 7.

| # | Step | Seat | Gate |
|---|---|---|---|
| 0 | A3: ORB-3 and VAN-3 answered, with exposure markers (standing) | Joshua | Before AUTHORITY_BOUND (row A10) |
| 1 | Lift the #611 and A9-PREP holds; merge #611 | coordinator / Joshua | — |
| 2 | Coordinator review → one narrow Codex review → **Joshua approves this design and the §12 decisions** | Joshua | No code before this |
| 3 | Settle #581 §3 item 8 and the A5/A6 text; merge #581 as DRAFT with A5/A6 frozen, adding a dated note that names the frozen commit and the A5/A6 section hashes. **This amends A1's order** (§12 item 5) | Joshua | Before the build, because the verdict code pins the hashes |
| 4 | Docs PR: the §11 addendum, A10b reasons, #581 §5 item 3 wording, and the §3 cells as pointers to the values block | CC | — |
| 5 | **Joshua approves the build card** (files of §9, packets of §9.1) | Joshua | Before any code |
| 6 | Build packets (§9.1), red-first, rebased on #611 | see §9.1 | Every packet merged → **H** |
| 7 | Joshua signs a **fresh r3c approval** whose window covers steps 7–12 (§12 item 10); **one P7 re-run** at H (A1 step 5); `t00_screen accept-p7` → record R and `p7_acceptance.json` | Joshua; executor / coordinator | Closure covers `production_source.py` and `p7_evidence.py` |
| 8 | Depth and budget from §6.4; Joshua decides §12 item 9. Any further probe needs its own dated answer and stays on P7's path windows (row G4) | coordinator / Joshua | — |
| 9 | Set and ratify #581 §3 and the `t00-step2-values/v1` block → C; C′ records C's SHA and nothing else (row A8). Record #581 OD-1 at the D-feed owner before step 3 returns | Joshua | — |
| 10 | Commit and review the independent label script (row X5) | coordinator | Before step 11 |
| 11 | Signing packet: authority bytes and SHA-256, scope, schema and subject, every binding, key fingerprint, the `p7_acceptance.json` SHA-256, and a statement that ratification left the A5/A6 bytes untouched; coordinator reviews; **Joshua signs `APPROVE_T00_SCREEN_AUTHORITY`** (row G5) | Joshua | — |
| 12 | Step 3, once: `run` → `finalize` → `verify` | executor / coordinator | Label recorded at the T00 owner |

---

## 9. Files (admitted only by a later build card)

| File | Change | In the P7 closure? |
|---|---|---|
| `ops/c1_rail/qualification/screen_authority.py` (new) | Schema constants, compiled r3c digest and pre-registration chain, validator, `_check_bindings`, receipt registry, `require_validated_screen_authority`, epochs and stat guard, `ScreenBracket`, act validator | No (forbidden in P7) |
| `ops/c1_rail/qualification/t00_screen/` (new package): `__init__.py`, `__main__.py` (CLI), `coordinator.py`, `worker.py`, `state.py` (`advance`, `classify`, `check_record`), `journal.py`, `plan.py`, `verdict.py` | Run driver | No (forbidden in P7 as one prefix) |
| `ops/c1_rail/qualification/production_source.py` | `screen_epoch`, `screen_bracket`, `_verify_identity`, `_consumed_splits`; sealed methods untouched (row K7) | **Yes** (covered by the planned re-run) |
| `ops/c1_rail/qualification/p7_evidence.py` | Bootstrap template parametrization; forbidden-list additions | **Yes** (covered by the planned re-run) |
| `scripts/t00_screen_label_check.py` (new) | The independent label recompute | No |
| `tests/ops/qualification/test_source_consumers.py` | Allowlist keyed by (owner, capability); new capabilities in the scan | — |
| `tests/ops/qualification/test_screen_authority.py`, `test_t00_screen_plan.py`, `test_t00_screen_verdict.py`, `test_t00_screen_state.py`, `test_t00_screen_driver.py` (new); `test_production_source.py`, the P7 tests | §10 | — |
| `docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md` | §11 dated addendum (separate docs PR) | — |
| #581 pre-registration | §5 item 3 names this authority; §3 cells point to the §6 values block | — |

**Forbidden:** `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py`, `replay.py`, `book_policy.py`, `core/` (including `dd_protection.py` and `mc/`), and any Pine, port or private artifact. Also forbidden are any edit to r3c's bytes or the pinned key, and any test that reads the real source.

### 9.1 Build packets (parallel against frozen interfaces)

| Packet | Scope | Depends on | Route |
|---|---|---|---|
| P-A | `screen_authority.py`; rows A1–A11, K1–K4, X2, X3 | — | CC solo (trust/auth: never GLM) |
| P-B | `production_source.py` and `p7_evidence.py` changes; A10b; rows K5–K10 | #611 merged | CC solo (P7 closure, security) |
| P-C | `t00_screen/verdict.py`; rows V1–V4 (synthetic rows only) | — | GLM-eligible: worktree `workdir`, no private data |
| P-D | `t00_screen/state.py` and `journal.py`; rows S1–S3, S9, S10, S13–S16 (fake source) | — | CC (the transition function is the crash model) |
| P-E | `t00_screen/plan.py`; rows R1–R3 | P-B interface | Cursor or CC |
| P-F | `coordinator.py`, `worker.py`, `__main__.py`, `accept-p7`, Job Object, probe; rows S4–S8, S11, S12, B1–B5, X1, X4–X6; integration tests | P-A to P-E | CC integration |

---

## 10. Tests

The 2026-09-30 attribution rule applies. Tests use TEST_ONLY keys generated in-process, with only the pinned root and the validator's repository-root constant monkeypatched, and synthetic fixtures. **No test reads the real source.**

- **Invariant tests.** One per §2.2 row from A1 to X6, named `test_<row>`. Each is red-first, builds an input that violates only that row, asserts that row's code, and has a passing twin. G rows are checked by the audit hooks and review.
- **Integration tests** (real subprocess workers, a deterministic fake source, injection only through a TEST_ONLY seam):
  - I1, every crash window of §4.4 from its own ledger prefix: the final `results.json` equals the uninterrupted run's bytes, or the stated class is reached;
  - I2, Ctrl-C through `fp.ps1` lands as W22 and resumes;
  - I3, every prefix of a recorded ledger folds through `advance` to the state the run was in when that prefix was durable.
- **Revision-2 test map.** T1→A1; T2→A3; T3→A2; T4→K1, K5; T5→A5, A7; T6→A8–A10; T7→K2; T8→K7, K8; T9→K9; T10→K10; T11→R1, S16; T12→V2; T13→V1, V4; T14→S3, S13, S14; T15→S4–S6, X3; T16→B2; T17→I1, S12; T18→B4, B5; T19→R2; T20→R3; T21→X1; T22→X4, X5; T23→S9, S10.
- **Regression:** A1–A23 of the 2026-09-30 spec, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py`, and `fp.ps1 check`, each with its cited `.cache/fp-verification` record.

---

## 11. Proposed dated addendum to the 2026-09-30 spec (A2; not edited in this PR)

**At `:124`, appended after the existing paragraph:**
> *Addendum 2026-10-0X (operator ruling A2, 2026-10-02).* The receipt itself still authorizes only the path above, and its `refusals` are unchanged. A source built from it may additionally serve `ProductionSource.screen_epoch` and `ProductionSource.screen_bracket`, and only those, while a validator-issued `ValidatedScreenAuthority` binds this receipt object and its exact `contract_sha256`, and only inside a screen-bootstrap worker of a ledgered T00 step-3 run. That authority has schema `t00_screen_authority/v1` and scope `APPROVE_T00_SCREEN_AUTHORITY` ([T00 screen-authority design](2026-10-02-t00-screen-authority-design.md)). The authority, not this receipt, authorizes the T00 step-3 screen and its kernel calls. `verify_for` still refuses the source for every qualification consumer, and `replay`, `replay_bracket` and `proof` still return sealed types and still check integrity on every call. Without a screen authority, every statement in this section holds unchanged.

**At `:358`, appended after the procedural rule:**
> *Addendum 2026-10-0X (operator ruling A2).* The rule is unchanged: no P7 record, P7 worksheet or `SourceOnly*` value is ever a screen input. A T00 step-3 run under a signed screen authority builds its own `ProductionSource` from the r3c receipt, in its own process, and obtains `BracketReplayResult`s only through `screen_bracket`. Those are screen outputs, not P7 output. The screen consumes the P7 record only as an acceptance precondition (its digest, `schema`, `contract_sha256`, `code_head`, `code_closure_sha256`, `bootstrap_sha256` and interpreter), never its result fields. Pre-ratification timing probes run only on the path P7 already ran, each under its own dated operator answer, and report wall and CPU time only.

**Consequential edits:**
- `:159`: "generated only for source contracts" becomes "generated only for source contracts, T00 screen authorities and T00 screen acts".
- `:342`: the superseded dominance description becomes a pointer to the deny-by-default scan (Status line) and its §9 widening.

---

## 12. Operator decisions at approval

Answer "all recommended except …".

1. **Design core and wording** (§2–§3, §5.1, §9, §11): the signed authority class; `screen_bracket` with its own loop, scored by the unchanged `evaluate_replay`, sealed methods untouched; one bootstrap template; A10b keyed by (owner, capability); the §11 addendum in a separate docs PR before H.
   *Recommend: adopt.* (Alternative: a duplicate scorer, which makes #581 A4's wording false.)
2. **Signing key.** Reuse `source:1ebae5d45bc51280` under two new scopes, `APPROVE_T00_SCREEN_AUTHORITY` and `APPROVE_T00_SCREEN_ACT`; scope separation is in the signed bytes.
   *Recommend: adopt.* (Alternative: a dedicated `screen:` key, with a second ceremony and edits at `contract.py:1001-1005` and `trust_domain.py:318-319`.)
3. **#581 OD-2 and OD-1** (relayed, confirmation pending): OD-2 = declared book, bound as `expressions: "DECLARED_BOOK"` (the editions would void r3c and this design); OD-1 = (c), recorded at the D-feed owner before step 3 returns.
   *Recommend: confirm both.*
4. **Launch bindings** (rows A1–A11): signature before any `git` call; HEAD, tree and interpreter read by the validator; P7 by binding plus the compiled bootstrap and closure checks; C→C′ changes only the SHA line; A3 by compiled paths and patterns on the §3 row.
   *Recommend: adopt.*
5. **Freeze A5/A6 before the build** (amends A1's order: part of step 6 moves ahead of step 4). Ratification must then leave the A5/A6 bytes untouched, or H, the build and P7 repeat.
   *Recommend: yes.*
6. **Values block** `t00-step2-values/v1` in #581 §6, with the §3 cells pointing to it: S0 only and Run-1 WAIVED (any other choice needs a new design), candidates flat in both runs, `LOWER_NEAREST_RANK_INF_INCLUDED`, H from A6; you set the RNG roots, `probe_root` and L, without seeing candidate counts.
   *Recommend: yes.*
7. **Budget and stops** (§4.3, §5.4): CPU only; a gated path budget (A6) and an overhead reserve that HALTs; crashes STOP or HALT and never end a run; a run is scored if the gate never refused a key; wall is recorded, not gated.
   *Recommend: adopt, with both budgets set from the §6.4 upper column.* (Alternatives: any crash VOIDs; strict `runner.py:120-122` parity; also gate wall.)
8. **Freeze point, acts and re-attempts** (§4.5): #581 is consumed at AUTHORITY_BOUND; TERMINATE and CONTINUE are your signed acts, listing every reader's exposure; any later attempt needs a successor pre-registration with an exposure statement and a code change.
   *Recommend: adopt.*
9. **Compute location and depth** (§6.4, §7): local only, because the private inputs cannot leave this machine; N ≈ 1,000, 3,000 or 10,000 per population, or 30,000 (prereg v2's reading, about 18–42 days).
   *Recommend: choose N from §6.4 by the days you can dedicate the machine; no number is recommended here.*
10. **Approval windows.** Fresh r3c and screen approvals with `expires_at` ≥ start + the upper wall figure for your N (§6.4) + `verify` time; r3c-a2 expires 2026-10-09T01:52:19Z (#581 §5).
    *Recommend: yes.*
11. **Result access and acceptance** (§5.6): the fixed console lines; exposure = any run-directory read or other output; the label script committed before signing; k = 9 re-executions; the coordinator runs `accept-p7`, or you run it yourself to close the §13 residual.
    *Recommend: adopt, with the coordinator running `accept-p7`.*

---

## 13. Risks and residuals

- **Dynamic and lexical access.** `getattr(src, 'screen_' + 'bracket')`, `source._quotes` and `source._domain` are outside A10b. Rows K1–K5 and the process boundary enforce instead.
- **In-process forgery.** Rows K3 and K4 read state that the screen bootstrap sets. Code running inside a screen-bootstrap process can set or bypass that state, just as it can call `_engine` directly. A script outside one lacks the recorder state; a script that builds a ledgered run directory under the bound root consumes #581 (row S4), so a preview defeats itself.
- **P7 acceptance is attested to the validator, not proven.** The validator checks the bindings, the compiled bootstrap and the closure digest (row A7). It cannot tell a reproduced record from a fabricated one that lists the true current hashes, and Joshua's signature authenticates only the bytes he is shown. To close this, Joshua runs `accept-p7` himself (§12 item 11).
- **Integrity epochs.** The residuals are in §3.3: in-process mutation is caught at close; a restored-mtime rewrite is caught at close or at the next start; a killed worker's records have no closing check.
- **Single use is local.** Deleting the run directory and relaunching is a procedural breach, not something code prevents. A copied private root fails row A6. The attestation and the ledger of attempts are the detectors.
- **Head drift.** Any commit before step 7 voids P7 at H. All packets must land first (§8).
- **Approval expiry mid-run.** A path started inside the window completes; the next refuses. Only Joshua's renewal resumes it, and only his TERMINATE act ends it. Size the windows (§12 item 10).
- **Compute and linearity.** prereg v2's depth needs about 18–42 days locally (§6.4). Linearity past 40 sessions is untested, and the in-run probe's refusal, after the freeze, consumes #581. No reduced depth is ever substituted after ratification (#581 A6).
- **Candidate scarcity.** A long L, or flatness in both runs, can empty the H1/H2 candidates and give INSUFFICIENT. L is chosen without candidate counts, because a pre-freeze candidate pass would expose W20's trigger.
- **Probe leakage.** Pre-ratification timing touched only sessions P7 had already exposed (§6). The in-run probe runs after AUTHORITY_BOUND, which is after the freeze (row S4).
- **Ctrl-C under `fp.ps1`** is a hard kill (`scripts/fp.py:274`, `:330`): resumable, with in-flight keys counted as losses (row S10).
- **Kernel trust.** P7 stubs the kernel, so P7 is no evidence that the kernel is correct. Kernel correctness rests on the existing runner and simulation tests, plus `code_head` binding.
- **Unhashed native libraries and data files.** Bound only through the interpreter and lock identity in the P7 record. This is a T05 hermeticity residual for both P7 and the screen.
- **Relabelling.** Screen output could be relabelled. This is mitigated by `evidence_class`, its own schemas and an unchanged `verify_for`. Any other use is a procedural violation.
- **Peeking.** Run directories are readable in the private root before `finalize`. A run ends early only on a deterministic #581 A6 cause, evidence of corruption, a key-lifecycle event or Joshua's signed act, which states every reader's exposure (rows S9, X2, X3). Any re-attempt needs a successor pre-registration (row S4).
- **Consumed-split count.** "A path with a consumed split" is read as either run having consumed one. The count is descriptive only.

**Residual risks** (the round-3 judge's list, copied):
- **CONTINUE acts:** every crash in BOUND, PREPARED or PROBING, every cap hit and every exhausted overhead reserve needs his signed CONTINUE, listing every reader's exposure. Over a run of days to weeks, expect several.
- **Single use is local:** the only thing stopping a relaunch is the run root (row A6) plus procedure. Deleting the run directory, or an identical-values authority under another root, is a procedural breach that code does not prevent. Results are deterministic, so neither can bias the verdict.
- **Killed path-worker epochs** rest on the opening check, the per-call checks, duplicate equality, witnesses and `verify`'s k = 9 re-executions, not on a closing check (§3.3).
- **P7 acceptance is attested to the validator, not proven,** unless Joshua runs `accept-p7` himself (§12 item 11).
- **Linearity is untested beyond 40 sessions.** The in-run probe runs after the freeze, so a cost above budget consumes #581. Set both budgets from the §6.4 upper column.
- **Mid-run worktree edits:** after edit 6 (row K6), an edit to the H worktree during a run STOPs it, and `resume` refuses until the tree is restored. Loaded-byte drift and a failed integrity check stay terminal (INSUFFICIENT).
- **#581 OD-1 and OD-2** are relayed and still need his direct confirmation (§12 item 3). Choosing the editions voids r3c and this design.

---

## Audit hooks

```bash
# r3c refuses SCREEN/MONTE_CARLO exactly; unchanged by this design (expect the constants and the exact-match check).
rg -n 'SOURCE_PURPOSE = "T00_P7_SOURCE_VERIFICATION"|"SCREEN", "MONTE_CARLO"|doc\["refusals"\] != list\(SOURCE_REFUSALS\)' ops/c1_rail/qualification/contract.py

# The fence this design keeps: verify_for refuses; evaluate_replay requires ReplayResult; replay_bracket checks integrity per call.
rg -n "SOURCE_ONLY_NOT_QUALIFICATION" ops/c1_rail/qualification/production_source.py
rg -n "isinstance\(result, ReplayResult\)" ops/c1_rail/qualification/runner.py
rg -n "def _check_path|self\._verify_integrity\(\)" ops/c1_rail/qualification/production_source.py

# The two O(source-size) checks the epoch hoists (row K6).
rg -n "_source_execution_snapshot\(self\) != issued\[1\]|_qualification_snapshots\(contract, dict\(self\.prepared\.retained_bytes\)\)" ops/c1_rail/qualification/production_source.py

# The run flags the screen wrapper carries are the ones replay_bracket computes and _seal records.
rg -n "failed = False|result, failed = exc.result, True|provider\._placed" ops/c1_rail/qualification/production_source.py

# P7 record fields row A7 checks: schema, closure digest, contract digest, and P7's own bootstrap check.
rg -n "RECORD_SCHEMA = 't00-p7-evidence/v1'|code_closure_sha256=sha256_bytes\(canonical\(closure\)\)" ops/c1_rail/qualification/p7_evidence.py
rg -n "'contract_sha256': receipt.contract_sha256|bootstrap_sha256 != p7_evidence.P7_BOOTSTRAP_SHA256" ops/c1_rail/qualification/p7_driver.py

# P7's forbidden-module rule is exact name or package prefix (row K10).
rg -n "name == module or name.startswith\(module \+ '.'\)" ops/c1_rail/qualification/p7_evidence.py

# Ctrl-C under fp.ps1: the launcher kills its child (W15 = W22).
rg -n "return subprocess.call\(command, cwd=root, env=child_env\)|except KeyboardInterrupt" scripts/fp.py

# A3 (row A10): each successor's own OWED pattern, applied to its first ORB-3/VAN-3 row (the §3 row) only.
# Expect no output once A3 is answered; today it names both files.
for f in docs/briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md docs/briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md; do
  awk '/^[|] (ORB|VAN)-3 /{print; exit}' "$f" | grep -qE '\| \*\*OW[E]D|\(OW[E]D,|— OW[E]D \(' && echo "A3 OWED: $f"; done

# Qualification seeds are stage-scoped; the screen tag must not appear in regime.py.
rg -n "'n1', 'n2', 'n3', 'probe'|tb-s2-rng-v2" ops/c1_rail/qualification/regime.py
rg -c "t00-screen-rng" ops/c1_rail/qualification/regime.py || echo "0 (expected)"

# P7 forbids the screen (post-build: expect both names in the list).
rg -n "c1_rail.qualification.screen_authority|c1_rail.qualification.t00_screen" ops/c1_rail/qualification/p7_evidence.py

# A10b covers the new capabilities and the raw paths (post-build).
rg -n "CAPABILITY_CALLS = " tests/ops/qualification/test_source_consumers.py

# Forbidden files untouched by the build (run on the build PR; expect no output).
git diff --name-only origin/main...HEAD -- ops/c1_rail/qualification/{contract,trust_domain,runner,provider,blocks,paths,regime,bracket,model,replay}.py ops/c1_signal_daemon/book_adapters.py core/

# No private value or count in this file (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md | grep -v 'rg -n'
```

---

## Appendix A. Finding → invariant

**Round 1** (review of `101cf1b`):

| Finding | Summary | Rows |
|---|---|---|
| P1-1 | `screen_bracket` dropped the deadline flags and consumed splits | K8, R3, V4 |
| P2-1 | The validator took HEAD, tree, interpreter and readers as arguments | A5 |
| P2-2 | The P7 record was not tied to r3c, and acceptance was not persisted | A7, X6 |
| P2-3 | The A3 check was ambiguous across the two `VAN-3` rows | A10 |
| P2-4 | The A4 probe leaked a deadline outcome through its timing | G4 |
| P2-5 | Exceptions were not mapped to crash windows | S9 |
| P2-6 | A crash could reset the budget, and orphaned workers outlived the coordinator | B4, B5, S11, S12 |
| P2-7 | Peek, then abandon; no one named who may end a run | S4, X2, X3 |
| P3-1 | Wrong `bracket.py` citations | G1 |
| P3-2 | The 1,500-session horizon was not tied to A6 | A11, V3 |
| P3-3 | Section hashes are fragile under ratification | A9 (§12 item 5) |
| P3-4 | The screen expiry carried the source expiry code | K2 |
| P3-5 | Torn tail plus in-segment restart | S2, S3 |
| P3-6 | Witness and run-directory edge cases | S6, S13 |
| P3-7 | The budget probe could be re-rolled | B2 |
| P3-8 | Multi-day local compute needs Joshua | G3 (§12 item 9) |
| P3-9 | `probe_root` and the roots are not #581 terms | A11 |
| P3-10 | `verify` gaps (approval, independence) | X4, X5 |
| P3-11 | The pre-registration binding allowed unseen edits | A8 |
| P3-12 | Revision 1's OD-5 amends A1's order | G3 (§12 item 5) |
| Q7 | Deletions: role map, per-root gating, per-worker candidate recompute | A1, R2 |

**Round 2** (review of `09486ef`):

| Finding | Summary | Rows | Fold |
|---|---|---|---|
| P1-1 | The freeze started too late, and a re-attempt edited a frozen #581 | S4, S5, X2 | Freeze at AUTHORITY_BOUND; `PREREG_CONSUMED`; `SCREEN_ATTEMPT_OPEN`; successor chain (§4.5, §12 item 8) |
| P2-1 | C→C′ let values change; §3/§6 completeness unchecked; OD-2 dependency | A8, A11 | Only the SHA line may change; §3 cells point to the block; §6 fields non-blank; `expressions` (§12 item 3) |
| P2-2 | Unsigned routes turned a running screen into INSUFFICIENT | S7, S9, S10, S15, B5 | `FINALIZE_NOT_COMPLETE`; resume refusal without state change; HALTED for non-deterministic caps |
| P2-3 | Nothing confined the authority to the bootstrap or the run | K3, K4, X4 | Bootstrap hash and run binding; `verify` inside the gate; §13 residual |
| P2-4 | P7 acceptance self-attested; C3 overclaimed | A7, X6 | Compiled bootstrap and closure checks; C3 reworded; §13 residual and §12 item 11 option |
| P2-5 | The A3 check could not pass; inputs unpinned | A4, A10 | Compiled paths and patterns on the §3 row; reachable commits; audit hook fixed |
| P2-6 | Build cost outside the projection, inside the gate | B1, B2, B4, B5 | Path budget and overhead reserve; probe in a built worker; §5.4 formula |
| P2-7 | Stale probe authority and costs; standing probe permission | G4 | §6 rewritten with both probes' authority and outputs; "any time" deleted |
| P2-8 | Workers wrote WORKER_STOP into the coordinator's ledger | S2 | WORKER_STOP is the worker journal's last record; the coordinator copies it into SEGMENT_END |
| P2-9 | Loss counts not durable; `OSError` resumes uncapped | S10 | KEY_START losses across segments; I/O cap |
| P2-10 | Outcome leaks outside the exposure rule | X1, X2 | Exposure redefined; fixed console per subcommand; no shard markers |
| P3-1 | Probe ordering; Ctrl-C under `fp.ps1` | B2, S12 | Checks before PROBE_START; W21 precedence; Ctrl-C documented as W22 |
| P3-2 | A10b keyed by owner; `_seal` refactor touched `replay` | K7, K9 | Own loop and copied placement expression; (owner, capability) allowlist; lexical residual in §13 |
| P3-3 | Unsigned fields reached `git` | A2, A4 | Signature second; commit syntax; `--end-of-options` |
| P3-4 | `t00_screen*` inexpressible in P7's list | K10 | `t00_screen` is a package; explicit screen list |
| P3-5 | State-model gaps | S1, S3, S6, S8, S9, S11, S12, S13, B4 | §4.1–§4.4 |
| P3-6 | Wording and accuracy | G2, G3, G5, V3 | Header reworded; token tests; §12 item 6; §13 L wording; §8 steps 3 and 5; act packet; §11 `:159` |
| Dropped (Integrity P2-4) | OD-1 recorded before step 3 returns | G3 | §8 step 9 |

**Revision-3 inputs** (second probe and its design consequences):

| Input | Rows |
|---|---|
| (a) Integrity once per worker epoch | K6 |
| (b) Budget model with build and integrity separated | B1, B4, B5 |
| (c) Compute location and depth | G3 (§6.4, §12 item 9) |
| (d) Linearity untested beyond 40 sessions | B3 (§6.3) |
