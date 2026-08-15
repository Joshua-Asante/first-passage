# Cursor Handoff — Lifecycle Call-1 rolling-PF sigma-harness + tier-demotion state writer

**Date:** 2026-07-14
**Parent session:** Claude Code operator session (Joshua + Claude) — the session authoring the open Phase-2 lifecycle build handoffs. **Cursor builds the two data-dependent Call-1 Phase-2 items** (`core/lifecycle.py:21-23` explicitly defers them: *"Writing state (a Call-1 tier demotion) is item 3, not built here — a human hand-edits lifecycle_state.json in the interim"*), as new `lab/` tooling that imports `core/lifecycle` read-only.
**Spawn target:** Cursor (frozen-spec implementation — `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`; §0.5 uses the Cursor recommended-defaults variant). Deps are stdlib + `numpy` only — already on the anchor path, no new deps.
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** Strategy-lifecycle ADR (`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`) — this is the **undelivered T4 artifact (adoption ADR §7)**: the Call-1 σ-source + harness + tier-demotion state writer. Its absence is why the Call-1 first evaluation (`docs/methodology/strategy_lifecycle.md`, first eval **2026-08-08**) is currently forced-AMBIGUOUS for lack of a data feed. This build supplies the machinery; it does not supply live fills.
**Authority:** Joshua (CEO). CC authored this brief; Cursor executes. **No commit/merge without Joshua's go.** Named locked surfaces Cursor must NOT touch (ADR 2026-07-14 test 1): `core/lifecycle.py`, `core/dd_protection.py`, `core/firm_rules.py`, `core/mc/*`, `core/config/params.toml`, any Pine source, and `ACTIVE_FIRM` / any `FIRM_RULES` tier. The harness **imports** `core/lifecycle` read-only and **writes only** `lifecycle_state.json` (runtime state, gitignored/local-only). **Surface-scope note:** that file resolves to `core/lifecycle_state.json` (`STATE_FILE = Path(__file__).parent / …`), so the write does land physically inside `core/` — but it is gitignored runtime state, not a code surface. The "no `core/*` touch" gate throughout this brief means **no git-tracked `core/` file is modified**; the §10 `git diff --stat -- core/ ops/` hook encodes exactly that (a gitignored write shows no diff).

> ⚠ **READER INTERCEPT 2026-08-11 (Rule-7 DRY F15) — banner only; frozen body unedited below.** The phrase *"the automated rail is unbuilt"* was true at handoff date (2026-07-14). The c1 rail is now **built, warm, and disarmed** with **no strategy deployed** — posture owner [`CLAUDE.md`](../../../CLAUDE.md) §Live-execution posture · [`S1 ADR`](../../adr/2026-08-07-loop-s1-environment-ratification.md). The build-ahead-of-data instruction still holds: there are still **no strategy-signal fills**, so rolling live PF has no live source; synthetic PF remains the correct harness path.
>
> **Build-ahead-of-data (read first).** There are **no live fills anywhere** — manual trading is retired (`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`) and the automated rail is unbuilt. So *"rolling live PF"* has **no live source today**; `strategy_lifecycle.md:37` names this the "provisional-until-data" state (ADR §6 AMBIGUOUS clause governs; re-confirm 2026-11-08 if the trade count is short). Build + unit-test this harness **entirely against synthetic PF series**, exactly as the prop survivor-scoring harness was built-ahead-of-candidate (`docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md`). The live-PF wiring is explicitly **out of scope** — the harness accepts PF as an input. The below-min-trade-count case MUST report **AMBIGUOUS**, never crash and never fabricate a demotion.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing a line of code. If repo state contradicts anything in §1/§2 below, return `NEEDS_CONTEXT` with the discrepancy quoted — do not resolve it yourself (ADR 2026-07-14 test 2: Cursor never resolves a spec ambiguity unilaterally).

