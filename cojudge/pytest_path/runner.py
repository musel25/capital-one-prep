"""Offline test-writing judge. No third-party runtime dependency is required."""
from cojudge.pybites.runner import RUNNER as OOP_RUNNER

# Reuse the same documented pytest subset as the OOP course.
HELPERS = OOP_RUNNER.split('\ndef solve(data):', 1)[0]
# This course needs patch decorators and shared built-in fixtures as well.
start, end = HELPERS.index('\ndef _call('), HELPERS.index('\ndef _report(')
HELPERS = HELPERS[:start] + HELPERS[end:]
HELPERS = HELPERS.replace('return _Captured(out, "")',
    'err = _PT_STDERR.getvalue()\n        _PT_STDERR.seek(0)\n        _PT_STDERR.truncate()\n        return _Captured(out, err)')

ENGINE = r'''
import ast as _ast
import json as _json
from unittest.mock import DEFAULT as _PT_MOCK_DEFAULT


def _call(function, namespace, given, buffer, cleanups, cache):
    kwargs = {}
    # patch supplies positional mock arguments to its wrapped function.
    injected = sum(getattr(patch, 'attribute_name', None) is None
                   and patch.new is _PT_MOCK_DEFAULT
                   for patch in getattr(function, 'patchings', []))
    parameters = list(_inspect.signature(function).parameters)[injected:]
    for arg in parameters:
        if arg in given:
            kwargs[arg] = given[arg]
            continue
        if arg not in cache:
            if arg in ('capsys', 'capfd'):
                value = _CapSys(buffer)
            elif arg == 'monkeypatch':
                value = _MonkeyPatch()
                cleanups.append(value.undo)
            elif arg == 'tmp_path':
                directory = _tempfile.TemporaryDirectory()
                cleanups.append(directory.cleanup)
                value = _Path(directory.name)
            elif getattr(namespace.get(arg), '_pb_fixture', None):
                fixture = namespace[arg]
                value = _call(fixture, namespace, given, buffer, cleanups, cache)
                if _inspect.isgeneratorfunction(fixture):
                    generator, value = value, next(value)
                    cleanups.append(lambda g=generator: next(g, None))
            else:
                raise TypeError(f'unknown fixture {arg!r}')
            cache[arg] = value
        kwargs[arg] = cache[arg]
    return function(**kwargs)


def _pt_module(source):
    module = _types.ModuleType(_PT_MODULE)
    module.__file__ = _PT_MODULE + '.py'
    _sys.modules[_PT_MODULE] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module


def _pt_suite(source, tests):
    """Load a fresh target and suite, then run each test with fresh fixtures."""
    global _PT_STDERR
    old_module = _sys.modules.get(_PT_MODULE, _MISSING)
    old_pytest = _sys.modules.get('pytest', _MISSING)
    old_trace = _sys.gettrace()
    visited, failures, ids = set(), [], []
    filename = _PT_MODULE + '.py'
    def trace(frame, event, arg):
        if event == 'line' and frame.f_code.co_filename == filename:
            visited.add(frame.f_lineno)
        return trace
    try:
        _sys.modules['pytest'] = _make_pytest()
        _sys.settrace(trace)
        with _contextlib.redirect_stdout(_io.StringIO()), _contextlib.redirect_stderr(_io.StringIO()):
            _pt_module(source)
            namespace = {'__name__': 'test_' + _PT_MODULE, '__file__': 'learner_tests.py'}
            _linecache.cache['learner_tests.py'] = (len(tests), None, tests.splitlines(True), 'learner_tests.py')
            try:
                exec(compile(tests, 'learner_tests.py', 'exec'), namespace)
            except Exception as error:
                return {'fatal': _report('collection', error, 'learner_tests.py'), 'ids': []}
            functions = []
            for name, value in list(namespace.items()):
                if name.startswith('test_') and _inspect.isfunction(value):
                    functions.append((name, value))
                elif name.startswith('Test') and _inspect.isclass(value):
                    for method in vars(value):
                        if method.startswith('test_'):
                            functions.append((name + '.' + method, getattr(value(), method)))
            for name, function in functions:
                for test_id, given in _expand(name, function):
                    ids.append(test_id)
                    cleanups = []
                    buffer = _io.StringIO()
                    _PT_STDERR = _io.StringIO()
                    try:
                        with _contextlib.redirect_stdout(buffer), _contextlib.redirect_stderr(_PT_STDERR):
                            # Per-test cache also shares a fixture among its dependencies.
                            _call(function, namespace, given, buffer, cleanups, {})
                    except Exception as error:
                        failures.append(_report(test_id, error, 'learner_tests.py'))
                    finally:
                        for cleanup in reversed(cleanups):
                            try:
                                cleanup()
                            except Exception as error:
                                failures.append(_report(test_id + ' teardown', error, 'learner_tests.py'))
        if not ids:
            return {'fatal': 'FAILED baseline | No test_ functions were collected', 'ids': []}
        tree = _ast.parse(source)
        executable = {node.lineno for node in _ast.walk(tree)
            if isinstance(node, _ast.stmt)
            and not isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef,
                                      _ast.Import, _ast.ImportFrom, _ast.Pass))
            and not (isinstance(node, _ast.Expr) and isinstance(node.value, _ast.Constant)
                     and isinstance(node.value.value, str))}
        coverage = 100 * len(executable & visited) / max(1, len(executable))
        return {'ids': ids, 'failures': failures, 'coverage': coverage,
                'missing': sorted(executable - visited)}
    finally:
        _sys.settrace(old_trace)
        for name, old in ((_PT_MODULE, old_module), ('pytest', old_pytest)):
            if old is _MISSING:
                _sys.modules.pop(name, None)
            else:
                _sys.modules[name] = old


def _pt_grade(tests, case):
    base = _pt_suite(_PT_TARGET, tests)
    if base.get('fatal'):
        return 'FAILED baseline | ' + base['fatal']
    if base['failures']:
        return 'FAILED correct code | ' + base['failures'][0]
    if case == 'baseline':
        if base['coverage'] < 90:
            return f"FAILED coverage | {base['coverage']:.1f}% statement coverage; need 90%; missing lines {base['missing']}"
        return 'passed'
    mutant = next((item for item in _PT_MUTANTS if item['name'] == case), None)
    if mutant is None:
        return 'FAILED | Unknown mutation: ' + case
    changed = _pt_suite(mutant['source'], tests)
    if changed.get('fatal'):
        return 'FAILED mutation collection | ' + changed['fatal']
    if changed['ids'] != base['ids']:
        return 'FAILED | The test collection changed with the target code'
    if not changed['failures']:
        return 'SURVIVED | ' + case + ' | Add a test that detects this fault'
    return 'passed'


# Make the correct module and pytest subset available to the editable tests below.
_sys.modules['pytest'] = _make_pytest()
_pt_module(_PT_TARGET)
'''

ADAPTER = '''
# === END YOUR TESTS ===

# Supplied CoJudge adapter. Keep this section unchanged.
class Solution:
    def run(self, payload: str) -> str:
        text = _Path(__file__).read_text()
        tests = text.split("# === WRITE YOUR TESTS BELOW ===", 1)[1].split("# === END YOUR TESTS ===", 1)[0]
        return _pt_grade(tests, _json.loads(payload)["check"])
'''

MARKER = '''class Marker {
    public String run(String payload) { return "passed"; }
    public boolean isCorrect(String payload, String output) { return "passed".equals(output); }
}
'''
