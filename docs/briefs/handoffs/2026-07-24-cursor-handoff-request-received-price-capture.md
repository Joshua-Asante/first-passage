# Cursor Handoff — persist `close` / `stop_dist_pts` in the `request_received` event (B7 slippage-capture prerequisite)

**Date:** 2026-07-24
**Parent session:** Claude Code operator session (Joshua + Claude) — closed Q-COSTGEO-3 and queued the B7 per-fill slippage capture in the same session; this handoff removes that capture's one blocking prerequisite.
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (single-step)
**Parent question:** N/A — executes the B7 slippage-capture prerequisite queued by the Q-COSTGEO-3 closure. **⚠ That closure and the RUNBOOK §B7 Stage 2b section are on an unmerged parent branch and are ABSENT from `origin/main`** — so they are **not** §0 reads. Everything you need from them is inlined in §1. Do not go looking for them; their absence is expected, not a discrepancy.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **No `core/` edit, no Pine touch, no sizing-law change, no live rail/account touch, no config edit, no `dry_run` flip.** Telemetry-field widening only.

---

## Routing-test self-check (per [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md), applied by the parent before dispatch)

- **Test 0 (dispatch-environment bytes/credentials):** **PASS — no gated bytes needed.** This task touches `ops/` source + `tests/ops/` only. It requires **no** gitignored vendor data (`core/data/**`), **no** Pine, **no** API key, **no** deployed config. The two panel CSVs and the databento key that gated prior dispatches are **irrelevant here**. Cloud dispatch is safe.
- **Test 1 (locked/governed surface):** **PASS — not on it.** `ops/c1_rail/c1_rail_http_server.py` is not a `core/` anchor path (not `dd_protection.py` / `firm_rules.py` / `portfolio_mc.py` / `core/mc/*` / `lifecycle.py` / `dd_geometry.py`), not Pine, not an ADR/pre-reg/closure. The change adds two keys to a telemetry dict; it does not touch sizing arithmetic, the DD/lifecycle path, or any order field.
- **Test 2 (spec frozen):** **PASS.** The exact function, the exact dict, the two exact keys, and the acceptance assertions are pinned in §2. No judgment call is expected. Every ambiguity the parent could find is pre-resolved in §0.5 with a recommended default.
- **Test 3 (overhead threshold):** **Marginal, and dispatched anyway — deliberately.** The edit is ~2 lines in 1 file + tests; below the ~1-hour / ~3-file floor, so the ADR's default would be "stays on whichever surface is open." It is dispatched to Cursor regardless because **M1 is `CODE_LANDED`, not `RESOLVED`** ([`M1_MONITORING_ACCEPTANCE.json`](../../notes/rail_build/M1_MONITORING_ACCEPTANCE.json)): the parent session declines to touch the live request path while M1 acceptance evidence is mid-collection, and wants the change to arrive as a reviewable PR that can be sequenced with the M1 drills rather than as an in-session edit. **The isolation is the point, not the throughput.**

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing code. If repo state contradicts any §0 claim below, return `NEEDS_CONTEXT` with the discrepancy quoted — do **not** proceed on the inconsistent reading.

**Dispatch base ref: `origin/main`.** The parent authored this brief from a feature worktree that is **behind `origin/main`**; anchors below are re-verified **against `origin/main` @ 2026-07-24** and are what your worktree will contain. Verify each with `git log -1 --format='%h %ci' -- <path>`:

| File | Anchor on `origin/main` |
|---|---|
| `ops/c1_rail/c1_rail_http_server.py` | **`ff3510d`** (2026-07-24 11:36) |
| `ops/c1_rail/c1_rail_telemetry.py` | `54b1489` (2026-07-23 16:44) |
| `ops/c1_rail/c1_sizing_host_reference.py` | **`c134060`** (2026-07-24 19:14) |
| `tests/ops/test_c1_rail_http_server.py` | `54b1489` |
| `tests/ops/test_c1_rail_telemetry.py` | `54b1489` |

**Premise re-verified against `origin/main` by the parent before dispatch** (not assumed from the stale worktree): the `parsed` dict is byte-identical at **L481–485**, `ops/c1_rail/c1_rail_telemetry.py` is unchanged, and `_REQUIRED_PAYLOAD_FIELDS` still reads `("leg_id", "signal_type", "bar_time", "close", "stop_dist_pts")`. The only `c1_rail_http_server.py` change since `54b1489` is a **one-line comment edit** (a docstring cross-reference), touching nothing this task depends on.

