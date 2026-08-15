# NOTICE 2026-08-13 — MSL design-box re-derivation (slate 1 exhausted)

**Type:** Notice-phase analysis. **Proposes; rules on nothing.** $0 · K=0 · no gate moved, no threshold changed, no candidate admitted. Changing the ratified design box requires an operator election (see §8).
**Trigger:** first slate exhausted — [MSL-C2 `FALSIFIED`](../../briefs/closures/MSL-C2-closure-falsified.md), [MSL-C3 `OPERATOR-KILL`](../../briefs/closures/MSL-C3-closure-operator-kill.md), [MSL-C1 `FALSIFIED`](../../briefs/closures/MSL-C1-closure-falsified.md). Channel gate is RESOLVED (cards reached recorded outcomes with artifact trails); yield falsifier **not** fired (Stage-1 deaths 1/3; two G0 freezes inside two days).
**Reads:** `core/firm_rules.py` `Tradeify_Select_100K` @ HEAD (trail $3,000 · target $6,000 · `cost_per_side_usd` 0.91 index micros, **MGC $1.06** per L231/L318 comment pins) · [C1 RESULTS_g2](../../../lab/analysis/c1/msl_c1_mym_2026-08/RESULTS_g2.md) · [C2 closure](../../briefs/closures/MSL-C2-closure-falsified.md) · [population notice](N-2026-08-13-external-eval-population-data.md) §7.5 · [fade spec §3.2](../../superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md) (the per-trade-Sharpe claim this note tests) · [slow-archetype RESULTS](../../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) (no-time-limit venue fact).

---

## §1 — What slate 1 actually tested

All three cards occupied **one** corner of the design space: mean-reversion-at-a-level, `rr ≈ 1`, hard stop, k=1. Two were scored; both returned negative signed expectancy.

| Card | Mechanism | Arm | n | mean net R | WR | 95% CI | DELETE |
|---|---|---|---:|---:|---:|---|---|
| C2 (MGC) | London-range failed-extension fade | long | 327 | — | — | [−0.287, **−0.071**] | FAIL |
| C2 (MGC) | " | short | 310 | — | — | [−0.292, **−0.075**] | FAIL |
| C1 (MYM) | PDH/PDL failed-break reclaim | long | 406 | **−0.1756** | **0.461** | [−0.267, **−0.083**] | PASS |
| C1 (MYM) | " | short | 444 | **−0.1069** | **0.486** | [−0.197, **−0.017**] | PASS |

**C1 did not die of cost.** Its cost-law limb passed comfortably (1R ≈ 5.2–6.0× the 4×RT hurdle at realized stops). It died of **signed gross expectancy**: at `rr=1`, gross expectancy in R is `m₀ = p·rr − (1−p) = 2p − 1`, which is **negative for any p < 0.50**. At p = 0.461 / 0.486, `m₀ = −0.078 / −0.028` *before a cent of cost*. No sizing, no cost reduction, and no instrument swap rescues a negative gross edge — these are structurally different failures and must not be conflated.

**C1's DELETE PASS is the informative part.** The level constraint genuinely selected — the constrained arm was less negative than the sham. The mechanism is real; its magnitude is insufficient to cross zero at `rr=1`. That is a statement about **geometry**, not about the mechanism family.

---

## §2 — The two arithmetic constraints, stated exactly

**(a) Break-even win rate.** With per-trade risk `R` dollars, reward:risk `rr`, all-in round-trip cost `c`:

> `p* = (1 + c/R) / (rr + 1)`

At C1's realized geometry (`rr=1`, R = $67.50 at the 135-pt mean stop, c = $2.82): **p\* = 52.1%** long, **52.4%** short. Measured: 46.1% / 48.6% — short by 6.0 and 3.8 points.

