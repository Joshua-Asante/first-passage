# Pre-registration — Aegis→6J prop reconstruction **v2.2** (native-path 1R guard re-spec; unblocks Stage-2)

**Status:** `FROZEN` (operator §9 signed 2026-07-16 / JA — directed in-session: "author v2.2 for
option c, then re-run"). Authorizes the Stage-2 re-run. No in-place amendment (Trap #12).
**Role:** the **fresh pre-reg required** to re-specify the frozen §2.7 **1R guard** for the
**native-no-rescale** Stage-2 path, after it hard-failed on the c05 winner panel (NEEDS_CONTEXT,
5274c class). Does **not** amend v2 / v2.1 (both `FROZEN`) — this is the close-and-reopen route.
**Parents (unchanged):** v2 window-realigned pre-reg + v2.1 tie-break pre-reg (both `FROZEN`
§9 2026-07-16 / JA); winner **c05** (cap8 / 0.40% / 16:00 / panel `ED91CD2D`). **Inherits the
entire Stage-2 §2.7 protocol byte-identical** except the single 1R-guard clause below.
**Gate of record (unchanged, cited not re-decided):** [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md).
**Loop of record:** STRATEGIC.
**Authored:** 2026-07-16 · Claude Code (operator-directed).

---

## §0 — Rule-0 reads (verified this session 2026-07-16, byte-exact)

- **`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md`**
  (v2, `FROZEN`) §2.7 — *"1R guard: `pin_r_basis(full_stop_mean)` — hard-fail on FALLBACK or n<5
  full-stops (5274c class)."* This is the clause re-specified here.
- **`lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md`** (Stage-2 run, `1ababcf`) —
  **NEEDS_CONTEXT**: c05 native $100K panel has **0 full-stops** above 1%-of-$100K ($1,000);
  **max static loss $631.56** (82 losers, median ~$90); `pin_r_basis(full_stop_mean)` → FALLBACK.
- **`lab/archive/class_s_aegis_solo_scoring_2026-07-16/run_aegis_solo_scoring.py`** — native
  panel: decompound c05 → static $100K → daily book → `score_candidate` **directly**. 1R is
  **not** a scoring input (contrast the candidate #1/#2 CFD-decompound-and-**rescale** path).
- **`.claude/skills/trade-csv-reconcile/scripts/reconcile.py`** `pin_r_basis` — `full_stop_mean`
  = mean|loss| where |loss| > 1% acct, FALLBACK to `median` if zero full-stops; `median` mode =
  median|loss| (always defined when losses exist).
- **`lab/archive/class_s_aegis_solo_scoring_2026-07-16/HANDOFF.md`** §1 — native construction
  (operator-confirmed); 1R declared diagnostic-only.

---

## §1 — Context

Stage-2 (v2.1 winner c05) hard-failed the frozen §2.7 1R guard: the native $100K panel is a
0.40%/cap8 **mean-reversion** book (111 X-Short exits) whose losses are small and distributed
(max $631.56) — **no full-stop cohort** at the 1%-of-account threshold, so
`pin_r_basis(full_stop_mean)` FALLBACKs (5274c class → hard-fail).

**The guard is vestigial in the native path.** The §2.7 full-stop 1R guard was inherited from
candidate #1/#2, where 1R **re-scales** the CFD panel to the target risk% — there, a bad 1R
corrupts the sizing, so the hard-fail is essential. The **native-no-rescale** path (confirmed
HANDOFF §1) does **not** re-scale: c05 is the actual native-futures export, and `score_candidate`
runs the MC on the native daily book. **1R is not a scoring input**, so a FALLBACK 1R corrupts
nothing. The guard blocks a failure mode that cannot occur here.

**The guard-drop cannot bias the pending verdict** — because 1R does not enter the MC, changing
the 1R rule moves the H-SOLO result in **no** direction. Tail risk is still evaluated directly by
the MC's daily-book bootstrap (not by the 1R pin). This is the honesty anchor (§7).

---

## §2 — Frozen protocol

**Inherits v2 §2.7 byte-identical** (panel = c05; window 2022-01-12→2026-06-30; decompound-to-
static $100K; both firms `Tradeify_Select_100K` AND `MFFU_Rapid_100K`; Run-2; seeds 42/123/2026;
10k×3; horizon 1500; `dd_protection` OFF; inactivity off) **except:**

### §2.7′ — 1R rule for the native-no-rescale path (the ONLY delta)

The §2.7 full-stop 1R **hard-fail is REPLACED, on the native path only, by a non-gating
median-1R diagnostic:**
- Compute `pin_r_basis(pnl_static, "median", $100K)` and report it (informational — a panel
  sanity read, not a gate).
- Also report the full-stop attempt (method + n_full_stops) for transparency.
- **No hard-fail** on FALLBACK / n<5 full-stops when 1R is not a scoring input.
- **Scope:** native-no-rescale only. **Any path that re-scales a panel by 1R KEEPS the frozen
  §2.7 full-stop hard-fail** (unchanged — that guard remains load-bearing there).

Everything else in §2.7 is unchanged. The MC Part A engine, firms, and disposition are untouched.

---

## §3 — Calibration / discrimination note

No new panel, no new cells, no new MC parameters. Only the 1R **gate semantics** change (hard-fail
→ diagnostic) for the path where 1R is not load-bearing. The H-SOLO ceiling (bust ≤ 3.0% + pass ≥
50%) is untouched.

---

## §4 — Falsifier (H)

**H-SOLO (now runnable):** the c05 native panel alone clears Part A (**bust ≤ 3.0% AND P(pass) ≥
50%**, Run-2) on **BOTH** `Tradeify_Select_100K` AND `MFFU_Rapid_100K`.

**Falsified / close:** H-SOLO is **falsified** if **either** firm fails Part A (bust > 3.0% or
pass < 50%) on Run-2 → the winner expression closes; **no compose, no in-place reweight** (v2.1
§4). A cost-law (G2) kill on a firm counts as that firm not clearing.

**Guard-drop is not the hypothesis:** v2.2 only unblocks the run; the verdict is H-SOLO, decided
by the MC, unaffected by the 1R re-spec.

---

## §5 — Forbidden moves

- **Treating the 1R re-spec as able to change the MC outcome** — it cannot; 1R is not a scoring
  input on the native path. Any framing that leans on the guard-drop to explain a PASS is invalid.
- **Dropping the full-stop hard-fail on a RE-SCALE path** — the guard stays load-bearing wherever
  1R sizes the panel (candidate CFD path); v2.2 scopes strictly to native-no-rescale.
- **Using the median-1R diagnostic to re-scale** the panel (there is no re-scale).
- **Overriding a Part A FAIL** by any post-hoc metric (PF/expectancy/best-tier).
- **Switching `ACTIVE_FIRM`** off the FXIFY fixture; reading `compute_default_config()['bust_rate']`
  (use `summarize_outcomes`).
- **Composing with MYM+MNQ** inside this pre-reg (Stage-3 needs its own Class-S pre-reg).

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED (H-SOLO)** | Part A PASS on Tradeify_Select_100K **and** MFFU_Rapid_100K (Run-2) | Authorize Stage-3 Class-S compose pre-reg (separate artifact); rail/account still gated |
| **FALSIFIED** | Either firm fails Part A | Winner expression closes; no compose; no in-place reweight |
| **AMBIGUOUS** | Only if a frozen-gate calibration reference (if run) clears 3.0% on ≥2 tiers | Quarantine per gate §4/§6; do not claim H-SOLO |

Regime rider owed only on RESOLVED (gate §7(7)); FAIL does not overturn mechanical Part A.

---

## §7 — Prior-look disclosure (complete at freeze)

Inherits v2/v2.1 §7 (12 Stage-1 cells + v1 FALSIFIED + v2 AMBIGUOUS + v2.1 tie-break), **plus:**

| # | Date | Artifact | Note |
|---|---|---|---|
| s2 | 07-16 | Stage-2 run (`1ababcf`) | **NEEDS_CONTEXT** — §2.7 full-stop 1R FALLBACK; c05 max loss $631.56, 0 full-stops > $1,000 |
| gd | 07-16 | This 1R re-spec | authored **after** the NEEDS_CONTEXT; the guard-drop **cannot bias** the MC (1R not a scoring input) — so the H-SOLO verdict remains unbiased. Full-stop hard-fail retained on all re-scale paths. |

Honesty anchor: v2.2 is admissible because the re-specified guard does **not** feed the MC — the
pending H-SOLO verdict is independent of this change in every direction.

---

## §8 — Run protocol

1. §9 signed.
2. Update `run_aegis_solo_scoring.py`: 1R = non-gating median diagnostic (report full-stop attempt
   too); remove the FALLBACK/n<5 hard-fail on the native path; add v2.2 signature to Phase-0.
3. Re-run → `score_candidate` on the native $100K daily book across the frozen tiers; read
   `tiers[Tradeify_Select_100K].clears_part_a` **and** `[MFFU_Rapid_100K]`.
4. Write `RESULTS.md` + `aegis_solo_report.json`; verdict per §6; disclose prior-look s2/gd.

---

## §9 — Operator signature (the 1R re-spec freeze + Stage-2 re-run authorization)

```
SIGNED / FROZEN: 2026-07-16 / JA          (operator-directed in-session: "author v2.2 for option c, then re-run")
Re-spec the native-path 1R guard: full-stop hard-fail → non-gating median diagnostic (scope:
native-no-rescale only; re-scale paths keep the frozen full-stop hard-fail). Authorizes the
Stage-2 solo Part A re-run on the c05 panel. No override of a Part A FAIL.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature present
grep -n "SIGNED / FROZEN:" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md

# 2. Re-spec is scoped to native-no-rescale (re-scale paths keep the hard-fail)
grep -n "native-no-rescale only\|re-scale paths keep\|KEEPS the frozen" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md

# 3. Guard-drop cannot bias the MC (1R not a scoring input)
grep -n "cannot bias\|not a scoring input" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md

# 4. Driver: hard-fail removed on native path; median diagnostic present
grep -n "median\|non-gating\|diagnostic" lab/archive/class_s_aegis_solo_scoring_2026-07-16/run_aegis_solo_scoring.py

# 5. H-SOLO both-firms disposition intact
grep -n "Tradeify_Select_100K.*MFFU_Rapid_100K\|BOTH" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md --type brief
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Authored + §9 signed — v2.2 native-path 1R guard re-spec (full-stop hard-fail → non-gating median diagnostic; scope native-no-rescale only); unblocks Stage-2 re-run. Does not amend v2/v2.1 (Trap #12) | JA (operator, in-session) + Claude Code |
