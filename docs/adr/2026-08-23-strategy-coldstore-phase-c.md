# ADR 2026-08-23 — Admit Phase C strategy cold-store (living Guardian/Aegis BASE_RISK retirement)

**Status:** `Accepted` — operator GO 2026-08-23 for Phase C (fresh admitting ADR; Phase A Accept is not C authority)
**Decision date:** 2026-08-23
**Supersedes:** `2026-08-04-strategy-coldstore-phase-a.md` in part — Phase C non-touch list released for living Guardian/Aegis `BASE_RISK` keys only
**Supersedes:** `2026-08-03-claude-md-futures-refocus.md` in part — §7 CFD living-`BASE_RISK` / CLAUDE table retirement now executed (Striker keys + `LEG_MAP` stay)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 anchor table, pre-C cheap-falsifier literal, catalog-attestation and amendment-first notes, §6 Phase-2 sweep table, §7, the pre-C §10 hook and the Verification `git log` line removed; §2 gains a CATALOG pointer and a dated `LEG_MAP` note; Related repointed from the tombstoned Phase B ADR. Pre-trim text at blob `c5976fee6c1518748bb41cafc112a240c8e74a1d` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Authors:** Joshua (operator GO) + Cursor Cloud Agent
**Related:** [catalog authorization-axis table](../../core/strategies/CATALOG.md) (Phase B, authorization axis unchanged; ADR tombstoned) · [`2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md) §7 · [`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md) (lock lineage of the frozen percents) · [Phase C plan](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/superpowers/plans/2026-08-23-coldstore-phase-c-implementation.md)
**Layer:** live-sizing constants (LOCKED risk% key set). **No** `DD_TRIGGER` / `DD_SCALE` / `LEG_MAP` / Pine-parameter edit.
**Tier:** full — live-risk + LOCKED surface.

---

## §0 — Rule 0 reads (production-source verification)

Read 2026-08-23 at `ea0850f` before authoring: `core/firm_rules.py` `_BASE_RISK`, `core/dd_protection.py` `BASE_RISK`, `core/lifecycle.py` `STRATEGY_KEYS`, `core/historical_challenge.py`, `core/mc/modes.py` `ALLOCATIONS`, `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP`, `scripts/verify_lock_anchors.py`, and the two subscript-consumer tests. Full anchor table and the pre-C cheap-falsifier record at the pinned prior version (`4121e84c`).

---

## §1 — Context

08-03 §7 scoped CFD **code** retirement of Guardian + Aegis and deferred it. Phase A cold-stored files only. Phase B (sibling, same GO) left the authorization axis at `AUTHORIZED · MECHANISM @ 1.00×`. Living `_BASE_RISK` still presents Guardian / Aegis as deployable sizing keys after the CFD estate and Tradeify book are gone.

Call-4 is 2-of-4 / 3-of-4 over `STRATEGY_KEYS`. Dropping two living `BASE_RISK` keys without a keyed historical path would silently turn Call-4 into 2-of-2 if the CLI keeps using `BASE_RISK.keys()`.

**Decision driver (one sentence):** living sizing must stop listing CFD keys, and the 4-leg historical MC / Call-4 authorization book must keep their own owners so the delete does not smuggle a Call-4 recalibration.

---

## §2 — Decision

**Decision:** Retire **Guardian** and **Aegis** from living `firm_rules._BASE_RISK` and `dd_protection.BASE_RISK`. Move the frozen 4-leg percent book to `historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK` (bytes unchanged: guardian 0.0034 / striker 0.0070 / aegis 0.0150 / striker_nas100 0.0037). Historical MC `ALLOCATIONS` / `PINE_SHRINK_ALLOCATIONS` / sweep REG derive from that historical dict. `lifecycle.STRATEGY_KEYS` stays the four-leg authorization book. Call-4 assessment uses `STRATEGY_KEYS`, not living `BASE_RISK.keys()`. Striker living keys and `LEG_MAP` Striker rows stay. `DD_TRIGGER` / `DD_SCALE` stay. CLAUDE Strategy Reference CFD rows become pointer-only historical. (That table now lives in [`core/strategies/CATALOG.md`](../../core/strategies/CATALOG.md) §Locked parameter record, moved 2026-09-04.)

