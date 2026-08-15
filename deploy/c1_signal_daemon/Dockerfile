# c1 Python signal daemon — second Fly app (S2b / build ADR 2026-08-08).
#
# Build context = REPO ROOT. Never shares the listener volume / peak_equity.
#
# Deploy from repo root:
#   fly deploy . --config deploy/c1_signal_daemon/fly.toml \
#                --dockerfile deploy/c1_signal_daemon/Dockerfile
#
# Warm default: IdleBarSource + emit_enabled=false (NullStrategy). Databento
# Live wiring is a follow-on under the same build ADR; listener image stays
# stdlib-only and untouched.
FROM python:3.12-slim

WORKDIR /app

COPY ops/c1_signal_daemon/__init__.py ops/c1_signal_daemon/__main__.py \
     ops/c1_signal_daemon/b1_payload.py ops/c1_signal_daemon/daemon.py \
     ops/c1_signal_daemon/evaluate_loop.py ops/c1_signal_daemon/feed.py \
     ops/c1_signal_daemon/heartbeat.py ops/c1_signal_daemon/http_status.py \
     ops/c1_signal_daemon/listener_client.py \
     ops/c1_signal_daemon/strategy_protocol.py \
     ./ops/c1_signal_daemon/

# Config on volume; wait if missing (mirror listener — no crash-loop).
CMD ["sh", "-c", "if [ ! -f /data/c1_signal_daemon_config.json ]; then echo 'WAIT: /data/c1_signal_daemon_config.json missing — sftp config to /data, then: fly machine restart <id>' >&2; exec sleep infinity; fi; exec python ops/c1_signal_daemon/daemon.py --config /data/c1_signal_daemon_config.json"]
