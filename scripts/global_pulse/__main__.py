"""Capture explicitly supplied observations; generate and route Notice drafts."""
import argparse
import json
from pathlib import Path
import sys

from .bridge import capture, decode, draft, finalize, validate, verify_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "capture"):
        command = commands.add_parser(name)
        command.add_argument("--packet", required=True, type=Path)
        command.add_argument("--input-root", required=True, type=Path)
        if name == "capture":
            command.add_argument("--output", type=Path, default=Path("local_artifacts/global-pulse"))
    for name in ("verify", "draft", "finalize"):
        command = commands.add_parser(name)
        command.add_argument("--bundle", type=Path, required=True)
        if name == "finalize":
            command.add_argument("--routing", type=Path, required=True)
            command.add_argument("--notice-dir", type=Path, required=True,
                                 help="review privacy before choosing docs/notes/notice")
    args = parser.parse_args(argv)
    try:
        if args.command in ("validate", "capture"):
            packet = decode(args.packet.read_bytes())
            checked = validate(packet, args.input_root)
            result = {"valid": True, "limitations": checked["limitations"]}
            if args.command == "capture":
                result["bundle"] = str(capture(packet, args.input_root, args.output))
        elif args.command == "verify":
            packet = verify_bundle(args.bundle)
            result = {"integrity": "verified", "observation_id": packet["observation_id"]}
        elif args.command == "draft":
            result = {"draft": str(draft(args.bundle))}
        else:
            result = {"notice": str(finalize(args.bundle, decode(args.routing.read_bytes()), args.notice_dir))}
        print(json.dumps(result))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
