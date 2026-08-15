# Programme audit — post-de-scope claim alignment · **SPLIT 2026-08-05**

**Status:** `Split for navigability — content preserved and extended, not deleted.`
**Successor:** [`2026-08-05-claim-alignment/`](2026-08-05-claim-alignment/) — start at [`README.md`](2026-08-05-claim-alignment/README.md).
**Audit date:** 2026-08-05 · **Repo anchor:** `e031225` · **This file's original 1020-line text:** commit `06caf3a`.

---

This was the round-1 artifact of the post-de-scope claim-alignment audit — one document of 1020 lines, which is why it was split. The operator's stated problem was navigability: *"This is a long doc, we need to break this up into sections."*

**Its content lives at [`2026-08-05-claim-alignment/`](2026-08-05-claim-alignment/)**, restructured into nine files so a remediator can open exactly one and act from it: diagnostics, BLOCKERs, agent-facing, MISLEADING, COSMETIC, operator-judgement, follow-ups, and runnable hooks. **Nothing was dropped to shorten anything** — the split is a reorganization, and the section files are longer in total than this file was.

**Round 2 was integrated in the same pass.** After round 1 recorded which surfaces it had not swept, round 2 swept those seven — `.claude/`, `.cursor/`, `deploy/`, root docs + build files, `scripts/`, the `lab/analysis` RESULTS corpus, and specs/plans — raising 124 and confirming 110, of which **71 are agent-facing**. Both rounds carry their provenance per row. **Combined: 316 raised, 53 refuted, 250 confirmed.**

**Four items also moved after this file was written**, and the section set records them as settled rather than open: **B3** fixed (`d84c5e4`), **B2** fixed (`a818b3f`), **B1** fixed (`ae5ffe7`), **FU-1** ruled (`551d5c5`).

⚠ **One named exception to "content preserved":** round-1 finding **M45** (`lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md`) has no row in the section set and is owed one — recorded in the successor README §6 with its recovery path. Retrieve the original text with:

```bash
git show 06caf3a:docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md
```

**This stub is retained deliberately.** Inbound references to this path resolve to a pointer rather than a 404, and this repo tombstones — it does not silently remove.
