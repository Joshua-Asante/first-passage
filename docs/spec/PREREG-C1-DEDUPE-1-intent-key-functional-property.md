# PREREG-C1-DEDUPE-1 — One strategy intent, at most one venue order

**Type:** Change pre-registration (design + falsifier frozen BEFORE implementation).
**Status:** PRE-REGISTERED / **GATED on M1 `RESOLVED` + a separate operator GO**. Not scheduled; not in the OPERATOR QUEUE.
**Authored:** 2026-07-29. **Surface:** c1 rail transport layer (`ops/`). Touches **no** Pine parameter, no sizing law, no allocation, no `dd_protection` constant.
**Provenance of the idea:** external methodology source (F. Coyle, *Why Agentic Systems Need Ontologies*, AI Engineer 2026) supplied the **name** for a constraint class — a *functional property*: an entity that may hold at most one of something. The incident this pre-reg addresses is entirely in-repo and predates the source.

> **Do not implement inside a live or armed window.** The rail is the operation's only live execution surface; this change sits on the request path. Implementation happens on a disarmed rail, off-window, behind the §6 gate.

**Execution packet (frozen 2026-07-29):** [`PREREG-C1-DEDUPE-1-implementation-plan.md`](PREREG-C1-DEDUPE-1-implementation-plan.md) — five tasks, eight adversarial tests, blocking preconditions. This document remains the authority; where the plan disagrees with it, this file wins.

---

## §0 — Rule-0 production reads (verified this session, 2026-07-29)

| Source | What it grounds | Anchor |
|---|---|---|
| `ops/c1_rail/c1_rail_listener.py` L84–86 `_order_id()` | The rail **already derives a deterministic intent key**: `f"{leg_id}-{signal_type}-{bar_time}"`. Nothing consumes it as an identity. | `5fa31b5` 2026-07-27 16:57 -0400 |
| `ops/c1_rail/c1_rail_listener.py` L158–166 (`ledger.risk_add_blocked`) + L168–180 (`arming_expiry_reason`) | **The precedent shape this change must copy**: a policy gate that fires before `host.process_signal`, returns a `halt` `SizingDecision` with `qty_out=0, submit=False`, and `RailAction(sent=False, transport_state="not_attempted")`. Both are risk-add-scoped. | same |
| `ops/c1_rail/c1_rail_http_server.py` L367–372 `_b1_order_id()` | A **second, independent copy** of the same key formula (used for the `request_received` event). Two derivations of one identity = drift hazard; see §3 requirement R1. | `5fa31b5` 2026-07-27 16:57 -0400 |
| `ops/c1_rail/c1_rail_telemetry.py` — `EventLedger`, `TRANSPORT_STATES`, `find_records_for_event` | Append-only JSONL; **every** record carries `order_id`; the only join helper is by `event_id`. `TRANSPORT_STATES = {not_attempted, accepted, failed, unknown}`. | `b949642` 2026-07-27 16:21 -0400 |
| `grep -rnE "order_id" ops/*.py` | **No join by `order_id` exists anywhere.** `ops/c1_rail/c1_rail_slippage.py` reads it per-event only. The identity is recorded and never queried. | run 2026-07-29 |
| `ops/c1_rail/c1_sizing_host_reference.py` L278–305 (`entry`) / L307–311 (`add`) | **Why the confirmed-base interlock does not cover this.** The `entry` path never consults `open_leg_state`; L297–298 states the rule outright ("Intended qty is NOT executed base — confirm_executed_base only after broker evidence"). The `add` path halts without a *broker-confirmed* base — so a pre-attestation duplicate `add` fail-safes, but a post-attestation one re-sizes and re-submits. Neither path is a duplicate-intent guard. | read 2026-07-29 |
| `docs/notes/rail_build/b4_dry_fire_payloads/make_payload.py` docstring | The dated incident + the current fix: "CrossTrade `order_id` idempotency is DISPROVEN … an unmodified `b4_mym_entry.json` was POSTed a second time and filled a second unintended 8-lot position." | `b949642` 2026-07-27 16:21 -0400 |
| `docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-31.md` L194 | The constraint's **current** enforcement: prose. "never re-POST a saved file." | read 2026-07-29 |

