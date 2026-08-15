# ADR 2026-08-08 — S2b signal-daemon build (deferred limbs)

**Status:** `Accepted` — fills deferred limbs of [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md); **does not authorize build alone** — requires a separate operator build GO citing this ADR + Accepted S2b
**Decision date:** 2026-08-08
**Authors:** Joshua (plan execution GO) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) · [S2 ADR](2026-08-07-loop-s2-signal-host-fork.md) · [Databento research ADR](2026-07-10-databento-research-stack.md) · [M1 ADR](2026-07-22-c1-venue-native-monitoring-maturity.md) · [rail GO ADR](2026-07-17-c1-rail-build-account-registration-go.md)
**Layer:** infrastructure / signal-host. Fills S2b deferred decisions. Code/image/deploy wait on operator build GO.

---

## §0 — Rule 0 reads (verified 2026-08-08)

| Source | Anchor | What it pins |
|---|---|---|
| [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) | Accepted 2026-08-08 | Minimal daemon limbs; bar source / thresholds / exits policy deferred here |
| `ops/c1_rail/c1_rail_http_server.py` | `2345095` | `POST /c1/<path_token>` + JSON parse; **origin-agnostic** — cheap falsifier PASS (no sender-identity gate) |
| `ops/c1_rail/c1_sizing_host_reference.py` | `2345095` | B1 required fields: `leg_id`, `signal_type`, `bar_time`, `close`, `stop_dist_pts` |
| `deploy/c1_rail/fly.toml` | working tree | Listener single-machine / volume; S2b scoping note — daemon must be a **second** app |
| Tree probe | 2026-08-08 | `ops/c1_signal_daemon/` and `deploy/c1_signal_daemon/` **absent** before build GO |
| [Databento research ADR](2026-07-10-databento-research-stack.md) | Accepted | Research stack; “live rail KEEP” = sizing/CrossTrade/listener unchanged — **not** a ban on Databento as daemon evaluate feed |

---

## §1 — Context

S2 ruled the live signal origin Python-native. S2b Accepted the minimal daemon shape but deferred live bar source, reconnect/staleness, heartbeat paging thresholds, and exits/flats-on-feed-loss policy to a build ADR. Without those locks, an implementation would invent safety thresholds ad hoc. The listener B1 contract is already origin-agnostic; the daemon is an HTTP client of that listener, not a CrossTrade peer.

**Decision driver:** Unlock a buildable daemon design without collapsing DD-locality or re-opening Striker redeploy.

---

## §2 — Decision

**Deferred S2b limbs are locked as follows** (amend only by superseding ADR):

