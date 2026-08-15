# `MNQFVG-1` — RESULTS: underpowered by the frozen floor, and adverse on every limb beneath it

**Status:** AMBIGUOUS-UNDERPOWERED — V5 fired (n=117 < 150), and the disclosure beneath the power floor is uniformly adverse: mean net −21.6 pt/trade (net/G −0.28), worse than 93.7% of random-session placebos at identical target geometry, annSR −0.32, both halves negative — the daily-scale 0.86-in-10-days draw collapses to an 18% within-session touch rate because eligible near edges sit a median 291 pt above the open; do not read V5 as "try again with more data"

**Date:** 2026-08-04 · **Pre-registration:** [`PREREG.md`](PREREG.md) — **frozen at `38a213d` before any
event count existed** (freeze commit precedes this file's; §10 hook 1).
**Cost:** **$0.00** · **K_intrinsic = 1 spent and banked** — manifest
[`mnqfvg_draw_probe.json`](lab/archive/../../../discovery_manifests/mnqfvg_draw_probe.json) closed (p = 0.937;
0 of 1 survives). `K_banked(MNQ)` **3 → 4** (disclosure).
**Harness:** [`run_fvg_probe.py`](run_fvg_probe.py) — archived `_ict_offline` mechanics and the
committed MNQPOOL-1 machinery **imported unmodified** · **9 hand-computed unit tests passing before
the runner read a real bar** · raw [`RESULTS.json`](RESULTS.json).

---

## 1. Verdict — every pre-registered route walked (precedence as frozen)

| § | Route | Frozen trigger | Actual | Fired? |
|---|---|---|---|---|
| **V5** | **`AMBIGUOUS-UNDERPOWERED`** | **n < 150** | **n = 117** | **✓ (precedence)** |
| V2 | `FALSIFIED` | mean ≤ 0 OR CI includes 0 | would ALSO have fired: mean **−21.6 pt**, CI [−56.7, +14.0] | (subordinate) |
| V4 | `AMBIGUOUS-CONFOUND` | mean ≤ placebo p95 | would ALSO have fired: −21.6 ≪ p95 +20.2 (p_emp **0.937**) | (subordinate) |
| V3 / V1 | — | — | not reached | ✗ |

**The honest compound reading, stated so V5 cannot be spun:** the probe is underpowered *and* every
substantive limb is adverse. More sessions would raise n, not rescue a **negative** point estimate
sitting below 93.7% of its own placebo distribution. The construct is *worse than random sessions* —
consistent with §4's named mechanism: bear-FVG-active sessions follow down-displacement, and a
stop-free long into recent weakness bleeds on the E1 exit exactly on the days the draw fails to
complete intraday (82% of them).

## 2. The census is again the finding — dilution, second verse

| | value |
|---|---|
| Sessions / valid / bear FVGs / trades | 1,875 / 1,667 / **54** / **117** |
| **Median G (near edge above the 09:30 anchor)** | **291 pt** (p25 141 / p75 519) |
| Intraday touch rate (vs 0.86-in-10-days daily-scale) | **17.9%** |
| Mean net / net-per-G | **−21.6 pt** / **−0.285** |
| Placebo mean / p95 / p_emp | −0.20 pt / +20.2 pt / **0.937** |
| Halves | H1 −6.8 pt (n=66) · H2 **−40.9 pt** (n=51) |
| FVG count cross-check | 54 on this session-daily panel vs **52 blocks** on the TV daily panel — the registries agree |

**Why the distance is structural, not bad luck:** a bear FVG registers at the *bottom* of a
displacement down-move — `bot = high[t0]` is the top of the third bar of a plunge. By the next
morning's open, price sits far below it (median 291 pt). The daily-scale draw (0.86 within 10
days) is real but mostly completes on *later, multi-day* recoveries — only 18% of it is reachable
inside one 09:30→16:00 window. **T5 (flat-by-16:00) and the draw's native horizon are structurally
mismatched**, which is exactly the wall V5's pre-registered disposition names.

## 3. What the pre-registration predicted vs what happened

§4 named V2 most likely, V5 possible (from the 52-block count), and **dilution as the
MNQPOOL-repeating alternative kill** — dilution is precisely what the census shows. The
"least-null-expected" clause (fresh, near targets) was **wrong in its geometry premise**: FVG
near edges are fresh in *time* but not near in *price*; recency ≠ proximity after a displacement
move. Recorded as the second same-day instance of the same lesson, now measured from both sides:
**MNQPOOL-1's avoided objects recede; MNQFVG-1's consumed objects are born far away. Both ICT
object classes put their levels outside intraday reach on MNQ.**

## 4. What this does NOT establish

1. **The D-layer draw itself is untouched** — NQ's 0.8630 RESOLVED cell is a 10-day-horizon rate
   fact and remains true; this measures one *session-scale* expression of it.
2. **No multi-day expression is measured.** A construct holding across sessions toward the edge
   would need overnight/weekend holds (`weekend_holds: False` caps it) and its own K — named, not
   opened, and NOT recommended without an operator-level rethink of the T5 constraint.
3. **The 1m-scale FVG mid-retrace (W3's 59%) remains unexpressed and unlicensed** — it has no
   measured null (FM-1 barred it here).

## 5. Iterate — loop exit

- **Verdict used:** `AMBIGUOUS-UNDERPOWERED` (V5, frozen precedence), with the full adverse
  disclosure above.
- **Model update:** the two same-day probes now bracket the ICT object family from both sides:
  level-avoidance objects sit too far below (572 pt) and displacement-gap objects too far above
  (291 pt) for any 09:30→16:00 expression on MNQ. **The family's structural facts live at the
  daily horizon; the venue constraint (flat-by-16:00) lives at the session horizon; the mismatch
  is the binding wall, not edge existence.**
- **Next:** STOP.
- **Entry packet:** n/a (STOP). For the record: per PREREG §3/FM-6, **route-1 arguments on
  `MNQ × ict-liquidity` are now presumptively exhausted** — two same-class, same-day probes
  (FALSIFIED + UNDERPOWERED-adverse). A third probe in this class needs operator review and should
  arrive via **route 2** (order-flow modality — the Databento subscription's MBP-10/TBBO
  recent-window entitlements, cost-dry-run-gated) or route 3, not another OHLCV expression.
- **Stop rule / re-proposal bar:** a session-scale ICT-object construct on MNQ re-proposes only
  with evidence its objects sit **within intraday reach** (the two measured distance
  distributions are the bar to clear); a multi-day expression re-proposes only after the T5
  constraint question is taken to the operator explicitly.
- **Board write:** MNQ.md DEAD-list row + session log + **profile-cell correction** (the
  `ict-liquidity` cell now carries both probes — the consult's "untested" line was stale);
  STATE decision-index line; SESSIONS entry; CATALOG regen. All landed with this commit.

## 6. Reproduce

```bash
cd lab/archive/mnq_fvg_draw_probe_2026-08-04
python -m pytest test_run_fvg_probe.py -q      # 9 passed, before any real bar
python run_fvg_probe.py --census               # Step-0 census
python run_fvg_probe.py                        # full run -> RESULTS.json
```

Deterministic (seed 20260804). Data: the same pinned `MNQ.v.0` 1m panel (sha256 `38e29862…`,
asserted at load). Mechanics imported from the archived `_ict_offline` and the committed
MNQPOOL-1 harness — nothing re-derived.
