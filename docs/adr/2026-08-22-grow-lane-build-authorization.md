# ADR 2026-08-22 — GROW-lane build authorization (deep-iteration-lane tooling packet)

**Status:** `Accepted` — operator GO (JA) 2026-08-22 ("ratify, accept, and begin the build"),
electing [SPEC GROW v2](../spec/2026-08-22-grow-lane-generate-refine-spec.md) Part A in full.
**Tier:** full — limb 4 of the [ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) fires
(amends doctrine: extends the [deep-iteration lane charter](2026-08-16-deep-iteration-lane-charter.md)
with new tooling and rules on its §4 counter scope).
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-08-22
**Authors:** Joshua (commission + GO) + Claude Code (drafter)
**Supersedes:** nothing. Charter §2 discipline (K ≤ 33, `floor_at_k(K, confirm_years) ≤ 2.0`,
power ≥ 0.50), `CAP`/`DSR_MIN`/`axis_screen.py`, and every existing admission predicate stand
byte-unedited. Withdraws nothing from [GROW spec v1](../spec/2026-08-22-grow-lane-generate-refine-spec.md)'s
withdrawn D1–D3 (already dead per the 2026-08-22 dual-panel review — this ADR does not revisit
that verdict).
**Related:** [deep-iteration lane charter](2026-08-16-deep-iteration-lane-charter.md) (owner) ·
[GROW spec v2](../spec/2026-08-22-grow-lane-generate-refine-spec.md) (Part A/B) ·
[dual-panel audit note](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md) · F3
attestation-library spec
**Layer:** research governance — no live-risk surface; no locked parameter; no allocation; no
arming; no Databento spend (code + synthetic-data build only).

---

## §0 — Rule-0 reads (verified this session @ `f849402`, 2026-08-22)

| Source | Anchor | Supplies |
|---|---|---|
| [Deep-iteration lane charter](2026-08-16-deep-iteration-lane-charter.md) | `85a83ba`, this session | `Accepted`; §2.2's three conjuncts (K≤33 · floor≤2.0 · power≥0.50); §4 counters (campaigns completed 0, abandoned 1/2 — DL-1); §7 step-2/4 already licensed on Accept |
| [GROW spec v2](../spec/2026-08-22-grow-lane-generate-refine-spec.md) | this change-set | Part A engine + GROW-0 scope; Part B named-not-proposed; withdrawn D1–D3 |
| [`lab/research_utils/axis_screen.py`](../../lab/research_utils/axis_screen.py) | executed this session | `floor_at_k(k, years=6.5)` and `clause_n_power` — reused verbatim, not re-derived, for the deep-lane predicate |
| [`lab/discovery/admission_schema.py`](../../lab/discovery/admission_schema.py) | executed this session | The mechanism-first (S6/TNEC-1) predicate this ADR does **not** touch — deep-lane gets its own predicate module, S6's stays K≥4-refusing at `CAP=1.0` |
| [`lab/discovery/register_search.py`](../../lab/discovery/register_search.py) | executed this session, `4028be7` | `--lane` currently `{blind, mechanism-first}` only — `deep` does not exist; `open_run`'s per-lane gate-and-refuse-with-no-write shape is the pattern this build extends |
| [`docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md`](../briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) | referenced by charter change history | DL-1 ran without this predicate module or a `--lane deep` open — its abandonment stands unaffected; future campaigns use the tooling this ADR authorizes |

**Amendment-first / dedup (executed this session):**
```
$ grep -rln "deep_lane_admission\|grammar.py\|burned_segments" lab/discovery/ lab/research_utils/
(no output — none of this tooling exists yet)
```

---

## §1 — Context

GROW spec v2 Part A is tooling for the Accepted charter, not a new decision — but the packet's
own Boundary line makes one ruling depend on this ADR in writing: *"GROW-0 sits outside charter
§4 counters only if this packet's ratification says so in writing."* Everything else in Part A
(the grammar engine, `--lane deep`, the enforcement build manifest) is already licensed by the
charter's own §7 steps 2–4 on Accept and needs no further permission — but naming it here, once,
keeps the build auditable against a single dated authorization rather than scattered commit
messages.

