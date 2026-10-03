# T00 screen depth, precision and budget: decision packet (2026-10-03)

**Status:** decision packet for Joshua, prepared under coordinator 2's relay of your 2026-10-03 approval to prepare it. It is not a ruling, it sets no #581 §3 value, and it is not one of the Sheet 5 operator acts.
**Answers:** design #629 §12 items 7, 9 and 10 (head `3742a95`, `docs/superpowers/specs/2026-10-02-t00-screen-authority-design.md` §4.3, §4.5, §5.4, §6), and #581 §3 item 1, the depth (head `438b659`, `docs/briefs/pre-registration/2026-10-01-tradeify-t00-step2-screen-prereg.md` A2, A5, A6). Build card #634 (head `079b1b6`).
**Inputs:** the timing figures in design §6.2–§6.3 only. No replay or screen outcome was read, and no new probe was run.

## 1. Cost by depth

N is paths per population, and there are three populations (FULL, H1, H2). N = 3 × `depth_per_root`, so the nominal depths become 1,002, 2,001, 3,000, 5,001 and 10,002. Per-path CPU uses the integrity check hoisted to the worker epoch: 136 s point and 320 s upper (design §6.3). Wall time assumes 8 workers at 1.25 × CPU.

| N per population | Total paths | Path CPU-h, point / upper | Wall on 8 workers, point / upper | Overhead CPU-h (reserve, §3) | Overhead wall, upper |
|---|---|---|---|---|---|
| 1,002 | 3,006 | 114 / 267 | 17.7 h / 41.8 h (0.7 / 1.7 d) | 3.2 | 0.7 h |
| 2,001 | 6,003 | 227 / 534 | 35.4 h / 83.4 h (1.5 / 3.5 d) | 3.9 | 0.8 h |
| 3,000 | 9,000 | 340 / 800 | 53.1 h / 125 h (2.2 / 5.2 d) | 5.3 | 1.1 h |
| **5,001** | **15,003** | **567 / 1,334** | **88.6 h / 208 h (3.7 / 8.7 d)** | **7.5** | **1.4 h** |
| 10,002 | 30,006 | 1,134 / 2,667 | 177 h / 417 h (7.4 / 17.4 d) | 13.9 | 2.4 h |

Overhead covers three things:
- a worker epoch: build plus two integrity checks, 180 + 2 × 71.4 ≈ 323 s CPU, using the top of the build range;
- per segment: W = 8 epochs, run in parallel, so about 0.1 h wall;
- once per run: the candidate pass plus the probe, p ≈ 1,100 s at the upper estimate (design §5.4).

Overhead is at most 3% of point path CPU at every depth. Memory is 8 × 0.56 GiB ≈ 4.5 GiB of 15.6 GiB, so W = 8 (design §5.1).

## 2. Precision and misclassification

A2 and A6 compare **point estimates** with no confidence bound. GO needs 20·bust ≤ n in each of FULL, H1 and H2, plus 2·pass ≥ n in FULL. The probabilities below use a normal approximation, p̂ ~ N(p, p(1−p)/N) with no continuity correction. The exact binomial was also computed (Appendix) and differs by ≤ 2.2 pp in the worst case (N = 1,002, true 5.5%), and by ≤ 0.2 pp at N ≥ 5,001. "Wrong side" means a false NO-GO when the true rate is inside the threshold and a false GO when it is outside.

| N | SE at bust 5% | SE at pass 50% | Bust true 4.0% | 4.5% | 5.5% | 6.0% | Pass true 45% | 48% | 52% | 55% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,002 | 0.69 pp | 1.58 pp | 5.3% | 22.3% | 24.4% | 9.1% | 0.07% | 10.3% | 10.3% | 0.07% |
| 2,001 | 0.49 | 1.12 | 1.1% | 14.0% | 16.3% | 3.0% | <0.01% | 3.7% | 3.7% | <0.01% |
| 3,000 | 0.40 | 0.91 | 0.26% | 9.3% | 11.5% | 1.05% | <0.01% | 1.4% | 1.4% | <0.01% |
| **5,001** | **0.31** | **0.71** | **0.02%** | **4.4%** | **6.1%** | **0.15%** | **<0.01%** | **0.23%** | **0.23%** | **<0.01%** |
| 10,002 | 0.22 | 0.50 | <0.01% | 0.79% | 1.4% | <0.01% | <0.01% | <0.01% | <0.01% | <0.01% |

