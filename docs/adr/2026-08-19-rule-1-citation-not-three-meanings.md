# ADR 2026-08-19 — Rule 1 citation is one rule, not three; no gate script; no Anchor-family merge

**Status:** `Proposed`
**Decision date:** 2026-08-19
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** methodology citation. **$0 / K=0.**

Decision: (a) Do not rename. The [`regime_robustness_gate.md`](../methodology/regime_robustness_gate.md) "Rule 1 (partition-hypothesis permutation)" row is the 2026-04-24 *extension* of the same INQHIORI Rule 1 (small-cell variance prior), not a third numeral — expand the citation to the owner; keep the numeral. (b) Do not build `rule1_gate.py`. No file exists; the archive gated it on CFD-era USDJPY OHLC panel ingestion that never landed. Correct the "implementation deferred" pointer so it stops implying a pending script. Build only if a live n≤10 / partition investigation needs it. (c) Do not cross-wire [`mc_anchor_history.md`](../mc_anchor_history.md) and Rule 1 as siblings. Both say "don't over-read a number," but they are independent: Rule 1 is Investigate-phase noise-first on small cells; the MC file is a retired-calibration tombstone. Quintessentials **Anchor** is a third, GRAND-tier operator. Shared metaphor ≠ shared owner. Pointer-only edits authorized on the gate doc. Full `Rule N` prefixing stays with the 2026-08-08 conventions audit.

Grounds: [`N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`](../notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md) §4 Anchor ACTION (landed `a580191` / PR #50; absent at the `4a828c7` snapshot this session first read). Owner texts: Rule 1 archive L19 + L48–92; `mc_anchor_history.md` L3–5; gate L95/L198; Rule 2 ADR L26/§5.8; 2026-08-08 audit §5.

Reads: `docs/methodology/archive/notion/rule-1-small-cell-variance-prior.md` @ `027a729` · `docs/mc_anchor_history.md` @ `027a729` · `docs/methodology/regime_robustness_gate.md` @ `027a729` · `docs/adr/2026-06-16-rule-2-budget-before-acting.md` @ `d88e5f2` · `docs/methodology/inqhiori-canon.md` L247/L270 @ `9ebc78e` · `docs/notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md` §5 @ `937b9a2` · `find`: zero `rule1_gate.py`

Gate: RESOLVED if gate L95/L198 name the owner + extension and no longer say implementation is deferred. FALSIFIED if a later live small-cell investigation ships `rule1_gate.py` without a new record.

Boundary: Do not prefix-rename OPS/INQ/DBN Rule N ([2026-08-08 audit](../notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md) §5; Rule 2 ADR §5.8). Do not rewrite the Notion-verbatim Rule 1 archive. Do not quote 99.83/0.17/4.37 as live. Do not touch `dd_protection.py` / allocations / Pine.
