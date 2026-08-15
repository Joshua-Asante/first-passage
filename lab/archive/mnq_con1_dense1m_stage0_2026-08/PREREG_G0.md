# Q-MNQDTL-CON-1 — Stage-0 PREREG (G0) — dense 1m ES/NQ divergence construct

**Status:** `CLOSED FALSIFIED` 2026-08-09 — ENTRY named 2026-08-08; explore GO
(default full panel) scored both arms `FALSIFIED`. Cap seat not claimed.
**Date:** 2026-08-08 (freeze) / 2026-08-09 (explore)
**Parent brief:** [`docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md`](lab/archive/../../../docs/briefs/Q-MNQDTL-CON-1-dense-1m-em-construct-scoping.md)
**Intake gate:** [`TNEC-1`](lab/archive/../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) (`RATIFIED`) — N-ACT…N-SIZE; MNQDTL D1/D2 preferences only.
**Universe unlock:** [`Q-MNQSEL-2` RESOLVED](lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) — dense RTH 1m @ G=10.
**`K_intrinsic = 1`**. Cap 1.0 → DSR floor **0.650**.
**Cost so far:** **$0.0000** (MNQ + ES `ohlcv-1m` continuous cache reuse).

**FROZEN ON THIS FILE'S INTRODUCING COMMIT.** Zero candidate-path outcomes have been
computed at freeze time (cheap falsifier = arithmetic bars + named-entry / sign check
only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).

---

## Amendment log

- **2026-08-08 — G0 FROZEN with named ENTRY.** Operator supplied ES−NQ 5m log-return
  divergence vs 20-session median-|d| threshold (relative contrarian on MNQ). Geometry
  + scoring limbs below. Explore GO unpaid. No variants; sign not inverted.
- **2026-08-09 — Explore harness wired (still GO-gated).** `run_construct_g0.py --explore-go`
  scores MNQ+ES join when `EXPLORE_GO.md` is present; refuses otherwise. No path PnL
  computed at this amendment.

---

## §0 — Rule-0 / cheap falsifier (parent-side, 2026-08-08)

| Check | Result |
|---|---|
| MNQ panel | `~/.databento_cache/ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn` (`MNQ.v.0`) — MNQSEL-2 panel |
| ES panel | `~/.databento_cache/ohlcv-1m_continuous_17b6c454408be685.dbn` (`ES.v.0`) — cache hit, $0 |
| EM1 arithmetic | Pred. move ≥ **5.41 pt** · WR bar **0.7705** at G=10 / RT=1.41 for 0.40R disclosure |
| N-EDGE arithmetic | Pred. move ≥ **1.41 pt** · WR bar **0.5705** for net R > 0 |
| Prior-art effect | **None measured for this exact cell** → arithmetic bars disclosed; **not** `FALSIFIED-BY-ARITHMETIC` (no effect to compare; bar/2 rule idle) |
| Sign | Relative contrarian frozen (LONG when ES−NQ ≥ +θ); invert → own-instrument momentum → C5-dead (D5-RECOST-1) — **forbidden** |
| ENTRY | Named, causal at bar open, ≠ oracle — clears "cannot name entry" Stage-0 falsifier |

**Verdict:** `CHEAP_FALSIFIER_OK` — licenses G0 freeze + harness scaffold; **not** a path-PnL /
SHAPE-CLEAR result. Explore remains blocked pending operator GO.

---

## §1 — Universe and trade geometry

