"""Platform contracts; intentionally broken learner apps are verified separately."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cli(*args):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/practice.py'), *args],
                          cwd=ROOT, capture_output=True, text=True)


def test_list_exposes_twenty_independent_tasks():
    result = cli('list', '--json')
    assert result.returncode == 0, result.stderr
    tasks = json.loads(result.stdout)
    assert {x['id'] for x in tasks} == {
        f'd{day:02d}-{kind}' for day in range(1, 11) for kind in ('bug', 'feature')
    }


def test_invalid_task_cannot_escape_attempts(tmp_path):
    result = cli('start', '../../outside', '--output-root', str(tmp_path))
    assert result.returncode == 2
    assert 'unknown task' in result.stderr.lower()
    assert not list(tmp_path.iterdir())


def test_repeated_start_preserves_work_and_never_copies_coach(tmp_path):
    first = cli('start', 'd01-bug', '--output-root', str(tmp_path), '--json')
    assert first.returncode == 0, first.stderr
    one = Path(json.loads(first.stdout)['path'])
    (one / 'my-solution.txt').write_text('keep my work')
    second = cli('start', 'd01-bug', '--output-root', str(tmp_path), '--json')
    assert second.returncode == 0, second.stderr
    two = Path(json.loads(second.stdout)['path'])
    assert one != two and one.parent == two.parent == tmp_path
    assert (one / 'my-solution.txt').read_text() == 'keep my work'
    names = [str(p.relative_to(two)).lower() for p in two.rglob('*')]
    assert not any('coach' in p or 'reference' in p or 'solution' in p for p in names)
    assert (two / 'app/main.py').is_file()
    assert (two / 'app/static/app.js').is_file()
    assert (two / 'tests/test_smoke.py').is_file()


def test_check_rejects_unmarked_paths(tmp_path):
    result = cli('check', str(tmp_path))
    assert result.returncode == 2
    assert 'manifest' in result.stderr.lower()


def start_at(tmp_path, task='d01-bug'):
    result = cli('start', task, '--output-root', str(tmp_path), '--json')
    assert result.returncode == 0, result.stderr
    return Path(json.loads(result.stdout)['path'])


def digests(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob('*') if p.is_file()}


def test_check_executes_real_faulty_behavior_without_touching_attempt(tmp_path):
    attempt = start_at(tmp_path)
    (attempt / 'NOTES.md').write_text('Private learner notes: preserve exactly.')
    before = digests(attempt)
    result = cli('check', str(attempt), '--json')
    assert result.returncode == 1, result.stdout + result.stderr
    body = json.loads(result.stdout)
    assert body['status'] == 'failed' and body['task_id'] == 'd01-bug'
    assert digests(attempt) == before
    assert not list(attempt.rglob('__pycache__'))


def test_check_verifies_a_learner_fix_and_reports_import_errors_separately(tmp_path):
    attempt = start_at(tmp_path, 'd06-bug')
    service = attempt / 'app/service.py'
    service.write_text(service.read_text().replace("'balance': amount", "'balance_cents': amount"))
    passed = cli('check', str(attempt), '--json')
    assert passed.returncode == 0, passed.stdout + passed.stderr
    assert json.loads(passed.stdout)['status'] == 'passed'
    service.write_text('this is invalid Python!')
    broken = cli('check', str(attempt), '--json')
    assert broken.returncode == 2
    assert json.loads(broken.stdout)['status'] == 'error'


def test_check_rejects_traversal_in_manifest_and_symlinked_source(tmp_path):
    attempt = start_at(tmp_path)
    marker = attempt / '.practice.json'
    marker.write_text(json.dumps({'schema_version': 1, 'task_id': '../../outside'}))
    assert cli('check', str(attempt)).returncode == 2
    marker.write_text(json.dumps({'schema_version': 1, 'task_id': 'd01-bug'}))
    (attempt / 'unexpected-link').symlink_to(ROOT / 'pyproject.toml')
    rejected = cli('check', str(attempt))
    assert rejected.returncode == 2
    assert 'symlink' in rejected.stderr.lower()


def test_bad_manifest_type_is_a_setup_error_without_a_traceback(tmp_path):
    attempt = start_at(tmp_path)
    (attempt / '.practice.json').write_text(json.dumps({'schema_version': 1, 'task_id': ['d01-bug']}))
    result = cli('check', str(attempt))
    assert result.returncode == 2
    assert 'traceback' not in result.stderr.lower()


def test_learner_module_cannot_accidentally_shadow_external_coach(tmp_path):
    attempt = start_at(tmp_path)
    (attempt / 'contracts.py').write_text("CHECKS = {'d01-bug': lambda: None}\n")
    result = cli('check', str(attempt), '--json')
    assert result.returncode == 1
    assert json.loads(result.stdout)['status'] == 'failed'


def test_missing_browser_asset_is_reported_even_after_business_fix(tmp_path):
    attempt = start_at(tmp_path, 'd06-bug')
    service = attempt / 'app/service.py'
    service.write_text(service.read_text().replace("'balance': amount", "'balance_cents': amount"))
    (attempt / 'app/static/app.js').unlink()
    result = cli('check', str(attempt), '--json')
    assert result.returncode == 1
    assert json.loads(result.stdout)['status'] == 'failed'


def test_all_starters_fail_target_contract_and_references_pass():
    result = cli('verify', '--json')
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert len(report) == 20
    assert all(item['starter_fails'] and item['reference_passes'] for item in report)
