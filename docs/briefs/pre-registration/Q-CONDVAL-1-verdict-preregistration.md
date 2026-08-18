# Q-CONDVAL-1 — Verdict pre-registration (H-CONDVAL)

**Frozen:** 2026-08-18, **before the measured CL lift is read into the verdict
arithmetic.** Parent brief:
[`Q-CONDVAL-1-range-state-r-terms.md`](../Q-CONDVAL-1-range-state-r-terms.md).
Operator GO: this session, off
[`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)
§5 packet 1.

The three free parameters below are the packet's declared levers. A verdict
computed after moving any of them is void.

---

## §A — Three free parameters (declared before the lift is read)

### (i) Host geometry

**Gating cell = MSL slate-2 box center**, not a named alternative:

| Knob | Gating value | Box (disclosure only) | Source |
|---|---|---|---|
| `rr` | **2.5** | [2, 3] | [`2026-08-13-msl-slate-2-design-box`](../../adr/2026-08-13-msl-slate-2-design-box.md) |
| `WR` | **0.36** | [0.30, 0.42] | same (midpoint of the elected WR band) |
| stop | hard / structural | hard / structural | same |
| `k` | 1 | 1 | same |
| pyramiding | none | none | same |

Gross expectancy at the gating cell (R, 1R = stop):

```
E_box = WR * rr - (1 - WR) = 0.36 * 2.5 - 0.64 = 0.26
```

Corners with `E_box ≤ 0` (WR=0.30, rr=2 → −0.10R) are **excluded** from every
disclosure cell — the rederivation's own `solve()` returns `None` on negative
gross; no R rescues them.

### (ii) Lift → R mapping

**Form (α = 0, generous to the conditioner, stated as such):**

A host with slate-2 geometry realizes `E_box` only on *high-range* next days
(`y=1`); low-range next days session-flat at 0R (scratch). Then:

```
ΔE[R] = L * E_box
L     = P(y=1 | bias=1) - P(y=1)
```

`L` is the **raw conditional-minus-unconditional** lift. It is **not** the
IAAFT-excess (obs − surrogate-band center) and **not** the spec's 0.60
DECLARED-NOT-DERIVED rate.

**Read `L` from these committed keys only**, after this file exists on disk:

- `P(y=1 | bias=1)` ← `gateHit` in
  `lab/analysis/_inbox/rangestate_mcl_2026-08/s1b_results.json`
- `P(y=1)` ← `p_up_unconditional` in the same file

Those two quantities were carried verbatim into the official re-score
([`RESULTS_CORRECTED`](../../../lab/analysis/_inbox/rangestate_corrected_2026-08/RESULTS_CORRECTED.md)
§1 "frozen obs"). Do not re-derive them from the parquet.

**Forbidden input:** the corrected-battery spec O2 0.60 "minimum-useful
conditional rate." It is DECLARED-NOT-DERIVED. Using it here would launder the
undeclared number into the verdict this Q exists to derive.

### (iii) Material fraction of `hurdle_4x`

**Gating envelope cell = the N-EDGE reference cell the parent notice named:**

| Knob | Gating value | Envelope (disclosure only) | Source |
|---|---|---|---|
| `R` (1R dollars) | **$75** | ≈ $75–200 | notice packet; seed-target admissibility ≈ +0.10R @$75 |
| `RT` | **$4.12** | $2.82–4.12 | non-index pin in [design-box rederivation §9](../../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) (MGC `c=4.12`); CL/MCL is the same non-index class |
| `hurdle_4x` | `4 * RT / R` | — | cost-law convention |
| material fraction | **0.50** | — | product equals the notice's +0.10R @$75 N-EDGE quantum |

```
hurdle_4x = 4 * 4.12 / 75 = 0.219733... R
bar_ΔE    = 0.50 * hurdle_4x = 0.109866... R
L_star    = bar_ΔE / E_box = 0.109866... / 0.26 = 0.422564...
```

**Frozen gating bar, in lift units: `L_star = 0.422564`.**
(Exact: `0.50 * 4 * 4.12 / 75 / 0.26`.)

Reason this cell, not the easy end of the envelope: the decision is
kill-or-keep on a conditioner-engineering GO. The notice named +0.10R @$75 as
the quantum that "clears N-EDGE." A lift that cannot move N-EDGE by that
quantum at the cell the notice itself uses does not earn a new-K prereg.

---

## §B — Decision rule

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (KEEP — conditioner-engineering prereg still electable) | `L ≥ L_star` | `INTEGRATE` — O2 discharged (connecting arithmetic exists; lift clears) |
| `FALSIFIED` (PARK the S1b conditioner-engineering branch) | `L < L_star` | `STOP` — O2 discharged (required lift derived; measured lift misses); no conditioner-engineering GO |
| `AMBIGUOUS-HOLD` | either committed key missing, or `E_box ≤ 0` at the gating cell | `ITERATE` — recover `L` from another committed source; do not invent |

Corners / envelope ends are **disclosure**, never a third verdict. They may not
rescue a `FALSIFIED` or downgrade a `RESOLVED`.

---

## §C — Pinned ex-ante expectation

**Predicted: `FALSIFIED`.** Recorded before the lift is substituted: `L_star =
0.423` is a 42 pp lift on a next-day *above-median-TR* event. Ordinary
volatility clustering produces a high-teen / low-20s raw C−U on a top-quintile
yesterday filter (the class the SIGNAL-GENERIC verdict already named). Clearing
0.42 from clustering alone would be a surprise and should be treated as the
informative result.

This prediction uses the **class**, not the CL number. Substituting the CL
number to confirm the prediction is the compute step, not this freeze.

---

## §D — Forbidden moves (inherited; restated for the frozen record)

1. Using spec O2's 0.60 as an input to `L_star` or to `L`.
2. Replacing raw C−U with IAAFT-excess after seeing that GENERIC sits inside its
   band (that is a different question: "does EXCESS buy anything?").
3. Moving `rr`, `WR`, `R`, `RT`, `α`, or the 0.50 fraction after `L` is read.
4. Gating on a disclosure corner because the center missed.
5. Reading either verdict as a mechanism claim or as a discharge of MCL
   mechanism-owed (A6 rails still bind).
6. Opening a conditioner-engineering prereg from a `FALSIFIED` close.

---

**Freeze note:** this file must exist on disk, with a recorded sha256, **before**
the runner substitutes `gateHit` / `p_up_unconditional`. Commit-ordering
evidence lands when the operator commits; same-session freeze-then-compute
follows the Q-ICT-SWEEPFVG-1 / Q-CAPBAND-1 pattern.
