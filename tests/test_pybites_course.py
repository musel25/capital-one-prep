"""Check that Pybites verification detects plausible incomplete implementations."""
import pytest

from cojudge.pybites.support import load_specs, statement, verify


def test_verifier_rejects_a_mutation_that_the_tests_do_not_detect():
    spec = load_specs([2])[0]
    spec["mutations"] = [{"name": "equivalent", "old": "self.last_name[:7]", "new": "self.last_name[0:7]"}]
    with pytest.raises(AssertionError, match="survived"):
        verify(spec)


def test_verifier_reports_the_tests_that_detect_a_real_fault():
    spec = load_specs([2])[0]
    spec["mutations"] = [{"name": "surname too short", "old": "self.last_name[:7]", "new": "self.last_name[:6]"}]
    result = verify(spec)
    assert result["mutations"][0]["detected_by"]


def test_every_bite_defines_inputs_and_faults():
    for spec in load_specs():
        assert spec.get("contract"), f"Missing input contract for bite {spec['number']}"
        assert spec.get("mutations"), f"Missing fault checks for bite {spec['number']}"
