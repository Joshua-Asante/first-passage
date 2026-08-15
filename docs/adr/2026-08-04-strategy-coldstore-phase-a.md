# ADR 2026-08-04 — Admit Phase A strategy cold-store (filesystem surface only)

**Status:** `Accepted` — operator GO to execute Phase A via subagent-driven development, recorded 2026-08-04; this ADR is the admitting gate. Phase B (lifecycle disposition) and Phase C (hot-path code retirement) remain separately GO’d and are **not** authorized by this document.
**Decision date:** 2026-08-04
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (operator GO) + Cursor (SDD Task 1 recorder)
**Related:** [`2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md) §7 (CFD code retirement scoped, not executed — that work is Phase C, not this ADR) · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) (Striker stays `AUTHORIZED · MECHANISM @ 1.00×`; venue-fit ≠ decay) · design [`docs/superpowers/specs/2026-08-04-strategy-coldstore-retirement-design.md`](../superpowers/specs/2026-08-04-strategy-coldstore-retirement-design.md) · plan [`docs/superpowers/plans/2026-08-04-strategy-coldstore-phase-a.md`](../superpowers/plans/2026-08-04-strategy-coldstore-phase-a.md)
**Layer:** strategy surface (filesystem + discoverability). **No** `BASE_RISK`, lifecycle, `LEG_MAP`, or Pine-parameter edit.

---

## §0 — Rule 0 reads (production-source verification)

All read in-session on 2026-08-04 **before** authoring (anchors = `git log -1 --oneline -- <path>`):

| Source | Anchor | What it grounds |
|---|---|---|
| `core/dd_protection.py` `BASE_RISK` | `fc14682` | Keys `Guardian` / `Striker` / `Aegis` / `Striker NAS100` still present — Phase C not started; this ADR must not touch them. |
| `core/lifecycle.py` | `4441c72` | Authorization ladder unchanged; Striker remains on the authorization axis per ADR 2026-08-04 (Tradeify de-scope). Catalog disposition ≠ lifecycle write. |
| `ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` | `2345095` | `dj30_mym`→`Striker`, `nas100_mnq`→`Striker NAS100` — rail import surface; Phase A does not edit `LEG_MAP`. |
| `core/strategies/MANIFEST.sha256` | `dd4e4aa` | Hot-path Pine pins still under family dirs (pre-move); Phase A re-points path column only. |
| [`2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md) §7 | `dc7adcc` | Prior ADR scoped CFD code retirement and deferred execution; Phase A is the filesystem limb that §7 did not authorize. |
| [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) §2 | `dc7adcc` | Striker stays `AUTHORIZED · MECHANISM @ 1.00×`; catalog `VENUE_WITHDRAWN` must not be read as lifecycle `RETIRED`. |
| Design + Phase A plan | `59c2301` / `cfb84a6` | Approach 2 + frozen inventory table copied verbatim into §2 below. |

**Gitignore pre-flight.** `**/*.pine` is ignored. Phase A moves Pine with filesystem `shutil.move` (not `git mv`); hash pins stay byte-identical; only the manifest path column changes. No Pine parameter values are read or edited here.

**Collision check (Step 1):** `git fetch origin`; `origin/main ^HEAD` empty of strategy-coldstore work; no `docs/adr/2026-08-04-strategy-coldstore-phase-a.md` on `origin/main`; no `archive_strategy` / `strategy-coldstore` parallel Phase A on main.

---

## §1 — Context

After Tradeify de-scope ([`2026-08-04`](2026-08-04-tradeify-venue-descope-eval-included.md)), neither Striker futures leg is a Tradeify deployment target, CFD locked editions have no live venue, and ORB/candidates sit falsified-parked — yet `core/strategies/` still presents as a live multi-leg book (CFD Pine, futures editions, prototypes, and candidates side-by-side). Agents and humans still glob the hot tree as “what’s live.”

