# Personal lane live G0/G4: decisions for Joshua (2026-10-12)

**Status:** DRAFT decision list. None of these is ruled. It was drafted by a worker for the Deployment Coordinator, at `origin/main` `158bf2a`, and revised for the Claude docs review of #809.

**Cards:**
- [G0 calendar card](../briefs/handoffs/2026-10-12-personal-live-g0-calendar-card-DRAFT.md) (gap C4);
- [G4 roll card](../briefs/handoffs/2026-10-12-personal-live-g4-roll-card-DRAFT.md) (gap C5).

**Governs:** the FROZEN [Q-SFCLEAR-2 pre-registration](../briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md), §3 G0 and G4 and §11 item 11. Nothing here edits it.

## Relation to the frozen pre-registration

**No contradiction was found.** In §3 G4, "the route uses the same roll-date list" refers to the replay evidence route (§4 item 7, §6 VOID row, §7). The only live requirement is "the live rail rolls before that window".

**Reading note (no ruling needed).** G4 says "before", but OPEN-3 binds the live switch **at** the window's 18:00 ET open (zero margin; in the bound list, 36 of 36 6J/MGC seams have switch date = window start). The two agree because the old contract's last session ends, flat by G0's 16:00 ET, before the window opens. For the personal lane, G0's 16:00 own-flat carries OPEN-3's no-carry argument, which cites Tradeify's 16:45 flatten.

The live/replay G0 difference (evidence classes) is disclosed in §3 and was ruled at step 1 (g) "keep".

## Trust domain: premise for every wiring choice

`book_account_owner.py` is in the trust domain **T** (`trust_domain.py:146`, role `listener_account_owner`), and the collector re-derives imports. So:
- any owner edit is a **T** edit;
- an owner import of `personal_calendar_binding.py` or `contract_roll.py` pulls that module into **T**;
- either needs your code admission (G-1b in each card).

`c1_rail_listener.py` and `c1_rail_arm.py` were outside **T** at drafting. The calendar loader `book_session_calendar.py` is **T**.

## G0 decisions

**G0-1. What the personal live calendar is.**
- (a) Reuse the Tradeify-authored `book_session_calendar/v1` files byte-for-byte, admitted for the personal instance only through a separate personal ratification registry. No **T** code moves. On every PERMITTED row the times equal the personal rule (15:45, 15:55, 16:00).
- (b) A personal venue variant of the schema. This is a **T** loader edit plus an author-tool edit.
- (c) A separate personal loader and schema.
- **Recommendation: (a).**

**G0-2. Evidence-class denials in personal live.**
- (a) Keep all four first-release denials (§3, §11 item 11).
- (b) Drop UNCERTAIN_ADJACENT and MISSING_SOURCE for personal. This needs a **T** loader edit, because `book_session_calendar.py:535-538` requires the deny set to equal the four classes. It also needs authority beyond the calendar-parity amendment §2.
- **Recommendation: (a).**

**G0-3. Ratification unit.**
- (a) One personal registry row per digest, on your own words naming it.
- (b) A standing personal acceptance of every Tradeify-ratified digest.
- **Recommendation: (a).**

**G0-4. Future CME source captures.** CME's site terms bar agent automation.
- (a) Operator-attended captures.
- (b) An authenticated CME Reference Data pull.
- (c) Third-party encodings only.
- **Recommendation: (a).**

**G0-5. Personal venue deadline.** A Tradovate mandatory flat, liquidation or margin-switch time earlier than 16:15 ET for 6J, MGC, MYM or MNQ would break D = 16:00. Not verified.
- (a) You attest before the first personal ratification.
- (b) Use Tradeify's 16:45 as the proxy.
- **Recommendation: (a).**

**G0-6. Where the personal session binding is built (G0-b).**
- (a) Outside the owner, passing only the typed `BookSession` that the owner already validates. This keeps the module out of **T**.
- (b) Inside the owner. This is a **T** edit and needs G-1b.
- **Recommendation: (a).**

## G4 decisions

**G4-1. Live roll source (engineering choice).**
- (a) Regenerate the bound list byte-for-byte in ops (sha `72677d25…`), with no lab import, and extend it forward by the same rule.
- (b) A hand-maintained forward table, checked only against the CME capture.
- **Recommendation: (a).** Byte identity proves the live rule equals the replay route's.

**G4-2. Forward horizon.**
- (a) Admit 6J/MGC only for contracts that the 2026-10-12 capture confirms (6J through 2027-09, MGC through 2028-08). Refuse beyond that until a new operator-attended capture is bound.
- (b) The federal and Good Friday rule alone, with no horizon.
- (c) Require a D19 extension first.
- **Recommendation: (a).**
- Finding: in 2022–2026, D19 FULL_CLOSURE adds nothing to federal holidays and Good Friday. A drafting mutant run left the sha unchanged when either was dropped.

**G4-3. Selection object scope.**
- (a) All four legs, as OPEN-3 requires one object, with G4 refusal on 6J/MGC only.
- (b) 6J and MGC only.
- **Recommendation: (a).**

**G4-4. Where entry and add refusal sits (G4-b).**
- (a) The owner's dispatch path. This is a **T** edit, it pulls `contract_roll.py` into **T**, and it needs G-1b and a slot in the `book_account_owner.py` queue (P-L2 #805 → GC-5 → S2 → P4).
- (b) The listener's pre-send risk-add gate, beside the existing `book_halt` rejection (`c1_rail_listener.py:259-277`). This is P4's file and is outside **T** at drafting.
- (c) The sizing context. This is **T** and **F**.
- **Recommendation: (b), folded into P4.** It refuses before sizing and send with no **T** edit and no queue slot. Only (a) or (c) would put G4 inside the sealed domain, at the cost of a code admission. The flatten part goes wherever P4 puts its flatten executor; if that is the owner, it needs G-1b.

**G4-5. Which contract a live 6J/MGC order hits.** Today the rail sends continuous `6J1!`/`MGC1!` (`book_policy.py:182`, `:191`).
- (a) The personal route sends the dated contract from the OPEN-3 object, and 6J/MGC are refused until it can.
- (b) Keep `1!`, and refuse from each window start until you attest that the bridge has rolled.
- (c) Edit `LegSpec.order_symbol`. This moves **T** and **F**.
- **Recommendation: (a).**

## Both cards

**X-1. Executor:**
- (a) a Claude worker;
- (b) GLM.
- **Recommendation: (a).**

**X-2. Dispatch timing:**
- (a) build G0-a and G4-a now, in parallel;
- (b) wait for a RESOLVED Q-SFCLEAR-2 verdict.
- **Recommendation: (a).** The two share no file: only the G0 card edits `ops/calendars/README.md`. Both stay offline, outside **T** and outside the queue.
