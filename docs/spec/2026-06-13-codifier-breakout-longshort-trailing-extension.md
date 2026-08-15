# SPEC — Codifier/sweep pipeline extension: breakout entry + long-short + trailing exit

**Type:** Scoping spec / implementation plan (R&D-pipeline engineering) — input to a build-vs-park decision
**Status:** EXECUTED (pipeline capability) — **WI-1 (Donchian breakout) + WI-2 (long-short) + WI-3 (trailing ATR/chandelier exit) BUILT & TESTED 2026-06-13** (operator decisions: "build the long-short core" → then "continue to WI-3"). **WI-4 (oil-event gate) deferred** (data-dependent). **The USOIL Gate B itself is NOT run** — it remains operator-gated AND gated on the native-parity gauntlet (§4): the new long-short + trailing execution model has not been native-parity-validated, so the Python pre-filter carries no authority yet. See **§8 Landing record**.
**Date:** 2026-06-13
**Author:** Claude Code (Q-USOIL-1 codify session)
**D-S-A domain:** **system** (the object is the `lab/` R&D codification/sweep pipeline artefact — NOT the data corpus, NOT locked `core/` production). INQHIORI §2.
**Parent:** [`docs/ltm/briefs/Q-USOIL-1-regime-capture-counterbalance.md`](../ltm/briefs/Q-USOIL-1-regime-capture-counterbalance.md) §7 step 4 (codification capability boundary). Triggered because `CONCEPT-USOIL-RGC-001` cannot be codified by the current pipeline.
**Scope guard:** Everything here is in `lab/` (R&D). Zero `core/` mutation. The native-parity gate (`parity.py`) remains the sole deploy authority; the Python pre-filter has no gate authority (ADR `2026-06-05-sweep-engine` §2 invariant), so any defect introduced here can only mis-rank a shortlist, never deploy.

---

## §0 — Rule 0 reads (production source, this session, worktree `claude/q-usoil-1-codify` @ `3c8219f`)

All read 2026-06-13. Anchors are `git log -1 --format='%h %ci'`:

| File | Anchor | What it establishes |
|---|---|---|
| `lab/codification/primitives.py` | `6bf0dff` 2026-06-06 | `ENTRY_REGISTRY` = {mean-reversion/reversion/fade→bb, crossover/cross→ema_x, trend/recovery/momentum→ema_recovery}. **No breakout/Donchian/channel keyword or primitive.** All entry primitives are `*_long`. Exit is always `atr_stop_tp` (fixed stop + **fixed** TP). |
| `lab/codification/compose.py` | `0020665` 2026-06-06 | numpy twins + `_PINE_TO_NP`; `compose_signal_fn` raises `ComposeError` if no entry family matches. `SignalArrays` carries only `long_signal`. |
| `lab/validation/sweep/engine.py` | `6bf0dff` 2026-06-06 | `PythonPrefilterEngine._simulate` (lines 193–300): one position, **long-only** (`long_signal[i]`, `stop_price = price - stop_dist[i]`, PnL `(exit-entry)*size`), **fixed** stop+TP set at entry, STOP-FIRST straddle, max-hold time stop, dd_protection C2 sizing. No `short_signal`, no per-bar stop ratchet. |
| `lab/codification/signal_interface.py` | `6bf0dff` 2026-06-06 | `SignalModule.render_entry()` emits `longSignal = <expr>` only; `PrimitiveResult` has a single `expr`. No short slot. |
| `lab/codification/scaffold.pine.tmpl` | `55456b3` 2026-06-06 | Pine scaffold long-only end-to-end: ENTRY sets `longSignal`; `strategy.entry("Long", strategy.long)`; `stop = close - stopDist`; `strategy.exit(stop=, limit=)` (fixed at entry); `position_size > 0` management. |
| `lab/validation/sweep/grid.py` | `55456b3` 2026-06-06 | Honest-N = full cartesian product; `expand_grid` **refuses to truncate** (raises). Existing archetypes already exceed addressable memory if enumerated → pre-filter samples; DSR deflation uses true total-N. Adding params only raises the DSR bar (consistent with brief §5 #5). |
| `lab/validation/sweep/parity.py` | `6bf0dff` 2026-06-06 | Deploy authority: `parity_check` (trade-count EXACT + net/PF within `PARITY_NET_PF_BAND=0.02` on the anchor, vs a **native TradingView** export) + `rank_correlation_falsifier` (Spearman ρ ≥ `PREFILTER_RANK_RHO_FLOOR=0.70`). Both pre-registered/frozen. Native tier is a documented **manual** operator path. |
| `lab/codification/emit.py` | `c106807` 2026-06-06 | `emit_candidate` calls `compose_from_hint` → raises `EmitError` (wrapping the `ValueError`) for an unmatched family; renders into the scaffold; lints; writes to `core/strategies/candidates/`. |

**Empirical confirmation (cheap falsifier, run this session, not asserted):**
```
compose_from_hint(<CONCEPT-USOIL-RGC-001.logic_family_hint>)  -> ValueError (no entry family matches)
compose_signal_fn(<same>)                                     -> ComposeError (same)
entry keywords matched in the hint: []   filter keywords matched: ['volatility','atr']
grep -i 'short|trail|chandelier|donchian|breakout|strategy.short' lab/  -> no pipeline support (only shorttitle/margin_short=0/shortlist/unrelated analysis)
```

---

## §1 — Context

`CONCEPT-USOIL-RGC-001` (`logic_family_hint`: *Donchian/channel breakout · long-short · structure/vol stop ~2.5–3.5×ATR · trailing chandelier/ATR exit · vol-targeted sizing · oil-event gate*) is **gate-1 ADMIT** with **Gate A (feed-clean) PASS**. The next stage, **Codification**, is blocked: the pipeline cannot express the archetype. The Q-USOIL-1 brief §7-step-4 *hoped* a breakout/long-short single-instrument archetype was in `compose_from_hint`'s scope — §0 above shows it is **not**.

This connects to: Q-USOIL-1 (the consuming concept), the **0/4 pipeline base rate** (Stable, not Degenerating — a clean block here is a real finding, not a loss), and the **lean-portfolio / R&D-pipeline doctrine** (`docs/adr/2026-06-04-lean-portfolio-meta-layer.md`, the concept→codify→sweep→validate pipeline).

**Reusability framing (load-bearing for the decision).** The locked four cover only EMA-crossover / EMA-recovery / BB-reversion *long*. Breakout, long-short, and trailing exits are **foundational archetypes most future concepts will need** — this extension is pipeline capability, not USOIL-specific scaffolding. Its value is largely independent of whether USOIL itself resolves PROCEED.

---

## §2 — The capability gap (binary)

| Concept requires | Pipeline has | Verdict |
|---|---|---|
| Breakout / Donchian / channel entry | only ema_crossover, ema_recovery, bb_reversion | ❌ no primitive → composer **raises** |
| Long-short | every primitive `*_long`; `SignalArrays.long_signal`; engine + scaffold long-only | ❌ structural |
| Trailing / chandelier exit | exit hardcoded to fixed ATR stop + **fixed** ATR TP | ❌ collides with forbidden-move #7 |
| Vol-targeted sizing (inverse realized vol) | `calcSize = equity·risk%·mult / stopDist` with **ATR stop** | ✅ **already** inverse-vol (wider ATR stop in high vol → smaller size) |
| Oil-event gate (EIA/API/OPEC) | session/atr/regime filters only | ❌ missing; needs calendar data |

**Reframing to fit the library is FORBIDDEN.** The only library-expressible reduction is EMA-recovery + long-only + fixed-target — i.e. the Guardian transplant (D1 / brief §5 #3) + long-only (#6) + fixed-target (#7), a triple §5 violation. So there is no cheap "codify a degraded version" path; the gaps must be built or the concept parks.

---

## §3 — Scope decomposition + honest effort

Estimates are **relative sizing + concrete sub-tasks**, not false-precision day counts. The two deep items (WI-2, WI-3) are execution-model changes — the largest pipeline change since the engine was built.

### WI-1 — Donchian/breakout entry primitive — **LOW** (~½ day)
- `primitives.py`: `donchian_breakout()` — param `channelLen`; calc `dcHigh = ta.highest(high, channelLen)[1]`, `dcLow = ta.lowest(low, channelLen)[1]`; long expr `close > dcHigh`, short expr `close < dcLow`.
- `compose.py`: `_np_donchian_breakout` twin + `_PINE_TO_NP` entry; `ENTRY_REGISTRY` += `breakout`/`donchian`/`channel`.
- **Coupled to WI-2:** a breakout needs a *short* expr, which `PrimitiveResult`/`SignalArrays` cannot currently carry. WI-1 is trivial *only once WI-2 lands.*

### WI-2 — Long-short architecture — **HIGH** (structural core; the bulk)
End-to-end execution-model change:
- `signal_interface.py`: `PrimitiveResult` + `SignalModule` gain short entry/exit exprs; `render_entry` emits both `longSignal` and `shortSignal`; precedence rule for both-true bars (mutually exclusive for breakout, but the contract must define it).
- `scaffold.pine.tmpl`: short execution block (`strategy.entry("Short", strategy.short)`, `stop = close + stopDist`, `tp = close - exitAtr·tpAtr`, short `strategy.exit`), short position management (`position_size < 0`, `strategy.close("Short")`), short reset + alerts. `canTrade` already gates flat-only.
- `engine.py` `_simulate`: track `side` (±1); short entry `stop_price = price + stop_dist`, short exit `hit_stop = high[i] ≥ stop_price` / `hit_tp = low[i] ≤ tp`, PnL `(entry−exit)·size`; STOP-FIRST preserved. `SignalArrays` += `short_signal` (+ short stop/tp or side-aware).
- `compose.py`: twins return long+short; `SignalArrays` extension.
- Tests: `test_compose_bridge` (twin coverage) + a synthetic **long-short control oracle** in `test_sweep_controls` (recommended given the depth — don't rely on native parity alone for the deepest change).
- **Risk: HIGH** — touches Python engine + Pine scaffold + signal interface + bridge; each side needs independent native parity.

### WI-3 — Trailing/chandelier exit — **HIGH** (path-dependent; highest transcription risk)
- **Breaks an abstraction:** `SignalArrays.stop_dist/tp_price` are per-bar arrays fixed *independent of entry*. A chandelier stop depends on the high-water-mark **since entry** → path-dependent → not a precomputable per-bar array. The exit contract must gain a **mode** (`fixed | chandelier`); the engine ratchets the stop per bar while in-position (`stop_price = max(stop_price, highest_since_entry − mult·atr[i])` long; min-symmetric short).
- `primitives.py`: `chandelier_exit()` (Pine `var` ratchet + `ta.highest/lowest`); `compose_from_hint` exit selection becomes **conditional** on the hint (currently hardcoded `atr_stop_tp`).
- `scaffold.pine.tmpl`: fixed `strategy.exit(stop=, limit=)` → trailing (`trail_price`/`trail_offset` or manual per-bar ratchet + `strategy.close`).
- `engine.py` + `compose.py` twin: implement the identical ratchet — **highest transcription risk**; the parity gate is most load-bearing here and likely needs iteration.
- **Risk: HIGH.**

### WI-4 — Oil-event gate (EIA/API/OPEC) — **MEDIUM, data-dependent → RECOMMEND DEFER**
- Needs an event calendar (dates/times) as a data input; a filter primitive blocking entries in the window. Not required for Gate B edge-existence (belt refinement; brief defers belt filters). Omitting it is **conservative** (no event-timing alpha claimed). Defer to a later increment; flag in the candidate that Gate B ran without it.

### Cross-cutting / governance
- `test_compose_bridge` enforces a numpy twin per primitive — extend per new primitive.
- The sweep-engine ADR (`2026-06-05-sweep-engine`) describes a long-only fixed-exit model; shorts + trailing is an execution-model extension → **warrants an ADR amendment** (governance cost, small).
- Honest-N grows (channelLen × stop × trail × …) → raises the DSR bar; grid machinery handles it (refuses truncation). Fine.

**Total build (my side):** WI-1 (low) + WI-2 (high) + WI-3 (high) + tests + ADR amendment ≈ the largest single pipeline change since the engine was authored. Two independent path-dependent/structural execution changes, each parity-gated.

---

## §4 — The hidden operator cost (load-bearing; this gates Gate B regardless of my build)

After the build, **Gate B for the USOIL candidate cannot be trusted until the operator runs the native parity gauntlet** — because the Python pre-filter has no gate authority and a *new* execution model (shorts + trailing) has never been parity-validated:

1. **`parity_check`** — run the **anchor config natively in TradingView Strategy Tester** on the same `PEPPERSTONE:SPOTCRUDE` feed, export the trade-list CSV: trade-count **EXACT** + net/PF **within 2%**. First-pass failure is *likely* for a fresh execution model → operator iteration.
2. **`rank_correlation_falsifier`** — a representative config sample run natively → Spearman **ρ ≥ 0.70**. This is the **same manual bottleneck currently open on the GBPUSD rank-cert** (the cfg01–11 runbook step). For shorts+trailing it is a fresh cert.

Until both pass, the plateau / DSR / drop-top-k battery carries no authority. **This operator-manual cost is unavoidable and is on top of the build** — it is the real reason the build is not "free infra."

---

## §5 — Forbidden moves (genuinely tempting for *this build*)

- **Codify a degraded library-expressible version** (EMA-recovery + long-only + fixed-target) "just to get a number." That is the Guardian transplant + #6 + #7 — explicitly forbidden by Q-USOIL-1 §5. The block is real; do not route around it.
- **Build long-only-breakout-only as "phase 1" and run a USOIL Gate B on it.** Long-only discards the larger down-regimes (brief #6) and a fixed exit never fires (brief #7) — a long-only/fixed USOIL result is *mis-specified*, and any plateau/DSR on it is misleading. Phasing is fine for *de-risking the engine* (validate shorts before trailing); it is NOT a license to run a faithless USOIL gate on a partial build.
- **Ship the numpy twins without the native parity gauntlet** because "tests pass." The Python tier has no authority by design; green unit tests ≠ parity. The trailing twin especially must be reconciled natively.
- **Tune `PARITY_NET_PF_BAND` or `PREFILTER_RANK_RHO_FLOOR`** to make a fresh execution model pass. Frozen/pre-registered (ADR §5 #3); tuning is methodology p-hacking.
- **Silently truncate the enlarged grid** to keep N small. `expand_grid` refuses truncation for exactly this reason; report the honest total-N (brief #5; forbidden move #1 in the sweep layer).

---

## §6 — Recommendation + build-vs-park criteria (operator decides)

**This is genuinely the operator's call** — a resource-allocation fork I cannot resolve from code/brief. The honest synthesis:

- The extension is **foundational, reusable** pipeline capability with standalone roadmap value (most future concepts need breakout/long-short/trailing; the locked four don't cover it).
- BUT it is the **largest pipeline change since the engine was built** (two deep execution-model changes) **plus an unavoidable operator-manual parity gauntlet**, in service of a concept whose own brief says the **edge bar is RAISED** (random-walk feed, no persistence prior) and the **pipeline base rate is 0/4**.

**Recommendation: decide the extension on its pipeline-roadmap merits, decoupled from USOIL's ≤3-run / 2026-08-08 budget.** Two coherent dispositions:

- **(A) BUILD (phased), as foundational infra** — if the pipeline will keep running concepts (it will; there is a queue). Sequence: **WI-1+WI-2 first** (long-short breakout, fixed exit) to validate the long-short execution model end-to-end with the simplest exit and a synthetic control oracle; **then WI-3** (trailing) as a second increment; USOIL Gate B runs only after WI-3 (a faithful USOIL gate needs the trailing exit — §5 #2). Charge the build to the pipeline roadmap, not the USOIL budget.
- **(C) PARK USOIL `NEEDS_CONTEXT`** until the capability exists — honest INQHIORI terminal-for-now state (analogous to the brief's Gate-A-FAIL → `NEEDS_CONTEXT` branch: "not answerable from the current *pipeline*"). Silver stays **HOLD-at-4** (status quo; Silver is not admitted). Revisit at the **2026-08-08** regime trigger (Silver is first-to-pause there regardless), when the pipeline-roadmap priority of the extension can be weighed against everything else due then.

My lean: **(A) if and only if** Joshua wants long-short/breakout/trailing as standing pipeline capability now; otherwise **(C)**. Either way, **USOIL does not justify rushing the build under its own budget** — the build is infra, the concept is a low-base-rate consumer of it.

**Go/no-go criterion for the build (if A):** authorize WI-1+WI-2; WI-2 is DONE when (i) `test_compose_bridge` covers the breakout twin, (ii) a synthetic long-short control oracle passes in `test_sweep_controls`, (iii) the long-short scaffold lints clean via `emit.py`. Only then authorize WI-3. Only after WI-3 + native parity PASS does a USOIL Gate B carry authority.

---

## §8 — Landing record (WI-1 + WI-2, 2026-06-13)

**Decision (operator, AskUserQuestion):** "Build long-short core, defer trailing+USOIL." WI-1+WI-2 built as reusable pipeline infra; WI-3 (trailing) + the USOIL Gate B deferred.

**Implemented (TDD, RED→GREEN; branch `claude/q-usoil-1-codify`):**
- `lab/codification/np_indicators.py` — added `highest` / `lowest` (Pine `ta.highest`/`ta.lowest` twins, available-bars warmup).
- `lab/codification/primitives.py` — `PrimitiveResult.short_expr`; `donchian_breakout()` (long-short, `[1]`-offset channel, non-repainting); `ENTRY_REGISTRY` += `breakout`/`donchian`/`channel`; `atr_stop_tp()` now returns the short tp expr; `compose_from_hint` wires `short_entry_expr` + `exit_tp_short_expr`.
- `lab/codification/signal_interface.py` — `SignalModule.short_entry_expr` / `exit_tp_short_expr` + `render_short_entry()` (empty → `shortSignal = false`).
- `lab/codification/compose.py` — `_np_donchian_breakout` twin (returns long+short); `_PINE_TO_NP` += donchian; `_np_atr_stop_tp` returns short tp; `compose_signal_fn` handles tuple-returning entry twins and populates `short_signal`/`short_tp_price`.
- `lab/codification/scaffold.pine.tmpl` — `{{SIGNAL_ENTRY_SHORT}}` + `{{SIGNAL_EXIT_TP_SHORT}}` slots; short entry-execution block (stop ABOVE, tp BELOW; LONG-precedence `and not longSignal`); side-agnostic stale time-stop (`position_size != 0` + `strategy.close_all`); short alert.
- `lab/codification/emit.py` — substitutes the two new placeholders (short before long to avoid token-prefix collision).
- `lab/validation/sweep/engine.py` — `SignalArrays.short_signal` / `short_tp_price` (optional, default None = long-only contract byte-for-byte unchanged); `_simulate` tracks `cur_side`, executes shorts (stop above / tp below, side-signed PnL, STOP-FIRST straddle preserved), LONG-precedence on a both-signal bar.

**Implemented (WI-3 trailing ATR / chandelier exit, 2026-06-13 — "continue to WI-3"):**
- `lab/validation/sweep/engine.py` — `SignalArrays.trailing` (optional, default False = fixed contract unchanged); `_simulate` ratchets the stop AFTER the exit check using the bar's close (long `max(stop, close-stop_dist)`, short `min(stop, close+stop_dist)`, active next bar), and IGNORES the fixed tp when trailing. Sizing reuses `stop_dist` (unchanged).
- `lab/codification/primitives.py` — `chandelier_exit()` (trailing ATR exit; `exitAtrLength`+`stopAtr`, NO `tpAtr`); `compose_from_hint` SELECTS trailing when the hint has `trail`/`chandelier` → `exit_tp(_short)_expr="na"`, `module.trailing=True`, tag `exit:chandelier_trailing`.
- `lab/codification/signal_interface.py` — `SignalModule.trailing`.
- `lab/codification/compose.py` — `compose_signal_fn` sets `SignalArrays.trailing` from the same `trail`/`chandelier` keyword detection (the numpy twin reuses `_np_atr_stop_tp` for stop_dist; tp is computed but ignored when trailing).
- `lab/codification/scaffold.pine.tmpl` — `{{USE_TRAILING}}` baked literal + `var float trailStop`; entry blocks init `trailStop` and set `limit = useTrailing ? na : tp`; a per-bar ratchet block (`math.max/min`, re-issuing `strategy.exit`) gated on `useTrailing`; `trailStop := na` on reset.
- `lab/codification/emit.py` — substitutes `{{USE_TRAILING}}`.

**Tests (new, RED-first):**
- `lab/validation/sweep/tests/test_longshort_engine.py` (4: short tp-gain, short stop-loss, long-only-unchanged backward-compat, long-precedence).
- `lab/codification/tests/test_longshort_breakout.py` (9: highest/lowest fixtures, primitive long+short, registry keywords, Pine compose, USOIL-hint-no-longer-raises, numpy bridge short, twin fixture equality, twin-coverage guard, emit-lints-clean).
- `lab/validation/sweep/tests/test_trailing_engine.py` (5: long ratchet-up exit-above-entry, ignores-fixed-tp, short ratchet-down, monotonic-rise force-close, trailing-default-False=fixed).
- `lab/codification/tests/test_trailing_codify.py` (6: trail-hint sets trailing+na-tp, chandelier keyword, fixed-not-trailing, signal_fn trailing flag, USOIL-hint is trailing-long-short-breakout, emit trailing lints clean + has ratchet).

**Verification:** codification + sweep suites green (110 passed / 1 skip after WI-3); full `lab/` pytest green pre-WI-3 (207 passed) and re-confirmed on the affected trees post-WI-3; long-only crossover oracle + both parity-negative adversarial controls still pass (gate retains teeth); emitted long-short trailing Donchian candidate lints clean; `check_boundaries` OK. Zero `core/` mutation. **Adversarial review of WI-1/WI-2 (5 dims): 1 LOW doc-precision finding (ADR over-claim), 0 code bugs — fixed.**

**Deferred / NOT done:**
- **USOIL Gate B / native-parity gauntlet** (§4) — the long-short + trailing execution model has NOT been native-parity-validated (anchor trade-count-exact + net/PF≤2%, rank-ρ≥0.70). The Python pre-filter carries no authority until it is; the USOIL Gate B is also operator-gated.
- **WI-4 oil-event gate** — deferred (data-dependent).
- **ADR amendment** — DONE: append-only change-history row in `docs/adr/2026-06-05-sweep-engine.md` records the long-short + trailing execution-model extension (invariants preserved).

## §8b — WI-5 landing (2026-06-14): independent trailAtr + filter-routing fix

Surfaced executing the Q-USOIL-1 Gate B handoff against the frozen pre-reg: the
WI-1/2/3 composer could not faithfully express `CONCEPT-USOIL-RGC-001`'s Gate B grid.
Two defects, both fixed TDD-first (RED→GREEN; full `lab/` suite **248 passed / 19
skipped / 0 failed**; `check_boundaries` OK; zero tracked `core/` mutation):

- **D-2 — independent trail width.** `chandelier_exit()` reused one `stopAtr` for
  BOTH the initial stop (sizing) and the trail ratchet, so the frozen N=36 grid
  (independent `stopAtr` × `trailAtr`) was unexpressible. Added a `trailAtr`
  SweepParam + a `trail_dist_expr`; `SignalModule.trail_dist_expr`;
  `SignalArrays.trail_dist` (optional, `None` ⇒ ratchet by `stop_dist` = WI-3
  contract byte-unchanged); engine ratchet uses `trail_dist`; numpy twin computes
  `exitAtr×trailAtr`; new scaffold slot `{{SIGNAL_EXIT_TRAIL_DIST}}`. Sizing + the
  initial stop still use `stop_dist`.
- **D-1 — filter keyword false-positive.** Bare `"volatility"`/`"atr"`/`"regime"`
  `FILTER_REGISTRY` keys matched exit/sizing phrases ("volatility-targeted sizing",
  "ATR exit"), force-attaching an entry filter the pre-reg §3 forbids. Keys now
  require explicit entry-filter intent (`"... filter"`/`"... gate"`); the unbuilt
  WI-4 "event gate" maps to nothing. Shared registry ⇒ the numpy bridge inherits
  the fix; bridge-parity tests updated to pin the corrected behavior.

Tests: `lab/codification/tests/test_independent_trail_and_filter.py` (8),
`lab/validation/sweep/tests/test_trailing_independent_dist.py` (3); two prior tests
that pinned the D-1 bug (`test_compose_bridge::test_atr_in_hint...`,
`test_lint_controls::test_multi_filter...`) inverted to the fix. USOIL candidate
now emits `entry:breakout, exit:chandelier_trailing` (no `filter:*`), lint PASS,
params ⊇ {channelLen, stopAtr, trailAtr}. **USOIL Gate B still NOT run** — native
parity (B-0) + operator gate unchanged; the execution model changed (new trail
distance) so the parity cert is fresh.

## §10 — Audit hooks (runnable)

```bash
# The block reproduces (composer raises on the USOIL hint) until WI-1+WI-2 land
cd <repo> && PYTHONUTF8=1 python -c "import sys,yaml; sys.path.insert(0,'lab'); \
from codification.primitives import compose_from_hint; \
h=yaml.safe_load(open('lab/validation/concept_intake/concepts/CONCEPT-USOIL-RGC-001.yaml',encoding='utf-8'))['logic_family_hint']; \
import traceback; 
try: compose_from_hint(h); print('COMPOSES — WI-1/2 landed')
except ValueError as e: print('STILL BLOCKED:', str(e)[:60])"
# Expected (pre-build): STILL BLOCKED: logic_family_hint matches no known entry family ...

# No breakout/short/trail primitive in the pipeline (pre-build)
grep -rni "donchian\|breakout\|short_signal\|chandelier\|trail" lab/codification/primitives.py lab/codification/compose.py
# Expected (pre-build): no match

# Parity gate authority + frozen thresholds unchanged (must hold across the build)
grep -n "PARITY_NET_PF_BAND\|PREFILTER_RANK_RHO_FLOOR" lab/validation/sweep/__init__.py
# Expected: 0.02 and 0.70, unchanged

# Pre-filter has NO deploy authority (ADR §2 invariant — must survive the build)
grep -n "def deploy\|def gate\|def authoritative" lab/validation/sweep/engine.py
# Expected: NO match (the no-authority invariant)

# Zero core/ mutation from any build under this spec
git diff --name-only main -- core/   # Expected: empty
```

---

## Verification

```bash
# §0 anchors (re-confirm the read files unchanged since this spec)
for f in lab/codification/primitives.py lab/codification/compose.py \
  lab/validation/sweep/engine.py lab/codification/signal_interface.py \
  lab/codification/scaffold.pine.tmpl lab/validation/sweep/grid.py \
  lab/validation/sweep/parity.py lab/codification/emit.py; do \
  git log -1 --format='%h %ci' -- "$f"; done
# Expected: 6bf0dff / 0020665 / 55456b3 / c106807 (as listed in §0)

# Discipline check. NOTE: check_brief has no "spec" type; cc_handoff is nearest.
# The type-AGNOSTIC checks apply and must pass: [1] §0 anchored reads, [2] §5
# forbidden moves, [3] §10 runnable hooks. The cc_handoff-ONLY checks ([4] §0.5
# halt, [5] four-state return taxonomy, [6] §7 parent-review) are spawn-prompt
# mechanics and are N/A here — this is a scoping spec, not a CC spawn. They
# convert to live checks IF this spec is later promoted to a build CC-handoff.
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/spec/2026-06-13-codifier-breakout-longshort-trailing-extension.md --type cc_handoff
# Expected: [1][2][3] PASS; [4][5][6] FAIL = N/A-for-spec (see note above).
```

If [1]/[2]/[3] fail this spec is DRAFT, not a recorded scope.
