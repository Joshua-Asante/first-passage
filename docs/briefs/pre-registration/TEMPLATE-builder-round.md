# Builder round template (standing convention, 2026-11-04)

Use this for every strategy-builder round from R2 on, and for R1's owed re-registration. It turns the generation task chain below into fixed fields, so each round is produced the same way. The template decides nothing. Authority stays with the owners linked here, and Joshua's GO is recorded per round.

**Task chain** (zero-K work first, in parallel; trial-spending work last, in series):

| # | Task | K | Who |
|---|---|---|---|
| T1 | Supply map: rank untested cells ([`PROFILES.md`](../../../ops/instruments/PROFILES.md), the [register](../../rejected_candidates.md), domain bars) | 0 | agent |
| T2 | One cell dossier per candidate (Part A §A2) | 0 | agents, in parallel |
| T3 | Reach arithmetic (Part A §A3) | 0 | agent |
| T4 | Card and mechanism test (Part A §A4) | 0 | agent |
| T5 | Round registration (Part B), one GO from Joshua | 0 | agent, then Joshua |
| T6 | Run: [builder](../../../lab/builder/README.md), ledger first | spends | agent (local) |
| T7 | Verdict and routing (Part A §A5, applied mechanically) | — | mechanical |
| T8 | Feedback: ledgers, register and K banks re-rank T1 | 0 | agent |

