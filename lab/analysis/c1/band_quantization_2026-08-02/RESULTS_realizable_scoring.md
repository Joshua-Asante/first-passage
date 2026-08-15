# Sub-100K realizable-book Part A scoring — RESULTS

**Status:** ACTIVE — the realizable 1-leg MYM book FAILS Part A at both 50K tiers (4.54% / 4.29% vs 3.0%); the 2-leg cells reproduce the published clearers exactly and carry no independent information
**Verdict (per FROZEN §6, asserted against the numbers — no criterion moved after data):**
**`RESOLVED-CLEARER-SURVIVES`** — but see §3, which is the load-bearing section.
**Date:** 2026-08-03 (run) · **Pre-registration:** [`2026-08-02-sub100k-realizable-book-scoring-prereg.md`](../../../docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md)
(`SIGNED / FROZEN 2026-08-02 / JA`, freeze commit **`e5dc06d`** — strictly precedes this run, §10 hook 1)
**Runner / report:** [`run_realizable_scoring.py`](run_realizable_scoring.py) · [`realizable_scoring_report.json`](realizable_scoring_report.json) · [`scoring_run.log`](scoring_run.log)
**Engine:** frozen — 10,000 sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on,
corrected geometry (`dd_lock_offset_usd → 1_000_000.0`, **worker-attested per cell**, production
constant verified still `100` after the run). Panel 2020-01-06 → 2026-06-30, 1,692 bdays.
**Cost:** $0 · no K · nothing armed · no locked surface touched · wall 1,194 s.

---

## §1 — Controls (all green; verdict is readable)

| Control | Requirement | Measured | |
|---|---|---|---|
| **C2** standing anchor | `Tradeify_Select_100K` 2-leg @1.00× = 4.74% ±0.15pp | **4.7433%** | **MATCH** |
| **C1** published reproduction (B1) | T-50K = 1.06% ±0.15pp | **1.0600%** (+0.00pp) | **MATCH** |
| **C1** published reproduction (B2) | MFFU-50K = 0.96% ±0.15pp | **0.9633%** (+0.00pp) | **MATCH** |
| **C3** geometry attested | `1_000_000.0` per cell | 4/4 attested | **GREEN** |
| **C4** realized stacks disclosed | per-cell stacks ≤ cap, shape matches allocation | 4/4 | **GREEN** |

---

## §2 — The four frozen cells

| # | Tier | Book | cap_alloc | Realized stacks | Bust | Pass | Floor |
|---|---|---|---|---|---:|---:|---|
| **A1** | `Tradeify_Select_50K` | **1-leg MYM** | 34 / 5 | MYM 34 + MNQ 0 = 34/40 | **4.5367%** | 92.84% | **MISS** |
| **A2** | `MFFU_Rapid_50K` | **1-leg MYM** | 43 / 6 | MYM 42 + MNQ 0 = 42/50 | **4.2933%** | 93.73% | **MISS** |
| **B1** | `Tradeify_Select_50K` | 2-leg | 29 / 11 | MYM 25 + MNQ 11 = 36/40 | **1.0600%** | 98.93% | **CLEAR** |
| **B2** | `MFFU_Rapid_50K` | 2-leg | 39 / 11 | MYM 34 + MNQ 11 = 45/50 | **0.9633%** | 99.03% | **CLEAR** |

Neither A-cell is in the (3.0%, 3.2%] noise band — both are clean misses at ~1.5× the ceiling.

---

## §3 — The load-bearing finding: §4's prior called it, and the A-cells decide it

**§4 deliberately declined to predict the A-cells' direction**, naming two opposing mechanisms:
dropping MNQ *removes variance* (bust down) but *removes diversification and halves cadence*
(bust up). **The second mechanism dominates, decisively:**

> **Removing the low-variance MNQ leg RAISES bust roughly 4×** — T-50K 1.06% → **4.54%**,
> MFFU-50K 0.96% → **4.29%**. The 1-leg MYM book at a 4.0%-trail 50K tier lands almost exactly where
> the 2-leg book sits at the 3.0%-trail 100K tier (4.74%). **The second leg is not ballast; it is
> what makes the sub-100K band clear at all.**

