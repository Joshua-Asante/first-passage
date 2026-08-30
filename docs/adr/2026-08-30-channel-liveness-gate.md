# Channel-liveness gate — every sourcing channel declares a reachable attempt/session ceiling at open — `channel-liveness-gate`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-30; see Ratification note.
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Layer:** methodology (sourcing-channel doctrine only). No `dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue action; no spend.
**Tier:** full — Limb 4 fires (creates standing doctrine binding every future channel-opening artifact).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/adr/2026-08-24-sourcing-phase-channel-retirement.md` — anchor `340722c` (verified `git log -1` 2026-08-30). Retires Route B in full: "4 campaigns opened at G0... and 0/4 ever reached the confirm stage." §0/§1: the operator's retirement decision was "0-for-4... sufficient regardless of the un-tripped falsifier" — the governing ADR's own §4 falsifier required "two completed Route B confirm campaigns that printed RESOLVED on CONFIRM," a state that, with zero campaigns ever reaching Confirm, could structurally never fire.
- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` — anchor `340722c`. Clause 2-B (§2, verbatim): ratified structural-flow-census as a sourcing channel; its Addendum 2026-08-24 records: "zero seeds passed the §3 intake screen across all 4–5 census passes (2026-07-26 → 2026-08-01), satisfying 2-B's own falsifier — the operator elected to act on this now rather than wait for the formal second-quarterly-audit check date (2027-02-08)." This is the one channel in the estate that already carried a working, reachable liveness bound, and it fired as designed.
- `docs/methodology/strategy_harvest.md` — anchor `936eb0f` (2026-08-29). §2.3 ranked channel portfolio (ranks 1–6, the retired 1-tie census row) carries no standing *requirement* that any rank declare an attempt/session ceiling at open in a uniform shape — but as the five reads below establish, every live channel already has *some* consecutive-failure or calendar-bound clause, independently invented in its own ratifying ADR, in five different shapes and vocabularies.
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` — anchor `e11fd39` (2026-08-24). §6 precedent for policy-binds-now/code-may-lag ADRs: "Optional later: mechanical `register_search open` guard (separate implementation handoff — doctrine binds now; code may lag)." **Also carries its own dated ceiling**, missed in this ADR's first draft: §4's verdict vocabulary is `RESOLVED` (≥1 of the first two intake-class closures confirms OOS), `FALSIFIED` (per its own revert trigger), or **`AMBIGUOUS` if no intake-class campaign closes by 2026-11-08** — a reachable, calendar-denominated ceiling, never run through `gate-reachability-audit`.
- `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` — anchor `e11fd39`. **Already carries a ceiling**, missed in this ADR's first draft: step 6, "Lane stop-rule (amended 2026-08-16): 3 consecutive FALSIFIED-or-zero-yield mechanisms on this universe → a lane-review packet to the operator (SNAG discipline), never a 4th campaign by default. A close resets the streak only if it yields an admitted candidate." A reachable, yield-unit-denominated ceiling — but its named consequence ("a lane-review packet") is neither of this ADR's two options (automatic retirement / mandatory redesign) as stated, and it has never been run through `gate-reachability-audit`.
- `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` — anchor `e11fd39`. **Already carries a ceiling**, missed in this ADR's first draft: per `2026-08-14-msl-yield-falsifier-survival-limb.md`'s own header (next bullet), the base charter's `FALSIFIED(process)`/`FALSIFIED(yield)` clauses (6 consecutive pre-G0 deaths across ≥2 families / 12 calendar weeks zero G0) predate this ADR entirely.
- `docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md` — anchor `103b084` (2026-08-14), found via this ADR's own Phase-2 sweep (§7), not cited in the first draft. Amends the MSL charter's existing falsifier (above) with a two-rung ladder: Rung A (soft) at 6 consecutive G0-freezes-without-Pine → mandatory Board review (not a close); Rung B (hard) at 10 consecutive freezes with zero TNEC-1 survivors, or 8 calendar weeks from 2026-08-12 (≈2026-10-07) with ≥4 freezes and zero survivors. Reachable, dual-yield-unit, but Rung A's consequence ("Board review of the explore-stage screen calibration") is again neither of this ADR's two named options, and neither rung has been run through `gate-reachability-audit`.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` — anchor `e11fd39`. **Already carries two ceilings**, missed in this ADR's first draft: the channel's own §4 (`AMBIGUOUS-HOLD`, re-test 2027-02-08, if zero sourced candidates by 2026-11-08) and its 2026-08-15 addendum — "N = 3 consecutive countable pre-G0 kills ⇒ the channel reports generation-dry at the next quarterly programme audit" (D-K1's declared-K-ceiling, K ≤ 3, is a per-search cap, a different mechanism from a liveness ceiling, and not conflated here). Neither the pre-G0 N=3 clause nor §4's date has been run through `gate-reachability-audit`, and "reports generation-dry" is, again, neither of this ADR's two named consequences.
- `docs/adr/2026-08-16-deep-iteration-lane-charter.md` — anchor `e11fd39`. **Already carries the most complete existing ceiling of the five**, missed in this ADR's first draft: an Inertness limb (no lane-campaign prereg frozen within 6 weeks of acceptance, or by 2026-11-08 → demote to `Superseded` absent a re-election) and a Yield limb (2 consecutive completed campaigns whose survivor fails confirm/N-SURV ⇒ `FALSIFIED`, supersede) — the Yield limb's consequence (supersession) is the closest existing match to this ADR's "mandatory redesign" option, but it too has never cleared `gate-reachability-audit`.
- `docs/adr/2026-08-22-grow-lane-build-authorization.md` — anchor `e11fd39`. GROW-lane build authorization, titled "deep-iteration-lane tooling packet" — tooling within the deep-iteration lane, not a separately-chartered channel; not double-counted in this ADR's channel list.
- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` — anchor `e11fd39`. Rule 2 (budget-before-acting) binds per-task iteration budgets at a finer granularity than channel-open; confirmed no conflict — this ADR operates one level up (channel, not task).
- `docs/methodology/avenue_a_generate_confirm.md` — anchor `340722c`. Route B's own withdrawn G0/C0 checklist; confirms the Stage-6 Confirm definition this ADR's discussion of yield bars refers to.
- `lab/discovery/register_search.py` — anchor `e11fd39`. `open_run()` (lines 640–714) registers per-**campaign** K/α/window/hypothesis/lane; the manifest schema has no channel-identifying field. A channel-level ceiling cannot be mechanically enforced by this module today without a schema addition — confirms the policy-first, code-optional design below.
- `discovery_manifests/README.md` + `discovery_manifests/*.json` — anchor `e11fd39` / read this session. 20 manifests total; channel attribution today is by directory-naming convention and free-text `hypothesis`/`params` fields only, not a queryable field — small enough for a manual periodic audit hook.
- `.claude/workflows/gate-reachability-audit.js` — anchor `e11fd39`. Existing workflow audits "every gate in a prereg/G0/lane-spec for reachability AND bindingness before freeze," already scoped to accept a "lane-spec/charter doc" as its target — the natural check for a channel's liveness-ceiling clause once one is written.
- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). The interpretive note this ADR formalizes (tension 8 and the "Add one channel-liveness gate" row); per its own header, the note "changes no gate, threshold, lifecycle state, venue binding, or deployment authority" — this ADR is what gives its recommendation binding effect.

