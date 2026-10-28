"""Bite: Ninja rankings (recreated tests and template)."""

SPEC = {
    "title": "Ninja rankings",
    "module": "ninjas",
    "contract": "Ninja takes a string name and a nonnegative integer bites count. Comparisons "
                "between Ninjas use bites only. Rankings accepts Ninja objects and retains them. "
                "highest and lowest return lists, defaulting to one result; count is a nonnegative "
                "integer. A zero count returns an empty list; a large count returns all available "
                "results. dump removes and returns one lowest Ninja, or raises IndexError when "
                "empty. Local clarification: pair_up makes at most min(count, len(rankings)//2) "
                "pairs, so no person is reused or paired with itself. Its default count is 3. "
                "Ranking queries and pairing do not remove people. Equal-score order is unspecified. "
                "Add each person once and do not change bites after adding. Invalid argument types, "
                "negative counts, and mixed-type comparisons are outside this exercise.",
    "mutations": [
        {"name": "reuses_people_in_pairs", "old": "count = min(count, len(self._ninjas) // 2)", "new": "count = count"},
        {"name": "highest_is_reversed", "old": "return self._ninjas[:count]", "new": "return self._ninjas[::-1][:count]"},
        {"name": "dump_highest", "old": "return self._ninjas.pop()", "new": "return self._ninjas.pop(0)"},
    ],
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


@pytest.mark.parametrize("size,count", [(0, 3), (1, 3), (3, 3), (4, 3),
                                         (7, 99), (6, 3), (6, 0)])
def test_pairs_use_each_person_at_most_once(size, count):
    ranking = Rankings()
    for score in range(size):
        ranking.add(Ninja(str(score), score))
    pairs = ranking.pair_up(count)
    expected_count = min(count, size // 2)
    assert [(high.bites, low.bites) for high, low in pairs] == [
        (size - 1 - offset, offset) for offset in range(expected_count)]
    people = [id(person) for pair in pairs for person in pair]
    assert len(set(people)) == len(people)
    assert len(ranking) == size


def test_empty_ranking_queries_and_dump():
    ranking = Rankings()
    assert ranking.highest() == []
    assert ranking.lowest() == []
    assert ranking.pair_up() == []
    with pytest.raises(IndexError):
        ranking.dump()


def test_zero_and_large_query_counts_and_last_dump():
    ranking = Rankings()
    person = Ninja('', 0)
    ranking.add(person)
    assert ranking.highest(0) == ranking.lowest(0) == []
    assert ranking.highest(99)[0] is person
    assert ranking.lowest(99)[0] is person
    result = ranking.highest(99)
    result.clear()
    assert len(ranking) == 1
    assert ranking.dump() is person
    assert len(ranking) == 0


def test_equal_scores_and_separate_rankings():
    one, two = Ninja('a', 0), Ninja('b', 0)
    assert one == two
    assert not one < two
    assert not one > two
    ranking = Rankings()
    ranking.add(one)
    ranking.add(two)
    assert {id(n) for n in ranking.highest(99)} == {id(one), id(two)}
    assert len(Rankings()) == 0
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
        count = min(count, len(self._ninjas) // 2)
        return list(zip(self.highest(count), self.lowest(count)))
''',
}
