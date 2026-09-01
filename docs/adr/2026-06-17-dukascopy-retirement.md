# ADR 2026-06-17 — Retire Dukascopy; broker-feed BAR EXPORT v0.1 is the canonical bar producer

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - cached `*_duka.csv` retention clause only (§2 "legacy `*_duka.csv` panels are retained as manifest-pinned historical artifacts"). Adapter deletion, BAR EXPORT promotion, and every other clause stand.
**Retain-until:** none
**Decision date:** 2026-06-17
**Authors:** Joshua (decision) + Claude Code (recorder, this session)
**Supersedes:** `2026-06-12-tv-csv-canonical-feed-policy.md` in part - Section 2.3 + Section 4 Forbidden-move #3 (the "tooling retained, not deleted" clause) reversed by operator decision.
**Supersedes:** `2026-06-12-rnd-feed-instrument-class-split.md` full - premise (split R&D feeds by instrument class, Dukascopy serving FX/metals) mooted by full retirement; was Proposed, never ratified.
**Related:** Q-FEED-1 (`docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md`) — closed `RESOLVED-BY-RETIREMENT` by this ADR. Design spec: `docs/spec/2026-06-17-dukascopy-retirement-design.md`. Does NOT affect `docs/spec/feed_equivalence_discovery_test_LOCKED.md` (firm-onboarding execution-feed equivalence — different question).
**Layer:** infrastructure (R&D data-acquisition layer + the governance doctrine over it)

---

## §0 — Rule 0 reads (production-source verification)

All read this session (2026-06-17) before authoring; anchors via `git log -1 --format='%h %ci' -- <file>` in worktree `claude/quirky-davinci-db1578`:

- `core/lib/dukascopy.py` — content anchor `a43919b` (2026-06-07, per prior ADRs); **deleted** this session in `504e4b4`. The retired adapter: bi5-per-UTC-hour tick fetch → OHLCV, mapped point factors, closed-market 5xx skip+count, cross-feed parity caveat documented in its own docstring.
- `lab/validation/sweep/feed_loader.py` — anchor `0020665` (2026-06-06). The **feed-agnostic consumer that STAYS**: `load_bar_feed` reads `core/data/bar_data/*.csv` (`REQUIRED_COLUMNS = time,open,high,low,close`, `+volume` optional; ISO-8601 UTC). It does not care which producer wrote the bars — so this is a producer swap, not a pipeline change.
- `core/bar_export_loader.py` — anchor `5cba8af` (2026-06-17, created this session). The new canonical producer; decode subset promoted from `lab/archive/feed_divergence_2026-06/_lib.py`; imports `PRICE_COL_BY_INSTRUMENT` from `core/tv_export_loader.py` (single source of truth).
- `core/tv_export_loader.py` — anchor `b294993` (2026-06-17). Holds the shared `PRICE_COL_BY_INSTRUMENT` map (GBPUSD added this session).
- `scripts/check_data_manifests.py` — anchor `20e57ad` (2026-06-17). `MANIFEST_DIRS` now includes `core/data/tv_exports/pepperstone/bar_export` (M-9 hash gate covers the bar-export inputs).
- `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` — anchor `6f8063a` (2026-06-12). §2.3 retains tooling; §4#3 forbids deleting it — the supersession target.
- `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` — anchor `034452d` (2026-06-12). PROPOSED, gated on Q-FEED-1; §3(A) rules out full deletion citing the deep-history FX cost; §5 forbids re-proposing (A) absent Q-FEED-1 evidence — the disposition target and the recorded-cost source.
- `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md` — anchor `8a687db` (2026-06-12). OPEN-DRAFT; its closure was the stated gate for "the disposition of the 2026-06-12 Dukascopy-deletion proposal."

---

## §1 — Context

On 2026-06-12 Joshua proposed deleting Dukascopy from the R&D pipeline; the same-day governance response opened Q-FEED-1 (measure the Dukascopy↔TV bar divergence first) and authored two ADRs — one making TV CSV exports canonical for analysis while **retaining** the Dukascopy tooling as staging (`tv-csv-canonical-feed-policy`), and one PROPOSED ADR splitting R&D feeds by instrument class with Dukascopy kept for FX/metals (`rnd-feed-instrument-class-split`), gated on Q-FEED-1. The operator now decides to **completely retire Dukascopy** and standardize all bar data on the TradingView/Pepperstone **BAR EXPORT v0.1** mechanism (a Pine strategy encodes M15 OHLCV into the order Signal field; the List-of-Trades CSV is the transport). The grounds are interpretability of the analysis inputs and fidelity to the actual broker execution feed traded on FXIFY (Pepperstone-via-DXTrade/TV) — the same broker-fidelity argument the class-split ADR accepted for indices, now extended to all classes. This connects to standing doctrine: the BT-OFF/TV-CSV-canonical doctrine (2026-06-12), the parity-gate lesson (feed-source + PF≈1 calibration), and the sweep-engine same-feed discipline.