**Scope discipline (why this is one ADR, not a build-log stream):** the packet named a large
enforcement build manifest (ledger checks, `gates.yml` wiring, streak checker, LOCKED-leg
denylist, Rule-0 anchor checker, `universe_gate` exit-code propagation). Building all of it in
one pass risks the exact failure the dual-panel review caught in v1 — claiming scope that isn't
load-bearing yet. This ADR authorizes the **full** manifest but the build lands in dated slices;
§7 tracks what has actually shipped, and nothing here should be read as claiming a slice is done
before its own commit says so.

---

## §2 — Decision

1. **GROW-0 is exempted from the charter's §4 counters**, per the packet's own Boundary
   requirement. GROW-0 is engine/harness validation (synthetic data only, no mechanism family,
   no confirm read) — it terminates in the packet's own Gate (RESOLVED/FALSIFIED), never in the
   charter's `campaigns completed / survivors falsified / abandoned` counts. A GROW-0 fix-and-rerun
   is not an "abandonment"; the charter's counting machinery (§4(b)–(d)) is untouched for every
   *campaign* (GROW-1 onward), which counts exactly as DL-1 did.
2. **Part A tooling is commissioned**, build order per the packet's step numbering:
   - `lab/discovery/deep_lane_admission.py` — the charter §2.2 three-conjunct predicate (K ≤ 33
     · `floor_at_k(K, confirm_years) ≤ 2.0` · power ≥ 0.50), reusing `axis_screen.floor_at_k`/
     `clause_n_power` verbatim.
   - `lab/discovery/grammar.py` — grammar schema (operator families × ranges × generation budget
     G) with SHA256 pin/drift check.
   - `--lane deep` on `register_search.py` — wires the above two into `open_run`; refuses with
     no manifest write on any conjunct fail, prereg fail, or grammar-hash mismatch, mirroring
     the existing per-lane gate shape (`_require_admission`, `_require_prereg`).
   - `discovery_manifests/burned_segments.json` + `lab/discovery/burned_segments.py` — seeds the
     shared CON window (MNQ, 2025-09-01→2026-08-05, read 2026-08-20) as burned, per dual-panel
     finding B1; a standalone checker, not yet wired into `open_run` (§7 tracks that as forward
     work, named, not claimed).
   - **Named forward work, not built in this ADR's first slice:** GROW-0 harness (Limb A/B/RED),
     charter §4 streak checker, `gates.yml` door-check limb, LOCKED-leg denylist, Rule-0 anchor
     checker, `universe_gate` exit-code propagation. Each ships as its own dated commit against
     this ADR's authorization — no new ADR needed per-slice unless one changes charter-level
     doctrine.
3. **Nothing here changes what a GROW-1 campaign must do.** It is an ordinary deep-lane
   campaign: charter Q-ID, frozen prereg, operator GOs, confirm-read-once, falsification budget.
   The tooling only makes its own K-accounting and grammar-freeze machine-checked instead of
   hand-verified the way DL-1's was.

**Effective:** immediately upon Accept (2026-08-22). **$0 / K=0** — no campaign opens under
this ADR; it authorizes tooling only.

---

## §3 — Alternatives considered

| Alternative | Why not elected |
|---|---|
| Build everything named in Part A before shipping anything | Reproduces the "claimed but unscored" failure the dual-panel review caught in v1 — a large unshipped manifest is exactly as unbinding as v1's prose promises were |
| Fold GROW-0 into the charter's §4 counters (no exemption) | Charges engine-calibration failures against the lane's 2-strike falsification budget for a reason unrelated to the depth premise (H) — GROW-0 tests the tool, not the thesis; conflating them would let a harness bug spend the charter's one falsification budget |
| Skip a ratifying ADR; treat the packet's Part A as self-executing under the charter's existing Accept | The packet's own Boundary line makes the counter-exemption conditional on written ratification — self-execution would leave that ruling unmade, and DL-1's abandonment shows counter-accounting is genuinely load-bearing |

---

## §4 — Falsifier (revert trigger)

