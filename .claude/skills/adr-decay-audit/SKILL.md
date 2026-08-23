---
name: adr-decay-audit
description: Periodic/triggered sweep of the entire Accepted-ADR corpus for continued applicability — distinct from skew-audit (event-triggered, Code:-pointer scope only, fires on version locks) and programme-audit (programme-level Lakatos verdict on methodologies/portfolio as wholes, not per-decision). Use when asking "which ADRs still hold", "has anything decayed", "is our decision record still accurate", before a repo-public snapshot or major handoff, or on the cadence named below. Produces a four-way verdict per ADR (STILL_APPLICABLE / DECAYED_DOCUMENTED / DECAYED_UNDOCUMENTED / UNCERTAIN) via a two-phase batch-scan-then-adversarial-verify method. Hand off to brief-authoring for the audit-note artifact shape, blast-radius for a narrower single-edit propagation check, programme-audit for the programme-level (not per-ADR) diagnostic.
---

# ADR Decay Audit

## Purpose

ADRs are the canonical record of every decision in this repo. Canonical-but-wrong is worse than
absent, because it is trusted by default. This skill exists because **no other mechanism
periodically re-checks the whole Accepted-ADR corpus for continued applicability**:

- **Rule 6 skew-audit** (`docs/operational_rules.md` §6, `.claude/commands/skew-audit.md`) fires
  only on a strategy version-lock event and checks a narrow target set (`CLAUDE.md`, ADR `Code:`
  pointers, methodology docs) inside a bounded commit window.
- **programme-audit** runs a Lakatos diagnostic on *programmes* (methodologies as a whole, the
  strategy portfolio as a whole) on a quarterly/semi-annual cadence — it does not visit individual
  ADRs one by one.
- **blast-radius** is reactive: it fires after a specific edit, to catch other docs that might
  still restate what was just changed. It does not sweep ADRs that no recent edit touched.

The gap this leaves: an ADR whose header still says `Accepted`, but whose factual claim has been
overtaken by a *later* ADR that never links back to it, sits in the corpus indefinitely unless
someone happens to reread it. The canonical worked example (first full-corpus run, this skill's
origin) found this exact pattern twice in one pass out of roughly 150 Accepted ADRs — both cases
were a later ADR changing a number/architecture claim without any cross-reference added to the
earlier ADR that still asserted the old value as current.

**Boundary with sibling skills:**

- `skew-audit` — narrower and cheaper; keep using it at every version lock. This skill does not
  replace it.
- `programme-audit` — a Degenerating/Progressive verdict on a *programme* is a different question
  from "is ADR X's factual claim still true." Do not conflate a clean per-ADR sweep with a healthy
  programme, or vice versa — an ADR corpus can be 95% still-applicable while the programme it
  belongs to is Degenerating, and the reverse.
- `blast-radius` — run it immediately after any edit that touches an ADR's subject matter. Run
  *this* skill on a cadence or before a high-stakes moment, independent of whether anything was
  just edited.
- `brief-authoring` — provides the audit-note artifact template this skill's output should follow.

---

## Trigger conditions

**Cadence (backstop):** piggyback on `programme-audit`'s quarterly meta-layer cadence — run this
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

## Method: two-phase scan → verify

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
so) / `UNCERTAIN`. `UNCERTAIN` is a verdict, not a punt — same discipline as `programme-audit`'s
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

## Known traps

1. **Trusting a reviewer's structured output without a sanity check on its content.** The
   canonical run had one Phase-2 call return schema-valid but content-empty output (both
   free-text fields literally read as placeholder text, not real reasoning) while still carrying a
   verdict field. A verdict with no real reasoning behind it is not a verified finding — re-run it
   or verify by hand before trusting the verdict alone.
2. **A stale claim mirrored in an index file.** If the corpus maintains a summary/index document
   (a table of every ADR with a one-line status), check whether it repeats the same stale claim
   the source ADR carries — fixing the ADR without fixing its index mirror leaves the drift alive
   in the more-frequently-read surface.
3. **Conflating "decayed" with "wrong when written."** This audit is about drift *since*
   ratification, not original authoring error. An ADR that was correct when accepted and has since
   been overtaken by events is decay; an ADR that was wrong on day one is a different problem
   (a ratification-quality failure) with a different fix.
4. **Alarm at the raw decayed count.** A healthy corpus with good addendum-on-discovery habits
   can show a large `DECAYED_DOCUMENTED` count and a near-zero `DECAYED_UNDOCUMENTED` count — that
   is a *good* result, not a bad one. The count that matters is `DECAYED_UNDOCUMENTED`; report the
   `DECAYED_DOCUMENTED` figure for completeness but do not read a high number there as programme
   ill-health on its own (that verdict belongs to `programme-audit`, not this skill).
5. **Batch-size mistuning.** Batches too large risk shallow per-ADR treatment inside a single
   reviewer call; batches too small multiply fixed per-call overhead for no depth gain. Recalibrate
   from the corpus's typical ADR length, not a fixed constant.
6. **A finding reported and then forgotten.** A `DECAYED_UNDOCUMENTED` verdict is not complete
   until it has a named remediation (usually: author a short discharge addendum) *and* an owner —
   either fixed in the same session that ran the audit, or logged as a forward obligation
   (this repo's `STATE.md` forward-obligations surface, or the equivalent in another repo) with a
   date. Reporting the drift without assigning who closes it repeats the exact failure this skill
   exists to catch, one layer up.
7. **The audit itself going ceremonial.** A mechanically-run periodic audit that always comes back
   "corpus healthy, nothing new" across several consecutive runs is at risk of being rubber-stamped
   rather than actually re-examined — the same failure `programme-audit`'s "cadence ceremony" trap
   names for programme-level audits. If several consecutive runs find zero `DECAYED_UNDOCUMENTED`,
   treat that as a prompt to check whether the scan is still reading ADRs closely (e.g. spot-check
   one run's Phase-1 evidence by hand) rather than as proof the corpus needs no more scrutiny.

---

## Output artifact

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
rule, gate, or binding convention going forward (rare for this skill's findings).

---

## Discipline check summary

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
