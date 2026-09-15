# c1 Python signal daemon — second Fly app (S2b / build ADR 2026-08-08).
#
# Build context = REPO ROOT. Never shares the listener volume / peak_equity.
#
# Deploy from repo root:
#   fly deploy . --config deploy/c1_signal_daemon/fly.toml \
#                --dockerfile deploy/c1_signal_daemon/Dockerfile
#
# Operator-attended Stage 1 input; startup remains NullStrategy, emit disabled.
# Databento retired by operator; both images remain stdlib-only.
FROM python:3.12-slim

WORKDIR /app

COPY ops/c1_signal_daemon/__init__.py ops/c1_signal_daemon/__main__.py \
     ops/c1_signal_daemon/b1_payload.py ops/c1_signal_daemon/daemon.py \
     ops/c1_signal_daemon/evaluate_loop.py ops/c1_signal_daemon/feed.py \
     ops/c1_signal_daemon/heartbeat.py ops/c1_signal_daemon/http_status.py \
     ops/c1_signal_daemon/listener_client.py \
     ops/c1_signal_daemon/operator_input_source.py \
     ops/c1_signal_daemon/book_protocol.py \
     ops/c1_signal_daemon/book_adapters.py \
     ops/c1_signal_daemon/book_runtime.py \
     ops/c1_signal_daemon/book_evaluate_loop.py \
     ops/c1_signal_daemon/strategy_protocol.py \
     ops/c1_signal_daemon/m1_stage1.py \
     ops/c1_signal_daemon/m1_stage1_state.py \
     ops/c1_signal_daemon/m1_stage1_strategy.py \
     ops/c1_signal_daemon/m1_stage1_control.py \
     ./ops/c1_signal_daemon/

# Only the stdlib proof contract is shared, never listener/account state.
COPY ops/c1_rail/__init__.py ops/c1_rail/m1_stage1_contract.py \
     ops/c1_rail/m1_stage1_agent_input.py ops/c1_rail/c1_rail_listener.py \
     ops/c1_rail/c1_rail_telemetry.py ops/c1_rail/c1_sizing_host_reference.py \
     ops/c1_rail/crosstrade_payload.py ops/c1_rail/book_policy.py \
     ops/c1_rail/book_sizing_context.py ops/c1_rail/book_halt.py \
     ops/c1_rail/book_account_lock.py ops/c1_rail/book_account_owner.py \
     ops/c1_rail/book_capacity.py ops/c1_rail/book_session_calendar.py \
     ops/c1_rail/book_settlement.py ops/c1_rail/account_close_calculation.py \
     ops/c1_rail/account_close_evidence.py ops/c1_rail/account_close_ledger.py \
     ops/c1_rail/ed25519_verify.py ops/c1_rail/settlement_signing.py \
     ops/c1_rail/operator_keys.json ./ops/c1_rail/

COPY core/dd_protection.py core/dd_geometry.py core/firm_rules.py core/lifecycle.py \
     core/historical_challenge.py core/calendar_evidence.py ./core/
COPY core/lib/atomic_io.py core/lib/file_lock.py core/lib/mvd.py \
     core/lib/validation.py ./core/lib/

# Config on volume; wait if missing (mirror listener — no crash-loop).
CMD ["sh", "-c", "if [ ! -f /data/c1_signal_daemon_config.json ]; then echo 'WAIT: /data/c1_signal_daemon_config.json missing — sftp config to /data, then: fly machine restart <id>' >&2; exec sleep infinity; fi; exec python ops/c1_signal_daemon/daemon.py --config /data/c1_signal_daemon_config.json"]
