# Q-GATESTACK-1 — Does anything on GitHub actually require the declared gate stack to pass before code lands on main, and are the docs describing CI status current?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the 2026-08-18 assumption-sweep audit note, findings A1 and D7
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on live re-confirmation that `main` is GitHub-platform-enforced and that the CI-status claims in governing docs match the live Actions state
**Artifact path:** `docs/briefs/Q-GATESTACK-1-gate-stack-enforcement.md`

---

## Section 0 — Rule 0 reads (production-source verification)

- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md:80-82,142,195-197,217-219` — source audit note; findings A1 and D7 with their `gh api` cheap-falsifier hooks. Anchor: working-tree, not yet committed as of 2026-08-18 (`git status --porcelain` shows `??`) — this brief transcribes it in place, no separate re-derivation.
- `CLAUDE.md:218` — *"CI is **format-only** and cannot re-hash gitignored bytes"* — anchor `d88e5f2` (`git log -1 -- CLAUDE.md` on 2026-08-18, dated 2026-08-15).
- `CLAUDE.md:211-225` — *"Load-bearing gate — install the pre-commit hook once per clone"* and the "Gate composition authority" section naming `scripts/gates.yml` as the 18-gate roster — same anchor `d88e5f2`.
- `.github/workflows/manifest-check.yml:82-88` — *"INERT AS SHIPPED: GitHub Actions is disabled repo-wide (verified 2026-07-31 — actions/permissions {"enabled":false}; no workflow run since 2026-07-16)"* — anchor `027a729` (`git log -1` on 2026-08-18, dated 2026-08-14). Confirmed present verbatim on direct read this session.
- `scripts/githooks/post-merge:34-38` — *"the PR job added alongside it is inert while GitHub Actions is disabled repo-wide (verified 2026-07-31: actions/permissions {"enabled":false}; no run since 2026-07-16)"* — anchor `027a729`, same commit as the workflow file. Confirmed present verbatim on direct read this session.
- `scripts/gates.yml` — anchor `d48f7de` (`git log -1` on 2026-08-18, dated 2026-08-17). Confirmed `18` gate entries (`grep -c "^\s*-\s*id:"`) this session, matching the audit note's "all 18 declared gates" claim.
- `docs/adr/2026-08-07-w5-governance-diet.md` §2 — named by CLAUDE.md's gate-composition section as owning the still-open "deriving CI jobs from the gate manifest" item; scope boundary for this Q (see §2 below).

---

## Section 1 — Context and motivation

The 2026-08-18 assumption-sweep audit (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`) surfaced two findings that share one load-bearing precondition: **A1** — `main` returns 404-unprotected and `[]`-ruleset from the GitHub API, with the owner token carrying `push:true` — and **D7** — three canonical documents (`CLAUDE.md`, `manifest-check.yml`, `post-merge`) assert GitHub Actions is disabled repo-wide, a claim the audit found false since the 2026-08-15 public release. Both findings were independently re-confirmed live during the sweep session. Standing doctrine this tests: CLAUDE.md's own "Gate composition authority" section, which names `scripts/gates.yml` as the single source of gate truth and explicitly forbids a hand-maintained parallel list — a claim that presupposes something actually enforces the roster before merge.

---

## Section 2 — Prior art / lineage

- Source: `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` §4 (A1, Tier A; D7, Tier D) and §9 (aggregated audit hooks, reused verbatim below).
- **Adjacent, deliberately excluded scope** — the audit's own §3 D-gate deletions #2 and #3 already cover "CI never derives its jobs from `gates.yml`" and "`sessions-order`/`sessions-append-only` have no CI mirror," both citing `docs/adr/2026-08-07-w5-governance-diet.md` §2 as the owning, already-tracked open item. This Q does **not** re-open that scope — it asks only whether *anything on GitHub* is a required gate today, and whether the docs describing Actions' on/off state are accurate. Whether the 18 gates get CI jobs at all is W5's question, not this one.
- **Adjacent, deliberately excluded scope** — the audit's §4 finding B5 (public-visibility ADR Status field stuck at `Proposed`) and §7's documentation-drift observation group B5/D7/D10 as one pattern (canonical docs accreting corrections elsewhere without being patched). This Q covers only the CI-status claim (D7) and its branch-protection precondition (A1); the ADR Status field itself is not this Q's object.
- No prior Q-slug in `docs/briefs/INDEX.md` touches branch protection or Actions-enablement status — this is a first opening on this surface.