[`2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md) §7 scoped **code** retirement of Guardian + Aegis but never executed it, and forbade starting that project from the scope sketch alone. The operator-confirmed design (2026-08-04) chose **Approach 2**: Phase A cold-store surface → Phase B lifecycle disposition → Phase C hot-path code — each separately GO’d.

**Decision driver (one sentence):** the hot strategy tree is a discoverability hazard after venue de-scope, and filesystem cold-store can be admitted without moving the authorization or sizing axes that later phases must still decide deliberately.

---

## §2 — Decision

**Decision:** Admit **Phase A only** — cold-store unused strategy Pine and full lock/changelog/candidate docs under `core/strategies/_archive/<family>/`, leave hot `*_CARD.md` stubs + `CATALOG.md`, re-pin `MANIFEST.sha256` / `PORT_MANIFEST.sha256` path columns (hash digests unchanged), and exclude `_archive/` from default agent search. Catalog dispositions below are frozen for the Phase A move set.

**Effective:** immediately upon acceptance (implementation proceeds under the Phase A plan on this branch).
**Scope:** filesystem + discoverability under `core/strategies/` (plus opportunistic link repair / search excludes / map pointers named in the plan). **Out of scope:** Phase B lifecycle writes; Phase C `BASE_RISK` / `firm_rules` / Call-4 / CLAUDE Strategy Reference deletion; F2 rail teardown; F3 successor venue; Pine parameter edits.

### Frozen inventory (exact copy from Phase A plan)

| Disposition | Hot family | Files to cold-store |
|---|---|---|
| `VENUE_LESS_CFD` | `guardian/` | `guardian_gold_v5.5.pine`, `_indicator.pine`, `LOCK.md`, `guardian_CHANGELOG.md` |
| `VENUE_LESS_CFD` | `aegis/` | `aegis_usdjpy_v4.3.pine`, `_indicator.pine`, `LOCK.md`, `aegis_CHANGELOG.md` |
| `VENUE_LESS_CFD` | `striker/` | `striker_dj30_v4.5.pine`, `_indicator.pine`, `LOCK.md`, `striker_CHANGELOG.md` |
| `VENUE_LESS_CFD` | `nas/` | `striker_nas100_v1.pine`, `_indicator.pine`, `LOCK.md`, `striker_nas100_CHANGELOG.md` |
| `VENUE_WITHDRAWN` | `striker/` | `striker_dj30_v4.5_mym.pine`, `striker_dj30_v4.5_mym_FUTURES_LOCK.md` |
| `VENUE_WITHDRAWN` | `nas/` | `striker_nas100_v1_mnq.pine`, `striker_nas100_v1_mnq_FUTURES_LOCK.md` |
| `PARKED_PROTOTYPE` | `aegis/` | `aegis_jpy_futures_v0_3_prototype.pine`, `aegis_jpy_futures_v0_3_bepad_prototype.pine` |
| `FALSIFIED_PARKED` | `orb/` | `orb_mnq_v0_1.pine`, `orb_mnq_v0_2.pine`, both `*_CANDIDATE.md` |
| `FALSIFIED_PARKED` | `candidates/` | all files under `candidates/` (pine + sweep yamls) |

### Explicit non-touch list (this ADR)

| Surface | Status under Phase A |
|---|---|
| `core/dd_protection.py::BASE_RISK` | **Untouched** |
| `core/firm_rules.py::_BASE_RISK` | **Untouched** |
| `core/lifecycle.py` / `lifecycle_state.json` | **Untouched** — Striker stays `AUTHORIZED · MECHANISM @ 1.00×` per ADR 2026-08-04 |
| `ops/c1_rail` `LEG_MAP` | **Untouched** (F2 owns rail disposition) |
| Pine parameters (SL/TP/ATR/risk%/session/…) | **Untouched** — moves only; no re-fit |
| CLAUDE.md Strategy Reference table cells | **Untouched** this phase |

**Catalog disposition ≠ authorization axis.** `VENUE_WITHDRAWN` / `VENUE_LESS_CFD` are discoverability labels only.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Approach 1 — files-only forever** | Leaves `BASE_RISK` / CLAUDE table dishonest after cold-store; operator rejected in design. |
| **Approach 3 — hard delete + offline vault only** | Repeats unrecoverable-pin failure mode; over-retires vs F3. |
| **Bundle A+B+C in one PR** | Violates separate-GO sequencing; lifecycle Call-5 and engine pre-flight are distinct decisions. |
| **Lifecycle `RETIRED` for Striker in this ADR** | Explicitly barred by ADR 2026-08-04 §3 (no live fills; Call 5 one-way door; venue-fit ≠ decay). |
| **Extend 2026-08-03 §7 as the admitting instrument without a new ADR** | §7 scoped code retirement and forbade starting from the sketch; Phase A needs its own frozen inventory + filesystem gate. |
| **Status quo — no cold-store** | Hot tree continues to read as a live book after venue de-scope; agent/human discoverability stays wrong. |

---

## §4 — Falsifier (revert trigger)

**H:** Phase A cold-store (archive paths + CARD stubs + CATALOG + path-only manifest re-pins) correctly removes the “live book” presentation of unused strategy surfaces **without** changing sizing, lifecycle authorization, rail `LEG_MAP`, or Pine parameters — and every moved slug remains recoverable via CATALOG → CARD → `_archive/` body with hash pins intact.

**H is FALSIFIED — and this ADR is superseded — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | **Pin integrity loss** | Any Phase A–moved file’s SHA-256 digest ≠ the digest that was in `MANIFEST.sha256` / `PORT_MANIFEST.sha256` immediately before the move | Halt moves; restore from pre-move snapshot / offline copy; supersede if doctrine failed |
| T2 | **Silent Phase C / lifecycle bleed** | `BASE_RISK` / lifecycle / `LEG_MAP` / Pine parameters change in a PR that cites only this ADR as authority | Revert those edits; require Phase B/C admitting ADR + GO |
| T3 | **Catalog misread as retirement** | A dated session demotes or retires Striker **solely** because CATALOG says `VENUE_WITHDRAWN`, without Call-1 / Call-5 evidence | Correct lifecycle state; supersede or addendum clarifying the axes |
| T4 | **Hot-path Pine remains after claimed complete Phase A** | Any `.pine` under `core/strategies/{guardian,aegis,striker,nas,orb,candidates}/` (non-`_archive`) after Phase A merge claims complete | Incomplete delivery — finish moves or supersede scope |

**Revert action:** author a superseding ADR (full or in-part). Never silently edit this ADR’s §2 inventory or non-touch list (Known Trap #12).

**Trigger check schedule:** T1/T4 at every Phase A move commit and at Phase A merge; T2 on every PR that touches `core/strategies/` or `dd_protection` until Phase C admits; T3 at the 2026-08-08 programme audit.

**Verdict rule:** T1–T4 fire → **FALSIFIED** (supersede / repair); no T1–T4 through Phase A merge + one quarterly review → treat Phase A admission as **RESOLVED**-stable; disputed attribution of a sizing/lifecycle change to “catalog only” → **AMBIGUOUS** → programme audit.

---

## §5 — Forbidden moves (under this ADR)

- **Editing `BASE_RISK`, lifecycle state, or `LEG_MAP` “while we’re moving files.”** Genuinely tempting — cold-store makes CFD keys look dead. Barred: Phase C + Call-5 + F2 own those axes; this ADR’s non-touch list is load-bearing.
- **Reading `VENUE_WITHDRAWN` as lifecycle `RETIRED` for Striker.** Tempting after Tradeify de-scope. Barred by ADR 2026-08-04 §2–§3; catalog ≠ authorization.
- **Hard-deleting Pine or dropping hash pins** instead of archive + re-pin. Tempting under “gitignored anyway.” Barred: prior PORT_MANIFEST pin-loss failure mode; Approach 3 was rejected.
- **Starting Phase B or Phase C because this ADR is `Accepted`.** Acceptance admits Phase A only; B and C need separate operator GO + (for C) a fresh admitting ADR.
- **Loosening §4 triggers without a superseding ADR.** Silent amendment is methodology-layer `p`-hacking (Known Trap #12).

---

## §6 — Consequences

**Positive consequences:**
- Hot `core/strategies/` stops reading as a live multi-leg book; CATALOG + CARDs are the open-first surface.
- Pine integrity gates still own the tree (`_archive/` stays under the same MISSING/MISMATCH hard-fail).
- Phase B/C retain clean decision surfaces — filesystem work does not smuggle authorization or sizing changes.

**Negative consequences (real cost):**
- Two-hop lookup (CATALOG → CARD → `_archive/`) for Rule-0 deep reads that used to be one path.
- Link debt in `ops/instruments/` and maps until plan Task 6 lands.
- Agents that ignore search excludes may still find archive bodies if they force-search — mitigated by `.rgignore` / `.cursorindexingignore` and CATALOG discipline.

**Risks:**
- Operator moves Pine on a non-durable machine and authors pins where bytes cannot persist — mitigated by existing `--check-pin-provenance` doctrine and plan constraint (Joshua’s durable machine only).
- Partial Phase A merge leaves mixed hot/cold paths — mitigated by §10 emptiness + manifest hooks before claiming complete.

**Downstream artifacts (Phase A plan; not all in this Task-1 commit):**
- `core/strategies/CATALOG.md`, `*_CARD.md`, `_archive/`, manifest path re-pins, search excludes, instrument link repair, `REPO_MAP.md` / `PIPELINES.md` pointers, `docs/SESSIONS.md` on Phase A land, `docs/adr/INDEX.md` (regenerated with this ADR).

**Gate / verdict (binary):** Phase A admission is **RESOLVED** when §10 hooks #1–#5 pass after plan Tasks 2–7 land; **FALSIFIED** if any §4 trigger T1–T4 fires; **AMBIGUOUS** if a session attributes a sizing/lifecycle change to catalog disposition alone without a clear Call-1/Call-5 or Phase C ADR trail.

---

## §7 — Implementation plan

- **This commit (Task 1):** land this admitting ADR + regenerate `docs/adr/INDEX.md`. **No Pine moves.**
- **Tasks 2–7** (separate commits on the Phase A plan): search excludes + CATALOG skeleton → `archive_strategy.py` helper → VENUE_LESS_CFD moves → VENUE_WITHDRAWN / prototypes / orb / candidates → link repair → final verification + SESSIONS.
- **Phase B / Phase C:** separately planned and GO’d; not authorized here.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Pine manifest green after Phase A moves (path column → _archive/)
python scripts/check_pine_manifest.py
# Expected: exit 0 (EXTRA warns for unpinned archive candidates OK)

# 2. No hot-path .pine under family dirs (only under _archive/)
python -c "
from pathlib import Path
roots = ['guardian','aegis','striker','nas','orb','candidates']
bad = []
for r in roots:
    p = Path('core/strategies') / r
    if p.exists():
        bad.extend(p.rglob('*.pine'))
print('hot pine count', len(bad))
assert not bad, bad
"

# 3. Phase C not started — Guardian key still present in dd_protection
python -c "import pathlib; t=pathlib.Path('core/dd_protection.py').read_text(encoding='utf-8'); assert t.count('\"Guardian\"') >= 1"

# Equivalent one-liner form of the plan brief:
# grep Guardian core/dd_protection.py   # expect: ≥1 match until Phase C

# 4. Striker authorization axis not silently moved (lifecycle keys / sizing still present)
python -c "import pathlib; t=pathlib.Path('core/dd_protection.py').read_text(encoding='utf-8'); assert '\"Striker\"' in t and 'Striker NAS100' in t"
grep -n 'LEG_MAP\|Striker' ops/c1_rail/c1_sizing_host_reference.py
# Expected: LEG_MAP still maps both Striker legs

# 5. This ADR does not claim Phase B/C authority
grep -n 'Phase B\|Phase C\|separately GO' docs/adr/2026-08-04-strategy-coldstore-phase-a.md
# Expected: explicit separate-GO language present
```

**Note on hook #2 timing:** hooks #1–#2 are **post-move** acceptance criteria for Phase A completion (plan Tasks 4–7). At the moment this ADR lands (Task 1 only), hot-path `.pine` files are still expected to exist; do not treat a pre-move failure of hook #2 as falsifying H.

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-08-04-strategy-coldstore-phase-a.md --type adr
# Expected: PASS (no HARD)

# ADR lifecycle graph + INDEX
python scripts/check_adr_graph.py --regenerate-index
# Expected: exit 0

# Rule 0 anchors re-checkable
git log -1 --oneline -- core/dd_protection.py core/lifecycle.py ops/c1_rail/c1_sizing_host_reference.py core/strategies/MANIFEST.sha256 docs/adr/2026-08-03-claude-md-futures-refocus.md docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-04 | Initial authoring — Phase A admitting ADR (`Accepted`) | Joshua + Cursor SDD Task 1 |
