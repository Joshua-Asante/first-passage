# Q-PUBTRANS-1 — CLOSURE: `FALSIFIED` (Limb-D8 concretely fails; Limb-B5/D9 still owed)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED` (governance/methodology completeness Q, not a strategy PREREG F2 lane)
**Pre-registration:** [`Q-PUBTRANS-1-verdict-preregistration.md`](../pre-registration/Q-PUBTRANS-1-verdict-preregistration.md) — frozen at the brief's own 2026-08-18 authoring (Section 8's self-freeze); this sibling file is a 2026-08-23 mechanical backfill, not a re-freeze.
**Successor:** none named yet — B5 and D9 route to direct operator action (see Iterate), not a new Q
**Spend / K:** $0.00 · K consumed: 0
**Live effect:** none (no code, ADR, Pine, allocation, or dd_protection surface touched; no arming)
**Artifacts:** `docs/methodology/1r_estimation.md:77,153,379` (the D8 leak); `docs/adr/2026-08-14-repo-public-visibility-transition.md` (Status now `Accepted`, re-checked); `STATE.md:73` (the 2026-08-22 batch-Accept line); commit `19beee2` and remote-tracking ref `archive/main` (the D9 evidence)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | All three limbs clear | Not reached — D8 fails | — |
| `FALSIFIED` | Any one limb fails (B5 real literal, OR D8 ≥1 concrete field, OR D9 ≥1 item with no disposition record anywhere reachable) | **D8: FAILS.** Guardian Gold's ATR multiplier (1.55×) and grace-stop mechanism (`graceStopMult=2.0`, `minBarsBeforeStop=1`) are explicitly stated with a Pine file:line citation (`Guardian_Gold_v5.5_Strategy.pine:49,195-197`) in `docs/methodology/1r_estimation.md:77,379` — a tracked, non-gitignored, public file absent from the transition ADR's own §6 downstream-artifact inventory. A second, softer hit: Striker pyramid-layer stop ~1.77% of layer equity (line 153). | ✓ (on D8 alone) |
| `AMBIGUOUS-HOLD` | D8 checked and holds, but B5/D9 unresolved | Does not apply — D8 was checked and does NOT hold | — |

Per Brief §4 verbatim: "Any single limb failure means the transition did not complete cleanly." H-PUBTRANS is REJECTED on Limb-D8 alone; Limb-B5 and Limb-D9 were also investigated (see §2) but neither independently confirmed nor exonerated — both remain open, routed via the Iterate block below, per the FALSIFIED disposition's own instruction ("ITERATE for the brief as a whole, since the other limbs may still need their own verdict recorded").

## 2. What the pre-registration predicted vs what happened