- `core/lifecycle.py` (FULL) — report:
  - `decay_breach(rolling_pf, baseline_pf, pf_sigma, k_sigma=1.0)` (lines 139–146): the exact predicate `rolling_pf < (baseline_pf - k_sigma * pf_sigma)`, the **ratified `k=1.0`**, the **strict `<`** ("sitting exactly on the floor is not yet a breach"), and the docstring note *"A single-window breach; demotion requires 2 consecutive breaches (caller-tracked)."* — the 2-consecutive tracking is the harness's job.
  - `load_lifecycle_state()` (lines 58–73): the on-disk schema is a JSON object `{strategy: tier}`; it validates keys ⊆ `STRATEGY_KEYS` and each tier ∈ `TIER_MULTIPLIER`, raising `ValueError` otherwise; an absent file returns `{}`.
  - `STRATEGY_KEYS` (line 40) = `frozenset({"Guardian", "Striker", "Aegis", "Striker NAS100"})` — note "Striker" is the DJ30 key and "Striker NAS100" is the NAS key. Report these verbatim (they differ from the baselines.md row titles — see §0.5(A)).
  - `TIER_MULTIPLIER` (lines 33–38): `AUTHORIZED 1.00 / WATCH-1 0.50 / WATCH-2 0.25 / RETIRED 0.00`; `DEFAULT_TIER = "AUTHORIZED"` (line 39); `_LADDER_ORDER` (line 43).
  - `STATE_FILE = Path(__file__).parent / "lifecycle_state.json"` (line 55): runtime state, gitignored/local-only like `accounts.json`; **absent ⇒ every strategy AUTHORIZED @ 1.0×**.
  - `autonomous_demote(tier)` (lines 158–166): AUTHORIZED/WATCH-1 step **down** via `next_tier_down`; WATCH-2 and RETIRED return unchanged — **the autonomous floor is WATCH-2; WATCH-2→RETIRED is operator-gated (Call 5).** Report `next_tier_down` (lines 149–155) too.
  - Confirm `_validate_ladder()` runs at import (line 207) — importing the module is safe and side-effect-only-validates.
