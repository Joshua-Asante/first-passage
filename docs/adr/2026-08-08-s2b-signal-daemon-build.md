# ADR 2026-08-08 — S2b signal-daemon build (deferred limbs)

**Current feed disposition (2026-09-11): no live source selected.** Databento is retired and unsubscribed per the operator; the Databento selection in §2 was revised out in place on 2026-09-11 with its prior wording preserved (Rule 14 class 2; Addendum 2026-09-11 §Prior revision). For Stage 1 ceremonies only, the ruled input is an **operator-attended controlled input** — [Addendum 2026-09-11](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d), option D, **RATIFIED 2026-09-11**. No live feed is approved; live-feed readiness remains owed.

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

**Deferred S2b limbs are locked as follows** (amend only by superseding ADR or an operator-approved dated revision under the [ADR policy](2026-08-08-adr-ceremony-tiering.md) revision clause; the "Live CME bar source" row was revised in place 2026-09-11 — see [Addendum 2026-09-11](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d)):

| Limb | Lock |
|---|---|
| Live CME bar source | **Revised in place 2026-09-11** (operator ruling, Track A / A1r; prior wording verbatim under [Addendum 2026-09-11 §Prior revision](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d)). **No live source selected.** For Stage 1 ceremonies only, an **operator-attended controlled input**: the operator transcribes the just-closed 1m bar of the dated front-month MYM contract named in the ceremony manifest (`venue_contract`) from the Tradovate platform chart into the daemon container within the ceremony window; the strategy hook, B1 build, reservation and POST are the daemon's. `MYM1!` is the identity's listener route label, not a venue symbol. This is not a feed, not a fixture and not a replay; it certifies the chain, not feed readiness. S2b step 1's live-feed selection remains owed. Listener and daemon images stay stdlib-only under the Stage 1 disposition. **Production feed (operator ruling 2026-09-11, Track B open item O-4):** the **Tradovate market-data API on a personal live Tradovate account used for data only** (`live.tradovateapi.com`, `md/subscribeChart` or polled `md/getChart`, `MinuteBar`/1) — the addendum's option A′ — is the selected live CME bar source for the four production adapters; never the Tradeify eval sub-account. Credentials rest only on the daemon volume; the daemon image may then depend on a hash-pinned websocket client (listener image stays stdlib-only). Implementation is owed (Track A feed packet, A9) and no live feed is connected today; the Stage 1 ceremony input stays option D. |
| Reconnect | Auto-reconnect with backoff; feed **unhealthy** while disconnected. *Scope note 2026-09-11 (Addendum 2026-09-11):* applies to a live transport. The controlled Stage 1 input has no transport — `connected` is false outside a ceremony and true only while an injected bar is available (until `deactivate()`); there is nothing to reconnect and no reconnect is attempted or logged. |
| Staleness | Unhealthy if `now - last_bar_ts` exceeds **`2 × bar_period + 30s`** (e.g. 15m strategy bar → 30m + 30s). Formula is canonical; do not hard-code a one-off magic age. |
| Heartbeat | Operator-visible on the **daemon** app: process up + `last_bar_age_s` via `GET /` JSON (separate from listener health). Log/page when heartbeat missed for the same staleness window. *Scope note 2026-09-11 (Addendum 2026-09-11):* missed-bar paging applies to a live transport. Under the controlled input the health JSON keeps reporting `connected`, `feed_healthy`, `feed_mode`, `ceremony_state` and `poll_interval_s` (operator-visible), but an inert daemon with no ceremony is the expected state and raises no missed-feed alert — the existing unavailable-source behaviour, which logs nothing per poll (`test_unavailable_runtime_does_not_log_each_poll`), carries over. |
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

**H:** After Accept, any daemon build that lands under an operator GO citing this ADR implements the table in §2 (the source disposition in force — from 2026-09-11 the operator-attended controlled input for Stage 1 with no live source, revised in place per [Addendum 2026-09-11](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d); prior wording named Databento Live `ohlcv-1m` — formula staleness, fail-closed-all, second Fly app, emit-disabled default) and does not alter the listener B1 contract.

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

**Positive:** Buildable daemon design with fail-closed and second-app locks and, from 2026-09-11, a ruled Stage 1 input (operator-attended controlled input; the original explicit-feed wording is under Addendum 2026-09-11 §Prior revision — live-feed readiness remains outstanding); unblocked the operator build GO → warm infrastructure.

**Negative / costs:** no live-source dependency or data cost under the 2026-09-11 disposition (prior wording: Databento Live dependency + cost gate on the daemon image — revised in place 2026-09-11, [Addendum 2026-09-11 §Prior revision](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d)); a production feed and its cost remain owed; second always-on Fly machine; emit remains disabled until a strategy GO.

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

---

## Addendum 2026-08-24 — test-strategy emit GO for M1 item 5

**Does not amend** §2 feed / fail-closed / second-app locks. **Does not** claim M1 `RESOLVED`. **Does not** arm. **$0 / K=0.**

**Operator 2026-08-24:** the §2 “First emit waits a new strategy + any required `LEG_MAP` extension (separate GO)” gate is **GO’d for a test strategy only**, dated 2026-08-24, to discharge M1 item 5. `NullStrategy` stays the warm default until that attended emit. Withdrawn Striker / MYM / MNQ redeploy stays forbidden. `emit_enabled=true` remains the attended step the daemon already refuses without this GO.

Owner: [M1 addendum](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24).

## Addendum 2026-09-10 - selected source retired; no replacement

The operator retired Databento as a First Passage information source and reported unsubscribing. The Databento GLBX.MDP3 Live selection in section 2 is no longer authorized. The [source-owner retirement record](2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento) preserves the original decision and records its current disposition.

No replacement provider, subscription or connection is approved. Keep the daemon inert and M1 emission blocked. The existing live-feed requirement is not silently replaced with a local fixture or replay; that would need an explicit amendment identifying what the test certifies and leaving live-feed readiness separate. Source retirement does not waive expected nonzero dry-run sizing, genuine hook/transport evidence, operator signoff or the prohibition on arming. No deployment or operational action is authorized by this documentation change.

## Addendum 2026-09-11 — Stage 1 input source: options and RATIFIED selection (option D)

**Status:** RATIFIED 2026-09-11 — option D (operator-attended controlled input). Operator rulings: "i choose option d"; Q1–Q5 "adopt all, dated 2026-09-11". Recorded on disk by the parent session as Track A / A1r (this edit). The packet's recommendation was D, so the Selection block stands unrewritten.
**Track:** [Track A plan](../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) sub-track A1 · brief [A1](../briefs/handoffs/2026-09-10-track-a-a1-claude-signal-source-decision-packet.md) · the parent session records the ruling as A1r.
**Amends in place** (operational Rule 14 class 2 — accepted-ADR effective text after an approved revision; [ADR policy](2026-08-08-adr-ceremony-tiering.md) revision clause) the §2 "Live CME bar source" row, the §2 amendment clause, the §4 hypothesis parenthetical and the §6 cost line, each carrying a dated scope note; the prior wording is preserved verbatim under §Prior revision below and in git history. §4 revert limbs (1)–(5) are byte-unchanged. The header disposition line is the reader-intercept. **Does not** claim M1 `RESOLVED`. **Does not** arm, sign up, spend, connect, or implement. **$0 / K=0.**

### §0 — Rule 0 reads (this addendum; anchors are `git log -1 --format=%h -- <path>` on `origin/main` @ `051f8e5`)

