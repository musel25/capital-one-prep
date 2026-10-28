"""Build and test the seven exercises with real, bundled CLI libraries."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.pybites.runner import MARKER
from cojudge.pybites.support import description, full_source
from cojudge.presentation import course_help, statement_text, test_case_details
from cojudge.typer_path.presentation import CLARIFICATIONS, EXAMPLES

HERE = Path(__file__).parent
COURSE_ID = 'pybites-typer'
CATEGORIES = ['01-cli-basics', '02-options-and-callbacks', '03-rich-and-prompts']


def load_specs():
    from cojudge.typer_path.bites import SPECS
    pages = json.loads((HERE / 'source-pages.json').read_text())
    return [{**spec, 'number': page['n'], 'page': page,
             'id': f"pbty-{page['n']:02d}-{page['slug']}", 'title': page['title'],
             'category': CATEGORIES[0 if page['n'] <= 3 else 1 if page['n'] <= 5 else 2]}
            for spec, page in zip(SPECS, pages, strict=True)]


def run_all(spec, code):
    with tempfile.TemporaryDirectory(prefix='typer-path-') as folder:
        work = Path(folder)
        shutil.copyfile(HERE / 'python-libs.zip', work / 'python-libs.zip')
        (work / 'Solution.py').write_text(full_source(spec, code))
        (work / 'check.py').write_text(
            "import sys, json\nsys.path.insert(0, 'python-libs.zip')\nfrom Solution import Solution\n"
            "run = Solution().run\nids = json.loads(run(json.dumps({'test': '--list'})))\n"
            "print(json.dumps({i: run(json.dumps({'test': i})) for i in ids}))\n")
        done = subprocess.run(['uv', 'run', '--no-project', '--python', '3.11', 'python', '-S', 'check.py'],
                              cwd=folder, capture_output=True, text=True, timeout=120)
        assert done.returncode == 0, f"{spec['id']} runner crashed: {done.stderr[-3000:]}"
        return json.loads(done.stdout.strip().splitlines()[-1])


def verify(spec):
    results = run_all(spec, spec['reference'])
    failures = {name: value for name, value in results.items() if value != 'passed'}
    assert results and not failures, f"{spec['id']} reference fails: {failures}"
    template = run_all(spec, spec['template'])
    assert any(value != 'passed' for value in template.values()), 'Template passed all tests'
    mutations = []
    for fault in spec['mutations']:
        assert fault['old'] in spec['reference'], f"Missing mutation target: {fault['name']}"
        bad = spec['reference'].replace(fault['old'], fault['new'], 1)
        faulty = run_all(spec, bad)
        detected = [name for name, value in faulty.items() if value != 'passed']
        assert detected, f"Mutation survived: {fault['name']}"
        mutations.append({'name': fault['name'], 'detected_by': detected})
    return {'id': spec['id'], 'cases': len(results), 'tests': list(results),
            'template_failures': sum(value != 'passed' for value in template.values()), 'mutations': mutations}


def present_problem(spec, test_ids):
    return {
        'statement': statement_text(description(spec), CLARIFICATIONS[spec['number']]),
        'examples': [{'input': code, 'output': result} for code, result in EXAMPLES[spec['number']]],
        'testCaseDescriptions': test_case_details(spec['tests'], test_ids),
        'courseHelp': course_help(f"https://pybitesplatform.com/bites/{spec['page']['slug']}/",
            'These templates and tests are recreations from the public descriptions. '
            'Real Typer, Click, and Rich packages are bundled for offline use. Use Run '
            'and Submit; the playground and debugger do not load the library archive. '
            'Keep script entry points inside `if __name__ == "__main__":`. The runner '
            'supports the pytest features used by the supplied tests. Select Python.'),
    }


def statement(spec, count):
    return present_problem(spec, [])['statement']


def build(destination=ROOT / 'cojudge'):
    specs, records = load_specs(), []
    for spec in specs:
        result = verify(spec)
        folder = Path(destination) / 'problems' / spec['id']
        folder.mkdir(parents=True, exist_ok=True)
        payloads = [json.dumps({'test': name}) for name in result['tests']]
        presentation = present_problem(spec, result['tests'])
        metadata = {
            'id': spec['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
            'difficulty': 'Easy' if spec['number'] <= 3 else 'Medium', 'link': '',
            'category': spec['category'], 'pythonDependencies': True,
            'starterCode': {'python': full_source(spec, spec['template'])},
            **{key: value for key, value in presentation.items() if key != 'statement'},
            'testCases': [{'payload': p} for p in payloads[:3]], 'functionName': 'run',
            'params': [{'name': 'payload', 'type': 'string'}], 'outputType': 'string', 'hints': [],
        }
        write_json(folder / 'metadata.json', metadata)
        write_json(folder / 'official-tests.json', [{'payload': p} for p in payloads])
        (folder / 'statement.md').write_text(presentation['statement'])
        (folder / 'Marker.java').write_text(MARKER)
        (folder / 'solution.md').write_text(
            '## Reference solution\n\nPaste above the supplied tests and runner.\n\n```python\n' +
            spec['reference'].strip() + '\n```\n')
        shutil.copyfile(HERE / 'python-libs.zip', folder / 'python-libs.zip')
        records.append(result)
        print(f"PASS {spec['id']} ({result['cases']} tests)", flush=True)
    course = Path(destination) / 'courses' / COURSE_ID
    course.mkdir(parents=True, exist_ok=True)
    write_json(course / 'courseinfo.json', {
        'title': 'Pybites Typer Path',
        'description': 'The seven exercises of the Pybites Typer learning path, in the source order. '
                       'Practice arguments, commands, progress bars, options, callbacks, Rich tables, '
                       'and password prompts. Recreated templates and tests. Real libraries are bundled '
                       'for offline use. Select Python.',
        'category-order': CATEGORIES,
        'problems-of-category': {category: [s['id'] for s in specs if s['category'] == category]
                                 for category in CATEGORIES},
    })
    write_json(HERE / 'verification.json', records)
    return records
