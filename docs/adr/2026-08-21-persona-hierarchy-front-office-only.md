# ADR 2026-08-21 — Persona hierarchy narrowed to Front Office; Middle/Back-office functions run as mechanical gates

> ⚠ **Fully superseded 2026-08-31.** The entire persona-hierarchy system — including the
> Front-Office-only roster this ADR narrowed to — is retired. `docs/personas/` is deleted from the
> live tree; no persona is spawnable. This ADR's own D2 mechanical-gate mapping (the 8
> Middle/Back-office retirements) is unaffected and continues to stand — see
> [`2026-08-31-persona-hierarchy-full-retirement.md`](2026-08-31-persona-hierarchy-full-retirement.md)
> §2 item 5 for why nothing about D2's gates changes. This ADR's text below is left unedited as the
> historical record of what was ratified 2026-08-21 — read it as history, not as a current
> description of anything live.

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-21, in-session direct instruction ("What
i realized is [First Passage] is primarily a research entity, with deployment as a means of validating
this research... First Passage doesn't really need a dedicated Middle and Back Office, they just need
middle and back office services. The only personas I need are the ones in the Front Office"), scope
confirmed via `AskUserQuestion` ("Pure mechanical gates" / "Keep CFO as-is" / "Full change today"); see
Ratification note.
**Decision date:** 2026-08-21
**Authors:** Joshua + Claude Code (design collaboration, 2026-08-21)
**Supersedes:** `2026-08-19-loop-persona-hierarchy-review-panel.md` in part — D1's spawnable roster
(narrowed to Front Office + the CEO apex + the cross-office CFO; the six Middle/Back-office
C-suite/Senior-Manager seats are retired from the spawnable roster) and D3's *implementation* of the
CRO safety-invariant hard-block (now a standalone deterministic code check, not conditional on a
spawned CRO persona). D3's underlying claim — the hard-block enforces an existing non-negotiable and
grants no new AI authority — is unchanged and **not** superseded. D2 (extend the existing panel
workflow, not replace), D4's ownership-map delegation *mechanism* (reassigned, not abolished — see
§7), D5 (Joshua decides, always), and the GRAND/STRATEGIC panel trigger scope are all untouched.
Historical record only as of 2026-08-31 (see the full-supersession notice above).
**Superseded-by:** `2026-08-31-persona-hierarchy-full-retirement.md` — in full
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [persona hierarchy](2026-08-19-loop-persona-hierarchy-review-panel.md) (`Accepted`,
partially superseded by this ADR — see above) · [design spec](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md)
(content of record for the mechanism this ADR narrows; gains a cross-reference addendum only, per
this ADR's own §7) · [governance friction audit](../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md)
(found 13-of-18 spawnable personas had never fired as of 2026-08-19 — the evidentiary backdrop this
ADR's §1 draws on) · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (limb 4 fires — see §0)
**Layer:** meta-process (governance-of-what-governs, same class as the ADR this partially supersedes).
**$0 / K=0.**
**Loop-of-Record:** STRATEGIC — narrowing a review mechanism bound to the GRAND/STRATEGIC tiers is the
same LoR class as the ADR it partially supersedes.

---

## §0 — Rule 0 reads (this worktree, 2026-08-21)

- Persona-hierarchy ADR — `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` — anchor
  `8e54f3f` (2026-08-21, `git log -1 --oneline`). The decision this ADR partially supersedes; read in
  full, including all four same-day addenda.
- Persona roster index — `docs/personas/INDEX.md` — anchor `8948609` (2026-08-21). Confirmed live
  roster is 17 files (not the ADR's stale "16" — a Research Analyst seat landed 2026-08-20, one day
  after the ADR's last addendum, and the ADR's own roster count was never updated to match).
- Persona ownership map — `docs/personas/ownership-map.md` — anchor `90fbc52` (2026-08-21). Read in
  full: Layer 1 (directory skeleton, ~35 rows) and Layer 2 (38-pursuit table).
- `scripts/check_personas.py` — anchor `8948609` (2026-08-21). `EXPECTED_COUNT = 17`; confirmed the
  glob (`PERSONAS_DIR.glob("*.md")`, non-recursive) already excludes `docs/personas/archive/` —
  moving a persona file into that directory is the existing, already-load-bearing retirement
  mechanic, not a new one this ADR invents.
- `.claude/workflows/pre-ratification-adversarial-panel.js` — anchor `84a941a` (2026-08-21). Read in
  full: `PERSONA_REGISTRY` (10 entries, C-suite + Senior-Manager tier only — Staff tier fires at its
  own natural gate, outside this panel), the mandatory-CRO-on-GRAND rule, `citesSafetyInvariant()` /
  `croHardBlockFires()`, and the existing "biased toward over-triggering, fail-closed" design
  philosophy this ADR's §2 D3 preserves and re-targets.
- Design spec §6.7 (persona retirement procedure) — `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`
  — anchor `8948609` (2026-08-21). The individual-seat retirement mechanics (freeze intake / reassign
  ownership-map rows / archive-don't-delete the log / mark INDEX RETIRED with a pointer / ratify
  before merge) this ADR applies to six seats at once, as one structural decision under D5's
  owner-adjudication channel — not six separate per-seat §6.7 triggers.
- CLAUDE.md — anchor `4c90962` (2026-08-21). §Standing decision table row for the persona panel, the
  row this ADR's §7 updates.
- `core/dd_protection.py` — anchor `bf32aa3`-class (frozen; `_validate_protection_rule` import guard
  confirmed present, per CLAUDE.md §Protection) — the mechanical gate Head of Risk & Sizing's charter
  already delegated to.
- `docs/operational_rules.md` §8 — Rule 0 discipline; `scripts/check_advisor_dedup.py` — the
  mechanical gate Research Registry Analyst's charter already delegated to (per its own Domain field:
  "checks that new research work doesn't duplicate a prior investigation").

**Amendment-first / dedup (Rule 8 sub-rule 10):**

```
$ python scripts/check_advisor_dedup.py --keywords "front office only persona roster middle back office mechanical gate retire"
check_advisor_dedup: keywords: 'front office only persona roster middle back office mechanical gate retire'
  slugs found:    (none)
  keywords found: 9 significant terms

POSSIBLE PRIOR ART (top of 92 candidates) — none is an existing owner of *this* decision:
  [7] docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md — informational backdrop
      (cited in §1/Related), not an owner that should have taken this as an addendum
  [6] docs/briefs/closures/GSUB-2-closure-resolved-loadbearing.md — a downstream *consumer* of the
      panel this ADR narrows, not an owner
  [5] docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md — unrelated (18 shared generic
      tokens: back/gate/mechanical/retire/roster)
```

**Judgment:** the only candidate owner for *this specific* decision (narrow the spawnable roster to
Front Office) is the persona-hierarchy ADR itself. Per that ADR's own template rule ("Material
amendment to a decision already recorded here is never a silent edit... Amend by authoring a new ADR
that declares Supersedes"), amend-in-place is not available for an `Accepted` ADR's material content —
a superseding ADR is the mandated channel, not a dedup violation. Nothing here is re-derived from the
governance-friction audit or GSUB-2/GSUB-1 closures; they are cited as evidentiary backdrop only.

---

## §1 — Context

The persona hierarchy (2026-08-19) modeled First Passage's GRAND/STRATEGIC review mechanism on a
real institutional front/middle/back-office org chart, on the premise that a decision this
consequential needs the same independence structure a regulated trading firm uses. Two things have
changed since. First, direct operator reflection (2026-08-21, this session): First Passage is
primarily a **research entity** — `core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS` deployment exists
to *validate* research, not as a parallel line of business needing its own standing institutional
back-office. Middle-office risk/validation discipline and back-office governance/engineering
discipline are still necessary — but as **services the research function consumes**, not as
departments First Passage itself staffs with reporting chains. Second, the evidence already on
record supports this reading rather than resisting it: the 2026-08-19 governance-friction audit found
13-of-18 spawnable personas had never fired, and every retired Middle/Back-office seat's own Domain
field (read in full at §0) names a mechanical gate that already exists in code or as a script —
`core/dd_protection.py`'s import guard, `validate_c1_monitoring_acceptance.validate(require_resolved=True)`,
`scripts/check_brief.py`, `scripts/check_advisor_dedup.py`, `scripts/check_adr_graph.py`, the
`cursor-fleet` skill. The persona layer over these functions was, in most cases, a redundant LLM
wrapper around a gate that was already deterministic.

**Decision driver (one sentence):** the operator's own re-framing of First Passage's structure
(research entity first, deployment as validation) makes a standing Middle/Back-office persona roster
a mismatch with what the repo's own gates already do mechanically — and the evidence for that mismatch
(near-zero real fire history, self-describing mechanical equivalents) was already sitting in the repo
before this session started.

---

## §2 — Decision

**D1 — Retire the six Middle/Back-office C-suite/Senior-Manager personas from the spawnable roster.**
Retired: **CRO** (GRAND/Middle), **Head of Risk & Sizing** (STRATEGIC/Middle), **Head of Validation**
(STRATEGIC/Middle), **COO** (GRAND/Back), **Head of Engineering** (STRATEGIC/Back), **Head of
Governance** (STRATEGIC/Back) — plus their two Back-office Staff, **Documentation Analyst** and
**Research Registry Analyst**, whose charters are staff-level executions of Head of Governance's own
mandate and retire with it. The live spawnable roster after this ADR is Front Office
only, plus the two seats explicitly out of scope (D6): **CEO** (apex, never spawned), **CFO**
(cross-office) — **CIO**, **Head of Research**, **Head of Execution**, **Falsifier Analyst**,
**Pre-Registration Analyst**, **Research Analyst**, **TCA Analyst** (9 files, down from 17).

**D2 — Every retired persona's function continues running, as a mechanical (code/script/doc) gate,
not an LLM spawn.** Mapping, derived from each retired persona's own Domain field (§0):

| Retired persona | Charter | Mechanical equivalent (already existing, per §0) |
|---|---|---|
| CRO | Safety invariants (`dry_run`/`armed_until`/M1) | §2 D3 below (panel-workflow code) + `validate_c1_monitoring_acceptance.validate(require_resolved=True)` (arming interlock, independent of this panel) + `core/dd_protection.py` import guard |
| Head of Risk & Sizing | `dd_protection`, lifecycle axis, DD tier | `core/dd_protection.py`, `core/firm_rules.py` (`_BASE_RISK`), `_validate_protection_rule` |
| Head of Validation | M1 maturity, regime-robustness gate, Step-0/DSR/overfitting | `docs/methodology/regime_robustness_gate.md`, `strategy-validation` skill, M1 acceptance validator |
| COO | a5/a6 oversight, meta-belt, STATE/SESSIONS/CATALOG hygiene, retention | `docs/operational_rules.md` §Retention, `scripts/roll_sessions.py`, operator direct review |
| Head of Engineering | a5/a6, AI-agent orchestration | `cursor-fleet` skill — already the literal mechanism; the persona's own file noted it has "no named Staff underneath" and delegates entirely to Cursor workers |
| Head of Governance | ADR discipline, retention/pruning, cross-office inventory | `scripts/check_adr_graph.py`, `scripts/gate_manifest.py`, `scripts/check_personas.py`, `docs/adr/TOMBSTONES.md`, operator direct review |
| Documentation Analyst | Brief-compliance gate | `scripts/check_brief.py` — already named as the mechanical equivalent in the persona's own Domain field |
| Research Registry Analyst | Dedup-first discipline | `scripts/check_advisor_dedup.py`, `.claude/hookify.advisor-dedup-first.md` — already named as the mechanical equivalent |

No gate in the right-hand column is weakened, relaxed, or newly invented by this ADR — every one
already existed and ran independently of whether its corresponding persona was ever spawned.

**D3 — The CRO safety-invariant hard-block is preserved unconditionally, as a standalone deterministic
check, no longer requiring a spawned CRO persona.** Previously, `croHardBlockFires()` scanned a spawned
CRO persona's own findings for a safety-invariant citation — meaning the hard-block only fired if CRO
was spawned *and* happened to flag it. Under this ADR, the panel workflow instead reads the target
artifact's own committed text directly (`git show HEAD:<path>`) on every GRAND-tier persona-mode call
and runs `citesSafetyInvariant()` against it unconditionally — no persona spawn, no LLM judgment step,
matching the code's own pre-existing "deliberately biased toward over-triggering" design philosophy
(§0) more closely than the prior design did, since it no longer depends on a CRO persona happening to
surface the citation. This is a narrower re-implementation of an existing gate, not a new one: the
underlying non-negotiable (CLAUDE.md §Live-execution posture) is unchanged, and the arming-time
enforcement (`validate_c1_monitoring_acceptance.validate`) that actually gates `dry_run=false` is
entirely independent of this panel and untouched.

**D4 — Ownership-map reassignment.** Every `docs/personas/ownership-map.md` row (Layer 1, directory
skeleton) whose Primary or Secondary column named a retired persona is reassigned to the mechanical
gate from D2's table, or to "Operator (Joshua) — no persona; see [gate]" where no code/script gate
exists for that specific row. Layer 2 (the 38-pursuit table) is *not* hand-edited row-by-row — it
already carries its own "known rough edge, not fixed in this pass" admission — instead it gains one
generic redirect note pointing at the Layer-1 reassignment (§7). This follows the design spec's own
§6.7 individual-seat retirement mechanics (freeze intake / reassign / archive-don't-delete / mark
INDEX RETIRED / ratify before merge), applied to six seats at once under this ADR's own ratification
rather than six separate per-seat triggers.

**D5 — Nothing else about the panel mechanism changes.** The panel is still an opt-in mode on
`pre-ratification-adversarial-panel` (D2 of the prior ADR, untouched). Front-Office personas' review
scope, independence rule, and log discipline are unchanged. The GRAND/STRATEGIC panel trigger scope
(GRAND ratifications + strict-D2 STRATEGIC-tier Deletes) is unchanged. Joshua decides, always (D5 of
the prior ADR) — this ADR removes spawnable seats, it does not touch who has ratification authority.

**D6 — CEO and CFO are explicitly out of scope, by direct operator instruction.** The operator's
insight was about institutional Middle/Back-office overhead specifically — not about the CEO apex
(never spawned, not an "office" in the Front/Middle/Back sense) or the CFO's cross-office Survive-bound
/ spend-ceiling / capital-allocation function, which the operator confirmed should stay exactly as-is
when asked directly. Re-litigating either seat under this ADR is a forbidden move (§5).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep Middle/Back-office functions as callable-but-off-roster service-personas** (still LLM spawns, invoked ad hoc instead of standing on the roster) | Operator declined directly (`AskUserQuestion`, "Pure mechanical gates" chosen over this option): still pays LLM spawn cost/latency for functions the repo's own gates already check deterministically, with no clear gain over the code path. |
| **Keep CRO as a persona, retire the rest** | Considered because the safety hard-block is the single most load-bearing piece of the retired layer — but the CRO hard-block was *already* a deterministic regex check over a persona's structured findings (`citesSafetyInvariant()`, §0), not a judgment call the LLM persona was contributing beyond surfacing the citation. Re-targeting the same deterministic check at the raw artifact text (D3) preserves the safeguard without the spawn. Operator declined this option directly. |
| **Status quo — full front/middle/back-office roster** | The governance-friction audit's own evidence (13/18 personas never fired) and every retired seat's self-described mechanical equivalent (D2's table) show the roster was already mismatched to actual load; doing nothing leaves that mismatch standing against the operator's own stated view of what First Passage is. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** across the first 3 real (non-rehearsal) GRAND or STRATEGIC-Delete panel reviews
run under the narrowed Front-Office-only roster, if a mechanical gate from D2's table fails to catch a
defect that a confirmed BLOCKER, on independent re-read, is traceable to one of the eight retired
seats' domain (dd_protection/lifecycle territory, M1/regime-robustness territory, ADR-discipline
territory, dedup-first territory, brief-compliance territory, or a safety-invariant citation the new
D3 scan missed) — that is a falsifier for *that specific seat's* retirement.

**Revert action:** author a new ADR that supersedes this one in part — for the specific retired seat
whose mechanical equivalent proved insufficient — restoring it to the spawnable roster. Never silently
re-add a persona file without a superseding ADR (§5).

**Trigger check schedule:** at the 3rd real panel use under the narrowed roster, or the next quarterly
programme-audit gate (2026-11-08), whichever comes first — same cadence the prior persona ADR's own
§4 uses, not a new one. The prior ADR's own §4 falsifier (whether the panel mechanism as a whole
changes any ratification) is inherited unchanged and tracked separately — this §4 is scoped to the
roster-narrowing decision specifically.

