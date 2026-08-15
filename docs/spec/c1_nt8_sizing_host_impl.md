# SPEC — c1 sizing host: frozen implementation spec for the rail-side quantity computation

**Status:** `Proposed` — **Option C ADOPTED 2026-07-18** (operator decision, both §2.4 unknowns resolved favorably; supersede-in-part of the original NT8/NinjaScript execution path — the algorithm, leg map, state contract, and fail-safe in this document are UNCHANGED and now implemented directly in Python rather than ported to C#). The NT8 spine stays wired as a dormant fallback (nothing torn down). §2.2's algorithm is implemented and tested at [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py); the transport is implemented and tested at [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) + [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py); the TV-facing HTTP socket adapter is at [`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) (**§2.5(A)+(B) implemented 2026-07-18** — path-token gate + `equity_source` file/crosstrade dispatch; socket/real-network paths untested-by-design; §2.5 helpers unit-tested). Status note 2026-08-05: two of the four items formerly listed here are DISCHARGED — the always-on host stood up (deployed to Fly 2026-08-02 04:26 UTC, docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json; decision recorded RUNBOOK.md:55) and the B6 dry-fire PASSED 2026-07-20 (RUNBOOK.md §B6). The remaining two — live `equity_field` verify then flip `equity_source` to `crosstrade`, and instrument-symbol-format verification — each require a live Tradeify/CrossTrade/Tradovate target, which the 2026-08-04 de-scope removed in BOTH phases ([ADR](../adr/2026-08-04-tradeify-venue-descope-eval-included.md)). THIS SPEC CANNOT REACH `Accepted` AT THIS VENUE; its standing re-reads on operator fork F3 (2026-08-08). Status stays `Proposed` deliberately. **Deployment decided 2026-07-18: always-on host** (operator).
**Decision date:** 2026-07-17 (authored)
**Authors:** Joshua (direction) + Claude Code (authoring)
**Related:** [`c1_watch_realization_multiplier_layer.md`](c1_watch_realization_multiplier_layer.md) (`Accepted` — the sizing law this spec implements verbatim); [`2026-07-17-c1-rail-build-account-registration-go.md`](../adr/2026-07-17-c1-rail-build-account-registration-go.md) (B2 build step; B6 dry-fire gate consumes §7's test plan); [`lab/analysis/c1/q_rail_1_2026-07/f2_floors.json`](../../lab/analysis/c1/q_rail_1_2026-07/f2_floors.json) (worked-check oracle).
**Layer:** execution / infrastructure. No change to locked Pine parameters, allocations, or `dd_protection.py`/`firm_rules.py` constants — this host reads them, never edits them.

---

## §0 — Rule 0 reads (production-source verification, all 2026-07-17)

- [`core/lifecycle.py`](../../core/lifecycle.py) — anchor `4441c72` (2026-07-11). `TIER_MULTIPLIER = {"AUTHORIZED": 1.00, "WATCH-1": 0.50, "WATCH-2": 0.25, "RETIRED": 0.00}`; `STRATEGY_KEYS = frozenset({"Guardian", "Striker", "Aegis", "Striker NAS100"})`; `STATE_FILE = core/lifecycle_state.json`; **read-only-surface default when absent/unlisted = `"AUTHORIZED"` (1.0×)** — this spec explicitly diverges from that default for live order placement (§5), per the parent spec's own instruction that a live rail "must not fail-open to full size."
- [`core/dd_protection.py`](../../core/dd_protection.py) — anchor `a53ee99` (2026-07-13). `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40`; `BASE_RISK = {"Guardian": 0.0034, "Striker": 0.0070, "Aegis": 0.0150, "Striker NAS100": 0.0037}`; `calculate_protection`'s composition `scaled_risk = BASE_RISK × multiplier(DD) × lifecycle` is the exact law this host reproduces at the qty layer. `dd_protection_state.json` is the FXIFY/CFD-book peak-equity tracker — **scoped to the locked $200K book, not reusable for this new $100K futures eval account** (different account, different equity curve).
- [`core/firm_rules.py`](../../core/firm_rules.py) — anchor `a53ee99` (2026-07-13). `Tradeify_Select_100K`: `starting_balance=100_000`, `max_dd_pct=3.0` (trailing_locking, `dd_lock_offset_usd=100`), `micro_contract_cap=80`, `cost_per_side_usd=0.91`. `MFFU_Rapid_100K` fallback tier carries the same shape at `cost_per_side_usd=0.95`.
- [`docs/spec/c1_watch_realization_multiplier_layer.md`](c1_watch_realization_multiplier_layer.md) §2 — the normative sizing law and worked check this spec implements verbatim (not re-derived).
- [`lab/analysis/c1/q_rail_1_2026-07/f2_floors.json`](../../lab/analysis/c1/q_rail_1_2026-07/f2_floors.json) — MYM recent-90d: `sl_pts=60.8201`, `dollars_per_pt=0.5`, `risk_watch1_pct=0.35`, `base_capped=8`, `add_qty=60` (**re-pinned 2026-07-22** under the account-aggregate cap allocation `cap_alloc` MYM 69 / MNQ 11; the pre-split `(9, 67)` values are retained in the oracle under `pre_2026_07_22_whole_cap_per_leg`). This is §7's acceptance-test oracle.
- Venue Pine editions (gitignored; content-read this session, PORT_MANIFEST pins `42166af8…` DJ30/MYM, `139eb43d…` NAS100/MNQ) — locked `pyramidSize` inputs: DJ30 **750**, NAS100 **1000**; locked `mymPointValue`/`mnqPointValue`: **0.50** / **2.00**. B1's alert-payload contract (same session) is the upstream producer of this host's input JSON.

---

## §1 — Context

The parent spec ([`c1_watch_realization_multiplier_layer.md`](c1_watch_realization_multiplier_layer.md) §6) names rail-side equity/peak tracking as "new infrastructure with its own failure modes" and left the order-submission transport unresolved pending Q-RAIL-1 Phase 3's bridge-capability screen. That screen (PHASE3.md §2d) concluded row B — "NT8-side sizing host: NT8 script emits/overrides before or via ATI" — PASSes as the implementability route. This spec is that host's frozen design: every state source, the exact algorithm, the fail-safe, and the acceptance test Cursor's implementation must pass before the GO ADR's B6 dry-fire gate can close.

**Decision driver:** B6 cannot be scored without a frozen spec to implement against and test — "the sizing host works" is not verifiable without a named algorithm, named state sources, and a named oracle (this spec's §7 reproduces `f2_floors.json`'s exact recent-90d MYM numbers).

---

## §2 — Decision

**Decision:** An NT8 8.1+ NinjaScript component (`C1SizingHost`) computes order quantity for c1's two pyramided futures legs from the B1 alert payload plus three state sources (`core/lifecycle_state.json`, a new leg-scoped peak-equity tracker, and pinned firm/leg constants), per the algorithm in §2.2, with the fail-safe in §5. It does not manage exits, EOD flatten, or DD-limit closes — those remain the strategy's own `strategy.exit`/`strategy.close_all` orders and CrossTrade's Account Manager (E1); this host sizes **entry and add orders only**.

**Effective:** upon Cursor implementation + this spec's §7 test passing (B6 gate).
**Scope:** c1's two legs (`dj30_mym` → `Striker`, `nas100_mnq` → `Striker NAS100`) on one Tradeify Select 100K (or MFFU Rapid 100K fallback) account. Not a generic multi-firm sizing engine.

### §2.1 — leg_id mapping table (closes the ambiguity between the alert payload's `leg_id` and production's strategy keys)

| Pine `leg_id` | `lifecycle_state.json` key | `BASE_RISK` key | Locked `pyr_pct` | Locked `dollars_per_pt` |
|---|---|---|---|---|
| `dj30_mym` | `Striker` | `Striker` (0.0070) | 750 | 0.50 |
| `nas100_mnq` | `Striker NAS100` | `Striker NAS100` (0.0037) | 1000 | 2.00 |

An unrecognized `leg_id` is a hard input error — halt for that signal, per §5 (no silent fallback, matching the repo's standing no-silent-fallback philosophy already enforced in `core/lifecycle.py`'s own `_multipliers_from_state`).

### §2.2 — Algorithm (normative; transcribed from `c1_watch_realization_multiplier_layer.md` §2, DD/peak mechanism resolved here)

```
# Per incoming signal {leg_id, signal_type, bar_time, close, stop_dist_pts}:

leg_key, base_risk, pyr_pct, dollars_per_pt = LEG_MAP[leg_id]   # §2.1; halt if leg_id unknown

# 1. DD scale — this host's OWN peak-equity tracker (§2.3), NOT dd_protection_state.json
current_equity = account.NetLiquidation                         # NT8 Account object, live read
peak_equity    = max(peak_equity_state.peak_equity, current_equity)   # ratchet up, persist
dd_from_peak   = max(0.0, (peak_equity - current_equity) / peak_equity)
dd_scale       = DD_SCALE (0.40) if round(dd_from_peak, 6) >= DD_TRIGGER (0.015) else 1.0

# 2. Lifecycle multiplier — same file core/lifecycle.py reads, no second source of truth
lifecycle_tier = lifecycle_state.json[leg_key]                   # HALT if file/key/tier unreadable (§5)
lifecycle_m    = TIER_MULTIPLIER[lifecycle_tier]

# 3. Effective risk (identical composition to dd_protection.py:calculate_protection)
r_eff = base_risk * dd_scale * lifecycle_m

# 4. Quantity (only on signal_type == "entry" or "add")
if signal_type == "entry":
    risk_dollars = E_firm * r_eff
    per_contract = stop_dist_pts * dollars_per_pt
    qty_base_raw = floor(risk_dollars / per_contract) if per_contract > 0 else 0
    reserve_cap  = floor(cap_alloc / (1 + pyr_pct / 100))   # THIS LEG'S allocated share — HALT if absent (§5);
                                                            # NEVER fall back to cap_firm (see the block below)
    qty_out      = min(qty_base_raw, reserve_cap)
    if qty_out > 0:
        open_leg_state[leg_key].executed_base_qty = qty_out      # persisted for the add leg
    submit ENTRY order, qty=qty_out (skip submit if qty_out == 0; log FLOORED)

elif signal_type == "add":
    executed_base = open_leg_state[leg_key].executed_base_qty    # the ACTUAL filled base qty,
                                                                   # not a re-derived theoretical one —
                                                                   # keeps the base:add ratio internally
                                                                   # consistent even if DD/lifecycle
                                                                   # state changed between entry and add
    qty_out = floor(executed_base * (pyr_pct / 100))
    submit ADD order, qty=qty_out

elif signal_type in ("exit", "flat"):
    open_leg_state[leg_key] = cleared                             # bookkeeping only; no order —
    log AUDIT entry, qty_out=N/A                                  # exits/EOD/DD-close are the
                                                                   # strategy's own orders + CrossTrade AM
```

**Worked-check target (§7 acceptance test):** MYM recent-90d, WATCH-1, no DD — must reproduce **`qty_out=8`** (entry) then **`qty_out=60`** (add), matching `f2_floors.json` exactly (`legs[0].recent_90d`).

> ⚠ **Corrected 2026-08-05.** This target previously read `9` / `67` — the **pre-2026-07-22
> whole-cap-per-leg** pair, retained in the oracle under `pre_2026_07_22_whole_cap_per_leg` and
> **not** the current expected output. §0 and the §7 acceptance test already carried the corrected
> `(8, 60)` pin; this line and §2.2's `reserve_cap` did not, so the file contradicted itself. An
> implementer following §2.2 would have divided the **whole account cap** per leg — **153 micros
> against an 80 limit (1.91×)**. Source: claim-alignment audit **B3**.
>
> ⚠ **Same-date Status note (claim-alignment SP-20):** the header "Remaining before `Accepted`"
> checklist was replaced the same day — two items DISCHARGED, two stranded by venue de-scope;
> Status stays `Proposed` deliberately. §2.2 / leg map / state contract / fail-safe untouched.

### §2.3 — New infrastructure this spec introduces (named honestly, not hidden)

**Peak-equity tracker** (`c1_dd_state.json`, host-local, one file per live account — **not** `core/dd_protection_state.json`, which is FXIFY/CFD-book-scoped): `{"account": "Tradeify_Select_100K", "peak_equity": <float>, "last_updated_utc": "<iso8601>"}`. Updated on every NT8 account-equity-change callback; ratchets up only. Atomic write (temp file + rename), mirroring `dd_protection.py`'s own atomic-write discipline.

**Firm/leg constants mirror** (`c1_sizing_constants.json`, host-local, pinned from `firm_rules.py` + locked Pine at implementation time): `{E_firm, cap_firm, cost_per_side_usd}` per tier + the §2.1 leg map, which **must carry `cap_alloc` per leg** — §2.2's `reserve_cap` divides by it, and a missing `cap_alloc` **HALTS** (§5) rather than falling back to `cap_firm`. `cap_firm` is retained as the account-aggregate **bound** only (`Σ cap_alloc ≤ cap_firm`). **Audit hook (§10) re-diffs this file against `firm_rules.py`** — the NT8/.NET runtime cannot import Python at trade time, so a periodic re-pin is the mechanism (same M-9 shape as `PORT_MANIFEST.sha256`/`MANIFEST.sha256`).

### §2.4 — Order-submission transport (the one open integration question — named, not guessed)

Q-RAIL-1 PHASE3.md §2d screened this to "PASS via row B" using only vendor-doc-level evidence. Neither this spec's author nor the Q-RAIL-1 session has inspected CrossTrade's actual Pro-tier NT8 Add-On configuration surface (that requires the Pro subscription — GO ADR build step B3, not yet reached). Two candidate wirings, both compatible with §2.2's algorithm and §5's fail-safe:

| Option | Mechanism | Resolves at |
|---|---|---|
| **A (preferred if available)** | `C1SizingHost` runs its own listener (local HTTP endpoint or file-drop) parallel to CrossTrade, receiving the same TV alert JSON directly; computes qty; submits via NT8's Automated Trading Interface (ATI) directly — bypassing CrossTrade's own qty for entry/add orders. CrossTrade Pro's Account Manager is still used for EOD flatten (E1), trailing-DD alerts, and connection monitoring — none of which need this sizing law. | B3–B5, once CrossTrade Pro's actual webhook-routing options are visible |
| **B (fallback)** | CrossTrade forwards/exposes the raw incoming payload to a location the host can read (if Pro-tier config supports a custom pre-submit hook); the host overrides the `qty` field on CrossTrade's own order before it reaches the exchange. | Same |

**Resolution rule:** Cursor/operator picks at B3–B5 empirically and records the choice as a dated addendum to this spec — not a silent implementation detail. The algorithm and fail-safe are correct and testable under either option; only the JSON-in-qty-out transport differs.

**Addendum 2026-07-18 (B3 empirical input — CrossTrade "Tradovate Goes GA!" dashboard changelog):** CrossTrade's direct-Tradovate support left beta: webhooks, shared commands (place/limit/stop/close/flatten/cancel/reverse), Strategy Sync on Tradovate, and a full server-side REST API (`/v1/api/tv`) that "works with NinjaTrader closed." This surfaces a third candidate:

| Option | Mechanism | Status |
|---|---|---|
| **C (new — potentially eliminates the NT8 hop AND the C# port)** | Local sizing host (the already-tested Python reference, hardened) receives the TV alert JSON, computes qty per §2.2, submits via CrossTrade REST `/v1/api/tv` → Tradovate directly. CrossTrade Account Manager still handles E1 flatten / DD guard / monitoring. | **Load-bearing unknown RESOLVED YES 2026-07-18** (below). Second unknown — the qty-injection mechanic — still open; **NOT adopted**. |

**Resolution 2026-07-18 (operator-executed, browser-verified):** CrossTrade's Tradovate-direct linking is a proper OAuth flow — clicking "Link Tradovate" on the CrossTrade dashboard routes to `trader.tradovate.com/welcome` (Tradovate's own login page; CrossTrade never sees the password) and returns a scoped token (read: profile/prices/positions/contract-library; write: chat/users/orders/accounting/alerts/risks). CrossTrade's own onboarding page names Tradeify explicitly: *"Trading a prop firm account (Apex, Topstep, Tradeify, etc.)? Click Link Demo and sign in with the Tradovate username and password your firm issued. Funded-firm accounts, including funded/PA accounts, live on the Demo environment. Link Live is only for a personal real-money Tradovate login."* **"Demo environment" here is Tradovate's naming for the API surface prop-firm accounts sit on — it does not mean simulated/no-consequence; the Tradeify eval trading through it is the real account.** Operator clicked **Link Demo**, signed in with the Tradeify-issued credentials, link succeeded with **no "limited functionality" message** — the concern from Tradovate's own generic warning banner did not materialize for this flow. Dashboard now shows **Tradovate: Connected** (green) simultaneously with **NT8 Add-On: Connected** — both links are live at once, non-conflicting so far. One open detail: the Accounts panel under the Tradovate view showed "No accounts on Tradovate" immediately after linking — the specific Tradeify sub-account may need an explicit selection step; unverified whether this is a sync delay or a missing action.

**Second unknown RESOLVED YES 2026-07-18 (docs-verified, `crosstrade.io/docs/api/webhook-trading` + `crosstrade.io/docs/webhooks/commands/place-order`):**

- **Auth mechanism named exactly:** webhook URL is `https://app.crosstrade.io/v1/send/{webhook-id}/{secret-key}`; the account Secret Key additionally rides in the payload body via `key=...;`. Verbatim: *"no difference between the way these webhooks are sent and any other external webhook CrossTrade receives."* This means our own code — not just TradingView — can legitimately POST a well-formed payload with the account's own Secret Key and CrossTrade processes it identically. Resolves the "must a listener sit between TV and CrossTrade" question in the simplest possible way: it doesn't have to intercept anything — **TV's webhook alert can point directly at our listener; our listener then sends CrossTrade its own authenticated call**, using the same Secret Key CrossTrade already issued for this account.
- **Destination-agnostic confirmed:** `destination=tradovate;` is documented as an add-on to the *same* webhook-trading path used for NT8 — verbatim: *"Add `destination=tradovate;` for a linked Tradovate account"* applies uniformly, "not just TradingView-originated" calls. A separate Tradovate-specific PLACE section (`place-order` docs) confirms full support: `destination=tradovate;` including `flatten_first`, native TP/SL brackets, iceberg, trailing stops, MIT, extra TIFs.
- **`qty` is a plain writable integer field** (`qty=1;` in the docs' own example; no restriction against a program-computed value found in either doc — consistent with the original Options A/B finding, `docs/webhooks/commands`: "QTY = any integer; required on PLACE").
- **Concrete implementation shape (mostly already-tested code, not a from-scratch build):** `tests/rail_crosstrade/translator.py::appendix_a_to_crosstrade()` already builds this exact CrossTrade semicolon payload shape from a structured intent object (P5 golden-path infra, currently test-support only). Option C's remaining work is genuinely small: (1) promote that translator to a production module parameterized by destination/account/secret; (2) a thin HTTP listener that TV's alert points at directly, which calls `ops/c1_rail/c1_sizing_host_reference.py::process_signal()` for the qty decision and, on a non-halt result, builds and POSTs the CrossTrade payload via the promoted translator. No C#, no NT8 dependency in the execution path.

**Architecture pivot ADOPTED 2026-07-18 (operator decision, via explicit choice among three options).** Cursor's C# NinjaScript port is no longer needed; the NT8 spine (already wired, ATI enabled) stays connected as a dormant fallback rather than being torn down. Built same day, TDD (RED verified first): [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) (8 tests) promotes `tests/rail_crosstrade/translator.py`'s payload shape to production with `destination=` parameterization; [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) (9 tests) is the decision-routing layer tying `C1SizingHostReference` to a live CrossTrade order. The RED→GREEN cycle caught a real bug before it shipped: the sizing host's `submit` field is unconditionally `False` for exit/flat signals (correct in its own context — no sizing math runs for a close), which is *not* the right gate for "should the listener relay a close command" — an early implementation would have silently swallowed every exit/flat signal. Fixed before any code ran against real data.

The §2.2 algorithm, §2.1 leg map, state contract, and §5 fail-safe are transport-invariant — nothing above this section changes under any option.

### §2.5 — Always-on deployment: inbound-auth + live-equity contract (2026-07-18, operator decisions frozen for Cursor)

Two deployment decisions were made 2026-07-18. Both are frozen here as implementation contract (CC specifies / Cursor implements per the 2026-07-14 surface-allocation ADR); both are acceptance items at B6. **Implemented 2026-07-18** in [`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) (helpers unit-tested; socket + real urllib GET untested-by-design). Operator still owes always-on host + TLS proxy standup and the live `equity_field` verify before flipping `equity_source` off `file`.

**Decision 1 — always-on host (not a laptop tunnel).** The listener runs on a persistent always-on host; TradingView's alert webhook posts to it directly. This makes the endpoint **public**, which promotes inbound authentication from optional to **required before `dry_run=false`**.

**(A) Inbound-auth contract — REQUIRED.** `c1_rail_http_server.py::do_POST` currently processes any POST regardless of `self.path` — safe only on the `127.0.0.1` bind, unsafe the instant the endpoint is reachable by TradingView. An unauthenticated public POST of a crafted B1 payload triggers a live order once armed. Contract:

- Config gains **`path_token`** — a long random string (≥32 chars), gitignored with the other secrets.
- The server accepts sizing POSTs **only** at `POST /c1/<path_token>` (exact match against `self.path`). Any other path → **404, no body parse, no equity read, no `handle_signal`** — reject *before* touching state.
- The token is a **URL-path** secret, deliberately **not** a payload field — this keeps the B1 payload (and therefore the locked/hashed Pine editions) byte-unchanged. TradingView's webhook URL carries the token: `https://<host>/c1/<path_token>`.
- Health-probe `GET /` stays unauthenticated (no side effects); GET never sizes (already true — keep it that way).
- **TLS:** an always-on endpoint receiving order-triggering webhooks must be **HTTPS**. The stdlib `ThreadingHTTPServer` is plain HTTP by design — TLS terminates in front of it, in one of two valid topologies (the invariant is: the app never faces the public internet directly, and the path-token never traverses the wire in cleartext):
  - **Same-box reverse proxy** (a VPS with Caddy/nginx): proxy terminates TLS and forwards to the **loopback**-bound app — `bind_host=127.0.0.1`, proxy → `127.0.0.1:8787`.
  - **Managed-edge TLS** (Fly.io — the topology DECIDED 2026-07-18): the platform's edge terminates TLS and routes to the container's internal port over the platform's private network; the app binds the **container interface** — `bind_host=0.0.0.0`, `bind_port` = the platform's `internal_port`. Binding `0.0.0.0` here is NOT a public exposure: the only ingress is the edge proxy (no public IP reaches the container directly), so the security property is identical to the loopback case. The `deploy/c1_rail/` scaffolding (`Dockerfile` + `fly.toml` + runbook) implements this variant; `c1_rail_config.fly.example.json` carries `bind_host=0.0.0.0`, `bind_port=8080`.

  The path-token is the app-level auth gate under either topology; TLS keeps it off the wire in cleartext.

*B6 acceptance (auth):* a POST to a wrong path returns 404 with **no** audit-log sizing entry and **no** equity read; a POST to the correct `/c1/<path_token>` with a valid B1 payload sizes as expected.

**(B) Live-equity contract — replaces the interim file source.** The skeleton reads `current_equity` from a local `equity_path` JSON (interim; the module docstring itself flags "Tradovate live account-status read still owed"). Frozen live source (researched 2026-07-18 against `crosstrade.io/docs/api/accounts/get-account` + `.../get-accounts`):

- **`GET https://app.crosstrade.io/v1/api/tv/accounts/{account}`**, header `Authorization: Bearer <crosstrade_api_token>` → `{"success": true, "data": {…}}` carrying a balance snapshot. Use the **net-liquidation-equivalent** figure (the NT8 twin `GET /v1/api/accounts/{account}` returns `item.netLiquidation` explicitly; the Tradovate snapshot's exact key is **verify-once at B6** against a live response — do **not** hardcode a guessed name).
- New config key **`crosstrade_api_token`** — a **third**, distinct CrossTrade credential (separate from `secret_key` and `webhook_secret`; generated in the CrossTrade dashboard, gitignored). Account identity resolved once via `GET /v1/api/tv/accounts` (`accountId` / `name`), pinned into config.
- **Fail-closed, discipline unchanged:** any non-`success` body, HTTP error, timeout, or missing/implausible (≤0, non-finite) equity routes to the **same** `EquityReadError` path already implemented (CRITICAL log + HTTP 503 + no `handle_signal`, never invent equity). Per-signal fresh read (15m bars — one extra round-trip is immaterial), then the existing `ratchet_peak_equity`.
- Keep the file-based `read_current_equity` as a **documented test/fallback hook** (it is how the Phase-1/2 unit tests inject equity with no network). Select via a new config key `equity_source: "crosstrade" | "file"` (default `"crosstrade"` once the field name is B6-verified; `"file"` until then, so today's interim behavior is the explicit default, not an accident).

**Field-name caveat (Rule-0 honesty):** the exact balance field name inside the Tradovate `data` object is the one thing not verifiable from docs. Verify against a single live `GET` response before flipping `equity_source` to `"crosstrade"`; until then `"file"` stays authoritative.

**Config-template delta (Cursor, same commit as the implementation):** [`docs/notes/rail_build/c1_rail_config.example.json`](../notes/rail_build/c1_rail_config.example.json) gains `path_token`, `crosstrade_api_token`, and `equity_source` — all with `REPLACE`/default placeholders, never live values.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Reuse `core/dd_protection_state.json` for peak-equity** | Different account, different equity curve (FXIFY $200K CFD book vs this $100K futures eval); reusing it would silently cross-contaminate two unrelated peak trackers. A leg-scoped tracker (§2.3) is genuinely new but correctly isolated infrastructure. |
| **Fall through to `core/lifecycle.py`'s absent-file default (AUTHORIZED, 1.0×) on any read failure** | That default is safe for the read-only `ops/cli.py lots` display surface but wrong for a live rail — Q-PYRPARITY-1/the parent spec's whole premise is that this leg runs at WATCH-1, never 1.0×, by design; a read-failure fail-open to 1.0× would silently double the intended risk. Ruled out in favor of the §5 fail-to-zero rule. |
| **TV computes qty, host only relays it** | FALSIFIED upstream by Q-PYRPARITY-1 (TV qty ceiling breaks proportionality) — the entire reason this host exists. |
| **CrossTrade computes the sizing law itself (no separate NT8 host)** | PHASE3.md §2d row A: CrossTrade documents `qty` relay, not derivation from stop distance/lifecycle/DD — no computation hook exists at that layer. |
| **Recompute stop distance from NT8's own market data instead of trusting the payload's `stop_dist_pts`** | Offline-port trap (standing lesson: a parallel stop implementation can silently diverge from Pine's own ATR calc). The payload's `stop_dist_pts` is Pine's own value at signal time — the host consumes it, never re-derives it. |
| **Skip the `DRY_RUN` mode; treat the operator's first live session as the dry-fire** | Untestable and irreversible if the algorithm has a bug — a real "fire but log-only" mode (§5) is the only way B6 can be a genuine gate rather than a hope. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** if **any** of — (a) the §7.1 unit test fails to reproduce `f2_floors.json`'s `(8, 60)` MYM recent-90d numbers exactly (re-pinned 2026-07-22 from `(9, 67)`); (b) the §7.4 `DRY_RUN` dry-fire logs a `qty_out` that disagrees with hand-computed expectation for a live test alert; (c) neither §2.4 Option A nor Option B proves implementable once CrossTrade Pro's actual configuration surface is inspected — then this spec is **falsified as specified**.

**Falsified action:** (a)/(b) → halt Cursor implementation, return to CC for spec revision (the algorithm or state contract has an error CC's design didn't anticipate — not a Cursor-side patch-around). (c) → escalate to Q-RAIL-1 as an **F1-realization FAIL** per PHASE3.md's own ordered fallback (§4 of the parent spec: if no host on the chain can run the computation, score the affected rail tier FAIL — do not degrade to a TV-side alternative already ruled out in §3).

**Trigger check:** B6 dry-fire gate itself (GO ADR §4/§7) is the check — this spec's falsifier and the GO ADR's revert trigger are the same event, not two independent gates.

---

## §5 — Forbidden moves (under this spec)

- **Falling through to a default multiplier (1.0×, "last known good", or any non-zero guess) on a read failure** — the ONLY safe default under any state-read failure is `qty_out = 0` (no order). Tempting because it "keeps trading" through a transient glitch; ruled out because a wrong-size live fill is worse than a missed signal.
- **Reusing `dd_protection_state.json` for this account's peak-equity** — tempting because it's existing, tested infrastructure; ruled out in §3 (account cross-contamination).
- **Applying the lifecycle haircut a second time anywhere else in the rail** (e.g., also scaling in the Pine layer or in a CrossTrade template) — standing doctrine (lifecycle ADR): one layer owns the haircut. This host is that one layer for c1's live sizing.
- **Recomputing `stop_dist_pts` from NT8's own feed instead of trusting the payload** — offline-port trap; ruled out in §3.
- **Shipping without `DRY_RUN`** — the GO ADR's B6 gate has no teeth without it; ruled out in §3.
- **Amending §4's falsifier if the dry-fire "almost" passes** — a near-miss gets a spec revision cycle, not a loosened acceptance threshold (Trap #12, inherited from brief-authoring discipline).

---

## §6 — Consequences

**Positive:**
- WATCH/DD/account scaling collapse to one audited, testable computation with a concrete pass/fail oracle (`f2_floors.json`).
- The fail-safe (§5) makes "silently sized wrong" structurally impossible — every failure mode halts rather than guesses.
- `DRY_RUN` makes B6 a real gate, not an act of faith on the first live session.

**Negative (real):**
- Genuinely new infrastructure (peak-equity tracker, constants mirror) with its own bugs to find — this is new surface area, not a reuse of anything battle-tested.
- The constants mirror (`c1_sizing_constants.json`) is a cross-language duplication of `firm_rules.py` values that needs a re-pin discipline or it drifts silently (same class of gap `PORT_MANIFEST.sha256` already closes elsewhere).

**Risks:**
- **Instrument-symbol format is provisional, not verified** — `ops/c1_rail/c1_rail_listener.py::INSTRUMENT_SYMBOLS` uses TV's own continuous-contract notation (`MYM1!`, `MNQ1!`, matching the P5 golden-path fixture convention already in this repo) as a placeholder for the order-ticket symbol CrossTrade actually needs on a Tradovate-destination PLACE command. This must be checked against a real order (or CrossTrade's docs, if they specify) at B6 — do not assume it is correct for a live order without that check.
- **Deployment/reachability — DECIDED 2026-07-18: always-on host** (§2.5). §2.5(A) path-token + TLS-at-proxy **implemented** in [`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) (unit-tested helpers; host+TLS standup still operator). Hard B6 precondition remains: wrong-path POST must 404 with no audit sizing entry.
- Equity-peak tracking timing/reliability under Option C depends on how `current_equity` is sourced into `handle_signal`. Interim (explicit default, `equity_source="file"`): local `equity_path` JSON + peak ratchet. **Live source wired in §2.5(B)** — CrossTrade REST `GET /v1/api/tv/accounts/{account}` (Bearer `crosstrade_api_token`, config-driven `equity_field`); one field-name verification owed at B6 before flipping the default.
- NT8 account-equity callback timing/reliability is now moot under Option C (no NT8 read in this path) but stays a live concern if the NT8 fallback is ever activated instead.

**Downstream artifacts (updated 2026-07-18):**
- GO ADR §7 build order: B2 moved from "algorithm + transport implemented and tested; HTTP-server adapter + deployment still owed" to "algorithm + transport + HTTP adapter present; deployment/reachability + live equity + B6 still owed."
- This spec's Status stays `Proposed` — flips to `Accepted` once §7 Phase 4's B6 dry-fire passes for real (HTTP adapter alone does not flip it).
- §2.4's resolved transport option is recorded above as a dated addendum, not a silent edit.

---

## §7 — Implementation plan (test plan Cursor implements against; B6 consumes the result)

- **Phase 0** — Cursor re-verifies §0's anchors are still current at implementation time.
- **Phase 1 — Unit test (worked-check reproduction, must pass before any dry-fire):**
  Input: `leg_id="dj30_mym"`, `signal_type="entry"`, `stop_dist_pts=60.8201`; `lifecycle_state.json={"Striker":"WATCH-1"}`; `peak_equity=current_equity=100000` (no DD); constants `E_firm=100000, cap_firm=80, cap_alloc=69, pyr_pct=750, dollars_per_pt=0.50`.
  Expected: `dd_scale=1.0`, `lifecycle_m=0.50`, `r_eff=0.0035`, `qty_base_raw=floor(350/30.41)=11`, `reserve_cap=floor(69/8.5)=8`, **`qty_out=8`**.
  Then `signal_type="add"` (same leg, `executed_base_qty=8`): **`qty_out=floor(8×7.5)=60`**.
  *(Re-pinned 2026-07-22: `reserve_cap` divides this leg's **allocated share** of the account cap, not the whole `cap_firm` — Tradeify's limit is account-aggregate. Pre-split values were `reserve_cap=floor(80/8.5)=9`, `qty_out=9`, add `67`.)*
  Both must match [`f2_floors.json`](../../lab/analysis/c1/q_rail_1_2026-07/f2_floors.json) `legs[0].recent_90d.{base_capped, add_qty}` exactly.
- **Phase 2 — Fail-safe test:** delete/corrupt each of the three state files in turn; confirm `qty_out=0`, no ATI submit call, `CRITICAL` logged, desk notification fired.
- **Phase 3 — DD-trigger test** *(values corrected 2026-07-18 — the original vector `peak=101521, equity=100000` gives dd = 1.4982%, which rounds BELOW the trigger; and DD_SCALE is 0.40, so "exactly half" was wrong)*: set `peak_equity=100000, current_equity=98500` (dd_from_peak = 1.5% exactly at `DD_TRIGGER`); confirm `dd_scale=0.40` applies multiplicatively — MYM recent-90d at WATCH-1+DD: `r_eff = 0.0070×0.40×0.50 = 0.0014` → `qty_out = floor(140/30.41005) = 4` (0.40× the raw, not half). Companion negative case: `current_equity=98500.31` (dd ≈ 1.4997%, rounds below trigger) → `dd_scale=1.0`, `qty_out=8` (re-pinned 2026-07-22).
- **Phase 4 — Dry-fire (B6, live):** `DRY_RUN=true`, fire a real Webhook Trader test alert through the actual wired transport (§2.4, whichever option is selected); confirm the audit log shows the correct computation and **no live order was placed**. Only then flip `DRY_RUN=false` for the first armed session (GO ADR B7).

---

## §10 — Audit hooks (runnable)

```bash
# The sizing-law composition matches production (same shape as dd_protection.py)
grep -n "scaled_risk = {k: v \* multiplier \* lifecycle" core/dd_protection.py
# Lifecycle ladder unchanged
grep -n "TIER_MULTIPLIER = {" -A4 core/lifecycle.py
# BASE_RISK keys/values unchanged (leg map §2.1 depends on these)
grep -n "BASE_RISK = {" -A5 core/dd_protection.py
# Firm constants unchanged (re-run before any c1_sizing_constants.json re-pin)
grep -n "Tradeify_Select_100K\|MFFU_Rapid_100K" -A13 core/firm_rules.py | grep -n "starting_balance\|micro_contract_cap\|cost_per_side_usd"
# Worked-check oracle still matches this spec's §7 unit test
python -c "import json; d=json.load(open('lab/analysis/c1/q_rail_1_2026-07/f2_floors.json')); r=d['legs'][0]['recent_90d']; assert (r['base_capped'], r['add_qty'])==(8,60), r; print('MYM 8/60 OK')"
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/spec/c1_nt8_sizing_host_impl.md --type adr
git log -1 --format="%h %cs" -- core/lifecycle.py core/dd_protection.py core/firm_rules.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-17 | Initial authoring (Q-RAIL-1 B2, GO ADR build step) | Joshua + Claude Code |
| 2026-07-18 | **Python reference implementation landed** ([`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) + [`tests/ops/test_c1_sizing_host_reference.py`](../../tests/ops/test_c1_sizing_host_reference.py), 29 tests green, TDD) — proves §2.2 against the committed `f2_floors.json` oracle (all four leg×window rows) + full fail-safe battery. The NinjaScript port must match this reference at B6. **§7 Phase-3 vector corrected** (original `peak=101521` rounds below the trigger; "exactly half" → 0.40×) — caught by the RED phase, which is the point. Status stays `Proposed`: the C#/NinjaScript implementation and B6 dry-fire are still owed. | Joshua + Claude Code |
| 2026-07-18 | **§2.4 addendum: Option C recorded** (CrossTrade "Tradovate Goes GA" — server-side REST `/v1/api/tv`, works with NT8 closed). Candidate only; adoption gated on the firm-login compatibility check at B5 + operator sign-off. If adopted, the Python reference becomes the production-host candidate and the C# port is mooted — a supersede-in-part, not an edit. | Joshua + Claude Code |
| 2026-07-18 | **§2.4: firm-login compatibility unknown RESOLVED YES** — operator linked the Tradeify-issued Tradovate account via CrossTrade's OAuth "Link Demo" flow, no limited-functionality warning, dashboard shows Tradovate + NT8 both Connected simultaneously. Second unknown (qty-injection mechanic under the Tradovate-direct destination) still open — Option C remains NOT adopted pending that check + operator decision. | Joshua + Claude Code |
| 2026-07-18 | **§2.4: second unknown RESOLVED YES** (docs-verified) — CrossTrade's webhook auth is a URL+Secret-Key pair with no TV-specific gating ("no difference... any other external webhook"); `destination=tradovate;` works identically on the same path; `qty` is a plain writable field. Both Option C unknowns now resolved favorably. Implementation shape named: promote `tests/rail_crosstrade/translator.py` to production + a thin listener wired to `ops/c1_rail/c1_sizing_host_reference.py`. **Still NOT adopted** — the NT8-vs-Option-C architecture choice is an operator decision, not made here. | Joshua + Claude Code |
| 2026-07-18 | **Option C ADOPTED** (operator decision) — built + tested TDD: [`ops/c1_rail/crosstrade_payload.py`](../../ops/c1_rail/crosstrade_payload.py) (8 tests), [`ops/c1_rail/c1_rail_listener.py`](../../ops/c1_rail/c1_rail_listener.py) (9 tests). RED phase caught a real gating bug (sizing host's `submit` field is always `False` for exit/flat by design — not the right signal for "should the listener relay a close"). Full suite 862 passed, `check_boundaries` OK. NT8 spine stays wired as dormant fallback, not torn down. Open before `Accepted`: HTTP-server adapter, deployment/reachability decision, instrument-symbol-format verification, B6 dry-fire. | Joshua + Claude Code |
| 2026-07-18 | **HTTP-server socket adapter landed** ([`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) + config template [`docs/notes/rail_build/c1_rail_config.example.json`](../notes/rail_build/c1_rail_config.example.json)) — thin, untested-by-design process wrapper around `handle_signal`; interim file-based `equity_path` + peak ratchet into `c1_dd_state.json`. Open before `Accepted`: deployment/reachability, instrument-symbol format, Tradovate live equity read, B6 dry-fire. | Joshua + Cursor |
| 2026-07-18 | **§2.5 added — always-on deployment: inbound-auth + live-equity contract frozen.** Operator chose an always-on host (public endpoint). CC found the landed skeleton's `do_POST` has **no inbound auth** (processes any POST regardless of `self.path`) — safe on the `127.0.0.1` bind, an open order-placing surface the moment it's public. §2.5(A): path-token gate (`POST /c1/<path_token>`, 404-before-state on mismatch) + TLS-at-proxy, hard B6 precondition. §2.5(B): live equity read frozen to CrossTrade REST `GET /v1/api/tv/accounts/{account}` (Bearer `crosstrade_api_token`, a third credential), same fail-closed path; `equity_source` config key, file interim stays default until the balance field name is B6-verified. Config-template delta owed in Cursor's implementing commit. | Joshua + Claude Code |
| 2026-07-18 | **§2.5 implemented** ([`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) + [`tests/ops/test_c1_rail_http_server.py`](../../tests/ops/test_c1_rail_http_server.py)): path-token gate (404 before parse/equity/`handle_signal`), `equity_source` file/crosstrade dispatch with config-driven `equity_field` (no hardcoded guess), fail-closed into existing `EquityReadError` path, config template gains `path_token`/`crosstrade_api_token`/`equity_field`/`equity_source`. Socket + real urllib GET remain untested-by-design. Open before `Accepted`: always-on host+TLS standup, live `equity_field` verify, symbol format, B6 dry-fire. | Joshua + Cursor |
| 2026-07-18 | **§2.5(A) TLS bullet generalized to two topologies + Fly.io deploy scaffolding added.** Always-on host chosen = **Fly.io** (managed-edge TLS). Clarified that `bind_host` depends on topology: `127.0.0.1` for a same-box reverse proxy, `0.0.0.0` for managed-edge TLS (Fly) where the app faces only the edge proxy over a private network — same security property, not a public exposure. Scaffolding at [`deploy/c1_rail/`](../../deploy/c1_rail/) (`Dockerfile` stdlib-only 10-module subset, `fly.toml` always-on single-machine + edge TLS + `/data` volume, `.fly.example.json` config, README runbook) + repo-root `.dockerignore` (default-exclude; keeps Pine/CSV/research out of the build context). Subset proven import-complete by running the server from an isolated `/app`-layout (404 unauthorized / `qty=9` authorized). Not built/deployed via Docker locally (none installed) — first `fly deploy` is the real build test; failure mode is safe (missing COPY → loud build fail). | Joshua + Claude Code |
