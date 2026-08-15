# Stage-0 verdict pre-registration — `Q-ICT-1MEXEC-1` (ICT 1M execution layer, native MNQ)

**Status:** `DRAFT — NOT FROZEN · NOT SIGNED · NO K BOUND · NO MANIFEST OPENED · NO DATA PULLED`.
This document exists so the operator can decide **whether** to open the track. Nothing here is
ratified, and authoring it consumes no K and fetches no bytes. The freeze event is a separate
commit; the K-bind is a separate `register_search open`; both are gated on the §8 operator GO.

**⚠ Read §2 first. The reachability screen this document is required to carry reads
`FAIL-AS-WRITTEN`.** The admissible annSR band at this campaign's K is **[0.980, 1.000]** — a
0.020-wide window whose floor sits **above every result ever measured on MNQ**. Per
[ADR 2026-07-12](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) §4 clause 4,
*"a campaign whose disclosed minimum exceeds a stated plausible-edge ceiling is malformed and
must not freeze as written."* §8 states the three honest dispositions; the recommended one is
**NO-GO**.

**Campaign:** `Q-ICT-1MEXEC-1` — the ICT raid → FVG → DOL-draw execution layer, reconstructed
offline on native databento MNQ 1-minute data. **Sole anchor: MNQ.**
**Lane:** mechanism-first (requires a non-empty per-clause reachability attestation at
`register_search open` — [`register_search.py`](../../../lab/discovery/register_search.py) `_require_reachability_attestation`, L96–194).
**Occasioned by:** `Q-ICT-MNQ-1` Part C ([`RESULTS_1M_DIAG.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md)),
which removed the *fill-mechanics* objection to a 1M design and explicitly **named but did not
open** this decision: *"that decision is now live for the operator … and it is not opened here."*
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-08-04 · Claude Code (Opus 5), operator-directed.

---

## §0 — Rule-0 reads (production source, verified this session 2026-08-04)

Every anchor below is `git log -1` on this worktree at authoring time.

- **[`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1M_DIAG.md) @ `9aaa578` (2026-08-04)** — the evidence base. Refutes all three testable explanations of US500's 0/247 (raid-conditioning 59.01%; arm-delay flat to 55.91% at 8 bars late; ES 62.33% in the exact 2026-06-24→26 window), localizing it platform-side by elimination. §4 scope limit read in full and binding here: *"Nothing here measures edge. Fill mechanics only; no P&L was computed anywhere in Part C."*
- **[`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1H_1M.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/RESULTS_1H_1M.md) @ `9aaa578` (2026-08-04)** — §1 1H **FALSIFIED** multi-regime (n_eff 1852/1199), so **no PD gate is available to this design**; §2 the 59.06% retrace probe (n=128,089); §2.2 the load-bearing scope limit — the probe measures from the FVG *registration* bar, not from chain validation, so it is **not** the strategy's fill rate.
- **[`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) @ `2c5981e` (2026-08-04)** — W1–W4 standing warnings (W3 now resolved, W4 micro-era proxy discipline binding); **N1** ORB-MNQ-1's realized annSR **+0.890** at `K_eff=2` with the Stage-7 firm rider (**Tradeify $0.91 basis: annSR +0.835 / DSR 0.9644 — FAILS**); **N6** the modern MNQ cost hurdle **3.01 bp/session**; the DEAD list and the standing **F2 guard**.
- **[`docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md`](../../notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md) @ `6d9e603` (2026-08-03)** — `CONFIRM-FREE-NODEPLOY-2026-08-03`. Read in full. Its **first forbidden move is the reason this document must exist at all**: no re-framing of a RESOLVED `Q-ICT-MNQ-1` confirmation as a deploy step *"without a fresh, separate K-bound proposal, authored at that later point, that pays its own K and re-runs the reachability screen against the family bank at that time."* This is that document; §2 is that re-run.
- **[`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)** — the binding K/V rule: `K_DSR` at non-overlap floor, **`V = 1/n` pinned unconditionally** (never the empirical estimator), `DSR ≥ 0.95` retained, and §4 clause 4's **standing power-disclosure requirement** that §2 below discharges.
- **[`lab/archive/q_kbudget_1_2026-07/floor_scan.py`](../../../lab/archive/q_kbudget_1_2026-07/floor_scan.py)** — `CAP = 1.0` (Q-GATECART-1, resolved 2026-07-14) and `floor_at_k`. **Re-executed this session**, not transcribed — see §2 and the §10 hook.
- **[`discovery_manifests/st_eh_supertrend_grid.json`](../../../discovery_manifests/st_eh_supertrend_grid.json) @ `31d7df0`** + **[`discovery_manifests/d5_nq_intraday_mom.json`](../../../discovery_manifests/d5_nq_intraday_mom.json)** — the two banked MNQ-family looks. ST-EH-1 banks **executed** K=2 split **1 MNQ + 1 MYM** (`declared_K=84` recorded, **unbanked**, per [ADR 2026-07-26](../../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-C); D5 banks 1. **`K_banked(MNQ) = 2`**, read from the manifests, not from prose.
- **[`core/firm_rules.py`](../../../core/firm_rules.py) @ `2345095` (2026-08-03)** — `cost_per_side_usd` index micros: Bulenox **$0.61** (L99), Tradeify **$0.91** (L304), MFFU/BluSky-NT **$0.95** (L398). §3 declares Tradeify as the **binding** basis because Tradeify is the live account.
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `cd8b617` (2026-08-02)** — **E1** EOD-flat, build target **16:00 ET** (binding minimum MFFU 16:10 ET; Tradeify 16:45 ET). A 1m intraday layer is E1-compliant by construction; the §1 two-expression rule still requires the `DEPLOYABLE-DEFAULT-ENVELOPE` annotation at closure.
- **[`lab/archive/ict_cascade_2026-06-18/PREREG-1M.md`](../../../lab/archive/ict_cascade_2026-06-18/PREREG-1M.md) @ `47cc3eb`** and **`harness_1m.py`** — the frozen 1M construct this campaign inherits verbatim. Confirmed unmodified: `git diff HEAD -- lab/archive/ict_cascade_2026-06-18/` is **empty** (run this session).

**Citation-chain note (§0 sub-rule, gitignored source).** The deployed `ict_1m_execution_DRAFT.pine` is **lost** — not merely gitignored. It is therefore **not** a Tier-1 source and no constant below is taken from it. All construct constants come from `PREREG-1M.md` prose + `harness_1m.py` (Tier 1, in-repo, hash-stable). This is the same substitution `Q-ICT-MNQ-1` Parts A–C ran under, and it is the reason the vote sub-verdict and the 1H price-BASIS transfer axis are permanently `NOT-RUN`.

**Dedup attestation (executed this session, pasted, not claimed):**

    $ rg -n "ict-liquidity" -A 6 ops/instruments/MECHANISMS.md
    77:## ict-liquidity
    79:ICT-style liquidity-sweep / fair-value-gap geometry (sweep -> FVG -> opposing-pool draw)
       used as an entry signal.
    81:- Class finding: direction real on SPX500 (p=0.0144), fails robustness (drop-top-3 -0.152R)
    82:- Class finding (CORRECTED 2026-08-04): the 0%-fill wall is NOT feed-general -- refuted
    83:- Class finding: liquidity pools are ANTI-attractors on three instruments

    $ rg -rilE "\bFVG\b|fair.value.gap" docs/briefs/
    -> WSTRUCT-M2K-1 (closed, cost-law), SLR-MYM-1 (closed FALSIFIED Stage 0)

`Q-ICT-1MEXEC-1` **declares the existing `ict-liquidity` class** as its vocabulary (not `NEW`) —
its construct *is* the registered sweep→FVG→opposing-pool-draw entry signal. Both prior
`docs/briefs/` hits were read in full: neither is this candidate (WSTRUCT-M2K-1 is the weekly
structure component on M2K; SLR-MYM-1 is a bar-close reclaim on MYM that deliberately avoids the
resting-limit mechanism this campaign keeps).

---

## §1 — Context: why this candidate exists, and the tension named up front

`Q-ICT-MNQ-1` closed complete on 2026-08-04 having re-run the whole ICT cascade on NQ/MNQ at
`$0 / K=0 / no manifest / Cap seat unspent`. Its net result is unchanged from the original US500
campaign: **no layer licenses a deployable edge.** Two structural components confirmed (W weekly
structure RESOLVED on both instruments; D SSL bear-FVG RESOLVED on NQ), the gate layer between
them **FALSIFIED** at ~12× the original's power, the pool leg **FALSIFIED** for a third time, and
the execution layer's blocker **re-characterized rather than removed**.

What changed on 2026-08-04 is narrow and worth stating exactly: Part C removed the *fill-mechanics*
objection. The archived closure had recorded 0-of-247 fills as an instrument-general price law and
predicted it would recur on any fast 1m index; that law is refuted on two instruments across eight
years each, and the 0/247 is now localized to the platform side. **One objection died. No edge was
born.** `RESULTS_1M_DIAG.md` §4 says so in its own words: *"Nothing here measures edge."*

**The tension, named rather than buried.** The honest case *for* opening this campaign is that the
only measured reason to avoid a 1M design has been removed. The honest case *against* is threefold
and each limb is independently sufficient: (i) no ICT layer has ever produced a validated edge on
any instrument or timeframe — `SPX500 × ict-liquidity` is DEAD, `pharos_us500_sweepfvg` FALSIFIED
on robustness (drop-top-3 −0.152R), the 5M substitution INSUFFICIENT-N at n=23 and
drop-top-1-negative; (ii) the 1H gate that the original cascade used to condition entries is
FALSIFIED, so this construct would run *gate-free*, which is weaker than the design that already
failed; and (iii) **the K arithmetic** — §2 — which is the limb that actually decides it.

This document connects to standing doctrine at three points: `CONFIRM-FREE-NODEPLOY-2026-08-03`
(which *requires* a document of exactly this shape before any ICT result may be read as a deploy
step), ADR 2026-07-12 (the K/V rule and its power-disclosure requirement), and the `ops/instruments/MNQ.md`
F2 guard (which forbids the one modification that would otherwise rescue a marginal result).

---

## §2 — K accounting and the reachability screen — `FAIL-AS-WRITTEN`

This is the section the `CONFIRM-FREE-NODEPLOY` forbidden move requires, and it is the reason to
read this document before any other.

### 2.1 K arithmetic (read from manifests)

| Term | Value | Source |
|---|---|---|
| `K_banked(MNQ family)` | **2** | `d5_nq_intraday_mom.json` (1) + `st_eh_supertrend_grid.json` executed split 1 MNQ (1) |
| `K_intrinsic` | **1** | H1 is the sole candidate — one frozen construct, no conditioning gate, no exit variant, no grid |
| **`K_eff`** | **3** | `K_intrinsic + K_banked` |
| `K_SPA` | **1** | recorded distinct from `K_DSR` per ADR 2026-07-12 §2 clause 2 |
| `V` | **`1/n` pinned** | ADR 2026-07-12 §2 clause 3 — never the empirical estimator |

### 2.2 The floor, recomputed (not transcribed)

`floor_at_k` re-executed this session against the production module:

| `K_eff` | 1 | 2 | **3** | 4 | 5 |
|---|---|---|---|---|---|
| annSR floor @ `DSR ≥ 0.95` | 0.650 | 0.850 | **0.980** | 1.060 | 1.115 |
| headroom vs **Cap 1.0** | +0.350 | +0.150 | **+0.020** | −0.060 `CLOSED` | −0.115 `CLOSED` |

**Frequency does not rescue it.** A 1m layer fires far above the ladder's `{0.5,1,2,4}/day` grid,
so the floor was recomputed across the realistic range. It is **flat**:

| trades/day | 0.5 | 4 | 16 | 64 | 123 |
|---|---|---|---|---|---|
| n (6.5y) | 819 | 6,552 | 26,208 | 104,832 | 201,474 |
| annSR floor @ `K_eff=3` | 0.985 | 0.980 | 0.980 | 0.980 | 0.980 |
| implied min **per-trade** SR | 0.0878 | 0.0309 | 0.0154 | 0.0077 | 0.0056 |

High trade count lowers the required *per-trade* Sharpe but leaves the *annualized* floor at
**0.980**. There is no frequency at which this campaign's gate becomes easier on the axis the gate
actually reads. (This discharges ADR 2026-07-12 §4 clause 4's minimum-detectable-Sharpe disclosure.)

### 2.3 The screen — and why it fails

The admissible band is **annSR ∈ [0.980, 1.000]**: floor from `K_eff=3`, ceiling from the ratified
Cap. Against MNQ's own measured record:

| Benchmark | annSR | vs the 0.980 floor |
|---|---|---|
| `ORB-MNQ-1` full window, **Bulenox $0.61** basis (the repo's best-ever MNQ construct, N1) | **+0.890** | **−0.090 FAIL** |
| `ORB-MNQ-1` full window, **Tradeify $0.91** basis — *the live account* (N1 Stage-7 rider) | **+0.835** | **−0.145 FAIL** |
| `D5` intraday momentum, MNQ OOS | gross Sharpe **−0.13** | FAIL |

**The floor sits above everything ever measured on this instrument.** `Q-ICT-1MEXEC-1` would have
to beat the best MNQ result in the repo by **+0.090** (Bulenox) or **+0.145** (Tradeify) — and
land inside a 0.020-wide band before the Cap declares the claim itself not believable.

**Verdict: `REACHABILITY = FAIL-AS-WRITTEN`.** This is a *screen*, not a prediction: it says the
gate is near-unreachable, not that the mechanism is false. But ADR 2026-07-12 §4 clause 4 is
directive, not advisory — a campaign disclosing a minimum this far above its instrument's evidenced
ceiling **must not freeze as written**.

### 2.4 What is *not* an argument for opening it

Stated explicitly because each is locally true and none discharges §2.3:

1. **"Part C removed the fill wall."** It did — and Part C's own §4 says *"Nothing here measures edge."* Removing an objection is not producing an edge.
2. **"W and D are RESOLVED on NQ/MNQ."** They are, and `CONFIRM-FREE-NODEPLOY` forbidden move 1 bars using them as the deployability gate. They are also **leg (a) only** and route to *continued use + a per-entry transfer probe*, never to deploy.
3. **"59% of FVGs retrace."** A fill rate is not an edge. The 59% probe measures from the FVG registration bar, not from chain validation (`RESULTS_1H_1M.md` §2.2).
4. **"The 1H gate could be dropped to simplify."** The 1H is **FALSIFIED**, so there is no PD gate to drop — the design starts without one, which *weakens* rather than strengthens the construct relative to the original cascade.

---

## §3 — Frozen construct (inherited verbatim; nothing re-derived or loosened)

No value is re-tuned. Every constant is cited to `PREREG-1M.md` / `harness_1m.py`, and the
Part-B/C reconstruction already ran against these same values.

| Parameter | Value | Status |
|---|---|---|
| Instrument / panel | `MNQ.v.0` continuous, databento GLBX.MDP3, 1-minute, 2019-05-06 → present | LOCKED |
| Entry | `limit-on-return`, price = **FVG mid**, `retraceK = 6` bars | LOCKED (the exact mechanism that returned 0/247 on US500) |
| Chain | raid (`pvLen = 2`, `raidWin = 8`) → same-direction displacement FVG (`dispMlt = 1.5 × ATR`, `atrLen = 14`) → opposing-pool DOL target | LOCKED |
| Gate stack | **none** — bias / PD / killzone all OFF | LOCKED (1H is FALSIFIED; matches US500's all-gates-off cell) |
| Exit | pre-registered DOL target / stop geometry per `PREREG-1M.md` | LOCKED |
| Roll exclusion | ±4 calendar days of 3rd-Friday Mar/Jun/Sep/Dec, applied at object origin | LOCKED (inherited from `PREREG_D_W.md` §2) |
| **Cost basis (binding)** | **Tradeify $0.91/side** + 1 tick | LOCKED — see below |
| Cost basis (reported, non-binding) | Bulenox $0.61/side + 1 tick | REPORT-ONLY |
| Cost-law bar | **4.0×**, convention `edge / mean_cost_R` | LOCKED |
| Hurdle units | MNQ modern **3.01 bp/session** (N6) | LOCKED |

**Why Tradeify is the binding basis, declared before any result.** `ORB-MNQ-1`'s Stage-7 rider is
the precedent: it passed on Bulenox and **failed on Tradeify**, the account that actually trades.
Reporting the Bulenox figure as the headline would repeat exactly the ambiguity N1 warns about.
This campaign gates on the live account's basis and reports Bulenox only for cross-campaign
comparability.

---

## §4 — Falsifiable hypothesis

**H1 — the sole hypothesis under test (`K_intrinsic = 1`).** The frozen §3 construct, simulated on
native MNQ 1m over 2019-05-06 → present at the Tradeify cost basis, produces a mean gross edge
**≥ 4.0×** the MNQ cost hurdle (Stage 2) **and** a net-of-cost annualized Sharpe **≥ 0.980** with
**DSR ≥ 0.95** at `K_DSR = 3`, `V = 1/n` (Stage 6).

**Falsifier — frozen trigger/threshold table. If any row's trigger fires, then H1 is rejected at
that row's verdict, and no later stage runs.**

| # | Trigger (measured quantity) | Threshold | Action / verdict |
|---|---|---|---|
| F1 | Stage-2 gross edge vs MNQ hurdle, **Tradeify $0.91 basis** | **< 4.0×** | **FALSIFIED at Stage 2.** Campaign closes; Stages 3–8 never run. |
| F2 | Stage-6 net-of-cost annualized Sharpe | **< 0.980** | **FALSIFIED at Stage 6.** |
| F3 | Stage-6 DSR at `K_DSR = 3`, `V = 1/n` | **< 0.95** | **FALSIFIED at Stage 6.** |
| F4 | Realized fill rate on native 1m, armed orders | **< 20%** | **FALSIFIED on mechanics** — and Part C's platform-side conclusion is itself put in question. A pre-committed tripwire against this campaign's own evidence base. |
| F5 | Stage-6 net annualized Sharpe | **> 1.000** (the Cap) | **NOT a pass.** Routes to `AMBIGUOUS-IMPLAUSIBLE` + defect hunt, never promotion. Pre-committed so an implausibly good number cannot be read as success. |

Stated in one line: **if** the construct clears 4.0× at the live account's cost basis **and** lands
in annSR `[0.980, 1.000]` at DSR ≥ 0.95, **then** H1 is RESOLVED; **if** any of F1–F5 fires,
**then** H1 is rejected at that row's verdict.

**AMBIGUOUS** is reserved for: realized `n` below the frozen floor, or a Stage-2 pass with Stage-6
in **[0.850, 0.980)** — i.e. an edge that would have cleared at a lower banked K. That outcome is
recorded and **closed**; it does not license a K re-negotiation.

---

## §5 — Forbidden moves

Each was genuinely available at authoring time; removing this section would change behavior.

- **FM-1 — Adding any conditioning gate, filter, session window, or exit variant.** This is the tempting move and it is arithmetically fatal: it lifts `K_eff` 3 → 4, floor **1.060 > Cap 1.0** — the band **closes entirely**. It is also the exact class `ops/instruments/MNQ.md`'s standing **F2 guard** names as the highest-risk laundering move on this instrument.
- **FM-2 — Re-tuning `retraceK`, `pvLen`, `dispMlt`, `atrLen`, `drawK`, or the roll window after seeing any result.** Manufacturing fills by widening `retraceK` is precisely what the 2026-06-19 session refused to do; that refusal is why the 0/247 verdict was clean enough to later discriminate.
- **FM-3 — Citing `Q-ICT-MNQ-1`'s free W/D RESOLVED verdicts as the deployability gate.** Barred by `CONFIRM-FREE-NODEPLOY-2026-08-03` forbidden move 1. This document pays its own K precisely so that citation is never needed.
- **FM-4 — Switching instrument to dodge the K band.** M2K (bank 0, floor 0.650) and MYM (bank 1, floor 0.850) both have far more headroom, and moving there *to get a better floor* is the instrument-shopping the same ruling names. A move off MNQ requires a **stated non-K justification**, recorded before the switch.
- **FM-5 — Reporting the Bulenox figure as the headline** while the Tradeify basis fails (§3).
- **FM-6 — Treating the 59% retrace rate as edge, or as this construct's fill rate.** It is neither.
- **FM-7 — Re-opening the 1H PD gate.** FALSIFIED twice, the second time at ~12× power on the exact multi-regime data its own re-proposal bar demanded.
- **FM-8 — Any `core/`, lock, allocation, `dd_protection`, Pine, `LEG_MAP`, or rail change.** In particular the c1 rail stays **disarmed** (`dry_run=true`) throughout — this is offline research, and M1 is not `RESOLVED`.

---

## §6 — Verdict gate (binary)

| Verdict | Trigger |
|---|---|
| `RESOLVED` | Stage-2 ≥ 4.0× at Tradeify basis **AND** Stage-6 annSR ∈ **[0.980, 1.000]** **AND** DSR ≥ 0.95 at `K_DSR=3` **AND** within-day placebo p < 0.05 **AND** temporal battery PASS **AND** fill rate ≥ 20% |
| `FALSIFIED` | any §4 falsifier 1–3 fires |
| `AMBIGUOUS-IMPLAUSIBLE` | §4 falsifier 4 (annSR > Cap) |
| `AMBIGUOUS` | `n` < frozen floor, or Stage-6 annSR ∈ [0.850, 0.980) |
| `INSUFFICIENT-N` | fewer than the frozen minimum chain completions on the full panel |

**A `RESOLVED` verdict is not a deploy license.** It licenses exactly one next step: a separate
Cap-seat / manifest / rail-integration decision, which is an operator GO of its own and inherits
the c1 posture (M1 `RESOLVED` + separate arming GO).

---

## §8 — Operator decision gate

**Recommended: NO-GO.** §2.3 is the reason — the gate is near-unreachable on MNQ's own evidence,
and opening it spends the family's last usable K seat to run a test whose pass band is 0.020 wide
and sits above the best result ever measured on the instrument.

| Option | What it means | Cost |
|---|---|---|
| **A — NO-GO (recommended)** | Do not open. Record the reachability screen as the reason. `Q-ICT-MNQ-1` stays closed; MNQ's K bank stays at 2; the Cap seat stays unspent. The ICT track ends on an honest arithmetic wall rather than a null. | $0 · K=0 |
| **B — GO on MNQ as written** | Accept the 0.020 band. Freeze this document, `register_search open --lane mechanism-first` at `K_intrinsic=1`, run Stage 2 first as the cheap kill. | Last MNQ K seat; data $0.00 (regenerable) |
| **C — Re-target the mechanism to a K-clean instrument** | M2K (bank **0**, floor 0.650, headroom 0.350) or MYM (bank **1**, floor 0.850, headroom 0.150). **Requires a stated non-K justification** per §5.4 — and M2K's own ledger warns its bank is *"spendable exactly once"* and *"do not spend this bank on a wide search."* | One K seat on the chosen family |

**If B is chosen**, Stage 2 is deliberately first and cheap: the cost-law screen at the Tradeify
basis kills or clears the construct before any DSR machinery runs, and it is where D5 and H-OD-1
both died.

---

## §10 — Audit hooks (runnable)

**Every hook below was executed at authoring time** (2026-08-04) and its output matched the stated
expectation — including one that did **not** and was corrected (the `floor_scan.py` `__file__`
case, trap M-AHF).

```bash
# This document's status must still read DRAFT until the operator signs §8 (expect >= 1):
grep -c "NOT FROZEN" docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md

# No manifest may exist for this campaign while the status is DRAFT (expect NO match, rc=1):
ls discovery_manifests/ | grep -i ict

# K_banked(MNQ) = 2, read from manifests not prose (expect 1, then "2 operator-stopped"):
python -c "import json;print(json.load(open('discovery_manifests/d5_nq_intraday_mom.json'))['K'])"
python -c "import json;d=json.load(open('discovery_manifests/st_eh_supertrend_grid.json'));print(d['K'],d['closure_mode'])"

# The floor ladder, recomputed rather than trusted (expect: 1.0 [0.65, 0.85, 0.98]).
# floor_scan.py resolves sys.path from __file__, so a bare exec() raises NameError -- inject it:
python -c "import sys;sys.path.insert(0,'lab');p='lab/archive/q_kbudget_1_2026-07/floor_scan.py';g={'__file__':p};exec(open(p).read().split('# Ratified')[0],g);print(g['CAP'],[g['floor_at_k'](k) for k in (1,2,3)])"

# The archived detectors must stay byte-identical (expect EMPTY output):
git diff HEAD -- lab/archive/ict_cascade_2026-06-18/

# The governing ruling this document discharges forbidden-move 1 of (expect >= 1):
grep -c "CONFIRM-FREE-NODEPLOY-2026-08-03" docs/notes/2026-08-03-ict-instrument-confirmation-nodeploy-ruling.md

# The corrected class finding (expect >= 1; "feed-general" must not survive as a live claim):
grep -c "CORRECTED 2026-08-04" ops/instruments/MECHANISMS.md
```

---

## Amendment log (append-only)

- **2026-08-04 — AUTHORED AS DRAFT.** Not frozen, not signed, no K bound, no manifest, no data
  pulled. The §2 reachability screen reads `FAIL-AS-WRITTEN` and §8 recommends **NO-GO**. Authored
  in response to an operator instruction to draft the K-bound pre-registration that
  `CONFIRM-FREE-NODEPLOY-2026-08-03` forbidden-move 1 requires before any ICT result may be
  read as a step toward deployment.
