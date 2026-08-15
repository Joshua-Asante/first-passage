# Q-ICT-MNQ-1 / 1M diagnostic — VERDICT PRE-REGISTRATION (Part C)

**Registered before any measurement below is computed and before any ES data is pulled. No
criterion may move after the first real run. The commit of this file is the firewall-lift.**

**Part C** — follow-up to [`PREREG_1H_1M.md`](PREREG_1H_1M.md) §3, whose probe returned
`WALL-NOT-CONFIRMED` (59.06% retrace at the frozen `retraceK=6`, n=128,089 — see
[`RESULTS_1H_1M.md`](RESULTS_1H_1M.md) §2) and left US500's **0/247 fills** an *unexplained
fact* with three named, undiscriminated hypotheses. The operator directed a follow-up on the
1M result (2026-08-03). **This is that discrimination — and only that.** It is not the 1M
execution design; it opens nothing.

---

## §0 — Question, governance, and what is already known

**Question:** which of the surviving hypotheses can actually produce 0 fills in 247 attempts?

- **(a1) Arm-delay timing** — the strategy places its limit some bars after FVG registration;
  retraces are fast (median 2 bars), so late arming misses them.
- **(a2) Population conditioning** — the strategy arms only on raid-paired FVGs
  (sweep → same-direction FVG within `raidWin=8`); post-sweep displacement FVGs may retrace
  far less than the unconditioned population.
- **(b) Index-behavior in the US500 window** — the ~2-day 2026-06-24→26 window on an
  S&P-class instrument genuinely did not retrace.
- **(c) Platform-side** — a defect in the deployed (now lost) 1M script, TV's fill engine, or
  the retired Pepperstone CFD feed. **Not directly testable**; survives only by elimination.

**Governance:** order-free measurement, no P&L, no candidate, no manifest, **$0 / K=0 / no Cap
seat**. Same class as the Part B probe. This diagnostic informs the operator's later
execution-design/Cap-seat decision; it does not take it. `harness_1m.py`'s strategy ablation
stays untouched (K-bound, forbidden here as in Part B).

**Already observed (disclosed so the freeze is honest about what it can still bind):** the
unconditioned d=0 rate (**59.06%**), the `retraceK ∈ {3,6,12,30}` curve, and **median
bars-to-touch = 2.0** — the last implies the arm-delay curve will *decline* with d, so §2's
reading rules bind at a level (1.2%) far below anything that shape alone predicts. **Not yet
computed anywhere:** every raid-conditioned quantity, every d>0 cell, all second-touch
behavior, and all ES quantities.

