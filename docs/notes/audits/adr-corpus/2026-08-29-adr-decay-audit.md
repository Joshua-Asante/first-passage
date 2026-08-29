# ADR corpus decay audit — full-corpus Phase 1/2 run

**Audit ID:** AUDIT-2026-08-29-ADR-DECAY · **Date:** 2026-08-29 · **Trigger:** operator direction, during
a broader documentation-simplification pass, to run `adr-decay-audit` as a real repeatable process for
the first time against the full Accepted-ADR corpus (the skill itself had never been executed as a
full pass before this run — see `docs/adr/2026-08-23-adr-decay-audit-skill-ratification.md`).
**Authors:** Joshua (direction) + Claude Code. **Method:** the skill's own two-phase scan→verify fan-out
— 161 Accepted ADRs (of 168 files under `docs/adr/`, minus `INDEX.md`/`README.md`/`TOMBSTONES.md`; 4
already-terminal Superseded/Withdrawn files correctly excluded), batched by cumulative word count into
27 Phase-1 scan batches, followed by 14 Phase-2 verify batches (8 rigorous small-batch refutation passes
over every `DECAYED_UNDOCUMENTED`/`UNCERTAIN`/safety-relevant flag, 6 lighter-weight passes over every
`DECAYED_DOCUMENTED` flag) — 41 batch agents total, each independently deriving evidence from primary
source (production code, other ADRs, briefs, `STATE.md`/`SESSIONS.md`), not trusting the prior pass's
evidence string at face value.

---

## §1 — Result

| Verdict (Phase 1 raw) | Count |
|---|---:|
| STILL_APPLICABLE | 99 |
| DECAYED_DOCUMENTED | 39 |
| DECAYED_UNDOCUMENTED | 19 |
| UNCERTAIN | 4 |
| **Total** | **161** |

| Verdict (Phase 2 final, after reclassification) | Count |
|---|---:|
| STILL_APPLICABLE | 100 (+1) |
| DECAYED_DOCUMENTED | 38 (−1) |
| DECAYED_UNDOCUMENTED | 20 (+1) |
| UNCERTAIN | 1 (−3) |
| **Total** | **161** |

