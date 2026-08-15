# Q-RAIL-1 Phase 0 — deployment-fork re-verifies

**Date:** 2026-07-17  
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) §7 Phase 0  
**Scope:** re-fetch Tradeify FTA §6.6 + MFFU article 8444599 + both firms' 100K eval pricing (envelope §4 90-day / deployment-fork rule). No account registration, no rail build.

---

## 1. Automation posture (F5 input)

### Tradeify — FTA §6.6

| Field | Value |
|---|---|
| URL | https://tradeify.co/funded-trader-agreement |
| Fetched | 2026-07-17 (this session) |
| Doc stamp | "Last modified: May 2026" |
| Prior fetch | 2026-07-12 ([Q-AUTO-FIRM-1](../../../docs/ltm/briefs/Q-AUTO-FIRM-1-attended-automation-survey.md)) |

**§6.6 Automated Bots (verbatim substance, unchanged vs 07-12):** bots/algos permitted iff (1) sole ownership / no shared use, (2) exclusive use within Tradeify (not across multiple firms), (3) not HFT, (4) compliance/verification on request.

**Posture delta vs Q-AUTO-FIRM-1:** **NONE** on the attended-automation bar. Sole-owner + no-HFT still clear. The exclusive-use-across-firms clause remains load-bearing for any multi-firm packet (Phase 3/4), but is not a new ban on automation.

### MFFU — Fair Play article 8444599

| Field | Value |
|---|---|
| URL | https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices |
| Fetched | 2026-07-17 (this session) |
| Article stamp | November 24, 2025 |
| Prior fetch | 2026-07-12 (Q-AUTO-FIRM-1) |

**Section 1 Automated Trading Protocols (unchanged substance):** HFT not allowed; "Traders may make use of automated trading strategies tailored to their own specific settings" provided they do not exploit sim fills; live automated trading must abide by CME guidelines.

**Posture delta vs Q-AUTO-FIRM-1:** **NONE**.

**F5 score:** `PASS` at both discharge tiers — automation posture unchanged; no AMBIGUOUS escalation.

---

## 2. Eval pricing (Phase 4 cost-table input; not a F-limb)

| Tier | Primary source | Fetched | Price recorded | Notes |
|---|---|---|---|---|
| **Tradeify Select 100K** | https://tradeify.co/select-plan | 2026-07-17 | **$181** (displayed under 100K account-size picker) | Marketing page: "Evaluation price shown below. No hidden fees. No activation costs." Help-center pricing reference (`14369021`) returned **403** this session — list vs promo split not independently confirmable from help; Phase 4 should re-open checkout before ceiling sign-off. Secondary blogs still quote ~$259 list / ~$181 promo. |
| **MFFU Rapid 100K** | https://help.myfundedfutures.com/en/articles/11802636-traders-evaluation-simplified | 2026-07-17 ("Updated over a week ago") | **$267** (Price Eval / Reset row) | Marketing https://myfundedfutures.com/plans/rapid confirms $0 activation, Rapid 100K = 8 mini / 80 micro; page leads with promo "$79/mo starting" on the 50K sample — **use help-article $267 as the sourced Rapid 100K eval/reset figure**. |

**Activation fees:** both primary surfaces claim **$0** activation after pass (Tradeify select-plan; MFFU Rapid page + help article).

These figures feed Phase 4's cost table only. H-RAIL-1's cost clause stays **PENDING** until the operator sets a §8 ceiling against that table.

---

## 3. Session / EOD primary re-check (F4 input)

| Firm | URL | Fetched | Binding print | Delta vs envelope §4 (2026-07-13) |
|---|---|---|---|---|
| **MFFU** | https://help.myfundedfutures.com/en/articles/9558251-permitted-times-to-trade | 2026-07-17 (article stamp March 2, 2026) | Session 18:00 ET → **16:10 ET** auto-liq; post-16:10 orders can DISQUALIFY; holiday half-days NO auto-liq | **NONE** — still the binding minimum |
| **Tradeify** | https://help.tradeify.co/en/articles/10495876-rules-permitted-times-to-trade | 2026-07-17 | Intercom body did not render via fetch (TOC only) | **HOLD prior primary** from envelope §4: **16:59 ET** regular / 12:59 ET holiday-short, auto-flatten non-fatal. Re-open in Phase 3 if Tradeify is the recommended tier. |

E1 build target remains **16:00 ET** (≥10 min inside MFFU 16:10).

---

## 4. Tier-1 constants drift check (brief §10)

`core/firm_rules.py` tip still `a53ee99` (2026-07-13). Spot-checked this session:

| Field | Tradeify_Select_100K | MFFU_Rapid_100K |
|---|---|---|
| `max_dd_pct` | 3.0 | 3.0 |
| `micro_contract_cap` | 80 | 80 |
| `cost_per_side_usd` | 0.91 | 0.95 |
| `consistency_rule_pct` | 40.0 | 50.0 |

No drift vs brief §0.

---

## 5. Phase 0 verdict

| Check | Result |
|---|---|
| Automation posture both tiers | **UNCHANGED → F5 PASS** |
| Eval pricing sourced | **YES** (Tradeify $181 displayed; MFFU $267 help) — Phase 4 input |
| EOD binding minimum | **MFFU 16:10 ET re-confirmed** |
| Immediate AMBIGUOUS escalation? | **NO** |

Proceed to Phase 2 F-scoring (F2–F4) and Phase 1 inventory (MNQ pine still missing — see F-scorecard).
