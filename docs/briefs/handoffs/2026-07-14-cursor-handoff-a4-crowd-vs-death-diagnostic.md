# Cursor Handoff — A4 month-end footprint diagnostic (DROP-or-DEFER filter for the HARV successor)

**Date:** 2026-07-14 (v2 — adversarially revised; see "Revision note" below)
**Parent session:** claude.ai advisor (Joshua + Claude) — repo-priorities session.
**Spawn target:** Cursor (research venv `.venv-research`; pandas/numpy/scipy; **no** Databento client in new code).
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step; TDD build-with-synthetic, real-run gated on the operator's pull)
**Parent question:** the **A4 fork** — is the Q-HARV-0 month-end-harvest era decay **mechanism-death** (no on-futures harvest survives) or **not-clearly-dead**? Pre-registered in [`docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md`](../2026-07-14-a4-flow-data-fork-scoping.md) §4. **This diagnostic is a conservative DROP-or-DEFER filter, not a go/no-go: it can kill a dead candidate (save the K) but NEVER bless one.**
**Authority:** Joshua (CEO). claude.ai authored; Cursor executes. **No commit/merge without Joshua's go.** **NO `db_fetch` pull / estimate, NO Databento client construction anywhere in new code** — the pull is operator-side (skill Rule 1: mandatory cost estimate first). Build + test on synthetic fixtures; the real run is gated on `parents_ohlcv_1d.parquet` existing AND an explicit operator flag.

**Workspace pin (CORRECTED v3):** PR #368 has **merged to `main`** (commit `fcf8f32`, 2026-07-14 12:28 ET). The pre-registration memo and this handoff are both already on `origin/main`, byte-identical since the merge. **The old feature branch `claude/repo-priorities-474be0` is deleted from origin — do not reference it.** Branch off **`origin/main`**: `git fetch origin && git checkout -b cursor/a4-footprint-diagnostic origin/main`. Build in a **new** dir `lab/analysis/harvest/harv_a4_footprint_2026-07/` — **do not mutate the archived study** `lab/archive/harv_0_month_end_rebalance_es_2026-07/` (import/copy its frozen panel functions; leave its bytes untouched).

