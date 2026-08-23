# Q-SIZECOMP-1 — verdict pre-registration

**Frozen:** 2026-08-23, before Phase 1 result inspection — the gate criteria below are
transcribed verbatim from `Q-SIZECOMP-1-sizing-composition.md` §6, which was itself
written and pre-lock-checked 2026-08-18, five days before this pre-registration and Phase 1
execution. No criterion here was chosen or adjusted after seeing any `grep`/`sed`/`python`
output.

**Process note (honest disclosure, not a gap-paper — mirrors the Q-GATESTACK-1 precedent):**
the brief's §7/§8 sequencing calls for this pre-registration to be committed, then Phase 1
run, as two separate steps. Under the operator's explicit instruction to open and run this
brief's Phase 1 (2026-08-23), this file and the Phase 1 execution happened inside the same
turn rather than across two — the criteria were already frozen in the brief's own §6 on
2026-08-18, five days before either was read against results, so there was no opportunity
for the *content* of this pre-registration to be shaped by the results. The letter of
"committed before any grep/python call runs under this brief" was not observed as two
distinct turns. Recorded here rather than silently presented as clean two-step sequencing.

---

## Frozen gate (verbatim from §6)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | Limb-A confirms (0 `ops/` hits; `:55` imports `TIER_MULTIPLIER` only) **and** Limb-B confirms (arithmetic exact **and** no 3-way test exists) | `INTEGRATE` — record the rail/CLI composition asymmetry as an evidence-ratified fact and file the missing-test gap against `tests/test_lifecycle.py`; name (do not open) a successor decision packet for the operator on whether/how the rail should compose beta-death before `dry_run` is ever considered. No code change under this brief. |
| `FALSIFIED` | Limb-A **or** Limb-B does not confirm as stated (rail already calls `get_effective_multipliers`/`beta_death_assessment`, **or** the triple-compound arithmetic diverges from `BASE_RISK × 0.40 × 0.25`) | `STOP` — the composition-asymmetry claim as stated is wrong; re-proposal needs a fresh grounding read, not a re-run of the same grep/arithmetic. |
| `AMBIGUOUS-HOLD` | Limb-A confirms but Limb-B's arithmetic does not check out cleanly (a deeper `calculate_protection` defect surfaces), or a grep hit's reachability is ambiguous (dead/test-only code) | `ITERATE` — name (do not open) a successor Q scoped to whichever limb produced the ambiguity; carry forward the confirmed limb's result verbatim. |

## Reject conditions (verbatim from §4)

- **Limb-A false (rail already composes beta) if:** a call to `get_effective_multipliers` or `beta_death_assessment` exists anywhere under `ops/`.
- **Limb-B false (doctrine's own compound math is wrong) if:** the local triple-compound arithmetic check (§7/§10) does not return `BASE_RISK[k] × 0.40 × 0.25` exactly for a DD-triggered + WATCH-1 + beta-death input.
- Overall verdict is `FALSIFIED` if either limb is false as defined above.
- `AMBIGUOUS-HOLD` fires only for the two named degenerate cases above — not for any other kind of surprise (e.g. not for a stale hardcoded example key in the hook itself, which is a hook-authoring defect, not evidence against the composition claim).

**Commitment:** the verdict below will be read mechanically off these rows against the
Phase 1 output — no re-framing after the fact. §6 is not amended to match what the read
returns (brief's own §6 footer, carried forward here verbatim).
