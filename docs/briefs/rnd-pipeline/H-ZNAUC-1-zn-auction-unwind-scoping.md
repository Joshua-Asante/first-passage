# Campaign scoping — H-ZNAUC-1 ZN Treasury-auction dealer-hedging-unwind confirm

**Status:** `CLOSED — SCREEN-FAIL (cost-wall)` (2026-07-20). Operator authorized the Databento own-cohort δ-extraction (resolving the initial NEEDS_CONTEXT). Measured ZN post-auction δ = **1.01 bp/event** (primary 10Y-family, N=134, 0→15m) vs the Requirement-5 hurdle **6–10 bp** → FAIL by 6–10×; power also marginal at the realized N. Direction confirms Smales (dealer short-hedge unwind) but the edge is far sub-cost. Third Tier-B/C event-drift seed to die at the Stage-2 cost-law (after D5, H-OD-1). Closure: [`../closures/H-ZNAUC-1-closure-screen-fail.md`](../closures/H-ZNAUC-1-closure-screen-fail.md). **F-C steps up (its own family-K nod required).** K consumed 0; ZN bank stays 0; Databento pull $0.00.
> **Historical (pre-close):** the δ was initially `NEEDS_CONTEXT` — Smales 2021 (`acfi.12635`) is Wiley-paywalled and SSRN 403s automated fetch. The operator-authorized Databento own-cohort extraction superseded that route and resolved the screen directly.
**Axis:** fork **F-A** — `H-ZNAUC-1` post-auction dealer-hedging-unwind drift, 10-year T-note futures (**ZN**), from Smales (2021)
**Lane:** mechanism-first, Path **1a** (named mechanism — primary-dealer inventory hedging unwind). HARV ADR `Accepted` — HARD gate.
**Parents:** [`Q-BOOKFIT-1`](../Q-BOOKFIT-1-fork-composition-coordinate-triage.md) (`CLOSED-RESOLVED` 2026-07-20 — F-A projected ρ 0.512 / risk-N_eff Δ +0.787, book-improving band, **the composition-fit basis for funding this probe**) · [`Q-INVENTORY-1`](../closures/Q-INVENTORY-1-closure-falsified.md) (`FALSIFIED` 2026-07-17 — F-A the priced-but-unfunded ZN-auction fork; "Per-event δ not in abstract → full-text retrieval + δ extraction") · operator **Fork program GO** 2026-07-20 (STATE.md; order F-A → F-C → F-B)
**Inheritance:** harvest-intake ADR 2026-07-15 (`268851b`) + same-units/per-gate/panel-basis attestation ADR 2026-07-16 (`ba943a1`, `Accepted`) — Requirement-5 cost-law is binding at admission, in ZN's own bp-basis.
**Sibling precedent:** [`H-TSMOM-1`](H-TSMOM-1-ES-tsmom-scoping.md) (the "full-text scrape → δ/σ" pattern this probe would follow once the PDF is in hand) · [`H-OD-1`](H-OD-1-ES-overnight-drift-scoping.md) (Tier-B/C cost-law kill precedent — the wall F-A's δ must clear).

---

## §0 — Grounding (Rule-0 anchors, read 2026-07-20, HEAD `aacefd5`)

| Source | Anchor | Supplies |
|---|---|---|
| [`Q-BOOKFIT-1` closure](../closures/Q-BOOKFIT-1-closure-resolved.md) | `aacefd5` | F-A composition-fit: ρ 0.512 (<1.0), risk-N_eff Δ +0.787 (>0) at the 0.37% reference weight; N_b=36/yr episodic; this is *why* F-A funds first — book-fit is established, edge is the open question |
| [`Q-INVENTORY-1` closure](../closures/Q-INVENTORY-1-closure-falsified.md) | `4de8085` | F-A row: **~36 events/yr, N≈259 → confirm-power viable iff δ/σ ≥ 0.122** (Requirement 4); **ZN family bank 0** (Requirement 3 CLEAR — the one permanent kill does not fire); missing input = per-event δ, method = full-text retrieval + extraction; ~$0/one session/K-unchanged-until-screened |
| [`strategy_harvest.md`](../../methodology/strategy_harvest.md) §1 Req 2/4/5, §2.1 | `268851b` | Req 2: no citable δ ⇒ **UNSCREENABLE → δ-extraction probe or drop; never invent a number**. Req 4 confirm-power ≥ 0.50. §2.1: auction-drift is **Tier B** — "admits only if event rate clears Req 4 AND per-event δ clears the cost inequality; check both, assume neither." Req 5 relief valve = redesign route, not re-screen. |
| [same-units attestation ADR](../../adr/2026-07-16-harv-attestation-same-units-supersession.md) | `ba943a1` | Req-5 mandatory inequality `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, commissions incl.)`, at the basis the Stage-2 gate scores on — the wall D5 + H-OD-1 both died at. Cannot be run until δ exists. |
| Smales (2021), *The effect of treasury auctions on 10-year Treasury note futures*, *Accounting & Finance* 61(S1) 1517–1555 (DOI 10.1111/acfi.12635; SSRN 3315135) | web-verified 2026-07-20 | **Mechanism (1a) confirmed:** primary dealers buy back short futures hedges immediately post-auction ⇒ prices move higher, volatility + volume up, in the interval following the auction; **15-min intervals, 2000–2017, ZN-native.** **Magnitude NOT in any accessible summary** (see §0.5). |

---

## §0.5 — The load-bearing open input: the ZN-native per-event δ

**What is needed:** the **unconditional** average post-auction ZN futures return over the tradeable window (the 15-min interval(s) immediately following the auction), expressed as bp/event and as δ/σ (return ÷ interval-return σ), conservative-central reading + publication-decay haircut. This is the single input that gates both Requirement 4 (power: viable iff δ/σ ≥ 0.122) and Requirement 5 (cost-law: δ_bp ≥ 4×RT_frac).

**Why it is not in hand (2026-07-20, automated attempt exhausted):**
1. **Access.** Wiley full text is paywalled (`acfi.12635`, HTTP 403); the SSRN Delivery PDF (`SSRN_ID3315135`) 403s automated fetch; ResearchGate is request-only; the UWA repository landing is metadata-only; the one open blog summary (paperswithbacktest) carries **no numbers** and describes a *different* trade (a pre-auction 2s10s relative-value position, not the post-auction unwind drift). The δ requires the full-text tables, which need an authenticated download.
2. **Substantive risk to check the moment the PDF arrives (flag, not a verdict).** Every accessible summary frames the tradeable effect as **conditional on bid-to-cover** ("higher bid-to-cover ratios lead to positive returns; bid-to-cover exceeding average → positive returns and lower volatility"). Bid-to-cover is revealed *at* the auction. If the positive return is materially bid-to-cover-signed, the **unconditional** post-auction long (buy ZN after every auction, no auction-outcome conditioning) captures a *diluted* δ — auctions with below-average demand may show weak/negative drift. This is structurally F-B's informed-flow concern (Requirement 2). The extraction must therefore pull the **unconditional** post-auction mean return specifically, not the bid-to-cover-conditional coefficient, and must state which it is.

**Disposition of the missing input:** per `strategy_harvest.md` Req 2, no citable δ ⇒ **UNSCREENABLE**, routed to a δ-extraction probe (this scoping). The probe's data step is $0 / no-K, but its *input* (full text) is operator-suppliable — so this is `NEEDS_CONTEXT`, not `BLOCKED` and not a kill.

---

## §1 — Seed manifest (harvest §C 4-tuple)

| Field | Value | Status |
|---|---|---|
| **Family → K_banked** | ZN (10-yr T-note futures) → **0** | ✔ Req 3 CLEAR (the only permanent kill; does not fire) |
| **Design → K_intrinsic** | ≤ 3 fixed hypotheses (pre-committed at admission; the primary is a single unconditional post-auction long over a fixed window — see §2). Confirm-don't-mine: any post-admission widening (window sweep, bid-to-cover conditioning added as a variant) voids the screen and is a new axis. | declared |
| **Era → N** | ~36 auction events/yr; N ≈ 259 over the harvest panel (Req-4 power viable iff δ/σ ≥ 0.122) | from Q-INVENTORY row |
| **Cohort δ/σ** | **PENDING** — ZN-native, not yet extractable (§0.5); no cross-instrument transplant permitted (Req 2) | NEEDS_CONTEXT |
| **Mechanism (Req 1a)** | primary-dealer short-hedge unwind post-auction (Smales 2021) | ✔ confirmed |

---

## §2 — Pre-committed hypothesis (declared before any δ is read; frozen at Stage-0 if this proceeds)

**H-ZNAUC-1 (primary, K=1):** an **unconditional** long in ZN (or MYM-scale micro equivalent — instrument TBD at scoping; the micro/tick basis needs a ZN instrument-ledger card, absent today) opened at the first bar after the auction result and held over a **fixed** post-auction window, earns a positive mean per-event return, on the temporal-OOS era (Campaign-defaults Default #1), that clears **both** Req-4 power (δ/σ ≥ 0.122) **and** Req-5 cost-law (δ_bp ≥ 4×RT_frac at ZN's panel-era basis).

Optional pre-committed variants (still within K_intrinsic ≤ 3, declared now so they are not post-hoc): (2) the same over the roll-clean subset; (3) the same excluding the below-average-bid-to-cover events **only if** the unconditional form is reported so the conditioning is a disclosed robustness cut, not the edge itself — adding bid-to-cover *as the signal* is a new axis, not a variant.

---

## §3 — Gate (what this scoping resolves to, once δ is supplied)

| Outcome | Trigger | Disposition |
|---|---|---|
| `SCREEN-PASS` | extracted unconditional δ clears **both** Req-4 (δ/σ ≥ 0.122) **and** Req-5 (δ_bp ≥ 4×RT_frac, ZN basis) | licenses **Stage-0 campaign pre-registration** only (HARV §R reachability attestation still binds; nothing deploys); ZN instrument-ledger card authored as a Stage-0 prerequisite |
| `SCREEN-FAIL (cost-wall)` | δ_bp < 4×RT_frac | close (F-A dead as declared; D5/H-OD-1 class); **F-C steps up** (its family-K ask) |
| `SCREEN-FAIL (power)` | δ/σ < 0.122 at N≈259 | close; F-C steps up |
| `Req-2 informed-flow` | the only positive δ is bid-to-cover-conditional; no tradeable unconditional drift | close as informed-flow (F-B class); F-C steps up |
| `NEEDS_CONTEXT` (current) | full text not obtained | **hold**; operator supplies SSRN/Wiley PDF or authorizes a Databento own-cohort δ-extraction; re-enter at δ-extraction |

**No verdict is licensed by mechanism confirmation alone** — the M-21 book-fit (Q-BOOKFIT) says the risk *geometry* fits; it says nothing about edge. F-A remains an unscreened seed until δ clears the gate.

---

## §4 — Forbidden moves

- **Inventing or transplanting a δ.** No number from a non-ZN cohort, no plausibility estimate, no "similar auction studies suggest ~X bp." Req 2 is explicit: never invent. UNSCREENABLE is the honest state.
- **Reading the bid-to-cover-conditional coefficient as the tradeable δ.** That is the informed-flow trap; the confirm is an *unconditional* post-auction long. Conditioning is a disclosed robustness cut, never the edge.
- **Auto-promoting F-C because F-A is pending.** F-A is NEEDS_CONTEXT, not dead — it holds its priority slot. F-C advances only on an F-A close (FAIL/informed-flow) **or** an explicit operator decision to skip the paywall wait (and F-C still needs its own family-K nod).
- **Opening a pull or `register_search` on this seed now.** No data spend, no K, until δ clears the screen (confirm-don't-mine; the probe's cost is one division, not a campaign).
- **Window/threshold drift after seeing δ.** §2's window and the Req-4/Req-5 thresholds are frozen pre-extraction (Trap #12); a post-δ window search is a new axis.

---

## §10 — Audit hooks (runnable)

```bash
# Family-K still 0 (the CLEAR requirement must stay clear)
grep -rn "ZN" discovery_manifests/*.json 2>/dev/null | grep -i "family\|bank" || echo "ZN unbanked — Req 3 holds"
# No pull / no manifest opened by this scoping
git log --oneline --since=2026-07-20 -- discovery_manifests/ | wc -l   # expect 0 attributable here
# Re-screen readiness: does a ZN-native δ source exist in-repo yet?
ls lab/analysis/*zn*auc* 2>/dev/null || echo "no δ-extraction harness yet — NEEDS_CONTEXT holds"
# Same-units cost-law must be run at ZN basis before any SCREEN-PASS (guard):
grep -n "4 . RT_frac\|4×RT" ops/instruments/ZN.md 2>/dev/null || echo "ZN ledger card absent — author before SCREEN-PASS"
```

---

## Verification

```bash
$ python scripts/check_brief.py docs/briefs/rnd-pipeline/H-ZNAUC-1-zn-auction-unwind-scoping.md --type inquire
$ git log -1 --format='%h' -- docs/briefs/closures/Q-INVENTORY-1-closure-falsified.md   # expect 4de8085
# Mechanism/instrument confirmation (this session, web): Smales 2021 acfi.12635, ZN, 2000-2017, 15-min, dealer-hedge unwind
```
