# Design — CME-native breadth revival + candidate reproducibility index

**Status:** `Proposed` — design conversation, not yet ratified or built. No code touched by this
document; it records and self-reviews a design so it can be reviewed before any implementation work
starts, per the brainstorming skill's own gate.
**Date:** 2026-08-19
**Authors:** Joshua + Claude Code (design collaboration)
**Related:** [Q-COMPOSE-1 closure](../../briefs/closures/Q-COMPOSE-1-closure-falsified.md) ·
[Stage-8 variance-dominance ADR](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) ·
[agentic research team structures note](../../notes/research/2026-08-19-agentic-research-team-structures.md)
(Option E; the seam this design's Stage 2 also serves) · `lab/discovery/register_search.py` /
`lab/research_utils/breadth.py` / `core/mc/modes.py` (all Rule-0 read in full this session)

---

## §1 — Purpose and scope

Two related but independently-shippable problems, both surfaced this session while designing Option E
for the agentic-research-team-structures note:

1. **`breadth.py` is dormant.** It correctly computes both dependence-N_eff (correlation-based) and
   risk-N_eff (covariance-based) portfolio breadth — the exact statistic Q-COMPOSE-1 proved is the
   one that actually predicts composed-book bust, not the flattering-but-misleading correlation view —
   but its baseline-panel loader is hard-wired to `PANELS_BY_BROKER["pepperstone"]`, and Pepperstone/CFD
   data is retired repo-wide. The registry is empty; `breadth.py`'s own `load_baseline_panel` raises
   naming the gap. A previously load-bearing safety mechanism has no working data source, using data
   this repo no longer treats as canonical.
2. **There is no cross-campaign store of candidate return series.** `register_search.py`'s
   `close_run()` persists only submitted p-values, never full return series. Feeding a candidate into
   `breadth.py`'s "5th column" injection today means hand-deriving its daily return series from
   scratch every time.

This design answers: what should be built, in what order, and what should deliberately NOT be built
(a growing raw-data store — this repo has already been burned twice by exactly that pattern: the
2026-08-03 gate-stack audit's "56 adds / 26 revisions / zero genuine prunes" finding, and the
2026-08-13 dedup-first ADR's own retired semantic-gate precedent).

**Out of scope:** anything that gates *entry* into the K-ledger or promotion pipeline (that's Option E,
already built — see the research note). This design is about *portfolio-composition* analysis, a
downstream, optional, non-blocking use of a candidate's data, same tier as `breadth.py` already is.

---

## §2 — Context (Rule-0 grounding, this session)

- **Q-COMPOSE-1** (`FALSIFIED`, 2026-07-17): composing ORB-MNQ-1 into the 2-leg MYM+MNQ book blew
  bust probability from 2.65% to 38.75% (Tradeify tier) — 15× the 3.0% ceiling. The kill mechanism was
  plain variance dominance (ORB's daily $std $438 > the whole 2-leg book's $273), not correlation.
  Dependence-N_eff rose 1.9948→2.9502 (looked like great diversification); risk-N_eff stayed flat at
  1.96 (the true signal). **Any design that computes plain candidate-vs-book correlation would
  silently repeat this exact falsified pattern.**
- **`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`** (`Accepted`) promoted this
  lesson to a binding gate: composition admission requires `n_eff_risk_delta ≥ τ_risk`, with a
  positive dependence-delta explicitly declared insufficient. `breadth.py` already emits both
  statistics correctly — this design must feed that existing, correct mechanism, never build a
  parallel one.
- **`breadth.py`'s dormancy, verified this session:** `load_baseline_panel(panel_name="pepperstone")`
  → `PANELS_BY_BROKER["pepperstone"]` is empty ("substrate Phase 3 retired the Pepperstone executable
  anchor; registry is empty until a panel is admitted via ADR" — the code's own error message). The
  ADR's own header already records this: `Superseded-in-part-by: 2026-08-07-w4-minimal-gate-set-
  dormancy.md — sole-producer status of risk-breadth coordinates while breadth.py is tombstoned
  (doctrine retained; producer dormant)`.
- **The four locked strategies' futures-edition status is NOT uniform** (verified this session against
  `docs/pursuits/b1-aegis-6j-transfer-lane.md`, `docs/pursuits/b8-guardian-mgc-transfer-lane.md`, and
  `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`):

  | Strategy | Futures edition | Standing | Real backtest data present? |
  |---|---|---|---|
  | Striker DJ30 | MYM | `AUTHORIZED · MECHANISM @ 1.00×` — only *deployment* at Tradeify withdrawn, parameters untouched | Yes |
  | Striker NAS100 | MNQ | `AUTHORIZED · MECHANISM @ 1.00×` — same | Yes |
  | Aegis (USDJPY) | 6J | `PARK`, expiring 2026-11-08 absent renewal | Yes (v0.3, measured) |
  | Guardian Gold | MGC | `SUBTRACT`/DEAD — measured non-viable, bust 42.2/72.4/16.5% vs ≤3.0% ceiling | Yes, but the strategy itself failed |

  A "4-leg baseline" naively mirroring the old CFD book would include a leg (Guardian→MGC) already
  proven non-viable in futures form. The only two legs still `AUTHORIZED` are Striker DJ30 (MYM) and
  Striker NAS100 (MNQ) — the exact 2-leg composition Q-COMPOSE-1 itself used as its baseline.
- **The data already exists**, gitignored + hash-manifested exactly per this repo's existing
  convention: `core/data/tv_exports/cme/SHA256SUMS` carries real, dated TV-export CSVs for all four
  strategies' futures editions (verified this session — see §3.1 for exact filenames).
- **`PANELS_BY_BROKER` / `EXPECTED_SYMBOLS_BY_BROKER` / `EXPECTED_VERSIONS_BY_BROKER` in
  `core/mc/modes.py` are clean, currently-empty dict extension points** (verified: `Dict[str, Dict[str,
  Path]] = {}`, retired per ADR 2026-07-22 §2-C). `STRATEGY_FILENAME_TOKEN` is already broker-agnostic
  and populated for all four strategy keys. Adding a `"cme"` entry requires no validation-logic
  changes elsewhere — `load_baseline_panel`/`_load_all` key off the same three dicts generically.
- **This repo's own stated preference is reproducibility over storage**, not incidental to this
  design: `promotion_packet.py`'s claim schema already forbids prose evidence and requires a
  `reexecute_command` per claim — "artifact-only claims... prose carries nothing."

---

## §3 — Decision: two independently-shippable stages

### §3.1 — Stage 1: CME-native baseline panel (small, mechanical)

Add a `"cme"` entry to the three registries in `core/mc/modes.py`, scoped to **only the two
`AUTHORIZED` futures legs** — Striker DJ30 (MYM) and Striker NAS100 (MNQ). Aegis (PARKED) and
Guardian (DEAD) are deliberately excluded from the baseline; either could still be *injected as a
candidate* via `breadth.py`'s existing 5th-column mechanism (exactly like ORB-MNQ-1 was), but neither
belongs in the locked baseline given their current standing.

**Canonical export resolved by reading the pre-transition history in the private `first-passage-archive`
remote** (git history for this manifest is empty in the public repo past the 2026-08-14 transition
commit; the archive remote already exists at `archive` and required no unarchiving to read — GitHub
archived-repo state blocks writes, not reads/fetches):

- **MYM — resolved.** `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-21_73182.csv`. Commit `7d80037`
  ("data: pin latest MYM strategy export", 2026-07-22) is the canonical, explicitly-labeled latest
  strategy export.
- **MNQ — not ambiguous once traced, just narrower than it first looked.** The four same-day
  `Striker_NAS100_MNQ_CME_MINI_MNQ1!_2026-07-17_*.csv` files are **not** general-purpose strategy
  exports at all — commit `05b94e4` ("data: archive the 12 Q-RAIL-1 F3 Step-2/C3 evidence CSVs")
  names them explicitly as Q-RAIL-1's F3 Step-2 per-candle parity + C3 attribution-ladder evidence
  (`STEP2_PARITY.md` / `STEP3_1A/1B/1C.md`), a narrow rail-execution-parity study, not a backtest
  panel. Using any of them as a breadth baseline would be a category error. MNQ never received an
  equivalent "pin latest strategy export" commit the way MYM did — the 07-21 "fresher panels" commit
  (`da075a1`) only landed a raw `BAR_EXPORT_v0.2_CME_MINI_MNQ1!_2026-07-21_dd9d8.csv`, not a re-pinned
  `Striker_NAS100` strategy export. **The only remaining general-purpose MNQ candidate is the older
  `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv`** (predates the `Striker_NAS100_MNQ` naming
  convention) — usable, but ~6 weeks stale relative to MYM's 07-21 pin. Whether that staleness gap
  matters enough to pull a fresh MNQ export before Stage 1 ships (mirroring what was done for MYM) is
  an operator call, not a design default — flagged in §7, not resolved here.

**Mechanism:**
1. Determine the canonical CSV per leg (§7 open item).
2. Populate `PANELS_BY_BROKER["cme"]`, `EXPECTED_SYMBOLS_BY_BROKER["cme"]`,
   `EXPECTED_VERSIONS_BY_BROKER["cme"]` with `{"striker": <path>, "striker_nas100": <path>}` (matching
   `STRATEGY_FILENAME_TOKEN`'s existing keys — Guardian/Aegis keys deliberately omitted from the `cme`
   panel, not merely left unpopulated, so `load_baseline_panel(panel_name="cme")` cannot silently
   include them).
3. Run `python lab/research_utils/breadth.py --self-test --panel cme` to establish a **fresh** anchor.
   This will **not** match the old Q-NEFF-1 Pepperstone anchor (3.98 dependence / 3.09 risk) — that
   anchor was a 4-leg CFD panel; this is a 2-leg CME panel. A new anchor constant needs to be recorded
   once the real numbers are known, not predicted here.
4. **Optional, cheap cross-check:** because this reproduces Q-COMPOSE-1's own 2-leg MYM+MNQ baseline
   on native data, re-running Q-COMPOSE-1's daily-$-std ratio (ρ) and risk-N_eff-delta computation for
   ORB-MNQ-1 against this CME-native baseline would validate whether the CFD-era finding transfers to
   native data. Genuinely optional — not required to ship Stage 1.

**Explicitly not in scope for Stage 1:** wiring this into any live-trading or deployment decision.
`breadth.py` operates purely on historical CSV data for research/composition analysis — this is
research tooling, not a `dry_run`/M1/live-execution-adjacent change, and carries none of that
machinery's safety-invariant weight.

### §3.2 — Stage 2: candidate reproducibility index (not a raw-data store)

**Rejected approaches** (considered, not chosen — recorded so they aren't re-proposed without new
reasoning, per this repo's own dedup-first discipline):

| Approach | Why rejected |
|---|---|
| **A — Manual export script**, opt-in, no automatic wiring | Lowest engineering cost, but relies on a researcher remembering to run it — same "might never get exercised" risk this repo has already named twice (gate-stack audit's "unexecuted self-review" finding). |
| **B — Automatic capture at `close_run()`**, persisting daily return series alongside p-values | Guarantees the store actually populates, but (1) `RuleEval.bar_returns` today is a plain, unindexed numpy array — no date index exists to persist without new plumbing; (2) grows an unbounded, gitignored numeric data store with no pruning story, repeating the exact pattern the gate-stack audit flagged as this repo's real risk ("56 adds / 26 revisions / zero genuine prunes"). |
| **C — Reproducibility index (chosen)** | Store a *pointer*, not the data. Regenerate on demand. |

**Chosen: Approach C.** Extend `register_search.py`'s `close_run()` candidate records with a pointer
to that candidate's frozen-rule provenance file — the same `FrozenRule.as_provenance()` +
shape-array JSON shape already produced per campaign today (see `tests/test_stage4_7_drivers.py`'s
`test_load_frozen_rules_roundtrip` for the existing round-trip). This is a small, additive manifest
field, the same shape as the `cost_law_preflight`/`admission`/`prereg` pointer fields already added
to `register_search.py` this session (Option E) — no new persistence mechanism invented, the same
pattern reused a fourth time.

A new helper function, `regenerate_return_series(run_id, candidate_id) -> pandas.Series`:
1. Loads the K-ledger manifest for `run_id` (existing `register_search._load()`).
2. Resolves the frozen-rule pointer for `candidate_id`, loads the `FrozenRule`.
3. Reloads the canonical CME series data for the manifest's recorded `data_window` (already a
   top-level manifest field from `open_run`).
4. Re-runs `discovery.motif_rules.evaluate_rule(rule, series, ...)` — the exact same deterministic
   function that produced the original scoring result.
5. Attaches the reloaded data's own date index to the resulting `bar_returns` array — **this is where
   the date-indexing gap gets closed**, using the same index the canonical CME data already carries,
   rather than inventing a new date-tracking mechanism inside `motif_rules.py` itself.
6. Returns a date-indexed `pandas.Series`, directly injectable into
   `breadth.compute_breadth(panel, candidate=series)` with no further transformation.

**Why this is "reproducibility over storage," not a semantic dedup gate:** this does not infer
anything about a candidate's status from a label or text match (the pattern that already failed once
and was retired — 2026-08-13 ADR). It deterministically re-executes a pure function
(`evaluate_rule`) against data both the pointer and the canonical feed already make available. Nothing
is stored that could go stale relative to its own source; nothing grows unboundedly; nothing needs
pruning.

---

## §4 — Architecture / data flow

```
Stage 1 (one-time wiring):
  core/data/tv_exports/cme/*.csv (already exists, already manifested)
        │
        ▼
  core/mc/modes.py: PANELS_BY_BROKER["cme"] = {striker: <MYM path>, striker_nas100: <MNQ path>}
        │
        ▼
  breadth.load_baseline_panel(panel_name="cme")  →  2-leg CME-native baseline panel
        │
        ▼
  breadth.compute_breadth(panel)  →  fresh n_eff_dependence / n_eff_risk anchor

Stage 2 (per-candidate, on demand):
  register_search.py close_run()
        │  (new: candidate record gains a `rule_provenance_path` pointer)
        ▼
  discovery_manifests/<run_id>.json  (candidates: [{id, pvalue, rule_provenance_path}, ...])
        │
        ▼
  regenerate_return_series(run_id, candidate_id)
        │  loads FrozenRule from rule_provenance_path
        │  reloads canonical CME series for manifest's data_window
        │  re-runs evaluate_rule (deterministic, already-tested)
        │  attaches date index from the reloaded series
        ▼
  date-indexed pandas.Series
        │
        ▼
  breadth.compute_breadth(panel, candidate=series)  →  n_eff_risk_delta, ρ (via compose harness),
                                                        candidate_vs_leg_corr (context only, never
                                                        the admission signal per ADR 2026-07-20)
```

---

## §5 — Components and interfaces (sketch, not final signatures)

- `core/mc/modes.py`: three new dict entries under key `"cme"`. No new functions.
- `lab/research_utils/breadth.py`: **no changes required** — `load_baseline_panel(panel_name="cme")`
  and `compute_breadth(...)` already work generically once the registry is populated. This is the
  clean-extension-point property confirmed this session.
- `lab/discovery/register_search.py`: `close_run()` gains an optional per-candidate
  `rule_provenance_path` field in the `candidates` list (mirrors the existing `--pvalues-file` CSV
  shape — likely a third optional column, or a companion `--rule-provenance-file` mapping candidate id
  → path). Opt-in, additive — omitting it changes nothing for existing callers, same posture as every
  Option E field this session.
- **New module** `lab/discovery/return_series_index.py` (name TBD): houses
  `regenerate_return_series(run_id, candidate_id, *, ledger_dir=None) -> pd.Series`. Pure function
  given its inputs; no I/O beyond reading the manifest, the rule-provenance file, and the canonical
  CME CSV (already-established read paths, nothing new).

---

## §6 — Error handling

- Missing `rule_provenance_path` for a candidate → `regenerate_return_series` raises naming the gap
  (candidates registered before this field existed have no pointer; this is an honest "not
  reproducible from the ledger alone" state, not silently guessed).
- Underlying CME CSV changed/reprocessed since the original run (a new dated export superseding the
  one the manifest's `data_window` was computed against) → the manifest's `data_window` plus the CSV's
  own hash (already in `SHA256SUMS`) gives enough to detect drift; `regenerate_return_series` should
  compare the loaded CSV's hash against what was live at `opened_at` if that's recoverable, else
  surface a WARN (mirrors `breadth.py`'s own `thin_overlap` WARN pattern — report, don't silently
  trust).
- `FrozenRule` fails to load (corrupted/tampered provenance file) → existing `FrozenRuleLoadError`
  (already tested — `test_load_frozen_rules_tamper_fails`) propagates unchanged; no new error class
  needed.

---

## §7 — Open questions (must resolve before implementation, not guessed here)

1. **Resolved for MYM, open for MNQ (see §2's updated canonical-export finding).** MYM: use
   `2026-07-21_73182.csv`, explicitly pinned as latest. MNQ: the only general-purpose (non-parity)
   candidate is the ~6-week-stale `2026-07-11_beabf.csv` — whether to ship Stage 1 on that stale
   export or pull a fresh one first is the remaining operator call.
2. **Resolved — an ADR is required, not a judgment call.** `core/mc/modes.py`'s own header comment on
   `PANELS_BY_BROKER` states explicitly: "New panels require an admitting ADR + explicit registration
   here." This session's earlier "leaning toward no ADR needed" was wrong — corrected on direct Rule-0
   read of the file, not a preference. See
   [`docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`](../../adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md)
   (`Proposed`, awaiting operator ratification).
3. **Whether Aegis (PARKED, expiring 2026-11-08) should be test-injected as a candidate now**, given
   its expiry clock, or left untouched pending its own separate renewal decision — an operator call,
   not a design-doc default.
4. **Whether Head-of-Engineering ownership (per the research note's addendum, itself unratified)
   applies to this specific tooling** — this arguably sits closer to a5 (R&D tooling lane, already
   Head-of-Engineering-owned) than a3/a4 content, but that's a separate, later decision, not resolved
   by this design.
5. **The exact `rule_provenance_path` wire format** (new CLI flag shape, whether it's per-candidate or
   a single companion file) is sketched in §5, not finalized — a natural first task for
   `writing-plans` if this design is approved.

---

## §8 — Testing plan (sketch)

- Stage 1: reproduce the existing `breadth.py` self-test pattern against `--panel cme` once the
  registry is populated; assert panel shape (`n_bdays`/`n_blocks`) is internally consistent (no fixed
  anchor to check against yet — this run *establishes* the anchor).
- Stage 2: paired positive/negative per this repo's house style —
  - Positive: a candidate with a valid `rule_provenance_path` regenerates a return series whose
    `evaluate_rule` output byte-matches (or numerically matches within float tolerance) the original
    scoring run's `bar_returns`.
  - Negative: a candidate missing the pointer raises with a clear, actionable message; a tampered
    provenance file raises `FrozenRuleLoadError` (already covered by the existing test, just needs a
    new caller-path test).
  - Injection: `regenerate_return_series(...)` output fed directly into
    `breadth.compute_breadth(panel, candidate=series)` produces a result with the expected keys
    (`n_eff_risk_delta`, `candidate_vs_leg_corr`, etc.) — an integration smoke test, not a new
    correlation-methodology test (that methodology is `breadth.py`'s own, already anchored).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Initial authoring — design conversation write-up, Rule-0 grounded against `breadth.py`, the Stage-8 ADR, the Q-COMPOSE-1 closure, and this session's transfer-lane/data-manifest survey. Status `Proposed` — not yet reviewed or approved for implementation. | Claude Code (drafted at operator request, "write up the design spec from the previous turn") |
| 2026-08-19 | §2/§7 open item 1 resolved by reading the pre-transition history in the private `first-passage-archive` remote (operator confirmed readable without unarchiving). MYM's canonical export is now a resolved fact (`2026-07-21_73182.csv`, explicitly commit-pinned); MNQ's four same-day 07-17 candidates were traced to Q-RAIL-1 parity-evidence CSVs, not general-purpose exports, narrowing the real open item to a staleness tradeoff on the remaining `2026-07-11_beabf.csv` candidate. | Claude Code (investigated at operator's "you can verify in the first-passage-archive repo" direction) |
| 2026-08-19 | Operator pulled a fresh MNQ export (`2026-08-19_3ad92.csv`), closing item 1's staleness tradeoff outright — both legs now have a fresh, non-parity, general-purpose export. Manifest regenerated by hand-inserting the new line (not `--regenerate` in write mode, which would have silently dropped the 28 pre-existing entries not physically present in this session's worktree — same class of defect as the known CATALOG.md worktree-clobber pattern); the 28 pre-existing CSVs were copied in from the operator's main checkout (same repo, same bytes, different local worktree) to keep `check_data_manifests.py --check` meaningful rather than false-failing on partial presence. §7 item 2 corrected from "leaning toward no ADR needed" to **resolved: an ADR is required** — found on direct Rule-0 read of `core/mc/modes.py`'s own header comment mid-implementation, not a preference call. See [`docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`](../../adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md) (`Proposed`). | Claude Code (mid-Stage-1 build, course-corrected) |
| 2026-08-19 | **Both stages executed.** Stage 1: ADR ratified and built — `core/mc/modes.py` registered, `breadth.py` gained a CME-appropriate identity check (§3.1's "breadth.py needs no code change" claim was falsified at implementation time by the strict OANDA-shaped `assert_tv_export` parser not fitting any real CME filename; fixed, recorded in the ADR's own Ratification note, not silently patched) plus a panel-aware self-test; MYM's registered export corrected from the "latest pinned" file (343-day span, too short) to the actual long-history one (`2026-07-11_15d8b.csv`, 2359 days) after direct measurement. First real anchor: `n_eff_dependence=1.9988, n_eff_risk=1.0871` on a 2-leg panel — 19 pre-existing `breadth.py` tests still pass. Stage 2: dispatched to Cursor (`docs/briefs/handoffs/2026-08-19-cursor-handoff-candidate-return-series-index.md`), returned `DONE_WITH_CONCERNS` — §4's falsifiable premise held (regenerated series matches `evaluate_rule`'s own output at `atol=1e-15`), one self-disclosed footprint violation (an out-of-scope `docs/SESSIONS.md` touch, reverted rather than merged) found and corrected on review, 121 tests independently re-verified green. Both pending final commit/merge on operator go. | Claude Code (Stage 1 build + Stage 2 review, same session) |
