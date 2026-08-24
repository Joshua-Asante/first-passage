# -*- coding: utf-8 -*-
"""Idempotently splice SECTION13.md into RESULTS.md and refresh the status line
+ the §7.2 reader-intercept. Safe to re-run after regenerating SECTION13.md."""
import io
import re

RES = "RESULTS.md"
SEC = "SECTION13.md"
MARK_A = "<!-- GROWTH-SECTION-START -->"
MARK_B = "<!-- GROWTH-SECTION-END -->"

body = io.open(SEC, encoding="utf-8").read().strip()
t = io.open(RES, encoding="utf-8").read()

# 1. status line -------------------------------------------------------------
OLD_STATUS = ("**Status:** **ACTIVE** — 630-cell region published, Tradeify/MFFU identical; "
              "8/8 corner-case + 3/5 MARGINAL-band validation tuples resolve clean at full N "
              "(2/5 stay MARGINAL, 0 confident-verdict flips); screens shape, not mechanisms.")
NEW_STATUS = ("**Status:** **ACTIVE** — 945-cell region published (Tradeify Select / MFFU / "
              "**Tradeify Growth**, the last added 2026-08-24); Select≡MFFU bit-identical; "
              "8/8 corner-case + 3/5 MARGINAL-band validation tuples resolve clean at full N "
              "(2/5 stay MARGINAL, 0 confident-verdict flips). ⚠ **§7.2's \"no cell at "
              "win_rate ≤ 50% is FEASIBLE\" is scoped to the $3,000 rope and does NOT hold for "
              "Growth's $3,500 rope — see §13.** Screens shape, not mechanisms.")
if OLD_STATUS in t:
    t = t.replace(OLD_STATUS, NEW_STATUS, 1)
    print("status line: updated")
elif NEW_STATUS in t:
    print("status line: already current")
else:
    raise SystemExit("!! status line anchor not found -- refusing to guess")

# 2. §7.2 reader-intercept ---------------------------------------------------
OLD_72 = ("**2. No cell at win_rate ≤ 50% is `FEASIBLE`, for any shape, cadence, or EM2 risk "
          "level tested.**")
NEW_72 = ("**2. No cell at win_rate ≤ 50% is `FEASIBLE`, for any shape, cadence, or EM2 risk "
          "level tested.**\n⚠ **SCOPED 2026-08-24 — true for the $3,000 Select/MFFU rope only.** "
          "`Tradeify_Growth_100K`'s $3,500 rope makes `mild_right_skew`/cd2/$250 `FEASIBLE` at "
          "`win_rate=50%` (bust 1.17% at the full frozen N). Read this claim as a property of the "
          "rope, not of the venue class — see §13.2.")
if OLD_72 in t:
    t = t.replace(OLD_72, NEW_72, 1)
    print("§7.2 intercept: inserted")
elif "SCOPED 2026-08-24" in t:
    print("§7.2 intercept: already present")
else:
    raise SystemExit("!! §7.2 anchor not found -- refusing to guess")

# 3. splice the section ------------------------------------------------------
block = "%s\n\n%s\n\n%s" % (MARK_A, body, MARK_B)
if MARK_A in t:
    t = re.sub(re.escape(MARK_A) + r".*?" + re.escape(MARK_B), block, t, flags=re.S)
    print("§13: replaced in place")
else:
    t = t.rstrip("\n") + "\n\n---\n\n" + block + "\n"
    print("§13: appended")

io.open(RES, "w", encoding="utf-8", newline="\n").write(t)
print("RESULTS.md written")
