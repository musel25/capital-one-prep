"""Bite: Write your own data class (recreated tests and template)."""

SPEC = {
    "title": "Write your own data class",
    "module": "bite",
    "contract": "Use an int number and str title and level. Empty strings and zero or negative numbers are allowed. "
                "Do not validate these values. Apply str.capitalize() to title once at construction. "
                "The default level is 'Beginner'. Use a mutable, ordered dataclass with fields number, title, level. "
                "Equality and ordering compare all three fields in that order. Other input types are outside this exercise.",
    "template": '''from dataclasses import dataclass


class Bite:
    pass
''',
    "tests": '''from dataclasses import FrozenInstanceError, astuple, fields, is_dataclass

import pytest

from bite import Bite


@pytest.fixture
def bites():
    return [Bite(3, 'sum of numbers', 'Intermediate'), Bite(1, 'fizz buzz'),
            Bite(2, 'Parse dates', 'Advanced')]


def test_is_dataclass():
    assert is_dataclass(Bite)
    assert [f.name for f in fields(Bite)] == ['number', 'title', 'level']
    assert [f.type for f in fields(Bite)] in ([int, str, str], ['int', 'str', 'str'])


def test_default_level():
    assert Bite(1, 'Fizz buzz').level == 'Beginner'
    assert Bite(1, 'Fizz buzz', 'Advanced').level == 'Advanced'


def test_title_is_capitalized():
    """Hint: __post_init__ runs right after the generated __init__."""
    assert Bite(1, 'sum of numbers').title == 'Sum of numbers'
    assert Bite(2, 'fizz BUZZ').title == 'Fizz buzz'


def test_ordering(bites):
    assert [b.number for b in sorted(bites)] == [1, 2, 3]
    bites.sort()
    assert bites[0].title == 'Fizz buzz'
    assert Bite(1, 'a') < Bite(1, 'b')


def test_repr_and_equality():
    bite = Bite(5, 'parse a list of names')
    assert repr(bite) == "Bite(number=5, title='Parse a list of names', level='Beginner')"
    assert bite == Bite(5, 'Parse a list of names')
    assert bite != Bite(5, 'Parse a list of names', 'Advanced')


def test_mutable_unlike_a_namedtuple():
    bite = Bite(1, 'fizz buzz')
    bite.level = 'Intermediate'
    assert bite.level == 'Intermediate'


def test_not_a_tuple():
    bite = Bite(1, 'fizz buzz')
    with pytest.raises(TypeError):
        number, title, level = bite
    assert astuple(bite) == (1, 'Fizz buzz', 'Beginner')


def test_not_frozen():
    bite = Bite(1, 'fizz buzz')
    try:
        bite.number = 2
    except FrozenInstanceError:
        pytest.fail('Bite should be mutable')


@pytest.mark.parametrize('title, expected', [
    ('', ''), ('  fizz BUZZ', '  fizz buzz'), ('123 ABC', '123 abc'),
])
def test_title_boundaries(title, expected):
    assert Bite(0, title).title == expected


def test_level_breaks_ties_and_empty_values_are_kept():
    assert Bite(-1, '', '') < Bite(-1, '', 'Beginner')
    assert Bite(-1, '', '').level == ''
    assert Bite(-1, '', '') != Bite(-1, '', 'Beginner')


def test_title_normalization_only_happens_at_construction():
    bite = Bite(1, 'first TITLE')
    bite.title = 'new TITLE'
    assert bite.title == 'new TITLE'
''',
    "mutations": [
        {"name": 'not_ordered', "old": '@dataclass(order=True)', "new": '@dataclass'},
        {"name": 'titlecase_instead_of_capitalize', "old": 'self.title = self.title.capitalize()', "new": 'self.title = self.title.title()'},
        {"name": 'empty_title_index_error', "old": 'self.title = self.title.capitalize()', "new": 'self.title = self.title[0].upper() + self.title[1:].lower()'},
    ],
    "reference": '''from dataclasses import dataclass


@dataclass(order=True)
class Bite:
    number: int
    title: str
    level: str = 'Beginner'

    def __post_init__(self):
        self.title = self.title.capitalize()
''',
}