No Phase-1 batch returned schema-valid-but-content-empty output (Known Trap #1); no Phase-2 call
degenerated or failed to return real reasoning. Every non-`STILL_APPLICABLE` flag got an independent
refute-first second pass; none were rubber-stamped.

---

## §2 — Phase 1 → Phase 2 reclassifications (6 total)

| ADR | Phase 1 | Phase 2 | Why |
|---|---|---|---|
| `2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` | DECAYED_UNDOCUMENTED | **DECAYED_DOCUMENTED** | `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` §6 explicitly records the standing-research-interest suspension in prose ("it is its suspension, and it should be recorded as such") — no header link exists, but the fact is genuinely recorded elsewhere in the graph (Known Trap #2 shape). |
| `2026-06-30-state-md-role-reduction.md` | DECAYED_DOCUMENTED | **DECAYED_UNDOCUMENTED** | The cited corroboration (`docs/operational_rules.md` Rule 7's dated changelog) only explains one of `STATE.md`'s two undocumented extra headers (the decision-index). The other — `## OPERATOR QUEUE`, added by `2026-08-09-survive-bound-is-the-queue-cap.md`, cited across 31 files — has no cross-reference anywhere back to this ADR or into Rule 7's text. |
| `2026-07-26-regime-candidate-flag-lane.md` | UNCERTAIN | **DECAYED_UNDOCUMENTED** | Both of Addendum 2026-08-21's self-certifying claims independently reproduce as false: no `STATE.md` forward-board line exists under any wording (exhaustive grep + full manual read of the 2026-11-08 section), and the "Phase 2 hook 3 — 0 hits" claim returns 3 hits on an identical re-run today. |
| `2026-08-05-strategy-venue-binding-axis.md` | UNCERTAIN | **STILL_APPLICABLE** | The ADR's own §4 text explicitly states T2/T3/T4 are "unreachable before 2026-11-08 by construction" and names the quarterly-audit check date directly — today's live `ops/venue_editions/` vs. `LEG_MAP` disagreement is the anticipated pre-audit state the ADR itself designed for, not a silent firing. Flagged operationally: if unreconciled by 2026-11-08, T2 fires for real. |
| `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md` (LTM-retrieval clause) | UNCERTAIN | **resolved, no decay** | Phase-1's shallow clone made `git log --follow` unreliable. A full unshallow fetch (true root `027a729`, 862 commits) confirms the withdrawn predecessor ADR was pruned by the Great Prune (`docs/adr/TOMBSTONES.md` line 20) 6 days *before* the public repo was even seeded — its total absence from public history, and from `docs/ltm/adr/`'s post-transition cold-stub convention, is expected, not a gap. |
| `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` (unruled seam) | UNCERTAIN | **UNCERTAIN, confirmed genuine** | Re-verified: no ADR dated 2026-08-24 through 2026-08-29 touches either self-flagged open question (S1/S2); `docs/SESSIONS.md`'s most recent relevant entry (2026-08-23) still reads "S1/S2 still unruled." This is the skill's by-design case — an honest, still-open question, not silent decay. Stays open. |

---

## §3 — DECAYED_UNDOCUMENTED findings (20) — full entries

Each entry below carries: the stale claim, current reality, why the drift didn't reach the ADR, and the
remediation applied (or the forward obligation, if not applied this session — see §7 for disposition).

1. **`2026-08-15-regime-gate-scope-ratification.md`** — Both this ADR and the later
   `2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md` independently claim to discharge
   the same gate-stack-audit F1 obligation, unaware of each other. Root cause: `check_advisor_dedup.py`
   structurally never indexes `docs/adr/`, so the dedup tool guaranteed a false negative. Both rulings
   are substantively compatible (same grounds, no revert needed) — bookkeeping duplication, not a
   conflicting decision. **Remediated** — addendum added, `Superseded-in-part-by` cross-link added both
   directions.

2. **`2026-05-10-mc-c2-anchor-ratification.md`** — Audit hooks fail outright (`tests/test_mc_anchors.py`
   deleted; `core/portfolio_mc.py` is now a 50-line facade with none of the 5 cited hook targets).
   Root cause: `2026-07-22-challenge-era-substrate-retirement.md` Phase 3 deleted the Pepperstone anchor
   this ADR ratified, without adding itself to that retirement ADR's 7-item `Supersedes` list.
   **Remediated** — addendum + reciprocal header field.

3. **`2026-06-04-methodology-skills-under-vc.md`** — Ratified migrating 3 named skills
   (`fxify-challenge`, `live-execution-journal`, `notion-mcp-api-patterns`) verbatim into
   `.claude/skills/`; none exist there. GSUB-1 (2026-08-09) found the first two are platform-bundled
   plugins with no file-level existence to migrate, and the third was archived, not migrated — the
   opposite of this ADR's premise, never linked back. The ADR's canonical-home/gating-machinery
   decisions (§2.1/§2.4/§2.5) remain very much alive. **Remediated** — addendum narrowly scoped to the
   falsified 3-skill migration plan only.

4. **`2026-07-16-root-doc-charter-dedup.md`** — Own §10 hook expects `CLAUDE.md`'s Live-execution
   posture section at ≤25 lines; it's 54 today (Safety invariants block, Account-state paragraph, Eval
   bust-figures warning all accreted post-2026-08-03, each individually irreducible to a pointer line).
   No addendum records the exception. **Logged as forward obligation** (see §7) — this is a judgment
   call (accept the safety-content exception vs. trim back to pointer form) that belongs to the
   operator, not a mechanical discharge.

5. **`2026-07-06-bust-day-maxdd-inclusion.md`** — §10 hook cites `core/portfolio_mc.py`; the fix
   genuinely still holds, relocated to `core/mc/simulation.py` (verified live: the underwater-DD update
   precedes every bust-path return; `tests/core/test_mc_bustday_maxdd.py` re-run live, 4 passed). No ADR
   documents the `portfolio_mc.py → core/mc/*` split for this citation. **Remediated** — addendum
   repoints the hook.

6. **`2026-05-18-pine-input-float-defaults-realignment.md`** — Top blockquote asserts
   `scripts/validate_params.py` "remains in effect"; deleted by `2026-08-03-params-toml-gate-retirement.md`.
   Compounding: `docs/adr/INDEX.md`'s summary mirrors the identical stale claim (Known Trap #2).
   **Remediated** — addendum + header field + `INDEX.md` regenerated (see §7).

7. **`2026-07-13-harv-discovery-lane-ratification.md`** — Own §4 falsifier fired (independently
   confirmed against `lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md`, matching the
   successor's Trigger line on both conjuncts), but header never updated. **Remediated** — reciprocal
   `Superseded-in-part-by` field added.

8. **`2026-05-18-relock-to-test-values.md`** — Same `validate_params.py` staleness as #6, sibling file.
   **Remediated** — addendum + header field.

9. **`2026-07-14-prop-portfolio-existing-strategy-candidates.md`** — §2 asserts `ACTIVE_FIRM stays
   FXIFY` (deleted outright in substrate Phase 4, not repointed) and an untouched survivor-scoring
   ceiling (moved 3.0%→5.0% by a 2026-08-26 prereg). Neither successor cross-links back.
   **Remediated** — two `Superseded-in-part-by` fields added, mirroring the parent ADR's own pattern.

10. **`2026-06-06-firm-constants-single-source.md`** — Instituted the `ACTIVE_FIRM` selector this ADR's
    own successor deleted outright; absent from that retirement ADR's 7-item `Supersedes` list despite
    being the most directly gutted decision of the seven. **Remediated** — addendum + reciprocal field
    added on both sides.

11. **`2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`** — §4 revert-trigger limb 2 relies
    on the decompound quarterly-check machinery, confirmed permanently `NOT_EXECUTABLE` (Pepperstone
    retirement deleted its gitignored inputs) with an already-missed 2026-08-08 check date. **Remediated**
    — addendum striking limb 2, limbs 1/3 unaffected.

12. **`2026-06-14-rejected-candidate-patterns.md`** — §7/§D/§10 assert `dedup.py`/`feedback.py` as live
    machinery; deleted 2026-07-11. The death is documented in `docs/rejected_candidates.md`'s DEAD
    SECTION note but never cross-referenced back to this ADR. **Remediated** — addendum + reciprocal
    field.

13. **`2026-08-08-great-prune.md`** — Asserts unqualified byte-retrievability via
    `git show pre-prune-2026-08-08:<path>`; the tag doesn't exist on this public clone (`git tag -l`
    empty, independently re-verified). Two later addenda on the same file never touch this specific
    point. **Remediated** — addendum recording the retrievability guarantee's public-clone scope.

14. **`2026-07-11-fxify-ops-surface-retirement.md`** — §2 KEEP/PARK table names files all now deleted by
    two *different* later ADRs, neither cross-linked back (though `REPO_MAP.md` — a different file —
    does document both). **Remediated** — addendum + two reciprocal fields.

15. **`2026-07-01-guardian-pyport-public-tracking.md`** — §2.3/§3/§6 retrievability claim
    (`git show dc07898:...`) no longer resolves post the 2026-08-14 fresh-repo transplant; the ADR's own
    2026-08-14 addendum addresses visibility/redaction but never revisits this specific retrieval-hook
    claim. **Remediated** — addendum narrowly targeting the retrieval-mechanism claim only.

16. **`2026-07-10-databento-research-stack.md`** — §2 "Live-rail verdict" (TradingView→CrossTrade→
    NinjaTrader8→Bulenox via Rithmic) is fully superseded-in-fact by the S1/S2 loop ADRs (current rail:
    CrossTrade→Tradovate, Python-daemon origin, Tradeify_Select_100K venue); neither S1 nor S2 lists this
    ADR under `Supersedes`. The named §4 falsifier never fired — the venue changed by a different
    mechanism entirely. **Remediated** — addendum; the stack/tooling decision itself (databento,
    validation-suite adoption, Nautilus research-only) is unaffected.

17. **`2026-08-08-edge-cohort-correction-and-necessity-retarget.md`** — §2-B/§5/§10 assert
    `Q-MNQDTL-CON-1` stays OPEN; closed FALSIFIED one day after ratification, never recorded on the ADR.
    Judged a dead letter operationally — §5's forbidden move can no longer be violated since there's
    nothing left to over-read. **Remediated** — light addendum.

18. **`2026-07-31-orb-mnq-unpark-payability-target.md`** — Addenda declared "standing record" still
    assert the pre-family-K-disclosure gate math (K_eff sums bank, floor 0.98); superseded 2026-08-04
    (K_eff = K_intrinsic only). The 2026-08-04 ADR's own repair-sweep regex is a literal-string match
    that demonstrably misses this file's paraphrased prose. **Remediated** — reader-intercept banner
    added near the stale ruling text (frozen prose itself untouched, per Rule 14); repair-sweep regex
    gap flagged separately (§7).

19. **`2026-07-26-regime-candidate-flag-lane.md`** (reclassified from UNCERTAIN, §2) — Addendum
    2026-08-21's two self-certifying claims both independently reproduce as false. **Remediated** —
    follow-up addendum correcting both claims; `STATE.md` forward-board line added (§7, LIVING-doc fix).

20. **`2026-06-30-state-md-role-reduction.md`** (reclassified from DECAYED_DOCUMENTED, §2) — The
    `## OPERATOR QUEUE` header (2026-08-09, load-bearing, cited across 31 files) has no cross-reference
    anywhere. **Remediated** — reciprocal `Superseded-in-part-by` field added.

---

## §4 — DECAYED_DOCUMENTED findings (38) — compact list

All confirmed on independent Phase-2 re-derivation; "no action" means the addendum/banner/reciprocal
header field genuinely exists and genuinely covers the stale claim. Three carry a light opportunistic
follow-up noted inline (none blocking, none re-scored).

| ADR | Issue | Action |
|---|---|---|
| `2026-04-17-dd-trigger-calibration.md` | DD_TRIGGER re-locked by C2-relock | no action, reciprocal header exists |
| `2026-08-07-w6-rail-infra-closures.md` | `requirements-research.lock` owed → landed | no action, `REPO_MAP.md` records discharge |
| `2026-04-25-mvd-retrofit.md` | `docs/methodology/mvd.md` deleted | no action, own References line records it |
| `2026-05-23-relocate-ecr-to-live-journal.md` | ADR self-flagged SPENT | no action, inline note present |
| `2026-05-08-dd-trigger-c2-relock.md` | Quarterly revert-check unreachable | no action, reader-intercept banner present |
| `2026-04-24-mvd-discipline.md` | Doc-audit-table dropped, code self-checks live | no action, Status + addendum present |
| `2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` | Hook-3 claim stale | no action; addendum's tier count now off-by-one (6→7, later firm expansion) — cosmetic, not re-scored |
| `2026-05-16-fixture-test-requirement.md` | Hook-1 script deleted | no action, in-file Amendment present |
| `2026-06-30-no-manual-trading-cfd-retirement.md` | Attestation script absent | no action, in-file addendum present |
| `2026-06-22-cost-geometry-pregate.md` | Pepperstone reference stale | no action for the `operational_rules.md` mirror (repaired); the ADR's own §2a/§5 text + script docstring remain unrepaired — pre-existing, out of this citation's scope |
| `2026-06-24-oanda-retirement.md` | Sole-canonical-feed claim stale | no action, both reciprocal fields present |
| `2026-08-04-strategy-coldstore-phase-a.md` | Superseded by Phase B/C | no action, addendum + both reciprocal fields present |
| `2026-08-02-pepperstone-feed-retirement.md` | §2-F KEEP narrowed | no action, reciprocal field present (minor label-naming inconsistency noted, not substantive) |
| `2026-07-10-r6-nogo-futures-residual-disposition.md` | Sole-active-lane claim superseded twice | no action, both reciprocal fields present |
| `2026-06-05-concept-admissibility.md` | Machinery retired | no action, top banner present |
| `2026-07-20-stage8-variance-dominance-risk-neff-gate.md` | Producer status softened | no action, reciprocal field present |
| `2026-07-01-add-back-metric-layer-split.md` | Graduation trigger never fired | no action, self-admitting addendum present |
| `2026-06-05-sweep-engine.md` | Machinery retired, doctrine survives | no action, banner + addendum present |
| `2026-06-23-tv-backtest-egress-automation.md` | Original chain dead | no action — addendum landed **this session** (2026-08-29), reciprocal link on `2026-08-07-loop-s2-signal-host-fork.md` verified present |
| `2026-05-28-audit-doc-generation-doctrine.md` | Deliverables pruned, ADR intact | no action, dispositioned by name in a prior programme-audit note |
| `2026-07-23-c1-rung-selection-ev-objective.md` | Live-rung claims historical | no action, addendum + reciprocal field present |
| `2026-07-26-mechanism-counterparty-constraint-boundaries.md` | Clause 2-B narrowed then retired | no action, two addenda + reciprocal field present |
| `2026-08-05-blusky-inactivity-unsourced-encoding.md` | §4 T1 fired, discharged | no action, reciprocal field + code match present |
| `2026-05-22-reality-check-harness.md` | Component A dormant | no action, banner present |
| `2026-07-11-challenge-era-claims-rescope.md` | ACTIVE_FIRM claim superseded | no action, reciprocal field + in-file addendum present |
| `2026-08-04-iterate-closure-exit-mandatory.md` | Advisory-coverage clause narrowed | no action, reciprocal field + gate wiring confirmed |
| `2026-05-16-fxify-correct-timeout-semantic.md` | All falsifier limbs dead | no action, banner present |
| `2026-06-04-lean-portfolio-meta-layer.md` | §4 falsifier fired, meta-layer dormant | no action, discharge blockquote present |
| `2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` | §2.3 default flipped | no action, addendum + code match present |
| `2026-06-07-decompound-remc-hold.md` | Headline figures corrected, limbs dormant/orphaned | no action, three addenda present |
| `2026-07-12-prop-portfolio-four-friendly-firms.md` | ACTIVE_FIRM correction note itself one Phase stale | no action at top level — see §7 for a small opportunistic addendum-to-the-addendum |
| `2026-07-11-ops-cfd-estate-retirement.md` | KEEP row now moot | no action, reciprocal field present |
| `2026-08-19-loop-persona-hierarchy-review-panel.md` | Roster narrowed 19→9 | no action, reciprocal field present |
| `2026-06-05-monorepo-layer-boundaries.md` | §2.1 table stale, documented in `REPO_MAP.md` | no action — `REPO_MAP.md` is the ADR's own designated successor surface |
| `2026-07-17-c1-rail-build-account-registration-go.md` | Layer-line ACTIVE_FIRM claim false | no action at top level — reciprocal field exists though wording understates the deletion; see §7 for a small wording fix |
| `2026-05-23-allocation-refresh-2.md` | Forward monitoring dead | no action, three addenda present |
| `2026-08-04-tradeify-venue-descope-eval-included.md` | Stale "registry still owed" phrase | no action — self-contradicted one line down in the same file; see §7 for a trivial opportunistic fix |
| `2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md` | Standing research interest suspended | no action, recorded in prose on `2026-08-04-tradeify-venue-descope-eval-included.md` §6 (reclassified in from DECAYED_UNDOCUMENTED, §2) |

---

## §5 — UNCERTAIN (1)

**`docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md`** — self-flagged "unruled seam"
(S1: does Forbidden-move-4's instrument-hop bar reach a pre-G0 kill's construct; S2: does the deep-lane
GO/cost-dry-run discharge transfer to this channel). Confirmed genuinely still open as of 2026-08-29 —
this is the skill's by-design case, an honest open question, not decay. **Resolving evidence:** an
explicit operator ruling or superseding addendum settling S1/S2, or a later ADR naming FM-4's pre-G0
reach / cross-channel GO transfer without cross-linking here (which would flip this to
DECAYED_UNDOCUMENTED). **Re-check trigger:** next construct proposed on 6A/M6A or GC/MGC (forces S1/S2
to a head), or the 2026-11-08 §4 date, whichever comes first.

---

## §6 — Safety-relevant sub-finding: M1 arming gate (`2026-07-22-c1-venue-native-monitoring-maturity.md`)

Two narrow, documented-elsewhere sub-claims inside an otherwise `STILL_APPLICABLE` ADR:

(a) §10 Addendum-2026-07-31b hook-4 comment (dated 2026-08-08) still literally reads "the arm path
never invokes that validator" — now false (fixed 2026-08-09, per CLAUDE.md). Correction lives in
CLAUDE.md and the acceptance JSON's notes, never back-edited into the ADR. **Remediated** — light
addendum.

(b) `docs/notes/rail_build/RUNBOOK.md`, cited as a live Rule-0 anchor, is absent from the working tree —
already dispositioned as an expected public-clone 404 in `docs/notes/audits/2026-08-21-coherence-campaign.md`
(row C-P3-05). No action needed.

**The safety gate itself is confirmed enforced in code today**, independently verified this session:
`ops/c1_rail/c1_rail_arm.py` calls `validate_c1_monitoring_acceptance.validate(require_resolved=True)`
in the code path `--arm` actually invokes; the acceptance artifact's live `status` field reads
`"CODE_LANDED"` (not `"RESOLVED"`), so a plain `--arm` today is refused. The only override is an
explicit, ratified, logged operator deviation (`--acknowledge-m1-unresolved`), not a silent bypass.
CLAUDE.md's safety invariant — `dry_run=false` may not be set while M1 is not `RESOLVED` — holds.

---

## §7 — Remediation ledger

**Applied this session** (addenda landed per Rule 14 — frozen body untouched, dated addendum + header
metadata correction only): findings #1, #2, #3, #5, #6, #7, #8, #9, #10, #11, #12, #13, #14, #15, #16,
#17, #18, #19, #20 from §3 (19 of 20) — see commit history for the exact diffs.

**Logged as forward obligation, not fixed this session:**
- Finding #4 (`2026-07-16-root-doc-charter-dedup.md`) — the CLAUDE.md size-hook exception is an
  operator judgment call (accept as a bounded safety-content exception vs. trim back to pointer form),
  not a mechanical discharge. Owner: next session touching CLAUDE.md's Live-execution posture section,
  or the 2026-11-08 quarterly review at latest — logged on `STATE.md`.

**Living-document fixes (Rule 7 — corrected in place, not addendum-gated):**
- `STATE.md:197` "blind channel... 1/3" corrected to 2/3, per the no-counterparty ADR's own
  2026-08-23-dated canonical count.
- `STATE.md` 2026-11-08 forward-board section gains the missing line for the regime-candidate flag
  lane's §4 two-strikes check (finding #19).
- `docs/adr/INDEX.md` regenerated via `check_adr_graph.py --regenerate-index` after header-field
  additions, discharging the mirrored-staleness instances on findings #6/#8.

**Light opportunistic fixes** (trivial, same-file, bundled with the addendum pass above, not separately
re-scored): the `2026-07-12-prop-portfolio-four-friendly-firms.md` nested-staleness note, the
`2026-07-17-c1-rail-build-account-registration-go.md` Layer-line wording, and the
`2026-08-04-tradeify-venue-descope-eval-included.md` "registry still owed" phrase.

**Tooling defects surfaced, not fixed this session** (out of scope for an ADR-content audit; logged for
a separate task):
- `scripts/check_advisor_dedup.py::load_corpus()` structurally never indexes `docs/adr/`, guaranteeing
  false negatives for any ADR-to-ADR dedup check (root cause of finding #1).
- `docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md`'s Phase-3 repair-sweep regex is a
  literal-string match that misses paraphrased restatements of the superseded formula (root cause of
  finding #18 going unrepaired at authoring time).

**Adjacent non-ADR drift noted in passing, not remediated this session** (belongs to a different
retention surface):
- `lab/analysis/legacy/eurusd_pattern_enum/`: `README.md`'s phase table and `lab/CATALOG.md`'s `ACTIVE`
  tag are both stale against the campaign's own logged Phase-4 closure record.

---

## §8 — Discipline check

```
[x] Full Accepted-ADR list enumerated from the actual Status header (161, backtick-normalized)
[x] Phase 1 scan covers every ADR in the list, none silently dropped (27/27 batches returned)
[x] Phase 2 verify runs on every non-STILL_APPLICABLE flag, framed to refute not confirm (14/14 batches returned)
[x] Every Phase 2 verdict has real reasoning behind it, not placeholder/degenerate output
[x] DECAYED_UNDOCUMENTED findings each carry a named remediation AND an owner/date (19 fixed this session, 1 logged forward)
[x] UNCERTAIN verdicts each carry a named resolving check and a re-test date, not left open-ended (the 1 surviving case)
[x] Index/summary-mirror documents checked for the same stale claim, not just the source ADR (2 caught: docs/adr/INDEX.md, STATE.md)
[x] Output artifact lands at docs/notes/audits/adr-corpus/, following brief-authoring's audit-note template
[x] This is the first full run — no "consecutive all-clear" ceremony risk to check yet
[x] Next trigger named: cadence — piggyback on the next programme-audit quarterly cycle; event — before
    the next repo-public snapshot, or if a single ADR's falsifier is found to have fired undischarged
```
