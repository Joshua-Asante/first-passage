# Q-SFRISK-1 — Closure record: RESOLVED

**Closed:** 2026-07-15
**Closing verdict:** `RESOLVED`
**Parent brief:** [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](Q-SFRISK-1-successor-self-funded-risk-framework.md) (§6 gate criteria, §9 closure format)
**Pre-registration:** [`docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md`](pre-registration/Q-SFRISK-1-verdict-preregistration.md) (`9b219ab`, `NUMERIC FROZEN` 2026-07-14 — single triple T1, operator-confirmed via "confirm T1")
**Phase-1 numeric report:** [`lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md`](../../lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md) (merged `936a9e0`; independently cross-validated by a second local run this session — byte-identical numbers)
**Admitting artifact:** [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) (`Accepted`, ratified 2026-07-15)

---

## §1 — Verdict assertion (§6 applied to the Phase-1 numbers)

T1 is the sole declared triple (F2/TUW explicitly deferred, out of scope). Applying its three declared clauses to the Phase-1 report, both regime halves:

| Clause | Bar | H1 (2020-01→2023-03, 843 bd) | H2 (2023-03→2026-06, 844 bd) | Clears? |
|---|---|---|---|---|
| F1 — max-DD breach | p99 max-DD ≤ 10% / half | **8.00%** | **4.53%** | Both ≤ 10% ✅ |
| F3 — withdrawal model | ADOPT +5%/$200K banded | satisfied by construction (Phase-1 panel built under this model) | satisfied by construction | ✅ |
| F4 — impracticality | median days-to-first-skim > 252 bd ⇒ IMPRACTICAL | **51.0 bd** | **16.0 bd** | Both ≪ 252 bd — not impractical ✅ |

**All three T1 clauses clear on both regime halves.** Per the frozen §6 table (parent brief + pre-registration, identical wording):

> `RESOLVED` — "§8 Phase-0 numeric amendment committed **and** ≥1 declared triple clears both regime halves without crossing the §8 impracticality bar" → **Promote to admitting ADR / go-live risk artifact.**

Both conditions hold: the numeric amendment was committed and operator-ratified (`9b219ab`, "confirm T1"), and T1 — the sole declared triple — clears both halves on every declared clause without approaching the impracticality bar (H1's 51 bd is 4.9× inside the 252 bd ceiling; H2's 16 bd is 15.8× inside it). **H-SFRISK-1 is Accepted** under its own frozen text: "at least one §8-declared triple clears both regime halves under the declared bars without crossing the §8 impracticality bar, and an admitting ADR ... can be written from the result."

**Verdict: `RESOLVED`.**

---

## §2 — Fidelity note (transparency, not a gate)

F1's H1 p99 (8.00%) differs from the informal reproduction target cited in the pre-registration and the Phase-1 report (7.76%, from `RESULTS_cleanvintage_2026-06-25.md`'s LOCKED row) — pass/bust/median-days are byte-identical across both figures; only the max-DD tail statistic moved. This is **explained, not a defect**: [`docs/adr/2026-07-06-bust-day-maxdd-inclusion.md`](../adr/2026-07-06-bust-day-maxdd-inclusion.md) (`Accepted`, landed `83e589f`, 2026-07-06) corrected the MC engine so a bust path's `max_dd` includes the breach day's own drawdown — a fix that lands between the 2026-06-25 reference doc and every Phase-1 run, and scales with bust rate (H1's 13.84% bust moves; H2's 0.21% bust does not, and indeed H2 matches exactly). The 8.00% figure is the current, correct number under the ratified engine fix. It does not change T1's disposition — H1 still clears the 10% bar with 2.00pp of headroom.

Two independent Phase-1 runs (one merged to main via `936a9e0`, one run locally this session against the identical frozen spec) produced byte-identical numbers across every reported cell — cross-validating both the instrument's determinism and the correctness of the F4 panel-source fix (clean-vintage panel, not the stitched 2026-06-07 vintage `days_to_first_skim.build_banded_portfolio_panel()` would have defaulted to).

---

## §3 — Completion falsifier discharge (rescope ADR §4)

[`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../adr/2026-07-11-challenge-era-claims-rescope.md) §4's completion falsifier required a successor risk-framework Pre-Q pre-registered by 2026-11-08, or D1 escalates to a mandatory go-live blocker. This closure discharges it in full — existence (architecture pre-registered 2026-07-14), numeric freeze (T1 confirmed 2026-07-14), analysis (Phase 1 run + merged 2026-07-15), and verdict (this closure, `RESOLVED`, 2026-07-15) — well inside the hard date. See the rescope ADR's dated addendum for the formal discharge note.

---

## §4 — What this closure does NOT do

- **It does not authorize Aegis→M6J go-live.** Per `CLAUDE.md`'s Live-execution posture, go-live is a separately gated operator decision; this closure supplies that decision's risk-characterization input (a falsifiable successor to the retired challenge-era P(pass) claim), it does not substitute for the gate itself.
- **It does not re-open F2/TUW.** Deferred by explicit operator scope in the Phase-0 freeze; T1 is a 3-dimension triple by design. A future amendment may add a TUW clause without altering this RESOLVED disposition (T1 stands on its own three clauses).
- **It does not touch any locked parameter, allocation, `dd_protection` constant, or the historical MC anchor (99.83/0.17/4.37).** Zero `core/` behavior change; this closure and its admitting ADR are governance/documentation layer only.

---

## §5 — Downstream artifacts (this closure's obligations)

- [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](../adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) — the admitting ADR (§7 step 3 of the parent brief), `Accepted`, ratified 2026-07-15.
- Parent brief `Status` flips `OPEN` → `CLOSED-RESOLVED`, pointing here.
- Rescope ADR (`2026-07-11-challenge-era-claims-rescope.md`) — dated addendum discharging §4's D1 completion falsifier.
- `STATE.md` — the SFRISK forward-board entry updated from "Phase 1 unblocked" to closed/RESOLVED, pointing at this closure.
- `docs/SESSIONS.md` — session entry recording the closure.

---

## §10 — Audit hooks (runnable)

```bash
# Verdict recorded
grep -n "Verdict: \`RESOLVED\`" docs/briefs/Q-SFRISK-1-closure-resolved.md

# Parent brief flipped closed
grep -n "^\*\*Status:\*\*" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md
# Expected: CLOSED-RESOLVED

# Admitting ADR exists
test -f docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md

# Rescope ADR's completion falsifier discharge addendum present
grep -n "D1 completion falsifier discharged" docs/adr/2026-07-11-challenge-era-claims-rescope.md

# No core/ / allocation / dd_protection / Pine touch by this closure
git diff --stat <pre-closure-commit> -- core/
# Expected: empty

# Validators unaffected
python scripts/verify_lock_anchors.py
# Expected: ROUTING: Closed
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/Q-SFRISK-1-closure-resolved.md --type closure

git log -1 --format='%h %ci' -- lab/analysis/regime/decompound_remc_2026-06-07/RESULTS_sfrisk_t1_phase1_2026-07-15.md
# Expect the merge commit that landed 936a9e0's content
```
