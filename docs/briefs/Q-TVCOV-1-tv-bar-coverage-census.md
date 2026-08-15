# Q-TVCOV-1 — TV intraday bar-coverage census (pre-2022) — CC handoff

**Designation:** PROVISIONAL (operator may renumber; `docs/briefs/INDEX.md` registration owed at commit)
**Type:** CC handoff brief — data-integrity audit (not a discovery campaign; K=0, no candidate is mined)
**Loop of Record:** OUTER (INQHIORI) — evidence-weight question gating how much the 7-year panel extensions can ever carry
**Author:** claude.ai Tech Advisor session 2026-07-13 · Dispatch: operator → Claude Code
**Consumers:** any brief citing pre-2022 segments of the 2026-07-12 TV exports; 08-08 packet (evidence-weight footnote)

---

## §0 — Rule-0 reads (parent session, 2026-07-13)

- [`docs/adr/2026-07-10-databento-research-stack.md`](adr/2026-07-10-databento-research-stack.md) — existence verified via `git ls-files` (content read owed by spawn, Phase 0).
- [`lab/databento_fetch/db_fetch.py`](../../lab/databento_fetch/db_fetch.py) — path verified via `git ls-files` 2026-07-13. Spawn must content-read in Phase 0 (estimate/pull interface + the IS/OOS date-cap semantics added in commit `56a514a`).
- [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](rnd-pipeline/discovery-campaign-template.md) — Stage table + §Campaign-defaults content-read 2026-07-13 (last touch `dffcb5e`). Default #6 (per-campaign cost gate) honored below even though this is not a campaign.
- [`.claude/skills/databento-data/SKILL.md`](../../.claude/skills/databento-data/SKILL.md) — content-read 2026-07-13 (Rules 1–4: estimate-before-pull; coarsest schema; deliberate symbology; roll-rule confirmation).
- Evidence panels (claude.ai reconcile session 2026-07-13, Step-0 clean, exits-only P&L, multipliers verified 0.5/2.0/12.5M):
  - `Striker_DJ30_v4_5_MYM_...2026-07-12_1e459.csv` — sha256 `89a96dcc4f3fb6985f49190567f701d8132cc4f1c89c92ba312dcf44a2bb3ff2`
  - `Striker_NAS100_v1_...2026-07-12_d79cb.csv` — sha256 `5a9816610dc708dbe9b37b4766d4e7bafba7c3661b87eba2d7df1b92871b55ef`
  - `Aegis_JPY-Futures_v0_3_BEPAD-TEST_...2026-07-12_6d379.csv` — sha256 `dd6412d0830af94aa4635914d46a6b81f895acb9431c49aaa73854ab73e95e8b`

---

## §0.5 — Ambiguity halt (spawn: answer BEFORE executing §2)

List ambiguities and HALT for parent input if any of the following are unclear after Phase-0 reads:

1. Does `db_fetch.py` enforce the IS date-cap (`2018-12-31`) on ALL pulls? This audit needs 2019-06 → 2026-07 (OOS/native-micro era). If the cap is unconditional, report `NEEDS_CONTEXT` with the exact blocking code line — do NOT patch or bypass the cap, and do not hand-write a bare `get_range`.
2. Continuous-symbology roll rule for `MYM.c.0` / `MNQ.c.0` / `6J.c.0` per `reference/schemas-and-symbology.md` — confirm the letter/adjustment before pulling. (Bar counts are roll-insensitive; price comparison is out of scope regardless.)
3. Any conflict between this brief and `docs/adr/2026-07-10-databento-research-stack.md` cost falsifier accounting.

---

## §1 — Symptom (names what is wrong, not a fix)

The three 2026-07-12 TV exports show a trade-rate discontinuity at the 2022 boundary that volatility regime does not explain: MYM 24/yr pre-2022 → 50/yr post (2.1×); 6J 11/yr → 29/yr (2.7×); MNQ flat (1.1×). 2020 — the volatility-max year — prints only 20 MYM trades. 6J is a full-size contract (no early-micro-liquidity story available). Until the cause is known, the evidential weight of every pre-2022 panel segment is indeterminate: it could be genuine regime-dependent signal density, or a thinner TV intraday bar feed silently starving signal formation.

---

## §2 — Plan (two stages, cost-gated; one operator leg out of scope for the spawn)

**Stage 1 — coarse canonical census (ohlcv-1h).** `estimate` then `pull` via `lab/databento_fetch/db_fetch.py`, GLBX.MDP3, symbols `MYM.c.0, MNQ.c.0, 6J.c.0`, stype `continuous`, schema `ohlcv-1h`, range `2019-06-01 → 2026-07-01`. Emit per-instrument-month: hour-bar count, zero-volume-bar count, total volume.

