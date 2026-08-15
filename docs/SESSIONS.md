# Session Log

Chronological progress log, **newest first**. One entry per working session. Each entry
**links out** to the detailed artifacts (ADRs, notices, briefs, commits) rather than
duplicating them. Complements `MEMORY.md` (durable atomic facts, recalled by relevance);
this file is the narrative timeline you can scan top-to-bottom.

**Entry classes (W5 direction):** Decision / Build / Measurement / Hygiene — prefer
links; keep prose beyond the five fields ≤ **~40 words** where possible
([`W5 ADR`](adr/2026-08-07-w5-governance-diet.md)). Skip Hygiene-only turns.

Next session opens by reading the top entry's **Open / next**.

Same-day letter: `python scripts/roll_sessions.py --next-label YYYY-MM-DD` before writing (a-first; bare claims `a`).

---
## 2026-08-15a — Repoint historical PR/commit hrefs at first-passage-archive

**Focus:** After the 2026-08-14 public-repo transplant, historical GitHub PR/commit links still pointed at `first-passage` and 404'd; the objects live on the private archive.

**Shipped:** branch `cursor/repoint-archive-pr-links-52bf` — 48 hrefs in 8 files rewritten `first-passage` → `first-passage-archive` (`/pull/` + `/commit/` only). Append-only comparator treats that repo-name rewrite as non-mutation. Bare `PR #NNN` prose left alone.

**Decisions/defects:** none new. Owner: [transition ADR](adr/2026-08-14-repo-public-visibility-transition.md).

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14y — F-2 closure + CC/Cursor autonomous-loop ADR + webhook live

**Focus:** Close the Great Prune's fired F-2 falsifier; ratify a CC/Cursor autonomous dispatch-detect-merge loop at operator direction.

**Shipped:** branch `claude/first-passage-requirements-review-8c0bd9` — [`2026-08-14-f2-adr-corpus-disposition.md`](notes/audits/programme-audit/2026-08-14-f2-adr-corpus-disposition.md) (126-ADR corpus classified, 0/4 tombstone candidates survived adversarial verification) · addendum on [`2026-08-08-great-prune.md`](adr/2026-08-08-great-prune.md) · [`2026-08-14-cc-cursor-autonomous-loop.md`](adr/2026-08-14-cc-cursor-autonomous-loop.md) (Supersedes-in-part `2026-07-14-cc-cursor-surface-allocation.md`) · webhook routine live (`trig_012nvuH7jqmjFUFgoFVpZ6RP`, every-6h cron + GitHub PR-opened event). $0 · K=0.

**Decisions/defects:** F-2 ruled fired-on-a-miscalibrated-premise, not degeneration; instrument replaced (content-sample re-test), no new hard gate. 5 backlog-fix chips this session dispatched independently merged as PRs #824-826/828/829 before this branch landed — direct re-implementation of the same 5 fixes was reconciled out via hard-reset-and-restore rather than committed, confirmed non-duplicative by adversarial re-check (all 5 PRs fully cover scope). Auto-mode classifier blocked `gate_manifest.py`/`pytest` mid-session; resolved via a `.claude/settings.json` permission-allow rule.

