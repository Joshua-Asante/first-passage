# Stealth-model second opinion, scoped: `stealth/ox-alpha` as a sanitized-only adversarial lens — `2026-08-22-ox-alpha-adversarial-lens-scope`

Filename: `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`

**Status:** `Accepted` — ratified by operator (JA) 2026-08-22, after the validation-test
evidence in the addendum below (both seeded ground-truth defects independently caught blind)
**Decision date:** 2026-08-22
**Authors:** Joshua (direction) + Claude Code (evaluation, research workflow, draft)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [cc-cursor surface allocation](2026-07-14-cc-cursor-surface-allocation.md) ·
[cc-cursor autonomous loop](2026-08-14-cc-cursor-autonomous-loop.md) ·
[ADR ceremony tiering](2026-08-08-adr-ceremony-tiering.md) ·
[four-friendly-firms program](2026-07-12-prop-portfolio-four-friendly-firms.md) ·
[Tradeify venue de-scope](2026-08-04-tradeify-venue-descope-eval-included.md) ·
`.claude/skills/fable-judge/SKILL.md` · `.claude/skills/pre-ratification-adversarial-panel/`
**Layer:** governance convention (external-tool boundary). **$0 spend** (free listing) **/ K=0**
(this ADR gates a review lens, not a strategy candidate).

---

## §0 — Rule 0 reads (production-source verification)

Files read before authoring this ADR:

- `.claude/skills/cursor-fleet/SKILL.md` — anchor: `d88e5f22be1` (verified
  `git log -1 -- .claude/skills/cursor-fleet/SKILL.md` on 2026-08-22, commit dated 2026-08-15)
- `.claude/skills/task-routing/SKILL.md` — anchor: `027a729589c` (2026-08-14)
- `.claude/skills/fable-judge/SKILL.md` — anchor: `6b696bdf209` (2026-08-21)
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — anchor: `027a729589c` (2026-08-14)
- `docs/adr/2026-08-14-cc-cursor-autonomous-loop.md` — anchor: `027a729589c` (2026-08-14)
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor: `91e6caad099` (2026-08-15) — for
  the tier test applied below
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` §4 and
  `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` §7 — anchor: `027a729589c`
  (2026-08-14) — for the hard-date/bottleneck framing in §1
- Memory (outside repo, this session's own record):
  `project_ox_alpha_openrouter_evaluation_2026_08_22.md` — 10/10 across three sanitized test
  batteries (quant-reasoning, single-shot code-write, multi-turn agentic debugging), each
  independently re-verified this session by hand-calculation, execution, or re-running the
  test suite myself rather than trusting the model's or a subagent's own claim.
- Memory (outside repo, precedent): `project_grokbot_evaluation_2026_08_18.md` — a prior
  external-AI-tool evaluation (xAI's "Grok Bot") that reached a REJECT verdict on
  credential/exfiltration and structural-governance-mismatch grounds, but was never promoted
  to a governing ADR ("offered but not yet authored" per that memory's own closing line). This
  ADR is the first time that class of decision lands as a repo artifact rather than staying
  memory-only.
- `https://openrouter.ai/terms/stealth` (Stealth Program EULA) — anchor: verified via WebFetch
  2026-08-22. Material finding: the model's own OpenRouter listing page says prompts/completions
  are "retained... not used for training," but the incorporated EULA governing the Stealth
  Program says the opposite for the program as a whole — it exists so OpenRouter can "collect
  User Content for use in Stealth Model training and improvement" under a license described as
  "non-exclusive, irrevocable, perpetual, transferable, worldwide, fully paid-up, royalty-free,"
  content pseudonymized by a hashed identifier only, not anonymized. No binding free-window
  end-date exists; the EULA reserves removal "at any time... with or without notice."

---

## §1 — Context

