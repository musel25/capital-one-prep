"""Verify authored solutions through an existing CoJudge HTTP judge.

Use an authorized SSH tunnel to the server's loopback endpoint. This does not
change browser progress, disable authentication, or modify existing submissions.
"""
import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ADAPTER, ROOT, all_cases, encode, json_equal, load_specs, slug


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


def check_live(spec, base_url, review_cases=None):
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
    review_cases = review_cases or []
    if review_cases:
        reviewed = job(base_url, "/api/run", {
            **body, "testCases": [{"payload": encode(case["input"])} for case in review_cases],
        })
        results = reviewed.get("results", [])
        assert len(results) == len(review_cases), f"{problem_id} review results missing: {reviewed}"
        for case, result in zip(review_cases, results):
            assert result.get("isCorrect") and not result.get("error"), (
                f"{problem_id} review case failed: {result}"
            )
            for field in ("output", "correctAnswer"):
                assert json_equal(json.loads(result[field]), case["expected"]), (
                    f"{problem_id} review {field} differs from manual expectation: {result}"
                )
    mutations_rejected = []
    for mutation in spec["mutations"]:
        wrong = spec["reference"].replace(mutation["old"], mutation["new"], mutation.get("count", 1)) + ADAPTER
        rejected = job(base_url, "/api/submit", {**body, "code": wrong, "startTcNo": 0})
        assert rejected.get("accepted") is False and not rejected.get("error") and any(
            r.get("isCorrect") is False and not r.get("error")
            for r in rejected.get("results", [])
        ), f"{problem_id} faulty solution {mutation['name']!r} was not rejected by a wrong answer: {rejected}"
        mutations_rejected.append(mutation["name"])
    return {"id": problem_id, "sample_cases": 3, "official_cases": len(cases),
            "review_cases": len(review_cases), "mutations_rejected": mutations_rejected,
            "execution_ms": submitted.get("executionTimeMs")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--only", nargs="+", type=int)
    parser.add_argument("--include-review", action="store_true",
                        help="Run independent review cases and check their manual expected outputs")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    specs = load_specs(args.only)
    if not specs:
        parser.error("No matching problems")
    review_cases = (json.loads((ROOT / "cojudge/authoring/review-cases.json").read_text())
                    if args.include_review else {})
    report = {"checks": [], "failures": []}
    for spec in specs:
        try:
            cases = review_cases[str(spec["number"])] if args.include_review else []
            checked = check_live(spec, args.base_url, cases)
            report["checks"].append(checked)
            print(f"PASS {checked['id']}: Run, Submit {checked['official_cases']} cases, "
                  f"{checked['review_cases']} review cases, "
                  f"{len(checked['mutations_rejected'])} rejected mutations", flush=True)
        except Exception as error:
            report["failures"].append({"number": spec["number"], "error": str(error)})
            print(f"FAIL {spec['number']:02d}: {error}", flush=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Live checks: {len(report['checks'])} passed; {len(report['failures'])} failed.")
    raise SystemExit(bool(report["failures"]))


if __name__ == "__main__":
    main()
