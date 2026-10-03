# T00 screen authority: design

**Date:** 2026-10-02.
**Status:** DRAFT — design only; Joshua approves before any code (operator ruling A1 2026-10-02).
**Changelog:** Revision 2, 2026-10-02: folds review of 101cf1b.

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
- **A4.** One real-source timing probe, measuring wall and CPU time only and no outcomes, is allowed before #581 is ratified. It has run, as a timed P7 re-run (§6).

**Precedent:** [T00 source-only contract design](2026-09-30-t00-source-only-contract-design.md), revision 4.2, operator-accepted. Its structure, attribution rule and refusal discipline carry over here.

**Review path:** the coordinator reviews, then one narrow Codex review, then Joshua approves (A1 step 3).

**Code read at:** `origin/main@d5d559b`; revision 2 re-verified every cited line there after a fetch (main unchanged). The cited `ops/` and `tests/` files are byte-identical to `d716106`, where the three input proposals were read and the A4 probe ran. #611 (OPEN) edits `production_source.py` only, so its line numbers are re-anchored after #611 merges.

**Pre-registration read:** #581 at its PR head, `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md`, status DRAFT. This design cites #581 by section only and restates none of its values.

**Private-value rule.** This file holds no Pine, port body, private value, account identifier or P&L. The r3c digest, the key ID, the P7 record digest, the timings and the dates below are not private values.

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

**Backbone:** the authority proposal. **Grafted:** from the integrity proposal, the A10b widening, the A3 binding, the console policy, coordinator recompute and re-execution, the rule that only record bytes are accepted, and the refusal on an F1 source. From the execution proposal, the state model and journal, crash windows, budget accumulation across segments, the probe cost model, deterministic re-partitioning, and approval expiry held only in the approval payload.

**Conflicts resolved:**

