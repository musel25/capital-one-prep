"""Bite: Ninja rankings (recreated tests and template)."""

SPEC = {
    "title": "Ninja rankings",
    "module": "ninjas",
    "template": '''class Ninja:
    """
    The Ninja class will have the following features:

    string: name
    integer: bites
    support <, >, and ==, based on bites
    print out in the following format: [469] bob
    """
    pass


class Rankings:
    """
    The Rankings class will have the following features:

    method: add() that adds a Ninja object to the rankings
    method: dump() that removes/dumps the lowest ranking Ninja from Rankings
            and returns it
    method: highest() returns a list with the highest ranking Ninja, but it
            takes an optional count parameter indicating how many of the
            highest ranking Ninjas to return (highest first)
    method: lowest(), the same as highest but returns the lowest ranking
            Ninjas (lowest first), also supports an optional count parameter
    returns how many Ninjas are in Rankings when len() is called on it
    method: pair_up(), pairs up study partners, takes an optional count
            parameter (default 3) indicating how many pairs to make
    returns a list containing tuples of the paired up Ninja objects:
            (highest, lowest), (second highest, second lowest), ...
    """
    pass
''',
    "tests": '''import pytest

from ninjas import Ninja, Rankings


@pytest.fixture
def ninjas():
    return [Ninja("bob", 469), Ninja("julian", 487), Ninja("rhys", 287),
            Ninja("nick", 173), Ninja("martin", 213), Ninja("anthony", 96),
            Ninja("sam", 382)]


@pytest.fixture
def rankings(ninjas):
    ranking = Rankings()
    for ninja in ninjas:
        ranking.add(ninja)
    return ranking


def test_ninja():
    bob = Ninja("bob", 469)
    assert bob.name == "bob"
    assert bob.bites == 469
    assert str(bob) == "[469] bob"


def test_ninja_comparison():
    bob, julian, clone = Ninja("bob", 469), Ninja("julian", 487), Ninja("bob2", 469)
    assert bob < julian
    assert julian > bob
    assert bob == clone
    assert not bob == julian


def test_len(rankings):
    assert len(rankings) == 7
    assert len(Rankings()) == 0


def test_highest(rankings):
    assert [str(n) for n in rankings.highest()] == ["[487] julian"]
    assert [n.name for n in rankings.highest(3)] == ["julian", "bob", "sam"]


def test_lowest(rankings):
    assert [str(n) for n in rankings.lowest()] == ["[96] anthony"]
    assert [n.name for n in rankings.lowest(2)] == ["anthony", "nick"]


def test_dump(rankings):
    dumped = rankings.dump()
    assert str(dumped) == "[96] anthony"
    assert len(rankings) == 6
    assert rankings.lowest()[0].name == "nick"


def test_pair_up(rankings):
    pairs = rankings.pair_up()
    assert [(high.name, low.name) for high, low in pairs] == [
        ("julian", "anthony"), ("bob", "nick"), ("sam", "martin")]
    assert len(rankings) == 7


def test_pair_up_with_count(rankings):
    pairs = rankings.pair_up(count=1)
    assert len(pairs) == 1
    high, low = pairs[0]
    assert (str(high), str(low)) == ("[487] julian", "[96] anthony")


def test_add_after_ranking(rankings):
    rankings.add(Ninja("pro", 999))
    rankings.add(Ninja("newbie", 1))
    assert rankings.highest()[0].name == "pro"
    assert rankings.lowest()[0].name == "newbie"
    assert len(rankings) == 9
''',
    "reference": '''from functools import total_ordering


@total_ordering
class Ninja:
    def __init__(self, name, bites):
        self.name = name
        self.bites = bites

    def __eq__(self, other):
        return self.bites == other.bites

    def __lt__(self, other):
        return self.bites < other.bites

    def __str__(self):
        return f"[{self.bites}] {self.name}"


class Rankings:
    def __init__(self):
        self._ninjas = []

    def add(self, ninja):
        self._ninjas.append(ninja)
        self._ninjas.sort(reverse=True)

    def dump(self):
        return self._ninjas.pop()

    def highest(self, count=1):
        return self._ninjas[:count]

    def lowest(self, count=1):
        return self._ninjas[::-1][:count]

    def __len__(self):
        return len(self._ninjas)

    def pair_up(self, count=3):
        return list(zip(self.highest(count), self.lowest(count)))
''',
}
