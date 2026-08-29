# ADR 2026-06-06 — Firm-constants single source of truth (`firm_rules` canonical; consumers derive)

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - the ACTIVE_FIRM-selector-mechanism clause only (Phase 4, merged 2026-07-30, PR #572: ACTIVE_FIRM/FIRM_RULES["FXIFY"]/BASELINE_BALANCE deleted outright, not renamed). The broader "one canonical firm_rules.py home for firm constants" principle this ADR established is still honored in spirit — core/dd_protection.py now derives challenge constants from core/historical_challenge.py instead.
**Retain-until:** none
**Decision date:** 2026-06-06
**Authors:** Joshua + claude.ai (Tech Advisor)
**Supersedes:** none
**Related:** `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (layer contract — establishes `core↔core` as a legal edge, which this ADR relies on) · `docs/adr/2026-05-23-allocation-refresh-2.md` (the allocation lock `firm_rules._BASE_RISK` already serves as canonical for)
**Layer:** core (P0 locked modules — change only via the lock cycle); this ADR records the source-of-truth topology, it does not itself perform the edit

---

## §0 — Rule 0 reads (production-source verification)

All three files share commit anchor `dd4e4aa` (verified `git log -1 -- <file>` on 2026-06-06; working tree HEAD `d8dfed6` on branch `ci/fail-closed-path-liveness`, even with `origin/main`). The triplicated constants below were read in full **before** this ADR was framed.

- `core/firm_rules.py` — anchor `dd4e4aa`. **Canonical home (by its own docstring).** `FIRM_RULES["FXIFY"]` carries `max_dd_pct=5.0`, `daily_loss_pct=5.0`, `profit_target_pct=5.0`, `min_trading_days=5`, `inactivity_max_idle_days=60` (percentages as positive numbers). Also `BASELINE_BALANCE = 200_000`, `_BASE_RISK`/`RISK_TIERS`/`BASELINE_RISK` (already declared canonical for live-sizing risk %). Commented extension placeholders for `FundedNext` / `The5ers` / `BrightFunded` already present.
- `core/portfolio_mc.py` — anchor `dd4e4aa`, constants block L37–53. Re-declares: `STARTING_EQUITY = 200_000`, `PROFIT_TARGET = 210_000` (**absolute $**), `DAILY_LOSS_PCT = -0.05` (**signed fraction**), `STATIC_DD_PCT = -0.05`, `MIN_TRADING_DAYS = 5`, `INACTIVITY_LIMIT = 60`. The L43–44 comment *cites* `firm_rules.py:14` as the source for the `60` — then hardcodes it. A comment doing an import's job is the anchor failure mode this ADR closes.
- `core/dd_protection.py` — anchor `dd4e4aa`, constants block L42–45. Re-declares: `STARTING_EQUITY = 200_000`, `PROFIT_TARGET = 0.05` (**unsigned fraction**), `DAILY_LOSS_LIMIT = 0.05`, `STATIC_DD_LIMIT = 0.05`.
- Blast-radius read (external consumers, `git grep` 2026-06-06): the `lab/validation` harness re-exports the constant by attribute — `lab/validation/.../engine.py:58 STARTING_EQUITY = dd_protection.STARTING_EQUITY`, `.../ingest.py:41 STARTING_EQUITY = portfolio_mc.STARTING_EQUITY`, `.../disposition.py:106 portfolio_mc.STARTING_EQUITY`. `lab/validation/sweep/tests/test_sweep_controls.py:180` already asserts `eng.STARTING_EQUITY == dd_protection.STARTING_EQUITY == 200_000` — a pre-existing, single-constant consistency guard. **Blast-radius correction (executor Rule-0 grep, 2026-06-06):** this §0 originally undercounted external consumers as `lab/validation`-only. Additional by-attribute consumers of the in-scope constants exist: `tests/test_mc_anchors.py:43` (imports `STARTING_EQUITY`, `DAILY_LOSS_PCT`, `INACTIVITY_LIMIT`) and `tests/test_inactivity_boundary.py:22` (imports `STARTING_EQUITY`, `INACTIVITY_LIMIT`) read them directly; `scripts/` and closed `docs/briefs/Q-SWAP-*/` research scripts also reference them. All are protected by the same name-preservation constraint and the full-suite gate. **Execution constraint: the public attribute names must survive; only their definitions change.**
- Contract precondition (verified): `check_boundaries.py` lists `("core","core")` as an allowed edge, and `portfolio_mc.py` already does `from .dd_protection import DD_TRIGGER, DD_SCALE`. Intra-core import is sanctioned and already practiced — the duplication is **unforced**.

**Current-values note:** the three encodings currently *agree* numerically (210_000 = 200k × 1.05; −0.05 / 0.05 / 5.0 all mean 5%). This is a **latent hazard, not a live bug.** Nothing miscomputes today; the risk is the next edit.

---

## §1 — Context

The four FXIFY challenge constraints (profit target, daily loss, static DD, min trading days, inactivity) plus starting equity are encoded in **three** `core` modules in **three** incompatible representations — percent-as-number in `firm_rules`, absolute-dollars-and-signed-fractions in `portfolio_mc`, unsigned-fractions in `dd_protection`. `firm_rules.py` already declares itself the canonical config home and already holds every value in its `FIRM_RULES["FXIFY"]` dict, with commented `BrightFunded` extension slots. The two risk-math consumers re-declare the same numbers locally rather than reading the dict. The pre-existing `test_sweep_controls.py:180` equality assertion shows the drift risk was recognized and patched defensively (assert-equal) rather than structurally (single source).

The forcing function is **BrightFunded onboarding** (on the roadmap, per the SNAG scaling plan): a second firm with different parameters turns "three places, three conventions" from latent into active. Adding `FIRM_RULES["BrightFunded"]` while `portfolio_mc`/`dd_protection` still read hardcoded FXIFY literals means the risk math silently keeps computing FXIFY gates against a BrightFunded account — a wrong-but-plausible gate that no current test necessarily catches.

**Decision driver (one sentence):** the same firm rule is the source of truth in three modules at once, so it must have exactly one canonical home before a second firm makes the divergence load-bearing.

---

## §2 — Decision

**Decision:** `core/firm_rules.py` is the **single canonical source** for all firm-challenge constants and starting equity. `core/portfolio_mc.py` and `core/dd_protection.py` **derive** their module-level constants from `firm_rules.FIRM_RULES[ACTIVE_FIRM]` + `firm_rules.BASELINE_BALANCE` (a legal `core→core` import), preserving their existing public attribute names and each module's existing representation. No literal firm-rule numbers are declared anywhere except `firm_rules.FIRM_RULES`.

`firm_rules.py` gains an explicit `ACTIVE_FIRM = "FXIFY"` selector so the derivation source is `FIRM_RULES[ACTIVE_FIRM]`. This makes future firm onboarding a single-line switch (plus the new dict entry) rather than a three-module edit — directly serving the BrightFunded goal. (Selecting the active firm is the *only* new surface; it is not an allocation or rule change.)

**Derivation map (the values each consumer must resolve to — byte-identical to today):**

| Consumer constant | Today (literal) | After (derived from `firm_rules`) |
|---|---|---|
| `portfolio_mc.STARTING_EQUITY` | `200_000` | `BASELINE_BALANCE` |
| `portfolio_mc.PROFIT_TARGET` | `210_000` | `BASELINE_BALANCE * (1 + F["profit_target_pct"]/100)` |
| `portfolio_mc.DAILY_LOSS_PCT` | `-0.05` | `-F["daily_loss_pct"]/100` |
| `portfolio_mc.STATIC_DD_PCT` | `-0.05` | `-F["max_dd_pct"]/100` |
| `portfolio_mc.MIN_TRADING_DAYS` | `5` | `F["min_trading_days"]` |
| `portfolio_mc.INACTIVITY_LIMIT` | `60` | `F["inactivity_max_idle_days"]` |
| `dd_protection.STARTING_EQUITY` | `200_000` | `BASELINE_BALANCE` |
| `dd_protection.PROFIT_TARGET` | `0.05` | `F["profit_target_pct"]/100` |
| `dd_protection.DAILY_LOSS_LIMIT` | `0.05` | `F["daily_loss_pct"]/100` |
| `dd_protection.STATIC_DD_LIMIT` | `0.05` | `F["max_dd_pct"]/100` |

(where `F = firm_rules.FIRM_RULES[firm_rules.ACTIVE_FIRM]`.) Every derivation is mechanical — no representation a consumer's code relies on changes; only the *origin* of the number changes from a local literal to a derived reference.

**Effective:** on acceptance AND completion of the lock cycle for both P0 modules (see §7). This ADR records the topology; it does not perform the edit.
**Scope:** the ten constants in the derivation map. Explicitly NOT in scope: `_BASE_RISK`/allocations (already canonical in `firm_rules`, untouched), `DD_TRIGGER`/`DD_SCALE` (separate dd_protection lock), any numeric value.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo (triplicated literals + the existing equality assert)** | The assert at `test_sweep_controls.py:180` guards one constant (`STARTING_EQUITY`) across two modules; it does not cover `PROFIT_TARGET`/`DAILY_LOSS`/`STATIC_DD`/`INACTIVITY`, nor `firm_rules` itself, nor a second firm. Defensive patching of one cell of a 3×N drift surface. |
| **New `core/lib/firm_constants.py` as the home** | `firm_rules.py` already *is* this file by declaration and content (the FXIFY dict, the BrightFunded slots, the "add firms here" docstring). A new module would create a second canonical-ish home and orphan `firm_rules`. Reuse the declared canon. |
| **Make consumers `import firm_rules` and reference `firm_rules.FIRM_RULES[...]` at every use-site** (no module-level derived constants) | Breaks the `lab/validation` harness, which imports `portfolio_mc.STARTING_EQUITY` / `dd_protection.STARTING_EQUITY` *by attribute*, and breaks `test_sweep_controls.py:180`. The public attribute surface is load-bearing; keep it, re-point its definition. |
| **Normalize all three modules to one representation (e.g. everyone uses signed fractions)** | Scope creep into the consumers' internal math. `portfolio_mc` uses `PROFIT_TARGET` as absolute dollars (`210_000`) in equity comparisons; `dd_protection` uses fractions. Forcing a uniform representation means rewriting use-sites — a behavior-change risk on P0 code for zero correctness gain. Each module keeps its representation; only the source changes. |
| **Bundle this into the `portfolio_mc.py` decomposition** | Two P0 changes in one diff defeats the lock cycle's isolation. The decomposition is maintainability; this is correctness topology. Separate diffs, separate verification. |
| **Edit `firm_rules` to match the consumers' conventions** | Inverts the canon. `firm_rules` is the declared source; consumers derive from it, not vice versa. |

---

## §4 — Falsifier (behavior-preservation invariant / revert trigger)

This is a behavior-preserving refactor, so the falsifier is a correctness invariant rather than an edge hypothesis.

**Hypothesis (H):** deriving the ten constants from `firm_rules` is byte-identical to the current literals — every consumer resolves to the same value pre/post, the full suite stays green, and the live MC anchor reproduces.

**Revert trigger (binary — any one falsifies H and reverts the change):**
1. After the edit, any of the ten derived constants ≠ its pre-edit literal value (checked by the extended consistency test in §10).
2. The full suite (`pytest tests/` + `pytest lab/`) is not green on Python 3.11 post-edit where it was green pre-edit.
3. The default MC anchor does not reproduce `99.83 / 0.17 / 4.37` (median 26d) under the 2026-05-23 allocations post-edit.

If any fires, the derivation introduced drift (or a representation was mis-derived); revert and re-author the derivation row that broke. Do not adjust the gate to match the output (Known Trap #12).

---

## §5 — Forbidden moves

1. **Removing or renaming any of the ten public attributes.** The `lab/validation` harness and `test_sweep_controls.py` import them by attribute. Preserve the names; change only their right-hand side. (Tempting because "just import firm_rules everywhere" looks cleaner — it breaks the harness.)
2. **Changing any numeric value or representation a consumer relies on.** The derivation must reproduce today's exact values in today's units (absolute $ for `portfolio_mc.PROFIT_TARGET`, signed fractions for its DD/loss, unsigned for `dd_protection`). This ADR adds zero behavior. (Tempting to "fix" the unit inconsistency in the same pass — out of scope, behavior-change risk on P0.)
3. **Bundling with the `portfolio_mc.py` file decomposition.** Isolated diff, isolated lock cycle.
4. **Touching `_BASE_RISK` / allocations / `DD_TRIGGER` / `DD_SCALE`.** Different locks; not this decision.
5. **Performing the edit from this ADR without the lock cycle.** Both modules are P0. This artifact is the *why*; the *how* is §7.

---

## §6 — Gate (closure criteria)

**RESOLVED** when ALL hold:
- (a) `firm_rules.py` defines `ACTIVE_FIRM`; `portfolio_mc.py` and `dd_protection.py` derive all ten constants per the §2 map via `from . import firm_rules` (or equivalent legal `core→core` import).
- (b) `git grep` confirms no literal `200_000` / `210_000` / `0.05` / `-0.05` / `60` assigned to the ten named constants outside `firm_rules.FIRM_RULES` (the literals live in one dict).
- (c) The §10 consistency test (extended to all ten constants, all three modules) passes.
- (d) `pytest tests/` and `pytest lab/` green on Python 3.11.
- (e) MC anchor reproduces `99.83/0.17/4.37` (median 26d).

**FALSIFIED** if any §4 revert trigger fires.
**AMBIGUOUS** if a derivation cannot be expressed without a judgment call on a consumer's internal convention (none expected — the §2 map is mechanical — but if one appears, close AMBIGUOUS and surface rather than guessing).

---

## §7 — Execution path (lock cycle + handoff)

Both targets are P0 ("change only via the lock cycle"). The advisor (this session) does not commit. Execution routes as:
1. **Accept this ADR** (Joshua) — flip Status to `Accepted`, stage + commit the ADR alone.
2. **CC handoff brief** (author next, via `brief-authoring` → `references/cc_handoff.md`) spawning the edit with: §0 = `cat` the three constant blocks and report before editing; §2 = apply the §2 derivation map verbatim; §6 = the §10 consistency test + full-suite + MC-anchor reproduction as the spec-compliance gate; status taxonomy DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.
3. **Lock-cycle record** for the two P0 modules per `fxify-challenge` lock doctrine.

This ADR is the parent; the CC handoff is its execution child.

---

## §10 — Audit hooks (runnable)

```bash
# (1) Literals live in exactly one place — no firm-rule literal assigned outside FIRM_RULES.
#     Expect: matches ONLY in core/firm_rules.py (the dict).
git grep -nE '(STARTING_EQUITY|PROFIT_TARGET|DAILY_LOSS|STATIC_DD|INACTIVITY_LIMIT|MIN_TRADING_DAYS)\s*=\s*(-?0\.05|200_?000|210_?000|60|5)\b' -- core/

# (2) Consistency test exists and is extended to all ten constants across the three modules.
#     (Extends the pre-existing single-constant assert at
#      lab/validation/sweep/tests/test_sweep_controls.py:180.)
grep -rn 'firm_rules' tests/ lab/validation/sweep/tests/ | grep -iE 'assert|==' 

# (3) Behavior preservation — full suite green on the CI-matched interpreter.
.venv/Scripts/python -m pytest tests/ lab/ -q   # (PowerShell on Windows)

# (4) Live MC anchor reproduces post-edit.
.venv/Scripts/python core/portfolio_mc.py        # expect 99.83 / 0.17 / 4.37, median 26d

# (5) BrightFunded readiness — onboarding is a one-line ACTIVE_FIRM switch + one dict entry,
#     NOT a portfolio_mc/dd_protection edit. Confirm by grep that neither module hardcodes
#     firm SELECTION (quoted literal / direct index). NOTE (M-AHF, executor 2026-06-06): the
#     bare-'FXIFY' form returns ~18 hits from pre-existing comments/docstrings/print headers
#     that are NOT firm selection; use the quoted-selector form for a runnable hook.
git grep -nE '"FXIFY"' -- core/portfolio_mc.py core/dd_protection.py   # expect: zero hits
```

---

## Verification

```
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-06-06-firm-constants-single-source.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format='%h %ci' -- core/firm_rules.py core/portfolio_mc.py core/dd_protection.py   # expect dd4e4aa
$ sed -n '37,53p' core/portfolio_mc.py   # the six re-declared constants
$ sed -n '42,45p' core/dd_protection.py  # the four re-declared constants
$ sed -n '5,16p'  core/firm_rules.py     # FIRM_RULES["FXIFY"] canonical dict

# Cross-reference verification (blast radius cited correctly)
$ git grep -n 'STARTING_EQUITY = \(portfolio_mc\|dd_protection\)\.STARTING_EQUITY' -- lab/
$ git grep -n 'STARTING_EQUITY == .*== 200_000' -- lab/   # the pre-existing consistency assert
```

## Addendum 2026-08-29 — ACTIVE_FIRM deleted outright, not renamed; canon moved to historical_challenge.py

The 2026-08-29 `adr-decay-audit` full-corpus sweep flagged this ADR `DECAYED_UNDOCUMENTED`: §2/§6
assert `firm_rules.py` "gains an explicit `ACTIVE_FIRM = 'FXIFY'` selector" as live, current
architecture. It no longer is. This addendum is that discharge; the §0 reads, §1 Context, §2
Decision, and all other sections above stay byte-unedited as the historical record (Rule 14).

**Root cause.** `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` Phase 4 (merged
2026-07-30, PR #572, `fc14682`) deleted `ACTIVE_FIRM`, `FIRM_RULES["FXIFY"]`, and `BASELINE_BALANCE`
outright — this ADR is the decision that *instituted* `ACTIVE_FIRM` in the first place, yet it was
absent from the substrate-retirement ADR's own `Supersedes` header block despite being the most
directly affected predecessor of all five. Corrected in the same remediation batch as this
addendum (see that ADR's header, now carrying a `2026-06-06-firm-constants-single-source.md` in-part
line).

**Current state, verified against production (`core/firm_rules.py`, read in full 2026-08-29):**

- The module's own docstring (lines 4-9) records the deletion directly:

  > FXIFY row + ``ACTIVE_FIRM`` + ``BASELINE_BALANCE`` **deleted** (Phase 4). Historical challenge
  > semantics live in ``core/historical_challenge.py`` (opt-in fixture only). Live c1 uses the
  > explicit tier key ``Tradeify_Select_100K`` (rail JSON / ``generate_constants(tier)``).

- `core/firm_rules.py:25` imports `HISTORICAL_CHALLENGE_BASE_RISK` from `historical_challenge` —
  there is no `ACTIVE_FIRM` selector and no `FIRM_RULES["FXIFY"]` row left to select.
- The §2 derivation map (this ADR's core mechanism: `portfolio_mc`/`dd_protection` deriving ten
  constants from `firm_rules.FIRM_RULES[ACTIVE_FIRM]`) no longer describes production code — the
  selector it depended on is gone, not renamed or repointed.
- Live firm selection today is always an explicit `FIRM_RULES` key (e.g. `Tradeify_Select_100K`),
  never a module-level global selector. The broader §1 decision driver — one canonical
  `firm_rules.py` home rather than triplicated literals — is still honored: challenge-era constants
  now derive from `core/historical_challenge.py` instead of being re-declared per consumer, which is
  the same "single source, consumers derive" shape this ADR argued for, just with the challenge
  constants relocated to their own module rather than living in `firm_rules.FIRM_RULES["FXIFY"]`.

This ADR's §10 audit hooks (e.g. hook 5, `git grep -nE '"FXIFY"' ...`) are accordingly stale as
written — they assert absence of a *selector literal* whose surrounding mechanism (`ACTIVE_FIRM`
itself) no longer exists to select anything. Not rewritten in place per Rule 14; a reader should
consult `core/firm_rules.py`'s current docstring and
`docs/adr/2026-07-22-challenge-era-substrate-retirement.md` §2E / Phase 4 for the current topology.