**Falsifier source (Tier 2 — categorical claim, not a numeric simulation input; per brief-authoring §0 citation-tier rule):**

| `core/strategies/striker/LOCK.md:55` | DJ30/MYM: `pyramid trigger 1.29×ATR / size 750% / **minBars 6**` |
| `core/strategies/nas/LOCK.md:50` | NAS100/MNQ: `pyramid trigger 1.10×ATR / size 1000% / **minBars 6**` |

Pine source is gitignored (`**/*.pine`); LOCK.md is the version-anchored Tier-2 substitute, and the claim it grounds is categorical (minimum bar separation exists), not numeric.

---

## §1 — Context

On **2026-07-27** a re-POSTed B4 payload with an unchanged `bar_time` placed a **second live order** and filled an unintended 8-lot position (+$[redacted] realized on the session, one fill of which was unintended; `RUNBOOK.md` B7 arming log). The venue does **not** deduplicate: `order_id` idempotency is DISPROVEN.

The fix shipped that day was correct for its scope and is **not** what this pre-reg revisits: `make_payload.py` now stamps a **fresh** `bar_time` per invocation, so the static `b4_*.json` files cannot be re-fired into a collision. Note precisely what that does — for SIM traffic it makes each payload a *distinct intent*, which is the right semantics for a test harness. It **removes the collision rather than refusing it**, and it governs only the hand-POST path.

What remains unguarded is the general case: **any** repeat of an already-transported intent — an operator re-fire of a real alert, a TradingView duplicate webhook, a retry after an ambiguous response. For those, `bar_time` is the genuine bar timestamp, so the derived key collides, and nothing refuses the second order. The constraint lives in operator discipline (`B7_STAGE1_DESK_CARD:194`) and in a generator that only covers SIM payloads.

This is the repo's own recurring shape, named in memory as the enforcement ladder: *convention → documented rule → checker → impossible-by-construction*. The rail's best guards sit at the top (long-only-by-construction clears the venue hedging rule; `armed_until` fail-safes to EXPIRED on every malformed value). This constraint sits at rung two.

---

## §2 — Question (symptom, no fix baked in)

One strategy intent can reach the venue as two live orders, and the rail cannot tell that it happened. Stated as symptom only: *the rail computes a stable identity for every signal it processes, records that identity on every ledger event, and never asks whether it has already sent that identity to the venue.* The venue will not answer the question either — its idempotency is disproven. The one dated instance cost an unintended 8-lot position on a live eval account.

---

## §3 — The constraint, and its requirements

**Constraint (functional property):** for a given intent key, **at most one** venue order may reach `accepted`.

**Intent key:** `(leg_id, signal_type, bar_time)` — the tuple the rail already derives twice.

**R1 — One canonical derivation.** The two existing copies (`c1_rail_listener._order_id`, `c1_rail_http_server._b1_order_id`) must be replaced by a single shared function before any check consumes it. **A dedupe gate built on a key that can drift from the key in the payload is worse than no gate** — it would refuse real orders while passing duplicates. R1 is a precondition, not a cleanup.

**R2 — Scope: risk-add only** (`entry`, `add`). Never `exit`/`flat`. This preserves the rail's standing asymmetry — a fault blocks risk-*add*, never risk-*reduction*. Identical scoping to `arming_expiry_reason` (`c1_rail_listener.py:106–109`) and to `ledger.risk_add_blocked`.

**R3 — Prior-state predicate.** Refuse when a prior `transport_result` for this intent key recorded state `accepted`. Do **not** refuse on `not_attempted` or `failed` — a genuinely failed send is legitimately re-sendable, and refusing it would strand a real signal. `unknown` needs no new logic: it already blocks all risk-add globally via `block_risk_add` and must never be auto-retried.

**R4 — Per-signal refusal, not a sticky global block.** Refuse *this* signal, notify `WARNING`, leave the rail able to serve the next legitimate bar. Considered and rejected: routing duplicates through `ledger.block_risk_add` (sticky, operator-repair-only). A stray duplicate is evidence about one intent, not about rail health; a sticky block would convert a harmless refusal into a silent kill of the next real add. `CRITICAL` + sticky is reserved for `transport_unknown`, where the rail genuinely does not know what happened.