**Amendment-first / dedup (Rule 8 sub-rule 10), run at ratification:**

```
$ python scripts/check_advisor_dedup.py --keywords "channel liveness ceiling reachable attempt bound sourcing channel retirement redesign"
```

105 candidates surfaced, all keyword-overlap noise from unrelated audit notes and instrument ledgers (`ops/instruments/MNQ.md`, programme-audit diagnostics) — none is a competing decision artifact. No existing ADR or brief performs this ADR's channel-liveness-ceiling requirement.

---

## §1 — Context

Route B's governing ADR carried an empirical falsifier — "two completed
confirm campaigns that printed RESOLVED on CONFIRM" — that could only fire
from a state the channel itself had to reach first. Because the channel's
own generate/confirm firewall never let a campaign reach Confirm (0-for-4
across its entire life), the falsifier sat structurally unreachable for the
channel's whole existence: the process could keep producing honest nulls
without the designed check ever being able to rule on whether the two-stage
mechanism was working. Retirement happened anyway, but as an ad hoc
operator override ("0-for-4... regardless of the un-tripped falsifier"),
not the designed gate firing — the exact failure mode a *reachable*
process-level falsifier exists to prevent.

Clause 2-B (structural flow census) is the cleanest worked example: it
declared a bound measured in the channel's own meaningful yield unit — zero
seeds clearing the §3 intake screen by the second quarterly audit — and it
fired correctly, the operator retiring the channel on the clause's own
terms, ahead of its calendar deadline, with no override needed. **This
ADR's first draft read that as the sole existing precedent, against five
live channels carrying no ceiling at all — a premise this ADR's own
Phase-2 sweep (§7) found false.** Every one of the five live channels
(HARV, dense-1m/TNEC, MSL, no-counterparty-statistical/geometric, and
deep-iteration — GROW-lane tooling is inside deep-iteration, not a sixth
channel) already carries at least one consecutive-failure or calendar-bound
clause, in its own ratifying ADR or charter (§0). The actual gap is
narrower than "no ceiling exists," and three-fold instead: **(1)**
inconsistent named consequences — a lane-review packet, a mandatory Board
review, a generation-dry report, a supersession, an `AMBIGUOUS-HOLD` — none
of which map cleanly onto a single two-option taxonomy (retirement or
redesign) a reader could audit uniformly across channels; **(2)** none of
the five existing clauses has ever been run through the
`gate-reachability-audit` UNREACHABLE/UNBINDING check this ADR requires;
and **(3)** nothing requires a *future* channel to carry one at all — each
of the five existing clauses was independently invented by its own
authoring session, not derived from a portfolio-wide rule.

