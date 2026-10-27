"""The test runner appended to every Pybites OOP starter.

The judge saves the learner's editor as ``Solution.py``. For each judge test the
runner loads that file again as a fresh module under the name the Pybites tests
import (for example ``simple_property``), runs the tests in file order up to the
requested one (earlier tests can leave class-level state, as in pytest), and
returns ``"passed"`` or a short failure report. A minimal ``pytest`` stand-in
covers ``raises``, ``mark.parametrize``, ``fixture``, ``approx``, ``fail``, and
the ``capsys``, ``monkeypatch``, and ``tmp_path`` fixtures.
"""

RUNNER = r'''

# ---------------------------------------------------------------------------
# Test runner (supplied). It runs the pytest tests above on your code.
# ---------------------------------------------------------------------------
import contextlib as _contextlib
import importlib.util as _importlib_util
import inspect as _inspect
import io as _io
import itertools as _itertools
import linecache as _linecache
import re as _re
import sys as _sys
import tempfile as _tempfile
import traceback as _traceback
import types as _types
from collections import namedtuple as _namedtuple
from pathlib import Path as _Path


class _RaisesContext:
    def __init__(self, expected, match=None):
        self.expected, self.match = expected, match
        self.value = self.type = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise AssertionError(f"DID NOT RAISE {self.expected}")
        if not issubclass(exc_type, self.expected):
            return False
        if self.match is not None and not _re.search(self.match, str(exc)):
            raise AssertionError(f"Regex {self.match!r} does not match {str(exc)!r}")
        self.value, self.type = exc, exc_type
        return True


class _Approx:
    def __init__(self, expected, rel=1e-6, abs=1e-12):
        self.expected, self.rel, self.abs = expected, rel, abs

    def __eq__(self, actual):
        return abs(actual - self.expected) <= max(self.rel * abs(self.expected), self.abs)

    def __repr__(self):
        return f"approx({self.expected!r})"


def _fixture(function=None, **options):
    def mark(f):
        f._pb_fixture = options.get("scope", "function")
        return f
    return mark(function) if callable(function) else mark


def _parametrize(names, values, ids=None):
    def mark(f):
        f._pb_params = [(names, list(values), ids)] + getattr(f, "_pb_params", [])
        return f
    return mark


def _fail(message=""):
    raise AssertionError(message)


def _make_pytest():
    module = _types.ModuleType("pytest")
    module.raises = _RaisesContext
    module.approx = _Approx
    module.fixture = _fixture
    module.fail = _fail
    module.mark = _types.SimpleNamespace(parametrize=_parametrize)
    return module


_Captured = _namedtuple("CaptureResult", "out err")


class _CapSys:
    def __init__(self, buffer):
        self._buffer = buffer

    def readouterr(self):
        out = self._buffer.getvalue()
        self._buffer.seek(0)
        self._buffer.truncate()
        return _Captured(out, "")


class _MonkeyPatch:
    def __init__(self):
        self._undo = []

    def setattr(self, target, name, value=None):
        if isinstance(target, str):
            module_name, _, attr = target.rpartition(".")
            target, name, value = _sys.modules[module_name], attr, name
        self._undo.append((target, name, getattr(target, name, _MISSING)))
        setattr(target, name, value)

    def setitem(self, mapping, key, value):
        self._undo.append((mapping, key, mapping.get(key, _MISSING), "item"))
        mapping[key] = value

    def undo(self):
        for entry in reversed(self._undo):
            target, name, old = entry[:3]
            if len(entry) == 4:
                if old is _MISSING:
                    target.pop(name, None)
                else:
                    target[name] = old
            elif old is _MISSING:
                delattr(target, name)
            else:
                setattr(target, name, old)


_MISSING = object()


def _expand(name, function):
    """Yield (test id, function, parameter values) in pytest order."""
    params = getattr(function, "_pb_params", [])
    if not params:
        yield name, {}
        return
    groups = []
    for names, values, ids in params:
        names = [n.strip() for n in names.split(",")] if isinstance(names, str) else list(names)
        group = []
        for index, value in enumerate(values):
            row = dict(zip(names, value if len(names) > 1 else [value]))
            label = ids[index] if ids else "-".join(
                str(v) if isinstance(v, (str, int, float, bool, type(None))) else f"{k}{index}"
                for k, v in row.items())
            group.append((label, row))
        groups.append(group)
    for combo in _itertools.product(*reversed(groups)):
        row = {}
        for _, part in combo:
            row.update(part)
        yield f"{name}[{'-'.join(label for label, _ in combo)}]", row


def _call(function, namespace, given, buffer, cleanups, cache):
    kwargs = {}
    for arg in _inspect.signature(function).parameters:
        if arg in given:
            kwargs[arg] = given[arg]
        elif arg == "capsys":
            kwargs[arg] = _CapSys(buffer)
        elif arg == "monkeypatch":
            patch = _MonkeyPatch()
            cleanups.append(patch.undo)
            kwargs[arg] = patch
        elif arg == "tmp_path":
            kwargs[arg] = _Path(_tempfile.mkdtemp())
        elif getattr(namespace.get(arg), "_pb_fixture", None):
            fixture = namespace[arg]
            if fixture._pb_fixture != "function" and arg in cache:
                kwargs[arg] = cache[arg]
                continue
            value = _call(fixture, namespace, given, buffer, cleanups, cache)
            if _inspect.isgenerator(value):
                generator, value = value, next(value)
                cleanups.append(lambda g=generator: next(g, None))
            if fixture._pb_fixture != "function":
                cache[arg] = value
            kwargs[arg] = value
        else:
            raise TypeError(f"unknown fixture {arg!r}")
    return function(**kwargs)


def _report(test_id, error, test_file):
    lines = [f"FAILED {test_id}", f"{type(error).__name__}: {error}".rstrip(": ")]
    frames = [f for f in _traceback.extract_tb(error.__traceback__) if f.filename == test_file]
    if frames:
        lines.append(f"test line {frames[-1].lineno}: {frames[-1].line}")
    # The judge keeps one output line per test.
    return " | ".join(line.replace("\n", "\\n") for line in lines)


def solve(data):
    target = data["test"]
    here = _Path(__file__)
    spec = _importlib_util.spec_from_file_location(_PB_MODULE, here)
    module = _importlib_util.module_from_spec(spec)
    _sys.modules[_PB_MODULE] = module
    _sys.modules["pytest"] = _make_pytest()
    buffer = _io.StringIO()
    try:
        with _contextlib.redirect_stdout(buffer):
            spec.loader.exec_module(module)
    except Exception as error:
        return f"FAILED {target} | Your code raised while loading: {type(error).__name__}: {error}".replace("\n", " ")
    test_file = f"test_{_PB_MODULE}.py"
    _linecache.cache[test_file] = (len(_PB_TESTS), None, _PB_TESTS.splitlines(True), test_file)
    namespace = {"__name__": f"test_{_PB_MODULE}", "__file__": test_file}
    try:
        exec(compile(_PB_TESTS, test_file, "exec"), namespace)
    except Exception as error:
        return _report(target, error, test_file)
    cache, seen = {}, []
    for name, function in list(namespace.items()):
        if not (name.startswith("test") and _inspect.isfunction(function)):
            continue
        for test_id, given in _expand(name, function):
            cleanups = []
            buffer = _io.StringIO()
            try:
                with _contextlib.redirect_stdout(buffer):
                    _call(function, namespace, given, buffer, cleanups, cache)
                result = "passed"
            except Exception as error:
                result = _report(test_id, error, test_file)
            finally:
                for cleanup in reversed(cleanups):
                    cleanup()
            seen.append(test_id)
            if test_id == target:
                return result
    if target == "--list":
        import json
        return json.dumps(seen)
    return f"Unknown test: {target}"


class Solution:
    def run(self, payload: str) -> str:
        import json
        return solve(json.loads(payload))
'''

MARKER = '''class Marker {
    // Every test passes when the runner reports "passed" for it.
    public String run(String payload) { return "passed"; }
    public boolean isCorrect(String payload, String output) { return "passed".equals(output); }
}
'''
