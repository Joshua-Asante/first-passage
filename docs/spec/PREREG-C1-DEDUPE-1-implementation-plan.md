# C1-DEDUPE-1 Implementation Plan — one strategy intent, at most one venue order

> **For agentic workers:** REQUIRED SUB-SKILL — `superpowers:test-driven-development`
> (the planted defect must be demonstrated RED before the guard lands) plus
> `c1-rail` for the standing safety invariants. Steps use checkbox (`- [ ]`) syntax.
> **Do not deviate from the frozen predicate semantics in Task 3 without returning to
> the pre-reg author** — §5 of the spec forbids the two tempting variants.

**Goal:** Make the functional property mechanical: for a given intent key, **at most one**
venue order may reach `accepted`. Risk-add only (`entry`/`add`), never `exit`/`flat`.

**Architecture:** Additive and small — one canonical key derivation replacing two copies,
one ledger read helper, one pure predicate, one call site. No sizing arithmetic, no Pine,
no allocation, no `dd_protection` constant, no new dependency, no transport change. The
guard sits with the two existing risk-add policy gates (`ledger.risk_add_blocked`,
`arming_expiry_reason`) and returns their exact shape: a `halt` `SizingDecision` with
`qty_out=0, submit=False` and `RailAction(sent=False, transport_state="not_attempted")`.

**Tech Stack:** Python 3, pytest. `pyproject.toml` `pythonpath` puts `core/`, `lab/`, `ops/`
on the path (tests import `c1_rail_listener` bare). Boundaries by `scripts/check_boundaries.py`.

**Spec (authority — read first):** [`PREREG-C1-DEDUPE-1-intent-key-functional-property.md`](PREREG-C1-DEDUPE-1-intent-key-functional-property.md).
Where this plan and the spec disagree, **the spec wins**; report the divergence before executing.

**Testing model — TDD, adversarially.** The standing lesson is that discipline guards need
adversarial tests because a vacuous assert passes on an empty stream. So: **each of the eight
tests in Task 3 is written and shown FAILING against current `main` before the guard exists**
(the duplicate-refusal ones fail because nothing refuses; the allow-ones pass trivially and
are pinned as regression guards). Paste the RED output into the task. A guard whose tests were
only ever seen green is not accepted.

---

## Preconditions — BLOCKING, verify and paste evidence before Task 1

- [ ] **P1 — M1 `RESOLVED`.** `python -c "import json;print(json.load(open('docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json'))['status'])"` → must print `RESOLVED`. At plan-authoring time (2026-07-29) it printed `CODE_LANDED`. **If it still reads `CODE_LANDED`, STOP** — do not proceed, do not "start the harmless parts."
- [ ] **P2 — separate operator GO** for this packet, recorded in the session log. The pre-reg is not a GO.
- [ ] **P3 — rail confirmed DISARMED by a host read** (a repo-side grep does **not** establish this):

```bash
fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
```

Expect `dry_run=True`. On Windows this may exit 1 with "The handle is invalid." *after* printing correct output — judge by the printed line.

- [ ] **P4 — off-window, and after the 07-31 MYM session has landed.** Task 1 refactors the request path; the 07-31 session exists to prove that path carries a TV signal. Do not touch it before that lands. If a live/attended window is open, STOP.

---

## Sequencing

Task 1 → Task 2 are independent of each other and may run concurrently. Task 3 depends on
both. Tasks 4–5 are serial after 3. **Nothing deploys in this plan** — deploy is a separate
operator action gated on the §6 verdict.

---

### Task 0: Branch, baseline, and the two reads this plan deliberately does not prescribe

**Files:** none (verification + reporting only)

- [ ] **Step 1: Branch off a clean tree**

```bash
git status -sb && git switch -c claude/c1-dedupe-1-intent-key
```

- [ ] **Step 2: Baseline green, so any regression is attributable**

```bash
python -m pytest tests/ops/ tests/rail_crosstrade/ -q 2>&1 | tail -5
```

Record the pass/skip counts verbatim.

- [ ] **Step 3: Report the HTTP-adapter test shape BEFORE editing it (do not invent it)**

This plan intentionally does **not** prescribe the internals of
`tests/ops/test_c1_rail_http_server.py`, because the plan author did not read it. Read it and
report, in your Task 0 output: how the handler is exercised (real socket? handler class
instantiated directly? fake `rfile`/`wfile`?), and how a `request_received` ledger record is
observed. Task 3's parity test (T6) must follow **that** existing pattern.

- [ ] **Step 4: Confirm the two current key derivations, verbatim**

```bash
grep -nE -- "-\{signal_type\}-" ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_http_server.py
```

