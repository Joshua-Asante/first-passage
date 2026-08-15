---
name: futures-anomaly-discovery
description: >-
  Candidate-generation discipline for mining anomalies and features from CME
  futures price/volume data (First Passage / CONSTELLATION). Use whenever running
  the discovery stack — STUMPY matrix-profile motif/discord search, ruptures
  change-point / regime segmentation, tsfresh / catch22 feature extraction,
  hmmlearn HMM regime states, or gplearn / PySR symbolic regression — to generate
  candidate signals or features. Triggers: "mine candidates", "find anomalies",
  "matrix profile", "motif", "discord", "change point", "regime segmentation",
  "extract features", "symbolic regression", "what should we test next",
  "candidate generation", "data snooping", "multiple comparisons", "trial count",
  "pre-register the search". Also covers sourcing candidates from published
  literature rather than mining them — triggers: "harvest", "harvest a
  strategy", "public strategy", "port a published strategy", "seed
  discovery", "external mechanism", "published anomaly". Owns the K
  (trial-count) accounting and the pre-registration manifest that every
  candidate — mined or harvested — must carry into validation. This layer
  GENERATES candidates; it never blesses them. Hand the gate itself to
  strategy-validation; hand when-to-investigate framing to inqhiori. Does NOT
  modify strategy code, allocations, dd_protection, or MC calibration.
---

# Futures anomaly / feature discovery

This is the discovery layer that feeds the gate. Its single job is to generate
candidate anomalies and features **with their trial count K attached** — and to
route them into validation without blessing them. A discord, a change point, a
selected feature, a fitted expression is an **observation**, never a trade.

Boundary: methodology only. This skill does not touch locked strategy code,
allocations, `dd_protection`, or MC calibration — same wall as the other
methodology skills.

## Pipeline shape

Notice-phase mining → **candidate + K** → first-pass multiplicity check →
Inquire-phase falsifiable-H. Discovery lives entirely in the Notice phase: it
surfaces observations. A candidate only crosses into an Inquire-phase falsifiable
hypothesis after its K is registered and it clears the crude multiplicity floor.
From there, `strategy-validation` + `inqhiori` take over.

## Harvest intake — sourcing candidates from published literature (ADR 2026-07-15)

Wide mining is structurally unfundable at current banked K (Q-GATECART-1 M-19:
DSR floor 2.05 at K=3,177 > best in-house edge 1.83). A published mechanism
inverts the cost — the original author paid the mining cost; you pay only the
confirmation cost — entering at K_intrinsic ≤ 3, a beatable floor. This is now
the primary fundable discovery route (worked proof: D5, Baltussen et al. 2021
*JFE* intraday momentum, the only axis to PASS the Q-KBUDGET screen).

Externally-published mechanisms enter **only** via four admission
requirements, checked *before* screening, in [`docs/methodology/strategy_harvest.md`](../../../docs/methodology/strategy_harvest.md):

1. **Economic grounding** — a named mechanism (who loses money and why), **or**
   evidence-robustness in lieu of one for anomalies with no consensus
   mechanism (momentum-class): ≥3 decades covered, ≥3 independent cohorts,
   ≥1 replication ≥10yr post-discovery, no known sign-reversal condition —
   all four required, not a subset.
2. **Cohort-cited per-instrument δ/σ** with a conservative-central +
   decay-haircut reading. No cross-instrument transplants.
3. **Unburned family K-bank** — re-check `discovery_manifests/`; a
   burned family (e.g. GC/MGC) kills the seed regardless of quality.
4. **Confirm-power ≥ 0.50** at the declared panel N (frozen Clause-N
   formula) — daily/intraday event frequency is the practical bar; monthly
   bp-scale mechanisms are presumptively dead (killed twice: D3, D7).

Screen with `lab/research_utils/axis_screen.py` (manifest-driven; screen
constants Cap/DSR/power/K-floor are frozen, never tuned per-seed). **A PASS
never blesses** — it licenses campaign scoping only; downstream (HARV
reachability HARD gate, cost gate, universe gate, realism, survivor scoring)
still binds. **Confirm, don't mine:** K_intrinsic ≤ 3 declared at admission;
any post-admission widening voids the screen and is a new axis.

**Same-units attestation rule (ADR 2026-07-16, `Accepted`):** a §R reachability
attestation only discharges the gate it's simulated *in that gate's own units,
at the basis the gate actually scores on*. Two funded campaigns (D5, H-OD-1)
both confirmed their mechanism yet died at Stage-2 cost-law because §R argued
Sharpe-space against the Stage-6 floor instead of simulating the bp-space cost
gate — see [`strategy_harvest.md`](../../../docs/methodology/strategy_harvest.md)
§1 Requirement 5 for the mandatory cost-law inequality, now checked at both
sourcing time and admission.

