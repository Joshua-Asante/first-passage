# M1 Stage 1 test contract — 2026-09-10

Status: offline implementation on `codex/m1-stage1-test`, based on `1eb2b21`.
User approved this identity, one-micro cap, entry-only permanent dry-run restriction,
and offline implementation. No deployment, live configuration change, feed connection,
POST, arming, order, or M1 acceptance evidence is authorized by this document.
M1 remains `CODE_LANDED`; item 5 and operator signoff remain owed.

## Frozen sizing contract

| Input | Frozen value |
|---|---|
| Identity / lifecycle key | `m1_stage1_test` / `M1 Stage1 Test` |
| Instrument / B1 listener route | MYM / `MYM1!` |
| Tier / starting-balance sizing basis | `Tradeify_Select_100K` / 100000 |
| Base risk fraction | `0.0000125` (0.00125%) |
| Stop distance | `1.0` point, one MYM tick |
| Dollars per point | `0.5` |
| Pyramid / dedicated cap | `0.0` / at most 1 micro |
| Lifecycle default / attended test | `RETIRED` / `AUTHORIZED` (multiplier 1) |
| Generated cap / attended test | 0 / 1 |

The source owners are `core/firm_rules.py`, `core/dd_protection.py`,
`core/lifecycle.py`, `ops/c1_rail/c1_sizing_host_reference.py` and MYM tick handling
in `ops/c1_rail/c1_rail_slippage.py`. Production constants and strategies are unchanged.
Using the existing host arithmetic, normal risk is 1.25 dollars: floor(1.25/0.5)
is 2, capped to 1. At the 40% DD multiplier, risk is 0.5 dollars: floor(0.5/0.5)
is 1, capped to 1. Current equity selects DD behavior; it does not replace the
starting-balance risk basis. This does not promise quantity 1 under a lower multiplier.

Smallest means the smallest valid native stop first, then the smallest binary64
base risk that satisfies both required regimes. The immediately preceding float,
`math.nextafter(0.0000125, 0.0)`, produces DD risk
`0.49999999999999994`, hence zero contracts. Sub-tick stops are rejected.
The shared contract digest freezes the strategy inputs. Preflight also checks the
actual tier, account-wide cap, complete reservations, lifecycle and DD state.

## Enforcement and one-shot path

The listener samples dry-run once and rejects this identity unless it is explicitly
Boolean `true`, before sizing or payload construction. Non-entry requests halt at
the same boundary. The sizing host independently rejects non-entry requests and
malformed or drifting test constants. A stale request after future arming cannot
invoke the sender. Defaults are retired with cap zero; activation is explicit.

The daemon uses its existing `Strategy.on_bar` interface, normal B1 serializer and
listener client. The dormant Live adapter subscribes to `GLBX.MDP3`, `ohlcv-1m`,
one elected MYM native raw symbol. The reviewed manifest binds the native symbol,
instrument ID, publisher ID, target minute, expiration, expected quantity and
preflight digest. SDK mapping input/output names and record header IDs must match.
The elected native contract is separate from the listener's continuous route.
No fixture or manual POST qualifies as item-5 evidence.

A valid finalized target bar is evaluated once. The journal durably reserves the
send before HTTP and disables the ceremony. A crash or uncertain response never
retries that reservation. HTTP redirects are terminal responses and cannot create
another request. Duplicate bars, stale boot generations and spent ceremony
IDs cannot re-enable it. Operator close preserves late receipts without reopening
the ceremony. File locks and durable replacements protect state transitions.
Any prior unresolved evaluation/send checkpoint or uncertain transport also blocks
preparing a fresh ceremony ID, including after close or restart. This offline
packet supplies no reset or reconciliation bypass: preserve the journal and stop
until a separate operator-reviewed reconciliation procedure is available.
State, initialized marker and tombstones must survive rollback; deleting state is
not recovery. An established feed disconnect uses bounded reconnect backoff.

## Separate future attended phases

1. **A — offline review (this change):** review code and tests, Docker COPY closure,
   constants proof and this packet. Synthetic tests are software validation only.