---

## Section 3 — Question (Q-GATESTACK-1)

**Q-GATESTACK-1:** Is there any GitHub-platform mechanism that currently blocks a merge to `main` from bypassing the declared gate stack, and do the repo's own claims about CI's on/off state match what GitHub reports live?

(Symptom-only: names what's missing/wrong — a platform control, a doc's accuracy — without prescribing branch-protection rules, a required-checks list, or a doc edit.)

---

## Section 4 — Falsifiable hypothesis (H-GATESTACK)

**H-GATESTACK:** If **Limb-A** (`gh api .../branches/main/protection` returns a non-404 result naming ≥1 required status check or required review, AND `gh api .../rulesets` returns a non-empty ruleset enforcing on `main`, AND `push:true` is absent for the pushing identity) holds, **AND** **Limb-D** (`gh api .../actions/permissions` and `gh run list --workflow=manifest-check.yml` match the "disabled repo-wide / `enabled:false` / no runs since 2026-07-16" claims verbatim in `CLAUDE.md:218`, `manifest-check.yml:82-88`, `post-merge:34-38`) holds, then the gate-stack claim is backed by a live platform control and the docs describing it are current. **Otherwise**, whichever limb's re-check reproduces the audit's finding names a real gap: an unenforced `main` (Limb-A) and/or a stale "CI can't do anything yet" story that is actively masking Limb-A behind an obsolete frame (Limb-D).

**Reject H-GATESTACK if:** Limb-A re-check returns 404/`[]`/`push:true`-present (main still platform-unenforced) **and/or** Limb-D re-check returns `enabled:true` with ≥1 `success` run on `manifest-check.yml` since 2026-08-15 (docs stale) — either sub-condition alone rejects the corresponding limb; overall verdict is `FALSIFIED` if either or both limbs reject.

**Accept H-GATESTACK if:** Limb-A returns a non-404/non-empty result naming a required check **and** Limb-D's live state matches the "disabled" doc claims verbatim — both limbs must accept for `RESOLVED`.

**Ambiguous-hold if:** a `gh api`/`gh run list` call returns an auth/rate-limit error, an org-policy redirect, or an intermediate state the cheap falsifier cannot mechanically resolve (e.g., a ruleset present but not targeting `main`, or an `actions/permissions` response scoped differently than expected) without operator-level GitHub admin access.

---

## Section 5 — Forbidden moves