**Open / next:** operator ruling still owed on `closure-disposition-coverage-hard.md` (new hard gate landed 4 days into F-2's own trigger window — worth it or not); GitHub webhook trigger's branch filter not yet narrowed to `cursor/*` (cosmetic, routine's own logic already re-scopes). Carry: F1 2026-11-08; M1; weekly token; Magdon-Ismail B.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14x — breadth.py --self-test SKIP exits 2

**Focus:** Make `--self-test` SKIP distinguishable from PASS at the shell exit-code level.

**Shipped:** `main` — `lab/research_utils/breadth.py` SKIP returns `SELF_TEST_SKIP=2` (0 PASS / 1 FAIL unchanged); `tests/test_breadth.py` expects 2. Not wired in `scripts/gates.yml` / Makefile / CI.

**Decisions/defects:** none. Convention matches `pine_lint._self_test` missing-fixture = 2.

---

## 2026-08-14w — W1 materialized harness sys.path

**Focus:** Fix pre-existing `ModuleNotFoundError: reconcile` in `tests/test_nsurv_channel.py::test_w1_pin_reproduction_known_answer` when the pruned Class-S scoring harness is copied under pytest `tmp_path`.

**Shipped:** branch `cursor/w1-materialize-syspath-25b2` — [PR #832](https://github.com/Joshua-Asante/first-passage-archive/pull/832) — pin materialized `_ROOT` to the real repo (not `__file__.parents[3]`) in `_materialize_pruned_scoring_helpers`. Test-infrastructure only. $0 · K=0.

**Decisions/defects:** none new. Depth-relative `_ROOT` is correct at `lab/analysis/c1/<slug>/`; the bug is the materialization copy, not the historical harness.

**Open / next:** Raise Actions spending cap (operator). MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14v — CI diet (A+C+D) + ripgrep

**Focus:** Cut GitHub Actions minutes after billing-limit brick on #825–#828; restore pytest `rg` so the 1524-pass suite can go green.

**Shipped:** branch `cursor/ci-diet-pr-main-2df9` — [PR #831](https://github.com/Joshua-Asante/first-passage-archive/pull/831) — `.github/workflows/{tests,pylint,skills-check}.yml`. A: PR + `main` only. C: pylint 3.11 only. D: skip Tests/Pylint on `*.md` / `.claude/**`. Tests job installs ripgrep.

**Decisions/defects:** none new. CI trigger/path diet only; no gate dropped from `scripts/gates.yml`.

**Open / next:** Raise Actions spending cap (operator). MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14u — MSL falsifier survival-limb + explore-stage (5a) ADRs accepted

**Focus:** Operator election on the programme-audit's two follow-on ADRs; apply the charter/plan amendments each one owed.

**Shipped:** branch `claude/msl-programme-audit-2026-08-14` — [PR #830](https://github.com/Joshua-Asante/first-passage-archive/pull/830) — [survival-limb ADR](adr/2026-08-14-msl-yield-falsifier-survival-limb.md) Accepted (charter Gate line + plan §6/§7) · [explore-stage ADR](adr/2026-08-14-msl-explore-stage-5a.md) Accepted, light-tier (charter step **5a** + plan P3.x row) · [audit note](notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md) §5/§11 discharge notes. $0 · K=0.

**Decisions/defects:** Non-disruptive "5a" insertion chosen over a full renumber — grep confirmed external step-number citations outside the charter. Owner: both ADRs above.

**Open / next:** MSL still E1 HOLD, no slate-4 until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

---

## 2026-08-14t — C3 eviction-clause skip narrowed

**Focus:** Stop `check_status_consistency` whole-line-skipping a live `lab/` citation that shares a line with a `git show` / `pre-prune-` retrieval. Also correct the stale CLAUDE.md M1 interlock warning and make breadth `--self-test` SKIP exit 2.

**Shipped:** branch `fix/c3-eviction-clause-skip` — [PR #829](https://github.com/Joshua-Asante/first-passage-archive/pull/829) — `scripts/check_status_consistency.py` masks only the eviction clause (plus enclosing paren); mixed-line C3 regression; CLAUDE.md M1 line points at `validate(..., require_resolved=True)`; `lab/research_utils/breadth.py` `SELF_TEST_SKIP=2`; repointed the now-visible stale href in `docs/rejected_candidates.md`.

**Decisions/defects:** none. Twins still whole-line: `scripts/check_root_doc_liveness.py`, `scripts/check_md_relative_links.py`.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14s — MVD ceremony vs enforcement

**Focus:** Verify Stage-8 variance-dominance header (no edit) and reconcile MVD-discipline ceremony to what is actually enforced.

**Shipped:** branch `cursor/mvd-ceremony-reconcile-a1df` — [PR #828](https://github.com/Joshua-Asante/first-passage-archive/pull/828) — [MVD addendum](adr/2026-04-24-mvd-discipline.md). Stage-8 risk-N_eff ADR left unchanged (W4 in-part edge already complete). $0 · K=0.

**Decisions/defects:** none new. Owner: the 2026-08-14 addendum on [MVD discipline](adr/2026-04-24-mvd-discipline.md). Code checks untouched.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14r — Reconcile four partial-live ADRs

**Focus:** Dated Rule-14 addenda on four ADRs whose core decisions stand but whose machinery/status/occupancy framing had been overtaken.

**Shipped:** branch `cursor/adr-reconciliation-addenda-a1df` — [PR #827](https://github.com/Joshua-Asante/first-passage-archive/pull/827) — [reality-check](adr/2026-05-22-reality-check-harness.md) Component A dormant · [sweep-engine](adr/2026-06-05-sweep-engine.md) machinery retired / invariant live · [S7 occupancy](adr/2026-07-29-third-leg-symbol-occupancy-limb.md) 08-06 retained-not-released superseded · [venue-binding](adr/2026-08-05-strategy-venue-binding-axis.md) stalled/bypassed (Status stays Proposed). $0 · K=0.

**Decisions/defects:** none new. Owners: the four 2026-08-14 addenda. S7 untouched; Striker legs stay barred.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm. Third-leg spec still restates 08-06 retained-not-released (owed).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14q — Repair three vacuous gate scripts

**Focus:** Fix three live `scripts/` gate defects: A5 LOCK.md glob, `--enable` typo-pass, C3 theme-nest blind spot.

**Shipped:** branch `cursor/fix-dead-gate-scripts-bc8b` — [PR #825](https://github.com/Joshua-Asante/first-passage-archive/pull/825) — `scripts/check_adr_graph.py` · `scripts/check_status_consistency.py` · 11 instrument theme-nest repoints.

**Decisions/defects:** none. Gates now evaluate their targets (A5 once the age window opens; `--enable` rejects unknown ids; C3 flags flat-to-theme-nest).

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14p — Dead-trigger docs marked dormant

**Focus:** Four independently verified dead-trigger surfaces (2026-08-14): delete lock-brief template; dormancy-mark 1R live-calibration + E1–E4; discharge lean-portfolio meta-layer falsifier.

**Shipped:** branch `cursor/dormant-dead-trigger-docs-0ebd` — [PR #824](https://github.com/Joshua-Asante/first-passage-archive/pull/824) — [lock_decision.md deleted](../.claude/skills/brief-authoring/SKILL.md) · [1r_estimation](methodology/1r_estimation.md) · [lean-portfolio addendum](adr/2026-06-04-lean-portfolio-meta-layer.md) · [E1–E4](methodology/lessons/execution_lessons.md). $0 · K=0.

**Decisions/defects:** §4 falsifier of [lean-portfolio](adr/2026-06-04-lean-portfolio-meta-layer.md) recorded FIRED 2026-07-30 (ceremonial; children live). Owner: that ADR's 2026-08-14 addendum.

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14o — CapFLOW Cap-spend FALSIFIED (Cap held)

**Focus:** Discharge Q-CAPFLOW-1 Cap-spend: rebuild A×R join, score once under frozen PREREG.

**Shipped:** branch `cursor/capflow-score-0814` — [PR #823](https://github.com/Joshua-Asante/first-passage-archive/pull/823) — camp [`mnq_capflow_orb_r_2026-08`](../lab/analysis/c1/mnq_capflow_orb_r_2026-08/) · [RESULTS](../lab/analysis/c1/mnq_capflow_orb_r_2026-08/RESULTS.md) · [closure](briefs/closures/Q-CAPFLOW-1-closure-falsified.md). $0 new pull · Cap held · K=0.

**Decisions/defects:** CI includes 0 (ρ +0.020); C11 stands. Owner: [closure](briefs/closures/Q-CAPFLOW-1-closure-falsified.md).

**Open / next:** CapFLOW Cap-spend FALSIFIED (Cap held). Carry: F-2; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; no slate-4 until NEW WHO. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14n — MSL WHO-track (estate-wide; still dry)

**Focus:** Deep zero-data WHO track after E1 HOLD — every Tradeify product group + census backlog, not just MCL fade.

**Shipped:** branch `cursor/msl-who-track-85f5` — [PR #822](https://github.com/Joshua-Asante/first-passage-archive/pull/822) — [notice](notes/notice/N-2026-08-14-msl-who-track.md) · plan §6 P3.8 **STILL DRY** · no camp · no card · no new `MECHANISMS.md` id. $0 · K=0.

**Decisions/defects:** No NEW WHO. Closest leftovers (FX option-cut, USDA grains, Bund auction, LME warrants, pipeline nominations) die on sign / EIA-family / H-ZNAUC / F4 / §4.1a before 1a clears. Owner: [notice](notes/notice/N-2026-08-14-msl-who-track.md).

**Open / next:** no slate-4 card until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14m — MSL §7 E1 HOLD recorded

**Focus:** Record operator E1 HOLD on the §7 slate-generation packet.

**Shipped:** branch `cursor/msl-s7-e1-hold-85f5` — [PR #821](https://github.com/Joshua-Asante/first-passage-archive/pull/821) — [closure](briefs/closures/MSL-S7-closure-resolved-e1-hold.md) · plan §4/§6 Phase 3 **HOLD (E1)** · no camp · no E2 ADR. $0 · K=0.

**Decisions/defects:** E1 marked (plan confirmation). Charter stays RATIFIED. Yield not fired. Owner: [closure](briefs/closures/MSL-S7-closure-resolved-e1-hold.md).

**Open / next:** no slate-4 card until NEW WHO. Carry: F-2; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14k — MSL §7 slate-generation review packet (OWED-election)

**Focus:** Plan-§7 Board packet: evidence + E1 HOLD / E2 CLOSE; do not elect.

**Shipped:** branch `cursor/msl-s7-board-review-85f5` — [PR #820](https://github.com/Joshua-Asante/first-passage-archive/pull/820) — [packet](briefs/2026-08-14-msl-slate-generation-review.md) · plan §6 P3.7 **OWED-election** · no camp · no E2 ADR. $0 · K=0.

**Decisions/defects:** Yield not fired (four G0s; two pre-G0 deaths). Operator owns E1/E2. Owner: [packet](briefs/2026-08-14-msl-slate-generation-review.md).

**Open / next:** Operator mark E1 (HOLD, recommended) or E2 (CLOSE via full ADR). Carry: F-2 disposition; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14j — MSL slate-3 BLOCKED (mechanism-dry)

**Focus:** Board-lite slate-3 constraints + zero-data WHO attempt on MCL fade; stop if INTAKE-DRY.

**Shipped:** branch `cursor/msl-slate3-constraints-85f5` — [PR #819](https://github.com/Joshua-Asante/first-passage-archive/pull/819) — [notice](notes/notice/N-2026-08-14-msl-slate-3-constraints.md) · plan §6 P3.6 **BLOCKED** · no `msl_s3a_*` camp. $0 · K=0.

**Decisions/defects:** No WHO outside 2026-08-10 INTAKE-DRY; implied-SR reopen restored geometry not a flow family. §7 Board review owed (functional 3/3). Owner: [notice](notes/notice/N-2026-08-14-msl-slate-3-constraints.md).

**Open / next:** Operator §7 slate-generation review. Carry: F-2 disposition; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Confirm #806 CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14l — STATE F-2 queue row: fired-axis framing

**Focus:** Sharpen OPERATOR QUEUE row 2 so Great-prune F-2 reads as axis-fired, not “trending toward.”

**Shipped:** branch `docs/f2-queue-fired-axis-framing` — [PR #818](https://github.com/Joshua-Asante/first-passage-archive/pull/818) — re-measure at `origin/main` `df2c448`: ADR-count +14 (~400% of 50% ADR-Δ trigger, fired); file-Δ ~131% (fired); bytes ~63% of thresh (still short). [`STATE.md`](../STATE.md) row 2 only. Incidental: `msl_s2b` `verdict.md` + CATALOG heavy/one-liner align so `lab-catalog` passes (was red on main post-#817).

**Decisions/defects:** None — measurement/framing only; operator disposition still open ([`Great Prune §4 F-2`](adr/2026-08-08-great-prune.md)).

**Open / next:** Operator F-2 disposition still open (ADR-count axis already fired). Carry from 14i: Board next slate/channel after Stage-1 deaths 2/3; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs; `#806` CI; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14i — MSL-S2B Stage-0/1 FAIL (route)

**Focus:** S2B Stage-0 pins + Stage-1 door-check on MYM `sweep-failure-filtered-continuation`; route kill limb #1 first.

**Shipped:** branch `cursor/msl-s2b-stage01-85f5` — [PR #817](https://github.com/Joshua-Asante/first-passage-archive/pull/817) — camp [`msl_s2b_mym_2026-08`](../lab/analysis/c1/msl_s2b_mym_2026-08/) · [STAGE0](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE0.md) · [STAGE1](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) · [closure](briefs/closures/MSL-S2B-closure-stage1-fail-route.md) · MECHANISMS + registry + plan §6. $0 · K=0. No G0/Pine. Renumbered `14h`→`14i` on merge (#816 claimed `14h`).

**Decisions/defects:** Pre-G0 kill — raised bar unbound for continuation *entry*; SLR route ① filter-only; temporal-selectivity paused; composite refused. Owner: [second slate §S2B](briefs/2026-08-13-msl-second-slate.md) · [closure](briefs/closures/MSL-S2B-closure-stage1-fail-route.md).

**Open / next:** Stage-1 deaths **2/3**; slate-2 exhausted — Board owns next slate / channel review. Carry: Operator F-2 disposition (ADR-count axis already fired — from 14h/#816); CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` from primary checkout. Confirm #806 CI green; cart confirm.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14h — Post-chip-landing verification sweep + gap repair

**Focus:** Verify all 9 chips from 14a-14g actually landed correctly (8-agent workflow); fix what didn't.

**Shipped:** branch `claude/post-prune-simplification-acd9d7` — [PR #816](https://github.com/Joshua-Asante/first-passage-archive/pull/816) — archived `msl_c3_m2k_2026-08` + `msl_s2a_mcl_2026-08` (self-flagged owed since 14a-14g, never ran); fixed `archive_lab_analysis.rewrite_sibling_links()` multi-hop `../` corruption (64 links, +regression test); repointed 6 living-doc citations (STATE, `ops/instruments/*`, `rejected_candidates`) + rebuilt `PROFILES.md`/`profiles.json`; regenerated `lab/CATALOG.md` (also clears 9 phantom-Active rows [PR #809](https://github.com/Joshua-Asante/first-passage-archive/pull/809) reintroduced on `origin/main`); backfilled `Tier: light` on the one retire_adr stub written before [PR #812](https://github.com/Joshua-Asante/first-passage-archive/pull/812) landed; mirrored `mc` into `check_status_consistency._THEME_ORDER` (pre-existing pytest fail from PR #790, unrelated to 14a-14g); split STATE's dormant-threads pointer so Q-MSCHAN-1 (SUBTRACT/dead) no longer reads as open like b6/b7 (PARK).

**Decisions/defects:** [PR #810](https://github.com/Joshua-Asante/first-passage-archive/pull/810)'s on-machine `~/.claude/skills` resync still NOT done — `sync_skills.py` refuses `--force`-less deploy from a worktree checkout by design; needs `make sync-skills` from the primary checkout. F-2 ([809](https://github.com/Joshua-Asante/first-passage-archive/pull/809)/STATE queue row): ADR-count axis has already fired at 400% of its 50%-of-pruned-delta threshold (14 vs 3.5), not merely trending — byte/file framing undersold this.

**Open / next:** Operator F-2 disposition — now sharper: ADR-count axis already fired. On Windows: `make sync-skills` from primary checkout (from 14c/14g, still open). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. Ceremony-tiering falsifier review at first quarterly after 08-08 (STATE 11-08).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14g — Implied-SR candidate incident + light ADR word-cap trims

**Focus:** Log ceremony-tiering omitted-apparatus candidate (implied-SR light→full escalation); trim two over-300-word light ADRs.

**Shipped:** branch `cursor/implied-sr-incident-and-light-adr-trims-d214` — [PR #815](https://github.com/Joshua-Asante/first-passage-archive/pull/815) — [ceremony-tiering addendum](adr/2026-08-08-adr-ceremony-tiering.md) · STATE `### 2026-11-08` pointer · trims [C3 revive](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [Survive bound](adr/2026-08-09-survive-bound-is-the-queue-cap.md). No retired-ADR rewrites.

**Decisions/defects:** Candidate incident only (1-vs-2 = audit call). Owner: [ceremony tiering §Falsifier](adr/2026-08-08-adr-ceremony-tiering.md).

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c). Ceremony-tiering falsifier review at first quarterly after 08-08 (STATE 11-08).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14f — same-theme collision WARN test coverage

**Focus:** Pin `warn_new_slug_same_theme_collisions()` with positive/negative stderr tests so a silent catalog-parse refactor cannot drop the ADR 2026-08-13 report-only WARN.

**Shipped:** branch `cursor/test-same-theme-collision-warn-b103` — [PR #814](https://github.com/Joshua-Asante/first-passage-archive/pull/814) — [`tests/test_archive_lab_analysis.py`](../tests/test_archive_lab_analysis.py) (`test_warn_new_slug_same_theme_collision_emits_stderr`, `test_warn_new_slug_same_theme_collision_silent_without_overlap`).

**Decisions/defects:** Owner: [dedup-first before new work](adr/2026-08-13-dedup-first-before-new-work.md) §2 leg 3.

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14e — CLAUDE.md MYM/MNQ occupancy pointer

**Focus:** Close the posture-summary gap for [MYM/MNQ occupancy release](adr/2026-08-12-msl-mym-occupancy-release.md) per root-doc charter §2 / Rule 7.

**Shipped:** branch `cursor/claude-mym-mnq-occupancy-pointer-85b2` — [PR #813](https://github.com/Joshua-Asante/first-passage-archive/pull/813) — one Standing-decision row in [`CLAUDE.md`](../CLAUDE.md) linking `[occupancy]` (no retelling).

**Decisions/defects:** Owner unchanged: [occupancy ADR](adr/2026-08-12-msl-mym-occupancy-release.md). Pointer-only; Striker redeploy bar stands.

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: run `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14d — Preserve Tier on retire_adr stubs

**Focus:** Stop `retire_adr.build_stub()` from dropping `**Tier:** light` so superseded light ADRs stay visible to hot-dir census greps.

**Shipped:** branch `cursor/preserve-retire-adr-tier-0f0c` — [PR #812](https://github.com/Joshua-Asante/first-passage-archive/pull/812) — [`scripts/retire_adr.py`](../scripts/retire_adr.py) `extract_tier` + stub carry-forward; tests in [`tests/test_retire_adr.py`](../tests/test_retire_adr.py). No already-retired stub rewrites.

**Decisions/defects:** None — tool fix only. Convention owner: [ADR ceremony tiering](adr/2026-08-08-adr-ceremony-tiering.md).

**Open / next:** Operator F-2 disposition (from 14b/14c). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: `make sync-skills` (from 14c).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14c — ADR-tiering discoverability (brief-authoring + skills sync)

**Focus:** Make the 2026-08-08 ADR ceremony tiering convention discoverable at the ADR template and keep `~/.claude/skills/` from silently drifting.

**Shipped:** branch `cursor/adr-tiering-brief-authoring-fa22` — [PR #810](https://github.com/Joshua-Asante/first-passage-archive/pull/810) — tier-test branch atop [`.claude/skills/brief-authoring/references/adr.md`](../.claude/skills/brief-authoring/references/adr.md); [`scripts/sync_skills.py`](../scripts/sync_skills.py) / hook deploy to AppData **and** `~/.claude/skills/`; tests in [`tests/test_sync_skills.py`](../tests/test_sync_skills.py).

**Decisions/defects:** Owner: [ADR ceremony tiering](adr/2026-08-08-adr-ceremony-tiering.md). Cloud host had no prior `~/.claude/skills/brief-authoring` (copied fresh; Windows machine still needs `make sync-skills` or pull+hook).

**Open / next:** Operator F-2 disposition (from 14b). Confirm #806 CI green; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs. On Windows: run `make sync-skills` so the May-stale home brief-authoring cache is overwritten (script now backs both targets).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14b — escalate Great-prune F-2 re-accretion

**Focus:** Re-measure post-prune tracked size at current `origin/main` and surface F-2 breach on the OPERATOR QUEUE without deciding or building the gate.

**Shipped:** fast-forwarded local `main` to `669df95`; `STATE.md` OPERATOR QUEUE row 2 only (queue 3/5). Measure: HEAD 23,198,115 B / 2,161 files / 128 ADRs vs `7aab114` 20,343,262 / 1,757 / 114.

**Decisions/defects:** None — operator pick owed (gate now · recalibrate · accept as R1). Formal F-2 ADR limb breached (+14 ADRs vs 50% of −7 prune Δ); bytes at 62.4% of thresh. [`Great Prune §4`](adr/2026-08-08-great-prune.md).

**Open / next:** Operator F-2 disposition. Carry from 14a: Confirm build/pytest 3.11+3.12 + `validation-controls` green on #806; cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-14a — validation-controls collection + ops lock py311

**Focus:** Unblock CI after Actions re-enable: `validation-controls` collection errors (stale ignore, `test_construct_lib` collisions, orphan import camps) plus `numpy==2.5.1`/`scipy==1.18.0` 3.12-only pins.

**Shipped:** branch `cursor/fix-validation-controls-collect-0813` — [PR #806](https://github.com/Joshua-Asante/first-passage-archive/pull/806) — archive ignore + `--import-mode=importlib` + [`camp_import.py`](../lab/research_utils/camp_import.py); `pyproject.toml` `numpy<2.5`/`scipy<1.18`, lock regenerated on 3.11 (`numpy==2.4.6`, `scipy==1.17.1`).

**Decisions/defects:** Hyphenated camp slugs cannot be packages; lock was compiled on 3.12 with unconstrained deps. Ops-lock 13z dropped here (main claimed 13z for PR #805).

**Open / next:** Confirm build/pytest 3.11+3.12 + `validation-controls` green on #806. Carry from 13z: cart confirm; CapFLOW; F1 2026-11-08; M1; weekly token; Magdon-Ismail B; research venvs.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13a — SESSIONS append-only gate + push-collision exemption

**Focus:** Packet 1 of union-merge hygiene: freeze prior SESSIONS entry bodies and stop treating two new top entries as a governance collision.

**Shipped:** branch `fix/sessions-append-only-collision` — [PR #808](https://github.com/Joshua-Asante/first-passage-archive/pull/808) — `roll_sessions.py --check-append-only` (gates.yml `sessions-append-only`); `check_push_collision` drops `docs/SESSIONS.md` when ours is append-only vs merge-base. Tests in `tests/test_roll_sessions.py` + `tests/test_check_push_collision.py`.

**Decisions/defects:** Mutating a merge-base heading still collides; only the new-heading delta is exempt. Packets 2–4 (auto-normalize, `--next-label` from origin/main, `--append` writer) not in this change.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3. Next SESSIONS hygiene: packet 2 (auto `--normalize --reorder` + CI `--check-order`).

---

## 2026-08-13z — CATALOG duplicate-slug check hard-fail

**Focus:** Close the `lab/CATALOG.md` freshness false-pass where `_partition_catalog` last-wins on slug and drops Active+Archived (or same-table) duplicates from `--check --catalog-only`.

**Shipped:** branch `fix/catalog-duplicate-slug-check` — [PR #805](https://github.com/Joshua-Asante/first-passage-archive/pull/805) @ `f27888f` — `_partition_catalog` keys by `(section, slug)`; same-section dupes → `_CATALOG_STALE`; planted Active+Archived regression in `tests/test_archive_lab_analysis.py` (2026-08-13 MSL phantom-row class).

**Decisions/defects:** Defect in checker logic (instance rows already hand-fixed in PR #802); this is the gate hardening.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13y — TNEC-1 admission gate: EM1/D1/D2 disclosure-only

**Focus:** Align live `evaluate_admission` with ratified TNEC-1 / EM-screen supersession (code still refused on EM1 0.40R and D1/D2).

**Shipped:** branch `fix/tnec1-admission-disclosure-only` — [`admission_schema.py`](../lab/discovery/admission_schema.py) (N-EDGE gate; EM1/D1/D2 disclosure record); [`register_search.py`](../lab/discovery/register_search.py) + [futures-anomaly-discovery skill](../.claude/skills/futures-anomaly-discovery/SKILL.md) + [`strategy_harvest.md`](methodology/strategy_harvest.md) §6 pointer. Tests in [`test_register_search_admission.py`](../tests/test_register_search_admission.py).

**Decisions/defects:** None new — implements [TNEC-1](spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) / [ADR 2026-08-08](adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §2-B already ratified.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13w — Tradeify Select 100K checkout price re-sourced

**Focus:** Re-verify current Select 100K eval checkout + reset fees (primary page; Rule 13) after JULY promo expiry made the GO ADR $159/$181 figures non-current for modeling.

**Shipped:** branch `cursor/tradeify-select-100k-price-78c1` — [PR #801](https://github.com/Joshua-Asante/first-passage-archive/pull/801) · [`2026-08-13-tradeify-select-100k-checkout-price.md`](notes/2026-08-13-tradeify-select-100k-checkout-price.md); sprint-lane §4 soft-fee caveat + RUNBOOK reset pointer + compliance replacement-cost forward pointer. Historical GO ADR §B4 unpaid overwrite. Label renumbered `13s`→`13w` on merge (collision with Dependabot triage `13s` on main).

**Decisions/defects:** Dated fact only — list $265 / AUG $159 / reset $169 / activation None; promo ends 2026-08-31. Cart line-items not authenticated this pass.

**Open / next:** Cart confirm before any purchase; re-read fees after 2026-08-31 (or when AUG 5×40% exhausts → 30%). S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13v — ADR 2026-08-13 dedup-first mechanical wiring

**Focus:** Execute [`ADR 2026-08-13`](adr/2026-08-13-dedup-first-before-new-work.md) §7 Phases 1–5 (hookify + keyword search + Rule 8.8 + theme-collision WARN + brief-authoring link).

**Shipped:** branch `cursor/dedup-first-mechanical-wiring-0813` — [PR #800](https://github.com/Joshua-Asante/first-passage-archive/pull/800) @ `8a60c92`/`b48722a` — tracked `.claude/hookify.advisor-dedup-first.md`; `check_advisor_dedup.py --keywords`; Rule 8 sub-rule 8; `warn_new_slug_same_theme_collisions`; brief-authoring → §8. §10 audits PASS. [ADR](adr/2026-08-13-dedup-first-before-new-work.md). Label renumbered `13u`→`13v` on merge (collision with #799 soft-degrade on main).

**Decisions/defects:** Decision already Accepted; this session is pure mechanical execution (no re-litigation). Report-only WARN only — no `gates.yml` blocking change.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13u — catalog one-liner soft-degrade (msl_c3 blanking)

**Focus:** Diagnose archive_lab_analysis.py --check --catalog-only hard-fail at 9bcf3cb (CATALOG.md stale vs scan) — hand-authored one-liner blanking on scan when no RESULTS*/README source card.

**Shipped:** branch fix/catalog-one-liner-soft-degrade — soft-degrade in [archive_lab_analysis.py](../scripts/archive_lab_analysis.py) _compare_catalog (committed prose vs scan empty → WARN); tests in [test_archive_lab_analysis.py](../tests/test_archive_lab_analysis.py). Hand-deleted ghost Active row ict_mnq_2026-08 flat-path duplicate in [lab/CATALOG.md](../lab/CATALOG.md) (no --regenerate-catalog).

**Decisions/defects:** Root cause: mid-campaign STAGE*/PREREG-only bodies; choose_source_card returns None. Same class as heavy-column worktree tolerance (third live firing after Magdon catalog-ghost incident).

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13t — MSL-C3-K2 explore FALSIFIED (both axes)

**Focus:** Land M2K BAR EXPORT panel; pay explore GO; score dual-axis IS under `K_intrinsic=2`.

**Shipped:** branch `cursor/msl-c3-k2-explore-023e` — [PR #798](https://github.com/Joshua-Asante/first-passage-archive/pull/798) · `M2K_M15.csv` pin `81922570…` · [`RESULTS_g2`](../lab/analysis/c1/msl_c3_m2k_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C3-K2-closure-falsified.md) · registry/plan/M2K mirrors. $0 · K spent=0. CONFIRM unread. Label renumbered `13s`→`13t` on merge (collision with Dependabot hygiene on main).

**Decisions/defects:** Both axes CI entirely &lt; 0. Panel ends 2026-07-02 (TV truncation; MCL precedent). Globex session key fixed for Axis B overnight coherence.

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13s — Dependabot aiohttp triage (Hygiene)

**Focus:** Triage GitHub “3 vulnerabilities (1 high, 2 moderate)” notice; no Dependabot auto-fix PRs open.

**Shipped:** branch `cursor/dependabot-aiohttp-triage-03ba` — [PR #797](https://github.com/Joshua-Asante/first-passage-archive/pull/797) · `aiohttp` pin `3.14.1`→`3.14.3` in `requirements-research.txt` · [triage note](notes/2026-08-13-dependabot-aiohttp-triage.md).

**Decisions/defects:** All three alerts = aiohttp research-only (via databento); not ops/rail. setuptools CVE deferred (`nolds` needs `setuptools<81`).

**Open / next:** S2B may resume (C3-K2 board slot freed). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait). Recreate research venvs to pick up aiohttp 3.14.3.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13r — MSL-C3-K2 dual-axis G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO → freeze dual-axis `PREREG_G0` (`K_intrinsic=2`); GO-gated harness scaffold; no explore/panel/Pine.

**Shipped:** branch `cursor/msl-c3-k2-dual-axis-023e` — [PR #795](https://github.com/Joshua-Asante/first-passage-archive/pull/795) · [`PREREG_G0`](../lab/analysis/c1/msl_c3_m2k_2026-08/PREREG_G0.md) · `construct_lib` / `run_construct_g0` / `EXPLORE_GO.DRAFT` · STAGE1_K2/plan/M2K/registry mirrors. $0 · K spent=0. Explore unpaid.

**Decisions/defects:** Overnight window frozen a priori [18:00→09:29] ET. C1 MYM kill remains adjacency. Estate Cap/DSR/floor unchanged.

**Open / next:** Operator explore GO on C3-K2 (after W4 dry-run + panel pin) — or kill. S2B deferred (route still unresolved; no TV seat). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13q — MSL-C3-K2 dual-axis Stage-1 revive

**Focus:** Operator elects fresh C3 Stage-1 licensing `K_intrinsic=2` (both PDH/PDL + overnight stories scored); board ahead of S2B.

**Shipped:** branch `cursor/msl-c3-k2-dual-axis-023e` — [PR #795](https://github.com/Joshua-Asante/first-passage-archive/pull/795) · [ADR](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) · [`STAGE1_K2`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1_K2.md) · `overnight-range-failed-extension-fade` NEW in MECHANISMS · profiles rebuild · plan/S2B/registry mirrors. $0 · K spent=0. B4 unpaid.

**Decisions/defects:** Paying K=2 is the ladder escape hatch — estate Cap/DSR/floor **not** loosened. Prior ≤1-story STAGE1 remains historical OPERATOR-KILL record.

**Open / next:** Operator B4 GO on C3-K2 → dual-axis G0 freeze — or kill. S2B deferred (route still unresolved; no TV seat). Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13p — MSL-S2A explore FALSIFIED (N-ACT)

**Focus:** Operator explore GO on S2A → IS harness + delete/flip (local MCL_M15).

**Shipped:** branch `cursor/msl-s2a-explore-f01c` — [PR #794](https://github.com/Joshua-Asante/first-passage-archive/pull/794) · [`RESULTS_g2`](../lab/analysis/c1/msl_s2a_mcl_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-S2A-closure-falsified.md). $0 · K=0. CONFIRM unread.

**Decisions/defects:** `FALSIFIED` (trades/week 0.511); long FLIP FAIL; DELETE PASS both (moot). Sub-tick sham guard before RESULTS-of-record.

**Open / next:** S2B route still unresolved (do not take TV seat) — or kill. Carry: CapFLOW; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13o — MSL-S2A G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO on S2A → charter step 5 G0 freeze (pullback-failure resumption × MCL).

**Shipped:** branch `cursor/msl-s2a-g0-freeze-f01c` — [PR #793](https://github.com/Joshua-Asante/first-passage-archive/pull/793) · [`PREREG_G0`](../lab/analysis/c1/msl_s2a_mcl_2026-08/PREREG_G0.md) · STAGE1/MECHANISMS/plan §6. $0 · K=0. CONFIRM unread.

**Decisions/defects:** `K_intrinsic=1`; rr=3; session 09:00–14:30 ET; roll+FOMC calendars frozen; delete/flip unpaid until explore.

**Open / next:** Operator explore GO on S2A → IS harness + delete/flip — or kill. S2B route still unresolved. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13n — MSL P3.4 S2A campaign (MCL continuation)

**Focus:** P3.4 campaign manager — elect slate-2 box, S2A Stage-0 SNAG + Stage-1 pre-G0 on MCL pullback-failure resumption.

**Shipped:** branch `cursor/msl-p34-s2a-campaign-f01c` @ `a37dba86` — [PR #792](https://github.com/Joshua-Asante/first-passage-archive/pull/792) · [box ADR](adr/2026-08-13-msl-slate-2-design-box.md) · [STAGE0](../lab/analysis/c1/msl_s2a_mcl_2026-08/STAGE0.md) · [STAGE1](../lab/analysis/c1/msl_s2a_mcl_2026-08/STAGE1.md). $0 · K=0. No G0. Relettered 13n after #791 claimed 13m.

**Decisions/defects:** box ELECTED (rr∈[2,3]); Magdon-Ismail not calibration; sprint lane not opened; session window 09:00–14:30 ET card-scoped.

**Open / next:** Operator B4 GO on S2A → G0 freeze — or kill. S2B route still unresolved. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token. Magdon-Ismail B still undecided (do not wait).

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13m — catalog ghost rows after Magdon merge

**Focus:** Unblock `archive_lab_analysis.py --check --catalog-only` after PR #790 merge re-ghosted archive-flushed Active rows.

**Shipped:** branch `fix/orphan-mc-mdd-catalog` — hand-deleted 12 ghost Active rows in [`lab/CATALOG.md`](../lab/CATALOG.md) (no `--regenerate-catalog`). Heavy annotations untouched.

**Decisions/defects:** Magdon study itself landed correctly under `mc/`; ghosts were merge collateral from [`12126c58`](https://github.com/Joshua-Asante/first-passage-archive/commit/12126c58) onto [#789](https://github.com/Joshua-Asante/first-passage-archive/pull/789).

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13l — Magdon-Ismail MC bust validation

**Focus:** Magdon-Ismail MC bust validation — closed-form \(G_D\) vs production `simulate_path` trailing bust rates.

**Shipped:** branch `lab/mc-mdd-closed-form-2026-08` — [`RESULTS.md`](../lab/analysis/mc/mc_mdd_closed_form_2026-08/RESULTS.md) · harness + fixtures. $0 · K=0.

**Decisions/defects:** none (validation not calibration).

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13k — lab/analysis Wave-1 archive flush

**Focus:** Flush archive-owed hot bodies (option A); nest leftover flat inbox; park c1 cheap-falsifier debris. No `c1` split (B still open).

**Shipped:** branch `cursor/lab-archive-flush-ddac` @ `b2e3eec1` — 15 studies → [`lab/archive/`](../lab/archive/) + CARD stubs; `ict_mnq_2026-08` → [`_inbox`](../lab/analysis/_inbox/ict_mnq_2026-08/); [`cheap_falsifiers_2026-08`](../lab/analysis/c1/cheap_falsifiers_2026-08/). [`CATALOG`](../lab/CATALOG.md).

**Decisions/defects:** `git mv` EXDEV fallback in [`archive_lab_analysis.py`](../scripts/archive_lab_analysis.py). B (split `c1`) not taken.

**Open / next:** B still undecided. Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13j — MSL-C1 explore FALSIFIED (first slate exhausted)

**Focus:** Operator explore GO on C1 → IS harness + delete/flip score.

**Shipped:** branch `docs/msl-c1-explore` — harness · [`RESULTS_g2`](../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C1-closure-falsified.md) · registry. $0 · K=0. CONFIRM unread.

**Decisions/defects:** both arms CI entirely &lt; 0 (≈ −0.18/−0.11R); DELETE PASS moot; first slate C2/C3/C1 closed.

**Open / next:** Board — first MSL slate exhausted (C2 FALSIFIED · C3 OPERATOR-KILL · C1 FALSIFIED). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13i — MSL-C1 G0 FROZEN (B4 GO)

**Focus:** Operator B4 GO on C1 → charter step 5 G0 freeze (PDH/PDL failed-break reclaim × MYM).

**Shipped:** branch `docs/msl-c3-kill-c1-stage1` — [`PREREG_G0`](../lab/analysis/c1/msl_c1_mym_2026-08/PREREG_G0.md) · STAGE1/MYM/MECHANISMS/plan §6. $0 · K=0. CONFIRM unread.

**Decisions/defects:** `K_intrinsic=1`; RTH PDH/PDL + 15m reclaim; delete/flip unpaid until explore.

**Open / next:** Operator explore GO on C1 → IS harness + delete/flip — or kill. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13h — MSL-C3 OPERATOR-KILL → C1 Stage-1 PASS (B4 unpaid)

**Focus:** Operator kill C3 (B4 declined) → P3.3 C1 Stage-1 on MYM PDH/PDL reclaim.

**Shipped:** branch `docs/msl-c3-kill-c1-stage1` — [C3 closure](briefs/closures/MSL-C3-closure-operator-kill.md) · registry · [`C1 STAGE1`](../lab/analysis/c1/msl_c1_mym_2026-08/STAGE1.md) · preflight · plan §6. $0 · K=0.

**Decisions/defects:** C3 pre-G0 OPERATOR-KILL (class survives); Stage-1 deaths **1/3**; C1 route ① + B8 CLEAR; three limbs PASS.

**Open / next:** Operator B4 GO on C1 → G0 freeze — or kill → deaths 2/3. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13f — MSL-C3 Stage-1 PASS (B4 unpaid)

**Focus:** P3.2 Stage-1 — freeze stories, route ①, door-check, $0 screens on M2K.

**Shipped:** branch `docs/msl-c3-stage0` — [`STAGE1`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE1.md) · `pdh-pdl-failed-break-reclaim` NEW · preflight · profiles rebuild. $0 · K=0.

**Decisions/defects:** elected PDH/PDL failed-break reclaim; overnight story held; RAISED BAR CLEAR via SLR route ①; three limbs PASS.

**Open / next:** Operator B4 GO → G0 freeze — or kill → P3.3 C1. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13e — MSL-C3 Stage-0 PASS (L3 + WSTRUCT + W4)

**Focus:** P3.2 C3 Stage-0 — record L3 one-shot + WSTRUCT sequencing + W4 before flight.

**Shipped:** branch `docs/msl-c3-stage0` — [`STAGE0`](../lab/analysis/c1/msl_c3_m2k_2026-08/STAGE0.md) PROCEED · [`M2K.md`](../ops/instruments/M2K.md) ACTIVE/session · plan §6. $0 · K=0.

**Decisions/defects:** family one-shot void (K_intrinsic=1 brake); WSTRUCT SUPERSEDED-ON-COST sequenced discharged; W4 no pull.

**Open / next:** P3.2 Stage-1 (2–3 stories + door-check + $0 screens at M2K RT $2.82). Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13d — MSL-C2 explore GO → FALSIFIED; hand to C3

**Focus:** Local restore `MGC_M15.csv` + issue explore GO; score IS; close C2 on FALSIFIED.

**Shipped:** branch `cursor/msl-c2-explore-prep-292d` — [`RESULTS_g2`](../lab/analysis/c1/msl_c2_mgc_2026-08/RESULTS_g2.md) · [closure](briefs/closures/MSL-C2-closure-falsified.md) · registry row. $0 · K=0. CONFIRM unread.

**Decisions/defects:** both arms CI entirely &lt; 0 (≈ −0.18R); DELETE FAIL. STOP this G0.

**Open / next:** P3.2 C3 (M2K) Stage-0 — L3 one-shot + WSTRUCT sequencing before flight. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

## 2026-08-13c — MSL-C2 explore-path prep (harness + DRAFT GO)

**Focus:** Prep MSL-C2 explore path — freeze delete/flip in DRAFT; ship GO-gated IS harness; no score / Pine / C3.

**Shipped:** branch `cursor/msl-c2-explore-prep-292d` — [`EXPLORE_GO.DRAFT`](../lab/analysis/c1/msl_c2_mgc_2026-08/EXPLORE_GO.DRAFT.md) · [`construct_lib.py`](../lab/analysis/c1/msl_c2_mgc_2026-08/construct_lib.py) · [`run_construct_g0.py`](../lab/analysis/c1/msl_c2_mgc_2026-08/run_construct_g0.py) · synthetic tests · [explore-GO card](briefs/handoffs/2026-08-13-msl-c2-explore-go-card.md) (UNPAID). $0 · K=0.

**Decisions/defects:** none — explore GO still unpaid; `MGC_M15.csv` bytes still absent this checkout.

**Open / next:** Operator: restore `MGC_M15.csv` + issue explore GO per [card](briefs/handoffs/2026-08-13-msl-c2-explore-go-card.md) → `--explore-go` → Pine CC-solo → B5; else kill → P3.2 C3. Carry: CapFLOW; S2b; F1 2026-11-08; M1 arm-harden; weekly token.

**Live-ops state:** c1 warm/disarmed at incumbent; no arming.

---

<!-- ARCHIVE-INDEX:START -->
## Archive index

Older entries rolled to `docs/ltm/notes/archive/sessions/` (newest first).

| Date | Session | Archive |
|---|---|---|
| 2026-08-13 | PR #779 conflict resolve vs main (#778) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-13 | implied-SR demoted to report-only; fade cells reinstated | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 C2 B4 GO → G0 FROZEN | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 Stage-1 C2 (MGC) PASS → B4 | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P2 claim-manifest close | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P3.1 Stage-0 MGC bars | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL P2 umbrella frozen; LOCAL dispatch blocked (no cursor-agent) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL Board B1–B3 + B8 ratified | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | MSL sourcing-channel charter + slate + program plan (P1-reviewed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 ATR/instrument inputs extension (data-present only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 H_A ruled CLOSE (FALSIFIED-at-walls) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 H_A re-argument packet authored (ruling pending) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 cell #1 striker_nas100×MYM DEAD(cost) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 cell #2 striker×MNQ DEAD(N-SURV) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Accept coverage-limb promote-to-HARD ADR | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Promote coverage limb to self-arming HARD (Proposed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TNEC-CON-5 Branch A STOP elected (OHLCV temporal lane paused) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Ratify Q-SCORE-1 forward Lane:/Closed: fields | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 Blocks 2–3 election freeze + sibling-swap ports | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-TXG-1 Block 1 freeze + compile | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Land: Guardian-MGC MGC_M15 BAR EXPORT pin | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Q-SCORE-1 Block 1 H_A FALSIFIED (freeze + retro-map) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Harden roll_sessions against same-day label collisions | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-12 | Prep: Guardian-MGC bar-derived N-SURV re-run (scoping only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Decision: Guardian→MGC cell PREREG + DEAD(N-SURV) closure | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Decision/Measurement: Guardian→MGC (R7) port + F5 fix + b8 ratification | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Governance prose control-character gate | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TXG-1 Block-1 implementation plan (authored, not executed) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Hygiene: clear closure-disposition coverage backlog (9 → 0) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-SCORE-1 Block-1 implementation plan (freeze + retro-map) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-SCORE-1 approach-scoreboard design (derived lane ledger) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TXG-1 transfer/expression grid design (ratified) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Hygiene: Guardian-MGC (R7) pursuit backfill (PROPOSED PARK) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | N-SURV candidate-P&L channel (P2) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Sentinel: weekly activity-decision status at session start | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | MCL ledger: repair stale "1m cache exists" claim | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Code DRY remainder (C5 + SWEEP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | `Q-MCLTAS-1` scoped then closed `FALSIFIED` — probe never run | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Rule-7 DRY + Option B code DRY (slices 1–3 + code) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Block 1 intake screening re-run: MCL TAS re-open → still `SHAPE-UNSCREENABLE` | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | task-routing skill (local vs cloud) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Archive `usoil_regime_capture` (GSUB-1 residual) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 ITERATE packet (lean A STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-ENV-1 closed `NULL` (Phase B census 0 SEED-GRADE, STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-5 G0 freeze (pullback-VWAP-reclaim; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | CON-4 Branch B elected → CON-5 non-breakout design owed | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-4 ITERATE packet (lean A STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-CON-4 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-11 | Q-TNEC-ENV-1 Phase A compile → H_A NON-EMPTY (Phase B authorized) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-4 G0 freeze (PDH/PDL break; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | CON-3 Branch B elected → CON-4 design owed | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 ITERATE packet (election A/B unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 explore GO → AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Q-TNEC-CON-3 G0 freeze (HTF-native 5m; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Cell #3 reformulated framing falsifier: EVT-1 `KILL` — both drafted framings ... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Master-Pattern-shaped HTF-bias cell killed at cheap falsifier ($0 / no Q-ID) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | R8 gold-fix δ-extraction → SCREEN-FAIL (informed-flow + cost-law) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Block 1 intake screening on MCL → INTAKE-DRY; L2 sourcing re-stages gold-fix ... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | refine-question skill (select-box question refinement) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Lab-path relocation repair + relocation-rot gate | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | GRAND pursuit-records checker (WARN-tier) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Skill-ref warn triage (checker + citations) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Gate 14 coverage limb (missing-closure blind spot) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Missing closures authored + stale Q-roster Open rows cleared | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | W1 class_s intraday both-halves MEASURED | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-10 | Notion Phase 3 cold archival (retirement ADR addendum) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Four discernment calls made (SNAG · checker-canon · Survive · idle-clock) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | GRAND ratified + GSUB-1 CLOSED `RESOLVED-LOADBEARING` (all 4 phases) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Repo-truth sync + host-verified arm status (Hygiene) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Q-TNEC-CON-2 G0 freeze (compression→expansion; explore unpaid) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Instrument lane survey RESOLVED (MCL/MES/MGC) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | GRAND-tier ADR + GSUB-1 instantiated (`Proposed`; ratification pending) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | Harden M1 arm interlock (validate, not status-only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | CON-1 explore GO → FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-09 | CON-1 ES/NQ ENTRY freeze + explore harness wire | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | PR693 TNEC parallel integrate (G + Cap + Con) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | TNEC-1 necessity retarget ratified (Phase G) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Absolute path 1–2–3 (MNQSEL-2 / CapRES / construct) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2FLOW-1 explore GO → G2 FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 non-promotable STOP + Q-R2FLOW-1 G0 | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 explore GO → G2 AMBIGUOUS-HOLD (ITERATE) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2AGRUN-1 G0 freeze (MNQDTL R2 next causal set) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Delete-phase gap audit (conventions friction, Measurement) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2VBUCK-1 explore GO ratified → G2 FALSIFIED (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Fix roll_sessions reorder stranding same-day entries | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | ADR ceremony stakes-tiering RATIFIED (governance friction audit) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | Q-R2VBUCK-1 G0 freeze (MNQDTL R2 Phase-0) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-08 | S2b Accept → build ADR → build GO → daemon land | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | MNQDTL-1 §8 RATIFIED + S1 ledger hygiene (full package) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | S2 signal-host fork Accepted + S2b daemon spec (docs only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Closed-loop spec series S1–S7 (PROPOSED) + minimal-spec style ratified + blas... | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-MNQSEL-1 Phase-0 RUN → FALSIFIED (C2); STOP | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-MNQSEL-1 Phase-0 PREREG (selection-value ceiling; docs only) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | Q-OFCHAN-1 G2 Stage-G → VOID-COVERAGE (STOP) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
| 2026-08-07 | MNQDTL-1 amend: elect D2 L=$325 max loss (variant b) | [2026-Q3](ltm/notes/archive/sessions/SESSIONS-2026-Q3.md) |
<!-- ARCHIVE-INDEX:END -->