**Rules this template applies:**
- **The unit is a cell:** instrument × session window × mechanism × target firm.
- **Looks are a per-instrument budget.** K is banked across rounds (`lab/builder/ledger.py` `k()`). The reach bar is D7 ([generation note §9.2](../../notes/2026-11-01-generation-phase-strengthening-DRAFT.md#92-d7-decided-by-claude-under-joshuas-delegation)). Round shape, split, K scope and the mechanism test's status are D9 ([§10.1](../../notes/2026-11-01-generation-phase-strengthening-DRAFT.md#101-d9-the-shape-of-a-builder-round--decided-2026-11-03)). This template links them and never copies their values.
- **Prerequisite before any registration.** The [evaluation-order Addendum 2026-11-08](../../adr/2026-08-30-evaluation-order.md#addendum-2026-11-08--builder-gates-express-the-ten-step-order) requires a mapping of builder gates 5a–5h to the ten-step order, with listed exceptions, or gate 5g moved after the holdout. That mapping must exist before a round freezes.
- **Data movement** ([AGENTS.md](../../../AGENTS.md#public-clone-posture)):
  - Part A is **private**: it lives in `local_artifacts/` and is registered in [`PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256).
  - Part B is **public** and cites Part A only by repo-relative path and sha256.
  - Never publish parameter values, prices, P&L, trade lists or per-trade timestamps.

## Part A: pre-registration draft (private)

```
# PREREG-BUILDER-R<n>: <one-line round name>
Status: DRAFT v<k> · <date> · authorizes nothing until Part B records Joshua's GO

A1 Round envelope
  Prerequisite: gate mapping per the evaluation-order Addendum 2026-11-08, at <path or PR> (no freeze without it)
  Instruments and target firms: <instrument → firm>, cards per instrument per D9
  Data pins: <export path(s)> · sha256 per SHA256SUMS · window <first>..<last>
  Calendar pin: <admitted calendar path> · sha256 <…>
  Engine pin: lab/builder @ <commit> · gates.engine_version() <…>
  Split per instrument: dev_start <…> · dev_end <…> · holdout_end <…> (holdout per D9)
  K: register_search manifest <discovery_manifests/…json>, opened before any data read · k_scope per D9

A2 Cell dossier (one per card; T2)
  Cell: <opaque cell id> = <instrument> × <session window, ET, private> × <mechanism id from ops/instruments/MECHANISMS.md> × <target firm>
  Mechanism: WHO pays (a constraint, not a preference) · WHEN · WHY it persists · HOW it dies, or the 1b evidence-robustness path (strategy_harvest Req 1)
  Prior consult: `scripts/instrument_profiles.py cell <SYM> <mechanism>` output pasted; register hits; domain bars (advisory, Rule 26)
  Venue legality at the target firm: native route · flatten time · product offered · news and hold rules · cross-firm hedging (cite the venue-fact register)
  Distinctness: plain-language statement of how this cell differs from every book at another firm (instrument, session window, mechanism)
  Feed and calendar: instrument, bar size, window and every evaluated session inside the admitted calendar's coverage
  Effect priors: cited cohort win rate / mean win / mean loss or δ/σ with decay haircut, or UNSCREENABLE (never invented, Rule 20)

A3 Reach (T3; arithmetic only, before any data read)
  5f reach at banked K + this card and n development sessions: the fields gates.reachability(k, n) returns (builder README "Reachability line"), copied as computed
  If not reachable under D7: act as D7 directs; Joshua decides any exception
  Power at the expected event count (strategy_harvest Req 4) · barrier feasibility on the firm's geometry (EM screen / firm row) · cost and entry-slip sensitivity per M-16 (printed only; Req 5 deleted 2026-10-24) · risk breadth vs the firm's book per M-21

A4 Card and mechanism test (T4)
  Card: <card id> · sha256 <…> · library blocks only · parameter commitment per D9 (5d neighbours are kill checks only)
  Native expression: closed bars · stop/limit/market only · flat by the firm's time · NinjaScript-expressible for Tradeify targets
  Mechanism test (status per D9): the candidate contract's discriminator fields (observable and statistic · null · expected direction · threshold · coverage and power), measured independently of the payoff

A5 Pre-registered routing (T7)
  Gates: as the engine applies them (gates.py 5a–5g, THRESHOLDS cited not restated; holdout.py), each placed in the ten-step order by the prerequisite mapping and its listed exceptions
  Gate 5h (venue.py) is a standalone module, not wired into gates.py or run.py (builder README): state whether and how this round runs it; the form does not imply it is enforced
  Run integrity: the builder's fail-closed rules (unresolved trades, input DataError) and the evaluation order's EVIDENCE-VOID rule
  Mechanism test: record its outcome under the full Confirm taxonomy, with its precedence (evaluation-order §Confirm verdicts). While the test is not terminal (D9), a typed outcome neither ends a mechanism line nor rescues a card. The builder verdict governs, and any consequence of the typed outcome is Joshua's decision
  Survivor: to Joshua for the forward GO; nothing else is blessed (Rule 25)
  After the run: dated disposition in each instrument ledger (Rule 27); rejection routing per the rejection-patterns owner; K bank updated

A6 Forbidden moves
  Adding, swapping or re-parameterising a card after freeze · choosing a card by any outcome · reading the holdout before the development run is finished · changing THRESHOLDS · per-cell operator asks inside the approved envelope · assuming a venue fact not quoted with source and date
```

## Part B: committed registration (public)

```
# Builder run R<n>, <one-line round name>: committed registration
Status: REGISTERED <date>. Rule 23 requires this before any R<n> card produces a result.

| Item | Value |
|---|---|
| Pre-registration | Part A (private): local_artifacts/<…>/PREREG-BUILDER-R<n>-DRAFT-v<k>.md, sha256 <…> |
| Review log | local_artifacts/<…>, sha256 <…>; Codex rounds and their outcome, within Rule 6's limit |
| Freeze record | local_artifacts/<…>.json, sha256 <…>; pins cards, book series, run spec, data, calendar |
| Run spec | local_artifacts/<…>/run-r<n>.yaml, sha256 <…> |
| Engine | lab/builder at <commit>; gates.engine_version() <…> |
| Gate mapping | evaluation-order Addendum 2026-11-08 mapping at <path or PR> |
| Data | <export path(s)>, pinned in SHA256SUMS; windows <…> |
| Calendar | <admitted calendar path>, sha256 <…> |
| Cells | <opaque cell id> = instrument × mechanism class × target firm; session windows and clock settings stay in Part A |
| K | per instrument: banked <…> + new <…>; register_search manifest <discovery_manifests/…> |
| Reach (D7) | per instrument: the run's reachability_5f values, as computed |
| Authority | Joshua, <date>: "<verbatim GO>" |
| Hash index | every private file above registered in docs/evidence/PRIVATE_EVIDENCE.sha256 |

Engine check: the merged engine matches Part A's gates, split and book rules on the pinned inputs; no card outcome read.
Binding: changing a criterion needs a new version, a new review and a new registration. A survivor goes to Joshua for the forward GO.
```

Worked instance of Part B's table: [R1's registration](2026-11-01-builder-r1-mcl-orb-registration.md). Its one-card re-registration was withdrawn and MCL parked (addendum 2026-11-05).
