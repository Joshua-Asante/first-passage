# Q-SIZECOMP-1 — CLOSURE: `RESOLVED` (both limbs confirm)

**Verdict:** `RESOLVED`
**Closed:** 2026-08-23
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-SIZECOMP-1-verdict-preregistration.md`](../pre-registration/Q-SIZECOMP-1-verdict-preregistration.md) — frozen 2026-08-23, same-session as Phase 1 (see that file's process note)
**Successor:** none authored — two forward items named below per §6 `RESOLVED` disposition; naming ≠ opening
**Spend / K:** $0 / K=0
**Live effect:** none — read-only investigation; rail's `r_eff` formula and `tests/test_lifecycle.py` both left byte-identical
**Artifacts:** `docs/briefs/Q-SIZECOMP-1-sizing-composition.md` (parent); this file; pre-registration above

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Limb-A confirms AND Limb-B confirms | both confirmed (below) | ✓ |
| `FALSIFIED` | Limb-A or Limb-B does not confirm as stated | neither failed | — |
| `AMBIGUOUS-HOLD` | Limb-A confirms but Limb-B's arithmetic is dirty, or a grep hit is ambiguous | no grep hits to be ambiguous about; arithmetic clean once a live key was used | — |

**Limb-A (rail composition, A3) — CONFIRMS.** `grep -rn "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops/` → **0 hits** (exit 1). `ops/c1_rail/c1_sizing_host_reference.py:53-55` imports exactly:
```
from dd_protection import BASE_RISK, calculate_protection  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from lifecycle import TIER_MULTIPLIER  # noqa: E402
```
— only `TIER_MULTIPLIER`, as the brief's Section 0 cited. `:280` `r_eff = base_risk * dd_scale * lifecycle_m` — `lifecycle_m` comes from `_read_lifecycle_multiplier()` (`:203-216`), a bare `TIER_MULTIPLIER[tier]` lookup with **no** beta term anywhere in the expression. Cross-check: `core/dd_protection.py:451-452` (update branch) and `:485` (status branch) **do** call `get_effective_multipliers(STRATEGY_KEYS)` and `beta_death_assessment(get_lifecycle_multipliers(STRATEGY_KEYS))` — confirming the asymmetry the brief names: the CLI reaches the full composition, the rail structurally cannot.

**Limb-B (triple-compound reachability + coverage, D4) — CONFIRMS**, with one reproducibility defect surfaced (§4).

