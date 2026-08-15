# ADR 2026-08-03 — Lifecycle ladder: admit an intermediate WATCH-1H rung at 0.40×

**Status:** `Proposed`
**Decision date:** 2026-08-03
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua + Claude Code (Opus 5)
**Amends (on acceptance, not yet):** [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) (`c99c60d`) — adds one rung to the ladder; changes no existing rung's multiplier, no promotion rule, and no parameter. ⚠ While this ADR is `Proposed` it supersedes nothing, hence `Supersedes: none`. **If it is accepted, §7 must also declare the partial supersession here and add the reciprocal `Superseded-in-part-by` to the target ADR** — the graph checker enforces reciprocity, and landing the rung without it would leave the ladder's canonical definition silently forked.
**Governed by:** [`2026-07-23-c1-rung-selection-ev-objective.md`](2026-07-23-c1-rung-selection-ev-objective.md) (`9ab2e8b`, `Accepted`) — **the ratified rung-selection objective for the already-admitted c1 book.** This ADR operates strictly inside it and does not amend it. See §1 and §3.
**Related:** [`2026-07-17-c1-rail-build-account-registration-go.md`](2026-07-17-c1-rail-build-account-registration-go.md) (the GO that deployed c1 at WATCH-1 0.50×) · [`2026-08-03-c1-cadence-leg-preregistration.md`](../briefs/pre-registration/2026-08-03-c1-cadence-leg-preregistration.md) (sibling artifact from the same measurement) · [`2026-07-13-dd-protection-concept-not-constant.md`](2026-07-13-dd-protection-concept-not-constant.md) (the change-control chain any live rung change inherits)
**Layer:** methodology

---

## §0 — Rule 0 reads (verified 2026-08-03 at `a1123b8`, worktree clean)

| Source | Anchor | Supplies |
|---|---|---|
| [`core/lifecycle.py`](../../core/lifecycle.py) L34–36, L43, L180, L193–202 | `4441c72` 2026-07-11 | `TIER_MULTIPLIER = {AUTHORIZED 1.00, WATCH-1 0.50, WATCH-2 0.25, RETIRED 0.00}`; `_LADDER_ORDER`; the L180 self-check `expected = {…}` that **hard-fails** if any multiplier moves; `autonomous_demote` floor at WATCH-2. |
| [`core/firm_rules.py`](../../core/firm_rules.py) L321–334 + L266–292 | `89a069a` 2026-08-02 | `Tradeify_Select_100K`: `max_dd_pct 3.0` ⇒ $3,000; `profit_target_pct 6.0`; `min_trading_days 3`; `consistency_rule_pct 40.0`. **And the OPEN DEFECT block**: `dd_lock_offset_usd: 100` models a lock the eval does not have (art. 10495897, verbatim: *"Evaluation accounts do not have drawdown locking"*). |
| [`core/mc/simulation.py`](../../core/mc/simulation.py) L68, L86–89, L111, L141–169, L188–196 | `fc14682` 2026-07-30 | `intraday_low` argument + its docstring (*"Every bust figure produced without this argument is therefore a LOWER BOUND"*); floor ratchets on EOD `peak`, breach tests `equity_test`; pass requires `max_day_profit <= consistency_frac * total_profit`. |
| [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) | `ae91ddd` 2026-07-17 | Canonical owner of the ladder; the axis-separation rule (authorization multiplies, never edits parameters). |
| [`ops/instruments/MYM.md`](../../ops/instruments/MYM.md) status block | `96974de` 2026-08-03 | MYM is a **LIVE c1 leg (disarmed)** at WATCH-1 0.50×, `dry_run=true`, no strategy-signal-originated fill yet. Confirms the rung this ADR moves is live-but-unfired. |
| [`lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md`](../../lab/analysis/c1/c1_cadence_coverage_2026-08-03/RESULTS.md) | authored this session, `a1123b8` | The size frontier and its proxy sensitivity. All §2/§3 numbers. |
| [`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](2026-07-23-c1-rung-selection-ev-objective.md) §2, §4, §5 | `9ab2e8b` 2026-07-23 | **The governing objective.** Rung selection for the already-admitted c1 book is **EV-per-dollar-day**, selecting the EV-best rung **among the regime-robust admissible rungs**; regime-robustness (both-halves gate) is a **hard admissibility precondition, not overridden by EV**. §4 trigger 1: any rung change needs a fresh both-halves PASS for that rung. |
| [`lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md) + its operator-signed [pre-reg](../briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md) | RESULTS 2026-07-17; pre-reg signed 2026-07-16 | **The already-run both-halves gate.** `0.50× GATE PASS` on all four partitions (H1 0.14%, boot-95th 0.77%, pass-5th 95.76%); `1.00× GATE FAIL` (H1 4.37%, boot-95th 10.37%). **Computed close-only** — 13 days before `intraday_low` existed — and under `dd_lock_offset_usd: 100`. This is the evidence §4 puts at issue. |
| [`docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md`](../briefs/closures/Q-FUNNEL-1-closure-resolved.md) | `b56c5b3` 2026-07-22 | The EV evidence the objective consumes: on `edge_panel_historical`, **1.00× ≻ 0.50× ≻ 0.25×** on EV/dollar-day at every horizon, both halves. EV is **monotone increasing in rung** — which is why §3's "0.40× scores better" is *not* an admissible argument here. |

