# ADR 2026-08-13 — MSL slate-2 design box + S2A sequencing

**Status:** `Accepted` — operator election (P3.4 GO) 2026-08-13
**Decision date:** 2026-08-13
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Authors:** Joshua (election: "go straight to P3.4") + Cursor (recorder)
**Related:** [re-derivation](../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) · [second slate](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/programs/2026-08-13-msl-second-slate.md) · [charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) · [Magdon-Ismail RESULTS](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/mc/mc_mdd_closed_form_2026-08/RESULTS.md)
**Layer:** MSL hunting-region election only. **$0 / K=0.** No arming, no Pine, no `core/`, no gate/threshold change.
**Revision:** 2026-10-25 — rule consolidation D7 removed the slate-2 authoring and lane directives with the MSL channel's closure (ADR10-86, ADR10-88); prior decision at `91ccd984693d62c5c83ff3f428188dd47085633d`.

## Decision

Elected 2026-08-13: the [re-derivation](../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) §7 box for **slate 2**: `rr` ∈ [2, 3] · target WR 0.30–0.42 · `R` at the bust-≤3.0% **diffusion** frontier (provisional) · hard stop mandatory · k=1 · no pyramiding, with S2A (MCL) sequenced first, not waiting on Magdon-Ismail as a calibration, and the eval-sprint lane not opened. Slate 2 is exhausted (S2A FALSIFIED, S2B STAGE-1 FAIL) and the MSL channel closed 2026-10-07 ([ratification ADR](2026-08-12-msl-sourcing-channel-ratification.md), Addendum 2026-10-25), so the election directs no further MSL cards; the box geometry stays the reference other records cite.

## Grounds

Operator instruction 2026-08-13: go straight to P3.4 (S2-A campaign manager). Answers re-derivation §10 items 1 and 3 (re-point + author now) and item 2 as **S2A non-index first**. Slate-1 header stays the historical record of what slate 1 tested.

## Reads

[re-derivation](../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) @ `5dbf8129` · [second slate](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/docs/briefs/programs/2026-08-13-msl-second-slate.md) @ `dc67c164` · [Magdon-Ismail RESULTS](https://github.com/Joshua-Asante/first-passage-archive/blob/5d47b4dc5fd20da5e93edfed2f6eafd0d4a6ddd2/lab/analysis/mc/mc_mdd_closed_form_2026-08/RESULTS.md) @ HEAD — **MEASURED, validation only, not calibration** · [eval-sprint notice](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/notes/notice/N-2026-08-13-eval-sprint-lane-derivation.md) — **not elected**.

## Gate

RESOLVED when this ADR is Accepted and S2A Stage-0 may proceed under the elected box.

## Boundary

Do **not** loosen bust ≤ 3.0% or P(pass) ≥ 50%. Do not rewrite the first-slate header. Do not treat Magdon-Ismail validation as an `R_max` recalibration — every frontier dollar here stays the diffusion approximation until a separate calibration artifact exists.