2. **B — listener deployment:** obtain separate authorization and satisfy all six
   canonical deployment preconditions: verified flat/disarmed state; canonical
   repo-root deploy context from integrated reviewed source; complete import/COPY
   closure; fresh in-container fixture hashes; boot/health/disarm verification;
   and authenticated private crash-loop recovery instructions with rollback ready.
   The historical private recovery gap is not waived or reconstructed here.
3. **C — volume migration:** while flat and explicitly disarmed with no deadline,
   review a migration plan against private current state. Old 69/11 reservations
   require explicit `--release-withdrawn` under the accepted release; otherwise
   activation refuses over-allocation. Account-wide reservations must stay within
   the owner's cap. Apply requires reviewed preimage hashes and flat verification.
   It backs up state, writes cap zero, then lifecycle, then cap one. Interruption
   leaves zero capacity. DD and secrets are not migrated.
4. **D — daemon deployment:** separately authorize its own app/volume deployment;
   verify the pinned SDK on Linux Python 3.12, native import, copied CLI imports,
   then boot inert. Review actual source mapping and entitlement privately. A new
   boot starts disabled even if old config requested emit. Listener stays dry-run.
5. **E — ceremony:** perform a fresh private listener preflight, require quantity 1,
   and record its time and digest. Freeze a future target and source in the manifest;
   prepare leaves READY disabled. After reviewing current boot and source, explicitly
   enable that exact manifest. Observe one genuine target-bar request, close even
   after timeout, and check effective emit false. Never retry an uncertain attempt.

These phases require fresh evidence; no earlier health, flatness or equity claim is
carried forward from this offline session. A changed state or quantity requires a
new preflight and review. Preflight uses the existing read-only equity adapter and
host sizing method, never HTTP POST, ledger append, or DD ratchet.

## Operator interfaces (reference only; not executed live)

Listener commands, from the image's `/app`:

```text
python ops/c1_rail/m1_stage1_control.py migrate --config /data/c1_rail_config.json --enable-test
python ops/c1_rail/m1_stage1_control.py preflight --config /data/c1_rail_config.json
python ops/c1_rail/m1_stage1_control.py evidence --events /data/c1_rail_events.jsonl --daemon-state PRIVATE_COPIED_CLOSED_STATE --ceremony-id REVIEWED_ID
```

Migration defaults to plan-only. Any later apply additionally needs `--apply`,
`--flat-verified`, `--expect-constants` and `--expect-lifecycle` with the reviewed
hashes, and the same release flag if approved. Running migrate without
`--enable-test` plans retirement/cap zero. Do not restore withdrawn reservations
from backups during rollback.

Daemon CLI uses `PYTHONPATH=/app/ops` and
`python -m c1_signal_daemon.m1_stage1_control {status,prepare,enable,close}`.
Use `--config /data/c1_signal_daemon_config.json`,
`--state /data/c1_m1_stage1_state.json`, current `--boot-id`, reviewed
`--manifest PRIVATE_MANIFEST.json`, and `--ceremony-id` as the action requires.
The manifest fields are `ceremony_id`, `target`, `expires`, `source`,
`contract_sha256`, `expected_qty`, `preflight_sha256`; source fields are
`dataset`, `schema`, `raw_symbol`, `instrument_id`, `publisher_id`.
Target is a UTC minute start; expiration must exceed target+60 seconds and be no
later than target+150 seconds. The current config example remains null/disabled.

## Evidence, rollback and unresolved readiness

Evidence projection joins the actual closed daemon journal to exactly one genuine
listener `request_received` / `decision` / `transport_result` triad by request hash,
deterministic order identity and UUID. It verifies expected=observed=1, dry-run,
no sender, bound target/bar/source and disabled terminal state. Public output
allowlists IDs/hashes and verdicts; raw bar/account/response data stays private.
It does not write acceptance, claim broker `CHAIN_OK`, or supply operator signoff.
Capture daemon effective-emit status alongside it; a journal is not a substitute
for the final running-process observation.