## Rule 1 — every candidate carries a K; declare it before you look

Every tool here manufactures multiple-comparisons risk at industrial scale:
STUMPY over thousands of subsequences, tsfresh over hundreds of features, PySR
over vast expression spaces. This is the "explosion" the Simons criterion guards
against. A p-value or a Sharpe read off a mined candidate is meaningless without
the size of the search that produced it.

**Register the search space K *before* examining results.** The bundled script
makes this mechanical. Default lane is **mechanism-first** (SPEC S6 + TNEC-1): it
requires reachability attestation, profile consult, an `--admission-file` JSON that
clears **EM0 / EM2–EM5 + TNEC N-EDGE + DSR-cap / confirm-power** (EM1 0.40R and
D1/D2 are **disclosure-only** — recorded, never refuse; live edge intake is
[TNEC-1](../../../docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md)
N-EDGE: net expectancy > 0 after Req-5 costs, CI excluding 0, DSR ≥
`floor_at_k`), and a `--prereg` path naming this campaign's own frozen
pre-registration body — refuse at open writes **no** manifest
(`ABORT: admission refused (Cap/EM0|N-EDGE|power|…)`). Wide blind mining still
needs an explicit `--lane blind` (legacy 11-key schema; no admission gate, and
`--prereg` omittable there — blind opens stay unbound by design).

`--prereg` exists because W4 (2026-08-07) defines the live minimal gate set as
"G0–G5 + G8, **and any limb a campaign's own frozen prereg still binds**". Before
this flag the binding was an optional, undocumented manifest key that most
campaigns never wrote, so that clause was unevaluable. The check is mechanical —
exists, `.md`, non-empty, inside the repo — and the path is recorded
repo-relative. It does **not** parse the body or judge its freeze status.

```
# Preferred (canonical lab module) — mechanism-first default (SPEC S6):
PYTHONPATH=lab python -m discovery.register_search open \
    --run-id harv_d5_confirm_mnq --tool catch22 \
    --search-space-size 2 --alpha 0.05 \
    --data-window 2010-06-06:2026-01-01 \
    --hypothesis "confirm published intraday-momentum footprint on MNQ" \
    --reachability-attestation path/to/attestation.json \
    --profile-cell MNQ:intraday-momentum \
    --profile-consult path/to/consult.txt \
    --admission-file path/to/admission.json \
    --prereg lab/analysis/<theme>/<slug>/PREREG.md

# Refusal schema (no manifest written): Cap/EM0 when floor_at_k(K)>Cap (K≥4);
# power when confirm-power < 0.50; N-EDGE when supplied net/CI/DSR limbs fail;
# EM2–EM5 as scored. EM1 + D1/D2 are disclosure-only (never refuse reasons).

# Legacy wide mine — must pass --lane blind explicitly:
PYTHONPATH=lab python -m discovery.register_search open \
    --lane blind \
    --run-id qmech_matrix_es_2010_26 --tool stumpy \
    --search-space-size 48000 --alpha 0.05 \
    --data-window 2010-06-06:2026-01-01 \
    --hypothesis "recurrent NY-morning motif in ES 1m distinct from long-continuation beta"

PYTHONPATH=lab python -m discovery.register_search close \
    --run-id qmech_matrix_es_2010_26 --pvalues 0.0002,0.0009,0.004,0.011

# Skill wrapper (same args; forwards to the lab module):
python scripts/register_search.py open \
    --lane blind \
    --run-id qmech_matrix_es_2010_26 --tool stumpy \
    --search-space-size 48000 --alpha 0.05 \
    --data-window 2010-06-06:2026-01-01 \
    --hypothesis "recurrent NY-morning motif in ES 1m distinct from long-continuation beta"

python scripts/register_search.py close \
    --run-id qmech_matrix_es_2010_26 --pvalues 0.0002,0.0009,0.004,0.011
```

`open` binds K to the run and timestamps it (pre-registration as a file, not an
intention). `close` refuses to run without a prior `open` — you cannot declare K
after seeing results. It computes the Bonferroni floor (α/K), BH-FDR survivors at
K, and the expected number of false positives under the global null (K·α), then
emits a manifest whose verdict is **always a hand-off to `strategy-validation`,
never a promotion.** Nothing exits discovery without its manifest.

### Stage-2/4 campaign runner (Mine → Bind-K → Score → emit-matrix)

