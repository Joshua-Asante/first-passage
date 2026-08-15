# OANDA Retirement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retire OANDA entirely — delete the live REST API code, collapse the two-tier cross-feed MC validation to single-tier (Pepperstone/TV only), and freeze OANDA data + closed lab investigations as historical artifacts — leaving one canonical feed family (TV/Pepperstone BAR EXPORT v0.1).

**Architecture:** Purely subtractive. The replacement bar producer (`core/bar_export_loader.py` + `scripts/parse_bar_export.py`) already exists and is canonical (landed 2026-06-17). No new code is written. The work is: delete (Hat A — REST API), remove wiring + collapse methodology (Hat B — cross-feed tier), freeze (data + closed lab), update docs/memory, record governance. Verified facts: **no re-MC required** (Pepperstone headline is OANDA-independent) and **no live-API breakage** (gold-gate/parity read cached CSVs, not the API).

**Tech Stack:** Python 3, pandas, pytest, tomllib. Repo conventions: `pyproject.toml` `pythonpath` adds `core/`, `lab/`, `ops/`; boundaries enforced by `scripts/check_boundaries.py`; vendor-data integrity by `scripts/check_data_manifests.py` + the `scripts/githooks/pre-commit` hash gate; lock-anchor agreement by `scripts/verify_lock_anchors.py`.

**Spec:** `docs/spec/2026-06-24-oanda-retirement-design.md`

**Testing model (NOT new-test TDD — this is a removal):** the gate is the *existing* suite staying green after the removal, minus the deleted OANDA tests, plus `verify_lock_anchors.py` routing **Closed** and a clean grep sweep. Each task runs the relevant existing checks after its edit.

**Parallelization:** Tasks 1–4 touch **disjoint file sets** and run concurrently. Tasks 5→6→7→8 are serial (docs prose → governance → memory → final gate). The §8 execution note in the spec maps this to a Workflow fan-out + serial tail.

---

### Task 0: Branch + baseline green

**Files:** none (verification only)

- [ ] **Step 1: Confirm worktree branch + clean tree**

Run: `git status -sb`
Expected: on `claude/festive-neumann-289a93`, clean (design + plan already committed).

- [ ] **Step 2: Record the pre-change baseline (so regressions are attributable)**

Run: `python -m pytest tests/ -q 2>&1 | tail -5`
Expected: all green (data-dependent OANDA/Pepperstone tests may skip if vendor CSVs absent on this clone — note which).

Run: `python scripts/verify_lock_anchors.py`
Expected: `ROUTING: Closed` (exit 0).

Run: `python scripts/check_boundaries.py`
Expected: PASS.

---

### Task 1 [PARALLEL]: Delete the live OANDA REST API + its tests + `--from-oanda`

**Files:**
- Delete: `core/lib/oanda.py`, `core/lib/oanda_creds.py`, `scripts/fetch_oanda_bars.py`
- Delete: `tests/test_oanda.py`, `tests/test_oanda_gate.py`, `tests/test_fetch_oanda_bars.py`
- Modify: `ops/cli.py` (remove `_fetch_oanda_balance` + `--from-oanda`)

- [ ] **Step 1: Delete the six API/test files**

```bash
git rm core/lib/oanda.py core/lib/oanda_creds.py scripts/fetch_oanda_bars.py \
       tests/test_oanda.py tests/test_oanda_gate.py tests/test_fetch_oanda_bars.py
```

- [ ] **Step 2: Remove the `--from-oanda` path from `ops/cli.py`**

In `ops/cli.py`:
1. Delete the entire `_fetch_oanda_balance(account_id: str) -> float:` function (the `def` at ~line 36 through its `return float(summary["NAV"])` at ~line 67).
2. In `cmd_update`, replace the `--from-oanda` branch. Current shape (~lines 84–93):

```python
def cmd_update(args):
    try:
        if args.from_oanda:
            if args.balance is not None:
                raise ValueError("--from-oanda and explicit balance are mutually exclusive")
            balance = _fetch_oanda_balance(args.account_id)
        else:
            if args.balance is None:
                raise ValueError("balance required (or pass --from-oanda for OANDA-tracked accounts)")
            balance = args.balance
```

becomes:

```python
def cmd_update(args):
    try:
        if args.balance is None:
            raise ValueError("balance required")
        balance = args.balance
```

3. Delete the `--from-oanda` argparse option (~lines 228–229) and update the `balance` positional help (~lines 226–227) to drop the `--from-oanda` mention:

Current:
```python
    p_update.add_argument("balance", type=float, nargs="?", default=None,
                          help="New balance in account currency. Omit when --from-oanda is set.")
    p_update.add_argument("--from-oanda", action="store_true",
                          help="Read live NAV from OANDA REST API. Only allowed for firm=OANDA accounts that match the credentials in ~/.keys/oanda.txt.")
```
becomes:
```python
    p_update.add_argument("balance", type=float,
                          help="New balance in account currency.")
```

> Note: `balance` becomes required (was `nargs="?"`) because the only reason it was optional was `--from-oanda`. Verify no other code passes `args.from_oanda` (grep below).

- [ ] **Step 3: Verify no dangling `from_oanda` / `lib.oanda` reference in live code**

Run: `grep -rn "from_oanda\|lib.oanda\|oanda_creds\|account_summary\|fetch_candles" ops/ core/ scripts/ --include=*.py`
Expected: empty (frozen `lab/` importers handled in Task 3; they are not searched here).

- [ ] **Step 4: Boundaries + targeted tests still pass**

Run: `python scripts/check_boundaries.py`
Expected: PASS.

Run: `python -m pytest tests/test_fxify_challenge_integration.py -q`
Expected: PASS (this exercises `cli.py`; confirms the `cmd_update` edit is clean). If it references `--from-oanda`, fix that reference here.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor: delete OANDA REST API (lib.oanda + creds + fetch + --from-oanda) and its tests

Hat A of the OANDA retirement (docs/spec/2026-06-24-oanda-retirement-design.md).
Bar acquisition is now solely the BAR EXPORT v0.1 pipeline.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2 [SERIAL SPINE — atomic]: Collapse the OANDA cross-feed MC tier (single-feed)

**Why atomic:** `tests/test_mc_anchors.py:47` imports `OANDA_PANELS` from `portfolio_mc`; deleting that symbol breaks test collection unless the test is edited in the same commit. Removing `[mc_anchor_oanda]` from `params.toml` routes `verify_lock_anchors.py` to **Action** unless that script is edited in the same commit. So `portfolio_mc.py` + `params.toml` + `test_mc_anchors.py` + `verify_lock_anchors.py` + `test_verify_lock_anchors.py` + `CLAUDE.md` move together.

**Files:**
- Modify: `core/portfolio_mc.py`
- Modify: `core/config/params.toml`
- Modify: `tests/test_mc_anchors.py`
- Modify: `scripts/verify_lock_anchors.py`
- Modify: `tests/test_verify_lock_anchors.py`
- Modify: `CLAUDE.md`

- [ ] **Step 1: `core/portfolio_mc.py` — remove OANDA constructs**

1. Docstring (~line 15): delete the line `    python portfolio_mc.py --panel oanda                   # pattern-spotting proxy`.
2. Delete `OANDA_DIR` (line 75):
   ```python
   OANDA_DIR = Path(__file__).parent / "data" / "tv_exports" / "oanda"
   ```
3. Delete the `OANDA_PANELS` dict (lines 76–81):
   ```python
   OANDA_PANELS: Dict[str, Path] = {
       "guardian":       OANDA_DIR / "Guardian_Gold_v5.5_OANDA_XAUUSD_2026-05-24_6a494.csv",
       "striker":        OANDA_DIR / "Striker_DJ30_v4.5_OANDA_US30USD_2026-05-24_345b4.csv",
       "aegis":          OANDA_DIR / "Aegis_USDJPY_v4.3_OANDA_USDJPY_2026-05-24_d1d55.csv",
       "striker_nas100": OANDA_DIR / "Striker_NAS100_v1_OANDA_NAS100USD_2026-05-24_2aeda.csv",
   }
   ```
4. `PANELS_BY_BROKER` (lines 104–107) → drop the `"oanda"` key (keep the broker abstraction as a single-entry dict):
   ```python
   PANELS_BY_BROKER: Dict[str, Dict[str, Path]] = {
       "pepperstone": PEPPERSTONE_PANELS,
   }
   ```
   Also reword the comment above it (lines 100–103) to drop the OANDA framing — keep one line: `# Pepperstone is the sole canonical lock anchor (OANDA cross-feed retired 2026-06-24, ADR).`
5. `EXPECTED_SYMBOLS_BY_BROKER` (lines 110–113) → drop the `"oanda"` key and its preceding "(Pepperstone uses US30, OANDA uses US30USD…)" comment:
   ```python
   EXPECTED_SYMBOLS_BY_BROKER: Dict[str, Dict[str, str]] = {
       "pepperstone": {"guardian": "XAUUSD", "striker": "US30", "aegis": "USDJPY", "striker_nas100": "NAS100"},
   }
   ```