| # | Conflict | Resolution | Why |
|---|---|---|---|
| C1 | Scoring: a duplicated scorer over sealed rows (execution) against a raw `BracketReplayResult` from a gated method (authority, integrity) | **Gated `screen_bracket`**, scored by the unchanged `evaluate_replay` | #581 A4 and A6 name `runner.evaluate_replay` and `runner.py` lines. A duplicate would need #581 rewording and a differential test forever. The edit to `production_source.py` falls in the P7 re-run that is already planned. |
| C2 | Whether the authority binds the r3c **approval** digest (authority) | **It does not.** It binds the r3c **contract** digest and the P7 record digest. Any valid pinned OPERATOR approval over the r3c bytes may build the source. Each one is recorded in the attestation. | Every approval over r3c is an equally authoritative signature over the same bytes. Binding one approval's digest would make an expiry mid-run unrecoverable even when Joshua renews. |
| C3 | P7 check at launch: re-run `accept_p7_record` (integrity), or check bindings only | **Check bindings only, with no re-execution:** the record's SHA-256 equals the signed `p7.record_sha256`; its `schema` and `contract_sha256` are P7's and r3c's; `_current_bytes_check` passes (`p7_evidence.py:443`, called by `accept_p7_record` at `:482`); the validator itself finds HEAD equal to `code_head` with a clean tree. The signing packet carries the acceptance evidence | Joshua's signature over the record digest defeats a forged record or a forged acceptance object. Re-executing would be a second P7 run, which A1 does not allow, and it would need the P7 approval to still be valid. |
| C4 | Screen code identity: a signed `screen_closure_sha256` from an enumeration (integrity/execution), or the commit | **Bind `code_head` H (clean tree) plus the interpreter.** Every shard records its loaded closure, and all shards must agree. | A git commit binds every first-party byte, including modules imported lazily. Enumerating without running would under-record them. |
| C5 | Crash disposition: VOID the attempt (integrity), or resume (execution, authority) | **Deterministic resume** after an infrastructure crash, under a closed exception table (§4.5), with every attempt logged and a resume witness. Context refusal, budget exhaustion and termination acts are terminal INSUFFICIENT. Decided at OD-7. | Each per-path outcome is a pure function of (receipt bytes, authority bytes, key). A resume draws nothing new and cannot select outcomes. |
| C6 | In-run probe: none (execution), or present (authority) | **Present**, with the CPU projection `probe_cpu × total_paths ≤ max_cpu_seconds`. A refusal is INSUFFICIENT. | #581 A6 names the budget probe and its refusal. CPU makes the projection independent of shard count, and a dispatch gate bounds wall time. |
| C7 | Shard plan: signed into the authority (integrity), or a launch value | **A launch value**, recorded in the ledger | Results do not depend on W (test T11), and a resume may change W after a crash or a resource change. A resume on another machine is impossible anyway: the interpreter binding records an absolute `site_packages_path` (`p7_evidence.py:421`) and the private root is local. |
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
- **One consumer path, on a source built from the bound r3c receipt in a screen-bootstrap process:** `ProductionSource.screen_bracket(path, *, authority)` → `ScreenBracket` (a `BracketReplayResult` plus each run's deadline flag and consumed splits, §3.3), then `runner.evaluate_replay` on each run, then the A5 counting and A6 verdict functions. This is used **once**, for T00 step 3 under the ratified #581.
- The pre-ratification timing probes (§6) do not use the receipt. Ruling A4, and Joshua's answer for a second probe, are their authority.

**What it refuses, as a declaration** (enforced in §3.3 and §5):
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
4. **P7 output is never a screen input**, which is the 2026-09-30 spec's rule at `:358`. The screen consumes the P7 record only as an acceptance precondition (digest, `schema`, `contract_sha256`, `code_head`, `code_closure_sha256`, `bootstrap_sha256`, interpreter), never its result fields.
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
| `source.contract_sha256` | r3c digest | equals the **compiled** `T00_SCREEN_SOURCE_CONTRACT_SHA256` **and** the bound receipt's `contract_sha256` (`SCREEN_SOURCE_MISMATCH`). The digest binds r3c's 25 roles, so no separate role map is carried |
| `p7.record_sha256` | SHA-256 of the accepted P7 record's bytes | recomputed from the presented bytes; the record's `schema` equals `t00-p7-evidence/v1` (`p7_evidence.py:35`) and its `contract_sha256` (`p7_driver.py:76`) equals `source.contract_sha256` (`SCREEN_P7_MISMATCH`) |
| `p7.code_head` | 40-hex H | equals the record's `code_head` and the HEAD the validator reads itself, with a clean tree (§3.2) |
| `p7.code_closure_sha256`, `p7.bootstrap_sha256`, `p7.interpreter` | — | each equals the record's value; the interpreter the validator derives itself equals `p7.interpreter` |
| `prereg.path` | `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md` | exact |
| `prereg.commit` | the commit C′ whose blob is bound (§6 complete) | reachable from `origin/main`; `git diff C C′ -- <path>` changes only lines inside #581 §6 |
| `prereg.ratifying_commit` | C, the SHA written in #581 §6 | equals the §6 line; an ancestor of, or equal to, C′ |
| `prereg.blob_sha256` | SHA-256 of `git show C′:<path>` | recomputed; the Status line matches `RATIFIED \d{4}-\d{2}-\d{2}` (`SCREEN_PREREG_MISMATCH`) |
| `prereg.a5_text_sha256`, `prereg.a6_text_sha256` | section hashes (exact bytes between the A5/A6 headings and the next heading) | recomputed from the blob **and** equal to the compiled `A5_TEXT_SHA256` / `A6_TEXT_SHA256` in the verdict module (OD-5) |
| `a3_answers` | `[{path, commit, blob_sha256}]` for the two 2026-10-02 successor pre-registrations | each blob recomputes. In each blob, that successor's own §10 answerer-exposure regex (route-native successor `:155`, Vanguard successor `:187`) matches **exactly one line**, and no line beginning `\| ORB-3 ` or `\| VAN-3 ` contains `OWED` (`SCREEN_A3_UNANSWERED`). The Vanguard file has two `\| VAN-3` rows (`:98` answer, `:114` mapping), so a bare row-name check could pass with the answer still `OWED` |
| `parameters` | the closed set below | equals, byte for byte, the canonical JSON values block `t00-step2-values/v1` inside the ratified #581 §6 (OD-6) (`SCREEN_PARAMETER_UNSUPPORTED` / `SCREEN_PREREG_MISMATCH`) |
| `source_trust` | the pinned map | equals `_source_trust_document(SOURCE_SIGNING_KEYS)` (`contract.py:1037-1041`) |

**`parameters`** is a closed set. Each entry maps to a #581 §3 item; this design restates none of their values.

| Key | #581 item | Validation |
|---|---|---|
| `scenarios` | 7 | `["S0"]` only. r3c carries PRISTINE only (`contract.py:1156-1159`), and S1 needs a new source contract (OD-6) |
| `initial_state` | §2 A3 | equals `receipt.initial_state` |
| `horizon_sessions` | A6 ("within 1500 sessions") | equals the compiled `A6_HORIZON_SESSIONS` in the verdict module. The A6 section hash pins that text, and a test asserts the text contains the constant |
| `rng` | 4, A6 | `{tag:"t00-screen-rng/v1", roots:[3 distinct strings], probe_root}`. Joshua sets the three roots (item 4: "RNG root namespaces derived from seeds 42/123/2026") and `probe_root` (no #581 item; A6's probe "in its own RNG domain") as named values in the values block. `probe_root` differs from every root |
| `depth_per_root` | 1 | `{FULL,H1,H2}` → positive integers. Paths of the three roots pool per population, because A6 gates per population |
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
  - the key lifecycle check then runs (§3.2).
- **Scope exclusivity is already in the signed bytes** (`contract.py:389`):
  - a screen approval never verifies as a source contract (`SOURCE_SCOPE`, `:1189`), as `FREEZE_F1` (`:928`) or as a trust domain;
  - a source approval never verifies as a screen authority.
- **No path into qualification.** `source:` key IDs remain refused in qualification domains (`contract.py:1001-1005`; `trust_domain.py:318-319`). The authority never enters a `QualificationTrustDomain`.

### 3.2 Validator and receipt (OD-3)

New module `ops/c1_rail/qualification/screen_authority.py`. It **imports** the existing helpers in `contract.py` and edits none of them. The helpers are `_fields`, `_text`, `_receipt_snapshot`, `_pinned_source_keys`, `_source_trust_document`, `_check_source_key_lifecycle`, `verify_detached_approval`, `require_validated_source_contract` and `canonical_json_bytes`.

The validator's signature is `validate_screen_authority(authority_bytes, approval_bytes, public_keys, *, source_receipt, p7_record_bytes, artifact_root, now)`. **It takes no HEAD, tree, interpreter or reader argument.** It reads them itself from a fixed repository root, the checkout that holds the module (`Path(__file__).resolve().parents[3]`):
- `git rev-parse HEAD`, and `git status --porcelain --untracked-files=all`, which must print nothing;
- `p7_evidence.current_interpreter_binding(root)` (`p7_evidence.py:417-432`), through `_current_bytes_check` (`:451-455`);
- the pre-registration and A3 blobs, through module-internal `git show <commit>:<path>`.

`artifact_root` stays an argument, because `_current_bytes_check` re-hashes every artifact under it against the contract digests (`p7_evidence.py:446-450`). `now` stays an argument, as in every existing validator; `screen_bracket` re-checks with `_now()` on every call (§3.3), so a wrong `now` at launch cannot carry a run past expiry. Tests monkeypatch only the repository-root constant, as the 2026-09-30 tests monkeypatch only the pinned root.

It runs these steps in order, and each step has its own code:

1. Bytes, canonical round trip, closed fields, and exact schema, purpose, grants, refusals and evidence class (`SCREEN_AUTHORITY_FIELDS`).
2. `require_validated_source_contract(source_receipt, now=now)` (`contract.py:1229-1233`), then the source bindings (`SCREEN_SOURCE_MISMATCH`).
3. P7 bindings: the record hash, `p7_evidence.parse_record` (`:376`), the record's `schema` and `contract_sha256`, field equality, HEAD and a clean tree, and `_current_bytes_check` with the interpreter (`SCREEN_P7_MISMATCH`). There is no re-execution (C3).
4. Pre-registration bindings: the blob, Status, ancestry, the C→C′ diff, the A5 and A6 section hashes against the compiled constants, and the values block equal to `parameters` (`SCREEN_PREREG_MISMATCH`).
5. A3 (`SCREEN_A3_UNANSWERED`), as the §3 row states.
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

**P7 acceptance evidence.** `AcceptedP7Record` exists only in memory (`p7_evidence.py:436-441`, `:507`), and `fp.ps1 python` writes a `.cache/fp-verification` record only for pytest and `check` (`scripts/fp.py:241-254`). The coordinator therefore accepts through `t00_screen accept-p7`, which runs `accept_p7_record` and writes `p7_acceptance.json` (record SHA-256, `accepted_at`, HEAD, exit status) to the private root. The signing packet carries that file's SHA-256, and the attestation records it. The authority does not bind it: the validator could re-establish it only by a second P7 run (C3).

`require_validated_screen_authority(auth, *, source_contract, now)` runs on every use. Each failure has its own code:
- issued and unchanged;
- `auth.source_receipt is source_contract`, and the SHA-256 values are equal;
- the screen approval window and the pin lifecycle. It wraps `_check_source_key_lifecycle` and re-codes that function's `SOURCE_APPROVAL_EXPIRED` as `SCREEN_APPROVAL_EXPIRED`, so Joshua renews the right approval. The key codes stay `SOURCE_KEY_REMOVED` / `SOURCE_KEY_CHANGED` / `SOURCE_KEY_REVOKED`, because one key signs both approvals.

### 3.3 The one capability: `ProductionSource.screen_bracket`

```python
@dataclass(frozen=True)
class ScreenBracket:                         # screen_authority.py; model.py untouched
    bracket: BracketReplayResult             # r1, r2 (model.py:224-235)
    deadline_failure: tuple[bool, bool]      # per run: the `failed` flag (production_source.py:1229-1233)
    consumed_splits: tuple[tuple, tuple]     # per run: off-grid placements, derived as _seal does (:913-915)

def screen_bracket(self, path, *, authority):
    if not _is_source_only(self.contract):
        raise ValueError('SCREEN_REQUIRES_SOURCE_RECEIPT')
    from .screen_authority import ScreenBracket, require_validated_screen_authority   # lazy: P7 never loads it
    require_validated_screen_authority(authority, source_contract=self.contract, now=_now())
    results, failed, providers = self._bracket_results(path)
    return ScreenBracket(BracketReplayResult(*results), failed, tuple(_consumed_splits(p) for p in providers))
```

- **Refactor.** `replay_bracket`'s body (`production_source.py:1221-1234`) moves verbatim into `_bracket_results(path)`, which returns each run's result, `failed` flag and provider. The placement expression of `_seal` (`:913-915`) moves into `_consumed_splits(provider)`, which `_seal` then calls. `replay_bracket` keeps its exact outputs: sealed `SourceOnlyBracket` on r3c, `BracketReplayResult` on F1.
- **Why a wrapper.** A bare `BracketReplayResult` holds only the two `ReplayResult`s (`model.py:176-184`, `:224-235`). Without the flags, a short series could not be told apart from a confirmed deadline failure (A6), and #581 A5's consumed-split count could not be computed.
- **Every call is checked.** `_check_path` → `_verify_integrity` still runs, so the r3c lifecycle (`:1180-1182`) is re-checked per call, in addition to the screen-authority check.
- **Deadline handling.** A deadline failure becomes that run's result, exactly as in `replay_bracket` (`:1229-1236`). `BracketReplayResult.__post_init__` (`model.py:230-234`) enforces one fresh `ReplayResult` per run.
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
- the authority (§3.2), which itself reads HEAD, the clean tree (with `core.autocrlf=false`) and the interpreter, and checks the A3 blobs;
- the r3c validation, with its artifacts re-hashed through `ObservedBindings`.

A refusal at this stage is **LAUNCH_REFUSED**. No directory, replay or output exists, and nothing is consumed. Fixing the cause and relaunching is allowed.

**Freeze point.** The run directory `<private_root>/t00-step3/<authority_sha256>/` is created with O_EXCL. If it already exists:
- with a durable AUTHORITY_BOUND, the result is `SCREEN_ALREADY_RUN`, unless the call is a resume of a RESUMABLE run;
- without one (a crash between `mkdir` and AUTHORITY_BOUND), it holds no output, so `run` reuses it as a fresh start and records `DIR_REUSED`.

From the **first fsync'd path record**, step-3 output exists, and from then on #581 is frozen. A3 must already be bound.

### 4.2 Persistence (private root only; absolute path outside any worktree)

| File | Write discipline | Content |
|---|---|---|
| `lock` | held by the coordinator process (`msvcrt.locking`); each worker holds a per-shard lock | pid, host |
| `manifest.json` | temp file → fsync → `os.replace`, once, at PREPARED | the authority, r3c, P7-record and code-head digests; per population, the candidate block-start indices and `candidates_sha256`; plan digest (the SHA-256 of the sorted key universe) |
| `ledger/seg{k}.jsonl` | one file per coordinator segment; append + fsync, hash-chained, its first record chained to the previous file's last; never appended after its writer stops | AUTHORITY_BOUND, PREPARED, PROBE_START, PROBE{cpu, wall}, SEGMENT_START{k, W, assignment, witness keys, approval SHA-256s}, HEARTBEAT{wall, job CPU} every 60 s, WORKER_STOP{reason}, SEGMENT_END{state, wall, cpu, peak mem}, TERMINATION_ACT{act, approval SHA-256}, AGGREGATED, REPORTED, FINAL or TERMINAL_INSUFFICIENT{reasons} |
| `journal/seg{k}-w{i}-s{n}.jsonl` | one file per worker start, including a restart within a segment (`n` counts starts); append + fsync per record, hash-chained per file; never appended after its writer stops | key, seed, `path_sha256`, the path's `wall_s` and `cpu_s`, and per run: status, `sessions_to_pass`, failure reason, `kernel_outcome`, sessions replayed, `deadline_failure`, consumed-split count and SHA-256 (as `p7_driver.py:62-65`), `events_sha256`, run digest (the `p7_driver.py:55-59` projection). No P&L series |
| `results.json` | canonical JSON, atomic replace | a pure function of (authority SHA-256, r3c SHA-256, P7 record SHA-256, plan digest, sorted outcome multiset): A5 tallies under both assignments, the two #581 A5 descriptive counts per population (§5.5), the A6 verdict, labels. **No timestamps, W, approvals or timings** |
| `REPORT.md` | rendered from `results.json` only, by a fixed template | cites the SHA-256 of `results.json` |
| `attestation.json` | atomic | the SHA-256s of results, report, the ledger head and every journal head; the approval chain (every r3c and screen approval used); termination acts; segments; the per-shard loaded closure; the P7 acceptance-evidence SHA-256 |

### 4.3 Event sequences

**Happy path**

| Step | Event |
|---|---|
| 1 | Launch checks pass |
| 2 | Create the run directory with O_EXCL |
| 3 | AUTHORITY_BOUND |
| 4 | Candidate pass (§5.2); `manifest.json` written; PREPARED |
| 5 | PROBE_START; in-run probe (§5.4); PROBE |
| 6 | SEGMENT_START 1 |
| 7 | Workers append path records; the coordinator appends heartbeats |
| 8 | SEGMENT_END COMPLETE |
| 9 | `finalize`: coverage check, then AGGREGATED, then REPORTED |
| 10 | Console prints exactly `T00_SCREEN_VERDICT <label> results_sha256=<hex>`, then FINAL |

**Approval lapse**

| Step | Event |
|---|---|
| 1 | At the start of path p, `screen_bracket` refuses (`SOURCE_APPROVAL_EXPIRED` for r3c, `SCREEN_APPROVAL_EXPIRED` for the authority) |
| 2 | The worker writes WORKER_STOP(APPROVAL_LAPSE) and exits |
| 3 | The segment is RESUMABLE |
| 4 | Joshua signs a fresh approval over the **same** bytes. The subject digests are unchanged, so keys, seeds and outcomes are unchanged |
| 5 | `resume` re-runs the launch checks, then SEGMENT_START 2 |
| 6 | The resume witness passes, and the run continues |

Declining to renew is a termination act (§4.6).

**Context refusal**

| Step | Event |
|---|---|
| 1 | A worker raises `CONTEXT_REFUSAL` on key x |
| 2 | The coordinator stops all workers |
| 3 | TERMINAL_INSUFFICIENT{CONTEXT_REFUSAL, x} |
| 4 | `finalize` writes completed counts only, no rates (OD-7) |

### 4.4 Crash windows

| # | Window or event | Detection | Outcome |
|---|---|---|---|
| W0 | Crash before `manifest.json` is durable | no manifest | No output exists. Resume repeats PREPARED; the candidates are deterministic |
| W1 | Crash after the manifest, before any path record | no journal records | Resume behaves the same as a start |
| W2 | Worker lost mid-replay (killed, `MemoryError`, exit without WORKER_STOP) | no record for that key | RESUMABLE; the key is recomputed, identical by determinism. A key lost three times while the coordinator lived is TERMINAL `RESOURCE_EXHAUSTED` (§4.5) |
| W3 | Torn final line of a journal or ledger file | the last line fails parse or chain | Drop that tail only (TORN_TAIL); recompute the key. A break anywhere else, or a record appended after a torn line, is TERMINAL `CORRUPTION` |
| W4 | A durable record exists and the key is recomputed after resume | duplicate key | Identical projection: deduplicate. Different projection: TERMINAL `NONDETERMINISM` |
| W5 | Resume witness | SEGMENT_START assigns each worker one witness key: the last W′ completed keys in canonical order, one each. Each worker recomputes its witness first | Mismatch: TERMINAL `NONDETERMINISM` |
| W6 | Crash during aggregation, report or attestation | missing or temp files | Re-run `finalize`; the outputs are byte-identical |
| W7 | Crash after REPORTED, before FINAL | the ledger lacks FINAL | `finalize` re-verifies the digests and appends FINAL idempotently |
| W8 | Approval lapse (source or screen) | refusal at a path start or in the candidate pass, before any engine runs. A path started inside the window completes (`_check_path`, `production_source.py:1193-1194`) | STOP, RESUMABLE (§4.3). Only Joshua's signed termination act ends it as INSUFFICIENT `APPROVAL_LAPSE_UNRENEWED` (§4.6) |
| W9 | Wall or CPU budget exhausted with keys left | dispatch gate (§5.4) | TERMINAL `BUDGET_EXHAUSTED` |
| W10 | `ReplayNeedsContext`, a shape-check failure (§5.3), or a key lifecycle event (`SOURCE_KEY_*`) | worker exception (§4.5) | Fail fast; TERMINAL `CONTEXT_REFUSAL`, `INTRADAY_LOW_MISSING` or `SOURCE_KEY_LIFECYCLE`, with the key |
| W11 | Head, tree, interpreter or P7 binding drift between segments | SEGMENT_START repeats the launch checks | TERMINAL `CODE_OR_ARTIFACT_DRIFT` |
| W12 | Private artifact bytes change | `ObservedBindings` refusal (`contract.py:1110-1112`) or `_verify_integrity` | TERMINAL `CODE_OR_ARTIFACT_DRIFT` at a segment start; `UNCLASSIFIED_ERROR` mid-run (§4.5) |
| W13 | Disk full, or an antivirus lock on a journal file | write failure | Worker stops; RESUMABLE |
| W14 | A second coordinator starts, or `resume` runs while any lock is held | lock held | Refused (`SCREEN_WORKERS_ALIVE`); the existing run is unaffected |
| W15 | Operator interrupt (Ctrl-C) | signal | RESUMABLE. The Job Object kills every worker with the coordinator (§5.1) |
| W16 | `abandon` | Joshua's signed termination act (§4.6) | TERMINAL `ABANDONED`; it can never become GO |
| W17 | A record for a key outside the plan, or outside that shard's assignment | aggregation | TERMINAL `CORRUPTION` |
| W18 | Machine sleep or hibernation | wall budget counts only active segment time; a sleep-spanning segment counts in full | Disable sleep for the run. Monotonic-clock behaviour across sleep is pinned in a test |
| W19 | In-run probe ends in a deadline failure, cannot complete, or projects over `max_cpu_seconds` | probe step | TERMINAL INSUFFICIENT (#581 A6 budget-probe clause) |
| W20 | Candidate pass: an empty population, an empty candidate set, or a proof-path deadline failure | PREPARED step | TERMINAL INSUFFICIENT `CANDIDATES_UNAVAILABLE` (OD-6). An approval expiry here is W8, never W20 |
| W21 | PROBE_START without PROBE at resume | ledger | TERMINAL INSUFFICIENT `PROBE_INTERRUPTED`; the probe timing is never re-rolled |
| W22 | Coordinator killed hard | a segment without SEGMENT_END | RESUMABLE. The Job Object has killed every worker; the segment is charged its last HEARTBEAT plus one interval (§5.4) |

### 4.5 Exception classification (closed)

A worker classifies every exception by its type and the code its message leads with (`ContractValidationError` messages lead with their code, for example `contract.py:1054`).

| Raised | Window | Outcome |
|---|---|---|
| `SOURCE_APPROVAL_EXPIRED` or `SCREEN_APPROVAL_EXPIRED`, at a path start or in the candidate pass | W8 | RESUMABLE on renewal |
| `SOURCE_KEY_REVOKED`, `SOURCE_KEY_CHANGED` or `SOURCE_KEY_REMOVED` (`contract.py:1055-1062`), at any time | W10 | TERMINAL `SOURCE_KEY_LIFECYCLE`. No renewal exists without a new pinned root, which means a new H |
| `ReplayNeedsContext`; a shape-check failure; a missing or invalid `intraday_low` | W10 | TERMINAL `CONTEXT_REFUSAL` / `INTRADAY_LOW_MISSING` |
| `OSError` writing a journal or ledger file | W13 | RESUMABLE |
| `MemoryError`, or a worker exit without WORKER_STOP while the coordinator lives | W2 | RESUMABLE at most twice per key; the third is TERMINAL `RESOURCE_EXHAUSTED` |
| `KeyboardInterrupt` | W15 | RESUMABLE |
| Anything else, including the uncoded integrity refusals of `_verify_integrity` (`production_source.py:1171-1178`) | — | TERMINAL `UNCLASSIFIED_ERROR` |

Every TERMINAL row ends INSUFFICIENT. A misattributed terminal code changes the reason text only, never the outcome. No deterministic failure can resume indefinitely.

### 4.6 Termination acts and re-attempts (OD-8)

Journals are readable in the private root before `finalize`. Ending a run early turns a trending NO-GO into INSUFFICIENT, which anyone who wants to proceed prefers. So:
- **`abandon`, and `finalize` over an unrenewed approval lapse, are Joshua's acts only.** Each needs a termination act: canonical `t00_screen_termination/v1` `{authority_sha256, act: ABANDON | DECLINE_RENEWAL, statement, readers: [{name, exposure: seen | not seen}]}`, signed by the pinned key under its own scope `APPROVE_T00_SCREEN_TERMINATION`, so it never verifies as an authority, source contract or freeze. `readers` lists everyone who read any journal row before the act. The ledger and attestation record it. Agents never invoke these acts.
- **After any TERMINAL INSUFFICIENT, a re-attempt needs a new #581 ratification** that discloses the journal exposure. That gives a new authority SHA-256 and a new run directory. The terminal run directory is kept.

---

## 5. Driver

### 5.1 Process topology (local machine only; private data never leaves it)

**Coordinator.** `fp.ps1 python -m c1_rail.qualification.t00_screen {preflight|accept-p7|run|resume|finalize|verify|abandon} <args>`.

**Workers.**
- Each worker is a child process `sys.executable -I -S -B -c SCREEN_BOOTSTRAP`, generated from the shared bootstrap template (C8). It records an audit hook and a recording finder, as P7 does (`p7_evidence.py:57-339`).
- The environment is pinned: `PYTHONHASHSEED=0`, and `OMP_NUM_THREADS`, `MKL_NUM_THREADS` and `OPENBLAS_NUM_THREADS` all `=1`.
- Workers run in a Windows Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, created by the coordinator through `ctypes`. When the coordinator's handle closes, including by its death, every worker dies. A separate process group does not stop orphans on Windows. The job's accounted CPU includes workers that have exited (§5.4).
- Workers pickle nothing. **Every worker validates r3c and the authority and builds its own `ProductionSource`**, because receipts and sources are registered per process (`contract.py:1211-1215`; `production_source.py:1160-1164`).

**Screen forbidden modules:**
- `production`, `orchestration`, `result_adjudication`, `seal`, `execution.*`, `part_a`, `benchmark*`, `p7_driver`.
- The screen **stubs** `runner._run_stage` and `runner.run_synthetic_stage`.
- `evaluate_replay`, `simulate_path` and `bracket` load **live**.

**P7 forbidden modules gain** `c1_rail.qualification.screen_authority` and `c1_rail.qualification.t00_screen*`, so P7 can never reach the screen.

### 5.2 Candidate pass (PREPARED; §3 item 4 convention, OD-6)

The pass runs once, in one screen-bootstrap worker before PREPARED. For each population pool, in `partition_populations` order (`blocks.py:35-38`):
1. Assemble the chronological path, as `proof` does at `production_source.py:1268`.
2. Run `screen_bracket` on it.
3. Derive each run's edges as `proof` does (`:1282-1291`), and the joins from `self.adjacent`.
4. Compute `JointFlatBlocks(pool, edges_r, L, joins).candidates()` (`blocks.py:28-32`) for R1 and for R2. The candidates are their **intersection**.
5. Treat any of the following as `CANDIDATES_UNAVAILABLE`, mirroring `provider.py:36-54`:
   - `deadline_failure` in either run (§3.3);
   - a run shorter than the pool;
   - discontinuous edges;
   - an empty candidate set.

The manifest stores each population's candidate block-start indices and `candidates_sha256`. Each worker rebuilds the candidate tuples from those indices and its own source's sessions, and checks the digest.

`proof` is not used. Its single-run provider refuses unreviewed instants (§1), and its sealed output on r3c holds edges only after a single run.

### 5.3 Per path

```
for key in assigned_keys - completed_keys (ascending canonical order):
    budget.dispatch_gate()                                            # §5.4
    seed = int.from_bytes(sha256(canonical(["t00-screen-rng/v1", purpose, root, population, path_index]))[:8], "big")
    path = PathAssembler(path_start_date).sample(candidates[population], Random(seed), horizon_sessions=H)   # paths.py:44-51
    s = source.screen_bracket(path, authority=auth)                   # both lifecycles re-checked here
    for run, failed in zip((s.bracket.r1, s.bracket.r2), s.deadline_failure):
        shape_check(run, failed, path); outcome = evaluate_replay(run, initial_state=initial)   # runner.py:20-44
    append_record(key, seed, path_sha256, outcomes, s.consumed_splits, status)   # status: the BracketVerdict rule, bracket.py:95-112; fsync
```

**Seeds.**
- Seeds are separate from the qualification streams (`'tb-s2-rng-v2'`, `regime.py:22`).
- They do not reuse `regime.domain_seed`, whose stage set is qualification-only (`regime.py:12`).
- They depend on neither the authority digest nor W.

**`shape_check`** mirrors `provider.py:76-83` and #581 A6, using the run's own `deadline_failure` flag from `ScreenBracket`. Each run must satisfy **one** of these:
- `failed` is false, and the run has length H;
- `failed` is true, with `0 < len ≤ H`, where the last row is not flat-before-deadline and every earlier row is.

In both cases two more conditions hold:
- every `intraday_low` is finite and ≤ 0, with one per replayed session;
- `occurrence` and `source_session_id` equal the path prefix.

Anything else is `CONTEXT_REFUSAL`, or `INTRADAY_LOW_MISSING` for the low check. A series that ends short without the flag is therefore INSUFFICIENT, never scored (A6).

**`initial`** is `EvaluationState` built from `receipt.initial_state`, as `production_source.py:1259-1261` does.

### 5.4 Budget (OD-7)

- **In-run probe.** PROBE_START is fsync'd first. Then one path from `probe_root`, population FULL, index 0, is timed for wall and CPU, and PROBE is written. The CPU projection rule is `probe_cpu × total_paths ≤ max_cpu_seconds`. A probe that ends in a deadline failure or cannot complete is INSUFFICIENT (#581 A6), and an interrupted probe is never re-run (W21). The probe is not scored and is not in the tallies.
- **Wall** is cumulative active time across segments, on the coordinator's monotonic clock from SEGMENT_START to SEGMENT_END. **CPU** is the Job Object's accounted user and kernel time at SEGMENT_END, summed across segments.
- **Crash charging.** A segment without SEGMENT_END is charged its last HEARTBEAT plus one interval of wall, and that HEARTBEAT's job CPU plus one interval × W. A crash can only overcharge.
- **Dispatch gate.** No path starts after either budget is used up. Exhaustion with keys remaining is TERMINAL `BUDGET_EXHAUSTED`.
- **Overrun on the final path.** If every key completes and only the last path overran, the run is scored and the overrun is recorded descriptively. #581 A6 makes a budget stop INSUFFICIENT "before every population reaches its frozen depth", and this reading follows that text. It knowingly differs from `runner.py:120-122`. Strict parity is the alternative at OD-7.

### 5.5 Finalize (pure functions; no I/O inside the verdict)

**Coverage.** Every `(root, population, path_index)` must occur exactly once. Bindings and candidate digests must be identical across shards. A gap, a duplicate or a mismatch is TERMINAL INSUFFICIENT.

**A5 and A6.** `t00_screen_verdict.py` implements #581 A5 (1)–(3) and A6 **by reference to those sections**, with exact integer comparisons (`20·bust ≤ n`, `2·pass ≥ n`). Paths of the three roots pool per population. It takes:
- input: outcome rows, `parameters` and the insufficiency reasons;
- output: `INSUFFICIENT(reasons)`, `GO-evidence`, or `NO-GO-evidence{robust | UNDETERMINED-dependent}`.

**A5 descriptive counts.** With the verdict, `results.json` carries, per population, the count of paths with a consumed split (in either run) and the count of `UNDETERMINED` paths. They have no verdict role.

When any insufficiency reason exists, the function is never handed tallies, and a report shows completed counts only (OD-7). The hybrid is a labelled diagnostic only.

**Mapping of the #581 A6 triggers to screen codes.** The A6 text is left verbatim.

| #581 A6 trigger | Screen code / where enforced |
|---|---|
| `ReplayNeedsContext`, a source refusal, or a short series without a confirmed deadline failure | `CONTEXT_REFUSAL` (§5.3 with the `deadline_failure` flag, W10); `SOURCE_KEY_LIFECYCLE` (W10) |
| A run lacks its own synchronized `intraday_low` | `INTRADAY_LOW_MISSING` (§5.3) |
| P7 is not accepted for A1's identities at the executing head | LAUNCH_REFUSED before any output; `CODE_OR_ARTIFACT_DRIFT` mid-run (W11) |
| The runner raises `NeedsContext` (budget, a missing prerequisite, or a probe that cannot complete) before full depth | `BUDGET_EXHAUSTED` (W9); probe refusal (W19, W21); `CANDIDATES_UNAVAILABLE` (W20); `APPROVAL_LAPSE_UNRENEWED` (W8); `ABANDONED` (W16); `RESOURCE_EXHAUSTED`, `UNCLASSIFIED_ERROR` (§4.5) |
| Any §3 item is unset | The authority cannot validate (§3), so the screen cannot launch |
| A confirmed own-flat deadline failure on a scored path | A scored outcome, never INSUFFICIENT (§5.3 shape rule) |

### 5.6 Console, access and coordinator acceptance (OD-11)

**Console output.**
- stdout is exactly one line: `T00_SCREEN_VERDICT <GO-evidence|NO-GO-evidence-robust|NO-GO-evidence-UNDETERMINED-dependent|INSUFFICIENT> results_sha256=<hex>`.
- stderr carries refusal codes and shard-done markers only.
- No count or rate appears on any console, in CI or in a PR.

**`verify` subcommand** (the coordinator seat):
1. Re-validate offline the authority, the approvals and r3c.
2. Check the console digest against `sha256(results.json)`, the journal and ledger hash chains, and coverage.
3. Recompute the label with a **coordinator-written script that does not import `t00_screen_verdict`**, working from the ratified #581 A5/A6 text. The script is committed and reviewed before Joshua signs (§8 step 10); one written after the label prints is not independent.
4. Re-execute k paths whose indices are derived from `sha256(results.json)`, and compare their rows byte for byte. This needs unexpired r3c and screen approvals.

The result is VERIFIED or REFUTED. Under an expired approval, `verify` stops with `VERIFY_BLOCKED_APPROVAL_EXPIRED`, which is neither; the label stays unaccepted until Joshua renews.

**Public reporting.** Only the label is public. A public figure may only cite the private RESULTS path (`load_bearing_numbers.md` §1).

---

## 6. Timing probes (ruling A4)

**Recorded fact: the A4 probe was a timed P7 re-run.** Under ruling A4, the coordinator re-ran P7 at `origin/main@d716106` under r3c / r3c-a2 on 2026-10-03, with timing. The record (SHA-256 `6718b665900ee0d43a80544913cd5a2f35d533d059c9e5e20ea35329b5a4565d`) was ACCEPTED: closure `48bdc104…9139` MATCH, and the R1 and R2 digests MATCH. As a re-run of the path P7 had already run, it exposed no outcome beyond the record already accepted. It is not A1 step 5, which re-runs P7 at H after the build (§8).

| Measure | Value |
|---|---|
| P7 wall, 80 session-replays (2 runs × 40 sessions) | 352.6 s |
| Acceptance re-execution | 316.8 s wall, 279.2 s CPU, single-threaded |
| Peak memory | 564 MiB |
| Implied cost per session-replay | about 4 s, fixed overhead not separated |
| Host | 8 logical cores |

**Consequence.** If about 4 s is the true per-session cost, one path (2 runs × 1500 sessions) costs about 3.3 CPU hours. The prereg-v2 reading (about 90k paths, §7) would then need about 34 CPU-years, which is infeasible. One week on 8 cores at full efficiency fits that depth only at about 18 ms per session-replay. Most of the 4 s is probably fixed overhead: process start, source validation and build, the retained-bytes rehash and two engine builds. One window length cannot separate the two.

**Second probe (pending Joshua's answer).** The coordinator has asked Joshua whether a second timing probe may run, reporting wall and CPU only, to separate fixed from per-session cost. If he allows it, its form is:
1. The sealed `replay_bracket`, as the P7 driver calls it (`p7_driver.py:48`), on the path P7 already ran, at two window lengths within it. Both windows start at that path's first session, so every session replayed is one whose outcome P7 already exposed.
2. `simulate_path` on synthetic zero series of length 1500, in a separate process that builds no source and reads no private data.
3. Output: wall and CPU per window and for the kernel. There are no fills, labels, deadline flags or replayed-session counts, and stderr is limited to refusal codes. Any record the launcher writes stays in the private root, and its outcome fields are not read.

Before ratification, no probe replays the FULL chronological path or any path P7 has not run. That timing would show almost exactly whether a run was cut short by a deadline, which is W20's trigger and #581 §3 item 3's subject.

**Use.** From windows n₁ < n₂ sessions with times t₁ and t₂, the per-session-replay cost is c = (t₂ − t₁) / (2(n₂ − n₁)), and the intercept is F = t₁ − 2n₁c. F also contains the once-per-process build, so it bounds the per-path fixed cost from above. The projected cost per path is F + 2·1500·c + 2 × kernel. If Joshua declines the second probe, about 4 s per session-replay serves as the upper bound.

The coordinator tabulates, for candidate depths, the projected CPU hours and wall days at W workers (W ≤ 8, and W × 564 MiB ≤ 0.8 × RAM) against the approval windows. Joshua sets #581 §3 item 1 and decides compute location and duration (OD-9) from that table. Any reduction of depth happens here, before ratification, never after (#581 A6).

---

## 7. Sharding and compute

- **Key universe.** `K = {(root, population, path_index) : path_index < depth_per_root[population]}`, sorted canonically. The plan digest is the SHA-256 of that list.
- **Assignment.** Round-robin by ordinal mod W, so every shard gets a mix of populations. A resume may change W: the coordinator re-partitions `K − completed` among W′ workers, and SEGMENT_START records the assignment and witness keys.
- **Determinism.** Each outcome is a pure function of (receipt bytes, authority bytes, key). Every `screen_bracket` builds fresh engines (`production_source.py:1239-1263`), and no process-global cache selects a replay. Test T11 shows that W=1 and W=4 give identical `results.json` bytes.
- **Scale.** The prereg v2 reading of 10k × 3 roots × 3 populations is about 90k paths, each with 2 runs of 1500 sessions. At the A4 upper bound that is about 34 CPU-years (§6), so the depth is set from the §6 table.
- **Where it runs.** On the operator's local machine only. r3c's inputs include the accepted runtime ports, which may not leave the operator's primary checkout or go to any external service (AGENTS.md, private read surface), and the private root is local. So there is no cloud and no GLM. The options are a dedicated local run of N days with sleep disabled, or a reduced depth (OD-9).
- **Per-path integrity cost.** `_verify_integrity` rehashes the retained bytes on every call (`production_source.py:1179`). It is part of the fixed cost the second probe would bound.

---

## 8. Sequencing with #611 and P7

Every build PR must land **before** H. P7 acceptance is tied to its exact head: `code_head` is in the record and is not a volatile field (`p7_evidence.py:38`), so a record presented at any other head fails as `P7_RECORD_NOT_REPRODUCED`. Step 3 then runs from a detached worktree at H, and later commits on `main`, including ratification, do not affect it. The A4 timed P7 re-run at `d716106` (§6) is not step 7.

| # | Step | Seat | Gate |
|---|---|---|---|
| 0 | A3: ORB-3 and VAN-3 answered, with exposure markers (standing) | Joshua | Before any step-3 output |
| 1 | Lift the #611 and A9-PREP holds; merge #611 (`production_source.py`) | coordinator / Joshua | — |
| 2 | Coordinator review → one narrow Codex review → **Joshua approves this design and the §12 decisions** | Joshua | No code before this |
| 3 | Settle #581 §3 item 8 and the A5/A6 text; merge #581 as DRAFT with A5/A6 frozen. **This amends A1's order** (OD-5) | Joshua | Before the build, because the verdict code pins the section hashes |
| 4 | Spec-amendment docs PR (§11), A10b reasons, #581 §5 item 3 wording | CC | — |
| 5 | Build packets (§9.1), red-first, rebased on #611 | see §9.1 | Every packet merged → **H** |
| 6 | Joshua signs a **fresh r3c approval** whose window covers steps 7–12 (OD-10) | Joshua | — |
| 7 | **One P7 re-run** at H (A1 step 5); coordinator `t00_screen accept-p7` → record R and `p7_acceptance.json` | executor / coordinator | Closure covers `production_source.py` and `p7_evidence.py` |
| 8 | Depth and budget table (§6), from the A4 facts and the second probe if Joshua allows it; Joshua decides compute location and duration (OD-9) | coordinator / Joshua | The second probe may run any time before this step, under any valid r3c approval |
| 9 | Set and ratify #581 §3, including the `t00-step2-values/v1` block → C, C′ (C′ changes only lines inside §6) | Joshua | — |
| 10 | Commit and review the coordinator's independent label script (§5.6) | coordinator | Before step 11 |
| 11 | Signing packet: authority bytes, SHA-256, every binding listed, key fingerprint, the `p7_acceptance.json` SHA-256, and a statement that ratification left the A5/A6 bytes untouched; coordinator reviews; **Joshua signs `APPROVE_T00_SCREEN_AUTHORITY`** | Joshua | — |
| 12 | Step 3, once: `run` → `finalize` → `verify` | executor / coordinator | Label recorded at the T00 owner |

---

## 9. Files (admitted only by a later build card)

| File | Change | In the P7 closure? |
|---|---|---|
| `ops/c1_rail/qualification/screen_authority.py` (new) | Schema constants, compiled r3c digest, validator, receipt, registry, `require_validated_screen_authority`, `ScreenBracket`, termination-act validator | No (forbidden in P7) |
| `ops/c1_rail/qualification/t00_screen_plan.py` (new) | Key universe, seeds, candidate pass, shape check, shard assignment | No |
| `ops/c1_rail/qualification/t00_screen_verdict.py` (new) | A5/A6 pure functions; `A5_TEXT_SHA256` / `A6_TEXT_SHA256` / `A6_HORIZON_SESSIONS` | No |
| `ops/c1_rail/qualification/t00_screen_journal.py` (new) | Ledger, journal, manifest, results, attestation writers; torn-tail and chain rules | No |
| `ops/c1_rail/qualification/t00_screen.py` (new) | CLI; launch checks; `accept-p7`; coordinator (Job Object, heartbeats), worker, finalize, verify, termination acts | No |
| `ops/c1_rail/qualification/production_source.py` | `screen_bracket`, plus the verbatim `_bracket_results` and `_consumed_splits` refactor | **Yes** (covered by the planned re-run) |
| `ops/c1_rail/qualification/p7_evidence.py` | Bootstrap template parametrization; forbidden-list additions | **Yes** (covered by the planned re-run) |
| `scripts/t00_screen_label_check.py` (new) | The coordinator's independent label recompute; imports nothing from `t00_screen_verdict` | No |
| `tests/ops/qualification/test_source_consumers.py` | Scan widening and allowlist entries (OD-1) | — |
| `tests/ops/qualification/test_screen_authority.py`, `test_t00_screen_plan.py`, `test_t00_screen_verdict.py`, `test_t00_screen_journal.py`, `test_t00_screen_driver.py` (new); `test_production_source.py`, the P7 tests | §10 | — |
| `docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md` | §11 dated addendum (separate docs PR) | — |
| #581 pre-registration | §5 item 3 names this authority; §6 values block | — |

**Forbidden:** `contract.py`, `trust_domain.py`, `book_adapters.py`, `runner.py`, `provider.py`, `blocks.py`, `paths.py`, `regime.py`, `bracket.py`, `model.py`, `replay.py`, `book_policy.py`, `core/` (including `dd_protection.py` and `mc/`), and any Pine, port or private artifact. Also forbidden are any edit to r3c's bytes or the pinned key, and any test that reads the real source.

### 9.1 Build packets (parallel against frozen interfaces)

| Packet | Scope | Depends on | Route |
|---|---|---|---|
| P-A | `screen_authority.py`, T1–T7, T15 (termination-act validator) | — | CC solo (trust/auth: never GLM) |
| P-B | `screen_bracket` + refactor; bootstrap parametrization + forbidden lists; A10b widening; T8–T10 | #611 merged | CC solo (P7 closure, security) |
| P-C | `t00_screen_verdict.py`, T12–T13 (synthetic rows only) | — | GLM-eligible: worktree `workdir`, no private data |
| P-D | `t00_screen_journal.py`, T14, T17–T18 (fake source) | — | GLM- or Cursor-eligible |
| P-E | `t00_screen_plan.py`, T11, T19 | P-B interface | Cursor or CC |
| P-F | `t00_screen.py` integration, `accept-p7`, Job Object, in-run probe, T16, T20–T23 | P-A to P-E | CC integration |

---

## 10. Tests (red-first; each negative asserts its own code and has a passing twin)

The 2026-09-30 attribution rule applies. Tests use TEST_ONLY keys generated in-process, with only the pinned root and the validator's repository-root constant monkeypatched, and synthetic fixtures. **No test reads the real source.**

| ID | Test | Falsifier |
|---|---|---|
| T1 | Canonical round trip and closed fields; each F1 field, each r3c-only field, the r3c approval digest, a role map, a seed-pooling field, a shard count or an expiry in the doc is refused | Any variant validates |
| T2 | Scope exclusivity: a source-scope approval over the authority digest is refused; a screen approval is refused by `validate_source_contract`, `validate_frozen_contract` and the trust-domain validator; a termination approval never validates as an authority, and the reverse | A cross-scope signature verifies |
| T3 | Signer: TEST_ONLY, non-`source:`, unpinned, self-signed with a matching self-registry, revoked, expired or fingerprint-changed are each refused | Any verifies |
| T4 | `screen_bracket` refuses with no authority, a foreign authority, an authority bound to another receipt object (same SHA-256, different object), or on an F1 source. A spy shows `_engine` is never called | A mismatched source replays |
| T5 | P7 binding: record hash, `schema` ≠ `t00-p7-evidence/v1`, `contract_sha256` ≠ r3c's, `code_head` ≠ HEAD, a dirty tree (including an untracked file), interpreter, or a closure file changed (`_current_bytes_check`) are each refused. The validator has no HEAD, tree or interpreter parameter; a hand-built `AcceptedP7Record` is never an input | A stale, foreign or forged P7 binds, or a caller value overrides HEAD |
| T6 | Pre-registration: Status not RATIFIED, blob hash, ancestry, a C→C′ diff outside §6, values block ≠ `parameters`, A5/A6 hash ≠ compiled, or `horizon_sessions` ≠ `A6_HORIZON_SESSIONS` are each refused. A3: zero or two §10 regex matches, or any `\| VAN-3` / `\| ORB-3` line containing `OWED` (fixture: the mapping row carries a marker while the answer row is `OWED`) is refused | An unratified or edited prereg, or an unanswered A3, binds |
| T7 | Lifecycle: a mutated or lookalike authority is refused; expiry of the screen or r3c approval between calls refuses the next `screen_bracket`, with `SCREEN_APPROVAL_EXPIRED` and `SOURCE_APPROVAL_EXPIRED` respectively; a renewal over the same bytes passes | A replay runs expired, renewal changes results, or the wrong approval is named |
| T8 | Fence intact: with a valid authority, `replay`, `replay_bracket` and `proof` still return `SourceOnly*`; `verify_for` still raises; the A10 consumers still refuse; `replay_bracket` outputs are byte-identical before and after the refactor; on the same fake path, `ScreenBracket.deadline_failure` and `consumed_splits` equal the sealed runs' `deadline_failure` and `consumed_intrabar_splits` | Any fenced path opens, or the wrapper's flags diverge from the sealed ones |
| T9 | A10b: calls and attribute loads of `screen_bracket`, `_bracket_results`, `_replay_raw` and `_engine` are flagged; a planted consumer in `ops/`, `scripts/` or `tools/` fails the scan | An unlisted consumer passes |
| T10 | P7 refuses to import `screen_authority` and `t00_screen*` (`P7_FORBIDDEN_IMPORT`); the screen refuses `production`, `execution`, `seal` and `p7_driver`, and the stubbed `_run_stage`; existing A16–A23 stay green on the template-generated P7 bootstrap | A cross-process reach succeeds, or P7 behaviour changes |
| T11 | Determinism: W=1 and W=4, and an uninterrupted run against a three-segment run, give byte-identical `results.json`; screen seeds never equal `domain_seed` for the same indices | Results depend on W or segmentation, or streams collide |
| T12 | A5: every (1) row, every (2) agreed rule and every (3) assignment, under both item-3 values; `UNDETERMINED` always stays in the denominator; boundaries at exactly 5% and 50%; the median with even n and ∞ | Any misclassification |
| T13 | A6: GO, NO-GO robust and NO-GO `UNDETERMINED`-dependent; every INSUFFICIENT trigger in the §5.5 mapping; tallies are never read when a reason exists; the halves toggle; the two A5 descriptive counts per population | Any trigger yields GO or NO-GO |
| T14 | Journal and ledger: a torn tail in any file is dropped; a break mid-file, or a record after a torn line, is refused; an identical duplicate is deduplicated; a divergent duplicate is `NONDETERMINISM`; a key outside the plan or the shard is `CORRUPTION` | A corrupted journal aggregates |
| T15 | Single use and termination: a second launch is `SCREEN_ALREADY_RUN`; a launch refusal leaves no directory; a directory without AUTHORITY_BOUND is reused as a fresh start; `abandon`, or `finalize` over an unrenewed lapse, without a valid signed termination act is refused; neither can yield GO | Re-draws are possible, or an unsigned act ends a run |
| T16 | In-run probe: PROBE_START precedes the timing; PROBE_START without PROBE at resume is `PROBE_INTERRUPTED`; the probe path is never scored | The probe timing is re-rolled or scored |
| T17 | Crash windows W0–W8, W13–W16, W21 and W22 with real subprocess workers and a deterministic fake source, injected only through a TEST_ONLY seam: final bytes equal the uninterrupted run's; killing the coordinator kills every worker; `resume` refuses while any lock is held | Any window changes the result, or a worker survives its coordinator |
| T18 | Budget: the gate stops new paths; budget accumulates across segments, including exited workers' CPU; an unterminated segment is charged its last heartbeat plus one interval; exhaustion is INSUFFICIENT; a final-path overrun follows OD-7; a probe projection over budget is INSUFFICIENT | A budget breach yields a verdict, or a crash lowers the charge |
| T19 | Candidates: intersection across both runs; a proof-path deadline (by flag), discontinuity or empty set is `CANDIDATES_UNAVAILABLE`; `horizon % L` is enforced; workers rebuild candidates from the manifest's indices and match `candidates_sha256` | A one-run-flat block is sampled |
| T20 | Shape check: a short run without `deadline_failure`, `intraday_low > 0`, a NaN low or a prefix mismatch each refuses with its own code; a deadline run with earlier rows flat is scored | A malformed run is scored |
| T21 | Console: stdout matches `^T00_SCREEN_VERDICT (labels) results_sha256=[0-9a-f]{64}$` exactly | Any count reaches the console |
| T22 | `verify`: a changed row is caught by the hash-derived re-execution sample; the label recompute disagrees on a planted verdict bug; an expired approval gives `VERIFY_BLOCKED_APPROVAL_EXPIRED` | A tampered result verifies, or an expired run verifies |
| T23 | Exception table (§4.5): each row's exception reaches its window; an unlisted exception is `UNCLASSIFIED_ERROR`; a third loss of one key is `RESOURCE_EXHAUSTED`; a key revocation is never RESUMABLE | An exception resumes outside the table, or a deterministic failure resumes forever |

**Regression:** A1–A23 of the 2026-09-30 spec, the full `tests/ops/qualification` suite, `tests/ops/test_book_adapters_parity.py`, and `fp.ps1 check`, each with its cited `.cache/fp-verification` record.

---

## 11. Proposed dated addendum to the 2026-09-30 spec (A2; not edited in this PR)

**At `:124`, appended after the existing paragraph:**
> *Addendum 2026-10-0X (operator ruling A2, 2026-10-02).* The receipt itself still authorizes only the path above, and its `refusals` are unchanged. A source built from it may additionally serve `ProductionSource.screen_bracket`, and only that method, while a validator-issued `ValidatedScreenAuthority` binds this receipt object and its exact `contract_sha256`. That authority has schema `t00_screen_authority/v1` and scope `APPROVE_T00_SCREEN_AUTHORITY` ([T00 screen-authority design](2026-10-02-t00-screen-authority-design.md)). The authority, not this receipt, authorizes the T00 step-3 screen and its kernel calls, inside the screen bootstrap process only. `verify_for` still refuses the source for every qualification consumer, and `replay`, `replay_bracket` and `proof` still return sealed types. Without a screen authority, every statement in this section holds unchanged.

**At `:358`, appended after the procedural rule:**
> *Addendum 2026-10-0X (operator ruling A2).* The rule is unchanged: no P7 record, P7 worksheet or `SourceOnly*` value is ever a screen input. A T00 step-3 run under a signed screen authority builds its own `ProductionSource` from the r3c receipt, in its own process, and obtains `BracketReplayResult`s only through `screen_bracket`. Those are screen outputs, not P7 output. The screen consumes the P7 record only as an acceptance precondition (its digest, `schema`, `contract_sha256`, `code_head`, `code_closure_sha256`, `bootstrap_sha256` and interpreter), never its result fields. Pre-ratification timing probes (ruling A4) run only on the path P7 already ran and report wall and CPU time only.

**Consequential edits:**
- `:159`: "generated only for source contracts" becomes "generated only for source contracts and T00 screen authorities".
- `:342`: the superseded dominance description becomes a pointer to the deny-by-default scan (Status line) and its §9 widening.

---

## 12. Operator decisions at approval

Answer "all recommended except …".

1. **Design core** (§3, §3.3, §5.1, §9): the authority class, one gated `screen_bracket` scored by the unchanged `evaluate_replay`, one parametrized bootstrap template, the A10b widening. *Recommend: adopt.* (Alternative: a duplicate scorer, which makes #581 A4's wording false.)
2. **Signing key.** *Recommend: reuse `source:1ebae5d45bc51280` under the two new scopes;* scope separation is in the signed bytes. (Alternative: a dedicated `screen:` key, with a second ceremony and edits at `contract.py:1001-1005` and `trust_domain.py:318-319`.)
3. **Launch bindings** (§3, §3.2): the validator reads HEAD, tree and interpreter itself; P7 by binding only, including its schema and r3c contract; the signing packet carries the acceptance evidence; A3 by each successor's own §10 regex. *Recommend: adopt.*
4. **Wording.** *Recommend: adopt the §11 addendum in a separate docs PR before H; #581 §5 item 3 names this authority; A6 stays verbatim.*
5. **Freeze A5/A6 before the build. This amends A1's order:** part of A1 step 6 moves ahead of step 4. *Recommend: yes.* Ratification must then leave the A5/A6 bytes untouched, including A5's "(drafted; …)" note, or H, the build and P7 repeat.
6. **Values block** `t00-step2-values/v1` in #581 §6, equal to `parameters`. *Recommend: yes, with S0 only and Run-1 waived, candidates flat in both runs (else INSUFFICIENT), `LOWER_NEAREST_RANK_INF_INCLUDED`, H = 1500 from A6, and your three RNG roots and `probe_root`.*
7. **Budget and interruptions** (§4.4–§4.5, §5.4). *Recommend: an in-run CPU probe; heartbeat and Job Object charging; resume only per the closed exception table, else TERMINAL INSUFFICIENT with completed counts only; a finished run scored despite a last-path overrun.* (Alternatives: any crash VOIDs; strict `runner.py:120-122` parity.)
8. **Termination acts** (§4.6). *Recommend: `abandon` and declining renewal are yours alone, signed, with your statement and every reader's exposure; after any TERMINAL INSUFFICIENT, a re-attempt needs a new #581 ratification that discloses that exposure.*
9. **Compute location and duration** (§6, §7). Private inputs cannot leave this machine, so the options are a dedicated local run of N days or a reduced depth. *Recommend: name N from the §6 table, and reduce depth before ratification if the projection exceeds it.*
10. **Approval windows.** *Recommend: fresh r3c and screen approvals with `expires_at` ≥ start + 1.5 × projected wall + `verify` time.* r3c-a2 expires 2026-10-09T01:52:19Z (#581 §5).
11. **Result access and acceptance** (§5.6). *Recommend: a one-line console; rows read only by `finalize`, `verify` and the coordinator after the label prints; an independent label script committed before signing; a re-execution sample of k = 9 (one per root × population).*

---

## 13. Risks and residuals

- **Dynamic access.** `getattr(src, 'screen_' + 'bracket')` is outside A10b. The in-method authority check, the process boundary and the audit hook enforce instead.
- **Single use is local.** Deleting the run directory and relaunching is a procedural breach, not something code prevents. The attestation and the ledger of attempts are the detectors.
- **Head drift.** Any commit before step 7 voids P7 at H. All packets must land first (§8).
- **Approval expiry mid-run.** A path started inside the window completes; the next path start refuses. It is resumable only by Joshua's renewal. Size the windows (OD-10).
- **Compute.** At the A4 upper bound the prereg-v2 depth is infeasible (§6). INSUFFICIENT is the only outcome of an undersized budget. No reduced depth is ever substituted after ratification (#581 A6).
- **Candidate scarcity.** A long L, or flatness in both runs, can empty the H1/H2 candidates and give INSUFFICIENT. L must be set knowingly (item 4).
- **Probe leakage.** Pre-ratification timing touches only sessions P7 already exposed (§6). The in-run probe runs after #581 is frozen.
- **Kernel trust.** P7 stubs the kernel, so P7 is no evidence that the kernel is correct. Kernel correctness rests on the existing runner and simulation tests, plus `code_head` binding.
- **Unhashed native libraries and data files.** Bound only through the interpreter and lock identity in the P7 record. This is a T05 hermeticity residual for both P7 and the screen.
- **Relabelling.** Screen output could be relabelled. This is mitigated by `evidence_class`, its own schemas and an unchanged `verify_for`. Any other use is a procedural violation.
- **Peeking.** Journals are readable in the private root before `finalize`. Only Joshua's signed termination act can end a run early, with every reader's exposure stated, and a re-attempt needs a ratification that discloses it (§4.6). A3 and the #581 freeze are in force before the first record.
- **Consumed-split count.** "A path with a consumed split" is read as either run having consumed one. The count is descriptive only.

---

## Audit hooks

```bash
# r3c refuses SCREEN/MONTE_CARLO exactly; unchanged by this design (expect the constants and the exact-match check).
rg -n 'SOURCE_PURPOSE = "T00_P7_SOURCE_VERIFICATION"|"SCREEN", "MONTE_CARLO"|doc\["refusals"\] != list\(SOURCE_REFUSALS\)' ops/c1_rail/qualification/contract.py

# The fence this design keeps: verify_for refuses; evaluate_replay requires ReplayResult.
rg -n "SOURCE_ONLY_NOT_QUALIFICATION" ops/c1_rail/qualification/production_source.py
rg -n "isinstance\(result, ReplayResult\)" ops/c1_rail/qualification/runner.py

# The run flags the screen wrapper carries are the ones replay_bracket computes and _seal records.
rg -n "failed = False|result, failed = exc.result, True|provider\._placed" ops/c1_rail/qualification/production_source.py

# P7 record fields the validator checks (schema constant; contract digest in the record).
rg -n "RECORD_SCHEMA = 't00-p7-evidence/v1'" ops/c1_rail/qualification/p7_evidence.py
rg -n "'contract_sha256': receipt.contract_sha256" ops/c1_rail/qualification/p7_driver.py

# A3: the successors' own answerer-exposure hooks (route-native :155, Vanguard :187) must each print exactly one line;
# and no ORB-3/VAN-3 row may still be OWED (expect no output once A3 is answered; today it prints the two OWED rows).
rg -n '^\| (ORB|VAN)-3 .*OWED' docs/briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md docs/briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md

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
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md | grep -v 'rg -n'
```
