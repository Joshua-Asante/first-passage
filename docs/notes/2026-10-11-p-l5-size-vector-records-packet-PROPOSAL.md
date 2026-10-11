# P-L5: size-vector records packet (PROPOSAL)

**Date:** 2026-10-11 · **Base:** `origin/main` `b5571a9` (records unchanged through `ba000b2`) · **For:** the Deployment Coordinator ("Portfolio deployment coordination")

**Status:** a PROPOSAL. It writes no record, and authorizes no write.

**Parents:**
- [scope note](2026-10-11-live-size-vector-wiring-scope.md) §5 row P-L5;
- [P-L4 proposal](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md) (D-A);
- [R-SV](2026-10-11-r-sv-live-route-size-vector-requirement-PROPOSAL.md).

## 1. What P-L5 is, and who executes it

P-L5 is not a build. It is a list of record writes, each due at a fixed checklist step. Together they let T16 "prove equality to qualified shared components" for sizing, and let T17 show the active rail sizes with the screened vector.

**Executor: the coordinator seat, not a worker.**
- Every item is a governance or owner-record write (`governance.author`).
- `scripts/seat_authority.yml` grants that capability to coordinator, executive and escalation seats only. The worker grant list (`:105-108`) omits it.
- So no worker card is drafted.
- Each item rides the owner's own PR at its step. P-L5 is a checklist the coordinator carries, not a separate PR.

**Lane:** not GLM. Only hashes are written, but every item touches sizing identity. **Effort:** about 0.25 coordinator-day, spread over T9–T17.

## 2. The chain each record helps prove

```
pre-registration values block   size_vector_sha256 = 139919cd…c271   (public; recorded 2026-10-10)
  = screen authority            parameters.expressions.size_vector_sha256   (validated against r3d's bytes)
  = production E1 / FBR         sha256(canonical_json_bytes(sizing)) of the startup policy E1 replays
  = deployment GO (D-A)         size_vector_sha256 field (or the admitted row's provenance)
  = live loader (R-SV)          the hash of the referenced private bytes, before the owner is built
  = owner stamp (P-L2)          runtime_bindings.size_vector_sha256
  = activation ack (R-SV)       the stamped hash, read back after restart
```

Every link is a hash comparison, and no record carries a vector value. The startup policy v2 digest (`53dea292…`) is recorded beside the vector hash wherever the whole artifact is referenced (R-SV D-SV-2).

## 3. The record items

| # | Due at | Owner record | What is written | Check | Needs |
|---|---|---|---|---|---|
| REC-1 | Now (done) | Successor pre-registration values block | `size_vector_sha256` `139919cd…c271`; startup v2 `53dea292…` | `git grep -c 139919cd1a20961b660c57527fa45c6b811124d468cfc97a3dd161db4d54c271 origin/main -- docs/briefs/pre-registration/` ≥ 1 | Nothing. It must be re-validated at H′ (pre-registration §5a item 1); a change there returns to the coordinator |
| REC-2 | Screen authority issued (#758 §7 step 7) | The authority's own record | The authority's `size_vector_sha256` | `validate_screen_authority` ISSUED; its value equals REC-1 | Nothing new |
| REC-3 | T15 / CP-6 (F1 freeze) | [T10 source and freeze packet](../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md) and the F1 freeze record | The production attempt's startup policy is v2 with that `sizing`: its digest and its `size_vector_sha256` | The recomputed hash of E1's startup `sizing` equals REC-1 | **D-P5-1.** E1 must replay the successor's sizing, not r3c's v1 |
| REC-4 | T6 TB-B7 (EF1) | [Admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) §2a T6, and the TB-B7 record | EF lists the sizing artifact digest and `size_vector_sha256` as **shared components** (qualification ↔ live), so B7's shared-component proof covers sizing | B7 proof row: EF sizing hash = REC-3 | **D-P5-2.** T6's EF composition does not name sizing today. Adding it is an ADR addendum (Joshua) |
| REC-5 | T9 TB-D2 | The TB-D2 decision record (digests and labels only) | The §2 chain table, REC-1 through REC-4, each hash with its source | Every row equal | Nothing beyond REC-3 and REC-4 |
| REC-6 | T10 GO | `DEPLOYMENT_GO.json`, written by TB-D2 | The GO `size_vector_sha256` field, or the row provenance, per D-A | Equals REC-5 | P-L4 D-A, plus the ADR T10 addendum if D-A = GO field |
| REC-7 | T16 | The T16 combined-acceptance record | Links to the parity evidence: P-L1 LS2, P-L2 LB4 and LB8, P-L3 LE2 (the same law in replay, live owner and emulator); R-SV's loader tests | Records cited at their PR heads | P-L1, P-L2 and P-L3 merged; R-SV built |
| REC-8 | T17 activation | The activation-session record (TB-O1 procedure), and the venue-edition ledger's `deployment` column | The activation acknowledgment's stamped hash, read back after restart, equal to REC-6 | Read-back = REC-6 | **D-P5-3** (ledger row) |

## 4. Decisions

- **D-P5-1 (coordinator, then F1).** REC-3 needs the production E1 to replay the successor's v2 startup policy. Today's T10 packet (2026-09-21) predates P-S2, so it cannot name a v2 startup policy. *Recommend:* the F1 freeze inventory names the v2 startup artifact by digest. The successor GO is meaningless if E1 qualified r3c's sizing.
- **D-P5-2 (Joshua; ADR owner).** Add sizing to T6's EF composition, so that B7's shared-component proof covers it. *Recommend:* yes, in the same ADR addendum as P-L4 D-A, if D-A = GO field. One ratification would then cover both.
- **D-P5-3 (coordinator; venue-binding ADR §2.6 owner).** The [venue-edition ledger](../../ops/venue_editions/Tradeify_Select_100K.md) has no row for the four-leg book as such, and no Aegis row. It has the three route-native candidate rows (ORB MNQ, Striker MYM, Vanguard MGC). *Recommend:* add no column now (the ledger's form is its owner's, §2.6 "deliberately small"). At T17, whichever rows the owner process moves to live cite the activation's `size_vector_sha256` in their existing `deployment` cell. The book-level record stays REC-8's session record.

**Drafted 2026-10-11:** the ADR addendum for D-A (option A) and D-P5-2 is appended to the [admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#addendum-2026-10-11--the-books-size-vector-in-ef-and-the-deployment-go-proposed) as PROPOSED, awaiting Joshua's ratification.

## 5. Forbidden

- Writing any vector value, P&L or account identifier into any record.
- Copying the private startup bytes into the repo.
- Writing REC-3 to REC-8 before their checklist step. Each record is an output of its step, never a prediction of it.
- Editing a frozen card, or editing an ADR without Joshua's ratification.

## 6. Audit hooks (runnable)

```bash
# REC-1 present on main. Expected: 1 or more.
git grep -c 139919cd1a20961b660c57527fa45c6b811124d468cfc97a3dd161db4d54c271 origin/main -- docs/briefs/pre-registration/
# Workers lack governance.author. Expected: the worker grant list without it.
sed -n '/^  worker:/,/grantable/p;/^  worker:/,+3p' scripts/seat_authority.yml
# T6's EF composition today names no sizing component. Expected: no match on the T6 row.
grep -n "T6 TB-B7" docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md | grep -ci "size_vector\|sizing"
# The ledger has no Aegis row (D-P5-3). Expected: 0.
grep -ci aegis ops/venue_editions/Tradeify_Select_100K.md
```
