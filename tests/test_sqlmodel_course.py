"""Check the course against real SQLModel and FastAPI behavior."""
import importlib


def support():
    try:
        return importlib.import_module('cojudge.sqlmodel_path.support')
    except ModuleNotFoundError:
        assert False, 'The SQLModel course builder is missing'


def test_complete_course_keeps_the_supplied_order():
    course = support()
    specs = course.load_specs()
    assert len(specs) == 10
    assert [s['number'] for s in specs] == list(range(1, 11))
    info = course.course_info(specs)
    assert [p for group in info['problems-of-category'].values() for p in group] == [course.problem_id(s) for s in specs]


def test_references_pass_and_starters_and_faults_fail():
    course = support()
    for spec in course.load_specs():
        result = course.verify(spec)
        assert result['cases'] >= 5
        assert result['template_failures']
        assert result['mutations']
        assert all(m['detected_by'] for m in result['mutations'])


def test_runner_repeats_with_fresh_database_state():
    course = support()
    spec = course.load_specs([9])[0]
    assert course.run_all(spec, spec['reference']) == course.run_all(spec, spec['reference'])


def test_unknown_test_cannot_pass():
    course = support()
    spec = course.load_specs([1])[0]
    result = course.run_all(spec, spec['reference'], target='missing-test')
    assert result != 'passed'


def test_collection_errors_fail_all_expected_tests():
    course = support()
    spec = course.load_specs([1])[0]
    spec['tests'] += '\nimport missing_sqlmodel_course_dependency\n'
    results = course.run_all(spec, spec['reference'])
    assert results and all(value != 'passed' for value in results.values())
    assert any('missing_sqlmodel_course_dependency' in value for value in results.values())


def test_skipped_tests_cannot_pass():
    course = support()
    spec = course.load_specs([1])[0]
    spec['tests'] = spec['tests'].replace(
        'assert app.Workout.__tablename__ == "workout"', 'pytest.skip("not implemented")')
    results = course.run_all(spec, spec['reference'])
    assert results['test_workout_table_fields'] != 'passed'


def test_advanced_api_samples_detect_unfinished_new_endpoints():
    course = support()
    spec = course.load_specs([10])[0]
    results = course.run_all(spec, spec['template'])
    assert any(results[name] != 'passed' for name in course.test_ids(spec)[:3])
