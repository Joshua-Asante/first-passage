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

Q-PARITY-1 Phase 0 (2026-05-28) returned DONE_WITH_CONCERNS: three Tier-3-only strategies (Aegis v4.3, DJ30 v4.5, NAS100 v1) had only BRIEF-ONLY grounding for their load-bearing booleans and anticipation predicates, while Guardian alone had a Tier 1 audit doc. Of the two paths considered — accept BRIEF-ONLY grounding, or land Tier 1 audit docs for the other three (closing the repo gap) — Joshua chose the latter. Same-day, repo stays public / Pine stays gitignored was reaffirmed, framing the audit-doc path as the fix that respects that posture. (Full Phase 0 detail: Q-PARITY-1 brief cited in §0 — pruned from this public tree per the Great Prune, retrievable per [`docs/adr/2026-08-08-great-prune.md`](2026-08-08-great-prune.md).)

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
| **Path A — accept BRIEF-ONLY grounding** | Compounding audit-trail asymmetry; every future brief on these strategies re-hits Phase 0 Concern §C1. Joshua leaned Path B explicitly. |
| **Chat-paste-during-handoff per session** | Same per-session effort, no compounding — every future CC handoff needs a fresh Pine paste. Audit-doc workstream front-loads the cost once instead. |
| **`.local/` gitignored Pine cache + SHA manifest** | Reproducibility gap (session-time Pine isn't tracked); adds infrastructure without compounding benefit. |
| **Make repo private + remove Pine from gitignore** | Explicitly rejected 2026-05-28 (`gh repo view`: `isPrivate: false`) — stay public, find a different efficiency unlock. |
| **Bundle three audit docs into one CC handoff** | CC cannot read Pine (gitignored); authoring must be Joshua-led per strategy. Bundling defeats per-strategy quality. |
| **Status quo — do nothing** | Q-PARITY-1 Phase 1 stays blocked indefinitely; the asymmetry becomes a permanent repo gap. |

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

**Positive:** Unblocks Q-PARITY-1 Phase 1 once the three audit docs land; future briefs touching Aegis/DJ30/NAS100 inherit Tier 1 grounding (compounding across Q-PARITY-N and any non-parity brief); closes the per-strategy audit-doc asymmetry; pattern reuses at a fifth strategy's lock-completion.

**Negative:** ~3 hours front-loaded authoring across 3 sessions (~45–60 min/strategy); ~150–250 lines added per doc; needs manual sync when Pine changes (no automated drift detector — mitigation: a lock-checklist "audit doc updated" item); widens the bounded Pine-leak surface in doc excerpts (accepted trade-off; §5 bounds the scope).

**Risks:** audit-doc drift if a Pine patch lands without an update (mitigated by each doc's version-pin header, cross-checked against CLAUDE.md's Strategy Reference table); doctrine over-scoped if ≥2 of 3 strategies fall back to the §4 annex pattern (re-evaluate the ADR if so).

**Downstream artifacts:** Q-PARITY-1 brief §0 Layer 2 re-grounds per strategy as each doc lands; optional `CLAUDE.md` methodology pointer; a lock-decision brief template checklist item. (Q-PARITY-1 brief itself pruned from this public tree — see §0 anchor and [`docs/adr/2026-08-08-great-prune.md`](2026-08-08-great-prune.md).)

---

## §7 — Implementation plan

Per strategy: Joshua opens a fresh claude.ai session, pastes the indicator + strategy Pine, and confirms the locked version against ADR 2026-05-23-allocation-refresh-2. Claude.ai authors the audit doc to the Guardian template (§0 reads, indicator-vs-strategy diff, state-var enumeration, numeric constants, anticipation predicates, hypothesis verdicts where applicable). Joshua reviews against source, applies the §4 falsifier check (substantive-diff ≥50 lines, else switch to the annex pattern), and commits the doc to `docs/audits/`; the Q-PARITY-1 §0 Layer 2 row for that strategy updates from Tier 3-only to full Tier 1/2/3. After all three land, Q-PARITY-1's Verification block advances to "Path B execution complete."

**Authoring order:** Aegis first (smallest expected diff), DJ30 second, NAS100 third (largest expected complexity — pyramid-anticipation predicates).

---

## §10 — Audit hooks (runnable)

HOOK WIDENED 2026-08-31: the six hooks below queried `docs/audits/*.md` and the
Q-PARITY-1 brief, both removed by the 2026-08-08 Great Prune before any of this ADR's
three audit docs landed — pruned deliverables, not a passing state to re-check. Replaced
per the sanctioned repoint pattern (see `2026-08-04-tradeify-venue-descope-eval-included.md`
§10 "HOOK WIDENED") with checks against what's actually live today.

```bash
# Deliverables pruned 2026-08-08 (Great Prune) — docs/audits/ no longer exists in this
# public clone. Pattern still governs future locks (§2 Scope); this is expected, not a defect.
$ test -d docs/audits && echo "docs/audits present" || echo "docs/audits absent (expected post-prune)"

# Confirm this ADR is still on disk — pattern survives even though deliverables didn't
$ test -f docs/adr/2026-05-28-audit-doc-generation-doctrine.md && echo "ADR present"

# Confirm Pine still gitignored (repo-posture decision this ADR operates under)
$ grep -nE "\*\.pine" .gitignore
```

---

## Verification

```bash
# Discipline check on this ADR
$ PYTHONIOENCODING=utf-8 python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-05-28-audit-doc-generation-doctrine.md --type adr

# Status assertion
$ grep -E "^\*\*Status:\*\*" docs/adr/2026-05-28-audit-doc-generation-doctrine.md
# Expected: Status: Accepted
```

§0's anchors predate the 2026-08-14 public-repo reset (this file's own git history starts
at "Initial public release"); the commit hashes and the `docs/audits/` /
`docs/ltm/briefs/Q-PARITY-1-*` paths they cite are pre-transition and unreachable in this
clone's history. See `docs/adr/2026-08-08-great-prune.md` for the retrieval path — not
re-verified here.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-05-28 | Initial authoring on Q-PARITY-1 Phase 0 return + Path B selection + repo public-posture confirmation | Joshua + claude.ai |
