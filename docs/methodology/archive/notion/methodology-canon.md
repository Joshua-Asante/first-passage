<!--
Notion export (verbatim content) — Phase-2 migration per docs/adr/2026-06-12-notion-surface-retirement.md
Notion page-ID : 361dc0b53c1181138eccf03074d05486
Notion URL     : https://app.notion.com/p/361dc0b53c1181138eccf03074d05486
Notion path    : Trading Plan ▸ Command Center ▸ Methodology Canon
Source last-edited (per MCP fetch): 2026-06-06T10:47:30Z
Exported       : 2026-06-13 by Claude Code (Notion MCP fetch); container tags normalized to Markdown, text verbatim
Disposition    : methodology hub page → docs/methodology/archive/notion/
Note           : superseded as a workflow surface by repo canon — INQHIORI canon now at
                 docs/methodology/inqhiori-canon.md; §3.5 LoR now bound by docs/adr/2026-06-12-three-loop-methodology-binding.md.
-->

# 🧩 Methodology Canon

> **Purpose.** Single front door for methodology canon — rules that bind across role boundary (Joshua / claude.ai / CC walk-away / Cursor). For items with dedicated pages, this page is a pointer; for orphans, this page is the canonical home.
> **Role map (codified 2026-05-15):** Joshua=CEO (judgment, locks). claude.ai=Tech Advisor (briefs, methodology, no commits). CC walk-away=Analyst + Tactical Ops (mechanical analysis + OODA, starts independently, Notion read on-demand). Cursor=Engineering (load-bearing surgery, human-in-loop). Three surfaces: repo=code/ADRs/STATE/MC/fills ground truth; Notion=cross-team state + methodology canon; claude.ai memory=advisor context only.
> **Shrinkage test for memory:** if CC or Cursor needs a fact at work → repo or Notion, not memory.

# §1 Pointer — Rule 0 (audit-first)

> **Canonical home:** repo `docs/rule_0.md` (the Command Center opening callout is its operational restatement). Audit-first: read production code before any brief or implementation step touching risk controls; where docs and code disagree, code wins.

# §2 Pointer — The Algorithm

