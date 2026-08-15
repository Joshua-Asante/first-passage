# ADR 2026-08-03 — Retire `params.toml` hub gates (derived CFD lock mirror)

**Status:** `Accepted` — operator GO 2026-08-03 (shape 1: delete the mirror **and** retire hub drift gates that only compared against it; do not rebuild pairwise canonical↔canonical drift detection).
**Decision date:** 2026-08-03

**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

**Related:** [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md) (Phase 3 already removed `[mc_anchor_pepperstone]` from the living manifest); [`docs/adr/2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md) (futures-first charter; CFD code retirement separately gated); SESSIONS carry-forward that authorized retiring the `params.toml` gate as a follow-on packet.

---

## §0 — Rule 0 reads (production source, verified 2026-08-03)

| Path | What it establishes |
|---|---|
| `core/config/params.toml` @ `bd92d8e` | Derived CFD locked-book mirror only (`[strategies.*]` G/DJ30/A/NAS + `[dd_protection]` C2). No Tradeify / MYM / MNQ / firm-tier keys. Header states DERIVED MIRROR — NOT canonical. |
| `scripts/validate_params.py` | Hub gate: every comparison uses the TOML as the expected side vs `dd_protection` / `firm_rules` / CLAUDE / Pine / etc. |
| `scripts/check_path_liveness.py` | Dual-leg: params.toml `lock_md`/strategy-dir + `MANIFEST.sha256` parent dirs. |
| `scripts/verify_lock_anchors.py` | Soft lock-check: requires `params.toml` + `dd_protection.py`; Forward on Guardian band or DD-vs-toml skew. |
| `ops/recall/guard.py::load_denylist` | Soft-reads params.toml when present; also reads `dd_protection.py`, `firm_rules.py`, `CLAUDE.md`. |
| Grep `core/**/*.py` / `ops/c1_*` | No live sizing/rail import of `params.toml`. |

---

## §1 — Context

`core/config/params.toml` was a **governance hub**, not runtime config. Live sizing reads `dd_protection.BASE_RISK` / `firm_rules._BASE_RISK` / the c1 host; Pine is canonical for strategy behavior. The mirror existed so `validate_params` could hard-fail cross-source drift on the CFD locked book.

That book has **no live venue**. The futures-first charter keeps Striker sizing keys as c1 inputs, but those keys live in Python modules — not in the TOML. Keeping a CFD-shaped derived mirror as a HARD pre-commit/CI hub forces maintenance of a surface that no live path consumes, and that SESSIONS already flagged for retirement after substrate Phase 5.

**Decision driver (one sentence):** retire the unused derived mirror and the hub gates that only existed to compare against it; keep integrity on pine hashes, MANIFEST path-liveness, methodology skill no-constants, and recall denylist sourced from canonical Python/CLAUDE.

---

## §2 — Decision

**Shape 1 — delete mirror + retire hub gates.**

| Surface | Disposition |
|---|---|
| `core/config/params.toml` (+ empty `core/config/`) | **RETIRE** (`git rm`) |
| `scripts/validate_params.py` + fixtures/tests | **RETIRE** |
| `check_skills_no_constants` | **EXTRACT** to `scripts/check_skills_no_constants.py`; keep wired in pre-commit / CI / Makefile |
| `scripts/check_path_liveness.py` | **KEEP** MANIFEST-parent leg only; drop params.toml leg |
| `scripts/verify_lock_anchors.py` | **SLIM** to `dd_protection.py` only (Guardian safe band + readable DD literals); no toml Forward/Action |
| `ops/recall/guard.py` | Drop params.toml walk; emit %-forms from `firm_rules._BASE_RISK` decimals |

**Explicitly untouched:** Pine / `dd_protection.py` / `firm_rules.py` literals / MC pins / c1 rail. No parameter or sizing change.

**Not chosen (shape 2):** rewrite drift detection as pairwise canonical↔canonical without a mirror — larger rewrite; deferred unless §4 fires.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Shape 2 — delete mirror, keep pairwise drift gates** | Operator chose shape 1; CFD locked-book hub drift detection is not load-bearing for the live c1 path. |
| **`git rm` only, leave gates broken** | Breaks pre-commit/CI; not a retirement. |
| **Keep the mirror indefinitely** | CFD-era derived hub with no live consumer; contradicts futures-first charter and the standing "retire params.toml gate" carry-forward. |

---

## §4 — Falsifier

**H:** After retirement, integrity of live sizing + Pine pins + methodology skills does not require the TOML hub.

**Falsified if** within two quarterly cycles (next checks 2026-08-08 → 2026-11-08) a **live** defect is traced to silent skew among Pine / `dd_protection` / `firm_rules` / CLAUDE that the retired `validate_params` hub would have hard-failed, **and** that skew is not already caught by `check_pine_manifest` / path-liveness / skill no-constants / recall denylist → open a shape-2 restore ADR (pairwise gates without reintroducing a derived mirror), or restore from git history.

**Trigger check schedule:** 2026-08-08 quarterly — field added 2026-08-06 (operator-ratified R-B2a; restates existing §4 schedule verbatim — no change to the obligation)

---

## §5 — Forbidden moves

- Reintroducing a derived `params.toml` (or equivalent hub mirror) without a new ADR.
- Weakening `check_pine_manifest` / path-liveness / skill no-constants to "make retirement green."
- Editing `DD_TRIGGER` / `DD_SCALE` / `BASE_RISK` / `_BASE_RISK` / Pine as part of this change.
- Claiming this discharges the futures-refocus ADR §7 CFD **code** retirement (Guardian/Aegis) — that remains separately gated.

---

## §6 — Gate

**RESOLVED** when: `git ls-files core/config` is empty; pre-commit/CI call `check_skills_no_constants` (not `validate_params`); path-liveness is MANIFEST-only and green; `verify_lock_anchors` routes Closed on live `dd_protection.py` without reading a toml; recall denylist still contains locked risk %-forms from `firm_rules`; targeted pytest green.

---

## §10 — Audit hooks

```bash
git ls-files 'core/config/**'          # expect empty
rg -n 'validate_params|params\.toml' scripts/ ops/recall/ Makefile .github/workflows/skills-check.yml scripts/githooks/pre-commit
python scripts/check_skills_no_constants.py
python scripts/check_path_liveness.py
python scripts/verify_lock_anchors.py
python scripts/check_pine_manifest.py
```

---

## Addendum 2026-08-08 — Rule 11 dormancy record (frozen bodies this retirement darkened)

Rule 11 requires a retiring ADR to record the standing falsifiers whose named inputs it removed.
Discharged here rather than in the affected bodies: all five are **frozen pre-registrations**, editable
only by close+reopen (survivor-scoring prereg Trap #12), so the correction cannot land at the point of use.

**(a) Bodies darkened.** Measured 2026-08-08 by direct read.

| Frozen body | Hook | Shape of the darkening |
|---|---|---|
| `2026-07-16-striker-mym-reconstruction-candidate-1-prereg.md`:301 | `git diff -- core/strategies/striker/LOCK.md core/config/params.toml …` | silent-pass |
| `2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md`:349 | same | silent-pass |
| `2026-08-02-sub100k-realizable-book-scoring-prereg.md`:317 | `python scripts/validate_params.py && git diff --stat HEAD -- core/ …` | `&&` short-circuit |
| `Q-6JCOMPOSE-1-verdict-preregistration.md`:389 | same | `&&` short-circuit |
| `Q-6JCOMPOSE-2-verdict-preregistration.md`:239 | same | `&&` short-circuit |
| `Q-PYRPARITY-1-verdict-preregistration.md`:12, :92 | §0 anchors `core/config/params.toml` @ `784a9ab` lines 69/94 (`pyramid_pct = 750.0 / 1000.0`); §10 `git log -1 -- … params.toml` | anchor unresolvable |

Not darkened, checked and excluded: `2026-08-03-c1-cadence-leg-preregistration.md` repaired its own hooks at
authoring (:37, :241); `Q-XMEM-1`:15 names `params.toml` inside a memory **denylist**, which a deleted file does
not weaken.

**(b) Why the input cannot accrue — two distinct mechanisms, both silent.**
`git diff -- <path>` **exits 0 on a pathspec that matches nothing**, so once `core/config/params.toml` was deleted
these hooks report clean and are indistinguishable from "verified unchanged". And in `A && B`, retiring `A`
(`scripts/validate_params.py`, now absent → non-zero) means **`B` never executes** — so the surviving, still-valid
`git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py` limb was disabled as collateral, without
any output saying so.

**(c) Re-arm condition: none.** `params.toml` and its hub validator are retired permanently. Pine is canonical for
strategy behavior; `dd_protection.py` / `firm_rules.py` are canonical for live-sizing constants. Successors are
`scripts/check_pine_manifest.py` + `core/strategies/MANIFEST.sha256`.

**(d) Surviving coverage — run this instead**, verbatim, in place of every `&&`-suppressed limb above:

```bash
git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py
```

**Generalizable defect (also logged as a methodology lesson):** a hook of the form `git diff -- <path>` cannot
distinguish *absent* from *unchanged*, and an `A && B` hook silently disables `B` when `A` is retired. Prefer
`test -e <path> &&` guards, or separate the limbs onto their own lines.
