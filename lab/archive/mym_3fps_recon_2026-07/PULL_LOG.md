# MYM-3FPS-1 pull and diagnostic log

## Data acquisition

- Request: `MYM.v.0`, `continuous`, `ohlcv-1m`, 2019-05-06 inclusive to 2026-07-21 exclusive.
- Campaign/era: `mym-3fps-1` / `oos`.
- Pre-pull estimate: **$0.0000**, 2,470,697 records, 138,359,032 billable bytes.
- Pull result: **$0.0000**, 2,470,697 rows.
- Local cache: `/home/ubuntu/.databento_cache/ohlcv-1m_continuous_0011b43a03e3f21a.dbn`.
- Vendor condition warning: 2020-02-27, 2020-02-28, and 2020-06-30 degraded. None is a third-Friday event checkpoint.

The initial July 22 exclusive request was rejected by the metadata range gate before any pull. It was narrowed and re-frozen at July 21 exclusive; the 87-event calendar was unchanged because its latest event is July 17.

## Coverage diagnostic

Exact checkpoints existed for 84/87 events. Missing:

- 2022-04-15 — Good Friday closure.
- 2025-04-18 — Good Friday closure.
- 2025-06-20 — no complete exact-checkpoint triplet after the June 19 holiday.

Coverage therefore clears the frozen 90% gate; no nearest-bar substitutions were made.

## Non-gating year diagnostic

| Year | N | Overnight spike bp | Open-to-noon short bp |
|---|---:|---:|---:|
| 2019 | 8 | +11.82 | -16.86 |
| 2020 | 12 | +39.68 | +32.07 |
| 2021 | 12 | -7.95 | +9.63 |
| 2022 | 11 | -5.02 | +11.37 |
| 2023 | 12 | -8.68 | +11.30 |
| 2024 | 12 | -11.56 | -12.41 |
| 2025 | 10 | +8.78 | -5.66 |
| 2026 | 7 | -19.42 | -27.97 |

Signs are unstable and the newest three years are adverse on the tradable short limb. This diagnostic cannot alter the frozen aggregate verdict.
