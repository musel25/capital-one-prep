"""Protect native course links, identities, and runnable repair starters."""
import copy
import json

import pytest

from cojudge.authoring.support import build_problem, load_specs, validate_spec, json_equal, python_solver


def alternate_spec():
    spec = copy.deepcopy(load_specs([3])[0])
    spec.update(number=1, prefix="cb", course_id="capital-one-codebase-practice",
                category="01-read-and-trace", level=1)
    return spec


def test_alternate_course_has_its_own_identity_and_links(tmp_path):
    record = build_problem(alternate_spec(), tmp_path)
    assert record["id"] == "cb-01-missing-null-zero"
    folder = tmp_path / "problems" / record["id"]
    meta = json.loads((folder / "metadata.json").read_text())
    statement = (folder / "statement.md").read_text()
    assert meta["category"] == "01-read-and-trace"
    assert "/?course=capital-one-codebase-practice" in statement
    assert "capital-one-engineering-50" not in statement


@pytest.mark.parametrize("field", ["prefix", "course_id", "category"])
def test_course_metadata_rejects_path_or_markup_injection(field):
    spec = alternate_spec()
    spec[field] = "../other?bad=<tag>"
    with pytest.raises(ValueError, match="metadata"):
        validate_spec(spec)


def test_guided_repairs_are_runnable_and_do_not_expose_ai_answers(tmp_path):
    from cojudge.codebase.lessons import LESSONS
    from cojudge.codebase.support import load_codebase_specs

    specs = load_codebase_specs()
    assert len(specs) == 16
    for spec, lesson in zip(specs, LESSONS):
        starter = python_solver(spec["starter"])
        assert any(not json_equal(starter(copy.deepcopy(case["input"])), case["expected"])
                   for case in spec["cases"]), spec["title"]
        record = build_problem(spec, tmp_path)
        folder = tmp_path / "problems" / record["id"]
        assert lesson["ai_answer"] not in (folder / "statement.md").read_text()
        assert lesson["ai_answer"] in (folder / "solution.md").read_text()


def test_bug_reports_describe_the_starter_defect():
    from cojudge.codebase.lessons import LESSONS
    from cojudge.codebase.support import load_codebase_specs

    for spec, lesson in zip(load_codebase_specs(), LESSONS):
        check = lesson["ticket_check"]
        starter = python_solver(spec["starter"])(copy.deepcopy(check["input"]))
        reference = python_solver(spec["reference"])(copy.deepcopy(check["input"]))
        assert json_equal(starter, check["starter_output"]), spec["title"]
        assert not json_equal(reference, check["starter_output"]), spec["title"]
