# Claude handoff — Track A / A3: crash-loop recovery-path attestation

**Type:** cc_handoff (read-only verification + one governed note; operator attestation in-session)
**Date:** 2026-09-10
**Status:** dispatch after PR #332 and PR #334 are merged; must complete before A5
**Spawn target:** Claude Code (local session with `fly` auth and the private archive clone; operator present for one confirmation)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** read-only on Fly (`status`, `releases`, `image show`, `machine list`, `logs`); no deploy, no restart, no `ssh` writes. The private procedure is verified for **availability**, never reproduced.

## 0. Rule 0 reads (Phase 0 — report before writing the record)

Currency: `git fetch origin main`; record the SHA (authoring-time `47972f6`; #332 head `811df7c`). Hard check for `ops/c1_rail/m1_stage1_contract.py` on `origin/main`, else `NEEDS_CONTEXT`.

- `deploy/c1_rail/README.md` — the Status banner, the "A redeploy is not free… Pre-condition 4 is load-bearing" paragraph, and the "On first deploy the machine boots and **waits**" line (the public statement that the recovery path must be known before a deploy).
- `.claude/skills/c1-rail/SKILL.md` §Agent-session authority, deploy pre-condition 6 ("An expired `armed_until` makes the host refuse to boot, and `fly ssh` needs a booted machine, so a restart cannot fix it") — note that this sentence describes the **pre-fix** behaviour; verify against the code below and say so in the record.
- `ops/c1_rail/c1_rail_http_server.py::load_config` — the IMPLICIT DISARM block (in-memory disarm on expired/invalid `armed_until`; comment block dated to the 2026-07-31 incident). Then prove the **deployed** build has it, from the running bytes first: `MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "grep -n 'IMPLICIT DISARM' ops/c1_rail/c1_rail_http_server.py"` (read-only; the definitive evidence). Corroborate from history: `git show 31fd642:ops/c1_rail/c1_rail_http_server.py | grep -n "IMPLICIT DISARM"` — `31fd642` (2026-08-19) is a **public** commit, an ancestor of `origin/main` (`gh api repos/Joshua-Asante/first-passage/commits/31fd642` returns it), not archive lineage; if `git show` says `unable to read tree`, the clone is shallow — run `git fetch --unshallow origin` and retry. A shallow-clone failure is never evidence that the build lacks the fix; the in-container grep decides.
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — `code_commit_or_branch` (release v7, machine `e820221a657d28`, image `deployment-01M0DMFSFXVXEHZ27G8VYC0WQK`), the 2026-08-19 note ("the recovery sequence was pulled from history and reviewed before starting anyway, per precondition 6"), and the 2026-07-27 note (restart re-reads the volume config; disarm and restart are two separate actions).
- `docs/adr/2026-08-07-w6-rail-infra-closures.md` — Related line's RUNBOOK pointer (dead on the public tree by design) and §2 item 3 (prefer `c1_rail_arm.py` / `write_volume_config.py` over hand edits).
- `docs/ltm/README.md` and `docs/adr/2026-08-14-repo-public-visibility-transition.md` — archive retrieval guidance; `first-passage-archive` pins used across the repo resolve to `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2`.
- `docs/adr/2026-08-26-striker-legmap-cap-release.md` — the 69/11 → 0/0 release, so the record can state which allocation state is current and which is obsolete.
- Fly, read-only (paste the printed output): `fly releases -a c1-rail`, `fly status -a c1-rail`, `fly machine list -a c1-rail`, `fly image show -a c1-rail`, and the same four for `c1-signal-daemon`; `fly deploy --help | grep -n -- "--image"` (to confirm the no-build rollback form).
- Archive (read-only; confirm `git remote -v` shows the archive and that you never push): `git -C <archive-clone> show 5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2:docs/notes/rail_build/RUNBOOK.md | grep -n -i -E "^#+ .*(recover|self-brick|override|arming log|crash)"` — report heading lines and line numbers **only**.

## 0.5. Clarifications (halt on ambiguity)

- If the archive clone is absent on this machine, do not clone it inside this session by default; return `NEEDS_CONTEXT` naming the path the operator should provide. (Cloning is reversible but the archive was re-opened only to accept a preservation push; the operator decides.)
- If `fly image show` is unavailable in this flyctl version, derive the image reference from `fly status` and state the derivation.
- The operator's access confirmation is a sentence the operator says in-session after opening the procedure. If the operator is not present, complete every other section and return `NEEDS_CONTEXT` with the record otherwise finished.

## 1. Context and deliverable

The 2026-07-31 incident bricked the listener host: a lapsed `armed_until` with `dry_run=false` still on the volume made the boot gate raise, Fly stopped the machine at max restarts, and `fly ssh` could not reach a machine that never booted; recovery needed an entrypoint override. Main later reversed the boot gate to an in-memory implicit disarm. Track A will redeploy both apps; the public deploy guide requires knowing the recovery path first, and the packet requires a readiness record that establishes availability without publishing the procedure.

**Deliverable:** create `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md` (public, secret-free; later sub-tracks append §A4–§A8) with a header (date, owner, purpose, "this note authorizes nothing") and **§A3 — Recovery path** containing:

1. **Mitigation in code:** the implicit-disarm block exists on `origin/main` and in the deployed `31fd642` build (grep evidence both). State what it removes (the `armed_until`-lapse crash-loop class) and what it does not (config-missing → `WAIT` guard; `ModuleNotFoundError` at CMD → image rollback; anything else → the private procedure).
2. **Procedure availability:** repository, pinned SHA, path, and the heading list from the archive grep. No body text.
3. **Operator access confirmed:** date and the operator's own sentence, recorded only after it is said in-session.
4. **Current and rollback releases:** listener — release, machine id, image reference, source commit; daemon — the same (record that release v1 shows `failed` while the machine runs; A4 investigates, this section only names the image). The exact no-build rollback command for each app (`fly deploy --image <ref> --config deploy/<app>/fly.toml` or the form `fly deploy --help` confirms), and the pre-condition that a rollback is itself a deploy (six pre-conditions apply, host `--status` read first).
5. **Recovery cannot restore obsolete state:** recovery touches only `dry_run`/`armed_until` (via `c1_rail_arm.py --disarm` or the override) and never rewrites `c1_sizing_constants.json`, `lifecycle_state.json`, or the daemon journal; the 69/11 allocation is released doctrine, and any volume residue is handled only by A5's migration step, never by a recovery step; `dry_run=false` is never a recovery target.

**Not asked:** any deploy, restart, volume read beyond `--status`, or archive push; any edit to the private procedure; A4's checklist.

## 2. Execution plan

### Step 2.1 — Code evidence
Run the three greps — in-container on the deployed listener, on `origin/main`, and on `31fd642` (after `git fetch --unshallow origin` if the tree is unreadable); paste the matching line numbers. Gate: the in-container grep hits (decisive) and the two history greps corroborate. If the in-container grep does not hit, the deployed build predates the fix — record it as a NO-GO for A5 until A5's own deploy (which carries the fix) and say the recovery procedure is therefore load-bearing for A5's first boot.

### Step 2.2 — Fly read-only inventory
Run the read-only commands in §0; paste printed output (Windows `fly ssh` is not used here; these commands do not have the exit-code quirk). Gate: image references for both apps captured.

### Step 2.3 — Archive availability
Run the archive grep; record headings and line numbers. Gate: at least one heading matches; if none, widen to `grep -n -i "arming log"` and report honestly.

### Step 2.4 — Operator confirmation
Ask the operator to open the procedure and confirm in one sentence. Record date + sentence.

### Step 2.5 — Write the record and verify

```bash
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json   # untouched, exit 0
grep -n -i -E "netliq|token|secret|password" docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md   # expect no hits with values
git diff --stat origin/main...HEAD   # expect: the one new note
```

Commit on a `claude/*` branch, push, open a PR (Codex reviews; operator merges).

## 4. Falsifiable hypothesis

**H:** the deployed listener build contains the implicit-disarm boot path, the private procedure is reachable by the operator at the pinned SHA, and an exact no-build rollback command exists for both apps.
**Falsifier — reject if** any limb fails: if the in-container `grep 'IMPLICIT DISARM'` on the deployed listener is empty, then the deployed build lacks the mitigation and A5 is NO-GO until its own deploy (a shallow-clone `unable to read tree` on the `31fd642` corroboration is not this limb); if the archive grep returns no heading, then availability is unproven and A5/A6 are NO-GO; if `fly deploy --help` shows no `--image` form, then the rollback command must be re-derived before A5. **Accept if** all three limbs hold with pasted evidence. Either way the record is written. **Ambiguous** if the archive cannot be read from this machine → `NEEDS_CONTEXT`.

## 5. Forbidden moves

- Pasting any line of the private procedure, or paraphrasing its steps, into the public note — tempting because it would make the note "complete"; availability is the deliverable.
- Pushing to `first-passage-archive`, or cloning it without the operator's say-so.
- Any `fly deploy`, `fly machine restart`, `fly ssh` write, or reading the volume config (A4 owns those reads).
- Writing the operator's confirmation sentence yourself.
- Editing `deploy/c1_rail/README.md` to "fix" pre-condition 6's wording — flag the skew in the record for the parent instead.

## 6. Gate and return taxonomy

RESOLVED = §A3 complete with all five items evidenced. FALSIFIED = a limb of §4 failed (record written with NO-GO). AMBIGUOUS = archive unreadable or operator absent.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with branch, PR URL, and the two grep hit lines quoted.

## 7. Parent-session review

Pass 1 — spec compliance: one new file; no procedure content; no Fly writes in the transcript. Pass 2 — quality: the `31fd642` grep is real (parent re-runs it); image references match `fly status`; the rollback command form matches `fly deploy --help`; the "cannot restore obsolete state" section names the migration step as the only allocation writer.

## 10. Audit hooks

```bash
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "grep -n 'IMPLICIT DISARM' ops/c1_rail/c1_rail_http_server.py"
git show 31fd642:ops/c1_rail/c1_rail_http_server.py | grep -n "IMPLICIT DISARM"   # full-history clone; fetch --unshallow if needed
grep -n "^## §A3\|^## A3\|Operator access confirmed" docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md
fly status -a c1-rail | grep -n "Image"
fly status -a c1-signal-daemon | grep -n "Image"
```
