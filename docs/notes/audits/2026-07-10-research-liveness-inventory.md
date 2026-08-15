# Research liveness inventory — 2026-07-10

**Scope:** Phase 4 repository-noise review.
**Method:** inbound references, manifests/tests, decision status, C1–C4 deletion-ledger criteria.
**Rule:** uncertain code stays in place; historical evidence is never deleted.

## Inventory

| Path | Evidence | C1–C4 disposition | Action |
|---|---|---|---|
| `lab/analysis/oanda_stage1/` | The OANDA-retirement ADR explicitly freezes **and keeps** all eight files. The three Stage-1 scripts are **not runnable** after retirement: their retired ingestion/data dependencies and pre-monorepo `data/bar_data/*.csv` inputs were removed. With both layer roots present, `PYTHONPATH=lab;core python -m analysis.oanda_stage1.guardian_stage1` reaches the loader and fails on missing `data/bar_data/XAUUSD.csv`. Active `oil_carry` / `usdcad_rdm` consumers no longer depend on this tree. | C1 says retain the frozen historical artifacts. C2 still fails because the tree is cited by the retirement ADR and historical evidence chain, but not because it has live callers. C3 applies to provenance, not executable reproduction. C4 is tracked. | **KEEP as non-runnable historical evidence.** The reusable helper lives at `lab/research_utils/permutation.py`; the old module is compatibility-only for the frozen source tree. |
| `lab/analysis/noct_spx/CARD.md` | Archived 2026-07-11 (stub + `lab/archive/noct_spx/` body). `verdict.md` closes the concept FALSIFIED; the archive body is the reproducer and numeric evidence for `docs/rejected_candidates.md`. Still cited by the feed-divergence record, SPX500 feed-policy ADR, TOM research, methodology lessons, and the EURUSD custodian precedent. | C1 confirms the investigation is closed. C2 and C3 fail: inbound references are live and the directory is a closure evidence chain. C4 is tracked. | **KEEP (archived stub).** Closure alone is not permission to move evidence. |
| `lab/analysis/legacy/tom_spx/` | Layer A ran on the canonical Pepperstone feed on 2026-06-16 and is **RESOLVED-ABSENT** (Welch t=0.64, permutation p=0.2544, COVID concentration, half-sample sign reversal). Only the brief-reserved native Pine confirmation remains before formal DEAD closure. `test_verdict.py` still pins the frozen gate and `tom_test_spx500.pine` is hash-pinned. | C1 formal retirement is not complete while the reserved Pine confirmation remains. C2/C3 fail on that outstanding confirmation, the executable gate test, manifest, and ledger evidence. C4 includes locally protected Pine provenance. | **KEEP pending reserved Pine confirmation; do not describe Layer A as open or unrun.** |
| `lab/analysis/orb/orb_universe_2026-06-22/` | The base investigation produced a conditional NAS100 candidate and is cited by the NAS100 ORB admission ADR. Follow-up one-offs have closure/preregistration documents that link their exact harnesses and outputs (Friday, GEX, VIX term structure, T10Y3M, and gap follow-ups). Shared `orb_lib.py` and family-test machinery remain the reproducibility base. | No directory-wide C1 retirement. C2 and C3 fail for the shared harness and cited one-offs; moving selected scripts would break exact evidence links. C4 is tracked. | **KEEP.** Revisit only after the parent NAS100 ORB decision closes and a per-file reference map proves an orphan. |
| `lab/archive/noct_spx/fetch_panel.py` and `lab/analysis/tom_spx/fetch_daily.py` | Both depend on the retired Dukascopy route and are retained as historical/exploratory provenance. TOM's canonical Layer A is already resolved; its remaining confirmation is Pine-native. | Feed retirement is not equivalent to evidence retirement. C2/C3 fail on cited provenance, not current execution utility. | **KEEP with their owning investigations.** |

## Utility promotion

- Canonical reusable API: `lab/research_utils/permutation.py`.
- Active importers updated: `lab/archive/oil_carry/f1_mechanism.py` and
  `lab/archive/usdcad_rdm/gate.py`.
- Historical compatibility path retained:
  `lab/archive/oanda_stage1/permutation.py`.
- Contract coverage: `tests/test_research_permutation_utils.py`.

## Archival actions

No path conclusively met the standing archival criteria. Therefore this phase
made **no attic move, hard deletion, or deletion-ledger entry**. This is
intentional: the ledger requires an actual move/delete/ref-repair action, and a
speculative ledger row would misstate repository history.

## Deferred candidates

The closed ORB one-offs and `noct_spx` may become archival candidates after
their parent decisions/evidence links are consolidated. A future pass must
re-run basename-level inbound-reference checks, preserve outputs and retrieval
provenance, and append the deletion ledger in the same change as any move.
