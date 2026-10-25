"""Run the actual learner launcher and exercise, never existing user attempts."""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def launch(output):
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/progressive.py'),
                             'start', '--output-root', str(output), '--json'],
                            capture_output=True, text=True, cwd=ROOT)
    assert result.returncode == 0, result.stderr
    return Path(json.loads(result.stdout)['path'])


def test_progressive_launcher_preserves_work_and_copies_only_learner_material(tmp_path):
    one = launch(tmp_path)
    (one / 'notes.txt').write_text('Keep my work')
    before = {str(p.relative_to(one)): p.read_bytes() for p in one.rglob('*') if p.is_file()}
    two = launch(tmp_path)
    assert one != two and one.parent == two.parent == tmp_path
    assert {str(p.relative_to(one)): p.read_bytes() for p in one.rglob('*') if p.is_file()} == before
    assert not any('coach' in str(p.relative_to(two)) or 'reference' in p.name for p in two.rglob('*'))
    assert (two / 'solution.py').is_file()
    assert (two / 'pyproject.toml').is_file() and (two / 'uv.lock').is_file()
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', 'tests/test_stage1.py'],
                            cwd=two, capture_output=True, text=True)
    assert result.returncode == 1 and 'NotImplementedError' in result.stdout


def test_reference_passes_all_disclosed_stage_tests(tmp_path):
    attempt = launch(tmp_path)
    reference = ROOT / 'exercises/coach/progressive.py'
    assert reference.is_file(), 'Instructor reference must exist separately.'
    (attempt / 'solution.py').write_text(reference.read_text())
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=attempt,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def reference():
    path = ROOT / 'exercises/coach/progressive.py'
    assert path.is_file(), 'Missing instructor reference'
    spec = importlib.util.spec_from_file_location('progressive_reference', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.summarize


def test_progressive_reference_replay_partial_refunds_and_isolation():
    summarize = reference()
    rows = [
        {'id': 'p1', 'type': 'purchase', 'merchant': 'A', 'amount': 1000},
        {'id': 'p2', 'type': 'purchase', 'merchant': 'B', 'amount': 500},
        {'id': 'r1', 'type': 'refund', 'purchase_id': 'p1', 'amount': 300},
        {'id': 'r2', 'type': 'refund', 'purchase_id': 'p1', 'amount': 700},
    ]
    before = copy.deepcopy(rows)
    assert summarize(rows + [dict(rows[2])]) == {'A': 0, 'B': 500}
    assert rows == before
    assert summarize([]) == {}
    assert summarize([rows[0]]) == {'A': 1000}
    for extra in [
        {'id': 'p1', 'type': 'purchase', 'merchant': 'B', 'amount': 1000},
        {'id': 'r1', 'type': 'refund', 'purchase_id': 'p2', 'amount': 300},
        {'id': 'r3', 'type': 'refund', 'purchase_id': 'p1', 'amount': 1},
        {'id': 'r3', 'type': 'refund', 'purchase_id': 'unknown', 'amount': 1},
    ]:
        sample = rows + [extra]
        original = copy.deepcopy(sample)
        with pytest.raises(ValueError):
            summarize(sample)
        assert sample == original
    with pytest.raises(ValueError):
        summarize([rows[2], rows[0]])
