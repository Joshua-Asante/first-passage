# ADR 2026-08-21 — CFO subscription-ledger consolidation: one ledger, a required-field gate, a monthly reconfirm cadence

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-21, in-session direct instruction
("I want to implement 1-4, reconfirm ledger once a month"), following the CFO persona's own
2026-08-21 recommendations (`docs/personas/cfo-log.md`). See Ratification note.
**Decision date:** 2026-08-21
**Authors:** Joshua + Claude Code
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [persona hierarchy narrowing](2026-08-21-persona-hierarchy-front-office-only.md) (`Superseded`
2026-08-31 — was `Accepted` at this ADR's authoring: the ADR that kept the CFO seat live specifically
because spend-disposition judgment doesn't reduce to a mechanical gate the way retired seats did; this
ADR was that seat exercising exactly that judgment, before the 2026-08-31 full persona retirement) · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (limb 4 fires — see §0) ·
`docs/personas/cfo-log.md` 2026-08-21 entries (the C-1 closure that surfaced this gap, and this
decision's own source recommendations; file deleted in the 2026-08-31 persona-hierarchy full
retirement — see [`docs/adr/2026-08-31-persona-hierarchy-full-retirement.md`](2026-08-31-persona-hierarchy-full-retirement.md))
**Layer:** meta-process (a gate/convention over the pursuit-registry and persona-charter surfaces).
**$0 / K=0.**
**Loop-of-Record:** STRATEGIC — creating a standing gate and amending a persona charter both bind
future work at the same class as other meta-process ADRs this repo already carries (e.g. the persona
hierarchy narrowing, same day).

---

## §0 — Rule 0 reads (this worktree, 2026-08-21)

- `docs/personas/cfo-log.md` — anchor `412efa1` (2026-08-21, `git log -1 --oneline`). Read in full,
  including both 2026-08-21 entries: the C-1 closure (four numbered recommendations) and the d17
  ratification entry.
- `docs/pursuits/d11-tradingview-subscription.md` through `d17-claude-max-subscription.md` (7 files)
  — anchor `412efa1` (2026-08-21). Read in full; current Survive-bound text confirmed to be exactly
  what the companion handoff brief's §2 Step 2.2 quotes as "old text."
