"""Bite: Subclass the dict built-in (recreated tests and template)."""

SPEC = {
    "title": "Subclass the dict built-in",
    "module": "bdaydict",
    "template": '''from collections import UserDict

MSG = 'Hey {}, there are more people with your birthday!'


class BirthdayDict(UserDict):
    """Override UserDict to print a message every time a new person is added
       that has the same birthday (day+month) as somebody already in the dict"""

    def __setitem__(self, name, birthday):
        pass
''',
    "tests": '''from collections import UserDict
from datetime import date

from bdaydict import MSG, BirthdayDict


def test_birthday_dict(capsys):
    bd = BirthdayDict()
    bd['bob'] = date(1987, 6, 15)
    bd['tim'] = date(1984, 7, 15)
    assert capsys.readouterr().out == ''
    bd['mary'] = date(1987, 6, 15)  # whole date match
    assert capsys.readouterr().out.strip() == MSG.format('mary')
    bd['sara'] = date(1987, 6, 14)
    assert capsys.readouterr().out == ''
    bd['mike'] = date(1981, 7, 15)  # day + month match
    assert capsys.readouterr().out.strip() == MSG.format('mike')


def test_values_are_stored():
    bd = BirthdayDict()
    bd['bob'] = date(1987, 6, 15)
    bd['mary'] = date(1990, 6, 15)
    assert bd['bob'] == date(1987, 6, 15)
    assert bd['mary'] == date(1990, 6, 15)
    assert len(bd) == 2
    assert dict(bd) == {'bob': date(1987, 6, 15), 'mary': date(1990, 6, 15)}


def test_same_year_and_month_is_not_a_match(capsys):
    bd = BirthdayDict()
    bd['ann'] = date(2000, 1, 1)
    bd['ben'] = date(2000, 1, 2)
    bd['cid'] = date(2000, 2, 1)
    assert capsys.readouterr().out == ''


def test_message_once_per_new_person(capsys):
    bd = BirthdayDict()
    bd['a'] = date(1970, 12, 24)
    bd['b'] = date(1980, 12, 24)
    bd['c'] = date(1990, 12, 24)
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == [MSG.format('b'), MSG.format('c')]


def test_update_and_constructor_use_setitem(capsys):
    bd = BirthdayDict({'x': date(1999, 3, 3)})
    bd.update({'y': date(2001, 3, 3)})
    assert capsys.readouterr().out.strip() == MSG.format('y')
    assert bd['y'] == date(2001, 3, 3)


def test_subclasses_userdict():
    assert issubclass(BirthdayDict, UserDict)
''',
    "reference": '''from collections import UserDict

MSG = 'Hey {}, there are more people with your birthday!'


class BirthdayDict(UserDict):
    """Override UserDict to print a message every time a new person is added
       that has the same birthday (day+month) as somebody already in the dict"""

    def __setitem__(self, name, birthday):
        if any((d.month, d.day) == (birthday.month, birthday.day) for d in self.data.values()):
            print(MSG.format(name))
        super().__setitem__(name, birthday)
''',
}

SPEC["contract"] = (
    "Use string name keys and datetime.date birthday values. Each assigned name "
    "is new to this dictionary. Empty dictionaries and February 29 birthdays are "
    "valid. Store every entry. Before adding it, compare its month and day with "
    "the stored birthdays, ignoring the year. Print MSG.format(name) followed by "
    "one newline if any match exists, once per added name. Otherwise print nothing. "
    "Construction and update must apply the same rule. Existing-key replacement, "
    "datetime values and other input types are outside the contract; no validation "
    "is required for them. Instances keep separate entries."
)
SPEC["tests"] += '''


def test_leap_day_and_exact_single_newline(capsys):
    bd = BirthdayDict()
    bd['first'] = date(2000, 2, 29)
    assert capsys.readouterr().out == ''
    bd['second'] = date(2004, 2, 29)
    assert capsys.readouterr().out == MSG.format('second') + '\\n'
    bd['third'] = date(2008, 2, 29)
    assert capsys.readouterr().out == MSG.format('third') + '\\n'
    assert len(bd) == 3


def test_constructor_detects_matches_within_its_input(capsys):
    bd = BirthdayDict({'a': date(1970, 12, 31), 'b': date(2000, 12, 31)})
    assert capsys.readouterr().out == MSG.format('b') + '\\n'
    assert bd['a'] == date(1970, 12, 31)
    assert bd['b'] == date(2000, 12, 31)


def test_instances_do_not_share_birthdays(capsys):
    one, two = BirthdayDict(), BirthdayDict()
    one['a'] = date(1990, 1, 1)
    two['b'] = date(2000, 1, 1)
    assert capsys.readouterr().out == ''
    assert list(one) == ['a']
    assert list(two) == ['b']


def test_empty_constructor_and_nonmatching_update(capsys):
    bd = BirthdayDict({})
    assert len(bd) == 0
    bd.update({'a': date(2001, 1, 1), 'b': date(2001, 1, 2)})
    assert capsys.readouterr().out == ''
    assert len(bd) == 2
'''
SPEC["mutations"] = [
    {"name": "compare whole dates", "old": "(d.month, d.day) == (birthday.month, birthday.day)", "new": "d == birthday"},
    {"name": "compare month only", "old": "(d.month, d.day) == (birthday.month, birthday.day)", "new": "d.month == birthday.month"},
    {"name": "compare day only", "old": "(d.month, d.day) == (birthday.month, birthday.day)", "new": "d.day == birthday.day"},
    {"name": "require every birthday to match", "old": "if any(", "new": "if all("},
    {"name": "omit message newline", "old": "print(MSG.format(name))", "new": "print(MSG.format(name), end='')"},
]
