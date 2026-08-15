# Code DRY audit — 2026-08-11 (Option B)

**Status:** `CODE-DRY: REPAIRED` (S1 risk% + S2 DD imports + C5 rail ULP + SWEEP lock cells)  
**Companion:** Rule-7 prose DRY — [`2026-08-11-rule7-dry-fact-audit.md`](2026-08-11-rule7-dry-fact-audit.md)  
**Method:** Owner map from ADR 2026-06-06 + `firm_rules` docstring; grep for re-literalized lock bytes; triage intentional grids vs silent copies.

---

## Owners (code)

| Fact | Canonical owner |
|---|---|
| Locked book risk % | `core/firm_rules.py` `_BASE_RISK` (+ `base_risk_display()`) |
| Live sizing dict (Title-Case) | **derived** `dd_protection.BASE_RISK` |
| MC default allocations | **derived** `mc.modes.ALLOCATIONS` |
| `DD_TRIGGER` / `DD_SCALE` | `core/dd_protection.py` literals |
| DD scale application (ULP) | `dd_protection.calculate_protection` (rail calls through) |
| Historical FXIFY challenge fixture | `core/historical_challenge.py` (Phase 4; ADR SSOT completed) |

---

## Findings

| ID | path | issue | sev | action |
|---|---|---|---|---|
| C1 | `dd_protection.BASE_RISK` + `modes.ALLOCATIONS` + `PINE_SHRINK_ALLOCATIONS` | independent literals of `_BASE_RISK` | **S1** | **REPAIRED** — derive from `firm_rules` |
| C2 | `mc/preflight.py` | hardcoded `0.015`/`0.40` | **S2** | **REPAIRED** — import `DD_*` |
| C3 | `lab/discovery/prop_survivor_scoring.py` | `DD_SCALE = 0.40` | **S2** | **REPAIRED** — import |
| C4 | `scripts/verify_lock_anchors.py` | AST-parsed Guardian from `BASE_RISK` dict literal | — | **UPDATED** — Guardian from `firm_rules._BASE_RISK`; DD_* still from `dd_protection` |
| C5 | `ops/c1_rail/..._read_dd_scale` | parallel ULP DD math vs `calculate_protection` | **S2** | **REPAIRED** — ratchet then `calculate_protection(...).multiplier` |
| C6 | `modes.SWEEP_CONFIGS` / REG / GA / ML | restate lock bytes inside historical grids | — | **REPAIRED** — REG + unchanged legs from `ALLOCATIONS`; GA/ML overrides stay local |
| C7 | dated `lab/analysis/c1/*` campaign pins | `0.015`/`0.40` / F2 floors | leave | frozen RESULTS-tied |
| C8 | firm-challenge triplication (ADR 2026-06-06) | — | n/a | **already resolved** via `historical_challenge` |

---

## Tests

- `tests/core/test_firm_constants_single_source.py` — derivation + `PINE_SHRINK` + SWEEP REG/GA4
- `tests/ops/test_c1_sizing_host_reference.py` — DD trigger + C5 `_read_dd_scale` ↔ `calculate_protection`
- `tests/test_verify_lock_anchors.py` — dual-source fixtures

---

## Left intentionally

1. Broader copy-paste helpers (`utc_now_iso`) — S3 only  
2. Campaign-dated lab pins (C7) — do not fold into live owners  
3. GA/ML **variant** override literals in `SWEEP_CONFIGS` — historical search cells, not lock SSOT
