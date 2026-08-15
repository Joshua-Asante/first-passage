# Stage-2 — Aegis-6J solo Part A (H-SOLO) RESULTS

**Verdict:** `FALSIFIED`
**Date:** 2026-07-16
**Winner (v2.1):** c05 — cap8 / 0.40% / 16:00 / panel `ED91CD2D` (native $100K, decompound-to-static; no re-scale).
**Engine:** Run-2; seeds [42, 123, 2026]; 10000×3; horizon 1500; dd_protection OFF; inactivity off; `summarize_outcomes`. `ACTIVE_FIRM=FXIFY` fixture untouched.

## Citations
- v2.2 (1R re-spec + Stage-2 re-run auth): [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md)
- v2.1 winner: [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md)
- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
- Panel construction: [`HANDOFF.md`](HANDOFF.md) §1 (native, no re-scale)

## H-SOLO surface (both required)
- **Tradeify_Select_100K**: Part A FAIL (bust 0.0641 ≤ 0.03, pass 0.9327 ≥ 0.5; gated_on=run2)
- **MFFU_Rapid_100K**: Part A FAIL (bust 0.0641 ≤ 0.03, pass 0.9327 ≥ 0.5; gated_on=run2)

## Panel
- n_trades 128 · span 2022-01-12->2026-06-22 · overnight 0 · envelope YES · net_static $13,736 · 1R(median) $87 (full-stops=0; 1R diagnostic-only per v2.2 §2.7′)

## Prior-look (best-of-K)
v1 Stage-1 FALSIFIED (N≥80 unreachable) → v2 realign 12/12 clear (a)–(e), AMBIGUOUS (c05≡c06) → v2.1 tie-break → c05 → Stage-2 `NEEDS_CONTEXT` (full-stop 1R FALLBACK; `1ababcf`) → v2.2 native-path 1R re-spec (option c; guard-drop cannot bias MC — 1R not a scoring input). All 12 Stage-1 cells + degeneracies disclosed in v2/v2.1 §7; s2/gd in v2.2 §7.

```json
{
  "verdict": "FALSIFIED",
  "hsolo_part_a": {
    "Tradeify_Select_100K": false,
    "MFFU_Rapid_100K": false
  },
  "tiers": {
    "Tradeify_Select_100K": {
      "clears_part_a": false,
      "clears_funded": false,
      "gated_on": "run2",
      "run2": {
        "headline_bust": 0.0641,
        "pass_rate": 0.9327,
        "rates": {
          "pass": 0.9327,
          "bust_daily": 0.0,
          "bust_static": 0.0,
          "bust_trailing": 0.0641,
          "bust_inactivity": 0.0,
          "horizon_cap": 0.0032
        }
      }
    },
    "MFFU_Rapid_100K": {
      "clears_part_a": false,
      "clears_funded": false,
      "gated_on": "run2",
      "run2": {
        "headline_bust": 0.0641,
        "pass_rate": 0.9327,
        "rates": {
          "pass": 0.9327,
          "bust_daily": 0.0,
          "bust_static": 0.0,
          "bust_trailing": 0.0641,
          "bust_inactivity": 0.0,
          "horizon_cap": 0.0032
        }
      }
    }
  },
  "r_pin": {
    "basis": "median (native-path diagnostic; v2.2 \u00a72.7')",
    "gating": false,
    "median_r_dollars": 86.73593074363455,
    "median_n": 82,
    "full_stop_attempt": {
      "method": "median loss (FALLBACK \u2014 zero full stops)",
      "n_full_stops": 0,
      "dollars": 86.73593074363455
    }
  },
  "panel_meta": {
    "panel_file": "c05_fill1600_cap8_r40_ed91cd2d.csv",
    "sha256_lf": "ED91CD2D5D4075086F3571561AC7F88CE5F36D416E3B088AB4D112050C25C851",
    "detected_band": 100000,
    "static_base": 100000.0,
    "n_trades": 128,
    "panel_window": "2022-01-12->2026-06-30",
    "span": "2022-01-12->2026-06-22",
    "n_bdays": 1159,
    "overnight_holds": 0,
    "net_static": 13736.158365229921,
    "gross_pos": 26863.675095435618,
    "n_losers": 82,
    "max_static_loss": 631.5593041767667,
    "full_stop_threshold_1pct": 1000.0,
    "n_full_stops_1pct": 0
  }
}
```

