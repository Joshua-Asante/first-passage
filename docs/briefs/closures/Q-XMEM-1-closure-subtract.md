# Q-XMEM-1 — CLOSURE: `CLOSED` / `SUBTRACT` (GSUB-2 c1, pursuit-level)

**Verdict:** `CLOSED` — GSUB-2 **SUBTRACT** at the GRAND-tier pursuit layer. **Not** a re-verdict of
the investigation's own measurement history — the 2026-08-15 `ASSISTIVE-ONLY` Limb B
re-measurement (recall@5 0.500 vs. `rg`'s 0.088, below the 0.70 promotion floor) stands exactly as
last recorded. This closure ends the *standing exploration* (whether the pursuit continues), not
the measured verdict on Limb B, and does not touch Limb A (Mem0 T0, never started) or Limb C
(local-embedder, "a live question, not authorized to build") beyond folding them into the same
pursuit-level stop.
**Closed:** PARKED 2026-07-16 (T0 never started) · park ratified 2026-08-09 (GSUB-1 Phase 3) ·
**SUBTRACT ratified 2026-08-19** (GSUB-2 Phase 3)
**Pre-registration / parent (Inquire brief):**
[`Q-XMEM-1-cross-surface-memory-sidecar-pilot.md`](../Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) —
architecture + §6 gate frozen 2026-07-16; retained as a ready-to-run design, not deleted
**Spend / K:** GSUB-2 $0 / K=0. Prior Limb B build spend (Mem0/FTS5 measurement work) is unaffected
and not re-litigated by this closure.
**Live effect:** none — a research-tooling pursuit, no `core/`, `ops/c1_rail/`, or
`ops/c1_signal_daemon/` touch (CRO's own independent GSUB-2 review confirmed this).
**Artifacts:** [`pursuit c1`](../../pursuits/c1-q-xmem-1.md) ·
[`GSUB-2 brief`](../GSUB-2-park-cohort-early-review.md) ·
[`GSUB-2 closure`](GSUB-2-closure-resolved-loadbearing.md) ·
[`Limb B RESULTS`](../../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md)

---

## 1. Verdict (against the recorded disposition path)

| Route | Trigger (as recorded) | Actual | Fired? |
|---|---|---|---|
| PARK → re-entry | a dated cross-surface-memory-invisibility incident | **Zero incidents** in the 34 days since the 2026-07-16 freeze | — |
| PARK → expiry-SUBTRACT (self-executing) | 2026-11-08, absent renewal | **Superseded** — an earlier, ratified GRAND review (GSUB-2) reached the same disposition ~80 days ahead of the scheduled expiry, on the identical "outside Survive bounds" test GSUB-1 itself used, re-applied on updated (longer) elapsed-idle evidence | ✓ (early, via GSUB-2) |

## 2. What the pre-registration predicted vs what happened

The original design (2026-07-16) framed T0 (Mem0 sidecar pilot) as the next step once triggered by
a dated incident. No incident occurred; T0 was never started; the pursuit sat dormant through one
full GRAND-tier PARK cycle (GSUB-1) and into a second early review (GSUB-2), at which point the
same permitted test that justified the original PARK — applied fresh, on updated evidence — tipped
the disposition to SUBTRACT rather than a second PARK renewal.

## 3. What this closure does NOT license

- Reading this as a negative verdict on cross-surface memory as a concept — the architecture stays
  retained, ready to run, contingent on a genuine incident occurring (re-entry armor, GRAND ADR
  §2.3).
- Reopening or re-scoring the `ASSISTIVE-ONLY` Limb B measurement.
- Reviving Limb A (Mem0) or Limb C (local-embedder) as separate, un-gated efforts — both remain
  subject to the same pursuit-level SUBTRACT and its re-entry armor.
- Deleting `scripts/repo_retrieve.py` or any Limb B artifact — the quarantine ruling
  ([`SESSIONS 2026-08-15d`](../../SESSIONS.md)) is untouched by this closure.

## 4. Defects found in the frozen brief (recorded, not repaired)

None specific to this Q — see the GSUB-2 closure for the one defect (c3 coverage-table gap) found
in the pass that produced this disposition.

## 5. Lesson candidates

None new — absorbed into GSUB-2's own lesson candidate (panel routing tables are testable claims).

---

## Iterate — loop exit

- **Verdict used:** `CLOSED` / GSUB-2 `SUBTRACT` (pursuit-level, early — via a re-applied permitted
  test, not an expired PARK)
- **Model update:** a PARK's own permitted test can be re-applied on updated elapsed-time evidence
  without waiting for the pre-registered expiry, provided the re-application is transparent about
  which test is firing and does not smuggle a new test in as if already permitted.
- **Next:** STOP
- **Routing:** STOP — c1 pursuit record carries re-entry armor (out-of-frame evidence + attached
  falsifier via ADR/governance channel, GRAND ADR §2.3).
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** a genuine dated cross-surface-memory-invisibility incident,
  using the falsifier already on record in the frozen 2026-07-16 design — per c1 pursuit record /
  ADR GRAND §2.3.
- **Board write:** none — STOP, nothing owed beyond this closure + the c1 pursuit record + the
  `docs/briefs/INDEX.md` row move (all filed same commit).
- **Registry:** n/a — a GRAND-tier pursuit-disposition close, not a rejected trading-strategy or
  signal-mechanism candidate; `docs/rejected_candidates.md` tracks strategy/mechanism rejections
  only (Rule 8 sub-rule 9 scope). The Q-XMEM-1 architecture itself is not rejected, only parked
  with re-entry armor — see "What this closure does NOT license" above.

## §10 audit-hook discharge

```bash
ls docs/briefs/closures/Q-XMEM-1-closure-subtract.md
rg -n 'SUBTRACT|Q-XMEM-1' docs/pursuits/c1-q-xmem-1.md docs/briefs/INDEX.md
python3 -X utf8 scripts/check_closure_disposition.py docs/briefs/closures/Q-XMEM-1-closure-subtract.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Architecture + §6 gate frozen; PARKED (T0 never started) | Claude Code |
| 2026-08-09 | PARK ratified (GSUB-1 Phase 3, c1) | Joshua |
| 2026-08-19 | SUBTRACT ratified (GSUB-2 Phase 3, c1) — closure authored | Joshua (ratification) + Claude Code (execution) |
