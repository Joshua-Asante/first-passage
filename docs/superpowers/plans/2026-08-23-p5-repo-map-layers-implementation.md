# P5 REPO_MAP ↔ check_boundaries — Implementation Plan

> **For agentic workers:** Landed same session as GO. REQUIRED SUB-SKILL was executing-plans inline.

**AUTHORIZATION:** **GO 2026-08-23.** Operator: close remaining pain-point packets. Charter §P5.

**Goal:** HARD fail when `APP_LAYER_PREFIX` / `GOVERNANCE_PREFIXES` / `SCRIPTS_LAYER` drift from a machine sibling YAML.

**Shipped:**
- [`scripts/repo_map_layers.yml`](../../../scripts/repo_map_layers.yml)
- [`scripts/check_repo_map_layers.py`](../../../scripts/check_repo_map_layers.py)
- `repo-map-layers` in [`scripts/gates.yml`](../../../scripts/gates.yml) (path-conditional HARD)
- [`tests/test_repo_map_layers.py`](../../../tests/test_repo_map_layers.py)
- [`REPO_MAP.md`](../../../REPO_MAP.md) header pointer

**Falsifier:** prefix in Python dict missing from YAML (or reverse) and `make check` green — **cleared** (mutate test fails; live maps OK).
