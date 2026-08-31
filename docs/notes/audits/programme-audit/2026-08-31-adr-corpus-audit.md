# ADR corpus audit — third pass, evidence-based this time

**Audit ID:** AUDIT-2026-08-31-ADR-CORPUS
**Date:** 2026-08-31 · **Trigger:** operator direction ("I have 174 ADRs. I do not believe I need
174 ADRs... suggest deletions, consolidations, or simplifications").
**Authors:** Joshua (direction + rulings) + Claude Code.
**Method:** an inbound-reference index built first (bare-filename-stem scan across every
git-tracked file — prose citations, backticked paths, and audit-hook `rg` commands count, not
just markdown links — the instrument the Great Prune ADR §3.2/§4a said any future prune must
start from), then an 11-agent parallel classification pass reading all 172 live ADRs in full
(170 of 172 covered directly; the 2 missed by a batch-construction slip —
`2026-08-08-great-prune.md`, `2026-08-08-s2b-signal-daemon-build.md` — were confirmed KEEP by
direct inbound-reference check, §7), then adversarial verification (default-refute posture) of
every DELETE/CONSOLIDATE/STATUS_FIX proposal, then synthesis.

---

## §1 — Result

| Verdict | Count |
|---|---:|
| KEEP_AS_IS | 99 |
| STATUS_FIX | 33 |
| SIMPLIFY | 27 |
| CONSOLIDATE | 16 (unique files; some appear in more than one proposed family) |
| DELETE | 1 |

**Adversarial verification: 12 of 50 proposals survived (24%).** Zero consolidations, zero raw
deletions. This is the third independent pass over this corpus, and the running total of ADRs
that should be deleted stays at zero:

| Pass | Proposals | Survived | Precision |
|---|---:|---:|---:|
| Great Prune (2026-08-08) | 166 deletes | 3 of 69 reviewed | 4.3% |
| F-2 corpus read (2026-08-14) | 4 deletes | 0 | 0% |
| This pass (2026-08-31) | 50 (16 consolidate, 33 status, 1 delete) | 12 (0 consolidate, 0 delete, 11 status, 1 delete→retirement) | 24% |

## §2 — What the corpus actually costs

172 ADRs (175 files in `docs/adr/`; `INDEX.md`/`README.md`/`TOMBSTONES.md` are not ADRs).
**Only 11 of 172 have zero inbound references anywhere outside `docs/adr/`**, and 7 of those 11
are dated 2026-08-24 or later — too new to have accrued citations. ~100 ADRs are cited by code,
tests, gate scripts, `ops/instruments/*.md`, or lab `RESULTS*` files.

**File count cannot go down through the sanctioned instruments.** `scripts/retire_adr.py` moves
a retired/superseded/withdrawn body to `docs/ltm/adr/` and leaves a stub **at the same path** —
the count is unchanged by design. The only mechanism that removes a file is `TOMBSTONES.md`
(10 rows, all from the one 2026-08-08 prune whose broader delete classes were then halted on
measured 4.3% precision). Only 4 of 172 ADRs have ever gone through the cold-store path at all —
the disposal mechanism this repo already built is 98% unused, independent of anything found today.

**The real cost is words, and specifically scaffolding words.** Direct measurement of the whole
corpus: **428,817 words across 172 ADRs.** 38.5% of that (164,944 words) sits in seven repeating
template sections:

| Section | Words | Files carrying it | Avg/file |
|---|---:|---:|---:|
| §0 Rule-0 reads | 46,486 | 132 | 352 |
| §6 Consequences | 32,679 | 134 | 243 |
| §3 Alternatives considered | 27,583 | 128 | 215 |
| §10 Audit hooks | 20,965 | 134 | 156 |
| §7 Implementation plan | 15,643 | 101 | 154 |
| Change history | 14,598 | 103 | 141 |
| Verification | 6,990 | 106 | 65 |

**Growth is a minting-rate problem, not a verbosity problem.** Mean words/ADR is flat month to
month (~2,300). Monthly totals: Mar 528 → Apr 5,968 → May 29,274 → Jun 52,972 → Jul 133,724 →
**Aug 206,363**. August alone is 48% of every ADR word ever written, in 31 days. The sharpest
single data point: 2026-08-30 produced six ADRs, 22,734 words, from one operator instruction
("ratify the six ADRs").

**Reframe:** the target is not "fewer ADRs" (structurally near-fixed, and ~100 of 172 are
genuinely load-bearing) but **fewer scaffolding words and a tighter live-obligation set.**

## §3 — Executed this session

1. **`2026-03-01-aegis-session-selection.md` retired** (`scripts/retire_adr.py ... --reason
   retired`). Zero inbound references corpus-wide, all three supersession fields `none`, CFD
   estate retired, Aegis→6J lane separately closed. Both dated risk obligations in the body are
   dead: the 2026-04-28 BOJ meeting passed with no disposition recorded, and the DST-alignment
   check has no cadence to fire on. Recorded in the stub's Disposition line rather than left
   implicit.

   This is also the exact file `check_adr_graph.py`'s **A5 age-prune check** (enabled by default,
   HARD severity) fires on starting **2026-09-01** — confirmed directly:
   ```
   $ python scripts/check_adr_graph.py --today 2026-09-01
   HARD: docs/adr/2026-03-01-aegis-session-selection.md:4: A5 Accepted ADR older than 6 months with no inbound refs
   ```
   The `adr-graph` gate is path-conditional on `docs/adr/`/`STATE.md`, so the next ADR edit or
   STATE touch would have been blocked at pre-commit had this not been done today. Forward fire
   dates for awareness (not owed today): 2026-10-17 (`2026-04-17-guardian-v5.1-architecture.md`,
   `2026-04-17-striker-v4.3-pyramid.md` — **redact before touching**, see §7), 2026-11-03
   (`2026-05-03-sentinel-gate-decision.md`), 2027-01-15 (`2026-07-15-repo-rename-first-passage.md`),
   2027-02-20 (`2026-08-20-rule0-anchor-verification-and-triage-discipline.md`).

