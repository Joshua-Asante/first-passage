"""Check or regenerate the live G4 roll source artifacts (ops/c1_rail/contract_roll.py).

  --compat-check      print the compat build's sha256 and MATCH/DIFFERS against the bound list's pinned sha
  --forward           write ops/calendars/contract_roll_forward.json
  --forward --check   regenerate the forward artifact and compare bytes; write nothing
"""
import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ops"))
from c1_rail import contract_roll as cr  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--compat-check", action="store_true")
    mode.add_argument("--forward", action="store_true")
    ap.add_argument("--check", action="store_true", help="with --forward: compare only")
    args = ap.parse_args(argv)
    if args.compat_check:
        digest = hashlib.sha256(cr.build(*cr.COMPAT_WINDOW, compat=True)).hexdigest()
        same = digest == cr.COMPAT_SHA256
        print(f"{digest}  {'MATCH' if same else 'DIFFERS'}")
        return 0 if same else 1
    data, out = cr.forward(), cr.ROOT / cr.FORWARD
    digest = hashlib.sha256(data).hexdigest()
    if args.check:
        same = out.is_file() and out.read_bytes() == data
        print(f"{digest}  {'MATCH' if same else 'DIFFERS'}")
        return 0 if same else 1
    out.write_bytes(data)
    print(f"{digest}  {cr.FORWARD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
