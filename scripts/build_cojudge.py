"""Build the original Engineering 50 course in the native CoJudge file format."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, LEVELS, build_problem, load_specs, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="+", type=int, help="Build selected numbers while authoring")
    parser.add_argument("--output", type=Path, default=ROOT / "cojudge")
    args = parser.parse_args()
    specs = load_specs(args.only)
    if not args.only and [s["number"] for s in specs] != list(range(1, 51)):
        parser.error("The complete course must contain exactly problems 01–50")
    records = [build_problem(spec, args.output) for spec in specs]
    if not args.only:
        course = {
            "title": "Capital One Engineering 50",
            "description": "50 original Python problems for technical practice beyond basic LeetCode. Start at 01. Work through one level at a time: Python data, objects and state, APIs, SQL, then system components. Read the short lesson before coding. Select Python in the editor. API and distributed-system tasks use deterministic simulations; SQL references use real SQLite. Optional reference solutions are available. This is independent training, not an official question bank or a readiness score.",
            "category-order": LEVELS,
            "problems-of-category": {level: [r["id"] for r in records if r["category"] == level] for level in LEVELS},
        }
        folder = args.output / "courses/capital-one-engineering-50"
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / "courseinfo.json", course)
        write_json(args.output / "manifest.json", records)
    print(f"Built {len(records)} problems with {sum(r['cases'] for r in records)} cases.")


if __name__ == "__main__":
    main()