6. `EXPECTED_VERSIONS_BY_BROKER` (lines 117–120) → drop the `"oanda"` key and the "as of 2026-05-24, OANDA reaches parity…" comment:
   ```python
   EXPECTED_VERSIONS_BY_BROKER: Dict[str, Dict[str, str]] = {
       "pepperstone": {"guardian": "v5.5", "striker": "v4.5", "aegis": "v4.3", "striker_nas100": "v1"},
   }
   ```
7. MVD comment (line 258): reword to drop "OANDA":
   - From: `    # MVD cardinality — catches OANDA short-fetch class (audit instance #2).`
   - To:   `    # MVD cardinality — catches the short-fetch class (audit instance #2).`
8. The `panel_strats` / 3-vs-4 comment near lines 701–702 ("both Pepperstone and OANDA carry all 4 (OANDA reached parity…)") → reword to drop OANDA:
   `    # Panel-specific strategy set: the Pepperstone panel carries all 4 strategies.`
9. `--panel` argparse (line 1581): **no edit** — `choices=list(PANELS_BY_BROKER.keys())` auto-narrows to `["pepperstone"]`.

- [ ] **Step 2: `core/config/params.toml` — delete `[mc_anchor_oanda]`**

Delete the entire section (lines 134–141):
```toml
[mc_anchor_oanda]
pass_pct      = 99.85
bust_pct      = 0.15
p99_dd_pct    = 4.42
median_days   = 23
anchor_date   = "2026-05-24"
panel         = "4-strategy (DJ30 v4.5 + NAS100 v1, 2026-05-24 vintage, 1141 bdays / 227 week-blocks)"
note          = "Pattern-spotting proxy. ..."
```
Leave `[mc_anchor_pepperstone]` untouched.

- [ ] **Step 3: `tests/test_mc_anchors.py` — drop OANDA tests/fixtures**

1. Import (line 47): remove `OANDA_PANELS,` from the `from portfolio_mc import (...)` block.
2. Remove the OANDA presence marker (lines 56, 62–65): delete `_OANDA_PRESENT = ...` and the `requires_oanda = pytest.mark.skipif(...)` block.
3. Delete the `oanda_result` fixture (lines 76–81).
4. Delete `test_oanda_anchor` (lines 106–127) and `test_oanda_panel_shape` (lines 145–155).
5. Module docstring (lines 19–29): delete the "OANDA is the pattern-spotting proxy …" paragraph.
6. `test_default_panel_is_pepperstone` docstring (lines 161–174): reword to drop the OANDA-flip scenario — keep the assertion logic (lines 176–185) unchanged. Replacement docstring:
   ```python
       """Locks the doc-and-default agreement: DEFAULT_PANEL and the
       compute_default_config / mode_default / mode_sensitivity signature
       defaults must all be "pepperstone" (the sole canonical panel). Guards
       the bare `python portfolio_mc.py` path against silently changing feed.
       """
   ```

- [ ] **Step 4: `scripts/verify_lock_anchors.py` — make Pepperstone-only**

1. `load_params_anchors` (line 171): remove `"oanda": data.get("mc_anchor_oanda", {}),`.
2. Delete `_OANDA_HEADLINE_RE` (lines 187–191) and the comment line 179–180 "OANDA-style headline …".
3. `parse_claude_md_anchors_all` (194–224): replace the whole body with the Pepperstone-only version:
   ```python
   def parse_claude_md_anchors_all(
       text: str,
   ) -> dict[str, list[tuple[float, float, float]]]:
       """Return ALL Pepperstone headline match triples in CLAUDE.md.

       CLAUDE.md prints the Pepperstone headline more than once (Strategy
       Reference + Protection block); `check_claude_md_vs_params` flags any
       internal disagreement between occurrences as a Drift.
       """
       out: dict[str, list[tuple[float, float, float]]] = {"pepperstone": []}
       for m in _PEPPER_HEADLINE_RE.finditer(text):
           out["pepperstone"].append(
               (float(m.group(1)), float(m.group(2)), float(m.group(3)))
           )
       return out
   ```
4. `parse_claude_md_medians` (236–262): replace the body with the Pepperstone-only version:
   ```python
   def parse_claude_md_medians(text: str) -> dict[str, list[int]]:
       """Return median-days integers stated next to the Pepperstone headline."""
       out: dict[str, list[int]] = {"pepperstone": []}
       for m in _PEPPER_HEADLINE_RE.finditer(text):
           end = min(len(text), m.end() + _MEDIAN_WINDOW)
           mm = _MEDIAN_RE.search(text, m.end(), end)
           if mm:
               out["pepperstone"].append(int(mm.group(1)))
       return out
   ```
