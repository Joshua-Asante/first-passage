# Live size-vector wiring: scope (read-only)

**Date:** 2026-10-11 · **Base:** `origin/main` `b5571a9` · **For:** the Deployment Coordinator ("Portfolio deployment coordination") · **Status:** a scoping note. It authorizes no build, admission, dispatch or freeze.

**Question.** If the FLOOR-HALF successor screen returns GO, the live path must size orders with the same frozen vector that the screen tested, not with today's declared-book quantities. P-S1 to P-S3 (#762, #763, #764, all merged) carry the vector through qualification only ([build card](../briefs/handoffs/2026-10-10-t00-successor-screen-build-card-DRAFT.md) §3.1). The card's S-1 says: "The live rail does not pass a vector, so its behaviour is unchanged."

**Private inputs not read** (cloud-safe run): the r3d startup policy v2 bytes, the vector values (Q1 options sheet), ports and `effective_inputs.json`. Nothing below depends on them.

## 1. Live code paths that compute order quantity

| # | Site | What it does today | Vector? |
|---|---|---|---|
| L1 | `ops/c1_rail/book_sizing_context.py:255-262` (`size_book_request`) | Entry: `entry_quantities(...)`; add: `add_quantity(..., confirmed_base)`. Neither passes `size=` | **No**. This is the live book sizing law |
| L2 | `ops/c1_rail/book_account_owner.py:1812-1820` (`dispatch`) → `_context` `:1555-1590` | Builds `BookSizingBinding` from `self.binding` (`:1575-1581`), calls L1, reserves `decision.qty_out`; refuses `zero_size` at `:1819` | **No**. The binding has no vector field (`_validate_binding` `:458`) |
| L3 | `book_account_owner.py:1747-1760` (takeover) and close/flat (`:1934`), `book_protection_owner.py` brackets | Reuse a stored or filled quantity; they do not size | n/a |
| L4 | `ops/c1_signal_daemon/book_bundle_execution.py:158-169` | Offline single-bundle emulator (not a sender, `:1-6`); same two calls, no `size=` | **No**. It is the parity/emulator surface |
| L5 | `ops/c1_rail/c1_sizing_host_reference.py:296-400` (`process_signal`, qty `:368-382`, add `:398`), used by `c1_rail_listener.py:372` | The legacy single-leg (M1 test strategy) law, using `BASE_RISK` × DD scale × lifecycle | Out of scope. It is not the book, and `BASE_RISK` is locked |
| L6 | `c1_sizing_host_reference.py:276-294` (`process_book_signal`) | Delegates to L1 and always returns `submit=False` | Inherits L1 |
| ref | `ops/c1_rail/qualification/replay.py:612-616` | `size_vector.leg(k)` passed as `size=` to both calls | The **reference** live must equal |

Offline and compatibility-only callers stay as they are: `book_policy.py:574` (`leg_quantities`), `:624`/`:633` (`quantity_table`), and `qualification/prepare_compute.py:46`.

**Live state.** No production code constructs a `BookAccountOwner`. The only non-test boot is the synthetic IRM page (`book_incident_irm_live_page.py:105`). `c1_rail_listener.py:81-91` is the offline Phase-2 seam. So nothing is live yet. The host that will build the owner's binding is TB-I3-HOST's `book_host.py`, which is unbuilt.

## 2. Where the frozen vector enters