- **The halves compound.** H1 and H2 are scored independently at the same N, and each must clear the bust ceiling. If FULL, H1 and H2 all have a true bust rate of 4.5%, the chance that at least one shows > 5% is 53% at N = 1,002, 25% at 3,000, 12.6% at 5,001 and 2.4% at 10,002. At a true 4.0% the same figures are 15%, 0.8%, 0.05% and ≈ 0.
- **The bust ceiling binds; the pass floor does not.** Its SE is about twice as large, but the thresholds sit much further from the likely rates.
- **Precision is not the only error.** The pessimistic assignment (A5 (3)) adds every `UNDETERMINED` path to the bust count, so the estimate is biased upward by however many paths disagree, and depth does not shrink that bias.

## 3. Budgets and approval windows

The formulas are the design's (§5.4, §12 items 7 and 10), with the margins this packet proposes:
- **Path budget** `path_cpu_seconds` = 1.5 × 320 s × 3N = **1,440 × N CPU s**. This is a cap, not a spend.
- **Overhead reserve** `overhead_cpu_seconds` = (b + 2i)(W·S + R) + p, with b + 2i = 323 s, W = 8, R = 8 spare starts, p = 1,100 s, and S = max(3, ⌈upper wall in days⌉), i.e. one expected segment per machine-day. Exhausting it HALTs, and never TERMINALs on its own (design §4.3).
- **Approval windows** (r3c and screen): `expires_at` ≥ run start + 1.5 × (upper wall + overhead wall) + 2 h for `verify`. The 2 h assumes 9 serial re-executions, each with its own epoch, at the upper figures. The r3c approval must also cover the earlier §8 steps 7–11, which add your own lead time. A lapse is STOPPED `APPROVAL_LAPSE` and a renewal resumes it, so it is not terminal.

| N | Path budget (CPU s) | Overhead reserve (CPU s), S | Approval window after run start |
|---|---|---|---|
| 1,002 | 1,442,880 | 11,430 (S = 3) | ≥ 66 h (2.7 d) |
| 2,001 | 2,881,440 | 14,012 (S = 4) | ≥ 128 h (5.3 d) |
| 3,000 | 4,320,000 | 19,177 (S = 6) | ≥ 191 h (8.0 d) |
| **5,001** | **7,201,440** | **26,924 (S = 9)** | **≥ 317 h (13.2 d)** |
| 10,002 | 14,402,880 | 50,166 (S = 18) | ≥ 631 h (26.3 d) |

