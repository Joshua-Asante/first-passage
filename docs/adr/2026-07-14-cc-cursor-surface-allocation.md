# ADR — CC/Cursor surface allocation: CC designs and adjudicates, Cursor implements frozen specs

**Status:** Accepted (ratified 2026-07-14)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-14-cc-cursor-autonomous-loop.md` - narrows the "no commit/merge without operator go" return-contract line and the "Merging on green tests without CC/operator review" forbidden move to admit a binary auto-merge gate; the routing test, handoff contract, and locked-surface exclusions stand unchanged.
**Retain-until:** none
**Decision date:** 2026-07-14
**Authors:** Joshua + Claude Code
**Supersedes:** — (codifies existing practice; no prior ADR owns surface allocation)
**Related:** `docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md` (worked example of the handoff contract) | `.claude/skills/handoff-verify/SKILL.md` (consumer-side gate) | brief-authoring skill (producer-side templates)
**Layer:** infrastructure

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR (all anchors verified `git log -1 -- <path>` on 2026-07-14):

- `docs/operational_rules.md` — anchor `83ba1b2` (2026-07-12). Rule-maintenance clause read: new *operational rules* require a paid-for failure; this decision is therefore an ADR, not a Rule 13.
- `.claude/skills/handoff-verify/SKILL.md` — anchor `f133976` (2026-07-12). The consumer-side Phase-0 gate already exists and names "Cursor Phase-0 handoff" as a trigger.
- `docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md` — anchor `4d5704b` (2026-07-13). Read §0/§0.5/§1/§2 in full — the most mature Cursor handoff to date (7/7 `check_brief`; §0 read-report requirement; §0.5 halt-on-ambiguity with parent-recommended defaults; explicit forbidden moves; "No commit/merge without Joshua's go").
- `docs/SESSIONS.md` — anchor `b6e604a` (2026-07-14). Cursor-tagged entries read: 2026-07-13 survivor-scoring harness (15/15 tests green first pass, parallel with CC closing DISC-CAMP-0); 2026-07-13 Stage-4→7 drivers; 2026-07-12 Stage-7 realism engine + trackB; 2026-07-06 Cursor code-audit response (16-agent adversarial verification of external findings before acceptance).
- `CLAUDE.md` — anchor `b6e604a` (2026-07-14). §Methodology references (link-target surface for §6) and §Key Principle (locked-surface definition).
- `git log --oneline --all --since=2026-06-20` — division-of-labor evidence: `claude/*` branches author preregs/briefs/ADRs/closures and run adjudication; `cursor/*` branches (PRs #344, #348–350, #360, #364, #366–367) build harnesses/drivers from CC-authored handoff briefs.

**Explicitly non-load-bearing input:** a vendor-sourced CC-vs-Cursor performance comparison supplied in-session (Composer token-throughput figures, Merkle-tree indexing claims, speed tables). Treated as unverified marketing material per `verify-source` discipline. This ADR's grounds are the repo-observed evidence above; if every vendor claim were false, the decision would stand unchanged.

---

## §1 — Context

Since 2026-07-06 the repo has run a two-surface workflow without a written rule: Claude Code sessions (with the skill stack — Rule 0, brief-authoring, strategy-validation, verify-source, handoff-verify — plus persistent memory and doctrine context) author the pre-registrations, handoff briefs, ADRs, and closure adjudications; Cursor sessions execute frozen implementation specs on `cursor/*` branches and return PRs. The pattern has produced four clean lands in eight days (Stage-7 realism engine, trackB temporal-consistency, Stage-4→7 drivers, prop survivor-scoring harness — the last 15/15 tests green on first PR) and zero locked-surface incidents. The counter-pattern is also documented: external instruction packets confabulate repo state when not gated (`feedback_web_advisor_handoff_confabulates_repo_state`, multi-fire through 2026-07-11), which is why `handoff-verify` exists.

The allocation currently lives in operator habit and session precedent. Unwritten, it will drift under exactly the pressure the vendor comparison applies: "Cursor is faster, hand it more" — including, eventually, a judgment-heavy or locked-surface task where speed is the wrong criterion.

**Decision driver (one sentence):** the split is working and undocumented — codify it before a convenience-routed task crosses a locked surface or skips the handoff gate.

---

## §2 — Decision

**Decision:** Work is routed between surfaces by a three-question test, with an authored handoff brief as the mechanical eligibility gate for Cursor. CC designs, specifies, and adjudicates; Cursor implements frozen specs.

**Routing test (apply in order):**

0. **(Added 2026-07-16 addendum — RATIFIED 2026-07-16, see dated Addendum below.) Does Phase-0 reading require bytes or credentials not verifiably present in the dispatch environment?** Specifically: (a) any path under `core/data/tv_exports/**`, `core/data/bar_data/**`, `core/data/external/**` (gitignored vendor data — a cloud checkout has these only if manually staged there for *this* session), or (b) any API key/secret (e.g. the databento key). If yes and unconfirmed-present in the target surface → **local**, full stop, regardless of how questions 1–3 would resolve. See Addendum for the incidents that motivated this and the confirmed-present bar a handoff brief must clear to dispatch to cloud anyway.
1. **Does the task author doctrine or touch a locked/governed surface?** (ADRs, Pre-Qs, pre-registrations, closures, lifecycle state, `CLAUDE.md`/`STATE.md`/memory; any *edit* to `core/` anchor-path code — `dd_protection.py`, `firm_rules.py`, `portfolio_mc.py`, `core/mc/*`, `lifecycle.py`, `dd_geometry.py` — or Pine.) → **CC**, full stop. Read-only imports of `core/` from `lab/` code are fine on either surface.
2. **Is the spec frozen?** Binary acceptance gates, resolved ambiguities (§0.5-style defaults), enumerated forbidden moves, no judgment calls expected mid-build. If not → **CC** either does the work or freezes the spec first. Cursor never resolves a spec ambiguity unilaterally; it bounces `NEEDS_CONTEXT`.
3. **Does the build clear the handoff-overhead threshold?** Authoring + verifying a compliant brief costs a real fraction of a session. If the build is smaller than the brief (rule of thumb: < ~1 focused hour, or fewer than ~3 files touched), it stays on whichever surface is already open — default CC. Above threshold and spec-frozen → **Cursor**.

**Handoff contract (all four required for Cursor eligibility):**

- A handoff brief under `docs/briefs/**` passing `check_brief.py` (producer side: brief-authoring skill; the 2026-07-13 survivor-scoring brief is the reference example).
- §0 Phase-0 reads with a **read-report-before-code** requirement and `NEEDS_CONTEXT` bounce on any contradiction; Cursor runs the `handoff-verify` checklist as that Phase 0 (consumer side).
- §5 forbidden moves naming the locked surfaces the task runs near.
- Return contract: `cursor/*` branch, PR with tests green, **no commit/merge without operator go**; the PR is reviewed in a CC session under receiving-code-review discipline (or by the operator directly) before merge.
- **(Added 2026-07-16 addendum — RATIFIED 2026-07-16.)** §0 Phase-0 reads state explicitly whether any read touches a gitignored vendor-data path or a secret (test 0 above), and if so, name the confirmed-present staging/credential check performed for *this* dispatch — not a prior one, not a general belief the bytes/key exist "somewhere."

**Effective:** upon acceptance.
**Scope:** all task routing between Claude Code and Cursor on this repo. Other external surfaces (web advisors, claude.ai) keep their existing gates (`handoff-verify`, repo-context priming); this ADR does not re-govern them.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Route by "code vs docs" | Wrong axis both directions: a mechanical `SESSIONS.md` entry was successfully Cursor-handed (2026-07-12 brief), while `dd_geometry.py` — code — was correctly CC-built because it sits on a governed surface. Spec-completeness and surface-proximity predict outcomes; artifact type doesn't. |
| Everything stays in CC (status quo ante 2026-07) | Forfeits demonstrated parallel throughput: on 2026-07-13 Cursor built the survivor-scoring harness while CC closed DISC-CAMP-0 in the same window. Also spends CC context budget on mechanical TDD that a frozen spec fully determines. |
| Hand Cursor all implementation, including `core/` edits | Locked-surface edits carry Rule-0/anchor obligations (byte-identical-under-`ACTIVE_FIRM=FXIFY` proofs, MC pin regression, manifest gates) that are enforced by the CC skill stack and session doctrine. No incident yet precisely because this line hasn't been crossed; the ADR exists to keep it that way. |
| Adopt the vendor comparison as the routing rationale | Its claims are unverifiable marketing material (token throughput, indexing internals) and — decisively — they argue about *speed*, which is not the failure axis this repo cares about. The observed failure axis is spec-state confabulation and locked-surface discipline. Grounding doctrine in vendor claims violates `verify-source`. |
| Run a formal head-to-head benchmark before codifying | Cost without decision value: eight days of natural-experiment evidence already exists in git history, and the falsifier (§4) keeps collecting it for free. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger (either limb):**

1. **Allocation-caused defects:** over any rolling 8-week window, ≥2 merged Cursor-built PRs are found to carry defects traceable to *spec-interpretation judgment* (Cursor resolved an ambiguity instead of bouncing `NEEDS_CONTEXT`) rather than spec error. That is the exact failure class this allocation claims to contain; two instances mean the containment doesn't work.
2. **Overhead exceeds value:** ≥3 consecutive handoffs where authoring + verifying the brief demonstrably cost more session time than the gated build (operator-judged, logged in `SESSIONS.md`). The split is then net-negative for that task class.

**Revert action:** limb 1 → supersede with a tightened rule (narrower Cursor scope or mandatory CC re-verification of every Cursor diff hunk); limb 2 → carve the affected task class back into CC by superseding ADR — do not silently stop writing briefs.

**Trigger check schedule:** ride the standing 2026-08-08 review (already carries the lifecycle/regime/prop-program checks), then quarterly with it.

---

## §5 — Forbidden moves (under this ADR)

- **Verbal-spec handoffs** ("it's just a harness, I'll describe it in the Cursor chat") — genuinely tempting for mid-size tasks where the brief feels like ceremony; ruled out because the confabulation failure class is documented and multi-fire, and the brief *is* the containment.
- **Scope-creep via adjacency** — Cursor is in `lab/` and the fix "obviously" belongs three lines inside `core/mc/simulation.py`; ruled out — that edit re-routes to CC under test 1 regardless of size. The survivor-scoring brief's "landed inputs — call them, don't re-touch" line is the template.
- **Merging on green tests without CC/operator review** — tempting because Cursor's test suites have been clean; ruled out per receiving-code-review discipline (2026-07-06 session: external findings verified adversarially before acceptance — the same standard applies to external code).
- **Retro-fitting a brief after the build** to make the record compliant — self-attestation, same class as Rule 8 sub-rule 7's same-commit pre-registration.
- **Quoting the vendor comparison's numbers in future routing arguments** — if a speed claim matters to a future decision, measure it on this repo's tasks.

---

## §6 — Consequences

**Positive:**
- Parallel throughput becomes a rule, not a habit: CC session time concentrates on design, spec-freezing, and adjudication — the work the skill stack and memory actually differentiate.
- Cursor's demonstrated failure mode (acting on stale/confabulated repo state) stays contained by a gate that already exists and has fired correctly.

**Negative (real cost):**
- Brief-authoring overhead per handoff — the survivor-scoring brief is ~200 lines and took a real fraction of a session. Test 3 exists to keep this cost from being paid on tasks too small to amortize it.
- Two-surface coordination: worktree/branch hygiene load (already visible — repo-hygiene skill exists because of it).

**Risks:**
- Spec-freeze quality becomes a single point of failure: a wrong-but-frozen spec is executed faithfully and wrongly. Mitigation: §0.5 halt-on-ambiguity defaults + Cursor's standing license to bounce `NEEDS_CONTEXT` + CC-side PR review as the second look.
- The threshold heuristic in test 3 is a judgment call and will be argued at the margin; the falsifier's limb 2 is the pressure valve.

**Downstream artifacts (on acceptance):**
- `CLAUDE.md` §Methodology references — add one link line pointing here (routing rule discoverability; Rule 7: this ADR is the canonical owner, CLAUDE.md links).
- brief-authoring skill `references/cc_handoff.md` — flag (do not silently edit): the 2026-07-12/13 Cursor briefs added a §0.5 halt-on-ambiguity section the template lacks; per the skill's own "recent working example wins" rule, the template needs a Cursor-variant update through the skill-authoring path.
- `docs/SESSIONS.md` — session entry linking this ADR.

---

## §7 — Implementation plan

Mostly policy. Mechanical edits on acceptance only:

- **Phase 0** — re-verify §0 anchors at ratification time (`git log -1` on the five files).
- **Phase 1** — add the `CLAUDE.md` link line; append the SESSIONS entry.
- **Phase 2** — raise the cc_handoff-template §0.5 gap through the skill-authoring path (repo copy first, per `feedback_skill_amendments_via_authoring_path`).
- **Phase 3** — flip status to `Accepted` with a dated ratification note.

---

## §10 — Audit hooks (runnable)

```bash
# Every cursor/* merge since acceptance has a corresponding handoff brief:
git log --merges --oneline --since=2026-07-14 | grep -i "cursor/"
ls docs/briefs/handoffs/*cursor* docs/briefs/rnd-pipeline/*cursor* 2>/dev/null
# Expected: every merged cursor/* branch maps to a brief dated at or before its first commit.

# No Cursor-branch commit touches a locked surface:
git log --all --oneline --since=2026-07-14 --author=. --branches="cursor/*" -- core/dd_protection.py core/firm_rules.py core/portfolio_mc.py core/mc/ core/lifecycle.py core/dd_geometry.py
# Expected: empty.

# Brief compliance (run per new handoff):
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py <new-brief>.md --type cc_handoff

# §4 limb-1 evidence sweep (at each quarterly check):
grep -in "cursor" docs/SESSIONS.md | grep -in "defect\|redesign\|NEEDS_CONTEXT"
# Adjudicate hits against the two falsifier limbs; log the verdict in the review entry.
```

---

## Verification

```bash
# Discipline checks (mechanical)
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-14-cc-cursor-surface-allocation.md --type adr

# Production-source verification (Rule 0 confirmation)
git log -1 --format='%h %ci' -- docs/operational_rules.md .claude/skills/handoff-verify/SKILL.md docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md docs/SESSIONS.md CLAUDE.md
```

§6 downstream sweep executed at ratification (same commit): `CLAUDE.md` §Methodology references link added; `docs/SESSIONS.md` entry appended. `references/cc_handoff.md` §0.5 template gap remains an open follow-up (skill-authoring path, not a mechanical edit) — tracked here, not silently fixed.

---

## Addendum (2026-07-16, RATIFIED same day — operator chat directive "Step-0 cloud-dispatch addendum: ratify") — local-only dependency pre-check

**Trigger:** three cloud→local bounces in the 48h window 2026-07-15/16, each costing a full build→halt→local-continuation cycle (branch/worktree repackaging, not just a re-run):

- **Class-S C1 G0–G8 scoring** (07-15): cloud run → `NEEDS_CONTEXT` — gitignored CME CSVs (`15d8b`/`beabf`) absent from the cloud checkout; re-run locally on the same branch.
- **Class-S C1 regime-robustness rider** (07-15→16): same cause, same day — the session's own SESSIONS.md record notes "same gitignored absence as the first scoring cloud pass" — required a harness-PR/local-branch split (`#387` + `cursor/class-s-c1-regime-local-1713`) plus a later worktree repackage to land results.
- **H-OD-1 Stage-1/2** (07-16): Cursor cloud `BLOCKED — capability-problem` (no databento key in that environment) → ran locally.

**Root cause:** the three-question routing test asks about *surface* (locked/governed code, spec freeze, overhead threshold) but never asks about the *dispatch environment's contents*. `core/data/tv_exports/**`, `core/data/bar_data/**`, `core/data/external/**` are gitignored by standing policy (CLAUDE.md §Public-clone posture — personal export OK, redistribution not); a Cursor cloud checkout structurally cannot have those bytes unless someone staged them there by hand for that session, and that staging state doesn't transfer between cloud sessions or get verified before dispatch. The same blindness applies to secrets — a key being configured in Cursor Runtime Secrets for one project/session is not evidence it is present in the environment a specific dispatch runs in.

**Decision:** add routing-test **Step 0** (inserted into §2 above) and a 5th required handoff-contract item, both **binding as of ratification (2026-07-16)**. This closure targets a distinct failure class from the two named in §4 (judgment defects, overhead-exceeds-value) — dispatch-environment blindness, not spec quality — so it is handled here by addendum rather than by firing the existing falsifier.

**Downstream artifact (executed at ratification):** `.claude/skills/brief-authoring/references/cc_handoff.md` §0.75 "Local-only dependency check" block implements Step 0 (drafted same session as this addendum; its DRAFT marker flipped to ratified in the same commit as this ratification).

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-14 | Initial authoring | Joshua + Claude Code |
| 2026-07-14 | Ratified — status `Proposed` → `Accepted`; §6 downstream sweep executed (CLAUDE.md link, SESSIONS entry) | Joshua |
| 2026-07-16 | Addendum drafted (DRAFT — pending ratification) — routing-test Step 0 + handoff-contract 5th item, local-only dependency pre-check, after three cloud→local bounces in 48h | Claude Code (drafted at operator request, not yet ratified) |
| 2026-07-16 | Addendum RATIFIED — Step 0 + handoff-contract 5th item now binding; `cc_handoff.md` §0.75 marker flipped in the same commit | Joshua (chat directive: "Step-0 cloud-dispatch addendum: ratify") |
| 2026-08-14 | Addendum RATIFIED — see below (narrows §2 return-contract + §5 forbidden-move on merge) | Joshua (explicit ruling, in-session) |
| 2026-08-23 | Addendum RATIFIED — see below (automatic Claude judgment review on Cursor-first / opted-in PRs; review-only) | Joshua (chat: wire automatic Claude review on judgment-heavy PRs, especially Cursor-scoped) |
| 2026-08-29 | Addendum RATIFIED — see below (2026-08-23 addendum's automatic judgment-review request retargeted from Claude to Codex; review-only, same predicate) | Joshua (chat: "I have been having Cursor prompt Claudebot for reviews on PRs, this can go to Codex instead") |

---

## Addendum (2026-08-14, RATIFIED same day — operator ruling, in-session) — dispatch and merge narrowed by a sibling ADR

**Trigger:** operator direction to reduce manual involvement in CC/Cursor coordination, following a same-session incident (5 of 7 dispatch chips silently auto-dismissed before reaching the operator's UI, discovered only when the operator asked why they'd seen just two).

**What changes:** [`2026-08-14-cc-cursor-autonomous-loop.md`](2026-08-14-cc-cursor-autonomous-loop.md) supersedes-in-part two lines in this ADR:
- §2 return contract, "no commit/merge without operator go" → narrowed to *without operator go, unless the sibling ADR's binary auto-merge gate clears in full* (fable-judge `VERIFIED` exactly + full gate battery + full `pytest` + a mechanical forbidden-surface-path check + a compliant handoff brief).
- §5 forbidden move "Merging on green tests without CC/operator review" → narrowed the same way. "Green tests" alone was never sufficient even under the new ADR; the full gate requires an unambiguous adjudication verdict, not just passing CI.

**What does not change:** the §2 routing test (which tasks are Cursor-eligible at all, including the locked-surface exclusion) is untouched. The chip-approval step for *dispatch* also narrows under the sibling ADR (chips become the exception path, not the default), but that is a separate clause recorded there, not here — this addendum only tracks what the sibling ADR takes from *this* file's text.

**Why an addendum and not an edit:** per Rule 14 / Trap #12, this ADR's ratified body stays byte-unedited below this line. The narrowing is real and load-bearing, so it gets a proper cross-referenced record here, not silent supersession discoverable only from the other file.

---

<a id="addendum-2026-08-23-judgment-review"></a>

## Addendum (2026-08-23, RATIFIED same day — operator chat: wire automatic Claude review on judgment-heavy PRs) — review request, not merge

**Reads (before authoring):** `.github/workflows/claude.yml` `53a8968` (2026-08-23, `allowed_bots: "cursor"`; triggers only on comments/reviews/issues containing `@claude` — **not** on `pull_request` opened). This file `027a729` (public-clone seed; §2 return contract still says the PR is reviewed in a CC session). Sibling [`2026-08-14-cc-cursor-autonomous-loop.md`](2026-08-14-cc-cursor-autonomous-loop.md) `027a729` (auto-merge is a **separate** binary gate; this addendum does not touch it). Cheap falsifier: a Cursor-scoped judgment PR today gets a Claude look only if someone comments `@claude`.

**Trigger:** operator asked to wire an automatic Claude review request on PRs that need an extra level of judgment, especially when the work is scoped on Cursor first instead of in Claude Code. That is the exact gap the §2 return contract named ("reviewed in a CC session") and left as a manual mention.

**Routing note:** this addendum was implemented on a `cursor/*` branch at that same operator direction, with no CC-frozen handoff brief. That is a **one-packet exception** to §2 routing test 1 (doctrine → CC, full stop). It does not widen Cursor's doctrine-authoring eligibility. The mechanism installed here is the catch for the same class of PR going forward. Recorded because the first adjudication pass on this introducing PR named the violation (run `32672196619`).

**What changes:** a review-only GitHub Action requests a Claude adjudication pass when **all** of the following hold, implemented by `scripts/check_claude_judgment_review.py` + `.github/workflows/claude-judgment-review.yml`:

1. The PR is **not** a draft.
2. No prior `<!-- claude-judgment-review -->` comment exists (idempotent; re-review stays the existing `@claude` mention).
3. At least one opt-in matches:
   - label `claude-review`, or
   - body token `claude-review: judgment` (case-insensitive), or
   - head branch starts with `cursor/` **and** the diff touches a judgment surface (doctrine / governed `core/` / rail / skills / workflows — see the script's `JUDGMENT_*` lists).

Events: `opened`, `ready_for_review`, `reopened`, `labeled` (label must be `claude-review`). **Not** `synchronize`. `pull_request`, not `pull_request_target`. Never `*`. The request **posts `@claude`** (plus the marker) as `github-actions[bot]`; `claude.yml` on the **default branch** allow-lists `cursor,github-actions` and runs the review. That hop exists because a direct `pull_request` invocation of `anthropics/claude-code-action` **self-skips** on any PR that edits `.github/workflows/` (observed on this introducing PR, run `32672069340`: "workflow validation skip… will begin working once you merge"). Workflow diffs are themselves a judgment surface, so the mention path on `main` is the one that still fires.

**What does not change:**
- The §2 routing test (which tasks are Cursor-eligible) is untouched.
- The 2026-08-14 auto-merge gate is untouched. This addendum does not merge, does not green-wash CI, and does not satisfy gate (a) `fable-judge VERIFIED`.
- Tests-only / lab-harness `cursor/*` chores do not auto-fire.
- Human / `claude/*` PRs do not auto-fire unless labeled or body-tokened (CC is already in the room).
- No STATE queue row. No sixth root doc. $0.

**Forbidden:** treating a Claude review comment as merge authority; firing on every push; widening `allowed_bots` to `*`; using `pull_request_target`; auto-requesting on every `cursor/*` PR regardless of surface; invoking `claude-code-action` directly from the `pull_request` workflow (that path skips on workflow diffs).

---

<a id="addendum-2026-08-29-codex-judgment-review"></a>

## Addendum (2026-08-29, RATIFIED same day — operator chat: "I have been having Cursor prompt Claudebot for reviews on PRs, this can go to Codex instead") — auto-request retargeted from Claude to Codex

**Reads (before authoring):** this ADR `4f3ddc6` (2026-08-24, addendum above). `.github/workflows/claude-judgment-review.yml` (same anchor) — the two-hop `@claude`-mention dance and its stated cause (`claude-code-action` self-skips on `.github/workflows/` diffs). `scripts/check_claude_judgment_review.py` (same anchor) — the `JUDGMENT_*` opt-in predicate this addendum reuses unchanged. `.github/workflows/claude.yml` (same anchor) — `allowed_bots` and its `github-actions` rationale. `.github/workflows/notify-cursor.yml` (same anchor) — the `claude[bot]`-login match that pings `@cursor` once a review lands. `codex --help` / `codex exec review --help` / `codex login --help` run locally against the installed `@openai/codex` CLI (v0.151.0) — Codex has no GitHub-App mention listener analogous to `claude-code-action`; `codex exec review --base <branch>` is the non-interactive review primitive; auth is either a device-auth access token (`codex login --device-auth`, consumed via `--with-access-token`, drawing on a ChatGPT/Codex subscription) or an API key (`--with-api-key`, metered OpenAI API billing).

**Trigger:** operator directive to redirect the existing Cursor-PR auto-review-request mechanism (2026-08-23 addendum above) from Claude to Codex — a second, independently-trained reviewer is more likely to catch a blind spot Claude's own review shares, which is the whole point of a "second look."

**What changes:**

1. `scripts/check_codex_judgment_review.py` (renamed from `check_claude_judgment_review.py`, `git mv`, predicate logic byte-identical) — `LABEL` → `codex-review`, `BODY_TOKEN` → `codex-review: judgment`, `MARKER` → `<!-- codex-judgment-review -->`. The `JUDGMENT_EXACT` / `JUDGMENT_PREFIXES` / `JUDGMENT_SUFFIXES` opt-in surface is **unchanged** — same PRs qualify, only the reviewer changes.
2. `.github/workflows/codex-judgment-review.yml` (renamed from `claude-judgment-review.yml`) — same trigger events (`opened`, `ready_for_review`, `reopened`, `labeled` on label `codex-review`), same draft/marker/label/body-token gating. Where the old workflow **posted `@claude`** for `claude.yml` to pick up, this workflow installs the Codex CLI and runs `codex exec review --base origin/<base> --sandbox read-only` **directly in the same job**, then posts the last-message output as the PR comment (as `github-actions[bot]`, marker included for idempotency). The two-hop mention dance is dropped — it existed solely to work around `claude-code-action` self-skipping on `.github/workflows/` diffs, which does not apply to a plain CLI invocation.
3. Auth: `CODEX_ACCESS_TOKEN` repo secret (device-auth access token, `codex login --with-access-token`), mirroring `CLAUDE_CODE_OAUTH_TOKEN`'s subscription-draw design intent. The workflow's inline comments document the `OPENAI_API_KEY` / `--with-api-key` metered-billing alternative for whichever the operator's account actually supports. **Neither secret exists yet** — provisioning is an operator action (generate locally via `codex login --device-auth`, extract the token, add as a GitHub Actions secret) that cannot be completed from a repo-editing session. Until it is, the job fails at the "Authenticate Codex" step; this is a non-required check (`gate-manifest`'s `skills (3.12)` job is the only required one), so it does not block merges — but it also means **no live Codex review actually runs** until the secret lands.
4. `.github/workflows/notify-cursor.yml` — added an OR branch matching a `github-actions[bot]` comment containing the `<!-- codex-judgment-review -->` marker, so Cursor still gets pinged to address findings after a Codex review lands (it has no bot login to match the way `claude[bot]` does).
5. `.github/workflows/claude.yml` — `allowed_bots` narrowed from `cursor,github-actions` to `cursor`. `github-actions`'s sole cited purpose was posting `@claude` for the now-retargeted flow; grep confirms no other caller. Dropped rather than left as unused standing scope.

**Cost note (departs from the 2026-08-23 addendum's "$0"):** Claude's flow draws from the Claude Max/Pro subscription's included usage — genuinely $0 marginal. Codex's cost depends on which auth path the operator provisions: a device-auth access token draws on a ChatGPT/Codex subscription entitlement (the intended default here, matching "I have subscribed"); the documented `OPENAI_API_KEY` fallback is metered API billing, real dollars per review. Whichever is provisioned, this is **not** charted as $0 by default the way the Claude flow was — confirm the account's plan covers CI-volume `codex exec review` calls before relying on this at scale.

**What does not change:**
- The §2 routing test (which tasks are Cursor-eligible) is untouched.
- The 2026-08-14 auto-merge gate is untouched.
- The opt-in predicate surface (which PRs qualify) is untouched — only the reviewer and the transport.
- `claude.yml`'s manual `@claude`-mention capability for human/cursor commenters is untouched — this addendum only removes the `github-actions`-originated automatic mention, not the general listener.
- No STATE queue row. No sixth root doc. Not $0 (see above).

**Forbidden:** treating a Codex review comment as merge authority; firing on every push; widening `allowed_bots` back to include an unused bot or to `*`; using `pull_request_target`; auto-requesting on every `cursor/*` PR regardless of surface; committing an API key or access token to the repo instead of a GitHub Actions secret; letting `codex exec review` run outside `--sandbox read-only` in this job.

**Revert trigger:** either (1) `CODEX_ACCESS_TOKEN`/`OPENAI_API_KEY` remains unprovisioned past one full quarter (no live Codex review has ever run), or (2) a rolling 8-week window in which Codex's review comment is demonstrably lower-signal than Claude's on the same class of PR (operator-judged, logged in `SESSIONS.md`). Revert action: re-point `codex-judgment-review.yml`'s "Request review" step back to posting `@claude` (limb 1: no working alternative materialized) or restore `claude-judgment-review.yml` alongside it as a second, additive reviewer rather than a replacement (limb 2: Codex underperforms but is still worth keeping as a supplement).

**Revert trigger:** either (1) a tests-only `cursor/*` PR receives an automatic request, or (2) a `cursor/*` PR that edits `docs/adr/**` (non-draft, first look) does not. Both are mechanically checkable from the predicate tests + one live workflow run.
