# Dense-1m lane — unpause review (Board packet)

**Status:** `OPEN — OWED-election`
**Authored:** 2026-08-15
**Closed:** N/A
**Mark:** none — this draft elects neither
**Authors:** Cursor (recorder) — operator reviews
**Parent:** [CON-5 closure](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) Branch A · [lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
**Loop:** Inquire-light Board packet — U0 / U1 / U2 unpaid. $0 · K=0 · no camp · no CON-6 · pause stands until a mark.
**Artifact path:** `docs/briefs/2026-08-15-dense1m-lane-unpause-review.md`

---

## §0 — Rule 0 reads (this session @ `9a701505`)

| Path | Anchor |
|---|---|
| [CON-5 closure](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) | `027a7295` 2026-08-14 |
| [temporal-selectivity ADR](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) | `027a7295` 2026-08-14 |
| [lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) | `027a7295` 2026-08-14 |
| [analogue-modality ADR](../adr/2026-08-15-analogue-modality-route-ruling.md) | `ab303d07` 2026-08-15 |
| [MSL-S7](closures/MSL-S7-closure-resolved-e1-hold.md) | `027a7295` 2026-08-14 |
| [ceremony-tiering](../adr/2026-08-08-adr-ceremony-tiering.md) | `91e6caad` 2026-08-15 |

**Amendment-first (sub-rule 10).** Pause owner is the CON-5 closure (Branch A elected 2026-08-12). A new packet is the exception: Trap #12 forbids amending a closed brief's §6; [MSL-S7](2026-08-14-msl-slate-generation-review.md) is the election-vehicle precedent. If the operator marks U1 or U2, a **full** ADR (ceremony limb 4 — doctrine) supersedes Branch A. This file does not flip the pause.

```
$ rg -n "OHLCV temporal-selectivity lane default" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
11,60,96,126: pause / Branch A text (owner)

$ rg -n "Q-TNEC-CON-6|mnq_tnec_con6" lab/CATALOG.md docs/briefs/INDEX.md
(empty)

$ test ! -d lab/analysis/c1/mnq_tnec_con6_2026-08
PASS
```

**Rule-8** (`dense 1m unpause` / `CON-6` / `temporal-selectivity` on `lab/CATALOG.md` + `docs/briefs/INDEX.md`):

```
# lab/CATALOG.md
cheap_falsifiers_2026-08 — HOLD (parent-side cheap falsifiers for TNEC/dense-1m)
mnq_con1_dense1m_stage0_2026-08 — archived FALSIFIED
# no con6 slug

# docs/briefs/INDEX.md
Q-TNEC-CON-5 row: lane default paused pending new modality / non-route-① thesis
# no CON-6 / unpause packet
```

`check_advisor_dedup.py --keywords "dense 1m unpause CON-6 temporal-selectivity lane Branch B"`: slug hit is CON-5's own Branch-B table (declined). No unpause packet. No `msl_s4` / CON-6 camp.

**Cheap falsifier (parent-side, generous):** a CON-6 brief or `mnq_tnec_con6_*` camp already on `origin/main` would make this packet a re-derivation. **Neither exists.** Analogue-modality already lifted a *different* class (no named entry geometry); that carve-out is not this unpause.

---

## §1 — Context

CON-5 Branch A paused the dense-1m **OHLCV temporal-selectivity / entry-geometry** default on 2026-08-12, pending a new modality or non-route-① thesis. Branch B (lane continue → CON-6) was declined the same day. The mechanical lane stop is **1/3 FALSIFIED** (CON-1 only; AMBIGUOUS does not increment). The pause is the operator election, not that stop-rule.

The 08-10 ADR already opened route ① for within-instrument temporal selectivity and named **one** unauthored successor: a causally-named, K-charged, once-per-session-class cell aimed at trade-count cost geometry. CON-3 / CON-4 / CON-5 then used first/session as a *cap on entry geometry* and still died on cost (gross/(4×RT) ≈ 0.73× / 0.27× / 0.11×). First/session alone is spent as a distinction.

[Analogue-modality](../adr/2026-08-15-analogue-modality-route-ruling.md) already lifted the pause **for no-named-entry-geometry analogues only**. `MNQ-ANALOGUE-1` died pre-G0 the same day. That ruling explicitly does **not** unpause θ-parameterised entry-geometry.

MSL E1 HOLD is untouched: no slate-4, no S2B revive. This packet is TNEC L4 only.

---

## §2 — Prior art / lineage

- [CON-1](closures/Q-MNQDTL-CON-1-closure-falsified.md) FALSIFIED · [CON-2](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) AMBIGUOUS (gross ~0.65× of 4×RT) · [CON-3](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md) / [CON-4](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) / [CON-5](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) AMBIGUOUS; CON-3→4 and CON-4→5 were Branch B continues; CON-5 elected A.
- [ADR 2026-08-10](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-B / §6 — route ① open under a priori + K-per-axis; intended successor unauthored *as a temporal-criterion-as-mechanism cell*, not as another geometry+first/session cap.
- [08-10 cost-geometry falsifier](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md) — stop width cannot rescue (0.02–0.10× the 4× bar); surviving lever is trade count (once/session needs ~3.3% of the ~170 pt oracle vs ~20% at CON-2's ~6/day).
- [MSL-S7](closures/MSL-S7-closure-resolved-e1-hold.md) — un-pause listed as something E1 does not license; S2B route still needs Board un-pause *or* a non-route-① thesis. This packet does not grant that for MSL.
- Eight consecutive zero-yield closes 2026-08-08→08-12 (CON-5 election record) vs SNAG 3.

---

## §3 — Question

**Symptom-only:** the OHLCV temporal-selectivity default is paused after four non-promotable cells, while the mechanical 3-FALSIFIED stop has not fired and a different class (analogue) already has a carve-out; what does a Board mark do to that pause before any CON-6 is named?

---

## §4 — Falsifiable hypothesis

**H:** this packet presents exactly three live elections (U0 KEEP / U1 ADMIT-ONE / U2 OPEN-DEFAULT) and does not itself flip the pause, author CON-6, lift E1, or revive S2B; a later operator mark of U0, U1, or U2 is the only close.

**Reject H if:** the pause is flipped in this draft; a CON-6 G0 or camp is authored here; E1 is treated as lifted; S2B is revived; U2 lands as a light notice instead of a full ADR; or CON-6 is a θ-retune / first/session-only / stop-width "rescue" of CON-1–5.
**Accept H if:** operator marks U0, U1, or U2 under §6.
**Ambiguous-hold if:** operator defers with a dated hold (pause stays; no CON-6).

---

## §5 — Forbidden moves (this packet’s output)

- **Elect in this draft** — Board owns U0/U1/U2.
- **Author CON-6 / scaffold `mnq_tnec_con6_*` / freeze a G0** — the packet licenses a *procedure*, not a mechanism.
- **Treat first/session as the cost-geometry distinction** — CON-3/4/5 already used it; gross stayed below 4×RT.
- **Re-open hold-time or stop-width** under “cost geometry” — mapped and re-killed 2026-08-10.
- **Relabel a geometry cell as analogue** — [analogue ADR](../adr/2026-08-15-analogue-modality-route-ruling.md) test is *absence* of named entry geometry.
- **Use the unpause to revive S2B or author slate-4** — E1 and the S2B re-proposal bar stand.
- **Cite FALSIFIED(yield) or the 3-FALSIFIED lane stop** — neither has fired (lane counter 1/3).
- **Cap / Pine / arming / CONFIRM peek on CON-5.**

---

## §6 — Gate (operator marks one)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (U0 KEEP) | Operator marks **U0** | `STOP` — Branch A stands; analogue carve-out unchanged; no CON-6 |
| `RESOLVED` (U1 ADMIT-ONE) — **recommended, not marked** | Operator marks **U1** | `INTEGRATE` — **full** ADR (limb 4) supersedes Branch A *for one Q-ID only*; pause stays the default; CON-6 may be scoped only after that ADR and only if §7 U1 bar is written in the CON-6 brief *before* cheap falsifier / G0 |
| `RESOLVED` (U2 OPEN-DEFAULT) | Operator marks **U2** | `INTEGRATE` — **full** ADR flips the lane default back to open; CON-6 still needs a new family + §7 distinction; this is the “just unpause” mark |
| `FALSIFIED` | Pause flipped here, CON-6 authored here, E1/S2B laundered, or U2 as light notice | `STOP` — repair the process defect |
| `AMBIGUOUS-HOLD` | Dated deferral | `ITERATE` — re-open this packet on the hold date; pause stays |

**This draft elects none.** U1/U2 ADRs are **not** authored here.

### U1 admission bar (frozen if U1 is marked; binds the later CON-6 brief)

A CON-6 brief may proceed only if **all** hold:

1. **New family** — distinct from CON-1 ES−NQ divergence, CON-2 compression-break, CON-3 HTF-native compression, CON-4 PDH/PDL through-break, CON-5 impulse-pullback-VWAP-reclaim, and every C1–C11 / MNQ DEAD row.
2. **Cost-geometry distinction stated in writing** that is **not** first/session-only, **not** stop-width, **not** a θ-retune of CON-1–5. The 08-10 intended shape (temporal criterion *is* the mechanism; once-per-session; aimed at trade-count) is admissible only if the brief argues why it is not CON-3/4/5's geometry+cap.
3. **Route ①** answered via [ADR 2026-08-10](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-B: criterion causally named a priori, every axis charges `K_intrinsic`, F2 guard live. Executed `instrument_profiles.py cell` paste; every `BINDING BAR` answered.
4. **Parent cheap falsifier** on `_mnq_1m.parquet` **before** G0. Fail ⇒ $0 kill, no Q-ID, pause remains default.
5. **Lane counter** stays 1/3 until a FALSIFIED; a third FALSIFIED still fires the lane-review packet (spec step 6).

### Evidence (numbers live on the closures; not re-derived)

| Cell | Verdict | gross/(4×RT) | Note |
|---|---|---|---|
| CON-1 | FALSIFIED | — | both arms CI < 0; counter **1/3** |
| CON-2 | AMBIGUOUS | ~0.65× | ~6/day; RT ate +0.90/+0.97 pt |
| CON-3 | AMBIGUOUS | ~0.73× | first/session; stop ~29 pt |
| CON-4 | AMBIGUOUS | ~0.27× | first/session; stop ~257 pt |
| CON-5 | AMBIGUOUS → A | ~0.11× | first/session; stop ~17.5 pt; Branch B declined |

---

## §7 — Procedure after a mark (not run in this draft)

- **U0.** Closure of this packet `RESOLVED` (U0). No ADR. Pause text unchanged.
- **U1.** Full ADR: Branch A superseded for one reserved Q-ID (`Q-TNEC-CON-6`); default stays paused; analogue carve-out restated. Then a separate CON-6 scoping brief walks lane steps 1+1a + U1 bar + cheap falsifier. G0 only on operator explore GO. Fail-closed: a failed door-check or cheap falsifier does **not** spend the reserved Q-ID on a retune.
- **U2.** Full ADR: default returns to open; CON-5 CONFIRM stays unread; CON-1–5 stay closed. Next cell is still CON-6 under the lane spec + a stated distinction. Higher laundering risk (catalogue continue at the same level) — that is why U1 is the recommended mark.

---

## §8 — Verdict pre-registration

No separate pre-reg file. §6 table frozen at this packet’s commit (MSL-S7 precedent). Trap #12: do not amend §6 to match a later mark.

---

## §10 — Audit hooks

```bash
test ! -d lab/analysis/c1/mnq_tnec_con6_2026-08
rg -n "OWED-election" docs/briefs/2026-08-15-dense1m-lane-unpause-review.md
rg -n "OHLCV temporal-selectivity lane default \\*\\*paused\\*\\*" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
# Expected until U1/U2 ADR: pause text still present; this packet still OWED-election
rg -n "Q-TNEC-CON-6" docs/briefs/INDEX.md lab/CATALOG.md || echo "no CON-6 yet"
```

---

## Verification

```bash
python3 scripts/check_brief.py docs/briefs/2026-08-15-dense1m-lane-unpause-review.md --type inquire
git log -1 --format='%h %cs' -- docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
rg -n "1/3" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
```