**Source anchoring (Rule 0):** the chain is reconstructed from prose + ported primitives only —
`PREREG-1M.md` (pvLen=2 pools, `raidWin=8` "raid → entry window", limit-on-return/mid/
`retraceK=6`, the B4 arm counts) and `_ict_offline.py` (`pools_from_pivots`, `detect_raid`,
FVG/displacement detectors, all under the archive's 158 passing tests). The lost
`ict_1m_execution_DRAFT.pine` is **not** required. Known unrecoverable pieces and their
declared handling: **stop-distance/DOL geometry filters** (on US500's own B4 table they
removed only 6 cost-skips + 8 no-draw of ~261 setups ≈ 5% — omitted, disclosed as a ≤~5%
population trim that cannot move a §2-scale discrimination); **exact arm bar** (handled by
measuring the full d-curve rather than assuming one d); **raid-direction mapping** (declared
from the mechanism family's own registered definition, `ict-liquidity`: sweep → same-direction
FVG — SSL raid (old low swept) → **bull** FVG; BSL raid (old high swept) → **bear** FVG).

---

## §1 — Measurements (all frozen before any is computed)

Shared mechanics, identical to the Part B probe wherever they overlap: wick-basis displacement
FVGs (`dispMlt=1.5`, `atrLen=14`), roll-excluded origins (±4d of quarterly 3rd Friday),
bar-level touch semantics (bull: `low ≤ mid`; bear: `high ≥ mid`), forward-scan only.

**M1 — raid-conditioned fill rate, MNQ (primary; tests a2).**
Population: displacement FVGs paired to a raid — a `pvLen=2` pool sweep (`detect_raid`;
pools sweepable only **after** their registration bar `t + pvLen`, look-ahead-free) of the
matching side within the preceding `raidWin` bars: `0 ≤ i_fvg − i_raid ≤ 8` (same-bar pairing
allowed; boundary declared now, and a ±1 boundary cannot move a §2-scale read).
Measurement: P(mid touched in `(i, i+6]`) on this population. Data: the already-pulled
`MNQ.v.0` 1m panel.

**M2 — arm-delay curve, MNQ (tests a1, and a1∧a2 jointly).**
P(mid touched in `(i+d, i+d+6]`) for **d ∈ {0,1,…,8}** (d bounded by `raidWin` — validation
cannot plausibly exceed the raid→entry window), computed on (i) all displacement FVGs and
(ii) the M1 raid-conditioned population. A touch before arm does **not** fill a late order —
only touches inside the armed window count (this is what makes fast retraces *miss*).

**M3 — ES cross-check (tests b).**
The Part B probe (d=0, `retraceK=6`), run identically on `ES.v.0` 1m: (i) full era
2019-05-06 → 2026-08-03, per-year table; (ii) the exact US500 window **2026-06-24 → 26**
(tiny n; read for order-of-magnitude only, declared as such). Pull only after this commit,
after a recorded dry-run, `--max-cost` set, `--force` forbidden.

---

## §2 — Frozen discrimination arithmetic (the load-bearing rules)

The bar is set by the 0/247 likelihood itself: a per-attempt fill probability `p` is
*consistent* with 0 fills in 247 attempts (at the 5% level) only if
`(1−p)^247 ≥ 0.05` → **p ≤ 1.21%**. Therefore, for each hypothesis-bearing cell:

| Measured rate | Reading |
|---|---|
| **≤ 1.2%** | **EXPLAINS** — this mechanism alone can produce 0/247 |
| 1.2% – 20% | **CONTRIBUTES-INSUFFICIENT** — real attenuation, cannot alone produce 0/247 |
| **> 20%** | **REFUTED-AS-EXPLANATION** — at p>0.20, P(0/247) < 10⁻²³ |

Applied to, exactly:

1. **(a2):** M1 rate at d=0.
2. **(a1∧a2), generous-to-the-hypothesis:** **min over d ∈ 0..8** of the M2 conditioned
   curve. Designed generous on purpose (cheap-falsifier discipline): if even the most
   favorable arm delay cannot reach ≤1.2%, timing+conditioning is *conclusively* insufficient.
3. **(b):** M3 window rate. **> 20% → REFUTED** (that window on S&P futures retraced
   normally); ≤ 20% at its small n → recorded AMBIGUOUS-b, order-of-magnitude only, with the
   full-era per-year table as context.

**Joint reading, pre-committed:** hypothesis (a) *explains* 0/247 only if cell 2 (the joint,
most-generous cell) is ≤ 1.2%. Partial attenuations do **not** stack into an explanation
claim by narrative. **(c) leads by elimination** only when cells 1–2 are > 20% **and** cell 3
is > 20%. Cross-instrument caveat, standing: every measured rate is an MNQ/ES quantity; the
inference to US500 rides on M3 (index-generality) and is downgraded one grade if M3 is
AMBIGUOUS-b.

**Pre-committed outcome map:**

- **(a) EXPLAINS** → the fill wall is re-characterized as **mechanism-level**
  (retrace-speed vs validation-latency race, and/or conditioning) and is *instrument-general
  again in corrected form* → MNQ ledger W3 re-strengthened accordingly; the naive execution
  design stays dead-shaped; the F9 redesign directions (market-on-validation / near-edge /
  wider `retraceK`) remain K-bound and **unopened**.
- **(a),(b) REFUTED** → **(c) platform-side leads by elimination** → the *operational* wall
  on MNQ is gone; the Cap-seat/execution-design decision becomes live **for the operator**,
  with this diagnostic as its evidence base. Still not opened here.
- **Middle outcomes** → recorded as measured, W3 updated with the decomposition, no
  narrative synthesis beyond the frozen joint rule.

---

## §3 — Forbidden moves

1. **Selecting a d, a pairing boundary, or a `retraceK` after seeing the curves.** The
   verdict cells are §2's three, fixed now; curves are disclosure.
2. **Stacking CONTRIBUTES-INSUFFICIENT cells into an "explains" narrative** — only the joint
   cell ≤1.2% licenses that claim.
3. **Reading any cell as evidence about edge/P&L**, or citing this diagnostic as progress
   toward an execution design. It discriminates hypotheses about a *failure*, nothing more.
4. **Reconstructing the DOL/stop geometry from guesswork** to "complete" the chain — the
   ≤~5% trim is declared and left out; inventing it would add unanchored degrees of freedom.
5. **Running `harness_1m.py`'s ablation**, opening a manifest, or touching the Cap seat.
6. **Pulling ES without the recorded dry-run**, or any pull with `--force`.
7. No `core/`, lock, allocation, `dd_protection`, Pine, or rail change.

## §4 — Audit hooks

```bash
git log --oneline -- lab/analysis/_inbox/ict_mnq_2026-08/PREREG_1M_DIAG.md | tail -1   # lock commit
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/                            # must be EMPTY
grep -n "raidWin\|pvLen = 2\|pv_len" lab/archive/ict_cascade_2026-06-18/PREREG-1M.md lab/archive/ict_cascade_2026-06-18/_ict_offline.py | head
grep -n "247" lab/archive/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md | head -3
```

## Amendment log (append-only)

- **2026-08-03 — RATIFIED** on this file's introducing commit, before any M1/M2/M3 number
  existed and before any ES pull. The 1.2% bar is derived arithmetic (0/247 at the 5% level),
  not a tuned threshold; the 20% bar carries over from Part B §3 unchanged.
