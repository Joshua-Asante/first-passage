# R-SV: the frozen size vector in the live route packet (requirement PROPOSAL)

**Date:** 2026-10-11 · **Base:** `origin/main` `2ccb08b` · **For:** the Deployment Coordinator ("Portfolio deployment coordination"), and the author of the live route packet card

**Status:** a PROPOSAL. It is written in the shape of a [multi-leg rail extension spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) §3 row, so it can be carried verbatim into the live route packet's card when that card is written. The card is not written yet, and this note neither edits the spec nor authorizes any build.

**Parents:**
- [scope note](2026-10-11-live-size-vector-wiring-scope.md) §2;
- [P-L4 proposal](2026-10-11-p-l4-tb-i3-amendments-PROPOSAL.md) §4, which this note expands and corrects.

**Consumes:**
- [P-L2](../briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md): the owner binding's required `size_vector`, and the stamped `size_vector_sha256`.
- The P-L4 A-2 seam: `deployment_go.size_vector_reason`, with a `stamped_source` whose default refuses.

**The live route packet** is the packet that registers the book host and builds the owner. That covers R-A1, the registry and daemon boot, at spec `:144`, and R-H, restart, at `:157`. TB-I3-HOST leaves this to it (HOST card §5).

## 1. Facts this requirement is built on (read at `2ccb08b`)

