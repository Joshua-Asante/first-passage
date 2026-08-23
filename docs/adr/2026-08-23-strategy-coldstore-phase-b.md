# ADR 2026-08-23 — Admit Phase B strategy cold-store (authorization-axis disposition)

**Status:** `Accepted` — operator GO 2026-08-23: restore design then execute Phase B Tasks 2+ (design body unrestored; Approach 2 + Phase A inventory used; Approach 3 not invented)
**Decision date:** 2026-08-23
**Supersedes:** `2026-08-04-strategy-coldstore-phase-a.md` in part — Phase B is now GO’d; this ADR is that GO + the disposition table
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (operator GO) + Cursor Cloud Agent
**Related:** [`2026-08-04-strategy-coldstore-phase-a.md`](2026-08-04-strategy-coldstore-phase-a.md) (filesystem only) · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) (Striker stays `AUTHORIZED · MECHANISM @ 1.00×`) · [`2026-08-05-strategy-venue-binding-axis.md`](2026-08-05-strategy-venue-binding-axis.md) (edition `WITHDRAWN` ≠ book `RETIRED`) · [Phase B plan](../superpowers/plans/2026-08-23-coldstore-phase-b-implementation.md) · [retrieve note](../notes/2026-08-23-coldstore-phase-b-prego-blocked.md)
**Layer:** authorization axis (lifecycle disposition). **No** `BASE_RISK`, `LEG_MAP`, Pine-parameter, or `lifecycle_state.json` write.
**Tier:** full — doctrine limb (catalog disposition ≠ authorization write).

---

## §0 — Rule 0 reads (production-source verification)

All read 2026-08-23 **before** authoring (anchors = `git log -1 --oneline -- <path>` on `origin/main` `ea0850f`):

| Source | Anchor | What it grounds |
|---|---|---|
| `core/lifecycle.py` `STRATEGY_KEYS` / `TIER_MULTIPLIER` / `STATE_FILE` | `027a729` | Absent `lifecycle_state.json` ⇒ all `AUTHORIZED` @ 1.00×. Ladder pinned. Four-leg authorization book. |
| `core/dd_protection.py` `BASE_RISK` / `DD_SCALE` / `DD_TRIGGER` | `027a729` | Living keys still include Guardian / Aegis — Phase C owns that delete. This ADR must not touch them. |
| `core/firm_rules.py` `_BASE_RISK` | `027a729` | Canonical living slug dict. Untouched here. |
| `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` | `027a729` | Striker rows stay. F2 owns rail teardown. |
| Phase A ADR frozen inventory + Approach 2 | `1f855b6` | Design spec body unrestored. Approach 2 already elected. Approach 3 rejected in Phase A §3. |
| Venue-binding registry | living | Edition `WITHDRAWN` is not a book `RETIRED`. |

**Retrieve re-attempt (this session, before Tasks 2+):** `git show pre-prune-2026-08-08:docs/superpowers/specs/2026-08-04-strategy-coldstore-retirement-design.md` still `fatal: invalid object name`. `git clone` / `gh api` of `Joshua-Asante/first-passage-archive` still 404 / not resolvable. Path absent in this clone’s history. **Spec body not recovered.** Disposition table below is copied from Phase A’s frozen inventory (Approach 2), not from an invented Approach 3 schema.

**Amendment-first:** Phase A can hold a pointer addendum; it cannot hold B authority (Phase A §5). New file required.

**Catalog attestation (sub-rule 8; literal grep, not `repo_retrieve.py`):** `rg -n -i 'coldstore\|event.study\|detector.kit\|call1.oc' lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md` → **empty**. No prior lab slug or rejected-candidate entry owns this disposition.

---

## §1 — Context

Phase A cold-stored unused Pine and lock bodies. Catalog labels (`VENUE_LESS_CFD`, `VENUE_WITHDRAWN`, `PARKED_PROTOTYPE`, `FALSIFIED_PARKED`) are discoverability only. After Tradeify de-scope, agents still risk reading `VENUE_WITHDRAWN` as lifecycle `RETIRED` for Striker — the failure Phase A §4 T3 named.

