# Q-GATESTACK-1 — CLOSURE: `FALSIFIED` (both limbs reject)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-19
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-GATESTACK-1-verdict-preregistration.md`](../pre-registration/Q-GATESTACK-1-verdict-preregistration.md) — frozen 2026-08-19, same-session as Phase 1 (see that file's process note)
**Successor:** none authored — two packets named below per §6 `FALSIFIED` disposition; naming ≠ opening
**Spend / K:** $0 / K=0
**Live effect:** doc-correction successor packet executed same turn under explicit operator GO (see §3); branch-protection packet named, not opened
**Artifacts:** `docs/briefs/Q-GATESTACK-1-gate-stack-enforcement.md` (parent); this file; pre-registration above

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | Limb-A accepts AND Limb-D accepts | both rejected (below) | — |
| `FALSIFIED` | Limb-A rejects and/or Limb-D rejects | **both rejected** | ✓ |
| `AMBIGUOUS-HOLD` | a `gh` call errors or resolves ambiguously | no call errored; both resolved cleanly | — |

**Limb-A (branch protection) — REJECTS.** Ran `gh api repos/Joshua-Asante/first-passage/branches/main/protection` → `404 "Branch not protected"`. Ran `gh api repos/Joshua-Asante/first-passage/rulesets` → `[]`. Ran `gh api repos/Joshua-Asante/first-passage --jq .permissions,.private` → `{"admin":true,"maintain":true,"pull":true,"push":true,"triage":true}` / `false`. All three reject conditions hold simultaneously (404, empty ruleset set, `push:true` present for the queried identity). `main` is platform-unenforced.

**Limb-D (CI-status doc staleness) — REJECTS.** Ran `gh api repos/Joshua-Asante/first-passage/actions/permissions` → `{"enabled":true,"allowed_actions":"all",...}`. Ran `gh run list --workflow=manifest-check.yml --limit 10` → **10/10 `completed success`**, most recent 2026-08-20T02:12:13Z (today), earliest of the ten 2026-08-17T23:15:35Z — well past the 2026-08-15 threshold the reject condition names. Went one step further than the frozen hook: opened the most recent run's job list (`gh run view 32323796448 --json jobs`) and confirmed the `pine-pin-provenance` job specifically — the one `manifest-check.yml:82-88` and `post-merge:34-38` both describe as inert — genuinely executed and passed (`"name":"pine-pin-provenance","conclusion":"success"`, real start/end timestamps, not skipped). The docs' claim is not merely dated, it is actively wrong about current behavior.

---

## 2. What the pre-registration predicted vs what happened

Exact reproduction of the parent audit's (2026-08-18 assumption-sweep, findings A1/D7) informal finding — no surprises. The one thing this closure adds beyond that sweep: confirmation that the `pine-pin-provenance` **job**, not just the workflow wrapper, is live (the sweep and the parent brief's Rule-0 reads did not go to job-level granularity).

---

## 3. What this closure does NOT license

- Does **not** license reading live/green CI as a merge-blocking control — Limb-A independently rejects; CI passing and CI being *required* are separate facts, and this closure keeps them separate per the parent brief's §5 forbidden-move #2.
- Does **not** authorize branch-protection rules or a required-checks list for `main` — that is the named-not-opened successor packet #1, and repo-security-setting changes are outside what this session will make unilaterally regardless of operator GO on the doc-fix packet.
- Does **not** retroactively validate any `cursor/*` PR's test claims from the 07-06→08-14 dead-CI window (separate, larger finding from this session's earlier audit — not this brief's scope).

## 4. Defects found in the frozen brief (recorded, not repaired)

None. The parent brief's §4/§6 executed cleanly and mechanically against live data with no ambiguity requiring a judgment call outside the pre-registered branches.

## 5. Lesson candidates

Below the two-incident bar for a new named lesson — this is the second observed instance of the doc/live-state skew pattern already covered by `lesson_ratified_text_edited_alongside_authorized_change` and the existing `Q-GATESTACK-1` audit lineage (A1/D7). Watch, not a new entry.

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED` — both limbs reject.
- **Model update:** The repo's own account of its CI state was not merely stale by omission (an update that never landed) but actively describes current live behavior backward — a job the docs call "will not execute" ran and passed in the same session this closure was authored. "CI is format-only" and "Actions disabled repo-wide" are both false as of 2026-08-15 (public transition); real, multi-minute, genuinely-scored CI has run continuously since. Separately and independently, `main` carries zero platform enforcement — nothing about CI's revival makes it a gate.
- **Next:** `ITERATE`
- **Routing:** ITERATE → two dated successor packets, per §6:
  1. **Branch-protection/ruleset authoring for `main`** — named, **not opened**. Scope this against W5 ([`2026-08-07-w5-governance-diet.md`](../../adr/2026-08-07-w5-governance-diet.md) §2; CI `--tier check` landed 2026-08-23 — remaining debt is Limb-A required-checks, not job derivation) rather than duplicating it; needs its own operator GO — this is a repository security-setting change, handled separately from the doc-correction packet below.
  2. **Doc correction to `CLAUDE.md:218`, `.github/workflows/manifest-check.yml:82-88`, `scripts/githooks/post-merge:34-38`** — named **and opened** this same turn under operator GO ("close the loop, I ratify," 2026-08-19). Executed as a separate commit-worthy edit alongside this closure; see the blast-radius sweep run in the same session for the full file list touched.
- **Entry packet:** *(for successor #1 only, since #2 is being executed, not deferred)* — a future branch-protection packet must carry forward: the live Limb-A numbers above (404/`[]`/`push:true`), the W5 scope boundary (does not decide which of the 18 `scripts/gates.yml` entries become required checks — that's W5's question), and the constraint that CI passing ≠ merge-blocking until a ruleset actually exists.
- **Stop rule / re-proposal bar:** Re-open only when either (a) the operator authorizes the branch-protection packet with an explicit required-checks scope, or (b) a future audit finds the doc-correction packet's edits have drifted stale again (checkable via the same three `grep -n` hooks in §10 below, now pointed at corrected text).
- **Board write:** `docs/briefs/INDEX.md` Q-GATESTACK-1 row → `CLOSED — FALSIFIED` 2026-08-19, pointing here. (Written same commit as this file.)
- **Registry:** `n/a — governance/doc-accuracy finding, not a strategy-grounds kill; not a `rejected_candidates.md` object.`

## §10 audit-hook discharge

```
$ gh api repos/Joshua-Asante/first-passage/branches/main/protection
{"message":"Branch not protected","documentation_url":"...","status":"404"}

$ gh api repos/Joshua-Asante/first-passage/rulesets
[]

$ gh api repos/Joshua-Asante/first-passage --jq .permissions,.private
{"admin":true,"maintain":true,"pull":true,"push":true,"triage":true}
false

$ gh api repos/Joshua-Asante/first-passage/actions/permissions
{"enabled":true,"allowed_actions":"all","sha_pinning_required":false}

$ gh run list --repo Joshua-Asante/first-passage --workflow=manifest-check.yml --limit 10
[10 rows, all completed/success, 2026-08-17T23:15:35Z through 2026-08-20T02:12:13Z]
```

All hooks ran clean; none errored or needed `AMBIGUOUS-HOLD`.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Closure authored, both limbs run and scored | Joshua (GO) + Claude Code |
| 2026-08-19 | Addendum: successor packet #1 (branch-protection ruleset) opened and executed same day — `main-protection` ruleset id `21071355` created via `gh api repos/Joshua-Asante/first-passage/rulesets`: requires PR (0 approvals), blocks force-push/deletion, requires `skills (3.12)` status check, `current_user_can_bypass: never`. `pytest`/`build`/`manifest-check`/`validation-controls` deliberately NOT yet required — path-filtered on most workflows (would deadlock doc-only PRs) and `pytest (3.11)` is independently red on `main` right now (pre-existing, unrelated: `test_validate_c1_monitoring_acceptance.py::test_live_artifact_records_the_open_skew_rather_than_hiding_it`, `ops/c1_rail/c1_rail_arm.py` skew not named in the acceptance artifact's note — flagged as its own follow-up, not fixed here). Limb-A of this closure's own verdict is therefore stale as of this addendum — re-running `gh api .../branches/main/protection` today returns real enforcement, not 404. The `FALSIFIED` verdict itself stands unedited above per Trap #12; this addendum is the current-state pointer. | Joshua (GO: "no bypass" + "create it now") + Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md

# Reproduce the verdict
gh api repos/Joshua-Asante/first-passage/branches/main/protection   # expect 404
gh api repos/Joshua-Asante/first-passage/rulesets                    # expect []
gh api repos/Joshua-Asante/first-passage/actions/permissions         # expect enabled:true
gh run list --repo Joshua-Asante/first-passage --workflow=manifest-check.yml --limit 5
```