**Build-card point (#634).** Design §5.4 charges a crashed segment "that heartbeat's job CPU … as overhead". If the build charges a crashed segment's **whole** job CPU, path CPU included, then one crash late in a one-day segment (about 190 CPU-h) exhausts any reserve above and HALTs the run. That is recoverable only by your CONTINUE act. To keep the reserve meaningful, the build card should pin the reading as job CPU minus that segment's recorded path CPU. It is not an N decision.

## 4. Probe scope

No further real-source probe is needed or authorized before ratification. The two that were authorized are done:
- the timed P7 re-run (ruling A4, design §6.1);
- the two-window decomposition (sheet 2 item 1, design §6.2).

Row G4 also bars any probe that reads beyond P7's path windows, so a 1,500-session timing is not available before the freeze in any case. The only remaining measurement is the in-run probe (rows B2 and B3). It runs inside step 3, after AUTHORITY_BOUND.

**Residual risk.** Linearity is untested beyond 40 sessions, and the 1,500-session cost is a 37× extrapolation. B3 refuses when probe CPU × 3N > `path_cpu_seconds`. With the budget above, that means a probe path costing more than 480 s, whatever N is. The refusal is TERMINAL `PROBE_OVER_BUDGET`, which is INSUFFICIENT and consumes #581 (design §4.5).
- **What the budget absorbs.** It covers a per-session cost up to 0.318 s, which is 3.6 × the point slope and 1.5 × its 95% upper bound. The dispatch gate (B4) sums actual path CPU, so a mean cost up to 480 s per path also survives path-to-path variation after a cheap probe path. A higher mean would end TERMINAL `BUDGET_EXHAUSTED`.
- **What it does not absorb.** A two-window fit cannot see curvature: a quadratic term consistent with the 20- and 40-session data could put one path in the thousands of seconds, and the probe would refuse it.
- **The cheap lever, and its cost.** You can raise the multiplier, for example to 3 × upper (960 s per path). That turns a refusal into a longer run, up to about 26 days at N = 5,001, and renewals cover any lapse.
- **A zero-exposure check.** The coordinator can statically read the `replay_bracket` and `evaluate_replay` session loops for per-session work that grows with the window, without running anything. This packet does not do that.

## 5. Recommendation

**N = 5,001 per population (`depth_per_root` 1,667), with a path budget of 7,201,440 CPU s, an overhead reserve of 26,924 CPU s, and approvals running ≥ 13.2 days after the run starts.** This is the smallest listed depth at which misclassification 0.5 pp from the bust ceiling is about 5% per population (4.4% / 6.1%), and below 0.2% at 1 pp. The machine time is 3.7 days at the point estimate and 8.7 days at the upper estimate. N = 3,000 has roughly twice that risk (9–12%). N = 10,002 cuts it to about 1%, but doubles the machine time and does nothing about the upward bias from the pessimistic `UNDETERMINED` count (§2).

**Alternatives:**
- **(A) N = 3,000:** budget 4,320,000 s, reserve 19,177 s, window ≥ 8.0 d. Choose it if the machine cannot be dedicated beyond about 5 days. The risk is 9–12% at ±0.5 pp and ≤ 1% at ±1 pp.
- **(B) N = 10,002:** budget 14,402,880 s, reserve 50,166 s, window ≥ 26.3 d. Choose it if a result near the ceiling must be decisive. It costs 7.4–17.4 machine-days.

## 6. One-line reply

> T00 depth: N = 5,001 per population (depth_per_root 1,667); path_cpu_seconds 7,201,440; overhead_cpu_seconds 26,924; approvals expire ≥ run start + 13.2 d (r3c also covering §8 steps 7–11); no further pre-ratification probe.

For an alternative, substitute its row from §3.

---

## Appendix: arithmetic

**Inputs** (design §6.2–§6.3):
- replay_bracket t(s) = 74.36 + 0.0885 × s CPU s, with the slope's 95% CI [−0.034, 0.211];
- integrity check i = 71.4 s;
- build b = 166–180 s, with 180 used;
- one path = 1,500 sessions with both runs in one call.

**Per-path CPU with the integrity check hoisted:**
- point: 74.36 + 0.0885 × 1,500 − 71.4 = 135.7 ≈ 136 s;
- upper: 74.36 + 0.211 × 1,500 − 71.4 = 319.5 ≈ 320 s.

**Path CPU-h** = 3N × c / 3,600. For N = 5,001: 15,003 × 136 / 3,600 = 566.8, and 15,003 × 320 / 3,600 = 1,333.6.

**Wall (h)** = CPU-h / 8 × 1.25. For N = 5,001: 88.6 h point and 208.4 h upper.

**Overhead CPU** = (b + 2i)(W·S + R) + p = 322.8 × (8S + 8) + 1,100. For N = 5,001, S = ⌈8.68⌉ = 9: 322.8 × 80 + 1,100 = 26,924 s.

**Overhead wall (h)** = (S × 322.8 + 1,100) × 1.25 / 3,600. For S = 9: 1.39 h.

**Path budget** = 1.5 × 320 × 3N = 1,440N. For N = 5,001: 7,201,440 s.
- The probe refusal threshold per path is 7,201,440 / 15,003 = 480 s.
- The implied per-session cost ceiling is (480 − (74.36 − 71.4)) / 1,500 = 0.318 s.

**Approval window (h)** = 1.5 × (upper wall + overhead wall) + 2. For N = 5,001: 1.5 × (208.4 + 1.4) + 2 = 316.7 h = 13.2 d.

**Verify allowance** = 9 × (322.8 + 320) × 1.25 / 3,600 = 2.0 h, assuming serial re-executions with their own epochs.

**Standard error** = √(p(1−p)/N):
- at p = 0.05 and N = 5,001: √(0.0475 / 5,001) = 0.308 pp;
- at p = 0.5: √(0.25 / 5,001) = 0.707 pp.

**Misclassification** (normal approximation), with SE taken at the true p:
- bust, true p < 5%: P(p̂ > 0.05) = 1 − Φ((0.05 − p) / SE_p);
- bust, true p > 5%: Φ((0.05 − p) / SE_p);
- pass, at the 50% floor, mirrors the bust case.

Worked examples at N = 5,001:
- true 4.5%: SE = 0.293 pp, z = 1.705, 4.4%;
- true 5.5%: SE = 0.322 pp, z = −1.551, 6.1%;
- pass at 48%: SE = 0.706 pp, z = 2.83, 0.23%.

The exact binomial check uses P(X > ⌊N/20⌋) and P(X ≤ ⌊N/20⌋) for bust, and P(X ≥ ⌈N/2⌉) for pass. At N = 5,001 it gives 4.30% (true 4.5%), 6.23% (true 5.5%) and 0.233% (pass at 48%). The worst gap from the normal figures across the table is 2.2 pp, at N = 1,002 and true 5.5% (24.4% vs 26.6%).

**Three-population compounding** = 1 − (1 − q)³, where q is the per-population figure at the stated true rate. At N = 5,001 and true 4.5%: 1 − 0.956³ = 12.6%.
