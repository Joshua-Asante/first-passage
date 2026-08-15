# Recommendation — 1H transfer pre-gate: align the price-BASIS axis EQ-handling

**Type:** audit note / design recommendation (operator decision). **Status:** RATIFIED **ALIGN** 2026-06-18 — implemented (`harness_1h.py` `transfer_price_basis_axis` EQ-inclusive + valid-masked join; PREREG-1H §Amendment 2026-06-18b; regression `test_transfer_price_basis_eq_inclusive_counts_disagreements`). **Pre-data, firewall-safe** (no real 1H/1M export exists yet). Authored 2026-06-18 as the PR #198 follow-up #1.

## §0 — Rule-0 reads (production source, verified this session)

All directly readable in-repo (no gitignore citation-chain needed — the load-bearing source is the harness + PREREG, not the Pine):

| Source | Anchor | What it establishes |
|---|---|---|
| `harness_1h.py:575-611` (`_sign_agreement`) | commit `bcf2160` (PR #198) | `restrict_nonzero=False` = raw equality (EQ==EQ counts as agree, EQ-vs-nonzero is a disagree in the denom); `True` = drop every EQ row from num AND denom. |
| `harness_1h.py:636-654` (`transfer_range_lag_axis`) | `bcf2160` | Range-LAG axis (the **fixed** one): `_sign_agreement(zone, zone_gate, restrict_nonzero=False, mask=vg_mask)` — EQ-inclusive + valid&gateValid mask, pinned to Pine `agreeRate`. |
| `harness_1h.py:691-729` (`transfer_price_basis_axis`) | `bcf2160` | Price-BASIS axis (the axis in question): **L707** `_sign_agreement(hz, mz, restrict_nonzero=True)` — drops EQ rows, **no** valid mask. Comment L703-706 scopes the 1H-CRITICAL fix to the range-LAG axis only. |
| `harness_1h.py:732-744` (`transfer_pregate`) | `bcf2160` | REJECT the transfer if **EITHER** axis fails (≥90% agree AND ≤3pp gap, both axes). |
| `PREREG-1H.md:79-88` (Transfer pre-gate E1/H-CASCADE) | RATIFIED 2026-06-18 | Two axes, thresholds ≥90% / ≤3pp; "REJECT … if agreement < 90% OR gap > 3pp on EITHER axis." **L84** defines the price-BASIS axis (1-min close vs 1H close, same [1]-lagged range). The PREREG is **silent on the price-BASIS axis's EQ handling** — the range-LAG axis is EQ-inclusive only because it is pinned to Pine `agreeRate`; the price-BASIS axis has **no Pine counterpart** to pin it. |

## §1 — The symptom (not a fix)

The transfer pre-gate's two axes feed the **same** 90%/3pp threshold but measure "sign-agreement" two different ways: the range-LAG axis counts EQ rows (raw equality, masked), the price-BASIS axis drops them (`restrict_nonzero=True`, unmasked). This asymmetry was introduced deliberately when the 1H-CRITICAL fix was scoped to the range-LAG axis (it had a Pine `agreeRate` to match; the price-BASIS axis did not).

## §2 — Mechanism: the price-BASIS asymmetry is the *same* false-PASS shape, minus the Pine anchor

`restrict_nonzero=True` drops two row classes from the price-BASIS agreement:
- **EQ-vs-nonzero rows** (e.g. 1H reads discount −1, the 1M basis reads EQ 0): these are **genuine transfer failures** — the 1H proxy says "trade," the price-basis the live gate actually reads says "stand down," so the 1M gate would NOT fire where the 1H signal claimed it should. Dropping them **inflates** the agreement %.
- **EQ==EQ rows** (both 0): dropped; under EQ-inclusive they are faithful agreement (both stand down).

The load-bearing item is the first class. The gate's stated purpose (`harness_1h.py:697-698`, 1H-E1) is exactly *"if [the 1M basis] disagrees with the 1H zone the cheap 1H proxy licenses nothing."* Dropping the EQ-vs-nonzero disagreements makes the gate **less conservative** — it biases `agree` **up**, toward CLEARING the transfer, toward **licensing the 1M PD gate**. That is the identical bias direction and the identical H-CASCADE failure the confirmed 1H-CRITICAL finding fixed on the other axis. The only thing that differed was the *faithfulness anchor* (no Pine `agreeRate` here), not the *correctness argument*.

**Steelman for KEEP (both-nonzero):** "measure concordance only among bars where both bases give a directional read." Rejected: a bar where the signal exists on one basis and washes to EQ on the other is precisely the transfer failure the pre-gate exists to catch; excluding it answers a narrower question than the gate asks, and in the non-conservative direction. Boundary-churn near the EQ band producing disagreements is *real* transfer unreliability, correctly counted as disagreement.

## §3 — Recommendation: **ALIGN** (EQ-inclusive + a valid mask)

Mirror the range-LAG fix on the price-BASIS axis: `restrict_nonzero=False`, raw equality, **masked to valid bars**. The mask is **load-bearing** — EQ-inclusive *without* a mask would count warmup `0==0` rows (range undefined) as agreement, re-introducing an inflation in the other direction (the very reason the range-LAG fix added `_valid_gate_valid_mask`).

Implementation (NOT a pure one-liner — it needs the valid mask threaded through the timestamp join):
1. Have `_join_hour_to_minute` (L675-688) also return the `_valid_gate_valid_mask(ex)` value for each joined bar (and require the joined 1M `zone` to be defined / non-warmup on its side).
2. Change L707 to `_sign_agreement(hz, mz, restrict_nonzero=False, mask=joined_valid_mask)`.
3. Update the L703-706 comment (it currently *documents* the asymmetry as intentional).
4. Record the choice as an **append-only amendment to PREREG-1H** (genuine-choice ratification): "price-BASIS axis agreement = EQ-inclusive raw equality over valid joined bars, consistent with the range-LAG axis and the 1H-E1 conservative-transfer purpose." Pre-data, firewall-safe; no threshold changes.

## §4 — What would change the recommendation (falsifier)

KEEP (`restrict_nonzero=True`) is correct **only if** the operator's *intent* for the price-BASIS axis is "directional-read concordance among bars that are directional on both bases" — a deliberately narrower question than "does the 1H signal transfer to the 1M gate." That intent is recorded nowhere and contradicts the gate's own 1H-E1 statement. **If the operator confirms that narrower intent, KEEP and document it; otherwise ALIGN.**

## §5 — Forbidden moves
- Editing the **range-LAG** axis (already correct/pinned to Pine) "for symmetry" — only the price-BASIS axis is under question.
- EQ-inclusive **without** a valid mask (re-introduces the warmup-`0==0` inflation).
- Touching the frozen 90%/3pp thresholds or any other locked 1H constant — this is an agreement-*definition* change, not a threshold change.
- Aligning silently — it is a PREREG-1H design ratification and must be amended append-only, not edited in place.

## §6 — Decision gate (binary, operator)
- **ALIGN** → implement §3 (1–3) + the PREREG-1H amendment (§3.4). Recommended.
- **KEEP** → operator affirms the narrower "directional-concordance-only" intent; document it in PREREG-1H + the L703-706 comment so it reads as a ratified choice, not an unexamined default.

## §10 — Audit hooks (runnable)
```bash
# The asymmetry to resolve (expect a hit at the price-basis axis until ALIGNed):
grep -n "restrict_nonzero=True" lab/analysis/ict_cascade_2026-06-18/harness_1h.py
# After ALIGN: a unit test must pin an EQ-vs-nonzero joined row as a DISAGREE
# (in the denominator), not a dropped row:
grep -n "price_basis" lab/analysis/ict_cascade_2026-06-18/test_harness_1h.py
# PREREG amendment present:
grep -n "price-BASIS axis agreement" lab/analysis/ict_cascade_2026-06-18/PREREG-1H.md
```