---

## §5 — Forbidden moves (genuinely tempting)

- **Relitigating the CEO or CFO seats under this ADR** — D6 is explicit: this ADR is scoped to
  Middle/Back-office retirement only, confirmed directly with the operator (`AskUserQuestion`). Either
  seat needs its own fresh decision, not a drive-by change riding on this ADR's momentum.
- **Weakening or removing a D2 mechanical gate on the theory that "the persona covering it is already
  gone, so the code check matters less now"** — the reverse is true: with no persona backstop, the
  mechanical gates in D2's right-hand column are now the *only* enforcement for their function. None
  of them may be relaxed without its own ADR.
- **Softening the D3 safety-invariant scan's "biased toward over-triggering, fail-closed" philosophy**
  to cut false-positive hard-blocks — the code's own existing comment names this tradeoff as
  deliberate; reducing sensitivity to reduce operator friction defeats the reason the scan exists.
- **Reintroducing any retired persona (or a new Middle/Back-office seat) without a superseding ADR** —
  matches the discipline this repo already applies to locked constants: change-control runs through
  re-registration, not a casual re-add.
- **Treating D4's ownership-map reassignment as touching modification authority** — per
  `ownership-map.md`'s own opening line, "owner" means first-line reviewer/delegate, not edit
  authority; reassigning a row to "Operator (Joshua) — no persona" does not grant Joshua any authority
  they didn't already have, and does not touch locked-parameter authority (CLAUDE.md §Key Principle).

