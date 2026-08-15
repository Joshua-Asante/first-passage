# INSTRUMENT LEDGER — EURGBP

**Symbol:** EURGBP (euro / sterling G10 cross) · **Tradable:** DXTrade (FXIFY) · **Asset class:** FX major cross · **DXTrade contractValue:** unverified (default 1 expected, as Aegis USDJPY — broker-verify before any order)
**Canonical feed (if ever built):** TV CSV export per [`docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md`](../../docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md). **No panel has been exported — nothing has been run on EURGBP.**
**Status:** **NO LIVE CONCEPT.** One registry rejection (Aegis-v4.3 mean-reversion template port, **refuted pre-build at 5th-leg adversarial review 2026-06-21** on the EDGE & COST angle). Not in the live book; no backtest run.
**Last updated:** 2026-06-21 (stub created to record the refutation — see Session log).

**Purpose:** Single source of instrument-level truth. Any session deriving, testing, tuning, or adjudicating on EURGBP MUST read this file at session start and append a dated disposition at session end (operational rule 10, ratified 2026-06-11 — see [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created 2026-06-21 as a **stub** — the first session to adjudicate an EURGBP direction (an Aegis-port proposal, refuted), not a pre-emptive backfill (ADR §5). Canonical path: `ops/instruments/EURGBP.md`.

**Ownership boundary (operational rules 5/7):** this ledger owns instrument-level findings, concept status, and the shared anti-SNAG budget. Strategy parameters stay canonical in Pine source; locked-risk constants in `dd_protection.py` / `firm_rules.py`. The ledger links out, never restates.

## PROFILE (machine-readable)

```yaml
symbol: EURGBP
asset_class: fx-cross
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: mean-reversion-fade
    verdict: DEAD
    date: 2026-06-21
    source: "#D1"
structure:
  - claim: "EURGBP is the lowest-volatility G10 cross (ATR(14) ~6 pips) — any ATR-scaled-stop mean-reversion transfer from a wider-ATR pair fails the USDCAD cost law (cost-in-R >= 0.097R) by construction, before any panel is run."
    source: "#F1"
  - claim: "EURGBP did not cleanly range through the 2020-2023 H1 window — the 2022 sterling crisis (~0.82->0.90, spike to ~0.923) is the strong-trend sub-regime where mean-reversion bleeds."
    source: "#F3"
```

---

## DURABLE FINDINGS (instrument characterization)

> All three findings were established at the 2026-06-21 adversarial review by argument + cross-instrument precedent; **no EURGBP panel has been exported or run.** They are the *refutation basis*, recorded so a future session does not re-derive them. Confidence is "argument/precedent," not "measured on an EURGBP panel."

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **F1** | **Cost geometry fails the cost-law pre-flight.** EURGBP is the **lowest-volatility G10 cross** (ATR(14) ~6 pips; 15m ATR only a few pips), so an Aegis **1.42×ATR(15m)** stop is **smaller in price** than the USDCAD reference while spread is comparable (~0.6–1 pip + commission on DXTrade/prop). By the USDCAD **COST LAW** (cost-in-R ∝ price/stop_dist), cost/R **≥ 0.097R** — likely worse. USDCAD measured **0.097R round-trip at exactly 1.42×ATR(15m)** and already **failed a 4×-cost-hurdle gate**. An after-cost PF≈2.0 is not credible. | [`ops/instruments/USDCAD.md`](USDCAD.md) durable finding #1 (0.097R RT @ 1.42×ATR); Aegis SL = 1.42×ATR ([`docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md`](../../docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md):214). | **MODERATE-HIGH** (the cost-law is feed-robust; the EURGBP ATR figure is a characterization estimate, not a panel measurement). |
| **F2** | **The exact port is already dead on a comparable cross.** Aegis USDCAD v0.1 (mean-reversion transfer) FAILED: **n=245, PF 0.756**, loss character = pervasive trend-impulse, no hour/day/regime refuge. The same proven-mechanism / new-FX-instrument port died **far below the PF≈2.0 bar** on a comparable G10 cross. | [`ops/instruments/USDCAD.md`](USDCAD.md) dead-list. | **HIGH** (direct precedent, on disk). |
| **F3** | **The "edge persists in chop" claim fails on the H1 window that must be survived.** The 2020–2023 half contains the **2022 sterling crisis** — a sustained multi-month directional EURGBP move (~0.82 → ~0.90, mini-budget intraday spike to ~0.923 on 26 Sep 2022). That is the strong-trend sub-regime where mean-reversion bleeds; our own Aegis/USDJPY had 2022 PF only ≈1.12. EURGBP did **not** cleanly range through H1. | 2026-06-21 review (historical EURGBP path + Aegis/USDJPY 2022 per-year read). | **MODERATE** (argument/precedent; the EURGBP path is historical fact, the Aegis/USDJPY 2022 PF was not independently re-measured in this stub). |

**Net read (durable):** an Aegis-style 15m Bollinger mean-reversion template port to EURGBP is refuted on **EDGE & COST** before any panel is worth exporting. The binding constraint is the cost law (F1); the direct precedent (F2) and the H1 trend regime (F3) corroborate.

---

## DEAD / REJECTED (instrument-specific)

| # | Rejection | Class | Discriminator that fired | Source |
|---|---|---|---|---|
| **D1** | **Aegis-v4.3 mean-reversion template port to EURGBP** (Bollinger 19/1.9 + ATR19 + break-even, long-only, 15m) | venue/cost-constraint (primary) + edge-failure (secondary) | **REFUTED pre-build at 5th-leg adversarial review 2026-06-21** on the EDGE & COST angle. Cost geometry ≥ 0.097R/R (lowest-vol G10 cross, 1.42×ATR stop smaller than USDCAD, comparable spread) → after-cost PF≈2.0 not credible (F1); direct precedent Aegis USDCAD v0.1 dead (n=245, PF 0.756) (F2); MR bleeds through the 2022 sterling-crisis trend in the H1 window (F3). No EURGBP panel run. | This ledger; [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md); [`ops/instruments/USDCAD.md`](USDCAD.md) durable #1 + dead-list. |

---

## ANTI-SNAG LEDGER (shared budget — all sessions count)

**EURGBP mean-reversion family — zero concept-runs consumed.** D1 was **refuted at adversarial review, pre-build** — no intake, no codification, no panel export, no harness run. It is a reasoned rejection, not a null backtest, so it consumes **0 of the anti-SNAG budget**. There is no active EURGBP direction. A re-proposal must bring **new mechanism evidence** — a measured spread/ATR geometry that clears the cost hurdle on the canonical feed — **not** new params or a longer panel (see the `docs/rejected_candidates.md` re-proposal bar).

---

## Session log (append-only)

- 2026-06-21 / 5th-leg adversarial review (EDGE & COST angle): EURGBP-as-Aegis-v4.3-MR-port reviewed and **REFUTED pre-build**. Ledger stub created; D1 recorded; `docs/rejected_candidates.md` entry added. Refutation basis verified on disk: USDCAD durable finding #1 (0.097R RT @ 1.42×ATR), USDCAD dead-list (Aegis USDCAD v0.1 PF 0.756), Aegis SL = 1.42×ATR (`docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md:214`). No `core/` touch, no `.pine` touch, no lock/allocation change; **0 anti-SNAG slots consumed**.
