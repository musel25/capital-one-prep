"""Bite: Complete a user class: properties and representation dunder methods (recreated)."""

SPEC = {
    "title": "Complete a user class: properties and representation dunder methods",
    "module": "user",
    "template": '''# What you practise
# -----------------
# 1. Properties: methods that you read like attributes (user.username, no
#    parentheses). They run on every read, so they follow later changes to
#    first_name and last_name.
# 2. The two text forms of an object:
#      str(user)   calls __str__   -> friendly text for people
#      repr(user)  calls __repr__  -> code-like text for developers
#
# Work in three steps. Every test checks all four members together, so finish
# all three steps before you run the tests. Submit also runs edge-case tests.
#
#   Step 1 -> get_full_name and username
#   Step 2 -> __str__
#   Step 3 -> __repr__ (test_repr_of_a_subclass checks the twist)


class User:
    """A User class (Django's User model inspired us)."""

    def __init__(self, first_name, last_name):
        """Constructor, base values. This part is complete."""
        self.first_name = first_name
        self.last_name = last_name

    # Step 1a: title case for both names, one space between them.
    #
    #     User('bob', 'belderbos').get_full_name  -> 'Bob Belderbos'
    #     User('TIM', 'Lo').get_full_name         -> 'Tim Lo'
    @property
    def get_full_name(self):
        """Return 'First Last' in title case."""
        # TODO: use str.title() on each name.
        ...

    # Step 1b: first letter of first_name + first 7 letters of last_name,
    # all lowercase. A short last name is used whole.
    #
    #     User('bob', 'belderbos').username  -> 'bbelderb'
    #     User('TIM', 'Lo').username         -> 'tlo'
    @property
    def username(self):
        """Return the lowercase username, at most 8 characters."""
        # TODO: slice first_name[0] and last_name[:7], then lowercase.
        ...

    # Step 2: the friendly form. Reuse the two properties.
    #
    #     str(User('bob', 'belderbos'))  -> 'Bob Belderbos (bbelderb)'
    #
    # TODO: define __str__(self).

    # Step 3: the developer form. Use the ORIGINAL names (not title case) and
    # double quotes. Do not type the class name: read it from the object with
    # type(self).__name__, so a subclass shows its own name.
    #
    #     repr(User('bob', 'belderbos'))   -> 'User("bob", "belderbos")'
    #     repr(Admin('ada', 'lovelace'))   -> 'Admin("ada", "lovelace")'
    #         (Admin is a subclass of User that a test defines)
    #
    # TODO: define __repr__(self).
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

SPEC["hints"] = [
    'Concept: str(obj) calls obj.__str__() and repr(obj) calls obj.__repr__(). Both must return a string. A property is read without parentheses, so inside __str__ write self.username, not self.username().',
    "Formats: get_full_name is f'{first.title()} {last.title()}'. username is (first_name[0] + last_name[:7]).lower(). A slice past the end of a string is safe: 'Lo'[:7] is 'Lo'.",
    'For __repr__, use the stored names exactly as given and the class name from the object: f\'{type(self).__name__}("{self.first_name}", "{self.last_name}")\'.',
]