Expect exactly two formula sites: `c1_rail_listener.py:86` and `c1_rail_http_server.py:369`.
If there are now more or fewer, **stop and report** — the R1 premise has changed.

> **The pattern is deliberately form-agnostic, and this is a worked instance of trap M-AHF**
> (audit hooks tested against the author's mental form, not the artifact's storage form). The
> obvious pattern `leg_id\}-\{signal_type\}-` matches the listener and **silently misses the
> adapter**, because the adapter spells the dict access inline
> (`{payload['leg_id']}-...`, so the literal text is `leg_id']}-`). It would have reported
> "one formula site" and made R1 look already-done. Anchoring on `-{signal_type}-` — the one
> fragment both spellings share — catches both. Verified 2026-07-29.

---

### Task 1 [PARALLEL]: R1 — collapse two key derivations into one canonical function

**Files:** `ops/c1_rail/c1_rail_listener.py`, `ops/c1_rail/c1_rail_http_server.py`

**Why this is a precondition and not a cleanup:** a guard built on a key that can drift from
the key in the payload refuses real orders while passing duplicates. That is strictly worse
than no guard.

- [ ] **Step 1: Add the canonical derivation to `ops/c1_rail/c1_rail_listener.py`**, replacing `_order_id` (currently lines 84–86):

```python
def intent_key(payload: Mapping[str, Any], signal_type: str) -> str | None:
    """Canonical identity of one strategy intent — THE single derivation.

    Consumed by three call sites that MUST agree: the CrossTrade payload's
    order_id, the request_received telemetry event, and the duplicate-intent
    guard. Two independent copies of this formula (the pre-R1 state) is the
    hazard the guard cannot tolerate — see PREREG-C1-DEDUPE-1 §3 R1.

    Returns None when the payload lacks leg_id/bar_time; callers decide.
    """
    try:
        return f"{payload['leg_id']}-{signal_type}-{payload['bar_time']}"
    except (KeyError, TypeError):
        return None
```

Adopt the **None-returning** contract (the adapter's, not the listener's raising one) — it is
the safer of the two and both existing call sites already tolerate a None result.

- [ ] **Step 2: Repoint the listener's two call sites** (currently lines 183–188 and 252).

The line-186 site is already wrapped in `try/except (KeyError, TypeError)`; that wrapper
becomes dead and should go, since `intent_key` no longer raises. The line-252 site is strict
and sits after `payload["leg_id"]` has already been accessed at line 246 — it must now handle
`None` explicitly rather than assuming a string.

- [ ] **Step 3: Delete `_b1_order_id` from `ops/c1_rail/c1_rail_http_server.py`** (lines 367–372) and import the canonical function. Line 53 already reads:

```python
from c1_rail_listener import arming_expiry_reason, handle_signal  # noqa: E402
```

Extend it to `arming_expiry_reason, handle_signal, intent_key` and repoint the call site at
line 503. **Do not** re-add a local alias — an alias is how the second copy comes back.

- [ ] **Step 4: Boundaries + suite still green**

```bash
python scripts/check_boundaries.py && python -m pytest tests/ops/ tests/rail_crosstrade/ -q 2>&1 | tail -5
```

---

### Task 2 [PARALLEL]: the ledger read helper

**Files:** `ops/c1_rail/c1_rail_telemetry.py`, `tests/ops/test_c1_rail_telemetry.py`

No join by `order_id` exists anywhere in `ops/` today — this adds the first one. Place it
beside `find_records_for_event` (~line 624), which is the existing per-event join.

- [ ] **Step 1: Add the helper**

```python
def accepted_intent_keys(ledger: EventLedger) -> set[str]:
    """Intent keys (order_ids) whose transport_result recorded `accepted`.

    NOTE on the taxonomy: `accepted` means an HTTP response was received — it
    is NOT execution-verified, and it is NOT restricted to 2xx (see
    crosstrade_payload.send_to_crosstrade, which records `accepted` for any
    status). A first send that returned 500 therefore lands here, and will bar
    a re-send. That is deliberate: after a 500 nobody knows whether the order
    reached the venue, and blind re-sending into that uncertainty is exactly
    what the rail's no-auto-retry doctrine forbids.

    DRY_RUN sends record `not_attempted`, so dry-run replays never populate
    this set.
    """
    return {
        r["order_id"]
        for r in ledger.iter_records()
        if r.get("kind") == "transport_result"
        and r.get("transport_state") == "accepted"
        and isinstance(r.get("order_id"), str)
        and r["order_id"]
    }
```

