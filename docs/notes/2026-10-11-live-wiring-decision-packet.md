# Live size-vector wiring: decision packet for Joshua

**Date:** 2026-10-11 · **Base:** `origin/main` `7db42f1` · **Prepared by:** the live-wiring lane (single writer), for the Deployment Coordinator ("Portfolio deployment coordination") to relay. **Status:** **RULED 2026-10-11.** Joshua, 2026-10-11 (about 17:15Z): "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended". Recorded here and at each owner: J-1 in the ADR addendum (now Accepted); J-2 in the P-L1 and P-L2 cards' §11 G-1; J-3 in R-SV; J-4 in the cards' dispatch gates; every §5 default in its owner. P-L1, P-L2 and P-L3 are **frozen** (§6). None is dispatched: the J-4 build gate is not open.

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
- **BUILD** P-L1 and P-L2 when **either** the Tradeify successor screen returns GO **or** Q-SFCLEAR-1 resolves (#752; clearance plan §9 "#773 personal-lane dispatch should follow clearance RESOLVED").
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

1. **Freeze.** I freeze P-L1, P-L2 and P-L3 under the committed-handoff rule. Each card is re-anchored to the freeze base (#780 shifted `book_account_owner.py` lines), its §11 gates are recorded with your words and time, and the freeze SHA is reported to the coordinator.
2. **Dispatch proposal.**
   - **P-L1:** first, as soon as the J-4 build gate opens.
   - **P-L2:** when the J-4 gate and the `book_account_owner.py` queue both allow it.
   - **P-L3:** after P-L1 merges, parallel with P-L2.
   - Every packet goes to a Claude worker, CC-solo, never GLM. Merges go through the coordinator relay on your word.
3. **Cards for a GO.** P-L4 folds into TB-I3. R-SV is carried into the live route packet, which is written instance-parameterized (clearance plan 2.8). P-L5 runs as a coordinator checklist.

## 7. Blocking now

- **Your rulings J-1 to J-4.**
- **GC-5-DISPLACED and TB-I3 S2 are unbuilt.** Today they hold P-L2 behind them in the `book_account_owner.py` queue.
- **The personal R1 tuple's hash formula and encoding are unconfirmed** (§4 condition 2).
- **The build gate itself is not open.** Neither the screen GO nor Q-SFCLEAR-1 RESOLVED has happened.
