# MSL P2 packet A — execute exactly

**Packet:** A — `msl_preflight` · **Branch:** `cursor/msl-tooling-pA`
**Umbrella:** `docs/briefs/handoffs/2026-08-12-cursor-fleet-msl-tooling-umbrella.md`

1. Run the umbrella **§3 Phase-0** commands first. If the no-op condition fires, write
   `CURSOR_RETURN.md` with `DONE` citing the commit and stop.
2. Read umbrella §0 (Rule 0), §0.5, §3, §5, §6 in full.
3. Implement **only** the §2 / §3 footprint for packet A (evidence-only CLI + tests + fixtures).
4. Run acceptance tests; commit on your branch; push; open a PR (`MSL P2 W-A …`).
5. Write `CURSOR_RETURN.md` with exactly one of `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`.

Do not write SESSIONS/STATE/plan/ADRs/Pine. Do not implement packets B or C.