The operator GO’d Phase B Tasks 2+ on 2026-08-23 and asked to restore the pruned design first. Restore failed. Phase A already elected Approach 2 and rejected Approach 3 (hard delete + offline vault). This ADR records B without inventing a third schema.

**Decision driver (one sentence):** catalog dispositions must be bound to an explicit authorization-axis action (almost always **none**) so venue-fit cannot be collapsed into book decay.

---

## §2 — Decision

**Decision:** Record the authorization-axis consequence of every Phase A catalog row as **no lifecycle write**. Striker (both books) stays `AUTHORIZED · MECHANISM @ 1.00×`. Do **not** create or edit `lifecycle_state.json`. Do **not** write `RETIRED` / `WATCH-*` for any catalog class. Edition `WITHDRAWN` stays on the venue-binding registry.

**Effective:** immediately upon acceptance (this GO).
**Scope:** authorization-axis documentation + axis-separation tests. **Out of scope:** living `BASE_RISK` / `_BASE_RISK` / CLAUDE Strategy Reference deletion (Phase C); `LEG_MAP` / F2; Pine parameters; Approach 3.

### Disposition table (authorization axis)

| Catalog disposition | Families (Phase A inventory) | Authorization-axis action |
|---|---|---|
| `VENUE_LESS_CFD` | `guardian/`, `aegis/`, `striker/` CFD, `nas/` CFD | **none** — CFD books stay `AUTHORIZED · MECHANISM @ 1.00×`. No live venue ≠ decay. |
| `VENUE_WITHDRAWN` | `striker/` MYM edition, `nas/` MNQ edition | **none** — Tradeify de-scope is edition-level. Book stays `AUTHORIZED · MECHANISM @ 1.00×`. |
| `PARKED_PROTOTYPE` | `aegis/` JPY futures prototypes | **none** — never `AUTHORIZED`; do not mint a `RETIRED` row. |
| `FALSIFIED_PARKED` | `orb/`, `candidates/` | **none** — kill evidence lives in RESULTS / `rejected_candidates.md`; not a Call-5 retirement. |

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Invent Approach 3** (hard delete + offline vault) because the design file is gone | Phase A §3 already rejected it (unrecoverable-pin). Plan Task 1: STOP, do not invent. |
| **Write `lifecycle_state.json` `RETIRED` for Striker** | Barred by 08-04 de-scope and Phase A §5. Venue-fit ≠ decay. No live fills. Call 5 is a one-way door. |
| **Treat Phase A Accept as B authority** | Phase A §5 forbids it. This ADR exists because of that forbid. |
| **Demote CFD books to `WATCH` “because they have no venue”** | Same axis collapse. Authorization stays 1.00× until Call-1 / Call-5 evidence. |
| **Status quo — no B record** | Catalog misread (Phase A T3) stays unblocked. |

---

## §4 — Falsifier (revert trigger)

**H:** Recording catalog dispositions with authorization-axis action **none** prevents a dated session from demoting or retiring Striker (or any Phase A family) *solely* because CATALOG says `VENUE_WITHDRAWN` / `VENUE_LESS_CFD`, and a B-attributed change never mutates `BASE_RISK` / `DD_SCALE` / `DD_TRIGGER` / `TIER_MULTIPLIER` / `LEG_MAP`.

**H is FALSIFIED — and this ADR is superseded — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | **Silent sizing / rail bleed** | `BASE_RISK` / `_BASE_RISK` / `DD_SCALE` / `DD_TRIGGER` / `LEG_MAP` / Pine parameters change in a PR that cites only this ADR | Revert those edits; require Phase C / F2 / lock-decision ADR |
| T2 | **Catalog-only retirement** | A dated session writes `RETIRED` or `WATCH-*` for Striker solely from `VENUE_WITHDRAWN` | Restore default AUTHORIZED; supersede or addendum |
| T3 | **State file minted “to record B”** | `lifecycle_state.json` created by a B-attributed commit | Delete the file; absent ⇒ AUTHORIZED is the record |

**Revert action:** superseding ADR (full or in-part). Never silently edit §2.
**Trigger check schedule:** T1 on every PR that touches `core/lifecycle.py` / `dd_protection` / `firm_rules` until Phase C admits; T2/T3 at the next quarterly review.
**Gate:** T1–T3 fire → **FALSIFIED**; none through one quarterly review → **RESOLVED**; disputed catalog-only demotion → **AMBIGUOUS**.

