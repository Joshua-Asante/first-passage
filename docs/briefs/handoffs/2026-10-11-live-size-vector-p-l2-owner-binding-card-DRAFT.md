# P-L2: the frozen size vector in the account owner's runtime binding (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** DRAFT, 2026-10-11. Drafted at Joshua's request ("draft the P-L1 and P-L2 build cards") for the Deployment Coordinator ("Portfolio deployment coordination") to freeze. Not frozen, not dispatched. **Not dispatchable until the §11 gates hold.**

**Base:** `origin/main` `b5571a9`. Every `file:line` is at that commit unless marked otherwise. `ops/c1_rail/book_account_owner.py` last changed `18107a75` (2026-10-02); `book_incident_irm_live_page.py` last changed `eebd37ba` (2026-10-04). **The executor's base is later:** it is cut after P-L1, protection-health and (per D-2) GC-5 have merged, so Phase 0 re-anchors every line.

**Parent scope:** [live size-vector wiring scope](../../notes/2026-10-11-live-size-vector-wiring-scope.md) (PR #773) §2 and §5 row P-L2. The successor [build card](2026-10-10-t00-successor-screen-build-card-DRAFT.md) §3.1 owns the vector interfaces. The screen authority defines the hash this card must reproduce: `size_vector_sha256 = sha256(canonical_json_bytes(sizing))` (`screen_authority.py:401-432`). **Prerequisite:** [P-L1](2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md) merged (`BookSizingBinding.size`).

**Authority:** none yet. G-1, G-2 and G-3 are separate acts (§11).

**Executor:** a Claude worker, single writer of `claude/live-size-p-l2` (proposed). **Not GLM:** the change is to sizing and to a bound module.

**Coordinator:** the Deployment Coordinator.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - not_dispatchable_until_section_11_gates_recorded
  - cut_after_p_l1_and_protection_health_merged
  - offline_synthetic_only
  - card_section2_files_only
  - fixture_edits_limited_to_section_2_4
  - no_book_policy_edit
  - no_book_sizing_context_edit
  - no_schema_version_or_table_change
  - no_module_global_added_to_bound_modules
  - no_measured_closure_or_p7_closure_edit
  - no_dd_protection_or_frozen_constant_edit
  - no_private_vector_value_read_or_committed
  - no_rail_arm
  - no_rail_deploy
  - no_account_traffic
  - no_live_or_route_wiring
  - no_host_or_fly_command
  - no_pine_or_port_access
  - no_main_write
  - no_merge
  - no_pr_open
  - no_glm
  - single_writer
  - stop_at_coordinator_return
acceptance:
  - tests/ops/test_live_size_vector_owner_binding.py
  - tests/ops/test_live_size_vector_sizing_context.py
  - tests/ops/test_book_account_owner.py
  - tests/ops/test_four_leg_runtime.py
  - tests/ops/test_pr409_related_cases.py
  - tests/ops/test_pr409_review4.py
  - tests/ops/test_book_bootstrap_migration.py
  - tests/ops/test_book_fence_classification.py
  - tests/ops/test_feed_omission_session_end.py
  - tests/ops/test_attended_incident_rehearsal.py
  - tests/ops/test_synthetic_integrated_session.py
  - tests/ops/test_book_incident_grafana_irm.py
  - tests/ops/test_tradeify_sizing_integration.py
  - tests/ops/test_c1_rail_image_manifest.py
  - tests/ops/test_c1_signal_daemon_image_manifest.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_seal.py
  - tests/ops/qualification/test_composition_fixture.py
  - tests/ops/qualification/test_composition_route.py
  - tests/ops/qualification/test_runtime_inventory.py
```

- `test_live_size_vector_owner_binding.py` is new.
- `test_live_size_vector_sizing_context.py` is P-L1's and must stay green.
- The others exist and stay green. The only edits allowed are the two §2.4 fixture lines.
- The last five are listed because `book_account_owner.py` is bound as `listener_account_owner` (`trust_domain.py:146`; `composition_fixture.py:83`).
- No tracked file pins the current SHA-256 of `book_account_owner.py` (`0b45513a…`) or of `book_incident_irm_live_page.py` (`fac6a47d…`); checked at drafting, §0(c).

## 0. Phase 0: premise, Rule-0 reads and findings returned before code

Report each finding before any test. A contradiction is a **stop** (§7).

- **(a) Base.**
  - HEAD contains P-L1's merge, and `BookSizingBinding` ends in `size: LegSize | None = None`.
  - HEAD contains the protection-health build's merge.
  - It contains GC-5-DISPLACED's merge if D-2 orders GC-5 first.
  - Re-anchor every `file:line` below at HEAD and report the mapping.
- **(b) Closure membership.** The measured-closure script at HEAD shows `book_account_owner.py` and `book_incident_irm_live_page.py` in neither set (§10). At drafting: 68 measured / 63 staging, neither file present. The P7 D8 list ([C′ card](2026-10-02-h9-cprime-runtime-identity-build-DRAFT.md) `:260-265`) names neither.
- **(c) Pins.** `git grep` finds no tracked SHA-256 (full or 16-hex prefix) of either file.
- **(d) The binding seam, at base lines:**
  - `_validate_binding` `:456-517`, with the required key set at `:458`;
  - `_binding_record` `:108-136`, with its lazy import at `:109`;
  - within-session equality `:425-427`;
  - the cross-session `immutable` tuple `:431-433`;
  - `_context` `:1555-1590`, where `BookSizingBinding` is built at `:1575`;
  - the dispatch at `:1812-1820`, including `zero_size` at `:1819`.
  - Also report every other reader of the binding record: `book_bootstrap.py:47-49` and `:126`, and `book_migration.py:111-117` and `:411-417`.
- **(e) Binding constructors.** At drafting, three functions build a complete runtime binding:
  - `tests/ops/test_book_account_owner.py:50` `binding()`;
  - `tests/ops/test_four_leg_runtime.py:39` `binding(*, protected=False)`;
  - `ops/c1_rail/book_incident_irm_live_page.py:68-73`.
  - Every other suite imports or copies one of these with `.update(...)`.
  - Report any other constructor. If there is one, return `NEEDS_CONTEXT`, because the §2.4 edit set would grow.
- **(f) The encoder.** `qualification/contract.py:266` `canonical_json_bytes` is already in both images (`deploy/c1_rail/Dockerfile:64`, `deploy/c1_signal_daemon/Dockerfile:52`) and is a trust-domain runtime dependency. Confirm both. Confirm that `import c1_rail.book_account_owner` still succeeds with a function-local import of it (default (C)).
- **(g) Legacy records.** Run `test_book_bootstrap_migration.py` at HEAD. Report whether any migrated or legacy retained `runtime_bindings` record is followed by a boot in the **same** session. If it is, the within-session raw-equality check (`:425-427`) would refuse it once the record body gains keys. In that case return `NEEDS_CONTEXT` with the failing case.

## 0.5. Routing and clarifying questions

Routing: Claude worker, local or cloud. No vendor data, secret, Pine, port or private value is read (template §0.75: `N/A`). Tests use synthetic vectors built with `validate_size_vector` from public mappings. **Never use the FLOOR-HALF values.**

Apply each recommended default unless Phase 0 contradicts it. On a contradiction, return `NEEDS_CONTEXT` and quote the conflict.

- **(A) The binding key.** **Recommended default:** one new required key, `"size_vector"`, whose value is a `SizeVector`.
  - The owner computes the hash itself.
  - It never accepts a declared hash as a substitute for recomputing it.
  - The comparison against a declared hash belongs to P-L4 (the loader and the GO).
- **(B) Validation at the consumption boundary.** **Recommended default:** in `_validate_binding`:
  - require `isinstance(binding["size_vector"], SizeVector)`;
  - require `validate_size_vector(vector.as_mapping()) == vector`. A `SizeVector` built directly skips `_require_canonical`, so this round trip refuses a non-canonical vector.
  - Any failure raises `AccountOwnerError`. The identity vector is allowed: it is the declared book.
- **(C) The hash.** **Recommended default:** `sha256(canonical_json_bytes(vector.as_mapping())).hexdigest()`.
  - `canonical_json_bytes` is imported **inside** `_binding_record`, as `book_adapters` already is at `:109`, so no module-level name is added.
  - This is the screen authority's formula byte for byte.
- **(D) The record.** **Recommended default:** `_binding_record` adds two keys: `"size_vector"` (the mapping) and `"size_vector_sha256"`. Both are appended to the `immutable` tuple.
- **(E) Legacy records.** **Recommended default:** a retained record from before P-L2 lacks both keys. For the cross-session comparison only, read it as the identity vector's mapping and hash, computed inline. Every pre-P-L2 owner sized at identity, so this is a fact, not a default.
  - A record lacking the keys followed by a non-identity vector is refused: "unverified runtime binding transition".
  - Never raise `KeyError`.
- **(F) Passing the size.** **Recommended default:** `_context` passes `size=self.binding["size_vector"].leg(action.leg_id)` to `BookSizingBinding` by keyword. The owner never passes `None`.
- **(G) Parity reference.** **Recommended default:** law-level parity. The owner's `qty_out` equals `entry_quantities(..., size=vector.leg(k))` / `add_quantity(..., size=...)` for the same inputs, which are the calls at `replay.py:612-616`. A full `BookReplay`-driven comparison is optional. If it is not cheap with existing test helpers, say so under `DONE_WITH_CONCERNS`; do not build a harness.

## 1. Goal

Every live entry and add that the account owner sizes uses the frozen size vector held in its runtime binding. That vector is:
- required;
- validated in canonical form at the boundary;
- stamped with its `size_vector_sha256` into the durable `runtime_bindings` record;
- immutable for the owner's life.

The stamped hash is the value that P-L4's activation check compares with the screen authority and the deployment GO.

**Not asked:** the loader, configuration, deployment GO or boot gate (P-L4); the emulator (P-L3); any host or route wiring; any real vector value.

## 2. Scope

### 2.1 `book_account_owner.py`

- `_validate_binding`: add `"size_vector"` to the required set (`:458`), plus check (B).
- `_binding_record`: add the keys in (D), using (C).
- Boot transition: add both keys to `immutable` (`:431-433`), with the legacy reading in (E).
- `_context`: pass `size=` (F).

Change nothing else in the file.

### 2.2 `book_incident_irm_live_page.py`

The synthetic page's binding (`:68-73`) gains `"size_vector": IDENTITY_SIZE_VECTOR`. Its behaviour is unchanged: its allocations are 0.

### 2.3 What does not change

- `book_policy.py`, `book_sizing_context.py`, `book_bootstrap.py`, `book_migration.py`, the schema version (4), the tables, and every refusal reason other than the two transition messages already present (`:427`, and the "unverified runtime binding transition" at `:439`).
- The bootstrap `binding_digest` value changes, because the record body changes. Its derivation does not.

### 2.4 Fixture edits (the only test edits allowed)

- `tests/ops/test_book_account_owner.py` `binding()` (`:50-74`): one key, `"size_vector": IDENTITY_SIZE_VECTOR`, and that name added to the file's existing `book_policy` import.
- `tests/ops/test_four_leg_runtime.py` `binding()` (`:39-62`): the same one key and import.

The other suites inherit the key through these functions. Any further fixture edit is a **stop**.

### 2.5 Files

| File | Edit |
|---|---|
| `ops/c1_rail/book_account_owner.py` | §2.1 |
| `ops/c1_rail/book_incident_irm_live_page.py` | §2.2 |
| `tests/ops/test_book_account_owner.py`, `tests/ops/test_four_leg_runtime.py` | §2.4 only |
| `tests/ops/test_live_size_vector_owner_binding.py` | new |

## 3. Method

1. Phase 0 (§0). Post the findings, including (g).
2. Write the §4 rows. Run them at the cut base and record the **red** run.
3. Make §2.1–§2.4. Record the **green** run of the new file, then the acceptance list.
4. Run `python -I scripts/fp.py test-ops` once, and `python -I scripts/fp.py check`. Cite each `record.json`.
5. Stage only the §2.5 files. Check the commit message against `git diff --cached`. Push the branch and return.

Neither edited code file is in the S2 workflow's path filters (`qualification-s2-supervision.yml:33-55`), so no S2 run is triggered.

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** `N/A`. This executes the scope note's P-L2 row; there is no hypothesis under test.

| Row | Test in `test_live_size_vector_owner_binding.py` | Fails if |
|---|---|---|
| LB1 | A binding without `size_vector`: `BookAccountOwner.boot` raises `AccountOwnerError` ("complete runtime binding required"); no database file is created | The vector is optional |
| LB2 | `size_vector` given as a dict mapping, not a `SizeVector`: refused | An untyped vector is accepted |
| LB3 | A `SizeVector` built directly with a non-canonical Striker encoding (a cap multiplier above the canonical smallest, which `validate_size_vector` refuses): refused | A non-canonical vector is accepted |
| LB4 | After boot, the latest `runtime_bindings` body holds `size_vector == vector.as_mapping()` and `size_vector_sha256 == sha256(contract.canonical_json_bytes(vector.as_mapping()))` | The stamp is missing or uses another encoding |
| LB5 | Re-boot in the same session with a different vector: "runtime binding changed within session" | A vector changes inside a session |
| LB6 | Next session (valid prior-session chain) with a different vector: "unverified runtime binding transition" | A vector changes across sessions |
| LB7 | A retained record with both keys removed (written directly into a test database), then a next-session boot. With the identity vector: boots. With a non-identity vector: "unverified runtime binding transition". Neither path raises `KeyError` | Legacy records crash or admit a changed vector |
| LB8 | A synthetic non-identity vector, one entry per leg dispatched through `SyntheticBroker`: each reserved quantity equals `entry_quantities(..., size=vector.leg(k))` for the same inputs, and differs from the identity case on at least one leg | The owner does not pass the vector |
| LB9 | A leg at 0: entry returns `refusal_reason="zero_size"`, reserves nothing and sends no command | A zero leg sizes or sends |
| LB10 | Striker `adds=OFF`, with a confirmed base above 0: the add returns `zero_size`; with `UNCHANGED`, it equals `add_quantity(..., size=...)` | The add law ignores the vector |
| LB11 | With `IDENTITY_SIZE_VECTOR`, every listed existing suite passes with only the §2.4 lines changed | The default binding changes any behaviour |

**Revert trigger:** any listed suite changes outcome beyond the §2.4 key additions, or any quantity changes under the identity vector.

## 5. Forbidden

- Edits outside §2.5. In particular:
  - `book_policy.py`;
  - `book_sizing_context.py`;
  - `book_bootstrap.py`;
  - `book_migration.py` or the migration fixtures (`tests/fixtures/book_migration/*.json`);
  - `trust_domain.py`;
  - `policy_fingerprint.py`;
  - `book_runtime.py` and `c1_rail_listener.py`.
- A schema-version bump, a new table or a new column.
- A module-level import, constant or helper in `book_account_owner.py`. (C) and (E) are computed inside functions.
- Accepting a declared hash in place of recomputing it.
- A default vector in `_validate_binding`. `None` or absence is a refusal, not identity. Identity is read only for legacy **retained** records (E).
- Any real vector value; any private artifact, Pine, port or `effective_inputs.json`; GLM; a push to `main`; a merge; opening a PR.
- `dd_protection`, `DD_TRIGGER`/`DD_SCALE`, `CANDIDATE_SCALE`, `BASE_RISK` or the lifecycle multipliers.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | LB1–LB10 red at the cut base and green on the build; LB11 and every acceptance suite green; the `fp test-ops` and `fp check` records completed with exit 0; footprint equals §2.5 |
| `DONE_WITH_CONCERNS` | As DONE, with an off-pattern observation. This includes the (G) optional replay comparison not built |
| `NEEDS_CONTEXT` | (e) finds another constructor; (g) finds a same-session legacy reboot; a §0.5 default is contradicted |
| `BLOCKED — context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong` | As named; `plan-itself-wrong` covers a §0(b) closure hit or an import cycle that (C) cannot avoid |

**Gate verdict (coordinator, at review):**
- **RESOLVED** when the return is `DONE` and both §7 passes reproduce it.
- **FALSIFIED** when a §4 row cannot be made red on the base, or a revert trigger fires.
- **AMBIGUOUS** (held for the coordinator) on `DONE_WITH_CONCERNS`.

**Report:** the status; red and green record paths per row; the acceptance records; `git diff --name-only <cut base>..HEAD`; the Phase-0 re-anchor map; concerns; the next action recommended.

## 7. Stop conditions and parent review

**Stop and return; do not work around:**
- any §0 finding that contradicts this card;
- a listed suite red at the cut base;
- a row that cannot be made red;
- a green run needing an edit outside §2.5.

**Parent review (coordinator):**
- **Pass 1, spec compliance:**
  - the diff is exactly §2.5;
  - the fixture diffs are the two one-key additions and their imports;
  - there is no new module-level name in `book_account_owner.py`;
  - the record carries both keys;
  - `immutable` carries both keys.
- **Pass 2, quality:**
  - re-run LB1–LB11 and the acceptance list from a clean worktree at the returned head;
  - recompute LB4's hash independently with `screen_authority`'s formula;
  - confirm that `_context` cannot reach `size_book_request` with `size=None`.
- **Pass 3, consolidated read with P-L1:**
  - read P-L1's and P-L2's diffs together;
  - confirm that the size travels binding → `_context` → `BookSizingBinding.size` → `entry_quantities`/`add_quantity` with no `None` on the live path.

## 8. Out of scope and decision unlocked

**Out of scope:** P-L3 (emulator parity), P-L4 (GO and boot-gate equality as TB-I3 interlock amendments; the loader as requirement R-SV of the live route packet; [proposal](../../notes/2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md)) and P-L5 (records).

**Unlocks:**
- The owner's stamped `size_vector_sha256` exists for P-L4 to compare with the screen authority's `parameters.expressions.size_vector_sha256` and the GO.
- T16 can "prove equality to qualified shared components" for sizing.

## 9. Sequencing and file collisions

- **Protection-health** (FROZEN, building) edits `book_account_owner.py` near `:1694-1729`. P-L2 is cut only after it merges: "No two live packets share a file" (umbrella `:245`).
- **GC-5-DISPLACED** (DRAFT) adds an `aegis_takeover` keyword to `__init__`/`boot` and stamps its resolved value in the same binding record (GC-5 card `:116`). That is the same seam. Serialize per D-2, and keep one stamping pattern.
- **TB-I3** (DRAFT) edits `book_account_owner.py` in its S2 latch, which is already ordered after GC-5. The coordinator orders it against P-L2 at freeze (D-2). **TB-I3-HOST** (FROZEN 2026-10-06) forbids that file and is no collision.
- **Roadmap:** P-L2 is behaviour-changing frozen work. It lands before CP-6 (checklist T15). P-L4 then uses the stamp at T16 and T17.

## 10. Audit hooks (runnable)

```bash
# Card form and authority. Expected: RESULT: well-formed; 0 violations.
python scripts/check_brief.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md --type cc_handoff
python scripts/check_handoff_authority.py docs/briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md

# Closure membership (§0(b)). Expected: 0.
cp docs/notes/2026-09-29-s5-c3-record/stage1c-equivalence/stage1c_closure_table.py.txt "$TMP/closure.py"
python -I "$TMP/closure.py" . b5571a9 HEAD | grep -c "book_account_owner\|book_incident_irm_live_page"

# Pins (§0(c)). Expected: no output.
for f in ops/c1_rail/book_account_owner.py ops/c1_rail/book_incident_irm_live_page.py; do git grep -l "$(sha256sum $f | cut -c1-16)"; done

# Constructors (§0(e)). Expected: the three listed functions only.
grep -rn '"max_evidence_age": timedelta' ops tests

# Scope at return. Expected: exactly §2.5.
git diff --name-only <cut-base>..HEAD

# No module-level addition. Expected: no new top-level import or assignment.
git diff <cut-base>..HEAD -- ops/c1_rail/book_account_owner.py | grep -E '^\+(from|import|[A-Z_]+ *=)'

# Live path never passes None. Expected: one hit, with size= set from the binding.
grep -n "BookSizingBinding(" -A8 ops/c1_rail/book_account_owner.py | grep -n "size="

# Suites. Each prints a record.json; cite it.
python -I scripts/fp.py python -m pytest tests/ops/test_live_size_vector_owner_binding.py <the authority-block acceptance list>
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates (the card is NOT DISPATCHABLE until all three hold)

- **G-1. Joshua's code admission.** Joshua names the §2.1 edits to `book_account_owner.py` (bound as `listener_account_owner`, `trust_domain.py:146`) and the §2.2 edit. A single admission may also cover P-L1 (scope note Q5). The coordinator records his words and the time.
- **G-2. Coordinator freeze.** The coordinator answers §12, re-anchors §0(d) at the cut base, commits the frozen revision and records its SHA.
- **G-3. Dispatch.** Requires P-L1 and protection-health merged, plus the D-2 order. Recommended: after the successor screen returns GO (scope note Q6).

## 12. Open decisions (coordinator at freeze; Joshua where marked)

- **D-1 (Joshua; scope note Q1).** Required vector, with identity stated explicitly for the declared book? *Recommend:* yes. That is this card's (A) and the §5 ban on a default.
- **D-2. Order on the shared seam:** protection-health → GC-5 → P-L2, or protection-health → P-L2 → GC-5? *Recommend:* GC-5 first. It is ruled for the first release, and P-L2 then follows its stamping pattern.
- **D-3.** Confirm (E): legacy retained records read as identity for comparison only. *Recommend:* confirm. The alternative, refusing every legacy record, would refuse owners whose quantities were already today's.
- **D-4 (Joshua; scope note Q2).** Caps, tiers and risk basis are outside this card. *Recommend:* leave them out, and keep the T16 equality item that the scope note names.

## Pre-mortem

- **Loop cost.** One targeted run, one `fp test-ops` and one `fp check`. Budget: two full suite runs. A third run is a checkpoint. No S2 workflow run is triggered.
- **Decisions the executor will hit:** (A)–(G) are pre-ruled. The two likely bounces are §0(e) (another binding constructor) and §0(g) (a same-session legacy reboot). The coordinator can pre-empt both by running those two reads at freeze.
- **What would make this moot:** NO-GO on the screen (withdraw), or Joshua putting the vector somewhere other than the owner binding (D-1).
- **Evidence binding:** acceptance evidence is the targeted, `fp test-ops` and `fp check` records at the returned head only. A push afterwards voids them.
- **Measure:** wall time, runs and rounds are filled in at return.