**(b) Bust bound against the trailing barrier.** For a per-trade drift `μ` and standard deviation `σ`, the probability of ever drawing down `D` from the running peak is `exp(−2μD/σ²)`. With `σ = R(rr+1)√(p(1−p))` and `μ = R·m` (m = net expectancy in R), requiring bust ≤ 3.0% against `D = $3,000` gives:

> `R_max = 1711 · m / [ (rr+1)² · p(1−p) ]`   (solving the implied quadratic in R, since `m = m₀ − c/R`)

**Both limbs bind in opposite directions**, and this is the whole design problem: raising `R` speeds passage and raises bust; lowering `R` cuts bust and pushes the winning day under the **$200** payability floor.

---

## §3 — The feasible region (index micros, RT $2.82)

`R_max` = largest per-trade dollar risk holding bust ≤ 3.0%; trades-to-target at $6,000; all-win/worst day at k=1 entry/day.

| p | rr | m₀ gross | R_max | m net | μ/trade | trades to $6k | all-win day | worst day | verdict |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.461 | 1 | **−0.078** | — | — | — | — | — | — | **infeasible (C1 long, measured)** |
| 0.486 | 1 | **−0.028** | — | — | — | — | — | — | **infeasible (C1 short, measured)** |
| 0.55 | 1 | 0.10 | $137 | 0.080 | $10.9 | 550 | **$135** ✗ | $140 | fails $200 payability |
| 0.60 | 1 | 0.20 | $342 | 0.192 | $65.5 | 92 | $339 ✓ | $345 ✓ | feasible — but needs p ≥ 0.60 |
| 0.35 | 2 | 0.05 | — | — | — | — | — | — | **infeasible** (cost exceeds any bust-compliant R) |
| 0.42 | 2 | 0.26 | $191 | 0.245 | $46.9 | 128 | $380 ✓ | $194 ✓ | feasible |
| 0.50 | 2 | 0.50 | $374 | 0.493 | $184 | 33 | $746 ✓ | $377 ✓ | feasible |
| 0.30 | 3 | 0.20 | $85 | 0.167 | $14.2 | 423 | $252 ✓ | $88 ✓ | feasible, slow |
| 0.35 | 3 | 0.40 | $181 | 0.384 | $69.5 | 86 | $539 ✓ | $184 ✓ | **feasible** |
| 0.40 | 3 | 0.60 | $262 | 0.589 | $155 | 39 | $785 ✓ | $265 ✓ | **feasible, fast** |

**Cost is not the binding constraint at wide stops.** Re-running p=0.35/rr=3 at MGC's RT $4.12 gives R_max $177 and 90 trades — four trades slower than the index-micro cell. The cost tax at those stops is ≈0.023R, far inside the ENV-1 ≥40-tick guidance. The index-vs-metals cost gap is materially irrelevant to this geometry.

**Streak cross-check** (independent of the diffusion bound): at p=0.40/rr=3, R=$262, the expected longest losing run over 39 trades is ≈7.2 (`log n / log(1/(1−p))`), costing $1,883 against a $3,000 rope; 11 straight would breach, which sits at the few-percent level and is consistent with the 3.0% target. At p=0.30/rr=3, R=$85, the expected longest run over ~423 trades is ≈17.0, costing $1,441 — comfortably inside. The two methods agree, which is the sanity check that the bound isn't being applied nonsensically.

---

## §4 — The decisive result: the fade spec's math is right, and it was being evaluated on an empty set

The [fade spec §3.2](../../superpowers/specs/2026-07-30-tradeify-native-fade-program-design.md) claims per-trade Sharpe rises with win rate at fixed expectancy, so high-WR is *affirmatively* correct for barrier survival. **This re-derivation confirms it decisively** — hold gross expectancy fixed at `m₀ = 0.20R` and compare the two ends:

| Config | R_max | μ/trade | trades to $6k |
|---|---:|---:|---:|
| p=0.60, rr=1 | **$342** | $65.5 | **92** |
| p=0.30, rr=3 | $85 | $14.2 | 423 |