5. `parse_test_anchor_pins` (265–300): drop OANDA — `out` becomes `{"pepperstone": None}`; the name check becomes `if node.name != "test_pepperstone_anchor": continue`; the key assignment becomes `out["pepperstone"] = (...)`.
6. `check_claude_md_vs_params` (line 334): change `for panel in ("pepperstone", "oanda"):` → `for panel in ("pepperstone",):`.
7. `check_claude_md_medians_vs_params` (line 406): same loop change → `("pepperstone",)`.
8. `check_params_vs_test_pins` (line 433): same loop change → `("pepperstone",)`.
9. `_validate_manifest_shape` (583–618): delete the OANDA block (lines 600–608):
   ```python
       oanda = params["oanda"]
       if oanda:
           for key in ("pass_pct", "bust_pct", "p99_dd_pct"):
               if key not in oanda:
                   errors.append(
                       f"config/params.toml: [mc_anchor_oanda] missing key '{key}'"
                   )
       # OANDA section absence is allowed; reported as Drift in
       # check_claude_md_vs_params instead.
   ```
10. `decide()` Forward notes (lines 686–688): delete the line `                "  python portfolio_mc.py --panel oanda",`.
11. Docstring (line 38): already says `--panel pepperstone` — leave. Header line 14 `[mc_anchor_*]` is generic — leave.

- [ ] **Step 5: `tests/test_verify_lock_anchors.py` — drop OANDA from baselines**

1. `BASELINE_CLAUDE_MD` (line 46): delete `OANDA pattern-spotting: **99.51% pass / 0.49% bust / p99 DD 4.82%**.` (and its surrounding blank line).
2. `BASELINE_PARAMS_TOML` (lines 84–88): delete the `[mc_anchor_oanda]` section.
3. `BASELINE_TEST_ANCHORS` (lines 98–101): delete the `test_oanda_anchor` function.
4. **Read the rest of the file (lines 115+)** and delete/repoint any test case that specifically mutates the OANDA baseline (e.g. an "OANDA drift" case). If none reference OANDA, no further change.

- [ ] **Step 6: `CLAUDE.md` — all OANDA edits (anchor block + prose, single file)**

1. Anchor block (line 59): delete `* OANDA proxy: **99.85% pass / 0.15% bust / p99 DD 4.42%**, median 23.` Replace with: `* OANDA cross-feed tier retired 2026-06-24 — Pepperstone/TV is the sole canonical feed. See [\`docs/adr/2026-06-24-oanda-retirement.md\`](docs/adr/2026-06-24-oanda-retirement.md).`
2. Line 61: `Anchor evolution (9 Pepperstone anchors + OANDA overlay + bust-attribution), …` → `Anchor evolution (9 Pepperstone anchors + frozen OANDA historical overlay + bust-attribution), …` (overlay is now frozen-historical).
3. Line 55: `Full table for all four strategies (incl. OANDA cross-feed and historical archival rows) at …` → `Full table for all four strategies (incl. frozen OANDA historical rows) at …`
4. Vendor-data restore note (search for `OANDA bars still via \`scripts/fetch_oanda_bars.py\``, in the Public-clone posture section): change to drop OANDA — the bar restore route is now solely `python scripts/parse_bar_export.py --symbol <SYMBOL>`. Adjust the surrounding sentence so it no longer presents OANDA as a live bar source.
5. Vendor-data integrity gate — the "five manifest dirs" enumeration stays (the OANDA dir remains frozen-but-pinned per design §4.3); no change needed there.

- [ ] **Step 7: Verify the atomic unit is green**

Run: `python -m pytest tests/test_mc_anchors.py tests/test_verify_lock_anchors.py -q`
Expected: PASS (OANDA tests gone; Pepperstone tests pass or skip-if-no-vendor-CSV; verifier fixture tests green).

Run: `python scripts/verify_lock_anchors.py`
Expected: `ROUTING: Closed` (exit 0) — proves removing `[mc_anchor_oanda]` no longer trips Action.

Run: `python scripts/check_boundaries.py`
Expected: PASS.

Run (if Pepperstone vendor CSVs present): `python core/portfolio_mc.py --panel pepperstone 2>&1 | tail -5`
Expected: reproduces 99.83/0.17/4.37 (no re-MC). If CSVs absent on this clone, note skipped.

Run: `python -c "import portfolio_mc; print(list(portfolio_mc.PANELS_BY_BROKER))"`
Expected: `['pepperstone']`.

- [ ] **Step 8: Commit (atomic)**

