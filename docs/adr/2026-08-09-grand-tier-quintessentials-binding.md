# ADR 2026-08-09 — GRAND tier: bind The Quintessentials above STRATEGIC

**Status:** `Accepted` — ratified by operator (JA) 2026-08-09, in-session direct instruction ("make best judgements and run …"); §0 populated at instantiation; GSUB-1 accepted alongside — see Ratification note
**Decision date:** 2026-08-09
**Authors:** Joshua + Claude (advisor layer, claude.ai — drafted repo-state-agnostic) · instantiated, §0 populated, and reconciled to repo conventions by Claude Code 2026-08-09
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`three-loop binding`](2026-06-12-three-loop-methodology-binding.md) (`Accepted` — extended one tier up, not amended) · [`GSUB-1 run spec`](../briefs/programs/GSUB-1-first-grand-subtract-pass.md) (arms §4; ratifies alongside) · [`ceremony tiering`](2026-08-08-adr-ceremony-tiering.md) (limb-4 → FULL tier: creates doctrine)
**Layer:** meta-process (tier binding); additionally creates a fourth operator domain — **pursuit** (§2.4). **$0 / K=0.**
**Loop-of-Record:** STRATEGIC — binding methodology authority to tiers is governance-of-what-governs (same LoR class as the three-loop binding ADR's own declaration). On ACCEPT, the tier vocabulary itself gains GRAND.

> **Authoring provenance + instantiation deltas.** Drafted in the advisor layer without repo
> access, deliberately repo-state-agnostic; §0 population was delegated to the instantiating
> session as a ratification precondition. Instantiated 2026-08-09 (branch
> `claude/gsub-1-adr-grand-tier-bb2d54`). Deltas from the advisor draft — formatting
> reconciliation per the draft's own instruction ("the in-repo template wins"); **no §2 decision
> substance was altered**:
>
> 1. `ADR-XXX` → this filename (the repo has no `ADR-NNN` numbering; the date-slug is the identifier).
> 2. Header rebuilt to the six machine-parsed fields + house lines (Status token grammar, Layer, LoR).
> 3. §0 item 3 **corrected**: the "Notion dual-loop page" is a retired surface (FREEZE 2026-06-12 per
>    [`notion-surface-retirement`](2026-06-12-notion-surface-retirement.md)); the loop-selection
>    canon's live home is [`docs/methodology/inqhiori-canon.md`](../methodology/inqhiori-canon.md) §14.
> 4. §1 item 5's "override meta-analysis" has **no repo anchor** — advisor-layer finding; marked as
>    such in §0 with the nearest in-repo corroborating record.
> 5. §3 (alternatives) added from content already present in the draft (§1.3 placement finding + §4
>    sunset branch) — full-tier ADRs list alternatives.
> 6. §4 restated with explicit `H:` / `Falsifier:` / `Trigger check schedule:` tokens (checker +
>    sentinel field-form requirements).
> 7. `<pursuit-records-path>` instantiated as **`docs/pursuits/`** — proposed by the instantiating
>    session, confirmed at ratification (§10 note).
> 8. §2.6's "existing quarterly gate" named concretely (the quarterly programme audit; 2026-08-08
>    vehicle ran, next 2026-11-08).

---

## §0 — Rule 0 reads (instantiation checklist — populated 2026-08-09, this worktree)

- [x] Three-loop binding ADR — `docs/adr/2026-06-12-three-loop-methodology-binding.md` — Status
  `Accepted` (ratified 2026-07-06 by PO; D1–D3 graduated, D4 carried by sibling). D1 table binds
  **OODA = INNER, INQHIORI = OUTER, The Algorithm = STRATEGIC** exactly as cited in §1. Anchor:
  `ba943a1` 2026-07-17 (`git log -1`).
