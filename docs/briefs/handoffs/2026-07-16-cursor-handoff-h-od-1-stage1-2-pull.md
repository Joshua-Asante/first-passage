# Cursor Handoff — H-OD-1 Stage-1 (register + cost-gated pull) → Stage-2/4 cost-law screen

**Date:** 2026-07-16
**Parent session:** Claude Code (Fable 5) + Joshua
**Spawn target:** Cursor (execution lane — CC/Cursor surface-allocation ADR 2026-07-14: CC specifies, Cursor implements the frozen spec)
**Repo:** `multi_firm_operations`
**Brief type:** CC/Cursor handoff (multi-step)
**Parent pre-reg:** [`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md`](../pre-registration/H-OD-1-ES-overnight-drift-preregistration.md) (**STAGE-0 FROZEN · §8 GO signed 2026-07-16/JA**, committed `9d5b2ec` on `claude/h-od-1-stage0-freeze`)
**Authority:** Joshua (operator). GO signed. Cursor executes the frozen spec; **no threshold, window, construct, or cost-model change** — those are frozen and any deviation voids the campaign.

---

## §0 — Phase-0 reads (execute BEFORE any §2 work; post a read-report first)

Cursor: read each file and report back what it says (contents / relevant lines) before running anything. Do **not** open the search or pull until this read-report is posted and any §0.5 ambiguity is resolved. Verification anchors are `git log -1` (hash + commit-date) at authoring; re-confirm each resolves before you rely on it.

- **`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md`** (`9d5b2ec` 2026-07-16) — the frozen spec. Report: §2 (frozen universe + the **Execution/cost model** row), §3 (Stage-2 cost-law row), §R.1 (the passive-vs-crossing cost table — the load-bearing arithmetic), §4 (H-HOD1), §6 (gate criteria). **Everything you execute comes from this file.**
- **`lab/analysis/orb/d5_nq_intraday_mom_2026-07/run_stage2_4.py`** (`e1c51f0` 2026-07-16) + **`series.py`** + **`baltussen.py`** (same commit) — the D5 driver you will adapt. Report: how it builds the session series, computes the edge, and applies the cost-law. **You are adapting the harness shape, NOT the D5 construct or the D5 cost model** (see §5).
- **`lab/discovery/cost_mnq.py`** (`e1c51f0` 2026-07-16) — D5's cost function. Report: its slip assumption. **Critical:** it models a **full tick per side** (round-trip = 2 ticks; `RT_usd = 2 × (commission + 1×tick)`). H-OD-1's frozen model is **0.5 tick TOTAL round-trip** (§5). You will NOT reuse this as-is.
- **`lab/discovery/register_search.py`** (`67cc146` 2026-07-14) — Report: the `open` arg list (lines ~259–281) and the mechanism-first `--reachability-attestation` HARD gate (lines ~91–114). Invocation confirmed as `PYTHONPATH=lab python -m discovery.register_search` (`lab/discovery/__init__.py` present ⇒ package import).
- **`core/firm_rules.py`** (`a53ee99` 2026-07-13) — Report: `cost_per_side_usd` entries (ES/MES parent-vs-micro commissions) and any ES/MES contract spec (multiplier, tick value). Needed for the cost function.
- **`lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md`** (`e1c51f0` 2026-07-16) — Report: the exact `db_fetch pull` command shape (D5 used it at $0.00). Your pulls mirror it with ES/MES symbols.
- **`.claude/skills/databento-data/SKILL.md`** (or the db_fetch module `--help`) — Report: the mandatory cost dry-run (`estimate`) before every `pull`, and the `--phase` / `--campaign-id` / `--max-cost` flags.

After Phase 0: post the read-report and **stop**. Proceed to §2 only after posting.

---

## §0.5 — HALT-on-ambiguity

Ask (set `Status: NEEDS_CONTEXT`) rather than guess if any of these are unclear after Phase 0:

- **Cost model:** if `firm_rules.py` has no ES-parent commission entry, ASK which to use — do NOT silently fall back to D5's MNQ numbers.
- **ES symbology:** if `ES.FUT` parent (all expiries) 422s or returns an unexpected stype, ASK before switching symbol/stype (PD-1 pattern: dataset-floor / symbology defects are report-then-ask, not silent-fix).
- **Micro launch date:** if `MES.v.0` 422s on `2019-05-05` (pre-first-bar), adjust `--start` to the first available bar and NOTE it — that specific case is a known PD-1-class adjust-and-log, not an ASK.

---

## §1 — Context

D5 (the first fundable discovery axis) closed **FALSIFIED 2026-07-16** at Stage-2 (cost-law KILL: +1.46bp gross vs 11.06bp hurdle). H-OD-1 is the **second** fundable axis (harvest H1; screen PASS 0.837 power) and — load-bearing — the **tie-breaker for the harvest-intake §4 doctrine falsifier**: D5 fired 1 of the 2 FALSIFIED closures the doctrine counts; if H-OD-1 also falsifies on its confirm clause, the external-mechanism intake demotes to research-only; if it confirms, the doctrine RESOLVES. So this campaign's Stage-2 verdict matters beyond the axis itself.

**What Cursor produces:**
- Search register opened + closed for `h_od_1_es_overnight_drift` (manifest under `discovery_manifests/`).
- Cost-gated ES/MES `ohlcv-1m` caches (era-tagged).
- Stage-2/4 cost-law screen under the **frozen passive model** → KILL or PASS.
- `PULL_LOG.md` + `RESULTS.md` under `lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/`.

**What Cursor is NOT asked to do:** run Stage-5+ (blocked unless Stage-2 PASSES *and* the operator re-authorizes the OOS confirm); change any frozen value; deploy anything; touch `core/` / allocations / `dd_protection` / Pine.

---

## §2 — Execution plan (gated; stop at the Stage-2 verdict)

### Step 2.1 — `register_search open` (binds K=1; K_eff=2 with the ES bank)

- **Inputs:** the frozen pre-reg (attestation), `register_search.py`.
- **Action:** first write a params file `lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/params_open.json`:
  ```json
  {
    "k_rule": "K_eff=2 (K_intrinsic=1 H1 sole candidate + K_banked=1 ES family from Q-HARV-0; H3 disjoint-hour placebo consumes no selection-K)",
    "prereg": "docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md",
    "instrument": "ES parent sole confirm anchor; MES = Stage-7 realism leg; MNQ/NQ/MYM FORBIDDEN",
    "construct": "SR917 overnight-drift: long ES 02:00->03:00 ET hour, unconditional, one RT/session",
    "lane": "mechanism-first",
    "clause_k_floor": 0.85,
    "v_rule": "V=1/n unconditional pin",
    "cost_model": "FROZEN passive: 0.5 ES tick TOTAL round-trip + negligible commission, on ES-parent notional (NOT D5 per-side crossing)",
    "oos_axis": "IS ES parent 2010-06-06:2018-12-31; OOS ES parent 2019-01-02:pull-date; MES realism 2019-05-05:pull-date",
    "go_signed": "2026-07-16/JA"
  }
  ```
  Then:
  ```
  PYTHONPATH=lab python -m discovery.register_search open \
    --run-id h_od_1_es_overnight_drift \
    --lane mechanism-first \
    --reachability-attestation docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md \
    --tool sr917-fixed-hour \
    --search-space-size 1 \
    --alpha 0.05 \
    --data-window 2010-06-06:2018-12-31 \
    --hypothesis "ES 02:00-03:00 ET overnight-drift hour has positive mean return (Boyarchenko-Larsen-Whelan FRBNY SR917 dealer inventory-risk); net-of-cost annualized Sharpe>=0.85 at K_eff=2 under the frozen passive execution model; disjoint-hour 20:00-21:00 ET placebo null" \
    --params-file lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/params_open.json
  ```