*Arithmetic.* Ran the brief's §10 hook verbatim first — it **raises `KeyError: 'Guardian'`** (see §4): `core/firm_rules.py:588-589`'s `_LIVE_BASE_RISK_SLUGS` was narrowed to `("striker", "striker_nas100")` by commit `94041d9` ("Phase C living-key retirement," landed 2026-08-23, same day as but **after** this brief's Rule-0 anchor `027a729`), so `dd_protection.BASE_RISK` no longer carries a `"Guardian"` key. Re-ran with a live key (`"Striker"`) substituted:
```
BASE_RISK keys: ['Striker', 'Striker NAS100']
dd_triggered: True   dd_from_peak: 0.02   multiplier (DD_SCALE): 0.4
scaled_risk['Striker']: 0.0007000000000000001
expect BASE_RISK['Striker']*0.40*0.25:  0.0007000000000000001   -> exact match
```
Went further than the brief's own snippet and reproduced the **actual production call chain** (not a hand-built dict) — 3-of-4 legs (`Guardian`/`Striker`/`Aegis`) forced to `WATCH-1` via `get_effective_multipliers(STRATEGY_KEYS, _state_override=...)`, confirming `beta_death_assessment` fires (`watch_count=3`, `beta_death=True`, `portfolio_multiplier=0.50`), then fed through `calculate_protection(equity, peak, {k: eff[k] for k in BASE_RISK})` at a DD-triggered equity:
```
eff: {'Aegis': 0.25, 'Striker': 0.25, 'Guardian': 0.25, 'Striker NAS100': 0.5}
scaled_risk: {'Striker': 0.0007000000000000001, 'Striker NAS100': 0.0007400000000000001}
Striker        -> BASE_RISK*0.40*0.25  exact match
Striker NAS100 -> BASE_RISK*0.40*0.50  exact match
```
Composition is exact: `BASE_RISK[k] × DD_SCALE × (per-leg lifecycle × beta)` for every live key, both hand-computed and run through the real `get_effective_multipliers`/`beta_death_assessment`/`calculate_protection` chain.

*Coverage.* `grep -n "def test_" tests/test_lifecycle.py` → 22 test functions; read every one. `test_lifecycle_compounds_multiplicatively_with_dd_scale` (`:90-98`) hand-sets a single-leg `0.50` (WATCH-1) lifecycle value and asserts `DD_SCALE(0.40)×0.50=0.20×` — **no `beta_death_assessment`/`get_effective_multipliers` call anywhere in that test**. `test_effective_multipliers_fold_beta_derisk_when_3of4` (`:188-201`) asserts `get_effective_multipliers` folds the 0.50× beta term correctly — **no `calculate_protection` call, no DD term, anywhere in that test**. `grep -n "beta_death_assessment\|get_effective_multipliers\|calculate_protection" tests/test_lifecycle.py` confirms the two symbol families never co-occur inside one test body. No three-way test exists, exactly as the brief claimed.

---

## 2. What the pre-registration predicted vs what happened

Exact match on both limbs — the audit note's A3/D4 findings held up verbatim. The one thing this closure adds beyond the brief's own Section 0: the brief's illustrative arithmetic key (`"Guardian"`) went stale between authoring (2026-08-18, anchor `027a729`) and execution (2026-08-23) because of an intervening, ratified, unrelated commit (`94041d9`, "Phase C living-key retirement") that narrowed the *living* `BASE_RISK` dict to the two Striker legs — Guardian/Aegis moved to `core/historical_challenge.py` under a same-day, separately-ratified ADR (`docs/adr/2026-08-23-strategy-coldstore-phase-c.md`). Neither the brief nor its pre-registration anticipated this.

## 3. What this closure does NOT license

- Does **not** authorize wiring `get_effective_multipliers`/`beta_death_assessment` into `ops/c1_rail/c1_sizing_host_reference.py` — that is the named-not-opened successor decision packet below, and the rail's own header doctrine (fail-toward-zero-size on missing state) deliberately diverges from `lifecycle.py`'s display-safe default; how beta composition should behave in a fail-safe live path is a design decision this $0/K=0 closure has no authority to make (brief §5 forbidden move #2).
- Does **not** claim live money has ever been sized including the beta-death term — `dd_protection.py main()` is a read-only, operator-invoked local-state CLI, never wired to the c1 rail's execution path, and no strategy is deployed on c1 (CLAUDE.md live-execution posture; brief §5 forbidden move #3).
- Does **not** re-derive or challenge `DD_TRIGGER`(0.015)/`DD_SCALE`(0.40)/`BETA_DEATH_COUNT`(3)/`BETA_DEATH_DERISK`(0.50) — all re-read unchanged from `core/dd_protection.py:80-81` and `core/lifecycle.py:48-50`, matching CLAUDE.md's documented values (brief §5 forbidden move #4).
- Does **not** extend to the `core/firm_rules.py`/`core/historical_challenge.py` "Phase C living-key retirement" itself (commit `94041d9`) — that change is a same-day, separately-ADR'd decision this brief's scope does not reach; it is recorded here only because it broke the brief's own illustrative example key, not because this closure evaluates its merits.

## 4. Defects found in the frozen brief (recorded, not repaired)

**One, minor, non-verdict-altering.** The brief's §7/§10 audit-hook Python snippet hardcodes `lc["Guardian"] = 0.50 * 0.50` and `expect = BASE_RISK["Guardian"] * 0.40 * 0.25`. Run verbatim today it raises `KeyError: 'Guardian'`, because `core/firm_rules.py:588-589`'s `_LIVE_BASE_RISK_SLUGS` was narrowed to `("striker", "striker_nas100")` by commit `94041d9` (2026-08-23, landed the same day as — but after — this brief's `027a729` anchor). The brief's own §4 reject-condition ("does NOT return `BASE_RISK[k] × 0.40 × 0.25` exactly") implicitly assumed the snippet would *execute*, not raise; a `KeyError` is a stricter failure mode than either §4 branch anticipated. Substituting any currently-live `BASE_RISK` key (`"Striker"`, used above) reproduces the intended check and it passes exactly — this is a stale-illustration defect in the hook's literal text, not evidence against the composition claim. Recommend the hook be rewritten to pick a key by membership (e.g. `next(iter(BASE_RISK))`) rather than a hardcoded literal, next time it is re-run.

## 5. Lesson candidates

One dated instance — below the two-incident bar for a new named MEMORY.md lesson, but worth a watch note: a same-day, unrelated, ratified commit (`94041d9`) silently broke a brief's own hardcoded audit-hook literal between authoring and execution, five days apart. Same shape as `lesson_ratified_text_edited_alongside_authorized_change` but on a *runnable hook's literal value* rather than prose — audit hooks that hardcode a specific dict key from a *living* (not frozen) constant are fragile to legitimate, unrelated churn. Watch for a second instance before naming a new lesson.

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `RESOLVED` — both limbs confirm.
- **Model update:** The composition asymmetry is real and exactly as the audit note described: the live rail's `r_eff` structurally cannot include the Call-4 beta-death term (no import path exists anywhere under `ops/`), while the diagnostic CLI's `main()` reaches the full three-way compound and computes it exactly right — and that three-way case has never been unit-tested, only its two pairwise halves. Additionally (not anticipated going in): the *living* `BASE_RISK` dict is more volatile than the brief assumed — a same-day, independently-ratified coldstore decision (`94041d9`) already dropped two of the four legs from it, which will affect any future audit hook hardcoding a specific `BASE_RISK` key.
- **Next:** `INTEGRATE`
- **Routing:** INTEGRATE → record the composition asymmetry (this closure) as the evidence-ratified fact; no rail or test code is edited under this brief. Two forward items named, not opened:
  1. **Test-coverage gap** against `tests/test_lifecycle.py` — no test constructs `calculate_protection` fed a `get_effective_multipliers`-derived, beta-death-triggered, DD-triggered lifecycle dict together. A future PR should add e.g. `test_triple_compound_dd_lifecycle_beta` alongside the two existing pairwise tests (`:90-98`, `:188-201`).
  2. **Operator decision packet — rail beta-wiring:** whether and how `ops/c1_rail/c1_sizing_host_reference.py` should compose Call-4 beta-death into `r_eff` before `dry_run=false` is ever considered, given the rail's deliberate fail-toward-zero-size divergence from `lifecycle.py`'s display-safe default. Named here; **not opened** — needs a fresh brief + operator GO.
- **Entry packet:** n/a (Next = INTEGRATE, not ITERATE) — the two forward items above are self-contained pointers, not a continuation of this Q's own thread.
- **Stop rule / re-proposal bar:** n/a — integrated. Re-open only if a future read finds the rail *does* call `get_effective_multipliers`/`beta_death_assessment` (Limb-A would then be stale) or the arithmetic check no longer holds after a future `dd_protection.py`/`lifecycle.py` change (Limb-B would then be stale) — either needs a fresh grounding read, not a re-run of this closure's numbers.
- **Board write:** `STATE.md` forward board —
  `- **2026-08-23** — \`Q-SIZECOMP-1\` closed \`RESOLVED\`. Rail confirmed to never compose Call-4 beta-death into \`r_eff\`; \`tests/test_lifecycle.py\` confirmed to lack the 3-way DD×lifecycle×beta test. Two items named, not opened (test gap; rail beta-wiring operator decision). [\`closure\`](docs/briefs/closures/Q-SIZECOMP-1-closure-resolved.md)`
- **Registry:** `n/a — governance/composition-verification finding, not a strategy-grounds kill; not a rejected_candidates.md object.`

## §10 audit-hook discharge

```
$ grep -rn "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops/
[0 hits — grep exit 1]

$ sed -n '53,55p' ops/c1_rail/c1_sizing_host_reference.py
from dd_protection import BASE_RISK, calculate_protection  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from lifecycle import TIER_MULTIPLIER  # noqa: E402

$ sed -n '449,452p;471,476p' core/dd_protection.py
        # Call-4 stays 4-leg (STRATEGY_KEYS). Living scaled_risk uses BASE_RISK.
        eff = get_effective_multipliers(STRATEGY_KEYS)
        beta = beta_death_assessment(get_lifecycle_multipliers(STRATEGY_KEYS))
[...status-mode branch at :471-485 repeats both calls...]

$ python -c "<brief's verbatim §10 snippet, key='Guardian'>"
Traceback (most recent call last):
  File "<string>", line 7, in <module>
    expect = BASE_RISK['Guardian'] * 0.40 * 0.25
KeyError: 'Guardian'
# — reran substituting a live BASE_RISK key ('Striker'): passes exactly (§1 above)

$ grep -n "def test_" tests/test_lifecycle.py
[22 test functions; test_lifecycle_compounds_multiplicatively_with_dd_scale at :90,
 test_effective_multipliers_fold_beta_derisk_when_3of4 at :188 — the two pairwise tests
 the brief names; no third test combines both symbol families]
```

All hooks ran; one (the `§10` Python snippet) needed a live-key substitution to complete, recorded as a defect in §4 rather than silently patched.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored, both limbs run and scored, same session as operator GO | Joshua (GO) + Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-SIZECOMP-1-closure-resolved.md

# Reproduce the verdict
grep -rn "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops/       # expect 0 hits
sed -n '53,55p' ops/c1_rail/c1_sizing_host_reference.py                            # expect TIER_MULTIPLIER only
sed -n '449,452p;471,476p' core/dd_protection.py                                   # expect get_effective_multipliers + beta_death_assessment
grep -n "def test_" tests/test_lifecycle.py
```