```bash
git add core/portfolio_mc.py core/config/params.toml tests/test_mc_anchors.py \
        scripts/verify_lock_anchors.py tests/test_verify_lock_anchors.py CLAUDE.md
git commit -m "refactor: collapse OANDA cross-feed MC tier to single-feed (Pepperstone)

Hat B of the OANDA retirement. Removes OANDA_PANELS/--panel oanda, the
[mc_anchor_oanda] manifest section, the OANDA anchor pins + verifier parsing,
and the CLAUDE.md OANDA proxy line. Pepperstone headline unchanged (no re-MC).
verify_lock_anchors routes Closed.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3 [PARALLEL]: Freeze closed lab investigations + analytics

**Files:**
- Modify (banner): `lab/analysis/oanda_stage1/{guardian_stage1,aegis_stage1,striker_stage1,bar_loader,post_exit_excursion,__init__}.py`
- Modify (banner, "retained shared helper"): `lab/analysis/oanda_stage1/{permutation,pine_indicators}.py`
- Modify (archive banner): `docs/analytics/mc_anchor_evolution/README.md`

- [ ] **Step 1: Banner the OANDA-bar-consuming investigation scripts**

Insert as the very first line of each of the six files
(`guardian_stage1.py`, `aegis_stage1.py`, `striker_stage1.py`, `bar_loader.py`, `post_exit_excursion.py`, `__init__.py`):

```python
# OANDA retired 2026-06-24 (docs/adr/2026-06-24-oanda-retirement.md) — frozen historical artifact; no longer runs (imports the deleted lib.oanda / reads archived OANDA bars).
```

(Place above any `"""docstring"""` / `from __future__` line; a leading comment is valid before `from __future__`.)

- [ ] **Step 2: Banner the two SHARED helpers differently (they still run)**

`permutation.py` is imported by `lab/archive/oil_carry/f1_mechanism.py` and `lab/archive/usdcad_rdm/gate.py`; `pine_indicators.py` is a generic helper. Banner them as **retained**, NOT "no longer runs":

```python
# OANDA Stage-1 investigation frozen 2026-06-24 (docs/adr/2026-06-24-oanda-retirement.md). This module is a generic, broker-agnostic helper RETAINED for active importers (e.g. oil_carry, usdcad_rdm) — it does not touch the OANDA API.
```

- [ ] **Step 3: Archive banner on the analytics README**

At the top of `docs/analytics/mc_anchor_evolution/README.md`, add:

```markdown
> **ARCHIVE NOTE (2026-06-24)** — the OANDA cross-feed is retired (`docs/adr/2026-06-24-oanda-retirement.md`). The OANDA overlay below is **frozen at its 5 historical anchors (2026-05-05 → 2026-05-24)**; no new OANDA anchors will be added. `plot.py` / `data.csv` and the OANDA chart-guard tests remain as a historical record.
```

> `plot.py`, `data.csv`, and the 3 OANDA chart-guard tests in `tests/test_mc_anchor_chart.py` are **kept unchanged** (freeze-as-historical, design §4.2).

- [ ] **Step 4: Confirm nothing collected by pytest broke + helpers still import**

Run: `python -m pytest tests/test_mc_anchor_chart.py -q`
Expected: PASS (OANDA overlay + guard tests intact).

Run: `python -c "import sys; sys.path.insert(0,'lab'); import analysis.oanda_stage1.permutation; print('ok')"`
Expected: `ok` (the retained helper still imports — it has no OANDA-API dependency).

- [ ] **Step 5: Commit**

```bash
git add lab/analysis/oanda_stage1/ docs/analytics/mc_anchor_evolution/README.md
git commit -m "docs: freeze OANDA Stage-1 lab + mc_anchor_evolution overlay as historical

Banners on closed OANDA-bar-consuming scripts (no longer run); retained-helper
banners on permutation.py/pine_indicators.py (still imported by active lab dirs);
archive note on the analytics README. Overlay/data/guard-tests kept.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4 [PARALLEL]: Standalone consequence files (dependency, gate comment, ignore)

**Files:**
- Modify: `pyproject.toml`
- Modify: `ops/regime_gate/gold_gate_shadow.py`
- Modify: `.gitignore`

- [ ] **Step 1: Remove the `oandapyV20` optional dependency**

Read the context around `pyproject.toml:25` (`broker = ["oandapyV20"]`). Delete that line. If it was the **only** entry under `[project.optional-dependencies]`, delete the now-empty `[project.optional-dependencies]` header too. If other extras exist, leave them.

- [ ] **Step 2: Repoint the gold-gate restore comment (`ops/regime_gate/gold_gate_shadow.py:78-79`)**

