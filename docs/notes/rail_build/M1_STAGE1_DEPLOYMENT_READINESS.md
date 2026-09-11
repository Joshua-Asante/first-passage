# M1 Stage 1 deployment readiness record

**Date:** 2026-09-11 (opened by Track A / A3; §A4–§A8 append in later sub-tracks)
**Owner:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3 — the parent session records each sub-track's return after the two-pass review
**Purpose:** the public, secret-free evidence trail for the two Track A deployments and the single attended Stage 1 ceremony: what was verified, from where, and what remains NO-GO.
**This note authorizes nothing.** No deploy, arm, order, or `RESOLVED` claim rests on it; the owners are the [M1 ADR](../../adr/2026-07-22-c1-venue-native-monitoring-maturity.md), the [S2b build ADR](../../adr/2026-08-08-s2b-signal-daemon-build.md), the [GO ADR](../../adr/2026-07-17-c1-rail-build-account-registration-go.md) and the c1-rail skill. Private figures (tokens, account ids, equity, raw bar values) never appear here; every `--status` paste replaces the account token with `account=<redacted>`.

## §A3 — Recovery path (2026-09-11)

**Brief:** [A3 handoff](../../briefs/handoffs/2026-09-10-track-a-a3-claude-recovery-path-attestation.md) · **Currency:** `origin/main @ b7e028a`; A0 hard check `git ls-tree --name-only origin/main ops/c1_rail/ | grep -c m1_stage1_` → `2` · **Authority used:** read-only Fly commands and read-only reads of the public tree and the private archive; no deploy, restart, `ssh` write, volume read, or archive push.

### 1. Mitigation in code

- **On `origin/main @ b7e028a`:** `grep -n "IMPLICIT DISARM" ops/c1_rail/c1_rail_http_server.py` → `159:` (comment) and `186:` (the warning). The block (lines 158–191) runs inside `load_config`: when the volume config says `dry_run=false` but `armed_until` is expired, absent or malformed at boot, the process logs `IMPLICIT DISARM at boot — …`, sets `dry_run=True` and `armed_until=None` **in memory**, and boots disarmed; the file on disk is unchanged until `python ops/c1_rail/c1_rail_arm.py --disarm` makes the disarm durable. The comment block dates the reversal to the 2026-07-31 incident.
- **Deployed build, history corroboration:** `git show 31fd642:ops/c1_rail/c1_rail_http_server.py | grep -n "IMPLICIT DISARM"` → `159:` and `186:`. `31fd642` (2026-08-19) is an ancestor of `origin/main` (`git merge-base --is-ancestor` true) and a public commit (`gh api repos/Joshua-Asante/first-passage/commits/31fd642` → `2026-08-19T17:30:26Z`), and the acceptance JSON pins the running listener build to `origin/main @ 31fd642` (release v7, machine `e820221a657d28`, image `deployment-01M0DMFSFXVXEHZ27G8VYC0WQK`).
- **Deployed build, decisive in-container read:** `MSYS_NO_PATHCONV=1 fly ssh console -a c1-rail -C "grep -n IMPLICIT.DISARM ops/c1_rail/c1_rail_http_server.py"` → run by the operator in their own PowerShell console on 2026-09-11 (the form `& fly ssh console -a c1-rail -C "grep -n IMPLICIT.DISARM ops/c1_rail/c1_rail_http_server.py"`; flyctl auto-updated 0.4.85 → v0.4.102 during the call) and read from the Terminal panel by the session. Printed, verbatim:

```
Connecting to fdaa:9e:e939:a7b:894:a6fd:8e8a:2... complete
159:    # at boot, treat that as an IMPLICIT DISARM and boot disarmed — do not
186:                "IMPLICIT DISARM at boot — %s. The config on disk still says "
```

  The connection address is the private IP `fly machine list` reports for machine `e820221a657d28`, and the two line numbers equal the `31fd642` and `origin/main` greps. **The deployed listener carries the implicit-disarm boot path.**
