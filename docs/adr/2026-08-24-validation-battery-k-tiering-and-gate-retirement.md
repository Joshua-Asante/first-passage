# ADR 2026-08-24 — Validation-battery K-tiering, cost-law ownership, and pursuit-records retirement

**Status:** `Accepted` — ratified via operator in-session instruction to execute the
validation-phase-cuts plan (2026-08-24); see Ratification note.
**Decision date:** 2026-08-24
**Authors:** Joshua Asante (+ Claude Code, drafter)
**Supersedes:** nothing. No prior ADR states a K-tiering rule for §8's universe-level correction,
names a canonical cost-law owner, or rules on `pursuit-records`.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [Rule 16 — retention](../operational_rules.md#16-retention) · [great-prune ADR](2026-08-08-great-prune.md)
(§2 retention test, cited as authority) · [three-loop methodology binding](2026-06-12-three-loop-methodology-binding.md)
(`Accepted` — D2 STRATEGIC-Delete channel, cited and ruled inapplicable) ·
[gate-stack programme audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
(G7/G8 findings, provenance for §1) · [harv-attestation-same-units-supersession ADR](2026-07-16-harv-attestation-same-units-supersession.md)
(cost-law Requirement 5's own owning ADR, untouched) · [instrument-profile-index ADR](2026-07-25-instrument-profile-index.md)
(profile_cell/profile_consult enforcement, already-landed — cited in §1)
**Layer:** research governance / tooling retirement — no live-risk surface; no locked parameter;
no allocation; no arming. **$0 / K=0.**
**Loop-of-Record:** STRATEGIC — a standing-rule change to the validation battery's multiplicity
accounting and a deletion from the repo's gate-composition manifest (`scripts/gates.yml`),
governed by Rule 16 (retention), not by D2's programme/track/instrument-tier Delete channel — see
§2 D5 below for why.

---

## §0 — Rule 0 reads (this worktree, 2026-08-24)

- `.claude/skills/strategy-validation/SKILL.md` — anchor `1a07c35` (2026-08-21). Read in full.
  §5 ("Selection & multiplicity accounting") covers **within-panel** selection (best-of-K subset
  under a demeaned null; label-permutation) via `scripts/selection_tests.py`. §8 ("Universe-level
  correction & selection-under-K") covers selection **across K distinct candidates/configs** —
  its own text: *"§5 tests selection WITHIN one panel… §8 tests selection ACROSS K distinct
  candidates."* K-tiering belongs in §8, not §5 — see §1 correction below.
- `lab/research_utils/selection_tests.py` (canonical; `.claude/skills/strategy-validation/scripts/selection_tests.py`
  is a thin subprocess launcher, not independent code) — anchor `1a07c35`. Read in full. `bestof`
  (§5b) and `perm` (§5c) are both non-parametric Monte Carlo permutation tests, **distinct** in
  input shape (within-panel covariate split vs. cross-CSV pooling) and null construction (demeaned
  synthetic null vs. actual-returns reshuffle). Neither is parametric or "deflated-Sharpe-style" —
  that procedure is `lab/research_utils/deflated_sharpe.py`, a wholly separate module documented
  in SKILL.md §8b, not §5. **Verdict: not duplicative. No merge.**
- `docs/methodology/strategy_harvest.md` — anchor `ac05de6` (2026-08-24). Read §1 Requirement 5
  and §2.2 in full. Requirement 5 (line 30) states the cost-law inequality
  `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, frozen execution model, commissions
  included)` and is its own declared sole authority; §2.2 (line 67) explicitly declines to
  restate it: *"No independent constant or formula lives here; Requirement 5 is the sole
  authority."*
- `docs/methodology/lessons/methodology_lessons.md` M-20 (lines 898–913) — anchor `1a07c35`. Read
  in full. Restates Requirement 5's inequality **verbatim**, uncredited as a duplicate — a true
  Rule 7 violation (silent restatement, not a labeled mirror). `strategy_harvest.md`'s own
  audit-hook script scopes its uniqueness check to `strategy_harvest.md` itself, so it cannot see
  this duplicate.
- `lab/discovery/register_search.py::_require_cost_law` (lines 563–627) — anchor `c68a450`
  (2026-08-23). Read in full. Does **not** restate the formula; calls `cost_model.bp_hurdle`
  (shared arithmetic, `COST_LAW_MULTIPLE = 4.0` in `lab/discovery/cost_model.py`). Already Rule-7
  compliant — no edit needed.
- `.claude/skills/strategy-validation/SKILL.md` §2 "Cost-law pre-flight" (lines 24–28) — states a
  **different** formula: `cost_R ≈ [2·commission_pct·price + 2·slippage_ticks·ticksize] ·
  (price/stop_dist) / price`, a per-trade R-multiple/stop-distance form, not Requirement 5's
  per-event bp-of-panel-price form. Both share a "4×" convention and a round-trip-cost skeleton
  but are **not the same fact** — see §1 correction below.
- `scripts/cost_geometry_pregate.py` — anchor `1a07c35`. Read in full. Implements exactly
  SKILL.md §2's stop-distance-R formula (`round_trip_cost_price()` + `cost_r()`), as a runnable
  script with a PASS/FAIL verdict (`cost_R < ceiling`, default 0.05). The true duplicate pair.
- `scripts/gates.yml` lines 42–52 — anchor `44967d6` (2026-08-23). Read the `pursuit-records`
  entry in full: `tier: data-conditional`, `when.staged_regex: '^docs/pursuits/'`, `cmd: python
  scripts/check_pursuit_records.py`.
- `scripts/gate_manifest.py::select_gates()` (lines 140–174) — anchor `1a07c35`. Read in full.
  The `check` branch (the full merge-gating battery) selects only `tier in ("always",
  "path-conditional")` plus one hardcoded force-include (`data-manifests`) — `data-conditional`
  gates, `pursuit-records` included, are never selected by `--tier check`.
- `scripts/check_pursuit_records.py` — anchor `1a07c35`. Read `main()` in full. Both reachable
  exit paths (findings-present, clean) `return 0`; the only non-zero path (`return 2`) requires a
  malformed `--asof` CLI argument the gate's own invocation never supplies. **The script cannot
  fail as invoked by the gate — ever.**
- `docs/operational_rules.md` Rule 16 (lines 672–693) — anchor `aef55a9` (2026-08-23). Read in
  full. R5: *"an operator-signed decision with a still-open, dated, **fireable** obligation. An
  obligation whose check **cannot fire** does not qualify — unfalsifiable ceremony is deletable
  even when signed."* `pursuit-records` matches this exactly: staged-conditional trigger, but the
  check behind it structurally cannot produce a failing verdict.
- `lab/discovery/register_search.py::open_run` (lines 640–710) — anchor `c68a450`. Read in full.
  For `lane == "mechanism-first"` (the default since before this session — `--lane` default is
  `"mechanism-first"`, line 900), `_require_profile_consult`, `_require_admission`, and
  `_require_prereg` each hard-`sys.exit()` before any manifest write if `profile_cell` /
  `profile_consult` / `admission` / `prereg` are missing. **This enforcement is already landed —
  see §1 correction below.**
- `discovery_manifests/*.json` (17 files, repo root — not under `lab/discovery/`) — read all 17.
  **0 of 17 carry `profile_cell` / `profile_consult` / `admission` / `prereg` as a JSON key.**
  Every one predates the enforcement above; `open_run` refuses to overwrite an existing manifest
  ("Pre-registration is immutable"), so there is no retroactive-write path — these 17 stay
  permanently at their opened-at schema.
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` D2 (line 57) — anchor `1a07c35`. Read
  in full — see §2 D5 below for why its STRATEGIC-Delete channel does not govern the
  `pursuit-records` deletion in this ADR.

**Amendment-first / dedup (Rule 8 sub-rule 10):**

```
$ python scripts/check_advisor_dedup.py --keywords "cost law K tiering multiplicity pursuit-records gate retirement profile_cell profile_consult"
```
No existing ADR or brief performs any of this ADR's four decisions. The 2026-08-03 gate-stack
audit's G7/G8 findings (zero manifests bound, `--lane` defaulting to `"blind"`) are the closest
prior art and are **stale as of this session's read** — see §1.

**Judgment:** no true prior owner for D1–D4 below; this is fresh ground, correctly scoped by the
reads above rather than by the originating plan's own framing (see §1 correction).

---

## §1 — Context

The validation-phase-cuts plan carried forward into this session proposed four cuts. Verification
against production source this session found the plan's diagnosis correct on the shape of the
problem in three of four cases, but its specifics needed correction before landing in a permanent
record:

1. **K-tiering was proposed for SKILL.md §5.** §5 has no K-awareness at all — it is a within-panel
   test suite. The K-driven multiplicity-correction layer the plan is actually describing lives in
   §8 ("selection-under-K"). Placing a K-tiering rule in §5 would misfile it against Rule 7's "one
   canonical owner per fact" and create exactly the kind of drift Rule 7 exists to prevent.
2. **"5 cost-law restatement sites, collapse to one."** Direct reads found **two distinct
   formulas**, not one formula stated five times: a per-event bp-of-panel-price form (Requirement
   5 / M-20, verbatim-identical) used at harvest/admission time, and a per-trade
   stop-distance-R form (SKILL.md §2 / `cost_geometry_pregate.py`, verbatim-identical) used as a
   pre-build design-time sanity check. Only the true duplicate pairs need consolidating; treating
   both formulas as one fact would itself be a Rule 7 violation in the other direction.
   `register_search.py`'s cost-law pre-flight was flagged as a fifth site in the plan but is
   already compliant — it calls shared arithmetic and restates nothing.
3. **"Enforce or remove profile_cell/profile_consult/admission/prereg — rule on it in this ADR."**
   The code already enforces all four (hard abort before any mechanism-first manifest write) as
   of this session's read. This was landed after the 2026-08-03 gate-stack audit's G7/G8 findings
   (which the plan's framing was implicitly still working from) and after `--lane`'s default
   flipped from `"blind"` to `"mechanism-first"`. There is nothing left to rule on; this ADR
   records the closure instead of re-deciding it.
4. **`pursuit-records` retirement.** Confirmed exactly as proposed — `tier: data-conditional`,
   never selected by `--tier check`, and the underlying script structurally cannot exit non-zero
   as invoked. This is Rule 16 R5's textbook case.

The plan also cited an "add-back-metric-layer-split ADR" as the source of a STRATEGIC-tier
adjudication requirement for the `pursuit-records` deletion. That ADR (`2026-07-01-add-back-metric-layer-split.md`)
exists but governs a methodology calibration metric — it contains no adjudication-authority
clause. The actual rule (`2026-06-12-three-loop-methodology-binding.md` D2) governs
programme/track/instrument-tier **Delete verdicts**, not gate-infrastructure retirement — see §2
D5. Rule 16 is gate infrastructure's own governing authority and needs no separate adjudication
gate beyond its own R1–R5 retention test.

---

## §2 — Decision

**D1 — K-tiering for §8 selection-under-K (not §5).** Add to
`.claude/skills/strategy-validation/SKILL.md` §8: at declared search-space size **K∈{0,1}**, the
universe-level multiplicity correction (§8a SPA/StepM/MCS, §8c PBO-via-CPCV) is a **declared
no-op** — logged as "K≤1, correction not applicable" rather than silently never invoked. At
**K∈{2,3}**, the correction runs. This is the only band where it is both reachable and
load-bearing: in the standard/mechanism-first admission lane, `lab/discovery/admission_schema.py`
(via `research_utils.axis_screen.floor_at_k`, `CAP = 1.0`) refuses to open a manifest once
`floor_at_k(K) > CAP`, which the code's own comment states occurs "at K≥4 at current Cap" for the
standard 6.5-year confirm window — a candidate cannot reach §8 with K≥4 in that lane at all
(`ABORT-NO-MANIFEST`). §8b (deflated Sharpe / DSR) is unaffected — it is already K-aware by
construction (`SR0` is a function of K) and does not need a declared-no-op convention; the
K-tiering addition is scoped to §8a/§8c only, which are gated as DORMANT-unless-re-armed
independent of K.

**D2 — Cost-law: two owners, correctly separated, not one.**
- Per-event bp-of-panel-price form: `docs/methodology/strategy_harvest.md` §1 Requirement 5
  remains sole canonical owner (already self-declared as such; unedited). `methodology_lessons.md`
  M-20 is rewritten from a verbatim restatement into an explicitly-labeled derived mirror per
  Rule 7(b) — the lesson's narrative content stays, the formula is replaced with a pointer.
- Per-trade stop-distance-R form: `scripts/cost_geometry_pregate.py` becomes canonical owner (it
  is the runnable implementation with an enforced PASS/FAIL verdict).
  `.claude/skills/strategy-validation/SKILL.md` §2 is rewritten to state the convention (target ≥
  4× hurdle) and point to the script instead of restating its formula inline.
- `lab/discovery/register_search.py`'s cost-law pre-flight needs no edit — already compliant.

**D3 — Retire `pursuit-records` from `scripts/gates.yml`.** Deletes the `id: pursuit-records`
entry (lines 42–52) and `scripts/check_pursuit_records.py`'s gate wiring. Governed by Rule 16 R5:
an obligation whose check cannot fire does not qualify, "unfalsifiable ceremony is deletable even
when signed." Execution follows Rule 16's mandatory four-part scan (§4 below) before the deletion
commit lands, per Rule 16's own procedure — not a separate adjudication step.

**D4 — Record the profile_cell/profile_consult/admission/prereg enforcement as already-closed.**
No code change. This ADR is the record that `register_search.py open --lane mechanism-first`
already hard-fails on all four missing fields (verified §0), that the 17 pre-existing manifests
are permanently un-backfilled by design (pre-registration immutability), and that this closes the
open question the originating plan carried forward — it does not reopen a decision already made
in code.

**D5 — D2 (three-loop binding) does not govern D3.** The `pursuit-records` gate is repo
tooling/infrastructure, not a programme, track, or instrument. Rule 16 is gate infrastructure's
own governing authority (R1–R5 retention test + the mandatory four-part scan) and requires no
separate STRATEGIC-tier adjudication gate. The operator's in-session instruction to execute this
plan is, independent of D2's applicability, sufficient authorization under Rule 16's own
framework — Rule 16 does not itself require a distinct "adjudication" precondition beyond passing
its retention test.

**Effective:** immediately upon Accept (2026-08-24), with D3's deletion landing only after the
Rule 16 four-part scan (§4) and full `pytest` pass. **$0 / K=0** — no risk constant, no
allocation, no lifecycle authorization touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Put K-tiering in SKILL.md §5, as originally proposed | §5 has no K-awareness; would misfile a fact §8 already owns (Rule 7). |
| Collapse all 5 originally-named cost-law sites into 1 canonical owner | Would conflate two distinct formulas (bp-of-price vs. stop-distance-R) as one fact — a Rule 7 violation in the opposite direction. |
| Merge best-of-K (§5b) and label-permutation (§5c) as duplicative | Verified distinct (different input shape, different null construction) via direct code read; no merge. |
| Rule on profile_cell/profile_consult/admission/prereg enforce-vs-remove | Moot — already enforced in code as of this session; ruling on it would re-decide a closed question. |
| Revert `pursuit-records` to `tier: soft` instead of deleting | The gate's own header comment already rules this out ("do not use tier: soft — dead, no caller"); would keep dead weight in a different shape. |
| Route `pursuit-records` deletion through D2's STRATEGIC-Delete channel | Wrong-scoped authority — D2 governs programme/track/instrument kills, not gate-infrastructure retirement; Rule 16 already governs this class. |

---

## §4 — Falsifier (revert trigger)

**H / Revert trigger:** either (a) a future campaign with a genuinely-reachable K≥4 in the
standard lane surfaces (invalidating the "K∈{2,3} is the only reachable band" premise), or (b) a
future need for `docs/pursuits/` change detection resurfaces and no replacement mechanism exists.

**Revert action:** (a) extend the K-tiering table with a K≥4 band once a real campaign reaches it
under the standard lane's Cap; (b) re-author a pursuit-records-equivalent gate with an actual
failing condition (not a report-only always-0 script) if the need resurfaces — never restore the
deleted file verbatim, since its structural defect (cannot fail) is what earned the deletion.

**Trigger check schedule:** the next quarterly programme-audit cadence, or the next time a
campaign's declared K reaches 4 in the standard admission lane, whichever comes first.

---

## §5 — Forbidden moves (genuinely tempting)

- **Backfilling the 17 existing `discovery_manifests/*.json` with the four now-enforced fields**
  — `open_run` treats pre-registration as immutable by design; retroactively editing a manifest
  after the fact is exactly the drift the immutability rule exists to prevent.
- **Deleting `--lane blind` as a "closing the loophole" follow-on** — out of scope for this ADR;
  removing an existing lane is a separate decision this session did not research the justification
  for (why `blind` exists, what non-mechanism-first candidates still need it).
- **Treating D1's K-tiering as license to skip §8a/§8c even at K≥4** — the tiering rule exists
  *because* K≥4 is unreachable in the standard lane today, not to license skipping correction if
  a future lane change (e.g. the deep lane's own `K_CEILING = 33`) makes it reachable.

---

## §6 — Consequences

**Gate verdict (binary, ties to §4):** RESOLVED — all four decisions land with verified grounds;
no ambiguous or falsified condition present at ratification.

**Positive consequences:**
- SKILL.md §8's multiplicity accounting becomes audit-visible at every K, not silently
  no-op at K≤1.
- Two real cost-law formulas get two correctly-scoped canonical owners instead of one incorrect
  merge; `methodology_lessons.md` M-20 stops silently drifting from Requirement 5.
- `scripts/gates.yml` loses a gate that could never fail, tightening what "the gate battery passed"
  actually asserts.
- Closes a stale open question (profile_cell/consult/admission/prereg) the originating plan was
  working from outdated 2026-08-03 audit context.

**Negative consequences (real cost, not theatrical):**
- One fewer WARN-tier report surface (`pursuit-records`) — mitigated by it never having been able
  to warn-block anything; any real future need re-arms per §4.

**Downstream artifacts updated (this commit):**
- `.claude/skills/strategy-validation/SKILL.md` — §2 rewritten to point at `cost_geometry_pregate.py`;
  §8 gains the K-tiering subsection.
- `docs/methodology/lessons/methodology_lessons.md` — M-20 rewritten as a labeled derived mirror
  of Requirement 5.
- `scripts/gates.yml` — `pursuit-records` entry removed (Phase 4 commit, after the four-part scan).
- `scripts/check_pursuit_records.py` — retained on disk (Rule 16 does not require deleting the
  script itself, only its gate wiring) but no longer invoked by any tier; a header note records
  the retirement and this ADR.

**Downstream artifacts NOT changed:**
- `docs/methodology/strategy_harvest.md` Requirement 5 — already correctly self-declared as sole
  authority.
- `lab/discovery/register_search.py` — already Rule-7-compliant.
- Any of the 17 existing `discovery_manifests/*.json`.
- `lab/discovery/cost_model.py`, `lab/research_utils/selection_tests.py`,
  `lab/research_utils/deflated_sharpe.py` — no code changed, only documentation pointing at them.

---

## §7 — Implementation plan

- **Phase 3** — Edit `SKILL.md` §2 and §8 (D1, D2 pointer half); edit `methodology_lessons.md`
  M-20 (D2 mirror half).
- **Phase 4** — Run the Rule 16 four-part scan on `pursuit-records`; delete the `gates.yml` entry
  and the gate's own header wiring note; run full `pytest`.
- **Phase 5** — Blast-radius grep sweep for any other restatement of either cost-law formula, or
  of the profile_cell/consult/admission/prereg question as still-open.
- **Phase 6** — `python scripts/gate_manifest.py --tier check`; full `pytest`; commit; push; PR.

---

## §10 — Audit hooks (runnable)

```bash
python scripts/check_brief.py docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md --type adr
python scripts/check_adr_graph.py --regenerate-index

# D1: K-tiering lands in §8, not §5.
grep -n "K∈{0,1}\|K∈{2,3}" .claude/skills/strategy-validation/SKILL.md   # expect hits inside §8, not §5

# D2: cost-law formulas stay distinct, each with one owner.
grep -c "cohort δ (bp/event) ≥ 4" docs/methodology/lessons/methodology_lessons.md   # expect 0 after edit (mirror, not restatement)
grep -c "cohort δ (bp/event) ≥ 4" docs/methodology/strategy_harvest.md              # expect 1 (unchanged, sole authority)
grep -c "cost_R ≈" .claude/skills/strategy-validation/SKILL.md                      # expect 0 after edit (pointer, not restatement)

# D3: pursuit-records is gone from the manifest.
grep -c "id: pursuit-records" scripts/gates.yml   # expect 0
python scripts/gate_manifest.py --list | grep -c pursuit-records   # expect 0

# D4: no code change — confirm enforcement is still live.
grep -n "lane == \"mechanism-first\"" lab/discovery/register_search.py
```

---

## Ratification note

**Ratified by:** Joshua Asante, in-session direct instruction to execute the validation-phase-cuts
plan carried forward from a prior conversation (2026-08-24).

**§6-class preconditions at ratification:** §0 populated with anchors and the four scope
corrections (done, this commit) ✓ · the true cost-law formula count (2, not 1) verified against
production source ✓ · the profile_cell/consult/admission/prereg enforcement verified live in code,
not asserted from the stale 2026-08-03 audit ✓

**Not licensed by this ratification:** deleting `--lane blind`; backfilling any of the 17 existing
manifests; any edit to `core/`, `ops/`, `dd_protection`, or allocations; any change to
`lab/discovery/cost_model.py`'s or `deflated_sharpe.py`'s actual arithmetic.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring and ratification — K-tiering scoped to §8, cost-law split into its true two owners, pursuit-records retirement, profile-field question recorded as already-closed. | Claude Code, operator-directed |
