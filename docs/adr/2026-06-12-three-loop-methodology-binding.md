# ADR 2026-06-12 — Three-Loop Methodology Binding and Systematic Trading Lifecycle Map

**Path:** `docs/adr/2026-06-12-three-loop-methodology-binding.md`
> **Status:** ACCEPTED 2026-07-06 — ratified by PO (Joshua). D1 (loop-binding table), D2 (STRATEGIC-Delete LoR rule), D3 (no-borrowing) graduate PROPOSED→ACCEPTED per §4 H — hook #5 run 2026-07-06 against all in-scope closures found 0 real violations. D4 (add-back metric) is carried by its sibling ADR `docs/adr/2026-07-01-add-back-metric-layer-split.md` (still PROPOSED) and does not block this ratification — see Ratification Note below.
**Date:** 2026-06-12
**Status:** Accepted - ratified 2026-07-06 by PO (Joshua); D1/D2/D3 graduated Proposed to Accepted per the Section 4 hook (see blockquote header above for the full ratification note).
**Decision date:** 2026-06-12
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Owner:** Joshua
**Author:** Claude (Tech Advisor), authored in claude.ai (briefs/methodology/no-commits role); landed to repo via Claude Code 2026-06-12 (the repo uses date-prefixed ADR filenames, not sequential `NNN` — `NNN`→date applied, §0 anchors populated, and audit-hook paths repointed at landing).
**Loop-of-Record:** STRATEGIC — this ADR binds methodology authority to loop tiers, which is itself a Strategic-loop act (governance of what governs). Load-bearing clause: D2/D3 change which sessions may execute programme-tier Deletes. Switch-gate: N/A (no lower-loop execution component).
**Amends / extends:** PR #121 Lean-Portfolio meta-layer ADR (three-loop hierarchy + LoR discipline; `docs/adr/2026-06-04-lean-portfolio-meta-layer.md`); Methodology Canon loop-selection page (Notion `34ddc0b53c1181479d7bdecc61f47078` — surface retired same day per the Notion-retirement ADR `docs/adr/2026-06-12-notion-surface-retirement.md`; canon mirrored to `docs/methodology/inqhiori-canon.md`)

---

## §0 — Reads (Rule 0)

Repo-side anchors were `[ANCHOR PENDING]` at authoring (claude.ai could not read the repo); **populated at landing by Claude Code 2026-06-12** against the live worktree (branch `claude/sweet-chebyshev-11fc6c`).

- PR #121 — Lean-Portfolio meta-layer ADR (three loops INNER/OUTER/STRATEGIC; four-layer governance hierarchy): `docs/adr/2026-06-04-lean-portfolio-meta-layer.md` (commit `c5df37c`, 2026-06-04).
- LoR rollout artifacts (2026-06-05): memory user-edit #18 promotion of LoR to active §0 authoring requirement; CC handoff folding LoR into brief-authoring check #1 + 7 templates + `check_brief.py` assertion. In-repo anchors: `.claude/skills/brief-authoring/SKILL.md` (commits `a58b162` "bring methodology skills under version control + gate" 2026-06-05, `bf3f547` "repoint dropped inqhiori-algorithm refs" 2026-06-05); `scripts/check_brief.py` present in-repo.
- Methodology Canon — loop-selection page, Notion `34ddc0b53c1181479d7bdecc61f47078` — fetched live 2026-06-12 in the authoring session. The planned §14 Notion amendment was superseded same-day by the Notion surface retirement (`docs/adr/2026-06-12-notion-surface-retirement.md`, owner adjudication); the canon content is mirrored to `docs/methodology/inqhiori-canon.md` with §14 included natively (landed this same commit).
- `brief-authoring` SKILL.md — read in full this session (2026-06-12); also in-repo at `.claude/skills/brief-authoring/SKILL.md` (commit `a58b162`). Landing check: `scripts/check_brief.py --type adr` run by Claude Code 2026-06-12 (see Verification block) against the repo-side mechanical gate; structure conforms.
- `inqhiori`, `inqhiori-algorithm`, `ooda-loop`, `programme-audit` SKILL.md descriptions — read this session (skill-registry mount).
- Standing doctrine in userMemories: two-loops-on-two-clocks (R&D automation session 2026-06-05, session `91b8ead4`); LoR session `76f0547a` (four historical episodes motivating prospective loop-awareness); SNAG-budget doctrine; Q-CORR-1 closure + legitimate re-open (Guardian Silver beTriggerAtr=4.8 RF gate).
- Session lineage for this ADR: 2026-06-12 (this session) — corpus excavation → plan architecture → lifecycle/industry mapping → three-loop + Algorithm binding analysis.

