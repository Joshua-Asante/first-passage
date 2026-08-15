# Q-RAIL-1 Phase 3 — rail architecture selection

**Date:** 2026-07-17 (rev 2 — adversarial review fixes same day)  
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) §7 Phase 3  
**Sizing contract:** [`docs/spec/c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md) (`Accepted` 2026-07-17) — Phase-3 bridge-capability screen is this spec's §4 falsifier  
**Scope:** document the concrete per-tier chain from primary sources; attended-operation posture; failure modes + manual-intervention protocol; **bridge payload-qty capability screen**. **No CrossTrade/NT8 wiring, no account registration, no spend** (brief §5).

**Prior inputs:** [`PHASE0.md`](PHASE0.md) · [`PHASE1.md`](PHASE1.md) · [`PHASE1B.md`](PHASE1B.md) · [`F_SCORECARD.md`](F_SCORECARD.md) · rail note [`docs/notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md`](../../../docs/notes/2026-07-06-rail-reconciliation-traderspost-vs-crosstrade.md) · Q-AUTO-FIRM-1 (LTM)

---

## 1. Selected spine (both discharge tiers)

| Hop | Component | Role |
|---|---|---|
| 0 | TradingView chart (venue edition MYM / MNQ) | Signal + alert fire; Pine owns entry/exit/pyramid/EOD force-flat; **does not own live qty** (F1 fallback) |
| 1 | TradingView webhook → CrossTrade cloud | Authenticated `key=value;` payload; ~30 ms alert-to-execution (vendor claim) |
| 2 | CrossTrade NT8 Add-On | Receives WebSocket command; submits via NinjaTrader ATI |
| 3 | NinjaTrader 8.1+ | Order placement + connection to firm feed; **candidate host for the §2 sizing law** (spec §4 fallback) |
| 4 | **Tradovate** (firm credentials) | Execution venue for **both** Tradeify Select and MFFU Rapid under the CrossTrade path |

**Not selected for c1 go-live scoping:**

| Alt | Why deferred |
|---|---|
| NT8 → **Rithmic** | Discharge-tier CrossTrade connection guide lists Tradeify and MFFU as **NinjaTrader (Tradovate)**, not Rithmic. Tradeify Rithmic/TradeSea is a *different* checkout broker and does **not** open NT8 ([Tradeify NT8 setup](https://help.tradeify.co/en/articles/12268716-ninjatrader-8-setup-guide) + CrossTrade prop-connection guide). Rithmic remains the Bulenox path from the 2026-07-06 rail note — out of scope for this packet. |
| TV → Tradovate native add-on (no CrossTrade) | Firm-supported on Tradeify Tradovate accounts; loses CrossTrade Strategy Sync / Account Manager EOD safeguards that map to E1/F4. Not the envelope E6 reference rail. **Extra strike:** envelope §4 Tradeify row — **Tradovate API is LIVE-funded only**, so this alt is likely unavailable on eval. |
| TradersPost → Tradovate | Superseded 2026-07-06 (wrong rail for the NT8 stack; Q-BTC-3 lights-out lane already falsified). |

**Canonical string for the packet:**  
`TV alert → CrossTrade cloud → NT8 Add-On → Tradovate (Tradeify Select **or** MFFU Rapid)`

**WATCH-1 sizing (normative — not ambiguous):** per [`c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md) §2, every risk_pct-layer multiplier (account / lifecycle / DD) is realized as **one combined integer-floored qty computation at a single rail-side scaling point downstream of TradingView**. TV stays at panel-of-record config; the alert carries `{leg_id, signal_type, bar_time, close, stop_dist_pts}` — **never** TV-computed qty as the sizing source. Ruled out by that spec §3: TV risk%-input scaling, `floor(qty_tv × M)`, and setting TV `initial_capital` / accountSize to the effective value.

---

## 2. Per-tier connection (primary sources, fetched 2026-07-17)

### 2a. Tradeify_Select_100K