- [ ] **Step 2: Tests** — a ledger with one accepted risk-add returns that key; a ledger with only `not_attempted`/`unknown` records returns empty; an **absent** ledger file returns empty without raising (`iter_records` early-returns when the path does not exist); a record with `order_id: null` is skipped rather than admitted as `None`.

---

### Task 3: the predicate, the wiring, and the eight adversarial tests

**Files:** `ops/c1_rail/c1_rail_listener.py`, `tests/ops/test_c1_rail_listener.py`, `tests/ops/test_c1_rail_http_server.py`

- [ ] **Step 1: Write all eight tests FIRST and paste the RED output.**

Follow the existing conventions in `tests/ops/test_c1_rail_listener.py`: the `host(tmp_path)`
fixture, `entry_payload(...)`, `_CapturingSender`, `_config(**overrides)`, `_armed_until()`.

**Build the "already accepted" state by running the rail, not by hand-writing the ledger.**
Call `handle_signal(...)` once with `ledger=` and a `_CapturingSender()` returning 200 — that
appends a genuine `transport_result` with `transport_state="accepted"` and the order_id — then
re-issue the *same* payload. A hand-crafted ledger record would only prove the guard agrees
with my assumptions about the record shape.

| # | Test | Plants / asserts |
|---|---|---|
| T1 | duplicate `entry`, identical key, after an `accepted` transport | **REFUSED**: `halt=True`, `submit=False`, `qty_out=0`, `sender.calls` unchanged, `payload_text is None`, `transport_state="not_attempted"` |
| T2 | duplicate `entry` after a **`failed`** transport | **ALLOWED.** ⚠ `send_to_crosstrade` never emits `failed` (any HTTP response → `accepted`; every exception → `unknown`), so this state cannot be produced through the real sender. Construct the `failed` ledger record directly and say so in a comment — the R3 clause is defensive, and this test pins it against a future sender that does emit `failed`. |
| T3 | duplicate `exit` and duplicate `flat` on an already-accepted key | **ALLOWED** — sender called. This is the invariant that keeps a position closable; it is the most dangerous thing to get wrong. |
| T4 | same leg + signal, **different** `bar_time` | ALLOWED |
| T5 | `entry` then `add` sharing one `bar_time` | ALLOWED (distinct `signal_type` ⇒ distinct keys) |
| T6 | key parity: the adapter's `request_received.order_id`, the `transport_result.order_id`, and the `order_id` inside the built CrossTrade payload text all equal `intent_key(payload, signal_type)` | Fails if a second derivation is ever reintroduced. Use the harness shape reported in Task 0 Step 3. |
| T7 | guard against an **absent** and an **empty** ledger, and `ledger=None` | No raise; signal proceeds normally |
| T8 | duplicate `entry` while **`dry_run=true`** | **REFUSED** — unlike `arming_expiry_reason`, this guard is *not* gated on `not dry_run`, so the disarmed replay in Task 4 is meaningful |

- [ ] **Step 2: Add the predicate to `ops/c1_rail/c1_rail_listener.py`**, beside `arming_expiry_reason`:

```python
def duplicate_intent_reason(key: str | None,
                            ledger: EventLedger | None) -> str | None:
    """Return a halt reason if this intent already reached the venue, else None.

    Functional property: one strategy intent -> at most one `accepted` venue
    order. CrossTrade `order_id` idempotency is DISPROVEN (2026-07-27 incident,
    RUNBOOK B7 arming log): a re-sent payload with an unchanged order_id
    executes as a BRAND-NEW order, so the refusal has to happen here.

    Only `accepted` bars a re-send:
      - `failed`        -> legitimately re-sendable (currently unreachable; see
                           accepted_intent_keys docstring)
      - `unknown`       -> already blocks ALL risk-add via block_risk_add and is
                           never auto-retried; needs no logic here
      - `not_attempted` -> nothing left the process

    Callers apply this to risk-add (entry/add) ONLY. Never to exit/flat: the
    rail's standing asymmetry is that a fault blocks risk-ADD and never
    risk-REDUCTION, and refusing a duplicate flatten could strand an open
    position with no path to close.
    """
    if ledger is None or key is None:
        return None
    if key in accepted_intent_keys(ledger):
        return (f"duplicate intent: {key} already reached "
                f"transport_state=accepted; refusing a second venue order "
                f"(venue order_id idempotency is disproven)")
    return None
```

Import `accepted_intent_keys` alongside the other `c1_rail_telemetry` names (listener lines 43–54).

- [ ] **Step 3: Wire it into `handle_signal`** — after the armed-window block (ends line 180)
and **before** `host.process_signal` (line 182), so a duplicate is never even sized:

```python
    if is_risk_add:
        dup_reason = duplicate_intent_reason(
            intent_key(payload, str(payload.get("signal_type", ""))), ledger)
        if dup_reason is not None:
            notifier.notify("WARNING", dup_reason, event_id=eid)
            decision = SizingDecision(
                leg_id=str(payload.get("leg_id", "<absent>")),
                signal_type=str(payload.get("signal_type", "<absent>")),
                qty_out=0, submit=False, halt=True, halt_reason=dup_reason,
            )
            return RailAction(decision=decision, sent=False, dry_run=dry_run,
                              event_id=eid, transport_state="not_attempted")
```

**Frozen semantics — do not "improve" these** (spec §5):
- `WARNING`, **not** `CRITICAL`, and **no** `ledger.block_risk_add(...)`. A stray duplicate is
  evidence about one intent, not about rail health; a sticky global block would convert a
  harmless refusal into a silent kill of the next legitimate add. Sticky+CRITICAL is reserved
  for `transport_unknown`, where the rail genuinely does not know what happened.
- **No `is_risk_add` inversion, no exit/flat coverage** (T3).
- Not gated on `dry_run` (T8).

- [ ] **Step 4: Green, and the RED→GREEN transition is visible**

```bash
python -m pytest tests/ops/ tests/rail_crosstrade/ -q 2>&1 | tail -5
python scripts/check_boundaries.py
```

Paste both the earlier RED output and this GREEN output in the task record.

---

### Task 4: disarmed replay — the §6 RESOLVED criterion

**Files:** none (operator-run, host-side)

- [ ] **Step 1: Confirm still disarmed** (P3 command). `dry_run=True`.
- [ ] **Step 2: POST one generated payload twice** — the second must be refused:

```bash
python docs/notes/rail_build/b4_dry_fire_payloads/make_payload.py mym entry > /tmp/dup.json
```

Note the deliberate irony: `make_payload.py` exists to guarantee a *fresh* tag, so to test the
guard you must reuse **one** generated payload for both POSTs. This is the only sanctioned
reason to POST the same body twice, it is valid **only** while `dry_run=true`, and the file
must be deleted afterward.

- [ ] **Step 3: Assert on the ledger, not on the HTTP response** — first POST records a
`decision` + `transport_result(not_attempted, dry_run=true)`; second records a `decision` with
`halt=True` and the duplicate-intent `halt_reason`, and **no payload built**. Then delete `/tmp/dup.json`.

---

### Task 5: record the verdict and close the loop

- [ ] **Step 1: Stamp the §6 verdict** in the pre-reg (`RESOLVED` / `FALSIFIED` / `AMBIGUOUS`
per its own criteria) with the evidence commands and their output. If R1 turned out to require
touching sizing-law or equity code, the verdict is **AMBIGUOUS** — stop and re-scope rather
than proceeding on a divergent key.

- [ ] **Step 2: Desk-card and RUNBOOK note.** The prose rule and the fresh-tag generator both
**stay** (spec §5, R6) — the static `b4_*.json` files remain re-fireable by hand and a code
guard on the rail does not license removing the guard on the desk. Add: "a duplicate risk-add
intent is now refused rail-side; this does not make re-POSTing a saved file safe."

- [ ] **Step 3: Update the STATE.md forward-trigger pointer** from pre-registered to landed,
and note that deploy remains a separate operator action.

- [ ] **Step 4: Final gate sweep**

```bash
python -m pytest tests/ops/ tests/rail_crosstrade/ -q 2>&1 | tail -5
python scripts/check_boundaries.py && python scripts/check_root_doc_liveness.py && python scripts/check_path_liveness.py
```

---

## Known residuals (state; do not silently fix inside this packet)

1. **Ledger-scoped memory.** The guard's knowledge is exactly as durable as the events JSONL on
   the Fly volume. No rotation exists today; if one is ever added, accepted keys age out and a
   stale-bar duplicate could pass. Out of scope here — flag it in the rotation change.
2. **O(n) scan per risk-add.** Trivial at session scale (single-digit events). An in-memory
   index of accepted keys is the follow-on if it ever matters, not part of this change.
3. **`failed` is unreachable today** (T2). `handle_signal`'s existing `if outcome.state ==
   "failed"` branch at line 317 is likewise dead. Noticed, not fixed — a separate question is
   whether `send_to_crosstrade` *should* distinguish a 4xx/5xx from a 2xx.
4. **`accepted` ≠ succeeded.** A first send that got any HTTP response, including 500, bars a
   re-send. Fail-safe-correct and deliberate, but it will surprise a reader who equates
   `accepted` with success — hence the docstring in Task 2.