- [x] `docs/rule_0.md` — anchor: `7196893` 2026-06-24.
- [x] Loop-selection canon — **corrected surface** (delta 3): live home is
  `docs/methodology/inqhiori-canon.md` — §14 "Methodology-to-Loop Binding" (L285), three-object
  D-S-A framing (L42), D user-gate (L282: *"Claude Code and web Claude both propose deletions;
  Joshua authorizes"*). Anchor: `adb42d7` 2026-08-04. The Notion page cited in the advisor draft is
  retired read-only (`docs/adr/2026-06-12-notion-surface-retirement.md`, anchor `ba943a1`).
- [x] Skills index / methodology belt — `.claude/skills/` (19 `SKILL.md` under version control; the
  belt GSUB-1 treats as a pursuit class). Anchor: `d98ca40` 2026-08-09. Quarterly meta-layer
  cadence owner: `.claude/skills/programme-audit/SKILL.md` (`1772f26` 2026-07-08).
- [x] Pursuit/campaign registry surfaces — `docs/briefs/INDEX.md` (Q-roster; `7dfbbb5` 2026-08-09) ·
  `lab/CATALOG.md` (`7dfbbb5` 2026-08-09) · `STATE.md` (operator queue + decision index + dormant
  threads + forward triggers; `92b6f78` 2026-08-09) · `docs/rejected_candidates.md` (`baaab64`
  2026-08-08).
- [x] Instantiation-convention reads — `docs/adr/2026-08-08-adr-ceremony-tiering.md` (tier test:
  this ADR is limb-4 → FULL; `2a790d0` 2026-08-08) · `.claude/skills/brief-authoring/references/adr.md`
  (status grammar, six header fields) · `scripts/check_brief.py` (`47cc3eb` 2026-07-12; §4 token
  requirements) · `docs/operational_rules.md` retention test (`75e54ed` 2026-08-09; this ADR is
  R5 — open fireable obligation via §4, R3 — re-proposal bar via §2.3 SUBTRACT armor).
- [ ] ⚠ **Unanchored citation, surfaced (delta 4):** §1 item 5's "override meta-analysis" is an
  advisor-layer finding (2026-08-09 claude.ai session) with **no repo artifact**. Nearest in-repo
  record consistent with its signature:
  `docs/notes/audits/programme-audit/2026-08-05-claim-alignment/06-operator-judgement.md`
  (a *"reasoned operator override, not a silent boundary erosion"*, with the reasoning on the
  record). Context-tier citation only — no §2 clause load-bears on it beyond the Update-rule
  design it motivated. If the operator wants it load-bearing, the meta-analysis lands as its own
  note first.

---

## §1 — Context

1. The three-loop binding ADR is ratified (`Accepted` 2026-07-06): **OODA = INNER, INQHIORI =
   OUTER, The Algorithm = STRATEGIC** —
   [`2026-06-12-three-loop-methodology-binding.md`](2026-06-12-three-loop-methodology-binding.md).
2. 2026-08-09: **The Quintessentials** adopted as the decision framework for life choices —
   **Aim, Measure, Anchor, Survive, Subtract**, closed by **Update**, which carries a tripped
   pre-registered falsifier as its entry condition. The layer is named **GRAND**.
3. Placement finding (2026-08-09 advisor session): the framework is an **addition above the
   existing stack, not a replacement**. Subtract (removes *pursuits*) hands off to The Algorithm's
   Delete (removes *parts/requirements* within surviving pursuits). Distinct objects → handoff,
   not duplication.
4. Motivating symptom class (pattern-level; instances are GSUB-1's job, not this ADR's):
   pursuit-level accretion. Campaign-level kills carry pre-registration armor and stay dead;
   pursuit-level closes carry nothing — parks lack re-entry conditions and expiries, closed
   pursuits resurrect at zero evidence cost, pursuit intake is ungoverned, and the methodology
   belt accretes without pruning.
5. Standing doctrine this connects to: Rule 0 (`docs/rule_0.md`); the D user-gate
   (`docs/methodology/inqhiori-canon.md` L282 — Claude proposes deletions, Joshua authorizes);
   and the override meta-analysis finding (advisor-layer, provenance per §0) that vindicated
   overrides share exactly two features — **out-of-frame evidence import** and **exit through a
   governance channel with an attached falsifier**.

---

## §2 — Decision

### §2.1 Tier

Add **GRAND** as the fourth tier: **GRAND ▸ STRATEGIC ▸ OUTER ▸ INNER**. GRAND runs the
Quintessentials loop. Its object class is **pursuits**: whole commitments — campaigns, lanes,
ventures, standing explorations and feasibility threads, meta-belt items (skills, frameworks,
subscriptions), and aim-scale branches.

### §2.2 Interfaces

- **Downward — scoping authority only.** GRAND opens, keeps, parks, merges, and subtracts
  pursuits, and governs pursuit intake. It **never** modifies strategy code, locked parameters,
  allocations, dd_protection, MC calibration, or campaign pre-registrations. (The standing skill
  guard, extended one tier up.)
- **Upward — evidence channel only.** Falsifications, gate outcomes, and out-of-frame evidence
  propagate up. **Update fires only on a tripped pre-registered falsifier** — the
  vindicated-override signature, applied to the tier's own change control.
- **INNER (OODA) binding.** Inherits Aim and Survive as standing constraints. Receives no
  questions from GRAND.
- **Handoff seam.** Subtract (pursuits) → Delete (parts). The surviving pursuit set is the
  Algorithm's intake.

### §2.3 Pursuit lifecycle states (canonical)

`OPEN → { KEEP | PARK | MERGE | SUBTRACT }`

- **PARK** requires a **named re-entry condition AND an expiry date**. At expiry, PARK converts
  to SUBTRACT absent explicit operator renewal. A park missing either field is invalid.
- **SUBTRACT** is terminal with re-entry armor: re-opening requires **out-of-frame evidence plus
  an attached falsifier**, recorded through a governance channel (ADR or equivalent). This is the
  missing "§5 clause" at the pursuit layer — the anti-resurrection armor campaigns already have.
- **Residuals**: any residual function of a parked/subtracted pursuit must be explicitly
  enumerated and assigned an owner, or it subtracts with the pursuit.
- **MERGE** names its target and transfers residuals explicitly.

### §2.4 Domain-table extension (conflation guard)

The D-S-A three-domain table (data | system | meta-process —
`docs/methodology/inqhiori-canon.md` L42) gains a fourth row:

| Location | Operator domain | Object | Purpose |
|---|---|---|---|
| **GRAND tier** | **Pursuit** | Whole commitments | Bound what exists at all |

**Subtract is not D in any lower domain.** A GRAND artifact may not execute D on
data/system/meta-process objects; lower-tier artifacts may not disposition pursuits. Domain
conflation remains the primary guarded failure mode.

### §2.5 Intake rule

Opening a new pursuit requires a GRAND-level **entry record** (minimum one paragraph): Aim
served, Measure (what counts as progress), Survive bound (resource ceiling), and a review date.
No side-door pursuits. Existing pursuits are **not** grandfathered — GSUB-1 backfills entry
records for every KEEP.

### §2.6 Cadence

GRAND review binds to the **existing quarterly programme-audit gate** — no new ceremony. (The
2026-08-08 vehicle ran —
`docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md`; the next slate is
**2026-11-08**.) Update may fire off-cycle only on a tripped falsifier.

---

## §3 — Alternatives considered (added at instantiation from draft §1.3 + §4)

| Alternative | Why ruled out |
|---|---|
| Fold the Quintessentials into The Algorithm as additional operators | Distinct object class: Subtract removes *pursuits*; Delete removes *parts/requirements* within surviving pursuits (§1.3). Merging them conflates exactly what the §2.4 domain guard exists to keep separate. |
| Run the Quintessentials as a life-choices checklist, no tier binding | Not rejected a priori — this **is** the §4 sunset outcome if GSUB-1 shows the tier ceremonial. Deferred to evidence rather than presumed. |
| Status quo — no pursuit-layer governance | The motivating symptom class (§1.4): parks without re-entry/expiry, zero-evidence-cost resurrections, ungoverned intake, a belt that only grows. |

---

## §4 — Falsifiable hypothesis (this ADR's own falsifier)

**H:** The first GRAND-Subtract run (GSUB-1) yields **≥1 ratified disposition that differs from
status-quo standing** — i.e., the tier changes at least one real decision.

**If** H holds, the tier is load-bearing and this ADR holds. **Otherwise** the tier is
provisionally ceremonial: a sunset review arms at the following quarterly gate (**2026-11-08**),
at which the tier is demoted to a checklist unless a decision-difference has since emerged.

**Falsifier:** zero decision-differences through GSUB-1 **and** through the armed sunset window
**falsifies** the tier as load-bearing. Disposition on falsification is demotion-to-checklist via
a superseding record — never silent retention.

**Trigger check schedule:** quarterly programme-audit slate — first evaluation at the first audit
after GSUB-1 closes (**2026-11-08**; the 2026-08-08 vehicle has run).

---

## §5 — Forbidden moves (genuinely tempting)

- Using this ADR to relitigate any lower-tier lock, allocation, pre-registration, or
  risk-control constant ("while we're formalizing…").
- Creating a new standing review ceremony instead of binding to the existing gate.
- Grandfathering current pursuits past the intake rule.
- Relabeling existing parks as compliant without adding re-entry + expiry fields.
- Ratifying with an unpopulated §0.

---

## §6 — Gate (binary)

- **PROPOSED → ACCEPTED** requires: §0 populated with anchors (**done at instantiation,
  2026-08-09**); operator ratification; the GSUB-1 spec accepted alongside (the ADR's falsifier
  needs its test armed).
- **ACCEPTED** arms §4 against GSUB-1's outcome. Same-commit downstream updates at ACCEPT
  (pre-declared blast radius): `CLAUDE.md` standing-decision pointer row;
  `docs/methodology/inqhiori-canon.md` §14 gains the GRAND row; `STATE.md` gated row flips to the
  2026-11-08 forward-trigger board; `docs/pursuits/` is created by GSUB-1 Phase 4.
- **REJECTED / AMBIGUOUS** (named defect, returns for re-authoring) are the alternatives. No
  silent amendment of this ADR mid-review — defects close it AMBIGUOUS and a fresh version states
  the fix up front.

---

## §10 — Audit hooks (runnable, each quarterly gate)

Pursuit records surface: **`docs/pursuits/`**, one markdown file per pursuit (proposed at
instantiation per the draft's delegation; operator confirms at ratification — if a different
surface is chosen, these commands are edited in the ratification commit).

```bash
# every PARK record carries both required fields — scoped to PARK-standing files only
# (an unscoped grep over the whole dir also flags every KEEP/SUBTRACT/MERGE record,
# which correctly lack these fields; discovered running this hook for real 2026-08-09)
grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "re-entry:"
grep -l '\*\*Standing:\*\* PARK' docs/pursuits/*.md | xargs grep -L "expiry:"

# no pursuits opened without entry records since ACCEPT (target: 0)
# open set = Q-roster Open table + lab/CATALOG.md active rows + STATE.md dormant threads;
# mechanical assist, then hand-walk the diff at the gate:
ls docs/pursuits/*.md 2>/dev/null | wc -l
grep -c '^| \*\*' docs/briefs/INDEX.md

# resurrection counter — subtracted pursuits re-opened without a governance-channel record (target: 0)
grep -rln "SUBTRACT" docs/pursuits/ --include="*.md"
# cross-check each hit against the currently-open set; a re-open is compliant only with an
# ADR-or-equivalent record carrying out-of-frame evidence + an attached falsifier (§2.3)
```

---

## Ratification note (2026-08-09)

**Ratified by:** Joshua (PO), in-session direct instruction — *"make best judgements and run
`2026-08-09-grand-tier-quintessentials-binding.md` and `GSUB-1-first-grand-subtract-pass.md`"*
(2026-08-09, follow-on to PR #705). Authority channel: explicit owner adjudication — the
three-loop ADR's D2 channel (c), the same channel that ratified the three-loop binding itself.

**§6 preconditions at ratification:** §0 populated with anchors (instantiation, 2026-08-09) ✓ ·
operator ratification (this note) ✓ · GSUB-1 accepted alongside (same commit) ✓. "Run" arms the
pair and executes GSUB-1 Phases 1–2 in-session; it does **not** collapse the Phase-3 gate —
disposition ratification stays operator-gated per the D user-gate this ADR extends.

**Delegated judgment calls confirmed under "make best judgements":** pursuit-records surface =
`docs/pursuits/` (as instantiated); no separate GSUB-1 pre-registration file (its §4 gate has no
tunable thresholds — the pre-reg anchor is this ratification commit, populated in GSUB-1 §8 in
the follow-up commit).

**§6 ACCEPT downstream updates (this commit):** `CLAUDE.md` standing-decision row ·
`docs/methodology/inqhiori-canon.md` §14 GRAND row · `STATE.md` gated row → 2026-11-08
forward-trigger board. `docs/pursuits/` is created by GSUB-1 Phase 4 (post-Phase-3, by design).

---

## Addendum 2026-08-09 — §4 satisfied; tier is load-bearing

GSUB-1 ran and closed the same day it was accepted:
[`closure`](../briefs/closures/GSUB-1-closure-resolved-loadbearing.md) ·
[`inventory + dispositions`](../briefs/programs/GSUB-1-inventory-and-dispositions.md).

**§4 reading:** the run yielded **19 ratified dispositions differing from status-quo standing**
against a threshold of ≥1 (8 PARK · 9 SUBTRACT · 2 MERGE; operator bulk-ratified in-session).
**H holds — the tier is load-bearing; the sunset review does NOT arm.** The 2026-11-08 STATE row
is retained as the first *scheduled* §4 re-read (per §4's trigger schedule), not as a sunset.

**Substantive support beyond the bare count** (the count alone could be satisfied by trivia): the
inventory surfaced two decisions that had gone **unowned** rather than merely stale — the Notion
estate's Phase-3 disposition, pending through *two* quarterly audits with its own §4 hypothesis
holding throughout; and Q-USOIL-1's park, whose named "08-08 revisit" lapsed when its board row was
deleted at the Great Prune with no re-park. Neither was visible from any single existing surface.
That is the pursuit-layer accretion §1.4 predicted, in a shape the campaign-layer machinery does
not catch.

**§10 defect found and corrected by running the hook** (trap M-AHF): the park-compliance hook as
originally authored was unscoped and flagged every KEEP/SUBTRACT/MERGE record. Corrected in place
above; a §10 hook is machinery, not a frozen verdict construct.

**Not licensed by this addendum:** anything at a lower tier (§2.2 downward interface is scoping
authority only), and no campaign inside a KEEP pursuit is adjudicated by its KEEP.

## Addendum 2026-08-19 — Great Prune is not a Subtract

**Does not amend §2 / §3 / §4.** Citation only.

[`2026-08-08-great-prune.md`](2026-08-08-great-prune.md) is a documentation-class retention
test (keep-if R1–R5 on *parts*). It is not a GRAND Subtract and was not authored as The
Algorithm's Delete. §2.4's handoff names distinct objects; the L283 "deleted at the Great
Prune" line is an incident cite, not an operator identification. Live test owner:
`docs/operational_rules.md` Rule 16. Ruling:
[`2026-08-19-great-prune-is-not-grand-subtract.md`](2026-08-19-great-prune-is-not-grand-subtract.md).

---

## Verification

```bash
# Discipline checks — repo-side mechanical subset, then skill-side (canonical)
python scripts/check_brief.py docs/adr/2026-08-09-grand-tier-quintessentials-binding.md --type adr
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-09-grand-tier-quintessentials-binding.md --type adr
# Expected: RESULT: well-formed / PASS

# ADR lifecycle graph — header fields, edges, INDEX sync
python scripts/check_adr_graph.py
# Expected: exit 0 (A2 reverse-edge skipped while Proposed)

# Rule-0 confirmation (§0 anchors)
git log -1 -- docs/adr/2026-06-12-three-loop-methodology-binding.md   # ba943a1
git log -1 -- docs/methodology/inqhiori-canon.md                      # adb42d7
git log -1 -- docs/rule_0.md                                          # 7196893

# cited binding exists as cited
grep -n "OODA" docs/adr/2026-06-12-three-loop-methodology-binding.md  # D1 table: OODA = INNER
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-09 | Initial authoring (advisor layer, repo-state-agnostic) | Joshua + claude.ai |
| 2026-08-09 | Instantiated: §0 populated with anchors; deltas 1–8 in the provenance note (formatting + stale-surface corrections; no §2 substance change) | Claude Code |
| 2026-08-09 | Ratified `Proposed` → `Accepted` (operator in-session instruction; Ratification note); §6 downstream updates landed same commit | Joshua + Claude Code |
