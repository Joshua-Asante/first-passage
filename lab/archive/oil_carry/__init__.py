"""Helios USOIL-carry F1 mechanism probe (lab/analysis stage).

CONCEPT-USOIL-CARRY-001 — does conditioning on WTI futures-curve backwardation
separate forward returns from contango, or is it a disguised long-oil trend
trade? F1 is the cheap, pre-registered mechanism falsifier that gates whether
Helios ever earns a codify -> sweep -> validate pass.

Data source (Joshua-authorized 2026-06-06, after the brief's named EIA/FRED
sources were both unreachable from the build sandbox — EIA no-key/403, FRED
blocked/000): Databento GLBX.MDP3 CME crude-oil futures, continuous calendar
contracts CL.c.0 (front) and CL.c.1 (second). The calendar roll matches EIA's
"Contract 1 / Contract 2" definition the brief specified; CL.c.0/CL.c.1 IS the
real futures curve, not a spot proxy (forbidden move #5 satisfied).
"""