**R5 — Placement.** A pure predicate in `ops/c1_rail/c1_rail_listener.py` alongside `arming_expiry_reason`, called in `handle_signal` before `host.process_signal`, in the same region as the two existing policy gates. Ledger scan is `O(n)` per risk-add over a session-scale stream (single-digit events per session); that cost is stated, not hidden. If it ever matters, an in-memory index of accepted keys is the follow-on — not part of this change.

**R6 — Defense in depth.** The prose rule and the fresh-tag generator both **stay**. The static `b4_*.json` files still exist and remain re-fireable by hand; a code guard on the rail does not license removing the guard on the desk.

---

## §4 — Hypothesis (falsifiable) — and its cheap falsifier, run BEFORE authoring

**H-C1-DEDUPE-1:**
> The intent key `(leg_id, signal_type, bar_time)` is **collision-free for all legitimate traffic**. IF no two legitimate risk-add signals on one leg can share a `bar_time`, THEN refusing a repeat of an already-`accepted` key cannot suppress a real trade, and the constraint is safe to enforce mechanically. IF any legitimate risk-add pair *can* share the tuple, THEN the key is wrong, a naive guard would suppress real orders, and this design is **FALSIFIED** — the key would need a sequence component, which is a different and much more invasive change.

**Result: falsifier RUN and PASSED, 2026-07-29, before this document was authored.**

Both venue legs enforce a **minimum 6-bar separation** between pyramid adds (`striker/LOCK.md:55`, `nas/LOCK.md:50` — `minBars 6`). On the 15m signal timeframe that is a 90-minute floor between consecutive adds on a leg. `entry` and `add` are distinct `signal_type` values and therefore distinct keys, so an entry and its first add never collide either. **No legitimate risk-add pair can share the tuple.**

This is why the check is admissible: the one way it could have broken real trading is closed by the locked strategies' own construction, established by citation rather than by argument.

**Residual, stated honestly:** the falsifier is grounded in a Tier-2 citation of a gitignored Pine source. If a future venue edition were ever authored without `minBars`, H-C1-DEDUPE-1 would need re-checking. §10 carries the audit hook.

---

## §5 — Forbidden moves

- **Do not extend the refusal to `exit`/`flat`.** It inverts the rail's core asymmetry and can strand an open position with no path to close. This is the single most tempting "for consistency" move here and it is the dangerous one.
- **Do not route duplicates through the sticky global `block_risk_add`.** See R4.
- **Do not treat fresh-`bar_time` stamping as the general mechanism.** It is the correct SIM-harness fix and the wrong rail invariant: it makes duplicates *unrepresentable in tests* while leaving them *unrefused in production*.
- **Do not retire the prose rule or the generator when the code lands** (R6).
- **Do not implement before M1 `RESOLVED`**, and do not touch the request path inside an attended window. M1 is `CODE_LANDED`, not `RESOLVED` (`M1_MONITORING_ACCEPTANCE.json`), and item 1 of the OPERATOR QUEUE blocks everything downstream.
- **Do not let this change grow into "rail hardening."** One constraint, one predicate, one shared key derivation. Anything else is a separate packet.
- **Do not claim the 07-27 incident is "fixed" by this change.** It was already mitigated for its own path; this generalizes the guard. Overstating it would misrepresent the incident record.

---

## §6 — Gate (binary)

**Preconditions (all required before implementation starts):**
1. M1 `status` = `RESOLVED` in `M1_MONITORING_ACCEPTANCE.json` (currently `CODE_LANDED`).
2. A separate operator GO for this packet.
3. Rail confirmed **disarmed** by a host read (`fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"` → `dry_run=True`). A repo-side grep does **not** establish this.