---

## §1 — Context

PR #121 established the three-loop hierarchy (INNER tactical/recoverable, OUTER cross-track integration, STRATEGIC funding/attention/kill-continue) and the Loop-of-Record authoring discipline. The 2026-06-05 rollout made LoR a §0 field with switch-gate, no-borrowing, and load-bearing/ceremony checks.

Three gaps remained:

1. **The Strategic loop had no bound methodology.** OODA was established as the Inner-loop tempo discipline and INQHIORI as the Outer-loop epistemic discipline (two-loops-on-two-clocks, 2026-06-05). The Strategic loop had artifacts (SNAG budgets, programme audits, closures) but no named governing methodology — kill/continue verdicts were executed under INQHIORI/audit machinery without a declared authority tier.
2. **The Algorithm's scope was ambiguous.** D-S-A passes run everywhere (concept-record belt-stripping = Outer; programme closure = Strategic), with no rule for which tier of Delete requires which authority. The four LoR-motivating episodes (Q-CORR-1 INNER momentum, INQHIORI selection bias, Aegis silent-zone, DJ30 tail-anchor series) all reduce to lower-loop momentum executing or evading what are properly Strategic-tier verdicts.
3. **The lifecycle stages were unnamed.** The end-to-end operation (R&D → Pine construction → Copygram/DXTrade/TradersConnect execution → telemetry → analysis) had no canonical map tying stages to industry-standard names, to the loops that govern them, or to the two bridges (graduation, feedback) already in doctrine.

This ADR closes all three with one binding decision and one map.

---

## §2 — Decision

**D1 — Methodology-to-loop binding.**

| Loop | Cadence | Governing methodology | Core question | Canonical artifacts |
|---|---|---|---|---|
| STRATEGIC | Quarterly / audit-triggered | **The Algorithm** (Question → Delete → Simplify → Accelerate) | Should this exist and deserve resources? | SNAG budgets, programme closures, track deprecations, ADRs of this tier, programme-audit verdicts |
| OUTER | Per-investigation (days–weeks) | **INQHIORI** | Is this true? | Pre-Q briefs, dispositions, kill records, lock decisions |
| INNER | Per-session / real-time | **OODA** | What do I do right now? | dd_protection calls, FIRE-alert handling, copy-integrity responses, intra-session adjustments |

**D2 — The Algorithm is a fractal operator with Strategic binding authority.** D-S-A passes may run at any loop tier, each declaring its LoR (existing discipline, unchanged). What this ADR adds: **Delete verdicts at programme, track, or instrument tier are STRATEGIC-LoR acts.** They are valid only when executed (a) at programme-audit cadence, (b) on a fired pre-registered stopping rule (e.g., SNAG budget exhaustion, a pre-committed kill rule), or (c) by explicit owner adjudication (Joshua, in-session, named as such).

