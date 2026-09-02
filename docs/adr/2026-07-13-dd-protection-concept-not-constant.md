# ADR 2026-07-13 — dd_protection is a concept, not a constant (per-portfolio × per-firm protection instances)

**Status:** Accepted (operator directive 2026-07-12 "keep dd_protection as a concept, not as a constant — it is portfolio and prop firm variable"; recommendation ratified 2026-07-13 §6 `RESOLVED`, no dial adjustments; execution authorized "proceed with 1 and 2")
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - `POLICY_REGISTRY["FXIFY-C2"]` seed-row + `_validate_fxify_seed()` + `ACTIVE_FIRM` retention only. The concept-not-constant frame, the venue-agnostic policy type, and the pre-reg → re-MC → both-halves-gate → ADR admission chain stand (and are now the sole change-control on the DD constants).
**Retain-until:** none
**Decision date:** 2026-07-13
**Authors:** Joshua (decision) + Claude Code Opus 4.8 (recorder/implementer)
**Ratified recommendation (the §0 reads, engine findings, and verification record live there):** [`docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`](../briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md) (§3 + §7)
**Related:** [`2026-05-08-dd-trigger-c2-relock.md`](2026-05-08-dd-trigger-c2-relock.md) (the FXIFY-C2 instance); [`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) (audit item **D2** — this ADR is its frame); [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) (the program whose per-firm geometry made the reframe necessary); [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) (the sibling axis-separation precedent)
**Layer:** risk-control governance + one additive `core/` module — **zero change to any locked constant, allocation, Pine source, MC anchor, or executable line of `dd_protection.py`**.

---

## §0 — Rule-0 reads

Discharged in the ratified recommendation brief §0 (all production files content-read with per-file git anchors at `344c67b`, 2026-07-12): `core/dd_protection.py` @`99b7854`, `core/firm_rules.py` @`0e26a7b`, `core/mc/simulation.py` @`e9be4ec`, `core/mc/modes.py` @`f2be990`, plus the envelope/ADR/campaign docs. Re-verified at implementation (this branch, off `787f734`): the DD_TRIGGER/DD_SCALE literals sit at `dd_protection.py:69-70`; the MVD self-check at `:215-278`; the import-time division hazard at `:63`.

## §1 — Context

`dd_protection` shipped as one rule with two frozen constants (`DD_TRIGGER=0.015`, `DD_SCALE=0.40`), calibrated as **C2** for one venue (FXIFY $200K static-DD challenge) and one portfolio (the locked four-strategy book). The venue closed 2026-07-10; the 2026-07-11 rescope kept the *mechanism* live but flagged its *objective* as owed re-derivation (audit item D2). The 2026-07-12 prop-portfolio program then made the variability concrete: the four target firms span three DD geometries (`static` / `trailing` / `trailing_locking`), different budgets per tier (2.2–6.0%), and intraday-vs-EOD measurement — one constant pair cannot be correct across them, and transplanting FXIFY's pair onto a foreign geometry (what the early prop lab harnesses did) is exactly the un-derived move this ADR forbids.

## §2 — Decision

**The mechanism is the invariant; the numbers are per-instance variables.**

1. **Invariant (the concept):** when the portfolio's remaining room to its **live bust floor** is depleted past a fraction of the firm's DD budget, scale that day's sizing down; clear automatically on recovery to reference; the factor **multiplies** BASE_RISK (compounding with the lifecycle authorization haircut — it never edits any locked parameter); ULP rounding before the threshold compare; single tier. Any instance change ⇒ re-MC + regime-robustness gate + freeze record.
2. **Variables (per portfolio × firm-tier instance):** exactly three — `trigger`, `scale`, `reference_mode` (`static` = frozen dd-from-peak proxy; `trailing` = ratcheting %-of-peak floor; `locking` = ratchet-then-freeze fixed-$ floor; dispatched from `firm_rules` `dd_type`).
3. **FXIFY-C2 is ONE frozen instance,** not the concept: registered as the sole seed row of `core/dd_geometry.py::POLICY_REGISTRY`, import-asserted equal to `dd_protection.py`'s untouched literals (**one-way pin** — the registry pins TO the literals; a rebind in the other direction would fail both AST lock gates, `validate_params.py` and `verify_lock_anchors.py`, which require an `ast.Constant` RHS).
4. **θ\*=0.30 (C2's trigger/budget ratio 1.5%/5%) is provenance-only.** It is NOT a validated transferable invariant — FXIFY-C2's own Q-DDP-1 regime-robustness gate FAILED (recorded in `dd_protection.py`'s header). It may seed a candidate grid; it never validates one.
5. **Reference generalization semantics** (for the future engine branch — NOT built by this ADR): `static` keeps the byte-identical dd-from-peak compare (frozen conservative proxy — re-expressing FXIFY as distance-to-fixed-floor changes the arithmetic and drifts the anchor; the honest asymmetry is that the concept is stricter for trailing types than for its own seed). `trailing` needs only a budget-scaled trigger (fractional DD-from-peak already IS distance-to-floor in budget units). The generalization strictly bites for `trailing_locking` **post-lock** (floor freezes while peak rises → dd-from-peak over-de-risks); the correct reference reuses the same `floor(t)` the bust check already computes (`core/mc/simulation.py:80-82`).

**Landed by this ADR (safe-now, byte-identity provable):** `core/dd_geometry.py` (frozen `ProtectionPolicy` dataclass + `POLICY_REGISTRY` with the FXIFY-C2 seed + side-effect-free `protection_policy()` resolver + `reference_mode_for_dd_type()` helper reading `dd_type` only — immune to the `daily_loss_pct=None` import hazard + import-time one-way-pin self-check) and `tests/core/test_dd_geometry.py`. Nothing on the anchor import path imports the new module.

**Explicitly deferred (do NOT author until a real pre-registered prop candidate + the engine pre-flight exist — ratified trim):** seed-policy heuristics; the `reference_mode`-gated `simulate_path` de-risk branch; swapping the lab harnesses onto the resolver; low-n shrinkage floors; integer-micro snapping; the retry-EV objective. Scoring-run posture in the interim: pass `(dd_trigger, dd_scale)` as **arguments** to `run_seed`/`simulate_path` (default OFF or per-instance) — never edit the module globals.

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep the single constant pair; apply FXIFY-C2 to prop tiers | Un-derived transplant onto foreign DD geometry; C2 is not even regime-robust on its own venue (Q-DDP-1 criterion 5 failed) |
| Rebind `DD_TRIGGER/DD_SCALE = REGISTRY[...]` inside `dd_protection.py` | Breaks both AST lock gates (`ast.Constant` RHS required) and puts the registry on the anchor path — verified against `validate_params.py` + `verify_lock_anchors.py` parsing |
| Re-express FXIFY-static as distance-to-fixed-floor "for consistency" | Changes the live arithmetic once in profit → anchor drift; the frozen proxy is the correct historical fixture |
| Promote θ\*=0.30 to a policy function (trigger = 0.30 × budget everywhere) | Inherits an un-regime-robust ratio as law — the anchor-numerology failure mode; demoted to provenance-only seed |
| Build the full calibration machinery now (seed policy, engine branch, harness swaps) | Design-ahead-of-data for instances that don't exist, under a program with its own 2026-11-08 NO-GO falsifier; adversarial verification mandated the trim |

## §4 — Instance-admission governance (the calibration contract) + falsifier

> **Pointer (2026-08-02):** two of this section's revert-trigger limbs are **DORMANT** —
> see [Addendum 2026-08-02](#addendum--2026-08-02--4-limb-dormancy--10-hook-repair-retirement-back-propagation)
> at the foot of this ADR. The §4 text below is byte-unchanged (Rule 11: never edit the
> falsifier in place); the addendum records which limbs can no longer accrue and why.

**A new (portfolio, firm-tier) instance is admitted to `POLICY_REGISTRY` only by:**
1. **Pre-registering** (BEFORE any grid run; K ledgered against the discovery-family budget): the objective — minimize P(bust against THAT firm's live barrier) at least sizing intervention, subject to a productivity floor (the expression must still reach `profit_target_pct`) — plus the selection rule and the mandatory regime-robustness gate.
2. Running the (trigger × scale) grid through `simulate_path` via None-safe `firm_kwargs` threading (never module constants) — gated on the engine-support pre-flight (`daily_loss_pct=None` import sites + the `bust_trailing` headline aggregation, recommendation §1 F1).
3. Passing the **half-panel regime-robustness gate on both halves** (the gate FXIFY-C2 itself failed — no inheritance).
4. Freezing the winning row with provenance + freeze date + admitting ADR named in the row.

**Open question carried (11-08 D1 material, NOT resolved here):** the FXIFY bust<1% discipline encodes one-shot economics; prop evals allow cheap retries — each firm's objective must be re-derived to its reset/retry EV before a funded-tier instance is admitted. Numbers-before-question stays forbidden.

**Revert trigger (binary):** **Reject (FALSIFIED) if** `core/dd_geometry.py`'s presence makes ANY of {`tests/core/test_mc_anchors.py`, the `dd_protection` MVD import self-check, `validate_params.py`, `verify_lock_anchors.py`, `check_boundaries.py`} go red, OR the anchor stops reproducing 99.83/0.17/4.37 byte-identically on a panel-bearing checkout → then revert the module and re-design; never repair by weakening a gate. **Accept (holds) if** the full gate set stays green with the module present — re-checked at every commit touching `core/` via the standing hooks in §10.

**Revert action:** `git rm core/dd_geometry.py tests/core/test_dd_geometry.py`; supersede this ADR; the concept (operator directive) survives, the architecture gets a fresh brief.

## §5 — Forbidden moves (under this ADR)

- Rebinding `dd_protection.py`'s `DD_TRIGGER`/`DD_SCALE` literals to any computed expression.
- Editing the MVD self-check (`_validate_protection_rule`) or its pin literals for any reframe purpose.
- `dd_protection` importing `dd_geometry` (reverse edge — puts the registry on the anchor path).
- Defaulting an unregistered instance to FXIFY-C2, or an unknown `dd_type` to `static` (silent-fallback transplant).
- Naming θ\*=0.30 a validated invariant anywhere without the regime-gate-failed caveat.
- Admitting a registry row without the §4 chain (pre-registration → grid → both-halves regime gate → freeze + ADR).
- Switching `ACTIVE_FIRM` off FXIFY as a "convenience" for prop calibration runs.
- Authoring the deferred machinery (§2 list) before a real pre-registered candidate + engine pre-flight exist.

## §6 — Consequences

**Positive:** D2's frame is discharged (the dd_protection objective is now explicitly "defend a given portfolio against a given firm's bust geometry", per-instance, replacing the retired challenge-P(pass) framing — the *numeric* successor objective for the self-funded lane stays owed at 2026-11-08/D1); the survivor-scoring pipeline and this registry share one geometry surface; every instance is git-auditable (no runtime registration API).

**Negative (real cost):** a third assertion surface for 0.015/0.40 (after the literals and the MVD pin) — accepted as cheap; the registry is architecture-ahead-of-instances until the first prop candidate survives (bounded: one pure module + test); the reference-generalization semantics in §2.5 are recorded but unexercised until the engine branch lands (flagged, not hidden).

**Downstream artifacts updated by this ADR:** `core/dd_geometry.py` (new), `tests/core/test_dd_geometry.py` (new), `core/dd_protection.py` (docstring pointer ONLY — zero executable change), `CLAUDE.md` §Architecture core-module list + §Protection pointer, `REPO_MAP.md` core row, `STATE.md` forward board.

**NOT changed (explicit):** `DD_TRIGGER`/`DD_SCALE` literals, the MVD self-check, `BASE_RISK`, `ACTIVE_FIRM`, `core/mc/*`, `portfolio_mc`, Pine, `params.toml`, every test pin.

## §10 — Audit hooks (runnable)

> **Pointer (2026-08-02):** hooks 3 and 4 in the block below are **BROKEN** — hook 3 raises
> `KeyError`, hook 4 aborts before running any test. Run the corrected block in
> [Addendum 2026-08-02](#addendum--2026-08-02--4-limb-dormancy--10-hook-repair-retirement-back-propagation)
> instead. The original block is retained unedited as the historical record of what was
> authored on 2026-07-13.

```bash
# Literals never rebound (expect both lines, constant RHS)
grep -n "^DD_TRIGGER = 0.015\|^DD_SCALE = 0.40" core/dd_protection.py

# One-way edge holds (expect NO import of dd_geometry inside dd_protection)
grep -n "import dd_geometry" core/dd_protection.py && echo "REVERSE EDGE — FALSIFIED" || echo "clean"

# Registry pin + full gate set green
python -c "import sys; sys.path.insert(0,'core'); import dd_geometry; print('pin OK:', dd_geometry.POLICY_REGISTRY['FXIFY-C2'])"
python -m pytest tests/core/test_dd_geometry.py tests/core/test_dd_protection.py tests/core/test_mc_anchors.py -q
python scripts/validate_params.py && python scripts/verify_lock_anchors.py && python scripts/check_boundaries.py

# Instance admissions carry their governance chain (every non-seed row names an ADR)
python -c "
import sys; sys.path.insert(0,'core'); import dd_geometry
for k, p in dd_geometry.POLICY_REGISTRY.items():
    assert k == 'FXIFY-C2' or 'adr' in p.provenance.lower(), f'{k} lacks admitting ADR'
print('governance chain OK', sorted(dd_geometry.POLICY_REGISTRY))
"

# theta*=0.30 never promoted without the caveat
grep -rn "0\.30" docs/adr/2026-07-13-dd-protection-concept-not-constant.md | grep -vi "provenance\|seed\|failed\|caveat" && echo "CHECK PROMOTION" || echo "clean"
```

## Addendum — 2026-08-02 — §4 limb dormancy + §10 hook repair (retirement back-propagation)

Per operational-rules Rule 11 (retirement events back-propagate to standing falsifiers),
this addendum records that **two of §4's revert-trigger limbs are DORMANT and cannot
currently accrue**, and that **two §10 audit hooks abort rather than assert**. The §4 text
is **not edited** — no threshold, no gate-set membership, and no constant changes here.

**Surfaced by:** the 2026-08-02 §4 falsifier-input reachability census (31 of 69 ADR
falsifier sections name a mechanically resolvable input; 8 flagged; 5 confirmed by hand).

### Dormant §4 limbs

**Limb A — `tests/core/test_mc_anchors.py` (named in the five-member gate set).** The file
was **deleted 2026-07-24** in `bd92d8e` *("chore(mc): retire Pepperstone executable anchor
(substrate Phase 3)")*, executed under
[`2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md)
§7 Phase 3. It cannot go red or green: it does not exist. Its vendor-free successor for
engine correctness is `tests/core/test_mc_synthetic_engine.py` (+ `test_planted_defects.py`),
per `CLAUDE.md` §Protection.

**Limb B — "the anchor stops reproducing 99.83/0.17/4.37 byte-identically on a
panel-bearing checkout."** Dark under the same event. Verified 2026-08-02:

```
$ python core/portfolio_mc.py --panel pepperstone
portfolio_mc CLI: no registered broker panel. Pepperstone executable anchor retired
2026-07-24 (docs/adr/2026-07-22-challenge-era-substrate-retirement.md section 7 Phase 3).
```

There is no panel-bearing checkout to reproduce against, so the limb has no input.

**Why these can no longer accrue:** both limbs were denominated in the *executable*
Pepperstone anchor. Substrate Phase 3 retired that anchor deliberately; the 99.83/0.17/4.37
triple survives as a **historical record** (`docs/mc_anchor_history.md`, tombstone
`docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md`), not as a
re-runnable gate.

**Re-arm condition:** both limbs re-arm only if a panel-bearing executable anchor is
re-registered (a substrate decision that would need its own ADR). **They do not re-arm by
substituting the synthetic-engine tests** — swapping a named member of the §4 gate set is a
**falsifier amendment**, which this ADR's own §5 reserves to a superseding decision
("silent amendment of the revert trigger is `p`-hacking"). That substitution is therefore
**proposed, not executed** — see Open item below.

### Surviving §4 coverage (Rule 11 requirement (d))

Four of the six named limbs survive, and all four were **verified green 2026-08-02**:

| Limb | Status 2026-08-02 |
|---|---|
| `dd_protection` MVD import self-check | GREEN — `pytest tests/core/test_dd_geometry.py tests/core/test_dd_protection.py` → **23 passed** |
| `scripts/validate_params.py` | GREEN — exit 0 |
| `scripts/verify_lock_anchors.py` | GREEN — exit 0 |
| `scripts/check_boundaries.py` | GREEN — exit 0 |

The decision this ADR records — that `core/dd_geometry.py` may exist without disturbing the
anchor path — **remains covered**. The one-way-edge and literal-rebinding guards (the two
failure modes §4 actually protects against) are carried entirely by the surviving four.
Dormancy here narrows the evidence base; it does not leave the decision uncovered.

### §10 hook defects (mechanical — corrected block below)

1. **Hook 3 raises `KeyError: 'FXIFY-C2'`.** `POLICY_REGISTRY` is `{}` by design — the
   FXIFY-C2 seed row was retired in substrate **Phase 1** (2026-07-22). The hook pins a key
   the repo deliberately removed.
2. **Hook 4 aborts before running anything:** `ERROR: file or directory not found:
   tests/core/test_mc_anchors.py` → `no tests ran`. This is the load-bearing defect — the
   stale path does not merely drop its own limb, it **silently disables
   `test_dd_geometry.py` and `test_dd_protection.py` in the same command**, i.e. the two
   gates that do work returned no signal every time this hook was run.
3. **Hook 5 (governance chain) passes vacuously.** It iterates `POLICY_REGISTRY`; on an
   empty dict the loop body never executes and it prints `governance chain OK []`. Recorded,
   not repaired — the assertion is correct, it simply has nothing to assert over until a
   first instance is admitted (memory lesson: *discipline guards need adversarial tests*).

**Corrected §10 block (supersedes the 2026-07-13 block for execution purposes):**

```bash
# Literals never rebound (expect both lines, constant RHS)
grep -n "^DD_TRIGGER = 0.015\|^DD_SCALE = 0.40" core/dd_protection.py

# One-way edge holds (expect NO import of dd_geometry inside dd_protection)
grep -n "import dd_geometry" core/dd_protection.py && echo "REVERSE EDGE — FALSIFIED" || echo "clean"

# Registry is EMPTY by design post-Phase-1 (was: pin FXIFY-C2, which now KeyErrors)
python -c "
import sys; sys.path.insert(0,'core'); import dd_geometry
print('registry:', sorted(dd_geometry.POLICY_REGISTRY))
assert dd_geometry.POLICY_REGISTRY == {} or all(
    'adr' in p.provenance.lower() for p in dd_geometry.POLICY_REGISTRY.values()
), 'every admitted row must name its admitting ADR'
print('governance chain OK (n=%d)' % len(dd_geometry.POLICY_REGISTRY))
"

# Surviving gate set (test_mc_anchors.py removed — deleted bd92d8e, see Dormant limbs above)
python -m pytest tests/core/test_dd_geometry.py tests/core/test_dd_protection.py -q
python scripts/validate_params.py && python scripts/verify_lock_anchors.py && python scripts/check_boundaries.py

# theta*=0.30 never promoted without the caveat
grep -rn "0\.30" docs/adr/2026-07-13-dd-protection-concept-not-constant.md | grep -vi "provenance\|seed\|failed\|caveat" && echo "CHECK PROMOTION" || echo "clean"
```

### §5 forbidden move now moot (recorded, not edited)

*"Switching `ACTIVE_FIRM` off FXIFY as a 'convenience' for prop calibration runs"* is
**unexecutable**: `ACTIVE_FIRM` was **deleted** in substrate Phase 4 (`fc14682`, 2026-07-30).
The clause is recorded moot — not violated, and not removed. Live firm selection is an
explicit `FIRM_RULES` key (`Tradeify_Select_100K`), which satisfies the clause's intent
(no implicit global firm switch) by construction.

### Open item — operator ratification required

Whether `tests/core/test_mc_synthetic_engine.py` + `test_planted_defects.py` are admitted
**into the §4 gate set** in place of `tests/core/test_mc_anchors.py` is a falsifier
amendment and is **NOT decided here**. Options: (i) supersede this ADR with the amended
gate set; (ii) leave §4 at four live limbs and accept the narrowed evidence base as
recorded above. This addendum takes option (ii) as the status quo pending an operator call.

**NOT changed by this addendum:** `DD_TRIGGER` / `DD_SCALE` literals, the MVD self-check,
`BASE_RISK`, `core/dd_geometry.py`, `core/mc/*`, Pine, `params.toml`, every test pin, and
the §4 falsifier text itself.

## Addendum — 2026-09-01 — Limb C dormancy (`scripts/validate_params.py` retired) + second §10 hook repair

Per operational-rules Rule 11 (retirement events back-propagate to standing falsifiers), this
addendum records that a **third** §4 gate-set member — and a load-bearing piece of the 2026-08-02
addendum's own "corrected" §10 block — has itself gone dormant, one day after that addendum asserted
it green. The §4 text is **not edited**; the 2026-08-02 addendum text is **not edited** either
(append-only) — this section only adds newer facts on top.

**Surfaced by:** the 2026-09-01 cfd-retirement-pair-b file audit.

### Limb C — `scripts/validate_params.py`

Named in the original five-member §4 gate set and re-affirmed GREEN in the 2026-08-02 addendum's
"Surviving §4 coverage" table. The file was retired **2026-08-03** — one day after that addendum's
green check — under [`2026-08-03-params-toml-gate-retirement.md`](2026-08-03-params-toml-gate-retirement.md)
(the `params.toml` hub-validator shape was retired; `scripts/validate_params.py` + its
fixtures/tests removed). Verified 2026-09-01:

```
$ python scripts/validate_params.py
python: can't open file '...\scripts\validate_params.py': [Errno 2] No such file or directory
```

It cannot go red or green: it does not exist. That retirement ADR's §RESOLVED criteria describe
`verify_lock_anchors.py` / `check_pine_manifest` / path-liveness / the recall denylist as absorbing
the retired hub's *other* cross-source comparisons — but this ADR's §4 named `validate_params.py`
itself as a gate-set member, not a proxy for "whatever the hub covered," so that absorption does not
automatically re-arm this limb.

### Compounding defect: the 2026-08-02 "corrected" §10 block is now broken the same way it repaired

That block chains:
```bash
python scripts/validate_params.py && python scripts/verify_lock_anchors.py && python scripts/check_boundaries.py
```
Reproduced 2026-09-01: `validate_params.py` is absent, the shell reports "No such file or directory"
(exit 2), and by `&&` short-circuit **`verify_lock_anchors.py` and `check_boundaries.py` never run**
— the identical failure shape hook 4 had before the 2026-08-02 repair (a dead/missing path silently
disabling the live gates chained after it).

### Surviving §4 coverage, corrected

Of the original five named limbs, only **three now run and were verified green 2026-09-01** (each
run standalone, not chained):

| Limb | Status 2026-09-01 |
|---|---|
| `dd_protection` MVD import self-check | GREEN — `pytest tests/core/test_dd_geometry.py tests/core/test_dd_protection.py` |
| `scripts/verify_lock_anchors.py` | GREEN — exit 0 (run standalone) |
| `scripts/check_boundaries.py` | GREEN — exit 0 (run standalone) |

`tests/core/test_mc_anchors.py` (Limb A, dead since 2026-07-24) and `scripts/validate_params.py`
(Limb C, dead since 2026-08-03) are both gone; the panel-bearing-anchor-reproduction limb (Limb B)
remains dark per the 2026-08-02 addendum. **Three of the original six revert-trigger inputs now
survive** (down from four as of 2026-08-02).

The decision this ADR records — that `core/dd_geometry.py` may exist without disturbing the anchor
path — **remains covered**: the one-way-edge guard and the literal-rebinding guard are the two
failure modes §4 actually protects against, and both are still exercised by the surviving MVD
self-check plus `verify_lock_anchors.py`.

### Corrected §10 block (supersedes the 2026-08-02 corrected block for execution purposes; run each command standalone — do not chain with `&&` after a possibly-retired script)

```bash
# Literals never rebound
grep -n "^DD_TRIGGER = 0.015\|^DD_SCALE = 0.40" core/dd_protection.py

# One-way edge holds
grep -n "import dd_geometry" core/dd_protection.py && echo "REVERSE EDGE — FALSIFIED" || echo "clean"

# Registry still empty by design (Phase 1)
python -c "import sys; sys.path.insert(0,'core'); import dd_geometry; print(sorted(dd_geometry.POLICY_REGISTRY))"

# The two live process gates -- run standalone, NOT chained with && after
# scripts/validate_params.py (retired 2026-08-03; chaining after a missing
# script silently skips everything that follows, per this addendum)
python scripts/verify_lock_anchors.py
python scripts/check_boundaries.py

# theta*=0.30 never promoted without the caveat
grep -rn "0\.30" docs/adr/2026-07-13-dd-protection-concept-not-constant.md | grep -vi "provenance\|seed\|failed\|caveat" && echo "CHECK PROMOTION" || echo "clean"
```

> ⚠ **2026-09-01 reader-intercept:** the "not decided here" / option-(ii)-status-quo framing below is
> superseded by direct operator ruling the same day — see "Addendum 2026-09-01 (operator ruling)"
> below. Option (i) was elected: the §4 gate set is narrowed to the three surviving limbs. This
> paragraph is left unedited as the record of what this addendum originally proposed.

### Open item — operator ratification required (unresolved, same shape as the 2026-08-02 open item)

Whether to formally amend the §4 gate set (dropping `test_mc_anchors.py` and `validate_params.py`,
and naming explicit successors) is a falsifier amendment and is **not decided here**. Options: (i)
supersede this ADR with an amended, narrower gate set; (ii) leave §4's text at five named limbs and
accept the further-narrowed evidence base (now three of six original inputs live) as recorded above.
This addendum, like its predecessor, takes option (ii) as the status quo pending an operator call.

**NOT changed by this addendum:** `DD_TRIGGER`/`DD_SCALE` literals, the MVD self-check, `BASE_RISK`,
`core/dd_geometry.py`, `core/mc/*`, Pine, `params.toml` (already gone), every test pin, the §4
falsifier text itself, and the 2026-08-02 addendum text itself (append-only).

## Addendum 2026-09-01 (operator ruling) — §4 gate set narrowed to three limbs

**Ruling (direct operator instruction, 2026-09-01): elect option (i) above.** The §4 revert-trigger
gate set is narrowed, going forward, to the three limbs confirmed live in the addendum above:

- `dd_protection` MVD import self-check
- `scripts/verify_lock_anchors.py`
- `scripts/check_boundaries.py`

`tests/core/test_mc_anchors.py` and `scripts/validate_params.py` are **dropped as gate-set members**
— both are deleted files that cannot go red or green, and their continued presence in the §4 text
made the falsifier partially unevaluable rather than partially failing. No successor test is named
in their place by this ruling — that is a separate question (the 2026-08-02 addendum's own open item,
whether `test_mc_synthetic_engine.py` + `test_planted_defects.py` are admitted into the gate set,
remains genuinely open and is **not** resolved by this narrowing).

**Effective statement of §4's revert trigger from this date forward:** Reject (FALSIFIED) if
`core/dd_geometry.py`'s presence makes ANY of {the `dd_protection` MVD import self-check,
`verify_lock_anchors.py`, `check_boundaries.py`} go red → then revert the module and re-design;
never repair by weakening a gate. Accept (holds) if this narrower gate set stays green with the
module present. **The anchor-reproduction limb (99.83/0.17/4.37 byte-identical reproduction) is
dropped, not retained as an unevaluable fourth condition** — it stays dark on a checkout without
the retired Pepperstone panel registration (per the 2026-08-02 addendum above), and a narrowing
whose own trigger text still names a limb that can't be evaluated isn't actually the three-limb
gate it claims to be. It re-enters this trigger only if a panel-bearing checkout becomes available
again — that is a fresh re-arm question, not something this ruling decides.

**What does not change:** the original §4 text above stays byte-unedited as the historical record
(Rule 14/Trap #12) — this addendum is the operative amendment, not a rewrite. `DD_TRIGGER`/`DD_SCALE`
literals, the MVD self-check's own logic, `BASE_RISK`, `core/dd_geometry.py`'s design, `core/mc/*`,
Pine, and every surviving test pin are untouched. §5 Forbidden moves is unaffected. The 2026-08-02
addendum's own separate open item (admitting new tests) stays open, unresolved by this ruling.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13 | Initial acceptance + safe-now module landed | Joshua + Claude Code |
| 2026-08-02 | Addendum: §4 limbs A (`test_mc_anchors.py`, deleted `bd92d8e`) and B (panel-bearing anchor reproduction) flagged DORMANT under substrate Phase 3; four surviving limbs verified green; §10 hooks 3-4 (KeyError / abort-before-run) corrected in-addendum; §5 `ACTIVE_FIRM` clause recorded moot post-Phase-4. No threshold, constant, or §4 gate-set membership change. | Joshua + Claude Code (falsifier reachability census) |
| 2026-09-01 | Addendum: Limb C (`validate_params.py`) also retired 2026-08-03; the 2026-08-02 addendum's own "corrected" §10 chain silently broken the same way; three of six original revert-trigger inputs now survive; corrected standalone §10 block supplied | Claude Code (ADR-corpus reconciliation sweep) |
