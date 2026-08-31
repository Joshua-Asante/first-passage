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

## §5 — Simplification: the actual money (NOT yet adversarially verified — see §7 disposition)

27 ADRs, 102,181 words today, ranked by proposed savings (not yet executed — see §7 for what
happens next):

| # | ADR | Now | Proposed after | Saved |
|---|---|---:|---:|---:|
| 1 | `2026-07-31-orb-mnq-unpark-payability-target.md` | 7,088 | 1,800 | 5,288 |
| 2 | `2026-08-22-grow0-two-ledger-k-question.md` | 6,599 | 2,000 | 4,599 |
| 3 | `2026-07-10-strategies-never-locked-lifecycle-governance.md` | 6,748 | 3,000 | 3,748 |
| 4 | `2026-06-05-monorepo-layer-boundaries.md` | 4,830 | 1,800 | 3,030 |
| 5 | `2026-07-15-external-mechanism-harvest-intake.md` | 6,982 | 4,800 | 2,182 |
| 6 | `2026-05-22-reality-check-harness.md` | 3,252 | 1,100 | 2,152 |
| 7 | `2026-08-19-loop-persona-hierarchy-review-panel.md` | 4,746 | 2,600 | 2,146 |
| 8 | `2026-07-22-challenge-era-substrate-retirement.md` | 4,625 | 2,600 | 2,025 |
| 9 | `2026-05-16-fxify-correct-timeout-semantic.md` | 3,521 | 1,750 | 1,771 |
| 10 | `2026-08-24-sourcing-phase-channel-retirement.md` | 4,911 | 3,200 | 1,711 |
| 11–27 | (17 more files) | 40,999 | 29,440 | 11,559 |
| | **Total** | **102,181** | **54,090** | **48,091 (11% of corpus)** |

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

**Not executed today, explicitly deferred pending adversarial verification:** the §5 simplify
list and the §6 status-hygiene table. Both were produced by the classification pass only — they
did not go through the refute-by-default adversarial round that killed 76% of the verified
proposals in §1. Executing 27 subtractive edits to governance/decision records on a single
classification pass, on a corpus where the last two unverified passes were wrong 96–100% of the
time, is not a defensible standard even under an operator "go ahead" — the verification step is
what makes "go ahead" safe to act on rather than a blind batch apply. Planned: adversarial
verification per file (does the cut ADR still carry Decision/Falsifier/Gate/Forbidden-moves
intact; does Rule 14 permit a subtractive edit here; does anything else cite the section being
cut), execute only what survives, and report per-file outcome (fixed / skipped / no-change-needed).

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
(§7); executing the §5/§6 lists as an unverified batch.

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