**Adversarial tests are part of the deliverable, not a follow-up.** Per the standing lesson that discipline guards need adversarial tests — a vacuous assert passes on an empty stream — the test set must include **planted defects that the guard is required to catch**, each demonstrated failing before the guard lands:
- duplicate `entry` with identical key after an `accepted` transport → refused, `submit=False`, `transport_state="not_attempted"`, no sender call;
- duplicate after a `failed` transport → **allowed** (R3);
- duplicate `exit`/`flat` → **allowed** (R2);
- distinct `bar_time`, same leg + signal → allowed;
- `entry` then `add` on the same `bar_time` → allowed (distinct keys);
- key derivation identical between listener and HTTP adapter (R1) — a test that fails if the two ever drift;
- guard runs on an empty / absent ledger without raising.

**Verdicts:**
- **RESOLVED** — R1–R6 implemented; the full planted-defect set passes; `pytest tests/ops/ tests/rail_crosstrade/ -q` green; a disarmed `dry_run=true` replay of a duplicated payload shows the refusal in the ledger with no payload built.
- **FALSIFIED** — the §4 falsifier fails on re-check (a legitimate same-key risk-add pair exists). Close this pre-reg; do **not** patch the key to rescue the design. Re-scope as a fresh question.
- **AMBIGUOUS** — R1 cannot be done without touching sizing-law or equity code. Stop: the change has outgrown its scope. Close and re-scope rather than proceeding on a divergent key.

---

## §7 — What this is not

Not an idempotency layer (the venue's is disproven and cannot be fixed from here). Not a retry mechanism — it never re-sends anything. Not a reconciliation change: the six M1 verdicts, the confirmed-base interlock, and the evidence overlay are untouched. Not a substitute for attended operation. It refuses one thing, in one place, on one signal class.

---

## §10 — Audit hooks (runnable)

```bash
# The key derivation — must be ONE function after R1, not two (this is the R1 assert).
# Pattern is form-agnostic ON PURPOSE (trap M-AHF): `leg_id\}-\{signal_type\}-` matches the
# listener but MISSES the adapter, which spells the access inline as `{payload['leg_id']}-`.
# `-{signal_type}-` is the fragment both spellings share. Pre-R1 this returns exactly 2 sites.
grep -nE -- "-\{signal_type\}-" ops/c1_rail/c1_rail_listener.py ops/c1_rail/c1_rail_http_server.py
grep -rnE "_order_id|_b1_order_id|intent_key" ops/*.py

# Falsifier re-check — both legs must still declare a minBars floor between adds.
# If either line loses minBars, H-C1-DEDUPE-1 must be re-verified before trusting the guard:
grep -nE "pyramid trigger .* minBars" core/strategies/striker/LOCK.md core/strategies/nas/LOCK.md
# expect: striker minBars 6, nas minBars 6

# Gate precondition — M1 must read RESOLVED, not CODE_LANDED:
python -c "import json;print(json.load(open('docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json'))['status'])"

# Standing invariants this change must not disturb (risk-add-only scoping):
grep -nE "is_risk_add|risk_add_blocked|arming_expiry_reason" ops/c1_rail/c1_rail_listener.py

# Suite:
pytest tests/ops/ tests/rail_crosstrade/ -q
```

---

## §11 — Cross-references

- Incident record: [`RUNBOOK.md`](../notes/rail_build/RUNBOOK.md) §B7 arming log 2026-07-27 · [`make_payload.py`](../notes/rail_build/b4_dry_fire_payloads/make_payload.py) docstring · [`B7_STAGE1_DESK_CARD_2026-07-31.md`](../notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-31.md) §5.
- Gating ADR: [`2026-07-22-c1-venue-native-monitoring-maturity.md`](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) · acceptance [`M1_MONITORING_ACCEPTANCE.json`](../notes/rail_build/M1_MONITORING_ACCEPTANCE.json).
- Rail GO: [`2026-07-17-c1-rail-build-account-registration-go.md`](../adr/2026-07-17-c1-rail-build-account-registration-go.md) (attended-only, spend ceiling, arming = operator GO).
- Frozen sizing-host spec (untouched by this change): [`c1_nt8_sizing_host_impl.md`](c1_nt8_sizing_host_impl.md).
- Pre-reg lineage / shape: [`PREREG-NAS-ECR-1-live-edge-capture.md`](PREREG-NAS-ECR-1-live-edge-capture.md).
- Doctrine: `docs/methodology/lessons/methodology_lessons.md` (guards need adversarial tests; run the cheap falsifier before authoring).
