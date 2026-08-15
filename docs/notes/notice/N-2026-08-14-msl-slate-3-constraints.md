# NOTICE 2026-08-14 — MSL slate-3 constraints + mechanism-dry stop

**Notice ID:** N-2026-08-14-msl-slate-3-constraints
**Observed:** 2026-08-14
**Author:** Cursor (plan-elected sequence)
**Type:** Notice-phase. Constraints only; no card elected. $0 · K=0 · no camp.
**Status:** `GRADUATED` — slate-3 **BLOCKED** (mechanism-dry); [§7](../../briefs/2026-08-14-msl-slate-generation-review.md) **E1 HOLD** ([closure](../../briefs/closures/MSL-S7-closure-resolved-e1-hold.md))
**Trigger:** slate-2 exhausted; deaths **2/3**; fade region reopened without a mechanism.

---

## §0 — Anchors (this session @ `3942cb69`)

[plan](../../briefs/2026-08-12-msl-program-plan.md) `c203b34f` · [second slate](../../briefs/2026-08-13-msl-second-slate.md) `c203b34f` · [S2B closure](../../briefs/closures/MSL-S2B-closure-stage1-fail-route.md) `8a75ab43` · [`MCL.md`](../../../ops/instruments/MCL.md) 2026-08-10 INTAKE-DRY `5f7af2c3` · [implied-SR reopen](../../adr/2026-08-13-implied-sr-report-only-fade-reopen.md) `cc26ba3e` · [charter](../../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) `8290b895`.

**Rule-8** (`msl_s3` / `s3a` / `slate-3` on `lab/CATALOG.md` + `docs/briefs/INDEX.md`): **no matches.**

---

## §1 — Constraints (not a full §7 review)

1. **No index-futures continuation entry** (S2B route FAIL).
2. **No third MR-at-level rr≈1 card** (slate-1 C2/C1 FALSIFIED; C3 operator-kill).
3. **Non-index preferred; fade geometry is the open door.** Magdon-Ismail stays validation-not-calibration. Sprint lane stays closed.

---

## §2 — WHO attempt (zero data; fade × MCL)

| Candidate | Why not NEW |
|---|---|
| NY / overnight failed-extension fade | C2 + C3-K2 family; transfer barred |
| PDH/PDL failed-break reclaim on MCL | C1 + C3-K2 dead |
| Inverse of S2A (fade the pullback) | spike-fader / post-hoc of S2A FLIP |
| TAS / settlement / GSCI-roll | BE3 · SFX-1 · Q-MCLTAS-1 |
| EIA / carry / physical | H-FBEIA-1 · H-FCCARRY-1 · LIT-EIA-PHYS; &lt;2/day |
| PROPENG eject | DEAD |
| `CONFIG-B-MCL` as the WHO | geometry ≠ mechanism |
| Bare “stops get hunted” | ADR 2026-07-26 §2-A |

Implied-SR reopen restored the **region**, not a **flow family**. 2026-08-10 Gate 1 stands.

**Verdict:** no WHO without known-dead space. **Do not scaffold** `msl_s3a_*`.

---

## §3 — Routing

**BLOCKED — mechanism-dry.** Functional 3/3. [§7](../../briefs/2026-08-14-msl-slate-generation-review.md) **E1 HOLD**. CapFLOW queued. Magdon-Ismail B undecided.

---

## §10 — Audit hooks

```bash
test ! -d lab/analysis/c1/msl_s3a_mcl_2026-08
rg -n "slate-3 BLOCKED" docs/briefs/2026-08-12-msl-program-plan.md
rg -n "CLOSED-RESOLVED \\(E1 HOLD\\)" docs/briefs/2026-08-14-msl-slate-generation-review.md
```