| Source | Anchor | Passage that binds this packet |
|---|---|---|
| this ADR §2 row "Live CME bar source" | `2cb980d` | "Databento GLBX.MDP3 Live, schema `ohlcv-1m`" — locked "amend only by superseding ADR"; §2 "Listener image stays stdlib-only" |
| this ADR Addendum 2026-08-24 | `2cb980d` | first-emit gate "GO'd for a test strategy only, dated 2026-08-24" |
| this ADR Addendum 2026-09-10 | `2cb980d` | "No replacement provider, subscription or connection is approved"; a fixture or replay "would need an explicit amendment identifying what the test certifies and leaving live-feed readiness separate" |
| [S2 ADR](2026-08-07-loop-s2-signal-host-fork.md) §2 | `770413b` | "Pine/TradingView remains the research/export surface. TV login/actuation automation stays absolutely prohibited"; item 5 = "a Python-daemon B1 POST that produces a structured dry-run decision with expected (non-zero) sizing" |
| S2 ADR §4 limb 2 | `770413b` | DEAD-list: "canned payloads, live-armed evidence, or zero-qty floors" |
| [SPEC S2b](../spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md) step 1 + Boundary | `027a729` | "research panels / TV exports are not the live feed"; Boundary "no TV login/actuation automation" |
| [M1 ADR](2026-07-22-c1-venue-native-monitoring-maturity.md) §4 item 5 + AMBIGUOUS | `502a8fb` | "a structured `dry_run` event from a real strategy signal with expected sizing"; "AMBIGUOUS — stay disarmed: real strategy JSON does not arrive" |
| M1 ADR Addendum 2026-07-31, "What item 5 uniquely certifies" | `502a8fb` | every defect that bit the rail "was a real-signal-only discovery", including the 07-28 finding that `parsed.close` was not the bar's close; item 5 "is the only gate positioned to catch it before money is live" |
| M1 ADR Addendum 2026-08-24, "Qualifying instrument" | `502a8fb` | "evaluate-hook strategy, not a canned hand-POST (item 6 class), not `NullStrategy`, not a fabricated event id, not a withdrawn Striker redeploy" |
| [Databento ADR](2026-07-10-databento-research-stack.md) Addendum 2026-09-10 | `2cb980d` | "Any proposal to qualify controlled replay instead of the currently specified live feed requires an explicit acceptance amendment" |
| [Stage 1 contract](../notes/rail_build/M1_STAGE1_TEST_CONTRACT.md) | `811df7c` | "It does not intrinsically require Databento"; "An explicit amendment could define a controlled replay wiring test while keeping live-feed readiness separate"; the marker `{kind: offline_fixture, schema: ohlcv-1m, symbol: MYM1!}` "is not a provider selection or live-data claim" |
| `ops/c1_signal_daemon/feed.py` | `811df7c` | `BarSource` = `poll() -> Bar \| None` + `connected`; `Bar(ts, open, high, low, close, volume)`; staleness `2 × bar_period + 30 s` |
| `ops/c1_signal_daemon/evaluate_loop.py` | `811df7c` | `_step`: `coordinator.before_poll(source, now)` → `source.poll()` → `coordinator.accept_bar(bar, getattr(source, "binding", None), now)` → `feed_healthy` → `strategy.on_bar` → `reserve` → `post_b1` |
| `ops/c1_signal_daemon/m1_stage1.py` | `3cdeabe` | `before_poll` calls `source.activate(manifest["source"])` / `source.deactivate()`; `accept_bar` requires `binding == manifest["source"]`, `bar.ts == target`, `60 ≤ now − bar.ts ≤ 150`, finite positive numerics, `low ≤ min(o,c) ≤ max(o,c) ≤ high` |
| `ops/c1_signal_daemon/daemon.py` | `811df7c` | `IdleBarSource` (`feed_mode="unavailable"`, `poll()` → `None`); `build_loop` constructs `NullStrategy` with **no coordinator**; `load_config` accepts `strategy ∈ {"null","m1_stage1_test"}` and the `m1_test` ceremony keys |
| `ops/c1_signal_daemon/m1_stage1_control.py` | `811df7c` | `validate_manifest` requires `source == OFFLINE_SOURCE`; `main` returns 2 for `prepare`/`enable` before any state read ("ceremony blocked: no approved source; Databento retired"); no `sys.path` bootstrap (plan §3.1) |
| `ops/c1_rail/m1_stage1_contract.py` | `811df7c` | `OFFLINE_SOURCE`; `contract_sha256()` inputs = version, leg, symbol, tier, stop, row, `entry_only`, `permanently_dry_run_only` — the source marker is **not** an input |
| `ops/c1_rail/m1_stage1_control.py::project_evidence` | `811df7c` | requires `manifest["source"] == contract.OFFLINE_SOURCE`; checks `parsed.close == bar["close"]`; returns `offline_test_only: True`, `qualifying_live_source: False`, `listener_event_id`; never `dry_run_strategy_signal_event_id` |
| `scripts/validate_c1_monitoring_acceptance.py` | working tree | `RESOLVED_REQUIRED` includes `dry_run_strategy_signal_event_id` and `operator_signoff` (`.operator` required) |
| [Subscription ledger](../pursuits/SUBSCRIPTION_LEDGER.md) | `51609a4` | retired Databento run-rate **$200/mo** (change log 2026-09-10: "$720 to $520"); active total $420/mo; TradingView $70/mo (Premium per [d11](../pursuits/d11-tradingview-subscription.md)); CrossTrade $50/mo |
| [W6 ADR](2026-08-07-w6-rail-infra-closures.md) §2 item 1 | `770413b` | "CrossTrade→Tradovate relink procedure subsection (2-connection-cap fact)" — the cap itself lives in the private RUNBOOK |
| [Surface-allocation ADR](2026-07-14-cc-cursor-surface-allocation.md) §2 | `cd84198` | routing test 1 (doctrine → Claude), 2 (frozen spec → Cursor/Codex), 3 (overhead threshold) |
| `ops/prop_envelope_default.md` §4 Tradeify row | `1396b00` | "FTA §6.6: sole-owner bots OK; no HFT; **Tradovate API LIVE-funded only**" (re-verified 2026-07-22) |
| [GO ADR](2026-07-17-c1-rail-build-account-registration-go.md) §3 | `770413b` | "Tradovate API is LIVE-funded-only per envelope §4 (unavailable on eval)" |

Cheap falsifier run 2026-09-11: `grep -n "Tradovate API LIVE-funded only" ops/prop_envelope_default.md` hits (line 42); `contract_sha256()` inputs confirmed by reading the function body. Both hold.

### §0.5 — Readings put to the operator (confirm or reject with the ruling; the packet rests on neither silently)

1. **Delayed-but-genuine bars.** The identity's sizing is price-independent (fixed 1.0-pt stop; `close` only has to be finite and > 1.0), so the input's job is the **origin**, not price fidelity. Reading: a delayed market bar would satisfy the "real strategy signal" limb *if the daemon could accept it* — but it cannot without code: `accept_bar` rejects `now − bar.ts > 150 s` and `feed_healthy` marks the feed unhealthy past 150 s, so any feed delayed by more than ~85 s fails closed before the hook runs. Delayed sources therefore need a window/staleness amendment to §2 (an S2b lock), not just this packet. Options are scored on that basis; no delayed source is recommended.
2. **Operator-attended input (option D) — replay or distinct class?** Reading: it is a **distinct class** from "fixture or replay": the bar is a genuine, just-closed market bar transcribed by the operator at ceremony time, the payload is built by the daemon's strategy hook, and nothing is replayed from a store. It is nonetheless *not* a live feed, and the 2026-09-10 addenda require an explicit amendment either way; the amendment text under option D says exactly what the event certifies. Classification is the operator's call.

### Eligibility finding on the operator's conditional ruling (2026-09-11, PR #335 comment 5629047842: option A, conditional on eval-account API eligibility)

**Option A on the `Tradeify_Select_100K` eval account is NOT eligible on the record available to this session; the conditional ruling returns BLOCKED to the operator.**

