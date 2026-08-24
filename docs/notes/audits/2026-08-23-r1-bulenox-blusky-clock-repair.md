# Audit Note — R1: intraday-honest (CLOCK) re-run extended to all 7 Bulenox/BluSky trailing tiers

**Audit ID:** AUDIT-2026-08-23-r1-bulenox-blusky-clock-repair
**Date:** 2026-08-23
**Triggered by:** Task R1 of the [§4 firm-model parallel repair
plan](../../superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md), the named
(not opened) CLOCK-repair successor to
[`Q-FIRMEOD-1`](../../briefs/closures/Q-FIRMEOD-1-closure-falsified.md), operator-GO'd this session
(sibling Task R2 already landed this session at commit `65dc17b` before this task started).
**Scope:** the 7 `dd_type="trailing"` tiers in `core/firm_rules.py` (Bulenox_25K/50K/100K/150K/250K,
BluSky_Premium_50K/100K) + the `simulate_path`/`firm_kwargs`/`prop_survivor_scoring` engine path
they run through + every citing surface for the two published bust/pass figures this task re-runs.
**Lives in:** `docs/notes/audits/2026-08-23-r1-bulenox-blusky-clock-repair.md`

---

## §0 — Source anchors (Rule 0 — read before authoring anything touching these)

- `core/firm_rules.py` — `grep -n '"dd_type": "trailing"'` re-run this session: lines **122, 134,
  146, 158, 170, 538, 554** (7 hits). Q-FIRMEOD-1's own pin (92,104,116,128,140,508,524) has
  shifted by a constant +30 since — same 7 tiers, same order, confirmed not a changed tier set.
- `core/mc/simulation.py` — `simulate_path`, full function read. The `intraday_low` barrier
  construction (`equity_test = min(equity_new, equity + intraday_low[day]*scale)`, L131-134) and
  the `dd_type == "trailing"` branch (L141-151).
- `core/mc/preflight.py` — `firm_kwargs`, full function read. Confirms `dd_type="trailing"` never
  threads `dd_lock_offset_usd` (L169-171) — that kwarg is `trailing_locking`-only (L172-180), so
  Bulenox/BluSky need no lock-unreachable patch in this task.
- `lab/discovery/prop_survivor_scoring.py` — full file read. `run_tier_remc` / `firm_kwargs` /
  `assert_intraday_channel_nonvacuous` / `load_scoring_thresholds` / `paired_blocks_from_daily`
  confirmed tier-agnostic (no Tradeify/MFFU special-casing anywhere in the module).
- `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/run_w1_intraday_both_halves.py` +
  `RESULTS_INTRADAY_W1.md` — full files read, the template this task extends.
