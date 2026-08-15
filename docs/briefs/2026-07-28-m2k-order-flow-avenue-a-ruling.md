# M2K aggressor-signed order flow: Avenue-A procurement ruling (admit-or-reject)

**Type:** paid-data-procurement-gate ruling (zero-run, zero-K, zero-$ — estimates only). **Authored:** 2026-07-28.
**Source:** the modality wall named in [`wstruct_cost_geometry_2026-07-28`](../../lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md) §7 —
harvest returned **0 screenable seeds** for an asymmetric-payoff M2K mechanism because every non-OHLCV
modality is closed, and buying one is gated.
**Verdict (this brief):** **FALSIFIED (as scoped) — `scoped — not procured`**, blocked at
[Avenue-A](2026-07-24-avenue-a-microstructure-scoping.md) **§6 requirement 3 (survivor-tied)**, which fails
**by construction**. The cost limb passes for the first time; it is not the binding one.
**Precedent template:** [`2026-07-27-f1-moc-imbalance-mym-ruling.md`](2026-07-27-f1-moc-imbalance-mym-ruling.md).

---

## §0 — Rule-0 reads (verified this session, 2026-07-28)

Governing artifact read in full before authoring: `docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md`.

| Path | Anchor | What it grounds |
|---|---|---|
| `docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md` | §6 read verbatim | The **frozen qualifying triple** and the standing disposition *"Avenue A stays scoped-not-procured"* |
| `docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md` | `:15` | Names Avenue-A **"the governing artifact for any paid order-flow procurement"** — the scope limb this ruling turns on |
| `ops/instruments/M2K.md` | **M1**, **M4** | M1 = binding class bar `index-intraday-ohlcv-directional-timing-2026-07-21`; M4 = K bank **0**, `floor_at_k(1)` **0.650** |
| `STATE.md` | `:286-293` | The **$19.91 `mbp-10` escalation was DECLINED 2026-07-24 on "no lever exists"** — add = `floor(base × 7.5)`, pyramid **750% LOCKED**; even WATCH-2 0.25× ⇒ ~52 lots vs median depth **5** |
| `lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md` | §6, §7 | Asymmetric frontier **OPEN** (R ≥ 2.09 at p=0.40, 50bp stop, 1 RT); harvest **0 seeds**; modality is the wall |
| `.claude/skills/databento-data/SKILL.md` | Rule 2 | *"Do not pull `mbp-10` or `mbo` until a candidate has survived on bars"* |
| `docs/methodology/strategy_harvest.md` | Req 2 | Cohort-cited **per-instrument** δ/σ; **no cross-instrument transplants** |

**Prices measured this session** (`db_fetch estimate`, metadata endpoints only — **$0.00 billed**, no pull),
continuous symbology, window `2019-05-06 → 2024-01-01` (2024+ reserved holdout untouched):

| schema | RTY parent | M2K micro | skill Rule 2 |
|---|---:|---:|---|
| `trades` | $140.64 | **$82.69** | permitted |
| `tbbo` | $234.40 | $137.81 | permitted |
| `mbp-1` | $348.37 | — | permitted |
| `mbo` | $475.68 | — | **barred pre-survivor** |
| `mbp-10` | $711.04 | $638.62 | **barred pre-survivor** |

Unit economics: M2K `trades` = **$0.0707/session**; the 450 Wed/Thu ex-FOMC sessions the envelope permits
extrapolate to **~$32** — flagged **first-order**, must be per-day estimated before any action
(standing lesson: never extrapolate span cost from a slice).

---

## §1 — Context

The third-leg line has now failed three times, each time on a different limb, and the failures converge:
Stage-1 screened 8 micros to 4; Stage-2 measured σ and τ_max and found R1 satisfiable; the WSTRUCT
candidate died on **cost** at the deployable round-trip count; and the asymmetric-payoff re-open found the
**arithmetic open but the modality walled**. M2K's own ledger bar M1 is explicit that *"it's a new
instrument" does not clear it* — so an OHLCV-derived directional-timing proposal is barred regardless of
payoff shape.

That leaves buying a new modality. Until this session that was an **unpriced abstraction**. It is now
priced (§0), which converts the question from "what would it cost?" to "does the procurement clear the
gate?" — the gate being Avenue-A, whose §6 triple was **frozen on 2026-07-24** and has never been met.

---

## §3 — Question

**Pre-Q gate test:** stated as a symptom, not a fix.

**Q-A1-M2K:** the third-leg line has failed three times and the surviving obstruction is that every
non-OHLCV modality on M2K is either already rejected, venue-forbidden, or behind a paid gate — and the one
gate that could be opened has never been scored against the case, so it is unknown whether the obstruction
is a budget the operation could choose to spend or a rule it cannot cross.

