# Repo public-visibility transition via fresh-repo transplant — `repo-public-visibility-transition`

Filename: `docs/adr/2026-08-14-repo-public-visibility-transition.md`

**Status:** `Proposed` — mechanical remediation (§7 Phase 1) not yet landed; flips to
`Accepted` once Phase 1 merges and the §10 verification sweep returns clean
**Decision date:** 2026-08-14
**Supersedes:** `2026-07-01-guardian-pyport-public-tracking.md` in part — the
"repo is currently private; this posture is what ships if it is ever public again"
premise, and the §2.6 Forward question on LOCK.md/parameter-transcription
disclosure (now resolved: redact). The untracking decision itself (Python ports
gitignored + hash-pinned) stands unchanged and is not touched by this ADR.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

---

## Tier test — full ceremony or light record?

FULL ceremony applies. Two limbs fire: **limb 2** (touches a live-risk-adjacent
surface — the live prop-firm account identifier and realized P&L history, and the
`firm_rules`/`LOCK.md` disclosure of live risk-sizing parameters) and **limb 4**
(amends doctrine — supersedes the "repo is currently private" premise stated as
standing posture in `CLAUDE.md` §Public-clone-posture and decided in
[`2026-07-01-guardian-pyport-public-tracking.md`](2026-07-01-guardian-pyport-public-tracking.md)).

---

## §0 — Rule 0 reads (production-source verification)

- `.gitignore` — anchor: `9d86268` (verified `git log -1 -- .gitignore` on 2026-08-14; confirms
  `**/*.pine`, vendor CSVs, and the two named Guardian Python-port files are excluded, but
  `lab/archive/oanda_stage1/guardian_stage1.py` is NOT covered by any existing pattern)