Predicted (§D of the pre-registration, and the orchestrating task's own framing at GO time): `BLOCKED-NEEDS-OPERATOR-INPUT` — Brief §7 called Limb-D8 "fully agent-executable ($0, ~20-30 min)" and expected it to hold, "matching what the ADR accepted" as residual risk. That expectation is **wrong**: D8 fails on the first genuinely decisive hit, sourced from a file the ADR's own remediation inventory never enumerated. This is a real surprise, recorded as such rather than retrofitted.

A second surprise: Limb-D9's brief-stated remaining step ("needs private `first-passage-archive` repo access this session doesn't have") is also wrong. This local checkout has a configured `archive` remote (`https://github.com/Joshua-Asante/first-passage-archive.git`) already fetched and cached (`refs/remotes/archive/*`, HEAD at commit `73971f1`, dated 2026-08-15). Reading the actual archived queue.md there, and scanning ~140 subsequent archive-lineage commits for any disposition mention of the 12 pre-transition items, found nothing — strong (not airtight — see §3) evidence toward a second FALSIFIED limb, using genuine private-archive access, not a substitute for it.

A third, smaller surprise: Brief Section 0's ADR-status citation (`Proposed`, as of 2026-08-18) is now stale — the operator flipped it to `Accepted` on 2026-08-22, in a batch alongside 3 unrelated Proposed ADRs (STATE.md:73), a pattern that reads as status-hygiene rather than a dedicated re-run of the ADR's own §7-Phase-2-required grep-sweep.

A count correction, not a surprise about the mechanism but about the numbers: the audit note and brief both say "11 (7 PREREG-RUNEDIT + 4 PREREG-SAMECOMMIT)"; the actual 2026-08-10 sentinel run's own Action section contains **12 (7 + 5)** — the 5th SAMECOMMIT item is `PREREG-SAMECOMMIT-df7824e`.

## 3. What this closure does NOT license

- Does NOT license editing, redacting, or otherwise touching `docs/methodology/1r_estimation.md` under this brief — Brief §5's forbidden-move discipline (this Q names gaps, it does not open remediation) plus the general "naming is not opening" convention mean the redaction fix is a separate, operator-owned decision (a fresh remediation pass, per §6's own disposition text: "redaction patch, doc-vocabulary sweep... not a re-run of this same check").
- Does NOT license reading the D9 archive-remote evidence as a substitute for operator confirmation — it is strong circumstantial evidence from a genuinely private source, not a certified "no disposition record anywhere reachable" per Brief §5 forbidden-move #4's own standard (operator confirmation is still a distinct, unchecked channel).
- Does NOT license treating the 2026-08-22 ADR Accept as satisfying Limb-B5 — see §2; this closure explicitly declines that inference (Brief Forbidden Move #1, reinstantiated).
- Does NOT flip the ADR's Status back, edit STATE.md's OPERATOR QUEUE, or touch `docs/notes/sentinel/queue.md` — all three remain operator/ADR-owned per Brief §5.
- Does NOT authorize live-execution or dd_protection/allocation changes — none of the three limbs touch that surface; this is a governance-completeness Q, not a strategy-grounds finding.

## 4. Defects found in the frozen brief (recorded, not repaired)

1. **Section 0 drift.** The ADR Status citation (`Proposed`) is stale as of the operator's 2026-08-22 Accept — a fact that postdates the brief's 2026-08-18 authoring/re-check by 5 days and predates this Phase 1 execution by 1 day. Not a brief-authoring error (it was accurate when written); flagged so a successor doesn't re-cite the stale value.
2. **Section 7/audit-note item-count error.** "11 (7 PREREG-RUNEDIT + 4 PREREG-SAMECOMMIT)" should read "12 (7 + 5)" — verified by direct retrieval of the 2026-08-10 sentinel run's own Action section via `git show 19beee2:docs/notes/sentinel/queue.md`. Traced to the 2026-08-18 audit note (`...assumptions-sweep.md:146`), which the brief inherited without independently recounting.
3. **Section 7's D9 execution-plan premise is factually wrong.** "Remaining step needs private `first-passage-archive` repo access this session doesn't have" — false. The archive is a configured, already-fetched local git remote in this exact checkout. This is a load-bearing correction: a genuinely $0, agent-executable check was mischaracterized as operator/access-blocked, and would have gone unexamined if taken at face value.

## 5. Lesson candidates

- **"Unreachable from HEAD" ≠ "inaccessible."** `git merge-base --is-ancestor <sha> HEAD` returning exit 1 (the brief's own D9 audit hook) proves only that a commit isn't an ancestor of the current branch tip — it says nothing about whether the commit object is still present in the local object database. `git show <sha>:<path>` retrieved the full pre-transition sentinel queue directly. Dated anchor: 2026-08-23, this brief. Cost avoided: a real, decidable-at-$0 question (D9) was one inference away from being deferred to "needs private archive access" indefinitely. Perishability risk flagged: `19beee2` is unreachable from HEAD and could be pruned by a future `git gc`; a successor should either tag it (`git tag preserve/pubtrans-19beee2 19beee2`) or export its `queue.md` blob to a permanent location before that happens — this session could not do so (read-only checkout).
- **A batch ADR-Accept sweep is not evidence of any one ADR's own specific closing-grep having been rerun.** Extends the standing "a green gate is not evidence — coverage is" pattern (MEMORY.md `lesson_green_gate_is_not_coverage.md`) to ADR status fields: STATE.md:73's "Leftover Proposed ADRs: four Accepted" line accepted 4 unrelated ADRs in one sweep, which is legitimate hygiene but should not be read, on its own, as proof that THIS ADR's own §7 Phase-2 grep-sweep requirement was individually satisfied. Below the two-incident bar for a dedicated lesson file on its own — watch for a second instance before promoting.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED` (fired by Limb-D8; Limb-B5 and Limb-D9 remain individually unresolved)
- **Model update:** The brief's own confidence that D8 would hold (matching the ADR's accepted "sizing/instrument/version only" residual-risk framing) was wrong — the 2026-08-14 remediation pass's own file inventory never enumerated `docs/methodology/1r_estimation.md`, so a genuine parameter leak survived it undetected for over a week of public exposure. Separately, "needs private-archive access" was model-confabulated, not verified — the archive was a local git remote the whole time. Both corrections argue for verifying a stated blocker (grep for the resource, don't just trust the brief's characterization) before accepting it as a wall.
- **Next:** `ITERATE`
- **Routing:** ITERATE -> (a) an **operator decision item** for D8's STOP gap: a redaction/doc-vocabulary-sweep decision on `docs/methodology/1r_estimation.md` (and a scoped check of similar Rule-0-heavy methodology docs for the same class of leak, since this file was never flagged by the original transition audit); (b) a **dated operator packet** for Limb-B5: paste the withheld literal into the ADR §10 / Brief §10 grep commands, AND confirm whether the 2026-08-22 batch Accept included that grep or was status-only; (c) a **dated operator packet** for Limb-D9: confirm disposition (or its absence) of the corrected 12-item list, ideally after a fresh `git fetch archive` to rule out local-cache staleness.
- **Entry packet:** *(required — Next = ITERATE)* — carries forward: the exact D8 citation (`docs/methodology/1r_estimation.md:77,153,379`, Pine anchor `Guardian_Gold_v5.5_Strategy.pine:49,195-197`); the corrected D9 count (12 = 7 RUNEDIT + 5 SAMECOMMIT, full ID list in phase1_findings); the discovery that `archive` is a usable local git remote (URL, cached HEAD `73971f1` @ 2026-08-15) — a successor should `git fetch archive` before re-asking the D9 question; the B5 audit-hook commands verbatim from ADR §10 / Brief §10, still needing only the literal values. Forbidden re-opens: do not re-derive or guess the B5 literals; do not re-run the D8 grep expecting a different answer (it's settled); do not treat the 2026-08-22 Accept as B5 evidence.
- **Stop rule / re-proposal bar:** D8's finding does not get re-tested ("is it still concretely recoverable") — that's settled; re-proposal for D8's thread needs a *completed* redaction/doc-vocabulary decision, not a re-run of this grep. B5 and D9 re-open specifically on: the operator supplying the withheld literal (B5), or the operator confirming/denying disposition of the 12 items, or a fresh `archive` fetch showing new information (D9).
- **Board write:** STATE.md OPERATOR QUEUE row (≤5 cap, currently 2/5 — room for one more):
  `| 3 | **Q-PUBTRANS-1 follow-up — D8 leak fix + B5/D9 operator confirms.** D8 \`FALSIFIED\` (Guardian ATR 1.55x leaked at \`docs/methodology/1r_estimation.md:77,379\`, missed by the 2026-08-14 sweep); B5 needs the withheld literal (+ confirm the 2026-08-22 batch Accept wasn't read as B5 evidence); D9 needs disposition confirm on 12 (not 11) pre-transition sentinel items — the archive is a reachable local git remote, not inaccessible as the brief assumed. | [\`Q-PUBTRANS-1\`](docs/briefs/Q-PUBTRANS-1-public-transition-completeness.md) · [\`closure\`](docs/briefs/closures/Q-PUBTRANS-1-closure-falsified.md) | next redaction-sweep decision + two operator confirms |`
- **Registry:** `n/a — governance/methodology completeness question, not a strategy-grounds kill; no rejected_candidates.md row owed`

## §10 audit-hook discharge

```
# Brief §10, Limb-D8 (executed in full):
$ grep -rniE "ATR|\bSL\b|\bTP\b|stop|target|session|\bBE\b|breakeven|trail" \
  CLAUDE.md core/firm_rules.py core/strategies/_archive/*/LOCK.md docs/methodology/ docs/adr/
2,516 hits. Decisive: docs/methodology/1r_estimation.md:77 —
"...graceStopMult=2.0 widens the stop to 2.0 x 1.55 x ATR for the first minBarsBeforeStop=1 bar
after entry (Guardian_Gold_v5.5_Strategy.pine:49,195-197)..." — confirmed tracked
(git ls-files docs/methodology/1r_estimation.md) and not gitignored (git check-ignore exits 1).

# Brief §10, Limb-B5 (coarse pre-check only — operator literal still owed):
$ git log --all -p | grep -EiC1 "(account[_ -]?(id|number)|balance|fill|P&L)[^\n]{0,40}[0-9]{4,}"
Voluminous, all research/methodology $ figures (no account-ID/fill-balance pattern). Inconclusive
by design — real test needs the withheld literal.

# Brief §10, Limb-D9 (executed + extended beyond the brief's own plan):
$ git log --all -- docs/notes/sentinel/queue.md            # 14 commits, e4ba36f..8199843
$ git merge-base --is-ancestor 19beee2 HEAD; echo exit=$?   # exit=1 (unreachable, confirmed)
$ grep -n "PREREG-RUNEDIT-\|PREREG-SAMECOMMIT-" STATE.md docs/SESSIONS.md docs/briefs/closures/*.md
  (zero hits — confirmed negative)
$ git show 19beee2:docs/notes/sentinel/queue.md             # SUCCEEDS — commit not gc'd
  Run 2026-08-10 Action section: 7 PREREG-RUNEDIT + 5 PREREG-SAMECOMMIT = 12 items (not 11)
$ git remote -v                                              # archive -> first-passage-archive.git
$ git for-each-ref --contains=19beee2 | wc -l                # dozens of refs/remotes/archive/* hits
$ git show archive/main:docs/notes/sentinel/queue.md         # identical 12-item Action state
$ git log -p d72e2b8..archive/main -- STATE.md docs/SESSIONS.md docs/briefs/closures/ \
    | grep -i "PREREG-RUNEDIT\|PREREG-SAMECOMMIT\|sentinel.*dispos"   # zero hits across ~140 commits

# Production-source re-verification (Section 0):
$ grep -n "^\*\*Status" docs/adr/2026-08-14-repo-public-visibility-transition.md
  -> Accepted, operator 2026-08-22 (brief's Section 0 said Proposed — now stale, see §4 above)
$ sed -n '56,57p' STATE.md   # confirms OPERATOR QUEUE still exactly 2 items
$ grep -rn "Locked config\|Reference backtest" core/strategies/_archive/*/LOCK.md   # headers present, bodies redacted, confirmed by direct read
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored — Phase 1 executed same session under operator GO | Claude Code (subagent) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-PUBTRANS-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-PUBTRANS-1-closure-falsified.md
```
