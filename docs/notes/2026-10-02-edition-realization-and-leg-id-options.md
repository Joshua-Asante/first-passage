# Edition realization and leg identity: options and their cascade (2026-10-02)

**Status:** OPTIONS ONLY. This note proposes **no scheme** and recommends no option. It traces what each choice touches in the public code, so the operator can answer the edition identity rows in one sitting. Ticket O (coordinator dispatch, 2026-10-02), deliverable 2. *2026-10-02: the operator ruled A1 + B1 for ORB and Vanguard (one shared successor settings file), A2a + B1 for Striker, and rejected A2b (operator ruling 2026-10-02 (sitting 2)). This note remains the options record.*

**Serves:** the identity-binding rows and the realization paragraph in the [ORB/Striker successor §5](../briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md#5--identity-binding-fills-at-freeze) and the [Vanguard successor §4](../briefs/pre-registration/2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md#4--identity-binding-filled-at-freeze), the [Aegis skeleton](../briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md) §4, and gates G1a / G2a of the two [production](../briefs/handoffs/2026-09-26-orb-striker-edition-production.md) [handoffs](../briefs/handoffs/2026-09-26-vanguard-fixed-stop-edition-production.md).

**Reads (Rule 0, `origin/main@bd30646`):** the files cited by line below; the [ORB R2 supersession ADR](../adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md); the [venue-edition ledger](../../ops/venue_editions/Tradeify_Select_100K.md); [rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) R-B2 (B). No private Pine, port or effective-input file was read. Nothing was executed.

## 1. The two choices

**Realization, per leg:**
- **A1 — override-only.** The Pine and port bytes are unchanged. Behaviour changes through a successor effective-settings file.
- **A2 — code edition.** New port bytes. A2 has two variants:
  - **A2a:** a new Pine and a new port that embeds the new Pine identity. This is the production handoffs' plan.
  - **A2b:** the unchanged Pine, and a new port that still declares the old Pine identity. The loader accepts A2b, but the port then no longer ports that Pine. No public owner adopts or excludes A2b.

**Leg identity, per leg:**
- **B1 — keep** the current `leg_id`.
- **B2 — renew** it: a new `leg_id`, with the old one retired and never reused. The precedent is `dj30_mym` / `nas100_mnq` (`book_policy.py:199`; rail spec R-B2 (B); ledger lines 15–16).

**What the public record already constrains:**

| Leg | A1 available? | Source |
|---|---|---|
| ORB | Yes: trailing is disabled by input override | ORB/Striker successor §D; production handoff §2 |
| Vanguard | Yes: trailing is a single on/off input, and VAN-4 needs no code change | Vanguard successor §3a, §4 |
| Striker | Not per the public record: STR-1 removes the delayed-attach path | Production handoff §7 ("n/a (new port)"), §4 |
| Aegis | Not established: the source mapping is owed | Aegis skeleton §3a |

**Owners' standing conditions.** Both successors and both handoffs already say:
- the loader requires the port's embedded `PINE_SHA256` to equal the registry Pine identity;
- override-only is admissible only with unchanged compatible identities and explicitly bound effective settings;
- loader checks are never weakened.

## 2. Cascade through the named surfaces

| Surface | Where | A1 (override-only) | A2 (code edition) | B2 (renew `leg_id`) |
|---|---|---|---|---|
| **`BOOK_LEGS`** | `book_policy.py:179-199`; leg-keyed law branches at `:273`, `:295`, `:304-306`, `:312`, `:376` | No change | `pine_sha256` changes under A2a; A2b keeps it | New `LegSpec` id; the old id moves to `RETIRED_LEG_IDS`; every leg-keyed branch must follow, or the sizing law silently changes or fails closed. `lifecycle_key` is a separate field (see §3) |
| **`ADAPTERS` and the loader** | `book_adapters.py:38-62`; checks at `:122` (runtime digest), `:137-139` (`LEG_ID`), `:140-142` (`PINE_SHA256`); port path from `module` (`:104`) | `pine_sha256` and `runtime_sha256` unchanged | `runtime_sha256` changes; `pine_sha256` changes under A2a; `module` changes if the port file is renamed (the handoffs name new files), independently of `leg_id` | New id. **Unchanged port bytes declare the old `LEG_ID`, so A1 + B2 fails `:137-139` (and the qualification check at `:335`) under the current loader.** |
| **`L1_BASE_ENTRY_LEGS`** (ORB only) | `replay.py:31`, used at `:34-35` and `:553` | No change | No change | Must name the new id. Otherwise RC-9's one-bar cancel silently re-applies to the ORB edition's base entry, contradicting §59 Rulings 6 and 7(a). `replay.py` is the `replay_kernel` freeze-inventory module (`trust_domain.py:141`) |
| **`LEG_ORDER`** | `book_runtime.py:27-28`; exact key tuple required at `book_evaluate_loop.py:21`; barrier slots at `book_runtime.py:390-398`; bar body at `:50` | No change | No change | Derived from `BOOK_LEGS` priority, so the contents change and the order does not. Persisted runtime state keyed by the old id (`c1_rail.book_migration`; fixtures under `tests/fixtures/book_migration/`) needs a migration decision |
| **ORB R2 ADR scope** | [ADR](../adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md) scope line 10; §0 pin of `phase1_config.json` `orb_mnq_recon_v7` Pine `176c4f70…` (line 26); §2 grounds include ORB parity records (line 40); "Retain-until: … registry row is retired" (line 11) | The §0 identities still match, but the evaluated behaviour is trailing-free. The ADR does not say whether "ORB-MNQ recon v7" names the Pine identity or the configured leg | Under A2a the §0 Pine pin no longer identifies the evaluated ORB | The ADR names no `leg_id`. Renewal leaves its text intact but bears on which "registry row" Retain-until means |
| **Runtime digest** | `EFFECTIVE_INPUTS_SHA256` (`book_adapters.py:66`, checked at `:152-153`); `RUNTIME_EFFECTIVE_INPUTS_SHA256` (`:72`, derived at `:157-168`); qualification binding `contract.effective_settings_sha256` (`:226-230`, `trust_domain.py:130`) | The qualification loader binds a successor file through the contract without a code change (`:226-230`). **The runtime loader (`load_book_adapters`) needs both constants re-pinned, or a loader change, in a reviewed change, so A1 is not code-free at runtime.** The file holds all four legs keyed by `leg_id` (`:155`, `:234`), so the digest is **book-wide**: two A1 legs share one successor file | Unchanged only if the settings are unchanged **and** the new port's `build()` takes the same adapter keywords (`:175`, `:337`); otherwise a successor file is needed | The keys change, so the digest changes even with identical values. The ORB derivation and checks key on the id (`:162-163`, `:240`; `qualification/execution/admission.py:190`) |

## 3. Further surfaces the same choices reach

| Surface | Where | Reached by |
|---|---|---|
| **Qualification identity:** role → leg maps and the exact four-pin rule | `trust_domain.py:25-26`, `:103-119`; `runtime_inventory.py:28-33`; `model.py:11`; `contract.py:46`; `book_adapters.py:318-319` | A2 (pins); B2 (ids) |
| **Accepted historical pins**, including runtime ports and the Step 3 / Step 6 admissions | `contract.py:32-44` | A2 |
| **Historical admission binding.** The accepted Step 3 port digests must equal the domain's port pins; the Step 6 bundles are `O-N`, `O-P`, `S-*` | `production_source.py:622-623`, `:714-718` | **A2 fails `:717` unless new admission evidence or a reviewed identity-contract change exists.** For Striker, which is A2 only, this is unavoidable. B2 changes the alias keys |
| **Export parity:** leg → phase-1 source id; the port must declare its leg and Pine pin; exact parity with the captured export | `book_parity.py:38-43`; `tests/ops/test_book_adapters_parity.py:64-69`, `:75` onward | A2a has no export of the new Pine. **An export of an edition Pine is backtest output on the edition. Before freeze, §R bars agents from producing it, and any such output triggers the pre-registrations' no-amendment-after-output rule (§7), so A2a parity evidence can only follow freeze.** A1's captured-settings parity is unchanged but does not cover the trailing-free settings. B2 changes the map key |
| **Core identity table:** (`leg_id`, `lifecycle_key`, root) | `core/firm_rules.py:620-625` | B2 (a `core/` edit) |
| **Lifecycle:** `lifecycle_key` passed with tiers keyed by `leg_id` | `book_account_owner.py:1551-1552`; [strategy lifecycle](../methodology/strategy_lifecycle.md) | B2 with a new `lifecycle_key` would be a new authorization entry; B2 with the old key splits id and key |
| **Other leg-keyed branches** | `book_capacity.py:181`, `:392`; `book_takeover_owner.py:107` (Aegis as taker); `book_bundle_intake.py:84`; `book_bundle_execution.py:48`; `production_source.py:76`, `:96-98`, `:728`; `qualification/benchmark.py:54-107` | B2 |
| **Manifests and ledger:** `BOOK_SOURCES.sha256`, `PORT_MANIFEST.sha256`; ledger `CANDIDATE` rows say "no live leg_id" | `core/strategies/`; ledger lines 20–22 | A2 (manifests). B1 or B2 decides which id the ledger later records |
| **Tests and persisted fixtures** | More than a hundred files under `tests/` name the four ids, including `tests/fixtures/book_migration/` | B2 |

## 4. Combination summary

All four combinations, without ranking:

- **A1 + B1.** Pins unchanged. One book-wide successor effective-settings file, with both registry constants re-pinned. No new admission evidence for the port. Open questions: the ORB R2 scope reading, and whether captured-settings parity suffices for trailing-free behaviour.
- **A1 + B2.** Not loadable under the current loader (`book_adapters.py:137-139`, `:335`). It needs new port bytes, which makes it A2, or a separately reviewed identity-contract change. The successors forbid weakening the loader.
- **A2 + B1.** New pins and possibly a new `module`. New historical admission evidence, or a reviewed identity-contract change. Post-freeze parity for A2a. Every id-keyed surface unchanged.
- **A2 + B2.** Everything in A2 + B1, plus every id-keyed surface in §2–§3, a retired-id entry, and a migration decision.

Legs may differ. Striker is A2 by its rule set. A1 for ORB and Vanguard together would share one successor settings file.

## 5. Decisions this leaves with the operator

None is answered here.
1. Per leg: A1 or A2, and under A2 whether A2b is admissible.
2. Per leg: B1 or B2, and under B2 the new `lifecycle_key` or the old one.
3. Under A2: new Step 3 / Step 6 admission evidence or a reviewed identity contract, and the post-freeze parity ordering.
4. Whether the ORB R2 ADR's scope covers the ORB edition as written, or needs its owner's amendment before TB-D1 fills it.
5. Under A1 for more than one leg: one shared successor settings file and its sequencing.
