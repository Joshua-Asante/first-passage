# Audit Note — Methodology-belt scoped programme audit (diagnostics #2 + #7)

**Audit ID:** AUDIT-2026-07-01-methodology-belt-scoped
**Date:** 2026-07-01
**Triggered by:** degeneration signal #2 (belt-that-only-grows), operator-flagged 2026-07-01 discussion; scoped to two of the seven programme-audit diagnostics
**Authors:** Joshua + Claude Code (this session)
**Scope:** framework layer — **meta layer only** (the governance/methodology belt). This is a **scoped** audit: diagnostics **#2** (belt-churn balance + add-back) and **#7** (falsifier check on Rule 2). The other five diagnostics are **owed at this same cycle** (see §7).
**Lives in:** `docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md`
**Loop-of-Record:** STRATEGIC for the *disposition verdict* (a Degenerating verdict would trigger a belt-prune = Strategic Delete, owner-ratified, no-borrowing per `docs/adr/2026-06-12-three-loop-methodology-binding.md`). CC's execution was a bounded OUTER measurement task (deterministic census).
**Rule-2 budget:** OUTER (8 iterations). Landed under budget; no trip (recorded conceptually — census was deterministic).

---

## §0 — Source anchors (Phase-0 reads)

Read at on-disk-byte fidelity, 2026-07-01, worktree `competent-poincare-0b32d9`. Git anchors are `git log -1 --format='%h %ci'`.

- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` — `06e416d` 2026-06-16. Status **PROPOSED**. §4 falsifier (empty-log ≥2-cycle; hindsight-productive clustering; circular-re-derivation ban). §1:33 anchors 3/8/3.
- `docs/notes/audits/rule-2-trip-log.md` — `06e416d` 2026-06-16. One table; **1 row** (2026-06-16 OUTER, non-trip baseline).
- `docs/methodology/inqhiori-canon.md` — `06e416d` 2026-06-16. §14 add-back definition (`:295`, Guardian-Silver anchor) + §15 Rule 2 (`:301`–`:324`, 3/8/3).
- `docs/methodology/rejected_signals.md` — `7c864aa` 2026-06-04. **1 entry** (Starvation, REJECTED 2026-06-04).
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` — `e122582` 2026-06-13. D2 STRATEGIC-LoR Delete condition; D3 no-borrowing; D4 add-back-rate metric.
- Programme-audit protocol source — **no `*programme-audit*` ADR exists in `docs/adr/`**; source-of-truth is the `programme-audit` SKILL body (`.claude/skills/programme-audit/SKILL.md`). Diagnostics #2/#7, five verdicts, traps #1/#2 confirmed there.
- `ls docs/notes/audits/programme-audit/` → **ABSENT at audit start**. **No prior meta-layer audit note; this is the first.** Window start therefore proposed and owner-signed-off (§1).

**Failure class:** Investigation degeneration check (SNAG / belt-only-grows / falsifier creep) — proactive diagnostic, not a post-hoc failure.

---

## §1 — Trigger, window, and owner sign-off

