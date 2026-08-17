# Sentinel proposal queue

_Reverse-chron. Report-only; the operator authorizes every item (Action = do it, Forward = schedule it, Closed = log it)._

<!-- runs:newest-first -->

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