A free, anonymous-provider stealth model (`stealth/ox-alpha`, OpenRouter, appeared 2026-08-20)
was evaluated this session across three sanitized test batteries and scored 10/10, including a
genuine multi-turn agentic debugging run with sandboxed tool use, execution-verified rather than
eyeballed. Separately, a research workflow this session confirmed the actual Tradeify sprint
bottleneck is **mechanism-supply exhaustion**, not engine or data-access capacity — six research
threads run 2026-08-20 all terminated on "needs a genuinely new mechanism/data source, not
another test" — with the live queue instead holding new-modality data sourcing, an engine fix
for the composed-book "Trap #11" blocker, and **decision/pre-registration authoring** (the F1
fork ruling on how [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md)
§4 reads a Tradeify-resting discharge, plus GROW-lane pre-registration and streak-checker
artifacts), all due by the 2026-11-08 hard date.

The same workflow surfaced the EULA/training-license contradiction in §0 above — materially
different from what the model's own listing page implies, and a reason to be stricter than
"send it sanitized problems" alone. It also confirmed this repo already has one relevant
precedent (the Grok Bot rejection) that reached a governance verdict but was never captured as
an ADR — this repo's own doctrine ("ADRs are canonical for every decision," `CLAUDE.md`) implies
that gap should not repeat.

**Decision driver (one sentence):** a capable, zero-cost external model is available during a
deadline-critical, low-margin-for-error research sprint whose actual bottleneck is decision-shaped
(not more candidate-mining volume), and the CC/Cursor surface-allocation doctrine already gives a
clear boundary — locked surfaces stay CC-only — that this decision needs to extend to a
third-party, unaccountable, training-license-bearing provider explicitly, rather than leaving the
boundary to ad hoc judgment call by call.

---

## §2 — Decision

**Decision:** Claude Code may invoke OpenRouter's `stealth/ox-alpha` as a stateless, disposable,
zero-authority adversarial second-opinion lens on **sanitized, genericized** decision-authoring
artifacts — pre-registration briefs, ADR drafts, methodology writeups, closure records — run
*before* `fable-judge` and the human `pre-ratification-adversarial-panel`, never instead of them.
It receives no tool access, no repo access, no raw file contents, and no proprietary numbers,
names, or dates. Its output is candidate-objection input only: every objection must be
reconciled against the real, unsanitized artifact before being logged as a finding, and it
carries zero authority over either governing review step. All other candidate integration
patterns evaluated this session (public-mechanism-harvest worker; walled-off generic-tooling
assistant) are explicitly declined — see §3.

**Effective:** immediately upon acceptance.

**Scope:** any decision-authoring artifact Claude Code drafts in this repo — not limited to the
Tradeify sprint, though that sprint's live queue (the F1 fork ruling; GROW-lane
pre-registration/streak-checker artifacts) is this ADR's motivating and first-use context.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Public-mechanism/literature-harvest worker (third parallel lane alongside Cursor Ultra, sourcing candidate signals from published anomalies) | This session's own workflow found the literature/mechanism-harvest channel already "close to fully mined" — the 2026-08-20 discovery-channels-dry finding is that six threads died wanting a genuinely new mechanism, not more harvest volume. Near-zero marginal leverage on the actual bottleneck. |
| Walled-off generic-tooling assistant (new `path_allowlist` wrapper restricting it to `scripts/`/CI plumbing, docs prose, non-strategy tests) | The one concrete engineering blocker the sprint actually names (composed-book "Trap #11") sits in `core/portfolio_mc.py`-adjacent territory this design would itself have to exclude — the real leverage isn't in the safe zone. Building and maintaining new wrapper infrastructure under deadline pressure is unrecovered cost the moment the free listing disappears with no notice (§0 EULA finding). |
| No integration at all — personal, sanitized-problems-only side tool | Correctly names the Grok Bot precedent and the provenance risk, but treats all four candidate designs identically. The adversarial-lens design's actual payload — genericized argument structure, never the sprint's proprietary content — does not share the risk profile of the other three. Rejected as overreach given the payload difference, not because the underlying caution is wrong; the caution is instead encoded directly into §5's forbidden moves below. |
| Full repo/tool access as a cursor-fleet peer | Never seriously entertained. Direct collision with `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`'s locked-surface rule and the Grok Bot precedent's structural-governance-mismatch finding: an agent with persistent state and self-directed ambiguity resolution is the inverse of the frozen-spec, disjoint-footprint, mandatory-human-review discipline that makes the existing CC/Cursor split safe. |