- **The public expected value exists.** The successor pre-registration's values block records `size_vector_sha256` `139919cd…c271` (`docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md`). This is the hash only; the vector's values stay private. The P-L4 A-1 GO field (or option B's row provenance, D-A) carries the same value at activation.
- **There is a precedent for private inputs with public pins.** `book_adapters.load_book_adapters` (`:146-190`) reads private bytes from `port_root()` (`:98-100`). It checks them against a public compiled digest (`EFFECTIVE_INPUTS_SHA256`, `:66`) and refuses on mismatch. The owner binding then records the identity (`book_account_owner.py` `_binding_record`).
- **There is a delivery conflict.** Spec R-J guard (iii) (`:160`) requires `effective_inputs.json` "and every non-`.py` file in the port root" to be **absent from the image**. Yet `load_book_adapters` needs `effective_inputs.json` at runtime, and `deploy/c1_signal_daemon/Dockerfile` does not yet copy the port root at all. So the live packet must already decide how private non-`.py` inputs reach the daemon. The sizing artifact is a second such input. The P-L4 proposal §4 assumed the port overlay "already" carries it; it does not (§5 corrects that).
- **The config boundary.** `daemon.load_config` (`daemon.py:40`) and `build_loop` (`:80`) are where the live packet will construct the owner binding (R-A1).

## 2. The requirement row

| Id | Requirement | Owner files | Tag | Named tests |
|---|---|---|---|---|
| R-SV (A) | **Frozen size vector.** See §2.1–§2.6 below. | `ops/c1_signal_daemon/book_sizing_config.py` (new; the loader), `daemon.py` (`build_loop` binding construction), `ops/c1_rail/deployment_go.py` (the production `stamped_source` only), and the delivery files D-SV-1 selects | offline (synthetic vectors) / live (private bytes at activation) | `test_sizing_reference_required_no_default`, `test_identity_reference_is_explicit`, `test_sizing_bytes_digest_mismatch_refuses_boot`, `test_noncanonical_sizing_refuses_boot`, `test_sizing_hash_differs_from_expected_refuses_boot`, `test_loader_uses_validate_size_vector_not_a_copy`, `test_stamp_reader_returns_owner_latest_stamp`, `test_stamp_reader_missing_or_unreadable_refuses`, `test_restart_with_changed_sizing_halts_before_first_poll`, `test_activation_ack_records_stamp`, `test_no_vector_value_in_logs_status_or_errors` |

### 2.1 Configuration as code

- **Required reference.** The daemon config names the sizing source by reference only:
  - `{"sizing": {"kind": "FILE", "path": <private path>, "sha256": <hex>}}`; or
  - `{"sizing": {"kind": "IDENTITY"}}`, for the declared book.
- **No default.** An absent `sizing` key refuses at boot.
- **No inline values.** No vector value is ever written into versioned config.
- The `IDENTITY` form is the declared book stated explicitly (P-L2 D-1). It needs no file.

### 2.2 Loader (`book_sizing_config.py`)

1. For `FILE`, read the bytes at `path` and require `sha256(bytes) == sha256`. A mismatch refuses.
2. Parse the bytes as JSON, rejecting duplicate keys and non-finite values. Accept either the whole v2 startup policy (then take `doc["sizing"]` after checking `doc["schema"] == "qualification-source-startup/v2"`) or a bare sizing mapping. Which one is decision D-SV-2.
3. Call `book_policy.validate_size_vector(mapping)`. Never re-implement its rules.
4. Require `canonical_json_bytes(mapping) == canonical_json_bytes(vector.as_mapping())`. This is the screen authority's own canonical check (`screen_authority.py:427`).
5. Compute `size_vector_sha256 = sha256(canonical_json_bytes(vector.as_mapping()))`, the screen authority's formula.

### 2.3 Expected-value check (before the owner is built)

- The loader's hash must equal the expected value from the D-A owner: the baked GO field (P-L4 A-1) or the admitted row's provenance. For `IDENTITY`, it must equal `IDENTITY_SIZE_VECTOR`'s hash.
- A mismatch boots the daemon disarmed, with no risk-add and a CRITICAL log naming the gate.
- While the D-A owner holds no value (no GO, or an empty registry), every non-identity sizing refuses. This is the fail-closed default.

### 2.4 Binding

- `build_loop` passes the `SizeVector` as the owner binding's `size_vector` (P-L2 (A)). P-L2 stamps it.
- A restart with different sizing is refused by P-L2's `immutable` check, before the first poll. This sits alongside R-A1's digest halt.

### 2.5 Stamp read-back (replaces P-L4 A-2's refusing default)

- `deployment_go`'s production `stamped_source` opens the owner database **read-only**, in the `read_incidents` pattern (`book_account_owner.py` read-only open, `timeout=5`).
- It returns the latest `runtime_bindings` body's `size_vector_sha256`.
- A missing database, a missing row, a missing key or a read error refuses. It never returns a default.

### 2.6 Activation acknowledgment (D-5 activation slice) and private handling

- **Acknowledgment.** The durable acknowledgment records the stamped hash. T17's post-restart verification reads it back and compares it with the GO.
- **Private handling.** Values never appear in logs, `--status`, exception text or tests. Synthetic vectors only in tests. The bytes are delivered per D-SV-1 and never committed.

## 3. Acceptance (red-first, synthetic)

| Test | Fails if |
|---|---|
| `test_sizing_reference_required_no_default` | A config without `sizing` boots |
| `test_identity_reference_is_explicit` | `IDENTITY` does not yield `IDENTITY_SIZE_VECTOR`, or does not compare against its hash |
| `test_sizing_bytes_digest_mismatch_refuses_boot` | Bytes ≠ the declared `sha256` still load |
| `test_noncanonical_sizing_refuses_boot` | A non-canonical mapping (for example a Striker cap above its smallest encoding, or a reducible fraction) loads |
| `test_sizing_hash_differs_from_expected_refuses_boot` | Loader hash ≠ the D-A expected value, yet the daemon admits a risk-add |
| `test_loader_uses_validate_size_vector_not_a_copy` | The loader module defines its own size rules (an AST check: it calls `validate_size_vector`, and defines no `_require_canonical` or field tables) |
| `test_stamp_reader_returns_owner_latest_stamp` | The reader returns anything but the latest row's stamp |
| `test_stamp_reader_missing_or_unreadable_refuses` | A missing database, row or key, or a locked database, yields a value |
| `test_restart_with_changed_sizing_halts_before_first_poll` | A second boot in the same or next session with other sizing reaches a poll |
| `test_activation_ack_records_stamp` | The acknowledgment lacks the stamp, or the T17 read-back accepts a different one |
| `test_no_vector_value_in_logs_status_or_errors` | Any synthetic vector field value appears in captured logs, status output or exception text |

## 4. Decisions

- **RULED 2026-10-11** (Joshua, 2026-10-11 (about 17:15Z): "J-1 yes, J-2 yes, J-3 yes, J-4 yes, rest as recommended"; decision packet J-3 and §5): D-SV-1 = option (a), an explicit FILE source by path plus SHA-256 on each instance's volume, shared with `effective_inputs.json`; a missing file, digest mismatch, non-canonical encoding or expected-value mismatch boots disarmed; no default. D-SV-2 = the whole v2 startup policy (Tradeify) and the clearance study's frozen sizing artifact (personal). D-A = GO field (ADR addendum, Accepted).
- **D-SV-1 (Joshua; replaces scope note Q4). How the private sizing bytes reach the daemon.** R-J (iii) keeps every non-`.py` port-root file out of the image, and `effective_inputs.json` already faces the same constraint. Options:
  - **(a) Recommended.** A private, operator-placed file on the host's persistent volume, referenced by path and SHA-256 in the daemon config. Integrity comes from the hash and the expected-value check (§2.3), not from where the file sits. Use one mechanism for both `effective_inputs.json` and the sizing file, decided once in the live packet. Volume mutability is harmless: a changed file fails the hash and the daemon stays disarmed.
  - (b) An R-J amendment admitting named non-`.py` files into the image. This needs a spec change and a new guard. It also bakes private values into an image layer, which changes the image digest that EF2 records whenever the vector changes.
  - (c) A host secret store. This adds a provider dependency the spec does not have.
- **D-SV-2 (coordinator). File content.** The whole r3d v2 startup policy, or the bare `sizing` mapping. *Recommend:* the whole v2 policy, because its digest (`53dea292…`, pre-registration §2 A1) is already a recorded identity. The loader takes `sizing` from it, so no new artifact identity is created.
- **D-A (Joshua; from P-L4).** The expected value lives in a GO field or in the row provenance. R-SV reads whichever is chosen and works with either.

## 5. Corrections made with this note

The P-L4 proposal §4 said the sizing artifact goes "through the private overlay root that R-J already uses". R-J (iii) excludes non-`.py` files from the image, so that is not an existing path. §4 there now points to this note and to D-SV-1.

## 6. Audit hooks (runnable)

```bash
# The public expected value. Expected: one hit in the values block.
git show origin/main:docs/briefs/pre-registration/2026-10-08-tradeify-book-successor-screen-prereg-DRAFT.md | grep -c 139919cd1a20961b660c57527fa45c6b811124d468cfc97a3dd161db4d54c271
# R-J (iii) excludes non-.py port files from the image. Expected: the guard text.
grep -n "every non-\`.py\` file in the port root are absent" docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md
# The private-input pin precedent. Expected: a digest constant, and a refusal on mismatch.
grep -n "EFFECTIVE_INPUTS_SHA256 =\|do not match the accepted identity" ops/c1_signal_daemon/book_adapters.py
# The daemon does not copy the port root yet. Expected: no output.
grep -n "ports" deploy/c1_signal_daemon/Dockerfile
```