- `tests/core/test_mc_intraday_barrier.py` — full file read; `9 passed` reproduced.
- `docs/briefs/closures/Q-FIRMEOD-1-closure-falsified.md` — full file read (the entry packet).
- `docs/notes/audits/2026-08-23-bulenox-lock-scope-resolution.md` — R2's own audit note, full file
  read (confirms the Bulenox Master-lock does not reach the modeled horizon — no interaction with
  this task's CLOCK repair).
- `docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md` — the method-owner ADR, `Accepted`.
- Published-figure sources read in full: `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`,
  `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md`,
  `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md` +
  `run_corrected_haircut_fullpanel.py`, `lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md`,
  `lab/archive/q_compose_1_2026-07/RESULTS.md`, `lab/analysis/c1/band_quantization_2026-08-02/RESULTS.md`,
  `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md`,
  `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md`.
- Citing-surface candidates read in full or in relevant part: `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`,
  `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`,
  `docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md`,
  `docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md`, `docs/rejected_candidates.md`,
  `docs/briefs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md`,
  `docs/briefs/Q-GATECART-1-survivor-gate-cartography.md`, `STATE.md` (read-only, no hits, no edit).

---

## §1 — Trigger

`Q-FIRMEOD-1` (closed `FALSIFIED` 2026-08-23) proved the intraday-honest (CLOCK) fix W1 landed for
Tradeify/MFFU also flips Bulenox_100K's own `bust_trailing` count from 0 to 1 under its own real
`firm_kwargs()`, and explicitly declined to assume BluSky was clean by analogy. Its re-proposal bar
named the exact repair this task performs: "re-runs the intraday-honest fix (`intraday_low`) across
all 7 tiers per the W1 ADR pattern and reports whether any published figure flips."

**Failure class:** Source-of-truth fracture — the CLAUDE.md EOD-clock caveat was scoped to
Tradeify/Class-S only, while the underlying engine defect it names is generic to every
`dd_type="trailing"` branch. Not a methodology-discipline miss in how the caveat was authored; a
scoping gap the caveat's own author (W1) could not have closed without measuring firms outside
that campaign's scope.

---

## §2 — What actually happened

1. Reproduced the CLOCK sanity check two ways: `pytest tests/core/test_mc_intraday_barrier.py -q`
   (9 passed) and an independent direct diff against `firm_kwargs('Bulenox_100K')` (not the test's
   hand-built fixture) — reproduced the closure's exact `horizon_cap`→`bust_trailing` flip.
2. Extended the direct-diff check to all 7 tiers, including both BluSky tiers, per the task's
   explicit instruction not to assume BluSky is clean by analogy — all 7 flip.
3. Found the 7 tiers' `firm_rules.py` line numbers have shifted (+30) since Q-FIRMEOD-1's own pin
   — re-confirmed via fresh grep before citing, per the task brief's own caution.
4. Found `run_w1_intraday_both_halves.py`'s own `sys.path` setup is broken today (points at a
   directory the Great Prune emptied of `run_class_s_c1_scoring.py`) — confirmed empirically,
   worked around in a new sibling script rather than editing the frozen packet.
5. Searched the repo for every published bust/pass MC figure on the 7 tiers. Found exactly two,
   both on the same MYM+MNQ "Class-S candidate #1" book: Bulenox_100K / BluSky_Premium_100K at
   1.00× (`class_s_candidate1_scoring_2026-07-15/RESULTS.md`) and at 0.50× WATCH-1
   (`CORRECTED_FULLPANEL.md`). The other 5 tiers carry zero published bust/pass MC figures anywhere
   in the tree (confirmed by repo-wide grep + a check that the one pre-registration naming them,
   `2026-08-02-sub100k-realizable-book-scoring-prereg.md`, was signed/frozen but never executed).
6. Restored the gitignored vendor CSVs the re-run needs (MYM/MNQ 15m bars, the two Striker trade
   panels) into this worktree from the main checkout — sha256-verified against the tracked
   manifests both before and after copy; this worktree did not carry them (a worktree-vs-gitignored-data
   gap, not a data-integrity problem).
7. Wrote a new runner (`lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py`)
   that imports W1's `build_book_intraday_low` / `_run_partition` as a library (not re-derived) and
   points the broken import at the module's current live location. Smoke-tested at `n_sims=50`
   before running the full 10,000×3-seed campaign.
8. Ran the full campaign (non-vacuity guard per tier + both published arms) in the background;
   results below.
