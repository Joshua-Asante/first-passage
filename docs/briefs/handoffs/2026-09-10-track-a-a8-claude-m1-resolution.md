# Claude handoff — Track A / A8: operator signoff, `RESOLVED` artifact, listener redeploy — then STOP

**Type:** cc_handoff (multi-step; governed artifact edit + one listener redeploy under the 2026-08-02 grant)
**Date:** 2026-09-10
**Status:** dispatch only when A7 is DONE with a recorded listener event UUID and the operator is present to sign
**Spawn target:** Claude Code (local session with `fly` auth; clean checkout of `main`)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3
**Authority:** this session may flip the acceptance artifact to `RESOLVED` on the operator's signoff and redeploy the listener with it. **`RESOLVED` is not a GO.** `--arm` stays operator-only under a separate, later GO and is not run here under any wording.

## 0. Rule 0 reads (Phase 0 — report before any edit)

Currency: `git fetch origin main`; SHA recorded; tree clean. Hard checks: `ops/c1_rail/m1_stage1_contract.py` on main; readiness record §A7 present with a UUID, else `NEEDS_CONTEXT`.

- `scripts/validate_c1_monitoring_acceptance.py` — `RESOLVED_REQUIRED` (`fixture_hashes`, `dry_run_strategy_signal_event_id`, `sim_chain_ok_event_id`, `reconcile_verdict`, `notification_alert_id`, `notification_acked`, `drills`, `operator_signoff`), `REQUIRED_DRILLS`, the secret scanner (`_walk_secrets`: keys containing secret/token/password/bearer must be boolean or null — so the signoff object must not use such key names), `tree_skew`.
- `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — every field as it stands after A5; the notes discipline ("Do NOT set status=RESOLVED until … evidenced"; the 2026-07-28 entry explaining why a floored-to-zero event was deliberately left unset — the standard this event must clear).
- `ops/c1_rail/c1_rail_arm.py` — `m1_acceptance_reason` (validator with `require_resolved=True`; the in-image artifact is what the interlock reads), `describe_m1_gate` (`--status` output), `DEFAULT_ACCEPTANCE_PATH`.
- `deploy/c1_rail/Dockerfile` — the COPY of the acceptance JSON into the image ("when M1 flips to RESOLVED, arming requires a redeploy").
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` — §4 RESOLVED list (all 11), §6 maturity table, Addendum 2026-07-31b (gate object = the arm), Addendum 2026-08-24 ("Still owed after a recorded event id: `operator_signoff`").
- `docs/notes/rail_build/M1_STAGE1_DEPLOYMENT_READINESS.md` §A5–§A7 — the deployed pins, the UUID, the projection fields, the ratified source-qualification wording from A1.
- `STATE.md` queue row 1 and the decision-index conventions; `docs/SESSIONS.md` header (a full entry is owed only for a judgment call — the parent decides whether this session writes one).
- `.claude/skills/c1-rail/SKILL.md` §Agent-session authority — six pre-conditions for the redeploy.

## 0.5. Clarifications (halt on ambiguity)

- The signoff is the operator's sentence, said or typed in-session, with their name and the UTC date. The agent records it verbatim under `operator_signoff` as `{"operator": "...", "date": "...", "statement": "...", "event_id": "<uuid>"}` — key names chosen so the secret scanner is not tripped. If the operator is absent, complete everything except the signoff and `status`, and return `NEEDS_CONTEXT`.
- If the ratified A1 amendment says the event certifies the chain but **not** live-feed readiness, the notes entry says exactly that; `status=RESOLVED` is still correct because item 5's limbs are about origin, sizing, and dry-run, not feed readiness. If the amendment says the event does not qualify for item 5, this session does not flip the status and returns `BLOCKED — plan-itself-wrong`.
- If the A7 UUID does not resolve to exactly three ledger lines on the host, stop.

## 1. Context and deliverable

A7 produced the item-5 event. The validator requires both the genuine event id and an operator signoff for `RESOLVED`; the arming interlock reads the artifact **baked into the listener image**, so a redeploy is the only way the host learns the new status. This session lands the artifact, redeploys the listener disarmed, verifies the gate reads `PASS`, and stops. M1 complete; the book is still not ready to trade and nothing here says otherwise.

