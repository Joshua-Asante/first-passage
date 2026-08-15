# Design spec — Retire Dukascopy; broker-feed BAR EXPORT v0.1 as canonical bar producer

**Status:** `DRAFT — pending operator review`
**Date:** 2026-06-17
**Authors:** Joshua (decision) + Claude Code (design, this session)
**Type:** design spec (engineering + governance). The governance decision is recorded separately as `docs/adr/2026-06-17-dukascopy-retirement.md` (an implementation deliverable, §2).
**Supersedes / dispositions:** ADR `2026-06-12-tv-csv-canonical-feed-policy.md` §2.3 + §4 Forbidden-move #3 (the "tooling retained, not deleted" clause); ADR `2026-06-12-rnd-feed-instrument-class-split.md` (PROPOSED → Withdrawn/Superseded); closes Q-FEED-1 as `RESOLVED-BY-RETIREMENT`.
**Verification provenance:** two parallel 6-dimension audits this session (import footprint, boundary safety, test coupling, doc references, manifest/CI, producer correctness), validated against the real on-disk Q-FEED-1 bar-export samples.

---

## §0 — Rule 0 reads (production-source verification, this session)

Files read before authoring (file:line cited where load-bearing):

- `core/lib/dukascopy.py` — the adapter to delete: bi5-per-UTC-hour tick fetch → OHLCV; mapped point factors; closed-market 5xx skip+count; cross-feed parity caveat in its own docstring.
- `lab/validation/sweep/feed_loader.py:42,45,58,101` — the **feed-agnostic consumer that STAYS**: `REQUIRED_COLUMNS=("time","open","high","low","close")`, `DEFAULT_BAR_DIR=core/data/bar_data`, parses `time` as ISO-8601 UTC. Doesn't care which feed produced the bars.
- `lab/archive/feed_divergence_2026-06/_lib.py:29-35,37-42,111-201` — the decoder: `SIGNAL_PIPE_RE`/`COMMENT_RE`, `PRICE_COL`, `decode_bar_signal`, `price_tolerance`, `_trade_id_column`, `parse_tv_bar_export`. Imports only `re/numpy/pandas/pathlib/dataclasses` — **no first-party imports** → core-safe.
- `lab/archive/feed_divergence_2026-06/parse_tv_export.py` — the lab CLI wrapper (outputs `.bars.csv` sibling).
- `lab/archive/feed_divergence_2026-06/BAR_EXPORT_v0.1.md` — the export mechanism + the ≤9,000-bar TV List-of-Trades cap.
- `core/tv_export_loader.py:31-38` — the precedent core sibling (trade-export loader); `PRICE_COL_BY_INSTRUMENT` map (USDJPY/XAUUSD/XAGUSD/US30USD/US30/NAS100 → price column). Imports `from lib.mvd import …` (core→core, legal).
- `scripts/check_boundaries.py:37,66,73,109-113,152` — import contract: `tests/` in `EXEMPT_PREFIXES`; `('core','core')` is a `LEGAL_EDGE`; `lib` under `core/` indexes as layer `core`.
- `scripts/check_data_manifests.py:29-34,61,66` — `MANIFEST_DIRS` is **non-recursive** `iterdir()` → the `bar_export/` subdir is **not hashed today**.
- `scripts/githooks/pre-commit:26` — staging regex `^core/data/(tv_exports|bar_data|external)/` → bar_export CSVs trip a **fail-closed** MISSING_MANIFEST until a manifest exists.
- `.github/workflows/manifest-check.yml` — format-only; allows empty manifests; **no dukascopy reference anywhere in CI/hooks**.
- `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md:30,43` — §2.3 retain tooling / §4 FM#3 don't-delete → **supersession target**.
- `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md:3,37,48,71` — PROPOSED, gated on Q-FEED-1; §3(A) rules out full deletion; §5 forbids re-proposing (A) without Q-FEED-1 evidence → **disposition target + the recorded-cost source**.
- `pyproject.toml:39,51` — `testpaths=['tests']` (lab/analysis never collected); `pythonpath` adds core/lab/ops so `from lib.mvd import` and flat `from bar_export_loader import` resolve.
- On-disk samples: `core/data/tv_exports/pepperstone/bar_export/{GBPUSD,US30,USDJPY}_M15_pep.csv` (raw input) + `*_M15_pep.bars.csv` (parsed output), dated 2026-06-12; **no `SHA256SUMS` in that dir**.

---

## §1 — Goal & non-goals

