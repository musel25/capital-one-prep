"""Build and verify the Python OOP Path course without changing other courses."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ADAPTER, ROOT, encode, write_json
from cojudge.oop.support import (
    COURSE_ID, all_cases, build_problem, course_info, full_source, load_specs, problem_id, verify,
)


def request_json(base_url, path, user, body=None):
    request = Request(base_url.rstrip("/") + path, data=None if body is None else json.dumps(body).encode(),
                      headers={"Content-Type": "application/json", "X-CoJudge-User": user})
    try:
        with urlopen(request, timeout=120) as response:
            return json.load(response)
    except HTTPError as error:
        return json.load(error)


def job(base_url, endpoint, user, body):
    started = request_json(base_url, endpoint, user, body)
    if "jobId" not in started:
        raise AssertionError(f"Judge did not start: {started}")
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        response = request_json(base_url, endpoint + "?jobId=" + started["jobId"], user)
        if response.get("ready"):
            return response
        time.sleep(0.25)
    raise TimeoutError(started["jobId"])


def check_live(spec, base_url, user):
    """Submit the reference (must pass every test) and the starter (must fail) to the real judge."""
    pid, cases = problem_id(spec), all_cases(spec)
    submit = lambda classes: job(base_url, "/api/submit", user, {
        "problemId": pid, "language": "python", "code": full_source(classes).rstrip() + ADAPTER, "startTcNo": 0})
    good = submit(spec["reference"])
    assert good.get("accepted") and good.get("totalTc") == len(cases), f"{pid} reference rejected: {good}"
    samples = job(base_url, "/api/run", user, {
        "problemId": pid, "language": "python", "code": full_source(spec["reference"]).rstrip() + ADAPTER,
        "testCases": [{"payload": encode(c["input"])} for c in cases[:3]]})
    assert all(r.get("isCorrect") for r in samples.get("results", [])) and len(samples["results"]) == 3, samples
    bad = submit(spec["starter"])
    assert not bad.get("accepted"), f"{pid} starter accepted"
    return {"id": pid, "cases": len(cases)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify", "live"])
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--base-url", help="live: an authorized tunnel to the judge, e.g. http://127.0.0.1:15379")
    parser.add_argument("--user", default="musel", help="live: profile name for the identity header")
    args = parser.parse_args()
    if args.command == "live" and not args.base_url:
        parser.error("live needs --base-url")
    specs = load_specs(args.only)
    if not specs:
        parser.error("No matching exercises")
    records, failures = [], 0
    with tempfile.TemporaryDirectory(prefix="oop-course-") as work:
        for spec in specs:
            try:
                if args.command == "build":
                    result = build_problem(spec, ROOT / "cojudge")
                elif args.command == "verify":
                    result = verify(spec, work)
                else:
                    result = check_live(spec, args.base_url, args.user)
                records.append(result)
                print(f"PASS {result['id']} ({result['cases']} cases)", flush=True)
            except Exception as error:
                failures += 1
                print(f"FAIL {spec['number']:02d}: {error}", flush=True)
    if args.command == "build" and not args.only and not failures:
        if [r["number"] for r in records] != list(range(1, 23)):
            parser.error("The complete course must contain exercises 01-22")
        course = ROOT / "cojudge/courses" / COURSE_ID
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / "courseinfo.json", course_info(records))
    print(f"{len(records)} passed; {failures} failed.")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
