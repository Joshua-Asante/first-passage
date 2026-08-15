# SPEC: TNEC-AU-1 — application units for book admission (pass binds the book; bust binds both)

Status: PROPOSED · 2026-08-11 · authorizes nothing ($0 · K=0) · depends: TNEC-1
Objective: Pin the scored unit for each TNEC limb so that a **book** — not any single leg — is the unit that must pass the incumbent eval, while every leg must still not-kill the book.

Application units (the ruling; TNEC-1's "single construct, or book jointly" made limb-precise):

| Limb | Unit |
|---|---|
| N-ACT | **BOOK** — union cadence ≥1 trade/Mon–Fri week; co-idleness measured + disclosed (correlated idleness is the failure mode, EM4) |
| N-SURV · bust ≤3.0% | **BOTH** — composed book, full + both halves, intraday-honest, at deployable integer sizing; AND marginal (adding a leg may not degrade the composed book past the ceiling) |
| N-SURV · P(pass) ≥50% | **BOOK ONLY** — no per-leg pass requirement exists |
| N-EDGE | **LEG** — harvest Req 1–5, net>0 after costs, CI excluding 0, DSR ≥ floor_at_k(K_intrinsic), all unchanged per leg. Book-level *magnitude* adjudication is **not licensed here** (separate ruling if ever wanted) |
| N-SHAPE | **LEG** (EM3 independence, hard stops) + **BOOK** (§4a Product-Group/sign across co-legs; S7 occupancy where an account is shared) |
| N-SIZE | **BOOK** — edge-indexed frontier at book level; per-leg shares via the existing aggregate-cap machinery (RESERVE rule; missing per-leg share → HALT, never account-cap fallback) |

Marginal admission (leg k+1 into book B), in kill order: (1) S4/S7 structural screens; (2) $0 covariance pre-kill — daily-$-std(leg)/daily-$-std(B) + `n_eff_risk_delta` in covariance space (PR(cov), never PR(corr)); necessary-never-sufficient per M-21, ORB-MNQ-1 is the negative control; (3) composed both-halves intraday-honest re-MC: **ADMIT iff composed bust ≤3.0% (full + both halves) AND (composed P(pass) ≥ book-without-leg, OR liveness improves with bust preserved)**. Leg 1 of an empty book: the leg *is* the book — the full two-part ceiling binds it composed-of-one.

Vocabulary: a candidate failing **only** standalone N-ACT scores **`BOOK-CONDITIONAL(cadence)`** and routes to the book-candidate pool, not the rejected registry. No other limb earns the token.

Compositions are **pre-committed and scored once** (Q-COMPOSE-1 pattern). Selecting among ≥2 candidate books is best-of-K and is priced in K (EM0 arithmetic applies to composition search).

Supersession note: the FROZEN 2026-07-13 survivor-scoring pre-registration is never back-edited (Trap #12); its thresholds (3.0% / 50%), G0–G8 protocol, and ≥2-of-4-tiers discharge are **untouched**. On the application-unit question its freeze-time text is historical and **this spec governs forward** (the harvest-doc/§B precedent for frozen-vs-governing).

Steps:
1. Operator ratifies (Status → RATIFIED; ≤300-word light record per ceremony tiering).
2. $0 retro-sweep (report-first): list candidates killed solely on standalone cadence/N-ACT across closures, the rejected registry, and instrument DEAD lists (include the Q-6JCOMPOSE-1/-2 VOID closures); propose `BOOK-CONDITIONAL(cadence)` relabels; operator confirms each individually.
3. Dual-lens scoring (standalone + marginal-to-book) becomes standard in adjudications; Aegis→6J is the first to carry it.

Gate: RESOLVED if ratified AND ≥1 adjudication scores under the dual lens; FALSIFIED if any book admitted under this unit re-measures composed bust > 3.0% (both halves, intraday-honest) before deployment GO — revert via superseding spec, never in-place edit.
Boundary: no Req 1–5 / EM0 / regime-gate loosening under cover of book-necessity (TNEC boundary inherited verbatim) · the bust ceiling never becomes book-only · no composition search (pre-committed only) · covariance/risk-breadth pre-screens never substitute for the composed MC · margin-decisive N-SURV kills stay dead (Guardian-MGC; the token saves cadence-only kills, nothing else) · Striker-leg venue de-scope untouched · no second clock (rides the four-firms 2026-11-08 date).
Reads: TNEC-1 @ `7e92394` · survivor-scoring prereg @ `91137fb` (§0 two-part-ceiling resolution + Trap-#12 amendment rule read ±20) · objective_composition_map @ `8059d3b` (admission/book/composition rows) · Stage-8 ADR @ `5563cf4` · Q-COMPOSE-1 closure @ `76b7569` (variance dominance; 2.65%→38.75%) · Guardian-MGC closure @ `42e27a1` (margin-decisive calibration case) · decompound/5th-leg CARD @ `47cc3eb` (risk-neutral insertion; body archived) · `ops/c1_rail/c1_sizing_host_reference.py` @ `3d5dfb7` (RESERVE + HALT semantics, categorical).
Owner: TNEC-1 (2026-08-08 edge-cohort-correction ADR thread).
