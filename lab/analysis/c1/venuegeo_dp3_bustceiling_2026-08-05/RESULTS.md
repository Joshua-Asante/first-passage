**Theme:** c1
# Q-VENUEGEO-1 DP3 (bust-ceiling half) — Bulenox / MFFU / BluSky, instrumented vs bare

> ⚠ **2026-08-09 reader-intercept (W1 successor):** bust figures below are **EOD-clock** (instrumented inactivity-off arms from prior F3 cadence output). Class-S 0.50× full+halves on the **intraday-honest** clock now live at [`../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md`](../class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) — do not read this DP3 table as the honest-clock §4 geometry. Frozen body unedited.

**Status:** ACTIVE — bust-ceiling half of DP3 measured; EV/$ half (pass-EV per eval-dollar) NOT run — each firm's evaluation-purchase price is unsourced. This does not close H-VENUEGEO-1, which requires both limbs.
**Date:** 2026-08-05. **Trigger:** `Q-VENUEGEO-1` DP3 ("pass-EV per eval-dollar ranking at the frozen gate"), after DP2's compliance-instrument-legality sweep found Bulenox facially open and BluSky a gray zone for the token-trade rescue.
**Scope:** measurement only, reusing already-committed simulation output. **$0 spent, K=0, no manifest, no `core/` / Pine / allocation / `dd_protection` / lifecycle / rail change.**
**Harness:** [`extract_dp3.py`](extract_dp3.py) (no new simulation — reads two existing committed artifacts). **Raw:** [`dp3_bustceiling.json`](dp3_bustceiling.json).

---

## §0 — Data-staleness trap caught before use

`f3_cadence.json`'s **BluSky rows are stale** — they reflect the superseded `inactivity_max_idle_days: 30` encoding (ADR 2026-08-05, discharged same day by ADR 2026-08-05b's unit correction to 22). The corrected BluSky bare-book figures live in a separate, sibling artifact (`blusky_unit_sensitivity.json`), which the original F3 cadence study committed but did not fold back into the main JSON (by design — Trap #12, the parent RESULTS body is never edited in place). A DP3 pass that read `f3_cadence.json`'s BluSky rows directly would have compared Bulenox/MFFU against BluSky's **wrong** (10× too optimistic) bare-book number. Caught here by cross-checking both files before computing anything.

The **instrumented (token-trade / inactivity-fully-disabled) arm is unaffected by this staleness** — it bypasses the `inactivity_limit` field entirely regardless of its value, so Bulenox's and BluSky's OFF arms are numerically identical (`firm_kwargs` differ only in `inactivity_max_idle_days`, per RESULTS.md finding #2) and independent of which idle threshold is on record. The extraction script asserts this identity as a sanity check rather than assuming it.

---

## §1 — Headline table (deployed rung: C2-on / 0.50× — WATCH-1, the only regime-admissible rung)

1.00× is excluded as a comparison point — it **fails** the both-halves regime-robustness gate (`ADR 2026-07-23-c1-rung-selection-ev-objective` §2, citing the operator-signed `class_s_c1_haircut_regime_remc` result: H1 bust 4.37%, bootstrap-95th 10.37%, both > 3.0%) and is therefore not a legitimate rung at any firm.

| Firm | Instrumented total bust (token trade) | Clears 3.0%? | Bare total bust (no instrument) | Clears 3.0%? |
|---|---:|:---:|---:|:---:|
| Bulenox_100K | **2.96%** | YES | 97.54% | NO |
| MFFU_Rapid_100K | **3.54%** | **NO** | 97.54% | NO |
| BluSky_Premium_100K | **2.96%** | YES | 15.48% (corrected) | NO |

(Instrumented = `inactivity_off=True`, i.e. the barrier fully disabled — the seed-target-spec's own documented proxy for "what the R8 maintenance-trade instrument would deliver." Bare = the firm's real, sourced idle rule active, no mitigation.)

---

## §2 — Findings

1. **Instrumented, Bulenox and BluSky are statistically tied — and both sit inside simulation noise of the ceiling, not clearly under it.** 2.96% vs a 3.0% ceiling is a 0.04pp gap. At 10,000 sims × 3 seeds = 30,000 paths/arm (`core/mc/modes.py` `SIMS_PER_SEED`/`SEEDS`), the binomial standard error at p≈0.03 is ≈0.099pp, so a 95% CI is roughly ±0.19pp — **the 0.04pp margin is well within one standard error of the ceiling itself.** This is not a confident PASS; it is "statistically indistinguishable from the ceiling, pending a higher-precision re-run before any registration decision leans on it."

2. **MFFU fails the bust-ceiling instrumented, on DD geometry alone — independent of the entire token-trade question.** 3.54% > 3.0% even with inactivity fully disabled. Combined with DP2's confirmed CME 2%-price-limit finding (naming MNQ/MYM directly) and MFFU's discretionary-only token-trade legal read, MFFU now fails on two independent axes and is the weakest of the three candidates on current evidence — a genuinely different conclusion from the STATE.md board's current framing (which groups Bulenox and MFFU together as "ELIMINATED" for the same reason). **They are not eliminated for the same reason.** Bulenox's elimination reads on an untested instrument; MFFU's stands on its own DD geometry regardless of the instrument.

3. **The token-trade instrument is entirely load-bearing for all three firms.** Without it, Bulenox/MFFU bust 97.54% (catastrophic) and even BluSky — the firm whose cadence rule is loosest — busts 15.48% (still well over the 3.0% ceiling). No firm is viable on the bare book.

4. **This does not close H-VENUEGEO-1.** The gate requires bust ≤ ceiling **AND** pass-EV per eval-dollar ≥ a floor set at freeze. Only the first limb is measured here; the second needs each firm's evaluation-account purchase price (Tradeify's is pinned at $328/$258-promo per Q-RAIL-1 Phase 4 — no equivalent figure has been sourced for Bulenox/MFFU/BluSky in this or any prior pass).

---

## §3 — What this does NOT license

- **No registration, ranking, or successor election.** F3 remains operator-owned, dated 2026-08-08.
- **No re-opening of ADR 2026-08-05/05b** — those measured the bare-book cadence axis correctly for what they were asked; this note only extracts their already-published output for a different, complementary question (the instrumented comparison).
- **No claim that Bulenox or BluSky "passes."** 2.96% is inside the ceiling's own noise band — read as "not yet distinguishable from failing," not as a clearance.
- **No EV/$ ranking** — that half of DP3 is unrun; see §4.
- **No `firm_rules.py` change** — this is a read-only re-derivation of existing committed simulation output.

---

## §4 — What would close DP3 / H-VENUEGEO-1

1. **Higher-precision re-run of the instrumented arm at Bulenox/BluSky's shared geometry** — more seeds/sims to narrow the CI below the 0.04pp margin, so "clears the ceiling" becomes a real statistical claim rather than a coin flip against noise.
2. **Source each firm's $100K evaluation-account purchase price** (Bulenox, MFFU, BluSky — primary sources, same Rule-13 discipline as DP2) to compute pass-EV per eval-dollar and close H-VENUEGEO-1's second limb.
3. **DP2's remaining open item** — the 2 non-public Bulenox documents (individually-issued Master Agreement, Rithmic's platform agreement) that could still bar the token trade — stays a caveat on Bulenox's otherwise-clean legal read.

---

## §5 — Reproduction

```bash
python lab/analysis/c1/venuegeo_dp3_bustceiling_2026-08-05/extract_dp3.py
# Sanity check must print "OK" (BluSky OFF-arm == Bulenox OFF-arm) before trusting output.
```
