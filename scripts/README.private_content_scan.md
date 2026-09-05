# Private-content scanner — deferred prototype

Split from PR #302 at `a6d281784db3006e8f3d8019bf2b9055eefdbcfe` on the operator's
2026-09-05 instruction. The Python module and tests are preserved byte-for-byte.
This draft is independent of the campaign documentation PR. It is not a required
gate, a prerequisite for local research, or authorization to publish private data.

The scanner matches selected representations of private fields against Git objects.
A CLEAN result is not proof that a publication contains no private information:
derived values can disclose their source, and arbitrary reversible encodings are
outside a finite pattern matcher's guarantee. Do not use it as the sole control.

The recorded 22 review rounds and four panel runs remain in the
[source history](https://github.com/Joshua-Asante/first-passage/blob/a6d281784db3006e8f3d8019bf2b9055eefdbcfe/docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md).
No further scanner review or implementation is in the active campaign budget.
Before this draft becomes merge-ready, its owner must define a finite supported
input/publication contract and verify it with synthetic fixtures. The former
serialization-independent no-disclosure claim is withdrawn.

Local regression command: `python -m pytest -q tests/test_private_content_scan.py`.
Passing these tests verifies those fixtures only. The campaign population packet
uses a separate, explicit publication review; its private working files stay local.

Split verification on Windows / Python 3.12.14: **57 passed, 5 skipped, 1 failed**.
`test_a_multiline_value_is_caught_across_added_lines` expected a CELL hit but
received CLEAN (2026-09-05). This reproduced defect is left with this deferred
draft; neither the test nor the implementation was changed to make it pass.
