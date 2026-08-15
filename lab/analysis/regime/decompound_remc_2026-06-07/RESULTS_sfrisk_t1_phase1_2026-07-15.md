# Q-SFRISK-1 Phase 1 — T1 numeric report (report-only)

**Generated:** 2026-07-15
**Triple:** T1 = F1 + F3 (ADOPT +5%/$200K banded) + F4; F2 deferred
**Panel:** clean single-file 2026-06-25 vintage (`remc_cleanvintage.NEW_FILES`)
**F4 scale:** n_paths=30000, seed=20260607

Verdict deferred to Phase 2 (CC/operator) — numeric report only.

---

## F1 — per-half p99 max-DD (LOCKED k=1.0, static decompounded panel)

Phase-2 bar (context only, not applied here): p99 max-DD ≤ 10% per regime half.

| partition | window | n_bd | pass | bust | p99 DD | med days-to-pass |
|---|---|---:|---:|---:|---:|---:|
| H1 | 2020-01-06→2023-03-29 | 843 | 86.16% | 13.84% | 8.00% | 62 |
| H2 | 2023-03-30→2026-06-23 | 844 | 99.79% | 0.21% | 4.53% | 20 |

Reproduction target (`RESULTS_cleanvintage_2026-06-25.md` LOCKED row): H1 p99 7.76% / H2 p99 4.53%.

---

## F4 — median business-days-to-first-$210K-skim (banded panel)

Phase-2 bar (context only, not applied here): median days-to-first-skim > 252 bd ⇒ IMPRACTICAL.

Full panel n_bd=1687.

| partition | median_bd | censoring_rate | n_paths | horizon_bd | seed |
|---|---:|---:|---:|---:|---:|
| H1 | 51.0 | 0.3% | 30000 | 843 | 20260607 |
| H2 | 16.0 | 0.0% | 30000 | 844 | 20260607 |
| pooled | 26.0 | 0.0% | 30000 | 1687 | 20260607 |

---

## Notes

- No partition reached ≥50% censoring.
