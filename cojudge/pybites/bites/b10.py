"""Bite: Complete a tox ini file parser class (recreated tests and template)."""

SPEC = {
    "title": "Complete a tox ini file parser class",
    "module": "ini",
    "contract": "The input is the path to a readable, valid INI file with a [tox] section. "
                "DEFAULT options, interpolation, malformed files, and missing files are outside this exercise. "
                "Count named sections. envlist can be absent or empty; split it on commas and newlines, "
                "strip whitespace, discard empty items, and remove duplicates in first-seen order. "
                "Do not expand tox brace expressions. Each basepython value is one interpreter name. "
                "Return nonempty basepython values once in section order. Matching is case-sensitive. "
                "Expose config and the three read-only properties from the template.",
    "notes": "The tests write sample tox ini files to a temporary folder and pass the file path, "
             "as in the description's REPL example. The first sample has the same shape as the "
             "Django tox file in that example.",
    "template": '''import configparser

# FOCUS: load the file with configparser and write the three read-only properties by hand.
# SUPPLIED: the two list helpers below do the splitting and the duplicate removal.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _unique(values):
    """Drop None, empty strings and repeats. Keep first-seen order: ['a', None, 'a', 'b'] -> ['a', 'b']."""
    return [value for value in dict.fromkeys(values) if value]


def _split_list(text):
    """Split on commas and newlines, strip spaces, then _unique: 'a, b\\n c,a' -> ['a', 'b', 'c']."""
    return _unique(item.strip() for item in text.replace("\\n", ",").split(","))


class ToxIniParser:

    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        pass

    @property
    def number_of_sections(self):
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/articles/property-decorator
        """
        pass

    @property
    def environments(self):
        """Return a list of environments
           (= "envlist" attribute of [tox] section; it can be missing).
           Use _split_list."""
        pass

    @property
    def base_python_versions(self):
        """Return a list of all basepython values across the ini file,
           each value once, in the order they first appear. Use _unique."""
        pass
''',
    "tests": '''import pytest

from ini import ToxIniParser

django = """
[tox]
minversion = 3.18
skipsdist = true
envlist =
    py3
    flake8
    docs
    isort

[testenv]
usedevelop = true
passenv = DJANGO_SETTINGS_MODULE PYTHONPATH HOME DISPLAY
setenv =
    PYTHONDONTWRITEBYTECODE=1
deps =
    py{3,36,37}: -rtests/requirements/py3.txt
changedir = tests
commands =
    {envpython} runtests.py {posargs}

[testenv:flake8]
basepython = python3
usedevelop = false
deps = flake8
changedir = {toxinidir}
commands = flake8 .

[testenv:docs]
basepython = python3
usedevelop = false
allowlist_externals =
    make
deps =
    Sphinx
    pyenchant
    sphinxcontrib-spelling
changedir = docs
commands =
    make spelling

[testenv:isort]
basepython = python3
usedevelop = false
deps = isort
changedir = {toxinidir}
commands = isort --check-only --diff django tests scripts

[testenv:javascript]
usedevelop = false
deps =
changedir = {toxinidir}
whitelist_externals = npm
commands =
    npm install
    npm test

[flake8]
exclude = build,.git,.tox
max-line-length = 119
"""

library = """
[tox]
envlist = py38, py39, py310, py311, pypy3, lint, docs

[testenv]
deps = pytest
commands = pytest {posargs}

[testenv:pypy3]
basepython = pypy3

[testenv:lint]
basepython = python3.11
deps = ruff
commands = ruff check .

[testenv:docs]
basepython = python3.11
deps = sphinx
commands = sphinx-build docs docs/_build
"""

mixed = """
[tox]
envlist = py39,py310,
    coverage, py39

[testenv]
basepython = python3.10
commands = pytest

[testenv:coverage]
basepython = python3.9
commands = coverage report

[testenv:report]
basepython = python3.10
commands = coverage html
"""


@pytest.fixture
def make_parser(tmp_path):
    def make(text, name="tox.ini"):
        path = tmp_path / name
        path.write_text(text)
        return ToxIniParser(str(path))
    return make


def test_django(make_parser):
    tox = make_parser(django)
    assert tox.number_of_sections == 7
    assert tox.environments == ['py3', 'flake8', 'docs', 'isort']
    assert tox.base_python_versions == ['python3']


def test_comma_separated_envlist(make_parser):
    tox = make_parser(library)
    assert tox.number_of_sections == 5
    assert tox.environments == ['py38', 'py39', 'py310', 'py311', 'pypy3', 'lint', 'docs']
    assert tox.base_python_versions == ['pypy3', 'python3.11']


def test_commas_and_newlines_mixed(make_parser):
    tox = make_parser(mixed)
    assert tox.number_of_sections == 4
    assert tox.environments == ['py39', 'py310', 'coverage']
    assert tox.base_python_versions == ['python3.10', 'python3.9']


def test_no_basepython(make_parser):
    tox = make_parser("[tox]\\nenvlist = py311\\n\\n[testenv]\\ncommands = pytest\\n")
    assert tox.number_of_sections == 2
    assert tox.environments == ['py311']
    assert tox.base_python_versions == []


def test_config_attribute_and_properties(make_parser):
    tox = make_parser(library)
    assert hasattr(tox, 'config')
    for name in ('number_of_sections', 'environments', 'base_python_versions'):
        assert isinstance(ToxIniParser.__dict__[name], property)


@pytest.mark.parametrize('text', ['[tox]\\n', '[tox]\\nenvlist = , ,\\n    ,\\n'])
def test_missing_or_empty_envlist(make_parser, text):
    tox = make_parser(text)
    assert tox.number_of_sections == 1
    assert tox.environments == []
    assert tox.base_python_versions == []


def test_blank_basepython_and_case_sensitive_names(make_parser):
    tox = make_parser("""[tox]
envlist = py311, Py311, py311, py{310,311}
[testenv]
basepython =
[testenv:first]
basepython = python3
[testenv:second]
basepython = Python3
[testenv:third]
basepython = python3
""")
    assert tox.environments == ['py311', 'Py311', 'py{310', '311}']
    assert tox.base_python_versions == ['python3', 'Python3']


def test_instances_do_not_share_config(make_parser):
    first = make_parser(library, 'first.ini')
    second = make_parser('[tox]\\nenvlist = other\\n', 'second.ini')
    assert second.environments == ['other']
    assert first.environments == ['py38', 'py39', 'py310', 'py311', 'pypy3', 'lint', 'docs']
''',
    "hints": [
        "Focus: @property methods that read from self.config. The tests check that each one is a property.",
        "Supplied: _split_list and _unique do the splitting and duplicate removal. Use them.",
        "configparser: config = configparser.ConfigParser(); config.read(path); config.sections(); config[name].get(key, default).",
    ],
    "mutations": [
        {"name": 'envlist_required', "old": 'self.config["tox"].get("envlist", "")', "new": 'self.config["tox"]["envlist"]'},
        {"name": 'count_default_section', "old": 'len(self.config.sections())', "new": 'len(self.config)'},
        {"name": 'keep_duplicate_python_versions', "old": 'return _unique(self.config[s].get("basepython") for s in self.config.sections())', "new": 'return [self.config[s]["basepython"] for s in self.config.sections() if self.config[s].get("basepython")]'},
        {"name": 'shared_config', "old": 'self.config = configparser.ConfigParser(interpolation=None)', "new": 'self.config = ToxIniParser.config = getattr(ToxIniParser, "config", None) or configparser.ConfigParser(interpolation=None)'},
    ],
    "reference": '''import configparser

# FOCUS: load the file with configparser and write the three read-only properties by hand.
# SUPPLIED: the two list helpers below do the splitting and the duplicate removal.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _unique(values):
    """Drop None, empty strings and repeats. Keep first-seen order: ['a', None, 'a', 'b'] -> ['a', 'b']."""
    return [value for value in dict.fromkeys(values) if value]


def _split_list(text):
    """Split on commas and newlines, strip spaces, then _unique: 'a, b\\n c,a' -> ['a', 'b', 'c']."""
    return _unique(item.strip() for item in text.replace("\\n", ",").split(","))


class ToxIniParser:

    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(ini_file)

    @property
    def number_of_sections(self):
        return len(self.config.sections())

    @property
    def environments(self):
        return _split_list(self.config["tox"].get("envlist", ""))

    @property
    def base_python_versions(self):
        return _unique(self.config[s].get("basepython") for s in self.config.sections())
''',
}
