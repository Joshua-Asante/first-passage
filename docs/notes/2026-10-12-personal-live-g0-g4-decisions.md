# Personal lane live G0/G4: decisions for Joshua (2026-10-12)

**Status:** DRAFT decision list. None of these is ruled. It was drafted by a worker for the Deployment Coordinator, at `origin/main` `158bf2a`.

**Cards:**
- [G0 calendar card](../briefs/handoffs/2026-10-12-personal-live-g0-calendar-card-DRAFT.md) (gap C4);
- [G4 roll card](../briefs/handoffs/2026-10-12-personal-live-g4-roll-card-DRAFT.md) (gap C5).

**Governs:** the FROZEN [Q-SFCLEAR-2 pre-registration](../briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md), §3 G0 and G4 and §11 item 11. Nothing here edits it.

## Contradictions with the frozen pre-registration (scoped disposition needed)

1. **G4 "the route uses the same roll-date list" cannot hold literally for live use.**
   - The bound list (`roll_dates_6J_MGC_2022-09-01_2026-09-02.json`, sha `72677d25…`) holds only contracts whose window meets 2022-09-01..2026-09-02. Its rule C3 is "every one whose G4 window intersects the replay window". Every live contract lies outside it.
   - Disposition is G4-1 below. Either reading keeps the frozen text and the replay unchanged.
2. **Not a contradiction, but a reading to confirm with G4-1.** G4 says "the live rail rolls **before** that window", while OPEN-3 binds the live switch **at** the window's 18:00 ET open (zero margin; 36 of 36 6J/MGC seams in the bound list have switch date = window start).
   - The two agree only on this reading: the old contract's last session ends, flat by G0's 16:00 ET, before the window opens.
   - OPEN-3's own no-carry argument cites Tradeify's 16:45 ET flatten. For the personal lane, G0's 16:00 own-flat must carry it instead.

The live/replay G0 difference (evidence classes) is disclosed in §3 and was ruled at step 1 (g) "keep". It is not a contradiction.

## G0 decisions

**G0-1. What the personal live calendar is.**
- (a) Reuse the Tradeify-authored `book_session_calendar/v1` files byte-for-byte, admitted for the personal instance only through a separate personal ratification registry. No trust-domain code moves. On every PERMITTED row the times equal the personal rule (15:45 cutoff, 15:55 flatten start, 16:00 own-flat). Tradeify's venue rows stay in the bytes as an extra restriction.
- (b) A personal venue variant of the schema, without Tradeify's sources or clocks. This edits `book_session_calendar.py` (trust domain **T**, which moves the Tradeify domain) and the author tool.
- (c) A separate personal loader and schema. This duplicates the verifier.
- **Recommendation: (a).** Revisit (b) only if Tradeify's monthly extension stops.

**G0-2. Evidence-class denials in personal live.**
- (a) Keep all four first-release denials: HOLIDAY, SHORTENED, UNCERTAIN_ADJACENT, MISSING_SOURCE. Live then permits a subset of the replay's sessions, as §3 and §11 item 11 disclose.
- (b) Drop UNCERTAIN_ADJACENT and MISSING_SOURCE for personal, to match the replay. This needs a policy variant and authority beyond the calendar-parity amendment §2.
- **Recommendation: (a).**

**G0-3. Ratification unit.**
- (a) One personal registry row per calendar digest, on your own words naming it, each month.
- (b) One standing personal acceptance of every Tradeify-ratified digest.
- **Recommendation: (a).** Ratification is per digest, and (b) would let a Tradeify act admit personal risk.

**G0-4. Source captures for future months.** CME's site terms bar agent automation.
- (a) You read or attend each capture, including the Columbus and Veterans Day clearing notices whose absence makes a row MISSING_SOURCE.
- (b) An authenticated CME Reference Data pull (cost and licence unknown).
- (c) Third-party encodings only (secondary, D19-grade).
- **Recommendation: (a).**

**G0-5. Personal venue deadline.** Does Tradovate impose, for 6J, MGC, MYM or MNQ on a regular session, a mandatory flat, liquidation or margin-switch time earlier than 16:15 ET? Such a time would move V and break D = 16:00. Not verified at drafting.
- (a) You attest from Tradovate's published terms or its written answer before the first personal ratification.
- (b) Treat Tradeify's 16:45 as the proxy, with no attestation.
- **Recommendation: (a).**

## G4 decisions

**G4-1. Scoped disposition of "the same roll-date list"** (contradiction 1).
- (a) Read it as the same rule. The ops source regenerates the bound list byte-for-byte (sha `72677d25…`), with no lab import, and extends it forward under the same rules. The live/replay equality is then proven on the replay window.
- (b) A new frozen forward list, which needs a new pre-registration action. A frozen file cannot be amended in place.
- **Recommendation: (a).**

**G4-2. Forward horizon.**
- (a) Admit 6J and MGC entries only for contracts whose dates the 2026-10-12 CME capture reproduces (6J through 2027-09, MGC through 2028-08). Refuse beyond that until a new operator-attended capture is bound.
- (b) The federal and Good Friday rule alone, with no horizon.
- (c) Require a D19 extension first.
- **Recommendation: (a).**
- Finding: every D19 FULL_CLOSURE weekday in 2022–2026 is a federal holiday or Good Friday, so D19 adds nothing to the business-day rule there. A drafting mutant run confirmed this: dropping D19, or dropping Good Friday, leaves the bound sha unchanged. The forward residual is therefore only an unannounced ad hoc closure, which (a)'s capture vectors bound.

**G4-3. Selection object scope.**
- (a) One per-leg object for all four legs, as OPEN-3 requires ("one per-leg contract-selection object"), with G4 refusal on 6J and MGC only.
- (b) 6J and MGC only.
- **Recommendation: (a).**

**G4-4. Where live enforcement sits.**
- (a) The owner's dispatch path, for entry and add refusal, plus P4's flatten executor. These sit in the `book_account_owner.py` queue after P4 (P-L2 #805 in review → GC-5 → S2 → P4), or are folded into P4.
- (b) The listener entry gate (also P4's file).
- (c) The sizing context (`book_sizing_context.py`, **T** and **F**).
- **Recommendation: (a), folded into P4.** It saves a queue slot, and P4 already owns the entry gate and flatten.

**G4-5. Which contract a live 6J/MGC order hits.** Today the rail sends continuous `6J1!`/`MGC1!` (`book_policy.py:182`, `:191`, "provisional"), so the bridge's own roll picks the contract.
- (a) The personal route sends the dated contract returned by the OPEN-3 object. Until it can, every 6J/MGC entry is refused.
- (b) Keep `1!`, and refuse 6J/MGC entries from each window start until you attest that the bridge has rolled.
- (c) Edit `LegSpec.order_symbol`. This moves **T** and **F**, and the TB-I1 fingerprint.
- **Recommendation: (a).** It binds to ADR 2026-10-09 items 3–4. Note that the personal destination may change (#807, the native-runtime proposal).

## Both cards

**X-1. Executor:**
- (a) a Claude worker for G0-a and G4-a, with the G0-b and G4-b wiring inside P4;
- (b) GLM.
- **Recommendation: (a).** Both gate live risk.

**X-2. Dispatch timing:**
- (a) build G0-a and G4-a now, since they are offline and outside the queue;
- (b) wait for a RESOLVED Q-SFCLEAR-2 verdict.
- **Recommendation: (a).** Building grants no live use. M1, arming, live-spend and per-session GO stand.
