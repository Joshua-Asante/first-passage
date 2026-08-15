# Q-FILLTAX-1 — How large is the TV fill-optimism gap on the reference panels, and is Pine↔Python parity verified or assumed? (VALIDATION)

**Status:** `OPEN` — intaken 2026-08-05; **V2 Phase-0 scaffold `CODE_LANDED` 2026-08-07** (Gen-2 gate under [`lab/analysis/c1/parity_gen2_2026-08/`](../../lab/analysis/c1/parity_gen2_2026-08/); Gate RESOLVED still needs first family TV anchor — operator); `check_brief.py --type inquire` PASS (6/6) at intake
**Authored:** 2026-08-04
**Intaken:** 2026-08-05 (handoff-verify PASS; anchors re-verified at `origin/main` `21e09c8`; V2's CI-tier claim scoped to local/pre-commit — see Amendment log)
**Closed:** N/A
**Authors:** Joshua + claude.ai (advisor); intake + amendment by CC; S1/S3 scaffold note by Cursor
**Parent question:** Q-COSTGEO-3 (closed `AMBIGUOUS — needs depth`; this Q is the depth limb)
**Sub-questions opened:** none yet (**V1** fill-realism tax — *disposition follows S1 / Tradeify geometry; not running in this scaffold*; **V2** parity automation — *executes now at $0 under S1 incumbent env*)
**Loop:** Inquire-phase Pre-Q — closure gates whether a cost-law amendment question opens (ADR-gated) and whether behavioral parity becomes a standing local verification gate
**Artifact path:** `docs/briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md`
**V2 scaffold:** [`lab/analysis/c1/parity_gen2_2026-08/`](../../lab/analysis/c1/parity_gen2_2026-08/) · Phase-0 note [`RESULTS.md`](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md)
**Spend by authoring:** $0 · K=0 · no manifest · nothing armed

> ⚠ **Split 2026-08-04, before lock.** V1 and V2 are independent limbs with different costs, different gates, and different clocks; the original single-brief framing hid that V1 is the largest data spend across the current brief set in service of a book with **no venue**. **V2 executes now at $0 under the S1 incumbent env. V1 disposition follows S1 (Tradeify geometry)** — see Amendment log 2026-08-07 + §7 Sequencing. Both stay in one artifact because they share §0 reads and the parity harness is a V1 input; if V1 is ever cancelled outright, V2 closes on its own row.

---

## Amendment log

### 2026-08-07 — S1 environment + SPEC S3 Phase-0 / V2 scaffold

- **V2 executes now at $0 under S1 incumbent env.** [`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md)
  ratified the live `Tradeify_Select_100K` eval as the environment for **new** strategies
  (F2 warm/disarmed rail; F3 no successor migration now). V2 Phase-0 lands the Gen-2 parity
  scaffold at [`lab/analysis/c1/parity_gen2_2026-08/`](../../lab/analysis/c1/parity_gen2_2026-08/)
  (bands `FROZEN-PRE-RUN` before any family run; synthetic unit tests only). **No parity numbers
  fabricated.** S3 Gate RESOLVED still needs the first family manual TV anchor (operator).
- **V1 fill-realism-tax disposition follows S1 (Tradeify geometry).** The original §7 entry
  condition ("wait for F3 ≠ none / successor") is re-read under S1: there is no successor
  migration now; when V1 is sequenced, thresholds freeze at **Tradeify** incumbent geometry,
  not a hypothetical successor. V1 still does **not** run in this scaffold (no Databento pull).
  The §6 `MOOT` row (F3 = "no admissible successor") is not fired by S1's "stay at incumbent"
  ruling — S1 chose the incumbent as env, not "none forever."
- Spec pointer: [`SPEC S3`](../spec/2026-08-07-loop-s3-arbiter-two-tier-spec.md) Status notes
  `CODE_LANDED` scaffold.

### 2026-08-05 — intake

- **§0 re-anchored** at `origin/main` `21e09c8` (was `613aa0d`); content-diffed, no cited file changed
  in between (`handoff-verify` Phase-0 checklist run in full before this intake).
- **H-V2 and §6's V2 `RESOLVED` disposition corrected: "standing CI gate" scoped to local/pre-commit,
  not GitHub Actions.** The draft's wording ("land the parity harness as a standing CI gate") reads
  naturally as GitHub Actions CI. That is unbuildable as stated: Pine source and the panels are
  gitignored under the public-clone posture (`CLAUDE.md` §Public-clone posture), TV export is a
  manual-only step with no API (`project_tv_egress_automation` — automating TV login/export is
  explicitly barred), and the repo's own CI is **format-only by design**
  (`.github/workflows/manifest-check.yml` cannot re-hash gitignored bytes on GitHub runners, by the
  same constraint). A parity harness comparing a Pine-exported trade list against the Python port
  needs both gitignored inputs on disk, which a GitHub runner never has. Corrected to: the gate lands
  at the **local tier** — a `pre-commit` hook and/or `make validate` target, run on a machine that has
  the gitignored Pine/panel bytes, skip-if-missing on a clean clone (matching every other
  vendor-data-dependent test in this repo's suite). This catches Python-port drift continuously
  (every local commit) and Pine-side drift at each manual re-export — weaker than continuous GitHub
  CI would be, but the only form that can exist given what's gitignored. No other change to V2's
  scope, mutation-battery design, or gate criteria.

---

## §0 — Rule 0 reads

Read this session (anchored at `origin/main` `21e09c8`, 2026-08-05; content-diffed against the
original `613aa0d` anchor — no cited file changed in between):
- `STATE.md`, `docs/SESSIONS.md`, `CLAUDE.md` §posture (incl. §Public-clone posture, confirming Pine + panels gitignored) — via `git show` / diff

Anchored, body unread — `[§0-pending content read before lock]`:
- `docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md` — anchor: `2345095` (2026-08-03) — the parent verdict this Q discharges (verified: verdict wording `AMBIGUOUS-NEEDS-DEPTH` confirmed exact at intake)
- `lab/research_utils/universe_gate.py` — anchor: `e14d548` (2026-07-16) — what the stats gate already enforces (SPA/StepM + DSR + PBO/CPCV) — confirmed at intake: module covers all three
- `lab/analysis/c1/q_rail_1_2026-07/STEP2_PARITY.md` — anchor: `92abdbb` (2026-08-03) — the manual-parity precedent V2 automates
- `core/tv_export_loader.py` — anchor: `cc2fc71` (2026-07-13) — panel parsing law
- `scripts/check_pine_manifest.py` — anchor: `755d07f` (2026-08-03) — pins **source hashes**, not behavior (confirmed at intake: no `behavior`/`parity` string in the file — the gap V2 closes is real)
- `docs/notes/rail_build/RUNBOOK.md` §B6–B7 — anchor: `2345095` (2026-08-03) — measured rail timings for the latency bound

---

## §1 — Context & motivation (with an honest overlap statement)

Every published per-trade economic in this estate — including the two Striker 6-yr venue-edition reference panels feeding live c1 sizing — rests on TradingView bar-magnifier fill semantics whose deviation from ground truth has never been measured. Q-COSTGEO-3 closed `AMBIGUOUS — needs depth` (2026-07-23): this is that depth limb. Databento MBO reconstructs true queue position; hftbacktest's own docs state L2 "market replay" fill estimates are overly optimistic. **Overlap statement (anti-ceremony):** the research report's "formalize the statistics gate" recommendation is ~built here already — DSR ≥ 0.95 pin, permutation/placebo, pre-registration, `universe_gate.py`, K ledger, gate 14. This brief scopes only the two genuine deltas: **V1** the fill-realism tax, **V2** behavioral Pine↔Python parity as a **local verification gate** (`check_pine_manifest` proves source unchanged; STEP2_PARITY proved behavior once, by hand; see Amendment log for why this lands local, not GitHub CI). Anything broader would be re-derivation.

**Why V1 defers (the correction that produced the split).** The Striker legs did not fail at Tradeify on fill margin — they failed on funded-phase economics (1.01 qualifying winning days/mo, 104.7% of net from >40-micro days, $299.80/acct-mo chain) and on the eval-phase activity limb. A 1–2 tick optimism gap would not have changed that verdict, so measuring it now buys a number that moves nothing while spending this brief set's largest data budget on a book with no venue. The gap becomes genuinely decision-relevant at exactly one moment: **after F3 registers a successor and before the first arm at that venue**, when per-side degradation on an 0.85R MNQ edge determines whether the deployed rung's measured bust headroom is real or an artifact of optimistic fills. That is where V1 is sequenced. **V2 has no such dependency** — it is $0, venue-free hygiene closing a real gap (source-hash pinning is not behavioral parity, and behavior has been verified exactly once, manually), and it is a prerequisite input to V1 anyway.

---

## §2 — Prior art / lineage

- Q-COSTGEO-3 closure (`2345095`) — parent; databento re-scoped 2026-07-23 to live-book cost measurement.
- STEP2_PARITY (`92abdbb`) — manual MYM parity override precedent; the shape V2 mechanizes.
- Cost-geometry pre-gate ADR (G3, rides 08-08) — the standing cost-law surface a material V1 gap would feed, via its own ADR, not via this brief.
- Public-clone posture (`CLAUDE.md`) — the gitignore boundary that forces V2's gate to the local tier (intake amendment grounds).
- External: hftbacktest (Databento CME MBO native; queue position + feed/order latency models); trade-csv-reconcile skill (metric definitions — V1 reports in its vocabulary).

---

## §3 — Question (Q-FILLTAX-1)

**Q-FILLTAX-1:** The estate's published edge assumes TV fill semantics never measured against L3 ground truth, and Pine↔Python behavioral parity is asserted from one manual episode rather than continuously verified. How large is the fill deviation on the reference panels, and is parity actually held?

---

## §4 — Falsifiable hypotheses

**H-V1 (deferred — testable only once F3 ≠ none):** If replaying the two Striker legs' entry/exit intents (from the committed panel trade lists) through an L3 queue-position + latency fill model over a pre-registered window yields mean per-side degradation ≥ **T** (set at freeze as ticks/side AND as % of gross edge), then published panel economics carry a material optimism gap and a cost-law amendment question opens — ADR-gated, its own Pre-Q; otherwise TV fills are adequate at current geometry and the simulator archives as calibration evidence.

**Reject H-V1 if:** degradation < T on both legs over the frozen window → the tax is not material; STOP on V1.
**Accept H-V1 if:** ≥ T on ≥1 leg → the amendment question opens (this brief re-scores **nothing** itself).
**Ambiguous-hold if:** estimate unstable below the pre-registered N floor → extend window, cost-gated.

**H-V2:** If a parity harness comparing Pine-exported trade lists against the Python port on a pinned panel detects 100% of a pre-registered injected-mutation battery with 0 false passes, then behavioral parity is enforceable as a **local pre-commit / `make validate` gate** (skip-if-missing on a clean clone, per the public-clone posture — this is not GitHub Actions CI, which cannot see gitignored Pine/panel bytes) and the gate lands; otherwise the harness is not trustworthy and iterates (the harness, never the tolerance).

---

## §5 — Forbidden moves

- **Re-litigating closed verdicts from the gap number** — tempting the moment a big gap prints; a closed verdict re-opens only via its own ruling. V1's output is a question, not a re-score.
- **Tuning the fill model after seeing the gap** ("that looks too big, soften latency") — outcome-conditional; model parameters freeze at §8, calibrated only on data outside the scoring window, with the latency bound derived from RUNBOOK B6/B7 measured timings, not vibes.
- **Treating hftbacktest defaults as ground truth** — its latency/queue models must be parameterized from this rail's own numbers before any verdict is read.
- **Skipping the cost dry-run because "it's only a month"** — the panel era (2020-08→2026-07) sits almost entirely outside Standard's ~1-month included MBO window; V1's history purchase is the dominant spend. Freeze-time choice: score a recent pre-registered sub-window to bound cost, and say so in the verdict's scope line.
- **Widening V1 beyond the two reference legs** — scope creep dressed as thoroughness; two legs, pre-registered window, nothing else.
- **Running V1 before F3 rules, because the harness is ready and the question is interesting** — the sharpest temptation here: V2 will have built most of the scaffolding, the pull is one command away, and curiosity reads as diligence. It buys a number that changes no live decision while spending the largest data budget in the current brief set. V1 waits for a venue; if F3 returns "none," V1 does not run at all and this brief closes on V2's row alone.
- **Claiming V2 lands as GitHub Actions CI** (intake addition) — tempting because "CI gate" is the natural phrase for continuous verification; the repo's own gitignore/CI-format-only architecture makes that specific claim false. State the gate's actual tier (local pre-commit / `make validate`) so nobody later reads "CI-enforced" as "verified on every PR from a clean GitHub runner."

---

## §6 — Gate criteria (closure verdict)

**The limbs close independently.** V2 fires its row on the parity battery alone; V1's row may fire later, or never (F3 = none).

| Limb | Verdict | Trigger condition | Disposition (typed) |
|---|---|---|---|
| **V2** | `RESOLVED` | mutation battery: 100% detection, 0 false passes on the pinned panel | `INTEGRATE — land the parity harness as a standing local pre-commit / make validate gate (skip-if-missing on clean clones); not GitHub Actions CI` |
| **V2** | `FALSIFIED` | any missed mutation or false pass | `ITERATE — repair the harness, never the tolerance; re-run battery` |
| **V1** | `RESOLVED` | ≥ T on ≥1 leg at frozen model params | `INTEGRATE — open the cost-law amendment Pre-Q (ADR-gated); this brief re-scores nothing itself` |
| **V1** | `FALSIFIED` | gap < T both legs at frozen params | `STOP — tax immaterial at that venue's geometry; simulator archived as calibration evidence` |
| **V1** | `AMBIGUOUS-HOLD` | estimate below N floor, or latency bound not establishable from RUNBOOK timings | `ITERATE — extend window (cost-gated) or measure the missing bound; dated re-test` |
| **V1** | `MOOT` | F3 rules "no admissible successor" (per Q-VENUEGEO-1 / ADR 2026-08-04 §7 F3) | `STOP — V1 never runs; brief closes on V2's row; re-proposal bar = a registered venue` |

---

## §7 — Execution plan

**Two tracks, different clocks.**

**Track V2 — executes now, $0, under S1 incumbent env:**
- **Phase 0** — Rule-0 reads (§0 pending list) + Gen-2 scaffold
  ([`parity_gen2_2026-08/`](../../lab/analysis/c1/parity_gen2_2026-08/) — `CODE_LANDED` 2026-08-07;
  bands `FROZEN-PRE-RUN`; no family parity numbers yet).
- **Phase 1** — Freeze the mutation battery (§8).
- **Phase 2** — Run the battery on a pinned same-feed CME TV panel + first family TV anchor
  (operator; S3 Gate RESOLVED condition).
- **Phase 3** — Assert V2's §6 row; land the local gate (pre-commit / `make validate`) on pass.

**Track V1 — disposition follows S1 (Tradeify geometry); not running in this scaffold:**
- **Geometry (2026-08-07).** S1 ratified the incumbent `Tradeify_Select_100K` eval as the
  environment for new strategies (no successor migration now). V1 thresholds, when sequenced,
  freeze at **Tradeify** geometry. Original "wait for F3 successor" entry gate is superseded by
  that reading (Amendment log 2026-08-07); §6 `MOOT` still applies only if a future ruling is
  literally "no admissible venue / never measure."
- **Placement.** Before the first arm that would lean on fill-honest bust headroom — the one
  window where the number changes a decision.
- **Phase V1.0** — Rule-0 re-read incl. extracting B6/B7 measured latencies (re-confirm anchors; they will be months stale by then).
- **Phase V1.1** — Freeze (§8): window, T (ticks **and** %-of-gross), N floor, latency bound, queue model params. Thresholds set at **Tradeify** incumbent geometry per S1.
- **Phase V1.2** — Cost gate: `metadata.get_cost` dry-run; operator ceiling signed. Panel era (2020-08→2026-07) sits almost entirely outside the included MBO window, so a pre-registered sub-window is the likely scope — stated in the verdict's scope line.
- **Phase V1.3** — Pull, replay intents, per-side degradation per leg per order type.
- **Phase V1.4** — Assert V1's §6 row; closure per §9 (gate 14 typed Iterate block).

---

## §8 — Verdict pre-registration

`docs/briefs/pre-registration/Q-FILLTAX-1-verdict-preregistration.md` — committed before Phase 3. Hash/date: `<at prereg commit>`.

---

## §9 — Closure record format

Per `references/closure_record.md`; typed `## Iterate` block mandatory (gate 14 HARD).

---

## §10 — Audit hooks (runnable)

```bash
# Model params + T frozen before any pull
git log --oneline -- docs/briefs/pre-registration/Q-FILLTAX-1-* | tail -1

# Parity harness exists and its mutation battery passes
python -m pytest tests/ -k "parity" -q

# check_pine_manifest still source-only (V2 is additive, didn't quietly rewrite it)
rg -n "behavior|parity" scripts/check_pine_manifest.py

# V2 gate is local, not claimed as GitHub Actions CI (intake amendment)
rg -n "parity" .github/workflows/*.yml   # expect empty — parity gate is NOT a GitHub workflow
rg -n "parity" scripts/install_hooks.sh Makefile   # expect the local gate wiring instead

# No panel/lifecycle surface touched by this Q
git log --oneline --all -- core/strategies/ | head -3   # nothing citing Q-FILLTAX-1

# Latency bound traceable to measured rail numbers
rg -n "latency" docs/briefs/pre-registration/Q-FILLTAX-1-* docs/notes/rail_build/RUNBOOK.md

# Staging held: no V1 data artifact predates the F3 ruling
git log --oneline --diff-filter=A -- lab/analysis/**/filltax*/ | tail -3
rg -n "F3" docs/briefs/Q-FILLTAX-1-*.md STATE.md   # entry condition recorded, not assumed discharged
```

---

## Verification

`check_brief.py --type inquire` run at intake (2026-08-05): PASS (6/6). §0 anchors re-confirmed against `origin/main` `21e09c8`; Q-COSTGEO-3 closure wording grep-matched ("AMBIGUOUS-NEEDS-DEPTH" — exact); `check_pine_manifest.py` confirmed source-only (no `behavior`/`parity` string).

## Pre-Lock Checklist

V2 (now):
- [x] §0 pending reads completed with anchors (re-verified at intake against `21e09c8`)
- [x] Gen-2 scaffold landed (`parity_gen2_2026-08/`, bands FROZEN-PRE-RUN) — 2026-08-07
- [ ] First family TV anchor (operator) — S3 Gate RESOLVED still open
- [ ] Mutation battery frozen before the harness is trusted — owed, Phase 1
- [x] Q-ID confirmed unclaimed (checked HEAD + origin/main at intake, 2026-08-05)

V1 (sequenced under S1 Tradeify geometry; not at lock):
- [x] S1 environment reading recorded (incumbent Tradeify; V1 geometry follows S1) — 2026-08-07
- [ ] Not yet armed (placement window still open)
- [ ] §0 anchors re-confirmed (they will be stale)
- [ ] T set jointly in ticks and %-of-gross at Tradeify geometry, before any pull
- [ ] Latency bound derived from B6/B7 measured numbers
- [ ] Cost dry-run output + signed ceiling attached