Rollback: close/disable first, verify inert state, retire test lifecycle and cap
through the reviewed migration, then use the authenticated deployment rollback.
Keep backups and spent journal records. Listener must remain explicitly dry-run
with no armed deadline. Never arm to validate rollback.

The local SDK's native wheel targets CPython 3.11; the available complete test
runtime is CPython 3.12. Docker is unavailable. Consequently native SDK import,
Linux image build and real feed mapping are **not verified** here. Packaging is
checked offline through COPY/import closure and isolated CLI smoke only. Before
deployment, resolve this compatibility check plus private crash recovery, then
refresh deployed hashes from actual running containers. Existing M1 fixture hashes
remain historical and are not replaced by local tree hashes.

## Offline verification result

Python 3.12: **366 passed** across `tests/ops/test_c1_rail*.py`,
`test_c1_signal_daemon*.py`, `test_m1*.py`, `test_c1_sizing_host_reference.py`,
`tests/test_validate_c1_monitoring_acceptance.py` and `tests/rail_crosstrade`.
The integration fixtures exercise SDK-shaped callbacks through the normal hook,
client and actual HTTP handler into sizing and the structured ledger. They are
synthetic and are never acceptance evidence. Dedicated regressions cover the
minimum tuple, strict mode snapshot, malformed state, mapping, reconnect ordering,
close during POST, uncertain transport, duplicate/restart suppression and evidence
tampering. Independent listener, daemon and final coherence reviews completed;
identified issues were fixed and re-reviewed.

Offline COPY-subset smoke passed listener server, arm CLI and M1 control `--help`,
plus daemon and daemon M1 control `--help`, using isolated copied files.
`python scripts/check_boundaries.py` and `git diff --check` passed.
`python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --check-tree-skew`
passed structural validation as `CODE_LANDED` and honestly reported all six
historical pins differ. Only explanatory acceptance notes changed; status, IDs,
signoff and fixture hashes were verified equal to baseline.

Phase A initially left the work uncommitted in the isolated worktree. This task did not edit the
original checkout; final status showed concurrent instrument-ledger work there
on another branch, which was left alone. No live service, feed, deployment, signal, broker, arming, PR or
push was used during Phase A; the excluded compliance file was not inspected.

## PR preparation scope

**Offline M1 Stage 1 test infrastructure only — no deployment, no signal emission, no arm.**

The subsequent user instruction authorizes diff/secrets review, clean-state test
rerun, commit, push, PR creation, independent safety review and check monitoring.
It adds no operational authority. The inherited non-M1 commits are excluded from
the PR. No `core/`, accepted-book, production-protection, venue-edition, allocation,
or unrelated strategy file is changed; the MYM instrument ledger receives only the
test-identity appendix. Credential-pattern and manual review found only explicit
offline placeholders in added test literals, no credentials or private live data.

The independent PR review found a standard-library automatic-redirect gap in the
literal one-HTTP-attempt guarantee. A no-redirect opener fixes it; offline regression
reproduced three failures before the fix and passed all five redirect codes after.
The reviewer rechecked the fix and approved live-mode prohibition and one-shot
behavior. This is code-review evidence, not M1 item-5 acceptance or deployment GO.

Clean-state PR rerun: **371 passed** on Python 3.12 after removing prior pytest
fixtures and bytecode caches, with bytecode writing and pytest caching disabled.
This is the original 366-test selection plus five redirect regressions.

GitHub review follow-up: offline regressions reproduced 15 failures covering stale
SDK error callbacks, newline-terminated wire receipts, disabled polling logs and
fresh-ID bypass of unresolved sends. Repairs scope error callbacks to the SDK
session, preserve exact body hashes while recognizing the real response terminator,
keep disabled polling quiet, and block preparation across unresolved journal history.
The integration test now uses the HTTP handler's real response writer.

Follow-up verification: **387 passed** on Python 3.12. The callback lock-inversion
regression failed before moving all SDK calls outside the callback mutex, then
passed with the combined suite. No deployment, feed or signal was used.