- `docs/methodology/strategy_lifecycle.md` — report **Call 1 in full** (lines 30–37): metric = rolling live PF vs its MC/backtest baseline; **floor = `[baseline PF − 1.0σ of the MC PF distribution]`**; **2 consecutive** review windows → demote one tier (→ WATCH-1); σ=1.0 (tighter than a kill-trigger's 2σ *because the action is reversible*); consecutive count = 2; and the **provisional-until-data** caveat (line 37: min trade count, ADR §6 AMBIGUOUS, re-confirm 2026-11-08). Report **Call 4** for context (lines 75–81: the 2-of-4 soft-flag / 3-of-4 beta-death portfolio trigger — NOT this harness's job, but the reason per-leg tier state exists) and the **Implementation status** line 115: *"Pending — data-dependent Phase 2 code: (a) Call-1 σ-source + harness (reads baselines.md + a live-PF source; applies decay_breach/autonomous_demote; writes demotions into lifecycle_state.json)"* — **this handoff is that exact item.**
- `.claude/skills/trade-csv-reconcile/references/baselines.md` — report the per-strategy baseline **PF** the rolling PF is compared against: Guardian Gold v5.5 PF **3.750** (line 61), Striker DJ30 v4.5 PF **3.373** (line 87), Striker NAS100 v1 PF **3.717** (line 116), Aegis-Reversion v4.3 PF **4.188** (line 143). Report the **caveat** (line 24–27: DD is trade-close). Note: the "values are gross-of-swap" caveat is real but is documented in `CLAUDE.md` / the trade-csv-reconcile SKILL.md, **not** in `baselines.md` itself — do not expect a §Notes header here. Also note the row-title → `STRATEGY_KEYS` mapping problem for §0.5(A).
- `core/dd_protection.py` (READ-ONLY) — confirm the lifecycle multiplier is consumed **only** in the risk_pct sizing path: `calculate_protection(equity, peak, lifecycle=None)` at line 189, with `scaled_risk = {k: v * multiplier * lifecycle[k] ...}` at line 216, fed by `get_effective_multipliers(BASE_RISK.keys())` at lines 437/461. Report this to confirm **the haircut lives HERE** — so the writer must write only the *tier*, never apply the multiplier (no double-count; §5).
- `core/mc/modes.py` and `core/mc/simulation.py` (READ-ONLY) — determine whether the MC engine already emits a **per-sim PF distribution** that σ can be drawn from, or whether the harness must compute PF per bootstrap draw. Report: `run_seed(...)` (simulation.py lines 131–181) returns `{"outcomes", "days_to_pass", "max_dds", "bust_attribution"}` — **no PF field**; `compute_default_config(...)` (modes.py lines 242–318) aggregates `pass_rate`/`bust_rate`/`p99_dd`/etc. — **also no PF**. Report the daily-panel builders `build_daily_panel` / `build_week_blocks` (modes.py lines 133–134, compatibility aliases; canonical defs in `core/mc/ingest.py`) that produce the per-day strategy-P&L blocks a PF-per-draw computation would consume. **If your read confirms no PF distribution is emitted, that confirms §0.5(B)'s recommended default; if you find one I missed, bounce `NEEDS_CONTEXT`.**
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — report §2 (the three-question routing test + test 1 named-locked-surfaces / test 2 no-unilateral-spec-resolution) — this governs the whole handoff.
- `git log -1 --format='%h %ci' -- core/lifecycle.py` and the same for `docs/methodology/strategy_lifecycle.md` — report both as your build anchors.
- `scripts/check_boundaries.py` — report the import contract (`lab→{core,governance,lab}`; `lab↔ops` isolation). This harness lives in `lab/`, imports `core/lifecycle` read-only, and never touches `ops/`.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; **confirm or challenge in the Phase-0 response.** Set `Status: NEEDS_CONTEXT` until resolved. Cursor applies each default unless its Phase-0 read contradicts it, in which case it bounces the conflict.