- **Expected output:** manifest `discovery_manifests/h_od_1_es_overnight_drift.json` (status `open`, K=1). The `--search-space-size 1` binds this campaign's K; K_eff=2 is the ES-family-banked effective count used at the Stage-6 floor (not needed until confirm).
- **Per-step gate:** command exits 0; manifest exists with `lane: mechanism-first` and the attestation path recorded. If the HARD gate rejects (empty/missing attestation), STOP — the freeze commit is required first (it is `9d5b2ec`).

### Step 2.2 — Cost-gated pulls (estimate → gate → pull; every pull `--max-cost 1.00`)

Mirror the D5 PULL_LOG shape. **Run `db_fetch estimate` first for each; only `pull` if under the ceiling.** Log every estimate + actual to `PULL_LOG.md`.

1. **ES parent IS (discovery/tuning):**
   ```
   PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
     --symbols ES.FUT --stype parent --schema ohlcv-1m \
     --start 2010-06-06 --end 2019-01-01 \
     --campaign-id h_od_1_es_overnight_drift --phase discovery --max-cost 1.00
   ```
   (`--end` EXCLUSIVE ⇒ last included 2018-12-31; dataset floor 2010-06-06 per PD-1.)
2. **ES parent OOS (confirm era):**
   ```
   PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
     --symbols ES.FUT --stype parent --schema ohlcv-1m \
     --start 2019-01-02 --end <today+1> \
     --campaign-id h_od_1_es_overnight_drift --phase oos --max-cost 1.00
   ```
3. **MES OOS realism leg (Stage-7 input — micro cost cliff):**
   ```
   PYTHONPATH=lab python -m databento_fetch.db_fetch pull \
     --symbols MES.v.0 --stype continuous --schema ohlcv-1m \
     --start 2019-05-05 --end <today+1> \
     --campaign-id h_od_1_es_overnight_drift --phase oos --max-cost 1.00
   ```
- **Expected output:** three era-tagged caches; `PULL_LOG.md` with estimate/actual/records/vendor-degraded-days for each (carry any BentoWarning reduced-quality days into the Stage-6 defect log, as D5 did).
- **Per-step gate:** all three cached; any estimate exceeding `--max-cost` HALTS the pull and returns `NEEDS_CONTEXT` (the free-credit window should keep these at ~$0.00, but the gate is real).

### Step 2.3 — Stage-2/4 cost-law screen (FROZEN PASSIVE MODEL) + close

