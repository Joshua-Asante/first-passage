# Operational rules

Hard rules. No exceptions. Each rule is here because it was violated or nearly violated in the past and the correction was costly.

---

## 1. Never override a valid signal based on a macro volatility forecast

If the strategy fires a valid signal per its Pine code, take the trade. Do not skip it because of a scheduled macro event, a conflict headline, a Fed meeting, a BOJ decision, or any other forecast about what volatility might do.

**The overlay mechanism exists for this.** If a regime genuinely warrants reduced exposure, apply a risk overlay. No overlays are currently active. Do not improvise per-trade skips.

**Origin (HISTORICAL):** Guardian (CFD book; cold-stored / venue-less as of Phase B/C 2026-08-23) fired a valid long during the Iran ceasefire announcement (entry 4653.26, 1:18.1 R:R). Trade was skipped on the reasoning that ceasefire-driven gold volatility was unpredictable. The trade subsequently moved in favor through breakeven. The skip had no basis in the system's measured edge — it was intuition dressed up as risk management. The Guardian conflict-risk overlay was deactivated 2026-04-23 and evicted 2026-06-05 — retrieve with `git show pre-prune-2026-06-05:archive/docs/methodology/archive/overlays/guardian_conflict_risk.md`. The *principle* (no per-trade skip of a valid signal; overlays only) remains live; Guardian is not a live book.

---

## 2. Audit production code before authoring risk-control briefs

Before writing any brief, ADR, or decision document that specifies risk-control parameters, read the current state of the code being discussed. Do not author proposals against remembered or assumed code state.

**Origin:** 2026-04-17 session. A dd_protection retune brief was authored against an assumed single-tier architecture. The actual code had a two-tier architecture with `min()` combination. Three decision iterations occurred in one session (retune → reverse → delete equity tier) because the first two iterations were arguing about code that didn't match reality.

**Workflow:** `view` the relevant file(s) before the first line of the brief. Not after. Not "I remember what it does." Before.

---

## 3. DXTrade `contractValue` for DJ30 MUST be 10

**Status:** **HISTORICAL / DORMANT.** DXTrade/CFD execution is retired and idle
under the [`2026-06-30 retirement ADR`](adr/2026-06-30-no-manual-trading-cfd-retirement.md).

Default DXTrade `contractValue` is 1. At `contractValue=1`, Striker position sizing produces approximately **7% per-trade risk** against a 1% intended risk. This is catastrophic and silent — the platform will execute the trade without warning.

**Conditional check:** If DXTrade is explicitly reactivated, verify
`contractValue=10` before any Striker trade.

**Origin:** Prop firm setup phase. Caught during Pine-to-platform parameter reconciliation. Would have been account-ending if missed.

---

## 4. Three or more consecutive losses on one strategy = normal variance

Do not adjust strategy parameters, reduce size, or skip signals in response to 3+ consecutive losses on a single strategy. This is within the normal variance distribution of every strategy in the portfolio.

**What to do instead:** Log the losing streak in `docs/SESSIONS.md` (and, if on the c1 rail, note it against M1 telemetry / fill evidence — not a deleted weekly-review feeder). Continue executing signals per the Pine code / c1 rail. Only consider intervention if ALL of the following hold:
- Losing streak exceeds 5yr backtest p99 for that strategy
- No identifiable regime shift explains it (e.g., conflict overlay applies)
- Session log / c1 telemetry shows a systematic issue (e.g., execution slippage materially different from backtest)

**Origin:** The Algorithm (Delete before Optimize). Reactive parameter tuning during drawdown is the most common failure mode in systematic trading. Intervention during losing streaks has, historically, made things worse more often than better.

---

## 5. Pine file is the source of truth for strategy parameters

If the Pine file and any document (CHANGELOG, ADR, Notion page, README) disagree on a parameter value, the Pine file wins. Fix the document.

The only exceptions are:
- `core/dd_protection.py` parameters — those live in the Python pipeline, not in Pine
- `core/firm_rules.py` allocations — same
- Active overlays — those modify risk at the sizing layer. None are currently active; the historical Guardian overlay is git-retrievable at the command in Rule 1.

---

## 6. Doc/code skew audit fires on every version lock

When any strategy's locked version changes (e.g., Guardian v5.4 → v5.5), or
when any locked risk/allocation/`dd_protection` constant changes, immediately
run a doc/code skew audit before closing the lock commit. The audit checks:

1. **`CLAUDE.md`** — strategy table, Multiplier System risk numbers, Protection
   constants, MC anchor lines. Anything pointing to a strategy version or risk
   value must reflect the new lock or be explicitly marked as historical
   record.
2. **All ADRs in `docs/adr/`** — every `Code:` cross-reference line, every
   inline version mention. Stale `Code:` pointers are updated; conclusion
   text is left intact (ADRs are historical records of decisions made under
   the prior version) but a parenthetical is added noting what changed
   between the decision-era version and current.
3. **Active overlays (if any)** — currently none; the historical Guardian
   overlay is git-retrievable at the command in Rule 1. When an overlay
   is active, audit its doc the same as ADRs.
4. **`docs/methodology/`** — same as ADRs, plus measurement values that quote
   "Guardian v<X> observed" must be either re-measured or marked as
   pre-version-bump archival.

**Audit trigger is the lock event itself**, not calendar. Calendar audits
(weekly, monthly) produce mostly no-ops between locks and miss the high-risk
zero-day-after-lock window. Per-commit-touching-`core/strategies/` is too aggressive
(routine code-only edits without locks fire false positives, and `core/strategies/`
may not even be tracked).

**Fallback**: if the audit cannot run inline with the lock (e.g., lock is
committed off-hours), fire it on the *next* repo-touch session and gate that
session on completing the audit before any new decision work. The skew window
must be measured and logged on every lock — even a 0-day window is a logged
0.

**Origin:** 2026-04-23 lock of Guardian v5.5 / Striker v4.4 / Aegis v4.3 (and
Guardian risk 0.30% → 0.34%) introduced a 2-day doc/code skew window
(2026-04-23 → 2026-04-25). Four ADRs and one overlay carried stale `Code:`
pointers to old Pine filenames (`guardian_v5.1.pine`, `striker_v4.3.pine`,
`aegis_v4.1.pine`); `CLAUDE.md`'s strategy table was missing the new versions
and the post-relock MC anchors. The skew was caught when OANDA backtest
filenames (`Guardian_Gold_v5.5_OANDA_XAUUSD_2026-04-25_9ae1f.csv`) forced a
comparison and refreshed in commit `cfea4a2` on 2026-04-25.

