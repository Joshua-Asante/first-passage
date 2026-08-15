# ADR 2026-08-06 — Call-1 action-on-breach at `CANDIDATE` (operator review flag only)

**Status:** `Proposed` — awaiting operator Accept (not self-accepting)
**Decision date:** 2026-08-06
**Authors:** Joshua (packet GO: close governance gap first) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) Call 1 / Call 5 · [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) · ORB decay seed [`RESULTS_decay_monitor.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) · replay consumer [`RESULTS_decay_monitor_replay.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor_replay.md) · Cap companion [`2026-08-06-capa-tripwire-pfcusum-companion-registration.md`](2026-08-06-capa-tripwire-pfcusum-companion-registration.md) (orthogonal — forbids inventing demotion *under Cap registration*; this ADR is the separate Call-1 governance packet) · intermediate-rung Proposed [`2026-08-03-lifecycle-ladder-intermediate-rung.md`](2026-08-03-lifecycle-ladder-intermediate-rung.md) (orthogonal — WATCH-1H between WATCH-1 and WATCH-2; does not address below-AUTHORIZED)
**Layer:** methodology / authorization-axis Call-1 policy. No strategy parameter, allocation, `dd_protection`, Pine, Cap arming, or `STRATEGY_KEYS` extension.

---

## §0 — Rule 0 reads (verified 2026-08-06)

| Source | Anchor | What it pins |
|---|---|---|
| [`core/lifecycle.py`](../../core/lifecycle.py) `TIER_MULTIPLIER` / `_LADDER_ORDER` / `next_tier_down` / `autonomous_demote` / `STRATEGY_KEYS` | `4441c72` | Ladder starts at `AUTHORIZED`; `CANDIDATE` is not a coded tier; `next_tier_down("CANDIDATE")` / `autonomous_demote("CANDIDATE")` raise `ValueError`; ORB not in `STRATEGY_KEYS`; autonomous floor is WATCH-2 (Call 5) |
| [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) Call 1 + Call 5 | `546b00f` | Call-1 action from AUTHORIZED is de-risk → WATCH (never kill); Call 5: reversible demotions autonomous, WATCH-2→RETIRED operator GO |
| [`RESULTS_decay_monitor.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) §3 | working-tree + prior `9d8dffc` Cap Accept lineage | Standing interim posture: breach = operator-flagged review, not automatic tier-step, until a `strategy_lifecycle.md`-level decision closes the gap |
| [`ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) decay bullet | same | Gap named; replay emits `OPERATOR_REVIEW_FLAG` only |
| Cap companion ADR | `9d8dffc` | Cap registration forbids inventing demotion mapping *under Cap*; separate from this packet |
| Replay runner header / disposition | working-tree (sibling packet) | Research harness already emits `OPERATOR_REVIEW_FLAG` only; leaves governance gap to this ADR |

**Gitignore pre-flight:** no `.pine` read; authorization-axis policy only.

---

## §1 — Context

