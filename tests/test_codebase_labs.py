"""Check attempt preservation and honest grading of learner-written tests."""
import hashlib
import json
from pathlib import Path

import pytest

from codebase_labs import runner


@pytest.fixture
def lab(monkeypatch):
    value = {
        "id": "lab01", "title": "Fixture lab", "kind": "tests", "after": 4,
        "minutes": 20, "objective": "Test a function.", "brief": "Write a regression test.",
        "editable": ["tests/learner/"],
        "files": {"app/__init__.py": "", "app/main.py": "def double(x): return x * 2\n",
                  "tests/test_existing.py": "def test_boot(): assert True\n",
                  "tests/learner/test_task.py": '"""Write tests here."""\n'},
        "reference": {}, "contract_tests": "from app.main import double\ndef test_contract(): assert double(3) == 6\n",
        "reference_tests": "from app.main import double\ndef test_double(): assert double(3) == 6\n",
        "variants": [{"name": "off by one", "files": {"app/main.py": "def double(x): return x * 2 + 1\n"}}],
        "ai_claim": "A sample claim.", "ai_answer": "Private answer.", "sources": [],
    }
    monkeypatch.setattr(runner, "load_labs", lambda: [value])
    return value


def fingerprints(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file()}


def test_start_preserves_existing_work_and_excludes_instructor_material(tmp_path, lab):
    first = runner.start("lab01", tmp_path)
    (first / "NOTES.md").write_text("my work")
    saved = fingerprints(first)
    second = runner.start("lab01", tmp_path)
    assert first != second
    assert fingerprints(first) == saved
    combined = "\n".join(p.read_text() for p in second.rglob("*") if p.is_file())
    assert "Private answer." not in combined
    assert lab["reference_tests"] not in combined
    assert "off by one" not in combined


def test_check_grades_real_tests_without_changing_attempt(tmp_path, lab):
    attempt = runner.start("lab01", tmp_path)
    (attempt / "tests/learner/test_task.py").write_text(lab["reference_tests"])
    before = fingerprints(attempt)
    result = runner.check(attempt)
    assert result["status"] == "passed", result
    assert result["mutations_rejected"] == ["off by one"]
    assert fingerprints(attempt) == before


@pytest.mark.parametrize("source,phase", [
    ('"""No tests."""\n', "learner-reference"),
    ("import pytest\n@pytest.mark.skip\ndef test_skip(): pass\n", "learner-reference"),
    ("def test_weak(): assert True\n", "mutation: off by one"),
])
def test_empty_skipped_or_weak_tests_do_not_pass(tmp_path, lab, source, phase):
    attempt = runner.start("lab01", tmp_path)
    (attempt / "tests/learner/test_task.py").write_text(source)
    result = runner.check(attempt)
    assert result["status"] == "failed", result
    assert result["phase"] == phase


def test_import_error_is_a_setup_error_not_a_detected_bug(tmp_path, lab):
    attempt = runner.start("lab01", tmp_path)
    (attempt / "tests/learner/test_task.py").write_text("import missing_course_package\n")
    assert runner.check(attempt)["status"] == "error"


@pytest.mark.parametrize("message", ["crash", "AssertionError in adapter"])
def test_crashing_variant_does_not_count_as_assertion_evidence(tmp_path, lab, message):
    lab["variants"][0]["files"]["app/main.py"] = f"def double(x): raise RuntimeError({message!r})\n"
    attempt = runner.start("lab01", tmp_path)
    (attempt / "tests/learner/test_task.py").write_text(lab["reference_tests"])
    result = runner.check(attempt)
    assert result["status"] == "error", result
    assert result["mutations_rejected"] == []


def test_manifest_and_symlink_guards(tmp_path, lab):
    attempt = runner.start("lab01", tmp_path)
    marker = attempt / ".codebase-lab.json"
    marker.write_text(json.dumps({"schema_version": 1, "lab_id": "../outside"}))
    with pytest.raises(ValueError, match="manifest"):
        runner.check(attempt)
    marker.write_text(json.dumps({"schema_version": 1, "lab_id": "lab01"}))
    (attempt / "external").symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        runner.check(attempt)


def test_protected_source_cannot_change_in_a_test_only_lab(tmp_path, lab):
    attempt = runner.start("lab01", tmp_path)
    (attempt / "app/main.py").write_text("def double(x): return 0\n")
    with pytest.raises(ValueError, match="edit scope"):
        runner.check(attempt)


def test_hidden_contract_checks_the_learners_repair(tmp_path, lab):
    correct = lab["files"]["app/main.py"]
    lab["kind"] = "repair"
    lab["editable"].append("app/main.py")
    lab["reference"] = {"app/main.py": correct}
    lab["files"]["app/main.py"] = "def double(x): return x * 2 + 1\n"
    attempt = runner.start("lab01", tmp_path)
    result = runner.check(attempt)
    assert result["status"] == "failed"
    assert result["phase"] == "implementation-contract"
    (attempt / "app/main.py").write_text(correct)
    (attempt / "tests/learner/test_task.py").write_text(lab["reference_tests"])
    assert runner.check(attempt)["status"] == "passed"
