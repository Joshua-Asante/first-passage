# Feed proposals for operator disposition: capped collection overlapping T00, and a one-session October window exception

**Status:** PROPOSALS ONLY, for Joshua's final disposition. Nothing here is an adopted gate, a spend or collection GO, a reversal of an earlier ruling, or a change to the frozen feed-equivalence spec. Prepared by coordinator (4), the feed-spec owner, 2026-10-04. Joshua authorized *preparing* these (through hyper, then "Let's get to it" via C5); preparing them is not adopting them.

**Owner texts:** the feed-equivalence spec [`docs/spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md`](../spec/2026-09-27-cme-execution-feed-equivalence-test-DRAFT.md) (frozen; all eleven parameters bound; digest `3e409943…`); the [binding packet addendum 2026-10-04](2026-10-02-feed-spec-open-parameter-binding-packet.md) (Joshua's dispositions of hyper's proposals); the deployment checklist CP-7.

## 1. Capped provider/feed collection overlapping T00

**Earlier ruling (quoted):** Joshua, 2026-10-04T00:17:19Z, disposition 4: "**Funded, emission-disabled collection overlap: deferred.** T00 is not shown to be the final CP-7 blocker. Revisit only if it is."

**Proposal (bounded):**
- Collection runs with `emit_enabled=false` from one provider, chosen later, under a spend cap Joshua sets.
- Collection only: no adapter is used for trading, and nothing is emitted.
- The provider and budget are unspecified here; they come from the separate provider candidate decision sheet.

**What adoption would require:**
- An explicit reversal of disposition 4.
- A CP-7 grant within the scope already ruled (S2b addendum 2026-10-02: provider-specific adapter and shadow collection, emission disabled).
- A spend decision under the existing ceilings.
- Every frozen-spec rule still applies: bindings were fixed before any provider data, and a window opens only per OPEN-8.

**Trade-off:** it can save calendar time if T00 ends up as the last CP-7 blocker. It spends money and provider effort before T00's GO evidence, and it does not shorten the frozen window minimum.

## 2. One-session October exception to the window minimum

**Earlier ruling (quoted):** Joshua, 2026-10-04T00:17:19Z, disposition 1: "**Live month-end-adjacent session: rejected.** The adopted window minimum stays as frozen (spec §16.2). Removing it would need a §13 re-opening, and the saving may be zero."

**Proposal (bounded):** for one October window only, drop the month-end-adjacent session requirement. Keep everything else:
- ten covered four-leg sessions, two Sunday opens and two Friday closes;
- every existing control;
- all consumed timestamps, including settlement, in the verified current regime, with closeout before any regime transition.

**What adoption would require:**
- An explicit reversal of disposition 1.
- A **§13 re-opening ADR "justifying why prior thresholds were misspecified, written without reference to observed data"** (spec §16.2, §13 row), adopted **before any provider data is seen** and before CP-6.
- A new Status digest and a §16.4 log row.

**Trade-off:** it could start a window sooner in October. It removes the only month-boundary observation, and the §13 path is deliberately heavy.

## 3. Not covered here

- The provider candidate decision sheet (five parts) is drafted separately by Assist Coordinator 5.
- The verification-amendment proposal is also Assist Coordinator 5's.