**Q8a audit result (per-decision verification, not asserted).** Every commit inside the 2-day skew
window (2026-04-23 21:00 lock to 2026-04-25 11:39 fix) was checked against the four stale `Code:`
pointers it left behind, for whether the decision consulted a stale pointer and, if so, whether the
deprecated code was logically equivalent at the relevant logic. **Result: zero corrupted decisions**
across the 10 commits in the window — each either explicitly cited the current version or touched
code paths the stale pointers didn't cover. Full per-commit table and the fix-commit `cfea4a2`
equivalence analysis: `git log -p` on this file (pre-2026-08 history) or `git show cfea4a2`.

---

## 7. One canonical owner per fact; every other mention links or is a labeled mirror

Every fact has exactly **one** canonical owner. Any other document that mentions
that fact must either (a) **link** to the owner, or (b) be explicitly labeled a
**derived mirror** — it must never silently restate the value. A document that
restates a value it does not own will drift, and a stale duplicate reads as
truth.

This generalizes Rule 5 (Pine owns strategy parameters) from constants to
**state and narrative docs**. Canonical owners:

| Fact class | Canonical owner |
|---|---|
| Strategy parameters (risk %, pyramid, SL/TP) | Pine source (per Rule 5) |
| Current lock state + source blob hashes | `core/strategies/_archive/<family>/LOCK.md` + hot `*_CARD.md` stubs ([`core/strategies/CATALOG.md`](../core/strategies/CATALOG.md)) |
| `dd_protection` / allocation constants | `core/dd_protection.py` / `core/firm_rules.py` |
| MC anchors (historical record + engine pins) | `docs/mc_anchor_history.md` + `tests/core/test_mc_synthetic_engine.py` |
| Decision rationale (the *why*) | `docs/adr/` |
| ADR lifecycle status (`Proposed`/`Accepted`/`Superseded`/`Withdrawn`/`Retired`) | ADR header fields + derived `docs/adr/INDEX.md` + `scripts/check_adr_graph.py` |
| Per-strategy version lineage | `core/strategies/_archive/<family>/*_CHANGELOG.md` (bodies); CARD stubs under `core/strategies/<family>/` |
| What happened, session by session | `docs/SESSIONS.md` (append-only, links out) |
| Carried-forward "open / next" | top entry of `docs/SESSIONS.md` |
| Per-Q forward disposition (Iterate exit) | closure's own `## Iterate` block (`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`); a STATE forward-board row is a labeled pointer mirror only |
| Durable atomic facts | Owning ADRs and [`docs/methodology/lessons/`](methodology/lessons/). Claude-project `MEMORY.md` + memory files (outside this worktree) are **assistive-only** — never a Rule 7 owner, never Rule 0 / §0 attestation. Same class as `repo_retrieve.py` ([Limb B](../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md)). |

Roles that must **not** restate canonical values:
- **`STATE.md`** — the open-threads + forward-obligation register (dormant
  cross-session threads with no other home + the forward-trigger board). Not a
  state snapshot: carries no working-tree status, risk %, anchor number, version,
  hash, or owner table — points here (this §7) for ownership. See its header.
  Executed operator decisions appear only in its **decision index** (one line
  + owner link per decision — restored 2026-08-22 after the Phase 6 diet; the
  2026-08-19 concise relaxation is historical, see edit log), never as dated
  narrative sections (demoted 2026-07-16; reaffirmed 2026-08-03 — see edit
  log). Closed/retired rows are deleted from STATE (not struck); detail stays
  with the owning ADR/closure.
- **`docs/SESSIONS.md`** — narrates work; links the ADR/CHANGELOG/commit instead
  of duplicating its values. Prefer W5 entry classes and links over prose; the
  ~40-word-per-field figure is a soft target the ADR itself calls directional, not
  an enforced cap — [`W5 ADR`](adr/2026-08-07-w5-governance-diet.md).
- **`CLAUDE.md` §Live-execution posture** — a pointer block: the current
  scale-path picture plus one line + ADR link per standing decision. The
  multi-paragraph decision narrative lives in the owning ADRs; a new posture
  decision adds one pointer line, not a retelling (demoted 2026-07-16 — see
  edit log). The gated lock surface elsewhere in `CLAUDE.md` (Strategy
  Reference table, MC-anchor headlines, §Protection) is a **canonical owner**,
  not a mirror — this role note does not apply to it.
- **`README.md`** — human entry index; links out everywhere. Its public-clone
  note is a one-liner pointing at `CLAUDE.md` §Public-clone posture (the
  canonical statement).

**Origin:** 2026-06-03 doc-taxonomy audit. `STATE.md` (dated 2026-05-15) had
drifted three weeks stale: it restated the locked strategy table and MC anchor
as `DJ30 0.75% / pyr 500%, NAS 0.45%`, anchor `98.78/0.12/4.17` — the
pre-2026-05-23-refresh values — while `CLAUDE.md` (canonical) had moved to
`DJ30 0.70% / pyr 750%, NAS 0.37%`, anchor `99.83/0.17/4.37`. The snapshot was
duplicating canonical state with no link back, so it silently became wrong.
`STATE.md` was demoted to in-flight-only the same day and this rule written to
prevent the class.

---

## 8. Rule 0 sub-rules (brief-authoring / §0 discipline)

Applied at brief-authoring time **and** at the §0 (Rule 0 audit-first) read that
opens any decision brief or implementation step. These are the operationalized
sub-rules of Rule 0 / Rule 2 — each anchored to a specific brief failure.

1. **Cross-reference grep before classifying "isolated cruft."** For each
   candidate move/delete, run `grep -rn <basename>` across active paths and
   report N callers in §0. If N > 3, classify as "doctrine-referenced cruft"
   rather than "isolated cruft" — the move still goes through, but the cross-ref
   repair budget is non-trivial. _(Anchored: Simplify-pass cross-ref miss,
   2026-05-07.)_
