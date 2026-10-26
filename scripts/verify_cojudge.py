"""Check Python, Java, explicit expectations, and realistic mutations for each problem."""
import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import check_java, check_python, load_specs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--python-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    specs = load_specs(args.only)
    if not specs:
        parser.error("No authored problems matched")
    if not args.only and [s["number"] for s in specs] != list(range(1, 51)):
        parser.error("The complete course must contain exactly problems 01–50")
    reports, failures = [], []
    with tempfile.TemporaryDirectory(prefix="cojudge-verify-") as work:
        for spec in specs:
            try:
                report = check_python(spec)
                if not args.python_only:
                    report["java"] = check_java(spec, work)
                reports.append(report)
                print(f"PASS {report['id']}: {report['cases']} cases; {len(report['mutations'])} mutations rejected", flush=True)
            except Exception as error:
                failures.append({"number": spec["number"], "error": str(error)})
                print(f"FAIL {spec['number']:02d}: {error}", flush=True)
    result = {"problems": len(reports), "cases": sum(r["cases"] for r in reports),
              "mutations": sum(len(r["mutations"]) for r in reports), "reports": reports, "failures": failures}
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Verified {result['problems']} problems, {result['cases']} cases, {result['mutations']} mutations; {len(failures)} failures.")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