**So the realizable-as-configured sub-100K book does not clear Part A anywhere.** Under the
locked-proportional split — the only allocation currently in force — every FRIENDLY tier below 100K
degenerates to 1-leg MYM ([`RESULTS.md`](RESULTS.md) §1), and that book misses the floor by ~1.5×.

### The B-cells reproduced EXACTLY, and that is a finding about the gate, not about the book

§2.2 pre-registered that B would reproduce the published figures *"modulo an unmodellable clipping
term."* **The term is not merely unmodellable — it is absent.** B1 matched to **+0.00pp** because
the gate consumes an R-normalized daily series in which `cap_alloc` never appears: the B-cell
computation is *identical* to the one that produced the published 1.06%. The re-allocation's real
effect — MYM running a **25**-contract stack where the published cell modeled **34** (−26.5%) — is
invisible to this instrument.

**Consequence, stated plainly: B1/B2 clearing is evidence the harness reproduces, not evidence the
re-allocated book clears.** §4 pre-registered exactly this (*"a B-clear is weak evidence — it mostly
confirms the harness"*), and §8 pre-registered that a B-clear does not rescue the published clearer.
Both hold.

---

## §4 — What the verdict does and does not mean

The frozen §6 fires **`RESOLVED-CLEARER-SURVIVES`** because ≥1 cell cleared with controls green.
That is the pre-registered verdict and it is recorded as such. **It must not be read as "the
sub-100K clearer survived integer realization."** What actually survived is:

- a **2-leg** book that requires a **cap re-allocation nobody has authorized** (Q-CAPALLOC-2 closed
  `RESOLVED-FRAGILE` with the operator electing DECLINE — `69/11` stands, no `LEG_MAP` change), and
- whose clearing figure is a **reproduction**, not an independent measurement of that re-allocation.

Meanwhile the configuration that *is* in force realizes as 1-leg MYM and **fails**.

**Standing rider, unchanged and adverse:** the band study's regime rider for `Tradeify_Select_50K`
@1.00× was corrected on 2026-07-28 to a bootstrap-95th of **6.69% — `RIDER FAIL`** (the published
4.54%/4.49% figures are superseded M-23 artifacts). MFFU-50K's corrected bootstrap remains
**impeached / never re-measured**. So the B-cells' clear already carries a failing regime rider
before the §7 follow-on is even run.

---

## §5 — Dispositions

- **No falsifier discharged.** §4 of the prop-portfolio program discharges only at the frozen
  **$100K×4** set; sub-100K clearing bears on the 2026-11-08 **demotion clause**, never on the
  discharge. §4 status is **UNDISCHARGED**, hard date unchanged.
- **The 11-08 demotion-clause defeat is materially weaker than the published figures imply.** It now
  rests on a 2-leg book that is realizable only under an unauthorized re-allocation whose effect this
  gate cannot evaluate — and the in-force configuration fails. **Whether that still defeats the
  clause is an adjudication, not a measurement, and belongs to the operator.**
- **Nothing is admitted, adopted, or authorized.** No `LEG_MAP` change, no tier change, no eval
  purchase, no rail or sizing change. The live `Tradeify_Select_100K` account is untouched — 69/11
  realizes 2-leg at 79/80 exactly as deployed, and C2 reproduced its 4.74% anchor to 4 decimals.
- **Pre-committed §7 follow-on — RULED `DISCHARGED-BY-REPRODUCTION` (operator, 2026-08-03), and the
  discharge is PARTIAL, not uniform.** Discharge-by-reproduction can only inherit a rider that was
  validly measured. Per limb:

  | Cell | Both-halves limb | Bootstrap-95th limb | §7 status |
  |---|---|---|---|
  | **B1** `Tradeify_Select_50K` | H1 **1.83%** / H2 **0.63%** — both PASS (band rider) | **6.69%** corrected + worker-attested (2026-07-28) ⇒ **`RIDER FAIL`** | **DISCHARGED** — both limbs inherited; verdict inherited is **FAIL** |
  | **B2** `MFFU_Rapid_50K` | H1 **1.67%** / H2 **0.57%** — both PASS (band rider) | **IMPEACHED, NEVER RE-MEASURED** — the published 4.49% is a superseded M-23 process-pool artifact; no valid measurement exists to inherit | **PARTIAL** — halves discharged, **bootstrap NOT discharged** |

  **So B1's rider is closed at FAIL, and B2's bootstrap limb remains formally open.** It is *not*
  re-classified as owed work: B2 is an exact reproduction carrying no independent information, so
  measuring its bootstrap would characterise a book that (a) requires an unauthorized re-allocation
  and (b) already fails the same limb at the sibling tier. **Recorded as `OPEN-BUT-NOT-OWED`** — it
  becomes owed only if the re-allocation is ever authorized, which is the governance decision in §5
  bullet 2. Stating it this way rather than as a blanket discharge, because a blanket discharge would
  assert a measurement that does not exist.
- **The honest next question is not another band cell.** Both realizable shapes are now measured:
  1-leg fails, 2-leg is a reproduction requiring an unauthorized re-allocation. The band direction is
  exhausted as a source of new information without a governance decision.

---

## §5a — Upstream-staleness check (executed 2026-08-03, before the §7 ruling was recorded)

`origin/main` was **8 commits ahead** of this branch's merge-base at the time of recording, with
**CLAUDE.md and STATE.md both changed**. Diffed before writing anything, because a disposition
written against a superseded governance surface is the 2026-07-24 failure mode.

- **Panels: unaffected.** `17920cd` retires `core/data/tv_exports/pepperstone/` + `bar_export/`, not
  `cme/`. All three panels scored here (`15d8b`, `beabf`, `ae744`) remain in the upstream `cme/`
  `SHA256SUMS` at **identical digests**. This run's inputs are intact.
- **⚠ Two different "§4"s — do not conflate.** The upstream governance change concerns the
  **decompound-HOLD ADR's §4 limb 2** (quarterly Pepperstone regime re-MC, now **MOOT** because the
  data is unprocurable post-retirement; the *falsifier* stays LIVE, only the scheduled procurement
  was struck). That is **not** the **prop-portfolio program's §4 falsifier**, which is what this
  study bears on and which is **UNDISCHARGED with the 2026-11-08 hard date unchanged**.