2. **Archive convention verification.** For any move targeting an archive, §0
   must list current `archive/` subtrees to confirm the brief's destination
   convention matches the existing tree. _(Anchored: Simplify-pass
   parallel-archive near-miss, 2026-05-07.)_
3. **Rule 0 reads must include surrounding context.** When a brief cites a
   specific line, §0 reads the surrounding section (±20 lines minimum), not the
   line in isolation. Disambiguating qualifiers often live nearby. _(Anchored:
   NAS100 drift fix brief CLAUDE.md:48-vs-50 miss, 2026-05-07.)_
4. **Architecture truth before edit prescription.** For briefs that prescribe
   edits to production code not seen in the current conversation, §0 reads the
   *actual architecture* (module purposes, schemas, function signatures) and the
   §0 report proposes the *edit shape*; confirm before execution. The "prescribe
   specific edits, then execute" pattern is reliable only when the author's
   mental model matches the codebase. _(Anchored: lock-NAS100-live Path A vs
   Path B, 2026-05-07.)_
5. **Lock procedures need an operational-tooling integration phase.** Pine +
   manifest + MC ≠ live. A lock is not complete until operational tooling
   (`firm_rules` / `dd_protection` / `lifecycle` / c1 sizing host
   `ops/c1_rail/c1_sizing_host_reference.py`) reflects the new strategy. The retired
   continuous-lot `accounts` / `cli` spine is not the checklist. Lock memos
   include an "operational tooling integrated" checklist item before declaring
   lock complete. _(Anchored: NAS100 v1 lock 2026-05-05 vs operational
   integration 2026-05-07 gap; accounts/cli retired substrate Phase 2.)_
6. **Live-execution claims require edge-captured citation.** When a brief
   asserts a strategy is performing as designed in live trading, or proposes a
   change motivated by live execution behavior, §0 must cite the most recent
   edge-captured / fill-quality artifact for the relevant venue (historically
   `journal_review.py` output — **RETIRED 2026-07-11** with the CFD estate;
   rebuild-repo-native if a fill source returns). "I'm trading the system"
   without this citation is unverified — see execution lessons E1 (2026-04-07
   Guardian skip, $3,752 counterfactual) and E2 (2026-04-15 Aegis decomposition,
   $6,100 gap). _(Anchored: 2026-04-29 honesty audit; methodology layer was 6×
   more cited than execution layer in briefs over a 7-week sample.)_
7. **Pre-registration freeze is a separate, earlier commit than results.** A
   pre-registration / FREEZE artifact (frozen H, gates, thresholds, verdict
   logic) must land in its **own commit** that is an *ancestor* of the first
   commit reading forward data or writing results — never the same commit. The
   run commit must **not** edit frozen verdict logic. "Frozen before the run"
   that lives in the same commit as the run is self-attestation, not
   git-verifiable; the whole point of pre-registration is external checkability.
   The gold-standard pattern is `46f47d1` (freeze) → `913829b` (run).
   **Closure stamping (permitted, convention ratified 2026-07-27).** A closure
   commit **may** rewrite the prereg's single `**Status:**` header line — e.g.
   `` `FROZEN` `` → `` `CLOSED — AMBIGUOUS-ALIGNMENT` `` plus the verdict and a
   link to the closure — provided **everything below that line is retained
   unedited**, and the stamp itself says so. This keeps a reader who opens the
   prereg from mistaking a spent freeze for a live one, and costs nothing in
   checkability: the frozen text is still byte-diffable against the freeze commit.
   Anything beyond that one line is a **run-commit edit of frozen material** and
   is not covered by this allowance. Worked examples: `b0189db` (Q-COSTGEO-1),
   `6812146` (Q-COSTGEO-3) — each a one-line stamp over a freeze that sits in its
   own ancestor commit (`a51ce0a` / `4aa9971`).
   **Mechanical check (shipped 2026-07-02; split 2026-07-27):** the Sentinel
   Tier-1 `preregistration_scan` (`ops/sentinel/scan.py`; report-only,
   fail-open; run via `make sentinel`) emits **two distinct findings**, because
   an added prereg and an edited one are different claims:
   `PREREG-SAMECOMMIT` — the prereg is **added** with the results (the
   self-attested class); and `PREREG-RUNEDIT` — the prereg **predates** the
   results but the run commit edited it beyond the status header (a cheap proxy
   for the `3935d2c` verdict-logic class; status-only stamps are exempt per the
   paragraph above). The full verdict-logic class still needs semantic diffing,
   so it remains partly operator-vigilance. _(Anchored: the 2026-07-27 weekly
   run flagged three commits as same-commit freezes; investigation found one real
   — `7f60dad` — and two that were the gold-standard pattern plus a closure
   stamp. A check that is wrong on the facts two times in three trains the
   operator to ignore it.)_
   _(Anchored: 2026-07-01 programme audit R4 — Q-INCUMBENT-REGIME-1 /
   clean-vintage / Phase-B §0.5 preregs were same-commit self-attested;
   Q-ORB-FRIDAY-1's run commit `3935d2c` edited verdict logic post-freeze,
   flipping AMBIGUOUS→FALSIFIED — anti-candidate that time, but the class is
   real.)_