**D3 — No-borrowing (extension of the LoR no-borrowing rule).** An INNER- or OUTER-LoR session may *propose* a Strategic Delete; it may not *execute* one on local momentum. The proposal routes to one of the three D2 channels. Symmetric guard: a STRATEGIC session does not reach down to hand-tune Outer-loop gate criteria mid-investigation (existing brief-authoring trap #12 already forbids this; restated here as the downward half of no-borrowing).

**D4 — Add-back rate as a Strategic calibration metric.** *(AMENDED 2026-07-01 by `docs/adr/2026-07-01-add-back-metric-layer-split.md` (PROPOSED) — the single pooled metric below is split into two layer-segregated instruments; that ADR governs the add-back definition. Original single-metric text preserved in that ADR §0.)* Per The Algorithm's 10% rule, deletion aggressiveness is measurable. The metric is tracked in **two layer-segregated forms, never pooled** (programme-audit two-layer rule): **(a) meta-layer signal add-back** = rejected *methodology signals* (`docs/methodology/rejected_signals.md`) re-accepted on a dated incident ÷ issued — computed at **methodology** audits, no object-layer anchor (**registry-scoped**, currently 0/1; other governance-surface Delete reversals are meta-layer too but reviewed *qualitatively* at audit, not pooled into this rate); **(b) object-layer strategy add-back** = strategy/track/instrument Deletes (`docs/rejected_candidates.md`) later reversed on new mechanism evidence — computed at **portfolio** audits. **Object-layer anchor datum for (b):** Q-CORR-1 closed 2026-05-14; Guardian Silver legitimately re-opened on beTriggerAtr=4.8 clearing the RF +50.7% gate — one add-back, working as designed. Interpretation bands apply **per instrument, within its own layer's audit**: 0 add-backs over ≥2 audit cycles → deletion threshold likely too conservative (per the 10% rule, not deleting enough); sustained rate well above ~10–15% → threshold too aggressive or kill evidence too thin. Bands are heuristic, reviewed at audit, not auto-acting.

**D5 — Systematic trading lifecycle map adopted.** Five stages with industry names, loop overlay, and the two bridges, recorded at `docs/governance/systematic-trading-lifecycle.md` (companion document, committed with this ADR). The map is descriptive doctrine: it names what exists; it does not by itself authorize new builds.

**D6 — Codification surfaces and source-of-truth order (amended same-day).** Repo = sole canon: this ADR, the lifecycle doc, and the INQHIORI canon mirror `docs/methodology/inqhiori-canon.md` (carrying the binding as its §14). Notion: RETIRED as a workflow surface per the Notion-retirement ADR (`docs/adr/2026-06-12-notion-surface-retirement.md`, 2026-06-12, owner adjudication — the first STRATEGIC Delete executed under D2 channel (c)). Skills = routing lines only, folded into the already-planned consolidation handoff (no new skill — see §5). Memory = load-bearing edits with pointers.

---

## §3 — The Algorithm pass (on this ADR itself)

- **Question:** named owner is Joshua; the requirement ("Strategic loop needs a bound methodology") originates from the 2026-06-12 session's gap analysis, not a department abstraction.
- **Delete:** could we not bind anything and continue ad hoc? Rejected on evidence: all four LoR-motivating episodes are this gap expressing itself. Cost of the gap is measured (Q-CORR-1: ~3 days + audit + closure overhead).
- **Simplify:** smallest sufficient form chosen — one binding table, one tier rule, one metric, one map. Explicitly rejected larger forms (new skill, new loop, Notion prose duplication; see §5).
- **Accelerate:** nothing accelerated here; this ADR is itself the precondition gate for the R-plan's Accelerate phase (sweep engine), per "never accelerate what shouldn't exist."

---

## §4 — Falsifiable hypothesis

**H:** If, over the next two programme-audit cycles (target windows: 2026-Q3 meta-layer audit, then following cycle), (a) every programme/track/instrument-tier Delete executed in the window carries a STRATEGIC LoR declaration and routes through a D2 channel, AND (b) the add-back rate is computable at audit time from kill records + registry entries without archaeology, **then** the binding is load-bearing and graduates from PROPOSED→ACCEPTED at the first audit.
**Otherwise:** if ≥1 Strategic-tier Delete executes without declaration and without detection until audit, or the add-back metric cannot be computed from existing artifacts, the binding is ceremony as implemented — disposition at audit is amend-or-delete, not silent retention.
**Falsifier:** the otherwise-branch is the explicit falsifier — a single programme/track/instrument-tier Delete executed in-window without a STRATEGIC LoR declaration and undetected until audit, OR an add-back rate not computable at audit time from existing kill-records + registry entries, **falsifies** the binding as load-bearing.

---

## §5 — Forbidden moves (each genuinely considered)

1. **Creating a fourth methodology skill** for the three-loop framing. Tempting (symmetry: one skill per loop). Rejected: doctrine ≠ procedure; a fourth skill is the firm-constants-triplication pattern in the skill registry, the exact thing the same-day consolidation deletes. Routing lines in existing skills only.
2. **Reclassifying The Algorithm as a fourth loop.** Tempting (clean "loop per cadence" story). Rejected: it has no cadence of its own; it is an operator whose passes run on all three clocks. Binding ≠ residence.
3. **Duplicating the full ADR prose across read surfaces.** Rejected per the May meta-process sweep lesson: provenance lives in one place. (Originally scoped to Notion; Notion retired same-day per `docs/adr/2026-06-12-notion-surface-retirement.md` — the rule generalizes to any future read surface.)
4. **Retro-backfilling LoR/binding declarations onto the closed back-catalog** (`docs/briefs/`, `docs/adr/`). This re-opens the LoR rollout's open scope question. Held forward-only by default; backfill is a separate owner decision, not smuggled in here.
5. **Using this ADR to touch object-layer constants** — dd_protection C2, allocations, MC calibration, locked Pine. Out of scope by construction; two-layer coupling rule applies.
6. **Letting D4's bands auto-trigger threshold changes.** Tempting (self-tuning governance). Rejected: a gate that tunes itself is the falsifier-drift failure mode programme-audit exists to catch. Bands inform the audit; the audit decides.

---

## §6 — Gate (binary adoption criteria)

ADOPTED when all four are true; otherwise OPEN with the failing item named:

1. This ADR committed to `docs/adr/` with a date-prefixed filename (`2026-06-12-three-loop-methodology-binding.md`; the repo convention, not sequential `NNN`), §0 anchors populated, and `check_brief.py --type adr` passing.
2. INQHIORI canon mirror committed at `docs/methodology/inqhiori-canon.md` carrying the D1 table as its §14. *(Replaces the original Notion-amendment criterion — superseded by `docs/adr/2026-06-12-notion-surface-retirement.md`.)*
3. Consolidated INQHIORI skill description carries the one-line routing ("Outer loop; siblings: ooda-loop = Inner; Algorithm Strategic-tier verdicts bind via LoR") — rides the Phase-R0 skill-dedup CC handoff, not a separate dispatch.
4. Memory carries one edit: binding + pointer. *(Executed 2026-06-12; verify per §10.)*

Graduation PROPOSED→ACCEPTED: per §4 H at first programme audit. FALSIFIED/AMENDED: per §4 otherwise-branch.
**Graduated 2026-07-06 (D1–D3) — see Ratification Note below.**

---

## §7 — Consequences

- The R-plan's phase ordering acquires doctrinal force: Accelerate-tier builds (sweep engine) are licensed only after Question/Delete/Simplify have run at the appropriate tier — recorded in the sweep-engine ADR's own Algorithm pass.
- Programme-audit checklist gains two items: STRATEGIC-Delete declaration compliance; add-back rate computation. (Fold into `programme-audit` skill in the same R0 handoff.)
- Kill records and registry entries become the add-back metric's data source — no new artifact type required; existing conventions already carry the needed fields (date, tier, re-open trigger).
- The lifecycle map gives telemetry (Plan T) its consumer definition: every alert/report names its consuming loop and cadence (T1 spec requirement, already in plan).

---

## §10 — Audit hooks (runnable)

```bash
# 1. ADR present (date-prefixed filename per repo convention), status current
ls docs/adr/ | grep -i "three-loop-methodology-binding"
grep -E "^\*\*Status:\*\*" docs/adr/*three-loop-methodology-binding.md
# Expected: one file (2026-06-12-three-loop-methodology-binding.md); Status PROPOSED until first audit, then ACCEPTED/AMENDED

# 2. Lifecycle map committed alongside
ls docs/governance/ | grep -i "systematic-trading-lifecycle"

# 3. Repo canon mirror carries the binding (replaces retired Notion check)
grep -n "Methodology-to-Loop Binding" docs/methodology/inqhiori-canon.md
# Expected: §14 present; no live Notion dependency (see docs/adr/2026-06-12-notion-surface-retirement.md)

# 4. No fourth methodology skill created (forbidden move #1 held)
ls .claude/skills/ | grep -ciE "loop|algorithm|strategic" 
# Expected: count consistent with consolidated registry (no new loop/strategy-binding skill)

# 5. STRATEGIC-Delete compliance since adoption (run at audit)
# Regex hardened 2026-07-06 (trap M-AHF): the original \s* did not span a
# markdown bold-closing ** between the colon and STRATEGIC, false-flagging
# compliant files written as "**Loop-of-Record:** STRATEGIC".
grep -rliE "disposition|closure|parked|deprecat" docs/briefs/ docs/notes/ --include="*.md" -l | \
  xargs grep -LiE "Loop-of-Record:\*{0,2}\s*STRATEGIC"
# Expected: empty for programme/track/instrument-tier closures dated after 2026-06-12

# 6. Add-back metric computable (run at audit)
grep -riE "re-open|reopen|add-back|unparked" docs/rejected_candidates.md docs/briefs/ --include="*.md" | head
# Expected: hits parse to dated entries; Guardian Silver 2026-06 entry present as datum #1
```

---

## Ratification Note (2026-07-06)

**Ratified by:** Joshua (PO), in-session direct instruction ("ratify it") — D2 channel (c), explicit owner adjudication.

**Trigger:** none of the four 2026-07-01 programme-audit-cycle notes (`docs/notes/audits/programme-audit/2026-07-01-{methodology-belt-scoped-audit,meta-layer-audit-completion,portfolio-audit,cross-layer-synthesis}.md`) mechanically ran this ADR's own §10 audit hooks or flipped its Status, despite that cycle being billed as the "first programme audit" §4/§6 graduate on. All three of that cycle's verdict-bearing notes are themselves still `PROPOSED …pending owner ratification`. The graduation test named in §4 was never actually executed — this note executes it.

**Hook #5 (STRATEGIC-Delete compliance, D2) — PASSES.** Ran the literal §10 hook against all `docs/briefs/`/`docs/notes/` disposition/closure/parked/deprecat-matching files dated after 2026-06-12 (119 raw candidates → 63 in-scope after excluding pre-06-12-content Notion mirrors and a roster index). Of the 63: ~55 are OUTER-tier single-investigation closures (exempt by design — D2 only binds programme/track/instrument-tier Deletes); 1 apparent hit (`docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md`) was a **hook regex bug, not a violation** — it does declare `**Loop-of-Record:** STRATEGIC` in prose, but the markdown bold-closing `**` between the colon and `STRATEGIC` broke the literal match (trap M-AHF: hook tested against the author's mental form, not the artifact's stored form — regex hardened above); 1 borderline case (`docs/ltm/briefs/Q-P2-MEASURE-1-closure-resolved.md`, the NAS100-futures-book exclusion) traces its authority to a properly-declared-STRATEGIC parent ADR (`docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md`) via the pre-registered-stopping-rule channel (D2 channel b), which §5 forbidden-move #4 anticipates should not require re-declaration at every downstream execution artifact. **Zero real violations.**

**Hook #6 (add-back computability, D4) — fails as originally specified; carried forward on the sibling ADR, does not block D1–D3.** D4 is now governed by `docs/adr/2026-07-01-add-back-metric-layer-split.md` (still PROPOSED), whose object-layer (b) anchor is Guardian Silver's beTriggerAtr=4.8/RF+50.7% re-open (Q-CORR-1, 2026-05-14). Running hook #6 today: `docs/rejected_candidates.md`'s current text doesn't use the hook's grepped vocabulary ("re-open"/"add-back"; the registry says "admitted"/"override"/"CLOSED — NOT ADMITTED" instead), and more materially, the registry's own current content shows that admission was itself reversed on 2026-07-01 (no counterbalance materialized; Silver "remains rejected at its original bar"). So as of today the object-layer add-back rate is genuinely **0/1** (computable, just not a live "re-open" the way D4's citation implies) — the sibling ADR's anchor description needs a currency fix, tracked there. This is a real gap scoped to D4/the sibling ADR, not to D1–D3; §4's falsifier for *this* ADR turns on hook #5's condition, which passes.

**Disposition:** D1/D2/D3 **ACCEPTED**. D4 **carried by its sibling ADR**, which needs an anchor-currency fix — follow-up, not blocking.

---

## Verification (commit-time, Cursor)

```bash
python scripts/check_brief.py docs/adr/2026-06-12-three-loop-methodology-binding.md --type adr
# Expected: RESULT: well-formed. The repo-side checker is the mechanical subset; the
# skill-side checker (~/.claude/skills/brief-authoring/scripts/check_brief.py) governs.

# §0 anchors (populated at landing by Claude Code 2026-06-12):
git log -1 -- docs/adr/2026-06-04-lean-portfolio-meta-layer.md      # c5df37c 2026-06-04
git log --oneline -3 -- .claude/skills/brief-authoring/SKILL.md     # bf3f547, a58b162
```
