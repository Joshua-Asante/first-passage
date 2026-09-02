**Theme:** harvest
**Status:** ACTIVE — FTS5-as-Delete falsifier harness results
# FTS5-as-Delete falsifier — RESULTS

**Verdict:** `DELETE-HOLDS` — both frozen limbs PASS on point estimates. **Read the fragility note: limb 1 clears its floor by 2 pairs and its 95% CI straddles the floor.** Limb 2 passes overwhelmingly.
**Current run:** v2, 2026-07-27 — pre-registration [`...-prereg-v2.md`](../../../docs/briefs/pre-registration/2026-07-27-fts5-delete-falsifier-prereg-v2.md), frozen `b04cd15` **before** this harness ran
**Parent:** [`2026-07-27-hermes-agent-adoption-ruling.md`](../../../docs/briefs/programs/2026-07-27-hermes-agent-adoption-ruling.md) limb A (operator ruling `A3` = Delete)
**Harness:** [`falsifier_v2.py`](falsifier_v2.py) · superseded v1 harness [`falsifier.py`](falsifier.py)

---

## Run 2 (v2) — the current record

Fixture: **117 pairs**, 97 distinct targets, 1 dropped by the verbatim-confound guard. Corpus: **906** markdown documents with the SESSIONS family excluded from the candidate pool for both engines.

| Metric | Value |
|---|---|
| `R_fts5@5` | **0.718** (84/117) |
| `R_rg@5` (incumbent) | **0.222** (26/117) |
| Ratio | **3.23×** |

| Frozen limb | Result | Strength |
|---|---|---|
| 1 — `R_fts5@5 ≥ 0.70` | **PASS** | **Marginal.** Floor needs 82 hits; got 84. Margin = **2 pairs** |
| 2 — `R_fts5@5 > R_rg@5` | **PASS** | **Decisive.** Difference 0.496, z ≈ 8.8 |

### Fragility note (limb 1)

95% CI on `R_fts5@5`: **[0.630, 0.792]** (Wilson; normal-approx [0.636, 0.799]). **The 0.70 floor lies inside that interval.** So the honest statement is: the point estimate clears the bar, and the data do **not** establish that true recall exceeds 0.70. Three more misses would have flipped the verdict.

This is reported, not acted on. The pre-registration forbids changing the threshold or the metric now, and the frozen table keys on the point estimate. **The verdict is `DELETE-HOLDS`.** But anyone citing it downstream should carry "≈0.72, CI straddles the floor," never "≥0.70, established."

### What is and isn't established

- **Established, decisively:** deterministic FTS5 retrieval **massively outperforms the incumbent** literal-search baseline over this corpus — 3.2×, z ≈ 8.8. The anti-reimplementation limb is not close. Whatever else is true, this is not a reimplementation of `rg`.
- **Not established:** that recall is high enough in absolute terms to *remove* the cost `Q-XMEM-1` was opened about. At ≈0.72, roughly **one probe in four still misses**, and the interval reaches down to 0.63.

## Frozen disposition, applied

`DELETE-HOLDS` authorizes: build the sidecar, **search + staged write only** (scope frozen in the parent brief — no summarization; that path re-creates the retired weekly-review-feeder).

`DELETE-HOLDS` does **not** close `Q-XMEM-1`. Per parent §6 A3, it becomes *eligible* to close `MOOT` only on a separate operator confirmation that the original cost no longer bites. A recall number cannot supply that confirmation, and the fragility above is a reason to want it explicitly rather than by inference.

## Miss pattern (observation, not re-litigation)

33 FTS5 misses. A recurring shape: the expected document is a **generically-named file** — `STATE.md`, `MECHANISMS.md`, `RUNBOOK.md`, bare `RESULTS.md` — reached because the frozen rule takes the **first** link in an entry, which is sometimes a passing mention rather than that session's principal output. The v2 pre-registration stated this limitation **before the run**: *"first-link may pick an artifact the entry mentions only in passing... this biases against both engines equally; it is a floor on measurable recall, not a differential advantage."*

Also visible: very short queries after identifier-stripping (`adjudicated closed resolved`, `fix k manifest path cite repo root`) carry little signal for either engine.

Both observations are recorded as pre-stated limitations that materialized. **Neither is used to argue the true number is higher** — that would be the post-hoc rescue the forbidden-moves list bars. The measured value is the verdict.

## Run 1 (v1) — superseded, retained for the record

**Verdict was `AMBIGUOUS`** — fixture construction yielded **0 pairs** against a floor of 15; no recall number was computed.

v1 froze a rule harvesting links whose **link text** was ≥4-word descriptive prose from `lab/CATALOG.md` + the two INDEX files. That shape does not exist here: `CATALOG.md` carries **zero** markdown links (pipe table of bare slugs), and INDEX link texts are 1–2 word identifiers (`closure`, `RESULTS`, `pre-reg`). The defect was in the pre-registration, not the corpus — Known Trap #13, precision exceeding grounding, in a brief that cites Trap #13 by name.

v2's correction was procedural: **measure every structural assumption before freezing.** Doing so also rejected the first candidate replacement — brief bodies carry 758 one-word link texts across 134 files and exactly **one** link with ≥4 words, i.e. the same convention that killed v1. Freezing on brief bodies would have produced a second empty fixture.

## Reproduce

```bash
python lab/analysis/fts5_delete_falsifier_2026-07-27/falsifier_v2.py .
# expected: N=117, R_fts5@5 = 0.718, R_rg@5 = 0.222, VERDICT: DELETE-HOLDS
# runtime ~2-3 min (the rg baseline scans the corpus per query)

python lab/analysis/fts5_delete_falsifier_2026-07-27/falsifier.py .
# superseded v1: "fixture pairs constructed: 0" -> AMBIGUOUS
```
