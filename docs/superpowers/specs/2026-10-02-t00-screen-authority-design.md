# T00 screen authority: design

**Date:** 2026-10-02.
**Status:** DRAFT — design only; Joshua approves before any code (operator ruling A1 2026-10-02).

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
- **A4.** One real-source timing probe, measuring wall and CPU time only and no outcomes, is allowed before #581 is ratified.

**Precedent:** [T00 source-only contract design](2026-09-30-t00-source-only-contract-design.md), revision 4.2, operator-accepted. Its structure, attribution rule and refusal discipline carry over here.

**Review path:** the coordinator reviews, then one narrow Codex review, then Joshua approves (A1 step 3).

**Code read at:** `origin/main@d5d559b`. The cited `ops/` and `tests/` files are byte-identical to `d716106`, where the three input proposals were read. #611 (OPEN) edits `production_source.py` only, so its line numbers are re-anchored after #611 merges.

**Pre-registration read:** #581 at its PR head, `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md`, status DRAFT. This design cites #581 by section only and restates none of its values.

**Private-value rule.** This file holds no Pine, port body, private value, account identifier or P&L. The r3c digest, the key ID and the dates below are already public.

---

## 0. Design basis: three proposals judged

Three proposals were drafted independently, each through one lens. Each was scored on four criteria:
- whether it keeps the r3c fence and the accepted P7 machinery intact;
- whether it keeps #581 A4 and A6 true as written;
- the size of the trust surface it adds;
- whether its crash and compute story is complete.

| Proposal | Score /10 | Strength | Weakness |
|---|---|---|---|
| **Authority lens** (backbone) | **8.5** | Adds one gated method, `ProductionSource.screen_bracket`, that returns an unsealed `BracketReplayResult`. The **unchanged** `runner.evaluate_replay` scores it, so #581 A4 ("through `runner.evaluate_replay`") stays literally true. It edits nothing in `contract.py`, `trust_domain.py`, `book_adapters.py` or `runner.py`. It has the most precise schema and validation order. | Its crash and resume model is thin. It binds the r3c *approval* digest, which blocks approval renewal. It pins the A5/A6 hash without settling when the text freezes. |
| **Integrity lens** | 8.0 | Spots several real problems: a hand-built `AcceptedP7Record` proves nothing (`p7_evidence.py:436-441`); `code_head` voids acceptance at any other head; A10b misses `_replay_raw` and `_engine`; P7 says nothing about the kernel. Also contributes the A3 digest binding, a one-line console, and coordinator recompute with a hash-derived re-execution sample. | Its "closure-only enumeration" misses modules imported lazily inside functions (`_engine` imports at call time, `production_source.py:1239-1245`). It voids a whole attempt on any infrastructure crash. |
| **Execution lens** | 7.0 | Best state model: crash windows, hash-chained journal, timestamp-free `results.json`, budget across segments, probe cost model, deterministic re-partitioning. | Duplicates the scorer on top of sealed outputs (`screen/score.py`). That makes #581 A4's wording false, needs #581 edits, and opens a drift surface. Its stated reason, keeping the P7 closure untouched, is moot: a P7 re-run is already planned (A1 step 5). It also has no in-run probe, although #581 A6 names one. |

**Backbone:** the authority proposal. **Grafted:** from the integrity proposal, the A10b widening, the A3 binding, the console policy, coordinator recompute and re-execution, the rule that only record bytes are accepted, and the refusal on an F1 source. From the execution proposal, the state model and journal, crash windows W0–W18, budget accumulation across segments, the probe cost model, deterministic re-partitioning, and approval expiry held only in the approval payload.

**Conflicts resolved:**

| # | Conflict | Resolution | Why |
|---|---|---|---|
| C1 | Scoring: a duplicated scorer over sealed rows (execution) against a raw `BracketReplayResult` from a gated method (authority, integrity) | **Gated `screen_bracket`**, scored by the unchanged `evaluate_replay` | #581 A4 and A6 name `runner.evaluate_replay` and `runner.py` lines. A duplicate would need #581 rewording and a differential test forever. The edit to `production_source.py` falls in the P7 re-run that is already planned. |
| C2 | Whether the authority binds the r3c **approval** digest (authority) | **It does not.** It binds the r3c **contract** digest and the P7 record digest. Any valid pinned OPERATOR approval over the r3c bytes may build the source. Each one is recorded in the attestation. | Every approval over r3c is an equally authoritative signature over the same bytes. Binding one approval's digest would make an expiry mid-run unrecoverable even when Joshua renews. |
| C3 | P7 check at launch: re-run `accept_p7_record` (integrity), or check bindings only | **Check bindings only, with no re-execution:** the record's SHA-256 equals the signed `p7.record_sha256`; `_current_bytes_check` passes (`p7_evidence.py`, `:443`, called by `accept_p7_record` at `:482`); HEAD equals `code_head` with a clean tree; the interpreter equals the record's | Joshua's signature over the record digest defeats a forged record or a forged acceptance object. Re-executing would be a second P7 run, which A1 does not allow, and it would need the P7 approval to still be valid. |
| C4 | Screen code identity: a signed `screen_closure_sha256` from an enumeration (integrity/execution), or the commit | **Bind `code_head` H (clean tree) plus the interpreter.** Every shard records its loaded closure, and all shards must agree. | A git commit binds every first-party byte, including modules imported lazily. Enumerating without running would under-record them. |
| C5 | Crash disposition: VOID the attempt (integrity), or resume (execution, authority) | **Deterministic resume** after an infrastructure crash, with every attempt logged and a resume witness. Context refusal, budget exhaustion and abandonment are terminal INSUFFICIENT. Decided at OD-9. | Each per-path outcome is a pure function of (receipt bytes, authority bytes, key). A resume draws nothing new and cannot select outcomes. |
| C6 | In-run probe: none (execution), or present (authority) | **Present**, with the CPU projection `probe_cpu × total_paths ≤ max_cpu_seconds`. A refusal is INSUFFICIENT. | #581 A6 names the budget probe and its refusal. CPU makes the projection independent of shard count, and a dispatch gate bounds wall time. |
| C7 | Shard plan: signed into the authority (integrity), or a launch value | **A launch value**, recorded in the ledger | Results do not depend on W (test T11). Signing W would make a resume on a different machine impossible for no integrity gain. |
| C8 | Bootstrap: parametrize `p7_evidence` (authority), or a separate copy (implied) | **Parametrize one template.** P7's string is generated from it with P7's parameters. | One implementation of the audit hook and recording finder, instead of two security-critical copies. The P7 re-run absorbs the `P7_BOOTSTRAP_SHA256` change. |

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
| 5 | `run_bracket` needs an engine-level `build_replay` | `bracket.py:27-46` |

Two more facts shape the design:
- A single-run replay (`run is None`) refuses any instant without a reviewed schedule price (`production_source.py:442-452`, `:475-479`). On the real source, a candidate-edge pass therefore needs the bracket rather than `proof`.
- The production executors are retired or TEST_ONLY (`production.py`, `orchestration.py`).

Widening r3c would change its digest and void the P7 identity that #581 A1 binds. The screen therefore needs a **second, narrower door**: a separately signed object that wraps r3c and does not edit it.

---

## 2. Behavioral contract

### 2.1 What it is

A **T00 screen authority** is a canonical JSON document with schema `t00_screen_authority/v1`. One operator signature under the new scope `APPROVE_T00_SCREEN_AUTHORITY` turns it into a `ValidatedScreenAuthority` receipt.

