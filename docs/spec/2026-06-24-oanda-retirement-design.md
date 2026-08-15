# OANDA Retirement — Design Spec

**Date:** 2026-06-24
**Author:** Joshua (decision) + Claude Code (design)
**Status:** Approved (operator sign-off 2026-06-24)
**Implements:** full retirement of OANDA from the repo
**Plan:** `docs/spec/2026-06-24-oanda-retirement-plan.md`
**Governance:** `docs/adr/2026-06-24-oanda-retirement.md` (authored at execution)
**Precedent / template:** `docs/adr/2026-06-17-dukascopy-retirement.md` (+ its design/plan). That ADR
explicitly scoped `scripts/fetch_oanda_bars.py` (OANDA) **out** and "untouched"; this work
completes that arc — one canonical feed family (TV/Pepperstone BAR EXPORT v0.1).

---

## §0 — Decision (operator)

OANDA is retired entirely. Two operator decisions (2026-06-24) fix the posture:

1. **Cross-feed validation tier → full single-feed.** The `portfolio_mc.py` OANDA proxy panel,
   the `--panel oanda` CLI path, the "OANDA proxy 99.85%" anchor in `CLAUDE.md`, and the OANDA
   anchor pins are removed. The **two-tier canonical** methodology (OANDA proxy drives Action /
   Pepperstone validates) collapses to **single-tier** (Pepperstone/TV is the sole canonical feed).
2. **Data + closed lab investigations → freeze as historical.** Files are kept with retirement
   banners; OANDA CSVs stay manifest-pinned so historical anchors remain reproducible-in-principle.
   Mirrors the Dukascopy treatment of cached `*_duka.csv` + the 5 frozen lab scripts.

**Decision driver (one sentence):** the operator standardizes on one canonical, interpretable,
broker-fidelity feed (TV/Pepperstone BAR EXPORT) and accepts the loss of the independent OANDA
second-feed cross-check — the same cost the Dukascopy retirement accepted, now extended to all of OANDA.

---

## §1 — Context: what OANDA is in this repo

OANDA wears two hats. The operator's framing ("I was using it because of the available API, but the
bar export strategy works better") targets the first; decision §0.1 extends retirement to the second.

**Hat A — the OANDA REST API (data + live-NAV source).** `core/lib/oanda.py`
(`fetch_candles` + `account_summary`), `core/lib/oanda_creds.py`, `scripts/fetch_oanda_bars.py`,
`ops/cli.py --from-oanda`, creds at `~/.keys/oanda.txt`. Superseded by the already-canonical
BAR EXPORT v0.1 producer (`core/bar_export_loader.py` + `scripts/parse_bar_export.py`, landed 2026-06-17).

**Hat B — the cross-feed validation tier (methodology).** `portfolio_mc.py`
`PANELS_BY_BROKER["oanda"]` / `--panel oanda` (4 TV CSV exports under `core/data/tv_exports/oanda/`),
the `CLAUDE.md` "OANDA proxy" anchor, `[mc_anchor_oanda]` in `params.toml`, and the anchor pins in
`tests/test_mc_anchors.py` / `verify_lock_anchors.py`. This is the two-tier canonical rule
(memory `feedback_two_tier_canonical_pepperstone_oanda`).

**Architecture note — this is a removal, not a producer swap.** Unlike Dukascopy (which needed a new
loader built first), OANDA's replacement producer already exists and is canonical. So there is **no new
code to write** — only deletion, wiring removal, methodology collapse, governance, and verification.

---

## §2 — Load-bearing facts (verified by a 4-agent read-only mapping pass, 2026-06-24)

1. **No re-MC required.** The Pepperstone headline (99.83% pass / 0.17% bust / p99 DD 4.37% /
   median 26) is computed at `panel_name="pepperstone"` (the `DEFAULT_PANEL`), threaded through
   `compute_default_config → _load_all` independently of any OANDA construct. Removing the OANDA
   panel cannot change it. The fixed-1R reference `PRE_SHOCK_1R` is Pepperstone-derived.
2. **No live-API breakage.** The only runtime callers of the OANDA REST API are `cli.py --from-oanda`
   and `scripts/fetch_oanda_bars.py` — both deleted. `ops/regime_gate/gold_gate_shadow.py` and
   `ops/parity_check.py` read **cached CSVs** (`core/data/bar_data/XAUUSD.csv`, TV export CSVs), not
   the API. Three frozen lab scripts import `lib.oanda` but are not pytest-collected and are closed.
3. **`--panel` choices auto-narrow.** `argparse` builds `choices=list(PANELS_BY_BROKER.keys())`;
   dropping the `"oanda"` key removes the choice with no separate edit.
4. **The MVD short-fetch / cardinality gate is generic** (floor at 100 raw rows for any panel). It
   was *motivated* by an OANDA incident but is not OANDA-bound — it stays; only its comment is reworded.
