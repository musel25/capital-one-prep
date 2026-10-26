"""Check that live verification cannot silently skip extra cases or mutations."""
import pytest

from scripts import check_cojudge_live as live


def spec():
    return {"number": 1, "slug": "fixture", "reference": "def solve(data): return data['x']",
            "mutations": [{"name": "zero", "old": "data['x']", "new": "0"},
                          {"name": "one", "old": "data['x']", "new": "1"}]}


def stub_jobs(monkeypatch, review_output="2", review_verdict=True):
    calls = []
    cases = [{"input": {"x": 2}, "expected": 2}] * 3
    monkeypatch.setattr(live, "all_cases", lambda _: cases)

    def job(base, endpoint, body):
        calls.append((endpoint, body))
        if endpoint == "/api/run":
            if len(body["testCases"]) == 1:
                return {"results": [{"isCorrect": review_verdict, "output": review_output,
                                      "correctAnswer": "2", "error": None}]}
            return {"results": [{"isCorrect": True}] * 3}
        if "return data['x']" in body["code"]:
            return {"accepted": True, "totalTc": 3, "results": [{"isCorrect": True}] * 3}
        return {"accepted": False, "results": [{"isCorrect": False}]}

    monkeypatch.setattr(live, "job", job)
    return calls


def test_live_check_runs_every_mutation_and_manual_review_case(monkeypatch):
    calls = stub_jobs(monkeypatch)
    result = live.check_live(spec(), "http://test", [{"input": {"x": 2}, "expected": 2}])
    assert result["review_cases"] == 1
    assert result["mutations_rejected"] == ["zero", "one"]
    assert len([c for c in calls if c[0] == "/api/submit"]) == 3


@pytest.mark.parametrize("output,verdict", [("true", True), ("3", True), ("2", False)])
def test_review_result_must_match_manual_expectation_and_judge(monkeypatch, output, verdict):
    stub_jobs(monkeypatch, output, verdict)
    with pytest.raises(AssertionError, match="review"):
        live.check_live(spec(), "http://test", [{"input": {"x": 2}, "expected": 2}])


@pytest.mark.parametrize("rejection", [
    {"accepted": False, "error": "Runner unavailable"},
    {"accepted": False, "results": [{"isCorrect": False, "error": "Runner unavailable"}]},
])
def test_runner_failure_is_not_evidence_that_a_mutation_is_rejected(monkeypatch, rejection):
    stub_jobs(monkeypatch)
    original_job = live.job

    def job(base, endpoint, body):
        if endpoint == "/api/submit" and "return data['x']" not in body["code"]:
            return rejection
        return original_job(base, endpoint, body)

    monkeypatch.setattr(live, "job", job)
    with pytest.raises(AssertionError, match="faulty solution"):
        live.check_live(spec(), "http://test")