Call 1 ratifies a decay floor and a demotion path **starting at `AUTHORIZED`** (`AUTHORIZED → WATCH-1 → WATCH-2`, autonomous; `RETIRED` operator-gated). The narrative authorization axis also names `CANDIDATE` *before* `AUTHORIZED` ([`strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) axis table), but `core/lifecycle.py`'s coded ladder and multiplier table do **not** implement `CANDIDATE`. ORB-MNQ-1 sits at operator-admitted `CANDIDATE @ 1.00×` with a calibrated PF-CUSUM seed and a research replay that can emit breaches — so the monitor can fire while no reversible autonomous step exists below AUTHORIZED.

The decay RESULTS already recorded an interim posture (operator-flagged review, not automatic tier-step). Cap companion registration (`Accepted` 2026-08-06) correctly refused to invent demotion under Cap. The PF-CUSUM replay harness (sibling packet) correctly emits `OPERATOR_REVIEW_FLAG` only and leaves this gap to methodology. Closing the gap is now owed as a **lifecycle-owner decision**, not a per-candidate hack and not Cap arming.

**Decision driver:** a calibrated / replaying Call-1-shaped monitor on a `CANDIDATE` strategy needs a named action-on-breach before Cap arming or any Accept-era claim that demotion is defined below AUTHORIZED.

---

## §2 — Decision

**Decision:** On Accept, ratify that a Call-1 decay breach (or any research / seed consumer using the same Call-1 floor semantics) against a strategy whose authorization standing is **`CANDIDATE`** mandates **`OPERATOR_REVIEW_FLAG` only** — **no autonomous demotion**, **no invented ladder rung below `AUTHORIZED`**, and **`RETIRED` remains Call-5 operator GO**.

### Frozen pins

| Pin | Content |
|---|---|
| **Scope** | Methodology-wide for any strategy at `CANDIDATE` (ORB-MNQ-1 is the motivating instance, not a special case). Same rule applies to any authorization standing **outside** `core/lifecycle.py::_LADDER_ORDER` until a separate Accepted ADR admits that standing into the coded autonomous ladder. |
| **Mandated action** | Emit / record an **operator review flag** (canonical event name in research harnesses: `OPERATOR_REVIEW_FLAG`). Operator may then Hold, change admission standing, or Call-5 retire — those are operator acts, not automation. |
| **Forbidden autonomous step** | No `CANDIDATE → RETIRED` auto-step; no silent insert of `CANDIDATE` into `_LADDER_ORDER` / `TIER_MULTIPLIER`; no `autonomous_demote("CANDIDATE")` success path. |
| **Code posture on Accept** | **Docs-only.** Today's `ValueError` from `next_tier_down` / `autonomous_demote` on `CANDIDATE` **is** the hard-refuse that matches this rule. Accept does **not** require a code change. Optional later: a named refuse helper that raises the same class of error with an explicit message citing this ADR — still no demotion. |
| **Four-leg book** | Unchanged. Autonomous demotion among `AUTHORIZED` / `WATCH-*` / floor at `WATCH-2` stays as Call 5 already ratified. |
| **Cap / STRATEGY_KEYS / ORB** | **No** Cap fire thresholds, **no** Cap arming, **no** extending `STRATEGY_KEYS` to ORB, **no** `lifecycle_state.json` writes for ORB under this ADR. |

**Effective:** immediately upon operator Accept.
**Scope:** authorization-axis Call-1 action-on-breach policy below AUTHORIZED / at `CANDIDATE`. Does not unpark ORB, reopen payability, arm Cap, or change PF floors (link owners; do not restate).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Autonomous `CANDIDATE → RETIRED`** | Call 5: retirement is irreversible and operator-gated. Auto-kill from the first below-AUTHORIZED standing collapses the reversible/irreversible split. |
| **Invent a coded `CANDIDATE` rung + demote into WATCH-*** | Would silently extend `_LADDER_ORDER` / multipliers without a ladder-shape ADR; confuses admission standing with live AUTHORIZED→WATCH de-risk; Cap and decay RESULTS both forbade inventing mapping under pressure. The Proposed WATCH-1H ADR is a different granularity question *inside* the live ladder — not a template for inventing below-AUTHORIZED rungs here. |
| **Leave gap open indefinitely** | Replay already dry-fires flags; Cap companion packet is next. An unnamed gap invites per-candidate invention or silent demotion under a later wiring GO. |
| **Per-ORB special case only** | Gap is Call-1 / Call-5 methodology shape, not ORB-specific. ORB is the first consumer; the rule must be lifecycle-owner scope. |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, every hot mirror that speaks Call-1 action-on-breach for `CANDIDATE` describes **operator review flag only**, and no Accept-era code path autonomously demotes or retires from `CANDIDATE`.

**Falsifier / revert trigger (either limb — H is falsified if either fires):**
1. **Authority creep:** any Accept-era harness or live path writes a lifecycle demotion / `RETIRED` from `CANDIDATE` without a superseding Accepted ADR — → superseding ADR; offending path DEAD-listed.
2. **Rule replaced:** operator Accepts a different below-AUTHORIZED autonomous mapping (new rung or auto-retire) — → superseding ADR stating that rule; this ADR's Status becomes `Superseded`.

**Revert action:** author a superseding ADR (full or in-part); never silently edit §2 pins in place (Trap #12).

**Trigger check schedule:** Cap companion arming GO (packet 3), any ORB unpark GO, and 2026-11-08 programme audit if still open.

---

## §5 — Forbidden moves

- Treating this ADR (even after Accept) as license to **extend `STRATEGY_KEYS` to ORB** or write `lifecycle_state.json` for ORB.
- **Arming Cap** or inventing Cap fire thresholds under cover of closing this gap (Cap companion ADR owns that packet).
- Rewriting the PF-CUSUM **replay runner into demotion** — sibling harness posture stays `OPERATOR_REVIEW_FLAG` only; link, do not absorb.
- Restating PF floors / Cap Δ as owned values here — **link** decay RESULTS / Cap RESULTS.
- **Silently amending §4** if a future wiring session finds the rule inconvenient — supersede instead.
- Landing Accept-era code that makes `autonomous_demote("CANDIDATE")` return a tier without a superseding ADR.

---

## §6 — Consequences

**Positive:**
- Closes the named open design gap with a lifecycle-owner rule consistent with Call 5 and the decay RESULTS interim posture.
- Aligns Cap companion (no demotion invent under Cap) and the replay harness (`OPERATOR_REVIEW_FLAG` only) under one Acceptable governance sentence.
- Keeps RETIRED irreversible and operator-gated.

**Negative (real):**
- A `CANDIDATE` breach does not automatically reduce size — operator must act. For research-only / re-PARKED ORB this cost is near-zero today; it becomes operational when a live fill stream exists.
- `CANDIDATE` remains outside the coded multiplier ladder — intentional; admission standing ≠ WATCH de-risk.

**Risks:**
- Operators may treat repeated review flags as noise. Mitigation: flags stay auditable events; Cap arming and unpark GOs re-read them.

**Downstream artifacts needing update (Proposed-era pointers; flip language on Accept):**
- [`RESULTS_decay_monitor.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor.md) §3 — gap → this ADR
- [`ADMISSION.md`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) decay bullet
- [`RESULTS_decay_monitor_replay.md`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_decay_monitor_replay.md) disposition
- [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) — Call 1 / Call 5 pointer
- [`core/strategies/_archive/orb/orb_mnq_v0_1_CANDIDATE.md`](../../core/strategies/_archive/orb/orb_mnq_v0_1_CANDIDATE.md) checklist line
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate
- Cap companion ADR body — **leave historical** (§0/§3 cited the open gap at registration time); no reverse edge owed

---

## §7 — Implementation plan

- **Phase 0** — re-verify §0; confirm `core/lifecycle.py` still raises on `CANDIDATE` demote APIs and ORB ∉ `STRATEGY_KEYS`.
- **Phase 1 (this packet, Proposed)** — land this ADR + mirror pointers; **no code change**.
- **Phase 2** — blast-radius grep for `action-on-breach below` / `Open design gap` / `no defined action-on-breach`; disposition every hit.
- **Phase 3** — on operator Accept: flip Status token; refresh mirrors from "Proposed awaiting Accept" → "Accepted / in force"; optional refuse-helper only if a later wiring packet needs a clearer error string — still no demotion.
- **Policy only for Proposed** — no mechanical code edits required to hold the rule.

---

## §10 — Audit hooks (runnable)

```bash
# 1. This ADR still Proposed or Accepted as claimed
rg -n "^\*\*Status:\*\*" docs/adr/2026-08-06-candidate-call1-action-on-breach.md

# 2. Coded ladder still starts at AUTHORIZED; CANDIDATE absent from multipliers
rg -n "_LADDER_ORDER|TIER_MULTIPLIER|CANDIDATE" core/lifecycle.py

# 3. Demote APIs still refuse unknown / non-ladder tiers (incl. CANDIDATE)
python -c "from core.lifecycle import next_tier_down, autonomous_demote
for fn in (next_tier_down, autonomous_demote):
    try:
        fn('CANDIDATE'); raise SystemExit('VIOLATION: demote accepted CANDIDATE')
    except ValueError:
        pass
print('OK: CANDIDATE hard-refuse')"

# 4. Hot mirrors point at this ADR (not "open gap" as unresolved)
rg -n "action-on-breach|Open design gap|candidate-call1-action-on-breach" \
  lab/analysis/orb/orb_mnq_2026-07/ docs/methodology/strategy_lifecycle.md \
  core/strategies/_archive/orb/

# 5. Replay harness still flag-only (sibling packet — no demotion rewrite)
rg -n "OPERATOR_REVIEW_FLAG|autonomous_demote|lifecycle_state" \
  lab/analysis/orb/orb_mnq_2026-07/run_decay_monitor_replay.py

# 6. INDEX sync
python scripts/check_adr_graph.py
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-06-candidate-call1-action-on-breach.md --type adr
# Expected: discipline checks PASS

python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
# Expected: exit 0; this slug listed Proposed

git log -1 --format="%h %ci" -- core/lifecycle.py
# Expected: 4441c72 (no Accept-era code change in this packet)
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-06 | Initial authoring — `Proposed`, awaiting operator Accept | Joshua + Cursor |
