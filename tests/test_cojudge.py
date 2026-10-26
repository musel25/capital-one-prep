"""Exercise the content builder and real Java marker, without learner attempts."""
import json
import shutil
from pathlib import Path

import pytest

from cojudge.authoring.support import (
    ROOT, build_problem, check_python, check_java, json_equal, validate_spec, load_specs,
)


def sample_spec():
    return {
        "number": 1, "slug": "count-values", "title": "Count values",
        "difficulty": "Easy", "time": 15, "prerequisites": "Lists.",
        "learn": "A count can be zero. Keep zero distinct from false.",
        "task": "Return the number of items in data.values.",
        "constraints": ["values is a list with at most 30 integers."],
        "hints": ["Use the list length."],
        "starter": "def solve(data):\n    raise NotImplementedError\n",
        "reference": "def solve(data):\n    return len(data['values'])\n",
        "java": "public Object solve(Map<String,Object> d) { return arr(d.get(\"values\")).size(); }",
        "approach": "Count the items. O(1) time and space.",
        "cases": [{"input": {"values": list(range(i))}, "expected": i, "label": f"length {i}"} for i in range(12)],
        "generated": [{"values": list(range(i))} for i in range(12, 24)],
        "mutations": [{"name": "off by one", "old": "len(data['values'])", "new": "len(data['values']) + 1"}],
        "sources": ["https://docs.python.org/3/library/functions.html#len"],
    }


def test_json_comparison_preserves_type_order_and_exact_integer_values():
    assert json_equal({"a": 1, "b": [None, 2]}, {"b": [None, 2.0], "a": 1})
    assert not json_equal(True, 1)
    assert not json_equal([1, 2], [2, 1])
    assert not json_equal({"a": 1}, {"a": "1"})
    assert not json_equal(9007199254740992, 9007199254740993)


def test_validator_rejects_duplicate_inputs_and_surviving_mutations():
    spec = sample_spec()
    spec["generated"][0] = spec["cases"][0]["input"]
    with pytest.raises(ValueError, match="duplicate"):
        validate_spec(spec)
    spec = sample_spec()
    spec["mutations"][0]["new"] = "len(list(data['values']))"
    with pytest.raises(AssertionError, match="survived"):
        check_python(spec)


def test_builder_separates_starter_reference_and_expected_values(tmp_path):
    spec = sample_spec()
    record = build_problem(spec, tmp_path)
    folder = tmp_path / "problems" / record["id"]
    meta = json.loads((folder / "metadata.json").read_text())
    assert list(meta["starterCode"]) == ["python"]
    assert "NotImplementedError" in meta["starterCode"]["python"]
    assert "len(data['values'])" not in meta["starterCode"]["python"]
    assert "len(data['values'])" in (folder / "solution.md").read_text()
    tests = json.loads((folder / "official-tests.json").read_text())
    assert len(tests) == 24
    assert all(set(case) == {"payload"} for case in tests)
    assert (tmp_path / "instructor" / record["id"] / "reference.py").is_file()
    assert "type annotations" in (folder / "statement.md").read_text()


@pytest.mark.skipif(not shutil.which("javac"), reason="Java compiler needed")
def test_java_marker_computes_new_inputs_and_rejects_wrong_output(tmp_path):
    spec = sample_spec()
    report = check_java(spec, tmp_path)
    assert report["cases"] == 24
    assert report["wrong_rejected"] >= 24


@pytest.mark.skipif(not shutil.which("javac"), reason="Java compiler needed")
def test_java_json_handles_strings_large_numbers_and_boolean_types(tmp_path):
    spec = sample_spec()
    spec["reference"] = "def solve(data):\n    return data['value']\n"
    spec["java"] = 'public Object solve(Map<String,Object> d) { return d.get("value"); }'
    values = [None, True, False, 0, -1, 9007199254740993, "\"\\\n\t", "á😀", [], {}, [1, "1"], {"x": False}]
    spec["cases"] = [{"input": {"value": x}, "expected": x, "label": str(i)} for i, x in enumerate(values)]
    spec["generated"] = [{"value": {"n": i, "a": [None, False, "x"]}} for i in range(12)]
    spec["mutations"] = [{"name": "drops value", "old": "data['value']", "new": "None"}]
    assert check_java(spec, tmp_path)["cases"] == 24


@pytest.mark.skipif(not shutil.which("javac"), reason="Java compiler needed")
def test_java_preserves_integer_vs_float_input_type(tmp_path):
    spec = sample_spec()
    spec["reference"] = "def solve(data):\n    return type(data['value']) is int\n"
    spec["java"] = 'public Object solve(Map<String,Object> d) { return isInteger(d.get("value")); }'
    values = [0, 0.0, 1, 1.0, -1, -1.0, 100000, 1e5, True, False, "1", None]
    spec["cases"] = [{"input": {"value": x}, "expected": type(x) is int, "label": repr(x)} for x in values]
    spec["generated"] = [{"value": i + 12} for i in range(12)]
    spec["mutations"] = [{"name": "accepts floats", "old": "type(data['value']) is int", "new": "isinstance(data['value'], (int, float))"}]
    assert check_java(spec, tmp_path)["cases"] == 24


@pytest.mark.skipif(not shutil.which("javac"), reason="Java compiler needed")
def test_java_rejects_signed_unicode_escape_even_if_it_decodes_to_answer(tmp_path):
    spec = sample_spec()
    spec["reference"] = 'def solve(data):\n    return "A"\n'
    spec["java"] = 'public Object solve(Map<String,Object> d) { return "A"; }'
    spec["cases"] = [{**case, "expected": "A"} for case in spec["cases"]]
    spec["mutations"] = [{"name": "wrong character", "old": '"A"', "new": '"B"'}]
    assert check_java(spec, tmp_path)["cases"] == 24


def test_published_course_has_fifty_ordered_complete_python_problems():
    pack = ROOT / "cojudge"
    course = json.loads((pack / "courses/capital-one-engineering-50/courseinfo.json").read_text())
    groups = course["problems-of-category"]
    ids = [problem for group in course["category-order"] for problem in groups[group]]
    assert len(ids) == len(set(ids)) == 50
    assert all(len(groups[group]) == 10 for group in groups)
    assert [int(name.split("-")[1]) for name in ids] == list(range(1, 51))
    for problem in ids:
        folder = pack / "problems" / problem
        assert {"metadata.json", "statement.md", "official-tests.json", "Marker.java", "solution.md"} <= {p.name for p in folder.iterdir()}
        meta = json.loads((folder / "metadata.json").read_text())
        assert meta["link"] == ""  # The site would label this as a LeetCode link.
        assert list(meta["starterCode"]) == ["python"]
        compile(meta["starterCode"]["python"], problem, "exec")
        assert len(json.loads((folder / "official-tests.json").read_text())) >= 24
    review = json.loads((pack / "authoring/review-cases.json").read_text())
    assert set(review) == {str(n) for n in range(1, 51)}
    assert sum(len(cases) for cases in review.values()) == 51


def test_bugfix_starters_run_and_expose_the_disclosed_defect():
    from cojudge.authoring.support import python_solver
    import copy

    for spec in load_specs([11, 12, 17, 32, 36]):
        solve = python_solver(spec["starter"])
        wrong_results = 0
        for case in spec["cases"]:
            # These are runnable faulty programs, rather than missing-code stubs.
            actual = solve(copy.deepcopy(case["input"]))
            wrong_results += not json_equal(actual, case["expected"])
        assert wrong_results, f"Starter unexpectedly solves problem {spec['number']}"