**Deliverables:** (1) PR 1 — acceptance JSON with the three owed changes + notes entry; (2) listener redeployed from the merge SHA of PR 1, disarmed, `--status` → `m1_gate: status='RESOLVED' result=PASS`; (3) PR 2 — deploy record (`fixture_hashes` refreshed, `code_commit_or_branch`, `fixture_hashes_note` entry, readiness §A8, STATE row 1 leaves the queue with its record link); (3b) only if a pin moved at (2): one docs-only re-bake redeploy after PR 2 merges, ops bytes unchanged, plus a notes-only PR 3 with its release; (4) STOP.

**Not asked:** arming; changing any drill or evidence field; touching the daemon; a lifecycle or allocation change; declaring anything about strategy readiness.

## 2. Execution plan

### Step 2.1 — Re-verify the event on the host
`grep -c <uuid> /data/c1_rail_events.jsonl` in-container → 3; print the `decision` line's fields (`qty_out` 1, `halt` false, `dry_run` true, `test_only` true, `sender_invoked` false, `leg_id` `m1_stage1_test`) and the `transport_result` (`not_attempted`). Gate: all match §A7.

### Step 2.2 — Edit the artifact (repo, `claude/*` branch)
- `dry_run_strategy_signal_event_id`: the UUID.
- `operator_signoff`: the object from §0.5, verbatim from the operator.
- `status`: `RESOLVED`.
- `notes[]`: a dated entry — item 5 discharged by the A7 event (ceremony id, target minute, contract hash, `qty_out=1`, sender never invoked, rail `dry_run=true` throughout), what the ratified A1 amendment says it certifies and leaves open, the signoff date, and the sentence "RESOLVED is the arm-gate's precondition, not an arm; `dry_run=false` still requires a separate operator GO."
- Leave `fixture_hashes`, `drills`, `drill_evidence`, `sim_chain_ok_event_id`, `notification_*` untouched in this PR (`fixture_hashes` changes only in PR 2, from the Step 2.3 reads).
- Run: `python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (exit 0) and `… --require-resolved` (exit 0). Then the local gate simulation: `python ops/c1_rail/c1_rail_arm.py --status --config deploy/c1_rail/c1_rail_config.fly.example.json --acceptance docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` → `m1_gate: status='RESOLVED' result=PASS` (the example config is disarmed and secret-free; `--status` writes nothing).
- Commit, push, open PR 1 (Codex reviews; operator merges).

### Step 2.3 — Redeploy the listener (six pre-conditions)
After PR 1 merges: host `--status` read (`dry_run=True`, `armed_until=None`; anything else is the armed-host procedure in Track A plan §6 and the deploy does not happen); checkout `main` at the merge SHA, clean; `pytest tests/ops/test_c1_rail_image_manifest.py -q`; pre-deploy in-container hashes equal the A5 pins (the running build is still A5's); `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile`; boot line `dry_run=True armed_until=-`; health ok; in-container `--status` → `m1_gate: status='RESOLVED' result=PASS`; post-deploy `sha256sum` in `/app` of every pinned file the image carries (the `ops/c1_rail/*.py` and `scripts/` pins — `tests/ops/test_m1_acceptance_drills.py` is not COPYed, so that pin is re-verified from the checked-out merge-SHA tree exactly as A5 did) plus `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json`. Compare each pin to its A5 value: a file whose hash moved must have at least one commit in `git log <A5 deployed SHA>..<PR 1 merge SHA> -- <path>` that explains it — A1b legitimately changes `ops/c1_rail/m1_stage1_contract.py` (the source marker) and may change `ops/c1_rail/m1_stage1_control.py`, and those files are COPYed into the listener image — while any pin that moved with no explaining commit means the image is not what main describes: roll back to the A5 image and return `FALSIFIED`. Do not require "unchanged"; require "explained". The refreshed in-container values are what PR 2 records.

### Step 2.4 — Deploy record (PR 2)
`fixture_hashes` → the Step 2.3 values (deployed pins from in-container reads, the test pin from the tree; moved pins carried with their explaining commits; unmoved pins re-read, never assumed); `code_commit_or_branch` → the PR 1 merge SHA as the commit whose ops bytes are running, plus release/machine/image — and, when any pin moved, the sentence "this record is re-baked into the image by a docs-only redeploy from the PR 2 merge commit (ops bytes unchanged); the final release is recorded in readiness §A8"; `fixture_hashes_note` dated entry naming which pins moved, the commits that explain each, the artifact's own hash, and that the in-image status is now `RESOLVED`; readiness §A8; `STATE.md`: row 1 leaves the queue, decision index gains the dated consequence with the record link; the parent decides on a `SESSIONS.md` entry. Validator plain + `--require-resolved` exit 0; `--check-tree-skew` output pasted. Commit, push, PR 2.

### Step 2.4b — Re-bake the record (only if a pin moved in Step 2.3)
The arming interlock reads the artifact **baked into the image**, and `m1_acceptance_reason()` validates it structurally without comparing its pins to the running bytes. After Step 2.3 the running image carries PR 1's artifact, whose `fixture_hashes` are the A5 values; if A1b moved any listener pin, that embedded record describes a different image than the one running while reading `PASS`. So, after PR 2 merges: the six pre-conditions again (host `--status` read; clean checkout of `main` at the PR 2 merge SHA; image-manifest test; pre-deploy in-container hashes equal PR 2's `fixture_hashes` exactly — the ops bytes did not change); `fly deploy …`; boot line `dry_run=True armed_until=-`; health; in-container `--status` → `m1_gate: status='RESOLVED' result=PASS`; post-deploy in-container hashes **identical** to the pre-deploy ones (only the JSON changed) and the in-image JSON's own sha256 equals the repo file's. Record the release/machine/image in readiness §A8 via a notes-only PR 3 — no further deploy, because the JSON is not in its own pin set and the running record now describes its own bytes. If no pin moved in Step 2.3, skip this step: the baked pins already describe the running image.

### Step 2.5 — Stop
Final `--status` pasted: `dry_run=True armed_until=None … m1_gate: status='RESOLVED' result=PASS`. No arm.

## 4. Falsifiable hypothesis

**H:** the A7 event satisfies item 5 as the ADR and its 2026-08-24 addendum define it, the artifact with the owed fields validates under `--require-resolved`, and the redeployed listener's in-image gate reads `PASS` while the host stays disarmed.
**Reject** if the validator fails, if the in-image `--status` does not read `PASS` after the redeploy, if a pinned file's in-container hash moved with no explaining commit between the A5 deploy SHA and the PR 1 merge SHA, or if the host is anything but disarmed → `FALSIFIED`; do not edit the validator or the gate to make it pass. **Ambiguous** if the amendment's qualification wording is contested → `NEEDS_CONTEXT`.

## 5. Forbidden moves

- `--arm`, `--acknowledge-m1-unresolved`, or any config edit beyond what `fly deploy` does — tempting exactly now, and exactly forbidden: `RESOLVED` is one of two conditions, the other is a separate GO.
- Populating the event field with any id but the A7 UUID (the 2026-07-28 floored event, a fabricated id, the SIM chain id).
- Editing `drills`, `drill_evidence`, `sim_chain_ok_event_id`, or `notification_*` values at any point.
- Editing `fixture_hashes` in PR 1 (no deploy has happened yet; PR 1 changes only the three owed fields plus notes). PR 2 is the only place they change, and only to the Step 2.3 values.
- Loosening the validator, the secret scanner, or `m1_acceptance_reason`.
- Claiming live-feed readiness, strategy readiness, or deployment authority in the notes.
- Refreshing any image-carried pin from tree bytes (the non-image `tests/ops/test_m1_acceptance_drills.py` pin is verified from the merge-SHA tree by design).

## 6. Gate and return taxonomy

RESOLVED = both PRs open/merged as described, in-image gate `PASS`, host disarmed. FALSIFIED = §4 reject. AMBIGUOUS = signoff or qualification missing.

Return exactly one of `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`, with PR 1 and PR 2 URLs, the merge SHA, release number, image ref, and the final `--status` line.

## 7. Parent-session review

Pass 1 — spec compliance: JSON diff touches only the three owed fields plus notes; no drill/evidence edits; no arm command anywhere in the transcript. Pass 2 — quality: parent re-runs both validator forms and the in-container `--status`; the notes entry's qualification sentence matches the ratified A1 amendment word for word. Pass 3 — consolidated read of §A5–§A8 and the whole acceptance JSON.

## 10. Audit hooks

```bash
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved
MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "python ops/c1_rail/c1_rail_arm.py --status"
git log --oneline -3 -- docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
grep -n "B7-REFIRE Stage 1 + M1" STATE.md   # expect: gone from the queue, present in the decision index
```
