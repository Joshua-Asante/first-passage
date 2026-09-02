# `Q-FVGFLOW-1` — does the order book behave differently at bear-FVG near-edge touches on MNQ (scoping)

**Status:** `CLOSED — AMBIGUOUS-HOLD — VOID-POWER` (Phase 0 Step 1 executed same session,
2026-08-06, immediately after drafting). **The independent touch-event population is n=21,
confirmed by direct enumeration of the underlying FVG objects** — below every power floor this
estate has established for a between-event block-bootstrap diagnostic (n≥30 merged convention,
n≥50 MNQSR-1 reaction-limb convention). Per this brief's own §7 ordering (power gates before
admissibility — "no reason to resolve Avenue A for a probe that cannot be powered regardless"),
**Phase 0 Step 2 (the Avenue A admissibility ruling) is not reached.** $0 spent, no pull, no
manifest, K_intrinsic=0 unspent. Closure record: [`closures/Q-FVGFLOW-1-closure-ambiguous.md`](closures/Q-FVGFLOW-1-closure-ambiguous.md).
**Class:** Inquire-phase Pre-Q. Opens a structured investigation; does not itself open a probe.
**Authored:** 2026-08-06 · Cursor (Composer) / claude.ai (advisor) · operator-directed (F3 fork
elected from `Q-ICTNF-1` §7).
**Parent question:** `Q-ICTNF-1` (near-field SSL bear-FVG expression, Stage-0 STOP) — this brief
executes fork **F3** named in that brief's §7: *"Route 2 survivor-tied — order-flow / TBBO as
substrate on a named survivor mechanism (not blind `MNQFLOW-1`)."*
**Sub-questions opened:** none yet.
**Loop:** Inquire-phase Pre-Q — gated by Phase 0 admissibility + power, then (if both clear) by
the falsifiable hypothesis in §4.
**Artifact path:** `docs/briefs/rnd-pipeline/Q-FVGFLOW-1-fvg-edge-book-signature-scoping.md`

---

## §0 — Rule 0 reads (verified this session, 2026-08-06)

