# ADR 2026-08-05 — `core/firm_rules.py`: BluSky's inactivity limit is unsourced; contain it rather than trust it

**Status:** `Accepted` — operator directive this session (2026-08-05): *"fix the BluSky inactivity field encoding in firm_rules.py"*, given after being shown the measured consequence and the provenance finding it rests on.
**Decision date:** 2026-08-05
**Authors:** Joshua (directive) + Claude Code (measurement + draft + apply)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-08-05b-blusky-inactivity-rule-sourced.md`](2026-08-05b-blusky-inactivity-rule-sourced.md) in part — **§4 T1 FIRED same day.** BluSky's activity rule was sourced (Terms of Use art. 11490284 §3.3, trade-based per art. 12434442): the rule is real, binds evaluation accounts, and its faithful engine encoding is **22 idle business days**, not the 30 this ADR contained. The containment was correct for what was known and is **discharged, not overturned** — its guard machinery is retained and still gates the next unsourced tier.
**Retain-until:** superseded by an ADR recording BluSky's actual published activity rule (§4 T1), or by a firm-rules change that retires the BluSky tiers
**Related:** [`2026-08-04-firm-rules-eval-lock-fix-applied.md`](2026-08-04-firm-rules-eval-lock-fix-applied.md) (same file, same defect *class* — a field whose recorded value did not match the phase it models; **different field**, and that ADR's §5 forbidden move against widening the `dd_lock_offset_usd` fix to BluSky is respected, see §5 below) · measurement [`lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md`](../../lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md) §1 · [`2026-08-04-tradeify-venue-descope-eval-included.md`](2026-08-04-tradeify-venue-descope-eval-included.md) §7 F3 (the fork whose verdict this field silently decides)
**Layer:** production config correctness (provenance defect) + one engine-plumbing guard in `core/mc/preflight.py`. **No `dd_protection` constant, allocation, Pine file, lifecycle state, or frozen gate threshold is touched. No measured number changes.**

---

## §0 — Rule 0 reads (production source, verified 2026-08-05)

| Source | Anchor | What it grounds |
|---|---|---|
| `core/firm_rules.py` `BluSky_Premium_{50K,100K}` rows + block comment L430–448 | worktree, this session | Both tiers carried `inactivity_max_idle_days: 30` annotated verbatim *"30-day eval subscription renewal window"* — a billing cycle. The block's sourcing paragraph cites articles 12434059 / 12434069 + the automation FAQ for drawdown, consistency, cost and auto-liquidation, and is **silent on inactivity**. |
| Full-tree search for a BluSky activity rule (`rg --no-ignore`, incl. `lab/archive/` + `docs/ltm/`) | this session | **No BluSky activity rule exists anywhere in the repo.** The `30` is the only encoding, and its own comment says what it really is. |
| `core/firm_rules.py` Bulenox block L80–88 | worktree | Sibling precedent: Bulenox's inactivity *"was a carried-over FXIFY placeholder through 2026-07-05; corrected 2026-07-06 (residual track R2) to Bulenox's actual rule (≥1 trade per 5 trading days)"*. Placeholders in this field have been corrected before — **when a source existed.** |
| `core/firm_rules.py` `Tradeify_Select_100K` | worktree | Its `5` is a sourced venue fact (art. 10468318 + 12268494: idle week → warning → permanent deletion), attested as *"a VENUE FACT"* by the 2026-08-04 de-scope ADR §0. The field therefore mixes sourced rules and an unsourced billing window **across tiers, under one name**. |
| `core/mc/simulation.py:171-178` | verified this session | The consumer: `consecutive_idle >= inactivity_limit` → `return "bust_inactivity"`. A rolling consecutive-idle **ABSORBING** barrier — terminal, not a warning. |
| `core/mc/preflight.py:124` (pre-edit) | verified this session | `"inactivity_limit": (INACTIVITY_OFF if inactivity_off else f["inactivity_max_idle_days"])` — the value is threaded straight through with no provenance check. Default `inactivity_off=True`, so the field is read **only** by runs that explicitly opt in. |
| `lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md` §1, §4.2 | committed this session, PR #647 | The measurement. Tradeify control pin reproduced at Δ0.003pp before any F3 cell was read, so the delta below sits on a verified baseline. |

**Gitignore pre-flight.** `**/*.pine` is ignored; no Pine source is read or cited. No vendor CSV was re-exported; the F3 panel is the committed 2026-07-23 `daily_panel.csv`, unchanged.

---

## §1 — Context

Fork **F3** ([`ADR 2026-08-04`](2026-08-04-tradeify-venue-descope-eval-included.md) §7) required scoring Bulenox / MFFU / BluSky against the locked Striker book's cadence axis. The measurement landed 2026-08-05 and produced a clean-looking ranking: at their encoded idle limits, Bulenox shows 90.85–97.54% unmitigated inactivity death, MFFU 91.77–97.54%, and **BluSky 0.52–1.40%**.

That ranking is carried entirely by one integer. `firm_kwargs` for `Bulenox_100K` and `BluSky_Premium_100K` are **identical apart from `inactivity_limit`** — same `dd_type: trailing`, same −0.03 rope, same $106,000 target, same `min_trading_days: 0` — verified directly and confirmed independently by their inactivity-OFF arms measuring identically (69.13% pass / 30.87% bust / median 52 days). So the counterfactual needs no simulation: **at Bulenox's sourced 5, BluSky's numbers are Bulenox's numbers** — 90.85 / 97.50 / 91.81 / 97.54%.

And the `30` is not an activity rule. Its own inline comment, written at 2026-07-12 sourcing time, says it is the *eval subscription renewal window*: a billing cycle governing whether you keep paying, not a trading-cadence barrier that deletes an account. The engine nonetheless reads the field as an absorbing terminal barrier.

The result is a field that reports an assumption in the grammar of a measurement, on the one axis that a live fork turns on. Nothing published today is wrong — every prior figure ran inactivity-OFF, the documented default — but the next consumer to switch inactivity ON for BluSky gets a two-orders-of-magnitude-optimistic number with no signal that it rests on a billing window. That is the `lesson_driver_layer_fix_leaves_kernel_default_stale` shape, and the 2026-08-04 ADR §3 named exactly this failure mode for its own defect: *"any direct or naive invocation… silently inherits the wrong, optimistic geometry with no signal that a patch is expected."*

**Decision driver (one sentence):** the value cannot be corrected (no source exists to correct it *to*), so the only honest options are to keep it and make its unsourced status mechanically un-ignorable, or to delete it and break every consumer — and F3's verdict is due 2026-08-08.

---

## §2 — Decision

**1. Both `BluSky_Premium_*` tiers are marked unsourced on this field.** `inactivity_max_idle_days: 30` is **retained** (deleting it would break consumers and destroy a reproducible published cell) and gains `inactivity_rule_sourced: False`, plus an `OPEN DEFECT` block naming the billing-window provenance, the measured consequence, the containment, and the actual fix.

**2. `core/mc/preflight.py::firm_kwargs` refuses to silently use an unsourced limit.** A new keyword `allow_unsourced_inactivity: bool = False`; when a caller requests `inactivity_off=False` on a tier carrying `inactivity_rule_sourced: False` without it, `firm_kwargs` raises `ValueError` naming the tier, the value, why it is not a measurement, and both routes forward. **Absent the key, a tier is treated as sourced** — matching every tier whose value cites a venue article, so no other row changes behaviour.

**3. No measured number changes, and no verdict moves.** Inactivity-OFF — the default, and every published figure in the repo — never consults the flag. The F3 study declares the acknowledgement explicitly and reproduces its BluSky cell exactly (§8).

**Effective:** immediately upon acceptance.
**Scope:** `core/firm_rules.py` (2 tiers), `core/mc/preflight.py` (1 guard), `tests/core/test_mc_preflight.py` (6 tests), and the F3 harness's explicit acknowledgement. No `core/mc/simulation.py`, `core/dd_protection.py`, `core/lifecycle.py`, allocation, or Pine file is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — fix the comment only, leave the mechanics** | A comment does not stop `firm_kwargs` returning 30. The defect is that the wrong number is *usable by default*, and the F3 fork it decides is dated 2026-08-08. This is the alternative the RESULTS artifact already rejected by naming the field a live mis-encoding. |
| **Replace `30` with Bulenox's sourced `5`** | Fabricates a venue fact. BluSky publishes no such rule; adopting a sibling's rule because it is conveniently conservative is the mirror image of the current defect, and it would silently flip F3's answer from "undecidable" to "no successor" on invented evidence. |
| **Set the value to `None`** | Rejected for the same reason the 2026-08-04 ADR rejected `None` for `dd_lock_offset_usd`: it fails, but incoherently. `consecutive_idle >= None` raises a bare `TypeError` deep inside `simulate_path` with no statement of what is wrong or what to do. The guard raises at the boundary with an actionable message instead. |
| **Delete the key entirely** | Also fails loudly (`KeyError` at `preflight.py:124`), but destroys the reproducibility of a just-published cell and breaks display code that reads the field for logging. Loses the information that 30 is *something* — the renewal window — which the next person sourcing the real rule will want. |
| **Make `firm_kwargs` silently map unsourced → `INACTIVITY_OFF`** | The most dangerous option considered: it converts an optimistic number (0.52%) into a maximally optimistic one (0.00%) while looking like a safety measure. Explicitly recorded here so it is not re-proposed as "the conservative default". |
| **Source BluSky's real rule now and encode it** | The correct terminal fix, and §4 T1 is written to fire when it happens. Not done here because it requires reading BluSky's live help centre — an external-source verification pass with its own provenance discipline, not a code change. Sequencing it after containment means the 08-08 fork is not blocked on an unscheduled sourcing task. |
| **Widen the flag to MFFU's `5`** | MFFU's row annotates itself *"≥1 trade/week; not modeled as absorbing barrier"* — a real tension between annotation and modeling, flagged in RESULTS §1. But MFFU's rule **is** sourced (article 13286542 family); the defect there is a modeling-faithfulness question, not a provenance one, and it is a different decision. Named as a residual (§6), not bundled. |

---

## §4 — Falsifier (what would revert or amend this)

**H (what this ADR asserts, binary):** *`BluSky_Premium_*`'s `inactivity_max_idle_days: 30` is not a published activity rule, and with `inactivity_rule_sourced: False` in place no consumer can obtain a BluSky inactivity figure without explicitly declaring it an assumption — while every inactivity-OFF path, and every published number in the repo, is bit-for-bit unchanged.*

**H is FALSIFIED — and this ADR is amended or superseded — if any trigger below fires.**

| # | Trigger | Threshold | Action |
|---|---|---|---|
| T1 | BluSky publishes (or is found to publish) an actual evaluation-phase activity rule | primary source, article-cited | Encode the real value, set `inactivity_rule_sourced: True`, supersede this ADR, and **re-run F3's BluSky arms** — if the rule is 5-day-class, F3's answer becomes "no successor survives the unmitigated barrier" |
| T2 | A tier is added to `FIRM_RULES` whose `inactivity_max_idle_days` is not traceable to a published activity rule and which omits the flag | any new tier without sourced-or-flagged provenance | Block at engine pre-flight; §5's forbidden moves apply to new tiers too |
| T3 | The guard is found to be bypassable, vacuous, or removed | `test_unsourced_inactivity_on_raises_without_ack` passes while the guard is absent, or any consumer reads `inactivity_max_idle_days` directly to build a barrier without going through `firm_kwargs` | Repair the guard; treat any figure produced in the interim as unlabelled |
| T4 | An inactivity-ON BluSky figure appears in a published artifact without the assumption stated | any RESULTS/ADR/brief quoting a BluSky inactivity number as a measurement | Banner the artifact; the acknowledgement flag exists precisely so this is greppable |

**Not admissible as a revert route:** deleting `inactivity_rule_sourced` to make a run proceed, or substituting a sibling firm's value for BluSky's. Both re-introduce the exact defect this ADR contains.

**Revert action:** author a superseding ADR. Never edit this ADR's §2 in place.

**Trigger check schedule:** T1 at the next 90-day venue-fact re-verify (next due ~2026-10-20, standing cadence) **and** as the named first limb of F3's resolution (RESULTS §6 item 1). T2 on any new `FIRM_RULES` tier addition. T3/T4 at each programme audit.

---

## §5 — Forbidden moves (under this ADR)

- **Treating containment as sourcing.** This ADR does not establish what BluSky's activity rule is. It establishes that we do not know. A BluSky inactivity figure remains an assumption with a flag on it, not a measurement.
- **Reading this as electing, or excluding, a successor venue.** F3 is untouched and remains operator-owned at 2026-08-08. This ADR makes F3's evidence honest; it does not rule it.
- **Substituting a sibling firm's value** (Bulenox's 5, Tradeify's 5) for BluSky's, in code or in prose.
- **Deleting or defaulting away the flag** to make a harness run. The acknowledgement keyword exists for that need and leaves a greppable trace.
- **Widening this to the `dd_lock_offset_usd` fix's territory.** The 2026-08-04 ADR §5 forbids widening *that* fix to Bulenox/BluSky on the grounds those tiers are `dd_type: "trailing"` and structurally never read that field. That remains true and is **not** disturbed here: this ADR touches `inactivity_max_idle_days` only, adds no lock field, and changes no `dd_type`. Its §10 audit hook #2 (seven `"dd_type": "trailing"` rows) stays green.
- **Loosening any §4 trigger without a superseding ADR** (Known Trap #12).

---

## §6 — Consequences

**Positive:**
- The one field that decides F3's cross-venue verdict can no longer report a billing window as a cadence measurement. The failure is now at the boundary, with an actionable message, instead of two orders of magnitude deep in a results table.
- The provenance asymmetry the field was hiding — sourced venue facts on three tiers, a subscription window on a fourth — is now visible in the data, not only in a lab RESULTS section.
- F3 keeps its evidence and its reproducibility: the BluSky cell still runs and still returns exactly what it returned, for callers willing to say why.

**Negative consequences (real, not theatrical):**
- `firm_kwargs` grows a keyword and a conditional — a small permanent complexity cost on a module whose docstring advertises correctness-by-construction. Accepted because the alternative is correctness-by-tribal-knowledge on a field that has already produced one near-miss.
- The F3 harness now carries an explicit acknowledgement, so its BluSky arms are no longer runnable by a naive invocation. That is the intended behaviour, but it does mean a reproduction attempt must read the comment first.
- **This ADR does not make BluSky's cadence knowable.** It converts a confident wrong-shaped answer into an honest absence, which is progress in rigour and a regression in apparent decisiveness eight days before an operator fork.

**Risks:**
- **MFFU's annotation tension remains live and unfixed.** Its row says *"not modeled as absorbing barrier"* while every published run models it as exactly that. The rule is sourced, so this ADR's flag is the wrong instrument, but the gap is real and now recorded in two places (RESULTS §1, here). Direction of the error is unmeasured.
- **A future engineer could pass `allow_unsourced_inactivity=True` reflexively** to clear the exception, reproducing the defect with extra ceremony. Mitigated by the raise text naming the honest route first (source the rule), by §5, and by T4 making the trace greppable — but not eliminated.

**Downstream artifacts needing update (this commit):**
- [`core/firm_rules.py`](../../core/firm_rules.py) — OPEN DEFECT block + two `inactivity_rule_sourced: False` flags.
- [`core/mc/preflight.py`](../../core/mc/preflight.py) — `allow_unsourced_inactivity` keyword + guard + docstring.
- [`tests/core/test_mc_preflight.py`](../../tests/core/test_mc_preflight.py) — six tests, incl. the flag-in-place pin and the Bulenox≡BluSky identity that makes the flag load-bearing.
- [`lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_f3_cadence.py`](../../lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/run_f3_cadence.py) — explicit acknowledgement.
- [`docs/adr/INDEX.md`](INDEX.md) — regenerate. [`docs/SESSIONS.md`](../SESSIONS.md) — session entry.

---

## §7 — Implementation plan

- **Phase 0** — §0 anchors verified at implementation time. **DONE 2026-08-05.**
- **Phase 1** — apply the flags + OPEN DEFECT block in `core/firm_rules.py`. **DONE.**
- **Phase 2** — add the `firm_kwargs` guard + docstring. **DONE.**
- **Phase 3** — tests, including an adversarial check that the guard actually fires rather than passing vacuously (`lesson_discipline_guards_need_adversarial_tests`). **DONE**, §8.
- **Phase 4** — post-fix native reproduction of the published BluSky cell with the acknowledgement, zero monkey-patch (T3/T4 evidence). **DONE**, §8.
- **Phase 5** — full suite green; `check_adr_graph` / `check_status_consistency` / `check_falsifier_reachability` green; INDEX regenerated; SESSIONS entry.

---

## §8 — Verification result

**Guard behaviour (all four paths, exercised directly):**

```
BluSky ON, no ack   -> ValueError: 'BluSky_Premium_100K' has inactivity_rule_sourced=False ...
BluSky ON, with ack -> inactivity_limit = 30
BluSky OFF          -> inactivity_limit = 1501   (disabled sentinel, no raise)
Bulenox ON, no ack  -> inactivity_limit = 5      (sourced tier unaffected)
```

The guard is **not vacuous**: the no-ack path was executed and observed to raise, not merely asserted against.

**Post-fix native reproduction — zero runtime override, acknowledgement passed explicitly:**

```
[source] inactivity_limit = 30   sourced_flag = False
post-fix native: INACT 0.52% vs published 0.52%  -> MATCH
                 pass  68.77% vs published 68.77% -> MATCH
```

The published BluSky cell reproduces **exactly** through `firm_kwargs` → `run_seed`. The fix changes *who may obtain* the number, not the number. **T3 and T4 do not fire.**

**Regression check.** `tests/core/test_mc_preflight.py`: 32 passed. Full-suite result recorded in the session entry; no test anywhere asserted against BluSky's inactivity value (the two existing inactivity-ON tests use `Tradeify_Select_100K` and `MFFU_Rapid_100K`, both sourced tiers, both unaffected).

---

## §10 — Audit hooks (runnable)

```bash
# 1. Both BluSky tiers carry the unsourced flag — no hand-revert.
grep -c '"inactivity_rule_sourced": False' core/firm_rules.py
# Expected: exactly 2 (the BluSky_Premium_50K and _100K rows). A third occurrence
# in the OPEN DEFECT prose above them is expected and is not counted by this form.

# 2. The guard exists and is reachable from the public entry point.
grep -n "allow_unsourced_inactivity" core/mc/preflight.py
# Expected: keyword in the signature, the docstring, and the raise condition

# 3. The guard actually fires (adversarial — must raise, not pass).
python -c "import sys;sys.path.insert(0,'core');from mc.preflight import firm_kwargs;firm_kwargs('BluSky_Premium_100K',inactivity_off=False)"
# Expected: ValueError mentioning inactivity_rule_sourced=False

# 4. Sourced tiers are untouched by the guard.
python -c "import sys;sys.path.insert(0,'core');from mc.preflight import firm_kwargs;print(firm_kwargs('Bulenox_100K',inactivity_off=False)['inactivity_limit'])"
# Expected: 5

# 5. The 2026-08-04 ADR's dd_type hook stays green (this ADR changed no dd_type).
grep -c '"dd_type": "trailing"' core/firm_rules.py
# Expected: 7 (5 Bulenox + 2 BluSky), unchanged

# 6. No dd_protection, lifecycle, allocation, or Pine file changed.
git diff --stat HEAD~1 -- core/dd_protection.py core/lifecycle.py core/strategies/
# Expected: empty

# 7. The measurement this ADR rests on states the provenance before its grid.
grep -n "subscription renewal window" lab/analysis/c1/f3_cadence_successor_venues_2026-08-05/RESULTS.md
# Expected: present in §1, ahead of the tables
```

---

## Verification

```bash
python scripts/check_adr_graph.py
python scripts/check_status_consistency.py
python scripts/check_falsifier_reachability.py
python -m pytest tests/core/test_mc_preflight.py -q

# §0 anchors still current
git log -1 --format="%h %cs core/firm_rules.py" -- core/firm_rules.py
git log -1 --format="%h %cs core/mc/preflight.py" -- core/mc/preflight.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-05 | Initial authoring, `Accepted` on operator directive this session. Two `BluSky_Premium_*` rows flagged `inactivity_rule_sourced: False` with an OPEN DEFECT block; `firm_kwargs` gains `allow_unsourced_inactivity` and refuses unsourced inactivity-ON runs; six tests added; F3 harness declares the acknowledgement explicitly. No measured number changes — the published BluSky cell reproduces exactly. MFFU's annotation-vs-modeling tension named as a residual, not bundled. | Joshua (directive) + Claude Code (draft + apply) |