5. **OANDA is not a configured firm** in `firm_rules.py`; the `--from-oanda` gate is a thin live-NAV
   reader in `ops/cli.py` only. Removing it sends any `firm="OANDA"` account to manual balance entry.

---

## §3 — Disposition model (five buckets; 153 files, ~710 refs)

### Bucket (i) — DELETE (live API + its tests)
`git rm`:
- `core/lib/oanda.py`, `core/lib/oanda_creds.py`
- `scripts/fetch_oanda_bars.py`
- `tests/test_oanda.py`, `tests/test_fetch_oanda_bars.py`, **`tests/test_oanda_gate.py`**
- `ops/cli.py`: delete `_fetch_oanda_balance(...)` + the `--from-oanda` argparse option + its routing in `cmd_update`.

> **Resolved judgment call:** `test_oanda_gate.py` is **deleted** (not kept). It exercises
> `_fetch_oanda_balance` / `--from-oanda`, whose subject is removed; it has nothing left to test.

### Bucket (ii) — REMOVE WIRING (edit to drop OANDA; anchor-verification must stay GREEN)
Treated as **one coherent unit** because these must remain mutually consistent:
- `core/portfolio_mc.py`: delete `OANDA_DIR`, `OANDA_PANELS`; remove the `"oanda"` key from
  `PANELS_BY_BROKER`, `EXPECTED_SYMBOLS_BY_BROKER`, `EXPECTED_VERSIONS_BY_BROKER`; drop the
  `--panel oanda` docstring example; reword the MVD comment to drop "OANDA". (`--panel` choice
  auto-narrows.) Broker abstraction survives as a single-entry dict; bust-attribution stays the 4-tuple.
- `core/config/params.toml`: delete the `[mc_anchor_oanda]` section (line 134+); update the header comment.
- `scripts/verify_lock_anchors.py`: delete `_OANDA_HEADLINE_RE`; make the CLAUDE.md/params/test-pin
  parsers + comparators Pepperstone-only (loops `("pepperstone", "oanda")` → `("pepperstone",)`);
  drop the optional `[mc_anchor_oanda]` manifest-shape validation; drop the `--panel oanda` hint in `decide()`.
- `tests/test_mc_anchors.py`: delete `test_oanda_anchor`, `test_oanda_panel_shape`, the `oanda_result`
  fixture, the `requires_oanda` marker / `_OANDA_PRESENT`; rewrite the module docstring +
  `test_default_panel_is_pepperstone` docstring to single-tier. Keep all Pepperstone tests.
- `tests/test_verify_lock_anchors.py`: remove OANDA from `BASELINE_CLAUDE_MD`, `BASELINE_PARAMS_TOML`,
  `BASELINE_TEST_ANCHORS` fixtures (the routing tests then prove the verifier tolerates OANDA-absence).
- `CLAUDE.md` MC anchor block: delete the "OANDA proxy: 99.85% …" line (line 59); replace with a
  one-line "OANDA cross-feed retired 2026-06-24 (see ADR)" pointer.

### Bucket (iii) — FREEZE WITH BANNER (closed investigations + frozen analytics)
- `lab/analysis/oanda_stage1/`: banner the **OANDA-bar-consuming** investigation scripts
  (`guardian_stage1.py`, `aegis_stage1.py`, `striker_stage1.py`, `bar_loader.py`,
  `post_exit_excursion.py`, `__init__.py`). **`permutation.py` + `pine_indicators.py` are shared
  helpers** imported by `oil_carry/f1_mechanism.py` and `usdcad_rdm/gate.py` — banner them as
  "retained, shared helper" (NOT "no longer runs").
- `docs/analytics/mc_anchor_evolution/`: add a dated **archive banner** to `README.md`. **Keep
  `plot.py`, `data.csv` (6 OANDA rows), and the 3 OANDA chart-guard tests** in
  `tests/test_mc_anchor_chart.py` — the historical OANDA overlay stays frozen and visible.

> **Resolved judgment call:** broken `from lib.oanda import …` in the 3 frozen lab scripts
> (`regime_ratevol_2026-06-16`, `eurusd_pattern_enum`) is acceptable — `lab/` is not pytest-collected,
> investigations are closed, banner states they no longer run. Exact Dukascopy precedent.

### Bucket (iv) — LEAVE AS HISTORICAL RECORD (no edit; ~120 files)
`docs/adr/*`, `docs/briefs/*` (Q-SWAP / Q-REGIME / pre-registration), `docs/mc_anchor_history.md`,
prior `docs/SESSIONS.md` entries, instrument ledgers, strategy changelogs, prior audits. These are the
audit trail and are not edited.

### Bucket (v) — METHODOLOGY / MEMORY UPDATE (two-tier → single-tier)
- `docs/operational_rules.md`: revise the two-tier-canonical references to single-tier.
- `CLAUDE.md` prose: any line presenting OANDA as a live cross-feed / the vendor-data restore note's
  "OANDA bars via `fetch_oanda_bars.py`" clause.