---

## §5 — Forbidden moves (under this ADR)

- **Writing `lifecycle_state.json`** — tempting as “the B write.” Absent file *is* the AUTHORIZED record. Barred.
- **Demoting Striker because Tradeify was de-scoped** — edition axis, not authorization. Barred by 08-04.
- **Editing `LEG_MAP` / living `BASE_RISK` / Pine** — Phase C / F2. Barred.
- **Inventing Approach 3** because the design file is unrestored. Barred.
- **Starting Phase C from this ADR’s Accept** — C needs its own admitting ADR + this same GO’s C clause. This file is B only.
- **Loosening §4 without a superseding ADR** — Known Trap #12.

---

## §6 — Consequences

**Gate:** §4 T1–T3 → **FALSIFIED** / **RESOLVED** / **AMBIGUOUS** as named there.

**Positive consequences:**
- Catalog labels have an explicit authorization-axis binding (none).
- Phase A T3 (catalog misread as retirement) has a dated owner.

**Negative consequences (real cost):**
- Design spec body still unrestored; B quotes Phase A inventory, not the pruned Phase B section.
- CFD books remain AUTHORIZED on a book with no live venue — honest, but easy to misread as “deployable.”

**Risks:**
- A later session treats “AUTHORIZED + no venue” as a defect and writes RETIRED — mitigated by §4 T2 + tests.

**Downstream artifacts:**
- Phase A addendum + `Superseded-in-part-by` (this file)
- `docs/methodology/strategy_lifecycle.md` disposition pointer
- `tests/test_coldstore_phase_b.py`
- Phase B plan header (GO recorded)
- Retrieve note (GO proceeded unrestored)

---

## §7 — Implementation plan

- **Phase 0** — retrieve re-attempt recorded in §0; Approach 3 not invented.
- **Phase 1** — this ADR `Accepted`; Phase A addendum; methodology pointer; axis-separation tests.
- **Phase 2 sweep (pre-decision vocabulary):** `VENUE_WITHDRAWN` · `RETIRED` · `lifecycle_state.json` · `AUTHORIZED · MECHANISM` · living `BASE_RISK` keys. Disposition: this ADR + methodology note edited; `STATE.md` T2/T3/T4 row is Phase C/T2 work; `LEG_MAP` / `DD_*` ruled unaffected (B does not touch them).
- **Phase 3** — verification block; status `Accepted` with this GO.

---

## §10 — Audit hooks (runnable)

```bash
# Catalog attestation (sub-rule 8) — empty on 2026-08-23 before this ADR
rg -n -i 'coldstore|event.study|detector.kit|call1.oc' lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
# Expected: empty

# No B write to sizing / rail
git diff --stat -- core/dd_protection.py core/firm_rules.py ops/c1_rail/c1_sizing_host_reference.py
# Expected at B-only commit: empty. Phase C (same GO, later commit) may touch the first two.

# Striker stays AUTHORIZED by default
python -c "from lifecycle import load_lifecycle_state, get_lifecycle_multipliers, STRATEGY_KEYS; assert load_lifecycle_state() == {}; assert get_lifecycle_multipliers(STRATEGY_KEYS) == {k: 1.0 for k in STRATEGY_KEYS}"

# Disposition table names none for VENUE_WITHDRAWN
grep -n 'VENUE_WITHDRAWN' docs/adr/2026-08-23-strategy-coldstore-phase-b.md
# Expected: table row with **none**

python scripts/check_brief.py docs/adr/2026-08-23-strategy-coldstore-phase-b.md --type adr
python -m pytest tests/test_coldstore_phase_b.py -q
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-23-strategy-coldstore-phase-b.md --type adr
python scripts/check_adr_graph.py --regenerate-index
git log -1 --oneline -- core/lifecycle.py core/dd_protection.py docs/adr/2026-08-04-strategy-coldstore-phase-a.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial authoring — Phase B admitting ADR (`Accepted`) | Joshua + Cursor Cloud Agent |