**Decision driver (one sentence):** every live channel already has some
shape of consecutive-failure or calendar-bound clause, invented
independently in five different forms and never checked against a common
reachability/bindingness standard or a closed consequence taxonomy — and
nothing requires a future channel to carry one at all.

---

## §2 — Decision

**Decision:** Every sourcing channel's founding charter — an ADR, a
methodology-doc §2.3 portfolio row, or a ratified spec, whichever artifact
currently or henceforth defines the channel — must declare, at channel-open,
a **reachable liveness ceiling**: a bounded count of unsuccessful attempts,
measured in a yield unit the channel's own charter names (e.g., admissible
seeds clearing intake screen, campaigns reaching Stage-6 Confirm, or an
equivalent), and/or a bounded elapsed-time horizon (e.g., N quarterly
programme-audit cycles). Reaching the ceiling without a qualifying yield
event triggers exactly one of two consequences, named at declaration time
alongside the ceiling itself: **(a) retirement** — no further campaign
opens under the channel absent a fresh ratifying ADR — or **(b) mandatory
redesign** — a superseding ADR must state what changed in the design before
a new campaign opens. **Neither consequence is self-executing** (§5):
reaching the ceiling makes the pre-declared consequence *due*, not
automatically enacted — enactment still runs through the same operator
GO/ratifying-ADR mechanism as any other channel-level decision. "Retirement"
in option (a) names *which* consequence was pre-declared, foreclosing
re-litigation of that choice at fire time; it does not mean the ceiling
enacts itself in code. The ceiling is itself subject to the
gate-reachability-audit's UNREACHABLE/UNBINDING taxonomy before the
channel's charter may be marked ratified: a ceiling that cannot fire within
the channel's realistic operating envelope, or one that fires but the
campaign choreography never consults, fails this ADR's requirement the same
way either failure mode fails a candidate-level gate.

**Reconciliation of the five existing clauses (§0/§1).** Each of the five
live channels already carries a consecutive-failure or calendar-bound
clause, but none was authored against this standard. Each is owed a dated
reconciliation addendum on its own owning artifact (never a rewrite here,
per amendment-first discipline, §5) that: **(i)** runs the existing clause
through `gate-reachability-audit`; **(ii)** maps its existing named
consequence onto exactly one of this ADR's two options — a mapping, not a
new invention, since four of the five already have a real-world consequence
to classify (dense-1m/TNEC's lane-review packet and MSL's Rung-A Board
review are closest to "mandatory redesign" in effect — a forced look before
any new campaign proceeds unchanged; deep-iteration's Yield-limb supersession
and no-counterparty-statistical's generation-dry report are closest to
"retirement" in effect for their own channel) or, where no existing
consequence fits either option cleanly, states that explicitly and adds one;
**(iii)** does not change the existing clause's own numeric bound or yield
unit — this ADR reconciles form, never re-derives a calibrated number
(§5). No existing clause is edited by this ADR itself.