- **(A) Strategy-key mapping (baselines.md rows → `STRATEGY_KEYS`).** The lifecycle state keys are `{"Guardian", "Striker", "Aegis", "Striker NAS100"}` (`lifecycle.py:40`), but baselines.md titles the rows "Guardian Gold v5.5", "Striker DJ30 v4.5", "Striker NAS100 v1", "Aegis-Reversion v4.3". **Recommended default:** the harness carries an explicit, unit-tested mapping dict `{"Guardian": Guardian-PF, "Striker": DJ30-PF, "Aegis": Aegis-PF, "Striker NAS100": NAS100-PF}` whose keys are asserted `== sorted(core.lifecycle.STRATEGY_KEYS)` at load time (so a future key rename fails loudly), and whose baseline PF values are **parsed from baselines.md, not hardcoded** (mirroring the survivor-scoring harness's "parse from the file, never hardcode" discipline). Confirm, or flag if you find a canonical mapping already in the repo.
- **(B) Source of `pf_sigma` (σ of the MC PF distribution).** Your Phase-0 read of `core/mc/*` should confirm the engine emits **no per-sim PF distribution** (`run_seed` returns outcomes/days/DD/attribution only). So σ has no ready-made source. **Recommended default:** the harness computes σ itself by **computing PF per bootstrap draw** over the existing week-block daily panel — for each of the `SIMS_PER_SEED × len(SEEDS)` draws, `PF_draw = Σ(positive daily P&L) / |Σ(negative daily P&L)|` for that strategy's contribution, then `pf_sigma = np.std(PF_draws)` — and this σ-derivation is a **separate, independently-testable pure function** that takes a panel/blocks array as input (so it is unit-testable on a synthetic panel and does NOT require re-running the locked anchor). It must **not** import or mutate any `core/mc` module state, only read the panel it is handed. **This is the single most load-bearing design decision in the build** — if your Phase-0 read shows the engine *does* emit a PF distribution, or shows the σ should instead come from live-PF window variance rather than the MC panel, bounce `NEEDS_CONTEXT` rather than guess. (`strategy_lifecycle.md:35` says "1.0σ of the MC PF distribution" — MC, not live-window — which is why the default draws σ from the panel.)
- **(C) Rolling-PF input contract (build-ahead-of-data).** No live fills exist. **Recommended default:** the harness's public entry point accepts, per strategy, a `rolling_pf: float | None` (the caller-supplied rolling live PF over the review window) plus a `trade_count: int`; it does **not** parse any fill CSV or invent a live feed. When `trade_count < MIN_TRADE_COUNT` (a named constant the harness exposes; recommended provisional value **30**, clearly logged as a placeholder pending the 2026-08-08 review's pre-registration — do NOT treat it as a ratified threshold) or `rolling_pf is None`, that strategy's window result is **AMBIGUOUS** and contributes **no breach** to the consecutive counter. Confirm the input contract and the AMBIGUOUS-on-thin-data rule; challenge the placeholder count if Phase-0 reveals a pre-registered value.
- **(D) Consecutive-window state persistence.** `decay_breach` is single-window; demotion needs **2 consecutive** (`lifecycle.py:145`, `strategy_lifecycle.md:36`). That per-strategy consecutive-breach counter must persist across harness runs. **Recommended default:** persist it in a **separate** harness-owned JSON file under `lab/` (e.g. `lab/discovery/lifecycle_call1/breach_state.json`), NOT inside `lifecycle_state.json` — the latter is `core/lifecycle`'s validated tier interface with a strict `{strategy: tier}` schema (`lifecycle.py:58-73`) that would reject extra fields. The harness writes `lifecycle_state.json` **only** on a confirmed 2nd-consecutive breach, and only the tier value from `autonomous_demote`. Confirm the two-file split.
- **(E) Output artifact shape.** **Recommended default:** one JSON report per harness run — per strategy: `{rolling_pf, baseline_pf, pf_sigma, floor, breached: bool, consecutive_count, window_result: BREACH|CLEAR|AMBIGUOUS, tier_before, tier_after, demoted: bool}` plus a top-level `state_file_written: bool` and the exact `lifecycle_state.json` delta if any. Every baseline/σ number carries its provenance (parsed source + line). Confirm or propose an alternative.

---

## §1 — Context

The strategy-lifecycle ADR ratified a Call-1 decay rule — *rolling live PF below `[baseline PF − 1.0σ of the MC PF distribution]` for 2 consecutive windows → demote one tier* — and landed its **pure logic** (`decay_breach`/`autonomous_demote`, `core/lifecycle.py`), but explicitly deferred the **data feed + state writer** to "item 3," with a human hand-editing `lifecycle_state.json` in the interim (`lifecycle.py:21-23`; `strategy_lifecycle.md:115`). That gap is why the Call-1 first evaluation (2026-08-08) is forced-AMBIGUOUS. This handoff builds that missing machinery. Because there are **no live fills** (manual trading retired), the build is infrastructure-ahead-of-data: it must be correct and fixture-proven before any live PF exists to run through it.

**What Cursor is asked to produce:**
- `lab/discovery/lifecycle_call1/sigma_harness.py` (or a small package `lab/discovery/lifecycle_call1/`) implementing, as composable pure functions:
  - a **baselines.md PF loader** parsing per-strategy baseline PF, keyed to `core.lifecycle.STRATEGY_KEYS` (§0.5(A));
  - a **`pf_sigma` computer** — PF-per-bootstrap-draw σ over a supplied panel/blocks array (§0.5(B)), independently testable, importing no `core/mc` module state;
  - a **decay evaluator** calling `core.lifecycle.decay_breach(rolling_pf, baseline_pf, pf_sigma, k_sigma=1.0)` (import read-only), returning `BREACH | CLEAR | AMBIGUOUS` per strategy (AMBIGUOUS on thin/`None` data, §0.5(C));
  - a **2-consecutive-window tracker** persisted in a harness-owned file (§0.5(D));
  - a **tier-demotion state writer** that, on a confirmed 2nd consecutive breach, steps the tier down via `core.lifecycle.autonomous_demote` (WATCH-2 floor, never auto-RETIRE) and writes/updates `lifecycle_state.json` in the exact `{strategy: tier}` schema `load_lifecycle_state` validates.
