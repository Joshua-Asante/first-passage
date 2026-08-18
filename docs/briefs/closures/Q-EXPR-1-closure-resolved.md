# Q-EXPR-1 — CLOSURE: `RESOLVED` (H1 horizon-mismatch models the orphaning)

**Verdict:** `RESOLVED` — H1 share 4/4 = 1.00 ≥ 0.50; H2 1/5 = 0.20 misses; H3 cannot fire
**Closed:** 2026-08-18
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-EXPR-1-verdict-preregistration.md`](../pre-registration/Q-EXPR-1-verdict-preregistration.md) — frozen on disk at sha256 `27c366f4f7e7a924a8e91ba549c8ade25eadd2024add1e827d70a31828e6441a` (printed by the scorer **before** `TABLE.json` was opened)
**Spend / K:** $0.00 · K consumed: **0** · no manifest
**Live effect:** none on rail / `core/` / `dd_protection`. Next slate admission screens claim horizon vs the E1 (flat-by-16:00) envelope.
**Artifacts:** [parent brief](../Q-EXPR-1-regularity-expression-conversion.md) · [prereg](../pre-registration/Q-EXPR-1-verdict-preregistration.md) · [`RESULTS`](../../../lab/analysis/_inbox/q_expr_1_2026-08/RESULTS.md)
**Parent notice:** [`N-2026-08-18-iteration2-identify-notice`](../../notes/notice/N-2026-08-18-iteration2-identify-notice.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | ≥1 of H1, H2, H3 meets 0.50 | H1 = 1.00 | ✓ |
| `FALSIFIED` | no H meets 0.50; no voiding BOUNDED disagreement | H1 fired | — |
| `AMBIGUOUS-HOLD` | BOUNDED disagreement, or H1/H2 miss and H3 cannot-fire is the only remaining modeling path | H1 fired, so the H3-collision clause does not apply | — |

Walked the non-firing Hs (required): H2 0.20 (only CON-2 is H2-positive). H3 cannot fire — weekly and daily share the earliest first-measurement day (2026-06-19, Q-ICT-CASCADE-1). Modal horizon is daily (3/4) — disclosed, not a fire.

## 2. What the pre-registration predicted vs what happened

Prereg §F predicted `RESOLVED` (H1) from the class (headline objects live at weekly/daily against a session envelope). Observed 4/4 H1-eligible rows are weekly or daily. No surprise on H1. H2 and H3 were disclosed-not-predicted; both stayed off.

## 3. What this closure does NOT license

- An H2 admission-rule change (projected gross/(4×RT) at native stop). H2 missed; CON-2 remains a hurdle kill on *its own* bar, not a class rewrite of CON-3/4/5.
- Demoting "find more regularities" via H3.
- Opening Q-TRAINKILL-1 (separate packet; operator GO).
- Retracting W / D-FVG / pools / CL SIGNAL-GENERIC. H1 prices the *conversion*, not the facts.
- Treating Q-TXG-1 as this Q's discovery (prior + evidence rows).
- Conflating this E1 with MSL "E1 HOLD."
- Lowering any cost bar or moving 0.50 after the table.
- Reading this `RESOLVED` as a live-scored H1-vs-rival contest. Prereg §F's pinned prediction
  shows the parent notice (obs. A, pre-freeze) had already named the headline objects at
  weekly/daily native horizon against the session E1 envelope — H1 could not plausibly have
  landed below 0.50. H3 was structurally cannot-fire at freeze (weekly and daily share the
  2026-06-19 first-measurement stamp, TABLE.json). H2 scores a disjoint denominator (the B3
  class), so it was never a rival to H1 either. This closure certifies a compositional fact —
  the native horizon of already-known orphaned regularities — not a result that discriminated
  H1 against a live competing H.

## 4. Defects found in the frozen brief (recorded, not repaired)

Q-R2AGRUN-1's packet death-stage vocabulary has no `magnitude` token. The table records it as `CI-power` (association/magnitude floor). Either label is H2-negative. No brief amendment.

Q-WLEGB-1 has no in-tree brief file (glob 0). The attempt row cites the MNQ ledger N8, which carries the numbers. Not a missing regularity.

## 5. Lesson candidates

**2026-08-18 — a weekly/daily RESOLVED fact is not an E1-expressible claim.** WSTRUCT-M2K would have died at admission under this filter, before its scoping brief, at $0. Dated: this close. Dollar cost: $0 (caught at the cheap falsifier). Below the two-incident bar as a standing lesson — watch; the filter is the INTEGRATE commit, not a new doctrine file.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `RESOLVED` (H1)
- **Model update:** The converter has not fired because the estate's validated regularities live at weekly/daily native layers and the venue envelope is session-flat. Cost-quantization is real on CON-2 and on the TXG small-edge wall, but it is not the *dominant* property of the orphaning class (H2 0.20). Screening-order clustering cannot be scored — W and D were first measured the same day.
- **Next:** INTEGRATE
- **Routing:** INTEGRATE — next slate / harvest admission screens claim horizon vs the E1 (flat-by-16:00) envelope. A claim whose native horizon is weekly or daily is rejected at $0 unless it names a same-horizon (session) expression *before* any build. This is the packet's H1 branch. H2/H3 branches stay off.
- **Entry packet:** n/a — INTEGRATE
- **Stop rule / re-proposal bar:** n/a — integrated
- **Board write:** STATE decision-index 2026-08-18 Q-EXPR-1 line; SESSIONS 18f Open/next; notice packet 2 CLOSED; next slate admission carries the horizon screen.
- **Registry:** n/a — conversion census / methodology; not a strategy-grounds seed kill

## §10 audit-hook discharge

```
rg -n "N-2026-08-18-iteration2-identify-notice" docs/briefs/Q-EXPR-1-regularity-expression-conversion.md
→ hits (parent cite)

rg -n "E1 HOLD|flat-by-16:00" docs/briefs/pre-registration/Q-EXPR-1-verdict-preregistration.md
→ E1 defined as flat-by-16:00; MSL E1 HOLD explicitly not this object

rg -n "27c366f4f7e7a924a8e91ba549c8ade25eadd2024add1e827d70a31828e6441a" lab/analysis/_inbox/q_expr_1_2026-08/RESULTS.md
→ 10:`27c366f4f7e7a924a8e91ba549c8ade25eadd2024add1e827d70a31828e6441a`

python lab/analysis/_inbox/q_expr_1_2026-08/score_expr.py
→ H1 4/4  H2 1/5  H3 cannot_fire  verdict RESOLVED
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-18 | Closure authored | Cursor (this session) |
| 2026-08-18 | Added §3 compositional-fact disclosure bullet; fixed §10 audit-hook cmd 3 (was a non-matching `"prereg_sha256"` string search, exit 1) | Claude (adversarial review) |
