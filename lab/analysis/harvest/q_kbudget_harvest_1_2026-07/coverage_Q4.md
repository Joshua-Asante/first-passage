# Coverage log — Q4 (FX-futures microstructure timing 6E / 6J)

**Query family:** FX-futures microstructure timing (6E / 6J) with extractable δ
**Target families:** 6E, 6J (note M6J absent at FRIENDLY firms)
**Search date:** 2026-07-16
**Queries used:**
1. `currency futures microstructure timing momentum carry 6E 6J yen euro futures empirical study`

| Source | Venue / year | Examined | Economic grounding (1a/1b) | Four-field outcome |
|---|---|---|---|---|
| Menkhoff, Sarno, Schmeling & Schrimpf — "Currency momentum strategies" | *JFE* 2012 | PDF abstract/body skim | 1b-capable (momentum) | `EXCLUDE:spot-FX-cross-section-not-6E/6J-futures-cohort` — no CME 6E/6J per-contract δ |
| Breedon, Ranaldo et al. / Ranaldo — "Foreign Exchange Order Flow as a Risk Factor" | NBER w27199 → *JFQA* | abstract | 1a — order-flow risk | `EXCLUDE:spot-FX-order-flow-not-CME-futures-δ` |
| Fang & Liu / carry-momentum IRV | *JFQA*-class | abstract | intermediary IRV | `EXCLUDE:spot-portfolio-not-6E/6J-futures-δ` |
| Bundesbank DP — EUR futures speculative positions | working 2015 | abstract | efficiency / COT | `EXCLUDE:no-extractable-tradeable-δ` (efficiency test, not effect prior) |
| D7 / HARV class-analogue on 6J month-end | in-house | — | — | `EXCLUDE:already-D7` (E.1) |

**New rows from Q4:** none. Binding gap remains **per-contract CME 6E/6J cohort δ** (same class of missing input that left D7 on a class-analogue).
