# ADR 2026-08-03 — Retire CFD-era `bar_data` panels + `tv_exports/candidates`

**Status:** `Accepted` — operator GO 2026-08-03 (keep-set A: retain frozen MYM/MNQ/6J; delete CFD bars + uncertified GBPUSD candidate tree).
**Decision date:** 2026-08-03

**Supersedes:** [`2026-08-02-pepperstone-feed-retirement.md`](2026-08-02-pepperstone-feed-retirement.md) in part — §2-F only: that KEEP covered *all* of `core/data/bar_data/`; this ADR narrows KEEP to the three CME micros (`6J_M15`, `MNQ_M15`, `MYM_M15`) and **DELETE**-s CFD / CFD-era panels from the checkout and the active `bar_data/SHA256SUMS`.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none

**Related:** Pepperstone data tombstone [`docs/ltm/notes/2026-08-02-pepperstone-data-tombstone.md`](../ltm/notes/2026-08-02-pepperstone-data-tombstone.md); this retirement's hash record [`docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`](../ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md); futures-first charter [`docs/adr/2026-08-03-claude-md-futures-refocus.md`](2026-08-03-claude-md-futures-refocus.md).

---

## §0 — Rule 0 reads (production source, verified 2026-08-03)

| Path | What it establishes |
|---|---|
| `scripts/check_data_manifests.py` `MANIFEST_DIRS` @ `a78745b` | Active contract is three dirs: `tv_exports/cme`, `bar_data`, `external`. Comment still claims full-`bar_data` KEEP per Pepperstone §2-F. |
| `core/data/bar_data/SHA256SUMS` (working tree) | 12 CSV rows: 3 CME micros + 9 CFD/CFD-era (`NAS100*`, `US30*`, `USDJPY*`, `XAUUSD*`, `XAGUSD`). |
| Disk keep-set | `MYM_M15.csv`, `MNQ_M15.csv`, `6J_M15.csv` (+ metas) present. |
| `core/data/tv_exports/candidates/concept-gbpusd-vbr-001/` | Only candidate tree; outside `MANIFEST_DIRS`; rank-cert unfinished / CATALOG RETIRED. |
| Offline backup | `C:/Users/joshu/backups/first-passage-bar-cfd-candidates-preretirement-2026-08-03/` — **9/9** CFD CSVs hash-match `SHA256SUMS`; candidates tree copied + inventoried. |
| Live feed | `core/data/tv_exports/cme/` remains canonical CME TV exports (incl. PARKED Aegis-6J / Guardian-MGC trade-lists). |

---

## §1 — Context

Pepperstone feed retirement (2026-08-02) deleted broker TV exports and the BAR_EXPORT producer inputs, but **kept** all of `bar_data/` as frozen derived panels. That KEEP was correct for the CME micros still used by recent research (MYM/MNQ; 6J for the PARKED Aegis lane). It left a CFD-era residue (`US30`, `NAS100`, `USDJPY`, `XAUUSD`, `XAGUSD`) whose venue is closed, whose producer cannot regenerate them, and whose live program does not load them.

Separately, `tv_exports/candidates/` held one uncertified FX concept (`concept-gbpusd-vbr-001`) outside the manifest contract — regenerable R&D scratch that never cleared rank-cert, not a standing program input.

**Decision driver (one sentence):** delete the CFD / rejected-candidate data the futures-first program no longer needs, while preserving the frozen CME micros and the live `cme/` feed.

---

## §2 — Decision

| Surface | Disposition |
|---|---|
| `bar_data/{NAS100USD,NAS100_M15,US30USD,US30_M15,USDJPY,USDJPY_M15,XAGUSD,XAUUSD,XAUUSD_M15}.csv` (+ CFD metas) | **DELETE** from checkout; strip from `bar_data/SHA256SUMS` |
| `bar_data/{6J,MNQ,MYM}_M15.csv` (+ metas) | **KEEP** — still in manifest; still **FROZEN** (producer dead) |
| `tv_exports/candidates/` (entire tree, incl. tracked JSON sidecars) | **DELETE** |
| `tv_exports/cme/` (incl. PARKED Aegis/Guardian CSVs) | **KEEP** unchanged |
| `external/` | **KEEP** unchanged (R7c RETAINED) |
| `MANIFEST_DIRS` | **unchanged** (still three dirs); `bar_data/SHA256SUMS` shrinks 12 → 3 rows |
| Folder layout | **flat** `bar_data/` (no nest) + local README stating CME-only FROZEN disposition |

Historical lab scripts that loaded deleted CFD / candidate paths become **unrunnable in-place**; that is accepted honesty, not a defect to re-point.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Wipe all of `bar_data/` (incl. MYM/MNQ/6J) | Operator chose keep-set A; micros still feed recent analysis and the PARKED 6J ledger. |
| Keep only MYM/MNQ (drop 6J) | Operator ruled keep 6J with the micros. |
| Nest under `bar_data/cme/` | Manifest hasher is non-recursive per dir; nesting forces contract churn for no cleanliness gain once CFD files are gone. |
| Also delete PARKED Aegis/Guardian CSVs under `cme/` | Out of scope — parked-lane historical record, not rejected-candidate residue. |

---

## §4 — Falsifier

**H:** No live decision after this retirement requires a deleted CFD `bar_data` panel or the GBPUSD candidate tree.

**Revert trigger (binary):** if within **90 days** a live rail / screen / §4 / lifecycle decision is blocked on a deleted basename that no CME / Databento substitute can supply → restore from the offline copy and re-admit via superseding ADR.

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | 90 days with no live decision blocked on deleted bytes | Retirement holds |
| `FALSIFIED` | Live decision blocked on a deleted CFD/candidate path | Restore from offline; superseding ADR |
| `AMBIGUOUS` | Historical reproduction only | Read-only restore; **no** re-admission to manifest |

**Not a falsifier:** an archived study becoming unreproducible in-place.

---

## §5 — Forbidden moves

1. Deleting `MYM_M15` / `MNQ_M15` / `6J_M15` under this ADR.
2. Deleting PARKED Aegis/Guardian (or other) trade-lists under `tv_exports/cme/`.
3. Destroying the offline rollback copy as part of this motion.
4. Inventing a CME bar regenerator / rewiring `parse_bar_export.py` without a separate producer ADR.
5. Re-pointing deleted CFD consumers to CME panels and calling the old study still runnable.

---

## §6 — Gate

**RESOLVED** when:

1. Offline backup hash-verified (9/9 CFD + candidates inventoried).
2. CFD / candidates bytes absent from checkout; keep-set present.
3. `python scripts/check_data_manifests.py --check` green with 3-row `bar_data/SHA256SUMS`.
4. LTM tombstone + this ADR landed; living docs (`PIPELINES`, `REPO_MAP`, `CLAUDE`, `check_data_manifests` comment, `bar_data/README`) describe futures-only frozen `bar_data`.

---

## §10 — Audit hooks

```bash
ls core/data/bar_data/*.csv
# expect only: 6J_M15.csv MNQ_M15.csv MYM_M15.csv

test ! -e core/data/tv_exports/candidates
python scripts/check_data_manifests.py --check
rg -n 'tv_exports/candidates|NAS100_M15|US30_M15|XAGUSD\.csv' PIPELINES.md REPO_MAP.md CLAUDE.md scripts/check_data_manifests.py
```
