# Sentinel gate-audit — forbidden-D-test log

**Purpose.** The safety audit trail for the Sentinel's quarterly LLM gate. One row per
forbidden-D-test the gate was tempted by and refused (e.g. "signal-to-noise is high",
"fits my model", "known mechanism"). Mirrors `rule-2-trip-log.md` — one table, not a
subsystem. Tier-1 (`make sentinel`) does not write here; the quarterly LLM probe does.

| Date | Run | Forbidden D-test tempted | What it would have deleted | Disposition (retained + routing) |
|---|---|---|---|---|