Current:
```python
        print(f"[skip] gold-gate shadow: missing vendor bars {missing} under {BARS} "
              f"(gitignored; restore via scripts/fetch_oanda_bars.py or a TV export). No log written.")
```
becomes:
```python
        print(f"[skip] gold-gate shadow: missing vendor bars {missing} under {BARS} "
              f"(gitignored; restore via scripts/parse_bar_export.py --symbol XAUUSD). No log written.")
```

- [ ] **Step 3: `.gitignore` comment hygiene (cosmetic, low-risk)**

Update the two primary vendor-data comment lines to drop the live-feed framing (the OANDA data files themselves stay gitignored — do **not** remove ignore *patterns*, only de-emphasize OANDA in comments):
- Line 72: `# Vendor-licensed data (Pepperstone TV exports + broker bar feeds + reference data; legacy OANDA exports frozen-historical).`
- Line 78: `# Vendor TV exports copied into research dirs under lab/ (Pepperstone TOS — local only).`
Leave lines 53, 133, 161 (specific ignore patterns / provenance notes) unchanged.

- [ ] **Step 4: Sanity — pyproject still parses, gate still imports**

Run: `python -c "import tomllib; tomllib.load(open('pyproject.toml','rb')); print('toml ok')"`
Expected: `toml ok`.

Run: `python -c "import sys; sys.path.insert(0,'ops'); import regime_gate.gold_gate_shadow; print('gate ok')"`
Expected: `gate ok`.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml ops/regime_gate/gold_gate_shadow.py .gitignore
git commit -m "chore: drop oandapyV20 dep; repoint gold-gate restore to parse_bar_export; gitignore comment hygiene

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5 [SERIAL — after 1–4]: Docs prose (README, REPO_MAP, operational_rules)

**Files:**
- Modify: `README.md`
- Modify: `REPO_MAP.md`
- Modify: `docs/operational_rules.md`

- [ ] **Step 1: `README.md`**

1. Line 53: delete `    python core/portfolio_mc.py --panel oanda            # pattern-spotting proxy panel` (the CLI choice is gone).
2. Line 56: `TradingView exports live under \`core/data/tv_exports/{pepperstone,oanda}/\`` → `… under \`core/data/tv_exports/pepperstone/\` (\`oanda/\` is a frozen historical panel)`.
3. Line 60: `The Pepperstone subdir is the lock-anchor source; OANDA is the proxy.` → `Pepperstone is the sole lock-anchor source (OANDA cross-feed retired 2026-06-24).`
4. Line 68: reword to keep the Pepperstone licensing note and frame OANDA as historical: `… Pepperstone (and legacy frozen OANDA) terms permit personal export but not public redistribution.`

- [ ] **Step 2: `REPO_MAP.md`**

1. Line 43 (live data-sources note): extend the existing Dukascopy-retirement clause to also note OANDA — append: `; OANDA retired per \`docs/adr/2026-06-24-oanda-retirement.md\` (\`*_oanda.csv\` frozen, manifest-pinned)`.
2. Line 92: remove `fetch_oanda_bars.py,` from the lab-scripts list (the script is deleted).
3. Lines 39, 49 (monorepo-migration mapping rows referencing `oanda_stage1/tv_export_loader.py`): **leave** — historical migration record.

- [ ] **Step 3: `docs/operational_rules.md`**

1. Read the file; find any statement of the **two-tier canonical (OANDA proxy / Pepperstone validates)** rule presented as CURRENT policy (the agent flagged ~line 21). Update it to single-tier: Pepperstone/TV is the sole canonical feed; OANDA retired 2026-06-24 (cite the ADR).
2. Line 256: `restore gitignored vendor data from its canonical source (cf. \`scripts/fetch_oanda_bars.py\`)` → `(cf. \`scripts/parse_bar_export.py\`)`.
3. Lines 100–101, 124 (the doc/code-skew **audit-table** historical rows): **leave** — these are dated incident records (bucket iv).

- [ ] **Step 4: Verify no live doc presents OANDA as a current feed/CLI**

Run: `grep -rn -i "panel oanda\|--from-oanda\|fetch_oanda_bars" README.md REPO_MAP.md docs/operational_rules.md CLAUDE.md`
Expected: empty.

- [ ] **Step 5: Commit**

