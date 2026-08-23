# T3 surrogate calibration note (additive; no IID default swap)

**Date:** 2026-08-23
**Owner:** [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T3
**Module:** [`lab/research_utils/breadth.py`](../../../lab/research_utils/breadth.py)

No new `lab/analysis/` slug (catalog grep empty; extend existing owner).

| Item | Value |
|---|---|
| Default null | `iid_gaussian` (unchanged) |
| Additive null | `garch_fitted` (explicit `kind=` only) |
| Nominal FPR | 0.05 |
| Pre-registered band | `[0.01, 0.15]` |
| Pin | `tests/test_breadth_t3.py::test_surrogate_fpr_iid_inside_preregistered_band` |

ENB + downside-corr + `marginal_admission_delta` live on the same module. Corpus-FDR IID-Gaussian default is **not** swapped.
