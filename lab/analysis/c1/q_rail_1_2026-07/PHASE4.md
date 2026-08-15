# Q-RAIL-1 Phase 4 — GO/NO-GO packet (cost table + §8 ceiling re-request)

**Date:** 2026-07-17
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) §7 Phase 4
**Inputs:** [`PHASE0.md`](PHASE0.md) (ToS + eval pricing) · [`PHASE3.md`](PHASE3.md) (spine, bridge floor, attendance, failure modes) · [`F_SCORECARD.md`](F_SCORECARD.md) · haircut re-MC [`RESULTS.md`](../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md)
**§10 audit hooks re-run this session:** gating language intact (G8_INTAKE "separately gated"; self-funded ADR §5 line present); `core/firm_rules.py` tip still `a53ee99` (2026-07-13), tier constants unchanged; MNQ edition pinned `a67fd3b4…` in PORT_MANIFEST; zero rail artifacts in git history.
**Scope honored:** no account registration, no CrossTrade/NT8 wiring, no spend, no Pine edits. This packet prepares the GO decision; it does not make it (brief `Loop` line + self-funded-close ADR §5).

---

## 1. F-scorecard (final)

| F1 — WATCH-1 injection | F2 — integer sizing | F3 — deployable expression | F4 — session/EOD | F5 — ToS |
|---|---|---|---|---|
| **PASS-via-fallback** (multiplier layer; [Q-PYRPARITY-1 closure](../../../docs/briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md)) | **PASS** (floors MYM $8,689 / MNQ $59,039 < $100K; adds survive) | **PASS** (Step-2 parity + C3 1a→1c; MYM 1b 72.6% short-window caveat carried) | **PASS** (16:00 ET build target inside MFFU 16:10) | **PASS** (posture unchanged both firms, fetched 2026-07-17) |

H-RAIL-1's fidelity limb is fully satisfied at **both** discharge tiers. Only the cost clause (PENDING per §4) remains.

## 2. Cost table (all sources fetched 2026-07-17 unless noted)

### 2a. Shared monthly run-rate (both tiers)

