# AUDIT — GROW-lane spec v1 dual adversarial review (2026-08-22)

**Target:** `docs/spec/2026-08-22-grow-lane-generate-refine-spec.md` v1 (merged via PR #96 at
`a02126f`; reviewed at that content). **Reviews:** gate-reachability-audit workflow (38 agents)
+ pre-ratification-adversarial-panel workflow (72 agents, refute-first, 2 skeptics per finding),
both run 2026-08-22 before any ratification.

**Verdicts:** gate audit — **BLOCKED-AT-FREEZE** (tally: 4 REACHABLE+BINDING · 1 UNREACHABLE ·
23 UNBINDING · 2 UNVERIFIABLE of 30 gates; 4 BINDING BARs unreached by the door check).
Panel — **BLOCKED: do not ratify D1–D3 as drafted** (5 BLOCKERs, 4 CONCERNs).
**Disposition:** v1's D1–D3 withdrawn; spec recast same day as an extension packet to the
Accepted [deep-iteration lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md)
(v2, same path). This note is the durable record of why.

## Consolidated BLOCKERs (panel B1–B5, corroborated by the audit)

- **B1 — D3 cohort facts stale/mischaracterized.** CON-2…5 share one physical reserved CONFIRM
  window (2025-09-01→2026-08-05, MNQ); it was **read 2026-08-20** under the spent U1 override
  (CON-4 closure change history; `RESULTS_CONFIRM.md` on disk) — a D3 read would be a second
  consultation of a burned segment. CON-2's window is "virgin to selection, not to sight";
  CON-5's is "unread forever" by operator Branch-A election; the dense-1m temporal-selectivity
  pause is lane-wide unconditional as of 2026-08-20 and already binds a sibling (MSL-S2B).
  Q-OFCHAN-1/Q-R2FLOW-1 closed with zero candidates — nothing to rescue. The "reserved-but-unread"
  seed class is **empty** at the spec's own date (audit verdict G-D3-ONCE: UNREACHABLE).
- **B2 — undisclosed collision with the Accepted deep-iteration lane charter (2026-08-16).**
  Same refinement thesis, already chartered with hard controls v1 dissolves (K ≤ 33; survivor
  floor at full declared K; W4 SPA/StepM re-arm; standing-pause attestation; no double-homing;
  2-strike falsification budget, currently 1/2 after DL-1's abandonment). v1 greps for the
  charter/W4/SPA/StepM: zero hits. Unbounded disclosure-only `K_select` is the accounting move
  that doctrine complex refused, re-proposed without engagement.
- **B3 — "EM0's catalogue ≤ 3 is preserved as M ≤ 3" is an amendment presented as preservation,
  with every real owner omitted from the supersession list.** EM0 caps the *examined* catalogue
  via K_eff = K_intrinsic = catalogue size — exactly the quantity D2 unbounds. Un-named owners a
  D2 ratification would silently contradict: TNEC-1 N-EDGE (`floor_at_k(K_intrinsic)`,
  RATIFIED), EM screen §8 change control (§2 limbs change only by superseding spec), S6 /
  `admission_schema.py` (CODE_LANDED; machine-refuses K ≥ 4 at open — an honest GROW open is
  refused, a K=M registration misstates the search-space size, a bypass fires S6's own
  FALSIFIED clause), and the blind-channel ADR L208 ("A train/confirm split does not rescue a
  wide mine… Splitting is a bias control, not a K control"). Also: v1's Reads annotation
  "(blind lane; `--prereg` binding)" inverts the code's documented residual — blind opens are
  deliberately unbound (`register_search.py:357-360`).
- **B4 — route ③ door-check discharge claimed-but-unscored.** "beats-incumbent-ORB-MNQ
  net-of-cost, which the fitness function already scores" is false at HEAD: no
  incumbent-comparison term exists anywhere in the scoring code; the raised bar's route ③
  demands beats-incumbent, "not merely clears the cost floor" — which is precisely what the
  step-4 composite computes; the 2026-08-10 falsifier LOG (L78; the STATE decision-index row
  carrying it was collapsed by the same-day nav pass) records route ③ "unclearable ex ante"
  for the sibling lane. Separately (audit G-DOOR): v1's own Verify block accepted the
  `instrument_profiles.py` exit-2 FATAL as proof the door check "executes" — on that path
  `cmd_cell` returns **before** the BINDING BAR loop, proving execution without consultation.
- **B5 — no executed dedup/amend-first search output pasted (Rule 8.8/8.10).** The skipped
  search had a demonstrated material miss: it is exactly what surfaces B1's pauses and B2's
  charter (the charter's own §0 pasted its dedup grep; the standard applies to lane charters).

## Confirmed CONCERNs (carry into v2 / GROW-0 PREREG)

- **C1** Limb B kill-switch power underived: at the ≥20-panel floor a binomial envelope has
  ~13–35% power against 2–3× leakage; Limb-A failure was absent from the FALSIFIED branch;
  harness retries un-ledgered.
- **C2** Lane-wide $0.91/$0.95 cost literals are index-micro-only; MGC/MCL run $1.06/$1.10
  actual (`firm_rules.py`) — ~16% understatement on sealed-segment adjudication. Bind costs per
  instrument via the cost_model discipline.
- **C3** "20.18% → 0.00%" bust-elimination is an **EOD-clock lower-bound** figure
  (Q-EVALSEQ-1); the 2026-08-17 intraday-honest remeasure (Q-POLFRONT-1 fork) collapsed the
  related 5.107× headline. Quote only with the label.
- **C4** No cross-campaign bound on cumulative sealed consultations — each new operator family
  mints a fresh confirm budget on finite cached data; unpriced. Must be answered in any future
  two-ledger ADR.

## Gate-audit highlights beyond the panel

- 23/30 gates UNBINDING (no named mechanical executor) — including every FALSIFIED trigger of
  v1's own Gate line; per-gate one-line repairs recorded in the workflow output (session record,
  wqrh7rmp2 / wf_9040ce41-97a; panel: wa4zej465 / wf_b93a5ac4-3a9).
- Unreached BINDING BARs besides route ③: the EOD-adversity raised bar 2026-08-02 (+ ADR
  2026-07-31 §5 15:30-exit bar) is registered in **zero** profile ledgers yet binds the
  grammar's exit-geometry construct class; the CON-5 temporal-selectivity pause has no consult
  path that prints it; ORB-MNQ-1's deployment-target rejection is dedup-excluded by design so
  no attestation can return it; a fresh family id sidesteps the parked-not-DEAD
  `MNQ×opening-range-breakout` cell (adjacency consult repair).
- `rejected_candidates.md`'s tier=always enforcement claims are **stale**: `gates.yml` runs
  `instrument-profiles` path-conditional on `^ops/instruments/`, so a PREREG landing under
  `lab/` triggers no automatic consult. T3 (2026-08-10 ADR §4) ruled pre-emptively satisfied:
  the door-check limb should land in `gates.yml` with the ratifying packet, not after the first
  violation.

## Disputed items (operator judgment; v2 adopts the cheap fixes)

- Origin wording: "one admission (ORB-MNQ-1, 2026-07-16, later payability-falsified at the
  venue); none since" replaces "no promotions".
- GROW campaigns open under the charter's `--lane deep` (mechanism-first semantics), never
  `--lane blind`.
- D3 exclusion predicate: moot in v2 (D3 withdrawn; rescue routes through charter §2.1
  re-proposal-bar clearance or a U1-style per-seed override ADR).
