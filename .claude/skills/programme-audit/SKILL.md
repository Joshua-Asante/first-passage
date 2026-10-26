---
name: programme-audit
description: Use when a methodology or 4-strategy portfolio shows degeneration signals — belt-patches without independent corroboration, belt that only grows never prunes, falsifier thresholds drifting toward "we'd never hit this", methodology invoked to rationalize a decision already made, SNAG pattern (multiple null/ambiguous loops same domain), cross-layer contamination (methodology citing portfolio evidence or vice versa), or a negative heuristic crossed without repair. Also fires on scheduled cadence — quarterly for meta-layer methodologies (The Algorithm, INQHIORI, OODA, brief-authoring), semi-annual or triggered for the portfolio. Loads the Programme Audit Protocol — seven diagnostic questions, five disposition verdicts (Progressive / Stable / Degenerating / Falsified / Ambiguous), two-layer architecture rules. Also runs the per-ADR decay sweep (merged from adr-decay-audit 2026-10-24): "which ADRs still hold", "has anything decayed", before a repo-public snapshot or major handoff, or alongside the quarterly cadence — a four-way verdict per Accepted ADR (STILL_APPLICABLE / DECAYED_DOCUMENTED / DECAYED_UNDOCUMENTED / UNCERTAIN) via batch scan then adversarial verify. Hand off to inqhiori for follow-up falsifiable-H investigations, brief-authoring for audit artifact structure, c1-rail for live-ops facts, prop-firm-challenge for firm rules and dd_protection.
---

# Programme Audit Protocol

This skill applies the Lakatos research-programmes diagnostic to Joshua's methodologies (meta layer) and the 4-strategy portfolio (object layer). It exists because methodologies and portfolios can degenerate silently — accumulating belt-patches without independent corroboration, drifting falsifier thresholds, or substituting layer evidence — and the cost of catching degeneration late is high. The first proof-of-value (2026-05-12) was the audit producing surplus content: the strategy-vs-instrument correlation finding surfaced as a byproduct of routine portfolio audit, falsifying an implicit belt assumption. That session is the canonical worked example.

**Source-of-truth hierarchy:** this SKILL.md body (discipline rules) → audit artifacts in `docs/notes/audits/programme-audit/` (lineage). When this skill disagrees with a more recent audit that demonstrably worked, the audit wins and the skill needs updating — flag this. (A canonical programme-audit ADR tier was contemplated and never authored; the clause was struck 2026-10-15 under claim-alignment row A12 rather than re-numbered — `ADR-NNN` numbering itself was dropped 2026-07-17.)

**Boundary with sibling skills** (beyond the frontmatter hand-offs): OODA is not relevant
to programme audits except as a methodology being audited; `pinescript-v6`-owned strategy code is
the *object* of portfolio-layer audits, never modified by the audit itself.

---

## Trigger conditions (degeneration signals primary; cadence secondary)

The skill fires **immediately** on any of the following degeneration signals — calendar cadence is a backstop, not the primary trigger:

1. **Belt-patches without independent corroboration.** A parameter, filter, gate, or constant was changed to accommodate an observation, but no independent evidence (separate data, separate test, separate mechanism) supports the change. The Q-DDP-1 → ADR override is the canonical edge case worth re-examining each audit.
2. **Belt that only grows, never prunes.** Adds outpace removes across consecutive audit windows. Healthy programmes prune as evidence converges.
3. **Falsifier thresholds drifting toward "we'd never hit this anyway."** Either explicit threshold revisions or implicit reinterpretation that softens triggers.
4. **Methodology invoked to rationalize a decision already made.** The audit was authored to justify a conclusion, not to test it. Tell: the disposition is written before the evidence is assembled.
5. **SNAG pattern.** Multiple null/ambiguous loops in the same domain — DJ30 Q-DJ30-1/2/3 (all null/ambiguous/null) is the canonical anchor. SNAG budget exhaustion is the right response, not infinite-patching.
6. **Cross-layer contamination.** Methodology audit verdicts cite portfolio performance as evidence, or vice versa. The two layers corroborate each other in the long run; they do not substitute in any given cycle.
7. **Negative heuristic crossed without repair.** A forbidden move appears in recent work and is tolerated rather than removed.