- **Canonical object (configuration as code).** The vector already has one canonical source: the `sizing` mapping in the signed r3d startup policy v2. It is parsed by `production_source.parse_startup_policy` (`:180-211`), which calls `validate_size_vector` (`book_policy.py:398`). Live config must **reference** that artifact by path, startup-bytes SHA-256 and `size_vector_sha256`. It must never hold a copy of the values. The host loader reuses the same parser and validator; it does not reimplement them.
- **Identity and version binding.** Add `size_vector` (a `SizeVector`) and `size_vector_sha256` to the owner's required binding keys (`_validate_binding` `:458`). Stamp both in `_binding_record` (`:108-136`), and add both to the cross-session `immutable` tuple (`:431-433`). A changed vector across sessions then refuses as "unverified runtime binding transition"; within a session it is already refused (`:427`).
- **Validation at the consumption boundary.** `_validate_binding` recomputes `sha256(canonical_json_bytes(size_vector.as_mapping()))` with `qualification/contract.py:266`, which is already a trust-domain runtime dependency. It refuses a mismatch with the declared hash and never trusts the declared hash alone. `_context` (`:1575`) passes `size_vector.leg(leg_id)` into `BookSizingBinding`. L1 passes it as `size=` to both calls, exactly as `replay.py:612-616` does. The field is required, with no `None` default (Q1 below).
- **Activation proof.** Equality must hold along one chain: the screen authority's `parameters.expressions.size_vector_sha256` (bound by `screen_authority.py:401-432` to r3d's bytes) = the hash in the deployment GO artifact = the hash recomputed by the host loader from the referenced r3d bytes = the hash stamped in the owner's `runtime_bindings` record. That check belongs in TB-I3's `deployment_go.validate` and the boot gate. It is read back after restart at T17 ("effective runtime activation, not merely a config write").

## 3. Bound, locked and admission-gated files

- **Bound qualification code (edit needs a G-1-style operator admission):**
  - `book_account_owner.py` is bound as `listener_account_owner` (`trust_domain.py:146`; `composition_fixture.py:83`).
  - `book_sizing_context.py` is a trust-domain runtime dependency (`trust_domain.py:163`) and a TB-I1 policy-fingerprint component (`policy_fingerprint.py:29-32`), so an edit moves that fingerprint.
  - Seal, trust-domain and composition suites must stay green, and the edit adds no module-level global (protection-health card `:80`, `:136`).
- **Avoid:** `book_policy.py`. It sits in the P7 measured closure (GC-5 card `:62`). An edit after H′ "defines a new H′ and repeats §7 step 1" (build card §4). No `book_policy.py` change is needed, because `size=` already exists.
- **Closure premise, resolved 2026-10-11:** the measured-closure script at `b5571a9` gives 68 measured / 63 staging, with `book_sizing_context.py` and `book_account_owner.py` in neither set. The public P7 D8 list (40 paths) names neither file. So P-L1 and P-L2 do not move H′. Each card re-checks this in its Phase 0.
- **Locked and untouched (any need for these is a stop):** `DD_TRIGGER`, `DD_SCALE` and `CANDIDATE_SCALE`/`require_policy` (`book_policy.py:99-115`); `BASE_RISK`; lifecycle multipliers; Pine; ports; `effective_inputs.json`; `book_adapters.py`.
- **Not bound:** `book_runtime.py`, `c1_rail_listener.py` and `book_bundle_execution.py` are not in the trust domain (protection-health freeze check, `:7`). The plan does not need to edit `book_runtime.py` or `c1_rail_listener.py`.

## 4. Collisions with in-flight work

| Work | Status at `b5571a9` | Shared files | Consequence |
|---|---|---|---|
| Protection-health ([card](../briefs/handoffs/2026-10-03-protection-health-admission-card-DRAFT.md)) | FROZEN, building | `book_account_owner.py` (occurrence disposition near `:1694-1729`), `book_protection_owner.py`, `book_runtime.py`, `c1_rail_listener.py` | P-L2 shares `book_account_owner.py`. "No two live packets share a file" (umbrella `:245`), so P-L2 is cut after it merges |
| GC-5-DISPLACED ([card](../briefs/handoffs/2026-10-03-gc5-displaced-takeover-switchoff-card-DRAFT.md)) | DRAFT, unbuilt (`AEGIS_TAKEOVER` absent) | `book_policy.py`, `book_capacity.py`, and the `book_account_owner.py` `__init__`/`boot` seam plus binding-record stamping (`:116`) | Same seam as P-L2. Serialize, and use one stamping pattern for both resolved values |
| TB-I3 synthetic interlock ([card](../briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md)) | DRAFT; `deployment_go.py` absent | §2.7: `deployment_go.py` (new), `c1_rail_arm.py`, `c1_rail_http_server.py`, the Dockerfile/`.dockerignore`/`c1_image_validation.sh` lines, and `book_account_owner.py` (S2 latch only); `policy_fingerprint.py` is read only | P-L4's GO and gate amendments fold into its S1 ([proposal](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md)). S2 shares `book_account_owner.py` with P-L2, so the two are ordered at freeze |
| TB-I3-HOST ([card](../briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md)) | FROZEN 10-06 | `book_host.py` and `tests/ops/test_book_host.py` only; its §5 *forbids* `book_account_owner.py`, `daemon.py`, `book_runtime.py` and `deploy/**` | None. It injects an already-bound loop, so the loader belongs to the live route packet (corrected 2026-10-11; [proposal](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md) §1) |

