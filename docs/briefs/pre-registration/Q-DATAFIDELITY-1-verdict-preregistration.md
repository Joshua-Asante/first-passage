# Q-DATAFIDELITY-1 — Verdict pre-registration (H-DATAFIDELITY-1)

**Frozen:** 2026-08-23, before any independent-reference price value or Limb C3 grep result was read. Parent brief: [`Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md`](../Q-DATAFIDELITY-1-tv-price-fidelity-and-integrity-gate-scope.md) (frozen at commit `3336d05`, authored 2026-08-18). **Execution requires a separate operator GO** — recorded 2026-08-23 in chat.

---

## §A — Limb C2: pinned inputs (frozen; no substitutions)

| Input | Value | Source |
|---|---|---|
| Instrument | **MGC** (COMEX Micro Gold), TV continuous symbol `MGC1!` | `core/data/tv_exports/cme/BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv` (on-disk, `SHA256SUMS`-pinned) |
| Sampled trading days | **9 CME trade dates**, mechanically selected as *the last 9 distinct trade dates present in the on-disk file* (see bucketing rule below) — no value-based cherry-picking: `2026-07-21, 07-22, 07-23, 07-24, 07-27, 07-28, 07-29, 07-30, 07-31` | Derived from the file's own decoded bar timestamps |
| Selection rule (frozen before any comparison) | Extract all `Entry` rows' `Signal` field (BAR EXPORT v0.2), decode `epoch_ms` (bar-open, UTC, authoritative per `core/bar_export_loader.py:8-12`), convert to `America/New_York`, assign `trade_date = (ts_ET + 6h).date()` (standard CME/Globex session convention: session opens D-1 18:00 ET, closes D 17:00 ET). Take the last 9 distinct `trade_date` values. | This session, `c2_diff.py` (scratchpad) |
| TV-side daily OHLC | `open` = first bar's `o` in the `trade_date` bucket (by time); `high` = max `h`; `low` = min `l`; `close` = last bar's `c` | Same script |
| Independent reference | **Databento GLBX.MDP3**, symbol `MGC.v.0` (continuous, **volume-based roll** — matches TV's `1!` front-month selection per this repo's own `lesson_roll_rule_changes_bar_existence` memory; NOT `.c.0`), schema `ohlcv-1h` aggregated to the identical trade-date bucket via the identical `+6h` rule. Native `ohlcv-1d` is explicitly **not** used as the reference because it is UTC-midnight bucketed, not trade-date bucketed (`lesson_databento_ohlcv1d_weekend_bars` — confirmed live this session: the native `ohlcv-1d` pull produced a low-volume phantom "2026-07-26 Sunday" bar). | `lab/databento_fetch/db_fetch.py`; window `2026-07-18` – `2026-08-01` |
| Tolerance ("1 tick") | **0.1 index points** — read from the TV file's own BAR EXPORT v0.2 metadata suffix (`mintick=0.1`), corroborated by CME Micro Gold's public contract spec ($0.10/tick, $10/point) | `core/bar_export_loader.py:46-51` (`SIGNAL_PIPE_V2_RE` field order) |
| Stop/TP-relevant fields | High and Low primarily (bar extremes determine stop/TP-hit); Open and Close also compared and reported | Section 4 wording |
| Budget | $0.00 (Databento `estimate` run before every `pull`; both calls billed $0.0000 per the tool's own metadata endpoint) | `db_fetch.py estimate/pull` output |

**Escalation note (recorded here, before any value was compared):** Phase 1a as literally written in the brief names "a trivial free-tier Databento daily-bar pull." The native `ohlcv-1d` schema was pulled first and inspected for *shape* only (row count, phantom-Sunday pattern, contract-id roll) before any OHLC value was compared against TV — this is a data-shape check, not the falsifiable comparison. That shape check surfaced the known UTC-bucketing gotcha this project has already documented (`lesson_databento_ohlcv1d_weekend_bars`), so the reference was escalated to `ohlcv-1h` (still the coarsest schema that answers the question, per the `databento-data` skill's own Rule 2) and re-bucketed by trade date instead of UTC day. This escalation is a methodology correction, not a re-roll of a close/borderline numeric result (§5 forbidden move #4 concerns the latter) — no OHLC value was read before this decision was made, and the incremental cost was $0.

## §B — Limb C3: frozen grep patterns (verbatim from the brief's own §7/§10)

1. `rg -i "byte.stab|drift.only|capture.time|wrongly.sourced|hashed.correctly|source.correctness" docs/ scripts/check_data_manifests.py`
   — expect 0 hits describing the manifest gate's byte-stability-only blind spot outside this brief's own text and its 2026-08-18 source audit note.
2. `rg -i "feed.equivalence|feed_equivalence"` (repo-wide)
   — expect only `docs/spec/feed_equivalence_discovery_test_LOCKED.md` (the broken Pepperstone-only spec) plus citing surfaces; no second CME-futures-scoped spec.
3. `rg -n "DOC-1" STATE.md docs/SESSIONS.md docs/adr/INDEX.md`
   — expect no resolution logged since `docs/notes/audits/2026-08-14-requirements-backlog-ratification.md`.

No pattern may be edited, added, or dropped after seeing a grep result.

## §C — Decision rule (mirrored verbatim from the parent brief's §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb C2: all sampled days within 1-tick tolerance on the diffed instrument's stop/TP-relevant OHLC values. Limb C3: repo grep finds an existing documented byte-stability-only caveat on the manifest gate, AND a CME-era feed-equivalence replacement is found to already exist. | `INTEGRATE — record TV CME-futures price fidelity and safety-net scope as evidence-checked for the sampled instrument/dates; no code or doc change owed.` |
| `FALSIFIED` | Limb C2: ≥1 sampled day exceeds 1-tick tolerance on a stop/TP-relevant value. OR Limb C3: grep confirms 0 hits documenting the manifest gate's blind spot AND 0 hits for a CME-era feed-equivalence successor. | `STOP — the specific safety-net gap(s) confirmed real are named findings for the operator queue (candidate items: a CME-era feed-equivalence replacement; a documented manifest-gate scope caveat; a price-fidelity census extended to MGC/MCL/M2K). Re-proposal bar: new mechanism evidence (a real fix landed and re-verified), not a re-run of the same diff.` |
| `AMBIGUOUS-HOLD` | Limb C2 inconclusive (reference source unavailable/insufficient granularity for the sampled dates) and Limb C3 partially decisive (one sub-claim confirmed, the other not). | `ITERATE — name (do not open) a successor: re-run Limb C2 against a different free reference source or a different sampled instrument; re-test window: next time a 4th CME micro is onboarded via BAR_EXPORT.` |

**Combined H rule (from §4):** If Limb C2 holds (divergence found) OR Limb C3 holds (both scope gaps confirmed undocumented/unfilled), H-DATAFIDELITY-1 is CONFIRMED → brief verdict FALSIFIED. If neither limb holds, H is REJECTED → RESOLVED.

Neither branch may be amended after either limb's result is read (Known Trap #12).

## §D — Pinned ex-ante expectation (surprise marker)

**Predicted: `FALSIFIED` via Limb C3 alone, Limb C2 outcome genuinely uncertain.** Reasoning recorded before either limb ran: Section 0's own Rule-0 reads already established (a) `docs/spec/feed_equivalence_discovery_test_LOCKED.md` is the only feed-equivalence spec in the corpus and is Pepperstone-only, and (b) the manifest gate's own admitting ADR states the byte-stability/source-correctness distinction only inside a Trade-offs table, not as a surfaced caveat — so Limb C3 is expected to fire FALSIFIED on structural grounds alone, independent of what Limb C2 finds. Limb C2 is the genuinely open empirical question: MGC's TV export could plausibly match an independent reference exactly (TV/Databento both ultimately source CME Globex prints), or diverge due to feed-specific capture defects, or — a possibility not named in the brief's own forbidden-moves list — diverge due to continuous-series roll-timing noise on exactly the instrument/window sampled (Q-TVCOV-1's own forbidden move #4 names this class of noise for *counts*; the parent brief does not exclude it for *price comparison*, which is a gap in the frozen brief, not a discretionary read).

## §E — Forbidden moves (inherited from the parent §5, restated for the frozen record)

1. Treating Q-TVCOV-1's FALSIFIED bar-coverage closure as settling price fidelity.
2. Treating "the manifest gate passed" as fidelity evidence.
3. Fixing DOC-1 (deleting/repairing the feed-equivalence spec) as a side effect of this brief.
4. Running a new backtest or paid data pull to "really" nail down a close-but-not-exact Limb C2 result — a borderline result routes to Ambiguous-hold, not further spend.
5. Amending §C's gate table, §A's frozen sample, or §B's grep patterns after seeing any result.

---

**Freeze note:** this pre-registration is authored and committed in spirit before Phase 1's diff or grep results are used to form any verdict. No Limb C2 OHLC divergence value and no Limb C3 grep-hit count had been read at the time §A/§B/§C above were fixed (the §A "escalation note" documents the one shape-only exception and why it does not compromise the freeze).
