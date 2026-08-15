# ADR — Root-doc charter ratified; posture narrative demoted to pointers

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-16
**Authors:** Joshua + Claude Code
**Supersedes:** none (extends `docs/operational_rules.md` Rule 7 from *values* to *decision narrative*)
**Related:** Rule 7 origin incident (2026-06-03 STATE.md drift); [`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) ("retire, but do not over-retire")
**Layer:** infrastructure (governance docs)

---

## §0 — Rule 0 reads (production-source verification)

All read in-session on 2026-07-16, before authoring (anchors = `git log -1 --format='%h %ci' -- <path>`):

- `README.md` — anchor `e6ec1ff` (2026-07-15). Public-clone note = 20 lines duplicating CLAUDE.md §Public-clone posture.
- `CLAUDE.md` — anchor `ae6eb27` (2026-07-15). §Live-execution posture = 4 dense paragraphs retelling the R6 / FXIFY / rescope / prop-reopen ADRs.
- `STATE.md` — anchor `e0724cb` (2026-07-15). Four dated `## 2026-07-1x` sections (~72 lines) re-summarizing Accepted ADRs, ahead of the dormant-threads + forward-board content its own header declares as its charter.
- `REPO_MAP.md` / `PIPELINES.md` — anchor `e6ec1ff` (2026-07-15). Static-vs-dynamic split confirmed clean; PIPELINES carries a one-paragraph dormancy preamble (kept — see §3).
- `docs/operational_rules.md` — anchor `83ba1b2` (2026-07-12). Rule 7 (one canonical owner per fact) + its 2026-06-03 origin incident.
- `scripts/validate_params.py` + `scripts/verify_lock_anchors.py` — anchor `f2be990` (2026-07-11). Confirmed the gated CLAUDE.md surface: the Strategy Reference table cells (risk% / contractValue / version) and every bolded `**N% pass / N% bust ...**, p99 DD N%` headline (+ trailing `median N` token). Both parsed regions live OUTSIDE the sections demoted here; the posture prose's bare `(99.83/0.17/4.37)` mention does not match the headline regex.
- `scripts/check_root_doc_liveness.py` — anchor `e6ec1ff` (2026-07-15). Dead-link gate over exactly these five docs; all links in the demoted replacements must resolve.

---

## §1 — Context

The five root docs have a sound division of labor (README = human entry index; CLAUDE.md = agent orientation + gated lock surface; REPO_MAP = static layer map; PIPELINES = dynamic data-flow map; STATE = open-threads + forward-obligation register), but three duplication classes have crept in:

1. **Live-execution posture told three times** — CLAUDE.md §Live-execution posture (multi-paragraph), STATE.md's dated 2026-07-10/11/12/15 decision blocks, and PIPELINES.md's dormancy preamble — all re-summarizing the same Accepted ADRs (R6 NO-GO, FXIFY closure, claims re-scope, prop-portfolio reopen).
2. **Public-clone posture told twice** — README's three-class note duplicates CLAUDE.md's fuller §Public-clone posture.
3. **STATE.md grown past its charter** — its header says "not a state snapshot," yet ~72 lines of dated ADR re-summaries sat above the register content. This is the exact failure class Rule 7 was written for: on 2026-06-03, STATE.md silently drifted three weeks stale restating the strategy table and MC anchor. Narrative restatements drift the same way values do.

**Decision driver (one sentence):** the operator reviewed the five-doc split on 2026-07-16, ratified the file roles, and directed the three duplication classes be removed permanently rather than re-trimmed session by session.

---

## §2 — Decision

**Decision:** Ratify the five-root-doc charter and extend Rule 7 from canonical *values* to canonical *decision narrative*: the owning ADR is the sole home of a decision's retelling; root docs carry at most **one pointer line + one-line consequence** per standing decision.

Concretely (all executed with this ADR):

- **CLAUDE.md §Live-execution posture** → demoted to a pointer block: a short current-scale-path paragraph + one bullet per standing decision (bolded consequence + ADR link). The gated lock surface (Strategy Reference table, MC-anchor headlines, §Protection) is untouched.
- **STATE.md dated decision sections** → demoted to a compact "Executed operator decisions — pointer log" (one line per decision, newest first). Dormant threads, the discovery-campaign register, and the forward-trigger board stay. The harvest-intake §4 falsifier + idle guard move onto the forward board where they belong.
- **README.md §Public-clone note** → one sentence + link to CLAUDE.md §Public-clone posture.
- **`docs/operational_rules.md` Rule 7** → role list gains CLAUDE.md-§posture and README rows; dated edit-log entry added.

**Effective:** immediately.
**Scope:** the five root orientation docs (`README.md`, `CLAUDE.md`, `REPO_MAP.md`, `PIPELINES.md`, `STATE.md`). Future posture decisions add one pointer line to CLAUDE.md §posture and one to STATE.md's pointer log — never a retelling.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Merge CLAUDE.md into README (one entry doc) | Different consumers: README is the human index; CLAUDE.md is the agent-loaded orientation + machine-gated lock surface (`validate_params` / `verify_lock_anchors` parse it). Merging couples human prose churn to a parsed surface. |
| Collapse STATE.md into `docs/SESSIONS.md` | SESSIONS is an append-only per-session narrative; STATE is the mutable cross-session board (dormant threads + dated obligations) that no single session entry carries. Distinct jobs. |
| Also strip PIPELINES.md's dormancy preamble | Operator-scoped leave-alone; the one-paragraph dormancy read is load-bearing for its status column (a pipeline map that ignored dormancy would document machinery that isn't turning). It is a labeled framing paragraph, not a per-decision retelling. |
| Delete the historical posture facts outright | Over-retire — violates the 2026-07-11 rescope directive ("retire, but do not over-retire"). Demotion keeps every fact reachable one hop away in its ADR. |
| Status quo (re-trim ad hoc) | The 2026-06-03 incident shows restatements drift silently; without an ownership rule the retellings regrow with each new decision. |