- Memory (outside repo): rewrite `feedback_two_tier_canonical_pepperstone_oanda.md` to single-tier;
  retire `reference_oanda_credentials.md`; leave `feedback_oanda_dow_feed_artifact.md` (valid historical
  prior). Update `MEMORY.md` index.

### Live-consequence edits (small, in-scope)
- `pyproject.toml`: remove `broker = ["oandapyV20"]` (line 25).
- `.gitignore`: drop OANDA from the two vendor-data comment lines.
- `README.md`, `REPO_MAP.md`: drop OANDA-as-live-feed mentions; point bar restoration at `parse_bar_export.py`.
- `ops/regime_gate/gold_gate_shadow.py`: one-line edit to its restore-method comment
  (`fetch_oanda_bars.py` → `parse_bar_export.py --symbol XAUUSD`).
- `.github/workflows/manifest-check.yml` + `scripts/check_data_manifests.py`: **no change** — the
  OANDA manifest dir stays pinned (see §4.3).

---

## §4 — Key disposition rulings (with rationale)

1. **`test_oanda_gate.py` → DELETE.** Subject (`--from-oanda`) is removed.
2. **`mc_anchor_evolution` → FREEZE, keep overlay.** Consistent with freeze-as-historical; the chart
   keeps the OANDA proxy trajectory + its guard tests; only an archive banner is added.
3. **`core/data/tv_exports/oanda/` manifest dir → KEEP, stays gated.** Frozen-but-pinned matches the
   Dukascopy `*_duka.csv` treatment and preserves reproducibility of historical anchors. It remains one
   of the five `MANIFEST_DIRS`; the gate is a no-op protector over frozen bytes.
4. **`oanda_stage1/permutation.py` + `pine_indicators.py` → retained shared helpers.** Imported by live
   lab analyses; a "does-not-run" banner would be wrong.
5. **No re-MC, no live-gate breakage** (§2.1, §2.2). The retirement is purely subtractive.

---

## §5 — Governance & supersession

- Author `docs/adr/2026-06-24-oanda-retirement.md` via **brief-authoring** (ADR type): §0 Rule-0 reads,
  §2 decision, §3 alternatives (keep-API-only / deprecate-in-place / status-quo — ruled out), §4 falsifier
  (single-feed accepts loss of the independent cross-check; revert trigger = a pre-registered cross-feed
  corroboration need that single-feed cannot satisfy — supersede, never edit §4 in place), §5 forbidden
  moves (re-introducing a programmatic broker feed by convention without an ADR; citing frozen OANDA CSVs
  as canonical-fresh; loosening §4 under friction), §6 consequences, §10 audit hooks.
- Records the **two-tier → single-tier methodology change** and notes it **extends** the 2026-06-17
  Dukascopy retirement (no supersession needed — that ADR scoped OANDA out; this completes it).

---

## §6 — Out of scope (explicit)

- **Skill files (8, cloud-synced):** `fxify-challenge`, `trade-csv-reconcile` (+ `baselines.md`,
  `reconcile.py`), `inqhiori`, `live-execution-journal` (+ `journal_review.py`), `code-defect-debugging`.
  On-disk `SKILL.md` edits do not persist (memory `feedback_skill_amendments_via_authoring_path`). These
  are **listed for the operator** to amend via the skill-authoring path; NOT edited in this run.
- **`~/.keys/oanda.txt`** (outside the repo): operator may delete; not a repo action.
- **Gold-gate feed re-source** (`parse_bar_export.py --symbol XAUUSD` to refresh
  `core/data/bar_data/XAUUSD.csv`): operator follow-up; cached CSV still serves the shadow gate, so not
  a blocker.

---

## §7 — Verification gate (acceptance)

- `python scripts/check_boundaries.py` — clean.
- `python -m pytest tests/ -q` — green; no `test_oanda*.py` / `test_fetch_oanda_bars.py`; Pepperstone
  anchor + chart tests pass.
- `python scripts/verify_lock_anchors.py` — routes **Closed** (no OANDA expected in CLAUDE.md/params/pins).
- `make validate` — params + data manifests + pine manifest all pass (OANDA manifest dir still pinned).
- `python core/portfolio_mc.py --panel pepperstone` — reproduces the canonical headline (no re-MC).
- `grep -rin "lib.oanda\|fetch_oanda_bars\|--from-oanda\|--panel oanda" --include=*.py .` — only frozen
  banners / closed lab bodies; no live importer of the deleted API.

---

## §8 — Execution & parallelization

Parallel subagents per independent bucket, then a serialized verify gate. Bucket (ii) — anchor surgery —
runs as **one coherent unit** (portfolio_mc + params.toml + verify_lock_anchors + the two anchor tests +
the CLAUDE.md anchor block must stay mutually consistent). Buckets (i) API-delete, (iii) lab-freeze,
(v)+consequence docs run in parallel. `CLAUDE.md` is a shared hazard file (anchor block in (ii), prose in
(v)) — its edits are serialized into a single pass. Final stage: the §7 gate. Detailed task graph in the plan.