```bash
git add README.md REPO_MAP.md docs/operational_rules.md
git commit -m "docs: single-feed framing in README/REPO_MAP/operational_rules (OANDA retired)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6 [SERIAL]: Governance — retirement ADR + SESSIONS

**Files:**
- Create: `docs/adr/2026-06-24-oanda-retirement.md` (via **brief-authoring** skill, ADR type)
- Modify: `docs/SESSIONS.md`

- [ ] **Step 1: Author the ADR**

Invoke the **brief-authoring** skill (ADR type). Required content (model on `docs/adr/2026-06-17-dukascopy-retirement.md`):
- **Status:** Accepted (operator executive decision, recorded). **Date:** 2026-06-24.
- **§0 Rule-0 reads:** `core/lib/oanda.py`, `ops/cli.py`, `core/portfolio_mc.py`, `scripts/verify_lock_anchors.py`, `core/config/params.toml`, `CLAUDE.md` anchor block, `docs/adr/2026-06-17-dukascopy-retirement.md` — cite content anchors via `git log -1 --format='%h %ci' -- <file>`.
- **§1 Context:** OANDA's two hats (REST API + cross-feed validation tier). Operator retires both; bar acquisition already canonical via BAR EXPORT v0.1. Extends the 2026-06-17 Dukascopy retirement (which scoped OANDA out).
- **§2 Decision:** (a) delete the REST API + tests + `--from-oanda`; (b) collapse two-tier → single-tier (remove OANDA panel/anchor/pins); (c) freeze OANDA data + closed lab as historical (manifest-pinned); (d) skill files handled via authoring path, `~/.keys/oanda.txt` operator-deleted.
- **§3 Alternatives:** keep-API-only / keep-panel-as-frozen-cross-check / deprecate-in-place / status-quo — ruled out (operator chose one broker-fidelity feed; the cross-check value did not justify maintaining a second feed + the two-tier methodology).
- **§4 Falsifier (revert trigger):** single-feed accepts the loss of independent cross-feed corroboration. Trigger: a **pre-registered** decision that materially needs an independent second-feed corroboration that single-feed cannot provide (a dated incident, not renewed plausibility). Action: supersede with a fresh ADR re-evaluating a second feed; never edit §4 in place. Review at each quarterly programme audit (next 2026-08-08).
- **§5 Forbidden moves:** re-introducing a programmatic broker feed by convention without an ADR; citing the frozen OANDA CSVs as canonical-fresh; loosening §4 under friction; re-adding `--panel oanda` wiring.
- **§6 Consequences:** + one canonical interpretable feed, single-tier methodology, one fewer maintained code path; − loss of the independent cross-check (accepted); gold-gate XAUUSD feed re-sources from `parse_bar_export.py` (operator follow-up; cached CSV still serves). Downstream-artifacts-updated list (CLAUDE.md, params.toml, tests, README, REPO_MAP, operational_rules, memory).
- **§10 Audit hooks (runnable):** `grep -rin "lib.oanda\|fetch_oanda_bars\|--from-oanda\|--panel oanda" --include=*.py .` → only frozen banners; `python scripts/verify_lock_anchors.py` → Closed; `python scripts/check_boundaries.py`; `make validate`.
- Records the **two-tier → single-tier methodology change**.

- [ ] **Step 2: Validate ADR discipline**

Run: `python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-06-24-oanda-retirement.md --type adr`
Expected: all checks PASS.

- [ ] **Step 3: SESSIONS.md entry**

Prepend a reverse-chron entry (5 fields per the session-log discipline): date 2026-06-24; what (OANDA fully retired — REST API deleted, cross-feed tier collapsed to single-feed, data/lab frozen, ADR recorded); result (suite green, verifier Closed, no re-MC); open/next (operator: skill-authoring-path edits for 8 skill files; optional gold-gate XAUUSD re-source; delete `~/.keys/oanda.txt`).

- [ ] **Step 4: Commit**

```bash
git add docs/adr/2026-06-24-oanda-retirement.md docs/SESSIONS.md
git commit -m "governance(oanda): retirement ADR (two-tier -> single-tier); SESSIONS entry

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7 [SERIAL]: Memory updates (outside the repo — not committed)