- **Inputs:** ES-parent IS cache; the frozen construct + cost model.
- **Construct (frozen — §2 of pre-reg):** on each ES RTH-day (America/New_York, DST-aware), `r_hour = ln(px_open_0300 / px_open_0200)` using the 02:00 and 03:00 ET 1-minute bar opens; **position is unconditional LONG** (overnight drift is directional-positive — this is NOT D5's `sign(rod)×last` timing). Edge series = `r_hour` per session; mean gross edge = mean(`r_hour`). One RT/session. Volume-lead stitch the ES parent expiries at analysis time (DISC-CAMP-0 / D5 pattern).
- **Cost model (frozen — pre-reg §2 Execution row + §R.1; THE load-bearing instruction):**
  - Slippage = **0.5 ES tick for the ENTIRE round trip** = 0.5 × 0.25pt × $50 = **$6.25 per contract RT** (passive-both-sides). Do **NOT** use D5's per-side full-tick crossing (`cost_mnq.py`), which for ES would be 2 × $12.50 = $25 RT and would wrongly kill.
  - Commission = ES-parent `cost_per_side_usd` × 2 (≤ ~$3.00/side ⇒ ≤ 0.03bp — negligible per §2, include it but it barely moves the hurdle).
  - `RT_frac = (6.25 + 2×comm) / notional`, `notional = median_px_0300 × $50`. Hurdle = **4 × RT_frac**.
  - Build a fresh ES cost function (e.g. `lab/discovery/cost_es.py`, ES multiplier $50, tick $12.50) — do not monkey-patch MNQ constants.
  - **Self-check against pre-reg §R.1:** at ES index ~4,400 the passive RT ≈ 0.28–0.29bp, 4× hurdle ≈ 1.16bp; gross ≈ 1.5bp ⇒ a **thin PASS** is the expected shape (unlike D5's 7.6× miss). If your harness produces a >1bp RT cost, you have almost certainly applied the crossing model — STOP and recheck.
- **Action:** `PASS iff mean gross edge ≥ 4 × RT_frac`. Emit `stage2_4_report.json` + `stage4_is_edges.csv` (mirror D5's schema). Then close the register:
  ```
  PYTHONPATH=lab python -m discovery.register_search close \
    --run-id h_od_1_es_overnight_drift --pvalues 1.0
  ```
  (On a Stage-2 KILL the single candidate is a non-survivor ⇒ `--pvalues 1.0`, as D5 closed. On a Stage-2 PASS, do **not** invent a confirm p-value here — Stage-6 owns that; close with the Stage-2 disposition noted and STOP for operator re-authorization, §6.)
- **Per-step gate:** report emitted; verdict is one of KILL / PASS; manifest closed (banks ES family K → 2).

### Step 2.N — Closure artifacts

- `lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/PULL_LOG.md` (pulls) + `RESULTS.md` (Stage-2/4 verdict, mirroring D5's RESULTS.md).
- Update `docs/briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md` status + `STATE.md` forward-board harvest-intake line to record the closure (KILL ⇒ 2-of-2 FIRED ⇒ intake FALSIFIED→research-only; PASS ⇒ campaign advances to OOS confirm, doctrine trends RESOLVED).
- Add a `docs/SESSIONS.md` top entry.

---

## §4 — Falsifiable hypothesis (verbatim from pre-reg §4)

**H-HOD1 — if** the fixed ES 02:00–03:00 ET construct (H1), scored on the ES-parent OOS era under the frozen passive cost model and gates, delivers **net-of-cost annualized Sharpe ≥ 0.85** (DSR ≥ 0.95 at K_eff=2) **AND** clears the temporal-consistency battery **AND** the disjoint-hour placebo stays null, **then** confirmed candidate; **otherwise** closes (all-null close is success-eligible).

**This handoff reaches only the Stage-2 cost-law gate** (the cheap kill). Stage-6 net-Sharpe / placebo / temporal battery are downstream and operator-re-gated. **Stage-2 KILL trigger:** mean gross edge < 4 × frozen-passive RT cost fraction.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Reusing D5's `cost_mnq.py` per-side crossing model on ES.** THE trap. D5 = full tick per side (2-tick RT crossing); H-OD-1 = 0.5 tick TOTAL RT passive (§2.3). Copying D5's cost harness verbatim applies ~4× the true frozen cost and wrongly kills. Build the ES passive cost fresh and self-check vs pre-reg §R.1.
- **Copying D5's `sign(rod)×last` construct.** H-OD-1 is unconditional LONG of the 02:00–03:00 ET hour, not a same-session timing signal. Different mechanism entirely.
- **Any MNQ/NQ/MYM expression, or shifting the 02:00–03:00 / 20:00–21:00 ET clocks, or adding the BtD (RSV<0) conditional.** All frozen/forbidden (BtD dropped per P1(a) to preserve H-TSMOM-1; re-adding it needs a fresh Stage-0).
- **Proceeding past Stage-2 on a KILL, or auto-running Stage-5+ on a PASS.** Stage-2 is a hard gate; a PASS returns to the operator/CC for OOS-confirm authorization, it does not license Cursor to continue.
- **Pulling before `register_search open`, or opening before the freeze commit `9d5b2ec` is present.** Freeze-before-open is git-checkable (pre-reg §10 hook 1).
- **Amending any frozen threshold after seeing a number** (Trap #12). If the plan looks wrong, return `BLOCKED — plan-itself-wrong`.
- **Silent scope creep** into `core/` / allocations / `dd_protection` / Pine. Log off-pattern observations under `DONE_WITH_CONCERNS`; do not fix.

---

## §6 — Status return taxonomy

Return EXACTLY one: `DONE` (Stage-1 + Stage-2/4 ran; verdict emitted; manifest closed; artifacts written) · `DONE_WITH_CONCERNS` (ran but flags something off-pattern — e.g. a cost-model ambiguity you resolved but want reviewed) · `NEEDS_CONTEXT` (missing ES commission / symbology 422 / estimate over ceiling) · `BLOCKED — <sub-case>`.

**`BLOCKED` sub-cases (mandatory):**
- `BLOCKED — context-problem`: a needed input is missing/unreadable → re-dispatch with more context.
- `BLOCKED — capability-problem`: databento auth / research-venv / API limit blocks the pull → escalate to operator.
- `BLOCKED — scope-problem`: the Stage-1→2 span is too large for one pass → decompose (e.g. pull-only, then screen).
- `BLOCKED — plan-itself-wrong`: a frozen value in §2 is internally inconsistent with the pre-reg → escalate to CC; do not proceed on a guess.

**On a Stage-2 PASS specifically:** return `DONE_WITH_CONCERNS` with "Stage-2 PASS — OOS confirm requires operator re-authorization (Stage-5+ blocked per §5)" as the concern, so it routes back rather than reading as a finished green campaign.

Closure report format:
```
Status: <...>
Per-step gates: 2.1 [..], 2.2 [..], 2.3 [..], 2.N [..]
Stage-2 verdict: <KILL | PASS> (mean gross edge <x>bp vs 4× passive hurdle <y>bp)
Diffs (files touched): <list>
Closure artifacts: PULL_LOG.md, RESULTS.md, manifest
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (CC, after Cursor returns)

**Pass 1 — Spec compliance:** manifest lane=mechanism-first + attestation path; three ES/MES caches era-tagged; cost harness is the 0.5-tick passive ES model (grep the cost code for the multiplier/tick and confirm `$50`/`0.5 tick RT`, NOT `cost_mnq`); diff touches only the campaign dir + scoping/STATE/SESSIONS.
**Pass 2 — Quality:** re-run the Stage-2 screen; confirm the RT cost lands ~0.28–0.44bp (passive), not ~0.6–2.3bp (crossing); confirm the verdict logic is `mean edge ≥ 4×RT_frac`; confirm §0 anchors match.
**Pass 3 — Consolidated:** the KILL/PASS verdict, the manifest close (`--pvalues 1.0` iff KILL), and the STATE harvest-intake line (1-of-2 vs 2-of-2 FIRED) tell a consistent story.

---

## §10 — Audit hooks (runnable)

```bash
# Manifest opened+closed, mechanism-first, attestation recorded
python -c "import json; m=json.load(open('discovery_manifests/h_od_1_es_overnight_drift.json')); print(m['status'], m['lane'], m['K'], m['reachability_attestation'])"
# expect: closed mechanism-first 1 docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md

# Cost model is the passive ES model, NOT the D5 crossing model
grep -n "0.5\|12.5\|50" lab/discovery/cost_es.py            # ES multiplier/tick + half-tick RT
grep -L "cost_mnq" lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/run_stage2_4.py  # must NOT import cost_mnq

# Verdict reproduces
PYTHONPATH=lab;core python lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/run_stage2_4.py

# Freeze-before-open held (freeze commit precedes the manifest open timestamp)
git log --oneline -- docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md | tail -1  # 9d5b2ec

# Self-check the passive RT cost is sub-0.5bp (else crossing model leaked in)
python -c "print('passive RT bp at index 4400:', round((6.25)/(4400*50)*1e4,3))"   # ~0.28 bp
```

---

## Verification (parent-side, before dispatch)

```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/handoffs/2026-07-16-cursor-handoff-h-od-1-stage1-2-pull.md --type cc_handoff
# Expected: PASS

# Freeze commit present (the thing this handoff depends on)
git log --oneline -1 --grep="freeze H-OD-1"   # 9d5b2ec
```