- `core/firm_rules.py` — anchor: `0356be2` (verified `git log -1 -- core/firm_rules.py` on
  2026-08-14; `_BASE_RISK` at line 583 — `{"guardian": 0.0034, "striker": 0.0070, "aegis": 0.0150,
  "striker_nas100": 0.0037}` — tracked in source, matches `CLAUDE.md`'s Strategy Reference table)
- `core/dd_protection.py` — anchor: `0356be2` (same commit; no account/balance content, unaffected)
- `docs/adr/2026-07-01-guardian-pyport-public-tracking.md` — anchor: `5563cf4` (verified
  `git log -1` on 2026-08-14; §2.6 explicitly forwarded the LOCK.md-disclosure question as
  unresolved, and a same-day addendum found the repo was gh-verified private since 2026-06-06,
  contrary to that ADR's own premise)
- `core/strategies/_archive/guardian/LOCK.md` — anchor: `85156a0` (verified `git log -1` on
  2026-08-14, pre-redaction; confirmed the "Locked config" block transcribed full entry/exit
  parameters — SL/TP/ATR multipliers, hold/day-count limits, session window, hour-blocks — and
  "Reference backtest" published trade count, net P&L, PF, WR, and max DD figures. Literal values
  are not reproduced here (this file ships in the public seed) — the private archive at this
  commit is the record. The other 3 core LOCK.md files shared this two-block structure and were
  redacted identically; the 2 `FUTURES_LOCK.md` venue-delta files do not have this structure and
  were left unchanged, per §6)
- `.github/workflows/tests.yml` — anchor: `c9ae0e7` (verified `git log -1` on 2026-08-14; all jobs
  across all 4 workflow files run `ubuntu-latest` only — confirms the cost driver is
  job-count×trigger-frequency, not an OS-runner multiplier)
- `gh pr view 831` — checked live 2026-08-14: state `OPEN`, checks failing on the billing-gate
  annotation (root cause per operator: no payment method was ever added to the GitHub account,
  which produces GitHub's generic "recent account payments have failed or your spending limit
  needs to be increased" message)

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

**Downstream artifacts that need updating (§6 list — DERIVED, see §10 raw sweep output; every hit dispositioned):**

*Curation rule (revised from a pure line-scrub during implementation):* `docs/notes/**`,
`docs/ltm/**`, and `docs/superpowers/**` are internal working-memory/ops-log directories with no
standalone public-documentation value (`docs/ltm/` is explicitly cold long-term-memory archive
already). Rather than line-scrub dense multi-paragraph operational logs (`RUNBOOK.md`,
`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`, the session archive, audit notes, etc.) with the
attendant risk of an incomplete redaction, these three directories are **excluded from the new
repo's Phase-3 seed tree wholesale** — unmodified, unscrubbed, staying only in this (archived,
private-forever) repo. This is a curation default, easy to revisit before Phase 3 actually runs.

- `CLAUDE.md` — rewrite §Public-clone-posture entirely (repo is now public via the new repo; this
  file's account-ID/balance line at L41 scrubbed) — **EDIT**
- `STATE.md:144` — scrub account ID — **EDIT**
- `docs/adr/2026-08-05-strategy-venue-binding-axis.md:78` — scrub account ID from example — **EDIT**
- `deploy/c1_rail/README.md` — scrub balance figure — **EDIT** (kept in-scope for public: genuine
  deployment documentation, not an ops log)
- `tests/ops/test_c1_rail_arm.py:125` — replace real account ID with a fake test fixture value —
  **EDIT** (good practice regardless of visibility)
- `docs/notes/2026-08-09-repo-truth-sync-fix-queue.md:28`,
  `docs/notes/rail_build/RUNBOOK.md`, `docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`,
  `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md`,
  `docs/notes/2026-07-29-comparative-advantage-thesis.md`,
  `docs/notes/audits/2026-08-11-rule7-dry-fact-audit.md`,
  `docs/notes/audits/programme-audit/2026-08-05-claim-alignment/03-agent-facing.md`,
  `docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-28.md`,
  `docs/superpowers/plans/2026-08-02-cadence-inactivity-support-research.md`,
  `docs/superpowers/specs/2026-08-02-idle-rule-disposition-options.md`,
  `lab/analysis/c1/c1_cadence_inactivity_2026-08-02/RESULTS.md` — **EXCLUDE FROM SEED** (curation
  rule above; unmodified in this repo)
- `core/strategies/_archive/{guardian,striker,aegis,nas}/LOCK.md`,
  `core/strategies/_archive/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md`,
  `core/strategies/_archive/striker/striker_dj30_v4.5_mym_FUTURES_LOCK.md` — redact
  parameter/backtest blocks to name/version/lock-date/risk%/hash — **EDIT**
- `core/firm_rules.py:583` — **RULED UNAFFECTED, explicit reason**: `_BASE_RISK` constants are
  load-bearing runtime values, not disclosure-only text; accepted per §6 negative consequences
- `lab/archive/oanda_stage1/{guardian,aegis,striker}_stage1.py` — **UNTRACK** (`git rm --cached` +
  `.gitignore` pattern addition). Widened during implementation: the original exposure audit named
  only `guardian_stage1.py`, but `aegis_stage1.py` and `striker_stage1.py` are the same class —
  frozen historical missed-alpha analysis scripts that embed real filter/pyramid parameters
  (EOM block days, hour-blocks, ATR-expansion thresholds, pyramid trigger/size). `bar_loader.py`,
  `permutation.py`, `pine_indicators.py`, `post_exit_excursion.py`, `__init__.py`, `RESULTS.md` in
  the same directory stay tracked — generic statistical/data-loading infra and a disposition
  marker, not strategy-signal logic (same infra-vs-edge split as the 2026-07-01 ADR's
  `next_open_engine.py` precedent).
- `LICENSE` — **NEW FILE**, all-rights-reserved notice
- `docs/adr/2026-07-01-guardian-pyport-public-tracking.md` — addendum noting partial supersession
  by this ADR (premise + §2.6 Forward question) — **EDIT** (addendum only, not a rewrite — see
  Change history discipline)
- `docs/adr/INDEX.md` — regenerate — **EDIT**
- New GitHub repository (separate resource, not a repo path) — create, seed, configure branch
  protection — **NEW**
- Cursor background-agent repo target — operational follow-up, not a repo path — **FLAG, owed
  separately, not blocking this ADR's Accepted status**

---

## §7 — Implementation plan

- **Phase 0** — §0 reads reverified at implementation time (rerun the `git log -1` anchors above
  immediately before Phase 1 edits land).
- **Phase 1** — mechanical edits: scrub account ID/balances (16 files), redact LOCK.md-family
  parameter/backtest blocks (6 files), untrack `oanda_stage1/guardian_stage1.py`, fix the test
  fixture, add LICENSE. Lands as a normal reviewed PR to this (still-private) repo's `main`.
- **Phase 2** — grep-sweep verification (§10) rerun post-merge; zero hits required except the
  dispositioned `firm_rules.py` residual. ADR status flips `Proposed` → `Accepted` only once this
  is clean.
- **Phase 3** — *(requires separate explicit operator go-ahead — publish/account-setting action,
  not authorized by ADR acceptance alone)*: create the new public GitHub repository; seed it with a
  single "initial public release" commit built from Phase 1's merged tree, **excluding**
  `docs/notes/**`, `docs/ltm/**`, `docs/superpowers/**` per the §6 curation rule; configure branch
  protection and repo metadata.
- **Phase 4** — *(same explicit-go requirement)*: archive this repo (GitHub Settings → Archive —
  read-only, stays private, full history retained) once the new repo is confirmed live and green.
- **Phase 5** — operational follow-up: repoint Cursor background-agent configuration and any local
  clone remotes to the new repo.

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
# Discipline checks (mechanical) — run once brief-authoring's checker is available in this env
$ python <brief-authoring-skill-path>/scripts/check_brief.py docs/adr/2026-08-14-repo-public-visibility-transition.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation) — anchors above, reverify at Phase 0
$ git log -1 --format="%h %ci" -- .gitignore core/firm_rules.py core/dd_protection.py \
    docs/adr/2026-07-01-guardian-pyport-public-tracking.md core/strategies/_archive/guardian/LOCK.md \
    .github/workflows/tests.yml

# Downstream artifact update verification — post Phase 1, all §6 EDIT-dispositioned hits should be
# gone outside docs/notes|ltm|superpowers/** (substitute the literal values from the private archive
# for $ACCOUNT_ID / $ACCOUNT_NUMERIC_ID — not reproduced here; this file ships in the public seed)
$ git grep -n "$ACCOUNT_ID\|$ACCOUNT_NUMERIC_ID" -- . | grep -v '^docs/notes/\|^docs/ltm/\|^docs/superpowers/' ; echo "expect: no output"

# Supersede chain integrity (partial supersession — no accept+retire checklist required)
$ grep -A1 "Supersedes" docs/adr/2026-08-14-repo-public-visibility-transition.md
$ grep -A1 "Superseded-in-part-by" docs/adr/2026-07-01-guardian-pyport-public-tracking.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Initial authoring | Joshua + claude.ai |
