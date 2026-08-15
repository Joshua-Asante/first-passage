# Formal regime-robustness gate — Guardian-removal candidates (REF / D1 / D3)

**LoR:** OUTER (INQHIORI). Mandatory gate (`docs/methodology/regime_robustness_gate.md`) on the
reallocation candidates, on the canonical **decompounded-static Pepperstone** basis (single-feed —
directly comparable to PR #157's rejected C1/C2; removes the off-feed-Striker confound). Locked config
untouched. 2026-06-15.

**Floor** (Phase-4 amendment — the two lock gates in EACH partition): bust < 1% AND p99 DD < 5%,
applied to {6-mo-block bootstrap 95th-pct, H1 2020-2023, H2 2023-2026}. Pass IFF all three clear both.
Harness: `realloc_gate.py` (reuses PR #157 `regime_gate.py` pattern verbatim). Bootstrap n=100, block 126 bd.

## Result — all three FAIL

| candidate | Σrisk | full p / b / p99 | **H1** bust / p99 | H2 bust / p99 | boot bust95 / p99-95 | verdict |
|---|---:|---|---|---|---|---|
| REF (4-strat locked) | 2.91% | 97.04 / 2.96 / 5.93 | 24.54% / 8.57% ❌ | 0.54% / 4.87% ✅ | 9.00% / 7.14% | **FAIL** |
| D1 (drop Guardian) | 2.57% | 97.88 / 2.12 / 5.60 | 16.25% / 8.05% ❌ | 0.59% / 4.89% ✅ | 6.73% / 6.97% | **FAIL** |
| D3 (dropG→Strikers) | 2.91% | 94.76 / 5.24 / 6.40 | 23.23% / 8.44% ❌ | 2.15% / 5.68% ❌ | 12.64% / 7.63% | **FAIL** |

- **Fidelity:** REF full-panel reproduces PR #157's S_2020 (97.04 / 2.96 / 5.93) exactly. Harness verified.
- **All three fail decisively on H1** (bust 16–25% ≫ 1%, p99 8.0–8.6% ≫ 5%) — the deterministic half-panel
  alone determines the verdict; the n=100 bootstrap (bust95 6.7–12.6%) corroborates.
- **D3 is WORSE than D1** (full bust 5.24% vs 2.12%; D3 also fails H2) — on the honest decompounded basis,
  reallocating the freed Guardian budget *up into the pyramid Strikers backfires* (decompounding un-hides
  the Striker tail; the compounded grid's D3-best ranking was a compounding artifact).
- Dropping Guardian (D1) helps H1 (24.54 → 16.25% bust) but stays far above the floor.

**Verdict:** no static reallocation — including removing Guardian — is regime-robust. Re-confirms PR #157.
The fix is regime-adaptive, not static. → `oracle_test.md` (which then killed resizing too).

**Artifacts:** `realloc_gate.py` + `realloc_gate.json`.
