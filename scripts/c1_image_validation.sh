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
  /app/ops/c1_signal_daemon/operator_input_source.py
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

# Every boot uses this boundary; callers must preserve its failure in their
# check flag. Keep Docker's creation error in the uploaded evidence as well.
launch_container() {
  local name="$1"; shift
  docker run -d --name "$name" "$@" >"$LOG_DIR/${name#c1-}.cid" 2>"$LOG_DIR/${name#c1-}.launch.err"
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
import sys, urllib.error, urllib.request
url = sys.argv[1]
# First line = HTTP status (callers assert exactly 200); the body follows.
try:
    with urllib.request.urlopen(url, timeout=5) as resp:
        status, body = int(resp.status), resp.read()
except urllib.error.HTTPError as exc:
    status, body = int(exc.code), exc.read()
sys.stdout.buffer.write(f"{status}\n".encode("utf-8"))
sys.stdout.buffer.write(body)
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

argv: path qty halt_mode [halt_reason [contract [expect_dry_run]]]
  halt_mode: true|false|any
  expect_dry_run: true (default) | false  — the decision row's dry_run must equal this exactly
"""
import json, sys
path, qty_s, halt_mode = sys.argv[1], sys.argv[2], sys.argv[3]
halt_reason = sys.argv[4] if len(sys.argv) > 4 else ""
contract = sys.argv[5] if len(sys.argv) > 5 else ""
expect_dry_run = (sys.argv[6] if len(sys.argv) > 6 else "true") != "false"
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
need(d.get("dry_run") is expect_dry_run, f"dry_run={d.get('dry_run')} want {expect_dry_run}")
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
  # Writes the body to <out> and the HTTP status to <out>.status; returns non-zero
  # unless the status is exactly 200 (a 201/204 must not read as a healthy probe).
  local name="$1" url="$2" out="$3"
  docker cp "$LOG_DIR/_http_get.py" "$name:/tmp/_http_get.py" >/dev/null || return 1
  docker exec "$name" python /tmp/_http_get.py "$url" >"$out.raw" || return 1
  head -1 "$out.raw" >"$out.status"
  tail -n +2 "$out.raw" >"$out"
  grep -qx 200 "$out.status"
}

http_post_in() {
  local name="$1" url="$2" body="$3" out="$4"
  docker cp "$LOG_DIR/_http_post.py" "$name:/tmp/_http_post.py" >/dev/null || return 1
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

# Run a pytest subset INSIDE a built image (tests/ + lock + pyproject mounted
# read-only; PYTHONPATH points at the image's own /app modules so the code under
# test is the deployed code, not the repo checkout). Returns 0 only when pytest
# exits 0 AND at least one test actually ran (Codex P1, 2026-09-11: a session
# that executed zero in-image tests must not read as PASS).
image_pytest() {
  local image="$1" pythonpath="$2" logf="$3"; shift 3
  local extra_mounts=()
  while [[ "${1:-}" == "-v" ]]; do extra_mounts+=("$1" "$2"); shift 2; done
  mkdir -p "${HOME:-/root}/.cache/pip"
  set +e
  docker run --rm \
    -v "$ROOT/tests:/work/tests:ro" \
    -v "$ROOT/requirements-ops.lock:/work/requirements-ops.lock:ro" \
    -v "$ROOT/pyproject.toml:/work/pyproject.toml:ro" \
    -v "${HOME:-/root}/.cache/pip:/root/.cache/pip" \
    "${extra_mounts[@]}" \
    -e "PYTHONPATH=$pythonpath" \
    -w /work "$image" \
    bash -lc "python -m pip install --require-hashes -r requirements-ops.lock >/tmp/pip.log 2>&1 || { cat /tmp/pip.log; exit 97; }; python -m pytest -q -p no:cacheprovider $*" \
    >"$logf" 2>&1
  local rc=$?
  set -e
  local passed
  passed="$(grep -oE '[0-9]+ passed' "$logf" | tail -1 | awk '{print $1}')"
  [[ "$rc" -eq 0 && -n "$passed" && "$passed" -gt 0 ]]
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
    local dep
    for dep in L2 L3 L4 L5a L5b L6 L6b L7 L8 L9; do record_fail "$dep" "not runnable: listener image build failed (L1)"; done
    return 0
  fi

  local files="$LOG_DIR/L2_files.txt" exp="$LOG_DIR/L2_expected.txt"
  local probe_ok=1
  if ! docker run --rm --network none --entrypoint find "$LISTENER_TAG" /app -type f | sort >"$files"; then probe_ok=0; fi
  printf '%s\n' "${LISTENER_FILES[@]}" | sort >"$exp"
  local l2=1
  [[ "$probe_ok" -eq 1 ]] || l2=0   # an image that cannot run `find` is a FAIL, not a script abort
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
  if launch_container c1-L3 --network none -v "$d3:/data" "$LISTENER_TAG" \
     && wait_for_log c1-L3 'WAIT:' 10 "$LOG_DIR/L3.log" && container_alive c1-L3; then
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
    local l4=1
    launch_container c1-L4 --network none -v "$d4:/data" "$LISTENER_TAG" || l4=0
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
)" || l5b=0
      [[ -n "$csha" ]] || l5b=0   # a broken contract-hash probe is a validation result, not a harness abort
    fi
    local bar_b; bar_b="ci-l5b-$(python3 -c 'import uuid;print(uuid.uuid4())')"
    local body_b; body_b="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar_b','close':42000.0,'stop_dist_pts':1.0}))")"
    if [[ "$l5b" -eq 1 ]]; then
      http_post_in c1-L4 "http://127.0.0.1:8080/c1/${tok}" "$body_b" "$LOG_DIR/L5b.out" 2>"$LOG_DIR/L5b.post.err" || l5b=0
      # The helper can fail before creating its output (e.g. docker cp). Read
      # under a guard so missing response evidence fails this check, not the run.
      grep -q 'dry_run: computed, not sent' "$LOG_DIR/L5b.out" || l5b=0
      head -1 "$LOG_DIR/L5b.out" | grep -qx 200 || l5b=0
      docker exec c1-L4 cat /data/c1_rail_events.jsonl >"$LOG_DIR/L5b.events" 2>/dev/null \
        || cp "$d4/c1_rail_events.jsonl" "$LOG_DIR/L5b.events" || l5b=0
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
  local l6=1
  launch_container c1-L6 --network none -v "$d6:/data" "$LISTENER_TAG" || l6=0
  wait_for_log c1-L6 'dry_run=False' 15 "$LOG_DIR/L6.log" || l6=0
  local tok; tok="$(path_token)"
  local bar6; bar6="ci-l6-$(python3 -c 'import uuid;print(uuid.uuid4())')"
  local body6; body6="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar6','close':42000.0,'stop_dist_pts':1.0}))")"
  if container_alive c1-L6; then
    http_post_in c1-L6 "http://127.0.0.1:8080/c1/${tok}" "$body6" "$LOG_DIR/L6.out" 2>"$LOG_DIR/L6.post.err" || l6=0
    head -1 "$LOG_DIR/L6.out" | grep -qx 200 || l6=0   # a halted decision is still a 200 "halted: …" reply
    docker exec c1-L6 cat /data/c1_rail_events.jsonl >"$LOG_DIR/L6.events" 2>/dev/null \
      || cp "$d6/c1_rail_events.jsonl" "$LOG_DIR/L6.events" || l6=0
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
  local l6b=1
  launch_container c1-L6b --network none -v "$d6b:/data" "$LISTENER_TAG" || l6b=0
  wait_for_log c1-L6b 'dry_run=True armed_until=-' 15 "$LOG_DIR/L6b.log" || l6b=0
  local bar6b; bar6b="ci-l6b-$(python3 -c 'import uuid;print(uuid.uuid4())')"
  local body6b; body6b="$(python3 -c "import json;print(json.dumps({'leg_id':'m1_stage1_test','signal_type':'entry','bar_time':'$bar6b','close':42000.0,'stop_dist_pts':1.0}))")"
  if container_alive c1-L6b; then
    http_post_in c1-L6b "http://127.0.0.1:8080/c1/${tok}" "$body6b" "$LOG_DIR/L6b.out" 2>"$LOG_DIR/L6b.post.err" || l6b=0
    head -1 "$LOG_DIR/L6b.out" | grep -qx 200 || l6b=0
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
  local l7=1
  launch_container c1-L7 --network none -v "$d7:/data" --entrypoint sleep "$LISTENER_TAG" infinity || l7=0
  local before after; before="$(sha256_file "$d7/c1_rail_config.json")"
  docker exec c1-L7 python ops/c1_rail/c1_rail_arm.py --status --config /data/c1_rail_config.json \
    >"$LOG_DIR/L7.status" 2>&1 || l7=0
  grep -q "m1_gate: status='CODE_LANDED' result=FAIL" "$LOG_DIR/L7.status" || l7=0
  set +e
  docker exec c1-L7 python ops/c1_rail/c1_rail_arm.py --arm --hours 1 --config /data/c1_rail_config.json \
    >"$LOG_DIR/L7.arm" 2>&1
  local arc=$?
  set -e
  [[ "$arc" -eq 1 ]] || l7=0   # the validated refusal path exits 1; any other status is a regression
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
  if launch_container c1-L8 --network none -v "$d8:/data" "$LISTENER_TAG" \
     && wait_for_log c1-L8 'dry_run=True armed_until=-' 15 "$LOG_DIR/L8.log" \
     && grep -q 'IMPLICIT DISARM' "$LOG_DIR/L8.log" \
     && container_alive c1-L8; then
    record_pass L8 "IMPLICIT DISARM on expired armed_until; alive"
  else
    record_fail L8 "see L8.log (or the container exited after disarm)"
  fi
  stop_rm c1-L8

  # L9 compatible listener tests run against the BUILT listener image (Codex P2,
  # 2026-09-11): the slim suite exercises repo source in python:3.12-slim, not the
  # image that deploys. Subset = files whose imports resolve from /app alone; the
  # F2 sizing oracle is data and is mounted read-only for test_c1_sizing_host_reference.
  local l9_files=(
    tests/ops/test_c1_rail_arm.py
    tests/ops/test_c1_rail_http_server.py
    tests/ops/test_c1_rail_listener.py
    tests/ops/test_c1_rail_slippage.py
    tests/ops/test_c1_rail_telemetry.py
    tests/ops/test_c1_sizing_host_reference.py
    tests/ops/test_m1_stage1_listener.py
    tests/ops/test_m1_stage1_control.py
    tests/ops/test_m1_acceptance_drills.py
    tests/ops/test_crosstrade_payload.py
  )
  local f2="$ROOT/lab/analysis/c1/q_rail_1_2026-07/f2_floors.json"
  if image_pytest "$LISTENER_TAG" "/app/ops/c1_rail:/app/core:/app/ops:/app" "$LOG_DIR/L9_inimage.log" \
       -v "$f2:/work/lab/analysis/c1/q_rail_1_2026-07/f2_floors.json:ro" "${l9_files[@]}"; then
    record_pass L9 "listener-image tests executed and green" "$(grep -E 'passed|failed|error' "$LOG_DIR/L9_inimage.log" | tail -1)"
  else
    record_fail L9 "listener-image tests failed or did not execute; see L9_inimage.log" "$(grep -E 'passed|failed|error' "$LOG_DIR/L9_inimage.log" | tail -1)"
  fi
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
    local dep
    for dep in D2 D3 D4 D5 D6 D7 D8 D9 D10 D11; do record_fail "$dep" "not runnable: daemon image build failed (D1)"; done
    return 0
  fi

  local files="$LOG_DIR/D2_files.txt" exp="$LOG_DIR/D2_expected.txt"
  local probe_ok=1
  if ! docker run --rm --network none --entrypoint find "$DAEMON_TAG" /app -type f | sort >"$files"; then probe_ok=0; fi
  printf '%s\n' "${DAEMON_FILES[@]}" | sort >"$exp"
  local d2=1
  [[ "$probe_ok" -eq 1 ]] || d2=0   # an image that cannot run `find` is a FAIL, not a script abort
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
    return {norm(r["name"]) for r in json.loads(out)}

def norm(name):
    # PEP 503 normalization: runs of -, _ and . are equivalent; compare canonical forms.
    import re as _re
    return _re.sub(r"[-_.]+", "-", name).lower()

base, img = dists("python:3.12-slim"), dists(sys.argv[1])
extras = sorted(img - base)
req = Path("deploy/c1_signal_daemon/requirements.txt")
if not req.exists():
    expected = []
else:
    text = req.read_text(encoding="utf-8")
    # Every logical requirement (backslash-continued lines joined) must carry its
    # own --hash= (Codex P2, 2026-09-11): a single hashed line must not vouch for
    # an unpinned neighbour. Options (-r/--index-url…) and comments are skipped.
    logical=[]; buf=""
    for raw in text.splitlines():
        line=raw.split("#",1)[0].rstrip()
        if line.endswith("\\"):
            buf += line[:-1] + " "; continue
        buf += line
        if buf.strip(): logical.append(buf.strip())
        buf=""
    if buf.strip(): logical.append(buf.strip())
    names=[]
    for item in logical:
        if item.startswith("-"): continue
        if "--hash=" not in item or "==" not in item:
            print(f"FAIL: requirement without a pin and hash: {item.split()[0]}")
            sys.exit(2)
        names.append(norm(item.split("==")[0].split("[")[0].strip()))
    expected=sorted(set(n for n in names if n))
print(json.dumps({"extras":extras,"expected":expected}, sort_keys=True))
sys.exit(0 if extras==expected else 1)
PY
  python3 "$LOG_DIR/D2_pip.py" "$DAEMON_TAG" >"$LOG_DIR/D2_pip.json" 2>"$LOG_DIR/D2_pip.err" || d2=0
  if [[ "$d2" -eq 1 ]]; then record_pass D2 "COPY exact; no databento; extras match" "$(cat "$LOG_DIR/D2_pip.json")"
  else record_fail D2 "see D2_diff.txt / D2_pip.err" "$(cat "$LOG_DIR/D2_pip.json" 2>/dev/null | tr -d '\n')"; fi

  local d3="$LOG_DIR/D3_data"; rm -rf "$d3"; mkdir -p "$d3"
  stop_rm c1-D3
  if launch_container c1-D3 --network none -v "$d3:/data" "$DAEMON_TAG" \
     && wait_for_log c1-D3 'WAIT:' 10 "$LOG_DIR/D3.log" && container_alive c1-D3; then
    record_pass D3 "WAIT present; alive"
  else record_fail D3 "see D3.log"; fi
  stop_rm c1-D3

  # D4 inert boot
  local d4="$LOG_DIR/D4_data"
  stage_daemon_data "$d4" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D4
  local d4ok=1
  launch_container c1-D4 --network none -v "$d4:/data" "$DAEMON_TAG" || d4ok=0
  wait_for_log c1-D4 'daemon up' 15 "$LOG_DIR/D4.log" || d4ok=0
  grep -Eq 'daemon up bind=.+:.+ emit_enabled=false boot_id=' "$LOG_DIR/D4.log" || d4ok=0
  host_readable_data c1-D4
  http_get_in c1-D4 'http://127.0.0.1:8080/' "$LOG_DIR/D4.get" 2>"$LOG_DIR/D4.get.err" || d4ok=0
  cat >"$LOG_DIR/D4_health.py" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
need={"emit_enabled":False,"effective_emit":False,"strategy":"NullStrategy",
      "feed_mode":"operator_input","poll_interval_s":5,"connected":False,"feed_healthy":False,
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
  rm -rf "$LOG_DIR/D4_data_cp"   # never let a previous run's snapshot stand in for this one
  docker cp c1-D4:/data "$LOG_DIR/D4_data_cp" >/dev/null 2>&1 || rm -rf "$LOG_DIR/D4_data_cp"
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
  local d5ok=1
  launch_container c1-D5 --network none -v "$d5:/data" "$DAEMON_TAG" || d5ok=0
  wait_for_log c1-D5 'daemon up' 15 "$LOG_DIR/D5.log" || d5ok=0
  host_readable_data c1-D5
  http_get_in c1-D5 'http://127.0.0.1:8080/' "$LOG_DIR/D5.get" 2>"$LOG_DIR/D5.get.err" || d5ok=0
  python3 "$LOG_DIR/D4_health.py" "$LOG_DIR/D5.get" >"$LOG_DIR/D5.health" 2>"$LOG_DIR/D5.health.err" || d5ok=0
  sleep 5
  # Still alive after the interval (Codex P2, 2026-09-11): a daemon that exits on
  # the stale-enabled config must not validate as "inert".
  container_alive c1-D5 || d5ok=0
  docker logs c1-D5 >"$LOG_DIR/D5.log" 2>&1 || true
  # A transport attempt that fails logs only a `step … transport_unknown` record
  # (no b1_post marker), so step records are rejected here exactly as in D4.
  grep -E 'step |b1_post|m1_b1_post' "$LOG_DIR/D5.log" >/dev/null && d5ok=0
  if [[ "$d5ok" -eq 1 ]]; then record_pass D5 "stale-enabled stays inert; alive after interval"
  else record_fail D5 "see D5.log"; fi
  stop_rm c1-D5

  # D6 standalone CLI: three refusals without any state/config/publication write.
  local d6="$LOG_DIR/D6_data" d6ok=1
  stage_daemon_data "$d6" "$FIXTURES/c1_signal_daemon_config.json"
  python3 - "$d6/c1_signal_daemon_config.json" <<'PY' || d6ok=0
import json,sys
from pathlib import Path
p=Path(sys.argv[1]); cfg=json.loads(p.read_text()); cfg["poll_interval_s"]=1
p.write_text(json.dumps(cfg))
PY
  stop_rm c1-D6seed
  if launch_container c1-D6seed --network none -v "$d6:/data" "$DAEMON_TAG"; then
    wait_for_log c1-D6seed 'daemon up' 15 "$LOG_DIR/D6.seed.log" || d6ok=0
  else d6ok=0; fi
  stop_rm c1-D6seed
  cat >"$LOG_DIR/D6_probe.py" <<'PY'
import hashlib,json,os,subprocess,sys,tempfile
from datetime import datetime,timezone
from pathlib import Path
sys.path[:0]=["/app/ops", "/app"]
from c1_rail.m1_stage1_contract import contract_sha256
from c1_signal_daemon.m1_stage1_control import validate_manifest

data=Path("/data")
state=data/"c1_m1_stage1_state.json"
config=data/"c1_signal_daemon_config.json"
value=json.loads(Path("/tmp/ceremony_manifest.json").read_text())
value["contract_sha256"]=contract_sha256()  # computed from this image
validate_manifest(value, datetime.now(timezone.utc))
# The Docker-copied fixture is input only. Generate into a private directory
# owned by this process rather than rewriting a copied file in shared /tmp.
manifest=Path(tempfile.mkdtemp(prefix="c1-d6-"))/"ceremony_manifest.json"
manifest.write_text(json.dumps(value))
boot=json.loads(state.read_text())["boot_id"]
cid=value["ceremony_id"]
upload=data/f"m1_upload_{cid}.json"
env=dict(os.environ); env.pop("PYTHONPATH", None)
cli=[sys.executable,"ops/c1_signal_daemon/m1_stage1_control.py"]
common=["--state",str(state),"--config",str(config)]
def hashes():
    return tuple(hashlib.sha256(p.read_bytes()).hexdigest() for p in (config,state))
original=hashes()
actions=[
    ("prepare",["--boot-id","stale-boot","--manifest",str(manifest)]),
    ("enable",["--boot-id",boot,"--manifest",str(manifest),"--ceremony-id","does-not-exist"]),
    ("inject",["--boot-id",boot,"--ceremony-id",cid,"--contract",value["venue_contract"],
               "--time",value["target"],"--bar-file",str(upload)]),
]
for action,args in actions:
    if action=="inject":
        upload.write_text(json.dumps({"open":41000,"high":41002,"low":40999,"close":41001,"volume":3}))
    result=subprocess.run(cli+[action]+common+args,cwd="/app",env=env,
                          capture_output=True,text=True,timeout=10)
    assert result.returncode==2, f"{action} exit={result.returncode}"
    expected="inject refused: not active" if action=="inject" else "ceremony control failed closed"
    assert result.stdout.strip()==expected and not result.stderr, f"{action} unexpected output"
    assert hashes()==original, f"{action} changed config/state"
    assert not list(data.glob("m1_bar_*")) and not list(data.glob("m1_claim_*"))
    assert not upload.exists(), f"{action} upload retained"
    print(f"{action}: exit=2; config/state hashes unchanged; upload/bar/claim absent")
result=subprocess.run(cli+["status"]+common,cwd="/app",env=env,
                      capture_output=True,text=True,timeout=10)
assert result.returncode==0 and not result.stderr
status=json.loads(result.stdout)
assert status["effective_emit"] is False and status["source_status"]=="disconnected"
assert hashes()==original
print(json.dumps(status,sort_keys=True))
PY
  stop_rm c1-D6
  if launch_container c1-D6 --network none -v "$d6:/data" --entrypoint sleep "$DAEMON_TAG" infinity; then
    docker cp "$FIXTURES/ceremony_manifest.json" c1-D6:/tmp/ceremony_manifest.json >/dev/null || d6ok=0
    docker cp "$LOG_DIR/D6_probe.py" c1-D6:/tmp/D6_probe.py >/dev/null || d6ok=0
    docker exec c1-D6 python /tmp/D6_probe.py >"$LOG_DIR/D6.out" 2>"$LOG_DIR/D6.err" || d6ok=0
  else d6ok=0; fi
  if [[ "$d6ok" -eq 1 ]]; then record_pass D6 "prepare/enable/inject exit 2; hashes unchanged; no input files" "$(tr '\n' ' ' <"$LOG_DIR/D6.out")"
  else record_fail D6 "see D6.out / D6.err / D6.launch.err"; fi
  stop_rm c1-D6

  # D7 ownership
  local d7="$LOG_DIR/D7_data"
  stage_daemon_data "$d7" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D7
  local d7ok=1
  launch_container c1-D7 --network none -v "$d7:/data" "$DAEMON_TAG" || d7ok=0
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
  local d8ok=1
  stage_daemon_data "$d8" "$FIXTURES/c1_signal_daemon_config.json"
  stop_rm c1-D8a
  launch_container c1-D8a --network none -v "$d8:/data" "$DAEMON_TAG" || d8ok=0
  wait_for_log c1-D8a 'daemon up' 15 "$LOG_DIR/D8a.log" || d8ok=0
  host_readable_data c1-D8a
  python3 "$LOG_DIR/D4_state.py" "$d8" >"$LOG_DIR/D8a.state" 2>"$LOG_DIR/D8a.err" || d8ok=0
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
  launch_container c1-D8b --network none -v "$d8:/data" "$DAEMON_TAG" || d8ok=0
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
  # The restarted daemon must still be running (logs and bind-mounted state survive
  # a stopped container, so the assertions above cannot tell on their own).
  container_alive c1-D8b || d8ok=0
  if [[ "$d8ok" -eq 1 ]]; then record_pass D8 "boot_id changed; generation+1; lock initialized; alive"
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
  local slim_rc=1
  if [[ "${#d9_list[@]}" -gt 0 ]]; then
    set +e
    docker run --rm \
      -v "$ROOT:/work:ro" \
      -v "${HOME:-/root}/.cache/pip:/root/.cache/pip" \
      -w /work python:3.12-slim \
      bash -lc "python -m pip install --require-hashes -r requirements-ops.lock >/tmp/pip.log 2>&1 && python -m pytest -q ${d9_list[*]}" \
      >"$LOG_DIR/D9_slim.log" 2>&1
    slim_rc=$?
    set -e
  else
    echo "No focused test paths selected; refusing unrestricted pytest discovery" >"$LOG_DIR/D9_slim.log"
  fi
  [[ "$slim_rc" -eq 0 ]] || d9ok=0
  grep -Eq '(^|[[:space:]])[1-9][0-9]* passed' "$LOG_DIR/D9_slim.log" || d9ok=0
  # Daemon-image subset: files whose imports resolve from /app/ops alone (the
  # listener-importing tests and the image-manifest test read the repo tree and
  # run in the slim cell only). The subprocess lock test prepends a nonexistent
  # /work/ops but tests/conftest.py preserves PYTHONPATH for children, so its child
  # interpreters resolve the image's /app/ops modules — it runs here deliberately.
  # The subset must execute and pass (Codex P1, 2026-09-11) — no escape hatch.
  local d9_image_files=(
    tests/ops/test_c1_signal_daemon_b1_payload.py
    tests/ops/test_c1_signal_daemon_evaluate_loop.py
    tests/ops/test_c1_signal_daemon_feed.py
    tests/ops/test_c1_signal_daemon_listener_client.py
    tests/ops/test_c1_signal_daemon_m1.py
    tests/ops/test_c1_signal_daemon_source_retirement.py
    tests/ops/test_c1_signal_daemon_transport.py
    tests/ops/test_c1_signal_daemon_operator_input.py
    tests/ops/test_c1_signal_daemon_inject.py
    tests/ops/test_c1_signal_daemon_cli_bootstrap.py
  )
  local in_ok=1
  image_pytest "$DAEMON_TAG" "/app/ops:/app" "$LOG_DIR/D9_inimage.log" \
    "${d9_image_files[@]}" || in_ok=0
  [[ "$in_ok" -eq 1 ]] || d9ok=0
  {
    echo "slim_rc=$slim_rc inimage_ok=$in_ok"
    echo "slim_files=${#d9_list[@]} paths=${d9_list[*]}"
    echo "inimage_files=${#d9_image_files[@]} paths=${d9_image_files[*]}"
    echo -n "slim_counts "; grep -E 'passed|failed|error|skipped' "$LOG_DIR/D9_slim.log" | tail -1 || echo "(no summary)"
    echo -n "inimage_counts "; grep -E 'passed|failed|error|skipped' "$LOG_DIR/D9_inimage.log" | tail -1 || echo "(no summary)"
  } >"$LOG_DIR/D9_summary.txt"
  cat "$LOG_DIR/D9_summary.txt"
  if [[ "$d9ok" -ne 1 ]]; then
    echo "---- D9_slim.log (tail) ----"
    tail -n 80 "$LOG_DIR/D9_slim.log" || true
    echo "---- D9_inimage.log (tail) ----"
    tail -n 40 "$LOG_DIR/D9_inimage.log" || true
  fi
  if [[ "$d9ok" -eq 1 ]]; then record_pass D9 "slim suite green; daemon-image subset executed and green" "$(tr '\n' ' ' <"$LOG_DIR/D9_summary.txt")"
  else record_fail D9 "slim suite failed, or the daemon-image subset failed / did not execute; see D9_slim.log / D9_inimage.log" "$(tr '\n' ' ' <"$LOG_DIR/D9_summary.txt")"; fi

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
    # Choose the first quarterly third Friday on/after this probe's target.
    venues = []
    for year in (target.year, target.year + 1):
        for month, code in ((3, "H"), (6, "M"), (9, "U"), (12, "Z")):
            first = target.date().replace(year=year, month=month, day=1)
            expiry = first + timedelta(days=(4 - first.weekday()) % 7 + 14)
            if expiry >= target.date():
                venues.append((expiry, f"MYM{code}{year % 10}"))
    manifest = {
        "ceremony_id": cid,
        "target": target.isoformat(),
        "expires": (target + timedelta(seconds=140)).isoformat(),
        "source": source_binding,
        "venue_contract": min(venues)[1],
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
        def activate(self, binding, *, ceremony_id): assert binding == self.binding
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
    if not isinstance(result, dict) or result.get("action") != "transport_unknown":
        raise SystemExit(f"step must return transport_unknown, got {result!r}")
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

  # D11 real-clock, one-shot input in the daemon image. Docker launch/health
  # failures never enter the long wait. All CLI calls use the standalone A7 form.
  local d11="$LOG_DIR/D11_data" d11ok=1
  local d11_start=$SECONDS
  stage_daemon_data "$d11" "$FIXTURES/c1_signal_daemon_config.json"
  python3 - "$d11/c1_signal_daemon_config.json" <<'PY' || d11ok=0
import json,sys
from pathlib import Path
p=Path(sys.argv[1]); cfg=json.loads(p.read_text())
cfg.update(poll_interval_s=1,bar_period_s=60,strategy="null",emit_enabled=False,
           listener_base_url="http://127.0.0.1:9")
p.write_text(json.dumps(cfg))
PY
  cat >"$LOG_DIR/D11_probe.py" <<'PY'
"""D11: exercise the packaged CLI and daemon, using this probe's UTC clock."""
import json,math,os,subprocess,sys,time,urllib.request
from datetime import date,datetime,timedelta,timezone
from pathlib import Path
from uuid import uuid4

DATA=Path("/data")
STATE=DATA/"c1_m1_stage1_state.json"
CONFIG=DATA/"c1_signal_daemon_config.json"
CLI=[sys.executable,"ops/c1_signal_daemon/m1_stage1_control.py"]
COMMON=["--state",str(STATE),"--config",str(CONFIG)]
VALUES=("41000","41001","40999","41002")

def command(action, expected, *args):
    env=dict(os.environ); env.pop("PYTHONPATH",None)
    result=subprocess.run(CLI+[action]+COMMON+list(args),env=env,
                          capture_output=True,text=True,timeout=10)
    # Never amplify a runtime leak into the validator's own stdout/traceback.
    assert not any(value in result.stdout+result.stderr for value in VALUES), "bar value leaked"
    assert result.returncode==expected, f"{action} exit={result.returncode}, expected={expected}"
    assert not result.stderr, f"{action} unexpected stderr"
    print(f"{action} exit={result.returncode} {result.stdout.strip()}",flush=True)
    return result.stdout

def wait_until(checkpoint, *, latest):
    remaining=checkpoint-time.time()
    while remaining>0:
        time.sleep(min(remaining,1))
        remaining=checkpoint-time.time()
    assert time.time()<latest, "missed injection checkpoint"

def health():
    with urllib.request.urlopen("http://127.0.0.1:8080/",timeout=2) as response:
        assert response.status==200
        return json.load(response)

def await_health(expected):
    deadline=time.monotonic()+5
    while True:
        value=health()
        if all(value.get(key)==want for key,want in expected.items()):
            print("health "+json.dumps({key:value[key] for key in expected},sort_keys=True),flush=True)
            return value
        remaining=deadline-time.monotonic()
        assert remaining>0, "health checkpoint timed out"
        time.sleep(min(.1,remaining))

def venue_contract(target):
    for year in (target.year,target.year+1):
        for month,code in ((3,"H"),(6,"M"),(9,"U"),(12,"Z")):
            first=date(year,month,1)
            expiry=first+timedelta(days=(4-first.weekday())%7+14)
            if expiry>=target.date():
                return f"MYM{code}{year%10}"
    raise AssertionError("no quarterly contract")

def manifest(contract_hash, source):
    target=datetime.fromtimestamp(math.ceil((time.time()+20)/60)*60,timezone.utc)
    return dict(ceremony_id="ci-d11-"+uuid4().hex[:12],target=target.isoformat(),
                expires=(target+timedelta(seconds=150)).isoformat(),
                source=source,venue_contract=venue_contract(target),
                contract_sha256=contract_hash,expected_qty=1,preflight_sha256="e"*64)

def publication_identity(path):
    try:
        stat=path.stat()
        return stat.st_ino,stat.st_mtime_ns,stat.st_size
    except FileNotFoundError:
        return None

def main():
    sys.path[:0]=["/app/ops","/app"]
    from c1_rail.m1_stage1_contract import contract_sha256,OPERATOR_INPUT_SOURCE
    from c1_signal_daemon.m1_stage1_control import validate_manifest
    from c1_signal_daemon.m1_stage1_state import CeremonyStore
    started=time.monotonic()
    initial=await_health(dict(poll_interval_s=1,feed_mode="operator_input",
                              effective_emit=False,connected=False,ceremony_state="DISABLED"))
    boot=initial["boot_id"]
    assert boot
    value=manifest(contract_sha256(),OPERATOR_INPUT_SOURCE)
    validate_manifest(value,datetime.now(timezone.utc))
    cid=value["ceremony_id"]
    target=datetime.fromisoformat(value["target"]).timestamp()
    assert 19<=target-time.time()<=80
    path=DATA/f"m1_manifest_{cid}.json"
    path.write_text(json.dumps(value))
    upload=DATA/f"m1_upload_{cid}.json"
    published=DATA/f"m1_bar_{cid}.json"
    claim=DATA/f"m1_claim_{cid}"
    binding=["--boot-id",boot,"--manifest",str(path)]
    injection=["--ceremony-id",cid,"--boot-id",boot,"--contract",value["venue_contract"],
               "--time",value["target"]]
    def stage():
        upload.write_text(json.dumps(dict(open=41000,high=41002,low=40999,close=41001,volume=3)))
    command("prepare",0,*binding)
    status=json.loads(command("status",0))
    assert status["state"]=="READY" and status["effective_emit"] is False
    await_health(dict(effective_emit=False))
    command("enable",0,*binding,"--ceremony-id",cid)
    await_health(dict(effective_emit=True,ceremony_state="READY",connected=False))

    stage()
    wait_until(target+59,latest=target+60)
    early=command("inject",2,*injection,"--bar-file",str(upload))
    assert early.strip()=="inject refused: before window"
    assert not upload.exists() and not published.exists() and not claim.exists()
    print("early refusal: upload/bar/claim absent",flush=True)
    stage()
    wait_until(target+61,latest=target+70)
    receipt=json.loads(command("inject",0,*injection,"--bar-file",str(upload)))
    received=time.monotonic()
    assert target+61<=datetime.fromisoformat(receipt["published_at"]).timestamp()<=target+70
    assert len(receipt["bar_sha256"])==64 and not upload.exists()
    # Capture publication identity before the immediate duplicate. Deactivation
    # may remove it concurrently; the duplicate must never create/replace it.
    before=publication_identity(published)
    stage()
    duplicate=command("inject",2,*injection,"--bar-file",str(upload))
    assert duplicate.strip() in {"inject refused: already injected",
                                 "inject refused: not enabled","inject refused: not active"}
    after=publication_identity(published)
    assert not upload.exists() and (after is None or after==before)
    print("duplicate refusal: upload absent; no new publication",flush=True)

    store=CeremonyStore(STATE)
    deadline=received+5
    while True:
        obj=store.read(); item=obj["ceremonies"][cid]
        if (item["state"]=="TRANSPORT_UNKNOWN" and not published.exists() and not claim.exists()):
            assert obj["enabled"] is False and item["bar_sha256"]==receipt["bar_sha256"]
            assert time.monotonic()<=deadline, "terminal/cleanup exceeded five seconds"
            break
        remaining=deadline-time.monotonic()
        assert remaining>0, "terminal/cleanup exceeded five seconds"
        time.sleep(min(.05,remaining))
    print(json.dumps(dict(state=item["state"],enabled=obj["enabled"],
                          receipt_bar_sha256=receipt["bar_sha256"],journal_bar_sha256=item["bar_sha256"],
                          upload_absent=not upload.exists(),bar_absent=True,claim_absent=True)),flush=True)
    # Stable terminal state avoids mistaking a legitimate reservation write for
    # a bad-path write. Take the journal lock as an additional race guard: path
    # validation must refuse without trying to acquire it.
    with store.locked():
        before_state=STATE.read_bytes()
        bad_path=command("inject",2,*injection,"--bar-file",str(STATE))
        assert bad_path.strip()=="inject refused: bad upload path"
        assert STATE.read_bytes()==before_state
    print("protected-path refusal: state byte-identical",flush=True)
    command("close",0,"--ceremony-id",cid)
    obj=store.read(); item=obj["ceremonies"][cid]
    assert item["state"]=="CLOSED" and item["previous_state"]=="TRANSPORT_UNKNOWN"
    assert obj["enabled"] is False
    # Fresh future manifest makes the refusal prove the unresolved-attempt
    # barrier, not a stale target, reused ID, or invalid quarterly contract.
    fresh=manifest(contract_sha256(),OPERATOR_INPUT_SOURCE)
    validate_manifest(fresh,datetime.now(timezone.utc))
    fresh_path=DATA/f"m1_manifest_{fresh['ceremony_id']}.json"
    fresh_path.write_text(json.dumps(fresh))
    before_state=STATE.read_bytes(); before_config=CONFIG.read_bytes()
    refused=command("prepare",2,"--boot-id",boot,"--manifest",str(fresh_path))
    assert refused.strip()=="ceremony control failed closed"
    assert STATE.read_bytes()==before_state and CONFIG.read_bytes()==before_config
    assert fresh["ceremony_id"] not in store.read()["ceremonies"]
    await_health(dict(effective_emit=False))
    assert not upload.exists() and not published.exists() and not claim.exists()
    assert time.monotonic()-started<240, "D11 exceeded four minutes"
    print("CLOSED previous_state=TRANSPORT_UNKNOWN; fresh prepare refused; effective_emit=false",flush=True)

if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        # Exception details may contain captured private values (e.g. JSON
        # decoder diagnostics). Keep failures useful without printing locals.
        print("D11 probe failed: "+type(exc).__name__,file=sys.stderr)
        raise SystemExit(1)
PY
  stop_rm c1-D11
  if [[ "$d11ok" -eq 1 ]] && launch_container c1-D11 --network none -v "$d11:/data" "$DAEMON_TAG"; then
    if wait_for_log c1-D11 'daemon up' 15 "$LOG_DIR/D11.boot.log" \
       && docker cp "$LOG_DIR/D11_probe.py" c1-D11:/tmp/D11_probe.py >/dev/null; then
      local d11_budget=$((240 - (SECONDS - d11_start)))
      if [[ "$d11_budget" -gt 0 ]]; then
        timeout "$d11_budget" docker exec c1-D11 python /tmp/D11_probe.py >"$LOG_DIR/D11.out" 2>"$LOG_DIR/D11.err" || d11ok=0
      else d11ok=0; fi
    else d11ok=0; fi
  else
    d11ok=0
    cp "$LOG_DIR/D11.launch.err" "$LOG_DIR/D11.err" 2>/dev/null || true
  fi
  docker logs c1-D11 >"$LOG_DIR/D11.log" 2>&1 || d11ok=0
  [[ $(grep -c "step {'action': 'transport_unknown'}" "$LOG_DIR/D11.log" || true) -eq 1 ]] || d11ok=0
  # No raw journal dump: it deliberately retains the bar for evidence joins.
  if grep -E '41000|41001|40999|41002' "$LOG_DIR/D11.log" "$LOG_DIR/D11.out" "$LOG_DIR/D11.err" >/dev/null 2>&1; then d11ok=0; fi
  [[ $((SECONDS - d11_start)) -le 240 ]] || d11ok=0
  container_alive c1-D11 || d11ok=0
  if [[ "$d11ok" -eq 1 ]]; then
    record_pass D11 "one receipt; one transport_unknown; matching bar hash; cleanup; close/barrier; no values"
    cat "$LOG_DIR/D11.out"
  else record_fail D11 "see D11.out / D11.err / D11.log"; fi
  stop_rm c1-D11
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
