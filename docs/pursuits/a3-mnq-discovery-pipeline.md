# MNQ discovery pipeline (TNEC intake · Route A/B · CapFLOW · dense-1m/instrument/W1) — KEEP

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A2 — generate/validate candidate strategies for the MNQ discovery track
**Measure:** TNEC-1 intake gate throughput; per-campaign pre-registered gates (G0/G2/G3 etc.) firing as designed, PASS or FALSIFIED
**Survive bound:** near-daily operator sessions (the estate's most active lane); databento per-pull cost under the skill's cost-gate discipline
**Review date:** 2026-11-08 (co-scheduled with the quarterly programme audit)
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** [`TNEC-1`](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) ·
[`lab/CATALOG.md`](../../lab/CATALOG.md) `c1` theme

**~~Open concern~~ → RESOLVED 2026-08-09** by
[`ADR rejection-register topology`](../adr/2026-08-09-rejection-register-topology-and-bar-wiring.md).
The concern as recorded ("the SNAG register feed stopped 2026-08-03; repair authored, never
ratified") was directionally right but mis-diagnosed. Measured outcome: the mandated repair is now
**ratified** (D1); the kills were **not** unrecorded but routed to the instrument ledger, which is
the register the machine consult actually reads — now ruled canonical for per-direction
instrument-scoped rejections (D3), so the in-window mechanism kills are **discharged there, not
back-transcribed**; and the audit's "both stopping rules non-operative" is **half refuted** — the
domain bar is operative and blocking at a tier=always gate, while the per-direction feed has no
enforcement instrument (D4, dispatched). This pursuit stays KEEP.

**Source:** [`GSUB-1 inventory`](../briefs/GSUB-1-inventory-and-dispositions.md) row a3