---

## §4 — Falsifier (revert trigger)

**H:** a stateless, zero-authority, sanitized-only adversarial lens run by an anonymous free-tier
model adds real pre-screening value to this repo's decision-authoring artifacts without leaking
reconstructable proprietary content.

**Revert trigger:** if either (a) any single sanitized artifact sent to this lens is later shown
to be reconstructable back to a real repo strategy, parameter, or firm (a fingerprinting
incident), or (b) three consecutive uses produce zero objections that survive reconciliation
against the real artifact (the lens catches nothing a human/CC pass would not have caught
anyway), this ADR is revoked.

**Revert action:** author a new ADR that fully supersedes this one (`Supersedes:
2026-08-22-ox-alpha-adversarial-lens-scope.md full`); discontinue the lane immediately. No
migration is required — the lane is stateless by design, so reverting is a non-event, not a
fallback project.

**Trigger check schedule:** reviewed at the first use and again at the third use (whichever
exposes trigger (b) earlier), and at the next quarterly programme audit regardless.

---

## §5 — Forbidden moves (under this ADR)

- **Sending an unsanitized artifact "just this once" for speed** — ruled out because provenance
  is the actual product of this sprint; the one no-integrate argument this ADR accepts in full
  is exactly this one (§3).
- **Granting it tool or repo access to speed up round-trips** — ruled out; this directly
  reintroduces the Grok Bot structural-governance-mismatch failure mode (self-directed access to
  repo-adjacent surfaces with no per-repo ACL, no audit log).
- **Treating a differing or dissenting verdict from this lens as authoritative over `fable-judge`
  or the human panel** — ruled out; it is a tripwire generator, not a gate, same relationship
  `pre-ratification-adversarial-panel` already has to `fable-judge`.
- **Extending usage to the harvest-worker or engineering-assist patterns because the wiring is
  already free and available** — ruled out per §3; scope creep into either rejected pattern
  needs a fresh ADR, not an assumed extension of this one.
- **Treating the free listing as a load-bearing dependency** — budgeting migration effort for it,
  or delaying real sprint work waiting on it — ruled out; OpenRouter's own terms reserve removal
  "at any time... with or without notice" (§0), and the lane is designed to be disposable.
- **Letting sanitization drift toward "generic enough for now" on a distinctive, fingerprintable
  filter or parameter combination** — ruled out. This is a hardening bar added beyond the
  evaluating workflow's own proposal: if a genericized description is still specific enough to be
  recognizable as this repo's strategy even after stripping names/numbers/dates, it does not go
  out; genericize further or keep it in-house.

---

## §6 — Consequences

**Positive consequences:**
- A cheap, stateless pre-screen catches "looks like our usual template" fallacies that
  repo-fluent CC/Cursor reviewers can pattern-match past, before an artifact reaches the
  higher-cost human/`fable-judge` pass.
- Zero migration cost if the free listing disappears mid-sprint — nothing depends on it
  persisting, by design.
- Closes a policy gap the Grok Bot evaluation left open (rejected in memory, never governed by
  an ADR) with a reusable sanitize → send → triage → reconcile pattern for any future
  free/anonymous-model evaluation, without waiting for another incident to force the question.

**Negative consequences (real cost, not theatrical):**
- Adds one more review step, however cheap, to artifacts already reviewed by `fable-judge`/the
  human panel — a marginal time cost per artifact.
- Requires real sanitization discipline every single time; a sloppy pass is worse than no lens
  at all, since it substitutes the appearance of caution for the thing itself.

**Risks (probabilistic, distinct from costs):**
- The EULA's perpetual/irrevocable training-license grant means sanitized content, once sent,
  cannot be recalled — mitigated by the sanitization and fingerprinting bar in §5, not
  eliminated.
- The model's identity is unconfirmed (competing, unverified lab theories per §0); if it is later
  revealed to be a lab this repo has separately excluded, this ADR needs immediate re-review —
  no mitigation beyond the §4 trigger schedule.
- The free window could lapse mid-review with no notice — mitigated by the lane being fully
  stateless and optional, never gating a decision on its availability.