**Effective:** immediately upon acceptance, for any channel charter authored
or amended after this date, and for the reconciliation addenda above.
**Scope:** channel-level sourcing doctrine only — the five live channels
named in §1 (HARV, dense-1m/TNEC, MSL, no-counterparty-statistical/
geometric, deep-iteration) and any future channel — never campaign-level
K/multiplicity accounting, which stays governed by each campaign's own
pre-registration. Does **not** retroactively invent a ceiling number for
any currently-open channel (each already has one, §0) and does **not**
itself edit any of the five existing clauses; see §5.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Status quo — leave each channel's existing clause exactly as authored, in its own shape | Route B is the negative case that had none at all, and its own designed falsifier structurally could not fire. The five live channels are a different failure mode from Route B's: each already has a clause, but in five inconsistent shapes/vocabularies, none audited for reachability/bindingness — status quo leaves that inconsistency and the missing audit pass uncorrected. |
| Mandate one universal ceiling number/unit for every channel | Channels operate at incompatible granularities — structural-flow-census consumed zero K per pass and could run cheaply and often; a mechanism-first HARV campaign spends real data/K per attempt. A single number is toothless for cheap channels or prematurely fatal for expensive ones. Per-channel-declared (this ADR) preserves calibration while still requiring a common consequence taxonomy and an audit pass. |
| Rewrite the five existing clauses' own numeric bounds/yield units inside this ADR | Would re-derive calibrated numbers a prior authoring session already set against that channel's real operating envelope, without this ADR having done the review work those sessions did — risking exactly the UNREACHABLE or UNBINDING failure this ADR exists to prevent, and doing it by fiat. Each channel's own owning artifact gets a reconciliation addendum instead (§2/§5) that maps and audits, never re-derives. |
| Mandate "reaches Stage-6 Confirm" as the universal yield unit | The cleanest bar, and the one Route B itself used — but a zero-K screening channel (structural-flow-census) never reaches a K-bearing campaign at all until *after* its own intake screen; a Confirm-only yield bar would make such a channel's ceiling structurally unreachable by construction, reproducing this ADR's own target defect. The charter names its own meaningful yield unit instead. |
| Build the mechanical `register_search.py --channel` guard now, as a precondition for accepting this ADR | `open_run()`'s manifest schema has no channel field today (§0); adding one is a real schema change. `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` §6 sets the estate's own precedent for this exact shape of decision — doctrine binds immediately, code is optional and separate. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** a per-channel, charter-declared liveness ceiling,
checked for reachability/bindingness at ratification, catches the
Route-B-shaped failure (a channel producing honest nulls indefinitely while
its own success falsifier stays unreachable) without prematurely retiring a
channel that is working slowly but validly.

**Revert trigger:** at the next scheduled quarterly programme audit
following any channel's ceiling first firing (retirement or redesign
triggered), if a gate-reachability-audit pass on that ceiling finds it was
itself UNREACHABLE (could not have fired within any realistic operating
envelope for that channel) or UNBINDING (fired, but a campaign opened under
the channel after the fact regardless) — **or** if any channel's fired
ceiling requires an ad hoc operator override to actually retire or redesign
the channel, reproducing Route B's own bypass of its designed gate — this
ADR is revoked.

**Revert action:** author a superseding ADR that either strengthens
enforcement (mandates the `register_search.py --channel` mechanical guard
rather than leaving it optional) or narrows this ADR's scope. Never silently
edit this ADR's decision text.

**Trigger check schedule:** every quarterly programme audit (next:
2026-11-08, per the standing radar cadence, `strategy_harvest.md` §2.4).

---

## §5 — Forbidden moves (under this ADR)

- **Rewriting any of the five live channels' (§1) existing numeric bound or
  yield unit inside this ADR, or inside its own dated addendum, to make the
  doctrine look immediately complete.** Ruled out in §2/§3: a number picked
  or edited without redoing the real-operating-envelope review a prior
  authoring session already did risks landing UNREACHABLE or UNBINDING,
  which is worse than an acknowledged gap — it manufactures a false sense
  that the gap is closed. Reconciliation maps and audits the existing
  number; it does not re-derive one (tracked as an owed STATE.md row, §6).
- **Treating an existing channel's consecutive-failure or calendar-bound
  clause as automatically satisfying this ADR without running it through
  `gate-reachability-audit` or mapping its consequence onto one of the two
  named options.** Ruled out in §2 — existence of *some* clause is not the
  same as reachability, bindingness, or a closed consequence taxonomy; the
  reconciliation addendum is required precisely because a nominal-looking
  ceiling can still be UNREACHABLE, UNBINDING, or resolve to a consequence
  outside this ADR's two-option taxonomy.
