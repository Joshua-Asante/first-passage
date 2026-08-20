# Archived sections — persona-hierarchy design spec

**Source:** [`docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`](../2026-08-18-loop-persona-hierarchy-design.md)
**Archived:** 2026-08-19, operator-authorized cut, per
[`docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`](../../../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md).

Verbatim text below, unedited from the live spec at archival time. Each section stayed at zero
executions from ratification (2026-08-19) to archival (2026-08-19, same day) — none of this is a
"proven wrong" verdict, only "never used, don't carry it as live spec weight until it is." Kept here
in full rather than only in git history so it's a plain read, not an archaeology exercise, if any of
it needs to come back. Re-propose per the live spec's own §6.7/§11 discipline: only when the
mechanism's own stated trigger is imminent, not preemptively.

---

## §6.3 addendum — Citation-diff / independent-dissent flag (drafted, not wired in)

> **Drafted, not wired in (added 2026-08-19).** A deterministic extension to synthesis, sketched here
> for review and intentionally not yet active: for every pair of personas' non-NIT findings, flag
> where `severity` diverges (one flags BLOCKER/CONCERN, another says clean) **and** their `location`
> fields are an exact non-match — a purely syntactic proxy for "independently-sourced" dissent, no
> fuzzy topic-matching. Where it fires, inject a line into the synthesis prompt (mirroring how
> `hardBlockLine` is already injected today for the CRO hard-block above) instructing the synthesis
> pass to surface that finding prominently as independently-sourced dissent, never average it into
> general disagreement. This sharpens the "dissent preserved verbatim" rule above with a concrete
> escalation signal, without reopening the CRO hard-block's status as the *only* case where a dissent
> is elevated above uniform advisory status.
>
> **Held, explicitly, until the first real N=3 data point lands (§10) — currently 1/3 banked
> (GSUB-2, §13 addendum).** Wiring this into the live
> `.claude/workflows/pre-ratification-adversarial-panel.js` before the base mechanism itself has
> cleared its own falsifier gate would layer new analytical machinery onto a mechanism still on
> probation. This paragraph is the frozen spec for that future patch, not the patch itself — no code
> changes accompany this addition.

**Why archived:** self-labeled "drafted, not wired in," explicitly held until its own stated
condition (N=3 real data) clears. Archiving simply enforces the hold that was already written —
nothing here reverses a decision, it removes standing spec text for a patch that was never applied
and whose own gate hadn't opened.

**Confirmed stays archived, 2026-08-19 (tested, not just deprioritized).** Operator pushback asked
whether archived items would "earn their keep" against real evidence rather than being assumed
ceremonial. Ran the actual rule (severity diverges AND `location` fields don't match, across every
pair of non-NIT findings) against GSUB-2's real panel output: CIO's BLOCKER (routing authority,
`§7 Phase 2.5 lines 193-201`) and COO's CONCERN (c3 coverage gap, `lines 197-199`) differ in both
severity and location, so the rule fires — flagging them as "independently-sourced dissent." They
are not: the two findings are about unrelated questions and no genuine disagreement exists between
the personas on either topic. The syntactic proxy produces a false positive on the one real data
point available. Needs a same-item/same-nomination constraint (not just non-matching `location`
strings) before re-proposing — a design flaw found by testing, not just an unmet N=3 precondition.

---

## §6.4.1 — Charter versioning and bounded self-refinement (added 2026-08-19)

