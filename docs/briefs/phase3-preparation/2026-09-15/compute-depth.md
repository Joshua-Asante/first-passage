# Simulation depth and compute preparation

**Draft — not submitted for ratification.** Numbers below are design calculations
and synthetic engineering timings, never observed portfolio performance. No
n1/n2/n3/Part A or diagnostic run on real panels was executed.

## Reproduction and verified calculator

Selected code: `scripts/certification_power.py` from merged `4e7a25d`, present
unchanged at base `c86a0a0`; source SHA-256
`4cb7851ec91077c574f5fc20d461cbfe37651b86e3a95942b1cdef262ff7de15`.
Review/merge prerequisite is present in main, not inferred solely from old PR371.
Current tests cover exact-rational speed oracle, inclusive boundary/one-ULP
rejection, all smaller grid sizes, unequal-limb joint formula and CLI compatibility.
Calculator plus fingerprint suites: **150 passed in6.60s**, CPython3.12.14,
2026-09-15, selected worktree sources; no private panel tests involved.

From the isolated worktree (PowerShell), these are verified real flags:

```powershell
$py = 'C:\Users\joshu\multi_firm_operations\.worktrees\a1b-operator-input\.venv\Scripts\python.exe'
$env:PYTHONDONTWRITEBYTECODE = '1'
& $py scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --power 0.80 --dependence frechet --ceiling 0.05 --alpha 0.05 --pass-target 0.50 --step 10 --n-max 8000
& $py scripts/certification_power.py --true-rate 0.03 --true-pass-rate 0.65 --n 970 --ceiling 0.05 --alpha 0.05 --pass-target 0.50
```

The recorded calculation used the identical library functions through
[prepare_compute.py](../../../../ops/c1_rail/qualification/prepare_compute.py); CLI help was checked, and CLI behavior
was exercised by the existing tests. The exact command lines above are reproduction
instructions, not a claim that both were separately timed.

For n and assumed failure probability p, find largest k with
`BinomCDF(k;n,.05)≤.05`; qF=`BinomCDF(k;n,p)`. Speed's smallest certifying count
r satisfies `P(Binomial(n,.5)≥r)≤.05`, calculated with exact rational arithmetic.
qS is probability of obtaining at least r successes at the assumed pass-by200
probability. Dependence-valid Fréchet lower bound:
`max(0,1−3(1−qF)−(1−qS))`. Linear scan step10 finds first qualifying n;
joint power is not assumed monotonic. The old equal-q cube is insufficient.

| Design-only failure/pass-by200 assumptions | n per FULL/H1/H2 | qF | qS | Joint Fréchet |
|---|---:|---:|---:|---:|
| .03 / .65 (primary P1 proposal) | 970 | .9386202050 | .9999999999999979 | .8158606150 |
| .03 / .60 (sensitivity) | 970 | .9386202050 | .9999977290 | .8158583440 |
| .02 / .60 (sensitivity) | 390 | .9471837753 | .9896355590 | .8311868848 |

For candidate970, each failure limb permits at most37 failures; FULL speed
requires at least512 pass-by200 observations. Failed/unresolved attempts enter
failure denominators and T=∞. These are acceptance-count **design cutoffs**, not
qualification outputs. No statement is made that the portfolio's actual rates
equal any assumption. The proposal retains970;390 is not selected because a
more favourable assumed alternative yields a smaller calculation.

## Proposed workload accounting

| Workload | Exact candidate count | Notes |
|---|---:|---|
| E1 n1 | 3×200=600 | screen only; all three failures≤10 to continue |
| E1 n2 | 3×970=2,910 | speed reuses FULL970; Part B is existing H1/H2 |
| E1 Part A ordinary | 100×200=20,000 | separate n2/REGIME children |
| E1 Part A reserved maximum | 200×200=40,000 | append100 only on prescribed close-call; no extra depth |
| E1 main total | 23,510 ordinary /43,510 reserved maximum | excludes legality, diagnostic parity, bootstrap construction and warmup overhead |
| E2 sole n3, later | 3×970=2,910 | no Part A, no independent speed sample |
| Decision workload across stages | 26,420 ordinary /46,420 maximum | E2 does not run in this assignment |
| Monitoring, later | 600×(18+M)=10,800+600M | baseline +17 perturbation cells +exact seam count M; no reuse of n3 streams |

