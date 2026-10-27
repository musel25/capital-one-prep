"""Build and verify the Pybites OOP Path course without changing other courses."""
import argparse
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.pybites.support import (
    COURSE_ID, build_problem, course_info, full_source, load_specs, problem_id, run_all, verify,
)


def request_json(base_url, path, user, body=None):
    request = Request(base_url.rstrip("/") + path, data=None if body is None else json.dumps(body).encode(),
                      headers={"Content-Type": "application/json", "X-CoJudge-User": user})
    try:
        with urlopen(request, timeout=120) as response:
            return json.load(response)
    except HTTPError as error:
        return json.load(error)


def submit(base_url, user, pid, code):
    started = request_json(base_url, "/api/submit", user,
                           {"problemId": pid, "language": "python", "code": code, "startTcNo": 0})
    if "jobId" not in started:
        raise AssertionError(f"Judge did not start: {started}")
    deadline = time.monotonic() + 300
    while time.monotonic() < deadline:
        response = request_json(base_url, "/api/submit?jobId=" + started["jobId"], user)
        if response.get("ready"):
            return response
        time.sleep(0.25)
    raise TimeoutError(started["jobId"])


def check_live(spec, base_url, user):
    """The reference must pass every test on the real judge; the template must not."""
    pid = problem_id(spec)
    total = len(run_all(spec, spec["reference"]))
    good = submit(base_url, user, pid, full_source(spec, spec["reference"]))
    assert good.get("accepted") and good.get("totalTc") == total, f"{pid} reference rejected: {str(good)[:1500]}"
    bad = submit(base_url, user, pid, full_source(spec, spec["template"]))
    assert not bad.get("accepted"), f"{pid} template accepted"
    return {"id": pid, "cases": total}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify", "live"])
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--base-url", help="live: an authorized tunnel to the judge, e.g. http://127.0.0.1:15379")
    parser.add_argument("--user", default="musel")
    args = parser.parse_args()
    if args.command == "live" and not args.base_url:
        parser.error("live needs --base-url")
    specs = load_specs(args.only)
    records, failures = [], 0
    for spec in specs:
        try:
            if args.command == "build":
                result = build_problem(spec, ROOT / "cojudge")
            elif args.command == "verify":
                result = verify(spec)
                result["cases"] = len(result["tests"])
            else:
                result = check_live(spec, args.base_url, args.user)
            records.append(result)
            print(f"PASS {result['id']} ({result['cases']} tests)", flush=True)
        except Exception as error:
            failures += 1
            print(f"FAIL {spec['number']:02d}: {error}", flush=True)
    if args.command == "build" and not args.only and not failures:
        if [r["number"] for r in records] != list(range(1, 23)):
            parser.error("The complete course must contain bites 01-22")
        course = ROOT / "cojudge/courses" / COURSE_ID
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / "courseinfo.json", course_info(records))
    print(f"{len(records)} passed; {failures} failed.")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