**Decision driver (one sentence):** the operator chooses one canonical, interpretable, broker-fidelity bar family over a second independent feed, accepting the deep-history cost — and an un-superseded retention clause + a PROPOSED feed-split ADR cannot both stand once the underlying feed is gone, so the disposition must be recorded now.

---

## §2 — Decision

**Decision:** Dukascopy is retired entirely as a bar source. `core/bar_export_loader.py` (BAR EXPORT v0.1 → `core/data/bar_data/<SYMBOL>_M15.csv`) is the canonical bar producer, consumed unchanged by `lab/validation/sweep/feed_loader.py`. The adapter (`core/lib/dukascopy.py`), its test (`tests/test_dukascopy.py`), and Q-FEED-1's panel fetcher (`lab/archive/feed_divergence_2026-06/fetch_duka_panels.py`) are deleted. Five closed-investigation scripts that imported the adapter are frozen in place with banners (the investigations are closed; their records stay). Cached `core/data/bar_data/*_duka.csv` files and `scripts/fetch_oanda_bars.py` (OANDA, a different feed) are out of scope and untouched.

**Effective:** immediately upon acceptance (code landed this session; vendor-data production of canonical `bar_data` runs in the main working copy where the gitignored CSVs live).
**Scope:** all bar-data acquisition for analysis, sweeps, and any verdict from this date onward. Existing closed verdicts are not reopened; legacy `*_duka.csv` panels are retained as manifest-pinned historical artifacts, not regenerated.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Keep the 2026-06-12 instrument-class split** (Dukascopy canonical for FX/metals, TV for indices) | Leaves two bar feeds and a per-instrument-class equivalence argument standing. The operator's broker-fidelity ground applies to FX/metals too: a near-equivalent interbank feed is not the feed traded. Maintaining the adapter + export workflow for one half of the book is the two-source cost the class-split ADR itself flagged. |
| **Deprecate-in-place** (keep `dukascopy.py` as a `NotImplementedError` shim) | Does not satisfy "completely retire"; leaves dead code and a parser parked in a throwaway lab dir. No benefit over deletion given the producer is promoted to `core/`. |
| **Wait for Q-FEED-1 to close on measured divergence, then decide** | Q-FEED-1's question (cross-feed transfer-validity) **dissolves** under retirement: with no Dukascopy in the pipeline there is no cross-feed transfer to validate. Running the measurement first spends effort to inform a decision already made on independent (broker-fidelity) grounds. |
| **Status quo — no decision** | The retention clause (`tv-csv-canonical` §2.3/§4#3) and the PROPOSED class-split ADR both rest on Dukascopy continuing to exist. Deferring leaves contradictory governance on the books while the operator has decided to remove the feed. Worse than recording the disposition. |

---

## §4 — Falsifier (revert trigger)

This ADR accepts a real cost (§6): deep multi-year M15 FX/metals history for `N≥100` and regime-robustness gates is no longer a single programmatic pull — it is manual, TV-plan-capped (~9,000 bars/export pass), multi-pass operator labor. The accepted mitigation is operator-supplied multi-page exports, which `parse_bar_export` concatenates (dedup on bar-open `time`).

**Revert trigger (binary):** if a **pre-registered** deep-history FX/metals gate — an `N≥100` panel OR a regime-robustness half-panel split that a brief floor requires — **cannot be assembled from operator-supplied bar exports within a single working session** (concretely, the export labor exceeds one session for one symbol's required window), the programmatic-feed question is reopened with that dated incident as the anchor.

**Revert action:** supersede this ADR with a fresh one re-evaluating a programmatic, deployment-consistent bar API (TV/broker) as the FX/metals deep-history source. Never edit §4 in place (Known Trap #12).

**Trigger check schedule:** on each occurrence (event-driven, at the moment a deep-history gate is pre-registered and fails to assemble); and reviewed at each quarterly programme audit (next 2026-08-08, aligned with the standing regime trigger).

---

## §5 — Forbidden moves (under this ADR)

- **Re-introducing a programmatic bar feed (Dukascopy or a REST adapter) by convention without an ADR** — Dukascopy's "canonical R&D feed" status originally existed only in PR #152 + handoff briefs, never an ADR; that un-governed convention is exactly what the 2026-06-12 ADRs and this one exist to prevent recurring. A programmatic feed returns only via the §4 revert trigger or a fresh Pre-Q, not by quietly adding an adapter.
- **Citing the retained cached `*_duka.csv` bars as canonical-fresh** — they are frozen historical provenance, not a live feed. Using them to back a new verdict re-introduces the retired feed through the back door.
- **Loosening the §4 trigger after a deep-history gate proves annoying to assemble** — "the export was tedious so we lowered the bar" is `p`-hacking at the methodology layer. The tedium IS the trigger; fire it openly (supersede), do not edit §4.
- **Re-proposing the instrument-class split or full-Dukascopy retention without new mechanism evidence** — those alternatives (§3) are ruled out for stated reasons; reviving one requires evidence invalidating the §3 reason, not renewed cost frustration.
- **Writing producer intermediates (`*_pep.csv`, `*.bars.csv`) into `core/data/bar_data/`** — `bar_data/` holds only canonical `<SYMBOL>_M15.csv`; `feed_loader` would silently load a stray intermediate.

---

## §6 — Consequences

**Positive consequences:**
- One canonical, interpretable bar family that matches the broker execution feed — no per-analysis "is this feed equivalent enough?" argument, and the bars are directly human-readable OHLCV.
- The sweep/validation consumer is unchanged (feed-agnostic); retirement is a producer swap, verified by `feed_loader` round-trip tests.
- Governance is consistent again: no retention clause or PROPOSED class-split ADR resting on a feed that no longer exists; Q-FEED-1's open question is resolved by dissolution.
- One fewer maintained code path (adapter + bi5 fetch machinery deleted).

**Negative consequences (real cost):**
- Deep multi-year M15 FX/metals panels for `N≥100` / regime-robustness gates become manual, TV-plan-capped, multi-pass operator labor instead of one programmatic pull (the cost `rnd-feed-instrument-class-split` §3(A) identified). Accepted, with the §4 falsifier as the safety valve.
- Bar-data acquisition now depends on the operator producing exports on demand; no programmatic refresh.

**Risks:**
- TV plan/export-format changes break BAR EXPORT v0.1. Mitigation: the Entry-`Price` == encoded-`close` cross-check is a format-drift detector that hard-fails on the first malformed row.
- A symbol's window exceeds the ~9,000-bar export cap and the operator forgets a page. Mitigation: multi-page dedup is explicit; a missing page shows as a time gap in the produced bars.

**Downstream artifacts that need updating:**
- `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` — header note: §2.3 + §4#3 superseded by this ADR.
- `docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` — status → Withdrawn/Superseded.
- `docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md` (+ its pre-registration) — status → CLOSED RESOLVED-BY-RETIREMENT.
- `CLAUDE.md` (Public-clone posture: name `bar_export/`, bar_data restoration route) + `REPO_MAP.md` (data-sources note) + `docs/SESSIONS.md` (session entry).
- Memory: `reference_dukascopy_adapter.md`, `project_tv_csv_canonical_feed_policy.md`, `project_rnd_pipeline_state.md`.

---

## §7 — Implementation plan

Executed this session per `docs/spec/2026-06-17-dukascopy-retirement-plan.md` (Tasks 1–8, 10–12 in worktree `claude/quirky-davinci-db1578`):

- **Phase 0** — §0 reads verified current (anchors above).
- **Phase 1** — `core/bar_export_loader.py` + `scripts/parse_bar_export.py` + tests (TDD); GBPUSD added to shared `PRICE_COL_BY_INSTRUMENT`; `bar_export` registered in `MANIFEST_DIRS`.
- **Phase 2** — delete adapter + test + Q-FEED-1 fetcher; frozen-artifact banners on 5 closed-Q scripts; grep-sweep for stale "canonical R&D feed" references.
- **Phase 3** — this ADR + dispositions (§6 downstream); doc/memory updates; verification block.
- **Operator step (main working copy)** — `python scripts/parse_bar_export.py --symbol <SYMBOL>` to produce canonical `bar_data` from the gitignored exports + `check_data_manifests.py --regenerate` to populate `bar_export/SHA256SUMS` and the `bar_data/SHA256SUMS` delta (Task 9; needs vendor bytes absent in the worktree).

---

## §10 — Audit hooks (runnable)

```bash
# No live Dukascopy code remains (only frozen banners + frozen lab artifact + this ADR's references)
grep -rin "from lib import dukascopy\|from lib.dukascopy\|core/lib/dukascopy" --include=*.py . | grep -v "lab/analysis/"
# Expected: empty (no live importer outside frozen lab dirs)

# The 5 frozen scripts carry the retirement banner
grep -rl "Dukascopy retired 2026-06-17" lab/analysis/ | sort
# Expected: noct_spx/fetch_panel.py, tom_spx/fetch_daily.py, custodian_eurusd/fetch_panel.py,
#           silver_regime_2026-06-10/dukascopy_runner_check.py, silver_regime_2026-06-10/dukascopy_feed_equiv.py

# Producer + consumer contract holds
python scripts/check_boundaries.py
python -m pytest tests/test_bar_export_loader.py tests/test_parse_bar_export_cli.py -q
# Expected: boundaries OK; producer tests pass

# Supersede chain integrity (bidirectional)
grep -n "Superseded\|superseded by 2026-06-17\|RESOLVED-BY-RETIREMENT" \
  docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md \
  docs/adr/2026-06-12-rnd-feed-instrument-class-split.md \
  docs/ltm/briefs/Q-FEED-1-dukascopy-tv-feed-divergence.md
# Expected: each carries its disposition note pointing at this ADR

# §4 trigger reminder — next programme audit / regime check: 2026-08-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-06-17-dukascopy-retirement.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (§0 anchors)
git log -1 --format='%h' -- lab/validation/sweep/feed_loader.py   # 0020665
git log -1 --format='%h' -- core/bar_export_loader.py             # 5cba8af
git log -1 --format='%h' -- docs/adr/2026-06-12-rnd-feed-instrument-class-split.md  # 034452d

# Supersede chain integrity
grep -A1 "Supersedes" docs/adr/2026-06-17-dukascopy-retirement.md
grep -n "Status:" docs/adr/2026-06-12-rnd-feed-instrument-class-split.md   # Withdrawn/Superseded
```

---

## Addendum 2026-09-01 -- feed_loader.py consumer citation stale (diagnostic only)

§0 and §2 of this ADR name `lab/validation/sweep/feed_loader.py` (`load_bar_feed`) as "the
feed-agnostic consumer that STAYS" and state the retirement is "consumed unchanged by" it. That
module was deleted 2026-07-11 by `docs/adr/2026-07-11-gen1-pipeline-retirement.md` (§2 decision
table: `lab/validation/sweep/**` -> RETIRE, replaced by Gen-2 vectorbt/Nautilus under the K-ledger)
-- an unrelated decision about the sweep-engine's own retirement, not a reversal of this ADR. That
ADR lists this ADR only under "Related" (pattern precedent), not as a Supersedes target, so no graph
edge records the effect. `core/bar_export_loader.py`'s own module docstring (line 4, live production
code) still names the now-deleted path as the consumer of its output schema.

This ADR's core decision -- Dukascopy retired, `core/bar_export_loader.py` is the canonical bar
producer -- is unaffected and remains accurate; re-verified 2026-09-01: `core/lib/dukascopy.py` stays
deleted, `core/bar_export_loader.py` is live and imported by current code. Only the specific named
downstream consumer is stale. Current live consumers of `core/data/bar_data/*.csv` instead call
`bar_export_loader.parse_bar_export` directly (e.g. `lab/research_utils/beta_cohesion.py`) -- no
single successor module plays `feed_loader.py`'s former "feed-agnostic consumer" role.

Separately: the §10 audit hooks' banner-file expectations (5 named paths under `lab/analysis/...`) no
longer reproduce verbatim -- the underlying investigations were closed and their harnesses relocated
to `lab/archive/...` or reduced to RESULTS-only per this repo's standing lab-retention doctrine
(CLAUDE.md §Lab layout). Expected entropy, not a defect in this ADR's decision.

**Operator call (not resolved here):** whether to (a) add a reciprocal `Supersedes:
`2026-07-11-gen1-pipeline-retirement.md` in part` / `Superseded-in-part-by` header-field pair scoped
to just the consumer-citation clause, or (b) leave this as a diagnostic-only addendum and instead fix
the dangling reference at its source (`core/bar_export_loader.py`'s docstring, a live production file
-- not this ADR's frozen §2 prose, which Rule 14/Trap 12 protect from rewrite).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-17 | Initial authoring + acceptance (operator executive decision) | Joshua + Claude Code |
| 2026-09-01 | Addendum: feed_loader.py consumer citation stale (diagnostic only); operator call on formal edge vs. source-file fix | Claude Code (ADR-corpus reconciliation sweep) |