**Effective:** immediately upon acceptance (this GO).
**Scope:** living key set + historical owner + verifier + CLAUDE pointer + tests. **Out of scope:** F2 rail teardown; Pine parameters; `lifecycle_state.json`; Call-4 constant recalibration (2/3/0.50 stay); authorization `RETIRED`.

### How Call-4 survives a 2-key living book

| Surface | After C |
|---|---|
| Living sizing (`BASE_RISK`, rail `LEG_MAP`) | `Striker`, `Striker NAS100` only (2026-10-15: `LEG_MAP` also carries the separately sized M1 proof leg `m1_stage1_test`, `m1_stage1_contract.BASE_RISK`, cap 0 by default; no Guardian/Aegis key) |
| Authorization book (`STRATEGY_KEYS`, default multipliers) | four keys, all `AUTHORIZED` @ 1.00× (Phase B) |
| Call-4 `beta_death_assessment` | over `STRATEGY_KEYS` (still 2-of-4 / 3-of-4) |
| Historical MC `ALLOCATIONS` | four slugs from `HISTORICAL_CHALLENGE_BASE_RISK` |
| `verify_lock_anchors` Guardian band | parses **historical** guardian, not living `_BASE_RISK` |
| Living `_BASE_RISK` re-gaining `guardian`/`aegis` | verifier **Error** (C invariant) |

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep CFD keys in living `_BASE_RISK` “because MC needs them”** | Leaves the live sizing map dishonest. MC can own the historical book. |
| **Recalibrate Call-4 to 2-of-2** | Silent doctrine change. 2/3/0.50 stay pinned. |
| **Write `RETIRED` for Guardian/Aegis** | Phase B said none. C is a sizing-key retirement, not Call-5. |
| **Delete Striker `LEG_MAP` / living Striker keys** | F2 / rail. This GO did not name them. |
| **Edit `DD_TRIGGER` / `DD_SCALE`** | Frozen. Not in scope. |
| **Execute C from Phase A Accept** | Phase A §5 T2. This ADR exists because of that forbid. |

---

## §4 — Falsifier (revert trigger)

**H:** After C, no living sizing path subscripts `BASE_RISK["Guardian"]` / `["Aegis"]`; historical MC allocations remain byte-identical to the pre-C 4-leg `_BASE_RISK`; Call-4 still assesses four `STRATEGY_KEYS`; `DD_TRIGGER==0.015` and `DD_SCALE==0.40`; `LEG_MAP` still maps both Striker legs.

**H is FALSIFIED — and this ADR is superseded — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | **Living CFD key remains** | `"guardian"` or `"aegis"` in living `_BASE_RISK` after C claims complete | Finish the delete or supersede scope |
| T2 | **Historical percent drift** | `HISTORICAL_CHALLENGE_BASE_RISK` bytes ≠ pre-C `{0.0034, 0.0070, 0.0150, 0.0037}` | Restore bytes; this was a move, not a retune |
| T3 | **Call-4 collapsed to living keys** | `beta_death_assessment` in the dd_protection CLI uses `BASE_RISK.keys()` (2-leg) | Restore `STRATEGY_KEYS`; supersede if intentional |
| T4 | **Protection literals moved** | `DD_TRIGGER` ≠ 0.015 or `DD_SCALE` ≠ 0.40 | Revert; not in this ADR |
| T5 | **`LEG_MAP` Striker rows deleted** | `dj30_mym` / `nas100_mnq` missing | Revert; F2 owns that |

**Revert action:** superseding ADR. Never silently edit §2.
**Trigger check schedule:** T1–T5 at C merge and the next quarterly review.
**Gate:** T1–T5 fire → **FALSIFIED**; none through one quarterly review → **RESOLVED**; disputed Call-4 key-set change → **AMBIGUOUS**.

