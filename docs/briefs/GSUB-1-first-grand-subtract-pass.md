# GSUB-1 — First GRAND-Subtract pass over the First Passage pursuit portfolio

**Status:** `OPEN` — accepted 2026-08-09 alongside the
[`GRAND-tier ADR`](../adr/2026-08-09-grand-tier-quintessentials-binding.md) (ratification note
there); **CLOSED `RESOLVED-LOADBEARING` 2026-08-09** — all four phases executed same day →
[`inventory + dispositions`](GSUB-1-inventory-and-dispositions.md) (37 rows, 19 differences) ·
[`closure`](closures/GSUB-1-closure-resolved-loadbearing.md) · records at [`docs/pursuits/`](../pursuits/)
**Authored:** 2026-08-09
**Closed:** N/A
**Authors:** Joshua + claude.ai (advisor; repo-state-agnostic draft) + Claude Code (instantiation 2026-08-09)
**Parent question:** N/A — first run of the tier created by the paired ADR
**Loop:** Inquire-style brief, CC-handoff-ready — closure gated on §4 (disposition-difference count)
**Loop-of-Record:** GRAND (tier created by the paired ADR). Under pre-GRAND vocabulary the
Phase-3 dispositions are STRATEGIC-tier Deletes routed through the three-loop ADR's D2 channel
(c) — explicit owner adjudication — so the run is authority-compliant even before the tier exists.
**D-S-A domain:** data (pre-Q gate on the inventory corpus) **+ pursuit** (dispositions, per ADR
§2.4). Cascade: the pursuit-domain dispositions authorize *no* corpus-, system-, or
meta-process-level D beyond what §7 states.
**Artifact path:** `docs/briefs/GSUB-1-first-grand-subtract-pass.md`

> **Authoring provenance + instantiation deltas.** Drafted repo-state-agnostic by design: repo
> state has moved past advisor memory, so **this spec carries no pursuit inventory and no named
> dispositions**. Any pursuit names appearing in prior advisor conversation are stale
> illustrations, **not inputs**. The inventory is built fresh in Phase 1. Instantiation deltas
> (2026-08-09, formatting reconciliation only — no execution substance altered): `ADR-XXX` → the
> real slug; house header block added; renumbered to the house inquire layout (§2 prior-art, §3
> question, §7 execution — the advisor draft had execution at §2 and parent review at §7, now §7
> Phase 5); §4 restated in explicit if/then form; §6 gains the typed-disposition table; §8/§9
> (pre-registration, closure format) added per template; pursuit records surface instantiated as
> `docs/pursuits/` (per ADR §10 note); §0 annotated with live surface names + pending-markers;
> verification paths made concrete.

---

## §0 — Rule 0 (executing session, before any disposition)

Build the pursuit inventory from **live surfaces only**, each row citing source + anchor.
Anchors marked `[§0-pending]` are populated by the **executing** session at run time
(`git log -1 -- <path>` each), per the inquire-template convention for pre-locked briefs:

- [ ] Repo: `docs/adr/` (+ `INDEX.md`, `TOMBSTONES.md`) · `docs/briefs/` incl. `INDEX.md`
  (Q-roster), `closures/`, `pre-registration/`, `handoffs/` (locks and parks included) ·
  campaign registry `lab/CATALOG.md` · `STATE.md` (operator queue, decision index, dormant
  threads, forward triggers) · `docs/notes/` — anchors: `[§0-pending]`
- [ ] Skills / methodology belt listing — `.claude/skills/` (19 `SKILL.md` at instantiation) +
  the user-level plugin belt (the belt is in scope as a pursuit class) — anchor: `[§0-pending]`
- [ ] Tooling & subscription stack — ⚠ instantiation verification 2026-08-09: **no single repo
  registry of subscriptions exists**; candidate sources are scattered (databento entitlement,
  Cursor, Fly.io, CrossTrade, TradingView across `docs/notes/` + advisor memory). Expect a §0.5
  ambiguity item naming the source chosen — source: `[§0-pending]`
- [ ] Advisor memory — **input, not corpus**: usable to check the inventory for omissions, never
  as a row's sole source.

Dispositions proposed before the inventory is complete are Rule-0 violations — suspect even if
right.

## §0.5 — Ambiguity halt (mandatory before Phase 2)

The executing session lists ambiguities and **halts for operator input** rather than defaulting.
Expected ambiguity classes: what counts as a pursuit at the margin (thread vs sub-task), unclear
residual ownership, records with no discoverable standing. Implicit-completeness is a spec
failure.

---

## §1 — Context & motivation

