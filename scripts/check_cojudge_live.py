"""Verify authored solutions through an existing CoJudge HTTP judge.

Use an authorized SSH tunnel to the server's loopback endpoint. This does not
change browser progress, disable authentication, or modify existing submissions.
"""
import argparse
import copy
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ADAPTER, ROOT, all_cases, encode, load_specs, slug


def request_json(base_url, path, body=None):
    request = Request(base_url.rstrip("/") + path,
                      data=None if body is None else json.dumps(body).encode(),
                      headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=120) as response:
            return json.load(response)
    except HTTPError as error:
        result = json.load(error)
        if not isinstance(result, dict):
            raise
        return result


def job(base_url, endpoint, body):
    started = request_json(base_url, endpoint, body)
    if "jobId" not in started:
        raise AssertionError(f"Judge did not start: {started}")
    deadline = time.monotonic() + 240
    while time.monotonic() < deadline:
        response = request_json(base_url, endpoint + "?jobId=" + started["jobId"])
        if response.get("ready"):
            return response
        time.sleep(0.25)
    raise TimeoutError(f"Judge job timed out: {started['jobId']}")


def check_live(spec, base_url):
    problem_id = slug(spec)
    code = spec["reference"].rstrip() + ADAPTER
    cases = all_cases(spec)
    body = {"problemId": problem_id, "language": "python", "code": code}
    samples = job(base_url, "/api/run", {
        **body, "testCases": [{"payload": encode(case["input"])} for case in cases[:3]],
    })
    sample_results = samples.get("results", [])
    assert len(sample_results) == 3 and all(r.get("isCorrect") for r in sample_results), (
        f"{problem_id} samples failed: {samples}"
    )
    submitted = job(base_url, "/api/submit", {**body, "startTcNo": 0})
    assert submitted.get("accepted") and submitted.get("totalTc") == len(cases), (
        f"{problem_id} submit failed: {submitted}"
    )
    assert len(submitted.get("results", [])) == len(cases)
    assert all(r.get("isCorrect") for r in submitted["results"])
    mutation = spec["mutations"][0]
    wrong = spec["reference"].replace(mutation["old"], mutation["new"], mutation.get("count", 1)) + ADAPTER
    rejected = job(base_url, "/api/submit", {**body, "code": wrong, "startTcNo": 0})
    assert not rejected.get("accepted") and (rejected.get("error") or any(
        not r.get("isCorrect") for r in rejected.get("results", [])
    )), f"{problem_id} faulty solution was not rejected: {rejected}"
    return {"id": problem_id, "sample_cases": 3, "official_cases": len(cases),
            "mutation_rejected": mutation["name"],
            "execution_ms": submitted.get("executionTimeMs")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    specs = load_specs(args.only)
    if not specs:
        parser.error("No matching problems")
    report = {"checks": [], "failures": []}
    for spec in specs:
        try:
            checked = check_live(spec, args.base_url)
            report["checks"].append(checked)
            print(f"PASS {checked['id']}: Run, Submit {checked['official_cases']} cases, rejected mutation", flush=True)
        except Exception as error:
            report["failures"].append({"number": spec["number"], "error": str(error)})
            print(f"FAIL {spec['number']:02d}: {error}", flush=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Live checks: {len(report['checks'])} passed; {len(report['failures'])} failed.")
    raise SystemExit(bool(report["failures"]))


if __name__ == "__main__":
    main()