**Gitignore pre-flight:** no `.pine` file is read or cited by this ADR; the decision is entirely at
the authorization layer. No citation-chain substitution required.

**Post-authoring merge (recorded, not re-stamped).** All reads above were performed at `a1123b8`. The branch subsequently merged `origin/main` `d4a1cc9` (PR #624, params.toml gate retirement). Every file anchor cited above was re-verified unchanged across that merge; `scripts/validate_params.py` was deleted by #624 and the §10 hooks were repaired accordingly.

---

## §1 — Context

The c1 two-leg book (Striker DJ30 v4.5 → MYM1!, Striker NAS100 v1 → MNQ1!) is deployed at
**WATCH-1 0.50×**. That rung is not arbitrary and it is not merely "the ladder's first haircut": it
is the output of a ratified selection rule. Under [`2026-07-23-c1-rung-selection-ev-objective.md`](2026-07-23-c1-rung-selection-ev-objective.md)
(`9ab2e8b`), rung selection is **EV-per-dollar-day among the regime-robust admissible rungs**. EV is
monotone increasing in rung (Q-FUNNEL-1: 1.00× ≻ 0.50× ≻ 0.25×), so the objective would prefer
1.00×; 1.00× is excluded because it **FAILS** the both-halves regime gate. 0.50× is selected because
it is the highest rung that **PASSES** that gate.

**Everything therefore rests on the 0.50× both-halves PASS — and that PASS was computed on a clock
the venue does not use.** The `class_s_c1_haircut_regime_remc` run (RESULTS 2026-07-17) predates
`core/mc/simulation.py`'s `intraday_low` argument by thirteen days and ran under
`dd_lock_offset_usd: 100`, a mechanism the evaluation phase does not have. Its own engine now
documents that every figure produced without `intraday_low` is a **lower bound, not an estimate**.

A 2026-08-03 measurement on two 250-trade venue-edition exports scores the combined book against the
eval's true geometry — no lock, intraday-enforced breach, integer contracts. Under the honest
overlap proxy the book's worst intraday excursion consumes the entire $3,000 rope at **0.441×**,
below the deployed 0.50×. That does not by itself overturn a frozen, operator-signed gate result —
one path is not a distribution — but it is direct evidence that **the input to the admissibility
precondition is stale in the optimistic direction**.

This is the third instance of one shape. The 2026-07-22 lock-correction withdrawal moved Tradeify's
measured bust 2.65% → 4.74% by removing a modelled mechanism the venue does not apply; the
2026-08-03 gate-stack audit found the same constant still live at HEAD across six tiers with ten
per-run monkeypatches. Each time, a deployed configuration was validated against a geometry more
forgiving than the venue's.

**Decision driver (one sentence):** if the 0.50× both-halves PASS does not survive re-measurement on
the venue's own clock, the ratified objective has **no admissible rung to select** between 0.50× and
0.25× — so the ladder's granularity, not the rung choice, becomes the binding constraint, and that
gap must be closed *before* the re-measurement lands rather than under its pressure.

---

## §2 — Decision

**Decision:** admit one intermediate rung, **`WATCH-1H` = 0.40×**, between `WATCH-1` (0.50×) and
`WATCH-2` (0.25×) in `core/lifecycle.py::TIER_MULTIPLIER`, `_LADDER_ORDER`, the L180 self-check's
`expected` dict, and [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md).

Four properties are **unchanged** and are part of the decision:

1. **No existing multiplier moves.** 1.00 / 0.50 / 0.25 / 0.00 keep their values; the L180 self-check
   keeps hard-failing on any change to them.
2. **`autonomous_demote` still floors at WATCH-2** and still never promotes. `WATCH-1H` is inserted
   into the demotion order, so an autonomous step from WATCH-1 lands on WATCH-1H rather than
   WATCH-2 — a *smaller* automatic haircut, which is the conservative direction for an
   automation-moves-down-only ladder only if paired with property 3.
3. **Demotion depth is preserved on the decay path.** `decay_breach` firing twice from WATCH-1 now
   reaches WATCH-2 as before, one step later. Any caller relying on "one demotion from WATCH-1 = 0.25×"
   must be re-read at implementation, not assumed.
4. **This ADR does not itself move c1 to 0.40×, and does not claim 0.40× is the right rung.** It
   makes the rung *available*. Under the governing objective the rung is **selected by EV among
   regime-robust admissible rungs** — never by this ADR and never by pass-rate ranking. 0.40× becomes
   selectable **only if** 0.50× loses its both-halves admissibility on re-measurement; if 0.50×
   re-passes, EV selects 0.50× and `WATCH-1H` stays an unused rung. Re-tiering the live legs is a
   separate operator action under the `concept-not-constant` change-control chain.

**Effective:** on acceptance + the §7 implementation landing.
**Scope:** the authorization axis for all strategies. No parameter-axis effect whatsoever.
**Explicitly NOT in scope:** the rung-selection objective (`9ab2e8b` §2, untouched), the survivor-scoring
admission gate (`be6dda6`, untouched), and the live c1 rung (stays WATCH-1 0.50× / disarmed).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Demote c1 to WATCH-2 (0.25×)** if 0.50× loses admissibility | This is the *status-quo-compliant* fallback and the alternative this ADR exists to avoid. It is not wrong — it is safe and needs no governance change — but under the ratified objective it is the **EV-worst** admissible rung, and the ladder forces it purely because nothing sits between 0.50× and 0.25×. Choosing a rung by "what the ladder happens to offer" rather than by the objective is the defect. |
| **Hold at WATCH-1 0.50× on the existing PASS** | Legitimate today and it may well be the final answer — the 2026-07-17 gate result is frozen, operator-signed, and one path is not a distribution. This ADR does **not** overturn it. What it declines is to let the PASS stand *unre-measured* once its engine has documented the figure as a lower bound. ⚠ **The earlier draft of this ADR argued 0.50× was "dominated" because 0.40× scored a higher pass rate. That argument is withdrawn: it is inadmissible under the governing objective**, which ranks rungs by EV-per-dollar-day (monotone increasing in rung), not by pass rate. Pass-rate ranking would have quietly replaced a ratified objective. |
| **Change WATCH-1 itself from 0.50× to 0.40×** | Silently redefines a tier that other artifacts cite by name (the 2026-07-17 GO, `MYM.md`/`MNQ.md` status blocks, the Q-COMPOSE-1 closure, the c1 sizing host). Renumbering an existing rung breaks every historical reference; adding one does not. |
| **Per-strategy continuous multiplier instead of a ladder** | Reopens the exact discretion the 2026-07-10 ADR closed — a fixed ladder exists so de-risk is a *pre-registered* step, not a tuned number. A continuous knob invites fitting the multiplier to the panel, which is what §5 forbids. |
| **Status quo — no decision** | If the re-measurement unseats 0.50×, the objective is left with only WATCH-2 to select — a rung chosen by ladder availability rather than by the ratified rule, decided under time pressure with a first armed send pending. Closing the granularity gap *before* the evidence lands is the whole point. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger — the proxy limb.** This ADR rests on `cluster` (overlapping holds sit at max
adverse together) being the honest intraday model. Under `seq` the deployed 0.50× shows 0.0%
failure and the ADR's premise dissolves. **If** a bar-level `intraday_low` series — real 15m bars
through `core/mc/simulation.py`'s `intraday_low` argument, not per-trade MAE — puts the combined
book's max intraday drawdown at **≤ $3,000 at 0.50×** (equivalently critical scale **≥ 0.50×**),
**then** this ADR is revoked as unnecessary and WATCH-1 stands unqualified.

**Revert trigger — the admissibility limb (the load-bearing one).** This ADR's justification is that
0.50×'s both-halves admissibility may not survive re-measurement on the venue's clock. **If** a
re-run of the `class_s_c1_haircut_regime_remc` both-halves gate — same frozen pre-registration, same
partitions, `intraday_low` fed from 15m bars and `dd_lock_offset_usd` set unreachable — returns
**0.50× GATE PASS on all four partitions**, **then** 0.50× remains the EV-selected admissible rung,
this ADR's premise dissolves, and `WATCH-1H` should be withdrawn rather than left as an unused rung
inviting future selection-by-availability.

**Note on the shape of this falsifier.** It is deliberately *not* "0.40× outscores 0.50×". Under the
governing objective a higher rung is preferred whenever it is admissible, so a pass-rate comparison
cannot license a lower rung. Only loss of admissibility can — which is why the re-run, not the
frontier, is the trigger.

**Revert action:** supersede with a fresh ADR recording the bootstrap result; restore
`TIER_MULTIPLIER` and `_LADDER_ORDER` to the 4-rung form; re-tier any leg sitting at WATCH-1H to
WATCH-1. Do **not** edit this ADR's triggers in place.

**Trigger check schedule:** at the both-halves re-run's completion (§7 Phase 4), and in any case **before
the first `dry_run=false` armed send with non-zero sizing** (B7-REFIRE Stage 1). Whichever comes
first. Re-checked at the 2026-11-08 §4 hard date if still open.

---

## §5 — Forbidden moves (under this ADR)

- **Treating the 0.0% failure figures as a bust probability.** They are zero *observed* failures on
  **one** 5.67-year path with ~310 overlapping (heavily autocorrelated) start dates — an effective
  sample near ten evals. Quoting "0% bust at 0.40×" as a rate is the error `RESULTS.md` §C1 exists to
  prevent, and it is exactly the shape of the withdrawn §4 discharge.
- **Tuning the rung to the panel.** 0.40× was selected as the nearest round rung *below* the measured
  critical scale of 0.441×, not by scanning multipliers for the best pass rate. A future amendment
  proposing 0.44× or 0.45× "because it scores better" is fitting the ladder to one realization and is
  forbidden without a fresh pre-registration.
- **Letting a new rung become a promotion path.** The ladder moves **down only** under automation
  (`autonomous_demote`, `c99c60d`). WATCH-1H must never be reachable *upward* from WATCH-2 by any
  automatic rule; re-authorization stays an operator GO.
- **Reading this ADR as authorization to arm.** It changes an available multiplier. `dry_run=false`
  still requires M1 `RESOLVED` **at arm time** (2026-07-31b addendum) plus a separate operator GO,
  and B7-REFIRE Stage 1 remains owed.
- **Reading this ADR as license to touch the pyramid.** The measurement identifies the pyramid as the
  source of both the edge (57.4% MYM / 85.5% MNQ) and the intraday overlap that sets the critical
  scale. Pyramid % is **parameter-axis LOCKED**. The authorization axis is the only lever this ADR
  moves, and a "reshaped" Striker is a new construct requiring its own pre-registration and K.
- **Ranking rungs by pass rate.** The governing objective is EV-per-dollar-day among regime-robust
  admissible rungs (`9ab2e8b` §2). EV is monotone increasing in rung, so "0.40× passes more often"
  can never license a lower rung — only loss of admissibility can. This ADR's own first draft made
  exactly this error; it is recorded in §3 rather than quietly deleted.
- **Treating this ADR as a route to re-open 1.00×.** 1.00× FAILED the both-halves gate (H1 4.37%,
  boot-95th 10.37%). Adding a rung *below* WATCH-1 authorizes nothing above it, and `9ab2e8b` §5
  already forbids the override.
- **Silently amending §4 if the re-run disagrees.** Trap #12 — if the trigger is wrong, supersede.

---

## §6 — Consequences

**Positive:**
- Ensures the ratified EV objective has a rung to *select* if 0.50× loses admissibility, instead of
  collapsing to WATCH-2 by default. The objective keeps choosing; the ladder stops choosing for it.
- Puts the deployed rung **inside** its measured critical scale (0.40× → headroom ×1.20 against the
  $3,000 rope; 0.50× → ×0.89, i.e. 11% over) under the honest proxy, and 0.0% failure under **all
  three** proxies rather than only the flattering one.
- Makes ladder granularity a governance decision with a written falsifier instead of an implicit
  constraint discovered at deployment.

**Negative (real):**
- One more tier in every artifact that enumerates the ladder — `lifecycle.py`, `strategy_lifecycle.md`,
  the L180 self-check, and any test pinning the 4-tuple. Enumeration cost is permanent.
- **Demotion semantics shift by one step.** "One autonomous demotion from WATCH-1" now means 0.40×,
  not 0.25×. Any caller or doc that encodes demotion *depth* rather than *tier name* silently changes
  meaning — §7 Phase 2 exists to find them, and this is the most likely place for a defect to hide.
- A five-rung ladder is marginally more tunable than a four-rung one, i.e. slightly more surface for
  the fitting §5 forbids.

**Risks (probabilistic):**
- The `cluster` proxy may overstate within-day overlap damage; if so the rung is unnecessary
  (§4 limb 1 catches it). Mitigation: the ADR costs nothing operationally if revoked — no leg is
  re-tiered by this ADR itself.
- The measured critical scale is one path's worst excursion. A regime 10% worse than anything in
  2020-2026 puts 0.40× at the line too. Mitigation: the both-halves re-run in §7 Phase 4 is the instrument
  that prices this; until it runs, 0.40× is "inside the worst *observed*", not "safe".

**Downstream artifacts needing update:**
- [`core/lifecycle.py`](../../core/lifecycle.py) — `TIER_MULTIPLIER`, `_LADDER_ORDER`, L180 `expected`.
- [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) — ladder table + demotion-depth prose.
- [`CLAUDE.md`](../../CLAUDE.md) §Strategy Authorization Lifecycle — the `1.00× / 0.50× / 0.25× / 0.00×` enumeration.
- Any test pinning the 4-tuple (§7 Phase 2 sweep finds them).
- [`STATE.md`](../../STATE.md) — forward-board line for the §4 bootstrap trigger.

---

## §7 — Implementation plan

- **Phase 0** — re-verify §0 anchors; confirm `core/lifecycle.py` still at `4441c72` and the L180
  self-check still enumerates exactly four tiers.
- **Phase 1** — land the panels into `core/data/tv_exports/cme/` and regenerate `SHA256SUMS`
  (`python scripts/check_data_manifests.py --regenerate --dry-run` then `--regenerate`, committed in
  the **same** commit). Repairs the `RESULTS.md` §0 provenance defect. **Blocking for lock-grade use.**
- **Phase 2** — `rg -n "WATCH-2|0\.25|TIER_MULTIPLIER|_LADDER_ORDER|autonomous_demote"` across
  `core/ ops/ tests/ docs/`; classify each hit as *tier-name* (safe) or *demotion-depth* (must be
  re-read). Report the depth-dependent set **before** editing.
- **Phase 3** — edit `lifecycle.py` + `strategy_lifecycle.md` + `CLAUDE.md`; extend the L180 self-check
  to five tiers; add a regression asserting `next_tier("WATCH-1") == "WATCH-1H"` and that
  `autonomous_demote` still cannot pass WATCH-2.
- **Phase 4 — the §4 trigger.** Re-run the `class_s_c1_haircut_regime_remc` **both-halves regime
  gate** under its own frozen pre-registration — same partitions, same thresholds — with
  `intraday_low` fed from 15m bars and `dd_lock_offset_usd` set unreachable. Score 0.50× first (the
  admissibility question), then 0.40× only if 0.50× fails. This is the measurement that decides
  whether `WATCH-1H` is ever selectable, and it converts the frontier from one path to a distribution.
  ⚠ Re-running a frozen operator-signed gate on corrected inputs is itself a decision — it needs an
  operator GO before it runs, and its result may not be read as superseding the 07-17 record without
  one.
- **Phase 5** — verification block; status → `Accepted` only if Phase 4 has not fired §4.

**Status stays `Proposed` until Phase 4 reports.** Landing Phases 1–3 without Phase 4 makes the rung
*available* on a single-path justification; that is acceptable for optionality but is **not**
grounds to re-tier c1.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Ladder shape matches this ADR (5 tiers) and the self-check was extended, not bypassed.
rg -n "TIER_MULTIPLIER|_LADDER_ORDER|WATCH-1H" core/lifecycle.py
rg -n "expected = \{" -A3 core/lifecycle.py

# 2. No existing multiplier moved — 1.00 / 0.50 / 0.25 / 0.00 must all still be present verbatim.
rg -n '"AUTHORIZED": 1\.00|"WATCH-1":\s+0\.50|"WATCH-2":\s+0\.25|"RETIRED":\s+0\.00' core/lifecycle.py

# 3. Automation still cannot promote and still floors at WATCH-2.
rg -n "autonomous_demote" -A12 core/lifecycle.py | rg -n "WATCH-2|no autonomous move"

# 4. Demotion-depth callers were re-read (Phase 2 evidence must exist).
rg -n "demotion-depth|depth-dependent" docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md

# 5. §4 trigger status — has the bootstrap run?
ls lab/analysis/class_s_c1_haircut_regime_remc_intraday_2026-08/ 2>/dev/null \n  || echo "Phase 4 NOT run -> ADR stays Proposed"

# 6. Panel provenance repaired (Phase 1).
rg -n "2026-08-03_906e3|2026-08-03_17bc9" core/data/tv_exports/cme/SHA256SUMS 2>/dev/null \
  || echo "VIOLATION: panels still outside the manifest tree"

# 7. No parameter-axis drift smuggled in alongside.
# validate_params.py RETIRED 2026-08-03 (ADR 2026-08-03-params-toml-gate-retirement.md);
# successors are the pine-hash + skills-no-constants + path-liveness gates.
python scripts/check_pine_manifest.py && python scripts/check_skills_no_constants.py \n  && python scripts/check_path_liveness.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md --type adr

git log -1 --format='%h %ci' -- core/lifecycle.py        # expect 4441c72 (pre-implementation)
git log -1 --format='%h %ci' -- core/firm_rules.py       # expect 89a069a
git log -1 --format='%h %ci' -- core/mc/simulation.py    # expect fc14682
git log -1 --format='%h %ci' -- ops/instruments/MYM.md   # expect 96974de

# Frontier reproduces from the pinned panels
cd lab/analysis/c1/c1_cadence_coverage_2026-08-03 && python run_coverage.py --mym <path> --mnq <path> \
  | python -c "import json,sys; d=json.load(sys.stdin); print(d['size_frontier']['0.40x']['bust_pct'], d['size_frontier']['0.50x']['bust_pct'])"
# Expected: 0.0 16.0
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-03 | Initial authoring — `Proposed`, pending §7 Phase 4 | Joshua + Claude Code |
| 2026-08-03 | **Argument rebuilt pre-merge** after the gate-stack audit (R11): cited the governing EV-objective ADR `9ab2e8b`, withdrew the inadmissible pass-rate dominance argument, and re-hinged §4 on the both-halves admissibility re-run. Still `Proposed`; never tracked in the defective form. | Claude Code |