| Element | Frozen value |
|---|---|
| Clocks | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET** 1m bar opens |
| Trade instrument | `MNQ.v.0` continuous |
| Feature instrument | `ES.v.0` continuous (joined on bar-open epoch; intersection coverage) |
| Roll exclusion | `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec) — same helper as MNQSEL-2 |
| Stop | **G = 10.0 pt** hard adverse; same-bar stop wins |
| Exit | **Session-flat** at last in-session RTH bar close (elected). No 1R take-profit in this cell |
| Cost | Tradeify RT **1.41 pt**; `R = (pts − 1.41) / 10` |
| Independence | EM3 — one position at a time; ignore further signals while in a trade; no pyramid/scale-in |
| Arms | Long and short **separate** for gate stats (never pool for a gate limb) |
| K | `K_intrinsic = 1` — one named cell; no variant scored |

---

## §2 — Catalogue cell C1 — ENTRY (causal; all constants a priori)

Inputs at each RTH 1m bar open `t` (both known at `t`, no path foresight):

```
r_ES(t) = log( ES.v.0  close[t-1] / close[t-6] )   # trailing 5 completed minutes
r_NQ(t) = log( MNQ.v.0 close[t-1] / close[t-6] )
d(t)    = r_ES(t) - r_NQ(t)                          # signed divergence, ES minus NQ
theta(t)= median( |d| ) over all RTH clock |d| in the trailing 20 completed RTH sessions
```

`theta` is constant within a session (computed from prior completed sessions only).
Clocks lacking 6 prior RTH closes on the joined series, or lacking 20 prior sessions for
θ, are ineligible (no trade).

Signal:

| Condition | Action |
|---|---|
| `d(t) >= +theta(t)` | enter **LONG** MNQ at open of bar `t` |
| `d(t) <= -theta(t)` | enter **SHORT** MNQ at open of bar `t` |
| otherwise | no trade at clock `t` |

While in a position, all further signals are ignored until session-flat or stop (EM3).

**Frozen constants (do not retune on scored data):** lookback **5** min · threshold window
**20** sessions · statistic **median** of `|d|` · sign as above.

**Mechanism (disclosure):** ES/NQ common factor; liquidity hits the deeper ES book first;
residual error-corrects. **Relative contrarian** in MNQ (buy NQ when it has *lagged*) —
**not** own-instrument momentum. If sign inverted → own-instrument momentum → C5-dead
(D5-RECOST-1). Do not invert to rescue.

**Closed-door clearance (class, not a re-score):** not ORB/C7 · not bars-only S/R C10 ·
not opening-volume C6 · not depth/L1-tilt C9/C11 · not ICT C1–C4.

---

## §3 — Scoring (EXPLORATION only; after operator GO)

Per arm (long / short separate):

| Limb | Definition |
|---|---|
| Primary | Mean net R; session-block bootstrap **95% CI** must exclude 0 |
| Placebo | Within-session R-shuffle **1000** reps; seed **20260808** |
| Halves | Older/newer EXPLORATION session-date halves; sign disagree → `VOID` / AMBIGUOUS-HOLD as frozen at GO |
| DSR | ≥ **0.650** at `K_intrinsic=1` |
| Disclose | WR · max adverse/favorable excursion · trades/session · coverage · EM six-char |

**Gate:** `SHAPE-CLEAR` / `FALSIFIED` / `VOID` as specified at explore GO.
**TNEC verdict string** (unscored limbs typed **U** until their GO):

```
N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)
```

At G0 freeze (pre-explore): all five N-* limbs are **U**; bust / P(pass) / μ are `U`.

**Deferred (not this packet):** full N-SURV MC · Cap claim · ORB unpark · Pine/rail ·
elevating D1/D2 preferences into gates · G=5/20 retune.

---

## §4 — Explore path (Con-3)

1. Stage-0 freeze (**this file**) — DONE when committed.
2. Operator **explore GO** (separate) — unpaid at freeze.
3. Harness `run_construct_g0.py` refuses real-panel path PnL unless
   `EXPLORE_GO.md` exists in this directory (gitignored token) **and** `--explore-go` is passed.
4. Path-PnL scorer is **wired** (MNQ+ES cache join, session-block CI, within-session
   path-R shuffle placebo, halves, annSR/DSR) — still refuses without the token.
   Optional `start:` / `end:` YYYY-MM-DD lines in `EXPLORE_GO.md` bound the window;
   omit both → full joined panel.
5. First scored run = EXPLORATION only. Cap not claimed unless a separate Cap reservation covers a Cap-style cell (this construct is **not** CapFLOW).

---

## §5 — Forbidden moves

- Inventing ENTRY variants / lookback / θ-window / statistic after freeze.
- Inverting the sign to rescue a fail.
- Path-scoring real bars before explore GO.
- Oracle / completed-window ranking; OF ρ as substitute entry; ORB filter laundering (F2).
- Promoting G=5/20 diagnostics; claiming Cap from this packet alone; Pine/deploy/arming.