> **Canonical home:** The Algorithm — default problem-solving framework (reference) [Notion `34ddc0b53c11811eb6a0d9192b63d252`; exported to docs/methodology/archive/notion/the-algorithm.md]. Strict order: **Question → Delete → Simplify → Accelerate → Automate.** Don't optimize what shouldn't exist. Pairs with INQHIORI (decide what's real before deciding what to do about it).

# §3 Pointer — INQHIORI ⊕ OODA (separated 2026-05-09)

> **Canonical home:** INQHIORI canon [Notion `34ddc0b53c1181479d7bdecc61f47078`; now repo-canonical at docs/methodology/inqhiori-canon.md]. INQHIORI = structural / low-reversibility / statistical (param changes, lock decisions, MC, anomaly investigations). OODA = tactical / recoverable / tempo (live trades, dd_protection, multi-firm sequencing, broker ops). Canon for OODA lives in the `ooda-loop` skill (no Notion). **Tiebreaker:** no falsifiable 1-sentence H → OODA. Rule 0 binds both.

# §3.5 Loop-of-Record (LoR) tag (2026-06-05, canonical here)

> **Canonical home:** Lean Portfolio meta-layer ADR (`docs/adr/2026-06-04-lean-portfolio-meta-layer.md`, PR #121) + brief-authoring §0 (now a REQUIRED §0 field — see field spec below; repo template + `check_brief.py` enforcement via CC-handoff, pending). **NOTE (2026-06-12):** the loop tiers are now bound to governing methodologies by `docs/adr/2026-06-12-three-loop-methodology-binding.md` (STRATEGIC→The Algorithm / OUTER→INQHIORI / INNER→OODA). **Orthogonal to §3:** §3 picks the *methodology* (INQHIORI vs OODA, rigor-vs-tempo); LoR declares the *governance loop* an artifact answers to. An artifact can be OODA-governed AND Inner-loop, or INQHIORI-governed AND Strategic. **Rule:** every decision artifact declares its primary loop.
> **INNER** — "are we building this iteration's stories correctly?" Team layer / OODA tempo. Tactical, recoverable. Falsifier + budget are tactical (one trade, one sweep, one patch).
> **OUTER** — "are our integrated features delivering the integrated system we planned?" Program layer. Cross-track integration, dependency-level (e.g. a defect latent across all four indicators).
> **STRATEGIC** — "are we funding the right value streams to win the market?" Lean-Portfolio governance layer. Funding / attention / kill-continue.
> **Switch-gate (forcing function):** before any INNER refinement, ask the STRATEGIC question — is the value stream this serves still worth funding? Forward version of the SNAG-budget call. Three of four historical anchors (Q-CORR-1, INQHIORI selection bias, Q-DJ30-1/2/3) would have closed cleaner with this asked up front.
> **No cross-loop evidence borrowing:** an artifact tagged for one loop may not import another loop's evidence to justify its decision (Programme Audit signal #6/#7 cross-layer-contamination lineage).
> **Ceremonial test:** the tag must change the falsifier, budget, or evidence applied. If declaring the loop changes nothing about how the artifact is adjudicated, the tag is ceremonial — drop it.
> **§0 required field (authoring form).** Every Pre-Q / ADR / lock / CC-handoff / audit note / lesson declares, in §0: `Loop-of-Record: INNER | OUTER | STRATEGIC` + one line on what that loop makes load-bearing (the falsifier/budget/evidence the tag changes). If the artifact is an INNER refinement, §0 also records the **switch-gate answer** (Strategic question asked + verdict: fund / starve / kill). A brief that omits LoR, or whose LoR changes nothing, fails the §0 check.
> **Rollout status (2026-06-05):** claude.ai memory ✓ → Notion canon ✓ (this entry) → repo (`brief-authoring` skill §0 template + `check_brief.py` LoR assertion) via CC-handoff — pending.

# §4 Pointer — Regime-robustness gate

> **Canonical home:** repo `docs/methodology/regime_robustness_gate.md` (mandatory pre-LOCK gate per CLAUDE.md; Q-DDP-1 worked example 2026-05-06; mechanics live there). MC-anchor context: Portfolio MC Lock Details [Notion `35cdc0b53c11813e82fdf5f09f36a459`]. **Override history (the operational why):** ADR 2026-05-08 (broker-feed grounds); ADR 2026-05-14 (improving-bust-direction inverts the gate's failure mode). Forward retrospective catch: quarterly `lab/analysis/time_to_pass.py --regime-check`, next 2026-08-08.

---

# §5 Standing overlay doctrine (canonical here)

**NO regime overlays without full INQHIORI.** Strategies are inherently regime-adaptive via EMA / BB / ATR gates — overlays double-adjust the base logic. Repo history of the Iran-Israel / Hormuz overlay (deactivated 2026-04-23): evicted with `archive/` 2026-06-05 — retrieve via `git show pre-prune-2026-06-05:archive/docs/methodology/archive/overlays/guardian_conflict_risk.md`.

**Hard lesson:** headlines and tweets drive markets regardless of physical ground-truth — never build overlays on physical facts.

# §6 Parallel work doctrine (STAGED — canonical here)

Staged 2026-05-10 at `docs/spec/` (singular path convention, ref `reference_docs_spec_singular.md`). Routing is now handled by the §0 Role map (single CC, both analyst + OODA modes). **Proving cluster:** GH #54-57 ULP `dd_protection`. **Promotion gate (binary):** post-mortem needs (a) prevented rework + (b) no over-restrictive rule + (c) no ambiguous cases. **Skill authored post-promotion** (not before — see CC-handoff hygiene §7 for the structural argument on probationary promotion).

# §7 CC-handoff hygiene (standing rule — canonical here)

Promoted 2026-05-15 from candidate-lesson status under the role-map consolidation. **Rule:** for any CC spawn brief with ≥3 mechanical edits in the same defect family, claude.ai MUST dry-run edits on a local snapshot and grep-sweep residuals BEFORE authoring the handoff. **Origin:** Q-CORR-1.3 Rev 3 — caught a 6th defect surface that would have escaped via CC roundtrip. **Structural argument for promotion:** CC running with less oversight and expanded scope makes the spawn brief the only pre-execution filter. Empirical second instance not required.

---

# §8 Lesson registry (canonical here)

Growing list. Each lesson earns its slot through real error-recovery loops; do not add speculative entries.

| # | Lesson |
|---|---|
| 1 | Hurst R/S on log **returns**, not log prices (log-prices → H ≈ 1, AUDNZD case) |
| 2 | Pine source canonical — never reverse-engineer from spec page (NAS v1) |
| 3 | Pyramid-load-bearing strategies need pyramid-conditional WR validation |
| 4 | Architecture-family-transfer requires direction-symmetry check (MFE/MAE) BEFORE direction-flip mirror |
| 5 | Fork ungated sub-Qs from gated parents (Q-A1) |
| 6 | TV <30-day JPY backtests unreliable (~153x P&L inflation; JPY→USD hook fails to initialize on short ranges) |
| 7 | `barstate.islast` dashboard = rightmost bar, NOT entry bar — read Pine conditions on the entry bar, not the screenshot |

---

> **Discipline.** When a new lesson surfaces in a real error-recovery loop, add it here. When a candidate lesson is below graduation threshold (single instance), keep it as a probationary entry in claude.ai memory until it re-fires OR the structural argument promotes it (see §7 origin). Do not pre-emptively codify hypothetical lessons.
