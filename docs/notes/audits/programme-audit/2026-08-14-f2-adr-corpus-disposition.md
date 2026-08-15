# F-2 disposition — full ADR-corpus classification + adversarial deletion test

**Audit ID:** AUDIT-2026-08-14-F2-ADR-DISPOSITION
**Date:** 2026-08-14 · **Trigger:** Great Prune ADR falsifier F-2 (ADR-count re-accretion), fired; operator direction to work through its disposition with an explicit "aggressively delete ADRs that are superseded, stale, or overly constricting" instinct.
**Authors:** Joshua (direction + rulings) + Claude Code.
**Method:** two sequential multi-agent workflows against the full live ADR corpus (126 files, `docs/adr/*.md` minus `INDEX.md`), at `origin/main`-tracking worktree state 2026-08-14. Phase 1: 10 parallel classification agents, each reading a batch of 11-15 ADRs in full (not grep-only) against the standing retention test (`docs/operational_rules.md` Rule 16), instructed to default to the safer disposition whenever uncertain. Phase 2: 8 adversarial agents (2 independent verifiers per candidate) instructed to *refute* each Phase-1 deletion candidate using the retention test's own mandated 4-part classification instrument (Rule 16) — quoted-path scan, pathlib-join scan, inbound-reference scan beyond markdown links, header-reciprocity check.

---

## §1 — Result

| Phase-1 disposition | Count | % of corpus |
|---|---:|---:|
| KEEP_SAFETY_CRITICAL | 38 | 30% |
| KEEP_LIVE | 54 | 43% |
| KEEP_HISTORICAL_RECORD | 24 | 19% |
| PARTIAL_EDIT_CANDIDATE | 6 | 5% |
| TOMBSTONE_CANDIDATE | 4 | 3% |

**Phase 2 (adversarial verification of the 4 tombstone candidates): 0 of 4 survived. 8 of 8 verdicts returned `still_needed: true`.**

