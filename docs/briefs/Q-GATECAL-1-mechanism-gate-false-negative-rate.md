# Q-GATECAL-1 — Mechanism gate false-negative rate

**Status:** `OPEN — DRAFT (pre-lock)`
**Authored:** 2026-08-29
**Closed:** N/A
**Authors:** Joshua + claude.ai (advisor)
**Parent question:** N/A (forked from Notice N-2026-08-25 row 3f, not a gated Q)
**Sub-questions opened:** N/A
**Loop:** Inquire-phase Pre-Q — closes on RESOLVED / FALSIFIED / AMBIGUOUS-HOLD per §6; K=8 blind-lane registration required before the stratified draw (§7 Phase 2)
**Artifact path:** `docs/briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md`

---

## §0 — Rule 0 reads (production-source verification)

- `docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md` — anchor: `a360976` (2026-08-25)
- `docs/notes/audits/2026-08-23-kill-register-attribution-audit.md` — anchor: `00c8451` (2026-08-23)
- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` — anchor: `340722c` (2026-08-24)
- `docs/adr/2026-06-14-rejected-candidate-patterns.md` — anchor: `027a729` (2026-08-14)
- `docs/rejected_candidates.md` — anchor: `0c305d7` (2026-08-24)
- `lab/discovery/register_search.py` — anchor: `c68a450` (2026-08-23)
- `lab/research_utils/deflated_sharpe.py` — anchor: `027a729` (2026-08-14)
- `scripts/cost_geometry_pregate.py` — anchor: `027a729` (2026-08-14)
- `lab/research_utils/selection_tests.py` — anchor: `027a729` (2026-08-14)
- `docs/methodology/regime_robustness_gate.md` — anchor: `bd00f72` (2026-08-24)
- `.claude/skills/strategy-validation/SKILL.md` — anchor: `bd00f72` (2026-08-24)

**Amendment-first (this session, before authoring):**

```
$ python scripts/check_advisor_dedup.py --keywords "gate calibration false negative mechanism admission" --top 8
check_advisor_dedup: keywords: 'gate calibration false negative mechanism admission'
  slugs found:    (none)
  keywords found: 6 significant terms

POSSIBLE PRIOR ART — review before treating the keywords as new work (top 8 of 222 candidate(s)):

  [  6] docs/notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md — Conventions friction — Delete-phase gap audit — 2026-08-08
        shared terms: ['admission', 'calibration', 'false', 'gate', 'mechanism', 'negative']

  [  6] docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md — SLR-MYM-1 — sweep-liquidity-reclaim at the open, MYM third leg (scoping)
        shared terms: ['admission', 'calibration', 'false', 'gate', 'mechanism', 'negative']

  [  5] docs/briefs/closures/Q-INTAKEGOV-1-closure-ambiguous-hold.md — Q-INTAKEGOV-1 — CLOSURE: `AMBIGUOUS-HOLD` (limbs split — B2 holds, D2 confirms, C4 confirms)
        shared terms: ['admission', 'false', 'gate', 'mechanism', 'negative']

  [  5] docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md — SLR-MYM-1 — CLOSURE: `FALSIFIED (as scoped)` at Stage 0
        shared terms: ['admission', 'false', 'gate', 'mechanism', 'negative']

  [  5] docs/notes/audits/2026-07-12-disccamp0-gate-reachability-audit.md — Audit Note — DISC-CAMP-0 pre-freeze gate-reachability audit (Q-HARV-0 obligation)
        shared terms: ['admission', 'calibration', 'gate', 'mechanism', 'negative']

  [  5] docs/notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md — Programme audit (object layer) — "single-instrument index-futures intraday OHLCV directional timing" discovery domain
        shared terms: ['admission', 'calibration', 'gate', 'mechanism', 'negative']

  [  5] docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md — Programme audit — strategy-candidate admission/validation gate stack (meta layer)
        shared terms: ['admission', 'false', 'gate', 'mechanism', 'negative']

  [  5] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/01-diagnostics.md — §3 — The seven diagnostic questions
        shared terms: ['admission', 'false', 'gate', 'mechanism', 'negative']

None of the above owns "measure the mechanism gate's FN rate by re-testing sampled rejects
against downstream statistical gates" — nearest neighbors are an unrelated delete-phase-gap
audit, unrelated scoping/closure docs, a gate-*reachability* audit (different question), and the
2026-08-03 gate-stack programme audit (a different meta-layer diagnostic, not this measurement).