> **Charter versioning (no caveat).** Every `docs/personas/<slug>.md` file is already ordinary
> committed markdown. The only addition is capturing the charter's git state at spawn time:
> `Charter-Commit` (§12's template) records the short SHA of `docs/personas/<slug>.md`
> (`git log -1 --format=%h -- docs/personas/<slug>.md`) at spawn time, filled in by the calling
> session during the §12 log-append procedure — no change to the Workflow script itself. This makes a
> review reproducible against the exact charter text in force when it ran.
>
> **Bounded self-refinement, Governance-gated.** A persona may *propose* — never silently apply — a
> charter edit, but only on a pre-registered trigger: **2 consecutive real log entries where Joshua's
> ratification diverges from the persona's recommendation, citing the same root cause.** On that
> trigger, the persona drafts a proposed charter diff + rationale, appended to its own log as a
> flagged, not-yet-ratified entry.
>
> **Before Joshua ever sees it, a fresh Head of Governance spawn independently reads only the
> proposed diff + stated rationale — not the underlying case history — and endorses or objects,
> logged to `docs/personas/head-of-governance-log.md` per its own existing convention.** This
> Governance hop is required specifically for control-layer personas (CRO, Head of Risk & Sizing,
> Model Validation Analyst, and Head of Governance itself) proposing edits to their *own* review
> scope — without it, a control-layer persona auditing its own proposed redefinition reproduces, in
> miniature, exactly the self-audit failure §5.2.1 already reasoned through once ("placing [Head of
> Governance] under CRO would have Risk auditing itself"). Only after Governance's independent pass
> does the diff reach Joshua, as an ordinary doc-change PR — the same ratification path any other
> charter or doctrine edit in this repo already takes.

**Why archived:** trigger requires 2 consecutive divergent ratifications; the only real review to
date (GSUB-2) produced zero divergence. Outside current temporal scope — mirrors
`operational_rules.md`'s "rules earn their place by being paid for." Re-propose when a second
divergence looks imminent, not before the first.

---

## §6.6 — Cross-examination round (interactive, opt-in — added 2026-08-19)

> **Status: ACCEPTED — ratified by Joshua 2026-08-19, in-session direct instruction ("ratify now"),
> separately from the persona-hierarchy ADR's own D1 pointer** (which predates this subsection by
> roughly two hours the same day and does not itself cover it — see the ADR's own addendum). No
> implementing code exists yet for anything in this subsection; ratification licenses building it,
> it does not retroactively assert it is built. Preceded by two rounds of adversarial review before
> ratification was asked for: the full panel (workflow `wf_88c21d8d-a7f`, `BLOCKED`, 6 confirmed
> BLOCKERs, fixed same day) and a targeted recheck of those fixes (workflow `wf_8d2086b0-27d`, which
> found one fix still inadequate and prompted the structural redesign in mechanics point 5 below —
> that redesign itself was ratified on the operator's own judgment, without a third review round).
>
> Everything in §6.1–§6.5 stays exactly as ratified: Stage 1 is blind, independent, and no persona
> reads another's live reasoning during its *own* review. This subsection adds a strictly additive,
> **post-synthesis** extension for the case where Joshua wants two personas to argue a specific point
> directly, rather than only reading the synthesis memo's account of their disagreement.
>
> **Trigger.** Elective, never automatic. Either (a) Joshua names a finding and a persona pair
> directly, or (b) the synthesizing session proposes it when Stage 1's own verify pass already
> produced a *disputed* (not unanimous) finding between two personas who both own the item — since
> that is exactly the shape of disagreement this round exists to deepen. Forcing it on every panel
> run would blur "genuine disagreement worth debating" into ceremony, the same failure class the
> retention self-test (§2.1) already worries about for the rest of this design.
>
> **Ownership precondition (hard gate, not a judgment call).** A cross-examination round between
> persona A and persona B on item X may run **only if both A and B are named Primary or Secondary
> owner of X** in `docs/personas/ownership-map.md` — or, for an item the ownership map doesn't yet
> cover, both are in the panel's own spawn list for X under the §4 office-touches-domain rule. If
> this fails, the round does not run — same fail-closed posture as the frozen-artifact precondition
> (§6.1), and for the same reason: without it, cross-examination becomes a free-for-all where any
> persona can dogpile any other persona's finding outside its own mandate, which is exactly the
> domain-crispness §7's error-handling table already protects one layer down.
>
> **CRO carve-out (mandatory, not an ownership-map lookup).** CRO is always an eligible cross-
> examination participant on any GRAND-tier item, regardless of what `ownership-map.md` lists —
> this mirrors this spec's own §4 mandatory-CRO rule ("CRO on every single GRAND decision, with no
> exceptions") verbatim, one layer down. Checked against the map directly: CRO is named Primary or
> Secondary owner on exactly 1 of 38 tracked pursuit rows (`e1`), so without this carve-out the
> ownership gate would hard-fail-closed on the other 37 even though CRO's own Stage-1 participation
> producing the disputed finding was itself mandatory. The gate as applied to every *other* persona
> pair is unchanged.
>
> **Mechanics.**
> 1. Stage 1 findings are **frozen** once produced. A cross-examination round never edits, deletes,
>    or retroactively softens a Stage-1 finding — it produces new, clearly-labeled response entries
>    layered on top, matching the append-only ethic persona memory (§6.4) already uses.
> 2. The round is a single fresh `agent()` spawn for persona **B** — never persona A rewriting
>    itself. B reads: (a) its own Stage-1 finding on this item, if any; (b) persona A's Stage-1
>    finding on this item, verbatim, in full; (c) nothing else — not the synthesis memo's framing of
>    it, not any other persona's take. B is prompted to state agreement, refutation, or partial
>    agreement with its own reasoning — not asked to "resolve" the disagreement, since resolution
>    stays Joshua's alone (D5, unchanged).
> 3. Capped at **one response round per (finding, persona-pair) by default.** A second round (B
>    responds, then A responds to B's response) requires Joshua's explicit ask each time — bounding
>    the round prevents unbounded ping-pong and keeps it deliberate rather than automatic, the same
>    discipline the verify stage already applies (two skeptics per finding, not unlimited).
> 4. Joshua may inject his own question or framing into what persona B reads (e.g., *"B, does A's
>    point hold given the March allocation ADR?"*). This is safe specifically because by the time a
>    cross-examination round exists, **every** Stage-1 review of the item is already complete and
>    locked — there is no remaining unbiased persona left to protect from seeing the CEO's framing,
>    and Joshua's ratification authority (D5) already presumes he can steer the conversation openly
>    once independent judgment has been recorded.
> 5. **A round's written record lives in a separate file, `docs/personas/<slug>-cross-exam-log.md`
>    — never in `docs/personas/<slug>-log.md`, the file §6.2's fresh Stage-1 spawn actually reads.**
>    File-separation closes the influence pathway structurally: a future Stage-1 spawn of persona B,
>    per §6.2, reads only `<slug>-log.md` — the cross-exam log is never in that read path, so
>    operator-framed content genuinely cannot reach a not-yet-run Stage-1 judgment on an unrelated
>    future item. The cross-exam log is read by: a human auditing the mechanism, a future
>    *cross-examination* round involving that persona, and the supplementary synthesis addendum
>    author. It is never in a Stage-1 spawn's read list.
> 6. A round still produces a supplementary synthesis addendum when it changes the operator-facing
>    recommendation — same as before, never silently folded back into the original synthesis text.
>
> **What this does not change.** The CRO hard-block (§6.3/D3) is untouched: if the disputed finding
> under cross-examination is itself a CRO safety-invariant citation, the hard-block already fired at
> synthesis, and a round can only have B explain its own reasoning — never overrule CRO's blocking
> citation. A new safety-invariant citation, authored by CRO specifically and surfaced for the first
> time by cross-examination itself, is not exempt just because it arrived late: the same
> `citesSafetyInvariant` check (§6.3) applies to CRO's own cross-exam text before it reaches any
> operator-facing addendum. Scoped to CRO specifically, matching §6.3's own literal wording and the
> underlying code (`croHardBlockFires` keys off the `cro` lens result only) — a non-CRO persona's
> citation during cross-examination does not trigger this deterministic hard-block.
>
> **Falsifier.** Rides the existing §10 tracker rather than opening a second clock, with an explicit
> third branch so a low-opportunity count isn't silently read either way: **(a)** if ≥3 real
> disputed-finding opportunities accrue and cross-examination is never invoked, that is informative
> against the mechanism; **(b)** if invoked ≥1 time and never changes the operator-facing synthesis
> addendum, that is also informative against it; **(c)** if fewer than 3 disputed-finding
> opportunities have accrued by the shared checkpoint, the mechanism is **not yet tested**, not
> passing. The §13 rehearsal produced zero disputed-finding-between-personas events, a real data
> point toward branch (c) being the likely outcome at the first checkpoint.

**Why archived:** zero implementing code, zero executions — no `<slug>-cross-exam-log.md` file was
ever created. Consumed two full adversarial-review cycles (one `BLOCKED` with 6 confirmed BLOCKERs,
a recheck that found the fix "visibility-only" and forced a redesign) reviewing a feature that was
never built. Per Great Prune R5: an obligation whose check cannot fire is deletable even when signed.
Re-propose alongside the first real disputed Stage-1 finding that actually needs it.

**Confirmed genuinely blocked on data, 2026-08-19 (tested, not just deprioritized).** Checked
GSUB-2's real synthesis output directly: "DISPUTED FINDINGS FOR OPERATOR JUDGMENT: None... every
non-nit finding was either unanimously confirmed or unanimously refuted." Zero disputed findings
exist anywhere in this repo's real panel history — the trigger genuinely hasn't fired, not "wasn't
given a chance." No test can manufacture this precondition without inventing a fake disagreement.

---

## §10.1 — Preference-anchoring companion check (added 2026-08-19)

> A distinct risk from the H/Falsifier above, surfaced by 2025-2026 research on stateful personal
> agents: once a claim is committed to durable (not session-only) memory, agreement-bias/failure
> rate has been measured to rise sharply on repeated retrieval — agents can promote a user-favored
> conclusion to higher epistemic authority over time. The persona-memory design (§6.4) is durable,
> append-only, and read before every spawn — precisely the condition that research names as the
> trigger. This is a plausible latent exposure in an already-built, already-ratified mechanism, not
> a new risk this addition introduces.
>
> **Check (a distinct H′, not folded into the §10 count above).** After a given persona's log
> accumulates its 5th and every 5th subsequent real (non-rehearsal) entry, read the trend of two
> figures across that persona's history: (i) the plain agreement rate — entries where `Ratified as
> recommended` reads `Yes`, divided by total; (ii) the `Confirmed findings` trend — is it drifting
> toward "none." The specific red flag is **both trending together** — agreement rising while
> findings-count falls — not high agreement alone, since a genuinely careful reviewer can legitimately
> agree with a careful operator often. That combined signature is what "hollowing into a rubber
> stamp" actually looks like on paper, distinct from ordinary competent agreement.
>
> This is a manual, periodic read (Joshua or CC eyeballing a log file), not automated tooling —
> proportionate to a diagnostic that is only meaningful past a handful of data points, and consistent
> with this spec's own anti-belt-growth stance (§8) against building infrastructure ahead of
> demonstrated need. Any note this check produces is tagged the same way the existing `**Rehearsal:**
> yes` convention already tags non-counting entries (§13), so a future reader of
> `docs/personas/*-log.md` never mistakes this diagnostic for part of the real §10 N=3 count.

**Why archived:** trigger is the 5th real log entry for a given persona. Deepest log at archival time
is CRO's, at 3 total entries (1 rehearsal + 2 real). Structurally unreachable at current usage — the
source it's drawn from (durable personal-agent memory research) is also a different system class
than this review-panel mechanism. Re-propose once any persona's log approaches 5 real entries.

**Reconfirmed 2026-08-19 (re-checked, not just re-asserted):** CRO's log now has 4 entries after the
§10.2 self-consistency test below was logged — still short of 5. Genuinely blocked on data.

---

## §10.2 — Self-consistency companion checkpoint (added 2026-08-19)

> A distinct, earlier, and cheaper comparison point than the H/Falsifier above — sourced from 2026
> research finding automatically-designed multi-agent systems can underperform a single agent's
> Chain-of-Thought with Self-Consistency (the same agent sampled N times, majority vote), at a
> fraction of the compute cost.
>
> **Check.** On the first 1-2 real GRAND-tier reviews, alongside the real panel run, separately spawn
> 3 same-persona samples of the CRO build prompt (already defined at `PERSONAS.find(p => p.key ===
> 'cro').build()` in `.claude/workflows/pre-ratification-adversarial-panel.js`) via a plain
> `parallel()` call, majority-vote their `clean`/`findings` output, and compare against what the CRO
> seat produced inside the real panel run. No change to the ratified workflow file is needed — this
> runs alongside it, as an ad hoc side call, not inside it.
>
> **Explicitly a different H′, not a substitute measurement.** The §10 falsifier above is anchored to
> human ground truth ("changes what Joshua would have ratified"). Self-consistency-vs-panel agreement
> is AI-vs-AI — a panel could match the self-consistency baseline 100% of the time and still change
> what Joshua would have ratified, or diverge sharply and still match his actual call. This checkpoint
> is a supplementary, non-counting diagnostic, logged with the same explicit non-counting tag §13's
> rehearsal entries already use, never folded silently into the real falsifier count.

**Why archived:** trigger ("first 1-2 real GRAND-tier reviews") already fired at GSUB-2, and the
checkpoint was never executed — a grep for "Self-consistency checkpoint" across every real log file
returns zero hits. A diagnostic whose own qualifying event already passed unexercised isn't a live
obligation, it's a missed one; archiving rather than re-running it after the fact avoids manufacturing
a retroactive data point. Re-propose fresh at the next real GRAND-tier review if still wanted.

**Superseded 2026-08-19 — actually exercised, retroactively, and discharged.** Reconsidered after
operator pushback: the frozen GSUB-2 artifact already exists, so running this side-experiment
against it now isn't "manufacturing a retroactive data point," it's testing against evidence that
was already there. Spawned 3 fresh CRO samples, blinded to the real outcome (given only the
pre-GSUB-2 log state), against the same frozen brief. Result: 3/3 `clean:true`, majority matches
the real panel's CRO verdict exactly; one sample independently found the same NIT the real CIO lens
raised. Logged at `docs/personas/cro-log.md` (2026-08-19, tagged non-counting). This was always
designed as a bounded 1-2-use diagnostic, not a standing mechanism — having now run it once, the
spec text stays archived (nothing left to keep "live"), but the archival reason changes from
"missed" to "exercised and done."

---

## §12 — Extended log-append template fields (Evidence-Cited, Deviation-from-Precedent, Charter-Commit)

> ```markdown
> ## <YYYY-MM-DD> — <result.targetPath>
>
> **Verdict:** <BLOCKED | CLEAR-WITH-CONCERNS | CLEAR, from result.synthesis for this persona>
> **Confirmed findings:** <count, or "none">
> **Evidence-Cited:** <the specific file:line or artifact section this verdict was keyed off, from
> result.synthesis's per-persona breakdown -- "n/a" if clean with nothing to cite>
> **Deviation-from-Precedent:** <a one-line note on how this verdict differs from what this
> persona's own prior log entries would have predicted, or "None" if it doesn't -- "n/a -- first
> entry" if step 1 found no prior log>
> **Charter-Commit:** <short git SHA of docs/personas/<slug>.md at spawn time>
> **Ratified as recommended:** <Yes | No | Pending -- operator has not yet ratified>
> ```

**Why archived:** `scripts/check_personas.py`'s `LOG_REQUIRED_SUBFIELDS` was never updated to enforce
these three fields, and a grep across every real log file (`docs/personas/{cfo,cio,coo,cro,
head-of-execution}-log.md`) confirms zero entries have ever used any of them — including entries
written the same day this template extension landed. Per Great Prune R5, a field no gate checks and
no entry uses is ceremony regardless of intent. The live spec's §12 now reverts to the minimal
3-field template (`Verdict` / `Confirmed findings` / `Ratified as recommended`) that
`check_personas.py` actually enforces. Re-propose the extended fields together with the code change
that would make them load-bearing (i.e., have the log-append step or `check_personas.py` actually
populate/require them), not as prose alone.

---

## §14 — MAST pre-mortem procedure — RESTORED 2026-08-19, same day, see below

**This section is no longer archived.** Kept here only as a record of the brief archival episode.
Tested against GSUB-2's real preserved journal (`wf_e016a5d9-3f6`) the same day it was archived;
found 2 genuine findings the panel's own verify stage had not caught, falsifying the "duplicated by
a higher-fidelity source" rationale below. Live text is back at
[design spec §14](../2026-08-18-loop-persona-hierarchy-design.md#14-mast-pre-mortem-procedure-added-2026-08-19-briefly-archived-and-restored-same-day--see-change-history),
including the actual findings from that run. Original archived text preserved below for the record.

## §14 — MAST pre-mortem procedure (added 2026-08-19) — ORIGINAL ARCHIVE ENTRY, SUPERSEDED ABOVE

> A one-time, read-only process check against the panel's own mechanism — distinct from §10's
> falsifier, which measures OUTCOME only ("does panel input ever change a ratified disposition").
> Sourced from Cemri, Pan, Yang et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv:2503.13657,
> NeurIPS 2025 Datasets & Benchmarks) — MAST, an empirically-derived 14-mode taxonomy of multi-agent
> failures, built from 150+ expert-annotated traces (κ=0.88 on the IAA subset) across 5 MAS
> frameworks.
>
> **Scope, narrowed to this panel's actual architecture.** MAST was built from systems where agents
> converse (AutoGen, ChatDev, AppWorld). This panel is a fan-out of independent, schema-constrained,
> single-shot `agent()` calls across three pipeline stages (Review → Verify → Synthesize) — never a
> live back-and-forth dialogue. Four of the 14 modes assume a conversation that doesn't exist here
> and are excluded by architecture, not oversight: loss of conversation history, unaware of
> termination conditions, conversation reset, fail to ask for clarification.
>
> The other ten modes map onto this panel's actual stages:
>
> | Mode | Stage | Check |
> |---|---|---|
> | Disobey task specification | Review | Did the persona's finding stay inside the target artifact's actual subject matter, not a different task? |
> | Disobey role specification | Review | Did the persona's finding stay inside its stated Domain (`docs/personas/<slug>.md`)? |
> | Task derailment | Review | Does `notes`/`findings` actually address the target artifact? |
> | Information withholding | Synthesize | Does every CONFIRMED/DISPUTED finding in `lensResults` surface in the synthesis memo? |
> | Ignored other agent's input | Synthesize | Does the memo engage with a persona that said `clean:true` with a substantive rationale? |
> | Reasoning-action mismatch | Review + Verify | Does a finding's `why_wrong` support its `severity`? Does a skeptic's `rationale` support its `refuted` call? |
> | Premature termination | Review | Is a `clean:true` result backed by specific section/line engagement, not a generic one-liner? |
> | No/incomplete verification | Review + Verify | Open every cited `location` and confirm it exists and says what's claimed. |
> | Incorrect verification | Verify | Re-check a sample of the Verify stage's own `refuted` calls independently. |
> | Step repetition | Verify (weak) | Do the two independent skeptic votes read as genuinely independent, or templated restatement of each other? |
>
> **Cadence — one-time, not periodic.** Run once, against `<transcriptDir>/journal.jsonl` from each
> of the first 3 real (non-rehearsal) panel uses tracked by §10's own falsifier.

**Why archived:** never run once, and the citation itself needed two rounds of self-correction to its
own arithmetic (framework count, mode count) before it was ever exercised — a process check that
generated more adversarial-review overhead fixing itself than actual usage. Duplicated by a
higher-fidelity source already in the corpus: the existing `pre-ratification-adversarial-panel`
already performs pre-mortem-style failure enumeration on every real run. Re-propose against real
`journal.jsonl` data once 3 real panel uses exist, if it still seems worth a one-time read at that
point.
