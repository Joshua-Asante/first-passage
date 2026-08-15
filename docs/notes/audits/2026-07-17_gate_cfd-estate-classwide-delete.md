# Gate audit — cfd-estate-classwide-delete — 2026-07-17

**Trigger:** forbidden D-test caught (pre-application — no deletion executed)
**Loop context:** The Algorithm / Delete step on the CFD data estate, post CFD-venue retirement (operator-proposed 2026-07-17)

## What the gate did

- D-test proposed (implicit): "Is this datum CFD-specific / do its results fail to translate to futures?"
- Items it would have deleted: the entire `core/data/tv_exports/pepperstone/` CFD estate (incl. the 2026-05-24 panel-of-record + 2026-06-25 clean vintages), OANDA exports, CFD-era `bar_data/`.
- S compression: partition by dependency class (KEEP / TRIGGER-DATED / CANDIDATE-NOW) recorded in `docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md`.
- A index: per-file D-test table + `rg --no-ignore` consumer verification, so future prune decisions cost seconds.

## What went wrong (caught before application)

"Does not translate to futures" is the *hypothesis* Q-RAIL-1 F3 exists to test (per-candle parity vs CFD source), encoded as a relevance test — the Iran-Hormuz shape. The scope premise was also factually wrong: three live consumers bind the estate (F3 arbiter; `test_mc_anchors.py` `skipif`-on-missing pin, which dies **silently** on deletion; the 2026-08-08 regime-check/Call-1/D2 obligations). Additionally, the bytes are gitignored — no `git show` retrieval path exists, making this the repo's first *irreversible* Delete class.

## Criterion update

- Old D-test: "CFD-specific / doesn't translate" (class-wide).
- New D-test: venue-retirement-scoped deletion must first enumerate consumers-of-record — `skipif`-guarded tests, ACTIVE CATALOG studies, dated STATE obligations, open-brief citations — and may fire only per-file where that enumeration is empty. Class-wide deletion requires the named triggers (T1/T2) to discharge first.
- Permitted-list addition: "Is this file's consumer set empty across tests, ACTIVE lab studies, dated forward obligations, and open briefs (verified by `rg --no-ignore`, not memory)?"
- Standing caution: for gitignored vendor bytes, Delete is irreversible — the reversibility assumption behind "D is reversible by re-running the gate" does not hold; treat as operator-gated always.

## Cross-references

- Disposition: `docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md`
- Affected decisions: `docs/adr/2026-07-11-challenge-era-claims-rescope.md` ("retire, but do not over-retire"); Q-RAIL-1 F3; STATE 2026-08-08 board (D2)
