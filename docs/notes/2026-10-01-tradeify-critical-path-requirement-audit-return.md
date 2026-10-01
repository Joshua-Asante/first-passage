# Tradeify critical-path requirement audit — executor return (2026-10-01)

**Type:** generic
**Return state:** `NEEDS_CONTEXT`
**Verdict on §4's H:** not reached (the analysis stopped at §0)
**Card:** [2026-10-01 critical-path requirement audit](https://github.com/Joshua-Asante/first-passage/blob/0e31f2c7fd2363b0c1abe632313549948830cccf/docs/briefs/handoffs/2026-10-01-tradeify-critical-path-requirement-audit.md), frozen at dispatch revision `0e31f2c7fd2363b0c1abe632313549948830cccf` (head of `claude/critical-path-audit-card`, PR [#579](https://github.com/Joshua-Asante/first-passage/pull/579), unmerged)
**Seat:** worker. Dispatched by the operator on 2026-10-01 ("dispatch the audit card").

## §1 — Context and return summary

One of the card's premises is false at the dispatch revision and a second has drifted, so §2 steps 1–6 were not started. AGENTS.md and the dispatch instruction say to stop and return `NEEDS_CONTEXT` in that case, not to work around the problem.

1. **The T08 §7.10 route-path ruling is not in the owner record at the dispatch revision or on `origin/main`.** The card relies on it in §0, §0.5, §1, §5 and §10, and step 2 depends on it.
2. **The #570 packet has moved on from the revision the card pins.** The card's §1 defect statement, that #570 ranks D-MON/D-GO/D-REC/D-HIST as priorities 1–3, describes `9ff9318`. It does not describe the current PR head.

No owner record was edited. No private file was read. Nothing was run or measured, and no vendor, provider, account or host was contacted.

## §0 — Production reads

**Dispatch revision:** `0e31f2c7fd2363b0c1abe632313549948830cccf`. Its merge base with `origin/main` is `2b98d22bf14ea7268b3df682173a1dbff280b609`, which is the current `origin/main` head. The dispatch branch adds only the card (`0e31f2c`).

**Drift on `origin/main` after the dispatch revision:** none. Every input below is byte-identical at the dispatch revision and at `origin/main` (`git diff` is empty for each path).

| Input | Last-modified commit (dispatch = `origin/main`) | Present |
|---|---|---|
| `STATE.md` | `afa8c2c` 2026-10-01 | yes |
| `docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md` | `25816d2` 2026-10-01 | yes (it includes the 2026-09-27, 2026-09-28 and 2026-10-01 addenda) |
| `docs/briefs/handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md` | `56b7a64` 2026-09-29 | yes |
| `docs/briefs/handoffs/2026-09-24-tradeify-t00-p7-closure.md` | `4848189` 2026-09-26 | yes |
| `docs/notes/2026-09-29-t00-t10-cp7-sequence.md` | `b084cbc` 2026-09-29 | yes |
| `docs/briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md` | `4848189` 2026-09-26 | yes |
| `docs/notes/2026-09-27-feed-provider-neutral-preparation.md` | `4a94f9b` 2026-09-27 | yes |
| `docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md` | `4848189` 2026-09-26 | yes, but **it has no §7.10**. The file ends at §7.9. |
| `docs/superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md` | `4848189` 2026-09-26 | yes |
| `docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md` | `4a94f9b` 2026-09-27 | yes (§A8 is still Proposed) |
| `docs/briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md` | `4848189` 2026-09-26 | yes |
| `docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md` | `3880edd` 2026-10-01 | yes |
| `docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md` | `1d6ccb5` 2026-09-29 | yes |
| `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` | `4848189` 2026-09-26 | yes |
| `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` | `4848189` 2026-09-26 | yes |
| `docs/notes/2026-09-30-tradeify-simplification-decision-packet.md` | none | **absent** at both revisions. #570 is unmerged, so the card's fallback (PR head `9ff9318`) applies; see finding 2. |

## §4 — Hypothesis status and premise findings

The §4 hypothesis was not tested, because steps 1–6 were not run. The verdict is withheld: it is neither RESOLVED, FALSIFIED nor AMBIGUOUS.

### Finding 1 — the route-path ruling is not recorded in its owner (blocks step 2; premise of §0.5 and §5)

**What the card asserts.** §0 says to read "T08 §7.6–§7.10, including the 2026-10-01 route-path ruling (§7.10, Reading 1 …)". §0.5 says "The route path is ruled (T08 §7.10)". §1 says "The operator ruled the amendment path on 2026-10-01 (T08 §7.10)". §5 lists "the route path (T08 §7.10)" among the ruled decisions that must not be reopened.

**What the owner says at the dispatch revision and on `origin/main`.** [T08](../briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md) ends at §7.9, the 2026-09-25 support reply. Its last ruling on the route is §7.8 part 1: hold live release until the vendor question (b) or the amendment (a) settles. §7.9 leaves both open. A repository-wide `git grep` at the dispatch revision finds no 2026-10-01 route-path ruling and no "Reading 1" route text. The STATE decision index's newest entry is 2026-09-27, and it records no 2026-10-01 route ruling.

**Where the text exists.** It exists only on branch `ccr-fa571fe5-s624q4`, open PR [#575](https://github.com/Joshua-Asante/first-passage/pull/575) ("Record CrossTrade reply in STATE and the 2026-10-01 route-path ruling"), unmerged at head `aa20360a`. Two later commits on that PR (`1b5c2deb`, `aa20360a`) revised §7.10 after Codex P2 review, so its wording is still moving. Following the card's §0 instruction not to reconstruct an absent owner, this return does not adopt that text.

**Why this blocks rather than limits.** Step 2 schedules acceptance of the amendment "on the ruled path" and names when T09 becomes specifiable. The card's §10 hook "Reading 1 preserved" and the §5 no-reopen list test against that same ruling. Without a recorded ruling, the owner state is T08 §7.8: options (a) and (b) both open, and live release held. Step 2 would have to either assume the unmerged text (working around the gap) or treat the route path as open (contradicting the card). Steps 4 and 6 consume step 2, so they are blocked too.

### Finding 2 — #570 premise drift (affects the §1 defect statement and the §4 framing)

The card pins #570 at PR head `9ff9318` "if not merged". #570 is still open, but its head is now `c45237b`, which descends from `9ff9318` through `428b668` ("docs: prioritize T00 and route acceptance in deployment acceleration") and `c45237b` (Codex P2 folds). At `c45237b`, the packet's priority table is:

- **1A:** T00 / feed investment (GO-evidence path or a replacement D-feed gate)
- **1B:** route-amendment acceptance schedule, run in parallel
- **2:** E1/n3 decision value
- **Secondary:** D-MON, D-GO, D-REC and D-HIST

The defect in card §1 ("#570 ranks D-MON, D-GO, D-REC and D-HIST as priorities 1–3 … aimed at the wrong items first") is true of `9ff9318` and false of the current #570 head. The card and #570 now set out largely the same rescoping. This does not block on its own. It does change what the return is a decision aid *for*, and it makes card §1 a stale mirror of #570. Under §10 "Premise drift", it is recorded here for the coordinator.

### Other §0 observations (recorded, not acted on)

- The T00 → T10 → CP-7 note is present. The STATE 2026-09-24 decision-index entry carries the 2026-09-29 correction (D-feed (a) needs GO-evidence), consistent with the card's §1 item 1.
- The four-firm §4 falsifier is listed under STATE's 2026-11-08 forward triggers. It states that discharge needs its own dated re-MC (D-T00 condition 4, ruled 2026-09-23), consistent with the card's §1.
- The amendment scope's §5 steps 3–5 are unscheduled at the dispatch revision, as the card says. Step 2 (the T08 N1 map) is partly discharged by the 2026-09-25 operator attestation recorded in T08 §7.8.
- Card §0 says "Read these first, on `origin/main` at the dispatch revision". The dispatch revision is a branch head, not an `origin/main` commit. Because the two trees match for every input, this has no effect here.

## §5 — Constraints observed

This return is read-only. The text of #575 and #570 was read only to establish the drift. Neither is adopted as owner text. Observed constraints:

- One added file only. No owner record, gate, checkpoint or criterion was edited.
- No private read (Pine, ports, `local_artifacts/` or account data).
- No run, re-MC or measurement.
- No vendor, provider, Tradeify, account or host contact. No order action, deploy, arm or spend.
- No dispatch or carding of follow-on work.

## §6 — Return state and context needed

**Return state:** `NEEDS_CONTEXT`. **Verdict on H:** none of RESOLVED, FALSIFIED or AMBIGUOUS applies, because the hypothesis was untested. A premise of the card is false at the dispatch revision (Finding 1), and a pinned input has drifted (Finding 2).


Any one of the following resolves Finding 1. Choosing among them is the coordinator's or operator's decision, not the executor's:

1. **Merge #575**, or otherwise record the 2026-10-01 route-path ruling in T08 at a named revision. Then re-dispatch the card against a revision that contains it. Fold the Finding 2 drift into the re-dispatched card (re-pin #570 at `c45237b`, or at its merge commit, and restate §1's defect), so a second dispatch does not hit the same stale premise.
2. **Re-issue the card** with the route path stated as open under T08 §7.8 and §7.9, and step 2 rescoped to schedule both options (a) and (b).
3. **The operator states the ruling's owner revision explicitly** (for example, "#575 at `aa20360a` is the ruling of record for this audit"), accepting that it is unmerged.

Nothing in steps 1, 3 and 5 depends on Finding 1. If the coordinator prefers a partial return, a re-dispatch can scope those steps alone, but this executor did not run them under the current card.

## §10 — Audit hooks

The hooks were run on branch `claude/critical-path-audit-return`, cut from `origin/main@2b98d22`. The card file is not on this branch, so hook 1 was run in a detached worktree at `0e31f2c`. To re-run the hooks:

```bash
python -I scripts/fp.py python scripts/check_brief.py docs/notes/2026-10-01-tradeify-critical-path-requirement-audit-return.md
python scripts/check_md_relative_links.py | grep critical-path-requirement-audit || true
git diff --name-status origin/main...HEAD   # expect exactly one A docs/notes/... line
git diff --check
```

Results:

- `python -I scripts/fp.py python scripts/check_brief.py --type handoff <card>` exited 2: `fp: Operations virtual environment missing … /tmp/ops-env`. The cloud container has no operations environment. As a disclosed substitute, the same checker run under system `python3` returned `RESULT: well-formed` (0 HARD, 0 WARN). That substitute is not a launcher-recorded verification.
- `check_brief.py` on this return file (authority acceptance): the result is reported in the PR body.
- `check_md_relative_links.py | grep critical-path-requirement-audit`: the first run flagged this file's relative link to the card as dead, because the card is unmerged. The link now points to the card at the dispatch commit.
- `git diff --name-status origin/main...HEAD`: exactly one `A docs/notes/2026-10-01-tradeify-critical-path-requirement-audit-return.md`.
- `git diff --check`: clean.
- Premise drift: the 2026-10-01 continuation addendum and STATE queue item 1 are unchanged since the dispatch revision. #570 drifted (Finding 2).
- Savings claims: none made.
- Reading 1 preserved: not applicable. No route row was produced.