**Symptom (pattern-level):** pursuit accretion. Parks lack re-entry conditions and expiries;
closed pursuits resurrect at zero evidence cost; pursuit intake is ungoverned; the meta-belt
grows without pruning. Campaign-level kills stay dead because pre-registration armors them;
pursuit-level closes have no equivalent armor.

---

## §2 — Prior art / lineage

- [`GRAND-tier ADR`](../adr/2026-08-09-grand-tier-quintessentials-binding.md) (`Proposed`) —
  creates the tier, the pursuit domain, the lifecycle states, and the intake rule this run
  executes; its §4 falsifier is armed by this run's outcome.
- [`Three-loop binding ADR`](../adr/2026-06-12-three-loop-methodology-binding.md) (`Accepted`) —
  D2 channel (c) is the pre-existing authority route for the Phase-3 dispositions.
- No prior GSUB run exists (verified at instantiation: `GRAND|Quintessential|GSUB` grep over the
  repo returns only unrelated "grandfathered" tooling hits) — the question is genuinely novel at
  this layer; campaign-level analogues are the pre-registration kill records the symptom
  statement cites.

---

## §3 — Question (GSUB-1, symptom-phrased)

**GSUB-1:** What is the full current pursuit inventory; what does each pursuit cost on a
recurring basis; which stated Aim does each serve; and which standings survive a Quintessentials
pass?

**Pre-Q gate:**
```
D: advisor-memory pursuit snapshots — test: duplicated by higher-fidelity source (live repo state)
S: inventory compressed to one row per pursuit (fields in §7, Phase 1)
A: single table indexed by class + standing, so each disposition question costs O(seconds)
```

---

## §4 — Falsifiable hypothesis

**H:** the ratified disposition set contains **≥1 pursuit whose disposition differs from its
status-quo standing**.

