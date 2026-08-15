# ADR 2026-08-06 — Cap tripwire companion registration beside ORB PF-CUSUM seed

**Status:** `Accepted` — **operator Accept recorded 2026-08-06** (*"accept"*)
**Decision date:** 2026-08-06
**Authors:** Joshua (GO: companion registration; Accept) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`Q-CAPA-1` closure](../briefs/closures/Q-CAPA-1-closure-resolved.md) · Cap RESULTS [`mnq_capa_n14_tripwire_2026-08-06`](../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md) · N14 [`mnq_orb_flow_substrate_2026-08-05`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) · ORB decay seed [`RESULTS_decay_monitor.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) · [`ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md)
**Layer:** research-lifecycle monitoring disposition only. No strategy parameter, allocation, `dd_protection`, lifecycle code, Pine, or rail config is touched. **$0 / K=0** — Cap seat already spent on Cap-spend; this ADR opens no new Cap cell.

---

## §0 — Rule 0 reads (verified 2026-08-06)

| Source | Anchor | What it pins |
|---|---|---|
| [`ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) “Still gated” decay bullet | `92abdbb` | PF-CUSUM seed calibrated; not fired; ORB not in `lifecycle_state.json` / four-leg Call-1 |
| [`RESULTS_decay_monitor.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) | `92abdbb` | baseline PF **1.1691** / floor **1.0855** / `block_size=2`; seed posture; no action-on-breach below `AUTHORIZED` |
| [`Q-CAPA-1-closure-resolved.md`](../briefs/closures/Q-CAPA-1-closure-resolved.md) §3 + Iterate | `2433e5b` | Cap spent; tripwire candidate; wiring = separate GO; no auto-wire / gate / PROX / MBP-10 |
| N14 Iterate ([`RESULTS.md`](../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) §6) | `be6b94e` | Deliverable = watchlist + forward tripwire **candidate companion** to PF-CUSUM; wiring separate |
| Cap RESULTS / N16 | `2433e5b` | Forward `[t, t+60s)` mean signed `A` persists; Cap seat spent; FM-1 held |
| `core/lifecycle.py::STRATEGY_KEYS` | `4441c72` | ORB not in the four locked-leg frozenset — Call-1 harness hard-gates away from ORB |

---

## §1 — Context

Q-CAPA-1 Cap-spend `RESOLVED` and marked the MNQ Cap seat **spent** on a Route A cell that showed N14’s against-break L1 tilt **intensifies** in the 60 s after the ORB touch. Cap’s Iterate left the tripwire as a **candidate** and named a separate wiring GO — explicitly not auto-wire, not an entry filter, not live-monitor auth.

ORB-MNQ-1 already carries a Stage-6d **PF-CUSUM decay-monitor seed** (Tradeify economics, 2021+). That seed fires only on **realized P&L** and therefore only *after* decay is paid. N14/Cap named the missing piece: a **pre-P&L structural companion** at the trigger boundary. ORB is re-PARKED; the rail is research-only; no live ORB fill stream exists.

**Decision driver:** Cap’s INTEGRATE fork is open until the companion is either registered or explicitly left watchlist-only — without inventing lifecycle coupling the Cap stop rule forbade.

---

## §2 — Decision

**Decision:** On Accept, register Cap-spend forward L1 asymmetry `A` as a **named companion observable** beside ORB-MNQ-1’s PF-CUSUM decay-monitor seed — **docs registration only**.

### Frozen pins

| Pin | Content |
|---|---|
| **Observable** | Cap-spend construct: mean signed L1 `A` on **`[t, t+60s)`** at the N14 ORB trigger set vs the same ToD-matched controls. N16 numbers evidence persistence; they are **not** re-run by this ADR. |
| **Role vs PF-CUSUM** | **Pre-P&L structural companion.** PF seed = post-realized-P&L decay floor. `A_fwd` = named pre-P&L watch observable that seed lacked. |
| **Standing** | **Registered companion** — watchlist-grade. Evaluation owed when a live ORB fill stream exists (or on unpark + separate GO). **Not armed today.** |
| **Fire thresholds** | **Deferred.** This ADR does **not** invent operational breach levels, demotion mapping, auto-alerts, or Call-1 interlock. |
| **Cap / K / $** | Cap seat already **spent** on Cap-spend. This ADR spends **$0 / K=0** and opens **no** new Cap cell. Fresh Cap-seat discovery needs a fresh reservation. |
| **Code / lifecycle** | **No** runner, **no** `lifecycle_state.json` write, **no** `core/lifecycle.py` change, **no** Pine / rail / allocation / `dd_protection` change. |