---

## §6 — Consequences

**Gate verdict (binary, ties to §4):** this ADR's own roster-narrowing decision reads **RESOLVED** if
the D2 mechanical mapping holds through the falsifier window with no confirmed BLOCKER traceable to a
retired seat's domain; **FALSIFIED** for a specific seat if §4's revert trigger fires for that seat
and a superseding ADR restores it; **AMBIGUOUS** if the 3-review window (or the 2026-11-08 backstop)
closes with a disputed-not-confirmed finding, in which case the seat stays retired pending operator
adjudication rather than auto-restoring.

**Positive consequences:**
- Removes LLM-spawn cost/latency for eight seats whose own charters already point at deterministic
  code/script gates, with no coverage loss on any of the eight (D2's table).
- Matches the operator's own stated model of First Passage (research entity; deployment validates
  research) instead of carrying a standing institutional org-chart the operator no longer believes the
  program needs.
- The safety-invariant hard-block (D3) becomes *less* dependent on an LLM spawn happening to surface a
  citation, not more — a straightforward net hardening of the one piece of the retired layer that
  actually gated something load-bearing.

**Negative consequences (real cost, not theatrical):**
- Any genuine judgment call in retired territory that does *not* reduce to a deterministic check (e.g.
  a novel ADR-discipline edge case Head of Governance's judgment, not `check_adr_graph.py`, would have
  caught) now has no dedicated reviewer seat — falls to the operator directly or to a Front-Office
  persona reviewing outside its charter (which its own Independence rule instructs it to decline
  rather than opine on).