- **What the mitigation removes:** the `armed_until`-lapse crash-loop class — on 2026-07-31 a lapsed `armed_until` with `dry_run=false` still on the volume made the boot gate raise, Fly stopped the machine at its max restart count, and `fly ssh` could not reach a machine that never booted, so the documented remedy (edit `/data`, restart) was unreachable and recovery took an entrypoint override.
- **What it does not remove:** (a) config missing → the entrypoint's `WAIT:` guard sleeps instead of crash-looping (both apps; load the volume, then restart); (b) a green build whose CMD dies with `ModuleNotFoundError` (a module in no COPY line) → image rollback to the references in item 4 (the 2026-07-31 `core/historical_challenge.py` class; re-trace the import closure before every deploy); (c) a config that **exists but does not validate** — the `WAIT:` guard only tests the file's existence, and both entrypoints call `load_config` before the health server starts, so the process exits and Fly restarts it until the machine is stopped, the same reachability problem as 2026-07-31. Listener (`ops/c1_rail/c1_rail_http_server.py::load_config`): not a JSON object, missing required keys, `dry_run=false` without `events_log_path`, a `path_token` shorter than the minimum or still starting with `REPLACE`, and the other `ValueError` branches at lines 195–213. Daemon (`ops/c1_signal_daemon/daemon.py::load_config`): malformed JSON, `m1_test` not an object, missing required keys or a short `path_token` (`SystemExit`), non-boolean enable flags, an unknown `strategy`, or an enabled-ceremony configuration that is incomplete or carries a non-positive `generation` (`ValueError`, lines 58–86). These recur after A6 or a rollback whenever the staged file is wrong, which is why A6 Step 2.2b runs `load_config` locally on the prepared daemon config before the operator puts it, and why A4 reads the listener config's key set before A5. (d) any other boot failure. Classes (c) and (d) are the private procedure's territory (item 2); the daemon has no arming gate, so class (a) of item 1's mitigation never applies to it, but (a), (b), (c) and (d) all do.
- **Skew flagged, not edited:** `.claude/skills/c1-rail/SKILL.md` deploy pre-condition 6 still reads "An expired `armed_until` makes the host refuse to boot, and `fly ssh` needs a booted machine, so a restart cannot fix it." That sentence describes the pre-fix behaviour; the code above (on `main` since before `31fd642`) boots disarmed instead. The pre-condition's conclusion — know the recovery path before starting — still holds because classes (b), (c) and (d) remain. The parent rewords it through the skill's own authoring path; this record does not touch the skill.

### 2. Procedure availability

