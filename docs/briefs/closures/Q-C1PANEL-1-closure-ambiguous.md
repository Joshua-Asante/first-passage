# Q-C1PANEL-1 — Closure: `AMBIGUOUS` (premise failure at Phase 0, pre-run)

**Verdict:** `AMBIGUOUS` — premise failure detected at **P0.1**, before any pull, port, or re-MC arm.
**Closed:** 2026-07-23 (same day as authoring + signature)
**Brief:** [`Q-C1PANEL-1-c1-regime-panel-start-boundary.md`](../Q-C1PANEL-1-c1-regime-panel-start-boundary.md)
**Pre-registration:** [`Q-C1PANEL-1-verdict-preregistration.md`](../pre-registration/Q-C1PANEL-1-verdict-preregistration.md) — `FROZEN`, signed 2026-07-23 / JA, freeze commit **`6674c32`** (2026-07-23 17:55:25 -0400)
**Spend:** **$0.00.** No databento pull. No port built. No re-MC arm run. No K consumed. No manifest touched.
**Live effect:** **none.** c1 rung stays **WATCH-1 0.50× / disarmed**. `core/` · allocations · `dd_protection` · Pine all untouched; lock HELD.

---

## 1. Verdict in one line

The instrument was **void on its own terms** before it could produce a verdict: P0.1 falsified one of the three structural premises the brief declared binding, and surfaced a second, independent design bias pointing at the operator's preferred answer.

---

## 2. What P0.1 measured

Both byte-pinned panel CSVs read from the primary checkout; **both sha256 pins verify** against `core/data/tv_exports/cme/SHA256SUMS`.

| Leg | File | sha256 | Trades | Span |
|---|---|---|---|---|
| MYM | `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` | `9acfa297…` ✓ | 267 | **2020-01-14 11:15 → 2026-06-30 12:00** |
| MNQ | `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv` | `8884e6dd…` ✓ | 284 | **2020-01-06 09:45 → 2026-06-30 14:30** |

Entry-row distribution by year — MYM `{2020:20, 2021:22, 2022:52, 2023:54, 2024:51, 2025:49, 2026:19}`; MNQ `{2020:48, 2021:45, 2022:31, 2023:55, 2024:44, 2025:37, 2026:24}`.

**Mootness trigger did not fire** (panel starts after 2019-05-06). The gap to contract launch is **~8 months** (2019-05-06 → 2020-01-06), not the ~14 the brief assumed.

---

## 3. Why the run is void

The brief's §5 declared three structural defenses against panel-shopping, "all binding," with the clause: *"If any of the three is weakened during execution, the run is void."*

| Defense | Status after P0.1 |
|---|---|
| 1. Falsifier is two-sided (0.50× PASS→FAIL moves the live rung **down** to 0.25×) | **Intact** |
| 2. Boundary is the contract-launch date — a fact that cannot be shopped | **Intact** |
| 3. Added window is chop/crisis ⇒ makes the gate **harder** | **FALSIFIED** |

**Defense 3 rested on a factual error.** The brief argued the extension adds "pre-COVID grind plus the March-2020 crash." The March-2020 crash is **already inside the panel** — it starts 2020-01. The actual added window is **May–Dec 2019**: two modest vol episodes (May trade-war selloff, August curve inversion) inside a strongly trending year. That is **H2-type regime material, not the H1 chop the partition exists to capture.**

### 3b. Second, independent defect — the split rule biases toward PASS

The partition is **index-midpoint on trade count** (`part_b_half_panel`, harness L127). Prepending trades therefore moves the H1/H2 boundary **earlier in calendar time**:

| Leg | Incumbent boundary | Post-extension (est., at 2020 trade rates) |
|---|---|---|
| MYM | 2023-10-10 | ~2023-08-18 |
| MNQ | 2023-05-15 | ~2023-01-17 |

