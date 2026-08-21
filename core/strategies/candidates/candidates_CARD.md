# candidates

**Family:** candidates
**Disposition:** MIXED — see per-file note below (Phase A cold-store body stays FALSIFIED_PARKED)
**Body:** `core/strategies/_archive/candidates/`

## Live candidate (not yet hash-pinned)

- `expiry_oi_strike_convergence_mgc_v0_1.pine` — MSL-S4 (`expiry-oi-strike-convergence` on MGC),
  G0 FROZEN 2026-08-21, `pine_lint` PASS 13/13. Authored in an ephemeral cloud session and sent
  directly to the operator rather than committed — see
  `lab/analysis/c1/msl_s4_mgc_2026-08/RUNBOOK.md` §The Pine file for why (avoids the
  unrecoverable-pin-bytes failure mode `check_pine_manifest.py` exists to catch) and the exact
  placement + hash-pin steps owed on a durable local checkout. **Not yet in
  `MANIFEST.sha256`** — pin it from the machine that holds the file, never from a cloud session.

## Hash pins

- _(none — the Phase A cold-store body has none; the live candidate above is intentionally
  unpinned pending a durable-machine pin)_

## ADR

- `docs/adr/2026-08-04-strategy-coldstore-phase-a.md`
