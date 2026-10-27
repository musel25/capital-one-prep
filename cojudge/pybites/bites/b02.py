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