At **identical** gross edge, the high-WR configuration tolerates **4.0× the risk** and passes **4.6× faster**. High-WR geometry is not merely defensible; it is strictly superior — *if you can reach positive expectancy there*.

**That is the entire finding.** The estate optimized geometry-given-edge inside a region where the edge is negative. Two independent measurements now sit below the `rr=1` break-even line, and the [population evidence](N-2026-08-13-external-eval-population-data.md) §7.5 supplies the mechanism: observed high-WR passers reach their win rate by **removing the stop** — a route your 2026-08-13 hard-stop ruling closes permanently and correctly. Conditional on a mandatory hard stop, the attested positive-edge region is the low-WR / high-rr corner (Archetype A), which **MSL has never tested**.

So the proposed shift is **not** "better geometry." It is: *worse geometry, in the only place edge has been observed to exist under our own binding constraint.* Any future reader tempted to cite this note as evidence that low-WR is preferable should stop at this section — it says the opposite.

---

## §5 — Robustness, which is the second argument for the shift

Feasibility at `rr=1` requires **p ≥ 0.60** to clear survival and payability jointly (p=0.55 survives but yields a $135 winning day, under the $200 floor; the joint floor is ≈p 0.57). C1 measured 0.461 — an **11-point** gap, not a near miss.

At `rr=3`, every cell from **p=0.30 to p=0.40** is feasible. The design tolerates being wrong about p by a wide margin, and passage time degrades gracefully (39 → 424 trades) rather than falling off a cliff. At `rr=2` the region is narrower and has a hard floor near p≈0.40 (p=0.35 is infeasible at any R).

Given that we have no reliable prior on a new mechanism's win rate, **a design whose feasible region spans a 10-point WR band is worth materially more than one requiring a point estimate we have missed twice.**

---

## §6 — The enabling venue facts

1. **No time limit** on the evaluation ([verified](../../../lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) §2, primary-source). A 39–424-trade passage is admissible; only the **≥1 trade per Mon–Fri week** idle rule binds, and every cell above clears it at k=1/day.
2. **40% consistency (eval only).** At k=1/day the best day is one win: $785 at the fastest cell against a $6,000 target = 13% — comfortable. ⚠ At k>1/day a multi-win day at `rr=3` can approach the 40% line (three wins at p=0.40 → $2,354 = 39%). **The consistency rule binds on `rr` × entries/day, not on either alone** — it must be screened at the declared design point, not assumed.
3. **$200 winning day** is the funded-phase payout floor and is the limb that kills the low-R end at `rr=1`.

---

## §7 — Proposed slate-2 hunting region

**Geometry:** `rr` ∈ [2, 3] · target WR 0.30–0.42 · `R` solved to the bust-≤3.0% frontier (≈$180–$260 at rr=3) · **hard stop mandatory** (2026-08-13 ruling) · k=1 independent entry/day · flat by 16:00 ET · no pyramiding.

**Mechanism family:** trend-continuation / breakout-with-follow-through — the Archetype-A shape, and the structural opposite of everything slate 1 tested.

**Instrument:** **non-index**. On index instruments the single-index intraday OHLCV raised bar makes momentum/continuation the named *exhausted* lever, while MR-at-level (route ①) has now failed twice — both directions are squeezed. Non-index (MGC · MCL · M6A) sits outside that bar entirely, and its cost penalty is ≈4 trades at this geometry (§3).

**Adverse prior to price honestly, not to route around:** the Guardian→MGC transfer cell closed `DEAD(N-SURV)` at bust 42.2%/72.4%/16.5%. That was a **locked strategy transferred at its own sizing**, not a fresh construct sized to the frontier — the sizing is precisely the variable this note solves. Slate 2's MGC card must state its R against that closure's R and show the difference, or it is re-running a dead cell. This is a Stage-0 obligation, not a footnote.

---

## §8 — What this note does NOT establish