8. **Paste literal search output before opening new work.** Before opening any
   new `lab/analysis/<theme>/<slug>/` directory or scoping new `core/`-adjacent
   implementation work (externally-sourced paper, algorithm, technique, or a
   task inherited from a "spawned as a separate task" pointer), §0 must paste
   the *literal command output* — not a conclusion — of searches against
   `lab/CATALOG.md` and `docs/briefs/INDEX.md` (and a cheap companion
   `git log --oneline -20` / keyword probe via
   `python scripts/check_advisor_dedup.py --keywords "..."`). An attestation
   without executed search output is void. **Any work naming a candidate
   mechanism for a specific instrument additionally reads
   `ops/instruments/<SYM>.md` in full** — that ledger's own purpose line
   already makes this mandatory ("any session deriving/testing/adjudicating on
   `<SYM>` MUST read this at session start"), and `check_advisor_dedup.py`'s
   corpus now includes `ops/instruments/*.md` + `docs/briefs/rnd-pipeline/*.md`
   so a mechanism-specific keyword probe surfaces it too — but the ledger read
   is the primary check; the probe is the cheap companion, same relationship
   as CATALOG/INDEX above. This is the creation-side mirror of sub-rule 1's
   deletion-side "cross-reference grep before classifying isolated cruft,"
   lifting the binding procedure from the 2026-07-26 forced-flow census past
   its harvest-only origin. _(Anchored:
   [`ADR 2026-08-13`](adr/2026-08-13-dedup-first-before-new-work.md);
   2026-08-13 Tradeify eval-battery near-miss (caught by deliberate sweep) and
   Magdon-Ismail closed-form MDD duplicate (uncaught until pre-commit
   `lab-catalog`); source language
   `N-2026-07-26-forced-flow-census` (pruned at the Great Prune; retrieve via
   `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`)
   L195-208. **2026-08-19 addendum:** a Research Analyst inaugural draft
   recommended GRADUATE on the D5 Baltussen intraday-momentum axis for MNQ as
   "unspent" — it had already been ratified, built, and killed twice (IS-era
   Stage-2, then OOS-era via D5-RECOST-1), HIGH-confidence, recorded in
   `ops/instruments/MNQ.md` N5 — because neither the mining pass nor the
   project-level dedup probe ever read that ledger. Caught by the operator
   asking whether the new work overlapped the instrument ledger, not by any
   automated gate. See `scripts/check_advisor_dedup.py`'s own docstring for
   the full account. **2026-08-19, same-day follow-up (Head of Research's own
   review of the near-miss):** the pattern is broader than this one instance
   — e.g. `docs/rejected_candidates.md`'s ORB-MNQ-1 Tradeify-rejection row is
   flagged in its own text as carrying no dedup-machinery tag, "must be
   checked by hand." `scripts/check_instrument_ledger_coverage.py <artifact>`
   is a mechanical, WARN-tier companion for the specific narrow slice of this
   pattern that's checkable without judgment: it derives the known-instrument
   set from `ops/instruments/*.md` filenames (no hand-maintained list to
   drift), flags any symbol the artifact mentions without citing that
   symbol's ledger, and prints (advisory only, not scored) the raw
   `docs/rejected_candidates.md` hit count per symbol as a by-hand-check
   reminder. Not wired into `scripts/gates.yml` — like `check_advisor_dedup.py`,
   it's a per-artifact assistant invoked at authoring time, not a
   staged-file-scanning pre-commit gate; run it alongside the dedup probe
   above, same discipline.)_
9. **Registry line on every new closure.** A non-grandfathered file under
   `docs/briefs/closures/` must carry `- **Registry:**` in the Iterate block:
   either `rejected_candidates.md — ### <heading>` (strategy-grounds
   FALSIFIED / DEAD / STOP / STAGE-1 FAIL / OPERATOR-KILL) or
   `n/a — <reason>` (RESOLVED, governance, not a strategy-grounds kill).
   Token-only; heading-join quality is judgment. The 2026-08-03→08-11 kill
   run produced ~15 closures with zero registry rows because Iterate / Board
   write were gated and the registry append was checklist-only.
   _(Anchored: 2026-08-08 quarterly object audit §1.2 diagnostic 4; feed
   resumed 2026-08-11 only when sessions remembered the checklist.)_
10. **Amend the existing owner before minting a sibling.** Before creating a
    new ADR, brief, notice, or `lab/analysis/<theme>/<slug>/`, paste search
    output that names the existing owner that should take an addendum, or
    states none exists. Attestation without executed output is void (same
    standard as sub-rule 8). Default is amend-in-place; a new file is the
    exception. Ceremony-tiering already prefers light records when no limb
    fires — this sub-rule is the adoption tooth, not a new ceremony.
    _(Anchored: F-2 already fired on ADR-count / file-Δ; MSL 17 ADD / 0
    REMOVE in 2 days; implied-SR light pair then full reversal.)_

**Origin:** migrated 2026-06-03 from `docs/notion/repo_context.md` §7 (the
brief-authoring priming surface for web/claude.ai), which was deleted that day —
the repo was public at the time, so claude.ai read the repo directly and no
longer needed a Notion-mirror priming doc. These six sub-rules were the only
non-mirror content in that file; they are relocated here as their canonical
in-repo home. The `brief-authoring` skill bundle carries a generalized
propagation and is downstream of this section (repo wins on drift). _(Sub-rule 7
added 2026-07-01; sub-rule 8 added 2026-08-13; sub-rules 9–10 added
2026-08-15.)_ **[2026-07-01 note:** the repo is now **private** (gh-verified
`isPrivate: true`); the "repo is public" rationale above is historical. claude.ai
reaches the repo via its GitHub connector, which supports private repos, so the
migration rationale is unaffected. See CLAUDE.md §Public-clone posture.**]**
⚠ **Superseded 2026-08-14:** the repo went public again
([transition ADR](adr/2026-08-14-repo-public-visibility-transition.md)); current
visibility is owned by CLAUDE.md §Public-clone posture, not this 2026-07-01
footnote. Either way claude.ai reaches the repo (directly when public, via the
GitHub connector when private), so the migration rationale this note defends
was never at risk.

---

## 9. Pine-dependent work in a git worktree requires a Pine sync pre-flight

`**/*.pine` is gitignored (the live edge is held privately — CLAUDE.md "Public-clone
posture"). Gitignored files are **not** shared across git worktrees: the locked
`.pine` live only in the primary checkout. Any worktree from `git worktree add`
starts with `core/strategies/*/*.pine` **absent**, which silently blocks every
Pine-dependent task — codification / scaffold extraction, and any decision-brief §0
that reads `*.pine`.

**Procedure (run at the start of any Pine-dependent task):**

1. **Pre-flight gate.** `python scripts/sync_pine_to_worktree.py --check` — exit 0
   if the locked Pine is present in the current tree, exit 1 if you are in a
   worktree without it. A brief's §0 reading `*.pine` should gate on this.
2. **Remedy.** `python scripts/sync_pine_to_worktree.py [--verify]` copies the
   locked `.pine` from the auto-detected primary worktree into the current
   worktree (gitignore keeps them uncommittable; `--verify` checks bytes against
   `core/strategies/MANIFEST.sha256`). This is the Pine analogue of restoring
   gitignored vendor data from its canonical source (cf. `scripts/parse_bar_export.py`).
3. **Fallback** when no local checkout has the Pine at all: use the
   brief-authoring §0 **citation-chain** sub-rule (Tier 1 audit-doc verbatim
   quote → Tier 2 `LOCK.md` → Tier 3 CHANGELOG/baselines), per Rule 8 and the
   Q-GUARDIAN-TRAIL-1 anchor. Cite, do not infer.

**Do not** edit locked `.pine` inside a worktree — Rule 5 stands (Pine source of
truth; edits happen in the primary checkout). Synced worktree copies are
read-only fuel for §0 reads and scaffold extraction; candidate Pine goes to
`core/strategies/candidates/` (a distinct, non-locked path).

**Origin:** 2026-06-05. The R&D-pipeline codification stage (reads the four
locked `.pine` as scaffold templates) was dispatched into worktree
`xenodochial-nobel-a54b80` and would have hit absent Pine — a `NEEDS_CONTEXT`
bounce at best, a silent Rule-0 citation substitution at worst. `validate_params`
Pine cross-check had already been silently no-op'ing in worktrees for the same
reason (that script was retired 2026-08-03 with the `params.toml` hub —
[ADR](adr/2026-08-03-params-toml-gate-retirement.md) — this is historical
illustration only, not a live cross-check today). `scripts/sync_pine_to_worktree.py`
+ this rule close the class.

---

## 10. Instrument-ledger read at session start; disposition append at session end

Any session that derives, tests, tunes, or adjudicates on an instrument MUST
(a) read `ops/instruments/<SYMBOL>.md` **before its first run or edit**, and
(b) append a dated disposition entry at session end. This applies on every
surface (Claude Code, claude.ai, cursor) — the ledger exists precisely because
per-surface memory is mutually invisible.

Ledgers carry: active concepts + status, dead/parked items (with revival bars),
durable instrument findings, the **shared anti-SNAG budget** (instrument-level,
counted across all sessions, with family-level sub-ledgers where mechanisms
genuinely differ), and open decisions awaiting adjudication.

Boundaries:
- Ledgers own instrument-level findings and concept status only. Strategy
  parameters stay canonical in Pine (Rule 5); sizing constants in
  `core/dd_protection.py`/`core/firm_rules.py`; everything else links out (Rule 7).
- Ledgers are created on the **first session touching a new instrument** — no
  pre-emptive backfill for instruments with only historical work (rules earn
  their place; so do ledgers).
- The §0 (Rule 0) read that opens any decision brief on an instrument includes
  the ledger read; treat a missing ledger read like a missing production read.

**Profile-block clause (added 2026-07-25;
canonical: [`docs/adr/2026-07-25-instrument-profile-index.md`](adr/2026-07-25-instrument-profile-index.md)).**
The session-end disposition includes updating the ledger's `PROFILE` block when a
verdict changed, and rebuilding the derived view
(`python scripts/instrument_profiles.py build`). Enforcement is mechanical — a
stale generated view fails the `instrument-profiles` gate
([`scripts/gates.yml`](../scripts/gates.yml)) — so this clause documents the
obligation rather than carrying it.

**Phase-0 cost-geometry pre-gate (added 2026-06-22; canonical:
[`docs/adr/2026-06-22-cost-geometry-pregate.md`](adr/2026-06-22-cost-geometry-pregate.md)).**
Any session that opens a *new candidate entry mechanism* on an instrument MUST,
at Phase 0 (before the first backtest), run the cost-geometry pre-gate and record
`cost_R` + the verdict in the ledger disposition:

```bash
python scripts/cost_geometry_pregate.py --csv <canonical M15 series> \
    --spread <round-trip spread, price units> --stop-atr <REALIZED stop ATR-mult>
```

It computes `median(spread)/median(ATR15m)` from the **canonical TV**
15m series (per the 2026-06-12 feed policy) and the realized round-trip
`cost_R = round_trip_cost / (stop_atr · median(ATR15m))`. **PASS iff
`cost_R < 0.05R`** (the round-trip cost a PF~2.0 after-cost leg absorbs with
margin; consistent with the standing 4×-median-cost hurdle). The stop fed in MUST
be the strategy's **realized** stop, not an assumed comfortable k·ATR — the USOIL
trap is a sub-ATR confirmation stop that reads "comfortable" assumed but is ~8×
the cost realized (use `--realized-stop` for structural stops; the gate flags any
sub-ATR stop). A **FAIL** means the mechanism *as specified* is cost-infeasible
and does not proceed to backtest without a stop-geometry change or a lower-cost
venue (the venue/cost add-back condition,
[`docs/adr/2026-06-14-rejected-candidate-patterns.md`](adr/2026-06-14-rejected-candidate-patterns.md)
§A). A **PASS is necessary-not-sufficient** — the pre-registered backtest still
runs. This makes the L-COST-GEOMETRY lesson (the USOIL spike-fader kill,
[`lab/archive/usoil_rdm/RESULTS.md`](../lab/archive/usoil_rdm/RESULTS.md) (stub:
[`lab/analysis/usoil_rdm/CARD.md`](../lab/analysis/usoil_rdm/CARD.md)); the
USDCAD durable finding #1) a mechanical pre-flight rather than a post-hoc finding.

**Origin:** 2026-06-11 USDCAD parallel-session collision — two same-day sessions
burned one instrument's shared anti-SNAG budget with mutually invisible
forbidden moves and findings, and one session's pre-registration (BPC FM#3)
ambiguously captured the other session's concept (SVRN v0.2-X15). Ratified as
proposal P1 the same day. Decision record:
`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`. First ledger:
`ops/instruments/USDCAD.md`.

---

## 11. Retirement events back-propagate to standing falsifiers

When an ADR/decision retires a **venue, feed, or operator role** (or otherwise
removes a surface that a *live* falsifier limb depends on), that same decision
MUST sweep the standing falsifier set for limbs referencing the retired surface
and, for each one it darkens, append a dated **re-arm condition** (an addendum,
never an in-place edit of the falsifier). A falsifier whose input can no longer
accrue is not "in force" regardless of unchanged threshold text — an
unacknowledged dormant falsifier reads as live coverage that does not exist.

**What "back-propagate" requires:** for each dormant limb — (a) name it and the
retiring event, (b) state why its input can no longer accrue, (c) give the
condition under which it re-arms (usually: the replacement surface goes live), (d)
confirm the *surviving* limbs still cover the decision. Do this in the retiring
ADR's own §Consequences and by addendum on each affected prior ADR.

**Origin:** 2026-07-01 programme audit. The 2026-06-30 CFD-retirement ADR
(manual trading stopped, FXIFY idle) silently darkened the 2026-05-23
allocation-refresh ADR's live edge-captured limbs (DJ30/NAS100 <0.70 over ≥30
post-lock trades — half of that lock's named "dual retroactive catch-paths") and
the decompound-HOLD §4 limb 1 (≥2 live challenge failures / 6mo). The 06-30 ADR
proved the failure class was understood — it flagged unaccruability for *its own*
≥80%-ECR revert metric — but did not apply it to the older ADRs. NAS100's limb
was in fact dark from birth (zero verified fills ever). Same class: the Guardian
decay-gate (dormancy ~14mo → indefinite once Guardian was benched off the
futures venue) and the STATE.md Q-NAS-ECR-1 gate (keyed on a "verified
DXTrade fill" that can no longer occur). Retroactive addenda landed the same day
(2026-05-23 ADR, decompound-HOLD ADR, decay-gate README, STATE.md).

---

## 12. A DRAFT / HOLD artifact needs an explicit lift artifact before it merges

A commit or PR marked `[DRAFT]`, `[HOLD]`, or "DO NOT MERGE without <owner>'s go"
may only be merged after an **explicit, timestamped, identity-attributed lift**
— minimally a PR review/comment by the owner stating approval and that the
draft/hold is lifted (e.g. "Approved <date> … Un-drafted; ready to merge"). The
lift is the artifact of record; do not rely on merge-actor inference (a git
author string) as the ratification. This is a governance/merge discipline, not a
risk-control gate — but a DRAFT-HOLD that merges on inferred approval erodes the
signal for the next one.

**Origin:** 2026-07-01 programme audit. `034cef6` ("[DRAFT -- HOLD] … DO NOT MERGE
without Joshua's go") merged via `eaff257` ~21 min later. Ratification *was*
adequately documented (PR #264 carried an explicit "Approved … Un-drafted; ready
to merge" comment 21s pre-merge) — but no *procedure* existed, so on first read
the merge looked like a bypass. This rule codifies what PR #264 already did.

---

## 13. Venue facts are recorded as quote + source + date + explicit scope; silence on scope reads BROAD

Any obligation borrowed from a venue, broker, or counterparty document — ToS,
help-centre article, contract clause, dashboard rule — is recorded with four
things or it is not recorded:

1. **The verbatim quote.** Not a paraphrase, not "verbatim substance". A
   four-point summary of a four-point clause loses exactly the sub-clause that
   turns out to matter.
2. **The source**, to the article number or contract section.
3. **The date read**, because these drift (Tradeify's own Guidelines article is
   stamped "Updated this week" and the firm revises on a ~90-day cycle).
4. **An explicit scope tag** — which phase/account-type the obligation binds:
   `STANDING` (in force now) vs `PAYOUT-GATED` vs `funded-only`, etc.

**The scope rule, which is the load-bearing half:** when the source is *silent*
on scope, check whether that same source scopes its **sibling** rules
explicitly. If the siblings are scoped and yours is not, **the silence is
deliberate and the obligation reads BROAD.** Do not resolve silence with the
narrow reading because narrow feels conservative — it is the opposite. A
wrongly-narrowed obligation reads as *"not owed yet"*, so readiness is deferred
and nobody re-checks; it surfaces only when the counterparty acts, on their
timing. A wrongly-broad reading costs some unnecessary preparation. **Default
BROAD on silence.**

**Never inherit a qualifier the source does not carry**, including from our own
prior notes. When correcting one, record *where in the chain the narrowing
entered* — the original venue read is usually innocent, and distrusting it is
the wrong repair. Corollary: if a note narrows a rule relative to the spec it
cites, that is a defect in the note, not a refinement.

**Precedence must be read, not assumed.** Which source wins on conflict is
itself a fact with a location — read the agreement's own precedence clause
before asserting a hierarchy. For Tradeify that is FTA §11 + §4.1, and it runs
**opposite** to what this repo assumed for weeks.

**Origin — two paid incidents, both 2026-07-31, both from the same missing
convention:**

- **Scope narrowed in transcription.** The automation-identity obligations
  (sole-ownership proof, live video of enabling the code) were filed in
  [`TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`](notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)
  as *"Before relying on the rail for a **funded** payout"*, in a payout
  checklist. Help-centre article 10468318 carries **no funded/eval qualifier**
  on its Bots section, while scoping microscalping (*"ONLY to sim funded
  accounts"*) and idle-time (heading names both) explicitly. The obligations
  were **standing, in force on the eval**, and had been mis-filed as deferred.
  The 07-30 design spec had it correctly unscoped; the narrowing entered
  transcribing spec → standing-owner note. Quote fidelity was never at fault.
- **Precedence inverted, in five documents.** The repo carried *"if the FTA
  disagrees with the help centre, the FTA wins."* FTA **§11** says the **Help
  Center** prevails on trading rules, account parameters, product
  classifications/groupings, and prohibited-conduct definitions; §4.1
  incorporates help-centre rules as binding. No verdict flipped — every affected
  citation happened to agree across sources — but the reasoning ran on the
  inverted rule for weeks, and help-centre-sourced pins had been recorded as
  provisional when they were in fact governing.

Neither was expensive to fix and both were nearly free to find: each came from
reading a public web page. That asymmetry — cheap to check, silently wrong for
weeks — is what earns this rule its place.

**Canonical worked example:**
[`docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md`](notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md)
(§Precedence, §1, §1a, §1b) — quote-first, scope-tagged, precedence read from
the agreement rather than assumed.

---

## 14. Corrections land where the error is read, not where it is convenient to write

A withdrawn, superseded, or retracted claim must be marked **at the position a
reader encounters it** — the headline, the §Verdict, the top-of-card table —
not only in an addendum appended below it. Documents are consumed in **reading
order**; corrections were being applied in **writing order**, and the gap
between the two is invisible to a diff review (the correction *is there*, just
downstream of the claim it corrects).

**The two-class boundary this rule draws, which Trap #12 never drew:**

1. **FROZEN artifacts** (pre-registrations, closures, signed/ratified bodies):
   Trap #12 stands — the body stays byte-unedited and the impeachment lives in
   an addendum. **But the addendum alone is not the correction.** A
   reader-intercept goes **upstream of the impeached claim in reading order**:
   a head banner, or a `⚠ SUPERSEDED — see Addendum` marker directly above the
   stale table. The canonical worked example is the book-composition brief's
   §2 banner (2026-07-28), placed *above* the eval columns it impeaches.
   Trap #12 protects the **record**; the intercept protects the **reader**.
   Both, always — one without the other is half a correction.
2. **LIVING operational documents** (desk cards, DRAFT specs, STATE, ledgers,
   compliance notes, same-session RESULTS not yet merged): corrected **in
   place, at the assertion site**. A living doc that retracts its own headline
   three paragraphs below the headline has not been corrected. Same-session
   work is *never* frozen — freezing your own uncommitted document and
   appending to it is the append reflex misfiring, not discipline.

**The sweep half (extends the restating-surfaces rule):** withdrawing a claim
is not complete until the withdrawn value has been grepped **repo-wide,
including artifacts authored in the same session** — your own hour-old
documents are restating surfaces too, and they are precisely the ones the
author skips because the correction feels "already handled" by the addendum
they just wrote.

**Mechanical backstop (deliberately narrow):**
`scripts/check_supersession_placement.py` (the `supersession-placement` gate,
[`scripts/gates.yml`](../scripts/gates.yml)) hard-fails any
in-scope document (desk cards, `lab/analysis/*/RESULTS*.md`) whose
addendum-confined supersession token has no upstream marker or pointer. It
catches the addendum-shaped instance only; the in-section instance (a claim
retracted below itself inside one section) is judgment and stays owned by this
rule's prose — a gate pretending to cover it would be vacuous assurance (M-8).

Earned 2026-08-02: **two firings in one session** (a RESULTS §Verdict still
asserting a figure its own Addendum c withdrew; a desk card *leading* with a
"MEASURED" table whose numbers were retracted three paragraphs later — read
top-down at the desk, the retraction inverted into its opposite), caught only
by a manual pre-merge review; the gate's first repo scan then found **four
merged-or-pending instances**, confirming the pattern predates the session.

---

## 15. Always-on hosting is not the desktop (console-only desktops)

**Always-on processes** (c1 listener, future signal daemon, any process that must
survive a laptop lid-close) run on an **always-on host** (Fly.io today for the
c1 rail — see `deploy/c1_rail/`). The operator desktop is **console-only** for
those processes: SSH/`fly ssh`, status reads, attended arm/disarm commands —
not the runtime host.

**Scope:** always-on / unattended-capable services. Does **not** ban
route-LOCAL interactive agent work (Cursor fleet, one-shot analysis) on a
desktop. Does **not** authorize leaving `dry_run=false` unattended.

Owner ADR: [`docs/adr/2026-08-07-w6-rail-infra-closures.md`](adr/2026-08-07-w6-rail-infra-closures.md).
Pointers: `deploy/c1_rail/README.md` · `.claude/skills/c1-rail/SKILL.md`.

## 16. Retention — an artifact must earn its place, and deletion is classified by execution, not by folder

**Paid for by:** the 2026-08-08 quarterly audit (both layers `Degenerating`; ADR corpus 48→121 in 38 days with zero removals; 47 trigger riders on one date, 37 owed and 2 discharged; 15 checks that cannot fire) and by four classifier failures during the prune that followed it.

**The retention test.** An artifact survives iff at least one holds:

- **R1 — pipeline-consumed:** read at decision time by the live pipeline (intake screens, instrument ledgers, `docs/rejected_candidates.md`, OPEN briefs and their pre-registrations, `discovery_manifests/`, gate scripts that fire).
- **R2 — live safety:** carries a live safety invariant for real money or the rail (M1 chain, RUNBOOK, compliance, arming rules, `dd_protection`/`firm_rules` change-control).
- **R3 — re-proposal bar:** primary kill evidence a DEAD-list row or `rejected_candidates.md` cites as its kill source.
- **R4 — reproducibility manifest** for non-regenerable bytes (`SHA256SUMS`, Pine `MANIFEST`, `PORT_MANIFEST`).
- **R5 — open obligation:** an operator-signed decision with a still-open, dated, **fireable** obligation. An obligation whose check *cannot fire* does not qualify — unfalsifiable ceremony is deletable even when signed.

Everything else is deleted under a snapshot tag and retrieved with `git show <tag>:<path>`. Revival requires fresh pre-registration under the standing chain — never a lookup.

**The classification instrument (this is the part that was paid for).** "It lives under `docs/` so it is prose" is **false** and cost four near-misses, including the c1 arming artifact. Before any deletion commit lands, run all four:

1. quoted-path scan for `docs/…` and `lab/…` literals across `core/ ops/ scripts/ tests/ lab/`;
2. **pathlib-join scan** (`"docs" / "notes" / …`) — constructed paths have no literal to grep;
3. inbound markdown-link analysis from the files that will survive;
4. **full `pytest`** — the pre-commit gate battery does not run tests and is not sufficient evidence of safety.

Owner: [`ADR 2026-08-08-great-prune`](adr/2026-08-08-great-prune.md) (§2 test, §4a failure log).

## 17. Quarterly programme-audit checklist — standing tooling census

This checklist's first entry is the mechanical partial-check for *Rule 11*'s obligation (a
falsifier whose input can no longer accrue is not "in force" regardless of unchanged threshold
text) — see Rule 11 for the underlying duty; coverage here is a minority of falsifiers and blind
to retirement (per the script's own docstring), so a clean run is never a substitute for a Rule 11
sweep.

At each quarterly programme audit (`programme-audit` skill cadence; next **2026-11-08**), run:

- `python scripts/check_falsifier_reachability.py --stats` and record the **coverage trend**, not
  just the point figure. The script's own docstring shows coverage eroding as the ADR corpus grows
  faster than anchored falsifiers (28% → 25% → 23% across three reads) — a single number carries no
  information about direction. This is **not** a hard gate — the script's own docstring explains why
  (M-22 lesson: a hard gate here would block commits on ADRs nobody is touching). `scripts/gates.yml`
  id `falsifier-reachability-census` already runs it report-only on every `make check` invocation
  (and the CI-required `skills (3.12)` job) — **not** `make validate`, which is a narrower historical
  selector (data manifests + Pine only; verified against `gate_manifest.py`'s `select_gates()`) — so
  the trend surfaces well before the quarterly cycle; this line is the standing human checkpoint that
  actually reads the trend and decides whether it warrants action.

This is the checklist's first entry — future standing per-cycle tooling runs are added here as
additional bullets, not as new rules.

**Origin:** 2026-08-27/28 SSOT/data-lineage remediation program
([`ADR`](adr/2026-08-27-ssot-data-lineage-remediation-program.md) Phase 1 Task 4).
`check_falsifier_reachability.py` already existed and already self-reported real eroding coverage,
but ran on no schedule at all — it was never wired into `gates.yml` and had no standing checklist to
belong to. **Note on scope:** the governing ADR's own §2 Scope line refers to "`docs/operational_rules.md`'s
quarterly-checklist section" as though one already existed; Task 4's own Step 1 (grep this file for
`quarterly`/`programme.audit`) found no section under that description — this rule is that
checklist's first entry, not an edit to a prior one. Recorded here per Rule 0 (verify current file
shapes before acting on a brief's assumption) rather than silently treating the ADR's premise as
correct.

## Rule maintenance

New operational rules are added here only after a specific failure or near-miss. Do not add preemptive rules based on what might go wrong. Rules earn their place by being paid for.

Edits to existing rules must be logged with a dated entry explaining what changed and why. Rules do not silently drift.

### Edit log

Full incident narration for each entry lives in `git log -p` on this file and in the linked ADR; this
log states what changed and why in one line. Unless noted, edits are additive — no locked config,
allocation, `dd_protection`, Pine, or rail touched.

- **2026-08-28** — Rule 17 added (quarterly programme-audit checklist; `check_falsifier_reachability.py --stats` census, wired `gates.yml`). [`ADR`](adr/2026-08-27-ssot-data-lineage-remediation-program.md)
- **2026-08-23** — P4 museum rules: Rule 1 origin marked HISTORICAL (Guardian cold-stored); Rule 7 lock-state paths retargeted to `_archive/<family>/`.
- **2026-08-23** — Rule 7 durable-atoms owner demoted to owning ADRs / `docs/methodology/lessons/`; Claude-project MEMORY is assistive-only, never a Rule 7 owner. [`addendum`](adr/2026-06-30-state-md-role-reduction.md#addendum-2026-08-23--memory-is-assistive-only-not-the-rule-7-owner)
- **2026-08-22** — Rule 7 STATE decision-index restored to one line + owner (had grown back into multi-paragraph restatements after the 2026-08-19 relaxation below).
- **2026-08-21** — Rule 9/10/14 reference repair: dropped a stale retired-script example, replaced drifted ordinal gate-number pointers with stable `id:` fields. No rule behavior changed.
- **2026-08-19** — Rule 7 STATE decision-index cap relaxed from strict one-line to concise (practice had drifted; operator ruled relax-to-match). Still bars multi-sentence narrative.
- **2026-08-15** — Rule 8 sub-rules 9–10 added: closures carry a `Registry:` line; amend the existing owner before minting a new ADR/brief/notice/lab slug. [`ADR`](adr/2026-08-13-dedup-first-before-new-work.md)
- **2026-08-13** — Rule 8 sub-rule 8 added: paste literal dedup-search output (`lab/CATALOG.md` + `docs/briefs/INDEX.md`) before opening new work. [`ADR`](adr/2026-08-13-dedup-first-before-new-work.md)
- **2026-08-08** — ADR ceremony stakes-tiering ratified (pointer only, no rule text changed): full §0–§7 only when a tier-test limb fires. [`ADR`](adr/2026-08-08-adr-ceremony-tiering.md)
- **2026-08-07** — Rule 15 added (always-on hosting is not the desktop). [`ADR`](adr/2026-08-07-w6-rail-infra-closures.md)
- **2026-08-07** — Rule 7 / SESSIONS·STATE entry-class direction (W5 — see the prose-target note above §7). [`ADR`](adr/2026-08-07-w5-governance-diet.md)
- **2026-08-07** — Rule 7 owner table drops the retired `params.toml` row.
- **2026-08-04** — Rule 7 owner table gains a "Per-Q forward disposition" row (each closure's own `## Iterate` block is canonical).
- **2026-08-03** — Rule 7 STATE anti-accretion reaffirmed after STATE re-grew past charter (~2129 lines); rewritten to open-board only.
- **2026-08-02** — Rule 14 added (corrections land where the error is read, not where it's convenient to write) + gate `check_supersession_placement.py`.
- **2026-08-02** — Rule 4 + Rule 8 sub-rule 5 updated to point at current owners (retired weekly-review-feeder / accounts / cli surfaces).
- **2026-08-02** — Rule 13 added (venue facts recorded as quote + source + date + explicit scope; silence reads BROAD).
- **2026-07-16** — Rule 7 role list extended: CLAUDE.md posture, STATE.md decisions, README public-clone note all demoted to pointers (root-doc de-dup). [`ADR`](adr/2026-07-16-root-doc-charter-dedup.md)
- **2026-07-11** — Rule 3 marked dormant unless DXTrade is explicitly reactivated.
- **2026-07-10** — Live-path skew repair: Rule 7/9 examples updated to current `core/` paths.
- **2026-07-02** — Rule 8 sub-rule 7: shipped the queued mechanical check (`ops/sentinel/scan.py` `preregistration_scan`).
- **2026-07-01** — Rules 11 + 12 added (falsifier back-propagation on retirement; DRAFT/HOLD needs an explicit lift artifact); Rule 8 sub-rule 7 added (pre-registration freeze is a separate earlier commit) — programme-audit remediation.
- **2026-06-22** — Rule 10 gained the Phase-0 cost-geometry pre-gate (`scripts/cost_geometry_pregate.py`). [`ADR`](adr/2026-06-22-cost-geometry-pregate.md)
