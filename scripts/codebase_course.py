"""Build and verify the Codebase Practice course without changing Engineering 50."""
import argparse
import copy
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import (
    ROOT, all_cases, build_problem, check_java, check_python,
    json_equal, python_solver, write_json,
)
from cojudge.codebase.support import COURSE_ID, course_info, load_codebase_specs, review_cases
from scripts.check_cojudge_live import check_live


def verify_spec(spec, work):
    result = check_python(spec)
    result["java"] = check_java(spec, work)
    reviews = review_cases(spec)
    reference = python_solver(spec["reference"])
    for case in reviews:
        assert json_equal(reference(copy.deepcopy(case["input"])), case["expected"]), case["label"]
    result["review"] = {"cases": len(reviews), "java": check_java(
        {**spec, "cases": reviews, "generated": []}, work)}
    starter = python_solver(spec["starter"])
    wrong = sum(not json_equal(starter(copy.deepcopy(case["input"])), case["expected"])
                for case in all_cases(spec))
    assert wrong, f"Starter unexpectedly passes: {result['id']}"
    result["starter_wrong_answers"] = wrong
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify", "live"])
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--base-url")
    args = parser.parse_args()
    if args.command == "live" and not args.base_url:
        parser.error("live needs --base-url for an authorized tunnel")
    specs = load_codebase_specs(args.only)
    if not specs:
        parser.error("No matching exercises")
    report = {"command": args.command, "checks": [], "failures": []}
    with tempfile.TemporaryDirectory(prefix="codebase-course-") as work:
        for spec in specs:
            try:
                if args.command == "build":
                    result = build_problem(spec, ROOT / "cojudge")
                elif args.command == "verify":
                    result = verify_spec(spec, work)
                else:
                    result = check_live(spec, args.base_url, review_cases(spec))
                report["checks"].append(result)
                print(f"PASS {result['id']}", flush=True)
            except Exception as error:
                report["failures"].append({"number": spec["number"], "error": str(error)})
                print(f"FAIL {spec['number']:02d}: {error}", flush=True)
            if args.report:
                write_json(args.report, report)
    if args.command == "build" and not args.only and not report["failures"]:
        from codebase_labs.guide import build_briefs
        build_briefs()
        course = ROOT / "cojudge/courses" / COURSE_ID
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / "courseinfo.json", course_info(report["checks"]))
        write_json(ROOT / "cojudge/codebase/manifest.json", report["checks"])
    print(f"{len(report['checks'])} passed; {len(report['failures'])} failed.")
    raise SystemExit(bool(report["failures"]))


if __name__ == "__main__":
    main()