1. **It changes no ratified surface.** The design box in the [first slate](../../briefs/2026-08-12-msl-first-slate.md) header was ratified with the charter (B1/B2). Re-pointing it is an operator election; this note is the derivation offered in support, nothing more.
2. **The bust bound is an approximation.** `exp(−2μD/σ²)` assumes i.i.d. trades, a continuous diffusion, and an infinite horizon. Infinite horizon makes it **conservative** (bust-before-target ≤ bust-ever); i.i.d. makes it **optimistic** where real trades cluster. The spawned [Magdon-Ismail regression task](N-2026-08-13-external-eval-population-data.md) §4 replaces it with an exact closed form and its published tables — **every R_max in §3 should be re-derived once that lands**, and any number here is provisional until then.
3. **No mechanism is proposed.** A hunting region is not a candidate. Slate-2 cards still walk charter steps 1→8 unchanged: dedup, executed door-check, $0 screens, cheap falsifier, Req 1a delete/flip, G0 on operator B4.
4. **p is not transferable across exits.** C1's measured 0.461 was at `rr=1`; the same entry at `rr=3` has a **different and unknown** win rate — wider targets are hit less often. Nothing here licenses assuming any mechanism lands in the 0.30–0.42 band. That is what the explore measures.
5. **The 3.0% bust ceiling and 50% pass floor are unchanged.** This note re-derives *where to hunt inside them*, never the thresholds. The [population notice](N-2026-08-13-external-eval-population-data.md) §7.2 governs: a base rate is a third input, not a dial.

---

## §9 — Audit hook (reproduces every number in §3–§5)

Every figure in this note was verified computationally before authoring, not hand-derived. Stdlib only:

```python
import math
D, TARGET, X = 3000.0, 6000.0, -math.log(0.03)   # X = 3.5066

def solve(p, rr, c):
    m0 = p*rr - (1-p)                             # gross expectancy in R
    if m0 <= 0: return None                       # negative gross: no R rescues it
    K = (2*D/X) / ((rr+1)**2 * p*(1-p))
    disc = (K*m0)**2 - 4*K*c
    if disc < 0: return None                      # cost exceeds any bust-compliant R
    R = (K*m0 + math.sqrt(disc))/2
    m = m0 - c/R
    return dict(R=R, m=m, mu=R*m, n=TARGET/(R*m), win=rr*R-c, worst=R+c)

# index micros c=2.82; MGC c=4.12
for p, rr, c in [(0.461,1,2.82),(0.55,1,2.82),(0.60,1,2.82),(0.42,2,2.82),
                 (0.30,3,2.82),(0.35,3,2.82),(0.40,3,2.82),(0.35,3,4.12)]:
    print(p, rr, c, solve(p, rr, c))
# break-even: p* = (1 + c/R)/(rr+1)  ->  C1 long (R=67.50) = 0.5209; short (R=58.00) = 0.5243
```

Expected: p=0.461/rr=1 → `None` · 0.55/1 → R 137.4, n 550, win $135 · 0.60/1 → R 341.8, n 92 · 0.42/2 → R 191.4, n 128 · 0.30/3 → R 84.9, n 423 · 0.35/3 → R 180.7, n 86 · 0.40/3 → R 262.6, n 39 · 0.35/3 @ MGC → R 177.1, n 90. Every row returns bust exactly 0.0300 by construction.

## §10 — Operator elections requested

1. **Re-point the design box** from high-WR/`rr≈1` to `rr` ∈ [2,3] / WR 0.30–0.42 / R-at-frontier, per §7? (Slate-1 header stands until elected.)
2. **Slate-2 instrument lane** — non-index as §7 argues, or hold for the Magdon-Ismail anchor first so R_max is exact before cards are authored?
3. **Sequencing** — author slate 2 now, or wait on the anchor? The clock is **2026-11-08**; at the fastest feasible cell a passage is ~39 trading days, so one more full card cycle fits, two is tight.