2. **`scripts/check_advisor_dedup.py` fixed** — `docs/adr/*.md` (excl. INDEX/README/TOMBSTONES)
   added as an eighth corpus surface. Verified by direct grep before the fix: `docs/adr` appeared
   **zero times** in the file. Two dated consequences already in this corpus: the 2026-08-15 /
   2026-08-24 regime-gate ADRs discharged the same F1 nine days apart with no dedup hit between
   them, and `2026-08-21-persona-hierarchy-review-panel.md` pasted this tool's `slugs found:
   (none)` output as its own §0 dedup evidence — a guaranteed false negative displayed as proof,
   since the tool structurally could not see a single ADR. Test `test_load_corpus_reads_all_eight_surfaces`
   updated (was `..._seven_surfaces`) with positive + negative (scaffolding-exclusion) coverage;
   `pytest tests/test_check_advisor_dedup.py` — 13 passed.

## §4 — Consolidations: 0 of 16 survived (the finding, not a null result)

Consolidation was the class most likely to look valuable going in. It went 0-for-16 against a
review instructed to refute by default. Three recurring reasons, useful for the next time a merge
looks obvious:

1. **Already litigated and ratified against.** Three of the six 2026-08-30 ADRs
   (`candidate-contract`, `channel-liveness-gate`, `evaluation-order`, `operator-approvals-campaign-envelope`,
   `terminal-taxonomy`, `tradeable-reachable-gate`) carry §3 Alternatives rows explicitly ruling
   out the exact merge proposed, with reasons, ratified the same day. Same for the third-leg pair
   (`2026-08-02-third-leg-liveness-limb.md` §3: "Fold it into S7. Rejected — S7 is a *prohibition*
   and L1 is a *preference*").
2. **Rule 14 makes a compliant merge word-neutral.** Ratified bodies stay byte-unedited, so a
   legal merge is verbatim concatenation, not a rewrite. The CC/Cursor-chain merge candidate would
   have saved ~120 header words out of 10,377 and produced one ADR at 4.6× the corpus median —
   a worse document, not a smaller one.
3. **Same subject ≠ same decision.** Coldstore Phase B explicitly says don't touch the
   authorization axis; Phase C deletes from the sizing axis. Merged, the result contradicts
   itself. `2026-07-14-cc-cursor-surface-allocation.md` rules what routes to Cursor;
   `2026-08-14-cc-cursor-autonomous-loop.md` rules whether a PR may merge unattended — different
   questions that happen to share two words in their title.

**Two families were found, verified, and are explicitly NOT recommended for merge** (the
restraint is deliberate, not an oversight):

- **dd-protection lock chain** (6 ADRs, 7,939 words) — genuinely one subject, two same-day
  siblings. But `core/dd_protection.py:206`, `ops/c1_rail/c1_sizing_host_reference.py:248`, and
  two test files all cite these files as anchors, and `2026-04-17-equity-tier-deletion.md` is a
  named Rule-0 read surface in CLAUDE.md. Total saving under 1,000 words — not worth repointing a
  live-safety anchor chain for.
- **`2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`** — textbook addendum shape, but has
  35 inbound references (more than its own parent ADR's 28). Repoint cost exceeds the 1,626-word
  saving.

## §5 — Simplification: verified and executed (updated same day, post-verification)

The 27 classification-pass proposals below went through their own adversarial (default-refute)
round before anything was edited, same posture as §1. **19 of 27 (70%) were refuted outright —
consistent with the ~76% verified-round refutation rate this note originally flagged as the
expected base rate.** 8 survived, in every case narrower than proposed; all 8 were then edited,
each re-verified post-edit for header-field and Decision/Falsifier/Gate/Forbidden-moves integrity.
**Net: 2,967 words cut across 8 files — not the 48,091-word headline the unverified pass
projected.** The gap between those two numbers is the point of running verification before
editing a decision corpus, not after.

Original ranked table, annotated with actual disposition:

| ADR | Words before | Words after | Disposition |
|---|---:|---:|---|
| `2026-07-31-orb-mnq-unpark-payability-target.md` | 7,088 | 6,718 | **APPLIED**, saved 370 |
| `2026-08-22-grow0-two-ledger-k-question.md` | 6,599 | 6,021 | **APPLIED**, saved 578 |
| `2026-07-10-strategies-never-locked-lifecycle-governance.md` | 6,748 | 6,748 | Refused — the proposal targeted the ADR's own §2 Decision section by name, a standing off-limits section; the "restated" text is this ADR's sole owner of the reasoning, not a duplicate |
| `2026-06-05-monorepo-layer-boundaries.md` | 4,830 | 4,743 | **APPLIED**, saved 87 |
| `2026-07-15-external-mechanism-harvest-intake.md` | 6,982 | 6,982 | Refused — the three "duplicate" §0 tables are independently anchor-cited reads for three different ratification events on three different dates; the falsifier blocks are the evidentiary chain for a §4 limb this pass may not touch |
| `2026-05-22-reality-check-harness.md` | 3,252 | 3,118 | **APPLIED**, saved 134 |
| `2026-08-19-loop-persona-hierarchy-review-panel.md` | 4,746 | 4,746 | Refused — 2 of the 4 "roster-churn" addenda are substantively unrelated governance rulings with no headcount content; the premise mischaracterized the file |
| `2026-07-22-challenge-era-substrate-retirement.md` | 4,625 | 4,625 | Refused — Read the full file (632 lines) and verified both named bloat sections against the repo |
| `2026-05-16-fxify-correct-timeout-semantic.md` | 3,521 | 2,757 | **APPLIED**, saved 764 |
| `2026-08-24-sourcing-phase-channel-retirement.md` | 4,911 | 4,911 | Refused — §10 alone is 781 words (largest section); the retirement rationale differs materially per channel, not a repeated boilerplate |
| `2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md` | 2,990 | 2,990 | Refused — the worked-example narrative is the only concrete illustration of the rule; no duplicate exists |
| `2026-05-28-audit-doc-generation-doctrine.md` | 2,522 | 1,886 | **APPLIED**, saved 636 |
| `2026-06-16-rule-2-budget-before-acting.md` | 4,958 | 4,958 | Refused — the narrative is the ratification rationale itself, not a restatement of the addendum |
| `2026-08-23-adr-decay-audit-skill-ratification.md` | 2,854 | 2,854 | Refused — the worked example is unique per section, not a repeated walkthrough |
| `2026-08-27-ssot-data-lineage-remediation-program.md` | 5,766 | 5,766 | Refused — the phase narrative is each addendum's own completion record, not duplicated elsewhere |
| `2026-08-22-ox-alpha-adversarial-lens-scope.md` | 4,994 | 4,994 | Refused — the 'Use N' addenda are each a dated, distinct measurement event, not repetitions of one caveat |
| `2026-08-21-persona-hierarchy-front-office-only.md` | 3,692 | 3,692 | Refused — the parent-rationale restatement is what makes this narrowing self-contained without a second read |
| `2026-08-15-notice-log-is-the-live-observation-routing-convention.md` | 2,589 | 2,589 | Refused — the proposal targets a section that does not exist in the file |
| `2026-06-30-state-md-role-reduction.md` | 2,403 | 2,403 | Refused — no before/after full-text STATE.md reproduction exists in this file to cut |
| `2026-08-29-clv-autocorrelation-admission-route-scope.md` | 4,492 | 4,492 | Refused — the named bloat section does not exist in this file |
| `2026-08-02-third-leg-liveness-limb.md` | 2,266 | 2,109 | **APPLIED**, saved 157 |
| `2026-08-03-orb-mnq-repark-payability-falsified.md` | 3,641 | 3,641 | Refused — the RESULTS numbers are the falsified verdict's own evidentiary support, not a restatement |
| `2026-08-21-cfo-subscription-ledger-consolidation.md` | 2,595 | 2,595 | Refused — the proposed bloat section does not exist in this file as described |
| `2026-08-09-survive-bound-is-the-queue-cap.md` | 901 | 901 | Refused — each addendum resolves a distinct queue-ordering event on a different date, not a repeated point |
| `2026-05-10-manifest-integrity-gate.md` | 982 | 741 | **APPLIED**, saved 241 |
| `2026-04-17-striker-v4.3-pyramid.md` | 635 | 635 | Refused — cited by `core/strategies/_archive/striker/striker_CHANGELOG.md`; flagged separately for a public-redaction question this pass does not decide (§7) |
| `2026-08-14-msl-explore-stage-5a.md` | 599 | 599 | Refused — the file is already light-tier (599 words); the proposed cut has no safe room to take from without touching Decision/Gate |
| | **102,181** | **99,214** | **8 applied (2,967 words saved) · 19 refused** |

Post-edit checks, all passing: `check_adr_graph.py` OK; header fields (`Status`/`Decision
date`/`Supersedes`/`Superseded-by`/`Superseded-in-part-by`/`Retain-until`/`Tier`) byte-identical
on all 8 edited files (grepped diffs directly, zero touched); no Decision/Falsifier/Gate/Forbidden-
moves heading removed on any file; `check_brief.py` shows the same MALFORMED verdicts pre- and
post-edit on the 3 files that carry them (`manifest-integrity-gate`, `fxify-correct-timeout-
semantic`, `reality-check-harness`) — confirmed against `git show HEAD:<path>` before editing:
these are pre-existing section-naming-convention gaps in older ADRs, not regressions from this
pass.

Common bloat patterns, in priority order of recoverable words:

- **(a) §0 has become a transcript.** 46,486 words, avg 352/file — worst offenders re-tell what a
  cited file says in prose where a six-row anchor table would do the same job. A uniform 50% trim
  of §0 + §3 alone recovers ~37,000 words — more than every consolidation family combined — and
  touches no decision text, no falsifier, no supersession edge.
- **(b) Measurement addenda accreting on decision records.** `2026-07-31-orb-mnq` (3 addenda,
  3,194w), `2026-08-22-ox-alpha-adversarial-lens-scope.md` (7 near-identical "Use N" addenda,
  1,597w implementing a counter the ADR itself says is untrustworthy), `2026-08-09-survive-bound-is-the-queue-cap.md`
  (3 addenda about STATE.md queue ordering on a light-tier ADR). Each names its own Rule 7 owner
  in its first line — the ADR should carry the verdict and a pointer, not the transcript.
- **(c) Implementation plans that outlive their execution.** 15,643 words across 101 files,
  nearly all DONE/MERGED. Some now assert the negation of the current tree —
  `2026-06-05-monorepo-layer-boundaries.md` hook #10 still prints "DUPLICATE or misplaced ECR
  engine" against a clean repo; `2026-05-10-manifest-integrity-gate.md`'s transcript references
  `data/` where the checker walks `core/data/`.

## §6 — Status hygiene: 11 verified fixes (cheap, none deletes anything)

| ADR | Fix |
|---|---|
| `2026-08-30-channel-liveness-gate.md` **and** `-candidate-contract.md` | Both declare §7 Phase 3 = add a STATE.md forward-board row; both read `Accepted`. **Zero of the six 08-30 stems appear in STATE.md** — verified directly, all six. Ten owed addenda have no tracked home. One shared row under the 2026-11-08 bucket discharges both. |
| `2026-08-21-stage2-stage3-progression-criteria.md` | Phase 1's logging obligation is dormant — `error_log.md` has one commit since seeding, against 43 `cursor/*` + 65 `claude/*` PR merges in that window. The ADR's own §10 hook (`wc -l` on the log) already proves this. Owed: dated addendum + operator ruling (re-arm / narrow / withdraw). Do not delete — it freezes the forbidden-surface list. |
| `2026-07-13-prop-account-book-segregation.md` | §4's 2026-08-08 check passed with no disposition recorded. An arithmetic reading exists (27.04% vs a 25% trigger) but sits in a `DRAFT — SUPERSEDED BY EVENTS` brief with deleted provenance. Add a verdict-free pointer addendum; the verdict itself is an operator call. |
| `2026-06-05-concept-admissibility.md` **and** `-sweep-engine.md` | Both self-declare "Graph edge OWED, not landed." Land `Superseded-in-part-by: 2026-07-11-gen1-pipeline-retirement.md` (machinery only), regenerate INDEX same commit. Do not edit the retirement ADR — one-sided in-part edges are already live convention here. |
| `2026-08-07-w4-minimal-gate-set-dormancy.md` | §2 asserts `universe_gate.py` "still defaults to the empirical estimator." It doesn't — flipped to `1/n` at `universe_gate.py:363-365`, recorded in the 2026-08-15 addendum. Three stale reader-intercept markers to fix. |
| `2026-08-07-w5-governance-diet.md` | Three sites still read "CI re-enable = owed" — discharged 2026-08-23, `gate-manifest.yml:45` runs it. One genuinely owed item (two `check_brief.py`) stays as-is. |
| `2026-08-07-w1-intraday-honest-engine-remeasure.md` | `core/firm_rules.py:336` still reads "W1 (Proposed)" — flipped to Accepted 2026-08-22. Needs `(Accepted 2026-08-22)`, not a bare swap. |
| `2026-07-10-r6-nogo-futures-residual-disposition.md` | §10's hook greps `ls ops/` for "crosstrade" and prints OK while `ops/c1_rail/crosstrade_payload.py` exists — fails open. Strike the hook; don't redirect it. |
| `2026-05-23-relocate-ecr-to-live-journal.md` | Owed retirement, blocked a month on a misread precondition (`--reason retired` needs no `--by`). Can run today. |
| `2026-08-13-msl-c3-k2-dual-axis-revive.md` | 6 dead `lab/analysis/c1/` links — bodies moved to `lab/archive/`. Repoint here + 2 closure files. Do not edit §Gate. |

## §7 — Disposition and what happens next

**Executed today (§3):** the retirement, the dedup-tool fix (+ tests), this note.

**Executed today, same session (§5):** the 27 simplify proposals went through their own
refute-by-default adversarial round before any edit — the same standard applied to §1's
DELETE/CONSOLIDATE/STATUS_FIX proposals, not a lighter one just because "simplify" sounds safer.
**19 of 27 (70%) refused**, consistent with §1's ~76% verified-round refutation rate; the 8
that survived were narrowed by verification (none applied as originally proposed) and edited,
each re-checked post-edit for header-field and Decision/Falsifier/Gate/Forbidden-moves integrity.
Net: 2,967 words cut, not the 48,091-word unverified projection. This is the intended outcome of
running verification before editing, not a shortfall — see §5 for the full per-file table and
§9 for why that gap is the finding, not a failure.

**Not executed today:** the §6 status-hygiene table (11 items) — none were subtractive edits to
ratified ADR bodies, so the risk profile differs from §5, but they were not run through the same
adversarial pass this session and should not be treated as pre-verified. Same standard applies
before executing any of them.

**Separately flagged, not actioned by this note:** `2026-03-01-aegis-session-selection.md`'s
retired body (now `docs/ltm/adr/`) still publishes locked-book backtest figures (Net ~$62K, PF
2.28, WR 59.9%, Max DD 3.46%) that the 2026-08-14 public-visibility redaction pass should have
caught if `docs/adr/` (or its `ltm` destination) was in that pass's scope. This note does not
redact it — that is a public-redaction-policy call, not a corpus-hygiene one, and belongs with the
operator. `2026-04-17-guardian-v5.1-architecture.md` and `2026-04-17-striker-v4.3-pyramid.md`
carry the same class of exposure and are both due for A5 retirement-consideration on 2026-10-17 —
redact before touching, not after.

## §8 — Process change (grounded, not proposed as new doctrine)

The ceremony-tiering ADR is not failing — of the 64 ADRs dated 2026-08-08 or later, 16 are
`Tier: light` = 25%, above its own ≥⅕ falsifier target, and 69 of 172 ADRs corpus-wide already use
amend-in-place addenda. **But 29 of those 64 (45%) carry no `Tier:` field at all** — the falsifier
is being evaluated over a population that silently excludes every ADR that skipped the test.

Three fixes, in priority order (recorded here as findings; not self-authorizing new doctrine —
Rule 14/§Restraint below applies):

1. **`check_advisor_dedup.py` blindness — fixed this session (§3.2).** Highest-leverage single
   change; it was upstream of at least two dated incidents already in this corpus.
2. Make `Tier:` mandatory in the header parse, and require a full-tier ADR naming "creates
   standing doctrine" (ceremony-tiering limb 4) to name *which* rule — 12 of 19 declared-`full`
   ADRs use exactly this formula, including two 2026-08-20 override ADRs whose own §5 says "this
   is a single named exception, **not** a doctrine change."
3. Amend the change-control clauses that force minting over amending — e.g.
   `docs/spec/2026-07-27-third-leg-target-spec.md`'s "§7 thresholds change only by a superseding
   ADR or the §6.1 verdict firing" converted two spec amendments into 5,175 words of full-tier ADR.
   The 2026-08-29 amend-over-mint operator preference cannot take effect while clauses like this
   stand; they'd need to admit "a superseding ADR **or** a dated addendum on the owning limb
   register."

**Also found, not actioned:** `check_a2` in `check_adr_graph.py` only validates edges declared by
the *successor* side. A `Superseded-by` on a target with no reciprocal `Supersedes` is never
examined, and `FIELD_RE` takes only the first filename in a multi-target field. `check_adr_graph.py`
returns OK today, yet `2026-08-15-regime-gate-scope-ratification.md` points at
`2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md`, which declares `Supersedes:
nothing`. **A green `adr-graph` run is not evidence the supersession graph is sound** — worth a
future `A9` check. Not implemented here; outside this note's scope.

## §9 — Restraint

Per `feedback_visible_restraint_in_closing_brief`: no new gate, rule, or ADR is proposed by this
note itself — §8's three items are findings for an operator decision, not self-executing changes.
Deliberately **not** recommended: a fourth delete-classifier pass (three strikes is enough
evidence); all 16 consolidation families, several of which looked obviously right at first glance
(the 08-30 six, the CC/Cursor chain, both coldstore phase pairs, the two 2026-08-20 ICT overrides);
a doc-budget gate (operator already declined one on 2026-08-14; the A5 age-clock is the better,
evidence-based instrument and nothing here changes that); retro-converting any full ADR to light
(named forbidden move in the ceremony-tiering ADR, and would game its own falsifier by shrinking
the denominator); redacting the aegis-session backtest figures without an operator ruling on scope
(§7); executing the §5/§6 lists as an unverified batch (§5 was verified before execution — 19 of
27 proposals were withdrawn at that step rather than applied on the strength of the classification
pass alone; §6 stays unverified and unexecuted for the same reason).

## Verification

```bash
# Corpus census (re-run against current HEAD)
ls docs/adr/*.md | grep -v -E 'INDEX.md|README.md|TOMBSTONES.md' | wc -l   # 172 at audit time

# A5 fires tomorrow — confirmed directly this session
python scripts/check_adr_graph.py --today 2026-09-01

# dedup-tool blindness, before the fix (re-run against docs/adr on a pre-fix checkout to reproduce)
grep -c "docs/adr" scripts/check_advisor_dedup.py     # was 0, now >0

# retirement executed this session
git log --oneline -1 -- docs/ltm/adr/2026-03-01-aegis-session-selection.md
cat docs/adr/2026-03-01-aegis-session-selection.md    # stub + disposition banner

# dedup test coverage
python -m pytest tests/test_check_advisor_dedup.py -q  # 13 passed
```