---

## §4 — Falsifier (revert trigger)

**H:** one pointer line + one-line consequence per standing decision is sufficient orientation for the root docs — no future decision error will be attributable to the demotion (the fact was one ADR-hop away and the pointer named the consequence).

**Revert trigger (H falsified if):** a dated incident occurs in which a decision (operator, agent, or Cursor session) goes materially wrong **because** a fact removed from a demoted block was needed at orientation time and the one-hop ADR link did not surface it (i.e., the defect log of a session or a Rule 6 skew audit attributes the error to the demotion, not to a stale ADR).

**Revert action:** restore the specific inline block class that was needed (posture paragraph, STATE dated section, or README note) by superseding addendum on this ADR — not a silent regrow.

**Trigger check schedule:** rides the quarterly review dates (next 2026-08-08): confirm zero demotion-attributed defects, and spot-check that the pointer blocks have not regrown into retellings (§10 hooks).

---

## §5 — Forbidden moves (under this ADR)

- **Editing the gated lock surface while trimming CLAUDE.md** — the posture prose sits directly above the Strategy Reference table and repeats the anchor triple informally; it is tempting to "normalize" the parsed headline copies or the table while in the file. Ruled out: `verify_lock_anchors.py` treats every bolded headline as a pinned copy, and `validate_params.py` pins the table cells. Any anchor-block change requires its own re-MC governance, never a doc-cleanup ride-along.
- **Adding "just this once" narrative for the next big decision** — the next R6-scale decision will feel too important for one line. Ruled out: that is exactly how the current triple-telling accreted (07-10 → 07-11 → 07-12 → 07-15, each one paragraph at a time). The ADR carries the weight; the pointer carries the consequence.
- **Extending the demotion to REPO_MAP / PIPELINES** — tempting for symmetry (PIPELINES restates dormancy). Operator-scoped out; see §3.
- **Deleting STATE's one-liner facts that have no other committed home** (the 2026-07-10 operator retirements bullet, the local `accounts.json` migration note) — tempting as "not forward-board material." Ruled out: they are recorded one-line facts whose canonical homes are weak or local-only; dropping them is over-retirement.

---

## §6 — Consequences

**Positive:**
- One narrative owner per decision (the ADR); the drift surface shrinks from three tellings to one telling + pointers.
- CLAUDE.md orientation cost drops (~40 dense lines → ~15 pointer lines) without losing the load-bearing operational facts (`ACTIVE_FIRM` pin, 08-08-is-a-checkpoint, gated-rail status).
- STATE.md returns to its charter; its register content is findable again.

**Negative (real cost):**
- Detail is one hop away: an agent that reads only CLAUDE.md loses the inline nuance (e.g., the −$4,188.85 discretionary-tilt episode, P2 gate mechanics). Mitigation: each pointer names its consequence, and the ADR links are adjacent.
- One-line consequences are lossy compressions authored once; a badly compressed line could mislead until the ADR is opened. A dated incident of this class fires §4 and the demotion is FALSIFIED for that block class (restore by addendum); absent any such incident through two quarterly reviews, treat the charter as RESOLVED-stable.

**Risks:**
- A future session "helpfully" re-expands the pointers (the reverse failure). Mitigation: Rule 7 role rows + §10 size hooks make the regrowth mechanically visible.

**Downstream artifacts updated with this ADR:**
- `CLAUDE.md` (§Live-execution posture demoted), `STATE.md` (pointer log + forward-board harvest line), `README.md` (public-clone one-liner), `docs/operational_rules.md` (Rule 7 rows + edit log), `docs/SESSIONS.md` (session entry).

---

## §7 — Implementation plan

Executed in the same PR as this ADR (single-commit-family change):

- **Phase 0** — §0 reads (done; anchors above). Confirm `verify_lock_anchors.py --quiet` routes `Closed` pre-edit.
- **Phase 1** — the four doc edits per §2.
- **Phase 2** — grep-sweep: no remaining multi-paragraph posture retelling outside ADRs; all links in edited docs resolve (`check_root_doc_liveness.py`).
- **Phase 3** — verification block below passes; ADR lands `Accepted` (operator direction to execute was given in-session 2026-07-16).

---

## §10 — Audit hooks (runnable)

```bash
# 1. Gated surfaces still intact after any root-doc edit
python scripts/verify_lock_anchors.py --quiet     # expect: ROUTING: Closed (exit 0)
python scripts/validate_params.py                 # expect: exit 0
python scripts/check_root_doc_liveness.py         # expect: exit 0

# 2. Posture block has not regrown into a retelling (pointer block ≈ 15 lines)
awk '/^## Live-execution posture/,/^## Architecture/' CLAUDE.md | wc -l   # expect: <= 25

# 3. STATE.md carries no dated decision sections (pointer log only)
grep -cE '^## 2026-' STATE.md                     # expect: 0

# 4. README public-clone note stays a one-liner + link
awk '/^## Public-clone note/,0' README.md | wc -l # expect: <= 8

# 5. Rule 7 role rows present
grep -n 'Live-execution posture' docs/operational_rules.md   # expect: >= 1 hit
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-16-root-doc-charter-dedup.md --type adr
# §0 anchors re-checkable:
git log -1 --format='%h' -- CLAUDE.md STATE.md README.md docs/operational_rules.md
# Downstream sweep = §10 hooks 1–5 above.
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Initial authoring + same-session execution | Joshua + Claude Code |
