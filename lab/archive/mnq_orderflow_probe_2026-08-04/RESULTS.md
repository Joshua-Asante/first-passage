# `MNQFLOW-1` — RESULTS: depth imbalance does not predict the next minute; route 2's first swing is a clean null

> ⚖ **RULED 2026-08-05 (operator-delegated) — read the standing before citing anything below.**
> This executed the **blind-discovery** PREREG (`3fb10a3`), which does **not** clear Avenue A §6
> (condition 3, *"survivor-tied … not blind discovery"*, is a shape requirement the $0 entitlement
> cannot satisfy — §1's own triple declined to claim limb 3). The ruling
> ([governance note §7](lab/archive/../../../docs/notes/2026-08-05-order-flow-probe-governance-question.md)):
> the run is a **recorded deviation, not retroactively ratified** (the M1 Addendum 2026-07-31b
> instrument); the `FALSIFIED` verdict stands **as a measurement, quarantined to the MNQ.md DEAD
> list** — never a gate-cleared route-2 discharge; the **K spend (MNQ 4→5) stands unconditionally**
> (executed looks bank); the **depth census stands as a durable finding** and transfers to the
> sanctioned thread as mandatory disclosed context; and **§5's re-proposal bar below is RE-SCOPED
> to blind re-proposals only** — it does **not** bind the sanctioned re-aimed probe
> ([`mnq_orb_flow_substrate_2026-08-05/PREREG.md`](lab/analysis/c1/mnq_orb_flow_substrate_2026-08-05/PREREG.md)),
> whose pull sign-off remains a separate, unbundled operator GO.

**Status:** FALSIFIED — V2 fired as pre-registered most likely: the observable book carries no
directional information at the 1-minute horizon. Spearman ρ **−0.01205** on n=1,167 RTH pairs is
**wrong-signed** against a hypothesis that predicted positive, and sits at the **36.7th percentile**
of its own within-day-shuffled null (p_emp **0.633** one-sided as frozen; two-sided on |ρ| 0.681).
The first order-flow modality probe in the estate returns nothing.

**Date:** 2026-08-05 · **Pre-registration:** [`PREREG.md`](PREREG.md) — frozen at **`3fb10a3`**
before any MBP-10 outcome existed.

> **Freeze-hash lineage (read before auditing the freeze ordering).** `3fb10a3` was later **reset
> off its branch** and is contained by no mainline ref; it survives on **`rescue/mnqflow-1-scaffold`**,
> created expressly to keep the freeze commit reachable. Its content was cherry-picked onto this
> branch as **`c62ff7b`**, which is **byte-identical** over the probe directory — verifiable with
> `git diff 3fb10a3 c62ff7b -- lab/archive/mnq_orderflow_probe_2026-08-04/` (empty). So the
> ordering proof reads `c62ff7b` (freeze) → `f6376bd` (results) on this branch, and `3fb10a3` is
> the original freeze object. **Do not delete `rescue/mnqflow-1-scaffold`** without first
> confirming `3fb10a3` is reachable from some other ref, or this citation becomes unverifiable.
**Cost:** **$0.00** — every window re-estimated before pulling and priced at `$0.0000` under the
standing subscription. **K_intrinsic = 1 spent and banked**; manifest
[`mnqflow_depth_imbalance.json`](lab/archive/../../../discovery_manifests/mnqflow_depth_imbalance.json)
closed (0 of 1 survives; Bonferroni and BH-FDR agree). `K_banked(MNQ)` **4 → 5** (disclosure, not
a gate, per [ADR 2026-08-04](lab/archive/../../../docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md)).
**No `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.**

---

## 1. Verdict — the frozen gates, evaluated literally

| § | Route | Frozen trigger | Actual | Fired? |
|---|---|---|---|---|
| V5 | `AMBIGUOUS-UNDERPOWERED` | n < 500 | n = **1,167** | ✗ |
| **V2** | **`FALSIFIED`** | **p_emp ≥ 0.05** | **p_emp = 0.633** | **✓** |
| V1 | `RESOLVED (diagnostic)` | p_emp < 0.05 ∧ ρ > 0 | neither limb holds | ✗ |

The null is not merely un-beaten — the point estimate has the **wrong sign**. §1 predicted
bid-heavy books precede *up* minutes; the measured association is weakly negative and lands in
the middle of the shuffle distribution.

| | value |
|---|---|
| Minute pairs (389 × 3 days) | **1,167** |
| Observed ρ | **−0.012047** |
| Null mean / sd | −0.002498 / 0.028941 |
| Null p05 / p95 | −0.049278 / +0.044739 |
| Observed percentile in null | **36.7th** |
| p_emp (one-sided, frozen) | **0.633** |
| I mean / sd | +0.00975 / 0.14026 |
| r_next sd | 6.399 bp |

## 2. The census is the second finding — NQ's displayed book is too thin to carry a fine signal

| | value |
|---|---|
| Total 10-level depth, both sides (p05 / p50 / p95) | **40 / 67 / 94 contracts** |
| Distinct I values in 1,167 observations | **525** |
| Observations inside a tie group (>1) | **78.1%** |
| Exactly I = 0 | 68 (5.8%) |

NQ front-month shows a **median 67 contracts across all twenty price levels** — roughly 3.4 per
level. A ratio built from small integers is coarse by construction, so `I` is heavily tied and
carries far less information than its continuous definition suggests. This does not rescue the
null (a coarse feature can still rank-correlate, and the placebo is computed on the same tied
values, so the comparison is fair) — but it does bound what any 10-level size-imbalance feature
can resolve on this instrument, and it is the number a successor should argue against first.

## 3. What this run required beyond the frozen scaffold — disclosed, not smoothed over

The scaffold was frozen but had never been run. Three things stood between it and a verdict, and
each is recorded because each could have changed a number:

1. **Recovery.** The freeze commit `3fb10a3` had been reset off its branch and was reachable only
   via reflog; its working tree, including the compressed panels, was gone. Recovered by
   cherry-pick into an isolated worktree. The ~2.3 GB MBP-10 DBN cache was untouched, so every
   panel was rebuilt at **$0.00** — nothing was re-purchased.
2. **The compressor could not have finished.** The committed per-record loop took **8m50s on the
   smallest 866k-record chunk**; a 20M-record RTH day was out of reach. A vectorized path was
   added and **pinned byte-identical against the reference loop on real MBP-10 bytes**
   ([`test_compress_equivalence.py`](test_compress_equivalence.py)). It independently reproduces
   the 391-minute count the original compressor produced for 07-28.
3. **An adversarial review of the frozen spec and harness raised 30 findings; 11 survived
   independent verification** (8 MAJOR, 3 MINOR). All were fixed in **code**, never by editing the
   frozen PREREG. The load-bearing one:

   > **S2's RTH window was enforced nowhere in code** — it lived only in the pull command. Because
   > databento filters on `ts_recv` while records carry `ts_event` up to **70 ms earlier**, a
   > sliver of pre-open records (**15 on 07-28, against ~103,000 in a real minute**) landed in an
   > **09:29** bucket that sits outside the frozen 09:30–16:00 window. Every day's panel was
   > shifted one minute early. Fixed at the single chokepoint both load paths share.

   Also fixed: the gate branch let `V2` absorb the region `p_emp < α ∧ ρ ≤ 0`, which satisfies
   **no** frozen §6 row (now `UNASSIGNED-BY-SPEC`, and pinned by a region table); the census
   copied the `WINDOWS` constant instead of measuring the loaded panel; `load_windows` read an
   entire parquet purely to sniff its layout, and silently accepted a raw record dump down a
   second code path; S1's instrument/schema (`NQ.v.0` / `mbp-10`) was asserted nowhere; a
   refuse-to-emit guard now covers databento's UNDEF price sentinel (verified **absent** from all
   three windows — the guard is a no-op here and exists so a future cleared book hard-stops
   instead of producing a plausible-looking finite mid); §10's audit hook
   `python test_run_flow_probe.py` executed **nothing**, the file having no entrypoint (added —
   and note no vacuous "tests green" attestation was ever made here, because the suite was run
   under `pytest` from the outset); and S1's input was pinned by **nothing but a filename**, where
   both sibling probes hash-pin and assert. Since this probe's input is a derived panel and
   `data/` is gitignored, a **content digest** is now computed per window and emitted in the
   census, so every run attests to the exact bytes it measured.

   **Declared non-move:** the RTH repair was applied **before** the run, as spec compliance. The
   counterfactual verdict on the un-repaired panel was deliberately **not computed** — that would
   be a second look at the data under FM-1/FM-3. Three of 1,170 candidate minutes were excluded;
   the verdict rests on the single frozen execution.

**Test state:** **22 unit tests green** before the runner read a real bar (6 original + 16 added
for the repairs), plus **3 compressor-equivalence tests against real MBP-10 bytes**. The review
noted the original suite covered none of `load_windows`, `load_minute_parquet`, or `run` — the
three functions holding the defects; all three are now covered.

**Panel digests (SHA-256 over index + depth/price columns; emitted by every run):**

| window | digest |
|---|---|
| `nq_mbp10_2026-07-28.parquet` | `16b6cd1f36248b3c6af7c7e8a6fd825bd28c431f7a647ca8dd75f0a4f2956664` |
| `nq_mbp10_2026-07-29.parquet` | `4f6a69959f33c3c02338527f7e709a61c6fc54fb47e2ca440523bd4d9b1965b4` |
| `nq_mbp10_2026-07-30.parquet` | `5825631902b9426ce103a961efd4f7e1708c5c9f9c1af9cddb877273b76e84e6` |

Each panel derives from **7 hour-chunked `NQ.v.0` `mbp-10` DBN pulls** (21 total) held in the
local Databento cache; `compress_mbp_minutes.py` asserts schema and symbol against frozen S1
before compressing.

## 4. What this does NOT establish

1. **Not a claim about MBP-10 as a modality.** One feature (10-level size imbalance), one horizon
   (1 minute), three days. The domain bar's route 2 is not closed by this; its cheapest swing is.
2. **Not a claim about MNQ economics.** Measured on **NQ** parent depth per proxy-discipline Rule
   4 — structural discovery only. No tick value, cost, or fill assumption was applied, and none
   should be borrowed from this.
3. **Not a power statement.** n=1,167 clears the frozen floor by 2.3×, but three days is a
   **modality shakedown**, as §1 said in advance. A longer subscription-covered panel is a
   different question — and per V2's frozen disposition, one this result does not license.
4. **No deployment implication whatsoever.** Rail disarmed, venue de-scoped, no Stage-0 opened.

## 5. Iterate — loop exit

- **Verdict used:** `FALSIFIED` (V2), the pre-registered most-likely branch. §4 called V2 most
  likely and V1 "live only if the subscription book carries a large, un-arbitraged
  imbalance→return link — not the prior." That expectation held; no defect investigation fires.
- **Model update:** route 2's first swing lands where routes 1 did. Combined with `MNQPOOL-1`
  (avoided objects recede 572 pt) and `MNQFVG-1` (consumed objects born 291 pt away), the estate
  now has **three consecutive same-instrument nulls across two different modalities**. The new
  datum is narrower but sharper than the ICT pair: at the one-minute horizon the *observable book
  itself* carries no directional information on NQ, and the depth census suggests one reason —
  there is very little book to observe.
- **Next:** **STOP** on 1-minute depth-imbalance expressions.
- **Entry packet:** n/a (STOP).
- **Stop rule / re-proposal bar (⚖ RE-SCOPED by the 2026-08-05 ruling: binds BLIND re-proposals
  only — the sanctioned survivor-tied thread is governed by Avenue A §6 and its own PREREG, not by
  this bar):** a **blind** successor on this modality re-proposes only with **(a)** a named feature
  that is not top-of-book size imbalance — the depth census above is the bar any size-derived
  feature must clear — **or (b)** a cohort-cited literature δ for a futures-native order-flow
  feature, which harvest Req 2 has never yet been supplied on this instrument. **Not** a horizon
  re-cut, a threshold on `I`, more days of the same feature, or a move to MNQ's own book to get a
  different tick grid. Either way a blind probe must **also** clear Avenue A §6, which the ruling
  reaffirmed unmodified.
- **Board write:** MNQ.md DEAD-list row + profile cell (`order-flow` mechanism, new) + session
  log; STATE decision-index line; SESSIONS entry; CATALOG regen; manifest closed. Landed with this
  commit.

## 6. Reproduce

```bash
cd lab/archive/mnq_orderflow_probe_2026-08-04
python -m pytest test_spec_parity.py test_run_flow_probe.py -q   # 22 passed
python -m pytest test_compress_equivalence.py -q                 # 3 passed (~9 min, real DBN)
python run_flow_probe.py                                         # -> RESULTS.json
```

Deterministic (seed 20260804, 1,000 within-day shuffles). Panels rebuilt from the local DBN cache
via `compress_mbp_minutes.py <out.parquet> <chunk1.dbn> ...`; vendor bytes stay local under
`data/` (gitignored). Raw [`RESULTS.json`](RESULTS.json).
