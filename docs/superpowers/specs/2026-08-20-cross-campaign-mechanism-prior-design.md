# Cross-campaign mechanism prior — design spec

**Status:** Design approved (brainstorming skill flow), not yet implemented. $0/K=0 — read-only over already-closed campaigns, no live/in-flight data touched.
**Date:** 2026-08-20
**Authors:** Joshua + Claude Code
**Lives in:** `docs/superpowers/specs/2026-08-20-cross-campaign-mechanism-prior-design.md`

---

## 1. What this is, and what it explicitly is not

A small, deterministic, disclosure-only tool that reads First Passage's own closed-campaign history (`docs/rejected_candidates.md`, `discovery_manifests/*.json`) and produces a **weighted prior over mechanism classes, sourcing channels, and instruments** — i.e., "historically, which kinds of ideas have tended to survive vs. die, and by how much, given how few data points we actually have." A human (or a future scoping session) reads the report before deciding what to source next. Nothing about this mechanism decides anything on its own.

**It is not** a live generation loop. Earlier in this session's arc, the idea was framed as "build an actual small generation loop where a candidate gets scored against a real computed number... closing an RLVR-style loop for real." Working through the design surfaced that the *within-campaign* version of that idea — a miner iterating on live scored feedback before a campaign's CONFIRM freeze — collides directly with this pipeline's pre-registration discipline (every axis a design varies is priced into `K_intrinsic`; iterating on seen scores before freeze is the "grid search after seeing outcomes" pattern already forbidden everywhere). The scope that survived design is narrower and safer: cross-campaign, **read-only over already-closed history**, informing what gets *sourced* next rather than reshaping anything in flight.

**It is not** a fourth instance of this program-week's external-mechanism-mapping move-class (Quintessentials, Anthropic training principles, peer-firm portfolio-construction — all three `DROP`, that move-class's own programme-audit closed `DEGENERATING` with its Rule-2 STRATEGIC budget exactly consumed). This is a home-grown idea about First Passage's own historical data, not an import from outside — it does not draw on that exhausted budget and isn't gated by that audit's stop recommendation.

---

## 2. Background — why this exists

Two of this session's three external-mapping exercises independently surfaced the same architectural gap: every candidate in this pipeline is generated, evaluated, and deployed as an **individually sufficient signal** — nothing pools historical outcomes across campaigns into a prior that shapes where the *next* search looks. Numerai's Meta Model Contribution and WorldQuant's mega-alpha construction both pointed at variants of "combine many things" as the answer; both proposed mechanisms built around that idea were killed on adversarial review (category mismatch with the actual named bottleneck, evidentiary-substitution risk, domain-conflation). This design is a much narrower, differently-scoped answer to a related but distinct question — not "combine candidates into a tradeable portfolio" (which is what got killed), but "learn a weak prior from history about where to look next" (which nothing in this pipeline does today, and which the killed candidates never actually proposed).

---

## 3. Data & tagging schema

**Source corpus:** all 117 entries in `docs/rejected_candidates.md` + the 15 files in `discovery_manifests/*.json`, pooled into one population (not treated as two separate ones).

**Tagged fields** — deliberately reusing `strategy_harvest.md`'s existing vocabulary rather than inventing a new taxonomy (the direct lesson from every candidate killed this session — a new categorical scheme here would itself be a domain-conflation failure):

| Field | Values | Source vocabulary |
|---|---|---|
| `mechanism_tier` | A (fund-first) / B (conditional) / C (graveyard-watch) / unclear | `strategy_harvest.md` §2.1 |
| `sourcing_channel_rank` | 1–6, 1-tie, or n/a (mined, not harvested) | `strategy_harvest.md` §2.3 |
| `target_instrument_family` | e.g. MNQ, GC/MGC, ES, 6E | as stated in the entry |
| `outcome` | `SURVIVED` / `KILLED_AT_ADMISSION` / `KILLED_AT_TEST` / `AMBIGUOUS` | normalized from each entry's own verdict string |
| `provenance` | source path + section/line, date tagged | audit trail, not an analytical field |

**Explicitly cut during design review**, and why:
- **`requirement1_path` (1a/1b)** — an admission-mechanics detail (how economic grounding was established), not a signal about what survives; harvest-channel-only; doesn't add information `mechanism_tier` doesn't already carry for this purpose.
- **`k_intrinsic`** — demoted from a tagged field to "record it only if it's already sitting in the entry, but not part of v1's weighting." The ask is a survival-rate prior, not a cost-efficiency prior; pulling in a second axis before the first one proves useful is unrequested scope.

