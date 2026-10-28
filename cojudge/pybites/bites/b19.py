"""Bite: Subclass the list built-in (recreated tests and template)."""

SPEC = {
    "title": "Subclass the list built-in",
    "module": "intlist",
    "contract": "Construct an IntList from an iterable of finite int or float values, with bool "
                "excluded. append accepts one number or a list of numbers. + and += accept lists "
                "of numbers. These three operations raise TypeError for invalid elements and do "
                "not change the list on failure. + returns a new IntList; += preserves identity. "
                "mean and median are read-only properties and do not reorder the list. On an empty "
                "list they raise statistics.StatisticsError. Constructor validation, other mutation "
                "methods, nonfinite numbers, and non-list operands for + or += are outside this exercise.",
    "mutations": [
        {"name": "bool_accepted", "old": "isinstance(value, bool) or not isinstance(value, (int, float))", "new": "not isinstance(value, (int, float))"},
        {"name": "median_uses_mean", "old": "return median(self)", "new": "return mean(self)"},
        {"name": "addition_returns_plain_list", "old": "return IntList(list(self) + self._validate(other))", "new": "return list(self) + self._validate(other)"},
    ],
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


def test_empty_properties():
    from statistics import StatisticsError
    values = IntList()
    for name in ('mean', 'median'):
        with pytest.raises(StatisticsError):
            getattr(values, name)
    values.append([])
    assert values == []
    assert values + [] == []
    alias = values
    values += []
    assert values is alias
    assert values == []


def test_fractional_negative_values_and_unsorted_median():
    values = IntList([9, -2, 1.5])
    assert values.mean == pytest.approx(8.5 / 3)
    assert values.median == 1.5
    assert values == [9, -2, 1.5]
    single = IntList([-2.5])
    assert single.mean == single.median == -2.5
    for name in ('mean', 'median'):
        with pytest.raises(AttributeError):
            setattr(values, name, 1)


@pytest.mark.parametrize("bad", [True, False, '2', None, [2]])
def test_invalid_elements_are_atomic_in_all_named_operations(bad):
    values = IntList([1])
    with pytest.raises(TypeError):
        values.append([2, bad])
    assert values == [1]
    with pytest.raises(TypeError):
        values + [2, bad]
    assert values == [1]
    with pytest.raises(TypeError):
        values += [2, bad]
    assert values == [1]


def test_append_rejects_scalar_bool():
    values = IntList([1])
    with pytest.raises(TypeError):
        values.append(True)
    assert values == [1]
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