- Repo record (Rule 0): the ratified envelope's Tradeify row, re-verified against Tradeify's help center on 2026-07-22, reads "Tradovate API LIVE-funded only" (FTA §6.6), and the GO ADR §3 already ruled out "TV → Tradovate native" on that ground: "unavailable on eval".
- Public record (accessed 2026-09-11): Tradovate's API is a paid add-on (**$25/mo**) that requires a **live** Tradovate account with **≥ $1,000** equity ([community.tradovate.com/t/how-do-i-access-the-api/2380](https://community.tradovate.com/t/how-do-i-access-the-api/2380), […/t/could-i-user-api-access-the-simulation-env-by-a-simulation-account/4033](https://community.tradovate.com/t/could-i-user-api-access-the-simulation-env-by-a-simulation-account/4033), […/t/does-this-api-work-anymore-how-much-does-it-cost/7458](https://community.tradovate.com/t/does-this-api-work-anymore-how-much-does-it-cost/7458)); prop-firm evaluation and funded sub-accounts are reported excluded regardless of balance ([…/t/api-access-for-propfirm-accounts/10348](https://community.tradovate.com/t/api-access-for-propfirm-accounts/10348), […/t/how-can-i-use-tradovate-apis-for-prop-firm-eval-and-paid-accounts/7814](https://community.tradovate.com/t/how-can-i-use-tradovate-apis-for-prop-firm-eval-and-paid-accounts/7814), [blog.pickmytrade.trade/tradovate-api-access-without-1000-minimum-2026-options/](https://blog.pickmytrade.trade/tradovate-api-access-without-1000-minimum-2026-options/)). Tradeify's own FAQ (mirror at [pickmytrade.trade/en/prop-firm-faq/tradeify-faq/](https://pickmytrade.trade/en/prop-firm-faq/tradeify-faq/)) names webhook bridges as the sanctioned automation path and does not offer direct API access.
- **Not established from a primary page:** Tradovate's and NinjaTrader's own API-access articles (`api.tradovate.com`, `support.tradovate.com`, `vendor-support.ninjatrader.com/s/article/Tradovate-API-Access`) and Tradeify's help center returned no readable text (JS-rendered / HTTP 403) to this session. The exclusion rests on the repo's 2026-07-22 verification plus convergent secondary sources. If the operator can open the Tradeify FTA §6.6 text or the NinjaTrader article and it says otherwise, the finding flips; nothing else in this packet changes.
- Whether the exclusion is imposed by Tradovate (platform) or by Tradeify (firm policy on its sub-accounts) is not established; either way the eval account cannot subscribe.

A separate **personal live Tradovate account used for market data only** is eligible on the public record and is scored below as **A′**. It is a signup plus a $1,000 deposit, which this session may not perform.

### Options — scoring summary (details and sources per option follow)

| # | Option | Item-5 limbs | Doctrine amendment beyond this ADR's §2 feed row | Certifies / leaves open | Cost (sourced) | Build | Operational / terms risk | Reversibility | Grade |
|---|---|---|---|---|---|---|---|---|---|
| A | Tradovate market-data API on the **eval** account | would satisfy | none | — | — | — | — | — | **INELIGIBLE** (finding above) |
| A′ | Tradovate market-data API on a **personal live** Tradovate account (data only) | satisfies all | none | chain + production-class live feed / leaves nothing | $25/mo API + ~$4–12/mo CME non-pro L1; **$1,000 deposit parked**; KYC | WS client + auth renewal; 3–5 files; lock file | **live brokerage login at rest** on the daemon volume; token renewal; session cap on that account only | close account, withdraw deposit | viable — the production-feed route, not needed for M1 |
| B | Licensed third-party CME 1m feed (real-time) | satisfies all | none | chain + production-class feed / vendor SLA | cheapest plain-API real-time: **$199/mo** (Massive Advanced) = the retired run-rate; broker-sponsored APIs $55–125/mo need a brokerage account | WS client; lock file | data-only key at rest; vendor outage → fail-closed | cancel | viable, not recommended |
| B-delayed | Massive Starter, 10-min delayed | fails `accept_bar` window and staleness without amending §2 locks | window + staleness amendment | — | $29/mo | as B | — | cancel | not viable as specified |
| C | TradingView alert webhook as **bar transport** (strategy stays in Python) | satisfies all technically | S2/S2b clarification (TV as transport ≠ origin); M1 note; **and a ruling on TradingView Terms of Use §3** | chain on a genuine live bar / production feed still owed | $0 incremental on Premium if real-time CME is active, else **$7/mo** CME add-on | ingest handler + source; 5–7 files; no new dependency | new public POST path on the daemon app; **TV Terms of Use license alerts/webhooks for "exclusive display-only use" and forbid machine-driven non-display use** | delete the alert; remove the ingest key | technically viable — **not recommended** (terms conflict) |
| D | Operator-attended controlled input (bar read from the Tradovate chart, injected in-container) | satisfies all as read in §0.5 (2) | the explicit amendment the 2026-09-10 addenda name | chain on a genuine market bar, input → decision identity / **live-feed readiness untouched** | **$0** | CLI + one-shot source; 4–6 files; no dependency, no ingress, no secret | human transcription in the data path; 60 s window for the operator (target + 60 to + 120) | nothing persists | **viable — recommended · RATIFIED 2026-09-11** |
| E | Databento re-subscription | — | — | — | $199/mo Standard | — | — | — | **NOT AUTHORIZED** (Track A) |
| F | Free / unlicensed sources (Yahoo `YM=F`, `yfinance`, Stooq, Google Finance) | — | — | — | $0 | — | terms bar automated access; CAPTCHA-gated; delayed | — | **EXCLUDED** |

### Option A′ — Tradovate market-data API, personal live account (data only)

- **Item-5 limbs:** bars from a live CME feed → `M1Stage1TestStrategy.on_bar` → daemon B1 POST → listener `qty_out=1` at `dry_run=true`. Not canned; ruled host; expected sizing. Satisfies §2 "Live CME bar source" as a source selection.
- **Doctrine:** this ADR §2 row only (text below). No M1/S2/S2b amendment.
- **Certifies / leaves open:** the full chain on a production-class feed, including feed → daemon → listener price identity (the 07-28 class); live-feed readiness for MYM would be **discharged** (reconnect/staleness per §2 already implemented against `BarSource`). Leaves open: nothing M1 needs. The account stays separate from the eval sub-account.
- **Cost (accessed 2026-09-11):** API add-on $25/mo; CME non-professional Level-1 ~$12/mo for the four-exchange bundle or ~$4/mo single exchange ([pickmytrade.trade/how-to/tradovate-professional-data-rates/](https://pickmytrade.trade/how-to/tradovate-professional-data-rates/), community 7458 — vendor pages warn figures drift); **$1,000 minimum live balance** to subscribe (one-time gate per community posts). ≈ $30–37/mo plus parked capital, versus the retired $200/mo.
- **Build:** `ops/c1_signal_daemon/tradovate_md_source.py` (REST `auth/accessTokenRequest` → `mdAccessToken`; WebSocket `md/subscribeChart` or polled `md/getChart` with `underlyingType: MinuteBar`, `elementSize: 1`, `elementSizeUnit: UnderlyingUnits`; renewal via `auth/renewAccessToken` ~15 min before the ~80–90 min expiry — TTL conflicts across sources ([partner.tradovate.com auth overview](https://partner.tradovate.com/overview/quick-setup/auth-overview), community 3586/5276); resolve on the partner docs at build time); config keys `tradovate.{env, username, password, app_id, app_version, cid, sec, device_id, symbol}`; a hash-pinned `deploy/c1_signal_daemon/requirements.txt` for a websocket client (stdlib has none); Dockerfile COPY + `.dockerignore` re-include; marker `TRADOVATE_MD_SOURCE = {"kind": "tradovate_md_ws", "schema": "ohlcv-1m", "symbol": "MYM1!"}` in `m1_stage1_contract.py`; tests: auth/renewal/reconnect/staleness against a fake WS. Time-to-first-event: account opening + KYC + deposit (days, operator) then 2–3 build days.
- **Operational risk:** the daemon volume would hold a **live brokerage login** (username/password/cid/sec) — order-capable credentials, not a data key — the worst secret-at-rest profile of any option; Tradovate's session cap (community: 2 concurrent, third evicts oldest; one thread reports a single market-data connection and that a Trader UI login ends the API session — [community 2118](https://community.tradovate.com/t/understanding-concurrent-connection-limits/2118), [community 4482](https://community.tradovate.com/t/how-many-socket-session-can-keep-in-one-account/4482)) applies to the personal account only; the CrossTrade link on the Tradeify sub-account is untouched. Fail-closed on loss: yes (`feed_healthy`).
- **Reversibility:** close the account, withdraw the deposit, drop the module and lock.

### Option B — licensed third-party CME 1-minute feed

- **Item-5 limbs / doctrine / certifies:** as A′ (source selection only).
- **Cost (accessed 2026-09-11):** Massive (ex-Polygon) Advanced **$199/mo** real-time futures, REST + WebSocket, official Python client, no brokerage account ([massive.com/futures](https://massive.com/futures)); Massive Starter $29/mo is 10-min delayed (see B-delayed). DTN IQFeed ~$35 base + $24.87/mo CME non-pro surcharge but a proprietary local-socket client (not a plain WS a Fly container can run cleanly). Rithmic ~$125/mo + broker sponsorship ([ampfutures.com/rithmic-pricing](https://ampfutures.com/rithmic-pricing)); CQG API from $45/mo + $9 CME + $1 ([cqg.com market-data fees](https://www.cqg.com/partners/exchanges/market-data-fees)), broker-sponsored; IBKR $10/mo (waived with commissions) and TradeStation/Schwab $0 all require a **funded brokerage account** plus a heavyweight gateway. Barchart OnDemand, dxFeed retail, Sierra Denali: **pricing not public**. Kinetick is NinjaTrader-bound. Alpaca/Twelve Data/Tiingo/Marketstack carry no CME futures.
- **Build:** as A′ with a vendor WS client; data-only API key at rest. Time-to-first-event: signup same day + 1–2 build days.
- **Operational risk:** low (data-only key); vendor outage → fail-closed. **Reversibility:** cancel.
- **Why not recommended:** the only plain-API real-time vendor costs what Databento cost; the operator retired that run-rate on 2026-09-10. A production feed decision belongs with a production strategy, not with a one-ceremony M1 discharge.
- **B-delayed (Massive Starter $29/mo):** a 10-min delay fails `accept_bar` (`now − bar.ts ≤ 150`) and `feed_healthy` (150 s) — every bar arrives unhealthy. Qualifying it would amend two §2 locks (window, staleness) and change the ceremony contract's `expires − target ≤ 150`. Not viable as specified; listed so the cheapest number is visibly priced and rejected.

### Option C — TradingView alert webhook as bar transport

- **Mechanism:** one standing alert, created **manually once** on a `MYM1!` 1-minute chart, frequency **Once Per Bar Close**, webhook URL = the daemon app's authenticated ingest path, message body = `{"secret":"…","symbol":"{{ticker}}","exchange":"{{exchange}}","interval":"{{interval}}","time":"{{time}}","open":{{open}},"high":{{high}},"low":{{low}},"close":{{close}},"volume":{{volume}}}`. TradingView POSTs the message as the body at bar close; `{{time}}` is the bar's timestamp in UTC (`yyyy-MM-ddTHH:mm:ssZ`), `{{timenow}}` the firing time ([placeholders](https://www.tradingview.com/support/solutions/43000531021-how-to-use-a-variable-value-in-alert/), [frequencies](https://www.tradingview.com/support/solutions/43000474415-differences-between-alert-frequencies/), [webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/), all accessed 2026-09-11). The daemon stores the most recent bar; `poll()` returns it once; `binding` = the marker. Strategy logic, B1 build, reservation, POST, listener decision are unchanged and all in Python.
- **Item-5 limbs:** real strategy signal from the ruled host (the hook runs in the daemon on a genuine live bar); not canned (the payload is daemon-built, `bar_time` = ceremony event id, `close` = the live bar's close); expected non-zero sizing at `dry_run=true`; no silent redefinition (this addendum would be the express amendment).
- **Doctrine conflicts and resolution (repo):** (i) S2 §2 "Pine/TradingView remains the research/export surface" and S2b step 1 "research panels / TV exports are not the live feed" — an alert webhook is neither an export nor a panel, but the lock's intent (TV is not the signal origin) must be restated: TV here is a **bar transport**, the signal origin stays the daemon. (ii) S2's rationale for leaving TV — the alert-snapshot / port-parity class — is not re-imported: no Pine strategy runs, no alert carries a *decision*, the bar values are the closed bar's OHLCV, and the daemon rejects anything outside the ceremony window. (iii) "TV login/actuation automation absolutely prohibited" — untouched: no login, no UI actuation; the alert is created by hand and left standing. (iv) M1 item 5: satisfied as written.
- **Terms conflict (external, load-bearing):** TradingView's Terms of Use §3 ("Ownership of information; license to use TradingView; redistribution of data; non-display usage", [tradingview.com/policies/](https://www.tradingview.com/policies/), accessed 2026-09-11, text read on the rendered page) license content and market data — naming charts, alerts and webhooks — for "exclusive display-only use", enumerate automated trading, automated order generation, algorithmic decision-making and any machine-driven process without direct human-readable display as prohibited non-display uses, and state that TradingView expressly forbids both direct non-display use and tools built to enable it. A daemon consuming alert webhooks to drive a signal decision is a machine-driven non-display use as written, however common the pattern is among bridging services. The same standard that excludes option F applies: **a safety-relevant acceptance artifact must not rest on a feed whose terms forbid the use.** Only the operator can rule the clause inapplicable; the packet does not.
- **What the event would certify / leave open:** the chain on a genuine live bar delivered by an automated transport; a production feed still owed (no SLA, no reconnect semantics; alerts on Essential/Plus expire after 2 months, Premium/Ultimate allow open-ended alerts that deactivate after a year untouched).
- **Cost (accessed 2026-09-11):** webhooks are included on every paid plan from Essential ($14.95/mo monthly) up ([tradingview.com/pricing/](https://www.tradingview.com/pricing/)); the operator's plan is Premium ($70/mo, already paid, 400 technical alerts, open-ended alert duration). Real-time CME data on TradingView is a non-professional add-on at **$7.00/mo**; delayed CME data is free with a 10-minute delay ([tradingview.com/cme/](https://www.tradingview.com/cme/)) — a delayed bar closes outside the daemon's 60–150 s window, so C requires the add-on if it is not already active.
- **Build (daemon only, if ever ratified):** `ops/c1_signal_daemon/tv_webhook_source.py` (`BarSource` + `activate/deactivate/binding/feed_mode="tv_alert_webhook"`; accepts a bar only while activated, only for `symbol == "MYM1!"` and `interval == "1"`, parses `time` as the bar timestamp UTC, rejects duplicates by `ts`); `http_status.py` gains `POST /ingest/<ingest_token>` (constant-time secret compare on the body field, `Content-Length` cap 4 KiB, must answer within TradingView's 3 s limit on port 443, 204 on accept, 404 otherwise, never echoes the body); `daemon.build_loop` constructs the source **disconnected** plus `M1Coordinator`; `load_config` validates `tv_webhook.{ingest_token (≥ 32 chars), secret, symbol}`; `m1_stage1_control.validate_manifest` accepts `source == TV_WEBHOOK_SOURCE`, and `prepare`/`enable` drop the hard `2` while keeping every boot/generation/manifest check; `sys.path` bootstrap added (plan §3.1); marker `TV_WEBHOOK_SOURCE = {"kind": "tv_alert_webhook", "schema": "ohlcv-1m", "symbol": "MYM1!"}` in `m1_stage1_contract.py` (`contract_sha256()` unchanged); `project_evidence` accepts that marker and returns `qualifying_live_source: True`, `offline_test_only: False`, `production_feed: False`, `source_kind: "tv_alert_webhook"`; no new dependency; Dockerfile COPY + `.dockerignore`; tests for ingest auth/size/duplicate/out-of-window, activation gating, the real-HTTP-handler integration path, retirement test updated; A2 D2/D6 expectations updated in the same PR; README documents the volume keys as a pending write for A4-D/A6. TradingView requires 2FA on the account for webhook alerts. Time-to-first-event: ~1 build day + A2-D/A4-D/A6 + one attended ceremony.
- **Operational risk:** a second public path on the daemon app (today GET `/` only) — mitigated by token-in-path + body secret + accept-only-while-activated (outside a ceremony the handler returns 404 and stores nothing); secrets at rest = one shared alert secret. Fail-closed on loss: bars stop → `feed_healthy` false → no signal of any type (§2 lock preserved).
- **Reversibility:** delete the TradingView alert; remove the `tv_webhook` config block; module can stay dormant.

### Option D — operator-attended controlled input

- **Mechanism:** the ceremony manifest names `source = OPERATOR_INPUT_SOURCE`. At target + 60…120 s the operator reads the just-closed 1-minute bar of the **dated front-month MYM contract named in the ceremony manifest** (`venue_contract`, chosen by the operator at `prepare` time from the venue's front-month designation) from the **Tradovate platform chart** of the eval account (real-time, human display; Tradeify states it covers the CME non-professional data fee — [Tradeify FAQ mirror](https://pickmytrade.trade/en/prop-firm-faq/tradeify-faq/), accessed 2026-09-11) and creates a private local JSON file outside the recorded console, transfers it by SFTP to the distinct upload path `/data/m1_upload_<ceremony_id>.json`, then runs `inject --bar-file /data/m1_upload_<ceremony_id>.json` inside the daemon container. The published one-shot path is separately fixed as `/data/m1_bar_<ceremony_id>.json`; deleting the upload can therefore never delete the bar awaiting the daemon. The CLI validates against the READY manifest and current boot (including `--contract == manifest.venue_contract`) **and requires both the journal's `enabled` and the config's `m1_test.enabled` / `emit_enabled` to be true** — after `prepare` but before `enable` the state is `READY` yet inactive, and the daemon would `deactivate()` and delete a freshly published file, consuming the sole permitted injection (Codex P2, 2026-09-11); the pre-enable case is a refusal test. Bar values arrive only through `--bar-file <private upload path on the volume>` rather than command-line arguments, so no raw value enters a transcript; the CLI prints a value-free receipt and removes the upload file in a `finally` path on success or refusal. `close`, teardown, and daemon startup also remove any ceremony-bound orphan upload, covering an abort before `inject`. Under a stable per-ceremony exclusive claim created with `O_CREAT|O_EXCL` and retained through ceremony close, `inject` performs enablement/identity/time/OHLC validation and publication as one serialized operation; concurrent or later injectors fail on the claim, so exactly one process can publish. It then writes the distinct one-shot bar file bound to the ceremony id **atomically** (temp file in the same directory, flush + fsync, `os.replace` — the daemon's existing `atomic_json` in `m1_stage1_state.py`), so the polling daemon can never observe partial JSON and discard the only permitted bar; `OperatorInputSource.poll()` returns it exactly once; the rest of the chain is unchanged. **Injection deadline (Codex P2, 2026-09-11):** the daemon consumes the one-shot file only on its next `EvaluateLoop.step()` (`run_daemon` sleeps `poll_interval_s` between steps; the example config sets 5 s) and `accept_bar` rejects the bar once `now − bar.ts > 150`, so an injection completed near target + 150 s could be consumed after the cutoff with no second injection possible. `inject` therefore refuses, before any write, once `now − target > 120` (30 s of headroom over the acceptance cutoff), refuses before target + 60 (the bar has not closed), and `prepare` requires the ceremony config's `0 < poll_interval_s ≤ 1` so consumption latency is bounded by one second (`load_config` imposes no lower bound today, and `time.sleep(0)` would spin while `time.sleep(-1)` raises — `prepare` fails closed on either before touching ceremony state). A refused injection writes nothing and the ceremony simply expires at its manifest `expires`; the operator prepares a fresh ceremony for a later target. **Contract identification (Codex P1, 2026-09-11):** `MYM1!` is TradingView continuous-contract notation carried as the identity's listener route label (`INSTRUMENT_SYMBOLS`, provisional per `docs/spec/c1_nt8_sizing_host_impl.md` §Risks); Tradovate charts show dated contracts. The manifest therefore names the exact contract the operator reads, the bar record and `bar_sha256` carry it, and `project_evidence` reports it, so the record cannot label a bar as something it is not — including across a quarterly roll. Sizing is price-independent, so the contract month cannot change the decision; this binds provenance honesty, not discharge validity. Tradovate's platform data is used by a human at a screen, which is display use; nothing machine-reads it.
- **Item-5 limbs:** the strategy hook runs in the ruled host on a genuine market bar; the B1 payload is daemon-built, not canned; expected non-zero sizing at `dry_run=true`; the express amendment below prevents silent redefinition. **Operator call (§0.5 (2)):** whether an operator-transcribed bar is a "controlled input" distinct from "fixture or replay". It is not replayed from any store and did not exist before the ceremony; it is also not machine-sourced.
- **Doctrine:** this is "the explicit amendment identifying what the test certifies and leaving live-feed readiness separate" that Addendum 2026-09-10 and the Databento retirement addendum name. S2/S2b untouched (no TradingView involvement at all).
- **Certifies / leaves open:** certifies hook → B1 → listener → dry-run decision at `qty_out=1` on a real market bar, in production containers, with the ceremony journal, reservation and evidence join end to end — including **input → decision price identity** (`parsed.close == bar.close`, the 07-28 class from the operator's input onward). Leaves open **everything about a live feed**: no source connects, so feed → daemon identity and feed health are not exercised; S2b step 1 remains fully owed.
- **Cost:** $0. **Build:** `ops/c1_signal_daemon/operator_input_source.py`; `inject` action in `m1_stage1_control.py` (+ `sys.path` bootstrap); `daemon.build_loop` wires the source (disconnected until a bar is injected) + coordinator; **connectivity contract:** `EvaluateLoop._step()` calls `source.poll()` and only afterwards evaluates `feed_healthy(connected=source.connected, …)`, so `OperatorInputSource` must report `connected == True` from the moment a valid injected bar is available and keep reporting it after `poll()` has handed the bar out, until `deactivate()` (ceremony close/expiry) — an implementation that derives `connected` from the one-shot file's continued existence would consume the file and suppress the valid bar as `feed_unhealthy` before the strategy runs; the integration test covers the sequence inject → `poll()` → `connected` still true → hook fires → `deactivate()` → disconnected, a concurrent-publication case (poll racing a slow writer sees either nothing or the complete bar, never a partial file), a concurrent-inject case (exactly one process obtains the claim and publishes), an upload-vs-published-path case (upload deletion leaves the one-shot intact), refusal/close/startup cleanup cases for the private upload, and an orphan case (inject, then restart or expiry before `poll()` → the file is gone and the next ceremony starts clean); marker `OPERATOR_INPUT_SOURCE = {"kind": "operator_attended_input", "schema": "ohlcv-1m", "symbol": "MYM1!"}` (fixed; `accept_bar` binding equality unchanged); `validate_manifest` accepts it and requires a top-level manifest field `venue_contract` matching `^MYM[HMUZ]\d$` — YM/MYM lists quarterly contracts only, third-Friday expiry in Mar/Jun/Sep/Dec (`ops/instruments/YM.md` W1), so a non-quarterly code such as `MYMN6` is refused, not merely required to match — and whose third-Friday expiry falls on or after the ceremony `target` date and within the next two quarterly expiries (front or next; the year digit resolved against the target year), so a dead or far-dated contract is refused; which of the two the venue designates as front is the operator's reading, recorded verbatim (covered by `manifest_sha256`, not by `contract_sha256()`); `inject --contract` must equal it; `inject` enforces `60 ≤ now − target ≤ 120` before any write; `prepare` validates `0 < poll_interval_s ≤ 1`; **deployment gate for the interval (Codex P1, 2026-09-11):** `run_daemon` reads `poll_interval_s` once at startup, the deployed daemon volume carries the example value 5, and option D introduces no new config keys — so A1b sets the example config to `"poll_interval_s": 1`, adds `poll_interval_s` to the heartbeat JSON (`GET /`) so the running value is verifiable, and A4-D records the interval as a **pending write** that A6 stages on the daemon volume before the deploy (operator `sftp` put of the locally prepared config, as for any volume change); A6 then verifies `GET /` reports `poll_interval_s: 1` and A7 refuses to start on any other value; the bar record carries `venue_contract` inside the `bar_sha256` fingerprint; `project_evidence` returns `qualifying_live_source: False`, `offline_test_only: False`, `operator_attended_input: True`; no dependency, no ingress, no secret; tests for inject validation (wrong boot/ceremony/time, malformed OHLC, second and concurrent inject refused), one-shot semantics, integration path; retirement test updated; A2 D6 expectation updated. Time-to-first-event: ~1 build day + A2-D/A4-D/A6 + one attended ceremony.
- **Operational risk:** the operator has ~60 s (target + 60 to target + 120) to transcribe five numbers and run one command over `fly ssh console` (open the console before target; the command is pre-typed); a transcription error is caught by the OHLC consistency check or simply yields a different `close` — sizing is unaffected. No ingress, no secrets. Fail-closed: nothing else can produce a bar.
- **Reversibility:** nothing persists beyond the ceremony journal — the private upload is removed on every `inject` exit and by close/teardown/startup, while the one-shot bar file is removed by `deactivate()` (ceremony close or expiry) and by daemon startup for any ceremony that is not READY under the current boot, so a crash or expiry between `inject` and `poll()` cannot leave raw bar data on the volume or hand it to a later ceremony (the file is bound to its ceremony id and refused by any other); the integration test covers the crash-before-poll case; the CLI action can be removed.

### Option E — Databento re-subscription: NOT AUTHORIZED

Recorded as considered: Standard **$199/mo** (intro $179 first 12 months) ([databento.com/blog/introducing-new-cme-pricing-plans](https://databento.com/blog/introducing-new-cme-pricing-plans), accessed 2026-09-11) — the run-rate the operator retired on 2026-09-10. Track A forbids restoring credentials or re-subscribing ("Do not simply restore Databento credentials or substitute a fixture"). Out.

### Option F — free / unlicensed sources: EXCLUDED

Yahoo Finance shows `YM=F` / `MYM=F` as delayed quotes; Yahoo's Terms of Service §2(a) prohibit bots, scrapers and data-mining tools without express prior permission ([legal.yahoo.com/us/en/yahoo/terms/otos/index.html](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html)), the developer API terms are personal display-only ([legal.yahoo.com/…/apiforydn](https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn)), and `yfinance` scrapes undocumented endpoints and disclaims affiliation ([github.com/ranaroussi/yfinance](https://github.com/ranaroussi/yfinance)). Stooq gates its CSV endpoint behind a CAPTCHA-issued key with a daily quota; its terms page could not be retrieved (unverified, not assumed permissive). Google Finance has no API. Investing.com's terms restrict storing or redistributing market information (secondary-sourced). All are delayed, which also fails the acceptance window (§0.5 (1)). No free, terms-clean, CME-licensed 1-minute futures API was found (accessed 2026-09-11). Out.

### Amendment text — option A′ (APPLIED 2026-09-11 as the production feed — operator ruling on Track B open item O-4)

Appended to this ADR's §2 row "Live CME bar source" as the production-feed disposition (the Stage 1 ceremony input stays option D; the row's Stage 1 text is unchanged). The ruling: the operator chose A′ after the A1 packet's pricing (≈ $25/mo API add-on + CME/COMEX non-professional data, a $1,000 minimum live balance parked, brokerage login at rest on the daemon volume as the named risk) and after CrossTrade was verified to relay no Tradovate market data. Original amendment text as scored:

```
| Live CME bar source | **Tradovate market-data API** (`live.tradovateapi.com`, `md/subscribeChart` or `md/getChart`, `MinuteBar`/1) on a **personal live Tradovate account used for data only** — never the Tradeify eval sub-account (FTA §6.6; eval accounts are API-ineligible). Credentials rest only on the daemon volume; the listener image stays stdlib-only; the daemon image may depend on a hash-pinned websocket client. Selected 2026-09-11 as the production feed (Addendum 2026-09-11, O-4 ruling 2026-09-11). |
```

No M1 ADR amendment: item 5 is discharged under option D; when the A′ feed is live, `project_evidence` may report `qualifying_live_source: True` only for a ceremony whose bar came from that feed.

### Amendment text — option B

```
| Live CME bar source | **<vendor> <plan>** real-time CME 1-minute OHLCV over WebSocket/REST; data-only API key rests on the daemon volume; the listener image stays stdlib-only; the daemon image may depend on the vendor's hash-pinned client. Selected 2026-09-DD (Addendum 2026-09-11, ratified 2026-09-DD). |
```

No M1 ADR amendment.

### Amendment text — option C (only if the operator rules TradingView Terms of Use §3 inapplicable; the ruling is recorded in the row)

This ADR §2 row:

```
| Live CME bar source | **Stage 1 ceremonies only:** a TradingView **alert webhook as bar transport** — one manually created, standing "Once Per Bar Close" alert on `MYM1!` 1m posting OHLCV+time JSON to the daemon's authenticated ingest path; the signal origin remains the daemon (strategy hook, B1 build, reservation, POST). No TV login/actuation automation; no Pine strategy; no decision travels in the alert. Operator ruling 2026-09-DD on TradingView Terms of Use §3 (display-only / non-display): <ruling and grounds>. **Not a production feed:** S2b step 1's live-feed selection for any deployable strategy remains owed and unselected. Selected 2026-09-DD (Addendum 2026-09-11, ratified 2026-09-DD). |
```

Append to the M1 ADR (`docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`), after Addendum 2026-08-24:

```
## Addendum 2026-09-DD — item-5 input transport for Stage 1: TradingView alert webhook (express)

**Does not amend** item 5's limbs. **Does not** claim `RESOLVED`. **Does not** arm. **$0 / K=0.**

The Stage 1 ceremony's bar reaches the ruled host through a TradingView alert webhook acting as
**bar transport** (S2b build ADR Addendum 2026-09-11, option C, ratified 2026-09-DD). The signal
origin is the daemon: `Strategy.on_bar` → B1 → listener → structured dry-run decision at expected
non-zero sizing. TradingView is not the signal origin (S2 §2 stands) and no login/actuation
automation is involved.

**What the item-5 event certifies:** the ruled host produced a real strategy signal on a genuine
live market bar with expected sizing at `dry_run=true`, through the deployed daemon and listener.
**What it does not certify:** a production live feed. Live-feed readiness for any deployable
strategy remains separate and owed (S2b step 1). The evidence projection records
`qualifying_live_source: true`, `production_feed: false`, `source_kind: "tv_alert_webhook"`;
`dry_run_strategy_signal_event_id` is written only by the operator-signed A8 edit from a
projection's `listener_event_id`.
```

M1 ADR change-history row: `| 2026-09-DD | Addendum — item-5 Stage 1 input transport = TV alert webhook (express); limbs, decline, no-arm stand | Joshua (ruling) · Claude (recorder) |`.

### Amendment text — option D (APPLIED 2026-09-11)

This ADR §2 row — applied in place 2026-09-11 (identical to the live row; prior wording under §Prior revision):

```
| Live CME bar source | **Revised in place 2026-09-11** (operator ruling, Track A / A1r; prior wording verbatim under [Addendum 2026-09-11 §Prior revision](#addendum-2026-09-11--stage-1-input-source-options-and-ratified-selection-option-d)). **No live source selected.** For Stage 1 ceremonies only, an **operator-attended controlled input**: the operator transcribes the just-closed 1m bar of the dated front-month MYM contract named in the ceremony manifest (`venue_contract`) from the Tradovate platform chart into the daemon container within the ceremony window; the strategy hook, B1 build, reservation and POST are the daemon's. `MYM1!` is the identity's listener route label, not a venue symbol. This is not a feed, not a fixture and not a replay; it certifies the chain, not feed readiness. S2b step 1's live-feed selection remains owed. Listener and daemon images stay stdlib-only under the Stage 1 disposition. **Production feed (operator ruling 2026-09-11, Track B open item O-4):** the **Tradovate market-data API on a personal live Tradovate account used for data only** (`live.tradovateapi.com`, `md/subscribeChart` or polled `md/getChart`, `MinuteBar`/1) — the addendum's option A′ — is the selected live CME bar source for the four production adapters; never the Tradeify eval sub-account. Credentials rest only on the daemon volume; the daemon image may then depend on a hash-pinned websocket client (listener image stays stdlib-only). Implementation is owed (Track A feed packet, A9) and no live feed is connected today; the Stage 1 ceremony input stays option D. |
```

Append to the M1 ADR after Addendum 2026-08-24:

```
## Addendum 2026-09-11 — item-5 input for Stage 1: operator-attended controlled input (express)

**Does not amend** item 5's limbs. **Does not** claim `RESOLVED`. **Does not** arm. **$0 / K=0.**

The Stage 1 ceremony's bar is a genuine, just-closed 1-minute bar of the dated front-month MYM contract named
in the ceremony manifest (`venue_contract`), transcribed by the operator from the Tradovate platform chart and
injected in-container within the ceremony window (`MYM1!` is the identity's listener route label, not a venue
symbol; S2b build ADR
Addendum 2026-09-11, option D, ratified 2026-09-11). This is the explicit amendment the 2026-09-10
addenda require: it is a **controlled input**, not a fixture or a replay — nothing is replayed from a
store and the bar did not exist before the ceremony. The signal origin is the daemon (`Strategy.on_bar`
→ B1 → listener); the payload is not canned.

**What the item-5 event certifies:** the ruled host produced a real strategy signal on a real market bar
with expected sizing at `dry_run=true`, through the deployed daemon and listener, including the
ceremony journal, reservation, evidence join and input → decision price identity in production
containers.
**What it does not certify:** any live feed. Live-feed readiness, feed → daemon price identity and feed
health remain entirely separate and owed (S2b step 1). The evidence projection records
`qualifying_live_source: false`, `operator_attended_input: true`; `dry_run_strategy_signal_event_id`
is written only by the operator-signed A8 edit from a projection's `listener_event_id`.
```

M1 ADR change-history row: `| 2026-09-11 | Addendum — item-5 Stage 1 input = operator-attended controlled input (express); limbs, decline, no-arm stand | Joshua (ruling) · Claude (recorder) |`. **Applied 2026-09-11:** the addendum above (with a Rule 0 line and the Q1–Q5 scope note) and this row were appended to the M1 ADR by the same A1r edit.

### Selection

**RATIFIED 2026-09-11 — option D.** The operator adopted the packet's recommendation as written; the grounds below stand as the dated record.

**Recommended: option D — operator-attended controlled input, bar read from the Tradovate platform chart.** Grounds: (1) every item-5 limb is met with the daemon as the signal origin on a real market bar, and the event exercises the whole production chain including the input → decision price identity that item 5 exists to catch; (2) $0, no signup, no capital parked, no credentials at rest, no new public ingress; (3) the doctrine change is the exact amendment the 2026-09-10 addenda already anticipate, and it says plainly that live-feed readiness stays owed; (4) it uses the venue's own real-time data the eval account already carries, by human display, with no terms conflict; (5) nothing persists to reverse. Its cost is honesty about scope: it certifies the chain, not a feed.

**Not recommended:** C would be the stronger technical claim at $0, but TradingView's Terms of Use §3 forbid the machine-driven non-display use it requires; the packet applies the same bar it applies to free sources. **A′** is the production-feed route (Tradovate data, machine feed, feed → decision identity certified) at ~$30–37/mo plus $1,000 parked and a live login at rest; it belongs with a production-strategy ruling, not with M1, and it is available as an alternative if the operator wants a machine feed now. **B** repeats the retired run-rate for no M1 gain.

Sequence of rulings: the operator's first, conditional ruling for option A returned **BLOCKED — eval account ineligible** and the packet selected no fallback; the operator then ruled **option D** on 2026-09-11 (§Operator rulings below). No further ruling is owed.

### Falsifiable hypothesis (brief §4) — outcome

**H:** at least one option satisfies every item-5 limb and every S2/S2b bar without a doctrine amendment, at or below the retired $200/mo run-rate, with a build confined to `ops/c1_signal_daemon/`, `deploy/c1_signal_daemon/`, `ops/c1_rail/m1_stage1_contract.py` (marker only) and `tests/ops/`.
**Outcome: H is FALSIFIED — no option satisfies it.** Every option, A′ and B included, needs `ops/c1_rail/m1_stage1_control.py::project_evidence` to accept the ratified marker: it hard-codes `manifest["source"] == OFFLINE_SOURCE` and always projects `qualifying_live_source: False`, and that file sits outside H's stated build surface (the Track A plan §3.1 already lists it as an A1b surface). On doctrine alone A′ and B would have been feed-row-only ($30–37/mo plus $1,000 parked, or $199/mo) and both need an operator signup outside this session's authority. The brief's reject branch therefore applies as written: the recommendation is an amendment-class option (D) with its amendment text drafted. **AMBIGUOUS on option A:** eval-account eligibility could not be established from a primary page; the repo's own 2026-07-22 verification says ineligible.

### Return gate (this packet)

RESOLVED for A1 = every option scored on every criterion, recommendation stated, amendment text drafted, checkers green — **met**; Q1–Q5 ruled 2026-09-11 (below). FALSIFIED would be an option graded viable that violates a limb — C was re-graded from viable on the terms finding, which is this clause working as intended. AMBIGUOUS = option A eligibility (above).

### Operator rulings 2026-09-11 (Q1–Q5; operator: "adopt all, dated 2026-09-11")

- **Q1 — RULED: controlled input, not replay.** The bar did not exist before the ceremony, nothing is read back from a store, and the B1 payload is built by the daemon's strategy hook — the distinction the 2026-09-10 addenda draw. D is ratifiable; the option D amendment text states what the event certifies and what stays owed.
- **Q2 — RULED: left open, dated.** The option A exclusion rests on the repo's 2026-07-22 verification plus convergent secondary sources and is not primary-confirmed; re-verify only if A′ or any Tradovate feed is proposed. Nothing in Track A depends on it once D is chosen.
- **Q3 — RULED: TradingView Terms of Use §3 applicable; C stays out.** The historical TV-alert → listener path is already superseded by S2 and no strategy is deployed, so nothing operational changes; the touch on that history is this dated note, not a re-litigation.
- **Q4 — RULED: reading confirmed.** A delayed-but-genuine bar would satisfy the origin limb only under an amended window and staleness lock; any future delayed-feed proposal must carry both amendments, so the S2b locks cannot loosen by omission.
- **Q5 — RULED: later** (morning) **→ RULED 2026-09-11 (afternoon): A′ selected as the production feed** for the four adapters, after CrossTrade was verified to relay no Tradovate market data and Databento re-subscription was weighed and declined. The operator performs the signup, funding and data subscriptions; implementation is the Track A feed packet (A9); TB-I5 applies to this source. M1 itself still needs no machine feed (option D).

### Prior revision — immutable record of the 2026-09-11 in-place edits (all at `2cb980d`)

§2 amendment clause, prior: `**Deferred S2b limbs are locked as follows** (amend only by superseding ADR):`

§2 row "Live CME bar source", prior:

```
| Live CME bar source | **Databento GLBX.MDP3 Live**, schema `ohlcv-1m` (parent/micro as the strategy requires). Express reading of the Databento research ADR: “live rail KEEP” means the sizing/CrossTrade/**listener** path stays unchanged; the daemon image **may** depend on `databento`. Listener image stays stdlib-only. |
```

§4 hypothesis, prior (revert limbs (1)–(5) unchanged):

```
**H:** After Accept, any daemon build that lands under an operator GO citing this ADR implements the table in §2 (Databento Live `ohlcv-1m`, formula staleness, fail-closed-all, second Fly app, emit-disabled default) and does not alter the listener B1 contract.
```

§6 cost line, prior: `**Negative / costs:** Databento Live dependency + cost gate on the daemon image; second always-on Fly machine; emit remains disabled until a strategy GO.`

### §10 — Audit hooks (this addendum)

```bash
grep -n "^## Addendum 2026-09-11 — Stage 1 input source" docs/adr/2026-08-08-s2b-signal-daemon-build.md              # 1 hit (the fenced M1 template heading differs)
grep -c "^| Live CME bar source | \*\*Revised in place 2026-09-11" docs/adr/2026-08-08-s2b-signal-daemon-build.md   # 2 (live §2 row + its fenced copy)
grep -n "^\*\*Status:\*\* RATIFIED 2026-09-11" docs/adr/2026-08-08-s2b-signal-daemon-build.md                     # 1 hit (A1r landed 2026-09-11)
grep -n "^## Addendum 2026-09-11 — item-5 input for Stage 1" docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md   # 1 hit (M1 amendment applied)
grep -n "Tradovate API LIVE-funded only" ops/prop_envelope_default.md                                        # 1 hit (option A finding)
python scripts/check_adr_graph.py                                                                            # OK
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json     # unchanged, exit 0, CODE_LANDED
git diff --name-only origin/main...HEAD   # exactly: STATE.md; both ADRs; A4, A6, and A7 handoffs; M1_STAGE1_TEST_CONTRACT.md; and the Track A parent plan (8 files)
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-09-11 | **Production feed ruled — option A′** (personal live Tradovate data-only account) appended to the §2 row as the production-feed disposition; A′ amendment block marked APPLIED; Q5 updated. Stage 1 input stays option D. Recorded from the operator's chat ruling; implementation owed (Track A A9) | Joshua (ruling) · Claude (recorder) |
| 2026-09-11 | Codex round 12 folded (7 P2): non-recorded local creation + SFTP upload; upload cleanup on every exit; serialized one-shot injection claim; receipt-to-journal/projection hash join; A7 stale-interval remedy routed through A6 redeploy; complete eight-file diff audit; distinct upload and published paths | Codex (takeover) · Codex (review) |
| 2026-09-11 | Codex round 11 folded (1 P1 + 3 P2): A7 waits for a terminal journal state (≈ target + 165 s bound) instead of the manifest expiry; bar values pass through a private volume file, never the transcript; `inject` refuses until journal and config are both enabled; A6's stale-interval remedy is re-stage + redeploy within existing authority | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 10 folded (3 P2): A7 Step 2.1 gates the heartbeat's `poll_interval_s` before Step 2.2; one-shot bar cleanup on deactivate/startup with an orphan test case; STATE decision index gains the ratification entry | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 9 folded (2 P2): A6 Step 2.2b gates `poll_interval_s == 1` before the put and the post-deploy remedy is re-stage + machine restart + re-verify; the Stage 1 contract's readiness gate names what is still owed (A1b, validation, A3, A4–A6) instead of a source approval already granted | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 8 folded (2 P2): §2 Reconnect and Heartbeat rows carry dated scope notes (live-transport semantics; non-alerting controlled-input semantics); the Stage 1 test contract records the ratified disposition and separates the pre-A1b runtime from the approved post-A1b design | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 7 folded (2 P2): addendum heading renamed to its RATIFIED state (anchors updated in the M1 ADR, A7 brief and STATE.md); `inject` publishes the one-shot bar atomically (`atomic_json`), with a concurrent-publication integration case | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 6 folded (1 P1 + 2 P2): `poll_interval_s` deployment gate (example config → 1, heartbeat reports it, A4-D pending write, A6 stages and verifies, A7 refuses otherwise); §6 positive consequence no longer claims an explicit feed; parent plan reserves `inject` for the operator | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 5 folded (2 P2): A7 header reserves `inject` for the operator alongside `enable`; option D specifies the one-shot source's `connected` contract through the evaluation cycle (true after `poll()` until `deactivate()`) with an integration-test requirement | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 4 folded (3 P2): `0 < poll_interval_s ≤ 1`; A7 §7 review verifies the operator ran both `enable` and `inject`; §10 diff hook narrowed to the ADR pair | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 3 folded (2 P1 + 3 P2): `venue_contract` restricted to quarterly codes `H/M/U/Z` with an expiry-window check; summary row's operator window corrected to 60 s; brief-§4 outcome corrected to FALSIFIED (`project_evidence` is outside H's surface for every option); A7 handoff brief updated to option D (manifest `venue_contract`, operator `inject` step, deadline); STATE.md source blocker replaced by the ratified disposition | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex round 2 folded (3 P2): header intercept no longer claims a byte-unedited §2; §10 diff hook expects the two paired ADRs; option D gains an `inject` deadline (`60 ≤ now − target ≤ 120`, enforced before any write) and `poll_interval_s ≤ 1` during a ceremony, because the daemon consumes the one-shot file only on its next poll | Claude (fold) · Codex (review) |
| 2026-09-11 | Codex review of PR #340 folded (6 findings, all verified real): §2 row, §2 amendment clause, §4 hypothesis parenthetical and §6 cost line revised **in place** with prior wording preserved (Rule 14 class 2 / ADR policy revision clause — the earlier "byte-unedited" framing was the wrong Rule 14 class); option D gains the `venue_contract` provenance requirement; stale "fresh ruling owed" sentence replaced; M1 addendum Rule 0 pin distinguishes packet pin from ratification; addendum-count hook narrowed | Claude (fold) · Codex (review) |
| 2026-09-11 | **RATIFIED — option D** (operator: "i choose option d"; Q1–Q5 adopted as suggested, dated 2026-09-11). Status line, header disposition, Selection and the option D amendment applied here; option D addendum + change-history row appended to the M1 ADR (Track A / A1r) | Joshua (ruling) · Claude (recorder) |
| 2026-09-11 | Addendum — Stage 1 input-source decision packet (options A/A′/B/C/D/E/F scored; option A found ineligible on the eval account; C re-graded on TradingView Terms of Use §3; D recommended); status PROPOSED, ratification owed (Track A / A1r) | Claude (packet) · Joshua (ruling owed) |