$ grep -ril "GATECAL" .   # empty
$ grep -in "gate.calibration" docs/briefs/INDEX.md lab/CATALOG.md   # empty
```

No existing owner. `docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md` was checked and is a
different object — N-2026-08-25 row 3f itself notes "Q-CAPBAND-1's 'gate-calibration' is a
different object (gate-layer counterfactual, no candidate scored)." This brief is the graduation
of N-2026-08-25 row 3f, not a duplicate of anything standing.

---

## §1 — Context & motivation

On 2026-08-25 an external adversarial-lens review (ox-alpha, under the ADR 2026-08-22 base-scope
consult) argued the mechanism-first admission gate (2-A four-clause test) is an uncalibrated
filter stacked on the calibrated DSR floor, and that its false-negative rate against downstream
statistical gates has never been measured — because gate-killed candidates are never run through
them (N-2026-08-25 §1 rows 1a/3f). The reconciliation in that notice refuted the stronger claim
that the gate is *over-correcting* (wall-scope: 13/14 walls legitimately scoped, dryness is a
generation-input problem, not over-tight evaluation; A1: revival list empty under two proposed
citation-based loosenings) but explicitly let the measurement itself stand as "genuinely
novel — open thread... not actionable now... recorded so it is not lost" (row 3f). This brief
opens that measurement, deliberately bounded: K=8, blind-lane registered, stratified against A1's
own kill-class tags, and run only against the validation-stage gates the notice's own §3 boundary
leaves untouched (cost-law, DSR, decay) — never the discovery/mining pipeline that boundary
explicitly withholds authorization for.

**Scope note (disclosed, not silently narrowed):** ox-alpha's claim and 2-A specifically concern
zero-data, ex-ante admission clauses (WHO/WHEN/WHY/HOW-dies). A1's own cell-demonstrated taxonomy
is broader — it also includes computed, already-backtested kill classes such as CADENCE (e.g.
"0.511 trades/wk < 1"), which a candidate can only reach *after* surviving 2-A. This brief's
question (§3) is deliberately posed at that broader "mechanism/evidence-grounding stage" level,
not narrowed to 2-A alone, so its DIRECTION and SIZE strata measure 2-A directly while its
CADENCE stratum measures a different, downstream early-kill screen. §6's RESOLVED disposition
routes each accordingly.

---

## §2 — Prior art / lineage

- **N-2026-08-25-ox-alpha-mechanism-gate-overcorrection** (`RESOLVED`) — names this exact
  measurement as a genuinely novel, not-yet-actionable thread (row 3f) and bars, in §3, using it
  to authorize running candidates through the discovery pipeline, raising any K cap, or treating
  the locked book as a live confirm. This brief's §5 is scoped to stay inside that boundary.
- **A1 kill-register attribution audit** (`Closed`, 2026-08-23) — built and tagged the ~70-row
  kill census this probe's sampling frame reuses (`SIZE / DIRECTION / CADENCE / COST / TRANSFER /
  REGISTRY / POWER / VENUE / SPREAD / EVIDENCE / OTHER`). It tested a different question — would
  two citation-based admission-wording amendments revive a cell — not whether a candidate's
  original construction clears cost-law/DSR/decay. Its own scope explicitly could not touch
  DIRECTION kills (WHY/delete-flip stays untouched by both amendments — Task A3's own phrasing,
  "byte-untouched," confirmed empirically by A1's empty revival list); this probe's DIRECTION
  stratum is the first actual re-test of that class.
- **MSL wall-scope audit** (2026-08-15) — 13/14 walls legitimately scoped, dryness attributed to
  generation-input, not over-tight evaluation. Cited by N-2026-08-25 as the refutation this brief
  does not re-litigate; this probe measures a rate, not whether the gate's *wording* is too strict.
- **Q-CAPBAND-1** (`RESOLVED`) — a different "gate-calibration" object per N-2026-08-25's own
  reconciliation (gate-layer counterfactual, no candidate scored); not a prior owner of this
  question.

---

## §3 — Question (Q-GATECAL-1)

**Q-GATECAL-1:** Of candidates killed at the mechanism/evidence-grounding admission stage, what
fraction would have cleared the downstream statistical gates (cost-law, DSR at own K,
decay/split-half) had they been let through?

(Symptom-only: names what is unmeasured, not what to do about the gate if the rate turns out
nonzero.)

---

## §4 — Falsifiable hypothesis (H-GATECAL-1)

**H-GATECAL-1:** If ≥1 of 8 stratified-random mechanism-stage kills clears cost-law (cost_R <
0.05, i.e. ≥4× hurdle) **AND** clears DSR at its own K (DSR ≥ 0.95) **AND** survives the decay
check (§8), then the mechanism gate has a nonzero measured false-negative rate on this sample;
otherwise (0/8 clear all three) the gate is measured clean on this sample.

**Reject H-GATECAL-1 if:** 0/8 sampled candidates clear all three gates.
**Accept H-GATECAL-1 if:** ≥1/8 sampled candidates clears all three gates. (Report raw count and
rate — e.g. "2/8 = 25%" — as a sample statistic, not a population estimate.)
**Ambiguous-hold if:** after one pre-declared substitution attempt per irrecoverable slot (§7
Phase 3), ≥2 of the 8 drawn slots remain UNTESTABLE for lack of reconstructable logic + data
(i.e. fewer than 7 of 8 produce a verdict).

---

## §5 — Forbidden moves

- **Expanding the sampling frame after the K=8 registration is open** (e.g., pulling in the 27
  `ops/instruments/*.md` DEAD tables A1 only spot-checked one of) — ruled out because the frame
  must be frozen before the stratified draw; this is a real, found gap, tempting to "fix" mid-probe.
- **Including category-inherited kills** (killed by citation to a prior kill, never independently
  run — ~19 of the ~70 rows per A1 §8) — ruled out; "would this have cleared" isn't well-posed for
  a construction that was never itself measured. Frame is restricted to cell-demonstrated kills.
- **Running discovery/mining tools (STUMPY, tsfresh, gplearn, etc.) on a sampled candidate during
  reconstruction** — ruled out because N-2026-08-25 §3 explicitly withholds authorization for
  running rejected candidates through the discovery pipeline. This probe runs validation-stage
  gates only (cost-law, DSR, decay); it never re-mines or extends a sampled candidate.
- **Treating a nonzero finding (≥1/8) as authorizing a change to any screening step** — 2-A
  admission clauses (relevant only if a DIRECTION/SIZE candidate clears) or the CADENCE
  activity-floor screen (relevant only if the CADENCE candidate clears) — ruled out; this probe
  measures a rate. Any structural response is a separate, freshly-scoped ADR decision (§6 RESOLVED
  disposition).
- **Re-interpreting "clears" after seeing results** (e.g., loosening cost_R < 0.05 or DSR ≥ 0.95
  because a near-miss looks compelling) — ruled out per Known Trap #12; thresholds are frozen in
  §8 before any candidate is touched.
- **Silently substituting a different candidate for one that turns out irrecoverable** — ruled
  out; the substitution rule (redraw once within the same stratum, else mark UNTESTABLE) is
  pre-declared in §7, not improvised at execution time.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | ≥1/8 sampled candidates clears cost-law AND DSR AND decay | `ITERATE — hand the finding (raw count/rate + per-candidate detail) to a fresh, separately-scoped ADR deciding whether/how the relevant screen warrants recalibration: 2-A admission clauses if the clearing candidate is DIRECTION/SIZE, the CADENCE activity-floor screen if it is CADENCE. This brief authorizes no change to either screen itself. Entry packet: this closure's per-candidate table. Re-test window: none required.` |
| `FALSIFIED` | 0/8 sampled candidates clears all three gates | `STOP — mechanism gate measured clean on this K=8 blind-lane sample. Re-proposal bar: a fresh probe needs its own newly registered, larger K — not a re-draw of this sample.` |
| `AMBIGUOUS-HOLD` | ≥2 of 8 slots UNTESTABLE after one substitution attempt each (i.e. fewer than 7/8 produce a verdict) | `ITERATE — return target: resolve the reconstruction/data-budget blocker (larger Databento pull budget, or a fresh amendment relaxing the cell-demonstrated-only frame). Re-test window: next session with the blocker resolved.` |

---

## §7 — Execution plan

Self-executing in a Claude Code session with repo + Databento access (this session qualifies).

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — Build the sampling frame.** Pull A1's four-table census verbatim
  (`docs/notes/audits/2026-08-23-kill-register-attribution-audit.md` §2 Table 2, §3 Table 1, §4
  Table 3, §5 Table 4); restrict to
  cell-demonstrated rows (drop category-inherited); keep A1's own per-row tags. Output: a flat
  list, one row per candidate, tagged `DIRECTION | SIZE | CADENCE` (compound-tagged rows assigned
  to their first-listed tag).
- **Phase 2 — K-accounting, then stratified blind draw.** Run:
  ```
  PYTHONPATH=lab python -m discovery.register_search open \
    --tool "gate-calibration-probe" --search-space-size 8 \
    --data-window "2015-01-01:2026-08-01" --lane blind \
    --run-id gatecal_1_2026 --hypothesis "<H-GATECAL-1 text>"
  ```
  before drawing anything. Then draw **5 DIRECTION / 1 SIZE / 2 CADENCE** using a disclosed seeded
  random draw (seed stated in the closure record) from the Phase-1 frame. **SIZE stratum note
  (disclosed, not a mid-probe adjustment):** A1's cell-demonstrated census carries exactly two
  SIZE-tagged candidates (§3.4 USDA prints × ZC/ZS/ZW, §3.5 Bund auction × FGBL). §3.5/FGBL is
  Eurex-listed and excluded from the eligible frame — this repo's only data pipeline is CME-only
  (`databento-data` skill, GLBX.MDP3), so FGBL is not sourceable by any channel this repo has.
  That leaves §3.4 as the sole eligible SIZE candidate: population = draw = 1, so the SIZE slot
  has zero substitution capacity — if §3.4 turns out irrecoverable in Phase 3, it goes straight to
  UNTESTABLE (§4/§6 AMBIGUOUS-HOLD), no redraw is possible. DIRECTION absorbs the freed slot
  (population 8, healthy spare margin).
- **Phase 3 — Reconstruct each drawn candidate.** Follow the registry's pointer to its
  `PREREG_G0.md` / `STAGE1.md` / harness / closure. If logic is prose-only (irrecoverable exact
  construction), redraw once within the same stratum; if the redraw also fails, mark UNTESTABLE.
  Pull required CME panel bytes via the `databento-data` skill's cost-gated dry-run flow (vendor
  CSVs are not git-tracked in this checkout — confirmed, §0).
- **Phase 4 — Run the three gates.**
  - Cost-law: `python scripts/cost_geometry_pregate.py --csv <pulled bars> --symbol SYM --spread
    <px> --stop-atr <mult>` → pass iff `cost_R < 0.05`.
  - DSR: `PYTHONPATH=lab python -m research_utils.deflated_sharpe --returns-file <candidate
    returns> --trials <candidate's own declared K if one exists in `discovery_manifests/`, else 1
    — reported explicitly either way> --threshold 0.95`.
  - Decay: `PYTHONPATH=lab python -m research_utils.selection_tests halves <candidate trades.csv>`
    — pass iff H1 and H2 expectancy are both sign-consistent with the full-sample expectancy and
    neither is negative (§8; no official candidate-level decay gate exists today —
    `regime_robustness_gate.md` is scoped to `dd_protection` risk-constant sweeps, not strategy
    candidates, so this probe adopts and discloses its own threshold rather than borrowing that one).
- **Phase 5 — Verdict assertion and closure.** Apply §6 literally; close the K=8 registration
  (`register_search.py close --run-id gatecal_1_2026`, p-value-equivalent per candidate derived
  from the DSR statistic — exact convention confirmed against the script at execution time, not
  guessed here); author the closure record.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

Separate file: `docs/briefs/pre-registration/Q-GATECAL-1-verdict-preregistration.md`, committed
before Phase 1 (register_search open) runs.

Pre-registration commit hash: `<populated at pre-registration commit time>`
Pre-registration date: 2026-08-29

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-GATECAL-1-closure-resolved.md`
- **If FALSIFIED:** `docs/briefs/closures/Q-GATECAL-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-GATECAL-1-closure-ambiguous.md` with explicit
  re-test trigger and date

Must include the mandatory typed `## Iterate` block (Next: INTEGRATE | ITERATE | STOP), the
per-candidate table (tag, cost_R, DSR, decay verdict, overall clear/kill), and a `Registry:` line
(`n/a — this closure measures the gate, it does not open or close a rejected_candidates.md row`).

---

## §10 — Audit hooks (runnable)

```bash
# This brief exists and is well-formed
python scripts/check_brief.py docs/briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md --type inquire

# Pre-registration committed before Phase 1
git log --oneline docs/briefs/pre-registration/Q-GATECAL-1-verdict-preregistration.md

# K=8 registration status
PYTHONPATH=lab python -m discovery.register_search status --run-id gatecal_1_2026

# Confirm the notice's row 3f is the cited origin and has not been separately actioned
rg -n "gate-calibration probe|Q-GATECAL-1" docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md docs/methodology/ docs/adr/

# §0 anchors still resolve
git log -1 -- docs/notes/audits/2026-08-23-kill-register-attribution-audit.md | grep 00c8451
```

---

## Verification

```bash
# Discipline checks (mechanical) — inquire
$ python scripts/check_brief.py docs/briefs/Q-GATECAL-1-mechanism-gate-false-negative-rate.md --type inquire
# Expected: RESULT: well-formed

# Production-source verification (Rule 0 confirmation)
$ git log -1 -- docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md
$ git log -1 -- docs/notes/audits/2026-08-23-kill-register-attribution-audit.md

# Cross-reference verification
$ rg -n "row 3f|gate-calibration probe" docs/notes/notice/N-2026-08-25-ox-alpha-mechanism-gate-overcorrection.md

# Pre-registration commit verification
$ git log --oneline docs/briefs/pre-registration/Q-GATECAL-1-verdict-preregistration.md
# Expected: pre-registration commit predates first analysis script run (none has run yet)
```

If any verification command fails, the brief is not complete. Re-author the section that broke;
do not handwave.

---

## Adversarial review record

`pre-ratification-adversarial-panel` run against this brief 2026-08-29 (6-lens review → 2-skeptic
verify → adjudication, 42 agents). Verdict: **BLOCKED**, 4 confirmed BLOCKERs. All 4 repaired in
this revision:

1. SIZE stratum was a deterministic full-inclusion of an unsourceable FGBL/Eurex candidate — fixed
   by restricting SIZE to its true 1-candidate sourceable population, rebalancing to 5/1/2 (§7).
2. CADENCE is a downstream computed kill, not a 2-A zero-data admission kill — fixed by broadening
   §1/§6's stated scope and disclosing which strata implicate 2-A vs. the CADENCE screen.
3. (Same root cause as #1, combinatorics framing.) Fixed alongside #1.
4. Pre-registration's gate table was mislabeled "verbatim" while actually paraphrased — fixed;
   now byte-for-byte identical to §6 (verified by diff).

Three items the panel explicitly left as **operator judgment, not resolved here**:

- **D1:** whether opening this brief (per `notice_log.md`'s GRADUATE convention: "Open `Q-X-
  [slug].md`" — no further ADR/operator step named) is itself sufficient graduation of
  N-2026-08-25 row 3f's "future-consideration pointer only" framing, or whether Phase 1 (the K=8
  register_search open + draw) additionally needs an explicit operator GO before it runs.
- **D2:** whether the brief adequately distinguishes this probe's question from A1's (revival
  eligibility) for every stratum — the DIRECTION distinction is clean (A1 left it byte-untouched);
  the SIZE distinction is narrower now that only §3.4 is eligible, but A1's own empty-revival
  finding on §3.4 is still directly adjacent and worth the operator's own read before Phase 1.
- **D3:** whether the 27-file `ops/instruments/*.md` DEAD-table coverage gap (§5) needs a
  dedicated forward-pointer beyond its current home in Forbidden Moves.

**Phase 1 (register_search open + draw) is held pending explicit operator sign-off on D1.**

---

## Pre-Lock Checklist (DRAFT briefs only)

Remove this section once the brief is locked.

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [x] §5 forbidden moves are genuinely tempting, not strawmen
- [x] §6 gates have specific numerical triggers
- [x] §8 pre-registration committed BEFORE Phase 1 runs — both files committed in the same push,
      before Phase 1 (no `register_search open` has run for this probe)
- [x] §10 audit hooks are runnable commands
- [x] Verification block executed and passing — both `check_brief.py` checkers green; adversarial
      panel run, 4 confirmed BLOCKERs repaired (see Adversarial review record above)
- [ ] Operator sign-off on D1 (self-execution authorization) obtained before Phase 1 runs
