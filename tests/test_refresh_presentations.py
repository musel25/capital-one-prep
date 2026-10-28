import json


def test_refresh_preserves_judge_inputs_and_code(tmp_path):
    from scripts.refresh_custom_presentations import refresh_problem

    metadata = {'id': 'vehicle', 'starterCode': {'python': 'class Vehicle: pass'},
                'testCases': [{'payload': '{"test":"test_vehicle"}'}],
                'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
                'examples': [{'input': '{"test":"test_vehicle"}', 'output': 'passed'}]}
    (tmp_path / 'metadata.json').write_text(json.dumps(metadata))
    (tmp_path / 'statement.md').write_text('Old task')
    (tmp_path / 'official-tests.json').write_text('[{"payload":"unchanged"}]')
    presentation = {'statement': 'Build a Vehicle.\n',
                    'examples': [{'input': 'Vehicle("Toyota", "Corolla", 4).description()', 'output': "'Toyota Corolla with 4 wheels'"}],
                    'testCaseDescriptions': {'test_vehicle': {'title': 'test_vehicle', 'code': 'assert vehicle.wheels == 4'}},
                    'courseHelp': {'title': 'Course help', 'body': 'Keep the supplied tests.'}}
    refresh_problem(tmp_path, presentation)
    current = json.loads((tmp_path / 'metadata.json').read_text())
    assert current['starterCode'] == metadata['starterCode']
    assert current['testCases'] == metadata['testCases']
    assert current['functionName'] == metadata['functionName']
    assert current['params'] == metadata['params']
    assert current['examples'] == presentation['examples']
    assert (tmp_path / 'statement.md').read_text() == 'Build a Vehicle.\n'
    assert (tmp_path / 'official-tests.json').read_text() == '[{"payload":"unchanged"}]'