**Trigger.** The 2026-07-01 discussion flagged an asymmetry: the object/strategy layer has earned "best part is no part" (4-strategy lock, D-S-A pruning, `docs/rejected_candidates.md`), but the methodology/governance layer has been accreting for ~a quarter (three-loop binding 06-12, Rule 2 06-16, coordination-signal #8/C1 06-04, the fourth D-S-A dimension) while `rejected_signals.md` holds exactly one rejection. Prima-facie degeneration signal #2, pointed at the methodology itself.

**Parent question (symptom-only):** *Is the governance/methodology belt still load-bearing, or has it begun to degenerate?* This note assembles the gating evidence; it does **not** prescribe a prune.

**§0.5 owner sign-off (obtained before any counting, to avoid meta-layer p-hacking):**
- **Taxonomy** = *full structural taxonomy* — 8 device classes: (a) numbered governance rules, (b) loop bindings + LoR discipline, (c) D-S-A structure, (d) programme-audit devices, (e) observation-routing buckets, (f) mandatory brief-header/gate types (incl. validation/enforcement gates), (g) methodology-layer registries-as-containers, (h) methodology skills + hooks. M-# lessons **excluded**. Installed-item removals and proposed-item rejections reported as **separate** balances.
- **Window** = **[2026-06-04 → 2026-07-01]** (lean-portfolio meta-layer ADR / three-loop framework origin — captures all named accretion with a clean baseline; the first meta-layer audit, so no prior-audit boundary exists).
- **Add-back scope** = **meta-layer only** (numerator = rejected *methodology signals* re-accepted on a dated incident; Guardian Silver excluded — definition-anchor only). The canon §14/D4 cross-layer collision is spawned as a follow-up (§5.1).

---

## §2 — Method (reproducible)

Deterministic git enumeration (61 commits touching `docs/methodology/` + `docs/adr/` + `.claude/skills/` in-window) → parallel classification of **all 61** commits against the fixed taxonomy → **adversarial verification** of each candidate belt event (skeptic default = refute; checks: add-vs-mirror/back-fill, prune-vs-rename/move, meta-vs-object). Census workflow `wf_f0b0f88a-bcc` (26 agents). Cross-layer exclusion enforced (object-layer feed/venue/strategy/MC/refactor content classified NEITHER unless it introduced a governance device).

---

## §3 — Diagnostic evidence (assembled BEFORE any verdict — trap #1)

### Q-A ≡ Diagnostic #2 — belt-churn balance + meta-layer add-back

**Confirmed belt events (17), each git-anchored:**

| # | Type | Class | Device | Commit |
|---|---|---|---|---|
| 1 | ADD | h | verify-source discipline skill | `f3a3587` |
| 2 | ADD | h | sync_skills_hook.py PostToolUse skill-sync hook | `f3a3587` |
| 3 | ADD | a/f | Phase-0 cost-geometry pre-gate (Rule 10 sub-step) | `6d48ba4` |
| 4 | ADD | a | **Rule 2** — budget before acting (canon namespace) | `06e416d` |
| 5 | ADD | g | Rule-2 forward trip-log (container) | `06e416d` |
| 6 | ADD | g/f | Rejected-candidate 4-class pattern taxonomy + add-back gate | `88e11dc` |
| 7 | ADD | b | **Three-loop binding** + no-borrowing + add-back-rate metric | `e122582` |
| 8 | ADD | a | operational Rule 10 — instrument-ledger read/append | `5baf01f` |
| 9 | ADD | f | cfg-fingerprint convention + Step-0 verification gate | `5baf01f` |
| 10 | **PRUNE** | f | brief-evidence-coverage **Hook 1 retired** | `5df088e` |
| 11 | ADD | f | check_boundaries.py AST import-contract gate | `e8ce8fb` |
| 12 | ADD | a | operational Rule 9 — Pine-sync pre-flight | `0f5a05d` |
| 13 | ADD | f | check_skill_refs.py path-reference linter gate | `a58b162` |
| 14 | ADD | f | validate_params no-operational-constants guard | `a58b162` |
| 15 | ADD | f | check_brief.py brief well-formedness validator | `a58b162` |
| 16 | ADD | g | rejected_signals.md registry (container) | `7c864aa` |
| 17 | **REJECTION** | g/d | within-stream Starvation signal (rejected pre-install) | `7c864aa` |

**Refuted candidates (3 of 20 — the verify stage doing real work):**
- `c6af48f` trade-capture mirror gates — claimed PRUNE → **NEITHER** (object-layer cascade of the Notion-ingest retirement; trap #2).
- `a58b162` inqhiori-algorithm skill — claimed PRUNE → **NEITHER** (never installed in-repo; dedup of a dead ~95% duplicate; traps #2/#5).
- `a58b162` sync_skills.py — claimed ADD → **NEITHER** (one-way deploy plumbing, not a wired gate; trap #5).

**Tallies:**
- **Installed-item balance = 15 ADD − 1 PRUNE = +14** (net-positive, one window).
- **Sensitivity:** ~7 of 15 adds are class-(f) **enforcement/CI gates** (`check_boundaries`, `check_skill_refs`, `check_brief`, cost-geometry, cfg-fingerprint, no-constants guard, sync-hook). Excluding those as engineering infra → **≈ +7**. **Verdict is invariant to the boundary** (net-positive-with-one-prune either way).
- **Proposed-item rejection count = 1** (Starvation).
- **Meta-layer add-back rate = 0 / 1** — zero rejected methodology signals re-accepted, one issued. **Under-sampled (N=1); not evidence in either direction.**

**#2 threshold application:** protocol thresholds — net-positive one window = **yellow**; net-positive across **≥3 consecutive** audits = **red**. This is audit **#1**, so the red condition is **structurally inapplicable**. The brief's Degenerating trigger ("adds outpace prunes with **zero** prunes this window") is **not met** — one genuine prune occurred (`5df088e`). The adds are overwhelmingly **incident-earned** (Rule 10 ← 2026-06-11 USDCAD collision; Rule 9 ← worktree-Pine near-miss; cfg-fingerprint ← relay-defect class; cost-geometry ← measured need) — corroborated belt-patches *with* independent support, the opposite of degeneration signals #1/#4.

### Q-B ≡ Diagnostic #7 — Rule 2 falsifier liveness

- **Genuine post-2026-06-16 trip events = 0.** The trip-log's one row is an explicit **non-trip baseline** (2026-06-16 OUTER, "wire did not fire … a calibration baseline, not a trip") — correctly labeled, not fabricated (respects ADR §4). No cfg00–12 re-derivation present (circular-count barred).
- **Threshold drift = none.** 3/8/3 reads **identically** across ADR §2 (`:47`–`:49`), canon §14 (`:297`) + §15 (`:309`–`:311`), and the trip-log seed (`:11`–`:13`). No softening toward "we'd never hit this."
- **Elapsed cycles since codification = 0.16 quarterly cycles** (15 days, 2026-06-16 → 2026-07-01) — far below the **≥2** the ADR §4 empty-log falsifier requires.
- Hindsight-productive clustering: N/A (no trips to cluster).

---

## §4 — Proposed disposition verdicts (PROPOSED — pending owner ratification)

> Per forbidden move #2 / trap #7, the disposition is **owner-assigned**. These are proposals with reasoning, not decisions. A Degenerating verdict would trigger a belt-prune = Strategic Delete and cannot execute on CC momentum.

**Q-A (#2) → PROPOSED: STABLE (yellow-flag) — NOT Degenerating.**
Reasoning: balance is net-positive (+14, or ≈+7 excluding enforcement-gate infra), which is a yellow flag on magnitude — but (a) this is the first window, so the ≥3-consecutive red condition is inapplicable; (b) ≥1 genuine prune occurred, so the "zero-prunes" Degenerating trigger is not met; (c) the adds are incident-earned corroborated gates, not ceremony; (d) the window is the framework's **construction phase** (three-loop hierarchy, Rule 2, R&D-pipeline gates, skills-under-VC), where mostly-adds is expected. The seeding premise "belt only grows, never prunes" is **partly refuted** (Hook-1 prune + Starvation rejection both exist; the "N=1 rejection" look is registry youth, not degeneration). **Load-bearing caveat:** STABLE holds *only if the magnitude does not persist* — see §10 re-test.

**Q-B (#7) → PROPOSED: AMBIGUOUS (on-schedule).**
Reasoning: empty of genuine trips **and** <2 cycles elapsed — the exact case ADR §4 defines as not-yet-falsifiable. FALSIFIED is **barred** (the ≥2-cycle condition is part of the falsifier; forbidden move #4). Rule-2-live is not yet establishable (needs ≥1 genuine trip). Thresholds intact (no #7 drift). AMBIGUOUS here is a dated verdict with a named re-test, not "we'll wait."

**Consolidated read (both steps together).** No contradiction. Q-A: belt growing fast but pruning and rejecting. Q-B: the *newest* belt device (Rule 2) has not yet been exercised (empty trip-log). Together they describe a **young, actively-constructed belt that is adding faster than it is exercising or pruning its newest instruments** — expected for a build phase, and precisely the pattern to re-measure. The methodology is **provisionally load-bearing**; neither diagnostic supports a prune now.

---

## §5 — Spawned follow-ups

1. **Add-back cross-layer collision (canon §14/D4).** Canon defines add-back over object-layer "Strategic Deletes" with an object-layer anchor (Guardian Silver) but tracks it "at programme audits" (meta-layer events). For a *methodology* audit this is latent cross-layer contamination (trap #2 baked into the canon). Owner chose meta-layer-only for this audit; a canon amendment (split meta-layer signal add-back from object-layer strategy add-back) is queued for owner adjudication. Spawned as a task chip.
2. **The other five diagnostics are owed this cycle** (#1 hard-core integrity, #3 progressive evidence, #4 degeneration evidence, #5 boundary respected, #6 theory-comparison). A scoped audit shipped as complete would itself be ceremony (§7).
3. **Belt/infra boundary confirmation.** Before the forward re-test uses this window as baseline, the owner should confirm whether class-(f) enforcement/CI gates count as methodology belt (+14) or engineering infra (≈+7). Verdict is invariant, but the baseline count is not.

---

## §7 — Programme-audit signal check (cross-skill) + scoped-audit flag

- [x] Belt-patches without independent corroboration? **No** — adds are incident-earned.
- [~] Belt that only grows, never prunes? **Partly** — net +14 (yellow), but ≥1 real prune + 1 real rejection refute the strong form. Re-test forward.
- [ ] Falsifier thresholds drifting? **No** — 3/8/3 intact.
- [ ] Methodology invoked to rationalize a decision already made? **No** — evidence assembled before verdict (§3 before §4).
- [ ] SNAG pattern? Out of scope (#2/#7 only).
- [ ] Cross-layer contamination? **One latent instance in the canon** (§5.1) — flagged, not executed-on.
- [ ] Negative heuristic crossed without repair? **No** — the three refuted candidates show the boundary held.

**Scoped-audit flag (trap #6).** This covers diagnostics **#2 and #7 only**. Diagnostics **#1, #3, #4, #5, #6 remain OWED at this same quarterly cycle.** Do not treat this note as a complete meta-layer audit.

---

## §10 — Audit hooks (runnable at next cycle)

```bash
# Q-B liveness: trip-log entry count + dates (empty of genuine trips = 0 firings)
grep -nE '^\| 20[0-9]{2}-' docs/notes/audits/rule-2-trip-log.md
# Rule 2 threshold drift: confirm 3 / 8 / 3 unchanged across ADR + canon + trip-log
grep -nE 'INNER.*3 iteration|OUTER.*8 iteration|STRATEGIC.*3 constituent' \
  docs/adr/2026-06-16-rule-2-budget-before-acting.md docs/methodology/inqhiori-canon.md docs/notes/audits/rule-2-trip-log.md
# Q-A meta-layer prune registry size (rejected signals)
grep -c '^### REJECTED' docs/methodology/rejected_signals.md
# Q-A belt census over the NEXT window (set WINDOW_START = this audit date)
git log --oneline --since="2026-07-01" -- docs/methodology/ docs/adr/ .claude/skills/
# Scoped-audit completeness: was the FULL seven-question audit run this cycle, or only #2/#7?
ls docs/notes/audits/programme-audit/ | tail -3
```

**Forward re-tests (scheduled obligations):**
- **Q-B (Rule-2 empty-log falsifier):** cannot fire until **≥2 quarterly cycles** past 2026-06-16 (≈ **2026-12** meta-layer audit). Empty log at the 1st post-06-16 audit (≈2026-09) = still AMBIGUOUS; empty at the 2nd (≈2026-12) = **FALSIFIED-as-load-bearing**.
- **Q-A (belt-churn trend):** this is audit **#1**. If audits **#2 (≈2026-09)** and **#3 (≈2026-12)** are also net-positive with prunes not catching up → **≥3-consecutive net-positive = red = Degenerating-candidate**. STABLE is provisional on the magnitude receding.

---

## §11 — Closure

- **Status:** `Closed (immediate — evidence assembled, proposed verdicts pending owner ratification; structural follow-ups §5 deferred)`
- **Q-A (#2):** PROPOSED STABLE (yellow-flag), not Degenerating. Owner ratification required.
- **Q-B (#7):** PROPOSED AMBIGUOUS (on-schedule). Re-test ≈2026-12.
- **Follow-up audits triggered:** the five remaining diagnostics (#1,#3,#4,#5,#6) at this cycle; canon add-back amendment (§5.1).
- **CC status return:** `DONE_WITH_CONCERNS` — the belt/infra boundary for class-(f) enforcement gates is genuinely ambiguous even after §0.5 sign-off (it moves the balance +14↔+7 without changing the verdict).

---

## Verification

```bash
# Authoritative gate for the 'audit' type is the SKILL-SIDE checker (repo-side check_brief.py
# maps audit->generic and mis-applies the brief-family shape; it redirects here itself).
# On Windows force UTF-8 so the ✓ glyphs don't crash cp1252:
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python "$HOME/.claude/skills/brief-authoring/scripts/check_brief.py" \
  docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md --type audit
# Expected: RESULT: PASS (6/6 checks)   [confirmed 2026-07-01]

# §0 anchors resolve
git log -1 --format='%h %ci' -- docs/adr/2026-06-16-rule-2-budget-before-acting.md   # 06e416d
git log -1 --format='%h %ci' -- docs/methodology/rejected_signals.md                  # 7c864aa
# Confirm the confirmed-event commits exist
for h in f3a3587 6d48ba4 06e416d 88e11dc e122582 5baf01f 5df088e e8ce8fb 0f5a05d a58b162 7c864aa; do git cat-file -t $h; done
```
