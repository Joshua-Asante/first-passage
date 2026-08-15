# ADR 2026-05-28 — Audit-doc generation doctrine for locked-strategy parity grounding

**Status:** Accepted
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-05-28
**Authors:** Joshua + claude.ai (advisor)
**Related:** [Q-PARITY-1](../ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md) (parent Pre-Q whose §1 observation #2 + Phase 0 Concern §C1 motivate this ADR); [docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md](../audits/2026-05-08-guardian-v55-indicator-strategy-diff.md) (the template)
**Layer:** methodology

---

## §0 — Rule 0 reads (production-source verification)

Reads completed before authoring; anchors verifiable post-hoc.

- [`docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md`](../audits/2026-05-08-guardian-v55-indicator-strategy-diff.md) — anchor: `948f76a` 2026-05-09 (verified during Q-PARITY-1 Phase 0). The template this ADR generalizes. Audit doc line 156 carries the Tier 1 numeric quote (`atrLength=14, proximityAtr=0.50, strictProximity=0.15, emaSlowLen=385, entryEmaLen=25`) verified EXACT match on 2026-05-28.
- [`docs/ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md`](../ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md) — anchor: `b4d7f56` 2026-05-28 (post-§0-finalization commit). §1 observation #2 named the per-strategy audit-doc asymmetry repo gap as out-of-scope-but-known; Phase 0 Concern §C1 surfaced BRIEF-ONLY classification for all load-bearing booleans across Aegis/DJ30/NAS100; §Verification block declares Joshua leans Path B as of 2026-05-28.
- [`docs/ltm/briefs/handoffs/2026-05-28-cc-handoff-Q-PARITY-1-phase-0.md`](../ltm/briefs/handoffs/2026-05-28-cc-handoff-Q-PARITY-1-phase-0.md) — anchor: `85374af` 2026-05-28. Closure report inline in spawn return (DONE_WITH_CONCERNS as designed) enumerates the five Concerns including the load-bearing C1 + C3 that this ADR addresses.
- [`core/strategies/guardian/LOCK.md`](../../core/strategies/guardian/LOCK.md) — anchor: `948f76a` 2026-05-09. Tier 2 reference for the Guardian template's quality bar.
- `.gitignore:50` — `**/*.pine` (verified `grep -nE '\\*\\.pine' .gitignore` returns `50:**/*.pine`). Pine source stays gitignored per 2026-05-28 repo-posture decision (public repo stays public; ungitignoring Pine rejected explicitly).
- `gh repo view` — confirmed `isPrivate: false`, public at `https://github.com/Joshua-Asante/multi_firm_operations`. Frames the bounded-Pine-leak constraint this ADR operates under.

---

## §1 — Context

Q-PARITY-1 Phase 0 (2026-05-28) returned DONE_WITH_CONCERNS with three Tier-3-only strategies (Aegis v4.3, DJ30 v4.5, NAS100 v1) showing BRIEF-ONLY classification for all load-bearing booleans + anticipation predicates. The strategy CHANGELOGs corroborate filter *behavior* (sessions, day restrictions, hour blocks, ATR floors) but do not enumerate filter *boolean variable names* — the May 19 brief is the only on-disk source naming `filters_pass`, `filtersOK`, `anticip_pass`, `anticipOK`, `approachZone`, `strictApproach`, etc. Guardian alone has a Tier 1 audit doc (the 2026-05-08 indicator-vs-strategy diff) providing nominal grounding.

Two paths to unblock Q-PARITY-1 Phase 1 were surfaced and explicitly considered on 2026-05-28: Path A (accept BRIEF-ONLY on Joshua's personal Pine knowledge; Phase 1 schema locks against brief variable names) or Path B (defer Phase 1 until Tier 1 audit docs land for the three Tier-3-only strategies; closes the underlying repo gap). Joshua chose Path B. Same-day, the alternative-efficiency-unlock question (could `.gitignore` be relaxed to make Pine readable) was decided as: repo stays public, Pine stays gitignored. That decision frames this ADR — the audit-doc path is the structural fix that respects the public-repo posture.

**Decision driver (one sentence):** Q-PARITY-1 Phase 1 cannot be authored until Aegis/DJ30/NAS100 state-var inventories convert from BRIEF-ONLY to CONFIRMED, and the chat-paste-per-handoff alternative doesn't compound across Q-PARITY-N or future briefs touching these strategies.

---

## §2 — Decision

Three Tier 1 audit docs land — one each for Aegis v4.3, Striker DJ30 v4.5, Striker NAS100 v1 — modeled on the [`2026-05-08-guardian-v55-indicator-strategy-diff.md`](../audits/2026-05-08-guardian-v55-indicator-strategy-diff.md) template.

**Authoring mechanism:** collaborative per-strategy claude.ai chat session. Joshua pastes the indicator + strategy Pine source for one strategy; claude.ai structures the audit doc to template parity (indicator-vs-strategy diff, state-var enumeration with name + type + definition, numeric constants tabulated, anticipation predicates classified, hypothesis verdict block where applicable). One strategy per session; three sessions total.

**Filename convention:** `docs/audits/<YYYY-MM-DD>-<strategy>-v<version>-indicator-strategy-diff.md`. Examples: `docs/audits/2026-05-29-aegis-v43-indicator-strategy-diff.md`, etc. Date is the audit doc authoring date; version is the locked version per ADR 2026-05-23-allocation-refresh-2.

**Version pinning:** each audit doc carries the Guardian template's "Audit dated YYYY-MM-DD audits vX.Y LOCKED YYYY-MM-DD" line in its header — anchors the audit to a specific Pine version. If the Pine version changes, a new audit doc is authored; old one stays in `docs/audits/` as historical record.

**Effective:** Immediately upon Acceptance.
**Scope:** All four locked strategies per ADR 2026-05-23-allocation-refresh-2 (Guardian already has one; the three Tier-3-only get parity). Pattern reusable when a fifth strategy is admitted — audit doc lands as part of lock-completion checklist, parallel to the "operational tooling integrated" sub-rule in lock procedures.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Path A — accept BRIEF-ONLY on Joshua's personal Pine knowledge** | Lower friction but creates audit-trail asymmetry (3 of 4 strategies lack reproducible grounding). Each future brief touching these strategies re-introduces Phase 0 Concern §C1; the discipline cost compounds. Joshua leaned Path B explicitly per 2026-05-28 Q-PARITY-1 §Verification status. |
| **Chat-paste-during-handoff per session** | Same per-session authoring effort, no compounding. Each future CC handoff against these strategies needs a fresh Pine paste. Audit-doc workstream front-loads cost once; benefit accrues across Q-PARITY-N for n>1 plus any future brief touching these strategies. |
| **`.local/` gitignored Pine cache + SHA manifest** | Workable but creates reproducibility problem (Pine source at session-time isn't tracked); SHA manifest mitigation adds infrastructure without compounding benefit beyond the immediate session. Audit doc IS the durable artifact and matches the Guardian pattern already in use. |
| **Make repo private + remove Pine from gitignore** | Explicitly rejected on 2026-05-28 (`gh repo view` confirms `isPrivate: false`, user chose "stay public, find different efficiency unlock"). Public-clone posture stays. |
| **Bundle three audit docs into one CC handoff** | Each strategy needs Joshua-side Pine reads + judgment on what counts as a state-var. CC cannot read Pine (gitignored); the authoring must be Joshua-led. Bundling defeats per-strategy quality. Three separate sessions. |
| **Status quo — do nothing** | Q-PARITY-1 Phase 1 stays blocked indefinitely. Per-strategy audit-doc asymmetry remains a permanent repo gap. Future briefs continue hitting Concern §C1. |

---

## §4 — Falsifier (revert trigger)

This ADR assumes the indicator-vs-strategy diff is non-trivial for each of the three target strategies. Guardian's audit doc is ~200 lines of substantive diff (indicator + strategy are meaningfully different code paths). If for any strategy the diff turns out to be trivial (strategy script is a thin wrapper around the indicator's `signal_fired` output with no independent BE/trail/exit/pyramid logic, producing a diff doc < 50 lines of substantive content), then the full audit-doc treatment is over-engineered for that strategy.

**Revert trigger (per-strategy):** If during the authoring session the indicator-vs-strategy diff for a strategy produces < 50 lines of substantive content (counting actual differences, not headers/scaffolding), halt before landing; switch to the **annex pattern** for that strategy.

**Annex pattern (fallback):** Author a `strategies/<strategy>/<strategy>_state_vars.md` file (sibling to LOCK.md) enumerating named state-vars with definitions, but without the full diff treatment. This delivers Tier 1 nominal grounding (state-var names are quoted from Pine) without the full audit-doc ceremony.

**Trigger check schedule:** Per-strategy, during the authoring session itself (not after-the-fact). Joshua + claude.ai assess substantive-diff line count before declaring the audit doc complete.

**Revert action:** Replace the full audit doc with the annex; update this ADR's Change history with the per-strategy variance.

---

## §5 — Forbidden moves

- **Do NOT skip the indicator-vs-strategy diff and only list state-vars.** The diff is the load-bearing artifact for parity testing (it shows whether strategy and indicator can disagree on any bar — exactly Q-PARITY-1's question). State-var listing without the diff is half the work and produces a Tier 1 doc that doesn't actually support the downstream brief's reasoning. The annex pattern (§4 revert) is the explicit lighter alternative for the trivial-diff case; it is NOT a default.
- **Do NOT bundle three audit docs into one CC handoff or one claude.ai chat session.** Per-strategy authoring quality requires per-strategy attention. CC also cannot read Pine (gitignored per repo posture). Three separate Joshua-led claude.ai sessions.
- **Do NOT "harmonize" the three audit docs against the Guardian template via post-hoc edits.** Each strategy's Pine has its own idioms (Aegis is mean-reversion on BB; DJ30/NAS100 are breakout with pyramid). Force-fitting Guardian's trend-rider structure where it doesn't apply is the silent-substitution pattern in another domain. Template is a starting point, not a Procrustean bed. The hypothesis verdict block (Guardian audit doc §4) applies only where there's a meaningful hypothesis to verdict against.
- **Do NOT commit Pine source beyond the minimal verbatim quotes needed to anchor the diff claims.** Audit doc excerpts must be bounded: function signatures, constant declarations, structural patterns are in-scope; full function bodies, complete entry/exit logic blocks, pyramid mechanics in full are out-of-scope. The repo public-posture decision (2026-05-28) protects the edge by keeping Pine gitignored; audit docs widen the leak surface but must not expand it beyond what is necessary for grounding.
- **Do NOT make audit docs Tier 1 for sections of Pine they do not directly quote.** Per brief-authoring SKILL.md §0 citation-chain sub-rule, Tier 1 requires verbatim quote. If a state-var is described but not quoted in the audit doc, it grounds at Tier 2 (audit-doc paraphrase), not Tier 1. Downstream briefs citing the audit doc must respect this distinction.
- **Do NOT defer audit-doc landing on "we'll do it later" grounds without superseding this ADR.** If after one or two audit docs land Joshua decides the workstream isn't earning its keep, supersede this ADR with one explicitly switching the remaining strategies to a different pattern. Silent abandonment of the third doc is the methodology p-hacking pattern (Known Trap #12 in brief-authoring).

---

## §6 — Consequences

**Positive consequences:**
- Q-PARITY-1 Phase 1 unblocks immediately once the three audit docs land (Phase 1 handoff authors once §0 Layer 2 re-grounds Aegis/DJ30/NAS100 from Tier 3-only to full Tier 1/2/3).
- Future briefs touching Aegis/DJ30/NAS100 inherit Tier 1 grounding — compounding benefit across Q-PARITY-N for n>1 and any non-parity brief (e.g., a future cap-family or DDP investigation on one of these strategies).
- Per-strategy audit-doc asymmetry repo gap closes (parent Q-PARITY-1 §1 observation #2 resolved).
- Pattern reusable: when a fifth strategy is admitted, the audit doc lands as part of lock-completion (parallel to "operational tooling integrated" sub-rule in lock procedures, per SKILL.md §0).

**Negative consequences (real cost):**
- ~3 hours front-loaded authoring across 3 sessions (estimate: ~45–60 min per strategy at Guardian-template parity).
- Each audit doc adds ~150–250 lines to the repo (modest).
- Audit docs need maintenance when Pine changes — manual sync, no automated drift detector. Mitigation: lock-decision brief checklist gets an "audit doc updated" item on future strategy version locks.
- Bounded Pine leak surface in audit doc excerpts. Wider than current state (no excerpts) but narrower than full Pine commit. Joshua accepted this trade-off implicitly by choosing audit-doc path over `.local/` cache; the §5 forbidden move on excerpt scope bounds the leak.

**Risks (probabilistic):**
- **Audit doc drift when Pine updates.** If a v4.3.2 / v4.5.2 / v1.1 patch lands without updating the audit doc, downstream briefs citing Tier 1 from the audit doc would be silently grounded against stale Pine. Mitigation: audit doc carries explicit version-pin (`audits vX.Y LOCKED YYYY-MM-DD`); pre-commit or pre-lock check that audit doc version matches CLAUDE.md Strategy Reference table.
- **Trivial-diff strategies degrade the doctrine.** If 2 of 3 fall back to annex pattern, the ADR is over-scoped — should have been "audit doc OR annex, evaluate per-strategy" from the start. §4 revert handles this per-strategy; aggregate ADR re-evaluation if ≥2 of 3 trigger.

**Downstream artifacts that need updating:**
- [`docs/ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md`](../ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md) §0 Layer 2 (Aegis/DJ30/NAS100 rows): re-ground from Tier 3-only to full Tier 1/2/3 chain after each audit doc lands. §Verification block updates when all three landed.
- `CLAUDE.md` Methodology references list: optional addition of "audit-doc generation doctrine" pointer to this ADR. Defer unless a third brief cites the pattern.
- Lock-decision brief template (future addition): "Tier 1 audit doc present" checklist item. Defer to next lock-decision authoring.

---

## §7 — Implementation plan

- **Phase 0** — Joshua opens a fresh claude.ai session per strategy. Pastes the indicator Pine + strategy Pine source for that strategy. Confirms current locked version against ADR 2026-05-23-allocation-refresh-2 (Aegis v4.3, DJ30 v4.5, NAS100 v1).
- **Phase 1** — Claude.ai authors the audit doc following the 2026-05-08 Guardian template: §0 Rule 0 reads, §1 indicator-vs-strategy diff, §2 state-var enumeration with name + type + definition, §3 numeric constants tabulated, §4 anticipation predicates classified, §5 hypothesis verdicts (if applicable to the strategy's design intent — Aegis is mean-reversion so hypothesis verdicts may be light; breakout strategies may have more substantive verdicts).
- **Phase 2** — Joshua reviews audit doc against actual Pine source for accuracy; corrections applied. §4 falsifier check: substantive-diff line count ≥50? If yes, proceed; if no, switch to annex pattern per §4 revert.
- **Phase 3** — Audit doc commits to `docs/audits/`. Q-PARITY-1 §0 Layer 2 row for that strategy updates: Tier 3-only contingency replaced with full Tier 1/2/3 chain (mirror Guardian row structure).
- **Phase 4 (after all three landed)** — Q-PARITY-1 §Verification block updates: "Phase 0 status" advances to "all 4 strategies Tier 1 grounded; Path B execution complete." Phase 1 handoff for Q-PARITY-1 becomes authorable.

Authoring order: **Aegis first** (smallest expected diff — Aegis is the simplest of the three by §1 of the May 19 brief's grep-sweep table; tests the §4 falsifier first). **DJ30 second.** **NAS100 third** (largest expected complexity due to pyramid-anticipation predicates per Phase 0 Concern §C3).

---

## §10 — Audit hooks (runnable)

```bash
# Confirm audit docs exist for all 4 locked strategies
$ ls docs/audits/*-indicator-strategy-diff.md 2>&1
# Expected after Phase 3 of each: 4 files (Guardian + 3 new)

# Per audit doc, confirm version-pin matches current locked version
$ for f in docs/audits/*-indicator-strategy-diff.md; do
    echo "=== $f ==="
    grep -E "audits v[0-9.]+ LOCKED" "$f" | head -1
  done
# Expected: each line matches the locked version per ADR 2026-05-23-allocation-refresh-2
#   Guardian → audits v5.5 LOCKED 2026-04-23
#   Aegis    → audits v4.3 LOCKED 2026-04-23
#   DJ30     → audits v4.5 LOCKED 2026-05-05
#   NAS100   → audits v1   LOCKED 2026-05-05

# Confirm Q-PARITY-1 §0 Layer 2 re-grounded for each strategy
$ grep -B1 -A3 "Aegis v4.3 \|DJ30 v4.5 \|NAS100 v1 " docs/ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md | head -20
# Expected after Phase 3 of each: Tier 1 row populated (not "Tier 3-only contingency")

# Confirm no Pine source landed in repo (gitignore intact per 2026-05-28 posture decision)
$ find . -name "*.pine" -not -path "./.git/*" 2>&1
# Expected: empty

# Audit-doc-drift check (manual; runs at next lock-decision authoring)
$ for strat in guardian aegis striker-dj30 striker-nas100; do
    audit=$(ls docs/audits/*-${strat}-*-indicator-strategy-diff.md 2>/dev/null | tail -1)
    [ -z "$audit" ] && echo "MISSING audit for $strat" && continue
    audit_version=$(grep -E "audits v[0-9.]+ LOCKED" "$audit" | head -1)
    echo "$strat: $audit_version"
  done
# Cross-check against CLAUDE.md Strategy Reference table
```

---

## Verification

```bash
# Discipline check on this ADR
$ PYTHONIOENCODING=utf-8 python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-05-28-audit-doc-generation-doctrine.md --type adr

# §0 anchor verification
$ git log -1 --format='%h %ci' -- docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md
$ git log -1 --format='%h %ci' -- docs/ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md
$ git log -1 --format='%h %ci' -- docs/ltm/briefs/handoffs/2026-05-28-cc-handoff-Q-PARITY-1-phase-0.md
$ git log -1 --format='%h %ci' -- strategies/guardian/LOCK.md
$ grep -nE "\*\.pine" .gitignore
$ gh repo view --json isPrivate

# Cross-references resolve
$ test -f docs/audits/2026-05-08-guardian-v55-indicator-strategy-diff.md && echo "template exists"
$ test -f docs/ltm/briefs/Q-PARITY-1-indicator-backtest-state-parity.md && echo "parent Pre-Q exists"
$ test -f docs/ltm/briefs/handoffs/2026-05-28-cc-handoff-Q-PARITY-1-phase-0.md && echo "Phase 0 handoff exists"
$ test -f strategies/guardian/LOCK.md && echo "Guardian LOCK.md exists"

# Status assertion
$ grep -E "^\*\*Status:\*\*" docs/adr/2026-05-28-audit-doc-generation-doctrine.md
# Expected: Status: Accepted
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-05-28 | Initial authoring on Q-PARITY-1 Phase 0 return + Path B selection + repo public-posture confirmation | Joshua + claude.ai |