| Field | Value | Source |
|---|---|---|
| CrossTrade product page | Select included; TV webhooks → NT8 → Tradeify Tradovate; ~30 ms | [crosstrade.io/prop-firms/tradeify](https://crosstrade.io/prop-firms/tradeify) |
| Connection type | **NinjaTrader (Tradovate)** | [CrossTrade prop-firm connection guide](https://crosstrade.io/docs/getting-started/prop-firm-connection-guide) |
| Firm NT8 setup | Login `trader.tradovate.com` first → sign Non-Professional Data Agreement → wait ≤15 min → NT8 with Tradovate creds; **Account Type = Simulation** on Evaluation / Sim Funded | [help.tradeify.co …/12268716](https://help.tradeify.co/en/articles/12268716-ninjatrader-8-setup-guide) (fetched 2026-07-17) |
| Checkout constraint | Broker connection chosen at purchase is sticky; **NT8 requires Tradovate broker**, not Rithmic/TradeSea | CrossTrade guide + Tradeify NT8 guide; Tradeify marketing platform post (secondary) |
| Flat deadline | **16:59 ET** regular / **12:59 ET** holiday-short; auto-flatten non-fatal | Envelope §4 (2026-07-13); Phase 0 HOLD on help article body render |
| CrossTrade EOD safeguard (vendor) | Account Manager schedule example **4:55 PM ET**; holiday calendar-aware flatten advertised | CrossTrade Tradeify page |
| Automation ToS | FTA §6.6 sole-owner bots OK; no HFT; **exclusive use within Tradeify (not across multiple firms)** | [`PHASE0.md`](PHASE0.md) |
| Commission model (engine) | `$0.91`/side | `firm_rules.py` `Tradeify_Select_100K` |

**Implication:** at account registration (post-GO), purchase must select **Tradovate** or the CrossTrade/NT8 rail cannot attach. Rithmic/TradeSea checkout = wrong pipe for this architecture.

### 2b. MFFU_Rapid_100K

| Field | Value | Source |
|---|---|---|
| CrossTrade product page | Core/Pro/Rapid; TV → NT8 Add-On; Tradovate among listed platforms | [crosstrade.io/prop-firms/my-funded-futures](https://crosstrade.io/prop-firms/my-funded-futures) |
| Connection type | **NinjaTrader (Tradovate)** | CrossTrade prop-firm connection guide § My Funded Futures |
| Setup | Login `trader.tradovate.com` with MFFU creds → sign live market data agreement → NT8 connection **Account Type = Simulation** → green status | Same guide |
| Instruments | MYM + MNQ on firm instrument list; round-trip all-in **$1.90** each (primary fee table) | [MFFU article 9735811](https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list) (fetched 2026-07-17; "Updated this week") |
| Flat deadline | Session 18:00 ET → **16:10 ET** auto-liq; **post-16:10 orders can DISQUALIFY**; holiday half-days **no** auto-liq | [`PHASE0.md`](PHASE0.md) / article 9558251 |
| E1 build target | Pine + CrossTrade force-flat **≤16:00 ET** (≥10 min inside 16:10) | Envelope E1 + F4 PASS |
| Automation ToS | Own-settings automated strategies OK; HFT banned | [`PHASE0.md`](PHASE0.md) / article 8444599 |
| Commission model (engine) | `$0.95`/side | `firm_rules.py` `MFFU_Rapid_100K` |

**Geometry note (do not resolve here):** CrossTrade marketing describes Rapid trailing as **intraday**; `firm_rules.py` encodes Rapid as `trailing_locking` (EOD MLL + $100 lock). Phase 4 / post-GO wiring must re-read MFFU Rapid primary rules and configure Account Manager to the **firm** print, not the vendor summary.

### 2c. Shared CrossTrade hops (both tiers)

| Step | Requirement | Source |
|---|---|---|
| TV account | Webhooks require **2FA** enabled | [CrossTrade TradingView Alerts docs](https://crosstrade.io/docs/getting-started/tradingview-alerts) (search/index 2026-07-17; full page fetch timed out — treat as vendor doc claim to re-open at wiring) |
| Alert message | **Only** CrossTrade `key=value;` payload — strip TV default strategy text | Same docs + [your-first-automated-trade](https://crosstrade.io/docs/getting-started/complete-guides/your-first-automated-trade) |
| NT8 | Multi-provider enabled; restart after toggle; Add-On logged in and connected | Connection guide |
| Bridge pricing | List: Standard **$29**/mo · Pro **$49**/mo · Elite **$99**/mo (7-day trial). FAQ (same page, re-fetched 2026-07-17): **Account Manager (incl. auto-flatten) is Pro ($49)+ / Elite** — Standard is webhooks + journal + manual dashboard only. **E1 bridge cost floor = $49/mo.** | [crosstrade.io/pricing](https://crosstrade.io/pricing) FAQ: "Pro ($49/mo) adds the Trade Copier, NT8 Account Manager, and full REST API" |

### 2d. Bridge payload-qty capability screen (spec §4 falsifier)

**Question (verbatim from [`c1_watch_realization_multiplier_layer.md`](../../../docs/spec/c1_watch_realization_multiplier_layer.md) §4):** can the candidate chain set per-order quantity from **computed** payload fields — or does it only mirror a TV-supplied qty / fixed presets with no computation hook?

| Candidate | Per-order `qty` settable from payload? | Computes sizing law from `{stop_dist_pts,…}`? | Doc cite | Score |
|---|---|---|---|---|
| **A. TV → CrossTrade webhook → NT8 → Tradovate** (selected spine) | **YES** — `PLACE` requires `qty` as an integer field in the webhook body; alert qty supersedes ATM default | **NO** — CrossTrade documents relay of `qty`, not derivation from stop distance / lifecycle / DD | [Commands](https://crosstrade.io/docs/webhooks/commands) (`QTY` = any integer; required on PLACE); [Place Order](https://crosstrade.io/docs/webhooks/commands/place-order) | **PASS on qty-injection; FAIL as sole computation host** |
| **B. Same spine + NT8-side sizing host** (spec §4 ordered fallback) | YES — NT8 script emits / overrides before or via ATI; CrossTrade still carries `qty` if webhook path used, or NT8 places directly | **YES (by design)** — host reads alert fields + `lifecycle_state.json` + DD equity; runs §2 law; fail-safe = most-conservative tier if state unreadable | Spec §4 falsified-action (1); NT8 ATI is CrossTrade's documented delivery target | **PASS** — implementability path when A alone is insufficient |
| **C. TV → Tradovate native / CrossTrade `destination=tradovate`** | Place with `qty` supported on Tradovate destination (vendor) | Same gap as A unless an external host injects `qty` | Place Order "On Tradovate" note; envelope: Tradeify Tradovate API **LIVE-funded only** | **FAIL for eval** (API availability) + same computation-host gap |

**Current venue-edition state (blocks A as end-to-end today):** Phase 1b re-author applied D1–D5 constants ([`PHASE1B.md`](PHASE1B.md)) but **did not** land the spec's alert-payload contract. Venue `alert()` calls remain plain-text strings (no `{leg_id, signal_type, bar_time, close, stop_dist_pts}`); Pine still sizes at full `accountSize=100000` risk with **no** downstream haircut hook in the fired message. Spec §7 Phase 1 payload work is therefore still **owed** before any live qty path.

**§4 falsifier result:** the payload-computation route is **not** unimplementable — CrossTrade proves per-order `qty` injection, and the ordered NT8-side host (row B) is available on the selected spine. What is **not** supported is claiming "no hard rail blocker" without naming: (1) owed alert-payload fields on the venue editions, (2) an NT8 (or equivalent) computation host for the sizing law, (3) Pro-tier Account Manager for E1. Those are **implementation preconditions**, not missing connection hops.

---

## 3. Attended-operation posture (E6)

Envelope E6: attended automation on TV→CrossTrade→NT8 — **not** unattended 24h (Q-BTC-3 falsified lights-out).

### 3a. Who / when (from locked session calendars — DST-aware)

Pine gates entries with `hour(time, "UTC") >= 13 and < 17` (venue editions; LOCK sheets print the same UTC band). LOCK narrative "08–12 EST" is the **standard-time** wall-clock expression of that UTC band — it is **not** year-round ET.

| Season | UTC entry band | Wall clock (America/New_York) | Desk presence (entries + early adds) |
|---|---|---|---|
| **EDT (≈ Mar–Nov; current / go-live season)** | 13:00–17:00 UTC | **09:00–13:00 ET** | **09:00–13:15 ET** |
| **EST (≈ Nov–Mar)** | 13:00–17:00 UTC | **08:00–12:00 ET** | **08:00–12:15 ET** |

| Leg | Instrument | UTC entry (Pine / LOCK) | Active weekdays | Presence |
|---|---|---|---|---|
| Striker DJ30 → MYM | MYM | 13–17 UTC | **Tue, Fri** | per season table above |
| Striker NAS100 → MNQ | MNQ | 13–17 UTC | **Mon, Tue** | per season table above |

Sources: [`core/strategies/striker/LOCK.md`](../../../core/strategies/striker/LOCK.md), [`core/strategies/nas/LOCK.md`](../../../core/strategies/nas/LOCK.md); venue Pine `hour(time,"UTC")` gates (content-read). Prefer stating the window in **UTC** when scheduling; convert to ET only with the active offset.

**Combined attendance calendar (c1 book on one account) — use the seasonal presence row:**

| Day | Legs that can fire | Required presence |
|---|---|---|
| Mon | MNQ | seasonal window above |
| Tue | MYM + MNQ | seasonal window (highest concurrency) |
| Wed | — | No scheduled entry window; still check flat/idle if a holdover existed (should not under E1) |
| Thu | — | Same |
| Fri | MYM | seasonal window |
| **Every session with any open risk** | EOD | Operator **or** CrossTrade Account Manager (Pro+) flatten armed by **16:00 ET** (binding for MFFU 16:10) |

Pyramid adds can fire after the entry bar inside the same UTC session — presence through the seasonal end+15m covers the typical add window; trail/BE thereafter is alert-driven but still attended (operator reachable for desync / missed exit).

**Rev-1 defect closed:** the prior "08:00–12:15 ET" year-round print was wrong under EDT (desk on before fire; off 45m before entries can still print).

### 3b. Attended checklist (pre-session, every active day)

1. NT8 running; Tradovate connection green; CrossTrade Add-On connected.  
2. TV alerts armed (MYM and/or MNQ as per weekday); webhook URL + secret current.  
3. Rail-side sizing host armed: lifecycle + DD → qty into CrossTrade `PLACE` (spec §2) — **not** TV risk% alone.  
4. CrossTrade **Pro+** Account Manager: trailing-DD / optional DLL / **EOD flatten ≤16:00 ET** enabled for the live account.  
5. Operator phone/desktop notifications on for CrossTrade alert failures + NT8 disconnect.

### 3c. Multi-firm constraint

Tradeify FTA §6.6 exclusive-use clause (Phase 0): bots/algos for Tradeify must not be shared across firms. **Do not** run the same CrossTrade/TV bot concurrently on Tradeify + MFFU. Packet may score both tiers; live GO picks **one** first account.

---

## 4. Failure modes → manual-intervention protocol

| # | Failure | Detection | Immediate action | Resume rule |
|---|---|---|---|---|
| M1 | **Missed entry alert** (TV webhook fail, 2FA/webhook misconfig, CrossTrade reject, NT8 Add-On down) | No NT8 order when TV strategy shows entry; CrossTrade Alert History empty/error | **Do not chase** mid-bar. Log miss. Stay flat for that signal. Fix rail before next session. | Next valid session only after green connection test (Webhook Trader dry-fire OK) |
| M2 | **Missed exit / trail / BE alert** | TV flat or reduced; NT8 still in position (or vice versa) | Manual flatten **now** via NT8/Tradovate to match **intended** risk-off state. Prefer flat over reconstructing a trail. | Re-enable alerts only after Strategy Sync / position match confirmed |
| M3 | **Partial pyramid fill** (base filled, add rejected/partial; or qty floor left add at 0) | NT8 qty < intended stack; or add alert error | Treat as **strategy-incomplete expression**: flatten entire position if add is load-bearing for the edge thesis **or** hold base only if SL/BE still valid per Pine state — default for NAS100/MNQ (edge ~adds): **flatten** if add permanently failed. | Do not manually “complete” the pyramid at a worse price unless operator explicitly overrides |
| M4 | **TV↔NT desync** (Strategy Sync flags drift) | CrossTrade desync / unexpected NT qty | Auto-flatten if configured; else manual flatten to zero. Investigate before next entry. | Same as M2 |
| M5 | **EOD flatten miss** approaching 16:00 ET | Clock + open position | Manual flatten **immediately**; for MFFU, never send new orders after 16:10. Holiday half-days: operator owns flat (no firm auto-liq). | Account review if MFFU post-16:10 order risked |
| M6 | **Wrong Tradeify broker pipe** (Rithmic/TradeSea purchased) | NT8 cannot attach / no Tradovate creds | **Stop.** Do not improvise a Rithmic CrossTrade path for this packet. New account with Tradovate broker only after fresh GO. | N/A |
| M7 | **Firm / bridge outage** mid-session | Red connection; rejected orders | Flatten via any remaining working UI (Tradovate web). Halt automation for the day. | Resume next session after vendor green |
| M8 | **Sizing-host failure** (lifecycle/DD unread; computed qty missing; fail-open risk) | PLACE without computed `qty`, or host error | **Do not** fall through to TV full-size qty. Halt entries; flatten if a bad-size fill landed. | Resume only after host proves fail-safe (spec §6: absent state ⇒ most-conservative tier, never 1.0×) |

**Attended bar:** M1–M8 assume a human can act within minutes during the presence windows in §3. Overnight unattended hold is forbidden by E1 anyway.

---

## 5. Architecture verdict (Phase 3 only)

| Question | Answer |
|---|---|
| Documented end-to-end **connection** chain at Tradeify Select? | **YES** — TV→CrossTrade→NT8→Tradovate (primary docs 2026-07-17) |
| Documented end-to-end **connection** chain at MFFU Rapid? | **YES** — same spine (primary docs 2026-07-17) |
| Spec §4 bridge payload-qty screen | **PASS via row B** (CrossTrade injects `qty`; NT8-side host runs the sizing law). Row A alone is insufficient as computation host. |
| Hard **connection** blocker at either tier? | **None found** in firm/vendor hop documentation. |
| Hard **F1-realization / implementability** blockers still open? | **YES — named:** (1) venue editions still lack alert-payload contract fields; (2) NT8 (or equivalent) sizing-host not built; (3) E1 requires CrossTrade **Pro ($49/mo)+** Account Manager. These are preconditions for a GO packet, not missing Tradovate hops. |
| Checkout / config landmines | Tradeify must buy **Tradovate** broker; NT8 Account Type **Simulation** on eval; MFFU EOD **16:00 ET** hard; Tradeify exclusive-use blocks dual-firm same-bot; Tradovate-native alt blocked on eval API |
| Tier preference | Still **packet decides** (§8) — Phase 3 does not pick. Phase 4 compares cost + rule friction (MFFU 16:10 DISQUALIFY vs Tradeify softer auto-flat; exclusive-use; eval fees from Phase 0; **+$49/mo bridge floor**). |

**Forbidden moves honored:** no account opened, no CrossTrade/NT8 install, no `ACTIVE_FIRM` switch, no spend. Pine edits limited to prior Phase 1b venue work (gitignored) — payload contract still owed.

---

## 6. Phase 4 handoff (inputs this phase produced)

- Spine string + per-tier Tradovate connection steps.  
- Bridge cost floor for E1: **$49/mo Pro** (Account Manager), not $29 Standard.  
- Attended calendar: **UTC 13–17**; ET presence **09:00–13:15 (EDT)** / **08:00–12:15 (EST)**; Mon MNQ / Tue both / Fri MYM + daily 16:00 ET flatten.  
- Failure-mode protocol table incl. M8 sizing-host (annex-ready).  
- Spec §4 screen result + owed: alert-payload fields + NT8 sizing host.  
- Landmines: Tradovate-at-checkout; exclusive-use; Rapid DD geometry verify; MFFU post-16:10 DISQUALIFY; Tradovate API eval gap for native alt.