- **No upstream change touches** the band clearers (1.06% / 0.96%), the 11-08 demotion clause, the
  50K tier configs, or the frozen gate.

**Owed, not done here:** this branch is 8 commits behind, so `STATE.md` / `CLAUDE.md` pointer-sync for
this result must be authored **against upstream**, not against the stale local copies. Not attempted
in this pass.

---

## §6 — Audit hook (append-only)

Was any criterion moved after data arrived? **No.** Floor (3.0% ∧ 50%), cell set (4, all pre-named),
allocation-selection rule (max-MYM, operator-approved *before* authoring), tier set (frozen at two),
control pins and tolerances (±0.15pp), and verdict vocabulary all match the FROZEN 2026-08-02
pre-registration. Freeze commit `e5dc06d` strictly precedes this run. The §4 prior — *"B expected to
clear, weak evidence; A direction deliberately unpredicted; the load-bearing cell is A"* — was
recorded before the run and is scored correct on both limbs.

```bash
python lab/analysis/band_quantization_2026-08-02/run_realizable_scoring.py   # exit 2 if controls fail
git log -1 --format=%ci e5dc06d   # freeze; must precede the run artifacts
rg -n "dd_lock_offset_usd" core/firm_rules.py | head -2   # production constant still 100
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-03 | §7 follow-on ruled **DISCHARGED-BY-REPRODUCTION** (operator). Recorded as **partial**: B1 both limbs inherited (verdict FAIL); B2 halves inherited but its bootstrap limb has no valid prior measurement to inherit (published 4.49% is a superseded M-23 artifact) → `OPEN-BUT-NOT-OWED`. §5a upstream-staleness check added: 8 commits ahead, panels unaffected, and the upstream §4 change is the decompound-HOLD ADR's, not the prop-portfolio program's | Claude Code (Opus 5) |
| 2026-08-03 | Run executed per the FROZEN 2026-08-02 pre-registration. Controls 4/4 green. A-cells MISS (4.54% / 4.29%); B-cells CLEAR as exact reproductions (+0.00pp). Verdict `RESOLVED-CLEARER-SURVIVES` per §6, with §3/§4 recording that the clear is a harness reproduction and the in-force configuration fails | Claude Code (Opus 5) |
