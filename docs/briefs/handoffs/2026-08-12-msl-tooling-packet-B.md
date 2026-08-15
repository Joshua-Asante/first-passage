# MSL P2 packet B — execute exactly

**Packet:** B — `msl_score` · **Branch:** `cursor/msl-tooling-pB`
**Umbrella:** `docs/briefs/handoffs/2026-08-12-cursor-fleet-msl-tooling-umbrella.md`

1. Run the umbrella **§3b Phase-0** commands first. If the no-op condition fires, write
   `CURSOR_RETURN.md` with `DONE` citing the commit and stop.
2. Read umbrella §0 (Rule 0), §0.5, §3b, §5, §6 in full.
3. Implement **only** the §2 / §3b footprint for packet B (adapter + tests + fixtures).
4. Run acceptance tests; commit on your branch; push; open a PR (`MSL P2 W-B …`).
5. Write `CURSOR_RETURN.md` with exactly one of `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`.

Do not write SESSIONS/STATE/plan/ADRs/Pine. Do not implement packets A or C. Adapter only — no new MC.