**Files (memory dir `C:\Users\joshu\.claude\projects\C--Users-joshu-multi-firm-operations\memory\`):**
- Modify: `feedback_two_tier_canonical_pepperstone_oanda.md`
- Modify/retire: `reference_oanda_credentials.md`
- Modify: `MEMORY.md` (index)

- [ ] **Step 1: Rewrite the two-tier memory to single-tier**

Update `feedback_two_tier_canonical_pepperstone_oanda.md`: the two-tier rule is **retired 2026-06-24** — Pepperstone/TV is the sole canonical feed; OANDA findings no longer route anything (the feed is gone). Keep a one-line historical note + link the ADR. Update the `description:` line accordingly.

- [ ] **Step 2: Retire the creds reference**

`reference_oanda_credentials.md`: mark the OANDA REST API + `~/.keys/oanda.txt` retired 2026-06-24 (code deleted). Either rewrite to a one-line tombstone or delete the file. Leave `feedback_oanda_dow_feed_artifact.md` as a valid historical prior.

- [ ] **Step 3: Update the MEMORY.md index**

Adjust the index lines for the two changed files (and remove the line if a file was deleted). Add a one-line pointer to the OANDA retirement if useful.

> No commit — memory lives outside the repo.

---

### Task 8 [SERIAL]: Final verification gate + skill-file handoff

**Files:** none (verification only)

- [ ] **Step 1: Full validate**

Run: `make validate`
Expected: params + data manifests + pine manifest all PASS (the frozen OANDA manifest dir still pins cleanly; pine WARN-only on this clone is OK).

- [ ] **Step 2: Boundaries + full suite**

Run: `python scripts/check_boundaries.py && python -m pytest tests/ -q`
Expected: both PASS; no `test_oanda*.py` / `test_fetch_oanda_bars.py`; Pepperstone anchor + chart tests pass (or skip-if-no-vendor-CSV). Note any skips.

- [ ] **Step 3: Lock-anchor routing**

Run: `python scripts/verify_lock_anchors.py`
Expected: `ROUTING: Closed` (exit 0).

- [ ] **Step 4: Grep sweep — no live OANDA code remains**

Run: `grep -rin "lib.oanda\|oanda_creds\|fetch_oanda_bars\|--from-oanda\|--panel oanda\|account_summary\|fetch_candles" --include=*.py . | grep -v "lab/analysis/"`
Expected: empty (only frozen `lab/analysis/oanda_stage1` banners + closed-Q bodies remain, which are excluded).

Run: `grep -rin "mc_anchor_oanda\|OANDA_PANELS\|requires_oanda\|test_oanda_anchor" --include=*.py --include=*.toml .`
Expected: empty (no live reference to the removed constructs).

- [ ] **Step 5: Report + skill-file handoff list**

Summarize: suite green (note skips), boundaries clean, manifests consistent, verifier Closed, grep sweep clean, no re-MC. Then hand the operator the **8 cloud-synced skill files** needing skill-authoring-path edits (on-disk edits don't persist, per `feedback_skill_amendments_via_authoring_path`):
- `.claude/skills/fxify-challenge/SKILL.md`
- `.claude/skills/trade-csv-reconcile/SKILL.md` + `references/baselines.md` + `scripts/reconcile.py`
- `.claude/skills/inqhiori/SKILL.md`
- `.claude/skills/live-execution-journal/SKILL.md` + `scripts/journal_review.py`
- `.claude/skills/code-defect-debugging/SKILL.md`
Each: drop OANDA from canonical-feed lists / two-tier-rule prose; keep historical baseline rows labeled archival.

---

## Self-Review

**Spec coverage:** Bucket (i) DELETE → Task 1. Bucket (ii) REMOVE WIRING → Task 2 (atomic). Bucket (iii) FREEZE → Task 3. Bucket (iv) LEAVE → no task (correct — REPO_MAP/operational_rules historical rows explicitly left in Tasks 2/5). Bucket (v) METHODOLOGY/MEMORY → Tasks 2 (CLAUDE.md prose), 5 (operational_rules), 7 (memory). Consequence edits → Task 4. Governance → Task 6. Verification gate (spec §7) → Tasks 0 + 8. Skill files (spec §6 out-of-scope) → Task 8 handoff. Gold-gate re-source (spec §6) → noted as operator follow-up (Task 6 SESSIONS + ADR §6). All covered.

**Placeholder scan:** ADR prose (Task 6) is authored via brief-authoring with concrete required-content bullets. All edits show verbatim old→new or precise construct + replacement. No TBD/TODO. The two "read the file then apply" steps (Task 2 Step 5.4 OANDA-baseline test cases; Task 5 Step 3.1 operational_rules two-tier statement) are bounded reads with an explicit decision rule, not open-ended placeholders.

**Type/consistency:** `PANELS_BY_BROKER` becomes `{"pepperstone": ...}` consistently across portfolio_mc (Step 1.4), the `['pepperstone']` assertion (Step 7), and verify_lock_anchors loops (Step 4.6–4.8). `parse_*` functions return `{"pepperstone": ...}` consistently after Step 4.3–4.5. `requires_oanda`/`OANDA_PANELS`/`oanda_result`/`test_oanda_anchor` all removed together (Task 2 Step 3) and grep-verified absent (Task 8 Step 4). The atomic-commit rationale (test import coupling + verifier Action coupling) is honored by bundling all six files in Task 2.