## §4 — Falsifiable hypothesis

**H-A1-M2K:** an M2K aggressor-signed order-flow procurement (`trades`, or `tbbo`) clears
[Avenue-A](2026-07-24-avenue-a-microstructure-scoping.md) §6's qualifying triple **plus** the cost limb,
and is therefore authorized for a pre-registration.

**If** all three §6 limbs hold (depth-shape **and** not-fill-trivial **and** survivor-tied) **and** the
dry-run lands inside the $125 credit, **then** H holds and the procurement is authorized pending operator
sign-off; **otherwise** H is FALSIFIED and the disposition reverts to `scoped — not procured`.

**FALSIFIED if any one of the three §6 limbs fails** — a single failed limb is decisive and no partial
credit accrues, because the gate is binary on the triple (§6 verbatim: *"A qualifying feature would re-open
toward RESOLVED, never AMBIGUOUS"*).

---

## §5 — Forbidden moves (each genuinely tempting in authoring this ruling)

- **Buying M2K `trades` because $82.69 fits inside the $125 free credit.** The credit is a budget, not an
  authorization. §6 requires the triple **AND** the cost limb, conjunctively. Affordability was never the
  gate; treating the newly-passing cost limb as permission inverts the rule.
- **Re-proposing the $19.91 MYM/MNQ `mbp-10` pull as the "survivor-tied" workaround.** It is survivor-tied
  and it is priced — and it was **declined 2026-07-24 on "no lever exists"** (`STATE.md:288`). Routing a
  closed decision through a new question is decision-laundering. Its own ground is durable and unrelated
  to M2K: no rung fits the add to the book, and realized B7 fills are strictly better evidence and free.
- **Reading `trades` as outside Avenue-A because §6's text says "MBP-10".** The F1 ruling names Avenue-A
  *"the governing artifact for **any** paid order-flow procurement"* (`:15`). Narrowing it to one schema
  would let every cheaper schema walk through a gate built to stop exactly this.
- **Calling aggressor side "depth-shape."** It is not. `trades` carries no book geometry at any price; the
  schema that does is barred by skill Rule 2 pre-survivor and costs $638.62 on M2K.
- **Declaring M1 cleared by asserting "order flow is a new modality."** M1 is the domain raised bar
  `index-intraday-ohlcv-directional-timing-2026-07-21` — canonical three-route test in
  [`docs/rejected_candidates.md`](../rejected_candidates.md) §RAISED BAR 2026-07-21 (route 2 is
  *different modality / venue*, and the registry parenthesises order-flow as untouched until a
  survivor justifies buying it). A modality claim with no cohort-cited Russell δ supplies neither a
  screenable seed (harvest Req 2) nor Avenue-A limb 3. "New modality" is a claim about the data, not
  about an edge. (Earlier drafts of this bullet paraphrased M1 via the OPENPRESS-1 addback text —
  that provenance was false; corrected 2026-07-29 with the ledger reconciliation.)
- **Pricing the pull and calling the pricing itself progress.** It is a measurement, not a step toward
  procurement; recording it as momentum would be the same error as the WSTRUCT cost screen.

---

## §6 — Gate / verdict

Scored against Avenue-A §6's frozen triple (**all three** required, **plus** cost dry-run inside the $125
credit **and** operator sign-off):

| # | §6 limb | M2K aggressor-signed flow | Verdict |
|---|---|---|---|
| 1 | **Depth-shape, not category** — a book-geometry feature MBP-10 *identifies* | `trades`/`tbbo` carry **no book geometry**. The depth schema that would satisfy this is `mbp-10` at **$638.62** (M2K) — 5× the free credit, and independently **barred pre-survivor** by databento Rule 2 | **FAIL** (unsatisfiable at the affordable rung; barred at the rung that could satisfy it) |
| 2 | **Not fill-trivial** — answers something the 1-tick fill model does not | Aggressor-signed volume is not derivable from the 1-tick fill model | **PASS** |
| 3 | **Survivor-tied** — improves/monitors an **admitted survivor**, not blind discovery | M2K has **zero cells, zero admitted mechanisms, K bank 0**. The pull's entire purpose is to *discover* a mechanism | **FAIL — by construction** |
| + | Cost dry-run inside $125 credit | M2K `trades` **$82.69** full-span; **~$32** Wed/Thu-targeted | **PASS** (first time) |
| + | Operator sign-off | not sought — moot on limbs 1 and 3 | n/a |

All three dispositions, stated so the verdict is checkable against its own criteria:

| Verdict | Trigger | Fired? |
|---|---|---|
| `RESOLVED` | All three §6 limbs hold **and** dry-run inside the $125 credit **and** operator sign-off | **no** — limbs 1 and 3 fail |
| `FALSIFIED` | Any one §6 limb fails | **YES** — limb 3 fails by construction; limb 1 fails independently |
| `AMBIGUOUS` | — | **unreachable by construction.** Avenue-A §6 is binary on the triple (*"never AMBIGUOUS"*); recorded here so a later reader does not mistake its absence for an omission |