**Goal.** Remove Dukascopy entirely as a bar source and make the TradingView/Pepperstone **BAR EXPORT v0.1** comment-encoded export the canonical producer of `core/data/bar_data/<SYMBOL>_M15.csv`. Rationale (operator): interpretability of the analysis inputs and fidelity to the actual broker execution feed traded on FXIFY (Pepperstone-via-DXTrade/TV), rather than an independent near-equivalent feed.

**Non-goals (explicit, per operator scope decisions):**
1. Existing cached `core/data/bar_data/*.csv` keep their provenance as manifest-pinned historical artifacts (incl. the three `*_duka.csv` lines in `bar_data/SHA256SUMS`). Not re-exported, not deleted.
2. `scripts/fetch_oanda_bars.py` (OANDA — a different feed) is untouched.
3. Closed-investigation findings/records are not rewritten; only a frozen-artifact banner is added where a script imports the deleted module.

---

## §2 — Governance (load-bearing; do this honestly)

Retiring Dukascopy is an **operator override** of a PROPOSED ADR that explicitly ruled this action out. The new ADR `docs/adr/2026-06-17-dukascopy-retirement.md` (authored via the brief-authoring conventions: §0 Rule-0 reads, falsifier, forbidden moves, honest consequences) must:

1. **Supersede** `2026-06-12-tv-csv-canonical-feed-policy.md` §2.3 ("Tooling is retained, not deleted") and §4 Forbidden-move #3 ("Deleting the staging tooling as 'dead under policy'"). State plainly that the 5-day-old retention clause is reversed by operator decision.
2. **Disposition** `2026-06-12-rnd-feed-instrument-class-split.md` (PROPOSED) → **Withdrawn/Superseded**. Its entire premise — split R&D feeds by instrument class with Dukascopy serving FX/metals — dies when Dukascopy is retired. Its ratification was gated on Q-FEED-1, which now closes mooted.
3. **Close Q-FEED-1** (`docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md`, currently `OPEN — DRAFT`) as **`RESOLVED-BY-RETIREMENT / mooted`**: the cross-feed transfer-validity question dissolves once we consume the broker-feed bar export directly — there is no cross-feed transfer left to validate.
4. **Record the cost the prior ADR identified, and that the operator accepts it.** Per `rnd-feed-instrument-class-split` §3(A): full deletion removes the deep, programmatic, free FX/metals history channel; multi-year M15 panels feeding N≥100 / regime-robustness gates now require **manual, TV-plan-capped, multi-pass** exports (~9,000 bars/pass) instead of one programmatic pull. **Accepted mitigation:** the operator supplies multi-page exports on demand (the "if multiple pages are needed due to bar count, ask and it will be provided" path), which the new producer concatenates (§4). The residual cost is manual labor vs programmatic refresh — accepted on interpretability + broker-fidelity grounds.
5. **Falsifier / revert trigger for the new ADR:** if a pre-registered deep-history FX/metals gate (N≥100 or a regime-robustness half-panel split) cannot be assembled from operator-supplied bar exports within a working session, reopen the programmatic-feed question with that dated incident as the anchor (do not edit the falsifier in place — supersede).

> This section exists because silently overriding a ruled-out alternative is the exact failure the programme-audit discipline watches for ("methodology invoked to rationalize a decision already made"). The override is legitimate operator authority; it must be **recorded**, not buried.

---

## §3 — Architecture: producer swap, not a pipeline rebuild

The bar pipeline is `producer → core/data/bar_data/<SYMBOL>_M15.csv → load_bar_feed() → sweep/validation`. The consumer (`feed_loader.load_bar_feed`) is feed-agnostic and **unchanged**. We swap only the producer:

```
BEFORE:  Dukascopy bi5 ticks ── lib/dukascopy.fetch_candles ──▶ bar_data/<SYMBOL>_M15.csv
AFTER:   TV chart (Pepperstone) ── bar_export_v01.pine (local, gitignored)
           ──▶ TV List-of-Trades CSV  (core/data/tv_exports/pepperstone/bar_export/<SYMBOL>_M15_pep[.pageN].csv)
           ──▶ core.bar_export_loader.parse_bar_export ──▶ bar_data/<SYMBOL>_M15.csv
```

Round-trip validated against real bytes: `USDJPY_M15_pep.bars.csv` row decodes from `epoch_ms 1772409600000` → `2026-03-02T00:00:00Z`, header matches `feed_loader.REQUIRED_COLUMNS`, no timezone shift applied.

---

## §4 — New module `core/bar_export_loader.py`

