# Claude Code / Cursor handoff — correct §2.4's rounded win-rate-floor citation to the actual per-shape floors

**Status:** ready to dispatch
**Authority:** surfaced during a same-day PR-learnings reconciliation (2026-08-24, this session) —
reviewing all 16 PRs merged today found #152 (which authored §2.4) citing a single rounded
`≥~65–70%` win-rate floor for the shape pre-check, while #153 (merged later the same day, same
map, Select rows explicitly unchanged) published the real per-shape floors — two of the three are
below that rounded number. Confirmed directly against the source table this session, not inherited
from a paraphrase.
**Layer:** `docs/methodology/` only. No `core/`, Pine, `dd_protection`, ADR, `STATE.md`, or
`docs/SESSIONS.md` touched. $0. Nothing armed. Not a Phase B GO, not a re-run, not a threshold
change — a citation-accuracy fix only.

---

## §0 — Rule 0 reads (this session, verified before this handoff was written)

- [`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) §2.4 — anchor
  `ac05de6` (2026-08-24 11:48:17 -0400). Current live sentence (verbatim, via
  `git show origin/main:docs/methodology/strategy_harvest.md`), embedded inside the §2.4 paragraph's
  clause (4):
  > Current instance: `Tradeify_Select_100K` requires FEASIBLE ≥~65–70% win rate + large mean win,
  > not low skew
  > ([`shape_feasibility_map_2026-08/RESULTS.md`](../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md))
  > — this binds ahead of, not instead of, §2.2;
- [`lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md`](../../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) —
  anchor `89ff641` (2026-08-24 20:22:51 +0000). The actual per-shape win-rate floor table (§6.3
  region), read in full this session:
  ```
  | Shape               | Select floor |
  |----------------------|-------------|
  | `symmetric`          | 65%         |
  | `mild_right_skew`    | 55%         |
  | `bounded_clustered`  | 60%         |
  ```
  Prose confirms: "The floor sits at 55%–70% depending on shape (§6.3)" and separately
  "lowest win-rate floor (55% vs 60–70%)" for `mild_right_skew`. §13.2 confirms these Select
  figures are **unchanged** by #153's same-day Growth-tier addition (Select rows are explicitly
  byte-identical, 0/315 mismatches) — so this table is still the live, current-main truth for
  `Tradeify_Select_100K`, the tier §2.4 names.
- [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) —
  this packet's routing: `docs/methodology/` is not a locked surface (test 1 clear — the locked
  set is `core/` anchor code, Pine, ADRs/pre-regs/`CLAUDE.md`/`STATE.md`); the exact old→new text
  is fully frozen below, no judgment call mid-build (test 2 clear); single small text edit, one
  file — below the fleet threshold, so this is a **single Cursor handoff**, not a multi-packet
  fleet (`.claude/skills/cursor-fleet/SKILL.md` routing table: "One implementation build → Single
  Cursor handoff... Fleet overhead is pure waste at N=1").
- No vendor data, no secrets — pure markdown text edit. Test 0: **N/A**.

---

## §0.9 — Phase-0 staleness check (run before touching anything)

```bash
grep -n "Current instance.*Tradeify_Select_100K.*65" docs/methodology/strategy_harvest.md
# If this line no longer matches (already corrected, or reworded) -- STOP, return DONE citing the
# commit that changed it, or NEEDS_CONTEXT if the wording changed in a way that makes this packet's
# exact old-text match irrelevant. Do not force the edit onto text that doesn't match.

git log --oneline origin/main --since="24 hours ago" -- docs/methodology/strategy_harvest.md lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md
# Confirm neither file has moved since this packet was authored (anchors above: ac05de6 / 89ff641).
# If RESULTS.md has a newer commit, re-read its §6.3 floor table before proceeding -- the numbers
# below must still match verbatim.

gh pr list --state open --search "strategy_harvest"
```

---

## §0.5 — Ambiguity surfacing (read before executing)

None. The old text and new text are both given verbatim in §2 below — this is a find-and-replace,
not a drafting task. The only case requiring judgment is already routed to `NEEDS_CONTEXT` by the
staleness check above: if the source table in `RESULTS.md` §6.3 no longer reads `65% / 55% / 60%`
for `symmetric` / `mild_right_skew` / `bounded_clustered`, **stop and return `NEEDS_CONTEXT`**
with the actual current figures — do not substitute them yourself and do not round them.

---

## §1 — Context

`docs/methodology/strategy_harvest.md` §2.4 (added by PR #152, 2026-08-24) wires a "shape
pre-check" into the standing harvest cadence: a staged candidate's payoff shape must clear the
live venue's feasibility region before §2.2's cost-sniff test runs. The check's whole point is to
stop a fund-first-but-shape-wrong seed like `H-TSMOM-1` from recurring. But the sentence stating
the actual bar rounds three different per-shape floors (65% / 55% / 60%) into one number
(`≥~65–70%`) — a candidate at 55–60% in the right shape (`mild_right_skew` or `bounded_clustered`)
would read as failing a check it should pass. This packet corrects the citation to state the real,
source-verified per-shape floors, changing no code, no threshold, and no judgment logic — only
the accuracy of what the standing prose says the bar is.

---

## §2 — Frozen scope

**Do — exactly this one substitution, in exactly this one file:**

In `docs/methodology/strategy_harvest.md`, inside §2.4's paragraph, replace this exact clause
(verbatim, confirmed at anchor `ac05de6`):

> Current instance: `Tradeify_Select_100K` requires FEASIBLE ≥~65–70% win rate + large mean win, not low skew ([`shape_feasibility_map_2026-08/RESULTS.md`](../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md)) — this binds ahead of, not instead of, §2.2;

with:

> Current instance: `Tradeify_Select_100K` requires FEASIBLE win rate ≥65% (`symmetric`), ≥55% (`mild_right_skew`), or ≥60% (`bounded_clustered`) at that shape's own most favorable cadence/risk — floor ranges 55%–70% depending on shape, not one flat number — plus large mean win, not low skew ([`shape_feasibility_map_2026-08/RESULTS.md`](../../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md) §6.3) — this binds ahead of, not instead of, §2.2;

No other word in the surrounding paragraph changes. Preserve the existing markdown link target and
all surrounding punctuation/clause structure exactly (the semicolon before clause (5) stays).

**Do NOT:**

- Touch `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` — read-only source of truth,
  never edited by this packet.
- Touch any other section of `docs/methodology/strategy_harvest.md` (§2.1–§2.3, §3+, etc.).
- Touch `core/firm_rules.py`, any ADR, `STATE.md`, or `docs/SESSIONS.md`.
- Run any new computation, re-sweep, or MC — the corrected figures are already published in
  `RESULTS.md` §6.3; this packet cites them, it does not re-derive them.
- "Improve" or reword anything beyond the frozen substitution above, even if a tighter phrasing
  occurs to you — this is a citation-accuracy fix, not a rewrite.

---

## §4 — Falsifiable hypothesis

**H:** the live §2.4 sentence understates two of three shape-specific win-rate floors by rounding
them into a single `≥~65–70%` figure, which could cause the shape pre-check to wrongly kill a
future candidate at 55–60% predicted win rate in `mild_right_skew` or `bounded_clustered` shape —
even though `RESULTS.md` §6.3 shows such a candidate can be `FEASIBLE`.

**Falsifier / accept-reject:** **ACCEPT** (merge) if the returned diff touches exactly
`docs/methodology/strategy_harvest.md`, contains exactly the frozen substitution in §2 (old text
gone, new text present verbatim, nothing else in the file changed), and the packet's own
Phase-0/`NEEDS_CONTEXT` gate wasn't tripped. **REJECT** the dispatch (fall back to Claude solo)
if it returns `NEEDS_CONTEXT` or `BLOCKED` twice — two bounces on a fully frozen one-sentence
substitution means something about this packet's premise was wrong, not that Cursor needs a third
try.

---

## §5 — Forbidden moves

- Editing `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` (read-only source).
- Editing any ADR, `STATE.md`, or `docs/SESSIONS.md` (orchestrator-reserved / locked surfaces).
- Rounding, re-deriving, or "cleaning up" the per-shape figures — cite them exactly as given in §2.
- Expanding scope to also fix or comment on any other conflict from today's PR review (the Growth
  headline-cell fragility finding, the ox-alpha Use-N tracking gap, the SESSIONS.md date
  mislabeling, etc.) — those are explicitly out of this packet's footprint and are being routed
  separately by the orchestrator.
- Widening the fix to touch Growth-tier figures — this packet is scoped to the `Tradeify_Select_100K`
  instance §2.4 currently names; Growth is a separate, already-self-disclosed OWED item (see the
  orchestrator's own notes) and is not this packet's concern.

---

## §6 — Return contract

Branch: `cursor/harvest-shape-floor-citation`. One PR against `main`. Four-state status:

- **`DONE`** — the frozen substitution landed verbatim, diff touches exactly one file
  (`docs/methodology/strategy_harvest.md`), no forbidden move triggered.
- **`DONE_WITH_CONCERNS`** — landed, but something about the surrounding paragraph's phrasing felt
  off after the edit — flag exactly what, orchestrator adjudicates before merge.
- **`NEEDS_CONTEXT`** — the Phase-0 staleness check's grep didn't match, or `RESULTS.md` §6.3's
  figures have changed since the anchor commit — state the actual current text/figures found.
- **`BLOCKED`** — some other structural obstruction (e.g. merge conflict on this exact paragraph
  from concurrent same-day work) — state it plainly.

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED>
Branch: cursor/harvest-shape-floor-citation
Diff (files touched): <must be exactly docs/methodology/strategy_harvest.md>
Concerns (if any): <list>
```

---

## §10 — Audit hooks (orchestrator-side, after the packet returns)

```bash
# Diff touches exactly the one named file
git diff origin/main..cursor/harvest-shape-floor-citation --name-only
# Expected: exactly docs/methodology/strategy_harvest.md

# New text landed verbatim, old rounded figure is gone
grep -n "≥~65–70% win rate" docs/methodology/strategy_harvest.md
# Expected: no match (old text removed)
grep -n "≥65% (\`symmetric\`), ≥55% (\`mild_right_skew\`), or ≥60% (\`bounded_clustered\`)" docs/methodology/strategy_harvest.md
# Expected: one match

# RESULTS.md untouched
git diff origin/main..cursor/harvest-shape-floor-citation -- lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md
# Expected: empty
```

---

## Verification (parent-side, before declaring this handoff complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-08-24-cursor-handoff-harvest-shape-floor-citation.md --type handoff
# Expected: well-formed (§0 cites repo paths with anchors; §4 carries H:/falsifier; §5 lists forbidden moves; §10 has a fenced hook; §6 carries the four-state taxonomy)
```