| Candidate | Why it was rescued |
|---|---|
| `2026-05-18-pine-input-float-defaults-realignment.md` | Cited by its sibling `2026-05-18-relock-to-test-values.md` (Status: Accepted, live per `INDEX.md`'s "Partially superseded" bucket) via an informal `**Supersedes (same day):**` header field + live markdown link. `scripts/check_adr_graph.py`'s `FIELD_RE` only recognizes the canonical `Supersedes:` field, so the mechanical gate would not catch the orphaned link this deletion would create. |
| `2026-05-18-relock-to-test-values.md` | Reciprocal of the above — cited back by the same sibling. Also: `check_adr_graph.py` gate A4 requires this Accepted-status file stay full-body; plain deletion bypasses the repo's own sanctioned cold-storage retirement path (Status → cold token + `docs/ltm/adr/` stub), which its own cited successor went through correctly. |
| `2026-05-23-relocate-ecr-to-live-journal.md` | Cited in backticked prose (no markdown link) by `docs/spec/2026-05-23-trade-capture-skill-design.md:27`, a spec a *separate* 2026-08-05 claim-alignment audit already flagged as needing its own retirement banner — still unexecuted 9 days later. Its own designated retirement mechanism (`scripts/retire_adr.py`) was also never run against it. |
| `2026-05-28-audit-doc-generation-doctrine.md` | The only surviving spec for a lock-completion-checklist pattern `docs/operational_rules.md` Rule 5 still references ("operational tooling integrated" item), relevant to any future strategy admission — this worktree's own name is `strategy-candidate-discovery`. Tellingly, the Great Prune itself deleted this ADR's *deliverables* (`docs/audits/*.md`) on 2026-08-08 but deliberately left the ADR intact — the repo's own retention instrument already ruled on this exact question once. |

One process note: during adversarial testing, one verifier moved the real working-tree file aside and back to simulate deletion rather than using a scratch copy; a parallel sibling agent observed the transient state mid-flight. `git status` confirmed the tree settled clean with no lasting effect. A correctly-run sibling verdict used a scratch-directory copy instead — future workflow prompts asking agents to "empirically simulate a deletion" should say so explicitly.

---

## §2 — What this means for F-2

**Great Prune §4 F-2** fired on regrowth: ADR count +14 (~400% of the 50%-of-pruned-delta trigger), file count +412 (~131%), bytes +2.90 MB (~63%, short). Measured at `origin/main` `df2c448`, 2026-08-14, 6 of the 91 days to the 2026-11-08 audit window. F-2's prescribed action, as written: *"escalate to a doc-budget gate (hard, counted, in `gates.yml`)."*

This audit tested the premise underneath that prescription — that regrowth indicates the prune "treated symptom not cause," i.e., that dead/ceremonial material is re-accumulating. **The premise does not hold.** A rigorous, adversarially-checked pass over the entire live corpus found:

- 3.2% of the corpus (4 files) looked deletable on content grounds after a full read against the retention test.
- 0% actually were, once checked against the instrument the retention test itself mandates (Rule 16).
- 92% classified KEEP on the first pass, much of it for reasons a keyword/date-based heuristic would miss entirely (informal supersession fields, prose citations without markdown links, doctrine surviving its own implementation's retirement).

The corpus is not accumulating junk. **The re-accretion the falsifier measured is very likely genuine decision throughput** — this operation keeps making real, load-bearing calls (dd_protection changes, prop-portfolio program decisions, MSL sourcing rulings, closure dispositions), and each one correctly earns an ADR under this repo's own doctrine-minting discipline. A doc-budget gate counting ADRs would not distinguish that from real bloat; it would just make the next necessary decision more expensive to record.

**A relevant data point the same window produced:** `docs/adr/2026-08-12-closure-disposition-coverage-hard.md` self-armed a new HARD, commit-blocking gate four days *after* F-2's trigger window opened — the only file in the full 126-ADR corpus that installs repo-wide commit-blocking enforcement for what is fundamentally a documentation-bookkeeping concern (unclosed terminal-verdict claims). This is exactly the class of decision F-2's literal prescription would encourage more of. It is not this audit's place to rule on whether that specific gate was warranted — flagged in §4 below as an open item for the operator.

---

## §3 — The 6 partial-edit candidates (RESOLVED same session — kept as the analytical record)

All 6 were dispatched as chips and merged into `origin/main` before this note landed on `main` — read this table as history of what was found, not as owed work.

| ADR | What was needed | Resolved by |
|---|---|---|
| `2026-05-22-reality-check-harness.md` | Component A (OANDA data loader) is dead; Components B-H (bootstrap/Davison-Hinkley methodology) are feed-agnostic and still cited. Dormancy note on Component A only. | PR #827 |
| `2026-06-04-lean-portfolio-meta-layer.md` | Already identified in the earlier backlog-ratification pass this session (DOC-4) — chip already spawned. | PR #824 |
| `2026-06-05-sweep-engine.md` | Machinery retired by `2026-07-11-gen1-pipeline-retirement.md`, but its core invariant (Python never gates deployment; same feed for pre-filter and confirm) is still cited as live doctrine by `2026-06-23-tv-backtest-egress-automation.md`. Needed a "machinery retired, doctrine survives" banner matching the one `2026-06-05-concept-admissibility.md` (its sibling) already received. | PR #827 |
| `2026-07-20-stage8-variance-dominance-risk-neff-gate.md` | Header already carried a `Superseded-in-part-by` pointer with dormancy language — confirmed adequate, no further edit needed. | N/A — already correct |
| `2026-07-29-third-leg-symbol-occupancy-limb.md` | Core S7 decision (order-symbol occupancy) stays live, but its 2026-08-06 addendum's "MYM1!/MNQ1! retained-not-released pending F2" claim was overtaken by the later `2026-08-12-msl-mym-occupancy-release.md`. Needed a reconciling addendum, not a rewrite of S7 itself. | PR #827 |
| `2026-08-05-strategy-venue-binding-axis.md` | Never ratified (Status: Proposed); its own T1 falsifier appears to have fired when F2/F3 were resolved by `2026-08-07-loop-s1-environment-ratification.md` without producing an edition-state transition. Needed a status-correction/dormancy addendum. | PR #827 (also later touched by PR #833's public-visibility scrubbing pass — unrelated content, no conflict) |

## §4 — 6 "overly constricting" flags (orthogonal to deletion — where the real ceremony-weight lives)

| ADR | Disposition | Concern |
|---|---|---|
| `2026-04-24-mvd-discipline.md` | KEEP_SAFETY_CRITICAL | Mandates a blocking MVD-attest line on every artifact citing a number, forever. Its doc-audit-table half was already quietly dropped by the retrofit ADR — the doc still describes the heavier original ceremony, not what actually survives in practice. |
| `2026-05-16-fixture-test-requirement.md` | KEEP_LIVE | Mandatory gate; its only automated enforcement was deleted as unworkable (all-false-positive), so it now rests entirely on manual diligence. Falsifier target 2026-11-16, not yet due — flag for awareness, no action owed yet. |
| `2026-05-28-audit-doc-generation-doctrine.md` | TOMBSTONE_CANDIDATE (rescued) | ~45-90 min manual audit mandated per strategy lock, no automated backstop. Cost is conditional (only recurs if a 5th strategy is ever locked), not a recurring tax — correctly scoped as-is, no action needed. |
| `2026-06-04-lean-portfolio-meta-layer.md` | PARTIAL_EDIT_CANDIDATE | Subsumed by the dormancy-addendum fix already chipped. |
| `2026-06-16-rule-2-budget-before-acting.md` | KEEP_LIVE | Checked directly (`docs/notes/audits/rule-2-trip-log.md`): **not actually starved** — one legitimate baseline row exists; the 2026-08-08 audit-cycle check was simply skipped once, and the file already self-documents this as "a single-cycle miss, not a pattern" with the falsifier clock explicitly deferred to the 2026-11-08 gate. No action needed. |
| `2026-08-12-closure-disposition-coverage-hard.md` | KEEP_LIVE | The one file in the corpus that self-armed a new HARD/commit-blocking gate, landing 4 days into F-2's own trigger window. See §2 — flagged for an explicit operator ruling, not a mechanical fix. |

---

## §5 — Disposition

**F-2 is closed as: fired-on-a-miscalibrated-premise, not degenerating.** The mechanical trigger (ADR/file-count regrowth) is accurate as measured; the inference it was built to support (regrowth ⇒ dead-material accumulation ⇒ escalate to a hard gate) is refuted by this audit's direct content test. Recorded as an addendum to `docs/adr/2026-08-08-great-prune.md` §4 (Rule 14 — frozen ADR, addendum not in-place edit) rather than here; this note is the evidence base, not the ruling.

**Recommended, not executed here:**
1. Do not add a new hard doc-budget gate. The evidence points the opposite direction from what F-2's literal text prescribes.
2. Replace the count-based F-2 instrument with a periodic content-sample check (a smaller version of this audit — read N random live ADRs against Rule 16 each cycle) as the actual falsifier for "is the corpus accumulating dead weight," at the next programme-audit cadence.
3. ~~Execute the 6 partial-edit addenda (§3)~~ — done; all 6 merged same-session (see §3's "Resolved by" column).
4. Operator ruling owed on `closure-disposition-coverage-hard.md` (§4) — was a new hard gate the right call four days into a regrowth-degeneration warning window, or should it be softened to warn-tier pending the 2026-11-08 re-audit?

## §6 — Restraint

Per `feedback_visible_restraint_in_closing_brief`: no new rule, gate, or ADR is proposed by this note itself (recommendation 2 above names a *replacement* instrument for F-2, not an addition). No `dd_protection`, `firm_rules`, Pine, allocation, or c1-rail content was touched — all 38 KEEP_SAFETY_CRITICAL ADRs were read, none edited. No deletion was executed — the 4 tombstone candidates were rescued, not force-deleted despite the operator's stated aggressive-delete instinct; that instinct was tested in good faith and the corpus held up under scrutiny.

---

## Verification

```bash
# F-2 measurement inputs (re-run against current HEAD)
ls docs/adr/*.md | grep -v INDEX.md | wc -l                    # ADR count at audit time: 126 (+ INDEX.md = 127 ls total)
git log --oneline --since=2026-08-08 -- docs/adr | wc -l       # churn since the prune

# Rescue evidence spot-check (either sibling)
sed -n '1,12p' docs/adr/2026-05-18-relock-to-test-values.md    # informal Supersedes (same day) field, uncaught by check_adr_graph.py

# Trip-log finding
cat docs/notes/audits/rule-2-trip-log.md                       # 1 baseline row; falsifier deferred to 2026-11-08 by its own text
```
