"""Platform contracts; intentionally broken learner apps are verified separately."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def cli(*args):
    return subprocess.run([sys.executable, str(ROOT / 'scripts/practice.py'), *args],
                          cwd=ROOT, capture_output=True, text=True)


def test_list_exposes_original_tasks_and_four_larger_mock_tasks():
    result = cli('list', '--json')
    assert result.returncode == 0, result.stderr
    tasks = json.loads(result.stdout)
    assert {x['id'] for x in tasks} == {
        f'd{day:02d}-{kind}' for day in range(1, 11) for kind in ('bug', 'feature')
    } | {'mock-support-bug', 'mock-support-feature', 'mock-dispatch-bug', 'mock-dispatch-feature'}


def test_invalid_task_cannot_escape_attempts(tmp_path):
    result = cli('start', '../../outside', '--output-root', str(tmp_path))
    assert result.returncode == 2
    assert 'unknown task' in result.stderr.lower()
    assert not list(tmp_path.iterdir())


def test_current_and_archived_planner_labs_resolve_to_preserved_catalog():
    from exercises.catalog import BY_ID
    plan = json.loads((ROOT / 'curriculum/plan.json').read_text())
    blocks = [b for d in plan['days'] for b in d['blocks']] + plan['archivedBlocks']
    linked = {task for block in blocks for task in block.get('labs', [])}
    assert linked == set(BY_ID)


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


def legacy_at(tmp_path, task):
    from scripts.practice import build
    attempt = tmp_path / task
    build(task, attempt, revision=1)
    return attempt


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
    attempt = legacy_at(tmp_path, 'd06-bug')
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
    attempt = legacy_at(tmp_path, 'd06-bug')
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
    assert len(report) == 24
    assert all(item['starter_fails'] and item['reference_passes'] for item in report)
    assert all(item['public_starter_passes'] and item['public_reference_passes'] for item in report)


def test_remaining_tasks_use_unfamiliar_applications():
    tasks = json.loads(cli('list', '--json').stdout)
    remaining = [task for task in tasks if task['id'].startswith('d') and task['id'] > 'd02-bug']
    assert len(remaining) == 17
    assert len({task['context'] for task in remaining}) == 17
    assert all(task['context'] != 'bank' for task in remaining)


def test_interview_mode_separates_contract_and_guided_mode_reveals_it(tmp_path):
    from exercises.catalog import BY_ID
    task = BY_ID['d02-feature']
    attempt = start_at(tmp_path, task.id)
    brief = (attempt / 'README.md').read_text()
    answers = (attempt / 'CLARIFICATIONS.md').read_text()
    assert task.brief in brief
    assert task.contract not in brief and task.probe not in brief
    assert task.contract in answers and task.probe in answers
    assert 'CLARIFICATIONS.md' in brief
    guided = cli('start', task.id, '--mode', 'guided', '--output-root', str(tmp_path), '--json')
    assert guided.returncode == 0, guided.stderr
    guided_brief = (Path(json.loads(guided.stdout)['path']) / 'README.md').read_text()
    assert task.contract in guided_brief


def test_new_attempt_manifest_and_public_behavior_tests(tmp_path):
    attempt = start_at(tmp_path, 'd02-feature')
    marker = json.loads((attempt / '.practice.json').read_text())
    assert marker['schema_version'] == 2 and marker['catalog_revision'] == 2
    assert (attempt / 'tests/test_existing.py').is_file()
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=attempt,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert cli('check', str(attempt)).returncode == 1


@pytest.mark.parametrize('context', ['support', 'dispatch'])
def test_large_mock_bug_and_feature_are_independent_and_preserve_existing_work(tmp_path, context):
    bug = start_at(tmp_path, f'mock-{context}-bug')
    (bug / 'NOTES.md').write_text('Keep my diagnosis and unfinished work.')
    before = digests(bug)
    feature = start_at(tmp_path, f'mock-{context}-feature')
    assert bug != feature and digests(bug) == before
    assert len(list((feature / 'app').glob('*.py'))) >= 10
    assert not any('coach' in str(p.relative_to(feature)) or 'reference' in str(p.relative_to(feature)) for p in feature.rglob('*'))
    assert cli('check', str(bug)).returncode == 1
    assert cli('check', str(feature)).returncode == 1


def test_old_replaced_task_keeps_original_contract_without_editing_attempt(tmp_path):
    from scripts.practice import build
    attempt = tmp_path / 'legacy-history'
    build('d02-feature', attempt, reference=True, revision=1)
    marker = json.loads((attempt / '.practice.json').read_text())
    assert marker == {'schema_version': 1, 'task_id': 'd02-feature'}
    assert 'transfer history' in (attempt / 'README.md').read_text().lower()
    before = digests(attempt)
    result = cli('check', str(attempt), '--json')
    assert result.returncode == 0, result.stdout + result.stderr
    assert digests(attempt) == before


@pytest.mark.parametrize('task, source, original, incorrect', [
    ('mock-support-feature', 'app/assignments.py', "'current': agent['id']", "'current': None"),
    ('mock-dispatch-bug', 'app/quotes.py', "'signature_cents': signature_cents", "'signature_cents': 0"),
    ('mock-dispatch-feature', 'app/orders.py', "record(store, order_id, 'cancelled', {'items': order['items']})", "record(store, order_id, 'cancelled', {})"),
    ('mock-dispatch-feature', 'app/shipments.py', "raise HTTPException(409, 'Order must be reserved before shipment')", "record(store, order['id'], 'shipped', {})\n        raise HTTPException(409, 'Order must be reserved before shipment')"),
])
def test_mock_checks_detect_incorrect_output_and_rejected_request_side_effects(tmp_path, task, source, original, incorrect):
    from scripts.practice import build
    attempt = tmp_path / task
    build(task, attempt, reference=True)
    target = attempt / source
    text = target.read_text()
    assert original in text
    target.write_text(text.replace(original, incorrect))
    result = cli('check', str(attempt), '--json')
    assert result.returncode == 1, result.stdout + result.stderr
    assert json.loads(result.stdout)['status'] == 'failed'


@pytest.mark.parametrize('revision', [None, True, '2', 3, [], {}])
def test_unsupported_catalog_revision_is_reported_as_setup_error(tmp_path, revision):
    attempt = start_at(tmp_path)
    (attempt / '.practice.json').write_text(json.dumps({
        'schema_version': 2, 'task_id': 'd01-bug', 'catalog_revision': revision,
    }))
    result = cli('check', str(attempt))
    assert result.returncode == 2
    assert 'traceback' not in result.stderr.lower()
