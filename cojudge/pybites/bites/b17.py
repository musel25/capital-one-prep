"""Bite: Building a karma app - implement the user class (recreated tests and template)."""

SPEC = {
    "title": "Building a karma app - implement the user class",
    "module": "karma",
    "template": '''from collections import namedtuple

Transaction = namedtuple('Transaction', 'giver points')


class User:
    pass
''',
    "tests": '''import pytest

from karma import Transaction, User


@pytest.fixture
def users():
    alice, bob, tim = User('alice'), User('bob'), User('tim')
    alice + Transaction(giver=bob, points=1)
    alice + Transaction(giver=tim, points=2)
    alice + Transaction(giver=bob, points=3)
    bob + Transaction(giver=alice, points=1)
    return alice, bob, tim


def test_name():
    assert User('alice').name == 'alice'


def test_karma(users):
    alice, bob, tim = users
    assert alice.karma == 6
    assert bob.karma == 1
    assert tim.karma == 0


def test_points(users):
    alice, bob, tim = users
    assert alice.points == [1, 2, 3]
    assert tim.points == []


def test_fans(users):
    alice, bob, tim = users
    assert alice.fans == 2  # bob gave twice, he is one fan
    assert bob.fans == 1
    assert tim.fans == 0


def test_str(users):
    alice, bob, tim = users
    assert str(alice) == 'alice has a karma of 6 and 2 fans'
    assert str(bob) == 'bob has a karma of 1 and 1 fan'
    assert str(tim) == 'tim has a karma of 0 and 0 fans'


def test_comparison(users):
    alice, bob, tim = users
    assert tim < bob < alice
    assert alice > bob
    assert [u.name for u in sorted([alice, tim, bob])] == ['tim', 'bob', 'alice']


def test_add_more_karma(users):
    alice, bob, tim = users
    tim + Transaction(giver=alice, points=5)
    assert tim.karma == 5
    assert tim > bob
    assert str(tim) == 'tim has a karma of 5 and 1 fan'


def test_properties():
    for name in ('karma', 'points', 'fans'):
        assert isinstance(User.__dict__[name], property)


def test_users_do_not_share_state():
    one, two = User('one'), User('two')
    one + Transaction(giver=two, points=1)
    assert two.points == []
''',
    "reference": '''from collections import namedtuple

Transaction = namedtuple('Transaction', 'giver points')


class User:

    def __init__(self, name):
        self.name = name
        self._transactions = []

    @property
    def karma(self):
        return sum(self.points)

    @property
    def points(self):
        return [t.points for t in self._transactions]

    @property
    def fans(self):
        return len({t.giver.name for t in self._transactions})

    def __add__(self, transaction):
        self._transactions.append(transaction)
        return self

    def __lt__(self, other):
        return self.karma < other.karma

    def __str__(self):
        fans = self.fans
        return f"{self.name} has a karma of {self.karma} and {fans} {'fan' if fans == 1 else 'fans'}"
''',
}