- **Treating "pre-commit is opt-in but load-bearing" as sufficient without naming the bypass channels.** Tempting because CLAUDE.md already documents the install step and frames it as "Load-bearing gate" — reads like the gate exists. Ruled out: per-clone opt-in is bypassable by design via a direct push, an admin merge with red checks, or a GitHub-web-UI merge, none of which ever touch a local hook — naming this explicitly is the whole point of Limb-A, not a footnote to skip.
- **Reading a live "Actions enabled, runs green" state as itself proof of an enforced gate.** Tempting because green checks visually resemble protection. Ruled out: CLAUDE.md's own "Gate composition authority" doctrine calls CI **advisory-only** — conflating green CI with a merge-blocking control would launder D7's exact finding (docs overstate/understate CI's role) into a false comfort in the opposite direction. Limb-A and Limb-D are scored independently for this reason.
- **Proposing or landing a specific branch-protection ruleset, required-checks list, or doc correction under this brief.** Tempting because the fix looks small once the gap is confirmed. Ruled out by the Section 3 symptom-only test (this Q names the gap, not the remedy) and by scope: which of the 18 `gates.yml` entries would even become required-status-checks is undecided territory already owned by the open W5 item (`docs/adr/2026-08-07-w5-governance-diet.md` §2, named in the audit's §3 D-gate deletion #2/#3) — writing protection rules here would silently annex that scope.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb-A accepts (main platform-enforced) AND Limb-D accepts (CI-status docs match live state) | `INTEGRATE` — record both claims as evidence-ratified; discharge A1/D7 in the audit note's own routing table. No config or doc changes made under this brief. |
| `FALSIFIED` | Limb-A rejects and/or Limb-D rejects (reproduces the audit's 404/`[]`/`push:true` state and/or `enabled:true`-with-green-runs state) | `ITERATE` — name (do not open) two successor decision packets: (1) branch-protection/ruleset authoring for `main`, scoped against the still-open W5 CI-derivation item rather than duplicating it; (2) a doc correction to `CLAUDE.md:218`, `manifest-check.yml:82-88`, `post-merge:34-38` flipping the "disabled" claim. Operator GO required for either. |
| `AMBIGUOUS-HOLD` | A `gh` call returns an auth/rate-limit/scope error, or an intermediate state neither limb's binary test can resolve at $0 | `ITERATE` — re-test when operator-level GitHub admin access is available to disambiguate; re-test window: next M1/c1-rail-adjacent session or next quarterly methodology audit, whichever comes first. |

**Pre-registered before any `gh` call runs under this brief.** Not amended mid-check to match what the call returns.

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — Limb-A (branch protection).**
  ```bash
  gh api repos/Joshua-Asante/first-passage/branches/main/protection
  gh api repos/Joshua-Asante/first-passage/rulesets
  gh api repos/Joshua-Asante/first-passage --jq .permissions,.private
  ```
- **Phase 1 — Limb-D (CI-enabled staleness).**
  ```bash
  gh api repos/Joshua-Asante/first-passage/actions/permissions
  gh run list --workflow=manifest-check.yml --limit 10
  ```
- **Phase 2 — Verdict assertion.** Apply Section 6 mechanically against the Phase 1 output; produce the closure artifact per Section 9.

No additional spend, backtests, or data pulls — this is the entire execution plan, and both phases were already run once, live, inside the audit-note sweep session (2026-08-18); Phase 1 here is the formal same-question reproducibility check that promotes that sweep-session observation to a closed Q verdict.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, to be committed to `docs/briefs/pre-registration/Q-GATESTACK-1-verdict-preregistration.md` **before** Phase 1 runs under this brief's own authority (as distinct from the audit sweep's prior informal run, which predates and cannot substitute for this pre-registration). Not yet authored — this Q is named, not opened.

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-GATESTACK-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md` (no `recommendation.md` — the fix packets are named, not opened, per Section 6); `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named.

---

## Section 10 — Audit hooks (runnable)

```bash
# Limb A — branch protection
gh api repos/Joshua-Asante/first-passage/branches/main/protection
gh api repos/Joshua-Asante/first-passage/rulesets
gh api repos/Joshua-Asante/first-passage --jq .permissions,.private

# Limb D — CI-enabled staleness
gh api repos/Joshua-Asante/first-passage/actions/permissions
gh run list --workflow=manifest-check.yml --limit 10
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/briefs/Q-GATESTACK-1-gate-stack-enforcement.md --type inquire
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation)
$ git log -1 -- CLAUDE.md                                    # expect d88e5f2, 2026-08-15
$ git log -1 -- .github/workflows/manifest-check.yml          # expect 027a729, 2026-08-14
$ git log -1 -- scripts/githooks/post-merge                   # expect 027a729, 2026-08-14
$ git log -1 -- scripts/gates.yml                              # expect d48f7de, 2026-08-17
$ grep -n "format-only" CLAUDE.md                               # expect :218
$ grep -n "INERT AS SHIPPED" .github/workflows/manifest-check.yml   # expect :82
$ grep -n "disabled repo-wide" scripts/githooks/post-merge      # expect :34-38 region
$ grep -c "^\s*-\s*id:" scripts/gates.yml                       # expect 18

# Cross-reference verification (source audit note still holds the cited findings)
$ grep -n "^\*\*A1\." docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md
$ grep -n "^\*\*D7\." docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md
```

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [ ] Section 8 pre-registration owed at operator GO — not yet authored
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened
