"""Bite: Oop fun at the zoo (recreated tests and template)."""

SPEC = {
    "title": "Oop fun at the zoo",
    "module": "zoo",
    "template": '''class Animal:

    def __init__(self, name):
        pass

    def __str__(self):
        pass

    @classmethod
    def zoo(cls):
        pass
''',
    "tests": '''from zoo import Animal


def test_zoo_string():
    dog = Animal('dog')
    cat = Animal('cat')
    fish = Animal('fish')
    lion = Animal('lion')
    mouse = Animal('mouse')
    assert str(dog) == '10001. Dog'
    assert str(mouse) == '10005. Mouse'
    zoo = Animal.zoo()
    assert zoo == '\\n'.join(['10001. Dog', '10002. Cat', '10003. Fish',
                              '10004. Lion', '10005. Mouse'])


def test_next_animal_continues_the_sequence():
    horse = Animal('horse')
    assert str(horse) == '10006. Horse'
    assert Animal.zoo().splitlines()[-1] == '10006. Horse'
    assert len(Animal.zoo().splitlines()) == 6


def test_title_case():
    leopard = Animal('snow leopard')
    assert str(leopard) == '10007. Snow Leopard'


def test_zoo_is_a_classmethod():
    assert isinstance(Animal.__dict__['zoo'], classmethod)


def test_sequence_is_shared_by_all_instances():
    first, second = Animal('ant'), Animal('bee')
    number = int(str(first).split('.')[0])
    assert str(second) == f'{number + 1}. Bee'
''',
    "reference": '''from itertools import count


class Animal:
    _sequence = count(10001)
    _animals = []

    def __init__(self, name):
        self.name = name.title()
        self.number = next(Animal._sequence)
        Animal._animals.append(self)

    def __str__(self):
        return f"{self.number}. {self.name}"

    @classmethod
    def zoo(cls):
        return "\\n".join(str(animal) for animal in cls._animals)
''',
}