**Effective:** immediately upon Accept (2026-08-06).
**Scope:** ORB-MNQ-1 research-lifecycle monitoring documentation and instrument-ledger disposition language. Does not unpark ORB, reopen payability, or authorize live spend.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Leave candidate forever** (no registration) | Cap Iterate’s INTEGRATE is unpaid; PF seed still lacks a named pre-P&L companion; “wiring GO separate” would stay permanently open |
| **Research harness** (offline `A_fwd` runner beside PF seed) | Useful later; not required to discharge Cap’s wiring fork; invents a second artifact class Cap did not demand |
| **Lifecycle coupling** (tripwire → Call-1 / demotion) | Cap stop rule + ADMISSION: ORB outside `STRATEGY_KEYS`; no action-on-breach below `AUTHORIZED`; no live fills — would invent authority Cap forbade |
| **Entry / fifth-gate conversion** | F2 GUARD + Cap FM-1 / FM-6 — outcome-free measurement must not become a filter without a new K-bound PREREG + GO |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, every mirror that speaks Cap-tripwire / PF-CUSUM companion standing correctly describes a **registered, not live-wired** companion, and Cap seat remains disclosed as **spent**.

**Revert trigger (either limb):**
1. **Authority creep:** any Accept-era artifact claims the tripwire is wired into Call-1 demotion, entry filtering, or auto-arming — → superseding ADR withdrawing registration; offending claim DEAD-listed.
2. **Cap restatement:** any Accept-era hot surface restates the MNQ Cap seat as **unspent** because of this registration — → supersede; Cap-spend closure remains canonical for seat status.

**Trigger check schedule:** next ORB unpark GO, or 2026-11-08 programme audit if unpark has not fired — confirm mirrors still say registered-not-wired.

---

## §5 — Forbidden moves

- Treating registration as **live monitor authorization** or Cap-spent as arming.
- Converting `A_fwd` into an **ORB entry filter / fifth conditioning gate** without a new K-bound PREREG + GO.
- **Lifecycle write** or extending Call-1 harness / `STRATEGY_KEYS` to ORB under cover of this ADR.
- **Outcome joins**, PROX reopen, MBP-10 escalation, horizon retune, or a second Cap cell “because companion exists.”
- Inventing **operational fire thresholds** or demotion mapping in this ADR.
- Restating Cap Δ / PF floors as owned values here — **link** Cap RESULTS / decay RESULTS; do not duplicate.

---

## §6 — Consequences

- Cap’s separate wiring GO is **discharged as docs-only companion registration** (this ADR).
- Tripwire standing flips: **candidate → registered companion** (still not live).
- PF-CUSUM seed unchanged; still a seed, not a fired monitor.
- ORB re-PARKED / payability FALSIFIED unchanged.
- Fresh Cap-seat discovery still needs a **fresh reservation**.

---

## §7 — Audit hooks

```bash
# ADR present and Proposed/Accepted
rg -n "Registered companion|Fire thresholds|\\$0 / K=0" docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md

# Mirrors point here; must not claim live wire
rg -n "companion registration|registered companion" \
  lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md \
  lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md \
  ops/instruments/MNQ.md

# Must NOT claim demotion / entry filter as authorized by this ADR
rg -n "auto-wire|demot|entry filter|fifth gate" docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md

# Cap seat still spent (canonical: Cap closure / N16 — not this ADR)
rg -n "Cap seat.*spent|Cap seat SPENT" ops/instruments/MNQ.md docs/briefs/closures/Q-CAPA-1-closure-resolved.md
```

---

## Amendment log

- **2026-08-06 — Authored `Proposed`.** Operator wiring GO chose docs-only companion registration (not harness, not lifecycle coupling).
- **2026-08-06 — Operator Accept** (*"accept"*). Status `Proposed` → `Accepted`. Mirror “Proposed until Accept” pointers flipped same change.