**If** H holds, **then** close `RESOLVED-LOADBEARING` (the paired ADR's §4 holds). **If** zero
differences, **then** close `RESOLVED-CEREMONIAL` (the ADR's sunset review arms, 2026-11-08).
**If** the inventory cannot be completed within budget, **then** close `AMBIGUOUS` — capture
why, respec; do not amend this gate mid-run. A zero-difference outcome is the pre-registered
**falsifier** for the paired ADR's load-bearing claim — it does not falsify this brief's own
execution.

---

## §5 — Forbidden moves (genuinely tempting)

- Amending any pre-registered construct because a parked candidate's slices look good in passing.
- Opening any new pursuit mid-run.
- Reaching into campaign internals — parts and parameters are Delete's jurisdiction, not this
  run's.
- Dispositioning from memory or recall instead of the Phase-1 inventory.
- Converting a warranted SUBTRACT into a PARK to avoid finality, without a genuine, named
  re-entry condition.
- "While I was in there" repo cleanup of any kind.

---

## §6 — Gate criteria (closure verdict) and return taxonomy

Closure is binary per §4; dispositions typed per
[`iterate-closure-exit`](../adr/2026-08-04-iterate-closure-exit-mandatory.md):

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED-LOADBEARING` | ≥1 ratified disposition differs from status-quo standing | `INTEGRATE — ADR §4 holds; records land per §7 Phase 4` |
| `RESOLVED-CEREMONIAL` | zero ratified dispositions differ from status quo | `INTEGRATE — records still land; ADR sunset review arms (2026-11-08)` |
| `AMBIGUOUS` | inventory not completable within the §6 budget | `ITERATE — capture why, respec fresh; never amend this gate mid-run` |

(No `FALSIFIED` row for the run itself: the zero-difference branch **is** the pre-registered
`FALSIFIED` outcome for the paired ADR's §4 claim, recorded there, not here.)

Spawn returns use: `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`, with BLOCKED sub-cased
as context-problem (re-dispatch with context), capability-problem (stronger model / human),
scope-problem (decompose), or plan-itself-wrong (escalate to parent).

**Budget:** one attended session for Phases 1–2; ratification (Phase 3) separate. No artifacts
beyond the inventory table, disposition records, and this brief's closure note.

---

## §7 — Execution plan

### Phase 1 — Inventory

Enumerate pursuits across five classes: **(a)** active campaigns; **(b)** parked lanes,
including their residual functions; **(c)** standing explorations / feasibility threads;
**(d)** meta-belt items (skills, frameworks, tooling subscriptions); **(e)** aim-scale branches.

Row fields: `name | class | current standing | last activity (anchor) | recurring cost (hrs
and/or $) | Aim served | falsifier or review date, if any | residuals`.

### Phase 2 — Disposition proposals

One proposal per row — `KEEP | PARK(re-entry, expiry) | MERGE(target) | SUBTRACT` — **each
logging the test applied**.

**Permitted subtract-tests:**
- Serves no currently stated Aim.
- Duplicated by a higher-fidelity pursuit already retained.
- Outside current Survive / resource bounds (hours or dollars).
- Residual function unowned and unneeded.
- Expired PARK with no renewal case.

**Forbidden tests** (encode the conclusion; do not apply, and do not substitute a permitted test
that produces the same disposition a forbidden one would — surface it instead):
- "Has been useful before" (sunk cost).
- "Might be useful someday" (unbounded optionality — that is what PARK-with-expiry exists for).
- "Is exciting / feels alive."
- Any test whose answer requires first resolving a strategy-layer question the pursuit exists to
  answer (reach-down).

A test not on the permitted list: stop, write it verbatim, declare it new, surface to operator
before applying. New tests enter the gate audit trail.

### Phase 3 — Operator ratification

All dispositions are **user-gated**: Claude proposes, Joshua authorizes — the D user-gate
(`docs/methodology/inqhiori-canon.md` L282) extended one tier up. Low-reversibility subtractions
(aim-scale branches) may take a cooling period at operator discretion before ratification.

### Phase 4 — Record

Records land at **`docs/pursuits/`**, one markdown file per pursuit (surface per ADR §10 note;
operator confirms at ratification):

- Entry records backfilled for every KEEP (Aim, Measure, Survive bound, review date).
- PARK fields (`re-entry:` + `expiry:`) added to every park.
- SUBTRACT records written with the re-entry armor clause (out-of-frame evidence + attached
  falsifier via governance channel).
- Residuals assigned an owner or subtracted with their pursuit.

### Phase 5 — Parent-session review (two passes + consolidated read)

1. **Spec compliance:** exactly the inventory and dispositions — nothing missing, nothing added.
2. **Quality:** tests logged per row; no forbidden test applied or laundered through a permitted
   one.
3. **Consolidated read** (integration check): does the KEEP set's **aggregate** recurring cost
   fit within the Survive bound? Per-row dispositions can each be sound while the retained
   portfolio still exceeds available hours — the portfolio-level read is where that surfaces.

---

## §8 — Verdict pre-registration

§4 is the frozen verdict gate and has **no tunable thresholds** (the trigger is a
disposition-difference count against status quo). The ratification commit — the commit that
flips the paired ADR to `Accepted` — serves as the pre-registration anchor; no separate
pre-registration file is created unless the operator directs one at ratification.

Pre-registration commit hash: `c90746d` (the ratification commit, 2026-08-09)

---

## §9 — Closure record format

On verdict, the closure note lands at `docs/briefs/closures/GSUB-1-closure-<verdict>.md`
(verdict ∈ `resolved-loadbearing | resolved-ceremonial | ambiguous`), carrying: the verdict vs
the §6 table, the inventory-table location, the disposition log, the mandatory typed `## Iterate`
block discharging the §6 Disposition column, and the paired ADR's §4 reading. The Q-roster row
and the STATE gated row are deleted in the same commit (STATE anti-accretion).

---

## §10 — Audit hooks (runnable at the next quarterly gate)

```bash
# park compliance — scoped to PARK-standing files only (see ADR SS10 note)
grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "re-entry:"
grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "expiry:"

# intake compliance since GSUB-1 (target: 0 pursuits opened without entry records)
# open set = Q-roster Open table + lab/CATALOG.md active rows + STATE.md dormant threads;
# mechanical assist, then hand-walk the diff at the gate:
ls docs/pursuits/*.md 2>/dev/null | wc -l
grep -c '^| \*\*' docs/briefs/INDEX.md

# resurrection counter (target: 0 SUBTRACTs re-opened absent a governance-channel record)
grep -rln "SUBTRACT" docs/pursuits/ --include="*.md"
# cross-check each hit against the currently-open set (ADR §2.3 armor: out-of-frame evidence
# + attached falsifier, via ADR or equivalent)

# drift check
# re-run the Phase-1 inventory; diff against the GSUB-1 table; route deltas to the gate
```

---

## Verification

```bash
# Discipline checks — repo-side mechanical subset, then skill-side (canonical)
python scripts/check_brief.py docs/briefs/GSUB-1-first-grand-subtract-pass.md --type inquire
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/GSUB-1-first-grand-subtract-pass.md --type inquire
# Expected: RESULT: well-formed / PASS

# when spawned as a CC handoff:
python scripts/check_brief.py docs/briefs/GSUB-1-first-grand-subtract-pass.md --type cc_handoff

# Rule-0 confirmation at run time (executing session):
# git log -1 anchors for every §0 surface read in Phase 1
```
