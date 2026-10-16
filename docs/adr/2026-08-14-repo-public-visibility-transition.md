# Repo public-visibility transition via fresh-repo transplant — `repo-public-visibility-transition`

Filename: `docs/adr/2026-08-14-repo-public-visibility-transition.md`

**Status:** `Accepted` — operator 2026-08-22. Phase 1 remediation and the fresh-repo transplant already executed; this public clone is that seed. Status field lagged the executed work.
**Decision date:** 2026-08-14
**Supersedes:** `2026-07-01-guardian-pyport-public-tracking.md` in part — the
"repo is currently private; this posture is what ships if it is ever public again"
premise, and the §2.6 Forward question on LOCK.md/parameter-transcription
disclosure (now resolved: redact). The untracking decision itself (Python ports
gitignored + hash-pinned) stands unchanged and is not touched by this ADR.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): tier test, §0
read detail, §7 implementation plan, the §6 per-file downstream list and Verification detail removed; an
*As executed* record added under §2.
No decision text changed. Pre-trim text at blob `fe8d9193cb94794d6b24f6c75210785caf3f54ca`
(commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).

---

## §0 — Rule 0 reads (production-source verification)

- Read 2026-08-14 at authoring: `.gitignore` (`9d86268`), `core/firm_rules.py` and
  `core/dd_protection.py` (`0356be2`), `docs/adr/2026-07-01-guardian-pyport-public-tracking.md`
  (`5563cf4`), `core/strategies/_archive/guardian/LOCK.md` (`85156a0`, pre-redaction),
  `.github/workflows/tests.yml` (`c9ae0e7`) and `gh pr view 831`. Findings per file are at the pre-trim
  blob above; literal account and parameter values were never reproduced in this file.

---

## §1 — Context