- [`ops/c1_rail/c1_rail_http_server.py`](../../../ops/c1_rail/c1_rail_http_server.py) — **the only file this task edits.** Report: (a) `_handle_post`'s full body, specifically the `parsed = {...}` dict built when `signal_type is not None`; (b) `_emit_request`'s full body; (c) every call site of `_emit_request` — there are **three** (`non_json`, `non_object_json`, and the parsed-B1 call, all in `_handle_post`). **Separately**, the unauthorized-path branch in `do_POST` emits a `request_received` record by calling `ledger.append` + `make_request_received` **inline**, *not* via `_emit_request`, and passes no `parsed_fields` at all (so `parsed` defaults to `None`). *(An earlier revision of this brief said "four `_emit_request` sites" — wrong, and corrected here from a Cursor Phase-0 report the parent re-verified.)* **Confirm the parent's claim: the `parsed` dict currently carries exactly `leg_id`, `signal_type`, `bar_time` — and does NOT carry `close` or `stop_dist_pts`.**
- [`ops/c1_rail/c1_rail_telemetry.py`](../../../ops/c1_rail/c1_rail_telemetry.py) — report `make_request_received`'s signature and body, and `assert_no_secrets`'s denylist + value-hint regex. **Confirm two things: (1) `make_request_received` forwards `parsed_fields` verbatim via `dict(parsed_fields)` — so it needs NO change for this task; (2) `assert_no_secrets` runs on every `ledger.append` record and hard-fails on denylisted keys or secret-shaped values.**
- [`ops/c1_rail/c1_sizing_host_reference.py`](../../../ops/c1_rail/c1_sizing_host_reference.py) — report `_REQUIRED_PAYLOAD_FIELDS` (**L101-102 on `origin/main`**) and the `stop_dist_pts` consumption (**L279**). *(This file was refactored on `origin/main` after the parent's worktree snapshot — the contract is unchanged but the line numbers moved; trust the file, not these numbers.)* **Confirm the B1 payload contract is `("leg_id", "signal_type", "bar_time", "close", "stop_dist_pts")` and that `stop_dist_pts` is already parsed as `float`.**
- [`tests/ops/test_c1_rail_http_server.py`](../../../tests/ops/test_c1_rail_http_server.py) — report the module docstring and the helper conventions (`_base_cfg`, `_write_cfg`, `TOKEN`). Note that this file currently tests **pure module-level helpers only** — `_handle_post` and `_emit_request` are handler-closure internals with no direct coverage here.
- [`tests/ops/test_c1_rail_telemetry.py`](../../../tests/ops/test_c1_rail_telemetry.py) — report `test_append_request_decision_transport_seq_monotonic` (~L68-90), which already appends a `request_received` record with a `parsed` dict. **This is the existing coverage proving `request_received` IS emitted and IS exercised.**
- [`docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`](../../notes/rail_build/M1_MONITORING_ACCEPTANCE.json) — report `status` and the `notes` array. **Confirm `status == "CODE_LANDED"` (not `RESOLVED`)** — this is why §5 forbids any behavioral change to the request path.
- Baseline test run — report the result of:
  ```bash
  python -m pytest tests/ops/test_c1_rail_http_server.py tests/ops/test_c1_rail_telemetry.py -q
  ```
  **Parent-observed baseline 2026-07-24: `52 passed`.** If your count differs, report it before proceeding.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated. Confirm or challenge in the Phase-0 response; set `Status: NEEDS_CONTEXT` if you disagree with any.

- **(A) Coercion vs verbatim pass-through.** `close` and `stop_dist_pts` arrive from JSON and could be `int`, `float`, `str`, or absent. **Recommended default: pass through verbatim via `payload.get(...)`, exactly as the three existing keys do** — no `float()` coercion, no validation, no defaulting. Rationale: (1) the three incumbent keys use bare `.get()`, so this stays symmetric; (2) `request_received` is the *as-received* record — coercing it would destroy the forensic value of seeing what actually arrived; (3) the sizing host already coerces `stop_dist_pts` to `float` downstream at its own boundary (L247), and duplicating that here creates a second, divergent parse site. A malformed value should appear in the ledger as malformed.
- **(B) Which `_emit_request` call sites get the new keys.** **Recommended default: only the parsed-B1 site** — i.e. inside the `if signal_type is not None:` block where `parsed` is built. The two other `_emit_request` sites (`non_json`, `non_object_json`) pass `parsed=None` by construction, and the inline unauthorized-path append passes no `parsed_fields` at all; **all three must stay that way** — a non-JSON or unauthorized body has no `close`. Do **not** attempt to extract price fields from an unparsed body.
- **(C) Where the test lives.** `_handle_post` is a closure inside `make_handler`, not a module-level function, so a direct unit test needs either a handler instantiation or a small refactor. **Recommended default: do NOT refactor to expose it.** Instead extract the dict construction into a module-level pure helper (see §2 Step 2.1) and test that helper directly — this matches the file's existing "pure helpers ARE unit-tested; socket wiring is untested-by-design" split stated in its own docstring. If you see a materially cleaner option that does not touch the socket path, propose it in Phase 0 rather than implementing it.
- **(D) Secret-scan interaction.** The new keys are numeric price fields, so `assert_no_secrets` should be a no-op on them. **Recommended default: add one regression test asserting a realistic B1 payload (with `close` and `stop_dist_pts`) appends cleanly through `EventLedger.append` without raising `TelemetryError`.** Confirm no denylist key name collides with `close`/`stop_dist_pts` (parent read says it does not — `assert_no_secrets` matches on `secret`/`token`/`password`/`bearer` substrings).

---

## §1 — Context

Q-COSTGEO-3 (closed 2026-07-24) measured the live **67-lot MYM add at ~13× median displayed depth** — it clears the inside on **0 of 61** historical add-moments. The follow-up is to capture **realized** add slippage at B7 (the first armed session) and compare it against the panel's own basis. That basis is exact: **100%** of panel add entries fill at a deterministic offset from the signal-bar close (MYM `close + 1.00` index pt; MNQ `close + 0.50`), n=35/n=44, zero exceptions. So the live test is simply `fill_price − signal_bar_close`.

`BrokerEvidence` already persists `fill_price`. **The signal-bar close is not persisted anywhere** — so the subtraction is currently impossible from the ledger alone. That is the gap this task closes.

**Inlined context (the RUNBOOK §B7 Stage 2b section is NOT on `origin/main`; this is its substance, self-contained):** at B7 the operator records, per add fill, `event_id` · `leg_id` · `signal_type` · signal-bar `close` · `fill_price` · `fill_qty` · fill timestamp · `tradovate_order_id`, **cohort-split base vs add** (aggregate is worthless — the edge is 63.6% MYM / 87.7% MNQ in the add legs). Standing constraints there: keep `order_type=market`, and do not buy the $19.91 `mbp-10` depth escalation on one bad fill. None of that is your concern to implement — it is *why* the two fields must reach the ledger.

**Correction the parent owes this brief:** the first version of this prerequisite claimed `request_received` was "declared in `EVENT_KINDS` but never emitted" and located the fix in `c1_rail_listener.py`. **Both were wrong.** `request_received` *is* emitted — from `c1_rail_http_server._emit_request`, on four paths, with existing test coverage. The parent had grepped the listener alone and generalized to "the rail." The real gap is narrower: the `parsed` dict omits two fields. **Cursor should trust the §0 reads over any prose, here or elsewhere, and bounce `NEEDS_CONTEXT` on any residual contradiction.**

**What Cursor is asked to produce:**
- A ~2-line widening of the `parsed` dict in `ops/c1_rail/c1_rail_http_server.py` so `request_received` carries `close` and `stop_dist_pts`.
- A module-level pure helper for that dict construction, so it is directly unit-testable (§0.5(C)).
- Tests: the helper's output shape, the four-call-site invariant, and a secret-scan regression.

**What Cursor is NOT asked to do:** edit `ops/c1_rail/c1_rail_telemetry.py` (`make_request_received` already forwards `parsed_fields` verbatim — a change there would be scope creep); edit `ops/c1_rail/c1_rail_listener.py` (**the wrong file — that was the parent's original error**); add fields to `decision_fields()`, `BrokerEvidence`, or any other event variant; touch sizing, DD, lifecycle, equity, or transport logic; add validation/coercion (§0.5(A)); bump `SCHEMA_VERSION`; write the B7 analysis harness that will eventually *consume* these fields (out of scope, downstream, and gated on real fills); touch any deployed config or `dry_run`.

---

## §2 — Execution plan

TDD: write the failing test first, then the change.

### Step 2.1 — Extract + widen the parsed-fields builder

- **Inputs:** `ops/c1_rail/c1_rail_http_server.py` `_handle_post` (the `parsed = {...}` block); `_classify_signal_type`; `_b1_order_id`.
- **Action:**
  1. Add a module-level pure helper beside the existing `_classify_signal_type` / `_b1_order_id` helpers — suggested name `build_parsed_fields(payload: dict, signal_type: str) -> dict`. It returns the as-received B1 fields for the ledger:
     ```python
     {
         "leg_id": payload.get("leg_id"),
         "signal_type": signal_type,
         "bar_time": payload.get("bar_time"),
         "close": payload.get("close"),
         "stop_dist_pts": payload.get("stop_dist_pts"),
     }
     ```
     Verbatim `.get()` per §0.5(A) — no coercion, no defaults, no validation.
  2. Replace the inline `parsed = {...}` construction in `_handle_post` with a call to it. **No other line of `_handle_post` changes.**
- **Expected output:** `ops/c1_rail/c1_rail_http_server.py` diff of roughly +10 / −5 lines, confined to the new helper and the one call site.
- **Per-step gate:** `signal_type` remains the **classified** value (from `_classify_signal_type`), not `payload["signal_type"]` raw — preserving current behavior exactly. The other three `_emit_request` call sites are untouched and still pass `parsed=None`.

### Step 2.2 — Tests

- **Inputs:** `tests/ops/test_c1_rail_http_server.py` conventions; `tests/ops/test_c1_rail_telemetry.py` ledger fixtures.
- **Action:** add tests covering:
  1. `build_parsed_fields` returns all **five** keys for a well-formed B1 payload, with `close` and `stop_dist_pts` carrying the payload's values unchanged.
  2. Missing `close` / `stop_dist_pts` yield `None` for those keys and do **not** raise (informational-robustness).
  3. Verbatim pass-through: a string `close` (e.g. `"52737"`) stays a string — asserts no coercion crept in (§0.5(A)).
  4. `signal_type` in the returned dict equals the **classified** argument, not a raw payload echo (pass a payload whose `signal_type` differs from the argument to prove it).
  5. Secret-scan regression (§0.5(D)): appending a `request_received` record built from a realistic B1 payload through `EventLedger.append` succeeds and round-trips via `iter_records()` with `close` / `stop_dist_pts` intact.
- **Expected output:** ~5 new tests; **all previously-passing tests still pass** (baseline `52 passed`).
- **Per-step gate:** `python -m pytest tests/ops/ -q` green, with a strictly higher count than the 52 baseline. No existing test modified — if one must change, that is a behavioral change: **stop and return `NEEDS_CONTEXT`.**

### Step 2.3 — Repo gates

- **Action:** run `python scripts/check_boundaries.py` and the ops test suite.
- **Expected output:** boundaries clean; no new import edges (`ops/` already imports `c1_rail_telemetry`).
- **Per-step gate:** both green.

---

## §4 — Falsifiable premise (not a statistical hypothesis)

This handoff executes a queued prerequisite, so there is no Pre-Q hypothesis under test — the correctness bar is the §2 per-step gates + §6 acceptance. But the task **does** rest on one factual premise, and **the parent already stated a wrong version of it once** (§1). It is therefore written here as an explicit, Phase-0-checkable falsifier rather than assumed.

**Premise P:** in `ops/c1_rail/c1_rail_http_server.py` @ `ff3510d` (`origin/main`, re-verified 2026-07-24), the `parsed` dict built in `_handle_post` for a classified B1 signal carries exactly `{leg_id, signal_type, bar_time}` and **omits** `close` and `stop_dist_pts` — so the signal-bar close is absent from every `request_received` record, and `fill_price − signal_bar_close` is not computable from the ledger.

**P is FALSIFIED if** Phase 0 shows the `parsed` dict (or any other ledger event variant — `decision`, `broker_evidence`, `transport_result`) already persists the signal-bar close under any key. **Then this task is moot: do not write the change.** Return `NEEDS_CONTEXT` quoting the field and its location, so the parent can retarget the B7 capture at the field that already exists instead of adding a duplicate.

**P is CONFIRMED if** the four §0 reads agree that no price field reaches the ledger. Then proceed to §2.

**Why this is load-bearing rather than ceremony:** the parent's first version of this prerequisite asserted `request_received` was "never emitted" and named `c1_rail_listener.py` as the fix site. Both were false — established by reading one module and generalizing. A handoff built on that version would have edited the wrong file to add an event that already exists. Phase 0 exists to catch the same class of error one more time.

---

## §5 — Forbidden moves

- **Editing `ops/c1_rail/c1_rail_listener.py`.** The parent's own first draft named this file. It is the **wrong** file and the §0 reads prove it. Touching it re-introduces the corrected error.
- **Editing `ops/c1_rail/c1_rail_telemetry.py`.** `make_request_received` already forwards `parsed_fields` verbatim. Widening its signature or hardcoding price keys there duplicates the contract at a second site — the exact "second source of truth" the rail's design notes warn against.
- **Any behavioral change to the request path while M1 is `CODE_LANDED`.** No new failure modes, no changed HTTP status, no changed log line, no altered control flow, no new exception surface. If `request_received` telemetry fails it must still be swallowed exactly as today (`_emit_request`'s existing `except Exception` → `notifier.notify(CRITICAL)`). **A change that alters when an order is or isn't sent is an immediate `BLOCKED — plan-itself-wrong`.**
- **Adding validation or coercion** to `close` / `stop_dist_pts` (§0.5(A)). The sizing host owns that boundary; a second parse site can diverge silently.
- **Bumping `SCHEMA_VERSION`.** Adding optional keys to a free-form `parsed` sub-dict is additive; readers already tolerate `parsed: None`. A version bump would imply a breaking change and invalidate the existing ledger.
- **Scope creep — the "while I was in there" refactor.** Do not restructure `_handle_post`, do not add fields to `decision_fields()` or `BrokerEvidence`, do not "improve" the equity path, do not touch `_audit`. Log observations in §6 `DONE_WITH_CONCERNS` instead.
- **Writing the B7 slippage analysis harness.** It consumes these fields but is downstream, gated on real fills, and out of scope.
- **Touching deployed config, `dry_run`, secrets, or the Fly volume.** Nothing in this task requires them.

---

## §6 — Gate + status return taxonomy

Return **exactly one** status.

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | §2.1–2.3 gates green; diff confined to `ops/c1_rail/c1_rail_http_server.py` + `tests/ops/*`; no existing test modified; test count strictly > 52. | Parent reviews, sequences the merge with the M1 drills. |
| `DONE_WITH_CONCERNS` | Work complete but something off-pattern was noticed (e.g. a cleaner refactor exists, or a §0 read differed cosmetically). | Parent adjudicates before merge. |
| `NEEDS_CONTEXT` | A §0 claim contradicts repo state, or a §0.5 default is wrong. | Parent supplies the correction and re-dispatches. |
| `BLOCKED — <sub-case>` | Structural obstruction; sub-case mandatory (below). | Parent escalates, decomposes, or re-dispatches. |

**`BLOCKED` sub-cases (mandatory — name one):**
- `BLOCKED — plan-itself-wrong`: the change cannot be made without altering request-path behavior, or an existing test must be modified to pass. **The most likely sub-case here** — escalate, do not work around it.
- `BLOCKED — context-problem`: a §0 file or anchor is unreadable in the dispatch environment; re-dispatch with the missing context.
- `BLOCKED — capability-problem`: the environment cannot run `pytest` / `check_boundaries.py`; re-dispatch or escalate to the operator.
- `BLOCKED — scope-problem`: the change cannot be confined to `ops/c1_rail/c1_rail_http_server.py` + `tests/ops/*`; decompose before proceeding.

**Premise gate (§4, checked at Phase 0, before any code):** if premise P is **FALSIFIED** — the signal-bar close already reaches the ledger under some key — return `NEEDS_CONTEXT` with the field quoted and **write nothing**. This handoff has no valid work if P is false. A `DONE` returned on a falsified premise is the worst available outcome: a duplicate field added to a live telemetry path for no reason.

**Acceptance (all four must hold):**
1. `python -m pytest tests/ops/ -q` green, count strictly greater than the 52 baseline, **zero existing tests modified**.
2. `git diff --name-only` lists **only** `ops/c1_rail/c1_rail_http_server.py` and files under `tests/ops/`.
3. A `request_received` record produced from a well-formed B1 payload contains `parsed.close` and `parsed.stop_dist_pts` with the as-received values.
4. `python scripts/check_boundaries.py` clean.

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [pass/concern], 2.2 [...], 2.3 [...]
Diffs (files touched): <list>
Test count: <before> -> <after>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance.**
- [ ] Diff confined to `ops/c1_rail/c1_rail_http_server.py` + `tests/ops/*` — **no listener, no telemetry module**
- [ ] `make_request_received` unchanged
- [ ] No existing test modified
- [ ] `SCHEMA_VERSION` unchanged
- [ ] The three non-B1 `_emit_request` call sites still pass `parsed=None`

**Pass 2 — Quality.**
- [ ] `signal_type` in `parsed` is the classified value, not a raw echo
- [ ] No coercion/validation added to the two new fields
- [ ] Control flow of `_handle_post` byte-equivalent apart from the extracted call
- [ ] Secret-scan regression present and green

**Pass 3 — Integration (M1 sequencing).**
- [ ] Confirm the merge is sequenced **with** the M1 drills, not ahead of them — re-check `M1_MONITORING_ACCEPTANCE.json` still reads `CODE_LANDED` and decide with the operator whether this lands before or after `RESOLVED`.

---

## §10 — Audit hooks (runnable)

```bash
# 1. The gap this task closes: parsed currently omits the two price fields.
grep -n -A6 'parsed = {' ops/c1_rail/c1_rail_http_server.py
#   BEFORE: leg_id / signal_type / bar_time only.  AFTER: + close + stop_dist_pts

# 2. request_received IS emitted (four sites) — the corrected claim.
grep -n '_emit_request\|"request_received"' ops/c1_rail/c1_rail_http_server.py

# 3. The telemetry module must be untouched by this task.
git diff --name-only | grep -c 'c1_rail_telemetry.py'   # expect 0
git diff --name-only | grep -c 'c1_rail_listener.py'    # expect 0

# 4. B1 payload contract (the source of the two field names).
grep -n -A1 '_REQUIRED_PAYLOAD_FIELDS' ops/c1_rail/c1_sizing_host_reference.py

# 5. Baseline vs post test count.
python -m pytest tests/ops/test_c1_rail_http_server.py tests/ops/test_c1_rail_telemetry.py -q | tail -2
#   parent baseline 2026-07-24: 52 passed

# 6. M1 still mid-flight — merge sequencing check.
grep -n '"status"' docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json

# 7. §0 anchors still resolve.
git log -1 --format='%h %ci' -- ops/c1_rail/c1_rail_http_server.py   # expect ff3510d or later
```

---

## Verification (parent-side)

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/handoffs/2026-07-24-cursor-handoff-request-received-price-capture.md --type cc_handoff

git log -1 --format='%h %ci' -- ops/c1_rail/c1_rail_http_server.py      # ff3510d (origin/main)
git log -1 --format='%h %ci' -- ops/c1_rail/c1_rail_telemetry.py        # 54b1489
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py # c134060 (origin/main)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | **Revised after a Cursor `NEEDS_CONTEXT` bounce (dispatch #1) — both its findings verified correct by the parent.** (1) §0 told Cursor to read `RUNBOOK.md` §B7 Stage 2b, which exists only on an unmerged parent branch — `grep -c` on `origin/main` returns **0**. That §0 item is **removed** and its substance **inlined** in §1; the Q-COSTGEO-3 closure link (also absent from `origin/main`) is likewise de-referenced. A handoff dispatched to a worktree off `origin/main` may reference only what is on `origin/main`, or carry it inline. (2) The "four `_emit_request` call sites" claim was **wrong** — there are **three**, plus one *inline* `ledger.append` in the unauthorized path; corrected in §0 and §0.5(B). Parent's second factual error about this file's structure, both caught by gates rather than by the parent. | Joshua (direction) + Claude Code (Opus 4.8) |
| 2026-07-24 | **Re-anchored to `origin/main` before dispatch.** The authoring worktree was behind main; `ops/c1_rail/c1_rail_http_server.py` is `ff3510d` (not `54b1489`) and `ops/c1_rail/c1_sizing_host_reference.py` is `c134060` with moved line numbers. **Premise P re-verified against `origin/main`** — parsed dict byte-identical at L481-485, telemetry module unchanged, B1 contract unchanged; the only http_server delta is a one-line comment. Caught pre-dispatch; an unfixed version would have (correctly) bounced `NEEDS_CONTEXT` at Phase 0. | Joshua (direction) + Claude Code (Opus 4.8) |
| 2026-07-24 | Authored. Scope: widen the `request_received` `parsed` dict to carry `close` + `stop_dist_pts`, closing the B7 slippage-capture prerequisite. **Corrects the parent's own earlier mis-statement** (the defect is a missing dict field in `c1_rail_http_server`, not an unemitted event in `c1_rail_listener`) — correction carried in §1 and in the RUNBOOK note rather than silently overwritten. Dispatched to Cursor despite being under the ADR's overhead threshold, because M1 is `CODE_LANDED` and the parent declines to touch the live request path mid-acceptance. | Joshua (direction) + Claude Code (Opus 4.8) |
