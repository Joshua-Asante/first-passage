# ADR 2026-08-19 — Great Prune is not a GRAND Subtract

**Status:** `Accepted` — ratified by operator (JA) 2026-08-21. Gate independently re-verified this session: both target ADRs already carry their "not a Subtract" addenda (great-prune.md Addendum 2026-08-19; grand-tier ADR Addendum 2026-08-19 "Great Prune is not a Subtract"), and neither's §2/§4 decision text changed — the Gate condition was met at authoring; only this Status field lagged.
**Decision date:** 2026-08-19
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Layer:** methodology citation. **$0 / K=0.**

Decision: Do not cite [`2026-08-08-great-prune.md`](2026-08-08-great-prune.md) as an instance of GRAND pursuit-Subtract, and do not retcon it as The Algorithm's Delete worked example. Great Prune is a documentation-class retention test (keep-if R1–R5 on *parts*). GRAND Subtract removes *pursuits*. §2.4 forbids treating Subtract as D in any lower domain. One-line disambiguation addenda on both Accepted ADRs are authorized; they do not amend §2 / §4 decision text. Do not add a Great Prune sentence to `inqhiori-canon.md` §14 (labeled mirror of the GRAND ADR; the owner addendum is enough).

Grounds: [`N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`](../notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md) §4 Subtract ACTION. The notice's "neither cites the other" and its §10 "Expected: no hit" are already stale: GRAND L283 incident-cites "deleted at the Great Prune"; §0 L61–62 cites the `operational_rules.md` retention-test *mirror* (R5/R3 classification of this ADR), not an operator identification. Canon §14 still has zero "Great Prune" tokens; great-prune.md still has zero Algorithm / D-S-A / STRATEGIC / GRAND tokens. Lifecycle overlay at canon §14 L311 is a different gap (stage-5 ownership), already closed.

Reads: `docs/adr/2026-08-08-great-prune.md` @ `027a729` · `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` @ `027a729` (L61–62, L119–120, L144–146, L283) · `docs/methodology/inqhiori-canon.md` §2 L34–42 + §14 L288–311 @ `9ebc78e` · `docs/operational_rules.md` Rule 16 @ owner pointer to great-prune §2 · notice @ `a580191`

Gate: RESOLVED if both addenda say "not a Subtract" and neither ADR's §2 / §4 text changed. FALSIFIED if a later artifact cites Great Prune as a GRAND Subtract or as Algorithm-Delete precedent without a superseding record.

Boundary: Do not fold Subtract into Delete (GRAND §3 already rejected that). Do not reopen GRAND §3. Do not rewrite the retention test. Do not touch `dd_protection.py` / allocations / Pine.
