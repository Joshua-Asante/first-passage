# ADR 2026-08-07 — W5: governance diet (gate-manifest runner + tiered entries)

**Status:** `Accepted` — composition/tier owned by one runner; entry-class diet
**Decision date:** 2026-08-07
**Authors:** Joshua (Posture-A direction) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S7](../spec/2026-08-07-loop-s7-repo-alignment-spec.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) · [`scripts/gates.yml`](../../scripts/gates.yml) · [`scripts/gate_manifest.py`](../../scripts/gate_manifest.py) · [root-doc charter](2026-07-16-root-doc-charter-dedup.md)
**Layer:** governance tooling + doc diet. **$0 / K=0** — no gate dropped; CI re-enable separately owed.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| `scripts/githooks/pre-commit` | gates 1–14 enumerated in shell | Composition duplicated vs `Makefile` targets |
| `Makefile` `check` / `validate` | parallel wrappers | Same battery, hand-kept |
| `docs/SESSIONS.md` / `STATE.md` headers | narrative vs open-board | Accretion risk without tier/cap |

---

## §1 — Context

Pre-commit and Make each hand-enumerate the same gate battery. Orientation docs restate the gate list. SESSIONS/STATE accrete without entry classes. Posture-A wants one manifest owning **which** gates run at **which** tier, and a diet for session/state prose.

---

## §2 — Decision

### Gate-manifest runner

1. **`scripts/gates.yml`** is the composition authority: each gate has `id`, `cmd`, `tier` (`always` | `data-conditional` | `soft`), and optional `when` (e.g. staged paths under `core/data/…`).
2. **`scripts/gate_manifest.py`** loads that file and runs the selected tier. Exit non-zero on any hard failure.
3. **`scripts/githooks/pre-commit`** becomes a thin caller: `python scripts/gate_manifest.py --tier pre-commit`.
4. **`make validate` / `make check`** call the same runner (equivalent behavior — **no gate dropped** in this land).
5. **CLAUDE.md** gate list collapses to a pointer at `scripts/gates.yml` + this ADR.

### Tiered SESSIONS / STATE entry classes (direction)

| Class | Surfaces | Cap / rule |
|---|---|---|
| **A — Decision** | ADR / brief Accept; lock; fork ruling | SESSIONS: Focus + link; ≤ **40 words** of prose beyond links |
| **B — Build** | Code land with tests; rail tooling | SESSIONS: Shipped links; no constant restatement |
| **C — Measurement** | RESULTS / closure | Link RESULTS; do not restate bust % |
| **D — Hygiene** | pointer sweeps, INDEX regen | Prefer skip SESSIONS; if needed, one line |

STATE stays open-board only (Rule 7 / anti-accretion). New decision-index lines remain one line + owning ADR. This ADR **directs** the 40-word cap; mechanical enforcement is optional later.

### Explicitly owed (not in this land if risky)

- GitHub Actions CI re-enable / deriving CI job list from `gates.yml` (workflows stay format-only / inert-as-shipped until a dedicated re-enable commit).
- Collapsing `check_brief.py` + template verification blocks to a single authoritative tool (templates may still name both until that pass).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep dual hand-lists in sync by convention | Already drifted historically |
| Drop soft gates to shrink the battery | Out of scope; diet is ownership, not deletion |
| Enforce 40-word cap in a hook now | Premature; direction first |

---

## §4 — Falsifier

**H:** Adding/removing a pre-commit gate requires editing `gates.yml` (and tests if any), not a second hand-copy in the shell hook.

**FALSIFIED if:** a hard gate present in the pre-W5 hook is absent from `gates.yml` after land, or `make check` skips a gate the hook still ran.

---

## §5 — Forbidden moves

- Dropping a gate under cover of “diet.”
- Restating operational constants in SESSIONS/STATE under class A–D.
- Flipping CI from format-only without a dedicated commit.

---

## §6 — Gate

Same-PR: `gates.yml` + `gate_manifest.py` + wired pre-commit + Makefile + CLAUDE.md pointer + SESSIONS/STATE/Rule-7 header notes. CI re-enable = owed.

---

## §7 — Audit hooks

```bash
python scripts/gate_manifest.py --list
python scripts/gate_manifest.py --tier pre-commit --dry-run
grep -n "gates.yml\|gate_manifest" CLAUDE.md scripts/githooks/pre-commit Makefile
```