Location: **`core/` root**, sibling to `tv_export_loader.py` (boundary-confirmed: layer `core`, may import `from lib.mvd import …` if needed). One clear purpose: decode BAR EXPORT v0.1 List-of-Trades CSV(s) → canonical OHLCV bar CSV.

**Promote (copy) the decode subset from `_lib.py`:** `decode_bar_signal`, `price_tolerance`, `_trade_id_column`, `parse_tv_bar_export`, `floor_m15_utc`, `SIGNAL_PIPE_RE`, `COMMENT_RE`. (`_lib.py` is **not** deleted — it stays frozen with the Q-FEED-1 dir banner because `measure_divergence.py` still uses its divergence helpers. The decode duplication is acceptable: `_lib.py` is frozen/unmaintained.)

**Public API:**
```python
def parse_bar_export(paths: str | Path | Sequence[str | Path], *, symbol: str) -> pd.DataFrame
    # Decode one or more List-of-Trades page CSVs → DataFrame[time, open, high, low, close, volume].
    # time is tz-aware UTC; the CLI/writer formats it ISO-8601 'Z'.

def write_bar_data(df, *, symbol, out_dir=core/data/bar_data) -> Path
    # Write canonical core/data/bar_data/<SYMBOL>_M15.csv (time ISO-8601 'Z', float OHLC, int volume).
```