The missing middle between a pulled dataset and (when re-armed) `universe_gate`
/ `temporal_consistency` lives in `lab/discovery/stage24_runner.py`. It mines
(STUMPY / catch22-covariate / ruptures), binds K_DSR via `discovery.k_count`
(ADR 2026-07-12 non-overlap floor), scores frozen IS rules, and emits the
option-(i) Stage-4 return matrix. Synthetic-only until the
operator authorizes a real `register_search open` / `db_fetch pull`.
**W4:** SPA/PBO path dormant — prefer temporal-consistency + campaign-named
limbs; when calling DSR/`universe_gate`, the module default is `var_trials=1/n`
(audit R5, flipped 2026-08-15). An explicit pin still overrides.

```
# Preferred (canonical lab module):
PYTHONPATH=lab python -m discovery.stage24_runner --synthetic-e2e
PYTHONPATH=lab python -m discovery.stage24_runner --mine-synthetic

# Skill wrapper:
python scripts/stage24_runner.py --synthetic-e2e
```

`universe_gate` defaults to `var_trials=1/n`. Catch22 is covariate-only (0 scored columns). Low-n (≤250 OOS trades)
candidates are flagged `dsr_unreachable_low_n: true`, never silently dropped.

The manifest computes the *cheap* multiplicity triage. The *rigorous* universe-
level correction — White's Reality Check / Hansen SPA / Romano–Wolf, which
re-centre the null across the full searched universe — lives in
`strategy-validation` and needs the returns of all K strategies. This layer just
makes K a recorded fact so that correction is possible.

## Rule 2 — least-overfit tool first, escalate deliberately

Reach for the lower-K, more-constrained option before the flexible one, because
flexibility is snooping surface:
- **catch22 (22 canonical features) before full tsfresh (~800).** Full tsfresh
  only when catch22 is demonstrably insufficient — and its FRESH selection is a
  *per-run* FDR control, not a program-level one.
- **Fixed / criterion-chosen penalties in ruptures**, not a penalty sweep. A swept
  penalty is a researcher degree of freedom; pre-register the sweep if you must.
- **Simple PySR expressions off the Pareto front.** A complex expression that
  barely beats a simple one is overfit; prefer the knee, not the tail.
- **Held-out likelihood for HMM state count**, not fit on the same data.

Per-tool footguns and the K each contributes: `reference/tool-discipline.md`.

## Rule 3 — discovery outputs are candidates, not signals

STUMPY discords are anomalies *by construction*. ruptures change points and
hmmlearn states are **conditioning variables**, not entries. A tsfresh feature is
a covariate. A PySR expression is the highest-suspicion output in the stack and
must clear the strictest OOS plus universe-level correction. None of these is a
strategy until it survives the gate on native micro-era data.

## Explanation is deferred (Simons stage 3)

Discovery does **not** need a mechanism — a survivor eventually does. Do not buy
explanatory data (MenthorQ gamma, SqueezeMetrics GEX/DIX, COT) before a candidate
has survived validation; explanation is the *last* stage, not the first. Mining
without a mechanism is fine; deploying without one is not.

## Red flags — STOP

- Reading a p-value or Sharpe off a mined candidate with no registered K → register first.
- Running `close` without a prior `open` (declaring K after seeing results) → invalid; the script blocks it.
- Sweeping a penalty / feature set / state count and reporting only the best → that sweep IS K; log it.
- Calling a discord / change point / feature / expression a "signal" → it's a candidate; route it to the gate.
- Promoting a candidate straight to strategy without the native-micro OOS gate → hand to `strategy-validation`.
- Reaching for full tsfresh or a deep PySR search as the first move → drop back to catch22 / a bounded search.

## Hand-offs

- **The gate itself + universe-level correction (White RC / SPA / Romano–Wolf, DSR/PBO, CPCV):** `strategy-validation`.
- **Whether a candidate is worth an Inquire-phase question at all; what gates a question:** `inqhiori`.
- **The data these tools run on (cost-gated, proxy-disciplined):** `databento-data`.
- **A candidate that graduates into a Pre-Q / decision artifact:** `brief-authoring`.
- **The campaign this discovery runs inside (Stage-0 universe registration + the ratified rules of evidence):** `git show pre-prune-2026-08-08:docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` (pruned 2026-08-08).
- **Sourcing/admitting a published external mechanism (the four requirements, sourcing tiers, seed manifest):** `docs/methodology/strategy_harvest.md` (ADR `docs/adr/2026-07-15-external-mechanism-harvest-intake.md`).
- **Why the K-ledger / least-overfit-first discipline exists (the statistics):** `docs/methodology/references/statistics-of-tradable-anomalies.md` (Domain 4 = multiplicity; Part II = the stage pipeline).