| Path | Anchor | What it grounds |
|---|---|---|
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md`](../../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md) | `be6b94e` 2026-08-05 | **N14 — the only prior L1/TBBO book-asymmetry measurement in the estate.** Difference **−0.009367** (session-block CI **[−0.013430, −0.005354]**), placebo \|.\| p95 **0.004166**, p_emp **0.000**, on **n=255** trigger events, **4,220,030 TBBO quotes**. Design shape this brief reuses: unconditional-on-outcome (FM-1 held), diagnostic/watchlist disposition, `K_intrinsic=0` |
| [`lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md`](../../../lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md) | `be6b94e` 2026-08-05 | Frozen construct N14 ran under — session/roll/RTH machinery, ToD-matched control sampling, session-block bootstrap 10,000 reps. This brief's §2 construct is a level-class substitution on the same machinery, not a redesign |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N14 | `87b0547` 2026-08-05 | N14's own caveat: **"level-proximity is NOT controlled"** — controls match ToD only, so N14 cannot say whether its tilt is ORB-specific or generic level microstructure. This brief's result, whichever way it lands, is the discriminator N14 names as owed |
| [`lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md`](../../../lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md) | `c66972f` 2026-08-04 | The object class: bear-FVG near edge. Median G **291 pt** above open (p25 141/p75 519), intraday touch rate **17.9%**, n=**117** eligible session-days, mean net **−21.6 pt** as a *trade*. This brief does not re-open the trade verdict (AMBIGUOUS-UNDERPOWERED/adverse, V5) — it asks a different, structure-only question about the book at the touch moment |
| [`lab/archive/mnq_fvg_draw_probe_2026-08-04/run_fvg_probe.py`](../../../lab/archive/mnq_fvg_draw_probe_2026-08-04/run_fvg_probe.py) L70-190 | `c66972f` 2026-08-04 | **Counting mechanics, and the object-level enumeration this brief ran (§0-B).** `fvgs: 54` distinct objects (`t0` = each object's registration bar, a stable id); `trades: 117` session-day rows (`DRAW_K=10`, an object stays eligible across up to 10 session-days until touched or expired). Grouping the 117 trade rows by `t0` on the pinned panel (same hash MNQFVG-1 asserts, `38e29862…`), executed this session: **54 objects total → 45 became eligible (had ≥1 trade row) → 21 were ever touched within their window.** This is a direct enumeration, not the `0.179 × 117 ≈ 21` estimate `Q-ICTNF-1` used — the two independently agree |
| [`lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md`](../../../lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md) L67 | `b160ab2` 2026-08-05 | **The MERGED, in-`main` power-floor convention this brief applies as primary:** "VOID-POWER if n_paired < 30 or n_level moments in the paired set < 50% of n_ORB moments" — a paired-touch-moment design, the same shape as this brief's construct |
| [`docs/briefs/rnd-pipeline/Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md`](Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md) §0-B | `5f08cd6` 2026-08-06 (merged to `main` via PR #662, same session as this brief's authoring) | Independently derived the same population from the same census: **n_near ≈ 0.179 × 117 ≈ 21**, and ruled that count power-dead **for a trade construct** against this class's own floors (n≥100 `Q-ICTEXP-1` / n≥150 `MNQFVG-1` V5). This brief inherits that arithmetic but asks whether a *microstructure diagnostic* (N14's shape, not a trade) has a different, lower floor — and states the floor it will actually apply in §0-B rather than assume one |
| [`docs/notes/2026-08-05-order-flow-probe-governance-question.md`](../../notes/2026-08-05-order-flow-probe-governance-question.md) §7 | `a7dde66` 2026-08-05 | **The RULING this brief's admissibility question must clear or distinguish from.** Avenue A §6's qualifying triple — depth-shape, not fill-trivial, **"survivor-tied … not blind discovery"** — is a shape requirement, "untouched by a $0 cost fact." The blind `MNQFLOW-1` probe failed limb 3 and its executed run was ruled a *recorded deviation, not retroactively ratified*. Re-proposal bar re-scoped to **blind** re-proposals only (ruling item 6) |
| [`docs/briefs/programs/2026-07-24-avenue-a-microstructure-scoping.md`](../programs/2026-07-24-avenue-a-microstructure-scoping.md) L76-90 | `b0427fd` 2026-08-05 | Avenue A §6's literal text: sanctions an MBP-10/TBBO pull naming a feature that "**improves or monitors `ORB-MNQ-1`** (or another admitted survivor), **not blind discovery**." No FVG-linked construct is named as an admitted survivor anywhere in this estate — see §1-admissibility below |
| [`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../../spec/2026-08-05-eval-mechanism-shape-screen.md) EM0 | `87b0547` 2026-08-05 | Catalogue-size K wall: **K=1–2 is the working budget**, K=4 closes the band at Cap 1.0. This brief is designed `K_intrinsic=0` (diagnostic, no outcome conditioning, N14's precedent) precisely to sit outside this wall — see §5 forbidden move on quietly becoming K-bound |
| `python scripts/instrument_profiles.py cell MNQ ict-liquidity` | this session, 2026-08-06 | **DEAD (2026-08-04)**, binding bar `index-intraday-ohlcv-directional-timing-2026-07-21`. This brief does not attempt to discharge that bar for a *trade* — it is a structural measurement, same class as N14, which the bar does not reach (N14 shipped under the same DEAD cell without reopening it) |

**Data / spend so far:** $0.00. No pull. No `register_search open`. All reads are of committed
artifacts and unmodified re-inspection of a script already on disk.

---

## §1 — Context & motivation

`Q-ICTNF-1` closed the session-scale, price-only expression of the D-layer bear-FVG draw at
Stage-0 STOP: the near-field touch population is thin (~21 events) and the parent panel is
already adverse (−21.6 pt/trade). Its §7 named the honest remainder — the draw itself is the one
confirmed *attractor* in an object class where pools are otherwise measured *anti*-attractors
three times over (N9). Whether that attraction shows up in the **order book itself**, not just in
price outcomes, is a question this estate has one working method for: N14's book-asymmetry
diagnostic at a level-touch moment, which returned a precisely-estimated, wrong-signed (for ORB)
result on the one level class it has been tried on. N14 explicitly flags that its own tilt could
be generic level microstructure rather than ORB-specific, and that discriminating the two needs
"its own PREREG + K + operator GO." This brief is that discriminator, aimed at a second level
class instead of a second ORB cut.

**Admissibility, named plainly, not assumed:** N14 was survivor-tied *by construction* — its
trigger moments *are* `ORB-MNQ-1`'s own triggers. A bear-FVG edge touch is not `ORB-MNQ-1`'s
trigger, and no FVG-linked construct holds admitted-survivor status anywhere in this estate. This
brief does **not** claim Avenue A's survivor-tie condition is satisfied. §7 Phase 0 makes
resolving that claim, one way or the other, the first executable step — before any TBBO byte is
pulled.

---

## §2 — Prior art / lineage

- `Q-ICTNF-1` (parent, merged `main` via PR #662) — Stage-0 STOP on the session-scale *price*
  expression; named this fork (F3) as the only non-laundering order-flow route remaining.
- `mnq_orb_flow_substrate_2026-08-05` (N14) — `RESOLVED`, the design template this brief reuses:
  L1/TBBO size asymmetry at a level-touch moment vs ToD-matched controls, session-block
  bootstrap, `K_intrinsic=0`, no outcome conditioning.
- `mnq_orderflow_probe_2026-08-04` (`MNQFLOW-1`) — `FALSIFIED` (V2), then ruled inadmissible as a
  *blind* probe (2026-08-05 governance ruling). Its re-proposal bar is scoped to blind
  re-proposals; this brief is not a re-proposal of that construct (different feature-conditioning:
  L1 asymmetry *at a named level-touch event*, not an unconditional next-minute regression) but
  is close enough in mechanism that §7 Phase 0 treats the distinction as something to state and
  defend, not assume.
- `mnq_fvg_draw_probe_2026-08-04` (`MNQFVG-1`) — `AMBIGUOUS-UNDERPOWERED` (V5), adverse. Supplies
  the object definition and the touch-event population this brief measures against. Its trade
  verdict is not reopened (§5 FM-1).
- `2026-08-05-order-flow-probe-governance-question.md` — the governance-scoping precedent this
  brief's own §7 Phase 0 follows: surface the admissibility question in writing, get an operator
  ruling, before running anything.

---

## §3 — Question (Q-FVGFLOW-1)

**Pre-Q gate test:** rephrased to symptom-only — does it name a fix? No; it asks what the book
does, not what to build.

**Q-FVGFLOW-1:** Does the observable order book (L1/TBBO size asymmetry) show a directional
signature at bear-FVG near-edge touch moments on MNQ that differs from time-of-day-matched
non-touch moments — and if so, in which direction relative to the touch (the book yielding toward
the draw, or leaning against it as N14 found at ORB boundaries)?

---

## §4 — Falsifiable hypothesis (H-FVGFLOW-1)

**H-FVGFLOW-1:** At the moment price first touches an active, untouched bear-FVG near edge, L1
size asymmetry signed toward the draw direction (long, per the RESOLVED D-layer draw) differs
from time-of-day-matched non-touch control moments — consistent with a book that yields toward a
level being drawn to, the opposite signature from N14's ORB-boundary result.

**Reject H-FVGFLOW-1 if:** the session-block bootstrap 95% CI on the signed difference straddles
zero, **or** the point estimate has the same sign as N14's (book leans against the touch, not
toward it) with a CI excluding zero — either result is informative and closes the question, it
does not merely fail to confirm.

**Accept H-FVGFLOW-1 if:** the CI excludes zero, the sign is toward the draw (positive, book
yielding), and it survives against the within-session label-shuffle placebo at p_emp < 0.05 (N14's
own certification standard).

**Ambiguous-hold if:** Phase 0 (§7) determines the independent touch-event population is below
the power floor stated in §0-B, in which case the brief closes `AMBIGUOUS-HOLD — VOID-POWER` at
$0 with no TBBO pull, re-test window tied to accumulation of new native-history bars (see §6).

---

## §0-B — Power floor, and Phase 0 Step 1 EXECUTED (2026-08-06, same session)

This estate's power-floor convention for a between-event block-bootstrap diagnostic: **n ≥ 30**
(merged, in-`main`: `mnq_orb_level_proximity_2026-08-05` PREREG §S7 VOID-POWER, `n_paired < 30`),
with a stricter **n ≥ 50** applied specifically to reaction-type limbs in the not-yet-merged
`MNQSR-1` study (merged `main` via PR #661, `PREREG.md` S9). N14 cleared either floor at n=255 events.

**Executed, not merely estimated:** Phase 0 Step 1 (§7) ran against the live, hash-verified panel
this session. Grouping `run_fvg_probe.py`'s 117 trade rows by their underlying FVG object id
(`t0`) gives **54 total FVG objects → 45 became eligible for a trade-day row → 21 were ever
touched within their `DRAW_K=10` window.** `Q-ICTNF-1`'s independent estimate (`0.179 × 117 ≈
21`, derived from the aggregate touch rate, not object enumeration) agrees exactly. **n=21 fails
both floors** (21 < 30 and 21 < 50).

**This is the full native-history population, not a windowed subset** — `MNQFVG-1`'s pinned panel
spans 2019-05-06 → 2026-08-04 (~8 years), and `DRAW_K=10` is the frozen construct's own object
lifetime, not a lookback choice this brief could widen without opening a fresh axis (FM-3).
**VOID-POWER fires. Phase 0 Step 2 (admissibility) is not reached** — see §7.

---

## §5 — Forbidden moves

- **FM-1 — Reopen `MNQFVG-1`'s trade verdict.** This brief measures book structure, never net P&L,
  win rate, or any outcome table on the touch events. Ruled out because it is the exact laundering
  shape the estate's F2 guard exists to block (a structural finding smuggled back in as an
  outcome-conditioned re-cut).
- **FM-2 — Proceed to Phase 1 (TBBO pull) without a written admissibility ruling.** Ruled out
  because Avenue A §6's survivor-tie condition is not self-evidently met (§1), and the 2026-08-05
  governance precedent is explicit that a $0 cost fact does not discharge a shape requirement. An
  instruction to "go ahead" without the distinction stated in front of the operator is not a
  sign-off — that is the exact failure the 2026-08-05 ruling corrected.
- **FM-3 — Widen the touch population by loosening the FVG object definition (radius, `drawK`,
  displacement threshold) to manufacture n≥50.** Ruled out: this is a swept construct parameter,
  which is a fresh K-bound axis and a researcher degree of freedom, not this frozen probe. If
  Phase 0 finds n<50, the honest close is AMBIGUOUS-HOLD-VOID-POWER, not a widened definition.
- **FM-4 — Treat a RESOLVED result as a license to build a trade construct.** This brief's
  `K_intrinsic=0` disposition (N14's precedent) means a positive result is a diagnostic finding,
  transferred to the DURABLE FINDINGS ledger — converting it into a gate, filter, or entry
  condition is a fresh, K-bound axis requiring its own PREREG (identical to N14's own stated
  boundary).
- **FM-5 — Condition on outcome.** No cell may compare "book at touches that later profited" vs
  "book at touches that later reversed." FM-1 discipline (unconditional-on-outcome) from N14
  carries over unmodified.
- **FM-6 — Any `core/`, lock, rail arming, Pine, or lifecycle edit.**

---

## §6 — Gate criteria (closure verdict)

Pre-registered before any TBBO data is pulled or any count beyond §0's committed-artifact reads is
run.

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | Phase 0 clears (n≥50 independent touch events **and** operator admissibility ruling obtained) **and** session-block bootstrap CI excludes zero, sign toward the draw, placebo p_emp < 0.05 | New durable finding on `ops/instruments/MNQ.md` (companion to N14); watchlist/tripwire disposition per FM-4; no strategy opened |
| `FALSIFIED` | Phase 0 clears **and** CI excludes zero with the sign matching N14 (book leans against), or CI straddles zero | New DEAD-list-adjacent structural finding; discharges N14's open level-proximity caveat either way (N14's tilt is confirmed ORB-specific if this brief's sign disagrees, or confirmed generic if it agrees) |
| `AMBIGUOUS-HOLD — VOID-POWER` | **FIRED 2026-08-06.** Phase 0 Step 1 found n=21 independent touch objects, below both the 30-floor (merged convention) and 50-floor (MNQSR-1 reaction convention) | Closed at $0, no pull, no manifest, K_intrinsic=0 unspent. Re-test window: re-count after the native panel accumulates enough additional history that the object-touch count crosses 30 — at the historical object-formation rate (54 objects / ~8 yr ≈ 6.75/yr, of which ~39% touch), that is **roughly 3+ more years of native history**, not a near-term re-test; stated explicitly here rather than implying an imminent retry |
| `AMBIGUOUS-HOLD — INADMISSIBLE` | Phase 0 admissibility ruling declines to extend Avenue A's survivor-tie condition to this construct, and the operator does not elect to widen the gate | Close at $0. Record as a second governance precedent alongside the 2026-08-05 ruling: N14's shape (K_intrinsic=0, unconditional, diagnostic) does not itself grant survivor-tie to a new level class — each level class needs its own admissibility answer |

---

## §7 — Execution plan

**Phase 0 — Admissibility + power (both gates, $0, no pull, before anything else):**

1. **Power count — EXECUTED 2026-08-06.** Ran `run_fvg_probe.py`'s object-level bookkeeping
   against the live, hash-verified panel already used by `MNQFVG-1`: **54 FVG objects total → 45
   eligible for a trade-day row → 21 ever touched** within their `DRAW_K=10` window, across the
   full native history (2019-05-06 → 2026-08-04). Against the n≥30 (merged) and n≥50 (MNQSR-1,
   merged PR #661) floors in §0-B: **21 < 30 < 50 — VOID-POWER fires under either convention.** Per this
   step's own pre-registered instruction ("if <50, close here — do not proceed to step 2"),
   **Phase 0 Step 2 and Phase 0 Step 3 are NOT executed.**
2. ~~**Admissibility ruling.**~~ **Not reached.** The admissibility question named in §1 (whether
   Avenue A's survivor-tie condition extends to a zero-K structural diagnostic on a second level
   class) stays genuinely open — this brief neither answers it nor needs to, since the power gate
   independently kills the probe. It remains available as a live question for a *future* proposal
   on this level class once the population crosses 30 (§6 re-test horizon), or for a differently
   powered level class today.
3. ~~**Cost dry-run.**~~ **Not reached** — no TBBO pull is proposed.

**Phase 1–3 — not reached.** No pull, no measurement, no verdict assertion beyond the
`AMBIGUOUS-HOLD — VOID-POWER` closure already recorded in §6.

**Phase 1 — Data pull (only if Phase 0 clears both gates + cost dry-run).** Pull TBBO for the
touch-event set + N14-style ToD-matched controls, same session/day scope discipline as N14 §S1–S2.

**Phase 2 — Measurement.** L1 size asymmetry at touch vs controls, session-block bootstrap 10,000
reps (N14's machinery, imported unmodified per FM discipline), within-session label-shuffle
placebo.

**Phase 3 — Verdict assertion.** Run §6 against the actual numbers; produce closure artifact.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

To be committed at `docs/briefs/pre-registration/Q-FVGFLOW-1-verdict-preregistration.md`,
containing the §6 table plus exact threshold numbers, **before Phase 1's TBBO pull runs** — not
before Phase 0, since Phase 0's own outputs (the power count, the admissibility ruling) are
themselves gating inputs to whether a pre-registration is ever written.

Pre-registration commit hash: `<populated at pre-registration commit time, after Phase 0 clears>`
Pre-registration date: `<TBD — after Phase 0>`

---

## §9 — Closure record format

- **If `RESOLVED` or `FALSIFIED`:** `docs/briefs/rnd-pipeline/closures/Q-FVGFLOW-1-closure-<verdict>.md` (no `recommendation.md` — this is `K_intrinsic=0`, diagnostic disposition per FM-4; nothing is promoted). New row on `ops/instruments/MNQ.md` DURABLE FINDINGS, cross-referencing N14.
- **If `AMBIGUOUS-HOLD — VOID-POWER` or `— INADMISSIBLE`:** `docs/briefs/rnd-pipeline/closures/Q-FVGFLOW-1-closure-ambiguous.md`, stating explicitly which gate failed, the exact count or ruling, and (for VOID-POWER) the honest re-test horizon computed in §6 rather than a vague "later." **Written: [`closures/Q-FVGFLOW-1-closure-ambiguous.md`](closures/Q-FVGFLOW-1-closure-ambiguous.md), 2026-08-06.**

---

## §10 — Audit hooks

```bash
# Phase-0 Step 1 — reproduce the object-level touch count ($0, no pull). EXECUTED 2026-08-06;
# expected output: "objects: 54 | eligible: 45 | touched: 21".
python - <<'PY'
import sys, collections
sys.path.insert(0, 'lab/archive/mnq_fvg_draw_probe_2026-08-04')
import run_fvg_probe as m
import hashlib
assert hashlib.sha256(m.DBN_PATH.read_bytes()).hexdigest() == m.DBN_SHA256
import databento as db
df = db.DBNStore.from_file(m.DBN_PATH).to_df()[["open", "high", "low", "close"]]
df = m._P.assign_sessions(df)
daily = m._P.session_daily(df)
sessions = list(daily.index)
roll = m._P.roll_dates(range(sessions[0].year, sessions[-1].year + 1))
censored = [s in roll for s in sessions]
highs = daily["high"].to_numpy()
fvgs = m.build_fvgs(daily, censored)
rth = m.build_rth_up(df)
trades = []
for d, s in enumerate(sessions):
    if censored[d] or s not in rth:
        continue
    anchor = rth[s]["anchor"]
    f = m.eligible_target(fvgs, highs, d, anchor)
    if f is None:
        continue
    g_pt = f["bot"] - anchor
    if g_pt < m.G_MIN_PT:
        continue
    gross = m.replay_target(rth[s], f["bot"])
    trades.append({"t0": f["t0"], "touched": bool(abs(gross - g_pt) < 1e-9)})
by_obj = collections.defaultdict(list)
for t in trades:
    by_obj[t["t0"]].append(t["touched"])
print("objects:", len(fvgs), "| eligible:", len(by_obj),
      "| touched:", sum(1 for rows in by_obj.values() if any(rows)))
PY

# Confirm §0 anchors still resolve:
git log -1 --format="%h %ad" --date=short -- lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md
git log -1 --format="%h %ad" --date=short -- lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md
git log -1 --format="%h %ad" --date=short -- docs/notes/2026-08-05-order-flow-probe-governance-question.md

# Confirm the ict-liquidity profile cell is still what §0 says it is:
python scripts/instrument_profiles.py cell MNQ ict-liquidity

# Confirm no manifest has been opened prematurely (expect no match until Phase 1):
ls discovery_manifests/ | grep -iE "fvgflow"

# Re-derive the n≥30 power floor citation (merged convention):
grep -n "VOID-POWER" lab/archive/mnq_orb_level_proximity_2026-08-05/PREREG.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/rnd-pipeline/Q-FVGFLOW-1-fvg-edge-book-signature-scoping.md --type inquire
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation) — see §10 block above

# Cross-reference verification
$ grep -nE "K_intrinsic ?= ?0" lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/RESULTS.md
# `Q-ICTNF-1` (PR #662) and `MNQSR-1` (PR #661) merged to `main` same session as this brief's
# authoring — plain working-tree grep now resolves both directly:
$ grep -n "0.179 × 117\|≈ 21" docs/briefs/rnd-pipeline/Q-ICTNF-1-nearfield-ssl-bear-fvg-scoping.md

# §8 pre-registration: NOT APPLICABLE. Phase 0 closed the brief before Phase 1; §8 is only
# committed if a future re-test (§6 re-test horizon) clears the power floor.
```

VOID-POWER firing at Phase 0 means §8 (pre-registration) is never reached and no
`Q-FVGFLOW-1-verdict-preregistration.md` file exists — this is the correct, not incomplete,
state for an `AMBIGUOUS-HOLD` closure at this gate.

---

## Pre-Lock Checklist (DRAFT briefs only)

**Not applicable — this brief closed at Phase 0 (`AMBIGUOUS-HOLD — VOID-POWER`) rather than
locking.** Retained below as the record of what was checked before Phase 0 ran, since the closure
happened same-session as authoring.

- [ ] All §0 paths read and anchored with commit hash
- [ ] §3 question passes the symptom-only rephrase test
- [ ] §4 hypothesis is genuinely falsifiable (binary triggers in §6)
- [ ] §5 forbidden moves are genuinely tempting, not strawmen — FM-2 and FM-3 in particular reflect
      real temptations (an operator "go ahead" without the distinction stated; loosening the FVG
      definition to fix an inconvenient power count)
- [ ] §6 gates have specific numerical triggers
- [ ] **Phase 0 Step 1 (power count) executed and its result stated in §0-B before Phase 0 Step 2
      (admissibility ruling) is sought** — no reason to spend operator attention on a ruling for a
      probe that cannot be powered
- [ ] §8 pre-registration committed BEFORE Phase 1 runs (not before Phase 0)
- [ ] §10 audit hooks are runnable commands
- [ ] Verification block executed and passing
