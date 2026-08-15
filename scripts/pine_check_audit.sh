#!/usr/bin/env bash
# pine_check_audit.sh - re-checkable validation hooks for scripts/pine_check.py.
#
# Provenance: pine_check.py was validated RESOLVED-TRUSTWORTHY on 2026-06-23
# (handoff cc_handoff_pine_check_validation.md). These hooks keep that result
# re-checkable rather than a one-off (validation brief s10).
#
# LOCAL / MANUAL gate - NOT a CI gate, for two reasons:
#   * it POSTs to the live TradingView Guest endpoint (network required), and
#   * the oracle regression targets the locked strategy .pine, which are
#     gitignored and present only in the MAIN working tree (NOT in git worktrees
#     or fresh clones) - so that section skips-if-missing.
#
# Exit 0 = every runnable hook passed; 1 = a hook failed; 2 = zero oracles ran.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PC="$ROOT/scripts/pine_check.py"
FIX="$ROOT/tests/pine_check_fixtures"
MANIFEST="$ROOT/core/strategies/MANIFEST.sha256"
fail=0
ran=0
pause() { python -c "import time;time.sleep(0.4)"; }   # gentle on the undocumented endpoint

echo "== fixture assertions =="
python "$PC" "$FIX/good.pine"
if [ $? -eq 0 ]; then echo "PASS good->0"; else echo "FAIL good (expected exit 0)"; fail=1; fi
pause
python "$PC" "$FIX/bad.pine"
if [ $? -eq 1 ]; then echo "PASS bad->1"; else echo "FAIL bad (expected exit 1)"; fail=1; fi
pause

echo "== ENDPOINT tamper-grep (Guest translate_light facade unchanged) =="
# ENDPOINT is split across two adjacent string literals, so the full
# "translate_light?user_name=Guest" never appears contiguously in the source -
# check the three constituent constants instead (host + endpoint + Guest user).
if grep -q "pine-facade.tradingview.com" "$PC" \
   && grep -q "translate_light" "$PC" \
   && grep -q "user_name=Guest" "$PC"; then
  echo "PASS endpoint intact"
else
  echo "FAIL endpoint constant changed"; fail=1
fi

echo "== oracle regression (locked .pine; skip-if-absent - they live in the MAIN tree only) =="
mapfile -t ORACLES < <(awk '{print $2}' "$MANIFEST" | grep -v '_indicator\.pine$')
for rel in "${ORACLES[@]}"; do
  f="$ROOT/$rel"
  if [ ! -f "$f" ]; then echo "SKIP (absent) $rel"; continue; fi
  ran=$((ran + 1))
  if python "$PC" "$f" >/dev/null; then echo "PASS $rel"; else echo "REGRESSION $rel"; fail=1; fi
  pause
done

if [ "$ran" -eq 0 ]; then
  echo "NOTE: ZERO oracles ran (locked .pine absent — expected in a worktree/public clone, NOT in the main tree)"
  echo "== audit INCONCLUSIVE: 0/${#ORACLES[@]} oracles regression-tested — this is NOT a PASS =="
  exit 2
fi

if [ $fail -eq 0 ]; then
  echo "== audit PASS ($ran/${#ORACLES[@]} oracles regression-tested) =="
else
  echo "== audit FAIL ($ran/${#ORACLES[@]} oracles regression-tested) =="
fi
exit $fail