> **Binding context (read first).**
> - Flow data can't adjudicate this fork (A4 memo §2). The **price footprint** on data already pullable can — but **only on the death side.** A clear, cross-channel month-end volume-footprint collapse is decent evidence that no futures-harvestable expression survives; acting on it (DROP, save K) is conservative even if the cause is ambiguous (true death vs off-futures crowding).
> - **The crowd/GO side does NOT identify** (this is why v2 removed it). Under death, thin-cell noise fabricates apparent "earlier-entry migration"; under true crowd, off-futures front-running can also shrink the on-futures footprint; and the earliest observable entry (T-4) is the R_spread **selection endpoint**, so its return inherits the ~30–39bp conditioning-window mechanical drift the Q-HARV-0 closure identified as the placebo trap. All three push toward a spurious GO — the one expensive, build-authorizing outcome. So **this diagnostic never authorizes a build.**
> - **DEFER's destination is CORRECTED in v3 — read before dispatch.** v2 said "not clearly dead" DEFERS to "the successor's own 2018+ pre-registered earlier-entry/alt-instrument price test, which is the real adjudicator (memo §3)." **That successor was authored same-day as HARV-2026-002 / [`Q-HARV-1`](../ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md) and DECLINED at its own mandatory §R gate-reachability simulation** (commit `9bddd33`, 2026-07-14) — its confirm bundle had P(RESOLVED | mechanism true) ≈ 5–6% at the available 2018+ N, and its own closure states no reshape rescues it at that N ("the only path to real power is a different information axis... not a re-run of the same 2018+ price panel"). **There is currently no live test for DEFER to route to.** DEFER in v3 means: *the HARV month-end family is not excluded from the [`Q-KBUDGET-1`](../pre-registration/Q-KBUDGET-1-screen-preregistration.md) candidate-axis inventory as mechanism-dead — but any future HARV-family attempt requires a genuinely new design on a different information axis (per Q-HARV-1's own closing finding, not a re-run of the declined 2018+ price test), and that new design needs its own fresh §R reachability sim + Q-KBUDGET-1 screen before any K is spent.* DROP retains its original force: cross-channel footprint collapse excludes the HARV family from the Q-KBUDGET-1 inventory entirely — no further HARV-family axis authoring.
> - **LOW-POWER PRIOR, no K** (a diagnostic re-read of a closed result — no `register_search`, no DSR). Ambiguous/DEFER is the likely modal outcome and is honest; report the MDE so a null isn't over-read.
> - **Reachability discipline (HARV lane HARD gate, PR #367) binds the design:** both surviving outputs (DROP / DEFER) must be able to fire from the real 163-event panel, not just from crafted fixtures.
>
> **Revision note (v2):** v1's H-crowd→GO branch and its T-4-migration trigger were removed after adversarial verification found they could manufacture a false GO via the selection-endpoint drift (the Q-HARV-0 trap) and single-day noise. The timing scan is retained **informational-only** (it cannot drive a call). The footprint leg gains a pre-committed primary read + co-movement rule (removing garden-of-forking-paths), an un-truncated qualifying-count channel, and roll-baseline hardening.
>
> **Revision note (v3, 2026-07-14, pre-dispatch):** workspace pin corrected — PR #368 merged to `main` (`fcf8f32`); the old feature branch is deleted, branch off `origin/main` directly. DEFER's destination corrected per the binding-context bullet above (Q-HARV-1 declined same-day at §R, after this handoff's v2 was finalized). No change to the DROP branch, the footprint/co-movement mechanics, or the offline test suite — v3 is a dispatch-readiness correction, not a redesign. Verified by an independent adversarial dispatch-readiness check before this revision.

---

## §0 — Rule 0 reads (PHASE 0 — before any code)

Cursor: read each and post a read-report first. If repo state contradicts a §2 assumption, `NEEDS_CONTEXT`.

- [`docs/briefs/2026-07-14-a4-flow-data-fork-scoping.md`](../2026-07-14-a4-flow-data-fork-scoping.md) — report **§4 (disposition map)** + §8 verbatim. Note v2 of THIS handoff **narrows** the frozen map to its DROP + (non-GO) DEFER outputs by design — assert against that narrowing, stated in §4 below.
- `lab/archive/harv_0_month_end_rebalance_es_2026-07/build_panel.py` — report: `load_symbol_frame` (**returns OHLC only — DROPS `volume`**; §2.1 needs a volume-preserving variant), the settle-date/weekend-drop logic, `signal_from_r_spread` (**qualifying is truncation-floored at |R_spread|≥100bp** — L107-113), `build_monthly_panel` columns (`T_1..T_4`, `R_spread`, `R_spread_bp`, `window`, `signal`, `qualifying`, `quarter_end`, `micro_era`), and **L149-151 (R_spread conditioning window ends at `close[T-4]`)** — this is why T-4 is the selection endpoint. Frozen functions: import/copy, never edit.
- `lab/archive/harv_0_month_end_rebalance_es_2026-07/run_harv0.py` — report `perm_test_signed` + `effect_on` (the signed-effect + label-permutation + bootstrap pattern the informational timing leg reuses).
- `lab/archive/harv_0_month_end_rebalance_es_2026-07/chunked_pull.py` — report the symbols/schema/range (`ES.c.0 YM.c.0 ZN.c.0 GC.c.0` + `MES/MYM`, `ohlcv-1d` continuous, 2010-06-06→2026-07-01). **Confirm `ohlcv-1d` carries `volume`** (it does) — the footprint premise depends on it.
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — report §2 (the HARD reachability rule) — its spirit binds the DROP/DEFER reachability requirement.
- `git log -1 --format='%h %ci' -- lab/archive/harv_0_month_end_rebalance_es_2026-07/build_panel.py` — anchor.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY; parent defaults stated)

Cursor: this is your explicit license to **halt and ask**. Do **not** guess if any item is ambiguous or any default looks wrong after Phase 0 — the cost of asking is one round-trip; the cost of guessing is a wasted build + a wasted operator pull. Post ambiguities under `## §0.5 Response — ambiguities` and set **`Status: NEEDS_CONTEXT`** until Joshua resolves them.