**What the receipt authorizes, exactly:**
- **One consumer path, on a source built from the bound r3c receipt in a screen-bootstrap process:** `ProductionSource.screen_bracket(path, *, authority)` → `BracketReplayResult`, then `runner.evaluate_replay` on each run, then the A5 counting and A6 verdict functions. This is used **once**, for T00 step 3 under the ratified #581.
- The A4 timing probe (§6) does not need the receipt. Ruling A4 is its authority.

**What it refuses, as a declaration** (enforced in §2.6 and §5):
- qualification stages, Part A, F1 and decision rules;
- seal, admission, deployment and arm;
- four-firm §4 falsifier evidence (#581 §1b);
- parameter changes.

**What does not change:**
- The r3c receipt, `build`, `verify_for` and `_resolve_domain` are unchanged.
- The sealed `replay`, `replay_bracket` and `proof` are unchanged.
- `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py` and `core/` are unchanged.
- Without a screen authority, every statement in the 2026-09-30 spec holds unchanged.

### 2.2 Invariants

1. **Opening the fence takes all of the following:**
   - an issued, unchanged `ValidatedScreenAuthority`;
   - an issued, unchanged r3c receipt whose `contract_sha256` equals the authority's;
   - **object identity** between the authority's bound receipt and `self.contract`;
   - valid approval windows and pin state for both, re-checked on **every** call.
2. `verify_for` still raises on an r3c source with or without an authority. So `ProductionExecutor`, `execution/compute.py` and `execution/evidence.py` still refuse.
3. Every screen output carries `evidence_class: "T00_STEP3_SCREEN"` and the label **"T00 step-3 screen evidence; not qualification, F1, admission, deployment or four-firm §4 falsifier evidence"**. Execution and seal parsers accept only their own schemas.
4. **P7 output is never a screen input**, which is the 2026-09-30 spec's rule at `:358`. The screen consumes the P7 record only as an acceptance precondition (digest, `code_head`, `code_closure_sha256`, `bootstrap_sha256`, interpreter), never its result fields.
5. No R2-P&L/R1-lows hybrid enters the verdict (#581 A4).
6. Every parameter that can move a verdict is in the signed bytes. Seeds are a deterministic function of the signed roots and the key. Nothing is chosen after a scored path exists.

---

## 3. Schema

Canonical bytes are `contract.canonical_json_bytes` (`contract.py:266`), and they must round-trip through `parse_canonical_json` (`:289`). The authority SHA-256 is the SHA-256 of those bytes. The field set is closed, and any extra or missing field is refused.

| Field | Content | Validation (refusal code) |
|---|---|---|
| `schema` | `"t00_screen_authority/v1"` | exact (`SCREEN_AUTHORITY_FIELDS`) |
| `authority_id` | text | nonempty |
| `purpose` | `"T00_STEP3_SELECTED_BOOK_SCREEN"` | exact |
| `grants` | `["T00_STEP3_SCREEN_ONCE"]` | exact |
| `refusals` | `["QUALIFICATION_STAGES","PART_A","F1","DECISION_RULES","SEAL","ADMISSION","DEPLOYMENT","ARM","FALSIFIER_EVIDENCE","PARAMETER_CHANGE"]` | exact |
| `evidence_class` | `"T00_STEP3_SCREEN"` | exact |
| `source.contract_sha256` | r3c digest | equals the **compiled** `T00_SCREEN_SOURCE_CONTRACT_SHA256` **and** the bound receipt's `contract_sha256` (`SCREEN_SOURCE_MISMATCH`) |
| `source.roles` | the 25 roles → SHA-256 | key set equals `SOURCE_CONTRACT_ROLES`; the map equals `receipt.runtime_load_sha256` (`SCREEN_SOURCE_MISMATCH`) |
| `p7.record_sha256` | SHA-256 of the accepted P7 record's bytes | recomputed from the presented bytes (`SCREEN_P7_MISMATCH`) |
| `p7.code_head` | 40-hex H | equals the record's `code_head`, the executing checkout's `HEAD`, and a clean tree |
| `p7.code_closure_sha256`, `p7.bootstrap_sha256`, `p7.interpreter` | — | each equals the record's value; the executing interpreter equals `p7.interpreter` |
| `prereg.path` | `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md` | exact |
| `prereg.commit` | the commit C′ whose blob is bound (§6 complete) | reachable from `origin/main` |
| `prereg.ratifying_commit` | C, the SHA written in #581 §6 | equals the §6 line; an ancestor of, or equal to, C′ |
| `prereg.blob_sha256` | SHA-256 of `git show C′:<path>` | recomputed; the Status line matches `RATIFIED \d{4}-\d{2}-\d{2}` (`SCREEN_PREREG_MISMATCH`) |
| `prereg.a5_text_sha256`, `prereg.a6_text_sha256` | section hashes (exact bytes between the A5/A6 headings and the next heading) | recomputed from the blob **and** equal to the compiled `A5_TEXT_SHA256` / `A6_TEXT_SHA256` in the verdict module (OD-5) |
| `a3_answers` | `[{path, commit, blob_sha256, row}]` for the ORB-3 and VAN-3 rows of the two 2026-10-02 successor pre-registrations | each blob recomputes; the named row is no longer `OWED` and carries the `Answerer exposure:` marker those files define (`SCREEN_A3_UNANSWERED`) |
| `parameters` | the closed set below | equals, byte for byte, the canonical JSON values block `t00-step2-values/v1` inside the ratified #581 §6 (OD-6) (`SCREEN_PARAMETER_UNSUPPORTED` / `SCREEN_PREREG_MISMATCH`) |
| `source_trust` | the pinned map | equals `_source_trust_document(SOURCE_SIGNING_KEYS)` (`contract.py:1037-1041`) |

**`parameters`** is a closed set. Each entry maps to a #581 §3 item; this design restates none of their values.

| Key | #581 item | Validation |
|---|---|---|
| `scenarios` | 7 | `["S0"]` only. r3c carries PRISTINE only (`contract.py:1156-1159`), and S1 needs a new source contract (OD-16) |
| `initial_state` | §2 A3 | equals `receipt.initial_state` |
| `horizon_sessions` | prereg v2 G4 (reused) | positive integer |
| `rng` | 4 | `{tag:"t00-screen-rng/v1", roots:[3 distinct strings derived from the prereg v2 seeds], probe_root}`, with `probe_root` distinct from every root |
| `seed_pooling` | 1 | `"POOLED_PER_POPULATION"` or `"PER_ROOT_GATING"` (OD-6) |
| `depth_per_root` | 1 | `{FULL,H1,H2}` → positive integers |
| `block` | 4 | `{family:"JOINT_FLAT_BOTH_RUNS", length_sessions:L}`. Requires `horizon % L == 0` (`paths.py:48-49`) and `L ≤` the smallest pool |
| `path_start_date` | 4 | equals `receipt.path_start_date` |
| `pass_floor_halves` | 2 | `"BINDING"` or `"REPORTED"` |
| `deadline_only_is_bust` | 3 | bool |
| `run1_diagnostic` | 5 | `"WAIVED"` only. The runner fixes `consistency=.40` (`runner.py:27`) |
| `a5_rule` | 8 | `"T00_A5/v1"` (the drafted rule), or a successor ID compiled in the verdict module |
| `median_rule` | A2/A5 reading | `"LOWER_NEAREST_RANK_INF_INCLUDED"` (OD-6) |
| `budget` | 1 | `{max_wall_seconds, max_cpu_seconds}`, finite and positive |

**Excluded:**
- **F1 fields:** `replay`, `result_plan`, `approval_policy`, `coverage`, `clocks`, `trust_domain_sha256`, `policy_sha256`.
- **r3c-only fields:** `artifacts`, `historical_pins`, `port_runtime_pins`, `populations`.
- **The r3c approval digest** (C2).
- **Shard count and worker count** (C7).
- **Expiry.** It lives only in the approval payload (`contract.py:383-385`), so the authority SHA-256 is stable when Joshua renews an approval.

A document that carries any excluded field is refused.

### 3.1 Approval

- **Payload.** A detached Ed25519 approval verified by `verify_detached_approval` (`contract.py:366-435`), with:
  - `scope = APPROVE_T00_SCREEN_AUTHORITY`;
  - `subject_sha256 = contract_sha256 =` the authority SHA-256;
  - `authority_class = OPERATOR`;
  - `allow_test_authority=False`.
- **Signer.** The pinned `source:1ebae5d45bc51280` (OD-2). The trust checks follow `contract.py:1171-1191`:
  - the supplied public keys must hash to the pin;
  - the signer must start with `source:` and be pinned;
  - the approval must verify;
  - `_check_source_key_lifecycle` then runs.
- **Scope exclusivity is already in the signed bytes** (`contract.py:389`):
  - a screen approval never verifies as a source contract (`SOURCE_SCOPE`, `:1189`), as `FREEZE_F1` (`:928`) or as a trust domain;
  - a source approval never verifies as a screen authority.
- **No path into qualification.** `source:` key IDs remain refused in qualification domains (`contract.py:1001-1005`; `trust_domain.py:318-319`). The authority never enters a `QualificationTrustDomain`.

### 3.2 Validator and receipt

New module `ops/c1_rail/qualification/screen_authority.py`. It **imports** the existing helpers in `contract.py` and edits none of them. The helpers are `_fields`, `_text`, `_receipt_snapshot`, `_pinned_source_keys`, `_source_trust_document`, `_check_source_key_lifecycle`, `verify_detached_approval`, `require_validated_source_contract` and `canonical_json_bytes`.

The validator's signature is `validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, prereg_reader, a3_reader, code_head, interpreter, now)`. It runs these steps in order, and each step has its own code:

1. Bytes, canonical round trip, closed fields, and exact schema, purpose, grants, refusals and evidence class (`SCREEN_AUTHORITY_FIELDS`).
2. `require_validated_source_contract(source_receipt, now=now)` (`contract.py:1229-1233`), then the source bindings (`SCREEN_SOURCE_MISMATCH`).
3. P7 bindings: the record hash, `p7_evidence.parse_record` (`:376`), field equality, HEAD and a clean tree, the interpreter, and `_current_bytes_check` (`SCREEN_P7_MISMATCH`). There is no re-execution (C3).
4. Pre-registration bindings: the blob, Status, ancestry, the A5 and A6 section hashes against the compiled constants, and the values block equal to `parameters` (`SCREEN_PREREG_MISMATCH`).
5. A3 rows (`SCREEN_A3_UNANSWERED`).
6. Parameter semantics (`SCREEN_PARAMETER_UNSUPPORTED`).
7. Trust and signature, as §3.1 (`SCREEN_TRUST_ROOT_MISMATCH` / `SOURCE_KEY_*` / scope mismatch).
8. Issue a frozen `ValidatedScreenAuthority`. It holds:
   - `authority_sha256`;
   - the `approval` and the key SHA-256;
   - a **reference to the exact `source_receipt`**;
   - read-only `parameters`;
   - the P7 and pre-registration bindings;
   - `evidence_class`.

   Registration in `_ISSUED_SCREEN_AUTHORITIES` uses a weakref plus a snapshot, the same pattern as `contract.py:1211-1215`.

`require_validated_screen_authority(auth, *, source_contract, now)` runs on every use. Each failure has its own code:
- issued and unchanged;
- `auth.source_receipt is source_contract`, and the SHA-256 values are equal;
- the screen approval window and the pin lifecycle (`SCREEN_APPROVAL_EXPIRED` / `SOURCE_KEY_REMOVED` / `SOURCE_KEY_CHANGED` / `SOURCE_KEY_REVOKED`).

### 3.3 The one capability: `ProductionSource.screen_bracket`

```python
def screen_bracket(self, path, *, authority):
    if not _is_source_only(self.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT')
    from .screen_authority import require_validated_screen_authority   # lazy: P7 never loads it
    require_validated_screen_authority(authority, source_contract=self.contract, now=_now())
    return self._bracket_results(path, seal=False)                      # BracketReplayResult(r1, r2)
```

- **Refactor.** `replay_bracket`'s body (`production_source.py:1215-1237`) moves verbatim into `_bracket_results(path, *, seal)`. `replay_bracket` keeps its exact outputs: sealed `SourceOnlyBracket` on r3c, `BracketReplayResult` on F1.
- **Every call is checked.** `_check_path` → `_verify_integrity` still runs, so the r3c lifecycle (`:1180-1182`) is re-checked per call, in addition to the screen-authority check.
- **Deadline handling.** A deadline failure becomes that run's result, exactly as in `replay_bracket` (`:1229-1236`). `BracketReplayResult.__post_init__` (`model.py:225-235`) enforces one fresh `ReplayResult` per run.
- **Ordering.** Every refusal fires **before** `_engine` is called (test T4).

---

## 4. State model, event sequences and crash windows

### 4.1 States

```
UNBOUND ─launch checks─▶ PREPARED ─probe ok─▶ RUNNING(k) ─▶ { RESUMABLE(k) | TERMINAL_INSUFFICIENT }
   │                         │                    │                ▲         │
   └─LAUNCH_REFUSED          └─probe refused──────┴────────────────┘         ▼
     (no run dir; no output)   ▶ TERMINAL_INSUFFICIENT          AGGREGATED ▶ REPORTED ▶ FINAL
```

**Launch checks run before any run directory exists:**
- the authority (§3.2);
- the r3c validation, with its artifacts re-hashed through `ObservedBindings`;
- HEAD and a clean tree, with `core.autocrlf=false`;
- the interpreter;
- the A3 rows.

A refusal at this stage is **LAUNCH_REFUSED**. No directory, replay or output exists, and nothing is consumed. Fixing the cause and relaunching is allowed.

**Freeze point.** The run directory `<private_root>/t00-step3/<authority_sha256>/` is created with O_EXCL; if it already exists, the result is `SCREEN_ALREADY_RUN`, unless the call is a resume of a RESUMABLE run. From the **first fsync'd path record**, step-3 output exists, and from then on #581 is frozen. A3 must already be bound.

### 4.2 Persistence (private root only; absolute path outside any worktree)

| File | Write discipline | Content |
|---|---|---|
| `lock` | held by the coordinator process (`msvcrt.locking`); workers hold per-shard locks | pid, host |
| `manifest.json` | temp file → fsync → `os.replace`, once, at PREPARED | the authority, r3c, P7-record and code-head digests; per-population `candidates_sha256`; plan digest (the SHA-256 of the sorted key universe) |
| `run_ledger.jsonl` | append + fsync, hash-chained | AUTHORITY_BOUND, PREPARED, PROBE{cpu, wall}, SEGMENT_START{k, W, approval SHA-256s}, WORKER_STOP{reason}, SEGMENT_END{state, wall, cpu, peak mem}, AGGREGATED, REPORTED, FINAL or TERMINAL_INSUFFICIENT{reasons} |
| `journal/seg{k}-w{i}.jsonl` | append + fsync per record, hash-chained per file; never rewritten | key, seed, `path_sha256`, and per run: status, `sessions_to_pass`, failure reason, `kernel_outcome`, sessions replayed, `deadline_failure`, consumed-split count, `events_sha256`, run digest (the `p7_driver.py:55-59` projection). No P&L series |
| `results.json` | canonical JSON, atomic replace | a pure function of (authority SHA-256, r3c SHA-256, P7 record SHA-256, plan digest, sorted outcome multiset): A5 tallies under both assignments, the A6 verdict, labels. **No timestamps, W, approvals or timings** |
| `REPORT.md` | rendered from `results.json` only, by a fixed template | cites the SHA-256 of `results.json` |
| `attestation.json` | atomic | the SHA-256s of results, report, ledger head and every journal head; the approval chain (every r3c and screen approval used); segments; the per-shard loaded closure |

### 4.3 Event sequences

**Happy path**

| Step | Event |
|---|---|
| 1 | Launch checks pass |
| 2 | Create the run directory with O_EXCL |
| 3 | AUTHORITY_BOUND |
| 4 | Candidate pass (§5.2); `manifest.json` written; PREPARED |
| 5 | In-run probe (§5.4); PROBE |
| 6 | SEGMENT_START 1 |
| 7 | Workers append path records |
| 8 | SEGMENT_END COMPLETE |
| 9 | `finalize`: coverage check, then AGGREGATED, then REPORTED |
| 10 | Console prints exactly `T00_SCREEN_VERDICT <label> results_sha256=<hex>`, then FINAL |

**Approval lapse**

| Step | Event |
|---|---|
| 1 | At the start of path p, `screen_bracket` refuses (`SOURCE_APPROVAL_EXPIRED` or `SCREEN_APPROVAL_EXPIRED`) |
| 2 | The worker writes WORKER_STOP(APPROVAL_LAPSE) and exits |
| 3 | The segment is RESUMABLE |
| 4 | Joshua signs a fresh approval over the **same** bytes. The subject digests are unchanged, so keys, seeds and outcomes are unchanged |
| 5 | `resume` re-runs the launch checks, then SEGMENT_START 2 |
| 6 | The resume witness passes, and the run continues |

**Context refusal**

| Step | Event |
|---|---|
| 1 | A worker raises `CONTEXT_REFUSAL` on key x |
| 2 | The coordinator stops all workers |
| 3 | TERMINAL_INSUFFICIENT{CONTEXT_REFUSAL, x} |
| 4 | `finalize` writes completed counts only, no rates (OD-9) |

### 4.4 Crash windows

| # | Window or event | Detection | Outcome |
|---|---|---|---|
| W0 | Crash before `manifest.json` is durable | no manifest | No output exists. Resume repeats PREPARED; the candidates are deterministic |
| W1 | Crash after the manifest, before any path record | no journal records | Resume behaves the same as a start |
| W2 | Worker killed mid-replay | no record for that key | RESUMABLE; the key is recomputed, identical by determinism |
| W3 | Torn final journal line | the last line fails parse or chain | Drop that tail only (TORN_TAIL) and recompute the key. A break anywhere else is TERMINAL `CORRUPTION` |
| W4 | A durable record exists and the key is recomputed after resume | duplicate key | Identical projection: deduplicate. Different projection: TERMINAL `NONDETERMINISM` |
| W5 | Resume witness | each worker first recomputes the last completed key of its previous shard | Mismatch: TERMINAL `NONDETERMINISM` |
| W6 | Crash during aggregation, report or attestation | missing or temp files | Re-run `finalize`; the outputs are byte-identical |
| W7 | Crash after REPORTED, before FINAL | the ledger lacks FINAL | `finalize` re-verifies the digests and appends FINAL idempotently |
| W8 | Approval lapse (source or screen) | refusal at path start, before any engine runs | STOP, RESUMABLE (§4.3). No renewal by `finalize`: INSUFFICIENT `APPROVAL_LAPSE_UNRENEWED` |
| W9 | Wall or CPU budget exhausted with keys left | dispatch gate (§5.4) | TERMINAL `BUDGET_EXHAUSTED` |
| W10 | `ReplayNeedsContext`, a source refusal, or a shape-check failure (§5.3) | worker exception | Fail fast; TERMINAL `CONTEXT_REFUSAL` with the key |
| W11 | Head, tree, interpreter or P7 binding drift between segments | SEGMENT_START repeats the launch checks | TERMINAL `CODE_OR_ARTIFACT_DRIFT` |
| W12 | Private artifact bytes change | `ObservedBindings` refusal (`contract.py:1110-1112`) or `_verify_integrity` | TERMINAL `CODE_OR_ARTIFACT_DRIFT` |
| W13 | Disk full, or an antivirus lock on a journal file | write failure | Worker stops; RESUMABLE |
| W14 | A second coordinator starts | lock held | Refused; the existing run is unaffected |
| W15 | Operator interrupt (Ctrl-C) | signal | RESUMABLE |
| W16 | Operator `abandon` | explicit command | TERMINAL `ABANDONED`; it can never become GO |
| W17 | A record for a key outside the plan, or outside that shard's assignment | aggregation | TERMINAL `CORRUPTION` |
| W18 | Machine sleep or hibernation | wall budget counts only active segment time; a sleep-spanning segment counts in full | Disable sleep for the run. Monotonic-clock behaviour across sleep is pinned in a test |
| W19 | In-run probe ends in a deadline failure, cannot complete, or projects over `max_cpu_seconds` | probe step | TERMINAL INSUFFICIENT (#581 A6 budget-probe clause) |
| W20 | Candidate pass: an empty population, an empty candidate set, or a proof-path deadline failure | PREPARED step | TERMINAL INSUFFICIENT `CANDIDATES_UNAVAILABLE` (OD-7) |

---

## 5. Driver

### 5.1 Process topology (local machine only; private data never leaves it)

**Coordinator.** `fp.ps1 python -m c1_rail.qualification.t00_screen {preflight|run|resume|finalize|verify|abandon|probe} <args>`.

**Workers.**
- Each worker is a child process `sys.executable -I -S -B -c SCREEN_BOOTSTRAP`, generated from the shared bootstrap template (C8). It records an audit hook and a recording finder, as P7 does (`p7_evidence.py:57-339`).
- The environment is pinned: `PYTHONHASHSEED=0`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` all `=1`, and a separate process group.
- Workers pickle nothing. **Every worker validates r3c and the authority and builds its own `ProductionSource`**, because receipts and sources are registered per process (`contract.py:1211-1215`; `production_source.py:1160-1164`).

**Screen forbidden modules:**
- `production`, `orchestration`, `result_adjudication`, `seal`, `execution.*`, `part_a`, `benchmark*`, `p7_driver`.
- The screen **stubs** `runner._run_stage` and `runner.run_synthetic_stage`.
- `evaluate_replay`, `simulate_path` and `bracket` load **live**.

**P7 forbidden modules gain** `c1_rail.qualification.screen_authority` and `c1_rail.qualification.t00_screen*`, so P7 can never reach the screen.

### 5.2 Candidate pass (PREPARED; §3 item 4 convention, OD-7)

For each population pool, in `partition_populations` order (`blocks.py:35-38`):
1. Assemble the chronological path, as `proof` does at `production_source.py:1268`.
2. Run `screen_bracket` on it.
3. Derive each run's edges as `proof` does (`:1282-1291`), and the joins from `self.adjacent`.
4. Compute `JointFlatBlocks(pool, edges_r, L, joins).candidates()` (`blocks.py:28-32`) for R1 and for R2. The candidates are their **intersection**.
5. Treat any of the following as `CANDIDATES_UNAVAILABLE`, mirroring `provider.py:36-54`:
   - a deadline failure in either run;
   - a run shorter than the pool;
   - discontinuous edges;
   - an empty candidate set.

Each worker repeats the pass, and its `candidates_sha256` must equal the manifest's.

`proof` is not used. Its single-run provider refuses unreviewed instants (§1), and its sealed output on r3c holds edges only after a single run.

### 5.3 Per path

```
for key in assigned_keys - completed_keys (ascending canonical order):
    budget.dispatch_gate()                                            # §5.4
    seed = int.from_bytes(sha256(canonical(["t00-screen-rng/v1", purpose, root, population, path_index]))[:8], "big")
    path = PathAssembler(path_start_date).sample(candidates[population], Random(seed), horizon_sessions=H)   # paths.py:44-51
    b = source.screen_bracket(path, authority=auth)                   # both lifecycles re-checked here
    for run in (b.r1, b.r2): shape_check(run, path); outcome = evaluate_replay(run, initial_state=initial)  # runner.py:20-44
    append_record(key, seed, path_sha256, r1, r2, BracketVerdict status)   # bracket.py:89-112, fsync
```

**Seeds.**
- Seeds are separate from the qualification streams (`'tb-s2-rng-v2'`, `regime.py:22`).
- They do not reuse `regime.domain_seed`, whose stage set is qualification-only (`regime.py:12`).
- They depend on neither the authority digest nor W.

**`shape_check`** mirrors `provider.py:76-83` and #581 A6. Each run must satisfy **one** of these:
- length H and no `deadline_failure`;
- `deadline_failure` with `0 < len ≤ H`, where the last row is not flat-before-deadline and every earlier row is.

In both cases two more conditions hold:
- every `intraday_low` is finite and ≤ 0, with one per replayed session;
- `occurrence` and `source_session_id` equal the path prefix.

Anything else is `CONTEXT_REFUSAL`, or `INTRADAY_LOW_MISSING` for the low check.

**`initial`** is `EvaluationState` built from `receipt.initial_state`, as `production_source.py:1259-1261` does.

### 5.4 Budget (OD-8)

- **In-run probe.** One path from `probe_root`, population FULL, index 0, timed for wall and CPU. The CPU projection rule is `probe_cpu × total_paths ≤ max_cpu_seconds`. A probe that ends in a deadline failure or cannot complete is INSUFFICIENT (#581 A6). The probe is not scored and is not in the tallies.
- **Wall.** Cumulative active wall time across segments, measured on the coordinator's monotonic clock from SEGMENT_START to SEGMENT_END. **CPU** is the sum of every worker's `process_time`.
- **Dispatch gate.** No path starts after either budget is used up. Exhaustion with keys remaining is TERMINAL `BUDGET_EXHAUSTED`.
- **Overrun on the final path.** If every key completes and only the last path overran, the run is scored and the overrun is recorded descriptively. #581 A6 makes a budget stop INSUFFICIENT "before every population reaches its frozen depth", and this reading follows that text. It knowingly differs from `runner.py:120-122`. Strict parity is the alternative at OD-8.

### 5.5 Finalize (pure functions; no I/O inside the verdict)

**Coverage.** Every `(root, population, path_index)` must occur exactly once. Bindings and candidate digests must be identical across shards. A gap, a duplicate or a mismatch is TERMINAL INSUFFICIENT.

**A5 and A6.** `t00_screen_verdict.py` implements #581 A5 (1)–(3) and A6 **by reference to those sections**, with exact integer comparisons (`20·bust ≤ n`, `2·pass ≥ n`). It takes:
- input: outcome rows, `parameters` and the insufficiency reasons;
- output: `INSUFFICIENT(reasons)`, `GO-evidence`, or `NO-GO-evidence{robust | UNDETERMINED-dependent}`.

When any insufficiency reason exists, the function is never handed tallies, and a report shows completed counts only (OD-9). The hybrid is a labelled diagnostic only.

**Mapping of the #581 A6 triggers to screen codes.** The A6 text is left verbatim.

| #581 A6 trigger | Screen code / where enforced |
|---|---|
| `ReplayNeedsContext`, a source refusal, or a short series without a confirmed deadline failure | `CONTEXT_REFUSAL` (§5.3, W10) |
| A run lacks its own synchronized `intraday_low` | `INTRADAY_LOW_MISSING` (§5.3) |
| P7 is not accepted for A1's identities at the executing head | LAUNCH_REFUSED before any output; `CODE_OR_ARTIFACT_DRIFT` mid-run (W11) |
| The runner raises `NeedsContext` (budget, a missing prerequisite, or a probe that cannot complete) before full depth | `BUDGET_EXHAUSTED` (W9); probe refusal (W19); `CANDIDATES_UNAVAILABLE` (W20); `APPROVAL_LAPSE_UNRENEWED` (W8); `ABANDONED` (W16) |
| Any §3 item is unset | The authority cannot validate (§3), so the screen cannot launch |
| A confirmed own-flat deadline failure on a scored path | A scored outcome, never INSUFFICIENT (§5.3 shape rule) |

### 5.6 Console, access and coordinator acceptance (OD-17)

**Console output.**
- stdout is exactly one line: `T00_SCREEN_VERDICT <GO-evidence|NO-GO-evidence-robust|NO-GO-evidence-UNDETERMINED-dependent|INSUFFICIENT> results_sha256=<hex>`.
- stderr carries refusal codes and shard-done markers only.
- No count or rate appears on any console, in CI or in a PR.

**`verify` subcommand** (the coordinator seat):
1. Re-validate offline the authority, the approvals and r3c.
2. Check the console digest against `sha256(results.json)`, the journal hash chains, and coverage.
3. Recompute the label with a **coordinator-written script that does not import `t00_screen_verdict`**, working from the ratified #581 A5/A6 text.
4. Re-execute k paths whose indices are derived from `sha256(results.json)`, and compare their rows byte for byte.

The result is VERIFIED or REFUTED.

**Public reporting.** Only the label is public. A public figure may only cite the private RESULTS path (`load_bearing_numbers.md` §1).

---

## 6. A4 timing probe (before #581 ratification)

**Mode.** `t00_screen probe` runs under the screen bootstrap with `evaluate_replay` and `simulate_path` **stubbed to refuse**, as P7 does (`p7_evidence.py:327-329`).
- It needs **no screen authority**; ruling A4 is its authority. That is recorded in its A10b allowlist reason.
- It uses only r3c, under a valid r3c approval, and the **sealed** `replay_bracket`.

**What it measures:**
1. Build cost: validate and `build`, giving wall, CPU and peak working set.
2. One sealed `replay_bracket` on the FULL chronological path. The result is discarded in memory.
3. The same call in W concurrent processes, W ∈ {1, W_target}, giving efficiency `e(W)` and peak memory per worker.
4. Kernel cost: `simulate_path` on synthetic zero series of length H, in a separate process that builds no source and reads no private data.

**Output.** An allowlisted schema of keys:
- wall, CPU, peak memory;
- the input path length (public: FULL 997);
- the W values;
- the derived per-input-session cost.

There are no fills, labels, deadline flags, session counts replayed or candidate counts. stderr is limited to refusal codes.

**Using P7 itself as the probe is rejected.** The P7 record exposes `deadline_failure`, fills and labels (`p7_driver.py:55-74`), which would contaminate #581 §3 item 3 before ratification.

**Residual, accepted under A4.** Timing correlates weakly with activity: a run cut short by a deadline is faster.

**Use.** The coordinator projects `cost_per_path ≈ build/W + H × per-session cost × 2 + 2 × kernel` and tabulates, for candidate depths, the projected wall days and CPU hours against the approval windows. Joshua sets #581 §3 item 1 (depth and budget) from that table. Any reduction of depth happens here, before ratification, never after.

---

## 7. Sharding and compute

- **Key universe.** `K = {(root, population, path_index) : path_index < depth_per_root[population]}`, sorted canonically. The plan digest is the SHA-256 of that list.
- **Assignment.** Round-robin by ordinal mod W, so every shard gets a mix of populations. A resume may change W: the coordinator re-partitions `K − completed` among W′ workers, and SEGMENT_START records the assignment.
- **Determinism.** Each outcome is a pure function of (receipt bytes, authority bytes, key). Every `screen_bracket` builds fresh engines (`production_source.py:1239-1263`), and no process-global cache selects a replay. Test T11 shows that W=1 and W=4 give identical `results.json` bytes.
- **Scale.** The prereg v2 reading of 10k × 3 roots × 3 populations is about 90k paths, each with 2 runs of H sessions. That is days of single-process compute. W is chosen from the A4 probe (`W·mem ≤ 0.8·RAM`, maximum throughput).
- **Where it runs.** On the operator's local machine only. There is no cloud and no GLM, because private data stays local.
- **Per-path integrity cost.** `_verify_integrity` rehashes the retained bytes on every call (`production_source.py:1179`). The probe measures it, and it may dominate the fixed cost per path.

---

## 8. Sequencing with #611 and P7

Every build PR must land **before** H. P7 acceptance is tied to its exact head: `code_head` is in the record and is not a volatile field (`p7_evidence.py:38`), so a record presented at any other head fails as `P7_RECORD_NOT_REPRODUCED`. Step 3 then runs from a detached worktree at H, and later commits on `main`, including ratification, do not affect it.

| # | Step | Seat | Gate |
|---|---|---|---|
| 0 | A3: ORB-3 and VAN-3 answered, with exposure markers (standing) | Joshua | Before any step-3 output |
| 1 | Lift the #611 and A9-PREP holds; merge #611 (`production_source.py`) | coordinator / Joshua | — |
| 2 | Coordinator review → one narrow Codex review → **Joshua approves this design and OD-1…OD-18** | Joshua | No code before this |
| 3 | Settle #581 §3 item 8 and the A5/A6 text; merge #581 as DRAFT with A5/A6 frozen (OD-5) | Joshua | Before the build, because the verdict code pins the section hashes |
| 4 | Spec-amendment docs PR (§11), A10b reasons, #581 §5 item 3 wording | CC | — |
| 5 | Build packets (§9.1), red-first, rebased on #611 | see §9.1 | Every packet merged → **H** |
| 6 | Joshua signs a **fresh r3c approval** whose window covers steps 7–11 (OD-10) | Joshua | — |
| 7 | **One P7 re-run** at H; coordinator `accept_p7_record` → record R | executor / coordinator | Closure covers `production_source.py` and `p7_evidence.py` |
| 8 | A4 probe at H (§6) → depth and budget table | executor | After P7, so the timings are clean |
| 9 | Set and ratify #581 §3, including the `t00-step2-values/v1` block → C, C′ | Joshua | — |
| 10 | Signing packet: authority bytes, SHA-256, every binding listed, key fingerprint; coordinator reviews; **Joshua signs `APPROVE_T00_SCREEN_AUTHORITY`** | Joshua | — |
| 11 | Step 3, once: `run` → `finalize` → `verify` | executor / coordinator | Label recorded at the T00 owner |

---

## 9. Files (admitted only by a later build card)

| File | Change | In the P7 closure? |
|---|---|---|
| `ops/c1_rail/qualification/screen_authority.py` (new) | Schema constants, compiled r3c digest, validator, receipt, registry, `require_validated_screen_authority` | No (forbidden in P7) |
| `ops/c1_rail/qualification/t00_screen_plan.py` (new) | Key universe, seeds, candidate pass, shape check, shard assignment | No |
| `ops/c1_rail/qualification/t00_screen_verdict.py` (new) | A5/A6 pure functions; `A5_TEXT_SHA256` / `A6_TEXT_SHA256` | No |
| `ops/c1_rail/qualification/t00_screen_journal.py` (new) | Ledger, journal, manifest, results, attestation writers; torn-tail and chain rules | No |
| `ops/c1_rail/qualification/t00_screen.py` (new) | CLI; launch checks; coordinator, worker, probe, finalize and verify | No |
| `ops/c1_rail/qualification/production_source.py` | `screen_bracket`, plus the verbatim `_bracket_results` refactor | **Yes** (covered by the planned re-run) |
| `ops/c1_rail/qualification/p7_evidence.py` | Bootstrap template parametrization; forbidden-list additions | **Yes** (covered by the planned re-run) |
| `tests/ops/qualification/test_source_consumers.py` | Scan widening and allowlist entries (OD-14) | — |
| `tests/ops/qualification/test_screen_authority.py`, `test_t00_screen_plan.py`, `test_t00_screen_verdict.py`, `test_t00_screen_journal.py`, `test_t00_screen_driver.py` (new); `test_production_source.py`, the P7 tests | §10 | — |
| `docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md` | §11 dated addendum (separate docs PR) | — |
| #581 pre-registration | §5 item 3 names this authority; §6 values block | — |

**Forbidden:** `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py`, `replay.py`, `book_policy.py`, `core/` (including `dd_protection.py` and `mc/`), and any Pine, port or private artifact. Also forbidden are any edit to r3c's bytes or the pinned key, and any test that reads the real source.

### 9.1 Build packets (parallel against frozen interfaces)

| Packet | Scope | Depends on | Route |
|---|---|---|---|
| P-A | `screen_authority.py`, T1–T7 | — | CC solo (trust/auth: never GLM) |
| P-B | `screen_bracket` + refactor; bootstrap parametrization + forbidden lists; A10b widening; T8–T10, T16 | #611 merged | CC solo (P7 closure, security) |
| P-C | `t00_screen_verdict.py`, T12–T13 (synthetic rows only) | — | GLM-eligible: worktree `workdir`, no private data |
| P-D | `t00_screen_journal.py`, T14, T17–T18 (fake source) | — | GLM- or Cursor-eligible |
| P-E | `t00_screen_plan.py`, T11, T19 | P-B interface | Cursor or CC |
| P-F | `t00_screen.py` integration, probe, T15, T20–T22 | P-A to P-E | CC integration |

---

## 10. Tests (red-first; each negative asserts its own code and has a passing twin)

The 2026-09-30 attribution rule applies. Tests use TEST_ONLY keys generated in-process, with only the pinned root monkeypatched, and synthetic fixtures. **No test reads the real source.**

| ID | Test | Falsifier |
|---|---|---|
| T1 | Canonical round trip and closed fields; each F1 field, each r3c-only field, the r3c approval digest, a shard count or an expiry in the doc is refused | Any variant validates |
| T2 | Scope exclusivity: a source-scope approval over the authority digest is refused; a screen approval is refused by `validate_source_contract`, `validate_frozen_contract` and the trust-domain validator | A cross-scope signature verifies |
| T3 | Signer: TEST_ONLY, non-`source:`, unpinned, self-signed with a matching self-registry, revoked, expired or fingerprint-changed are each refused | Any verifies |
| T4 | `screen_bracket` refuses with no authority, a foreign authority, an authority bound to another receipt object (same SHA-256, different object), or on an F1 source. A spy shows `_engine` is never called | A mismatched source replays |
| T5 | P7 binding: record hash, `code_head` ≠ HEAD, dirty tree, interpreter, or a closure file changed (`_current_bytes_check`) are each refused; a hand-built `AcceptedP7Record` is never an input | A stale or forged P7 binds |
| T6 | Pre-registration: Status not RATIFIED, blob hash, ancestry, values block ≠ `parameters`, or A5/A6 hash ≠ compiled are each refused; A3 row `OWED`, or a missing exposure marker, is refused | An unratified or edited prereg, or an unanswered A3, binds |
| T7 | Lifecycle: a mutated or lookalike authority is refused; expiry of the screen or r3c approval between calls refuses the next `screen_bracket`; a renewal over the same bytes passes | A replay runs expired, or renewal changes results |
| T8 | Fence intact: with a valid authority, `replay`, `replay_bracket` and `proof` still return `SourceOnly*`; `verify_for` still raises; the A10 consumers still refuse; `replay_bracket` outputs are byte-identical before and after the refactor | Any fenced path opens |
| T9 | A10b: calls and attribute loads of `screen_bracket`, `_bracket_results`, `_replay_raw` and `_engine` are flagged; a planted consumer in `ops/`, `scripts/` or `tools/` fails the scan | An unlisted consumer passes |
| T10 | P7 refuses to import `screen_authority` and `t00_screen*` (`P7_FORBIDDEN_IMPORT`); the screen refuses `production`, `execution`, `seal` and `p7_driver`, and the stubbed `_run_stage`; existing A16–A23 stay green on the template-generated P7 bootstrap | A cross-process reach succeeds, or P7 behaviour changes |
| T11 | Determinism: W=1 and W=4, and an uninterrupted run against a three-segment run, give byte-identical `results.json`; screen seeds never equal `domain_seed` for the same indices | Results depend on W or segmentation, or streams collide |
| T12 | A5: every (1) row, every (2) agreed rule and every (3) assignment, under both item-3 values; `UNDETERMINED` always stays in the denominator; boundaries at exactly 5% and 50%; the median with even n and ∞ | Any misclassification |
| T13 | A6: GO, NO-GO robust and NO-GO `UNDETERMINED`-dependent; every INSUFFICIENT trigger in the §5.5 mapping; tallies are never read when a reason exists; the halves toggle | Any trigger yields GO or NO-GO |
| T14 | Journal: a torn tail is accepted; a break mid-file is refused; an identical duplicate is deduplicated; a divergent duplicate is `NONDETERMINISM`; a key outside the plan or the shard is `CORRUPTION` | A corrupted journal aggregates |
| T15 | Single use: a second launch is `SCREEN_ALREADY_RUN`; a launch refusal leaves no directory; `abandon` can never yield GO | Re-draws are possible |
| T16 | Probe schema: the output keys are a subset of the allowlist; kernel calls refuse; stderr has no digits other than refusal codes | Any outcome leaks |
| T17 | Crash windows W0–W8 and W13–W16 with real subprocess workers and a deterministic fake source, injected only through a TEST_ONLY seam: final bytes equal the uninterrupted run's | Any window changes the result |
| T18 | Budget: the gate stops new paths; budget accumulates across segments; exhaustion is INSUFFICIENT; a final-path overrun follows OD-8; a probe projection over budget is INSUFFICIENT | A budget breach yields a verdict |
| T19 | Candidates: intersection across both runs; a proof-path deadline, discontinuity or empty set is `CANDIDATES_UNAVAILABLE`; `horizon % L` is enforced; digest agreement between workers | A one-run-flat block is sampled |
| T20 | Shape check: a short run without `deadline_failure`, `intraday_low > 0`, a NaN low or a prefix mismatch each refuses with its own code; a deadline run with earlier rows flat is scored | A malformed run is scored |
| T21 | Console: stdout matches `^T00_SCREEN_VERDICT (labels) results_sha256=[0-9a-f]{64}$` exactly | Any count reaches the console |
| T22 | `verify`: a changed row is caught by the hash-derived re-execution sample; the label recompute disagrees on a planted verdict bug | A tampered result verifies |

**Regression:** A1–A23 of the 2026-09-30 spec, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py`, and `fp.ps1 check`, each with its cited `.cache/fp-verification` record.

---

## 11. Proposed dated addendum to the 2026-09-30 spec (A2; not edited in this PR)

**At `:124`, appended after the existing paragraph:**
> *Addendum 2026-10-0X (operator ruling A2, 2026-10-02).* The receipt itself still authorizes only the path above, and its `refusals` are unchanged. A source built from it may additionally serve `ProductionSource.screen_bracket`, and only that method, while a validator-issued `ValidatedScreenAuthority` binds this receipt object and its exact `contract_sha256`. That authority has schema `t00_screen_authority/v1` and scope `APPROVE_T00_SCREEN_AUTHORITY` ([T00 screen-authority design](2026-10-02-t00-screen-authority-design.md)). The authority, not this receipt, authorizes the T00 step-3 screen and its kernel calls, inside the screen bootstrap process only. `verify_for` still refuses the source for every qualification consumer, and `replay`, `replay_bracket` and `proof` still return sealed types. Without a screen authority, every statement in this section holds unchanged.

**At `:358`, appended after the procedural rule:**
> *Addendum 2026-10-0X (operator ruling A2).* The rule is unchanged: no P7 record, P7 worksheet or `SourceOnly*` value is ever a screen input. A T00 step-3 run under a signed screen authority builds its own `ProductionSource` from the r3c receipt, in its own process, and obtains `BracketReplayResult`s only through `screen_bracket`. Those are screen outputs, not P7 output. The screen consumes the P7 record only as an acceptance precondition (its digest, `code_head`, `code_closure_sha256`, `bootstrap_sha256` and interpreter), never its result fields. The one pre-ratification timing probe (ruling A4) uses only the sealed `replay_bracket` and records timing fields only.

**Consequential edits:**
- `:159`: "generated only for source contracts" becomes "generated only for source contracts and T00 screen authorities".
- `:342`: the superseded dominance description becomes a pointer to the deny-by-default scan (Status line) and its §9 widening.

---

## 12. Operator decisions at approval (each with a recommendation)

1. **Adopt the authority class:** the schema, scope, purpose, grants, exact refusals and closed field set of §3. *Recommend: adopt.*
2. **Signing key.** *Recommend: reuse `source:1ebae5d45bc51280` under the new scope.* Scope separation is in the signed bytes, and `source:` IDs stay barred from qualification. The alternative is enrolling a dedicated `screen:` key, which means a second ceremony and edits at `contract.py:1001-1005` and `trust_domain.py:318-319`.
3. **Capability route.** *Recommend: one gated `ProductionSource.screen_bracket`, returning a raw `BracketReplayResult` scored by the unchanged `evaluate_replay`.* This keeps #581 A4 literally true. The alternative is a duplicated scorer over sealed rows.
4. **A2 text.** *Recommend: adopt §11 as written,* in a separate docs PR before H.
5. **Freeze the A5/A6 text before the build.** This means settling #581 §3 item 8 now and merging #581 as DRAFT. The verdict module pins the section hashes. *Recommend: yes.* Otherwise, any A5 change at ratification forces a rebuild, a new H and another P7 re-run.
6. **A machine-readable values block** `t00-step2-values/v1` in #581 §6, which must equal `parameters`. It includes `seed_pooling` and `median_rule`. *Recommend: yes, with `POOLED_PER_POPULATION` and `LOWER_NEAREST_RANK_INF_INCLUDED`.* The denominator in #581 A5 is "every path in the population". The lower median is consistent with the ≥ 50% floor at its boundary.
7. **Candidate construction** (part of #581 §3 item 4). *Recommend: a block is a candidate only if it is flat in both R1 and R2 over the chronological pool. A proof-path deadline failure, a discontinuity or an empty set is INSUFFICIENT* (following the `provider.py:36-54` precedent).
8. **Budget semantics.** *Recommend: an in-run probe with a CPU projection (refusal = INSUFFICIENT), a wall and CPU dispatch gate summed over active segments, and a fully completed run scored even if its final path overran.* The alternative is strict parity with `runner.py:120-122`.
9. **Interruptions.** *Recommend:*
   - an infrastructure crash resumes deterministically, with every attempt logged and the resume witness checked;
   - an approval lapse resumes only on a fresh approval over the same bytes;
   - a context refusal fails fast as INSUFFICIENT;
   - budget exhaustion and abandonment are INSUFFICIENT;
   - an INSUFFICIENT report carries completed counts only.

   The alternative, from the integrity lens, is that any crash VOIDs the attempt and needs a new authority with `attempt: 2`.
10. **Approval windows.** *Recommend:* both the fresh r3c approval and the screen approval have `expires_at ≥ now + 1.5 ×` the projected wall time, plus the time for `verify`. The current r3c approval expires 2026-10-09T01:52:19Z (#581 §5).
11. **A4 probe form** (§6). *Recommend: one probe process, a timing-only sealed `replay_bracket`, and the allowlisted output schema.* Using the P7 run as the probe is rejected.
12. **P7 check at launch.** *Recommend: binding checks only* (signed record digest, `_current_bytes_check`, HEAD and clean tree, interpreter), with no re-execution (C3).
13. **Bootstrap.** *Recommend: parametrize the one P7 template.* P7 forbids the screen modules, and the screen forbids the qualification, seal and execution modules (§5.1). The planned P7 re-run absorbs this.
14. **A10b widening.** *Recommend:* add `screen_bracket`, `_bracket_results`, `_replay_raw` and `_engine` to the scan, flag attribute loads of them as well as calls, and extend the scan roots to `scripts/` and `tools/`. Dynamic `getattr` stays a named residual.
15. **A3 binding.** *Recommend: machine-checked.* The authority carries the blob digests of the two successor pre-registrations with the ORB-3 and VAN-3 rows answered and the exposure markers present.
16. **Scope.** *Recommend: S0 only, with Run-1 waived* (#581 items 7 and 5). S1 needs a new non-PRISTINE source contract, and S2 contradicts T00's P1 finding.
17. **Result access and acceptance.** *Recommend:*
    - a one-line console;
    - rows read only by `finalize` and `verify`;
    - the coordinator seat reads them after the label prints;
    - an independent label recompute plus a hash-derived re-execution sample of k = 9 (one per root × population);
    - the reader's exposure is disclosed in any later successor pre-registration.
18. **#581 wording.** *Recommend:* §5 item 3 names this authority. A6 stays verbatim, and the §5.5 mapping lives here. No other #581 edit.

---

## 13. Risks and residuals

- **Dynamic access.** `getattr(src, 'screen_' + 'bracket')` is outside A10b. The in-method authority check, the process boundary and the audit hook enforce instead.
- **Single use is local.** Deleting the run directory and relaunching is a procedural breach, not something code prevents. The attestation and the ledger of attempts are the detectors.
- **Head drift.** Any commit before step 7 voids P7 at H. All packets must land first (§8).
- **Approval expiry mid-run.** It is resumable only by Joshua's renewal. Size the windows (OD-10).
- **Compute.** The wall time is unknown until the A4 probe. INSUFFICIENT is the only outcome of an undersized budget. No reduced depth is ever substituted after ratification (#581 A6).
- **Candidate scarcity.** A long L, or flatness in both runs, can empty the H1/H2 candidates and give INSUFFICIENT. L must be set knowingly (item 4).
- **Probe leakage.** Timing correlates weakly with activity. Accepted under A4.
- **Kernel trust.** P7 stubs the kernel, so P7 is no evidence that the kernel is correct. Kernel correctness rests on the existing runner and simulation tests, plus `code_head` binding.
- **Unhashed native libraries and data files.** Bound only through the interpreter and lock identity in the P7 record. This is a T05 hermeticity residual for both P7 and the screen.
- **Relabelling.** Screen output could be relabelled. This is mitigated by `evidence_class`, its own schemas and an unchanged `verify_for`. Any other use is a procedural violation.
- **Peeking.** Journals are readable in the private root before `finalize`. An abort after peeking yields only INSUFFICIENT, which can never become GO. A3 and the #581 freeze are in force before the first record.

---

## Audit hooks

```bash
# r3c refuses SCREEN/MONTE_CARLO exactly; unchanged by this design (expect the constants and the exact-match check).
rg -n 'SOURCE_PURPOSE = "T00_P7_SOURCE_VERIFICATION"|"SCREEN", "MONTE_CARLO"|doc\["refusals"\] != list\(SOURCE_REFUSALS\)' ops/c1_rail/qualification/contract.py

# The fence this design keeps: verify_for refuses; evaluate_replay requires ReplayResult.
rg -n "SOURCE_ONLY_NOT_QUALIFICATION" ops/c1_rail/qualification/production_source.py
rg -n "isinstance\(result, ReplayResult\)" ops/c1_rail/qualification/runner.py

# Qualification seeds are stage-scoped; the screen tag must not appear in regime.py.
rg -n "'n1', 'n2', 'n3', 'probe'|tb-s2-rng-v2" ops/c1_rail/qualification/regime.py
rg -c "t00-screen-rng" ops/c1_rail/qualification/regime.py || echo "0 (expected)"

# P7 forbids the screen (post-build: expect both names in the list).
rg -n "screen_authority|t00_screen" ops/c1_rail/qualification/p7_evidence.py

# A10b covers the new capability and the raw paths (post-build).
rg -n "CAPABILITY_CALLS = " tests/ops/qualification/test_source_consumers.py

# Forbidden files untouched by the build (run on the build PR; expect no output).
git diff --name-only origin/main...HEAD -- ops/c1_rail/qualification/{contract,trust_domain,runner,provider,blocks,paths,regime,bracket,model,replay}.py ops/c1_signal_daemon/book_adapters.py core/

# No private value or count in this file (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md
```