- `docs/personas/ownership-map.md` Layer 2 (38-pursuit table) is not hand-reconciled row-by-row under
  this ADR — documented via a redirect note (D4), not silently absorbed, but real staleness until a
  future pass closes it.

**Risks (probabilistic, distinct from costs):**
- The 3-real-review falsifier (§4) is the only backstop against a genuine coverage gap in D2's
  mapping. Mitigation: the mapping is derived directly from each retired persona's own stated Domain,
  not invented fresh, so a systematic miss would have already shown up as a gap in that persona's own
  charter — low but non-zero probability.

**Downstream artifacts updated (this commit):**
- `docs/personas/INDEX.md` — 8 retired rows moved to a "Retired 2026-08-21" section with pointers into
  `archive/`; live roster table now 9 rows.
- `docs/personas/archive/` — gains `cro.md`, `head-of-risk-sizing.md`, `head-of-validation.md`,
  `coo.md`, `head-of-engineering.md`, `head-of-governance.md`, `documentation-analyst.md`,
  `research-registry-analyst.md`. Their `*-log.md` files stay in `docs/personas/` (frozen, per design
  spec §6.7 step 3 — git history is the archive, matching the Great Prune convention).
- `docs/personas/ownership-map.md` — Layer 1 rows reassigned per D2's table; Layer 2 gains a redirect
  note.
