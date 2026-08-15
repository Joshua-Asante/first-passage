# Q-USOIL-1 — CLOSURE: `CLOSED` / `SUBTRACT` (expired PARK; GSUB-1 b4)

**Verdict:** `CLOSED` — GSUB-1 **SUBTRACT** (expired PARK with no renewal case). Not a formal
edge `FALSIFIED` on the regime-capture path; the spike-fader mechanism was separately REJECTED
earlier ([ADR 2026-06-14](../../adr/2026-06-14-reject-usoil-rdm-spike-fader.md)).
**Closed:** PARKED 2026-06-15 · park re-confirmed 2026-07-10 · **SUBTRACT ratified 2026-08-09**
(GSUB-1 Phase 3) · lab body archived 2026-08-09/11
**Pre-registration / parent (inquire brief, historical):**
`git show pre-prune-2026-08-08:docs/ltm/briefs/Q-USOIL-1-regime-capture-counterbalance.md`
**Spend / K:** advisory Gate B-3 DSR fail informed the park; native cert + battery not spent ·
GSUB-1 $0 / K=0
**Live effect:** none — USOIL not in the book; does **not** bar oil/energy generally (live route =
MCL instrument-lane intake, `ops/instruments/MCL.md`)
**Artifacts:** [`pursuit b4`](../../pursuits/b4-q-usoil-1.md) ·
[`CARD`](../../../lab/analysis/usoil_regime_capture/CARD.md) ·
[`archive README`](../../../lab/archive/usoil_regime_capture/README.md) ·
[`GSUB-1 closure`](GSUB-1-closure-resolved-loadbearing.md) ·
[`operator-retirements-record`](../../notes/2026-07-10-operator-retirements-record.md)

> **Records-completeness note (2026-08-11).** CATALOG stamps CLOSED / GSUB-1 SUBTRACT residual with
> no joinable closure under `docs/briefs/closures/` or `docs/ltm/briefs/`. The pre-prune inquire
> brief still said PARKED — restoring it alone would mis-label the terminal disposition. This stub
> reconstructs the **ratified** disposition from b4 + GSUB-1 + CARD — **reconstructed-from-partial-record**
> only in the sense that no dedicated closure was filed at SUBTRACT time; the pursuit record is
> complete.

---

## 1. Verdict (against the recorded disposition path)

| Route | Trigger (as recorded) | Actual | Fired? |
|---|---|---|---|
| Gate B / edge RESOLVED-PROCEED | DSR + §9 H1 recovery on feed-clean panel | Advisory B-3 DSR @ N=36 **FAIL** (p=0.215); operator **PARKED** rather than spend native cert (inquire brief banner, 2026-06-15) | park path |
| Formal FALSIFIED-REJECT (regime-capture) | Gate B/C fail after full battery | Battery **not run** — 0 anti-SNAG slots consumed; §9 Silver counterbalance **unanswered** | — |
| Spike-fader REJECT | separate concept CONCEPT-USOIL-RDM-001 | **Accepted** ADR 2026-06-14 | ✓ (sibling kill) |
| GSUB-1 SUBTRACT | expired PARK, 08-08 revisit lapsed, no renewal | **Ratified 2026-08-09** ([b4](../../pursuits/b4-q-usoil-1.md)) | ✓ (terminal) |

## 2. What the pre-registration predicted vs what happened

The inquire brief framed a binary Gate B/C edge + Silver §9 counterbalance test. Advisory
deflation evidence was enough for the operator to park (2026-06-15) and re-confirm the park
(2026-07-10) with an 08-08 revisit. That revisit board row was deleted at the Great Prune with no
re-park; GSUB-1 treated the lapse as expired PARK → SUBTRACT.

## 3. What this closure does NOT license

- Reading SUBTRACT as a measured FALSIFIED of the regime-capture edge (battery never completed).
- Barring oil/energy instruments or MCL intake (b4: "not a scope bar").
- Re-running Gen-1 harnesses under `lab/archive/usoil_regime_capture/` (NON-RUNNABLE after
  Gen-1 pipeline retirement 2026-07-11).

## 4. Defects found in the frozen brief (recorded, not repaired)

Inquire brief's PARK + 08-08 revisit outlived its board row — the load-bearing GSUB-1 finding
about unowned decisions. Not repaired by editing the historical brief.

## 5. Lesson candidates

Already absorbed into GSUB-1's model update (unowned parked decisions). No new lesson from this
records stub.

---

## Iterate — loop exit

- **Verdict used:** `CLOSED` / GSUB-1 `SUBTRACT` (expired PARK)
- **Model update:** terminal disposition is governance-expiry (lapsed revisit), not a completed
  Gate B falsification; the spike-fader kill is a separate, earlier mechanism reject.
- **Next:** STOP
- **Routing:** STOP — b4 carries re-entry armor (out-of-frame evidence + attached falsifier via
  ADR/governance channel). Lab body archived.
- **Entry packet:** n/a — STOP
- **Stop rule / re-proposal bar:** out-of-frame evidence plus attached falsifier through a
  governance channel (ADR or equivalent) — per b4 / ADR GRAND §2.3; not a Gen-1 harness re-run.
- **Board write:** none — STOP, nothing owed (b4 pursuit + CATALOG CLOSED row + GSUB-1 already
  filed; SESSIONS 2026-08-11g recorded lab archive).

## §10 audit-hook discharge

```bash
ls docs/briefs/closures/Q-USOIL-1-closure-subtract.md
rg -n 'SUBTRACT|Q-USOIL-1' docs/pursuits/b4-q-usoil-1.md lab/CATALOG.md lab/analysis/usoil_regime_capture/CARD.md
python3 -X utf8 scripts/check_closure_disposition.py docs/briefs/closures/Q-USOIL-1-closure-subtract.md
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-06-15 | PARKED on advisory evidence | operator |
| 2026-08-09 | GSUB-1 SUBTRACT ratified (b4) | GSUB-1 |
| 2026-08-11 | Joinable closure stub authored (records-completeness; no re-verdict) | Cursor Cloud Agent |
