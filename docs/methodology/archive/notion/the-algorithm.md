<!--
Notion export (verbatim content) — Phase-2 migration per docs/adr/2026-06-12-notion-surface-retirement.md
Notion page-ID : 34ddc0b53c11811eb6a0d9192b63d252  (legacy canon-referenced page; resolved in docs/governance/notion-redirect-map.md)
Notion URL     : https://app.notion.com/p/34ddc0b53c11811eb6a0d9192b63d252
Notion path    : Trading Plan ▸ Dev-phase archive ▸ Framework references ▸ The Algorithm
Source last-edited (per MCP fetch): 2026-04-25T17:03:26Z
Exported       : 2026-06-13 by Claude Code (Notion MCP fetch); container tags normalized to Markdown, text verbatim
Disposition    : framework/lesson/rule page → docs/methodology/archive/notion/
-->

# ⚙️ The Algorithm — default problem-solving framework (reference)

> **Purpose.** Canonical definition of The Algorithm. Linked from `CLAUDE.md` and from Claude Code briefs so the framework has a single, stable meaning. Five steps. Strict order. Apply to strategy code, infrastructure, repo structure, methodology docs, and analysis frameworks themselves.
>
> **Domain.** General-purpose. Applied heavily in trading-system / pipeline work but the framework is not trading-specific.

# The five steps

**Question → Delete → Simplify → Accelerate → Automate**

Strict order. Do not skip steps and do not reorder. Each step's output is the next step's input — accelerating before deleting accelerates waste; automating before simplifying cements complexity.

## 1. Question

Question every requirement, every constraint, every assumption. Don't optimize what shouldn't exist. Question whose requirement it was — if you can't name a person, the requirement is suspect. The most leveraged step in the loop; everything downstream is wasted motion if Question is skipped.

## 2. Delete

Delete the part or process. Add back ~10% of what you delete; if you don't add anything back, you didn't delete enough. Deletion is the highest-yield action — every saved part is a part that doesn't need simplifying, accelerating, or automating downstream.

## 3. Simplify

Simplify what remains. Combine, collapse, reduce parameters, reduce surface area. Only after Question and Delete have done their work — simplifying parts that should have been deleted is wasted effort.

## 4. Accelerate

Accelerate cycle time on what's left. Only after deletion and simplification — accelerating a process that shouldn't exist makes things worse. "Faster" is a property of correct work, not of any work.

## 5. Automate

Automate last. Automating before deletion bakes in waste; automating before simplification cements complexity. The automation step is cheap if the prior four were done well, and expensive (or actively harmful) if they were skipped.

---

# Common failure modes

- **Optimizing a process that should be deleted entirely.** Symptom: improvement plan with no "why does this exist" line at the top.
- **Automating before simplifying.** Symptom: an automation that has a complex internal state machine because it inherited the unreduced shape of what it replaced.
- **Adding back too much after deletion.** Symptom: the post-deletion artifact is structurally identical to the pre-deletion one, just with a few different labels.
- **Skipping Question because the requirement "feels obvious."** Symptom: the requirement turns out to belong to nobody, or to a person who left two years ago, or to an external constraint that no longer applies. Always name the owner.
- **Replacing a heavy framework with another heavy framework.** Symptom: the simplified artefact has the same number of moving parts as the thing it replaced, just relabelled. If Simplify produces an output that isn't lighter, simplify further.

---

# Distinction from INQHIORI

INQHIORI (Identify → Notice → Question → Hypothesize → Investigate → Observe → Reflect → Integrate / Iterate) inserts an explicit `Optimize` discipline between Simplify and Accelerate inside its own loop, and is the broader investigation framework. The Algorithm is the leaner five-step variant for *what to build / keep / remove* questions.

- **The Algorithm** governs *what to build, keep, or remove* — structural decisions on existing or proposed artefacts.
- **INQHIORI** governs *how to learn before deciding* — investigation discipline that produces a validated finding.

Use INQHIORI to decide whether something is real; then use The Algorithm to decide what to do about it. The two are orthogonal: INQHIORI gates evidence-quality, The Algorithm gates structural-decision-quality.

## When to default to which

- **Default to The Algorithm.** Most operational and methodology decisions — "is this framework still load-bearing?", "should this artefact set exist?", "is this rule pulling its weight?" — are best handled by Question / Delete / Simplify before any acceleration or automation.
- **Use INQHIORI** when a residual investigation is needed *before* a structural decision can be made — i.e., when the input to The Algorithm is itself an unvalidated finding. Run INQHIORI first to validate; then run The Algorithm on the validated artefact.
- **Use INQHIORI's Optimize step** when a residual optimization pass on a simplified artefact has identifiable leverage. The Algorithm is happy to call into INQHIORI's Optimize discipline when Simplify has plateaued and a measured optimization run would yield further gains.

---

# Applies to

- Strategy code (Pine, infra)
- Repo structure (file layout, doc layout, methodology hierarchy)
- Pipelines and frameworks (e.g., the Notice/Inquire framework that was compressed under The Algorithm on 2026-04-25 into the three-bucket observation routing gate)
- Analysis frameworks themselves — recursive application is allowed and encouraged. If applying The Algorithm to artefact X surfaces sub-tasks that look like they want optimization, apply The Algorithm to those sub-tasks first.

---

# Worked example — Notice phase compression (2026-04-25)

| Step | Decision | Output |
|---|---|---|
| Question | Is the Notice/Inquire two-phase framework load-bearing or ceremonial? Audit: of three threads in the most recent run, two produced "no action" outputs against material analytical cost. | Framework was producing analysis, not protection. |
| Delete | Drop standing JSON / figure / CSV outputs for the closed-bucket findings (A1–A4, C1–C4). Compress to one-paragraph archive entries. | 9 JSONs + 4 figures + 6 CSVs deleted; `notice_phase.py` retained for reproducibility. |
| Simplify | Replace the Notice/Inquire two-phase structure with a three-bucket routing gate (Closed / Action / Forward). Document in `docs/methodology/observation_routing.md`. | One file replaces a multi-phase framework. |
| Accelerate | (No acceleration step needed. The simplified gate is already low-latency — observation → bucket → done.) | — |
| Automate | (No automation step needed. The gate is a discipline, not a process to automate.) | — |

The Algorithm finished at Simplify in this case — Accelerate and Automate were not warranted. That's a feature, not a bug: not every artefact runs the full ladder.

---

# Cross-references

- **INQHIORI reference page**: parent investigation framework. Use INQHIORI to validate findings; use The Algorithm to decide what to do about them.
- **Observation routing gate** (`docs/methodology/observation_routing.md` in the repo): three-bucket replacement for the Notice/Inquire framework, produced by applying The Algorithm to that framework.
- **Operational rules** (`docs/operational_rules.md` in the repo): hard rules that constrain what The Algorithm can decide. The Algorithm operates within these rules, not above them.

---

# Usage notes for Claude Code

- Cite The Algorithm by name when the structural-decision discipline is being applied. "Question / Delete / Simplify" applied recursively at three levels of an artefact is fine and good — the recursion is part of the discipline.
- Do not produce a brief that promises "applying The Algorithm" but only renames or relocates the artefact under review. If Question doesn't surface a real reason the artefact shouldn't exist, *say so*; don't manufacture deletions.
- The Algorithm is user-gated at Delete. Claude Code proposes deletions; the user authorizes. (The Algorithm permits agent-initiated proposals; it does not permit silent deletions.)
