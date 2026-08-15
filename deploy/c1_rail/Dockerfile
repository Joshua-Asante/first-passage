# c1 rail sizing host — Fly.io image (spec docs/spec/c1_nt8_sizing_host_impl.md §2.5).
#
# Build context = REPO ROOT (so COPY can reach ops/ + core/). A repo-root
# .dockerignore allow-lists ONLY the traced module set, so no proprietary bytes
# (Pine, vendor CSVs, research, .git) ever enter the build context sent to Fly's
# remote builder.
#
# Deploy from repo root (no local Docker needed — Fly builds remotely):
#   fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile
#
# Runs as root (image default): a single-purpose, path-token-gated, private
# micro-service whose only ingress is Fly's TLS-terminating edge. Root avoids the
# Fly-volume-ownership footgun (a mounted volume masks image-time chown, so a
# non-root user cannot write c1_dd_state.json / the audit log without a runtime
# chown+privilege-drop). Non-root + volume chown is the documented hardening path
# (deploy/c1_rail/README.md), not v1.
FROM python:3.12-slim

# The c1 rail host is STDLIB-ONLY (verified: requires-python >=3.11; the traced
# module set imports nothing third-party). If a dependency is ever introduced,
# add a requirements.txt + `pip install --no-cache-dir -r requirements.txt` here.

WORKDIR /app

# Exactly the transitively-imported modules (traced 2026-07-18 via sys.modules;
# re-verified by running the server from this isolated subset; re-traced
# 2026-07-31 after substrate Phase 4 added core/historical_challenge.py, which
# core/dd_protection.py:62 imports unguarded — it was missing here for one day
# and would have crash-looped the machine at CMD on the next deploy, with a
# GREEN build, since a module in no COPY line cannot fail a COPY).
# Layout (2026-08-03): rail modules live under ops/c1_rail/. Bootstrap:
#   _REPO_ROOT = Path(__file__).resolve().parents[2]   ->  /app
#   sys.path.insert(/app/core), sys.path.insert(/app/ops/c1_rail)
# c1_rail_arm.py / c1_rail_slippage.py are not imported by the server — they
# are operator-run CLIs (`--arm/--disarm`, Stage 2b fill-slippage) that must
# be present in-container to be usable over `fly ssh console`.
COPY ops/c1_rail/c1_rail_http_server.py ops/c1_rail/c1_rail_listener.py \
     ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_sizing_host_reference.py \
     ops/c1_rail/crosstrade_payload.py ops/c1_rail/c1_rail_arm.py \
     ops/c1_rail/c1_rail_slippage.py ops/c1_rail/__init__.py \
     ./ops/c1_rail/
COPY core/dd_protection.py core/firm_rules.py core/lifecycle.py \
     core/historical_challenge.py ./core/
COPY core/lib/atomic_io.py core/lib/file_lock.py core/lib/mvd.py \
     core/lib/validation.py ./core/lib/

# The M1 acceptance artifact — read by ops/c1_rail/c1_rail_arm.py's arming interlock
# (ADR 2026-07-22 Addendum 2026-07-31b: dry_run=false may not be set while M1
# is not RESOLVED). This is the ONE docs/ path in the image, and it is here
# deliberately: the deployed host must gate on the acceptance record deployed
# WITH it, not on a mutable file the operator could edit to satisfy the gate.
# Consequence, by design: when M1 flips to RESOLVED, arming requires a redeploy
# — the same redeploy that must refresh fixture_hashes anyway.
# NOTE: absence is FAIL-SAFE (m1_acceptance_reason treats unreadable as NOT
# RESOLVED), so a missing COPY here refuses arming rather than permitting it.
COPY docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json ./docs/notes/rail_build/

# Schema owner for the arming interlock (hardened 2026-08-09): c1_rail_arm
# imports validate() from this module with require_resolved=True. Without this
# COPY the arm CLI dies at import in-container — same silent-green-build class
# as the historical_challenge miss (Dockerfile comment block above).
COPY scripts/validate_c1_monitoring_acceptance.py ./scripts/

# Config + ALL state (secrets + mutable peak-equity) live on the mounted Fly
# volume at /data — NEVER baked into the image. If the config isn't on the
# volume yet, WAIT (do not crash-loop) so the operator can `fly ssh sftp` it in
# and restart the machine. Inlined so there is no entrypoint.sh CRLF footgun.
CMD ["sh", "-c", "if [ ! -f /data/c1_rail_config.json ]; then echo 'WAIT: /data/c1_rail_config.json missing — sftp config + state JSON to /data, then: fly machine restart <id>' >&2; exec sleep infinity; fi; exec python ops/c1_rail/c1_rail_http_server.py --config /data/c1_rail_config.json"]