**Design points (all verification-derived):**
1. **Shared PRICE_COL, single source of truth.** Import `PRICE_COL_BY_INSTRUMENT` from `core/tv_export_loader.py` (core→core, legal) rather than duplicating `_lib.PRICE_COL`. Extend the shared map to every symbol we export bars for. Confirmed needed: `USDJPY, GBPUSD, XAUUSD, XAGUSD, US30, US30USD, NAS100`. Research-pipeline additions (`USDCAD, USOIL` → `Price USD` inferred; `EURUSD` pending a real export sample) added as they mature. The map is both the decode contract (which price the cross-check reads) and the load contract (which Entry/Exit column exists) — a mismatch silently mis-loads, so keep it authoritative and shared. *(Note the coupling: `tv_export_loader` = trades, `bar_export_loader` = bars; both consume the same map — never fork it.)*
2. **Multi-page ingestion** (the operator's "pages due to bar count" path; TV caps List-of-Trades at ~9,000 bars). `parse_bar_export` accepts a list/glob of page CSVs: parse each via `parse_tv_bar_export`, concatenate, **dedup on bar-open** (`drop_duplicates(subset=bar_open, keep="last")` — prefer the later re-export), sort by bar-open. Handles overlapping page boundaries gracefully.
3. **Filename contract.** Input: `core/data/tv_exports/pepperstone/bar_export/<SYMBOL>_M15_pep[.pageN].csv` (raw List-of-Trades). Canonical output: `core/data/bar_data/<SYMBOL>_M15.csv` (what `feed_loader.DEFAULT_BAR_DIR` expects). **Retire the `.bars.csv` sibling-output convention** (the current lab default) — it wrote parsed bars next to the input, which is not the canonical location. The producer writes to `bar_data/`.
4. **Cross-check retained.** Entry `Price` == encoded `close` (process_orders_on_close) → raise on mismatch = TV-export format-drift detector. `epoch_ms` is authoritative over the CSV `Date and time` column (avoids chart-TZ ambiguity).
5. **Output schema** is `feed_loader.REQUIRED_COLUMNS`-compliant by construction (time ISO-8601 UTC `Z`, float OHLC, int volume) so `load_bar_feed` consumes it with zero changes.

---

## §5 — CLI / regeneration workflow

`scripts/parse_bar_export.py` (thin wrapper over the module):
```
python scripts/parse_bar_export.py --symbol USDJPY            # default in/out paths
python scripts/parse_bar_export.py --symbol USDJPY --pages a.csv b.csv   # multi-page
```
Standard operator workflow after a fresh TV export:
1. Drop `<SYMBOL>_M15_pep[.pageN].csv` into `core/data/tv_exports/pepperstone/bar_export/`.
2. `python scripts/parse_bar_export.py --symbol <SYMBOL>` → writes `core/data/bar_data/<SYMBOL>_M15.csv`.
3. `python scripts/check_data_manifests.py --regenerate --dry-run` then `--regenerate`.
4. Commit the input CSV(s) + `bar_data/<SYMBOL>_M15.csv` + both `SHA256SUMS` deltas **in one commit** (§8).

This mirrors the existing vendor-data integrity gate workflow in CLAUDE.md.

---

## §6 — Deletions (live code only)

- `core/lib/dukascopy.py` — the adapter.
- `tests/test_dukascopy.py` — its only test (verified: the **only** test importing the adapter; after deletion zero tests reference it).
- `lab/archive/feed_divergence_2026-06/fetch_duka_panels.py` — Q-FEED-1's Dukascopy-panel fetcher (`_lib`-independent of the decode subset; its question is mooted).

**NOT deleted:** `lab/archive/feed_divergence_2026-06/measure_divergence.py` (no Dukascopy import — verified) and `_lib.py` (frozen; still used by `measure_divergence.py`).

---

## §7 — Frozen-artifact banners (no deletion)

Add a one-line top-of-file banner to each closed-Q script that imports the deleted module (verified live-import sites, all in dirs with no `__init__.py`, none collected by pytest):

```python
# Dukascopy retired 2026-06-17 (docs/adr/2026-06-17-dukascopy-retirement.md) — frozen historical artifact; no longer runs.
```

- `lab/archive/noct_spx/fetch_panel.py:34`
- `lab/analysis/tom_spx/fetch_daily.py:35`
- `lab/archive/custodian_eurusd/fetch_panel.py:59`
- `lab/analysis/silver_regime_2026-06-10/dukascopy_runner_check.py:17`
- `lab/analysis/silver_regime_2026-06-10/dukascopy_feed_equiv.py:21`

Plus a one-line banner in `lab/archive/feed_divergence_2026-06/README.md` noting the dir is frozen post-retirement (its `fetch_duka_panels.py` was deleted; `measure_divergence.py`/`_lib.py` remain as the historical Q-FEED-1 record).

**Not bannered:** `lab/archive/usdcad_rdm/fetch_panel.py` — TV-only, never imported Dukascopy (verified).

---

## §8 — Manifest / integrity gate changes

1. **Add `core/data/tv_exports/pepperstone/bar_export` as its own `MANIFEST_DIRS` entry** in `scripts/check_data_manifests.py` (the checker is non-recursive, so the subdir is ungoverned today). This brings bar-export inputs under the M-9 hash gate, parity with `bar_data/`.
2. **Create `core/data/tv_exports/pepperstone/bar_export/SHA256SUMS`** via `--regenerate` (none exists). Required because the pre-commit hook regex already matches bar_export paths and **fails closed** (MISSING_MANIFEST) on the first staged bar_export CSV.
3. **Leave `bar_data/SHA256SUMS` `*_duka.csv` lines** (`GBPUSD_M15_duka.csv`, `USA30IDXUSD_M15_duka.csv`, `USDJPY_M15_duka.csv`) — out of scope (cached historical provenance).
4. No CI workflow or hook references Dukascopy (verified) — `.github/` and the Makefile need no edits for CI logic.
5. **Optional guard** (nice-to-have): a check that no `*_pep.csv` / `*.bars.csv` intermediate lands in `bar_data/` (the canonical dir), preventing accidental intermediate-file pollution. Can be a line in `check_data_manifests.py` or the pre-commit hook.

---

## §9 — Doc updates (live docs only; dated closed-Q records stay frozen)

| File | Change |
|---|---|
| `CLAUDE.md` — Strategy Reference / baselines + Public-clone posture | Replace the Dukascopy-feed-adapter framing; the public-clone/manifest section must **name `bar_export/`** and explain that `bar_data/` restoration for the Pepperstone feed now routes through the BAR EXPORT v0.1 producer (not Dukascopy). Keep the OANDA `fetch_oanda_bars.py` restore line (out of scope). |
| `REPO_MAP.md` | Add/adjust a "Data sources" note: `bar_data/` = TV/Pepperstone bar-export output (canonical) + historical `*_duka.csv`/`*_oanda.csv` (manifest-pinned, staging/historical); cross-link the retirement ADR. |
| `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` | Add a header note: §2.3 + §4#3 superseded by `2026-06-17-dukascopy-retirement.md` (do not edit §4 in place — annotate). |
| `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` | Status `Proposed` → `Withdrawn/Superseded`; change-history line citing the retirement ADR. |
| `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md` | Status `OPEN — DRAFT` → `CLOSED — RESOLVED-BY-RETIREMENT`; link the retirement ADR + closure record. |
| `docs/ltm/briefs/pre-registration/Q-FEED-1-verdict-preregistration.md` | Note the pre-registration is moot (Q-FEED-1 closed by retirement); leave frozen otherwise. |
| `docs/SESSIONS.md` | New reverse-chron entry (5 fields) for the retirement. |
| Memory: `reference_dukascopy_adapter.md` | Mark the adapter retired 2026-06-17 (or delete and replace with a bar-export-producer reference); update `MEMORY.md` index line. |
| Memory: `project_tv_csv_canonical_feed_policy.md`, `project_rnd_pipeline_state.md` | Note Dukascopy retired; bar-export #1 is the canonical bar producer; rnd-feed-class-split ADR withdrawn. |

**Leave as frozen history (dated closed-Q records):** `docs/rejected_candidates.md`, the `ops/instruments/*.md` historical lines, closed-Q `README.md`/`RESULTS.md`/`verdict.md`, and CC-handoff briefs. *Note:* `CC-HANDOFF-USDCAD-RDM-001`'s "Dukascopy canonical" line was already superseded by the 2026-06-12 TV-CSV ADR and its `fetch_panel.py` is TV-only — retirement makes the stale label fully moot; a one-line pointer to the retirement ADR is sufficient, it is **not** a code blocker.

---

## §10 — Tests

- **New `tests/test_bar_export_loader.py`** — port coverage from `tests/test_feed_divergence_parsing.py:31-65` (decode pipe + legacy-comment formats; `parse_bar_export` end-to-end cross-check; reject-on-price-mismatch), importing the canonical `from bar_export_loader import …` (pythonpath-resolved; `tests/` is boundary-exempt). Add: (a) multi-page concat+dedup test; (b) an integration round-trip `parse_bar_export → write_bar_data → feed_loader.load_bar_feed` confirming the format contract; (c) PRICE_COL coverage for the added symbols.
- **Keep `tests/test_feed_divergence_parsing.py`** as-is (still green against frozen `_lib.py`); it now tests the frozen historical decoder. No churn.
- Real-CSV-dependent cases skip-if-missing, per public-clone posture.

---

## §11 — Verification gate / acceptance

- `make validate` clean (params + data manifests + pine manifest), including the new `bar_export/` manifest entry.
- `python scripts/check_boundaries.py` clean — no broken `core/lib/dukascopy` imports; `core/bar_export_loader.py` passes the contract.
- `pytest tests/` green: `test_dukascopy.py` gone, `test_bar_export_loader.py` passing, no other test affected (verified: lab/analysis never collected).
- End-to-end: `parse_bar_export` on a real `*_pep.csv` → `bar_data/<SYMBOL>_M15.csv` → `load_bar_feed` produces a valid `BarFeed`; round-trip matches the committed `.bars.csv` bytes for the 3 existing symbols.
- `grep -rin dukascopy` returns only: the intentional frozen-artifact banners, dated closed-Q historical records, and the retirement ADR's supersession references. Zero live-code imports remain.
- ADR discipline: `python scripts/check_brief.py docs/adr/2026-06-17-dukascopy-retirement.md --type adr` passes.

---

## §12 — Implementation order (for the plan)

1. `core/bar_export_loader.py` + shared PRICE_COL refactor + `scripts/parse_bar_export.py`; `tests/test_bar_export_loader.py` (TDD).
2. Add `bar_export/` to `MANIFEST_DIRS`; regenerate the bar-export + bar_data manifests; commit data + manifests together.
3. Delete `core/lib/dukascopy.py`, `tests/test_dukascopy.py`, `fetch_duka_panels.py`; add the 6 banners.
4. Author `docs/adr/2026-06-17-dukascopy-retirement.md` (supersessions + Q-FEED-1 closure + recorded cost/falsifier); disposition the two 2026-06-12 ADRs + Q-FEED-1 brief.
5. Doc/memory updates (§9); `docs/SESSIONS.md` entry.
6. Run §11 verification gate; iterate to green.

---

## §13 — Open items / accepted risks

- **Deep-history FX/metals depth** (§2.4) — accepted cost; mitigated by operator-supplied multi-page exports; falsifier set if a pre-registered deep gate can't be assembled.
- **EURUSD price column** — unknown until a real EURUSD export sample exists; PRICE_COL entry deferred (not a blocker; no EURUSD bars needed yet).
- **`.bars.csv` legacy files on disk** — the 3 existing `*_M15_pep.bars.csv` in `bar_export/` predate this contract; decide in the plan whether to delete them (intermediate) or leave for audit. Recommendation: delete (redundant once `bar_data/<SYMBOL>_M15.csv` is canonical), or move under an `audit/` subdir excluded from `bar_data/`.
