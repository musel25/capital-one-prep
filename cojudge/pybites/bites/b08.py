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

SPEC["contract"] = (
    "name is a string without newline characters. Empty names and duplicate names "
    "are valid. Apply str.title without trimming whitespace. Each new Animal gets "
    "the next shared integer ID; the first ID is 10001. str returns '<ID>. <Name>'. "
    "The classmethod zoo returns all created animals in creation order, joined "
    "with newlines and no trailing newline. An empty zoo returns ''. Repeated "
    "calls to str or zoo do not create animals or change IDs. Subclasses, direct "
    "attribute changes and other input types are outside the contract; no "
    "validation is required for them."
)
# This check must run before the existing tests create their first Animal.
SPEC["tests"] = SPEC["tests"].replace(
    "def test_zoo_string():",
    "def test_empty_zoo():\n    assert Animal.zoo() == ''\n\n\ndef test_zoo_string():",
    1,
)
SPEC["tests"] += '''


def test_duplicate_names_are_distinct_animals():
    first, second = Animal('DOG'), Animal('DOG')
    number = int(str(first).split('.')[0])
    assert str(first) == f'{number}. Dog'
    assert str(second) == f'{number + 1}. Dog'
    assert Animal.zoo().splitlines()[-2:] == [str(first), str(second)]


def test_reading_zoo_and_str_does_not_change_sequence():
    first = Animal('parrot')
    text = str(first)
    snapshot = Animal.zoo()
    assert str(first) == text
    assert Animal.zoo() == snapshot
    second = Animal('owl')
    number = int(text.split('.')[0])
    assert str(second) == f'{number + 1}. Owl'
    assert str(first) == text


def test_empty_and_spaced_names_preserve_spacing():
    empty, spaced = Animal(''), Animal('  sNOW leopard  ')
    number = int(str(empty).split('.')[0])
    assert str(empty) == f'{number}. '
    assert str(spaced) == f'{number + 1}.   Snow Leopard  '
    assert Animal.zoo().endswith(str(empty) + '\\n' + str(spaced))
'''
SPEC["mutations"] = [
    {"name": "first ID is ten thousand", "old": "count(10001)", "new": "count(10000)"},
    {"name": "capitalize only first word", "old": "name.title()", "new": "name.capitalize()"},
    {"name": "trim name whitespace", "old": "name.title()", "new": "name.strip().title()"},
    {"name": "store animals in reverse order", "old": "Animal._animals.append(self)", "new": "Animal._animals.insert(0, self)"},
    {"name": "reset ID for each instance", "old": "self.number = next(Animal._sequence)", "new": "self.number = 10001"},
]
