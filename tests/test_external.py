"""Verify upstream fidelity, exercise feedback, and preservation of learner work."""
import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "external"
UPSTREAM = EXTERNAL / "upstream/gilded-rose"


def cli(script, *args):
    return subprocess.run(
        [sys.executable, str(EXTERNAL / script), *map(str, args)],
        cwd=ROOT, capture_output=True, text=True, timeout=20,
    )


def load_module(path):
    module = types.ModuleType("gilded_rose_under_test")
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


@pytest.mark.parametrize("sell_in,quality,expected", [
    (3, 6, (2, 4)),
    (1, 8, (0, 6)),
    (0, 8, (-1, 4)),
    (-2, 8, (-3, 4)),
    (3, 1, (2, 0)),
    (0, 3, (-1, 0)),
    (0, 0, (-1, 0)),
])
def test_reference_conjured_extension(sell_in, quality, expected):
    module = load_module(EXTERNAL / "reference/gilded_rose.py")
    item = module.Item("Conjured Mana Cake", sell_in, quality)
    module.GildedRose([item]).update_quality()
    assert (item.sell_in, item.quality) == expected


def test_snapshot_matches_pinned_upstream_git_blobs():
    provenance = json.loads((EXTERNAL / "provenance.json").read_text())
    for record in provenance["files"]:
        content = (UPSTREAM / record["path"]).read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert digest == record["git_blob_sha"], record["path"]


def test_start_never_overwrites_work_or_copies_instructor_material(tmp_path):
    first = cli("start.py", "external-gilded-rose", "--output-root", tmp_path)
    assert first.returncode == 0, first.stderr
    one = Path(first.stdout.strip())
    (one / "gilded_rose.py").write_text("# my incomplete solution\n")
    (one / "notes.md").write_text("preserve my explanation")
    second = cli("start.py", "external-gilded-rose", "--output-root", tmp_path)
    assert second.returncode == 0, second.stderr
    two = Path(second.stdout.strip())
    assert one != two and one.parent == two.parent == tmp_path
    assert (one / "gilded_rose.py").read_text() == "# my incomplete solution\n"
    assert (one / "notes.md").read_text() == "preserve my explanation"
    assert (two / "gilded_rose.py").read_bytes() == (UPSTREAM / "python/gilded_rose.py").read_bytes()
    assert (two / "LICENSE").read_bytes() == (UPSTREAM / "license.txt").read_bytes()
    assert {p.name for p in two.iterdir()} == {
        "gilded_rose.py", "texttest_fixture.py", "LICENSE", "TASK.md",
        "README.md", "GildedRoseRequirements.md", ".external-attempt.json",
    }


def test_invalid_id_creates_no_workspace(tmp_path):
    result = cli("start.py", "../../elsewhere", "--output-root", tmp_path)
    assert result.returncode == 2
    assert list(tmp_path.iterdir()) == []


def test_checker_distinguishes_preserved_baseline_and_missing_extension():
    baseline = cli("check.py", UPSTREAM / "python", "--json")
    assert baseline.returncode == 1, baseline.stdout + baseline.stderr
    report = json.loads(baseline.stdout)
    assert all(case["passed"] for case in report["checks"] if case["group"] == "smoke")
    assert any(not case["passed"] for case in report["checks"] if case["group"] == "conjured")
    reference = cli("check.py", EXTERNAL / "reference", "--json")
    assert reference.returncode == 0, reference.stdout + reference.stderr
    assert all(case["passed"] for case in json.loads(reference.stdout)["checks"])


def test_smoke_can_pass_before_extension_and_check_preserves_attempt(tmp_path):
    started = cli("start.py", "external-gilded-rose", "--output-root", tmp_path)
    assert started.returncode == 0, started.stderr
    attempt = Path(started.stdout.strip())
    before = {str(p.relative_to(attempt)): p.read_bytes() for p in attempt.rglob("*") if p.is_file()}
    smoke = cli("check.py", attempt, "--smoke")
    assert smoke.returncode == 0, smoke.stdout + smoke.stderr
    missing = cli("check.py", attempt)
    assert missing.returncode == 1, missing.stdout + missing.stderr
    assert "FAIL" in missing.stdout and "conjured" in missing.stdout.lower()
    after = {str(p.relative_to(attempt)): p.read_bytes() for p in attempt.rglob("*") if p.is_file()}
    assert after == before


def test_checker_reports_invalid_workspace_as_error(tmp_path):
    result = cli("check.py", tmp_path)
    assert result.returncode == 2
    assert "gilded_rose.py" in result.stderr
