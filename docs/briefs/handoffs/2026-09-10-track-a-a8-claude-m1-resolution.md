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

**Deliverables:** (1) PR 1 — acceptance JSON with the three owed changes + notes entry; (2) listener redeployed from the merge SHA of PR 1, disarmed, `--status` → `m1_gate: status='RESOLVED' result=PASS`; (3) PR 2 — deploy record (`code_commit_or_branch`, `fixture_hashes_note` entry, readiness §A8, STATE row 1 leaves the queue with its record link); (4) STOP.

**Not asked:** arming; changing any drill or evidence field; touching the daemon; a lifecycle or allocation change; declaring anything about strategy readiness.

## 2. Execution plan

### Step 2.1 — Re-verify the event on the host
`grep -c <uuid> /data/c1_rail_events.jsonl` in-container → 3; print the `decision` line's fields (`qty_out` 1, `halt` false, `dry_run` true, `test_only` true, `sender_invoked` false, `leg_id` `m1_stage1_test`) and the `transport_result` (`not_attempted`). Gate: all match §A7.

### Step 2.2 — Edit the artifact (repo, `claude/*` branch)
- `dry_run_strategy_signal_event_id`: the UUID.
- `operator_signoff`: the object from §0.5, verbatim from the operator.
- `status`: `RESOLVED`.
- `notes[]`: a dated entry — item 5 discharged by the A7 event (ceremony id, target minute, contract hash, `qty_out=1`, sender never invoked, rail `dry_run=true` throughout), what the ratified A1 amendment says it certifies and leaves open, the signoff date, and the sentence "RESOLVED is the arm-gate's precondition, not an arm; `dry_run=false` still requires a separate operator GO."
- Leave `fixture_hashes`, `drills`, `drill_evidence`, `sim_chain_ok_event_id`, `notification_*` untouched.
- Run: `python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` (exit 0) and `… --require-resolved` (exit 0). Then the local gate simulation: `python ops/c1_rail/c1_rail_arm.py --status --config deploy/c1_rail/c1_rail_config.fly.example.json --acceptance docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` → `m1_gate: status='RESOLVED' result=PASS` (the example config is disarmed and secret-free; `--status` writes nothing).
- Commit, push, open PR 1 (Codex reviews; operator merges).

### Step 2.3 — Redeploy the listener (six pre-conditions)
After PR 1 merges: host `--status` read (`dry_run=True`, `armed_until=None`); checkout `main` at the merge SHA, clean; `pytest tests/ops/test_c1_rail_image_manifest.py -q`; pre-deploy in-container hashes equal the A5 pins; `fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile`; boot line `dry_run=True armed_until=-`; health ok; in-container `--status` → `m1_gate: status='RESOLVED' result=PASS`; post-deploy `sha256sum` of the pinned files → unchanged vs A5 (only the JSON changed) and `sha256sum docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` recorded.

### Step 2.4 — Deploy record (PR 2)
`code_commit_or_branch` → the PR 1 merge SHA + release/machine/image; `fixture_hashes_note` dated entry (pins unchanged, artifact hash recorded, status now RESOLVED in-image); readiness §A8; `STATE.md`: row 1 leaves the queue, decision index gains the dated consequence with the record link; the parent decides on a `SESSIONS.md` entry. Validator plain + `--require-resolved` exit 0. Commit, push, PR 2.

### Step 2.5 — Stop
Final `--status` pasted: `dry_run=True armed_until=None … m1_gate: status='RESOLVED' result=PASS`. No arm.

## 4. Falsifiable hypothesis

**H:** the A7 event satisfies item 5 as the ADR and its 2026-08-24 addendum define it, the artifact with the owed fields validates under `--require-resolved`, and the redeployed listener's in-image gate reads `PASS` while the host stays disarmed.
**Reject** if the validator fails, if the in-image `--status` does not read `PASS` after the redeploy, or if the host is anything but disarmed → `FALSIFIED`; do not edit the validator or the gate to make it pass. **Ambiguous** if the amendment's qualification wording is contested → `NEEDS_CONTEXT`.

## 5. Forbidden moves

- `--arm`, `--acknowledge-m1-unresolved`, or any config edit beyond what `fly deploy` does — tempting exactly now, and exactly forbidden: `RESOLVED` is one of two conditions, the other is a separate GO.
- Populating the event field with any id but the A7 UUID (the 2026-07-28 floored event, a fabricated id, the SIM chain id).
- Editing `drills`, `drill_evidence`, `sim_chain_ok_event_id`, `notification_*`, or `fixture_hashes` values.
- Loosening the validator, the secret scanner, or `m1_acceptance_reason`.
- Claiming live-feed readiness, strategy readiness, or deployment authority in the notes.
- Refreshing pins from tree bytes.

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