---

## §5 — Forbidden moves (under this ADR)

- **Deleting Striker living keys or `LEG_MAP`** — F2. Tempting “while we’re here.” Barred.
- **Editing `DD_TRIGGER` / `DD_SCALE`** — frozen. Barred.
- **Recalibrating Call-4 2/3/0.50** — not a side effect of a key-set change. Barred.
- **Writing `lifecycle_state.json` `RETIRED` for CFD books** — Phase B none. Barred.
- **Re-literalizing the four percents in a third owner** — historical dict is the 4-leg owner; living `_BASE_RISK` is a subset projection. Barred.
- **Loosening §4 without a superseding ADR** — Known Trap #12.

---

## §6 — Consequences

**Gate:** §4 T1–T5 → **FALSIFIED** / **RESOLVED** / **AMBIGUOUS** as named there.

**Positive consequences:**
- Living `BASE_RISK` matches the deployable futures pair.
- Historical MC / lock percents keep a named owner.

**Negative consequences (real cost):**
- Two dicts to keep in sync (living ⊂ historical). Mitigated by deriving living from historical.
- CLAUDE table no longer machine-lists CFD risk% cells; pointer must stay one hop.

**Risks:**
- `verify_lock_anchors` fixtures that only write living `_BASE_RISK` with guardian will Error until updated — intended.
- A session re-adds `guardian` to living `_BASE_RISK` “for MC.” Verifier Errors.

**Downstream artifacts:**
- `core/historical_challenge.py` historical book
- `core/firm_rules.py` living subset
- `core/mc/modes.py` `ALLOCATIONS` source
- `core/dd_protection.py` CLI Call-4 keys
- `scripts/verify_lock_anchors.py` + tests
- `tests/test_lifecycle.py` / `tests/core/test_firm_constants_single_source.py`
- `CLAUDE.md` Strategy Reference
- Phase A / 08-03 `Superseded-in-part-by`
- `docs/adr/INDEX.md`

---

## §10 — Audit hooks (runnable)

```bash
# After C: living keys are Striker pair only
python -c "from firm_rules import _BASE_RISK; assert set(_BASE_RISK)=={'striker','striker_nas100'}, _BASE_RISK"
python -c "from dd_protection import BASE_RISK; assert set(BASE_RISK)=={'Striker','Striker NAS100'}, BASE_RISK"
python -c "assert 'BASE_RISK[\"Guardian\"]' not in open('core/dd_protection.py',encoding='utf-8').read()"
python -c "assert 'BASE_RISK[\"Aegis\"]' not in open('core/dd_protection.py',encoding='utf-8').read()"

# Historical percents byte-identical to pre-C lock
python -c "from historical_challenge import HISTORICAL_CHALLENGE_BASE_RISK as h; assert h=={'guardian':0.0034,'striker':0.0070,'aegis':0.0150,'striker_nas100':0.0037}, h"

# Call-4 still 4-leg
python -c "from lifecycle import STRATEGY_KEYS; assert STRATEGY_KEYS==frozenset({'Guardian','Striker','Aegis','Striker NAS100'})"

# Protection literals + LEG_MAP
python -c "from dd_protection import DD_TRIGGER, DD_SCALE; assert DD_TRIGGER==0.015 and DD_SCALE==0.40"
grep -n 'LEG_MAP' ops/c1_rail/c1_sizing_host_reference.py

python scripts/verify_lock_anchors.py   # ROUTING: Closed
python scripts/check_brief.py docs/adr/2026-08-23-strategy-coldstore-phase-c.md --type adr
python -m pytest tests/test_lifecycle.py tests/core/test_firm_constants_single_source.py tests/test_verify_lock_anchors.py tests/core/test_mc_synthetic_engine.py tests/test_coldstore_phase_c.py -q
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-23-strategy-coldstore-phase-c.md --type adr
python scripts/check_adr_graph.py --regenerate-index
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Initial authoring — Phase C admitting ADR (`Accepted`) | Joshua + Cursor Cloud Agent |