Legality screen and required chronological NORMAL/PROTECTED diagnostics need
their own exact source-bar counts and costs, not a guessed count of MC paths.
I2 must return those counts and source indices before F1. They are not permission
to run a trial qualification. All real-panel diagnostics remain unrun here.

## Current representative measurements — provisional

The repeated 500-session path and alternate-panel proof measurements in
[representative-workloads.md](representative-workloads.md) supersede the earlier
generic-component proxy for current planning. Exact raw observations and
runtime/source identities are retained with that report. These are invented
adapters and source panels, not accepted private-port or qualification runs.

| Measured shape | Wall minimum / median / maximum |
|---|---|
| Assemble, continuous replay, shared kernel and serialize one 500-session path | 9.489 / 10.090 / 10.352 seconds |
| Generate eight source months, sample six-month outer blocks, continuously prove/rebuild the alternate panel, then replay/kernel/serialize one 500-session path | 10.885 / 11.467 / 13.190 seconds |

Three sequential repeats retained identical output digests for each shape. The
175-session alternate-panel proof is shorter than the intended historical source
population. The workload and adapter complexity therefore do not bound actual
production cost or memory.

| Draft workload | Limited linear illustration |
|---|---:|
| E1: n1=200 and n2=970 per population; 100 Part A panels at depth200 | 65.99 hours |
| Same E1 proposal with 200 Part A panels | 122.14 hours |
| Later sole n3: 970 per FULL/H1/H2, 2,910 paths | 8.16 hours |

These figures exclude initial FULL/H1/H2 proofs, probes, runtime capture and
verification, G1/G2/G5, durable controller receipts, actual source I/O and the
final output inventory. The full signed composition was incomplete at measurement
time. No entire 100/200-panel batch or qualification depth was run. These are
**illustrations, not approved budgets, depth ratification or resource bounds**.
See [tooling-review.md](tooling-review.md) for checkpoint acceptance and
[production-readiness.md](production-readiness.md) for actual evidence still owed.

## Historical component benchmark

Code: [prepare_compute.py](../../../../ops/c1_rail/qualification/prepare_compute.py), SHA-256 recorded in
[compute-observation.json](compute-observation.json). Refreshed2026-09-16T00:14:14Z after moving executable code into the ops layer;
CPython3.12.14, Windows11 build26200, single process. Executable hash and all
observed source pins are in the observation. This historical refresh superseded
the packet's first component timing; the representative measurements above are
the newer planning evidence. Source-free computation was repeated on the implementation base. No actual
account/ports/panels were read.

Workload:25 invented sessions×92 M15 bars×4 generic brokers=9,200 broker-bar
iterations per repeat. Real `TVBrokerEmulator.process_bar/submit` plus real shared
Striker quantity arithmetic run each iteration; one synthetic1-contract entry and
flat per broker/session. Prices are generated under
`phase3-preparation/synthetic-component-benchmark/v1`; synthetic clock begins2000.
The script verifies100 completed round trips and zero final positions/pending
orders but does not publish P&L or call the qualification kernel.
Three repeats, no parallel fan-out:0.5923552s,0.6290197s,0.6794353s;
median0.6290197s, observed maximum0.6794353s. All three completion assertions passed.

Reproduce safely with a fresh output name (fails if the target already exists):

```powershell
$py = 'C:\Users\joshu\multi_firm_operations\.worktrees\a1b-operator-input\.venv\Scripts\python.exe'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONTZPATH = 'C:/Users/joshu/multi_firm_operations/.venv-research/Lib/site-packages/tzdata/zoneinfo'
$out = 'C:\Users\joshu\multi_firm_operations\tmp\phase3-preparation-compute-new.json'
if (Test-Path -LiteralPath $out) { throw 'Choose a fresh synthetic output path' }
& $py ops/c1_rail/qualification/prepare_compute.py | Set-Content -LiteralPath $out -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Preparation calculation failed' }
```

Linear **component-only proxy** per500-session shape:
`0.6794353×500/25=13.588706s`.
E1 maximum proxy `43510×13.588706/3600=164.2346h`;
n3 proxy `2910×13.588706/3600=10.9842h`.
This is not a full replay benchmark or even a guaranteed lower bound: real
strategy signal frequency, early path termination, adapter cost, retained-history
growth, account serialization, I/O, state warmup and bootstrap construction differ.
Scaling25 to500 sessions is an assumption; no uncertainty interval is inferred
from three repeats. The minimum unoptimized shape is not a calibrated full-engine
performance model. These limitations prevent using the proxy as F1's measured
deterministic budget evidence.