**Scheduled cadence (backstop):**

- **Methodologies:** quarterly. Cheap audits (no live data dependency); rhythm matters more than depth.
- **Portfolio:** semi-annual baseline, triggered between cycles on degeneration signals or on accumulation of ≥6mo new live data. Portfolio audits are expensive (require re-MC, edge-captured analysis); calendar-forced audits without new evidence are ceremony.

---

## Two-layer architecture (load-bearing)

The most important structural rule. Methodologies and the portfolio are *nested* research programmes, not the same programme:

- **Meta layer (methodologies):** The Algorithm, INQHIORI, OODA, brief-authoring, programme-audit itself. Hard cores are *epistemic moves*. They generate decisions.
- **Object layer (portfolio):** the 4-strategy locked portfolio, allocations, dd_protection, firm deployments. Hard core is *empirical claims about market behavior and operational capacity*. It is the *output* of methodology layer.

**Coupling rules:**

1. Methodology verdicts do not automatically promote to portfolio verdicts. INQHIORI being progressive does not mean Aegis is progressive. They are judged on their own evidence.
2. Portfolio verdicts can trigger methodology audits but not the reverse. A failing portfolio is evidence about the methodology that built it; a thriving methodology is not evidence the portfolio still holds.
3. Cross-layer contamination is itself a degeneration signal (see trigger #6 above).

**Operational consequence:** when authoring a portfolio audit, do not reference methodology audit verdicts. When authoring a methodology audit, do not cite portfolio performance. Each audit stands on its own evidence base. If a future cross-layer synthesis is wanted, it is a separate document with its own discipline.

---

## The seven diagnostic questions

Every audit, regardless of layer, runs these seven questions. The phrasing differs slightly between layers (meta-layer asks about epistemic moves; object-layer asks about empirical claims) but the structure is identical.

**1. Hard core integrity.** Has the hard core been preserved across recent uses, or quietly violated under the programme's name?

- Meta example: running INQHIORI without a falsifiable H, then calling the output an INQHIORI finding.
- Object example: a locked strategy modified outside the formal version-lock cycle; dd_protection overridden tactically without ADR.

**2. Belt churn balance.** How many belt items added vs. removed since the last audit? Healthy programmes prune as evidence converges. Belts that only grow accumulate ceremony.

- Tally adds and removes. Net-positive growth across consecutive audits is a yellow flag; net-positive growth across ≥3 consecutive audits is a red flag.

**3. Progressive evidence.** Has the programme produced predicted-and-corroborated results in the audit window? Concrete examples required — predictions made *before* outcomes, then confirmed.

- Meta example: Aegis short-mirror falsification (INQHIORI predicted asymmetry, tested, confirmed).
- Object example: live PF within MC band; dd_protection firing correctly on the right regime; a tail event survived as projected.

**4. Degeneration evidence.** Has the programme been used to patch anomalies after the fact without independent support? Belt-patches existing only to rescue prior conclusions are the canonical signal.

- The diagnostic: when belt items were last revised, was the revision *predicted* by an independent model, or *rationalized* after the fact?

**5. Boundary respected.** Have moves the negative heuristic forbids appeared in recent work? If so, was the boundary repaired (move removed, lesson captured) or eroded (move tolerated, becoming new normal)?

- Meta example: a methodology used for a decision its negative heuristic forbids (INQHIORI on tactical, OODA on structural).
- Object example: a regime overlay built on physical facts; a rejected candidate quietly re-proposed without new mechanism evidence.

**6. Theory-comparison performance.** Where competing options existed, did the chosen option outperform the unchosen ones in subsequent evidence? Track the counterfactuals.

- Meta example: when the tiebreaker routed a question to INQHIORI vs OODA, did the chosen routing produce the better outcome?
- Object example: when allocation A was chosen over B, did A outperform B in subsequent live evidence?

**7. Falsifier check.** Are the programme's pre-committed falsifiers still in force at their original thresholds? Have any drifted toward "we'd never hit this anyway"?

- Verify by grep / diff against original locked values. Drift is mechanical to detect and disqualifying when found.

---

## Five disposition verdicts

Each audit cycle ends with one verdict per programme:

- **Progressive** — earning its existence; predictions corroborated; continue.
- **Stable** — delivering value but not generating new insight in the audit window; continue with watch flag, re-examine cadence.
- **Degenerating** — belt-patches without independent corroboration, or net-positive belt growth across consecutive audits, or methodology being used to rationalize. Intervene: prune belt, refactor procedures, or escalate to replacement.
- **Falsified** — pre-committed falsifier triggered or hard-core proposition failed. Abandon or fundamentally restructure the programme.
- **Ambiguous** — insufficient data for a verdict. Document explicitly and re-test at next cycle. AMBIGUOUS is not "we'll wait longer" — it is a verdict, dated, with re-test conditions named.

---

## Audit artifact structure (handoff to brief-authoring)

Programme audits produce an audit note in `docs/notes/audits/programme-audit/YYYY-MM-DD-<layer>-audit.md`. The artifact follows `references/audit_note.md` from brief-authoring with these audit-specific additions:

- §1 Context lists the programme being audited, the audit window (start date, end date), and the trigger (scheduled cadence vs specific degeneration signal).
- §3 (audit-specific) contains the seven diagnostic questions, each with a specific answer grounded in evidence anchors (commit hashes, file paths, specific numbers).
- §4 contains the disposition verdict with explicit reasoning.
- §5 lists any spawned follow-ups (INQHIORI loops opened, belt-prune ADRs queued, falsifier checks needed).
- §10 audit hooks runnable at the next cycle.

---

## Known traps

Failure modes that recur, in order of frequency:

**1. Audit authored to confirm a verdict already held.** The audit reads as justification for "we're doing fine" or "we need to change X" — predetermined. Repair: separate the evidence assembly from the verdict assignment. Write §3 (seven questions, with evidence) before writing §4 (verdict). If the verdict was decided before evidence, the audit is theater.

**2. Cross-layer leakage.** Methodology audit cites portfolio P&L. Portfolio audit cites methodology rigor. Repair: re-author with layer discipline enforced — no cross-layer citations.

**3. AMBIGUOUS used as "we don't want to decide."** AMBIGUOUS is a verdict requiring named re-test conditions. "We'll know more later" is not AMBIGUOUS — it is no verdict at all. Repair: name the specific evidence that would resolve the ambiguity and the date by which it should be available.

**4. Belt-churn metrics absent.** The audit notes "we made some changes" without counting adds and removes. Repair: explicit tally. The number matters because trend across audits matters.

**5. Falsifier check skipped.** Audit references that falsifiers exist without verifying current threshold values match locked values. Repair: grep / diff against the locked ADR; report the diff.

**6. Audit cadence ceremony.** Quarterly audit run on schedule when no new evidence has accumulated; produces "stable, no changes" with no real examination. Repair: collapse to a one-line status update; reserve full audit for cycles where new evidence or degeneration signals exist.

**7. Audit triggered by degeneration signal but spawned no follow-up action.** Degeneration was identified, recorded, and then nothing changed. Repair: every Degenerating verdict requires at least one named action (belt-prune ADR, INQHIORI loop, restructure proposal) with an owner and date.

---

## Discipline check summary

Run before declaring an audit complete:

```
[ ] Seven diagnostic questions answered, each with evidence anchor
[ ] Belt churn balance counted (adds vs removes, numbers explicit)
[ ] Falsifier check executed (grep / diff against locked thresholds)
[ ] STRATEGIC-Delete declarations checked; add-back rate computed from kill records and registry entries
[ ] Cross-layer contamination check passed (no cross-citations)
[ ] Disposition verdict assigned (one of five), with reasoning
[ ] If Degenerating or Falsified, follow-up actions named with owner and date
[ ] If Ambiguous, re-test conditions and target date named
[ ] §10 audit hooks runnable at next cycle
```

---

## Worked example (canonical anchor)

**2026-05-12 portfolio audit, applying the seven diagnostic questions to the 4-strategy portfolio.** Audit produced surplus content as a byproduct: question 1 (hard core integrity) led to examining whether the implicit "instrument correlation ≈ strategy correlation" assumption had been preserved. Direct evidence from the existing locked portfolio (DJ30 / NAS strategy-level correlation materially lower than instrument-level correlation would predict) was inconsistent with the assumption. This was not predicted by the audit; it surfaced as a consequence of asking the question rigorously.

Outcome: belt-level falsification of an implicit assumption; Notice log captured; Pre-Q Q-CORR-1.1 (Guardian-on-Silver) opened to test the corrected belt. The audit also produced ADR-NNN (prop-firm-capital falsifiers) as a parallel artifact — the methodology was visibly producing belt-level findings and falsifier infrastructure in a single session.

This single example demonstrates the value of the protocol better than any pre-authored justification could. Treat it as the canonical anchor — replicate the discipline, not the specific finding.

---

## ADR decay sweep — per-decision applicability

Merged 2026-10-24 from the retired `adr-decay-audit` skill ([tombstone](../../../docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation)). The programme audit above judges programmes as wholes; this sweep visits each Accepted ADR.

ADRs are the canonical record of every decision in this repo. Canonical-but-wrong is worse than
absent, because it is trusted by default. This sweep exists because **no other mechanism
periodically re-checks the whole Accepted-ADR corpus for continued applicability**:

- **Skew audit** (`docs/operational_rules.md` §6, `.claude/commands/skew-audit.md`) fires
  only on a strategy version-lock event and checks a narrow target set (`AGENTS.md`, ADR `Code:`
  pointers, methodology docs) inside a bounded commit window.
- **The programme audit above** runs a Lakatos diagnostic on *programmes* (methodologies as a whole, the
  strategy portfolio as a whole) on a quarterly/semi-annual cadence — it does not visit individual
  ADRs one by one.
- **blast-radius** is reactive: it fires after a specific edit, to catch other docs that might
  still restate what was just changed. It does not sweep ADRs that no recent edit touched.

The gap this leaves: an ADR whose header still says `Accepted`, but whose factual claim has been
overtaken by a *later* ADR that never links back to it, sits in the corpus indefinitely unless
someone happens to reread it. The canonical worked example (first full-corpus run, this sweep's
origin) found this exact pattern twice in one pass out of roughly 150 Accepted ADRs — both cases
were a later ADR changing a number/architecture claim without any cross-reference added to the
earlier ADR that still asserted the old value as current.

**Boundary with the programme audit above:** don't conflate a
clean per-ADR sweep with a healthy programme, or vice versa — an ADR corpus can be 95%
still-applicable while the programme it belongs to is Degenerating, and the reverse
(the programme audit above). Run `blast-radius` immediately after any edit touching an ADR's subject
matter; run *this* sweep on a cadence or before a high-stakes moment, independent of whether
anything was just edited. `brief-authoring` provides the audit-note artifact template this
sweep's output should follow.

---

### Trigger conditions

**Cadence (backstop):** piggyback on the programme audit's quarterly meta-layer cadence — run this
alongside it, not on a separate clock. Do not add a second standing calendar trigger; two
independent audit clocks drift out of sync and one silently stops being followed.

**Event triggers (primary):**

1. Before any repo-public snapshot, external handoff, or new-session onboarding that will treat
   the ADR corpus as ground truth.
2. When the corpus has grown by a large batch since the last full sweep (e.g. a fast multi-week
   stretch that added dozens of new Accepted ADRs) — new volume raises the odds an earlier ADR
   quietly went stale in the interim.
3. On direct operator request ("which ADRs still hold", "has anything decayed").
4. When a single ADR's own pre-registered falsifier/expiry condition is discovered to have fired
   without a discharge addendum — that is itself one confirmed hit; treat it as a signal to run
   the full sweep rather than patching the one file in isolation, since if one decision rotted
   silently, siblings from the same era plausibly did too.

---

### Method: two-phase scan → verify

Do not attempt this file-by-file in a single pass for a corpus of any real size — a flat read-all
approach either shallow-reads everything or exhausts context before finishing. Use a fan-out
workflow:

**Phase 1 — Scan.** Batch the Accepted-ADR list per the scale guidance above and run one independent scan pass per
batch. For each ADR, check:

1. **Top-of-file blockquote override.** Many ADRs in mature corpora accumulate a later-dated
   addendum prepended above the original decision text (a "DISCHARGE ADDENDUM", "WITHDRAWN",
   "CEREMONIAL", "SUPERSEDED" note). If present and it declares the decision no longer live, that
   is decay **already documented** — quote the key phrase as evidence, do not treat it as news.
2. **Falsifier / expiry / hard-date clauses inside the body**, not just the top blockquote.
   Determine whether the named date has passed or the named condition has since been met, and
   whether a later document already records the discharge.
3. **Factual claims asserted as current/ongoing** (a constant, a path, "the code path is X",
   "currently Y holds") — spot-check against the actual current source those claims are about, not
   against the ADR's own narrative. This is the check most likely to surface an undocumented case:
   an ADR can be internally consistent and still be describing a world that no longer exists.
4. **Supersedes / Superseded-by / Superseded-in-part-by header fields** — cross-check both
   directions. A later ADR claiming to supersede an earlier one should be reciprocated in the
   earlier ADR's header; a mismatch either way is worth a look.
5. Do **not** flag an ADR merely because the one-time action it recorded (a rename, a retirement,
   a lock) is complete — a finished one-time decision is still an accurate historical record. Flag
   only when current reality actually contradicts what the ADR asserts as true.

Verdict per ADR: `STILL_APPLICABLE` / `DECAYED_DOCUMENTED` (decision no longer holds, but the
repo already says so somewhere) / `DECAYED_UNDOCUMENTED` (decision no longer holds, nothing says
so) / `UNCERTAIN`. `UNCERTAIN` is a verdict, not a punt — same discipline as the programme audit's
AMBIGUOUS: it must name the specific evidence that would resolve it and a date/trigger to
re-check, not just "needs a human look" left open-ended.

**Scale the method to the corpus.** For a small corpus (rough guide: under ~30 Accepted ADRs),
read them inline in the main context — a fan-out workflow's overhead isn't worth it below that
size. Above it, use the batch scan → verify fan-out below. Batch size itself should track typical
ADR length in the corpus (shorter, templated ADRs tolerate bigger batches per reviewer call;
long, addendum-heavy ones need smaller batches to get real per-file attention) — do not default to
a fixed batch size without checking that.

**Phase 2 — Verify.** Every ADR *not* scored `STILL_APPLICABLE` in Phase 1 gets an independent
second pass — a fresh reviewer, explicitly briefed to try to refute the flag rather than confirm
it, re-deriving the evidence from scratch (not trusting the Phase-1 evidence string at face
value). This catches two failure directions: Phase-1 false positives (a benign historical note
misread as decay — the canonical run caught one: an apparent gap that a *later* ADR had already
addressed under a different name), and Phase-1 under-calls (a case scored `DECAYED_DOCUMENTED`
that on closer reading has no real discharge anywhere and should be `DECAYED_UNDOCUMENTED` — the
canonical run's two real findings were both *upgrades* of this shape, not fresh Phase-1 flags).

Only fan out Phase 2 across the flagged subset, not the full corpus — this is the barrier point
where cost should concentrate (most of the corpus clears Phase 1 clean).

---

### Known traps

1. **Trusting a reviewer's structured output without a sanity check on its content.** The
   canonical run had one Phase-2 call return schema-valid but content-empty output (both
   free-text fields literally read as placeholder text, not real reasoning) while still carrying a
   verdict field. A verdict with no real reasoning behind it is not a verified finding — re-run it
   or verify by hand before trusting the verdict alone.
2. **A stale claim mirrored in an index file.** If the corpus maintains a summary/index document
   (a table of every ADR with a one-line status), check whether it repeats the same stale claim
   the source ADR carries — fixing the ADR without fixing its index mirror leaves the drift alive
   in the more-frequently-read surface. Correct the mirror in the same commit as the discharge addendum.
3. **Conflating "decayed" with "wrong when written."** This audit is about drift *since*
   ratification, not original authoring error. An ADR that was correct when accepted and has since
   been overtaken by events is decay; an ADR that was wrong on day one is a different problem
   (a ratification-quality failure) with a different fix.
4. **Alarm at the raw decayed count.** A healthy corpus with good addendum-on-discovery habits
   can show a large `DECAYED_DOCUMENTED` count and a near-zero `DECAYED_UNDOCUMENTED` count — that
   is a *good* result, not a bad one. The count that matters is `DECAYED_UNDOCUMENTED`; report the
   `DECAYED_DOCUMENTED` figure for completeness but do not read a high number there as programme
   ill-health on its own (that verdict belongs to the programme audit, not this sweep).
5. **Batch-size mistuning.** Batches too large risk shallow per-ADR treatment inside a single
   reviewer call; batches too small multiply fixed per-call overhead for no depth gain. Recalibrate
   from the corpus's typical ADR length, not a fixed constant.
6. **A finding reported and then forgotten.** A `DECAYED_UNDOCUMENTED` verdict is not complete
   until it has a named remediation (usually: author a short discharge addendum) *and* an owner —
   either fixed in the same session that ran the audit, or logged as a forward obligation
   (this repo's `STATE.md` forward-obligations surface, or the equivalent in another repo) with a
   date. Reporting the drift without assigning who closes it repeats the exact failure this sweep
   exists to catch, one layer up.
7. **The audit itself going ceremonial.** A mechanically-run periodic audit that always comes back
   "corpus healthy, nothing new" across several consecutive runs is at risk of being rubber-stamped
   rather than actually re-examined — the same failure the programme audit's "cadence ceremony" trap
   names for programme-level audits. If several consecutive runs find zero `DECAYED_UNDOCUMENTED`,
   treat that as a prompt to check whether the scan is still reading ADRs closely (e.g. spot-check
   one run's Phase-1 evidence by hand) rather than as proof the corpus needs no more scrutiny.

---

### Output artifact

Follow `brief-authoring`'s audit-note template. Land at
`docs/notes/audits/adr-corpus/YYYY-MM-DD-adr-decay-audit.md`:

- Summary table: verdict counts (`STILL_APPLICABLE` / `DECAYED_DOCUMENTED` /
  `DECAYED_UNDOCUMENTED` / `UNCERTAIN`), Phase-1→Phase-2 reclassifications (false positives
  caught, under-calls upgraded), any Phase-2 calls that failed or returned degenerate output and
  how they were resolved.
- One entry per `DECAYED_UNDOCUMENTED` finding in full: the stale claim, the current reality,
  where the drift actually got recorded (if anywhere adjacent) and why it didn't reach the ADR in
  question, recommended remediation (usually a short discharge addendum, occasionally a header
  field correction).
- A compact list (file + one-line issue + action-or-none) for every `DECAYED_DOCUMENTED` finding —
  most should read "no action, already discharged by `<file>`."
- Do not silently drop the failed/degenerate Phase-2 calls from the report — name them and how
  they were resolved (manual re-check, re-run), per this repo's no-silent-caps convention.

**Remediation weight.** In a repo with a tiered decision-ceremony convention (this repo's
`docs/adr/2026-08-08-adr-ceremony-tiering.md`), a discharge addendum that records drift on an
existing ADR is *recording a fact*, not creating new doctrine — it does not by itself need a fresh
full-ceremony decision record. Only escalate to a new ADR when the remediation itself changes a
rule, gate, or binding convention going forward (rare for this sweep's findings).

---

### Discipline check summary

```
[ ] Full Accepted-ADR list enumerated from the actual Status header (not assumed from a prior count)
[ ] Phase 1 scan covers every ADR in the list, none silently dropped
[ ] Phase 2 verify runs on every non-STILL_APPLICABLE flag, framed to refute not confirm
[ ] Every Phase 2 verdict has real reasoning behind it, not placeholder/degenerate output
[ ] DECAYED_UNDOCUMENTED findings each carry a named remediation AND an owner/date (fixed now, or logged forward)
[ ] UNCERTAIN verdicts each carry a named resolving check and a re-test date, not left open-ended
[ ] Index/summary-mirror documents checked for the same stale claim, not just the source ADR
[ ] Output artifact lands at docs/notes/audits/adr-corpus/, following brief-authoring's template
[ ] If this is the Nth consecutive all-clear run, one Phase-1 batch's evidence spot-checked by hand
[ ] Next trigger (cadence or event) named before closing
```
