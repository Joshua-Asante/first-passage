# MSL P2 packet C — execute exactly

**Packet:** C — `tv_static_equity` · **Branch:** `cursor/msl-tooling-pC`
**Umbrella:** `docs/briefs/handoffs/2026-08-12-cursor-fleet-msl-tooling-umbrella.md`

1. Run the umbrella **§3c Phase-0** commands first. If the no-op condition fires, write
   `CURSOR_RETURN.md` with `DONE` citing the commit and stop.
2. Read umbrella §0 (Rule 0), §0.5, §3c, §5, §6 in full.
3. Implement **only** the §2 / §3c footprint for packet C (shared util + tests + fixtures).
4. Run acceptance tests; commit on your branch; push; open a PR (`MSL P2 W-C …`).
5. Write `CURSOR_RETURN.md` with exactly one of `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`.

Do not write SESSIONS/STATE/plan/ADRs/Pine. Do not edit `score_cell.py`. Do not implement packets A or B.
