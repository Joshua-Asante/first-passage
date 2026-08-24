# Sentinel proposal queue

_Reverse-chron. Report-only; the operator authorizes every item (Action = do it, Forward = schedule it, Closed = log it)._

<!-- runs:newest-first -->

## Run 2026-08-24

weekly activity decision [2026-08-24->08-28]: NOT RECORDED (5 business days left) — operator call, see STATE row 0

### Action
- **PREREG-RUNEDIT-3c7ca2f** [prereg] — Commit 3c7ca2f introduces results/closure `docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md` and also edits the pre-existing pre-registration `docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md` beyond its status header — the run commit must not move frozen verdict logic (Rule 8.7).
  - source: `docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md`
  - next: Diff the prereg against its freeze commit (`git log --diff-filter=A -- <prereg>`, then `git diff <freeze> <run> -- <prereg>`) and confirm no gate, threshold, or verdict rule moved. A closure `**Status:**` stamp alone is exempt and never reaches here. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-RUNEDIT-414e537** [prereg] — Commit 414e537 introduces results/closure `lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md` and also edits the pre-existing pre-registration `docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md` beyond its status header — the run commit must not move frozen verdict logic (Rule 8.7).
  - source: `lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md`
  - next: Diff the prereg against its freeze commit (`git log --diff-filter=A -- <prereg>`, then `git diff <freeze> <run> -- <prereg>`) and confirm no gate, threshold, or verdict rule moved. A closure `**Status:**` stamp alone is exempt and never reaches here. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-RUNEDIT-d0dcdad** [prereg] — Commit d0dcdad introduces results/closure `docs/briefs/closures/Q-NSURV-2-closure-resolved.md` and also edits the pre-existing pre-registration `docs/briefs/pre-registration/Q-NSURV-2-verdict-preregistration.md` (+1 more pair(s)) beyond its status header — the run commit must not move frozen verdict logic (Rule 8.7).
  - source: `docs/briefs/closures/Q-NSURV-2-closure-resolved.md`
  - next: Diff the prereg against its freeze commit (`git log --diff-filter=A -- <prereg>`, then `git diff <freeze> <run> -- <prereg>`) and confirm no gate, threshold, or verdict rule moved. A closure `**Status:**` stamp alone is exempt and never reaches here. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-13c0915** [prereg] — Commit 13c0915 introduces results/closure `docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md` together with its pre-registration `docs/briefs/pre-registration/Q-TRAINKILL-1-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-1632de9** [prereg] — Commit 1632de9 introduces results/closure `docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md` together with its pre-registration `docs/briefs/pre-registration/Q-CONDVAL-1-verdict-preregistration.md` (+1 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-1e17bcc** [prereg] — Commit 1e17bcc introduces results/closure `docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md` together with its pre-registration `docs/briefs/pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md` (+1 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-1e40b11** [prereg] — Commit 1e40b11 introduces results/closure `lab/archive/dstruct_mnq_2026-08/RESULTS_DSTRUCT.md` together with its pre-registration `lab/archive/dstruct_mnq_2026-08/PREREG_DSTRUCT.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/archive/dstruct_mnq_2026-08/RESULTS_DSTRUCT.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-3e351fc** [prereg] — Commit 3e351fc introduces results/closure `lab/analysis/c1/mnqtape1_power_check_2026-08-23/RESULTS.md` together with its pre-registration `docs/briefs/pre-registration/2026-08-22-mnq-tape-imbalance-prereg.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/analysis/c1/mnqtape1_power_check_2026-08-23/RESULTS.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-4062562** [prereg] — Commit 4062562 introduces results/closure `lab/analysis/_inbox/dstruct_mnq_2026-08/RESULTS_DSTRUCT.md` together with its pre-registration `lab/analysis/_inbox/dstruct_mnq_2026-08/PREREG_DSTRUCT.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/analysis/_inbox/dstruct_mnq_2026-08/RESULTS_DSTRUCT.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-50396fc** [prereg] — Commit 50396fc introduces results/closure `docs/briefs/closures/Q-CALLBOUND-1-closure-ambiguous-hold.md` together with its pre-registration `docs/briefs/pre-registration/Q-CALLBOUND-1-verdict-preregistration.md` (+9 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-CALLBOUND-1-closure-ambiguous-hold.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-8c208ec** [prereg] — Commit 8c208ec introduces results/closure `lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md` together with its pre-registration `lab/analysis/_inbox/rangestate_mcl_2026-08/PREREG_S1B.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/analysis/_inbox/rangestate_mcl_2026-08/RESULTS_S1B.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-8d2195c** [prereg] — Commit 8d2195c introduces results/closure `docs/briefs/closures/Q-MONSURF-1-closure-resolved.md` together with its pre-registration `docs/briefs/pre-registration/Q-MONSURF-1-verdict-preregistration.md` (+1 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-MONSURF-1-closure-resolved.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-96eaf09** [prereg] — Commit 96eaf09 introduces results/closure `docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md` together with its pre-registration `docs/briefs/pre-registration/Q-GATESTACK-1-verdict-preregistration.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-ab303d0** [prereg] — Commit ab303d0 introduces results/closure `docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md` together with its pre-registration `docs/briefs/pre-registration/Q-BUSTGATE-2-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-afa0d56** [prereg] — Commit afa0d56 introduces results/closure `docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md` together with its pre-registration `docs/briefs/pre-registration/Q-TRADECAP-1-verdict-preregistration.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-b8b54d6** [prereg] — Commit b8b54d6 introduces results/closure `lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md` together with its pre-registration `lab/analysis/_inbox/rangestate_gc_2026-08/PREREG_S1A.md` — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/analysis/_inbox/rangestate_gc_2026-08/RESULTS_S1A.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-be694ca** [prereg] — Commit be694ca introduces results/closure `docs/briefs/closures/Q-TRAINKILL-2-closure-ambiguous-hold.md` together with its pre-registration `docs/briefs/pre-registration/Q-TRAINKILL-2-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-TRAINKILL-2-closure-ambiguous-hold.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-dd2cc67** [prereg] — Commit dd2cc67 introduces results/closure `docs/briefs/closures/Q-EXPR-1-closure-resolved.md` together with its pre-registration `docs/briefs/pre-registration/Q-EXPR-1-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-EXPR-1-closure-resolved.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-f200c05** [prereg] — Commit f200c05 introduces results/closure `docs/briefs/closures/Q-TRAINKILL-3-closure-ambiguous-hold.md` together with its pre-registration `docs/briefs/pre-registration/Q-TRAINKILL-3-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-TRAINKILL-3-closure-ambiguous-hold.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-f2cbb7b** [prereg] — Commit f2cbb7b introduces results/closure `lab/archive/ict_target_investigation_2026-08-20/RESULTS.md` together with its pre-registration `lab/archive/mnq_capflow_orb_r_2026-08/PREREG.md` (+8 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `lab/archive/ict_target_investigation_2026-08-20/RESULTS.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.

### Forward
- **OBLIG-adr-triggers-2026-09-21** [obligation] — 1 ADR 'Trigger check schedule' field(s) name 2026-09-21 (28d out): docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md
  - source: `docs/adr/ (1 file(s))`
  - next: rg -l "2026-09-21" docs/adr/*.md — cross-check against STATE.md's ### 2026-09-21 section (see PRECOND-board-sync findings if any).
- **OBLIG-adr-triggers-2026-10-20** [obligation] — 2 ADR 'Trigger check schedule' field(s) name 2026-10-20 (57d out): docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md, docs/adr/2026-08-05-blusky-inactivity-unsourced-encoding.md
  - source: `docs/adr/ (2 file(s))`
  - next: rg -l "2026-10-20" docs/adr/*.md — cross-check against STATE.md's ### 2026-10-20 section (see PRECOND-board-sync findings if any).
- **PRECOND-board-sync-2026-10-20** [precondition] — 2 ADR trigger-schedule field(s) name 2026-10-20 (57d out); STATE.md (no ### 2026-10-20 heading) references only 0 of them.
  - source: `STATE.md`
  - next: rg -l "2026-10-20" docs/adr/*.md, then add a STATE.md pointer row for any still-live (undischarged) obligation under ### 2026-10-20. A gap can also mean the obligation was already discharged elsewhere — verify before adding a row.
- **SESSIONS-over-window** [hygiene] — docs/SESSIONS.md has 34 entries (> 20 live-window); older entries should roll to docs/ltm/notes/archive/sessions/.
  - source: `docs/SESSIONS.md`
  - next: Run `python scripts/roll_sessions.py` to archive entries beyond the newest 20, then commit the SESSIONS.md + archive delta.

## Run 2026-08-17

weekly activity decision [2026-08-17→08-21]: NOT RECORDED (5 business days left) — operator call, see STATE row 0

### Action
- **PREREG-RUNEDIT-3c7ca2f** [prereg] — Commit 3c7ca2f introduces results/closure `docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md` and also edits the pre-existing pre-registration `docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md` beyond its status header — the run commit must not move frozen verdict logic (Rule 8.7).
  - source: `docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md`
  - next: Diff the prereg against its freeze commit (`git log --diff-filter=A -- <prereg>`, then `git diff <freeze> <run> -- <prereg>`) and confirm no gate, threshold, or verdict rule moved. A closure `**Status:**` stamp alone is exempt and never reaches here. See docs/operational_rules.md Rule 8 sub-rule 7.
- **PREREG-SAMECOMMIT-ab303d0** [prereg] — Commit ab303d0 introduces results/closure `docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md` together with its pre-registration `docs/briefs/pre-registration/Q-BUSTGATE-2-verdict-preregistration.md` (+2 more pair(s)) — the freeze is self-attested, not git-verifiable (Rule 8.7: prereg must be a separate, earlier commit).
  - source: `docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md`
  - next: Freeze the pre-registration in a separate, EARLIER commit than its results (gold standard: 46f47d1 freeze -> 913829b run). For already-merged history, log it Closed; catch the next one pre-merge by splitting the freeze commit out. See docs/operational_rules.md Rule 8 sub-rule 7.

### Forward
- **SESSIONS-over-window** [hygiene] — docs/SESSIONS.md has 73 entries (> 20 live-window); older entries should roll to docs/ltm/notes/archive/sessions/.
  - source: `docs/SESSIONS.md`
  - next: Run `python scripts/roll_sessions.py` to archive entries beyond the newest 20, then commit the SESSIONS.md + archive delta.

