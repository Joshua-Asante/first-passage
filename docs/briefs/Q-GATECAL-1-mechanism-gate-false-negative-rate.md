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
# nearest: conventions delete-phase-gap audit; SLR-MYM-1 scoping; Q-INTAKEGOV-1;
# gate-reachability audit; gate-stack audit (K-banking, unrelated finding).
# None owns "measure the mechanism gate's FN rate by re-testing sampled rejects."

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
  DIRECTION kills (WHY/delete-flip stays "byte-untouched" by both amendments); this probe's
  DIRECTION stratum is the first actual re-test of that class.
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
Phase 3), fewer than 6 of the 8 drawn slots produce a verdict (i.e. ≥2 slots remain UNTESTABLE for
lack of reconstructable logic + data).

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
- **Treating a nonzero finding (≥1/8) as authorizing a change to the mechanism admission clauses
  (2-A)** — ruled out; this probe measures a rate. Any structural response is a separate,
  freshly-scoped ADR decision (§6 RESOLVED disposition).
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
| `RESOLVED` | ≥1/8 sampled candidates clears cost-law AND DSR AND decay | `ITERATE — hand the finding (raw count/rate + per-candidate detail) to a fresh, separately-scoped ADR deciding whether/how the 2-A admission clauses warrant recalibration. This brief authorizes no change to 2-A itself. Entry packet: this closure's per-candidate table. Re-test window: none required.` |
| `FALSIFIED` | 0/8 sampled candidates clears all three gates | `STOP — mechanism gate measured clean on this K=8 blind-lane sample. Re-proposal bar: a fresh probe needs its own newly registered, larger K — not a re-draw of this sample.` |
| `AMBIGUOUS-HOLD` | ≥2 of 8 slots UNTESTABLE after one substitution attempt each (fewer than 6/8 produce a verdict) | `ITERATE — return target: resolve the reconstruction/data-budget blocker (larger Databento pull budget, or a fresh amendment relaxing the cell-demonstrated-only frame). Re-test window: next session with the blocker resolved.` |

---

## §7 — Execution plan

Self-executing in a Claude Code session with repo + Databento access (this session qualifies).

- **Phase 0 — Rule-0 reads.** Done (§0).
- **Phase 1 — Build the sampling frame.** Pull A1's four-table census verbatim
  (`docs/notes/audits/2026-08-23-kill-register-attribution-audit.md` §3–§6); restrict to
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
  before drawing anything. Then draw 4 DIRECTION / 2 SIZE / 2 CADENCE using a disclosed seeded
  random draw (seed stated in the closure record) from the Phase-1 frame.
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

## Pre-Lock Checklist (DRAFT briefs only)

Remove this section once the brief is locked.

- [x] All §0 paths read and anchored with commit hash
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [x] §5 forbidden moves are genuinely tempting, not strawmen
- [x] §6 gates have specific numerical triggers
- [ ] §8 pre-registration committed BEFORE Phase 1 runs — pre-registration file authored this
      session; commit ordering to be confirmed once both files land in the same push
- [x] §10 audit hooks are runnable commands
- [ ] Verification block executed and passing — pending `check_brief.py` run + adversarial pass