**Downstream artifacts that need updating:**
- None mechanically required — this is a policy-only decision (§7).
- A `docs/SESSIONS.md` entry documenting this session's evaluation-and-ADR work is owed at land
  time, per this repo's session-log discipline — not included in this ADR's body.

---

## §7 — Implementation plan

Policy only — no mechanical edits required. No companion CC handoff brief is needed; the lane is
invoked ad hoc by Claude Code itself under the rules in §2/§5, not built as new infrastructure.

---

## §10 — Audit hooks (runnable)

```bash
# Confirm no repo doc references sending this lens non-genericized content
grep -rn "ox-alpha" docs/adr/ docs/briefs/ 2>/dev/null
# Expected: only this ADR (and, later, any ADR that supersedes it)

# Confirm no repo/tool-access integration was ever wired for this lane (forbidden move #2)
grep -rl "stealth/ox-alpha\|stealth_ox_alpha\|OPENROUTER_API_KEY" scripts/ ops/ core/ lab/ 2>/dev/null
# Expected: empty -- this lane is chat-completions-only, never a repo/tool-access integration

# Calendar trigger reminder
# Re-check at the next quarterly programme audit, and immediately if OpenRouter or independent
# research discloses the provider identity behind stealth/ox-alpha.
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md --type adr
# Expected: exit 0 / no HARD violations

# ADR lifecycle graph -- header fields, edges, cold-store shape, INDEX sync
$ python scripts/check_adr_graph.py
# Expected: exit 0

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%H %ad" --date=short -- .claude/skills/cursor-fleet/SKILL.md
$ git log -1 --format="%H %ad" --date=short -- .claude/skills/task-routing/SKILL.md
$ git log -1 --format="%H %ad" --date=short -- .claude/skills/fable-judge/SKILL.md
$ git log -1 --format="%H %ad" --date=short -- docs/adr/2026-07-14-cc-cursor-surface-allocation.md
$ git log -1 --format="%H %ad" --date=short -- docs/adr/2026-08-14-cc-cursor-autonomous-loop.md
$ git log -1 --format="%H %ad" --date=short -- docs/adr/2026-08-08-adr-ceremony-tiering.md
# Expected: hashes/dates match the §0 anchors above

# Downstream artifact update verification
# n/a -- policy-only, no downstream edits declared in §6
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Initial authoring | Joshua + Claude Code |
| 2026-08-22 | Ratified `Proposed` → `Accepted`; appended non-material evidentiary addendum below (validation-test result) | Joshua + Claude Code |
| 2026-08-22 | **Bounded extension addendum — `Accepted`, operator real-time authorization.** §2 Scope amended narrowly: authorizes ONE sanitized candidate-generation ask (Tradeify eval-strategy-fit constraint), the exact pattern §3/§5 had previously rejected in general form. Does not lift §5's harvest-worker/engineering-assist prohibition generally — a different or repeated ask needs its own authorization. | Joshua (real-time GO in chat, in response to an explicit tradeoff question) + Claude Code (draft + apply) |
| 2026-08-23 | Use 2 of the sanctioned lens recorded (methodology-skill review). Does not amend §2 / §4 / §5. Pointer only. | Cursor Cloud Agent |
| 2026-08-23 | **Merge note (concurrent-session reconciliation).** The two rows above were authored independently by separate concurrent sessions and only discovered each other at merge time. Flagging honestly rather than silently combining: this session (see the second addendum below, and the mechanism-supply-sourcing / "hardest problems" / reformulation-tension asks recorded in `project_tradeify_consistency_payoff_shape_constraint_2026_08_22.md`, memory) made several additional sanitized ox-alpha sends today, some under the original §2 adversarial-lens scope and some under the separately-authorized bounded extension below — **none were logged against the "Use N" counter the other session introduced**, because this session was not aware that convention existed until this merge. The §4 revert trigger ("three consecutive zero-value uses") should not be read as accurately tracked until a full cross-session reconciliation of every actual send this date is done — this row exists so that gap is visible, not silently inherited. | Claude Code (merge-time note) |
| 2026-08-23 | Use N of the sanctioned lens recorded (analog-pin vs inspiration). Does not amend §2 / §4 / §5. Pointer only. | Cursor Cloud Agent |

---

## Addendum 2026-08-22 — Validation test: both seeded ground-truth defects caught blind

**Dated note; does not amend §Decision / §2 Scope / §4 Falsifier.** Evidentiary only — this is
the test that moved §4's H from "plausible argument" to "demonstrated on one artifact" and is
the basis this ADR was ratified same-day rather than left `Proposed`.

**Method.** The real `docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md`
scoping brief is the artifact `feedback_adversarial_review_before_ratification.md` (memory)
documents: a 14-agent adversarial review found 6 BLOCKERs in it, all invisible to
`check_brief.py`'s mechanical 6/6 PASS. Two of the six are pure logic/arithmetic flaws requiring
zero repo context to detect — a double-applied 4x cost multiplier, and an N-basis mismatch
between a full-panel sample-census gate and a downstream in-sample-partition power gate. (The
other four require reading actual cited ADR clauses or verifying actual repo state and are not
fair tests of a context-blind reviewer — they were excluded from this test, not swept under it.)
Both flaws were genericized into one self-contained sanitized excerpt — no real instrument, firm,
dollar figure, or strategy-specific mechanism — and sent with this ADR's own review framing.

**Result.**
- Run 1 ("find the weakest link," singular): caught the multiplier bug exactly — correct
  16x-vs-4x derivation, correct two-layer double-count mechanism, correct downstream-contamination
  reasoning, correct fix. Silent on the second bug, but the prompt only asked for one flaw, so
  this run is uninformative about it either way, not a miss.
- Run 2 (prompt changed to "find ALL independent flaws," same artifact, isolating the one
  variable): caught **both** seeded bugs with correct supporting arithmetic, including deriving
  the N-basis gate's implied 188-event threshold (⌈120/0.64⌉) from a boundary case. It also
  produced 4 further findings of mixed, mostly-unverifiable quality — one landed almost exactly on
  a real, separately-encoded repo principle (own-panel cost-basis recomputation, harvest Req 5,
  per the real brief's own §2.3) despite being an inference beyond the literal sanitized text; one
  is very likely a false positive (treating the standing, ratified 4x cost-law buffer as
  unjustified padding); one is almost certainly an artifact of this test's own sanitization (a
  "missing Gate 2" that only exists because of how the excerpt was abbreviated); one is a
  plausible but unverifiable general point.

**Why this matters for §5, not just §4.** The mixed quality of the "find everything" bonus output
— one real hit, one plausible false positive, one sanitization artifact, indistinguishable
without ground truth — is a live demonstration of exactly the failure mode §2/§5 already guard
against: this lens's output is never a finding until reconciled against the real artifact. This
run is evidence the guard is necessary, not evidence it can be relaxed.

**Full detail, including both raw transcripts:** `project_ox_alpha_openrouter_evaluation_2026_08_22.md`
(memory, battery 4).

---

## Addendum 2026-08-22 (second) — Bounded extension: one candidate-generation ask, Tradeify eval-strategy-fit

**Amends §2 Scope narrowly. Does not touch §4 Falsifier, §0, or the general §5 forbidden-move list
except by carving one explicit, bounded exception into it.** Everything else in this ADR —
sanitization discipline, zero-authority framing, reconciliation-before-finding, the retention/
training-license caveat — stands unchanged and governs this use too.

**Context.** Same-session work quantified (via the real production engine, not estimation) why the
locked Striker book fails a Tradeify-shaped consistency rule: its win distribution is dominated by
rare, large, pyramid-driven days, and a per-day-profit ceiling mathematically requires several
comparably-sized offsetting wins to clear — a payoff-shape problem, not a sizing problem. This sits
on top of an already-documented finding (`project_tradeify_discovery_channels_dry_2026_08_20.md`)
that this repo's own discovery channels are close to fully mined for new mechanisms. §3's original
"Public-mechanism/literature-harvest worker" alternative was rejected on exactly that near-zero-
marginal-leverage ground — but that rejection was about a **standing, general-purpose harvest lane**,
not about one bounded, sanitized ask targeted at a single, freshly-quantified constraint.

**Decision.** Claude Code may send `stealth/ox-alpha` **one** sanitized prompt asking for candidate
strategy-mechanism ideas that would plausibly satisfy the quantified constraint (high win-frequency,
low payoff-skew, non-pyramid-dependent shape, clearing a per-day-profit-share ceiling in reasonable
time under a tight trailing-DD budget) — genericized exactly as every prior sanitized send in this
ADR has been: no real strategy name, parameter, instrument, firm name, dollar figure, or Pine logic.
Output is candidate-objection-grade input only, per §2/§5 above — reconciled against real repo
context before anything is treated as a lead, never wired into any tool/code path, never used to
justify skipping this repo's own pre-registration/K-accounting discipline
(`futures-anomaly-discovery` skill) for whatever, if anything, comes of it.

**Why this is a real extension, not a re-reading of the existing scope.** §2's original text is
"adversarial second-opinion lens on... decision-authoring artifacts" — reviewing something already
drafted. Asking for candidate mechanisms is generative, the pattern §3/§5 named and declined. Calling
this an extension rather than quietly treating it as already-covered is the point of this addendum.

**Bound (what this does NOT authorize).** A second or different candidate-generation ask — a new
constraint, a different firm, a follow-up "give me more ideas" — is **not** covered by this
addendum and needs its own authorization, the same way §5 already required for the general pattern.
This is a one-time, one-constraint carve-out, not a standing lane. Nothing here changes the F1/F3
fork ownership, the ceremony-tiering ADR's rules, or any live-risk surface.

**Authorization record.** Real-time operator GO in chat, 2026-08-22, in direct response to an
explicit question naming the tradeoff (fresh-authorization requirement + the §0 training-license
retention risk already on record in this ADR) and three concrete alternatives (in-scope adversarial
review only / bounded extension / skip ox-alpha) — "Extend scope deliberately" selected.

**Falsifier (of this addendum, distinct from §4 above).** If this bounded-exception pattern is
invoked a second time without a fresh, explicit authorization citing this addendum's own bound
paragraph, that is a violation of this addendum's own terms, not a permitted continuation.

---

## Addendum 2026-08-23 — Use 2: sanitized `futures-anomaly-discovery` skill review

**Dated note; does not amend §Decision / §2 Scope / §4 Falsifier / §5 Forbidden moves.**
Use-count only, so the §4 trigger schedule stays evaluable.

- **Use 1** (production): DL-2 prereg, 2026-08-22 — objections survived reconciliation (axis-coverage imbalance; mechanism-id reuse). Recorded on that prereg, not here.
- **Use 2** (this note): sanitized copy of `.claude/skills/futures-anomaly-discovery` sent to `stealth/ox-alpha` via OpenRouter chat-completions. Reconciliation owner: [`N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md`](../notes/notice/N-2026-08-23-ox-alpha-futures-anomaly-discovery-skill-review.md). Several objections survived, so revert trigger (b) (three consecutive zero-value uses) does not tick. Third-use review still owed.

No transcript is stored in-repo (reasoning-channel dump; sanitization bar). The notice holds the objection table.

- **Use 3** (2026-08-23, this row): sanitized MSL WHO-sourcing-methodology critique, sent under §2 base scope (adversarial lens on the WHO-track sweep + Req 1a admission bar, not the bounded-extension candidate-generation carve-out). Reconciliation owner: [`N-2026-08-23-ox-alpha-msl-who-sourcing-methodology-review.md`](../notes/notice/N-2026-08-23-ox-alpha-msl-who-sourcing-methodology-review.md). Every objection concrete enough to name a specific already-tried mechanism (macro-print-on-index, index-roll/reconstitution, gamma-sign-from-OI, crude margin-call substitution) did **not** survive reconciliation — each was already tested and killed internally, several on sharper grounds than the objection assumed. Five more abstract/methodological threads (SPAN+COT-signed liquidation cascades, compelled-abstention mechanisms, an impact-persistence reframing of the size screen, bounded-duration-compulsion as a payoff-shape selection heuristic, a pre-G0 rule-feasibility Monte-Carlo simulator) remain open and unrefuted. Revert trigger (b) (three consecutive zero-value uses) does not tick — real objections survived.
- **Use 4** (2026-08-23): sanitized mechanism-supply **candidate-generation** ask — the second invocation of the bounded-extension pattern, made under a **fresh, explicit operator authorization given in chat this date** (*"offer the mechanism supply question to ox-alpha. Sanitize while giving it the context it needs"*), recorded here citing the second addendum's own Bound paragraph as that paragraph requires. Prompt carried the Use-3 reconciliation outcomes (dead classes + actual kill reasons) so dead ground was not re-suggested. Output: 11 candidates drafted, 7 self-refuted by the model before answering, 4 returned with self-refutations + $0 kill scripts; the Use-3 SPAN+COT cascade thread **conceded dead by its own proposer** ("nothing converts it — demote to filter"). Reconciliation owner: [`N-2026-08-23-ox-alpha-mechanism-supply-candidates.md`](../notes/notice/N-2026-08-23-ox-alpha-mechanism-supply-candidates.md) — one candidate (MOC-imbalance wake) converges with the estate's own named free supply route, one (buyback-blackout abstention) is genuinely novel, one confirms existing registry kills, one dies against F3's cost precedent at micro sizing. Revert trigger (b) does not tick. A third candidate-generation ask needs its own fresh authorization, same as this one did.

**Concurrent-session note (added at merge, 2026-08-23):** this "Use N" ledger and the second
addendum above were authored independently by separate sessions with no cross-visibility until
merge. This session made additional sanitized ox-alpha sends today under both the original §2
scope and the bounded extension above that are **not** reflected in the Use 1/Use 2 count —
see the Change history row dated 2026-08-23 ("Merge note") for the explicit gap disclosure. Do
not treat Use 1/Use 2 as a complete count of this date's activity without a fresh reconciliation
sweep.

---

## Addendum 2026-08-23 — Use N: sanitized analog-pin vs inspiration consult

**Dated note; does not amend §Decision / §2 Scope / §4 Falsifier / §5 Forbidden moves.**
Use-count only, so the §4 trigger schedule stays evaluable.

One sanitized governance question (when an external-framework analog should become a standing
pin versus remaining disposable inspiration) was sent to `stealth/ox-alpha` via OpenRouter
chat-completions. No vendor, product, repo, or operator identifiers. Reconciliation owner:
[`N-2026-08-23-ox-alpha-analog-pin-vs-inspiration.md`](../notes/notice/N-2026-08-23-ox-alpha-analog-pin-vs-inspiration.md).
Several objections survived, so revert trigger (b) (three consecutive zero-value uses) does
not tick.

No transcript is stored in-repo (sanitization bar). The notice holds the objection table.

The Use-N ledger remains incomplete across concurrent sessions — see the Change history
merge note. This row does not claim to be Use 3 of a complete series.

---

## Addendum 2026-08-23 — Use N: sanitized review of three hard-decision judgment calls (Phase A / §4 firm-repair)

**Dated note; does not amend §Decision / §2 Scope / §4 Falsifier / §5 Forbidden moves.**
Use-count only, so the §4 trigger schedule stays evaluable.

Sent under §2's **base scope** (adversarial lens on reasoning/judgment calls, not the
candidate-generation extension) at operator direction ("send the hardest decision elements to
ox-alpha, generalized with enough context to be useful"). Three scenarios genericized past
recognition — no firm name, instrument, dollar figure, percentage, or internal naming. Full
sanitization statement, reconciliation table, and audit hooks:
[`N-2026-08-23-ox-alpha-phase-a-firm-repair-hard-decisions-review.md`](../notes/notice/N-2026-08-23-ox-alpha-phase-a-firm-repair-hard-decisions-review.md).

Notable: one high-value, concrete objection (a possible day-1 scorer-semantics bug in a
consistency-rule check) was independently checked directly against the real production engine
(`core/mc/simulation.py:186-196`) and against real historical pass evidence, and does **not**
survive — a rare case where reconciliation affirmatively clears an objection rather than just
filtering it. Several other objections survive as open, actionable follow-ups. Revert trigger
(b) (three consecutive zero-value uses) does not tick.

No transcript of the hidden-reasoning channel is stored in-repo (sanitization bar).