- **Repository:** `Joshua-Asante/first-passage-archive` — private; marked archived (read-only) on GitHub since the 2026-09-06 preservation push (`gh repo view` → `archived=true`, `PRIVATE`).
- **Pinned SHA:** `5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2` — the pin every archive link on this tree uses (for example the W6 ADR's Related line).
- **Path:** `docs/notes/rail_build/RUNBOOK.md` — blob `0b90318f7695`, 119,887 bytes, 40 headings at that SHA. The public pointer to it is the W6 ADR's Related link `docs/notes/rail_build/RUNBOOK.md`, dead on this tree by design.
- **Heading grep** `^#+ .*(recover|self-brick|override|arming log|crash)` → one hit: line **217 `## B7 arming log`**, the section the acceptance JSON's 2026-07-27 and 2026-08-19 notes cite for the incident timeline and the "self-brick class"; the file names the incident date `2026-07-31` five times and the override once. No body text is reproduced here.
- **Method:** no clone of the archive exists on this machine and none was created (brief §0.5 forbids cloning by default). Availability was verified read-only through the GitHub contents API at the pinned SHA; only heading lines and counts left the shell pipe.

### 3. Operator access confirmed

**2026-09-11** — the operator opened the procedure in the browser at the pinned commit and said, in-session, verbatim: "I opened the RUNBOOK B7 arming log at 5d47b4dc." Recorded after it was said; nothing else about the procedure is recorded.

### 4. Current and rollback releases

Read-only inventory, 2026-09-11, `flyctl v0.4.85` (`fly releases`, `fly status`, `fly machine list`, `fly image show`):

| App | Release | Machine | Image (tag) | Image (digest) | Source commit |
|---|---|---|---|---|---|
| `c1-rail` (listener) | v7 `complete`, 2026-08-19 18:28 | `e820221a657d28` — `started`, 1/1 checks, last updated 2026-08-19T18:28:50Z, volume `vol_vxm828pzmlzyn7j4` | `registry.fly.io/c1-rail:deployment-01M0DMFSFXVXEHZ27G8VYC0WQK` | `sha256:05d509ad2166760e6af00be09f592190522e8962cccd02ae7f1d973cb1a21e13` | `origin/main @ 31fd642` (acceptance JSON `code_commit_or_branch`) |
| `c1-signal-daemon` | v1 **`failed`**, 2026-08-08 04:50 — the only release, yet the machine runs (A4 explains this from evidence; this section only names the image) | `840759c2474928` — `started`, 1/1 checks, last updated 2026-08-08T04:53:26Z, volume `vol_r1j1pglm3zpmyy9r` | `registry.fly.io/c1-signal-daemon:deployment-01KZFVAFXM3RTWJWVWND6W6TQ7` | `sha256:8e3a8f687ac4770b8125a99301a10265fdc55400d3031c71710b16b888f0ce2b` | not pinned in any record; the plan §0 identifies it as the 2026-08-08 pre-#332 `IdleBarSource` build |

- **Rollback targets:** A5 → the listener image above (not v6: v6 is the flat-layout build v7 retired). A6 → the daemon image above (the source-free build, inert by construction: no `ops/c1_signal_daemon/m1_stage1_*` modules, no journal).
- **No-build rollback form:** `fly deploy --help` line 134 confirms `-i, --image string   The Docker image to deploy`. From the repo root:

```bash
fly deploy --image registry.fly.io/c1-rail:deployment-01M0DMFSFXVXEHZ27G8VYC0WQK --config deploy/c1_rail/fly.toml
fly deploy --image registry.fly.io/c1-signal-daemon:deployment-01KZFVAFXM3RTWJWVWND6W6TQ7 --config deploy/c1_signal_daemon/fly.toml
```

- **Pre-condition:** a rollback is itself a deploy. The six per-app pre-conditions apply in order — the listener host `--status` read first (judge by printed output; Windows `fly ssh console -C` may exit 1 after correct output), the documented command from the repo root, the import-closure re-trace, `fixture_hashes` re-pinned from **in-container** bytes for the listener (a rollback moves pinned files back), the boot line and health verified after, and this recovery path known.

### 5. Recovery cannot restore obsolete state

- Recovery writes touch only `dry_run` and `armed_until`: `c1_rail_arm.py --disarm` (`plan_disarm` sets `dry_run=True`, `armed_until=None`; `_write` is an atomic write keeping a one-deep backup) or the entrypoint override in the private procedure. Neither rewrites `c1_sizing_constants.json`, `lifecycle_state.json`, the DD state, or the daemon journal (`c1_m1_stage1_state.json`, its `.lock` and `.owner.lock`).
- The 69/11 Striker allocation is released doctrine ([ADR 2026-08-26](../../adr/2026-08-26-striker-legmap-cap-release.md); the committed `LEG_MAP` reads 0/0). Any residue on the listener volume is handled only by A5's attended migration step (`ops/c1_rail/m1_stage1_control.py migrate … --release-withdrawn`, operator-confirmed in-session), never by a recovery step.
- `dry_run=false` is never a recovery target: recovery ends disarmed, and re-arming is operator-only under the M1 gate (`--arm` is not in Track A).

### Deviations and flags for the parent

- Archive availability was verified through the GitHub API (read-only, headings and counts only) rather than a local clone — none exists here and the brief forbids creating one by default.
- Codex review (P2, 2026-09-11) folded: the daemon's failure classes were understated as two; config-validation crash loops are now class (c) for both apps, with the A6/A4 guards named.
- The decisive in-container grep was run by the operator in their own console because this session's permission layer blocked `fly ssh console`; the session read the printed output from the Terminal panel and recorded it verbatim (item 1).
- c1-rail skill pre-condition 6 wording skew (item 1) — parent rewords via the skill's authoring path.

**Return:** `DONE_WITH_CONCERNS` — every §4 limb held with pasted evidence and all five items are recorded; the three flags above are for the parent (the skill wording skew needs an edit outside this record; the other two are method deviations, recorded so the review can weigh them). Per-step gates: 2.1 pass · 2.2 pass · 2.3 pass · 2.4 pass · 2.5 pass. Files touched: this note only.