**VERDICT: `FALSIFIED (as scoped)` → `scoped — not procured`.** Same standing disposition as Avenue-A's
own, and the same wall that closed F1.

**The sharpening this ruling records.** On M2K the procurement gate is **not about money**. For the first
time in this line the cost limb passes — and the gate still shuts, on limb 3, *by construction*: the pull's
value is precisely that no survivor exists yet, which is exactly what limb 3 excludes. That is a
**structural deadlock, not a budget one**, and it is the intended behaviour of the standing rule rather
than an oversight in it.

**Not spent:** no `register_search open`, no manifest, no K, no pull, **$0.00**. M2K's bank remains **0**
(floor 0.650, the widest DSR headroom in the repo, still spendable exactly once).

---

## §7 — Forked questions

1. **The free re-open (cheapest, and the same one F1 names).** A **published cohort δ for aggressor-signed
   flow → Russell/RTY futures response**, citable **without** procurement. That converts the question from
   blind discovery into a *confirm*, which supplies limb 3's survivor-shaped warrant and simultaneously
   satisfies harvest Req 2. Cost: $0. This ruling does **not** claim such a δ was searched for exhaustively —
   only that none surfaced in the 2026-07-28 pass (`wstruct_cost_geometry_2026-07-28` §7).
2. **Does limb 1 need amending for non-depth modalities?** §6's triple was authored against MBP-10 and its
   limb 1 is depth-specific, so a `trades`-shaped proposal cannot satisfy it *in principle*. Either that is
   correct (order flow without book geometry is never admissible pre-survivor) or §6 needs a non-depth
   branch. **Not decided here** — it is moot while limb 3 fails, and amending a frozen gate to admit the
   candidate that just failed it would be gate-drift.
3. **Whether a survivor can emerge on M2K by any free route at all.** M1 bars OHLCV directional timing;
   harvest returns 0 seeds; procurement is gated on having a survivor. If no free route exists, the honest
   reading is that **M2K is not reachable** and its K bank should stay unspent indefinitely rather than be
   spent on the least-bad option.

---

## §10 — Audit hooks (runnable)

```bash
# The frozen gate this ruling is judged against must still say what it says
grep -n "qualifying triple\|scoped — not procured\|scoped-not-procured" \
  docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md

# Avenue-A's scope must still be "any paid order-flow procurement" (if this narrows, re-read §6 limb 1)
grep -n "governing artifact for any paid order-flow procurement" \
  docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md

# Limb 3 turns on M2K having NO admitted mechanism. Expect an empty dict.
python -c "import json;print('M2K cells:', json.load(open('ops/instruments/profiles.json'))['cells'].get('M2K'))"

# The class bar that forces the modality question must still be declared on M2K
grep -c "index-intraday-ohlcv-directional-timing-2026-07-21" ops/instruments/M2K.md

# The survivor-tied pull must still be DECLINED on no-lever (not merely unbought)
grep -n "Do NOT spend the .19.91\|no lever exists" STATE.md

# NOTHING was procured on the back of this ruling: manifest count and cache must be unchanged
ls discovery_manifests/*.json | wc -l          # expect 8
find ~/.databento_cache -name '*.dbn' | wc -l  # expect 481 (no growth from this ruling)

# Re-price if acting later — these are 2026-07-28 quotes, not standing facts
# .venv-research/Scripts/python.exe lab/databento_fetch/db_fetch.py estimate \
#   --symbols M2K.v.0 --stype continuous --schema trades --start 2019-05-06 --end 2024-01-01
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/2026-07-28-m2k-order-flow-avenue-a-ruling.md --type inquire

# §0 anchors resolve
for f in docs/briefs/2026-07-24-avenue-a-microstructure-scoping.md \
         docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md \
         ops/instruments/M2K.md \
         lab/analysis/c1/wstruct_cost_geometry_2026-07-28/RESULTS.md; do
  git log -1 --format="%h %ci $f" -- "$f"; done
```

**Discipline checklist:** §0 populated with paths + anchors ✓ · governing artifact read in full before
authoring ✓ · falsifiable H in §4 with a decisive single-limb trigger ✓ · §5 moves genuinely tempting
(each was live in this session) ✓ · §6 binary on the frozen triple, not re-derived ✓ · question names the
symptom (is the procurement authorized?) not a fix ✓ · §10 runnable, with expected counts ✓ ·
connects to standing doctrine (Avenue-A, F1, M1, harvest Req 2, databento Rule 2) ✓ · decides nothing that
spends ✓.
