"""Start preserved codebase labs and check implementation and test evidence."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from codebase_labs.runner import ROOT, check, load_labs, start, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    create = commands.add_parser("start")
    create.add_argument("lab_id")
    create.add_argument("--output-root", type=Path, default=ROOT / "attempts")
    grade = commands.add_parser("check")
    grade.add_argument("path", type=Path)
    author = commands.add_parser("verify")
    author.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "list":
            for lab in load_labs():
                print(f"{lab['id']}  {lab['title']}  ({lab['minutes']} min; {lab['kind']})")
        elif args.command == "start":
            print(start(args.lab_id, args.output_root))
        elif args.command == "check":
            result = check(args.path)
            print(json.dumps(result, indent=2))
            return {"passed": 0, "failed": 1, "error": 2}[result["status"]]
        else:
            result = verify()
            if args.report:
                args.report.write_text(json.dumps(result, indent=2) + "\n")
            print(f"Verified {len(result['labs'])} local labs.")
    except (ValueError, OSError, AssertionError) as error:
        print(f"Check could not complete: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