## 5. Packets

Every packet is CC solo, because each one touches sizing (build card §5 bars GLM for sizing). Codex review is fine.

| Packet | Write footprint | Red-first tests | Effort | Roadmap slot |
|---|---|---|---|---|
| **P-L1** sizing-context seam | `book_sizing_context.py` (a `BookSizingBinding.size: LegSize` field passed as `size=` at `:256-262`); `tests/ops/test_book_sizing_context.py` | A non-identity `LegSize` changes `qty_out` to replay's value for the same inputs; Striker `adds=OFF` gives add 0; a leg at 0 gives qty 0, so the owner refuses `zero_size` | 0.5 d | Before CP-6 (behaviour-changing frozen work; T15 prerequisite) |
| **P-L2** owner binding | `book_account_owner.py` (`_validate_binding`, `_binding_record`, `immutable`, `_context`); `tests/ops/test_book_account_owner.py` | Missing vector refused; hash mismatch refused; vector change across sessions refused; dispatch `qty_out` equals `BookReplay` for one synthetic action script under a synthetic non-identity vector; trust-domain, seal and composition suites unchanged | 1 d | After protection-health and GC-5; before CP-6 |
| **P-L3** emulator parity | `book_bundle_execution.py` (`SizingInputs.size`); its tests and the parity suite | Emulator quantities equal L1 and replay under the same vector | 0.5 d | With P-L2 (T16 equality evidence) |
| **P-L4** config and activation | TB-I3 interlock S1 amendments A-1 to A-4 (`deployment_go.py`, arm, boot gate), plus R-SV for the unwritten live route packet (loader and stamp read-back); see the [proposal](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md) | SV1–SV6: GO field shape; refusing default stamp; stamp ≠ GO → disarmed; stamp = GO → armed positive control; arm evidence; no real values | 1 d | T16 (bind configuration, prove equality), exercised at T17 |
| **P-L5** records | Venue edition rows and the release inventory carry `size_vector_sha256` (no values) | Docs check | 0.25 d | T16 |

The total is about 3.25 CC days. None of it is needed on NO-GO.

Draft build cards: [P-L1](../briefs/handoffs/2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md) · [P-L2](../briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md).

## 6. Open questions for Joshua

1. **Required or defaulted vector live?** *Recommend:* required. The declared book binds `IDENTITY_SIZE_VECTOR` explicitly, so every live binding states its vector and its hash.
2. **Is the vector hash enough for equality?** The replay sized with per-request cap 80 and paper capital (`production_source.py:197-210`). Live uses the binding's `cap_allocations` and `risk_dollars`. *Recommend:* P-L2 binds the vector now. T16 adds an explicit equality item, or a ruled permitted difference, for caps, tiers and the risk basis.
3. **Legs floored to 0.** *Recommend:* keep the adapter running and refuse at sizing (`zero_size`), as in replay Z7. Not running the adapter is a separate runtime behaviour that the screen did not test.
4. **The private vector on the rail host.** The §60 read surface covers ports and `effective_inputs.json`, not the r3d startup policy. *Recommend:* rule that the r3d startup bytes may be deployed to the host as a private artifact referenced by hash.
5. **Admission.** *Recommend:* one G-1-style admission naming P-L1 and P-L2's bounded edits to `book_sizing_context.py` and `book_account_owner.py`, with `book_policy.py` excluded.
6. **Timing.** *Recommend:* author the cards now and dispatch the builds after screen GO. They must still land before CP-6, so a GO late relative to F1 is a schedule risk worth naming now.
