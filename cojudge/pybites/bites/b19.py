"""Bite: Subclass the list built-in (recreated tests and template)."""

SPEC = {
    "title": "Subclass the list built-in",
    "module": "intlist",
    "notes": "As in the description's REPL example, numbers such as `1.0` are accepted; other types raise `TypeError`.",
    "template": '''class IntList(list):
    pass
''',
    "tests": '''import pytest

from intlist import IntList


def test_mean_and_median():
    mylist = IntList([1, 3, 5])
    assert mylist.mean == 3
    assert mylist.median == 3
    mylist.append(7)
    mylist.append(1.0)
    assert mylist.mean == pytest.approx(3.4)
    assert mylist.median == 3


def test_median_of_even_length():
    assert IntList([1, 2, 3, 4]).median == 2.5


def test_append_rejects_other_types():
    mylist = IntList([1, 3, 5])
    with pytest.raises(TypeError):
        mylist.append('a')
    with pytest.raises(TypeError):
        mylist.append(None)
    assert mylist == [1, 3, 5]


def test_append_a_list_of_numbers():
    mylist = IntList([1, 3, 5])
    mylist.append([2, 3])
    assert mylist == [1, 3, 5, 2, 3]
    with pytest.raises(TypeError):
        mylist.append([2, 'a'])
    assert mylist == [1, 3, 5, 2, 3]


def test_iadd():
    mylist = IntList([1, 3, 5])
    original = mylist
    mylist += [1]
    assert mylist == [1, 3, 5, 1]
    assert mylist is original
    with pytest.raises(TypeError):
        mylist += [1, 'a']
    assert original == [1, 3, 5, 1]


def test_add_returns_an_intlist():
    mylist = IntList([2, 4])
    result = mylist + [6]
    assert result == [2, 4, 6]
    assert isinstance(result, IntList)
    assert result.mean == 4
    assert mylist == [2, 4]
    with pytest.raises(TypeError):
        mylist + ['x']


def test_is_a_list_and_properties():
    assert issubclass(IntList, list)
    assert isinstance(IntList.__dict__['mean'], property)
    assert isinstance(IntList.__dict__['median'], property)
''',
    "reference": '''from statistics import mean, median


class IntList(list):

    @staticmethod
    def _validate(values):
        values = list(values)
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"only numbers allowed, not {type(value).__name__}")
        return values

    @property
    def mean(self):
        return mean(self)

    @property
    def median(self):
        return median(self)

    def append(self, value):
        if isinstance(value, list):
            super().extend(self._validate(value))
        else:
            super().append(*self._validate([value]))

    def __add__(self, other):
        return IntList(list(self) + self._validate(other))

    def __iadd__(self, other):
        return super().__iadd__(self._validate(other))
''',
}
