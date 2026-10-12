# Live size-vector wiring: decision packet for Joshua

**Date:** 2026-10-11 · **Base:** `origin/main` `7db42f1` · **Prepared by:** the live-wiring lane (single writer), for the Deployment Coordinator ("Portfolio deployment coordination") to relay. **Status:** **RULED 2026-10-11.** Joshua, 2026-10-11 (about 17:15Z): "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended". Recorded here and at each owner: J-1 in the ADR addendum (now Accepted); J-2 in the P-L1 and P-L2 cards' §11 G-1; J-3 in R-SV; J-4 in the cards' dispatch gates; the §5 defaults in the owners this lane writes (the cards and the three proposals). Three owner records outside this lane still owe a pointer (§7). P-L1, P-L2 and P-L3 are a **candidate freeze** (§6). The freeze is effective on the coordinator's countersignature. None is dispatched: the J-4 build gate is not open. *Update 2026-10-12 (successor Deployment Coordinator):* the freeze at `8a8d7a0` is countersigned and J-4 is amended (§6a): the build gate opens once #792 merges. The frozen cards' Status and gate lines predate both; §6a governs where they differ.

**Sources:**
- the [scope note](2026-10-11-live-size-vector-wiring-scope.md);
- the cards [P-L1](../briefs/handoffs/2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md), [P-L2](../briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md) and [P-L3](../briefs/handoffs/2026-10-11-live-size-vector-p-l3-emulator-parity-card-DRAFT.md);
- the proposals [P-L4](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md), [R-SV](2026-10-11-r-sv-live-route-size-vector-requirement-PROPOSAL.md) and [P-L5](2026-10-11-p-l5-size-vector-records-packet-PROPOSAL.md);
- the [ADR addendum](../adr/2026-09-12-tradeify-book-protection-instance-admission.md#addendum-2026-10-11--the-books-size-vector-in-ef-and-the-deployment-go-proposed);
- the [personal-clearance plan](2026-10-11-personal-clearance-plan-tradeify-book.md) (#785).

Vectors are bound by hash only:
- Tradeify r3d: `139919cd…c271`;
- personal R1 tuple: `62d7ae19…671f`;
- declared book (identity): `dc9200a2…1fea`.

No private value was read.

## Your four rulings, at a glance

| # | Decision | Recommendation | Ruling |
|---|---|---|---|
| **J-1** | Ratify the PROPOSED ADR addendum: D-A (a GO field) and D-P5-2 (sizing as an EF shared component) | **Yes**, for the Tradeify instance. The personal GO mirrors it under clearance-plan row 2.7 | **Yes** |
| **J-2** | Code admission (G-1) for the P-L1 and P-L2 edits to bound code | **Yes**, exactly as bounded in §2 | **Yes** |
| **J-3** | D-SV-1: how the private sizing file reaches the daemon | **An explicit FILE source** (path plus SHA-256) on the instance's host volume, operator-placed. A mismatch or a missing file boots disarmed. No default | **Yes** |
| **J-4** | The build gate and the activation gates (§4) | **Yes to the coordinator's rule**, with my three conditions | **Yes** |

The §5 decisions were ruled "rest as recommended": every recommendation in §5 is now the ruling.

## 1. J-1: ratify the ADR addendum

**What it does** (Tradeify instance only):
- EF's shared-component proof at B7 (T6) covers sizing: the deployed vector's hash must equal the vector FBR qualified.
- The deployment GO gains a tenth field, `size_vector_sha256` (T10). It is still a closed set, and the reseal rule is unchanged.
- T11 adds one check: the GO hash must equal the owner's stamped hash at boot. A mismatch, or a missing or unreadable stamp, boots disarmed.

**What it doesn't do:** choose a vector. It also leaves `dd_protection`, the registry row, the fingerprint recipe, Pine, ports and arming rules untouched. It works for GO and NO-GO alike, because the declared book is the identity vector (`dc9200a2…`).

**Wording** (from the addendum): "I ratify the 2026-10-11 addendum to the protection-instance admission ADR at commit `7db42f1`: sizing as an EF shared component, the GO's tenth field `size_vector_sha256`, and the T11 stamp check."

**What it unblocks:** the P-L4 amendments fold into TB-I3 S1 at its freeze, rather than a later S3 slice.

## 2. J-2: code admission for the P-L1 and P-L2 bound-code edits

| Packet | File | Functions edited | Why it is bound | Closure status (re-verified at `7db42f1`) |
|---|---|---|---|---|
| P-L1 | `ops/c1_rail/book_sizing_context.py` | `BookSizingBinding`: one optional last field, `size: LegSize \| None = None`. `_identities`: refuses a size that is not this leg's (`size_binding_mismatch`). `size_book_request`: passes `size=` to `entry_quantities` and `add_quantity`. One import name (`LegSize`) | A trust-domain runtime dependency (`trust_domain.py:163`). A TB-I1 policy-fingerprint component (`policy_fingerprint.py:29-32`), so the edit **moves that fingerprint** | **Not** in the Stage-1c measured closure (68 measured / 63 staging) or the P7 D8 list (40 paths). The successor screen's H′ and the running screen are untouched |
| P-L2 | `ops/c1_rail/book_account_owner.py` | `_validate_binding`: requires `size_vector` and does a canonical round trip. `_binding_record`: stamps `size_vector` and `size_vector_sha256`, with the encoder imported inside the function. Boot transition: both keys immutable; a legacy record without them reads as identity, for comparison only. `_context`: passes `size=vector.leg(leg_id)` | Bound as `listener_account_owner` (`trust_domain.py:146`; `composition_fixture.py:83`) | **Not** in either closure. #780's hunks (`:1651-1736`) don't overlap these sites |
| P-L2 (unbound) | `ops/c1_rail/book_incident_irm_live_page.py` | The synthetic page's binding gains `IDENTITY_SIZE_VECTOR` | Not bound | Not in either closure |

**What the admission permits:**
- exactly those edits;
- two one-key fixture additions (`tests/ops/test_book_account_owner.py`, `tests/ops/test_four_leg_runtime.py`);
- new test files.

The seal, trust-domain, composition, image-manifest and policy-fingerprint suites must pass **unchanged**.

**What it does not permit:**
- any edit to `book_policy.py` (it is in both closures; an edit would move H′);
- any module-level global in a bound module;
- schema or table changes;
- any other bound file;
- private values;
- dispatch, arming or deployment.

P-L3 (`book_bundle_execution.py`) is unbound and needs no admission.

## 3. J-3: D-SV-1, private sizing delivery

**The constraint.** Spec R-J (iii) keeps every non-`.py` port-root file out of the daemon image. `effective_inputs.json` already has the same problem, so whichever mechanism is chosen is shared by both files.

**Recommendation.** It is R-SV as proposed, applied per instance:
- **Reference.** Each instance's daemon config names `{"sizing": {"kind": "FILE", "path": …, "sha256": …}}`. The declared book is `{"kind": "IDENTITY"}`, written explicitly.
- **No default.** An absent `sizing` key refuses at boot.
- **Placement.** The operator places the file on that instance's persistent volume. The values never enter the repo or an image layer.
- **Checks.** The loader verifies the SHA-256 and then `validate_size_vector`. It then checks the hash against the expected value from the GO (J-1). A missing file, a digest mismatch, a non-canonical encoding or an expected-value mismatch **boots disarmed**: no risk-add, and a CRITICAL log naming the gate.

**Alternatives rejected:**
- *An R-J amendment putting the file in the image:* private values in a layer, and the image digest changes with the vector.
- *A secret store:* a new provider dependency.

## 4. J-4: build gate and activation gates

**The coordinator's rule.**
- **BUILD** P-L1 and P-L2 when **either** the Tradeify successor screen returns GO **or** the personal clearance study (Q-SFCLEAR-1: #752 or its re-scoped ID) returns **RESOLVED** (FALSIFIED or AMBIGUOUS does not open it) (clearance plan §9 "#773 personal-lane dispatch should follow clearance RESOLVED").
- **ACTIVATE** each lane's frozen vector only under its own gate:
  - **Tradeify:** screen GO, plus Tradeify arming (M1 `RESOLVED`, the T10 GO with the J-1 field, the per-session GO).
  - **Personal:** Q-SFCLEAR-1 RESOLVED, plus ADR 10-09 owed items 3–7, plus the 2026-10-11b one-account-at-a-time rule, plus the two-way switch check (outgoing account flat, no working orders, no delayed-entry path).

**My view: agree.** The code is lane-neutral. P-L1 and P-L2 carry *a* vector; the per-instance binding names *which* one. Building on either gate costs nothing for the other lane, and a NO-GO on Tradeify should not strand the personal lane (#785). Three conditions:

1. **Building is not binding.** Merged code changes nothing live: every live binding must name its own vector (P-L2 D-1, no default). A lane can only ever stamp its own hash: Tradeify `139919cd…` (or identity on NO-GO), personal `62d7ae19…`. Nothing in P-L1 or P-L2 lets one lane's gate activate the other's vector.
2. **The personal hash must use the same formula.** The R1 tuple's hash has to be `sha256(canonical_json_bytes(sizing))` over a mapping that `validate_size_vector` accepts. If the personal rung uses a quantity law a `LegSize` cannot express (clearance plan §3.3 port-replay rungs), P-L1 and P-L2 do not carry it, and that lane needs its own card. **I could not verify this:** `62d7ae19…` is not in the public repo. The clearance-study owner should confirm it at the 1.1 freeze.
3. **The queue still decides when P-L2 runs.** `book_account_owner.py` has one writer at a time: GC-5-DISPLACED, then TB-I3 S2, then P-L2/P4/P-SW (#785 §8). GC-5 and TB-I3 S2 are both unbuilt at `7db42f1`. *Recommend:* P-L2 may take the file as soon as GC-5 merges, if TB-I3 S2 is not yet dispatched. Run the queue in order of readiness, still one at a time. P-L1 and P-L3 are not in that queue.

The personal lane also needs clearance-plan row 2.2 (tier and instance parameterization). P-L1 and P-L2 do not supply it.

## 5. The remaining open questions (recommended defaults)

| Source | Question | Owner | Recommendation |
|---|---|---|---|
| Scope Q1 / P-L2 D-1 | Is the vector required, with identity stated explicitly? | Joshua | Yes |
| Scope Q2 / P-L2 D-4 | Caps, tiers and risk basis beyond the vector | Joshua | A T16 equality item (Tradeify), and the 1.1 freeze (personal). Not in P-L2 |
| Scope Q3 | A leg that floors to 0 | Joshua | Keep its adapter running and refuse at sizing (`zero_size`), as in replay row Z7 |
| P-L1 D-2, P-L3 D-3 | The cards' §0.5 defaults | Coordinator | Confirm |
| P-L2 D-2 | Order on `book_account_owner.py` | Coordinator | GC-5 first, then by readiness (§4 condition 3) |
| P-L2 D-3 | Legacy records read as identity, for comparison only | Coordinator | Confirm |
| P-L3 D-1 | Build P-L3 at all? | Coordinator | Yes. It is about half a day, needs no admission, and keeps rehearsals from sizing at declared quantities |
| P-L3 D-2 | Executor | Coordinator | A Claude worker, to keep one writer for the lane. No @codex unless Joshua asks |
| P-L4 D-B | Fold A-1 to A-4 into TB-I3 S1, or add an S3 slice | Coordinator | Fold, if J-1 is ratified before the TB-I3 freeze |
| R-SV D-SV-2 | Sizing file content | Coordinator | Tradeify: the whole v2 startup policy (`53dea292…`). Personal: the clearance study's frozen sizing artifact |
| P-L5 D-P5-1 | E1 replays the v2 startup policy | Coordinator (F1) | Yes. Name the v2 artifact by digest in the F1 freeze inventory |
| P-L5 D-P5-3 | Venue-ledger row | Coordinator | No new column. Rows that go live at T17 cite the hash |
| P-L4 / plan 2.7 | Personal GO field | Joshua (admission owner) | Mirror J-1 in the personal GO definition |

## 6. After your rulings

1. **Freeze.** I prepare the freeze revision of P-L1, P-L2 and P-L3. Each card is re-anchored to the freeze base (#780 shifted `book_account_owner.py` lines), and its §11 gates are recorded with your words and time. The lane directive exists only in chat, and the committed-handoff rule does not count a chat-only direction. So the freeze takes effect when the coordinator commits the delegation or countersigns the revision SHA reported to it.
2. **Dispatch proposal.**
   - **P-L1:** first, as soon as the J-4 build gate opens.
   - **P-L2:** when the J-4 gate and the `book_account_owner.py` queue both allow it.
   - **P-L3:** after P-L1 merges, parallel with P-L2.
   - Every packet goes to a Claude worker, CC-solo, never GLM. Merges go through the coordinator relay on your word.
3. **Cards for a GO.** P-L4 folds into TB-I3. R-SV is carried into the live route packet, which is written instance-parameterized (clearance plan 2.8). P-L5 runs as a coordinator checklist.

### 6a. Countersign request (to the Deployment Coordinator)

**Asked:** countersign the freeze of P-L1, P-L2 and P-L3 at **`8a8d7a077915548eb6e1bb5006d256959900f0af`** (freeze base `origin/main` `7db42f1`). Or, instead, commit the 2026-10-11 lane delegation. Either one makes the freeze effective. Neither one dispatches anything: the J-4 build gate (§4) and the §7 blockers still apply.

**What the revision holds:**
- Joshua's J-1 to J-4 rulings, recorded in each card's §11 G-1.
- The fixes from the #788 independent review (VERIFIED WITH CAVEATS; no blockers).
- No code changes. `fp check` passed on the tree that became `8a8d7a0`: status completed, exit 0, source stable. The record is `.cache/fp-verification/20261012T000251Z-9829e0ede340/record.json`, in the lane's cloud session.

**Checks before signing** (each should give the result shown):

```bash
# The card bytes are unchanged since the revision. Expected: no output.
git diff 8a8d7a0 HEAD -- docs/briefs/handoffs/2026-10-11-live-size-vector-p-l*.md
# The card form and authority blocks. Expected: well-formed; 0 violations.
for f in docs/briefs/handoffs/2026-10-11-live-size-vector-p-l*.md; do python -I scripts/check_brief.py "$f" --type cc_handoff; python -I scripts/check_handoff_authority.py "$f"; done
```

**How to record it.** Option (a): commit the line below into this section, on #788's branch or on `main` after the merge. Option (b): commit the delegation into the coordinator's synthesis record (the campaign record or `docs/SESSIONS.md`), naming the lane, its single writer, and that freeze authority covers P-L1, P-L2 and P-L3.

> **Countersigned** `<YYYY-MM-DD HH:MMZ>` by the Deployment Coordinator ("Portfolio deployment coordination"): the freeze of P-L1, P-L2 and P-L3 at `8a8d7a0` is effective. Dispatch stays under J-4 and §7.

> **Countersigned** `2026-10-12 00:34Z` by the Deployment Coordinator ("Portfolio deployment coordination"): the freeze of P-L1, P-L2 and P-L3 at `8a8d7a0` is effective. Dispatch stays under J-4 and §7.
>
> **Operator confirmation and J-4 amendment** (Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "confirm J-1 to J-4; amend J-4: the F1 acceptance opens it"). J-1 to J-4 are confirmed as recorded. **J-4 amended:** the build gate also opens on Joshua's acceptance of the FLOOR-HALF successor screen's risk into T15's F1 (NO-GO-evidence-UNDETERMINED-dependent, confirmed "confirm A" 2026-10-12T00:12Z; recorded in PR #792), in addition to a successor screen GO or the personal clearance study RESOLVED. That acceptance is recorded, so the J-4 **build** gate opens once #792 merges. It is lane-neutral: activation of either lane's vector stays under §4, unchanged. §7 blockers still apply and dispatch remains a separate act.
>
> **Freeze of record and dispatch** (successor Deployment Coordinator, 2026-10-12; Joshua reconfirmed directly the same day: "confirm A and J-4 amendment"). The freeze of record is `8a8d7a0`, not `4edf564`. The cards' G-2 lines ("frozen … at the commit that adds the Status line"), their Status lines ("Not dispatched: the J-4 build gate … is not open") and their G-3 gate text predate the countersignature and the amendment; the cards stay frozen and this section governs where they differ. Every dispatch prompt cites this section and #792's merge commit, names a fresh worktree and branch unique to the worker, and forbids reusing one in use.

**Not asked:** the merge of #788, which stays Joshua's word through the coordinator relay; any dispatch; and the §7 items owed by other owners, which are listed for relay only.

## 7. Blocking now

- ~~**The coordinator's countersignature** of the freeze revision, or a committed delegation (§6 item 1).~~ Done 2026-10-12 00:34Z (§6a).
- **GC-5-DISPLACED and TB-I3 S2 are unbuilt.** Today they hold P-L2 behind them in the `book_account_owner.py` queue.
- **The personal R1 tuple's hash formula and encoding are unconfirmed** (§4 condition 2).
- ~~**The build gate itself is not open.** Neither the screen GO nor Q-SFCLEAR-1 RESOLVED has happened.~~ *2026-10-12:* the amended J-4 gate opens on #792's merge (§6a).

**Owed by other owners (coordinator relay; not blocking the freeze):**
- **Clearance plan** (#785): row 2.7 should record the personal GO mirror of J-1 (§5, last row). `:308`'s queue text (GC-5-DISPLACED → TB-I3 S2 → P-L2/P4/P-SW) should read "GC-5 first, then by readiness, one writer at a time" (P-L2 D-2).
- **TB-I3 interlock card** (DRAFT): a back-pointer to the P-L4 D-B fold ruling, for its freezing coordinator.
- **STATE decision index:** a 2026-10-11 row for the ADR addendum's ratification (J-1 to J-4).
- **Live route packet** (clearance plan row 2.8): it must name which process holds the GO and the owner database. Today the GO is baked into the listener image only, and R-SV's daemon-side expected-value check assumes otherwise (R-SV §2.3).

## 6b. Owner-file order amendment (2026-10-12)

Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "1 yes, 2 yes", on the coordinator's packet.

- **(1) P-L2 ahead of GC-5-DISPLACED and TB-I3 S2.** P-L2 may take `book_account_owner.py` before GC-5-DISPLACED and TB-I3 S2. Grounds (coordinator readiness return, 2026-10-12, read-only at `ebd84e4`): the dependency is single-writer serialization only. GC-5 stamps its takeover mode on the `Reserve` record (`book_account_owner.py:1827`), not in `_binding_record` (`:108-136`), so P-L2 §9's shared-seam premise (`:274`) does not hold; P-L2's edits (`:108-136`, `:431-439`, `:458-460`, `:1575-1581`) do not overlap GC-5's or S2's. This amends P-L2's gate text (constraint `cut_after_p_l1_and_gc5_merged_one_writer_queue`, §0(a), G-3, D-2) to: cut after P-L1 merged, one writer at a time on the owner file. The card stays frozen; this entry governs where it differs. GC-5 and S2 re-anchor after P-L2 (their bases are stale anyway). One uncertainty carried: GC-5's D5 boot-halt site is unnamed; if it lands in boot next to P-L2's edits, GC-5 re-anchors there.
- **(2) Run-path card A before GC-5-DISPLACED.** Card A (dispatched) and GC-5 both edit `book_capacity.py` `_reserve` (`:163-196`) and `book_policy`; card A goes first and GC-5 re-anchors after it. Only one writer is active (GC-5 is not dispatched).

## 6c. P-L2 amendment: legacy reading extended; takeover owner admitted (2026-10-12)

Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "extend (E), admit book_takeover_owner.py", on the coordinator's packet after P-L2's Phase-0 stop (§0(g): with the two keys added, 30 migration-fixture tests refuse at the same-session check `book_account_owner.py:427`; the fixtures retain their binding in the booting session).

- **(E) extended.** A retained record that lacks **both** size-vector keys is read as the identity vector's mapping and hash, computed inline, at three comparisons: the cross-session check (as ruled), the same-session check (`book_account_owner.py:425-427`), and the takeover plan's `admission_binding` checks (`book_takeover_owner.py:110-111`, `:560-581`). Every pre-P-L2 owner sized at identity, so this reads a fact.
- **Still refused:** a record with exactly one of the two keys; a legacy record when the live vector is not identity (sizing changed within the session); any other difference. No default vector in `_validate_binding`; absence on a live binding remains a refusal (card §5 unchanged).
- **Admission extended (G-1):** `ops/c1_rail/book_takeover_owner.py` (trust-domain dependency, `trust_domain.py:164`; not a TB-I1 fingerprint component), its two comparison sites only. The J-2 admission otherwise stands. Fixtures stay untouched (card §2.4).
- **Added acceptance:** legacy same-session passes; legacy versus non-identity live vector refuses; one-key record refuses; migrated legacy `pending_takeover` plan passes; mutant "any key-less record matches anything" is killed.
- The card stays frozen at `8a8d7a0`; §6a, §6b and this entry govern where it differs.

## 6d. Owner-file order amendment: P4 and P-SW ahead of GC-5 and TB-I3 S2 (2026-10-12)

Joshua, 2026-10-12, directly to the Deployment Coordinator, verbatim: "2 extend", on the coordinator's decision plan (extend §6b so P4 and P-SW go ahead of GC-5 and TB-I3 S2).

- After P-L2 (#805, merged `143a61a`), `book_account_owner.py`'s writer order is **P4 → P-SW → GC-5-DISPLACED → TB-I3 S2**. GC-5 and S2 serve the deferred Tradeify route ([route record](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#addendum-2026-10-12-later--tradeify-support-strategy-logic-must-be-native-for-evaluation-accounts)); they re-anchor after P-SW.
- One writer at a time, each cut from `main` after its predecessor merges, is unchanged. P4 still builds on `2cfb3d7` or later and preserves #780's routing.
- Not checked: whether P4's or P-SW's edit sites overlap GC-5's or S2's. Re-anchoring absorbs any overlap; no card is changed by this entry.