- A top-level driver/CLI emitting the §0.5(E) report.
- Synthetic-fixture tests for every function, including the AMBIGUOUS-on-thin-data path, the strict-`<` boundary (rolling PF exactly on the floor is NOT a breach), the single-breach-does-not-demote path, the 2-consecutive-breach demotion, and the WATCH-2 autonomous floor (a WATCH-2 leg breaching again does **not** move to RETIRED).

**What Cursor is NOT asked to do:** edit `core/lifecycle.py`, `core/dd_protection.py`, or any `core/*` file; **apply the lifecycle multiplier haircut** (it lives in `dd_protection.py`'s risk_pct layer — the harness writes the tier only, §5); invent or wire a live-PF fill source (out of scope — PF is an input); auto-RETIRE a strategy (WATCH-2 is the autonomous floor); switch `ACTIVE_FIRM`; re-run or re-anchor the locked MC (the σ computer reads a supplied panel, it does not touch the anchor path); decide any 2026-08-08 review disposition.

---

## §2 — Execution plan

TDD throughout; every step's tests run offline on synthetic fixtures. No test requires live fills or a re-run of the locked anchor.

### Step 2.1 — baselines.md PF loader + STRATEGY_KEYS mapping
- **Inputs:** `.claude/skills/trade-csv-reconcile/references/baselines.md`; `core.lifecycle.STRATEGY_KEYS` (§0.5(A)).
- **Action:** parse the four per-strategy baseline PF values from baselines.md (never hardcode); return a dict keyed by `STRATEGY_KEYS`; assert its keyset `== set(core.lifecycle.STRATEGY_KEYS)` at load, raising on mismatch.
- **Expected output:** loader + tests (parses the real file to Guardian 3.750 / Striker 3.373 / Aegis 4.188 / Striker NAS100 3.717; a corrupted/missing-PF fixture raises rather than silently defaulting; a mutated `STRATEGY_KEYS` fixture raises the keyset assertion).
- **Per-step gate:** grep proves no PF literal (`3.750`/`3.373`/`3.717`/`4.188`) anywhere outside this loader's tests.

### Step 2.2 — `pf_sigma` computer (PF-per-draw σ over a supplied panel)
- **Inputs:** §0.5(B) resolution; a synthetic week-block/daily-panel array (the test supplies it; the real caller would pass the locked panel's blocks, but this build does NOT run the anchor).
- **Action:** pure function `pf_sigma_from_panel(daily_pnl_blocks, strategy, n_draws, seed) -> float` computing `PF_draw = Σ(positive) / |Σ(negative)|` per bootstrap draw, returning `np.std` of the draws. Imports no `core/mc` module state; reads only its argument.
- **Expected output:** function + tests (a deterministic synthetic panel yields a known σ under a fixed seed; an all-wins draw handles the zero-loss denominator explicitly — decide and TEST the convention, do not let it silently `inf`/`nan` into `decay_breach`).
- **Per-step gate:** the function does not import `portfolio_mc`/`modes`/`simulation` module-level state; grep proves it.

### Step 2.3 — decay evaluator (calls `decay_breach`, read-only) + AMBIGUOUS gate
- **Inputs:** Step 2.1 baseline PF, Step 2.2 σ, caller-supplied `rolling_pf`/`trade_count` (§0.5(C)); `core.lifecycle.decay_breach`.
- **Action:** per strategy, if `trade_count < MIN_TRADE_COUNT` or `rolling_pf is None` → `AMBIGUOUS` (no breach); else call `decay_breach(rolling_pf, baseline_pf, pf_sigma, k_sigma=1.0)` and map `True→BREACH`, `False→CLEAR`.
- **Expected output:** evaluator + tests: strict-`<` boundary (rolling PF `== baseline − σ` → CLEAR, not BREACH); a clear breach; thin trade count → AMBIGUOUS with zero breach contribution; `rolling_pf=None` → AMBIGUOUS.
- **Per-step gate:** the harness **calls** `core.lifecycle.decay_breach` — no reimplemented `rolling_pf < baseline - kσ` inequality anywhere in the harness; grep proves it.

### Step 2.4 — 2-consecutive-window tracker (harness-owned state)
- **Inputs:** §0.5(D) resolution; Step 2.3 per-window results.
- **Action:** load/persist a per-strategy consecutive-breach counter in `lab/discovery/lifecycle_call1/breach_state.json` (harness-owned, NOT `lifecycle_state.json`). BREACH increments; CLEAR resets to 0; AMBIGUOUS leaves the counter unchanged (a data-gap window neither advances nor resets — confirm this in §0.5(C) if you disagree, but the default is "AMBIGUOUS is inert").
- **Expected output:** tracker + tests (BREACH→BREACH reaches count 2; BREACH→CLEAR→BREACH stays at 1; BREACH→AMBIGUOUS→BREACH — assert the chosen semantics explicitly).
- **Per-step gate:** the tracker never writes `lifecycle_state.json`; only Step 2.5 does.

### Step 2.5 — tier-demotion state writer (calls `autonomous_demote`, WATCH-2 floor)
- **Inputs:** Step 2.4 counter; `core.lifecycle.load_lifecycle_state`, `autonomous_demote`, `TIER_MULTIPLIER`.
- **Action:** on a confirmed 2nd consecutive breach for a strategy, read the current tier via `load_lifecycle_state` (absent/unlisted ⇒ `AUTHORIZED`), compute the next tier via `autonomous_demote` (AUTHORIZED→WATCH-1→WATCH-2; WATCH-2/RETIRED unchanged), and write the updated `{strategy: tier}` object to `lifecycle_state.json` — validating the written object round-trips through `load_lifecycle_state` without error. Reset that strategy's consecutive counter to 0 after a demotion.
- **Expected output:** writer + tests: AUTHORIZED + 2 breaches → WATCH-1 written and re-loadable; **WATCH-2 + 2 breaches → stays WATCH-2** (autonomous floor, never auto-RETIRE — the single most important assertion in this step); a written state file passes `core.lifecycle.load_lifecycle_state`.
- **Per-step gate:** grep proves the writer applies **no multiplier** and calls `autonomous_demote` (never a hand-rolled ladder step); the written schema is exactly `{strategy: tier}`.

### Step 2.6 — top-level driver + report
- **Inputs:** all prior steps; §0.5(E) report shape.
- **Action:** a driver/CLI accepting per-strategy `rolling_pf`/`trade_count`, running 2.1→2.5, emitting the JSON report.
- **Expected output:** driver + one synthetic end-to-end test (a candidate breaching 2 consecutive windows demotes exactly one tier and the report's `state_file_written` is `True`; an all-AMBIGUOUS run writes nothing and reports every strategy AMBIGUOUS).
- **Per-step gate:** e2e green offline; `check_boundaries` green; no `ops` import; no `core/*` diff.

### Step 2.7 — Closure report
Post the §6-format closure report.

---

## §4 — Falsifiable hypothesis

**N/A — build task, no hypothesis under test.** This handoff builds the Call-1 σ-source + harness + state writer; it runs no live evaluation and asserts no decay verdict. The parent gate it feeds: the **Call-1 first evaluation, 2026-08-08** (`strategy_lifecycle.md:37,115`), which this machinery makes *computable* once a live-PF source exists — but which remains ADR-§6 AMBIGUOUS until the trade count clears the (yet-to-be-pre-registered) minimum. A `DONE` here is **never** a claim that any strategy has decayed or been demoted; it is a claim that the machinery is built and fixture-proven.

---

## §5 — Forbidden moves

- **Editing `core/lifecycle.py`, `core/dd_protection.py`, or any `core/*` file.** These are named locked surfaces (ADR 2026-07-14 test 1). The harness **imports** `core.lifecycle` read-only and writes only `lifecycle_state.json`. A demotion is a *state write*, never a code edit — `autonomous_demote`/`decay_breach` are consumed, never reimplemented or "improved."
- **Applying the lifecycle multiplier haircut in the harness.** The haircut lives in `dd_protection.py` at `scaled_risk = BASE_RISK × multiplier × lifecycle` (line 216), consumed via `get_effective_multipliers`. The harness writes the **tier string only**; if it also scaled risk, the size would be double-counted. This is *the* trap — the two surfaces (state writer here, sizing there) must never both apply the factor.
- **Auto-RETIRE.** Autonomous demotion floors at **WATCH-2** (`autonomous_demote`, Call 5). Only the operator sets RETIRED. A harness that steps WATCH-2→RETIRED is an integrity failure.
- **Inventing a live-PF feed.** No fill source exists; PF is a harness **input**. Do not parse a CSV, scrape DXTrade, or fabricate a rolling PF. Thin/absent data → AMBIGUOUS, not a guessed number.
- **Reimplementing the breach inequality or the tier ladder.** `rolling_pf < baseline − kσ` and the AUTHORIZED→WATCH-1→WATCH-2 step are `core.lifecycle`'s (`decay_breach`, `autonomous_demote`). Call them; never inline them.
- **Widening `lifecycle_state.json`'s schema.** It is a strict `{strategy: tier}` object (`load_lifecycle_state`, lines 58–73). Put the consecutive-breach counter in a separate harness-owned file (§0.5(D)); do not append fields to the validated interface.
- **Hardcoding baseline PF or `MIN_TRADE_COUNT` as a ratified constant.** PF is parsed from baselines.md (Step 2.1); the min-trade count is a clearly-logged placeholder pending 2026-08-08 pre-registration, not a frozen threshold.
- **Switching `ACTIVE_FIRM` "for convenience"** (would break the MC anchor's byte-reproducibility) or re-running the locked anchor to get σ (the σ computer reads a *supplied* panel).
- **Re-deriving §0 facts.** If a §0 anchor seems inconsistent with disk, return `NEEDS_CONTEXT` with the discrepancy — do not proceed on the inconsistent value.
- **The "while I was in there" refactor** of `lifecycle.py`/`dd_protection.py`/`mc/*`. Log observations under `DONE_WITH_CONCERNS`; touch nothing.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of:

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All §2 steps built; all per-step gates green; no scope creep; no `core/*`/`ops/` touch. | Accept, merge, close. |
| `DONE_WITH_CONCERNS` | Built, but Cursor flags a correctness/scope/methodology doubt. Every gate passed but something reads off-pattern. | Parent reviews concerns; accept or re-dispatch. |
| `NEEDS_CONTEXT` | Cannot proceed without missing input (a §0.5 default contradicted by Phase-0, a referenced file absent, an underspecified parameter). | Parent supplies context; re-dispatch same plan. |
| `BLOCKED — <sub-case>` | Structural obstruction. | Parent escalates/decomposes/re-spawns. |

**`BLOCKED` sub-cases:** `context-problem` / `capability-problem` / `scope-problem` / `plan-itself-wrong`.

A `DONE` here means the harness is built and fixture-proven — it is **never** a claim that any strategy decayed, was demoted, or that the 2026-08-08 Call-1 evaluation is now live-evaluable (it remains AMBIGUOUS until a live-PF source and a ratified min trade count exist).

Closure report format:
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...], 2.4 [...], 2.5 [...], 2.6 [...]
Diffs (files touched): <list — expect only lab/discovery/lifecycle_call1/* and tests/>
§0.5 resolutions applied: A=<...>, B=<...>, C=<...>, D=<...>, E=<...>
WATCH-2 autonomous-floor test (never auto-RETIRE): <pass/fail — load-bearing>
No-double-count check (harness applies tier only, never the multiplier): <pass/fail — load-bearing>
AMBIGUOUS-on-thin-data test: <pass/fail>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance.** Every Step 2.x output present; diff list contains ONLY `lab/discovery/lifecycle_call1/*` and `tests/` files; no `core/`/`ops/`/Pine touch; no pyproject change; no new field on `lifecycle_state.json`'s schema.

**Pass 2 — Quality.** The WATCH-2 floor test genuinely fails if the code let WATCH-2→RETIRED (verify by temporarily relaxing `autonomous_demote`'s consumer and confirming the test would then wrongly pass — the "does this test test anything" check); the no-double-count check genuinely proves the harness writes only a tier string (grep the harness for any `* multiplier` / `TIER_MULTIPLIER[...]` sizing use — there must be none); the strict-`<` boundary test is present; the σ computer's zero-loss-denominator convention is explicit and tested, not an accidental `nan`; no PF/threshold literal outside the Step-2.1 loader.

**Pass 3 — Consolidated read** across all diffs: the 2.1→2.5 chain flows end-to-end — a single breach genuinely does NOT demote; two consecutive genuinely write `lifecycle_state.json` via `autonomous_demote`; an AMBIGUOUS window genuinely leaves both the counter and the state file untouched; the written state file genuinely round-trips through `core.lifecycle.load_lifecycle_state`.

Only after all three passes does the parent recommend Joshua accept/merge.

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# No baseline-PF or threshold literals outside the pre-reg/baseline loader (expect: only the loader + its tests)
grep -rn "3\.750\|3\.373\|3\.717\|4\.188" lab/discovery/lifecycle_call1/ | grep -v test

# The harness NEVER applies the lifecycle multiplier (haircut lives in dd_protection.py) — expect: no sizing use
grep -rn "TIER_MULTIPLIER\|\* multiplier\|\* lifecycle" lab/discovery/lifecycle_call1/

# The breach inequality + ladder step are core.lifecycle's — expect: decay_breach / autonomous_demote CALLED, never inlined
grep -rn "decay_breach\|autonomous_demote" lab/discovery/lifecycle_call1/
grep -rn "rolling_pf <\|baseline_pf -" lab/discovery/lifecycle_call1/   # expect: empty (no reimplemented inequality)

# No core/* or ops/* edits (expect: empty)
git diff --stat <pre-spawn-commit> -- core/ ops/

# lifecycle_state.json schema stays {strategy: tier} — harness never widens it
grep -rn "lifecycle_state.json" lab/discovery/lifecycle_call1/

# §0 anchors
git log -1 --format='%h %ci' -- core/lifecycle.py
git log -1 --format='%h %ci' -- docs/methodology/strategy_lifecycle.md

# Tests + boundaries
python -m pytest tests/ -q
python scripts/check_boundaries.py
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md --type cc_handoff
# Expected: all checks PASS

grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related

- Canonical owner: [`docs/methodology/strategy_lifecycle.md`](../../methodology/strategy_lifecycle.md) (Call 1, lines 30–37; Implementation status line 115 names this exact pending item)
- Adoption ADR (the T4 artifact this delivers, §7): [`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`](../../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md)
- Locked surface (imported read-only): `core/lifecycle.py` (`decay_breach` / `autonomous_demote` / `load_lifecycle_state`)
- Haircut consumer (must NOT be double-counted): `core/dd_protection.py` (`calculate_protection`, line 216)
- Baseline PF source: [`.claude/skills/trade-csv-reconcile/references/baselines.md`](../../../.claude/skills/trade-csv-reconcile/references/baselines.md)
- CC/Cursor surface-allocation governance: [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
- Reference handoff (same build-ahead discipline): [`docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md`](../../ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md)
