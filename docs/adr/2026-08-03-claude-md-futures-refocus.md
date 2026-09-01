# ADR — Root docs re-chartered futures-first; CFD-era narrative demoted; CFD-strategy code retirement scoped (not executed)

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-23-strategy-coldstore-phase-c.md` — §7 CFD living-`BASE_RISK` / CLAUDE table retirement executed (Striker keys + `LEG_MAP` stay)
**Retain-until:** none
**Decision date:** 2026-08-03
**Authors:** Joshua + Claude Code
**Supersedes:** none (extends [`2026-07-16-root-doc-charter-dedup.md`](2026-07-16-root-doc-charter-dedup.md) — same demotion discipline applied to the Purpose + reference sections; adds the era-closure aggregation form)
**Related:** [`2026-07-16-root-doc-charter-dedup.md`](2026-07-16-root-doc-charter-dedup.md); [`2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md); [`2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md); [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md)
**Layer:** infrastructure (governance docs)

---

## §0 — Rule 0 reads (production-source verification)

All read in-session on 2026-08-03, before authoring (anchors = `git log -1 --format='%h %ci' -- <path>`):

- `CLAUDE.md` — anchor `c619135` (2026-08-03, pre-edit state). Purpose still framed the repo around the CFD-era locked book; posture intro had regrown into a multi-decision retelling (five-session arming chronicle, Net-Liq arithmetic, alert-shadowing remedy narrative).
- `README.md` — anchor `0091c5f` (2026-08-02). Opening paragraph restated the old locked-book-first purpose.
- `scripts/validate_params.py` — anchor `f2be990` (2026-07-11). `check_claude_md()` HARD-pins the CLAUDE.md Strategy Reference table: all four rows by name (`CLAUDE_MD_NAME_MAP`), with risk% (cells[2]), contractValue (cells[4]), and version (cells[3]) checked against `params.toml`. A missing row is a HARD violation. This is the only content-parsing gate on CLAUDE.md (confirmed by grep over `scripts/`); `check_root_doc_liveness.py` additionally requires links to resolve.
- `scripts/verify_lock_anchors.py` — anchor `bd92d8e` (2026-07-24). Post-Phase-3 it reads only `dd_protection.py` + `params.toml`; it does NOT parse CLAUDE.md. (The 07-16 charter §0's note about bolded-MC-headline parsing is stale for this script — the MC-headline prose in CLAUDE.md is no longer machine-pinned.)
- `ops/c1_rail/c1_sizing_host_reference.py` — anchor `c134060` (2026-07-24). Line 52 imports `BASE_RISK` from `dd_protection`; the leg map consumes `BASE_RISK["Striker"]` (MYM) and `BASE_RISK["Striker NAS100"]` (MNQ) at lines 87/93/121. The two Striker table rows are therefore LIVE sizing inputs, not historical residue.
- `docs/adr/2026-07-16-root-doc-charter-dedup.md` — anchor `ba943a1` (2026-07-17). Demotion discipline + §10 size hooks (posture awk ≤ 25 lines); §5 forbids editing the gated lock surface during doc cleanup.
- `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` — anchor `0091c5f` (2026-08-02). §Phase 6 verified: "consolidated documentation and completion" (root-doc updates, final suite, offline-copy destruction) — NOT strategy-code retirement. The follow-up project scoped in §7 below is therefore new, not a duplicate of Phase 6.

---

## §1 — Context

Operator direction 2026-08-03 (in-session): re-charter the root docs **futures-first** — the repo is the research + operational layer for finding and deploying automated futures strategies at automation-friendly prop firms, with the Tradeify Select 100K eval as the sole live account; delete the CFD strategies and requirements from the orientation surface; simplify explanations without dropping load-bearing detail. Since the 07-16 charter executed, two drift classes had re-emerged: the §Live-execution posture intro regrew into a retelling (the exact failure class the charter §6 flagged as a risk), and the §Purpose still described the operation the repo no longer runs. Three operator rulings were taken in-session: (1) Strategy Reference table handling → **retire the CFD strategies from code as a separately-gated follow-up project — scoped here, not executed**; the table stays machine-pinned this pass; (2) the five CFD-era closure bullets → **aggregate into one era-closure pointer line**; (3) record the restructure in this ADR.

**Decision driver (one sentence):** the operator read the entire CLAUDE.md on 2026-08-03 and directed the futures refocus as a standing re-charter, not a session-local trim.

---

## §2 — Decision

**Decision:** Re-charter the agent-orientation root docs futures-first: CLAUDE.md's Purpose describes the prop-portfolio futures program (discover → validate → deploy at four automation-friendly firms; sole live account `Tradeify_Select_100K` via the c1 rail), and CFD/challenge-era content survives only as pointer lines — including one **aggregated era-closure line** carrying all five closure decisions' consequences + ADR links, an admitted form under the charter's "at most one pointer line + one-line consequence per standing decision."

Concretely (all executed with this ADR):

- **CLAUDE.md §Purpose** rewritten futures-first; locked-book/FXIFY/CFD framing removed; multiplier retirement kept as one clause.
- **README.md opening** aligned to the same purpose statement.
- **§Live-execution posture intro** compressed to program + rail state + safety invariants (disarm-before-`armed_until`, arm gated on M1 `RESOLVED`, account-not-pristine, B7-REFIRE owed); the session chronicle lives in `RUNBOOK.md` §B6–B7. Bullets reordered futures-first; the two ORB bullets merged into one arc; the five CFD-era closures (manual/CFD/FXIFY close, R6 NO-GO, claims re-scope, D2 revert-check retirement, locked-book-untouched) aggregated into one pointer line with every ADR link retained.
- **CFD-era analytic narrative** (per-strategy baselines, MC anchor mechanics, regime caveat, overlay history, Q-SWAP, C0→C2 relock grounds) demoted to a "Historical CFD-era record" pointer list; §Protection keeps the live rule, the frozen constants, the lost-revert-triggers ⚠, and the standing change-control chain in force.
- **Strategy Reference table stays byte-intact** (machine-pinned; Striker rows are live c1 inputs), reframed as "LOCKED legacy book" with the pin + live-consumption rationale stated inline.
- **Multiplier System section deleted**; retirement + no-rebuild caveat carried by the §Purpose and §CLI one-liners.
- Architecture retired-surface enumerations, Firm Expansion archaeology, Public-clone posture, and the vendor-gate tombstone chain compressed to pointers; all live gates and rules retained verbatim in effect.

**Effective:** immediately.
**Scope:** `CLAUDE.md`, `README.md` opening (+ `STATE.md` pointer-log line, `docs/SESSIONS.md` entry, `docs/adr/INDEX.md` regeneration). The CFD-strategy **code** retirement is explicitly OUT of scope — see §7.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep the old Purpose, trim prose only | Operator-overruled 2026-08-03 — the doc's declared purpose no longer matched the operation it orients. |
| Delete the Strategy Reference table + retire the CFD strategies from code in the same pass | `validate_params.check_claude_md` HARD-fails on any missing row; `BASE_RISK["Striker"]` / `BASE_RISK["Striker NAS100"]` are live c1 sizing inputs; the deletion cascades across `core/` + `params.toml` + validator fixtures + manifests + tests. That is a gated engineering project, not a doc edit — scoped in §7, awaiting its own ADR + operator GO. |
| Move the table to a separate doc and repoint the validator | Touches the validator + its self-test fixtures for purely cosmetic gain; re-examine inside the code-retirement project if it proceeds. |
| Keep five separate CFD closure bullets (charter-literal) | Operator chose aggregation 2026-08-03; every decision's link + consequence is retained inline, satisfying the charter's "at most one pointer line per standing decision." |
| Status quo (re-trim ad hoc) | The posture intro regrew within 15 days of the charter; without a recorded re-charter the CFD framing regrows the same way. |

---

## §4 — Falsifier (revert trigger)

**H:** the futures-first re-charter loses nothing load-bearing — no future decision error will be attributable to a fact this pass demoted, aggregated, or deleted (each fact remains one ADR/RUNBOOK hop away with its consequence named in the pointer).

**Revert trigger (H falsified if):** a dated incident occurs in which a decision (operator, agent, or Cursor session) goes materially wrong **because** a fact removed or aggregated by this pass was needed at orientation time and the one-hop link did not surface it — i.e., a session defect log or Rule 6 skew audit attributes the error to this demotion rather than to a stale ADR.

**Revert action:** restore the specific block class that was needed (posture chronicle, MC-anchor narrative, separate closure bullet, README framing) by superseding addendum on this ADR — never a silent regrow.

**Trigger check schedule:** rides the 2026-08-08 review and subsequent quarterly reviews, alongside the 07-16 charter's own §4 check.

---

## §5 — Forbidden moves (under this ADR)

- **Editing the Strategy Reference table cells or §Protection constants while trimming** — they are validator-pinned mirrors of live constants (and the Striker rows feed live c1 sizing); any value change requires its own re-MC governance, never a doc-cleanup ride-along. Inherited verbatim from charter §5; it was live temptation again this pass ("delete the CFD strategies" reads naturally as "delete the table").
- **Deleting the era-closure pointer line entirely** — genuinely tempting under "futures focus"; ruled out because a future session that rediscovers FXIFY/CFD code paths, docs, or data needs the closure signal one hop away ("retire, but do not over-retire", 2026-07-11 directive).
- **Starting the CFD code retirement now because §7 already contains the scope** — the scope sketch is not a GO. Execution needs its own admitting ADR, an engine-support pre-flight (§Firm Expansion doctrine), and an operator lifecycle disposition for the four legs.
- **Re-expanding the posture intro at the next incident** — that is exactly how the arming chronicle accreted (07-20 → 07-31, one incident at a time). RUNBOOK owns the chronicle; the intro carries only standing invariants.

---

## §6 — Consequences

**Positive:**
- Orientation reads futures-first; the Purpose matches the operation actually being run (prop-portfolio + c1/Tradeify).
- The drift surface shrinks again: one telling + pointers, now including the Purpose and reference sections the 07-16 charter left untouched.
- The CFD→futures boundary is now explicit in the doc: what is live (c1 rail, DD rule, lifecycle, gates, two Striker legs' constants) vs. what is historical record.

**Negative (real cost):**
- The arming chronicle, MC-anchor mechanics, relock grounds, and Q-SWAP caveats are one hop away (RUNBOOK / `docs/mc_anchor_history.md` / ADRs); a badly compressed pointer could mislead until the target is opened — same accepted cost class as charter §6, same falsifier protection (§4).
- The era-closure aggregate is lossier than five separate bullets; mitigated by keeping each decision's consequence + link inline.

**Risks:**
- Regrowth (the reverse failure) — mitigated by the charter §10 size hook plus this ADR's §10 greps.
- The aggregate line becoming a dumping ground for future closures — only decisions belonging to the CLOSED CFD/challenge era may join it; new posture decisions still get their own line.

**Verdict rule:** a dated §4-attributed incident **FALSIFIES** the demotion for that block class (restore by addendum); absent any such incident through two quarterly reviews (2026-08-08 + the next), treat the re-charter as **RESOLVED**-stable; a disputed attribution routes **AMBIGUOUS** to the next programme audit.

**Downstream artifacts updated with this ADR:**
- `CLAUDE.md` (full revamp per §2), `README.md` (opening), `STATE.md` (pointer-log line), `docs/SESSIONS.md` (session entry), `docs/adr/INDEX.md` (regenerated).

---

## §7 — Implementation plan

Executed in the same PR as this ADR: the §2 edits, the downstream artifact updates, and the §10 verification battery.

**Scoped follow-up — CFD-strategy code retirement (NOT executed here; separately gated):**

- **Target:** remove the venue-less CFD legs (**Guardian XAUUSD, Aegis USDJPY**) from the active code path. **Striker DJ30 / Striker NAS100 constants STAY** — they are live c1 sizing inputs via the sizing-host leg map (§0 read).
- **Touch list (from the §0 reads):** `core/dd_protection.py::BASE_RISK`, `core/firm_rules.py::_BASE_RISK`, `core/mc/modes.py::ALLOCATIONS`, `core/csv_parser.py::STRATEGY_DAYS`, `core/config/params.toml [strategies]`, `scripts/validate_params.py` key maps + `tests/validator_fixtures/`, the CLAUDE.md table rows, per-strategy `LOCK.md`s, `core/strategies/MANIFEST.sha256`, and dependent tests. Recommended retention: the 4-leg synthetic fixtures in `tests/core/test_mc_synthetic_engine.py` (vendor-free engine regression is calibration-independent and should survive the leg removal).
- **Prerequisites before any execution:** (1) an operator **lifecycle disposition** for the affected legs — all four are currently `AUTHORIZED · MECHANISM @ 1.00×`, and removing code without an authorization-axis ruling would contradict the lifecycle ADR; (2) an **admitting ADR + engine-support pre-flight** per §Firm Expansion doctrine; (3) a **historical-record retention decision** (LOCK.md files, MC anchor records — "retire, but do not over-retire").
- **Trigger:** operator GO; no date attached.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Gated surfaces intact after the revamp
python scripts/verify_lock_anchors.py --quiet     # expect: ROUTING: Closed (exit 0)
python scripts/validate_params.py                 # expect: exit 0 (table rows intact)
python scripts/check_root_doc_liveness.py         # expect: exit 0 (all links resolve)

# 2. Posture block has not regrown (charter hook, inherited)
awk '/^## Live-execution posture/,/^## Architecture/' CLAUDE.md | wc -l   # expect: <= 25

# 3. Era-closure aggregate present exactly once; old purpose framing gone
grep -c 'CFD / challenge era CLOSED' CLAUDE.md            # expect: 1
grep -c 'locked four-strategy' CLAUDE.md README.md         # expect: 0 per file

# 4. Pre-code-retirement invariant: c1 sizing host still consumes Striker keys
grep -n 'Striker' ops/c1_rail/c1_sizing_host_reference.py          # expect: leg_key hits (lines ~87/93)

# 5. Follow-up project not silently started (no admitting ADR => keys still present)
grep -c '"Guardian"' core/dd_protection.py                 # expect: >= 1 until the gated ADR lands
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-03-claude-md-futures-refocus.md --type adr
# §0 anchors re-checkable:
git log -1 --format='%h' -- CLAUDE.md README.md scripts/validate_params.py scripts/verify_lock_anchors.py ops/c1_rail/c1_sizing_host_reference.py
# Downstream sweep = §10 hooks 1–5 above.
```

---

## Addendum 2026-08-03a — scope extended to PIPELINES.md (operator direction)

The 2026-07-16 charter ADR §3 ruled "also strip PIPELINES.md's dormancy preamble" **out of scope** as an operator-scoped leave-alone, on the grounds that its one-paragraph dormancy read was load-bearing for its status column. **Operator direction 2026-08-03 supersedes that**: PIPELINES.md was reviewed in the same pass and directed toward deletion/simplification. Recorded here rather than executed silently (§5 forbids silent scope amendment).

**Executed:** posture retellings removed (the dormancy preamble, the P5 arming chronicle, and the closing current-state summary were all re-tellings of CLAUDE.md §Live-execution posture — the same duplication class the charter targets); the unique data-flow content was retained in full (P1 stage diagram, inputs/transforms/outputs table, ratified rules of evidence, P3 module chain, P5 repo touchpoints, the X governance table, and the data-stores table). 30,354 → 18,992 bytes.

**Three stale/contradictory facts were corrected, not merely compressed** — each had drifted because the posture was told in two places:

1. **P2 contradicted itself** — the inventory row said `RETIRED 2026-08-02` while the section heading said `PARKED`. RETIRED is correct.
2. **"amendment unwritten"** appeared in three places (header, P5 inventory row, P5 body) asserting the M1 gate-crossing amendment was still owed. It was **written and ratified 2026-07-31** (Addendum 2026-07-31b, 5 occurrences in the monitoring ADR). Corrected by pointing at CLAUDE.md rather than restating.
3. **Pepperstone tombstone pointer** — the data-stores table linked `2026-08-03-pepperstone-data-tombstone.md` while the adjacent row already named the **2026-08-02** one canonical and flagged the 08-03 record's no-rollback claim as corrected. Now points at the canonical 08-02 tombstone + the feed-retirement ADR. The 08-03 file is not orphaned (still referenced by its corrector, `STATE.md`, and `docs/SESSIONS.md`).

This is direct evidence for the charter's §1 premise: narrative restatements drift, and the drift shows up as internal contradiction rather than as a visible error.

**Falsifier:** unchanged — §4 above now also covers the PIPELINES.md block classes demoted here.

---

## Addendum 2026-09-01 — §10 audit-hook staleness (diagnostic only, no disposition)

Re-checked 2026-09-01 during the coldstore-pair ADR cluster audit (commands run against the current tree):

1. **Hook #1** (`python scripts/validate_params.py` — "expect: exit 0") — the script no longer exists. A same-day **sibling** ADR, [`2026-08-03-params-toml-gate-retirement.md`](2026-08-03-params-toml-gate-retirement.md) (not this ADR, and does not supersede it), retired the whole `params.toml` hub gate and deleted `scripts/validate_params.py`. Running the hook now fails on "file not found," not the documented "exit 0." That ADR's own §10 names the live replacement: `python scripts/check_pine_manifest.py`.
2. **Hook #2** (posture-block size, `awk '/^## Live-execution posture/,/^## Architecture/' CLAUDE.md | wc -l` — "expect: <= 25") — now measures 54 lines. Part of the growth is the "Standing decision" pointer table added after this ADR (one row per decision — the compact discipline this ADR itself calls for), not necessarily the narrative regrowth §5 warned against — but the hook's literal threshold no longer holds, and it does not distinguish the two shapes of growth.
3. **Hook #3a** (`grep -c 'CFD / challenge era CLOSED' CLAUDE.md` — "expect: 1") — now returns 0; the aggregated era-closure line's exact wording has since changed under later posture edits.

Hooks #3b and #4 still pass as documented. Hook #5 (`grep -c '"Guardian"' core/dd_protection.py` expect `>=1` "until the gated ADR lands") now returns 0 — already accounted for by this ADR's own header `Superseded-in-part-by` pointer to Phase C, which executed exactly that retirement.

**Not decided here — operator call:** whether to repair hooks #1–#3a to match current CLAUDE.md phrasing/tooling, mark them historical-only (this ADR's live audit surface has largely been superseded by later ADRs' own hooks), or leave them as a dated record of what this ADR checked at authoring time. No disposition is made in this addendum.

**Falsifier read:** this is audit-hook staleness from normal subsequent doc/tooling evolution, not evidence that this ADR's own §4 H was falsified — no incident is attributed to lost load-bearing content, so §4 remains unfired.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-03 | Initial authoring + same-session execution | Joshua + Claude Code |
| 2026-08-03 | Addendum 2026-08-03a — scope extended to PIPELINES.md per operator direction; three stale facts corrected | Joshua + Claude Code |
| 2026-09-01 | Addendum: §10 audit-hook staleness (3 of 5 hooks now fail on normal subsequent doc/tooling evolution); diagnostic only, operator call on repair | Claude Code (ADR-corpus reconciliation sweep) |
