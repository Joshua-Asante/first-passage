# Audit Note — Meta-layer programme audit completion (diagnostics #1, #3, #4, #5, #6)

**Audit ID:** AUDIT-2026-07-01-meta-layer-completion
**Date:** 2026-07-01
**Triggered by:** owed obligation — the same-day scoped audit (`2026-07-01-methodology-belt-scoped-audit.md` §5.2/§7) covered only diagnostics #2 + #7 and declared the other five "OWED at this same cycle"; operator requested a 5-week programme audit this session.
**Authors:** Joshua (operator) + Claude Code (this session)
**Scope:** meta layer only — methodologies/governance (INQHIORI, The Algorithm, OODA, brief-authoring, programme-audit, operational rules, gates, skills). Diagnostics **#1 hard-core integrity, #3 progressive evidence, #4 degeneration evidence, #5 boundary respected, #6 theory-comparison**. Together with the sibling scoped note (#2, #7) this completes the seven-question cycle for the meta layer.
**Window:** **2026-05-27 → 2026-07-01** (operator-specified "past 5 weeks"). The sibling audit's belt-census sub-window (2026-06-04 → 07-01, owner-signed §0.5) nests inside it. Where a diagnostic's example predates 2026-05-27 (e.g. the C2-relock override, 2026-05-08) it is marked supplementary, not in-window evidence.
**Method:** multi-agent workflow `wf_1daea9d2-09f` (33 agents): 8 parallel evidence sweeps → 1 diagnostic agent per question (structured answer + key claims + grade) → 1 adversarial verifier per diagnostic (default stance: refute; every anchor re-opened) → completeness critic. Two verifier failures re-run as standalone agents. Evidence was assembled and adversarially verified **before** any verdict below was drafted (trap #1).
**Layer discipline:** no conclusion below cites portfolio P&L. Research-loop *outcomes* are object-layer (see the sibling portfolio audit); loop *discipline* (pre-reg held, falsifiers fired as designed) is meta-layer and is what this note grades.

---

## §0 — Source anchors (Phase-0 reads)

Read at on-disk-byte fidelity 2026-07-01, worktree `nervous-williams-a3c130`, HEAD `9402ee5`; commit anchors via `git log`/`git show` (all hashes cited in §3 resolved by the verification pass).

- `docs/notes/audits/programme-audit/2026-07-01-methodology-belt-scoped-audit.md` — sibling scoped audit (#2/#7); §5.2/§7 declare the five diagnostics this note completes; §0.5 owner-signed belt-census window.
- `.claude/skills/programme-audit/SKILL.md` — seven-question protocol, five verdicts, traps, layer-coupling rules (source-of-truth; no programme-audit ADR exists).
- `docs/SESSIONS.md` — window session entries (2026-05-27 → 07-01), read directly this session for the 06-29→07-01 arc.
- `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (commit `20857d3`) — read in full this session (used here only for discipline/lineage facts, not portfolio evidence).
- `docs/ltm/briefs/2026-06-11-guardian-silver-v1-admission-override.md` (`081f579`, amendment `27e2c38`) — the #5 crossing exhibit; verified at cited lines.
- `docs/adr/2026-07-01-guardian-pyport-public-tracking.md` + `docs/ltm/briefs/2026-06-06-Q-VISIBILITY-1-core-ops-privatization.md` (`b7eb3e5`) — visibility-posture exhibits; ADR :20/:56 grep-verified this session. Platform state (repo **private**) operator-verified via GitHub settings screenshot, 2026-07-01.
- Key discipline commits re-opened content-level by verifiers: `76ab018`→`4fed5ed` (GO→withdrawal), `cdbc3ce` (OOS-leak fix + RED test), `46f47d1`→`913829b` / `e03e72d`→`04bd31c` / `fe7bba5`→`8f86ebd` / `711d499`→`3935d2c` (freeze→run pairs), `887120b` (skeptic recompute), `a0094bc` (intake tightening), `33b929d` (D4 layer-split), `034cef6`/`eaff257` (DRAFT-HOLD merge).

**Failure class:** scheduled-completion diagnostic (owed cycle work), not a post-hoc failure investigation.

---

## §3 — Diagnostic evidence (assembled and verified before §4)

### #1 Hard-core integrity — GREEN (verify: 4/4 claims CONFIRMED)

Hard core (falsifiable-H before investigation; pre-reg freeze before forward data; D-S-A pre-Q gate; Rule 0; loop-of-record) **preserved**; one genuine breach, internally caught and repaired; zero quiet violations found.

- Five spot-checked freeze→run pairs are commit-ordered freeze-first with content-verified freezes (no forward data in the frozen artifacts): `46f47d1`→`913829b`, `e03e72d`→`04bd31c`, `fe7bba5`→`8f86ebd`, `711d499`→`3935d2c`, `4f467a5`→`96dd54c`.
- **The one breach (repaired):** `cdbc3ce` — the OOS harness selected IS-best on the full series (holdout saw selection), a leak the commit itself proves DSR's n_trials correction cannot see. Caught by the operator's independent adversarial probe after 4 per-task reviews + a whole-branch review missed it (the spec had blessed the defect), fixed with a RED test (`test_oos_selection_must_not_see_holdout`) **before** any verdict relied on the harness; main never carried the leak (fix is an ancestor of PR #251's merge).
- Every gate override in-window is explicit with recorded grounds; the Silver admission override names both overridden decision records and was *tightened* same-day by operator amendment (`081f579`→`27e2c38`).
- D-S-A pre-Q gate did load-bearing blocking (Q-REGIME-COND-1 Phase-0 re-scope; 06-28 "no new alpha" re-pin restraint).
- Minor unrepaired residue: no DRAFT-HOLD lift *procedure* exists (see #5); repo-side `check_brief.py` audit→generic shape mis-mapping.

### #3 Progressive evidence — GREEN (verify: claims 1–2 CONFIRMED, 3–4 WEAKENED, all deviations anti-rescue)

The meta layer produced ≥3 non-routine predicted-and-corroborated results — machinery predictions pre-dating outcomes:

1. **Pre-committed gate overturned a same-session GO.** The NAS100-ORB GO commit (`76ab018`) itself pinned "lock landing gated on native TV-CSV" with §4 tolerances; two hours later the native artifact falsified the offline harness (fills inflated meanR ~5.6×) and the ADR was withdrawn (`4fed5ed`) with **zero threshold movement** (diff-verified). The canonical-feed doctrine (2026-06-12) predates the event.
2. **OOS survivorship-leak catch** (`cdbc3ce`, above) — the audit machinery caught a defect its own statistical correction provably could not.
3. **Frozen Edit-2 source-check fired twice** in Phase B — 2/4 Lane-B "returns-independent" self-labels contradicted by their own papers; intake check subsequently tightened stricter (`a0094bc`).
4. §7 Pass-D anti-rescue: the one rescue-capable cell (residual-PCA1) deliberately surfaced and killed on every frozen gate (`7f91a0e`); standalone skeptic recompute importing no run code reproduced the result (`887120b`).

**Verified corrections (carry forward):** (a) Q-ORB-FRIDAY-1's run commit (`3935d2c`) edited verdict logic post-freeze — the frozen code would have printed AMBIGUOUS where FALSIFIED shipped. Direction anti-candidate, but "no threshold movement across all four series" is true for only 3 of 4. (b) The Edit-2 "caught → then tightened" causal order is unverifiable in-repo (the tightening may predate the catch); Phase B's §0.5 locks landed in the same commit as its closure. (c) The `cdbc3ce` finder attribution ("independent adversarial probe") lives in memory, not the repo.

### #4 Degeneration evidence — GREEN (verify: 4/4 CONFIRMED)

No post-hoc anomaly-patching without independent support found. The only favorable-direction revision (decompound severity 2.92%→1.47%) came from a pre-registered symmetry check that fixed a verified stitch-seam artifact and **left the adverse verdict intact** (both gates still breach; HOLD unchanged). `regime_robustness_gate.md` has zero in-window edits — no gate text bent for a failing candidate. The strongest disposition-before-evidence candidate (Silver override) is the honest inverse: gate FAIL recorded, override logged with acknowledged weakness, tightened same-day, terminally **not admitted**.

**Watch item:** the D4 add-back metric was redefined (layer-split, `33b929d`) in the same cycle it was first consulted, removing the sole nonzero data point from the meta numerator. This instance is clean (owner scope pre-signed §0.5 before counting; the point re-routed, not destroyed; 0/1 declared non-evidential) — but "metric redefined at first consultation" is the exact shape definitional drift takes. Monitor at ≈2026-09.

### #5 Boundary respected — YELLOW (verify: 2 CONFIRMED, 2 WEAKENED; plus one audit-time addition)

- **Genuine crossing, contained, repair incomplete on HEAD:** Guardian Silver v1.0 admission (2026-06-11) crossed the re-proposal-requires-new-mechanism bar and *said so* in its own text. Contained (same-day conditional amendment; §9 counterbalance never found; never live — `_BASE_RISK` has 4 keys). Operator CLOSED it 2026-07-01, **but on the audited HEAD the propagation is skewed**: the formal NOT-ADMITTED stamp (`73eeab6`) sits on an unmerged branch; the admission brief on HEAD still reads CONDITIONALLY APPROVED; `docs/rejected_candidates.md` carries no override/closure annotation (the annotation step was go-live-gated, now owed).
- **BTC futures reopen honored the heuristic:** prior closure pre-documented the legitimacy precondition (venue-only death, anti-SNAG unconsumed); Phase-0 gate fired against the candidate; re-proposal bar raised at re-closure.
- **DRAFT-HOLD merge (`034cef6`):** ratification better documented than first found (PR #264 carries an explicit timestamped "Approved… Un-drafted; ready to merge" comment 21s pre-merge) — but no documented hold-lift *procedure* exists.
- **Audit-time addition (operator-verified 2026-07-01): repository-visibility doc/reality skew.** Q-VISIBILITY-1 flipped the repo private on 2026-06-06 (PRIVATIZE-ALL, `b7eb3e5`). Yet `docs/adr/2026-07-01-guardian-pyport-public-tracking.md` asserts in its §0 Rule-0 anchors "Repo is public" (:20) and rejects a history purge because "the repo has been public since 2026-06-23" (:56), and CLAUDE.md §Public-clone posture still opens "This repo is public." **GitHub shows the repository private (operator screenshot, 2026-07-01).** Since `guardian_signal.py` first landed 2026-06-23 — *after* privatization — the port bytes may never have been publicly served; the ADR accepted a "history exposure" cost for an exposure that may not have occurred. Error direction is conservative (actual ≤ assumed exposure) and the untrack+hash-pin decision stands under either premise, but an ADR §0 anchor carried an unverified platform-state claim — the M-12 / verify-source failure class appearing inside a governance artifact's verification block. (This audit's own first-pass gap agent repeated the error, inferring "public" from the doc text — caught only by operator ground truth.)
- Frequency watch: three operator overrides in ~10 days (Silver 06-11, anti-SNAG 06-18, F8 06-20) — each with logged dissent and terminal outcomes against the overridden candidate, but the channel is the standing pressure point.

### #6 Theory-comparison — GREEN (verify: 3 CONFIRMED, 1 WEAKENED)

Four concrete counterfactuals; in each the chosen procedure outperformed:
- **C1 (true head-to-head):** canonical-feed doctrine vs wire-off-offline-harness — the rejected alternative is documented in the GO ADR's own alternatives table; the native gate fired same-day and withdrew the GO the alternative would have shipped into production sizing.
- **C2:** skeptic-recompute vs trust-first-run — caught the OOS leak the incumbent control provably could not; the original spec had explicitly endorsed the leaky design.
- **C3:** multi-agent adversarial verify vs solo/self-label — measurable refutation rates (3/20 census events; 2/4 harvest self-labels; 1 shipped bug). *Correction:* "every in-window deployment" overstates a 3-item enumeration against 20+ actual workflows (spot-checked extras corroborate the direction).
- **C4 (directional):** pre-reg-freeze-first — zero retractions across pre-reg'd loops; the window's one author-before-decisive-test artifact cost a same-day withdrawal.
- Adherence-only (no comparative evidence yet, not a flag): INQHIORI-vs-OODA routing; feed-retirement reopen falsifiers unfired.

---

## §4 — Proposed disposition (PROPOSED — pending owner ratification)

**Meta layer, seven-question consolidated: PROPOSED PROGRESSIVE, with four named watch items.**

Grades: #1 green · #2 STABLE/yellow (sibling, proposed) · #3 green · #4 green · #5 **yellow** · #6 green · #7 AMBIGUOUS-on-schedule (sibling, proposed).

Reasoning: the layer meets the Progressive bar on its own terms — machinery predictions made before outcomes and corroborated, including one verdict-reversing gate fire against the programme's own same-session GO, one caught-and-repaired hard-core breach, and quantified refutation rates from the verify stage. Degeneration checks are clean (no post-hoc patching; no gate-text drift; belt prunes and rejects). It is not merely Stable: the window contains new, non-routine corroborations, not just continued operation.

Watch items that keep this provisional: (W1) belt-growth magnitude (sibling #2 yellow — STABLE only if the +14 pace recedes; re-test ≈2026-09); (W2) same-commit self-attested prereg freezes, flagged independently by five verifiers across both layers — the freeze-commit-precedes-results-commit discipline exists (best practice: `46f47d1`) but is not enforced; (W3) Silver repair paperwork incomplete on HEAD + no DRAFT-HOLD lift procedure; (W4) the visibility doc/reality skew (#5 addition) — a Rule-0-class miss inside an ADR's §0.

---

## §5 — Spawned follow-ups

1. **Prereg-freeze commit-ordering rule** (fixes W2): a pre-registration artifact and its results may not land in the same commit; run commits may not edit frozen verdict logic (Q-ORB-FRIDAY-1 case). Candidate enforcement: sentinel check or `check_brief.py`. Owner: operator ratifies; CC implements. Cross-layer: also spawned by the portfolio audit.
2. **Silver closure propagation** (fixes W3a): merge or re-land the NOT-ADMITTED stamp on main; append the owed `rejected_candidates.md` override/closure annotation; sync memory. One small PR.
3. **DRAFT-HOLD lift procedure** (fixes W3b): one paragraph in `docs/operational_rules.md` naming the lift artifact (PR approval comment suffices — codify what PR #264 already did).
4. **Visibility posture reconciliation** (fixes W4): operator confirms the visibility timeline (GitHub Settings → audit log); addendum to the py-port ADR correcting the §0 premise (supersede-style, not in-place); fix CLAUDE.md §Public-clone posture; re-scope the parameter-transcription Forward question as contingent-on-re-publicization. Until then it is opsec debt with no owner date.
5. **D4 add-back metric stability check** at the ≈2026-09 audit (no redefinition without a dated incident).
6. Ratify or amend the sibling scoped audit's PROPOSED verdicts and the `33b929d` layer-split ADR (both still PROPOSED).

---

## §7 — Programme-audit signal check (this layer)

- [ ] Belt-patches without independent corroboration? **No** (sibling #2: incident-earned adds).
- [~] Belt only grows? **Yellow** — sibling #2; re-test ≈2026-09.
- [ ] Falsifier thresholds drifting? **No** — Rule-2 3/8/3 intact (sibling #7); no in-window gate-text edits found.
- [ ] Methodology invoked to rationalize? **No** — evidence assembled before verdicts here and in the exemplars audited (#4).
- [ ] SNAG pattern at the meta layer? **No** — meta-layer loops in-window are resolution-heavy.
- [~] Cross-layer contamination? **Contained** — canon §14/D4 collision already flagged (sibling §5.1); verifiers flagged one meta-citation inside an object answer (corrected in the portfolio note).
- [~] Negative heuristic crossed without repair? **One incomplete repair** (Silver paperwork, W3) + **one unverified-premise artifact** (W4). Neither silent; both have named follow-ups above.

---

## §10 — Audit hooks (runnable at next cycle, ≈2026-09)

```bash
# W2: prereg freezes must precede results (spot-check newest loops)
git log --oneline --since="2026-07-01" | grep -iE "prereg|FREEZE" # each should have a later, separate run commit
# W3: Silver closure propagated to HEAD?
grep -n "Silver" docs/rejected_candidates.md            # expect an override/closure annotation
grep -n "STATUS" docs/ltm/briefs/2026-06-11-guardian-silver-v1-admission-override.md  # expect CLOSED — NOT ADMITTED
# W4: visibility posture reconciled?
grep -n "This repo is public" CLAUDE.md                 # expect corrected posture text
grep -n "Repo is public" docs/adr/2026-07-01-guardian-pyport-public-tracking.md  # expect addendum
# W1: belt census over the next window
git log --oneline --since="2026-07-01" -- docs/methodology/ docs/adr/ .claude/skills/
# Override-frequency watch
grep -icE "override" docs/SESSIONS.md
```

---

## §11 — Closure

- **Status:** `Closed (evidence assembled and adversarially verified; PROPOSED verdict pending owner ratification; follow-ups §5 spawned)`
- **Verdict:** meta layer **PROPOSED PROGRESSIVE** with watch items W1–W4.
- Companion artifacts: sibling scoped audit (#2/#7); portfolio audit + cross-layer synthesis (same date, this directory).