- **Mandating "reaches Stage-6 Confirm" as the sole permitted yield unit.**
  Tempting because it is the rigorous bar Route B itself used — ruled out
  because it would make a zero-K screening channel's ceiling structurally
  unreachable by construction (§3), the exact defect this ADR targets.
- **Editing `strategy_harvest.md` §2.3's ranked-channel table rows directly
  to add ceiling numbers as part of this ADR's own implementation.**
  Amendment-first discipline requires each channel's *owning* artifact
  (its own ratifying ADR or spec) to carry its addendum, not a summary
  table maintained elsewhere — editing only the table would create the
  source-of-truth fracture Rule 6's skew-audit exists to catch. §2.3 gains
  only a pointer to this ADR's requirement, not per-row numbers.
- **Treating a fired ceiling as self-executing.** A fired ceiling means the
  pre-declared consequence is now *due*, not automatically applied without
  a human decision — retirement or redesign still requires an operator
  GO/ratifying ADR, consistent with every other automated-de-risk /
  human-gated-risk-adding asymmetry already standing in this repository's
  authorization axis.

---

## §6 — Consequences

**Positive consequences:**
- Closes the specific gap Route B's retirement diagnosed: a channel whose
  own success falsifier depends on a state the channel may never reach.
- Generalizes a pattern (clause 2-B, and the five already-independently-
  invented clauses this ADR's own sweep surfaced) into one closed
  consequence taxonomy and one mandatory audit pass, rather than leaving
  five inconsistent shapes uncompared.
- Requires no K or data spend to satisfy — structural-flow-census's own
  precedent, and the five existing clauses' own history, show a working
  liveness bound can be zero-K.
- Gives `gate-reachability-audit` a new standing class of gate (channel
  ceilings, not only campaign-level pre-registration clauses) to check —
  and a concrete backlog of five to run it against immediately.

**Negative consequences (real cost, not theatrical):**
- Every future channel-opening ADR or spec now carries additional authoring
  work: picking a yield unit, a bound, and a named consequence, and
  defending both against the reachability/bindingness audit before
  ratification.
- The five currently-open channels' existing clauses now carry an
  acknowledged reconciliation debt (mapping + audit, not fresh authoring)
  until their addenda land — named explicitly here rather than hidden by a
  retrofit (§5).

**Risks (probabilistic, distinct from costs):**
- A badly-calibrated per-channel ceiling — too loose is toothless, too
  tight retires a slow-but-real channel — is a real risk. §4's falsifier
  catches it, but only at the *next* quarterly audit after first firing:
  one bad retirement or redesign can occur before the mechanism
  self-corrects.

**Downstream artifacts that need updating:**
- `docs/methodology/strategy_harvest.md` §2.3 — one new paragraph above the
  ranked-channel table stating the requirement and pointing to this ADR;
  no per-row edits (§5).
- `STATE.md` — new forward-board row: HARV / dense-1m-TNEC / MSL /
  no-counterparty-statistical-geometric / deep-iteration each owed a dated
  reconciliation addendum on their own owning artifact (gate-reachability-
  audit pass + consequence-taxonomy mapping) — not a fresh ceiling, each
  already has one (§0).
- `.claude/workflows/gate-reachability-audit.js` — no code change required
  (already scoped to lane-spec/charter targets, §0); exercise it against
  each channel's addendum once written.
- `lab/discovery/register_search.py` — optional, separate implementation
  handoff for a mechanical `--channel` guard (§7); not required for
  acceptance.

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time (`git log -1`
  on each cited file).
- **Phase 1** — add the requirement paragraph to `strategy_harvest.md` §2.3
  (above the ranked-channel table), citing this ADR by filename.
- **Phase 2** — grep-sweep, two limbs (Known Trap #7): **(i)** no
  predecessor to check (`Supersedes: none`); **(ii)** consumers of
  channel-opening vocabulary — `grep -rl "register_search open\|sourcing
  channel\|channel portfolio\|lane charter" docs/adr/ docs/spec/
  docs/methodology/`, run this session, confirmed the full list of
  channel-shaped artifacts owed a reconciliation addendum: HARV
  (`2026-07-15-external-mechanism-harvest-intake.md`), dense-1m/TNEC
  (`2026-08-09-dense1m-entry-mechanism-lane-spec.md`), MSL
  (`2026-08-12-msl-manual-sourcing-loop-charter.md` +
  `2026-08-12-msl-sourcing-channel-ratification.md`), no-counterparty
  statistical/geometric (`2026-08-15-no-counterparty-statistical-sourcing-channel.md`),
  and deep-iteration (`2026-08-16-deep-iteration-lane-charter.md`; GROW's
  build-authorization ADR is tooling inside this lane, not a sixth
  channel). Every other hit (CON-5's cheap-falsifier gate, the S6 K-aware
  generation spec, the ambiguous-hold null-run-threshold ADR, this ADR
  itself, `docs/adr/INDEX.md`) is dispositioned as *not* a channel charter —
  each is either a scoping rule inside an existing channel, cross-lane
  infrastructure, or the graph index — and needs no addendum. **A closer
  read of each of the five owning artifacts (not just the grep hit list)
  found this ADR's first draft had wrongly asserted all five carry no
  ceiling at all — every one already has a consecutive-failure or
  calendar-bound clause (§0/§1). Corrected throughout before finalizing;
  the reconciliation-addendum framing (§2) replaces the original
  fresh-authoring framing.**
- **Phase 3** — add the STATE.md forward-board row (§6); verification block
  executes; status → `Accepted`.

Mechanical `register_search.py --channel` enforcement is an **optional,
separate implementation handoff** — doctrine binds now; code may lag, per
the HARV-lane precedent (§0).

---

## §10 — Audit hooks (runnable)

```bash
# Which channel charters still lack a RECONCILIATION addendum citing this
# ADR? Each of the five already has its own pre-existing ceiling clause
# (§0) -- this checks for the mapping/audit addendum, not a fresh ceiling.
# Expected at ratification: all five print (none reconciled yet) -- each
# is a STATE.md-tracked owed item, not a gap in this ADR.
grep -L "channel-liveness-gate" \
  docs/adr/2026-07-15-external-mechanism-harvest-intake.md \
  docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md \
  docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md \
  docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md \
  docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md \
  docs/adr/2026-08-16-deep-iteration-lane-charter.md

# §2.3 carries the pointer paragraph, not per-row ceiling numbers
grep -n "channel-liveness-gate" docs/methodology/strategy_harvest.md

# Coarse manual channel-attempt cross-check (until register_search.py gains --channel)
ls discovery_manifests/*.json | wc -l

# §4 trigger check -- re-run at each quarterly programme audit against any
# channel whose ceiling fired since the last audit. Invoked as a Workflow
# call (gate-reachability-audit.js is a workflow script, not a Python
# module -- there is no `python -m` form):
#   Workflow({ name: "gate-reachability-audit", args: { targetPath: "<channel charter>" } })

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-channel-liveness-gate.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/adr/2026-08-24-sourcing-phase-channel-retirement.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md
$ git log -1 --format="%h %ci" -- docs/methodology/strategy_harvest.md
$ git log -1 --format="%h %ci" -- lab/discovery/register_search.py

# Downstream artifact update verification (post Phase 1-3)
$ grep -n "channel-liveness-gate" docs/methodology/strategy_harvest.md STATE.md
```

---

## Ratification note

**Ratified by:** Joshua, direct instruction ("ratify the six ADRs," 2026-08-30), following a
self-conducted adversarial re-read (the full 6-lens Workflow panel was declined for cost) that added
the missing amendment-first/dedup attestation (§0) and confirmed no other correction was owed.

**§6-class preconditions at ratification:** mechanical checks clean (`check_brief.py` 0 HARD,
`check_adr_graph.py` OK) ✓ · amendment-first dedup run, no genuine prior art ✓ · the Codex review
round's 3 findings on this file (false "no channel has a ceiling" premise, the "automatic retirement"
self-execution contradiction, the workflow-invocation syntax) verified already fixed in this file's
current text ✓.

**Not licensed by this ratification:** authoring any of the five channels' owed reconciliation
addenda (each channel's own owning artifact, separately, per §2/§5) · building the mechanical
`register_search.py --channel` guard (§7, optional, separate handoff) · any edit to `core/`, `ops/`,
`dd_protection`, or allocations.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
| 2026-08-30 | Ratified — status → `Accepted` | Joshua (operator ratification) |