- `scripts/check_personas.py` — `EXPECTED_COUNT` 17 → 9.
- `.claude/workflows/pre-ratification-adversarial-panel.js` — `PERSONA_REGISTRY` drops the six retired
  slugs; mandatory-CRO-on-GRAND auto-add logic removed; `croHardBlockFires()` replaced by a standalone
  deterministic target-text scan per D3.
- `CLAUDE.md` — §Standing decision table row updated + this ADR added as a second pointer.
- `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` — gains `Superseded-in-part-by` header
  line + an addendum section, per the "in-part supersede" edge rule.
- `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md` — gains a one-line cross-reference
  addendum in its own Change History (not a rewrite of ratified content).
- `docs/adr/INDEX.md` — regenerated via `check_adr_graph.py --regenerate-index` (never hand-edited).
- `STATE.md` — new decision-index entry.
- `docs/SESSIONS.md` — new entry `2026-08-21d`.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads confirmed current at implementation time (this commit's own `git log`
  anchors).
- **Phase 1** — mechanical edits per §6's downstream-artifacts list above, all landed in this commit.
- **Phase 2** — grep-sweep in two limbs (Known Trap #7 — source-of-truth fracture):
  - **(i) stale references to the pre-decision configuration's own vocabulary** — every place that
    named a retired persona as a live reviewer/owner: `docs/personas/ownership-map.md` (fixed, D4),
    `.claude/workflows/pre-ratification-adversarial-panel.js` `PERSONA_REGISTRY` (fixed, D3), the old
    ADR's own body (left as-is — it is a historical record of what was ratified 2026-08-19, corrected
    going forward via the new `Superseded-in-part-by` header line, not rewritten in place per that
    file's own change-history rule).
  - **(ii) consumers of the retired personas' *log files*** — `scripts/check_personas.py`'s
    `check_logs()` continues validating `cro-log.md` / `coo-log.md` / `head-of-governance-log.md` /
    `documentation-analyst-log.md` / `research-registry-analyst-log.md` in place (they stay in
    `docs/personas/`, frozen, per D4) — confirmed this does not error since their structure is already
    well-formed and no code path requires them to receive new entries.
  - This ADR fully supersedes nothing (all edges are `in part`), so the accept+retire checklist
    (moving a file to `docs/ltm/adr/`) does not apply.
- **Phase 3** — verification block below executes; ADR status is `Accepted` at authoring time per the
  Ratification note (operator instruction already given in-session, per this ADR's own header).

---

## §10 — Audit hooks (runnable)

```bash
# Discipline checks
python scripts/check_brief.py docs/adr/2026-08-21-persona-hierarchy-front-office-only.md --type adr
python scripts/check_adr_graph.py

# Roster count + INDEX sync
python scripts/check_personas.py
# Expected: "check_personas: OK -- 9 persona files, all required fields present, INDEX.md in sync"

# No retired slug remains live in the panel's persona registry
grep -n "cro:\|coo:\|head-of-risk-sizing:\|head-of-validation:\|head-of-engineering:\|head-of-governance:" \
  .claude/workflows/pre-ratification-adversarial-panel.js
# Expected: no hits inside PERSONA_REGISTRY (comments/strings referencing the retirement itself are fine)

# No stray Office: Middle / Office: Back among the live (non-archive) roster
grep -L "Office:\*\* N/A\|Office:\*\* Front\|Office:\*\* Cross-office" docs/personas/*.md
# Expected: empty (every live persona file is Front/N/A/Cross-office; Middle/Back only exist under archive/)

# Superseded-in-part edge is bidirectional
grep -A1 "Supersedes" docs/adr/2026-08-21-persona-hierarchy-front-office-only.md
grep -A1 "Superseded-in-part-by" docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md

# §4 trigger check
# Quarterly regime/programme-audit check due: 2026-11-08 (or 3rd real panel use under the new roster, whichever first)
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction (2026-08-21) — the structural insight itself
("First Passage doesn't really need a dedicated Middle and Back Office, they just need middle and back
office services. The only personas I need are the ones in the Front Office"), followed by explicit
scope confirmation via `AskUserQuestion`: service form = "Pure mechanical gates," CFO seat = "Keep
CFO as-is," scope = "Full change today." Authority channel: explicit owner adjudication, same channel
the prior persona-hierarchy ADR itself was ratified under.

**§6-class preconditions at ratification:** §0 populated with anchors (done, this commit) ✓ · operator
ratification of this ADR's specific scope (this note, distinct from the general insight — the three
`AskUserQuestion` answers close the "how" that the general insight alone left open) ✓ · `python
scripts/check_brief.py docs/adr/2026-08-21-persona-hierarchy-front-office-only.md --type adr` (run at
authoring time, see Verification) · `python scripts/check_adr_graph.py` (run at authoring time, see
Verification).

**Not licensed by this ratification:** anything §5's forbidden moves already exclude — this ratifies
the roster-narrowing decision and its mechanical-gate mapping; it does not retroactively bless every
future Middle/Back-office-shaped function as automatically mechanical (a genuinely novel future
function still needs its own D2-style mapping or its own ADR), and it does not touch the CEO or CFO
seats (D6).

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-21-persona-hierarchy-front-office-only.md --type adr
python scripts/check_adr_graph.py
python scripts/check_personas.py
node --check .claude/workflows/pre-ratification-adversarial-panel.js
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-21 | Initial authoring and ratification — narrows the persona-hierarchy spawnable roster to Front Office + CEO/CFO, retiring six Middle/Back-office seats (plus their two Back-office Staff) to mechanical gates per D2's mapping table, and re-targets the CRO safety-invariant hard-block as a standalone deterministic check (D3). Operator-ratified in-session; scope confirmed via `AskUserQuestion`. | Joshua + Claude Code |