So extended-H1 would **gain benign 2019 *and* shed late-2023 material to H2** — its composition moves toward passing for reasons unrelated to statistical power. In the emitted numbers this would be **indistinguishable** from a genuine "1.00× now clears H1." The frozen instrument was mechanically biased toward the answer the operator wanted, and the brief did not see it.

This was **not** caught by the two intact defenses. Two-sidedness protects against *choosing* a favourable panel; it does not protect against a panel change that *re-partitions* the very cut being tested.

---

## 4. Why the panel axis is closed for c1 — not merely paused

The obvious repair — pin the H1/H2 boundary in **calendar** terms at the incumbent date, so extension lengthens H1 and leaves H2 byte-identical — is sound in isolation and would remove defect 3b. **It does not rescue the instrument**, for a reason no design change reaches:

- The only history available to add is **2019-05-06 → 2020-01-06**, and 2019-05-06 is the **CME contract-launch date for MYM and MNQ**. There is no more native micro history to buy, from databento or anyone.
- That 8 months is predominantly **trending, low-vol** material. The H1 verdict's real weakness is **power** — bootstrap-95th **10.37%** against a 3.0% floor is a very wide band — and adding wrong-regime data **dilutes** that estimate rather than sharpening it.
- Parent-instrument history (YM/NQ back to 2010-06-06) is **not admissible** here: the proxy-discipline rule makes parent data valid for structural discovery, **not for P&L**, and this gate is entirely P&L/bust-denominated.

**Standing consequence:** the panel axis is closed for c1 by *data physics*, not by the §5 no-repeat clause (which by its letter binds only on `RESOLVED-PANEL-ROBUST`). Re-opening requires genuinely new data — which for these two instruments means the passage of live time, not a new window over the same history.

**Therefore: databento cannot resolve the 1.00× rung question.** The binding constraint is the instruments' age, and no subscription changes it.

---

## 5. Process defect **PD-1** — §0 read the wrong artifact for the panel span

The brief's §0 honestly flagged that the panel CSVs were unreadable from the authoring worktree and correctly made the span a **blocking Phase-0 read** — which is why this was caught before spend. But the substituted Tier-3 value was wrong, and **the correct value was already recorded in a source the brief cited by path**:

- [`docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md`](../pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) **§2, line 116** — *"Panel window | 2020-01-06 → 2026-06-30 (1692 bdays)"* (also line 50).
- [`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md) **line 43** — *"window 2020-01-06 → 2026-06-30 (1692 bdays)"*.

The brief instead took `2020-07-01` from [`STATE.md`](../../../STATE.md) line 678, **which is correct** — it describes the **BAR EXPORT bar panels** (`core/data/bar_data/{MYM,MNQ}_M15.csv`, first bar verified `2020-07-01T23:00:00Z`, 141,471 / 141,536 bars), a **different artifact** from the List-of-Trades panels the gate consumes.

**No repo artifact misstates the c1 scoring-panel span.** A propagation sweep of every `2020-07-01` occurrence found all of them referring correctly to the bar panels. **There is nothing to correct in the repo** — the defect was authoring-side substitution of a same-named field across two artifacts of the same instrument pair.

**Counterfactual cost:** had §0 read the cited parent pre-registration for this field, the brief would **never have been authored** — the 8-month gap and the benign-2019 composition are both visible directly from that one line. The blocking Phase-0 gate contained the damage to zero dollars and zero K, but it fired one step later than a complete §0 would have.

**Lesson candidate (methodology):** *when a brief cites a frozen parent artifact in lineage, read it for every field the child re-states — a cited-but-unread parent is a Tier-4 source wearing a Tier-1 label.* Extends [[feedback_verify_source_not_label]] and the Rule-0 surrounding-context sub-rule from "read around the line" to "read the parent you cite." Dated anchor: this closure. Cost: one authoring cycle + one operator signature, $0 spend.

---

## 6. Disposition

| Item | Disposition |
|---|---|
| c1 lifecycle rung | **Unchanged — WATCH-1 0.50×, disarmed.** No movement in either direction (§6 `AMBIGUOUS`). |
| 1.00× admissibility | **Unchanged — inadmissible.** The incumbent 2026-07-17 both-halves FAIL stands as the operative evidence. This closure supplies **no** fresh both-halves PASS, so the EV-ADR §Trigger-1 bar is unmet. |
| Incumbent haircut pre-registration | **Byte-unedited** (Trap #12 honored). |
| Q-C1PANEL-1 pre-registration | **Frozen, unedited, retained** as the record of what was authorized and why it halted. |
| Panel axis for c1 | **Closed by data physics** (§4). Re-opening requires new live time, not a new window. |
| B7 arm / M1 monitoring | **Unaffected** — separately gated, untouched by this instrument. |
| Databento | **Does not bear on the rung question.** See §4. |

---

## 7. What the pre-registration predicted vs what happened

The pre-registration anticipated three failure routes: §4a reproduction deviation, §4b parity failure, and P0.1 mootness. **None of them fired.** The instrument died on the parent brief's §5 void clause — a route the pre-registration's §6 verdict table did **not** enumerate, and which had to be mapped onto `AMBIGUOUS` via its "Defect/premise failure" disposition text.

**Second lesson candidate (brief-authoring):** *a §5 void clause is a verdict route; enumerate it in §6.* The gate table listed only the defect routes the author expected the *execution* to hit, not the one where a declared premise is falsified by the brief's own Phase-0 read. Repair for future briefs: any "if X is weakened, the run is void" clause gets a matching §6 row.

---

## 8. Audit hooks (this closure)

> **Note on the freeze commit's subject line (PD-2, cosmetic).** `6674c32` was authored with
> PowerShell here-string syntax (`@'…'@`) passed to a Bash shell, so its **subject line is a bare
> `@`** and a stray `@` trails the body. **The message body is complete and correct**, and the
> commit's content, author, and timestamp are untouched. It was **deliberately not rewritten**:
> this is the *freeze* commit, its hash is cited by three artifacts (this closure, the brief §8,
> `STATE.md`), and its evidentiary value is precisely that it has never been amended. Rewriting a
> freeze commit for cosmetics would destroy the property it exists to prove. Verify the body with
> `git log -1 --format='%B' 6674c32`.

```bash
# Freeze predates every Phase-0 artifact (the load-bearing audit property).
git log -1 --format='%h %ci' 6674c32

# Freeze commit body is intact despite the cosmetic '@' subject (PD-2).
git log -1 --format='%B' 6674c32 | sed -n '2p'   # real subject: "brief(Q-C1PANEL-1): freeze…"

# Panel truth — re-derivable from the byte-pinned CSVs (primary checkout; gitignored).
cd "$(git rev-parse --show-toplevel)" && sha256sum \
  "core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv" \
  "core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv"
# expect 9acfa297… and 8884e6dd…

# The correct span was always recorded in the frozen parent pre-reg (PD-1).
grep -n "2020-01-06" docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md
grep -n "2020-01-06" lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md

# Every repo 2020-07-01 refers to the BAR EXPORT bars, not the scoring panel (no correction owed).
head -2 core/data/bar_data/MYM_M15.csv   # first bar 2020-07-01T23:00:00Z

# No extension artifact was ever created.
ls -d lab/analysis/c1_panel_extension_* 2>/dev/null | wc -l   # must be 0

# Incumbent evidence untouched.
git log --oneline -- docs/briefs/pre-registration/2026-07-16-class-s-c1-lifecycle-haircut-regime-remc-preregistration.md
grep -n "4.37\|10.37" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS.md | head -3
```

---

## 9. Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | Closure authored `AMBIGUOUS` — premise failure at P0.1 (defense 3 falsified; split-rule bias 3b surfaced). Panel axis closed for c1 by data physics. PD-1 recorded: §0 substituted the bar-panel span for the trade-panel span; correct value was in the cited-but-unread frozen parent pre-reg. Two lesson candidates raised. $0.00 spend, no K, no live effect. | Joshua (direction) + Claude Code (Opus 4.8) |