CI cost pressure (private-repo Actions billing, projected $200–300/mo at current ship rates)
prompted a review of whether to flip this repo public. [PR #831](https://github.com/Joshua-Asante/first-passage-archive/pull/831)
independently cuts that cost ~3x by removing a `push`+`pull_request` dual-trigger and narrowing
the pylint matrix, but does not touch the underlying billing-gate block (no payment method on
file) and does not eliminate the cost — it only reduces it while staying private.

The operator has separately decided to go public for visibility, cost elimination (public repos
get free/unlimited standard-runner Actions minutes), and simplified Cursor/CC workflow (one repo
target, no billing gate to manage). That decision is a precondition of this ADR, not its subject.
What this ADR decides is **how** to go public given what a read-only exposure audit found: the
live Tradeify/Tradovate account identifier and real dollar P&L are hardcoded (not gitignored)
across 7 tracked files plus 14 historical commits (6 of which carry the identifier in the commit
message itself, dating to `3b19c1e`, 2026-07-19); 6 tracked `LOCK.md`-family files disclose full
locked-strategy entry/exit parameters and real backtest performance figures; there is no LICENSE;
and a stray Python reimplementation of Guardian's signal logic
(`lab/archive/oanda_stage1/guardian_stage1.py`) is tracked despite the standing policy (from the
2026-07-01 ADR this partially supersedes) that executable strategy ports land gitignored by
default.

**Decision driver (one sentence):** The operator's public-visibility decision is made; this ADR
exists because executing it naively (flip the visibility bit on the current repo) would
permanently publish 1,582 commits' worth of account/balance history and leave the 2026-07-01
ADR's unresolved LOCK.md disclosure question answered by default rather than by decision.

---

## §2 — Decision

**Decision:** Go public via a **fresh-repo transplant**, not an in-place visibility flip. Perform
a bounded remediation pass on this (currently private) repo's current tracked state — scrub the
live account identifier and dollar balances, redact the LOCK.md-family parameter/backtest blocks
to name/version/lock-date/risk%/hash-only, untrack the stray Python port, add an all-rights-reserved
LICENSE — land it as a normal reviewed PR, then seed a **new, separate public GitHub repository**
from that post-remediation tree as a single "initial public release" commit (no inherited history).
This repo (`first-passage`) is archived immediately after — kept private forever, full history
intact, as the permanent retrievable record (same pattern as the existing Great Prune convention:
nothing is destroyed, it is moved out of the actively-developed/public surface).

**Effective:** immediately upon acceptance (Phase 1 remediation may begin without further sign-off;
Phase 3+ — creating the new repo, pushing, and any visibility/archive changes — requires a separate
explicit operator go per the standing "publishing external content" guardrail, checked at that
step regardless of this ADR's status).

**Scope:** applies to the one-time public-visibility transition. Does not change ongoing gitignore
policy beyond adding the one missing pattern (§6), does not touch Pine, `dd_protection` constants,
or allocations, and does not reopen the 2026-07-01 ADR's untracking decision (which stands).

**As executed (recorded 2026-10-15).** Phase 1 remediation landed; the public repo was seeded as one
"Initial public release" commit `027a7295` (2026-08-14) with `LICENSE` and without `docs/notes/**`,
`docs/ltm/**` and `docs/superpowers/**`. It is a separate GitHub resource that took the `first-passage`
name; the original private repository continues as `first-passage-archive`. That repository was
GitHub-archived (read-only) after the transplant and was later un-archived (date not recorded; first
recorded write: the 2026-09-06 preservation branch of
[`2026-09-06-tracked-file-reduction-prune.md`](2026-09-06-tracked-file-reduction-prune.md)). It is now
the private, writable evidence store of [M-41](../methodology/lessons/methodology_lessons.md)
(`scripts/evidence_archive.py`). Private visibility and retained full history are unchanged. Open for the
operator: whether the name reuse (§5 fourth bullet) and the non-archived state are ratified as executed.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Stay private, rely on PR #831's ~$50–85/mo post-diet cost | Doesn't achieve the operator's stated visibility goal; CI stays gated behind adding a payment method regardless. |
| Self-hosted Actions runner (own hardware/VPS), stay private | Solves cost with zero exposure tradeoff, but doesn't achieve the visibility goal and adds maintenance overhead that runs counter to "simpler Cursor/CC workflow" — the stated motivation for going public over this option. |
| In-place visibility flip, no remediation | Rejected on the exposure audit alone — publishes the live account ID, real P&L, full strategy parameters, and backtest results with zero scrubbing. |
| In-place `git filter-repo` history rewrite, single repo going forward | Real scope measured 2026-08-14: 1,582 commits get new hashes (from `3b19c1e` to `origin/main`), invalidating the Rule-0 hash-anchor citations in 173 ADR-authoring commits; requires a force-push. Superseded by the fresh-repo transplant, which achieves the same clean-history outcome with zero rewrite risk. |
| Keep LOCK.md disclosure as-is (raw Pine stays gitignored, parameters/results don't) | This is the 2026-07-01 ADR's own deferred framing; operator resolved it here toward redaction rather than accepting the fuller disclosure. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** (a) any dated incident within 90 days of the public flip where public
visibility is causally implicated in unauthorized access, scraping-and-reuse of the (even
redacted) locked-strategy parameters, or a security/safety incident touching the c1 rail; **or**
(b) GitHub Actions overage is still >$0/mo 30 days after the flip (indicates the new repo, not
just PR 831, isn't actually what's live).

**Revert action:** flip the new repo back to private immediately (a reversible operation, unlike
anything touching this repo's history); author a superseding ADR documenting the incident and any
further remediation needed.

**Trigger check schedule:** 30-day and 90-day checkpoints after the flip date; ongoing informal
monitoring in between.

---

## §5 — Forbidden moves (under this ADR)

- **Rewriting this repo's git history in place (`git filter-repo`, force-push).** Genuinely the
  first option chosen before the 1,582-commit / 173-ADR blast radius was measured — ruled out once
  sized, superseded by the fresh-repo transplant. Do not revisit without a new ADR justifying why
  the transplant approach has become insufficient.
- **Partial LOCK.md redaction** (e.g., dropping only the dollar P&L but keeping PF/WR/session
  windows). The operator's decision was full parameter-block + backtest-results removal down to
  name/version/lock-date/risk%/hash; a softer redaction wasn't the option chosen and defeats the
  purpose of resolving the 2026-07-01 ADR's Forward question decisively.
- **Deferring the LICENSE file to a follow-up.** Ships with the public repo's first commit, not
  added later — an unlicensed public repo of live trading strategies is not the intended posture
  for even a single day.
- **Reusing this repo's existing remote/name for the new public repo** (rename-in-place, transfer,
  or toggling `isPrivate` on the current repo). That is the in-place approach this ADR rejects; the
  new repo must be a genuinely separate GitHub resource seeded from a clean tree.

---

## §6 — Consequences

**Positive consequences:**
- GitHub Actions cost → $0/mo on standard runners (vs. ~$50–85/mo post-PR-831, ~$160–290/mo
  pre-diet), with no OS-multiplier exposure since all jobs are `ubuntu-latest`.
- Achieves the operator's stated visibility goal without publishing the live account
  identifier, real P&L, or full strategy parameter/backtest detail.
- This repo becomes a clean, permanently-retrievable private archive — no information is
  destroyed, only moved out of the public/actively-developed surface, consistent with the
  existing Great Prune retrievability convention.
- Resolves the 2026-07-01 ADR's open §2.6 Forward question by decision rather than by default.

**Negative consequences (real cost, not theatrical):**
- One-time remediation cost: ~16 files to scrub (account ID/balance), 6 LOCK.md-family files to
  redact, one file to untrack, one LICENSE to author.
- The new public repo starts with a single "initial public release" commit — it does not carry
  this repo's actual development history or ADR provenance forward; anyone reading the public repo
  sees only the post-transplant state, not the reasoning trail behind it (the trail stays in the
  private archive).
- `core/firm_rules.py:583`'s `_BASE_RISK` constants remain in tracked source in the new repo
  (they're load-bearing for live sizing, not something that can be redacted without breaking the
  code) — an accepted residual disclosure of risk% only, matching what the redacted LOCK.md files
  also retain per the redaction decision.
- Going forward, any accidental commit of sensitive operational detail (a real risk given this
  project's dense `RUNBOOK.md`-style live-narration habit) becomes instantly and permanently public
  in the new repo — no more benefit of a private-repo safety net.

**Risks (probabilistic, distinct from costs):**
- Redacted LOCK.md still discloses risk% and session-structure vocabulary elsewhere in tracked
  docs (methodology files, ADRs describing session windows in prose); a sufficiently motivated
  reader could partially reconstruct strategy behavior from the union of public artifacts. Residual,
  accepted — mitigation is out of scope for this ADR (would require a much broader doc-vocabulary
  sweep with its own cost/benefit call).

**Curation and redaction rules (executed with Phase 1; the per-file disposition list is at the pre-trim
blob):**

- *Curation rule:* `docs/notes/**`, `docs/ltm/**` and `docs/superpowers/**` are internal working-memory /
  ops-log directories with no standalone public-documentation value. Rather than line-scrub dense
  operational logs, they were **excluded from the public seed wholesale** and stay only in the private
  archive. Named members of that exclusion include `docs/notes/rail_build/RUNBOOK.md`,
  `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`,
  `docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-28.md`,
  `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md`, the audit notes, and
  `lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md`.
- *LOCK-family redaction:* `core/strategies/_archive/{guardian,striker,aegis,nas}/LOCK.md` reduced to
  name / version / lock-date / risk% / hash; the two `*_FUTURES_LOCK.md` venue-delta files lack that
  structure and were left unchanged.
- *Untracked:* `lab/archive/oanda_stage1/{guardian,aegis,striker}_stage1.py` (`git rm --cached` +
  `.gitignore`); generic infra in the same directory stays tracked (the 2026-07-01 ADR's infra-vs-edge
  split).
- `core/firm_rules.py` `_BASE_RISK` — **ruled unaffected, explicit reason**: load-bearing runtime values,
  not disclosure-only text; accepted under the negative consequences above.
- `LICENSE` — all-rights-reserved, shipped in the first public commit.

---

## §10 — Audit hooks (runnable)

```bash
# Account ID / accountId / balance sweep — expect ZERO hits after Phase 1, outside the
# EXCLUDE-FROM-SEED directories (docs/notes/**, docs/ltm/**, docs/superpowers/**), which
# are permitted to still carry it since they never enter the public repo. The literal
# account ID / accountId / dollar figures are deliberately NOT reproduced in this ADR
# (this file itself ships in the public seed) — pull the literal values from the private
# operational archive (CLAUDE.md pre-2026-08-14, or STATE.md history) before running:
git grep -n "$ACCOUNT_ID" -- . | grep -v '^docs/notes/\|^docs/ltm/\|^docs/superpowers/'
git grep -n "$ACCOUNT_NUMERIC_ID" -- . | grep -v '^docs/notes/\|^docs/ltm/\|^docs/superpowers/'
git grep -nF -e "$BALANCE_1" -e "$BALANCE_2" -e "$FILL_1" -e "$FILL_2" -e "$FILL_3" -- . | grep -v '^docs/notes/\|^docs/ltm/\|^docs/superpowers/'

# LOCK.md redaction check — expect the "## Locked config" and "## Reference backtest" headers GONE post-Phase-1:
grep -rln "## Locked config" core/strategies/_archive/
grep -rln "## Reference backtest" core/strategies/_archive/

# Untracked-port check — expect this to print nothing (file removed from index):
git ls-files | grep oanda_stage1

# LICENSE presence:
git ls-files | grep -iE '^LICENSE'

# §4 trigger check — 30-day / 90-day post-flip
# (manual: any incident report referencing public visibility + exposure; Actions billing dashboard $0 check)
```

---

## Verification

```bash
$ python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-14-repo-public-visibility-transition.md --type adr
$ python scripts/check_adr_graph.py
```

---

## Addendum 2026-09-11 — PR-number era convention

**Does not amend §2 / §4 / §5.** Records a consequence of §2's fresh-repo transplant that the
ADR did not name, and fixes the citation convention going forward. No retro-edit of any dated
artifact.

**Reads (2026-09-11, origin/main `2449cfc`):** `gh pr list --state all --limit 1` → highest live
PR is #344. `git log --all --oneline --grep="Merge pull request #308"` → two merges: `1316290`
(Databento research stack, 2026-07-11, archive-era numbering) and `32b31d5` (Select-campaign
consolidation, 2026-09-05, live numbering). `git grep -c -E "PR #[0-9]+"` over tracked
`*.md|*.py|*.yml|*.jsonl` → 699 references in 199 files, 519 of them with a number in the
collision range 1–344; 47 references already use the full `first-passage-archive` pull URL, 91
the live pull URL, none the `owner/repo#N` form. First observed misresolution: the 2026-09-11
memory-consolidation pass found a memory citing "PR #308 merged 2026-07-11" that resolves on
GitHub to the 2026-09-05 PR.

**The consequence.** The public repo was seeded fresh on 2026-08-15 (§2), so its pull-request
numbers restarted at #1. Every PR number cited in an artifact dated before 2026-08-15 belongs to
`first-passage-archive`, and the range in which an unqualified number is ambiguous grows by one
with every live PR.

**Convention (forward-only).**
1. An archive-era PR is cited as the plain-text identifier `first-passage-archive#N` or by
   its full archive pull URL. A bare `PR #N` is never used for one from here on.
   For clickable citations in repository Markdown, use an explicit Markdown link to the
   pull URL. In GitHub discussions, cross-repository autolinks require the owner-qualified
   form `Joshua-Asante/first-passage-archive#N` (without code formatting); the short
   identifier does not auto-link. GitHub does not create these autolinks in repository
   files. Source: [GitHub autolink documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls),
   verified 2026-09-11. The same distinction applies to live-repository citations.
2. A live PR may be cited bare only inside an artifact whose own date is on or after 2026-08-15
   and that cites no archive-era PR. Documents that mix eras — `docs/SESSIONS.md`, `STATE.md`,
   `docs/operational_rules.md`, `CLAUDE.md`, session memory — use `first-passage#N`.
3. An ambiguous historical number is resolved by merge commit or branch name, never by number.
4. Existing references in dated artifacts stay as written (Rule 14 class 1: frozen bodies are
   not edited; the date disambiguates). The reader-intercept is the paragraph in the
   `docs/SESSIONS.md` living header, which is the document that mixes eras most (80 references).

**Boundary.** No gate is added. A report-only audit check under `make audit` (flag an
unqualified number in the collision range inside an era-mixing living document) is owed only if
a second documented misresolution occurs; record it against this addendum.

**Audit hooks (runnable; none matches this addendum's own text).**

```bash
# Collision witness — expect exactly 2 lines, one per era
git log --all --oneline --grep="Merge pull request #308"
# Reader-intercept present in the SESSIONS living header — expect 1
grep -c "^\*\*PR numbers are era-scoped" docs/SESSIONS.md
# Convention uptake — baseline 0 on 2026-09-11; expect growth, never regression to 0 once used
git grep -c -E "first-passage(-archive)?#[0-9]+" -- 'docs/*.md' 'STATE.md' | awk -F: '{s+=$2} END {print s+0}'
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Initial authoring | Joshua + claude.ai |
| 2026-08-22 | **Operator Accept.** Status `Proposed` → `Accepted`. Phase 1 remediation and the fresh-repo transplant already executed; this public clone is that seed. Status field lagged the executed work. | Joshua (Accept) + Cursor (record) |
| 2026-09-11 | **Addendum — PR-number era convention.** Numbers restarted at #1 with the §2 transplant; citation rule (`first-passage-archive#N` / `first-passage#N`), no retro-edits, reader-intercept in the `docs/SESSIONS.md` living header. Does not amend §2 / §4 / §5. | Joshua (request) + Claude Code (record) |
| 2026-10-15 | Retention trim: tier test, §0 detail, §7 plan, §6 per-file list and Verification detail removed (pre-trim blob `fe8d9193cb94794d6b24f6c75210785caf3f54ca`); *As executed* record added under §2. No decision change. | Joshua (direction) + Claude Code |
