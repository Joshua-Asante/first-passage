# 02 — BLOCKER tier (both rounds) — all three FIXED

**What this file is.** Every **BLOCKER**-severity finding the two-round post-de-scope claim-alignment audit produced: **3 rows**, all three from round 1 (`B1`–`B3`, ported from the round-1 artifact's §5.1), touching **7 target files** across **3 commits**. **All three are FIXED and committed.** Round 2 raised **zero** new BLOCKERs — read [§Round 2](#round2) below before concluding what that means. **8 residue items** are carried forward by name; **none is at BLOCKER severity**, and none is a re-opening.

**Evidential standing — the highest in this set.** All three rows are round-1 findings, raised against a **21.4%** refutation rate, each survived the adversarial pass, and each carried a **runnable hook executed at anchor `e031225`** in the round-1 artifact. Every one of those hooks has been **re-executed at HEAD for this section** and the output is pasted below (§Verification). Round 2 contributes no finding here — only a residue enumeration on B3, reported as executed rather than asserted. The README's round-1-vs-round-2 standing note does not bear on this file.

**This file's job is twofold and both halves matter.** It is the record that these three are **CLOSED**, so a future reader does not re-open them. It is equally the record that **the failure class is not closed**: three repaired BLOCKERs against **250 confirmed findings** is not a repaired estate — the agent-facing, MISLEADING, COSMETIC and operator-judgement sections carry the remaining **247**, and every one of them is still a recommendation pending operator ruling.

**Pointer:** section index, combined counts, and the round-1-vs-round-2 evidential-standing note live in [`README.md`](README.md).

---

## Status at a glance

| # | Finding | Target files | Commit | Status | Residue carried |
|---|---|---|---|---|---|
| **B3** | Reserve denominator `cap_firm` → `cap_alloc[leg]` in the normative sizing law | `docs/spec/c1_watch_realization_multiplier_layer.md` §2 · `docs/spec/c1_nt8_sizing_host_impl.md` §2.2/§2.3/§7 | [`d84c5e4`](#b3) | ✅ **FIXED** 2026-08-05 | **4** — one live spec line, one live agent skill, one frozen LOCK record, one frozen baseline JSON |
| **B2** | `STATE.md`'s published 08-08 rider-enumeration command under-reaches | `STATE.md` | [`a818b3f`](#b2) | ✅ **FIXED** 2026-08-05 | **2** — the durable additive-field fix is unratified; the hand-check table drifts |
| **B1** | The GO ADR carries no reader-intercept of the de-scope that spent its deployment limb | `docs/adr/2026-07-17-…-go.md` · `docs/adr/2026-08-04-…descope….md` · `docs/adr/INDEX.md` · `docs/notes/rail_build/RUNBOOK.md` | [`ae5ffe7`](#b1) | ✅ **FIXED** 2026-08-05 | **2** — one un-mirrored Authority claim in `deploy/`; one standing over-reach in `STATE.md` |

**Ordering is by consequence, not by ID.** Round 1's §7 recorded the honest inversion in its own follow-up list — B3 is the highest-consequence item in the audit and appeared **second** there, behind a calendar-forced row, because *urgency is not consequence*. Nothing forces that ordering here, so it is reversed. B3 also differs in kind from B1 and B2: it is **not de-scope-caused**. It descends from the 2026-07-22 account-aggregate cap split and had been latent for fourteen days.

---

<a id="b3"></a>

## B3 — the reserve denominator: `cap_firm` → `cap_alloc[leg]` · FIXED `d84c5e4`

> **Class:** contradiction · **Verdict as filed:** `KEEP-CORRECTED` · **Not de-scope-caused.**

### B3.1 — What was claimed (round 1 §5.1, verbatim from the Action cell)

> **Highest safety consequence in the audit, and not de-scope-caused.** RESERVE line → `qty_base = min(qty_base, floor(cap_alloc[leg] / (1 + pyr_pct/100)))`. Add above the fence as a normative safety property: *"the cap is account-aggregate, allocated per leg (MYM 69 / MNQ 11 since 2026-07-22); a missing `cap_alloc` must **HALT**, never fall back to `cap_firm` — the fallback computes 1.91× the account limit (MYM 76 + MNQ 77 = 153 against 80)."* … **Do not touch `ops/c1_rail/c1_sizing_host_reference.py` — production is correct — and do not change the 69/11 values.**

### B3.2 — What was verified

**The mechanism, stated plainly.** `docs/spec/c1_nt8_sizing_host_impl.md` declares at L6/L16 that the WATCH spec's §2 law is *"the sizing law this spec implements verbatim (not re-derived)"*. That §2 law read:

```
qty_base  = min( qty_base, floor( cap_firm / (1 + pyr_pct/100) ) )      # RESERVE: the add must fit under the firm cap
```

`cap_firm` is **80** — the *account-aggregate* micro cap for `Tradeify_Select_100K`, counted across both legs. An implementer following the declared chain divides the **whole** account cap **per leg**, and the arithmetic is not a rounding difference:

| Leg | `pyr_pct` | Whole-cap divisor (what the spec said) | Base | Add | Leg total |
|---|---:|---|---:|---:|---:|
| MYM | 750% | `floor(80 / 8.5)` | **9** | `floor(9 × 7.5)` = **67** | **76** |
| MNQ | 1000% | `floor(80 / 11)` | **7** | `floor(7 × 10)` = **70** | **77** |
| | | | | **Aggregate** | **153 against an 80 limit — 1.91×** |

Against the correct per-leg allocation (`cap_alloc` MYM 69 / MNQ 11): `floor(69/8.5) = 8` → add **60** → 68; `floor(11/11) = 1` → add **10** → 11; aggregate **79 ≤ 80**.

**Production was already correct, and records the breach in its own header comment.** `ops/c1_rail/c1_sizing_host_reference.py` divides by `cap_alloc` (L296), halts on a missing `cap_alloc` (L287–291, *"a missing `cap_alloc` is a state defect"*) and halts on `cap_alloc > cap_firm` (L293–295). L68–70 names the pre-split behaviour and its measured consequence verbatim. **The defect was spec-side only, in both directions: the spec understated what production does, and no code was ever wrong.**

**The shape of the miss — a fix that landed where the thing is CHECKED, not where it is READ.** The 2026-07-22 split changed production. The [2026-08-02 `9/67` staleness sweep](../../../2026-08-02-cap-split-9-67-staleness-sweep.md) found the WATCH spec's **§10 audit hook** asserting the pre-split pair — *"A RUNNABLE HOOK THAT HAS BEEN FAILING SINCE 2026-07-22"* — and re-pinned it to `(8, 60)`. It did **not** touch §2. From **2026-08-02 to 2026-08-05 the file contradicted itself**: its executable hook asserted `(8, 60)` while its normative law thirty lines above asserted the arithmetic that produces `(9, 67)`.

⚠ **The sweep's own closing lesson explains the miss, which is why it is worth pinning rather than scolding.** §4 of that note reads: *"A superseded constant is most dangerous where it is executable… When a pin is re-pinned, grep for it in **audit hooks and tests first**, prose second."* That prioritisation is correct about danger and **wrong about completeness**: it triaged the normative law into the "prose second" bucket, where it stayed. A *normative sizing law* is not prose — it is source for a human implementer, and this repo's declared chain says so on the face of the consuming spec.

**Executed at `e031225` (round-1 hook H3), output as printed:**

```bash
rg -n 'cap_firm' docs/spec/c1_watch_realization_multiplier_layer.md
# spec L43  "qty_base  = min( qty_base, floor( cap_firm / (1 + pyr_pct/100) ) )"
# spec L47  constants gloss naming cap_firm — and NO occurrence of cap_alloc in the file
```

### B3.3 — What was actually done · `d84c5e4`

*(commit title: `fix(spec): B3 — reserve denominator cap_firm -> cap_alloc in both sizing specs`)*

| File · anchor | Change |
|---|---|
| `docs/spec/c1_watch_realization_multiplier_layer.md` §2 fence | RESERVE line → `qty_base = min( qty_base, floor( cap_alloc[leg] / (1 + pyr_pct/100) ) )`, comment re-worded to *"must fit under **THIS LEG'S** cap share"* |
| same file, above the fence | **Normative safety property added**: the cap is account-aggregate allocated per leg (MYM 69 / MNQ 11); applying `cap_firm` per leg computes **153 against 80 (1.91×)**; **a missing `cap_alloc` must HALT, never fall back** — mirroring production at `c1_sizing_host_reference.py:290-296` |
| same file, constants gloss | `cap_firm` re-defined as the account-aggregate **bound only, never a per-leg denominator**; `cap_alloc[leg]` added, sourced to `LEG_MAP`, with `Σ cap_alloc ≤ cap_firm` named as a host-asserted invariant |
| same file, worked check | `floor(80/8.5) = 9` → `qty_add = 67` becomes `floor(cap_alloc 69 / 8.5) = 8` → `qty_add = 60`, pinned to `f2_floors.json` `legs[0].recent_90d`; the pre-split pair is **retained under a labelled provenance note**, not deleted |
| same file, Change history | Dated `2026-08-05` row recording the correction, its cause, and *"Production was already correct and is untouched; no encoded value changed; the 69/11 split is unchanged."* |
| `docs/spec/c1_nt8_sizing_host_impl.md` §2.2 | `reserve_cap = floor(cap_alloc / (1 + pyr_pct / 100))` with inline `HALT if absent (§5); NEVER fall back to cap_firm` |
| same file, §2.3 constants mirror | `c1_sizing_constants.json`'s leg map **must carry `cap_alloc` per leg**; missing ⇒ HALT; `cap_firm` retained as the bound |
| same file, §7 worked-check target | `9` / `67` → **`8` / `60`**, with a dated `⚠ Corrected 2026-08-05` intercept naming the pre-split key |

**What was deliberately not touched:** `ops/c1_rail/c1_sizing_host_reference.py` (production, already correct), its tests, `f2_floors.json`, and the `69/11` values. **The repair moves the spec to production, never the reverse** — round 1 flagged the inverse reading as the single most likely misreading of B3, and it remains so.

### B3.4 — What remains open — residue

**The residue question round 1 did not ask and round 2's specs-and-plans domain did:** does any *other* consumer inherit the whole-cap assumption? Enumerated by execution at HEAD (post-`d84c5e4`), not asserted:

```bash
rg -n --no-ignore 'cap_firm|cap_alloc|reserve_cap|floor\(80' .            # whole tree, ignore-files bypassed
rg -n --no-ignore 'reserve_cap|cap_firm|cap_alloc|floor\(80' .claude/ .cursor/ deploy/
# Executed 2026-08-05 at HEAD. Second command: NO OUTPUT, exit 1 (zero matches).
# ⚠ THAT ZERO IS NOT THE ANSWER — the four tokens are this repo's vocabulary, not the law's.
# Re-run on the CONCEPT (the account cap used as a per-leg denominator, under any name):
rg -n --no-ignore 'account_cap|micro_contract_cap|RESERVE cap' .claude/ .cursor/ deploy/
#   .claude/skills/prop-firm-challenge/SKILL.md:189  "capped by the tier's `micro_contract_cap`"
#   .claude/skills/prop-firm-challenge/SKILL.md:191  "**RESERVE cap rule** ... floor(account_cap / (1 + pyramid_pct))"
#   .cursor/, deploy/ -> still zero. See R-B3d and the correction note below.
```

**Four residual sites. None is at BLOCKER severity; none is a code path.**

| # | Site · anchor | What it carries | Class | Disposition |
|---|---|---|---|---|
| **R-B3a** | `docs/spec/c1_watch_realization_multiplier_layer.md` **L18** (§0 Rule-0 read block) | *"MYM recent-90d: ideal base 11 → RESERVE-capped **9**, add **67** … **These are the numbers any realization mechanism must reproduce.**"* | **normative clause inside a dated read block** | **Not covered by `d84c5e4`, and the most consequential of the three.** Trap #12 protects the *read* — it is a correct record of what `f2_floors.json` held on 2026-07-17 — but the trailing sentence is a **live normative instruction**, and it names the pre-split pair. **Action:** append a bracketed intercept immediately after that sentence, leaving the read byte-intact: *"⚠ 2026-08-05 — `f2_floors.json` was re-pinned 2026-07-22 to `(8, 60)` under the per-leg `cap_alloc` allocation; the `(9, 67)` pair above is the pre-split record retained under `pre_2026_07_22_whole_cap_per_leg` and is **not** what a realization mechanism must reproduce. See §2 and the Change history."* **Couple with round-1 `U2`**, which carries two further defects on this same §0 block (a lapsed Status deferral at L3, a `git log` verification line naming a deleted path) and was left **unadjudicated** — one file open, three edits, one commit. |
| **R-B3b** | `core/strategies/_archive/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md` **L21** | *"RESERVE at cap 80 → base max `floor(80/11)=7`"*, alongside venue-delta item 5's *"`microCap` default **80**"* | **whole-cap-per-leg in a frozen venue-edition LOCK record** | **The 08-02 sweep could not reach it**: that sweep searched the **MYM** `9/67` pair, and this site states the **MNQ** form, whose numbers (`7`, `70`) share no digits with the pattern. Same defect family, different arithmetic — the exact reason a pattern-scoped sweep is not a class-scoped one. **Consequence today is nil**: the file is cold-stored (`241cef4`), stamped **`NOT live.`**, no strategy is deployed, and the rail's sizing authority is the host, not Pine. **Action: impeach, do not edit** — this is a frozen LOCK record (Trap #12). Add a row to the 08-02 sweep note's §2 impeachment table naming the MNQ form and the correct post-split values (`floor(11/11)=1`, add `10`). ⚠ If a successor venue is elected at F3 and a Pine edition is re-pointed, the `microCap` input default becomes live again — record that as the trigger, not as a current defect. |
| **R-B3c** | `docs/notes/substrate_retirement_baselines/baseline_c1_lifecycle_ddp.json` — `c1_sizing_constants.leg_map` | `cap_firm: 80` at top level; **both legs carry `base_risk`/`dollars_per_pt`/`leg_key`/`pyr_pct` and NO `cap_alloc`** | **frozen baseline snapshot** | **Fail-safe, not permissive — and that is the whole finding.** Replayed as constants, production halts (`if "cap_alloc" not in leg_const: return _halt(...)`, L287–291) rather than falling back. **No action.** Recorded here only so a future reader does not read the *absence* of `cap_alloc` as evidence that the whole-cap form is still sanctioned. |
| **R-B3d** | `.claude/skills/prop-firm-challenge/SKILL.md` **L191** (§Futures venues) | *"**RESERVE cap rule** for pyramided strategies: base position size must be capped at `floor(account_cap / (1 + pyramid_pct))` so the pyramid add-on never gets starved of headroom by an oversized base."* — with **L189** immediately above it: *"capped by the tier's `micro_contract_cap`"* | **the whole-cap-per-leg law restated on the auto-loading agent surface, under a different token** | **The one live site, and it was missed by the token sweep — see the correction note below.** The rule is **not false**, it is **incomplete**: for a single pyramided leg on an account, `floor(account_cap / (1+pyr))` is exactly right, and L189 correctly sources the cap from `micro_contract_cap`. It breaks the moment **two** pyramided legs share one account-aggregate cap — which is the c1 book, and which is what produced **153 against 80**. **Action:** append one clause to L191 and nothing else — *"— where `account_cap` is **this leg's allocated share** when several legs share one account-aggregate cap (Tradeify counts the limit across the whole account; the c1 book allocates MYM 69 / MNQ 11 of 80). Applying the **whole** account cap per leg computes 1.91× the limit. A missing per-leg allocation must **HALT**, never fall back to the account cap — `ops/c1_rail/c1_sizing_host_reference.py:287-296`."* ⚠ **Live-consequence note, and it is why this is not COSMETIC:** this section is the skill's **durable, venue-generic** sizing knowledge, not a c1 posture paragraph — it is what an agent reads when sizing a pyramided book at a **successor** venue, which is precisely what **F3** may elect on 08-08. The de-scope did not defuse it. **Severity MISLEADING, not BLOCKER** — no rung of it reaches production, and the host halts on the shape it would produce. The archived ancestor of the same line (`docs/ltm/superpowers/plans/2026-07-08-prop-firm-challenge-skill.md` L190) is **LTM, dated, and out of audit scope — no action**; its live design spec (`docs/superpowers/specs/2026-07-08-prop-firm-challenge-skill-design.md` §8) names the rule by title only and states no formula, so it needs no edit. |

⚠ **Correction to this section's own first pass, recorded rather than quietly fixed.** The enumeration above was first run on the four tokens `cap_firm | cap_alloc | reserve_cap | floor(80)`, returned **zero** matches across `.claude/`, `.cursor/` and `deploy/`, and this file concluded from that zero that *"the skill surface never inherited this defect because it never restated the law."* **That conclusion was wrong.** The skill restates the law under the token **`account_cap`**, which shares no substring with any of the four. Re-run on the *concept* rather than the vocabulary, it surfaces immediately — R-B3d. **This is R-B3b's lesson firing a second time inside the same section**: a pattern-scoped sweep is not a class-scoped one, and the 08-02 sweep, round 1, and this section's first pass each missed a different member of one defect family by searching for the previous member's characters. It is left visible because the residue's whole point is that the class is not closed.

**Sites checked and found clean** — reported so the negative is auditable rather than assumed: production (`c1_sizing_host_reference.py`) and its tests (`test_c1_sizing_host_reference.py:345,383-412`, which assert `cap_firm`/`account_cap` as a **bound**, not a denominator); `lab/analysis/c1/band_quantization_2026-08-02/` (runner + RESULTS, both use `cap_alloc = floor(share × cap_firm / 80)` and constrain the realized aggregate to `cap_firm`); `docs/briefs/pre-registration/2026-08-02-sub100k-realizable-book-scoring-prereg.md` (aggregate usage); `Q-CAPALLOC-1-verdict-preregistration.md` (labels the pre-split pair explicitly); `lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md` (states the law with `cap_alloc`); `lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py` L5-20 (docstring states the whole-cap arithmetic **and** labels it `PRE-2026-07-22`, then states the correction — a model of how a dated harness should carry a superseded rule); `ops/instruments/{MYM,6J}.md` (both reason from `cap_alloc`, and 6J's L81 uses `69 + 11 = 80, zero headroom` as a live structural constraint); the GO ADR L226/L232 (historical narration of the defect and its fix). **`.cursor/` and `deploy/` are clean on both the token and the concept** — neither restates a sizing law at all.

---

<a id="b2"></a>

## B2 — `STATE.md`'s published 08-08 rider-enumeration command under-reaches · FIXED `a818b3f`

> **Class:** gate-unreachable · **Verdict as filed:** `SIMPLIFY`.

### B2.1 — What was claimed (round 1 §5.1, verbatim from the Action cell)

> The one-line `rg 'Trigger check schedule.*2026-08-08'` returns **33** and is single-line, single-spelling. Replace with: defer to `python -m ops.sentinel.scan` for the wrapped-field and `**Check schedule:**` cases, **plus a named hand-check list** for the class no pattern reaches — hard-core **P1, P2, P3, P4** … **Preferred durable fix:** give P1–P4 and the params-toml ADR an additive `**Trigger check schedule:** 2026-08-08 quarterly` field … Additive metadata only: **do not touch §2 decision text, §4 falsifier logic, or any [RATIFY] line.**

### B2.2 — What was verified, and the corrected measurements

The finding held: the board published a one-line, single-spelling pattern as the mechanical way to enumerate every ADR riding the 2026-08-08 quarterly, and it silently drops files. Fixing it required measuring the residue properly, and **three of round 1's numbers moved**.

| Quantity | Round 1 said (H2 @ `e031225`) | Measured while fixing (`a818b3f`) | At HEAD, 2026-08-05 |
|---|---:|---:|---:|
| Published one-liner reach (`rg -l 'Trigger check schedule.*2026-08-08' docs/adr/`) | **33** | **33** | **34** |
| `ops/sentinel` field-form reach (canonical invocation) | *not measured* | **36** | 37 — one ADR joined the field-form class; not re-run, see below |
| ADRs mentioning `2026-08-08` at all | 54 *(file count incl. `INDEX.md`)* | **53** *(ADRs; `INDEX.md` excluded)* | **55** |
| Residue carrying the duty in **prose with no trigger field** — reached by *no* tool | *not enumerated* | **17** | **18** |
| — of which are **live obligations** needing a hand-walk | *"≥8 live-obligation files"* | **~10** | ~10 |
| — of which are **hard-core integrity gates** | **four** (`P1`–`P4`) | ⚠ **FIVE** (`P1`–`P5`) | FIVE |

⚠ **The four-versus-five error was visible inside the round-1 artifact itself.** Its Action cell named `P1, P2, P3, P4`; its own hook **H2**, ten lines of output later, printed *"Cross-check: `rg -l '2026-08-08' docs/adr/2026-07-03-hardcore-p*.md` returns **ALL FIVE** (P1..P5)."* The hook was executed and the count was correct; the prescription was written against the author's recollection of it. **The artifact contradicted its own pasted evidence, and no gate reads an audit note.** This is the sharpest instance in either round of the class the whole audit is about, and it is filed against the audit, not against the estate.

**Why a third class exists at all, and why it is not a sentinel bug.** `ops/sentinel/scan.py:147` deliberately restricts matching to the **field form** so that change-history rows, §0 stamps and prose mentions of the date do not read as triggers. That is correct design: a scanner that matched prose would report the withdrawn 08-02 ADR (whose trigger table is expressly *"NO LONGER IN FORCE"*) as a live rider. The consequence is structural — **an obligation stated only in prose is invisible to every tool by construction**, and the only fix is to give it a field.

### B2.3 — Discovered while fixing: the documented sentinel invocation throws

```bash
python -m ops.sentinel.scan --asof 2026-08-08
# Executed 2026-08-05: ModuleNotFoundError: No module named 'sentinel'
PYTHONPATH=ops python -m sentinel --help
# Executed: usage: sentinel [-h] [--asof ASOF] [--horizon-days ...]      <- canonical form, matches Makefile:106
```

⚠ **The broken form's only publication site was the round-1 artifact's own B2 prescription.** A tree-wide search at HEAD returns **zero** live occurrences of `python -m ops.sentinel.scan`; the canonical `PYTHONPATH=ops python -m sentinel` appears at `Makefile:106`, `STATE.md:259` and in the 2026-06-23 sentinel plan/design specs. So the audit recommended replacing an under-reaching command with **a command that does not run** — caught only because the fix was executed rather than filed. The gate-estate reading of this (a scanner whose *published* invocation throws binds only for a reader who already knows the undocumented form) is filed **meta** at [`01-diagnostics.md`](01-diagnostics.md) `[R2]`; it is not re-adjudicated here.

### B2.4 — What was actually done · `a818b3f`

*(commit title: `fix(state): B2 — retire the under-reaching 08-08 rider-enumeration command`)*

| `STATE.md` anchor | Change |
|---|---|
| Queue row 2 | *"**~31 ADRs** name 2026-08-08 as their `Trigger check schedule`"* → *"**36 ADRs** carry a field-form `Trigger check schedule` naming 2026-08-08 — **plus ~10 more whose duty is prose-only and which NO pattern reaches**"*, pointing at the hand-check list |
| 2026-08-08 section, fenced command | `rg -l 'Trigger check schedule.*2026-08-08' docs/adr/` **retired**; replaced with `PYTHONPATH=ops python -m sentinel --asof 2026-08-08` and a `# canonical; see Makefile 'sentinel' target` note |
| same, immediately below | ⚠ block recording **33 vs 36** and *why* the one-liner missed (single-line, single-spelling: no `**Check schedule:**` variant, no wrapped continuation lines), **plus a warning that the sentinel WRITES** a run block to `docs/notes/sentinel/queue.md` — revert it if you are only counting |
| same, new ⚠⚠ block | The third class named and enumerated: 53 mention / 36 field-form / **17 prose-only residue**, with `ops/sentinel/scan.py:147` cited for *why* the regex excludes prose. **A 10-row hand-check table** with each file's prose form of the obligation quoted — `P1`–`P5` first, flagged as hard-core, then the params-toml ADR, the C2 relock, the test-values relock, the allocation refresh, and the FXIFY timeout ADR (marked *"⚠ verify liveness; the FXIFY venue is retired"*) |
| same | The non-obligation mentions named explicitly (withdrawn 08-02 ADR, ORB re-park, substrate retirement, two BluSky ADRs, iterate-closure) with **"Do not count these as riders."** |
| same | The **preferred durable fix** recorded as text: additive `**Trigger check schedule:** 2026-08-08 quarterly` on `P1`–`P5` + the params-toml ADR, annotated *"field added 2026-08-05; restates existing §6 prose verbatim — no change to the obligation"*, **after which the sentinel reaches them and this table can be deleted** |
| same | **P4 booked `standing-unfalsifiable`, not a rollover** — it delegates to a HOLD whose own §4 banner reads *"NEITHER LIMB CAN FIRE TODAY"* and whose quarterly schedule was struck 2026-08-03 (discharges round-1 `FU-9`) |

**Untouched, per the constraint:** no §2 decision text, no §4 falsifier logic, no `[RATIFY]` line, and no ADR file at all — the entire fix is one root-doc board.

### B2.5 — What remains open — residue

| # | Item | Standing |
|---|---|---|
| **R-B2a** | **The durable fix is specified but NOT executed.** Adding `**Trigger check schedule:** 2026-08-08 quarterly` to `2026-07-03-hardcore-p1…` through `…-p5…` and `2026-08-03-params-toml-gate-retirement.md` is **additive metadata on five hard-core integrity ADRs** — that is a governance act, not an editorial one, and it **needs operator ratification** before it lands. Until it does, the hand-check table in `STATE.md` is load-bearing: it is the only thing standing between the 08-08 quarterly and silently skipping five hard-core gates. **The exact edit is frozen in `STATE.md`; nothing else is owed to specify it.** |
| **R-B2b** | **The hand-check table drifts, and has already drifted — by design, which is the argument for R-B2a.** In the three commits since the fix, `2026-08-05-strategy-venue-binding-axis.md` landed **with** a field-form trigger (L197 — correctly reached, no action), and the B1 fix below added an `2026-08-08` **prose** mention to the GO ADR's Addendum (L336), taking the prose-only residue **17 → 18**. That one is a *pointer to F2*, which is already boarded, so it belongs in the "do not count these as riders" bucket and **not** on the hand-check list. **Action: none today** — recorded so the next reader who re-measures and gets 34/55/18 instead of 33/53/17 does not conclude the fix regressed. The board's own instruction already covers this: *"Enumerate the riders; do not trust the number — it moves as ADRs land and retire."* |

---

<a id="b1"></a>

## B1 — the GO ADR carried no reader-intercept of the de-scope · FIXED `ae5ffe7`

> **Class:** orphaned-scope · **Verdict as filed:** `KEEP-CORRECTED`.

### B1.1 — What was claimed (round 1 §5.1, verbatim from the Action cell)

> Add `**Superseded-in-part-by:** 2026-08-04-tradeify-venue-descope-eval-included.md — **DEPLOYMENT LIMB ONLY**` … **plus the reciprocal `Supersedes … in part` on the 08-04 ADR header**, moving it out of `Related` so `check_adr_graph` A2 reciprocity is satisfied. Then a dated Addendum 2026-08-04 recording what §2 no longer authorizes and what stands … Mirror the in-part marker on `RUNBOOK.md` L3's Authority line. **§2, §4, §5 and all five prior addenda stay byte-intact.** Run `python scripts/check_adr_graph.py` in the same commit — both header edits must land together or the gate hard-fails.

### B1.2 — What was verified

**Executed at `e031225` (round-1 hook H1), output as printed:**

```bash
rg -c '2026-08-04|de-scope|descope' docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
# Executed: no output, exit 1 — ZERO matches.
rg -n '^\*\*(Status|Supersedes|Superseded-by):' docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
# L3  "**Status:** Accepted (operator executive decision, recorded)"
# L4  "**Superseded-by:** none"
```

The ADR that authorized building the rail and registering the Tradeify account read as an **unqualified `Accepted` deployment GO** four days after its deployment limb was spent — while `RUNBOOK.md` L3 named it, by that word, as *"Authority"*. A reader consulting the canonical artifact for *"what was authorized?"* got the pre-08-04 answer with nothing to intercept it.

### B1.3 — What was actually done · `ae5ffe7`

*(commit title: `fix(adr): B1 — reciprocal supersession edges for the Tradeify de-scope`)*

| File · anchor | Change |
|---|---|
| `docs/adr/2026-07-17-…-go.md` header | Third `**Superseded-in-part-by:**` line added — `2026-08-04-tradeify-venue-descope-eval-included.md` — **DEPLOYMENT LIMB ONLY**, spelling out that §2's authorization to *deploy* is spent while build, registration, attended-only posture, $700 ceiling and arm gate **stand** |
| `docs/adr/2026-08-04-…descope….md` header | `**Supersedes:** none` → the GO ADR *"in part — the **deployment limb only**"*, with the same standing clause; **and the GO ADR removed from `Related`** — a loose pointer became a formal graph edge |
| `docs/adr/2026-07-17-…-go.md` body | **Addendum 2026-08-04** appended: a ⚠ reader-intercept (*"this ADR is no longer authorization to deploy anything"*), a **what §2 no longer authorizes** list, a **what stands, byte-untouched** list (rail build, registered account, attended-only, $700/$208, per-session arm GO, the `dry_run=false` arm gate, and the lifecycle axis at `AUTHORIZED @ 1.00×` — *"venue-fit is not decay"*), and the scope limit that Tradeify-shaped **research** is expressly not barred |
| `docs/notes/rail_build/RUNBOOK.md` L4 | Mirror intercept directly under the Authority line: *"That authority is SUPERSEDED IN PART (2026-08-04) — its DEPLOYMENT limb only … **Do not read any step here as authorization to arm or deploy.**"* |
| `docs/adr/INDEX.md` | Regenerated; the de-scope row's `Supersedes` cell now carries the in-part edge |

⚠ **Why both header edits had to be one commit.** `check_adr_graph`'s **A2** check enforces reciprocity: a `Supersedes … in part` with no matching `Superseded-in-part-by` (or the reverse) is a **hard fail**, so splitting the two edits across commits leaves the tree red in between and the first commit cannot pass the gate. Verified in the same commit and again at HEAD: `check_adr_graph: OK (enabled=['A1','A2','A3','A4','A6'])`. The GO ADR went from **0 → 7** mentions of the de-scope.

**Untouched, per Trap #12:** §2, §4, §5 and all five prior addenda are byte-intact. **The Addendum is the intercept, not a revision** — it says so on its own face.

### B1.4 — The misreading the Addendum corrected — worth pinning on its own

The Addendum records one correction that is not a supersession edge and is easy to lose in the commit:

> B7-REFIRE Stage 1 … stays owed, and is undischargeable *at this venue* while no strategy is deployed to emit the signal. ⚠ Note precisely what that is **not**: M1 item 5 is a `dry_run` strategy signal at non-zero size, *"unarmed by design"*, which routes no order — so the blocker is **the absence of a deployed strategy**, not a standing rule making M1 unresolvable. Deploying any qualifying strategy makes it dischargeable again.

**Why this matters beyond B1.** The circulating reading was that M1 had become permanently unresolvable — i.e. that a *rule* had closed the path. It had not. M1 §4 item 5 asks for a first real TV strategy entry at **non-zero size under `dry_run`**; it is a signal-capture requirement, unarmed by construction, routing nothing to the broker. What is missing is an emitter. That distinction is load-bearing in exactly one live place: under the **FU-1 ruling** (`551d5c5`) the *primary* path to covering the eval's activity week is **deploying a Tradeify-shaped strategy before 2026-08-07** — and if that path fires, B7-REFIRE Stage 1 becomes dischargeable at this venue. A reading that treats it as barred by rule would have declined to notice.

### B1.5 — What remains open — residue

| # | Item | Standing |
|---|---|---|
| **R-B1a** | **The mirror list was one site short.** `deploy/c1_rail/README.md` **L5** makes the same Authority-shaped claim the RUNBOOK line did — *"**Nothing here arms trading.** `dry_run` stays `true` … until the GO ADR's B6 dry-fire passes"* — and received **no** intercept. **B6 passed 2026-07-20**, so by the clause's own terms its restraint has already lapsed, and the file names neither of the two conditions actually holding the rail disarmed (the M1 arm interlock, the de-scope). The whole `deploy/` tree was swept by no round-1 domain; round 2 swept it and files this at MISLEADING alongside the arming recipe at L78. **Not re-opened here** — recorded so that whoever remediates `deploy/c1_rail/README.md` knows the correct intercept text already exists at `RUNBOOK.md` L4 and should be mirrored, not re-derived. |
| **R-B1b** | **`STATE.md` L43 still over-reaches, and it is the sentence that generated the misreading.** *"**B7-REFIRE Stage 1 stays permanently owed and permanently undischargeable at this venue.**"* — bolded, in the queue banner. Round 1 named this as one of its **two calibration exemplars** (the observations that triggered the audit) and **deliberately excluded it from the findings set**, so it carries no finding ID and no row anywhere. It is still standing at HEAD, and it now sits **immediately above** the board's own row 0, which contemplates deploying a strategy at this venue by Friday. **Action:** replace *"permanently … permanently"* with the contingency, using the Addendum's wording as the source — *"owed, and undischargeable at this venue **while no strategy is deployed to emit the signal**; M1 item 5 is a `dry_run` signal, unarmed by design, routing no order."* ⚠ The identical phrase in the de-scope ADR **§6** is frozen decision text and is **not** edited; STATE.md is the living board and is where the correction lands. |

---

<a id="round2"></a>

## Round 2 — zero new BLOCKERs, read carefully

**The plain fact.** Round 2 swept seven surfaces round 1 never reached — `.claude/`, `.cursor/`, `deploy/`, root docs + build files, `scripts/`, the `lab/analysis` RESULTS corpus, and specs/plans — raised **124** findings, confirmed **110**, and rated **0 BLOCKER / 50 MISLEADING / 60 COSMETIC**. **Not one new BLOCKER.** Every BLOCKER either round produced is in this file, and all three are fixed.

**What that is genuine evidence for.** Round 1 aimed at the artifacts that *authorize* things — ADRs, specs, the forward board — and that is where consequence lives. B1 was a spent authorization reading as live; B2 an enumeration feeding a gate; B3 a normative sizing law an implementer is told to follow verbatim. Each is a document that, followed, causes a wrong **act**. The round-2 surfaces are mostly documents that, followed, cause a wrong **belief** first, and an act only via an actor who then hits a guard. Round 1 picked the right target on the first pass, and the round-2 severity profile is consistent with that.

**What it is emphatically NOT evidence for, and this is the load-bearing half.** It does **not** mean the agent-facing surfaces are safe. **71 of round 2's 110 confirmed findings are agent-facing** — consumed by an agent or an operator mid-task, where a stale instruction produces an **action** rather than merely misleading a reader — concentrated in `.claude` (23), `docs` (19), `scripts` (16), `deploy` (8) and `.cursor` (4). The reason none reached BLOCKER is specific, and it is a reason that can expire:

> **The refutation pass repeatedly narrowed agent-facing findings from BLOCKER to MISLEADING because an independent guard catches the actor.** `deploy/c1_rail/README.md`'s arming recipe ends *"Only then flip `dry_run: false`"* with neither current gate in view — and drops to MISLEADING because `ops/c1_rail/c1_rail_arm.py::m1_acceptance_reason` refuses the flip while M1 is not `RESOLVED`. Two skills assert a **two-condition** arming gate — and drop because the same interlock holds. **R-B3d** states the whole-cap law on the auto-loading skill surface — and drops because the production host **HALTs** on a missing per-leg allocation instead of falling back.
>
> **A guard that catches you is not the same as an instruction that is correct.** Every one of those downgrades is a bet on a *second* artifact staying correct — in a repo whose entire audited failure class is second artifacts going stale because nothing forced a re-read. Note also that three of the guards above are **the same guard**. The severity ratings are right; the comfort is not.

**The counting rule, so no one adds these up wrongly.** Round 1's §5.10 rated **nine** completeness-critic candidates BLOCKER, several on exactly the `.claude/` and `deploy/` files round 2 then swept. Those nine were **explicitly not added** to round 1's three, because they had not passed a refutation pass. Round 2 *is* that pass, and it returned **zero** — they were verified, adjudicated, and came back smaller, which is the machinery working as designed. **Anyone quoting a combined BLOCKER count above three is quoting a number neither round produced.**

**The honest asymmetry, and its actual bearing here.** Round 2 refuted **9.7%** of what it raised against round 1's **21.4%**, and nothing in the data distinguishes *"these surfaces were never swept, so they are genuinely rot-heavy"* from *"round 2's refutation pass was less aggressive"* (the README states both readings once, plainly). **That has no bearing on this file** — its three rows are all round-1, all hook-verified, all fixed. It bears only on how firmly to read the zero, and it cuts the reassuring way: **a less aggressive refutation pass yields MORE surviving BLOCKERs, not fewer.** The zero is not an artifact of leniency in the direction that would matter.

---

## Verification — every hook re-executed at HEAD

Round 1 recorded its hooks at anchor `e031225`, **before** any fix. Each is re-run below **at HEAD** (post-`0af62ec`), output as printed. A hook asserting a fix is worth only what its last execution is worth.

```bash
# H1 / B1 — the GO ADR now carries the intercept.  Was: no output, exit 1 (ZERO matches).
rg -c '2026-08-04|de-scope|descope' docs/adr/2026-07-17-c1-rail-build-account-registration-go.md
# 7
python scripts/check_adr_graph.py
# check_adr_graph: OK (enabled=['A1', 'A2', 'A3', 'A4', 'A6'])
#   -> A2 reciprocity satisfied: the two header edits are consistent at HEAD.

# H3 / B3 — the normative law now divides by the per-leg share, in BOTH specs.
rg -n 'cap_firm / \(1|cap_alloc\[leg\]' docs/spec/c1_watch_realization_multiplier_layer.md
# L41  "denominator is **`cap_alloc[leg]`** (this leg's share), **never `cap_firm`** (the whole account)."
# L52  "qty_base  = min( qty_base, floor( cap_alloc[leg] / (1 + pyr_pct/100) ) )"
#   -> ZERO occurrences of the `cap_firm / (1 + ...)` denominator form remain.
rg -n 'reserve_cap  = floor' docs/spec/c1_nt8_sizing_host_impl.md
# L71  "reserve_cap  = floor(cap_alloc / (1 + pyr_pct / 100))   # THIS LEG'S allocated share — HALT if absent (§5);"

# H2 / B2 — the counts moved, exactly as the board's own instruction predicted.
rg -l 'Trigger check schedule.*2026-08-08' docs/adr/ | wc -l    # the RETIRED one-liner
# 34        (was 33 at e031225 — one ADR landed carrying the field form)
rg -l '2026-08-08' docs/adr/ | wc -l                            # any mention, incl. INDEX.md
# 56        (= 55 ADRs + INDEX.md; was 54 at e031225 counted the same way)

# B2.3 — the documented invocation still throws; the canonical one runs.
python -m ops.sentinel.scan --asof 2026-08-08
# ModuleNotFoundError: No module named 'sentinel'
PYTHONPATH=ops python -m sentinel --help
# usage: sentinel [-h] [--asof ASOF] [--horizon-days HORIZON_DAYS] ...

# R-B3c — the frozen baseline omits cap_alloc; production HALTs rather than falling back.
python -c "import json;d=json.load(open('docs/notes/substrate_retirement_baselines/baseline_c1_lifecycle_ddp.json'));c=d['c1_sizing_constants'];print('cap_firm' in c, any('cap_alloc' in l for l in c['leg_map'].values()))"
# True False

# R-B3b — the frozen MNQ LOCK record still states the whole-cap form (impeach, do not edit).
rg -n 'RESERVE at cap 80|microCap' core/strategies/_archive/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md
# L15  "`microCap` default **80** (Tradeify Select / MFFU Rapid 100K)."
# L21  "RESERVE at cap 80 -> base max `floor(80/11)=7`."

# R-B3d — the concept-scoped re-run of the agent-surface sweep (see the correction note in B3.4).
rg -n --no-ignore 'account_cap|micro_contract_cap|RESERVE cap' .claude/ .cursor/ deploy/
# .claude/skills/prop-firm-challenge/SKILL.md:189  "capped by the tier's `micro_contract_cap`"
# .claude/skills/prop-firm-challenge/SKILL.md:191  "**RESERVE cap rule** ... floor(account_cap / (1 + pyramid_pct))"
#   -> .cursor/ and deploy/ return nothing on either the token or the concept.
```

**One hook is deliberately NOT re-run, and the omission is disclosed rather than papered over.** `PYTHONPATH=ops python -m sentinel --asof 2026-08-08` **writes** a run block to `docs/notes/sentinel/queue.md` — `STATE.md`'s own corrected text carries that warning — and re-running it to refresh a count in an audit note would plant a spurious sentinel run in the record three days before the gate it feeds. The field-form figure at HEAD is therefore stated in the B2.2 table as **derived** (55 ADR mentions − 18 prose-only residue = 37), **not measured**, and is labelled as such. Re-measure it **at** the 08-08 gate, where the write is the point.

**Standing, restated so this file closes cleanly.** B1, B2 and B3 are **CLOSED** — verified, fixed, committed, re-verified at HEAD. The **eight residue items** are open, each naming its own next action; none is a re-opening, and none is at BLOCKER severity. **The failure class is not closed.** Three repaired BLOCKERs against **250 confirmed findings** is a repaired *edge*, not a repaired estate — the remaining **247** live in the other five sections, and every one of them is still a recommendation pending operator ruling.

---