| Limb | Lock |
|---|---|
| Live CME bar source | **Databento GLBX.MDP3 Live**, schema `ohlcv-1m` (parent/micro as the strategy requires). Express reading of the Databento research ADR: “live rail KEEP” means the sizing/CrossTrade/**listener** path stays unchanged; the daemon image **may** depend on `databento`. Listener image stays stdlib-only. |
| Reconnect | Auto-reconnect with backoff; feed **unhealthy** while disconnected. |
| Staleness | Unhealthy if `now - last_bar_ts` exceeds **`2 × bar_period + 30s`** (e.g. 15m strategy bar → 30m + 30s). Formula is canonical; do not hard-code a one-off magic age. |
| Heartbeat | Operator-visible on the **daemon** app: process up + `last_bar_age_s` via `GET /` JSON (separate from listener health). Log/page when heartbeat missed for the same staleness window. |
| Fail-closed | On unhealthy/stale/missing feed: **emit no signals of any type** (`entry` / `add` / `exit` / `flat`). |
| Second Fly app | App name `c1-signal-daemon`; tree `deploy/c1_signal_daemon/` + `ops/c1_signal_daemon/`; own volume for daemon state only — **never** listener `peak_equity`. |
| Listener | Unchanged B1 contract; daemon holds listener base URL + path token as secrets. Fresh `bar_time` every fire. |
| Strategy surface | Pluggable evaluate hook. **No Striker / MYM / MNQ redeploy.** First emit waits a new strategy + any required `LEG_MAP` extension (separate GO). Until then: feed + heartbeat with **`emit_enabled=false`**. |
| M1 item 5 | This ADR does **not** claim M1 `RESOLVED`. Discharge still needs a real strategy-signal B1 → expected non-zero dry-run sizing + `operator_signoff`. |

**Effective:** immediately upon Accept (2026-08-08).
**Spend:** $0 / K=0 until a separate operator **build GO** citing this ADR + Accepted S2b. That GO licenses code + image + warm deploy with emit disabled; it does **not** license arming, Striker redeploy, or M1 fabrication.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Absorb S2b into this ADR without prior Accept | Path-1 unlock keeps Accept → build ADR → GO as separate gates |
| Collapse daemon into `c1-rail` Fly app | Violates DD-locality / S2b step 5 |
| TV/export panels as “live” feed | Explicitly barred by S2b step 1 |
| Fail-open exits on feed loss | Tempting for orphan-position rescue; fail-closed default wins until a superseding ADR |
| Build under this ADR alone | Boundary: separate operator build GO required |

---

## §4 — Falsifier (revert trigger)

**H:** After Accept, any daemon build that lands under an operator GO citing this ADR implements the table in §2 (Databento Live `ohlcv-1m`, formula staleness, fail-closed-all, second Fly app, emit-disabled default) and does not alter the listener B1 contract.

**Revert / FALSIFIED (any limb):**
1. Daemon shares the listener volume / `peak_equity` → tear back; restore two-app boundary.
2. Daemon emits entry/add/exit/flat while feed unhealthy → tear back emit path; reinstate fail-closed.
3. Listener B1 fields changed without a superseding ADR → unauthorized contract change.
4. Code/image/deploy lands **without** a dated operator build GO citing this ADR + Accepted S2b → unauthorized build; tear back.
5. Striker / withdrawn MYM/MNQ legs redeployed under this ADR → forbidden; tear back.

**Trigger check schedule:** first daemon deploy / emit enable, or 2026-08-08 programme audit.

---

## §5 — Forbidden moves

- Building/deploying under this ADR **without** a separate operator build GO.
- Collapsing daemon into the listener app or sharing `peak_equity`.
- Changing B1 listener contract without a superseding ADR.
- Arming the rail / setting `dry_run=false` / claiming M1 `RESOLVED`.
- TV login/actuation automation.
- Redeploying withdrawn Striker legs.
- Silently loosening §4 triggers or §2 staleness/fail-closed locks.

---

## §6 — Consequences

**Positive:** Buildable daemon design with explicit feed, fail-closed, and second-app locks; unblocks operator build GO → warm infrastructure.

**Negative / costs:** Databento Live dependency + cost gate on the daemon image; second always-on Fly machine; emit remains disabled until a strategy GO.

**Risks:** Live feed outages suppress all signals including exits (accepted under fail-closed); mitigate with heartbeat visibility + attended ops.

**Downstream (after build GO):** `ops/c1_signal_daemon/`, `deploy/c1_signal_daemon/`, tests, RUNBOOK daemon section, c1-rail skill pointer refresh, `.dockerignore` allow-list for the daemon COPY set.

---

## §7 — Audit hooks

```bash
# Spec Accepted:
rg -n "^Status: Accepted" docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md
# No collapse into listener deploy dir:
test ! -f deploy/c1_rail/../c1_signal_daemon/fly.toml -o -f deploy/c1_signal_daemon/fly.toml
# After build: second app present, listener still separate
test -f deploy/c1_signal_daemon/fly.toml && rg -n 'app = "c1-signal-daemon"' deploy/c1_signal_daemon/fly.toml
# Listener B1 fields unchanged:
rg -n '_REQUIRED_PAYLOAD_FIELDS' ops/c1_rail/c1_sizing_host_reference.py
```
