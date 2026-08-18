# Q-TRAINKILL-1 — Verdict pre-registration (H-TRAINKILL)

**Frozen:** 2026-08-18, **before any closure n / CI / se is substituted.**
Parent brief: [`Q-TRAINKILL-1-train-gate-power.md`](../Q-TRAINKILL-1-train-gate-power.md).
Operator GO: this session, off
[`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)
§5 packet 3.

A verdict computed after moving the set, the bar, the se formula, the
kill-event map, or the fit floor is void.

**Forbidden regardless of outcome:** no gate threshold moves. Remedy space is
design power (longer panels, pooled families, parent-era data), never
bar-lowering.

---

## §A — Closure set (frozen at GO from the packet + SESSIONS sweep)

Packet names, counted exactly:

1. Q-TNEC-CON-2
2. Q-TNEC-CON-3
3. Q-TNEC-CON-4
4. Q-TNEC-CON-5
5. MSL-C1
6. MSL-C2
7. MSL-C3-K2
8. MSL-S2A
9. Q-R2VBUCK-1
10. Q-R2FLOW-1
11. Q-R2AGRUN-1
12. Q-MNQDTL-CON-1
13. DL-1

**SESSIONS sweep (2026-08-08 → 2026-08-18 GO), siblings ADDED:**

14. Q-CAPFLOW-1 — measured explore FALSIFIED 2026-08-14
15. H-DSTRUCT-MNQ-1 — measured Tier-1 NULL 2026-08-18

**Considered, not added** (wrong death class — not a train-mean / explore
score; disclosed so the sweep is auditable):

- MSL-S2B Stage-1 FAIL (pre-explore route)
- MSL-C3 OPERATOR-KILL (pre-G0)
- Q-EVALSEQ-1 / Q-POLFRONT-1 (policy levers)
- S1a/S1b range-state screens (different object; not the construct-kill
  record this Q scores)
- six-lead / WHO / Clause-N / Req-2 (admissibility, observation B)

**n = 15.** Silent exclusion of any of 1–15 voids the read.

---

## §B — Effect size and se (declared before substitute)

- **μ_0 = 0**
- **μ_bar = +0.10 R** (admissibility bar at $75 / trade; packet)
- **se = (CI_hi − CI_lo) / 3.92** from the closure's binding reported
  session-block CI on the **per-trade mean in R**. That is the packet's
  "CI width / 3.92".
- Normal approximation: `mean_hat ~ N(μ, se²)`. CDF `Φ` = `0.5*(1+erf(z/√2))`.
- **annSR-only limbs** (no mean-R CI): BOUNDED (see §D).
- **ρ / association cells** with no mean-R CI: BOUNDED under μ_bar (the
  +0.10R bar does not translate to ρ without an undeclared mapping).
- **N-ACT / cadence / abandonment / Stage-1** cells: BOUNDED (not a mean-R
  gate).

---

## §C — Observed-event map (CI-mean rows only)

The closure's binding reported CI (the limb the §6 table used) maps to
exactly one of:

| Event | Definition |
|---|---|
| `FALSIFIED` | CI_hi < 0 |
| `AMBIGUOUS` | CI includes 0 |
| `CLEARED` | CI_lo > 0 |

Two-arm closures: use the **binding arm** named in the §6 firing row. If
the gate required *both* arms (e.g. "both-arms CI upper < 0"), treat the
observed event as the joint and score `P = P_arm1 * P_arm2` under
independence (disclosed). If only one arm is quoted as decisive, use that
arm alone.

```
P(FALSIFIED | μ, se) = Φ(-1.96 - μ/se)
P(CLEARED    | μ, se) = Φ( μ/se - 1.96)
P(AMBIGUOUS  | μ, se) = 1 - P(FALSIFIED) - P(CLEARED)
```

Aux limbs (placebo p, annSR floor, halves) do **not** rewrite the event
once a mean-R CI exists. They are disclosed, not a second kill.

---

## §D — Partial-table / BOUNDED

A row whose mean-R CI or n is unrecoverable, or whose kill is not a
mean-R CI event, enters as **BOUNDED**: `P(observed | μ)` is bracketed
at `{ε, 1-ε}` with `ε = 1e-6` (open interval so log-likelihood is
defined). The three-way reading is asserted under **both** extremes
(all-BOUNDED-at-ε vs all-BOUNDED-at-1-ε, crossing with the scored
rows held fixed). If the two extremes **disagree** on the reading, the
verdict is `AMBIGUOUS-HOLD`. Silent drop is void.

---

## §E — Fit floor and the three readings

Let `n*` = number of **scored** (non-BOUNDED) rows.
Let `g(μ) = exp((1/n*) Σ log P(v_i | μ, se_i))` — geometric mean.

**A DGP fits** iff `g(μ) ≥ 0.05`.

| Reading | Trigger | Disposition |
|---|---|---|
| `KILLS-INFORMATIVE` | zero fits AND bar does not | `INTEGRATE` — the kill record is consistent with empty families and not with +0.10R; zero-yield streaks may be quoted as supply-drought **only with this power annotation**; affirmative evidence for letting §4 fire |
| `GATES-UNDERPOWERED` | bar fits (zero may or may not) | `INTEGRATE` — +0.10R also produces this record; next explore designs change n / panel-length **before** more screens; zero-yield may not be quoted as drought without the power annotation |
| `MISCALIBRATED` | neither fits (and BOUNDED extremes agree) | `ITERATE` — neither DGP produces the record; do not lower bars; recover a different DGP or missing se |

If bar fits, the packet's "fits too" language selects `GATES-UNDERPOWERED`
even when zero also fits — that is the reading that changes design.

`AMBIGUOUS-HOLD` if BOUNDED extremes disagree, or `n* = 0`.

---

## §F — Pinned ex-ante expectation

**Predicted: `GATES-UNDERPOWERED`.** Class prediction, not a substitute of
se values: a +0.10R mean against the se of a few hundred session-blocked
trades typically leaves CI straddling 0 (the AMBIGUOUS class that
dominates the named CON/MSL cells). Formal FALSIFIED (CI_hi < 0) at
μ=+0.10 requires se ≲ 0.05, which short explore panels rarely have.
Substituting CIs to confirm this is the compute step, not this freeze.

---

## §G — Adjacent prior, not this unit

Gate-reachability / bindingness audits
(`docs/notes/audits/2026-07-12-*-reachability-audit.md` and successors)
ask whether a gate *can fire* and *binds mechanically*. This Q asks
whether the observed *firing rate* discriminates edge-absence from
under-power. Different unit. Cited so it is not rediscovered.

---

**Freeze note:** this file must exist on disk, with a recorded sha256,
**before** `TABLE.json` is assembled from closures. Same-session
freeze-then-score as Q-CONDVAL-1 / Q-EXPR-1.