9. Ran a monotonicity argument (grounded in `simulate_path`'s own `min()` construction) for the two
   already-FALSIFIED candidates whose Bulenox/BluSky figures are 4–49pp over the ceiling on the EOD
   clock, rather than spending K to reconfirm an engine-forced direction.

---

## §3 — Discipline checks

| Check | Should have caught | Actual behavior |
|---|---|---|
| Rule 0 (production read before acting) | Would have surfaced the broken `run_w1_intraday_both_halves.py` import before wasting a run | Caught — verified the import fails empirically before designing around it |
| "Confirm line numbers still hold" (task's own caution) | Catches stale citations of `firm_rules.py` line numbers | Caught — the +30 shift was real; re-confirmed via fresh grep |
| "Do not assume BluSky clean by analogy" (task's own instruction) | Would catch a lazy inheritance of Bulenox's CLOCK finding | Honored — both BluSky tiers independently diffed via `simulate_path`, and both target-tier non-vacuity guards run separately (not inherited from Tradeify's W1 proof) |
| Worktree-vs-gitignored-data gap | Not a standing check in this repo yet | New finding this session (see §6) — no existing check would have caught this before a `NeedsContext` exception at run time |

---

## §4 — Root cause analysis (for the scoping gap itself)

- **Immediate cause:** W1's own scope (per its ADR §2) was explicitly Tradeify/MFFU's four named
  decisions of record — it never claimed to cover Bulenox/BluSky, and its `RESULTS_INTRADAY_W1.md`
  never asserted it did.
- **Contributing factor:** the CLAUDE.md caveat line generalized the *conclusion* ("eval bust
  figures remain EOD-clock lower bounds") to a scope wider than what had actually been measured
  ("unless they cite an intraday-honest RESULTS path" — but no such path existed for Bulenox/BluSky
  until this task), without a matching pointer for the un-measured firms.
- **Structural cause:** no repo convention forces a "which tiers does this caveat's own citation
  actually cover" check when a caveat is authored — the gap was invisible until Q-FIRMEOD-1
  specifically went looking for it via the assumption-sweep. No new standing rule is proposed here
  (this is the second data point on the same class of gap Q-FIRMEOD-1's own §5 already flagged as
  below the two-incident bar for a new lesson — see §6).

---

## §5 — Repair plan

### Immediate

- [x] Re-run the intraday-honest fix on the two tiers carrying a published figure
  (Bulenox_100K, BluSky_Premium_100K) at both published arms (1.00×, 0.50×).
- [x] Record "none to re-measure" for the 5 tiers with no published figure, rather than
  manufacturing one.
- [x] Run BluSky through the same direct `simulate_path` diff Bulenox got (not assumed clean).
- [x] Publish `lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md` + `lab/CATALOG.md` row.
- [x] Extend the CLAUDE.md caveat's scope from Tradeify/Class-S to Bulenox/BluSky, same commit.
- [x] Reader-intercept the citing surfaces for figures that moved (see §6 of the RESULTS doc and
  the disposition table below).

### Structural

- None owed by this task specifically. The worktree-vs-gitignored-vendor-data gap (§2 item 6) is a
  candidate observation, not yet a lesson — this is a first occurrence in the record I could find;
  below the two-incident bar for graduating a new standing rule.

---

## §6 — Reader-intercept disposition (surfaces citing the re-run figures)

**Final numbers:** no verdict flips anywhere. 1.00× (already-FAIL both clocks): Bulenox
3.51%→26.77%, BluSky 4.44%→32.26%. 0.50× WATCH-1 (PASS both clocks): Bulenox 0.08%→0.59%, BluSky
0.08%→0.59% (2.41pp of headroom under the 3.0% ceiling on both).

Per the task's own criterion ("do this for any flips you find, or explicitly state 'no flips
found, no reader-intercepts needed' if none") — **no verdict flip occurred, so strictly no
reader-intercept is required.**

**Judgment call, disclosed rather than silently applied:** this repo's own precedent
(`venuegeo_dp3_bustceiling_2026-08-05/RESULTS.md`'s banner) adds a reader-intercept even where no
verdict flipped, on the reasoning that a reader citing a *stale, since-superseded-in-magnitude*
number is still being misled even if the PASS/FAIL side didn't move. The 1.00× arm's ~7.6×
magnitude change is the same class of "materially different, not just re-confirmed" finding that
motivated that precedent. Applying the same standard here, this task added a light,
non-"SUPERSEDED" pointer banner (frozen body left unedited, Trap #12 discipline) to the **three
primary/highest-traffic sources** for the two re-run figures:

| Surface | Citation | Banner added? | Reasoning |
|---|---|:---:|---|
| `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md` §4 | Bulenox/BluSky 1.00× "control, unchanged" table | **Yes** | Primary source of the "control, unchanged" framing; highest downstream citation count |
| `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md` | Bulenox/BluSky 1.00× Run-2 headline table | **Yes** | Original source of the 3.51%/4.44% figures; already carries one banner (LOCK-defect, Tradeify/MFFU-scoped) — this adds a second, CLOCK-scoped pointer, not a rewrite of the first |
| `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md` | Bulenox/BluSky 0.50× WATCH-1 table | **Yes** | The *only* place the 0.08%/0.08% 0.50× figures are published |
| `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` §4 table | Bulenox/BluSky 1.00× as "control, unchanged" | No | Secondary/parenthetical citation; the ADR's own argument (Tradeify/MFFU flip, Bulenox/BluSky don't change the LOCK verdict) is unaffected by the CLOCK magnitude — the argument concerns the LOCK question, not a live bust-rate claim |
| `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` | Bulenox/BluSky 1.00× as baseline context | No | Closed; own conclusion (44.75%/51.91%, catastrophically FAIL) is unaffected by whether the baseline was 3.51% or 26.77% |
| `docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-2-prereg.md` | Bulenox/BluSky 1.00× as prior-art context | No | Closed/FALSIFIED candidate's own pre-reg; citation is historical framing, not a live claim |
| `docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md` | Bulenox/BluSky 1.00× as "state of record" | No | Closed (`AMBIGUOUS-PARAMETERIZATION`, 2026-07-25); its own conclusion (no envelope claim) does not depend on the exact Bulenox/BluSky magnitude |

This split is a judgment call, not a mechanical rule — flagged explicitly so the operator can
overrule it. The four "No" rows share one property the three "Yes" rows do not: each cites
Bulenox/BluSky's number only to support an argument whose conclusion is unchanged by the more
precise figure (LOCK-question control-group framing; "already failed" background). The three "Yes"
rows are the ones a reader would most plausibly copy the 3.51%/4.44%/0.08% figures FROM into a new
context.

---

## §7 — Programme-audit signal check

- [ ] Belt-patches without independent corroboration? — No; both target tiers independently
  non-vacuity-guarded, both BluSky tiers independently `simulate_path`-diffed, panel/bar data
  sha256-verified before use.
- [ ] Belt that only grows, never prunes? — N/A.
- [ ] Falsifier thresholds drifting? — No; `load_scoring_thresholds()` reused unedited.
- [ ] Methodology invoked to rationalize a decision already made? — No; the honest-clock numbers
  were not known before the run, and the monotonicity argument for the FALSIFIED candidates is a
  code-grounded proof, not a post-hoc rationalization to skip work.
- [ ] SNAG pattern? — No.
- [ ] Cross-layer contamination? — No.
- [ ] Negative heuristic crossed without repair? — No.

No escalation to programme-audit needed.

---

## §10 — Audit hooks

```bash
# 7 trailing tiers still resolve at the cited lines (re-run before citing — they have shifted once already)
grep -n '"dd_type": "trailing"' core/firm_rules.py

# CLOCK evidence reproduces
python -m pytest tests/core/test_mc_intraday_barrier.py -q

# R1 honest-clock report exists and matches the RESULTS doc's table
python -c "import json; d=json.load(open('lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/r1_bulenox_blusky_intraday_report.json')); print(d['arms']['1.00x']['tiers']['Bulenox_100K']['headline_bust'], d['arms']['0.50x']['tiers']['Bulenox_100K']['headline_bust'])"

# CLAUDE.md caveat now scopes to Bulenox/BluSky
grep -n "Bulenox/BluSky" CLAUDE.md

# Confirm the frozen W1 script's import defect (re-check if geofit dir is ever pruned)
python -c "import sys; sys.path.insert(0,'lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16'); sys.path.insert(0,'core'); sys.path.insert(0,'lab'); import run_w1_intraday_both_halves" 2>&1 | tail -1
```

---

## §11 — Closure

- **Status:** `Closed (immediate complete; structural N/A)` — 2026-08-23
- **Immediate repair completed:** 2026-08-23
- **Structural repair completed:** N/A (none owed — see §5)
- **Lessons graduated to standing rule:** none (worktree-data-gap observation below the
  two-incident bar; sourcing-comment-completeness pattern already tracked by Q-FIRMEOD-1's own §5,
  not re-raised here)
- **Follow-up audits triggered:** none. Task R2 already landed separately. Task R3 (survivor §4
  scoring) remains a separate, un-blocked-by-this-note task in the parent plan, gated on a Phase-C
  survivor existing.

---

## Verification

```bash
python -m pytest tests/core/test_mc_intraday_barrier.py -q
python lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py
grep -n '"dd_type": "trailing"' core/firm_rules.py
grep -n "Bulenox/BluSky" CLAUDE.md
```

---

## §12 — Fix-pass addendum (2026-08-23, independent re-verification)

**Trigger:** dispatched as a Task R1 "fix" pass with an **empty** reviewer-findings list (no
Critical/Important items supplied). Rather than guess at unstated findings, this pass re-ran Rule
0 independently against every substantive claim in §§0–9 above and in
[`RESULTS.md`](../../../lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md), acting
as its own adversarial reviewer before deciding what, if anything, needed fixing.

**Re-verified independently (all held, no discrepancy found):**

- The 7 `"dd_type": "trailing"` line pins (122, 134, 146, 158, 170, 538, 554) — re-grepped and
  read `core/firm_rules.py` directly at those lines; both BluSky tiers confirmed `dd_type="trailing"`.
- `core/mc/simulation.py::simulate_path` — read in full. Confirmed the `equity_test = min(equity_new,
  equity + intraday_low[day]*scale)` construction and that forward state (`equity`, `peak`) is
  carried on `equity_new`, never `equity_test` — which is what makes the §4 monotonicity proof
  (honest-clock bust rate ≥ EOD-clock bust rate, same seeds) actually sound rather than asserted:
  traced the induction directly (identical state up to the first divergence day, and the honest
  clock can only diverge by busting *earlier*, never later).
- `core/mc/preflight.py::firm_kwargs` — read in full; confirmed `dd_type=="trailing"` (L169-171)
  never threads `dd_lock_offset_usd` (that branch is `trailing_locking`-only, L172-180), so the
  script's "no lock-unreachable patch needed" premise holds.
- `lab/discovery/prop_survivor_scoring.py` — read in full, including that
  `run_class_s_c1_regime_gate._consistency_frac` (used by `W1._run_partition`, which the new
  runner reuses) is byte-identical to `prop_survivor_scoring._consistency_frac` — no drift between
  the two copies.
- `r1_bulenox_blusky_intraday_report.json` — every figure in the RESULTS.md §3 table and this
  audit note's headline numbers traced back to this file field-by-field; internally consistent.
- The "5 tiers carry no published figure" claim — independently repo-grepped for
  `Bulenox_25K|Bulenox_50K|Bulenox_150K|Bulenox_250K|BluSky_Premium_50K` (11 files hit); read the
  unfamiliar ones not already cited in §0 (`docs/briefs/Q-FIRMEOD-1-eod-breach-clock-bulenox-blusky.md`,
  `docs/adr/2026-08-05-blusky-inactivity-unsourced-encoding.md`, `tests/core/test_mc_preflight.py`,
  the `prop-firm-challenge` skill doc) — none carry a bust/pass MC figure, only rule-config/
  inactivity-sourcing content. Claim holds.
- The two monotonicity-disposed candidates' cited figures — read
  `lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md` (Bulenox 7.38%, BluSky 8.76%) and
  `lab/archive/q_compose_1_2026-07/RESULTS.md` (Bulenox 44.75%, BluSky 51.91%) directly; both
  quoted figures match byte-for-byte.
- All three reader-intercept banners (`CORRECTED_FULLPANEL.md`,
  `class_s_candidate1_scoring_2026-07-15/RESULTS.md`, `tradeify_eval_lock_correction_2026-07-22/RESULTS.md`)
  — read post-fix (commit `949b6b3` already corrected the one wrapped-heading defect); all three
  render as single-line blockquote headers now.
- Forbidden-moves compliance — `git diff` over the full R1 range touches no line in
  `core/firm_rules.py`, `core/dd_protection.py`, `STATE.md`, or `docs/SESSIONS.md`.
- Re-ran (not just re-read): `pytest tests/core/test_mc_intraday_barrier.py -q` → `9 passed`;
  `pytest tests/core/ tests/test_prop_survivor_scoring.py -q` → `240 passed, 4 skipped in 261s`
  (matches the prior implementer's figures exactly); `check_boundaries.py`,
  `check_status_consistency.py`, `check_closure_disposition.py`, `sync_liveness_indexes.py`,
  `check_root_doc_liveness.py`, `check_path_liveness.py`, `archive_lab_analysis.py --check
  --catalog-only` — all `OK` (the CATALOG one-liner WARNs are pre-existing and affect ~10 other
  unrelated rows, not specific to this campaign's row). Did **not** re-run the ~24-minute MC
  campaign itself (`run_r1_bulenox_blusky_intraday.py`) — the deterministic seeded computation was
  already traced code-path-by-code-path above and its output cross-checked field-by-field against
  both the JSON and the RESULTS.md table; re-running would reconfirm an already-traced
  deterministic result, not surface anything the code audit could not.

**One gap found and fixed:** the parent plan
([`docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md`](../../superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md))
opens with "REQUIRED SUB-SKILL: `superpowers:subagent-driven-development` or
`superpowers:executing-plans`. Checkbox (`- [ ]`) syntax for tracking" — but Task R1's four
checkboxes were still `- [ ]` and the Gate (R1) line still read as an unfired conditional
("`RESOLVED` **when**...") even though every item was independently re-verified complete above.
Left as-is, a reader of the plan (human or agent) would see an apparently-unstarted Task R1
alongside this note's own `Closed` disposition — a source-of-truth fracture of exactly the class
this repo's own doc-discipline culture flags. **Fixed:** checked all four Task R1 boxes and
rewrote the Gate line to a fired `RESOLVED` statement pointing at this note and the RESULTS doc.
Scope note: Task R2's and R3's checkboxes in the same plan file were **not** touched — out of
scope for a Task R1 fix pass (R2 landed separately at `65dc17b` under its own task; R3 is
unblocked-but-not-run per §11 above, correctly still open).

**Nothing else changed.** No finding rose to a level requiring any edit to the RESULTS doc, the
JSON report, the runner script, the CLAUDE.md caveat text, the CATALOG row, or any of the three
reader-intercept banners — all held up under independent re-verification as written.

**Verification (this pass):**

```bash
python -m pytest tests/core/test_mc_intraday_barrier.py -q
# 9 passed

python -m pytest tests/core/ tests/test_prop_survivor_scoring.py -q
# 240 passed, 4 skipped

python scripts/check_boundaries.py
python scripts/check_status_consistency.py
python scripts/check_closure_disposition.py
python scripts/sync_liveness_indexes.py
python scripts/check_root_doc_liveness.py
python scripts/check_path_liveness.py
python scripts/archive_lab_analysis.py --check --catalog-only
# all OK/CLEAN

grep -n '\[x\]' docs/superpowers/plans/2026-08-23-viable-strategy-parallel-s4-firm-repair.md
# Task R1's 4 items now checked
```
