"""Bite: Multiple inheritance (__mro__) (recreated tests and template)."""

SPEC = {
    "title": "Multiple inheritance (__mro__)",
    "module": "mro",
    "template": '''class Person:
    pass


class Father:
    pass


class Mother:
    pass


class Child:
    pass
''',
    "tests": '''import inspect

import pytest

from mro import Child, Father, Mother, Person


def test_mro():
    assert [cls.__name__ for cls in Child.__mro__] == ['Child', 'Father', 'Mother', 'Person', 'object']


def test_inheritance():
    assert issubclass(Father, Person)
    assert issubclass(Mother, Person)
    assert issubclass(Child, Father)
    assert issubclass(Child, Mother)


@pytest.mark.parametrize("cls, expected", [
    (Person, 'I am a person'),
    (Father, 'I am a person and cool daddy'),
    (Mother, 'I am a person and awesome mom'),
    (Child, 'I am the coolest kid'),
])
def test_str(cls, expected):
    assert str(cls()) == expected


@pytest.mark.parametrize("cls", [Father, Mother, Child])
def test_person_text_only_in_base_class(cls):
    assert 'I am a person' in inspect.getsource(Person)
    assert 'I am a person' not in inspect.getsource(cls)


def test_print(capsys):
    for cls in (Person, Father, Mother, Child):
        print(cls())
    assert capsys.readouterr().out.splitlines() == [
        'I am a person', 'I am a person and cool daddy',
        'I am a person and awesome mom', 'I am the coolest kid']
''',
    "reference": '''class Person:
    def __str__(self):
        return 'I am a person'


class Father(Person):
    def __str__(self):
        return f'{super().__str__()} and cool daddy'


class Mother(Person):
    def __str__(self):
        return f'{super().__str__()} and awesome mom'


class Child(Father, Mother):
    def __str__(self):
        return 'I am the coolest kid'
''',
}