**Feasibility hold:** there is no approved numerical CPU-hour budget. The newer
8.16-hour illustrative n3 replay cost is not a complete elapsed-time envelope.
n3 plus adjudication/GO/reseal/build/restart must fit actual B7 validity and
no-activity requirements. Do not capture B7 or launch n3 to measure feasibility.
The complete accepted route still needs a representative synthetic rehearsal.

## Final measurement protocol and deterministic budget

Existing benchmarks provide non-decision-bearing, source-free fixtures through
the continuous pipeline:500 sessions, all four synthetic
adapters, NORMAL/PROTECTED transitions, capacity/takeovers, exact calendar schedule,
adverse marking, duplicate/reversed blocks, warmup, kernel and actual output format.
Single-process, no qualification namespaces; include bounded high-activity and
long-retained-history fixtures and measured peak memory/output volume. Repeat the
same predefined fixtures three times; retain all timings, hardware/power settings,
runtime/source/distribution/dependency hashes and workload shapes. Measure separate
outer-panel construction, index generation, per-path warmup and serialization.
Path and Part A benchmark commands now exist and were exercised; their exact
invocations are in the representative-workloads report. The remaining measurement
extends them through the final accepted controller, full proof population,
runtime capture, durability and output inventory. Existing timings do not close
that composed measurement or actual-workload feasibility requirement.

Freeze B_E1/B_monitor in CPU-seconds and B_n3 in elapsed seconds, with a declared
engineering reserve factor (proposal2× observed maximum, **not a statistical
confidence guarantee**). Use separate measured tFULL,tH1,tH2,tA where shapes differ:

`C_E1 = C_screen + C_diagnostics + C_index + C_A_build(200)
       + (200+970)*(tFULL+tH1+tH2) + 200*d*tA + C_seal`.

Every t includes per-path initialization/warmup/output; overhead is not double
counted. Budget must cover the200-panel reserved maximum before any outcomes.
`C_n3 = 970*(tFULL+tH1+tH2) + C_adjudication + C_GO + C_reseal_build_restart`.
Measured fixtures must bound the **declared engineering envelope**, with explicit
uncertainty; failure to establish it blocks F1, not permission to splice paths.
RC-3 requires a pre-batch runtime check and `NEEDS_CONTEXT` on budget excess.
Do not silently truncate depth, lower horizon, add processors or drop a battery.

Candidate d=200 is a planning proposal: per-panel pass fractions have0.005
resolution, two count steps per1pp close-call band. It is not derived from the
four-limb power calculator (which sizes confirmation populations, not p5 precision),
and200 does not imply a statistical precision guarantee for the regime percentile.
Its exact suitability and compute cost need the post-F1 operator decision.
There is currently **no approved numerical CPU-hour budget**. The costed proposal
is reviewable but not feasible-by-assertion. If final timings/budget do not support
it, F1 must settle a justified positive depth and budget before any result; no
post-observation depth repair is allowed.

## Exact-depth decision text — draft, not submitted

> Following the already recorded first P2 ratification, and only after TB-F1 is
> finalized, ratify the exact Part A depth **200 continuous paths per alternate
> panel** if retained by that freeze. Part A starts with100 six-calendar-month
> replacement-bootstrap panels, each truncated to the original N venue sessions,
> with its own rebuilt five-session inner block index. Use the exact candidate
> construction and RNG rules adopted in the frozen contract. Evaluate nearest-rank
> p5 against.95; within an inclusive1pp band append the preallocated100 panels and
> adjudicate the cumulative200. Retain p5≤FULL point-pass sanity and source-half
> partition sanity, full-depth Part B, and every prescribed failure bound.
> Ratification identifies the **actual frozen contract digest**, **exact positive
> depth**, **accepted integration revision**, **fingerprint tool/runtime/dependency/
> vector digests**, **measured timing report**, **deterministic worst-case cost** and
> **approved numerical budget**. These identities are supplied by F1; none is
> issued by this preparation. If F1 selects another depth, replace200 throughout
> the decision and recompute the full budget before presenting it. This second
> dated addendum activates only the scoped A1 depth supersession. It authorizes
> the already gated E1 sequence, no policy change, additional sample, n3, D0/D1
> approval or deployment.

Coordinator must replace this conditional draft with a literal final decision
that names actual evidence and contains no pending fields. Do not ask for its
approval until F1 is frozen. Existing first-decision approval is reused.