| Item | Monthly | Source / note |
|---|---|---|
| CrossTrade **Pro** (Account Manager required for E1 auto-flatten — Standard $29 lacks it) | **$49** | [crosstrade.io/pricing](https://crosstrade.io/pricing) FAQ; 7-day trial first |
| NinjaTrader 8.1+ desktop | **$0** | CrossTrade prop-firm connection guide: "No license key required for most prop firm connections" |
| CME market data on eval | **$0 expected — UNVERIFIED** | Provisioned via firm Tradovate creds + data-agreement signature (Tradeify guide 12268716 / CrossTrade guide); **no fee printed on any firm surface**; re-verify at wiring — this is the one unpriced-risk row |
| TradingView (webhook alerts need any paid tier) | **$0 incremental** | Already-held workspace subscription; no new spend attributed |
| **Run-rate total** | **$49/mo** | |

### 2b. Per-tier

| Item | Tradeify_Select_100K | MFFU_Rapid_100K |
|---|---|---|
| Eval fee (100K) | **$181 list · $111 promo** (code JULY, through 2026-07-31; select-plan page re-opened this session, discharging Phase 0's list-vs-promo caveat) | **$267** (help 11802636; = reset price) |
| Activation after pass | **$0** — waived across plans. (An earlier fetch misparsed "$1,500/$4,000 activation" — those are the 100K **payout caps**: Daily $1,500 / Flex $4,000. Verify at checkout regardless.) | **$0** ("absolutely no activation fees") |
| Reset (contingency, not in base) | $239 | $267 |
| Commission model | $0.91/side → $1.82/RT/micro (engine constant; already inside the re-MC via `cost_per_side_usd`) | $0.95/side → $1.90/RT (matches firm fee table 9735811) |
| **Cost-to-first-live-fill (§8 scope: eval + 3 mo run-rate)** | **$328 list / $258 promo** | **$414** |
| + one reset contingency | $567 / $497 | $681 |

**Worst-case across both tiers incl. one reset: $681.** First fills occur during the eval (Account Type = Simulation on the NT8 connection), so funded-path economics (Tradeify 90/10 split, payout caps) sit outside the §8 scope and are context only.

### 2c. WATCH-1 practicality restated (must-read next to the cost)

At 0.50× the book's per-day return halves: **median days-to-pass roughly doubles**; pass **rate** stays ≥95% within the 1500-day horizon (re-MC pass-5th **95.76%**; median not surfaced by `summarize_outcomes` — documented §8 Phase-0 deviation, non-gating). Practical consequence: if the eval runs past 3 months, each extra month adds $49 bridge run-rate; the §8 ceiling scope stays eval + 3 months by definition.

## 3. Standing risk framing (operator must see next to any GO)

- **Q-DECAY-1:** common-mode edge death is *uncovered* — no family-level monitor exists; detection is by drawdown only, after a ~bust-line loss.
- **Q-PERSIST-1:** +0.46pp MC bust optimism on the decompounded basis.
- **Regime-conditionality:** at 1.00× this book **failed** the regime gate; the H1 rescue is the haircut's doing (0.50× arm: H1 bust 0.14%, bootstrap-95th 0.77%). WATCH-1 is load-bearing, not a courtesy discount.
- **Return language:** the Class-S claim is bust-geometry survival, **not** CFD-edge preservation — this packet promises pass/bust odds, never P&L.
- **MYM Step-2 parity override (added 2026-07-18, post-GO):** F3's MYM per-candle parity limb is `PASS-via-operator-override`, re-affirmed 2026-07-18 against a corrected exit-lag census — **9 lagged exits, not the 3 originally documented; max lag +10 bars (2.5h)**, not the original "1–3 bars" bound. Entry-cascade mechanism and lag-absorption both re-affirmed as-is; full census + operator quote at [`STEP2_PARITY.md`](STEP2_PARITY.md). This correction post-dates the 2026-07-17 GO ADR — see that ADR's Addendum. Discharging same-size control remains the pre-registered, still-open revisit condition; binds before B6 dry-fire leans on MYM CME-native timing precision.

## 4. Build preconditions on GO (priced/named; not blockers to the decision)

1. **Alert-payload contract** fields on both venue editions (spec §2: `{leg_id, signal_type, bar_time, close, stop_dist_pts}`) — Pine work, gitignored, hash re-pin owed.
2. **NT8-side sizing host** (account × lifecycle × DD → integer qty; fail-safe = most-conservative tier) — spec §4 row B.
3. **CrossTrade Pro** subscription + Account Manager EOD flatten ≤16:00 ET armed.
4. **Checkout landmine (M6):** Tradeify purchase must select **Tradovate** broker or the rail cannot attach.
5. Attended calendar per PHASE3 §3 (EDT: 09:00–13:15 ET; Mon MNQ / Tue both / Fri MYM + EOD).

## 5. Tier recommendation (packet decides, per §8 ratification)

**Primary: `Tradeify_Select_100K`. Fallback: `MFFU_Rapid_100K`.**

| Axis | Tradeify Select | MFFU Rapid | Reads |
|---|---|---|---|
| All-in to first fill | $328 ($258 promo) | $414 | Tradeify −$86 to −$156 |
| EOD failure mode | 16:59 ET auto-flatten, **non-fatal** | 16:10 ET auto-liq; post-16:10 orders can **DISQUALIFY** | Tradeify materially softer on the M5 failure mode |
| Consistency rule | 40% — stricter, but **eval-only soft at-pass gate, none funded** (`firm_rules.py` comment) | 50% | MFFU looser; Tradeify's is soft ⇒ delay-not-death on a pyramid-concentrated win day |
| Automation ToS | Sole-owner bots OK; **exclusive-use within Tradeify** | Own-settings automation OK; news trading allowed | Exclusive-use is moot for a single-account GO; blocks a future dual-firm same-bot only |
| Re-MC floor | PASS (0.50× arm) | PASS (0.50× arm) | Tie |
| Min trading days | 3 | 2 | Negligible at ~2× median pass time |

Both tiers clear every F-limb; the recommendation is cost + failure-mode softness. Nothing in it forecloses MFFU later — Tradeify's exclusive-use clause only binds once a Tradeify bot exists.

## 6. §8 ceiling re-request (the one fresh operator number)

Per the frozen §8 mechanism, the operator is now asked to **set (or decline) a budget ceiling** for all-in cost-to-first-live-fill against table §2. Decision aids:

- **$414** covers either tier at list, no resets.
- **$681** covers the worst tier + one reset.
- Recommended-tier base case is **$328** ($258 if purchased before 2026-07-31).

On a ceiling ≥ the chosen tier's base case → H-RAIL-1 cost clause **ACCEPTS** → §6 `RESOLVED` (decision-ready packet) → the rail-build/account GO itself remains a separate fresh operator decision + ADR (this packet is the input to that decision, not the decision).
On a ceiling below $328/$258 at both tiers → cost-`FALSIFIED` (cheap re-open class, per §6).
No ceiling set → `AMBIGUOUS-HOLD` carried to the 08-08 packet as "cost table ready, awaiting operator ceiling."

**CEILING SIGNED (2026-07-17, same session):** operator set **$700** via `AskUserQuestion` against this table — clears both tiers plus one reset ($681 worst case). Cost clause **ACCEPTS at both tiers** → §6 fires `RESOLVED`; closure at [`docs/briefs/closures/Q-RAIL-1-closure-resolved.md`](../../../docs/briefs/closures/Q-RAIL-1-closure-resolved.md).
