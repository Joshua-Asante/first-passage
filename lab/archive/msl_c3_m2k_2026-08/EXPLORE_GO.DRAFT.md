# EXPLORE_GO.DRAFT — unpaid template (paid token is gitignored EXPLORE_GO.md)

**Status:** template only. Explore scoring requires gitignored `EXPLORE_GO.md`
with a real panel sha and operator GO.

## Preconditions (all mandatory)

1. Operator explore GO citing
   [`PREREG_G0.md`](PREREG_G0.md) +
   [`docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md`](../../../../docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md).
2. Panel land (TV BAR EXPORT elected — no Databento pull / W4 estimate):
   `core/data/bar_data/M2K_M15.csv` pinned in `core/data/bar_data/SHA256SUMS`.
3. Paste `sha256` of the panel file below.

## Paid form (copy to `EXPLORE_GO.md` — gitignored)

```markdown
# EXPLORE_GO — paid

Operator: <name>
Date: <ISO date>
Panel path: core/data/bar_data/M2K_M15.csv
Panel sha256: <64-hex>
Source: core/data/tv_exports/cme/BAR_EXPORT_v0.2_CME_MINI_M2K1!_2026-08-13_14faf.csv
W4: TV elected (no Databento pull)
Citation: PREREG_G0.md + ADR 2026-08-13-msl-c3-k2-dual-axis-revive

I authorize IS-only explore scoring for MSL-C3-K2 under K_intrinsic=2.
CONFIRM remains unread.
```

Then:

```bash
python run_construct_g0.py --explore-go
```

## Still forbidden after explore GO

CONFIRM peek · Pine before delete/flip · Cap · arming · silent K=1
drop · θ-retune · estate K-ladder edits.