**Stage 2 — fine canonical census (ohlcv-1m, 9 pre-registered sample months).** Months (FROZEN here, no post-hoc substitution): `2019-09, 2020-03, 2020-09, 2021-03, 2021-09` (pre-break) and `2022-03, 2023-06, 2024-03, 2025-06` (post-break). Same symbols/venue, schema `ohlcv-1m`. Metric per instrument-month: coverage ratio = fraction of 15-minute grid intervals, weekdays, 08:00–16:30 ET, containing ≥1 one-minute bar with volume > 0. Exclude days with zero bars all day (holidays) from the denominator. Report pre-break vs post-break coverage-ratio deltas per instrument.

**Cost discipline:** summed `estimate` for both stages BEFORE any pull; ceiling `--max-cost $5.00` total; abort and report if exceeded. Cache per `db_fetch` defaults.

**Out of scope for the spawn (operator leg, pre-registered here):** TV-side 15m bar counts for the same 9 months × 3 symbols in the same ET window (chart count or Pine bar-counter export). The spawn's deliverable must print the canonical per-month 15m-interval counts in a table formatted for direct side-by-side entry of the TV counts.

---

## §4 — Falsifier (falsifiable hypothesis)

**H (artifact):** pre-2022 intraday coverage available to the backtests was materially deficient — operationalized as either (a) canonical coverage ratio pre-break trailing post-break by ≥5pp for the same instrument (feed genuinely thin), or (b) canonical coverage complete but the operator TV leg shows TV 15m bar counts ≥5% below canonical on ≥2 pre-break months for an instrument (TV mirror thin).

If H holds → pre-2022 segments of the affected instrument's panels are downgraded to NON-EVIDENTIAL (annotate any brief citing them).

**Falsifier:** canonical coverage complete AND TV counts match (±1%) on all pre-break sample months → H is FALSIFIED (break is real). Limb (a) or (b) met → H RESOLVED-true = ARTIFACT-CONFIRMED. 1–5pp band → AMBIGUOUS, parent decides on a finer schema.

If canonical coverage is complete AND TV counts match (±1%) → the frequency break is real (regime / strategy-structure interaction); pre-2022 extensions retain standing with a regime caveat; the "why" is a separate question that must NOT be opened inside this audit.

---

## §5 — Forbidden moves (genuinely tempting)

- Patching or flag-bypassing the `db_fetch` IS date-cap to make the pull go through (tempting: one-line change). `NEEDS_CONTEXT` instead.
- Substituting sample months after seeing Stage-1 results (tempting: chase anomalous months). The 9 are frozen; anomalous Stage-1 months may be REPORTED but not swapped in.
- Reconstructing strategy signals on canonical data to "explain" the break (scope creep into a strategy port; this audit counts bars only).
- Comparing prices across TV/Databento continuous series (roll-rule/adjustment mismatch noise; counts only).
- Treating a canonical-complete result as closing the question (the decisive comparison for hypothesis limb (b) is the operator TV leg; say so in the report).

---

## §6 — Gate + return

Binary per instrument: `ARTIFACT-CONFIRMED` (H limb a or b met) / `COVERAGE-COMPLETE-PENDING-TV-LEG` (canonical complete; operator counts owed) / `AMBIGUOUS` (deltas in 1–5pp band → parent decides whether a finer schema is justified).

Return taxonomy: `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` (e.g., date-cap, missing API key env var) / `BLOCKED` (sub-case stated: context / capability / scope / plan-wrong).

Deliverables: `lab/analysis/c1/tvcov_2026-07/RESULTS.md` (tables + verdict per instrument), pull manifests/cache keys, and the side-by-side TV-entry table.

---

## §7 — Parent review (two passes)

1. Spec compliance: exactly Stages 1–2 as written; 9 frozen months; no cap bypass; no extra schemas; cost ≤ $5.
2. Quality: denominators handled (holidays/early closes), ET conversion DST-aware, zero-volume vs missing-bar distinguished.

Single-step-family work; no consolidated multi-diff read expected beyond `RESULTS.md`.

---

## §10 — Audit hooks

```bash
grep -n "FROZEN\|2019-09, 2020-03" docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md   # sample months unchanged
ls lab/analysis/c1/tvcov_2026-07/RESULTS.md                                              # deliverable landed
grep -rn "max-cost 5" lab/analysis/c1/tvcov_2026-07/ || echo "cost ceiling not evidenced" # cost gate honored
```

**Verification**

```bash
python scripts/check_brief.py docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md --type cc_handoff
```
