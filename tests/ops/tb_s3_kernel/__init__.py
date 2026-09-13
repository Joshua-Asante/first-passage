"""Executable kernel model of the TB-S3 rail-extension spec (test-only reference).

Spec: ``docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md`` (rev 5.4, PR #360).

The package models §1 of the spec — the account-state table, the sticky account-wide
blocks, the three execution primitives (``CLOSE`` / ``AMEND`` / ``ATTACH``), evidence
currency, L-2 capability gating, the daemon's action-class emission gates and the
feed-loss / daemon-loss timers — against a fake broker whose only capabilities are the
L-2 items the spec names. Nothing here is production code; TB-I3 implements the real
rail against this reference, and every review finding on the spec becomes a test here.

Deliberately not modelled (owned elsewhere): the sizing laws (R-Q, the sizing host's own
reference), the bar-time barrier order (RC-5), the session calendars and closure overlay
(R-G), the settled protection mode (R-L), duplicate suppression (TB-I4), the adapters and
their checkpoints, and the arm interlock; ``size`` is injectable so cases use the spec's
public quantities directly.
"""
