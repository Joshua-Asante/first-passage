# ADR 2026-08-02 — Pepperstone feed retirement (canonical-feed status, A5/P1, and the data)

**Status:** `Accepted` — operator ruling 2026-08-02, verbatim: *"We do not need pepperstone exports, anything relying on pepperstone can be retired"*, and on scope: *"Tier 2 should ride with it"*.
**Decision date:** 2026-08-02

**Supersedes:** `2026-06-24-oanda-retirement.md` in part — its operative consequence was *"Pepperstone/TV is the **sole canonical feed**"*. There is now **no canonical CFD feed**; the live feed is CME futures. The OANDA retirement itself stands.
**Superseded-by:** none
**Superseded-in-part-by:** [`2026-08-03-bar-data-cfd-and-candidates-retirement.md`](2026-08-03-bar-data-cfd-and-candidates-retirement.md) — narrows §2-F KEEP from all of `bar_data/` to CME micros only (MYM/MNQ/6J); CFD panels deleted
**Retain-until:** none
**Completes:** [`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md) — Phase 3 emptied the executable panel registry; this ADR retires the feed the registry used to point at, and applies the Phase-5 data pattern to it.

---

## §0 — Rule 0 reads (production source, verified 2026-08-02)

| Path | What it establishes |
|---|---|
| `core/mc/modes.py:96-112` | **`PANELS_BY_BROKER = {}`** — the registry is *already empty* (Phase 3). `PEPPERSTONE_DIR` / `GUARDIAN_V56_CSV` survive as dangling constants |
| `lab/research_utils/breadth.py:86-106` | `load_baseline_panel("pepperstone")` **already raises `KeyError`**; `baseline_panel_available()` already returns `False` |
| `lab/analysis/regime/decompound_remc_2026-06-07/decompound.py:61-78` | **A5's engine reads four Pepperstone CSVs** from its own `inputs/` — A5 is fully Pepperstone-bound |
| `scripts/check_data_manifests.py:37-38` | The two Pepperstone dirs are 2 of the 5 active manifest dirs |
| `lab/analysis/c1/tradeify_book_composition_2026-07-23/` §0 | The c1 panels are **CME** (`CBOT_MINI_MYM1!`, `CME_MINI_MNQ1!`) — **no Pepperstone dependency** |
| Disk scan | `core/data/tv_exports/oanda`, `core/data/dukascopy` **absent** — the Phase-5 precedent deleted bytes, it did not merely de-scope |
| `backups/first-passage-vendor-preretirement-2026-07-22/INVENTORY.txt` | Holds only **4** Pepperstone files; this retirement covers **35** ⇒ the prior backup does **not** cover it |

---

## §1 — Context

**Nothing live depends on Pepperstone, and the code already reflects that.** Substrate Phase 3
emptied `PANELS_BY_BROKER` on 2026-07-22, so no live path can load a Pepperstone panel — the loaders
raise. Every current research and execution surface — the c1 rail, the cadence measurement, the
liveness harness, the third-leg screen — runs on **CME futures** exports. The feed's canonical
status was doctrine that the code had already stopped honouring.

**What still depended on it was a diagnostic whose subject had moved out from under it.** A5
(decompound-HOLD limb 2) monitors regime risk on the locked **CFD** book, using a feed for a
**closed venue** (CFD retirement 2026-06-30; FXIFY closed 2026-07-10), to inform allocations that
are actually executed as **MYM/MNQ venue editions on CME futures**. P1 — a fresh 4-leg Pepperstone
export, operator-owed by ~2026-08-05 — existed only to feed it.

That is the same shape as the C2→C0 quarterly revert check that **D2 retired on 2026-07-22**: its
criterion was denominated in a venue that no longer exists. The consistent disposition is
retirement, not re-export.

**Decision driver (one sentence):** the feed's only remaining consumer is a diagnostic pointed at a
book with no live execution path, so re-exporting it would buy a measurement nobody can act on.

---

## §2 — Decision

**Retire Pepperstone as a data feed, in both tiers, in one motion.**

### 2-A — Canonical-feed status

**There is no canonical CFD feed.** The 2026-06-24 OANDA retirement's *"Pepperstone/TV is the sole
canonical feed"* is superseded in part: the live feed is **CME futures TV exports**
(`core/data/tv_exports/cme/`). Historical CFD-era numbers keep their provenance labels and stay
readable as record; they gain no successor.

### 2-B — A5 and P1 are RETIRED, not deferred

- **A5** (decompound-HOLD limb 2 / `regime_gate.py --regime-check`) — **struck from Class A.** Not
  re-pointed: its panel, its instruments and its venue are all retired. `regime_gate.py` and
  `decompound.py` stay on disk as the historical record of the 2026-06-07 HOLD; they become
  **unrunnable** once the inputs are deleted, which is honest rather than a defect.
- **P1** (fresh 4-leg Pepperstone export, operator-owed ~08-05) — **struck.** No export is owed.
- **A1** (accept-beta fork) loses its stated input. It is **not** thereby decided — see §2-C.

### 2-C — A1 is re-scoped, not silently orphaned

The 08-08 packet sequences *"A1 reads A5"*. With A5 gone, **A1 may not be decided on a
Pepperstone-shaped input that no longer exists, and may not be decided by default either.** A1
carries forward as an open fork whose evidence base is now the venue-native record (Q-COMPOSE-1
breadth, fork-program exhaustion, ORB-ZB falsification, the ORB-MNQ correct-clock scorecard). Any
future A1 decision states which of those it rests on. **Inventing an A5-substitute number to close
A1 is forbidden** (§5).

### 2-D — A LIVE falsifier is orphaned by this retirement. Recorded, not papered over.

⚠ **This is the one genuinely uncomfortable consequence, and it must not be filed as a packet-row
strike.** A5 is not only a slate item — it is the executable half of the **decompound-HOLD ADR §4
limb-2**, carried on the STATE forward board as a **LIVE config-falsifier**: *re-run quarterly;
`p99 DD ≥ 5% OR bust ≥ 1%` ⇒ **HOLD FALSIFIED** → open a regime-adaptive-sizing Pre-Q + interim
k≈0.55 mitigation.* That falsifier was the **compensation** the 2026-06-07 HOLD offered for
consciously accepting regime risk on the locked config.

**Deleting its inputs makes it unable to fire.** A HOLD whose own falsifier cannot fire is
unfalsifiable, which is precisely the degeneration signature the programme-audit protocol exists to
catch (*"falsifier thresholds drifting toward 'we'd never hit this'"*). **This ADR does not claim
that is fine.**

**What is actually true, and why the disposition is still retirement:** limb-2 was **already
measuring the wrong exposure**. It scores p99 DD / bust on the **CFD** panel, while the locked
config's live expression is **MYM/MNQ venue editions on CME futures**. So the feed retirement did
not break a working falsifier — it removed the last substrate from one that had been aimed at a
dormant book since the CFD venue closed. The failure predates today.

**Disposition — the two holes are one hole:**

- The **owed forward regime monitor** (already OWED, all three original catch-paths dark) and the
  **orphaned decompound §4 limb-2** are hereby recorded as **the same obligation**. The venue-native
  successor discharges both.
- **Until that successor exists, the decompound HOLD has NO live falsifier.** That is a recorded,
  dated gap — not a silent one, and not a claim that the HOLD is safe.
- Standing constraints carry unchanged: it must **not** be pass-rate-shaped, and the both-halves
  gate must not be re-run as if the answer were unknown.
- **Limb-1** (≥2 live DD failures) is unaffected — it was already dormant for want of live fills, and
  it is feed-independent, so it survives this retirement intact.

### 2-E — Tier 2: data + manifest contract

- `core/data/tv_exports/pepperstone/` and `core/data/tv_exports/pepperstone/bar_export/` **leave the
  active manifest contract** (`check_data_manifests.py`), reducing five dirs to three.
- **The bytes are deleted from the checkout** (35 files), matching the Phase-5 precedent, which
  deleted rather than de-scoped.
- **A verified offline copy was taken first** — 35/35 hash-verified, 0 mismatches — and the hashes
  are recorded in [`2026-08-02-pepperstone-data-tombstone.md`](../ltm/notes/2026-08-02-pepperstone-data-tombstone.md).
  The pre-existing 2026-07-22 backup covered only 4 of the 35 and was **not** sufficient.

### 2-F — Out of scope, explicitly

`core/data/bar_data/` **stays** — on disk and in the manifest contract. It is derived M15 data, and
deleting it would break more than it cleans. But its **producer is now dead**
(`parse_bar_export.py` reads the deleted `pepperstone/bar_export/`), so those panels are **frozen:
usable, not regenerable** without an offline restore. Recorded rather than hidden.

---

## §3 — Alternatives considered

1. **Take the P1 export and keep A5 alive.** Rejected — it buys a regime read on a book with no live
   execution path, at manual-egress cost, to inform a fork that can be argued on venue-native
   evidence.
2. **Tier 1 only (doctrine, keep the bytes).** Rejected by the operator's scope ruling. It would also
   leave two manifest dirs whose gate can never be satisfied from CI and whose only consumer is
   retired.
3. **Delete `bar_data/` too.** Rejected — derived, still consumed by historical studies, and its
   removal was never in the authorized scope.
4. **Re-point A5 at the CME panels.** Rejected as a *rename*: the decompound HOLD is a specific
   2020–26 CFD-history result. A venue-native regime monitor is a **new** design (§2-D), not A5
   with different inputs.

---

## §4 — Falsifier (revert trigger)

**H:** nothing that still matters depended on Pepperstone.

**Revert trigger (binary):** if within **90 days** any live decision — a rail change, a lifecycle
rung move, a screen verdict, or an 11-08 §4 limb — requires a Pepperstone-sourced number that no
venue-native substitute can supply, this retirement was mis-scoped: restore from the offline copy
and re-admit the panel via a superseding ADR.

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | 90 days pass with no live decision blocked on a Pepperstone number | Retirement holds; offline copy may be considered for destruction under a separate ruling |
| `FALSIFIED` | A live decision is blocked on a Pepperstone-sourced number | Restore from offline copy; re-admit by superseding ADR; record what the venue-native substitute failed to supply |
| `AMBIGUOUS` | A *historical* citation needs the bytes for reproduction only | Restore read-only from the offline copy; **no** re-admission to the manifest contract |

**Not a falsifier:** an old study becoming unreproducible in-place. That is the accepted cost, and
the offline copy is its remedy.

---

## §5 — Forbidden moves

1. **Destroying the offline rollback copy** as part of this retirement. It is the only path back for
   bytes that were never in git, and several panels are **not re-exportable at all** (CFD venue
   closed, TV egress manual).
2. **Inventing an A5-substitute number to close A1.** A1 is re-scoped, not decided (§2-C). This is
   the *"do not invent a p99 on a stale window"* rule, extended to a window that no longer exists.
3. **Re-pointing the retired A5 at CME panels and calling it A5.** That is a new instrument wearing a
   retired one's ratified standing (§3-4).
4. **Building the owed forward regime monitor as a pass-rate.** Unchanged standing constraint —
   a challenge-denominated rate is uninterpretable with the venue closed, which is exactly why D2
   retired its predecessor outright rather than re-pointing it.
5. **Treating "no canonical CFD feed" as "no canonical feed."** CME futures exports are canonical
   for everything live.
6. **Quietly deleting `core/data/bar_data/`** under this ADR's authority. Out of scope (§2-F).

---

## §6 — Consequences

**Positive:** the manifest contract drops from five dirs to three; a diagnostic aimed at a dead
venue stops consuming operator hours; the 08-08 slate loses the A5→A1 chain that was its only
load-bearing internal sequence, so the gate collapses toward a records pass; and the owed regime
monitor is forced onto the instruments actually traded.

**Negative (real, and accepted):** several historical mechanism studies become unreproducible
in-place — `lab/analysis/legacy/xauusd_cgb_2026-06-15/` hardcodes an absolute path to a deleted CSV, and
`decompound.py` / `regime_gate.py` become unrunnable. `bar_data/` becomes frozen (§2-F). The
mitigation for all of it is the offline copy, which is exactly why §5-1 protects it.

---

## §7 — Implementation

1. Tombstone with all 35 hashes + the offline path — **done before deletion**.
2. `check_data_manifests.py`: drop both Pepperstone dirs (5 → 3).
3. Delete `core/data/tv_exports/pepperstone/` from the checkout.
4. Docs: `CLAUDE.md` canonical-feed + manifest-dir claims; `STATE.md` A5/P1 forward-board lines; the
   08-08 packet's A5/P1/A1 rows and §2 sequence.
5. **Not done here:** no deletion of `bar_data/`, no destruction of the offline copy, no A1 decision,
   no forward-regime-monitor design.

---

## §10 — Audit hooks (runnable)

```bash
# The bytes are gone from the checkout, and the manifest no longer claims them
ls core/data/tv_exports/pepperstone 2>/dev/null && echo "STILL PRESENT" || echo "deleted (expected)"
rg -n "pepperstone" scripts/check_data_manifests.py || echo "de-scoped (expected)"

# The offline rollback copy still exists and still verifies (§5-1 protects it)
ls "C:/Users/joshu/backups/first-passage-pepperstone-preretirement-2026-08-02/INVENTORY.txt"
rg -c "copy=OK" "C:/Users/joshu/backups/first-passage-pepperstone-preretirement-2026-08-02/INVENTORY.txt"   # expect 35

# A5 / P1 are struck, not merely deferred
rg -n "A5|P1 " docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md | rg -i "retired|struck"

# bar_data is still in scope (§2-F) — this retirement must not have taken it
ls core/data/bar_data >/dev/null && echo "bar_data retained (expected)"

# The registry stays empty — nothing re-admitted a panel without an ADR
rg -n "^PANELS_BY_BROKER" -A 1 core/mc/modes.py
```

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-02-pepperstone-feed-retirement.md --type adr
python scripts/check_data_manifests.py
```

## Change history

| Date | Change |
|---|---|
| 2026-08-03 | **Independent parallel retirement reconciled at merge (PR #619).** An upstream session, without knowledge of this ADR, executed the same data retirement on a second operator ruling (*"all pepperstone has been retired in light of the futures pivot"*): same SHA256SUMS deletions, own tombstone (2026-08-03), PIPELINES.md sync, and the `tests/test_check_data_manifests.py` fix this branch had missed. Reconciliation: this ADR + the 2026-08-02 tombstone are canonical (they carry the decision, the A5/P1/A1 dispositions, and the **verified offline copy** the 08-03 record did not know existed — its *"no offline rollback copy"* claim is **corrected in place** per Rule 14); the 08-03 tombstone is retained as the independent record with a correction banner; PIPELINES' *"no live restore path"* narrowed to *"no live regeneration path."* Two operator rulings, same direction, four days apart — the retirement is doubly confirmed |
| 2026-08-02 | Initial ADR. Retires Pepperstone as a feed (Tier 1) and its data + manifest dirs (Tier 2) in one motion, per operator ruling. Strikes A5 and P1; re-scopes A1 without deciding it; re-points the owed forward regime monitor venue-native. Offline copy taken and hash-verified 35/35 **before** deletion; `bar_data/` explicitly out of scope |
