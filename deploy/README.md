# `deploy/` — Fly.io packaging (ops, no `.py`)

Build context is the **repo root**. Do not collapse the two apps.

| App | Config | Code |
|---|---|---|
| Listener | [`c1_rail/`](c1_rail/) | [`ops/c1_rail/`](../ops/c1_rail/) |
| S2b daemon | [`c1_signal_daemon/`](c1_signal_daemon/) | [`ops/c1_signal_daemon/`](../ops/c1_signal_daemon/) |

Posture (disarmed / no book) is owned by
[`CLAUDE.md`](../CLAUDE.md) §Live-execution posture.
Runbooks in the per-app READMEs are standup only — they do not authorize arming.

Linux image validation (build, inert/disarmed boot, POSIX fsync/flock, arming
interlock) lives in [`.github/workflows/c1-image-validation.yml`](../.github/workflows/c1-image-validation.yml)
and [`scripts/c1_image_validation.sh`](../scripts/c1_image_validation.sh); procedure
ownership stays in the per-app READMEs.
