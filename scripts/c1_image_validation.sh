#!/usr/bin/env bash
# Track A / A2 — Linux image validation for c1 listener + signal daemon.
# Usage: ./scripts/c1_image_validation.sh listener|daemon|all
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TARGET="${1:-}"
if [[ "$TARGET" != "listener" && "$TARGET" != "daemon" && "$TARGET" != "all" ]]; then
  echo "Usage: $0 listener|daemon|all" >&2
  exit 2
fi

LOG_DIR="${C1_IMAGE_VALIDATION_LOG_DIR:-/tmp/c1_image_validation}"
mkdir -p "$LOG_DIR"
FIXTURES="$ROOT/tests/fixtures/c1_image_validation"
LISTENER_TAG="c1-rail:ci"
DAEMON_TAG="c1-signal-daemon:ci"

PASS_N=0
FAIL_N=0
declare -a RESULTS=()

record_pass() {
  local id="$1"; shift
  PASS_N=$((PASS_N + 1))
  RESULTS+=("PASS $id")
  printf 'PASS %s' "$id"
  if [[ $# -gt 0 ]]; then printf ' %s' "$*"; fi
  printf '\n'
}

record_fail() {
  local id="$1"; shift
  FAIL_N=$((FAIL_N + 1))
  RESULTS+=("FAIL $id")
  printf 'FAIL %s' "$id"
  if [[ $# -gt 0 ]]; then printf ' %s' "$*"; fi
  printf '\n'
  # Surface evidence in the job log (artifacts alone are easy to miss).
  local f
  for f in "$@"; do
    [[ -f "$f" ]] || continue
    printf -- '----- begin %s -----\n' "$f"
    cat "$f" 2>/dev/null || true
    printf -- '----- end %s -----\n' "$f"
  done
}

# atomic_json/mkstemp writes root-owned mode 0600 into the bind mount; the
# runner user then cannot read state/owner files. Re-open world-read after boot.
host_readable_data() {
  local name="$1"
  docker exec "$name" sh -c 'chmod -R a+rX /data 2>/dev/null || true' || true
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 2; }
}
need_cmd docker
need_cmd python3

LISTENER_FILES=(
  /app/core/dd_protection.py
  /app/core/firm_rules.py
  /app/core/historical_challenge.py
  /app/core/lib/atomic_io.py
  /app/core/lib/file_lock.py
  /app/core/lib/mvd.py
  /app/core/lib/validation.py
  /app/core/lifecycle.py
  /app/docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
  /app/ops/c1_rail/__init__.py
  /app/ops/c1_rail/c1_rail_arm.py
  /app/ops/c1_rail/c1_rail_http_server.py
  /app/ops/c1_rail/c1_rail_listener.py
  /app/ops/c1_rail/c1_rail_slippage.py
  /app/ops/c1_rail/c1_rail_telemetry.py
  /app/ops/c1_rail/c1_sizing_host_reference.py
  /app/ops/c1_rail/crosstrade_payload.py
  /app/ops/c1_rail/m1_stage1_contract.py
  /app/ops/c1_rail/m1_stage1_control.py
  /app/scripts/validate_c1_monitoring_acceptance.py
)

DAEMON_FILES=(
  /app/ops/c1_rail/__init__.py
  /app/ops/c1_rail/m1_stage1_contract.py
  /app/ops/c1_signal_daemon/__init__.py
  /app/ops/c1_signal_daemon/__main__.py
  /app/ops/c1_signal_daemon/b1_payload.py
  /app/ops/c1_signal_daemon/daemon.py
  /app/ops/c1_signal_daemon/evaluate_loop.py
  /app/ops/c1_signal_daemon/feed.py
  /app/ops/c1_signal_daemon/heartbeat.py
  /app/ops/c1_signal_daemon/http_status.py
  /app/ops/c1_signal_daemon/listener_client.py
  /app/ops/c1_signal_daemon/m1_stage1.py
  /app/ops/c1_signal_daemon/m1_stage1_control.py
  /app/ops/c1_signal_daemon/m1_stage1_state.py
  /app/ops/c1_signal_daemon/m1_stage1_strategy.py
  /app/ops/c1_signal_daemon/strategy_protocol.py
)

sha256_file() {
  # Never trip `set -e` on a missing path (D6 seed can leave state_file empty).
  if [[ -z "${1:-}" || ! -f "$1" ]]; then
    printf '%s\n' "FILE_MISSING"
    return 0
  fi
  sha256sum "$1" | awk '{print $1}'
}

# Copy evidence into *.log so the workflow artifact upload (*.log) retains it.
evidence_log() {
  local dest="$1"; shift
  {
    printf '=== %s ===\n' "$*"
    for f in "$@"; do
      [[ -e "$f" ]] || continue
      printf -- '--- %s ---\n' "$f"
      cat "$f" 2>/dev/null || true
      printf '\n'
    done
  } >"$dest" 2>/dev/null || true
}

stop_rm() { docker rm -f "$1" >/dev/null 2>&1 || true; }

container_alive() {
  docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null | grep -qx true
}

wait_for_log() {
  local name="$1" pattern="$2" seconds="$3" logf="$4"
  local i
  for i in $(seq 1 "$seconds"); do
    docker logs "$name" >"$logf" 2>&1 || true
    if grep -q -- "$pattern" "$logf"; then return 0; fi
    sleep 1
  done
  docker logs "$name" >"$logf" 2>&1 || true
  return 1
}

# HTTP against --network none via docker exec + urllib (helper .py avoids quote hell).
write_http_helpers() {
  cat >"$LOG_DIR/_http_get.py" <<'PY'
import sys, urllib.request
url = sys.argv[1]
with urllib.request.urlopen(url, timeout=5) as resp:
    sys.stdout.buffer.write(resp.read())
PY
  cat >"$LOG_DIR/_http_post.py" <<'PY'
import sys, urllib.error, urllib.request
url, body = sys.argv[1], sys.argv[2].encode("utf-8")
req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")
# Write status+body through the buffer only — mixing print() and buffer.write()
# can reorder lines under block buffering inside `docker exec`.
def _emit(code: int, payload: bytes) -> None:
    sys.stdout.buffer.write(f"{code}\n".encode("ascii"))
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        _emit(resp.status, resp.read())
except urllib.error.HTTPError as exc:
    _emit(exc.code, exc.read())
PY
  cat >"$LOG_DIR/_assert_decision.py" <<'PY'
"""Assert last decision (+ transport_result) in an events JSONL ledger.

argv: path qty halt_mode [halt_reason [contract [require_dry_run]]]
  halt_mode: true|false|any
  require_dry_run: true (default) | false  — L6 live-mode halt records dry_run=false
"""
import json, sys
path, qty_s, halt_mode = sys.argv[1], sys.argv[2], sys.argv[3]
halt_reason = sys.argv[4] if len(sys.argv) > 4 else ""
contract = sys.argv[5] if len(sys.argv) > 5 else ""
require_dry_run = (sys.argv[6] if len(sys.argv) > 6 else "true") != "false"
qty = int(qty_s)
rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
decisions = [r for r in rows if r.get("kind") == "decision"]
transports = [r for r in rows if r.get("kind") == "transport_result"]
if not decisions:
    raise SystemExit("no decision rows")
d = decisions[-1]
# Pair the transport row with THIS decision by event_id (Codex P1, 2026-09-11):
# the ledger still holds earlier checks' rows, so "last transport" is not "this
# request's transport" when a regression omits it.
transports = [r for r in transports if r.get("event_id") == d.get("event_id")]
errs = []
def need(c, m):
    if not c: errs.append(m)
need(d.get("qty_out") == qty, f"qty_out={d.get('qty_out')} want {qty}")
if require_dry_run:
    need(d.get("dry_run") is True, f"dry_run={d.get('dry_run')}")
need(d.get("test_only") is True, f"test_only={d.get('test_only')}")
need(d.get("sender_invoked") is False, f"sender_invoked={d.get('sender_invoked')}")
if halt_mode == "true":
    need(d.get("halt") is True, f"halt={d.get('halt')}")
elif halt_mode == "false":
    need(d.get("halt") is False, f"halt={d.get('halt')}")
if halt_reason:
    need(d.get("halt_reason") == halt_reason, f"halt_reason={d.get('halt_reason')!r}")
if contract:
    need(d.get("test_contract_sha256") == contract, f"test_contract_sha256 mismatch")
if not transports:
    errs.append(f"no transport_result for decision event_id={d.get('event_id')}")
else:
    need(transports[-1].get("transport_state") == "not_attempted",
         f"transport_state={transports[-1].get('transport_state')}")
if errs:
    raise SystemExit("; ".join(errs) + " | decision=" + json.dumps(d, sort_keys=True, default=str)[:500])
print(json.dumps({"qty_out": d.get("qty_out"), "halt": d.get("halt"),
                  "halt_reason": d.get("halt_reason"), "dry_run": d.get("dry_run"),
                  "transport_state": transports[-1].get("transport_state")}, sort_keys=True))
PY
}

http_get_in() {
  local name="$1" url="$2" out="$3"
  docker cp "$LOG_DIR/_http_get.py" "$name:/tmp/_http_get.py" >/dev/null
  docker exec "$name" python /tmp/_http_get.py "$url" >"$out"
}

http_post_in() {
  local name="$1" url="$2" body="$3" out="$4"
  docker cp "$LOG_DIR/_http_post.py" "$name:/tmp/_http_post.py" >/dev/null
  docker exec "$name" python /tmp/_http_post.py "$url" "$body" >"$out"
}

path_token() { tr -d '[:space:]' <"$FIXTURES/PATH_TOKEN.txt"; }
daemon_path_token() { tr -d '[:space:]' <"$FIXTURES/DAEMON_PATH_TOKEN.txt"; }

stage_listener_data() {
  local dest="$1"
  rm -rf "$dest"; mkdir -p "$dest" "$dest/c1_rail_alert_acks"
  cp "$FIXTURES/c1_rail_config.json" "$dest/c1_rail_config.json"
  cp "$FIXTURES/lifecycle_state.json" "$dest/lifecycle_state.json"
  cp "$FIXTURES/c1_dd_state.json" "$dest/c1_dd_state.json"
  cp "$FIXTURES/c1_current_equity.json" "$dest/c1_current_equity.json"
  : >"$dest/c1_rail_events.jsonl"
}

generate_constants_in_image() {
  local dest="$1" logf="$2"
  # -i forwards the heredoc on stdin; without it `python -` sees EOF and exits 0
  # while writing nothing — L4 GET still passes, but later POSTs halt on missing constants.
  docker run --rm -i --network none -v "$dest:/data" "$LISTENER_TAG" \
    python - >"$logf" 2>&1 <<'PY'
import json, sys
sys.path[:0] = ["/app/ops/c1_rail", "/app/core"]
from c1_sizing_host_reference import generate_constants
constants = generate_constants("Tradeify_Select_100K")
with open("/data/c1_sizing_constants.json", "w", encoding="utf-8") as fh:
    json.dump(constants, fh, sort_keys=True, indent=2)
    fh.write("\n")
print("ok", constants.get("tier"))
PY
  # Fail closed if the mirror never landed (empty-python-success trap).
  [[ -s "$dest/c1_sizing_constants.json" ]] || return 1
}

stage_daemon_data() {
  local dest="$1" cfg="$2"
  rm -rf "$dest"; mkdir -p "$dest"
  cp "$cfg" "$dest/c1_signal_daemon_config.json"
}

########################################################################
# Listener
########################################################################
run_listener() {
  write_http_helpers
  local blog="$LOG_DIR/L1_build.log"
  if docker build -f deploy/c1_rail/Dockerfile -t "$LISTENER_TAG" . >"$blog" 2>&1; then
    record_pass L1 "built $LISTENER_TAG"
  else
    record_fail L1 "build failed; see $blog"
    return 0
  fi

  local files="$LOG_DIR/L2_files.txt" exp="$LOG_DIR/L2_expected.txt"
  docker run --rm --network none --entrypoint find "$LISTENER_TAG" /app -type f | sort >"$files"
  printf '%s\n' "${LISTENER_FILES[@]}" | sort >"$exp"
  local l2=1
  diff -u "$exp" "$files" >"$LOG_DIR/L2_diff.txt" || l2=0
  if grep -E '\.pine$|/core/data(/|$)|/tests/' "$files" >/dev/null; then l2=0; fi
  if ! grep -qx '/app/docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json' "$files"; then l2=0; fi
  if ! docker run --rm --network none "$LISTENER_TAG" \
      python -c "import sys; sys.path.insert(0,'scripts'); import validate_c1_monitoring_acceptance" \
      >"$LOG_DIR/L2_import.log" 2>&1; then l2=0; fi
  if [[ "$l2" -eq 1 ]]; then record_pass L2 "exact COPY set; validator imports"
  else record_fail L2 "see $LOG_DIR/L2_diff.txt / L2_import.log"; fi

  local d3="$LOG_DIR/L3_data"; rm -rf "$d3"; mkdir -p "$d3"
  stop_rm c1-L3
  docker run -d --name c1-L3 --network none -v "$d3:/data" "$LISTENER_TAG" >"$LOG_DIR/L3.cid"
  if wait_for_log c1-L3 'WAIT:' 10 "$LOG_DIR/L3.log" && container_alive c1-L3; then
    record_pass L3 "WAIT present; alive"
  else
    record_fail L3 "see $LOG_DIR/L3.log"
  fi
  stop_rm c1-L3

  local d4="$LOG_DIR/L4_data"
  stage_listener_data "$d4"
  if ! generate_constants_in_image "$d4" "$LOG_DIR/L4_constants.log"; then
    record_fail L4 "constants generation failed"
  else
    stop_rm c1-L4
    docker run -d --name c1-L4 --network none -v "$d4:/data" "$LISTENER_TAG" >"$LOG_DIR/L4.cid"
    local l4=1
    wait_for_log c1-L4 'dry_run=True' 15 "$LOG_DIR/L4.log" || l4=0
    grep -q 'dry_run=True armed_until=-' "$LOG_DIR/L4.log" || l4=0
    http_get_in c1-L4 'http://127.0.0.1:8080/' "$LOG_DIR/L4.get" 2>"$LOG_DIR/L4.get.err" || l4=0
    python3 - "$LOG_DIR/L4.get" <<'PY' || l4=0
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
assert d.get("ok") is True and d.get("service")=="c1_rail_http_server"
PY
    if [[ "$l4" -eq 1 ]]; then record_pass L4 "boot disarmed; GET ok"
    else record_fail L4 "see $LOG_DIR/L4.log / L4.get"; fi
  fi

  # L5a / L5b share c1-L4 if alive
  if container_alive c1-L4; then
    local tok; tok="$(path_token)"
    local bar_a; bar_a="ci-l5a-$(python3 -c 'import uuid;print(uuid.uuid4())')"
    local body_a; body_a="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar_a','close':42000.0,'stop_dist_pts':1.0}))")"
    local l5a_post=1
    http_post_in c1-L4 "http://127.0.0.1:8080/c1/${tok}" "$body_a" "$LOG_DIR/L5a.out" 2>"$LOG_DIR/L5a.post.err" || l5a_post=0
    # Prefer in-container ledger bytes (bind-mount visibility is usually fine on
    # Linux, but docker exec removes any doubt when asserting).
    docker exec c1-L4 cat /data/c1_rail_events.jsonl >"$LOG_DIR/L5a.events" 2>"$LOG_DIR/L5a.events.err" || true
    if [[ ! -s "$LOG_DIR/L5a.events" && -s "$d4/c1_rail_events.jsonl" ]]; then
      cp "$d4/c1_rail_events.jsonl" "$LOG_DIR/L5a.events"
    fi
    if [[ "$l5a_post" -eq 1 ]] && head -1 "$LOG_DIR/L5a.out" | grep -qx 200 \
       && python3 "$LOG_DIR/_assert_decision.py" "$LOG_DIR/L5a.events" 0 any \
            >"$LOG_DIR/L5a.assert" 2>"$LOG_DIR/L5a.err"; then
      record_pass L5a "qty_out=0 default identity" "$(cat "$LOG_DIR/L5a.assert")"
    else
      evidence_log "$LOG_DIR/L5a.fail.log" "$LOG_DIR/L5a.out" "$LOG_DIR/L5a.err" "$LOG_DIR/L5a.events" "$LOG_DIR/L5a.events.err"
      record_fail L5a "$LOG_DIR/L5a.fail.log"
    fi

    local l5b=1
    if ! docker exec c1-L4 python ops/c1_rail/m1_stage1_control.py migrate \
          --config /data/c1_rail_config.json --enable-test \
          >"$LOG_DIR/L5b.plan" 2>"$LOG_DIR/L5b.plan.err"; then l5b=0; fi
    local ec el
    ec="$(python3 -c "import json;print(json.load(open('$LOG_DIR/L5b.plan'))['before']['constants'])" 2>/dev/null || true)"
    el="$(python3 -c "import json;print(json.load(open('$LOG_DIR/L5b.plan'))['before']['lifecycle'])" 2>/dev/null || true)"
    [[ -n "$ec" && -n "$el" ]] || l5b=0
    if [[ "$l5b" -eq 1 ]]; then
      if ! docker exec c1-L4 python ops/c1_rail/m1_stage1_control.py migrate \
            --config /data/c1_rail_config.json --enable-test \
            --apply --flat-verified \
            --expect-constants "$ec" --expect-lifecycle "$el" \
            >"$LOG_DIR/L5b.apply" 2>"$LOG_DIR/L5b.apply.err"; then l5b=0; fi
    fi
    ls "$d4"/*.m1-backup-* >/dev/null 2>&1 || l5b=0
    local csha=""
    if [[ "$l5b" -eq 1 ]]; then
      # -i is required so the heredoc reaches `python -`; without it csha is empty.
      csha="$(docker exec -i c1-L4 python - <<'PY'
import sys
sys.path[:0]=["/app/ops/c1_rail","/app/core"]
from m1_stage1_contract import contract_sha256
print(contract_sha256())
PY
)"
    fi
    local bar_b; bar_b="ci-l5b-$(python3 -c 'import uuid;print(uuid.uuid4())')"
    local body_b; body_b="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar_b','close':42000.0,'stop_dist_pts':1.0}))")"
    if [[ "$l5b" -eq 1 ]]; then
      http_post_in c1-L4 "http://127.0.0.1:8080/c1/${tok}" "$body_b" "$LOG_DIR/L5b.out" 2>"$LOG_DIR/L5b.post.err" || l5b=0
      local rbody; rbody="$(tail -n +2 "$LOG_DIR/L5b.out")"
      grep -q 'dry_run: computed, not sent' <<<"$rbody" || l5b=0
      head -1 "$LOG_DIR/L5b.out" | grep -qx 200 || l5b=0
      docker exec c1-L4 cat /data/c1_rail_events.jsonl >"$LOG_DIR/L5b.events" 2>/dev/null \
        || cp "$d4/c1_rail_events.jsonl" "$LOG_DIR/L5b.events"
      python3 "$LOG_DIR/_assert_decision.py" "$LOG_DIR/L5b.events" 1 false "" "$csha" \
        >"$LOG_DIR/L5b.assert" 2>"$LOG_DIR/L5b.err" || l5b=0
    fi
    if [[ "$l5b" -eq 1 ]]; then record_pass L5b "migrate+POST qty_out=1; no restart" "$(cat "$LOG_DIR/L5b.assert")"
    else
      evidence_log "$LOG_DIR/L5b.fail.log" "$LOG_DIR/L5b.plan" "$LOG_DIR/L5b.plan.err" \
        "$LOG_DIR/L5b.apply" "$LOG_DIR/L5b.apply.err" "$LOG_DIR/L5b.out" "$LOG_DIR/L5b.err" "$LOG_DIR/L5b.events"
      record_fail L5b "$LOG_DIR/L5b.fail.log"
    fi
  else
    record_fail L5a "container down"
    record_fail L5b "container down"
  fi
  stop_rm c1-L4

  # L6 live-mode
  local d6="$LOG_DIR/L6_data"
  stage_listener_data "$d6"
  generate_constants_in_image "$d6" "$LOG_DIR/L6_constants.log" || true
  python3 - "$d6/c1_rail_config.json" <<'PY'
import json,sys
from datetime import datetime,timedelta,timezone
p=sys.argv[1]; c=json.load(open(p,encoding="utf-8"))
c["dry_run"]=False
c["armed_until"]=(datetime.now(timezone.utc)+timedelta(hours=1)).replace(microsecond=0).isoformat()
json.dump(c, open(p,"w",encoding="utf-8"), indent=2); open(p,"a",encoding="utf-8").write("\n")
PY
  stop_rm c1-L6
  docker run -d --name c1-L6 --network none -v "$d6:/data" "$LISTENER_TAG" >"$LOG_DIR/L6.cid"
  local l6=1
  wait_for_log c1-L6 'dry_run=False' 15 "$LOG_DIR/L6.log" || l6=0
  local tok; tok="$(path_token)"
  local bar6; bar6="ci-l6-$(python3 -c 'import uuid;print(uuid.uuid4())')"
  local body6; body6="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar6','close':42000.0,'stop_dist_pts':1.0}))")"
  if container_alive c1-L6; then
    http_post_in c1-L6 "http://127.0.0.1:8080/c1/${tok}" "$body6" "$LOG_DIR/L6.out" 2>"$LOG_DIR/L6.post.err" || l6=0
    docker exec c1-L6 cat /data/c1_rail_events.jsonl >"$LOG_DIR/L6.events" 2>/dev/null \
      || cp "$d6/c1_rail_events.jsonl" "$LOG_DIR/L6.events"
    # Live-mode halt records dry_run=false on the decision row — do not require True.
    python3 "$LOG_DIR/_assert_decision.py" "$LOG_DIR/L6.events" 0 true \
      "m1_test_requires_explicit_dry_run" "" false >"$LOG_DIR/L6.assert" 2>"$LOG_DIR/L6.err" || l6=0
  else l6=0; fi
  if [[ "$l6" -eq 1 ]]; then record_pass L6 "live-mode halted" "$(cat "$LOG_DIR/L6.assert")"
  else
    evidence_log "$LOG_DIR/L6.fail.log" "$LOG_DIR/L6.log" "$LOG_DIR/L6.out" "$LOG_DIR/L6.err" "$LOG_DIR/L6.events"
    record_fail L6 "$LOG_DIR/L6.fail.log"
  fi
  stop_rm c1-L6

  # L6b absent dry_run
  local d6b="$LOG_DIR/L6b_data"
  stage_listener_data "$d6b"
  generate_constants_in_image "$d6b" "$LOG_DIR/L6b_constants.log" || true
  python3 - "$d6b/c1_rail_config.json" <<'PY'
import json,sys
p=sys.argv[1]; c=json.load(open(p,encoding="utf-8")); c.pop("dry_run",None)
json.dump(c, open(p,"w",encoding="utf-8"), indent=2); open(p,"a",encoding="utf-8").write("\n")
PY
  stop_rm c1-L6b
  docker run -d --name c1-L6b --network none -v "$d6b:/data" "$LISTENER_TAG" >"$LOG_DIR/L6b.cid"
  local l6b=1
  wait_for_log c1-L6b 'dry_run=True armed_until=-' 15 "$LOG_DIR/L6b.log" || l6b=0
  local bar6b; bar6b="ci-l6b-$(python3 -c 'import uuid;print(uuid.uuid4())')"
  local body6b; body6b="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar6b','close':42000.0,'stop_dist_pts':1.0}))")"
  if container_alive c1-L6b; then
    http_post_in c1-L6b "http://127.0.0.1:8080/c1/${tok}" "$body6b" "$LOG_DIR/L6b.out" 2>"$LOG_DIR/L6b.post.err" || l6b=0
    python3 "$LOG_DIR/_assert_decision.py" "$d6b/c1_rail_events.jsonl" 0 any \
      >"$LOG_DIR/L6b.assert" 2>"$LOG_DIR/L6b.err" || l6b=0
  else l6b=0; fi
  if [[ "$l6b" -eq 1 ]]; then record_pass L6b "absent dry_run defaults True"
  else record_fail L6b "see L6b.log / L6b.err"; fi
  stop_rm c1-L6b

  # L7 arming interlock
  local d7="$LOG_DIR/L7_data"
  stage_listener_data "$d7"
  generate_constants_in_image "$d7" "$LOG_DIR/L7_constants.log" || true
  stop_rm c1-L7
  docker run -d --name c1-L7 --network none -v "$d7:/data" --entrypoint sleep "$LISTENER_TAG" infinity
  local before after; before="$(sha256_file "$d7/c1_rail_config.json")"
  local l7=1
  docker exec c1-L7 python ops/c1_rail/c1_rail_arm.py --status --config /data/c1_rail_config.json \
    >"$LOG_DIR/L7.status" 2>&1 || l7=0
  grep -q "m1_gate: status='CODE_LANDED' result=FAIL" "$LOG_DIR/L7.status" || l7=0
  set +e
  docker exec c1-L7 python ops/c1_rail/c1_rail_arm.py --arm --hours 1 --config /data/c1_rail_config.json \
    >"$LOG_DIR/L7.arm" 2>&1
  local arc=$?
  set -e
  [[ "$arc" -ne 0 ]] || l7=0
  grep -qi 'refusing to arm' "$LOG_DIR/L7.arm" || l7=0
  after="$(sha256_file "$d7/c1_rail_config.json")"
  [[ "$before" == "$after" ]] || l7=0
  if [[ "$l7" -eq 1 ]]; then record_pass L7 "interlock refuses arm; sha unchanged"
  else record_fail L7 "see L7.status / L7.arm"; fi
  stop_rm c1-L7

  # L8 implicit disarm
  local d8="$LOG_DIR/L8_data"
  stage_listener_data "$d8"
  generate_constants_in_image "$d8" "$LOG_DIR/L8_constants.log" || true
  python3 - "$d8/c1_rail_config.json" <<'PY'
import json,sys
from datetime import datetime,timedelta,timezone
p=sys.argv[1]; c=json.load(open(p,encoding="utf-8"))
c["dry_run"]=False
c["armed_until"]=(datetime.now(timezone.utc)-timedelta(hours=1)).replace(microsecond=0).isoformat()
json.dump(c, open(p,"w",encoding="utf-8"), indent=2); open(p,"a",encoding="utf-8").write("\n")
PY
  stop_rm c1-L8
  docker run -d --name c1-L8 --network none -v "$d8:/data" "$LISTENER_TAG" >"$LOG_DIR/L8.cid"
  if wait_for_log c1-L8 'dry_run=True armed_until=-' 15 "$LOG_DIR/L8.log" \
     && grep -q 'IMPLICIT DISARM' "$LOG_DIR/L8.log"; then
    record_pass L8 "IMPLICIT DISARM on expired armed_until"
  else
    record_fail L8 "see L8.log"
  fi
  stop_rm c1-L8
}

########################################################################
# Daemon
########################################################################
run_daemon() {
  write_http_helpers
  local blog="$LOG_DIR/D1_build.log"
  if docker build -f deploy/c1_signal_daemon/Dockerfile -t "$DAEMON_TAG" . >"$blog" 2>&1; then
    record_pass D1 "built $DAEMON_TAG"
  else
    record_fail D1 "build failed; see $blog"
    return 0
  fi

  local files="$LOG_DIR/D2_files.txt" exp="$LOG_DIR/D2_expected.txt"
  docker run --rm --network none --entrypoint find "$DAEMON_TAG" /app -type f | sort >"$files"
  printf '%s\n' "${DAEMON_FILES[@]}" | sort >"$exp"
  local d2=1
  diff -u "$exp" "$files" >"$LOG_DIR/D2_diff.txt" || d2=0
  set +e
  docker run --rm --network none "$DAEMON_TAG" python -c 'import databento' >"$LOG_DIR/D2_db.log" 2>&1
  local db=$?
  set -e
  [[ "$db" -ne 0 ]] || d2=0
  cat >"$LOG_DIR/D2_pip.py" <<'PY'
import json, subprocess, sys
from pathlib import Path

def dists(image):
    out = subprocess.check_output(
        ["docker","run","--rm","--network","none",image,"python","-m","pip","list","--format=json"],
        text=True)
    return {r["name"].lower() for r in json.loads(out)}

base, img = dists("python:3.12-slim"), dists(sys.argv[1])
extras = sorted(img - base)
req = Path("deploy/c1_signal_daemon/requirements.txt")
if not req.exists():
    expected = []
else:
    text = req.read_text(encoding="utf-8")
    if "--hash=" not in text:
        print("FAIL: requirements.txt not hash-pinned")
        sys.exit(2)
    names=[]
    for line in text.splitlines():
        line=line.strip()
        if not line or line.startswith("#") or line.startswith("-"): continue
        names.append(line.split("==")[0].split("[")[0].strip().lower())
    expected=sorted(set(n for n in names if n))
print(json.dumps({"extras":extras,"expected":expected}, sort_keys=True))
sys.exit(0 if extras==expected else 1)
PY
  python3 "$LOG_DIR/D2_pip.py" "$DAEMON_TAG" >"$LOG_DIR/D2_pip.json" 2>"$LOG_DIR/D2_pip.err" || d2=0
  if [[ "$d2" -eq 1 ]]; then record_pass D2 "COPY exact; no databento; extras match" "$(cat "$LOG_DIR/D2_pip.json")"
  else record_fail D2 "see D2_diff.txt / D2_pip.err"; fi

  local d3="$LOG_DIR/D3_data"; rm -rf "$d3"; mkdir -p "$d3"
  stop_rm c1-D3
  docker run -d --name c1-D3 --network none -v "$d3:/data" "$DAEMON_TAG" >"$LOG_DIR/D3.cid"
  if wait_for_log c1-D3 'WAIT:' 10 "$LOG_DIR/D3.log" && container_alive c1-D3; then
    record_pass D3 "WAIT present; alive"
  else record_fail D3 "see D3.log"; fi
  stop_rm c1-D3

  # D4 inert boot
  local d4="$LOG_DIR/D4_data"
  stage_daemon_data "$d4" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D4
  docker run -d --name c1-D4 --network none -v "$d4:/data" "$DAEMON_TAG" >"$LOG_DIR/D4.cid"
  local d4ok=1
  wait_for_log c1-D4 'daemon up' 15 "$LOG_DIR/D4.log" || d4ok=0
  grep -Eq 'daemon up bind=.+:.+ emit_enabled=false boot_id=' "$LOG_DIR/D4.log" || d4ok=0
  host_readable_data c1-D4
  http_get_in c1-D4 'http://127.0.0.1:8080/' "$LOG_DIR/D4.get" 2>"$LOG_DIR/D4.get.err" || d4ok=0
  cat >"$LOG_DIR/D4_health.py" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
need={"emit_enabled":False,"effective_emit":False,"strategy":"NullStrategy",
      "feed_mode":"unavailable","connected":False,"feed_healthy":False,
      "ceremony_state":"DISABLED"}
for k,v in need.items():
    if d.get(k)!=v: raise SystemExit(f"{k}={d.get(k)!r} want {v!r}")
if not d.get("boot_id"): raise SystemExit("empty boot_id")
print(json.dumps({**need,"boot_id":d["boot_id"]}, sort_keys=True))
PY
  python3 "$LOG_DIR/D4_health.py" "$LOG_DIR/D4.get" >"$LOG_DIR/D4.health" 2>"$LOG_DIR/D4.health.err" || d4ok=0
  # Snapshot /data from inside the container so bind-mount surprises are visible.
  docker exec c1-D4 sh -c 'ls -la /data; echo ---; for f in /data/*.json /data/*.lock /data/*.owner.lock; do [ -e "$f" ] || continue; echo "# $f"; wc -c "$f"; done' \
    >"$LOG_DIR/D4.data.ls.log" 2>&1 || true
  docker cp c1-D4:/data "$LOG_DIR/D4_data_cp" >/dev/null 2>&1 || true
  cat >"$LOG_DIR/D4_state.py" <<'PY'
import json,sys
from pathlib import Path
data=Path(sys.argv[1]); state=None; sp=None
listing=sorted(p.name for p in data.iterdir()) if data.is_dir() else []
for p in data.glob("*.json"):
    try: obj=json.loads(p.read_text(encoding="utf-8"))
    except Exception: continue
    if "schema_version" in obj and "boot_id" in obj:
        state,sp=obj,p; break
if state is None:
    raise SystemExit(f"state missing; dir={listing}")
assert state["schema_version"]==1, state
assert state["enabled"] is False, state
assert state["active"] is None, state
assert state["boot_id"], state
locks=list(data.glob("*.owner.lock"))
assert locks, f"owner.lock missing; dir={listing}"
print(json.dumps({"path":sp.name,"boot_id":state["boot_id"],"generation":state.get("generation"),
                  "inode":sp.stat().st_ino,"owner":locks[0].name,"dir":listing}, sort_keys=True))
PY
  # State check tracked separately: the docker-cp fallback may recover only THIS
  # check, never an earlier health/log failure (Codex P1, 2026-09-11).
  local d4state=1
  python3 "$LOG_DIR/D4_state.py" "$d4" >"$LOG_DIR/D4.state" 2>"$LOG_DIR/D4.state.err" || d4state=0
  if [[ "$d4state" -ne 1 && -d "$LOG_DIR/D4_data_cp" ]]; then
    python3 "$LOG_DIR/D4_state.py" "$LOG_DIR/D4_data_cp" >"$LOG_DIR/D4.state.cp" 2>"$LOG_DIR/D4.state.cp.err" && d4state=1 || true
  fi
  [[ "$d4state" -eq 1 ]] || d4ok=0
  sleep 15
  # The daemon must still be running after the quiet interval; a crash-looping
  # image would otherwise pass the "no step lines" grep trivially.
  container_alive c1-D4 || d4ok=0
  docker logs c1-D4 >"$LOG_DIR/D4.log" 2>&1 || true
  if grep -E 'step |b1_post|m1_b1_post' "$LOG_DIR/D4.log" >/dev/null; then d4ok=0; fi
  if [[ "$d4ok" -eq 1 ]]; then record_pass D4 "inert boot" "$(cat "$LOG_DIR/D4.health")"
  else
    evidence_log "$LOG_DIR/D4.fail.log" "$LOG_DIR/D4.log" "$LOG_DIR/D4.get" "$LOG_DIR/D4.health.err" \
      "$LOG_DIR/D4.state.err" "$LOG_DIR/D4.state.cp.err" "$LOG_DIR/D4.data.ls.log"
    record_fail D4 "$LOG_DIR/D4.fail.log"
  fi
  stop_rm c1-D4

  # D5 stale-enabled
  local d5="$LOG_DIR/D5_data"
  stage_daemon_data "$d5" "$FIXTURES/c1_signal_daemon_config.stale_enabled.json"
  stop_rm c1-D5
  docker run -d --name c1-D5 --network none -v "$d5:/data" "$DAEMON_TAG" >"$LOG_DIR/D5.cid"
  local d5ok=1
  wait_for_log c1-D5 'daemon up' 15 "$LOG_DIR/D5.log" || d5ok=0
  host_readable_data c1-D5
  http_get_in c1-D5 'http://127.0.0.1:8080/' "$LOG_DIR/D5.get" 2>"$LOG_DIR/D5.get.err" || d5ok=0
  python3 "$LOG_DIR/D4_health.py" "$LOG_DIR/D5.get" >"$LOG_DIR/D5.health" 2>"$LOG_DIR/D5.health.err" || d5ok=0
  sleep 5
  # Still alive after the interval (Codex P2, 2026-09-11): a daemon that exits on
  # the stale-enabled config must not validate as "inert".
  container_alive c1-D5 || d5ok=0
  docker logs c1-D5 >"$LOG_DIR/D5.log" 2>&1 || true
  grep -E 'b1_post|m1_b1_post' "$LOG_DIR/D5.log" >/dev/null && d5ok=0
  if [[ "$d5ok" -eq 1 ]]; then record_pass D5 "stale-enabled stays inert; alive after interval"
  else record_fail D5 "see D5.log"; fi
  stop_rm c1-D5

  # D6 CLI refusal
  local d6="$LOG_DIR/D6_data"
  stage_daemon_data "$d6" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D6seed
  docker run -d --name c1-D6seed --network none -v "$d6:/data" "$DAEMON_TAG"
  wait_for_log c1-D6seed 'daemon up' 15 "$LOG_DIR/D6.seed.log" || true
  host_readable_data c1-D6seed
  stop_rm c1-D6seed
  local state_file
  state_file="$(python3 - <<PY
from pathlib import Path
import json
for p in Path("$d6").glob("*.json"):
    try: o=json.loads(p.read_text())
    except Exception: continue
    if "schema_version" in o:
        print(p); break
PY
)"
  local cfg_sha st_sha
  cfg_sha="$(sha256_file "$d6/c1_signal_daemon_config.json")"
  st_sha="$(sha256_file "$state_file")"
  stop_rm c1-D6
  docker run -d --name c1-D6 --network none -v "$d6:/data" --entrypoint sleep "$DAEMON_TAG" infinity
  local d6ok=1
  for act in prepare enable; do
    set +e
    docker exec -e PYTHONPATH=/app/ops c1-D6 python -m c1_signal_daemon.m1_stage1_control "$act" \
      >"$LOG_DIR/D6_${act}.out" 2>&1
    local rc=$?
    set -e
    [[ "$rc" -eq 2 ]] || d6ok=0
    grep -q 'ceremony blocked: no approved source' "$LOG_DIR/D6_${act}.out" || d6ok=0
  done
  set +e
  docker exec -e PYTHONPATH=/app/ops c1-D6 python -m c1_signal_daemon.m1_stage1_control status \
    >"$LOG_DIR/D6_status.out" 2>&1
  local src=$?
  set -e
  [[ "$src" -eq 0 ]] || d6ok=0
  python3 - "$LOG_DIR/D6_status.out" <<'PY' || d6ok=0
import json,sys
d=json.loads(open(sys.argv[1],encoding="utf-8").read())
assert d.get("effective_emit") is False
assert d.get("source_status")=="unavailable"
PY
  [[ "$(sha256_file "$d6/c1_signal_daemon_config.json")" == "$cfg_sha" ]] || d6ok=0
  [[ "$(sha256_file "$state_file")" == "$st_sha" ]] || d6ok=0
  if [[ "$d6ok" -eq 1 ]]; then record_pass D6 "prepare/enable exit 2; hashes unchanged"
  else record_fail D6 "see D6_*.out"; fi
  stop_rm c1-D6

  # D7 ownership
  local d7="$LOG_DIR/D7_data"
  stage_daemon_data "$d7" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D7
  docker run -d --name c1-D7 --network none -v "$d7:/data" "$DAEMON_TAG"
  local d7ok=1
  wait_for_log c1-D7 'daemon up' 15 "$LOG_DIR/D7.log" || d7ok=0
  host_readable_data c1-D7
  set +e
  timeout 5 docker exec c1-D7 python ops/c1_signal_daemon/daemon.py --config /data/c1_signal_daemon_config.json \
    >"$LOG_DIR/D7.second" 2>&1
  local src=$?
  set -e
  # Must EXIT non-zero within 5 s: 124 is GNU timeout's "command timed out" and
  # 125-127 are docker/exec infrastructure statuses, none of which is a refusal.
  case "$src" in 0|124|125|126|127) d7ok=0 ;; esac
  grep -q 'daemon ownership unavailable' "$LOG_DIR/D7.second" || d7ok=0
  http_get_in c1-D7 'http://127.0.0.1:8080/' "$LOG_DIR/D7.get" 2>"$LOG_DIR/D7.get.err" || d7ok=0
  if [[ "$d7ok" -eq 1 ]]; then record_pass D7 "second process refused; GET ok"
  else record_fail D7 "see D7.second"; fi
  stop_rm c1-D7

  # D8 restart semantics
  # Brief: boot_id changed, generation +1, enabled false, active null, lock still
  # "initialized", state not re-created (generation > 0). atomic_json uses
  # os.replace, so inode may change — do not require inode equality.
  local d8="$LOG_DIR/D8_data"
  stage_daemon_data "$d8" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D8a
  docker run -d --name c1-D8a --network none -v "$d8:/data" "$DAEMON_TAG"
  wait_for_log c1-D8a 'daemon up' 15 "$LOG_DIR/D8a.log" || true
  host_readable_data c1-D8a
  python3 "$LOG_DIR/D4_state.py" "$d8" >"$LOG_DIR/D8a.state" 2>"$LOG_DIR/D8a.err" || true
  local marker
  # Prefer explicit *.json.lock (ceremony companion; skip owner locks).
  marker="$(python3 - <<PY
from pathlib import Path
data=Path("$d8")
cands=list(data.glob("*.json.lock"))+list(data.glob("*.lock"))
for p in cands:
    if "owner" in p.name: continue
    print(p.read_text(encoding="utf-8").strip()); break
PY
)"
  stop_rm c1-D8a
  stop_rm c1-D8b
  docker run -d --name c1-D8b --network none -v "$d8:/data" "$DAEMON_TAG"
  local d8ok=1
  wait_for_log c1-D8b 'daemon up' 15 "$LOG_DIR/D8b.log" || d8ok=0
  host_readable_data c1-D8b
  python3 "$LOG_DIR/D4_state.py" "$d8" >"$LOG_DIR/D8b.state" 2>"$LOG_DIR/D8b.err" || d8ok=0
  if [[ "$d8ok" -eq 1 ]]; then
    python3 - "$LOG_DIR/D8a.state" "$LOG_DIR/D8b.state" "$marker" "$d8" <<'PY' || d8ok=0
import json,sys
from pathlib import Path
a,b=json.load(open(sys.argv[1])),json.load(open(sys.argv[2]))
marker,data=sys.argv[3],Path(sys.argv[4])
assert a["boot_id"]!=b["boot_id"], (a["boot_id"], b["boot_id"])
assert b["generation"]==a["generation"]+1, (a.get("generation"), b.get("generation"))
assert marker=="initialized", marker
ok=False
for p in list(data.glob("*.json.lock"))+list(data.glob("*.lock")):
    if "owner" in p.name: continue
    assert p.read_text(encoding="utf-8").strip()=="initialized"
    ok=True
assert ok, "ceremony lock missing after restart"
# Continuity = generation advanced from a prior state (not a fresh generation-0 boot).
assert a["generation"] >= 0 and b["generation"] > 0
for p in data.glob("*.json"):
    try: o=json.loads(p.read_text())
    except Exception: continue
    if "schema_version" in o:
        assert o["enabled"] is False and o["active"] is None
        assert o.get("generation",0) > 0
print("ok")
PY
  fi
  if [[ "$d8ok" -eq 1 ]]; then record_pass D8 "boot_id changed; generation+1; lock initialized"
  else
    evidence_log "$LOG_DIR/D8.fail.log" "$LOG_DIR/D8a.state" "$LOG_DIR/D8b.state" \
      "$LOG_DIR/D8a.err" "$LOG_DIR/D8b.err" "$LOG_DIR/D8a.log" "$LOG_DIR/D8b.log"
    record_fail D8 "see D8.fail.log marker=$marker"
  fi
  stop_rm c1-D8b

  # D9 focused suites
  local d9_list=()
  local g
  for g in \
    tests/ops/test_c1_signal_daemon_*.py \
    tests/ops/test_m1_stage1_*.py \
    tests/ops/test_c1_rail_*.py \
    tests/ops/test_c1_sizing_host_reference.py \
    tests/ops/test_m1_acceptance_drills.py \
    tests/ops/test_crosstrade_payload.py \
    tests/test_validate_c1_monitoring_acceptance.py \
    tests/rail_crosstrade \
    tests/test_rail_goldenpath_crosstrade.py
  do
    # shellcheck disable=SC2206
    local exp=( $g )
    local e
    for e in "${exp[@]}"; do [[ -e "$e" ]] && d9_list+=("$e"); done
  done
  local d9ok=1
  # Ephemeral pip needs network (brief §0.5(A)); boot checks stay --network none.
  mkdir -p "${HOME:-/root}/.cache/pip"
  set +e
  docker run --rm \
    -v "$ROOT:/work:ro" \
    -v "${HOME:-/root}/.cache/pip:/root/.cache/pip" \
    -w /work python:3.12-slim \
    bash -lc "python -m pip install --require-hashes -r requirements-ops.lock >/tmp/pip.log 2>&1 && python -m pytest -q ${d9_list[*]}" \
    >"$LOG_DIR/D9_slim.log" 2>&1
  local slim_rc=$?
  set -e
  [[ "$slim_rc" -eq 0 ]] || d9ok=0
  set +e
  docker run --rm \
    -v "$ROOT/tests:/work/tests:ro" \
    -v "$ROOT/requirements-ops.lock:/work/requirements-ops.lock:ro" \
    -v "$ROOT/pyproject.toml:/work/pyproject.toml:ro" \
    -v "${HOME:-/root}/.cache/pip:/root/.cache/pip" \
    -w /work "$DAEMON_TAG" \
    bash -lc 'python -m pip install --require-hashes -r requirements-ops.lock >/tmp/pip.log 2>&1; python -m pytest -q tests/ops/test_c1_signal_daemon_*.py tests/ops/test_m1_stage1_*.py' \
    >"$LOG_DIR/D9_inimage.log" 2>&1
  local in_rc=$?
  set -e
  # Executed-test failures in the built image are gating (Codex P1, 2026-09-11);
  # collection-time import errors stay informational per brief §0.5 (A).
  if grep -qE '(^|[^a-z])[0-9]+ failed' "$LOG_DIR/D9_inimage.log"; then d9ok=0; fi
  {
    echo "slim_rc=$slim_rc inimage_rc=$in_rc"
    echo "slim_files=${#d9_list[@]} paths=${d9_list[*]}"
    echo -n "slim_counts "; grep -E 'passed|failed|error|skipped' "$LOG_DIR/D9_slim.log" | tail -1 || echo "(no summary)"
    echo -n "inimage_counts "; grep -E 'passed|failed|error|skipped' "$LOG_DIR/D9_inimage.log" | tail -1 || echo "(no summary)"
    if grep -qiE 'ModuleNotFoundError|ImportError' "$LOG_DIR/D9_inimage.log"; then
      echo "inimage_note=imports failed in-image (reported, not forced)"
    fi
  } >"$LOG_DIR/D9_summary.txt"
  cat "$LOG_DIR/D9_summary.txt"
  if [[ "$d9ok" -ne 1 ]]; then
    echo "---- D9_slim.log (tail) ----"
    tail -n 80 "$LOG_DIR/D9_slim.log" || true
    echo "---- D9_inimage.log (tail) ----"
    tail -n 40 "$LOG_DIR/D9_inimage.log" || true
  fi
  if [[ "$d9ok" -eq 1 ]]; then record_pass D9 "slim suite green; in-image: no executed failures (rc=$in_rc; import errors informational)" "$(tr '\n' ' ' <"$LOG_DIR/D9_summary.txt")"
  else record_fail D9 "slim suite failed or in-image executed tests failed; see D9_slim.log / D9_inimage.log" "$(tr '\n' ' ' <"$LOG_DIR/D9_summary.txt")"; fi

  # D10 real-socket timeout — helper temp .py
  cat >"$LOG_DIR/D10_probe.py" <<'PY'
"""D10: emitting loop + real default_transport → silent listening socket."""
from __future__ import annotations
import json, os, socket, sys, threading, time, traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

sys.path[:0] = ["/app/ops", "/app"]

from c1_signal_daemon.evaluate_loop import EvaluateLoop
from c1_signal_daemon.feed import Bar
from c1_signal_daemon.listener_client import ListenerClient, default_transport
from c1_signal_daemon.m1_stage1 import M1Coordinator
from c1_signal_daemon.m1_stage1_control import enable, prepare
from c1_signal_daemon.m1_stage1_state import CeremonyStore
from c1_signal_daemon.m1_stage1_strategy import M1Stage1TestStrategy
from c1_rail.m1_stage1_contract import contract_sha256


def main() -> int:
    work = Path(os.environ.get("D10_WORK", "/tmp/d10_work"))
    work.mkdir(parents=True, exist_ok=True)
    accepted = {"n": 0}
    stop = {"flag": False}

    def server():
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", 0))
        srv.listen(5)
        (work / "port.txt").write_text(str(srv.getsockname()[1]), encoding="utf-8")
        srv.settimeout(1.0)
        conns = []
        while not stop["flag"]:
            try:
                conn, _ = srv.accept()
                accepted["n"] += 1
                conns.append(conn)  # never read
            except socket.timeout:
                continue
        for c in conns:
            try: c.close()
            except OSError: pass
        srv.close()

    threading.Thread(target=server, daemon=True).start()
    for _ in range(50):
        if (work / "port.txt").exists(): break
        time.sleep(0.05)
    port = int((work / "port.txt").read_text(encoding="utf-8").strip())
    base_url = f"http://127.0.0.1:{port}"

    target = datetime(2099, 1, 1, 14, 0, tzinfo=timezone.utc)
    now = target - timedelta(minutes=1)
    received = target + timedelta(seconds=61)
    cid = "ci-d10-" + uuid4().hex[:12]
    token = "c" + ("i" * 47)

    state_path = work / "state.json"
    cfg_path = work / "daemon.json"
    store = CeremonyStore(state_path)
    store.boot("d10-boot")
    cfg = {
        "listener_base_url": base_url,
        "path_token": token,
        "bind_host": "127.0.0.1",
        "bind_port": 18080,
        "bar_period_s": 60,
        "poll_interval_s": 1,
        "emit_enabled": False,
        "strategy": "null",
        "m1_test": {"enabled": False, "state_path": str(state_path)},
    }
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    source_binding = {"kind": "offline_fixture", "schema": "ohlcv-1m", "symbol": "MYM1!"}
    manifest = {
        "ceremony_id": cid,
        "target": target.isoformat(),
        "expires": (target + timedelta(seconds=140)).isoformat(),
        "source": source_binding,
        "contract_sha256": contract_sha256(),
        "expected_qty": 1,
        "preflight_sha256": "e" * 64,
    }
    prepare(store, cfg_path, manifest, boot_id="d10-boot", now=now)
    enable(store, cfg_path, cid, boot_id="d10-boot", reviewed=manifest, now=now)

    class Source:
        connected = True
        binding = source_binding
        feed_mode = "offline_fixture"
        def activate(self, binding): assert binding == self.binding
        def deactivate(self): pass
        def poll(self): return Bar(target, 41000.0, 41002.0, 40999.0, 41001.0, 3.0)

    coordinator = M1Coordinator(store, cfg_path, boot_id="d10-boot")
    client = ListenerClient(base_url=base_url, path_token=token, transport=default_transport)
    loop = EvaluateLoop(
        source=Source(), client=client, strategy=M1Stage1TestStrategy(coordinator),
        coordinator=coordinator, bar_period_s=60, emit_enabled=True, boot_id="d10-boot",
    )

    t0 = time.monotonic()
    try:
        result = loop.step(received)
    except Exception as exc:  # noqa: BLE001
        result = {"action": "exception", "exc": type(exc).__name__}
        traceback.print_exc()
    elapsed = time.monotonic() - t0

    obj = store.read()
    item = obj["ceremonies"].get(cid) or obj["ceremonies"].get(obj.get("active"), {})
    state = item.get("state")
    prev = item.get("previous_state")
    n1 = accepted["n"]
    loop.step(received)
    loop.step(received)
    n2 = accepted["n"]
    stop["flag"] = True

    report = {
        "elapsed_s": round(elapsed, 3),
        "accepted_first": n1,
        "accepted_after": n2,
        "ceremony_state": state,
        "previous_state": prev,
        "result": result,
    }
    print(json.dumps(report, sort_keys=True))
    if n1 != 1: raise SystemExit(f"accepted_first={n1}")
    if n2 != 1: raise SystemExit(f"accepted_after={n2}")
    if elapsed < 25 or elapsed > 45: raise SystemExit(f"elapsed={elapsed}")
    if state != "TRANSPORT_UNKNOWN" and prev != "TRANSPORT_UNKNOWN":
        raise SystemExit(f"state={state!r} prev={prev!r} item={item!r}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
PY
  local d10w="$LOG_DIR/D10_work"; rm -rf "$d10w"; mkdir -p "$d10w"
  set +e
  docker run --rm --network none \
    -v "$LOG_DIR/D10_probe.py:/tmp/D10_probe.py:ro" \
    -v "$d10w:/tmp/d10_work" \
    -e D10_WORK=/tmp/d10_work -e PYTHONPATH=/app/ops \
    "$DAEMON_TAG" python /tmp/D10_probe.py \
    >"$LOG_DIR/D10.out" 2>"$LOG_DIR/D10.err"
  local d10rc=$?
  set -e
  if [[ "$d10rc" -eq 0 ]]; then record_pass D10 "30s timeout; TRANSPORT_UNKNOWN; one accept" "$(tail -1 "$LOG_DIR/D10.out")"
  else record_fail D10 "see D10.err / D10.out"; fi
}

########################################################################
echo "c1 image validation — target=$TARGET log_dir=$LOG_DIR"
case "$TARGET" in
  listener) run_listener ;;
  daemon) run_daemon ;;
  all) run_listener; run_daemon ;;
esac

echo
echo "==== summary ===="
for r in "${RESULTS[@]}"; do echo "$r"; done
echo "PASS=$PASS_N FAIL=$FAIL_N"
printf '%s\n' "${RESULTS[@]}" >"$LOG_DIR/summary.txt"
echo "PASS=$PASS_N FAIL=$FAIL_N" >>"$LOG_DIR/summary.txt"
[[ "$FAIL_N" -eq 0 ]]