- `scripts/check_pursuit_records.py` — anchor `412efa1` (2026-08-21, unchanged since). Read in full.
  Confirmed: WARN-tier, report-only, exit-0 severity philosophy stated explicitly in its own module
  docstring ("Default every limb to WARN / report-only... gate composition is owned by
  `scripts/gates.yml`... Wiring is an operator decision, proposed in the landing report, not landed
  here") — this ADR's D2 follows that same philosophy, does not escalate it.
- `docs/personas/cfo.md` — anchor `412efa1` (2026-08-21). Current charter read in full; `Writes:` field
  currently names only `docs/personas/cfo-log.md`.
- `STATE.md` § Scheduled forward triggers — anchor (this session, pre-edit). The existing
  "Weekly — recurring" subsection (venue idle-clock obligation) read in full as the structural
  precedent this ADR's D3 mirrors for a monthly cadence, including the note that the operator's own
  local `daily-repo-truth-sync` scheduled task already reads this section for near-term obligations —
  confirmed via `docs/adr/2026-08-14-cc-cursor-autonomous-loop.md` §0's citation of
  `C:\Users\joshu\.claude\scheduled-tasks\daily-repo-truth-sync\SKILL.md` as live precedent.
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor confirmed current. **Tier test applied
  directly:** limb 1 (spends K/money) — no, $0/K=0. Limb 2 (live-risk surface) — no, no
  `dry_run`/M1/arming/DD-constant touch. Limb 3 (LOCKED surface) — no. **Limb 4 (creates or amends
  doctrine: a rule, gate, or convention binding future work) — fires**: D2 adds a new mechanical gate
  limb to `check_pursuit_records.py` and D3 amends `docs/personas/cfo.md`'s own charter (a governed
  persona file, per `scripts/check_personas.py`'s REQUIRED_FIELDS enforcement). One limb firing is
  sufficient; per that ADR's own escalation rule, this is full-tier, not light.
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` + `.claude/skills/cursor-fleet/SKILL.md` —
  both read in full this session (see the companion handoff brief's own §0). Routing test applied:
  the ledger-creation + pursuit-record-edit + checker-extension work is mechanical, spec-freezable,
  and clears 9 files (well above the ~3-file/1-hour threshold) — routed to a single Cursor handoff
  (`docs/briefs/handoffs/2026-08-21-cc-handoff-subscription-ledger-consolidation.md`), not fleeted
  (only one genuinely disjoint, threshold-clearing packet exists; fleet overhead is waste at N=1 per
  the skill's own routing table). This ADR itself, `STATE.md`, and `docs/personas/cfo.md` stay CC-solo
  — locked surfaces under that ADR's §2 test 1, full stop, no exception.

---

## §1 — Context

The CFO's own 2026-08-21 C-1 closure (`docs/personas/cfo-log.md`) named the root mechanism behind a
12-day-open, explicitly-tagged gap: no forcing function existed. The tag sat visible in six (now
seven) pursuit records without anything making it come back into view. The CFO's memo named four
fixes: (1) one consolidated ledger instead of per-row tags, (2) a required ledger-pointer field at
row-creation time, (3) a standing proactive trigger instead of passive waiting, (4) treating
unprompted disclosure as a design smell. The operator ratified implementing all four, with the
trigger cadence set to monthly.

**Decision driver (one sentence):** the CFO's own diagnosis is already correct and already on
record; this ADR is the mechanical follow-through the operator just authorized, not a fresh
investigation.

---

## §2 — Decision

**D1 — One consolidated ledger.** `docs/pursuits/SUBSCRIPTION_LEDGER.md` becomes the canonical
source for every d11–d17 $/mo figure (Rule 7: one canonical owner, everyone else links). Each of the
seven pursuit records' Survive-bound field is re-pointed to it instead of restating the number
inline. Content and exact per-file edits are frozen in the companion handoff brief (§7 below);
execution is delegated to Cursor, not performed in this commit.

**D2 — Required ledger-pointer field, mechanically checked.** `scripts/check_pursuit_records.py`
gains a fifth limb, `ledger-pointer`: any KEEP-standing pursuit record whose Class is `(d) meta-belt
(subscription)` or `(d) meta-belt (venue account)` must reference `SUBSCRIPTION_LEDGER.md`
somewhere in its body, or the check flags it. **WARN-tier, report-only, exit 0** — identical severity
to every existing limb in that script; this ADR does not escalate the script's own severity
philosophy. This closes the CFO's recommendation #2 (make $/mo a required field at row-creation
time, not backfillable) for the one class of pursuit record it applies to; it is not a general
required-field mandate across all pursuit classes.

**D3 — Standing monthly trigger.** Two mechanisms, not one, matching the CFO's recommendation #3
("give this seat an actual trigger instead of passive waiting"):
- `STATE.md` § Scheduled forward triggers gains a "Monthly — recurring" subsection, structurally
  identical to the existing weekly venue-idle-clock subsection: next deadline **2026-09-21**, rolled
  forward each occurrence, read by the operator's own existing local `daily-repo-truth-sync`
  scheduled task (no new infrastructure — reuses the radar that already reads this section, per §0).
- `docs/personas/cfo.md`'s charter gains one line: the CFO checks `SUBSCRIPTION_LEDGER.md`'s
  "Last confirmed" dates whenever spawned for **any** reason, not only when consulted about spend —
  matching recommendation #3's second half. `Writes:` field gains `docs/pursuits/SUBSCRIPTION_LEDGER.md`
  alongside the existing `cfo-log.md`.

**D4 — Practice norm, no artifact.** Recommendation #4 ("treat unprompted disclosure as a design
smell, not a lucky break" — any $/mo mentioned in-session updates the ledger same-session) is
recorded here as a standing practice, not built as tooling. Per this ADR's own §5 and the CFO's Rule-2
§5 forbidden-move #6 (no telemetry subsystem), no hookify rule or automation is created for this.
If a hookify one-liner later earns its keep after D1–D3 are live, it needs its own decision, not a
default extension of this one.

**Effective:** immediately upon acceptance (this commit for D3's CC-solo pieces; upon Cursor's PR
merge for D1/D2's mechanical pieces).
**Scope:** the seven `docs/pursuits/d11–d17` records, `scripts/check_pursuit_records.py`,
`docs/personas/cfo.md`, `STATE.md`'s forward-trigger board. Does not touch any other pursuit class,
any other persona charter, or any other gate script.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Leave the six/seven scattered `(C-1)`-style tags as-is, just populate them with the operator's numbers** (the C-1 closure commit's own approach, same day, earlier) | Already done and already insufficient by the CFO's own account — the scattered-tag shape is what let a *known, tagged* gap sit 12 days. Fixing the numbers without fixing the shape repeats the failure mode on the next stale figure. |
| **HARD-gate the ledger-pointer check** (fail CI, not just WARN) | Rejected — crosses `check_pursuit_records.py`'s own stated severity philosophy ("gate wiring is an operator decision, proposed in the landing report, not landed here") without a separate operator ruling on wiring specifically; also this repo's own gate-stack culture (Q-GATESTACK-1, W5) is explicitly wary of gate proliferation. WARN matches every sibling limb. |
| **Build a monthly Claude Code Remote cron Routine as the trigger** (a new scheduled job, separate from `STATE.md`) | Rejected — the operator's own local `daily-repo-truth-sync` task already reads `STATE.md`'s forward-trigger section daily; a second, parallel scheduling surface for the same kind of obligation is exactly the "telemetry subsystem" pattern Rule 2 §5 #6 warns against, and duplicates infrastructure that already exists and already works (the weekly venue-idle-clock row is live proof). |
| **Fleet the mechanical build across multiple Cursor workers** | Considered per the operator's "dispatch engineering tasks to Cursor" instruction — but only one genuinely disjoint, threshold-clearing packet exists once the checker extension is folded into the same build as the ledger/pursuit-record edits (see §0's routing-test application). Fleet overhead (umbrella brief, claim manifest, N branches) is waste at N=1 per the `cursor-fleet` skill's own routing table; a single Cursor handoff is the correct lane. |
| **Build a Phase-4 hookify rule now, alongside D1–D3** | Rejected for now — no evidence yet that a passive practice norm is insufficient (D1–D3 haven't run once). Matches the CFO's own explicit hedge ("unless a hookify one-liner earns its keep after Phase 1-3 are live") and Rule 2 §5 #6. Revisit only if D4 demonstrably fails in practice. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** at the first monthly reconfirm (2026-09-21) or any reconfirm thereafter, if
either (a) the `ledger-pointer` check has produced ≥1 false-positive WARN against a pursuit record
that genuinely has no meaningful $/mo to track, or (b) the ledger itself is found to carry a stale or
wrong figure that a pursuit record's own (pre-consolidation) text would have caught — that is a
falsifier for D1/D2's specific mechanism (not for the underlying goal). **Separately:** if three
consecutive monthly reconfirms pass with zero figures actually changing and zero staleness found,
that is evidence the monthly cadence is tighter than the underlying data warrants (subscriptions
don't reprice that often) — a signal to lengthen the cadence, not evidence the mechanism is wrong.

**Revert action:** limb (a)/(b) → author a superseding ADR narrowing or redesigning the affected
mechanism (D1's ledger schema or D2's regex scope), citing the specific miss. The
zero-change-3-times signal → propose (not silently adopt) a quarterly cadence instead, via the same
channel.

**Trigger check schedule:** every monthly reconfirm (2026-09-21, then rolled forward), read this
falsifier at each occurrence — not just the calendar date.

---

## §5 — Forbidden moves (genuinely tempting)

- **Escalating the `ledger-pointer` check to HARD-tier "while I'm in there."** Ruled out explicitly
  by §3; needs its own operator ruling on gate wiring, not a default upgrade riding this ADR.
- **Widening `CLASS_LEDGER_TRACKED`'s regex to cover pursuit classes beyond `(subscription)` /
  `(venue account)`** without re-verifying against the live corpus first — the pattern was tested
  against actual `docs/pursuits/*.md` content before freezing (see the companion handoff brief's §2
  Step 2.3); a plausible-looking widen can silently change coverage.
- **Building the Phase-4 hookify mechanism preemptively.** D4 is explicit: practice only, until D1–D3
  demonstrate the practice alone is insufficient.
- **Treating this ADR's ratification as re-opening the CFO's C-1 closure or the d17 ratification**
  (both same-day, earlier commits) — this ADR consolidates the *shape* those closures left the data
  in; it does not re-adjudicate any figure, disposition, or the Databento billing-model tension.
- **Skipping the monthly reconfirm because "nothing's changed"** — a null result is still a
  reconfirm; D4's whole point is that silence is not evidence of currency.

---

## §6 — Consequences

**Gate verdict (binary, ties to §4):** this ADR reads **RESOLVED** if the monthly reconfirm cadence
runs without a false-positive `ledger-pointer` WARN or a caught-stale ledger figure; **FALSIFIED**
for D1/D2's specific mechanism if §4's revert trigger fires, requiring a superseding ADR to redesign
the affected piece; **AMBIGUOUS** only in the narrow sense of the zero-change-3-times signal (§4),
which prompts a cadence proposal, not a verdict on the mechanism itself.

**Positive consequences:**
- Closes the actual mechanism the CFO diagnosed (no forcing function), not just its symptom (stale
  numbers) — the second time this session a subscription-tracking gap has been addressed, this time
  structurally.
- Reuses existing infrastructure (`daily-repo-truth-sync`'s daily `STATE.md` read) rather than adding
  a parallel scheduling surface.
- The mechanical build routes to Cursor per this repo's own established CC/Cursor discipline,
  freeing this session's context for the judgment work (this ADR, the charter amendment) that
  discipline reserves to CC.

**Negative consequences (real cost, not theatrical):**
- One more WARN-tier check in `check_pursuit_records.py` — a small, permanent addition to what that
  script scans, though at the same severity (report-only) as everything else there.
- The monthly cadence is itself unvalidated — §4's falsifier is the honest acknowledgment that
  "monthly" was the operator's stated preference, not a derived-and-tested interval.

**Risks (probabilistic, distinct from costs):**
- A ledger separate from the pursuit records it summarizes can itself drift from them if a future
  edit touches one without the other — mitigated by D2's mechanical check (a record missing the
  pointer is flagged) but *not* by anything that checks the ledger's own figures against reality;
  that check stays human (the monthly reconfirm).

**Downstream artifacts that need updating:**
- `docs/pursuits/SUBSCRIPTION_LEDGER.md` (new), `docs/pursuits/d11–d17-*.md` (7 files) — via the
  companion Cursor handoff, not this commit.
- `scripts/check_pursuit_records.py`, `tests/scripts/test_check_pursuit_records.py` — via the same
  handoff.
- `docs/personas/cfo.md` — this commit (D3).
- `STATE.md` § Scheduled forward triggers — this commit (D3).
- `docs/personas/cfo-log.md` — this commit (ratification entry).
- `docs/adr/INDEX.md` — regenerated via `check_adr_graph.py --regenerate-index`, this commit.

---

## §7 — Implementation plan

- **Phase 0 (this commit)** — author this ADR; amend `docs/personas/cfo.md` (D3); add the
  `STATE.md` monthly subsection (D3); append the `cfo-log.md` ratification entry; author and freeze
  `docs/briefs/handoffs/2026-08-21-cc-handoff-subscription-ledger-consolidation.md` (the D1/D2
  mechanical spec).
- **Phase 1 (pending)** — the handoff brief is dispatched to Cursor (operator-fired, per
  `cursor-fleet`'s dispatch-mechanics constraint: this session runs in a cloud environment without
  local access to `scripts/dispatch_cursor.ps1`, which is a Windows-local script; self-dispatch is
  not available here — see the handoff brief's own header). Cursor returns a PR; CC reviews per the
  brief's §7 two-pass discipline; operator merges.
- **Phase 2** — after merge, `docs/pursuits/SUBSCRIPTION_LEDGER.md` exists and D1/D2 are live;
  re-run `python scripts/check_pursuit_records.py` and `pytest tests/scripts/test_check_pursuit_records.py`
  against `main` to confirm.
- **Phase 3** — first monthly reconfirm due 2026-09-21 per D3's `STATE.md` row.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline checks
python scripts/check_brief.py docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md --type adr
python scripts/check_adr_graph.py

# Companion handoff brief well-formed
python scripts/check_brief.py docs/briefs/handoffs/2026-08-21-cc-handoff-subscription-ledger-consolidation.md --type cc_handoff

# D3: cfo.md charter carries the ledger + the standing-check line
grep -n "SUBSCRIPTION_LEDGER" docs/personas/cfo.md

# D3: STATE.md carries the monthly trigger, next deadline correctly rolled
grep -n -A3 "Monthly — recurring" STATE.md

# Phase 2 (after Cursor PR merges) — ledger + gate live
ls docs/pursuits/SUBSCRIPTION_LEDGER.md
python scripts/check_pursuit_records.py
pytest tests/scripts/test_check_pursuit_records.py -v

# §4 trigger check
# Next monthly reconfirm due: 2026-09-21 (STATE.md § Scheduled forward triggers)
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction — *"I want to implement 1-4, reconfirm ledger
once a month"* (2026-08-21), following the CFO's own recommendations recorded in `docs/personas/cfo-log.md`
the same day. Authority channel: explicit owner adjudication, same channel this repo's other same-day
ADRs used.

**§6-class preconditions at ratification:** §0 populated with anchors (done, this commit) ✓ ·
operator ratification of this ADR's specific scope (this note) ✓ · `python scripts/check_brief.py
docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md --type adr` (run at authoring time, see
Verification) · `python scripts/check_adr_graph.py` (run at authoring time, see Verification).

**Not licensed by this ratification:** D1/D2's mechanical build is *specified*, not yet *executed* —
it is `Accepted` as a design ratification with execution phased to Phase 1 (Cursor dispatch, pending
operator fire) per §7. Re-adjudicating any C-1 figure, the Databento tension, or the still-open
Fly.io/Tradeify rows (§5).

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md --type adr
python scripts/check_adr_graph.py
python scripts/check_personas.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-21 | Initial authoring and ratification — consolidates the CFO's four 2026-08-21 recommendations into one design (ledger, mechanical gate, monthly trigger via existing infrastructure, practice norm), operator-ratified in-session, mechanical build delegated to a companion Cursor handoff per this repo's own CC/Cursor routing discipline. | Joshua + Claude Code |