**H:** the tooling this ADR authorizes lands in dated, tested slices that a future deep-lane
campaign actually uses (i.e., GROW-1 or later opens via `--lane deep` with the predicate module
and grammar hash-pin, not a hand-verified equivalent the way DL-1 was).

**Revert / FALSIFIED (any limb):**
1. A future campaign opens under `--lane deep` without the predicate refusing an out-of-bound K
   or an under-powered target — the module is unbinding; supersede and repair before reuse.
2. GROW-0's exemption is read as license to exempt a real campaign (GROW-1+) from the charter's
   counters — unauthorized; this ADR's §2.1 names GROW-0 only.
3. The named forward-work list (§2.2 last bullet) is silently claimed complete in a future
   session without its own commit — flag at the next programme audit.

**Trigger check schedule:** first `--lane deep` open attempt, or the 2026-11-08 charter reading,
whichever is earlier.

---

## §5 — Forbidden moves

- Charging GROW-0 against the charter's §4 counters.
- Building `--lane deep` to accept anything the charter's §2.2 conjuncts would refuse.
- Loosening S6/`admission_schema.py`'s mechanism-first predicate to share code with the deep-lane
  predicate — they stay separate modules scoring different thresholds (CAP=1.0 vs 2.0).
- Wiring `burned_segments.py` as a silent auto-pass — an unlisted window is neither burned nor
  clean; the checker must say which.
- Claiming any §2.2-last-bullet item shipped without its own commit reference.
- Any Databento pull, any Pine touch, any arming, any `LEG_MAP` claim.

---

## §6 — Consequences

**Positive:** the charter's K-accounting and grammar-freeze become machine-checked instead of
resting on a human re-deriving `floor_at_k` by hand each campaign (DL-1's actual path); GROW-0
gives the engine a synthetic non-vacuity check before any cached-data campaign spends the
charter's falsification budget on a tooling bug instead of the depth premise.

**Negative (real, stated):** two parallel admission predicates now exist in `lab/discovery/`
(mechanism-first vs deep) — a future reader must know which lane a campaign is on before
reading its refusal reasons; the named forward-work items are real gaps until they land, and a
`--lane deep` campaign opened before the burned-segments checker is wired into `open_run` still
depends on a human pasting the check by hand (no regression from DL-1, but no improvement yet
either).

**Downstream artifacts NOT changed:** `core/` (all), `axis_screen.py` constants, S6/
`admission_schema.py` semantics, the charter's own §2 text, `register_search.py`'s existing
blind/mechanism-first lanes.

---

## §7 — Implementation log (updated per landed slice, not claimed ahead of its commit)

| Date | Slice | Commit |
|---|---|---|
| 2026-08-22 | `deep_lane_admission.py` + `grammar.py` + `--lane deep` wiring + `burned_segments.py`/seed — this session | `a5ee05e` |
| 2026-08-22 | GROW-0 harness (`grow0_dgp.py`/`grow0_scoring.py`/`grow0_harness.py`/`grow0_red_patch.py`, Limb A/B + three RED controls + retry ledger + CLI), built against its own frozen PREREG | `a90e70c` |
| 2026-08-22 | GROW-0's real full-scale invocation (N=5,500/c=7) run for the first time — `RESOLVED` (engine + calibration instrument sound); Part B's filing decision now unlocked for the operator, not decided here | [closure](../briefs/closures/GROW-0-closure-resolved.md) |

---

## §10 — Audit hooks

```bash
# Charter status unaffected (this ADR amends tooling, not the charter's own text):
grep -n "Status:" docs/adr/2026-08-16-deep-iteration-lane-charter.md
# Expected: Accepted, unchanged

# Deep-lane predicate reuses axis_screen arithmetic (no re-derivation):
grep -n "from research_utils.axis_screen import" lab/discovery/deep_lane_admission.py

# --lane deep exists and is distinct from mechanism-first:
grep -n '"deep"' lab/discovery/register_search.py

# Forward-work items not silently claimed (grep returns non-empty until each lands):
grep -n "GROW-0 harness\|streak checker\|gates.yml door-check\|LOCKED-leg denylist" \
  docs/adr/2026-08-22-grow-lane-build-authorization.md
```