- **(A) PRIMARY footprint read — pre-committed (removes garden-of-forking-paths).** The DROP decision reads exactly **two co-committed primary channels, era-split**: (1) **ES month-end volume-bump, ex-quarter-end** = `mean(daily vol over {T-3,T-2,T-1}) / mean(daily vol over the trailing 21 trading days ending T-4)`, median per era; (2) **qualifying-event COUNT per era** = `#(|R_spread|≥100bp months) / #(months in era)` — an **un-truncated** flow-intensity proxy (the |R_spread| *magnitude* is truncation-floored by the qualifying rule, so it is NOT primary). Confirm these two as primary.
- **(B) Era boundary.** **2010–2017 vs 2018–2026**, keyed on `T_1.year` (matches Q-HARV-0's decay split). Confirm.
- **(C) Timing leg — INFORMATIONAL ONLY (cannot drive a call).** Report, for context, the incremental single-day signed means **T-4→T-3 and T-3→T-2** (not the nested cumulative returns) with bootstrap 95% CIs, per era. **T-4 is the R_spread selection endpoint — its raw edge inherits the conditioning-window mechanical drift (~30–39bp/2-day, Q-HARV-0 closure); it is reported with that caveat and NEVER read as crowding.** Max detectable migration is one day (T-3→T-4); earlier front-running is pre-signal/unobservable. Confirm the timing leg is informational and drives no disposition.
- **(D) Secondary corroboration (informational).** ZN volume-bump, all-months (incl. QE) reads, and |R_spread| median among ALL months — each with its confound caveat (|R_spread| is vol-regime confounded + truncation-floored). These corroborate but never override the two primary channels.
- **(E) Roll hardening on BOTH windows.** Ex-quarter-end filters the EVENT window; **also exclude any month whose trailing-21-day baseline window overlaps a contract roll** (the `.c.0` roll migrates volume and can inflate/deflate the baseline even for an ex-QE event month). Confirm the baseline-window roll exclusion (default: drop months whose T-4 minus 21 bdays reaches into a roll week; report the count dropped).
- **(F) Disposition = co-movement rule, not effect-size threshold (keeps DROP reachable, removes cherry-picking).** **DROP** iff BOTH primary channels (A1 ES ex-QE bump AND A2 qualifying-count) shrink era-over-era with **non-overlapping bootstrap CIs**; **DEFER** otherwise. No numeric effect-size gate (preserves reachability); the co-movement of two pre-committed channels is the rule. Confirm.
- **(G) MDE / power.** On the synthetic harness, compute + report the bootstrap-CI half-width (minimum detectable era-difference) at realistic N (~50–58/era footprint ex-QE; ~76–87 timing) so the likely DEFER is read as designed-in low power, not evidence. Confirm you'll report it.

---

## §1 — Context

The A4 fork gates whether the HARV successor is worth building. This diagnostic is the **conservative first filter**: a clear cross-channel footprint collapse kills the candidate cheaply (DROP); anything else defers to the successor's own 2018+ pre-registered test. It cannot bless a build.

**What Cursor produces** (in `lab/analysis/harvest/harv_a4_footprint_2026-07/`):
- `a4_footprint.py` — volume-preserving loader + the two PRIMARY footprint channels (A) with the co-movement DROP rule (F) + roll-hardened baseline (E) + secondary corroboration (D) + the informational timing leg (C) + disposition assembly (DROP / DEFER only) + MDE reporting (G).
- `test_a4_footprint.py` — synthetic-fixture tests (fixtures via `bdate_range`, no cache/network): footprint-ratio + qualifying-count math; the co-movement rule; **both surviving branches (DROP, DEFER) reachable from crafted fixtures**; a **roll-spike-in-baseline fixture proving the metric isn't fooled**; the timing leg reports but never gates; volume survives the loader; weekend bars dropped.
- On the real run (operator-gated): `RESULTS.md` with the era table, the DROP/DEFER disposition, the MDE, and a **data-reachability paragraph** (for DROP and DEFER, the concrete real-panel observable that fires it + confirmation it isn't truncated/constant by construction).

**What Cursor is NOT asked to do:** fire any Databento pull/estimate or construct a Databento client; author a GO / bless a successor (DROP-or-DEFER only); read the timing leg as crowding evidence; mutate the archived study or any frozen panel function; add `register_search`/K; touch `core/` / allocation / `dd_protection` / `ACTIVE_FIRM` / Pine; the "while I was in there" refactor.

---

## §2 — Execution plan (TDD throughout; tests offline on synthetic fixtures)

### Step 2.1 — Volume-preserving loader
- **Action:** loader variant reusing `build_panel`'s settle-date + weekend-drop logic but **keeping `volume`**. Fixture-injectable.
- **Gate:** synthetic test asserts volume survives + weekend bars dropped; zero Databento references.

### Step 2.2 — Footprint channels (the DROP evidence)
- **Action:** per qualifying month compute the (A1) ES ex-QE volume-bump; compute the (A2) per-era qualifying-event COUNT; apply the (E) roll-baseline exclusion; compute secondary (D) reads with caveats. Era-split (B). Emit per-channel median + bootstrap CI.
- **Gate:** fixtures — a shrinking-late-era ES bump AND a falling qualifying-count → both primary channels detect attenuation; a roll-spike injected into the baseline does NOT flip the bump verdict.

### Step 2.3 — Timing leg (INFORMATIONAL ONLY)
- **Action:** incremental single-day signed means T-4→T-3, T-3→T-2 (same ex-QE primary set as 2.2) with bootstrap CIs + permutation-p, per era. Attach the T-4 selection-endpoint caveat and the one-day-sensitivity caveat. **This leg drives no disposition.**
- **Gate:** a test asserts the timing output never feeds the DROP/DEFER decision; the T-4 caveat string is emitted.

### Step 2.4 — Disposition (DROP or DEFER)
- **Action:** **DROP** iff both primary channels co-move to attenuation with non-overlapping CIs (F); else **DEFER** to the successor's own 2018+ earlier-entry/alt-instrument test. Attach the MDE (G) + the data-reachability paragraph. No GO output exists.
- **Gate:** DROP fixture → DROP; flat / single-channel / conflicting fixture → DEFER; assert no code path emits GO.

### Step 2.5 — Synthetic-fixture tests
- **Action:** full offline suite incl. the two-branch reachability fixtures, the roll-spike-baseline fixture, the co-movement rule, the timing-never-gates test, era split, loader volume. `check_boundaries` green; no `ops` import; no Databento client.
- **Gate:** all green offline in `.venv-research`.

### Step 2.6 — Real-data run (OPERATOR-GATED)
- **Action:** gated like `bind_real_k` — refuses unless `parents_ohlcv_1d.parquet` exists AND an operator flag is passed. **Pre-run assertion:** confirm the raw parquet schema carries `volume` (via `build_panel.inspect_parquet`) → clean refusal if absent (not a mid-run crash). With the gate open: run → `RESULTS.md` (era table, DROP/DEFER, MDE, data-reachability paragraph). Cursor builds this path + its refusal/schema tests; the operator runs it after the pull.
- **Gate:** refusal tests pass (no parquet / no flag / no volume column ⇒ refuse); the real run is NOT executed in Cursor's session.

### Step 2.7 — Closure report
Post the §6-format report. Do **not** author a successor decision — the DROP/DEFER disposition feeds the operator; DEFER routes to the successor's own test, not to a build authorized here.

---

## §4 — Assertion target (the narrowed disposition — DROP or DEFER only)

`N/A` — no confirmatory hypothesis; a diagnostic prior. The driver asserts against this **narrowed** map (v2), which is the frozen A4 memo §4 map with the non-identifying GO branch collapsed into DEFER:
- **DROP** ⇒ both primary channels co-move to clear attenuation (F) ⇒ "on-futures month-end footprint gone (death **or** off-futures crowding — either way no futures-harvestable expression) ⇒ **DROP** the successor, save the K."
- **DEFER** ⇒ anything else (flat, single-channel, conflicting, or ambiguous) ⇒ "not clearly dead ⇒ the HARV family stays in the [`Q-KBUDGET-1`](../pre-registration/Q-KBUDGET-1-screen-preregistration.md) candidate-axis inventory (not excluded as mechanism-dead); a future attempt needs a genuinely new design on a different information axis, with its own fresh §R sim and K-budget screen (see the binding-context DEFER-destination correction, v3) — **not** a re-run of the declined 2018+ price test (Q-HARV-1)."
- **No GO.** This diagnostic never authorizes a build. The informational timing leg is reported but drives nothing. A restated map that re-introduces a GO branch, or reads a raw T-4 edge as crowding, is a defect (repeats the Q-HARV-0 selection-endpoint trap).

## §5 — Forbidden moves (each genuinely tempting)

- **Firing the pull "since it's ~$0."** Operator-side (skill Rule 1). Build the gate; never open it. No Databento client in new code (grep-audited, §10).
- **Re-introducing a GO / letting the diagnostic bless a build.** It is DROP-or-DEFER only. "Not clearly dead" is DEFER, not GO.
- **Reading a raw T-4 edge as crowding.** T-4 is the R_spread selection endpoint; its return inherits the conditioning-window mechanical drift (Q-HARV-0 placebo trap). The timing leg is informational; it never gates.
- **Cherry-picking among the footprint reads.** The two pre-committed primary channels + the co-movement rule (F) decide DROP; ZN/all-months/|R_spread| are corroboration only. Do not let a secondary read flip the call.
- **Scanning pre-T-4 entries** (look-ahead — signal known only at T-4 close).
- **Treating this prior as confirmatory** / suppressing the MDE or the confound caveats.
- **Mutating the archived study** or any frozen panel function — import/copy, never edit `lab/archive/...`.
- **Re-tuning the frozen §4 map or Q-HARV-0 §4** after seeing real results (Known Trap #12 → `BLOCKED — plan-itself-wrong`).
- **The "while I was in there" refactor** of `build_panel`/`run_harv0` — log under `DONE_WITH_CONCERNS`.

## §6 — Gate + status return taxonomy

Report EXACTLY one of `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`. `DONE` = the driver + tests are built and fixture-proven with both DROP and DEFER branches reachable — it is **not** a crowd-vs-death verdict (that comes from the operator-run real pass, and even then is only DROP-or-DEFER). `DONE_WITH_CONCERNS` = built but Cursor flags a doubt. `NEEDS_CONTEXT` = a §0.5 ambiguity or missing input blocks progress. **`BLOCKED` requires a sub-case:** `BLOCKED — context-problem`, `BLOCKED — capability-problem`, `BLOCKED — scope-problem`, or `BLOCKED — plan-itself-wrong` (e.g. a §0.5 default proves unbuildable, or a branch is unreachable).
```
Status: <...>
Per-step gates: 2.1 [..] 2.2 [..] 2.3 [informational] 2.4 [..] 2.5 [..] 2.6 [refusal-only]
§0.5 resolutions applied: A=<primary pair> B=<..> C=<timing informational> D=<..> E=<roll-both-windows> F=<co-movement> G=<MDE>
Diffs (files touched): <only lab/analysis/harvest/harv_a4_footprint_2026-07/*>
Concerns surfaced: <list>
Next action recommended: operator runs the pull (skill Rule 1) then 2.6 real pass
```

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — spec-compliance:** diffs only under the new analysis dir; archived study byte-untouched; no Databento client; no `register_search`/K; **no GO output anywhere**; real-run path present + gated (incl. volume-schema refusal).
**Pass 2 — quality:** the two primary channels + co-movement rule decide DROP (no cherry-picking); timing leg is informational + carries the T-4 selection-endpoint caveat; roll-spike-baseline fixture passes; both DROP and DEFER reachable; MDE + data-reachability paragraph present; no pre-T-4 entry computed.
**Pass 3 — consolidated read (multi-step):** loader→footprint→(informational timing)→disposition chain consistent; the narrowed §4 map asserted, not re-widened to a GO.

## §10 — Audit hooks (runnable)

```bash
# No data acquisition in new code (expect empty)
grep -rn "Historical(\|get_range\|db_fetch\|databento\|register_search" lab/analysis/harvest/harv_a4_footprint_2026-07/

# No GO output / no build-authorization (expect empty)
grep -rniE "\bGO\b|authorize|bless" lab/analysis/harvest/harv_a4_footprint_2026-07/a4_footprint.py | grep -viE "no.go|never|defer" || echo "no GO output — good"

# Look-ahead: no pre-T-4 entry COMPUTED (scope to indexing, not comment text — a documented 'T-5 excluded' comment is expected)
grep -rnE "t\[5\]|offsets\[5\]|T_5\b" lab/analysis/harvest/harv_a4_footprint_2026-07/a4_footprint.py || echo "no pre-T-4 entry computed — good"

# Archived study + locked core untouched (expect empty)
git diff fcf8f32 -- lab/archive/harv_0_month_end_rebalance_es_2026-07/ core/ CLAUDE.md

# Offline suite + boundaries
PYTHONPATH=lab .venv-research/Scripts/python.exe -m pytest lab/analysis/harvest/harv_a4_footprint_2026-07/ -q
python scripts/check_boundaries.py
```

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-14-cursor-handoff-a4-crowd-vs-death-diagnostic.md --type cc_handoff
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

## Related
- Pre-registration: [`2026-07-14-a4-flow-data-fork-scoping.md`](../2026-07-14-a4-flow-data-fork-scoping.md) (§4 map, §8) · PR #368 (merged to `main` at `fcf8f32`, 2026-07-14).
- DEFER-destination correction (v3): [`Q-HARV-1 / HARV-2026-002`](../../ltm/briefs/Q-HARV-1-month-end-rebalance-successor.md) DECLINED at §R (commit `9bddd33`) · [`Q-KBUDGET-1`](../pre-registration/Q-KBUDGET-1-screen-preregistration.md) (the inventory DEFER now feeds).
- HARV lane reachability discipline: [`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md) (Accepted, HARD gate).
- Data provenance: `lab/archive/harv_0_month_end_rebalance_es_2026-07/chunked_pull.py`.
- **v2 revision basis:** adversarial pre-dispatch verification (2026-07-14, 4 lenses) — collapsed the non-identifying GO branch, pre-committed the footprint primary + co-movement rule, added the un-truncated qualifying-count channel, roll-hardened the baseline, made the timing leg informational with the T-4 selection-endpoint caveat, fixed the branch base to the #368 head, and added MDE + data-reachability reporting.