**Small-N honesty, load-bearing for everything downstream:** ~130 total entries across years of program history means most cells will have single-digit counts. Every reported rate carries its N and a Wilson score interval, never a bare percentage — per this repo's own Rule 1 (small-cell variance prior).

---

## 4. Storage & computation

**Storage:** `lab/research_utils/mechanism_prior_tags.json` — append-only, one record per historical entry (the 5 fields above). New records are appended when a campaign closes. Nothing is ever rewritten.

**Computation:** `lab/research_utils/mechanism_prior.py` — same family as `breadth.py` / `ic_similarity.py`. Reads the tag file, produces three separate **univariate** tables — survival rate by `mechanism_tier`, by `sourcing_channel_rank`, by `target_instrument_family` — each cell showing N and a 95% Wilson score interval. No cross-tabs (the N doesn't support them). The script never calls an LLM; it is pure arithmetic over the persisted tags.

**Output:** a Markdown report, generated on demand via CLI call. No dashboard, no standing process — a disclosure artifact a human reads, not a service.

**Refresh discipline:** no new automation or hooks. Tagging a newly-closed campaign is one LLM call appended to `mechanism_prior_tags.json` as part of that closure's normal wrap-up — manual, same as everything else in this pipeline. The report always reflects whatever's currently in the tag file (never stale by construction), but the *underlying corpus* can lag if a closure's tag is never appended — so every generated report states its own timestamp and the tag file's current entry count, same honesty convention as the K-bank disclosure's "re-read the manifests, do not trust a snapshot."

---

## 5. Pipeline stage & guardrail compliance

**Stage: UPDATE.** This mechanism reads `docs/rejected_candidates.md`, which UPDATE already owns, and stops there — it produces a report; it does not reach into GENERATE and decide anything. A human (or a future GENERATE-stage scoping session) reads the report and decides what to source next; the mechanism itself has no opinion beyond the numbers.

Explicit compliance with the two standing guardrails established this program-week ([`N-2026-08-20-anthropic-training-principles-pipeline-mapping.md`](../../notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md) §4, sharpened in [`N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md`](../../notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md) §4):

- **Evidentiary-substitution guardrail.** The LLM's only role is a one-time classification of already-*settled* history (a closed campaign's own recorded verdict and mechanism description) — it never scores or judges anything live or in-flight. All downstream weighting is deterministic arithmetic. The report is disclosed-only; no gate, script, or decision procedure reads it as evidence of anything.
- **Domain-conflation guardrail, including the sharpened "altitude/stage-reach" form.** Single declared stage (UPDATE). Its only input is UPDATE's own registry; its only output is a report a human reads before a *separate*, unrelated GENERATE-stage decision. It reuses `strategy_harvest.md`'s existing Tier A/B/C and channel-rank vocabulary verbatim — it does not invent a governing taxonomy layered over the pipeline.

---

## 6. Forbidden moves

- Never gates, blocks, or auto-selects anything — disclosure only, matching the harvest channel's existing "disclosed but not gating" K-bank pattern.
- Never crosses tabs (tier × channel × instrument) — the N doesn't support it; a crossed cell with N=1 is noise dressed as signal.
- Never touches a live or in-flight campaign — only closed, already-verdicted entries are eligible for tagging.
- Never invents a new mechanism-class or channel taxonomy — reuses `strategy_harvest.md`'s existing categories exactly.
- Never re-tags an existing entry to "improve" its classification after the fact — a tag is written once at closure time and stands. If a tag is later found wrong, the correction is a **new record** carrying a `supersedes` pointer to the original entry's `provenance` (the original record is never edited or deleted) — same append-only discipline as everything else in this pipeline. The computation script reads only the latest non-superseded record per entry.

---

## 7. Open questions (not blocking implementation)

- The `outcome` normalization (mapping ~130 heterogeneous historical verdict strings onto 4 categories) is itself a real judgment call — the tagging pass should log its own normalization decisions per entry (already covered by `provenance`), so a future reviewer can audit *why* an ambiguous historical entry landed where it did.
- No decision yet on cadence for re-tagging newly-closed campaigns (every closure vs. batched at programme-audit time) — left to whoever executes the first tagging pass to propose, since it has no bearing on the design itself.

---

## 8. Next step

Implementation plan via the `writing-plans` skill.
