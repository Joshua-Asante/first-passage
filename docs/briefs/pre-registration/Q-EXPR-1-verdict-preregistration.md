# Q-EXPR-1 — Verdict pre-registration (H-EXPR)

**Frozen:** 2026-08-18, **before the conversion table is built or scored.**
Parent brief: [`Q-EXPR-1-regularity-expression-conversion.md`](../Q-EXPR-1-regularity-expression-conversion.md).
Operator GO: this session, off
[`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)
§5 packet 2.

The share thresholds, universe rules, and H-positive definitions below are the
packet's declared levers. A verdict computed after moving any of them is void.

**E1 in this file** = the venue/session **intraday capture / flat-by-16:00 ET
envelope** (k=1, no overnight hold). It is **not** MSL slate "E1 HOLD"
(slate-generation pause). Conflating the two voids the read.

---

## §A — Share threshold (all three Hs)

**Each H wins if its positive-count / its own denominator ≥ 0.50.**
Hs are **not** mutually exclusive (packet: all three can win).
**NO-DOMINANT** if no H meets 0.50.

0.50 is majority-of-own-class. It is not tuned after the table exists.

---

## §B — Two tables, three scoring sets

### B1 — Validated-regularity rows (H1 / H3 denominator source)

A row enters iff **all** of:

1. A committed RESULTS / instrument-ledger / `MECHANISMS.md` cell records the
   *object* (not an expression of it) as `RESOLVED`, `SIGNAL-GENERIC`, or a
   replicated correct-sign / anti-attractor fact.
2. The cell is either (a) a **market regularity** (price / volume / structure)
   or (b) a **packet-named meta**: dead-weeks / liveness, regime findings.
3. Conversion success count on that object is 0 (observation A). Every such
   row is treated as expression-orphaned.

**One object, one row.** Replications across instruments (W on US500/NQ/MNQ;
pools on three panels) are notes on the same row, not extra rows.

**Horizon assignment (native):** the bar-aggregation / cascade *layer* at
which the object was measured and resolved, not the hold of a later
expression.

| Token | Rank (high → low) |
|---|---|
| `weekly` | 4 |
| `daily` | 3 |
| `session` | 2 |
| `intradaily-1m` | 1 |
| `operational` | not ranked — H1/H3-ineligible |

**E1-expressible horizon** is frozen as `session` (flat-by-16:00).

**H1/H3-eligible:** native_horizon ∈ {weekly, daily, session, intradaily-1m}.
`operational` metas **must still appear** in the table (partial-table rule)
but are excluded from H1 and H3 denominators.

### B2 — Conversion-attempt rows (evidence; not H1/H3 denom)

Every named expression of a B1 market-regularity row, **plus** every
Q-TXG-1 transfer cell cited by the packet. Required columns: native
horizon · E1-expressible horizon · death stage ∈ {reachability,
cost-hurdle, CI-power, session-legality, never-attempted} ·
gross/(4×RT) at death where measured · stop geometry at death.

Q-TXG-1 is **prior art + evidence rows**, never an independent discovery
([closure](../closures/Q-TXG-1-closure-falsified-at-walls.md)).

### B3 — H2 scoring class (frozen at GO from INDEX)

Exactly these INDEX recently-closed `AMBIGUOUS-HOLD` cells dated
2026-08-08 through 2026-08-16 inclusive that are expressed constructs
or the packet-named CON set:

| Cell | Why it is in the class |
|---|---|
| Q-TNEC-CON-2 | packet-named |
| Q-TNEC-CON-3 | packet-named |
| Q-TNEC-CON-4 | packet-named |
| Q-TNEC-CON-5 | packet-named |
| Q-R2AGRUN-1 | sole window sibling on INDEX (AMBIGUOUS-HOLD 2026-08-08). Association/magnitude cell — **must be scored, must not be silently dropped.** |

No other sibling is added after the table is seen. Route-B FALSIFIED cells
(R2VBUCK, R2FLOW) are not AMBIGUOUS-HOLD and are out of class.

---

## §C — H-positive definitions

### H1 — horizon-mismatch

**Denom:** H1-eligible B1 rows (orphaned validated regularities with a ranked
horizon).

**H1-positive:** `rank(native_horizon) > rank(session)`.
I.e. native ∈ {weekly, daily}.

### H2 — cost-quantization

**Denom:** the B3 class (n=5 as frozen above).

**H2-positive:** death_stage ∈ {cost-hurdle, stop-geometry} **and**
`gross_edge_present = TRUE`.

`gross_edge_present` is TRUE iff the closure records **mean signed gross > 0**
**and** at least one of:

- a placebo p < 0.05 on the signed-gross or edge limb, or
- a CI on signed-gross or per-trade mean that **excludes 0**.

A gross-positive death with placebo-corroborated gross (the packet's CON-2
example, p=0.027) is a hurdle kill, not an edge absence. Signed-gross > 0
with a straddling CI and no placebo fire is **not** `gross_edge_present`.
Association/magnitude deaths (no cost-hurdle stage) are H2-negative even
if they sit in the class.

### H3 — survivor artifact

**Denom:** same as H1 (H1-eligible B1 rows).

**First-screened horizon class:** among those rows, the native_horizon
class whose *earliest committed first-measurement date* (RESULTS authored /
ledger first-measurement / cascade run date — earliest recoverable
committed stamp) is the minimum. Dates come from the committed record
only, after this file exists on disk.

**H3-positive / H3 wins:** the **modal** native_horizon of the H1-eligible
set **equals** that first-screened class **and** the mode's share ≥ 0.50.

**H3 cannot fire** (counts as H3-miss, not as a third verdict by itself)
if two horizon classes share the same earliest date to the calendar day
(cannot discriminate first-screened).

H3 tests clustering at the screening-order's first horizon. It does **not**
require an independent "what markets favor" measure; that alternative is
unidentified in this corpus.

---

## §D — Partial-table / void rules

- Silent exclusion of any row matching B1 / B2 / B3 voids the read.
- A row whose required field is unrecoverable from the committed record
  enters as **BOUNDED** (both extremes stated). If the two extremes
  **disagree** on whether any H meets 0.50, the verdict is
  `AMBIGUOUS-HOLD`. If both extremes agree, that agreed verdict stands
  and the BOUNDED row is disclosed.
- Death-stage labels are taken from the closure/RESULTS language; do not
  re-diagnose a cell to fit an H.

---

## §E — Decision rule

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (conversion is modeled) | ≥1 of H1, H2, H3 meets 0.50 | `INTEGRATE` — admit the firing branch(es)' admission-rule change from the parent packet; non-firing Hs stay disclosed-off |
| `FALSIFIED` (NO-DOMINANT) | no H meets 0.50; no voiding BOUNDED disagreement | `STOP` — conversion stays unmodeled; B2 election proceeds on admissibility/power evidence alone |
| `AMBIGUOUS-HOLD` | BOUNDED extremes disagree on whether any H meets 0.50, or H1/H2 miss and H3 is the cannot-fire collision *and* that collision is the only remaining path that could have modeled conversion | `ITERATE` — recover the missing stamp; do not invent |

Per-branch actions (packet; fire only for Hs that won):

- **H1** → next slate admission screens claim horizon vs the E1 envelope.
- **H2** → admission screens projected gross/(4×RT) at native stop geometry;
  the four TNEC-CON AMBIGUOUS-HOLD cells are re-read as hurdle-killed
  (re-proposal through their own bars). R2AGRUN is not rewritten by an H2
  fire unless it itself was H2-positive.
- **H3** → "find more regularities" is demoted; channel election tilts to
  expression-side work.
- **NO-DOMINANT** → no admission-rule change from this Q.

---

## §F — Pinned ex-ante expectation

**Predicted: `RESOLVED` (H1 fires).** Recorded before the table is built:
the notice already named three headline objects at weekly/daily native
layers against a session E1 envelope. That is a **class** prediction, not
a substitute of row counts. H2 and H3 are disclosed, not predicted — the
H2 class mixes hurdle-kills with CI-straddle / association cells, and H3
depends on first-measurement dates not yet read into a scoring table.

Substituting the table to confirm this prediction is the compute step,
not this freeze.

---

## §G — Forbidden moves (inherited; restated for the frozen record)

1. Moving the 0.50 share, the H2 class membership, or `gross_edge_present`
   after any table row is scored.
2. Dropping a B1/B2/B3-matching row because it "doesn't fit."
3. Treating Q-TXG-1 as an independent discovery of cost-tax vs survival.
4. Conflating this E1 (flat-by-16:00 envelope) with MSL "E1 HOLD."
5. Opening Q-TRAINKILL-1 from this close (separate packet; operator GO).
6. Re-reading a TNEC-CON cell as edge-absent if H2 fired and that cell
   was H2-positive.
7. Using `scripts/repo_retrieve.py` output as a sub-rule 8/10 attestation.

---

**Freeze note:** this file must exist on disk, with a recorded sha256,
**before** the RESULTS table is assembled from closures. Same-session
freeze-then-tabulate follows the Q-CONDVAL-1 / Q-ICT-SWEEPFVG-1 pattern.
Commit-ordering evidence lands when the operator commits.
