# ADR 2026-08-07 — W1: intraday-honest engine re-measure (method freeze + $0 re-run GO)

**Status:** `Accepted` — operator 2026-08-22. Method freeze stands. Class-S 0.50× honest-clock RESULTS landed; the other three decisions of record remain owed as measurement, not as a status gate. Still does **not** invent bust figures.
**Decision date:** 2026-08-07
**Authors:** Joshua (Posture-A direction) + Cursor (drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [SPEC S7](../spec/2026-08-07-loop-s7-repo-alignment-spec.md) · [alignment manifest](../notes/2026-08-07-posture-a-alignment-manifest.md) · [gate-stack audit §5.3 R1/R2](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) · [eval-lock fix ADR](2026-08-04-firm-rules-eval-lock-fix-applied.md)
**Layer:** measurement method + commission only. **$0 / K=0** — no arming, no invented MC numbers, no lock/allocation/`dd_protection`/Pine edit.

---

## §0 — Rule 0 reads (verified 2026-08-07)

| Source | Anchor | What it pins |
|---|---|---|
| `core/firm_rules.py` Tradeify/MFFU blocks | `dd_lock_offset_usd: 1_000_000.0` (08-04 fix) + RESIDUAL EOD-clock caveat | Default geometry is no-lock; bust figures remain **lower bounds** until intraday clock is used |
| Gate-stack audit §5.4 item 4 | 2026-08-03 | Highest-value cheap measurement: re-run four decisions of record with `intraday_low` + corrected offset |
| Alignment manifest W1 section | HEAD | Surfaces to annotate; monkeypatch restore-to-100 now **diverges** from production default |
| `lab/analysis/c1/c1_band_rescore_2026-07-24/run_band_rescore.py` | restore `= 100` in `finally` | Corrupt-on-re-run if executed against 08-04 defaults |

---

## §1 — Context

The 08-04 firm-rules fix made unreachable `dd_lock_offset_usd` the **default** for Tradeify/MFFU eval tiers. Historical Part-A / F3 / band-rescore figures were still computed on an **EOD** breach clock. The engine can thread an intraday low; published decisions of record have not been re-measured on that clock. Meanwhile several `lab/analysis/c1/*` harnesses still `finally:` restore `dd_lock_offset_usd = 100`, which would **re-inject the defect** into process memory after a corrected run.

---

## §2 — Decision

**Authorize** a single $0 / K=0 re-measure campaign that:

1. Uses the **intraday** breach clock (`intraday_low` threaded per survivor-scoring / MC path — same capability the audit names).
2. Leaves `dd_lock_offset_usd` at the production no-lock default (`1_000_000.0`); does **not** restore to `100`.
3. Re-runs these **four decisions of record** only (frozen seeds/sims/panels where the original study pinned them):
   - 2026-07-15 Class-S / §4 discharge pins (as later corrected)
   - 2026-07-22 eval-lock withdrawal / remc correction
   - 2026-07-24 50K-band re-score
   - 2026-08-02 realizable-book / band-quantization scoring
4. Publishes RESULTS with before/after deltas; **does not invent interim bust %** in this ADR or in orientation docs.

**Until RESULTS land:** every cited EOD-clock bust / clearer figure in CLAUDE.md, STATE, skills, and instrument ledgers is labeled **EOD-clock lower bound pending W1** — pointer only, linking this ADR.

**Harness hygiene (this PR):** dated comments + restore-to-**captured-original** (or skip restore when already at `UNREACHABLE`) on monkeypatch harnesses named in the alignment manifest. Science bodies stay; silent deletion declined. Gen-2 parity scaffold (`parity_gen2_2026-08/`) remains out of scope.

**Frozen survivor-scoring prereg:** not edited here (W4 owns freeze discipline).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Accept this ADR with invented new bust % | Fabricates science; audit forbids |
| Delete monkeypatch harnesses | Destroys reproducibility of historical campaigns |
| Skip re-run; only annotate | Leaves the highest-value cheap measurement uncommissioned |
| Edit frozen prereg bodies for G1 labels | Trap #12; close+reopen only |

---

## §4 — Falsifier

**H:** After Accept + RESULTS, orientation docs either (a) cite the new intraday-honest figures with provenance, or (b) keep the EOD lower-bound label until Accept.

**FALSIFIED if:** any orientation doc publishes a new bust % without a RESULTS path; or a harness restore-to-100 lands on `main` after this hygiene pass without a dated exception comment.

---

## §5 — Forbidden moves

- Inventing or hand-editing bust / clearer / boot-95th percentages in this ADR.
- Arming the rail, spending K, or changing locked sizing constants.
- Editing frozen survivor-scoring prereg bodies.
- Retiring science harnesses without a RESULTS tombstone.

---

## §6 — Gate

| Limb | Verdict |
|---|---|
| Method frozen + re-run authorized at $0 | **this ADR (`Accepted` 2026-08-22)** |
| Harness restore-to-100 hygiene + orientation scoping-notes | **landed with the W1 PR** |
| RESULTS — Class-S 0.50× full+halves | **MEASURED** — [`RESULTS_INTRADAY_W1`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md) |
| RESULTS — remaining three decisions of record | **owed** as measurement (not a status gate) |
| `firm_rules` RESIDUAL caveat Superseded-by | **owed** when the remaining RESULTS publish |

---

## §7 — Audit hooks

```bash
grep -n "pending W1\|EOD-clock lower bound" CLAUDE.md STATE.md
rg -n "dd_lock_offset_usd.*= *100|expect 100|OPEN-DEFECT" lab/analysis/c1 --glob "*.py"
grep -n "Status:" docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md
```

## Addendum 2026-08-22 — Operator Accept

**Status `Proposed` → `Accepted`.** Method freeze and the $0 re-run GO stand. Class-S 0.50× full+halves on the honest clock is MEASURED ([`RESULTS_INTRADAY_W1`](../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)). The other three decisions of record named in §2 remain owed as measurement. This flip does not invent or republish bust figures.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-07 | Initial authoring — `Proposed`; method freeze + $0 re-run GO | Joshua (Posture-A) + Cursor |
| 2026-08-22 | **Operator Accept.** Status `Proposed` → `Accepted`. Class-S 0.50× RESULTS already MEASURED; remaining three decisions still owed. | Joshua (Accept) + Cursor (record) |
