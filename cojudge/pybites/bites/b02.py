"""Bite: Complete a user class: properties and representation dunder methods (recreated)."""

SPEC = {
    "title": "Complete a user class: properties and representation dunder methods",
    "module": "user",
    "template": '''class User:
    """A User class
       (Django's User model inspired us)
    """

    def __init__(self, first_name, last_name):
        """Constructor, base values"""
        self.first_name = first_name
        self.last_name = last_name

    @property
    def get_full_name(self):
        """Return first and last name separated by a whitespace
           and using title case for both.
        """
        # TODO 1: your code
        pass

    @property
    def username(self):
        """A username consists of the first char of
           the user's first_name and the first 7 chars
           of the user's last_name, both lowercased.
        """
        # TODO 2: your code
        pass

    # TODO 3: your code
    #
    # add a __str__ and a __repr__
    # "__repr__ is for devs, __str__ is for customers"
    #
    # see the TESTS for the required output
    #
    # Hint for the __repr__ twist: do not hard-code the class name.
    # A subclass should show its own name: self.__class__.__name__
''',
    "tests": '''from user import User


def test_bob():
    bob = User('bob', 'belderbos')
    assert bob.get_full_name == 'Bob Belderbos'
    assert bob.username == 'bbelderb'  # lowercase, max 8 chars
    assert str(bob) == 'Bob Belderbos (bbelderb)'
    assert repr(bob) == 'User("bob", "belderbos")'


def test_julian():
    julian = User('julian', 'sequeira')
    assert julian.get_full_name == 'Julian Sequeira'
    assert julian.username == 'jsequeir'
    assert str(julian) == 'Julian Sequeira (jsequeir)'
    assert repr(julian) == 'User("julian", "sequeira")'


def test_short_last_name_and_mixed_case():
    tim = User('TIM', 'Lo')
    assert tim.get_full_name == 'Tim Lo'
    assert tim.username == 'tlo'
    assert str(tim) == 'Tim Lo (tlo)'
    assert repr(tim) == 'User("TIM", "Lo")'


def test_properties_are_properties():
    assert isinstance(User.__dict__['get_full_name'], property)
    assert isinstance(User.__dict__['username'], property)


def test_values_follow_attribute_changes():
    ann = User('ann', 'smith')
    ann.last_name = 'johnson'
    assert ann.username == 'ajohnson'
    assert ann.get_full_name == 'Ann Johnson'


def test_repr_of_a_subclass():
    """The twist: repr uses the class name of the instance."""
    class Admin(User):
        pass
    admin = Admin('ada', 'lovelace')
    assert repr(admin) == 'Admin("ada", "lovelace")'
    assert str(admin) == 'Ada Lovelace (alovelac)'
''',
    "reference": '''class User:
    """A User class
       (Django's User model inspired us)
    """

    def __init__(self, first_name, last_name):
        """Constructor, base values"""
        self.first_name = first_name
        self.last_name = last_name

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def username(self):
        return (self.first_name[0] + self.last_name[:7]).lower()

    def __str__(self):
        return f"{self.get_full_name} ({self.username})"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.first_name}", "{self.last_name}")'
''',
}

SPEC["contract"] = (
    "first_name and last_name are non-empty strings of ASCII letters A-Z or a-z. "
    "Empty names, whitespace, punctuation, non-ASCII names and other types are outside "
    "the contract; no validation is required for them. get_full_name returns both "
    "title-cased names with one space. username lowercases the first letter of "
    "first_name followed by at most seven letters of last_name. Both properties "
    "use the current attributes. str returns 'Full Name (username)'. repr returns "
    "ClassName(\"first_name\", \"last_name\") with the original case and the instance's class name. "
    "Each instance keeps its own names."
)
SPEC["tests"] += '''


def test_one_letter_names():
    user = User('A', 'B')
    assert user.get_full_name == 'A B'
    assert user.username == 'ab'
    assert str(user) == 'A B (ab)'
    assert repr(user) == 'User("A", "B")'


def test_surname_at_and_above_seven_letters():
    assert User('Ada', 'Abcdefg').username == 'aabcdefg'
    assert User('Ada', 'Abcdefgh').username == 'aabcdefg'


def test_both_names_can_change_without_affecting_another_user():
    user, other = User('ann', 'smith'), User('bob', 'jones')
    user.first_name = 'EVE'
    user.last_name = 'BROWN'
    assert user.get_full_name == 'Eve Brown'
    assert user.username == 'ebrown'
    assert str(user) == 'Eve Brown (ebrown)'
    assert repr(user) == 'User("EVE", "BROWN")'
    assert other.get_full_name == 'Bob Jones'
    assert other.username == 'bjones'
'''
SPEC["mutations"] = [
    {"name": "surname truncated at six letters", "old": "self.last_name[:7]", "new": "self.last_name[:6]"},
    {"name": "surname truncated at eight letters", "old": "self.last_name[:7]", "new": "self.last_name[:8]"},
    {"name": "hard-coded repr class", "old": "self.__class__.__name__", "new": '"User"'},
    {"name": "use final first-name letter", "old": "self.first_name[0]", "new": "self.first_name[-1]"},
]
